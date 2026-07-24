from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import json
import signal
import subprocess
import sys
import tempfile
import time
import types
import unittest
from pathlib import Path
from unittest import mock


PODCAST = Path(__file__).resolve().parents[2]
WORKSPACE = PODCAST.parent
PODCAST_SCRIPTS = PODCAST / "scripts"
CROSSFIRE_SHARED = (
    WORKSPACE / "video-workspace/crossfire-series/scripts/shared"
)
ERROR_CHANNEL = "1524923755019636948"
INFO_CHANNEL = "1485243812442804327"


def load_module(name: str, path: Path):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class ActiveBuildLogRoutingTests(unittest.TestCase):
    def test_crossfire_alert_senders_are_helper_first_with_error_fallback(self):
        paths = (
            CROSSFIRE_SHARED / "shorts_watchdog_cron.py",
            CROSSFIRE_SHARED / "shorts_cadence_watchdog.py",
            CROSSFIRE_SHARED / "shorts_upload.py",
        )
        for path in paths:
            with self.subTest(path=path.name):
                source = path.read_text()
                self.assertIn(
                    "from post_build_log import post_build_log as routed_post_build_log",
                    source,
                )
                self.assertIn("routed_post_build_log(msg, error=True)", source)
                self.assertLess(
                    source.index("routed_post_build_log(msg, error=True)"),
                    source.index("urllib.request.Request", source.index("def discord") if "def discord" in source else 0),
                )
                self.assertIn(ERROR_CHANNEL, source)
                self.assertNotIn(INFO_CHANNEL, source)
                self.assertIn("build-log alert undelivered", source)

    def test_crossfire_terminal_failure_is_not_suppressed_by_prior_warning(self):
        module = load_module(
            "crossfire_shorts_upload_routing_test",
            CROSSFIRE_SHARED / "shorts_upload.py",
        )
        alerts: list[str] = []
        module._TERMINAL_FAILURE_ALERT_DELIVERED = False
        with mock.patch.object(module, "main", return_value=3), mock.patch.object(
            module, "_make_discord_fn", return_value=lambda message: alerts.append(message) or True
        ):
            self.assertEqual(module.run_cli(), 3)
        self.assertEqual(len(alerts), 1)
        self.assertIn("FAILED (exit 3)", alerts[0])

        # A delivered warning uses the ordinary callback and must not suppress a
        # later exact terminal summary.
        module._TERMINAL_FAILURE_ALERT_DELIVERED = False
        alerts.clear()
        with mock.patch.object(module, "main", return_value=4), mock.patch.object(
            module, "_make_discord_fn", return_value=lambda message: alerts.append(message) or True
        ):
            module._make_discord_fn()("⚠️ earlier requeue warning")
            self.assertEqual(module.run_cli(), 4)
        self.assertEqual(len(alerts), 2)
        self.assertIn("FAILED (exit 4)", alerts[-1])

    def test_cadence_delivery_failure_does_not_claim_sent_or_suppress_retry(self):
        module = load_module(
            "crossfire_cadence_routing_test",
            CROSSFIRE_SHARED / "shorts_cadence_watchdog.py",
        )
        saved = mock.Mock()
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(module, "crontab_lines", return_value=[]),
            mock.patch.object(module, "queue_statuses", return_value=[]),
            mock.patch.object(module, "build_issues", return_value=[("stalled", "queue stalled")]),
            mock.patch.object(module, "load_state", return_value={}),
            mock.patch.object(module, "discord", return_value=False),
            mock.patch.object(module, "save_state", saved),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            self.assertEqual(module.main(["--series", "ironvane"]), 2)
        saved.assert_not_called()
        self.assertNotIn("ALERT: sent", stdout.getvalue())
        self.assertIn("delivery failed", stderr.getvalue())

    def test_agentstack_error_ack_requires_every_error_delivery(self):
        module = load_module(
            "agentstack_shorts_routing_test",
            PODCAST_SCRIPTS / "upload_agentstack_shorts.py",
        )
        module._ERROR_NOTIFICATION_DELIVERED = False
        module._ERROR_NOTIFICATION_ATTEMPTS = 0
        module._ERROR_NOTIFICATION_FAILURES = 0

        ok_module = types.SimpleNamespace(post_build_log=lambda *_a, **_kw: None)
        with mock.patch.dict(sys.modules, {"post_build_log": ok_module}):
            self.assertTrue(module.discord_build_log("❌ first failure"))
        self.assertTrue(module._ERROR_NOTIFICATION_DELIVERED)

        def fail_post(*_args, **_kwargs):
            raise RuntimeError("offline")

        failed_module = types.SimpleNamespace(post_build_log=fail_post)
        with mock.patch.dict(sys.modules, {"post_build_log": failed_module}), mock.patch.object(
            module, "_load_env_key", return_value=""
        ):
            self.assertFalse(module.discord_build_log("❌ second failure"))
        self.assertEqual(module._ERROR_NOTIFICATION_ATTEMPTS, 2)
        self.assertEqual(module._ERROR_NOTIFICATION_FAILURES, 1)
        self.assertFalse(module._ERROR_NOTIFICATION_DELIVERED)

    def test_shell_wrappers_are_helper_first_with_correct_fallback_channels(self):
        morning = PODCAST_SCRIPTS / "agentstack_morning.sh"
        shorts = PODCAST_SCRIPTS / "agentstack_shorts_cron.sh"
        subprocess.run(["/bin/bash", "-n", str(morning)], check=True)
        subprocess.run(["/bin/bash", "-n", str(shorts)], check=True)
        morning_source = morning.read_text()
        shorts_source = shorts.read_text()
        self.assertIn('"$POST_BUILD_LOG" --info', morning_source)
        self.assertIn('"$POST_BUILD_LOG" --error', morning_source)
        self.assertIn('target "channel:$BUILD_LOG_CHANNEL"', morning_source)
        self.assertIn('target "channel:$BUILD_LOG_ERROR_CHANNEL"', morning_source)
        self.assertIn("morning pipeline DEGRADED", morning_source)
        self.assertIn('"$POST_BUILD_LOG" --error', shorts_source)
        self.assertIn('target "channel:$BUILD_LOG_ERROR_CHANNEL"', shorts_source)
        self.assertIn('error_notification_failures', shorts_source)
        self.assertNotIn("Child completed with handled exit", shorts_source)

    def test_morning_fallback_targets_info_and_error_channels_offline(self):
        source = (PODCAST_SCRIPTS / "agentstack_morning.sh").read_text()
        prefix = source.split('blog "agentstack_morning: starting"', 1)[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_log = root / "build.log"
            helper = root / "helper.py"
            helper.write_text("raise SystemExit(1)\n")
            calls = root / "openclaw.calls"
            openclaw = root / "openclaw"
            openclaw.write_text(
                "#!/bin/bash\n"
                'printf "%s\\n" "$*" >> "$OPENCLAW_CALL_LOG"\n'
                "exit 0\n"
            )
            openclaw.chmod(0o755)
            harness = root / "harness.sh"
            harness.write_text(prefix + '\nalert "progress"\nalert_error "⚠️ degraded"\n')
            env = os.environ.copy()
            env.update(
                {
                    "SHOW_NOTES_BUILD_LOG": str(build_log),
                    "AGENTSTACK_POST_BUILD_LOG": str(helper),
                    "OPENCLAW_BIN": str(openclaw),
                    "OPENCLAW_CALL_LOG": str(calls),
                }
            )
            subprocess.run(["/bin/bash", str(harness)], env=env, check=True)
            routed = calls.read_text()
        self.assertIn(f"channel:{INFO_CHANNEL}", routed)
        self.assertIn(f"channel:{ERROR_CHANNEL}", routed)

    def test_guard_manages_attempt_notifications_and_reports_signal_exit(self):
        guard = PODCAST_SCRIPTS / "show_notes_research_guard.sh"
        morning_source = (PODCAST_SCRIPTS / "agentstack_morning.sh").read_text()
        guard_source = guard.read_text()
        self.assertIn('AGENTSTACK_GUARD_MANAGED=1 /bin/bash "$SCRIPT"', guard_source)
        self.assertIn('trap \'handle_guard_signal TERM 143\' TERM', guard_source)
        self.assertIn('"${AGENTSTACK_GUARD_MANAGED:-0}" = "1"', morning_source)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child_started = root / "child.started"
            child = root / "fake_morning.sh"
            child.write_text(
                "#!/bin/bash\n"
                'printf started > "$FAKE_CHILD_STARTED"\n'
                "while :; do sleep 1; done\n"
            )
            child.chmod(0o755)
            post_log = root / "posts.jsonl"
            helper = root / "post_build_log.py"
            helper.write_text(
                "import json, os, sys\n"
                "with open(os.environ['FAKE_POST_LOG'], 'a') as handle:\n"
                "    handle.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            )
            build_log = root / "build.log"
            run_log = root / "run.log"
            env = os.environ.copy()
            env.update(
                {
                    "SHOW_NOTES_RESEARCH_SCRIPT": str(child),
                    "SHOW_NOTES_POST_BUILD_LOG": str(helper),
                    "SHOW_NOTES_BUILD_LOG": str(build_log),
                    "SHOW_NOTES_RESEARCH_LOG": str(run_log),
                    "SHOW_NOTES_GUARD_MAX_RUNS": "1",
                    "FAKE_CHILD_STARTED": str(child_started),
                    "FAKE_POST_LOG": str(post_log),
                }
            )
            proc = subprocess.Popen(
                ["/bin/bash", str(guard)],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
            )
            deadline = time.time() + 5
            while not child_started.exists() and time.time() < deadline:
                time.sleep(0.05)
            self.assertTrue(child_started.exists(), "fake morning child never started")
            os.killpg(proc.pid, signal.SIGTERM)
            proc.communicate(timeout=10)

            self.assertEqual(proc.returncode, 143)
            self.assertIn("terminated by SIGTERM", build_log.read_text())
            posts = [json.loads(line) for line in post_log.read_text().splitlines()]
            self.assertEqual(len(posts), 1)
            self.assertIn("terminated by SIGTERM", " ".join(posts[0]))

    def test_guard_managed_stage_failure_does_not_dispatch_attempt_error(self):
        source = (PODCAST_SCRIPTS / "agentstack_morning.sh").read_text()
        prefix = source.split('blog "agentstack_morning: starting"', 1)[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_log = root / "build.log"
            post_log = root / "posts.log"
            helper = root / "post_build_log.py"
            helper.write_text(
                "import os\n"
                "with open(os.environ['FAKE_POST_LOG'], 'a') as handle:\n"
                "    handle.write('posted\\n')\n"
            )
            harness = root / "harness.sh"
            harness.write_text(
                prefix
                + '\nNEXT_EP_PAD=087\nfail_stage "transcript" "deterministic failure"\n'
            )
            env = os.environ.copy()
            env.update(
                {
                    "SHOW_NOTES_BUILD_LOG": str(build_log),
                    "AGENTSTACK_POST_BUILD_LOG": str(helper),
                    "AGENTSTACK_POST_BUILD_LOG_PYTHON": sys.executable,
                    "AGENTSTACK_GUARD_MANAGED": "1",
                    "FAKE_POST_LOG": str(post_log),
                }
            )
            result = subprocess.run(["/bin/bash", str(harness)], env=env, check=False)

            self.assertEqual(result.returncode, 1)
            self.assertFalse(post_log.exists())
            self.assertIn("guard-managed attempt failure", build_log.read_text())

    def test_repair_prompt_requires_canonical_review_delivery(self):
        watcher = load_module(
            "sol_build_repair_watcher_prompt_test",
            PODCAST_SCRIPTS / "sol_build_repair_watcher.py",
        )
        prompt = watcher.build_repair_prompt(
            {
                "id": "123",
                "timestamp": "2026-07-15T10:59:13Z",
                "content": "❌ EP087 morning pipeline FAILED at stage: transcript",
            }
        )
        self.assertIn("canonical review delivery is part of the required terminal artifact", prompt)
        self.assertIn("Never use --dry-run, --skip-telegram, --skip-discord", prompt)
        self.assertIn("These canonical review posts are allowed", prompt)
        self.assertNotIn(
            "Never post to Discord, episode channels, or Telegram from the repair turn.",
            prompt,
        )

    def test_repair_prompt_routes_ironvane_oauth_to_lilly(self):
        watcher = load_module(
            "sol_build_repair_watcher_ironvane_prompt_test",
            PODCAST_SCRIPTS / "sol_build_repair_watcher.py",
        )
        prompt = watcher.build_repair_prompt(
            {
                "id": "1526865160298565805",
                "timestamp": "2026-07-15T08:17:01Z",
                "content": "❌ Shorts watchdog (--watchdog-all) FAILED: invalid_grant",
            }
        )
        self.assertIn("profile named Lilly", prompt)
        self.assertIn("lillyaxolotlgamer@gmail.com", prompt)
        self.assertIn("UCMx7-QZTE_RkcDxpBMZplPA", prompt)
        self.assertIn("auth/auth_crossfire_loopback.py", prompt)
        self.assertIn("Never use Profile 2", prompt)
        self.assertIn("shorts_upload.py --watchdog-all", prompt)
        self.assertIn("Do not pass", prompt)
        self.assertIn("--source-error", prompt)


if __name__ == "__main__":
    unittest.main()
