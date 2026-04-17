#!/usr/bin/env python3
"""
Repair legacy OpenClaw feed enclosure URLs and lengths.

This backfills historical feed entries whose enclosure URLs drifted away from
the actual published media paths, and normalizes enclosure lengths to the
current local file sizes so feed validators see accurate metadata.

Usage:
  python3 scripts/repair_feed_media.py
  python3 scripts/repair_feed_media.py --feed en
  python3 scripts/repair_feed_media.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse


WORKSPACE = Path.home() / ".openclaw" / "workspace"
PODCAST_DIR = WORKSPACE / "openclaw-podcast"
AUDIO_REPO_DIR = WORKSPACE / "openclaw-podcast-audio"
ARCHIVE_AUDIO_DIR = (
    WORKSPACE
    / ".archive"
    / "openclaw-podcast-audio-backup-20260228-080815"
    / "current-audio"
)

FEEDS = {
    "en": PODCAST_DIR / "feed.xml",
    "es": PODCAST_DIR / "translations" / "feed_es.xml",
    "de": PODCAST_DIR / "translations" / "feed_de.xml",
    "pt": PODCAST_DIR / "translations" / "feed_pt.xml",
    "hi": PODCAST_DIR / "translations" / "feed_hi.xml",
}

ITUNES_NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
OP3_PREFIX = "https://op3.dev/e/"
PAGES_AUDIO_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/"
RAW_AUDIO_BASE = (
    "https://raw.githubusercontent.com/"
    "clawdassistant85-netizen/openclaw-podcast-audio/main/"
)

OLD_AUDIO_PREFIXES = (
    PAGES_AUDIO_BASE,
    RAW_AUDIO_BASE,
    "https://github.com/clawdassistant85-netizen/openclaw-podcast-audio/raw/main/",
    "https://media.githubusercontent.com/media/"
    "clawdassistant85-netizen/openclaw-podcast-audio/main/",
)
OLD_PODCAST_PREFIXES = (
    "https://grayking-creator.github.io/openclaw-podcast/",
    "https://raw.githubusercontent.com/grayking-creator/openclaw-podcast/main/",
    "https://github.com/grayking-creator/openclaw-podcast/raw/main/",
    "https://media.githubusercontent.com/media/grayking-creator/openclaw-podcast/main/",
)

# These files are not reliably served from GitHub Pages today, so we point
# their enclosures at raw GitHub instead of waiting on a Pages build.
RAW_ONLY_RELATIVE_PATHS = {
    "exo_cluster_podcast.mp3",
    "audio/episode_003_full.mp3",
    "audio/episode_002_full.mp3",
    "audio/episode_001_full_v2.mp3",
}


def unwrap_op3(url: str) -> str:
    if url.startswith(OP3_PREFIX):
        return url[len(OP3_PREFIX) :]
    return url


def strip_known_prefix(url: str, prefixes: tuple[str, ...]) -> str | None:
    for prefix in prefixes:
        if url.startswith(prefix):
            return url[len(prefix) :]
    return None


def resolve_local_path(url: str, lang: str) -> Path | None:
    direct = unwrap_op3(url)

    stripped = strip_known_prefix(direct, OLD_AUDIO_PREFIXES)
    if stripped:
        candidate = AUDIO_REPO_DIR / unquote(stripped)
        if candidate.exists():
            return candidate

    stripped = strip_known_prefix(direct, OLD_PODCAST_PREFIXES)
    if stripped:
        candidate = PODCAST_DIR / unquote(stripped)
        if candidate.exists():
            return candidate

    parsed = urlparse(direct)
    path = unquote(parsed.path.lstrip("/"))
    basename = Path(path).name
    candidates = [
        AUDIO_REPO_DIR / path,
        AUDIO_REPO_DIR / "audio" / basename,
        AUDIO_REPO_DIR / "translations" / lang / basename,
        PODCAST_DIR / path,
        PODCAST_DIR / "audio" / basename,
        PODCAST_DIR / "translations" / lang / basename,
        ARCHIVE_AUDIO_DIR / path,
        ARCHIVE_AUDIO_DIR / "audio" / basename,
        ARCHIVE_AUDIO_DIR / "translations" / lang / basename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def preferred_relative_path(current_url: str, local_path: Path, lang: str) -> str | None:
    if local_path.is_relative_to(AUDIO_REPO_DIR):
        rel = local_path.relative_to(AUDIO_REPO_DIR).as_posix()
        if lang == "en" and rel in {"audio/episode_013.mp3", "audio/episode_014.mp3"}:
            return rel
        if lang in {"es", "de", "pt"} and rel.startswith(f"translations/{lang}/"):
            return rel
        if lang == "hi":
            return rel
        return rel

    basename = local_path.name
    archive_rel = {
        "exo_cluster_podcast.mp3": "exo_cluster_podcast.mp3",
        "episode_003_full.mp3": "audio/episode_003_full.mp3",
        "episode_002_full.mp3": "audio/episode_002_full.mp3",
        "episode_001_full_v2.mp3": "audio/episode_001_full_v2.mp3",
    }
    if basename in archive_rel:
        return archive_rel[basename]

    direct = unwrap_op3(current_url)
    stripped = strip_known_prefix(direct, OLD_AUDIO_PREFIXES)
    if stripped:
        return stripped
    return None


def preferred_public_url(rel_path: str, lang: str) -> str:
    if lang != "en" or rel_path in RAW_ONLY_RELATIVE_PATHS:
        return f"{OP3_PREFIX}{RAW_AUDIO_BASE}{rel_path}"
    return f"{OP3_PREFIX}{PAGES_AUDIO_BASE}{rel_path}"


def canonical_relative_path_for_episode(lang: str, episode: int) -> str | None:
    ep = f"{episode:03d}"
    candidate_rels = []

    if lang == "en":
        candidate_rels.extend(
            [
                f"audio/episode_{ep}.mp3",
                f"episode_{ep}.mp3",
                f"audio/episode_{ep}_full.mp3",
                f"audio/episode_{ep}_full_v2.mp3",
            ]
        )
    else:
        candidate_rels.extend(
            [
                f"audio/episode_{ep}_{lang}.mp3",
                f"translations/{lang}/episode_{ep}_{lang}.mp3",
                f"episode_{ep}_{lang}.mp3",
            ]
        )

    search_roots = [AUDIO_REPO_DIR, PODCAST_DIR, ARCHIVE_AUDIO_DIR]
    for rel in candidate_rels:
        for root in search_roots:
            if (root / rel).exists():
                return rel
    return None


def repo_blob_size_or_worktree(local_path: Path) -> int:
    if not local_path.is_relative_to(AUDIO_REPO_DIR):
        return local_path.stat().st_size

    rel = local_path.relative_to(AUDIO_REPO_DIR).as_posix()
    diff = subprocess.run(
        ["git", "-C", str(AUDIO_REPO_DIR), "diff", "--quiet", "--", rel],
        check=False,
    )
    if diff.returncode == 0:
        return local_path.stat().st_size

    head_size = subprocess.run(
        ["git", "-C", str(AUDIO_REPO_DIR), "cat-file", "-s", f"HEAD:{rel}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if head_size.returncode == 0 and head_size.stdout.strip().isdigit():
        return int(head_size.stdout.strip())

    return local_path.stat().st_size


def update_item_block(block: str, new_url: str, new_length: int) -> str:
    def repl(match: re.Match[str]) -> str:
        return f'{match.group(1)}{new_url}{match.group(2)}{new_length}{match.group(3)}'

    block, count = re.subn(
        r'(<enclosure\b[^>]*\burl=")[^"]+(".*?\blength=")[^"]+(".*?/>)',
        repl,
        block,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise ValueError("Could not update enclosure block")
    return block


def repair_feed(feed_key: str, dry_run: bool = False) -> int:
    feed_path = FEEDS[feed_key]
    content = feed_path.read_text(encoding="utf-8")
    root = ET.fromstring(content)
    channel = root.find("channel")
    if channel is None:
        raise ValueError(f"{feed_path} is missing <channel>")

    updates = 0
    for item in channel.findall("item"):
        enclosure = item.find("enclosure")
        if enclosure is None:
            continue

        episode_text = item.findtext("itunes:episode", namespaces=ITUNES_NS)
        current_url = enclosure.attrib.get("url", "")
        current_length = enclosure.attrib.get("length", "")
        rel_path = None
        local_path = None

        if episode_text:
            expected_rel = canonical_relative_path_for_episode(feed_key, int(episode_text))
            if expected_rel:
                current_ep_match = re.search(r"episode_(\d{3})", current_url)
                current_ep = int(current_ep_match.group(1)) if current_ep_match else None
                current_lang_match = re.search(r"episode_\d{3}(?:_([a-z]{2}))?\.mp3", current_url)
                current_lang = current_lang_match.group(1) if current_lang_match else None
                if current_ep != int(episode_text) or (
                    feed_key != "en" and current_lang not in {feed_key}
                ):
                    rel_path = expected_rel
                    local_path = (
                        AUDIO_REPO_DIR / rel_path
                        if (AUDIO_REPO_DIR / rel_path).exists()
                        else PODCAST_DIR / rel_path
                    )

        if rel_path is None:
            local_path = resolve_local_path(current_url, feed_key)
            if local_path is None:
                continue
            rel_path = preferred_relative_path(current_url, local_path, feed_key)
        if rel_path is None:
            continue

        new_url = preferred_public_url(rel_path, feed_key)
        new_length = repo_blob_size_or_worktree(local_path)
        if current_url == new_url and current_length == str(new_length):
            continue

        if episode_text:
            episode = int(episode_text)
            item_pattern = re.compile(
                rf"(<item\b(?:(?!</item>).)*?<itunes:episode>{episode}</itunes:episode>(?:(?!</item>).)*?</item>)",
                re.DOTALL,
            )
        else:
            escaped_url = re.escape(current_url)
            item_pattern = re.compile(
                rf'(<item\b(?:(?!</item>).)*?<enclosure\b(?:(?!</item>).)*?url="{escaped_url}"(?:(?!</item>).)*?</item>)',
                re.DOTALL,
            )
        match = item_pattern.search(content)
        if not match:
            ident = f"episode {episode_text}" if episode_text else current_url
            raise ValueError(f"Could not find item block for {ident} in {feed_path}")

        block = match.group(1)
        new_block = update_item_block(block, new_url, new_length)
        content = content[: match.start(1)] + new_block + content[match.end(1) :]
        updates += 1

    ET.fromstring(content)
    if not dry_run and updates:
        feed_path.write_text(content, encoding="utf-8")
    return updates


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair legacy feed enclosure URLs and lengths")
    parser.add_argument("--feed", choices=sorted(FEEDS), help="Only repair one feed")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report without writing")
    args = parser.parse_args()

    targets = [args.feed] if args.feed else list(FEEDS)
    total_updates = 0
    for feed_key in targets:
        updates = repair_feed(feed_key, dry_run=args.dry_run)
        print(f"{feed_key}: {updates} item(s) updated")
        total_updates += updates
    return 0 if total_updates >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
