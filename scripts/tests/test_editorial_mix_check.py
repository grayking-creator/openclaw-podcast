#!/usr/bin/env python3
"""Focused regression tests for the EP087+ editorial-mix QC gate."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_show_notes as qc  # noqa: E402


PASSING_MIX = {
    "flagship_products": 2,
    "builder_projects": 3,
    "local_ai": 2,
    "hardware_compute": 2,
    "policy_regulation": 1,
    "research": 2,
}


def _notes(mix: dict[str, object] | None, *, extra_lines: list[str] | None = None) -> str:
    if mix is None:
        return "# AgentStack Daily\n\n## Story Slate\nPlaceholder\n"
    lines = [f"- {key}: {value}" for key, value in mix.items()]
    lines.extend(extra_lines or [])
    return (
        "# AgentStack Daily\n\n"
        "## Editorial Mix Check\n"
        + "\n".join(lines)
        + "\n\n## Story Slate\nPlaceholder\n"
    )


def test_gate_starts_at_ep087() -> None:
    assert qc.editorial_mix_errors(_notes(None), 86) == []
    errors = qc.editorial_mix_errors(_notes(None), 87)
    assert any("missing" in error.lower() for error in errors), errors


def test_exact_thresholds_pass() -> None:
    assert qc.editorial_mix_errors(_notes(PASSING_MIX), 87) == []
    assert qc.editorial_mix_errors(
        _notes(PASSING_MIX, extra_lines=["---"]), 87
    ) == []


def test_each_minimum_is_hard() -> None:
    minima = {
        "flagship_products": 2,
        "builder_projects": 3,
        "local_ai": 2,
        "hardware_compute": 2,
        "policy_regulation": 1,
    }
    for key, minimum in minima.items():
        mix = dict(PASSING_MIX)
        mix[key] = minimum - 1
        errors = qc.editorial_mix_errors(_notes(mix), 87)
        assert any(key in error and str(minimum) in error for error in errors), (
            key,
            errors,
        )


def test_research_ceiling_is_hard() -> None:
    mix = dict(PASSING_MIX)
    mix["research"] = 3
    errors = qc.editorial_mix_errors(_notes(mix), 87)
    assert any("research" in error and "2" in error for error in errors), errors


def test_manifest_requires_exact_known_integer_keys() -> None:
    missing = dict(PASSING_MIX)
    missing.pop("local_ai")
    errors = qc.editorial_mix_errors(_notes(missing), 87)
    assert any("local_ai" in error and "missing" in error.lower() for error in errors), errors

    malformed = dict(PASSING_MIX)
    malformed["research"] = "two"
    errors = qc.editorial_mix_errors(_notes(malformed), 87)
    assert any("research" in error and "integer" in error.lower() for error in errors), errors

    errors = qc.editorial_mix_errors(
        _notes(PASSING_MIX, extra_lines=["- industry_news: 4"]), 87
    )
    assert any("industry_news" in error and "unknown" in error.lower() for error in errors), errors

    errors = qc.editorial_mix_errors(
        _notes(PASSING_MIX, extra_lines=["- research: 1"]), 87
    )
    assert any("research" in error and "duplicate" in error.lower() for error in errors), errors


if __name__ == "__main__":
    tests = [
        ("gate_starts_at_ep087", test_gate_starts_at_ep087),
        ("exact_thresholds_pass", test_exact_thresholds_pass),
        ("each_minimum_is_hard", test_each_minimum_is_hard),
        ("research_ceiling_is_hard", test_research_ceiling_is_hard),
        ("manifest_requires_exact_known_integer_keys", test_manifest_requires_exact_known_integer_keys),
    ]
    passed = failed = 0
    for name, fn in tests:
        print(f"\n[test] {name}")
        try:
            fn()
            passed += 1
            print("  ✅ PASS")
        except AssertionError as exc:
            failed += 1
            print(f"  ❌ FAIL: {exc}")
        except Exception as exc:
            failed += 1
            print(f"  ❌ ERROR: {type(exc).__name__}: {exc}")
    print(f"\n{'=' * 60}")
    print(f"{passed}/{len(tests)} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
