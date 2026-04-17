#!/usr/bin/env python3
"""
Post-approval OpenClaw Daily release orchestrator.

Flow:
  1. Run rel.phase_setup first.
  2. Launch three parallel lanes:
     - EN publish: rel.phase_en_feed -> rel.phase_publish_en
     - translations: rel.phase_translate -> rel.phase_tts -> rel.phase_covers
     - EN video: bootstrap crossfire episode -> FLUX -> Ken Burns -> EN publish video
  3. As soon as translations finish, run:
     - rel.phase_translated_feeds
     - rel.phase_qc
     - rel.phase_cdn
     - rel.phase_publish_translations
  4. After EN video is done, build translated publish videos.
  5. Run rel.phase_youtube, then rel.phase_discord.

This script intentionally reuses scripts/release_episode.py as the library of
record for podcast release phases and persists its progress into the same state
file, under the "approved_orchestrator" key.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_youtube_episode_videos as video_build
import release_episode as rel


SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
VIDEO_ROOT = Path.home() / ".openclaw/workspace/video-workspace/crossfire-series"
VIDEO_PYTHON = VIDEO_ROOT / ".venv" / "bin" / "python3"
VIDEO_BOOTSTRAP = VIDEO_ROOT / "shared" / "bootstrap_podcast_episode.py"
VIDEO_PIPELINE = VIDEO_ROOT / "shared" / "run_pipeline.py"
PUBLISH_LOCK = threading.Lock()

STEP_SETUP = "setup"
STEP_EN_PUBLISH = "lane_en_publish"
STEP_TRANSLATIONS = "lane_translations"
STEP_POST_TRANSLATION = "post_translation"
STEP_EN_VIDEO = "lane_en_video"
STEP_TRANSLATED_VIDEOS = "translated_videos"
STEP_YOUTUBE = "youtube"
STEP_DISCORD = "discord"

STEP_ORDER = [
    STEP_SETUP,
    STEP_EN_PUBLISH,
    STEP_TRANSLATIONS,
    STEP_POST_TRANSLATION,
    STEP_EN_VIDEO,
    STEP_TRANSLATED_VIDEOS,
    STEP_YOUTUBE,
    STEP_DISCORD,
]


class LaneError(RuntimeError):
    def __init__(self, lane: str, message: str, state: dict[str, Any] | None = None):
        super().__init__(message)
        self.lane = lane
        self.state = state or {}


def log(msg: str) -> None:
    stamp = time.strftime("%H:%M:%S")
    print(f"[{stamp}] {msg}", flush=True)


def post_build_log(ep_num: int, msg: str) -> None:
    try:
        rel.build_log(msg, ep_num)
    except Exception:
        pass


def orchestrator_meta(state: dict[str, Any]) -> dict[str, Any]:
    meta = state.setdefault("approved_orchestrator", {})
    meta.setdefault("completed_steps", [])
    meta.setdefault("lane_results", {})
    meta.setdefault("updated_at", None)
    return meta


def completed_steps(state: dict[str, Any]) -> set[str]:
    return set(orchestrator_meta(state).get("completed_steps", []))


def save_state(ep_num: int, state: dict[str, Any]) -> None:
    orchestrator_meta(state)["updated_at"] = datetime.now(timezone.utc).isoformat()
    rel.save_state(ep_num, state)


def mark_step_complete(ep_num: int, state: dict[str, Any], step: str, details: dict[str, Any] | None = None) -> None:
    meta = orchestrator_meta(state)
    steps = meta.setdefault("completed_steps", [])
    if step not in steps:
        steps.append(step)
    if details:
        meta.setdefault("step_details", {})[step] = details
    save_state(ep_num, state)


def mark_lane_result(state: dict[str, Any], lane: str, status: str, details: dict[str, Any] | None = None) -> None:
    payload = {
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if details:
        payload.update(details)
    orchestrator_meta(state).setdefault("lane_results", {})[lane] = payload


def prune_from_step(state: dict[str, Any], from_step: str) -> None:
    idx = STEP_ORDER.index(from_step)
    keep = {step for step in STEP_ORDER[:idx]}
    meta = orchestrator_meta(state)
    meta["completed_steps"] = [step for step in meta.get("completed_steps", []) if step in keep]
    lane_results = meta.get("lane_results", {})
    meta["lane_results"] = {k: v for k, v in lane_results.items() if k in keep}
    step_details = meta.get("step_details", {})
    meta["step_details"] = {k: v for k, v in step_details.items() if k in keep}


def merge_release_state(base: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    if not incoming:
        return base
    for key, value in incoming.items():
        if key == "approved_orchestrator":
            continue
        if key == "completed_phases":
            existing = list(base.get("completed_phases", []))
            seen = set(existing)
            for phase in value or []:
                if phase not in seen:
                    existing.append(phase)
                    seen.add(phase)
            base["completed_phases"] = existing
            continue
        if key == "translations":
            base["translations"] = copy.deepcopy(value)
            continue
        base[key] = copy.deepcopy(value)
    return base


def run_streaming(cmd: list[str], cwd: Path | None = None) -> None:
    rendered = " ".join(str(part) for part in cmd)
    log(f"$ {rendered}")
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def paragraph_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", text)
    total = 0
    for block in blocks:
        collapsed = " ".join(line.strip() for line in block.splitlines() if line.strip())
        if collapsed:
            total += 1
    return total


def ensure_crossfire_bootstrap(ep_num: int, state: dict[str, Any]) -> None:
    ep_dir = VIDEO_ROOT / f"ep{ep_num}"
    config_path = ep_dir / "config.json"
    story_path = ep_dir / "story.py"
    narr_path = ep_dir / "narration.txt"

    if config_path.exists() and story_path.exists() and narr_path.exists():
        log(f"[ EN VIDEO ] Crossfire ep{ep_num} already bootstrapped")
        return

    existing = [path.name for path in (config_path, story_path, narr_path) if path.exists()]
    if existing:
        raise RuntimeError(
            f"Partial crossfire bootstrap exists in {ep_dir} ({', '.join(existing)}). "
            "Refusing to overwrite it automatically."
        )

    if not VIDEO_BOOTSTRAP.exists():
        raise FileNotFoundError(f"Missing crossfire bootstrap script: {VIDEO_BOOTSTRAP}")
    if not VIDEO_PYTHON.exists():
        raise FileNotFoundError(f"Missing crossfire venv python: {VIDEO_PYTHON}")

    ep_str = f"{ep_num:03d}"
    transcript_path = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript_nova.md"
    audio_path = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    if not transcript_path.exists():
        raise FileNotFoundError(f"Missing EN transcript for crossfire bootstrap: {transcript_path}")
    if not audio_path.exists():
        raise FileNotFoundError(f"Missing EN audio for crossfire bootstrap: {audio_path}")

    meta = rel.get_en_release_metadata(ep_num, state)
    scene_count = paragraph_count(transcript_path)
    if scene_count < 2:
        raise RuntimeError(f"Transcript only produced {scene_count} scene(s); need at least 2 for split FLUX generation")
    split_scene = scene_count // 2
    if split_scene < 1 or split_scene >= scene_count:
        raise RuntimeError(f"Computed invalid split scene {split_scene} for {scene_count} scenes")

    log(f"[ EN VIDEO ] Bootstrapping crossfire ep{ep_num} ({scene_count} scenes, split {split_scene}/{scene_count - split_scene})")
    run_streaming([
        str(VIDEO_PYTHON),
        str(VIDEO_BOOTSTRAP),
        "--episode", str(ep_num),
        "--title", meta["episode_title"],
        "--transcript", str(transcript_path),
        "--direct-audio", str(audio_path),
        "--split-scene", str(split_scene),
        "--root", str(VIDEO_ROOT),
    ], cwd=VIDEO_ROOT)


def run_crossfire_stage(ep_num: int, stage: str) -> None:
    if not VIDEO_PIPELINE.exists():
        raise FileNotFoundError(f"Missing crossfire pipeline: {VIDEO_PIPELINE}")
    if not VIDEO_PYTHON.exists():
        raise FileNotFoundError(f"Missing crossfire venv python: {VIDEO_PYTHON}")
    run_streaming([
        str(VIDEO_PYTHON),
        str(VIDEO_PIPELINE),
        "--episode", str(ep_num),
        "--stage", stage,
    ], cwd=VIDEO_ROOT)


def build_publish_video(ep_num: int, lang: str, force: bool = False) -> Path:
    cfg = video_build.load_video_config(ep_num)
    state = video_build.load_release_state(ep_num)
    return video_build.build_lang_video(ep_num, lang, cfg, state, force=force)


def build_translated_publish_videos(ep_num: int) -> dict[str, str]:
    outputs: dict[str, str] = {}
    for lang in rel.LANGS:
        log(f"[ VIDEO / {lang.upper()} ] Building localized publish video...")
        path = build_publish_video(ep_num, lang)
        outputs[lang] = str(path)
        log(f"[ VIDEO / {lang.upper()} ] ✅ {path}")
    return outputs


def en_publish_lane(ep_num: int, state: dict[str, Any], pub_date: str) -> dict[str, Any]:
    lane_state = copy.deepcopy(state)
    try:
        log("[ LANE / EN PUBLISH ] Starting...")
        lane_state = rel.phase_en_feed(ep_num, lane_state, pub_date)
        with PUBLISH_LOCK:
            lane_state = rel.phase_publish_en(ep_num, lane_state)
        log("[ LANE / EN PUBLISH ] Complete")
        return lane_state
    except Exception as exc:
        raise LaneError(STEP_EN_PUBLISH, str(exc), lane_state) from exc


def translation_lane(ep_num: int, state: dict[str, Any]) -> dict[str, Any]:
    lane_state = copy.deepcopy(state)
    try:
        log("[ LANE / TRANSLATIONS ] Starting...")
        lane_state = rel.phase_translate(ep_num, lane_state)
        lane_state = rel.phase_tts(ep_num, lane_state)
        lane_state = rel.phase_covers(ep_num, lane_state)
        log("[ LANE / TRANSLATIONS ] Complete")
        return lane_state
    except Exception as exc:
        raise LaneError(STEP_TRANSLATIONS, str(exc), lane_state) from exc


def en_video_lane(ep_num: int, state: dict[str, Any]) -> dict[str, Any]:
    lane_state = copy.deepcopy(state)
    try:
        log("[ LANE / EN VIDEO ] Starting...")
        ensure_crossfire_bootstrap(ep_num, lane_state)
        run_crossfire_stage(ep_num, "flux")
        run_crossfire_stage(ep_num, "kenburns")
        video_path = build_publish_video(ep_num, "en")
        log(f"[ LANE / EN VIDEO ] ✅ {video_path}")
        return {
            "video_outputs": {
                "en": str(video_path),
            }
        }
    except Exception as exc:
        raise LaneError(STEP_EN_VIDEO, str(exc), lane_state) from exc


def run_post_translation(ep_num: int, state: dict[str, Any], pub_date: str) -> dict[str, Any]:
    log("[ POST TRANSLATION ] Starting...")
    post_build_log(ep_num, "⏳ [POST TRANSLATION] starting…")
    state = rel.phase_translated_feeds(ep_num, state, pub_date)
    save_state(ep_num, state)
    state = rel.phase_qc(ep_num, state)
    save_state(ep_num, state)
    state = rel.phase_cdn(ep_num, state)
    save_state(ep_num, state)
    with PUBLISH_LOCK:
        state = rel.phase_publish_translations(ep_num, state)
    save_state(ep_num, state)
    post_build_log(ep_num, "✅ [POST TRANSLATION] complete")
    log("[ POST TRANSLATION ] Complete")
    return state


def run_step(ep_num: int, state: dict[str, Any], step: str, label: str, fn, *args) -> dict[str, Any]:
    log(f"[ {label} ] Starting...")
    post_build_log(ep_num, f"⏳ [{label}] starting…")
    state = fn(ep_num, state, *args)
    mark_step_complete(ep_num, state, step)
    post_build_log(ep_num, f"✅ [{label}] complete")
    log(f"[ {label} ] Complete")
    return state


def format_lane_errors(errors: dict[str, BaseException]) -> str:
    lines = []
    for lane, exc in errors.items():
        lines.append(f"{lane}: {exc}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenClaw Daily approved-release orchestrator")
    parser.add_argument("episode", type=int, help="Episode number (e.g. 33)")
    _today = datetime.now(timezone.utc).strftime("%a, %d %b %Y 18:00:00 +0000")
    parser.add_argument(
        "--pub-date",
        default=_today,
        help="RSS pubDate string (default: today at 18:00 UTC)",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear only this orchestrator's progress markers and keep existing release state",
    )
    parser.add_argument(
        "--from-step",
        choices=STEP_ORDER,
        help="Rewind this orchestrator from the chosen step onward before running",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ep_num = args.episode
    ep_str = f"{ep_num:03d}"

    state = rel.load_state(ep_num)
    if args.reset:
        state.pop("approved_orchestrator", None)
    if args.from_step:
        prune_from_step(state, args.from_step)
    save_state(ep_num, state)

    log(f"\n{'=' * 68}")
    log(f"OpenClaw Daily — EP{ep_str} Approved Release")
    log(f"{'=' * 68}\n")
    post_build_log(ep_num, "🚀 Approved release orchestrator started")

    try:
        if STEP_SETUP not in completed_steps(state):
            state = run_step(ep_num, state, STEP_SETUP, "SETUP", rel.phase_setup)
        else:
            log("[ SETUP ] Already complete, skipping")

        lane_errors: dict[str, BaseException] = {}
        futures: dict[Any, str] = {}

        with ThreadPoolExecutor(max_workers=3, thread_name_prefix=f"ep{ep_str}-approved") as executor:
            if STEP_EN_PUBLISH not in completed_steps(state):
                futures[executor.submit(en_publish_lane, ep_num, state, args.pub_date)] = STEP_EN_PUBLISH
            else:
                log("[ LANE / EN PUBLISH ] Already complete, skipping")

            if STEP_TRANSLATIONS not in completed_steps(state):
                futures[executor.submit(translation_lane, ep_num, state)] = STEP_TRANSLATIONS
            else:
                log("[ LANE / TRANSLATIONS ] Already complete, skipping")

            if STEP_EN_VIDEO not in completed_steps(state):
                futures[executor.submit(en_video_lane, ep_num, state)] = STEP_EN_VIDEO
            else:
                log("[ LANE / EN VIDEO ] Already complete, skipping")

            if STEP_TRANSLATIONS in completed_steps(state) and STEP_POST_TRANSLATION not in completed_steps(state):
                state = run_step(
                    ep_num,
                    state,
                    STEP_POST_TRANSLATION,
                    "POST TRANSLATION",
                    run_post_translation,
                    args.pub_date,
                )

            for future in as_completed(futures):
                lane = futures[future]
                try:
                    result = future.result()
                except LaneError as exc:
                    if exc.state:
                        state = merge_release_state(state, exc.state)
                        save_state(ep_num, state)
                    lane_errors[lane] = exc
                    mark_lane_result(state, lane, "failed", {"error": str(exc)})
                    save_state(ep_num, state)
                    post_build_log(ep_num, f"❌ [{lane}] FAILED: {exc}")
                    log(f"[ {lane} ] FAILED: {exc}")
                except Exception as exc:
                    lane_errors[lane] = exc
                    mark_lane_result(state, lane, "failed", {"error": str(exc)})
                    save_state(ep_num, state)
                    post_build_log(ep_num, f"❌ [{lane}] FAILED: {exc}")
                    log(f"[ {lane} ] FAILED: {exc}")
                else:
                    if isinstance(result, dict):
                        state = merge_release_state(state, result)
                    mark_lane_result(state, lane, "complete")
                    mark_step_complete(ep_num, state, lane)
                    post_build_log(ep_num, f"✅ [{lane}] complete")
                    log(f"[ {lane} ] Complete")

                    if lane == STEP_EN_VIDEO and isinstance(result, dict):
                        outputs = result.get("video_outputs")
                        if outputs:
                            mark_lane_result(state, lane, "complete", {"video_outputs": outputs})
                            save_state(ep_num, state)

                    if lane == STEP_TRANSLATIONS and STEP_POST_TRANSLATION not in completed_steps(state):
                        state = run_step(
                            ep_num,
                            state,
                            STEP_POST_TRANSLATION,
                            "POST TRANSLATION",
                            run_post_translation,
                            args.pub_date,
                        )

        if lane_errors:
            raise RuntimeError(format_lane_errors(lane_errors))

        if STEP_EN_VIDEO not in completed_steps(state):
            raise RuntimeError("EN video lane did not complete; refusing to build translated publish videos")
        if STEP_POST_TRANSLATION not in completed_steps(state):
            raise RuntimeError("Post-translation finalize did not complete; refusing to continue to video + YouTube")

        if STEP_TRANSLATED_VIDEOS not in completed_steps(state):
            outputs = build_translated_publish_videos(ep_num)
            mark_step_complete(ep_num, state, STEP_TRANSLATED_VIDEOS, {"video_outputs": outputs})
            post_build_log(ep_num, "✅ [TRANSLATED VIDEOS] complete")
        else:
            log("[ TRANSLATED VIDEOS ] Already complete, skipping")

        if STEP_YOUTUBE not in completed_steps(state):
            state = run_step(ep_num, state, STEP_YOUTUBE, "YOUTUBE", rel.phase_youtube)
        else:
            log("[ YOUTUBE ] Already complete, skipping")

        if STEP_DISCORD not in completed_steps(state):
            state = run_step(ep_num, state, STEP_DISCORD, "DISCORD", rel.phase_discord)
        else:
            log("[ DISCORD ] Already complete, skipping")

        log(f"\n{'=' * 68}")
        log(f"✅ EP{ep_str} approved release complete")
        log(f"  Website: https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/")
        log(f"  Feed: https://clawdassistant85-netizen.github.io/openclaw-podcast/feed.xml")
        log(f"{'=' * 68}")
        post_build_log(ep_num, f"🎙️ Approved release complete — <https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/>")
        return 0

    except Exception as exc:
        log(f"\n❌ Approved release failed: {exc}")
        trace = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        post_build_log(ep_num, f"❌ Approved release failed: {trace}")
        save_state(ep_num, state)
        return 1


if __name__ == "__main__":
    sys.exit(main())
