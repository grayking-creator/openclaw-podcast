#!/bin/bash
# AgentStack Daily — full morning pipeline.
#
# Goal: by 8:00 AM ET a complete, listenable episode (show notes + transcript +
# EN audio + cover art) is on the CDN with a review post in Discord. Publish
# still requires Toby's explicit ✅ on the review audio — this script never
# releases anything.
#
# Stages:
#   1. sync episode counter against live YouTube channel
#   2. collision check (existing un-released draft → HOLD, exit 2)
#   3. gather_research_context.py     (deterministic data collection)
#   4. build_show_notes.py            (deterministic builder + inline section QC,
#                                      final check_show_notes.py gate inside)
#   5. post_show_notes_draft_discord  (draft attachment for reference; non-fatal)
#   6. generate_episode_transcript.py (model + check_episode.py QC loop)
#   7. build_episode.py               (slate verify, QC, nova render, EN audio,
#                                      bespoke cover art, CDN push, Discord
#                                      review post — stops at approval gate)
#
# Launched by show_notes_research_guard.sh from cron. All failures append to
# BUILD_LOG and post to the Discord alerts channel (per graduated lesson:
# research cron failures must always leave both trails).

set -u

BUILD_LOG="${SHOW_NOTES_BUILD_LOG:-/tmp/show_notes_build.log}"
RUN_LOG="${SHOW_NOTES_RESEARCH_LOG:-/tmp/show_notes_research.log}"
ALERTS_CHANNEL=1485243812442804327
SCRIPT_DIR=/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/scripts
PODCAST_DIR=/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast
DONE_FILE="${SCRIPT_DIR}/youtube_uploaded.txt"
OPENCLAW_BIN="${OPENCLAW_BIN:-/opt/homebrew/bin/openclaw}"

# cron runs with a minimal PATH; the pipeline needs homebrew tools
# (openclaw, ffmpeg, git helpers) on every stage.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

ts() { date '+%Y-%m-%d %H:%M:%S'; }
blog() { printf '[%s] %s\n' "$(ts)" "$*" >> "$BUILD_LOG"; }

alert() {
  "$OPENCLAW_BIN" message send --channel discord --target "channel:$ALERTS_CHANNEL" \
    --message "$1" >> "$BUILD_LOG" 2>&1 || blog "agentstack_morning: WARN Discord alert failed"
}

fail_stage() {
  local stage=$1 detail=$2
  blog "FAIL EP${NEXT_EP_PAD:-???} stage '${stage}': ${detail}"
  alert "❌ EP${NEXT_EP_PAD:-???} morning pipeline FAILED at stage: ${stage}
${detail}
Run log: ${RUN_LOG}
Build log: ${BUILD_LOG}"
  exit 1
}

blog "agentstack_morning: starting"

# ── Stage 1: sync against live YouTube channel ───────────────────────────────
if [ -f "${SCRIPT_DIR}/sync_uploaded_from_youtube.py" ]; then
  python3 "${SCRIPT_DIR}/sync_uploaded_from_youtube.py" >> "$BUILD_LOG" 2>&1 || \
    blog "agentstack_morning: WARN youtube sync failed; using local counter"
fi

_LAST_EP=$(tail -1 "$DONE_FILE" | tr -d '[:space:]')
_NEXT_EP=$(( 10#$_LAST_EP + 1 ))
NEXT_EP_PAD=$(printf "%03d" "$_NEXT_EP")
DRAFT_PATH="${PODCAST_DIR}/show_notes_episode_${NEXT_EP_PAD}.md"
TRANSCRIPT_PATH="${PODCAST_DIR}/episodes/episode_${NEXT_EP_PAD}_transcript.md"

blog "agentstack_morning: targeting EP${NEXT_EP_PAD} (last released: EP${_LAST_EP})"

# ── Stage 2: collision check — an existing draft means yesterday's episode
#    was never released; that's a numbering decision for a human, not a build.
if [ -f "$DRAFT_PATH" ]; then
  MSG="⚠️ EP${NEXT_EP_PAD} draft already exists and has not been released
File: show_notes_episode_${NEXT_EP_PAD}.md

The morning pipeline is stopping so yesterday's stories are not stranded and EP$(printf "%03d" $(( _NEXT_EP + 1 ))) is not silently created.

Choose one recovery path:
1. Keep the prior stories: python3 ${SCRIPT_DIR}/resolve_episode_gap.py prepare-merge --prior ${_NEXT_EP} --target $(printf "%03d" $(( _NEXT_EP + 1 )))
2. Replace the prior stories: python3 ${SCRIPT_DIR}/resolve_episode_gap.py archive ${_NEXT_EP} --reason 'replaced before transcript generation'

No new draft was created. This is a release-numbering decision, not a YouTube upload status."
  blog "HOLD EP${NEXT_EP_PAD}: draft already exists; decision required"
  alert "$MSG"
  exit 2
fi

# ── Stage 3: research gathering (deterministic) ──────────────────────────────
blog "agentstack_morning: EP${NEXT_EP_PAD} stage 3 — gather research context"
if ! python3 "${SCRIPT_DIR}/gather_research_context.py" >> "$RUN_LOG" 2>&1; then
  fail_stage "research-gather" "gather_research_context.py exited nonzero"
fi
if [ ! -s /tmp/agent_research_context.json ]; then
  fail_stage "research-gather" "no /tmp/agent_research_context.json produced"
fi

# ── Stage 4: deterministic show-notes build (inline QC + final gate inside) ──
blog "agentstack_morning: EP${NEXT_EP_PAD} stage 4 — build show notes"
if ! python3 "${SCRIPT_DIR}/build_show_notes.py" "$_NEXT_EP" >> "$RUN_LOG" 2>&1; then
  fail_stage "show-notes-build" "build_show_notes.py failed (see run log tail; any rejected draft is saved as ${DRAFT_PATH}.rejected.builder)"
fi
if [ ! -s "$DRAFT_PATH" ]; then
  fail_stage "show-notes-build" "no QC-passing ${DRAFT_PATH} was written"
fi
blog "OK EP${NEXT_EP_PAD}: show notes written and QC-passed"

# ── Stage 5: post draft to Discord (reference copy; review audio comes later) ─
if ! python3 "${SCRIPT_DIR}/post_show_notes_draft_discord.py" "$_NEXT_EP" --file "$DRAFT_PATH" >> "$BUILD_LOG" 2>&1; then
  blog "agentstack_morning: WARN EP${NEXT_EP_PAD} draft Discord attachment failed (non-fatal; review post follows after build)"
fi

# ── Stage 6: transcript generation (model + check_episode.py QC loop) ────────
blog "agentstack_morning: EP${NEXT_EP_PAD} stage 6 — generate transcript"
if ! python3 "${SCRIPT_DIR}/generate_episode_transcript.py" "$_NEXT_EP" >> "$RUN_LOG" 2>&1; then
  fail_stage "transcript" "generate_episode_transcript.py failed after its internal QC-repair attempts"
fi
if [ ! -s "$TRANSCRIPT_PATH" ]; then
  fail_stage "transcript" "no transcript artifact at episodes/episode_${NEXT_EP_PAD}_transcript.md"
fi
blog "OK EP${NEXT_EP_PAD}: transcript written and QC-passed"

# ── Stage 7: full episode build — audio, cover art, CDN, Discord review post ─
blog "agentstack_morning: EP${NEXT_EP_PAD} stage 7 — build episode (audio + art + CDN + review post)"
if ! python3 "${SCRIPT_DIR}/build_episode.py" "$_NEXT_EP" >> "$RUN_LOG" 2>&1; then
  fail_stage "episode-build" "build_episode.py failed (audio/art/CDN/review-post stage; it posts its own step-level failures to build-log)"
fi

blog "OK EP${NEXT_EP_PAD}: morning pipeline complete — review audio posted; publish waits for Toby's ✅"
exit 0
