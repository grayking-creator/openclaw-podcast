#!/bin/bash
# Regenerate an UNRELEASED episode from scratch — show notes, transcript, AND
# audio — and re-post the review. Use this when Toby disapproves the show notes:
# all three artifacts are downstream of the notes, so all three are rebuilt.
#
#   scripts/regen_episode.sh <N> ["optional guidance for the rebuild"]
#
# It archives the current notes + transcript (audio is overwritten by
# --force-audio) so nothing is silently lost, re-gathers research, rebuilds the
# show notes with the deterministic builder (+ repair loop), regenerates the
# transcript, and runs build_episode.py to remake audio/art and post one fresh
# review. Publish still requires Toby's ✅ — this never releases.
#
# Guard: refuses to run if the episode is already in feed.xml (released).

set -u

SCRIPT_DIR=/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/scripts
PODCAST_DIR=/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast
ARCHIVE_DIR="${PODCAST_DIR}/archive/regen"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

if [ "$#" -lt 1 ]; then
  echo "usage: regen_episode.sh <episode_number> [guidance]" >&2
  exit 64
fi
EP="$1"
EP_PAD=$(printf "%03d" "$EP")
GUIDANCE="${2:-}"

NOTES="${PODCAST_DIR}/show_notes_episode_${EP_PAD}.md"
TRANSCRIPT="${PODCAST_DIR}/episodes/episode_${EP_PAD}_transcript.md"
STAMP=$(date +%Y%m%d-%H%M%S)

# Released-episode guard: feed.xml is the canonical release record.
if grep -q "episode_${EP_PAD}\b\|Episode ${EP}\b\|EP${EP_PAD}\b" "${PODCAST_DIR}/feed.xml" 2>/dev/null; then
  echo "❌ EP${EP_PAD} appears in feed.xml — it looks released. Refusing to regen a released episode." >&2
  echo "   If this is wrong, regen the artifacts manually with build_show_notes.py / generate_episode_transcript.py / build_episode.py." >&2
  exit 3
fi

mkdir -p "$ARCHIVE_DIR"
echo "[regen] EP${EP_PAD}: archiving current artifacts (stamp ${STAMP})"
[ -f "$NOTES" ] && mv "$NOTES" "${ARCHIVE_DIR}/show_notes_episode_${EP_PAD}.md.${STAMP}"
[ -f "$TRANSCRIPT" ] && mv "$TRANSCRIPT" "${ARCHIVE_DIR}/episode_${EP_PAD}_transcript.md.${STAMP}"

echo "[regen] EP${EP_PAD}: gathering fresh research"
python3 "${SCRIPT_DIR}/gather_research_context.py" || { echo "❌ research gather failed" >&2; exit 1; }

echo "[regen] EP${EP_PAD}: rebuilding show notes"
BUILD_ARGS=("$EP" --force)
[ -n "$GUIDANCE" ] && export SHOW_NOTES_EXTRA_GUIDANCE="$GUIDANCE"
if ! python3 "${SCRIPT_DIR}/build_show_notes.py" "${BUILD_ARGS[@]}"; then
  echo "❌ show-notes rebuild failed (rejected draft saved as ${NOTES}.rejected.builder)" >&2
  exit 1
fi

echo "[regen] EP${EP_PAD}: regenerating transcript"
if ! python3 "${SCRIPT_DIR}/generate_episode_transcript.py" "$EP" --force; then
  echo "❌ transcript regeneration failed" >&2
  exit 1
fi

echo "[regen] EP${EP_PAD}: rebuilding audio + art + posting fresh review"
if ! python3 "${SCRIPT_DIR}/build_episode.py" "$EP" --force-audio; then
  echo "❌ episode build failed" >&2
  exit 1
fi

echo "✅ EP${EP_PAD} regenerated — new review (notes + transcript + audio) posted. Publish still waits for Toby's ✅."
