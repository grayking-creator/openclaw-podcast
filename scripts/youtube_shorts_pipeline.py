#!/usr/bin/env python3
"""
YouTube Shorts pipeline helper for OpenClaw Daily.

Current behavior (safe by default):
- Generates/stages 10 EN shorts candidates from the latest uploaded episode transcript.
- Creates a cross-channel queue (EN + ES/DE/PT/HI) with 2 shorts/day schedule slots.
- Enforces an EN review gate before any auto-upload rollout.
- Does NOT upload anything yet.

Usage:
  python3 youtube_shorts_pipeline.py --mode cron
  python3 youtube_shorts_pipeline.py --show-review
  python3 youtube_shorts_pipeline.py --approve-en short-en-001
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

ET = "-04:00"
SHORT_SLOTS = ["10:00:00", "18:00:00"]
TARGET_SHORTS = 10

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
EPISODES_DIR = PODCAST_DIR / "episodes"
STAGING_ROOT = PODCAST_DIR / "content_staging" / "shorts"
STATE_PATH = SCRIPTS_DIR / "youtube_shorts_state.json"
UPLOADED_PATH = SCRIPTS_DIR / "youtube_uploaded.txt"

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
    language: str = "en"
    score: float = 0.0


def load_state() -> Dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {
        "review_gate": {
            "required_en_approvals": 2,
            "approved_en_short_ids": [],
            "auto_upload_enabled": False,
        },
        "prepared_episodes": [],
    }


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


def score_line(line: str) -> float:
    tokens = word_tokens(line)
    filtered = [t for t in tokens if t not in STOPWORDS]
    counts = Counter(filtered)
    unique_ratio = len(set(filtered)) / max(1, len(filtered))
    hook_hits = sum(1 for t in filtered if t in HOOK_WORDS)
    repeat_penalty = max(counts.values(), default=0) / max(1, len(filtered))
    quote_bonus = 0.8 if ":" in line else 0.0
    punctuation_bonus = 0.5 * line.count("—") + 0.3 * line.count("!")
    return (
        len(filtered) * 0.12
        + unique_ratio * 4.0
        + hook_hits * 1.1
        + quote_bonus
        + punctuation_bonus
        - repeat_penalty * 3.0
    )


def make_hook(line: str) -> str:
    # Grab first sentence-ish fragment and shape into a short hook.
    fragment = re.split(r"(?<=[.!?])\s+", line)[0].strip()
    fragment = fragment[:105].rstrip(" ,;:")
    if not re.search(r"[.!?]$", fragment):
        fragment += "…"
    return fragment


def build_candidates(ep: int, transcript_text: str) -> List[ShortCandidate]:
    lines = clean_lines(transcript_text)
    if not lines:
        return []

    # Spread picks across transcript for variety.
    step = max(1, len(lines) // TARGET_SHORTS)
    picks = []
    idx = 0
    while len(picks) < TARGET_SHORTS and idx < len(lines):
        picks.append(lines[idx])
        idx += step
    while len(picks) < TARGET_SHORTS:
        picks.append(lines[min(len(lines) - 1, len(picks))])

    results: List[ShortCandidate] = []
    for i, line in enumerate(picks[:TARGET_SHORTS], start=1):
        short_id = f"short-en-{i:03d}"
        hook = make_hook(line)
        snippet = line[:260].rstrip()
        rationale = (
            "Built for strong Shorts retention: concise hook + high-information claim "
            "from the latest episode narrative."
        )
        results.append(
            ShortCandidate(
                short_id=short_id,
                hook=hook,
                snippet=snippet,
                rationale=rationale,
                source_episode=ep,
                score=score_line(line),
            )
        )
    return results


def build_range_candidates(start_ep: int, end_ep: int, limit: int = 10) -> List[ShortCandidate]:
    pool: List[ShortCandidate] = []
    for ep in range(start_ep, end_ep + 1):
        path = episode_text_path(ep)
        if path is None:
            continue
        lines = clean_lines(path.read_text())
        scored = sorted(lines, key=score_line, reverse=True)
        for idx, line in enumerate(scored[:3], start=1):
            pool.append(
                ShortCandidate(
                    short_id=f"short-en-ep{ep:03d}-{idx:02d}",
                    hook=make_hook(line),
                    snippet=line[:260].rstrip(),
                    rationale=f"High-signal candidate from episode {ep} selected from source text.",
                    source_episode=ep,
                    score=score_line(line),
                )
            )
    ranked = sorted(pool, key=lambda c: c.score, reverse=True)
    return ranked[:limit]


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
            "status": "staged_review_required" if i < 2 else "staged",
            "requires_manual_review": i < 2,
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
            })

    queue_path = ep_dir / "shorts_upload_queue.json"
    queue_path.write_text(json.dumps(queue, indent=2) + "\n")

    review_md = ep_dir / "REVIEW.md"
    review_md.write_text(
        "# Shorts Review (EN gate)\n\n"
        f"Episode: {ep}\n\n"
        "Manual review required before auto-upload rollout.\n"
        "First two EN shorts are gate items:\n\n"
        + "\n".join(
            [
                f"- **{c.short_id}**\n"
                f"  - Hook: {c.hook}\n"
                f"  - Snippet: {c.snippet}\n"
                for c in candidates[:2]
            ]
        )
        + "\n\nApprove with:\n"
        "```bash\n"
        "python3 scripts/youtube_shorts_pipeline.py --approve-en short-en-001\n"
        "python3 scripts/youtube_shorts_pipeline.py --approve-en short-en-002\n"
        "```\n",
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

    candidates = build_candidates(ep, tpath.read_text())
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
        print(ensure_prepared_latest_episode(state))
        gate = state.get("review_gate", {})
        print(
            f"Review gate: approved {len(gate.get('approved_en_short_ids', []))}/"
            f"{gate.get('required_en_approvals', 2)}, "
            f"auto_upload_enabled={gate.get('auto_upload_enabled', False)}"
        )
        print("Auto-upload for shorts is not executed by this script yet.")
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
