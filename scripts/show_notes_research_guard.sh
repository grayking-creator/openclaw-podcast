#!/bin/bash
# Guarded launcher for the daily AgentStack morning pipeline.
#
# This wrapper exists so pre-execution failures, especially shell syntax errors
# in agentstack_morning.sh, still leave both a local and Discord Build Log note.

set -u

BUILD_LOG="${SHOW_NOTES_BUILD_LOG:-/tmp/show_notes_build.log}"
RUN_LOG="${SHOW_NOTES_RESEARCH_LOG:-/tmp/show_notes_research.log}"
SCRIPT="${SHOW_NOTES_RESEARCH_SCRIPT:-/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/scripts/agentstack_morning.sh}"
# Fixed 2026-07-08: previous default pointed at .openclaw/scripts/utils/ (no
# 'workspace'), which doesn't exist — every guard FAIL/HOLD Discord post was
# silently skipped with only a WARN in the local build log.
POST_BUILD_LOG="${SHOW_NOTES_POST_BUILD_LOG:-/Users/tobyglennpeters/.openclaw/workspace/scripts/utils/post_build_log.py}"
SCRIPTS_DIR="$(dirname "$SCRIPT")"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

append_build_log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" >> "$BUILD_LOG"
}

post_discord_build_log() {
  local message=$1
  if [ "${SHOW_NOTES_DISABLE_DISCORD:-0}" = "1" ]; then
    append_build_log "show_notes_research_guard: Discord Build Log post skipped by SHOW_NOTES_DISABLE_DISCORD"
    return 0
  fi
  if [ ! -f "$POST_BUILD_LOG" ]; then
    append_build_log "show_notes_research_guard: WARN missing Build Log helper: $POST_BUILD_LOG"
    return 1
  fi
  python3 "$POST_BUILD_LOG" "$message" >> "$BUILD_LOG" 2>&1 || {
    append_build_log "show_notes_research_guard: WARN Discord Build Log post failed"
    return 1
  }
}

fail_guard() {
  local summary=$1
  local code=${2:-1}
  local message
  append_build_log "show_notes_research_guard: FAIL $summary"
  message=$(printf '[FAIL] AgentStack Daily research guard: %s\nLog: %s\nBuild log: %s' "$summary" "$RUN_LOG" "$BUILD_LOG")
  post_discord_build_log "$message" || true
  exit "$code"
}

# Pre-flight: routing assertion (locked 2026-06-27, post-EP075 incident).
# Wipe __pycache__ to defeat any stale .pyc from a half-edited module, then
# run the assertion. The assertion sends a one-line ping to the operator's
# Telegram DM (chat id 8319992332) to prove the bot is wired to the right
# place; if anything is wrong it sends a 🚨 ROUTING MIS-WIRED alert and
# exits 2, which causes this guard to fail the morning build loudly.
if [ -d "${SCRIPTS_DIR}/__pycache__" ]; then
  rm -rf "${SCRIPTS_DIR}/__pycache__" 2>/dev/null || true
fi
if [ -f "${SCRIPTS_DIR}/assert_telegram_routing.py" ]; then
  if ! python3 "${SCRIPTS_DIR}/assert_telegram_routing.py" >> "$RUN_LOG" 2>&1; then
    append_build_log "show_notes_research_guard: ROUTING MIS-WIRED — Telegram pre-flight failed; ABORTING"
    fail_guard "Telegram routing pre-flight failed (see $RUN_LOG for the assertion output). The morning pipeline refuses to build until the bot is wired to the operator's DM (chat id 8319992332)." 2
  fi
  append_build_log "show_notes_research_guard: Telegram routing pre-flight PASS"
fi

append_build_log "show_notes_research_guard: starting"

if [ ! -f "$SCRIPT" ]; then
  fail_guard "research script missing: $SCRIPT" 127
fi

if ! /bin/bash -n "$SCRIPT" >> "$RUN_LOG" 2>&1; then
  fail_guard "syntax check failed before launch: $SCRIPT" 2
fi

append_build_log "show_notes_research_guard: syntax OK"

if [ "${SHOW_NOTES_GUARD_DRY_RUN:-0}" = "1" ]; then
  append_build_log "show_notes_research_guard: dry run complete"
  exit 0
fi

# The morning script is resume-safe (QC-passed show notes, an existing
# transcript, and a pre-generated art module are all picked up, not redone),
# so a transient failure gets one automatic retry before waking a human.
# Exit 2 (HOLD) is deliberate and never retried. Added 2026-07-08: EP082 and
# EP083 both died on retryable transcript-stage failures and sat dead until
# manual reruns hours later.
MAX_RUNS="${SHOW_NOTES_GUARD_MAX_RUNS:-2}"
RETRY_DELAY_S="${SHOW_NOTES_GUARD_RETRY_DELAY_S:-180}"
attempt=1
while :; do
  /bin/bash "$SCRIPT"
  rc=$?

  if [ "$rc" -eq 0 ]; then
    break
  fi

  if [ "$rc" -eq 2 ]; then
    append_build_log "show_notes_research_guard: HOLD research script exited 2: $SCRIPT"
    hold_message=$(printf '[HOLD] AgentStack Daily research stopped with exit 2.\nLog: %s\nBuild log: %s' "$RUN_LOG" "$BUILD_LOG")
    post_discord_build_log "$hold_message" || true
    exit 2
  fi

  if [ "$attempt" -lt "$MAX_RUNS" ]; then
    attempt=$((attempt + 1))
    append_build_log "show_notes_research_guard: research script exited $rc — auto-retry ${attempt}/${MAX_RUNS} in ${RETRY_DELAY_S}s (resume-safe)"
    post_discord_build_log "[RETRY] AgentStack Daily morning run exited $rc — auto-retrying (${attempt}/${MAX_RUNS}) in ${RETRY_DELAY_S}s. Completed stages resume, not rebuild." || true
    sleep "$RETRY_DELAY_S"
    continue
  fi

  fail_guard "research script exited $rc after ${attempt} run(s): $SCRIPT" "$rc"
done

append_build_log "show_notes_research_guard: completed successfully"
