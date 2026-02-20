# Podcast Audio Generation Notes

## Overview
This document describes how to generate high-quality podcast audio from the markdown scripts using Microsoft Edge TTS.

## Requirements

### Install Dependencies
```bash
pip install edge-tts
```

### Prerequisites
- `ffmpeg` must be installed (for audio processing)
- Python 3.8+

## Voice Configuration (LOCKED IN - Feb 20, 2026)

| Host | Voice | Description |
|------|-------|-------------|
| Nova | `en-GB-SoniaNeural` | Warm British female voice |
| Alloy | `en-US-JennyNeural` | American female voice |

⚠️ DO NOT CHANGE VOICES WITHOUT APPROVAL

### Available Voices
To see all available Edge TTS voices:
```bash
edge-tts --list-voices
```

To filter for British English:
```bash
edge-tts --list-voices | grep "en-GB"
```

## Generating Episodes

### Step 1: Write Script
Write the episode script to `episode_XXX.md`

### Step 2: Generate Show Notes (REQUIRED)
Create `show_notes_episode_XXX.md` with:
- Topics covered (with links to sources when available)
- Tips from the episode
- Links mentioned
- Timestamps if applicable

### Step 3: Generate Audio
```bash
python generate_audio.py episode_XXX.md -o episode_XXX_full
```

This will generate:
- `audio/episode_002.mp3` - Full combined audio
- `audio/episode_002_nova.mp3` - Nova's parts only
- `audio/episode_002_alloy.mp3` - Alloy's parts only

### Custom Output Name
```bash
python generate_audio.py episode_002.md -o episode_002_full
```

## How It Works

1. **Script Parsing**: The script is parsed to extract dialogue segments marked with `[NOVA]:` or `[ALLOY]:` tags.

2. **Voice Generation**: Each segment is converted to audio using Microsoft Edge TTS:
   - Nova segments use `en-GB-SoniaNeural`
   - Alloy segments use `en-GB-RyanNeural`

3. **Audio Processing**: 
   - Edge TTS outputs WebM format with Opus codec
   - Each segment is converted to WAV (22kHz, mono)
   - Segments are concatenated into a single WAV file
   - Final output is encoded as MP3 (128kbps)

## Why Edge TTS?

- **Free**: No API costs
- **High Quality**: Neural voices sound natural
- **No Account Required**: Works without authentication
- **Fast**: Generates audio quickly

## Alternative Voices

If you want to try different voices, here are some alternatives:

### British Female (for Nova)
- `en-GB-SoniaNeural` - Recommended (warm, professional)
- `en-GB-MaisieNeural` - Younger sound
- `en-GB-LibbyNeural` - Alternative

### British Male (for Alloy)
- `en-GB-RyanNeural` - Recommended (neutral, clear)
- `en-GB-ThomasNeural` - Older sound

### American Voices
- `en-US-JennyNeural` - Female
- `en-US-GuyNeural` - Male

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

### Segments not aligning
The concatenation is lossless (PCM). Any gaps or overlaps are preserved from the original TTS output.

## History

- **2026-02-18**: Initial setup using edge-tts for Episode 1
- **2026-02-20**: Documented generation process, created generate_audio.py script
