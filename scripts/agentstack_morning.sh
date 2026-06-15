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
#                                      final check_show_notes.py gate + repair
#                                      loop inside — a QC drift costs a repair
#                                      round, never the morning run)
#   5. post_show_notes_draft_discord  (EARLY post: story slate + "transcript in
#                                      progress" so Toby can reject mid-stream
#                                      before the audio compute is spent)
#   6. generate_episode_transcript.py (model + check_episode.py QC loop)
#   7. build_episode.py               (slate verify, QC, nova render, EN audio,
#                                      bespoke cover art, CDN push, full Discord
#                                      review post bundling notes+transcript+audio
#                                      — stops at approval gate)
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
RESUME_EXISTING_DRAFT=0

blog "agentstack_morning: targeting EP${NEXT_EP_PAD} (last released: EP${_LAST_EP})"

# ── Stage 2: collision check / resume.
#    A QC-passing draft should not strand a day of audio work. Resume from it.
#    A failed draft is archived and rebuilt with fresh context.
if [ -f "$DRAFT_PATH" ]; then
  blog "agentstack_morning: EP${NEXT_EP_PAD} existing draft found — checking whether it can resume"
  if python3 "${SCRIPT_DIR}/check_show_notes.py" "$DRAFT_PATH" >> "$BUILD_LOG" 2>&1; then
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
  blog "agentstack_morning: EP${NEXT_EP_PAD} stage 3 — gather research context"
  if ! python3 "${SCRIPT_DIR}/gather_research_context.py" >> "$RUN_LOG" 2>&1; then
    fail_stage "research-gather" "gather_research_context.py exited nonzero"
  fi
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

# ── Stage 5: early show-notes post (mid-stream reject gate, 2026-06-15) ──────
#    Post the generated story slate the moment the show notes pass QC, BEFORE the
#    expensive transcript + audio steps, so Toby can reject bad stories early and
#    save the compute. The full bundled review (notes+transcript+audio) still
#    follows from stage 7.
if ! python3 "${SCRIPT_DIR}/post_show_notes_draft_discord.py" "$_NEXT_EP" --file "$DRAFT_PATH" \
      --headline "📝 AgentStack Daily EP${NEXT_EP_PAD} — show notes generated, transcript generation in progress" \
      --note "🛠 Transcript + audio are building now. Reply here to REJECT mid-stream if these stories are bad — that stops the run before the audio is wasted. The full listenable review (transcript + audio) follows shortly." \
      >> "$BUILD_LOG" 2>&1; then
  blog "agentstack_morning: WARN EP${NEXT_EP_PAD} early show-notes post failed (non-fatal; full review still follows)"
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
