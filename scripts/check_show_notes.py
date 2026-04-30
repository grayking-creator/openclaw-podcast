#!/usr/bin/env python3
"""
Show-notes QC checker — run after drafting and before transcript generation.

This enforces the editorial shape Toby wants the automation to produce:
- OpenClaw releases first when release coverage exists
- no theme-first / "common thread" glue driving the whole episode
- fewer, more important stories
- release-heavy episodes must not bury the release details
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CHECKS: list[str] = []
WARNINGS: list[str] = []
ERRORS: list[str] = []

THEME_GLUE_PATTERNS = [
    r"\btrust layer\b",
    r"\bcommon thread\b",
    r"\bnot (?:disconnected|unrelated)\b",
    r"\bwhat today is really about\b",
    r"\bmap of the\b",
    r"\bthese stories all\b",
    r"\bthese stories are all connected\b",
    r"\ball of these stories\b",
    r"\bthese stories all point to\b",
    r"\bthe real story is\b",
    r"\bthe bigger story is\b",
    r"\bone story told across\b",
]

LISTENER_SPECIFIC_PATTERNS = [
    r"\balready owns two Macs\b",
    r"\byour two Macs\b",
    r"\bToby(?:'s)?\b.*\bworkflow\b",
    r"\bfor Toby\b",
]


def check(label: str, condition: bool, severity: str = "ERROR", hint: str = "") -> None:
    if condition:
        CHECKS.append(f"  ✅ {label}")
        return

    msg = f"  {'❌' if severity == 'ERROR' else '⚠️'} {label}"
    if hint:
        msg += f"\n     → {hint}"
    if severity == "ERROR":
        ERRORS.append(msg)
    else:
        WARNINGS.append(msg)


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def first_words(text: str, n: int) -> str:
    return " ".join(text.split()[:n])


def extract_section(notes: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*\n(.+?)(?=\n## |\Z)"
    match = re.search(pattern, notes, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_show_notes_block(notes: str) -> str:
    match = re.search(r"## Show Notes\s*```md\s*(.*?)```", notes, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_story_titles(notes: str) -> list[str]:
    titles = re.findall(r"^###\s+\d+\.\s+\*\*(.+?)\*\*", notes, re.MULTILINE)
    if titles:
        return titles
    titles = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", extract_section(notes, "Story Slate"), re.MULTILINE)
    return titles


def extract_release_tags(notes: str) -> list[str]:
    tags = re.findall(r"openclaw/openclaw/releases/tag/(v\d{4}\.\d+\.\d+)", notes)
    if not tags:
        tags = re.findall(r"\bv\d{4}\.\d+\.\d+\b", extract_section(notes, "Release Coverage Check"))
    deduped: list[str] = []
    seen = set()
    for tag in tags:
        if tag not in seen:
            deduped.append(tag)
            seen.add(tag)
    return deduped


def extract_block_segments(block: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^\[(\d{2}:\d{2}(?:[–-]\d{2}:\d{2})?)\]\s*(.+)$", block, re.MULTILINE))
    segments: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        title = collapse_ws(match.group(2))
        body = block[start:end].strip()
        segments.append((title, body))
    return segments


def contains_theme_glue(text: str) -> list[str]:
    hits = []
    lowered = text.lower()
    for pattern in THEME_GLUE_PATTERNS:
        match = re.search(pattern, lowered, re.IGNORECASE)
        if match:
            hits.append(match.group(0))
    return hits


def run_checks(path: str) -> None:
    notes = Path(path).read_text(encoding="utf-8", errors="ignore")

    show_notes_block = extract_show_notes_block(notes)
    story_titles = extract_story_titles(notes)
    release_tags = extract_release_tags(notes)
    tagline = collapse_ws(extract_section(notes, "Tagline"))
    feed_desc = collapse_ws(extract_section(notes, "Feed Description"))
    block_intro = first_words(show_notes_block, 180)
    segments = extract_block_segments(show_notes_block)

    print(f"\n📋 Show Notes QC: {path}")
    print(f"   Stories: {len(story_titles)}")
    print(f"   Release tags: {', '.join(release_tags) if release_tags else '(none)'}")
    print()

    check("Show notes block exists", bool(show_notes_block),
          hint="Missing `## Show Notes` fenced markdown block.")
    check("Story slate exists", len(story_titles) >= 1,
          hint="Missing `## Story Slate` titles.")

    if show_notes_block:
        intro_words = len(first_words(show_notes_block, 999999).split())
        check("Show notes block is substantial", intro_words >= 450, severity="WARNING",
              hint=f"Show-notes block is only {intro_words} words. Deep episodes usually need more structure/detail.")

    story_slate = extract_section(notes, "Story Slate")
    technical_angle_count = len(re.findall(r"Technical depth angle\s*:\s*\S", story_slate, re.IGNORECASE))
    check("Every story slate item has a Technical depth angle",
          len(story_titles) > 0 and technical_angle_count >= len(story_titles),
          hint=f"Found {technical_angle_count} Technical depth angle line(s) for {len(story_titles)} story/stories. MiniMax/Gemini needs a concrete mechanism to synthesize, not just article summaries.")

    mechanism_terms = re.findall(
        r"\b(API|SDK|runtime|architecture|training|evaluation|benchmark|observability|security|privacy|deployment|configuration|config|failure mode|latency|throughput|cost|memory|scheduler|inference|model card|system card|changelog|release notes)\b",
        show_notes_block,
        re.IGNORECASE,
    )
    check("Show-notes block contains enough technical mechanism vocabulary",
          len(mechanism_terms) >= max(6, len(story_titles) * 2),
          severity="WARNING",
          hint=f"Only found {len(mechanism_terms)} mechanism terms; deepen APIs/runtime/architecture/evals/infra/security/operator tradeoffs before synthesis.")

    listener_specific_hits = []
    for pattern in LISTENER_SPECIFIC_PATTERNS:
        match = re.search(pattern, notes, re.IGNORECASE)
        if match:
            listener_specific_hits.append(match.group(0))
    check("No listener-specific personal setup references", len(listener_specific_hits) == 0, severity="WARNING",
          hint=f"Found listener-specific phrasing: {listener_specific_hits[:3]}")

    title_theme_hits = contains_theme_glue(" ".join([extract_section(notes, "Episode Title"), tagline, feed_desc]))
    intro_theme_hits = contains_theme_glue(first_words(show_notes_block, 220))
    check("No theme-first framing in title/tagline/feed description", len(title_theme_hits) == 0,
          hint=f"Theme-first umbrella framing is banned: {title_theme_hits[:3]}")
    check("No theme-first framing in the show-notes intro", len(intro_theme_hits) == 0,
          hint=f"Theme-first umbrella framing is banned in the intro: {intro_theme_hits[:3]}")

    if release_tags:
        first_title = story_titles[0] if story_titles else ""
        check("Release story is story #1", bool(re.search(r"openclaw|v\d{4}\.\d+\.\d+", first_title, re.IGNORECASE)),
              hint=f"Story #1 should be the OpenClaw release block, got: {first_title!r}")

        first_120 = first_words(show_notes_block, 120)
        first_180 = first_words(show_notes_block, 180)
        check("Intro names OpenClaw release coverage immediately",
              bool(re.search(r"openclaw|v\d{4}\.\d+\.\d+", first_120, re.IGNORECASE)),
              hint="The first paragraph should open on the release(s), not on a thematic frame.")
        check("Intro includes all covered release tags early",
              all(tag in first_180 for tag in release_tags),
              hint=f"Expected all release tags in the first 180 words: {release_tags}")

        non_release_story_count = max(0, len(story_titles) - 1)
        runtime_exception = bool(re.search(r"\b40–48 min\b|\b40-48 min\b|\b50|60 minutes\b|\bkeep the existing builder stories\b", notes, re.IGNORECASE))
        check("Release episode keeps extra stories tightly limited", non_release_story_count <= 3 or runtime_exception,
              hint=f"Found {non_release_story_count} non-release stories. Cut lower-priority stories before cutting release detail unless Toby explicitly asked to keep the existing builder stories and extend runtime.")

        if len(segments) >= 2:
            first_story_title, first_story_body = segments[1]
            first_story_words = len(first_story_body.split())
            check("First post-hook segment is the release deep dive",
                  bool(re.search(r"openclaw|v\d{4}\.\d+\.\d+", first_story_title, re.IGNORECASE)),
                  hint=f"First real segment should be the release block, got: {first_story_title!r}")
            check("Release segment is detailed enough to carry the front of the episode",
                  first_story_words >= 260,
                  hint=f"First release segment is only {first_story_words} words. Push more concrete release detail into the front of the episode.")
        else:
            check("Timestamped segment structure exists in show notes", False,
                  hint="Expected at least an intro segment and a release segment in the show-notes block.")
    else:
        check("Episode does not sprawl into too many low-priority stories", len(story_titles) <= 5, severity="WARNING",
              hint=f"Found {len(story_titles)} stories. Keep non-release episodes tight unless there is a major-news day.")

        early_words = first_words(show_notes_block, 180)
        no_release_meta_hits = []
        for pattern in [
            r"\bnot a release episode\b",
            r"\bno release coverage\b",
            r"\bno new stable openclaw release\b",
            r"\bthere is no new stable openclaw release\b",
            r"\bthe latest stable tags are\b",
            r"\bcovered in recent episode notes\b",
            r"\bfive stories today\b",
            r"\bthis is a builder-stack episode\b",
        ]:
            match = re.search(pattern, early_words, re.IGNORECASE)
            if match:
                no_release_meta_hits.append(match.group(0))
        check("No-release intro avoids meta throat-clearing / list-style opening", len(no_release_meta_hits) == 0,
              hint=f"Opening should hook, not announce episode mechanics: {no_release_meta_hits[:4]}")

    if "images 2.0" in notes.lower() or "gpt-image-2" in notes.lower():
        image_story_context = extract_section(notes, "Story Slate") + "\n" + show_notes_block
        has_workflow_lens = bool(re.search(
            r"workflow|builder|production|mock|ui|layout|diagram|slides|poster|text-heavy|readable text",
            image_story_context,
            re.IGNORECASE,
        ))
        check("Image-model coverage includes a practical workflow lens", has_workflow_lens, severity="WARNING",
              hint="If covering Images 2.0 / gpt-image-2, explain whether it changes practical builder workflows.")

    print("Results:")
    for item in CHECKS:
        print(item)
    if WARNINGS:
        print()
        for item in WARNINGS:
            print(item)
    if ERRORS:
        print()
        for item in ERRORS:
            print(item)
        print(f"\n❌ {len(ERRORS)} error(s) — fix show notes before approving transcript generation\n")
        sys.exit(1)

    print(f"\n✅ All checks passed ({len(WARNINGS)} warning(s))\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run QC checks on podcast show notes")
    parser.add_argument("show_notes", help="Path to show notes markdown")
    args = parser.parse_args()
    run_checks(args.show_notes)
