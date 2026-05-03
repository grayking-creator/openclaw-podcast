# EP044 — OpenClaw v2026.4.29, Active-Run Steering, People-Aware Memory, Model Provenance, and Account Security
**OpenClaw Daily** | May 1, 2026 | ~52–60 min

## Release Selection Verification
- Draft collision check: `show_notes_episode_044.md` did not exist when generation started.
- Current stable release selected for the public episode: `v2026.4.29`.
- Result: EP044 leads with OpenClaw `v2026.4.29`.

## Episode Title
**OpenClaw v2026.4.29, Active-Run Steering, People-Aware Memory, Model Provenance, and Account Security**

## Tagline
OpenClaw v2026.4.29 is an operator-control release: active-run steering becomes the default queue behavior, visible replies can be enforced through the message tool, follow-up commitments become opt-in heartbeat work, memory gains people-aware wiki metadata and provenance views, NVIDIA joins the provider catalog, startup diagnostics get sharper, and channel reliability tightens across Slack, Telegram, Discord, WhatsApp, Signal, Feishu, Matrix, Teams, and more. The back half covers Cisco’s Model Provenance Kit for AI supply-chain verification and OpenAI Advanced Account Security for phishing-resistant ChatGPT and Codex accounts.

## Feed Description
The episode starts with OpenClaw v2026.4.29. The release adds active-run steering defaults, visible-reply enforcement, spawned-subagent routing metadata, opt-in follow-up commitments, people-aware memory wiki metadata, per-conversation Active Memory filters, partial recall on timeout, a bounded REM preview RPC, NVIDIA provider onboarding and catalog metadata, Bedrock Opus 4.7 thinking parity, OpenGrep scan workflows, stricter restrictive-profile tool behavior, startup diagnostics, reusable model catalogs, stale-session recovery, runtime-dependency repairs, systemd loop prevention, and many channel fixes. After the release deep dive, the episode covers Cisco’s Model Provenance Kit as a practical model-lineage and AI supply-chain tool, then OpenAI Advanced Account Security as a concrete account-hardening bundle for ChatGPT and Codex users doing high-stakes agent work.

## Story Slate

### 1. **OpenClaw v2026.4.29 Makes Active Runs, Memory, Providers, Startup, Security, and Channels More Controllable**
OpenClaw v2026.4.29 is the valid release block for EP044 and should carry the front half of the episode. The release changes the operator surface for live conversations and automation: active-run queueing defaults to `steer`, `messages.visibleReplies` can force visible output through the message tool, inferred follow-up commitments become opt-in heartbeat work, subagent broadcasts expose `spawnedBy`, restrictive profiles stop being implicitly widened by configured `tools.exec` and `tools.fs`, memory gains people wiki metadata and provenance reports, NVIDIA becomes a bundled provider, and channel reliability fixes cluster around Slack Block Kit limits, Telegram proxy and polling behavior, Discord startup and rate limits, WhatsApp delivery/liveness, Signal streaming, Feishu empty-text handling, and Teams/Matrix edges. Technical depth angle: explain queue modes and model-boundary steering, visible-reply routing contracts, commitment extraction and heartbeat delivery, `commitments.enabled` / `commitments.maxPerDay`, per-agent/per-channel scoping, `allowedChatIds` / `deniedChatIds`, people wiki aliases/cards/relationship graphs/evidence drilldown, NVIDIA model-ref picker behavior, Bedrock Opus 4.7 thinking profiles, OpenGrep SARIF workflows, systemd `sysexits 78`, stale-session recovery, model-catalog stale refresh, and channel failure modes such as Slack Block Kit limits, Telegram long-polling timeouts, WhatsApp send acknowledgement, and Discord 429 cooldowns.

### 2. **Cisco Model Provenance Kit Turns Model Lineage into a Supply-Chain Check**
Cisco’s Model Provenance Kit is a strong security-infrastructure story because it treats AI model origin as something operators can test instead of something they only read from a model card or repository name. The kit is described as a Python toolkit and CLI with compare and scan modes that analyze architecture metadata, tokenizer structure, and weight-level signals such as embedding geometry, normalization layers, energy profiles, and direct weight comparisons, with an initial fingerprint database covering roughly 150 base models across 45-plus families and 20-plus publishers. Technical depth angle: explain model fingerprinting, compare versus scan workflows, composite lineage scores, metadata spoofing risk, tokenizer and weight-level evidence, known-fingerprint databases, derivation relationships from the Model Provenance Constitution, and how model provenance fits into AI supply-chain policy, licensing review, vulnerability response, and deployment gates.

### 3. **OpenAI Advanced Account Security Hardens ChatGPT and Codex as Agent Work Becomes Sensitive**
OpenAI’s April 30 Advanced Account Security release is worth covering because ChatGPT and Codex accounts increasingly hold connected tools, code work, personal context, and sensitive business information. The opt-in mode requires passkeys or physical security keys, disables password login, disables email and SMS recovery, uses backup passkeys/security keys/recovery keys, shortens sessions, adds login alerts and session management, automatically excludes conversations from model training, and will be required for individual Trusted Access for Cyber users accessing the most capable and permissive cyber models beginning June 1, 2026. Technical depth angle: explain phishing-resistant authentication, account-recovery tradeoffs, passkeys versus passwords, hardware security keys, session lifetime reduction, active-session review, Codex account coverage, automatic training exclusion, and the operational tradeoff between stronger takeover resistance and stricter recovery responsibility.

## Show Notes
```md
OPENCLAW DAILY — EPISODE 044 — May 1, 2026

[00:00] INTRO / HOOK
OpenClaw v2026.4.29 leads the episode because it changes concrete operator behavior immediately: active-run steering, visible-reply routing, heartbeat-backed commitments, people-aware memory, model catalog behavior, stricter tool profiles, startup recovery, and channel reliability.

This release changes a lot of operational behavior. Active-run queueing now defaults to steering instead of one-at-a-time legacy queuing. Visible replies can be enforced through the message tool. Follow-up commitments become opt-in heartbeat work with extraction and delivery limits. Subagent events carry routing metadata. Memory gains people-aware wiki metadata, provenance views, per-conversation Active Memory filters, partial recall on timeout, and bounded REM preview diagnostics. Provider coverage expands through NVIDIA onboarding, faster manifest-backed model and auth paths, Bedrock Opus 4.7 thinking parity, and safer Codex/OpenAI-compatible replay behavior. Security and operations add stricter restrictive-profile tool handling, OpenGrep scanning, sharper GHSA triage policy, safer owner-scope handling, Docker onboarding automation, and web-fetch IPv6 ULA opt-in for trusted proxy stacks.

The fix list is also very operational: slow-host startup, reusable model catalogs, event-loop readiness diagnostics, runtime-dependency repair, stale-session recovery, version-scoped update caches, Slack Block Kit limits, Telegram proxy and polling resilience, Discord startup/rate-limit behavior, WhatsApp delivery and liveness, Signal media and receive streams, Feishu empty-message handling, Matrix and Teams edges, and systemd restart-loop prevention.

After the release deep dive, the episode covers two security stories with primary technical surfaces: Cisco’s Model Provenance Kit for model-lineage checks, and OpenAI Advanced Account Security for phishing-resistant ChatGPT and Codex account protection.

[02:30] STORY 1 — OpenClaw v2026.4.29 Makes Active Runs, Memory, Providers, Startup, Security, and Channels More Controllable
Start with active-run behavior, because this is where the release changes day-to-day agent interaction.

OpenClaw now defaults active-run queueing to `steer`, with a 500ms follow-up fallback debounce. The older one-at-a-time behavior stays available as `queue`. The difference matters. In a long-running agent turn, a user may send follow-up instructions while the model is still working. A queue mode that simply stacks messages can make the next turn lag behind the current state. Steering is different: pending Pi steering messages drain at the next model boundary, so the agent can incorporate accepted follow-ups at the point where it can safely change course.

The operational question is not just “can a user send another message?” It is “when does that message become part of the agent’s plan?” Steering makes the boundary explicit. The runtime can accept follow-ups, debounce them, and apply them at a safe model boundary instead of interrupting arbitrary tool execution or losing the message after app-server cleanup. The release also flushes accepted debounced Codex steering messages before normal app-server turn cleanup, so an acknowledged follow-up does not disappear if the turn completes quickly.

Visible-reply enforcement is another important messaging control. The new global `messages.visibleReplies` setting lets operators require visible output to go through `message(action=send)` for any source chat, while `messages.groupChat.visibleReplies` remains available as a group or channel override. That is a routing contract. If the system says a reply must be visible through the channel message tool, the agent should not quietly finish a turn without producing a user-visible response. The related fix for group chats falls back to automatic source delivery when a channel precomputes message-tool-only replies but the message tool is unavailable. That prevents Discord or Slack-style group turns from silently completing with no visible reply.

Subagent routing metadata also improves. Gateway events now surface `spawnedBy` on subagent chat and agent broadcast payloads. That gives clients enough information to route child-session events without doing a separate session lookup. In a multi-agent UI or chat integration, this matters because child work should remain attached to the parent request, especially when spawned sessions are doing background tasks, delegated research, or tool-heavy work.

Then there are inferred follow-up commitments. The release adds opt-in commitments with hidden batched extraction, per-agent and per-channel scoping, heartbeat delivery, CLI management, `commitments.enabled`, `commitments.maxPerDay`, and heartbeat-interval due-time clamping so reminders do not fire immediately in a magical way. This is the right cautious shape. Automated follow-up is useful, but it can become creepy or noisy if every vague future phrase turns into a reminder. Scoping, extraction limits, delivery through heartbeat, and per-day caps let operators make it deliberate.

The practical guidance is to enable commitments only where the channel and agent role justify it. A personal assistant may benefit from a bounded “check back later” capability. A public group bot probably should not infer reminders from casual conversation. The config needs to reflect channel norms, agent role, and delivery risk.

[12:00] STORY 1B — Memory Becomes More People-Aware, More Filtered, and More Inspectable
Memory is the second major release area. OpenClaw adds agent-facing people wiki metadata, canonical aliases, person cards, relationship graphs, privacy and provenance reports, evidence-kind drilldown, and search modes for person lookup, question routing, source evidence, and raw claims.

That is a meaningful step beyond generic recall. People memory is not just another document index. A person can have aliases, relationships, preferences, roles, privacy constraints, and evidence with different reliability. If an agent recalls “Alex said X,” the operator needs to know which Alex, which source, which conversation, which claim, and whether the evidence is strong enough to use. Person cards and relationship graphs give agents a structured way to reason about identity and context without flattening everything into one text blob.

The provenance view is especially important. Memory systems fail when they make old, weak, or misattributed facts sound certain. Evidence-kind drilldown lets the system separate raw claims, source evidence, generated related links, and readable body snippets. The release also keeps broad shared-source and generated related-link blocks from turning every page into a search hit, caps noisy backlinks, supports all-term searches such as people-routing queries, and prefers readable page body snippets over generated metadata.

Active Memory gets sharper filters too. Optional per-conversation `allowedChatIds` and `deniedChatIds` let operators enable recall only for selected direct, group, or channel conversations while keeping broad sessions skipped. That is a privacy and relevance feature. A workspace may want recall in a private operations chat but not in a noisy public channel. Without filters, recall can become overbroad even when the underlying memory system is technically working.

Timeout behavior improves as well. Active Memory can return bounded partial recall summaries when the hidden memory sub-agent times out, including the default temporary-transcript path, so useful recovered context is not discarded. That is the right reliability tradeoff: a timed-out recall should not necessarily become zero recall if a safe partial summary is available. Operators need bounded output and clear diagnostics rather than all-or-nothing behavior.

There is also a read-only `doctor.memory.remHarness` RPC for bounded REM dreaming previews without mutation paths. This gives operator clients a way to inspect what the memory dreaming machinery would produce without actually promoting or changing memory. For memory systems, preview and mutation should be separate. Debugging a memory pipeline should not accidentally rewrite the memory store.

[20:00] STORY 1C — Providers, Model Catalogs, Startup Diagnostics, and Runtime Deps Get More Predictable
Provider and model coverage expands with NVIDIA onboarding and static catalog metadata. The NVIDIA provider includes API-key onboarding, setup docs, static catalog rows, and literal model-ref picker support so hosted NVIDIA models can be selected with their provider prefix intact. The release also persists the `NVIDIA_API_KEY` provider marker and marks bundled NVIDIA Chat Completions models as string-content compatible so NIM models load from `models.json` and OpenAI-compatible subagent calls send plain text content.

The operational point is provider identity. If a model ref needs to keep its provider prefix, the picker should not normalize it away into an ambiguous string. If the provider has a marker key, onboarding and catalog behavior should remember that. If a compatible endpoint expects plain text content for subagent calls, the runtime should shape the request accordingly. These details are small individually, but they determine whether a provider works reliably in real agent flows.

Bedrock support gets thinking-profile parity for Claude Opus 4.7. The release exposes `xhigh`, `adaptive`, and `max` thinking profiles for Bedrock model refs while keeping Opus and Sonnet 4.6 on adaptive-by-default. It also omits deprecated `temperature` for Opus 4.7 Bedrock model IDs, named profiles, and application inference profiles, and classifies nested validation responses for failover. That is another example of provider-specific correctness. The same model family can have different transport rules depending on whether it is called directly or through Bedrock.

Model catalog reliability improves too. Gateway models can serve the last successful model catalog while stale reloads refresh in the background. That prevents control-plane and OpenAI-compatible requests from blocking behind model-provider rediscovery after model config changes. On slow hosts, this is a big usability improvement: the catalog may be stale for a moment, but the Gateway does not stop answering while it reloads everything.

Startup diagnostics become more explicit. Gateway diagnostics can emit an opt-in startup timeline that records lifecycle and plugin-load phases behind a config flag, so slow-start diagnosis no longer requires bespoke instrumentation. That gives operators a way to answer: where did boot time go? Was it config validation, plugin metadata, provider discovery, channel startup, runtime dependency repair, or event-loop readiness?

Runtime dependency repair gets a long pass. The release replaces stale symlinked mirror target roots before writing runtime-mirror temp files, skips rewriting already materialized hardlinks, writes dependency maps even when plans are empty, verifies staged package entry files before reusing mirrored roots, prefers `require` conditional exports for CommonJS-only plugin deps, scopes packaged Node compile caches by OpenClaw version and install metadata, and prunes stale `openclaw-unknown-*` roots during Gateway startup while preserving recent or locked roots. The builder takeaway: packaged plugin deps are an operating system inside the operating system. They need locks, version scoping, repair, and safe replacement semantics.

[29:00] STORY 1D — Security and Channel Fixes Narrow Real Failure Modes
Security/tools is one of the most important behavior changes in v2026.4.29: configured `tools.exec` and `tools.fs` sections no longer implicitly widen restrictive profiles such as `messaging` and `minimal`. If users need those tools under a restrictive profile, they must add explicit `alsoAllow` entries, and startup warns about affected configs.

That is a cleaner security boundary. A restrictive profile should mean restrictive. If a config section for exec or filesystem tools silently widens the profile, operators may think an agent is running with a narrow surface while it can actually do more. Requiring `alsoAllow` makes the expansion intentional and auditable.

OpenGrep scanning is added with a precise rulepack, source-rule compiler, provenance metadata checks, and PR/full scan workflows that validate first-party code and rulepack-only changes while uploading SARIF to GitHub Code Scanning. This is useful because security automation should be reproducible. A rulepack needs provenance, a compiler path, validation, CI workflows, and a standard output format such as SARIF so findings land where maintainers already triage code security.

Gateway/systemd behavior gets a concrete operational fix: supervised lock and `EADDRINUSE` conflicts now exit with sysexits 78, so `RestartPreventExitStatus=78` stops `Restart=always` loops instead of repeatedly reloading plugins against an occupied port. That is a classic service-management failure mode. If another Gateway already owns the port, endlessly restarting the service does not fix the conflict; it burns CPU, churns logs, and can repeatedly load plugins into a bad state. A deterministic exit code lets the service manager stop trying.

Stale-session recovery is also more conservative. OpenClaw can release stale session lanes while active embedded runs, reply operations, and lane tasks remain serialized, so queued follow-ups can drain without aborting legitimate long-running work. Doctor and task maintenance can reconcile orphaned subagents with persisted recovery attempts and wedged-session tombstones. The product goal is to recover from stale bookkeeping without treating every long task as stuck.

Channel fixes are extensive. Slack gets a large Block Kit pass: native command argument menus stay within option limits, fallback button labels and values are truncated or dropped when necessary, confirmation text is capped to dialog limits, approval metadata and update fallback text stay within Slack limits, message-tool presentation and interactive blocks are merged, and fallback text is capped for sends and edits. The practical failure mode is simple: one oversized button value or fallback string can make Slack reject the whole block payload. The release makes the adapter preserve valid interactive structure while clipping invalid pieces.

Telegram fixes focus on proxy behavior, polling, webhooks, quotes, and safe sends. Telegram honors `ALL_PROXY`, `all_proxy`, and service-level `OPENCLAW_PROXY_URL` for HTTP/1 Bot API transport. Long-polling timeouts are clamped so low configured values do not force fresh HTTPS connections every few seconds. Polling liveness warnings surface in channel status and doctor. Webhook runtime state warns when registration has not completed. Quote replies retry without stale or invalid quote excerpts. Safe-send retry avoids duplicate visible messages on ambiguous network envelopes. The pattern is bounded resilience: keep transient network failures from killing the Gateway, but do not blindly duplicate user-visible replies.

Discord fixes cover startup and rate-limit handling, thread-bound ACP resolution, long CJK chunking, duplicate gateway monitor suppression, channel health summaries, startup closed behavior when bot identity cannot be resolved, bounded WebSocket handshakes, and cooldowns for Cloudflare/Error 1015 HTML 429 responses using `Retry-After` when available. WhatsApp fixes require real Baileys outbound message IDs before marking auto-replies delivered, expose liveness and timeout settings, recover listeners after certain reconnect stalls, and log dispatcher delivery failures with enough identifiers to debug typing-without-send reports. Signal fixes include group allowlist matching, installer download caps, media response caps, and long-lived receive SSE behavior. Feishu skips empty-text messages that carry no media so blank user turns are not written into sessions.

The release verdict: v2026.4.29 is about making live agent systems more controllable. It narrows ambiguous queue behavior, visible reply delivery, follow-up automation, memory provenance, provider catalogs, startup diagnostics, restrictive tool profiles, stale sessions, service restart loops, and channel adapter failure modes.

[39:00] STORY 2 — Cisco Model Provenance Kit Turns Model Lineage into a Supply-Chain Check
Cisco’s Model Provenance Kit is a strong AI infrastructure story because it addresses a basic question that is getting harder to answer: where did this model actually come from?

Model cards, repository names, and metadata are useful, but they are not enough by themselves. Models are fine-tuned, merged, quantized, distilled, converted, renamed, repackaged, and redistributed. A downstream team may receive a checkpoint that claims to be derived from one family, but the actual weights, tokenizer, or architecture may tell a more complicated story. That matters for licensing, vulnerability response, safety review, benchmark interpretation, and deployment policy.

The kit is described as a Python toolkit and CLI with compare and scan workflows. Compare mode takes two models, including Hugging Face or local checkpoints, and breaks down similarity across architecture metadata, tokenizer structure, and weight-level signals. Scan mode starts with one model and matches it against a database of known fingerprints to identify closest lineage candidates.

The technical detail is that the kit is not only looking at names. It analyzes signals such as embedding geometry, normalization layers, energy profiles, direct weight comparisons, tokenizer structure, and architecture metadata. Those signals matter because metadata can be spoofed or stripped. Weight-level evidence is harder to fake if the goal is to hide model origin while preserving model behavior.

The initial fingerprint database is reported to cover roughly 150 base models across more than 45 model families and more than 20 publishers. That database is important because provenance is comparative. A fingerprint is most useful when it can be matched against known references. Without a reference set, a tool can say two models are similar, but it has less ability to place a model in a broader lineage graph.

Cisco also published a Model Provenance Constitution that defines derivation relationships such as direct descent, indirect descent, mechanical transformation, identity, and transitivity. That is useful because lineage needs a vocabulary. Fine-tuning, quantization, format conversion, and merging are not the same relationship. A deployment policy may allow one and reject another.

For operators, the practical place to use a tool like this is in the model intake pipeline. Before a model is approved for production, scan it. Compare it with the claimed base family. Store the fingerprint result with the model artifact. Tie that evidence to licensing review, security review, benchmark results, and deployment gates. If a vulnerability or policy issue later affects a base family, provenance evidence helps identify which deployed models might be downstream.

There are limitations. Fingerprinting is evidence, not a magic certificate. A high similarity score needs interpretation. Fine-tunes, merges, pruning, quantization, and format conversion can change signals in different ways. A fingerprint database can be incomplete. Proprietary models may not be available as references. But the direction is right: model origin should become testable operational evidence, not only a label.

The OpenClaw-relevant takeaway is that agent runtimes increasingly depend on model supply chains. If an agent can choose local models, hosted models, fine-tuned models, marketplace models, and converted checkpoints, the operator needs a way to ask not only “does it run?” but also “what is it derived from, what policy applies, and what risk follows it?”

[47:00] STORY 3 — OpenAI Advanced Account Security Hardens ChatGPT and Codex as Agent Work Becomes Sensitive
OpenAI’s Advanced Account Security release is not a model release, but it is a serious agent-operations story because ChatGPT and Codex accounts now sit close to sensitive context, code, connected tools, and high-stakes workflows.

The opt-in mode bundles several protections. It requires passkeys or physical security keys and disables password-based login. That makes phishing-resistant authentication the default for enrolled accounts. A stolen password should not be enough to get in because there is no password login path to use.

Account recovery changes are just as important. Advanced Account Security disables email and SMS recovery and requires stronger recovery methods: backup passkeys, security keys, and recovery keys. This is a deliberate tradeoff. Email and SMS recovery are convenient, but if an attacker controls the email account or phone number, those recovery paths become account-takeover paths. Stronger recovery reduces that risk, but it also means OpenAI Support will not be able to recover enrolled accounts if the user loses the required recovery methods.

Sessions become shorter to reduce exposure if a device or active session is compromised. Users receive login alerts and can review and manage active sessions across devices. That matters because long-lived sessions are a real risk when an account contains connected tools, code work, memory, or sensitive conversations. A shorter session window and clearer session list do not eliminate compromise, but they reduce dwell time and improve detection.

Automatic training exclusion is included too. Conversations from enrolled accounts are not used to train OpenAI models. For high-risk users and sensitive work, that removes one account-level privacy decision from the user’s daily workflow. The account mode carries the data-use preference automatically.

The Codex detail matters for builders. OpenAI says protection applies to Codex as well when accessed through the same login. That means the security setting covers not only chat conversations but also coding-agent workflows. Codex may touch repositories, diffs, terminal output, issue context, and connected development work. If an account is compromised, the risk is not just someone reading chats; it can become access to engineering context and agentic workflows.

OpenAI also says individual members of Trusted Access for Cyber who access the most capable and permissive cyber models will be required to enable Advanced Account Security beginning June 1, 2026. Organizations with trusted access can alternatively attest that phishing-resistant authentication is part of their single sign-on workflow. That is a strong signal about where account security is going for high-capability AI access: stronger models and more permissive tools require stronger account protection.

For operators and builders, the practical lesson is to match account security to capability. If an AI account can use Codex, connect tools, hold sensitive context, or access advanced cyber models, password-plus-email recovery is not enough. Use phishing-resistant auth. Maintain backup keys. Store recovery keys safely. Review active sessions. Shorten session exposure. And understand the recovery cost before enabling stricter protections.

The best security setting is the one the user can actually sustain. Advanced Account Security raises the floor, but it also raises the responsibility for recovery hygiene. The deployment recommendation is to document key enrollment, backup key storage, recovery-key handling, device replacement, and offboarding before requiring it across a team.

[54:00] OUTRO
The release lead is OpenClaw v2026.4.29 because it moves concrete operator surfaces: active-run steering, visible-reply routing, follow-up commitments, subagent routing metadata, people-aware memory, per-conversation recall filters, partial recall, NVIDIA provider onboarding, Bedrock thinking profiles, startup diagnostics, model-catalog refresh behavior, restrictive-profile tool boundaries, OpenGrep workflows, systemd restart-loop prevention, stale-session recovery, and channel adapter reliability.

Cisco’s Model Provenance Kit is the model-supply-chain story: compare models, scan against known fingerprints, inspect metadata, tokenizer, and weight-level evidence, and turn lineage into a deployment check.

OpenAI Advanced Account Security is the account-hardening story: passkeys and security keys, no password login, stronger recovery, shorter sessions, login alerts, active-session review, automatic training exclusion, Codex coverage, and stricter requirements for high-capability cyber access.

The practical takeaway: live agent systems need explicit control boundaries. Queueing, memory, providers, channels, models, and accounts all need surfaces operators can inspect, configure, and recover.
```

## Verified Links
- OpenClaw — Release `v2026.4.29`: https://github.com/openclaw/openclaw/releases/tag/v2026.4.29
- OpenClaw — Release API for `v2026.4.29`: https://api.github.com/repos/openclaw/openclaw/releases/tags/v2026.4.29
- Cisco — Model Provenance Kit: https://blogs.cisco.com/ai/model-provenance-kit
- Cisco — Model Provenance Constitution: https://blogs.cisco.com/ai/model-provenance-constitution
- OpenAI — Introducing Advanced Account Security: https://openai.com/index/advanced-account-security/
- OpenAI — Cybersecurity Action Plan PDF: https://cdn.openai.com/pdf/7ca95dce-4424-4b62-9eab-89233bb38f82/oai-cybersecurity-action-plan.pdf

## Chapters
- **[00:00] Hook — OpenClaw v2026.4.29 Leads EP044**
- **[02:30] OpenClaw v2026.4.29 Makes Active Runs, Memory, Providers, Startup, Security, and Channels More Controllable**
- **[12:00] Memory Becomes More People-Aware, More Filtered, and More Inspectable**
- **[20:00] Providers, Model Catalogs, Startup Diagnostics, and Runtime Deps Get More Predictable**
- **[29:00] Security and Channel Fixes Narrow Real Failure Modes**
- **[39:00] Cisco Model Provenance Kit Turns Model Lineage into a Supply-Chain Check**
- **[47:00] OpenAI Advanced Account Security Hardens ChatGPT and Codex as Agent Work Becomes Sensitive**
- **[54:00] Outro**
