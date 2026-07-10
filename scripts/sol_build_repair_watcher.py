#!/usr/bin/env python3
"""Watch #build-log-errors and dispatch a Sol repair agent for new failures.

Every deterministic pipeline on this machine and the DGX posts its
unrecoverable errors to the #build-log-errors Discord channel (via
scripts/utils/post_build_log.py severity routing). This watcher polls that
channel and, for each new actionable failure, runs one autonomous repair turn
on the OpenClaw gateway with the GPT-5.6 Sol model so the problem is being
worked before Toby ever sees it — the 9am episode deadline must not depend on
manual intervention.

Dispatch rules:
  - Only failure posts are actionable (❌ / 🚨 / [FAIL] / "FAILED").
  - [RETRY] posts are skipped — the pipeline is already retrying itself.
  - [HOLD] / 🛑 posts are skipped — holds are deliberate approval-workflow
    stops that only Toby resolves (audio approval is never inferred).
  - "🔧 Sol repair" posts are skipped — that's this system talking.
  - Each error signature gets at most MAX_ATTEMPTS_PER_SIGNATURE repair
    attempts per ATTEMPT_WINDOW_HOURS, so a truly stuck failure cannot burn
    the model in a loop.

Usage:
  sol_build_repair_watcher.py --poll        # normal cron entry point
  sol_build_repair_watcher.py --once        # single poll (guard kicks this on final FAIL)
  sol_build_repair_watcher.py --bootstrap   # mark current channel history as seen, no repairs
  sol_build_repair_watcher.py --dry-run     # show what would be dispatched, don't run the agent

Environment overrides:
  SOL_REPAIR_MODEL     agent model (default: openai/gpt-5.6-sol)
  SOL_REPAIR_TIMEOUT   seconds per repair turn (default: 2700)
  SOL_REPAIR_CHANNEL   channel id to watch (default: build-log-errors)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
WORKSPACE_DIR = PODCAST_DIR.parent
BUILD_LOG_HELPER = WORKSPACE_DIR / "scripts/utils/post_build_log.py"

ERROR_CHANNEL = os.environ.get("SOL_REPAIR_CHANNEL", "1524923755019636948")
REPAIR_MODEL = os.environ.get("SOL_REPAIR_MODEL", "openai/gpt-5.6-sol")
REPAIR_TIMEOUT = int(os.environ.get("SOL_REPAIR_TIMEOUT", "2700"))
OPENCLAW_BIN = "/opt/homebrew/bin/openclaw"

STATE_PATH = SCRIPTS_DIR / ".sol_repair_state.json"
LOCK_PATH = Path("/tmp/sol_build_repair_watcher.lock")
LOCK_MAX_AGE_S = 2 * 3600
LOG_PREFIX = "sol_build_repair_watcher"

MAX_ATTEMPTS_PER_SIGNATURE = 2
ATTEMPT_WINDOW_HOURS = 24
MAX_DISPATCHES_PER_RUN = 1  # one repair per poll; cron picks up the rest

ACTIONABLE_MARKERS = ("❌", "🚨", "🔴", "[FAIL]", "FAILED")
SKIP_MARKERS = ("[RETRY]", "auto-retry", "[HOLD]", "🛑", "🔧 Sol repair")


def log(msg: str) -> None:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {LOG_PREFIX}: {msg}", flush=True)


def load_token() -> str:
    env_file = Path.home() / ".openclaw/.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("DISCORD_BOT_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("DISCORD_BOT_TOKEN", "")


def discord_get_messages(token: str, after: str | None) -> list[dict]:
    url = f"https://discord.com/api/v10/channels/{ERROR_CHANNEL}/messages?limit=50"
    if after:
        url += f"&after={after}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bot {token}",
            "User-Agent": "OpenClaw Sol Repair Watcher",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        messages = json.loads(resp.read().decode("utf-8"))
    # Discord returns newest first; process oldest first.
    return sorted(messages, key=lambda m: int(m["id"]))


def post_build_log(message: str, *, error: bool = False) -> None:
    if not BUILD_LOG_HELPER.exists():
        log(f"WARN missing build-log helper: {BUILD_LOG_HELPER}")
        return
    flag = "--error" if error else "--info"
    subprocess.run(
        [sys.executable, str(BUILD_LOG_HELPER), flag, message],
        check=False, timeout=30, capture_output=True,
    )


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            log("WARN state file unreadable — starting fresh (bootstrap semantics)")
    return {"last_seen_id": None, "attempts": {}, "handled": []}


def save_state(state: dict) -> None:
    state["handled"] = state.get("handled", [])[-500:]
    tmp = STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)


def error_signature(content: str) -> str:
    """Stable signature for 'the same error again': lowercase, digits and
    volatile tokens (ids, hashes, timestamps, paths' episode numbers) removed."""
    text = content.lower()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[0-9a-f]{8,}", "", text)  # message ids, hashes
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha1(text[:400].encode("utf-8")).hexdigest()[:16]


def is_actionable(content: str) -> tuple[bool, str]:
    if any(marker in content for marker in SKIP_MARKERS):
        return False, "retry/hold/self post"
    if not any(marker in content for marker in ACTIONABLE_MARKERS):
        return False, "not a failure post (warning/info)"
    return True, ""


def attempts_in_window(state: dict, signature: str) -> int:
    cutoff = time.time() - ATTEMPT_WINDOW_HOURS * 3600
    stamps = [t for t in state.get("attempts", {}).get(signature, []) if t >= cutoff]
    state.setdefault("attempts", {})[signature] = stamps
    return len(stamps)


def build_repair_prompt(message: dict) -> str:
    content = message.get("content", "")
    msg_id = message.get("id", "?")
    timestamp = message.get("timestamp", "?")
    return f"""You are Sol, the automated build-repair agent for Toby's OpenClaw pipelines. A pipeline failure was posted to Discord #build-log-errors and you must diagnose and FIX it now, autonomously — Toby must not need to intervene, and the daily podcast must be listenable by 9am ET.

--- ERROR MESSAGE (#build-log-errors, message {msg_id}, {timestamp}) ---
{content}
--- END ERROR MESSAGE ---

Environment map:
- Podcast pipeline repo: /Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast — all cron/build scripts in scripts/. Morning run log: /tmp/show_notes_research.log; build log: /tmp/show_notes_build.log.
- Shorts uploader log: /Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/content_staging/shorts/upload_cron.log. YouTube episode cron log: /tmp/youtube_upload_cron.log.
- DGX Spark (CUDA, website + blog pipelines): ssh toby@192.168.1.6
- M4 Max repair account: ssh toby@tobyM4Max.local (user 'toby', NOT 'tobyglennpeters').
- The transcript stage already has its own internal gpt-5.6-sol rescue loop; if a transcript failure reached this channel anyway, read the run-log tail first — the cause is usually upstream (providers, prompt assembly, QC contradiction), not one more retry.
- The morning pipeline (scripts/agentstack_morning.sh) is resume-safe: rerunning it resumes from completed stages. Rerun it via: /bin/bash scripts/show_notes_research_guard.sh

Do this, in order:
1. Read the relevant log tails and find the root cause. Do not guess from the Discord message alone.
2. Apply the smallest safe fix (script/config repair, cleanup of a bad artifact, restart of a wedged process).
3. Re-run the failed stage or its resume-safe wrapper to verify the fix actually clears the failure.
4. Post ONE summary of what you found, what you changed, and the verification result:
   python3 /Users/tobyglennpeters/.openclaw/workspace/scripts/utils/post_build_log.py --info "🔧 Sol repair: <root cause> — <fix> — <verified outcome>"

HARD LIMITS — violating these is worse than leaving the error unfixed:
- NEVER release, publish, or approve an episode, and never treat this repair task as approval. Audio approval comes ONLY from Toby after listening. Do not run release_episode.py, launch_approved_release.py, or any full-episode YouTube upload. Rebuilding REVIEW artifacts (show notes, transcript, review audio) is allowed and encouraged.
- Never upload shorts manually or in a loop — shorts ship only via their crontab scheduler.
- Never force push. Never delete episodic/semantic memory. Never edit .agent/protocols/permissions.md.
- Post status only via the post_build_log.py helper above — never to episode channels, never to Telegram.
- If the fix genuinely requires Toby (expired credentials/OAuth, a listening approval, physical hardware), post exactly one line starting "🔧 Sol repair BLOCKED:" with --error explaining what he must do, then stop."""


def dispatch_repair(message: dict, dry_run: bool) -> bool:
    # Defense in depth: this is the ONLY function in the watcher that spends
    # model tokens. Re-verify the deterministic gate here so no future caller
    # can reach the LLM with a non-error message.
    actionable, why = is_actionable(message.get("content", ""))
    if not actionable:
        log(f"REFUSED dispatch for {message.get('id', '?')}: {why} "
            f"(deterministic gate; no model call made)")
        return False
    msg_id = message["id"]
    excerpt = " ".join(message.get("content", "").split())[:180]
    if dry_run:
        log(f"DRY-RUN would dispatch Sol repair for message {msg_id}: {excerpt}")
        return True
    log(f"dispatching Sol repair for message {msg_id}: {excerpt}")
    post_build_log(f"🔧 Sol repair dispatched (msg {msg_id}): {excerpt}")
    prompt = build_repair_prompt(message)
    cmd = [
        OPENCLAW_BIN, "agent",
        "--model", REPAIR_MODEL,
        "--session-key", f"agent:main:sol-repair-{msg_id}",
        "--thinking", "high",
        "--timeout", str(REPAIR_TIMEOUT),
        "--json",
        "--message", prompt,
    ]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=REPAIR_TIMEOUT + 120,
        )
    except subprocess.TimeoutExpired:
        log(f"repair turn for {msg_id} timed out after {REPAIR_TIMEOUT}s")
        post_build_log(
            f"🔧 Sol repair for msg {msg_id} timed out after {REPAIR_TIMEOUT}s — "
            f"will not auto-retry beyond the signature budget", error=True)
        return False
    reply = ""
    try:
        data = json.loads(proc.stdout)
        payloads = ((data.get("result") or {}).get("payloads")) or []
        reply = " ".join((p.get("text") or "") for p in payloads).strip()
        status = data.get("status", "?")
    except (json.JSONDecodeError, AttributeError):
        status = f"exit {proc.returncode}"
        reply = (proc.stdout or proc.stderr or "").strip()
    reply_short = " ".join(reply.split())[:600] or "(no reply text)"
    log(f"repair turn for {msg_id} finished: status={status}; reply: {reply_short}")
    post_build_log(f"🔧 Sol repair finished (msg {msg_id}, status {status}): {reply_short}")
    return proc.returncode == 0


def acquire_lock() -> bool:
    if LOCK_PATH.exists():
        age = time.time() - LOCK_PATH.stat().st_mtime
        if age < LOCK_MAX_AGE_S:
            log(f"another watcher run holds the lock ({int(age)}s old) — exiting")
            return False
        log(f"stale lock ({int(age)}s) — reclaiming")
    LOCK_PATH.write_text(str(os.getpid()), encoding="utf-8")
    return True


def release_lock() -> None:
    try:
        LOCK_PATH.unlink()
    except FileNotFoundError:
        pass


def poll(bootstrap: bool, dry_run: bool) -> int:
    token = load_token()
    if not token:
        log("FATAL no Discord bot token available")
        return 1
    state = load_state()
    first_run = state.get("last_seen_id") is None

    try:
        messages = discord_get_messages(token, state.get("last_seen_id"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        log(f"WARN Discord fetch failed: {exc}")
        return 1

    if not messages:
        log("no new messages")
        return 0

    newest_id = messages[-1]["id"]
    if bootstrap or first_run:
        state["last_seen_id"] = newest_id
        save_state(state)
        log(f"{'bootstrap' if bootstrap else 'first run'}: marked {len(messages)} "
            f"existing message(s) as seen up to {newest_id}; no repairs dispatched")
        return 0

    dispatched = 0
    for message in messages:
        msg_id = message["id"]
        state["last_seen_id"] = max(int(msg_id), int(state["last_seen_id"] or 0))
        state["last_seen_id"] = str(state["last_seen_id"])
        content = message.get("content", "")
        if msg_id in state.get("handled", []):
            continue
        actionable, why = is_actionable(content)
        if not actionable:
            log(f"skip {msg_id}: {why}")
            state.setdefault("handled", []).append(msg_id)
            continue
        signature = error_signature(content)
        if attempts_in_window(state, signature) >= MAX_ATTEMPTS_PER_SIGNATURE:
            log(f"skip {msg_id}: signature {signature} exhausted its "
                f"{MAX_ATTEMPTS_PER_SIGNATURE}-attempt budget in the last "
                f"{ATTEMPT_WINDOW_HOURS}h")
            post_build_log(
                f"🔧 Sol repair skipped (msg {msg_id}): same error already attempted "
                f"{MAX_ATTEMPTS_PER_SIGNATURE}x in {ATTEMPT_WINDOW_HOURS}h — needs Toby.",
                error=True)
            state.setdefault("handled", []).append(msg_id)
            continue
        if dispatched >= MAX_DISPATCHES_PER_RUN:
            log(f"dispatch budget for this run reached — {msg_id} waits for the next poll")
            break  # do NOT mark handled; next poll picks it up
        state.setdefault("attempts", {}).setdefault(signature, []).append(time.time())
        state.setdefault("handled", []).append(msg_id)
        save_state(state)  # persist before the long agent run
        dispatch_repair(message, dry_run)
        dispatched += 1

    save_state(state)
    log(f"poll complete: {dispatched} repair(s) dispatched")
    return 0


def selftest() -> int:
    """Prove the deterministic no-error → no-LLM gate with canned messages.

    Runs entirely offline: no Discord fetch, no state mutation, no agent call.
    Exits nonzero if any non-error message would reach the model or any real
    failure would be missed."""
    cases = [
        # (content, should_dispatch, label)
        ("✅ Sent via Discord. EP084 build complete", False, "success line"),
        ("🏗 EP084 build started\n✅ Show notes QC passed", False, "progress line"),
        ("📺 **EP084 YouTube status** (5/5 channels done)", False, "status line"),
        ("⚠️ **EP084 YouTube upload issues**\nWarnings only", False, "warning-only post"),
        ("[RETRY] AgentStack Daily morning run exited 1 — auto-retrying (2/2)", False, "retry post"),
        ("[HOLD] AgentStack Daily research stopped with exit 2.", False, "hold post"),
        ("🛑 EP084 morning HOLD: existing review audio is unapproved", False, "unapproved-audio hold"),
        ("🔧 Sol repair BLOCKED: YouTube OAuth expired — Toby must re-auth", False, "own blocked post"),
        ("🔧 Sol repair skipped (msg 123): same error already attempted 2x", False, "own budget post"),
        ("", False, "empty message"),
        ("❌ EP084 morning pipeline FAILED at stage: transcript", True, "stage failure"),
        ("[FAIL] AgentStack Daily research guard: script exited 1 after 2 run(s)", True, "guard failure"),
        ("❌ YouTube EP84 upload failed (exit 1). Check /tmp/youtube_upload_cron.log", True, "upload failure"),
        ("🚨 DGX website deploy unreachable from release phase", True, "DGX failure"),
    ]
    failures = 0
    for content, expected, label in cases:
        got, why = is_actionable(content)
        ok = got == expected
        failures += 0 if ok else 1
        verdict = "PASS" if ok else "FAIL"
        decision = "DISPATCH" if got else f"skip ({why})"
        print(f"  {verdict}: {label!r} -> {decision}")
    # The dispatch function itself must refuse a non-error even if called.
    refused = dispatch_repair({"id": "selftest", "content": "✅ all good"}, dry_run=True)
    if refused:
        print("  FAIL: dispatch_repair accepted a non-error message")
        failures += 1
    else:
        print("  PASS: dispatch_repair refuses non-error messages directly")
    print(f"selftest: {len(cases) + 1 - failures}/{len(cases) + 1} checks passed "
          f"(zero network calls, zero model calls)")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--poll", action="store_true", help="normal cron poll")
    mode.add_argument("--once", action="store_true", help="single poll (event-driven kick)")
    mode.add_argument("--bootstrap", action="store_true",
                      help="mark current channel history as seen; dispatch nothing")
    mode.add_argument("--selftest", action="store_true",
                      help="offline check that only real failures can reach the model")
    parser.add_argument("--dry-run", action="store_true",
                        help="log what would be dispatched without running the agent")
    args = parser.parse_args()

    if args.selftest:
        return selftest()

    if not acquire_lock():
        return 0
    try:
        return poll(bootstrap=args.bootstrap, dry_run=args.dry_run)
    finally:
        release_lock()


if __name__ == "__main__":
    raise SystemExit(main())
