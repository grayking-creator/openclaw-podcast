#!/bin/bash
# Distributed batch-build AgentStack Daily shorts across M3, M4, DGX.
# M3 (local): renders EN shorts
# M4: renders ES and DE shorts
# DGX: renders PT and HI shorts
# Merges everything back onto M3.

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
PODCAST_DIR="$(dirname "$SCRIPTS_DIR")"
STAGING_ROOT="$PODCAST_DIR/content_staging/shorts"
MEDIA_EN_AUDIO_DIR="$HOME/.openclaw/workspace/openclaw-podcast-media-en/audio"
CDN_AUDIO_DIR="$HOME/.openclaw/workspace/openclaw-podcast-audio/audio"
LOCAL_AUDIO_DIR="$PODCAST_DIR/audio"
IMAGES_DIR="$PODCAST_DIR/images"
LOG="$STAGING_ROOT/distribute_build.log"

PYTHON_M3="/Users/tobyglennpeters/.codex-video-tools/.venv/bin/python"
PYTHON_M4="/Users/toby/.openclaw/workspace/video-workspace/crossfire-series/.venv/bin/python"
PYTHON_DGX="/home/toby/.venv_shorts/bin/python3"

mkdir -p "$STAGING_ROOT"
echo "[$(date)] Starting distributed short build" | tee -a "$LOG"

resolve_audio() {
  local ep_str="$1"
  local candidate
  for candidate in \
    "$MEDIA_EN_AUDIO_DIR/episode_${ep_str}.mp3" \
    "$CDN_AUDIO_DIR/episode_${ep_str}.mp3" \
    "$LOCAL_AUDIO_DIR/episode_${ep_str}.mp3"; do
    if [ -f "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

EPISODES=("$@")
if [ ${#EPISODES[@]} -eq 0 ]; then
  mapfile -t EPISODES < <(/usr/bin/env python3 - <<PY
import re
from pathlib import Path
podcast = Path("$PODCAST_DIR")
staging = Path("$STAGING_ROOT")
released = sorted({int(x) for x in re.findall(r"<itunes:episode>(\\d+)</itunes:episode>", (podcast / "feed.xml").read_text())})
missing = []
for ep in released:
    if ep < 58:
        continue
    ep_dir = staging / f"episode_{ep:03d}"
    if not (ep_dir / "clip_01.mp4").exists() or not (ep_dir / "clip_02.mp4").exists():
        missing.append(ep)
for ep in missing[: int("${SHORTS_BUILD_LIMIT:-1}")]:
    print(ep)
PY
  )
fi

if [ ${#EPISODES[@]} -eq 0 ]; then
  echo "[$(date)] No released episodes missing rendered shorts." | tee -a "$LOG"
  exit 0
fi

# Function to rsync local workspace to remote node
sync_to_remote() {
  local host="$1"
  local dest_dir="$2"
  echo "Syncing workspace to $host:$dest_dir..." | tee -a "$LOG"
  ssh "$host" "mkdir -p '$dest_dir'"
  rsync -avz --delete \
    --exclude '.git/' \
    --exclude '.venv/' \
    --exclude '.venv_shorts/' \
    --exclude 'node_modules/' \
    --exclude 'audio/' \
    --exclude 'content_staging/' \
    --exclude '*.log' \
    "$PODCAST_DIR/" "$host:$dest_dir/"

  echo "Syncing episode ${ep_str} staging directory..." | tee -a "$LOG"
  ssh "$host" "mkdir -p '$dest_dir/content_staging/shorts/episode_${ep_str}'"
  rsync -avz \
    "$PODCAST_DIR/content_staging/shorts/episode_${ep_str}/" \
    "$host:$dest_dir/content_staging/shorts/episode_${ep_str}/"
}

# Function to rsync results back from remote node
sync_from_remote() {
  local host="$1"
  local src_dir="$2"
  echo "Syncing results back from $host:$src_dir..." | tee -a "$LOG"
  rsync -avz "$host:$src_dir/content_staging/shorts/" "$STAGING_ROOT/"
}

FAILED=0

for ep_num in "${EPISODES[@]}"; do
  ep_str=$(printf "%03d" "$ep_num")
  out_dir="$STAGING_ROOT/episode_${ep_str}"
  audio="$(resolve_audio "$ep_str" || true)"
  cover="$IMAGES_DIR/episode_${ep_str}_cover.png"

  echo "--------------------------------------------------------" | tee -a "$LOG"
  echo "[$(date)] processing EP${ep_str}..." | tee -a "$LOG"

  # Step 1: Build EN clips locally on M3 (if not already built)
  if [ -f "$out_dir/clip_01.mp4" ] && [ -f "$out_dir/clip_02.mp4" ]; then
    echo "EN clips already exist for EP${ep_str}" | tee -a "$LOG"
  else
    if [ -z "$audio" ]; then
      echo "ERROR: EN audio missing for EP${ep_str}; checked media-en, CDN audio, and local podcast audio" | tee -a "$LOG"
      FAILED=1
      continue
    fi
    if [ ! -f "$cover" ]; then
      echo "ERROR: Cover art missing at $cover" | tee -a "$LOG"
      FAILED=1
      continue
    fi
    mkdir -p "$out_dir"
    echo "Rendering EN clips locally on M3..." | tee -a "$LOG"
    "$PYTHON_M3" "$SCRIPTS_DIR/make_podcast_shorts.py" \
      --input-audio "$audio" \
      --output-dir "$out_dir" \
      --cover "$cover" \
      --episode-label "EP${ep_str}" \
      --num-clips 2 \
      2>&1 | tee -a "$LOG"
  fi

  # Get the actual episode title and URL from feed/metadata
  EP_TITLE=$("$PYTHON_M3" -c "
import sys, re
from pathlib import Path
feed_path = Path('$PODCAST_DIR/feed.xml')
if feed_path.exists():
    content = feed_path.read_text()
    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    for item in items:
        ep_match = re.search(r'<itunes:episode>(\d+)</itunes:episode>', item)
        if ep_match and int(ep_match.group(1)) == $ep_num:
            title_match = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item)
            if title_match:
                print(title_match.group(1).replace(\"'\", \"'\"))
                sys.exit(0)
print('AgentStack Daily EP$ep_str')
")
  
  EP_URL="https://tobyonfitnesstech.com/podcasts/episode-${ep_num}/"

  echo "EP_TITLE: $EP_TITLE" | tee -a "$LOG"

  # Step 2: Sync to M4 and DGX
  sync_to_remote "m4max" "/Users/toby/.openclaw/workspace/openclaw-podcast"
  sync_to_remote "dgxspark" "/home/toby/.openclaw/workspace/openclaw-podcast"

  # Step 3: Run multilingual clips in parallel
  echo "Launching translated short builds in parallel..." | tee -a "$LOG"
  
  # ES & DE on M4
  ssh m4max "
    set -e
    export PATH=/opt/homebrew/bin:\$PATH
    source ~/.openclaw/workspace/video-workspace/crossfire-series/.venv/bin/activate
    cd /Users/toby/.openclaw/workspace/openclaw-podcast
    echo 'Starting ES/DE rendering on M4 (Clip 1)...'
    python3 scripts/build_translated_short_with_gpt52.py --episode $ep_num --lang es --clip-index 0 --episode-title \"$EP_TITLE\" --full-episode-url \"$EP_URL\" & p1=\$!
    python3 scripts/build_translated_short_with_gpt52.py --episode $ep_num --lang de --clip-index 0 --episode-title \"$EP_TITLE\" --full-episode-url \"$EP_URL\" & p2=\$!
    render_status=0
    wait \$p1 || render_status=1
    wait \$p2 || render_status=1
    if [ \"\$render_status\" -ne 0 ]; then
      echo 'M4 Clip 1 rendering failed.'
      exit \$render_status
    fi

    echo 'Starting ES/DE rendering on M4 (Clip 2)...'
    python3 scripts/build_translated_short_with_gpt52.py --episode $ep_num --lang es --clip-index 1 --episode-title \"$EP_TITLE\" --full-episode-url \"$EP_URL\" & p3=\$!
    python3 scripts/build_translated_short_with_gpt52.py --episode $ep_num --lang de --clip-index 1 --episode-title \"$EP_TITLE\" --full-episode-url \"$EP_URL\" & p4=\$!
    wait \$p3 || render_status=1
    wait \$p4 || render_status=1
    if [ \"\$render_status\" -eq 0 ]; then
      echo 'M4 rendering done.'
    else
      echo 'M4 rendering failed.'
    fi
    exit \$render_status
  " > "$STAGING_ROOT/m4_render_ep${ep_str}.log" 2>&1 &
  PID_M4=$!

  # PT & HI on DGX
  ssh dgxspark "
    set -e
    export PATH=/home/toby/.hermes/node/bin:\$PATH
    source ~/.venv_shorts/bin/activate
    cd /home/toby/.openclaw/workspace/openclaw-podcast
    echo 'Starting PT/HI rendering on DGX (Clip 1)...'
    python3 scripts/build_translated_short_with_gpt52.py --episode $ep_num --lang pt --clip-index 0 --episode-title \"$EP_TITLE\" --full-episode-url \"$EP_URL\" & p1=\$!
    python3 scripts/build_translated_short_with_gpt52.py --episode $ep_num --lang hi --clip-index 0 --episode-title \"$EP_TITLE\" --full-episode-url \"$EP_URL\" & p2=\$!
    render_status=0
    wait \$p1 || render_status=1
    wait \$p2 || render_status=1
    if [ \"\$render_status\" -ne 0 ]; then
      echo 'DGX Clip 1 rendering failed.'
      exit \$render_status
    fi

    echo 'Starting PT/HI rendering on DGX (Clip 2)...'
    python3 scripts/build_translated_short_with_gpt52.py --episode $ep_num --lang pt --clip-index 1 --episode-title \"$EP_TITLE\" --full-episode-url \"$EP_URL\" & p3=\$!
    python3 scripts/build_translated_short_with_gpt52.py --episode $ep_num --lang hi --clip-index 1 --episode-title \"$EP_TITLE\" --full-episode-url \"$EP_URL\" & p4=\$!
    wait \$p3 || render_status=1
    wait \$p4 || render_status=1
    if [ \"\$render_status\" -eq 0 ]; then
      echo 'DGX rendering done.'
    else
      echo 'DGX rendering failed.'
    fi
    exit \$render_status
  " > "$STAGING_ROOT/dgx_render_ep${ep_str}.log" 2>&1 &
  PID_DGX=$!

  # Wait for both remote tasks to complete
  echo "Waiting for M4 (PID $PID_M4) and DGX (PID $PID_DGX) to finish rendering EP${ep_str}..." | tee -a "$LOG"
  remote_status=0
  wait $PID_M4 || remote_status=1
  wait $PID_DGX || remote_status=1
  if [ "$remote_status" -ne 0 ]; then
    echo "ERROR: One of the remote rendering jobs failed for EP${ep_str}." | tee -a "$LOG"
    echo "Check M4 log: $STAGING_ROOT/m4_render_ep${ep_str}.log" | tee -a "$LOG"
    echo "Check DGX log: $STAGING_ROOT/dgx_render_ep${ep_str}.log" | tee -a "$LOG"
    exit 1
  fi

  # Step 4: Sync results back
  sync_from_remote "m4max" "/Users/toby/.openclaw/workspace/openclaw-podcast"
  sync_from_remote "dgxspark" "/home/toby/.openclaw/workspace/openclaw-podcast"

  echo "✅ Finished EP${ep_str} for all languages." | tee -a "$LOG"
done

if [ "$FAILED" -ne 0 ]; then
  echo "[$(date)] Distributed build finished with missing-input failures" | tee -a "$LOG"
  exit 1
fi

echo "[$(date)] Distributed build completed successfully" | tee -a "$LOG"
