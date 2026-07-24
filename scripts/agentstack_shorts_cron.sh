#!/bin/bash
# Cron wrapper for AgentStack Daily Shorts uploads.

set -u

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export YOUTUBE_STUDIO_RELAUNCH_CHROME="${YOUTUBE_STUDIO_RELAUNCH_CHROME:-1}"

PODCAST_DIR="/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast"
LOG="$PODCAST_DIR/content_staging/shorts/upload_cron.log"
LOCKFILE="/tmp/agentstack_shorts_upload.lock"
LOCK_MAX_AGE=7200
PYTHON="$PODCAST_DIR/.venv_shorts/bin/python3"
POST_BUILD_LOG="/Users/tobyglennpeters/.openclaw/workspace/scripts/utils/post_build_log.py"
OPENCLAW_BIN="${OPENCLAW_BIN:-/opt/homebrew/bin/openclaw}"
BUILD_LOG_ERROR_CHANNEL="${BUILD_LOG_ERROR_CHANNEL_ID:-1524923755019636948}"
CHROME_LOCK_HELPER="/Users/tobyglennpeters/.openclaw/workspace/scripts/utils/chrome_automation_lock.sh"
CHILD_MARKER=""

mkdir -p "$(dirname "$LOG")"

# AgentStack Daily / OpenClaw Daily shorts are disabled by standing policy.
# Keep this legacy entry point fail-closed in case an old scheduler or operator
# invokes it, but do not alert: no rendered shorts package is expected.
echo "[$(date)] AgentStack Shorts disabled by policy; no upload attempted" >> "$LOG"
exit 0

post_build_log() {
  local message="$1"
  if [ -f "$POST_BUILD_LOG" ] && \
      /usr/bin/python3 "$POST_BUILD_LOG" --error "$message" >> "$LOG" 2>&1; then
    return 0
  fi
  echo "[$(date)] WARN: shared Build Log helper failed; trying OpenClaw fallback" >> "$LOG"
  if "$OPENCLAW_BIN" message send --channel discord \
      --target "channel:$BUILD_LOG_ERROR_CHANNEL" --message "$message" >> "$LOG" 2>&1; then
    return 0
  fi
  echo "[$(date)] WARN: Discord Build Log post failed through helper and fallback" >> "$LOG"
  return 1
}

if [ -f "$LOCKFILE" ]; then
  lock_age=$(( $(date +%s) - $(stat -f %m "$LOCKFILE" 2>/dev/null || echo 0) ))
  if [ "$lock_age" -lt "$LOCK_MAX_AGE" ]; then
    echo "[$(date)] AgentStack Shorts uploader already running; skipping (lock age ${lock_age}s)" >> "$LOG"
    exit 0
  fi
  echo "[$(date)] Removing stale AgentStack Shorts lock (${lock_age}s old)" >> "$LOG"
  rm -f "$LOCKFILE"
fi

if ! touch "$LOCKFILE"; then
  msg="AgentStack Shorts uploader failed before launch: could not create lock $LOCKFILE"
  echo "[$(date)] $msg" >> "$LOG"
  post_build_log "❌ [AgentStack Shorts] $msg"
  exit 1
fi
cleanup() {
  if command -v chrome_automation_lock_release >/dev/null 2>&1; then
    chrome_automation_lock_release
  fi
  rm -f "$LOCKFILE"
  if [ -n "${CHILD_MARKER:-}" ]; then
    rm -f "$CHILD_MARKER"
  fi
}
trap cleanup EXIT

if [ ! -x "$PYTHON" ]; then
  msg="AgentStack Shorts uploader failed before launch: missing python at $PYTHON"
  echo "[$(date)] $msg" >> "$LOG"
  post_build_log "❌ [AgentStack Shorts] $msg"
  exit 1
fi

if ! cd "$PODCAST_DIR"; then
  msg="AgentStack Shorts uploader failed before launch: could not cd to $PODCAST_DIR"
  echo "[$(date)] $msg" >> "$LOG"
  post_build_log "❌ [AgentStack Shorts] $msg"
  exit 1
fi

if [ ! -r "$CHROME_LOCK_HELPER" ]; then
  msg="AgentStack Shorts uploader failed before launch: missing shared Chrome lock helper $CHROME_LOCK_HELPER"
  echo "[$(date)] $msg" >> "$LOG"
  post_build_log "❌ [AgentStack Shorts] $msg"
  exit 1
fi
. "$CHROME_LOCK_HELPER"

if ! CHILD_MARKER=$(mktemp /tmp/agentstack_shorts_child.XXXXXX); then
  msg="AgentStack Shorts uploader failed before launch: could not create child completion marker"
  echo "[$(date)] $msg" >> "$LOG"
  post_build_log "❌ [AgentStack Shorts] $msg"
  exit 1
fi

if ! chrome_automation_lock_acquire \
  "AgentStack Shorts" \
  "${AGENTSTACK_CHROME_LOCK_WAIT_SECONDS:-900}" >> "$LOG" 2>&1; then
  msg="AgentStack Shorts uploader failed before launch: shared Chrome automation lock timed out"
  echo "[$(date)] $msg" >> "$LOG"
  post_build_log "❌ [AgentStack Shorts] $msg"
  exit 1
fi

echo "[$(date)] AgentStack Shorts uploader cron started" >> "$LOG"
AGENTSTACK_SHORTS_SCRIPT="$PODCAST_DIR/scripts/upload_agentstack_shorts.py" \
AGENTSTACK_SHORTS_CHILD_MARKER="$CHILD_MARKER" \
"$PYTHON" -c '
import os
import json
import runpy
import sys
from pathlib import Path

script = os.environ["AGENTSTACK_SHORTS_SCRIPT"]
marker = Path(os.environ["AGENTSTACK_SHORTS_CHILD_MARKER"])
sys.path.insert(0, str(Path(script).parent))
sys.argv = [script, "--mode", "cron"]
namespace = runpy.run_path(script, run_name="agentstack_shorts_cron_child")
status = namespace["main"]()
exit_code = 0 if status is None else int(status)
marker.write_text(json.dumps({
    "exit_code": exit_code,
    "error_notification_delivered": bool(namespace.get("_ERROR_NOTIFICATION_DELIVERED", False)),
    "error_notification_attempts": int(namespace.get("_ERROR_NOTIFICATION_ATTEMPTS", 0)),
    "error_notification_failures": int(namespace.get("_ERROR_NOTIFICATION_FAILURES", 0)),
}), encoding="utf-8")
raise SystemExit(exit_code)
' >> "$LOG" 2>&1
status=$?

if [ "$status" -ne 0 ]; then
  msg="AgentStack Shorts uploader cron failed on $(hostname -s) with exit $status. Check $LOG"
  echo "[$(date)] $msg" >> "$LOG"
  notification_delivered="false"
  if [ -s "$CHILD_MARKER" ]; then
    notification_delivered=$("$PYTHON" -c 'import json,sys; print("true" if json.load(open(sys.argv[1])).get("error_notification_delivered") is True else "false")' "$CHILD_MARKER" 2>/dev/null || echo "false")
  fi
  if [ "$notification_delivered" = "true" ]; then
    echo "[$(date)] Child confirmed delivery of a concrete error alert; wrapper duplicate suppressed" >> "$LOG"
  else
    if ! post_build_log "❌ [AgentStack Shorts] $msg"; then
      echo "[$(date)] WARN: child reported no delivered error alert and wrapper alert also failed" >> "$LOG"
    fi
  fi
else
  echo "[$(date)] AgentStack Shorts uploader cron completed" >> "$LOG"
fi

exit "$status"
