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

**Step 1 — Build the transcript artifact** (required before the build script can run):
Generate `episodes/episode_0NN_transcript.md` from the approved show notes in `show_notes_episode_0NN.md` with:
```bash
python3 scripts/generate_episode_transcript.py <N>
```
That script calls OpenClaw's configured OpenAI text model directly and then runs transcript QC before moving the file into place. It does not spawn nested OpenClaw agents. Transcript format: `[NOVA]:` and `[ALLOY]:` speaker turns, `[PAUSE]` between sections, and section headers with timestamps. See any existing `episodes/episode_0NN_transcript.md` for the exact format.

**Step 2 — Run the build:**
```bash
python3 scripts/build_episode.py <N>
```
This verifies the transcript matches the approved story slate, runs QC, generates EN audio + cover, pushes to CDN, and posts the listen URL to Discord. **STOP after this. Do not proceed until Toby replies ✅.**

`build_episode.py` will fail immediately with a Discord notification if the transcript file is missing — do not skip Step 1.

When Toby asks to create review audio from show notes, do the explicit two-step pre-greenlight path: first create and verify `episodes/episode_0NN_transcript.md`, then run `python3 scripts/build_episode.py <N>`. Do not describe `build_episode.py` as if it turns show notes directly into audio, and do not wait on a silent transcript-agent handoff without checking that the transcript artifact exists.

If the transcript is missing, do not spawn nested OpenClaw CLI workers from a wrapper. That path caused silent timeouts on EP060. The valid action is artifact-producing: run `python3 scripts/generate_episode_transcript.py <N>`, verify `episodes/episode_0NN_transcript.md`, then run `python3 scripts/build_episode.py <N> --force-audio`. `scripts/attempt_review_audio.py` may now call that direct generator; it must not call `openclaw agent`.

**When Toby disapproves review audio and leaves a comment, revise with ONE command — do not hand-edit the transcript step by step in chat.** Running perl/sed edits and rebuilds as separate in-context steps balloons the agent context, forces repeated compaction, and triggers "Codex stopped before confirming the turn was complete" mid-fix. Instead run the single guarded subprocess:

```
python3 scripts/attempt_review_audio.py <N> --feedback "<Toby's exact audio comment>"
```

This regenerates the transcript to address the feedback (`generate_episode_transcript.py --force --feedback ...`, which auto-repairs any `check_episode.py` QC failure by feeding the failures back to the model, up to `TRANSCRIPT_GEN_ATTEMPTS` attempts), reruns transcript QC, rebuilds the EN audio with `build_episode.py --force-audio`, and posts the new review audio — all in one call, so almost nothing lives in the agent's context. Only fall back to manual steps if this subprocess itself fails and reports a concrete Build Log error.

Cover art generation uses OpenAI for the bespoke art module. `scripts/generate_episode_art.py` must call OpenAI Responses and write `scripts/episode_art/episode_0NN_art.py`; do not reintroduce `claude -p`, Claude CLI, or a nested agent for this step. The final cover still renders locally through Pillow into `images/episode_0NN_cover.png`.

### Post-greenlight (full release)
This is the operator-facing post-approval command. After Toby's actual review-audio approval, include the Discord message id for Toby's approving reply so the launcher can verify the approval before publishing:
```bash
python3 scripts/launch_approved_release.py <N> --audio-approved-by-toby --approval-message-id <toby_reply_message_id> --pub-date "Day, DD Mon YYYY HH:MM:SS +0000"
```
It detaches the approved release, starts a watchdog, and runs EN publish, translations, website/feed updates, the crossfire FLUX/Ken Burns video lane, localized burn-in video builds, YouTube uploads, CDN sync, and Discord in the right order. **Run this to completion — do not stop between phases.** Use `scripts/release_episode.py` only as the underlying phase library or for targeted recovery/debug work.

When Toby approves from Discord/ARIA, verify the approval reply from the review channel and run this launcher directly. Do not infer approval from a "fix it", "run the scripts", or "what is broken" message. Do not answer only by delegating artifact edits to Codex/MiniMax subagents; if a delegated build task already failed, inspect the episode state/logs, repair the artifact locally, then resume the release script from the appropriate step.

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

6a. **Release launcher approval evidence is mandatory.** `build_episode.py` records the reviewed EN audio hash and Discord review message, then sets `audio_approval.approved=false`. `launch_approved_release.py` and `release_episode_approved.py` refuse to publish feeds unless the same audio hash has approval recorded from a verified non-bot Discord reply after the review post. `--audio-approved-by-toby` must be paired with `--approval-message-id <toby_reply_message_id>`. Never infer approval from a request to debug, fix, or run scripts. (EP059 failure, 2026-05-29)

7. **If Toby sends a Discord voice note, transcribe it before answering.** Use:
   `python3 /Users/tobyglennpeters/.openclaw/workspace/scripts/utils/transcribe_audio.py "<audio_path>"`
   Never answer "Did you read my voice message?" from nearby text context alone.

8. **Do not claim GitHub Pages is disabled unless you verify it at the host level.**
   If a new episode URL fails, compare it with a known-good episode URL on the same `clawdassistant85-netizen.github.io/openclaw-podcast-audio` host first. If older episodes return 200, then Pages is enabled and the issue is path-specific, propagation, or file-level — not repo-level Pages being off.

9. **AgentStack Daily/OpenClaw Daily shorts are approved and active.** Toby re-approved shorts for this podcast on 2026-06-06. Do not say Toby turned them off. Do not add a manual review gate. The `youtube_shorts_pipeline.py --mode cron` runs daily at 09:30 ET via cron and stages 2 EN short candidates per episode plus translated shorts for ES/DE/PT/HI. After the episode is present in canonical `feed.xml`, `upload_agentstack_shorts.py --mode cron` uploads the built multilingual backlog automatically at 08:00, 14:00, and 20:00 ET on following days, continuing from EP058. If EN catch-up shorts were uploaded but translated channel shorts for the same episode are missing, catch up the missing translated shorts immediately before returning to the 3/day backlog cadence. Failures are reported to Discord `#build-log` (channel `1485243812442804327`). Do NOT re-disable the pipeline or add `SystemExit` guards without an explicit instruction from Toby. Full episode uploads and shorts staging run in separate processes to avoid resource contention.

10. **Podcast website deploy is release-blocking.** The DGX/gx website host should be reachable for every release. If website deploy cannot connect, hangs, times out, or the delegated website script fails, post a Discord `#build-log` failure and fail the release phase instead of continuing to YouTube/Discord as if the release completed.

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
- If OpenClaw, Hermes, Codex, or Claude Code has no new stable/verified release, do not turn that non-event into a listener-facing topic such as "stable watch", "watch lane", "stability check", or "beta watch". Keep no-release and prerelease bookkeeping in the `## Release Coverage Check` only; titles, taglines, Story Slate items, chapters, and show-notes prose should name things that actually changed.
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
- Current-news/actionability rule (locked 2026-05-22): if Toby rejects an episode as boring, stale, too technical, too fluffy, or not actionable, rebuild from fresh same-day/source-verified news and make each major story answer "what changed, what can I try now, and what should I avoid." Do not stretch one runtime/security story into a long lecture; increase story density and cut abstract connective tissue.
- EP056 correction persistence rule (locked 2026-05-22): future AgentStack Daily show notes for agent-stack cleanup requests must explicitly track OpenClaw, Codex, Claude Code, and Hermes when relevant, include `Technical depth angle`, `Actionability angle`, and `Listener hook` for every Story Slate item, and keep the spoken episode listenable with stakes, friction, and concrete try-now moves rather than a dry release recap.
- GitHub project meaning rule (locked 2026-05-25): when Toby asks for GitHub projects, treat that as a hot open-source repo/tool discovery lane around OpenClaw, Codex, Claude Code, Hermes Agent, MCP, local/self-hosted agents, codebase understanding, and model gateways. Do not fill it with GitHub-the-company product news, GitHub Projects boards, duplicate official release repos, or generic star-count trivia. Every repo item must include what it does, why it improves the stack, and a concrete `Try now:` use case.
- GitHub project evidence rule (locked 2026-06-02): when an AgentStack episode talks about GitHub-hosted projects, include current star counts or another concrete repository scale/velocity signal in the show notes and, where natural, in the spoken profile. Star counts are context, not the story, but omitting them makes the project lane feel under-specified.
- No empty-bookkeeping line rule (locked 2026-06-02): do not include listener-facing non-events such as "no todo list today." Empty categories, release gaps, and other bookkeeping belong only in internal checks, never in episode copy or audio.
- Release gap correction rule (locked 2026-05-25): do not let the no-back-to-back repeat rule suppress a newer or missed OpenClaw, Codex, Claude Code, or Hermes release. Always compare the latest upstream stable/verified version against the last relevant episode's detected version tags; if upstream is newer, include the release block even when the release timestamp predates the latest feed item.
- AI news plus project lane rule (locked 2026-05-26): when Toby asks for GitHub projects in an AgentStack episode, do not replace the broader AI-news slate with only repository picks, and do not fill the main episode with GitHub/Copilot product news unless it directly affects the stack. Build both lanes: source-verified AI/model/agent news plus GitHub-hosted projects that are relevant to OpenClaw, Codex, Claude Code, Hermes, MCP, local/self-hosted agents, model routing, and codebase understanding.
- Model discovery rule (locked 2026-06-01): every AgentStack Daily show-notes draft must include a `## Model Discovery Check` section, separate from release discovery, that checks primary/official sources for major new or materially updated AI models from MiniMax, Anthropic, OpenAI, Google/Gemini, xAI, Meta, Mistral, Qwen/Alibaba, DeepSeek, Z.ai/GLM, Kimi/Moonshot, NVIDIA, and other relevant labs. Major model drops, especially coding-agent, multimodal, long-context, local/self-hosted, and open-weight releases, are first-class story candidates and should outrank lower-impact repo/tool stories. For MiniMax M3 in EP061, cover the June 1, 2026 release, MSA sparse attention, 1M context, native multimodality, coding/agent benchmarks, MiniMax Code integration, API availability, and the stated technical-report/open-weights follow-up.
- Listener-experience rule (locked 2026-06-01): AgentStack Daily must not sound like homework. Do not repeat "run this test/check" language through every segment. For models such as MiniMax M3, prioritize new capabilities, how much of an improvement the release appears to be, what people are doing with it, online/real-world reactions, and caveats around vendor-run evidence. For OpenClaw releases, include observed breakage/regression/reaction signals because OpenClaw updates can disrupt workflows, but frame compatibility checks as risk context rather than a long assignment list.
- Structural surgery rule (locked 2026-06-01): when Toby rejects an episode for "do this, then do that" checklist pacing, rebuild the episode from the ground up instead of lightly editing phrases. Keep OpenClaw release coverage concise unless it is the explicit headline; do not let it occupy the first 20 minutes with operational tests before the main model/story. Move the most interesting model/capability story early and make the episode informational: what changed, how people use it, what it provides, real-world reactions, and only one or two high-level cautions.
- Spoken version-number rule (tightened 2026-05-27 after EP057 approval): transcripts must not read full patch notation aloud for release identifiers. Use a shortened spoken form once, then refer to "this release", "the update", or the product name. `0.133.0`, `2.1.149`, and similar full dot notation can stay in show notes/source links, but not in the spoken transcript.
- GitHub project showcase rule (tightened 2026-05-27 after EP057 approval): repo segments must feel like short profiles, not a rushed roundup. For each highlighted project, include popularity/velocity signals where available, what it does, which agents/tools it plugs into, concrete builder use cases, and at least one plausible workflow scenario. Star counts alone are not enough, but omitting scale/use-case/integration detail is also not enough.

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
