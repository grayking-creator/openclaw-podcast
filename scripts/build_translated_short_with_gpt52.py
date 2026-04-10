#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

import make_podcast_shorts as shorts_work
import render_youtube_short as short_renderer

PODCAST_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
WORK_DIR = PODCAST_DIR / "content_staging" / "shorts"
DEFAULT_AGENT = "shorts-gpt52"
DEFAULT_METADATA_AGENT = "codex"
WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
LANGUAGE_NAMES = {
    "es": "Latin American Spanish",
    "de": "German",
    "pt": "Brazilian Portuguese",
    "hi": "Hindi",
}
ROMANIZED_LANGS = {"hi"}
MIN_MATCH_SCORE = {
    "es": 0.35,
    "de": 0.35,
    "pt": 0.35,
    "hi": 0.08,
}


def read_json(path: Path) -> dict | list:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def normalize_text(text: str) -> str:
    text = text.replace("’", "'")
    text = re.sub(r"\[.*?\]", " ", text)
    text = re.sub(r"[^0-9A-Za-z\u00C0-\u024F\u0400-\u04FF\u0900-\u097F@#' -]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def word_tokens(text: str) -> list[str]:
    return re.findall(r"[0-9A-Za-z\u00C0-\u024F\u0400-\u04FF\u0900-\u097F']+", normalize_text(text))


def normalize_source_text(text: str) -> str:
    text = text.replace("2020 SIX's", "2026's")
    text = text.replace("2020 SIX", "2026")
    text = text.replace("P-A-N-W", "PANW")
    return re.sub(r"\s+", " ", text).strip()


def call_openclaw_agent(agent: str, prompt: str) -> str:
    proc = subprocess.run(
        ["openclaw", "agent", "--agent", agent, "--json", "--message", prompt],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(proc.stdout)
    try:
        return payload["result"]["payloads"][0]["text"].strip()
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected agent response: {proc.stdout}") from exc


def numeric_tokens(text: str) -> set[str]:
    return set(re.findall(r"\b\d+\b", text))


def needs_retry(source_text: str, translated_text: str) -> bool:
    source_nums = numeric_tokens(source_text)
    target_nums = numeric_tokens(translated_text)
    return not source_nums.issubset(target_nums)


def translate_clip_text(agent: str, lang: str, source_text: str) -> str:
    source_text = normalize_source_text(source_text)
    target_lang = LANGUAGE_NAMES[lang]
    output_style = "romanized Hindi in Latin script" if lang in ROMANIZED_LANGS else target_lang
    prompt = (
        f"Translate this English podcast short clip into natural {output_style} for burned-in captions. "
        "Requirements: preserve meaning closely; preserve all numbers and years exactly as digits; "
        "do not translate brand names like Palo Alto Networks; do not leave English words; keep it concise and spoken; "
        "output plain translated text only, with no notes, labels, or quotes. "
        f"English: {source_text}"
    )
    translated = call_openclaw_agent(agent, prompt)
    if not needs_retry(source_text, translated):
        return translated

    retry_prompt = (
        f"Revise this {output_style} translation so every number and year from the English source remains exactly as digits. "
        "Do not add commentary. Return only the corrected translation.\n\n"
        f"English source: {source_text}\n\n"
        f"Current translation: {translated}"
    )
    retry = call_openclaw_agent(agent, retry_prompt)
    return retry


def metadata_prompt(
    episode: int,
    lang: str,
    clip_text: str,
    episode_title: str,
    full_episode_url: str,
) -> str:
    target_lang = "romanized Hindi in Latin script" if lang in ROMANIZED_LANGS else LANGUAGE_NAMES[lang]
    return (
        f"Write YouTube Shorts metadata in natural {target_lang}. "
        "Return strict JSON with keys title, description, tags. "
        f"Requirements: title under 100 characters, hook-first, no quotes, include OpenClaw Daily EP{episode} and #shorts. "
        "Description format: first line strong hook; second line payoff/context; third line CTA to the full episode URL; "
        "fourth line compact hashtag block. Keep it tight. tags must be a JSON array of 5-8 short strings. "
        f"Episode title: {episode_title}. Full episode URL: {full_episode_url}. Clip transcript: {clip_text}"
    )


def generate_metadata(
    episode: int,
    agent: str,
    lang: str,
    clip_text: str,
    episode_title: str,
    full_episode_url: str,
) -> dict:
    raw = call_openclaw_agent(
        agent,
        metadata_prompt(episode, lang, clip_text, episode_title, full_episode_url),
    )
    match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"Metadata JSON missing from model output: {raw}")
    data = json.loads(match.group(0))
    title = re.sub(r"\s+", " ", str(data["title"]).strip())
    description = str(data["description"]).strip()
    tags = [str(tag).strip() for tag in data.get("tags", []) if str(tag).strip()]
    return {
        "title": title[:100],
        "description": description,
        "tags": tags[:8],
    }


def ensure_transcript(audio_path: Path, transcript_json: Path) -> dict:
    transcript_json.parent.mkdir(parents=True, exist_ok=True)
    wav_path = transcript_json.parent / f"{audio_path.stem}.wav"
    shorts_work.extract_audio(audio_path, wav_path)
    return shorts_work.transcribe_audio(wav_path, transcript_json, WHISPER_MODEL)


def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    a_set = set(a)
    b_set = set(b)
    if not a_set or not b_set:
        return 0.0
    return len(a_set & b_set) / len(a_set | b_set)


def find_best_segment_window(transcript_data: dict, clip_text: str) -> tuple[float, float, float]:
    segments = transcript_data.get("segments", [])
    clip_tokens = word_tokens(clip_text)
    if not clip_tokens:
        raise RuntimeError("Translated clip text produced no tokens")

    best: tuple[float, float, float] | None = None
    for i in range(len(segments)):
        merged_text = ""
        start = float(segments[i]["start"])
        for j in range(i, min(len(segments), i + 18)):
            merged_text = f"{merged_text} {segments[j].get('text', '')}".strip()
            duration = float(segments[j]["end"]) - start
            if duration < 20:
                continue
            if duration > 65:
                break
            score = jaccard(clip_tokens, word_tokens(merged_text))
            if best is None or score > best[2]:
                best = (start, float(segments[j]["end"]), score)
    if best is None:
        raise RuntimeError("Unable to find a matching translated transcript window")
    return best


def anchor_words_for_window(transcript_data: dict, start: float, end: float) -> list[dict]:
    anchors: list[dict] = []
    for segment in transcript_data.get("segments", []):
        seg_start = float(segment.get("start", 0.0))
        seg_end = float(segment.get("end", 0.0))
        if seg_end < start:
            continue
        if seg_start > end:
            break
        for word in segment.get("words") or []:
            word_start = float(word.get("start", 0.0))
            word_end = float(word.get("end", word_start))
            if word_end < start:
                continue
            if word_start > end:
                continue
            token = str(word.get("word", "")).strip()
            if not token:
                continue
            anchors.append({
                "text": token,
                "start": max(0.0, word_start - start),
                "end": max(0.0, word_end - start),
            })
    return anchors


def build_segment_payload(episode: int, clip_text: str, start: float, end: float, lang: str) -> list[dict]:
    titles = {
        "es": "La mayor amenaza interna de la IA",
        "de": "Die groesste Insider-Gefahr durch KI",
        "pt": "A maior ameaca interna da IA",
        "hi": "AI ka sabse bada insider threat",
    }
    return [
        {
            "slug": "clip_01",
            "episode_label": f"EP{episode}",
            "title": titles[lang],
            "transcript": clip_text,
            "start": round(start, 2),
            "duration": round(end - start, 2),
        }
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=int, required=True)
    parser.add_argument("--lang", choices=["es", "de", "pt", "hi"], required=True)
    parser.add_argument("--agent", default=DEFAULT_AGENT)
    parser.add_argument("--metadata-agent", default=DEFAULT_METADATA_AGENT)
    parser.add_argument("--clip-index", type=int, default=0)
    parser.add_argument("--episode-title")
    parser.add_argument("--full-episode-url")
    args = parser.parse_args()

    ep_str = f"{args.episode:03d}"
    selected_path = WORK_DIR / f"episode_{ep_str}" / f"review_renders_ep{args.episode}" / f"episode_{ep_str}_work" / "selected_clips.json"
    selected = read_json(selected_path)[args.clip_index]
    source_text = selected["text"]

    audio_path = AUDIO_DIR / "translations" / args.lang / f"episode_{ep_str}_{args.lang}.mp3"
    cover_art = PODCAST_DIR / "images" / f"episode_{ep_str}_cover_{args.lang}.png"
    transcript_json = WORK_DIR / f"episode_{ep_str}" / "translations" / args.lang / f"episode_{ep_str}_{args.lang}_work" / "transcript.json"
    render_dir = WORK_DIR / f"episode_{ep_str}" / "translations" / args.lang / "rollout_render"
    manifest_path = render_dir / "clip_01_segments.json"
    translation_path = render_dir / "clip_01_translation.txt"
    metadata_path = render_dir / "clip_01_metadata.json"

    if not audio_path.exists():
        raise FileNotFoundError(f"Missing translated audio: {audio_path}")
    if not cover_art.exists():
        raise FileNotFoundError(f"Missing cover art: {cover_art}")

    transcript_data = ensure_transcript(audio_path, transcript_json)
    clip_text = translate_clip_text(args.agent, args.lang, source_text)
    translation_path.parent.mkdir(parents=True, exist_ok=True)
    translation_path.write_text(clip_text)
    start, end, score = find_best_segment_window(transcript_data, clip_text)
    min_score = MIN_MATCH_SCORE[args.lang]
    if score < min_score:
        raise RuntimeError(
            f"Refusing to render {args.lang} short: transcript match score {score:.4f} is below required {min_score:.2f}"
        )
    manifest = build_segment_payload(args.episode, clip_text, start, end, args.lang)
    manifest[0]["anchor_words"] = anchor_words_for_window(transcript_data, start, end)
    write_json(manifest_path, manifest)

    rendered = short_renderer.render_short(
        audio=audio_path,
        transcript=manifest[0]["transcript"],
        episode_label=manifest[0]["episode_label"],
        title=manifest[0]["title"],
        start=float(manifest[0]["start"]),
        duration=float(manifest[0]["duration"]),
        out_dir=render_dir,
        slug=manifest[0]["slug"],
        cover_art=cover_art,
        language=args.lang,
        anchor_words=manifest[0].get("anchor_words"),
    )

    metadata = None
    if args.episode_title and args.full_episode_url:
        metadata = generate_metadata(
            episode=args.episode,
            agent=args.metadata_agent,
            lang=args.lang,
            clip_text=clip_text,
            episode_title=args.episode_title,
            full_episode_url=args.full_episode_url,
        )
        write_json(metadata_path, metadata)

    print(json.dumps({
        "episode": args.episode,
        "lang": args.lang,
        "translation_path": str(translation_path),
        "manifest_path": str(manifest_path),
        "rendered": str(rendered),
        "match_score": round(score, 4),
        "start": round(start, 2),
        "end": round(end, 2),
        "metadata_path": str(metadata_path),
        "metadata_written": bool(metadata),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
