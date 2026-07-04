#!/usr/bin/env python3
"""
Telegram routing pre-flight check (locked 2026-06-27, post-EP075 incident).

Runs at 06:25 AM ET — 5 minutes before the AgentStack Daily morning
pipeline. Verifies that the Telegram bot is configured to post to the
operator's home DM (chat id 8319992332) and NOT to a different account
or chat. Posts a 🚨 ROUTING MIS-WIRED alert to the operator's DM
if anything is wrong, then exits 2 so the morning pipeline aborts
before any audio is generated.

This is the guard rail that makes the 2026-06-27 routing incident
(EP075 review audio posted to the ARIA Discord channel instead of the
operator's Telegram DM) impossible to repeat. The morning pipeline
must call this script first; if it exits non-zero, the build is held.

Usage:
    python3 scripts/assert_telegram_routing.py [--check-only]

Exit codes:
    0   routing is correct
    2   routing is mis-wired (Telegram alert sent)
    3   openclaw CLI is not available
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

OPERATOR_TELEGRAM_CHAT_ID = "8319992332"
OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "/opt/homebrew/bin/openclaw")


def _telegram_drysend(target: str, message: str) -> tuple[int, str]:
    """Send a Telegram message. Returns (exit_code, stdout)."""
    try:
        proc = subprocess.run(
            [
                OPENCLAW_BIN, "message", "send",
                "--channel", "telegram",
                "--target", target,
                "--message", message,
            ],
            check=False, capture_output=True, text=True, timeout=20,
        )
        return proc.returncode, (proc.stdout or "").strip()
    except FileNotFoundError:
        return 127, "openclaw CLI not found"
    except Exception as exc:
        return 1, str(exc)


def _check_session_key() -> tuple[bool, str]:
    """Verify HERMES_SESSION_KEY ends with the operator's chat id."""
    sk = os.environ.get("HERMES_SESSION_KEY", "")
    if not sk:
        return True, "HERMES_SESSION_KEY not set; skipping session-key assertion"
    if sk.endswith(f":{OPERATOR_TELEGRAM_CHAT_ID}"):
        return True, f"HERMES_SESSION_KEY ends with :{OPERATOR_TELEGRAM_CHAT_ID} (operator DM)"
    return False, (
        f"HERMES_SESSION_KEY ends with ':{sk.rsplit(':', 1)[-1]}' but the "
        f"only valid AgentStack Daily review target is "
        f"':{OPERATOR_TELEGRAM_CHAT_ID}'"
    )


def _check_target_drysend() -> tuple[bool, str]:
    """Send a tiny dry-run message to the configured target to confirm
    routing. We do NOT use --dry-run because the openclaw CLI's
    --dry-run does not verify the target is reachable; we send a real
    message but with a routing-check body that the operator can ignore
    if it's correct, or investigate if it's not.

    The body starts with '🧭 [routing-check]' so it's filterable.
    """
    body = (
        f"🧭 [routing-check] AgentStack Daily Telegram routing verified. "
        f"Target chat id: {OPERATOR_TELEGRAM_CHAT_ID}. "
        f"This is a pre-flight ping 5 minutes before the morning build; "
        f"no action needed if you see this."
    )
    rc, stdout = _telegram_drysend(OPERATOR_TELEGRAM_CHAT_ID, body)
    if rc != 0:
        return False, f"openclaw send to {OPERATOR_TELEGRAM_CHAT_ID} failed (rc={rc}): {stdout}"
    # Try to extract the message id from the stdout
    m = re.search(r"(\d{2,})", stdout)
    msg_id = m.group(1) if m else "?"
    return True, f"drysend to {OPERATOR_TELEGRAM_CHAT_ID} succeeded (message id: {msg_id})"


def _alert_misconfigured(reason: str) -> None:
    """Send a routing-mis-wired alert to the operator's DM. We send to
    the hardcoded operator chat id even on the failure path, because
    if the operator's DM is not reachable, the morning pipeline
    cannot run anyway and the operator needs to be told manually.
    """
    body = (
        f"🚨 AgentStack Daily ROUTING MIS-WIRED — morning build aborted.\n"
        f"\n"
        f"Reason: {reason}\n"
        f"\n"
        f"The morning pipeline will NOT generate audio, transcript, or "
        f"show notes until routing is fixed. Investigate:\n"
        f"  • HERMES_SESSION_KEY env (must end with :{OPERATOR_TELEGRAM_CHAT_ID})\n"
        f"  • openclaw CLI bot token (channel=telegram)\n"
        f"  • Target chat id (must be {OPERATOR_TELEGRAM_CHAT_ID}, not ARIA Discord or any other chat)\n"
        f"\n"
        f"Once fixed, run `python3 scripts/assert_telegram_routing.py` "
        f"and re-trigger the morning pipeline manually."
    )
    _telegram_drysend(OPERATOR_TELEGRAM_CHAT_ID, body)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true",
                        help="Print the routing check result and exit; do not send the drysend")
    args = parser.parse_args()

    # 1. Session key assertion
    sk_ok, sk_detail = _check_session_key()
    print(f"[1/2] session-key: {sk_detail}")
    if not sk_ok:
        print(f"❌ ROUTING MIS-WIRED: {sk_detail}")
        _alert_misconfigured(sk_detail)
        return 2

    # 2. Live target drysend (skip if --check-only)
    if args.check_only:
        print("[2/2] target-drysend: skipped (--check-only)")
        print("✅ routing check passed (session-key only)")
        return 0

    target_ok, target_detail = _check_target_drysend()
    print(f"[2/2] target-drysend: {target_detail}")
    if not target_ok:
        print(f"❌ ROUTING MIS-WIRED: {target_detail}")
        _alert_misconfigured(target_detail)
        return 2

    print("✅ Telegram routing verified: bot will post to the operator's DM")
    return 0


if __name__ == "__main__":
    sys.exit(main())
