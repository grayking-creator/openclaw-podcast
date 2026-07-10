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
CHILD_MARKER=""

mkdir -p "$(dirname "$LOG")"

post_build_log() {
  local message="$1"
  if [ -f "$POST_BUILD_LOG" ]; then
    /usr/bin/python3 "$POST_BUILD_LOG" --error "$message" >> "$LOG" 2>&1 || \
      echo "[$(date)] WARN: Discord Build Log post failed" >> "$LOG"
  else
    echo "[$(date)] WARN: missing Build Log helper: $POST_BUILD_LOG" >> "$LOG"
  fi
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

if ! CHILD_MARKER=$(mktemp /tmp/agentstack_shorts_child.XXXXXX); then
  msg="AgentStack Shorts uploader failed before launch: could not create child completion marker"
  echo "[$(date)] $msg" >> "$LOG"
  post_build_log "❌ [AgentStack Shorts] $msg"
  exit 1
fi

echo "[$(date)] AgentStack Shorts uploader cron started" >> "$LOG"
AGENTSTACK_SHORTS_SCRIPT="$PODCAST_DIR/scripts/upload_agentstack_shorts.py" \
AGENTSTACK_SHORTS_CHILD_MARKER="$CHILD_MARKER" \
"$PYTHON" -c '
import os
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
marker.write_text(str(exit_code), encoding="utf-8")
raise SystemExit(exit_code)
' >> "$LOG" 2>&1
status=$?

if [ "$status" -ne 0 ]; then
  msg="AgentStack Shorts uploader cron failed on $(hostname -s) with exit $status. Check $LOG"
  echo "[$(date)] $msg" >> "$LOG"
  if [ -s "$CHILD_MARKER" ]; then
    echo "[$(date)] Child completed with handled exit $(cat "$CHILD_MARKER"); wrapper alert suppressed" >> "$LOG"
  else
    post_build_log "❌ [AgentStack Shorts] $msg"
  fi
else
  echo "[$(date)] AgentStack Shorts uploader cron completed" >> "$LOG"
fi

exit "$status"
