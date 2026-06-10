#!/usr/bin/env python3
"""Guarded pre-greenlight audio attempt for one AgentStack episode.

This wrapper makes the show-notes -> transcript -> build path observable:
every failure posts a concrete Build Log error instead of leaking an agent
runtime message back to the episode channel.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
WORKSPACE_DIR = PODCAST_DIR.parent
BUILD_LOG_HELPER = WORKSPACE_DIR / "scripts/utils/post_build_log.py"
BUILD_LOG_CHANNEL = "1485243812442804327"


def run(cmd: list[str], *, cwd: Path = PODCAST_DIR, log_path: Path | None = None) -> subprocess.CompletedProcess[str]:
    started = time.time()
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"\n\n$ {' '.join(cmd)}\n")
            fh.flush()
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = proc.stdout or ""
    if log_path:
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"# exit={proc.returncode} elapsed={time.time() - started:.1f}s\n")
            fh.write(output)
    return proc


def load_token() -> str:
    env_file = Path.home() / ".openclaw/.env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("DISCORD_BOT_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"')
    return ""


def post_build_log(message: str) -> None:
    if BUILD_LOG_HELPER.exists():
        subprocess.run([sys.executable, str(BUILD_LOG_HELPER), message], check=False)
        return
    token = load_token()
    if not token:
        print(f"[build-log unavailable] {message}", flush=True)
        return
    payload = json.dumps({"content": message}).encode("utf-8")
    req = urllib.request.Request(
        f"https://discord.com/api/v10/channels/{BUILD_LOG_CHANNEL}/messages",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "OpenClaw Podcast Audio Guard",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15):
            pass
    except Exception as exc:
        print(f"[build-log post failed] {exc}: {message}", flush=True)


def fail(ep_str: str, phase: str, detail: str, log_path: Path) -> int:
    post_build_log(
        f"❌ EP{ep_str} audio attempt failed during {phase}: {detail}\n"
        f"Log: `{log_path}`"
    )
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guarded review-audio attempt; with --feedback, revises the transcript "
                    "from reviewer audio feedback and rebuilds the audio in one pass."
    )
    parser.add_argument("episode", type=int)
    parser.add_argument("--feedback", default="",
                        help="Reviewer audio feedback — regenerate the transcript to address it, then rebuild audio")
    parser.add_argument("--feedback-file", default="",
                        help="Path to a file with reviewer audio feedback (alternative to --feedback)")
    args = parser.parse_args()

    ep_num = args.episode
    ep_str = f"{ep_num:03d}"
    notes_path = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    transcript_path = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript.md"
    audio_path = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    log_path = Path(f"/tmp/ep{ep_str}_audio_attempt.log")

    feedback = args.feedback.strip()
    if args.feedback_file:
        fb_path = Path(args.feedback_file)
        if not fb_path.exists():
            return fail(ep_str, "preflight", f"feedback file not found `{fb_path}`", log_path)
        feedback = (feedback + "\n" + fb_path.read_text(encoding="utf-8", errors="ignore")).strip()

    if feedback:
        post_build_log(f"🎙 EP{ep_str} review-audio REVISION started: revising transcript from your audio feedback → rebuilding audio")
    else:
        post_build_log(f"🎙 EP{ep_str} audio attempt started: show notes → transcript → build_episode.py")

    if not notes_path.exists():
        return fail(ep_str, "preflight", f"missing show notes `{notes_path.name}`", log_path)

    qc_notes = run([sys.executable, "scripts/check_show_notes.py", str(notes_path)], log_path=log_path)
    if qc_notes.returncode != 0:
        return fail(ep_str, "show-notes QC", "show notes failed `check_show_notes.py`", log_path)

    # Feedback forces a transcript revision; otherwise only generate if missing.
    if feedback or not transcript_path.exists():
        gen_cmd = [sys.executable, "scripts/generate_episode_transcript.py", str(ep_num)]
        if feedback:
            post_build_log(f"📝 EP{ep_str} revising transcript to address your audio feedback (auto-repairs QC failures)")
            gen_cmd += ["--force", "--feedback", feedback]
        else:
            post_build_log(f"📝 EP{ep_str} transcript missing — generating directly from approved show notes with OpenAI")
        transcript = run(gen_cmd, log_path=log_path)
        if transcript.returncode != 0 or not transcript_path.exists():
            return fail(
                ep_str,
                "transcript revision" if feedback else "transcript generation",
                (
                    f"`generate_episode_transcript.py` did not produce `{transcript_path.name}`. "
                    "No nested agent fallback was used."
                ),
                log_path,
            )

    qc_transcript = run([sys.executable, "scripts/check_episode.py", str(transcript_path)], log_path=log_path)
    if qc_transcript.returncode != 0:
        return fail(ep_str, "transcript QC", "`check_episode.py` rejected the transcript", log_path)

    build = run([sys.executable, "scripts/build_episode.py", str(ep_num), "--force-audio"], log_path=log_path)
    if build.returncode != 0:
        return fail(ep_str, "audio build", "`build_episode.py` exited nonzero", log_path)

    if not audio_path.exists() or audio_path.stat().st_size < 1_000_000:
        return fail(ep_str, "audio verification", "canonical audio file missing or too small after build", log_path)

    post_build_log(f"✅ EP{ep_str} audio attempt completed; review audio build finished and URLs should be posted by build_episode.py")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        ep_arg = sys.argv[1] if len(sys.argv) > 1 else "unknown"
        try:
            ep_str = f"{int(ep_arg):03d}"
        except ValueError:
            ep_str = str(ep_arg)
        log_path = Path(f"/tmp/ep{ep_str}_audio_attempt.log")
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"\n\nUNCAUGHT {type(exc).__name__}: {exc}\n")
        post_build_log(f"❌ EP{ep_str} audio attempt crashed before completion: {type(exc).__name__}: {exc}\nLog: `{log_path}`")
        raise
