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

    # ── Cold open + intro checks ───────────────────────────────────────────────
    # Cold open: unlabelled dramatic prose before first speaker label, within first ~112 words (45 sec @ 150wpm)
    first_112_words = ' '.join(content.split()[:112])
    first_speaker_match = re.search(r'(\[NOVA\]|\[ALLOY\]|\*?\*?NOVA\*?\*?|\*?\*?ALLOY\*?\*?):', content)
    words_before_first_speaker = len(content[:first_speaker_match.start()].split()) if first_speaker_match else 0
    has_cold_open = words_before_first_speaker >= 10
    check("Cold open present before first speaker label", has_cold_open,
          hint=f"Episode must open with unlabelled dramatic prose (cold open) before NOVA/ALLOY speak. "
               f"Currently {words_before_first_speaker} words before first speaker label — need at least 10.")

    # Host intro with show name within first 112 words after cold open (≈45 sec)
    first_300_words = ' '.join(content.split()[:300])
    has_host_intro = bool(re.search(r"I'm NOVA|I am NOVA|Welcome to OpenClaw|This is OpenClaw Daily", first_300_words, re.IGNORECASE))
    check("Host intro ('I'm NOVA / This is OpenClaw Daily') within first 300 words", has_host_intro,
          hint="Must include 'I'm NOVA' or 'This is OpenClaw Daily' shortly after the cold open")

    has_show_name = bool(re.search(r"OpenClaw Daily", first_500_words, re.IGNORECASE))
    check("Show name mentioned in intro", has_show_name,
          hint="Must mention 'OpenClaw Daily' near the start")

    # ALLOY must introduce herself within the first 400 words
    first_400_words = ' '.join(content.split()[:400])
    has_alloy_intro = bool(re.search(r"I'?m ALLOY|I am ALLOY", first_400_words, re.IGNORECASE))
    check("ALLOY self-introduction within first 400 words", has_alloy_intro,
          hint="ALLOY must say 'I'm ALLOY' (or 'I am ALLOY') shortly after NOVA's intro. Both hosts must introduce themselves.")

    # NOVA and ALLOY introductions must be back-to-back (no more than 3 lines apart)
    lines = content.splitlines()
    nova_intro_line = next((i for i, l in enumerate(lines) if re.search(r"I'?m NOVA", l, re.IGNORECASE)), None)
    alloy_intro_line = next((i for i, l in enumerate(lines) if re.search(r"I'?m ALLOY|I am ALLOY", l, re.IGNORECASE) and i < 30), None)
    if nova_intro_line is not None and alloy_intro_line is not None:
        gap = alloy_intro_line - nova_intro_line
        intros_adjacent = 1 <= gap <= 4
    else:
        intros_adjacent = False
    check("NOVA and ALLOY introductions are back-to-back (within 4 lines)", intros_adjacent,
          hint="After 'I'm NOVA', ALLOY must say 'I'm ALLOY' within the next 1-4 lines. They must form a single intro unit.")

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
          hint=f"Got {word_count:,} words — minimum is 5,000 to guarantee 30+ min audio")

    check("Target length (5,500+ words)", word_count >= 5500, severity="WARNING",
          hint=f"Got {word_count:,} words — 5,500+ gives comfortable 30-35 min episodes")

    # Local paths / IPs must never appear in a public transcript
    local_path_matches = re.findall(r'/Users/[^\s\]\"\']+|/home/[^\s\]\"\']+', content)
    local_ip_matches = re.findall(r'192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+|localhost:\d+', content)
    check("No local file paths in transcript", len(local_path_matches) == 0,
          hint=f"Found local paths: {local_path_matches[:3]}")
    check("No local IP addresses or localhost ports in transcript", len(local_ip_matches) == 0,
          hint=f"Found local addresses: {local_ip_matches[:3]}")

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

    # ── Voice / conversational flow checks ──────────────────────────────────
    nova_lines = len(re.findall(r'^(\[NOVA\]|\*?\*?NOVA\*?\*?):\s', content, re.MULTILINE))
    alloy_lines = len(re.findall(r'^(\[ALLOY\]|\*?\*?ALLOY\*?\*?):\s', content, re.MULTILINE))
    check(f"Both hosts present (NOVA={nova_lines}, ALLOY={alloy_lines})",
          nova_lines >= 5 and alloy_lines >= 5,
          hint=f"NOVA has {nova_lines} lines, ALLOY has {alloy_lines} lines. Both must have 5+.")

    if nova_lines + alloy_lines > 0:
        ratio = min(nova_lines, alloy_lines) / max(nova_lines, alloy_lines)
        check(f"Host balance ratio ({ratio:.0%} — want >25%)", ratio >= 0.25,
              hint=f"NOVA={nova_lines}, ALLOY={alloy_lines}. One host is dominating — add more back-and-forth.")

    # Check for conversational back-and-forth (no monologues >5 consecutive same-speaker blocks)
    speaker_sequence = re.findall(r'^\*?\*?(NOVA|ALLOY)\*?\*?:', content, re.MULTILINE)
    max_consecutive = 1
    current_run = 1
    for i in range(1, len(speaker_sequence)):
        if speaker_sequence[i] == speaker_sequence[i-1]:
            current_run += 1
            max_consecutive = max(max_consecutive, current_run)
        else:
            current_run = 1
    check(f"No monologue runs >5 (longest run: {max_consecutive})",
          max_consecutive <= 5, severity="WARNING",
          hint="A host speaks more than 5 consecutive blocks — add interleaved responses.")

    # ── Segment structure checks ─────────────────────────────────────────────
    segment_headers = re.findall(r'^#{1,3} \[[\d:–-]+\]', content, re.MULTILINE)
    check(f"Has timestamped segments ({len(segment_headers)} found)", len(segment_headers) >= 3,
          hint="Episode must have at least 3 timestamped segment headers: ## [HH:MM–HH:MM] Title")

    # ── Outro quality checks ─────────────────────────────────────────────────
    has_website_cta = bool(re.search(r'tobyonfitnesstech\.com', last_500_words, re.IGNORECASE))
    check("CTA to tobyonfitnesstech.com in outro", has_website_cta,
          hint="Outro must direct listeners to tobyonfitnesstech.com for show notes")

    has_correct_closing = bool(re.search(r"we'll be back soon", last_500_words, re.IGNORECASE))
    has_wrong_closing = bool(re.search(r"we'll be back next week", last_500_words, re.IGNORECASE))
    check("Correct closing phrase ('we'll be back soon')", has_correct_closing and not has_wrong_closing,
          hint="Must say 'we'll be back soon' NOT 'we'll be back next week' — this is OpenClaw Daily")

    last_150_words = ' '.join(content.split()[-150:])
    has_no_discord_in_outro = not bool(re.search(r'discord', last_150_words, re.IGNORECASE))
    check("No Discord mention in outro (no listener Discord exists)", has_no_discord_in_outro,
          hint="Never mention Discord in the outro — there is no listener Discord. (Mentioning Discord in body content about platform features is fine.)")

    # ── Forbidden content checks ─────────────────────────────────────────────
    has_word_count_meta = bool(re.search(r'word count|Word Count|<!-- Word', content))
    check("No word count metadata in transcript body", not has_word_count_meta,
          hint="Remove any word count comments or metadata from the transcript")

    has_episode_footer = bool(re.search(r'^\*OpenClaw Daily — Episode', content, re.MULTILINE))
    check("No episode metadata footer", not has_episode_footer,
          hint="Remove the '*OpenClaw Daily — Episode XX, Date*' footer line")

    # ── Runtime/metadata leak checks ────────────────────────────────────────
    has_transcript_end_leak = bool(re.search(r'end of transcript|approximately \d+ minutes|\d,\d{3} words', content, re.IGNORECASE))
    check("No 'End of transcript' metadata leak", not has_transcript_end_leak,
          hint="Remove any 'End of transcript / approximately X minutes / N,NNN words' lines — these get read by TTS verbatim")

    has_inline_asterisks = bool(re.search(r'(?<!\[)(\*{1,2})[^*\n]+\*{1,2}(?!\])', content))
    check("No inline markdown asterisks in body text", not has_inline_asterisks,
          hint="Strip all **bold** and *italic* markdown from the transcript body — TTS reads asterisks as literal characters or skips them incorrectly")

    # ── Voice configuration check ────────────────────────────────────────────
    try:
        ga_path = Path(path).parent.parent / 'generate_audio.py'
        if ga_path.exists():
            ga_content = ga_path.read_text()
            import re as _re
            nova_voice = _re.search(r'"NOVA":\s*"([^"]+)"', ga_content)
            alloy_voice = _re.search(r'"ALLOY":\s*"([^"]+)"', ga_content)
            if nova_voice and alloy_voice:
                nv = nova_voice.group(1)
                av = alloy_voice.group(1)
                check(f"NOVA voice is en-GB-SoniaNeural (got: {nv})",
                      nv == "en-GB-SoniaNeural",
                      hint="NOVA must be en-GB-SoniaNeural (British female)")
                check(f"ALLOY voice is en-US-JennyNeural (got: {av})",
                      av == "en-US-JennyNeural",
                      hint="ALLOY must be en-US-JennyNeural (American female). NOT GuyNeural.")
    except Exception:
        pass

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
