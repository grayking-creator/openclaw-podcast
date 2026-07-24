# AgentStack Daily — Project Context for Agents

AgentStack Daily is an AI-generated daily podcast (EN + DE/ES/HI/PT translations).
The full pre-approval pipeline is AUTOMATED — cron builds a complete reviewable
episode every morning. Agents working here are normally doing recovery, fixes,
or post-approval release work, not drafting.

## The automated morning pipeline (cron, 6:30 AM ET)

```
crontab → scripts/show_notes_research_guard.sh → scripts/agentstack_morning.sh
  1. sync_uploaded_from_youtube.py      episode counter vs live channel
  2. collision check                     existing draft → RESUME release if in flight (locked 2026-06-21, EP072)
                                         OR HOLD if existing review audio is unapproved (locked 2026-06-27, EP075)
                                         OR resume from QC-passing draft → HOLD (exit 2) if a draft exists that fails QC
  3. gather_research_context.py          deterministic data → /tmp/agent_research_context.{md,json}
  4. build_show_notes.py <N>             deterministic structure + per-section model calls,
                                         every section validated inline; final
                                         check_show_notes.py gate runs inside
  5. post_show_notes_draft_discord.py    draft attachment (reference)
  6. generate_episode_transcript.py <N>  model + check_episode.py repair loop
  7. build_episode.py <N>                slate verify, QC, nova render, EN audio,
                                         bespoke cover art, CDN push, ARIA playable
                                         audio + Discord review/approval record
```

Result by ~8:00 AM ET: listenable review audio is posted through ARIA Telegram,
with transcript/cover/audio links and the hash-locked approval record in Discord.
**⛔ Publish requires Toby's verified ✅ reply in the Discord episode channel.
Nothing auto-releases.** Logs: /tmp/show_notes_research.log (run),
/tmp/show_notes_build.log (build log; failures also post to Discord alerts).

## Build-log error recovery (locked 2026-07-13)

`#build-log-errors` is an operational repair queue. Every podcast warning,
degraded rollup, stalled stage, or failure posted there must receive an
automatic repair attempt unless it is an active retry or an approval hold.
The watcher owns the terminal Discord closure: one leading `👍` for a
source-of-truth-verified recovery; `❌❌❌`, `HUMAN INTERACTION REQUIRED`, and
the exact next action if the repair is blocked, failed, or unverifiable. A
model turn ending successfully or a pipeline merely reaching the next stage
does not close an incident. Never infer or bypass audio approval during repair.

Podcast-rollup Instagram/Facebook capture on the M3 must use the installed
Google Chrome app with Toby's existing `tobypeters@gmail.com` identity
(currently Profile 2, resolved by account identity), matching AgentStack
Shorts. Never use Playwright Chromium, Chrome for Testing, or a separate auth
profile for this capture.

## Editorial format (EP072+)

- **Default daily format (locked 2026-06-17, EP071 v3 approval):**
  1. **Harnesses with updates** — front of episode, only the harnesses that actually shipped a new stable release (OpenClaw / Hermes / Codex / Claude Code / Antigravity). Never a roll call of harnesses that didn't ship. Latest contiguous uncovered block only.
  2. **14-story numbered slate (EP079+, locked 2026-07-04)** — at least 14 news / product / funding / acquisition / regulatory / research / local-AI stories that are not the harnesses above (was 10 for EP068–EP078). Toby's EP079 rejection: "30 minute videos with way more news ... There should be way more stories, way more content." Smaller slates are exceptions that need a stated reason.
  3. **GitHub Project Radar** — minimum 3 repos every day, focused on agent building, MCP, coding-agent harnesses, model serving, eval infrastructure, or related tooling. Required every show notes file.
  4. **Model Discovery Check** — new model releases / model family updates / open-weight drops. When none dropped in the cycle, the section is still required with an explicit "Not Selected" line, and the absence is itself a story worth mentioning in a release-heavy week.
  5. **Conclusion** — practical queue (one line per major thread, no checklist) + show-notes CTA + "We'll be back soon."
- Story Slate: 14 numbered topics (EP079+), each with Technical depth angle (≤120 words),
  Actionability angle (≤3 imperative sentences), Listener hook. Story #1 is the
  Agent Stack Release Readout whenever any harness shipped a stable release.
- Required sections: Story Slate, Model Discovery Check, Local LLM Spotlight,
  GitHub Project Radar (≥3 repos), Extra Research Candidates (3), Show Notes
  (fenced ```md block with timestamps), Chapters, Primary Links, Release
  Coverage Check, Harness Version Reference.
- All editorial bans (theme-glue framing, prior-episode recap, meta leakage,
  prerelease tags in public copy, listener-specific references) are enforced by
  scripts/check_show_notes.py — read its hints, don't guess.
- Transcript: hard floor **4,800** words AND hard ceiling **5,400** words (floor re-locked 2026-07-04 after the EP079 rejection — the floor-less EP076 rule produced a 19-min / 2,898-word show; ceiling locked 2026-06-18 after the EP072 drone). That lands 30-34 minutes at the ~159 wpm calibration for a 14-story slate + radar + spotlight + queue. [NOVA]:/[ALLOY]: turns, [PAUSE] tags, shortened spoken version numbers, exact CTA "Toby On Fitness Tech dot com" and closing "We'll be back soon." Per-story segment band 270-320 words non-release / 350-480 release. Enforced by scripts/check_episode.py.
- **Specs, not testing homework (locked 2026-07-13):** technical depth means
  concrete capabilities, specifications, architecture/mechanisms, measured
  behavior, limitations, and the actual news. Do not turn the show into test
  plans, evaluation procedure, checklists, drills, generic operator workflow,
  or repeated advice to "run tests." Explain specialist terms in plain spoken
  English. A 7,000-word draft is always rejected; the 5,400-word ceiling is a
  hard listener-fatigue guard, not a soft target.
- **Full-surface spoken coverage (locked 2026-06-18, EP072 round 3):** the
  transcript must cover every required show-notes section, not just the
  numbered slate. Required spoken segments, in order, are: 14-story slate,
  GitHub Project Radar (≥3 repos), Model Discovery Check (every Selected model
  + one collective beat for Not Selected), Local LLM Spotlight, Extra Research
  Candidates, practical queue. Skipping any required show-notes section in
  the spoken transcript is a hard QC failure. When the show lands under 30
  minutes, expand each Extra to a non-release slate story; otherwise
  summarize as a single beat.
- **No production/research-process narration (locked 2026-06-27, EP075):**
  public audio must never explain how the episode was researched, how source
  lanes were scanned, that there were no new model candidates, or that
  not-selected entries were grouped. If no model or release is selected, say
  nothing in the spoken transcript. `scripts/check_episode.py` hard-fails this.
- **No listener-facing model-pinning or version-targeting advice (locked
  2026-06-28, post-EP075-rewrite feedback).** Never tell the listener to
  "pin" a specific model, coding-agent release, or version as if it were
  a stable target. Reasons: (a) when a pinned model is removed the
  runtime falls back automatically (e.g. Fable → Opus), it does NOT
  crash — so the pin advice is wrong on the facts AND unhelpful; (b) the
  listener can't pin to gated previews like GPT-5.6 anyway. Never imply
  a specific ephemeral version is pinnable, reachable, or available as a
  default. Never narrate fallback lore ("didn't actually crash",
  "defaulted back to", "fell back to the previous model"). `check_episode.py`
  hard-fails via `model_pinning_advice_patterns`; covered by
  `scripts/tests/test_bleed_terms.py` fixture 2. Banned permanently,
  every episode.

## Manual recovery commands

```bash
# Rebuild show notes (refuses to overwrite an existing draft without --force)
python3 scripts/build_show_notes.py <N>

# Transcript from approved show notes
python3 scripts/generate_episode_transcript.py <N>

# Audio + art + CDN + ARIA Telegram and Discord review posts
python3 scripts/build_episode.py <N>

# Toby disapproved review audio with a comment → ONE command, never hand-edits:
python3 scripts/attempt_review_audio.py <N> --feedback "<Toby's exact audio comment>"

# Post-approval full release — ONLY after Toby's verified Discord ✅ reply
python3 scripts/launch_approved_release.py <N> --audio-approved-by-toby \
    --approval-message-id <discord_reply_message_id> \
    --pub-date "Day, DD Mon YYYY HH:MM:SS +0000"

# Targeted phase recovery
python3 scripts/release_episode.py <N> --from-phase <phase> --pub-date "..."

# Recovery for the EP072-style failure (translation lane died because the
# model returned titles with English bodies). Re-translates the bad metadata
# with a reinforcement prompt, patches the existing feed entries in place,
# re-runs QC + CDN + publish_translations, and marks the orchestrator state
# complete. Requires lane_en_publish to already be done.
python3 scripts/recover_failed_translation_lane.py <N>
```

When diagnosing "is it released / can you fix this" without an explicit episode
number: read the newest `scripts/release_ep*_state.json` files and the canonical
`feed.xml` first — local review audio or current-episode state is NOT proof an
episode is released.

## Hard rules (locked)

- **Never infer audio approval.** "Fix it" / "run the scripts" / "what is broken"
  is not approval. Release scripts are fail-closed on the reviewed audio hash +
  a verified non-bot approving Discord reply.
- **Never hand-edit feed.xml or translation feeds** — `add_feed_entry.py` only.
- **Never reuse a transcript without slate verification** (build_episode.py enforces).
- Cover art: `scripts/generate_episode_art.py` uses OpenAI Responses + local
  Pillow render. Never Claude CLI / nested agents for art.
- **Title-specific cover art (locked 2026-07-15, EP087):** parse the real
  `**Title:**` and `**Tagline:**` fields before prompting. The image must turn
  the title's named subjects, mechanisms, and quantitative hook into visible
  content, with at least two title-specific cues and the headline subject
  dominant. Generic dashboards, robot arms, glowing cores, and reusable agent
  network scenes fail review. When a headline source supplies a useful figure
  or reference image (for example TerraZero), use it as visual grounding where
  licensing/access permits; do not merely repeat the previous cover aesthetic.
- **Weighted editorial cover selection (locked 2026-07-19, EP089):** the art
  prompt must evaluate the real title plus the full story slate. Treat the
  headline as dominant, then rank supporting stories by listener importance,
  novelty, visual distinctiveness, concrete imagery, and ability to form one
  coherent scene. Use at most one or two supporting cues. Never turn the slate
  into a checklist collage, and never let rundown order determine the cover.
  At thumbnail review, reject any artwork that could plausibly belong to a
  different episode.
  Withhold the episode number and podcast/show branding from the image-model
  prompt entirely; the deterministic local renderer adds those afterward.
- **Headline is independent of Story 1 (locked 2026-07-17, EP088):** the
  harness-release readout can lead the rundown without becoming the episode
  title or cover. Select the strongest, most visually distinctive headline
  from the entire slate. Prefer a major model/capability story or quantitative
  hook over routine harness patch versions. Never put Codex, Claude Code,
  OpenClaw, or other release strings on the cover merely because that block is
  first. Once selected, both title and artwork must center that same headline.
- Discord posts: URL links only, never filesystem paths.
- Git: stage explicit paths only (never `git add .`/`-A`); never commit
  `__pycache__/`, `*_nova.md`, YouTube token/state files; `xmllint --noout`
  any feed XML before committing.
- Shorts: AgentStack Daily/OpenClaw Daily shorts are not approved. Do not
  generate, stage, upload, schedule, QA, or post Discord alerts for them.

Full workflow details: PODCAST_WORKFLOW.md. Pre-2026-06-10 project lore:
archive/2026-06-10-harness-cleanup/AGENTS.md.pre-cleanup.

## GitHub Project Radar depth rule (locked 2026-06-24, EP074 voice feedback)
Toby: the GitHub Project Radar section has been too shallow. Each radar repo
gets one line of description; the listener cannot tell which projects are
shipping, which are gaining serious traction, and which Toby should care about.

Mandatory depth changes (forward-only, starting EP075):
1. **Per-repo data, not a one-liner.** Every GitHub Project Radar repo must
   carry, in the show notes, the current GitHub star count, the 30-day star
   delta, the most recent release tag + date, and one concrete "why this is
   on the radar now" sentence (a recent significant commit, a notable user,
   a recent release with new functionality, a security patch, or a meaningful
   integration moment). The spoken segment for each repo must surface the
   star count and one concrete traction signal in addition to the repo
   description, not the description alone.
2. **Reuse rule for repos already covered.** If a repo that has appeared in
   the GitHub Project Radar within the last 30 days has had multiple
   significant releases (a major version bump, a meaningful feature
   addition, a security fix, a notable adopter) **and** a star-count jump
   large enough to be worth flagging, it is eligible to come back on the
   radar even though it was recent. "Significant" is defined as ≥1 major
   release (X.0 / X.Y.0 with new functionality, not patch releases) and
   ≥10% star-count growth since the prior coverage. Reused repos must
   explicitly note the previous coverage date in the spoken segment
   ("Back on the radar, last covered June 19 with X stars, now at Y") so
   the listener hears the reappearance as a signal, not a repeat.
3. **Star-tracking system.** The show-notes build must maintain a
   rolling `radar_star_history.json` (or equivalent) recording star
   counts at the moment of coverage for every repo that has ever appeared
   on the radar. When a repo returns to the radar, the show notes must
   report the prior star count alongside the current count. When a brand
   new repo lands on the radar with a star count that exceeds the median
   star count of repos already on the radar, the spoken segment must
   flag it explicitly ("This is a new entry, but the star count already
   puts it ahead of X% of the existing radar").
4. **Model Discovery Check — same depth treatment.** Model Discovery entries
   that are marked "Selected" must carry, in the show notes, the parameter
   count (active and total for MoE), the context window, the modality
   surface (text / image / audio / tool-use), the listing surface
   (OpenRouter / direct API / weights), and one concrete "why this is
   the marquee pick" sentence. The spoken segment must surface the
   parameter count, context window, and one concrete differentiator, not
   the parameter count alone.
5. **Per-repo and per-model word budget for the spoken segment.** Each
   radar repo gets ~60-100 spoken words covering the repo name, what it
   does, the star count + one traction signal, and the concrete
   integration angle. Each Model Discovery Selected entry gets ~50-80
   spoken words. The current 80-120 word radar cap is the floor, not the
   ceiling — the floor is now 100 words per repo, with a hard cap of 140
   so the full section stays inside the episode pacing budget. This
   replaces the prior "one NOVA + one ALLOY turn, 80-120 words" floor.
6. **`scripts/check_show_notes.py` enforcement.** Add hard-fail checks
   for: (a) every GitHub Project Radar repo has a `stars:` and
   `stars_delta_30d:` field, (b) every Model Discovery Selected entry
   has a `params_active:`, `params_total:` (or `n/a`), `context:`,
   and `modality:` field, (c) the spoken-transcript QC in
   `scripts/check_episode.py` scans for the star count string in each
   radar repo's spoken segment, (d) the spoken-transcript QC scans
   for the parameter count and context window in each Selected
   Model Discovery entry's spoken segment. Until those checks are
   wired, every daily show notes file must be visually re-verified
   against this rule before the transcript is generated.

Forward behavior: the next episode that ships without GitHub stars
on the radar repos, or without model parameters/context on Model
Discovery Selected entries, is a hard QC failure of this rule, not
a stylistic preference.

## Pacing is a first-class QC requirement (updated 2026-07-10, EP084 recovery)
The same NOVA/ALLOY 4-turn exposition loop on every story is a hard fail. Per-story show-notes material targets 270-320 words for non-release stories and 350-420 words for release stories. Per-story spoken body between `[PAUSE]` tags must be ≤320 words (non-release) or ≤480 words (release). No two consecutive stories can use the same opening move. The exposition loop (`NOVA news → ALLOY why-it-matters → NOVA deeper-implication → ALLOY builder-relevance → [PAUSE]`) cannot fire more than 2× per episode. Transcript hard band is 4,800-5,700 words for a dense 30-ish minute show. The EP072 8,052-word / 55-minute drone pattern remains a QC failure regardless of how clean the slate is.

## ARIA Telegram + Discord review surfaces (restored 2026-07-10)
The morning pipeline posts the playable review audio through ARIA's explicit
Telegram `default` account (`@TobyCoderBot`, chat id `8319992332`) and posts
the durable review record to `#agent-stack-epNNN` in Discord. Telegram carries
only listenable review audio and the shipped confirmation. Progress, warnings,
failures, and pipeline narration go to the Discord build logs.

Discord is the canonical approval surface. A later non-bot ✅ reply in the
episode channel is fetched and verified against the review timestamp and the
current audio hash. ARIA Telegram is a listening/feedback duplicate and cannot
authorize publication by itself.

## Fresh-research gate (locked 2026-06-27, EP075 recovery; updated 2026-06-29 EP076)
The morning pipeline runs `scripts/fresh_research_gate.py` as Stage 0,
before the YouTube sync. The gate enforces two hard rules:

1. **Freshness.** `/tmp/agent_research_context.{json,md}` must be
   younger than 24 hours.
2. **No duplicate.** The SHA-256 of the research context must not match
   any prior episode's recorded `research_context_hash` in
   `scripts/release_ep*_state.json`. The morning pipeline's
   `gather_research_context.py` populates `last_uploaded_episode` and
   `youtube_upload_count` so the gate has a counter signal; the
   counter check is **advisory** (logged, not enforced) because the
   counter being stuck usually means the release orchestrator is
   stuck, not that the morning research is stale.

If the gate fails the pipeline exits 2 and no show notes, transcript,
or audio is generated. The `scripts/fresh_research_gate.py --no-alert`
flag exists for tests and CI.

### Gate behavior (locked 2026-06-29, EP076 incident)
The EP076 incident on 2026-06-29 showed the gate's original Stage 0
ordering was brittle: a stale research artifact could block the pipeline
indefinitely, while the bail-out message told the operator to
"Re-run scripts/gather_research_context.py" — i.e. to manually run the
exact script the morning pipeline should be running. The same incident
also routed the bail-out alert to Telegram (via `openclaw message
send`) instead of Discord Build Log, violating the rule that Telegram
is reserved for playable review audio and the shipped confirmation.

Fixed behavior:
- **Auto-refresh on stale.** When `_check_freshness()` fails, the gate
  now calls `scripts/gather_research_context.py` itself (timeout 240s)
  and re-checks. Self-heals the common case. If the auto-refresh also
  fails (script missing, non-zero exit, timeout, no JSON written), the
  gate then exits 2.
- **No Telegram posts.** All gate-failure alerts route through the Discord
  error log. `--no-telegram` remains an alias for the clearer `--no-alert`
  test flag. This aligns with Toby's standing rule: Telegram receives only
  playable review audio and the shipped confirmation.
- **Bail-out message updated.** When the gate does fail (after auto-
  refresh also failed), the message no longer instructs the operator
  to run a script by hand — it points them at gather's logs instead.

The fix is "stale → re-gather → re-check → bail only if gather also
fails." Most mornings should now silently heal without any alert.

## Production/research-process narration ban (locked 2026-06-27, EP075 recovery)
Public audio must never explain how the episode was researched, how
source lanes were scanned, that there were no new model candidates,
or that not-selected entries were grouped. The ban is enforced by
`scripts/check_episode.py:internal_impl_patterns` (already pre-EP075)
and by the EP075 bleed-term extension (added 2026-06-27):

* `r"\bthe (?:this )?morning'?s research\b"`
* `r"\bbuild (?:picked up|has|chose|chose to|chose the|will)\b"`
* `r"\bmodel (?:was |is )?not (?:promoted|selected|featured|covered)\b"`
* `r"\bno (?:new )?candidates? (?:was |were |is |are )?(?:not )?(?:selected|featured|covered|promoted)\b"`
* `r"\bnot selected\b[^.\n]{0,80}\b(?:as|for) (?:a |one )?(?:read|beat|line)\b"`
* `r"\bcurrent release cycle\b"`
* `r"\bfor this (?:run|build|episode|cycle|cycle's release)\b"`

`scripts/tests/test_bleed_terms.py` runs seven EP075 fixture lines
through the live pattern list. If any line is not flagged, or any
expected critical pattern is missing from `check_episode.py`, the
test exits 1. The fixture lives in the test file; new bleed phrases
must be added to the fixture and the live pattern list together.

## Discord approval gate (restored 2026-07-10)
`scripts/release_approval_gate.py:mark_audio_approved_from_discord`
records a verified Discord approval. The gate verifies:

* the audio file exists,
* the Discord review channel/message/timestamp are recorded in
  `scripts/release_ep{NNN}_state.json:review_audio`,
* the approving reply is later than the review post, from a non-bot author,
  and contains approval rather than rejection/rebuild language,
* the audio file SHA-256 on disk matches the SHA the review post
  was sent for (i.e. the operator is approving the audio they
  actually heard).

`scripts/launch_approved_release.py --audio-approved-by-toby
--approval-message-id <id>` is the only new-approval path. The retired
`--audio-approved-by-telegram` flag fails closed.

## Post-approval shipping notification
`scripts/release_episode_approved.py` posts a single ARIA Telegram
"🚀 EP{NNN} shipped" message after the orchestrator reaches
`run_status == complete`. The message carries the canonical episode
URL and the CDN audio URL. The post is best-effort; a failed
Telegram post does not roll back the publish.
