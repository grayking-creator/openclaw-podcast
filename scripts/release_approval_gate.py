#!/usr/bin/env python3
"""Approval marker helpers for the AgentStack Daily release gate."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


APPROVAL_RE = re.compile(
    r"(✅|\bapprove\b|\bapproved\b|\bgreen[- ]?light\b|\bgreenlit\b|\bship it\b|\bship this\b|\bit was good\b|\bthis is good\b|\b(?:episode|audio)\s+is\s+good\b|\bdeploy this\b)",
    re.I,
)
REJECTION_RE = re.compile(r"(❌|\bnot approved\b|\bdo not\b|\bdon't\b|\brebuild\b|\bfeedback\b|\bchanges\b)", re.I)
FOLLOWUP_NOTES_RE = re.compile(r"\bnotes?\s+for\s+next\s+episode\b\s*:", re.I)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def record_review_audio(
    state: dict[str, Any],
    *,
    audio_path: Path,
    duration: str,
    audio_url: str,
    cover_url: str,
) -> dict[str, Any]:
    review_audio = {
        "path": str(audio_path),
        "sha256": sha256_file(audio_path),
        "size": audio_path.stat().st_size,
        "duration": duration,
        "audio_url": audio_url,
        "cover_url": cover_url,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }
    state["review_audio"] = review_audio
    state["audio_approval"] = {
        "approved": False,
        "required": True,
        "reason": "Toby must approve the reviewed EN audio before feeds or website publish.",
        "review_audio_sha256": review_audio["sha256"],
        "updated_at": review_audio["reviewed_at"],
    }
    return state


def record_review_discord_post(
    state: dict[str, Any],
    *,
    channel_id: str,
    message_id: str,
    posted_at: str | None = None,
) -> dict[str, Any]:
    review_audio = state.setdefault("review_audio", {})
    review_audio["discord_channel_id"] = str(channel_id)
    review_audio["discord_message_id"] = str(message_id)
    if posted_at:
        review_audio["discord_posted_at"] = posted_at
    state.setdefault("audio_approval", {})["updated_at"] = datetime.now(timezone.utc).isoformat()
    return state


def mark_audio_approved(
    state: dict[str, Any],
    *,
    audio_path: Path,
    approved_by: str = "Toby",
    source: str = "operator-confirmed",
) -> dict[str, Any]:
    audio_sha = sha256_file(audio_path)
    state["audio_approval"] = {
        "approved": True,
        "required": True,
        "approved_by": approved_by,
        "source": source,
        "review_audio_sha256": audio_sha,
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    return state


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def approval_decision_text(content: str) -> str:
    """Use only the approval clause when a message also contains future-episode notes."""
    parts = FOLLOWUP_NOTES_RE.split(content, maxsplit=1)
    return parts[0].strip() or content


def discord_request(token: str, method: str, path: str) -> dict[str, Any]:
    req = urllib.request.Request(
        f"https://discord.com/api/v10{path}",
        method=method,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def mark_audio_approved_from_discord(
    state: dict[str, Any],
    *,
    audio_path: Path,
    ep_num: int,
    approval_message_id: str,
    token: str,
) -> dict[str, Any]:
    ep_str = f"{ep_num:03d}"
    review_audio = state.get("review_audio") or {}
    channel_id = str(review_audio.get("discord_channel_id") or "")
    if not channel_id:
        raise SystemExit(
            f"EP{ep_str} release blocked: no Discord review post is recorded for this audio. "
            "Rebuild/repost the review audio before approving release."
        )
    if not token:
        raise SystemExit("Release blocked: DISCORD_BOT_TOKEN is unavailable, so approval cannot be verified.")

    msg = discord_request(token, "GET", f"/channels/{channel_id}/messages/{approval_message_id}")
    author = msg.get("author") or {}
    content = str(msg.get("content") or "")
    decision_text = approval_decision_text(content)
    timestamp = str(msg.get("timestamp") or "")
    msg_time = parse_timestamp(timestamp)
    review_time = parse_timestamp(
        str(review_audio.get("discord_posted_at") or review_audio.get("reviewed_at") or "")
    )

    if author.get("bot") is True:
        raise SystemExit(f"EP{ep_str} release blocked: approval message is from a bot account.")
    if REJECTION_RE.search(decision_text):
        raise SystemExit(f"EP{ep_str} release blocked: approval message contains rejection/rebuild language.")
    if not APPROVAL_RE.search(decision_text):
        raise SystemExit(
            f"EP{ep_str} release blocked: approval message must contain ✅, approved, greenlight, or ship it."
        )
    if review_time and msg_time and msg_time <= review_time:
        raise SystemExit(f"EP{ep_str} release blocked: approval message predates the review-audio post.")

    audio_sha = sha256_file(audio_path)
    state["audio_approval"] = {
        "approved": True,
        "required": True,
        "approved_by": author.get("username") or "Discord user",
        "approval_author_id": author.get("id"),
        "approval_channel_id": channel_id,
        "approval_message_id": str(approval_message_id),
        "approval_message_timestamp": timestamp,
        "approval_message_excerpt": content[:160],
        "source": "verified-discord-message",
        "review_audio_sha256": audio_sha,
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    return state


def assert_audio_approved(state: dict[str, Any], *, audio_path: Path, ep_num: int) -> None:
    ep_str = f"{ep_num:03d}"
    if not audio_path.exists():
        raise SystemExit(f"EP{ep_str} release blocked: missing EN audio file {audio_path}")

    current_sha = sha256_file(audio_path)
    approval = state.get("audio_approval") or {}
    review_audio = state.get("review_audio") or {}
    approved = approval.get("approved") is True
    approved_sha = approval.get("review_audio_sha256")
    review_sha = review_audio.get("sha256")

    if not approved:
        raise SystemExit(
            f"EP{ep_str} release blocked: EN audio has not been explicitly approved. "
            "Run the launcher only after Toby approves the review audio, using the approval "
            "message id from the episode review channel."
        )
    if approved_sha != current_sha:
        raise SystemExit(
            f"EP{ep_str} release blocked: approval hash does not match current audio. "
            "Regenerate/repost the review audio or record a fresh approval."
        )
    if review_sha and review_sha != current_sha:
        raise SystemExit(
            f"EP{ep_str} release blocked: current audio differs from the posted review audio. "
            "Post the new audio for review before publishing."
        )
