#!/bin/bash
# AgentStack Daily — full morning pipeline.
#
# Goal: by 8:00 AM ET a complete, listenable episode (show notes + transcript +
# EN audio + cover art) is on the CDN, the audio is playable in ARIA Telegram,
# and a hash-locked review record is in Discord. Publish still requires Toby's
# verified Discord ✅ — this script never releases anything.
#
# Stages:
#   1. sync episode counter against live YouTube channel
#   2. collision check (existing un-released draft → HOLD, exit 2)
#   3. gather_research_context.py     (deterministic data collection)
#   4. build_show_notes.py            (deterministic builder + inline section QC,
#                                      final check_show_notes.py gate + repair
#                                      loop inside — a QC drift costs a repair
#                                      round, never the morning run)
#   5. post_show_notes_draft_discord  (EARLY post: story slate + "transcript in
#                                      progress" so Toby can reject mid-stream
#                                      before the audio compute is spent)
#   6. generate_episode_transcript.py (model + check_episode.py QC loop)
#   7. build_episode.py               (slate verify, QC, nova render, EN audio,
#                                      bespoke cover art, CDN push, ARIA audio +
#                                      full Discord review record — stops at gate)
#
# Stage 5 gives Toby an early reject gate on the stories; stage 7 delivers the
# listenable review. If he disapproves, regen all three: scripts/regen_episode.sh <N>
#
# Launched by show_notes_research_guard.sh from cron. All failures append to
# BUILD_LOG and post to the Discord alerts channel (per graduated lesson:
# research cron failures must always leave both trails).

set -u

BUILD_LOG="${SHOW_NOTES_BUILD_LOG:-/tmp/show_notes_build.log}"
RUN_LOG="${SHOW_NOTES_RESEARCH_LOG:-/tmp/show_notes_research.log}"
SCRIPT_DIR=/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/scripts
PODCAST_DIR=/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast
DONE_FILE="${SCRIPT_DIR}/youtube_uploaded.txt"
POST_BUILD_LOG="${AGENTSTACK_POST_BUILD_LOG:-/Users/tobyglennpeters/.openclaw/workspace/scripts/utils/post_build_log.py}"
POST_BUILD_LOG_PYTHON="${AGENTSTACK_POST_BUILD_LOG_PYTHON:-/usr/bin/python3}"
OPENCLAW_BIN="${OPENCLAW_BIN:-/opt/homebrew/bin/openclaw}"
BUILD_LOG_CHANNEL="${BUILD_LOG_CHANNEL_ID:-1485243812442804327}"
BUILD_LOG_ERROR_CHANNEL="${BUILD_LOG_ERROR_CHANNEL_ID:-1524923755019636948}"

# cron runs with a minimal PATH; the pipeline needs homebrew tools
# (openclaw, ffmpeg, git helpers) on every stage.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

ts() { date '+%Y-%m-%d %H:%M:%S'; }
blog() { printf '[%s] %s\n' "$(ts)" "$*" >> "$BUILD_LOG"; }

alert() {
  if [ -f "$POST_BUILD_LOG" ] && \
      "$POST_BUILD_LOG_PYTHON" "$POST_BUILD_LOG" --info "$1" >> "$BUILD_LOG" 2>&1; then
    return 0
  fi
  blog "agentstack_morning: WARN shared Build Log info helper failed; trying OpenClaw fallback"
  if "$OPENCLAW_BIN" message send --channel discord --target "channel:$BUILD_LOG_CHANNEL" \
      --message "$1" >> "$BUILD_LOG" 2>&1; then
    return 0
  fi
  blog "agentstack_morning: WARN Discord info alert failed through helper and fallback"
  return 1
}

alert_error() {
  if [ -f "$POST_BUILD_LOG" ] && \
      "$POST_BUILD_LOG_PYTHON" "$POST_BUILD_LOG" --error "$1" >> "$BUILD_LOG" 2>&1; then
    return 0
  fi
  blog "agentstack_morning: WARN shared Build Log error helper failed; trying OpenClaw fallback"
  if "$OPENCLAW_BIN" message send --channel discord --target "channel:$BUILD_LOG_ERROR_CHANNEL" \
      --message "$1" >> "$BUILD_LOG" 2>&1; then
    return 0
  fi
  blog "agentstack_morning: WARN Discord error alert failed through helper and fallback"
  return 1
}

fail_stage() {
  local stage=$1 detail=$2
  blog "FAIL EP${NEXT_EP_PAD:-???} stage '${stage}': ${detail}"
  if [ "${AGENTSTACK_GUARD_MANAGED:-0}" = "1" ]; then
    # The guard owns retry/final notification. Posting an attempt-level error
    # here lets the repair watcher race and kill the guard's in-flight retry.
    blog "agentstack_morning: guard-managed attempt failure; final notification belongs to show_notes_research_guard"
  else
    alert_error "❌ EP${NEXT_EP_PAD:-???} morning pipeline FAILED at stage: ${stage}
${detail}
Run log: ${RUN_LOG}
Build log: ${BUILD_LOG}"
  fi
  exit 1
}

blog "agentstack_morning: starting"

# ── Stage 0.1: gather research context (deterministic data collection) ───────
#    We do this first so the fresh-research gate runs against newly gathered
#    context, preventing stale-on-disk artifacts from blocking the pipeline.
blog "agentstack_morning: gathering research context before gate check"
if ! python3 "${SCRIPT_DIR}/gather_research_context.py" >> "$RUN_LOG" 2>&1; then
  blog "agentstack_morning: WARN gather_research_context.py failed at startup"
  alert_error "⚠️ AgentStack Daily morning pipeline DEGRADED: gather_research_context.py failed at startup. The fresh-research gate will still run, but today's source refresh is not verified. Run log: ${RUN_LOG}"
fi

# ── Stage 0: fresh-research gate (locked 2026-06-27, EP075 incident class).
#    Hard fail. If research is stale, was used by a prior episode, or the
#    YouTube counter has not advanced since the prior approved release,
#    refuse to build. The gate posts its own Discord error and exits 2.
#    A new research context is gathered by the morning pipeline itself
#    (Stage 3) so the gate normally runs against yesterday's context —
#    that is intentional. The freshness check fires only if the cron has
#    been skipped for >24h; the no-duplicate check fires whenever the
#    morning's gather fails to actually re-fetch and the old context
#    persists.
if [ -f "${SCRIPT_DIR}/fresh_research_gate.py" ]; then
  _GATE_NEXT_EP=0
  if [ -f "$DONE_FILE" ]; then
    _GATE_LAST=$(tail -1 "$DONE_FILE" | tr -d '[:space:]')
    if [ -n "$_GATE_LAST" ] && [ "${_GATE_LAST:-0}" -gt 0 ] 2>/dev/null; then
      _GATE_NEXT_EP=$(( 10#$_GATE_LAST + 1 ))
    fi
  fi
  python3 "${SCRIPT_DIR}/fresh_research_gate.py" "$_GATE_NEXT_EP" >> "$BUILD_LOG" 2>&1
  rc=$?
  if [ "$rc" -ne 0 ]; then
    blog "agentstack_morning: EP$(printf '%03d' "$_GATE_NEXT_EP") fresh-research gate exit=$rc — HOLDING without rebuilding"
    exit 2
  fi
  blog "agentstack_morning: fresh-research gate PASS"
else
  blog "agentstack_morning: WARN fresh_research_gate.py missing — proceeding without the no-duplicate guard"
  alert_error "⚠️ AgentStack Daily morning pipeline DEGRADED: fresh_research_gate.py is missing, so the pipeline is proceeding without its freshness and duplicate-story guard. Build log: ${BUILD_LOG}"
fi

# ── Stage 1: sync against live YouTube channel ───────────────────────────────
if [ -f "${SCRIPT_DIR}/sync_uploaded_from_youtube.py" ]; then
  if ! python3 "${SCRIPT_DIR}/sync_uploaded_from_youtube.py" >> "$BUILD_LOG" 2>&1; then
    blog "agentstack_morning: WARN youtube sync failed; using local counter"
    alert_error "⚠️ AgentStack Daily morning pipeline DEGRADED: YouTube episode-state sync failed; the run is continuing with the local episode counter. Build log: ${BUILD_LOG}"
  fi
fi

_LAST_EP=$(tail -1 "$DONE_FILE" | tr -d '[:space:]')
_NEXT_EP=$(( 10#$_LAST_EP + 1 ))
NEXT_EP_PAD=$(printf "%03d" "$_NEXT_EP")
DRAFT_PATH="${PODCAST_DIR}/show_notes_episode_${NEXT_EP_PAD}.md"
TRANSCRIPT_PATH="${PODCAST_DIR}/episodes/episode_${NEXT_EP_PAD}_transcript.md"
RESUME_EXISTING_DRAFT=0

blog "agentstack_morning: targeting EP${NEXT_EP_PAD} (last released: EP${_LAST_EP})"

# ── Stage 2: collision check / resume.
#    A QC-passing draft should not strand a day of audio work. Resume from it.
#    A failed draft is archived and rebuilt with fresh context.
#    (Locked 2026-06-21, EP072 incident: morning pipeline was regenerating the
#    same episode after the approved release orchestrator died in
#    lane_translations, because the collision check only looked at show-notes
#    QC, not at the release-state file. The morning pipeline now also reads
#    scripts/release_ep${NEXT_EP_PAD}_state.json and refuses to regenerate an
#    episode whose approved release is still in flight — it instead attempts
#    to resume the orchestrator and only alerts Toby if resume fails.)
EP_NUM_PADDED="${NEXT_EP_PAD}"
STATE_FILE="${SCRIPT_DIR}/release_ep${EP_NUM_PADDED}_state.json"
if [ -f "$DRAFT_PATH" ]; then
  blog "agentstack_morning: EP${NEXT_EP_PAD} existing draft found — checking whether it can resume"
  if python3 "${SCRIPT_DIR}/check_show_notes.py" "$DRAFT_PATH" >> "$BUILD_LOG" 2>&1; then
    # Draft QC-passed. Now check if a release is in flight.
    if [ -f "$STATE_FILE" ]; then
      RUN_STATUS=$(python3 -c "import json; print(json.load(open('${STATE_FILE}')).get('approved_orchestrator',{}).get('run_status',''))" 2>/dev/null || echo "")
      COMPLETED_STEPS=$(python3 -c "import json; print(','.join(json.load(open('${STATE_FILE}')).get('approved_orchestrator',{}).get('completed_steps',[])))" 2>/dev/null || echo "")
      DISCORD_STEP_DONE=$(echo "$COMPLETED_STEPS" | grep -q "discord" && echo "yes" || echo "no")
      if [ -n "$RUN_STATUS" ] && [ "$RUN_STATUS" != "complete" ] && [ "$DISCORD_STEP_DONE" != "yes" ]; then
        # Release is in flight (started but not finished). Do NOT regenerate.
        # Resume the orchestrator instead — it will pick up at the next
        # incomplete step (release_episode_approved.py honours completed_steps
        # via mark_step_complete on disk).
        blog "agentstack_morning: EP${NEXT_EP_PAD} approved release in flight (run_status=${RUN_STATUS}); attempting to resume orchestrator"
        alert "🔁 EP${NEXT_EP_PAD} morning: approved release is in flight (run_status=${RUN_STATUS}, completed_steps=${COMPLETED_STEPS}). Resuming orchestrator — not regenerating today's episode."
        STORED_PUB_DATE=$(python3 -c "import json; print(json.load(open('${STATE_FILE}')).get('pub_date',''))" 2>/dev/null || echo "")
        if [ -n "$STORED_PUB_DATE" ] && python3 "${SCRIPT_DIR}/launch_approved_release.py" "$_NEXT_EP" \
            --pub-date "$STORED_PUB_DATE" \
            >> "$BUILD_LOG" 2>&1; then
          blog "agentstack_morning: EP${NEXT_EP_PAD} orchestrator resume launched successfully"
          exit 0
        fi
        blog "agentstack_morning: EP${NEXT_EP_PAD} orchestrator resume FAILED to launch; HOLDING"
        alert_error "❌ EP${NEXT_EP_PAD} morning: orchestrator resume FAILED to launch. Release stuck at run_status=${RUN_STATUS}, step $(echo "$COMPLETED_STEPS" | tr ',' ' '). Manual recovery: python3 scripts/recover_failed_translation_lane.py ${NEXT_EP_PAD} or python3 scripts/launch_approved_release.py ${NEXT_EP_PAD} --pub-date '<original>'. Not regenerating."
        exit 2
      fi
      REVIEW_AUDIO_SHA=$(python3 -c "import json; print((json.load(open('${STATE_FILE}')).get('review_audio') or {}).get('sha256',''))" 2>/dev/null || echo "")
      AUDIO_APPROVED=$(python3 -c "import json; print('yes' if (json.load(open('${STATE_FILE}')).get('audio_approval') or {}).get('approved') is True else 'no')" 2>/dev/null || echo "no")
      if [ -n "$REVIEW_AUDIO_SHA" ] && [ "$AUDIO_APPROVED" != "yes" ]; then
        blog "agentstack_morning: EP${NEXT_EP_PAD} has unapproved review audio — HOLDING instead of reposting stale review"
        alert_error "🛑 EP${NEXT_EP_PAD} morning HOLD: existing review audio is unapproved, so the pipeline will not reuse or repost the same show notes/audio. Run scripts/regen_episode.sh ${_NEXT_EP} with the rejection guidance to rebuild from fresh research."
        exit 2
      fi
    fi
    blog "agentstack_morning: EP${NEXT_EP_PAD} existing draft passes QC — resuming downstream"
    RESUME_EXISTING_DRAFT=1
  else
    ARCHIVE_PATH="${DRAFT_PATH}.rejected.existing.$(date +%s)"
    mv "$DRAFT_PATH" "$ARCHIVE_PATH"
    blog "agentstack_morning: EP${NEXT_EP_PAD} existing draft failed QC; archived to ${ARCHIVE_PATH}; rebuilding"
  fi
fi

# ── Stage 3: research gathering (deterministic) ──────────────────────────────
if [ "$RESUME_EXISTING_DRAFT" -eq 0 ]; then
  blog "agentstack_morning: EP${NEXT_EP_PAD} stage 3 — using research context gathered at startup"
  if [ ! -s /tmp/agent_research_context.json ]; then
    fail_stage "research-gather" "no /tmp/agent_research_context.json produced"
  fi
else
  blog "agentstack_morning: EP${NEXT_EP_PAD} stage 3 — skipped; resuming existing QC-passing draft"
fi

# ── Stage 4: deterministic show-notes build (inline QC + final gate inside) ──
if [ "$RESUME_EXISTING_DRAFT" -eq 0 ]; then
  blog "agentstack_morning: EP${NEXT_EP_PAD} stage 4 — build show notes"
  if ! python3 "${SCRIPT_DIR}/build_show_notes.py" "$_NEXT_EP" >> "$RUN_LOG" 2>&1; then
    fail_stage "show-notes-build" "build_show_notes.py failed (see run log tail; any rejected draft is saved as ${DRAFT_PATH}.rejected.builder)"
  fi
else
  blog "agentstack_morning: EP${NEXT_EP_PAD} stage 4 — skipped; using existing QC-passing show notes"
fi
if [ ! -s "$DRAFT_PATH" ]; then
  fail_stage "show-notes-build" "no QC-passing ${DRAFT_PATH} was written"
fi
blog "OK EP${NEXT_EP_PAD}: show notes written and QC-passed"

# ── Stage 5: early Discord show-notes post (mid-stream reject gate) ─────────
#    Post the complete story slate as an attachment to #agent-stack-epNNN as
#    soon as show notes pass QC. Telegram remains quiet until listenable review
#    audio exists. This gives Toby a durable place to reject a weak slate before
#    transcript and audio compute are spent; the full review follows in stage 7.
if ! python3 "${SCRIPT_DIR}/post_show_notes_draft_discord.py" "$_NEXT_EP" --file "$DRAFT_PATH" \
      --headline "📝 AgentStack Daily EP${NEXT_EP_PAD} — show notes generated, transcript generation in progress" \
      --note "🛠 Transcript + audio are building now. Reply here to REJECT mid-stream if these stories are bad. The full listenable review follows shortly through ARIA Telegram and this Discord channel." \
      >> "$BUILD_LOG" 2>&1; then
  blog "agentstack_morning: WARN EP${NEXT_EP_PAD} early Discord show-notes post failed (non-fatal; full review still follows)"
  alert_error "⚠️ EP${NEXT_EP_PAD} morning pipeline DEGRADED: the early Discord show-notes review post failed. Transcript and review-audio generation are continuing, but the early review checkpoint is missing. Build log: ${BUILD_LOG}"
else
  blog "agentstack_morning: EP${NEXT_EP_PAD} complete show-notes slate posted to Discord"
fi

# ── Stage 5.5: pre-generate bespoke art in the background ───────────────────
#    Art depends only on show notes, so it overlaps the transcript stage.
#    build_episode stage 5 finds the module ready (or regenerates with its
#    own retries if this background attempt failed) — either way is safe.
_ART_BG_PID=""
if [ ! -f "${SCRIPT_DIR}/episode_art/episode_${NEXT_EP_PAD}_art.py" ]; then
  python3 "${SCRIPT_DIR}/generate_episode_art.py" "$_NEXT_EP" >> "$RUN_LOG" 2>&1 &
  _ART_BG_PID=$!
  blog "agentstack_morning: EP${NEXT_EP_PAD} stage 5.5 — bespoke art pre-generating in background (pid ${_ART_BG_PID})"
fi

# ── Stage 6: transcript generation (model + check_episode.py QC loop) ────────
blog "agentstack_morning: EP${NEXT_EP_PAD} stage 6 — generate transcript"
if ! python3 "${SCRIPT_DIR}/generate_episode_transcript.py" "$_NEXT_EP" >> "$RUN_LOG" 2>&1; then
  fail_stage "transcript" "generate_episode_transcript.py failed after its internal QC-repair attempts AND the gpt-5.6-sol rescue stage"
fi
if [ ! -s "$TRANSCRIPT_PATH" ]; then
  fail_stage "transcript" "no transcript artifact at episodes/episode_${NEXT_EP_PAD}_transcript.md"
fi
blog "OK EP${NEXT_EP_PAD}: transcript written and QC-passed"

# Close the art race before the build: if the background pre-generation is
# still running, wait for it so build_episode never generates concurrently.
if [ -n "$_ART_BG_PID" ]; then
  if ! wait "$_ART_BG_PID" 2>/dev/null; then
    blog "agentstack_morning: WARN art pre-generation failed; build_episode will regenerate"
    alert_error "[RETRY] EP${NEXT_EP_PAD} bespoke-art pre-generation failed; build_episode.py is continuing with its own regeneration attempt. Run log: ${RUN_LOG}"
  fi
fi

# ── Stage 7: full episode build — audio, cover art, CDN, Discord review post ─
blog "agentstack_morning: EP${NEXT_EP_PAD} stage 7 — build episode (audio + art + CDN + review post)"
if ! python3 "${SCRIPT_DIR}/build_episode.py" "$_NEXT_EP" >> "$RUN_LOG" 2>&1; then
  fail_stage "episode-build" "build_episode.py failed (audio/art/CDN/review-post stage; it posts its own step-level failures to build-log)"
fi

blog "OK EP${NEXT_EP_PAD}: morning pipeline complete — review audio posted through ARIA and Discord; publish waits for Toby's verified Discord ✅"
exit 0
