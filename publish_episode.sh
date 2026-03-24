#!/bin/bash
# publish_episode.sh — Episode publish script
# Usage: bash publish_episode.sh 14
# Handles: cover art copy, feed updates, CDN push, website build

set -e

EP=$1
if [ -z "$EP" ]; then
  echo "Usage: bash publish_episode.sh <episode_number>"
  exit 1
fi

EPNUM=$(printf "%03d" $EP)
WORKSPACE="$HOME/.openclaw/workspace"
PODCAST_DIR="$WORKSPACE/openclaw-podcast"
WEBSITE_PUBLIC="$WORKSPACE/websiteBuilder/frontend/public/images/podcast"

echo "=== Publishing Episode $EP (episode_$EPNUM) ==="

# ── Step 1: Cover art copy (the thing that keeps getting missed) ──────────────
COVER_SRC="$PODCAST_DIR/images/episode_${EPNUM}_cover.png"
COVER_DST="$WEBSITE_PUBLIC/episode_${EPNUM}_cover.png"

echo ""
echo "[ 1/5 ] Cover art..."
if [ ! -f "$COVER_SRC" ]; then
  echo "  ❌ MISSING: $COVER_SRC"
  exit 1
fi
cp "$COVER_SRC" "$COVER_DST"
echo "  ✅ Copied to $COVER_DST"

# ── Step 2: Verify feed.xml has the episode ──────────────────────────────────
echo ""
echo "[ 2/5 ] Checking feed.xml..."
if grep -q "episode_${EPNUM}" "$PODCAST_DIR/feed.xml"; then
  echo "  ✅ EN feed.xml has episode_$EPNUM"
else
  echo "  ❌ episode_$EPNUM not found in feed.xml — add it before publishing"
  exit 1
fi

# ── Step 3: Push to grayking-creator/openclaw-podcast ─────────────────────────
echo ""
echo "[ 3/5 ] Pushing podcast repo (feed.xml + assets)..."
cd "$PODCAST_DIR"
git add -A
git diff --cached --quiet && echo "  ℹ️  Nothing new to commit in podcast repo" || \
  (git commit -m "EP$EP: publish episode_$EPNUM" && git push && echo "  ✅ Podcast repo pushed")

# ── Step 4: Refresh training data + build website ─────────────────────────────
echo ""
echo "[ 4/5 ] Refreshing training data and building website..."
cd "$WORKSPACE"
python3 scripts/update_website_training_data.py --skip-sync 2>&1 | tail -5

# ── Step 5: Push websiteBuilder ───────────────────────────────────────────────
echo ""
echo "[ 5/5 ] Pushing website..."
cd "$WORKSPACE/websiteBuilder"
git add -A
git diff --cached --quiet && echo "  ℹ️  Nothing new to commit in website repo" || \
  (git commit -m "EP$EP: cover art + website update" && git push && echo "  ✅ Website pushed")

echo ""
echo "=== ✅ Episode $EP publish complete ==="
echo "  Cover art: $COVER_DST"
echo "  Feed: https://grayking-creator.github.io/openclaw-podcast/feed.xml"
echo "  Website: https://tobyonfitnesstech.com/podcasts/openclaw/"
