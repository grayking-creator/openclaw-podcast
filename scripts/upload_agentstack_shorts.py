#!/usr/bin/env python3
"""AgentStack Daily Shorts — scheduled uploader.

Uploads rendered short MP4s from content_staging/shorts/ to the EN YouTube
channel on a 3-per-day cadence (08:00, 14:00, 20:00 ET).

No manual review gate. Liminal and IronVane use the separate crossfire-series
shorts_upload.py. This script is AgentStack Daily / OpenClaw Daily only.

State file: content_staging/shorts/upload_state.json
  { "uploaded": ["episode_058/clip_01.mp4", ...] }

Run via cron: called by youtube_cron_runner.sh or directly.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
except Exception:
    ET = None

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
STAGING_ROOT = PODCAST_DIR / "content_staging" / "shorts"
STATE_PATH = STAGING_ROOT / "upload_state.json"
BUILD_LOG_CHANNEL_ID = "1485243812442804327"

# EN channel only for AgentStack Daily shorts
TOKEN_PATH = SCRIPTS_DIR / "youtube_token_en.json"
EXPECTED_CHANNEL = {
    "id": "UCT6t2lhEGVmPnm7Cxkrv3dw",
    "title": "AgentStack Daily",
    "title_aliases": ["OpenClaw Daily"],
    "handle": "@AgentStackDaily",
}

# 3 slots per day (ET)
UPLOAD_SLOTS_ET = ["08:00", "14:00", "20:00"]

# Episodes in order, oldest first
EPISODE_ORDER = [58, 59, 60, 61, 62, 63, 64]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_env_key(name: str) -> str:
    env_file = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_file):
        for line in open(env_file):
            if name in line and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get(name, "")


def discord_build_log(msg: str) -> None:
    try:
        token = _load_env_key("DISCORD_BOT_TOKEN")
        if not token:
            return
        payload = json.dumps({"content": msg}).encode()
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{BUILD_LOG_CHANNEL_ID}/messages",
            data=payload,
            headers={
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json",
                "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=8)
    except Exception:
        pass


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    return {"uploaded": [], "scheduled": {}}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")


def now_et() -> datetime:
    if ET:
        return datetime.now(ET)
    # fallback: UTC-4
    return datetime.now(timezone(timedelta(hours=-4)))


def next_slot_datetimes(from_dt: datetime, count: int) -> list[datetime]:
    """Return the next `count` upload slot datetimes at or after from_dt."""
    slots = []
    day = from_dt.date()
    while len(slots) < count:
        for slot_str in UPLOAD_SLOTS_ET:
            h, m = map(int, slot_str.split(":"))
            if ET:
                slot_dt = datetime(day.year, day.month, day.day, h, m, tzinfo=ET)
            else:
                slot_dt = datetime(
                    day.year, day.month, day.day, h, m,
                    tzinfo=timezone(timedelta(hours=-4))
                )
            if slot_dt > from_dt:
                slots.append(slot_dt)
                if len(slots) >= count:
                    break
        day = day + timedelta(days=1)
    return slots


def get_episode_title(ep_num: int) -> str:
    ep_str = f"{ep_num:03d}"
    feed_path = PODCAST_DIR / "feed.xml"
    if feed_path.exists():
        content = feed_path.read_text()
        items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
        for item in items:
            ep_match = re.search(r"<itunes:episode>(\d+)</itunes:episode>", item)
            if ep_match and int(ep_match.group(1)) == ep_num:
                title_match = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", item)
                if title_match:
                    return title_match.group(1).strip()
    return f"AgentStack Daily EP{ep_str}"


def clip_label(ep_num: int, clip_idx: int) -> str:
    """Short-form upload title: hook line from selected_clips.json or fallback."""
    ep_str = f"{ep_num:03d}"
    manifest = STAGING_ROOT / f"episode_{ep_str}" / f"episode_{ep_str}_work" / "selected_clips.json"
    if manifest.exists():
        try:
            clips = json.loads(manifest.read_text())
            if clip_idx - 1 < len(clips):
                text = clips[clip_idx - 1].get("text", "")
                fragment = re.split(r"(?<=[.!?])\s+", text)[0].strip()
                label = fragment[:80].rstrip(" ,;:") or get_episode_title(ep_num)
                return label
        except Exception:
            pass
    return get_episode_title(ep_num)


def build_short_title(ep_num: int, clip_idx: int) -> str:
    ep_str = f"{ep_num:03d}"
    label = clip_label(ep_num, clip_idx)
    # YouTube Shorts needs #Shorts in title or description; put it last
    title = f"EP{ep_str} | {label} #Shorts"
    return title[:100]


def build_short_description(ep_num: int) -> str:
    ep_str = f"{ep_num:03d}"
    title = get_episode_title(ep_num)
    show_notes_url = f"https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"
    return (
        f"EP{ep_str} | {title}\n\n"
        f"Full episode: {show_notes_url}\n"
        f"Listen everywhere: https://tobyonfitnesstech.com/podcasts/\n\n"
        f"#AgentStackDaily #AIPodcast #Shorts"
    )


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

def upload_short(clip_path: Path, title: str, description: str) -> str:
    """Upload a short MP4 to EN channel. Returns video ID."""
    with open(TOKEN_PATH) as f:
        creds = Credentials.from_authorized_user_info(json.load(f))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())

    yt = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["AgentStack Daily", "AI podcast", "AI news", "Shorts"],
            "categoryId": "28",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(str(clip_path), mimetype="video/mp4", resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            print(f"    {int(status.progress() * 100)}%...")

    return response["id"]


# ---------------------------------------------------------------------------
# Queue builder
# ---------------------------------------------------------------------------

def build_upload_queue(state: dict) -> list[dict]:
    """Return ordered list of clips not yet uploaded, with assigned slots."""
    uploaded = set(state.get("uploaded", []))
    pending = []
    for ep_num in EPISODE_ORDER:
        ep_str = f"{ep_num:03d}"
        ep_dir = STAGING_ROOT / f"episode_{ep_str}"
        for clip_idx in (1, 2):
            clip_path = ep_dir / f"clip_{clip_idx:02d}.mp4"
            key = f"episode_{ep_str}/clip_{clip_idx:02d}.mp4"
            if clip_path.exists() and key not in uploaded:
                pending.append({
                    "key": key,
                    "ep_num": ep_num,
                    "clip_idx": clip_idx,
                    "clip_path": str(clip_path),
                })

    # Assign slot times starting now
    if not pending:
        return []

    slots = next_slot_datetimes(now_et(), len(pending))
    for item, slot in zip(pending, slots):
        item["scheduled_at"] = slot.isoformat()

    return pending


# ---------------------------------------------------------------------------
# Cron mode: upload whatever is due now
# ---------------------------------------------------------------------------

def run_cron(state: dict) -> int:
    queue = build_upload_queue(state)
    if not queue:
        print("No pending shorts to upload.")
        return 0

    now = now_et()
    due = [item for item in queue if datetime.fromisoformat(item["scheduled_at"]) <= now]

    if not due:
        next_item = queue[0]
        print(f"Next short scheduled at {next_item['scheduled_at']} — not due yet.")
        return 0

    errors = []
    for item in due:
        ep_num = item["ep_num"]
        clip_idx = item["clip_idx"]
        clip_path = Path(item["clip_path"])
        ep_str = f"{ep_num:03d}"

        title = build_short_title(ep_num, clip_idx)
        description = build_short_description(ep_num)

        print(f"Uploading EP{ep_str} clip {clip_idx}: {title}")
        try:
            vid_id = upload_short(clip_path, title, description)
            url = f"https://www.youtube.com/shorts/{vid_id}"
            print(f"  ✅ {url}")
            state.setdefault("uploaded", []).append(item["key"])
            state.setdefault("urls", {})[item["key"]] = url
            save_state(state)
            discord_build_log(f"📱 [AgentStack Shorts] EP{ep_str} clip {clip_idx} uploaded: {url}")
        except Exception as exc:
            msg = f"❌ [AgentStack Shorts] EP{ep_str} clip {clip_idx} upload failed: {exc}"
            print(msg)
            discord_build_log(msg)
            errors.append(msg)

        time.sleep(3)

    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Status mode: show what's built, uploaded, and what's next
# ---------------------------------------------------------------------------

def run_status(state: dict) -> None:
    queue = build_upload_queue(state)
    uploaded = state.get("uploaded", [])
    urls = state.get("urls", {})

    print(f"\n=== AgentStack Daily Shorts Status ===")
    print(f"Uploaded: {len(uploaded)}")
    for key in uploaded:
        url = urls.get(key, "")
        print(f"  ✅ {key}  {url}")

    print(f"\nPending ({len(queue)}):")
    for item in queue:
        clip_exists = Path(item["clip_path"]).exists()
        status = "BUILT" if clip_exists else "NOT BUILT"
        print(f"  [{status}] EP{item['ep_num']:03d} clip {item['clip_idx']} → {item['scheduled_at']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["cron", "status"], default="cron")
    args = parser.parse_args()

    state = load_state()

    if args.mode == "status":
        run_status(state)
        return 0

    return run_cron(state)


if __name__ == "__main__":
    sys.exit(main())
