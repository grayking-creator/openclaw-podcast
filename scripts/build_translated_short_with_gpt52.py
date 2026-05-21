#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Iterable, Any

import make_podcast_shorts as shorts_work
import render_youtube_short as short_renderer

PODCAST_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
TRANSLATED_AUDIO_PROXY_BASE = "https://openclaw-audio-proxy.tobypeters.workers.dev/audio"
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


def ensure_translated_audio(ep_str: str, lang: str) -> Path:
    audio_path = AUDIO_DIR / "translations" / lang / f"episode_{ep_str}_{lang}.mp3"
    if audio_path.exists() and audio_path.stat().st_size > 0:
        return audio_path

    audio_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = audio_path.with_suffix(audio_path.suffix + ".tmp")
    url = f"{TRANSLATED_AUDIO_PROXY_BASE}/{lang}/episode_{ep_str}.mp3"
    try:
        urllib.request.urlretrieve(url, tmp_path)
    except Exception as exc:
        tmp_path.unlink(missing_ok=True)
        raise FileNotFoundError(f"Missing translated audio: {audio_path}; proxy fetch failed: {url}") from exc
    if tmp_path.stat().st_size == 0:
        tmp_path.unlink(missing_ok=True)
        raise FileNotFoundError(f"Translated audio proxy returned an empty file: {url}")
    tmp_path.replace(audio_path)
    return audio_path


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


def strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def extract_json_document(raw: str) -> Any:
    cleaned = strip_code_fences(raw)
    decoder = json.JSONDecoder()
    for idx, char in enumerate(cleaned):
        if char not in "{[":
            continue
        try:
            data, _ = decoder.raw_decode(cleaned[idx:])
        except json.JSONDecodeError:
            continue
        if isinstance(data, (dict, list)):
            return data
    raise ValueError("No valid JSON object found")


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
        "Return strict JSON with keys title, alternate_titles, description, hashtags, tag_groups. "
        "Requirements: title must be curiosity-driven, concise/mobile-friendly, and contain no hashtags or quotes; keep it at 65 characters or fewer. "
        "alternate_titles must contain exactly 2 distinct backup title options that follow the same rules. "
        "Description should be short, natural, and end with a line containing about 3 hashtags, not a hashtag in the title. "
        "hashtags must be a JSON array of exactly 3 short hashtag strings for the description only. "
        "tag_groups must be a JSON object with post_specific, niche_specific, and broad arrays of short tags; keep the groups distinct and useful for upload metadata. "
        "Do not invent marketing fluff; stay close to the clip transcript and episode context. "
        f"Episode title: {episode_title}. Full episode URL: {full_episode_url}. Clip transcript: {clip_text}"
    )


def _clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _collapse_inline_whitespace(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text).strip()


def _clean_title(title: str) -> str:
    title = _clean_whitespace(title)
    title = re.sub(r"#\S+", "", title)
    title = title.replace('"', "").replace("“", "").replace("”", "")
    title = re.sub(r"\s+", " ", title).strip(" -:;,.")
    if len(title) > 65:
        title = title[:65].rsplit(" ", 1)[0].rstrip(" -:;,")
    return title


def _clean_tag(tag: str) -> str:
    tag = _clean_whitespace(tag)
    tag = tag.lstrip("#")
    tag = tag.strip(" ,;")
    return tag


def _clean_hashtag(tag: str) -> str:
    cleaned = _clean_tag(tag)
    cleaned = re.sub(r"[^\w\u00C0-\u024F\u0400-\u04FF\u0900-\u097F-]+", "", cleaned)
    return f"#{cleaned}" if cleaned else ""


def _coerce_tag_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    tags: list[str] = []
    for item in value:
        if item is None:
            continue
        cleaned = _clean_tag(str(item))
        if cleaned and cleaned not in tags:
            tags.append(cleaned)
    return tags


def _coerce_tag_groups(value: Any) -> dict[str, list[str]]:
    groups = {"post_specific": [], "niche_specific": [], "broad": []}
    if not isinstance(value, dict):
        return groups
    for key in groups:
        groups[key] = _coerce_tag_list(value.get(key, []))
    return groups


def _flatten_tag_groups(tag_groups: dict[str, list[str]]) -> list[str]:
    flattened: list[str] = []
    for key in ("post_specific", "niche_specific", "broad"):
        for tag in tag_groups.get(key, []):
            if tag not in flattened:
                flattened.append(tag)
    return flattened


def _derive_fallback_tag_groups(tags: list[str]) -> dict[str, list[str]]:
    if not tags:
        return {"post_specific": [], "niche_specific": [], "broad": []}
    post_specific = tags[: min(3, len(tags))]
    niche_specific = tags[len(post_specific) : len(post_specific) + min(3, max(0, len(tags) - len(post_specific)))]
    broad = [tag for tag in tags if tag not in post_specific and tag not in niche_specific]
    return {
        "post_specific": post_specific,
        "niche_specific": niche_specific,
        "broad": broad,
    }


def _coerce_description(description: str, hashtags: list[str]) -> str:
    description = description.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in description.split("\n") if line.strip()]
    content_lines: list[str] = []
    existing_hashtags: list[str] = []
    for line in lines:
        if "#" in line:
            existing_hashtags.extend([part for part in line.split() if part.startswith("#")])
            stripped = line
            for tag in existing_hashtags:
                stripped = stripped.replace(tag, "")
            stripped = stripped.strip()
            if stripped:
                content_lines.append(_collapse_inline_whitespace(stripped))
        else:
            content_lines.append(_collapse_inline_whitespace(line))
    if len(content_lines) < 2:
        content_lines = content_lines[:1]
    chosen_hashtags = []
    for tag in hashtags + existing_hashtags:
        cleaned = _clean_hashtag(tag)
        if cleaned and cleaned not in chosen_hashtags:
            chosen_hashtags.append(cleaned)
        if len(chosen_hashtags) == 3:
            break
    if len(chosen_hashtags) < 3:
        for fallback in ("#OpenClawDaily", "#Shorts", "#AI"):
            if fallback not in chosen_hashtags:
                chosen_hashtags.append(fallback)
            if len(chosen_hashtags) == 3:
                break
    content_lines = content_lines[:3]
    if not content_lines:
        content_lines = ["Watch the clip for the key idea."]
    content_lines.append(" ".join(chosen_hashtags))
    return "\n".join(content_lines)


def repair_metadata_prompt(episode: int, lang: str, raw_output: str, issues: list[str]) -> str:
    target_lang = "romanized Hindi in Latin script" if lang in ROMANIZED_LANGS else LANGUAGE_NAMES[lang]
    issues_text = "; ".join(issues) if issues else "Output did not match the requested metadata shape."
    return (
        f"Repair this YouTube Shorts metadata JSON in natural {target_lang}. "
        "Return strict JSON only, with no markdown fences and no extra text. "
        "Required keys: title, alternate_titles, description, hashtags, tag_groups. "
        "Rules: title must be curiosity-driven, concise/mobile-friendly, and contain no hashtags or quotes; keep it at 65 characters or fewer. "
        "alternate_titles must contain exactly 2 distinct backup title options that follow the same rules. "
        "Description must be short, natural, and end with a line containing exactly 3 hashtags. "
        "hashtags must be an array of exactly 3 short hashtag strings for the description only. "
        "tag_groups must be an object with post_specific, niche_specific, and broad arrays of useful tags; keep the groups distinct. "
        f"Problems found: {issues_text}. "
        f"Original output: {raw_output}"
    )


def generate_metadata(
    episode: int,
    agent: str,
    lang: str,
    clip_text: str,
    episode_title: str,
    full_episode_url: str,
) -> dict:
    raw = call_openclaw_agent(agent, metadata_prompt(episode, lang, clip_text, episode_title, full_episode_url))
    issues: list[str] = []
    try:
        data = extract_json_document(raw)
    except ValueError:
        issues.append("Could not parse any valid JSON object from the model output")
        repair = call_openclaw_agent(agent, repair_metadata_prompt(episode, lang, raw, issues))
        try:
            data = extract_json_document(repair)
        except ValueError as exc:
            raise RuntimeError(f"Metadata JSON missing from model output: {raw}") from exc
    if not isinstance(data, dict):
        issues.append("Parsed metadata was not a JSON object")
        repair = call_openclaw_agent(agent, repair_metadata_prompt(episode, lang, json.dumps(data, ensure_ascii=False), issues))
        data = extract_json_document(repair)
        if not isinstance(data, dict):
            raise RuntimeError(f"Metadata JSON was not an object: {data}")

    title = _clean_title(str(data.get("title", "")))
    if not title:
        issues.append("Missing or empty title")
    alternate_titles = []
    for raw_alt in data.get("alternate_titles", []) if isinstance(data.get("alternate_titles", []), list) else []:
        cleaned = _clean_title(str(raw_alt))
        if cleaned and cleaned not in alternate_titles and cleaned != title:
            alternate_titles.append(cleaned)
        if len(alternate_titles) == 2:
            break

    hashtags = _coerce_tag_list(data.get("hashtags", []))
    hashtags = [_clean_hashtag(tag) for tag in hashtags]
    hashtags = [tag for tag in hashtags if tag]
    tag_groups = _coerce_tag_groups(data.get("tag_groups", {}))
    flat_tags = _coerce_tag_list(data.get("tags", []))
    if not flat_tags:
        flat_tags = _flatten_tag_groups(tag_groups)
    if not flat_tags:
        flat_tags = _coerce_tag_list(data.get("keywords", []))
    if not flat_tags:
        issues.append("Missing tags or tag_groups")
        flat_tags = _coerce_tag_list(hashtags)

    if not tag_groups["post_specific"] and not tag_groups["niche_specific"] and not tag_groups["broad"]:
        tag_groups = _derive_fallback_tag_groups(flat_tags)

    if not hashtags:
        hashtags = []
        for tag in tag_groups["post_specific"] + tag_groups["niche_specific"] + tag_groups["broad"]:
            cleaned = _clean_hashtag(tag)
            if cleaned and cleaned not in hashtags:
                hashtags.append(cleaned)
            if len(hashtags) == 3:
                break
    description = _coerce_description(str(data.get("description", "")), hashtags)
    if len(hashtags) != 3:
        issues.append("Hashtags could not be normalized to exactly 3 items")
    if len(alternate_titles) < 2:
        issues.append("Alternate titles could not be normalized to exactly 2 items")
    if issues:
        repair = call_openclaw_agent(
            agent,
            repair_metadata_prompt(episode, lang, json.dumps(data, ensure_ascii=False), issues),
        )
        try:
            repaired = extract_json_document(repair)
        except ValueError as exc:
            raise RuntimeError(f"Repair output was not valid JSON: {repair}") from exc
        if not isinstance(repaired, dict):
            raise RuntimeError(f"Repair output was not valid JSON: {repair}")
        data = repaired
        title = _clean_title(str(data.get("title", ""))) or title
        alternate_titles = []
        for raw_alt in data.get("alternate_titles", []) if isinstance(data.get("alternate_titles", []), list) else []:
            cleaned = _clean_title(str(raw_alt))
            if cleaned and cleaned not in alternate_titles and cleaned != title:
                alternate_titles.append(cleaned)
            if len(alternate_titles) == 2:
                break
        hashtags = _coerce_tag_list(data.get("hashtags", []))
        hashtags = [_clean_hashtag(tag) for tag in hashtags if _clean_hashtag(tag)]
        tag_groups = _coerce_tag_groups(data.get("tag_groups", {})) or tag_groups
        flat_tags = _coerce_tag_list(data.get("tags", [])) or flat_tags
        if not hashtags:
            hashtags = []
            for tag in tag_groups["post_specific"] + tag_groups["niche_specific"] + tag_groups["broad"]:
                cleaned = _clean_hashtag(tag)
                if cleaned and cleaned not in hashtags:
                    hashtags.append(cleaned)
                if len(hashtags) == 3:
                    break
        description = _coerce_description(str(data.get("description", "")), hashtags)

    tags = _flatten_tag_groups(tag_groups)
    for tag in flat_tags:
        if tag not in tags:
            tags.append(tag)
    if not tags:
        raise RuntimeError(f"Metadata generation produced no tags: {data}")
    if len(alternate_titles) < 2:
        if title:
            alternate_titles.append(f"{title} now")
        if len(alternate_titles) < 2 and tag_groups["post_specific"]:
            alternate_titles.append(_clean_title(tag_groups["post_specific"][0]))
    alternate_titles = [item for item in alternate_titles if item and item != title][:2]
    return {
        "title": title,
        "alternate_titles": alternate_titles,
        "description": description,
        "hashtags": hashtags[:3],
        "tag_groups": tag_groups,
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
            if duration < 12:
                continue
            if duration > 35:
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


def build_segment_title(clip_text: str) -> str:
    first_sentence = re.split(r"(?<=[.!?])\s+", clip_text.strip(), maxsplit=1)[0].strip()
    title = re.sub(r"\s+", " ", first_sentence).strip(" -:;,.")
    if len(title) > 62:
        title = title[:62].rsplit(" ", 1)[0].rstrip(" -:;,")
    return title or "OpenClaw Daily short"


def build_segment_payload(episode: int, clip_text: str, start: float, end: float, lang: str) -> list[dict]:
    return [
        {
            "slug": "clip_01",
            "episode_label": f"EP{episode}",
            "title": build_segment_title(clip_text),
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

    audio_path = ensure_translated_audio(ep_str, args.lang)
    cover_art = PODCAST_DIR / "images" / f"episode_{ep_str}_cover_{args.lang}.png"
    transcript_json = WORK_DIR / f"episode_{ep_str}" / "translations" / args.lang / f"episode_{ep_str}_{args.lang}_work" / "transcript.json"
    render_dir = WORK_DIR / f"episode_{ep_str}" / "translations" / args.lang / "rollout_render"
    manifest_path = render_dir / "clip_01_segments.json"
    translation_path = render_dir / "clip_01_translation.txt"
    metadata_path = render_dir / "clip_01_metadata.json"

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
