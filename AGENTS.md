# OpenClaw Podcast — Project Context for Agents

Read this at the start of any session working on this project.

## What This Is
OpenClaw Daily — an AI-generated podcast with multilingual episodes (EN/DE/ES/HI/PT).

## Key Directories
- `episodes/` — final episode files (transcripts, audio)
- `audio/` — generated audio files
- `images/` — cover art per episode
- `translations/` — translated episode content
- `content_staging/` — drafts not yet approved

## Key Scripts
- `generate_audio.py` — English audio generation
- `generate_audio_lang.py` — multilingual audio generation
- `hourly_content.py` — automated content generation (cron)
- `auto_generate.sh` — full pipeline script
- `deploy.sh` — publishes feed

## Critical Files
- `feed.xml` — **NEVER edit directly without Toby approving audio first**
- `PODCAST_WORKFLOW.md` — HARD RULES, read before doing anything

## ⛔ ABSOLUTE RULES (from PODCAST_WORKFLOW.md)
1. **DO NOT generate audio until Toby explicitly approves in Discord** — this rule was violated for EP11/EP12
2. Every Discord review post MUST include all three: show notes + cover art + transcript
3. **NEVER update feed.xml or any translation feed** without Toby approving the audio first — show XML diff, wait for "go ahead", then push
4. Audio approval = explicit "go ahead" in Discord, not silence

## Telegram/Main-Session Safety
- If working from Aria's main Telegram DM session, never run long podcast steps synchronously and never babysit them with `process poll`.
- Allowed in the main Telegram session: drafting, research, transcript edits, review prep, and checking approval status.
- Not allowed in the main Telegram session: long audio generation, translated audio rendering, feed updates, publish/deploy loops, or any other long-running podcast job that would keep the DM lane occupied.
- After approval, long podcast jobs must run detached in the background with a short completion line, or be moved to desktop/web or `@TobyOllomaBot` / `local-gpt`.
- Prefer `spark` or local-model agents for long translation generation. Do not do big multilingual translation work directly in the parent Sonnet main session.

## Episode Naming
- `episode_0XX.md` — script/content
- `episodes/episode_0XX_transcript.md` — final transcript
- `images/episode_0XX_cover.png` — cover art
- Show notes: `show_notes_episode_0XX.md`

## Spec Files
- `PODCAST_WORKFLOW.md` — hard rules for every episode
- `GENERATION_NOTES.md` — technical generation notes
