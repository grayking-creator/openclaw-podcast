#!/usr/bin/env python3
"""Regression coverage for the EP085 radar/model depth repair contract."""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import build_show_notes as builder  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    repos = [
        {
            "full_name": f"example/repo-{index}",
            "url": f"https://github.com/example/repo-{index}",
            "stars": 1000 + index,
            "pushed_at": "2026-07-13T10:00:00Z",
            "latest_release": "v1.2.3",
            "latest_release_date": "2026-07-12T12:00:00Z",
            "blurb": "Agent tooling.",
            "stack_improvement_angle": "Adds a testable tool surface.",
            "try_now": "Run the example integration.",
        }
        for index in range(1, 4)
    ]
    legacy_radar = "\n\n".join(
        f"- **{repo['full_name']}** — {repo['url']} — {repo['blurb']}\n"
        f"  Stack improvement angle: {repo['stack_improvement_angle']}\n"
        f"  Try now: {repo['try_now']}"
        for repo in repos
    )
    repaired_radar, radar_repairs = builder.ensure_radar_depth_metadata(legacy_radar, repos)
    require(radar_repairs >= 3, "legacy radar bullets were not repaired")
    for field in ("stars:", "stars_delta_30d:", "latest_release:",
                  "Why this is on the radar now:"):
        require(repaired_radar.count(field) >= 3, f"missing repaired radar field: {field}")
    second_radar, second_radar_repairs = builder.ensure_radar_depth_metadata(
        repaired_radar, repos)
    require(second_radar == repaired_radar and second_radar_repairs == 0,
            "radar depth repair is not idempotent")

    selected = [{
        "id": "example/model-1",
        "name": "Example Model 1",
        "url": "https://example.com/model-1",
        "context_length": 131072,
        "params_active": "7B",
        "params_total": "42B",
        "modality": "text and image input; text output",
    }]
    legacy_models = (
        "- **Example Model 1** (example) — Primary source: https://example.com/model-1. "
        "Decision: Selected — new standalone model.\n\n"
        "- **Older Model** (example) — Primary source: https://example.com/older. "
        "Decision: Not Selected — already covered."
    )
    repaired_models, model_repairs = builder.ensure_model_depth_metadata(
        legacy_models, selected)
    require(model_repairs == 1, "selected model bullet was not repaired exactly once")
    selected_block, not_selected_block = repaired_models.split("\n\n", 1)
    for field in ("params_active:", "params_total:", "context:", "modality:"):
        require(field in selected_block, f"missing repaired model field: {field}")
        require(field not in not_selected_block,
                f"Not Selected model was incorrectly treated as Selected: {field}")
    second_models, second_model_repairs = builder.ensure_model_depth_metadata(
        repaired_models, selected)
    require(second_models == repaired_models and second_model_repairs == 0,
            "model depth repair is not idempotent")

    current_radar = builder.render_radar(repos)
    _, current_radar_repairs = builder.ensure_radar_depth_metadata(current_radar, repos)
    current_models = builder.render_model_discovery(selected, [], [])
    _, current_model_repairs = builder.ensure_model_depth_metadata(current_models, selected)
    require(current_radar_repairs == 0 and current_model_repairs == 0,
            "current deterministic renderers do not satisfy their checker contract")

    raw_release = (
        "# vLLM v0.25.1\r\n\r\n## Highlights\r\n\r\n"
        "- Lazy-load `torchcodec` when FFmpeg is unavailable."
    )
    flattened = builder.inline_source_excerpt(raw_release)
    require("\n" not in flattened and "##" not in flattened,
            "release-note Markdown can still terminate the Extras section")
    require("vLLM v0.25.1 Highlights Lazy-load torchcodec" in flattened,
            "release-note flattening removed substantive source text")

    print("PASS: show-notes radar/model depth repair contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
