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
7. Posts listen URL to `#openclaw-ep0NN` in Discord

**⛔ STOP after this. Do not proceed until Toby replies ✅.**

**Required inputs before running:**
- `show_notes_episode_0NN.md` — approved story slate
- `episodes/episode_0NN_transcript.md` — transcript built from that slate (not reused from disk without verification)

---

## Script 2 — Release (post-greenlight)

```bash
python3 scripts/release_episode_approved.py <N> --pub-date "Day, DD Mon YYYY HH:MM:SS +0000"
```

**What it does:**
1. `setup` — verify EN assets and canonicalize audio name
2. Launch three lanes in parallel:
   EN publish to feed + website
   translations (show notes + transcript + audio + covers)
   EN crossfire FLUX/Ken Burns video build
3. Publish translated feeds + website as soon as translated assets are ready
4. Build localized burn-in YouTube masters from the crossfire episode outputs
5. Upload all 5 localized videos to YouTube
6. Sync CDN + post Discord release message

`scripts/release_episode.py` remains the resumable phase library underneath this flow. Use it directly only for targeted recovery/debug work.

**Recovery / targeted restart:**
```bash
python3 scripts/release_episode.py 28 --from-phase covers --pub-date "..."
```

---

## Hard Rules (locked — do not override)

### Transcript
- **NEVER reuse an existing `episode_0NN_transcript.md` without verifying it matches the approved story slate.** `build_episode.py` enforces this automatically. If you're writing a transcript manually, read `show_notes_episode_0NN.md` first and verify every story title appears in the transcript before running the build script.

### Feeds
- **NEVER hand-edit feed.xml or translation feeds.** `release_episode_approved.py` uses `release_episode.py` + `add_feed_entry.py`, which validates XML before and after. Hand-editing broke EP024 feeds.

### Approval gate
- Audio is uploaded to CDN before asking for approval. Toby listens at the posted URL, then replies ✅ to trigger `release_episode_approved.py`.
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
