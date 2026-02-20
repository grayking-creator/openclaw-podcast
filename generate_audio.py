#!/usr/bin/env python3
"""
Podcast TTS Generator using Microsoft Edge TTS
Generates high-quality audio from podcast scripts with alternating voices.
"""

import asyncio
import argparse
import os
import re
import subprocess
import tempfile
from pathlib import Path

# Voice mappings for podcast hosts
# Nova: warm British female voice
# Alloy: neutral male voice
VOICES = {
    "NOVA": "en-GB-SoniaNeural",
    "ALLOY": "en-GB-RyanNeural"
}

AUDIO_DIR = Path(__file__).parent / "audio"


async def generate_audio(text: str, voice: str, output_path: str):
    """Generate audio for a single text segment using edge-tts."""
    from edge_tts import Communicate
    
    communicate = Communicate(text, voice)
    await communicate.save(output_path)


def parse_script(script_path: str) -> list:
    """Parse podcast script and extract dialogue segments."""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by speaker tags
    parts = re.split(r'(\[NOVA\]:|\[ALLOY\]:)', content)
    
    dialogue = []
    for i in range(1, len(parts), 2):
        speaker = parts[i].strip('[]:')
        text = parts[i+1].strip()
        if text and speaker in VOICES:
            dialogue.append((speaker, text))
    
    return dialogue


async def generate_podcast_audio(script_path: str, output_name: str = None):
    """Generate full podcast audio with alternating voices."""
    script_path = Path(script_path)
    
    if output_name is None:
        output_name = script_path.stem
    
    # Parse script
    dialogue = parse_script(script_path)
    print(f"Found {len(dialogue)} dialogue segments")
    
    # Create temp directory for segments
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        segment_files = []
        
        # Generate audio for each segment
        for i, (speaker, text) in enumerate(dialogue):
            voice = VOICES[speaker]
            segment_file = temp_path / f"seg_{i:03d}.webm"
            
            print(f"Generating {speaker} ({voice}): {text[:50]}...")
            await generate_audio(text, voice, str(segment_file))
            segment_files.append((speaker, str(segment_file)))
        
        # Combine all segments using ffmpeg
        # First, convert webm to wav, then concat, then convert to mp3
        
        print("Combining audio segments...")
        
        # Create concat file
        concat_file = temp_path / "concat.txt"
        
        # Convert each segment to a consistent format and list them
        wav_files = []
        for i, (speaker, seg_file) in enumerate(segment_files):
            wav_file = temp_path / f"seg_{i:03d}.wav"
            # Convert webm to wav (edge-tts outputs webm with opus)
            subprocess.run([
                'ffmpeg', '-y', '-i', str(seg_file),
                '-acodec', 'pcm_s16le', '-ar', '22050', '-ac', '1',
                str(wav_file)
            ], capture_output=True)
            wav_files.append(str(wav_file))
            # Add to concat file
            with open(concat_file, 'a') as f:
                f.write(f"file '{wav_file}'\n")
        
        # Concatenate all wav files
        combined_wav = temp_path / "combined.wav"
        subprocess.run([
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat_file),
            '-c', 'copy', str(combined_wav)
        ], capture_output=True)
        
        # Convert to mp3
        output_mp3 = AUDIO_DIR / f"{output_name}.mp3"
        subprocess.run([
            'ffmpeg', '-y', '-i', str(combined_wav),
            '-b:a', '128k', '-ar', '22050',
            str(output_mp3)
        ], capture_output=True)
        
        print(f"✅ Generated: {output_mp3}")
        
        # Also generate separate tracks for each voice
        for speaker in VOICES.keys():
            speaker_segments = [wav for s, wav in zip([s for s, _ in dialogue], wav_files) if s == speaker]
            
            if speaker_segments:
                speaker_concat = temp_path / f"concat_{speaker}.txt"
                with open(speaker_concat, 'w') as f:
                    for wf in speaker_segments:
                        f.write(f"file '{wf}'\n")
                
                combined_speaker_wav = temp_path / f"combined_{speaker}.wav"
                subprocess.run([
                    'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(speaker_concat),
                    '-c', 'copy', str(combined_speaker_wav)
                ], capture_output=True)
                
                output_speaker_mp3 = AUDIO_DIR / f"{output_name}_{speaker.lower()}.mp3"
                subprocess.run([
                    'ffmpeg', '-y', '-i', str(combined_speaker_wav),
                    '-b:a', '128k', '-ar', '22050',
                    str(output_speaker_mp3)
                ], capture_output=True)
                
                print(f"✅ Generated: {output_speaker_mp3}")
        
        return output_mp3


def main():
    parser = argparse.ArgumentParser(description="Generate podcast audio from script")
    parser.add_argument("script", help="Path to podcast script markdown file")
    parser.add_argument("-o", "--output", help="Output filename (without extension)")
    args = parser.parse_args()
    
    asyncio.run(generate_podcast_audio(args.script, args.output))


if __name__ == "__main__":
    main()
