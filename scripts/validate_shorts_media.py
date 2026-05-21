#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

PCM_WAV_CODECS = {
    "pcm_s16le",
    "pcm_s24le",
    "pcm_s32le",
    "pcm_f32le",
    "pcm_f64le",
    "pcm_u8",
}
DECODE_ERROR_MARKERS = (
    "Invalid data found when processing input",
    "Error submitting packet",
    "Error parsing",
    "Header missing",
    "Reserved bit set",
    "Prediction is not allowed",
    "channel element",
)


class MediaValidationError(RuntimeError):
    pass


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def _probe(path: Path) -> dict[str, Any]:
    result = _run([
        FFPROBE,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_entries",
        "format=duration,bit_rate:stream=index,codec_type,codec_name,codec_tag_string,codec_tag,bit_rate,duration,sample_rate,channels",
        str(path),
    ])
    if result.returncode != 0:
        raise MediaValidationError(f"ffprobe failed for {path}: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise MediaValidationError(f"ffprobe returned invalid JSON for {path}") from exc


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _measure_volume(path: Path) -> tuple[float | None, float | None, str]:
    result = _run([
        FFMPEG,
        "-hide_banner",
        "-nostdin",
        "-i",
        str(path),
        "-vn",
        "-af",
        "volumedetect",
        "-f",
        "null",
        "-",
    ])
    text = "\n".join(part for part in (result.stdout, result.stderr) if part)
    mean_volume: float | None = None
    max_volume: float | None = None
    for line in text.splitlines():
        if "mean_volume:" in line:
            mean_volume = _to_float(line.split("mean_volume:", 1)[1].split("dB", 1)[0].strip())
        elif "max_volume:" in line:
            max_volume = _to_float(line.split("max_volume:", 1)[1].split("dB", 1)[0].strip())
    return mean_volume, max_volume, text


def validate_media_file(
    path: Path | str,
    *,
    expected_duration: float | None = None,
    expected_tolerance: float = 2.0,
    require_audio: bool = True,
    require_video: bool | None = None,
    require_pcm_wav: bool | None = None,
    min_duration: float = 1.0,
    max_duration: float = 75.0,
    min_audio_bitrate: int = 24_000,
    min_mean_volume_db: float = -50.0,
    min_max_volume_db: float = -35.0,
) -> dict[str, Any]:
    media_path = Path(path)
    errors: list[str] = []
    if not media_path.exists():
        raise MediaValidationError(f"{media_path} does not exist")
    if media_path.stat().st_size <= 0:
        raise MediaValidationError(f"{media_path} is empty")

    if require_video is None:
        require_video = media_path.suffix.lower() in {".mp4", ".mov", ".m4v"}
    if require_pcm_wav is None:
        require_pcm_wav = media_path.suffix.lower() == ".wav"

    probe = _probe(media_path)
    streams = probe.get("streams") or []
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    duration = _to_float((probe.get("format") or {}).get("duration"))

    if duration < min_duration:
        errors.append(f"duration {duration:.2f}s is below {min_duration:.2f}s")
    if duration > max_duration:
        errors.append(f"duration {duration:.2f}s exceeds {max_duration:.2f}s")
    if expected_duration is not None and abs(duration - expected_duration) > expected_tolerance:
        errors.append(
            f"duration {duration:.2f}s differs from expected {expected_duration:.2f}s "
            f"by more than {expected_tolerance:.2f}s"
        )
    if require_video and not video_streams:
        errors.append("missing video stream")
    if require_audio and not audio_streams:
        errors.append("missing audio stream")

    audio_codec = ""
    audio_bitrate = 0
    mean_volume: float | None = None
    max_volume: float | None = None
    if audio_streams:
        audio = audio_streams[0]
        audio_codec = str(audio.get("codec_name") or "")
        audio_bitrate = _to_int(audio.get("bit_rate"))
        if require_pcm_wav and audio_codec not in PCM_WAV_CODECS:
            errors.append(f".wav audio is {audio_codec or 'unknown'}, expected PCM")
        if audio_bitrate and audio_bitrate < min_audio_bitrate:
            errors.append(f"audio bitrate {audio_bitrate} bps is below {min_audio_bitrate} bps")

        mean_volume, max_volume, volume_log = _measure_volume(media_path)
        if any(marker in volume_log for marker in DECODE_ERROR_MARKERS):
            errors.append("audio decoder reported malformed packets")
        if mean_volume is None or max_volume is None:
            errors.append("could not measure audio volume")
        else:
            if mean_volume < min_mean_volume_db:
                errors.append(f"mean volume {mean_volume:.1f} dB is below {min_mean_volume_db:.1f} dB")
            if max_volume < min_max_volume_db:
                errors.append(f"max volume {max_volume:.1f} dB is below {min_max_volume_db:.1f} dB")

    if errors:
        raise MediaValidationError(f"{media_path}: " + "; ".join(errors))

    return {
        "path": str(media_path),
        "duration": duration,
        "audio_codec": audio_codec,
        "audio_bitrate": audio_bitrate,
        "mean_volume_db": mean_volume,
        "max_volume_db": max_volume,
    }


def _recent_files(root: Path, since: float | None) -> list[Path]:
    candidates: list[Path] = []
    for pattern in ("*.mp4", "*_clip.wav"):
        candidates.extend(root.rglob(pattern))
    out: list[Path] = []
    for path in sorted(set(candidates)):
        if since is not None and path.stat().st_mtime < since:
            continue
        out.append(path)
    return out


def _validate_upload_results(root: Path, since: float | None, expected_langs: list[str]) -> dict[str, Any]:
    paths = sorted(root.rglob("upload_results*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if since is not None:
        paths = [p for p in paths if p.stat().st_mtime >= since]
    if not paths:
        raise MediaValidationError(f"{root}: no fresh upload_results*.json found")
    path = paths[0]
    data = json.loads(path.read_text())
    records = data
    if isinstance(data, dict):
        for key in ("upload_results", "uploads"):
            if isinstance(data.get(key), dict):
                records = data[key]
                break
    errors: list[str] = []
    accepted: dict[str, dict[str, Any]] = {}
    for lang in expected_langs:
        item = records.get(lang) if isinstance(records, dict) else None
        if not isinstance(item, dict):
            errors.append(f"{lang}: missing upload result")
            continue
        upload = item.get("upload") if isinstance(item.get("upload"), dict) else item
        status = str(item.get("status") or "").lower()
        upload_status = str(upload.get("status") or "").lower()
        status_text = " ".join(part for part in (status, upload_status) if part)
        video_id = upload.get("video_id") or item.get("video_id")
        url = upload.get("url") or item.get("url")
        has_uploaded_marker = bool(video_id or url)
        has_skip_marker = bool(upload.get("skipped") or item.get("skipped"))
        has_good_status = any(
            word in status_text
            for word in ("upload", "duplicate", "already", "success", "live", "skipped")
        )
        if not has_good_status and not has_uploaded_marker:
            errors.append(f"{lang}: bad status {status or '<empty>'}")
            continue
        if not has_uploaded_marker and not has_skip_marker:
            errors.append(f"{lang}: uploaded status without video_id/url")
            continue
        accepted[lang] = {
            "video_id": video_id,
            "url": url,
            "status": status_text or ("uploaded" if has_uploaded_marker else "skipped"),
        }
    if errors:
        raise MediaValidationError(f"{path}: " + "; ".join(errors))
    return {"path": str(path), "langs": expected_langs, "uploads": accepted}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AgentStack Shorts media before state advancement/upload.")
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--episode-dir", type=Path)
    parser.add_argument("--since", type=float, help="Unix epoch; only validate files modified at or after this time.")
    parser.add_argument("--require-upload-results", action="store_true")
    parser.add_argument("--expected-langs", default="en,es,de,pt,hi")
    args = parser.parse_args()

    paths = list(args.paths)
    if args.episode_dir:
        paths.extend(_recent_files(args.episode_dir, args.since))
    paths = sorted(set(paths))

    errors: list[str] = []
    results: list[dict[str, Any]] = []
    if not paths:
        errors.append("no fresh MP4 or *_clip.wav files found to validate")
    for path in paths:
        try:
            results.append(validate_media_file(path))
        except Exception as exc:
            errors.append(str(exc))

    upload_result: dict[str, Any] | None = None
    if args.require_upload_results:
        expected_langs = [part.strip() for part in args.expected_langs.split(",") if part.strip()]
        try:
            if not args.episode_dir:
                raise MediaValidationError("--require-upload-results needs --episode-dir")
            upload_result = _validate_upload_results(args.episode_dir, args.since, expected_langs)
        except Exception as exc:
            errors.append(str(exc))

    payload = {
        "checked_at_epoch": time.time(),
        "files_checked": results,
        "upload_results": upload_result,
        "errors": errors,
    }
    print(json.dumps(payload, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
