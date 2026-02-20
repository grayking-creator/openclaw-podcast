#!/usr/bin/env python3
"""
Hourly Podcast Content Gatherer
Runs every hour to collect news, build content, and generate episodes when ready.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
import sys

# Configuration
PODCAST_DIR = Path("/Users/tobyglennpeters/.openclaw/workspace/podcast")
CONTENT_DIR = PODCAST_DIR / "content_staging"
HOURLY_LOG = PODCAST_DIR / "hourly_log.md"
TELEGRAM_CHAT_ID = "8319992332"
INDEX_URL = "https://grayking-creator.github.io/openclaw-podcast/"

# Target episode duration (30-40 minutes = 1800-2400 seconds)
TARGET_MIN = 30
TARGET_MAX = 40
SECONDS_PER_WORD = 3  # ~20 words per minute for narration

# Ensure directories exist
CONTENT_DIR.mkdir(exist_ok=True)

# News sources to check (URLs)
NEWS_SOURCES = {
    "reuters": "https://www.reuters.com/search/news?blob=openclaw",
    "venturebeat": "https://venturebeat.com/ai/",
    "techcrunch": "https://techcrunch.com/tag/openclaw/",
    "wired": "https://www.wired.com/tag/openai/",
}

def log(message):
    """Log message to hourly log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HOURLY_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def fetch_news():
    """Fetch news from various sources"""
    log("Fetching latest news...")
    # In production, this would scrape actual news sites
    # For now, we'll simulate with a placeholder
    return []

def get_latest_episode_num():
    """Find the next episode number"""
    existing = list(PODCAST_DIR.glob("episode_*.md"))
    nums = []
    for f in existing:
        match = re.search(r'episode_(\d+)', f.name)
        if match:
            nums.append(int(match.group(1)))
    return max(nums) + 1 if nums else 1

def estimate_duration(text):
    """Estimate audio duration in seconds"""
    word_count = len(text.split())
    return word_count * SECONDS_PER_WORD

def load_staged_content():
    """Load all staged content"""
    content_file = CONTENT_DIR / "staged_content.json"
    if content_file.exists():
        with open(content_file) as f:
            return json.load(f)
    return {"segments": [], "last_updated": None}

def save_staged_content(data):
    """Save staged content"""
    content_file = CONTENT_DIR / "staged_content.json"
    data["last_updated"] = datetime.now().isoformat()
    with open(content_file, "w") as f:
        json.dump(data, f, indent=2)

def add_content_segment(title, source, text, category="general"):
    """Add a new content segment"""
    data = load_staged_content()
    data["segments"].append({
        "title": title,
        "source": source,
        "text": text,
        "category": category,
        "timestamp": datetime.now().isoformat()
    })
    save_staged_content(data)
    log(f"Added content segment: {title}")

def build_episode_from_segments():
    """Build episode script from staged segments"""
    data = load_staged_content()
    if not data["segments"]:
        log("No staged content to build episode from")
        return None
    
    # Group segments by category
    categories = {}
    for seg in data["segments"]:
        cat = seg.get("category", "general")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(seg)
    
    # Build script
    episode_num = get_latest_episode_num()
    script_lines = [
        f"# OpenClaw Daily Podcast - Episode {episode_num}: Latest Updates",
        f"# Date: {datetime.now().strftime('%B %d, %Y')}",
        "# Hosts: Nova (warm British) & Alloy (neutral)",
        "",
        "---",
        "",
        "[NOVA]: Good evening and welcome back to OpenClaw Daily! I'm Nova.",
        "",
        "[ALLOY]: And I'm Alloy. We've got another hour of updates for you today.",
        "",
    ]
    
    # Add content from each segment
    for i, seg in enumerate(data["segments"]):
        script_lines.append(f"[ALLOY]: {seg['text']}")
        script_lines.append("")
    
    # Closing
    script_lines.extend([
        "[NOVA]: That's all the news for this update. Thanks for listening!",
        "",
        "[ALLOY]: Stay curious, stay local, and keep building!",
        "",
        "---",
        "",
        "# END OF EPISODE",
    ])
    
    return "\n".join(script_lines)

def generate_audio(script_path):
    """Generate audio from script"""
    episode_num = get_latest_episode_num()
    output_name = f"episode_{episode_num:03d}_full"
    
    cmd = [
        sys.executable,
        str(PODCAST_DIR / "generate_audio.py"),
        str(script_path),
        "-o", output_name
    ]
    
    log(f"Generating audio for episode {episode_num}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        audio_file = PODCAST_DIR / "audio" / f"{output_name}.mp3"
        if audio_file.exists():
            duration = subprocess.run([
                "ffprobe", "-v", "error", 
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(audio_file)
            ], capture_output=True, text=True)
            return float(duration.stdout.strip() or 0)
    return 0

def update_rss(episode_num, duration_sec):
    """Update RSS feed"""
    feed_file = PODCAST_DIR / "feed.xml"
    duration_min = int(duration_sec / 60)
    
    # Read feed
    with open(feed_file) as f:
        content = f.read()
    
    # Add new episode item (before last </channel>)
    episode_item = f'''
    <item>
      <title>Episode {episode_num}: Hourly Update</title>
      <link>https://grayking-creator.github.io/openclaw-podcast/episode_{episode_num:03d}.md</link>
      <description>Hourly news update covering the latest OpenClaw developments.</description>
      <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S EST')}</pubDate>
      <enclosure url="https://grayking-creator.github.io/openclaw-podcast/audio/episode_{episode_num:03d}_full.mp3" length="0" type="audio/mpeg"/>
      <itunes:duration>{duration_min}:{int(duration_sec % 60):02d}</itunes:duration>
      <itunes:episode>{episode_num}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
    </item>'''
    
    content = content.replace("</channel>", episode_item + "\n  </channel>")
    
    # Update last build date
    content = content.replace(
        "{{LAST_BUILD_DATE}}",
        datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    )
    
    with open(feed_file, "w") as f:
        f.write(content)
    
    log(f"Updated RSS feed for episode {episode_num}")

def deploy():
    """Deploy to GitHub"""
    log("Deploying to GitHub...")
    subprocess.run(["git", "add", "."], cwd=PODCAST_DIR)
    subprocess.run([
        "git", "commit", "-m", 
        f"Auto-update {datetime.now().isoformat()}"
    ], cwd=PODCAST_DIR)
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=PODCAST_DIR,
        capture_output=True, text=True
    )
    if result.returncode == 0:
        log("Deployed successfully!")
        return True
    else:
        log(f"Deploy failed: {result.stderr}")
        return False

def notify_telegram(episode_num, duration_min):
    """Send Telegram notification"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        log("TELEGRAM_BOT_TOKEN not set, skipping notification")
        return
    
    message = f"""🎙️ New Episode Ready!

Episode: {episode_num}
Duration: {duration_min} minutes
Listen: {INDEX_URL}

# OpenClaw #AI #Podcast"""
    
    subprocess.run([
        "curl", "-s", "-X", "POST",
        f"https://api.telegram.org/bot{token}/sendMessage",
        "-d", f"chat_id={TELEGRAM_CHAT_ID}",
        "-d", f"text={message}"
    ])
    log("Sent Telegram notification")

def main():
    """Main hourly task"""
    log("=== Starting hourly content gathering ===")
    
    # Fetch latest news
    news = fetch_news()
    
    # For demo, add a timestamped segment
    current_hour = datetime.now().strftime("%I %p")
    add_content_segment(
        title=f"Hourly Update - {current_hour}",
        source="auto",
        text=f"It's {current_hour} and here's the latest on OpenClaw. The local AI revolution continues to gain momentum with new developments coming in every hour.",
        category="update"
    )
    
    # Check total content duration
    data = load_staged_content()
    total_text = " ".join([s["text"] for s in data["segments"]])
    total_duration = estimate_duration(total_text)
    total_minutes = total_duration / 60
    
    log(f"Total staged content: {total_minutes:.1f} minutes")
    
    # If we have enough content (30-40 min), generate episode
    if total_duration >= TARGET_MIN * 60:
        log(f"Content target reached! Building episode...")
        
        # Build script
        script = build_episode_from_segments()
        if script:
            episode_num = get_latest_episode_num()
            script_file = PODCAST_DIR / f"episode_{episode_num:03d}.md"
            
            with open(script_file, "w") as f:
                f.write(script)
            
            log(f"Written script to {script_file}")
            
            # Generate audio
            duration = generate_audio(script_file)
            
            if duration > 0:
                # Update RSS
                update_rss(episode_num, duration)
                
                # Deploy
                if deploy():
                    # Notify
                    notify_telegram(episode_num, int(duration/60))
                    
                    # Clear staged content after successful episode
                    save_staged_content({"segments": [], "last_updated": None})
                    log("Episode complete, content cleared")
            else:
                log("Audio generation failed")
    else:
        log(f"Need {TARGET_MIN - total_minutes:.1f} more minutes of content")
    
    log("=== Hourly content gathering complete ===")

if __name__ == "__main__":
    main()
