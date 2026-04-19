#!/usr/bin/env python3
"""
OpenClaw Daily — Episode Release Pipeline
From: approved EN audio + cover from the pre-approval build flow
To:   EN feed/site published immediately after approval, translations generated and
      published after translated audio exists, and the EN video lane started early.

Uses Minimax M2.7 API for all translations.

Usage:
  /opt/homebrew/bin/python3.14 scripts/release_episode.py 25
  /opt/homebrew/bin/python3.14 scripts/release_episode.py 25 --from-phase tts
  /opt/homebrew/bin/python3.14 scripts/release_episode.py 25 --pub-date "Mon, 07 Apr 2026 18:00:00 +0000"
"""

import argparse
import asyncio
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import migrate_media_releases as media_releases

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
WEBSITE_DIR = Path.home() / ".openclaw/workspace/websiteBuilder"
WEBSITE_PODCAST_IMG = WEBSITE_DIR / "frontend/public/images/podcast"
WORKSPACE_DIR = Path.home() / ".openclaw/workspace"

LANGS = ["es", "de", "pt", "hi"]
LANG_NAMES = {
    "es": "Latin American Spanish",
    "de": "German",
    "pt": "Brazilian Portuguese",
    "hi": "Hindi",
}
TITLE_PREFIXES = {"es": "Episodio", "de": "Folge", "pt": "Episódio", "hi": "एपिसोड"}
SHOW_NOTES_CTA = {
    "es": "Notas del episodio:",
    "de": "Episodennotizen:",
    "pt": "Notas do episódio:",
    "hi": "एपिसोड नोट्स:",
}
LANG_LINKS = {
    "es": "https://tobyonfitnesstech.com/es/podcasts/episode-{ep}/",
    "de": "https://tobyonfitnesstech.com/de/podcasts/episode-{ep}/",
    "pt": "https://tobyonfitnesstech.com/pt/podcasts/episode-{ep}/",
    "hi": "https://tobyonfitnesstech.com/hi/podcasts/episode-{ep}/",
}
CDN_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio"

SERIAL_PHASES = [
    "setup",
    "en-feed",
    "en-publish",
    "en-video",
    "translate",
    "tts",
    "covers",
    "translated-cdn",
    "translated-feeds",
    "qc",
    "publish-translations",
    "youtube",
    "discord",
]
PHASE_ALIASES = {
    "feeds": "en-feed",
    "cdn": "translated-cdn",
    "publish": "publish-translations",
    "video": "en-video",
}
FULL_RELEASE_ORDER = [
    "setup",
    "en-feed",
    "en-publish",
    "en-video",
    "translate",
    "tts",
    "covers",
    "translated-cdn",
    "translated-feeds",
    "qc",
    "publish-translations",
    "youtube",
    "discord",
]
TRANSLATION_LANE_ORDER = [
    "translate",
    "tts",
    "covers",
    "translated-cdn",
    "translated-feeds",
    "qc",
    "publish-translations",
]
LEGACY_ONLY_PHASES = {"feeds", "cdn", "publish"}
CLI_PHASE_CHOICES = SERIAL_PHASES + ["feeds", "cdn", "publish", "video"]

# ── Helpers ──────────────────────────────────────────────────────────────────

BUILD_LOG_CHANNEL_ID = "1485243812442804327"

def log(msg, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{msg}", flush=True)

def build_log(msg, ep_num=None):
    """Post a short status line to #build-log on Discord. Fire-and-forget — never raises."""
    import urllib.request, urllib.error
    try:
        token = load_env_key("DISCORD_BOT_TOKEN")
        prefix = f"EP{ep_num:03d} " if ep_num is not None else ""
        body = json.dumps({"content": f"{prefix}{msg}"}).encode()
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{BUILD_LOG_CHANNEL_ID}/messages",
            data=body, method="POST",
            headers={
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json",
                "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
            }
        )
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception:
        pass  # never block the pipeline over a log post

def run(cmd, cwd=None, check=True, env=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(str(c) for c in cmd)}\n{result.stderr}")
    return result

def ffprobe_duration_str(path):
    """Returns HH:MM:SS or MM:SS string."""
    r = run(["/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "csv=p=0", str(path)])
    secs = float(r.stdout.strip())
    m, s = divmod(int(secs), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

def load_env_key(name):
    env_file = Path.home() / ".openclaw/.env"
    for line in env_file.read_text().splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip()
    return os.environ.get(name, "")

def normalize_phase_name(name):
    phase = (name or "").strip().lower()
    return PHASE_ALIASES.get(phase, phase)

def phase_completed(state, phase):
    return phase in set(state.get("completed_phases", []))

def mark_phase_complete(ep_num, state, phase):
    completed = state.setdefault("completed_phases", [])
    if phase not in completed:
        completed.append(phase)
    save_state(ep_num, state)

def git_add_paths(repo_dir, paths):
    ordered = []
    seen = set()
    for path in paths:
        if not path or path in seen:
            continue
        seen.add(path)
        ordered.append(path)
    if ordered:
        run(["git", "add", "--"] + ordered, cwd=str(repo_dir))

def ensure_website_cover(ep_num, lang=None):
    ep_str = f"{ep_num:03d}"
    if lang:
        src = PODCAST_DIR / "images" / f"episode_{ep_str}_cover_{lang}.png"
        dst = WEBSITE_PODCAST_IMG / f"episode_{ep_str}_cover_{lang}.png"
    else:
        src = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
        dst = WEBSITE_PODCAST_IMG / f"episode_{ep_str}_cover.png"
    if src.exists():
        WEBSITE_PODCAST_IMG.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
    return dst

def git_commit_if_needed(repo_dir, message, env=None, extra_paths=None, allow_empty=False):
    git_add_paths(repo_dir, list(extra_paths or []))
    diff = run(["git", "diff", "--cached", "--quiet"], cwd=str(repo_dir), check=False)
    if diff.returncode == 0 and not allow_empty:
        return False
    commit_cmd = ["git", "commit", "-m", message]
    if allow_empty:
        commit_cmd.insert(2, "--allow-empty")
    run(commit_cmd, cwd=str(repo_dir), env=env)
    run(["git", "push"], cwd=str(repo_dir))
    return True

def collapse_ws(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_section(notes, heading):
    pattern = rf"^## {re.escape(heading)}\s*\n(.+?)(?=\n## |\Z)"
    match = re.search(pattern, notes, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_episode_title(notes, ep_num):
    title = re.search(r"^## Episode Title\s*\n\*\*(.+?)\*\*", notes, re.MULTILINE)
    return title.group(1).strip() if title else f"Episode {ep_num}"

def extract_tagline(notes):
    return collapse_ws(extract_section(notes, "Tagline"))

def extract_feed_description(notes):
    feed_desc = collapse_ws(extract_section(notes, "Feed Description"))
    if feed_desc:
        return feed_desc

    tagline = extract_tagline(notes)
    if tagline:
        return tagline

    intro = re.search(r"```md\s*\n.*?\n\n(.+?)(?=\n\n\[|\n```)", notes, re.DOTALL)
    if intro:
        return collapse_ws(intro.group(1))

    return ""

def strip_title_prefix(title):
    if ": " in title:
        return title.split(": ", 1)[1].strip()
    return title.strip()

def fallback_cover_lines(title):
    words = strip_title_prefix(title).split()
    if not words:
        return "", ""
    if len(words) <= 4:
        return " ".join(words).upper(), ""

    split_at = max(2, min(4, len(words) // 2))
    line1 = " ".join(words[:split_at]).upper()
    line2 = " ".join(words[split_at:]).upper()
    return line1, line2

def normalize_translated_metadata(meta, ep_num, prefix, fallback_title, fallback_tagline):
    normalized = dict(meta or {})
    title = collapse_ws(normalized.get("title", "")) or f"{prefix} {ep_num}: {fallback_title}"
    normalized["title"] = title
    normalized["description"] = collapse_ws(normalized.get("description", "")) or fallback_tagline or fallback_title

    line1 = collapse_ws(normalized.get("cover_line1", "")).upper()
    line2 = collapse_ws(normalized.get("cover_line2", "")).upper()
    if not line1:
        line1, fallback_line2 = fallback_cover_lines(title)
        if not line2:
            line2 = fallback_line2
    normalized["cover_line1"] = line1
    normalized["cover_line2"] = line2

    tagline = collapse_ws(normalized.get("cover_tagline", ""))
    normalized["cover_tagline"] = tagline or strip_title_prefix(title)
    return normalized

# ── Minimax translation ───────────────────────────────────────────────────────

def gemini_call(prompt, max_tokens=4000, retries=3):
    """Call Minimax M2.7, strip <think> blocks, return clean text. Retries on empty output."""
    import openai
    key = load_env_key("MINIMAX_API_KEY")
    client = openai.OpenAI(
        base_url="https://api.minimaxi.chat/v1",
        api_key=key,
        timeout=180.0,
    )
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            r = client.chat.completions.create(
                model="MiniMax-M2.7",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            raw = r.choices[0].message.content or ""
            clean = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
            if clean:
                return clean
            # Empty response — retry
            log(f"    ⚠️  Empty response (attempt {attempt}/{retries}), retrying...", indent=2)
            time.sleep(3 * attempt)
        except Exception as e:
            last_err = e
            log(f"    ⚠️  API error (attempt {attempt}/{retries}): {e}", indent=2)
            time.sleep(5 * attempt)
    raise RuntimeError(f"Minimax API failed after {retries} attempts. Last error: {last_err}")

def translate_metadata(ep_num, lang):
    """Returns dict: title, description, cover_line1, cover_line2, cover_tagline."""
    lang_name = LANG_NAMES[lang]
    prefix = TITLE_PREFIXES[lang]

    # Read show notes for EN title, tagline, description
    show_notes_path = PODCAST_DIR / f"show_notes_episode_{ep_num:03d}.md"
    notes = show_notes_path.read_text()

    # Extract title, tagline, description from show notes
    en_title = extract_episode_title(notes, ep_num)
    en_tagline = extract_tagline(notes)
    en_desc = extract_feed_description(notes) or en_tagline or en_title

    # Cover text - extract from cover script if it exists, else derive from title
    cover_script = SCRIPTS_DIR / f"generate_episode_{ep_num:03d}_cover.py"
    line1, line2, cover_tag = "", "", ""
    if cover_script.exists():
        cs = cover_script.read_text()
        l1m = re.search(r'LINE1\s*=\s*["\'](.+?)["\']', cs)
        l2m = re.search(r'LINE2\s*=\s*["\'](.+?)["\']', cs)
        ctm = re.search(r'TAG_LINE\s*=\s*["\'](.+?)["\']', cs)
        line1 = l1m.group(1) if l1m else en_title.upper().split()[0]
        line2 = l2m.group(1) if l2m else ""
        cover_tag = ctm.group(1) if ctm else en_tagline

    prompt = f"""Translate this podcast episode metadata from English to {lang_name}.
Return ONLY valid JSON, no other text, no markdown fences.

English episode title: "{en_title}"
English tagline: "{en_tagline}"
English podcast description (2-3 sentences): "{en_desc[:500]}"
English cover title line 1 (ALL CAPS, 2-4 words): "{line1}"
English cover title line 2 (ALL CAPS, 2-4 words): "{line2}"
English cover tagline (short phrase): "{cover_tag}"
Episode number: {ep_num}
Title prefix for this language (e.g. "Episodio"): "{prefix}"

Return JSON with these exact keys:
{{
  "title": "{prefix} {ep_num}: <translated episode title>",
  "description": "<translated 2-3 sentence description>",
  "cover_line1": "<translated line 1 in ALL CAPS>",
  "cover_line2": "<translated line 2 in ALL CAPS>",
  "cover_tagline": "<translated short tagline phrase>"
}}"""

    raw = gemini_call(prompt, max_tokens=4000)
    # Extract JSON from response
    json_m = re.search(r'\{[\s\S]*\}', raw)
    if not json_m:
        raise ValueError(f"No JSON in metadata translation for {lang}: {raw[:200]}")
    return normalize_translated_metadata(
        json.loads(json_m.group(0)),
        ep_num,
        prefix,
        en_title,
        en_tagline or en_desc,
    )

TRANSCRIPT_SPEAKER_RE = re.compile(r"^\[(NOVA|ALLOY)\]:\s*(.+)$", re.DOTALL)
TRANSCRIPT_LEAK_RE = re.compile(
    r"(speaker tags exactly|do not translate|let me re-read|i(?:'|’)ll continue|"
    r"i recognize the linguistic complexity|the current technological landscape|"
    r"translate the following|output only the translated|keep \[nova\]|keep \[alloy\])",
    re.IGNORECASE,
)
UNEXPECTED_SCRIPT_RE = {
    "es": re.compile(r"[\u0400-\u04FF]"),
    "de": re.compile(r"[\u0400-\u04FF]"),
    "pt": re.compile(r"[\u0400-\u04FF]"),
}

def transcript_paragraphs(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]

def validate_language_scripts(text, lang, label):
    pattern = UNEXPECTED_SCRIPT_RE.get(lang)
    if not pattern:
        return
    if pattern.search(text):
        raise ValueError(f"{label} contains unexpected script content for {lang.upper()}")

def validate_transcript_chunk(chunk_paragraphs, translated_text):
    expected_speakers = []
    for paragraph in chunk_paragraphs:
        match = TRANSCRIPT_SPEAKER_RE.match(paragraph)
        if not match:
            raise ValueError(f"Transcript paragraph missing speaker tag: {paragraph[:80]}")
        expected_speakers.append(match.group(1))

    translated_paragraphs = transcript_paragraphs(translated_text)
    if len(translated_paragraphs) != len(chunk_paragraphs):
        raise ValueError(
            f"Translated paragraph count mismatch: expected {len(chunk_paragraphs)}, got {len(translated_paragraphs)}"
        )

    cleaned = []
    for idx, (expected_speaker, paragraph) in enumerate(zip(expected_speakers, translated_paragraphs), start=1):
        match = TRANSCRIPT_SPEAKER_RE.match(paragraph)
        if not match:
            raise ValueError(f"Translated paragraph {idx} missing speaker tag: {paragraph[:120]}")
        speaker, body = match.groups()
        body = collapse_ws(body)
        if speaker != expected_speaker:
            raise ValueError(
                f"Translated paragraph {idx} speaker mismatch: expected [{expected_speaker}], got [{speaker}]"
            )
        if not body:
            raise ValueError(f"Translated paragraph {idx} is empty")
        if TRANSCRIPT_LEAK_RE.search(body):
            raise ValueError(f"Translated paragraph {idx} contains prompt leakage: {body[:160]}")
        cleaned.append(f"[{speaker}]: {body}")
    return "\n\n".join(cleaned)

def translate_transcript_paragraph(paragraph, lang_name):
    match = TRANSCRIPT_SPEAKER_RE.match(paragraph)
    if not match:
        raise ValueError(f"Transcript paragraph missing speaker tag: {paragraph[:80]}")
    speaker, body = match.groups()
    body = body.strip()
    if body == "...":
        return f"[{speaker}]: ..."

    prompt = (
        f"Translate this single podcast transcript paragraph from English to {lang_name}.\n"
        "Return ONLY the translated spoken content with no speaker tag, no commentary, and no quotation marks.\n"
        "Keep product names unchanged: OpenClaw, Cursor, OpenSearch, KernelEvolve, Anthropic, Claude, Roblox, Salesforce, Adobe.\n\n"
        f"English paragraph:\n{body}"
    )

    for attempt in range(1, 4):
        translated = collapse_ws(gemini_call(prompt, max_tokens=1200))
        if not translated:
            continue
        if TRANSCRIPT_LEAK_RE.search(translated):
            log(f"      ⚠️  Paragraph fallback leaked prompt text (attempt {attempt}/3)", indent=3)
            continue
        if translated.startswith("[") and "]:" in translated:
            translated = translated.split("]:", 1)[1].strip()
        translated = translated.strip("\"' ")
        if translated:
            return f"[{speaker}]: {translated}"
    raise RuntimeError(f"Failed to translate transcript paragraph cleanly for {lang_name}")

def translate_transcript_chunk(chunk_paragraphs, lang_name):
    chunk_text = "\n\n".join(chunk_paragraphs)
    prompt = (
        f"Translate this podcast transcript chunk from English to {lang_name}.\n"
        "Rules:\n"
        "- Preserve the exact number of paragraphs and the exact paragraph order\n"
        "- Preserve the speaker tag at the start of every paragraph exactly as [NOVA]: or [ALLOY]:\n"
        "- Keep product names unchanged: OpenClaw, Cursor, OpenSearch, KernelEvolve, Anthropic, Claude, Roblox, Salesforce, Adobe\n"
        "- Translate all spoken content naturally for a conversational podcast\n"
        "- Output ONLY the translated transcript chunk and nothing else\n\n"
        "Transcript chunk:\n\n"
        f"{chunk_text}"
    )

    last_error = None
    for attempt in range(1, 3):
        raw = gemini_call(prompt, max_tokens=10000)
        try:
            return validate_transcript_chunk(chunk_paragraphs, raw)
        except Exception as exc:
            last_error = exc
            log(f"      ⚠️  Chunk validation failed (attempt {attempt}/2): {exc}", indent=3)

    log("      ↳ Falling back to paragraph-by-paragraph transcript translation", indent=3)
    translated = [translate_transcript_paragraph(paragraph, lang_name) for paragraph in chunk_paragraphs]
    return "\n\n".join(translated)

def translate_text_chunked(text, lang, chunk_type="transcript"):
    """Translate long text (transcript/show notes) in chunks via Minimax."""
    lang_name = LANG_NAMES[lang]

    if chunk_type == "transcript":
        system_note = (
            "Translate this podcast transcript from English to {lang_name}. Rules:\n"
            "- Keep [NOVA]: and [ALLOY]: speaker tags EXACTLY as written (do NOT translate them)\n"
            "- Keep product names unchanged: OpenClaw, Cursor, OpenSearch, KernelEvolve, etc.\n"
            "- Translate all other content naturally in conversational podcast style\n"
            "- Output ONLY the translated transcript, no commentary\n"
        ).format(lang_name=lang_name)
    else:  # show_notes
        system_note = (
            "Translate this podcast show notes document from English to {lang_name}. Rules:\n"
            "- Keep all URLs unchanged\n"
            "- Keep product names unchanged\n"
            "- Translate all other text naturally\n"
            "- Output ONLY the translated content, no commentary\n"
        ).format(lang_name=lang_name)

    # Split into chunks; Hindi needs smaller transcript batches to avoid count drift.
    paragraphs = transcript_paragraphs(text)
    chunk_size = 60
    if chunk_type == "transcript" and lang == "hi":
        chunk_size = 20
    chunks = [paragraphs[i:i+chunk_size] for i in range(0, len(paragraphs), chunk_size)]

    translated_chunks = []
    for i, chunk in enumerate(chunks):
        log(f"    Translating chunk {i+1}/{len(chunks)} ({len(chunk)} paragraphs)...", indent=2)
        if chunk_type == "transcript":
            result = translate_transcript_chunk(chunk, lang_name)
        else:
            chunk_text = "\n\n".join(chunk)
            prompt = f"{system_note}\n\nTranslate the following:\n\n{chunk_text}"
            result = gemini_call(prompt, max_tokens=10000)
        validate_language_scripts(result, lang, f"{chunk_type} chunk {i+1}/{len(chunks)}")
        translated_chunks.append(result)
        if i < len(chunks) - 1:
            time.sleep(1)  # polite pause between chunks

    return "\n\n".join(translated_chunks)

# ── Cover generation ──────────────────────────────────────────────────────────

def generate_en_cover(ep_num):
    """Generate EN cover art from show notes title — LLM picks cover lines."""
    ep_str = f"{ep_num:03d}"
    notes = (PODCAST_DIR / f"show_notes_episode_{ep_str}.md").read_text()
    title_m = re.search(r"^## Episode Title\s*\n\*\*(.+?)\*\*", notes, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else f"Episode {ep_num}"
    tag_m = re.search(r"^## Tagline\s*\n(.+?)(?=\n\n|\n##)", notes, re.MULTILINE | re.DOTALL)
    tagline = (tag_m.group(1).strip() if tag_m else "").split(".")[0][:60]

    # Extract cover lines from title structure: split on commas and "and"
    # e.g. "Claw Tax, Courtrooms, and the New AI Stack" → ["CLAW TAX", "COURTROOMS", "THE NEW AI STACK"]
    def extract_cover_lines(t):
        # Strip episode number prefix if present (e.g. "Episode 29: ...")
        t = re.sub(r'^Episode\s+\d+:\s*', '', t, flags=re.IGNORECASE)
        # Split on ", and ", ", ", " and "
        parts = re.split(r',\s*(?:and\s+)?|\s+and\s+', t)
        # Clean filler words from each part, uppercase
        cleaned = []
        for p in parts:
            p = p.strip().upper()
            # Drop short filler-only parts
            if p and p not in ("THE", "A", "AN", "AND", "OR", "BUT", "IN", "OF"):
                cleaned.append(p)
        return cleaned

    concepts = extract_cover_lines(title)
    if len(concepts) >= 2:
        line1 = concepts[0]
        line2 = concepts[1]
    elif len(concepts) == 1:
        words = concepts[0].split()
        mid = max(1, len(words) // 2)
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
    else:
        words = title.upper().split()
        mid = max(1, len(words) // 2)
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])

    meta = {"cover_line1": line1, "cover_line2": line2, "cover_tagline": tagline}

    out_path = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    return generate_translated_cover(ep_num, "de", meta, out_path=out_path)


def generate_translated_cover(ep_num, lang, meta, out_path=None):
    """Render a cover image for the episode. Pass out_path to override default filename."""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    import random

    W, H = 1400, 1400
    if out_path is None:
        out_path = PODCAST_DIR / "images" / f"episode_{ep_num:03d}_cover_{lang}.png"

    # Read EN cover script to extract visual parameters (colors etc.)
    # We rebuild the design from scratch matching EP's style
    # Fall back to a generic dark+strata design if the cover script can't be parsed
    cover_script = SCRIPTS_DIR / f"generate_episode_{ep_num:03d}_cover.py"
    cover_src = cover_script.read_text() if cover_script.exists() else ""

    # Extract color palette from source or use defaults
    def extract_color(name, default):
        m = re.search(rf'{name}\s*=\s*\((\d+),\s*(\d+),\s*(\d+)\)', cover_src)
        return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else default

    BLACK        = extract_color("BLACK",        (2, 4, 10))
    AMBER        = extract_color("AMBER",        (215, 145, 25))
    AMBER_BRIGHT = extract_color("AMBER_BRIGHT", (248, 180, 55))
    TEAL        = extract_color("TEAL",         (20, 180, 160))
    BLUE        = extract_color("BLUE",         (40, 110, 220))
    STEEL_LIGHT = extract_color("STEEL_LIGHT",  (48, 68, 105))
    DIM_WHITE   = extract_color("DIM_WHITE",    (140, 165, 200))
    WHITE       = extract_color("WHITE",        (242, 248, 255))

    img = Image.new("RGBA", (W, H), BLACK + (255,))
    d = ImageDraw.Draw(img)

    # Background gradient — saturated enough to read on screen, hue cycles per episode
    _bg_palettes = [
        ((20, 45, 110), (2, 3, 8)),    # 0: steel blue
        ((24, 10,  4),  (8, 3, 1)),    # 1: dark rust  ← EP029 approved look
        ((4,  45, 45),  (2, 8, 8)),    # 2: deep teal
        ((30, 8,  55),  (6, 2, 12)),   # 3: dark purple
        ((6,  40, 12),  (2, 8, 4)),    # 4: deep green
        ((45, 20,  4),  (10, 6, 2)),   # 5: ember orange
        ((8,  12, 70),  (2, 3, 14)),   # 6: deep indigo
        ((28, 28,  6),  (8, 8, 2)),    # 7: dark gold
    ]
    _top, _bot = _bg_palettes[ep_num % len(_bg_palettes)]
    for y in range(H):
        t = y / (H - 1)
        r = int(_top[0] * (1 - t) + _bot[0] * t)
        g = int(_top[1] * (1 - t) + _bot[1] * t)
        b = int(_top[2] * (1 - t) + _bot[2] * t)
        d.line([(0, y), (W, y)], fill=(r, g, b, 255))

    def blur_overlay(draw_fn, blur=18):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        draw_fn(ld)
        return layer.filter(ImageFilter.GaussianBlur(blur))

    # Per-episode bespoke middle art — try episode_art/episode_NNN_art.py first
    _art_mod = None
    _art_path = SCRIPTS_DIR / "episode_art" / f"episode_{ep_num:03d}_art.py"
    if _art_path.exists():
        import importlib.util as _ilu
        _spec = _ilu.spec_from_file_location(f"episode_{ep_num:03d}_art", _art_path)
        _art_mod = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_art_mod)

    if _art_mod is not None:
        img = _art_mod.draw_art(img, W, H)
        d = ImageDraw.Draw(img)
    else:
        # Fallback: strata geological cross-section
        random.seed(ep_num)
        strata = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strata)
        strata_defs = [
            (120, 3, TEAL, 45), (185, 2, STEEL_LIGHT, 35), (240, 4, BLUE, 40),
            (310, 2, STEEL_LIGHT, 30), (370, 3, AMBER, 35), (420, 2, TEAL, 30),
            (480, 5, BLUE, 45), (530, 2, STEEL_LIGHT, 25), (590, 3, AMBER, 40),
            (640, 2, TEAL, 30), (700, 4, BLUE, 35), (760, 2, AMBER, 30),
            (820, 3, TEAL, 35), (870, 2, STEEL_LIGHT, 25),
        ]
        for y_center, thickness, color, alpha in strata_defs:
            pts = []
            for x in range(0, W + 20, 20):
                wave = math.sin(x * 0.008 + y_center * 0.01) * 8
                wave += math.sin(x * 0.003 - y_center * 0.02) * 12
                pts.append((x, y_center + wave))
            for i in range(len(pts) - 1):
                sd.line([pts[i], pts[i+1]], fill=color + (alpha,), width=thickness)
        img = Image.alpha_composite(img, strata.filter(ImageFilter.GaussianBlur(12)))
        img = Image.alpha_composite(img, strata.filter(ImageFilter.GaussianBlur(0.8)))

        markers = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        mkd = ImageDraw.Draw(markers)
        for y in range(80, 900, 60):
            tick_len = 25 if y % 180 == 0 else 12
            mkd.line([(40, y), (40+tick_len, y)], fill=STEEL_LIGHT+(50,), width=1)
            mkd.line([(W-40, y), (W-40-tick_len, y)], fill=STEEL_LIGHT+(50,), width=1)
        mkd.line([(40, 80), (40, 880)], fill=STEEL_LIGHT+(35,), width=1)
        mkd.line([(W-40, 80), (W-40, 880)], fill=STEEL_LIGHT+(35,), width=1)
        img = Image.alpha_composite(img, markers)

        for center, color in [((700, 400), BLUE), ((700, 600), AMBER), ((700, 300), TEAL)]:
            g = blur_overlay(
                lambda ld, c=center, col=color: ld.ellipse(
                    [(c[0]-500, c[1]-200), (c[0]+500, c[1]+200)], fill=col+(7,)), blur=110)
            img = Image.alpha_composite(img, g)

        d = ImageDraw.Draw(img)

    # Fonts
    font_path_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    font_path_reg  = "/System/Library/Fonts/Supplemental/Arial.ttf"
    hi_font_paths  = [
        "/System/Library/Fonts/Supplemental/ITFDevanagari.ttc",
        "/System/Library/Fonts/DevanagariMT.ttc",
        "/System/Library/Fonts/Supplemental/DevanagariMT.ttc",
    ]

    is_hindi = (lang == "hi")
    title_font_path = font_path_bold
    if is_hindi:
        for p in hi_font_paths:
            if Path(p).exists():
                title_font_path = p
                break

    try:
        font_show  = ImageFont.truetype(font_path_bold, 46)
        font_ep    = ImageFont.truetype(font_path_bold, 68)
        base_title_size = 100 if is_hindi else 118
        font_title = ImageFont.truetype(title_font_path, base_title_size)
        font_sub   = ImageFont.truetype(font_path_reg, 28 if is_hindi else 30)
    except Exception:
        font_show = font_ep = font_title = font_sub = ImageFont.load_default()
        base_title_size = 118

    md = ImageDraw.Draw(img)

    SHOW_TEXT = "OPENCLAW DAILY"
    EP_TEXT   = f"EP{ep_num:03d}"
    line1     = meta.get("cover_line1", "").upper()
    line2     = meta.get("cover_line2", "").upper()
    tagline   = meta.get("cover_tagline", "")

    def fit_font(text_value, start_size, min_size=56, max_width=W-110):
        if not text_value:
            return font_title
        if not hasattr(ImageFont, "truetype"):
            return font_title
        size = start_size
        while size >= min_size:
            candidate = ImageFont.truetype(title_font_path, size)
            if md.textlength(text_value, font=candidate) <= max_width:
                return candidate
            size -= 4
        return ImageFont.truetype(title_font_path, min_size)

    font_title_l1 = fit_font(line1, base_title_size)
    font_title_l2 = fit_font(line2, base_title_size)

    # "OPENCLAW DAILY" top
    sw = md.textlength(SHOW_TEXT, font=font_show)
    md.text(((W-sw)/2, 55), SHOW_TEXT, font=font_show, fill=(185, 205, 230, 210))

    # "EP025" amber glow
    ew = md.textlength(EP_TEXT, font=font_ep)
    for blur_amt, alpha in ((18, 95), (34, 45)):
        eg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        egd = ImageDraw.Draw(eg)
        egd.text(((W-ew)/2, 112), EP_TEXT, font=font_ep, fill=AMBER+(alpha,))
        eg = eg.filter(ImageFilter.GaussianBlur(blur_amt))
        img = Image.alpha_composite(img, eg)
    md = ImageDraw.Draw(img)
    md.text(((W-ew)/2, 112), EP_TEXT, font=font_ep, fill=AMBER_BRIGHT+(255,))

    # Dark title plate
    plate = blur_overlay(
        lambda ld: ld.polygon([(0, 940), (W, 940), (W, H), (0, H)], fill=(0, 0, 0, 200)),
        blur=28)
    img = Image.alpha_composite(img, plate)
    md = ImageDraw.Draw(img)

    # Line 1 — white with teal glow
    l1w = md.textlength(line1, font=font_title_l1)
    md.text(((W-l1w)/2+3, 988), line1, font=font_title_l1, fill=(0, 0, 0, 160))
    tg1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tg1).text(((W-l1w)/2, 985), line1, font=font_title_l1, fill=TEAL+(50,))
    img = Image.alpha_composite(img, tg1.filter(ImageFilter.GaussianBlur(14)))
    md = ImageDraw.Draw(img)
    md.text(((W-l1w)/2, 985), line1, font=font_title_l1, fill=WHITE+(255,))

    # Line 2 — amber glow
    l2w = md.textlength(line2, font=font_title_l2)
    md.text(((W-l2w)/2+4, 1118), line2, font=font_title_l2, fill=(0, 0, 0, 170))
    tg2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tg2).text(((W-l2w)/2, 1115), line2, font=font_title_l2, fill=AMBER+(80,))
    img = Image.alpha_composite(img, tg2.filter(ImageFilter.GaussianBlur(16)))
    md = ImageDraw.Draw(img)
    md.text(((W-l2w)/2, 1115), line2, font=font_title_l2, fill=AMBER_BRIGHT+(255,))

    # Tagline
    tw = md.textlength(tagline, font=font_sub)
    if tw > W - 80:  # wrap if too long
        # Simple truncate with ellipsis
        while md.textlength(tagline + "...", font=font_sub) > W - 80 and tagline:
            tagline = tagline[:-1]
        tagline += "..."
        tw = md.textlength(tagline, font=font_sub)
    md.text(((W-tw)/2, 1305), tagline, font=font_sub, fill=AMBER_BRIGHT+(120,))

    # Vignette
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).rectangle((50, 25, W-50, H-25), fill=205)
    inv = Image.eval(vig, lambda p: 255-p)
    black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    black.putalpha(inv.filter(ImageFilter.GaussianBlur(90)))
    img = Image.alpha_composite(img, black)

    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=145, threshold=2))
    img.convert("RGB").save(str(out_path), "PNG")
    return out_path

def get_en_release_metadata(ep_num, state):
    ep_str = f"{ep_num:03d}"
    notes = (PODCAST_DIR / f"show_notes_episode_{ep_str}.md").read_text()
    en_episode_title = extract_episode_title(notes, ep_num)
    en_title = f"Episode {ep_num}: {en_episode_title}"
    en_desc = extract_feed_description(notes) or en_episode_title
    duration = state.get("audio_duration", "33:00")
    en_size = state.get("audio_size")
    if not en_size:
        raise RuntimeError("Missing audio_size in pipeline state; refusing to emit a placeholder enclosure length")
    return {
        "episode_title": en_episode_title,
        "title": en_title,
        "description": en_desc,
        "duration": duration,
        "size": en_size,
    }

def translated_release_tag(ep_num):
    return f"ep{ep_num:03d}"

def translated_release_repo(lang):
    return media_releases.LANG_REPOS[lang]

def translated_release_audio_name(ep_num):
    return f"episode_{ep_num:03d}.mp3"

def translated_release_cover_name(ep_num):
    return f"episode_{ep_num:03d}_cover.png"

def translated_audio_release_direct_url(ep_num, lang):
    return media_releases.release_asset_url(
        translated_release_repo(lang),
        translated_release_tag(ep_num),
        translated_release_audio_name(ep_num),
    )

def translated_audio_direct_url(ep_num, lang):
    return media_releases.translated_audio_proxy_direct_url(lang, ep_num)

def translated_audio_guid_url(ep_num, lang):
    return translated_audio_release_direct_url(ep_num, lang)

def translated_audio_url(ep_num, lang):
    return media_releases.op3_wrap(translated_audio_direct_url(ep_num, lang))

def translated_cover_url(ep_num, lang):
    return media_releases.release_asset_url(
        translated_release_repo(lang),
        translated_release_tag(ep_num),
        translated_release_cover_name(ep_num),
    )

def upload_translated_release_assets(ep_num, lang):
    ep_str = f"{ep_num:03d}"
    audio_path = PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"
    cover_path = PODCAST_DIR / "images" / f"episode_{ep_str}_cover_{lang}.png"
    if not audio_path.exists():
        raise FileNotFoundError(f"Missing translated audio for {lang.upper()}: {audio_path}")
    if not cover_path.exists():
        raise FileNotFoundError(f"Missing translated cover for {lang.upper()}: {cover_path}")

    repo = translated_release_repo(lang)
    media_releases.ensure_repo_initialized(repo)
    media_releases.ensure_release_with_assets(
        repo,
        translated_release_tag(ep_num),
        f"EP{ep_str}",
        {
            translated_release_audio_name(ep_num): audio_path,
            translated_release_cover_name(ep_num): cover_path,
        },
    )

def deploy_website(ep_num, message, extra_paths):
    log("  Building website...")

    pushed = git_commit_if_needed(
        WEBSITE_DIR,
        message,
        extra_paths=extra_paths,
    )
    if pushed:
        log("  ✅ Website pushed")
    else:
        git_commit_if_needed(
            WEBSITE_DIR,
            f"EP{ep_num}: trigger website deploy",
            allow_empty=True,
        )
        log("  ✅ Website deploy triggered (empty commit)")

# ── Phase implementations ─────────────────────────────────────────────────────

def phase_setup(ep_num, state):
    log("[ SETUP ] Checking prerequisites...")
    ep_str = f"{ep_num:03d}"

    # Check EN audio — accept canonical name or legacy _en / _approved_en suffixes
    en_audio_dst = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    audio_candidates = [
        en_audio_dst,
        PODCAST_DIR / "audio" / f"episode_{ep_str}_en.mp3",
        PODCAST_DIR / "audio" / f"episode_{ep_str}_approved_en.mp3",
    ]
    en_audio_src = next((p for p in audio_candidates if p.exists()), None)
    if not en_audio_src:
        raise FileNotFoundError(
            f"Missing EN audio — tried: {', '.join(p.name for p in audio_candidates)}"
        )
    if en_audio_src != en_audio_dst:
        shutil.copy2(str(en_audio_src), str(en_audio_dst))
        log(f"  ✅ Canonicalized: {en_audio_src.name} → episode_{ep_str}.mp3")
    else:
        log(f"  ✅ Canonical audio: episode_{ep_str}.mp3")

    # Check EN cover — generate if missing
    en_cover = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    if not en_cover.exists():
        log(f"  ℹ️  EN cover missing — generating from show notes...")
        generate_en_cover(ep_num)
        log(f"  ✅ EN cover generated")
    else:
        log(f"  ✅ EN cover exists")

    # Check show notes
    show_notes = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    if not show_notes.exists():
        raise FileNotFoundError(f"Missing show notes: {show_notes}")
    log(f"  ✅ Show notes exist")

    # Check transcript nova file
    transcript = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript_nova.md"
    if not transcript.exists():
        raise FileNotFoundError(f"Missing transcript: {transcript}")
    log(f"  ✅ Transcript exists ({transcript.stat().st_size // 1024}KB)")

    # Store audio info
    duration_str = ffprobe_duration_str(en_audio_dst)
    file_size = en_audio_dst.stat().st_size
    state["audio_duration"] = duration_str
    state["audio_size"] = file_size
    log(f"  ✅ Audio: {duration_str}, {file_size // 1024 // 1024}MB")

    return state

def phase_translate(ep_num, state):
    log("[ TRANSLATE ] Generating translations via Minimax M2.7...")
    ep_str = f"{ep_num:03d}"
    transcript_path = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript_nova.md"
    show_notes_path = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    transcript_text = transcript_path.read_text()
    show_notes_text = show_notes_path.read_text()

    # Extract show notes block (content inside ```md ... ```)
    block_m = re.search(r"```md\s*\n(.*?)```", show_notes_text, re.DOTALL)
    show_notes_block = block_m.group(1).strip() if block_m else show_notes_text

    translations = state.get("translations", {})

    for lang in LANGS:
        lang_dir = PODCAST_DIR / "translations" / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        transcript_out = lang_dir / f"episode_{ep_str}_{lang}.md"
        notes_out = lang_dir / f"show_notes_episode_{ep_str}_{lang}.md"
        lang_state = translations.setdefault(lang, {})

        if lang_state.get("done"):
            log(f"  ⏭  {lang.upper()} already translated, skipping")
            continue

        if transcript_out.exists() and notes_out.exists():
            log(f"  ⏭  {lang.upper()} translated files already exist, reusing", indent=1)
            if not lang_state.get("meta"):
                log(f"     Metadata...", indent=1)
                lang_state["meta"] = translate_metadata(ep_num, lang)
                log(f"     Title: {lang_state['meta'].get('title', '?')}", indent=1)
            lang_state["done"] = True
            state["translations"] = translations
            save_state(ep_num, state)
            continue

        log(f"  → {lang.upper()} ({LANG_NAMES[lang]})...")

        # 1. Metadata
        log(f"     Metadata...", indent=1)
        meta = translate_metadata(ep_num, lang)
        lang_state["meta"] = meta
        log(f"     Title: {meta.get('title', '?')}", indent=1)

        # 2. Transcript
        log(f"     Transcript...", indent=1)
        translated_transcript = translate_text_chunked(transcript_text, lang, "transcript")
        transcript_out.write_text(translated_transcript)
        log(f"     ✅ Saved: {transcript_out.name}", indent=1)

        # 3. Show notes
        log(f"     Show notes...", indent=1)
        translated_notes = translate_text_chunked(show_notes_block, lang, "show_notes")
        notes_out.write_text(translated_notes)
        log(f"     ✅ Saved: {notes_out.name}", indent=1)

        lang_state["done"] = True
        state["translations"] = translations
        save_state(ep_num, state)

    return state

def phase_tts(ep_num, state):
    log("[ TTS ] Generating translated audio via edge-tts...")
    ep_str = f"{ep_num:03d}"

    sys.path.insert(0, str(SCRIPTS_DIR.parent))  # add podcast root
    import generate_audio as ga

    LANG_VOICES = {
        "es": {"NOVA": "es-ES-ElviraNeural",    "ALLOY": "es-ES-AlvaroNeural"},
        "de": {"NOVA": "de-DE-KatjaNeural",     "ALLOY": "de-DE-ConradNeural"},
        "pt": {"NOVA": "pt-BR-FranciscaNeural", "ALLOY": "pt-BR-AntonioNeural"},
        "hi": {"NOVA": "hi-IN-SwaraNeural",     "ALLOY": "hi-IN-MadhurNeural"},
    }

    for lang in LANGS:
        out_path = PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"
        if out_path.exists():
            log(f"  ⏭  {lang.upper()} audio exists ({out_path.stat().st_size // 1024 // 1024}MB), skipping")
            continue

        script_path = PODCAST_DIR / "translations" / lang / f"episode_{ep_str}_{lang}.md"
        if not script_path.exists():
            raise FileNotFoundError(f"Missing translated script for {lang}: {script_path}")

        log(f"  → {lang.upper()} ({LANG_NAMES[lang]})...")
        ga.VOICES = LANG_VOICES[lang]
        ga.AUDIO_DIR = PODCAST_DIR / "audio"
        asyncio.run(ga.generate_podcast_audio(str(script_path), f"episode_{ep_str}_{lang}"))
        log(f"  ✅ {out_path.name} ({out_path.stat().st_size // 1024 // 1024}MB)")

    return state

def phase_covers(ep_num, state):
    log("[ COVERS ] Generating translated cover art...")
    ep_str = f"{ep_num:03d}"
    translations = state.get("translations", {})
    en_notes = (PODCAST_DIR / f"show_notes_episode_{ep_str}.md").read_text()
    en_episode_title = extract_episode_title(en_notes, ep_num)
    en_tagline = extract_tagline(en_notes) or extract_feed_description(en_notes)

    # Auto-generate bespoke middle art module if not already present
    art_mod_path = SCRIPTS_DIR / "episode_art" / f"episode_{ep_str}_art.py"
    if not art_mod_path.exists():
        log(f"  → No art module for EP{ep_str} — generating via Claude CLI...")
        gen_script = SCRIPTS_DIR / "generate_episode_art.py"
        result = subprocess.run(
            ["python3", str(gen_script), str(ep_num)],
            capture_output=False,
            text=True,
        )
        if art_mod_path.exists():
            log(f"  ✅ Art module generated: {art_mod_path.name}")
        else:
            log(f"  ⚠️  Art generation failed (exit {result.returncode}) — covers will use strata fallback")
    else:
        log(f"  ✅ Art module exists: {art_mod_path.name}")

    # Also copy EN cover to CDN
    en_cover_src = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    en_cover_cdn = CDN_DIR / f"episode_{ep_str}_cover.png"
    if not en_cover_cdn.exists():
        shutil.copy2(str(en_cover_src), str(en_cover_cdn))
        log(f"  ✅ EN cover → CDN")

    # Copy EN cover to website
    WEBSITE_PODCAST_IMG.mkdir(parents=True, exist_ok=True)
    en_cover_web = WEBSITE_PODCAST_IMG / f"episode_{ep_str}_cover.png"
    if not en_cover_web.exists():
        shutil.copy2(str(en_cover_src), str(en_cover_web))
        log(f"  ✅ EN cover → website")

    for lang in LANGS:
        out_path = PODCAST_DIR / "images" / f"episode_{ep_str}_cover_{lang}.png"
        if out_path.exists():
            log(f"  ⏭  {lang.upper()} cover exists, skipping")
        else:
            meta = translations.get(lang, {}).get("meta", {})
            if not meta:
                log(f"  ℹ️  No cached metadata for {lang} — fetching via Minimax...", indent=1)
                meta = translate_metadata(ep_num, lang)
            meta = normalize_translated_metadata(
                meta,
                ep_num,
                TITLE_PREFIXES[lang],
                en_episode_title,
                en_tagline,
            )
            translations.setdefault(lang, {})["meta"] = meta
            state["translations"] = translations
            log(f"  → Generating {lang.upper()} cover...")
            generate_translated_cover(ep_num, lang, meta)
            log(f"  ✅ {out_path.name}")

        # Copy to website
        web_cover = WEBSITE_PODCAST_IMG / f"episode_{ep_str}_cover_{lang}.png"
        if not web_cover.exists():
            shutil.copy2(str(out_path), str(web_cover))
            log(f"     → {web_cover.name} copied to website")

    return state

def phase_feeds(ep_num, state, pub_date):
    log("[ FEEDS ] Adding feed entries...")
    state = phase_en_feed(ep_num, state, pub_date)
    state = phase_translated_feeds(ep_num, state, pub_date)
    return state

def phase_en_feed(ep_num, state, pub_date):
    log("[ FEEDS / EN ] Adding EN feed entry...")
    ep_str = f"{ep_num:03d}"
    meta = get_en_release_metadata(ep_num, state)
    add_feed_script = str(SCRIPTS_DIR / "add_feed_entry.py")
    review_audio = CDN_DIR / "audio" / f"episode_{ep_str}.mp3"
    review_cover = CDN_DIR / f"episode_{ep_str}_cover.png"
    if not review_audio.exists() or not review_cover.exists():
        raise FileNotFoundError(
            "Missing pre-approval CDN review assets. "
            f"Expected {review_audio.name} and {review_cover.name} from build_episode.py"
        )

    # EN feed
    en_audio_url = f"{CDN_BASE}/audio/episode_{ep_str}.mp3"
    en_cover_url = f"{CDN_BASE}/episode_{ep_str}_cover.png"
    en_link = f"https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"

    en_feed = PODCAST_DIR / "feed.xml"
    # Check if already in feed
    if f"<itunes:episode>{ep_num}</itunes:episode>" not in en_feed.read_text():
        log(f"  → Adding EN feed entry...")
        run([
            sys.executable, add_feed_script,
            str(en_feed),
            "--episode", str(ep_num),
            "--title", meta["title"],
            "--description", meta["description"],
            "--pub-date", pub_date,
            "--audio-url", en_audio_url,
            "--cover-url", en_cover_url,
            "--duration", meta["duration"],
            "--link", en_link,
            "--length", str(meta["size"]),
        ])
        log(f"  ✅ EN feed updated")
    else:
        log(f"  ⏭  EN feed already has EP{ep_num}")

    return state

def phase_translated_feeds(ep_num, state, pub_date):
    log("[ FEEDS / TRANSLATED ] Adding translated feed entries...")
    ep_str = f"{ep_num:03d}"
    translations = state.get("translations", {})
    en_meta = get_en_release_metadata(ep_num, state)
    add_feed_script = str(SCRIPTS_DIR / "add_feed_entry.py")

    # Translated feeds
    for lang in LANGS:
        feed_path = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
        feed_text = feed_path.read_text()
        prefix = TITLE_PREFIXES[lang]

        if f"<itunes:episode>{ep_num}</itunes:episode>" in feed_text:
            log(f"  ⏭  {lang.upper()} feed already has EP{ep_num}")
            continue

        lang_audio = PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"
        if not lang_audio.exists():
            raise FileNotFoundError(
                f"Refusing to insert {lang.upper()} feed entry before translated audio exists: {lang_audio.name}"
            )

        meta = translations.get(lang, {}).get("meta", {})
        if not meta:
            log(f"  ℹ️  No cached metadata for {lang.upper()} — fetching...", indent=1)
            meta = translate_metadata(ep_num, lang)
            translations.setdefault(lang, {})["meta"] = meta
            state["translations"] = translations
        lang_title = meta.get("title", f"{prefix} {ep_num}: {en_meta['episode_title']}")
        lang_desc_base = meta.get("description", en_meta["description"])
        lang_link = LANG_LINKS[lang].format(ep=ep_num)

        lang_audio_url = translated_audio_direct_url(ep_num, lang)
        lang_cover_url = translated_cover_url(ep_num, lang)

        lang_size = lang_audio.stat().st_size

        # For translated feed, duration comes from translated audio
        lang_duration = en_meta["duration"]
        try:
            lang_duration = ffprobe_duration_str(lang_audio)
        except Exception:
            pass

        log(f"  → Adding {lang.upper()} feed entry...")
        run([
            sys.executable, add_feed_script,
            str(feed_path),
            "--episode", str(ep_num),
            "--title", lang_title,
            "--description", lang_desc_base,
            "--pub-date", pub_date,
            "--audio-url", lang_audio_url,
            "--guid", translated_audio_guid_url(ep_num, lang),
            "--cover-url", lang_cover_url,
            "--duration", lang_duration,
            "--link", lang_link,
            "--length", str(lang_size),
        ])
        log(f"  ✅ {lang.upper()} feed updated: {lang_title}")

    return state

def phase_qc(ep_num, state):
    log("[ QC ] Running translation quality check...")
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "check_episode_translations.py"), str(ep_num)],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("QC check failed — fix issues before continuing")
    return state

def phase_youtube(ep_num, state):
    log("[ YOUTUBE ] Uploading all 5 channels...")
    venv_python = PODCAST_DIR / ".venv_shorts/bin/python3"
    youtube_python = str(venv_python) if venv_python.exists() else sys.executable
    result = subprocess.run(
        [youtube_python, str(SCRIPTS_DIR / "youtube_scheduled_upload.py"), str(ep_num)],
        cwd=str(PODCAST_DIR)
    )
    if result.returncode != 0:
        raise RuntimeError("YouTube upload failed")
    return state

def phase_en_video(ep_num, state):
    log("[ EN VIDEO ] Starting EN FLUX/video lane...")
    build_script = SCRIPTS_DIR / "build_youtube_episode_videos.py"
    if not build_script.exists():
        log("  ℹ️  build_youtube_episode_videos.py not found — skipping EN video lane")
        return state
    result = subprocess.run(
        [sys.executable, str(build_script), str(ep_num), "--lang", "en"],
        cwd=str(PODCAST_DIR),
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        raise RuntimeError(
            "EN video lane failed\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return state

def phase_cdn(ep_num, state):
    log("[ CDN ] Syncing translated media release assets...")
    return phase_translated_cdn(ep_num, state)

def phase_translated_cdn(ep_num, state):
    log("[ CDN / TRANSLATED ] Uploading translated audio + covers to media release repos...")
    for lang in LANGS:
        upload_translated_release_assets(ep_num, lang)
        log(f"  ✅ {lang.upper()} media release updated")

    return state

def phase_publish(ep_num, state):
    log("[ PUBLISH ] Pushing podcast repo + website...")
    state = phase_publish_en(ep_num, state)
    state = phase_publish_translations(ep_num, state)
    return state

def push_podcast_stage(ep_num, stage, commit_message):
    existing = [f for f in stage if (PODCAST_DIR / f).exists()]
    git_add_paths(PODCAST_DIR, existing)
    result = run(["git", "diff", "--cached", "--quiet"], cwd=str(PODCAST_DIR), check=False)
    if result.returncode != 0:
        env = {**os.environ, "FEED_APPROVED": "1"}
        run(["git", "commit", "-m", commit_message], cwd=str(PODCAST_DIR), env=env)
        run(["git", "push"], cwd=str(PODCAST_DIR))
        log(f"  ✅ Podcast repo pushed")
    else:
        log(f"  ℹ️  Podcast repo already up to date")

def phase_publish_en(ep_num, state):
    log("[ PUBLISH / EN ] Pushing EN podcast + website...")
    ep_str = f"{ep_num:03d}"
    ensure_website_cover(ep_num)

    stage = [
        f"feed.xml",
        f"images/episode_{ep_str}_cover.png",
        f"show_notes_episode_{ep_str}.md",
        f"episodes/episode_{ep_str}_transcript.md",
    ]
    push_podcast_stage(ep_num, stage, f"EP{ep_num}: publish EN episode_{ep_str}")
    deploy_website(
        ep_num,
        f"EP{ep_num}: EN cover art + website update",
        [f"frontend/public/images/podcast/episode_{ep_str}_cover.png"],
    )

    return state

def phase_publish_translations(ep_num, state):
    log("[ PUBLISH / TRANSLATED ] Pushing translated podcast + website...")
    ep_str = f"{ep_num:03d}"
    stage = [
        f"translations/feed_de.xml",
        f"translations/feed_es.xml",
        f"translations/feed_hi.xml",
        f"translations/feed_pt.xml",
    ]
    for lang in LANGS:
        ensure_website_cover(ep_num, lang)
        stage += [
            f"images/episode_{ep_str}_cover_{lang}.png",
            f"translations/{lang}/episode_{ep_str}_{lang}.md",
            f"translations/{lang}/show_notes_episode_{ep_str}_{lang}.md",
        ]
    push_podcast_stage(ep_num, stage, f"EP{ep_num}: publish translated episode_{ep_str}")
    deploy_website(
        ep_num,
        f"EP{ep_num}: translated cover art + website update",
        [f"frontend/public/images/podcast/episode_{ep_str}_cover_{lang}.png" for lang in LANGS],
    )

    return state

def phase_discord(ep_num, state):
    import urllib.request, urllib.error

    DISCORD_TOKEN = load_env_key("DISCORD_BOT_TOKEN")
    GUILD_ID = "1475905694145318944"
    DAILY_CHANNEL_ID = "1485445727772475533"
    ep_str = f"{ep_num:03d}"
    ep_channel_name = f"openclaw-ep{ep_str}"

    def discord_request(method, path, body=None):
        url = f"https://discord.com/api/v10{path}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bot {DISCORD_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
        })
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body_text = e.read().decode()
            raise RuntimeError(f"Discord {method} {path} → {e.code}: {body_text}")

    log(f"[ DISCORD ] Posting release to #openclaw-daily and cleaning up #{ep_channel_name}...")

    # Read show notes for the release announcement
    show_notes_path = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    if show_notes_path.exists():
        show_notes = show_notes_path.read_text()
        # Extract just title + tagline + story titles for the announcement (keep it concise)
        lines = show_notes.splitlines()
        title_line = next((l for l in lines if l.startswith("# EP")), f"# EP{ep_str}")
        tagline_line = next((l for l in lines if l.startswith("**OpenClaw Daily**")), "")
        announcement = f"🎙️ **EP{ep_str} is live!**\n\n{title_line}\n{tagline_line}\n\nhttps://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"
    else:
        announcement = f"🎙️ **EP{ep_str} is live!**\nhttps://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"

    # Post to #openclaw-daily
    discord_request("POST", f"/channels/{DAILY_CHANNEL_ID}/messages", {"content": announcement})
    log(f"  ✅ Posted to #openclaw-daily")

    # Find and delete the per-episode channel
    channels = discord_request("GET", f"/guilds/{GUILD_ID}/channels")
    ep_channel = next((c for c in channels if c.get("name") == ep_channel_name), None)
    if ep_channel:
        discord_request("DELETE", f"/channels/{ep_channel['id']}")
        log(f"  ✅ Deleted #{ep_channel_name}")
    else:
        log(f"  ℹ️  #{ep_channel_name} not found (already deleted or never created)")

    return state

# ── State management ──────────────────────────────────────────────────────────

def load_state(ep_num):
    state_file = SCRIPTS_DIR / f"release_ep{ep_num:03d}_state.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {"completed_phases": [], "translations": {}}

def save_state(ep_num, state):
    state_file = SCRIPTS_DIR / f"release_ep{ep_num:03d}_state.json"
    state_file.write_text(json.dumps(state, indent=2))

# ── Main ──────────────────────────────────────────────────────────────────────

PHASE_FNS = {
    "setup": phase_setup,
    "en-feed": phase_en_feed,
    "en-publish": phase_publish_en,
    "en-video": phase_en_video,
    "translate": phase_translate,
    "tts": phase_tts,
    "covers": phase_covers,
    "translated-cdn": phase_translated_cdn,
    "translated-feeds": phase_translated_feeds,
    "qc": phase_qc,
    "publish-translations": phase_publish_translations,
    "youtube": phase_youtube,
    "discord": phase_discord,
    # Backward-compatible wrappers
    "feeds": phase_feeds,
    "cdn": phase_cdn,
    "publish": phase_publish,
}

PUB_DATE_PHASES = {"feeds", "en-feed", "translated-feeds"}

def resolve_only_phase(name):
    raw = (name or "").strip().lower()
    if raw in LEGACY_ONLY_PHASES:
        return raw
    return normalize_phase_name(raw)

def resolve_from_phase(name):
    phase = normalize_phase_name(name)
    if phase not in FULL_RELEASE_ORDER:
        raise ValueError(
            f"Unknown phase '{name}'. Valid phases: {', '.join(CLI_PHASE_CHOICES)}"
        )
    return phase

def run_named_phase(phase, ep_num, state, pub_date):
    fn = PHASE_FNS.get(phase)
    if fn is None:
        raise ValueError(
            f"Unknown phase '{phase}'. Valid phases: {', '.join(CLI_PHASE_CHOICES)}"
        )
    if phase in PUB_DATE_PHASES:
        return fn(ep_num, state, pub_date)
    return fn(ep_num, state)

def main():
    parser = argparse.ArgumentParser(description="OpenClaw episode release pipeline")
    parser.add_argument("episode", type=int, help="Episode number (e.g. 25)")
    parser.add_argument("--from-phase", help=f"Start from phase: {', '.join(CLI_PHASE_CHOICES)}")
    parser.add_argument("--only-phase", help="Run only this phase")
    _today = datetime.now(timezone.utc).strftime("%a, %d %b %Y 18:00:00 +0000")
    parser.add_argument("--pub-date",
                        default=_today,
                        help="RSS pubDate string (default: today at 18:00 UTC)")
    parser.add_argument("--reset", action="store_true", help="Clear saved state and restart")
    args = parser.parse_args()

    ep_num = args.episode
    state = load_state(ep_num)

    if args.reset:
        state = {"completed_phases": [], "translations": {}}
        save_state(ep_num, state)
        log(f"State reset for EP{ep_num:03d}")

    completed = set(state.get("completed_phases", []))

    # Determine which phases to run
    if args.only_phase:
        phases_to_run = [resolve_only_phase(args.only_phase)]
    elif args.from_phase:
        start_phase = resolve_from_phase(args.from_phase)
        idx = FULL_RELEASE_ORDER.index(start_phase)
        phases_to_run = FULL_RELEASE_ORDER[idx:]
    else:
        phases_to_run = FULL_RELEASE_ORDER

    log(f"\n{'='*60}")
    log(f"OpenClaw Daily — EP{ep_num:03d} Release Pipeline")
    log(f"Phases: {', '.join(phases_to_run)}")
    log(f"{'='*60}\n")

    build_log(f"🚀 Release pipeline started — phases: {', '.join(phases_to_run)}", ep_num)

    for phase in phases_to_run:
        if phase in completed and phase != "qc":
            log(f"[ {phase.upper()} ] Already completed, skipping")
            continue

        log(f"\n{'-'*60}")
        build_log(f"⏳ [{phase.upper()}] starting…", ep_num)
        try:
            state = run_named_phase(phase, ep_num, state, args.pub_date)

            completed.add(phase)
            state["completed_phases"] = list(completed)
            save_state(ep_num, state)
            log(f"[ {phase.upper()} ] ✅ Complete")
            build_log(f"✅ [{phase.upper()}] complete", ep_num)

        except Exception as e:
            log(f"[ {phase.upper()} ] ❌ FAILED: {e}")
            build_log(f"❌ [{phase.upper()}] FAILED: {e}", ep_num)
            save_state(ep_num, state)
            sys.exit(1)

    ep_str = f"{ep_num:03d}"
    log(f"\n{'='*60}")
    log(f"✅ EP{ep_num:03d} release complete!")
    log(f"  Feed: https://clawdassistant85-netizen.github.io/openclaw-podcast/feed.xml")
    log(f"  Audio: {CDN_BASE}/audio/episode_{ep_str}.mp3")
    log(f"  Website: https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/")
    build_log(
        f"🎙️ Release complete! "
        f"<https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/>",
        ep_num
    )
    log(f"{'='*60}")

if __name__ == "__main__":
    main()
