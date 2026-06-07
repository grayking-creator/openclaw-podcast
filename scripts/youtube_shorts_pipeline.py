#!/usr/bin/env python3
"""AgentStack Daily Shorts staging and cron helper.

Stages short candidates for each new episode and reports failures to #build-log
on Discord. Daily shorts are active; staging metadata is for audit/review, not a
manual upload gate.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

try:
    import make_podcast_shorts as shorts_work
except Exception:
    shorts_work = None

ET = "-04:00"
SHORT_SLOTS = ["10:00:00", "18:00:00"]
TARGET_SHORTS = 2
WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
BUILD_LOG_CHANNEL_ID = "1485243812442804327"

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
EPISODES_DIR = PODCAST_DIR / "episodes"
STAGING_ROOT = PODCAST_DIR / "content_staging" / "shorts"
STATE_PATH = SCRIPTS_DIR / "youtube_shorts_state.json"
UPLOADED_PATH = SCRIPTS_DIR / "youtube_uploaded.txt"
AUDIO_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio/audio"
MEDIA_EN_AUDIO_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-media-en/audio"

CHANNELS = ["en", "es", "de", "pt", "hi"]
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "had",
    "has", "have", "he", "her", "here", "hers", "him", "his", "how", "i", "if",
    "in", "into", "is", "it", "its", "just", "me", "my", "of", "on", "or", "our",
    "out", "she", "so", "that", "the", "their", "them", "there", "they", "this",
    "to", "up", "was", "we", "were", "what", "when", "where", "who", "why", "with",
    "you", "your",
}
HOOK_WORDS = {
    "agent", "agents", "android", "automation", "crazy", "data", "discord", "finally",
    "health", "infrastructure", "intelligence", "local", "memory", "never", "openclaw",
    "privacy", "release", "rent", "security", "streaming", "telegram", "threads", "topic",
    "vote", "workflow",
}


@dataclass
class ShortCandidate:
    short_id: str
    hook: str
    snippet: str
    rationale: str
    source_episode: int
    start_sec: float = 0.0
    end_sec: float = 0.0
    duration_sec: float = 0.0
    source_story: str = ""
    score_details: list[str] = field(default_factory=list)
    language: str = "en"
    score: float = 0.0


def load_state() -> Dict:
    if STATE_PATH.exists():
        return normalize_state(json.loads(STATE_PATH.read_text()))
    return normalize_state({
        "review_gate": {
            "required_en_approvals": 0,
            "approved_en_short_ids": [],
            "auto_upload_enabled": True,
        },
        "prepared_episodes": [],
    })


def normalize_state(state: Dict) -> Dict:
    gate = state.setdefault("review_gate", {})
    gate["required_en_approvals"] = 0
    gate["auto_upload_enabled"] = True
    gate.setdefault("approved_en_short_ids", [])
    state.setdefault("prepared_episodes", [])
    return state


def _load_env_key(name: str) -> str:
    env_file = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_file):
        for line in open(env_file):
            if name in line and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get(name, "")


def discord_build_log(msg: str) -> None:
    """Post a one-liner to #build-log on Discord. Fire-and-forget — never raises."""
    try:
        import urllib.request
        token = _load_env_key("DISCORD_BOT_TOKEN")
        if not token:
            return
        payload = json.dumps({"content": msg}).encode()
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{BUILD_LOG_CHANNEL_ID}/messages",
            data=payload,
            headers={
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json",
                "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=8)
    except Exception:
        pass


def save_state(state: Dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")


def latest_uploaded_episode() -> int | None:
    if not UPLOADED_PATH.exists():
        return None
    vals = [int(x.strip()) for x in UPLOADED_PATH.read_text().splitlines() if x.strip().isdigit()]
    return max(vals) if vals else None


def latest_transcript_episode() -> int | None:
    episodes = []
    for path in EPISODES_DIR.glob("episode_*_transcript.md"):
        m = re.search(r"episode_(\d+)_transcript\.md$", path.name)
        if m:
            episodes.append(int(m.group(1)))
    return max(episodes) if episodes else None


def latest_episode_for_shorts() -> int | None:
    uploaded = latest_uploaded_episode()
    latest_tx = latest_transcript_episode()

    if uploaded is not None and transcript_path(uploaded).exists():
        return uploaded
    return latest_tx


def transcript_path(ep: int) -> Path:
    return EPISODES_DIR / f"episode_{ep:03d}_transcript.md"


def episode_audio_path(ep: int) -> Path | None:
    candidates = [
        MEDIA_EN_AUDIO_DIR / f"episode_{ep:03d}.mp3",
        AUDIO_DIR / f"episode_{ep:03d}.mp3",
        AUDIO_DIR / f"episode_{ep:03d}_full.mp3",
        AUDIO_DIR / f"episode_{ep:03d}_full_v2.mp3",
        AUDIO_DIR / f"episode_{ep:03d}_v2.mp3",
        PODCAST_DIR / "audio" / f"episode_{ep:03d}.mp3",
        AUDIO_DIR / "latest.mp3",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def get_episode_title(ep_num: int, lang: str = "en") -> str:
    ep_str = f"{ep_num:03d}"
    if lang == "en":
        feed_path = PODCAST_DIR / "feed.xml"
    else:
        feed_path = PODCAST_DIR / "translations" / f"feed_{lang}.xml"
    if not feed_path.exists():
        return f"AgentStack Daily EP{ep_str}"
    content = feed_path.read_text()
    items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
    for item in items:
        ep_match = re.search(r"<itunes:episode>(\d+)</itunes:episode>", item)
        if ep_match and int(ep_match.group(1)) == ep_num:
            title_match = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", item)
            if title_match:
                return title_match.group(1).strip()
    return f"AgentStack Daily EP{ep_str}"


def episode_text_path(ep: int) -> Path | None:
    candidates = [
        transcript_path(ep),
        PODCAST_DIR / f"episode_{ep:03d}.md",
        PODCAST_DIR / f"episode_{ep:03d}_full_v2.md",
        PODCAST_DIR / f"episode_{ep:03d}_script.md",
        PODCAST_DIR / f"episode_{ep:03d}_transcript.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def clean_lines(text: str) -> List[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("---"):
            continue
        # strip markdown emphasis
        line = re.sub(r"[*_`]+", "", line)
        # keep substantial lines only
        if len(line) < 45:
            continue
        lines.append(line)
    return lines


def word_tokens(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9']+", text.lower())


def make_hook(line: str) -> str:
    # Grab first sentence-ish fragment and shape into a short hook.
    fragment = re.split(r"(?<=[.!?])\s+", line)[0].strip()
    fragment = fragment[:90].rstrip(" ,;:")
    if not re.search(r"[.!?]$", fragment):
        fragment += "…"
    return fragment


def parse_timestamp(raw: str) -> int:
    parts = [int(part) for part in raw.split(":")]
    if len(parts) == 2:
        mins, secs = parts
        return mins * 60 + secs
    hours, mins, secs = parts
    return hours * 3600 + mins * 60 + secs


def story_boundaries(ep: int) -> list[tuple[int, str]]:
    show_notes = PODCAST_DIR / f"show_notes_episode_{ep:03d}.md"
    if not show_notes.exists():
        return []
    boundaries: list[tuple[int, str]] = []
    for raw_line in show_notes.read_text().splitlines():
        line = raw_line.strip()
        match = re.match(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+)$", line)
        if not match:
            continue
        stamp, title = match.groups()
        title = title.strip()
        if "—" in title:
            title = title.split("—", 1)[1].strip()
        boundaries.append((parse_timestamp(stamp), title))
    return boundaries


def source_story_for_time(ep: int, start_sec: float) -> str:
    boundaries = story_boundaries(ep)
    current = ""
    for boundary_sec, title in boundaries:
        if start_sec + 0.01 < boundary_sec:
            break
        current = title
    return current


def choose_top_candidates(candidates: list, limit: int = TARGET_SHORTS) -> list:
    picked: list[shorts_work.Candidate] = []
    ranked = sorted(candidates, key=lambda item: item.score, reverse=True)
    for candidate in ranked:
        if any(shorts_work.overlap(candidate, existing) > shorts_work.SELECTION_OVERLAP_MAX for existing in picked):
            continue
        if any(shorts_work.content_similarity(candidate.text, existing.text) > 0.58 for existing in picked):
            continue
        picked.append(candidate)
        if len(picked) >= limit:
            break
    return picked


def build_candidates(ep: int) -> List[ShortCandidate]:
    if shorts_work is None:
        path = episode_text_path(ep)
        if path is None:
            return []
        lines = clean_lines(path.read_text())
        return [
            ShortCandidate(
                short_id=f"short-en-{idx:03d}",
                hook=make_hook(line),
                snippet=line[:220].rstrip(),
                rationale="Transcript-only fallback because the audio scoring environment was unavailable.",
                source_episode=ep,
                score=float(len(lines) - idx),
            )
            for idx, line in enumerate(lines[:TARGET_SHORTS], start=1)
        ]

    audio_path = episode_audio_path(ep)
    if audio_path is None:
        path = episode_text_path(ep)
        if path is None:
            return []
        lines = clean_lines(path.read_text())
        return [
            ShortCandidate(
                short_id=f"short-en-{idx:03d}",
                hook=make_hook(line),
                snippet=line[:220].rstrip(),
                rationale="Fallback transcript-only candidate because no episode audio was available.",
                source_episode=ep,
                score=float(idx),
            )
            for idx, line in enumerate(lines[:TARGET_SHORTS], start=1)
        ]

    analysis_dir = STAGING_ROOT / f"episode_{ep:03d}" / "_analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    wav_path = analysis_dir / f"episode_{ep:03d}.wav"
    transcript_json = analysis_dir / "transcript.json"

    shorts_work.extract_audio(audio_path, wav_path)
    transcript = shorts_work.transcribe_audio(wav_path, transcript_json, WHISPER_MODEL)
    rms, bucket_seconds = shorts_work.load_energy(wav_path)
    raw_candidates = [
        candidate
        for candidate in shorts_work.build_candidates(transcript.get("segments", []), rms, bucket_seconds)
        if candidate.start >= 90.0
    ]
    if not raw_candidates:
        raw_candidates = shorts_work.build_candidates(transcript.get("segments", []), rms, bucket_seconds)
    ranked = choose_top_candidates(raw_candidates, TARGET_SHORTS)

    episode_title = get_episode_title(ep, "en")
    results: List[ShortCandidate] = []
    for idx, candidate in enumerate(ranked, start=1):
        story_title = source_story_for_time(ep, candidate.start)
        rationale = (
            "Audio-scored candidate tuned from channel analytics: 35-55s target, "
            "strong opening hook, dense payoff, and non-overlapping with the other episode pick."
        )
        results.append(
            ShortCandidate(
                short_id=f"short-en-{idx:03d}",
                hook=make_hook(candidate.text),
                snippet=candidate.text[:240].rstrip(),
                rationale=rationale,
                source_episode=ep,
                start_sec=round(candidate.start, 2),
                end_sec=round(candidate.end, 2),
                duration_sec=round(candidate.end - candidate.start, 2),
                source_story=story_title or episode_title,
                score_details=candidate.reasons,
                score=round(candidate.score, 3),
            )
        )
    return results


def build_range_candidates(start_ep: int, end_ep: int, limit: int = TARGET_SHORTS) -> List[ShortCandidate]:
    pool: List[ShortCandidate] = []
    for ep in range(start_ep, end_ep + 1):
        ranked = sorted(build_candidates(ep), key=lambda c: c.score, reverse=True)
        pool.extend(ranked[:limit])
    return pool


def next_slot_times(start_dt: datetime, count: int) -> List[str]:
    scheduled = []
    day = start_dt.date()
    cursor = start_dt
    while len(scheduled) < count:
        for slot in SHORT_SLOTS:
            slot_dt = datetime.fromisoformat(f"{day.isoformat()}T{slot}{ET}")
            if slot_dt <= cursor:
                continue
            scheduled.append(slot_dt.isoformat())
            if len(scheduled) >= count:
                break
        day = day + timedelta(days=1)
    return scheduled


def write_episode_artifacts(ep: int, candidates: List[ShortCandidate]) -> Path:
    ep_dir = STAGING_ROOT / f"episode_{ep:03d}"
    ep_dir.mkdir(parents=True, exist_ok=True)

    candidates_path = ep_dir / "shorts_candidates_en.json"
    candidates_path.write_text(json.dumps([asdict(c) for c in candidates], indent=2) + "\n")

    now = datetime.now().astimezone()
    scheduled_times = next_slot_times(now, len(candidates))

    queue = []
    for i, c in enumerate(candidates):
        queue.append({
            "short_id": c.short_id,
            "source_episode": ep,
            "hook": c.hook,
            "snippet": c.snippet,
            "start_sec": c.start_sec,
            "end_sec": c.end_sec,
            "duration_sec": c.duration_sec,
            "source_story": c.source_story,
            "score": c.score,
            "retry_after_days": 2,
            "status": "staged",
            "requires_manual_review": False,
            "scheduled_publish_at": scheduled_times[i],
            "language": "en",
        })

    # Translation channels are scaffolded from EN sources for future auto rollout.
    for lang in [x for x in CHANNELS if x != "en"]:
        for i, c in enumerate(candidates):
            queue.append({
                "short_id": f"short-{lang}-{i+1:03d}",
                "source_episode": ep,
                "source_short_id": c.short_id,
                "status": "pending_translation",
                "language": lang,
                "scheduled_publish_at": scheduled_times[i],
                "retry_after_days": 2,
            })

    queue_path = ep_dir / "shorts_upload_queue.json"
    queue_path.write_text(json.dumps(queue, indent=2) + "\n")

    review_md = ep_dir / "REVIEW.md"
    review_md.write_text(
        "# Shorts Review (Auto Rollout)\n\n"
        f"Episode: {ep}\n\n"
        "Daily shorts are active; this file records the selected clips for audit/review.\n"
        "Selection rubric: 35-55s duration, hard first-two-second hook, dense payoff, no hashtags in titles.\n"
        "The two EN shorts below are the episode package queued for rollout:\n\n"
        + "\n".join(
            [
                f"- **{c.short_id}**\n"
                f"  - Story: {c.source_story or 'Unknown'}\n"
                f"  - Timing: {c.start_sec:.2f}s–{c.end_sec:.2f}s ({c.duration_sec:.2f}s)\n"
                f"  - Hook: {c.hook}\n"
                f"  - Snippet: {c.snippet}\n"
                f"  - Score: {c.score}\n"
                f"  - Signals: {', '.join(c.score_details[:5])}\n"
                for c in candidates[:2]
            ]
        )
        + "\n",
    )

    return ep_dir


def write_range_artifacts(start_ep: int, end_ep: int, candidates: List[ShortCandidate]) -> Path:
    range_dir = STAGING_ROOT / f"range_{start_ep:03d}_{end_ep:03d}"
    range_dir.mkdir(parents=True, exist_ok=True)

    candidates_path = range_dir / "shorts_candidates_en.json"
    candidates_path.write_text(json.dumps([asdict(c) for c in candidates], indent=2) + "\n")

    review_md = range_dir / "REVIEW.md"
    review_md.write_text(
        "# Shorts Review (Episode Range)\n\n"
        f"Episode range: {start_ep}-{end_ep}\n\n"
        "Top ranked candidates across the requested range:\n\n"
        + "\n".join(
            [
                f"- **{c.short_id}**\n"
                f"  - Episode: {c.source_episode}\n"
                f"  - Story: {c.source_story or 'Unknown'}\n"
                f"  - Timing: {c.start_sec:.2f}s–{c.end_sec:.2f}s ({c.duration_sec:.2f}s)\n"
                f"  - Hook: {c.hook}\n"
                f"  - Snippet: {c.snippet}\n"
                f"  - Score: {c.score:.2f}\n"
                for c in candidates
            ]
        )
        + "\n"
    )
    return range_dir


def ensure_prepared_latest_episode(state: Dict) -> str:
    ep = latest_episode_for_shorts()
    if ep is None:
        return "No transcript episodes found yet; skipping shorts staging."

    if ep in state.get("prepared_episodes", []):
        return f"Episode {ep} already prepared for shorts."

    tpath = transcript_path(ep)
    if not tpath.exists():
        return f"Transcript missing for episode {ep}: {tpath}"

    candidates = build_candidates(ep)
    if len(candidates) < TARGET_SHORTS:
        return f"Could not create {TARGET_SHORTS} shorts for episode {ep}."

    out_dir = write_episode_artifacts(ep, candidates)
    state.setdefault("prepared_episodes", []).append(ep)
    save_state(state)
    return f"Prepared {len(candidates)} EN shorts + translation scaffolding for episode {ep} at {out_dir}"


def prepare_range_review(start_ep: int, end_ep: int) -> str:
    candidates = build_range_candidates(start_ep, end_ep)
    if not candidates:
        return f"No source episode text found for range {start_ep}-{end_ep}."
    out_dir = write_range_artifacts(start_ep, end_ep, candidates)
    return f"Prepared {len(candidates)} ranked candidates for episodes {start_ep}-{end_ep} at {out_dir}"


def approve_en_short(state: Dict, short_id: str) -> str:
    gate = state.setdefault("review_gate", {})
    approved = gate.setdefault("approved_en_short_ids", [])
    required = int(gate.get("required_en_approvals", 2))

    if short_id in approved:
        return f"{short_id} already approved ({len(approved)}/{required})."

    approved.append(short_id)
    if len(approved) >= required:
        gate["auto_upload_enabled"] = True

    save_state(state)
    status = "enabled" if gate.get("auto_upload_enabled") else "still gated"
    return f"Approved {short_id}. EN gate: {len(approved)}/{required} ({status})."


def show_review(state: Dict) -> str:
    prepared = state.get("prepared_episodes", [])
    if not prepared:
        return "No prepared episodes yet. Run --mode cron first."
    latest = max(prepared)
    review_path = STAGING_ROOT / f"episode_{latest:03d}" / "REVIEW.md"
    if not review_path.exists():
        return f"Review file missing: {review_path}"
    return review_path.read_text()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["cron"], help="Run staging automation")
    parser.add_argument("--show-review", action="store_true")
    parser.add_argument("--approve-en", type=str)
    parser.add_argument("--episode-range", type=str, help="Episode range like 1-9 for cross-episode review")
    args = parser.parse_args()

    state = load_state()

    if args.mode == "cron":
        try:
            result = ensure_prepared_latest_episode(state)
            print(result)
            gate = state.get("review_gate", {})
            gate_summary = (
                "Auto-upload: active "
                f"(manual approval required={gate.get('required_en_approvals', 0)})"
            )
            print(gate_summary)
            if result.startswith("Could not create") or result.startswith("Transcript missing"):
                discord_build_log(f"⚠️ [AgentStack Shorts] Staging incomplete: {result}")
            elif "already prepared" not in result and "skipping" not in result:
                discord_build_log(f"✅ [AgentStack Shorts] {result}")
        except Exception as exc:
            msg = f"❌ [AgentStack Shorts] cron failed: {exc}"
            print(msg)
            discord_build_log(msg)
            return 1
        return 0

    if args.episode_range:
        match = re.fullmatch(r"(\d+)-(\d+)", args.episode_range.strip())
        if not match:
            print("Invalid --episode-range. Use START-END, for example 1-9.")
            return 1
        start_ep = int(match.group(1))
        end_ep = int(match.group(2))
        if end_ep < start_ep:
            start_ep, end_ep = end_ep, start_ep
        print(prepare_range_review(start_ep, end_ep))
        return 0

    if args.approve_en:
        print(approve_en_short(state, args.approve_en.strip()))
        return 0

    if args.show_review:
        print(show_review(state))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
