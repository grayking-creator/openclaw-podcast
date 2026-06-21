#!/usr/bin/env python3
"""
AgentStack Daily — Episode Release Pipeline
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
import shlex
import shutil
import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

import migrate_media_releases as media_releases

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
AUDIO_CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
MEDIA_EN_CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-media-en"
CDN_DIR = AUDIO_CDN_DIR
WEBSITE_DIR = Path.home() / ".openclaw/workspace/websiteBuilder"
WEBSITE_PODCAST_IMG = WEBSITE_DIR / "frontend/public/images/podcast"
WORKSPACE_DIR = Path.home() / ".openclaw/workspace"
WEBSITE_DEPLOY_HOST = os.environ.get("OPENCLAW_WEBSITE_DEPLOY_HOST", "gx10-594d")
WEBSITE_DEPLOY_TIMEOUT_SECONDS = int(os.environ.get("OPENCLAW_WEBSITE_DEPLOY_TIMEOUT_SECONDS", "180"))
WEBSITE_DEPLOY_SCRIPT = os.environ.get(
    "OPENCLAW_WEBSITE_DEPLOY_SCRIPT",
    "/home/toby/.openclaw/workspace/scripts/publish_podcast_website_update.py",
)

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
AUDIO_CDN_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio"
MEDIA_EN_CDN_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-media-en"
PODCAST_FEED_URL = "https://grayking-creator.github.io/openclaw-podcast/feed.xml"
CDN_BASE = AUDIO_CDN_BASE
MEDIA_EN_START_EPISODE = 57
EN_RELEASE_ASSET_START_EPISODE = 65


def en_media_target(ep_num):
    """Return the EN media repo that hosts this episode's approved assets."""
    if ep_num >= MEDIA_EN_START_EPISODE:
        return {"dir": MEDIA_EN_CDN_DIR, "base": MEDIA_EN_CDN_BASE}
    return {"dir": AUDIO_CDN_DIR, "base": AUDIO_CDN_BASE}


def is_en_release_asset_episode(ep_num):
    return ep_num >= EN_RELEASE_ASSET_START_EPISODE


def en_release_repo():
    return media_releases.LANG_REPOS["en"]


def en_release_tag(ep_num):
    return f"ep{ep_num:03d}"


def en_release_audio_name(ep_num):
    return f"episode_{ep_num:03d}.mp3"


def en_release_cover_name(ep_num):
    return f"episode_{ep_num:03d}_cover.png"


def en_release_show_notes_name(ep_num):
    return f"show_notes_episode_{ep_num:03d}.md"


def en_release_transcript_name(ep_num):
    return f"episode_{ep_num:03d}_transcript.md"


def en_release_asset_url(ep_num, asset_name):
    return media_releases.release_asset_url(en_release_repo(), en_release_tag(ep_num), asset_name)


def en_audio_url(ep_num):
    ep_str = f"{ep_num:03d}"
    if is_en_release_asset_episode(ep_num):
        return en_release_asset_url(ep_num, en_release_audio_name(ep_num))
    return f"{en_media_target(ep_num)['base']}/audio/episode_{ep_str}.mp3"


def en_cover_url(ep_num):
    ep_str = f"{ep_num:03d}"
    if is_en_release_asset_episode(ep_num):
        return en_release_asset_url(ep_num, en_release_cover_name(ep_num))
    return f"{en_media_target(ep_num)['base']}/episode_{ep_str}_cover.png"

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

def run(cmd, cwd=None, check=True, env=None, timeout=None):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"Command timed out after {timeout}s: {' '.join(str(c) for c in cmd)}"
        ) from exc
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(str(c) for c in cmd)}\n{result.stderr}")
    return result

def sync_repo_before_publish(repo_dir):
    """Fast-forward/rebase from upstream before the release lane stages files."""
    upstream = run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        cwd=str(repo_dir),
        check=False,
    )
    if upstream.returncode != 0:
        return
    run(["git", "pull", "--rebase", "--autostash"], cwd=str(repo_dir))

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
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip()
    env_value = os.environ.get(name, "")
    if env_value:
        return env_value

    provider_by_env = {
        "MINIMAX_API_KEY": "minimax",
        "GEMINI_API_KEY": "google",
        "GOOGLE_API_KEY": "google",
        "NVIDIA_API_KEY": "nvidia",
        "MISTRAL_API_KEY": "mistral",
    }
    provider = provider_by_env.get(name)
    config_file = Path.home() / ".openclaw/openclaw.json"
    if provider and config_file.exists():
        try:
            data = json.loads(config_file.read_text())
            providers = data.get("providers") or data.get("models", {}).get("providers") or {}
            value = (providers.get(provider) or {}).get("apiKey") or ""
            if value and not value.endswith("_API_KEY"):
                return value
        except Exception:
            return ""
    return ""

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

def push_current_branch_if_ahead(repo_dir):
    upstream = run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        cwd=str(repo_dir),
        check=False,
    )
    if upstream.returncode != 0:
        return False
    ahead = run(["git", "rev-list", "--count", "@{u}..HEAD"], cwd=str(repo_dir), check=False)
    if ahead.returncode != 0:
        return False
    try:
        ahead_count = int(ahead.stdout.strip() or "0")
    except ValueError:
        return False
    if ahead_count <= 0:
        return False
    run(["git", "push"], cwd=str(repo_dir))
    log(f"  ✅ Podcast repo pushed ({ahead_count} local commit(s) ahead)")
    return True

def podcast_cover_path(ep_num, lang=None):
    ep_str = f"{ep_num:03d}"
    if lang:
        return PODCAST_DIR / "images" / f"episode_{ep_str}_cover_{lang}.png"
    return PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"

def ensure_website_cover(ep_num, lang=None):
    """Compatibility helper: return the podcast cover that DGX will publish to the website."""
    return podcast_cover_path(ep_num, lang)

def git_commit_if_needed(repo_dir, message, env=None, extra_paths=None, allow_empty=False):
    sync_repo_before_publish(repo_dir)
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
    section = extract_section(notes, "Episode Title")
    if section:
        for raw_line in section.splitlines():
            line = collapse_ws(raw_line).strip("*_` ")
            if line:
                return line
    inline = re.search(r"^\*\*Title:\*\*\s*(.+?)\s*$", notes, re.MULTILINE)
    if inline:
        return collapse_ws(inline.group(1))
    return f"Episode {ep_num}"

def extract_tagline(notes):
    tagline = collapse_ws(extract_section(notes, "Tagline"))
    if tagline:
        return tagline
    inline = re.search(r"^\*\*Tagline:\*\*\s*(.+?)\s*$", notes, re.MULTILINE)
    return collapse_ws(inline.group(1)) if inline else ""

def extract_feed_description(notes):
    feed_desc = collapse_ws(extract_section(notes, "Feed Description"))
    if feed_desc:
        return feed_desc

    inline = re.search(r"^\*\*Feed description:\*\*\s*(.+?)\s*$", notes, re.MULTILINE | re.IGNORECASE)
    if inline:
        return collapse_ws(inline.group(1))

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


def derive_cover_lines_from_title(title):
    title = collapse_ws(strip_title_prefix(title).replace("—", ",").replace("–", ","))
    parts = [collapse_ws(part) for part in title.split(",") if collapse_ws(part)]
    if len(parts) >= 2:
        line1 = parts[0].upper()
        line2 = parts[1].upper()
        return line1, line2
    return fallback_cover_lines(title)


def normalize_translated_metadata(meta, ep_num, prefix, fallback_title, fallback_tagline):
    normalized = dict(meta or {})

    def clean_or_empty(value):
        text = collapse_ws(value)
        low = text.lower()
        if not text:
            return ""
        if "<" in text or ">" in text:
            return ""
        if "translated episode title" in low or "translated 2-3 sentence description" in low:
            return ""
        if "translated line" in low or "translated short tagline" in low:
            return ""
        return text

    title = clean_or_empty(normalized.get("title", "")) or f"{prefix} {ep_num}: {fallback_title}"
    normalized["title"] = title
    normalized["description"] = clean_or_empty(normalized.get("description", "")) or fallback_tagline or fallback_title

    line1 = clean_or_empty(normalized.get("cover_line1", "")).upper()
    line2 = clean_or_empty(normalized.get("cover_line2", "")).upper()
    generic_line1 = line1 in {"OPENCLAW", "AGENTSTACK DAILY", "ओपनक्लॉ"}
    if not line1 or generic_line1 or not line2:
        derived_line1, derived_line2 = derive_cover_lines_from_title(title)
        if not line1 or generic_line1:
            line1 = derived_line1
        if not line2:
            line2 = derived_line2
    normalized["cover_line1"] = line1
    normalized["cover_line2"] = line2

    tagline = clean_or_empty(normalized.get("cover_tagline", ""))
    normalized["cover_tagline"] = tagline or strip_title_prefix(title)
    return normalized

# ── Minimax translation ───────────────────────────────────────────────────────

_MINIMAX_WALL_TIMEOUT = 180  # hard wall-clock cap per attempt

def _minimax_call(prompt, max_tokens=4000, retries=3):
    import openai
    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
    key = load_env_key("MINIMAX_API_KEY")
    client = openai.OpenAI(base_url="https://api.minimaxi.chat/v1", api_key=key, timeout=_MINIMAX_WALL_TIMEOUT)
    last_err = None
    last_raw = None

    def _call():
        r = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            extra_body={"reasoning_split": True},
        )
        # With reasoning_split=True, content is clean translation only (no <think> tags)
        return r.choices[0].message.content or ""

    for attempt in range(1, retries + 1):
        try:
            ex = ThreadPoolExecutor(max_workers=1)
            future = ex.submit(_call)
            try:
                raw = future.result(timeout=_MINIMAX_WALL_TIMEOUT)
            except FutureTimeout:
                future.cancel()
                ex.shutdown(wait=False, cancel_futures=True)
                raise TimeoutError(f"wall-clock timeout after {_MINIMAX_WALL_TIMEOUT}s")
            else:
                ex.shutdown(wait=True)
            last_raw = raw
            clean = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
            if clean:
                return clean
            last_err = f"empty response (raw_len={len(raw)})"
            log(f"    ⚠️  Empty response (attempt {attempt}/{retries}), retrying...", indent=2)
            time.sleep(3 * attempt)
        except Exception as e:
            last_err = e
            log(f"    ⚠️  Minimax error (attempt {attempt}/{retries}): {e}", indent=2)
            time.sleep(5 * attempt)
    raw_note = ""
    if isinstance(last_raw, str) and last_raw:
        preview = last_raw[:200].replace("\n", " ")
        raw_note = f" Raw preview: {preview!r}"
    raise RuntimeError(f"Minimax API failed after {retries} attempts. Last error: {last_err}.{raw_note}")


def _local_claude_call(prompt, max_tokens=4000):
    """Call the local OpenClaw Claude gateway only after explicit opt-in."""
    if os.getenv("ALLOW_CLAUDE_RELEASE_GATEWAY") != "1":
        raise RuntimeError(
            "Local Claude release gateway is disabled. Set "
            "ALLOW_CLAUDE_RELEASE_GATEWAY=1 only after explicit approval."
        )
    import urllib.request, json as _json
    payload = _json.dumps({
        "model": "claude-code",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:18792/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": "Bearer none"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = _json.loads(resp.read())
    return data["choices"][0]["message"]["content"].strip()


def _nvidia_gateway_call(prompt, max_tokens=4000):
    """Call NVIDIA DeepSeek V3.2 via local gateway — non-OpenAI, non-Anthropic fallback."""
    import urllib.request, json as _json
    payload = _json.dumps({
        "model": "nvidia/deepseek-ai/deepseek-v3.2",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:18792/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": "Bearer none"},
    )
    with urllib.request.urlopen(req, timeout=480) as resp:
        data = _json.loads(resp.read())
    return data["choices"][0]["message"]["content"].strip()


def _mistral_call(prompt, max_tokens=4000):
    """Call Mistral large via API — reliable multilingual fallback."""
    import urllib.request, json as _json
    key = load_env_key("MISTRAL_API_KEY")
    if not key:
        raise RuntimeError("MISTRAL_API_KEY not configured")
    payload = _json.dumps({
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(
        "https://api.mistral.ai/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = _json.loads(resp.read())
    return data["choices"][0]["message"]["content"].strip()


def gemini_call(prompt, max_tokens=4000, retries=3):
    """Translation backend chain: Minimax×3 → Gemini×1 → Mistral → NVIDIA DeepSeek V3.2."""
    # 1. Minimax M2.7 — up to `retries` attempts (default 3)
    try:
        return _minimax_call(prompt, max_tokens, retries)
    except RuntimeError as minimax_err:
        log(f"    ⚠️  Minimax exhausted ({minimax_err}), trying Gemini...", indent=2)

    # 2. Gemini — primary key only (fallback key has project-level 403)
    from google import genai
    last_gemini_err = None
    key = load_env_key("GEMINI_API_KEY")
    if key:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"max_output_tokens": max_tokens},
            )
            return r.text.strip()
        except Exception as e:
            log(f"    ⚠️  Gemini GEMINI_API_KEY/gemini-2.5-flash failed: {e}", indent=2)
            last_gemini_err = e

    # 3. Mistral large (256k context, strong multilingual)
    log("    ⚠️  Gemini exhausted, trying Mistral large...", indent=2)
    try:
        return _mistral_call(prompt, max_tokens)
    except Exception as mistral_err:
        log(f"    ⚠️  Mistral failed: {mistral_err}", indent=2)

    # 4. NVIDIA DeepSeek V3.2 via local gateway (non-OpenAI, non-Anthropic)
    log("    ⚠️  Mistral exhausted, trying NVIDIA DeepSeek V3.2...", indent=2)
    try:
        return _nvidia_gateway_call(prompt, max_tokens)
    except Exception as nvidia_err:
        raise RuntimeError(
            f"All translation backends exhausted. "
            f"Minimax failed, Gemini failed ({last_gemini_err}), "
            f"Mistral failed, NVIDIA failed ({nvidia_err})"
        ) from nvidia_err

# Languages whose target script is non-Latin. Title translation must produce
# text in these scripts; an all-Latin title fails the QC rule and is treated
# as a translation miss, not a "keep proper nouns" exception.
NON_LATIN_LANGS = {"hi"}  # Hindi is Devanagari; ES/DE/PT are Latin-script but still must differ from EN

def _title_body_is_mostly_english(translated_title: str, en_title: str) -> bool:
    """Detect the EP072-style bug: model returned a title whose body after the
    "{prefix} {ep_num}:" prefix is essentially the English title unchanged.

    QC fails because the translated title is indistinguishable from the
    English title. Returns True when the title needs to be re-translated with
    a stronger prompt.
    """
    if not translated_title or not en_title:
        return False
    # Strip leading "{prefix} {ep_num}:" if present
    m = re.match(r"^.+?\s+\d+\s*[:\-–]\s*(.+)$", translated_title.strip())
    body = (m.group(1) if m else translated_title).strip()
    en = en_title.strip()
    # Case-insensitive, whitespace-normalized equality → identical body
    if re.sub(r"\s+", " ", body.lower()) == re.sub(r"\s+", " ", en.lower()):
        return True
    # Non-Latin languages: if no script-native characters are present, model
    # silently fell back to English
    if NON_LATIN_LANGS:
        pass  # handled per-lang by caller
    return False


def _title_missing_native_script(translated_title: str, lang: str) -> bool:
    """For non-Latin target scripts, require SOME characters in the target
    script. A Hindi title that contains zero Devanagari is just English."""
    if lang not in NON_LATIN_LANGS:
        return False
    if not translated_title:
        return True
    # Devanagari U+0900–U+097F
    return not re.search(r"[\u0900-\u097F]", translated_title)


def translate_metadata(ep_num, lang):
    """Returns dict: title, description, cover_line1, cover_line2, cover_tagline.

    Translates with up to 3 Gemini attempts: a default prompt, then a stronger
    "actually translate the body" prompt if the model returned an English body
    or (for non-Latin scripts) zero script-native characters.
    """
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
        derived_line1, derived_line2 = derive_cover_lines_from_title(en_title)
        line1 = l1m.group(1) if l1m else derived_line1
        line2 = l2m.group(1) if l2m else derived_line2
        cover_tag = ctm.group(1) if ctm else en_tagline

    base_prompt = f"""Translate this podcast episode metadata from English to {lang_name}.
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

    reinforce_prompt = f"""You previously translated this podcast metadata to {lang_name}
but the title body is still in English. Translate EVERY non-proper-noun word
to {lang_name}. Keep ONLY these in English:
  - Product names: OpenClaw, Codex, Claude Code, Hermes, MiniMax, ChatGPT, Gemini, GLM
  - Model names and version numbers: GLM-5.2, rust-v0.141.0, 2.1.170, 2026.6.8
  - Generic tech terms that are universal in {lang_name}: API, SDK, MCP, RAG
Translate ALL of: verbs, adjectives, common nouns, and connectives. The title
MUST differ from the English body by more than just the "{prefix} {ep_num}:"
prefix. Common phrases to translate: "Open Weights", "shipped", "released",
"launches", "update", "new", "model", "tools".

English episode title: "{en_title}"
Title prefix for this language: "{prefix}"

Return ONLY the corrected JSON object (same shape as before), nothing else."""

    last_meta = None
    for attempt in range(3):
        prompt = reinforce_prompt if attempt > 0 else base_prompt
        raw = gemini_call(prompt, max_tokens=4000)
        json_m = re.search(r'\{[\s\S]*\}', raw)
        if not json_m:
            log(f"  ⚠️  [translate_metadata] {lang}: no JSON in attempt {attempt + 1}; retrying")
            continue
        try:
            meta = json.loads(json_m.group(0))
        except json.JSONDecodeError as exc:
            log(f"  ⚠️  [translate_metadata] {lang}: JSON parse failed ({exc}); retrying")
            continue
        meta = normalize_translated_metadata(
            meta, ep_num, prefix, en_title, en_tagline or en_desc
        )
        last_meta = meta
        title = meta.get("title", "")
        if attempt == 0 and (
            _title_body_is_mostly_english(title, en_title)
            or _title_missing_native_script(title, lang)
        ):
            log(
                f"  ⚠️  [translate_metadata] {lang}: title body still English "
                f"(attempt 1: {title!r}); retrying with reinforcement prompt"
            )
            continue
        return meta

    # All attempts produced an English body — return the last one and let QC
    # surface the failure rather than silently keep retrying forever.
    log(
        f"  ❌ [translate_metadata] {lang}: 3 attempts all returned English body "
        f"(last title: {last_meta.get('title') if last_meta else '<none>'!r}); "
        "QC will fail — investigate model output"
    )
    return last_meta

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
        raw = gemini_call(prompt, max_tokens=16000)
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

    # 20-paragraph chunks for most languages; 10 for Hindi — Devanagari generates
    # significantly more output tokens, causing Minimax to consistently exceed the
    # 180s wall-clock timeout at 20 paragraphs.
    paragraphs = transcript_paragraphs(text)
    chunk_size = 10 if lang == "hi" else 20
    chunks = [paragraphs[i:i+chunk_size] for i in range(0, len(paragraphs), chunk_size)]

    translated_chunks = []
    for i, chunk in enumerate(chunks):
        log(f"    Translating chunk {i+1}/{len(chunks)} ({len(chunk)} paragraphs)...", indent=2)
        result = None
        last_error = None
        for attempt in range(1, 4):
            try:
                if chunk_type == "transcript":
                    result = translate_transcript_chunk(chunk, lang_name)
                else:
                    chunk_text = "\n\n".join(chunk)
                    prompt = f"{system_note}\n\nTranslate the following:\n\n{chunk_text}"
                    result = gemini_call(prompt, max_tokens=16000)
                validate_language_scripts(result, lang, f"{chunk_type} chunk {i+1}/{len(chunks)}")
                break
            except Exception as exc:
                last_error = exc
                if attempt >= 3:
                    raise
                log(
                    f"      ⚠️  Chunk {i+1}/{len(chunks)} retry {attempt}/3 after validation failure: {exc}",
                    indent=3,
                )
                time.sleep(2 * attempt)
        if result is None and last_error is not None:
            raise last_error
        translated_chunks.append(result)
        if i < len(chunks) - 1:
            time.sleep(1)  # polite pause between chunks

    return "\n\n".join(translated_chunks)

# ── Cover generation ──────────────────────────────────────────────────────────

def generate_en_cover(ep_num):
    """Generate EN cover art from show notes title — LLM picks cover lines."""
    ep_str = f"{ep_num:03d}"
    notes = (PODCAST_DIR / f"show_notes_episode_{ep_str}.md").read_text()
    title = extract_episode_title(notes, ep_num)
    tag_m = re.search(r"^## Tagline\s*\n(.+?)(?=\n\n|\n##)", notes, re.MULTILINE | re.DOTALL)
    tagline = (tag_m.group(1).strip() if tag_m else "").split(".")[0][:60]

    # Extract cover lines from title structure: split on commas and "and"
    # e.g. "Claw Tax, Courtrooms, and the New AI Stack" → ["CLAW TAX", "COURTROOMS", "THE NEW AI STACK"]
    def extract_cover_lines(t):
        # Strip episode number prefix if present (e.g. "Episode 29: ...")
        t = re.sub(r'^Episode\s+\d+:\s*', '', t, flags=re.IGNORECASE)
        # Cover text should sell the story, not repeat release-number bookkeeping.
        # Remove version tokens and drop empty/generic OpenClaw-only chunks so release-led
        # episodes can still use the concrete follow-on stories as the readable title.
        t = re.sub(r'\bv\d{4}\.\d+\.\d+\b', '', t, flags=re.IGNORECASE)
        # Split on ", and ", ", ", " and "
        parts = re.split(r',\s*(?:and\s+)?|\s+and\s+', t)
        cleaned = []
        for p in parts:
            p = re.sub(r'\s+', ' ', p).strip(' :-—–').upper()
            if not p or p in ("THE", "A", "AN", "AND", "OR", "BUT", "IN", "OF", "OPENCLAW", "AGENTSTACK DAILY"):
                continue
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

    # Per-episode bespoke middle art is mandatory. Do not silently render generic fallback art.
    _art_path = SCRIPTS_DIR / "episode_art" / f"episode_{ep_num:03d}_art.py"
    if not _art_path.exists():
        raise FileNotFoundError(
            f"Missing bespoke art module for EP{ep_num:03d}; fallback cover art is disabled"
        )

    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(f"episode_{ep_num:03d}_art", _art_path)
    _art_mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_art_mod)
    img = _art_mod.draw_art(img, W, H)
    d = ImageDraw.Draw(img)

    # Fonts
    font_path_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    font_path_reg  = "/System/Library/Fonts/Supplemental/Arial.ttf"
    hi_font_paths  = [
        "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc",
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
        font_sub   = ImageFont.truetype(title_font_path if is_hindi else font_path_reg, 28 if is_hindi else 30)
    except Exception:
        font_show = font_ep = font_title = font_sub = ImageFont.load_default()
        base_title_size = 118

    md = ImageDraw.Draw(img)

    SHOW_TEXT = "AGENTSTACK DAILY"
    EP_TEXT   = f"EP{ep_num:03d}"
    line1     = collapse_ws(meta.get("cover_line1", "")).upper()
    line2     = collapse_ws(meta.get("cover_line2", "")).upper()
    tagline   = collapse_ws(meta.get("cover_tagline", ""))
    generic_line1 = line1 in {"OPENCLAW", "AGENTSTACK DAILY", "ओपनक्लॉ"}
    if not line1 or generic_line1 or not line2:
        derived_line1, derived_line2 = derive_cover_lines_from_title(meta.get("title", ""))
        if not line1 or generic_line1:
            line1 = derived_line1 or line1
        if not line2:
            line2 = derived_line2 or line2

    def fit_font(text_value, start_size, min_size=42, max_width=W-180):
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

    # "AGENTSTACK DAILY" top
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
    md.text(((W-l1w)/2+3, 1028), line1, font=font_title_l1, fill=(0, 0, 0, 160))
    tg1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tg1).text(((W-l1w)/2, 1025), line1, font=font_title_l1, fill=TEAL+(50,))
    img = Image.alpha_composite(img, tg1.filter(ImageFilter.GaussianBlur(14)))
    md = ImageDraw.Draw(img)
    md.text(((W-l1w)/2, 1025), line1, font=font_title_l1, fill=WHITE+(255,))

    # Line 2 — amber glow
    l2w = md.textlength(line2, font=font_title_l2)
    md.text(((W-l2w)/2+4, 1158), line2, font=font_title_l2, fill=(0, 0, 0, 170))
    tg2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tg2).text(((W-l2w)/2, 1155), line2, font=font_title_l2, fill=AMBER+(80,))
    img = Image.alpha_composite(img, tg2.filter(ImageFilter.GaussianBlur(16)))
    md = ImageDraw.Draw(img)
    md.text(((W-l2w)/2, 1155), line2, font=font_title_l2, fill=AMBER_BRIGHT+(255,))

    # Tagline
    def wrap_text(text_value, font, max_width):
        words = text_value.split()
        if not words:
            return []
        lines = []
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if md.textlength(candidate, font=font) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def fit_tagline(text_value, start_size, min_size=22, max_lines=2, max_width=W-120):
        size = start_size
        while size >= min_size:
            candidate_font = ImageFont.truetype(title_font_path if is_hindi else font_path_reg, size)
            wrapped = wrap_text(text_value, candidate_font, max_width)
            if wrapped and len(wrapped) <= max_lines:
                return candidate_font, wrapped
            size -= 2
        candidate_font = ImageFont.truetype(title_font_path if is_hindi else font_path_reg, min_size)
        wrapped = wrap_text(text_value, candidate_font, W-120)
        return candidate_font, wrapped[:2]

    # No extra bottom tagline. It frequently duplicates version metadata or creates a
    # third competing text block; covers should stay clean: show name, episode number,
    # two-line story title, and bespoke art only.

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
    if en_episode_title.strip() == f"Episode {ep_num}":
        raise RuntimeError(
            f"EP{ep_num}: episode title did not resolve from show notes — extract_episode_title "
            f"fell back to the bare 'Episode {ep_num}' placeholder. Refusing to emit a feed entry "
            f"with a placeholder title (this produced the 'Episode {ep_num}: Episode {ep_num}' feed "
            f"bug). Ensure show_notes_episode_{ep_str}.md has an '## Episode Title' section or a "
            f"'**Title:**' line before publishing."
        )
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


def cover_stale_against_art(cover_path, art_path):
    if not cover_path.exists() or not art_path.exists():
        return False
    return cover_path.stat().st_mtime < art_path.stat().st_mtime


def sync_if_newer(src_path, dst_path):
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    if (
        not dst_path.exists()
        or src_path.stat().st_mtime > dst_path.stat().st_mtime
        or src_path.stat().st_size != dst_path.stat().st_size
    ):
        shutil.copy2(str(src_path), str(dst_path))
        return True
    return False


def ensure_bespoke_art_module(ep_num, force=False):
    ep_str = f"{ep_num:03d}"
    art_mod_path = SCRIPTS_DIR / "episode_art" / f"episode_{ep_str}_art.py"
    if art_mod_path.exists() and not force:
        log(f"  ✅ Art module ready: {art_mod_path.name}")
        return art_mod_path

    if force and art_mod_path.exists():
        log(f"  ♻️  Regenerating art module: {art_mod_path.name}")
    else:
        log(f"  → Generating bespoke art module for EP{ep_str}...")

    gen_script = SCRIPTS_DIR / "generate_episode_art.py"
    result = subprocess.run(
        ["python3", str(gen_script), str(ep_num)],
        capture_output=False,
        text=True,
    )
    if result.returncode != 0 or not art_mod_path.exists():
        raise RuntimeError(
            f"Bespoke art module generation failed for EP{ep_str}; "
            "fallback cover art is disabled"
        )

    log(f"  ✅ Art module ready: {art_mod_path.name}")
    return art_mod_path


def assert_feed_sequence(feed_path, ep_num):
    if ep_num <= 0 or not feed_path.exists():
        return
    feed_text = feed_path.read_text()
    existing = {int(m) for m in re.findall(r"<itunes:episode>(\d+)</itunes:episode>", feed_text)}
    if not existing or ep_num in existing:
        return
    expected = 0
    while expected in existing:
        expected += 1
    if ep_num != expected:
        expected_str = f"{expected:03d}"
        prior_draft = PODCAST_DIR / f"show_notes_episode_{expected_str}.md"
        draft_hint = (
            f"\nUnreleased prior draft exists: {prior_draft.name}"
            if prior_draft.exists()
            else ""
        )
        raise RuntimeError(
            f"Refusing to publish EP{ep_num:03d}: {feed_path.name} expects EP{expected:03d} next."
            f"{draft_hint}\n"
            "Choose one recovery path before publishing:\n"
            f"1. Keep the prior stories: merge EP{expected_str}'s Story Slate into the episode you meant to publish, "
            "then publish the next expected episode number.\n"
            f"   Helper: python3 scripts/resolve_episode_gap.py prepare-merge --prior {expected} --target {ep_num}\n"
            f"2. Replace the prior stories: archive EP{expected_str}'s draft/assets and reuse EP{expected_str} "
            "for the new story slate, regenerating transcript, audio, cover, translations, and YouTube assets from that replacement.\n"
            f"   Helper: python3 scripts/resolve_episode_gap.py archive {expected} --reason 'replaced before transcript generation'"
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


def upload_en_release_assets(ep_num, include_review_docs=True):
    ep_str = f"{ep_num:03d}"
    audio_path = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    cover_path = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    show_notes_path = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    transcript_path = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript.md"

    if not audio_path.exists():
        raise FileNotFoundError(f"Missing EN audio: {audio_path}")
    if not cover_path.exists():
        raise FileNotFoundError(f"Missing EN cover: {cover_path}")

    assets = {
        en_release_audio_name(ep_num): audio_path,
        en_release_cover_name(ep_num): cover_path,
    }
    if include_review_docs:
        if show_notes_path.exists():
            assets[en_release_show_notes_name(ep_num)] = show_notes_path
        if transcript_path.exists():
            assets[en_release_transcript_name(ep_num)] = transcript_path

    repo = en_release_repo()
    media_releases.ensure_repo_initialized(repo)
    media_releases.ensure_release_with_assets(
        repo,
        en_release_tag(ep_num),
        f"EP{ep_str}",
        assets,
    )


def deploy_website(ep_num, message, extra_paths):
    log(f"  Delegating website deploy to {WEBSITE_DEPLOY_HOST}...")

    cover_names = []
    cover_paths = []
    for path in extra_paths:
        name = Path(path).name
        src = PODCAST_DIR / "images" / name
        if not src.exists():
            raise FileNotFoundError(f"Missing podcast cover for website deploy: {src}")
        cover_names.append(name)
        cover_paths.append(src)
    if not cover_paths:
        raise RuntimeError("No website cover assets provided for delegated deploy")

    remote_staging = f"/tmp/openclaw_podcast_website_update_ep{ep_num:03d}_{os.getpid()}_{uuid.uuid4().hex[:8]}"
    ssh_base = [
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=15",
        "-o", "ServerAliveInterval=10",
        "-o", "ServerAliveCountMax=2",
        WEBSITE_DEPLOY_HOST,
    ]
    try:
        run(ssh_base + ["mkdir", "-p", remote_staging], timeout=WEBSITE_DEPLOY_TIMEOUT_SECONDS)
        run(
            ["rsync", "-az"] + [str(path) for path in cover_paths] + [f"{WEBSITE_DEPLOY_HOST}:{remote_staging}/"],
            timeout=WEBSITE_DEPLOY_TIMEOUT_SECONDS,
        )
        remote_cmd = [
            "python3",
            WEBSITE_DEPLOY_SCRIPT,
            "--episode",
            str(ep_num),
            "--message",
            message,
            "--empty-message",
            f"EP{ep_num}: trigger website deploy",
            "--staging-dir",
            remote_staging,
        ] + [arg for name in cover_names for arg in ("--cover", name)]
        result = run(ssh_base + [shlex.join(remote_cmd)], timeout=WEBSITE_DEPLOY_TIMEOUT_SECONDS)
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                log(f"  {line}")
        log("  ✅ Website deploy handled by DGX")
    except Exception as exc:
        build_log(f"❌ [WEBSITE] blocking deploy failure: {exc}", ep_num)
        raise
    finally:
        run(ssh_base + ["rm", "-rf", remote_staging], check=False, timeout=30)

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

    art_mod_path = ensure_bespoke_art_module(ep_num)

    # Check EN cover — generate if missing or stale versus newer bespoke art
    en_cover = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    if not en_cover.exists():
        log(f"  ℹ️  EN cover missing — generating from show notes...")
        generate_en_cover(ep_num)
        log(f"  ✅ EN cover generated")
    elif cover_stale_against_art(en_cover, art_mod_path):
        log(f"  ♻️  EN cover is older than {art_mod_path.name} — re-rendering")
        generate_en_cover(ep_num)
        log(f"  ✅ EN cover refreshed")
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

def phase_translate(ep_num, state, langs=None):
    """Translate episode content. Pass langs=[...] to translate only specific languages."""
    target_langs = langs if langs is not None else LANGS
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

    for lang in target_langs:
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

def phase_covers(ep_num, state, langs=None):
    log("[ COVERS ] Generating translated cover art...")
    ep_str = f"{ep_num:03d}"
    target_langs = list(langs or LANGS)
    translations = state.get("translations", {})
    en_notes = (PODCAST_DIR / f"show_notes_episode_{ep_str}.md").read_text()
    en_episode_title = extract_episode_title(en_notes, ep_num)
    en_tagline = extract_tagline(en_notes) or extract_feed_description(en_notes)

    # Bespoke art is a required prerequisite for all cover generation.
    art_mod_path = ensure_bespoke_art_module(ep_num)

    # Also copy EN cover to CDN
    en_cover_src = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    en_cover_cdn = en_media_target(ep_num)["dir"] / f"episode_{ep_str}_cover.png"
    if cover_stale_against_art(en_cover_src, art_mod_path):
        log(f"  ♻️  EN cover is older than {art_mod_path.name} — re-rendering")
        generate_en_cover(ep_num)
    if sync_if_newer(en_cover_src, en_cover_cdn):
        log(f"  ✅ EN cover → CDN")

    # Copy EN cover to website
    WEBSITE_PODCAST_IMG.mkdir(parents=True, exist_ok=True)
    en_cover_web = WEBSITE_PODCAST_IMG / f"episode_{ep_str}_cover.png"
    if sync_if_newer(en_cover_src, en_cover_web):
        log(f"  ✅ EN cover → website")

    for lang in target_langs:
        out_path = PODCAST_DIR / "images" / f"episode_{ep_str}_cover_{lang}.png"
        needs_refresh = cover_stale_against_art(out_path, art_mod_path)
        if out_path.exists() and not needs_refresh:
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
            if needs_refresh:
                log(f"  ♻️  {lang.upper()} cover is older than {art_mod_path.name} — re-rendering")
            else:
                log(f"  → Generating {lang.upper()} cover...")
            generate_translated_cover(ep_num, lang, meta)
            log(f"  ✅ {out_path.name}")

        # Copy to website
        web_cover = WEBSITE_PODCAST_IMG / f"episode_{ep_str}_cover_{lang}.png"
        if sync_if_newer(out_path, web_cover):
            log(f"     → {web_cover.name} copied to website")

    return state

def phase_feeds(ep_num, state, pub_date):
    log("[ FEEDS ] Adding feed entries...")
    state = phase_en_feed(ep_num, state, pub_date)
    state = phase_translated_feeds(ep_num, state, pub_date)
    return state


def ensure_en_feed_item_media(feed_path, ep_num, audio_url, cover_url, duration, length):
    """Keep an existing EN feed item pointed at the current media host."""
    text = feed_path.read_text(encoding="utf-8")
    episode_pat = re.escape(f"<itunes:episode>{ep_num}</itunes:episode>")
    item_re = re.compile(r"(?P<item><item>.*?" + episode_pat + r".*?</item>)", re.DOTALL)
    match = item_re.search(text)
    if not match:
        return False

    item = match.group("item")
    direct_enclosure = f"https://op3.dev/e/{audio_url}"
    updated = re.sub(
        r'<enclosure url="[^"]*" length="[^"]*" type="audio/mpeg"\s*/>',
        f'<enclosure url="{direct_enclosure}" length="{length}" type="audio/mpeg"/>',
        item,
        count=1,
    )
    updated = re.sub(
        r"<itunes:duration>[^<]*</itunes:duration>",
        f"<itunes:duration>{duration}</itunes:duration>",
        updated,
        count=1,
    )
    updated = re.sub(
        r'<itunes:image href="[^"]*"\s*/>',
        f'<itunes:image href="{cover_url}"/>',
        updated,
        count=1,
    )
    if updated == item:
        return False

    new_text = text[: match.start("item")] + updated + text[match.end("item") :]
    feed_path.write_text(new_text, encoding="utf-8")
    ET.parse(feed_path)
    return True


def phase_en_feed(ep_num, state, pub_date):
    log("[ FEEDS / EN ] Adding EN feed entry...")
    ep_str = f"{ep_num:03d}"
    meta = get_en_release_metadata(ep_num, state)
    add_feed_script = str(SCRIPTS_DIR / "add_feed_entry.py")
    if is_en_release_asset_episode(ep_num):
        upload_en_release_assets(ep_num)
        review_audio = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
        review_cover = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
        log(f"  ✅ EN media release assets uploaded: {en_release_tag(ep_num)}")
    else:
        en_target = en_media_target(ep_num)
        review_audio = en_target["dir"] / "audio" / f"episode_{ep_str}.mp3"
        review_cover = en_target["dir"] / f"episode_{ep_str}_cover.png"
    if not review_audio.exists() or not review_cover.exists():
        raise FileNotFoundError(
            "Missing pre-approval CDN review assets. "
            f"Expected {review_audio.name} and {review_cover.name} from build_episode.py"
        )

    # EN feed
    en_audio_url_value = en_audio_url(ep_num)
    en_cover_url_value = en_cover_url(ep_num)
    en_link = f"https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"

    en_feed = PODCAST_DIR / "feed.xml"
    assert_feed_sequence(en_feed, ep_num)
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
            "--audio-url", en_audio_url_value,
            "--cover-url", en_cover_url_value,
            "--duration", meta["duration"],
            "--link", en_link,
            "--length", str(meta["size"]),
        ])
        log(f"  ✅ EN feed updated")
    elif ensure_en_feed_item_media(
        en_feed,
        ep_num,
        en_audio_url_value,
        en_cover_url_value,
        meta["duration"],
        str(meta["size"]),
    ):
        log(f"  ✅ EN feed media URLs repaired")
    else:
        log(f"  ⏭  EN feed already has EP{ep_num}")

    return state


def update_translated_feed_entry(ep_num, lang, *, title=None, description=None):
    """Patch the existing <item> for EP{ep_num} in translations/feed_{lang}.xml
    in place — used when a feed entry was inserted with a bad title (EP072-style
    bug: only the prefix was translated) and we need to update the title /
    description without re-inserting (which would fail the duplicate check).

    Returns True if the feed was modified, False if no matching item was found.
    Validates the XML before and after the rewrite.
    """
    import xml.etree.ElementTree as ET
    feed_path = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
    if not feed_path.exists():
        log(f"  ℹ️  No {feed_path.name} to update")
        return False
    text = feed_path.read_text(encoding="utf-8")
    try:
        ET.fromstring(text)
    except ET.ParseError as exc:
        raise RuntimeError(f"{feed_path} is not valid XML; refusing to patch: {exc}") from exc

    # Locate the item block for this episode: anchor on <itunes:episode>{ep_num}
    # and walk back to its enclosing <item>...</item>.
    pattern = re.compile(
        rf"(    <!-- Episode {ep_num} -->\n)?"
        rf"(\s*)<item>(?:(?!</item>).)*?<itunes:episode>{ep_num}</itunes:episode>(?:(?!</item>).)*?</item>",
        re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        log(f"  ℹ️  No existing EP{ep_num} item in {feed_path.name}; nothing to update")
        return False

    item_text = m.group(0)
    new_item = item_text

    if title is not None:
        # Escape XML special chars minimally in the title
        safe_title = (title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        new_item = re.sub(
            r"<title>.*?</title>",
            f"<title>{safe_title}</title>",
            new_item,
            count=1,
        )
    if description is not None:
        # The description is wrapped in <![CDATA[...]]>; substitute the body.
        def _replace_desc(match: re.Match) -> str:
            inner = description.replace("]]>", "]]]]><![CDATA[>")
            return f"<description><![CDATA[{inner}]]></description>"

        new_item = re.sub(
            r"<description><!\[CDATA\[.*?\]\]></description>",
            _replace_desc,
            new_item,
            count=1,
            flags=re.DOTALL,
        )

    if new_item == item_text:
        log(f"  ⏭  {feed_path.name} EP{ep_num}: no field changed; nothing to update")
        return False

    new_text = text[: m.start()] + new_item + text[m.end() :]
    # Validate the rewritten XML
    try:
        ET.fromstring(new_text)
    except ET.ParseError as exc:
        raise RuntimeError(
            f"Rewritten {feed_path.name} is not valid XML; refusing to write: {exc}"
        ) from exc
    feed_path.write_text(new_text, encoding="utf-8")
    log(f"  ✅ {feed_path.name} EP{ep_num}: updated in place (title/description patched)")
    return True


def phase_translated_feeds(ep_num, state, pub_date, langs=None):
    log("[ FEEDS / TRANSLATED ] Adding translated feed entries...")
    ep_str = f"{ep_num:03d}"
    translations = state.get("translations", {})
    en_meta = get_en_release_metadata(ep_num, state)
    add_feed_script = str(SCRIPTS_DIR / "add_feed_entry.py")

    # Translated feeds
    for lang in (langs if langs is not None else LANGS):
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
        meta = normalize_translated_metadata(
            meta,
            ep_num,
            prefix,
            en_meta["episode_title"],
            en_meta["description"],
        )
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
    youtube_python = sys.executable
    for candidate in (
        PODCAST_DIR / ".venv_youtube/bin/python3",
        PODCAST_DIR / ".venv_shorts/bin/python3",
    ):
        if candidate.exists():
            youtube_python = str(candidate)
            break
    video_mode = str(state.get("youtube_video_mode", "static")).strip().lower() or "static"
    result = subprocess.run(
        [youtube_python, str(SCRIPTS_DIR / "youtube_scheduled_upload.py"), str(ep_num), "--video-mode", video_mode],
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

def phase_translated_cdn(ep_num, state, langs=None):
    target_langs = list(langs or LANGS)
    log("[ CDN / TRANSLATED ] Uploading translated audio + covers to media release repos...")
    for lang in target_langs:
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
    elif push_current_branch_if_ahead(PODCAST_DIR):
        pass
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

def phase_publish_translations(ep_num, state, langs=None):
    target_langs = list(langs or LANGS)
    log("[ PUBLISH / TRANSLATED ] Pushing translated podcast + website...")
    ep_str = f"{ep_num:03d}"
    stage = []
    for lang in target_langs:
        stage.append(f"translations/feed_{lang}.xml")
        ensure_website_cover(ep_num, lang)
        stage += [
            f"images/episode_{ep_str}_cover_{lang}.png",
            f"translations/{lang}/episode_{ep_str}_{lang}.md",
            f"translations/{lang}/show_notes_episode_{ep_str}_{lang}.md",
        ]
    push_podcast_stage(ep_num, stage, f"EP{ep_num}: publish translated episode_{ep_str} ({'-'.join(target_langs)})")
    deploy_website(
        ep_num,
        f"EP{ep_num}: translated cover art + website update ({'-'.join(target_langs)})",
        [f"frontend/public/images/podcast/episode_{ep_str}_cover_{lang}.png" for lang in target_langs],
    )

    return state

def phase_discord(ep_num, state):
    import urllib.request, urllib.error

    DISCORD_TOKEN = load_env_key("DISCORD_BOT_TOKEN")
    GUILD_ID = "1475905694145318944"
    DAILY_CHANNEL_ID = "1485445727772475533"
    DAILY_CHANNEL_NAME = "agentstack-daily"
    ep_str = f"{ep_num:03d}"
    working_channel_names = (f"agent-stack-ep{ep_str}", f"openclaw-ep{ep_str}")

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

    log(
        f"[ DISCORD ] Posting release to #{DAILY_CHANNEL_NAME} and cleaning up "
        f"{', '.join('#' + name for name in working_channel_names)}..."
    )

    discord_state = state.setdefault("discord_cleanup", {})

    # Read show notes for the release announcement
    show_notes_path = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    if show_notes_path.exists():
        show_notes = show_notes_path.read_text()
        lines = show_notes.splitlines()
        title_line = next((l for l in lines if l.startswith("# EP")), f"# EP{ep_str}")
        tagline_line = next((l for l in lines if l.startswith("**AgentStack Daily**")), "")
        announcement = f"🎙️ **EP{ep_str} is live!**\n\n{title_line}\n{tagline_line}\n\nhttps://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"
    else:
        announcement = f"🎙️ **EP{ep_str} is live!**\nhttps://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"

    if not discord_state.get("daily_posted"):
        discord_request("POST", f"/channels/{DAILY_CHANNEL_ID}/messages", {"content": announcement})
        discord_state["daily_posted"] = True
        save_state(ep_num, state)
        log(f"  ✅ Posted to #{DAILY_CHANNEL_NAME}")
    else:
        log(f"  ℹ️  #{DAILY_CHANNEL_NAME} post already sent")

    channels = discord_request("GET", f"/guilds/{GUILD_ID}/channels")
    ep_channels = [c for c in channels if c.get("name") in working_channel_names]
    if ep_channels:
        deleted_names = []
        for ep_channel in ep_channels:
            discord_request("DELETE", f"/channels/{ep_channel['id']}")
            deleted_names.append(ep_channel.get("name") or ep_channel["id"])
        discord_state["working_channel_deleted"] = True
        discord_state["working_channel_deleted_names"] = deleted_names
        discord_state.pop("working_channel_delete_missing_names", None)
        save_state(ep_num, state)
        log(f"  ✅ Deleted {', '.join('#' + name for name in deleted_names)}")
    elif discord_state.get("working_channel_deleted"):
        log(
            "  ℹ️  Working channel already marked deleted and no matching channel "
            f"found ({', '.join('#' + name for name in working_channel_names)})"
        )
    else:
        discord_state["working_channel_deleted"] = False
        discord_state["working_channel_delete_missing_names"] = list(working_channel_names)
        save_state(ep_num, state)
        raise RuntimeError(
            "Discord working channel not found for cleanup; looked for "
            + ", ".join(f"#{name}" for name in working_channel_names)
        )

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
    parser = argparse.ArgumentParser(description="AgentStack Daily episode release pipeline")
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
    log(f"AgentStack Daily — EP{ep_num:03d} Release Pipeline")
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
    log(f"  Feed: {PODCAST_FEED_URL}")
    log(f"  Audio: {en_audio_url(ep_num)}")
    log(f"  Website: https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/")
    build_log(
        f"🎙️ Release complete! "
        f"<https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/>",
        ep_num
    )
    log(f"{'='*60}")

if __name__ == "__main__":
    main()
