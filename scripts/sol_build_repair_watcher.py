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
  - Every new post in #build-log-errors is actionable unless it is an explicit
    retry, approval hold, watcher outcome, or no-action routing test.  The
    channel itself is the severity boundary; warnings/degraded states must not
    sit there without a repair attempt.
  - [RETRY] posts are skipped — the pipeline is already retrying itself.
  - [HOLD] / 🛑 posts are skipped — holds are deliberate approval-workflow
    stops that only Toby resolves (audio approval is never inferred).
  - "🔧 Sol repair" / "AUTO-REPAIR" posts are skipped — that's this
    system talking.
  - Every source message receives its own first repair attempt. Interrupted
    retries are bounded per message, so one recurring signature cannot consume
    a different incident's attempt budget.
  - An incident is closed only after its terminal Discord outcome is delivered;
    interrupted repairs and failed terminal posts remain durable state.

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
import copy
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
STATE_VERSION = 2

MAX_ATTEMPTS_PER_MESSAGE = 2
MAX_RESULT_FIELD_CHARS = 280

RETRY_PREFIX_RE = re.compile(
    r"^\s*(?:(?:❌){1,3}\s*)?(?:\[retry\]|retry:)", re.IGNORECASE
)
HOLD_PREFIX_RE = re.compile(
    r"^\s*(?:(?:❌){1,3}\s*)?\[hold\]", re.IGNORECASE
)
APPROVAL_HOLD_RE = re.compile(
    r"^\s*(?:(?:❌){1,3}\s*)?🛑.*"
    r"(?:\bhold\b.*(?:approv|unapprov|review audio)|"
    r"(?:approv|unapprov|review audio).*\bhold\b)",
    re.IGNORECASE,
)
WATCHER_PREFIX_RE = re.compile(
    r"^\s*(?:(?:(?:❌){1,3}|👍|🔧)\s*)?(?:codex\s+)?auto-repair\b|"
    r"^\s*(?:👍|(?:❌){1,3})\s+(?:EP\d+\s+)?manual\s+recovery\s+"
    r"(?:succeeded|failed)\b.*?\bsource error\s+\d+|"
    r"^\s*🔧\s*sol\s+repair\b",
    re.IGNORECASE | re.DOTALL,
)
NO_ACTION_TEST_RE = re.compile(
    r"^\s*(?:(?:❌){1,3}\s*)?"
    r"\[(?:build\s+log\s+routing\s+check|sol-watcher-test)\]",
    re.IGNORECASE,
)
RESULT_PREFIX = "REPAIR_RESULT_JSON:"
NON_ERROR_PREFIXES = ("✅", "🏗", "📺")
OK_AGENT_STATUSES = {"ok", "success", "completed"}
NONE_ACTION_VALUES = {"none"}
NON_TERMINAL_VERIFICATION_RE = re.compile(
    r"\b(?:resum(?:e|ed|ing)|next\s+stage|downstream|in[ -]?progress|"
    r"still\s+running|start(?:ed|ing)?|launch(?:ed|ing)?|queued|"
    r"advanced?\s+to|proceed(?:ed|ing)?\s+to|moved?\s+to|"
    r"continu(?:e|ed|ing)\s+to|reached?\s+(?:the\s+)?next)\b",
    re.IGNORECASE,
)
TERMINAL_SOURCE_RE = re.compile(
    r"^\s*(?:(?:❌){1,3}|👍)\s+"
    r"(?:(?:CODEX\s+)?AUTO-REPAIR|(?:EP\d+\s+)?MANUAL\s+RECOVERY)\s+"
    r"(?:SUCCEEDED|FAILED).*?"
    r"source error\s+(\d+)",
    re.IGNORECASE | re.DOTALL,
)
PODCAST_MORNING_FAILURE_RE = re.compile(
    r"\bEP\s*0*(\d{1,4})\s+morning pipeline\s+FAILED\b",
    re.IGNORECASE,
)


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


def post_build_log(message: str, *, error: bool = False) -> bool:
    if not BUILD_LOG_HELPER.exists():
        log(f"WARN missing build-log helper: {BUILD_LOG_HELPER}")
        return False
    flag = "--error" if error else "--info"
    try:
        proc = subprocess.run(
            [sys.executable, str(BUILD_LOG_HELPER), flag, message],
            check=False,
            timeout=30,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        log(f"WARN build-log post failed before completion: {exc}")
        return False
    if proc.returncode != 0:
        detail = proc.stderr or proc.stdout or "unknown helper failure"
        log(f"WARN build-log post failed: {' '.join(detail.split())[:240]}")
        return False
    return True


def new_state() -> dict:
    return {
        "version": STATE_VERSION,
        "last_seen_id": None,
        "message_attempts": {},
        "handled": [],
        "in_progress": {},
        "pending_terminal": {},
        "outcomes": {},
    }


def normalize_state(raw: object) -> dict:
    """Return a valid state without inventing a cursor for invalid input."""
    if not isinstance(raw, dict):
        return new_state()
    if raw.get("version") == STATE_VERSION:
        required_shapes = {
            "message_attempts": dict,
            "handled": list,
            "in_progress": dict,
            "pending_terminal": dict,
            "outcomes": dict,
        }
        if any(not isinstance(raw.get(key), kind) for key, kind in required_shapes.items()):
            return new_state()
    elif (
        "handled" not in raw
        or not isinstance(raw.get("handled"), list)
        or "last_seen_id" not in raw
    ):
        # Legacy v1 is migratable only when its durable cursor companion exists.
        return new_state()
    state = new_state()
    last_seen = raw.get("last_seen_id")
    if last_seen is not None:
        try:
            state["last_seen_id"] = str(int(last_seen))
        except (TypeError, ValueError):
            return new_state()
    state["handled"] = [str(item) for item in raw.get("handled", [])]
    for key in ("message_attempts", "in_progress", "pending_terminal", "outcomes"):
        value = raw.get(key)
        if isinstance(value, dict):
            state[key] = {str(item_key): item for item_key, item in value.items()}
    return state


def load_state() -> dict:
    if not STATE_PATH.exists():
        log("WARN state file missing — replaying visible channel history; no bootstrap skip")
        return new_state()
    try:
        raw = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        log(f"WARN state file unreadable ({exc}) — replaying visible channel history")
        return new_state()
    if not isinstance(raw, dict):
        log("WARN state root is not an object — replaying visible channel history")
        return new_state()
    return normalize_state(raw)


def save_state(state: dict) -> None:
    state["version"] = STATE_VERSION
    state["handled"] = state.get("handled", [])[-500:]
    if len(state.get("outcomes", {})) > 500:
        keep = set(state["handled"][-500:])
        state["outcomes"] = {
            key: value for key, value in state["outcomes"].items() if key in keep
        }
    tmp = STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(STATE_PATH)


def is_actionable(content: str) -> tuple[bool, str]:
    stripped = content.strip()
    if not stripped:
        return False, "empty post"
    if RETRY_PREFIX_RE.match(stripped):
        return False, "active retry post"
    if HOLD_PREFIX_RE.match(stripped) or APPROVAL_HOLD_RE.match(stripped):
        return False, "approval hold post"
    if WATCHER_PREFIX_RE.match(stripped):
        return False, "watcher outcome post"
    if NO_ACTION_TEST_RE.match(stripped):
        return False, "explicit no-action routing test"
    if stripped.startswith(NON_ERROR_PREFIXES):
        return False, "misrouted success/progress post"
    # #build-log-errors is itself the severity contract.  Requiring a second
    # magic word here caused degraded rollup failures to be silently marked
    # handled without any repair attempt on 2026-07-13.
    return True, "error-channel post"


def attempt_count(state: dict, msg_id: str) -> int:
    attempts = state.get("message_attempts", {}).get(msg_id, [])
    return len(attempts) if isinstance(attempts, list) else 0


def advance_cursor(state: dict, msg_id: str) -> None:
    current = int(state.get("last_seen_id") or 0)
    state["last_seen_id"] = str(max(current, int(msg_id)))


def mark_handled(state: dict, msg_id: str) -> None:
    handled = state.setdefault("handled", [])
    if msg_id not in handled:
        handled.append(msg_id)


def reconcile_delivered_terminals(state: dict, messages: list[dict]) -> None:
    """Recover closure facts from channel history after state loss/corruption."""
    for message in messages:
        match = TERMINAL_SOURCE_RE.match(message.get("content", ""))
        if match:
            mark_handled(state, match.group(1))


def select_next_incident(messages: list[dict], state: dict) -> dict | None:
    """Advance only across durable/skipped items and stop before an incident.

    The actionable message's cursor is advanced only when it is persisted as
    in-progress, so a one-dispatch limit can never skip the following message.
    """
    tracked = set(state.get("handled", []))
    tracked.update(state.get("in_progress", {}).keys())
    tracked.update(state.get("pending_terminal", {}).keys())
    for message in messages:
        msg_id = str(message["id"])
        if msg_id in tracked:
            advance_cursor(state, msg_id)
            continue
        actionable, why = is_actionable(message.get("content", ""))
        if actionable:
            return message
        log(f"skip {msg_id}: {why}")
        mark_handled(state, msg_id)
        advance_cursor(state, msg_id)
    return None


def preview_next_incident(messages: list[dict], state: dict) -> dict | None:
    """Dry-run planner that cannot mutate persistent or caller-owned state."""
    preview_state = copy.deepcopy(state)
    reconcile_delivered_terminals(preview_state, messages)
    return select_next_incident(messages, preview_state)


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
- M4 Max repair account: ssh m4max (fallback: ssh toby@192.168.1.222;
  user 'toby', home /Users/toby, NOT 'tobyglennpeters'). If an error cites a
  generic /tmp log, first identify the owning machine from its active crontab
  and read the log on that machine rather than assuming it is local.
- CROSSFIRE/IRONVANE OAuth is the explicit exception to the normal Toby/Profile
  2 browser identity. Read video-workspace/crossfire-series/docs/youtube_oauth_upload_contract.md.
  It uses the installed Chrome profile named Lilly (`lillyaxolotlgamer@gmail.com`,
  currently Profile 1), the IronVaneStory brand channel, and exact channel id
  UCMx7-QZTE_RkcDxpBMZplPA. Never use Profile 2, Chrome for Testing, or an
  AgentStack credential for this series.
- The transcript stage already has its own internal gpt-5.6-sol rescue loop; if a transcript failure reached this channel anyway, read the run-log tail first — the cause is usually upstream (providers, prompt assembly, QC contradiction), not one more retry.
- The morning pipeline (scripts/agentstack_morning.sh) is resume-safe: rerunning it resumes from completed stages. Rerun it via: /bin/bash scripts/show_notes_research_guard.sh

Do this, in order:
1. Read the relevant log tails and find the root cause. Do not guess from the Discord message alone.
2. Apply the smallest safe fix (script/config repair, cleanup of a bad artifact, restart of a wedged process).
3. Re-run the failed stage or its resume-safe wrapper to verify the fix actually clears the failure.
4. Return one machine-readable terminal result to this watcher. Do not post to
   Discord yourself; the watcher owns the same-channel outcome and guarantees
   it cannot disappear into the normal Build Log.

Your final response must be exactly one line beginning REPAIR_RESULT_JSON:
REPAIR_RESULT_JSON: {{"status":"fixed|blocked|failed","root_cause":"plain-language cause","change":"what changed","verification":"real source-of-truth check","terminal_verified":true|false,"terminal_evidence":"FINAL OUTCOME: the final expected artifact/job result, or none","human_action":"none, or the exact human action required"}}

Use status=fixed only after the real failed outcome is recovered and verified.
For status=fixed, terminal_verified must be true, terminal_evidence must name
the final expected source-of-truth outcome and begin exactly "FINAL OUTCOME:",
and human_action must be exactly "none". Merely saying a pipeline resumed,
started, advanced downstream, is
running, or reached the next stage is NOT terminal verification and will be
rejected by the watcher. For blocked/failed, terminal_verified must be false,
terminal_evidence must be "none", and human_action must be a specific non-none
step that Toby must take.
Use status=blocked when credentials, interactive authentication, approval, or
physical access are required. Use status=failed when your autonomous repair
attempt did not recover the outcome. Keep every field concise; include no local
paths, shell commands, raw logs, secrets, or tool-display labels.

HARD LIMITS — violating these is worse than leaving the error unfixed:
- NEVER release, publish, or approve an episode, and never treat this repair task as approval. Audio approval comes ONLY from Toby after listening. Do not run release_episode.py, launch_approved_release.py, or any full-episode YouTube upload. Rebuilding REVIEW artifacts (show notes, transcript, review audio) is allowed and encouraged.
- Never upload shorts manually or in a loop — shorts ship only via their crontab scheduler.
- Never force push. Never delete episodic/semantic memory. Never edit .agent/protocols/permissions.md.
- Never send ad-hoc status or repair-outcome posts to Discord or Telegram; the watcher owns the #build-log-errors outcome.
- For a morning-podcast recovery, canonical review delivery is part of the required terminal artifact: run the resume-safe wrapper or build_episode.py normally so it posts the hash-locked review through ARIA Telegram and the episode Discord channel. Never use --dry-run, --skip-telegram, --skip-discord, or monkeypatch/suppress notification functions for that recovery. These canonical review posts are allowed; they do not release or approve the episode.
- For a CROSSFIRE/IRONVANE invalid_grant, run the foreground helper from the
  crossfire-series root: `.venv/bin/python3 auth/auth_crossfire_loopback.py`.
  It opens Lilly Chrome, waits up to 15 minutes for the human Google consent
  step, rejects the wrong channel before saving, and leaves the old token
  untouched on mismatch. If consent completes during the turn, verify token
  health, exact IronVaneStory channel identity, and the original
  `shorts_upload.py --watchdog-all` stage before returning fixed. Do not pass
  `--source-error` inside the watcher turn because the watcher owns its one
  terminal Discord post.
- If the fix genuinely requires Toby (expired credentials/OAuth, a listening approval, physical hardware), return status=blocked with the exact human_action, then stop."""


def failed_outcome(
    root_cause: str,
    change: str,
    verification: str,
    human_action: str,
) -> dict[str, object]:
    return {
        "status": "failed",
        "root_cause": root_cause,
        "change": change,
        "verification": verification,
        "terminal_verified": False,
        "terminal_evidence": "none",
        "human_action": human_action,
    }


def rejected_result(reason: str) -> dict[str, object]:
    return failed_outcome(
        "The automated repair turn ended without an acceptable terminal result.",
        "The watcher rejected the repair claim instead of reporting a false success.",
        reason,
        "Review the source incident and its referenced job log, then rerun the automated repair with terminal source-of-truth evidence.",
    )


# Long-running children of the morning show-notes pipeline. A single
# build_show_notes.py pass can legitimately take 55-70 minutes (14 stories,
# each needing multiple LLM validation rounds), which is longer than
# REPAIR_TIMEOUT. If the repair-diagnosis turn times out while one of these
# is still alive, the underlying job hasn't actually failed a second time —
# only the diagnosis agent ran out of time watching it.
PIPELINE_PROCESS_PATTERNS = (
    "agentstack_morning.sh",
    "build_show_notes.py",
    "show_notes_research_guard.sh",
)


def pipeline_processes_alive() -> bool:
    for pattern in PIPELINE_PROCESS_PATTERNS:
        try:
            result = subprocess.run(
                ["pgrep", "-f", pattern],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode == 0 and result.stdout.strip():
            return True
    return False


def recovering_outcome(root_cause: str, verification: str) -> dict[str, object]:
    return {
        "status": "recovering",
        "root_cause": root_cause,
        "change": "No repair change was made; the source pipeline is still running on its own.",
        "verification": verification,
        "terminal_verified": False,
        "terminal_evidence": "none",
        "human_action": "None yet — only revisit if the job is still running well past its normal ~70min window.",
    }


def parse_repair_result(
    reply: str,
    returncode: int,
    agent_status: str | None = "ok",
) -> dict[str, object]:
    """Parse the agent's strict one-line result contract.

    An agent process exiting zero only proves the turn ended; it does not prove
    that the underlying job recovered.  Missing/invalid result data therefore
    fails closed and becomes a triple-red human escalation.
    """
    normalized_agent_status = str(agent_status or "").strip().casefold()
    if returncode != 0 or normalized_agent_status not in OK_AGENT_STATUSES:
        return failed_outcome(
            "The automated repair turn did not complete successfully.",
            "No verified repair was recorded.",
            f"Repair process exit={returncode}; agent status={agent_status or 'missing'}.",
            "Review the source incident and its referenced job log, then restart the repair after correcting the agent failure.",
        )
    result_line = next(
        (
            line.lstrip()
            for line in reversed(reply.splitlines())
            if line.lstrip().startswith(RESULT_PREFIX)
        ),
        "",
    )
    try:
        parsed = json.loads(result_line[len(RESULT_PREFIX):].strip())
    except (json.JSONDecodeError, TypeError):
        return rejected_result("No valid repair-result JSON object was returned.")
    if not isinstance(parsed, dict):
        return rejected_result("The repair-result JSON value was not an object.")
    status = str(parsed.get("status", "")).lower()
    required = (
        "root_cause",
        "change",
        "verification",
        "terminal_evidence",
        "human_action",
    )
    if status not in {"fixed", "blocked", "failed"} or any(
        not str(parsed.get(key, "")).strip() for key in required
    ):
        return rejected_result("The repair-result contract was incomplete or had an invalid status.")
    if not isinstance(parsed.get("terminal_verified"), bool):
        return rejected_result("terminal_verified was missing or was not a JSON boolean.")
    normalized: dict[str, object] = {
        key: str(parsed[key]).strip() for key in required
    }
    normalized["status"] = status
    normalized["terminal_verified"] = parsed["terminal_verified"]
    human_action = str(normalized["human_action"]).casefold()
    terminal_evidence = str(normalized["terminal_evidence"])
    verification_text = f"{normalized['verification']} {terminal_evidence}"
    if status == "fixed":
        if human_action not in NONE_ACTION_VALUES:
            return rejected_result("A fixed result requested human action.")
        if normalized["terminal_verified"] is not True:
            return rejected_result("A fixed result did not assert terminal verification.")
        if terminal_evidence.casefold() in NONE_ACTION_VALUES or len(terminal_evidence) < 16:
            return rejected_result("A fixed result did not include concrete terminal evidence.")
        if not terminal_evidence.casefold().startswith("final outcome:"):
            return rejected_result("Terminal evidence did not identify the final outcome.")
        if NON_TERMINAL_VERIFICATION_RE.search(verification_text):
            return rejected_result(
                "The claimed verification described a transitional or next-stage state, not a terminal outcome."
            )
    else:
        if normalized["terminal_verified"] is not False:
            return rejected_result("An unresolved result incorrectly claimed terminal verification.")
        if terminal_evidence.casefold() not in NONE_ACTION_VALUES:
            return rejected_result("An unresolved result claimed terminal completion evidence.")
        if human_action in NONE_ACTION_VALUES:
            return rejected_result("An unresolved result did not provide a human action.")
    for key in required:
        normalized[key] = str(normalized[key])[:MAX_RESULT_FIELD_CHARS]
    return normalized


def _json_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_known_terminal_outcome(
    message: dict,
    outcome: dict[str, object],
    *,
    podcast_dir: Path = PODCAST_DIR,
    qc_runner=None,
) -> dict[str, object]:
    """Replace self-asserted podcast success with artifact-level evidence.

    The generic structured contract applies to every project.  Morning podcast
    failures have an additional deterministic contract because a previous
    repair incorrectly called "transcript generation resumed" a success.  A
    completed morning run must leave QC-passing source files plus the same audio
    hash in the local review state, ARIA Telegram send record, and MP3.
    """
    if outcome.get("status") != "fixed":
        return outcome
    match = PODCAST_MORNING_FAILURE_RE.search(str(message.get("content", "")))
    if not match:
        return outcome

    episode = int(match.group(1))
    ep = f"{episode:03d}"
    scripts_dir = podcast_dir / "scripts"
    show_notes = podcast_dir / f"show_notes_episode_{ep}.md"
    transcript = podcast_dir / "episodes" / f"episode_{ep}_transcript.md"
    audio = podcast_dir / "audio" / f"episode_{ep}.mp3"
    cover = podcast_dir / "images" / f"episode_{ep}_cover.png"
    release_state = scripts_dir / f"release_ep{ep}_state.json"
    telegram_record = scripts_dir / ".telegram_send_records" / f"ep{ep}.json"
    problems: list[str] = []

    required_artifacts = (
        (show_notes, 100, "show notes"),
        (transcript, 100, "transcript"),
        (audio, 10_000, "review MP3"),
        (cover, 1_000, "cover art"),
    )
    for path, minimum_bytes, label in required_artifacts:
        try:
            if path.stat().st_size < minimum_bytes:
                problems.append(f"{label} is missing or too small")
        except OSError:
            problems.append(f"{label} is missing or too small")

    if qc_runner is None:
        def qc_runner(command: list[str]) -> bool:
            try:
                result = subprocess.run(
                    command,
                    cwd=str(podcast_dir),
                    capture_output=True,
                    text=True,
                    timeout=120,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired):
                return False
            return result.returncode == 0

    if show_notes.exists() and not qc_runner(
        [sys.executable, str(scripts_dir / "check_show_notes.py"), str(show_notes)]
    ):
        problems.append("show-notes QC does not pass")
    if transcript.exists() and not qc_runner(
        [sys.executable, str(scripts_dir / "check_episode.py"), str(transcript)]
    ):
        problems.append("transcript QC does not pass")

    state = _json_object(release_state)
    review = state.get("review_audio") if isinstance(state.get("review_audio"), dict) else {}
    telegram = _json_object(telegram_record)
    ready = telegram.get("ready") if isinstance(telegram.get("ready"), dict) else {}
    audio_hash = ""
    if audio.exists():
        try:
            audio_hash = _sha256(audio)
        except OSError:
            problems.append("review MP3 hash could not be read")
    if not audio_hash or review.get("sha256") != audio_hash:
        problems.append("release review state does not match the current MP3 hash")
    if not review.get("discord_message_id"):
        problems.append("Discord review-post evidence is missing")
    if not review.get("audio_url") or not review.get("cover_url"):
        problems.append("verified review URLs are missing from release state")
    if ready.get("review_audio_sha256") != audio_hash:
        problems.append("ARIA Telegram send record does not match the current MP3 hash")
    if ready.get("account_id") != "default":
        problems.append("ARIA Telegram send record is not routed through the default account")
    if not ready.get("message_id") or not ready.get("audio_message_id") or not ready.get("chat_id"):
        problems.append("ARIA Telegram ready-message evidence is incomplete")

    if problems:
        return rejected_result(
            f"EP{ep} failed deterministic terminal verification: "
            + "; ".join(dict.fromkeys(problems))
        )

    verified = dict(outcome)
    verified["verification"] = (
        f"EP{ep} show notes and transcript pass QC; review MP3 and cover exist; "
        "the MP3 hash matches both Discord review state and the ARIA Telegram send record."
    )
    verified["terminal_evidence"] = (
        f"FINAL OUTCOME: EP{ep} listenable review audio is hash-locked and posted "
        "through ARIA Telegram and Discord; publishing still waits for Toby's approval."
    )
    return verified


def format_terminal_outcome(msg_id: str, outcome: dict[str, object]) -> str:
    if outcome["status"] == "fixed":
        return (
            f"👍 CODEX AUTO-REPAIR SUCCEEDED — source error {msg_id}\n"
            f"Cause: {outcome['root_cause']}\n"
            f"Fix: {outcome['change']}\n"
            f"Verified: {outcome['verification']}\n"
            f"Terminal evidence: {outcome['terminal_evidence']}"
        )
    if outcome["status"] == "recovering":
        return (
            f"⏳ CODEX AUTO-REPAIR INCONCLUSIVE (pipeline still running, no action needed) — source error {msg_id}\n"
            f"Cause: {outcome['root_cause']}\n"
            f"Status: {outcome['verification']}\n"
            f"Next step: {outcome['human_action']}"
        )
    return (
        f"❌❌❌ CODEX AUTO-REPAIR FAILED — HUMAN INTERACTION REQUIRED — source error {msg_id}\n"
        f"Cause: {outcome['root_cause']}\n"
        f"Attempt: {outcome['change']}\n"
        f"Verification: {outcome['verification']}\n"
        f"Needed to fix: {outcome['human_action']}"
    )


def post_terminal_outcome(msg_id: str, outcome: dict[str, object]) -> bool:
    is_error = outcome["status"] not in {"fixed", "recovering"}
    return post_build_log(format_terminal_outcome(msg_id, outcome), error=is_error)


def dispatch_repair(message: dict, dry_run: bool) -> dict[str, object]:
    # Defense in depth: this is the ONLY function in the watcher that spends
    # model tokens. Re-verify the deterministic gate here so no future caller
    # can reach the LLM with a non-error message.
    actionable, why = is_actionable(message.get("content", ""))
    if not actionable:
        log(f"REFUSED dispatch for {message.get('id', '?')}: {why} "
            f"(deterministic gate; no model call made)")
        return {"status": "refused", "reason": why}
    msg_id = message["id"]
    excerpt = " ".join(message.get("content", "").split())[:180]
    if dry_run:
        log(f"DRY-RUN would dispatch Sol repair for message {msg_id}: {excerpt}")
        return {"status": "dry-run", "reason": excerpt}
    log(f"dispatching Sol repair for message {msg_id}: {excerpt}")
    if not post_build_log(
        f"🔧 CODEX AUTO-REPAIR ATTEMPT STARTED — source error {msg_id}: {excerpt}",
        error=True,
    ):
        log(f"WARN attempt-start post for {msg_id} was not delivered")
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
        if pipeline_processes_alive():
            log(f"source pipeline still running for {msg_id} — downgrading to recovering, not failed")
            return recovering_outcome(
                "The repair-diagnosis turn timed out, but the source pipeline "
                "(agentstack_morning.sh / build_show_notes.py / show_notes_research_guard.sh) "
                "is still actively running.",
                "A matching pipeline process was still alive when the diagnosis timeout fired, "
                "so this is not a confirmed second failure — the normal retry/build is likely "
                "just taking its usual long time.",
            )
        return failed_outcome(
            "The automated repair turn timed out.",
            "The watcher stopped waiting after its repair timeout.",
            "No recovered job outcome was verified.",
            "Review the source incident and its referenced job log, then retry the repair with a narrower recovery step.",
        )
    except OSError as exc:
        log(f"repair turn for {msg_id} could not start: {exc}")
        return failed_outcome(
            "The automated repair process could not be started.",
            "No repair change was completed.",
            f"The local agent launcher failed: {exc}",
            "Review the source incident and restore the local OpenClaw agent launcher before retrying repair.",
        )
    reply = ""
    agent_status: str | None = None
    try:
        data = json.loads(proc.stdout)
        if not isinstance(data, dict):
            raise TypeError("agent JSON root was not an object")
        result = data.get("result") or {}
        payloads = result.get("payloads") if isinstance(result, dict) else []
        if not isinstance(payloads, list):
            payloads = []
        reply = "\n".join(
            str(payload.get("text") or "")
            for payload in payloads
            if isinstance(payload, dict)
        ).strip()
        agent_status = str(data.get("status", ""))
        status = agent_status or "missing"
    except (json.JSONDecodeError, TypeError, AttributeError):
        status = "invalid-json"
        agent_status = "invalid-json"
        reply = (proc.stdout or proc.stderr or "").strip()
    reply_short = " ".join(reply.split())[:600] or "(no reply text)"
    log(f"repair turn for {msg_id} finished: status={status}; reply: {reply_short}")
    outcome = parse_repair_result(reply, proc.returncode, agent_status)
    return verify_known_terminal_outcome(message, outcome)


def queue_terminal(state: dict, msg_id: str, outcome: dict[str, object]) -> None:
    state.setdefault("pending_terminal", {})[msg_id] = {
        "outcome": outcome,
        "created_at": time.time(),
        "post_attempts": 0,
    }


def deliver_pending_terminal(
    state: dict,
    msg_id: str,
    *,
    poster=post_terminal_outcome,
    persist=save_state,
) -> bool:
    """Post one queued terminal result and close only after delivery succeeds."""
    entry = state.get("pending_terminal", {}).get(msg_id)
    if not isinstance(entry, dict) or not isinstance(entry.get("outcome"), dict):
        log(f"WARN pending terminal state for {msg_id} is invalid")
        return False
    outcome = entry["outcome"]
    required_outcome_keys = {
        "status",
        "root_cause",
        "change",
        "verification",
        "terminal_evidence",
        "human_action",
    }
    if not required_outcome_keys.issubset(outcome):
        outcome = failed_outcome(
            "The durable terminal-result record was incomplete.",
            "The watcher converted the malformed result into a fail-closed escalation.",
            "No trustworthy terminal repair result remained in state.",
            "Review the source incident and explicitly requeue it after repairing the watcher state record.",
        )
        entry["outcome"] = outcome
    try:
        post_attempts = int(entry.get("post_attempts", 0))
    except (TypeError, ValueError):
        post_attempts = 0
    entry["post_attempts"] = post_attempts + 1
    entry["last_post_attempt_at"] = time.time()
    persist(state)
    try:
        delivered = poster(msg_id, outcome)
    except Exception as exc:  # terminal state must survive any posting adapter failure
        log(f"WARN terminal poster for {msg_id} raised: {exc}")
        delivered = False
    if not delivered:
        log(f"terminal outcome for {msg_id} remains pending after post failure")
        persist(state)
        return False
    state.setdefault("outcomes", {})[msg_id] = outcome
    state.setdefault("pending_terminal", {}).pop(msg_id, None)
    mark_handled(state, msg_id)
    persist(state)
    log(f"terminal outcome for {msg_id} delivered; incident closed")
    return True


def drain_pending_terminals(state: dict) -> bool:
    """Retry durable terminal posts before any new repair is dispatched."""
    pending_ids = list(state.get("pending_terminal", {}).keys())
    all_delivered = True
    for msg_id in pending_ids:
        if not deliver_pending_terminal(state, msg_id):
            all_delivered = False
    return all_delivered


def record_repair_attempt(state: dict, message: dict) -> None:
    """Durably record ownership of an incident before starting the agent."""
    msg_id = str(message["id"])
    attempt_map = state.setdefault("message_attempts", {})
    attempts = attempt_map.get(msg_id)
    if not isinstance(attempts, list):
        attempts = []
        attempt_map[msg_id] = attempts
    attempts.append(time.time())
    state.setdefault("in_progress", {})[msg_id] = {
        "message": message,
        "started_at": time.time(),
        "attempt_number": len(attempts),
    }
    advance_cursor(state, msg_id)


def exhausted_attempt_outcome(msg_id: str) -> dict[str, object]:
    return failed_outcome(
        "The same source incident exhausted its automated repair attempts before a terminal outcome was recorded.",
        f"The watcher made {MAX_ATTEMPTS_PER_MESSAGE} repair attempts for source error {msg_id}.",
        "No recovered terminal job outcome was verified.",
        "Review the source incident and its referenced job log, correct the remaining blocker, then explicitly requeue this source message for repair.",
    )


def execute_incident(state: dict, message: dict) -> bool:
    """Attempt one incident and durably carry its terminal post to delivery."""
    msg_id = str(message["id"])
    if attempt_count(state, msg_id) >= MAX_ATTEMPTS_PER_MESSAGE:
        state.setdefault("in_progress", {}).pop(msg_id, None)
        queue_terminal(state, msg_id, exhausted_attempt_outcome(msg_id))
        save_state(state)
        return deliver_pending_terminal(state, msg_id)

    record_repair_attempt(state, message)
    save_state(state)
    outcome = dispatch_repair(message, dry_run=False)
    if outcome.get("status") in {"refused", "dry-run"}:
        outcome = failed_outcome(
            "The watcher refused an incident after it had already passed queue classification.",
            "No autonomous repair was completed.",
            "The deterministic dispatch gate and queue classifier disagreed.",
            "Review the source incident and repair the watcher classification mismatch before requeueing it.",
        )
    state.setdefault("in_progress", {}).pop(msg_id, None)
    queue_terminal(state, msg_id, outcome)
    save_state(state)
    return deliver_pending_terminal(state, msg_id)


def recover_in_progress(state: dict) -> bool:
    """Resume one interrupted incident without denying later messages a first try."""
    records = state.get("in_progress", {})
    if not records:
        return True
    msg_id = next(iter(records))
    record = records.get(msg_id)
    message = record.get("message") if isinstance(record, dict) else None
    if not isinstance(message, dict) or str(message.get("id", "")) != msg_id:
        state.setdefault("in_progress", {}).pop(msg_id, None)
        queue_terminal(
            state,
            msg_id,
            failed_outcome(
                "The durable in-progress repair record was incomplete.",
                "The watcher preserved the incident instead of guessing its source message.",
                "No safe repair retry could be constructed from state.",
                "Review the source incident in the error channel and explicitly requeue it after repairing the watcher state record.",
            ),
        )
        save_state(state)
        return deliver_pending_terminal(state, msg_id)
    log(f"recovering interrupted repair for source error {msg_id}")
    return execute_incident(state, message)


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
    state = load_state()

    if not dry_run:
        if state.get("pending_terminal") and not drain_pending_terminals(state):
            log("pending terminal delivery remains unresolved; no new repair dispatched")
            return 1
        if state.get("in_progress"):
            return 0 if recover_in_progress(state) else 1

    token = load_token()
    if not token:
        log("FATAL no Discord bot token available")
        return 1

    try:
        messages = discord_get_messages(token, state.get("last_seen_id"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        log(f"WARN Discord fetch failed: {exc}")
        return 1

    if not messages:
        log("no new messages")
        return 0

    if dry_run:
        before = copy.deepcopy(state)
        if bootstrap:
            log(f"DRY-RUN bootstrap would mark {len(messages)} message(s) seen")
            return 0
        candidate = preview_next_incident(messages, state)
        if candidate:
            dispatch_repair(candidate, dry_run=True)
        else:
            log("DRY-RUN found no actionable incident")
        if state != before:
            log("FATAL dry-run mutated caller state")
            return 1
        return 0

    newest_id = str(messages[-1]["id"])
    if bootstrap:
        state["last_seen_id"] = newest_id
        save_state(state)
        log(f"explicit bootstrap: marked {len(messages)} existing message(s) "
            f"as seen up to {newest_id}; no repairs dispatched")
        return 0

    if state.get("last_seen_id") is None:
        reconcile_delivered_terminals(state, messages)
    candidate = select_next_incident(messages, state)
    save_state(state)
    if not candidate:
        log("poll complete: no actionable incidents")
        return 0
    msg_id = str(candidate["id"])
    log(f"selected source error {msg_id}; later messages remain behind the cursor")
    return 0 if execute_incident(state, candidate) else 1


def selftest() -> int:
    """Offline regression suite: no network, Discord posts, state writes, or agents."""
    cases = [
        # (content, should_dispatch, label)
        ("✅ Sent via Discord. EP084 build complete", False, "success line"),
        ("🏗 EP084 build started\n✅ Show notes QC passed", False, "progress line"),
        ("📺 **EP084 YouTube status** (5/5 channels done)", False, "status line"),
        ("⚠️ **EP084 YouTube upload issues**\nWarnings only", True, "warning post in error channel"),
        ("⚠️ Podcast rollup DEGRADED: social web capture failed", True, "degraded rollup"),
        ("IRONVANE Shorts cadence stalled", True, "unmarked stalled job"),
        ("[RETRY] AgentStack Daily morning run exited 1 — auto-retrying (2/2)", False, "retry post"),
        ("[retry] lower-case retry is active", False, "case-normalized retry"),
        ("❌ [RETRY] red retry is active", False, "red retry prefix"),
        ("[HOLD] AgentStack Daily research stopped with exit 2.", False, "hold post"),
        ("❌❌❌ [hold] approval workflow", False, "red hold prefix"),
        ("🛑 EP084 morning HOLD: existing review audio is unapproved", False, "unapproved-audio hold"),
        ("🛑 database unavailable", True, "non-approval stop is actionable"),
        ("🔧 Sol repair BLOCKED: YouTube OAuth expired — Toby must re-auth", False, "own blocked post"),
        ("❌❌❌ codex auto-repair failed — source error 123", False, "own terminal post"),
        ("👍 EP087 MANUAL RECOVERY SUCCEEDED — source error 123\nVerified: final review audio", False, "manual recovery terminal post"),
        ("[BUILD LOG ROUTING CHECK] no action required", False, "routing test"),
        ("[sol-watcher-test] synthetic failure", False, "watcher test"),
        ("❌ [SOL-WATCHER-TEST] synthetic failure", False, "red watcher test"),
        ("❌ parser failed because upstream said no action required", True, "embedded no-action text"),
        ("❌ parser failed while reading [HOLD] as data", True, "embedded hold text"),
        ("❌ worker mentioned AUTO-REPAIR then crashed", True, "embedded watcher text"),
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
    checks_run = len(cases)

    def check(ok: bool, label: str) -> None:
        nonlocal failures, checks_run
        checks_run += 1
        print(f"  {'PASS' if ok else 'FAIL'}: {label}")
        failures += 0 if ok else 1

    # The dispatch function itself must refuse a no-action test without a model.
    refused = dispatch_repair(
        {"id": "selftest", "content": "[BUILD LOG ROUTING CHECK] no action required"},
        dry_run=True,
    )
    check(refused.get("status") == "refused", "dispatch gate refuses no-action test")

    def result_line(**overrides: object) -> str:
        payload: dict[str, object] = {
            "status": "fixed",
            "root_cause": "missing credential propagation",
            "change": "restored the credential to the owning job",
            "verification": "The final source-of-truth dashboard contains fresh non-zero metrics.",
            "terminal_verified": True,
            "terminal_evidence": "FINAL OUTCOME: the dashboard has fresh non-zero metrics and today's timestamp.",
            "human_action": "none",
        }
        payload.update(overrides)
        return f"ignored preface\n{RESULT_PREFIX} {json.dumps(payload)}"

    fixed = parse_repair_result(result_line(status="FIXED"), 0, "ok")
    blocked = parse_repair_result(
        result_line(
            status="blocked",
            verification="Interactive authentication is still denied.",
            terminal_verified=False,
            terminal_evidence="none",
            human_action="Sign in interactively to refresh the expired account.",
        ),
        0,
        "ok",
    )
    failed = parse_repair_result(
        result_line(
            status="failed",
            verification="The final job still exits non-zero.",
            terminal_verified=False,
            terminal_evidence="none",
            human_action="Review the provider outage and retry after service is restored.",
        ),
        0,
        "ok",
    )
    resumed = parse_repair_result(
        result_line(
            verification="The pipeline resumed transcript generation.",
            terminal_evidence="FINAL OUTCOME: the downstream transcript stage is now running.",
        ),
        0,
        "ok",
    )
    fixed_needs_human = parse_repair_result(
        result_line(human_action="Sign in again."), 0, "ok"
    )
    fixed_without_final_evidence = parse_repair_result(
        result_line(terminal_evidence="The dashboard has fresh non-zero metrics."),
        0,
        "ok",
    )
    unresolved_no_action = parse_repair_result(
        result_line(
            status="failed",
            terminal_verified=False,
            terminal_evidence="none",
            human_action="none",
        ),
        0,
        "ok",
    )
    wrong_agent_status = parse_repair_result(result_line(), 0, "error")
    unstructured = parse_repair_result("looks fixed", 0, "ok")
    check(fixed["status"] == "fixed", "terminally verified fixed result parses")
    fixed_text = format_terminal_outcome("1", fixed)
    check(
        fixed_text.startswith("👍 CODEX AUTO-REPAIR SUCCEEDED"),
        "fixed terminal outcome starts with a thumbs up",
    )
    check(not is_actionable(fixed_text)[0], "fixed terminal outcome cannot self-trigger")
    check(blocked["status"] == "blocked", "blocked result with human action parses")
    check(failed["status"] == "failed", "failed result with human action parses")
    blocked_text = format_terminal_outcome("2", blocked)
    check(
        blocked_text.startswith("❌❌❌ CODEX AUTO-REPAIR FAILED"),
        "blocked terminal outcome starts with three red Xs",
    )
    check(not is_actionable(blocked_text)[0], "blocked terminal outcome cannot self-trigger")
    check(
        resumed["status"] == "failed"
        and "transitional" in str(resumed["verification"]),
        "next-stage/resumed claim is rejected as false success",
    )
    check(
        fixed_needs_human["status"] == "failed",
        "fixed result cannot request human action",
    )
    check(
        fixed_without_final_evidence["status"] == "failed",
        "fixed result requires explicit final-outcome evidence",
    )
    check(
        unresolved_no_action["status"] == "failed"
        and str(unresolved_no_action["human_action"]).casefold() != "none",
        "unresolved result must supply a concrete human action",
    )
    check(wrong_agent_status["status"] == "failed", "non-ok agent status fails closed")
    check(unstructured["status"] == "failed", "unstructured agent reply fails closed")
    for non_object in ("[]", "null", '"fixed"', "42"):
        parsed = parse_repair_result(f"{RESULT_PREFIX} {non_object}", 0, "ok")
        check(parsed["status"] == "failed", f"non-object JSON {non_object} fails closed")

    missing_episode = verify_known_terminal_outcome(
        {"id": "998", "content": "❌ EP999 morning pipeline FAILED at stage: transcript"},
        fixed,
    )
    check(
        missing_episode["status"] == "failed"
        and "deterministic terminal verification" in str(missing_episode["verification"]),
        "podcast morning success is rejected when final review artifacts are absent",
    )
    generic_fixed = verify_known_terminal_outcome(
        {"id": "997", "content": "❌ unrelated cron failed"},
        fixed,
    )
    check(
        generic_fixed["status"] == "fixed",
        "non-podcast incidents retain the generic terminal-evidence contract",
    )

    # Cursor regression: the second actionable message must remain after A.
    queue_state = new_state()
    queue_state["last_seen_id"] = "100"
    incident_a = {"id": "101", "content": "❌ project A failed"}
    incident_b = {"id": "102", "content": "❌ project B failed"}
    first = select_next_incident([incident_a, incident_b], queue_state)
    check(first == incident_a, "oldest actionable incident is selected")
    check(queue_state["last_seen_id"] == "100", "cursor does not advance past selected incident")
    record_repair_attempt(queue_state, incident_a)
    check(
        queue_state["last_seen_id"] == "101"
        and "101" in queue_state["in_progress"]
        and "101" not in queue_state["handled"],
        "selected incident is durably in-progress before being handled",
    )
    queue_state["in_progress"].pop("101")
    mark_handled(queue_state, "101")
    second = select_next_incident([incident_b], queue_state)
    check(second == incident_b, "second actionable incident remains available next poll")

    # Per-message budget: prior messages cannot consume a new incident's first try.
    budget_state = new_state()
    budget_state["message_attempts"]["101"] = [1.0, 2.0]
    check(attempt_count(budget_state, "101") == 2, "same-message retry budget is counted")
    check(attempt_count(budget_state, "102") == 0, "new message retains its first attempt")

    # Durable terminal retry: failed delivery leaves the source open.
    terminal_state = new_state()
    queue_terminal(terminal_state, "201", fixed)
    no_persist = lambda _state: None
    delivered = deliver_pending_terminal(
        terminal_state,
        "201",
        poster=lambda _msg_id, _outcome: False,
        persist=no_persist,
    )
    check(
        not delivered
        and "201" in terminal_state["pending_terminal"]
        and "201" not in terminal_state["handled"],
        "failed terminal post remains pending and unhandled",
    )
    delivered = deliver_pending_terminal(
        terminal_state,
        "201",
        poster=lambda _msg_id, _outcome: True,
        persist=no_persist,
    )
    check(
        delivered
        and "201" not in terminal_state["pending_terminal"]
        and "201" in terminal_state["handled"],
        "terminal retry closes only after successful delivery",
    )
    malformed_terminal_state = new_state()
    malformed_terminal_state["pending_terminal"]["202"] = {
        "outcome": {"status": "fixed"},
        "post_attempts": "invalid",
    }
    delivered = deliver_pending_terminal(
        malformed_terminal_state,
        "202",
        poster=lambda _msg_id, outcome: outcome.get("status") == "failed",
        persist=no_persist,
    )
    check(
        delivered and "202" in malformed_terminal_state["handled"],
        "malformed pending result becomes a delivered fail-closed terminal",
    )

    # Dry-run planning and state-loss recovery must not consume incidents.
    dry_state = new_state()
    dry_messages = [
        {"id": "301", "content": "✅ normal success"},
        {"id": "302", "content": "❌ unattended failure"},
    ]
    dry_before = copy.deepcopy(dry_state)
    dry_candidate = preview_next_incident(dry_messages, dry_state)
    check(dry_candidate == dry_messages[1], "dry-run still identifies the incident")
    check(dry_state == dry_before, "dry-run planning does not mutate state")

    recovered = normalize_state(None)
    recovered_candidate = select_next_incident(
        [{"id": "401", "content": "❌ outstanding after state loss"}],
        recovered,
    )
    check(recovered["last_seen_id"] is None, "invalid state does not invent a bootstrap cursor")
    check(recovered_candidate is not None, "state loss replays an outstanding incident")
    partially_corrupt = normalize_state(
        {
            "version": STATE_VERSION,
            "last_seen_id": "999",
            "message_attempts": {},
            "handled": "not-a-list",
            "in_progress": {},
            "pending_terminal": {},
            "outcomes": {},
        }
    )
    check(
        partially_corrupt["last_seen_id"] is None
        and partially_corrupt["handled"] == [],
        "partially corrupt state replays instead of preserving a stale cursor",
    )

    delivered_history = new_state()
    history = [
        {"id": "501", "content": "❌ old source failure"},
        {
            "id": "502",
            "content": "👍 CODEX AUTO-REPAIR SUCCEEDED — source error 501\nVerified: final outcome",
        },
    ]
    reconcile_delivered_terminals(delivered_history, history)
    check("501" in delivered_history["handled"], "channel terminal post reconstructs closure after state loss")
    manual_history = new_state()
    reconcile_delivered_terminals(
        manual_history,
        [
            {"id": "601", "content": "❌ old source failure"},
            {
                "id": "602",
                "content": "👍 EP087 MANUAL RECOVERY SUCCEEDED — source error 601\n"
                "Verified: final review audio",
            },
        ],
    )
    check(
        "601" in manual_history["handled"],
        "manual recovery terminal post reconstructs closure after state loss",
    )

    print(f"selftest: {checks_run - failures}/{checks_run} checks passed "
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
