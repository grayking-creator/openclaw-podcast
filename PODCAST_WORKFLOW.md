# PODCAST WORKFLOW — Hard Rules (locked 2026-03-12)

## ⛔ ABSOLUTE GATE — NO AUDIO WITHOUT DISCORD APPROVAL

**ARIA MUST NOT generate audio until Toby explicitly approves in Discord.**
This rule was violated for EP11 and EP12. It will not happen again.

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

### Step 4 — Publish
- [ ] Update `feed.xml` with EN episode entry
- [ ] Update translation feeds (feed_de, feed_es, feed_pt, feed_hi) with translated entries
- [ ] Push audio + cover to CDN repo (`openclaw-podcast-audio`)
- [ ] **Run publish script** (handles cover art copy + website build + push automatically):
  ```bash
  bash openclaw-podcast/publish_episode.sh <episode_number>
  ```
  This script:
  1. Copies cover art to `websiteBuilder/frontend/public/images/podcast/` ← the step that kept getting missed
  2. Verifies feed.xml has the episode
  3. Pushes podcast repo
  4. Refreshes training data + builds website
  5. Pushes website
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

