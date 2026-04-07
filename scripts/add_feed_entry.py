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
    [--length 31000000]

This script:
  - Validates the feed XML before and after modification
  - Inserts the new episode as the FIRST <item> in the channel (newest first)
  - Checks for duplicate episode numbers before inserting
  - Updates lastBuildDate to match the new episode's pubDate
  - Preserves all existing entries and formatting

MINIMAX: Use this script instead of hand-editing feed XML files.
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET


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
    guid = args.audio_url  # Use raw audio URL as guid (no op3 prefix)
    enclosure_url = f"https://op3.dev/e/{args.audio_url}"
    length = args.length or "31000000"

    return f"""    <!-- Episode {args.episode} -->
    <item>
      <title>{args.title}</title>
      <guid isPermaLink="false">{guid}</guid>
      <link>{args.link}</link>
      <description><![CDATA[{args.description}{show_notes_line}]]></description>
      <pubDate>{args.pub_date}</pubDate>
      <enclosure url="{enclosure_url}" length="{length}" type="audio/mpeg"/>
      <itunes:duration>{args.duration}</itunes:duration>
      <itunes:episode>{args.episode}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:image href="{args.cover_url}"/>
    </item>
"""


def main():
    parser = argparse.ArgumentParser(description="Add episode to podcast feed XML")
    parser.add_argument("feed_file", help="Path to feed XML file")
    parser.add_argument("--episode", type=int, required=True, help="Episode number")
    parser.add_argument("--title", required=True, help="Episode title")
    parser.add_argument("--description", required=True, help="Episode description")
    parser.add_argument("--pub-date", required=True, help="RFC 2822 publish date")
    parser.add_argument("--audio-url", required=True, help="Direct audio URL (no op3 prefix)")
    parser.add_argument("--cover-url", required=True, help="Cover art URL")
    parser.add_argument("--duration", required=True, help="Episode duration (MM:SS or HH:MM:SS)")
    parser.add_argument("--link", required=True, help="Episode show notes URL")
    parser.add_argument("--length", help="Audio file size in bytes (default: 31000000)")
    parser.add_argument("--dry-run", action="store_true", help="Print result without writing")

    args = parser.parse_args()

    # Read current feed
    with open(args.feed_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pre-flight: validate existing XML
    if not validate_xml(args.feed_file):
        print(f"ERROR: {args.feed_file} is already invalid XML. Fix it first.", file=sys.stderr)
        sys.exit(1)

    # Check for duplicates
    if check_duplicate(content, args.episode):
        print(f"ERROR: Episode {args.episode} already exists in {args.feed_file}", file=sys.stderr)
        sys.exit(1)

    # Build the new item block
    item_block = build_item_block(args)

    # Find the first <item> and insert before it
    first_item = re.search(r'(\n\s*)(<!-- Episode \d+|<item>|<item><title>)', content)
    if not first_item:
        print("ERROR: Could not find any existing <item> in the feed. Is this a valid podcast feed?", file=sys.stderr)
        sys.exit(1)

    insert_pos = first_item.start()
    new_content = content[:insert_pos] + "\n" + item_block + content[insert_pos:]

    # Update lastBuildDate
    new_content = re.sub(
        r'<lastBuildDate>[^<]+</lastBuildDate>',
        f'<lastBuildDate>{args.pub_date}</lastBuildDate>',
        new_content,
        count=1
    )

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
