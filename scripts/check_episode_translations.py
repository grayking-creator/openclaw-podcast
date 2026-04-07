#!/usr/bin/env python3
"""
Episode Translation QC Gate
Validates all 4 languages have complete, correctly translated assets before publish.
Blocks feed push if any check fails.

Usage:
    python3 check_episode_translations.py 21
    python3 check_episode_translations.py 21 --fix  (show what's missing, suggest fixes)
"""
import sys
import re
import json
import argparse
from pathlib import Path

PODCAST_DIR = Path(__file__).resolve().parent.parent
CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
WEBSITE_DIR = Path.home() / ".openclaw/workspace/websiteBuilder/frontend/public/images/podcast"
LANGS = ["es", "de", "pt", "hi"]
LANG_NAMES = {"es": "Spanish", "de": "German", "pt": "Portuguese", "hi": "Hindi"}
TITLE_PREFIXES = {"es": "Episodio", "de": "Folge", "pt": "Episódio", "hi": "एपिसोड"}

errors = []
warnings = []
passes = []

def ok(msg):
    passes.append(f"  ✅ {msg}")

def err(msg, hint=""):
    full = f"  ❌ {msg}"
    if hint:
        full += f"\n     → {hint}"
    errors.append(full)

def warn(msg):
    warnings.append(f"  ⚠️  {msg}")

def get_en_title(ep_num):
    """Extract EN episode title from feed.xml."""
    feed = PODCAST_DIR / "feed.xml"
    if not feed.exists():
        return None
    text = feed.read_text()
    m = re.search(rf'<title>Episode\s+{ep_num}\s*[:\-–]\s*(.+?)</title>', text)
    return m.group(1).strip() if m else None

def get_feed_title(ep_num, lang):
    """Extract translated title from language feed."""
    feed = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
    if not feed.exists():
        return None
    text = feed.read_text()
    prefix = TITLE_PREFIXES.get(lang, "Episode")
    m = re.search(rf'<title>{prefix}\s+{ep_num}\s*[:\-–]\s*(.+?)</title>', text)
    return m.group(1).strip() if m else None

def check_lang(ep_num, lang, en_title):
    ep_str = f"{ep_num:03d}"
    lang_name = LANG_NAMES[lang]
    prefix = f"[{lang.upper()}]"

    # 1. Feed entry exists
    feed = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
    if not feed.exists():
        err(f"{prefix} Feed file missing: feed_{lang}.xml")
        return
    feed_text = feed.read_text()
    ep_pattern = rf'{TITLE_PREFIXES[lang]}\s+{ep_num}'
    if not re.search(ep_pattern, feed_text):
        err(f"{prefix} No EP{ep_num} entry in feed_{lang}.xml",
            f"Expected title starting with '{TITLE_PREFIXES[lang]} {ep_num}:'")
        return
    ok(f"{prefix} Feed entry exists")

    # 2. Title is translated (not same as EN)
    translated_title = get_feed_title(ep_num, lang)
    if translated_title and en_title:
        if translated_title.lower() == en_title.lower():
            err(f"{prefix} Title NOT translated — still English: '{translated_title}'",
                f"Translate '{en_title}' to {lang_name}")
        else:
            ok(f"{prefix} Title translated: '{translated_title}'")
    elif not translated_title:
        warn(f"{prefix} Could not parse title from feed")

    # 3. Show notes exist
    show_notes = PODCAST_DIR / "translations" / lang / f"show_notes_episode_{ep_str}_{lang}.md"
    if show_notes.exists():
        ok(f"{prefix} Show notes exist")
    else:
        err(f"{prefix} Show notes missing: translations/{lang}/show_notes_episode_{ep_str}_{lang}.md")

    # 4. Transcript exists (audio can't exist without a transcript — check all known locations)
    transcript_candidates = [
        PODCAST_DIR / "translations" / lang / f"episode_{ep_str}_{lang}.md",
        PODCAST_DIR / "translations" / lang / f"episode_{ep_str}_{lang}_nova.md",
        PODCAST_DIR / "episodes" / f"episode_{ep_str}_{lang}.md",
        PODCAST_DIR / "episodes" / f"episode_{ep_str}_{lang}_nova.md",
        PODCAST_DIR / "content_staging" / "translations" / f"episode_{ep_str}_{lang}.md",
        PODCAST_DIR / "content_staging" / "translations" / f"episode_{ep_str}_{lang}_nova.md",
    ]
    if any(t.exists() for t in transcript_candidates):
        ok(f"{prefix} Transcript exists")
    else:
        err(f"{prefix} Transcript missing — checked: translations/{lang}/episode_{ep_str}_{lang}.md")

    # 5. Audio exists (CDN or podcast dir)
    audio_candidates = [
        CDN_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3",
        CDN_DIR / "translations" / lang / f"episode_{ep_str}_{lang}.mp3",
        PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3",
    ]
    if any(a.exists() for a in audio_candidates):
        ok(f"{prefix} Audio exists")
    else:
        err(f"{prefix} Audio missing — no episode_{ep_str}_{lang}.mp3 found in CDN or podcast dirs")

    # 6. Cover art exists with translated text
    cover_candidates = [
        PODCAST_DIR / "images" / f"episode_{ep_str}_cover_{lang}.png",
        CDN_DIR / f"episode_{ep_str}_cover_{lang}.png",
    ]
    if any(c.exists() for c in cover_candidates):
        ok(f"{prefix} Cover art exists")
    else:
        err(f"{prefix} Cover art missing: images/episode_{ep_str}_cover_{lang}.png")

    # 7. Cover in website dir
    website_cover = WEBSITE_DIR / f"episode_{ep_str}_cover_{lang}.png"
    if website_cover.exists():
        ok(f"{prefix} Cover in website dir")
    else:
        warn(f"{prefix} Cover missing from website: {website_cover.name}")

    # 8. Description translated (check it's not identical to EN)
    en_feed = PODCAST_DIR / "feed.xml"
    if en_feed.exists():
        en_text = en_feed.read_text()
        en_desc_match = re.search(rf'Episode\s+{ep_num}.*?<description><!\[CDATA\[(.+?)\]\]></description>', en_text, re.DOTALL)
        lang_desc_match = re.search(rf'{TITLE_PREFIXES[lang]}\s+{ep_num}.*?<description><!\[CDATA\[(.+?)\]\]></description>', feed_text, re.DOTALL)
        if en_desc_match and lang_desc_match:
            en_desc = en_desc_match.group(1)[:100]
            lang_desc = lang_desc_match.group(1)[:100]
            if en_desc == lang_desc:
                err(f"{prefix} Description NOT translated — identical to EN",
                    f"First 100 chars match: '{en_desc[:50]}...'")
            else:
                ok(f"{prefix} Description translated")

def main():
    parser = argparse.ArgumentParser(description="Episode Translation QC Gate")
    parser.add_argument("episode", type=int, help="Episode number to check")
    parser.add_argument("--fix", action="store_true", help="Show fix suggestions")
    args = parser.parse_args()

    ep_num = args.episode
    en_title = get_en_title(ep_num)

    print(f"\n🔍 Translation QC — Episode {ep_num}")
    print(f"   EN title: {en_title or '(not found)'}")
    print(f"   Languages: {', '.join(LANGS)}")
    print()

    for lang in LANGS:
        check_lang(ep_num, lang, en_title)

    # Also check EN cover in website
    ep_str = f"{ep_num:03d}"
    en_website_cover = WEBSITE_DIR / f"episode_{ep_str}_cover.png"
    if en_website_cover.exists():
        ok("[EN] Cover in website dir")
    else:
        err("[EN] Cover missing from website dir",
            f"cp images/episode_{ep_str}_cover.png → websiteBuilder/.../podcast/")

    print("── Results ──")
    for p in passes:
        print(p)
    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    print()
    if errors:
        print(f"❌ {len(errors)} ERROR(s) — DO NOT PUBLISH until fixed")
        return 1
    elif warnings:
        print(f"⚠️  {len(warnings)} warning(s) but no blockers — OK to publish")
        return 0
    else:
        print("✅ All translation checks passed")
        return 0

if __name__ == "__main__":
    sys.exit(main())
