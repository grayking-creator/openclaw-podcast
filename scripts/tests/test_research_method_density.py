#!/usr/bin/env python3
"""Regression tests for listenable research coverage in spoken transcripts."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_episode as checker  # noqa: E402


def test_rejected_ep087_pope_minute_fails_density_gate() -> None:
    # Keep the rejected minute as an immutable fixture.  The canonical EP087
    # transcript is intentionally replaced after this regression was added, so
    # reading that live path would make a successful rebuild break the test.
    transcript = """
    [NOVA]: Mehmet Iscan's Form, Not Content applies a placebo-controlled test
    to code self-repair. The common loop is simple: a local model writes a
    program, execution fails, the failed program and error output go back into
    the prompt, and the model tries again. PoPE, short for Popperian
    Placebo-controlled Evaluation, asks whether the actual error content
    improves repair or whether the surrounding retry scaffold carries the gain.

    [ALLOY]: The method treats the failed program as a conjecture and the
    execution counterexample as an oracle-relative refutation. It pairs live
    error content with placebos that preserve the predeclared prompt structure
    while removing task-relevant content or deranging the assignment between
    task and error. The study covers frozen small code models in the 0.5 to 1.5
    billion parameter range, with preregistered rules and four generations per
    arm-unit pair.

    [NOVA]: Two channels were tested. In the prompt channel, a 40-unit resistant
    band unlocked 12 units under the content-ablated form placebo and 10 under
    the live error-pattern arm, producing a mechanism-null result. In the
    weight channel, small-data adapter training produced an 8-to-8 tie between
    the error-content adapter and the intervention-free baseline at p equals
    1.0. A deranged placebo adapter reached 10 unlocks. Content-attributable
    superiority was not confirmed.

    [ALLOY]: The authors do not claim equivalence or non-inferiority, and they
    limit the finding to the public-tier screening endpoint.
    """

    failures = checker.research_method_density_windows(transcript)

    assert failures, "the rejected EP087 PoPE methodology minute must fail"
    constructs = set(failures[0]["constructs"])
    assert len(constructs) >= checker.RESEARCH_METHOD_DENSITY_THRESHOLD
    assert {
        "preregistered protocol",
        "arm-unit pair",
        "content-ablated condition",
        "mechanism-null result",
        "intervention-free baseline",
        "p-value notation",
        "non-inferiority",
        "equivalence",
    }.issubset(constructs)


def test_plain_language_product_and_research_summary_passes() -> None:
    transcript = """
    [NOVA]: A new local model now runs on a laptop with 32 gigabytes of memory.
    It can summarize documents, call tools, and help edit a codebase without
    sending private files to a hosted service. The release also adds a longer
    context window and faster first-token latency. One published benchmark
    reports better coding accuracy, although independent testing is still
    limited.

    [ALLOY]: The useful story is what people can make with it. A small support
    team built an offline search assistant for repair manuals, while a teacher
    used the same model to create private lesson summaries. Both projects run
    on ordinary computers and keep source material local. The model card also
    reports one p-value and a teacher-forced evaluation, but those method details
    do not dominate the explanation. Builders get a concrete capability, two
    examples, and a clear limitation without an oral research-paper review.

    [NOVA]: The API remains compatible with common local runtimes, so an existing
    application can swap models without changing its tool schemas. The vendor
    says quantization cuts memory use further, but has not yet published results
    across older hardware. That is the next practical question to watch.
    """

    assert checker.research_method_density_windows(transcript) == []


def test_isolated_legitimate_method_terms_do_not_accumulate_across_show() -> None:
    separated = (
        "A paper reports log likelihood as one evaluation measure. "
        + ("A product story explains a shipped capability in plain English. " * 170)
        + "A simulator models a Markov decision process in one research result."
    )

    assert checker.research_method_density_windows(separated) == []


if __name__ == "__main__":
    test_rejected_ep087_pope_minute_fails_density_gate()
    test_plain_language_product_and_research_summary_passes()
    test_isolated_legitimate_method_terms_do_not_accumulate_across_show()
    print("research-method density regression checks passed")
