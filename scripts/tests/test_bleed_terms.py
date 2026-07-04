#!/usr/bin/env python3
"""
EP075 bleed-term fixtures (locked 2026-06-27, extended 2026-06-28).

Two related bleed classes are covered:

  1. EP075_PRODUCTION_PROCESS_BLEED — narration that disclosed how the
     episode was researched/built ("the model discovery scan",
     "scanned lanes", "not selected entries are grouped"). Banned
     permanently after the 2026-06-27 EP075 review audio.

  2. EP075_LISTENER_ADVICE_BLEED — listener-facing advice the EP075
     rewrite introduced that tells the listener to "pin" to a specific
     model or version, or treats ephemeral versions like GPT-5.6 as
     pinnable targets. Banned permanently after Toby's 2026-06-28
     feedback. The runtime already falls back automatically when a
     pinned model is removed (e.g. Fable -> Opus) — it does NOT crash —
     so the pin advice is wrong on the facts AND unhelpful.

This test loads both fixtures and asserts that every line is flagged by
the matching `*_patterns` block in `check_episode.py`. It also asserts
the union of expected patterns is present in the live pattern list (so
a future refactor that drops a critical pattern triggers a failure
here, not in production).

Run:
    python3 scripts/tests/test_bleed_terms.py
Exit:
    0  all bleed phrases were flagged
    1  at least one bleed phrase slipped through, or a critical pattern
       is missing from check_episode.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR.parent
CHECK_EPISODE = SCRIPTS_DIR / "check_episode.py"

# These are the bleed phrases that appeared in the EP075 transcript's
# "Model Discovery Check" close. Every one must be flagged by
# internal_impl_patterns.
EP075_BLEED_LINES = [
    "The model discovery scan across major OpenRouter provider lanes did not surface a new or materially updated model candidate selected for deeper coverage.",
    "The practical interpretation is restraint: no model was promoted just for churn, and the main model-adjacent stories are coming from infrastructure, research, and applied deployments rather than a fresh leaderboard entrant.",
    "Not selected entries are grouped as one read: the scanned lanes produced no new model candidate that changed the build surface enough to displace the release, chip, agent-research, or GPT-5 Pro science stories.",
    "There were no new stable release candidates selected from the fetched release window.",
    "The daily release check returned no model promotion this cycle.",
    "Model not selected for the radar because of churn in the current release cycle.",
    "There were no candidates selected for the build this run.",
]

# Each line is expected to be flagged by AT LEAST one of these patterns.
# The mapping tracks which pattern we expect to fire on which line so a
# future refactor that drops a pattern that was carrying a particular
# line triggers a specific failure (and a useful diagnostic).
EXPECTED_HITS_PER_LINE = [
    # Line 1: provider lanes + model discovery scan
    {r"\bmodel discovery scan\b", r"\bprovider lanes\b",
     r"\bno new (?:or materially updated )?model candidates?\b"},
    # Line 2: no model was promoted + promoted just for churn
    {r"\bno model was promoted\b", r"\bpromoted just for churn\b"},
    # Line 3: not selected entries + scanned lanes
    {r"\bnot selected entries\b", r"\bscanned lanes\b",
     r"\bnot selected\b[^.\n]{0,80}\bgrouped\b",
     r"\bno new (?:or materially updated )?model candidates?\b"},
    # Line 4: no new stable .* candidate + selected from the fetched + release window
    {r"\bno new stable .*candidate\b", r"\bselected from the fetched\b",
     r"\brelease window\b"},
    # Line 5: daily release check
    {r"\bdaily release check\b"},
    # Line 6: current release cycle + model not selected
    {r"\bcurrent release cycle\b", r"\bmodel (?:was |is )?not (?:promoted|selected|featured|covered)\b"},
    # Line 7: no candidate was selected
    {r"\bno (?:new )?candidates? (?:was |were |is |are )?(?:not )?(?:selected|featured|covered|promoted)\b"},
]


# Fixture 2 — EP075 listener-advice bleed (locked 2026-06-28).
# Phrases the rewrite slipped in that told the listener to pin to a
# specific model/version, or treated ephemeral version numbers as
# pinnable targets. Every one must be flagged by
# model_pinning_advice_patterns. None of these should ever appear in
# any future episode.
EP075_LISTENER_ADVICE_BLEED_LINES = [
    # The exact lines from EP075 that triggered the lockdown:
    "[ALLOY]: The terminal-based AI coding agent Claude Code .181 is also in the stable release set, giving builders a new pinned command-line surface for coding-agent workflows.",
    "[NOVA]: Claude Code .181 rounds out the stable release set for builders who pin the terminal-based AI coding agent in local and enterprise workflows.",
    "[ALLOY]: Claude Code .181 gives builders a fresh stable pin for terminal-based AI coding work, which matters anywhere reproducibility beats chasing every small change.",
    # Hypothetical constructions the rewrite almost shipped (and the
    # next rewrite would invent again if we don't lock them):
    "If you had pinned Fable to your coding-agent config, whenever it was removed you would have just went back to the last model.",
    "It didn't actually break; it just defaulted back to Opus when Fable was removed.",
    "It didn't actually crash. The runtime fell back to the previous model automatically.",
    "You can pin to GPT-5.6 if your provider exposes it.",
    "Teams already splitting work should plan around GPT-5.6 as the new default.",
    "5.6 is available to trusted partners, so pin to 5.6 once the gate lifts.",
    "Builders should pin a stable release of the terminal-based AI coding agent for reproducibility.",
    "We pinned Claude Code .181 to keep coding-agent behavior stable across the team.",
]

# Each line in fixture 2 must be flagged by at least one of these
# expected patterns in model_pinning_advice_patterns.
EP075_LISTENER_ADVICE_EXPECTED_HITS = [
    # Line 1: "new pinned command-line surface"
    {r"\b(?:a |the )?pinned (?:command[- ]line|cli|surface|release|target|model|behavior)\b",
     r"\bnew (?:stable )?pin(?:ning|s)?\b"},
    # Line 2: "pin the terminal-based AI coding agent"
    {r"\bpin(?:ning|ned|s)? (?:[A-Za-z][A-Za-z0-9 .'_-]{0,40} )?(?:terminal[- ]based )?(?:AI )?coding[- ]agent\b"},
    # Line 3: "fresh stable pin"
    {r"\bfresh stable pin\b",
     r"\bpin(?:ning|ned|s)? (?:for|of) (?:terminal|reproducibility|repeatable|stability|stable behavior)\b"},
    # Line 4: "If you had pinned ... went back to the last model"
    {r"\bif you (?:had |have )?pin(?:ned)?\b",
     r"\bfell back to (?:the |a )?(?:last|previous|prior) model\b"},
    # Line 5: "didn't actually break ... defaulted back to Opus"
    {r"\bdefaulted back (?:to|onto) [A-Za-z][A-Za-z0-9 .'_-]{0,40}\b"},
    # Line 6: "didn't actually crash ... fell back to the previous model"
    {r"\b(?:it )?didn'?t (?:actually )?crash\b",
     r"\bfell back to (?:the |a )?(?:last|previous|prior) model\b"},
    # Line 7: "you can pin to GPT-5.6"
    {r"\b(?:you|builders?|teams?|users?) (?:can|should|could|may|might|need to|have to|want to) pin\b",
     r"\bpin(?:ning|ned|s)? (?:[A-Za-z][A-Za-z0-9 .'_-]{0,20} )?5\.6\b"},
    # Line 8: "plan around GPT-5.6"
    {r"\bplan(?:ning)? around (?:GPT[- ]?5\.6|GPT[- ]?5|Opus|Sonnet|Haiku)\b"},
    # Line 9: "5.6 is available ... pin to 5.6"
    {r"\b5\.6 (?:is |as )?(?:available|reachable|pinnable|stable|shipped)\b",
     r"\bpin(?:ning|ned|s)? (?:[A-Za-z][A-Za-z0-9 .'_-]{0,20} )?5\.6\b"},
    # Line 10: "should pin ... terminal-based AI coding agent ... reproducibility"
    {r"\bpin(?:ning|ned|s)? (?:[A-Za-z][A-Za-z0-9 .'_-]{0,40} )?(?:terminal[- ]based )?(?:AI )?coding[- ]agent\b",
     r"\bpin(?:ning|ned|s)? (?:for|of) (?:terminal|reproducibility|repeatable|stability|stable behavior)\b"},
    # Line 11: "pinned Claude Code .181"
    {r"\bpin(?:ning|ned|s)? (?:[A-Za-z][A-Za-z0-9 .'_-]{0,30} )?(?:claude code|codex|openclaw|hermes)\b"},
]


def load_internal_impl_patterns() -> list[str]:
    """Pull the internal_impl_patterns list out of check_episode.py source.

    We deliberately avoid `import check_episode` because the file has
    side effects on import (writes artifacts, etc.). We use Python's AST
    to extract the string literals from the list assignment — much more
    reliable than regex over the source text.
    """
    import ast
    src = CHECK_EPISODE.read_text()
    tree = ast.parse(src, filename=str(CHECK_EPISODE))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "internal_impl_patterns":
                    if isinstance(node.value, ast.List):
                        patterns: list[str] = []
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                patterns.append(elt.value)
                        if patterns:
                            return patterns
    raise SystemExit("could not locate internal_impl_patterns in check_episode.py")


def load_model_pinning_advice_patterns() -> list[str]:
    """Pull the model_pinning_advice_patterns list out of check_episode.py.

    Same approach as load_internal_impl_patterns — AST walk to find the
    list assignment, no `import check_episode`.
    """
    import ast
    src = CHECK_EPISODE.read_text()
    tree = ast.parse(src, filename=str(CHECK_EPISODE))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "model_pinning_advice_patterns":
                    if isinstance(node.value, ast.List):
                        patterns: list[str] = []
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                patterns.append(elt.value)
                        if patterns:
                            return patterns
    raise SystemExit("could not locate model_pinning_advice_patterns in check_episode.py")


def run_fixture(
    fixture_name: str,
    bleed_lines: list[str],
    expected_hits_per_line: list[set[str]],
    patterns: list[str],
) -> list[str]:
    """Run a single bleed-term fixture against its pattern list.

    Returns a list of failure strings. Empty list = the fixture passed.
    """
    compiled = [(p, re.compile(p, re.IGNORECASE)) for p in patterns]
    failures: list[str] = []

    if len(bleed_lines) != len(expected_hits_per_line):
        failures.append(
            f"FAIL ({fixture_name} misconfigured — bleed_lines and "
            f"expected_hits_per_line differ in length)"
        )
        return failures

    live_patterns = {p for p, _ in compiled}

    for idx, (line, expected) in enumerate(zip(bleed_lines, expected_hits_per_line), 1):
        fired = [p for p, rx in compiled if rx.search(line)]
        if not fired:
            failures.append(f"[{fixture_name}] NO HIT (line {idx}): {line[:80]!r}…")
            continue
        # Refactor guard: every pattern in the expected set must still
        # exist in the live pattern list. Other patterns may have caught
        # the line, but the *intent* of the expected pattern must remain
        # expressed somewhere — otherwise a future refactor that
        # accidentally drops the intent-specific pattern won't surface
        # as a test failure.
        for pat in expected:
            if pat not in live_patterns:
                failures.append(
                    f"[{fixture_name}] CRITICAL pattern missing from "
                    f"check_episode.py: {pat!r} (line {idx}: {line[:50]!r} "
                    f"was caught by something else, but the intent of "
                    f"{pat!r} is no longer expressed)"
                )

    return failures


def main() -> int:
    failures: list[str] = []

    # Fixture 1 — production-process bleed (locked 2026-06-27)
    failures.extend(run_fixture(
        fixture_name="EP075 production-process bleed",
        bleed_lines=EP075_BLEED_LINES,
        expected_hits_per_line=EXPECTED_HITS_PER_LINE,
        patterns=load_internal_impl_patterns(),
    ))

    # Fixture 2 — listener-advice bleed (locked 2026-06-28)
    failures.extend(run_fixture(
        fixture_name="EP075 listener-advice bleed",
        bleed_lines=EP075_LISTENER_ADVICE_BLEED_LINES,
        expected_hits_per_line=EP075_LISTENER_ADVICE_EXPECTED_HITS,
        patterns=load_model_pinning_advice_patterns(),
    ))

    if failures:
        print("EP075 bleed-term fixture: FAIL")
        for f in failures:
            print(f"  • {f}")
        return 1

    total_lines = len(EP075_BLEED_LINES) + len(EP075_LISTENER_ADVICE_BLEED_LINES)
    print(
        f"EP075 bleed-term fixture: PASS "
        f"({len(EP075_BLEED_LINES)} production-process bleed lines + "
        f"{len(EP075_LISTENER_ADVICE_BLEED_LINES)} listener-advice bleed "
        f"lines = {total_lines} total flagged; refactor-guard patterns "
        f"present in check_episode.py)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
