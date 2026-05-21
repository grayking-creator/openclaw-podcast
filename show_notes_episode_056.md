# AgentStack Daily EP056 - OpenClaw 2026.5.19, Claude Code 2.1.146, Secure MCP, and Agent Runtimes

## Release Coverage Check

- **OpenClaw** - Latest stable/verified version: `v2026.5.19` from `https://api.github.com/repos/openclaw/openclaw/releases?per_page=10` with prereleases skipped. Recent episode version tags detected: `v2026.5.12`, `v2026.5.18`, plus earlier `v2026.5.x` tags in the recent tag scan. Selected missing versions: `v2026.5.19`. Candidate verification: the latest stable list starts at `v2026.5.19` and stops when `v2026.5.18` appears in the recent tag scan.
- **Hermes Agent** - Latest stable/verified version: `v2026.5.16` / Hermes Agent 0.14.0 from `https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=10` with prereleases skipped. Recent episode version tags detected: `v2026.5.7`, `v2026.5.16`. Selected missing versions: none. Candidate verification: the latest stable release is present in the recent tag scan, so this lane has no selected release for EP056.
- **OpenAI Codex app/CLI** - Latest stable/verified version: `rust-v0.132.0` / Codex CLI 0.132.0 from `https://api.github.com/repos/openai/codex/releases?per_page=10` with prereleases skipped. Recent episode version tags detected: `rust-v0.130.0`, `rust-v0.131.0`, `rust-v0.132.0`. Selected missing versions: none. Candidate verification: the latest stable release is present in the recent tag scan, so this lane has no selected release for EP056.
- **Claude Code CLI** - Latest verified npm package version: `2.1.146` from `https://registry.npmjs.org/@anthropic-ai/claude-code/latest`; concrete changes verified from Anthropic's Claude Code changelog at `https://docs.anthropic.com/en/release-notes/claude-code` and the GitHub release tag. Recent episode version tags detected: `2.1.141`, `2.1.142`, `2.1.143`, `2.1.144`, `2.1.145`. Selected missing versions: `2.1.146`. Candidate verification: the latest verified list starts at `2.1.146` and stops when `2.1.145` appears in the recent tag scan.
- **Agent-stack release story** - Included. Release coverage leads the episode with OpenClaw `v2026.5.19` and Claude Code CLI `2.1.146`.
- **Runtime target** - 60 minutes.

## Episode Title

OpenClaw 2026.5.19, Claude Code 2.1.146, Secure MCP, and Agent Runtimes

## Tagline

OpenClaw sharpens runtime plugins, browser dialogs, QA gates, and delivery reliability while Claude Code fixes background sessions, MCP pagination, policies, and tracing; then OpenAI and Google ship new private-tooling and distributed-agent infrastructure.

## Feed Description

OpenClaw v2026.5.19 leads with concrete operator changes: Node 22.19 as the floor, runtime-neutral Docker and Podman build args, typed tool plugin commands, browser dialog handling, Codex plugin controls, proxy TLS trust, runtime parity QA gates, realtime Android voice relay, config reload metadata, and a long list of delivery, provider, memory, browser, Telegram, Discord, Slack, media, and Codex app-server fixes. Claude Code CLI 2.1.146 follows with the `/code-review` command rename, AskUserQuestion behavior fixes, MCP pagination repairs, policy enforcement fixes, Windows PowerShell and background-session hardening, OTEL and SDK cleanup, and large-diff rendering improvements. The episode then covers OpenAI Secure MCP Tunnel, Google's Agent Executor runtime, GKE Agent Sandbox GA with Agent Substrate, GitHub Copilot's Auto routing and semantic issue search, and Google Cloud Data Agent Kit.

## Story Slate

### 1. **Agent-stack release readout: OpenClaw v2026.5.19 and Claude Code CLI 2.1.146 move runtime control, QA, plugins, and background agents**
OpenClaw v2026.5.19 changes several surfaces builders actually touch: `OPENCLAW_IMAGE_APT_PACKAGES` and `OPENCLAW_IMAGE_PIP_PACKAGES` for local image builds, `openclaw browser evaluate --timeout-ms`, pending dialog snapshots and `browser dialog --dialog-id`, `defineToolPlugin` plus `openclaw plugins build`, `validate`, and `init`, `/codex plugins list|enable|disable`, shared skill installs with `--global`, runtime parity QA gates, proxy TLS CA trust, config reload metadata, and a stricter Node.js 22.19 floor. Claude Code CLI 2.1.146 renames `/simplify` to `/code-review`, fixes AskUserQuestion suppression in Auto mode, repairs MCP resource/template/prompt pagination, forwards `CLAUDE_CODE_SUBAGENT_MODEL` to child processes, hardens managed login policies, background sessions, Windows PowerShell, NTFS worktree cleanup, SDK streaming, and auto-updater retries.
Technical depth angle: explain OpenClaw's runtime surfaces, image-build knobs, browser modal API, typed plugin manifest generation, Codex plugin control path, config hot-reload metadata, QA runtime parity gates, proxy TLS trust, and cross-channel delivery fixes; explain Claude Code's command rename, Auto-mode question routing, MCP pagination contract, managed-policy enforcement, background-session permission reuse, child-process model propagation, PowerShell launcher behavior, and SDK stream failure modes.
Primary links:
- https://github.com/openclaw/openclaw/releases/tag/v2026.5.19
- https://github.com/anthropics/claude-code/releases/tag/v2.1.146
- https://docs.anthropic.com/en/release-notes/claude-code
- https://www.npmjs.com/package/@anthropic-ai/claude-code

### 2. **OpenAI Secure MCP Tunnel gives private tools an outbound-only path into ChatGPT, Codex, Responses API, and AgentKit**
OpenAI released Secure MCP Tunnel for enterprise customers so private or on-prem MCP servers can be used by supported OpenAI products without opening inbound firewall ports or publishing the MCP server to the internet. The tunnel client runs inside the network that can already reach the MCP server, opens outbound HTTPS to OpenAI, long-polls for queued JSON-RPC work, forwards requests locally, and posts responses back through the same path.
Technical depth angle: explain the tunnel endpoint, tunnel identity, outbound HTTPS control path, queued MCP work, JSON-RPC forwarding, private-server trust boundary, mTLS option, supported OpenAI surfaces, and why this changes the security model for enterprise connectors and internal tool calls.
Primary links:
- https://developers.openai.com/api/docs/changelog
- https://developers.openai.com/api/docs/guides/secure-mcp-tunnels

### 3. **Google Agent Executor open-sources a distributed runtime for durable, resumable, auditable agent execution**
Google introduced Agent Executor, or AX, as an open-source runtime standard for agent execution, resumption, and distributed deployment. It provides event logs, snapshots, secure isolation, session consistency through a single-writer architecture, client reconnect with response backfill from the last seen sequence, and trajectory branching from checkpoints for long-running agents.
Technical depth angle: explain durable event logs, snapshot/resume semantics, single-writer session state, resumable bidirectional streams, isolated actors for controllers, tools, skills and agents, policy/audit control points, client reconnect sequence handling, and how AX federates custom agents with Google-managed agents, A2A, ADK, LangChain, LangGraph, MCPs, and custom compute.
Primary links:
- https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime
- https://github.com/google/ax

### 4. **GKE Agent Sandbox reaches GA and Agent Substrate targets dense, low-latency agent scheduling**
Google made GKE Agent Sandbox generally available and introduced Agent Substrate as an open-source project for higher-density agent infrastructure. The GA story is not just Kubernetes packaging: Agent Sandbox adds pod snapshots, warm pools, standby capacity buffers, gVisor and network-policy isolation, and a Sandbox API that Google says can allocate 300 sandboxes per second per cluster with most allocations completing in 200 milliseconds.
Technical depth angle: explain pod snapshot suspend/resume, warm pools, standby capacity buffers, gVisor and Kata isolation choices, default-deny network policy, Kubernetes control-plane latency limits, Agent Substrate actor-to-worker multiplexing, sub-second activation, state persistence, and why idle long-running agent sessions stress normal pod scheduling.
Primary links:
- https://cloud.google.com/blog/products/containers-kubernetes/bringing-you-agent-sandbox-on-gke-and-agent-substrate
- https://docs.cloud.google.com/kubernetes-engine/docs/concepts/machine-learning/agent-sandbox
- https://docs.cloud.google.com/kubernetes-engine/docs/how-to/agent-sandbox-pod-snapshots
- https://github.com/agent-substrate/substrate

### 5. **GitHub Copilot adds task-aware Auto model routing in VS Code and semantic issue search on the web**
GitHub shipped Copilot Auto model selection in VS Code that routes based on real-time model availability, reliability, task complexity, reasoning needs, code-generation difficulty, bug-diagnosis difficulty, and tool-orchestration needs while preserving admin model policies. GitHub also added semantic issue search in Copilot Chat on web, using a semantic issues index so natural-language queries can find, group, and analyze issues even when the exact title or keywords are missing.
Technical depth angle: explain model-routing signals, cache-boundary routing, premium-request multipliers and discounts, admin policy constraints, health-aware fallback behavior, semantic issue indexing, natural-language repository triage, and where automatic routing helps or hurts reproducibility in coding-agent sessions.
Primary links:
- https://github.blog/changelog/2026-05-20-auto-model-selection-now-routes-based-on-your-task-in-vs-code/
- https://docs.github.com/copilot/concepts/auto-model-selection
- https://github.blog/changelog/2026-05-20-semantic-issue-search-in-copilot-chat

### 6. **Google Cloud Data Agent Kit brings data skills, MCP tools, and plugins into Codex, Claude Code, Gemini CLI, VS Code, and Antigravity**
Google Cloud described Data Agent Kit as an open-source collection of agentic data engineering and data science skills, MCP tools, and plugins that connect local agent surfaces to enterprise data systems such as BigQuery, AlloyDB, Spanner, and Google Cloud Storage. The important change is the shape of the data workflow: codified skills for query optimization, ML best practices, data validation, drift checks, governance, and troubleshooting reduce the need to paste schema context into prompts, while MCP tools expose data platforms through configured connectors.
Technical depth angle: explain MCP connector setup for cloud data systems, codified skill prompts as reusable operational policy, natural-language-to-SQL grounding, intelligent routing between BigQuery and Spark, schema/context-window cost, data governance and troubleshooting surfaces, and the risks of giving coding agents broad data-estate visibility.
Primary link:
- https://cloud.google.com/blog/products/data-analytics/data-agent-kit-brings-data-skills-and-tools-to-your-ide-or-cli

## Extra Research Candidates

- **Google AI Edge Portal adds on-device LLM benchmarking and Model Explorer debugging.** Primary link: https://cloud.google.com/blog/products/ai-machine-learning/benchmark-llms-on-device-with-ai-edge-portal
  Technical depth angle: explain LiteRT-LM benchmarking across more than 120 Android device types, initialization time, prefill speed, decode speed, peak memory, CPU/GPU/NPU backend differences, graph comparison, tensor shapes, quantization error analysis, and per-op latency debugging.

- **Visual Studio 2026 May update surfaces Copilot Agent Skills inside the IDE.** Primary link: https://learn.microsoft.com/en-us/visualstudio/releases/2026/release-notes
  Technical depth angle: explain workspace and user-profile skill discovery, the chat-window skills panel, edit/open/search flows, and how IDE-managed skill files change local agent customization without leaving Visual Studio.

- **GitHub moves Copilot usage metrics report downloads to GitHub-owned domains.** Primary link: https://github.blog/changelog/2026-05-20-copilot-usage-metrics-reports-now-use-github-owned-download-urls/
  Technical depth angle: explain the API URL change from Azure Front Door patterns to `copilot-reports.github.com` and `copilot-reports.*.ghe.com`, firewall and proxy allowlist effects, transition behavior, Azure Blob fallback, and automation reliability for enterprise Copilot reporting.

## Show Notes

```md
[00:00] Opening - OpenClaw runtime surfaces first
OpenClaw v2026.5.19 is the first stop today because it changes the host surfaces that decide whether agents can actually run, recover, inspect browsers, load plugins, and deliver replies reliably. The runtime floor is now Node.js 22.19. Local image builds get runtime-neutral package knobs with `OPENCLAW_IMAGE_APT_PACKAGES` and `OPENCLAW_IMAGE_PIP_PACKAGES`, while the older Docker-specific apt variable remains as a fallback. Browser automation gets explicit modal handling: snapshots surface pending and recently handled dialogs, actions can return `blockedByDialog`, `browser dialog --dialog-id` can answer a pending modal, and `openclaw browser evaluate --timeout-ms` gives long page functions a larger action and request budget.

[02:00] OpenClaw v2026.5.19 and Claude Code CLI 2.1.146 release readout
OpenClaw's plugin and Codex surfaces move too. The CLI now has `defineToolPlugin` plus `openclaw plugins build`, `openclaw plugins validate`, and `openclaw plugins init` for typed simple tool plugins with generated manifest metadata, optional tool declarations, and context factories. Codex sessions get `/codex plugins list`, `/codex plugins enable`, and `/codex plugins disable`, which turns plugin management from config-file surgery into a chat-visible control path. Skills can be installed or updated into shared managed skill storage with `--global`, the repo-local closeout review skill was renamed to `autoreview`, and new debugging, diagram, spike-workflow, meme-maker, Obsidian, and Python debugging skills expand the practical toolbelt.

The release also hardens operator visibility. Gateway restart traces now attribute startup probe, config, runtime, and resource-count costs. Startup logging overlaps with plugin-service startup and channel sidecars while preserving `/readyz` gating, so faster readiness does not mean pretending sidecars are ready before they are. Config tools can distinguish restart-required, hot-reloadable, and no-op fields before applying edits. Managed forward proxies can use HTTPS endpoints and scoped CA trust through `proxy.tls.caFile`. QA-Lab adds runtime parity scenarios, runtime-tool fixture coverage, and blocking drift checks for Codex-native workspace tools versus OpenClaw dynamic tools, plus live-only canaries for Pi-shaped reads, plugin hook crashes, manifest contract errors, and WebChat routing.

The fixes are broad, but several are worth hearing as operating guidance. Memory search now scans the JavaScript fallback vector path in bounded batches so large chunk tables cannot pin the Node.js main thread for seconds. DeepSeek tool schemas with `anyOf` and `oneOf` unions are normalized before requests. Claude model rows keep native image capability even if local catalog data is stale. Browser evaluate and highlight routes enforce current-tab URL allowlists. Telegram forum topics get topic-aware inbound serialization and follow-up routing. Discord, Slack, WebChat, TTS, generated media, outbound registry lookup, direct-message reply delivery, and Codex app-server handoff paths all get fixes that reduce duplicate replies, lost thread context, or stuck tool state.

Claude Code CLI 2.1.146 is the adjacent CLI maintenance release. The visible command change is `/simplify` becoming `/code-review`, with an optional effort level such as `/code-review high`. Auto mode now stops suppressing `AskUserQuestion` when the user or a skill explicitly relies on it. MCP pagination is repaired for `resources/list`, `resources/templates/list`, and `prompts/list`, so paginating servers no longer drop everything past page one. `CLAUDE_CODE_SUBAGENT_MODEL` is forwarded to child processes in multi-agent sessions, managed settings such as `forceLoginOrgUUID` and `forceLoginMethod` are enforced against third-party-provider and API-key sessions, and backgrounded sessions stop re-prompting for tool permissions that were granted with "don't ask again."

The Windows fixes matter for teams running mixed fleets: PowerShell invocations installed through winget or the Microsoft Store stop failing with "command line is invalid," background worktree cleanup no longer follows NTFS junctions into the main repo, attached background sessions stop strobing in Windows Terminal, and GNOME Terminal paste handling is repaired. Claude Code also improves auto-updater retry behavior, large-diff rendering, SDK streaming cleanup, full-screen theme dialogs, and `/background` handling when the only typed input is a skill or custom slash command. The upgrade checklist is concrete: test modal browser flows, long browser evaluations, local image builds, plugin creation and validation, Codex plugin toggles, config reload metadata, runtime parity QA, private proxy trust, MCP pagination, Auto-mode questions, and child-model propagation in delegated sessions.

[17:30] OpenAI Secure MCP Tunnel - private tools without public MCP servers
OpenAI's Secure MCP Tunnel is a security and connectivity release for enterprise tool use. The problem is familiar: ChatGPT, Codex, Responses API, or AgentKit needs to call an MCP server that lives inside a private network, but exposing that server to the internet is the wrong tradeoff. Secure MCP Tunnel flips the direction. A `tunnel-client` runs inside the network that can already reach the private MCP server. It opens outbound HTTPS to OpenAI, or to `mtls.api.openai.com` when control-plane mTLS is configured, then polls for queued work.

The request path stays recognizable as MCP. OpenAI-hosted tunnel endpoints receive MCP work from supported products, queue JSON-RPC requests, and the tunnel client forwards each request to the private MCP server. Responses travel back through the same outbound tunnel. For builders, the design difference is that the private MCP server keeps its local network boundary, while OpenAI products see a normal MCP endpoint. For security teams, the review surface becomes tunnel identity, endpoint configuration, outbound egress policy, local server authorization, and audit logging instead of a new inbound service on the public internet.

The practical use case is internal tools: source-control metadata, issue trackers, data catalogs, incident systems, compliance lookups, internal package registries, or deployment controls that should never be published as public connectors. The risk does not disappear. A private tool is still a tool, and once an agent can call it the policy question moves to scopes, approvals, logging, and output handling. The important change is that private enterprise MCP can now participate in OpenAI agent workflows without the brittle pattern of reverse proxies, temporary tunnels, or copy-pasted credentials.

[27:00] Google Agent Executor - durable distributed agent runtime
Google's Agent Executor, or AX, is an open-source runtime for long-running agents that need recovery, isolation, and distributed deployment. The core idea is that agent work is not a single request. It is an execution with state, tool calls, pauses, reconnects, possible human confirmations, and sometimes multiple actors trying to touch shared session state. AX puts a controller, event log, registry, remote agents, tools, skills, and environments behind a runtime that can record execution state and resume after failures.

The key mechanism is durable execution through event logs and snapshots. If a client disconnects, AX can reconnect and backfill responses from the last sequence seen by that client. If a workflow needs to pause for human review, or a worker fails mid-run, the runtime has a recovery point. Session consistency uses a single-writer architecture so multiple components do not corrupt shared state by racing writes. Trajectory branching lets a workflow fork from a checkpoint so an agent can test or evaluate different paths without losing the original context.

AX is also meant to federate deployment models. Google describes it as compatible with Antigravity, Google-built frontier agents, Managed Agents in Gemini API, custom agents built with ADK, LangChain, LangGraph, and systems using Agent2Agent Protocol. The important builder implication is portability of the execution layer. If the agent harness, tools, models, and compute all have to be swapped independently, the runtime needs consistent resumption, audit, and policy boundaries. AX is early and the repository warns that resumption protocols can change before stable release, but the direction is clear: production agent platforms are converging on execution logs, resumable streams, isolated actors, and explicit policy points.

[36:00] GKE Agent Sandbox and Agent Substrate - scheduling idle agents at scale
GKE Agent Sandbox is now generally available, and its details are more interesting than the GA label. Agent workloads are bursty. They execute code, wait for model responses, wait for humans, wait for external systems, then wake up again. Keeping every session hot wastes compute, but starting a fresh sandbox for every request adds cold-start latency. GKE Agent Sandbox addresses that with pod snapshots, warm pools, standby capacity buffers, and sandbox APIs for isolated stateful workloads.

Google says the Sandbox API's integrated warm pool can allocate 300 sandboxes per second per cluster, with 90 percent of allocations completing in 200 milliseconds. Pod snapshots let idle agent workloads suspend and resume in seconds. Standby capacity buffers use suspended VMs to refill warm pools at lower cost. The isolation stack includes gVisor, default-deny Kubernetes network policy, and pluggable interfaces for runtimes like Kata Containers. That combination is aimed at the hard part of code-using agents: untrusted logic needs kernel and network isolation, but the platform still has to feel close to interactive.

Agent Substrate pushes the same problem below normal Kubernetes scheduling. The open-source project maps a larger set of stateful actors onto a smaller set of ready worker pods, relying on the fact that many agent-like applications are idle most of the time. It manages actor lifecycle, suspend/resume, worker assignment, and traffic routing while keeping the Kubernetes control plane out of the critical path for some operations. The builder takeaway is not that every team needs this immediately. It is that high-scale agent infrastructure is starting to look less like ordinary request serving and more like dense session scheduling with fast teleportation of state onto available compute.

[45:00] GitHub Copilot - Auto model routing and semantic issue search
GitHub's VS Code Auto model selection update makes Copilot routing more explicit. Auto weighs real-time model availability and reliability, then evaluates the task along dimensions such as reasoning demand, code-generation complexity, bug-diagnosis difficulty, and tool-orchestration needs. It honors admin model policies, shows which model was used, and routes along natural cache boundaries to avoid avoidable cache costs. Billing follows the selected model, currently limited to models with 0x to 1x multipliers, with a 10 percent discount on the model multiplier when Auto uses a billable model.

For coding agents, Auto routing is useful when the main problem is throughput and reliability: ask mode, light edits, explanation, triage, and straightforward code generation do not always need a high-reasoning model. The tradeoff is reproducibility. If the selected model can vary by health, availability, subscription, policy, and task classification, teams need to know when to pin a model for evals, incident reproduction, or sensitive refactors. The right default is probably Auto for ordinary work and explicit model selection for tests whose result needs to be comparable run to run.

The semantic issue search update gives Copilot Chat on web a repository-planning surface. Instead of exact title or keyword matching, Copilot can use a semantic issues index to find, group, and analyze related issues from a natural-language query. That matters for maintenance agents because issue triage often starts with fuzzy memory: "the Windows terminal paste bug," "the thing about quota reset," or "all reports about stale PR badges." The limitation is that semantic retrieval needs verification against the actual issue text before a coding agent treats the result as a work order.

[52:00] Google Cloud Data Agent Kit - data skills and MCP tools in the coding surface
Google Cloud Data Agent Kit is aimed at a different bottleneck: agents that need enterprise data context without a giant manual prompt. The kit brings data engineering and data science skills, MCP tools, and plugins into VS Code, Claude Code, Codex, Gemini CLI, and Antigravity CLI. The primitives are concrete. Skills codify workflows for query optimization, ML best practices, data validation, drift checks, governance, and troubleshooting. MCP tools connect agent workflows to BigQuery, AlloyDB, Spanner, and Google Cloud Storage. Plugins put those surfaces into the developer environment.

The practical mechanism is reducing the context-window tax. Instead of pasting schema metadata, query examples, governance notes, and troubleshooting steps into every prompt, the agent can use configured connectors and reusable data skills. Google also describes intelligent routing between compute engines, for example BigQuery for SQL-native analytics and ELT, or Spark for custom Python transformations and distributed ML training. Conversational analytics brings natural-language dataset exploration into the same workspace, using Gemini natural-language-to-SQL technology.

The risk is access scope. A coding agent with broad data-estate visibility can be useful, but it also becomes a place where governance, lineage, authorization, and query-cost controls must be enforced. Builders should treat Data Agent Kit as a harness for grounded data work, not as permission to give every agent every dataset. Start with read-only connectors, explicit project and dataset scopes, query-cost limits, and skills that encode the organization's preferred validation and governance checks.

[58:30] Close - what to test next
The release work to test first is concrete. Upgrade OpenClaw where Node 22.19 is available, validate image-build package knobs, try a browser modal flow, run a long browser evaluation with an explicit timeout, create or validate a simple tool plugin, toggle a Codex plugin from chat, inspect config reload metadata, and run the runtime parity QA tier that matches your deployment. On Claude Code, test `/code-review`, Auto-mode question prompts, MCP pagination against a server with more than one page, managed-login policy enforcement, background permissions, and child-process model propagation.

For the external stories, the useful experiments are small. Put one private MCP server behind Secure MCP Tunnel and review the resulting trust boundary. Run an AX sample only if you need resumable distributed execution, and watch the resumption protocol churn before depending on it. Treat GKE Agent Sandbox as the production option for isolated code execution on Kubernetes, and Agent Substrate as the scaling direction for dense idle sessions. Use Copilot Auto for everyday work, pin models for reproducible evaluations, and treat semantic issue search as a triage accelerator that still needs source verification. For Data Agent Kit, start narrow: one dataset, one read-only connector, one codified skill, and one validation path.
```

## Verified Links

- https://github.com/openclaw/openclaw/releases/tag/v2026.5.19
- https://github.com/anthropics/claude-code/releases/tag/v2.1.146
- https://docs.anthropic.com/en/release-notes/claude-code
- https://www.npmjs.com/package/@anthropic-ai/claude-code
- https://developers.openai.com/api/docs/changelog
- https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
- https://cloud.google.com/blog/products/ai-machine-learning/agent-executor-googles-distributed-agent-runtime
- https://github.com/google/ax
- https://cloud.google.com/blog/products/containers-kubernetes/bringing-you-agent-sandbox-on-gke-and-agent-substrate
- https://docs.cloud.google.com/kubernetes-engine/docs/concepts/machine-learning/agent-sandbox
- https://docs.cloud.google.com/kubernetes-engine/docs/how-to/agent-sandbox-pod-snapshots
- https://github.com/agent-substrate/substrate
- https://github.blog/changelog/2026-05-20-auto-model-selection-now-routes-based-on-your-task-in-vs-code/
- https://docs.github.com/copilot/concepts/auto-model-selection
- https://github.blog/changelog/2026-05-20-semantic-issue-search-in-copilot-chat
- https://cloud.google.com/blog/products/data-analytics/data-agent-kit-brings-data-skills-and-tools-to-your-ide-or-cli
- https://cloud.google.com/blog/products/ai-machine-learning/benchmark-llms-on-device-with-ai-edge-portal
- https://learn.microsoft.com/en-us/visualstudio/releases/2026/release-notes
- https://github.blog/changelog/2026-05-20-copilot-usage-metrics-reports-now-use-github-owned-download-urls/

## Chapters

- **[00:00] Opening - OpenClaw runtime surfaces first**
- **[02:00] Release readout - OpenClaw v2026.5.19 and Claude Code CLI 2.1.146**
- **[17:30] OpenAI Secure MCP Tunnel - private tools without public MCP servers**
- **[27:00] Google Agent Executor - durable distributed agent runtime**
- **[36:00] GKE Agent Sandbox and Agent Substrate - scheduling idle agents at scale**
- **[45:00] GitHub Copilot - Auto model routing and semantic issue search**
- **[52:00] Google Cloud Data Agent Kit - data skills and MCP tools in the coding surface**
- **[58:30] Close - what to test next**
