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


if __name__ == "__main__":
    tests = [
        ("catches_ep079_zcode_double_coverage", test_catches_ep079_zcode_double_coverage),
        ("version_normalization", test_version_normalization),
        ("distinct_stories_same_vendor_pass", test_distinct_stories_same_vendor_pass),
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
