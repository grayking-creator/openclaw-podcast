#!/usr/bin/env python3
"""AgentStack Daily Shorts — scheduled uploader.

Uploads rendered short MP4s from content_staging/shorts/ to the AgentStack
Daily / OpenClaw Daily YouTube channels on a 3-per-day follow-up cadence
(11:00, 16:00, and 23:00 ET).

No manual review gate. Liminal and IronVane use the separate crossfire-series
shorts_upload.py. This script is AgentStack Daily / OpenClaw Daily only.

State file: content_staging/shorts/upload_state.json
  { "uploaded": ["episode_058/clip_01_en.mp4", ...] }

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

# AgentStack/OpenClaw Daily shorts auto-upload covers EN plus translated
# channels. The day-of-publish catch-up can ship two EN clips; following days
# continue the full multilingual backlog at three uploads per day.
CHANNELS = ["en", "es", "de", "pt", "hi"]

# 3 slots per day (ET) after the day-of-publish catch-up.
UPLOAD_SLOTS_ET = ["11:00", "16:00", "23:00"]

# Discovery floor for the rendered AgentStack Daily backlog. Newer episodes are
# picked up from content_staging/shorts/episode_NNN automatically.
MIN_EPISODE = 58
UPLOAD_SLOT_CATCHUP_WINDOW = timedelta(hours=2)


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


def slot_datetime(day, slot_str: str) -> datetime:
    h, m = map(int, slot_str.split(":"))
    if ET:
        return datetime(day.year, day.month, day.day, h, m, tzinfo=ET)
    return datetime(
        day.year, day.month, day.day, h, m,
        tzinfo=timezone(timedelta(hours=-4)),
    )


def next_slot_datetimes(from_dt: datetime, count: int) -> list[datetime]:
    """Return the next `count` upload slot datetimes at or after from_dt."""
    slots = []
    day = from_dt.date()
    while len(slots) < count:
        for slot_str in UPLOAD_SLOTS_ET:
            slot_dt = slot_datetime(day, slot_str)
            if slot_dt > from_dt:
                slots.append(slot_dt)
                if len(slots) >= count:
                    break
        day = day + timedelta(days=1)
    return slots


def latest_slot_at_or_before(from_dt: datetime) -> datetime:
    day = from_dt.date()
    for _ in range(2):
        day_slots = [slot_datetime(day, slot_str) for slot_str in UPLOAD_SLOTS_ET]
        candidates = [slot_dt for slot_dt in day_slots if slot_dt <= from_dt]
        if candidates:
            return candidates[-1]
        day = day - timedelta(days=1)
    return next_slot_datetimes(from_dt - timedelta(days=1), 1)[0]


def first_schedule_slot(from_dt: datetime) -> datetime:
    latest = latest_slot_at_or_before(from_dt)
    if from_dt - latest <= UPLOAD_SLOT_CATCHUP_WINDOW and latest.date() == from_dt.date():
        return latest
    return next_slot_datetimes(from_dt, 1)[0]


def slot_sequence(first_slot: datetime, count: int) -> list[datetime]:
    if count <= 0:
        return []
    return [first_slot] + next_slot_datetimes(first_slot, count - 1)


def next_free_slot_after(from_dt: datetime) -> datetime:
    return next_slot_datetimes(from_dt, 1)[0]


def batch_key(ep_num: int, clip_idx: int) -> str:
    return f"episode_{ep_num:03d}/clip_{clip_idx:02d}"


def clip_key(ep_num: int, clip_idx: int, lang: str) -> str:
    return f"{batch_key(ep_num, clip_idx)}_{lang}.mp4"


def clip_path_for(ep_num: int, clip_idx: int, lang: str) -> Path:
    ep_str = f"{ep_num:03d}"
    ep_dir = STAGING_ROOT / f"episode_{ep_str}"
    if lang == "en":
        return ep_dir / f"clip_{clip_idx:02d}.mp4"
    return ep_dir / "translations" / lang / "rollout_render" / f"clip_{clip_idx:02d}.mp4"


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


def released_episode_numbers() -> set[int]:
    feed_path = PODCAST_DIR / "feed.xml"
    if not feed_path.exists():
        return set()
    episodes = set()
    for match in re.finditer(r"<itunes:episode>(\d+)</itunes:episode>", feed_path.read_text()):
        episodes.add(int(match.group(1)))
    return episodes


def discover_episode_order() -> list[int]:
    released = released_episode_numbers()
    episodes = []
    for ep_dir in STAGING_ROOT.glob("episode_[0-9][0-9][0-9]"):
        match = re.fullmatch(r"episode_(\d{3})", ep_dir.name)
        if not match:
            continue
        ep_num = int(match.group(1))
        if ep_num < MIN_EPISODE or ep_num not in released:
            continue
        if any((ep_dir / f"clip_{idx:02d}.mp4").exists() for idx in (1, 2)):
            episodes.append(ep_num)
            continue
        for lang in CHANNELS:
            if any((ep_dir / "translations" / lang / "rollout_render" / f"clip_{idx:02d}.mp4").exists() for idx in (1, 2)):
                episodes.append(ep_num)
                break
    return sorted(set(episodes))


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

def upload_short(clip_path: Path, title: str, description: str, lang: str) -> str:
    """Upload a short MP4 to the specified language channel. Returns video ID."""
    token_path = SCRIPTS_DIR / f"youtube_token_{lang}.json"
    with open(token_path) as f:
        creds = Credentials.from_authorized_user_info(json.load(f))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as f:
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
def load_metadata_for_clip(ep_num: int, clip_idx: int, lang: str) -> tuple[str, str]:
    """Load localized title and description if available, else fall back to English."""
    ep_str = f"{ep_num:03d}"
    if lang == "en":
        title = build_short_title(ep_num, clip_idx)
        description = build_short_description(ep_num)
        return title, description

    metadata_path = STAGING_ROOT / f"episode_{ep_str}" / "translations" / lang / "rollout_render" / f"clip_{clip_idx:02d}_metadata.json"
    if metadata_path.exists():
        try:
            meta = json.loads(metadata_path.read_text())
            title = meta.get("title", "").strip()
            desc = meta.get("description", "").strip()
            if title:
                if "#Shorts" not in title and "#shorts" not in title:
                    title = f"{title} #Shorts"
                title = title[:100]
                if not desc:
                    desc = build_short_description(ep_num)
                return title, desc
        except Exception:
            pass

    # Fallback to English
    title = build_short_title(ep_num, clip_idx)
    description = build_short_description(ep_num)
    return title, description


def collect_pending_batches(state: dict) -> list[dict]:
    """Return ordered episode+clip batches that still have uploads pending."""
    uploaded = set(state.get("uploaded", []))
    batches = []
    for ep_num in discover_episode_order():
        ep_str = f"{ep_num:03d}"
        for clip_idx in (1, 2):
            items = []
            missing_langs = []
            for lang in CHANNELS:
                clip_path = clip_path_for(ep_num, clip_idx, lang)
                key = clip_key(ep_num, clip_idx, lang)
                if not clip_path.exists():
                    missing_langs.append(lang)
                    continue
                if key not in uploaded:
                    items.append({
                        "key": key,
                        "ep_num": ep_num,
                        "clip_idx": clip_idx,
                        "lang": lang,
                        "clip_path": str(clip_path),
                    })
            if items:
                batches.append({
                    "batch_key": batch_key(ep_num, clip_idx),
                    "ep_num": ep_num,
                    "ep_str": ep_str,
                    "clip_idx": clip_idx,
                    "items": items,
                    "missing_langs": missing_langs,
                    "complete": not missing_langs,
                })
    return batches


def build_upload_queue(state: dict, persist_schedule: bool = False) -> list[dict]:
    """Return ordered pending batches with stable, persisted schedule slots."""
    batches = collect_pending_batches(state)
    if not batches:
        return []

    by_key = {batch["batch_key"]: batch for batch in batches}
    schedule = dict(state.get("scheduled_batches", {}))
    schedule = {
        key: when
        for key, when in schedule.items()
        if key in by_key
    }

    now = now_et()
    seed_slot = first_schedule_slot(now)
    existing_slots = sorted(datetime.fromisoformat(when) for when in schedule.values())
    cursor = max(existing_slots) if existing_slots else seed_slot

    # Keep one global cadence across episode+clip batches. Existing explicit
    # batch slots are preserved so one-off recovery slots do not get rewritten
    # on the next cron run; only newly discovered batches get appended.
    for batch in batches:
        key = batch["batch_key"]
        if key in schedule:
            continue
        if not existing_slots and cursor == seed_slot:
            slot = cursor
        else:
            slot = next_free_slot_after(cursor)
        schedule[key] = slot.isoformat()
        cursor = slot
        existing_slots.append(slot)

    if persist_schedule:
        state["scheduled_batches"] = schedule
        state["scheduled"] = {
            item["key"]: schedule[batch["batch_key"]]
            for batch in batches
            for item in batch["items"]
        }
        save_state(state)

    all_pending = []
    for batch in batches:
        scheduled_at = schedule.get(batch["batch_key"])
        if scheduled_at:
            batch = dict(batch)
            batch["items"] = [dict(item) for item in batch["items"]]
            batch["scheduled_at"] = scheduled_at
            for item in batch["items"]:
                item["scheduled_at"] = scheduled_at
            all_pending.append(batch)

    # Sort all pending by scheduled_at so chronological order is maintained
    all_pending.sort(key=lambda x: x["scheduled_at"])
    return all_pending


def note_missing_batch_once(state: dict, batch: dict) -> None:
    missing = batch.get("missing_langs", [])
    if not missing:
        return
    signature = ",".join(missing)
    alerts = state.setdefault("missing_render_alerts", {})
    if alerts.get(batch["batch_key"]) == signature:
        return
    alerts[batch["batch_key"]] = signature
    save_state(state)
    msg = (
        f"❌ [AgentStack Shorts] EP{batch['ep_str']} clip {batch['clip_idx']} "
        f"held: missing rendered language(s): {signature}"
    )
    print(msg)
    discord_build_log(msg)


# ---------------------------------------------------------------------------
# Cron mode: upload whatever is due now
# ---------------------------------------------------------------------------

def run_cron(state: dict, catch_up_now: bool = False) -> int:
    queue = build_upload_queue(state, persist_schedule=True)
    if not queue:
        print("No pending shorts to upload.")
        return 0

    now = now_et()
    due = [batch for batch in queue if datetime.fromisoformat(batch["scheduled_at"]) <= now]
    if catch_up_now and not due:
        due = [queue[0]]
        due[0]["scheduled_at"] = now.isoformat()

    if not due:
        next_batch = queue[0]
        langs = ",".join(item["lang"] for item in next_batch["items"])
        print(
            f"Next short batch scheduled at {next_batch['scheduled_at']} — "
            f"EP{next_batch['ep_str']} clip {next_batch['clip_idx']} ({langs}) not due yet."
        )
        return 0

    errors = []
    for batch in due:
        if batch.get("missing_langs"):
            note_missing_batch_once(state, batch)
            errors.append(f"{batch['batch_key']} missing {','.join(batch['missing_langs'])}")
            continue

        uploaded_urls = []
        for item in batch["items"]:
            ep_num = item["ep_num"]
            clip_idx = item["clip_idx"]
            clip_path = Path(item["clip_path"])
            lang = item["lang"]
            ep_str = f"{ep_num:03d}"

            title, description = load_metadata_for_clip(ep_num, clip_idx, lang)

            print(f"Uploading EP{ep_str} clip {clip_idx} ({lang}): {title}")
            try:
                vid_id = upload_short(clip_path, title, description, lang)
                url = f"https://www.youtube.com/shorts/{vid_id}"
                print(f"  ✅ {url}")
                state.setdefault("uploaded", []).append(item["key"])
                state.setdefault("urls", {})[item["key"]] = url
                save_state(state)
                uploaded_urls.append((lang, url))
            except Exception as exc:
                msg = f"❌ [AgentStack Shorts] EP{ep_str} clip {clip_idx} ({lang}) upload failed: {exc}"
                print(msg)
                discord_build_log(msg)
                errors.append(msg)

            time.sleep(3)

        if uploaded_urls:
            lang_list = ", ".join(lang for lang, _ in uploaded_urls)
            url_lines = "\n".join(f"- {lang}: {url}" for lang, url in uploaded_urls)
            discord_build_log(
                f"📱 [AgentStack Shorts] EP{batch['ep_str']} clip {batch['clip_idx']} "
                f"uploaded across: {lang_list}\n{url_lines}"
            )

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

    pending_items = sum(len(batch["items"]) for batch in queue)
    print(f"\nPending batches: {len(queue)} ({pending_items} videos)")
    for batch in queue:
        langs = ",".join(item["lang"] for item in batch["items"])
        missing = ",".join(batch.get("missing_langs", []))
        status = "BUILT" if not missing else f"HELD missing={missing}"
        print(
            f"  [{status}] EP{batch['ep_num']:03d} clip {batch['clip_idx']} "
            f"({langs}) → {batch['scheduled_at']}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["cron", "status"], default="cron")
    parser.add_argument("--catch-up-now", action="store_true", help="Upload the next pending batch immediately.")
    args = parser.parse_args()

    state = load_state()

    if args.mode == "status":
        run_status(state)
        return 0

    return run_cron(state, catch_up_now=args.catch_up_now)


if __name__ == "__main__":
    sys.exit(main())
