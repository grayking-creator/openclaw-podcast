#!/usr/bin/env python3
"""
Detached launcher and watchdog for scripts/release_episode_approved.py.

The approved release can run for hours. This wrapper starts it in a new session
so it survives the command process that triggered it, then starts a tiny watcher
that posts to the build log if the child disappears before reaching a terminal
state.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import release_episode as rel
import release_approval_gate as approval_gate


SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
LOG_DIR = PODCAST_DIR / "logs"

TERMINAL_STATUSES = {"complete", "failed", "interrupted", "paused", "exited_early"}


def post_build_log(ep_num: int, msg: str) -> None:
    try:
        rel.build_log(msg, ep_num)
    except Exception:
        pass


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def redacted_log_tail(log_path: Path, max_lines: int = 4) -> str:
    try:
        lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return ""
    tail = [line.strip() for line in lines[-max_lines:] if line.strip()]
    if not tail:
        return ""
    rendered = " | ".join(tail)
    return rendered.replace(str(Path.home()), "~")[:900]


def monitor_child(ep_num: int, pid: int, log_path: Path, poll_seconds: int) -> int:
    while process_alive(pid):
        time.sleep(poll_seconds)

    time.sleep(5)
    state = rel.load_state(ep_num)
    meta = state.get("approved_orchestrator", {})
    status = str(meta.get("run_status") or "unknown")
    completed = set(meta.get("completed_steps") or [])
    if status in TERMINAL_STATUSES or "discord" in completed:
        return 0

    step = str(meta.get("current_step") or "unknown step")
    heartbeat = str(meta.get("last_heartbeat_at") or "unknown time")
    tail = redacted_log_tail(log_path)
    detail = f" Last log: {tail}" if tail else ""
    post_build_log(
        ep_num,
        f"❌ Approved release watcher: process exited before completion "
        f"(status {status}, step {step}, heartbeat {heartbeat}).{detail} "
        "Rerun the approved release launcher to resume.",
    )
    # Run-stopping failures also go to Telegram (operator rule, 2026-07-07).
    # Best-effort; the watcher's exit code is the record of truth.
    subprocess.run(
        [
            sys.executable, str(SCRIPTS_DIR / "notify_telegram_review.py"),
            "--ep", str(ep_num), "--intent", "failed",
            "--reason", f"release ({step})",
            "--detail", f"process exited before completion (status {status})."
                        " Rerun the approved release launcher to resume.",
            "--build-log", str(log_path),
        ],
        check=False, capture_output=True, timeout=60,
    )
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start an approved release detached with a watcher")
    parser.add_argument("episode", type=int, nargs="?", help="Episode number (e.g. 53)")
    parser.add_argument("--pub-date", help="RSS pubDate string")
    parser.add_argument("--reset", action="store_true", help="Clear only approved release progress markers")
    parser.add_argument(
        "--audio-approved-by-toby",
        action="store_true",
        help="Record Toby's explicit approval of the current EN review audio before launching; requires --approval-message-id",
    )
    parser.add_argument(
        "--audio-approved-by-telegram",
        action="store_true",
        help="Record operator-confirmed Telegram approval (no Discord message id needed). "
             "This is the default approval path as of 2026-06-27; the launcher is "
             "invoked from the Telegram chat that received the review-post, so the "
             "✅ reply is the operator confirmation. The audio SHA is verified to "
             "match the review post before the release starts.",
    )
    parser.add_argument(
        "--approver",
        default="Toby (Telegram)",
        help="Approver name recorded in release state. Defaults to 'Toby (Telegram)'.",
    )
    parser.add_argument(
        "--approval-message-id",
        help="Discord message id for Toby's approving reply in the episode review channel",
    )
    parser.add_argument("--from-step", help="Pass-through recovery step for release_episode_approved.py")
    parser.add_argument("--through-step", help="Pass-through stop step for release_episode_approved.py")
    parser.add_argument("--youtube-video-mode", choices=["static", "flux"], help="Static cover video or FLUX videos")
    parser.add_argument("--monitor-pid", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--monitor-episode", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--log", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--poll-seconds", type=int, default=20, help=argparse.SUPPRESS)
    return parser.parse_args()


def child_command(args: argparse.Namespace) -> list[str]:
    if args.episode is None:
        raise SystemExit("episode is required")
    cmd = [sys.executable, str(SCRIPTS_DIR / "release_episode_approved.py"), str(args.episode)]
    if args.pub_date:
        cmd.extend(["--pub-date", args.pub_date])
    if args.reset:
        cmd.append("--reset")
    if args.from_step:
        cmd.extend(["--from-step", args.from_step])
    if args.through_step:
        cmd.extend(["--through-step", args.through_step])
    if args.youtube_video_mode:
        cmd.extend(["--youtube-video-mode", args.youtube_video_mode])
    return cmd


def launch(args: argparse.Namespace) -> int:
    if args.episode is None:
        raise SystemExit("episode is required")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ep_num = args.episode
    ep_str = f"{ep_num:03d}"
    state = rel.load_state(ep_num)
    audio_path = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    if args.audio_approved_by_toby and not args.approval_message_id:
        raise SystemExit("--audio-approved-by-toby requires --approval-message-id from Toby's review-channel reply")
    if args.audio_approved_by_toby and args.audio_approved_by_telegram:
        raise SystemExit(
            "Pass EITHER --audio-approved-by-toby (legacy Discord path) OR "
            "--audio-approved-by-telegram (default). They are mutually exclusive."
        )
    # Default: Telegram approval path. The launcher is invoked from the
    # Telegram chat that received the review post; the ✅ reply is the
    # operator confirmation. No third-party message id is needed.
    if not args.audio_approved_by_toby:
        if not state.get("audio_approval", {}).get("approved") is True \
                or not args.audio_approved_by_telegram:
            # First time: require the explicit flag to record the approval.
            # On subsequent runs the approval is already in state and the
            # launcher resumes without re-confirming.
            pass
        if args.audio_approved_by_telegram:
            approval_gate.mark_audio_approved_from_telegram(
                state,
                audio_path=audio_path,
                ep_num=ep_num,
                approver=args.approver,
            )
            rel.save_state(ep_num, state)
    if args.approval_message_id:
        approval_gate.mark_audio_approved_from_discord(
            state,
            audio_path=audio_path,
            ep_num=ep_num,
            approval_message_id=args.approval_message_id,
            token=rel.load_env_key("DISCORD_BOT_TOKEN"),
        )
        rel.save_state(ep_num, state)
    if not state.get("audio_approval", {}).get("approved"):
        state = approval_gate.mark_audio_approved_from_recent_telegram_text(
            state,
            audio_path=audio_path,
            ep_num=ep_num,
            approver=args.approver,
        )
        if state.get("audio_approval", {}).get("approved"):
            rel.save_state(ep_num, state)
    approval_gate.assert_audio_approved(state, audio_path=audio_path, ep_num=ep_num)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"ep{ep_str}_approved_release_{ts}.log"
    monitor_log_path = LOG_DIR / f"ep{ep_str}_approved_release_{ts}.watcher.log"

    cmd = child_command(args)
    with log_path.open("a", encoding="utf-8") as child_log:
        child_log.write(f"EP{ep_str} approved release detached launch {datetime.now(timezone.utc).isoformat()}\n")
        child_log.flush()
        proc = subprocess.Popen(
            cmd,
            cwd=str(PODCAST_DIR),
            stdin=subprocess.DEVNULL,
            stdout=child_log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            close_fds=True,
        )

    pid_path = log_path.with_suffix(log_path.suffix + ".pid")
    pid_path.write_text(f"{proc.pid}\n", encoding="utf-8")

    monitor_cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--monitor-pid",
        str(proc.pid),
        "--monitor-episode",
        str(ep_num),
        "--log",
        str(log_path),
    ]
    with monitor_log_path.open("a", encoding="utf-8") as monitor_log:
        subprocess.Popen(
            monitor_cmd,
            cwd=str(PODCAST_DIR),
            stdin=subprocess.DEVNULL,
            stdout=monitor_log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            close_fds=True,
        )

    post_build_log(ep_num, "🚀 Approved release recovery started.")
    print(f"EP{ep_str} approved release launched")
    print(f"pid: {proc.pid}")
    print(f"log: {log_path}")
    print(f"watcher: {monitor_log_path}")
    return 0


def main() -> int:
    args = parse_args()
    if args.monitor_pid is not None:
        if args.monitor_episode is None or args.log is None:
            raise SystemExit("--monitor-episode and --log are required with --monitor-pid")
        return monitor_child(args.monitor_episode, args.monitor_pid, args.log, args.poll_seconds)
    return launch(args)


if __name__ == "__main__":
    sys.exit(main())
