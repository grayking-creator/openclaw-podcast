from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


SCRIPTS_DIR = Path(__file__).resolve().parents[1]


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def review_state(gate, audio_path: Path) -> dict:
    now = datetime.now(timezone.utc)
    state: dict = {}
    gate.record_review_audio(
        state,
        audio_path=audio_path,
        duration="00:01",
        audio_url="https://example.invalid/audio.mp3",
        cover_url="https://example.invalid/cover.png",
    )
    gate.record_review_discord_post(
        state,
        channel_id="episode-channel",
        message_id="review-message",
        posted_at=now.isoformat(),
    )
    return state


def approval_message(*, author_id: str, content: str = "✅", timestamp: str | None = None) -> dict:
    return {
        "author": {"id": author_id, "username": "Toby", "bot": False},
        "content": content,
        "timestamp": timestamp,
        "attachments": [],
    }


class ReviewRoutingTests(unittest.TestCase):
    def test_telegram_review_is_pinned_to_aria(self):
        notifier = load_module("notify_telegram_review")
        guard = load_module("assert_telegram_routing")
        self.assertEqual(notifier.TELEGRAM_ACCOUNT, "default")
        self.assertEqual(notifier.TELEGRAM_TARGET, "8319992332")
        self.assertEqual(guard.TELEGRAM_ACCOUNT, "default")
        self.assertEqual(guard.EXPECTED_BOT_ID, 8260045001)

    def test_newline_slate_serialization_preserves_title_semicolons(self):
        notifier = load_module("notify_telegram_review")
        summary = "First story; with a subtitle\nSecond story"
        self.assertEqual(
            notifier._summary_chunks(summary),
            ["First story; with a subtitle", "Second story"],
        )

    def test_openclaw_camel_case_send_result_is_recorded(self):
        notifier = load_module("notify_telegram_review")
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(notifier, "SEND_RECORD_DIR", Path(tmp)):
                with mock.patch.object(notifier, "_active_audio_sha", "review-sha"):
                    notifier._persist_send_record(
                        84,
                        "ready",
                        json.dumps({
                            "messageId": "14307",
                            "payload": {"result": {"messageId": "14307"}},
                        }),
                    )
                record = json.loads((Path(tmp) / "ep084.json").read_text())
        self.assertEqual(record["ready"]["message_id"], "14307")
        self.assertEqual(record["ready"]["chat_id"], "8319992332")
        self.assertEqual(record["ready"]["account_id"], "default")
        self.assertEqual(record["ready"]["review_audio_sha256"], "review-sha")

    def test_verified_discord_approval_requires_toby_and_post_review_time(self):
        gate = load_module("release_approval_gate")
        with tempfile.TemporaryDirectory() as tmp:
            audio = Path(tmp) / "episode.mp3"
            audio.write_bytes(b"hash-locked-audio")
            state = review_state(gate, audio)
            review_time = datetime.fromisoformat(state["review_audio"]["discord_posted_at"])
            message = approval_message(
                author_id=gate.TOBY_DISCORD_USER_ID,
                timestamp=(review_time + timedelta(seconds=1)).isoformat(),
            )
            with mock.patch.object(gate, "discord_request", return_value=message):
                gate.mark_audio_approved_from_discord(
                    state,
                    audio_path=audio,
                    ep_num=84,
                    approval_message_id="approval-message",
                    token="test-token",
                )
            self.assertEqual(state["audio_approval"]["source"], "verified-discord-message")

    def test_publish_is_an_explicit_discord_approval(self):
        gate = load_module("release_approval_gate")
        with tempfile.TemporaryDirectory() as tmp:
            audio = Path(tmp) / "episode.mp3"
            audio.write_bytes(b"hash-locked-audio")
            state = review_state(gate, audio)
            review_time = datetime.fromisoformat(state["review_audio"]["discord_posted_at"])
            message = approval_message(
                author_id=gate.TOBY_DISCORD_USER_ID,
                content="publish",
                timestamp=(review_time + timedelta(seconds=1)).isoformat(),
            )
            with mock.patch.object(gate, "discord_request", return_value=message):
                gate.mark_audio_approved_from_discord(
                    state,
                    audio_path=audio,
                    ep_num=91,
                    approval_message_id="approval-message",
                    token="test-token",
                )
            self.assertTrue(state["audio_approval"]["approved"])

    def test_unverified_discord_messages_fail_closed(self):
        gate = load_module("release_approval_gate")
        messages = [
            approval_message(author_id="someone-else", timestamp=datetime.now(timezone.utc).isoformat()),
            approval_message(
                author_id=gate.TOBY_DISCORD_USER_ID,
                content="I will go over this later",
                timestamp=datetime.now(timezone.utc).isoformat(),
            ),
            approval_message(author_id=gate.TOBY_DISCORD_USER_ID, timestamp=None),
        ]
        for message in messages:
            with self.subTest(message=message):
                with tempfile.TemporaryDirectory() as tmp:
                    audio = Path(tmp) / "episode.mp3"
                    audio.write_bytes(b"hash-locked-audio")
                    state = review_state(gate, audio)
                    before = copy.deepcopy(state)
                    with mock.patch.object(gate, "discord_request", return_value=message):
                        with self.assertRaises(SystemExit):
                            gate.mark_audio_approved_from_discord(
                                state,
                                audio_path=audio,
                                ep_num=84,
                                approval_message_id="not-an-approval",
                                token="test-token",
                            )
                    self.assertEqual(state["audio_approval"], before["audio_approval"])

    def test_changed_audio_cannot_be_approved(self):
        gate = load_module("release_approval_gate")
        with tempfile.TemporaryDirectory() as tmp:
            audio = Path(tmp) / "episode.mp3"
            audio.write_bytes(b"reviewed-audio")
            state = review_state(gate, audio)
            review_time = datetime.fromisoformat(state["review_audio"]["discord_posted_at"])
            audio.write_bytes(b"changed-after-review")
            message = approval_message(
                author_id=gate.TOBY_DISCORD_USER_ID,
                timestamp=(review_time + timedelta(seconds=1)).isoformat(),
            )
            with mock.patch.object(gate, "discord_request", return_value=message):
                with self.assertRaisesRegex(SystemExit, "hash-locked Discord review"):
                    gate.mark_audio_approved_from_discord(
                        state,
                        audio_path=audio,
                        ep_num=84,
                        approval_message_id="approval-message",
                        token="test-token",
                    )


if __name__ == "__main__":
    unittest.main()
