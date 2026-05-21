# PODCAST WORKFLOW

Two scripts cover the full pipeline. Everything else is handled automatically.

---

## Script 1 — Build (pre-greenlight)

```bash
python3 scripts/build_episode.py <N>
```

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
- `episodes/episode_0NN_transcript.md` — transcript built from that slate (not reused from disk without verification)

---

## Script 2 — Release (post-greenlight)

```bash
python3 scripts/launch_approved_release.py <N> --pub-date "Day, DD Mon YYYY HH:MM:SS +0000"
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
- **Default to 2-4 total stories.** Cut lower-priority stories before cutting OpenClaw release detail.
- **Technical deep-dive standard:** use the EP042 model for future episodes: explain what each technology is, how the stack works, concrete mechanisms/APIs/configs/architecture, tradeoffs, failure modes, operational impact, and practical recommendations or ratings where useful. Less article recap; more technical review and analysis.
- **Theme-first umbrella framing is banned.** Do not build the show around phrases like “trust layer,” “common thread,” or “these stories are all connected.”
- **Never mention Toby or listener-specific setup details in the episode body.** Use generic workflow language instead. Never include drafting/request meta like “Toby wanted/requested/asked” or “requested format.” The only default exception is the exact end CTA “Toby On Fitness Tech dot com.”

### Feeds
- **NEVER hand-edit feed.xml or translation feeds.** `release_episode_approved.py` uses `release_episode.py` + `add_feed_entry.py`, which validates XML before and after. Hand-editing broke EP024 feeds.

### Approval gate
- Audio is uploaded to CDN before asking for approval. Toby listens at the posted URL, then replies ✅ to trigger `launch_approved_release.py`.
- Audio approval = automatic trigger for the full release pipeline. No second approval needed for feeds.

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
