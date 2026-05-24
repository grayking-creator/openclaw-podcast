# AgentStack Daily EP056 - OpenClaw, Codex, Claude Code, Hermes, Appshots, MCP Tunnels, and Agent News

## Release Coverage Check

- **OpenClaw** - Latest stable/verified release: `v2026.5.20` from `https://api.github.com/repos/openclaw/openclaw/releases?per_page=10` with prereleases skipped. Selected missing version: `v2026.5.20`.
- **OpenAI Codex app/CLI** - Latest stable/verified release: `rust-v0.133.0` from `https://api.github.com/repos/openai/codex/releases?per_page=10`; current product updates verified from OpenAI ChatGPT/Codex release notes.
- **Claude Code CLI** - Latest verified npm package version: `2.1.148` from `npm view @anthropic-ai/claude-code version dist-tags time --json`; concrete changes verified in Anthropic's Claude Code changelog.
- **Hermes Agent** - Latest stable/verified release: `v2026.5.16` / `v0.14.0` from `https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=10`.

## Episode Title

OpenClaw, Codex, Claude Code, Hermes, Appshots, MCP Tunnels, and Agent News

## Tagline

A denser and livelier EP056: upgrade the local agent stack, make Hermes useful with Codex and Claude workflows, capture visual bugs with Appshots, expose private tools through scoped MCP tunnels, migrate Gemini CLI work before the Antigravity cutoff, and leave with things to test today.

## Feed Description

AgentStack Daily EP056 opens with the release work that matters now: OpenClaw v2026.5.20 adds policy checks, safer secret-file handling, provider routing, cron and subagent recovery, voice context, and image-generation timeout fixes; Codex rust-v0.133.0 adds goals, remote-control readiness, permission-profile APIs, plugin discovery, and lifecycle hooks; Claude Code 2.1.148 follows a larger 2.1.147 update with pinned background sessions, code review, MCP pagination, enterprise policy enforcement, Windows behavior fixes, background approvals, and a Bash regression fix; Hermes Agent v0.14.0 adds the PyPI install path, a local OpenAI-compatible proxy for OAuth providers, SuperGrok auth, X search, Teams, lighter lazy installs, faster startup, browser speedups, handoff, LSP diagnostics, video generation, wider computer use, and more messaging surfaces. Then the episode moves through Codex Appshots, Secure MCP tunnels, Google Agent Executor, GKE Agent Sandbox and Agent Substrate, the Antigravity CLI migration, Microsoft MagenticLite, Google Data Agent Kit, Gemini API-key hardening, and Copilot Auto plus semantic issue search. Runtime target: 50 minutes.

## Story Slate

1. **OpenClaw Codex Claude Code upgrade path makes the local agent stack inspectable**
   OpenClaw v2026.5.20 changes the host layer: bundled Policy plugin, channel conformance checks, doctor lint findings, per-agent lean local-model mode, xAI device-code OAuth, OpenRouter provider routing policy, fail-closed symlink secret loading, cron final-output delivery, subagent completion handoff recovery, Discord voice follow behavior, bounded realtime voice identity context, and a longer image-generation watchdog. Codex rust-v0.133.0 adds default goals, dedicated goal storage, remote-control readiness, permission-profile APIs, marketplace-aware plugin discovery, and lifecycle extension events. Claude Code 2.1.147 and 2.1.148 improve pinned background sessions, code review, updater diagnostics, enterprise login policy, MCP pagination, Windows and PowerShell behavior, background permission reuse, and Bash exit-code handling.
   Technical depth angle: explain the exact surfaces to verify after upgrading: `doctor`, policy findings, secret symlink rejection, provider routing, cron final replies, subagent completion, Codex goals, remote-control readiness, permission profile listing, plugin inventory, lifecycle hooks, MCP pagination, pinned Claude sessions, and code review on a real diff.
   Actionability angle: run one tiny cross-stack smoke test: OpenClaw starts or schedules the task, Codex edits or inspects with a goal, Claude Code reviews or validates, and the result is checked through logs or diagnostics.
   Listener hook: this is the "stop guessing which agent broke" segment; every changed surface gets a named test so the stack feels less haunted and more debuggable.
   Primary links: https://github.com/openclaw/openclaw/releases/tag/v2026.5.20, https://github.com/openai/codex/releases/tag/rust-v0.133.0, https://docs.anthropic.com/en/release-notes/claude-code

2. **Hermes Agent Foundation release turns subscriptions, local tools, and messaging into a sharper agent bench**
   Hermes Agent v0.14.0 is the practical Hermes block: `pip install hermes-agent`, a local OpenAI-compatible proxy for OAuth-backed Claude Pro, ChatGPT Pro, and SuperGrok providers, xAI SuperGrok OAuth, `x_search`, Microsoft Teams, lazy dependency installs, a faster launch path, browser-console acceleration, LINE and SimpleX Chat, live `/handoff`, platform-native clarify buttons, Discord history backfill, direct pixel vision, per-turn file mutation verification, LSP semantic diagnostics, pluggable `video_generate`, non-Anthropic computer-use backend support, Zed ACP Registry integration, OpenRouter Pareto Code routing, optional skills, API approval events, and plugin-side `ctx.llm` calls.
   Technical depth angle: map Hermes as a local agent bench: provider auth, local proxy, API shape, browser CDP performance, messaging adapters, approval events, LSP checks, file mutation footer, and computer-use backend boundaries.
   Actionability angle: install or update Hermes, run `hermes doctor`, start `hermes proxy`, point one OpenAI-compatible tool at it, test one browser inspection, one LSP-backed write, one `/handoff`, and one messaging clarification flow.
   Listener hook: Hermes is the messy toolbox segment, but in a good way: the fun is finding which two features remove an annoyance this week.
   Primary link: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.16

3. **OpenAI Codex Appshots and goal mode make visual product work less guessy**
   OpenAI's May 21 Codex update adds Appshots in the macOS app, goal mode across the app/IDE/CLI, browser annotations, faster asset extraction, read-only JavaScript context, cleaner tab grouping, and locked computer use for eligible Mac Computer Use users. The valuable shift is practical context capture: a UI bug can arrive with pixels, available text, and a durable goal instead of only a vague written complaint.
   Technical depth angle: explain Appshots as screenshot plus text context, goal mode as a durable task target, annotations as spatial feedback, read-only JavaScript as safer inspection, and locked computer use as supervised continuity.
   Actionability angle: pick one visible UI bug, capture an Appshot, write a narrow goal, patch the smallest relevant surface, run the page, and capture a second state before accepting the result.
   Listener hook: this is the "stop describing a broken layout like a witness sketch" segment.
   Primary link: https://help.openai.com/en/articles/6825453-chatgpt-release-notes

4. **Secure MCP tunnels turn private tools into reachable agent tools without opening inbound ports**
   OpenAI and Anthropic both moved MCP tunnel patterns forward in May. The practical idea is simple: an internal MCP server can be reached from an agent surface through an outbound tunnel, instead of exposing a public inbound service. The caveat is just as important: a tunnel is not a permission model; identity, tool authorization, local server trust, auditing, and secret handling still matter.
   Technical depth angle: compare outbound-only tunnel setup, local MCP auth, account/project binding, audit logs, tool allowlists, and the failure mode where a reachable private tool becomes too broadly authorized.
   Actionability angle: design one read-only private MCP tool first, name the allowed methods, log every call, and add mutating actions only after approval gates and audit behavior are boringly predictable.
   Listener hook: this is the segment where "it connects" stops being the finish line and becomes the first security question.
   Primary links: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels, https://docs.anthropic.com/en/docs/agents-and-tools/mcp-tunnels

5. **Google Agent Executor makes long-running agents resumable instead of one-shot**
   Google's Agent Executor release is about durable execution. It names the runtime pieces serious agents need: event logs, snapshots, reconnect and backfill, isolated actors, single-writer session state, and trajectory branching. This is useful because agent runs are increasingly long-lived systems, not single prompt-response calls.
   Technical depth angle: explain what an event log records, when snapshots matter, why reconnect/backfill is product behavior, how branchable trajectories help debugging, and why durable state should live below the model prompt.
   Actionability angle: take one flaky long-running task and write its event sequence: start, tool call, approval, failure, retry, resume, and success.
   Listener hook: the entertaining bit is brutally practical: if your agent cannot resume, it is one network blink away from improv.
   Primary links: https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime, https://github.com/google/ax

6. **GKE Agent Sandbox and Agent Substrate target the awkward shape of idle but stateful agents**
   Google pushed GKE Agent Sandbox to general availability and introduced Agent Substrate patterns for high-density agent sessions. The workload shape is specific: many sessions are isolated, mostly idle, then need to wake quickly with state intact. Warm pools, snapshots, gVisor isolation, actor scheduling, and worker multiplexing are the operational pieces.
   Technical depth angle: explain why normal container scheduling struggles with many idle agent sessions, how warm pools and snapshots change activation time, and what to test before putting coding agents, MCP servers, or browser workers into this kind of substrate.
   Actionability angle: sketch one agent service by active sessions, idle sessions, wake latency, retained state, allowed tools, isolation level, and debugging evidence.
   Listener hook: this is infrastructure with a punchline: paying for idle agents is painful, but waking cold agents is painful too.
   Primary links: https://cloud.google.com/blog/products/containers-kubernetes/bringing-you-agent-sandbox-on-gke-and-agent-substrate, https://github.com/agent-substrate/substrate

7. **Google Antigravity CLI migration gives Gemini CLI users a real deadline**
   Google says Gemini CLI consumer/free usage stops serving requests on June 18, 2026, and Antigravity CLI becomes the new terminal surface. The migration matters because Antigravity is positioned around a shared multi-agent harness: skills, hooks, subagents, plugins, async work, and shared context across CLI and desktop.
   Technical depth angle: explain the migration decision tree: consumer versus enterprise usage, token/auth changes, config migration, skill compatibility, hook behavior, subagent patterns, and how to test an existing Gemini CLI task before the cutoff.
   Actionability angle: inventory the Gemini CLI tasks that run weekly, move the highest-value one to Antigravity now, and compare tools used, approvals requested, files changed, and success output.
   Listener hook: deadline stories are only boring until a terminal command goes quiet on the morning you need it.
   Primary links: https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/, https://cloud.google.com/blog/topics/developers-practitioners/io26-news-for-agent-developers-on-google-cloud

8. **Microsoft MagenticLite shows small-model computer use can work when the harness is designed around it**
   Microsoft Foundry Labs released MagenticLite, MagenticBrain, and Fara1.5. The point is not only model size; it is co-design. MagenticBrain is trained inside the same harness where it runs, Fara1.5 handles computer-use tasks, browser/code work can run in Quicksand's QEMU sandbox, and critical actions pause for approval.
   Technical depth angle: explain harness-faithful training, tool schema parity, browser-model delegation, sandbox boundaries, human takeover, approval gates, and which daily tasks are plausible for a smaller orchestrator.
   Actionability angle: try one bounded computer-use task with obvious success and low consequence: gather facts from a known dashboard, fill a draft form without submitting, or prepare a local report inside a sandbox.
   Listener hook: this is the "cheap and cheerful, but only if caged properly" segment.
   Primary links: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/whats-new-in-microsoft-foundry-labs-%E2%80%93-may-2026/4520310, https://labs.ai.azure.com/projects/magenticlite/, https://github.com/microsoft/magentic-ui

9. **Google Data Agent Kit packages data access as configured agent tools instead of pasted schema**
   Google Data Agent Kit brings data skills and MCP-style tools into developer-agent surfaces including Codex, Claude Code, Gemini CLI, VS Code, and Antigravity. The useful shift is that data context can become configured, scoped tool access rather than copied schema and credentials in a prompt.
   Technical depth angle: explain BigQuery, AlloyDB, Spanner, and Cloud Storage connectors; query optimization and validation skills; drift and governance checks; context-window cost; and access-scope risk.
   Actionability angle: build one read-only data-agent path with a single dataset, one question type, query validation, cost estimate, and a clear rule for summaries versus raw rows.
   Listener hook: this is the segment where a data agent can save time or burn budget, depending on whether you scope it first.
   Primary link: https://cloud.google.com/blog/products/data-analytics/data-agent-kit-brings-data-skills-and-tools-to-your-ide-or-cli

10. **Gemini API-key guidance gives agent builders a security task they can finish today**
    Google reminds developers that Gemini API keys are standard Google API keys and should be treated as open secrets. The concrete path is standalone projects, API restrictions, application restrictions, Secret Manager for server-side keys, traffic monitoring by credential ID, and rotation when keys spread.
    Technical depth angle: explain API restrictions versus application restrictions, one key per application shape, browser-client risk, Secret Manager injection, `credential_id` monitoring, and why generated apps should not call paid model APIs directly from exposed clients.
    Actionability angle: pick one Gemini key and verify project isolation, API restriction, application restriction, storage location, usage metric, and rotation path.
    Listener hook: this is the rare security segment that can be fixed before lunch.
    Primary link: https://cloud.google.com/blog/topics/developers-practitioners/api-keys-are-open-secrets

11. **GitHub Copilot Auto and semantic issue search make planning and model routing part of coding work**
    GitHub Copilot Auto now routes based on task signals while respecting admin policy and showing the selected model. Copilot Chat also adds semantic issue search, so developers can ask for related issues by meaning rather than only exact labels or text. The useful move is to triage before editing and log the model when reproducibility matters.
    Technical depth angle: explain task-aware routing, admin policy, model visibility, reproducibility risk, semantic issue clustering, and a practical order: search related issues, group failure modes, then hand the narrowed task to the coding agent.
    Actionability angle: before the next bug fix, ask Copilot for related issues by symptom and platform, cluster the results, choose one failure mode, and only then ask an agent to patch.
    Listener hook: this is how to stop asking a coding agent to solve a mystery with half the clues missing.
    Primary links: https://github.blog/changelog/2026-05-20-auto-model-selection-now-routes-based-on-your-task-in-vs-code/, https://github.blog/changelog/2026-05-20-semantic-issue-search-in-copilot-chat/

12. **Extra builder picks round out the week with flags, images, and edge benchmarks**
    Three backup items are worth quick hits if runtime allows: AppLifecycle Manager feature flags for AI behavior, Microsoft Image-2e efficiency, and Google AI Edge Portal benchmarking. They matter because prompts, image generation, and edge agents all need release controls, production cost evidence, and device-specific performance data.
    Technical depth angle: explain OpenFeature/flagd targeting for prompt/config changes, image-model latency and throughput tradeoffs, and edge benchmark metrics such as prefill, decode, memory, backend, and quantization error.
    Actionability angle: add one kill switch around an AI behavior, benchmark one image path for latency/cost, or test one local model on the actual device instead of assuming desktop numbers transfer.
    Listener hook: this is the grab bag that is only a grab bag until one of these items saves a rollout.
    Primary links: https://cloud.google.com/blog/products/application-development/new-feature-flags-in-applifecycle-manager, https://labs.ai.azure.com/projects/mai-image-2-efficient/, https://cloud.google.com/blog/products/ai-machine-learning/benchmark-llms-on-device-with-ai-edge-portal

## Extra Research Candidates

- **Google Jules asynchronous coding agent** - Primary source: https://blog.google/technology/google-labs/jules/. Technical depth angle: compare async task handoff, repository context, artifact review, and where a hosted coding agent complements Codex/Claude Code rather than replacing local CLI work.
- **Chrome DevTools for agents** - Primary source: https://developer.chrome.com/blog/devtools-for-agents. Technical depth angle: explain browser-state evidence, console/runtime inspection, and why visual agent repair needs first-class browser diagnostics.
- **OpenAI Responses API tool planning updates** - Primary source: https://platform.openai.com/docs/guides/tools. Technical depth angle: explain built-in tool selection, tool result boundaries, and how hosted tool orchestration differs from local MCP or CLI-hosted tools.

## Show Notes

```md
OpenClaw v2026.5.20 leads because it changes the surfaces an agent actually depends on: policy checks, safer secrets, provider routing, cron output, subagent completion, voice context, and image timeouts. Hermes v2026.5.16 gets its own practical segment because it changes install, local proxy, provider auth, browser speed, messaging, LSP diagnostics, file-change verification, computer use, and Codex/Claude-adjacent workflows. Codex rust-v0.133.0 adds goal storage, remote-control readiness, permission profiles, plugin discovery, and lifecycle hooks. Claude Code 2.1.148 follows a bigger terminal-agent update with pinned sessions, code review, MCP pagination, enterprise policy enforcement, Windows repairs, permission reuse, and Bash reliability. After that, the episode moves quickly through Appshots, MCP tunnels, durable agent execution, agent substrate infrastructure, Antigravity migration, small-model computer use, data agents, API-key hardening, and Copilot planning tools.

[00:00] Open on the releases that change daily agent work
Start with the four tools builders are most likely to touch this week: OpenClaw, Codex, Claude Code, and Hermes. Keep the first minute lively: the stack is no longer only "ask a model"; it is policy, auth, goals, plugins, local proxies, browser state, messaging, background sessions, and approvals. Promise a concrete try-now action for every major story.

[03:00] OpenClaw, Codex, and Claude Code upgrade path
OpenClaw: run `openclaw doctor`, inspect policy findings, verify plaintext secret warnings, confirm token files are not symlinked, test OpenRouter provider routing, run one cron task that ends with diagnostic warnings, and run one subagent task that finishes after the parent session has moved on. Treat the release as a host-runtime change, not just a chat-model change: policy, configuration, auth, provider selection, scheduled execution, subagent delivery, browser/image sanitization, voice context, message delivery, timeout behavior, diagnostics, and recovery all need one named test. Codex: create a goal-driven task, test `codex remote-control`, list permission profiles, inspect plugin discovery output, and decide which lifecycle events should be logged. The architecture move is durable goal state, explicit permission profiles, inspectable plugin inventory, and extension hooks around tool execution, turns, subagents, and approvals. Claude Code: test a pinned background session, `/code-review` on a real diff, MCP pagination against a server with more than one page, background permission reuse, Windows shell paths if relevant, and the Bash regression path. The failure modes to watch are concrete: missing MCP resources after page one, a background session asking again for an already-granted permission, enterprise login policy being bypassed through another provider path, or shell commands reporting the wrong exit state. Capture API and SDK behavior, runtime architecture, evaluation notes, benchmark evidence, observability signals, security and privacy boundaries, deployment configuration, latency, throughput, cost, memory, scheduler state, logs, trace IDs, request/response shape, and retry behavior while the task is tiny. The useful setup move is a small verification matrix: one channel action, one scheduled run, one provider-routed model call, one tool approval, one MCP inventory query, one browser/image operation, and one delegated subagent.

[10:00] Hermes Agent as the practical local bench
Hermes deserves a separate segment. The Foundation release adds the easy PyPI install path, `hermes proxy`, OAuth-backed providers, SuperGrok, X search, Teams, lazy installs, faster launch, browser-console acceleration, LINE, SimpleX, `/handoff`, native clarify buttons, Discord backfill, pixel vision, file mutation verification, LSP diagnostics, pluggable video generation, wider computer use, Zed ACP Registry integration, OpenRouter Pareto Code routing, optional skills, API approval events, and plugin-side LLM calls. Turn that into a test path: install or update, run `hermes doctor`, start the proxy, aim one OpenAI-compatible client at it, test one browser inspection, edit one small file and watch LSP feedback, hand off one session, and try one clarification button path. The payoff is not "use every feature"; it is making Hermes a sharper bench for Codex, Claude, local providers, and chat surfaces.

[17:00] Codex Appshots and goal mode
Use Appshots when a UI or desktop-app problem is easier to show than describe. The useful bundle is screenshot plus available text plus a durable goal. Browser annotations make visual feedback specific. Read-only JavaScript context makes inspection safer. Locked computer use is for supervised long local tasks where the Mac may lock before the run finishes. Try this with one UI issue: capture the bad state, set a goal, ask for the smallest code change, run the page, and capture a second state before accepting the result.

[22:00] Secure MCP tunnels
Use Secure MCP tunnels when a private tool should be reachable by an agent without opening inbound firewall ports. The tunnel solves connectivity, not authorization. Before connecting a private MCP server, define the tool allowlist, account/project binding, audit trail, local server trust boundary, and secret path. Avoid turning a tunnel into a universal private-network bridge. Build the first one as read-only and require human approval before mutating calls.

[27:00] Google Agent Executor and durable agent runs
Agent Executor matters because long-running agents need event logs, snapshots, reconnect/backfill, isolated actors, single-writer state, and branchable trajectories. Try mapping one current agent task into those pieces: what event stream exists, where state is stored, how resume works, how to branch a failed path, and what proof is left after the run. If the system cannot answer, the agent may work once but it is not yet trustworthy enough for repeated long-running jobs.

[32:00] GKE Agent Sandbox and Agent Substrate
GKE Agent Sandbox and Agent Substrate target the workload shape of agent systems: isolated sessions, lots of idle time, quick wakeups, stateful sandboxes, and bursty tool use. The practical test is whether warm pools, snapshots, gVisor, and actor scheduling reduce activation delay without hiding state and debugging evidence. Estimate active sessions, idle sessions, retained state, allowed tools, wake latency, and cost per useful session.

[37:00] Antigravity CLI migration
Gemini CLI consumer/free usage stops serving requests on June 18, 2026. Antigravity CLI becomes the planning target. Audit any Gemini CLI task now: auth, config, skills, hooks, subagents, plugins, async jobs, and desktop/CLI context sharing. Run one existing prompt through the new path before the cutoff and record what changed. The migration is easiest while the old path still answers.

[42:00] Microsoft MagenticLite and small-model computer use
MagenticLite is useful because it pairs smaller models with a harness, sandbox, approvals, and browser/file tools. The test is not whether a small model can do everything. It is which tasks become cheap enough and reliable enough when the orchestrator, browser model, approval points, and QEMU sandbox are designed together. Start with a bounded dashboard check, draft-form fill, known-web-tool navigation, or sandboxed local report.

[47:00] Google Data Agent Kit
Data Agent Kit packages data access as configured tools and skills for coding agents. Use it when a data task needs governed access to BigQuery, AlloyDB, Spanner, Cloud Storage, query validation, or drift checks. The first design choice is scope: what can the agent query, what can it write, how are credentials stored, and what should be summarized instead of pasted into context.

[51:00] Gemini API keys and Copilot planning tools
Treat Gemini API keys as paid bearer tokens. Create standalone projects, restrict keys to the intended API, add application restrictions, store server-side keys in Secret Manager, monitor request count by credential ID, and rotate keys that spread. Then use Copilot semantic issue search before code edits: group issues by failure mode, platform, or release area, and only then hand the narrowed task to an agent. If Copilot Auto chooses the model, log the model for high-risk changes.

[55:00] Close
Close with a concrete queue: upgrade OpenClaw/Codex/Claude Code, put Hermes through a small proxy/browser/LSP/handoff test, capture one Codex Appshot, design one MCP tunnel with permissions before connectivity, sketch durable state for one long-running agent, migrate one Gemini CLI task toward Antigravity, try one small-model computer-use task in a sandbox, scope one data agent tool, lock down keys, and use semantic issue search before asking a coding agent to edit.
```

## Chapters

- 00:00 Open on the releases that change daily agent work
- 03:00 OpenClaw, Codex, and Claude Code upgrade path
- 10:00 Hermes Agent as the practical local bench
- 17:00 Codex Appshots and goal mode
- 22:00 Secure MCP tunnels
- 27:00 Google Agent Executor and durable agent runs
- 32:00 GKE Agent Sandbox and Agent Substrate
- 37:00 Antigravity CLI migration
- 42:00 Microsoft MagenticLite and small-model computer use
- 47:00 Google Data Agent Kit
- 51:00 Gemini API keys and Copilot planning tools
- 55:00 Close

## Verified Links

- OpenClaw v2026.5.20: https://github.com/openclaw/openclaw/releases/tag/v2026.5.20
- Codex rust-v0.133.0: https://github.com/openai/codex/releases/tag/rust-v0.133.0
- Claude Code changelog: https://docs.anthropic.com/en/release-notes/claude-code
- Claude Code CHANGELOG: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
- Hermes Agent v0.14.0: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.16
- OpenAI ChatGPT/Codex release notes: https://help.openai.com/en/articles/6825453-chatgpt-release-notes
- OpenAI Secure MCP tunnels: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
- Anthropic MCP tunnels: https://docs.anthropic.com/en/docs/agents-and-tools/mcp-tunnels
- Google Agent Executor: https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime
- Google AX repo: https://github.com/google/ax
- GKE Agent Sandbox and Agent Substrate: https://cloud.google.com/blog/products/containers-kubernetes/bringing-you-agent-sandbox-on-gke-and-agent-substrate
- Agent Substrate repo: https://github.com/agent-substrate/substrate
- Antigravity CLI migration: https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/
- Google Cloud agent developer overview: https://cloud.google.com/blog/topics/developers-practitioners/io26-news-for-agent-developers-on-google-cloud
- Microsoft Foundry Labs May 2026: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/whats-new-in-microsoft-foundry-labs-%E2%80%93-may-2026/4520310
- MagenticLite: https://labs.ai.azure.com/projects/magenticlite/
- MagenticLite GitHub: https://github.com/microsoft/magentic-ui
- Google Data Agent Kit: https://cloud.google.com/blog/products/data-analytics/data-agent-kit-brings-data-skills-and-tools-to-your-ide-or-cli
- Google API-key guidance: https://cloud.google.com/blog/topics/developers-practitioners/api-keys-are-open-secrets
- GitHub Copilot Auto: https://github.blog/changelog/2026-05-20-auto-model-selection-now-routes-based-on-your-task-in-vs-code/
- GitHub Copilot semantic issue search: https://github.blog/changelog/2026-05-20-semantic-issue-search-in-copilot-chat/
- AppLifecycle Manager feature flags: https://cloud.google.com/blog/products/application-development/new-feature-flags-in-applifecycle-manager
- Microsoft Image-2e: https://labs.ai.azure.com/projects/mai-image-2-efficient/
- Google AI Edge Portal: https://cloud.google.com/blog/products/ai-machine-learning/benchmark-llms-on-device-with-ai-edge-portal
