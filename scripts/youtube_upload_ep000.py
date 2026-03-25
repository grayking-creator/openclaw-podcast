#!/usr/bin/env python3
"""Upload EP000 to all 4 translated YouTube channels."""
import os, json, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]
SECRET = os.path.join(os.path.dirname(__file__), "youtube_client_secret.json")
TOKEN  = os.path.join(os.path.dirname(__file__), "youtube_token.json")

BASE = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast"

CHANNELS = {
    "hi": {
        "channel_id": "UC0a37vGRA0ZTJKBxFNrU2dA",
        "handle":     "@OpenClawDailyHindi",
        "title":      "Special: Building a Distributed AI Cluster | हिंदी पॉडकास्ट | OpenClaw Daily EP000",
        "description": "हिंदी में: exo-labs के साथ एक Distributed AI Cluster कैसे बनाएं।\n\nOpenClaw Daily — रोज़ाना AI की दुनिया से।\n\nEnglish version: https://www.youtube.com/@tobyonfitness\nPodcast feed: https://grayking-creator.github.io/openclaw-podcast/translations/feed_hi.xml\n\nTags: hindi podcast, हिंदी पॉडकास्ट, AI hindi, artificial intelligence hindi, desi tech podcast, daily hindi podcast, openclaw",
        "tags": ["hindi podcast", "हिंदी पॉडकास्ट", "AI hindi", "artificial intelligence", "desi podcast", "indian tech podcast", "daily hindi podcast", "openclaw", "exo labs", "distributed AI"],
        "video": "/tmp/ep000_upload.mp4",
    },
    "es": {
        "channel_id": "UCIOxiwRkDPZr5MkCuc3NNhA",
        "handle":     "@OpenClawDailyES",
        "title":      "Especial: Construyendo un Clúster de IA Distribuida | OpenClaw Daily EP000 Español",
        "description": "En español: Cómo construir un clúster de IA distribuida con exo-labs.\n\nOpenClaw Daily — IA cada día.\n\nVersión en inglés: https://www.youtube.com/@tobyonfitness\nFeed del podcast: https://grayking-creator.github.io/openclaw-podcast/translations/feed_es.xml\n\nTags: podcast español, IA en español, inteligencia artificial, podcast tech español, openclaw",
        "tags": ["podcast español", "IA en español", "inteligencia artificial", "tech podcast español", "openclaw", "exo labs", "IA distribuida", "podcast diario"],
                        "video": "/tmp/ep000_upload.mp4",
    },
    "de": {
        "channel_id": "UC9OQsUqMSdY723JSa50pp5Q",
        "handle":     "@OpenClawDailyDE",
        "title":      "Special: Ein verteiltes KI-Cluster bauen mit exo-labs | OpenClaw Daily EP000 Deutsch",
        "description": "Auf Deutsch: Wie man mit exo-labs ein verteiltes KI-Cluster aufbaut.\n\nOpenClaw Daily — KI jeden Tag.\n\nEnglische Version: https://www.youtube.com/@tobyonfitness\nPodcast-Feed: https://grayking-creator.github.io/openclaw-podcast/translations/feed_de.xml\n\nTags: KI Podcast Deutsch, künstliche Intelligenz, Tech Podcast Deutsch, openclaw",
        "tags": ["KI Podcast", "künstliche Intelligenz", "Tech Podcast Deutsch", "openclaw", "exo labs", "verteilte KI", "deutschsprachiger Podcast"],
                        "video": "/tmp/ep000_upload.mp4",
    },
    "pt": {
        "channel_id": "UCtgocn6qv3GXMeX4FJtFgQQ",
        "handle":     "@OpenClawDailyPT",
        "title":      "Especial: Construindo um Cluster de IA Distribuída | OpenClaw Daily EP000 Português",
        "description": "Em português: Como construir um cluster de IA distribuída com exo-labs.\n\nOpenClaw Daily — IA todos os dias.\n\nVersão em inglês: https://www.youtube.com/@tobyonfitness\nFeed do podcast: https://grayking-creator.github.io/openclaw-podcast/translations/feed_pt.xml\n\nTags: podcast português, IA em português, inteligência artificial, podcast tech, openclaw",
        "tags": ["podcast português", "IA em português", "inteligência artificial", "tech podcast", "openclaw", "exo labs", "IA distribuída"],
                        "video": "/tmp/ep000_upload.mp4",
    },
}

def get_creds():
    creds = None
    if os.path.exists(TOKEN):
        with open(TOKEN) as f:
            creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRET, SCOPES)
            creds = flow.run_local_server(port=8766, open_browser=True)
        with open(TOKEN, "w") as f:
            f.write(creds.to_json())
    return creds

def upload_to_channel(yt, ch_data, lang):
    print(f"\n{'='*60}")
    print(f"Uploading to {ch_data['handle']} ({lang.upper()})...")

    body = {
        "snippet": {
            "title": ch_data["title"],
            "description": ch_data["description"],
            "tags": ch_data["tags"],
            "categoryId": "28",  # Science & Technology
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(ch_data["video"], mimetype="video/mp4", resumable=True)
    request = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Upload {int(status.progress() * 100)}%...")

    video_id = response["id"]
    print(f"  ✅ Uploaded: https://www.youtube.com/watch?v={video_id}")
    return video_id

def main():
    creds = get_creds()
    yt = build("youtube", "v3", credentials=creds)

    results = {}
    for lang, ch_data in CHANNELS.items():
        try:
            vid_id = upload_to_channel(yt, ch_data, lang)
            results[lang] = {"status": "ok", "video_id": vid_id, "url": f"https://www.youtube.com/watch?v={vid_id}"}
        except Exception as e:
            print(f"  ❌ Failed {lang}: {e}")
            results[lang] = {"status": "error", "error": str(e)}
        time.sleep(2)

    print("\n\n=== RESULTS ===")
    for lang, r in results.items():
        print(f"{lang.upper()}: {r}")

if __name__ == "__main__":
    main()
