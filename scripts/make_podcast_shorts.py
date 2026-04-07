#!/Users/tobyglennpeters/.codex-video-tools/.venv/bin/python

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shlex
import subprocess
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from moviepy import CompositeVideoClip, ImageClip, VideoFileClip

import mlx_whisper

STOPWORDS = {
    'a','an','and','are','as','at','be','but','by','for','from','had','has','have','he','her','here','hers','him','his','how','i','if','in','into','is','it','its','just','me','my','of','on','or','our','out','she','so','that','the','their','them','there','they','this','to','up','was','we','were','what','when','where','who','why','with','you','your',
}
HOOK_WORDS = {
    'actually','best','biggest','bro','crazy','easy','exactly','finally','first','hack','hard','insane','listen','look','literally','never','nobody','perfect','right','secret','seriously','should','story','thing','truth','wait','watch','win','worst','wow',
    'agent','agents','memory','workflow','release','platform','self-hosting','openai'
}
LOW_VALUE_TERMS = {'audio','camera','hear','hello','mic','mute','okay guys','ready','test','testing'}
CAPTION_FONT = '/System/Library/Fonts/Supplemental/Verdana Bold.ttf'
TITLE_FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
LABEL_FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
FFMPEG = '/opt/homebrew/bin/ffmpeg'
WIDTH = 1080
HEIGHT = 1920
FPS = 30


@dataclass
class Candidate:
    start: float
    end: float
    score: float
    text: str
    reasons: list[str]


def run(cmd: list[str]) -> None:
    print('+', ' '.join(shlex.quote(part) for part in cmd), flush=True)
    subprocess.run(cmd, check=True)


def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip())


def word_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9']+", text.lower())


def extract_audio(input_audio: Path, wav_path: Path) -> None:
    if wav_path.exists():
        return
    run([
        FFMPEG, '-y', '-i', str(input_audio), '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', str(wav_path)
    ])


def transcribe_audio(wav_path: Path, transcript_path: Path, model: str) -> dict:
    if transcript_path.exists():
        return json.loads(transcript_path.read_text())

    info = sf.info(str(wav_path))
    total_duration = float(info.duration)
    window_seconds = 75.0
    all_segments: list[dict] = []
    full_text: list[str] = []
    next_id = 0

    for start in np.arange(0.0, total_duration, window_seconds):
        end = min(total_duration, float(start + window_seconds))
        print(f'Transcribing {start:.1f}-{end:.1f}s', flush=True)
        result = mlx_whisper.transcribe(
            str(wav_path),
            path_or_hf_repo=model,
            word_timestamps=True,
            condition_on_previous_text=False,
            temperature=0.0,
            no_speech_threshold=0.4,
            compression_ratio_threshold=2.2,
            hallucination_silence_threshold=1.5,
            clip_timestamps=[round(float(start), 2), round(float(end), 2)],
        )
        for segment in result.get('segments', []):
            segment = json.loads(json.dumps(segment))
            segment['id'] = next_id
            next_id += 1
            text = normalize_text(segment.get('text', ''))
            if (
                all_segments
                and abs(float(segment['start']) - float(all_segments[-1]['start'])) < 0.2
                and text == normalize_text(all_segments[-1].get('text', ''))
            ):
                continue
            all_segments.append(segment)
            if text:
                full_text.append(text)

    result = {'text': ' '.join(full_text), 'segments': all_segments, 'language': 'en'}
    transcript_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def load_energy(wav_path: Path, bucket_seconds: float = 0.5) -> tuple[np.ndarray, float]:
    audio, sr = sf.read(str(wav_path))
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    hop = max(1, int(sr * bucket_seconds))
    chunks = len(audio) // hop + int(len(audio) % hop != 0)
    padded = np.pad(audio, (0, chunks * hop - len(audio)))
    frames = padded.reshape(chunks, hop)
    rms = np.sqrt(np.mean(np.square(frames), axis=1))
    return rms, bucket_seconds


def energy_slice(rms: np.ndarray, bucket_seconds: float, start: float, end: float) -> np.ndarray:
    a = max(0, int(start / bucket_seconds))
    b = min(len(rms), max(a + 1, int(math.ceil(end / bucket_seconds))))
    return rms[a:b]


def segment_words(segment: dict) -> list[dict]:
    words = []
    for word in segment.get('words') or []:
        token = normalize_text(word.get('word', ''))
        if token:
            words.append({'word': token, 'start': float(word['start']), 'end': float(word['end']), 'probability': float(word.get('probability', 0.0))})
    return words


def build_candidates(segments: list[dict], rms: np.ndarray, bucket_seconds: float) -> list[Candidate]:
    candidates: list[Candidate] = []
    current: list[dict] = []

    def flush() -> None:
        nonlocal current
        if not current:
            return
        start = float(current[0]['start'])
        end = float(current[-1]['end'])
        duration = end - start
        text = normalize_text(' '.join(seg['text'] for seg in current))
        if duration < 14 or len(word_tokens(text)) < 20:
            current = []
            return
        score, reasons = score_window(start, end, text, current, rms, bucket_seconds)
        candidates.append(Candidate(start=start, end=end, score=score, text=text, reasons=reasons))
        current = []

    for segment in segments:
        text = normalize_text(segment.get('text', ''))
        if not text:
            continue
        start = float(segment['start'])
        if current:
            prev = current[-1]
            gap = start - float(prev['end'])
            current_duration = float(prev['end']) - float(current[0]['start'])
            sentence_break = re.search(r'[.!?]$', normalize_text(prev.get('text', ''))) is not None
            if gap > 1.6 or current_duration > 46 or (sentence_break and current_duration > 28):
                flush()
        current.append(segment)
    flush()
    return candidates


def score_window(start: float, end: float, text: str, segments: list[dict], rms: np.ndarray, bucket_seconds: float) -> tuple[float, list[str]]:
    duration = end - start
    tokens = word_tokens(text)
    words = [t for t in tokens if t not in STOPWORDS]
    unique_ratio = len(set(words)) / max(1, len(words))
    word_counts = Counter(words)
    top_word_ratio = (max(word_counts.values()) / max(1, len(words))) if word_counts else 0.0
    bigrams = list(zip(tokens, tokens[1:]))
    bigram_counts = Counter(bigrams)
    top_bigram_ratio = (max(bigram_counts.values()) / max(1, len(bigrams))) if bigram_counts else 0.0
    hook_hits = sum(1 for token in tokens if token in HOOK_WORDS)
    number_hits = sum(1 for token in tokens if token.isdigit())
    question_bonus = text.count('?')
    emphasis_bonus = text.count('!') + len(re.findall(r'\b(no|never|always|literally|actually|finally|exactly)\b', text.lower()))
    low_value_hits = sum(1 for term in LOW_VALUE_TERMS if term in text.lower())
    speech_density = len(tokens) / max(duration, 1.0)
    probs = [float(word.get('probability', 0.0)) for segment in segments for word in (segment.get('words') or []) if word.get('probability') is not None]
    confidence = float(np.mean(probs)) if probs else 0.0
    energy = energy_slice(rms, bucket_seconds, start, end)
    energy_mean = float(np.mean(energy)) if len(energy) else 0.0
    energy_p90 = float(np.percentile(energy, 90)) if len(energy) else 0.0
    energy_var = float(np.std(energy)) if len(energy) else 0.0
    intro_penalty = 0.0  # keep strong openers in play for podcast shorts
    long_penalty = max(0.0, duration - 42.0) * 0.08
    short_penalty = max(0.0, 18.0 - duration) * 0.15
    repetition_penalty = max(0.0, top_word_ratio - 0.22) * 26.0 + max(0.0, top_bigram_ratio - 0.14) * 44.0
    score = (
        unique_ratio * 7.0 + hook_hits * 1.25 + number_hits * 0.6 + question_bonus * 0.9 + emphasis_bonus * 0.45 + speech_density * 1.3 + confidence * 4.0 + energy_mean * 95.0 + energy_p90 * 40.0 + energy_var * 20.0 - low_value_hits * 2.2 - intro_penalty - long_penalty - short_penalty - repetition_penalty
    )
    reasons = [f'duration={duration:.1f}s', f'hooks={hook_hits}', f'density={speech_density:.2f}', f'unique={unique_ratio:.2f}', f'repeat={top_word_ratio:.2f}/{top_bigram_ratio:.2f}', f'energy={energy_mean:.3f}/{energy_p90:.3f}', f'confidence={confidence:.2f}']
    return score, reasons


def overlap(a: Candidate, b: Candidate) -> float:
    return max(0.0, min(a.end, b.end) - max(a.start, b.start))


def content_similarity(a: str, b: str) -> float:
    a_terms = {token for token in word_tokens(a) if token not in STOPWORDS}
    b_terms = {token for token in word_tokens(b) if token not in STOPWORDS}
    if not a_terms or not b_terms:
        return 0.0
    return len(a_terms & b_terms) / len(a_terms | b_terms)


def choose_candidates(candidates: list[Candidate], num_clips: int) -> list[Candidate]:
    picked: list[Candidate] = []
    ranked = sorted(candidates, key=lambda item: item.score, reverse=True)
    for candidate in ranked:
        if any(overlap(candidate, existing) > 5.0 for existing in picked):
            continue
        if any(content_similarity(candidate.text, existing.text) > 0.58 for existing in picked):
            continue
        picked.append(candidate)
        if len(picked) == num_clips:
            return sorted(picked, key=lambda item: item.start)
    return sorted(picked, key=lambda item: item.start)


def candidate_words(transcript: dict, start: float, end: float) -> list[dict]:
    words = []
    for segment in transcript.get('segments', []):
        for word in segment_words(segment):
            if word['end'] < start:
                continue
            if word['start'] > end:
                continue
            words.append(word)
    return words


def group_captions(words: list[dict], start: float, end: float) -> list[dict]:
    captions = []
    current: list[dict] = []

    def flush() -> None:
        nonlocal current
        if not current:
            return
        text = ' '.join(item['word'] for item in current)
        captions.append({'start': max(0.0, current[0]['start'] - start), 'end': min(end - start, current[-1]['end'] - start + 0.1), 'text': normalize_text(text)})
        current = []

    for word in words:
        relative_word = {'word': word['word'], 'start': word['start'], 'end': word['end']}
        if not current:
            current.append(relative_word)
            continue
        current_text = ' '.join(item['word'] for item in current)
        word_count = len(current) + 1
        char_count = len(current_text) + 1 + len(relative_word['word'])
        duration = relative_word['end'] - current[0]['start']
        punctuation_break = bool(re.search(r'[.!?,]$', current[-1]['word']))
        if word_count > 5 or char_count > 28 or duration > 2.1 or (punctuation_break and duration > 0.9):
            flush()
        current.append(relative_word)
    flush()
    return captions


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ''
    for word in words:
        trial = word if not current else f'{current} {word}'
        bbox = draw.textbbox((0, 0), trial, font=font, stroke_width=4)
        if bbox[2] - bbox[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:2]


def caption_image(text: str, width: int = 980) -> Image.Image:
    font = ImageFont.truetype(CAPTION_FONT, 76)
    temp = Image.new('RGBA', (width, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(temp)
    lines = wrap_text(draw, text, font, width - 96)
    line_boxes = [draw.textbbox((0, 0), line, font=font, stroke_width=5) for line in lines]
    line_heights = [box[3] - box[1] for box in line_boxes]
    total_height = sum(line_heights) + 36 * (len(lines) - 1)
    canvas_height = total_height + 120
    image = Image.new('RGBA', (width, canvas_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    bg = (10, 10, 14, 228)
    draw.rounded_rectangle((20, 20, width - 20, canvas_height - 20), radius=34, fill=bg)
    y = 60
    for line, box in zip(lines, line_boxes):
        text_width = box[2] - box[0]
        x = (width - text_width) // 2
        draw.text((x, y), line, font=font, fill=(255, 248, 233, 255), stroke_width=5, stroke_fill=(0, 0, 0, 235))
        y += (box[3] - box[1]) + 36
    return image


def rounded_cover_image(cover_path: Path, width: int = 760) -> Image.Image:
    src = Image.open(cover_path).convert('RGBA')
    ratio = width / src.width
    height = int(src.height * ratio)
    src = src.resize((width, height), Image.LANCZOS)
    radius = 48
    mask = Image.new('L', src.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, src.size[0], src.size[1]), radius=radius, fill=255)
    card = Image.new('RGBA', (width + 70, height + 70), (0, 0, 0, 0))
    shadow = Image.new('RGBA', (width + 70, height + 70), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((22, 22, width + 22, height + 22), radius=radius + 6, fill=(0, 0, 0, 180))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    card.alpha_composite(shadow)
    framed = Image.new('RGBA', (width + 16, height + 16), (245, 248, 255, 255))
    framed_mask = Image.new('L', framed.size, 0)
    ImageDraw.Draw(framed_mask).rounded_rectangle((0, 0, framed.size[0], framed.size[1]), radius=radius + 8, fill=255)
    frame_canvas = Image.new('RGBA', framed.size, (245, 248, 255, 255))
    frame_canvas.putalpha(framed_mask)
    card.alpha_composite(frame_canvas, (27, 27))
    covered = Image.new('RGBA', src.size, (0, 0, 0, 0))
    covered.paste(src, (0, 0), mask)
    card.alpha_composite(covered, (35, 35))
    return card


def header_image(episode_label: str, title: str) -> Image.Image:
    label_font = ImageFont.truetype(LABEL_FONT, 42)
    title_font = ImageFont.truetype(TITLE_FONT, 60)
    canvas = Image.new('RGBA', (960, 360), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    label_box = draw.textbbox((0, 0), episode_label, font=label_font)
    label_w = (label_box[2] - label_box[0]) + 56
    draw.rounded_rectangle((0, 0, label_w, 72), radius=28, fill=(227, 242, 253, 235))
    draw.text((28, 16), episode_label, font=label_font, fill=(12, 18, 31, 255))

    title_lines = wrap_text(draw, title, title_font, 820)
    y = 102
    for line in title_lines:
        box = draw.textbbox((0, 0), line, font=title_font, stroke_width=4)
        draw.text((0, y), line, font=title_font, fill=(250, 252, 255, 255), stroke_width=4, stroke_fill=(6, 10, 18, 215))
        y += (box[3] - box[1]) + 16
    return canvas.crop((0, 0, 940, min(max(y + 8, 170), 340)))


def generate_background(bg_path: Path, duration: float) -> None:
    if bg_path.exists() and bg_path.stat().st_size > 100_000:
        print(f'[bg] reusing existing {bg_path}', flush=True)
        return
    frames = int(math.ceil(duration * FPS))
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    x = xx / WIDTH
    y = yy / HEIGHT
    cmd = [FFMPEG, '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WIDTH}x{HEIGHT}', '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', str(bg_path)]
    print('+', ' '.join(shlex.quote(c) for c in cmd), flush=True)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(frames):
        t = n / FPS
        wave1 = np.sin(5.0 * x + 2.4 * y + 0.8 * t)
        wave2 = np.cos(7.2 * y - 2.8 * x - 0.6 * t)
        wave3 = np.sin(8.8 * (x - y) + 0.35 * t)
        field = (wave1 + wave2 + wave3) / 3.0
        aurora_a = np.exp(-((y - 0.30 - 0.05 * np.sin(0.5 * t + x * 3.8)) ** 2) / 0.010)
        aurora_b = np.exp(-((y - 0.64 - 0.04 * np.cos(0.4 * t + x * 4.6)) ** 2) / 0.014)
        diagonal = np.clip(np.sin((x * 1.8 + y * 1.3 + t * 0.09) * math.pi), 0, 1)
        r = 10 + 18 * (0.5 + 0.5 * np.sin(field * 2.1 + t * 0.05)) + 62 * aurora_a + 18 * diagonal
        g = 14 + 28 * (0.5 + 0.5 * np.cos(field * 2.4 - t * 0.06)) + 96 * aurora_a + 28 * aurora_b + 12 * diagonal
        b = 24 + 74 * (0.5 + 0.5 * np.sin(field * 1.6 + t * 0.08)) + 128 * aurora_b + 22 * diagonal
        vignette = 1.0 - 0.34 * (((x - 0.5) ** 2) / 0.25 + ((y - 0.5) ** 2) / 0.25)
        vignette = np.clip(vignette, 0.64, 1.0)
        img = np.dstack([r, g, b]) * vignette[..., None]
        img = np.clip(img, 0, 255).astype(np.uint8)
        proc.stdin.write(img.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError('background render failed')


def render_podcast_base(audio_path: Path, cover_path: Path, output_path: Path, start: float, end: float, episode_label: str, title: str, bg_path: Path) -> None:
    duration = end - start
    generate_background(bg_path, duration)

    bg = VideoFileClip(str(bg_path))
    cover_img = np.array(rounded_cover_image(cover_path))
    header_img = np.array(header_image(episode_label, title))

    cover_clip = (
        ImageClip(cover_img)
        .with_duration(duration)
        .with_position(('center', 360))
    )
    header_clip = (
        ImageClip(header_img)
        .with_duration(duration)
        .with_position((90, 120))
    )
    composite = CompositeVideoClip([bg, cover_clip, header_clip], size=(WIDTH, HEIGHT))
    composite = composite.with_audio(VideoFileClip(str(bg_path)).audio)
    # attach real clip audio via ffmpeg trim to avoid moviepy decode weirdness
    temp_silent = output_path.with_name(output_path.stem + '_silent.mp4')
    composite.write_videofile(str(temp_silent), codec='libx264', audio=False, preset='medium', fps=30, threads=os.cpu_count() or 8, logger='bar')
    composite.close()
    bg.close()
    run([FFMPEG, '-y', '-ss', f'{start:.3f}', '-t', f'{duration:.3f}', '-i', str(audio_path), '-i', str(temp_silent), '-map', '1:v:0', '-map', '0:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', str(output_path)])
    temp_silent.unlink(missing_ok=True)


def render_captioned_clip(base_video: Path, output_path: Path, captions: list[dict]) -> None:
    clip = VideoFileClip(str(base_video))
    overlays = [clip]
    for caption in captions:
        image = np.array(caption_image(caption['text']))
        caption_clip = (
            ImageClip(image)
            .with_start(caption['start'])
            .with_duration(max(0.2, caption['end'] - caption['start']))
            .with_position(('center', 1480))
        )
        overlays.append(caption_clip)
    final = CompositeVideoClip(overlays, size=clip.size)
    final.audio = clip.audio
    final.write_videofile(str(output_path), codec='libx264', audio_codec='aac', preset='medium', fps=30, threads=os.cpu_count() or 8, logger='bar')
    final.close()
    clip.close()


def save_manifest(path: Path, clips: list[Candidate]) -> None:
    path.write_text(json.dumps([asdict(c) for c in clips], indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-audio', required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--cover', required=True)
    parser.add_argument('--episode-label', required=True)
    parser.add_argument('--title-mode', choices=['auto','manual'], default='auto')
    parser.add_argument('--manual-titles', help='JSON array of titles matching clips when using manual mode')
    parser.add_argument('--model', default='mlx-community/whisper-large-v3-turbo')
    parser.add_argument('--num-clips', type=int, default=2)
    args = parser.parse_args()

    input_audio = Path(args.input_audio).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    cover = Path(args.cover).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = input_audio.stem
    work_dir = output_dir / f'{stem}_work'
    work_dir.mkdir(parents=True, exist_ok=True)
    wav_path = work_dir / f'{stem}.wav'
    transcript_path = work_dir / 'transcript.json'
    manifest_path = work_dir / 'selected_clips.json'

    extract_audio(input_audio, wav_path)
    transcript = transcribe_audio(wav_path, transcript_path, args.model)
    rms, bucket_seconds = load_energy(wav_path)
    candidates = build_candidates(transcript.get('segments', []), rms, bucket_seconds)
    selected = choose_candidates(candidates, args.num_clips)
    save_manifest(manifest_path, selected)

    manual_titles = json.loads(args.manual_titles) if args.manual_titles else []

    for idx, candidate in enumerate(selected, start=1):
        clip_words = candidate_words(transcript, candidate.start, candidate.end)
        captions = group_captions(clip_words, candidate.start, candidate.end)
        base_path = work_dir / f'clip_{idx:02d}_base.mp4'
        bg_path = work_dir / f'clip_{idx:02d}_bg.mp4'
        final_path = output_dir / f'clip_{idx:02d}.mp4'
        title = manual_titles[idx - 1] if idx - 1 < len(manual_titles) else candidate.text.split('.')[0][:52].strip() or f'Short {idx}'
        render_podcast_base(input_audio, cover, base_path, candidate.start, candidate.end, args.episode_label, title, bg_path)
        render_captioned_clip(base_path, final_path, captions)
        print(f'clip_{idx:02d}: {candidate.start:.2f}-{candidate.end:.2f} | {title}')
        # Clean up intermediate videos (keep final clip only)
        for artifact in [base_path, bg_path]:
            try:
                artifact.unlink(missing_ok=True)
            except Exception:
                pass

    # Clean up work_dir WAV (large; transcript JSON is small, keep for reference)
    try:
        wav_path.unlink(missing_ok=True)
    except Exception:
        pass

    print(f'Rendered {len(selected)} clips to {output_dir}')


if __name__ == '__main__':
    main()
