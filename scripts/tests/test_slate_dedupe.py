#!/usr/bin/env python3
"""Within-slate duplicate-topic regression fence (locked 2026-07-04).

EP079 regen incident: the same ZCode launch entered the 14-story slate as
two separate stories, sourced from two different HN submissions ("ZCode –
Harness for GLM-5.2" and "ZCode: Claude Code from the Makers of GLM"). The
classic 3-shared-token dedupe missed it because 'GLM-5.2' and 'GLM'
tokenize differently, leaving only 'zcode' shared.

The fix is `titles_are_same_topic()` in check_show_notes.py (normalized
version tokens + shared lead-subject rule), used by the builder's pool
dedupe, the QC gate's within-slate check, and the repair loop's backfill.
This test pins the rule against the real EP079 slate: it must flag exactly
the ZCode pair and nothing else.

Run:
    python3 scripts/tests/test_slate_dedupe.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_show_notes as qc  # noqa: E402

# The real EP079 regen slate (2026-07-04) that shipped the duplicate.
EP079_SLATE = [
    "Agent Stack Release Readout: Hermes Agent v2026.7.1; Claude Code CLI 2.1.193",
    "Z.ai Ships ZCode, a GLM-5.2 Coding Harness with Anthropic-Compatible Tools",
    "Kimi K2.7 Code lands as a GA model option inside GitHub Copilot",
    "Jamesob's Local LLM Guide Hits HN Front Page",
    "Alibaba reportedly bans Claude Code over backdoor concerns",
    "ZCode Lands: z.ai Ships a Claude Code-Style Agent for GLM Models",
    "Mistral ships Leanstral 1.5, frames release as 'abundance for all'",
    "The Safari MCP server for web developers",
    "WebBrain Brings Local-First Browser Agents to Chrome and Firefox",
    "RECONTEXT teaches models to reread their own long context",
    "Snorkel Launches Senior SWE-Bench to Grade Agents as Senior Engineers",
    "ghealth: Open-Source CLI Wraps Google Health API for Agents",
    "Program-as-Weights Paper Turns Natural Language Into Neural Functions",
    "Reasoning LLM Lifts Speaker Recognition on a 532K-Line Drama Benchmark",
]


def _dup_pairs(titles: list[str]) -> list[tuple[int, int]]:
    out = []
    for j in range(1, len(titles)):
        for i in range(j):
            if qc.titles_are_same_topic(titles[i], titles[j]):
                out.append((i + 1, j + 1))
    return out


def test_catches_ep079_zcode_double_coverage():
    """The real EP079 slate must flag exactly the ZCode pair (2, 6)."""
    pairs = _dup_pairs(EP079_SLATE)
    assert pairs == [(2, 6)], (
        f"expected exactly the ZCode duplicate pair (2, 6); got {pairs}. "
        f"Fewer means the dedupe regressed; more means it grew false positives."
    )


def test_version_normalization():
    """'glm-5.2' and 'glm' must compare equal after normalization; short
    bases like 'k2.7' must be left alone (stripping them would over-merge)."""
    assert qc.normalize_product_tokens({"glm-5.2"}) == {"glm"}
    assert qc.normalize_product_tokens({"k2.7"}) == {"k2.7"}
    assert qc.normalize_product_tokens({"leanstral"}) == {"leanstral"}


def test_distinct_stories_same_vendor_pass():
    """Different stories about the same vendor must NOT merge — vendor names
    are stopworded, so only genuine product-subject overlap dedupes."""
    assert not qc.titles_are_same_topic(
        "Alibaba reportedly bans Claude Code over backdoor concerns",
        "Kimi K2.7 Code lands as a GA model option inside GitHub Copilot")
    assert not qc.titles_are_same_topic(
        "Mistral ships Leanstral 1.5, frames release as 'abundance for all'",
        "Mistral AI raises new funding round for EU datacenter build-out")


def test_ep088_generic_headline_overlap_passes():
    """Distribution/context phrasing and section labels are not products."""
    assert not qc.titles_are_same_topic(
        "Meta's Muse Spark 1.1 lands on OpenRouter with a 1M-token context window",
        "Kimi K3 Lands on OpenRouter With a Million-Token Context Window")
    assert not qc.titles_are_same_topic(
        "Research digest: AI coding assistants still can't read your bug screenshots",
        "Research digest: Search agents that stop getting stuck in loops")


def test_distinct_mcp_products_with_generic_assistant_wording_pass():
    """Generic headline verbs and audience nouns cannot make unrelated MCP
    products look like the same launch."""
    assert not qc.titles_are_same_topic(
        "Unity MCP v10.1.0 Gives AI Assistants Direct Editor Access",
        "codebase-memory-mcp gives AI coding assistants a persistent memory layer")


def test_codex_claude_only_release_readout_is_exempt_from_prior_dedupe():
    """A release readout remains slot-one infrastructure even when no
    OpenClaw/Hermes GitHub tag exists for ``extract_release_tags`` to find."""
    titles = [
        "Agent Stack Release Readout: OpenAI Codex rust-v0.144.5; Claude Code CLI 2.1.205",
        "Kimi K3 Lands on OpenRouter With a Million-Token Context",
    ]
    assert qc.story_titles_for_prior_repeat_check(titles, []) == titles[1:]
    assert qc.story_titles_for_prior_repeat_check(titles, ["v2026.7.2"]) == titles[1:]


def test_non_release_story_one_still_gets_prior_dedupe():
    titles = ["OpenAI launches a new coding-agent safety filter"]
    assert qc.story_titles_for_prior_repeat_check(titles, []) == titles


if __name__ == "__main__":
    tests = [
        ("catches_ep079_zcode_double_coverage", test_catches_ep079_zcode_double_coverage),
        ("version_normalization", test_version_normalization),
        ("distinct_stories_same_vendor_pass", test_distinct_stories_same_vendor_pass),
        ("ep088_generic_headline_overlap_passes",
         test_ep088_generic_headline_overlap_passes),
        ("distinct_mcp_products_with_generic_assistant_wording_pass",
         test_distinct_mcp_products_with_generic_assistant_wording_pass),
        ("codex_claude_only_release_readout_is_exempt_from_prior_dedupe",
         test_codex_claude_only_release_readout_is_exempt_from_prior_dedupe),
        ("non_release_story_one_still_gets_prior_dedupe",
         test_non_release_story_one_still_gets_prior_dedupe),
    ]
    passed = failed = 0
    for name, fn in tests:
        print(f"\n[test] {name}")
        try:
            fn()
            passed += 1
            print("  ✅ PASS")
        except AssertionError as e:
            failed += 1
            print(f"  ❌ FAIL: {e}")
        except Exception as e:
            failed += 1
            print(f"  ❌ ERROR: {type(e).__name__}: {e}")
    print(f"\n{'=' * 60}")
    print(f"{passed}/{len(tests)} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
