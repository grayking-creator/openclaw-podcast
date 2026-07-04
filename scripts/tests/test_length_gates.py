#!/usr/bin/env python3
"""EP079 length-gate regression fence (locked 2026-07-04).

EP079 root cause chain: EP076 dropped the transcript floor at the owner's
request, the segment floor followed, and five days later the pipeline
delivered a 19-minute / 2,898-word / 10-story episode that was rejected as
"unacceptable". These tests pin every length-related constant and behavior
so a future "loosen it just for today" edit fails here, offline and fast,
instead of in a rejected morning episode.

Covers:
  1. STORY_COUNT default is >= 14.
  2. validate_story enforces the 270-320 (non-release) / 350-480 (release)
     segment band — rejects the EP079-style 160-word segment.
  3. fallback_story output CLEARS the same floors by construction (fallback
     output is never validated, so this is the only fence it has).
  4. check_episode.py transcript floor/ceiling are 4,800 / 5,400 (AST-read,
     no import — check_episode has import-time side effects).
  5. check_show_notes.py enforces >= 14 slate topics and the >= 4,200-word
     show-notes-block pre-audio gate for EP079+.
  6. generate_episode_transcript.py's prompt states the same floor/ceiling
     numbers check_episode.py enforces (prompt/QC drift burns repair rounds).

Run:
    python3 scripts/tests/test_length_gates.py
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # …/openclaw-podcast
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_show_notes as bsn  # noqa: E402

TRANSCRIPT_FLOOR = 4800
TRANSCRIPT_CEILING = 5400
SEG_FLOOR_NEWS = 270
SEG_CEILING_NEWS = 320
SEG_FLOOR_RELEASE = 350
STORY_FLOOR = 14


def _words(n: int) -> str:
    """n words of story-shaped prose (cycles a sentence, never one giant token)."""
    base = ("The release changes the runtime API surface that agent builders "
            "configure and deploy against in production stacks today. ").split()
    return " ".join(base[i % len(base)] for i in range(n))


def _story(seg_words: int) -> dict:
    return {
        "title": "Example runtime ships a new inference API surface",
        "summary": _words(60),
        "technical_depth_angle": _words(50),
        "actionability_angle": "Evaluate the change against a current workload.",
        "listener_hook": "A default surface agent builders rely on just moved.",
        "segment": _words(seg_words),
    }


def _ast_int_assign(path: Path, name: str) -> int:
    """Extract `name = <int literal>` from a script without importing it."""
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (isinstance(target, ast.Name) and target.id == name
                        and isinstance(node.value, ast.Constant)
                        and isinstance(node.value.value, int)):
                    return node.value.value
    raise AssertionError(f"could not find integer assignment {name!r} in {path.name}")


def test_story_count_floor():
    """The builder's default slate size must stay >= 14 (EP079 lock)."""
    assert bsn.STORY_COUNT >= STORY_FLOOR, (
        f"STORY_COUNT default is {bsn.STORY_COUNT}; the EP079 lock requires >= {STORY_FLOOR}"
    )


def test_validate_story_rejects_ep079_length_segment():
    """A 160-word segment (the EP079 pattern) must fail; the band must pass."""
    problems = bsn.validate_story(_story(160), set(), is_release=False)
    assert any("segment" in p for p in problems), (
        f"160-word segment passed validate_story: {problems}"
    )
    problems = bsn.validate_story(_story(290), set(), is_release=False)
    assert not any("segment must be" in p for p in problems), (
        f"in-band 290-word segment rejected: {problems}"
    )
    problems = bsn.validate_story(_story(600), set(), is_release=False)
    assert any("segment" in p for p in problems), (
        f"600-word drone segment passed validate_story: {problems}"
    )


def test_validate_story_release_floor():
    """Release stories carry the deeper 350-word floor."""
    problems = bsn.validate_story(_story(300), set(), is_release=True)
    assert any("segment must be" in p for p in problems), (
        f"300-word release segment passed the 350-word release floor: {problems}"
    )


def test_fallback_story_clears_floor_thin_source():
    """fallback_story output is NEVER validated (gen_validated returns it
    as-is), so it must clear the floor by construction — even from the
    thinnest possible source (title only, no summary, no lane detail)."""
    thin = {"title": "Runtime project ships an update", "summary": "", "extra": "",
            "url": "https://example.com/x"}
    for is_release, floor in ((False, SEG_FLOOR_NEWS), (True, SEG_FLOOR_RELEASE)):
        pkg = bsn.fallback_story(thin, is_release)
        seg_words = len(str(pkg["segment"]).split())
        assert seg_words >= floor, (
            f"fallback_story(is_release={is_release}) produced a {seg_words}-word "
            f"segment from a thin source; floor is {floor}. This is the exact "
            f"all-routes-down path that rebuilds the 19-minute EP079."
        )
        # And it must also validate cleanly end-to-end (except mechanism terms,
        # which research-kind sources are exempt from anyway).
        problems = [p for p in bsn.validate_story(pkg, set(), is_release)
                    if "mechanism" not in p]
        assert not any("segment must be" in p for p in problems), (
            f"fallback_story segment out of band: {problems}"
        )


def test_check_episode_floor_and_ceiling_constants():
    """The transcript hard band in check_episode.py stays 4,800-5,400."""
    path = SCRIPTS / "check_episode.py"
    floor = _ast_int_assign(path, "floor")
    ceiling = _ast_int_assign(path, "ceiling")
    assert floor == TRANSCRIPT_FLOOR, (
        f"check_episode.py floor is {floor}; the EP079 lock requires {TRANSCRIPT_FLOOR}. "
        f"Do not loosen the floor — add stories and deepen segments instead."
    )
    assert ceiling == TRANSCRIPT_CEILING, (
        f"check_episode.py ceiling is {ceiling}; the EP072 drone lock requires {TRANSCRIPT_CEILING}."
    )


def test_check_show_notes_gates_present():
    """check_show_notes.py must keep the 14-topic slate gate and the
    >= 4,200-word show-notes-block pre-audio gate for EP079+."""
    src = (SCRIPTS / "check_show_notes.py").read_text()
    assert "fourteen real topics" in src and ">= 14" in src, (
        "the EP079+ 14-topic slate gate is missing from check_show_notes.py"
    )
    assert "4200" in src.replace(",", ""), (
        "the EP079+ >=4,200-word show-notes-block pre-audio gate is missing "
        "from check_show_notes.py"
    )


def test_transcript_prompt_matches_qc_band():
    """The transcript generator's prompt must state the same hard numbers
    check_episode.py enforces — drift between prompt and QC burns repair
    rounds every morning."""
    src = (SCRIPTS / "generate_episode_transcript.py").read_text()
    for token in ("4,800", "5,400"):
        assert token in src, (
            f"generate_episode_transcript.py prompt no longer states {token} — "
            f"it must match check_episode.py's hard band"
        )


if __name__ == "__main__":
    tests = [
        ("story_count_floor", test_story_count_floor),
        ("validate_story_rejects_ep079_length_segment",
         test_validate_story_rejects_ep079_length_segment),
        ("validate_story_release_floor", test_validate_story_release_floor),
        ("fallback_story_clears_floor_thin_source",
         test_fallback_story_clears_floor_thin_source),
        ("check_episode_floor_and_ceiling_constants",
         test_check_episode_floor_and_ceiling_constants),
        ("check_show_notes_gates_present", test_check_show_notes_gates_present),
        ("transcript_prompt_matches_qc_band", test_transcript_prompt_matches_qc_band),
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
