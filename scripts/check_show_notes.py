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

TITLE_OVERLAP_STOPWORDS = {
    "about", "across", "after", "agent", "agents", "agentstack", "around",
    "because", "before", "bring", "brings", "build", "builder", "builders",
    "code", "copilot", "daily", "from", "github", "into", "make", "makes", "model", "models",
    "release", "releases", "ship", "ships", "stack", "story", "that",
    "the", "their", "this", "through", "with", "work", "workflow", "workflows",
}

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


def extract_public_editorial_text(notes: str) -> str:
    sections = [
        notes.split("\n", 1)[0],
        extract_section(notes, "Episode Title"),
        extract_section(notes, "Tagline"),
        extract_section(notes, "Feed Description"),
        extract_section(notes, "Story Slate"),
        extract_show_notes_block(notes),
        extract_section(notes, "Chapters"),
    ]
    return "\n\n".join(section for section in sections if section)


def extract_story_titles(notes: str) -> list[str]:
    titles = re.findall(r"^###\s+\d+\.\s+\*\*(.+?)\*\*", notes, re.MULTILINE)
    if titles:
        return titles
    titles = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", extract_section(notes, "Story Slate"), re.MULTILINE)
    return titles


def extract_extra_candidate_titles(notes: str) -> list[str]:
    return re.findall(r"^\s*[-*]\s+\*\*(.+?)\*\*", extract_section(notes, "Extra Research Candidates"), re.MULTILINE)


def title_tokens(title: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9][a-z0-9.+-]{2,}", title.lower()))
    return {token for token in tokens if token not in TITLE_OVERLAP_STOPWORDS}


def extract_release_tags(notes: str) -> list[str]:
    tags = re.findall(r"openclaw/openclaw/releases/tag/(v\d{4}\.\d+\.\d+)", notes)
    tags.extend(re.findall(r"NousResearch/hermes-agent/releases/tag/(v\d{4}\.\d+\.\d+)", notes))
    deduped: list[str] = []
    seen = set()
    for tag in tags:
        if tag not in seen:
            deduped.append(tag)
            seen.add(tag)
    return deduped


# Public-facing sections of a show-notes draft where prerelease / beta tag mentions
# are banned. The internal `## Release Coverage Check` block and
# `## Harness Version Reference` are the only places a prerelease tag may appear.
PUBLIC_FACING_SECTIONS = [
    "AgentStack Daily EP",  # H1 episode title
    "## Story Slate",
    "## Show Notes",
    "## Chapters",
    "## Primary Links",
    "## GitHub Project Radar",
    "## Local LLM Spotlight",
    "## Model Discovery Check",
]

# Prerelease / non-stable version tag suffixes. Matched against the literal tag in
# public-facing copy, e.g. "v2026.6.5-beta.2" or "rust-v0.138.0-alpha.6".
PRERELEASE_SUFFIX_RE = re.compile(r"(?:^|[^a-z])(v\d[\w.\-]*?(?:alpha|beta|rc|dev|pre|preview)\.?[\w.\-]*?)(?=\b)", re.IGNORECASE)
# A more conservative catch for dash-suffixed tags like "-beta.2", "-rc.1".
# Match any "vN.M(.K)?-(alpha|beta|rc|dev|pre).N" pattern to cover year-prefixed and short-tag forms.
PRERELEASE_DASH_RE = re.compile(r"v\d+(?:\.\d+){1,3}-(?:alpha|beta|rc|dev|pre)(?:\.\d+)?", re.IGNORECASE)


def extract_prerelease_tag_mentions(public_text: str) -> list[str]:
    """Return every prerelease / non-stable tag mentioned in public-facing copy."""
    hits: list[str] = []
    for m in PRERELEASE_DASH_RE.finditer(public_text):
        hits.append(m.group(0))
    return sorted(set(hits))


def public_facing_text(notes: str) -> str:
    """Concatenate the public-facing sections of a show-notes draft.

    Excludes `## Release Coverage Check` and `## Harness Version Reference`,
    which are the only places a prerelease tag may legitimately appear.
    """
    lines = notes.splitlines()
    out: list[str] = []
    in_internal = False
    current_section: str | None = None
    section_buffer: list[str] = []
    kept: list[str] = []

    def flush():
        if current_section in [s for s in PUBLIC_FACING_SECTIONS]:
            kept.extend(section_buffer)

    for line in lines:
        stripped = line.strip()
        # Section header
        if stripped.startswith("## ") or stripped.startswith("# "):
            flush()
            current_section = stripped
            section_buffer = [line + "\n"]
            continue
        if current_section is not None:
            section_buffer.append(line + "\n")
    flush()
    return "".join(kept)


def find_prior_episode_repeats(notes_path: Path, ep_num: int, story_titles: list[str], lookback: int = 3) -> list[str]:
    """Compare current story titles against the last ``lookback`` episodes of show notes.

    The No Back-to-Back Topic Repeats rule (locked 2026-05-24, EP070 patch 2026-06-14) requires
    the slate to differ from the prior episode *and* the episodes before that. A topic that
    has already been a numbered story in any of the last few episodes must not be promoted
    back into the public slate just because the title was lightly reworded. A previous
    material_followup exemption (covering words like "suspend", "directive", "government",
    "access") was removed because it let a story we already led with yesterday pass as a
    fresh topic; that was the EP070 Story 1 regression.
    """
    if ep_num <= 1:
        return []

    seen_pairs: list[tuple[str, set[str]]] = []
    for back in range(1, lookback + 1):
        prior_path = notes_path.with_name(f"show_notes_episode_{ep_num - back:03d}.md")
        if not prior_path.exists():
            continue
        prior = prior_path.read_text(encoding="utf-8", errors="ignore")
        prior_topics = extract_story_titles(prior)
        prior_topics.extend(re.findall(r"^\s*[-*]\s+\*\*(.+?)\*\*", extract_section(prior, "Extra Research Candidates"), re.MULTILINE))
        for topic in prior_topics:
            tokens = title_tokens(topic)
            if tokens:
                seen_pairs.append((f"EP{ep_num - back:03d}::" + topic, tokens))

    repeats: list[str] = []
    for title in story_titles:
        tokens = title_tokens(title)
        if len(tokens) < 3:
            continue
        matched: list[str] = []
        for prior_label, prior_tokens in seen_pairs:
            hits = tokens & prior_tokens
            overlap = len(hits) / min(len(tokens), len(prior_tokens))
            if len(hits) >= 3 and overlap >= 0.45:
                matched.append(f"{prior_label.split('::', 1)[1]!r} ({len(hits)} shared title tokens)")
        if matched:
            repeats.append(f"{title} repeats a recent episode's topic: " + "; ".join(matched[:3]))
    return repeats


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
    public_editorial_text = extract_public_editorial_text(notes)
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
    if ep_num >= 68:
        check("AgentStack Daily slate has ten real topics",
              len(story_titles) >= 10,
              hint=f"Expected at least 10 numbered Story Slate topics for EP068+; found {len(story_titles)}. Do not leave viable topics under Extra Research Candidates when building the draft.")
    elif ep_num >= 55:
        check("AgentStack Daily slate has six real topics",
              len(story_titles) >= 6,
              hint=f"Expected at least 6 numbered Story Slate topics for EP055+; found {len(story_titles)}. Do not leave viable topics under Extra Research Candidates when building the draft.")
    if ep_num >= 57:
        prior_repeats = find_prior_episode_repeats(notes_path, ep_num, story_titles)
        check("Story slate does not repeat the previous episode's topics",
              len(prior_repeats) == 0,
              hint="Replace repeated topics before transcript generation: " + "; ".join(prior_repeats[:6]))

    if show_notes_block:
        intro_words = len(first_words(show_notes_block, 999999).split())
        check("Show notes block is substantial", intro_words >= 450, severity="WARNING",
              hint=f"Show-notes block is only {intro_words} words. Deep episodes usually need more structure/detail.")

    no_release_watch_hits = []
    for pattern in [
        r"\b(?:openclaw|hermes|codex)\s+stable\s+watch\b",
        r"\bstable\s+watch\b",
        r"\bwatch\s+lane\b",
        r"\bbeta\s+watch\b",
        r"\bstability\s+check\b",
    ]:
        no_release_watch_hits.extend(re.findall(pattern, public_editorial_text, re.IGNORECASE))
    check("No non-release watch lane promoted into public episode topics",
          len(no_release_watch_hits) == 0,
          hint=f"Keep no-release/beta bookkeeping inside Release Coverage Check only: {no_release_watch_hits[:5]}")

    # Prerelease / beta tag ban in public-facing copy (EP066 incident 2026-06-08).
    # Prerelease tags may only appear in `## Release Coverage Check` and
    # `## Harness Version Reference`. Anywhere else is a hard-fail.
    public_only = public_facing_text(notes)
    prerelease_in_public = extract_prerelease_tag_mentions(public_only)
    check("No prerelease / beta tags in public-facing copy",
          len(prerelease_in_public) == 0,
          hint=f"Prerelease tags belong only in `## Release Coverage Check` / `## Harness Version Reference`. "
               f"Found in title, Story Slate, Show Notes, Chapters, Primary Links, or other public sections: "
               f"{prerelease_in_public[:5]}. Phrase as 'prerelease', 'beta bundle', or 'upcoming release' instead.")

    # Local LLM Spotlight required in every show-notes draft (EP066 incident 2026-06-08).
    local_llm_spotlight = bool(extract_section(notes, "Local LLM Spotlight"))
    check("Local LLM Spotlight section exists",
          local_llm_spotlight,
          hint="Add a `## Local LLM Spotlight` section that names one local/self-hosted model or inference move worth tracking this cycle, "
               "with a primary-source link and a one-line `Try now:`. The spotlight is a recurring callout, not a full story.")

    # No watch-harness inclusion in public-facing copy (EP066 incident 2026-06-08).
    # The agent-harness block must only mention harnesses that shipped a new stable release
    # in the current cycle. "Held its position" / "remains at" / "on continuous delivery"
    # callouts for non-changing harnesses are banned in the public slate.
    watch_harness_patterns = [
        (r"\bHermes(?:\s+Agent)?\s+(?:remains\s+at|held\s+its\s+position|at\s+v\d|on\s+continuous\s+delivery)", "Hermes"),
        (r"\bCodex(?:\s+CLI)?\s+(?:remains\s+at|held\s+its\s+position|at\s+rust-v\d|on\s+continuous\s+delivery)", "Codex"),
        (r"\bAntigravity(?:\s+CLI)?\s+(?:remains\s+at|held\s+its\s+position|on\s+continuous\s+delivery)", "Antigravity"),
    ]
    # No-release narration for ANY harness is a hard failure in public copy
    # (Toby, 2026-06-10): with five tracked harnesses, "X had no release this
    # cycle" becomes a roll call every episode. Only harnesses that shipped get
    # named in release context; the internal Release Coverage Check is the only
    # place a no-change fact may be recorded.
    _harness_names = r"(?:OpenClaw|Hermes(?:\s+Agent)?|(?:OpenAI\s+)?Codex(?:\s+CLI)?|Claude\s+Code(?:\s+CLI)?|Antigravity(?:\s+CLI)?)"
    if ep_num >= 68:
        no_release_narration_patterns = [
            rf"\b{_harness_names}\b[^.\n]{{0,90}}\bno\s+(?:new\s+)?(?:stable\s+)?(?:release|update|version|change)s?\b",
            rf"\bno\s+(?:new\s+)?(?:stable\s+)?(?:release|update|version|change)s?\b[^.\n]{{0,90}}\b{_harness_names}\b",
            rf"\b{_harness_names}\b[^.\n]{{0,40}}\b(?:remains?|stays?|stayed|holds?|held|sits?)\s+(?:at|on|steady|unchanged|put)\b",
            rf"\bnothing\s+new\s+(?:from|for|on)\s+{_harness_names}\b",
            rf"\b{_harness_names}\b[^.\n]{{0,40}}\b(?:didn'?t|did\s+not|hasn'?t|has\s+not)\s+(?:ship|update|move|change)\b",
            rf"\bquiet\s+(?:cycle|week|day)\s+for\s+{_harness_names}\b",
        ]
        no_release_narration_hits: list[str] = []
        for pat in no_release_narration_patterns:
            for m in re.finditer(pat, public_only, re.IGNORECASE):
                no_release_narration_hits.append(m.group(0)[:70])
        check("No 'harness had no release' narration in public copy",
              len(no_release_narration_hits) == 0,
              hint="Only harnesses that shipped get named in release context. Record no-change facts in "
                   f"`## Release Coverage Check` only — never in public sections: {no_release_narration_hits[:5]}")
    watch_harness_hits: list[str] = []
    for pattern, harness_name in watch_harness_patterns:
        for m in re.finditer(pattern, public_only, re.IGNORECASE):
            watch_harness_hits.append(f"{harness_name} ({m.group(0)[:60]})")
    check("No watch-harness inclusion in public-facing copy",
          len(watch_harness_hits) == 0,
          hint=f"Do not mention a harness that did not ship a new stable release this cycle. "
               f"Drop or downgraded to a single in-passing reference: {watch_harness_hits[:5]}")

    story_slate = extract_section(notes, "Story Slate")
    extra_candidate_titles = extract_extra_candidate_titles(notes)
    duplicate_extra_candidates: list[str] = []
    story_token_sets = [(title, title_tokens(title)) for title in story_titles]
    for extra_title in extra_candidate_titles:
        extra_tokens = title_tokens(extra_title)
        if len(extra_tokens) < 2:
            continue
        for story_title, story_tokens in story_token_sets:
            if not story_tokens:
                continue
            overlap = len(extra_tokens & story_tokens)
            if overlap >= 2 and overlap / max(1, min(len(extra_tokens), len(story_tokens))) >= 0.5:
                duplicate_extra_candidates.append(f"{extra_title} duplicates {story_title}")
                break
    check("Extra Research Candidates do not duplicate selected slate topics",
          len(duplicate_extra_candidates) == 0,
          hint="Replace backup candidates that are already selected in Story Slate: " + "; ".join(duplicate_extra_candidates[:5]))

    technical_angle_count = len(re.findall(r"Technical depth angle\s*:\s*\S", story_slate, re.IGNORECASE))
    check("Every story slate item has a Technical depth angle",
          len(story_titles) > 0 and technical_angle_count >= len(story_titles),
          hint=f"Found {technical_angle_count} Technical depth angle line(s) for {len(story_titles)} story/stories. MiniMax/Gemini needs a concrete mechanism to synthesize, not just article summaries.")

    # Story-slope technical density cap (EP066 incident 2026-06-08; revised 2026-06-08
    # after Toby's follow-up: the per-story `Actionability angle` had turned into a
    # five-bullet "do this, then check that, then test X" checklist per story, and
    # that reads like operator homework, not news. The cap is now: keep the
    # `Technical depth angle` short enough to leave room for the news (≤ ~120
    # words); the `Actionability angle` must describe the implication (what this
    # means for builders, the stack, the market) and may include zero, one, or at
    # most two concrete examples. No more "≥3 try-now moves" enforcement. No more
    # "Actionability must be longer than Technical depth" enforcement. The point
    # of the angle is to land the news, not to assign a to-do list.
    def _angle_words(text: str, start_label: str, stop_labels: list[str]) -> int:
        m = re.search(rf"{start_label}\s*:\s*", text, re.IGNORECASE)
        if not m:
            return 0
        rest = text[m.end():]
        earliest = len(rest)
        for stop in stop_labels:
            sm = re.search(rf"{stop}\s*:\s*", rest, re.IGNORECASE)
            if sm and sm.start() < earliest:
                earliest = sm.start()
        chunk = rest[:earliest]
        # Stop at a blank line followed by another major heading.
        for sep in ["\n\n", "\n#"]:
            idx = chunk.find(sep)
            if idx >= 0 and idx < earliest:
                chunk = chunk[:idx]
        return len(chunk.split())

    tech_words_per_story: list[int] = []
    for title in story_titles:
        # Find the position of the title in the slate, then measure from there.
        m = re.search(re.escape(title), story_slate, re.IGNORECASE)
        if not m:
            continue
        segment = story_slate[m.start():]
        # The next title's position is the end of this story.
        next_titles = [t for t in story_titles if t != title]
        next_positions = []
        for nt in next_titles:
            nm = re.search(re.escape(nt), segment[20:], re.IGNORECASE)
            if nm:
                next_positions.append(20 + nm.start())
        end_pos = min(next_positions) if next_positions else len(segment)
        story_segment = segment[:end_pos]
        tw = _angle_words(story_segment, "Technical depth angle", ["Actionability angle", "Listener hook"])
        tech_words_per_story.append(tw)
    over_cap = [f"story {i+1}={tw}w" for i, tw in enumerate(tech_words_per_story) if tw > 120]
    check("Technical depth angle stays under ~120 words per story",
          not over_cap,
          hint=f"Cap each `Technical depth angle` at ~120 words; long technical rants bury the news. Over cap: {over_cap[:5]}")

    # Anti-checklist guard (EP066 follow-up 2026-06-08): per-story Actionability
    # angles that read like a homework checklist ("run X, then check Y, then
    # enable Z, then audit W, then test V") make the episode painful to listen
    # to. The angle should land the implication of the news, not assign a to-do
    # list. Reject angles that have four or more imperative "verb+object"
    # recipes stacked on top of each other.
    imperative_verbs = (
        r"\b(?:run|check|enable|test|try|install|configure|set up|setup|rotate|"
        r"watch|monitor|track|read|clone|explore|audit|evaluate|verify|"
        r"compare|connect|deploy|launch|use|pull|download|build|set|"
        r"open|review|inspect|tune|measure|benchmark|register|sign up|"
        r"subscribe|join|bookmark|note|plan|map|tag|label|wire|hook|attach|"
        r"add|remove|drop|swap|switch|roll|back|forward|reset|reload|"
        r"restart|promote|demote|pin|unpin|lock|unlock|approve|reject|"
        r"ship|publish|release|merge|rebase|push|pull|fork|star)\b"
    )
    checklist_angles: list[str] = []
    for title in story_titles:
        m = re.search(re.escape(title), story_slate, re.IGNORECASE)
        if not m:
            continue
        segment = story_slate[m.start():]
        next_titles = [t for t in story_titles if t != title]
        next_positions = []
        for nt in next_titles:
            nm = re.search(re.escape(nt), segment[20:], re.IGNORECASE)
            if nm:
                next_positions.append(20 + nm.start())
        end_pos = min(next_positions) if next_positions else len(segment)
        story_segment = segment[:end_pos]
        # Pull the Actionability angle text.
        am = re.search(r"Actionability angle\s*:\s*", story_segment, re.IGNORECASE)
        if not am:
            continue
        rest = story_segment[am.end():]
        # Stop at Listener hook or next heading or blank line.
        cut_positions = [len(rest)]
        for stop in [r"Listener hook\s*:", r"Technical depth angle\s*:", r"\n\n", r"\n#"]:
            sm = re.search(stop, rest, re.IGNORECASE)
            if sm and sm.start() < cut_positions[0]:
                cut_positions[0] = sm.start()
        act_text = rest[: cut_positions[0]]
        # Count imperative-verb sentences inside the angle.
        sentences = re.split(r"[.;]\s+", act_text)
        imperative_count = 0
        for s in sentences:
            if re.search(imperative_verbs, s, re.IGNORECASE):
                imperative_count += 1
        if imperative_count >= 4:
            checklist_angles.append(f"story '{title[:60]}' has {imperative_count} imperative sentences in Actionability angle (cap is 3)")
    check("Actionability angle is not a homework checklist (≤3 imperative sentences per story)",
          not checklist_angles,
          hint="The Actionability angle should land the implication of the news, not assign a to-do list. If a story angle has 4+ imperative 'do this' sentences, rewrite as 'what this means' / 'why this matters' with at most one or two concrete examples. Offenders: " + "; ".join(checklist_angles[:5]))

    action_angle_count = len(re.findall(r"Actionability angle\s*:\s*\S", story_slate, re.IGNORECASE))
    listener_hook_count = len(re.findall(r"Listener hook\s*:\s*\S", story_slate, re.IGNORECASE))
    if ep_num >= 56:
        check("Every story slate item has an Actionability angle",
              len(story_titles) > 0 and action_angle_count >= len(story_titles),
              hint=f"Found {action_angle_count} Actionability angle line(s) for {len(story_titles)} story/stories. The angle should land the implication of the news, not a checklist.")
        check("Every story slate item has a Listener hook",
              len(story_titles) > 0 and listener_hook_count >= len(story_titles),
              hint=f"Found {listener_hook_count} Listener hook line(s) for {len(story_titles)} story/stories. Future drafts need a listenable reason to care, not only a technical angle.")
        priority_stack_hits = re.findall(r"\b(OpenClaw|Codex|Claude Code|Hermes|Antigravity)\b", story_slate, re.IGNORECASE)
        is_release_context = bool(release_tags) or bool(re.search(r"\bagent-stack release\b|\bOpenClaw\b.*\bHermes\b|\bHermes\b.*\bOpenClaw\b", story_slate, re.IGNORECASE | re.DOTALL))
        if is_release_context:
            # Count harnesses that actually shipped a new stable release this cycle,
            # from the ## Release Coverage Check block. A harness "shipped" if its
            # line has "Selected missing version" or otherwise omits the
            # "No new stable release this cycle" / "Continuous delivery" markers.
            # The threshold should match the shipped count so we don't force
            # watch-harness inclusion for non-shipping harnesses (EP066 incident,
            # locked 2026-06-08, updated EP068 to be conditional).
            release_coverage_block = extract_section(notes, "Release Coverage Check")
            shipped_count = 0
            if release_coverage_block:
                for line in release_coverage_block.split("\n"):
                    if "Selected missing version" in line:
                        shipped_count += 1
                    elif line.lstrip().startswith(("- **", "**")) and "Latest stable verified" in line \
                            and "No new stable release" not in line \
                            and "Continuous delivery" not in line:
                        shipped_count += 1
            if shipped_count == 0 and release_tags:
                shipped_count = min(len(release_tags), 5)
            threshold = max(1, shipped_count) if shipped_count else 1
            check("AgentStack priority tools appear in the story slate",
                  len(set(hit.lower() for hit in priority_stack_hits)) >= threshold,
                  hint=f"EP056+ release/cleanup drafts should track the {shipped_count} harness(es) that shipped a new stable release this cycle (found in slate: {sorted(set(h.lower() for h in priority_stack_hits))}). The threshold matches the shipped count — never force watch-harness inclusion.")

    github_project_radar = extract_section(notes, "GitHub Project Radar")
    github_repo_links = re.findall(r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", github_project_radar)
    github_stack_angles = re.findall(r"Stack improvement angle\s*:\s*\S", github_project_radar, re.IGNORECASE)
    github_try_now = re.findall(r"Try now\s*:\s*\S", github_project_radar, re.IGNORECASE)
    github_owned_repos = [url for url in set(github_repo_links) if re.search(r"https?://github\.com/github/", url, re.IGNORECASE)]
    model_discovery = extract_section(notes, "Model Discovery Check")
    if ep_num >= 61:
        model_links = re.findall(r"https?://\S+", model_discovery)
        model_decisions = re.findall(r"Decision\s*:\s*\S", model_discovery, re.IGNORECASE)
        check("Model Discovery Check section exists",
              bool(model_discovery),
              hint="Future AgentStack drafts must include a separate model-discovery lane so major model drops are not missed.")
        check("Model Discovery Check includes primary-source links",
              len(model_links) >= 1,
              hint="Record official model announcements, model pages, docs, model cards, technical reports, or release pages.")
        check("Model Discovery Check records selection decisions",
              len(model_decisions) >= 1,
              hint="Each meaningful model candidate needs a selected/not-selected decision so model drops are not silently crowded out.")
        if re.search(r"\bMiniMax\s+M3\b", notes, re.IGNORECASE):
            m3_required_terms = [
                r"\bMSA\b|\bSparse Attention\b",
                r"\b1M\b|\bmillion-token\b|million token",
                r"\bmultimodal\b",
                r"\bMiniMax Code\b",
                r"\bAPI\b",
            ]
            missing_m3_terms = [term for term in m3_required_terms if not re.search(term, notes, re.IGNORECASE)]
            check("MiniMax M3 coverage includes core release mechanics",
                  len(missing_m3_terms) == 0,
                  hint="MiniMax M3 coverage should include MSA/sparse attention, 1M context, multimodality, MiniMax Code, and API availability.")
    if ep_num >= 57:
        check("GitHub Project Radar has at least three verified repos",
              len(set(github_repo_links)) >= 3,
              hint=f"Found {len(set(github_repo_links))} GitHub repo link(s). Future AgentStack drafts must scan adjacent projects around OpenClaw, Codex, Claude Code, Hermes, MCP/tooling, local agents, and model gateways.")
        check("GitHub Project Radar explains stack improvement angles",
              len(github_stack_angles) >= 3,
              hint=f"Found {len(github_stack_angles)} Stack improvement angle line(s). Each radar repo needs a concrete reason it could improve the agent stack.")
        check("GitHub Project Radar includes concrete try-now use cases",
              len(github_try_now) >= 3,
              hint=f"Found {len(github_try_now)} Try now line(s). GitHub projects should be usable/studiable repos, not only star counts.")
        check("GitHub Project Radar is not GitHub-the-company product coverage",
              len(github_owned_repos) == 0,
              hint="Do not count GitHub-owned product/news repos as this lane: " + ", ".join(github_owned_repos[:5]))

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



    # ── npm dist-tag / latest-vs-stable channel diffing is banned everywhere ──
    # Toby's standing rule (restated 2026-06-10 after EP067/EP068 violations):
    # coverage reports the stable release only — he runs stable, and the
    # latest-vs-stable diff conversation must never appear in any section,
    # including internal Release Coverage Check / Harness Version Reference
    # blocks (they leak into the next episode's research context).
    if ep_num >= 68:
        dist_tag_hits: list[str] = []
        for pat in [
            r"\bnpm latest\b",
            r"\bnpm stable\b",
            r"\bdist[- ]tags?\b",
            r"\b(?:stable|latest)\s+(?:track|channel)\b",
            r"\blatest\s+(?:vs\.?|versus)\s+stable\b",
            r"\bstable\s+(?:vs\.?|versus)\s+latest\b",
            r"\breceived via update\b",
            r"\bgap\s+(?:between|is)\s+(?:widening|narrowing)\b",
        ]:
            dist_tag_hits.extend(re.findall(pat, notes, re.IGNORECASE))
        check("No npm dist-tag / latest-vs-stable channel framing anywhere in the document",
              len(dist_tag_hits) == 0,
              hint="Standing rule: report the stable release only — never name or compare "
                   f"distribution channels/tags anywhere, internal sections included: {dist_tag_hits[:6]}")

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
        # EP068+: standing 10-topic slate (Toby, 2026-06-10) — one release readout
        # plus nine non-release stories is the daily format, not sprawl.
        non_release_cap = 9 if ep_num >= 68 else 3
        check("Release episode keeps extra stories tightly limited", non_release_story_count <= non_release_cap or runtime_exception,
              hint=f"Found {non_release_story_count} non-release stories (cap {non_release_cap}). Cut lower-priority stories before cutting release detail unless Toby explicitly asked to keep the existing builder stories and extend runtime.")

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
        max_non_release_stories = 10 if ep_num >= 68 else (6 if ep_num >= 55 else 5)
        check("Episode does not sprawl into too many low-priority stories", len(story_titles) <= max_non_release_stories, severity="WARNING",
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
