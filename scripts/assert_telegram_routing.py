#!/usr/bin/env python3
"""
Telegram routing pre-flight check (locked 2026-06-27, post-EP075 incident).

Runs before the AgentStack Daily morning pipeline. Verifies that OpenClaw's
``default`` Telegram account is configured, healthy, and resolves to ARIA's
immutable Telegram bot id (currently @TobyCoderBot). It never sends a
routing-check message; a credential probe is
enough to verify bot identity without cluttering the operator's review chat.

This prevents a future secondary Telegram account from silently capturing
the podcast workflow. The morning pipeline must call this script first; if it
exits non-zero, the build is held.

Usage:
    python3 scripts/assert_telegram_routing.py [--check-only]

Exit codes:
    0   routing is correct
    2   routing is mis-wired
    3   openclaw CLI is not available
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

OPERATOR_TELEGRAM_CHAT_ID = "8319992332"
TELEGRAM_ACCOUNT = "default"
EXPECTED_BOT_ID = 8260045001
OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "/opt/homebrew/bin/openclaw")


def _check_named_account() -> tuple[bool, str]:
    """Probe ARIA through OpenClaw and verify its exact bot identity."""
    try:
        proc = subprocess.run(
            [
                OPENCLAW_BIN, "channels", "status",
                "--channel", "telegram",
                "--probe", "--json",
            ],
            check=False, capture_output=True, text=True, timeout=30,
        )
    except FileNotFoundError:
        return False, "openclaw CLI not found"
    except Exception as exc:
        return False, str(exc)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "unknown error").strip()
        return False, f"OpenClaw Telegram probe failed (rc={proc.returncode}): {detail}"
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return False, f"OpenClaw Telegram probe returned invalid JSON: {exc}"
    accounts = ((payload.get("channelAccounts") or {}).get("telegram") or [])
    account = next(
        (item for item in accounts if str(item.get("accountId")) == TELEGRAM_ACCOUNT),
        None,
    )
    if not account:
        return False, f"Telegram account {TELEGRAM_ACCOUNT!r} is not configured"
    probe = account.get("probe") or {}
    bot = probe.get("botInfo") or probe.get("bot") or {}
    username = str(bot.get("username") or "")
    bot_id = int(bot.get("id") or 0)
    if probe.get("ok") is not True:
        return False, f"Telegram account {TELEGRAM_ACCOUNT!r} probe failed: {probe.get('error')}"
    if bot_id != EXPECTED_BOT_ID:
        return False, (
            f"Telegram account {TELEGRAM_ACCOUNT!r} resolves to bot id {bot_id or '?'} "
            f"(@{username or '?'}); expected ARIA bot id {EXPECTED_BOT_ID}"
        )
    if account.get("configured") is not True:
        return False, f"Telegram account {TELEGRAM_ACCOUNT!r} is not configured"
    return True, (
        f"OpenClaw account {TELEGRAM_ACCOUNT!r} resolves to @{username} "
        f"(bot id {bot_id}); "
        f"review target is {OPERATOR_TELEGRAM_CHAT_ID}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only", action="store_true",
        help="Compatibility flag; probes credentials and never sends a message.",
    )
    parser.parse_args()

    account_ok, detail = _check_named_account()
    print(f"[1/1] named-account probe: {detail}")
    if not account_ok:
        print(f"❌ ROUTING MIS-WIRED: {detail}")
        return 2

    print("✅ Telegram routing verified: podcast sends use ARIA (--account default)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
