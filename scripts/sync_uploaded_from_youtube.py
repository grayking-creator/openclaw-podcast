#!/usr/bin/env python3
"""
Sync youtube_uploaded.txt with actual YouTube channel state.
Uses a read-only API key (Lilly's quota) for playlist checks — 
no OAuth required, no upload quota burned.
Runs before youtube_cron_runner.sh picks the next episode.
"""
import json, os, sys, re, requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DONE_FILE = os.path.join(SCRIPT_DIR, "youtube_uploaded.txt")

# Load API key from .env
def load_api_key():
    env_file = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_file):
        for line in open(env_file):
            if "YOUTUBE_READONLY_API_KEY" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("YOUTUBE_READONLY_API_KEY", "")

# Channel IDs for all 5 OpenClaw Daily channels
CHANNELS = {
    "en": "UCTNxp_EbKdO3f2uengvBC4g",
    "es": "UCIOxiwRkDPZr5MkCuc3NNhA",
    "de": "UC9OQsUqMSdY723JSa50pp5Q",
    "pt": "UCtgocn6qv3GXMeX4FJtFgQQ",
    "hi": "UC0a37vGRA0ZTJKBxFNrU2dA",
}

def get_uploads_playlist(api_key, channel_id):
    """Get the uploads playlist ID for a channel."""
    resp = requests.get("https://www.googleapis.com/youtube/v3/channels", params={
        "key": api_key,
        "id": channel_id,
        "part": "contentDetails",
    })
    items = resp.json().get("items", [])
    if not items:
        return None
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_uploaded_episodes(api_key, channel_id):
    """Return set of episode numbers found on channel using read-only API key."""
    playlist_id = get_uploads_playlist(api_key, channel_id)
    if not playlist_id:
        return set()

    episodes = set()
    page_token = None
    while True:
        params = {
            "key": api_key,
            "playlistId": playlist_id,
            "part": "snippet",
            "maxResults": 50,
        }
        if page_token:
            params["pageToken"] = page_token
        resp = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params=params)
        data = resp.json()
        for item in data.get("items", []):
            title = item["snippet"]["title"]
            if "#" in title:
                continue  # skip shorts
            m = re.search(r'Episode\s+(\d+)', title, re.IGNORECASE) or \
                re.search(r'EP0*(\d+)', title, re.IGNORECASE)
            if m:
                episodes.add(int(m.group(1)))
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return episodes

# Load existing done set
try:
    with open(DONE_FILE) as f:
        done = set(int(x.strip()) for x in f if x.strip())
except FileNotFoundError:
    done = set()

print(f"youtube_uploaded.txt has: {sorted(done)}")

api_key = load_api_key()
if not api_key:
    print("⚠️  No YOUTUBE_READONLY_API_KEY found — skipping sync")
    sys.exit(0)

# Check EN channel as authoritative source
try:
    live = get_uploaded_episodes(api_key, CHANNELS["en"])
    print(f"YouTube EN channel has episodes: {sorted(live)}")
    merged = done | live
    if merged != done:
        with open(DONE_FILE, "w") as f:
            for ep in sorted(merged):
                f.write(f"{ep}\n")
        print(f"Updated youtube_uploaded.txt: added {sorted(merged - done)}")
    else:
        print("youtube_uploaded.txt already up to date")
except Exception as e:
    print(f"⚠️  Could not sync from YouTube: {e} — keeping existing file")
    sys.exit(0)
