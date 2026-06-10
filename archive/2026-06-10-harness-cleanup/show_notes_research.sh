#!/bin/bash
# Show Notes Research — runs daily at 8:00 AM ET
# Success : full show notes posted to #openclaw-epNNN (new channel)
# Skip/Fail: outcome + reason posted to Discord channel 1485243812442804327
#            and logged to BUILD_LOG

BUILD_LOG=/tmp/show_notes_build.log
ALERTS_CHANNEL=1485243812442804327
GUILD_ID=1475905694145318944
BOT_TOKEN=$(grep '^DISCORD_BOT_TOKEN=' ~/.openclaw/.env 2>/dev/null | cut -d= -f2 | tr -d '"' | tr -d "'")

discord_request() {
  local method=$1 path=$2 token=$3
  curl -s -X "$method" "https://discord.com/api/v10${path}" \
    -H "Authorization: Bot $token" \
    -H "Content-Type: application/json" 2>/dev/null
}
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
  _CHAN_NAME="agent-stack-ep${NEXT_EP_PAD}"
  _CHAN_ID=""
  _CHAN_LIST=$(discord_request "GET" "/guilds/${GUILD_ID}/channels" "$BOT_TOKEN" 2>/dev/null)
  _CHAN_ID=$(echo "$_CHAN_LIST" | python3 -c "import sys,json; channels=json.load(sys.stdin); [print(c['id']) for c in channels if c['name']=='${_CHAN_NAME}']" 2>/dev/null)
  if [ -z "$_CHAN_ID" ]; then
    _CHAN_ID=$(discord_request "POST" "/guilds/${GUILD_ID}/channels" "$BOT_TOKEN" '{"name":"'$_CHAN_NAME'","type":0}' 2>/dev/null | python3 -c 'import sys,json; print(json.get("id",""))' 2>/dev/null)
  fi
  if [ -n "$_CHAN_ID" ]; then
    /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$_CHAN_ID" --message "$MSG" >> "$BUILD_LOG" 2>&1
  else
    /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1
  fi
  exit 2
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: targeting EP${NEXT_EP_PAD} (last released: EP${_LAST_EP})" >> "$BUILD_LOG"

PROMPT=$(cat <<PROMPT_EOF
Draft show notes for EP${NEXT_EP_PAD} of AgentStack Daily. Do NOT send any Telegram messages and do NOT post to Discord; the shell script will post the saved draft after QC.

STEP 0 — Draft collision check: Check if ${DRAFT_PATH} already exists. If it does:
  1. Append this line to /tmp/show_notes_build.log: '[HOLD] EP${NEXT_EP_PAD} draft already exists; decision required'
  2. Stop immediately. Do not proceed to STEP 1. The shell wrapper will post the HOLD notice to the correct Discord channel.

STEP 1 — Agent-stack release checks: check OpenClaw, Hermes Agent, OpenAI Codex, and Claude Code CLI before general news. Treat these as recurring product-release lanes, not random news stories.

Primary release sources:
- OpenClaw: fetch https://api.github.com/repos/openclaw/openclaw/releases?per_page=10 and SKIP any release where prerelease=true.
- Hermes Agent: fetch https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=10 and SKIP any release where prerelease=true.
- OpenAI Codex app/CLI: fetch https://api.github.com/repos/openai/codex/releases?per_page=10 and SKIP any release where prerelease=true. Use the release tag/version exactly as published, for example rust-v0.130.0.
- Claude Code CLI: check the current CLI package/version from a primary source, preferably npm package @anthropic-ai/claude-code and Anthropic's official Claude Code release notes/changelog. Only include it when you can verify version information and concrete changes from a primary source. This is Claude Code CLI, not Claude Desktop.

Read last 5 show_notes_episode_*.md files and extract covered version tags for all four lanes: OpenClaw vYYYY.M.D tags, Hermes Agent release tags, Codex rust-v* tags, and Claude Code CLI versions. Add a section titled ## Release Coverage Check that lists each lane, latest stable/verified version, recent episode version tags detected, and selected missing versions. In the saved markdown, use the label "Recent episode version tags detected" rather than "covered versions".

Release-selection rule (STRICT, applies independently to OpenClaw, Hermes Agent, Codex, and Claude Code CLI):
- Build each product's stable/verified release list in descending order, latest first.
- Starting from the latest stable/verified release, walk downward until you hit the first already-covered release for that same product.
- The ONLY releases you may surface for that product are the missing releases in that latest contiguous uncovered block.
- This block may contain zero, one, or multiple releases, but it must always start at the latest stable/verified release.
- If the latest stable/verified release appears in the recent episode files, DO NOT surface any older uncovered release for that product. Treat that product's release coverage as complete for this episode.
- Never pick an older uncovered release just because it is uncovered.
- Before writing, explicitly verify each product's candidate release list against the covered tags and the primary stable/verified release list.

Release-story selection:
- If any OpenClaw, Hermes Agent, Codex, or Claude Code CLI release candidates exist, put release coverage before general news.
- If multiple product lanes have new releases, either combine them into a front-of-episode Agent Stack Release Readout or split them into adjacent release stories, ordered by operational importance.
- For each included product, name the exact version/tag, what changed since the last covered version, operator/builder impact, changed commands/APIs/configs/runtime behavior, migration risks, and what agents can now do that was previously impossible or brittle.
- Do not let generic AI news displace important release deltas from these four tools.
- If there are zero valid release candidates across all four lanes, say no agent-stack release story is included.

STEP 2 — Fresh stories: web_search for AI/tech news from last 2-3 days only. Rank stories by importance to the agent stack (OpenClaw, Hermes Agent, Codex, Claude Code CLI), practical builder/operator workflows, major-model/product significance, and technical depth. Prefer stories with primary-source technical material: release notes, changelogs, papers, API docs, architecture posts, benchmarks, SDK changes, infrastructure reports, security advisories, or model/system cards. Fetch each URL to verify it loads — drop any 404. Cross-check against last 3 episode show notes — drop any topic that appears in those recent episodes. Do NOT pad with filler just to hit a story count.

STEP 2A — Research backlog: besides the selected episode slate, keep exactly three additional technically strong backup candidates in a section titled \`## Extra Research Candidates\`. Each candidate must have a verified primary link and a \`Technical depth angle:\` sentence. These are not spoken by default; they give transcript synthesis and recovery three more sourced options if the selected slate is thin or painful.

STEP 2B — Technical-depth filter (STRICT): Before selecting the slate, reject or demote generic business/M&A/funding/regulatory/hype stories unless there is a concrete technical mechanism to explain. Every non-release story must support at least one of these angles: API/runtime behavior, model architecture/training/evaluation, agent workflow mechanics, browser/computer-use details, infra/observability/safety engineering, developer tooling, hardware/power constraints with real operational implications, or security/privacy implementation details.

STEP 2C — Source-quality gate for MiniMax/Gemini synthesis: Each selected story must include at least one primary technical source and a written 'Technical depth angle' in the Story Slate. The angle must name concrete mechanisms the episode can explain (for example: API contracts, request/response semantics, scheduling/runtime behavior, eval methodology, model/system-card constraints, failure modes, deployment knobs, observability, security boundaries, or hardware/power/cost tradeoffs). If you cannot state that angle from sources, drop the story.

STEP 3 — Draft show notes with: punchy title, tagline, story slate (2-3 sentences each), ## Extra Research Candidates with exactly three backup stories, full show notes block, verified links, ## Chapters with timestamps.

QC wording guard (STRICT): The saved markdown must not contain public recap/process phrases such as "already covered", "previously covered", "recently covered", "covered in EP", "covered in previous episodes", or "covered in recent episode notes". For the Release Coverage Check, say "Recent episode version tags detected" and "present in the recent-version scan" instead. Keep release-history bookkeeping out of public title, tagline, feed description, story slate, and show-notes block.

Editorial rules for STEP 3:
- If agent-stack release coverage exists for OpenClaw, Hermes Agent, Codex, or Claude Code CLI, it MUST be story #1 or the front release readout and the deepest block in the episode.
- Open the show-notes block on the agent-stack release versions and what actually changed. Do not open on an umbrella theme.
- Default to 3-5 total stories on non-release days; use 2-3 only when the selected stories are genuinely deep enough to carry the runtime. On release days, 2-3 stories is allowed only because the release block takes roughly half the episode.
- If there is OpenClaw, Hermes Agent, Codex, or Claude Code CLI release coverage, allocate about half the episode to concrete release details: changed components, operator surfaces, bug fixes, configs/APIs, commands, risks, migration guidance, setup steps, and exactly what agents can now do that was previously impossible or brittle.
- On release episodes, the spoken opening must start with technical details and setup/use cases for the OpenClaw/Hermes/Codex/Claude Code CLI changes. Do not spend the first minutes repeating product names, the word plugin, or generic release labels. After the concrete agent-stack operator readout, move into the selected external stories.
- If there is no agent-stack release, do not shrink into a thin news roundup. Use more technically strong stories or deeper source-backed dives so the episode still feels substantial.
- Each story segment must include a practical technical deep dive in the EP042 style: what the technology is, how the stack works, mechanisms, system design, tradeoffs, failure modes, APIs/configs, operational impact, builder implications, and practical recommendations/ratings where useful. Avoid summarizing articles at surface level.
- Every Story Slate item must include a 'Technical depth angle:' sentence for MiniMax/Gemini so synthesis knows exactly what mechanisms to explain, not just what happened.
- Theme-first umbrella framing is banned. Do not use “common thread,” “trust layer,” “these stories are all connected,” or similar language in the title, tagline, feed description, or opening.
- If covering a major OpenAI model, coding-agent, browser/computer-use, infra, or image/video release, explain the practical builder/workflow implication in generic terms. Do not mention Toby or any listener-specific personal setup.
- The release section should be concrete for every included product: what changed, why it matters, exact version/tag, and which operator/builder surfaces actually move.
- Tone target: builder workflow guide, not tech-news roundup and not implementation minutiae. Explain what a builder should use, when to use it, and how the tools combine in real workflows.
- Avoid boring low-level file/document movement unless it is the actual user-facing workflow. Do not dwell on moving files, copying documents, generic state records, or internal plumbing. Convert mechanisms into practical builder recipes.
- Default editorial target: what is new in LLMs and agents. Lead with newly released features, version changes, product updates, capability changes, ecosystem news, and why each update matters.
- Do NOT turn normal episodes into orchestration advice or builder-workflow consulting unless Toby explicitly asks for that angle. Avoid repeated which tool owns which lane framing.
- For each story, answer: what changed, what was added, who shipped it, why it matters now, what it enables, what limitation/risk changed, and what to watch next.
- Builder usefulness should be concrete but brief: one or two practical implications, not long architecture recipes.

STEP 4 — Save to ${DRAFT_PATH}

STEP 4B — Run:
  python3 ${SHOW_NOTES_QC} ${DRAFT_PATH}
If it fails, fix the draft until it passes before posting anything to Discord.

STEP 5 — Stop after STEP 4B. Do not create Discord channels and do not post messages. The shell wrapper will upload the Markdown draft as an attachment after QC passes.
PROMPT_EOF
)

/opt/homebrew/bin/openclaw agent --agent clarity-op --timeout 7200 --message "$PROMPT" \
 >> /tmp/show_notes_research.log 2>&1

EXIT_CODE=$?

# Shell-level failure detection — agent exit code and file presence check
if [ $EXIT_CODE -ne 0 ]; then
  MSG="❌ EP${NEXT_EP_PAD} research FAILED — agent exited ${EXIT_CODE}
Log: /tmp/show_notes_research.log
Build log: ${BUILD_LOG}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: agent exited $EXIT_CODE" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1

elif sed -n "${RUN_LOG_START},\$p" /tmp/show_notes_research.log | grep -qE "^Skipped EP${NEXT_EP_PAD}\b"; then
  :

elif [ ! -f "$DRAFT_PATH" ]; then
  MSG="❌ EP${NEXT_EP_PAD} research FAILED — agent exited 0 but show_notes_episode_${NEXT_EP_PAD}.md was not written
Log: /tmp/show_notes_research.log
Build log: ${BUILD_LOG}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: exited 0 but .md not written" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1

elif ! python3 "$SHOW_NOTES_QC" "$DRAFT_PATH" >> "$BUILD_LOG" 2>&1; then
  MSG="❌ EP${NEXT_EP_PAD} research FAILED — show notes QC rejected the draft
QC: python3 ${SHOW_NOTES_QC} ${DRAFT_PATH}
Log: /tmp/show_notes_research.log
Build log: ${BUILD_LOG}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: show notes QC rejected the draft" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1

else
  if ! python3 "$POST_DRAFT_DISCORD" "$_NEXT_EP" --file "$DRAFT_PATH" >> "$BUILD_LOG" 2>&1; then
    MSG="❌ EP${NEXT_EP_PAD} research FAILED — Discord draft attachment upload failed
Draft exists: show_notes_episode_${NEXT_EP_PAD}.md
Poster: python3 ${POST_DRAFT_DISCORD} ${_NEXT_EP} --file ${DRAFT_PATH}
Build log: ${BUILD_LOG}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: Discord draft upload failed" >> "$BUILD_LOG"
    /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1
    exit 1
  fi
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] OK EP${NEXT_EP_PAD}: show notes written and posted to Discord" >> "$BUILD_LOG"
fi
