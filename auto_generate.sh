#!/bin/bash
set -euo pipefail

PODCAST_DIR="/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast"

echo "❌ auto_generate.sh is disabled."
echo "This script bypassed episode QC/rendering safeguards and targeted the wrong workspace."
echo
echo "Use the supported build pipeline instead:"
echo "  cd ${PODCAST_DIR}"
echo "  python3 scripts/build_episode.py <episode_number>"
exit 1
