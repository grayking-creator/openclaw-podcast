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
import sys
import tempfile
from pathlib import Path

# Voice mappings for podcast hosts
# Nova: warm British female voice
# Alloy: American female voice
VOICES = {
    "NOVA": "en-GB-SoniaNeural",
    "ALLOY": "en-US-JennyNeural"
}

AUDIO_DIR = Path(__file__).parent / "audio"
PODCAST_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = PODCAST_ROOT / "scripts"
EPISODE_TRANSCRIPT_RE = re.compile(r"episode_\d{3}_transcript(?:_nova)?\.md$")
SPEAKER_MARKER_RE = re.compile(r"^\[(NOVA|ALLOY)\]:", re.MULTILINE)
OUTLINE_LINE_RE = re.compile(
    r"^(#{1,6}\s+.+|---+$|\*{0,2}(Title|Runtime|Producer Notes)\*{0,2}$|\[[0-9:–-]+\].+|[-*]\s+\S+)$",
    re.IGNORECASE,
)


def is_canonical_episode_script(script_path: Path) -> bool:
    return script_path.parent.name == "episodes" and EPISODE_TRANSCRIPT_RE.fullmatch(script_path.name) is not None


def canonical_transcript_path(script_path: Path) -> Path:
    if script_path.name.endswith("_transcript_nova.md"):
        return script_path.with_name(script_path.name.replace("_transcript_nova.md", "_transcript.md"))
    return script_path


def prepare_script_for_generation(script_path: Path) -> Path:
    """
    Fail closed for canonical EN episode scripts.

    Direct audio generation from episode transcripts must pass the same QC gate
    and fresh nova render used by the supported build pipeline.
    """
    if not is_canonical_episode_script(script_path):
        return script_path

    transcript_path = canonical_transcript_path(script_path)
    qc_script = SCRIPTS_DIR / "check_episode.py"
    render_script = SCRIPTS_DIR / "render_nova.py"

    if not transcript_path.exists():
        raise SystemExit(f"❌ Episode transcript not found: {transcript_path}")
    if not qc_script.exists() or not render_script.exists():
        missing = [p.name for p in (qc_script, render_script) if not p.exists()]
        raise SystemExit(
            f"❌ Missing podcast preflight helper(s): {', '.join(missing)}. "
            "Use scripts/build_episode.py from the podcast repo."
        )

    print(f"Running QC preflight for {transcript_path.name}...", flush=True)
    qc_result = subprocess.run([sys.executable, str(qc_script), str(transcript_path)])
    if qc_result.returncode != 0:
        raise SystemExit(
            "❌ Refusing to generate audio from an episode transcript that failed QC.\n"
            "   Fix the transcript and rerun `python3 scripts/build_episode.py <N>`."
        )

    print(f"Rendering fresh nova transcript for {transcript_path.name}...", flush=True)
    render_result = subprocess.run([sys.executable, str(render_script), str(transcript_path)])
    if render_result.returncode != 0:
        raise SystemExit(
            "❌ Failed to render a fresh nova transcript before audio generation.\n"
            "   Rerun `python3 scripts/build_episode.py <N>` after fixing the transcript."
        )

    nova_path = transcript_path.with_name(transcript_path.stem + "_nova.md")
    if not nova_path.exists():
        raise SystemExit(
            f"❌ Expected rendered transcript not found: {nova_path.name}. "
            "Use scripts/build_episode.py from the podcast repo."
        )

    print(f"Using validated transcript render: {nova_path.name}", flush=True)
    return nova_path


async def generate_audio(text: str, voice: str, output_path: str):
    """Generate audio for a single text segment using edge-tts.

    edge-tts occasionally returns transient 503s; we retry with backoff.
    Very short segments can hang intermittently, so we synthesize them inline.
    """
    from edge_tts import Communicate

    cleaned = text.strip()
    if len(cleaned) <= 16 and cleaned[-1:] not in ".!?":
        # Keep very short utterances natural without feeding raw SSML to edge-tts.
        cleaned = cleaned.rstrip(",;:") + "."

    last_err = None
    for attempt in range(1, 6):
        try:
            communicate = Communicate(cleaned, voice)
            await asyncio.wait_for(communicate.save(output_path), timeout=180)
            return
        except Exception as e:
            last_err = e
            # backoff: 2, 4, 8, 16, 20 seconds
            delay = min(20, 2 ** attempt)
            print(f"edge-tts error (attempt {attempt}/5): {e}. Retrying in {delay}s...")
            await asyncio.sleep(delay)

    raise last_err


def normalize_script_content(content: str) -> str:
    content = re.sub(r'^\*\*(NOVA|ALLOY):\*\*', r'[\1]:', content, flags=re.MULTILINE)
    content = re.sub(r'^(NOVA|ALLOY):\s*', r'[\1]: ', content, flags=re.MULTILINE)
    return content


def collect_outline_samples(content: str, limit: int = 5) -> list[str]:
    samples = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if OUTLINE_LINE_RE.match(stripped):
            samples.append(stripped)
        if len(samples) >= limit:
            break
    return samples


def assert_dialogue_transcript(content: str, script_path: str) -> None:
    speaker_markers = SPEAKER_MARKER_RE.findall(content)
    if len(speaker_markers) >= 4:
        return

    outline_samples = collect_outline_samples(content)
    if outline_samples:
        raise SystemExit(
            "❌ Refusing to generate audio from outline-style notes.\n"
            f"   {Path(script_path).name} does not look like a speaker-tagged transcript.\n"
            "   Expected repeated [NOVA]: / [ALLOY]: lines, but found outline markers like:\n"
            f"   - " + "\n   - ".join(outline_samples)
        )

    raise SystemExit(
        "❌ Refusing to generate audio because the script does not contain enough speaker-tagged dialogue.\n"
        f"   Add repeated [NOVA]: / [ALLOY]: lines to {Path(script_path).name}."
    )


def parse_script(script_path: str) -> list:
    """Parse podcast script and extract dialogue segments."""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = normalize_script_content(f.read())

    assert_dialogue_transcript(content, script_path)
    
    # Split by speaker tags
    parts = re.split(r'(\[NOVA\]:|\[ALLOY\]:)', content)
    
    dialogue = []
    for i in range(1, len(parts), 2):
        speaker = parts[i].strip('[]:')
        text = parts[i+1].strip()

        # --- TTS scrub pass (prevents spoken markdown artifacts) ---
        # Strip leading speaker label (e.g. "NOVA: " or "ALLOY: ") from spoken text
        text = re.sub(r'^(NOVA|ALLOY):\s*', '', text)
        # Remove markdown headings like "## Segment ..." or "# Title" that may sit between speaker turns.
        text = re.sub(r'^\s*#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
        # Remove fenced code blocks entirely
        text = re.sub(r'```[\s\S]*?```', '', text, flags=re.MULTILINE)
        text = re.sub(r'\[EMPHASIS\](.*?)\[/EMPHASIS\]', r'\1', text, flags=re.DOTALL)
        text = text.replace('[PAUSE]', '...')
        # Remove leftover markdown emphasis markers
        text = text.replace('**', '')
        # Collapse extra blank lines
        text = re.sub(r'\n{3,}', '\n\n', text).strip()

        # Skip segments that have no actual speakable words (e.g. "......" pause markers)
        has_words = bool(re.search(r'[A-Za-z\u00C0-\u024F\u0900-\u097F\u0600-\u06FF]', text))
        if text and speaker in VOICES and has_words:
            dialogue.append((speaker, text))

    if len(dialogue) < 4:
        raise SystemExit(
            "❌ Refusing to generate audio because the parsed dialogue is too thin.\n"
            f"   Parsed only {len(dialogue)} speakable segments from {Path(script_path).name}."
        )
    
    return dialogue


async def generate_podcast_audio(script_path: str, output_name: str = None):
    """Generate full podcast audio with alternating voices."""
    requested_path = Path(script_path).resolve()

    if output_name is None:
        output_name = requested_path.stem

    script_path = prepare_script_for_generation(requested_path)

    # Parse script
    dialogue = parse_script(str(script_path))
    print(f"Found {len(dialogue)} dialogue segments")

    # --- Narrative lint: prevent false-finish phrasing from slipping through ---
    # These phrases read like an outro, and multiple occurrences create "false finishes".
    # We warn here so production can fix the script before publishing.
    script_text = script_path.read_text(encoding='utf-8', errors='ignore').lower()
    false_finish_markers = [
        'one more thing',
        'one last thing',
        'before we close',
        'now we can close',
        'alright. now we can close',
    ]
    counts = {m: script_text.count(m) for m in false_finish_markers}
    if any(v > 0 for v in counts.values()):
        # Only print markers that occur
        bad = {k: v for k, v in counts.items() if v}
        print(f"WARNING: possible false-finish markers found in script: {bad}")
    
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
    parser = argparse.ArgumentParser(
        description="Generate podcast audio from script (canonical episode transcripts auto-run QC + render_nova)"
    )
    parser.add_argument("script", help="Path to podcast script markdown file")
    parser.add_argument("-o", "--output", help="Output filename (without extension)")
    args = parser.parse_args()
    
    asyncio.run(generate_podcast_audio(args.script, args.output))


if __name__ == "__main__":
    main()
