#!/usr/bin/env python3
"""
OpenClaw Daily — Episode Release Pipeline
From: approved EN audio (audio/episode_XXX_en.mp3) + EN thumbnail (images/episode_XXX_cover.png)
To:   all 5 channels uploaded, feeds updated, CDN synced, website deployed.

Uses Minimax M2.7 API for all translations.

Usage:
  /opt/homebrew/bin/python3.14 scripts/release_episode.py 25
  /opt/homebrew/bin/python3.14 scripts/release_episode.py 25 --from-phase tts
  /opt/homebrew/bin/python3.14 scripts/release_episode.py 25 --pub-date "Mon, 07 Apr 2026 18:00:00 +0000"
"""

import os, sys, json, re, shutil, subprocess, asyncio, math, argparse, time
from pathlib import Path

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

ALL_PHASES = ["setup", "translate", "tts", "covers", "feeds", "qc", "youtube", "cdn", "publish"]

# ── Helpers ──────────────────────────────────────────────────────────────────

def log(msg, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{msg}", flush=True)

def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
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

# ── Minimax translation ───────────────────────────────────────────────────────

def minimax_call(prompt, max_tokens=4000, retries=3):
    """Call Minimax M2.7, strip <think> blocks, return clean text. Retries on empty output."""
    import openai
    key = load_env_key("MINIMAX_API_KEY")
    client = openai.OpenAI(base_url="https://api.minimaxi.chat/v1", api_key=key)
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
    title_m = re.search(r"^## Episode Title\s*\n\*\*(.+?)\*\*", notes, re.MULTILINE)
    tag_m   = re.search(r"^## Tagline\s*\n(.+?)(?=\n\n|\n##)", notes, re.MULTILINE | re.DOTALL)
    # Description: intro paragraph from Show Notes block
    block_m = re.search(r"```md\s*\n.*?\n\n(.+?)(?=\n\n##)", notes, re.DOTALL)

    en_title    = title_m.group(1).strip() if title_m else f"Episode {ep_num}"
    en_tagline  = tag_m.group(1).strip()   if tag_m  else ""
    en_desc     = block_m.group(1).strip() if block_m else en_tagline

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

    raw = minimax_call(prompt, max_tokens=4000)
    # Extract JSON from response
    json_m = re.search(r'\{[\s\S]*\}', raw)
    if not json_m:
        raise ValueError(f"No JSON in metadata translation for {lang}: {raw[:200]}")
    return json.loads(json_m.group(0))

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

    # Split into chunks of ~60 paragraphs
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    chunk_size = 60
    chunks = [paragraphs[i:i+chunk_size] for i in range(0, len(paragraphs), chunk_size)]

    translated_chunks = []
    for i, chunk in enumerate(chunks):
        chunk_text = "\n\n".join(chunk)
        prompt = f"{system_note}\n\nTranslate the following:\n\n{chunk_text}"
        log(f"    Translating chunk {i+1}/{len(chunks)} ({len(chunk)} paragraphs)...", indent=2)
        result = minimax_call(prompt, max_tokens=10000)
        translated_chunks.append(result)
        if i < len(chunks) - 1:
            time.sleep(1)  # polite pause between chunks

    return "\n\n".join(translated_chunks)

# ── Cover generation ──────────────────────────────────────────────────────────

def generate_translated_cover(ep_num, lang, meta):
    """Render a translated cover image for the episode using same visual as EN."""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    import random

    W, H = 1400, 1400
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

    # Background gradient
    for y in range(H):
        t = y / (H - 1)
        r = int(BLACK[0] + 6 * t)
        g = int(BLACK[1] + 12 * t)
        b = int(BLACK[2] + 20 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b, 255))

    def blur_overlay(draw_fn, blur=18):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        draw_fn(ld)
        return layer.filter(ImageFilter.GaussianBlur(blur))

    # Strata lines (geological cross-section)
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
    d = ImageDraw.Draw(img)

    # Depth markers
    markers = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    mkd = ImageDraw.Draw(markers)
    for y in range(80, 900, 60):
        tick_len = 25 if y % 180 == 0 else 12
        mkd.line([(40, y), (40+tick_len, y)], fill=STEEL_LIGHT+(50,), width=1)
        mkd.line([(W-40, y), (W-40-tick_len, y)], fill=STEEL_LIGHT+(50,), width=1)
    mkd.line([(40, 80), (40, 880)], fill=STEEL_LIGHT+(35,), width=1)
    mkd.line([(W-40, 80), (W-40, 880)], fill=STEEL_LIGHT+(35,), width=1)
    img = Image.alpha_composite(img, markers)

    # Ambient glow
    for center, color in [((700, 400), BLUE), ((700, 600), AMBER), ((700, 300), TEAL)]:
        g = blur_overlay(
            lambda ld, c=center, col=color: ld.ellipse(
                [(c[0]-500, c[1]-200), (c[0]+500, c[1]+200)], fill=col+(7,)), blur=110)
        img = Image.alpha_composite(img, g)

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
        font_title = ImageFont.truetype(title_font_path, 100 if is_hindi else 118)
        font_sub   = ImageFont.truetype(font_path_reg, 28 if is_hindi else 30)
    except Exception:
        font_show = font_ep = font_title = font_sub = ImageFont.load_default()

    md = ImageDraw.Draw(img)

    SHOW_TEXT = "OPENCLAW DAILY"
    EP_TEXT   = f"EP{ep_num:03d}"
    line1     = meta.get("cover_line1", "").upper()
    line2     = meta.get("cover_line2", "").upper()
    tagline   = meta.get("cover_tagline", "")

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
    l1w = md.textlength(line1, font=font_title)
    md.text(((W-l1w)/2+3, 988), line1, font=font_title, fill=(0, 0, 0, 160))
    tg1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tg1).text(((W-l1w)/2, 985), line1, font=font_title, fill=TEAL+(50,))
    img = Image.alpha_composite(img, tg1.filter(ImageFilter.GaussianBlur(14)))
    md = ImageDraw.Draw(img)
    md.text(((W-l1w)/2, 985), line1, font=font_title, fill=WHITE+(255,))

    # Line 2 — amber glow
    l2w = md.textlength(line2, font=font_title)
    md.text(((W-l2w)/2+4, 1118), line2, font=font_title, fill=(0, 0, 0, 170))
    tg2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tg2).text(((W-l2w)/2, 1115), line2, font=font_title, fill=AMBER+(80,))
    img = Image.alpha_composite(img, tg2.filter(ImageFilter.GaussianBlur(16)))
    md = ImageDraw.Draw(img)
    md.text(((W-l2w)/2, 1115), line2, font=font_title, fill=AMBER_BRIGHT+(255,))

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

# ── Phase implementations ─────────────────────────────────────────────────────

def phase_setup(ep_num, state):
    log("[ SETUP ] Checking prerequisites...")
    ep_str = f"{ep_num:03d}"

    # Check EN audio
    en_audio_src = PODCAST_DIR / "audio" / f"episode_{ep_str}_en.mp3"
    en_audio_dst = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    if not en_audio_src.exists():
        raise FileNotFoundError(f"Missing approved EN audio: {en_audio_src}")

    # Canonicalize: episode_025_en.mp3 → episode_025.mp3
    if not en_audio_dst.exists():
        shutil.copy2(str(en_audio_src), str(en_audio_dst))
        log(f"  ✅ Canonicalized audio: episode_{ep_str}.mp3")
    else:
        log(f"  ✅ Canonical audio exists: episode_{ep_str}.mp3")

    # Check EN cover
    en_cover = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    if not en_cover.exists():
        raise FileNotFoundError(f"Missing EN cover: {en_cover}")
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
        if lang in translations and translations[lang].get("done"):
            log(f"  ⏭  {lang.upper()} already translated, skipping")
            continue

        log(f"  → {lang.upper()} ({LANG_NAMES[lang]})...")
        lang_dir = PODCAST_DIR / "translations" / lang
        lang_dir.mkdir(parents=True, exist_ok=True)

        # 1. Metadata
        log(f"     Metadata...", indent=1)
        meta = translate_metadata(ep_num, lang)
        translations.setdefault(lang, {})
        translations[lang]["meta"] = meta
        log(f"     Title: {meta.get('title', '?')}", indent=1)

        # 2. Transcript
        log(f"     Transcript...", indent=1)
        translated_transcript = translate_text_chunked(transcript_text, lang, "transcript")
        transcript_out = lang_dir / f"episode_{ep_str}_{lang}.md"
        transcript_out.write_text(translated_transcript)
        log(f"     ✅ Saved: {transcript_out.name}", indent=1)

        # 3. Show notes
        log(f"     Show notes...", indent=1)
        translated_notes = translate_text_chunked(show_notes_block, lang, "show_notes")
        notes_out = lang_dir / f"show_notes_episode_{ep_str}_{lang}.md"
        notes_out.write_text(translated_notes)
        log(f"     ✅ Saved: {notes_out.name}", indent=1)

        translations[lang]["done"] = True
        state["translations"] = translations

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
                raise ValueError(f"No translation metadata for {lang} — run translate phase first")
            log(f"  → Generating {lang.upper()} cover...")
            generate_translated_cover(ep_num, lang, meta)
            log(f"  ✅ {out_path.name}")

        # Copy to website
        web_cover = WEBSITE_PODCAST_IMG / f"episode_{ep_str}_cover_{lang}.png"
        if not web_cover.exists():
            shutil.copy2(str(out_path), str(web_cover))
            log(f"     → {web_cover.name} copied to website")

        # Copy to CDN
        cdn_cover = CDN_DIR / f"episode_{ep_str}_cover_{lang}.png"
        if not cdn_cover.exists():
            shutil.copy2(str(out_path), str(cdn_cover))
            log(f"     → {cdn_cover.name} copied to CDN")

    return state

def phase_feeds(ep_num, state, pub_date):
    log("[ FEEDS ] Adding feed entries...")
    ep_str = f"{ep_num:03d}"
    translations = state.get("translations", {})
    duration = state.get("audio_duration", "33:00")

    add_feed_script = str(SCRIPTS_DIR / "add_feed_entry.py")

    # EN feed
    en_audio_url = f"{CDN_BASE}/audio/episode_{ep_str}.mp3"
    en_cover_url = f"{CDN_BASE}/episode_{ep_str}_cover.png"
    en_link = f"https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"

    # Extract EN title from show notes
    notes = (PODCAST_DIR / f"show_notes_episode_{ep_str}.md").read_text()
    title_m = re.search(r"^## Episode Title\s*\n\*\*(.+?)\*\*", notes, re.MULTILINE)
    en_episode_title = title_m.group(1).strip() if title_m else f"Episode {ep_num}"
    en_title = f"Episode {ep_num}: {en_episode_title}"

    # Extract EN description from show notes block
    block_m = re.search(r"```md\s*\n.*?\n\n(.+?)(?=\n\n##)", notes, re.DOTALL)
    en_desc = block_m.group(1).strip() if block_m else en_episode_title
    en_desc += f"\n\nShow notes: {en_link}"

    en_size = state.get("audio_size", 30000000)

    en_feed = PODCAST_DIR / "feed.xml"
    # Check if already in feed
    if f"<itunes:episode>{ep_num}</itunes:episode>" not in en_feed.read_text():
        log(f"  → Adding EN feed entry...")
        run([
            sys.executable, add_feed_script,
            str(en_feed),
            "--episode", str(ep_num),
            "--title", en_title,
            "--description", en_desc,
            "--pub-date", pub_date,
            "--audio-url", en_audio_url,
            "--cover-url", en_cover_url,
            "--duration", duration,
            "--link", en_link,
            "--length", str(en_size),
        ])
        log(f"  ✅ EN feed updated")
    else:
        log(f"  ⏭  EN feed already has EP{ep_num}")

    # Translated feeds
    for lang in LANGS:
        feed_path = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
        feed_text = feed_path.read_text()
        prefix = TITLE_PREFIXES[lang]

        if f"<itunes:episode>{ep_num}</itunes:episode>" in feed_text:
            log(f"  ⏭  {lang.upper()} feed already has EP{ep_num}")
            continue

        meta = translations.get(lang, {}).get("meta", {})
        lang_title = meta.get("title", f"{prefix} {ep_num}: {en_episode_title}")
        lang_desc_base = meta.get("description", en_desc)
        lang_link = LANG_LINKS[lang].format(ep=ep_num)
        lang_cta = SHOW_NOTES_CTA.get(lang, "Show notes:")
        lang_desc = f"{lang_desc_base}\n\n{lang_cta} {lang_link}"

        lang_audio_url = f"{CDN_BASE}/audio/episode_{ep_str}_{lang}.mp3"
        lang_cover_url = f"{CDN_BASE}/episode_{ep_str}_cover_{lang}.png"

        # Get translated audio size
        lang_audio = PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"
        lang_size = lang_audio.stat().st_size if lang_audio.exists() else en_size

        # For translated feed, duration comes from translated audio
        lang_duration = duration
        if lang_audio.exists():
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
            "--description", lang_desc,
            "--pub-date", pub_date,
            "--audio-url", lang_audio_url,
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
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "youtube_scheduled_upload.py"), str(ep_num)],
        cwd=str(PODCAST_DIR)
    )
    if result.returncode != 0:
        raise RuntimeError("YouTube upload failed")
    return state

def phase_cdn(ep_num, state):
    log("[ CDN ] Syncing audio to CDN repo and pushing...")
    ep_str = f"{ep_num:03d}"

    # Copy EN audio to CDN audio dir
    en_src = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    en_dst = CDN_DIR / "audio" / f"episode_{ep_str}.mp3"
    if not en_dst.exists():
        shutil.copy2(str(en_src), str(en_dst))
        log(f"  ✅ EN audio → CDN/audio/")

    # Copy latest.mp3
    latest_dst = CDN_DIR / "audio" / "latest.mp3"
    shutil.copy2(str(en_src), str(latest_dst))
    log(f"  ✅ latest.mp3 updated")

    # Copy translated audio
    cdn_trans_base = CDN_DIR / "translations"
    for lang in LANGS:
        lang_src = PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"
        # Primary: CDN/audio/episode_025_es.mp3 (checked by upload script)
        lang_dst_audio = CDN_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"
        if lang_src.exists() and not lang_dst_audio.exists():
            shutil.copy2(str(lang_src), str(lang_dst_audio))
            log(f"  ✅ {lang.upper()} audio → CDN/audio/")

        # Also put in CDN/translations/{lang}/
        trans_dir = cdn_trans_base / lang
        trans_dir.mkdir(parents=True, exist_ok=True)
        lang_dst_trans = trans_dir / f"episode_{ep_str}_{lang}.mp3"
        if lang_src.exists() and not lang_dst_trans.exists():
            shutil.copy2(str(lang_src), str(lang_dst_trans))

    # Git commit + push CDN repo
    log(f"  Pushing CDN repo...")
    files_to_add = [
        f"audio/episode_{ep_str}.mp3",
        f"audio/latest.mp3",
        f"episode_{ep_str}_cover.png",
    ]
    for lang in LANGS:
        files_to_add += [
            f"audio/episode_{ep_str}_{lang}.mp3",
            f"episode_{ep_str}_cover_{lang}.png",
        ]
    # Only add files that exist
    existing = [f for f in files_to_add if (CDN_DIR / f).exists()]
    run(["git", "add", "--"] + existing, cwd=str(CDN_DIR))
    result = run(["git", "diff", "--cached", "--quiet"], cwd=str(CDN_DIR), check=False)
    if result.returncode != 0:
        run(["git", "commit", "-m", f"EP{ep_num}: audio + covers"], cwd=str(CDN_DIR))
        run(["git", "push"], cwd=str(CDN_DIR))
        log(f"  ✅ CDN repo pushed")
    else:
        log(f"  ℹ️  CDN repo already up to date")

    return state

def phase_publish(ep_num, state):
    log("[ PUBLISH ] Pushing podcast repo + website...")
    ep_str = f"{ep_num:03d}"

    # Stage podcast repo files
    stage = [
        f"feed.xml",
        f"images/episode_{ep_str}_cover.png",
        f"show_notes_episode_{ep_str}.md",
        f"episodes/episode_{ep_str}_transcript.md",
        f"episodes/episode_{ep_str}_transcript_nova.md",
        f"translations/feed_de.xml",
        f"translations/feed_es.xml",
        f"translations/feed_hi.xml",
        f"translations/feed_pt.xml",
    ]
    for lang in LANGS:
        stage += [
            f"images/episode_{ep_str}_cover_{lang}.png",
            f"translations/{lang}/episode_{ep_str}_{lang}.md",
            f"translations/{lang}/show_notes_episode_{ep_str}_{lang}.md",
        ]

    existing = [f for f in stage if (PODCAST_DIR / f).exists()]
    run(["git", "add", "--"] + existing, cwd=str(PODCAST_DIR))
    result = run(["git", "diff", "--cached", "--quiet"], cwd=str(PODCAST_DIR), check=False)
    if result.returncode != 0:
        env = {**os.environ, "FEED_APPROVED": "1"}
        result2 = subprocess.run(
            ["git", "commit", "-m", f"EP{ep_num}: publish episode_{ep_str}"],
            cwd=str(PODCAST_DIR), env=env, capture_output=True, text=True
        )
        if result2.returncode != 0:
            raise RuntimeError(f"git commit failed:\n{result2.stderr}")
        run(["git", "push"], cwd=str(PODCAST_DIR))
        log(f"  ✅ Podcast repo pushed")
    else:
        log(f"  ℹ️  Podcast repo already up to date")

    # Update website
    log(f"  Building website...")
    ws_script = WORKSPACE_DIR / "scripts/update_website_training_data.py"
    if ws_script.exists():
        subprocess.run([sys.executable, str(ws_script), "--skip-sync"],
                       capture_output=True, cwd=str(WORKSPACE_DIR))

    # Push website
    result = run(["git", "status", "--porcelain"], cwd=str(WEBSITE_DIR))
    if result.stdout.strip():
        run(["git", "add", "-A"], cwd=str(WEBSITE_DIR))
        result2 = run(["git", "diff", "--cached", "--quiet"], cwd=str(WEBSITE_DIR), check=False)
        if result2.returncode != 0:
            run(["git", "commit", "-m", f"EP{ep_num}: cover art + website update"], cwd=str(WEBSITE_DIR))
            run(["git", "push"], cwd=str(WEBSITE_DIR))
            log(f"  ✅ Website pushed")
        else:
            log(f"  ℹ️  Website already up to date")
    else:
        log(f"  ℹ️  Website no changes")

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
    "setup":     phase_setup,
    "translate": phase_translate,
    "tts":       phase_tts,
    "covers":    phase_covers,
    "feeds":     None,   # needs pub_date arg
    "qc":        phase_qc,
    "youtube":   phase_youtube,
    "cdn":       phase_cdn,
    "publish":   phase_publish,
}

def main():
    parser = argparse.ArgumentParser(description="OpenClaw episode release pipeline")
    parser.add_argument("episode", type=int, help="Episode number (e.g. 25)")
    parser.add_argument("--from-phase", help=f"Start from phase: {', '.join(ALL_PHASES)}")
    parser.add_argument("--only-phase", help="Run only this phase")
    parser.add_argument("--pub-date",
                        default=f"Mon, 07 Apr 2026 18:00:00 +0000",
                        help="RSS pubDate string")
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
        phases_to_run = [args.only_phase]
    elif args.from_phase:
        idx = ALL_PHASES.index(args.from_phase)
        phases_to_run = ALL_PHASES[idx:]
    else:
        phases_to_run = ALL_PHASES

    log(f"\n{'='*60}")
    log(f"OpenClaw Daily — EP{ep_num:03d} Release Pipeline")
    log(f"Phases: {', '.join(phases_to_run)}")
    log(f"{'='*60}\n")

    for phase in phases_to_run:
        if phase in completed and phase != "qc":
            log(f"[ {phase.upper()} ] Already completed, skipping")
            continue

        log(f"\n{'-'*60}")
        try:
            if phase == "feeds":
                state = phase_feeds(ep_num, state, args.pub_date)
            else:
                state = PHASE_FNS[phase](ep_num, state)

            completed.add(phase)
            state["completed_phases"] = list(completed)
            save_state(ep_num, state)
            log(f"[ {phase.upper()} ] ✅ Complete")

        except Exception as e:
            log(f"[ {phase.upper()} ] ❌ FAILED: {e}")
            save_state(ep_num, state)
            sys.exit(1)

    log(f"\n{'='*60}")
    log(f"✅ EP{ep_num:03d} release complete!")
    ep_str = f"{ep_num:03d}"
    log(f"  Feed: https://clawdassistant85-netizen.github.io/openclaw-podcast/feed.xml")
    log(f"  Audio: {CDN_BASE}/audio/episode_{ep_str}.mp3")
    log(f"  Website: https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/")
    log(f"{'='*60}")

if __name__ == "__main__":
    main()
