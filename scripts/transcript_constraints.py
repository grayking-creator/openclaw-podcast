#!/usr/bin/env python3
"""Shared transcript length, segment, and spoken-lane constraints.

The transcript prompt, repair controller, and final QC all import this module
so the definition of a release segment and the hard word band cannot drift.
This module is intentionally side-effect free; offline regression tests import
it directly.
"""

from __future__ import annotations

import re
from typing import Any


TRANSCRIPT_FLOOR = 4_800
TRANSCRIPT_CEILING = 5_400
TRANSCRIPT_TARGET = 5_100

NON_RELEASE_SEGMENT_CEILING = 320
RELEASE_SEGMENT_CEILING = 480
RESEARCH_SEGMENT_CEILING = 190

# This is the exact title classifier used by final QC. A paper, model, product,
# or dataset being published today does not make it a release-budget segment.
# The wider release allowance is only for the named agent-harness readout.
RELEASE_SEGMENT_TITLE_MARKERS = (
    "release readout",
    "agent stack release",
    "harness release",
)
HARNESS_TITLE_MARKERS = (
    "openclaw",
    "codex",
    "claude code",
    "hermes",
    "antigravity",
)

REQUIRED_SPOKEN_LANES = (
    "GitHub Project Radar",
    "Model Discovery Check",
    "Local LLM Spotlight",
    "Extra Research Candidates",
)

NO_SELECTED_MODEL_NATURAL_BEAT = (
    "Model progress today came through serving, evaluation results, and domain "
    "adaptation rather than a new general-purpose name."
)

_TRANSCRIPT_BOUNDARY_RE = re.compile(
    r"^##\s+(?:\[\d{2}:\d{2}(?:[–-]\d{2}:\d{2})?\]\s*.+"
    r"|(?:Local LLM Spotlight"
    r"|GitHub Project Radar"
    r"|Practical Queue"
    r"|Model Discovery Check"
    r"|Extra Research Candidates?)(?:\s*:.*)?"
    r")\s*$",
    re.MULTILINE,
)


def markdown_section(text: str, heading: str) -> str:
    """Return a level-two markdown section body, or an empty string."""
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(.+?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def is_release_segment_title(title: str) -> bool:
    lowered = title.lower()
    if any(marker in lowered for marker in RELEASE_SEGMENT_TITLE_MARKERS):
        return True
    return (any(marker in lowered for marker in HARNESS_TITLE_MARKERS)
            and bool(re.search(r"\b(?:release|ships?|version|update)\b", lowered)))


def is_research_segment_title(title: str) -> bool:
    return bool(re.search(r"\bresearch digest\s*:", title, re.IGNORECASE))


def segment_word_ceiling(title: str) -> int:
    if is_release_segment_title(title):
        return RELEASE_SEGMENT_CEILING
    if is_research_segment_title(title):
        return RESEARCH_SEGMENT_CEILING
    return NON_RELEASE_SEGMENT_CEILING


def transcript_segments(content: str) -> list[tuple[str, str, str]]:
    """Return ``(timestamp, title, body)`` for QC-counted transcript blocks."""
    matches = list(_TRANSCRIPT_BOUNDARY_RE.finditer(content))
    segments: list[tuple[str, str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        title = match.group(0).strip().lstrip("# ").strip()
        timestamp_match = re.match(r"\[(\d{2}:\d{2}(?:[–-]\d{2}:\d{2})?)\]", title)
        timestamp = timestamp_match.group(1) if timestamp_match else ""
        segments.append((timestamp, title, content[match.end():end].strip()))
    return segments


def transcript_lane_word_counts(content: str) -> dict[str, int]:
    """Count words in the computed-budget lanes using the shared parser.

    The opening excludes markdown headings because the episode title is not
    spoken. Segment bodies intentionally use the same whitespace word count as
    final QC and include speaker/pacing tokens, keeping lane totals auditable
    against the global transcript count.
    """
    matches = list(_TRANSCRIPT_BOUNDARY_RE.finditer(content))
    opening = content[:matches[0].start()] if matches else content
    opening = re.sub(r"^#{1,3}\s+.*$", "", opening, flags=re.MULTILINE)
    counts = {
        "opening": len(opening.split()),
        "radar": 0,
        "model_discovery": 0,
        "spotlight": 0,
        "extras": 0,
        "queue_outro": 0,
    }
    for _timestamp, title, body in transcript_segments(content):
        heading = re.sub(
            r"^\[\d{2}:\d{2}(?:[–-]\d{2}:\d{2})?\]\s*",
            "",
            title,
        )
        words = len(body.split())
        if re.match(r"GitHub Project Radar\b", heading, re.IGNORECASE):
            counts["radar"] += words
        elif re.match(r"Model Discovery Check\b", heading, re.IGNORECASE):
            counts["model_discovery"] += words
        elif re.match(r"Local LLM Spotlight\b", heading, re.IGNORECASE):
            counts["spotlight"] += words
        elif re.match(r"Extra Research Candidates?\b", heading, re.IGNORECASE):
            counts["extras"] += words
        elif re.match(r"Practical Queue\b", heading, re.IGNORECASE):
            counts["queue_outro"] += words
    return counts


def segment_overages(content: str) -> list[dict[str, Any]]:
    overages: list[dict[str, Any]] = []
    for index, (timestamp, title, body) in enumerate(transcript_segments(content), 1):
        body_no_label = re.sub(r"^\[PAUSE\]\s*", "", body.strip())
        words = len(body_no_label.split())
        ceiling = segment_word_ceiling(title)
        if words > ceiling:
            overages.append({
                "index": index,
                "timestamp": timestamp,
                "title": title,
                "words": words,
                "ceiling": ceiling,
                "overage": words - ceiling,
                "release": is_release_segment_title(title),
            })
    return overages


def story_titles_from_show_notes(show_notes: str) -> list[str]:
    slate = markdown_section(show_notes, "Story Slate")
    return [
        match.group(1).strip()
        for match in re.finditer(r"^\d+\.\s+\*\*(.+?)\*\*", slate, re.MULTILINE)
    ]


def bullet_labels(show_notes: str, heading: str) -> list[str]:
    return re.findall(
        r"^-\s+\*\*([^*]+)\*\*",
        markdown_section(show_notes, heading),
        re.MULTILINE,
    )


def selected_model_labels(show_notes: str) -> list[str]:
    """Return Model Discovery labels whose own bullet says Decision: Selected."""
    section = markdown_section(show_notes, "Model Discovery Check")
    entries = re.split(r"(?=^-\s+\*\*)", section, flags=re.MULTILINE)
    labels: list[str] = []
    for entry in entries:
        label = re.match(r"^-\s+\*\*([^*]+)\*\*", entry)
        if label and re.search(r"\bDecision:\s*Selected\b", entry, re.IGNORECASE):
            labels.append(label.group(1).strip())
    return labels


def required_spoken_lanes(show_notes: str) -> list[str]:
    return [heading for heading in REQUIRED_SPOKEN_LANES
            if markdown_section(show_notes, heading)]


def missing_spoken_lanes(transcript: str, show_notes: str) -> list[str]:
    missing: list[str] = []
    for heading in required_spoken_lanes(show_notes):
        spoken_heading = (r"Extra Research Candidates?"
                          if heading == "Extra Research Candidates"
                          else re.escape(heading))
        if not re.search(
            rf"^#{{1,3}}\s+(?:\[[^\]]+\]\s*)?{spoken_heading}(?:\s*:.*)?\s*$",
            transcript,
            re.MULTILINE | re.IGNORECASE,
        ):
            missing.append(heading)
    return missing


def build_episode_budget_ledger(show_notes: str) -> dict[str, Any]:
    """Compute a prompt ledger that fits a dense fourteen-story show.

    The ledger targets 5,100 words, leaving 300 words of safety below final QC's
    5,400 ceiling. The 4,800 floor remains a final hard gate. Story targets are
    adjusted for the actual slate and selected-model count, while every hard
    per-segment cap remains unchanged.
    """
    titles = story_titles_from_show_notes(show_notes)
    release_count = sum(is_release_segment_title(title) for title in titles)
    research_count = sum(is_research_segment_title(title) for title in titles)
    standard_count = len(titles) - release_count - research_count
    selected_models = selected_model_labels(show_notes)
    radar_count = min(3, len(bullet_labels(show_notes, "GitHub Project Radar")))
    extra_count = min(3, len(bullet_labels(show_notes, "Extra Research Candidates")))

    lanes = {
        "opening": {"target": 160, "ceiling": 200},
        "radar": {
            "count": radar_count,
            "per_item_target": 110,
            "target": radar_count * 110,
            "ceiling": radar_count * 140,
        },
        "model_discovery": {
            "selected_count": len(selected_models),
            "target": len(selected_models) * 70 if selected_models else 55,
            "ceiling": len(selected_models) * 80 if selected_models else 80,
            "no_selected": not selected_models,
        },
        "spotlight": {"target": 120, "ceiling": 140},
        "extras": {
            "count": extra_count,
            "per_item_target": 70,
            "target": extra_count * 70,
            "ceiling": extra_count * 80,
        },
        "queue_outro": {"target": 140, "ceiling": 160},
    }
    lane_target = sum(lane["target"] for lane in lanes.values())
    release_target = 400
    research_target = 165
    remaining_story_words = (TRANSCRIPT_TARGET - lane_target
                             - release_count * release_target
                             - research_count * research_target)
    if standard_count:
        non_release_target = round(remaining_story_words / standard_count)
        non_release_target = max(270, min(305, non_release_target))
    else:
        non_release_target = 0

    story_budgets: list[dict[str, Any]] = []
    for index, title in enumerate(titles, 1):
        release = is_release_segment_title(title)
        research = is_research_segment_title(title)
        story_budgets.append({
            "index": index,
            "title": title,
            "release": release,
            "research": research,
            "target_min": 380 if release else (130 if research else 270),
            "target_max": 420 if release else (180 if research else non_release_target),
            "ceiling": (RELEASE_SEGMENT_CEILING if release else
                        RESEARCH_SEGMENT_CEILING if research else
                        NON_RELEASE_SEGMENT_CEILING),
        })

    estimated_target = lane_target + sum(item["target_max"] for item in story_budgets)
    return {
        "floor": TRANSCRIPT_FLOOR,
        "ceiling": TRANSCRIPT_CEILING,
        "target": TRANSCRIPT_TARGET,
        "story_budgets": story_budgets,
        "lanes": lanes,
        "selected_models": selected_models,
        "estimated_target": estimated_target,
    }


def format_episode_budget_ledger(show_notes: str) -> str:
    ledger = build_episode_budget_ledger(show_notes)
    lines = [
        "EPISODE WORD-BUDGET LEDGER (hard; computed from this slate):",
        f"- Final QC band: {ledger['floor']:,}-{ledger['ceiling']:,} words. "
        f"Draft toward {ledger['target']:,}; the safety buffer is intentional.",
        f"- Opening: target {ledger['lanes']['opening']['target']} words, "
        f"hard cap {ledger['lanes']['opening']['ceiling']}.",
        "- RELEASE for this ledger means only a title matched by the agent-harness "
        "release classifier: an explicit release readout, or a named harness title "
        "that also says release, ships, version, or update. A `Research digest:` "
        "title targets 130-180 words and has a 190-word hard cap. Other papers, "
        "models, products, and datasets are NON-RELEASE and keep the 320-word cap. "
        "A paper, model, product, or dataset published today is not automatically "
        "an agent-harness release.",
    ]
    for story in ledger["story_budgets"]:
        kind = ("RELEASE" if story["release"] else
                "RESEARCH DIGEST" if story.get("research") else
                "NON-RELEASE")
        lines.append(
            f"- Story {story['index']} ({kind}) \"{story['title']}\": target "
            f"{story['target_min']}-{story['target_max']} words; hard cap "
            f"{story['ceiling']}."
        )
    radar = ledger["lanes"]["radar"]
    lines.append(
        f"- GitHub Project Radar: {radar['count']} repo beats at about "
        f"{radar['per_item_target']} words each; hard total cap {radar['ceiling']}."
    )
    model = ledger["lanes"]["model_discovery"]
    if model["no_selected"]:
        lines.append(
            "- Model Discovery Check: the heading and one natural 20-80 word spoken "
            "beat are required. State the market read directly, for example: "
            f"\"{NO_SELECTED_MODEL_NATURAL_BEAT}\" Never mention "
            "scanning, candidates, selection, research, the build, or internal process."
        )
    else:
        lines.append(
            f"- Model Discovery Check: {model['selected_count']} selected model beat(s), "
            f"50-80 words each; hard total cap {model['ceiling']}."
        )
    extras = ledger["lanes"]["extras"]
    lines.extend([
        f"- Local LLM Spotlight: target {ledger['lanes']['spotlight']['target']} words; "
        f"hard cap {ledger['lanes']['spotlight']['ceiling']}.",
        f"- Extra Research Candidates: name all {extras['count']} in one combined beat, "
        f"about {extras['per_item_target']} words each; hard total cap {extras['ceiling']}.",
        f"- Practical queue plus outro: target {ledger['lanes']['queue_outro']['target']} "
        f"words; hard combined cap {ledger['lanes']['queue_outro']['ceiling']}.",
        f"- Computed target with this slate: about {ledger['estimated_target']:,} words. "
        "If a section runs long, compress it toward its target minimum; never borrow "
        "past another section's hard cap.",
    ])
    return "\n".join(lines)


def lane_budget_overages(content: str, show_notes: str) -> list[dict[str, int | str]]:
    """Return computed-lane totals that exceed the same ledger shown to models."""
    ledger = build_episode_budget_ledger(show_notes)
    counts = transcript_lane_word_counts(content)
    overages: list[dict[str, int | str]] = []
    for lane, words in counts.items():
        ceiling = int(ledger["lanes"][lane]["ceiling"])
        if words > ceiling:
            overages.append({
                "lane": lane,
                "words": words,
                "ceiling": ceiling,
                "overage": words - ceiling,
            })
    return overages


def candidate_constraint_score(
    transcript: str,
    show_notes: str,
    failed_check_count: int,
) -> tuple[int, dict[str, int]]:
    """Return a repair-cost score plus auditable component metrics.

    Word-distance and every over-budget segment are charged by their actual
    overage. A missing mandatory lane costs 600 points (roughly the cost of
    reconstructing and revalidating it), and each remaining failed check costs
    100. Lower is the safer rescue candidate.
    """
    words = len(transcript.split())
    global_distance = max(TRANSCRIPT_FLOOR - words, words - TRANSCRIPT_CEILING, 0)
    per_segment_overage = sum(item["overage"] for item in segment_overages(transcript))
    missing_lanes = len(missing_spoken_lanes(transcript, show_notes))
    score = (
        global_distance
        + per_segment_overage
        + missing_lanes * 600
        + failed_check_count * 100
    )
    return score, {
        "words": words,
        "global_distance": global_distance,
        "per_segment_overage": per_segment_overage,
        "missing_lanes": missing_lanes,
        "failed_checks": failed_check_count,
    }
