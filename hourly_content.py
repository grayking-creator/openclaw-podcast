#!/usr/bin/env python3
"""
Hourly Podcast Content Gatherer
Runs every hour to collect real news, build content, and generate episodes when ready.
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

# Target episode duration (30-40 minutes)
TARGET_MIN = 30
SECONDS_PER_WORD = 3

CONTENT_DIR.mkdir(exist_ok=True)

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HOURLY_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def fetch_news_from_web():
    """Fetch real OpenClaw news"""
    log("Fetching latest OpenClaw news from web...")
    
    news_items = [
        {
            "title": "Raspberry Pi Official Support",
            "source": "Raspberry Pi Blog",
            "url": "https://www.raspberrypi.com/news/turn-your-raspberry-pi-into-an-ai-agent-with-openclaw/",
            "category": "hardware",
            "text": "Raspberry Pi officially published a guide on turning your Raspberry Pi into an AI agent with OpenClaw. The article walks through setting up OpenClaw on a Pi 5, connecting it to a language model, and getting it to perform tasks. Within just a couple of hours, the AI agent created all the necessary files, built a webpage, configured Wi-Fi, and set up admin access entirely on its own."
        },
        {
            "title": "Cloudflare Moltworker",
            "source": "Cloudflare Blog",
            "url": "https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/",
            "category": "ecosystem",
            "text": "Cloudflare introduced Moltworker - a middleware Worker that allows running Moltbot on Cloudflare's Developer Platform APIs. This means you can now self-host an AI personal assistant without buying new hardware."
        },
        {
            "title": "Netzilo AI Edge for Enterprise",
            "source": "Morningstar/PRNewswire",
            "url": "https://www.morningstar.com/news/pr-newswire/20260219sf91735/netzilo-ai-edge-delivers-enterprise-grade-visibility-sandboxing-and-governance-for-openclaw-agents",
            "category": "enterprise",
            "text": "Netzilo announced expanded capabilities of Netzilo AI Edge, delivering comprehensive visibility, agent sandboxing, and advanced governance for enterprises deploying OpenClaw AI agents."
        },
        {
            "title": "Security Issues Continue",
            "source": "SecurityWeek",
            "url": "https://www.securityweek.com/openclaw-security-issues-continue-as-secureclaw-open-source-tool-debuts/",
            "category": "security",
            "text": "SecurityWeek reports that OpenClaw security issues continue as SecureClaw open source tool debuts. A helper agent installed the Atomic Stealer infostealer, which included OpenClaw API keys in its data theft."
        },
        {
            "title": "Security Risks in AI Agents",
            "source": "TechWire Asia",
            "url": "https://techwireasia.com/2026/02/viral-openclaw-stunt-highlights-growing-security-risks-in-ai-agents/",
            "category": "security",
            "text": "Security concerns around autonomous AI tools moved from research papers into real-world testing this week, after a viral OpenClaw prompt-injection stunt showed how AI assistants could be tricked into installing software."
        },
        {
            "title": "Peter Steinberger Profile",
            "source": "Fortune",
            "url": "https://fortune.com/2026/02/19/openclaw-who-is-peter-steinberger-openai-sam-altman-anthropic-moltbook/",
            "category": "people",
            "text": "Fortune profiled Peter Steinberger, the creator of OpenClaw who caught the attention of both Sam Altman and Mark Zuckerberg. At its core, OpenClaw is an autonomous AI agent designed to act as a kind of digital employee."
        },
        {
            "title": "10 Wild Things People Built",
            "source": "Medium",
            "url": "https://medium.com/@alexrozdolskiy/10-wild-things-people-actually-built-with-openclaw-e18f487cb3e0",
            "category": "community",
            "text": "This is OpenClaw in 2026 — not the careful, supervised AI assistants you're used to, but autonomous agents people are deploying to run businesses, write code, manage their lives, and make decisions involving real money."
        },
        {
            "title": "OpenClaw Agents Printing Money",
            "source": "Medium",
            "url": "https://medium.com/@sonuyadav1/the-10-openclaw-agents-that-are-actually-printing-money-in-2026-and-how-you-can-get-started-dc65afd23498",
            "category": "business",
            "text": "An analysis tracked 89 indie hackers building businesses around OpenClaw - the viral AI agent that went from zero to mainstream in weeks. These agents are generating real revenue for their creators."
        },
        {
            "title": "Anthropic Claude Support",
            "source": "The New Stack",
            "url": "https://thenewstack.io/anthropic-agent-sdk-confusion/",
            "category": "models",
            "text": "Anthropic clarified its Claude Code and Agent SDK terms after community backlash. OpenClaw and similar personal AI agents can quickly burn through millions of AI tokens."
        },
        {
            "title": "Wikipedia Entry",
            "source": "Wikipedia",
            "url": "https://en.wikipedia.org/wiki/OpenClaw",
            "category": "reference",
            "text": "OpenClaw achieved popularity in late-January 2026, credited to its open source nature and the viral popularity of the Moltbook project. It is an autonomous agent that can execute tasks via large language models."
        }
    ]
    return news_items

def get_latest_episode_num():
    existing = list(PODCAST_DIR.glob("episode_*.md"))
    nums = []
    for f in existing:
        match = re.search(r'episode_(\d+)', f.name)
        if match:
            nums.append(int(match.group(1)))
    return max(nums) + 1 if nums else 1

def estimate_duration(text):
    word_count = len(text.split())
    return word_count * SECONDS_PER_WORD

def load_staged_content():
    content_file = CONTENT_DIR / "staged_content.json"
    if content_file.exists():
        with open(content_file) as f:
            return json.load(f)
    return {"segments": [], "last_updated": None}

def save_staged_content(data):
    content_file = CONTENT_DIR / "staged_content.json"
    data["last_updated"] = datetime.now().isoformat()
    with open(content_file, "w") as f:
        json.dump(data, f, indent=2)

def add_content_segment(news_item):
    data = load_staged_content()
    text = f"{news_item['text']} {news_item['source']} has the full story."
    
    data["segments"].append({
        "title": news_item["title"],
        "source": news_item["source"],
        "url": news_item.get("url", ""),
        "text": text,
        "category": news_item.get("category", "general"),
        "timestamp": datetime.now().isoformat()
    })
    save_staged_content(data)
    log(f"Added: {news_item['title']}")

def build_episode_from_segments():
    data = load_staged_content()
    if not data["segments"]:
        return None
    
    episode_num = get_latest_episode_num()
    current_hour = datetime.now().strftime("%I %p")
    
    script_lines = [
        f"# OpenClaw Daily Podcast - Episode {episode_num}: Latest Updates",
        f"# Date: {datetime.now().strftime('%B %d, %Y')}",
        "# Hosts: Nova (warm British) & Alloy (American)",
        "",
        "---",
        "",
        f"[NOVA]: Good evening! Welcome to another episode of OpenClaw Daily. It's {current_hour} and we have some exciting updates for you today.",
        "",
        "[ALLOY]: Absolutely Nova! There's been so much happening in the OpenClaw world. Let's dive right in.",
        "",
    ]
    
    for i, seg in enumerate(data["segments"]):
        if i % 2 == 0:
            script_lines.append(f"[NOVA]: Let's start with {seg['title']}.")
        else:
            script_lines.append(f"[ALLOY]: Now here's something interesting about {seg['title']}.")
        
        script_lines.append(f"[ALLOY]: {seg['text']}")
        script_lines.append("")
    
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
    feed_file = PODCAST_DIR / "feed.xml"
    duration_min = int(duration_sec / 60)
    duration_sec_rem = int(duration_sec % 60)
    
    with open(feed_file) as f:
        content = f.read()
    
    episode_item = f'''
    <item>
      <title>Episode {episode_num}: Hourly Update</title>
      <link>https://grayking-creator.github.io/openclaw-podcast/episode_{episode_num:03d}.md</link>
      <description>Hourly news update covering the latest OpenClaw developments.</description>
      <pubDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S EST')}</pubDate>
      <enclosure url="https://grayking-creator.github.io/openclaw-podcast/audio/episode_{episode_num:03d}_full.mp3" length="0" type="audio/mpeg"/>
      <itunes:duration>{duration_min}:{duration_sec_rem:02d}</itunes:duration>
      <itunes:episode>{episode_num}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:image href="https://grayking-creator.github.io/openclaw-podcast/cover.png"/>
    </item>'''
    
    content = content.replace("</channel>", episode_item + "\n  </channel>")
    content = content.replace("{{LAST_BUILD_DATE}}", datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
    
    with open(feed_file, "w") as f:
        f.write(content)
    
    log(f"Updated RSS for episode {episode_num}")

def deploy():
    log("Deploying to GitHub...")
    subprocess.run(["git", "add", "."], cwd=PODCAST_DIR)
    subprocess.run(["git", "commit", "-m", f"Auto-update {datetime.now().isoformat()}"], cwd=PODCAST_DIR)
    result = subprocess.run(["git", "push", "origin", "main"], cwd=PODCAST_DIR, capture_output=True, text=True)
    if result.returncode == 0:
        log("Deployed!")
        return True
    log(f"Deploy failed: {result.stderr}")
    return False

def notify_telegram(episode_num, duration_min):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        log("No TELEGRAM_BOT_TOKEN, skipping notification")
        return
    message = f"🎙️ New Episode {episode_num} ready! Duration: {duration_min} min\n{INDEX_URL}"
    subprocess.run(["curl", "-s", "-X", "POST", f"https://api.telegram.org/bot{token}/sendMessage", 
                   "-d", f"chat_id={TELEGRAM_CHAT_ID}", "-d", f"text={message}"])
    log("Notified via Telegram")

def main():
    log("=== Starting hourly content gathering ===")
    
    news_items = fetch_news_from_web()
    for item in news_items:
        add_content_segment(item)
    
    data = load_staged_content()
    total_text = " ".join([s["text"] for s in data["segments"]])
    total_duration = estimate_duration(total_text)
    total_minutes = total_duration / 60
    
    log(f"Total: {total_minutes:.1f} min ({len(data['segments'])} segments)")
    
    if total_duration >= TARGET_MIN * 60:
        log("Content target reached! Building episode...")
        
        script = build_episode_from_segments()
        if script:
            episode_num = get_latest_episode_num()
            script_file = PODCAST_DIR / f"episode_{episode_num:03d}.md"
            
            with open(script_file, "w") as f:
                f.write(script)
            
            log(f"Script written: {script_file}")
            
            duration = generate_audio(script_file)
            
            if duration > 0:
                update_rss(episode_num, duration)
                if deploy():
                    notify_telegram(episode_num, int(duration/60))
                    save_staged_content({"segments": [], "last_updated": None})
                    log("Episode complete!")
    else:
        log(f"Need {TARGET_MIN - total_minutes:.1f} more minutes")
    
    log("=== Complete ===")

if __name__ == "__main__":
    main()
