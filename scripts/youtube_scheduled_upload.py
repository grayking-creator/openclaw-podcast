#!/usr/bin/env python3
from __future__ import annotations

"""
Scheduled YouTube upload for AgentStack Daily episodes.
Uploads one episode to all 5 channels (EN, ES, DE, PT, HI).
Called by cron twice daily: 5AM and 6PM ET.

Usage: python3 youtube_scheduled_upload.py <episode_number> [--video-mode static|flux|auto]
"""
import argparse
import datetime as dt
import os, sys, json, time, subprocess, re, requests as _requests
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - defensive for older local runtimes
    ZoneInfo = None

def _load_env_key(name: str) -> str:
    env_file = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_file):
        for line in open(env_file):
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get(name, "")

READONLY_API_KEY = _load_env_key("YOUTUBE_READONLY_API_KEY")

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
AUDIO_CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
MEDIA_EN_CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-media-en"
CDN_DIR = AUDIO_CDN_DIR
IMAGES_DIR = PODCAST_DIR / "images"
SHARED_DIR = Path.home() / "clawd/shared"
FFPROBE = "/opt/homebrew/bin/ffprobe"
MAX_AUDIO_SHORTFALL_SECONDS = 2.0
BUILD_LOG_CHANNEL = os.environ.get("BUILD_LOG_CHANNEL", "1485243812442804327")
BUILD_LOG_ERROR_CHANNEL = os.environ.get("BUILD_LOG_ERROR_CHANNEL", "1524923755019636948")


def _post_discord_log(message: str, channel: str) -> bool:
    bot_token = _load_env_key("DISCORD_BOT_TOKEN")
    if not bot_token:
        print("Discord build-log token unavailable; notification skipped", file=sys.stderr)
        return False
    result = subprocess.run(
        [
            "curl", "-sS", "-f", "-X", "POST",
            "-H", f"Authorization: Bot {bot_token}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"content": message[:1900]}),
            f"https://discord.com/api/v10/channels/{channel}/messages",
        ],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace") if isinstance(result.stderr, bytes) else (result.stderr or "")
        detail = stderr.strip().replace("\n", " ")[:500]
        suffix = f": {detail}" if detail else ""
        print(
            f"Discord build-log delivery failed (curl exit {result.returncode}){suffix}",
            file=sys.stderr,
        )
        return False
    return True


def _append_unique_issue(collection, seen, label, detail):
    item = (str(label), str(detail))
    if item in seen:
        return
    seen.add(item)
    collection.append(item)


def _post_youtube_issues(ep_str, failures, warnings, deferred):
    deferred = list(dict.fromkeys(deferred))
    if not failures and not warnings and not deferred:
        return

    lines = []
    if failures:
        lines.append("Failures:")
        lines.extend(f"  {label}: {detail}" for label, detail in failures)
    if warnings:
        lines.append("Warnings:")
        lines.extend(f"  {label}: {detail}" for label, detail in warnings)
    if deferred:
        lines.append(
            "Degraded: YouTube quota deferred "
            + ", ".join(lang.upper() for lang in deferred)
        )

    marker = "❌" if failures else "⚠️"
    _post_discord_log(
        f"{marker} **EP{ep_str} YouTube upload issues**\n" + "\n".join(lines),
        BUILD_LOG_ERROR_CHANNEL,
    )


def resolve_video_root() -> Path:
    candidates = [
        Path.home() / ".openclaw/workspace/video-workspace/flux-videos",
        Path.home() / ".openclaw/workspace/video-workspace/crossfire-series",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return candidates[-1]


VIDEO_ROOT = resolve_video_root()
VIDEO_BUILD_SCRIPT = SCRIPTS_DIR / "build_youtube_episode_videos.py"
UPLOADED_PATH = SCRIPTS_DIR / "youtube_uploaded.txt"
PACKAGING_OVERRIDES_PATH = SCRIPTS_DIR / "youtube_packaging_overrides.json"
VALID_VIDEO_MODES = {"static", "flux", "auto"}
QUOTA_DEFERRED = "quota_deferred"
YOUTUBE_UPLOAD_INSERT_UNITS = 1600
YOUTUBE_QUOTA_RETRY_MINUTE = 20


def quota_day() -> str:
    if ZoneInfo is not None:
        return dt.datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
    return dt.datetime.utcnow().date().isoformat()


def next_quota_retry_time() -> dt.datetime:
    if ZoneInfo is not None:
        pacific = ZoneInfo("America/Los_Angeles")
        local_tz = dt.datetime.now().astimezone().tzinfo
        next_day = dt.datetime.now(pacific).date() + dt.timedelta(days=1)
        reset = dt.datetime.combine(
            next_day,
            dt.time(0, YOUTUBE_QUOTA_RETRY_MINUTE),
            tzinfo=pacific,
        )
        return reset.astimezone(local_tz)
    return dt.datetime.now() + dt.timedelta(days=1)


def is_youtube_quota_error(exc: Exception) -> bool:
    text = str(exc).lower()
    if isinstance(exc, HttpError):
        try:
            content = exc.content.decode("utf-8", errors="ignore").lower()
        except Exception:
            content = ""
        text = f"{text}\n{content}"
    return any(
        marker in text
        for marker in (
            "quotaexceeded",
            "quota exceeded",
            "uploadlimitexceeded",
            "daily limit",
            "rate limit",
        )
    )


def schedule_deferred_retry(ep_num: int, video_mode: str) -> None:
    run_at = next_quota_retry_time()
    ep_str = f"{ep_num:03d}"
    tag = f"youtube_deferred_ep{ep_str}_{run_at:%Y%m%d}"
    cmd = (
        f"{run_at.minute} {run_at.hour} {run_at.day} {run_at.month} * "
        f"cd {SCRIPTS_DIR} && {sys.executable} {SCRIPTS_DIR / 'youtube_scheduled_upload.py'} "
        f"{ep_num} --video-mode {video_mode} >> /tmp/youtube_deferred_ep{ep_str}.log 2>&1 # {tag}"
    )
    try:
        existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current = existing.stdout if existing.returncode == 0 else ""
        if tag in current:
            print(f"  Deferred retry already scheduled: {tag}")
            return
        subprocess.run(["crontab", "-"], input=current.rstrip("\n") + "\n" + cmd + "\n", text=True, check=True)
        print(f"  Deferred retry scheduled for {run_at:%Y-%m-%d %H:%M %Z}: {tag}")
    except Exception as exc:
        print(f"  ⚠️  Could not schedule deferred YouTube retry: {exc}")


def ffprobe_duration(path):
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def validate_upload_video(video_path, audio_path, label):
    video_duration = ffprobe_duration(video_path)
    audio_duration = ffprobe_duration(audio_path)
    if audio_duration - video_duration > MAX_AUDIO_SHORTFALL_SECONDS:
        raise RuntimeError(
            f"{label} is truncated: video={video_duration:.2f}s audio={audio_duration:.2f}s path={video_path}"
        )


def extract_video_id(value):
    value = (value or "").strip()
    if not value:
        return ""
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value
    match = re.search(r"[?&]v=([A-Za-z0-9_-]{11})", value)
    return match.group(1) if match else ""


def youtube_video_exists(video_id):
    if not video_id:
        return False
    try:
        resp = _requests.get(
            "https://www.youtube.com/oembed",
            params={
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "format": "json",
            },
            timeout=15,
        )
        return resp.status_code == 200
    except Exception:
        return False


def persist_channel_state(path, state):
    try:
        path.write_text(json.dumps(state, indent=2))
    except Exception:
        pass


def mark_episode_uploaded(ep_num):
    try:
        existing = set()
        if UPLOADED_PATH.exists():
            existing = {
                int(line.strip())
                for line in UPLOADED_PATH.read_text().splitlines()
                if line.strip().isdigit()
            }
        existing.add(int(ep_num))
        lines = [f"{ep}\n" for ep in sorted(existing)]
        UPLOADED_PATH.write_text("".join(lines))
    except Exception:
        pass


def load_packaging_overrides():
    if not PACKAGING_OVERRIDES_PATH.exists():
        return {}
    try:
        return json.loads(PACKAGING_OVERRIDES_PATH.read_text())
    except Exception:
        return {}


def get_packaging_override(ep_num, lang):
    overrides = load_packaging_overrides()
    ep_key = f"{int(ep_num):03d}"
    return overrides.get(ep_key, {}).get(lang, {})


def resolve_override_path(raw_path):
    if not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path
    video_candidate = VIDEO_ROOT / path
    if video_candidate.exists():
        return video_candidate
    return PODCAST_DIR / path


def get_custom_thumbnail_path(ep_num, lang):
    override = get_packaging_override(ep_num, lang)
    raw_path = override.get("thumbnail", "").strip()
    if not raw_path:
        return None
    path = resolve_override_path(raw_path)
    return path if path and path.exists() else None


def load_release_state(ep_num):
    path = SCRIPTS_DIR / f"release_ep{int(ep_num):03d}_state.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def resolve_video_mode(ep_num, cli_mode="auto"):
    cli_mode = (cli_mode or "auto").strip().lower()
    if cli_mode not in VALID_VIDEO_MODES:
        raise ValueError(f"Invalid video mode: {cli_mode}")
    if cli_mode != "auto":
        return cli_mode

    env_mode = os.environ.get("OPENCLAW_YOUTUBE_VIDEO_MODE", "").strip().lower()
    if env_mode in {"static", "flux"}:
        return env_mode

    state_mode = str(load_release_state(ep_num).get("youtube_video_mode", "")).strip().lower()
    if state_mode in {"static", "flux"}:
        return state_mode

    return "static"

YOUTUBE_COPY = {
    "en": {
        "topics": "In this episode:",
        "show_notes": "Full show notes and source links:",
        "listen": "Listen on your favorite podcast app:",
        "chapters": "Chapters:",
        "default_desc": "Daily AI news and sharp analysis on infrastructure, product strategy, and policy.",
        "hashtags": ["#AgentStackDaily", "#AIPodcast", "#ArtificialIntelligence"],
    },
    "es": {
        "topics": "En este episodio:",
        "show_notes": "Notas completas y enlaces fuente:",
        "listen": "Escucha el podcast completo:",
        "chapters": "Capítulos:",
        "default_desc": "Noticias diarias de IA con análisis claro sobre infraestructura, producto y política.",
        "hashtags": ["#AgentStackDaily", "#PodcastIA", "#InteligenciaArtificial"],
    },
    "de": {
        "topics": "Heute im Podcast:",
        "show_notes": "Vollständige Shownotes und Quellen:",
        "listen": "Den Podcast vollständig hören:",
        "chapters": "Kapitel:",
        "default_desc": "Tägliche KI-News mit klarer Analyse zu Infrastruktur, Produktstrategie und Politik.",
        "hashtags": ["#AgentStackDaily", "#KIPodcast", "#KuenstlicheIntelligenz"],
    },
    "pt": {
        "topics": "Neste episódio:",
        "show_notes": "Notas completas e links das fontes:",
        "listen": "Ouça o podcast completo:",
        "chapters": "Capítulos:",
        "default_desc": "Notícias diárias de IA com análise clara sobre infraestrutura, produto e política.",
        "hashtags": ["#AgentStackDaily", "#PodcastIA", "#InteligenciaArtificial"],
    },
    "hi": {
        "topics": "आज के विषय:",
        "show_notes": "पूरा शो नोट्स और स्रोत लिंक:",
        "listen": "पूरा पॉडकास्ट सुनें:",
        "chapters": "चैप्टर्स:",
        "default_desc": "रोज़ का AI न्यूज़ और साफ़ विश्लेषण: इंफ्रास्ट्रक्चर, प्रोडक्ट और पॉलिसी।",
        "hashtags": ["#AgentStackDaily", "#AIPodcast", "#HindiPodcast"],
    },
}

BASE_TAGS = {
    "en": [
        "openclaw",
        "agentstack daily",
        "agentstack podcast",
        "daily ai news",
        "ai infrastructure",
        "ai podcast",
        "ai news",
        "artificial intelligence",
        "tech podcast",
    ],
    "es": [
        "openclaw",
        "agentstack daily",
        "podcast agentstack",
        "noticias diarias ia",
        "infraestructura ia",
        "podcast ia",
        "noticias ia",
        "inteligencia artificial",
        "podcast tecnologia",
    ],
    "de": [
        "openclaw",
        "agentstack daily",
        "agentstack podcast",
        "tägliche ki news",
        "ki infrastruktur",
        "ki podcast",
        "ki news",
        "künstliche intelligenz",
        "tech podcast deutsch",
    ],
    "pt": [
        "openclaw",
        "agentstack daily",
        "podcast agentstack",
        "noticias diarias ia",
        "infraestrutura ia",
        "podcast ia",
        "noticias ia",
        "inteligência artificial",
        "podcast tecnologia",
    ],
    "hi": [
        "openclaw",
        "agentstack daily",
        "agentstack podcast",
        "daily ai news",
        "एआई न्यूज़",
        "ai podcast",
        "ai hindi",
        "हिंदी पॉडकास्ट",
        "कृत्रिम बुद्धिमत्ता",
    ],
}

TOPIC_TAG_RULES = [
    (["anthropic", "claude"], {
        "en": ["anthropic", "claude ai"],
        "es": ["anthropic", "claude ai"],
        "de": ["anthropic", "claude ai"],
        "pt": ["anthropic", "claude ai"],
        "hi": ["anthropic", "claude ai"],
    }),
    (["openai", "agents sdk", "agent"], {
        "en": ["openai", "openai agents sdk", "ai agents"],
        "es": ["openai", "agents sdk", "agentes ia"],
        "de": ["openai", "agents sdk", "ki agenten"],
        "pt": ["openai", "agents sdk", "agentes ia"],
        "hi": ["openai", "agents sdk", "ai agents"],
    }),
    (["tsmc", "chip", "foundry", "fundición", "gießerei", "fundição"], {
        "en": ["tsmc", "ai chips", "semiconductor news"],
        "es": ["tsmc", "chips ia", "semiconductores"],
        "de": ["tsmc", "ki chips", "halbleiter"],
        "pt": ["tsmc", "chips ia", "semicondutores"],
        "hi": ["tsmc", "ai chips", "semiconductor news"],
    }),
    (["kyc", "telegram", "identity", "identidad", "identität", "identidade"], {
        "en": ["kyc", "telegram", "digital identity"],
        "es": ["kyc", "telegram", "identidad digital"],
        "de": ["kyc", "telegram", "digitale identität"],
        "pt": ["kyc", "telegram", "identidade digital"],
        "hi": ["kyc", "telegram", "digital identity"],
    }),
    (["voice", "dubbing", "doblaje", "synchron", "dublagem", "वॉयस"], {
        "en": ["ai dubbing", "voice actors", "voice cloning"],
        "es": ["doblaje ia", "actores de voz", "clonacion de voz"],
        "de": ["ki synchronisation", "synchronsprecher", "stimmklonen"],
        "pt": ["dublagem ia", "atores de voz", "clonagem de voz"],
        "hi": ["ai dubbing", "voice actors", "voice cloning"],
    }),
]

# Episode metadata (titles per language)
# Will be loaded from feed XML or hardcoded for known episodes

CHANNEL_CONFIG = {
    "en": {
        "token": SCRIPTS_DIR / "youtube_token_en.json",
        "channel_name": "AgentStack Daily",
        "suffix": "",
        "expected_channel": {
            "id": "UCTNxp_EbKdO3f2uengvBC4g",
            "title": "AgentStack Daily",
            "title_aliases": ["OpenClaw Daily"],
            "handle": "@AgentStackDaily",
        },
    },
    "es": {
        "token": SCRIPTS_DIR / "youtube_token_es.json",
        "channel_name": "AgentStack Daily Español",
        "suffix": " Español",
        "expected_channel": {
            "id": "UCIOxiwRkDPZr5MkCuc3NNhA",
            "title": "AgentStack Daily Español",
            "title_aliases": ["OpenClaw Daily Español"],
            "handle": "@AgentStackDailyES",
        },
    },
    "de": {
        "token": SCRIPTS_DIR / "youtube_token_de.json",
        "channel_name": "AgentStack Daily Deutsch",
        "suffix": " Deutsch",
        "expected_channel": {
            "id": "UC9OQsUqMSdY723JSa50pp5Q",
            "title": "AgentStack Daily Deutsch",
            "title_aliases": ["OpenClaw Daily Deutsch"],
            "handle": "@AgentStackDailyDE",
        },
    },
    "pt": {
        "token": SCRIPTS_DIR / "youtube_token_pt.json",
        "channel_name": "AgentStack Daily Português",
        "suffix": " Português",
        "expected_channel": {
            "id": "UCtgocn6qv3GXMeX4FJtFgQQ",
            "title": "AgentStack Daily Português",
            "title_aliases": ["OpenClaw Daily Português"],
            "handle": "@AgentStackDailyPT",
        },
    },
    "hi": {
        "token": SCRIPTS_DIR / "youtube_token_hi.json",
        "channel_name": "AgentStack Daily Hindi",
        "suffix": " हिंदी",
        "expected_channel": {
            "id": "UC0a37vGRA0ZTJKBxFNrU2dA",
            "title": "AgentStack Daily Hindi",
            "title_aliases": ["OpenClaw Daily Hindi"],
            "handle": "@AgentStackDailyHindi",
        },
    },
}

def get_audio_path(ep_num, lang):
    """Find the audio file for an episode + language."""
    ep_str = f"{ep_num:03d}"
    
    if lang == "en":
        # Check CDN audio/ dir first
        candidates = [
            MEDIA_EN_CDN_DIR / "audio" / f"episode_{ep_str}.mp3",
            CDN_DIR / "audio" / f"episode_{ep_str}.mp3",
            CDN_DIR / "audio" / f"episode_{ep_str}_full.mp3",
            CDN_DIR / "audio" / f"episode_{ep_str}_full_v2.mp3",
            MEDIA_EN_CDN_DIR / f"episode_{ep_str}.mp3",
            CDN_DIR / f"episode_{ep_str}.mp3",
            CDN_DIR / f"episode_{ep_str}_full.mp3",
            PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3",
            PODCAST_DIR / "audio" / f"episode_{ep_str}_full.mp3",
        ]
    else:
        candidates = [
            CDN_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3",
            CDN_DIR / "translations" / lang / f"episode_{ep_str}_{lang}.mp3",
            CDN_DIR / f"episode_{ep_str}_{lang}.mp3",
            PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3",
        ]
    
    for c in candidates:
        if c.exists():
            return c
    return None

def get_cover_path(ep_num, lang):
    """Find cover art, preferring per-language version."""
    ep_str = f"{ep_num:03d}"
    
    # Try language-specific first
    if lang != "en":
        lang_cover = IMAGES_DIR / f"episode_{ep_str}_cover_{lang}.png"
        if lang_cover.exists():
            return lang_cover
    
    # Fall back to EN cover
    en_cover = IMAGES_DIR / f"episode_{ep_str}_cover.png"
    if en_cover.exists():
        return en_cover

    return None


def get_publish_video_path(ep_num, lang):
    canonical = VIDEO_ROOT / "build" / "openclaw-daily" / f"ep{ep_num}" / "outputs" / f"openclaw{ep_num}_kb_publish_{lang}.mp4"
    legacy = VIDEO_ROOT / f"build/ep{ep_num}" / "outputs" / f"openclaw{ep_num}_kb_publish_{lang}.mp4"
    if canonical.exists():
        return canonical
    return canonical if (VIDEO_ROOT / "openclaw-daily" / f"ep{ep_num}").exists() else legacy


def episode_has_video_pipeline(ep_num):
    return (
        (
            (VIDEO_ROOT / "openclaw-daily" / f"ep{ep_num}" / "config.json").exists()
            or (VIDEO_ROOT / f"ep{ep_num}" / "config.json").exists()
        )
        and VIDEO_BUILD_SCRIPT.exists()
    )


def build_publish_videos(ep_num):
    result = subprocess.run(
        [sys.executable, str(VIDEO_BUILD_SCRIPT), str(ep_num)],
        cwd=str(PODCAST_DIR),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Localized publish video build failed for EP{ep_num:03d}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    if result.stdout.strip():
        print(result.stdout.strip())

def get_episode_title(ep_num, lang):
    """Get episode title from feed, falling back to current show notes."""
    import re
    ep_str = f"{ep_num:03d}"
    
    if lang == "en":
        feed_path = PODCAST_DIR / "feed.xml"
    else:
        feed_path = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
    
    if feed_path.exists():
        content = feed_path.read_text()
        # Find the item with this episode number
        items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
        for item in items:
            ep_match = re.search(r'<itunes:episode>(\d+)</itunes:episode>', item)
            if ep_match and int(ep_match.group(1)) == ep_num:
                title_match = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item)
                if title_match:
                    return title_match.group(1).strip()

    notes_path = get_show_notes_path(ep_num, lang)
    if notes_path.exists():
        notes = notes_path.read_text()
        section_match = re.search(r"^## Episode Title\s*\n(.+?)(?=\n## |\Z)", notes, re.MULTILINE | re.DOTALL)
        if section_match:
            for raw_line in section_match.group(1).splitlines():
                line = " ".join(raw_line.split()).strip(" *_`")
                if line:
                    return line
        h1_match = re.search(r"^#\s+(.+)$", notes, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
    
    return f"AgentStack Daily EP{ep_str}"

def get_episode_description(ep_num, lang):
    """Get episode description from feed."""
    import re
    
    if lang == "en":
        feed_path = PODCAST_DIR / "feed.xml"
    else:
        feed_path = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
    
    if not feed_path.exists():
        return ""
    
    content = feed_path.read_text()
    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    for item in items:
        ep_match = re.search(r'<itunes:episode>(\d+)</itunes:episode>', item)
        if ep_match and int(ep_match.group(1)) == ep_num:
            desc_match = re.search(r'<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>', item, re.DOTALL)
            if desc_match:
                return desc_match.group(1).strip()
    
    return ""


def get_episode_chapters(ep_num, lang="en"):
    """Parse YouTube chapter markers from localized show notes when available.
    Returns a formatted string like:
      00:00 Hook — The Company Layer
      02:10 Story 1 — Paperclip ...
    Returns empty string if no chapters found.
    """
    show_notes_path = get_show_notes_path(ep_num, lang)
    if not show_notes_path.exists():
        return ""

    content = show_notes_path.read_text()

    # Find ## Chapters section
    chapters_match = re.search(r'## Chapters\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not chapters_match:
        return ""

    chapters_block = chapters_match.group(1)

    # Match lines like: - **[MM:SS] Title text**
    chapter_lines = []
    for m in re.finditer(r'\[\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*\]\s*(.*?)(?:\*\*)?(?:\s*\\?\s*\n|$)', chapters_block):
        timestamp = m.group(1).strip()
        # Ensure HH:MM:SS format for YouTube (it accepts MM:SS too)
        title_text = m.group(2).strip().rstrip('*').strip()
        if title_text:
            chapter_lines.append(f"{timestamp} {title_text}")

    return "\n".join(chapter_lines)


def get_show_notes_url(ep_num, lang):
    """Return the deep-link URL to the episode's show notes page."""
    lang_prefix = {
        "en": "",
        "es": "/es",
        "de": "/de",
        "pt": "/pt",
        "hi": "/hi",
    }
    prefix = lang_prefix.get(lang, "")
    return f"https://tobyonfitnesstech.com{prefix}/podcasts/episode-{ep_num}/"


def get_show_notes_path(ep_num, lang):
    ep_str = f"{ep_num:03d}"
    if lang == "en":
        return PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    return PODCAST_DIR / "translations" / lang / f"show_notes_episode_{ep_str}_{lang}.md"


def get_story_titles(ep_num, lang, limit=5):
    path = get_show_notes_path(ep_num, lang)
    if not path.exists():
        return []

    titles = []
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        match = re.match(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+)$", line)
        if not match:
            continue
        timestamp, heading = match.groups()
        if timestamp == "00:00":
            continue
        if "—" in heading:
            heading = heading.split("—", 1)[1].strip()
        elif "-" in heading:
            heading = heading.split("-", 1)[1].strip()
        heading = heading.strip(" -*")
        if not heading:
            continue
        titles.append(heading)
        if len(titles) >= limit:
            break
    return titles


def get_verified_links(ep_num, lang, max_links=30):
    """Return source/project links from the show notes for YouTube descriptions."""
    path = get_show_notes_path(ep_num, lang)
    if not path.exists() and lang != "en":
        path = get_show_notes_path(ep_num, "en")
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8", errors="ignore")
    links_match = re.search(r"^## Verified Links\s*\n(.*?)(?=\n## |\Z)", content, re.MULTILINE | re.DOTALL)
    if not links_match and lang != "en":
        en_path = get_show_notes_path(ep_num, "en")
        if en_path.exists():
            content = en_path.read_text(encoding="utf-8", errors="ignore")
            links_match = re.search(r"^## Verified Links\s*\n(.*?)(?=\n## |\Z)", content, re.MULTILINE | re.DOTALL)
    if not links_match:
        return []

    links = []
    seen = set()
    for raw_line in links_match.group(1).splitlines():
        line = " ".join(raw_line.strip().lstrip("-").split())
        if not line:
            continue
        match = re.match(r"(.+?):\s*(https?://\S+)", line)
        if match:
            label, url = match.groups()
            label = label.strip(" -*")
        else:
            url_match = re.search(r"https?://\S+", line)
            if not url_match:
                continue
            url = url_match.group(0)
            label = line.replace(url, "").strip(" :-*") or url
        url = url.rstrip(".,)")
        key = url.lower()
        if key in seen:
            continue
        links.append((label, url))
        seen.add(key)
        if len(links) >= max_links:
            break
    return links


def build_upload_title(ep_num, lang):
    override = get_packaging_override(ep_num, lang)
    title = (override.get("title") or get_episode_title(ep_num, lang) or "").strip()
    if not title:
        title = f"AgentStack Daily EP{ep_num:03d}"

    if lang != "en":
        suffix = CHANNEL_CONFIG[lang]["suffix"]
        if suffix not in title:
            title += f" | AgentStack Daily EP{ep_num:03d}{suffix}"

    if len(title) > 100:
        title = title[:97] + "..."
    return title


def build_youtube_description(ep_num, lang):
    copy = YOUTUBE_COPY.get(lang, YOUTUBE_COPY["en"])
    override = get_packaging_override(ep_num, lang)
    title = (override.get("title") or get_episode_title(ep_num, lang) or "").strip()
    header = f"EP{ep_num:03d} | {title}"
    show_notes_url = get_show_notes_url(ep_num, lang)
    stories = get_story_titles(ep_num, lang)
    chapters = get_episode_chapters(ep_num, lang)
    summary = (override.get("summary") or copy["default_desc"]).strip()

    lines = [header, "", summary]
    if stories:
        lines.extend(["", copy["topics"]])
        lines.extend([f"- {story}" for story in stories])

    lines.extend([
        "",
        f"{copy['show_notes']} {show_notes_url}",
        f"{copy['listen']} https://tobyonfitnesstech.com/podcasts/",
    ])

    verified_links = get_verified_links(ep_num, lang)
    if verified_links:
        lines.extend(["", "Source and project links:"])
        lines.extend([f"- {label}: {url}" for label, url in verified_links])

    if chapters:
        lines.extend(["", copy["chapters"], chapters])

    hashtag_line = " ".join(copy.get("hashtags", []))
    if hashtag_line:
        lines.extend(["", hashtag_line])

    result = "\n".join(lines).strip()
    return result[:5000]


def build_youtube_tags(ep_num, lang):
    text_parts = [
        build_upload_title(ep_num, lang) or "",
        get_episode_description(ep_num, lang) or "",
        *get_story_titles(ep_num, lang),
    ]
    haystack = " ".join(text_parts).lower()
    tags = list(BASE_TAGS.get(lang, BASE_TAGS["en"]))

    for keywords, lang_tags in TOPIC_TAG_RULES:
        if any(keyword in haystack for keyword in keywords):
            tags.extend(lang_tags.get(lang, lang_tags["en"]))

    tags.extend([f"episode {ep_num}", f"ep {ep_num}", f"ep{ep_num:03d}"])

    deduped = []
    seen = set()
    total_chars = 0
    for tag in tags:
        clean = " ".join(tag.split()).strip()
        if not clean:
            continue
        key = clean.lower()
        if key in seen:
            continue
        projected = total_chars + len(clean)
        if deduped:
            projected += 1
        if projected > 460:
            break
        deduped.append(clean)
        seen.add(key)
        total_chars = projected
    return deduped

def render_mp4(cover_path, audio_path, output_path):
    """Render MP4 from cover + audio."""
    subprocess.run([
        "ffmpeg", "-loop", "1",
        "-i", str(cover_path),
        "-i", str(audio_path),
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-pix_fmt", "yuv420p",
        str(output_path), "-y"
    ], capture_output=True, check=True)

def _normalize_handle(value):
    value = (value or "").strip()
    if not value:
        return ""
    handle = value if value.startswith("@") else f"@{value}"
    return handle.lower()


def fetch_channel_identity(yt):
    resp = yt.channels().list(part="id,snippet", mine=True).execute()
    items = resp.get("items", [])
    if not items:
        raise RuntimeError("No authenticated YouTube channel found for this token")

    ch = items[0]
    snippet = ch.get("snippet", {})
    custom_url = snippet.get("customUrl", "")
    return {
        "id": ch.get("id", ""),
        "title": (snippet.get("title", "") or "").strip(),
        "handle": _normalize_handle(custom_url),
    }


def verify_expected_channel(yt, token_path, expected):
    actual = fetch_channel_identity(yt)

    mismatches = []
    if expected.get("id") and actual["id"] != expected["id"]:
        mismatches.append(f"id expected={expected['id']} actual={actual['id']}")
    expected_titles = [expected.get("title", ""), *expected.get("title_aliases", [])]
    expected_titles = [t for t in expected_titles if t]
    if expected_titles and actual["title"] not in expected_titles:
        mismatches.append(
            f"title expected one of={expected_titles!r} actual={actual['title']!r}"
        )

    expected_handle = _normalize_handle(expected.get("handle", ""))
    if expected_handle and actual["handle"] != expected_handle:
        mismatches.append(
            f"handle expected={expected_handle!r} actual={actual['handle']!r}"
        )

    if mismatches:
        detail = "\n  - ".join(mismatches)
        raise RuntimeError(
            "\n❌ HARD STOP: Token channel mismatch before upload.\n"
            f"Token: {token_path}\n"
            f"Authenticated: id={actual['id']} title={actual['title']!r} handle={actual['handle']!r}\n"
            f"Expected: id={expected.get('id')} title={expected.get('title')!r} handle={expected_handle!r}\n"
            f"Mismatches:\n  - {detail}\n"
            "Upload aborted before videos.insert()."
        )

    print(
        f"  ✅ Channel verified: {actual['title']} ({actual['id']}, {actual['handle']})"
    )


def check_episode_already_uploaded(yt, episode_number):
    """Check if an episode with this number is already on the channel.
    Uses read-only API key (Lilly's quota) for playlist reads — no OAuth quota burned.
    Falls back to OAuth if API key unavailable.
    Returns (video_id, title) or (None, None)."""
    ep_str = f"{episode_number:03d}"
    search_terms = [f"EP{ep_str}", f"Episode {episode_number}:", f"Episode {ep_str}"]

    if READONLY_API_KEY:
        # Get channel ID from OAuth (1 unit), then use API key for playlist reads
        channel_resp = yt.channels().list(part="contentDetails", mine=True).execute()
        uploads_playlist = channel_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        page_token = None
        while True:
            params = {"key": READONLY_API_KEY, "playlistId": uploads_playlist,
                      "part": "snippet", "maxResults": 50}
            if page_token:
                params["pageToken"] = page_token
            resp = _requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params=params).json()
            for item in resp.get("items", []):
                title = item["snippet"]["title"]
                vid_id = item["snippet"]["resourceId"]["videoId"]
                if "#" in title:
                    continue  # skip shorts
                for term in search_terms:
                    if term.lower() in title.lower():
                        return vid_id, title
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        return None, None

    # Fallback: OAuth playlist read
    channel_resp = yt.channels().list(part="contentDetails", mine=True).execute()
    uploads_playlist = channel_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    playlist_resp = yt.playlistItems().list(part="snippet", playlistId=uploads_playlist, maxResults=50).execute()
    for item in playlist_resp.get("items", []):
        title = item["snippet"]["title"]
        vid_id = item["snippet"]["resourceId"]["videoId"]
        for term in search_terms:
            if term.lower() in title.lower():
                # Only match long-form episode uploads, not shorts (shorts have hashtags in title)
                if "#" not in title:
                    return vid_id, title
    return None, None


def set_custom_thumbnail(yt, video_id, thumbnail_path):
    yt.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg"),
    ).execute()


def upload_to_youtube(
    token_path,
    title,
    description,
    tags,
    video_path,
    expected_channel,
    episode_number=None,
    thumbnail_path=None,
    thumbnail_warnings=None,
):
    """Upload video to YouTube, return video ID."""
    with open(token_path) as f:
        creds = Credentials.from_authorized_user_info(json.load(f))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    yt = build("youtube", "v3", credentials=creds)

    # Hard pre-upload gate.
    verify_expected_channel(yt, token_path, expected_channel)

    # Duplicate guard: abort if this episode is already on the channel.
    if episode_number is not None:
        existing_id, existing_title = check_episode_already_uploaded(yt, episode_number)
        if existing_id:
            raise RuntimeError(f"DUPLICATE GUARD: Episode {episode_number} already exists on this channel as '{existing_title}' ({existing_id}). Aborting upload.")
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "28",  # Science & Technology
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        }
    }
    
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            print(f"    {int(status.progress()*100)}%...")

    video_id = response["id"]
    if thumbnail_path and Path(thumbnail_path).exists():
        try:
            set_custom_thumbnail(yt, video_id, thumbnail_path)
            print(f"    🎨 Thumbnail applied: {Path(thumbnail_path).name}")
        except Exception as exc:
            warning = f"Thumbnail upload failed: {exc}"
            print(f"    ⚠️  {warning}")
            if thumbnail_warnings is not None:
                thumbnail_warnings.append(warning)

    return video_id

def parse_args():
    parser = argparse.ArgumentParser(description="Upload an AgentStack Daily episode to YouTube")
    parser.add_argument("episode", type=int, help="Episode number")
    parser.add_argument(
        "--video-mode",
        choices=sorted(VALID_VIDEO_MODES),
        default="auto",
        help="Upload mode: static cover video, flux publish videos, or auto-resolve from state/env (default)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    ep_num = int(args.episode)
    ep_str = f"{ep_num:03d}"
    video_mode = resolve_video_mode(ep_num, args.video_mode)
    print(f"\n{'='*60}")
    print(f"YouTube Upload: Episode {ep_num}")
    print(f"{'='*60}")
    print(f"Video mode: {video_mode}")
    
    results = {}
    deferred = []
    failures = []
    warnings = []
    failure_keys = set()
    warning_keys = set()
    current_quota_day = quota_day()

    # Load per-channel state to skip already-uploaded channels
    channel_state_file = SCRIPTS_DIR / "youtube_channel_state.json"
    try:
        channel_state = json.loads(channel_state_file.read_text()) if channel_state_file.exists() else {}
    except Exception:
        channel_state = {}
    ep_state = channel_state.get(ep_str, {})
    use_video_pipeline = video_mode == "flux"
    if use_video_pipeline:
        try:
            if not episode_has_video_pipeline(ep_num):
                raise RuntimeError(
                    f"EP{ep_str} requested flux video mode, but the publish-video pipeline is not available for this episode"
                )
            print("Preparing localized publish videos from crossfire-series master...")
            build_publish_videos(ep_num)
        except Exception as exc:
            _append_unique_issue(
                failures,
                failure_keys,
                "FLUX",
                f"publish-video prebuild failed: {type(exc).__name__}: {exc}",
            )
            _post_youtube_issues(ep_str, failures, warnings, deferred)
            return 1

    for lang, config in CHANNEL_CONFIG.items():
        # Skip if this channel already confirmed uploaded for this episode
        if ep_state.get(lang) == "done":
            stored_url = ep_state.get(f"{lang}_url", "")
            stored_id = extract_video_id(stored_url)
            print(f"\n--- {lang.upper()} (AgentStack Daily {config['suffix']}) ---")
            if stored_id and youtube_video_exists(stored_id):
                print(f"  ⏭️  Already uploaded (skipping)")
                results[lang] = stored_url or "already uploaded"
                continue

            print("  ⚠️  Stored upload state is stale or deleted on YouTube — rebuilding/re-uploading")
            ep_state.pop(lang, None)
            ep_state.pop(f"{lang}_url", None)
            channel_state[ep_str] = ep_state
            persist_channel_state(channel_state_file, channel_state)

        if (
            ep_state.get(lang) == QUOTA_DEFERRED
            and ep_state.get(f"{lang}_quota_day") == current_quota_day
            and not os.environ.get("YOUTUBE_RETRY_SAME_QUOTA_DAY")
        ):
            print(f"\n--- {lang.upper()} ({config['channel_name']}) ---")
            print(
                "  ⏳ Deferred until the next YouTube quota day "
                f"(last quota error on {current_quota_day})"
            )
            deferred.append(lang)
            continue

        print(f"\n--- {lang.upper()} ({config['channel_name']}) ---")
        
        # Get audio
        audio = get_audio_path(ep_num, lang)
        if not audio:
            print(f"  ❌ No audio found for {lang}")
            _append_unique_issue(failures, failure_keys, lang.upper(), "No audio found")
            continue
        print(f"  Audio: {audio.name}")
        
        # Get title + description
        title = build_upload_title(ep_num, lang)
        desc = build_youtube_description(ep_num, lang)
        thumbnail_path = get_custom_thumbnail_path(ep_num, lang)
        
        print(f"  Title: {title[:80]}...")
        if thumbnail_path:
            print(f"  Thumbnail: {Path(thumbnail_path).name}")
        
        mp4_path = None
        publish_video = get_publish_video_path(ep_num, lang)
        if publish_video.exists():
            print(f"  Video: {publish_video.name}")
            upload_video = publish_video
        else:
            if use_video_pipeline:
                detail = f"Expected localized Flux publish video was not created: {publish_video}"
                print(f"  ❌ {detail}")
                _append_unique_issue(
                    failures,
                    failure_keys,
                    lang.upper(),
                    detail,
                )
                continue
            cover = get_cover_path(ep_num, lang)
            if not cover:
                print(f"  ❌ No cover art found")
                _append_unique_issue(failures, failure_keys, lang.upper(), "No cover art found")
                continue
            print(f"  Cover: {cover.name}")

            mp4_path = Path(f"/tmp/ep{ep_str}_{lang}.mp4")
            print(f"  Rendering MP4...")
            try:
                render_mp4(cover, audio, mp4_path)
            except Exception as e:
                print(f"  ❌ MP4 render failed: {e}")
                _append_unique_issue(
                    failures,
                    failure_keys,
                    lang.upper(),
                    f"MP4 render failed: {e}",
                )
                continue
            upload_video = mp4_path

        try:
            validate_upload_video(upload_video, audio, f"{lang.upper()} upload source")
        except Exception as e:
            print(f"  ❌ Upload source failed validation: {e}")
            _append_unique_issue(
                failures,
                failure_keys,
                lang.upper(),
                f"Upload source failed validation: {e}",
            )
            try:
                if mp4_path and mp4_path.exists():
                    mp4_path.unlink()
            except Exception:
                pass
            continue
        
        # Upload
        print(f"  Uploading...")
        tags = build_youtube_tags(ep_num, lang)
        thumbnail_upload_warnings = []
        try:
            vid_id = upload_to_youtube(
                config["token"],
                title,
                desc,
                tags,
                upload_video,
                config["expected_channel"],
                episode_number=ep_num,
                thumbnail_path=thumbnail_path,
                thumbnail_warnings=thumbnail_upload_warnings,
            )
            for warning in thumbnail_upload_warnings:
                _append_unique_issue(warnings, warning_keys, lang.upper(), warning)
            url = f"https://www.youtube.com/watch?v={vid_id}"
            print(f"  ✅ {url}")
            results[lang] = url
            # Save per-channel progress immediately
            ep_state[lang] = "done"
            ep_state[f"{lang}_url"] = url
            channel_state[ep_str] = ep_state
            persist_channel_state(channel_state_file, channel_state)
        except Exception as e:
            print(f"  ❌ Upload failed: {e}")
            if is_youtube_quota_error(e):
                print(
                    f"  ⏳ YouTube quota exhausted after estimated "
                    f"{YOUTUBE_UPLOAD_INSERT_UNITS} units for videos.insert; "
                    "deferring remaining channels."
                )
                remaining_langs = [
                    item_lang
                    for item_lang in CHANNEL_CONFIG
                    if ep_state.get(item_lang) != "done"
                    and item_lang not in deferred
                ]
                for item_lang in remaining_langs:
                    ep_state[item_lang] = QUOTA_DEFERRED
                    ep_state[f"{item_lang}_quota_day"] = current_quota_day
                    ep_state[f"{item_lang}_last_error"] = str(e)
                    deferred.append(item_lang)
                channel_state[ep_str] = ep_state
                persist_channel_state(channel_state_file, channel_state)
                break
            _append_unique_issue(failures, failure_keys, lang.upper(), str(e))
        finally:
            # Clean up rendered MP4 — no reason to keep it after upload
            try:
                if mp4_path and mp4_path.exists():
                    mp4_path.unlink()
                    print(f"  🧹 Cleaned up {mp4_path.name}")
            except Exception:
                pass

        time.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Episode {ep_num} Upload Summary:")
    for lang, url in results.items():
        print(f"  {lang.upper()}: {url}")
    if deferred:
        print(f"  Deferred by quota: {', '.join(lang.upper() for lang in deferred)}")
    if failures:
        for lang, error in failures:
            print(f"  Failed: {lang.upper()}: {error}")
    
    # Discord notifications: routine status and failures have separate channels.
    if results:
        done_count = len([lang for lang in CHANNEL_CONFIG if ep_state.get(lang) == "done"])
        msg = f"📺 **EP{ep_str} YouTube status** ({done_count}/5 channels done):\n"
        for lang, url in results.items():
            msg += f"  {lang.upper()}: {url}\n"
        _post_discord_log(msg, BUILD_LOG_CHANNEL)

    _post_youtube_issues(ep_str, failures, warnings, deferred)

    if len([lang for lang in CHANNEL_CONFIG if ep_state.get(lang) == "done"]) == 5:
        mark_episode_uploaded(ep_num)
        return 0
    if deferred and not failures:
        schedule_deferred_retry(ep_num, video_mode)
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
