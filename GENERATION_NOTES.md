# Podcast Audio Generation Notes

## Overview
This document describes how to generate high-quality podcast audio from the markdown scripts using Microsoft Edge TTS.

## Voice Configuration (LOCKED IN - Feb 20, 2026)

| Host | Voice | Description |
|------|-------|-------------|
| Nova | `en-GB-SoniaNeural` | Warm British female voice |
| Alloy | `en-US-JennyNeural` | American female voice |

⚠️ **DO NOT CHANGE VOICES WITHOUT EXPLICIT PERMISSION**

## Requirements

### Install Dependencies
```bash
pip install edge-tts
```

### Prerequisites
- `ffmpeg` must be installed (for audio processing)
- Python 3.8+

## Usage

### Generate Audio for an Episode
```bash
cd /Users/tobyglennpeters/.openclaw/workspace/podcast
python generate_audio.py episode_003.md -o episode_003_full
```

This will generate:
- `audio/episode_003_full.mp3` - Full combined audio

### Custom Output Name
```bash
python generate_audio.py episode_003.md -o episode_003_full
```

## Episode Workflow

### Step 1: Write Script
Write the episode script to `episode_XXX.md`

### Step 2: Generate Show Notes (REQUIRED)
Create `show_notes_episode_XXX.md` with:
- Topics covered (with links to sources when available)
- Tips from the episode
- Links mentioned
- Timestamps if applicable
- **Ensure NO overlap with previous episodes**

### Step 3: Generate Audio
```bash
python generate_audio.py episode_XXX.md -o episode_XXX_full
```

### Step 4: Verify Duration
Target: 30-40 minutes per episode
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio/episode_XXX_full.mp3
```

### Step 5: Commit & Push
```bash
git add . && git commit -m "Episode X" && git push origin main
```

## Important Rules

1. **NEVER touch feed.xml without explicit permission**
2. **Finish Episode N before starting Episode N+1**
3. **No content overlap between episodes**
4. **Generate show notes with HTML links for every episode**
5. **Voices are LOCKED - do not change without permission**

## Troubleshooting

### ffmpeg not found
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### Audio sounds distorted
The script automatically resamples to 22kHz. If you need higher quality, modify the `-ar` parameter in the script.

## History

- **2026-02-20**: Voices locked to Sonia (Nova) + Jenny (Alloy)
- **2026-02-18**: Initial setup using edge-tts for Episode 1
