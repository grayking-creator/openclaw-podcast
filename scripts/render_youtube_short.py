#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"
WHISPER = "/opt/homebrew/bin/whisper-cli"
WHISPER_MODEL_EN = "/Users/tobyglennpeters/.openclaw/workspace/models/ggml-base.en.bin"
WHISPER_MODEL_MULTI = "/Users/tobyglennpeters/.openclaw/workspace/models/ggml-base.bin"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_UNICODE = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONT_DEVANAGARI = "/System/Library/Fonts/Supplemental/DevanagariMT.ttc"
WIDTH = 1080
HEIGHT = 1920
FPS = 30


@dataclass
class Word:
    text: str
    start: float
    end: float


def run(cmd: List[str], cwd: Path | None = None) -> None:
    print("+", " ".join(shlex.quote(c) for c in cmd))
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        FFPROBE,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ], text=True)
    return float(out.strip())


def ffmpeg_has_filter(name: str) -> bool:
    out = subprocess.check_output([FFMPEG, "-hide_banner", "-filters"], text=True, stderr=subprocess.STDOUT)
    return name in out


def sec_to_ass(t: float) -> str:
    if t < 0:
        t = 0
    cs = int(round(t * 100))
    h = cs // 360000
    cs %= 360000
    m = cs // 6000
    cs %= 6000
    s = cs // 100
    cs %= 100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def sec_to_ffmpeg(t: float) -> str:
    ms = int(round(t * 1000))
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def norm_text(s: str) -> str:
    s = s.replace("’", "'")
    s = s.replace("—", " ")
    s = s.replace("–", " ")
    s = re.sub(r"\[.*?\]", " ", s)
    s = re.sub(r"[^\w' ]+", " ", s, flags=re.UNICODE)
    s = s.replace("_", " ")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def tokenize_transcript(s: str) -> List[str]:
    s = s.replace("’", "'")
    s = re.sub(r"\[.*?\]", " ", s)
    parts = re.findall(r"[^\W_]+(?:['’][^\W_]+)*|[.,!?;:]", s, flags=re.UNICODE)
    return parts


def choose_whisper_model(language: str, override: str | None = None) -> str:
    if override:
        return override
    if language == "en":
        return WHISPER_MODEL_EN
    return WHISPER_MODEL_MULTI


def choose_font_paths(text: str) -> tuple[str, str]:
    if re.search(r"[\u0900-\u097F]", text):
        return FONT_DEVANAGARI, FONT_DEVANAGARI
    if re.search(r"[^\x00-\x7F]", text):
        return FONT_UNICODE, FONT_UNICODE
    return FONT_BOLD, FONT_REGULAR


def whisper_transcribe(clip_wav: Path, out_base: Path, language: str = "en", model: str | None = None) -> Path:
    run([
        WHISPER,
        "-m", choose_whisper_model(language, model),
        "-l", language,
        "-f", str(clip_wav),
        "-ojf",
        "-of", str(out_base),
        "-np",
    ])
    return out_base.with_suffix(".json")


def load_words(whisper_json: Path) -> List[Word]:
    # Whisper CLI output can occasionally contain malformed byte sequences for
    # non-Latin languages; tolerate decode issues so caption rendering can proceed.
    data = json.loads(whisper_json.read_text(encoding="utf-8", errors="replace"))
    words: List[Word] = []
    for seg in data.get("transcription", []):
        for tok in seg.get("tokens", []):
            txt = tok.get("text", "")
            if txt.startswith("[_"):
                continue
            raw = txt.strip()
            if not raw or raw in ",.!?;:":
                continue
            start = tok["offsets"]["from"] / 1000.0
            end = tok["offsets"]["to"] / 1000.0
            if end <= start:
                end = start + 0.08
            words.append(Word(text=raw, start=start, end=end))
    # merge split wordpieces like special / i / ising => specialising-ish
    merged: List[Word] = []
    i = 0
    while i < len(words):
        cur = words[i]
        text = cur.text
        start = cur.start
        end = cur.end
        while i + 1 < len(words) and words[i + 1].start - end < 0.08 and (
            len(words[i + 1].text) <= 4 or len(text) <= 4
        ):
            nxt = words[i + 1]
            text += nxt.text
            end = nxt.end
            i += 1
        merged.append(Word(text=text, start=start, end=end))
        i += 1
    return merged


def transcript_to_windows(transcript: str) -> List[List[str]]:
    toks = tokenize_transcript(transcript)
    windows: List[List[str]] = []
    cur: List[str] = []
    cur_chars = 0
    for tok in toks:
        is_punct = bool(re.fullmatch(r"[.,!?;:]", tok))
        if is_punct:
            if cur:
                cur[-1] += tok
            if tok in ".!?" and cur:
                windows.append(cur)
                cur = []
                cur_chars = 0
            continue
        cur.append(tok)
        cur_chars += len(tok) + 1
        if len(cur) >= 6 or cur_chars >= 28:
            windows.append(cur)
            cur = []
            cur_chars = 0
    if cur:
        windows.append(cur)
    return windows


def align_windows(transcript: str, words: List[Word]) -> list[dict]:
    norm_words = [norm_text(w.text) for w in words]
    norm_words = [w for w in norm_words if w]
    word_refs = [w for w in words if norm_text(w.text)]
    windows = transcript_to_windows(transcript)
    out = []
    cursor = 0
    for win in windows:
        wanted = [norm_text(x) for x in win]
        wanted = [w for w in wanted if w]
        if not wanted:
            continue
        matched = []
        local = cursor
        for target in wanted:
            found = None
            for j in range(local, min(len(norm_words), local + 12)):
                nw = norm_words[j]
                if nw == target or nw.replace("'", "") == target.replace("'", "") or target in nw or nw in target:
                    found = j
                    break
            if found is None:
                continue
            matched.append(found)
            local = found + 1
        if not matched:
            continue
        cursor = matched[-1] + 1
        tokens = []
        for src_tok, idx in zip(win[:len(matched)], matched):
            ref = word_refs[idx]
            tokens.append({"text": src_tok, "start": ref.start, "end": ref.end})
        out.append({
            "start": tokens[0]["start"],
            "end": max(tokens[-1]["end"], tokens[0]["start"] + 0.18),
            "tokens": tokens,
        })
    return out


def ass_escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")


def build_ass(episode_label: str, title: str, windows: list[dict], duration: float) -> str:
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Episode,Arial,44,&H00F4F6FF,&H00F4F6FF,&H00161A24,&H80000000,1,0,0,0,100,100,1,0,1,2.0,0,8,80,80,120,1
Style: Title,Arial,74,&H00FFFFFF,&H00FFFFFF,&H00161A24,&H80000000,1,0,0,0,100,100,0,0,1,2.6,0,8,90,90,210,1
Style: Caption,Arial,54,&H00AEB8C8,&H00FFFFFF,&H00111721,&HAA000000,1,0,0,0,100,100,0,0,1,3.0,0,2,110,110,230,1
Style: Lane,Arial,54,&H00FFFFFF,&H00FFFFFF,&H00111721,&HAA000000,1,0,0,0,100,100,0,0,3,0,0,2,80,80,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{sec_to_ass(duration)},Episode,,0,0,0,,{ass_escape(episode_label)}
Dialogue: 0,0:00:00.00,{sec_to_ass(duration)},Title,,0,0,0,,{ass_escape(title)}
Dialogue: 0,0:00:00.00,{sec_to_ass(duration)},Lane,,0,0,90,,{{\p1\bord0\shad0\1c&H101827&\alpha&H18&}}m 110 1460 l 970 1460 970 1800 110 1800{{\p0}}
"""
    lines = [header]
    context_words = 1
    for win in windows:
        toks = win["tokens"]
        for i, tok in enumerate(toks):
            start = tok["start"]
            end = toks[i + 1]["start"] if i + 1 < len(toks) else max(tok["end"] + 0.10, tok["start"] + 0.22)
            pieces = []
            for j, item in enumerate(toks):
                text = ass_escape(item["text"])
                if j == i:
                    pieces.append(r"{\b1\1c&HFFFFFF&}" + text + r"{\rCaption}")
                elif abs(j - i) <= context_words:
                    pieces.append(r"{\1c&HE0E7F0&}" + text + r"{\rCaption}")
                else:
                    pieces.append(r"{\1c&H7A8699&}" + text + r"{\rCaption}")
            line = " ".join(pieces)
            lines.append(f"Dialogue: 1,{sec_to_ass(start)},{sec_to_ass(end)},Caption,,0,0,0,,{line}")
    return "\n".join(lines) + "\n"


def generate_background(bg_mp4: Path, duration: float) -> None:
    w, h, fps = WIDTH, HEIGHT, FPS
    frames = int(math.ceil(duration * fps))
    cmd = [
        FFMPEG,
        "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{w}x{h}",
        "-r", str(fps),
        "-i", "-",
        "-an",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "17",
        "-preset", "medium",
        str(bg_mp4),
    ]
    print("+", " ".join(shlex.quote(c) for c in cmd))
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    yy, xx = np.mgrid[0:h, 0:w]
    x = xx / float(w)
    y = yy / float(h)
    for n in range(frames):
        t = n / float(fps)
        wave1 = np.sin(6.4 * x + 4.1 * y + 0.9 * t)
        wave2 = np.sin(-3.2 * x + 8.3 * y - 0.7 * t)
        wave3 = np.cos(10.5 * (x - y) + 0.55 * t)
        flow = (wave1 + wave2 + wave3) / 3.0
        ridge = np.exp(-((y - 0.35 - 0.04 * np.sin(t * 0.35 + x * 4)) ** 2) / 0.015)
        glow = np.exp(-((y - 0.68 - 0.03 * np.cos(t * 0.42 + x * 3.5)) ** 2) / 0.02)
        r = 14 + 20 * (0.5 + 0.5 * np.sin(flow * 2.0 + t * 0.08)) + 70 * ridge + 18 * glow
        g = 18 + 34 * (0.5 + 0.5 * np.cos(flow * 2.3 - t * 0.07)) + 110 * ridge + 26 * glow
        b = 32 + 80 * (0.5 + 0.5 * np.sin(flow * 1.7 + t * 0.11)) + 140 * glow + 35 * ridge
        vignette = 1.0 - 0.38 * (((x - 0.5) ** 2) / 0.25 + ((y - 0.5) ** 2) / 0.25)
        vignette = np.clip(vignette, 0.62, 1.0)
        img = np.dstack([r, g, b]) * vignette[..., None]
        # subtle diagonal sheen
        sheen = 18 * np.clip(np.sin((x * 2.4 + y * 1.2 + t * 0.12) * math.pi), 0, 1)
        img[..., 2] += sheen
        img[..., 1] += sheen * 0.6
        img = np.clip(img, 0, 255).astype(np.uint8)
        proc.stdin.write(img.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("background ffmpeg encode failed")


def make_cover_frame(cover_art: Path) -> np.ndarray:
    cover = Image.open(cover_art).convert("RGB")
    bg = cover.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=28))
    bg = Image.eval(bg, lambda px: int(px * 0.38))

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (4, 8, 16, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(4, 8, 16, 110))
    overlay_draw.rectangle((0, 1320, WIDTH, HEIGHT), fill=(4, 8, 16, 80))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")

    side = 820
    cover_fg = cover.resize((side, side), Image.Resampling.LANCZOS)

    shadow = Image.new("RGBA", (side + 40, side + 40), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((20, 20, side + 20, side + 20), radius=34, fill=(0, 0, 0, 185))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=18))
    bg_rgba = bg.convert("RGBA")
    bg_rgba.alpha_composite(shadow, ((WIDTH - shadow.width) // 2, 116))

    frame_x = (WIDTH - side) // 2
    frame_y = 140
    border = Image.new("RGBA", (side + 20, side + 20), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.rounded_rectangle((0, 0, side + 19, side + 19), radius=34, fill=(238, 242, 247, 255))
    bg_rgba.alpha_composite(border, (frame_x - 10, frame_y - 10))
    bg_rgba.alpha_composite(cover_fg.convert("RGBA"), (frame_x, frame_y))
    return np.array(bg_rgba.convert("RGB"))


def wrap_tokens(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, tokens: list[dict], max_width: int) -> list[list[int]]:
    lines: list[list[int]] = []
    cur: list[int] = []
    cur_width = 0
    space_width = int(draw.textlength(" ", font=font))
    for idx, tok in enumerate(tokens):
        tok_width = int(draw.textlength(tok["text"], font=font))
        next_width = tok_width if not cur else cur_width + space_width + tok_width
        if cur and next_width > max_width:
            lines.append(cur)
            cur = [idx]
            cur_width = tok_width
        else:
            cur.append(idx)
            cur_width = next_width
    if cur:
        lines.append(cur)
    return lines


def render_moviepy_short(
    base_frame: np.ndarray,
    clip_audio: Path,
    windows: list[dict],
    episode_label: str,
    title: str,
    duration: float,
    final_mp4: Path,
    font_bold_path: str,
) -> None:
    try:
        from moviepy import AudioFileClip, VideoClip
    except ImportError:
        from moviepy.editor import AudioFileClip, VideoClip

    title_font = ImageFont.truetype(font_bold_path, 44)
    caption_font = ImageFont.truetype(font_bold_path, 66)
    caption_shadow = (7, 8, 12)
    pill_fill = (10, 18, 30, 220)
    box_fill = (10, 18, 30, 220)
    text_dim = (166, 177, 194)
    text_near = (224, 231, 240)
    text_active = (255, 255, 255)
    lane_left = 88
    lane_right = WIDTH - 88
    lane_top = 1380
    lane_bottom = 1810
    max_text_width = lane_right - lane_left - 56

    measure = ImageDraw.Draw(Image.new("RGB", (WIDTH, HEIGHT)))
    pill_bbox = measure.textbbox((0, 0), episode_label, font=title_font)
    pill_w = pill_bbox[2] - pill_bbox[0] + 48
    pill_h = pill_bbox[3] - pill_bbox[1] + 28

    def active_window(t: float) -> dict | None:
        for win in windows:
            if win["start"] - 0.03 <= t <= win["end"] + 0.25:
                return win
        return None

    def make_frame(t: float) -> np.ndarray:
        img = Image.fromarray(base_frame.copy())
        draw = ImageDraw.Draw(img)

        pill_x = (WIDTH - pill_w) // 2
        pill_y = 1010
        draw.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), radius=22, fill=pill_fill)
        draw.text((pill_x + 24, pill_y + 12), episode_label, font=title_font, fill=(244, 246, 255))

        win = active_window(t)
        if win:
            draw.rounded_rectangle((lane_left, lane_top, lane_right, lane_bottom), radius=30, fill=box_fill)
            tokens = win["tokens"]
            active_idx = None
            for idx, tok in enumerate(tokens):
                if tok["start"] - 0.02 <= t <= tok["end"] + 0.12:
                    active_idx = idx
                    break
            lines = wrap_tokens(draw, caption_font, tokens, max_text_width)
            line_height = 94
            total_height = len(lines) * line_height
            y = lane_top + max(42, ((lane_bottom - lane_top) - total_height) // 2)
            for line in lines:
                widths = [int(draw.textlength(tokens[idx]["text"], font=caption_font)) for idx in line]
                space_width = int(draw.textlength(" ", font=caption_font))
                line_width = sum(widths) + max(0, len(widths) - 1) * space_width
                x = lane_left + ((lane_right - lane_left) - line_width) // 2
                for pos, idx in enumerate(line):
                    word = tokens[idx]["text"]
                    if active_idx == idx:
                        fill = text_active
                    elif active_idx is not None and abs(active_idx - idx) <= 1:
                        fill = text_near
                    else:
                        fill = text_dim
                    draw.text((x + 3, y + 5), word, font=caption_font, fill=caption_shadow)
                    draw.text((x, y), word, font=caption_font, fill=fill)
                    x += widths[pos] + space_width
                y += line_height

        return np.array(img)

    audio_clip = AudioFileClip(str(clip_audio))
    video_clip = VideoClip(make_frame, duration=duration).with_audio(audio_clip)
    video_clip.write_videofile(
        str(final_mp4),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        bitrate="8M",
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
        logger=None,
    )
    video_clip.close()
    audio_clip.close()


def render_short(
    audio: Path,
    transcript: str,
    episode_label: str,
    title: str,
    start: float,
    duration: float,
    out_dir: Path,
    slug: str,
    cover_art: Path | None = None,
    language: str = "en",
    whisper_model: str | None = None,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    clip_audio = out_dir / f"{slug}_clip.wav"
    whisper_base = out_dir / f"{slug}_whisper"
    bg_mp4 = out_dir / f"{slug}_bg.mp4"
    ass_path = out_dir / f"{slug}.ass"
    final_mp4 = out_dir / f"{slug}.mp4"

    run([
        FFMPEG, "-y",
        "-ss", sec_to_ffmpeg(start),
        "-t", sec_to_ffmpeg(duration),
        "-i", str(audio),
        "-ac", "1",
        "-ar", "16000",
        str(clip_audio),
    ])
    whisper_json = whisper_transcribe(clip_audio, whisper_base, language=language, model=whisper_model)
    words = load_words(whisper_json)
    windows = align_windows(transcript, words)
    if not windows:
        raise RuntimeError(f"No caption windows aligned for {slug}")
    actual_duration = probe_duration(clip_audio)
    font_bold_path, _ = choose_font_paths(transcript)
    ass_path.write_text(build_ass(episode_label, title, windows, actual_duration))
    if cover_art is None:
        generate_background(bg_mp4, actual_duration)
    else:
        cover_frame = make_cover_frame(cover_art)
        frame_png = out_dir / f"{slug}_frame.png"
        Image.fromarray(cover_frame).save(frame_png)
    if ffmpeg_has_filter("subtitles"):
        video_input = bg_mp4.name if cover_art is None else frame_png.name
        ffmpeg_cmd = [
            FFMPEG, "-y",
        ]
        if cover_art is not None:
            ffmpeg_cmd.extend(["-loop", "1", "-t", sec_to_ffmpeg(actual_duration)])
        ffmpeg_cmd.extend([
            "-i", video_input,
            "-i", clip_audio.name,
            "-vf", f"subtitles=filename={ass_path.name}",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            final_mp4.name,
        ])
        run(ffmpeg_cmd, cwd=out_dir)
    else:
        if cover_art is None:
            cover_frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        render_moviepy_short(
            cover_frame,
            clip_audio,
            windows,
            episode_label,
            title,
            actual_duration,
            final_mp4,
            font_bold_path,
        )

    # Clean up intermediate artifacts (keep final MP4 and ASS subtitles only)
    for artifact in [clip_audio, whisper_json, bg_mp4]:
        try:
            artifact.unlink(missing_ok=True)
        except Exception:
            pass
    if cover_art is not None:
        frame_png = out_dir / f"{slug}_frame.png"
        frame_png.unlink(missing_ok=True)

    return final_mp4


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--audio", required=True)
    p.add_argument("--segments", required=True, help="JSON file with short definitions")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--cover-art", help="Optional square episode cover for EP0-style short composition")
    p.add_argument("--language", default="en", help="Whisper language code, or 'auto'")
    p.add_argument("--whisper-model", help="Optional whisper model override")
    args = p.parse_args()

    audio = Path(args.audio)
    out_dir = Path(args.out_dir)
    segments = json.loads(Path(args.segments).read_text())
    cover_art = Path(args.cover_art) if args.cover_art else None
    rendered = []
    for seg in segments:
        final = render_short(
            audio=audio,
            transcript=seg["transcript"],
            episode_label=seg["episode_label"],
            title=seg["title"],
            start=float(seg["start"]),
            duration=float(seg["duration"]),
            out_dir=out_dir,
            slug=seg["slug"],
            cover_art=cover_art,
            language=args.language,
            whisper_model=args.whisper_model,
        )
        rendered.append(str(final))
    print(json.dumps({"rendered": rendered}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
