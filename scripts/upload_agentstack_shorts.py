#!/usr/bin/env python3
"""AgentStack Daily Shorts — scheduled uploader.

Uploads rendered short MP4s from content_staging/shorts/ to the AgentStack
Daily / OpenClaw Daily YouTube channels on a 3-per-day follow-up cadence
(08:00, 14:00, and 20:00 ET).

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
from validate_shorts_media import MediaValidationError, validate_media_file

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
STAGING_ROOT = PODCAST_DIR / "content_staging" / "shorts"
STATE_PATH = STAGING_ROOT / "upload_state.json"
YOUTUBE_CHANNEL_STATE_PATH = SCRIPTS_DIR / "youtube_channel_state.json"
RELATED_VIDEO_SCRIPT = SCRIPTS_DIR / "youtube_studio_set_related_video.py"
BUILD_LOG_CHANNEL_ID = "1485243812442804327"
BUILD_LOG_ERROR_CHANNEL_ID = "1524923755019636948"

# AgentStack/OpenClaw Daily shorts auto-upload covers EN plus translated
# channels. The day-of-publish catch-up can ship two EN clips; following days
# continue the full multilingual backlog at three uploads per day.
CHANNELS = ["en", "es", "de", "pt", "hi"]

# 3 slots per day (ET) after the day-of-publish catch-up.
UPLOAD_SLOTS_ET = ["08:00", "14:00", "20:00"]

# Discovery floor for the rendered AgentStack Daily backlog. Newer episodes are
# picked up from content_staging/shorts/episode_NNN automatically.
MIN_EPISODE = 58
UPLOAD_SLOT_CATCHUP_WINDOW = timedelta(hours=2)
SET_RELATED_VIDEOS = os.environ.get("AGENTSTACK_SHORTS_SET_RELATED", "1").strip().lower() not in {
    "0",
    "false",
    "no",
}
RELAUNCH_CHROME_FOR_STUDIO = os.environ.get(
    "YOUTUBE_STUDIO_RELAUNCH_CHROME", ""
).strip().lower() in {
    "1",
    "true",
    "yes",
}


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


def discord_build_log(msg: str) -> bool:
    try:
        helper_dir = Path.home() / ".openclaw/workspace/scripts/utils"
        if str(helper_dir) not in sys.path:
            sys.path.insert(0, str(helper_dir))
        from post_build_log import post_build_log as routed_post_build_log

        routed_post_build_log(msg)
        return True
    except Exception:
        pass
    try:
        token = _load_env_key("DISCORD_BOT_TOKEN")
        if not token:
            print("WARN: DISCORD_BOT_TOKEN missing; Build Log post skipped", file=sys.stderr)
            return False
        is_error = any(marker in msg for marker in ("❌", "⚠", "🛑", "🚨", "🔴", "[FAIL]", "[HOLD]"))
        channel = BUILD_LOG_ERROR_CHANNEL_ID if is_error else BUILD_LOG_CHANNEL_ID
        payload = json.dumps({"content": msg}).encode()
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{channel}/messages",
            data=payload,
            headers={
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json",
                "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status not in (200, 201):
                print(f"WARN: Discord Build Log post returned HTTP {resp.status}", file=sys.stderr)
                return False
        return True
    except Exception as exc:
        print(f"WARN: Discord Build Log post failed: {exc}", file=sys.stderr)
        return False


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


def video_id_from_url(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", url or "")
    return match.group(1) if match else ""


def youtube_client(lang: str):
    token_path = SCRIPTS_DIR / f"youtube_token_{lang}.json"
    with open(token_path) as f:
        creds = Credentials.from_authorized_user_info(json.load(f))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def fetch_video_title(lang: str, video_id: str) -> str:
    yt = youtube_client(lang)
    response = yt.videos().list(part="snippet", id=video_id).execute()
    items = response.get("items", [])
    if not items:
        raise RuntimeError(f"YouTube video not found: {video_id}")
    return items[0]["snippet"]["title"].strip()


def full_episode_video_id(ep_num: int, lang: str) -> str:
    if not YOUTUBE_CHANNEL_STATE_PATH.exists():
        return ""
    try:
        state = json.loads(YOUTUBE_CHANNEL_STATE_PATH.read_text())
    except Exception:
        return ""
    entry = state.get(f"{ep_num:03d}") or state.get(str(ep_num)) or {}
    return video_id_from_url(entry.get(f"{lang}_url", ""))


def validate_clip_path(path: Path) -> tuple[bool, str]:
    try:
        validate_media_file(path, require_video=True)
        return True, ""
    except MediaValidationError as exc:
        return False, str(exc)
    except Exception as exc:
        return False, f"media validation failed: {exc}"


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
    selected = load_selected_clip(ep_num, clip_idx)
    return title_from_clip_text(selected.get("text", ""), get_episode_title(ep_num))[:100]


def build_short_description(ep_num: int) -> str:
    title = get_episode_title(ep_num)
    show_notes_url = f"https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"
    return ensure_description_hashtags(
        f"{title}\n\n"
        f"Full episode: {show_notes_url}\n"
        f"Listen everywhere: https://tobyonfitnesstech.com/podcasts/"
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


def episode_has_rendered_en_package(ep_num: int) -> bool:
    for idx in (1, 2):
        clip_path = clip_path_for(ep_num, idx, "en")
        if not clip_path.exists():
            return False
        is_valid, _ = validate_clip_path(clip_path)
        if not is_valid:
            return False
    return True


def missing_render_episodes() -> list[int]:
    missing = []
    for ep_num in sorted(released_episode_numbers()):
        if ep_num < MIN_EPISODE:
            continue
        if not episode_has_rendered_en_package(ep_num):
            missing.append(ep_num)
    return missing


def alert_missing_renders_once(state: dict, missing: list[int]) -> None:
    if not missing:
        return
    signature = ",".join(f"{ep:03d}" for ep in missing)
    if state.get("last_missing_render_alert") == signature:
        return
    state["last_missing_render_alert"] = signature
    save_state(state)
    first = missing[0]
    last = missing[-1]
    if first == last:
        span = f"EP{first:03d}"
    else:
        span = f"EP{first:03d}-EP{last:03d}"
    msg = (
        f"❌ [AgentStack Shorts] No pending uploads because released {span} "
        "have no rendered shorts package. Build the missing shorts before the uploader can publish."
    )
    print(msg)
    discord_build_log(msg)


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

def upload_short(clip_path: Path, title: str, description: str, lang: str, tags: list[str]) -> str:
    """Upload a short MP4 to the specified language channel. Returns video ID."""
    yt = youtube_client(lang)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags[:15],
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


def prepare_related_video_task(state: dict, item: dict, short_video_id: str) -> tuple[bool, str]:
    """Record the Studio related-video task for a freshly uploaded short."""
    if not SET_RELATED_VIDEOS:
        return True, ""
    ep_num = item["ep_num"]
    lang = item["lang"]
    related_id = full_episode_video_id(ep_num, lang)
    if not related_id:
        return False, f"missing full-episode YouTube ID for EP{ep_num:03d} ({lang})"
    try:
        related_title = fetch_video_title(lang, related_id)
    except Exception as exc:
        return False, f"could not fetch full-episode title for EP{ep_num:03d} ({lang}): {exc}"

    tasks = state.setdefault("related_video_tasks", {})
    existing = tasks.get(item["key"], {})
    tasks[item["key"]] = {
        "status": "pending",
        "short_id": short_video_id,
        "related_id": related_id,
        "related_title": related_title,
        "lang": lang,
        "ep_num": ep_num,
        "clip_idx": item["clip_idx"],
        "attempts": int(existing.get("attempts", 0)),
        "last_error": "",
    }
    save_state(state)
    return True, ""


def _related_success_ids(output: str) -> set[str]:
    success_ids = set()
    for line in output.splitlines():
        match = re.match(r"([A-Za-z0-9_-]{11}): (?:set related video|already set) ->", line.strip())
        if match:
            success_ids.add(match.group(1))
    return success_ids


def process_related_video_tasks(state: dict, keys: list[str]) -> list[str]:
    """Set queued Shorts related-video links through YouTube Studio."""
    if not SET_RELATED_VIDEOS:
        return []
    if not RELATED_VIDEO_SCRIPT.exists():
        return [f"related video helper missing: {RELATED_VIDEO_SCRIPT}"]

    tasks = state.get("related_video_tasks", {})
    pending = []
    errors = []
    for key in keys:
        task = tasks.get(key)
        if not task or task.get("status") == "done":
            continue
        if not all(task.get(field) for field in ("short_id", "related_id", "related_title")):
            task["status"] = "failed"
            task["attempts"] = int(task.get("attempts", 0)) + 1
            task["last_attempt_at"] = now_et().isoformat()
            task["last_error"] = "missing short_id, related_id, or related_title"
            errors.append(f"{key} related-video task is incomplete")
            continue
        pending.append((key, task))

    if not pending:
        if errors:
            save_state(state)
        return errors

    cmd = [sys.executable, str(RELATED_VIDEO_SCRIPT)]
    if RELAUNCH_CHROME_FOR_STUDIO:
        cmd.append("--relaunch-chrome")
    for _, task in pending:
        cmd.extend([
            "--pair",
            f"{task['short_id']}:{task['related_id']}:{task['related_title']}",
        ])

    print(f"Setting related full-episode video for {len(pending)} short(s) via YouTube Studio...")
    started_at = now_et().isoformat()
    try:
        result = subprocess.run(
            cmd,
            cwd=str(PODCAST_DIR),
            capture_output=True,
            text=True,
            timeout=max(300, 120 * len(pending)),
        )
    except Exception as exc:
        for _, task in pending:
            task["status"] = "failed"
            task["attempts"] = int(task.get("attempts", 0)) + 1
            task["last_error"] = str(exc)
            task["last_attempt_at"] = started_at
        save_state(state)
        return [f"related video Studio automation failed to run: {exc}"]

    output = "\n".join(part for part in (result.stdout, result.stderr) if part)
    success_ids = _related_success_ids(output)

    for key, task in pending:
        task["attempts"] = int(task.get("attempts", 0)) + 1
        task["last_attempt_at"] = started_at
        if result.returncode == 0 or task.get("short_id") in success_ids:
            task["status"] = "done"
            task["last_error"] = ""
            task["set_at"] = now_et().isoformat()
            continue
        task["status"] = "failed"
        tail = "\n".join(output.splitlines()[-10:]).strip()
        task["last_error"] = tail or f"Studio helper exited {result.returncode}"
        errors.append(
            f"related video not set for EP{task.get('ep_num'):03d} "
            f"clip {task.get('clip_idx')} ({task.get('lang')}): {task['last_error']}"
        )

    save_state(state)
    return errors


def pending_related_video_task_keys(state: dict) -> list[str]:
    tasks = state.get("related_video_tasks", {})
    return [
        key
        for key, task in tasks.items()
        if task and task.get("status") != "done"
    ]


# ---------------------------------------------------------------------------
# Queue builder
# ---------------------------------------------------------------------------
BAD_TITLE_PREFIXES = (
    "i'm nova",
    "i'm alloy",
    "this is agentstack",
    "this is agentstack daily",
    "today,",
    "today we",
    "you'll hear",
    "in this episode",
    "story one",
    "story two",
    "the order is deliberate",
    "for the project radar tools",
)


def clean_short_title(raw: str, max_len: int = 72) -> str:
    title = re.sub(r"\[(?:NOVA|ALLOY)\]:", "", raw or "", flags=re.IGNORECASE)
    title = title.replace("AgentStackDaily", "AgentStack Daily")
    title = re.sub(r"#\S+", "", title)
    title = re.sub(r"^EP\d{2,3}\s*[|:-]\s*", "", title.strip(), flags=re.IGNORECASE)
    title = title.replace('"', "").replace("“", "").replace("”", "")
    title = re.sub(r"\s+", " ", title).strip(" -:;,.")
    if len(title) > max_len:
        title = title[:max_len].rsplit(" ", 1)[0].strip(" -:;,")
    if title and title[0].islower():
        title = title[0].upper() + title[1:]
    return title


def title_is_weak(title: str) -> bool:
    lowered = title.lower().strip()
    if len(title) < 18:
        return True
    if any(lowered.startswith(prefix) for prefix in BAD_TITLE_PREFIXES):
        return True
    if "#short" in lowered or re.search(r"\bep\d{2,3}\b", lowered):
        return True
    return False


def load_selected_clip(ep_num: int, clip_idx: int) -> dict:
    ep_str = f"{ep_num:03d}"
    manifest = STAGING_ROOT / f"episode_{ep_str}" / f"episode_{ep_str}_work" / "selected_clips.json"
    if not manifest.exists():
        return {}
    try:
        clips = json.loads(manifest.read_text())
    except Exception:
        return {}
    if clip_idx - 1 >= len(clips):
        return {}
    return clips[clip_idx - 1] if isinstance(clips[clip_idx - 1], dict) else {}


def title_from_clip_text(text: str, fallback: str) -> str:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text or "") if part.strip()]
    for sentence in sentences[:5]:
        title = clean_short_title(sentence)
        if title and not title_is_weak(title):
            return title
    title = clean_short_title(fallback)
    if title and not title_is_weak(title):
        return title
    return "Why This AI Agent Stack Matters"


def metadata_paths_for_clip(ep_num: int, clip_idx: int, lang: str) -> list[Path]:
    ep_str = f"{ep_num:03d}"
    ep_dir = STAGING_ROOT / f"episode_{ep_str}"
    if lang == "en":
        return [
            ep_dir / f"clip_{clip_idx:02d}_metadata.json",
            ep_dir / f"clip_{clip_idx}_metadata.json",
        ]
    return [
        ep_dir / "translations" / lang / "rollout_render" / f"clip_{clip_idx:02d}_metadata.json",
    ]


def flatten_metadata_tags(meta: dict) -> list[str]:
    tags = []
    groups = meta.get("tag_groups", {})
    if isinstance(groups, dict):
        for key in ("post_specific", "niche_specific", "broad"):
            for item in groups.get(key, []) or []:
                tag = str(item).strip().lstrip("#")
                if tag and tag not in tags:
                    tags.append(tag)
    for item in meta.get("tags", []) or []:
        tag = str(item).strip().lstrip("#")
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def default_short_tags(ep_num: int, title: str = "") -> list[str]:
    tags = [
        "AgentStack Daily",
        "AI agents",
        "coding agents",
        "developer tools",
        "AI news",
        "software development",
        "Shorts",
        f"episode {ep_num}",
        f"ep{ep_num:03d}",
    ]
    lower = title.lower()
    topic_tags = [
        ("codex", "Codex"),
        ("claude", "Claude Code"),
        ("hermes", "Hermes Agent"),
        ("mcp", "MCP"),
        ("local", "local AI"),
        ("memory", "agent memory"),
        ("eval", "AI evaluations"),
    ]
    for needle, tag in topic_tags:
        if needle in lower and tag not in tags:
            tags.append(tag)
    return tags


def ensure_description_hashtags(description: str) -> str:
    desc = (description or "").strip()
    if "#Shorts" not in desc and "#shorts" not in desc:
        desc = f"{desc.rstrip()}\n\n#AgentStackDaily #AIAgents #Shorts".strip()
    return desc


def build_fallback_short_description(ep_num: int, title: str, clip_text: str) -> str:
    show_notes_url = f"https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/"
    snippet = re.sub(r"\s+", " ", clip_text or "").strip()
    if len(snippet) > 220:
        snippet = snippet[:220].rsplit(" ", 1)[0].rstrip(" ,;:.") + "."
    lead = title if title else get_episode_title(ep_num)
    if snippet and snippet.lower() != lead.lower():
        lead = f"{lead}\n\n{snippet}"
    return ensure_description_hashtags(
        f"{lead}\n\nFull episode: {show_notes_url}\nListen everywhere: https://tobyonfitnesstech.com/podcasts/"
    )


def load_metadata_for_clip(ep_num: int, clip_idx: int, lang: str) -> tuple[str, str, list[str]]:
    """Load localized title and description if available, else fall back to English."""
    for metadata_path in metadata_paths_for_clip(ep_num, clip_idx, lang):
        if not metadata_path.exists():
            continue
        try:
            meta = json.loads(metadata_path.read_text())
            title = clean_short_title(str(meta.get("title", "")), max_len=72)
            if title and not title_is_weak(title):
                desc = ensure_description_hashtags(str(meta.get("description", "")).strip())
                if not desc:
                    selected = load_selected_clip(ep_num, clip_idx)
                    desc = build_fallback_short_description(ep_num, title, selected.get("text", ""))
                tags = flatten_metadata_tags(meta) or default_short_tags(ep_num, title)
                return title[:100], desc, tags
        except Exception:
            pass

    # Fallback to English
    selected = load_selected_clip(ep_num, clip_idx)
    title = title_from_clip_text(selected.get("text", ""), get_episode_title(ep_num))
    description = build_fallback_short_description(ep_num, title, selected.get("text", ""))
    return title[:100], description, default_short_tags(ep_num, title)


def collect_pending_batches(state: dict) -> list[dict]:
    """Return ordered episode+clip batches that still have uploads pending."""
    uploaded = set(state.get("uploaded", []))
    batches = []
    for ep_num in discover_episode_order():
        ep_str = f"{ep_num:03d}"
        for clip_idx in (1, 2):
            items = []
            missing_langs = []
            invalid_langs = []
            invalid_reasons = {}
            for lang in CHANNELS:
                clip_path = clip_path_for(ep_num, clip_idx, lang)
                key = clip_key(ep_num, clip_idx, lang)
                if key in uploaded:
                    continue
                if not clip_path.exists():
                    missing_langs.append(lang)
                    continue
                is_valid, reason = validate_clip_path(clip_path)
                if not is_valid:
                    invalid_langs.append(lang)
                    invalid_reasons[lang] = reason
                    continue
                items.append({
                    "key": key,
                    "ep_num": ep_num,
                    "clip_idx": clip_idx,
                    "lang": lang,
                    "clip_path": str(clip_path),
                })
            if items or missing_langs or invalid_langs:
                batches.append({
                    "batch_key": batch_key(ep_num, clip_idx),
                    "ep_num": ep_num,
                    "ep_str": ep_str,
                    "clip_idx": clip_idx,
                    "items": items,
                    "missing_langs": missing_langs,
                    "invalid_langs": invalid_langs,
                    "invalid_reasons": invalid_reasons,
                    "complete": not missing_langs and not invalid_langs,
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
    invalid = batch.get("invalid_langs", [])
    if not missing and not invalid:
        return
    signature = f"missing={','.join(missing)};invalid={','.join(invalid)}"
    alerts = state.setdefault("missing_render_alerts", {})
    if alerts.get(batch["batch_key"]) == signature:
        return
    alerts[batch["batch_key"]] = signature
    save_state(state)
    problems = []
    if missing:
        problems.append(f"missing rendered language(s): {','.join(missing)}")
    if invalid:
        problems.append(f"invalid rendered language(s): {','.join(invalid)}")
    msg = (
        f"❌ [AgentStack Shorts] EP{batch['ep_str']} clip {batch['clip_idx']} "
        f"held: {'; '.join(problems)}"
    )
    print(msg)
    discord_build_log(msg)


# ---------------------------------------------------------------------------
# Cron mode: upload whatever is due now
# ---------------------------------------------------------------------------

def run_cron(state: dict, catch_up_now: bool = False) -> int:
    queue = build_upload_queue(state, persist_schedule=True)
    if not queue:
        missing = missing_render_episodes()
        if missing:
            alert_missing_renders_once(state, missing)
            return 1
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

    if len(due) > 1:
        print(
            f"{len(due)} short batches are overdue; processing oldest only "
            "to preserve the three-per-day cadence."
        )
        due = due[:1]

    errors = []
    for batch in due:
        if batch.get("missing_langs") or batch.get("invalid_langs"):
            note_missing_batch_once(state, batch)
            errors.append(
                f"{batch['batch_key']} incomplete "
                f"missing={','.join(batch.get('missing_langs', []))} "
                f"invalid={','.join(batch.get('invalid_langs', []))}"
            )
            continue

        uploaded_urls = []
        related_task_keys = []
        for item in batch["items"]:
            ep_num = item["ep_num"]
            clip_idx = item["clip_idx"]
            clip_path = Path(item["clip_path"])
            lang = item["lang"]
            ep_str = f"{ep_num:03d}"

            title, description, tags = load_metadata_for_clip(ep_num, clip_idx, lang)

            print(f"Uploading EP{ep_str} clip {clip_idx} ({lang}): {title}")
            try:
                vid_id = upload_short(clip_path, title, description, lang, tags)
                url = f"https://www.youtube.com/shorts/{vid_id}"
                print(f"  ✅ {url}")
                state.setdefault("uploaded", []).append(item["key"])
                state.setdefault("urls", {})[item["key"]] = url
                save_state(state)
                uploaded_urls.append((lang, url))
                ok, related_error = prepare_related_video_task(state, item, vid_id)
                if ok:
                    related_task_keys.append(item["key"])
                else:
                    msg = (
                        f"❌ [AgentStack Shorts] EP{ep_str} clip {clip_idx} ({lang}) "
                        f"related-video task not prepared: {related_error}"
                    )
                    print(msg)
                    discord_build_log(msg)
                    errors.append(msg)
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

        related_keys_to_process = list(dict.fromkeys(
            pending_related_video_task_keys(state) + related_task_keys
        ))
        related_errors = process_related_video_tasks(state, related_keys_to_process)
        for related_error in related_errors:
            msg = f"❌ [AgentStack Shorts] {related_error}"
            print(msg)
            errors.append(msg)
        if related_errors:
            detail = "\n".join(f"- {err}" for err in related_errors)
            if len(detail) > 1700:
                detail = detail[:1700].rstrip() + "\n- ... truncated; see upload_cron.log"
            discord_build_log(
                f"❌ [AgentStack Shorts] {len(related_errors)} related-video failure(s)\n{detail}"
            )

    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Status mode: show what's built, uploaded, and what's next
# ---------------------------------------------------------------------------

def run_status(state: dict) -> None:
    queue = build_upload_queue(state)
    uploaded = state.get("uploaded", [])
    urls = state.get("urls", {})
    missing = missing_render_episodes()
    related_tasks = state.get("related_video_tasks", {})

    print(f"\n=== AgentStack Daily Shorts Status ===")
    print(f"Uploaded: {len(uploaded)}")
    for key in uploaded:
        url = urls.get(key, "")
        print(f"  ✅ {key}  {url}")

    pending_items = sum(len(batch["items"]) for batch in queue)
    print(f"\nPending batches: {len(queue)} ({pending_items} videos)")
    if related_tasks:
        related_counts = {}
        for task in related_tasks.values():
            status = task.get("status", "unknown")
            related_counts[status] = related_counts.get(status, 0) + 1
        summary = ", ".join(f"{status}={count}" for status, count in sorted(related_counts.items()))
        print(f"Related video tasks: {summary}")
    if missing:
        span = ", ".join(f"EP{ep:03d}" for ep in missing)
        print(f"Missing rendered shorts packages: {span}")
    for batch in queue:
        langs = ",".join(item["lang"] for item in batch["items"])
        missing = ",".join(batch.get("missing_langs", []))
        invalid = ",".join(batch.get("invalid_langs", []))
        if missing or invalid:
            parts = []
            if missing:
                parts.append(f"missing={missing}")
            if invalid:
                parts.append(f"invalid={invalid}")
            status = "HELD " + " ".join(parts)
        else:
            status = "BUILT"
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
