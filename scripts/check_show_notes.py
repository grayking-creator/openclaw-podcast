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
    notes_path = Path(path)
    notes = notes_path.read_text(encoding="utf-8", errors="ignore")
    ep_match = re.search(r"episode_(\d{3})", notes_path.name)
    ep_num = int(ep_match.group(1)) if ep_match else 0

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
    if ep_num >= 55:
        check("AgentStack Daily slate has six real topics",
              len(story_titles) >= 6,
              hint=f"Expected at least 6 numbered Story Slate topics for EP055+; found {len(story_titles)}. Do not leave viable topics under Extra Research Candidates when building the draft.")

    if show_notes_block:
        intro_words = len(first_words(show_notes_block, 999999).split())
        check("Show notes block is substantial", intro_words >= 450, severity="WARNING",
              hint=f"Show-notes block is only {intro_words} words. Deep episodes usually need more structure/detail.")

    story_slate = extract_section(notes, "Story Slate")
    technical_angle_count = len(re.findall(r"Technical depth angle\s*:\s*\S", story_slate, re.IGNORECASE))
    check("Every story slate item has a Technical depth angle",
          len(story_titles) > 0 and technical_angle_count >= len(story_titles),
          hint=f"Found {technical_angle_count} Technical depth angle line(s) for {len(story_titles)} story/stories. MiniMax/Gemini needs a concrete mechanism to synthesize, not just article summaries.")

    extra_research = extract_section(notes, "Extra Research Candidates")
    extra_candidate_count = len(re.findall(r"^\s*[-*]\s+\*\*.+?\*\*", extra_research, re.MULTILINE))
    extra_angle_count = len(re.findall(r"Technical depth angle\s*:\s*\S", extra_research, re.IGNORECASE))
    extra_link_count = len(re.findall(r"https?://\S+", extra_research))
    if 46 <= ep_num < 55:
        check("Research phase includes exactly three extra technical story candidates",
              extra_candidate_count == 3 and extra_angle_count >= 3 and extra_link_count >= 3,
              hint=f"Expected 3 backup candidates with links and Technical depth angle lines; found candidates={extra_candidate_count}, angles={extra_angle_count}, links={extra_link_count}.")

    mechanism_terms = re.findall(
        r"\b(API|SDK|runtime|architecture|training|evaluation|benchmark|observability|security|privacy|deployment|configuration|config|failure mode|latency|throughput|cost|memory|scheduler|inference|model card|system card|changelog|release notes)\b",
        show_notes_block,
        re.IGNORECASE,
    )
    check("Show-notes block contains enough technical mechanism vocabulary",
          len(mechanism_terms) >= max(6, len(story_titles) * 2),
          severity="WARNING",
          hint=f"Only found {len(mechanism_terms)} mechanism terms; deepen APIs/runtime/architecture/evals/infra/security/operator tradeoffs before synthesis.")



    internal_impl_patterns = [
        r"\bfetched window\b",
        r"\bfetched release window\b",
        r"\brelease window\b",
        r"\bselected from the fetched\b",
        r"\bdaily release check\b",
        r"\bno new stable .*selected\b",
        r"\bno new stable .*candidate\b",
    ]
    internal_impl_hits = []
    for pat in internal_impl_patterns:
        internal_impl_hits.extend(re.findall(pat, notes, re.IGNORECASE))
    check("No internal research/build implementation language in public notes", len(internal_impl_hits) == 0,
          hint=f"Remove internal process/research/build wording from public episode: {internal_impl_hits[:8]}")

    public_meta_patterns = [
        r"\barchitecture-advice\b", r"\bdrops? the .*framing\b",
        r"\breturns? to a .*format\b", r"\bthis rewrite\b",
        r"\bchanges? the format\b",
        r"\bsix[- ]story\b",
        r"\bsix practical stories\b",
        r"\btoday'?s six stories\b",
        r"\bone obvious flagship release\b",
        r"\bflagship release\b",
        r"\bnot short on news\b",
        r"\bstretching one update\b",
        r"\bbefore audio\b",
        r"\bbefore .*publish\b",
        r"\breview before release\b",
        r"\brelease plan\b",
        r"\bactual artifact\b",
        r"\bstory in the slate\b",
        r"\btranscript include\b",
        r"\btranscript includes\b",
        r"\bwhat changed operationally\b",
        r"\blist of links\b",
        r"\bstrong new .*release block\b",
        r"\bcurrent stable feed window\b",
        r"\brecent-version scan\b",
        r"\bToby (?:asked|wanted|said|told)\b", r"\byou asked\b", r"\byou told\b",
        r"\bno grand theory\b", r"\bno abstract operating model\b", r"\bstraight what'?s-new episode\b",
        r"\bnot a lecture\b", r"\bdo not waste\b", r"\bdo not invent\b", r"\bnot a long .*recipe\b",
    ]
    public_meta_hits = []
    for pat in public_meta_patterns:
        public_meta_hits.extend(re.findall(pat, notes, re.IGNORECASE))
    check("No public editorial-feedback/meta framing leaks", len(public_meta_hits) == 0,
          hint=f"Remove production-instruction/meta phrasing from public show notes: {public_meta_hits[:8]}")

    operator_slog_hits = []
    for pat in [
        r"\boperator playbook\b",
        r"\bturn the .* into a .* workflow\b",
        r"\bthe first workflow\b",
        r"\bthe second workflow\b",
        r"\bthe third workflow\b",
        r"\bthe fourth workflow\b",
        r"\bthe fifth workflow\b",
        r"\bthe sixth workflow\b",
        r"\bthe seventh workflow\b",
        r"\bthe eighth workflow\b",
        r"\bconcrete builder workflow\b",
        r"\bchecklist is simple\b",
    ]:
        operator_slog_hits.extend(re.findall(pat, notes, re.IGNORECASE))
    check("No generic operator-playbook slog in public notes", len(operator_slog_hits) == 0,
          hint=f"Rewrite toward what changed / what is new / why it matters, not generic workflow advice: {operator_slog_hits[:8]}")

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


    # ── Editorial quality gate: no prior-episode/version-history filler ──────
    # Show notes feed the transcript; reject process housekeeping before it can
    # become spoken audio.
    prior_episode_meta_patterns = [
        r"\b(?:last|previous|prior|earlier)\s+(?:episode|episodes|show|shows|show-note|show-note files|show notes)\b.{0,140}\b(?:cover|covered|coverage|already|recent)\b",
        r"\b(?:already|previously|recently)\s+(?:cover|covered|discussed|talked about)\b",
        r"\b(?:we|I|this show|OpenClaw Daily)\s+(?:already|previously|recently)\s+(?:covered|discussed|talked about)\b",
        r"\b(?:covered|discussed|talked about)\s+(?:in|on)\s+(?:EP\d+|episode\s+\d+|a previous episode|previous episodes|recent episode notes)\b",
        r"\b(?:under|because of)\s+the\s+(?:latest-contiguous|contiguous-release|release coverage)\s+rule\b",
        r"\bEP\d+\s+(?:starts|surfaces|covers|covered|talked|discussed)\b",
        r"\b(?:show-note files|episode notes|release list)\s+(?:already\s+)?(?:cover|covered|show|indicate)\b",
        r"\b(?:v\d{4}\.\d+\.\d+[,\s]*(?:and\s+)*){2,}\b.*\b(?:older stable tags|already cover|previous|prior|recent)\b",
    ]
    prior_episode_meta_hits = []
    for pattern in prior_episode_meta_patterns:
        prior_episode_meta_hits.extend(re.findall(pattern, notes, re.IGNORECASE | re.DOTALL))
    check("No prior-episode / already-covered recap filler",
          len(prior_episode_meta_hits) == 0,
          hint=f"Remove release-history/show-process housekeeping before transcript generation: {[hit if isinstance(hit, str) else ' '.join(hit) for hit in prior_episode_meta_hits[:5]]}")

    public_episode_material = "\n".join([show_notes_block, story_slate, tagline, feed_desc])
    public_version_tags = sorted(set(re.findall(r"\bv\d{4}\.\d+\.\d+\b", public_episode_material)))
    if release_tags:
        off_slate_version_tags = [tag for tag in public_version_tags if tag not in release_tags]
        check("Public show notes do not mention off-slate old version tags",
              len(off_slate_version_tags) == 0,
              hint=f"Old-version roll calls are banned from public episode material: {off_slate_version_tags[:8]}")

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
