import unittest

from scripts.podcast_description import prepare_episode_summary, sanitize_episode_summary


class PodcastDescriptionTests(unittest.TestCase):
    def test_timestamped_transcript_becomes_concise_summary(self):
        raw = """[00:00] INTRO / HOOK
OpenClaw 2026.4.8 adds unified inference, session checkpoints, and restored
memory. Glasswing and new local training research round out the episode.
[02:00] STORY 1 - OpenClaw 2026.4.8
More transcript text follows here."""

        summary = prepare_episode_summary(raw, fallback="Episode 26")

        self.assertGreaterEqual(len(summary), 120)
        self.assertLessEqual(len(summary), 160)
        self.assertNotIn("[00:00]", summary)
        self.assertNotIn("STORY 1", summary)

    def test_removes_markdown_and_show_notes_link(self):
        raw = """```md
## Show Notes
[00:00] INTRO / HOOK
Codex and OpenClaw ship practical agent updates for daily workflows.
Show notes: https://tobyonfitnesstech.com/podcasts/episode-55/
```"""

        self.assertEqual(
            sanitize_episode_summary(raw),
            "Codex and OpenClaw ship practical agent updates for daily workflows.",
        )

    def test_fallback_never_returns_raw_timestamp(self):
        summary = prepare_episode_summary(
            "[00:00] INTRO / HOOK",
            fallback="Episode 94: Agent Releases and MCP Tools",
        )

        self.assertNotRegex(summary, r"\[\d{1,2}:\d{2}\]")
        self.assertLessEqual(len(summary), 160)


if __name__ == "__main__":
    unittest.main()
