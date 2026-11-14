#!/usr/bin/env python3
"""
Add an episode entry to a podcast feed XML file.

Usage:
  python3 scripts/add_feed_entry.py <feed_file> \\
    --episode 24 \\
    --title "Episode 24: The Narrative Layer" \\
    --description "Six stories about who controls the AI stack." \\
    --pub-date "Sun, 05 Apr 2026 14:00:00 +0000" \\
    --audio-url "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/audio/episode_024.mp3" \\
    --cover-url "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/episode_024_cover.png" \\
    --duration "38:00" \\
    --link "https://tobyonfitnesstech.com/podcasts/episode-24/" \\
    --length 31682185

This script:
  - Validates the feed XML before and after modification
  - Inserts the new episode in descending publication-date order
  - Checks for duplicate episode numbers before inserting
  - Updates lastBuildDate without regressing it during historical recovery
  - Preserves all existing entries and formatting

MINIMAX: Use this script instead of hand-editing feed XML files.
"""

from email.utils import parsedate_to_datetime

import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET

from podcast_description import prepare_episode_summary


def validate_xml(path):
    """Parse XML and return True if valid, False otherwise."""
    try:
        ET.parse(path)
        return True
    except ET.ParseError as e:
        print(f"  XML INVALID: {e}", file=sys.stderr)
        return False


def check_duplicate(content, episode_number):
    """Check if this episode number already exists in the feed."""
    pattern = rf'<itunes:episode>{episode_number}</itunes:episode>'
    return bool(re.search(pattern, content))


def build_item_block(args):
    """Build the XML <item> block for the new episode."""
    show_notes_line = f"\n\nShow notes: {args.link}" if args.link else ""
    description = prepare_episode_summary(args.description, fallback=args.title)
    guid = args.guid or args.audio_url  # Keep guid stable when enclosure host changes
    enclosure_url = f"https://op3.dev/e/{args.audio_url}"
    length = args.length

    title_xml = html.escape(args.title)
    episode_type = getattr(args, 'episode_type', 'full')
    episode_line = f'<itunes:episode>{args.episode}</itunes:episode>' if args.episode is not None else ''
    label = f'Episode {args.episode}' if args.episode is not None else 'Bonus episode'
    return f"""    <!-- {label} -->
    <item>
      <title>{title_xml}</title>
      <guid isPermaLink="false">{guid}</guid>
      <link>{args.link}</link>
      <description><![CDATA[{description}{show_notes_line}]]></description>
      <pubDate>{args.pub_date}</pubDate>
      <enclosure url="{enclosure_url}" length="{length}" type="audio/mpeg"/>
      <itunes:duration>{args.duration}</itunes:duration>
      {episode_line}
      <itunes:episodeType>{episode_type}</itunes:episodeType>
      <itunes:image href="{args.cover_url}"/>
    </item>
"""


def main():
    parser = argparse.ArgumentParser(description="Add episode to podcast feed XML")
    parser.add_argument("feed_file", help="Path to feed XML file")
    parser.add_argument("--episode", type=int, help="Episode number; omit only for a bonus with explicit GUID")
    parser.add_argument("--episode-type", choices=['full', 'bonus'], default='full')
    parser.add_argument("--title", required=True, help="Episode title")
    parser.add_argument("--description", required=True, help="Episode description")
    parser.add_argument("--pub-date", required=True, help="RFC 2822 publish date")
    parser.add_argument("--audio-url", required=True, help="Direct audio URL (no op3 prefix)")
    parser.add_argument("--guid", help="Optional stable guid URL (no op3 prefix)")
    parser.add_argument("--cover-url", required=True, help="Cover art URL")
    parser.add_argument("--duration", required=True, help="Episode duration (MM:SS or HH:MM:SS)")
    parser.add_argument("--link", required=True, help="Episode show notes URL")
    parser.add_argument("--length", required=True, help="Audio file size in bytes")
    parser.add_argument("--dry-run", action="store_true", help="Print result without writing")

    args = parser.parse_args()
    if args.episode is None and (args.episode_type != 'bonus' or not args.guid):
        parser.error('Unnumbered entries require --episode-type bonus and a stable --guid')

    # Read current feed
    with open(args.feed_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if args.guid and any(x.text == args.guid for x in ET.fromstring(content).findall('./channel/item/guid')):
        parser.error('This GUID already exists in the feed')

    # Pre-flight: validate existing XML
    if not validate_xml(args.feed_file):
        print(f"ERROR: {args.feed_file} is already invalid XML. Fix it first.", file=sys.stderr)
        sys.exit(1)

    # Check for duplicates
    if args.episode is not None and check_duplicate(content, args.episode):
        print(f"ERROR: Episode {args.episode} already exists in {args.feed_file}", file=sys.stderr)
        sys.exit(1)

    # Build the new item block
    item_block = build_item_block(args)

    # Keep historical recovery entries in descending publication order.
    new_date = parsedate_to_datetime(args.pub_date)
    blocks = list(re.finditer(r'(?:[ \t]*<!-- (?:Episode \d+|Bonus episode) -->\s*)?<item\b[^>]*>.*?</item>', content, re.S))
    if not blocks:
        raise SystemExit("ERROR: Could not find existing feed entries")
    insert_pos = blocks[-1].end()
    for block in blocks:
        old_date = re.search(r'<pubDate>(.*?)</pubDate>', block.group(), re.S)
        if old_date and new_date >= parsedate_to_datetime(old_date.group(1)):
            insert_pos = block.start()
            break
    new_content = content[:insert_pos] + "\n" + item_block + content[insert_pos:]
    # A backfill must never regress the feed's build timestamp.
    old_build = re.search(r'<lastBuildDate>(.*?)</lastBuildDate>', content)
    build_date = args.pub_date
    if old_build and parsedate_to_datetime(old_build.group(1)) > new_date:
        build_date = old_build.group(1)
    new_content = re.sub(r'<lastBuildDate>[^<]+</lastBuildDate>',
                         f'<lastBuildDate>{build_date}</lastBuildDate>',
                         new_content, count=1)

    if args.dry_run:
        print(new_content)
        return

    # Write the updated feed
    with open(args.feed_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Post-flight: validate the result
    if not validate_xml(args.feed_file):
        # Restore original
        with open(args.feed_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"ERROR: Insertion produced invalid XML. Original restored. Check your inputs.", file=sys.stderr)
        sys.exit(1)

    print(f"OK: Episode {args.episode} added to {args.feed_file}")


if __name__ == "__main__":
    main()
