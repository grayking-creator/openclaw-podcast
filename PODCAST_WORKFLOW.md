# PODCAST WORKFLOW — Hard Rules (locked 2026-03-12)

## ⛔ ABSOLUTE GATE — NO AUDIO WITHOUT DISCORD APPROVAL

**ARIA MUST NOT generate audio until Toby explicitly approves in Discord.**
This rule was violated for EP11 and EP12. It will not happen again.

## ✅ APPROVAL SEQUENCE (locked 2026-03-24 — do NOT ask for extra approval)

1. **Toby approves audio** → ARIA immediately pushes feeds (EN + all translation feeds). No approval needed. No asking. Just do it.
2. **ARIA shows website diff** → Toby approves → ARIA pushes website.

ARIA must NEVER ask Toby to approve the feeds after audio is approved. Feed publish is automatic on audio approval. Asking for feed approval after audio approval is a repeated process violation.

---

## Discord Review Checklist — MANDATORY for every episode

When posting to Discord for review, ALL THREE of the following are required in the same session:

1. ✅ **Show notes** — full structured notes with links (split across messages if needed)
2. ✅ **Cover art** — attach `images/episode_0XX_cover.png` as a file
3. ✅ **Transcript** — attach `episodes/episode_0XX_transcript.md` as a file

If ANY of these is missing, the review post is incomplete. Do not tell Toby "ready for review" until all three are posted.

---

## Full Episode Workflow (in order, no skipping)

### Step 1 — Build
- [ ] Write transcript → `episodes/episode_0XX_transcript.md`
- [ ] Generate cover art → `images/episode_0XX_cover.png`
- [ ] Write show notes → `show_notes_episode_0XX.md`

### Step 2 — Discord Review (GATE)
- [ ] Create `#openclaw-epXX` channel
- [ ] Post show notes (with all links)
- [ ] Post cover art as file attachment
- [ ] Post transcript as file attachment
- [ ] Post review checklist message asking for Toby's ✅

**⛔ STOP HERE. Do not proceed until Toby approves.**

### Step 3 — Audio Generation (only after approval)
- [ ] Toby reacts ✅ or explicitly says "go ahead" / "approved"
- [ ] **Run QC check first** (MANDATORY — do not skip):
  ```bash
  python3 openclaw-podcast/scripts/check_episode.py openclaw-podcast/episodes/episode_0XX_transcript.md
  ```
  Must pass all ERROR checks. Fix any failures before continuing.
- [ ] **Rebuild the nova.md render file** from the transcript (never generate audio from a stale render):
  ```bash
  python3 openclaw-podcast/scripts/render_nova.py openclaw-podcast/episodes/episode_0XX_transcript.md
  ```
- [ ] **Verify nova.md first paragraph** — read the first 5 lines and confirm structure before launching audio gen
- [ ] Generate EN audio → `audio/episode_0XX.mp3`
- [ ] **After generation: verify audio intro** — sample first 90 seconds and confirm host intro is in the right place before copying to shared
- [ ] Generate ES/DE/PT/HI translations
- [ ] Generate translated audio

### Step 3.5 — Translation QC Gate (MANDATORY)
- [ ] Run: `python3 scripts/check_episode_translations.py <episode_number>`
- [ ] Must pass ALL checks (titles translated, covers exist, show notes exist, transcripts exist, audio exists, descriptions translated)
- [ ] If any ❌ errors: FIX before proceeding. Do NOT skip.
- [ ] This gate is also enforced automatically by `publish_episode.sh`

### Step 4 — Publish

#### Feed Updates — USE THE SCRIPT, DO NOT HAND-EDIT XML

**⛔ NEVER edit feed.xml or translation feeds manually.** Use `scripts/add_feed_entry.py` for ALL feed insertions. Hand-editing XML has caused broken feeds in EP024 (duplicated EN entry, destroyed DE/ES/PT EP023 entries).

```bash
# EN feed
python3 scripts/add_feed_entry.py feed.xml \
  --episode 24 \
  --title "Episode 24: The Narrative Layer" \
  --description "Six stories about who controls the AI stack." \
  --pub-date "Sun, 05 Apr 2026 14:00:00 +0000" \
  --audio-url "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/audio/episode_024.mp3" \
  --cover-url "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/episode_024_cover.png" \
  --duration "38:00" \
  --link "https://tobyonfitnesstech.com/podcasts/episode-24/"

# Translation feeds (TRANSLATE the title and description — do NOT leave them in English)
python3 scripts/add_feed_entry.py translations/feed_de.xml \
  --episode 24 \
  --title "Folge 24: Die Erzählschicht" \
  --description "Sechs Geschichten darüber, wer den KI-Stack kontrolliert." \
  --pub-date "Sun, 05 Apr 2026 14:00:00 +0000" \
  --audio-url "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/audio/episode_024_de.mp3" \
  --cover-url "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/episode_024_cover_de.png" \
  --duration "38:00" \
  --link "https://tobyonfitnesstech.com/de/podcasts/episode-24/"

# Repeat for es, pt, hi — always translate title + description
```

The script:
- Validates XML before and after insertion
- Prevents duplicate episode numbers
- Inserts at the correct position (before the first existing `<item>`)
- Updates `lastBuildDate` automatically
- Rolls back if the resulting XML is invalid

- [ ] Run `add_feed_entry.py` for EN feed
- [ ] Run `add_feed_entry.py` for each translation feed (DE/ES/PT/HI) with TRANSLATED titles and descriptions
- [ ] **Verify translated transcript filenames** — website looks for `translations/<lang>/episode_<NNN>_<lang>.md` first, then `episode_<NNN>_<lang>_nova.md`. The `_nova` suffix variant is supported but prefer the clean name when possible.
- [ ] **Create translated show notes** for ALL 4 languages — `translations/<lang>/show_notes_episode_<NNN>_<lang>.md` — MANDATORY, not optional
  - Use **MiniMax** (`minimax` agentId) for all show notes translations — one agent per language, task: translate `show_notes_episode_0XX.md` → output to `translations/<lang>/show_notes_episode_0XX_<lang>.md`
  - ES title format: `Episodio NNN: <translated title>` | DE: `Folge NNN:` | PT: `Episódio NNN:` | HI: `एपिसोड NNN:`
  - Update episode page URL in the header to the locale path (e.g. `/es/podcasts/episode-19/`)
- [ ] **Create translated cover art thumbnails** — `episode_<NNN>_cover_<lang>.png` for de/es/pt/hi — MANDATORY, do not push translation feeds without them
  - Copy the EN cover script: `scripts/generate_episode_0XX_cover.py`
  - For each language, update `LINE1` / `LINE2` with the translated episode title and set `OUT` to `images/episode_<NNN>_cover_<lang>.png`
  - **Hindi (HI):** Arial Bold does NOT support Devanagari. Load `ITFDevanagari.ttc` (or `DevanagariMT.ttc`) as `font_title_hi` and use it for the title lines only — see EP019 cover script for the patch pattern
  - Run all 4 scripts with `python3`
  - Copy outputs to: `images/` (podcast repo), `openclaw-podcast-audio/` (CDN repo), and `websiteBuilder/frontend/public/images/podcast/` (website)
- [ ] **Copy EN cover to website** — `cp images/episode_0XX_cover.png ../../websiteBuilder/frontend/public/images/podcast/` — MANDATORY, the website auto-generates the cover path from the episode number and will show a broken image if this file is missing
- [ ] Push audio + cover to CDN repo (`openclaw-podcast-audio`)
- [ ] **Run publish script** (handles cover art copy + website build + push automatically):
  ```bash
  bash openclaw-podcast/publish_episode.sh <episode_number>
  ```
  This script:
  1. Replaces the canonical CDN audio at `openclaw-podcast-audio/audio/episode_0XX.mp3`
  2. Updates `openclaw-podcast-audio/audio/latest.mp3` so old build-log links can always hit the newest approved audio
  3. Copies cover art to both `openclaw-podcast-audio/` and `websiteBuilder/frontend/public/images/podcast/`
  4. Verifies `feed.xml` has the episode
  5. Pushes podcast repo + CDN repo
  6. Refreshes training data, builds website, and pushes website
- [ ] **Validate ALL feeds after any changes** (MANDATORY — do not push broken XML):
  ```bash
  xmllint --noout feed.xml translations/feed_de.xml translations/feed_es.xml translations/feed_pt.xml translations/feed_hi.xml
  ```
  ALL must report no errors. If any feed fails validation, DO NOT push. Fix the XML first.

- [ ] **YouTube upload** (after audio is in CDN):
  ```bash
  python3 scripts/youtube_scheduled_upload.py <episode_number>
  ```
  This renders MP4s from cover+audio and uploads to all 5 channels (EN/ES/DE/PT/HI). Skips channels that are already uploaded. Requires `ffmpeg` and Google API Python deps.

- [ ] **Verify episode appears on website** (MANDATORY — do not skip):
  Open `https://tobyonfitnesstech.com/podcasts/openclaw/` and confirm the new episode is listed.
  If it's missing, the website was not rebuilt. Fix:
  ```bash
  cd $HOME/.openclaw/workspace/websiteBuilder/frontend && npm run build
  cd .. && git add -A && git commit -m "EP<N>: website rebuild" && git push
  ```
  The `publish_episode.sh` script does this automatically — if you ran publish, the site should be updated.
  If you did NOT run `publish_episode.sh` (e.g. manual feed edits), you MUST rebuild the website manually.

  **⛔ THE EPISODE IS NOT PUBLISHED UNTIL IT APPEARS ON THE WEBSITE.**

- [ ] **Build-log / Discord message must include exact links**
  - Episode audio URL
  - Stable `latest.mp3` URL
  - Show-notes / website URL
  - Website episode page URL (verify it loads)
- [ ] Notify Toby

---

## Other Hard Rules

- NEVER send transcripts or show notes via Telegram — Discord only
- Telegram gets: short summary (≤500 chars) + Discord channel link
- Show notes must include links for every major topic/tool/model mentioned
- Topic audit: verify new topics haven't been covered in prior episodes

---

*Violated for EP11 (skipped Discord gate entirely) and EP12 (posted show notes but missing cover art + transcript). Locked 2026-03-12.*

---

## Git Hygiene — LOCKED RULES

- NEVER commit `__pycache__/`, `*.pyc`, or `*.pyo` files
- NEVER commit `scripts/youtube_channel_state.json`, `scripts/youtube_shorts_state.json`, or `scripts/youtube_uploaded.txt` — these are ephemeral upload state
- NEVER commit YouTube OAuth token files (`scripts/youtube_token*.json`, `scripts/youtube_client_secret*.json`)
- NEVER commit `tmp_short_test/` or other scratch directories
- `.gitignore` handles all of the above — do NOT override it with `git add -f`
- When adding files, use explicit paths (`git add feed.xml images/episode_024_cover.png`) — avoid `git add .` or `git add -A`

---

## Common Minimax Failures — DO NOT REPEAT

### EP024 Feed Corruption (2026-04-07)
**What happened:** Hand-editing XML feeds to insert EP024 caused:
1. EN feed: duplicate `<item>` block (EP024 appeared twice)
2. DE/ES/PT feeds: new `<item>` was inserted INSIDE the previous episode's `<title>` tag, destroying EP023's XML structure
3. Translation titles were left in English ("The Narrative Layer") instead of being translated

**Root cause:** String replacement on XML without understanding the document structure.

**Fix:** Use `scripts/add_feed_entry.py` for ALL feed insertions. It validates XML before and after, prevents duplicates, and inserts at the correct position. NEVER hand-edit feed XML files.

### EP024 Website Not Updated (2026-04-07)
**What happened:** Feed was pushed to podcast repo and YouTube uploads completed, but the episode did not appear on the website because `publish_episode.sh` was not run and the website was never rebuilt.

**Root cause:** Manual feed edits bypassed the publish script, which is the only step that triggers a website rebuild.

**Fix:** Always either run `publish_episode.sh` OR manually rebuild the website after pushing feed changes. Added a mandatory verification step: "Verify episode appears on website" — the episode is not published until it shows on the site.

---

## Episode Length — LOCKED RULE (2026-03-21)

**Minimum episode length: 30 minutes.**

All episodes must target 30 minutes or longer. This applies to transcript length (~4,500+ words at 150 wpm) and final audio duration.

- Transcript word count target: **4,500–5,500 words** (30–37 min)
- If a brief feels too thin for 30 min, add more stories, go deeper on each segment, or add a "Community Corner" / "Builder's Take" section
- Do NOT build and submit a transcript under 4,000 words — expand first

**Transcript sign-off rules (locked 2026-03-21):**
- NEVER include word counts or metadata in the transcript body (no `<!-- Word count: XXXX -->`)
- NEVER add an episode metadata footer line at the end (no `*OpenClaw Daily — Episode XX, Date*`)
- NEVER mention Discord in the outro — there is no listener Discord
- ALWAYS include a CTA to tobyonfitnesstech.com for show notes and episode archives
- NEVER say "we'll be back next week" — this is OpenClaw *Daily*, say "we'll be back soon"
- NEVER include fake UI references or MCP toggle buttons that don't exist

---

## Cold Open Format — LOCKED 2026-03-29

When using a cold open, the intro sequence MUST be:

1. **Cold open** — NOVA narrates dramatic untagged prose (2-4 sentences, no speaker label)
2. **`**NOVA:** I'm NOVA.`** — short, standalone line
3. **`**ALLOY:** And I'm ALLOY, and this is OpenClaw Daily.`** — ALLOY introduces herself AND names the show, then continues with 1-3 sentences previewing the episode before handing back
4. **NOVA** then continues with the episode content

Example:
```
[cold open prose]

**NOVA:** I'm NOVA.

**ALLOY:** And I'm ALLOY, and this is OpenClaw Daily. [PAUSE] Today we have four stories... [brief preview] ...

**NOVA:** Today we're talking about...
```

Rules:
- ALLOY must do more than just say her name — she must say "this is OpenClaw Daily" AND add substance
- NOVA's intro line must be short — not the full topic setup
- ALLOY's intro block must stand on its own before NOVA continues
- Use cold opens sparingly — not every episode

The QC script (`check_episode.py`) enforces: ALLOY intro within 400 words, back-to-back with NOVA within 4 lines.
