#!/usr/bin/env python3
"""Validate podcast feed files for unresolved placeholder episode titles.

Added 2026-06-05 after EP63 leaked into all five feeds as "Episode 63: Episode 63"
(extract_episode_title silently fell back to a bare "Episode N" placeholder and
nothing downstream rejected it before commit/push).

Exit codes:
  0  all feeds clean
  2  XML parse error
  3  placeholder / duplicated title found

Usage:
  validate_feed_titles.py feed.xml translations/feed_*.xml
"""
import re
import sys
import xml.etree.ElementTree as ET

# "Episode 63", "Folge 7", "Episódio 12", "एपिसोड 5" — a number with no real subtitle.
PLACEHOLDER = re.compile(r"^(Episode|Folge|Epis[oó]dio|Episodio|एपिसोड)\s+\d+$", re.I)


def find_placeholder_titles(path):
    """Return list of offending <item> titles in *path* (empty == clean)."""
    root = ET.parse(path).getroot()
    bad = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        if ": " in title:
            prefix, sub = (p.strip() for p in title.split(": ", 1))
        else:
            prefix, sub = "", title
        # placeholder subtitle ("...: Episode 63") or prefix duplicated as subtitle
        if PLACEHOLDER.match(sub) or (prefix and prefix == sub):
            bad.append(title)
    return bad


def main(argv):
    files = argv[1:]
    if not files:
        print("usage: validate_feed_titles.py <feed.xml> [more.xml ...]", file=sys.stderr)
        return 1
    failed = False
    for path in files:
        try:
            bad = find_placeholder_titles(path)
        except ET.ParseError as e:
            print(f"🚫 {path}: invalid XML — {e}", file=sys.stderr)
            return 2
        except FileNotFoundError:
            print(f"⚠️  {path}: not found, skipping", file=sys.stderr)
            continue
        if bad:
            failed = True
            print(f"🚫 {path}: placeholder/unresolved title(s):", file=sys.stderr)
            for t in bad:
                print(f"     {t}", file=sys.stderr)
        else:
            print(f"✅ {path}: titles OK")
    if failed:
        print(
            "\nRefusing to publish: an episode title did not resolve from its show notes "
            "(the EP63 'Episode N: Episode N' bug). Fix the show notes title before publishing.",
            file=sys.stderr,
        )
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
