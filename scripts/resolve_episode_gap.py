#!/usr/bin/env python3
"""Resolve an unreleased OpenClaw Daily episode gap.

This does not publish anything. It gives the operator two explicit recovery
paths when an earlier draft exists but a later episode is about to be built:

  1. prepare-merge: write a merge packet with the prior draft's Story Slate.
  2. archive: move unreleased draft/assets aside so the episode number can be reused.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
ARCHIVE_DIR = PODCAST_DIR / "archive" / "unreleased"
MERGE_DIR = PODCAST_DIR / "archive" / "merge_requests"
LANGS = ("es", "de", "pt", "hi")


def ep3(ep_num: int) -> str:
    return f"{ep_num:03d}"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_section(text: str, heading: str) -> str:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s+|\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_title(text: str) -> str:
    match = re.search(r"^##\s+Episode Title\s*\n\*\*(.+?)\*\*", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    first = next((line.strip("# ").strip() for line in text.splitlines() if line.strip()), "")
    return first or "(untitled draft)"


def feed_contains_episode(ep_num: int) -> bool:
    feed = PODCAST_DIR / "feed.xml"
    if not feed.exists():
        return False
    return f"<itunes:episode>{ep_num}</itunes:episode>" in read(feed)


def unreleased_paths(ep_num: int) -> list[Path]:
    ep = ep3(ep_num)
    paths = [
        PODCAST_DIR / f"show_notes_episode_{ep}.md",
        PODCAST_DIR / "episodes" / f"episode_{ep}_transcript.md",
        PODCAST_DIR / "episodes" / f"episode_{ep}_transcript_nova.md",
        PODCAST_DIR / "audio" / f"episode_{ep}.mp3",
        PODCAST_DIR / "audio" / f"episode_{ep}_en.mp3",
        PODCAST_DIR / "images" / f"episode_{ep}_cover.png",
        SCRIPTS_DIR / f"generate_episode_{ep}_cover.py",
        SCRIPTS_DIR / "episode_art" / f"episode_{ep}_art.py",
        SCRIPTS_DIR / f"release_ep{ep}_state.json",
    ]
    for lang in LANGS:
        paths.extend(
            [
                PODCAST_DIR / "translations" / lang / f"show_notes_episode_{ep}_{lang}.md",
                PODCAST_DIR / "translations" / lang / f"episode_{ep}_{lang}.md",
                PODCAST_DIR / "audio" / f"episode_{ep}_{lang}.mp3",
                PODCAST_DIR / "images" / f"episode_{ep}_cover_{lang}.png",
            ]
        )
    return paths


def command_status(args: argparse.Namespace) -> int:
    ep = args.episode
    found = [path for path in unreleased_paths(ep) if path.exists()]
    print(f"EP{ep3(ep)} unreleased asset scan")
    if feed_contains_episode(ep):
        print("This episode is already present in feed.xml; archive is blocked unless --force is used.")
    if not found:
        print("No draft/assets found.")
        return 0
    for path in found:
        print(f"- {path.relative_to(PODCAST_DIR)}")
    return 1


def command_prepare_merge(args: argparse.Namespace) -> int:
    prior = args.prior
    target = args.target
    prior_path = PODCAST_DIR / f"show_notes_episode_{ep3(prior)}.md"
    target_path = PODCAST_DIR / f"show_notes_episode_{ep3(target)}.md"
    if not prior_path.exists():
        raise SystemExit(f"Missing prior draft: {prior_path}")
    if not target_path.exists():
        raise SystemExit(f"Missing target draft: {target_path}")

    prior_text = read(prior_path)
    target_text = read(target_path)
    story_slate = extract_section(prior_text, "Story Slate")
    show_notes = extract_section(prior_text, "Show Notes")
    MERGE_DIR.mkdir(parents=True, exist_ok=True)
    out = MERGE_DIR / f"ep{ep3(prior)}_into_ep{ep3(target)}.md"
    out.write_text(
        "\n".join(
            [
                f"# Merge EP{ep3(prior)} stories into EP{ep3(target)}",
                "",
                "Use this packet when rewriting the target show notes before transcript generation.",
                "Keep the target episode number; do not publish the prior draft separately.",
                "",
                f"## Target Draft",
                extract_title(target_text),
                "",
                f"## Prior Draft",
                extract_title(prior_text),
                "",
                "## Prior Story Slate",
                story_slate or "(No Story Slate section found.)",
                "",
                "## Prior Show Notes Block",
                show_notes or "(No Show Notes section found.)",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote merge packet: {out}")
    return 0


def command_archive(args: argparse.Namespace) -> int:
    ep = args.episode
    if feed_contains_episode(ep) and not args.force:
        raise SystemExit(
            f"EP{ep3(ep)} is already present in feed.xml. Refusing to archive released assets. "
            "Pass --force only if you are deliberately repairing a released episode."
        )
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = ARCHIVE_DIR / f"ep{ep3(ep)}_{stamp}"
    moved: list[str] = []
    for path in unreleased_paths(ep):
        if not path.exists():
            continue
        rel = path.relative_to(PODCAST_DIR)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(target))
        moved.append(str(rel))

    if not moved:
        print(f"No EP{ep3(ep)} draft/assets found to archive.")
        return 0

    manifest = {
        "episode": ep,
        "archived_at": stamp,
        "reason": args.reason,
        "moved": moved,
    }
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "archive_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Archived EP{ep3(ep)} unreleased draft/assets to {dest}")
    for rel in moved:
        print(f"- {rel}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="List unreleased draft/assets for an episode")
    status.add_argument("episode", type=int)
    status.set_defaults(func=command_status)

    merge = sub.add_parser("prepare-merge", help="Create a packet for merging prior stories into a target draft")
    merge.add_argument("--prior", type=int, required=True)
    merge.add_argument("--target", type=int, required=True)
    merge.set_defaults(func=command_prepare_merge)

    archive = sub.add_parser("archive", help="Move unreleased draft/assets aside so the number can be reused")
    archive.add_argument("episode", type=int)
    archive.add_argument("--reason", default="replaced by newer approved story slate")
    archive.add_argument("--force", action="store_true", help="Allow archiving assets for an episode already present in feed.xml")
    archive.set_defaults(func=command_archive)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
