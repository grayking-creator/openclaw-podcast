#!/bin/bash
# YouTube scheduled upload runner
# Handles long-form uploads only. Shorts are managed separately.
# Run via cron every 15 minutes (or at least often enough to catch 08/12/16/20 ET slots).

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCHEDULE="${SCRIPT_DIR}/youtube_upload_schedule.json"
LOG="/tmp/youtube_upload_cron.log"
VENV_PYTHON="/opt/homebrew/bin/python3"
export PATH="/opt/homebrew/bin:$PATH"

# Prevent parallel runs
LOCKFILE="/tmp/youtube_upload.lock"
if [ -f "$LOCKFILE" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCKFILE" 2>/dev/null || echo 0) ))
    if [ "$LOCK_AGE" -lt 1800 ]; then
        echo "[$(date)] Another upload is already running (lock age: ${LOCK_AGE}s) — skipping" >> "$LOG"
        exit 0
    fi
    echo "[$(date)] Stale lock found (${LOCK_AGE}s old) — removing" >> "$LOG"
fi
touch "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

echo "[$(date)] YouTube cron runner started" >> "$LOG"

# Sync youtube_uploaded.txt with actual YouTube channel state before picking next ep
echo "[$(date)] Syncing uploaded state from YouTube..." >> "$LOG"
$VENV_PYTHON "${SCRIPT_DIR}/sync_uploaded_from_youtube.py" >> "$LOG" 2>&1

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

LONG_EXIT_CODE=0

if [ "$NEXT_EP" = "NONE" ] || [ -z "$NEXT_EP" ]; then
    echo "[$(date)] No long-form episodes due for upload" >> "$LOG"
else
    echo "[$(date)] Uploading EP${NEXT_EP}..." >> "$LOG"

    cd "$SCRIPT_DIR"
    $VENV_PYTHON youtube_scheduled_upload.py "$NEXT_EP" >> "$LOG" 2>&1
    LONG_EXIT_CODE=$?
fi

TELEGRAM_TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.openclaw/.env 2>/dev/null | cut -d= -f2 | tr -d '"')
TELEGRAM_CHAT="8319992332"

if [ "$NEXT_EP" != "NONE" ] && [ -n "$NEXT_EP" ]; then
    if [ $LONG_EXIT_CODE -eq 0 ]; then
        echo "$NEXT_EP" >> "${SCRIPT_DIR}/youtube_uploaded.txt"
        echo "[$(date)] ✅ EP${NEXT_EP} upload complete" >> "$LOG"
    else
        echo "[$(date)] ❌ EP${NEXT_EP} upload FAILED (exit $LONG_EXIT_CODE)" >> "$LOG"
        # Alert Toby via Telegram
        FAIL_MSG="❌ YouTube EP${NEXT_EP} upload failed. Check /tmp/youtube_upload_cron.log"
        if [ -n "$TELEGRAM_TOKEN" ]; then
            curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
                -d "chat_id=${TELEGRAM_CHAT}&text=${FAIL_MSG}" > /dev/null 2>&1
        fi
        # Do NOT mark as done — retry on next cron run
        echo "[$(date)] Will retry EP${NEXT_EP} on next run" >> "$LOG"
    fi
fi

exit $LONG_EXIT_CODE
