#!/usr/bin/env python3
"""
Multilingual podcast TTS generator.
Wraps generate_audio.py with per-language voice overrides.
"""
import sys
import asyncio
import argparse
from pathlib import Path

# Language voice mappings (female Nova / male Alloy)
LANG_VOICES = {
    "es": {"NOVA": "es-ES-ElviraNeural",   "ALLOY": "es-ES-AlvaroNeural"},
    "de": {"NOVA": "de-DE-KatjaNeural",    "ALLOY": "de-DE-ConradNeural"},
    "pt": {"NOVA": "pt-BR-FranciscaNeural","ALLOY": "pt-BR-AntonioNeural"},
    "hi": {"NOVA": "hi-IN-SwaraNeural",    "ALLOY": "hi-IN-MadhurNeural"},
    "en": {"NOVA": "en-GB-SoniaNeural",    "ALLOY": "en-US-JennyNeural"},
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="Path to translated script .md")
    parser.add_argument("--lang", required=True, choices=list(LANG_VOICES.keys()))
    parser.add_argument("-o", "--output", help="Output stem (no extension)")
    args = parser.parse_args()

    # Patch VOICES in generate_audio module
    import generate_audio as ga
    ga.VOICES = LANG_VOICES[args.lang]

    output = args.output or Path(args.script).stem
    asyncio.run(ga.generate_podcast_audio(args.script, output))

if __name__ == "__main__":
    main()
