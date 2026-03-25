#!/usr/bin/env python3
"""Upload EP000 to all 5 OpenClaw Daily channels using per-channel tokens."""
import os, json, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
BASE    = os.path.dirname(SCRIPTS)  # openclaw-podcast/

CHANNELS = {
    "en": {
        "token":   f"{SCRIPTS}/youtube_token_en.json",
        "title":   "Special: Building a Distributed AI Cluster with exo-labs | OpenClaw Daily EP000",
        "desc":    "How we built a distributed AI cluster using exo-labs — running large language models across multiple machines.\n\nOpenClaw Daily — AI every day.\n\nPodcast feed: https://grayking-creator.github.io/openclaw-podcast/feed.xml\nWebsite: https://tobyonfitnesstech.com",
        "tags":    ["openclaw", "exo labs", "distributed AI", "local AI", "LLM", "AI podcast", "tech podcast", "AI cluster"],
        "video":   "/tmp/ep000_en.mp4",
        "cover":   f"{BASE}/images/episode_000_cover.png",
        "audio":   f"{BASE}/audio/exo_cluster_podcast_nova.mp3",
    },
    "es": {
        "token":   f"{SCRIPTS}/youtube_token_es.json",
        "title":   "Especial: Construyendo un Clúster de IA con exo-labs | OpenClaw Daily EP000 Español",
        "desc":    "Cómo construimos un clúster de IA distribuida con exo-labs — ejecutando modelos de lenguaje en múltiples máquinas.\n\nOpenClaw Daily — IA cada día.\n\nFeed del podcast: https://grayking-creator.github.io/openclaw-podcast/translations/feed_es.xml\nVersión en inglés: https://www.youtube.com/@OpenClawDaily",
        "tags":    ["openclaw", "podcast español", "IA en español", "inteligencia artificial", "exo labs", "IA distribuida", "tech podcast español"],
        "video":   "/tmp/ep000_es.mp4",
        "cover":   f"{BASE}/images/episode_000_cover_es.png",
        "audio":   f"{BASE}/audio/exo_cluster_podcast_nova.mp3",
    },
    "de": {
        "token":   f"{SCRIPTS}/youtube_token_de.json",
        "title":   "Special: Ein verteiltes KI-Cluster mit exo-labs | OpenClaw Daily EP000 Deutsch",
        "desc":    "Wie wir mit exo-labs ein verteiltes KI-Cluster gebaut haben — große Sprachmodelle auf mehreren Maschinen.\n\nOpenClaw Daily — KI jeden Tag.\n\nPodcast-Feed: https://grayking-creator.github.io/openclaw-podcast/translations/feed_de.xml\nEnglische Version: https://www.youtube.com/@OpenClawDaily",
        "tags":    ["openclaw", "KI Podcast", "künstliche Intelligenz", "exo labs", "verteilte KI", "Tech Podcast Deutsch", "deutschsprachiger Podcast"],
        "video":   "/tmp/ep000_de.mp4",
        "cover":   f"{BASE}/images/episode_000_cover_de.png",
        "audio":   f"{BASE}/audio/exo_cluster_podcast_nova.mp3",
    },
    "pt": {
        "token":   f"{SCRIPTS}/youtube_token_pt.json",
        "title":   "Especial: Construindo um Cluster de IA com exo-labs | OpenClaw Daily EP000 Português",
        "desc":    "Como construímos um cluster de IA distribuída com exo-labs — rodando modelos de linguagem em múltiplas máquinas.\n\nOpenClaw Daily — IA todos os dias.\n\nFeed do podcast: https://grayking-creator.github.io/openclaw-podcast/translations/feed_pt.xml\nVersão em inglês: https://www.youtube.com/@OpenClawDaily",
        "tags":    ["openclaw", "podcast português", "IA em português", "inteligência artificial", "exo labs", "IA distribuída", "tech podcast"],
        "video":   "/tmp/ep000_pt.mp4",
        "cover":   f"{BASE}/images/episode_000_cover_pt.png",
        "audio":   f"{BASE}/audio/exo_cluster_podcast_nova.mp3",
    },
    "hi": {
        "token":   f"{SCRIPTS}/youtube_token_hi.json",
        "title":   "Special: exo-labs के साथ Distributed AI Cluster | OpenClaw Daily EP000 हिंदी",
        "desc":    "exo-labs के साथ एक Distributed AI Cluster कैसे बनाएं — कई मशीनों पर बड़े भाषा मॉडल चलाना।\n\nOpenClaw Daily — रोज़ाना AI की दुनिया से।\n\nPodcast feed: https://grayking-creator.github.io/openclaw-podcast/translations/feed_hi.xml\nEnglish version: https://www.youtube.com/@OpenClawDaily",
        "tags":    ["hindi podcast", "हिंदी पॉडकास्ट", "AI hindi", "artificial intelligence hindi", "exo labs", "desi tech podcast", "openclaw", "distributed AI hindi"],
        "video":   "/tmp/ep000_hi.mp4",
        "cover":   f"{BASE}/images/episode_000_cover_hi.png",
        "audio":   f"{BASE}/audio/exo_cluster_podcast_nova.mp3",
    },
}

def get_yt(token_path):
    with open(token_path) as f:
        creds = Credentials.from_authorized_user_info(json.load(f))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)

def make_video(lang, ch):
    """Render MP4 from cover + audio if not already done."""
    import subprocess
    out = ch["video"]
    if os.path.exists(out):
        print(f"  📼 Using existing {out}")
        return
    print(f"  🎬 Rendering MP4 for {lang}...")
    subprocess.run([
        "ffmpeg", "-loop", "1",
        "-i", ch["cover"],
        "-i", ch["audio"],
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-pix_fmt", "yuv420p",
        out, "-y"
    ], check=True, capture_output=True)
    print(f"  ✅ Rendered: {out}")

def upload(yt, ch, lang):
    body = {
        "snippet": {
            "title":       ch["title"],
            "description": ch["desc"],
            "tags":        ch["tags"],
            "categoryId":  "28",  # Science & Technology
        },
        "status": {
            "privacyStatus":          "public",
            "selfDeclaredMadeForKids": False,
        }
    }
    media = MediaFileUpload(ch["video"], mimetype="video/mp4", resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            print(f"  {int(status.progress()*100)}%...", end="\r")
    vid_id = response["id"]
    print(f"  ✅ https://www.youtube.com/watch?v={vid_id}")
    return vid_id

def main():
    results = {}
    for lang, ch in CHANNELS.items():
        print(f"\n{'='*60}")
        print(f"Channel: {lang.upper()}")

        # Verify token points to right channel
        yt = get_yt(ch["token"])
        resp = yt.channels().list(part="snippet", mine=True).execute()
        ch_name = resp["items"][0]["snippet"]["title"] if resp.get("items") else "UNKNOWN"
        print(f"  Token: {ch_name}")

        make_video(lang, ch)
        vid_id = upload(yt, ch, lang)
        results[lang] = {"channel": ch_name, "video_id": vid_id, "url": f"https://www.youtube.com/watch?v={vid_id}"}
        time.sleep(2)

    print("\n\n=== ALL DONE ===")
    for lang, r in results.items():
        print(f"{lang.upper()} ({r['channel']}): {r['url']}")

if __name__ == "__main__":
    main()
