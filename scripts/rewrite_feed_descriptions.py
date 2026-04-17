#!/usr/bin/env python3
"""
Rewrite existing EN feed descriptions from show-notes metadata.

Usage:
  python3 scripts/rewrite_feed_descriptions.py --episodes 29 30 31 32
"""

import argparse
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_PATH = ROOT / "feed.xml"


def collapse_ws(text):
    return re.sub(r"\s+", " ", text).strip()


def extract_section(notes, heading):
    pattern = rf"^## {re.escape(heading)}\s*\n(.+?)(?=\n## |\Z)"
    match = re.search(pattern, notes, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_feed_description(notes):
    feed_desc = collapse_ws(extract_section(notes, "Feed Description"))
    if feed_desc:
        return feed_desc

    tagline = collapse_ws(extract_section(notes, "Tagline"))
    if tagline:
        return tagline

    intro = re.search(r"```md\s*\n.*?\n\n(.+?)(?=\n\n\[|\n```)", notes, re.DOTALL)
    if intro:
        return collapse_ws(intro.group(1))

    return ""


def replace_item_description(content, episode, description):
    token = f"<itunes:episode>{episode}</itunes:episode>"
    mid = content.find(token)
    if mid == -1:
        raise ValueError(f"Episode {episode} not found in {FEED_PATH}")

    start = content.rfind("<item", 0, mid)
    end = content.find("</item>", mid)
    if start == -1 or end == -1:
        raise ValueError(f"Could not isolate item block for episode {episode}")

    item = content[start:end + len("</item>")]
    replacement = f"<description><![CDATA[{description}]]></description>"
    new_item, count = re.subn(
        r"<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>",
        replacement,
        item,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise ValueError(f"Could not replace description for episode {episode}")
    return content[:start] + new_item + content[end + len("</item>"):]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", nargs="+", type=int, required=True)
    args = parser.parse_args()

    content = FEED_PATH.read_text()
    for ep in args.episodes:
        notes_path = ROOT / f"show_notes_episode_{ep:03d}.md"
        if not notes_path.exists():
            raise FileNotFoundError(notes_path)
        notes = notes_path.read_text()
        desc = extract_feed_description(notes) or f"Episode {ep}"
        desc = f"{desc}\n\nShow notes: https://tobyonfitnesstech.com/podcasts/episode-{ep}/"
        content = replace_item_description(content, ep, desc)

    last_build = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    content = re.sub(
        r"<lastBuildDate>[^<]+</lastBuildDate>",
        f"<lastBuildDate>{last_build}</lastBuildDate>",
        content,
        count=1,
    )

    ET.fromstring(content)
    FEED_PATH.write_text(content)
    print(f"Updated {FEED_PATH} for episodes: {', '.join(str(ep) for ep in args.episodes)}")


if __name__ == "__main__":
    main()
