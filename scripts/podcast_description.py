#!/usr/bin/env python3
"""Normalize public podcast descriptions before they enter an RSS feed."""

from __future__ import annotations

import html
import re

DEFAULT_MAX_CHARS = 160
MIN_USEFUL_CHARS = 40

TIMESTAMP_HEADING_RE = re.compile(
    r"^\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*"
    r"(?:[-:–—]\s*)?"
    r"(?:intro|hook|story|section|chapter|outro|conclusion|sponsor)\b",
    re.IGNORECASE,
)


def _collapse_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def sanitize_episode_summary(value: str) -> str:
    """Remove transcript structure, markup, and link-only calls to action."""
    text = html.unescape(value or "")
    text = re.sub(r"<!\[CDATA\[|\]\]>", " ", text)
    text = re.sub(r"```(?:\w+)?", "\n", text)
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    kept_lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or TIMESTAMP_HEADING_RE.match(line):
            continue
        if re.match(
            r"^(?:#{1,6}\s*)?"
            r"(?:show notes?|full transcript|chapters?|links?|sources?)\s*:?\s*$",
            line,
            re.IGNORECASE,
        ):
            continue
        if re.match(
            r"^(?:agentstack|openclaw)\s+daily\b.*\bepisode\s+\d+",
            line,
            re.IGNORECASE,
        ):
            continue
        if re.match(r"^show notes?\s*:\s*https?://", line, re.IGNORECASE):
            continue

        line = re.sub(r"^#{1,6}\s*", "", line)
        line = re.sub(r"^\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*", "", line)
        line = re.sub(r"\*\*|__|`", "", line)
        line = re.sub(r"https?://\S+", " ", line, flags=re.IGNORECASE)
        if line.strip():
            kept_lines.append(line)

    return _collapse_ws(" ".join(kept_lines))


def compact_episode_summary(value: str, max_chars: int = DEFAULT_MAX_CHARS) -> str:
    """Trim at a useful sentence or word boundary without leaking raw notes."""
    clean = sanitize_episode_summary(value)
    if len(clean) <= max_chars:
        return clean

    window = clean[: max_chars + 1]
    sentence_ends = [
        match.end()
        for match in re.finditer(r"[.!?](?=\s|$)", window)
        if 110 <= match.end() <= max_chars
    ]
    if sentence_ends:
        return clean[: sentence_ends[-1]].strip()

    word_safe = re.sub(r"\s+\S*$", "", clean[: max(1, max_chars - 3)])
    word_safe = re.sub(r"[\s,:;/-]+$", "", word_safe)
    return f"{word_safe}..."


def prepare_episode_summary(
    value: str,
    *,
    fallback: str = "",
    max_chars: int = DEFAULT_MAX_CHARS,
) -> str:
    """Return a feed-safe summary, falling back to the episode title."""
    summary = compact_episode_summary(value, max_chars=max_chars)
    if len(summary) >= MIN_USEFUL_CHARS:
        return summary

    fallback_summary = compact_episode_summary(
        f"{fallback}. AgentStack Daily explains the key updates and why they matter.",
        max_chars=max_chars,
    )
    return fallback_summary or "AgentStack Daily episode summary."
