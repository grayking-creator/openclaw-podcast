# AgentStack Daily — Project Context for Agents

AgentStack Daily is an AI-generated daily podcast (EN + DE/ES/HI/PT translations).
The full pre-approval pipeline is AUTOMATED — cron builds a complete reviewable
episode every morning. Agents working here are normally doing recovery, fixes,
or post-approval release work, not drafting.

## The automated morning pipeline (cron, 6:30 AM ET)

```
crontab → scripts/show_notes_research_guard.sh → scripts/agentstack_morning.sh
  1. sync_uploaded_from_youtube.py      episode counter vs live channel
  2. collision check                     existing draft → HOLD (exit 2), human decides
  3. gather_research_context.py          deterministic data → /tmp/agent_research_context.{md,json}
  4. build_show_notes.py <N>             deterministic structure + per-section model calls,
                                         every section validated inline; final
                                         check_show_notes.py gate runs inside
  5. post_show_notes_draft_discord.py    draft attachment (reference)
  6. generate_episode_transcript.py <N>  model + check_episode.py repair loop
  7. build_episode.py <N>                slate verify, QC, nova render, EN audio,
                                         bespoke cover art, CDN push, Discord review post
```

Result by ~8:00 AM ET: listenable review audio + transcript + cover posted to
Discord. **⛔ Publish requires Toby's explicit ✅ reply on the review audio.
Nothing auto-releases.** Logs: /tmp/show_notes_research.log (run),
/tmp/show_notes_build.log (build log; failures also post to Discord alerts).

## Editorial format (EP068+)

- Story Slate: exactly 10 numbered topics, each with Technical depth angle
  (≤120 words), Actionability angle (≤3 imperative sentences), Listener hook.
- Story #1 is the Agent Stack Release Readout whenever OpenClaw / Hermes /
  Codex / Claude Code / Antigravity shipped a stable release (latest contiguous
  uncovered block only — never resurface older uncovered releases).
- Required sections: Story Slate, Model Discovery Check, Local LLM Spotlight,
  GitHub Project Radar (≥3 repos), Extra Research Candidates (3), Show Notes
  (fenced ```md block with timestamps), Chapters, Primary Links, Release
  Coverage Check, Harness Version Reference.
- All editorial bans (theme-glue framing, prior-episode recap, meta leakage,
  prerelease tags in public copy, listener-specific references) are enforced by
  scripts/check_show_notes.py — read its hints, don't guess.
- Transcript: 5,000–7,500 words, [NOVA]:/[ALLOY]: turns, [PAUSE] tags, shortened
  spoken version numbers, exact CTA "Toby On Fitness Tech dot com" and closing
  "We'll be back soon." Enforced by scripts/check_episode.py.

## Manual recovery commands

```bash
# Rebuild show notes (refuses to overwrite an existing draft without --force)
python3 scripts/build_show_notes.py <N>

# Transcript from approved show notes
python3 scripts/generate_episode_transcript.py <N>

# Audio + art + CDN + Discord review post (stops at approval gate)
python3 scripts/build_episode.py <N>

# Toby disapproved review audio with a comment → ONE command, never hand-edits:
python3 scripts/attempt_review_audio.py <N> --feedback "<Toby's exact audio comment>"

# Post-approval full release — ONLY after Toby's ✅ on the review audio
python3 scripts/launch_approved_release.py <N> --audio-approved-by-toby \
    --approval-message-id <toby_reply_message_id> --pub-date "Day, DD Mon YYYY HH:MM:SS +0000"

# Targeted phase recovery
python3 scripts/release_episode.py <N> --from-phase <phase> --pub-date "..."
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
- Discord posts: URL links only, never filesystem paths.
- Git: stage explicit paths only (never `git add .`/`-A`); never commit
  `__pycache__/`, `*_nova.md`, YouTube token/state files; `xmllint --noout`
  any feed XML before committing.
- Shorts: `youtube_shorts_pipeline.py --mode cron` (09:30 ET) and the timed
  upload slots are approved and active — do not disable, never upload shorts in
  a loop; one cron fire = one short.

Full workflow details: PODCAST_WORKFLOW.md. Pre-2026-06-10 project lore:
archive/2026-06-10-harness-cleanup/AGENTS.md.pre-cleanup.
