# AgentStack Podcast — Project Context for Agents

Read this at the start of any session working on this project.

## What This Is

AgentStack Daily — an AI-generated podcast with multilingual episodes (EN/DE/ES/HI/PT).

## Key Directories

- `episodes/` — final episode transcripts
- `audio/` — generated audio files
- `images/` — cover art per episode
- `translations/` — translated episode content per language
- `show_notes_episode_0NN.md` — approved story slate + show notes (source of truth for each episode)

## THE WORKFLOW — Two Commands

### Pre-greenlight (build + review)

**Step 1 — Write the transcript** (required before the build script can run):
Generate `episodes/episode_0NN_transcript.md` from the approved show notes in `show_notes_episode_0NN.md`. Use `[NOVA]:` and `[ALLOY]:` speaker turns, `[PAUSE]` between sections, and section headers with timestamps. See any existing `episodes/episode_0NN_transcript.md` for the exact format.

**Step 2 — Run the build:**
```bash
python3 scripts/build_episode.py <N>
```
This verifies the transcript matches the approved story slate, runs QC, generates EN audio + cover, pushes to CDN, and posts the listen URL to Discord. **STOP after this. Do not proceed until Toby replies ✅.**

`build_episode.py` will fail immediately with a Discord notification if the transcript file is missing — do not skip Step 1.

### Post-greenlight (full release)
```bash
python3 scripts/launch_approved_release.py <N> --pub-date "Day, DD Mon YYYY HH:MM:SS +0000"
```
This is the operator-facing post-approval command. It detaches the approved release, starts a watchdog, and runs EN publish, translations, website/feed updates, the crossfire FLUX/Ken Burns video lane, localized burn-in video builds, YouTube uploads, CDN sync, and Discord in the right order. **Run this to completion — do not stop between phases.** Use `scripts/release_episode.py` only as the underlying phase library or for targeted recovery/debug work.

That's it. Everything else is handled by the scripts.

## ⛔ Active Episode Rule — Always Verify From Disk

When asked about episode upload status, "Can you fix this?", or any failure diagnosis **without an explicit episode number in the message**:

1. **Always read state files first** before drawing any conclusion:
   ```bash
   python3 -c "
   import glob, json, os
   files = sorted(glob.glob('/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/scripts/release_ep*_state.json'), key=os.path.getmtime, reverse=True)[:5]
   for f in files:
       s = json.loads(open(f).read())
       meta = s.get('approved_orchestrator', {})
       results = meta.get('lane_results', {})
       print(os.path.basename(f), '|', {k: v.get('status') for k, v in results.items()})
   "
   ```

2. The **active broken episode** is the most recently modified state file with a lane showing `status: failed` or missing a step that should be complete.

3. **Never assume the active episode from** in-session context, what was discussed earlier, or background process completion notifications. A background completion event (e.g. `Exec completed (dawn-gul, code 1)`) only means a subprocess exited — it does **not** mean the referenced episode is the current issue.

4. **EP036 incident (2026-04-23):** A stale `dawn-gulf` EP036 rerun notification fired 12 hours late at 8:40 PM. ARIA treated it as the active failure, checked EP036 (already complete), declared "Fixed", and missed the real EP038 translation failure. This rule prevents that mistake.

## ⛔ ABSOLUTE RULES

1. **Never reuse an existing transcript without verifying every story title matches the approved show notes.** `build_episode.py` enforces this — if you skip it, you will render the wrong episode. (EP028 failure, 2026-04-11)

2. **Never hand-edit feed.xml or translation feeds.** `release_episode_approved.py` drives the publish flow, and its feed work goes through `release_episode.py` + `add_feed_entry.py` with XML validation. Hand-editing broke EP024 feeds.

3. **Never post filesystem paths in Discord replies.** Only CDN URLs (https://clawdassistant85-netizen.github.io/...). Never report sample clips unless explicitly requested.

4. **Never say "translations done" after only completing show notes.** The translation pipeline has 4 stages (show notes → transcripts → audio → feeds+covers). The approved release flow runs all of them. Do not stop early.

5. **No `latest.mp3`.** It no longer exists. Never surface it.

6. **The approval gate is after audio is uploaded to CDN.** Toby listens at the CDN URL, then replies ✅. That reply triggers `launch_approved_release.py` — no second approval needed for feeds or localized video generation.

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

## Editorial Rules (locked)

- Daily episodes are expected to deliver about **30 minutes of actual content by default**. The cron may produce a shorter draft when the topic slate is weak, but review drafts should be expanded back to roughly 30 minutes unless Toby explicitly asks for a shorter special.
- If OpenClaw release coverage exists, it is story #1 and the deepest part of the episode.
- The opening must get to the release versions and concrete release changes fast. Do not spend the intro on an abstract umbrella theme.
- If there is **no** qualifying OpenClaw release, do not open by announcing that absence, listing previously covered release tags, or explaining the release check in spoken detail. The listener should not hear a roll call of already-covered tags.
- No-release episodes still need a strong conversational hook in the first minute. Do not say things like “this is not a release episode,” “no release coverage,” or similar meta-throat-clearing in the spoken opening.
- The spoken intro must be conversational and entertaining, not a mechanical list of what will be covered. Avoid “five stories today” / “here’s the list” style openings unless Toby explicitly asks for that format.
- When the news slate is weak, **add stronger outside stories or deepen builder/use-case analysis** rather than letting the episode collapse below target length.
- Cut low-priority stories before cutting release detail. Default to 2-4 total stories, not a padded 5-6. Exception: if Toby explicitly asks to keep the existing outside stories and add a newly landed release on top, honor that even if the episode expands well past normal runtime.
- Theme-first umbrella framing is banned. Do not use “common thread,” “trust layer,” or “these stories are all connected” framing.
- Major outside stories should be ranked by importance to OpenClaw, practical builder/operator workflows, and major-model significance.
- Never mention Toby or any listener-specific personal setup inside the episode body. If a workflow angle matters, describe it generically.
- Exception for explicitly requested special episodes: if Toby asks for a setup-specific/private episode, you may explain his real build/setup directly, but do not include meta-process notes about his revision feedback, changing direction, or your drafting process inside the episode.
- Critical podcast feedback persistence rule (locked 2026-04-23): if Toby gives corrective feedback on episode framing/opening/editorial handling, update this project file and report the exact files changed. Do not just say you understood.
- Discord draft handling rule (locked 2026-04-23): if an episode draft is materially revised after posting in the per-episode Discord channel, rebuild the Discord draft in-channel from the updated show notes instead of telling Toby to inspect a filesystem path.
- If Toby rejects the audio in the first minute because the opening is bad, treat that as a transcript/QC failure, not an aesthetic difference. Fix the transcript and tighten QC before rebuilding audio.

## Spec Files

- `PODCAST_WORKFLOW.md` — full rules + common failure record
- `scripts/build_episode.py` — pre-greenlight script
- `scripts/launch_approved_release.py` — detached post-greenlight launcher + watchdog
- `scripts/release_episode_approved.py` — post-greenlight script
- `scripts/release_episode.py` — underlying resumable phase library / recovery tool

## Telegram/Main-Session Safety

- In ARIA's main Telegram DM: only drafting, research, transcript edits, status checks
- Never run audio generation, translations, feed updates, or deploys synchronously in the main session
- Long jobs → launch with exec background mode, end turn with a short status line
- Both pipeline scripts are designed to run detached and report completion
