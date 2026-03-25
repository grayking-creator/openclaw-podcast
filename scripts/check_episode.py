#!/usr/bin/env python3
"""
Episode QC checker — run before generating audio.
Checks for required structural elements and flags issues.
"""

import sys
import re
import argparse
from pathlib import Path

CHECKS = []
WARNINGS = []
ERRORS = []

def check(label, condition, severity="ERROR", hint=""):
    if condition:
        CHECKS.append(f"  ✅ {label}")
    else:
        msg = f"  {'❌' if severity == 'ERROR' else '⚠️'} {label}"
        if hint:
            msg += f"\n     → {hint}"
        if severity == "ERROR":
            ERRORS.append(msg)
        else:
            WARNINGS.append(msg)

def run_checks(path):
    with open(path, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    first_500_words = ' '.join(content.split()[:500])
    last_500_words = ' '.join(content.split()[-500:])
    word_count = len(content.split())

    print(f"\n📋 Episode QC: {path}")
    print(f"   Word count: {word_count:,}")
    print()

    # ── Intro checks ──────────────────────────────────────────────────────────
    has_host_intro = bool(re.search(r"I'm NOVA|I am NOVA|Welcome to OpenClaw|This is OpenClaw Daily", first_500_words, re.IGNORECASE))
    check("Host introduced within first 500 words", has_host_intro,
          hint="Must include 'I'm NOVA' or 'Welcome to OpenClaw Daily' early in the episode")

    has_show_name = bool(re.search(r"OpenClaw Daily", first_500_words, re.IGNORECASE))
    check("Show name mentioned in intro", has_show_name,
          hint="Must mention 'OpenClaw Daily' near the start")

    has_episode_description = bool(re.search(r"(today|this episode|special|deep.dive|breakdown|we're going to|you'll (learn|know|hear))", first_500_words, re.IGNORECASE))
    check("Episode topic introduced early", has_episode_description,
          hint="First 500 words should tell the listener what this episode is about")

    # ── Outro/close checks ────────────────────────────────────────────────────
    has_outro = bool(re.search(r"(OpenClaw Daily|that'?s? (it|all|a wrap)|thanks? for listening|next (time|episode)|see you|I'?m NOVA)", last_500_words, re.IGNORECASE))
    check("Closing/outro present", has_outro,
          hint="Episode must end with a proper sign-off — show name, host name, or 'thanks for listening'")

    has_single_ending = True
    ending_phrases = re.findall(r"(that'?s? (it|all|a wrap)|thanks? for listening|see you next|until next time|I'?m NOVA.*?\.)", content, re.IGNORECASE)
    if len(ending_phrases) > 3:
        has_single_ending = False
    check("Not too many 'ending' phrases (dedup check)", has_single_ending, severity="WARNING",
          hint=f"Found {len(ending_phrases)} closing phrases — may indicate repeated outro sections")

    # ── Content checks ────────────────────────────────────────────────────────
    check("Minimum length (5,000 words)", word_count >= 5000,
          hint=f"Got {word_count:,} words — target is 6,500–7,500 for a 40–45 min episode")

    check("Target length (6,500+ words)", word_count >= 6500, severity="WARNING",
          hint=f"Got {word_count:,} words — ideally 6,500–7,500")

    has_actionable = bool(re.search(r"(```|install |pip install|brew install|npm install|run:|command:|bash |python |step \d)", content, re.IGNORECASE))
    check("Contains actionable commands or code", has_actionable,
          hint="Technical episodes should include concrete commands/steps")

    # ── Duplicate detection ───────────────────────────────────────────────────
    paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 100]
    seen = {}
    dupes = []
    for i, p in enumerate(paragraphs):
        key = p[:80].lower()
        if key in seen:
            dupes.append(f"paragraph ~{i+1} duplicates ~{seen[key]+1}")
        else:
            seen[key] = i
    check("No duplicate paragraphs detected", len(dupes) == 0, severity="WARNING",
          hint='\n     '.join(dupes[:5]) if dupes else "")

    # ── Format checks ─────────────────────────────────────────────────────────
    has_pause_tags = '[PAUSE]' in content
    check("Contains [PAUSE] tags for natural pacing", has_pause_tags, severity="WARNING",
          hint="Add [PAUSE] markers at natural breathing points")

    broken_emphasis = content.count('[EMPHASIS]') != content.count('[/EMPHASIS]')
    check("Matched [EMPHASIS] tags", not broken_emphasis,
          hint="Mismatched [EMPHASIS] / [/EMPHASIS] tags")

    # ── TTS render check ──────────────────────────────────────────────────────
    # Check whether the _nova.md render exists and is free of spoken speaker labels.
    # If it exists, verify no line passes "NOVA:" or "ALLOY:" through to the TTS engine.
    nova_path = Path(path).parent / (Path(path).stem + '_nova.md')
    if nova_path.exists():
        nova_content = nova_path.read_text(encoding='utf-8', errors='ignore')
        # Each line should be: [NOVA]: <text> or [ALLOY]: <text>
        # The <text> must NOT start with "NOVA:" or "ALLOY:" (would be spoken aloud)
        spoken_label_lines = []
        for line in nova_content.splitlines():
            m = re.match(r'^\[(NOVA|ALLOY)\]:\s*(NOVA|ALLOY):', line)
            if m:
                spoken_label_lines.append(line[:80])
        check("TTS render has no spoken speaker labels",
              len(spoken_label_lines) == 0,
              hint=f"nova.md has {len(spoken_label_lines)} line(s) where 'NOVA:' or 'ALLOY:' would be spoken aloud. Re-run render_nova.py after fixing generate_audio.py scrub.")
    else:
        check("TTS render file exists (_nova.md)",
              False,
              severity="WARNING",
              hint=f"Run render_nova.py to create {nova_path.name} before generating audio")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("Results:")
    for c in CHECKS:
        print(c)
    if WARNINGS:
        print()
        for w in WARNINGS:
            print(w)
    if ERRORS:
        print()
        for e in ERRORS:
            print(e)
        print(f"\n❌ {len(ERRORS)} error(s) — fix before generating audio\n")
        sys.exit(1)
    else:
        print(f"\n✅ All checks passed ({len(WARNINGS)} warning(s))\n")
        sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run QC checks on a podcast episode script')
    parser.add_argument('script', help='Path to episode transcript markdown')
    args = parser.parse_args()
    run_checks(args.script)
