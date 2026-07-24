#!/usr/bin/env python3
"""Regression checks for required full-surface transcript coverage."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


generator = load_module("generate_episode_transcript", ROOT / "scripts/generate_episode_transcript.py")
checker = load_module("check_episode", ROOT / "scripts/check_episode.py")

notes = """# EP999

## Story Slate

1. **Main Story**

## Model Discovery Check

- **OpenAI: Example Model** — Decision: Selected.

## Local LLM Spotlight

- **Ollama v0.31.2** — local runtime update.

## GitHub Project Radar

- **getsentry/XcodeBuildMCP** — project one.
- **the-open-agent/openagent** — project two.
- **exa-labs/exa-mcp-server** — project three.

## Extra Research Candidates

- **Ideas Have Genomes: Benchmarking Lineage** — paper one.
- **Remember When It Matters: Proactive Memory** — paper two.
- **OpenCoF: Learning to Reason** — paper three.

## Primary Links

- https://example.invalid
"""

condensed = generator.condense_show_notes_for_prompt(notes)
for heading in (
    "Model Discovery Check",
    "Local LLM Spotlight",
    "GitHub Project Radar",
    "Extra Research Candidates",
):
    assert f"## {heading}" in condensed, heading
assert "## Primary Links" not in condensed

spoken = """
## [20:00] GitHub Project Radar
XcodeBuildMCP, OpenAgent, and Exa MCP Server are the three repos.
## [21:00] Extra Research Candidates
Ideas Have Genomes, Remember When It Matters, and OpenCoF are the three papers.
"""
for label in (
    "getsentry/XcodeBuildMCP",
    "the-open-agent/openagent",
    "exa-labs/exa-mcp-server",
    "Ideas Have Genomes: Benchmarking Lineage",
    "Remember When It Matters: Proactive Memory",
    "OpenCoF: Learning to Reason",
):
    assert checker.named_item_is_spoken(label, spoken), label

# EP087: release-labelled repo extras must match natural spoken versions even
# when punctuation and version pronunciation differ from the show-note label.
repo_release_spoken = """
## [29:25] Extra Research Candidates
The vllm-project/vllm project ships point two-five-one with lazy TorchCodec loading.
"""
assert checker.named_item_is_spoken(
    "vllm-project/vllm ships v0.25.1", repo_release_spoken
)

# EP090: a four-character repo slug remains a real product name. Natural
# possessive speech must not fail merely because the compact matcher has a
# five-character noise floor.
short_repo_spoken = "And don't miss nanbingxyz's 5ire, a desktop MCP client."
assert checker.named_item_is_spoken(
    "nanbingxyz/5ire — 5ire is a cross-platform desktop AI assistant",
    short_repo_spoken,
)

print("transcript full-surface regression checks passed")
