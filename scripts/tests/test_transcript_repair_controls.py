#!/usr/bin/env python3
"""Offline regression tests for transcript budgeting and bounded compaction."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_episode as checker  # noqa: E402
import generate_episode_transcript as generator  # noqa: E402
import transcript_constraints as constraints  # noqa: E402


def fixture_notes(selected: bool = False) -> str:
    stories = [
        "1. **Agent Stack Release Readout: OpenAI Codex 1.2**",
        "2. **Research model released today with a new benchmark**",
    ]
    stories.extend(f"{index}. **Concrete paper story {index}**" for index in range(3, 15))
    decision = "Selected" if selected else "Not Selected"
    return f"""# Episode fixture

## Story Slate

{chr(10).join(stories)}

## Model Discovery Check

- **Example Model** — Decision: {decision}.

## Local LLM Spotlight

- **Ollama 1.2** — concrete local capability.

## GitHub Project Radar

- **org/repo-one** — first repo.
- **org/repo-two** — second repo.
- **org/repo-three** — third repo.

## Extra Research Candidates

- **Paper Alpha Mechanism Study** — first paper.
- **Paper Beta Capability Study** — second paper.
- **Paper Gamma Runtime Study** — third paper.
"""


def test_shared_band_and_release_classifier() -> None:
    assert constraints.TRANSCRIPT_FLOOR == 4_800
    assert constraints.TRANSCRIPT_CEILING == 5_400
    assert constraints.is_release_segment_title("Agent Stack Release Readout: Codex")
    assert not constraints.is_release_segment_title(
        "Research model released today with a new benchmark"
    ), "publication is not an agent-harness release-budget segment"


def test_computed_budget_ledger_fits_with_buffer() -> None:
    notes = fixture_notes()
    ledger = constraints.build_episode_budget_ledger(notes)
    assert len(ledger["story_budgets"]) == 14
    assert ledger["story_budgets"][0]["release"]
    assert not ledger["story_budgets"][1]["release"]
    assert 4_900 <= ledger["estimated_target"] <= 5_250, ledger
    assert ledger["lanes"]["model_discovery"]["no_selected"]
    prompt_ledger = constraints.format_episode_budget_ledger(notes)
    assert "Story 2 (NON-RELEASE)" in prompt_ledger
    assert "paper, model, product, or dataset published today" in prompt_ledger
    assert "one natural 20-80 word spoken beat" in prompt_ledger


def test_selected_model_parser_does_not_confuse_not_selected() -> None:
    assert constraints.selected_model_labels(fixture_notes()) == []
    assert constraints.selected_model_labels(fixture_notes(selected=True)) == ["Example Model"]


def test_candidate_score_charges_length_segments_and_lanes() -> None:
    notes = fixture_notes()
    lane_headers = "\n".join(f"## {heading}\n[NOVA]: concrete news." for heading in constraints.REQUIRED_SPOKEN_LANES)
    near = "# Fixture\n" + ("news " * 4_850) + lane_headers
    far = "# Fixture\n" + ("news " * 7_000) + lane_headers
    near_score, near_metrics = constraints.candidate_constraint_score(near, notes, 2)
    far_score, far_metrics = constraints.candidate_constraint_score(far, notes, 2)
    assert near_metrics["global_distance"] == 0
    assert far_metrics["global_distance"] > 1_500
    assert near_score < far_score

    overlong_story = (
        "# Fixture\n## [02:00] Research model released today\n"
        + ("mechanism " * 400)
    )
    overages = constraints.segment_overages(overlong_story)
    assert overages[0]["ceiling"] == 320
    assert overages[0]["overage"] == 80


def test_one_compaction_trigger_and_preservation_fence() -> None:
    notes = fixture_notes()
    failures = [
        "  ❌ Hard ceiling (5,400 words)",
        "     → Got 6,000 words — hard ceiling is 5,400.",
    ]
    assert generator.needs_length_compaction(failures)
    assert not generator.needs_length_compaction(["  ❌ Missing outro"])

    per_story_failure = [
        "  ❌ Per-story word budget (≤320 non-release / ≤480 release)",
    ]
    below_floor = (
        "# Fixture\n" + ("context " * 4_400)
        + "\n## [02:00] Research Story\n" + ("mechanism " * 330)
    )
    enough_slack = below_floor.replace("context " * 4_400, "context " * 4_500)
    assert not generator.needs_length_compaction(per_story_failure, below_floor)
    assert generator.needs_length_compaction(per_story_failure, enough_slack)

    original = """# Fixture 0.402
[NOVA]: Concrete technology news names 183 parameters.
[ALLOY]: The mechanism changes latency by 55 percent.

## [02:00] Agent Stack Release Readout: OpenAI Codex 1.2
[NOVA]: Codex 1.2 ships the runtime change.
[ALLOY]: It preserves the API mechanism.
[PAUSE]

## Model Discovery Check
[NOVA]: Model progress came through serving and domain adaptation.
"""
    candidate = """# Fixture 0.402
[NOVA]: Concrete technology news names 183 parameters.
[ALLOY]: The mechanism changes latency by 55 percent.

## [02:00] Agent Stack Release Readout: OpenAI Codex 1.2
[NOVA]: Codex 1.2 ships the runtime change and preserves the API mechanism.
[ALLOY]: The capability is concrete.
[PAUSE]

## Model Discovery Check
[NOVA]: Model progress came through serving and domain adaptation.
"""
    assert generator.validate_length_compaction(original, candidate, notes) == []
    assert generator.validate_length_compaction(
        original, candidate.replace("183", ""), notes
    )
    assert generator.validate_length_compaction(
        original, candidate.replace("## Model Discovery Check", "## Model News"), notes
    )
    duplicate_number_original = """# Fixture
[NOVA]: One result improved by 55 percent.
[ALLOY]: A different result also improved by 55 percent.
"""
    duplicate_number_candidate = """# Fixture
[NOVA]: One result improved by 55 percent.
[ALLOY]: The second result remains source-grounded.
"""
    assert generator.validate_length_compaction(
        duplicate_number_original, duplicate_number_candidate, ""
    ) == ["numeric facts removed: ['55']"]
    prompt = generator.build_length_compaction_prompt(original, notes, failures)
    assert "LENGTH-ONLY COMPACTION" in prompt
    assert "Copy every markdown heading verbatim" in prompt
    assert "4,800-5,400 words" in prompt


def test_testing_gate_rejects_assignments_but_allows_results() -> None:
    filler = (
        "Builders should run a golden test before deployment, then validate the "
        "workflow with this checklist."
    )
    result = (
        "The published benchmark measured 0.402 accuracy across five datasets, "
        "and the new runtime cut latency by 18 percent."
    )
    assert checker.prescriptive_testing_hits(filler)
    assert checker.prescriptive_testing_hits(result) == []


def test_segment_parser_accepts_suffixed_untimestamped_lane_headings() -> None:
    transcript = """# Fixture
## GitHub Project Radar: org/repo-one
[NOVA]: Concrete repo capability.
## Model Discovery Check: Market Read
[ALLOY]: Progress landed in serving and domain adaptation.
## Local LLM Spotlight: Ollama
[NOVA]: Concrete local model capability.
## Extra Research Candidate: Paper Alpha
[ALLOY]: Concrete research mechanism.
"""
    segments = constraints.transcript_segments(transcript)
    assert len(segments) == 4
    assert constraints.missing_spoken_lanes(transcript, fixture_notes()) == []
    counts = constraints.transcript_lane_word_counts(transcript)
    assert counts["radar"] > 0
    assert counts["model_discovery"] > 0
    assert counts["spotlight"] > 0
    assert counts["extras"] > 0


def test_speaker_turn_parser_covers_bracketed_and_bold_labels() -> None:
    transcript = """[NOVA]: Bracketed turn.
**ALLOY:** Bold turn with the colon inside.
**NOVA**: Bold turn with the colon outside.
ALLOY: Legacy plain turn.
[NOVA]: Fifth turn.
"""
    assert checker.speaker_label_sequence(transcript) == [
        "NOVA", "ALLOY", "NOVA", "ALLOY", "NOVA",
    ]
    assert len(checker.speaker_label_sequence(transcript)) > 4
    assert checker.segment_turn_cap("[02:00] Concrete Research Story") == 4
    assert checker.segment_turn_cap("[33:12] Practical Queue") is None
    assert checker.per_story_turn_overages([
        ("02:00", "[02:00] Concrete Research Story", transcript),
    ])
    assert checker.per_story_turn_overages([
        ("33:12", "[33:12] Practical Queue", transcript),
    ]) == []


def test_computed_lane_caps_are_shared_with_qc() -> None:
    notes = fixture_notes()

    def body(word: str, count: int) -> str:
        return (word + " ") * count

    transcript = (
        "# Fixture\n" + body("opening", 200)
        + "\n## GitHub Project Radar: One\n" + body("radar", 140)
        + "\n## GitHub Project Radar: Two\n" + body("radar", 140)
        + "\n## GitHub Project Radar: Three\n" + body("radar", 140)
        + "\n## Model Discovery Check\n" + body("model", 80)
        + "\n## Local LLM Spotlight\n" + body("spotlight", 140)
        + "\n## Extra Research Candidate: One\n" + body("extra", 80)
        + "\n## Extra Research Candidate: Two\n" + body("extra", 80)
        + "\n## Extra Research Candidate: Three\n" + body("extra", 80)
        + "\n## Practical Queue\n" + body("queue", 160)
    )
    counts = constraints.transcript_lane_word_counts(transcript)
    assert counts == {
        "opening": 200,
        "radar": 420,
        "model_discovery": 80,
        "spotlight": 140,
        "extras": 240,
        "queue_outro": 160,
    }
    assert constraints.lane_budget_overages(transcript, notes) == []

    overlong = transcript.replace(body("spotlight", 140), body("spotlight", 141))
    assert constraints.lane_budget_overages(overlong, notes) == [{
        "lane": "spotlight",
        "words": 141,
        "ceiling": 140,
        "overage": 1,
    }]


def main() -> int:
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"transcript repair controls: PASS ({len(tests)} tests)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
