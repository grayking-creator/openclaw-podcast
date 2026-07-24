#!/usr/bin/env python3
"""Regression coverage for EP084's headline-only source hallucination."""

from __future__ import annotations

import sys
import time
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import build_show_notes as builder


def empty_lanes() -> dict:
    return {
        lane["key"]: {
            "label": lane["label"],
            "covered": [],
            "latest": None,
            "candidates": [],
        }
        for lane in builder.LANES
    }


def test_hn_uses_matching_rss_summary() -> None:
    research = {
        "recent_episodes": [],
        "openrouter": {"new_models": []},
        "hackernews": [{
            "title": "Example Model 9",
            "points": 1_000,
            "url": "https://vendor.example/model-9/",
            "comments_url": "https://news.ycombinator.com/item?id=1",
        }],
        "rss": {"Vendor": [{
            "title": "Introducing Example Model 9",
            "url": "https://vendor.example/model-9",
            "published": "2026-07-10T00:00:00Z",
            "summary": "The vendor describes the model's verified API and tool behavior.",
        }]},
        "arxiv_papers": [],
        "huggingface_papers": [],
        "github_trending": [],
        "reddit": [],
        "hf_trending_models": [],
        "infra_releases": {},
        "github_radar": [],
    }

    selected = builder.select_candidates(research, empty_lanes())
    story = selected["news"][0]
    assert story["summary"] == research["rss"]["Vendor"][0]["summary"]
    assert "via Vendor" in story["extra"]


def test_headline_only_hn_is_demoted_below_sourced_research() -> None:
    research = {
        "recent_episodes": [],
        "openrouter": {"new_models": []},
        "hackernews": [{
            "title": "Unverified Huge Headline",
            "points": 5_000,
            "url": "https://example.invalid/headline",
            "comments_url": "https://news.ycombinator.com/item?id=2",
        }],
        "rss": {},
        "arxiv_papers": [{
            "title": "Agent Benchmark Introduces Measured Evaluation",
            "url": "https://arxiv.org/abs/2607.00001",
            "arxiv_id": "2607.00001",
            "published": "2026-07-10T00:00:00Z",
            "summary": (
                "We introduce an agent benchmark with measured evaluation, "
                "repeatable tasks, and a structured failure analysis protocol."
            ),
            "authors": ["A. Researcher"],
        }],
        "huggingface_papers": [],
        "github_trending": [],
        "reddit": [],
        "hf_trending_models": [],
        "infra_releases": {},
        "github_radar": [],
    }

    selected = builder.select_candidates(research, empty_lanes())
    assert selected["news"][0]["kind"] == "arxiv"
    sparse = next(item for item in selected["leftover_news"] if item["kind"] == "hn")
    assert sparse["score"] == 120
    assert "insufficient for a full story" in sparse["extra"]


def test_same_model_release_from_two_sources_is_one_story() -> None:
    research = {
        "recent_episodes": [],
        "openrouter": {"new_models": []},
        "hackernews": [{
            "title": "GPT-9.2",
            "points": 1_000,
            "url": "https://vendor.example/gpt-9-2",
            "comments_url": "https://news.ycombinator.com/item?id=3",
        }],
        "rss": {"Vendor": [
            {
                "title": "GPT-9.2: New model family",
                "url": "https://vendor.example/gpt-9-2",
                "published": "2026-07-10T00:00:00Z",
                "summary": "The first-party release describes three tiers and their API availability.",
            },
            {
                "title": "Vendor releases GPT 9.2 with three model tiers",
                "url": "https://analysis.example/gpt-9-2",
                "published": "2026-07-10T01:00:00Z",
                "summary": "A second feed summarizes the same GPT 9.2 model-family launch.",
            },
        ]},
        "arxiv_papers": [],
        "huggingface_papers": [],
        "github_trending": [],
        "reddit": [],
        "hf_trending_models": [],
        "infra_releases": {},
        "github_radar": [],
    }

    selected = builder.select_candidates(research, empty_lanes())
    matching = [item for item in selected["news"] if "9.2" in item["title"]]
    assert len(matching) == 1


def test_recent_sol_terra_luna_routes_collapse_to_family() -> None:
    now = time.time()
    models = []
    for tier, description in (
        ("sol", "flagship tier"),
        ("terra", "balanced tier"),
        ("luna", "fast affordable tier"),
    ):
        for suffix in ("", "-pro"):
            models.append({
                "id": f"openai/gpt-5.6-{tier}{suffix}",
                "name": f"OpenAI: GPT-5.6 {tier.title()}{' Pro' if suffix else ''}",
                "context_length": 1_050_000,
                "created": now,
                "description": description,
            })
    research = {
        "recent_episodes": [],
        "openrouter": {"new_models": [], "major_models": models},
        "hackernews": [],
        "rss": {},
        "arxiv_papers": [],
        "huggingface_papers": [],
        "github_trending": [],
        "reddit": [],
        "hf_trending_models": [],
        "infra_releases": {},
        "github_radar": [],
    }

    selected = builder.select_candidates(research, empty_lanes())
    assert len(selected["model_selected"]) == 1
    family = selected["model_selected"][0]
    assert family["id"] == "openai/gpt-5.6"
    assert "Sol, Terra, Luna" in family["name"]
    assert all(tier in family["description"] for tier in ("Sol", "Terra", "Luna"))


def test_secondary_rss_and_thin_hf_summary_stay_out_of_slate() -> None:
    research = {
        "recent_episodes": [],
        "openrouter": {"new_models": []},
        "hackernews": [],
        "rss": {"Secondary Tech Blog": [{
            "title": "Secondary report with unverified model mechanisms",
            "url": "https://secondary.example/report",
            "published": "2026-07-10T00:00:00Z",
            "summary": "A long secondary summary that should remain a research lead, not a sourced story.",
        }]},
        "arxiv_papers": [{
            "title": "Primary Agent Evaluation Paper",
            "url": "https://arxiv.org/abs/2607.00002",
            "arxiv_id": "2607.00002",
            "published": "2026-07-10T00:00:00Z",
            "summary": "We introduce a measured agent evaluation with repeatable tasks and failure analysis.",
            "authors": ["A. Researcher"],
        }],
        "huggingface_papers": [{
            "title": "Thin AI Summary",
            "url": "https://huggingface.co/papers/2607.00003",
            "arxiv_id": "2607.00003",
            "ai_summary": "Too little source detail for a full grounded story.",
            "summary": "",
            "upvotes": 500,
        }],
        "github_trending": [],
        "reddit": [],
        "hf_trending_models": [],
        "infra_releases": {},
        "github_radar": [],
    }

    selected = builder.select_candidates(research, empty_lanes())
    assert selected["news"][0]["kind"] == "arxiv"
    assert all(item["kind"] not in {"rss", "hf_paper"} for item in selected["news"])
    assert {item["kind"] for item in selected["leftover_news"]} >= {"rss", "hf_paper"}


def test_insufficient_source_skips_without_retry_or_fallback() -> None:
    class Pool:
        calls = 0

        def run(self, prompt: str) -> str:
            del prompt
            self.calls += 1
            return '{"insufficient_source": true}'

    pool = Pool()
    fallback_called = False

    def fallback() -> dict:
        nonlocal fallback_called
        fallback_called = True
        return {"title": "must not be used"}

    result, used_fallback = builder.gen_validated(
        pool,
        lambda feedback: feedback,
        lambda obj: [],
        fallback,
        "test insufficient source",
        allow_insufficient=True,
    )
    assert result is None
    assert used_fallback is False
    assert pool.calls == 1
    assert fallback_called is False


if __name__ == "__main__":
    test_hn_uses_matching_rss_summary()
    test_headline_only_hn_is_demoted_below_sourced_research()
    test_same_model_release_from_two_sources_is_one_story()
    test_recent_sol_terra_luna_routes_collapse_to_family()
    test_secondary_rss_and_thin_hf_summary_stay_out_of_slate()
    test_insufficient_source_skips_without_retry_or_fallback()
    print("ok")
