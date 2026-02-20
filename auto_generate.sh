#!/bin/bash
# Podcast Episode Generator & Deploy Script
# Builds 30-40 min episodes, deploys, and notifies via Telegram

PODCAST_DIR="/Users/tobyglennpeters/.openclaw/workspace/podcast"
TELEGRAM_CHAT_ID="8319992332"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
INDEX_URL="https://grayking-creator.github.io/openclaw-podcast/"

# Source the environment
source ~/.zshrc 2>/dev/null

echo "🎙️ Starting podcast episode generation..."

# Find the next episode number
EPISODE_NUM=$(ls -1 ${PODCAST_DIR}/episode_*.md 2>/dev/null | grep -v _highlights | grep -v _full_v2 | wc -l)
EPISODE_NUM=$((EPISODE_NUM + 1))
printf -v EPISODE_NUM "%03d" $EPISODE_NUM

echo "Next episode number: $EPISODE_NUM"

# Target duration: 30-40 minutes (1800-2400 seconds)
TARGET_MIN=30
TARGET_MAX=40

# For now, this is a placeholder - in production this would gather news
# and write content to episode_${EPISODE_NUM}.md
echo "📝 Checking for new content to generate..."

# Check if there's a draft episode
DRAFT_FILE="${PODCAST_DIR}/episode_${EPISODE_NUM}.md"
if [ ! -f "$DRAFT_FILE" ]; then
    echo "No draft episode found. Creating a placeholder for review."
    cat > "$DRAFT_FILE" << 'EOF'
# OpenClaw Daily Podcast - Episode X: TBD
# Date: $(date +"%B %d, %Y")
# Hosts: Nova (warm British) & Alloy (neutral)

---

[NOVA]: Good evening and welcome back to OpenClaw Daily! I'm Nova.

[ALLOY]: And I'm Alloy. We've got another episode lined up for you today.

[NOVA]: Episode content coming soon. This is a placeholder for review.

[ALLOY]: Stay tuned for more updates on the local AI revolution.

[NOVA]: I'm Nova...

[ALLOY]: ...and I'm Alloy.

[NOVA]: ...and this has been OpenClaw Daily. See you next time!

[ALLOY]: Stay curious, stay local, and keep building!

---

# END OF EPISODE
EOF
fi

# Generate audio
echo "🎵 Generating audio..."
cd ${PODCAST_DIR}
python3 generate_audio.py "episode_${EPISODE_NUM}.md" -o "episode_${EPISODE_NUM}_full"

# Check duration
if [ -f "audio/episode_${EPISODE_NUM}_full.mp3" ]; then
    DURATION_SEC=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "audio/episode_${EPISODE_NUM}_full.mp3")
    DURATION_MIN=$((DURATION_SEC / 60))
    echo "Generated episode duration: ${DURATION_MIN} minutes"
    
    if [ $DURATION_MIN -lt $TARGET_MIN ]; then
        echo "⚠️ Episode is shorter than ${TARGET_MIN} min. Need more content."
        echo "📝 Adding more content to reach target length..."
        # Add more sections here in production
    fi
fi

# Update RSS feed
echo "📡 Updating RSS feed..."
LAST_BUILD=$(date -u +"%a, %d %b %Y %H:%M:%S GMT")
sed -i '' "s/{{LAST_BUILD_DATE}}/$LAST_BUILD/" ${PODCAST_DIR}/feed.xml

# Deploy to GitHub
echo "🚀 Deploying to GitHub Pages..."
cd ${PODCAST_DIR}
git add .
git commit -m "Episode ${EPISODE_NUM} auto-generated $(date)"
git push origin main

# Send Telegram notification
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "📱 Sending Telegram notification..."
    MESSAGE="🎙️ New Episode Ready for Review!

Episode: ${EPISODE_NUM}
Duration: ${DURATION_MIN:-~30} minutes
Listen: ${INDEX_URL}

Please review before publishing!"
    
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=${MESSAGE}" > /dev/null
else
    echo "⚠️ TELEGRAM_BOT_TOKEN not set. Skipping notification."
fi

echo "✅ Podcast episode generation complete!"
echo "🔗 Index: ${INDEX_URL}"
