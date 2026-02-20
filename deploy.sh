#!/bin/bash
# Podcast RSS Feed Generator & GitHub Pages Deploy Script
# Run this to generate RSS feed and deploy to GitHub Pages

PODCAST_DIR="/Users/tobyglennpeters/.openclaw/workspace/podcast"
REPO_URL="https://github.com/grayking-creator/openclaw-podcast.git"

echo "📡 Generating RSS feed..."

cd "$PODCAST_DIR"

# Generate timestamp
LAST_BUILD=$(date -u +"%a, %d %b %Y %H:%M:%S GMT")

# Replace placeholder in feed.xml
sed -i '' "s/{{LAST_BUILD_DATE}}/$LAST_BUILD/" feed.xml

echo "✅ RSS feed generated"

# Check if git remote exists, if not add it
if ! git remote get-url origin > /dev/null 2>&1; then
    git remote add origin "$REPO_URL"
fi

# Add files
git add .
git commit -m "Podcast update $(date)"

# Push to GitHub
echo "🚀 Deploying to GitHub Pages..."
git push origin main

echo "✅ Done! Your podcast RSS feed is live at:"
echo "   https://grayking-creator.github.io/openclaw-podcast/feed.xml"
