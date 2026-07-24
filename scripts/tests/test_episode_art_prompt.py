import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "generate_episode_art.py"
SPEC = importlib.util.spec_from_file_location("generate_episode_art", SCRIPT)
ART = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ART)


EP087_NOTES = """# AgentStack Daily EP087 — Verifier-Based RL, TerraZero, PalmClaw, and the Estimate-Execute-Expand Token Optimization

**Title:** PalmClaw Mobile Framework, TerraZero RL at 1.3M Steps, and 91% Token Reductions for Coding Agents

**Tagline:** TerraZero introduces demonstration-free RL driving at 1.3M steps per second, while Estimate, Execute, Expand cuts coding-agent tokens by 91 percent.
"""

EP087_CURRENT_NOTES = """# AgentStack Daily EP087 — GPT-5.6 Sol, Offline Pixel AI, and 128GB AMD Desktops

**Title:** GPT-5.6 Sol, Bonsai 27B, Gemini 3.5 Flash, and AMD 128GB PCs

**Tagline:** GPT-5.6 Sol aims to move agents from partial answers to finished work, while Bonsai 27B fits multimodal AI into phone-sized memory.
"""


class EpisodeArtPromptTests(unittest.TestCase):
    def test_current_inline_metadata_format_is_parsed(self):
        self.assertEqual(
            ART.extract_episode_title(EP087_NOTES, 87),
            "PalmClaw Mobile Framework, TerraZero RL at 1.3M Steps, and 91% Token Reductions for Coding Agents",
        )
        self.assertIn("demonstration-free RL driving", ART.extract_tagline(EP087_NOTES))

    def test_agentstack_heading_is_supported_without_inline_title(self):
        notes = "# AgentStack Daily EP088 — A Truly Specific Headline\n"
        self.assertEqual(ART.extract_episode_title(notes, 88), "A Truly Specific Headline")

    def test_terrazero_prompt_requires_title_specific_scene(self):
        prompt = ART.build_prompt(87, EP087_NOTES)
        self.assertIn("autonomous car", prompt)
        self.assertIn("real smartphone", prompt)
        self.assertIn("shrinks a large token stream by 91 percent", prompt)
        self.assertIn("not as a generic control desk", prompt)

    def test_current_ep087_prompt_bans_the_rejected_generic_scene(self):
        prompt = ART.build_prompt(87, EP087_CURRENT_NOTES)
        self.assertIn("finished-work capability", prompt)
        self.assertIn("3.9 GB memory motif", prompt)
        self.assertIn("128 GB unified memory", prompt)
        self.assertIn("instead of a glowing core", prompt)

    def test_prompt_withholds_episode_number_and_podcast_branding(self):
        prompt = ART.build_prompt(87, EP087_NOTES)
        self.assertNotIn("EP087", prompt)
        self.assertNotIn("episode 087", prompt.lower())
        self.assertNotIn("episode 87", prompt.lower())
        self.assertNotIn("AgentStack Daily", prompt)


if __name__ == "__main__":
    unittest.main()
