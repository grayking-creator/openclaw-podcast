#!/usr/bin/env python3
"""
Scheduled YouTube upload for OpenClaw Daily episodes.
Uploads one episode to all 5 channels (EN, ES, DE, PT, HI).
Called by cron twice daily: 5AM and 6PM ET.

Usage: python3 youtube_scheduled_upload.py <episode_number>
"""
import os, sys, json, time, subprocess, re, requests as _requests
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def _load_readonly_api_key():
    env_file = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_file):
        for line in open(env_file):
            if "YOUTUBE_READONLY_API_KEY" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("YOUTUBE_READONLY_API_KEY", "")

READONLY_API_KEY = _load_readonly_api_key()

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
IMAGES_DIR = PODCAST_DIR / "images"
SHARED_DIR = Path.home() / "clawd/shared"
VIDEO_ROOT = Path.home() / ".openclaw/workspace/video-workspace/crossfire-series"
VIDEO_BUILD_SCRIPT = SCRIPTS_DIR / "build_youtube_episode_videos.py"

YOUTUBE_COPY = {
    "en": {
        "topics": "In this episode:",
        "show_notes": "Full show notes and source links:",
        "listen": "Listen on your favorite podcast app:",
        "chapters": "Chapters:",
        "default_desc": "Daily AI news and sharp analysis on infrastructure, product strategy, and policy.",
        "hashtags": ["#OpenClawDaily", "#AIPodcast", "#ArtificialIntelligence"],
    },
    "es": {
        "topics": "En este episodio:",
        "show_notes": "Notas completas y enlaces fuente:",
        "listen": "Escucha el podcast completo:",
        "chapters": "Capítulos:",
        "default_desc": "Noticias diarias de IA con análisis claro sobre infraestructura, producto y política.",
        "hashtags": ["#OpenClawDaily", "#PodcastIA", "#InteligenciaArtificial"],
    },
    "de": {
        "topics": "Heute im Podcast:",
        "show_notes": "Vollständige Shownotes und Quellen:",
        "listen": "Den Podcast vollständig hören:",
        "chapters": "Kapitel:",
        "default_desc": "Tägliche KI-News mit klarer Analyse zu Infrastruktur, Produktstrategie und Politik.",
        "hashtags": ["#OpenClawDaily", "#KIPodcast", "#KuenstlicheIntelligenz"],
    },
    "pt": {
        "topics": "Neste episódio:",
        "show_notes": "Notas completas e links das fontes:",
        "listen": "Ouça o podcast completo:",
        "chapters": "Capítulos:",
        "default_desc": "Notícias diárias de IA com análise clara sobre infraestrutura, produto e política.",
        "hashtags": ["#OpenClawDaily", "#PodcastIA", "#InteligenciaArtificial"],
    },
    "hi": {
        "topics": "आज के विषय:",
        "show_notes": "पूरा शो नोट्स और स्रोत लिंक:",
        "listen": "पूरा पॉडकास्ट सुनें:",
        "chapters": "चैप्टर्स:",
        "default_desc": "रोज़ का AI न्यूज़ और साफ़ विश्लेषण: इंफ्रास्ट्रक्चर, प्रोडक्ट और पॉलिसी।",
        "hashtags": ["#OpenClawDaily", "#AIPodcast", "#HindiPodcast"],
    },
}

BASE_TAGS = {
    "en": [
        "openclaw",
        "openclaw daily",
        "openclaw podcast",
        "daily ai news",
        "ai infrastructure",
        "ai podcast",
        "ai news",
        "artificial intelligence",
        "tech podcast",
    ],
    "es": [
        "openclaw",
        "openclaw daily",
        "podcast openclaw",
        "noticias diarias ia",
        "infraestructura ia",
        "podcast ia",
        "noticias ia",
        "inteligencia artificial",
        "podcast tecnologia",
    ],
    "de": [
        "openclaw",
        "openclaw daily",
        "openclaw podcast",
        "tägliche ki news",
        "ki infrastruktur",
        "ki podcast",
        "ki news",
        "künstliche intelligenz",
        "tech podcast deutsch",
    ],
    "pt": [
        "openclaw",
        "openclaw daily",
        "podcast openclaw",
        "noticias diarias ia",
        "infraestrutura ia",
        "podcast ia",
        "noticias ia",
        "inteligência artificial",
        "podcast tecnologia",
    ],
    "hi": [
        "openclaw",
        "openclaw daily",
        "openclaw podcast",
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
        "channel_name": "OpenClaw Daily",
        "suffix": "",
        "expected_channel": {
            "id": "UCTNxp_EbKdO3f2uengvBC4g",
            "title": "OpenClaw Daily",
            "handle": "@openclawdaily",
        },
    },
    "es": {
        "token": SCRIPTS_DIR / "youtube_token_es.json",
        "channel_name": "OpenClaw Daily Español",
        "suffix": " Español",
        "expected_channel": {
            "id": "UCIOxiwRkDPZr5MkCuc3NNhA",
            "title": "OpenClaw Daily Español",
            "handle": "@openclawdailyes",
        },
    },
    "de": {
        "token": SCRIPTS_DIR / "youtube_token_de.json",
        "channel_name": "OpenClaw Daily Deutsch",
        "suffix": " Deutsch",
        "expected_channel": {
            "id": "UC9OQsUqMSdY723JSa50pp5Q",
            "title": "OpenClaw Daily Deutsch",
            "handle": "@openclawdailyde",
        },
    },
    "pt": {
        "token": SCRIPTS_DIR / "youtube_token_pt.json",
        "channel_name": "OpenClaw Daily Português",
        "suffix": " Português",
        "expected_channel": {
            "id": "UCtgocn6qv3GXMeX4FJtFgQQ",
            "title": "OpenClaw Daily Português",
            "handle": "@openclawdailypt",
        },
    },
    "hi": {
        "token": SCRIPTS_DIR / "youtube_token_hi.json",
        "channel_name": "OpenClaw Daily Hindi",
        "suffix": " हिंदी",
        "expected_channel": {
            "id": "UC0a37vGRA0ZTJKBxFNrU2dA",
            "title": "OpenClaw Daily Hindi",
            "handle": "@openclawdailyhindi",
        },
    },
}

def get_audio_path(ep_num, lang):
    """Find the audio file for an episode + language."""
    ep_str = f"{ep_num:03d}"
    
    if lang == "en":
        # Check CDN audio/ dir first
        candidates = [
            CDN_DIR / "audio" / f"episode_{ep_str}.mp3",
            CDN_DIR / "audio" / f"episode_{ep_str}_full.mp3",
            CDN_DIR / "audio" / f"episode_{ep_str}_full_v2.mp3",
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
    return VIDEO_ROOT / f"build/ep{ep_num}" / "outputs" / f"openclaw{ep_num}_kb_publish_{lang}.mp4"


def episode_has_video_pipeline(ep_num):
    return (VIDEO_ROOT / f"ep{ep_num}").exists() and VIDEO_BUILD_SCRIPT.exists()


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
    """Get episode title from translation feed or EN feed."""
    import re
    ep_str = f"{ep_num:03d}"
    
    if lang == "en":
        feed_path = PODCAST_DIR / "feed.xml"
    else:
        feed_path = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
    
    if not feed_path.exists():
        return f"OpenClaw Daily EP{ep_str}"
    
    content = feed_path.read_text()
    # Find the item with this episode number
    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    for item in items:
        ep_match = re.search(r'<itunes:episode>(\d+)</itunes:episode>', item)
        if ep_match and int(ep_match.group(1)) == ep_num:
            title_match = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item)
            if title_match:
                return title_match.group(1).strip()
    
    return f"OpenClaw Daily EP{ep_str}"

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


def get_episode_chapters(ep_num):
    """Parse YouTube chapter markers from EN show notes.
    Returns a formatted string like:
      00:00 Hook — The Company Layer
      02:10 Story 1 — Paperclip ...
    Returns empty string if no chapters found.
    """
    show_notes_path = PODCAST_DIR / f"show_notes_episode_{ep_num:03d}.md"
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


def build_youtube_description(ep_num, lang):
    copy = YOUTUBE_COPY.get(lang, YOUTUBE_COPY["en"])
    title = get_episode_title(ep_num, lang)
    header = f"EP{ep_num:03d} | {title}"
    show_notes_url = get_show_notes_url(ep_num, lang)
    stories = get_story_titles(ep_num, lang)
    chapters = get_episode_chapters(ep_num)

    lines = [header, "", copy["default_desc"]]
    if stories:
        lines.extend(["", copy["topics"]])
        lines.extend([f"- {story}" for story in stories])

    lines.extend([
        "",
        f"{copy['show_notes']} {show_notes_url}",
        f"{copy['listen']} https://tobyonfitnesstech.com/podcasts/",
    ])

    if chapters:
        lines.extend(["", copy["chapters"], chapters])

    hashtag_line = " ".join(copy.get("hashtags", []))
    if hashtag_line:
        lines.extend(["", hashtag_line])

    result = "\n".join(lines).strip()
    return result[:5000]


def build_youtube_tags(ep_num, lang):
    text_parts = [
        get_episode_title(ep_num, lang) or "",
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
    return value if value.startswith("@") else f"@{value}"


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
    if expected.get("title") and actual["title"] != expected["title"]:
        mismatches.append(
            f"title expected={expected['title']!r} actual={actual['title']!r}"
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


def upload_to_youtube(token_path, title, description, tags, video_path, expected_channel, episode_number=None):
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
    
    return response["id"]

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_scheduled_upload.py <episode_number>")
        sys.exit(1)
    
    ep_num = int(sys.argv[1])
    ep_str = f"{ep_num:03d}"
    print(f"\n{'='*60}")
    print(f"YouTube Upload: Episode {ep_num}")
    print(f"{'='*60}")
    
    results = {}

    # Load per-channel state to skip already-uploaded channels
    channel_state_file = SCRIPTS_DIR / "youtube_channel_state.json"
    try:
        channel_state = json.loads(channel_state_file.read_text()) if channel_state_file.exists() else {}
    except Exception:
        channel_state = {}
    ep_state = channel_state.get(ep_str, {})
    use_video_pipeline = episode_has_video_pipeline(ep_num)
    if use_video_pipeline:
        print("Preparing localized publish videos from crossfire-series master...")
        build_publish_videos(ep_num)

    for lang, config in CHANNEL_CONFIG.items():
        # Skip if this channel already confirmed uploaded for this episode
        if ep_state.get(lang) == "done":
            print(f"\n--- {lang.upper()} (OpenClaw Daily {config['suffix']}) ---")
            print(f"  ⏭️  Already uploaded (skipping)")
            results[lang] = ep_state.get(f"{lang}_url", "already uploaded")
            continue
        print(f"\n--- {lang.upper()} ({config['channel_name']}) ---")
        
        # Get audio
        audio = get_audio_path(ep_num, lang)
        if not audio:
            print(f"  ❌ No audio found for {lang}")
            continue
        print(f"  Audio: {audio.name}")
        
        # Get title + description
        title = get_episode_title(ep_num, lang)
        if lang != "en" and config["suffix"] not in title:
            title += f" | OpenClaw Daily EP{ep_str}{config['suffix']}"
        # YouTube title limit is 100 characters
        if len(title) > 100:
            title = title[:97] + "..."
        desc = build_youtube_description(ep_num, lang)
        
        print(f"  Title: {title[:80]}...")
        
        mp4_path = None
        publish_video = get_publish_video_path(ep_num, lang)
        if publish_video.exists():
            print(f"  Video: {publish_video.name}")
            upload_video = publish_video
        else:
            if use_video_pipeline:
                raise RuntimeError(
                    f"Expected localized publish video for {lang.upper()} but none was created: {publish_video}"
                )
            cover = get_cover_path(ep_num, lang)
            if not cover:
                print(f"  ❌ No cover art found")
                continue
            print(f"  Cover: {cover.name}")

            mp4_path = Path(f"/tmp/ep{ep_str}_{lang}.mp4")
            print(f"  Rendering MP4...")
            try:
                render_mp4(cover, audio, mp4_path)
            except Exception as e:
                print(f"  ❌ MP4 render failed: {e}")
                continue
            upload_video = mp4_path
        
        # Upload
        print(f"  Uploading...")
        tags = build_youtube_tags(ep_num, lang)
        try:
            vid_id = upload_to_youtube(
                config["token"],
                title,
                desc,
                tags,
                upload_video,
                config["expected_channel"],
                episode_number=ep_num,
            )
            url = f"https://www.youtube.com/watch?v={vid_id}"
            print(f"  ✅ {url}")
            results[lang] = url
            # Save per-channel progress immediately
            ep_state[lang] = "done"
            ep_state[f"{lang}_url"] = url
            channel_state[ep_str] = ep_state
            try:
                channel_state_file.write_text(json.dumps(channel_state, indent=2))
            except Exception:
                pass
        except Exception as e:
            print(f"  ❌ Upload failed: {e}")
        finally:
            # Clean up rendered MP4 — no reason to keep it after upload
            try:
                if mp4_path.exists():
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
    
    # Discord notification
    if results:
        msg = f"📺 **EP{ep_str} uploaded to YouTube** ({len(results)}/5 channels):\n"
        for lang, url in results.items():
            msg += f"  {lang.upper()}: {url}\n"
        
        bot_token = os.environ.get("DISCORD_BOT_TOKEN", "")
        subprocess.run([
            "curl", "-s", "-X", "POST",
            "-H", f"Authorization: Bot {bot_token}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"content": msg}),
            "https://discord.com/api/v10/channels/1485243812442804327/messages"
        ], capture_output=True)
    
    return 0 if len(results) == 5 else 1

if __name__ == "__main__":
    sys.exit(main())
