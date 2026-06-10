# PODCAST WORKFLOW

The pre-approval pipeline is fully automated (since 2026-06-10). The two manual
scripts below remain the recovery path and the post-approval path.

---

## Script 0 — Automated morning pipeline (cron, 6:30 AM ET)

`scripts/agentstack_morning.sh` (launched via `scripts/show_notes_research_guard.sh`)
produces a complete reviewable episode by ~8:00 AM ET:

1. `gather_research_context.py` — deterministic research data (GitHub releases,
   npm/PyPI, OpenRouter diffs, HN, lab RSS, GitHub radar) → `/tmp/agent_research_context.{md,json}`
2. `build_show_notes.py <N>` — deterministic show-notes builder: structure,
   Release Coverage Check, Harness Version Reference, Model Discovery, Chapters,
   Primary Links and timestamps are computed in code; models only write small
   prose sections, each validated in real time against the check_show_notes.py
   rules with per-section retries and deterministic fallbacks. The real
   `check_show_notes.py` runs as the final gate inside the builder.
3. `generate_episode_transcript.py <N>` — transcript + check_episode.py repair loop
4. `build_episode.py <N>` — slate verify, QC, nova render, EN audio, bespoke
   cover art, CDN push, Discord review post

**The pipeline stops at the review post. Publish still requires Toby's ✅.**
Failures at any stage append to `/tmp/show_notes_build.log` and post to the
Discord alerts channel. An existing unreleased draft HOLDs the pipeline (exit 2)
for a human numbering decision via `resolve_episode_gap.py`.

---

## Script 1 — Build (pre-greenlight, manual/recovery path)

```bash
python3 scripts/build_episode.py <N>
```

If `episodes/episode_0NN_transcript.md` is missing, create that artifact first with:
```bash
python3 scripts/generate_episode_transcript.py <N>
```
Do not use a wrapper that delegates transcript generation to another OpenClaw CLI process; EP060 showed that nested path can time out silently before creating an artifact. The transcript generator calls OpenClaw's configured OpenAI text model directly, runs `check_episode.py`, and only then moves the transcript into place. Review-audio work must start with a verified transcript file, then `build_episode.py`.

Cover art generation must not use Claude CLI. The build's bespoke art step calls `scripts/generate_episode_art.py`, which uses OpenAI Responses to create `scripts/episode_art/episode_0NN_art.py`, then local Pillow renders `images/episode_0NN_cover.png`. If OpenAI cannot produce/test the module, stop with the exact blocker instead of falling back to Claude or a generic cover.

**What it does:**
1. Verifies transcript matches the approved story slate in `show_notes_episode_0NN.md` — **blocks if any story is missing or mismatched**
2. Runs QC (`check_episode.py`) — blocks on any ERROR
3. Renders nova transcript
4. Generates EN audio
5. Generates EN cover art
6. Pushes audio + cover to CDN repo
7. Posts listen URL to `#agent-stack-ep0NN` in Discord

**⛔ STOP after this. Do not proceed until Toby replies ✅.**

**Required inputs before running:**
- `show_notes_episode_0NN.md` — approved story slate
- `episodes/episode_0NN_transcript.md` — transcript built by `scripts/generate_episode_transcript.py` or otherwise created from that slate and verified by `check_episode.py`

---

## Script 2 — Release (post-greenlight)

After Toby's actual review-audio approval, run it with the Discord message id for Toby's approving reply:
```bash
python3 scripts/launch_approved_release.py <N> --audio-approved-by-toby --approval-message-id <toby_reply_message_id> --pub-date "Day, DD Mon YYYY HH:MM:SS +0000"
```

**What it does:**
1. Detaches the release process and starts a watchdog notification process
2. `setup` — verify EN assets and canonicalize audio name
3. Launch three lanes in parallel:
   EN publish to feed + website
   translations (show notes + transcript + audio + covers)
   EN crossfire FLUX/Ken Burns video build
4. Publish translated feeds + website as soon as translated assets are ready
5. Build localized burn-in YouTube masters from the crossfire episode outputs
6. Upload all 5 localized videos to YouTube
7. Sync CDN + post Discord release message

`scripts/release_episode_approved.py` is the orchestrator underneath the launcher. `scripts/release_episode.py` remains the resumable phase library underneath this flow. Use either directly only for targeted recovery/debug work.

When approval arrives through Discord/ARIA, verify the approval reply from the review channel, run the launcher directly, and monitor the state file/log until terminal success or a real failure. Do not infer approval from a "fix it", "run the scripts", or "what is broken" message. Do not stop at a delegated Codex/MiniMax artifact task; if a subtask fails, repair the artifact from disk and resume the release script from the right step.

**Recovery / targeted restart:**
```bash
python3 scripts/release_episode.py 28 --from-phase covers --pub-date "..."
```

---

## Hard Rules (locked — do not override)

### Transcript
- **NEVER reuse an existing `episode_0NN_transcript.md` without verifying it matches the approved story slate.** `build_episode.py` enforces this automatically. If you're writing a transcript manually, read `show_notes_episode_0NN.md` first and verify every story title appears in the transcript before running the build script.
- **Episode runtime target is about 30 minutes.** At the current EN voices and pacing, that means roughly 4,600 to 4,800 words, not a 35-40 minute script.
- **If release coverage exists, the release block comes first and gets the deepest coverage.** Do not bury the release details under a long theme-setting intro.
- **EP068+: the Story Slate is exactly 10 topics** (release readout first when any
  agent-stack product shipped). At the ~30-minute runtime that means tighter,
  denser story segments — never pad to fill, never cut OpenClaw release detail
  before cutting lower-priority stories.
- **Technical deep-dive standard:** use the EP042 model for future episodes: explain what each technology is, how the stack works, concrete mechanisms/APIs/configs/architecture, tradeoffs, failure modes, operational impact, and practical recommendations or ratings where useful. Less article recap; more technical review and analysis.
- **Spoken version numbers:** do not read full patch notation aloud in the transcript. Say a shortened release identifier once, then switch to "this release", "the update", or the product name. Full dot notation is fine in show notes, feed metadata, and links; it is painful in audio and should not appear in future spoken transcripts.
- **GitHub project profiles:** GitHub project segments must include popularity/velocity signals, integrations or plug-in surfaces, concrete use cases, and workflow scenarios for builders. Treat the best repos as showcases/profiles with useful stack context, not as a late star-count list.
- **Theme-first umbrella framing is banned.** Do not build the show around phrases like “trust layer,” “common thread,” or “these stories are all connected.”
- **Never mention Toby or listener-specific setup details in the episode body.** Use generic workflow language instead. Never include drafting/request meta like “Toby wanted/requested/asked” or “requested format.” The only default exception is the exact end CTA “Toby On Fitness Tech dot com.”

### Feeds
- **NEVER hand-edit feed.xml or translation feeds.** `release_episode_approved.py` uses `release_episode.py` + `add_feed_entry.py`, which validates XML before and after. Hand-editing broke EP024 feeds.

### Approval gate
- Audio is uploaded to CDN before asking for approval. Toby listens at the posted URL, then replies ✅ to trigger `launch_approved_release.py`.
- Audio approval = automatic trigger for the full release pipeline. No second approval needed for feeds.
- The release launcher is fail-closed: `build_episode.py` records the exact reviewed EN audio hash and Discord review post, and `launch_approved_release.py` / `release_episode_approved.py` refuse to publish unless that same hash has explicit approval recorded from a verified non-bot Discord reply after the review post. Use `--audio-approved-by-toby --approval-message-id <toby_reply_message_id>` only after Toby actually approves the audio.

### Shorts
- AgentStack Daily/OpenClaw Daily Shorts are **approved and active** (re-approved 2026-06-06). The `youtube_shorts_pipeline.py --mode cron` runs daily at 09:30 ET and stages 2 EN short candidates per episode. Failures post to Discord `#build-log`. Do not disable the pipeline or add `SystemExit` guards without an explicit instruction from Toby. Full episode uploads and shorts staging run as separate cron processes to prevent resource contention.

### Build-log / Discord replies
- **Only post URL-based links.** Never post filesystem paths (`/Users/...`, `/tmp/...`).
- Never report sample clips unless explicitly requested.
- No `latest.mp3` URL — it no longer exists in the workflow.

### Translations
- The approved release flow runs all 4 translation stages (show notes → transcripts → audio → feeds + covers) in one go. It is idempotent on reruns. Never report "translations done" after only the first stage.

### Git hygiene
- Never commit `__pycache__/`, `*.pyc`, `*_nova.md`, or YouTube token/state files
- Never use `git add .` or `git add -A` — stage explicit paths only
- Never commit feed XML without running `xmllint --noout` first

---

## Common Failure Record

| Episode | What broke | Fix |
|---------|-----------|-----|
| EP024 | Hand-edited feed XML, duplicate + malformed entries | Use `add_feed_entry.py` only |
| EP024 | Website not rebuilt after feed push | Always run the approved release script or `release_episode.py` recovery — never raw git push |
| EP028 | Stale transcript (different stories) rendered — QC passed | `build_episode.py` now verifies story slate before QC |
| EP028 | Translation pipeline stopped after show-notes only | The approved release flow runs all stages in one command; `release_episode.py` is only the recovery path |
| EP059 | ARIA reported "Codex stopped" after delegated artifact work failed, then the detached release child inherited a bad stdin fd and died before Python init | Repair artifacts locally, run/resume `launch_approved_release.py`, and keep release subprocess stdin bound to `DEVNULL` |
| EP059 | Full release was launched before Toby approved the review audio | `build_episode.py` now records a review-audio hash and Discord review post; release scripts require a verified approving reply message for that same hash before touching feeds/website |
| EP059 | AgentStack/OpenClaw Daily shorts were discussed as if they were an approved workflow | Shorts are disabled for AgentStack Daily/OpenClaw Daily; only IronVane and Liminal shorts are approved |
