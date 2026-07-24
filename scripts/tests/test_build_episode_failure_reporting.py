from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]


def load_build_episode():
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(
        "build_episode_failure_reporting_test",
        SCRIPTS / "build_episode.py",
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildEpisodeFailureReportingTests(unittest.TestCase):
    def setUp(self):
        self.module = load_build_episode()
        self.module._ACTIVE_EPISODE = 87
        self.module._SYSTEM_EXIT_FAILURE_NOTIFIED = False

    def test_uncaught_runtime_error_reaches_build_log(self):
        with mock.patch.object(self.module, "post_build_log") as post:
            self.module._post_unnotified_failure(
                FileNotFoundError("missing replacement cover asset")
            )
        post.assert_called_once()
        message = post.call_args.args[0]
        self.assertIn("❌ EP087 build failed", message)
        self.assertIn("missing replacement cover asset", message)

    def test_previously_reported_failure_is_not_duplicated(self):
        self.module._SYSTEM_EXIT_FAILURE_NOTIFIED = True
        with mock.patch.object(self.module, "post_build_log") as post:
            self.module._post_unnotified_failure(RuntimeError("already reported"))
        post.assert_not_called()

    def test_successful_system_exit_is_not_reported(self):
        with mock.patch.object(self.module, "post_build_log") as post:
            self.module._post_unnotified_failure(SystemExit(0))
        post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
