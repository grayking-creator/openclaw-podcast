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
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start an approved release detached with a watcher")
    parser.add_argument("episode", type=int, nargs="?", help="Episode number (e.g. 53)")
    parser.add_argument("--pub-date", help="RSS pubDate string")
    parser.add_argument("--reset", action="store_true", help="Clear only approved release progress markers")
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
            stdout=monitor_log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            close_fds=True,
        )

    post_build_log(ep_num, f"🚀 Approved release detached launcher started (pid {proc.pid}).")
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
