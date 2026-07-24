#!/usr/bin/env python3
"""Regression fence for EP087's 14-paper editorial failure."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import build_show_notes as builder  # noqa: E402
import transcript_constraints as constraints  # noqa: E402


def item(kind: str, score: int, lanes: list[str], n: int) -> dict:
    return {
        "kind": kind,
        "title": f"{kind} candidate {n}",
        "url": f"https://example.com/{kind}/{n}",
        "summary": "A source-backed summary of a consequential change and its practical impact.",
        "extra": "primary source",
        "score": score,
        "editorial_lanes": lanes,
    }


def words(n: int) -> str:
    base = "The finding changes what people can build and explains why the result matters now".split()
    return " ".join(base[i % len(base)] for i in range(n))


def story(segment_words: int) -> dict:
    return {
        "title": "A research finding in plain English",
        "summary": words(55),
        "technical_depth_angle": words(30),
        "actionability_angle": "This gives builders one concrete idea to test.",
        "listener_hook": "The useful result fits in one ordinary-language sentence.",
        "segment": words(segment_words),
    }


def test_papers_cannot_swamp_numbered_slate() -> None:
    candidates = [item("arxiv", 1_000 - i, ["research"], i) for i in range(12)]
    candidates += [item("editorial", 800 - i, ["builder_projects"], i) for i in range(3)]
    candidates += [item("infra_release", 700 - i, ["local_ai"], i) for i in range(2)]
    candidates += [item("editorial", 600 - i, ["hardware_compute"], i) for i in range(2)]
    candidates += [item("editorial", 500, ["policy_regulation"], 1)]
    candidates += [item("editorial", 400 - i, ["flagship_products"], i) for i in range(2)]
    candidates += [item("editorial", 300 - i, ["industry_news"], i) for i in range(3)]
    candidates.sort(key=lambda candidate: candidate["score"], reverse=True)

    selected, counts = builder.select_balanced_news(candidates, 14)

    assert len(selected) == 14
    assert counts["research"] <= builder.MAX_NUMBERED_RESEARCH_STORIES
    for lane, minimum in builder.EDITORIAL_LANE_MINIMUMS.items():
        assert counts[lane] >= minimum, (lane, counts)


def test_research_cannot_impersonate_hardware_lane() -> None:
    paper = item("arxiv", 100, [], 1)
    paper["title"] = "New GPU architecture and HBM benchmark"
    assert builder.editorial_lanes(paper) == ["research"]


def test_radar_project_can_satisfy_builder_and_local_lanes() -> None:
    project = {
        "kind": "radar",
        "title": "holaOS local-first work agent",
        "summary": "A local-first agent that keeps its working context on device.",
        "url": "https://github.com/holaboss-ai/holaOS",
    }
    assert builder.editorial_lanes(project) == ["builder_projects", "local_ai"]


def test_research_digest_has_short_spoken_band() -> None:
    assert not any("segment must be" in problem for problem in
                   builder.validate_story(story(160), set(), False, "research_digest"))
    assert any("segment must be" in problem for problem in
               builder.validate_story(story(270), set(), False, "research_digest"))


def test_local_spotlight_prefers_model_over_ollama_runtime() -> None:
    research = {
        "hf_trending_models": [{
            "id": "example/phone-model-GGUF",
            "url": "https://huggingface.co/example/phone-model-GGUF",
            "is_gguf": True,
            "pipeline_tag": "image-text-to-text",
            "likes": 42,
            "downloads": 900,
            "tags": ["gguf", "multimodal"],
        }],
        "openrouter": {"new_models": []},
        "github_releases": {"ollama/ollama": [{
            "tag": "v9.9.9", "prerelease": False, "body": "runtime release"
        }]},
    }
    spotlight = builder.choose_local_spotlight(research)
    assert spotlight["name"] == "example/phone-model-GGUF"


def test_transcript_research_digest_keeps_short_budget() -> None:
    title = "Research digest: A useful finding without a methods lecture"
    assert constraints.is_research_segment_title(title)
    assert constraints.segment_word_ceiling(title) == 190
    assert not constraints.is_release_segment_title(
        "ChatGPT now puts Chat, Work, and Codex under one roof"
    )


if __name__ == "__main__":
    test_papers_cannot_swamp_numbered_slate()
    test_research_cannot_impersonate_hardware_lane()
    test_research_digest_has_short_spoken_band()
    test_local_spotlight_prefers_model_over_ollama_runtime()
    test_transcript_research_digest_keeps_short_budget()
    print("ok")
