#!/usr/bin/env python3
"""
Post-approval AgentStack Daily release orchestrator.

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
import atexit
import copy
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import uuid

import build_youtube_episode_videos as video_build
import release_episode as rel
import release_approval_gate as approval_gate


SCRIPTS_DIR = Path(__file__).resolve().parent
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
VIDEO_BOOTSTRAP = VIDEO_ROOT / "shared" / "bootstrap_podcast_episode.py"
VIDEO_PIPELINE = VIDEO_ROOT / "shared" / "run_pipeline.py"
PUBLISH_LOCK = threading.Lock()
STATE_SAVE_LOCK = threading.RLock()
# Serialises local TTS calls — generate_audio sets module-level ga.VOICES so concurrent
# threads would race and generate the wrong language voices for each other.
_LOCAL_TTS_LOCK = threading.Lock()

# M4 TTS dispatch — SSH via Thunderbolt link
M4_HOST = "192.168.1.222"
M4_USER = "toby"
M4_SSH_KEY = Path.home() / ".ssh/id_ed25519"
M4_PODCAST_DIR = Path("/Users/toby/podcast_gen")
# First M4_LANG_SLOTS languages in LANGS order run on M4; the rest run locally on M3
M4_LANG_SLOTS = 2

STEP_SETUP = "setup"
STEP_EN_PUBLISH = "lane_en_publish"
STEP_TRANSLATIONS = "lane_translations"
STEP_POST_TRANSLATION = "post_translation"
STEP_EN_VIDEO = "lane_en_video"
STEP_TRANSLATED_VIDEOS = "translated_videos"
STEP_YOUTUBE = "youtube"
STEP_DISCORD = "discord"
STEP_SHORTS = "shorts"

STEP_ORDER = [
    STEP_SETUP,
    STEP_EN_PUBLISH,
    STEP_TRANSLATIONS,
    STEP_POST_TRANSLATION,
    STEP_EN_VIDEO,
    STEP_TRANSLATED_VIDEOS,
    STEP_YOUTUBE,
    STEP_DISCORD,
    STEP_SHORTS,
]

VALID_YOUTUBE_VIDEO_MODES = {"static", "flux"}

RUN_CONTEXT: dict[str, Any] = {
    "ep_num": None,
    "state": None,
    "terminal_status": None,
}


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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def orchestrator_meta(state: dict[str, Any]) -> dict[str, Any]:
    meta = state.setdefault("approved_orchestrator", {})
    meta.setdefault("completed_steps", [])
    meta.setdefault("lane_results", {})
    meta.setdefault("updated_at", None)
    return meta


def completed_steps(state: dict[str, Any]) -> set[str]:
    return set(orchestrator_meta(state).get("completed_steps", []))


def save_state(ep_num: int, state: dict[str, Any]) -> None:
    with STATE_SAVE_LOCK:
        orchestrator_meta(state)["updated_at"] = utc_now()
        rel.save_state(ep_num, state)


def mark_run_status(
    ep_num: int,
    state: dict[str, Any],
    status: str,
    current_step: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    meta = orchestrator_meta(state)
    meta["run_status"] = status
    meta["run_pid"] = os.getpid()
    meta["last_heartbeat_at"] = utc_now()
    if current_step:
        meta["current_step"] = current_step
    if details:
        meta.update(details)
    RUN_CONTEXT["ep_num"] = ep_num
    RUN_CONTEXT["state"] = state
    if status in {"complete", "failed", "interrupted", "paused", "exited_early"}:
        RUN_CONTEXT["terminal_status"] = status
    save_state(ep_num, state)


def heartbeat(ep_num: int, state: dict[str, Any], current_step: str) -> None:
    mark_run_status(ep_num, state, "running", current_step)


def notify_unexpected_exit() -> None:
    ep_num = RUN_CONTEXT.get("ep_num")
    if ep_num is None:
        return
    if RUN_CONTEXT.get("terminal_status") in {"complete", "failed", "interrupted", "paused"}:
        return

    state = RUN_CONTEXT.get("state")
    if not isinstance(state, dict):
        try:
            state = rel.load_state(int(ep_num))
        except Exception:
            state = {}

    meta = orchestrator_meta(state)
    if STEP_DISCORD in set(meta.get("completed_steps", [])) or meta.get("run_status") == "complete":
        return

    step = meta.get("current_step") or "unknown step"
    try:
        mark_run_status(int(ep_num), state, "exited_early", str(step))
    except Exception:
        pass
    post_build_log(
        int(ep_num),
        f"❌ Approved release process exited before completion near {step}; rerun the approved release launcher to resume.",
    )
    # Also alert the operator on Telegram so failures are never invisible.
    try:
        telegram_alert(ep_num, f"❌ EP{ep_num:03d} approved release exited unexpectedly at {step}.\nRerun: `python3 scripts/launch_approved_release.py {ep_num} --audio-approved-by-telegram`")
    except Exception:
        pass


def install_signal_handlers(ep_num: int, state: dict[str, Any]) -> None:
    RUN_CONTEXT["ep_num"] = ep_num
    RUN_CONTEXT["state"] = state

    def handle_sighup(signum: int, _frame: Any) -> None:
        current_state = RUN_CONTEXT.get("state") if isinstance(RUN_CONTEXT.get("state"), dict) else state
        name = signal.Signals(signum).name
        meta = orchestrator_meta(current_state)
        meta["last_signal"] = name
        meta["sighup_ignored_at"] = utc_now()
        mark_run_status(ep_num, current_state, "running", str(meta.get("current_step") or "sighup"), {"last_signal": name})
        post_build_log(ep_num, "⚠️ Approved release received SIGHUP; continuing detached.")

    def handle_shutdown(signum: int, _frame: Any) -> None:
        current_state = RUN_CONTEXT.get("state") if isinstance(RUN_CONTEXT.get("state"), dict) else state
        name = signal.Signals(signum).name
        meta = orchestrator_meta(current_state)
        step = str(meta.get("current_step") or "unknown step")
        mark_run_status(ep_num, current_state, "interrupted", step, {"last_signal": name})
        post_build_log(ep_num, f"❌ Approved release interrupted by {name} near {step}.")
        raise SystemExit(128 + signum)

    if hasattr(signal, "SIGHUP"):
        signal.signal(signal.SIGHUP, handle_sighup)
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)


atexit.register(notify_unexpected_exit)


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
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, stdin=subprocess.DEVNULL, check=True)


def paragraph_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", text)
    total = 0
    for block in blocks:
        collapsed = " ".join(line.strip() for line in block.splitlines() if line.strip())
        if collapsed:
            total += 1
    return total


def transcript_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bootstrap_mismatches(ep_dir: Path, transcript_path: Path, audio_path: Path) -> list[str]:
    config_path = ep_dir / "config.json"
    narr_path = ep_dir / "narration.txt"
    mismatches: list[str] = []

    try:
        cfg = json.loads(config_path.read_text())
    except Exception as exc:
        return [f"config unreadable: {exc}"]

    expected_scene_count = paragraph_count(transcript_path)
    if int(cfg.get("scene_count") or 0) != expected_scene_count:
        mismatches.append(
            f"scene_count={cfg.get('scene_count')} but transcript now has {expected_scene_count} paragraphs"
        )

    expected_audio = str(audio_path)
    if cfg.get("direct_audio") != expected_audio:
        mismatches.append("direct_audio path no longer matches current EN audio")
    if cfg.get("paths", {}).get("narration") != expected_audio:
        mismatches.append("paths.narration no longer matches current EN audio")

    current_transcript = transcript_path.read_text(encoding="utf-8")
    try:
        bootstrapped_transcript = narr_path.read_text(encoding="utf-8")
    except Exception as exc:
        mismatches.append(f"narration.txt unreadable: {exc}")
    else:
        if bootstrapped_transcript != current_transcript:
            mismatches.append("narration.txt differs from the current transcript")

    fingerprint = cfg.get("source_fingerprint", {})
    current_hash = transcript_sha256(transcript_path)
    if fingerprint.get("transcript_sha256") and fingerprint["transcript_sha256"] != current_hash:
        mismatches.append("source_fingerprint transcript hash no longer matches")

    return mismatches


def derived_video_artifact_count(ep_num: int) -> int:
    build_dir = video_build.episode_build_dir(ep_num)
    patterns = (
        "assets/flux_images/scene_*.png",
        "assets/kb_clips/scene_*.mp4",
        "outputs/*.mp4",
    )
    total = 0
    for pattern in patterns:
        total += len(list(build_dir.glob(pattern)))
    return total


def video_episode_dir(ep_num: int) -> Path:
    canonical = VIDEO_ROOT / "openclaw-daily" / f"ep{ep_num}"
    legacy = VIDEO_ROOT / f"ep{ep_num}"
    if canonical.exists():
        return canonical
    if legacy.exists():
        return legacy
    return canonical


def ensure_crossfire_bootstrap(ep_num: int, state: dict[str, Any]) -> None:
    ep_dir = video_episode_dir(ep_num)
    config_path = ep_dir / "config.json"
    story_path = ep_dir / "story.py"
    narr_path = ep_dir / "narration.txt"
    ep_str = f"{ep_num:03d}"
    transcript_path = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript_nova.md"
    audio_path = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"

    if not transcript_path.exists():
        raise FileNotFoundError(f"Missing EN transcript for crossfire bootstrap: {transcript_path}")
    if not audio_path.exists():
        raise FileNotFoundError(f"Missing EN audio for crossfire bootstrap: {audio_path}")

    if config_path.exists() and story_path.exists() and narr_path.exists():
        mismatches = bootstrap_mismatches(ep_dir, transcript_path, audio_path)
        if not mismatches:
            log(f"[ EN VIDEO ] Crossfire ep{ep_num} already bootstrapped")
            return

        artifact_count = derived_video_artifact_count(ep_num)
        detail = "; ".join(mismatches)
        if artifact_count:
            raise RuntimeError(
                f"Crossfire bootstrap drift detected for ep{ep_num}: {detail}. "
                f"Found {artifact_count} derived video artifact(s) in {video_build.episode_build_dir(ep_num)}; "
                "refusing to reuse stale assets."
            )
        log(f"[ EN VIDEO ] Bootstrap drift detected — regenerating source files ({detail})")
        meta = rel.get_en_release_metadata(ep_num, state)
        scene_count = paragraph_count(transcript_path)
        split_scene = scene_count // 2
        run_streaming([
            str(VIDEO_PYTHON),
            str(VIDEO_BOOTSTRAP),
            "--episode", str(ep_num),
            "--title", meta["episode_title"],
            "--transcript", str(transcript_path),
            "--direct-audio", str(audio_path),
            "--split-scene", str(split_scene),
            "--root", str(VIDEO_ROOT),
            "--force",
        ], cwd=VIDEO_ROOT)
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
        heartbeat(ep_num, lane_state, STEP_EN_PUBLISH)
        lane_state = rel.phase_en_feed(ep_num, lane_state, pub_date)
        with PUBLISH_LOCK:
            lane_state = rel.phase_publish_en(ep_num, lane_state)
        log("[ LANE / EN PUBLISH ] Complete")
        return lane_state
    except Exception as exc:
        raise LaneError(STEP_EN_PUBLISH, str(exc), lane_state) from exc


def run_tts_on_m4(ep_num: int, lang: str, local_script: Path, local_out: Path) -> None:
    ep_str = f"{ep_num:03d}"
    remote_script = M4_PODCAST_DIR / f"episode_{ep_str}_{lang}.md"
    remote_out_stem = f"episode_{ep_str}_{lang}"
    remote_out = M4_PODCAST_DIR / "audio" / f"{remote_out_stem}.mp3"
    ssh_opts = ["-i", str(M4_SSH_KEY), "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=30", "-o", "ServerAliveInterval=60"]

    # Always sync local TTS code to M4 so the remote stage cannot silently run
    # stale generation logic.
    for script_name in ("generate_audio.py", "generate_audio_lang.py"):
        subprocess.run(
            ["scp"] + ssh_opts + [
                str(PODCAST_DIR / script_name),
                f"{M4_USER}@{M4_HOST}:{M4_PODCAST_DIR}/{script_name}",
            ],
            check=True, timeout=60,
        )
    subprocess.run(
        ["scp"] + ssh_opts + [str(local_script), f"{M4_USER}@{M4_HOST}:{remote_script}"],
        check=True, timeout=60,
    )
    subprocess.run(
        ["ssh"] + ssh_opts + [f"{M4_USER}@{M4_HOST}",
         f"export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH && "
         f"{M4_PODCAST_DIR}/venv/bin/python3 {M4_PODCAST_DIR}/generate_audio_lang.py"
         f" {remote_script} --lang {lang} -o {remote_out_stem}"],
        check=True, timeout=7200,
    )
    subprocess.run(
        ["scp"] + ssh_opts + [f"{M4_USER}@{M4_HOST}:{remote_out}", str(local_out)],
        check=True, timeout=300,
    )
    if not local_out.exists():
        raise RuntimeError(f"M4 TTS did not produce {local_out.name}")


def run_local_tts(ep_num: int, lang: str, out_path: Path) -> None:
    ep_str = f"{ep_num:03d}"
    if str(PODCAST_DIR) not in sys.path:
        sys.path.insert(0, str(PODCAST_DIR))
    import generate_audio as ga
    LANG_VOICES = {
        "es": {"NOVA": "es-ES-ElviraNeural",    "ALLOY": "es-ES-AlvaroNeural"},
        "de": {"NOVA": "de-DE-KatjaNeural",     "ALLOY": "de-DE-ConradNeural"},
        "pt": {"NOVA": "pt-BR-FranciscaNeural", "ALLOY": "pt-BR-AntonioNeural"},
        "hi": {"NOVA": "hi-IN-SwaraNeural",     "ALLOY": "hi-IN-MadhurNeural"},
    }
    script_path = PODCAST_DIR / "translations" / lang / f"episode_{ep_str}_{lang}.md"
    import asyncio
    with _LOCAL_TTS_LOCK:
        ga.VOICES = LANG_VOICES[lang]
        ga.AUDIO_DIR = PODCAST_DIR / "audio"
        asyncio.run(ga.generate_podcast_audio(str(script_path), f"episode_{ep_str}_{lang}"))
    if not out_path.exists():
        raise RuntimeError(f"{lang.upper()} local audio render did not produce {out_path.name}")


def run_tts_for_language(ep_num: int, state: dict[str, Any], lang: str) -> dict[str, Any]:
    ep_str = f"{ep_num:03d}"
    out_path = PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"
    if out_path.exists():
        post_build_log(ep_num, f"ℹ️ [{lang.upper()}] audio already exists")
        return state

    use_m4 = rel.LANGS.index(lang) < M4_LANG_SLOTS
    node_label = "M4" if use_m4 else "M3"
    post_build_log(ep_num, f"⏳ [{lang.upper()}] audio → {node_label}")
    script_path = PODCAST_DIR / "translations" / lang / f"episode_{ep_str}_{lang}.md"

    if use_m4:
        run_tts_on_m4(ep_num, lang, script_path, out_path)
    else:
        run_local_tts(ep_num, lang, out_path)

    return state


def incremental_language_publish(ep_num: int, state: dict[str, Any], lang: str, pub_date: str) -> dict[str, Any]:
    log(f"[ POST TRANSLATION / {lang.upper()} ] Starting...")
    post_build_log(ep_num, f"⏳ [{lang.upper()}] translated assets ready — running QA/publish")
    state = rel.phase_translated_feeds(ep_num, state, pub_date, langs=[lang])
    save_state(ep_num, state)

    qc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "check_episode_translations.py"), str(ep_num), "--lang", lang],
        capture_output=True,
        text=True,
    )
    if qc.stdout.strip():
        print(qc.stdout.strip(), flush=True)
    if qc.returncode != 0:
        if qc.stderr.strip():
            print(qc.stderr.strip(), flush=True)
        raise RuntimeError(f"{lang.upper()} QC failed")

    state = rel.phase_translated_cdn(ep_num, state, langs=[lang])
    save_state(ep_num, state)
    with PUBLISH_LOCK:
        state = rel.phase_publish_translations(ep_num, state, langs=[lang])
    save_state(ep_num, state)
    published = state.setdefault("incremental_translations_published", [])
    if lang not in published:
        published.append(lang)
    save_state(ep_num, state)
    post_build_log(ep_num, f"✅ [{lang.upper()}] QA passed and published")
    log(f"[ POST TRANSLATION / {lang.upper()} ] Complete")
    return state


def _tts_cover_publish(
    ep_num: int,
    lang: str,
    pub_date: str,
    state_snap: dict[str, Any],
    m4_sem: threading.Semaphore,
    shared_state: list[dict[str, Any]],
    shared_lock: threading.Lock,
) -> None:
    """Run TTS → cover → publish for one language. Runs in a thread pool."""
    ep_str = f"{ep_num:03d}"
    out_path = PODCAST_DIR / "audio" / f"episode_{ep_str}_{lang}.mp3"

    # TTS — try M4 first (non-blocking semaphore), fall through to M3 local on any failure
    if not out_path.exists():
        use_m4 = m4_sem.acquire(blocking=False)
        try:
            node = "M4" if use_m4 else "M3"
            post_build_log(ep_num, f"⏳ [{lang.upper()}] audio → {node}")
            script_path = PODCAST_DIR / "translations" / lang / f"episode_{ep_str}_{lang}.md"
            if use_m4:
                try:
                    run_tts_on_m4(ep_num, lang, script_path, out_path)
                except Exception as m4_err:
                    log(f"  ⚠️  [{lang.upper()}] M4 TTS failed ({m4_err}), falling back to local...")
                    post_build_log(ep_num, f"⚠️ [{lang.upper()}] M4 down — local TTS fallback")
                    run_local_tts(ep_num, lang, out_path)
            else:
                run_local_tts(ep_num, lang, out_path)
        finally:
            if use_m4:
                m4_sem.release()
        post_build_log(ep_num, f"✅ [{lang.upper()}] audio ready")

    # Cover + publish (serialised to avoid concurrent feed/git writes)
    with shared_lock:
        current = shared_state[0]
        current = rel.phase_covers(ep_num, current, langs=[lang])
        current = incremental_language_publish(ep_num, current, lang, pub_date)
        published = current.setdefault("incremental_translations_published", [])
        if lang not in published:
            published.append(lang)
        save_state(ep_num, current)
        shared_state[0] = current


def translation_lane(ep_num: int, state: dict[str, Any], pub_date: str) -> dict[str, Any]:
    """
    Incremental per-language pipeline:
      For each language in order:
        1. Translate (main thread, sequential — avoids API hammering)
        2. Immediately dispatch TTS → cover → publish to a thread pool
           • First M4_LANG_SLOTS languages get M4 (non-blocking semaphore acquire)
           • Overflow falls through to M3 (local)
      All TTS jobs run concurrently while translation of the next language proceeds.
    """
    lane_state = copy.deepcopy(state)
    try:
        log("[ LANE / TRANSLATIONS ] Starting (incremental per-language)...")

        already_published = set(lane_state.get("incremental_translations_published", []))
        pending = [l for l in rel.LANGS if l not in already_published]

        if not pending:
            log("[ LANE / TRANSLATIONS ] All languages already published, nothing to do")
            return lane_state

        # Shared mutable state — threads update via shared_lock
        shared_state = [copy.deepcopy(lane_state)]
        shared_lock = threading.Lock()
        # Semaphore gates M4 usage: up to M4_LANG_SLOTS concurrent TTS jobs on M4
        m4_sem = threading.Semaphore(M4_LANG_SLOTS)

        tts_futures: dict[str, Any] = {}

        with ThreadPoolExecutor(max_workers=len(pending)) as pool:
            for lang in pending:
                # ── Translation (main thread, sequential) ──────────────────
                if not lane_state.get("translations", {}).get(lang, {}).get("done"):
                    heartbeat(ep_num, lane_state, f"{STEP_TRANSLATIONS}:{lang}:translate")
                    post_build_log(ep_num, f"⏳ [{lang.upper()}] translating...")
                    lane_state = rel.phase_translate(ep_num, lane_state, langs=[lang])
                    # Propagate translated state into shared state
                    with shared_lock:
                        shared_state[0]["translations"] = copy.deepcopy(
                            lane_state.get("translations", {})
                        )
                    save_state(ep_num, lane_state)
                    post_build_log(ep_num, f"✅ [{lang.upper()}] text ready")

                # ── Dispatch TTS immediately (thread pool) ─────────────────
                snap = copy.deepcopy(lane_state)
                tts_futures[lang] = pool.submit(
                    _tts_cover_publish,
                    ep_num, lang, pub_date, snap,
                    m4_sem, shared_state, shared_lock,
                )

            # ── Wait for all TTS/publish threads ───────────────────────────
            errors = []
            for lang, fut in tts_futures.items():
                try:
                    fut.result()
                except Exception as e:
                    errors.append(f"{lang.upper()}: {e}")

            if errors:
                raise RuntimeError("TTS/publish failures: " + "; ".join(errors))

        lane_state = shared_state[0]
        log("[ LANE / TRANSLATIONS ] Complete")
        return lane_state
    except Exception as exc:
        raise LaneError(STEP_TRANSLATIONS, str(exc), lane_state) from exc


TRANSLATION_MAX_RETRIES = 2
TRANSLATION_RETRY_DELAY = 60  # seconds; multiplied by attempt number

# Telegram home channel for operator alerts (Toby / @DigiToby_bot).
# Locked 2026-06-21 (EP072 incident): when the translation lane exhausts
# retries, the failure is posted to BOTH the build log AND Telegram — the
# build log alone is invisible to the operator during the day.
TELEGRAM_ALERT_TARGET = os.environ.get("PODCAST_TELEGRAM_TARGET", "8319992332")
TELEGRAM_ALERT_CHANNEL = "telegram"
# Locked 2026-06-27: must use @DigiToby_bot, NOT openclaw's default
# ARIA bot. Read the token directly from the hermes .env. Do not fall
# back to openclaw's bot account; that posts to a different chat.
TELEGRAM_ALERT_BOT_TOKEN_FILE = "/Users/tobyglennpeters/.hermes/.env"
TELEGRAM_ALERT_BIN = os.environ.get("OPENCLAW_BIN", "/opt/homebrew/bin/openclaw")


def _telegram_alert_load_token() -> str:
    """Read TELEGRAM_BOT_TOKEN from the hermes .env. Required for the
    @DigiToby_bot identity. If the file is missing or the var is
    unset, raise SystemExit so the orchestrator fails loudly rather
    than silently routing to the wrong bot."""
    try:
        env_text = Path("/Users/tobyglennpeters/.hermes/.env").read_text()
    except FileNotFoundError:
        raise SystemExit(
            f"❌ ROUTING MIS-WIRED: /Users/tobyglennpeters/.hermes/.env not "
            f"found. The agentstack-podcast orchestrator must post via "
            f"@DigiToby_bot. Do not fall back to openclaw's ARIA bot."
        )
    for line in env_text.splitlines():
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise SystemExit(
        f"❌ ROUTING MIS-WIRED: TELEGRAM_BOT_TOKEN not set in "
        f"/Users/tobyglennpeters/.hermes/.env."
    )


def telegram_alert(ep_num: int, message: str) -> None:
    """Best-effort Telegram alert to the operator. Failures are swallowed so
    the alert path never breaks the orchestrator (it logs to /tmp instead)."""
    try:
        token = _telegram_alert_load_token()
        import urllib.parse, urllib.request, json
        data = urllib.parse.urlencode({
            "chat_id": TELEGRAM_ALERT_TARGET,
            "text": message,
            "disable_web_page_preview": "true",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data, method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read())
        if not result.get("ok"):
            raise RuntimeError(f"Telegram API error: {result}")
    except Exception as exc:  # pragma: no cover — never block the pipeline
        try:
            with open("/tmp/podcast_telegram_alert_errors.log", "a") as fh:
                fh.write(f"[{utc_now()}] ep{ep_num:03d}: telegram alert failed: {exc}\n")
        except Exception:
            pass


def format_translation_failure(ep_num: int, exc: "LaneError") -> str:
    """Surface the SPECIFIC QC failure (not the generic "TTS/publish failures"
    summary) to Telegram. Pulls the per-language QC messages from the lane
    error so Toby can diagnose without grepping build logs."""
    raw = str(exc) if exc else "unknown"
    # Try to extract the per-language QC hints from the lane state if attached
    qc_hints: list[str] = []
    if exc and exc.state:
        for lang, payload in (exc.state.get("translations") or {}).items():
            qc = payload.get("qc") if isinstance(payload, dict) else None
            if isinstance(qc, dict) and qc.get("errors"):
                for err in qc["errors"][:3]:
                    qc_hints.append(f"  {lang}: {err}")
    hint_block = ("\n".join(qc_hints) if qc_hints else "  (no per-language QC hints in state)")
    return (
        f"❌ EP{ep_num:03d} lane_translations exhausted "
        f"{TRANSLATION_MAX_RETRIES + 1} attempts.\n"
        f"Fatal: {raw}\n"
        f"QC hints:\n{hint_block}\n"
        f"Recovery: `python3 scripts/recover_failed_translation_lane.py {ep_num:03d}`\n"
        f"If 3am, the morning pipeline will now RESUME the orchestrator instead "
        f"of regenerating the same episode (agentstack_morning.sh Stage 2 — "
        f"locked 2026-06-21)."
    )


def translation_lane_with_retry(ep_num: int, state: dict[str, Any], pub_date: str) -> dict[str, Any]:
    """Wraps translation_lane with automatic retry on failure.

    Between retries, state is reloaded from disk so any per-language progress
    already saved (translations.*.done flags) is preserved and not repeated.

    When all retries are exhausted, a Telegram alert is sent to the operator
    with the specific QC failure (not just "TTS/publish failures") so the
    next-day recovery is one command, not an investigation.
    """
    last_exc: LaneError | None = None
    for attempt in range(TRANSLATION_MAX_RETRIES + 1):
        if attempt > 0:
            delay = TRANSLATION_RETRY_DELAY * attempt
            log(f"[ LANE / TRANSLATIONS ] Retry {attempt}/{TRANSLATION_MAX_RETRIES} in {delay}s...")
            post_build_log(ep_num, f"⚠️ [lane_translations] retry {attempt}/{TRANSLATION_MAX_RETRIES} — waiting {delay}s")
            time.sleep(delay)
            # Reload from disk to pick up per-language done flags saved before the failure
            state = rel.load_state(ep_num)
        try:
            return translation_lane(ep_num, state, pub_date)
        except LaneError as exc:
            if exc.state:
                merged = merge_release_state(state, exc.state)
                save_state(ep_num, merged)
            last_exc = exc
            if attempt < TRANSLATION_MAX_RETRIES:
                log(f"[ LANE / TRANSLATIONS ] Attempt {attempt + 1} failed: {exc}")
                post_build_log(ep_num, f"❌ [lane_translations] attempt {attempt + 1} failed: {exc}")
    # All retries exhausted. Surface the specific failure to Telegram so the
    # operator sees it the same day, not the next morning when the morning
    # pipeline tries to resume.
    if last_exc is not None:
        try:
            telegram_alert(ep_num, format_translation_failure(ep_num, last_exc))
        except Exception:
            pass
    raise last_exc  # type: ignore[misc]



def en_video_lane(ep_num: int, state: dict[str, Any]) -> dict[str, Any]:
    lane_state = copy.deepcopy(state)
    try:
        log("[ LANE / EN VIDEO ] Starting...")
        heartbeat(ep_num, lane_state, STEP_EN_VIDEO)
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
    heartbeat(ep_num, state, step)
    post_build_log(ep_num, f"⏳ [{label}] starting…")
    state = fn(ep_num, state, *args)
    mark_step_complete(ep_num, state, step)
    post_build_log(ep_num, f"✅ [{label}] complete")
    log(f"[ {label} ] Complete")
    return state


def run_shorts(ep_num: int, state: dict[str, Any]) -> dict[str, Any]:
    log("[ SHORTS ] Staging shorts candidates and metadata...")
    post_build_log(ep_num, "⏳ [SHORTS] Staging shorts candidates and metadata...")

    stage_script = SCRIPTS_DIR / "youtube_shorts_pipeline.py"
    if not stage_script.exists():
        raise FileNotFoundError(f"Missing youtube_shorts_pipeline.py script: {stage_script}")

    stage_python = "/Users/tobyglennpeters/.codex-video-tools/.venv/bin/python"
    if not Path(stage_python).exists():
        stage_python = sys.executable
    cmd_stage = [stage_python, str(stage_script), "--mode", "cron"]
    run_streaming(cmd_stage, cwd=PODCAST_DIR)

    log("[ SHORTS ] Starting distributed shorts build...")
    post_build_log(ep_num, "⏳ [SHORTS] Starting distributed shorts build...")

    dist_script = SCRIPTS_DIR / "distribute_shorts_build.sh"
    if not dist_script.exists():
        raise FileNotFoundError(f"Missing distribute_shorts_build.sh script: {dist_script}")

    cmd = ["/bin/bash", str(dist_script), str(ep_num)]
    run_streaming(cmd, cwd=PODCAST_DIR)

    log("[ SHORTS ] Distributed shorts build complete")
    post_build_log(ep_num, "✅ [SHORTS] Distributed shorts build complete")
    return state


def run_local_cleanup(ep_num: int, state: dict[str, Any]) -> None:
    cleanup_script = SCRIPTS_DIR / "cleanup_local_artifacts.py"
    if not cleanup_script.exists():
        return
    result = subprocess.run(
        [sys.executable, str(cleanup_script), "--completed-release", str(ep_num)],
        cwd=str(PODCAST_DIR),
        capture_output=True,
        text=True,
    )
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    state["local_cleanup"] = {
        "updated_at": utc_now(),
        "returncode": result.returncode,
        "output": output[-2000:],
    }
    save_state(ep_num, state)
    if result.returncode == 0:
        summary = output.splitlines()[-2:] if output else ["No local cleanup output."]
        post_build_log(ep_num, "🧹 Local release artifacts cleaned: " + " | ".join(summary))
        log("[ CLEANUP ] " + " | ".join(summary))
    else:
        post_build_log(ep_num, f"⚠️ Local cleanup failed after release; run {cleanup_script.name} manually.")
        log(f"[ CLEANUP ] Failed with exit {result.returncode}")


def format_lane_errors(errors: dict[str, BaseException]) -> str:
    lines = []
    for lane, exc in errors.items():
        lines.append(f"{lane}: {exc}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AgentStack Daily approved-release orchestrator")
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
        "--audio-approved-by-toby",
        action="store_true",
        help="Record Toby's explicit approval of the current EN review audio before releasing; requires --approval-message-id",
    )
    parser.add_argument(
        "--approval-message-id",
        help="Discord message id for Toby's approving reply in the episode review channel",
    )
    parser.add_argument(
        "--from-step",
        choices=STEP_ORDER,
        help="Rewind this orchestrator from the chosen step onward before running",
    )
    parser.add_argument(
        "--through-step",
        choices=STEP_ORDER,
        help="Stop after this step instead of running the full approved release",
    )
    parser.add_argument(
        "--youtube-video-mode",
        choices=sorted(VALID_YOUTUBE_VIDEO_MODES),
        help="Per-episode YouTube video mode: static cover video or flux publish videos",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ep_num = args.episode
    ep_str = f"{ep_num:03d}"
    through_idx = STEP_ORDER.index(args.through_step) if args.through_step else None

    state = rel.load_state(ep_num)
    audio_path = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    if args.audio_approved_by_toby and not args.approval_message_id:
        raise SystemExit("--audio-approved-by-toby requires --approval-message-id from Toby's review-channel reply")
    if args.approval_message_id:
        approval_gate.mark_audio_approved_from_discord(
            state,
            audio_path=audio_path,
            ep_num=ep_num,
            approval_message_id=args.approval_message_id,
            token=rel.load_env_key("DISCORD_BOT_TOKEN"),
        )
        rel.save_state(ep_num, state)
    approval_gate.assert_audio_approved(state, audio_path=audio_path, ep_num=ep_num)
    video_mode = str(
        args.youtube_video_mode
        or state.get("youtube_video_mode")
        or "static"
    ).strip().lower()
    if video_mode not in VALID_YOUTUBE_VIDEO_MODES:
        raise SystemExit(f"Invalid --youtube-video-mode: {video_mode}")
    state["youtube_video_mode"] = video_mode
    state["pub_date"] = args.pub_date
    if args.reset:
        state.pop("approved_orchestrator", None)
    if args.from_step:
        prune_from_step(state, args.from_step)
    install_signal_handlers(ep_num, state)
    mark_run_status(
        ep_num,
        state,
        "running",
        "start",
        {
            "started_at": utc_now(),
            "launcher_pid": os.getppid(),
        },
    )

    log(f"\n{'=' * 68}")
    log(f"AgentStack Daily — EP{ep_str} Approved Release")
    log(f"YouTube video mode: {video_mode}")
    log(f"{'=' * 68}\n")
    post_build_log(ep_num, "🚀 Approved release orchestrator started")

    def should_stop_after(step: str) -> bool:
        if through_idx is None:
            return False
        return STEP_ORDER.index(step) >= through_idx

    try:
        if STEP_SETUP not in completed_steps(state):
            state = run_step(ep_num, state, STEP_SETUP, "SETUP", rel.phase_setup)
        else:
            log("[ SETUP ] Already complete, skipping")
        if should_stop_after(STEP_SETUP):
            mark_run_status(ep_num, state, "paused", STEP_SETUP)
            post_build_log(ep_num, f"⏸ Approved release paused after {STEP_SETUP}")
            return 0

        lane_errors: dict[str, BaseException] = {}
        futures: dict[Any, str] = {}
        heartbeat(ep_num, state, "parallel_lanes")

        with ThreadPoolExecutor(max_workers=3, thread_name_prefix=f"ep{ep_str}-approved") as executor:
            if STEP_EN_PUBLISH not in completed_steps(state):
                futures[executor.submit(en_publish_lane, ep_num, state, args.pub_date)] = STEP_EN_PUBLISH
            else:
                log("[ LANE / EN PUBLISH ] Already complete, skipping")

            if STEP_TRANSLATIONS not in completed_steps(state):
                futures[executor.submit(translation_lane_with_retry, ep_num, state, args.pub_date)] = STEP_TRANSLATIONS
            else:
                log("[ LANE / TRANSLATIONS ] Already complete, skipping")

            if video_mode == "flux" and STEP_EN_VIDEO not in completed_steps(state):
                futures[executor.submit(en_video_lane, ep_num, state)] = STEP_EN_VIDEO
            elif video_mode != "flux":
                log("[ LANE / EN VIDEO ] Static mode selected, skipping FLUX/video lane")
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
                    # Telegram alert for any lane failure (not just translations)
                    try:
                        telegram_alert(
                            ep_num,
                            f"❌ EP{ep_num:03d} {lane} FAILED.\n"
                            f"Fatal: {exc}\n"
                            f"Run: `python3 scripts/launch_approved_release.py {ep_num:03d} --pub-date '{state.get('pub_date','')}'` to resume from completed steps.",
                        )
                    except Exception:
                        pass
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

        if video_mode == "flux" and STEP_EN_VIDEO not in completed_steps(state):
            raise RuntimeError("EN video lane did not complete; refusing to build translated publish videos")
        if STEP_POST_TRANSLATION not in completed_steps(state):
            raise RuntimeError("Post-translation finalize did not complete; refusing to continue to video + YouTube")
        if should_stop_after(STEP_POST_TRANSLATION):
            mark_run_status(ep_num, state, "paused", STEP_POST_TRANSLATION)
            post_build_log(ep_num, f"⏸ Approved release paused after {STEP_POST_TRANSLATION}")
            return 0

        if video_mode == "flux" and STEP_TRANSLATED_VIDEOS not in completed_steps(state):
            heartbeat(ep_num, state, STEP_TRANSLATED_VIDEOS)
            outputs = build_translated_publish_videos(ep_num)
            mark_step_complete(ep_num, state, STEP_TRANSLATED_VIDEOS, {"video_outputs": outputs})
            post_build_log(ep_num, "✅ [TRANSLATED VIDEOS] complete")
        elif video_mode != "flux":
            log("[ TRANSLATED VIDEOS ] Static mode selected, skipping localized publish-video builds")
        else:
            log("[ TRANSLATED VIDEOS ] Already complete, skipping")
        if should_stop_after(STEP_TRANSLATED_VIDEOS):
            mark_run_status(ep_num, state, "paused", STEP_TRANSLATED_VIDEOS)
            post_build_log(ep_num, f"⏸ Approved release paused after {STEP_TRANSLATED_VIDEOS}")
            return 0

        if STEP_YOUTUBE not in completed_steps(state):
            state = run_step(ep_num, state, STEP_YOUTUBE, "YOUTUBE", rel.phase_youtube)
        else:
            log("[ YOUTUBE ] Already complete, skipping")
        if should_stop_after(STEP_YOUTUBE):
            mark_run_status(ep_num, state, "paused", STEP_YOUTUBE)
            post_build_log(ep_num, f"⏸ Approved release paused after {STEP_YOUTUBE}")
            return 0

        if STEP_DISCORD not in completed_steps(state):
            state = run_step(ep_num, state, STEP_DISCORD, "DISCORD", rel.phase_discord)
        else:
            log("[ DISCORD ] Already complete, skipping")
        if should_stop_after(STEP_DISCORD):
            mark_run_status(ep_num, state, "paused", STEP_DISCORD)
            post_build_log(ep_num, f"⏸ Approved release paused after {STEP_DISCORD}")
            return 0

        if STEP_SHORTS not in completed_steps(state):
            state = run_step(ep_num, state, STEP_SHORTS, "SHORTS", run_shorts)
        else:
            log("[ SHORTS ] Already complete, skipping")

        run_local_cleanup(ep_num, state)

        log(f"\n{'=' * 68}")
        log(f"✅ EP{ep_str} approved release complete")
        log(f"  Website: https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/")
        log(f"  Feed: {rel.PODCAST_FEED_URL}")
        log(f"{'=' * 68}")
        mark_run_status(ep_num, state, "complete", STEP_SHORTS, {"completed_at": utc_now()})
        post_build_log(ep_num, f"🎙️ Approved release complete — <https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/>")
        # Telegram "shipped" notification (locked 2026-06-27). Telegram is
        # the operator's review surface; after a successful release the
        # post goes here, not to the Discord #agent-stack-epNNN channel.
        # The notify_telegram_review.py script owns the message format and
        # is also called from the morning pipeline's stage-7 ready post.
        _shipped_msg = (
            f"🚀 EP{ep_num:03d} shipped\n"
            f"\n"
            f"Canonical: https://tobyonfitnesstech.com/podcasts/episode-{ep_num}/\n"
            f"CDN: {rel.en_audio_url(ep_num) if hasattr(rel, 'en_audio_url') else ''}\n"
            f"Released at: {utc_now()}\n"
            f"\n"
            f"Translations + shorts queued. Telegram stays quiet until the "
            f"next morning's review."
        )
        _shipped_ok = False
        try:
            token = _telegram_alert_load_token()
            import urllib.parse, urllib.request
            data = urllib.parse.urlencode({
                "chat_id": TELEGRAM_ALERT_TARGET,
                "text": _shipped_msg,
                "disable_web_page_preview": "true",
            }).encode()
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data=data, method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as r:
                _shipped_result = json.loads(r.read())
            _shipped_ok = bool(_shipped_result.get("ok"))
        except Exception as _exc:
            post_build_log(ep_num, f"WARN Telegram shipped-post failed: {_exc}")
        if not _shipped_ok:
            # Fall through silently — the release is already complete; a
            # failed Telegram post must not roll back the publish.
            pass
        return 0

    except Exception as exc:
        log(f"\n❌ Approved release failed: {exc}")
        trace = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        step = orchestrator_meta(state).get("current_step")
        mark_run_status(ep_num, state, "failed", step, {"failure": trace})
        post_build_log(ep_num, f"❌ Approved release failed: {trace}")
        # Run-stopping failures also go to Telegram (operator rule,
        # 2026-07-07: Telegram = listenable audio + failures that stop
        # audio generation or publishing). Best-effort.
        telegram_alert(
            ep_num,
            f"❌ EP{ep_num:03d} approved release FAILED at {step or 'unknown step'} — "
            f"{trace[:600]}\nRerun the approved release launcher to resume.",
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
