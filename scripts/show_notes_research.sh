#!/bin/bash
# Show Notes Research — runs daily at 8:00 AM ET
# Success : full show notes posted to #openclaw-epNNN (new channel)
# Skip/Fail: outcome + reason posted to Discord channel 1485243812442804327
#            and logged to BUILD_LOG

BUILD_LOG=/tmp/show_notes_build.log
ALERTS_CHANNEL=1485243812442804327
SCRIPT_DIR=/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/scripts
PODCAST_DIR=/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast
DONE_FILE="${SCRIPT_DIR}/youtube_uploaded.txt"
SYNC_SCRIPT="${SCRIPT_DIR}/sync_uploaded_from_youtube.py"
SHOW_NOTES_QC="${SCRIPT_DIR}/check_show_notes.py"
POST_DRAFT_DISCORD="${SCRIPT_DIR}/post_show_notes_draft_discord.py"

# Sync against the live YouTube channel before picking the next episode.
if [ -f "$SYNC_SCRIPT" ]; then
  python3 "$SYNC_SCRIPT" >> "$BUILD_LOG" 2>&1 || true
fi

_LAST_EP=$(tail -1 "$DONE_FILE" | tr -d '[:space:]')
_NEXT_EP=$(( 10#$_LAST_EP + 1 ))
NEXT_EP_PAD=$(printf "%03d" "$_NEXT_EP")
DRAFT_PATH="${PODCAST_DIR}/show_notes_episode_${NEXT_EP_PAD}.md"

RUN_LOG_START=1
if [ -f /tmp/show_notes_research.log ]; then
  RUN_LOG_START=$(( $(wc -l < /tmp/show_notes_research.log) + 1 ))
fi

if [ -f "$DRAFT_PATH" ]; then
  MSG="⚠️ EP${NEXT_EP_PAD} draft already exists and has not been released
File: show_notes_episode_${NEXT_EP_PAD}.md

The show-notes job is stopping here so we do not strand yesterday's stories or silently create EP$(printf "%03d" $(( _NEXT_EP + 1 ))).

Choose one recovery path:
1. Keep the prior stories: merge this draft's Story Slate into the next approved episode before transcript generation.
   Helper: python3 ${SCRIPT_DIR}/resolve_episode_gap.py prepare-merge --prior ${_NEXT_EP} --target $(printf "%03d" $(( _NEXT_EP + 1 )))
2. Replace the prior stories: archive this draft and reuse EP${NEXT_EP_PAD} for the new story slate, regenerating downstream assets from that replacement.
   Helper: python3 ${SCRIPT_DIR}/resolve_episode_gap.py archive ${_NEXT_EP} --reason 'replaced before transcript generation'

No new draft was created. This is a release-numbering decision, not a YouTube upload status."
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] HOLD EP${NEXT_EP_PAD}: unreleased draft already exists; decision required" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1
  exit 2
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: targeting EP${NEXT_EP_PAD} (last released: EP${_LAST_EP})" >> "$BUILD_LOG"

/opt/homebrew/bin/openclaw agent --agent main --message "Draft show notes for EP${NEXT_EP_PAD} of OpenClaw Daily. Do NOT send any Telegram messages and do NOT post to Discord; the shell script will post the saved draft after QC.

STEP 0 — Draft collision check: Check if ${DRAFT_PATH} already exists. If it does:
  1. Append this line to /tmp/show_notes_build.log: '[HOLD] EP${NEXT_EP_PAD} draft already exists; decision required'
  2. Post to Discord using the send_message tool with channel_id=${ALERTS_CHANNEL} (do NOT look up the channel by name — use this exact numeric ID) in Guild 1475905694145318944, with this exact message:
     ⚠️ [SHOW NOTES RESEARCH] EP${NEXT_EP_PAD} draft already exists and has not been released
     File: show_notes_episode_${NEXT_EP_PAD}.md
     Choose whether to merge the prior stories into the next approved episode or archive/replace the draft before generating new assets.
     Helpers:
     python3 ${SCRIPT_DIR}/resolve_episode_gap.py prepare-merge --prior ${_NEXT_EP} --target $(printf "%03d" $(( _NEXT_EP + 1 )))
     python3 ${SCRIPT_DIR}/resolve_episode_gap.py archive ${_NEXT_EP} --reason 'replaced before transcript generation'
  3. Stop immediately. Do not proceed to STEP 1.

STEP 1 — OpenClaw releases: fetch https://api.github.com/repos/openclaw/openclaw/releases?per_page=10. SKIP any release where prerelease=true. Read last 5 show_notes_episode_*.md files and extract covered version tags.

Release-selection rule (STRICT):
- Build the stable-release list in descending order (latest first).
- Starting from the latest stable release, walk downward until you hit the first already-covered stable release.
- The ONLY releases you may surface are the missing releases in that latest contiguous uncovered block.
- This block may contain zero, one, or multiple releases, but it must always start at the latest stable release.
- If the latest stable release is already covered, DO NOT surface any older uncovered release. Treat release coverage as complete for this episode and skip OpenClaw release coverage.
- Never pick an older uncovered release just because it is uncovered.
- Never say 'newest uncovered stable release' unless it is also the latest stable release.
- Before writing, explicitly verify the candidate release list against the covered tags and the GitHub stable-release list. If there are zero valid candidates, say no OpenClaw release story is included.

STEP 2 — Fresh stories: web_search for AI/tech news from last 2-3 days only. Rank stories by importance to OpenClaw, practical builder/operator workflows, major-model/product significance, and technical depth. Prefer stories with primary-source technical material: release notes, changelogs, papers, API docs, architecture posts, benchmarks, SDK changes, infrastructure reports, security advisories, or model/system cards. Fetch each URL to verify it loads — drop any 404. Cross-check against last 3 episode show notes — drop any topic already covered. Do NOT pad with filler just to hit a story count.

STEP 2B — Technical-depth filter (STRICT): Before selecting the slate, reject or demote generic business/M&A/funding/regulatory/hype stories unless there is a concrete technical mechanism to explain. Every non-release story must support at least one of these angles: API/runtime behavior, model architecture/training/evaluation, agent workflow mechanics, browser/computer-use details, infra/observability/safety engineering, developer tooling, hardware/power constraints with real operational implications, or security/privacy implementation details.

STEP 2C — Source-quality gate for MiniMax/Gemini synthesis: Each selected story must include at least one primary technical source and a written "Technical depth angle" in the Story Slate. The angle must name concrete mechanisms the episode can explain (for example: API contracts, request/response semantics, scheduling/runtime behavior, eval methodology, model/system-card constraints, failure modes, deployment knobs, observability, security boundaries, or hardware/power/cost tradeoffs). If you cannot state that angle from sources, drop the story.

STEP 3 — Draft show notes with: punchy title, tagline, story slate (2-3 sentences each), full show notes block, verified links, ## Chapters with timestamps.

Editorial rules for STEP 3:
- If OpenClaw release coverage exists, it MUST be story #1 and the deepest block in the episode.
- Open the show-notes block on the release versions and what actually changed. Do not open on an umbrella theme.
- Default to 3-5 total stories on non-release days; use 2-3 only when the selected stories are genuinely deep enough to carry the runtime. On release days, 2-3 stories is allowed only because the release block takes roughly half the episode.
- If there is an OpenClaw release, allocate about half the episode to concrete release details: changed components, operator surfaces, bug fixes, configs/APIs, risks, migration guidance, and why each change matters.
- If there is no OpenClaw release, do not shrink into a thin news roundup. Use more technically strong stories or deeper source-backed dives so the episode still feels substantial.
- Each story segment must include a practical technical deep dive in the EP042 style: what the technology is, how the stack works, mechanisms, system design, tradeoffs, failure modes, APIs/configs, operational impact, builder implications, and practical recommendations/ratings where useful. Avoid summarizing articles at surface level.
- Every Story Slate item must include a "Technical depth angle:" sentence for MiniMax/Gemini so synthesis knows exactly what mechanisms to explain, not just what happened.
- Theme-first umbrella framing is banned. Do not use “common thread,” “trust layer,” “these stories are all connected,” or similar language in the title, tagline, feed description, or opening.
- If covering a major OpenAI model, coding-agent, browser/computer-use, infra, or image/video release, explain the practical builder/workflow implication in generic terms. Do not mention Toby or any listener-specific personal setup.
- The release section should be concrete: what changed, why it matters, and which operator/builder surfaces actually move.
- Tone target: technical operator briefing, not tech-news roundup. Less article recap; more explanation of how the technology works and what changes for builders.

STEP 4 — Save to ${DRAFT_PATH}

STEP 4B — Run:
  python3 ${SHOW_NOTES_QC} ${DRAFT_PATH}
If it fails, fix the draft until it passes before posting anything to Discord.

STEP 5 — Stop after STEP 4B. Do not create Discord channels and do not post messages. The shell wrapper will upload the Markdown draft as an attachment after QC passes." \
  >> /tmp/show_notes_research.log 2>&1

EXIT_CODE=$?

# Shell-level failure detection — agent exit code and file presence check
if [ $EXIT_CODE -ne 0 ]; then
  MSG="❌ EP${NEXT_EP_PAD} research FAILED — agent exited ${EXIT_CODE}
Log: /tmp/show_notes_research.log
Build log: ${BUILD_LOG}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: agent exited $EXIT_CODE" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1

elif sed -n "${RUN_LOG_START},\$p" /tmp/show_notes_research.log | grep -q "Skipped EP${NEXT_EP_PAD}"; then
  :

elif [ ! -f "$DRAFT_PATH" ]; then
  MSG="❌ EP${NEXT_EP_PAD} research FAILED — agent exited 0 but show_notes_episode_${NEXT_EP_PAD}.md was not written
Log: /tmp/show_notes_research.log
Build log: ${BUILD_LOG}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: exited 0 but .md not written" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1

elif ! python3 "$SHOW_NOTES_QC" "$DRAFT_PATH" >> "$BUILD_LOG" 2>&1; then
  MSG="❌ EP${NEXT_EP_PAD} research FAILED — show notes QC rejected the draft
QC: python3 ${SHOW_NOTES_QC} ${DRAFT_PATH}
Log: /tmp/show_notes_research.log
Build log: ${BUILD_LOG}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: show notes QC rejected the draft" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1

else
  if ! python3 "$POST_DRAFT_DISCORD" "$_NEXT_EP" --file "$DRAFT_PATH" >> "$BUILD_LOG" 2>&1; then
    MSG="❌ EP${NEXT_EP_PAD} research FAILED — Discord draft attachment upload failed
Draft exists: show_notes_episode_${NEXT_EP_PAD}.md
Poster: python3 ${POST_DRAFT_DISCORD} ${_NEXT_EP} --file ${DRAFT_PATH}
Build log: ${BUILD_LOG}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: Discord draft upload failed" >> "$BUILD_LOG"
    /opt/homebrew/bin/openclaw message send --channel discord --target "$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1
    exit 1
  fi
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] OK EP${NEXT_EP_PAD}: show notes written and posted to Discord" >> "$BUILD_LOG"
fi
