#!/usr/bin/env python3
"""
Telegram review-surface notifier (locked 2026-06-27, EP075 incident class).

Replaces the Discord review channel post for AgentStack Daily. Three intents:

  --intent ready      post the morning "ready to review" message with the
                       audio + cover + show notes + transcript URLs and a
                       5–7 bullet slate summary. Approving on Telegram is
                       the operator-confirmed path; no Discord message ID
                       is required.
  --intent shipped    post the post-approval "shipped" confirmation with the
                       canonical episode link and CDN URL.
  --intent skipped    post a "today's build was skipped" message naming the
                       specific gate that failed.

Telegram is for DECISIONS and APPROVALS only. This script never posts
status pings, plans, or pipeline narration. Replies are matched by the
orchestrator from the operator-confirmed path
(release_episode_approved.py:mark_audio_approved_from_telegram), not by
fabricated Discord message IDs.

Send-record persistence: after every successful send, the message id and
chat id are saved to scripts/.telegram_send_records/ep{NNN}.json so the
approval gate (mark_audio_approved_from_telegram) can verify the
operator is approving the audio they actually heard.

Usage:
    python3 scripts/notify_telegram_review.py --ep 76 --intent ready \\
        --audio-url <URL> --cover-url <URL> --show-notes-url <URL> \\
        --transcript-url <URL> --duration "24:25" --sha256 <HASH> \\
        --summary "Story 1: ...; Story 2: ..." [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional
import mimetypes

SCRIPT_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPT_DIR.parent

TELEGRAM_CHANNEL = "telegram"
TELEGRAM_TARGET = os.environ.get("PODCAST_TELEGRAM_TARGET", "8319992332")
# Locked 2026-06-27: this pipeline MUST use the @DigiToby_bot bot, which
# is the bot this conversation is on. openclaw's default Telegram bot
# (the ARIA bot, token 8260045001:***) is the wrong identity and posts to
# a different channel. We read the token directly from
# /Users/tobyglennpeters/.hermes/.env to bypass openclaw's account
# selection. If the env file is missing, the pipeline aborts loudly.
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_BOT_TOKEN_FILE = "/Users/tobyglennpeters/.hermes/.env"
OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "/opt/homebrew/bin/openclaw")


def _load_bot_token() -> str:
    """Read TELEGRAM_BOT_TOKEN from the hermes .env. This is the
    @DigiToby_bot token, the one this Telegram session is on. We do NOT
    use the openclaw CLI's bot account because openclaw defaults to the
    ARIA bot, which posts to a different chat."""
    global TELEGRAM_BOT_TOKEN
    if TELEGRAM_BOT_TOKEN:
        return TELEGRAM_BOT_TOKEN
    try:
        for line in Path(TELEGRAM_BOT_TOKEN_FILE).read_text().splitlines():
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                TELEGRAM_BOT_TOKEN = line.split("=", 1)[1].strip()
                return TELEGRAM_BOT_TOKEN
    except FileNotFoundError:
        pass
    raise SystemExit(
        f"❌ ROUTING MIS-WIRED: TELEGRAM_BOT_TOKEN not found in "
        f"{TELEGRAM_BOT_TOKEN_FILE}. The agentstack-podcast pipeline must "
        f"post via the @DigiToby_bot bot, which is the bot this "
        f"conversation is on. Do not fall back to openclaw's default "
        f"Telegram bot — that posts to the ARIA channel, not yours."
    )

SEND_RECORD_DIR = SCRIPT_DIR / ".telegram_send_records"

READY_TEMPLATE = (
    "✅ EP{ep:03d} ready to review\n"
    "\n"
    "🎧 Listen ({status}): {audio_url}\n"
    "🖼 Cover ({status}): {cover_url}\n"
    "📝 Show notes ({status}): {show_notes_url}\n"
    "📄 Transcript ({status}): {transcript_url}\n"
    "⏱ Duration: {duration}\n"
    "🔒 Audio hash: {sha256_short}…\n"
    "\n"
    "Slate ({slate_count} stories):\n"
    "{summary_lines}\n"
    "\n"
    "Reply publish to ship  /  reply with feedback to rebuild."
)

# Telegram routing (operator rule, 2026-07-07): listenable audio — the
# "ready" post with audio attached and the shipped confirmation link — plus
# run-stopping failures (anything that stops audio generation or publishing).
# Progress notes and mid-stream gates belong in the Discord build log
# (agentstack_morning.sh alert()), kept short. Do not add in-progress
# intents here.
FAILED_TEMPLATE = (
    "❌ EP{ep:03d} {reason} FAILED — {detail}\n"
    "Build log: {build_log}"
)

SHIPPED_TEMPLATE = (
    "🚀 EP{ep:03d} shipped\n"
    "\n"
    "Canonical: {canonical_url}\n"
    "CDN: {cdn_url}\n"
    "Released at: {pub_date}\n"
    "\n"
    "Translations + shorts are queued. Telegram stays quiet until the next "
    "morning's review."
)

SKIPPED_TEMPLATE = (
    "🛑 EP{ep:03d} SKIPPED — {reason}\n"
    "\n"
    "Detail: {detail}\n"
    "Rule: {rule}\n"
    "\n"
    "Run log: {run_log}\n"
    "Build log: {build_log}"
)

# Module-level state for the active send, used by _send() to record the
# result of the openclaw CLI call. main() sets these before dispatching.
_active_ep: Optional[int] = None
_active_intent: Optional[str] = None


# ── Send-record persistence ──────────────────────────────────────────────────

def _persist_send_record(ep: Optional[int], intent: Optional[str], raw: str) -> None:
    """Persist the message id + chat id returned by the openclaw CLI.

    Best-effort: failures to parse or write the record are swallowed.
    The approval gate (mark_audio_approved_from_telegram) requires the
    ready-post record; if it is missing, the gate falls back to
    verifying only the audio SHA against the file on disk.
    """
    if ep is None or intent is None or not raw:
        return
    parsed: dict = {}
    try:
        maybe = json.loads(raw)
        if isinstance(maybe, dict):
            parsed = maybe
    except Exception:
        m_id = re.search(r'"id"\s*:\s*"?(\d+)"?', raw)
        m_chat = re.search(r'"chat"\s*:\s*\{[^}]*"id"\s*:\s*"?(\d+)"?', raw)
        if m_id:
            parsed["id"] = m_id.group(1)
        if m_chat:
            parsed.setdefault("chat", {})["id"] = m_chat.group(1)
    msg_id = parsed.get("id") or parsed.get("message_id")
    chat = parsed.get("chat") or {}
    chat_id = chat.get("id") if isinstance(chat, dict) else None
    if not msg_id and not chat_id:
        return
    try:
        SEND_RECORD_DIR.mkdir(parents=True, exist_ok=True)
        record_path = SEND_RECORD_DIR / f"ep{ep:03d}.json"
        record: dict = {"updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        record[intent] = {
            "message_id": str(msg_id) if msg_id else None,
            "chat_id": str(chat_id) if chat_id else None,
        }
        if record_path.exists():
            try:
                existing = json.loads(record_path.read_text())
                if isinstance(existing, dict):
                    existing.update(record)
                    record = existing
            except Exception:
                pass
        record_path.write_text(json.dumps(record, indent=2))
    except Exception:
        pass


# ── Formatting helpers ──────────────────────────────────────────────────────

def _format_summary(summary: str, max_bullets: int = 24) -> str:
    """Render the operator-supplied slate summary as numbered bullets.

    Show the FULL slate (EP080 lesson: truncating to 7 made a 14-story
    episode look thin and nearly caused a needless rebuild). The cap only
    guards Telegram's 4096-char message limit."""
    if not summary:
        return "  (no summary provided)"
    chunks = _summary_chunks(summary)
    lines = [f"  {i+1}. {c}" for i, c in enumerate(chunks[:max_bullets])]
    if len(chunks) > max_bullets:
        lines.append(f"  … plus {len(chunks) - max_bullets} more — see show notes.")
    return "\n".join(lines)


def _summary_chunks(summary: str) -> list[str]:
    return [c.strip() for c in re.split(r"[;\n]+", summary or "") if c.strip()]


def _summary_count(summary: str) -> int:
    return len(_summary_chunks(summary))


# ── Send ────────────────────────────────────────────────────────────────────

def _send(message: str, dry_run: bool) -> int:
    """Send a Telegram message via the @DigiToby_bot Bot API directly.

    We do NOT use `openclaw message send` because openclaw defaults to
    the ARIA bot, which posts to a different chat. The agentstack-podcast
    pipeline posts to the @DigiToby_bot bot (the one this conversation
    is on), and it does so via a direct HTTP POST to the Telegram Bot
    API, not via the openclaw CLI.
    """
    if dry_run:
        print("DRY-RUN: would post to Telegram via @DigiToby_bot:")
        print("---")
        print(message)
        print("---")
        return 0
    token = _load_bot_token()
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_TARGET,
        "text": message,
        "disable_web_page_preview": "true",
    }).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read())
    except Exception as exc:
        print(f"notify_telegram_review: FAIL telegram post: {exc}", file=sys.stderr)
        return 1
    if not result.get("ok"):
        print(f"notify_telegram_review: FAIL telegram API: {result}", file=sys.stderr)
        return 1
    _persist_send_record(_active_ep, _active_intent, json.dumps(result.get("result", {})))
    return 0


def _send_audio_file(audio_file: str, caption: str, dry_run: bool) -> int:
    """Send the actual MP3 to Telegram after the review text post.

    EP080 lesson: the review surface must include the playable audio itself,
    not only a CDN link, so Toby can review directly in Telegram.
    """
    if not audio_file:
        return 0
    path = Path(audio_file)
    if not path.exists():
        print(f"notify_telegram_review: FAIL audio file missing: {path}", file=sys.stderr)
        return 1
    if dry_run:
        print(f"DRY-RUN: would send Telegram audio attachment: {path}")
        return 0
    token = _load_bot_token()
    boundary = f"----agentstack{int(time.time() * 1000)}"
    mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
    fields = {"chat_id": TELEGRAM_TARGET, "caption": caption}
    body = bytearray()
    for key, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
        body.extend(str(value).encode())
        body.extend(b"\r\n")
    body.extend(f"--{boundary}\r\n".encode())
    body.extend((
        f'Content-Disposition: form-data; name="audio"; filename="{path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode())
    body.extend(path.read_bytes())
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendAudio",
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            result = json.loads(r.read())
    except Exception as exc:
        print(f"notify_telegram_review: FAIL telegram audio post: {exc}", file=sys.stderr)
        return 1
    if not result.get("ok"):
        print(f"notify_telegram_review: FAIL telegram audio API: {result}", file=sys.stderr)
        return 1
    return 0


# ── Intent dispatchers ──────────────────────────────────────────────────────

def _intent_ready(args: argparse.Namespace) -> int:
    status = "verified" if args.verified else "not yet verified"
    msg = READY_TEMPLATE.format(
        ep=args.ep,
        audio_url=args.audio_url,
        cover_url=args.cover_url,
        show_notes_url=args.show_notes_url,
        transcript_url=args.transcript_url,
        duration=args.duration or "unknown",
        sha256_short=(args.sha256 or "")[:12],
        status=status,
        summary_lines=_format_summary(args.summary or ""),
        slate_count=_summary_count(args.summary or ""),
    )
    rc = _send(msg, args.dry_run)
    if rc != 0:
        return rc
    return _send_audio_file(
        args.audio_file,
        f"EP{args.ep:03d} review audio — reply publish to ship / reply with feedback to rebuild.",
        args.dry_run,
    )


def _intent_failed(args: argparse.Namespace) -> int:
    msg = FAILED_TEMPLATE.format(
        ep=args.ep,
        reason=args.reason or "build",
        detail=(args.detail or "(no detail)")[:600],
        build_log=args.build_log or "/tmp/show_notes_build.log",
    )
    return _send(msg, args.dry_run)


def _intent_shipped(args: argparse.Namespace) -> int:
    msg = SHIPPED_TEMPLATE.format(
        ep=args.ep,
        canonical_url=args.canonical_url or args.audio_url,
        cdn_url=args.cdn_url or args.audio_url,
        pub_date=args.pub_date or "(unknown)",
    )
    return _send(msg, args.dry_run)


def _intent_skipped(args: argparse.Namespace) -> int:
    msg = SKIPPED_TEMPLATE.format(
        ep=args.ep,
        reason=args.reason or "unspecified",
        detail=args.detail or "(no detail)",
        rule=args.rule or "(no rule)",
        run_log=args.run_log or "/tmp/show_notes_research.log",
        build_log=args.build_log or "/tmp/show_notes_build.log",
    )
    return _send(msg, args.dry_run)


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    global _active_ep, _active_intent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ep", type=int, required=True)
    parser.add_argument(
        "--intent", required=True,
        choices=["ready", "failed", "shipped", "skipped"],
    )
    parser.add_argument("--audio-url", default="")
    parser.add_argument("--audio-file", default="")
    parser.add_argument("--cover-url", default="")
    parser.add_argument("--show-notes-url", default="")
    parser.add_argument("--transcript-url", default="")
    parser.add_argument("--duration", default="")
    parser.add_argument("--sha256", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--verified", action="store_true",
                        help="URLs have been verified live on GitHub Pages")
    parser.add_argument("--canonical-url", default="")
    parser.add_argument("--cdn-url", default="")
    parser.add_argument("--pub-date", default="")
    parser.add_argument("--reason", default="")
    parser.add_argument("--detail", default="")
    parser.add_argument("--rule", default="")
    parser.add_argument("--run-log", default="")
    parser.add_argument("--build-log", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    _active_ep = args.ep
    _active_intent = args.intent

    if args.intent == "ready":
        return _intent_ready(args)
    if args.intent == "failed":
        return _intent_failed(args)
    if args.intent == "shipped":
        return _intent_shipped(args)
    if args.intent == "skipped":
        return _intent_skipped(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())

