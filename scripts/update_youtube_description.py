#!/usr/bin/env python3
"""
Update YouTube video descriptions for an already-uploaded episode.
Rebuilds descriptions from feed + show notes (with correct chapters) and patches
each video via the YouTube Data API.

Usage:
  /opt/homebrew/bin/python3.14 scripts/update_youtube_description.py 25
"""
import sys, json, re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent

sys.path.insert(0, str(SCRIPTS_DIR))
from youtube_scheduled_upload import (
    CHANNEL_CONFIG, get_episode_description, get_episode_chapters,
    get_episode_title, get_show_notes_url, _load_readonly_api_key,
)

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_authenticated_service(token_path):
    creds = Credentials.from_authorized_user_file(str(token_path))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)

def get_video_id_from_state(ep_num, lang):
    """Look up video ID from channel state JSON."""
    state_file = SCRIPTS_DIR / "youtube_channel_state.json"
    if not state_file.exists():
        return None
    state = json.loads(state_file.read_text())
    ep_str = f"{ep_num:03d}"
    ep_state = state.get(ep_str, {})
    return ep_state.get(f"{lang}_url", "").split("v=")[-1] or None

def build_description(ep_num, lang):
    """Rebuild the full description the same way youtube_scheduled_upload.py does."""
    desc = get_episode_description(ep_num, lang)
    if not desc:
        desc = f"OpenClaw Daily Episode {ep_num}"

    show_notes_url = get_show_notes_url(ep_num, lang)
    desc += f"\n\n📖 Full show notes & links: {show_notes_url}"
    desc += f"\n🎙️ Subscribe on your favourite podcast app: https://tobyonfitnesstech.com/podcasts/"

    chapters = get_episode_chapters(ep_num)
    if chapters:
        desc += f"\n\n─── CHAPTERS ───\n{chapters}"

    desc += f"\n\n---\nWebsite: https://tobyonfitnesstech.com"
    return desc

def get_current_video(yt, video_id):
    r = yt.videos().list(part="snippet", id=video_id).execute()
    items = r.get("items", [])
    return items[0] if items else None

def update_video_description(yt, video_id, new_description):
    video = get_current_video(yt, video_id)
    if not video:
        print(f"  ❌ Video not found: {video_id}")
        return False

    snippet = video["snippet"]
    snippet["description"] = new_description

    yt.videos().update(
        part="snippet",
        body={"id": video_id, "snippet": snippet}
    ).execute()
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: update_youtube_description.py <episode_number>")
        sys.exit(1)

    ep_num = int(sys.argv[1])
    ep_str = f"{ep_num:03d}"

    print(f"\nUpdating YouTube descriptions for EP{ep_str}...")
    print(f"Chapters from show_notes_episode_{ep_str}.md:")
    chapters = get_episode_chapters(ep_num)
    if not chapters:
        print("  ⚠️  No chapters found in show notes!")
    else:
        print(chapters)
    print()

    # Load video IDs from state file
    state_file = SCRIPTS_DIR / "youtube_channel_state.json"
    if not state_file.exists():
        print("❌ youtube_channel_state.json not found")
        sys.exit(1)
    state = json.loads(state_file.read_text())
    ep_state = state.get(ep_str, {})

    for lang, config in CHANNEL_CONFIG.items():
        url = ep_state.get(f"{lang}_url", "")
        if not url:
            print(f"  ⚠️  No {lang.upper()} video URL in state, skipping")
            continue

        video_id = url.split("v=")[-1]
        print(f"  → {lang.upper()}: {url}")

        try:
            yt = get_authenticated_service(config["token"])

            new_desc = build_description(ep_num, lang)
            title = get_episode_title(ep_num, lang)

            success = update_video_description(yt, video_id, new_desc)
            if success:
                print(f"  ✅ Description updated ({len(new_desc)} chars)")
                if chapters:
                    print(f"     Chapters: {len(chapters.splitlines())} entries")
            else:
                print(f"  ❌ Update failed for {video_id}")

        except Exception as e:
            print(f"  ❌ {lang.upper()} error: {e}")

    print("\nDone.")

if __name__ == "__main__":
    main()
