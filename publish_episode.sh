#!/bin/bash
# publish_episode.sh — Episode publish script
# Usage: bash publish_episode.sh 14
# Handles: canonical audio/CDN sync, cover art copy, feed checks, website build

set -e

EP=$1
if [ -z "$EP" ]; then
  echo "Usage: bash publish_episode.sh <episode_number>"
  exit 1
fi

EPNUM=$(printf "%03d" $EP)
WORKSPACE="$HOME/.openclaw/workspace"
PODCAST_DIR="$WORKSPACE/openclaw-podcast"
CDN_DIR="$WORKSPACE/openclaw-podcast-audio"
WEBSITE_PUBLIC="$WORKSPACE/websiteBuilder/frontend/public/images/podcast"
AUDIO_URL_BASE="https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/audio"
COVER_URL_BASE="https://clawdassistant85-netizen.github.io/openclaw-podcast-audio"

AUDIO_SRC="$PODCAST_DIR/audio/episode_${EPNUM}.mp3"
CDN_AUDIO_DST="$CDN_DIR/audio/episode_${EPNUM}.mp3"
LATEST_AUDIO_DST="$CDN_DIR/audio/latest.mp3"

echo "=== Publishing Episode $EP (episode_$EPNUM) ==="

# ── Step 1: Canonical audio sync (replace bad public file + update latest link)
echo ""
echo "[ 1/6 ] Syncing canonical audio to CDN..."
if [ ! -f "$AUDIO_SRC" ]; then
  echo "  ❌ MISSING: $AUDIO_SRC"
  exit 1
fi
cp "$AUDIO_SRC" "$CDN_AUDIO_DST"
cp "$AUDIO_SRC" "$LATEST_AUDIO_DST"
echo "  ✅ Episode audio synced to $CDN_AUDIO_DST"
echo "  ✅ Stable latest link synced to $LATEST_AUDIO_DST"

# ── Step 2: Cover art copy (the thing that keeps getting missed) ──────────────
COVER_SRC="$PODCAST_DIR/images/episode_${EPNUM}_cover.png"
COVER_DST="$WEBSITE_PUBLIC/episode_${EPNUM}_cover.png"
CDN_COVER_DST="$CDN_DIR/episode_${EPNUM}_cover.png"

echo ""
echo "[ 2/6 ] Cover art..."
if [ ! -f "$COVER_SRC" ]; then
  echo "  ❌ MISSING: $COVER_SRC"
  exit 1
fi
cp "$COVER_SRC" "$COVER_DST"
cp "$COVER_SRC" "$CDN_COVER_DST"
echo "  ✅ Copied to $COVER_DST"
echo "  ✅ Copied to $CDN_COVER_DST"

# ── Step 3: Verify feed.xml has the episode ──────────────────────────────────
echo ""
echo "[ 3/6 ] Checking feed.xml..."
if grep -q "episode_${EPNUM}" "$PODCAST_DIR/feed.xml"; then
  echo "  ✅ EN feed.xml has episode_$EPNUM"
else
  echo "  ❌ episode_$EPNUM not found in feed.xml — add it before publishing"
  exit 1
fi

# ── Step 4: Push to grayking-creator/openclaw-podcast ─────────────────────────
echo ""
echo "[ 4/6 ] Pushing podcast repo (feed.xml + assets)..."
cd "$PODCAST_DIR"
PODCAST_STAGE_PATHS=()
for rel in \
  "feed.xml" \
  "images/episode_${EPNUM}_cover.png" \
  "show_notes_episode_${EPNUM}.md" \
  "episodes/episode_${EPNUM}_transcript.md" \
  "translations/feed_de.xml" \
  "translations/feed_es.xml" \
  "translations/feed_hi.xml" \
  "translations/feed_pt.xml"; do
  if [ -e "$PODCAST_DIR/$rel" ]; then
    PODCAST_STAGE_PATHS+=("$rel")
  fi
done
git add -- "${PODCAST_STAGE_PATHS[@]}"
git diff --cached --quiet && echo "  ℹ️  Nothing new to commit in podcast repo" || \
  (git commit -m "EP$EP: publish episode_$EPNUM" && git push && echo "  ✅ Podcast repo pushed")

# ── Step 5: Push CDN repo ─────────────────────────────────────────────────────
echo ""
echo "[ 5/6 ] Pushing CDN repo (canonical + latest audio, cover)..."
cd "$CDN_DIR"
git add "audio/episode_${EPNUM}.mp3" "audio/latest.mp3" "episode_${EPNUM}_cover.png"
git diff --cached --quiet && echo "  ℹ️  Nothing new to commit in CDN repo" || \
  (git commit -m "EP$EP: sync canonical audio + latest link + cover" && git push && echo "  ✅ CDN repo pushed")

# ── Step 6: Refresh training data + build website ─────────────────────────────
echo ""
echo "[ 6/6 ] Refreshing training data and building website..."
cd "$WORKSPACE"
python3 scripts/update_website_training_data.py --skip-sync 2>&1 | tail -5

echo ""
echo "[ website ] Pushing website..."
cd "$WORKSPACE/websiteBuilder"
git add -A
git diff --cached --quiet && echo "  ℹ️  Nothing new to commit in website repo" || \
  (git commit -m "EP$EP: cover art + website update" && git push && echo "  ✅ Website pushed")

echo ""
echo "=== ✅ Episode $EP publish complete ==="
echo "  Cover art: $COVER_DST"
echo "  Feed: https://clawdassistant85-netizen.github.io/openclaw-podcast/feed.xml"
echo "  Website: https://tobyonfitnesstech.com/podcasts/openclaw/"
echo ""
echo "Discord / build-log links:"
echo "  Episode audio: ${AUDIO_URL_BASE}/episode_${EPNUM}.mp3"
echo "  Latest audio:  ${AUDIO_URL_BASE}/latest.mp3"
echo "  Cover art:     ${COVER_URL_BASE}/episode_${EPNUM}_cover.png"
