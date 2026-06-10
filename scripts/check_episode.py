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

THEME_GLUE_PATTERNS = [
    r"\btrust layer\b",
    r"\bcommon thread\b",
    r"\bnot (?:disconnected|unrelated)\b",
    r"\bwhat today is really about\b",
    r"\bmap of the\b",
    r"\bthese stories are all connected\b",
    r"\ball of these stories\b",
    r"\bthese stories all point to\b",
    r"\bthe real story is\b",
    r"\bone story told across\b",
]

RELEASE_TAG_MENTION_LIMIT = 4

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


def extract_release_tags_for_episode(path):
    transcript_path = Path(path)
    match = re.search(r'episode_(\d{3})_transcript', transcript_path.name)
    if not match:
        return []

    notes_path = transcript_path.parent.parent / f"show_notes_episode_{match.group(1)}.md"
    if not notes_path.exists():
        return []

    notes = notes_path.read_text(encoding='utf-8', errors='ignore')
    if 'AgentStack Daily' in notes:
        # Agent Stack tracks several release lanes. The Release Coverage Check can
        # include ledger/backfill tags that should not all be read aloud in the
        # opening, so use the selected first story's release source links.
        slate = re.search(r"^## Story Slate\s*\n(.+?)(?=\n## |\Z)", notes, re.MULTILINE | re.DOTALL)
        first_story = slate.group(1).split('### 2.', 1)[0] if slate else notes[:3000]
        tags = re.findall(r'/releases/tag/(v\d{4}\.\d+\.\d+)', first_story)
    else:
        tags = re.findall(r'openclaw/openclaw/releases/tag/(v\d{4}\.\d+\.\d+)', notes)
        if not tags:
            release_section = re.search(r"^## Release Coverage Check\s*\n(.+?)(?=\n## |\Z)", notes, re.MULTILINE | re.DOTALL)
            if release_section:
                tags = re.findall(r'\bv\d{4}\.\d+\.\d+\b', release_section.group(1))

    deduped = []
    seen = set()
    for tag in tags:
        if tag not in seen:
            deduped.append(tag)
            seen.add(tag)
    return deduped


def theme_glue_hits(text):
    hits = []
    lowered = text.lower()
    for pattern in THEME_GLUE_PATTERNS:
        match = re.search(pattern, lowered, re.IGNORECASE)
        if match:
            hits.append(match.group(0))
    return hits


def timestamped_segments(content):
    matches = list(re.finditer(r"^##\s+\[(\d{2}:\d{2}(?:[–-]\d{2}:\d{2})?)\]\s*(.+)$", content, re.MULTILINE))
    segments = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        segments.append((match.group(1), match.group(2).strip(), content[start:end].strip()))
    return segments

def shorten_release_tag(tag):
    """Spoken short form of a release tag: 'v2026.5.28' -> '5.28', 'v2026.5.29.2' -> '5.29.2'.
    Toby wants shortened versions read aloud, never the full year-prefixed tag."""
    m = re.match(r'v?20\d{2}\.(\d+)\.(\d+)(?:\.(\d+))?$', tag)
    if m:
        short = f"{m.group(1)}.{m.group(2)}"
        if m.group(3):
            short += f".{m.group(3)}"
        return short
    return tag


def run_checks(path):
    with open(path, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    first_500_words = ' '.join(content.split()[:500])
    last_500_words = ' '.join(content.split()[-500:])
    word_count = len(content.split())
    ep_match = re.search(r"episode_(\d{3})_transcript", str(path))
    ep_num = int(ep_match.group(1)) if ep_match else 0
    segments = timestamped_segments(content)

    print(f"\n📋 Episode QC: {path}")
    print(f"   Word count: {word_count:,}")
    print()




    # No editorial-feedback/meta framing leaks. The episode must not narrate Toby's
    # production instructions, prior rejected drafts, or the chosen editorial mode.
    meta_leak_patterns = [
        r"\bno grand theory\b",
        r"\bno abstract operating model\b",
        r"\bno long lecture\b",
        r"\bnot a lecture\b",
        r"\bdo not waste\b",
        r"\bdo not invent\b",
        r"\bnot a long .*recipe\b",
        r"\bnot a .*consulting\b",
        r"\bstraight what'?s-new episode\b",
        r"\bproduct-update briefing\b",
        r"\barchitecture-advice\b",
        r"\borchestration version\b",
        r"\bbuilder workflow version\b",
        r"\bdrops? the .*framing\b",
        r"\breturns? to a .*format\b",
        r"\bchanges? the format\b",
        r"\bsix[- ]story\b",
        r"\bsix practical stories\b",
        r"\btoday'?s six stories\b",
        r"\bone obvious flagship release\b",
        r"\bflagship release\b",
        r"\bnot short on news\b",
        r"\bstretching one update\b",
        r"\bbefore audio\b",
        r"\bbefore .*publish\b",
        r"\breview before release\b",
        # NOTE: "show notes" is intentionally NOT banned — the outro CTA
        # ("look at the show notes at Toby On Fitness Tech dot com") is allowed
        # and is required by the outro check below. What is not allowed is
        # reading the show-notes text or source links/URLs aloud, which is
        # caught by the spoken-URL guard.
        r"\brelease plan\b",
        r"\bactual artifact\b",
        r"\bstory in the slate\b",
        r"\bstory slate\b",
        # Narrating the episode's own editorial construction exposes how it's
        # built. Never reference "homework", or "this/today's episode" as a format.
        r"\bhomework\b",
        r"\bno homework\b",
        r"\bthis episode\b",
        r"\btoday'?s episode\b",
        r"\bin this (?:episode|block|segment)\b",
        r"\bthe (?:model|news|tooling) story (?:in|of) this\b",
        r"\btranscript include\b",
        r"\btranscript includes\b",
        r"\bwhat changed operationally\b",
        r"\blist of links\b",
        r"\bthis rewrite\b",
        r"\bToby (?:asked|wanted|said|told)\b",
        r"\byou asked\b",
        r"\byou told\b",
        r"\bwe were told\b",
    ]
    meta_leaks = []
    for pat in meta_leak_patterns:
        meta_leaks.extend(re.findall(pat, content, re.IGNORECASE))
    check("No editorial-feedback/meta framing leaks", len(meta_leaks) == 0,
          hint=f"Remove production-instruction/meta phrasing from spoken transcript: {meta_leaks[:8]}")


    internal_impl_patterns = [
        r"\bfetched window\b",
        r"\bfetched release window\b",
        r"\brelease window\b",
        r"\bselected from the fetched\b",
        r"\bdaily release check\b",
        r"\bno new stable .*selected\b",
        r"\bno new stable .*candidate\b",
        r"\bstrong new .*release block\b",
        r"\bcurrent stable feed window\b",
        r"\brecent-version scan\b",
    ]
    internal_impl_hits = []
    for pat in internal_impl_patterns:
        internal_impl_hits.extend(re.findall(pat, content, re.IGNORECASE))
    check("No internal research/build implementation language", len(internal_impl_hits) == 0,
          hint=f"Remove internal process/research/build wording from public episode: {internal_impl_hits[:8]}")

    # No default orchestration-advice overcorrection: unless explicitly requested,
    # AgentStack Daily should primarily answer "what's new?" in LLMs/agents.
    # Practical implications are good; long repeated architecture/orchestration advice is not.
    orchestration_terms = len(re.findall(r"\b(orchestration|workflow|workflows|lane|lanes|which tool owns|builder workflow|recipe|recipes|state machine|approval workflow|handoff|handoffs)\b", content, re.IGNORECASE))
    whats_new_terms = len(re.findall(r"\b(new|added|updated|released|release|feature|features|version|changed|ships|shipping|now supports|upgrade|preview|launch|announced|capability|capabilities)\b", content, re.IGNORECASE))
    check("No default orchestration-advice overcorrection", orchestration_terms <= max(90, whats_new_terms),
          hint=f"Orchestration/advice terms: {orchestration_terms}; what's-new terms: {whats_new_terms}. Rewrite toward feature updates and ecosystem news, not architecture consulting.")

    operator_slog_hits = []
    for pat in [
        r"\boperator playbook\b",
        r"\bturn the .* into a .* workflow\b",
        r"\bthe first workflow\b",
        r"\bthe second workflow\b",
        r"\bthe third workflow\b",
        r"\bthe fourth workflow\b",
        r"\bthe fifth workflow\b",
        r"\bthe sixth workflow\b",
        r"\bthe seventh workflow\b",
        r"\bthe eighth workflow\b",
        r"\bworkflow is .* workflow\b",
        r"\bconcrete builder workflow\b",
        r"\bchecklist is simple\b",
    ]:
        operator_slog_hits.extend(re.findall(pat, content, re.IGNORECASE))
    check("No generic operator-playbook slog", len(operator_slog_hits) == 0,
          hint=f"Remove generic workflow/checklist/playbook phrasing and rewrite toward concrete news/product changes: {operator_slog_hits[:8]}")

    homework_hits = re.findall(
        r"\b(?:recommended test|operator test|upgrade test|test here is|test is|actionability drill|checklist|run this test|run these tests|try this drill|do it in this order|do this,? then do that|run [^.\n]{0,30}checks?|run [^.\n]{0,30}tests?|confirm [^.\n]{0,40}and [^.\n]{0,40}confirm|verify [^.\n]{0,40}and [^.\n]{0,40}verify)\b",
        content,
        re.IGNORECASE,
    )
    check("Episode does not feel like homework",
          len(homework_hits) <= 2,
          hint=f"Too many test/checklist/drill phrases ({len(homework_hits)}). Replace repeated assignments with capabilities, observed reactions, real-world experiences, and implications: {homework_hits[:8]}")

    if ep_num >= 61:
        # The episode ALWAYS starts with the agent-harness updates, but that
        # front must stay concise/informational — not a long procedural/test
        # block. Cap the first two timestamped segments so the harness coverage
        # doesn't sprawl before the model/news stories.
        first_two_segment_text = "\n\n".join(seg[2] for seg in segments[:2])
        first_two_words = len(first_two_segment_text.split())
        check("Agent-harness front stays concise (not a long procedural block)",
              first_two_words <= 2800,
              hint=f"The first two timestamped segments are {first_two_words} words. Keep the harness updates concise and informational — cut release procedure/tests, do not move the model story ahead of the harness updates.")

    # Boring implementation-minutiae guard: the show should teach builder workflows,
    # not linger on generic document/file movement or invisible plumbing.
    boring_terms = len(re.findall(r"\b(document|documents|file|files|folder|folders|copy|copies|moving|move|moved|storage|record|records)\b", content, re.IGNORECASE))
    workflow_terms = len(re.findall(
        r"\b(workflow|build|builder|use case|use cases|recipe|pattern|when to use|how to use|how you use|you use|using it|use it|set up|configure|in practice|what it provides|what you get|wire|ship|deploy|agent task|operator)\b",
        content, re.IGNORECASE))
    # Recalibrated for the tighter 5,000-7,500 word format and broadened to
    # recognize practical "how you use it" phrasing, not just literal "workflow".
    check("Builder-workflow focus beats file/document minutiae", workflow_terms >= max(10, boring_terms // 3),
          hint=f"Workflow terms: {workflow_terms}; boring file/document/plumbing terms: {boring_terms}. Rewrite toward what to build and how to use the tools.")

    release_tags = extract_release_tags_for_episode(path)

    # ── Cold open + intro checks ───────────────────────────────────────────────
    first_speaker_match = re.search(r'(\[NOVA\]|\[ALLOY\]|\*?\*?NOVA\*?\*?|\*?\*?ALLOY\*?\*?):', content)
    words_before_first_speaker = len(content[:first_speaker_match.start()].split()) if first_speaker_match else 0
    check("Cold open, if used, stays brief", words_before_first_speaker <= 80, severity="WARNING",
          hint=f"Found {words_before_first_speaker} words before the first speaker label. Do not burn the opening on a long dramatic cold open.")

    first_300_words = ' '.join(content.split()[:300])
    has_host_intro = bool(re.search(r"I'm NOVA|I am NOVA|Welcome to AgentStack Daily|This is AgentStack Daily", first_300_words, re.IGNORECASE))
    check("Host intro ('I'm NOVA / show name') within first 300 words", has_host_intro,
          hint="Must include 'I'm NOVA' plus the show name near the start")

    has_show_name = bool(re.search(r"AgentStack Daily", first_500_words, re.IGNORECASE))
    check("Show name mentioned in intro", has_show_name,
          hint="Must mention the show name near the start")

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

    intro_theme_hits = theme_glue_hits(' '.join(content.split()[:260]))
    check("Opening is not built around a theme-first umbrella frame", len(intro_theme_hits) == 0,
          hint=f"Theme-first umbrella framing is banned: {intro_theme_hits[:3]}")

    if not release_tags:
        first_220_words = ' '.join(content.split()[:220])
        no_release_opening_hits = []
        for pattern in [
            r"\bnot a release episode\b",
            r"\bno release coverage\b",
            r"\bno new stable openclaw release\b",
            r"\bthere is no new stable openclaw release\b",
            r"\bthe latest stable tags are\b",
            r"\bcovered in recent episode notes\b",
            r"\bfive stories today\b",
            r"\bthis is a builder-stack episode\b",
        ]:
            match = re.search(pattern, first_220_words, re.IGNORECASE)
            if match:
                no_release_opening_hits.append(match.group(0))
        check("No-release opening avoids meta throat-clearing", len(no_release_opening_hits) == 0,
              hint=f"The first minute should hook, not announce mechanics: {no_release_opening_hits[:4]}")

        release_rollcall_hits = re.findall(r"\b(?:v)?\d{4}\.\d+\.\d+\b", first_220_words)
        check("No-release opening does not read out already-covered release tags", len(release_rollcall_hits) == 0,
              hint=f"Do not read version tags in a no-release opening: {release_rollcall_hits[:4]}")

    if release_tags:
        first_220_words = ' '.join(content.split()[:220])
        first_320_words = ' '.join(content.split()[:320])
        change_verbs = re.findall(
            r"\b(adds?|added|moves?|moved|switches?|switched|tightens?|tightened|hardens?|hardened|fixes?|fixed|changes?|changed|improves?|improved|introduces?|introduced|splits?|split|enforces?|enforced|preserves?|preserved|supports?|supported)\b",
            first_320_words,
            re.IGNORECASE,
        )
        technical_surface_hits = re.findall(
            r"\b(setup|wizard|logs?|fallback|provider|permissions?|cron|session|plugin|pricing|auth|image|media|browser|slack|command|transport|state|memory|model catalog)\b",
            first_320_words,
            re.IGNORECASE,
        )
        short_tags = [shorten_release_tag(tag) for tag in release_tags]
        mention_count = sum(first_500_words.count(short) for short in short_tags)
        check("Release episode names the covered versions immediately (shortened form)",
              all(short in first_320_words for short in short_tags),
              hint=f"Name the shortened release version early (e.g. {short_tags}); do not read the full year-prefixed tag aloud.")
        check("Release episode gets to concrete release changes quickly",
              len(change_verbs) >= 2 and len(set(x.lower() for x in technical_surface_hits)) >= 2,
              hint="Within the first ~320 words, move beyond abstract framing and name concrete release changes.")
        check("Release episode does not hammer version numbers before substance",
              mention_count <= RELEASE_TAG_MENTION_LIMIT,
              severity="ERROR",
              hint=f"Found {mention_count} release-tag mentions in the first 500 words. Name the versions, then get to what changed.")

    # ── Outro/close checks ────────────────────────────────────────────────────
    has_outro = bool(re.search(r"(AgentStack Daily|that'?s? (it|all|a wrap)|thanks? for listening|next (time|episode)|see you|I'?m NOVA)", last_500_words, re.IGNORECASE))
    check("Closing/outro present", has_outro,
          hint="Episode must end with a proper sign-off — show name, host name, or 'thanks for listening'")

    has_single_ending = True
    outro_window = last_500_words
    ending_phrases = re.findall(r"(that'?s? (it|all|a wrap)|thanks? for listening|see you next|until next time|we'll be back soon|I'?m NOVA.*?\.)", outro_window, re.IGNORECASE)
    unique_endings = {re.sub(r'\s+', ' ', e[0].lower()).strip() for e in ending_phrases}
    if len(unique_endings) > 3:
        has_single_ending = False
    check("Not too many 'ending' phrases (dedup check)", has_single_ending, severity="WARNING",
          hint=f"Found {len(unique_endings)} distinct closing phrases in the outro window — may indicate repeated outro sections")

    # ── Content checks ────────────────────────────────────────────────────────
    # AgentStack Daily target: tight, dense, no homework filler. Toby prefers a
    # shorter episode that gets to the point over a padded one, so the floor is
    # ~5,000 words (~31 min at ~159 wpm). 60 min is ~9,540 words.
    check("Minimum length (5,000 words)", word_count >= 5000,
          hint=f"Got {word_count:,} words — minimum is 5,000. Add informational substance (capabilities, real-world reactions), never homework/test filler.")

    check("Target length band (5,000-7,500 words for ~31-47 min)", 5000 <= word_count <= 7500, severity="WARNING",
          hint=f"Got {word_count:,} words — target band is 5,000-7,500 words (tight, dense, no filler)")

    # Local paths / IPs must never appear in a public transcript
    local_path_matches = re.findall(r'/Users/[^\s\]\"\']+|/home/[^\s\]\"\']+', content)
    local_ip_matches = re.findall(r'192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+|localhost:\d+', content)
    check("No local file paths in transcript", len(local_path_matches) == 0,
          hint=f"Found local paths: {local_path_matches[:3]}")
    check("No local IP addresses or localhost ports in transcript", len(local_ip_matches) == 0,
          hint=f"Found local addresses: {local_ip_matches[:3]}")

    # Reading source links / URLs aloud is brutal to listen to. The CTA may
    # point listeners to the show notes at the site, but raw URLs and spoken
    # link strings must not appear in the spoken transcript — the only allowed
    # site reference is the "Toby On Fitness Tech dot com" CTA.
    spoken_url_matches = re.findall(
        r'https?://\S+|www\.\S+|\b[a-z0-9-]+\.(?:com|io|ai|dev|org|net|app)/\S+',
        content,
        re.IGNORECASE,
    )
    spoken_url_matches = [u for u in spoken_url_matches if "toby on fitness tech" not in u.lower()]
    check("No source links / URLs read aloud in transcript", len(spoken_url_matches) == 0,
          hint=f"Do not read links/URLs aloud — describe what's at the source instead. Found: {spoken_url_matches[:4]}")

    # ── TTS-hostile content ban (locked 2026-06-05, EP064) ───────────────────
    # The TTS engine reads the following literally as garbled character output,
    # not as natural speech. Banned anywhere in the spoken transcript body.
    tts_hostile_patterns = {
        'inline backticks': (r'`[^\s`][^`]*[^\s`]?`', 3),
        'escaped dollar signs (\\$)': (r'\\\$', 0),
        'literal shell variable ($X)': (r'\$[A-Z_][A-Z0-9_]*', 0),
        'literal shell flag (--x)': (r'--[a-z][a-z0-9-]+', 0),
        'slash command (/plugin, /tmp)': (r'/(?:plugin|tmp|usr|opt|home|var|etc)/?\w*', 0),
        'dotted identifier in code form (x.y.z)': (r'\b[a-z][a-zA-Z0-9]*\.[a-z][a-zA-Z0-9]*\.[a-z][a-zA-Z0-9]*\b', 0),
    }
    tts_hostile_hits = {}
    for label, (pat, allow) in tts_hostile_patterns.items():
        matches = re.findall(pat, content)
        # Filter out code-fence blocks (which the TTS does not read) and standard
        # multi-language identifiers that are common spoken English ("Node.js").
        # TTS only consumes speaker turns; here we operate on full content so we
        # allow 3 backticks (math/code references) but block individual spans.
        if label == 'inline backticks':
            # Multi-backtick code fences are not spoken; collapse to 0.
            fences = len(re.findall(r'^```', content, re.MULTILINE))
            matches = [m for m in matches if not m.startswith('```')]
            # Allow a tiny number of harmless backticks (e.g. literal in the
            # closing CTA's plain text); zero is the target.
        if label == 'dotted identifier in code form (x.y.z)':
            # Common spoken forms like "Node.js", "Bash", "Sonia" are not
            # banned by this rule.
            matches = [m for m in matches if m.lower() not in {'node.js', 'github.com'}]
        if len(matches) > allow:
            tts_hostile_hits[label] = matches[:6]
    check("No TTS-hostile content (backticks, escaped $, shell flags, slash commands, dotted identifiers)",
          len(tts_hostile_hits) == 0,
          hint=(
              "TTS reads these literally as garbled character-by-character output. "
              "Strip backticks, expand escaped $ / literal $VAR to spoken English, "
              "and remove code-style dotted identifiers. "
              f"Found: {tts_hostile_hits}"
          ))

    # ── Spoken-English naturalness ban (locked 2026-06-05, EP064 round 2) ───────
    # Catches the ungrammatical substitutions that mechanical regex passes leave
    # behind when stripping TTS-hostile artifacts. Phrases like "deep the temp
    # directory" or "restoring correct the temp directory behavior" read OK on
    # a screen but sound like complete gibberish when spoken aloud. Always
    # hand-edit the surrounding sentence so substitutions make grammatical
    # sense in context — regex substitution is a starting point, not a final pass.
    naturalness_patterns = {
        'doubled article (the the X)': (r'\b[Tt]he the [a-zA-Z]', 0),
        'doubled noun (X X)': (r'\b(temp directory temp directory|filter filters|command command|directory directory|plugin plugin)\b', 0),
        'regex-artifact: deep the temp': (r'\bdeep the temp directory', 0),
        'regex-artifact: correct the temp': (r'\bcorrect the temp directory', 0),
        'regex-artifact: a Claude temp': (r'\ba Claude temp directory\b', 0),
        'regex-artifact: on the resume flag': (r'\bon the resume flag\b', 0),
        'regex-artifact: hook specific output': (r'\bhook specific output\b', 0),
    }
    naturalness_hits = {}
    for label, (pat, allow) in naturalness_patterns.items():
        matches = re.findall(pat, content, re.IGNORECASE)
        if len(matches) > allow:
            naturalness_hits[label] = matches[:6]
    check("No regex-substitution artifacts (natural spoken English)",
          len(naturalness_hits) == 0,
          hint=(
              "Phrases like 'deep the temp directory' or 'restoring correct the temp "
              "directory behavior' sound like gibberish to listeners even though the "
              "words are real. Hand-edit the surrounding sentence so substitutions "
              "make grammatical sense in context. Read each edited paragraph aloud "
              "before posting review audio. "
              f"Found: {naturalness_hits}"
          ))

    # ── Duplicate detection ───────────────────────────────────────────────────
    paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 100]
    seen = {}
    dupes = []
    for i, p in enumerate(paragraphs):
        key = re.sub(r'\s+', ' ', p).lower()[:120]
        if key in seen:
            dupes.append(f"paragraph ~{i+1} duplicates ~{seen[key]+1}")
        else:
            seen[key] = i
    check("No duplicate paragraphs detected", len(dupes) == 0,
          hint='\n     '.join(dupes[:5]) if dupes else "")

    repeated_runs = []
    normalized_paragraphs = [
        re.sub(r'\s+', ' ', re.sub(r'^\[(NOVA|ALLOY)\]:\s*', '', p, flags=re.IGNORECASE)).strip().lower()
        for p in paragraphs
    ]
    for window in range(3, 9):
        seen_runs = {}
        for i in range(0, max(0, len(normalized_paragraphs) - window + 1)):
            key = '\n'.join(normalized_paragraphs[i:i + window])
            if key in seen_runs:
                repeated_runs.append(f"{window}-paragraph run ~{i+1} repeats ~{seen_runs[key]+1}")
                break
            seen_runs[key] = i
        if repeated_runs:
            break
    check("No repeated multi-paragraph tail loops", len(repeated_runs) == 0,
          hint='\n     '.join(repeated_runs[:5]) if repeated_runs else "")

    # ── Format checks ─────────────────────────────────────────────────────────
    has_pause_tags = '[PAUSE]' in content
    check("Contains [PAUSE] tags for natural pacing", has_pause_tags, severity="WARNING",
          hint="Add [PAUSE] markers at natural breathing points")

    broken_emphasis = content.count('[EMPHASIS]') != content.count('[/EMPHASIS]')
    check("Matched [EMPHASIS] tags", not broken_emphasis,
          hint="Mismatched [EMPHASIS] / [/EMPHASIS] tags")

    listy_opening_phrases = re.findall(r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten) stories today\b|\bhere'?s what we'?re covering\b|\blet'?s run through\b", first_220_words, re.IGNORECASE)
    check("Opening is not a mechanical list lead-in", len(listy_opening_phrases) == 0,
          severity="ERROR",
          hint=f"The first minute should sound conversational, not like a rundown: {listy_opening_phrases[:3]}")

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
    if release_tags:
        segment_matches = list(re.finditer(r'^#{1,3} \[([\d:–-]+)\]\s*(.+)$', content, re.MULTILINE))
        if len(segment_matches) >= 2:
            first_story_title = segment_matches[0].group(2)
            first_story_start = segment_matches[0].end()
            first_story_end = segment_matches[1].start()
            first_story_words = len(content[first_story_start:first_story_end].split())
            check("First timestamped segment is the OpenClaw release block",
                  bool(re.search(r'openclaw|v\d{4}\.\d+\.\d+', first_story_title, re.IGNORECASE)),
                  hint=f"First real segment should be the OpenClaw release deep dive, got: {first_story_title!r}")
            check("Front-loaded release segment is detailed enough",
                  first_story_words >= 420,
                  hint=f"First release segment is only {first_story_words} words. Push more detailed release coverage to the front.")
        else:
            check("Release-led episode has a release segment", False,
                  hint="Expected a first timestamped release segment in a release-led episode.")

    # ── Outro quality checks ─────────────────────────────────────────────────
    allowed_site_cta_pattern = r'\bToby On Fitness Tech\s+(?:dot\s+com|\.com)\b'
    has_notes_cta = bool(re.search(r'(notes and links|show notes|episode notes|source links)', last_500_words, re.IGNORECASE))
    has_allowed_site_cta = bool(re.search(allowed_site_cta_pattern, last_500_words, re.IGNORECASE))
    check("Outro points to notes/source links at the allowed site CTA",
          ep_num <= 60 or (has_notes_cta and has_allowed_site_cta),
          hint="Outro must point listeners to show notes/source links/episode notes at the exact CTA: Toby On Fitness Tech dot com.")

    has_correct_closing = bool(re.search(r"we'll be back soon", last_500_words, re.IGNORECASE))
    has_wrong_closing = bool(re.search(r"we'll be back next week", last_500_words, re.IGNORECASE))
    check("Correct closing phrase ('we'll be back soon')", has_correct_closing and not has_wrong_closing,
          hint="Must say 'we'll be back soon' NOT 'we'll be back next week' — this is AgentStack Daily")

    last_150_words = ' '.join(content.split()[-150:])
    has_no_discord_in_outro = not bool(re.search(r'discord', last_150_words, re.IGNORECASE))
    check("No Discord mention in outro (no listener Discord exists)", has_no_discord_in_outro,
          hint="Never mention Discord in the outro — there is no listener Discord. (Mentioning Discord in body content about platform features is fine.)")

    # ── Forbidden content checks ─────────────────────────────────────────────
    content_without_allowed_site_cta = re.sub(allowed_site_cta_pattern, '', content, flags=re.IGNORECASE)
    owner_name_matches = re.findall(r'\bToby\b|\btobyglenn\w*\b|\btobyonfitnesstech\b|\btoby\s*on\s*fitness\s*tech\b', content_without_allowed_site_cta, re.IGNORECASE)
    check("Owner name appears only in the allowed site CTA",
          len(owner_name_matches) == 0,
          hint=f"Remove owner-name/domain phrasing except exact end CTA: {owner_name_matches[:5]}")

    meta_request_matches = re.findall(
        r'\b(?:Toby|the\s+owner|the\s+listener|you)\s+(?:asked|wanted|requested|told|specified)\b|\brequested\s+format\b|\bdirect\s+feedback\b|\bwhat\s+(?:Toby|the\s+owner|the\s+listener)\s+(?:asked|wanted|requested|told|specified)\b',
        content,
        re.IGNORECASE,
    )
    check("Episode contains no meta references to user requests or feedback",
          len(meta_request_matches) == 0,
          hint=f"Remove drafting/request meta from speakable content: {meta_request_matches[:5]}")

    has_word_count_meta = bool(re.search(r'word count|Word Count|<!-- Word', content))
    check("No word count metadata in transcript body", not has_word_count_meta,
          hint="Remove any word count comments or metadata from the transcript")

    has_episode_footer = bool(re.search(r'^\*AgentStack Daily — Episode', content, re.MULTILINE))
    check("No episode metadata footer", not has_episode_footer,
          hint="Remove the '*AgentStack Daily — Episode XX, Date*' footer line")


    # ── Editorial quality gate: no process recap / prior-episode filler ───────
    # Toby locked this after EP044 slipped through: release/version housekeeping,
    # "we already covered...", and user-feedback/process meta are not episode
    # content. They must fail before audio is generated.
    prior_episode_meta_patterns = [
        r"\b(?:last|previous|prior|earlier)\s+(?:episode|episodes|show|shows|show-note|show-note files|show notes)\b.{0,140}\b(?:cover|covered|coverage|already|recent)\b",
        r"\b(?:already|previously|recently)\s+(?:cover|covered|discussed|talked about)\b",
        r"\b(?:we|I|this show)\s+(?:already|previously|recently)\s+(?:covered|discussed|talked about)\b",
        r"\b(?:covered|discussed|talked about)\s+(?:in|on)\s+(?:EP\d+|episode\s+\d+|a previous episode|previous episodes|recent episode notes)\b",
        r"\b(?:under|because of)\s+the\s+(?:latest-contiguous|contiguous-release|release coverage)\s+rule\b",
        r"\bEP\d+\s+(?:starts|surfaces|covers|covered|talked|discussed)\b",
        r"\b(?:show-note files|episode notes|release list)\s+(?:already\s+)?(?:cover|covered|show|indicate)\b",
        r"\b(?:v\d{4}\.\d+\.\d+[,\s]*(?:and\s+)*){2,}\b.*\b(?:older stable tags|already cover|previous|prior|recent)\b",
    ]
    prior_episode_meta_hits = []
    for pattern in prior_episode_meta_patterns:
        prior_episode_meta_hits.extend(re.findall(pattern, content, re.IGNORECASE | re.DOTALL))
    check("No prior-episode / already-covered recap filler",
          len(prior_episode_meta_hits) == 0,
          hint=f"Remove release-history/show-process housekeeping from speakable content: {[collapse if isinstance(collapse, str) else ' '.join(collapse) for collapse in prior_episode_meta_hits[:5]]}")

    ep_match = re.search(r"episode_(\d{3})_transcript", str(path))
    ep_num = int(ep_match.group(1)) if ep_match else 0

    # Toby wants shortened versions spoken (e.g. "5.28", ".159") and NO full
    # forms — neither "2.1.159" nor the year-prefixed calver "2026.5.28". Flag
    # any three-part dotted version except the legitimate shortened release tags.
    allowed_short_tags = {shorten_release_tag(t) for t in (release_tags or [])}
    full_patch_versions = [
        version for version in re.findall(r"\b\d+\.\d+\.\d+\b", content)
        if version not in allowed_short_tags
    ]
    if ep_num >= 58:
        check("No full version numbers in spoken transcript (use shortened forms)",
              len(full_patch_versions) == 0,
              hint=(
                  "Use a shortened version aloud (e.g. '5.28', '.159', 'two point one'), never full dot "
                  f"notation or year-prefixed tags: {sorted(set(full_patch_versions))[:8]}"
              ))
    repeated_full_patch_versions = sorted(
        version for version in set(full_patch_versions)
        if full_patch_versions.count(version) > 1
    )
    check("No repeated full patch release numbers in spoken transcript",
          len(repeated_full_patch_versions) == 0,
          hint=(
              "Use a shortened release identifier once, then say this release/update. "
              f"Repeated full patch versions are painful in audio: {repeated_full_patch_versions[:8]}"
          ))

    version_tag_mentions = re.findall(r"\bv\d{4}\.\d+\.\d+\b", content)
    unique_version_tags = sorted(set(version_tag_mentions))
    # Prerelease / beta / alpha / rc tags are banned in spoken transcript (EP066 incident 2026-06-08).
    # Say "the prerelease", "the June beta", or "the upcoming release" — never "v2026.6.5-beta.2".
    prerelease_tag_mentions = re.findall(r"v\d{4}\.\d+\.\d+-(?:alpha|beta|rc|dev|pre)\.\d+|v\d{4}\.\d+-(?:alpha|beta|rc|dev|pre)(?:\.\d+)?", content, re.IGNORECASE)
    prerelease_tag_mentions = sorted(set(prerelease_tag_mentions))
    check("No prerelease / beta tag mentions in spoken transcript",
          len(prerelease_tag_mentions) == 0,
          hint=f"Prerelease versions belong in internal Release Coverage Check only. "
               f"Replace with 'the prerelease', 'the June beta', or 'the upcoming release' in spoken copy. "
               f"Found: {prerelease_tag_mentions[:8]}")
    if release_tags:
        off_slate_version_tags = [tag for tag in unique_version_tags if tag not in release_tags]
        check("Release episode does not mention off-slate old version tags",
              len(off_slate_version_tags) == 0,
              hint=f"Old-version roll calls are banned in the transcript: {off_slate_version_tags[:8]}")
    else:
        check("Non-release episode does not mention version-tag roll calls",
              len(unique_version_tags) <= 1,
              hint=f"Version-tag housekeeping is not listener value: {unique_version_tags[:8]}")

    tech_concrete_terms = re.findall(
        r"\b(API|SDK|runtime|request|response|schema|parameter|config(?:uration)?|flag|permission|auth|token|provider|adapter|transport|queue|scheduler|timeout|retry|fallback|state|memory|session|trace|log|metric|benchmark|evaluation|latency|throughput|cache|database|migration|sandbox|security|privacy|model card|system card|changelog|release notes|failure mode)\b",
        content,
        re.IGNORECASE,
    )
    check("Transcript has enough hard technical mechanism density",
          len(tech_concrete_terms) >= max(35, word_count // 180),
          severity="ERROR",
          hint=f"Found {len(tech_concrete_terms)} technical-mechanism terms; replace recap/fluff with concrete APIs, runtime behavior, config, failure modes, security boundaries, evals, or operator tradeoffs.")

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

        nova_without_allowed_site_cta = re.sub(allowed_site_cta_pattern, '', nova_content, flags=re.IGNORECASE)
        nova_owner_name_matches = re.findall(r'\bToby\b|\btobyglenn\w*\b|\btobyonfitnesstech\b|\btoby\s*on\s*fitness\s*tech\b', nova_without_allowed_site_cta, re.IGNORECASE)
        check("TTS render owner name appears only in allowed site CTA",
              len(nova_owner_name_matches) == 0,
              hint=f"Re-render after removing owner-name/domain phrasing except exact end CTA: {nova_owner_name_matches[:5]}")

        nova_meta_request_matches = re.findall(
            r'\b(?:Toby|the\s+owner|the\s+listener|you)\s+(?:asked|wanted|requested|told|specified)\b|\brequested\s+format\b|\bdirect\s+feedback\b|\bwhat\s+(?:Toby|the\s+owner|the\s+listener)\s+(?:asked|wanted|requested|told|specified)\b',
            nova_content,
            re.IGNORECASE,
        )
        check("TTS render contains no meta references to user requests or feedback",
              len(nova_meta_request_matches) == 0,
              hint=f"Re-render after removing drafting/request meta from transcript: {nova_meta_request_matches[:5]}")
    else:
        check("TTS render file exists (_nova.md)",
              False,
              severity="WARNING",
              hint=f"Run render_nova.py to create {nova_path.name} before generating audio")

    # ── Rule A — CLI release coverage = released stable tags only ────────────
    # Block the dist-tag framing from the spoken transcript
    forbidden_dist_tag_phrases = [
        r"\bnpm latest\b",
        r"\breceived via update\b",
        r"\blatest versus received\b",
        r"\blatest vs\.? received\b",
        r"\blatest or received\b",
        r"\bthe latest (?:stable )?(?:npm )?(?:tag|channel|dist-tag|build)\b",
        r"\bAnthropic.{0,8}stable channel\b",
    ]
    for pat in forbidden_dist_tag_phrases:
        check(
            f"No dist-tag framing in transcript ({pat!r})",
            not re.search(pat, content, re.IGNORECASE),
            severity="ERROR",
            hint="CLI release coverage = released stable tags only. Drop 'npm latest', 'received via update', 'latest vs. received', or any dist-tag framing. Talk about the released stable tag itself, not which channel it appeared on.",
        )

    # ── Rule B2 — no-release narration for any harness is a hard failure ──────
    # (Toby, 2026-06-10): with five tracked harnesses, reading out "Claude Code
    # had no release this cycle" turns every episode into a roll call. The
    # spoken transcript only names harnesses that actually shipped; silence
    # covers the rest.
    _harness_names = r"(?:OpenClaw|Hermes(?:\s+Agent)?|(?:OpenAI\s+)?Codex(?:\s+CLI)?|Claude\s+Code(?:\s+CLI)?|Antigravity(?:\s+CLI)?)"
    no_release_narration_hits = []
    for pat in [
        rf"\b{_harness_names}\b[^.\n]{{0,90}}\bno\s+(?:new\s+)?(?:stable\s+)?(?:release|update|version|change)s?\b",
        rf"\bno\s+(?:new\s+)?(?:stable\s+)?(?:release|update|version|change)s?\b[^.\n]{{0,90}}\b{_harness_names}\b",
        rf"\b{_harness_names}\b[^.\n]{{0,40}}\b(?:remains?|stays?|stayed|holds?|held|sits?)\s+(?:at|on|steady|unchanged|put)\b",
        rf"\bnothing\s+new\s+(?:from|for|on)\s+{_harness_names}\b",
        rf"\b{_harness_names}\b[^.\n]{{0,40}}\b(?:didn'?t|did\s+not|hasn'?t|has\s+not)\s+(?:ship|update|move|change)\b",
        rf"\bquiet\s+(?:cycle|week|day)\s+for\s+{_harness_names}\b",
    ]:
        for m in re.finditer(pat, content, re.IGNORECASE):
            no_release_narration_hits.append(m.group(0)[:70])
    check("No 'harness had no release' narration in the spoken transcript",
          len(no_release_narration_hits) == 0,
          severity="ERROR",
          hint="Never read out that a harness had no release/update this cycle — only harnesses that "
               f"shipped get named in release coverage. Cut these lines: {no_release_narration_hits[:5]}")

    # ── Rule B — Claude Code / Codex CLI must be framed as terminal-based AI coding agents ─
    # First mention per episode must include the "terminal-based" + "AI coding agent" framing
    def _has_terminal_based_ai_coding_agent_intro(text, product_pattern):
        """Return True if the FIRST mention of product_pattern carries the
        'terminal-based' + 'AI coding agent' framing within ±200 chars, or the
        product is never mentioned at all (vacuous truth).

        First-mention semantics on purpose (2026-06-10): the rule's hint and the
        transcript prompt both specify first-mention framing, but this used to
        require the framing before EVERY mention — on a 10-story episode that
        repeatedly names Claude Code it burned all regeneration attempts."""
        m = re.search(product_pattern, text, re.IGNORECASE)
        if not m:
            return True
        window = text[max(0, m.start() - 200):m.end() + 200]
        return bool(re.search(r"terminal[- ]based", window, re.IGNORECASE) and
                    re.search(r"AI coding agent|coding agent", window, re.IGNORECASE))

    check(
        "Claude Code is framed as a terminal-based AI coding agent",
        _has_terminal_based_ai_coding_agent_intro(content, r"\bClaude Code\b"),
        severity="ERROR",
        hint="The first time 'Claude Code' is named in the spoken transcript, it must be introduced as a 'terminal-based AI coding agent'. Re-introduce the product with the full framing phrase if you have already used the bare name.",
    )
    check(
        "Codex CLI is framed as a terminal-based coding agent",
        _has_terminal_based_ai_coding_agent_intro(content, r"\bCodex CLI\b"),
        severity="ERROR",
        hint="The first time 'Codex CLI' is named in the spoken transcript, it must be introduced as a 'terminal-based coding agent' (terminal-based + AI/coding agent). Re-introduce the product with the full framing phrase if you have already used the bare name.",
    )

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
