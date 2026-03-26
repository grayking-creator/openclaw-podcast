#!/bin/bash
# YouTube scheduled upload runner
# Checks the schedule and uploads the next due episode
# Run via cron at 5AM and 6PM ET

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCHEDULE="${SCRIPT_DIR}/youtube_upload_schedule.json"
LOG="/tmp/youtube_upload_cron.log"
VENV_PYTHON="/opt/homebrew/bin/python3"

echo "[$(date)] YouTube cron runner started" >> "$LOG"

# Find the next episode that should have been uploaded by now
NEXT_EP=$($VENV_PYTHON -c "
import json, sys
from datetime import datetime, timezone, timedelta

with open('${SCHEDULE}') as f:
    data = json.load(f)

now = datetime.now(timezone(timedelta(hours=-4)))
done_file = '${SCRIPT_DIR}/youtube_uploaded.txt'

try:
    with open(done_file) as f:
        done = set(int(x.strip()) for x in f.readlines() if x.strip())
except FileNotFoundError:
    done = set()

for entry in data['schedule']:
    ep = entry['episode']
    dt = datetime.fromisoformat(entry['datetime'])
    if ep not in done and dt <= now:
        print(ep)
        sys.exit(0)

print('NONE')
" 2>/dev/null)

if [ "$NEXT_EP" = "NONE" ] || [ -z "$NEXT_EP" ]; then
    echo "[$(date)] No episodes due for upload" >> "$LOG"
    exit 0
fi

echo "[$(date)] Uploading EP${NEXT_EP}..." >> "$LOG"

cd "$SCRIPT_DIR"
$VENV_PYTHON youtube_scheduled_upload.py "$NEXT_EP" >> "$LOG" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "$NEXT_EP" >> "${SCRIPT_DIR}/youtube_uploaded.txt"
    echo "[$(date)] ✅ EP${NEXT_EP} upload complete" >> "$LOG"
else
    echo "[$(date)] ⚠️ EP${NEXT_EP} upload had issues (exit $EXIT_CODE)" >> "$LOG"
    # Still mark as done to avoid retry loops — Discord notification will show what failed
    echo "$NEXT_EP" >> "${SCRIPT_DIR}/youtube_uploaded.txt"
fi
