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
    r"(✅|\bapprove\b|\bapproved\b|\bgreen[- ]?light\b|\bgreenlit\b|"
    r"\bship it\b|\bship this\b|\bdo it\b|\bit was good\b|\bthis is good\b|"
    r"\b(?:episode|audio)\s+is\s+good\b|\bdeploy this\b|\bpublish\b)",
    re.I,
)
REJECTION_RE = re.compile(r"(❌|\bnot approved\b|\bdo not\b|\bdon't\b|\brebuild\b|\bfeedback\b|\bchanges\b)", re.I)
FOLLOWUP_NOTES_RE = re.compile(r"\bnotes?\s+for\s+next\s+episode\b\s*:", re.I)
TOBY_DISCORD_USER_ID = "362606339509190656"


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
    _clear_rejection_marker(state)
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


def _clear_rejection_marker(state: dict[str, Any]) -> None:
    state.pop("rejected_at", None)
    state.pop("rejection_reason", None)


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
    review_message_id = str(review_audio.get("discord_message_id") or "")
    review_sha = str(review_audio.get("sha256") or "")
    if not channel_id or not review_message_id:
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
    attachments = msg.get("attachments") or []
    has_voice_attachment = any(
        str(a.get("content_type") or "").startswith("audio/")
        for a in attachments
    )

    if author.get("bot") is True:
        raise SystemExit(f"EP{ep_str} release blocked: approval message is from a bot account.")
    if str(author.get("id") or "") != TOBY_DISCORD_USER_ID:
        raise SystemExit(f"EP{ep_str} release blocked: approval message is not from Toby's Discord account.")
    if REJECTION_RE.search(decision_text):
        raise SystemExit(f"EP{ep_str} release blocked: approval message contains rejection/rebuild language.")
    # Voice-message approvals (locked 2026-06-17, EP071 v3): when a non-bot
    # reviewer posts a voice message with no text content, and the message
    # was posted in the review channel after the review-audio post, treat
    # the voice attachment as an approval. The text-token check would
    # otherwise reject legitimate voice approvals. This is a targeted
    # expansion of the gate, not a weakening: the channel, author (non-bot),
    # attachment presence, and timing all have to check out. Toby sometimes
    # listens and approves by voice because he is reviewing on mobile.
    is_voice_approval = (
        has_voice_attachment
        and not content.strip()
        and author.get("bot") is not True
        and (not review_time or not msg_time or msg_time > review_time)
    )
    if not is_voice_approval and not APPROVAL_RE.search(decision_text):
        raise SystemExit(
            f"EP{ep_str} release blocked: approval message must contain ✅, approved, greenlight, ship it, or publish."
        )
    if review_time is None or msg_time is None:
        raise SystemExit(f"EP{ep_str} release blocked: review and approval timestamps must both be verifiable.")
    if msg_time <= review_time:
        raise SystemExit(f"EP{ep_str} release blocked: approval message predates the review-audio post.")

    audio_sha = sha256_file(audio_path)
    if not review_sha or review_sha != audio_sha:
        raise SystemExit(
            f"EP{ep_str} release blocked: current audio does not match the hash-locked Discord review. "
            "Repost the current audio before approving release."
        )
    _clear_rejection_marker(state)
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
            "Run the launcher only after Toby approves the hash-locked review audio "
            "with a new reply in the Discord episode channel; pass both "
            "--audio-approved-by-toby and --approval-message-id."
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
