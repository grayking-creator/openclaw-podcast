#!/usr/bin/env python3
"""
Fresh-research gate (locked 2026-06-27, EP075 incident class).

The hard rule: AgentStack Daily may only build today's episode from research
that is (a) < 24h old, (b) not used by any prior episode, and (c) reflects
real movement (YouTube channel counter must have advanced since the prior
release). If any check fails the morning pipeline must NOT regenerate — it
posts a Telegram alert naming which gate failed and exits 0.

The "no duplicate ever" invariant is owned here. The morning pipeline calls
this script at the very top of Stage 1; if it exits non-zero, the rest of
the morning run is skipped and no show notes, transcript, or audio is
generated.

Usage:
    python3 scripts/fresh_research_gate.py [NEXT_EP]
        NEXT_EP defaults to the integer after scripts/youtube_uploaded.txt's
        last value.

Exit codes:
    0   Gate PASSED — proceed to the morning pipeline.
    2   Gate FAILED — pipeline must NOT build; a Telegram alert was sent.
    3   Gate FAILED — research context missing or unreadable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPT_DIR.parent
DONE_FILE = SCRIPT_DIR / "youtube_uploaded.txt"
RESEARCH_JSON = Path("/tmp/agent_research_context.json")
RESEARCH_MD = Path("/tmp/agent_research_context.md")

# Telegram is the only review surface going forward (locked 2026-06-27).
TELEGRAM_CHANNEL = "telegram"
TELEGRAM_TARGET = os.environ.get("PODCAST_TELEGRAM_TARGET", "8319992332")
OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "/opt/homebrew/bin/openclaw")

# Research is only "fresh" if it was gathered within this many hours.
MAX_AGE_HOURS = 24

# Auto-refresh budget — the gate calls gather_research_context.py itself when
# on-disk research is stale, instead of bailing and forcing the operator to
# re-run it by hand. Why this exists (locked 2026-06-29, EP076 incident):
# the original ordering (gate runs in Stage 0, BEFORE the morning script's
# Stage 3 gather) meant a stale research artifact could block the pipeline
# indefinitely, while the bail-out Telegram message told the operator to
# re-run the very script the morning pipeline should be running. The fix is
# for the gate to be self-healing: stale → call gather → re-check.
GATHER_SCRIPT = SCRIPT_DIR / "gather_research_context.py"
# 360s (was 240): the 2026-07-04 source expansion added ~15 network sources
# plus deliberate inter-request sleeps on the Reddit lane (unauthenticated
# fetches 429 without ~10s spacing between subreddits).
GATHER_TIMEOUT_SECONDS = 360


def _next_ep_from_done_file() -> int:
    if not DONE_FILE.exists():
        raise SystemExit(f"missing episode counter: {DONE_FILE}")
    last = (DONE_FILE.read_text().strip().splitlines() or ["0"])[-1].strip()
    if not last.isdigit():
        raise SystemExit(f"episode counter not numeric: {last!r}")
    return int(last) + 1


def _read_research_mtime() -> float:
    """mtime of whichever research artifact is newer."""
    candidates = [p for p in (RESEARCH_JSON, RESEARCH_MD) if p.exists()]
    if not candidates:
        return 0.0
    return max(p.stat().st_mtime for p in candidates)


def _research_context_hash() -> str:
    if not RESEARCH_JSON.exists():
        return ""
    h = hashlib.sha256()
    with RESEARCH_JSON.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _all_release_hashes() -> set[str]:
    """Walk every release_ep*_state.json and collect the
    research_context_hash entries recorded there. Empty hashes are skipped
    (older episodes predate this gate and never recorded a hash)."""
    seen: set[str] = set()
    pattern = re.compile(r"^release_ep(\d{3})_state\.json$")
    for path in sorted(SCRIPT_DIR.glob("release_ep*_state.json")):
        m = pattern.match(path.name)
        if not m:
            continue
        try:
            state = json.loads(path.read_text())
        except Exception:
            continue
        for key in ("research_context_hash", "approved_orchestrator"):
            if key == "research_context_hash" and isinstance(state.get(key), str):
                if state[key]:
                    seen.add(state[key])
            elif key == "approved_orchestrator":
                inner = state.get(key) or {}
                val = inner.get("research_context_hash")
                if isinstance(val, str) and val:
                    seen.add(val)
    return seen


def _prior_release_state_exists(ep_num: int) -> bool:
    """True if a release_ep{NNN}_state.json exists for the most recent
    released episode. If not, this is the first-ever run and the "no
    duplicate" check is a no-op."""
    # The prior released episode is the one whose state file is the newest
    # among those with completed_phases non-empty AND audio_approval.approved
    # == True.
    candidates = []
    for path in SCRIPT_DIR.glob("release_ep*_state.json"):
        m = re.match(r"^release_ep(\d{3})_state\.json$", path.name)
        if not m:
            continue
        ep = int(m.group(1))
        try:
            state = json.loads(path.read_text())
        except Exception:
            continue
        if (state.get("audio_approval") or {}).get("approved") is True:
            candidates.append((ep, path))
    if not candidates:
        return False
    candidates.sort(key=lambda x: x[0])
    last_ep, last_path = candidates[-1]
    return last_ep, last_path  # type: ignore[return-value]


def _counter_advanced_since(ep_num: int) -> Tuple[bool, str]:
    """Advisory check: the YouTube channel counter should have advanced
    since the prior released episode. If it hasn't, it usually means
    the release side is stuck on a prior episode — the operator wants
    to know about it, but the morning build is not the place to block
    on it. We log a warning rather than fail the gate.

    Returns (advanced, detail). advanced is True if the counter has
    moved, the counter is unknown, or there is no prior approved
    release. detail is a human-readable explanation.
    """
    if not RESEARCH_JSON.exists():
        return True, "research context missing — counter check skipped"
    try:
        ctx = json.loads(RESEARCH_JSON.read_text())
    except Exception:
        return True, "research context unreadable — counter check skipped"
    last_uploaded = ctx.get("last_uploaded_episode")
    prior = _prior_release_state_exists(ep_num)
    if isinstance(prior, tuple):
        prior_ep = prior[0]
    else:
        return True, "no prior approved release on record"
    if last_uploaded is None:
        return True, (
            f"research context has no last_uploaded_episode field; "
            f"counter check skipped (prior release was EP{prior_ep:03d})"
        )
    if int(last_uploaded) <= int(prior_ep):
        return False, (
            f"YouTube counter has not advanced since EP{prior_ep:03d} "
            f"(last_uploaded_episode={last_uploaded}). The release side "
            f"may be stuck — this is advisory and does not block the "
            f"morning build, but the operator should check the orchestrator."
        )
    return True, (
        f"counter advanced: research last_uploaded_episode={last_uploaded} > "
        f"prior release EP{prior_ep:03d}"
    )


def _send_telegram(message: str) -> None:
    """Gate bail-out destination handler — DEPRECATED for Telegram.

    Locked 2026-06-29, EP076 incident: Telegram is reserved for explicit
    approvals / decision requests, never for gate failures or pipeline
    diagnostics. This function now routes EVERY bail-out to the Discord
    Build Log via the workspace post_build_log utility. Operators find
    these in the same channel as every other pipeline event. Bail-out
    messages must point operators at LOGS, never at "run this script".

    The Telegram token lookup / direct send code is removed entirely to
    stop the ARIA-channel misroute that recurred on EP076.
    """
    try:
        import subprocess
        # Truncate the message to Discord's 2000-char limit
        chunk = message if len(message) <= 1900 else (message[:1900] + "\n... (truncated)")
        subprocess.run(
            [sys.executable,
             "/Users/tobyglennpeters/.openclaw/workspace/scripts/utils/post_build_log.py",
             chunk],
            timeout=15,
            check=False,
        )
    except Exception as exc:
        # Last-resort: print to stderr only — never reach for Telegram.
        print(f"fresh_research_gate: WARN Discord Build Log delivery failed: {exc}", file=sys.stderr)


def _auto_refresh_research() -> bool:
    """Re-run gather_research_context.py when on-disk research is stale,
    so the morning pipeline can self-heal instead of bailing into a
    're-run this script' Telegram alert. Locked 2026-06-29, EP076
    incident: the previous ordering had the gate run BEFORE the morning
    pipeline's gather stage, which meant a stale artifact could block
    every morning indefinitely while the bail-out message told the
    operator to manually re-run the very script the morning pipeline
    should be running. The fix is for the gate to be self-healing:
    stale → call gather → re-check. Returns True if the refresh wrote
    new research JSON (callers should re-run the freshness check),
    False on any error (script missing, non-zero exit, timeout, empty
    output)."""
    if not GATHER_SCRIPT.exists():
        print(
            f"fresh_research_gate: WARN gather script missing: {GATHER_SCRIPT}",
            file=sys.stderr,
        )
        return False
    try:
        proc = subprocess.run(
            [sys.executable, str(GATHER_SCRIPT)],
            timeout=GATHER_TIMEOUT_SECONDS,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        print(
            f"fresh_research_gate: WARN gather timed out after "
            f"{GATHER_TIMEOUT_SECONDS}s — falling back to stale-on-disk",
            file=sys.stderr,
        )
        return False
    except Exception as exc:  # pragma: no cover — defensive
        print(f"fresh_research_gate: WARN gather crashed: {exc}", file=sys.stderr)
        return False
    if proc.returncode != 0:
        print(
            f"fresh_research_gate: WARN gather exited {proc.returncode} "
            "— falling back to stale-on-disk",
            file=sys.stderr,
        )
        return False
    if not RESEARCH_JSON.exists() or RESEARCH_JSON.stat().st_size == 0:
        print(
            "fresh_research_gate: WARN gather wrote no research JSON "
            "— falling back to stale-on-disk",
            file=sys.stderr,
        )
        return False
    print("fresh_research_gate: auto-refreshed research context")
    return True


def _check_freshness() -> Tuple[bool, str]:
    if not RESEARCH_JSON.exists() and not RESEARCH_MD.exists():
        return False, "no /tmp/agent_research_context.{json,md} on disk"
    mtime = _read_research_mtime()
    if mtime == 0.0:
        return False, "research artifacts exist but report zero mtime"
    age_hours = (time.time() - mtime) / 3600.0
    if age_hours > MAX_AGE_HOURS:
        return False, (
            f"research is stale: {age_hours:.1f}h old > {MAX_AGE_HOURS}h "
            f"limit (mtime={time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))})"
        )
    return True, f"research age {age_hours:.1f}h (<= {MAX_AGE_HOURS}h)"


def _check_no_duplicate(ep_num: int) -> Tuple[bool, str]:
    h = _research_context_hash()
    if not h:
        return False, "research context hash is empty — refusing to build"
    seen = _all_release_hashes()
    if h in seen:
        return False, (
            f"research context hash {h[:12]}… was already used by a prior "
            f"episode; refusing to build a duplicate"
        )
    advanced, counter_detail = _counter_advanced_since(ep_num)
    counter_note = "" if advanced else f" (advisory: {counter_detail})"
    return True, f"research hash {h[:12]}… not seen in any prior release{counter_note}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "next_ep", nargs="?", type=int, default=None,
        help="next episode number (defaults to youtube_uploaded.txt + 1)",
    )
    parser.add_argument(
        "--no-telegram", action="store_true",
        help="do not post the Telegram alert on a gate failure (CI / test mode)",
    )
    args = parser.parse_args()

    try:
        next_ep = args.next_ep or _next_ep_from_done_file()
    except SystemExit as exc:
        print(f"fresh_research_gate: {exc}", file=sys.stderr)
        return 3

    print(f"fresh_research_gate: checking EP{next_ep:03d}")

    fresh_ok, fresh_detail = _check_freshness()
    if not fresh_ok:
        # Self-heal path: instead of forcing the operator to re-run the
        # gather script by hand (the EP076 incident on 2026-06-29), the
        # gate attempts an in-place refresh and re-checks. Only after a
        # refresh failure do we bail to the build log.
        print(
            "fresh_research_gate: freshness failed "
            f"({fresh_detail}); attempting auto-refresh",
            file=sys.stderr,
        )
        if _auto_refresh_research():
            fresh_ok, fresh_detail = _check_freshness()
        if not fresh_ok:
            msg = (
                f"🛑 EP{next_ep:03d} SKIPPED — fresh-research gate failed "
                f"(freshness + auto-refresh failed).\n"
                f"Reason: {fresh_detail}\n"
                f"Rule: AgentStack Daily may not build from research older "
                f"than {MAX_AGE_HOURS}h; the gate tried to re-gather in place "
                f"but the gather script did not produce fresh artifacts. "
                f"Inspect scripts/gather_research_context.py logs."
            )
            print(
                f"fresh_research_gate: FAIL {fresh_detail} "
                "(auto-refresh did not heal)",
                file=sys.stderr,
            )
            if not args.no_telegram:
                _send_telegram(msg)
            return 2
        print(
            f"fresh_research_gate: freshness healed after auto-refresh "
            f"({fresh_detail})"
        )

    no_dup_ok, no_dup_detail = _check_no_duplicate(next_ep)
    if not no_dup_ok:
        msg = (
            f"🛑 EP{next_ep:03d} SKIPPED — fresh-research gate failed (no-duplicate).\n"
            f"Reason: {no_dup_detail}"
        )
        print(f"fresh_research_gate: FAIL {no_dup_detail}", file=sys.stderr)
        if not args.no_telegram:
            _send_telegram(msg)
        return 2

    print(f"fresh_research_gate: PASS ({fresh_detail}; {no_dup_detail})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
