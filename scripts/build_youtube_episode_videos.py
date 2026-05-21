#!/usr/bin/env python3
"""
Build localized Ken Burns YouTube videos from the crossfire-series episode master.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent


def resolve_video_root() -> Path:
    candidates = [
        Path.home() / ".openclaw/workspace/video-workspace/flux-videos",
        Path.home() / ".openclaw/workspace/video-workspace/crossfire-series",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return candidates[-1]


VIDEO_ROOT = resolve_video_root()
VIDEO_PYTHON = VIDEO_ROOT / ".venv" / "bin" / "python3"
FFMPEG = "/opt/homebrew/bin/ffmpeg"
LANGS = ["en", "es", "de", "pt", "hi"]
MAX_AUDIO_SHORTFALL_SECONDS = 2.0

SHOW_NAMES = {
    "en": "AGENTSTACK DAILY",
    "es": "AGENTSTACK DAILY ESPAÑOL",
    "de": "AGENTSTACK DAILY DEUTSCH",
    "pt": "AGENTSTACK DAILY PORTUGUÊS",
    "hi": "AGENTSTACK DAILY HINDI",
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


def ffprobe_duration(path: Path) -> float:
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise RuntimeError(f"ffprobe failed for {path}: {stderr or exc}") from exc
    return float(result.stdout.strip())


def scene_ids_from_filelist(filelist: Path) -> list[int]:
    scene_ids: list[int] = []
    missing_paths: list[str] = []
    unparsable_lines: list[str] = []

    for raw_line in filelist.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue

        path_match = re.match(r"""^file\s+['"](.+?)['"]$""", line)
        if path_match:
            clip_path = Path(path_match.group(1))
            if not clip_path.exists():
                missing_paths.append(str(clip_path))

        scene_match = re.search(r"scene_(\d+)\.mp4", line)
        if not scene_match:
            unparsable_lines.append(line)
            continue
        scene_ids.append(int(scene_match.group(1)))

    if missing_paths:
        preview = ", ".join(missing_paths[:3])
        raise RuntimeError(
            f"Ken Burns filelist references missing clips: {preview}"
            + (" ..." if len(missing_paths) > 3 else "")
        )
    if unparsable_lines:
        preview = "; ".join(unparsable_lines[:3])
        raise RuntimeError(
            f"Ken Burns filelist contains unparsable entries: {preview}"
            + (" ..." if len(unparsable_lines) > 3 else "")
        )

    return scene_ids


def validate_filelist_coverage(filelist: Path, episode: int, expected_scenes: int) -> None:
    scene_ids = scene_ids_from_filelist(filelist)
    if not scene_ids:
        raise RuntimeError(f"Ken Burns filelist is empty for EP{episode:03d}: {filelist}")

    if not expected_scenes:
        return

    expected_ids = list(range(1, expected_scenes + 1))
    counts = Counter(scene_ids)
    duplicates = [sid for sid, count in counts.items() if count > 1]
    missing = [sid for sid in expected_ids if sid not in counts]
    unexpected = [sid for sid in scene_ids if sid < 1 or sid > expected_scenes]

    if missing or duplicates or unexpected or scene_ids != expected_ids:
        details = []
        if missing:
            details.append(f"missing={missing[:10]}")
        if duplicates:
            details.append(f"duplicates={duplicates[:10]}")
        if unexpected:
            details.append(f"unexpected={unexpected[:10]}")
        if scene_ids != expected_ids and not missing and not duplicates and not unexpected:
            first_bad = next(
                (
                    idx + 1,
                    actual,
                    expected,
                )
                for idx, (actual, expected) in enumerate(zip(scene_ids, expected_ids))
                if actual != expected
            )
            details.append(
                f"out_of_order_at_index={first_bad[0]} actual={first_bad[1]} expected={first_bad[2]}"
            )
        raise RuntimeError(
            f"Ken Burns clip coverage mismatch for EP{episode:03d}: {'; '.join(details)}. Filelist: {filelist}"
        )


def validate_audio_coverage(video_path: Path, audio_path: Path, label: str) -> None:
    video_duration = ffprobe_duration(video_path)
    audio_duration = ffprobe_duration(audio_path)
    if audio_duration - video_duration > MAX_AUDIO_SHORTFALL_SECONDS:
        raise RuntimeError(
            f"{label} is too short for its audio: video={video_duration:.2f}s audio={audio_duration:.2f}s path={video_path}"
        )


def duration_delta(path_a: Path, path_b: Path) -> float:
    return abs(ffprobe_duration(path_a) - ffprobe_duration(path_b))


def episode_source_dir(episode: int) -> Path:
    canonical = VIDEO_ROOT / "openclaw-daily" / f"ep{episode}"
    legacy = VIDEO_ROOT / f"ep{episode}"
    if canonical.exists():
        return canonical
    if legacy.exists():
        return legacy
    return canonical


def episode_build_dir(episode: int) -> Path:
    canonical = VIDEO_ROOT / "build" / "openclaw-daily" / f"ep{episode}"
    legacy = VIDEO_ROOT / "build" / f"ep{episode}"
    if canonical.exists() or episode_source_dir(episode).parent.name == "openclaw-daily":
        return canonical
    return legacy


def episode_config_path(episode: int) -> Path:
    return episode_source_dir(episode) / "config.json"


def load_video_config(episode: int) -> dict:
    with open(episode_config_path(episode)) as f:
        return json.load(f)


def load_release_state(episode: int) -> dict:
    state_path = SCRIPTS_DIR / f"release_ep{episode:03d}_state.json"
    if state_path.exists():
        return json.loads(state_path.read_text())
    return {}


def release_state_path(episode: int) -> Path:
    return SCRIPTS_DIR / f"release_ep{episode:03d}_state.json"


def get_audio_path(episode: int, lang: str) -> Path:
    ep_str = f"{episode:03d}"
    if lang == "en":
        return PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    return PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"


def translated_show_notes_path(episode: int, lang: str) -> Path | None:
    if lang == "en":
        return PODCAST_DIR / f"show_notes_episode_{episode:03d}.md"
    path = PODCAST_DIR / "translations" / lang / f"show_notes_episode_{episode:03d}_{lang}.md"
    return path if path.exists() else None


def get_episode_date(episode: int, state: dict | None = None) -> datetime.date:
    notes_path = PODCAST_DIR / f"show_notes_episode_{episode:03d}.md"
    content = notes_path.read_text()
    match = re.search(r"\*\*(?:AgentStack Daily|OpenClaw Daily)\*\*\s*\|\s*([A-Za-z]+ \d{1,2}, \d{4})\s*\|", content)
    if match:
        return datetime.strptime(match.group(1), "%B %d, %Y").date()

    pub_date = (state or {}).get("pub_date", "")
    if pub_date:
        try:
            return parsedate_to_datetime(pub_date).date()
        except Exception:
            pass

    raise RuntimeError(f"Could not parse episode date from {notes_path}; state pub_date is also missing/invalid")


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


OVERLAY_TEXT_TRANSLATIONS = str.maketrans(
    {
        "\u00a0": " ",
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2212": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
    }
)


def sanitize_overlay_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.translate(OVERLAY_TEXT_TRANSLATIONS)
    return re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", normalized)


def get_display_title(episode: int, lang: str, cfg: dict, state: dict) -> str:
    if lang == "en":
        return sanitize_overlay_text(cfg["title"].strip())

    meta_title = (
        state.get("translations", {})
        .get(lang, {})
        .get("meta", {})
        .get("title", "")
        .strip()
    )
    if meta_title:
        return sanitize_overlay_text(strip_title_prefix(meta_title))

    show_notes = PODCAST_DIR / "translations" / lang / f"show_notes_episode_{episode:03d}_{lang}.md"
    if show_notes.exists():
        content = show_notes.read_text()
        title_match = re.search(r"^## Episode Title\s*\n\*\*(.+?)\*\*", content, re.MULTILINE)
        if title_match:
            return sanitize_overlay_text(title_match.group(1).strip())

    raise RuntimeError(f"Missing translated title metadata for {lang.upper()} EP{episode:03d}")


def get_output_paths(episode: int, lang: str) -> tuple[Path, Path]:
    outputs_dir = episode_build_dir(episode) / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    final_video = outputs_dir / f"openclaw{episode}_kb_publish_{lang}.mp4"
    overlay_png = outputs_dir / f"openclaw{episode}_burnin_overlay_{lang}.png"
    return final_video, overlay_png


def get_lang_silent_path(episode: int, lang: str) -> Path:
    outputs_dir = episode_build_dir(episode) / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    if lang == "en":
        return VIDEO_ROOT / load_video_config(episode)["paths"]["kb_silent"]
    return outputs_dir / f"openclaw{episode}_kb_silent_{lang}.mp4"


def latest_input_mtime(episode: int, lang: str, cfg: dict, audio_path: Path) -> float:
    mtimes = [audio_path.stat().st_mtime]

    config_path = episode_config_path(episode)
    if config_path.exists():
        mtimes.append(config_path.stat().st_mtime)

    show_notes = translated_show_notes_path(episode, lang)
    if show_notes and show_notes.exists():
        mtimes.append(show_notes.stat().st_mtime)

    kb_silent = VIDEO_ROOT / cfg["paths"]["kb_silent"]
    if kb_silent.exists():
        mtimes.append(kb_silent.stat().st_mtime)

    for script_path in (
        VIDEO_ROOT / "shared" / "apply_burnins.py",
    ):
        if script_path.exists():
            mtimes.append(script_path.stat().st_mtime)

    # The release state file changes as orchestration progresses, but that should not
    # force us to rebuild already-valid publish videos when the underlying media inputs
    # have not changed.
    return max(mtimes)


def ensure_silent_master(episode: int, cfg: dict) -> Path:
    kb_silent = VIDEO_ROOT / cfg["paths"]["kb_silent"]

    filelist = episode_build_dir(episode) / "assets" / "kb_clips" / "filelist.txt"
    if not filelist.exists():
        run_pipeline = VIDEO_ROOT / "shared" / "run_pipeline.py"
        if run_pipeline.exists():
            subprocess.run(
                [str(VIDEO_PYTHON) if VIDEO_PYTHON.exists() else sys.executable, str(run_pipeline), "--episode", str(episode), "--stage", "kenburns"],
                check=True,
                cwd=str(VIDEO_ROOT),
            )
        if not filelist.exists():
            raise FileNotFoundError(f"Missing Ken Burns clip filelist: {filelist}")

    expected_scenes = int(cfg.get("scene_count") or 0)
    validate_filelist_coverage(filelist, episode, expected_scenes)

    kb_silent.parent.mkdir(parents=True, exist_ok=True)
    en_audio = get_audio_path(episode, "en")
    if kb_silent.exists() and kb_silent.stat().st_mtime >= filelist.stat().st_mtime:
        try:
            if en_audio.exists():
                validate_audio_coverage(kb_silent, en_audio, "Existing KB silent master")
            return kb_silent
        except RuntimeError:
            pass
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


def retime_silent_master(source_video: Path, audio_path: Path, output_video: Path) -> Path:
    source_duration = ffprobe_duration(source_video)
    target_duration = ffprobe_duration(audio_path)
    if source_duration <= 0 or target_duration <= 0:
        raise RuntimeError(
            f"Invalid durations for retime: video={source_duration:.2f}s audio={target_duration:.2f}s"
        )
    ratio = target_duration / source_duration
    run([
        FFMPEG,
        "-y",
        "-i",
        str(source_video),
        "-vf",
        f"setpts={ratio:.10f}*PTS,fps=25",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "14",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(output_video),
        "-loglevel",
        "error",
    ])
    validate_audio_coverage(output_video, audio_path, "Retimed silent master")
    return output_video


def ensure_lang_silent_master(
    episode: int,
    lang: str,
    cfg: dict,
    audio_path: Path,
    required_mtime: float,
) -> Path:
    base_silent = ensure_silent_master(episode, cfg)
    if lang == "en":
        return base_silent

    if duration_delta(base_silent, audio_path) <= MAX_AUDIO_SHORTFALL_SECONDS:
        return base_silent

    lang_silent = get_lang_silent_path(episode, lang)
    if lang_silent.exists() and lang_silent.stat().st_mtime >= required_mtime:
        try:
            validate_audio_coverage(lang_silent, audio_path, f"Existing {lang.upper()} silent master")
            if duration_delta(lang_silent, audio_path) <= MAX_AUDIO_SHORTFALL_SECONDS:
                return lang_silent
        except RuntimeError:
            pass

    return retime_silent_master(base_silent, audio_path, lang_silent)


def mux_audio(silent_video: Path, audio: Path, output_video: Path):
    validate_audio_coverage(silent_video, audio, "Refusing to mux truncated video")
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
        "--config",
        str(episode_config_path(episode)),
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

    final_video, overlay_png = get_output_paths(episode, lang)
    required_mtime = latest_input_mtime(episode, lang, cfg, audio_path)
    if final_video.exists() and not force and final_video.stat().st_mtime >= required_mtime:
        try:
            validate_audio_coverage(final_video, audio_path, "Existing publish video")
            return final_video
        except RuntimeError as exc:
            print(f"Rebuilding {final_video.name}: {exc}")

    silent_master = ensure_lang_silent_master(episode, lang, cfg, audio_path, required_mtime)
    temp_clean = final_video.with_name(f"{final_video.stem}__clean.mp4")
    title = get_display_title(episode, lang, cfg, state)
    subtitle = sanitize_overlay_text(format_date_for_lang(lang, get_episode_date(episode, state)))
    show_name = sanitize_overlay_text(SHOW_NAMES[lang])

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
    validate_audio_coverage(final_video, audio_path, "Final publish video")
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
