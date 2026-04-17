#!/usr/bin/env python3
"""
Build localized Ken Burns YouTube videos from the crossfire-series episode master.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
VIDEO_ROOT = Path.home() / ".openclaw/workspace/video-workspace/crossfire-series"
VIDEO_PYTHON = VIDEO_ROOT / ".venv" / "bin" / "python3"
FFMPEG = "/opt/homebrew/bin/ffmpeg"
LANGS = ["en", "es", "de", "pt", "hi"]

SHOW_NAMES = {
    "en": "OPENCLAW DAILY",
    "es": "OPENCLAW DAILY ESPAÑOL",
    "de": "OPENCLAW DAILY DEUTSCH",
    "pt": "OPENCLAW DAILY PORTUGUÊS",
    "hi": "OPENCLAW DAILY HINDI",
}

MONTH_NAMES = {
    "en": [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ],
    "es": [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ],
    "de": [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember",
    ],
    "pt": [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    ],
    "hi": [
        "जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून",
        "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर",
    ],
}


def run(cmd):
    subprocess.run(cmd, check=True)


def load_video_config(episode: int) -> dict:
    with open(VIDEO_ROOT / f"ep{episode}" / "config.json") as f:
        return json.load(f)


def load_release_state(episode: int) -> dict:
    state_path = SCRIPTS_DIR / f"release_ep{episode:03d}_state.json"
    if state_path.exists():
        return json.loads(state_path.read_text())
    return {}


def get_audio_path(episode: int, lang: str) -> Path:
    ep_str = f"{episode:03d}"
    if lang == "en":
        return PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    return PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"


def get_episode_date(episode: int) -> datetime.date:
    notes_path = PODCAST_DIR / f"show_notes_episode_{episode:03d}.md"
    content = notes_path.read_text()
    match = re.search(r"\*\*OpenClaw Daily\*\*\s*\|\s*([A-Za-z]+ \d{1,2}, \d{4})\s*\|", content)
    if not match:
        raise RuntimeError(f"Could not parse episode date from {notes_path}")
    return datetime.strptime(match.group(1), "%B %d, %Y").date()


def format_date_for_lang(lang: str, episode_date) -> str:
    month = MONTH_NAMES[lang][episode_date.month - 1]
    if lang == "en":
        return f"{month} {episode_date.day}, {episode_date.year}"
    if lang == "de":
        return f"{episode_date.day}. {month} {episode_date.year}"
    if lang in {"es", "pt"}:
        return f"{episode_date.day} de {month} de {episode_date.year}"
    return f"{episode_date.day} {month} {episode_date.year}"


def strip_title_prefix(title: str) -> str:
    if ": " in title:
        return title.split(": ", 1)[1].strip()
    return title.strip()


def get_display_title(episode: int, lang: str, cfg: dict, state: dict) -> str:
    if lang == "en":
        return cfg["title"].strip()

    meta_title = (
        state.get("translations", {})
        .get(lang, {})
        .get("meta", {})
        .get("title", "")
        .strip()
    )
    if meta_title:
        return strip_title_prefix(meta_title)

    show_notes = PODCAST_DIR / "translations" / lang / f"show_notes_episode_{episode:03d}_{lang}.md"
    if show_notes.exists():
        content = show_notes.read_text()
        title_match = re.search(r"^## Episode Title\s*\n\*\*(.+?)\*\*", content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()

    raise RuntimeError(f"Missing translated title metadata for {lang.upper()} EP{episode:03d}")


def get_output_paths(episode: int, lang: str) -> tuple[Path, Path]:
    outputs_dir = VIDEO_ROOT / f"build/ep{episode}" / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    final_video = outputs_dir / f"openclaw{episode}_kb_publish_{lang}.mp4"
    overlay_png = outputs_dir / f"openclaw{episode}_burnin_overlay_{lang}.png"
    return final_video, overlay_png


def ensure_silent_master(episode: int, cfg: dict) -> Path:
    kb_silent = VIDEO_ROOT / cfg["paths"]["kb_silent"]
    if kb_silent.exists():
        return kb_silent

    filelist = VIDEO_ROOT / f"build/ep{episode}" / "assets" / "kb_clips" / "filelist.txt"
    if not filelist.exists():
        raise FileNotFoundError(f"Missing Ken Burns clip filelist: {filelist}")

    kb_silent.parent.mkdir(parents=True, exist_ok=True)
    try:
        run([
            FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(filelist),
            "-c",
            "copy",
            str(kb_silent),
            "-loglevel",
            "error",
        ])
    except subprocess.CalledProcessError:
        run([
            FFMPEG,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(filelist),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "14",
            "-pix_fmt",
            "yuv420p",
            str(kb_silent),
            "-loglevel",
            "error",
        ])
    return kb_silent


def mux_audio(silent_video: Path, audio: Path, output_video: Path):
    run([
        FFMPEG,
        "-y",
        "-i",
        str(silent_video),
        "-i",
        str(audio),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(output_video),
        "-loglevel",
        "error",
    ])


def apply_burnins(
    episode: int,
    cfg: dict,
    input_video: Path,
    output_video: Path,
    overlay_png: Path,
    title: str,
    show_name: str,
    subtitle: str,
):
    video_python = str(VIDEO_PYTHON) if VIDEO_PYTHON.exists() else sys.executable
    cmd = [
        video_python,
        str(VIDEO_ROOT / "shared" / "apply_burnins.py"),
        "--episode",
        str(episode),
        "--input",
        str(input_video),
        "--output",
        str(output_video),
        "--title",
        title,
        "--show-name",
        show_name,
        "--subtitle",
        subtitle,
        "--review-label",
        "",
        "--overlay-png",
        str(overlay_png),
    ]
    panel_lift = cfg.get("burnin", {}).get("panel_lift")
    if panel_lift is not None:
        cmd.extend(["--panel-lift", str(panel_lift)])
    episode_label = cfg.get("burnin", {}).get("episode_label")
    if episode_label:
        cmd.extend(["--episode-label", str(episode_label)])
    run(cmd)


def build_lang_video(episode: int, lang: str, cfg: dict, state: dict, force: bool = False) -> Path:
    audio_path = get_audio_path(episode, lang)
    if not audio_path.exists():
        raise FileNotFoundError(f"Missing audio for {lang.upper()}: {audio_path}")

    silent_master = ensure_silent_master(episode, cfg)
    final_video, overlay_png = get_output_paths(episode, lang)
    if final_video.exists() and not force and final_video.stat().st_mtime >= audio_path.stat().st_mtime:
        return final_video

    temp_clean = final_video.with_name(f"{final_video.stem}__clean.mp4")
    title = get_display_title(episode, lang, cfg, state)
    subtitle = format_date_for_lang(lang, get_episode_date(episode))
    show_name = SHOW_NAMES[lang]

    mux_audio(silent_master, audio_path, temp_clean)
    apply_burnins(
        episode,
        cfg,
        temp_clean,
        final_video,
        overlay_png,
        title,
        show_name,
        subtitle,
    )
    if temp_clean.exists():
        temp_clean.unlink()
    return final_video


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("episode", type=int)
    parser.add_argument("--lang", choices=LANGS)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    cfg = load_video_config(args.episode)
    state = load_release_state(args.episode)
    langs = [args.lang] if args.lang else LANGS

    for lang in langs:
        video = build_lang_video(args.episode, lang, cfg, state, force=args.force)
        print(f"{lang}:{video}")


if __name__ == "__main__":
    main()
