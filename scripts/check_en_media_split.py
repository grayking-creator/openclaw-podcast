#!/usr/bin/env python3
"""Validate EN feed audio hosts after splitting archive/current media repos."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


WORKSPACE = Path.home() / ".openclaw" / "workspace"
PODCAST_DIR = WORKSPACE / "openclaw-podcast"
MEDIA_EN_DIR = WORKSPACE / "openclaw-podcast-media-en"
AUDIO_DIR = WORKSPACE / "openclaw-podcast-audio"

OP3_PREFIX = "https://op3.dev/e/"
ARCHIVE_MAX_EPISODE = 32
MEDIA_EN_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-media-en/"
AUDIO_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/"
ITUNES_NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}


def unwrap_op3(url: str) -> str:
    return url[len(OP3_PREFIX) :] if url.startswith(OP3_PREFIX) else url


def expected_for_episode(episode: int) -> tuple[str, Path]:
    ep = f"{episode:03d}"
    rel = f"audio/episode_{ep}.mp3"
    if episode <= ARCHIVE_MAX_EPISODE:
        return f"{MEDIA_EN_BASE}{rel}", MEDIA_EN_DIR / rel
    return f"{AUDIO_BASE}{rel}", AUDIO_DIR / rel


def main() -> int:
    feed_path = PODCAST_DIR / "feed.xml"
    root = ET.parse(feed_path).getroot()
    channel = root.find("channel")
    if channel is None:
        print(f"ERROR: {feed_path} has no channel element")
        return 1

    errors: list[str] = []
    checked = 0
    for item in channel.findall("item"):
        episode_text = item.findtext("itunes:episode", namespaces=ITUNES_NS)
        if not episode_text:
            continue
        episode = int(episode_text)
        enclosure = item.find("enclosure")
        if enclosure is None:
            errors.append(f"EP{episode:03d}: missing enclosure")
            continue

        actual_url = enclosure.attrib.get("url", "")
        direct_url = unwrap_op3(actual_url)
        expected_url, local_path = expected_for_episode(episode)
        if direct_url != expected_url:
            parsed = urlparse(direct_url)
            errors.append(
                f"EP{episode:03d}: expected {expected_url}, got {parsed.netloc}{parsed.path}"
            )
        if not local_path.exists():
            errors.append(f"EP{episode:03d}: missing local media {local_path}")
            continue

        expected_length = str(local_path.stat().st_size)
        actual_length = enclosure.attrib.get("length", "")
        if actual_length != expected_length:
            errors.append(
                f"EP{episode:03d}: expected length {expected_length}, got {actual_length}"
            )
        checked += 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Checked {checked} numbered EN episodes with {len(errors)} error(s).")
        return 1

    print(f"OK: checked {checked} numbered EN episodes across media split.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
