#!/bin/bash
# Batch-build AgentStack Daily shorts for EP058-EP064
# Renders 2 short clips per episode into content_staging/shorts/episode_NNN/
# Run once — idempotent (skips if clip_01.mp4 already exists)

set -euo pipefail

PYTHON="/Users/tobyglennpeters/.codex-video-tools/.venv/bin/python"
SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
PODCAST_DIR="$(dirname "$SCRIPTS_DIR")"
STAGING_ROOT="$PODCAST_DIR/content_staging/shorts"
AUDIO_DIR="$HOME/.openclaw/workspace/openclaw-podcast-media-en/audio"
IMAGES_DIR="$PODCAST_DIR/images"
LOG="$STAGING_ROOT/batch_build.log"

mkdir -p "$STAGING_ROOT"
echo "[$(date)] Starting batch short build EP058-EP064" | tee -a "$LOG"

EPISODES=(58 59 60 61 62 63 64)

for ep_num in "${EPISODES[@]}"; do
  ep_str=$(printf "%03d" "$ep_num")
  out_dir="$STAGING_ROOT/episode_${ep_str}"
  audio="$AUDIO_DIR/episode_${ep_str}.mp3"
  cover="$IMAGES_DIR/episode_${ep_str}_cover.png"

  # Skip if already built
  if [ -f "$out_dir/clip_01.mp4" ] && [ -f "$out_dir/clip_02.mp4" ]; then
    echo "[$(date)] EP${ep_str}: already built — skipping" | tee -a "$LOG"
    continue
  fi

  if [ ! -f "$audio" ]; then
    echo "[$(date)] EP${ep_str}: MISSING audio $audio — skipping" | tee -a "$LOG"
    continue
  fi
  if [ ! -f "$cover" ]; then
    echo "[$(date)] EP${ep_str}: MISSING cover $cover — skipping" | tee -a "$LOG"
    continue
  fi

  mkdir -p "$out_dir"
  echo "[$(date)] EP${ep_str}: building shorts..." | tee -a "$LOG"

  "$PYTHON" "$SCRIPTS_DIR/make_podcast_shorts.py" \
    --input-audio "$audio" \
    --output-dir "$out_dir" \
    --cover "$cover" \
    --episode-label "EP${ep_str}" \
    --num-clips 2 \
    2>&1 | tee -a "$LOG"

  if [ -f "$out_dir/clip_01.mp4" ]; then
    echo "[$(date)] EP${ep_str}: ✅ done" | tee -a "$LOG"
  else
    echo "[$(date)] EP${ep_str}: ❌ clip_01.mp4 not found after render" | tee -a "$LOG"
  fi
done

echo "[$(date)] Batch build complete" | tee -a "$LOG"
