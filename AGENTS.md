# OpenClaw Podcast — Project Context for Agents

Read this at the start of any session working on this project.

## What This Is

OpenClaw Daily — an AI-generated podcast with multilingual episodes (EN/DE/ES/HI/PT).

## Key Directories

- `episodes/` — final episode transcripts
- `audio/` — generated audio files
- `images/` — cover art per episode
- `translations/` — translated episode content per language
- `show_notes_episode_0NN.md` — approved story slate + show notes (source of truth for each episode)

## THE WORKFLOW — Two Commands

### Pre-greenlight (build + review)
```bash
python3 scripts/build_episode.py <N>
```
This verifies the transcript matches the approved story slate, runs QC, generates EN audio + cover, pushes to CDN, and posts the listen URL to Discord. **STOP after this. Do not proceed until Toby replies ✅.**

### Post-greenlight (full release)
```bash
python3 scripts/release_episode_approved.py <N> --pub-date "Day, DD Mon YYYY HH:MM:SS +0000"
```
This is the operator-facing post-approval command. It runs EN publish, translations, website/feed updates, the crossfire FLUX/Ken Burns video lane, localized burn-in video builds, YouTube uploads, CDN sync, and Discord in the right order. **Run this to completion — do not stop between phases.** Use `scripts/release_episode.py` only as the underlying phase library or for targeted recovery/debug work.

That's it. Everything else is handled by the scripts.

## ⛔ ABSOLUTE RULES

1. **Never reuse an existing transcript without verifying every story title matches the approved show notes.** `build_episode.py` enforces this — if you skip it, you will render the wrong episode. (EP028 failure, 2026-04-11)

2. **Never hand-edit feed.xml or translation feeds.** `release_episode_approved.py` drives the publish flow, and its feed work goes through `release_episode.py` + `add_feed_entry.py` with XML validation. Hand-editing broke EP024 feeds.

3. **Never post filesystem paths in Discord replies.** Only CDN URLs (https://clawdassistant85-netizen.github.io/...). Never report sample clips unless explicitly requested.

4. **Never say "translations done" after only completing show notes.** The translation pipeline has 4 stages (show notes → transcripts → audio → feeds+covers). The approved release flow runs all of them. Do not stop early.

5. **No `latest.mp3`.** It no longer exists. Never surface it.

6. **The approval gate is after audio is uploaded to CDN.** Toby listens at the CDN URL, then replies ✅. That reply triggers `release_episode_approved.py` — no second approval needed for feeds or localized video generation.

7. **If Toby sends a Discord voice note, transcribe it before answering.** Use:
   `python3 /Users/tobyglennpeters/.openclaw/workspace/scripts/utils/transcribe_audio.py "<audio_path>"`
   Never answer "Did you read my voice message?" from nearby text context alone.

8. **Do not claim GitHub Pages is disabled unless you verify it at the host level.**
   If a new episode URL fails, compare it with a known-good episode URL on the same `clawdassistant85-netizen.github.io/openclaw-podcast-audio` host first. If older episodes return 200, then Pages is enabled and the issue is path-specific, propagation, or file-level — not repo-level Pages being off.

## Episode Naming

- `show_notes_episode_0NN.md` — approved story slate (source of truth)
- `episodes/episode_0NN_transcript.md` — transcript (must match show notes before building)
- `images/episode_0NN_cover.png` — EN cover art
- `audio/episode_0NN.mp3` — canonical EN audio

## Spec Files

- `PODCAST_WORKFLOW.md` — full rules + common failure record
- `scripts/build_episode.py` — pre-greenlight script
- `scripts/release_episode_approved.py` — post-greenlight script
- `scripts/release_episode.py` — underlying resumable phase library / recovery tool

## Telegram/Main-Session Safety

- In ARIA's main Telegram DM: only drafting, research, transcript edits, status checks
- Never run audio generation, translations, feed updates, or deploys synchronously in the main session
- Long jobs → launch with exec background mode, end turn with a short status line
- Both pipeline scripts are designed to run detached and report completion
