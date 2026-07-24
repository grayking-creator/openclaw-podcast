#!/usr/bin/env python3
"""
ARIA Telegram review notifier plus Discord failure router.

Complements the Discord episode review post for AgentStack Daily:

  --intent ready      post the morning "ready to review" message with the
                       audio + cover + show notes + transcript URLs and the
                       complete slate summary. Approval is recorded only from
                       a later verified reply in the Discord episode channel.
  --intent shipped    post the post-approval "shipped" confirmation with the
                       canonical episode link and CDN URL.
  --intent failed     route a run-stopping failure to the Discord build log.
  --intent skipped    route a skipped-build reason to the Discord build log.

ARIA Telegram is for listenable review audio and shipped confirmation only.
Status, warnings, failures, and pipeline narration go to Discord. Publication
approval is verified from a later non-bot reply in the Discord episode channel;
the ARIA message is a convenient listening duplicate, not an approval source.

Send-record persistence: after every successful send, the message id and
chat id, ARIA account id, and audio hash are saved to
scripts/.telegram_send_records/ep{NNN}.json for routing/audit evidence.

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
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPT_DIR.parent

TELEGRAM_CHANNEL = "telegram"
TELEGRAM_TARGET = "8319992332"
# Locked 2026-07-10: podcast review audio is back on ARIA's Telegram account.
# Every send names ``default`` explicitly so a future additional Telegram
# account cannot silently capture the review workflow.
TELEGRAM_ACCOUNT = "default"
OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "/opt/homebrew/bin/openclaw")

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
    "Approval is recorded from your ✅ reply in the Discord episode channel. "
    "Send feedback here or there to rebuild."
)

# Telegram routing: only the listenable ready post and shipped confirmation.
# Failures, warnings, progress, and mid-stream gates belong in the Discord
# build log. The failed/skipped templates remain for callers but are dispatched
# by _post_discord_build_log(), never by the Telegram sender.
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
_active_audio_sha: Optional[str] = None


# ── Send-record persistence ──────────────────────────────────────────────────

def _persist_send_record(
    ep: Optional[int],
    intent: Optional[str],
    raw: str,
    *,
    media_message: bool = False,
) -> None:
    """Persist the message id + chat id returned by the openclaw CLI.

    Best-effort: failures to parse or write the record are swallowed.
    Discord remains the canonical approval anchor; this record proves which
    ARIA message carried the playable duplicate.
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
    candidates = [parsed]
    for parent in list(candidates):
        for key in ("payload", "result", "sendResult"):
            nested = parent.get(key) if isinstance(parent, dict) else None
            if isinstance(nested, dict):
                candidates.append(nested)
                nested_result = nested.get("result")
                if isinstance(nested_result, dict):
                    candidates.append(nested_result)
    msg_id = None
    chat_id = None
    for candidate in candidates:
        msg_id = msg_id or candidate.get("messageId") or candidate.get("message_id") or candidate.get("id")
        chat_id = chat_id or candidate.get("chatId") or candidate.get("chat_id")
        chat = candidate.get("chat") or {}
        if not chat_id and isinstance(chat, dict):
            chat_id = chat.get("id")
    if msg_id and not chat_id:
        chat_id = TELEGRAM_TARGET
    if not msg_id and not chat_id:
        return
    try:
        SEND_RECORD_DIR.mkdir(parents=True, exist_ok=True)
        record_path = SEND_RECORD_DIR / f"ep{ep:03d}.json"
        record: dict = {"updated_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        if record_path.exists():
            try:
                existing = json.loads(record_path.read_text())
                if isinstance(existing, dict):
                    existing.update(record)
                    record = existing
            except Exception:
                pass
        intent_record = record.setdefault(intent, {})
        if media_message:
            intent_record["audio_message_id"] = str(msg_id) if msg_id else None
        else:
            intent_record["message_id"] = str(msg_id) if msg_id else None
        intent_record.update({
            "chat_id": str(chat_id) if chat_id else None,
            "account_id": TELEGRAM_ACCOUNT,
            "review_audio_sha256": _active_audio_sha if intent == "ready" else None,
        })
        record["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
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
    # Current callers serialize one headline per line so punctuation inside a
    # title stays intact. Semicolons remain a legacy fallback for older callers.
    if "\n" in (summary or ""):
        return [line.strip() for line in summary.splitlines() if line.strip()]
    return [chunk.strip() for chunk in summary.split(";") if chunk.strip()]


def _summary_count(summary: str) -> int:
    return len(_summary_chunks(summary))


# ── Send ────────────────────────────────────────────────────────────────────

def _send(message: str, dry_run: bool) -> int:
    """Send through OpenClaw's explicit ARIA Telegram account."""
    cmd = [
        OPENCLAW_BIN, "message", "send",
        "--channel", TELEGRAM_CHANNEL,
        "--account", TELEGRAM_ACCOUNT,
        "--target", TELEGRAM_TARGET,
        "--message", message,
        "--json",
    ]
    if dry_run:
        cmd.append("--dry-run")
    proc = None
    detail = "unknown error"
    for attempt, delay in enumerate((0, 2, 5), start=1):
        if delay:
            time.sleep(delay)
        try:
            proc = subprocess.run(
                cmd, check=False, capture_output=True, text=True, timeout=30,
            )
            if proc.returncode == 0:
                break
            detail = (proc.stderr or proc.stdout or "unknown error").strip()
        except Exception as exc:
            detail = str(exc)
        if attempt < 3:
            print(
                f"notify_telegram_review: retrying ARIA Telegram post after attempt {attempt}: {detail}",
                file=sys.stderr,
            )
    if proc is None or proc.returncode != 0:
        print(f"notify_telegram_review: FAIL OpenClaw Telegram post: {detail}", file=sys.stderr)
        return 1
    if dry_run:
        print(proc.stdout.strip())
    else:
        _persist_send_record(_active_ep, _active_intent, proc.stdout.strip())
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
    cmd = [
        OPENCLAW_BIN, "message", "send",
        "--channel", TELEGRAM_CHANNEL,
        "--account", TELEGRAM_ACCOUNT,
        "--target", TELEGRAM_TARGET,
        "--message", caption,
        "--media", str(path),
        "--json",
    ]
    if dry_run:
        cmd.append("--dry-run")
    try:
        proc = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=180,
        )
    except Exception as exc:
        print(f"notify_telegram_review: FAIL OpenClaw Telegram audio post: {exc}", file=sys.stderr)
        return 1
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "unknown error").strip()
        print(f"notify_telegram_review: FAIL OpenClaw Telegram audio post: {detail}", file=sys.stderr)
        return 1
    if dry_run:
        print(proc.stdout.strip())
    else:
        _persist_send_record(
            _active_ep,
            _active_intent,
            proc.stdout.strip(),
            media_message=True,
        )
    return 0


def _post_discord_build_log(message: str, dry_run: bool) -> int:
    """Route non-listenable pipeline notices to the Discord build log."""
    if dry_run:
        print("DRY-RUN: would post to the Discord build log:")
        print(message)
        return 0
    try:
        helper_dir = Path.home() / ".openclaw/workspace/scripts/utils"
        if str(helper_dir) not in sys.path:
            sys.path.insert(0, str(helper_dir))
        from post_build_log import post_build_log

        post_build_log(message)
        return 0
    except (Exception, SystemExit) as exc:
        print(f"notify_telegram_review: FAIL Discord build-log post: {exc}", file=sys.stderr)
        return 1


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
        f"EP{args.ep:03d} review audio — approve with ✅ in the Discord episode channel; send feedback here or there to rebuild.",
        args.dry_run,
    )


def _intent_failed(args: argparse.Namespace) -> int:
    msg = FAILED_TEMPLATE.format(
        ep=args.ep,
        reason=args.reason or "build",
        detail=(args.detail or "(no detail)")[:600],
        build_log=args.build_log or "/tmp/show_notes_build.log",
    )
    return _post_discord_build_log(msg, args.dry_run)


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
    return _post_discord_build_log(msg, args.dry_run)


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    global _active_ep, _active_intent, _active_audio_sha
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
    _active_audio_sha = args.sha256 or None

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
