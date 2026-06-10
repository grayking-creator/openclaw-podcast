#!/bin/bash
# Show Notes Research — runs daily at 8:00 AM ET
# Success : full show notes posted to #openclaw-epNNN (new channel)
# Skip/Fail: outcome + reason posted to Discord channel 1485243812442804327
#            and logged to BUILD_LOG

BUILD_LOG=/tmp/show_notes_build.log
ALERTS_CHANNEL=1485243812442804327
GUILD_ID=1475905694145318944
BOT_TOKEN=$(grep '^DISCORD_BOT_TOKEN=' ~/.openclaw/.env 2>/dev/null | cut -d= -f2 | tr -d '"')

discord_request() {
  local method=$1 path=$2 token=$3
  local body="${4:-}"
  local args=(-s -X "$method" "https://discord.com/api/v10${path}" \
    -H "Authorization: Bot $token" \
    -H "Content-Type: application/json")
  if [ -n "$body" ]; then
    args+=(-d "$body")
  fi
  curl "${args[@]}" 2>/dev/null
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
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] HOLD EP${NEXT_EP_PAD}: draft already exists; decision required" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1
  exit 2
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: targeting EP${NEXT_EP_PAD} (last released: EP${_LAST_EP})" >> "$BUILD_LOG"

GATHER_SCRIPT="${SCRIPT_DIR}/gather_research_context.py"
if [ -f "$GATHER_SCRIPT" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: running pre-flight research gatherer" >> "$BUILD_LOG"
  python3 "$GATHER_SCRIPT" >> "$BUILD_LOG" 2>&1 || true
fi

read -r -d '' PROMPT <<'PROMPT_EOF' || true
Draft show notes for EP${NEXT_EP_PAD} of AgentStack Daily. Do NOT send any Telegram messages and do NOT post to Discord; the shell script will post the saved draft after QC.

PRE-FLIGHT RESEARCH CONTEXT (EXCLUSIVE SOURCE OF TRUTH):
You MUST call your file viewing tool to read the pre-compiled research context from the local file `/tmp/agent_research_context.md` before drafting. This file contains the release history of the last 5 episodes, current upstream GitHub releases, current NPM/PyPI registry versions, newly discovered and updated models from OpenRouter, top Hacker News developer discussions, primary RSS feed announcements, and trending GitHub Project Radar candidates.
STRICT BAN ON EXTERNAL CALLS: Do NOT run any search queries, web-scraping queries, curl commands, or GitHub API calls yourself. All of the information you need is already gathered inside `/tmp/agent_research_context.md`. Use this file exclusively.

CONTEXT BUDGET — STRICT: Do not paste or ingest full README files, full changelogs, full release feeds, or full web pages. Summarize tool output before fetching more. Write the draft once the slate is verified instead of expanding optional research.

STEP 0 — Draft collision check: Check if ${DRAFT_PATH} already exists. If it does:
  1. Append this line to /tmp/show_notes_build.log: '[HOLD] EP${NEXT_EP_PAD} draft already exists; decision required'
  2. Stop immediately. Do not proceed to STEP 1. The shell wrapper will post the HOLD notice to the correct Discord channel.

STEP 1 — Agent-stack release checks: check OpenClaw, Hermes Agent, OpenAI Codex, Claude Code CLI, and Antigravity CLI before general news. Treat these as recurring product-release lanes, not random news stories.
Use the data from `/tmp/agent_research_context.md` for these checks:
- OpenClaw: Use the stable releases from the file (SKIP any release where prerelease is true).
- Hermes Agent: Use the stable releases from the file (SKIP any release where prerelease is true).
- OpenAI Codex app/CLI: Use the stable releases from the file (SKIP any release where prerelease is true).
- Claude Code CLI: Use the latest and stable versions from the NPM registry info in the file.
- Antigravity CLI (Google): Check the file for any updates. If no new concrete version or build is found in the file, note "continuous delivery, latest build as of <date>".

Read the last 5 episodes history from `/tmp/agent_research_context.md` to extract covered version tags for all five lanes. Add a section titled ## Release Coverage Check that lists each lane, latest stable/verified version, recent episode version tags detected, and selected missing versions. In the saved markdown, use the label "Recent episode version tags detected" rather than "covered versions".

Release-selection rule (STRICT, applies independently to OpenClaw, Hermes Agent, Codex, Claude Code CLI, and Antigravity CLI):
- Build each product's stable/verified release list in descending order, latest first.
- Starting from the latest stable/verified release, walk downward until you hit the first already-covered release for that same product.
- The ONLY releases you may surface for that product are the missing releases in that latest contiguous uncovered block.
- This block may contain zero, one, or multiple releases, but it must always start at the latest stable/verified release.
- If the latest stable/verified release appears in the recent episode files, DO NOT surface any older uncovered release for that product. Treat that product's release coverage as complete for this episode.
- Never pick an older uncovered release just because it is uncovered.
- Before writing, explicitly verify each product's candidate release list against the covered tags and the primary stable/verified release list.
- The no-back-to-back topic-repeat rule does not suppress a newer or missed release. If the latest upstream stable/verified version is newer than the detected episode baseline for that product, include it even if the upstream release timestamp predates the latest feed item.
- For Claude Code CLI, be explicit about whether you are using npm `latest` or Anthropic's `stable` dist-tag; keep the method consistent with the version baseline you found in recent episode files.

Release-story selection:
- If any OpenClaw, Hermes Agent, Codex, Claude Code CLI, or Antigravity CLI release candidates exist, put release coverage before general news.
- If multiple product lanes have new releases, either combine them into a front-of-episode Agent Stack Release Readout or split them into adjacent release stories, ordered by operational importance.
- For each included product, name the exact version/tag, what changed since the last covered version, operator/builder impact, changed commands/APIs/configs/runtime behavior, migration risks, and what agents can now do that was previously impossible or brittle.
- Do not let generic AI news displace important release deltas from these five tools.
- If there are zero valid release candidates across all five lanes, say no agent-stack release story is included.
- If a product has zero stable/verified release candidates, keep that fact inside `## Release Coverage Check` only. Do not promote it into the public episode title, tagline, feed description, Story Slate, timestamps, or show-notes prose as "stable watch", "watch lane", "stability check", "beta watch", or a topic headline. A beta/prerelease is not a release story.

Harness Version Reference (REQUIRED): After the ## Release Coverage Check section, add a section titled ## Harness Version Reference that lists the current latest version/build of ALL five tracked products in a simple table or bullet list. Format:
- **OpenClaw** — `<latest stable tag>`
- **Hermes Agent** — `<latest stable tag>`
- **OpenAI Codex** — `<latest stable tag>`
- **Claude Code CLI** — `<latest npm latest tag>`
- **Antigravity CLI** — `<latest version or build date>`

STEP 1A — Model discovery checks: Check the OpenRouter Models section inside `/tmp/agent_research_context.md` to discover major new or materially updated AI models. Do NOT run any search engine queries or web searches yourself.
Add a saved section titled `## Model Discovery Check` that lists each model lane or provider, recent models detected in the last 5 episodes, newly discovered models post-last-update, and selected candidates for the Story Slate.

For each newly discovered model post-last-update, include a bullet in the saved section with:
- Model name/version and provider.
- Release date or verified freshness.
- Primary source URL.
- Availability status (API, app/product, open weights, local deployment, etc.).
- Concrete capabilities (architecture, context length, multimodal or coding agent focus).
- Integration/agent impact: a "Try now / integration angle:" sentence explaining how coding agents or developers can leverage it immediately.
- You MUST start the decision line with the exact word 'Decision:' (for example: 'Decision: Selected' or 'Decision: Not Selected' followed by reason). This word prefix is strictly required by the QC checker.

Model-story selection:
- Major model drops are first-class story candidates.
- Do NOT re-select or cover models that were already featured in the last 5 episodes.
- MiniMax M3 has already been covered and should not be covered again.
- Whenever you mention 'MiniMax M3' anywhere in the document (including in the Model Discovery Check decisions or comments), you MUST append this exact parenthetical suffix to it: (featuring MSA sparse attention, 1M context, multimodal, MiniMax Code, and API availability). Note that the word 'multimodal' MUST be used exactly, NOT 'multimodality', as the word boundary match requires 'multimodal'.

STEP 2 — Fresh stories: Use the Hacker News Developer Discussions and Primary Lab RSS Announcements sections inside `/tmp/agent_research_context.md` to select the top stories. Do NOT perform any search engine queries or URL scraping. Rank stories by importance to the agent stack (OpenClaw, Hermes Agent, Codex, Claude Code CLI), practical workflows, and technical depth.
- **STORY SLATE COUNT RULE (STRICT)**: For EP055+, the Story Slate MUST contain exactly six numbered topics. Each of the six must carry all three labeled lines (Technical depth angle, Actionability angle, Listener hook). If there are not enough general news stories to reach six, promote candidates from GitHub Project Radar or the Extra Research Candidates list to make up exactly six stories.

STEP 2A — GitHub Project Radar: Use the GitHub Project Radar Suggestions section in `/tmp/agent_research_context.md` to select your repository candidates. Do NOT run any GitHub API calls or searches yourself.
The saved draft MUST include a section titled `## GitHub Project Radar` with at least three verified repo bullets. Each bullet MUST include a direct github.com repository link (for example: https://github.com/owner/repo), `Stack improvement angle:`, and `Try now:`. Do not use blog posts or non-github links under this section, as the QC checker requires at least three unique github.com URLs.

STEP 2B — Research backlog: keep exactly three additional backup candidates in a section titled `## Extra Research Candidates`. Each candidate must have a verified primary link and a `Technical depth angle:` sentence.

STEP 2C — Technical-depth filter (STRICT): Reject generic business/funding/hype stories. Every non-release story must support a concrete technical mechanism (API, architecture, agent workflow, safety, security).

STEP 2D — Source-quality gate: Each selected story must include at least one primary link and a 'Technical depth angle' in the Story Slate.

STEP 3 — Draft show notes structure:
You MUST structure the saved draft in this exact order, using exactly these Markdown headings:

# AgentStack Daily EP${NEXT_EP_PAD} — [Summary of headline releases and stories]

**Title:** [Episode Title]

**Tagline:** [One-paragraph tagline summarizing the stories]

**Feed description:** [One-paragraph feed description summarizing the stories]

---

## Story Slate

[Exactly 6 numbered story slate topics. Each topic MUST have the format:
1. **Topic Title** — One-paragraph description of what happened and what it is.
Technical depth angle: [Under 120 words, explaining technical details/mechanisms]
Actionability angle: [Under 2-3 sentences. Explain what this means for builders/workflows. You can include at most one or two concrete examples, but keep the total number of imperative ('do this') sentences to at most two (strictly less than 3 sentences). Phrase as 'what this means' / 'why this matters' instead of a to-do list.]
Listener hook: [A single sentence listenable reason to care.]
]

---

## Model Discovery Check

[Model Discovery Check section as defined in STEP 1A]

---

## Local LLM Spotlight

- **[Model Name]** — [Primary Link] — [Description of model and capabilities].
  Try now: [One-line local deployment/test use case]

---

## GitHub Project Radar

[GitHub Project Radar section as defined in STEP 2A]

---

## Extra Research Candidates

[Extra Research Candidates section as defined in STEP 2B]

---

## Show Notes

```md
Episode ${NEXT_EP_PAD} — [Current Date, e.g., June 9, 2026]

[00:00] Episode hook

[Paragraph of intro hook text, around 120-150 words. If this is a release episode, it MUST name the release and include every covered release tag within the first 180 words.]

[02:00] [Story 1 Title]

[Detailed paragraphs for Story 1. If this is a release story, it must have at least 260 words of concrete release detail: changed components, operator surfaces, configs/APIs/commands, fixes, migration risk, and what agents can now do.]

[MM:SS] [Story 2 Title]

[Detailed paragraphs for Story 2]

... (Cover all 6 stories with timestamps)

[MM:SS] Practical queue

[Summary paragraph of try-now actions for all stories]
```

---

## Chapters

- 00:00 — Intro: [Brief summary]
- 02:00 — [Story 1 Title]
- ... (Chapters list with timestamps matching Show Notes section)

---

## Primary Links

- [Story 1 Name]: [Link]
- ... (List of links for all stories and projects)

---

## Release Coverage Check

[Release Coverage Check section as defined in STEP 1]

---

## Harness Version Reference

[Harness Version Reference section as defined in STEP 1]

QC wording guard (STRICT):
STRICT WORDING BAN: Do NOT use phrases like 'covered in EP...', 'previously covered', 'already covered', or 'discussed in prior episodes' ANYWHERE in the document (including in the internal Model Discovery Check or Release Coverage Check sections). If you refer to older versions or models, use date references ONLY (e.g. 'featured on June 5', 'featured on June 3', or 'no changes since the June 8 broadcast').
For the Release Coverage Check, use only the label "Recent episode version tags detected" for the detected-tags line.

Editorial rules for STEP 3:
- If agent-stack release coverage exists for OpenClaw, Hermes Agent, Codex, Claude Code CLI, or Antigravity CLI, it MUST be story #1 or the front release readout and the deepest block in the episode.
- Open the show-notes block on the agent-stack release versions and what actually changed. Do not open on an umbrella theme.
- The Story Slate must contain exactly 6 stories.
- If covering a major OpenAI model, coding-agent, browser/computer-use, infra, or image/video release, explain the practical builder/workflow implication in generic terms. Do not mention Toby or any listener-specific personal setup.
- The release section should be concrete for every included product: what changed, why it matters, exact version/tag, and which operator/builder surfaces actually move.
- Tone target: builder workflow guide, not tech-news roundup and not implementation minutiae. Explain what a builder should use, when to use it, and how the tools combine in real workflows.
- Avoid boring low-level file/document movement unless it is the actual user-facing workflow. Do not dwell on moving files, copying documents, generic state records, or internal plumbing. Convert mechanisms into practical builder recipes.
- Default editorial target: what is new in LLMs and agents. Lead with newly released features, version changes, product updates, capability changes, ecosystem news, and why each update matters.
- Do NOT turn normal episodes into orchestration advice or builder-workflow consulting.
- For each story, answer: what changed, what was added, who shipped it, why it matters now, what it enables, what limitation/risk changed, and what to watch next.
- Builder usefulness should be concrete but brief: one or two practical implications, not long architecture recipes.

STEP 4 — Save the draft to ${DRAFT_PATH}.
- Write the file with your file-writing/editor tool (apply_patch / write_file) directly. Do NOT pipe the markdown through a shell heredoc, echo, printf, or `cat <<EOF`. The draft contains apostrophes, backticks, and dollar signs; pushing 20KB+ of markdown through a quoted shell command is the known failure mode that aborts the turn with an "unexpected EOF while looking for matching quote" error and leaves no file written.
- After writing, verify the file exists and is non-empty (for example: wc -c ${DRAFT_PATH}). If it is missing or empty, write it again before doing anything else. Do NOT end the turn until ${DRAFT_PATH} exists and is non-empty.

STEP 4B — Run:
  python3 ${SHOW_NOTES_QC} ${DRAFT_PATH}
If it fails, fix the draft until it passes before posting anything to Discord.

STEP 5 — Stop after STEP 4B. Do not create Discord channels and do not post messages. The shell wrapper will upload the Markdown draft as an attachment after QC passes. Before ending the turn, confirm one final time that ${DRAFT_PATH} exists, is non-empty, and passed QC.
PROMPT_EOF
PROMPT=${PROMPT//\$\{NEXT_EP_PAD\}/$NEXT_EP_PAD}
PROMPT=${PROMPT//\$\{DRAFT_PATH\}/$DRAFT_PATH}
PROMPT=${PROMPT//\$\{SHOW_NOTES_QC\}/$SHOW_NOTES_QC}

# The agent CLI can exit 0 even when the underlying model turn failed.
# Treat a QC-passing draft or explicit Skip as the only success signal, and
# route each attempt through a fresh session so one provider failure does not
# poison the next model with an oversized failed context.
OPENCLAW_BIN="${OPENCLAW_BIN:-/opt/homebrew/bin/openclaw}"
RESEARCH_PASSES="${SHOW_NOTES_RESEARCH_PASSES:-${SHOW_NOTES_RESEARCH_ATTEMPTS:-3}}"
AGENT_NAME="${SHOW_NOTES_AGENT:-sage}"
PING_TIMEOUT="${SHOW_NOTES_PING_TIMEOUT:-90}"
AGENT_TIMEOUT="${SHOW_NOTES_AGENT_TIMEOUT:-600}"
SHOW_NOTES_RESEARCH_ROUTES="${SHOW_NOTES_RESEARCH_ROUTES:-sage|google/gemini-3-flash-preview
sage|google-2/gemini-2.5-flash
sage|minimax/MiniMax-M2.7
sage|nvidia/meta/llama-3.3-70b-instruct
sage|mistral/mistral-large-latest
sage|groq/llama-3.3-70b-versatile}"
PROVIDER_HARD_FAIL_REGEX="${SHOW_NOTES_PROVIDER_HARD_FAIL_REGEX:-(429|402|RESOURCE_EXHAUSTED|quota|Quota exceeded|depleted|monthly included credits|billing|rate limit|rate-limit|API rate limit|cooldown|model_not_found|HTTP 404|404 page not found|Unauthorized|401|403|Unknown arguments|LLM request failed)}"

next_research_log_line() {
  if [ -f /tmp/show_notes_research.log ]; then
    echo $(( $(wc -l < /tmp/show_notes_research.log) + 1 ))
  else
    echo 1
  fi
}

research_log_has() {
  local start_line="$1"
  local pattern="$2"
  sed -n "${start_line},\$p" /tmp/show_notes_research.log 2>/dev/null | grep -qiE "$pattern"
}

route_slug() {
  printf "%s" "$1" | tr -c 'A-Za-z0-9' '-' | sed 's/--*/-/g; s/^-//; s/-$//'
}

ROUTES_FILE=$(mktemp /tmp/show-notes-routes.XXXXXX)
printf "%s\n" "$SHOW_NOTES_RESEARCH_ROUTES" | sed '/^[[:space:]]*$/d' > "$ROUTES_FILE"
ROUTE_COUNT=$(wc -l < "$ROUTES_FILE" | tr -d '[:space:]')

EXIT_CODE=0
OUTCOME="none"   # none | skipped | qc_ok | qc_failed
ROUTE_ATTEMPTS=0
PING_SKIPS=0
PROVIDER_SKIPS=0
pass=1

while [ "$pass" -le "$RESEARCH_PASSES" ]; do
  route_index=0
  while IFS= read -r ROUTE; do
    route_index=$(( route_index + 1 ))
    ROUTE_AGENT="${ROUTE%%|*}"
    ROUTE_MODEL="${ROUTE#*|}"
    if [ "$ROUTE_AGENT" = "$ROUTE_MODEL" ]; then
      ROUTE_AGENT="$AGENT_NAME"
    fi
    ROUTE_SLUG=$(route_slug "${ROUTE_AGENT}-${ROUTE_MODEL}")
    SESSION_BASE="show-notes-ep${NEXT_EP_PAD}-p${pass}-r${route_index}-${ROUTE_SLUG}-$(date +%s)"

    PING_LOG_START=$(next_research_log_line)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: EP${NEXT_EP_PAD} preflight pass ${pass}/${RESEARCH_PASSES} route ${route_index}/${ROUTE_COUNT} ${ROUTE_MODEL}" >> "$BUILD_LOG"
    "$OPENCLAW_BIN" agent --agent "$ROUTE_AGENT" --session-key "agent:${ROUTE_AGENT}:${SESSION_BASE}-ping" --model "$ROUTE_MODEL" --timeout "$PING_TIMEOUT" --thinking off --message "Health check only. Reply exactly: PONG" \
      >> /tmp/show_notes_research.log 2>&1
    EXIT_CODE=$?

    if research_log_has "$PING_LOG_START" "$PROVIDER_HARD_FAIL_REGEX"; then
      PING_SKIPS=$(( PING_SKIPS + 1 ))
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: EP${NEXT_EP_PAD} skipped ${ROUTE_MODEL}; preflight found quota/auth/rate/model failure" >> "$BUILD_LOG"
      continue
    fi
    if ! research_log_has "$PING_LOG_START" "PONG"; then
      PING_SKIPS=$(( PING_SKIPS + 1 ))
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: EP${NEXT_EP_PAD} skipped ${ROUTE_MODEL}; preflight did not return PONG (exit ${EXIT_CODE})" >> "$BUILD_LOG"
      continue
    fi

    ROUTE_ATTEMPTS=$(( ROUTE_ATTEMPTS + 1 ))
    RUN_LOG_ATTEMPT_START=$(next_research_log_line)
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: EP${NEXT_EP_PAD} run ${ROUTE_ATTEMPTS} pass ${pass}/${RESEARCH_PASSES} route ${route_index}/${ROUTE_COUNT} ${ROUTE_MODEL}" >> "$BUILD_LOG"
    "$OPENCLAW_BIN" agent --agent "$ROUTE_AGENT" --session-key "agent:${ROUTE_AGENT}:${SESSION_BASE}" --model "$ROUTE_MODEL" --timeout "$AGENT_TIMEOUT" --thinking off --message "$PROMPT" \
      >> /tmp/show_notes_research.log 2>&1
    EXIT_CODE=$?

    if sed -n "${RUN_LOG_START},\$p" /tmp/show_notes_research.log | grep -qE "^Skipped EP${NEXT_EP_PAD}\b"; then
      OUTCOME="skipped"
      break 2
    fi

    if [ -f "$DRAFT_PATH" ]; then
      if python3 "$SHOW_NOTES_QC" "$DRAFT_PATH" >> "$BUILD_LOG" 2>&1; then
        OUTCOME="qc_ok"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: EP${NEXT_EP_PAD} run ${ROUTE_ATTEMPTS} (${ROUTE_MODEL}) draft passed QC" >> "$BUILD_LOG"
        break 2
      fi
      OUTCOME="qc_failed"
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: EP${NEXT_EP_PAD} run ${ROUTE_ATTEMPTS} (${ROUTE_MODEL}) draft FAILED QC (agent exit ${EXIT_CODE})" >> "$BUILD_LOG"
      # Archive the rejected draft (name kept off the show_notes_episode_*.md glob)
      # so the next route regenerates past the agent's STEP 0 collision check.
      mv -f "$DRAFT_PATH" "${DRAFT_PATH}.rejected.pass${pass}.route${route_index}" 2>> "$BUILD_LOG"
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: archived rejected draft, trying next route" >> "$BUILD_LOG"
    else
      OUTCOME="none"
      if research_log_has "$RUN_LOG_ATTEMPT_START" "$PROVIDER_HARD_FAIL_REGEX"; then
        PROVIDER_SKIPS=$(( PROVIDER_SKIPS + 1 ))
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: EP${NEXT_EP_PAD} ${ROUTE_MODEL} failed during generation with provider/quota/rate/model signal; trying next route" >> "$BUILD_LOG"
      else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] show_notes_research: EP${NEXT_EP_PAD} run ${ROUTE_ATTEMPTS} (${ROUTE_MODEL}) produced no draft (agent exit ${EXIT_CODE}); trying next route" >> "$BUILD_LOG"
      fi
    fi
  done < "$ROUTES_FILE"
  pass=$(( pass + 1 ))
done
rm -f "$ROUTES_FILE"

# Outcome handling — a QC-passing draft (or an explicit Skip) is the only success.
if [ "$OUTCOME" = "skipped" ]; then
  :

elif [ "$OUTCOME" = "qc_ok" ] && [ -f "$DRAFT_PATH" ]; then
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

elif [ "$OUTCOME" = "qc_failed" ]; then
  MSG="❌ EP${NEXT_EP_PAD} research FAILED — show notes QC rejected generated drafts after ${ROUTE_ATTEMPTS} viable model run(s) across ${RESEARCH_PASSES} pass(es) and ${ROUTE_COUNT} configured route(s)
QC: python3 ${SHOW_NOTES_QC} ${DRAFT_PATH}
Log: /tmp/show_notes_research.log
Build log: ${BUILD_LOG}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: show notes QC rejected generated drafts (${ROUTE_ATTEMPTS} viable runs, ${PING_SKIPS} preflight skips, ${PROVIDER_SKIPS} generation provider skips)" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1
  exit 1

else
  MSG="❌ EP${NEXT_EP_PAD} research FAILED — no QC-passing show_notes_episode_${NEXT_EP_PAD}.md was written after ${ROUTE_ATTEMPTS} viable model run(s), ${PING_SKIPS} preflight skip(s), and ${PROVIDER_SKIPS} generation provider skip(s)
Configured route pass(es): ${RESEARCH_PASSES}
Configured route count: ${ROUTE_COUNT}
Log: /tmp/show_notes_research.log
Build log: ${BUILD_LOG}"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAIL EP${NEXT_EP_PAD}: no QC-passing draft (${ROUTE_ATTEMPTS} viable runs, ${PING_SKIPS} preflight skips, ${PROVIDER_SKIPS} generation provider skips, last exit ${EXIT_CODE})" >> "$BUILD_LOG"
  /opt/homebrew/bin/openclaw message send --channel discord --target "channel:$ALERTS_CHANNEL" --message "$MSG" >> "$BUILD_LOG" 2>&1
  exit 1
fi
