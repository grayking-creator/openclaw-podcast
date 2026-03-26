#!/usr/bin/env python3
"""
Scheduled YouTube upload for OpenClaw Daily episodes.
Uploads one episode to all 5 channels (EN, ES, DE, PT, HI).
Called by cron twice daily: 5AM and 6PM ET.

Usage: python3 youtube_scheduled_upload.py <episode_number>
"""
import os, sys, json, time, subprocess
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
IMAGES_DIR = PODCAST_DIR / "images"
SHARED_DIR = Path.home() / "clawd/shared"

# Episode metadata (titles per language)
# Will be loaded from feed XML or hardcoded for known episodes

CHANNEL_CONFIG = {
    "en": {
        "token": SCRIPTS_DIR / "youtube_token_en.json",
        "channel_name": "OpenClaw Daily",
        "suffix": "",
    },
    "es": {
        "token": SCRIPTS_DIR / "youtube_token_es.json",
        "channel_name": "OpenClaw Daily Español",
        "suffix": " Español",
    },
    "de": {
        "token": SCRIPTS_DIR / "youtube_token_de.json",
        "channel_name": "OpenClaw Daily Deutsch",
        "suffix": " Deutsch",
    },
    "pt": {
        "token": SCRIPTS_DIR / "youtube_token_pt.json",
        "channel_name": "OpenClaw Daily Português",
        "suffix": " Português",
    },
    "hi": {
        "token": SCRIPTS_DIR / "youtube_token_hi.json",
        "channel_name": "OpenClaw Daily Hindi",
        "suffix": " हिंदी",
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

def upload_to_youtube(token_path, title, description, tags, video_path):
    """Upload video to YouTube, return video ID."""
    with open(token_path) as f:
        creds = Credentials.from_authorized_user_info(json.load(f))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    yt = build("youtube", "v3", credentials=creds)
    
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
    
    for lang, config in CHANNEL_CONFIG.items():
        print(f"\n--- {lang.upper()} ({config['channel_name']}) ---")
        
        # Get audio
        audio = get_audio_path(ep_num, lang)
        if not audio:
            print(f"  ❌ No audio found for {lang}")
            continue
        print(f"  Audio: {audio.name}")
        
        # Get cover
        cover = get_cover_path(ep_num, lang)
        if not cover:
            print(f"  ❌ No cover art found")
            continue
        print(f"  Cover: {cover.name}")
        
        # Get title + description
        title = get_episode_title(ep_num, lang)
        if lang != "en" and config["suffix"] not in title:
            title += f" | OpenClaw Daily EP{ep_str}{config['suffix']}"
        desc = get_episode_description(ep_num, lang)
        if not desc:
            desc = f"OpenClaw Daily Episode {ep_num}"
        desc += f"\n\nWebsite: https://tobyonfitnesstech.com"
        
        print(f"  Title: {title[:80]}...")
        
        # Render MP4
        mp4_path = Path(f"/tmp/ep{ep_str}_{lang}.mp4")
        print(f"  Rendering MP4...")
        try:
            render_mp4(cover, audio, mp4_path)
        except Exception as e:
            print(f"  ❌ MP4 render failed: {e}")
            continue
        
        # Upload
        print(f"  Uploading...")
        tags = ["openclaw", "AI podcast", "OpenClaw Daily", f"episode {ep_num}"]
        try:
            vid_id = upload_to_youtube(
                config["token"], title, desc, tags, mp4_path
            )
            url = f"https://www.youtube.com/watch?v={vid_id}"
            print(f"  ✅ {url}")
            results[lang] = url
        except Exception as e:
            print(f"  ❌ Upload failed: {e}")
        
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
