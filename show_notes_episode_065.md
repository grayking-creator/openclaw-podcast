# AgentStack Daily EP065 — Hermes Agent v0.16.0 Desktop App, Codex 0.137, Claude Code 2.1.167, and Gemma 4 12B on the Local Agent Stack

**Title:** Hermes Agent v0.16.0 Desktop App, Codex 0.137 Multi-Agent v2, Claude Code Fallback Models, and Gemma 4 12B on the Local Stack

**Tagline:** Hermes Agent v0.16.0 ships a real native desktop app with OAuth remote connect, drag-and-drop files, and a full web admin panel across 874 commits. Codex 0.137 adds multi-agent v2 runtime choice persistence and parallel web search. Claude Code 2.1.166/2.1.167 introduces fallback model chains and glob tool-name deny rules. Gemma 4 12B puts a 12B-parameter encoder-free multimodal model in the 16GB VRAM sweet spot for local agentic workflows.


**Feed description:** Hermes Agent v0.16.0 — "The Surface Release" — ships a real native desktop app with OAuth remote connect, drag-and-drop file input, and a browser-based admin panel. Codex 0.137 adds multi-agent v2 runtime choice persistence and parallel web search. Claude Code 2.1.166/2.1.167 introduces fallback model chains and glob tool-name deny rules. Gemma 4 12B is Google's latest open-weight 12B model that runs locally on a laptop with 16GB VRAM. The project radar covers the A2A protocol hitting v1.0, Kimi Code CLI as a TypeScript-native terminal coding agent, and the awesome-ai-agents-2026 curated resource list.

---

## Story Slate

1. **Hermes Agent v0.16.0 ships a real native desktop app across 874 commits** — Hermes Agent v0.16.0 landed June 6, 2026 as "The Surface Release" — the most surface-area-expanding release since the project started. The headline is a native Electron desktop application that installs like any other macOS/Linux/Windows app, updates itself in place, and gives you a proper chat window with streaming, session archiving, clipboard image paste, a Cmd+K command palette, and an inline model picker in the status bar. The desktop app does not have to run locally — it can connect to a remote Hermes gateway over OAuth or username/password, which means a team can share a hosted Hermes instance and each developer runs their own native GUI. The web dashboard grew a full browser-based administration panel covering the MCP catalog, messaging channels, credentials, webhooks, memory, and pluggable OIDC/username-password login. First-time setup now has a "Quick Setup via Nous Portal" path that gets you from install to first message in seconds. The default skill set was trimmed to what you actually need, `/undo` finally lets you take back the last N turns, and the model picker is fuzzy-searchable everywhere — desktop, web, TUI, and CLI. Two P0 and 62 P1 bug closures ride along, plus a security round: CVE-2026-48710 Starlette pin, SSRF off-loop hardening, and subprocess credential stripping.

Technical depth angle: explain the Electron desktop app architecture versus terminal wrapper approach, OAuth remote gateway authentication flow, the browser-based admin panel MCP catalog and credential management surfaces, fuzzy model picker implementation across surfaces, `/undo` turn rollback semantics, and the security fixes (CVE-2026-48710 Starlette pin, SSRF off-loop hardening, subprocess credential stripping).

Actionability angle: download the Hermes Agent desktop app installer and run it against your existing local or remote gateway; test OAuth login against a remote gateway to verify the authentication flow; explore the new web admin panel to audit MCP servers, messaging channels, and credentials; set up Quick Setup via Nous Portal on a fresh install to compare the new first-run experience against the old CLI flow.

Listener hook: Hermes Agent just became an app your non-technical teammates will actually use — a real desktop installer, OAuth remote connect, drag-and-drop files, and a web admin panel came in across 874 commits in a single release cycle.

2. **Codex rust-v0.137.0 adds multi-agent v2 runtime choice persistence and parallel web search** — OpenAI Codex CLI rust-v0.137.0 published June 4, 2026 as the latest stable tag, two releases past EP063's rust-v0.135.0 baseline. The headline feature is multi-agent v2 with runtime choice persistence: each spawned thread now carries its own runtime choice forward, and spawned agents get cleaner follow-up and metadata defaults — meaning multi-agent orchestration in Codex is less likely to lose its place when a parent session hands off to a child. F13-F24 keybinding support in the TUI and paste in searchable menus improve the terminal experience for power users. Enterprise and admin flows now show monthly credit limits and can apply cloud-managed config bundles including EDU workspaces. Plugin workflows gained machine-readable `codex plugin list --json` output and cached remote catalog suggestions. Hosted web and image tools are available in more code-mode flows, with standalone web searches now able to run in parallel. Permission requests and approvals now carry environment identity, which closes a gap where a permission granted in one context could leak across to another. Platform reliability improved for macOS app launches and Windows SQLite startup, thread resume, and sandbox setup refreshes.

Technical depth angle: explain multi-agent v2 runtime choice persistence per thread, F13-F24 keybinding architecture in the TUI, `codex plugin list --json` machine-readable output format, parallel standalone web search implementation, environment identity in permission requests and approvals, and Windows SQLite startup reliability improvements.

Actionability angle: upgrade Codex to rust-v0.137.0; test one multi-agent session to verify runtime choice persists correctly across spawn and resume; run `codex plugin list --json` to see the machine-readable output; test parallel web search in a code-mode flow to verify parallel execution; check the new monthly credit limit display in enterprise/admin flows.

Listener hook: multi-agent v2 is the feature that makes Codex's agent spawning actually hold together across session boundaries — runtime choice persistence means the orchestrator does not lose its place when it hands off to a child agent.

3. **Claude Code 2.1.166 adds fallback model chains and glob tool-name deny rules** — Claude Code's npm `latest` is now 2.1.166 and 2.1.167, following 2.1.165. Version 2.1.166 is the feature release: a new `fallbackModel` setting lets you configure up to three fallback models tried in order when the primary model is overloaded or unavailable — and `--fallback-model` now also applies to interactive sessions, not just background ones. Glob pattern support in deny rule tool-name positions means `"*"` denies all tools, with allow rules rejecting non-MCP globs and unknown tool names in deny rules triggering a startup warning. Version 2.1.167 is pure bug fixes and reliability improvements. The fallback model chain is the operator-facing feature that changes how you handle model unavailability: instead of a single prompt failing when a model is at capacity, Claude Code can automatically roll over to the next model in the chain you defined.

Technical depth angle: explain fallback model chain configuration semantics (up to three models in order), `--fallback-model` interactive session application, glob pattern `"*"` for full tool denial, allow rule non-MCP glob rejection logic, unknown tool name deny rule startup warnings, and how the fallback chain interacts with `requiredMinimumVersion`/`requiredMaximumVersion` fleet compliance settings.

Actionability angle: add `fallbackModel` to your Claude Code config with two or three alternatives ordered by preference; test the chain by temporarily making your primary model unavailable and verifying the fallback fires correctly; use `"*"` in a deny rule to test full tool lockout; verify that unknown tool names in deny rules produce startup warnings.

Listener hook: Claude Code can now chain fallback models so a saturating API does not stop your agent dead — configure up to three models in priority order and the runtime picks the next one when the primary is overloaded.

4. **Gemma 4 12B puts a capable encoder-free multimodal model in the 16GB VRAM sweet spot** — Google released Gemma 4 12B on June 3, 2026 as an Apache 2.0 open-weight checkpoint with a 256K context window, designed to bring agentic multimodal intelligence directly to laptops for local workflows. The key architectural decision is encoder-free multimodal input: vision and audio flow directly into the LLM backbone rather than through a separate multimodal encoder, which reduces the parameter overhead and lets the model run on 16GB and 32GB consumer GPUs. Benchmark performance is described as nearing Google's 26B model on advanced reasoning tasks, which would place a 12B model competitive with models twice its size. The agentic workflow positioning is explicit: autonomous data processing, visual insights, and webpage building are listed as target use cases. Google AI Edge integration provides the path for local deployment on laptop hardware. For the agent stack, Gemma 4 12B is the most realistic open-weight 12B model for local coding-agent use on consumer hardware — it changes what local-first agent workflows look like when the model and weights stay on your machine.

Technical depth angle: explain encoder-free multimodal architecture where vision/audio flow directly into the LLM backbone, the 256K context window implementation, 12B parameter class hardware requirements for 16GB VRAM, Google AI Edge local deployment path, benchmark performance positioning relative to the 26B model, and what encoder-free design means for latency and memory usage versus encoder-decoder multimodal approaches.

Actionability angle: pull the Gemma 4 12B checkpoint from Hugging Face and run it through LM Studio or Ollama on a laptop with 16GB VRAM; compare one coding task output against your current local model; test the 256K context on a long codebase or document understanding task; use Google AI Edge for the managed local deployment path if you prefer a一键 install.

Listener hook: Gemma 4 12B is the first 12B-class open-weight model from a major lab that Google says can run on your laptop and still do advanced reasoning — the encoder-free architecture is the trick that makes it fit in 16GB of VRAM.

5. **Kimi Code CLI brings a TypeScript-native terminal coding agent to the agent stack** — Moonshot AI released Kimi Code CLI on June 5, 2026 as an MIT-licensed open-source terminal AI coding agent written in TypeScript. The project is the successor to the older kimi-cli and is distributed via npm or a single install script that needs no Node.js pre-installed. It reads and edits code, runs shell commands, searches files, fetches web pages, and chooses its next step based on feedback — the standard coding agent loop. Out of the box it works with Moonshot AI's Kimi models and can be configured to use other compatible providers. Notable features include a fast TUI ready in milliseconds, video input for dropping screen recordings into chat, AI-native MCP configuration via `/mcp-config`, subagents for parallel work (coder, explore, and plan subagents in isolated contexts), and lifecycle hooks for gating tool calls, auditing decisions, or triggering notifications. The feedback-driven execution model runs read-only operations automatically and asks for confirmation on file edits or shell commands — an approval flow that keeps risky actions under developer control. Version 0.11.0 published June 5, 2026. The project has 1,902 GitHub stars and active development.

Technical depth angle: explain the feedback-driven execution model and approval flow for risky operations, TypeScript native architecture versus wrapper approaches, subagent isolation for parallel work (coder, explore, plan), lifecycle hook semantics for tool call gating and audit trails, AI-native MCP configuration via `/mcp-config`, and video input processing for screen recording ingestion.

Actionability angle: install Kimi Code CLI with `curl -fsSL https://code.kimi.com/kimi-code/install.sh | bash` and run `kimi --version` to verify; connect it to your Kimi API key or Moonshot AI OAuth; test one MCP server configuration via `/mcp-config`; run one subagent in parallel against a codebase task and compare execution quality against your current CLI agent.

Listener hook: Kimi Code CLI is the TypeScript-native terminal coding agent that was missing from the stack — written in TypeScript, distributed as a single binary, with native MCP support and subagents for parallel work.

6. **A2A Protocol v1.0 reaches a formal milestone as the agent interoperability layer** — The Agent-to-Agent (A2A) Protocol reached v1.0 in 2026 under the Linux Foundation, establishing a formal specification for how agents from different frameworks discover each other, establish communication channels, and delegate tasks. The protocol defines "agent cards" — JSON capability manifests — for agent discovery, and a task-based state machine for long-running interactions using JSON-RPC 2.0. Originally launched by Google, A2A is now governed by the Linux Foundation alongside MCP (which standardizes how agents connect to tools and data sources). The distinction matters: MCP is about what an agent can do with external tools; A2A is about how agents work together. The a2aproject/A2A GitHub repository has 24,153 stars and active development. For the agent stack, A2A v1.0 is the interoperability layer that will let a Claude Code session delegate to a Hermes agent, or an OpenClaw agent hand off to a Codex thread — without custom integration work for each pair. The protocol has reached sufficient maturity that builders should be aware of it when designing multi-agent workflows.

Technical depth angle: explain A2A agent card JSON capability manifests for discovery, the task-based state machine for long-running interactions, JSON-RPC 2.0 message format, the MCP versus A2A scope distinction (tools versus inter-agent communication), Linux Foundation governance, and what v1.0 formalization means for protocol stability and adoption.

Actionability angle: read the A2A v1.0 specification on the a2aproject/A2A GitHub repo to understand agent card structure and task state machine semantics; if you are building a multi-agent workflow, design the agent handoff points with A2A agent cards in mind; test one cross-framework agent delegation if you have two different agent runtimes available.

Listener hook: A2A v1.0 is the protocol that makes agent interoperability real — agents from different frameworks can now discover each other and hand off work through a formal JSON-RPC 2.0 state machine, not custom glue code for every pair.

---

## Model Discovery Check

**Lane: OpenRouter / Open-Source / Agent-Focused Models**

Recent episode model coverage detected:
- MiniMax M3 (open-weight, 1M context, MSA/sparse attention, multimodal, MiniMax Code, coding/agentic)
- Qwen 3.7 Max/Plus (coding-reasoning vs multimodal-vision split, open weights)
- Claude Opus 4.8 (Anthropic, coding agent model)
- GPT-5.5 (OpenAI)
- Gemini 3.x (Google)
- MAI-Code-1-Flash, MAI-Image-2.5 (Microsoft, Build 2026)
- Cosmos 3 (NVIDIA, COMPUTEX 2026)

Newly discovered models post-last-update:
- **Gemma 4 12B** — Provider: Google DeepMind. Release date: June 3, 2026. Availability: Apache 2.0 open weights on Hugging Face, local deployment via Google AI Edge on laptop hardware with 16GB+ VRAM. Architecture: 12B parameters, encoder-free multimodal (vision/audio direct to LLM backbone), 256K context window, agentic workflow design. Primary source: https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12B/. Decision: **SELECTED** — encoder-free multimodal design is architecturally distinct, 12B class fits in consumer GPU RAM, open-weight Apache 2.0 license, directly relevant to local agentic workflows on the agent stack.
- **Qwen 3.7 Plus** — Provider: Alibaba Qwen. Release date: June 2, 2026. Availability: API (OpenRouter, Qwen Bailian), open weights. Architecture: text+image input, 1M context, deep reasoning, self-programming, tool invocation. Primary source: https://openrouter.ai/models?qwen%2Fqwen3.7-plus. Decision: **NOT SELECTED** — Qwen 3.7 Max and Plus were both covered previously; re-selecting either variant in EP065 would duplicate prior coverage.
- **NVIDIA Nemotron 3 Ultra 550B** — Provider: NVIDIA. Release date: June 4, 2026. Availability: OpenRouter free tier and paid. Architecture: 55B active / 550B total MoE, hybrid Transformer-Mamba, 1M context, tool use, reasoning. Primary source: https://openrouter.ai/models. Decision: **NOT SELECTED** — MoE model with 550B total parameters is not architecturally novel (NVIDIA has released similar models), 55B active is large for most local use cases, and the encoder-free multimodal story from Gemma 4 12B is more impactful for the local agent stack audience.

---

## GitHub Project Radar

- **A2A Protocol** — https://github.com/a2aproject/A2A — Open protocol for agent-to-agent interoperability, JSON-RPC 2.0 task state machine, agent card discovery. 24,153 GitHub stars, active development as of June 6, 2026. Stack improvement angle: enables cross-framework agent handoff without custom integration code per pair — the formal interoperability layer the agent stack has been missing. Try now: read the A2A v1.0 spec to understand agent card structure, then design one multi-agent handoff point in your workflow using the protocol's task state machine.
- **Kimi Code CLI** — https://github.com/MoonshotAI/kimi-code — TypeScript-native terminal coding agent, MIT license, 1,902 stars, v0.11.0 published June 5, 2026. Works with Kimi models out of the box; configurable to other providers. Stack improvement angle: a TypeScript-first CLI coding agent with native MCP support, subagent parallel dispatch, and lifecycle hooks gives the agent stack a TypeScript-native option that plugs into the npm ecosystem directly. Try now: install with `curl -fsSL https://code.kimi.com/kimi-code/install.sh | bash`, run `kimi --version`, and test one MCP server connection via `/mcp-config`.
- **awesome-ai-agents-2026** — https://github.com/Zijian-Ni/awesome-ai-agents-2026 — Curated list of AI agent frameworks, tools, protocols, and resources for 2026. 124 stars, updated June 5, 2026. Covers MCP, A2A, coding agents, computer use, and agentic infrastructure. Stack improvement angle: the definitive curated index for the agent stack — use it to discover new MCP servers, agent frameworks, protocols, and tooling that apply to your specific workflow. Try now: browse the MCP/A2A protocol sections to find one new server or protocol implementation relevant to your stack.

---

## Extra Research Candidates

- **MCP security: NIST AI Agent Standards Initiative and NSA alert** — Primary source: https://www.gopher.security/news/nist-ai-agent-standards-2026-mcp-security and https://www.upguard.com/blog/mcp-ai-protocol-expanding-your-attack-surface. Technical depth angle: explain NIST's formal security requirements mandate for MCP deployments, NSA critical vulnerability alert scope, "Shadow MCP" attack surface risks, UpGuard's enterprise data exfiltration analysis, and what formal MCP security requirements mean for enterprise operator adoption.
- **Anthropic Claude Opus 4.8 and Dynamic Workflows for multi-agent orchestration** — Primary source: https://www.anthropic.com/news/expanding-project-glasswing and https://linas.substack.com/p/anthropic-claude-2026-every-launch-guide. Technical depth angle: explain Dynamic Workflows as a multi-agent orchestration primitive in Claude, Project Glasswing autonomous research capabilities, Claude Mythos Preview vulnerability scanning, and what Dynamic Workflows mean for parallel subagent orchestration in coding agent sessions.
- **Hermes Agent v0.16.0 desktop app architecture and OAuth remote connect internals** — Primary source: Hermes Agent v0.16.0 release announcement. Technical depth angle: explain the Electron desktop app architecture versus CLI-only design, OAuth WebSocket remote gateway authentication flow, web admin panel MCP catalog and credential management implementation, and the `/undo` turn rollback semantics and implementation constraints.

---

## Show Notes

```md
Episode 65 — June 6, 2026

[00:00] Episode hook

Hermes Agent v0.16.0 (v2026.6.5) drops "The Surface Release" on June 6, 2026 — a native cross-platform desktop app with OAuth remote connect, drag-and-drop file input, and a full browser-based web admin panel, all shipped across 874 commits and 542 merged PRs since v0.15.2. OpenAI Codex rust-v0.137.0 adds multi-agent v2 runtime choice persistence per thread, parallel standalone web search, and enterprise credit limit controls. Claude Code 2.1.166 introduces configurable fallback model chains of up to three models and glob tool-name deny rules, with 2.1.167 following as a bug-fix polish release. Gemma 4 12B is Google's June 3 open-weight release that puts a 12B-parameter encoder-free multimodal model in the 16GB VRAM sweet spot for local agentic workflows. The project radar covers A2A Protocol v1.0 as the formal agent interoperability layer, Kimi Code CLI as a TypeScript-native terminal coding agent, and the awesome-ai-agents-2026 curated resource index.

[02:00] Hermes Agent v0.16.0 — native desktop app, OAuth remote connect, and web admin panel

Hermes Agent v0.16.0 is the release that changes how Hermes meets the developer. The headline is a real native Electron desktop application — not a terminal wrapper, not a web tab — that installs like any other macOS, Linux, or Windows app and updates itself in place from inside the app. The desktop GUI gives you a proper chat window with streaming, a session list you can archive and search, drag-and-drop files anywhere in the chat area, clipboard image paste, a Cmd+K command palette, and a model picker right in the status bar. If you have been telling non-technical teammates "it is a CLI agent" and watching their eyes glaze over, you can now just send them an installer.

The desktop app does not have to run Hermes locally. Point it at a remote Hermes gateway — your homelab, a hosted box, a teammate's server — and it connects over a secure WebSocket, authenticating with OAuth or username/password. No fiddling with `--insecure` flags or hand-copied session tokens. Each profile can target its own remote host, and you can run concurrent sessions across multiple profiles simultaneously. This is the remote-connect story that enterprise and team Hermes deployments have been waiting for.

The web dashboard grew a full browser-based administration panel. You get MCP catalog management, messaging channel configuration, credential storage, webhook management, memory configuration, and pluggable OIDC or username-password login — all from a browser without touching the CLI. First-time setup now has a "Quick Setup via Nous Portal" path that gets you from install to first message in seconds, which matters for onboarding new users or evaluating Hermes in a fresh environment.

The default skill set was trimmed to what you actually need. NVIDIA/skills joined the trusted Skills Hub taps. The model picker is now fuzzy-searchable everywhere — desktop, web, TUI, and CLI — which sounds trivial until you have a long list of models and no search. `/undo` finally lets you take back the last N turns, which is the quality-of-life feature that users have requested since the first release.

Under the hood, two P0 and 62 P1 bug closures ride along. The security round is worth noting individually: CVE-2026-48710 pins the Starlette dependency to a fixed version, SSRF off-loop hardening closes a class of server-side request forgery vectors in plugin and provider request paths, and subprocess credential stripping ensures credentials do not leak into child process environments.

Practical upgrade list: download and install the desktop app for your OS; test OAuth login against a remote gateway if you have one; explore the web admin panel to audit MCP servers, channels, and credentials; run Quick Setup via Nous Portal on a fresh install to compare the new first-run experience; and verify `/undo` works for the last N turns in your session.

[16:00] Codex rust-v0.137.0 — multi-agent v2, parallel web search, and enterprise controls

Codex rust-v0.137.0 published June 4, 2026 as the latest stable CLI tag, two releases past EP063's rust-v0.135.0 baseline. The most architecturally significant change is multi-agent v2 with runtime choice persistence: each spawned thread now carries its own runtime choice forward, and spawned agents get cleaner follow-up and metadata defaults. This means when a parent Codex session spawns a child agent, the child does not lose its place when the parent session hands off — the runtime choice stays with the thread, not just the parent process. For multi-agent orchestration workflows, this is the difference between an agent that holds together across a hand-off and one that silently drops context.

F13-F24 keybinding support in the TUI and paste in searchable menus improve the terminal experience for power users who use extended keyboard layouts. Enterprise and admin flows now show monthly credit limits and can apply cloud-managed config bundles including EDU workspaces — the credit limit visibility closes a gap where operators could not see spend until the bill arrived.

Plugin workflows gained machine-readable `codex plugin list --json` output and cached remote catalog suggestions. The machine-readable output means you can pipe plugin lists into scripts, CI pipelines, or fleet management tooling without parsing human-readable text. Cached remote catalog suggestions speed up the plugin discovery flow by avoiding repeated network calls.

Hosted web and image tools are available in more code-mode flows, with standalone web searches now able to run in parallel. Parallel standalone web search means Codex can fire multiple search queries simultaneously and synthesize results rather than running them sequentially — a real latency win for research-heavy workflows. Permission requests and approvals now carry environment identity, which closes a gap where a permission granted in one context could incorrectly apply across context boundaries. Platform reliability improved for macOS app launches and Windows SQLite startup, thread resume, and sandbox setup refreshes.

Practical upgrade list: upgrade Codex to rust-v0.137.0; test one multi-agent session to verify runtime choice persists correctly across spawn and resume; run `codex plugin list --json` to see the machine-readable output format; test parallel web search in a code-mode flow; check the new monthly credit limit display in enterprise/admin flows.

[26:00] Claude Code 2.1.166/2.1.167 — fallback model chains and glob tool-name deny rules

Claude Code's npm `latest` is now 2.1.166 and 2.1.167, following 2.1.165. Version 2.1.166 is the feature release with two operator-visible additions. The headline is a new `fallbackModel` setting that lets you configure up to three fallback models tried in order when the primary model is overloaded or unavailable. The `--fallback-model` flag now also applies to interactive sessions, not just background ones — meaning interactive terminal sessions can also automatically roll over to the next model in the chain when the primary saturates. This changes how you handle model unavailability: instead of a single prompt failing when an API is at capacity, Claude Code automatically tries the next model you configured.

Glob pattern support in deny rule tool-name positions is the second feature. Using `"*"` denies all tools. Allow rules reject non-MCP globs, and unknown tool names in deny rules now warn at startup rather than silently accepting malformed rules. The startup warning for unknown tool names is the operator-friendly improvement: you now know at startup if a deny rule is misconfigured rather than discovering it when the rule fails to fire.

Version 2.1.167 is pure bug fixes and reliability improvements — the hygiene wave that keeps the release train clean between feature releases.

Practical upgrade list: add `fallbackModel` to your Claude Code config with two or three alternatives ordered by preference; test the chain by temporarily making your primary model unavailable and verifying the fallback fires correctly; use `"*"` in a deny rule to test full tool lockout; verify that unknown tool names in deny rules produce startup warnings; and upgrade to 2.1.167 for the latest bug fixes.

[34:00] Gemma 4 12B — encoder-free multimodal model in the 16GB VRAM sweet spot

Google released Gemma 4 12B on June 3, 2026 as an Apache 2.0 open-weight checkpoint with a 256K context window, designed to bring agentic multimodal intelligence directly to laptops for local workflows. The key architectural decision is encoder-free multimodal input: vision and audio flow directly into the LLM backbone rather than through a separate multimodal encoder. This is the same architectural pattern that makes large multimodal models fit in smaller parameter counts — by removing the encoder overhead, the 12B model can handle image and audio inputs without a separate processing stage that adds parameters and latency.

Benchmark performance is described as nearing Google's 26B model on advanced reasoning tasks, which would place a 12B model competitive with models twice its size on the benchmarks that matter for agentic workflows. The agentic workflow positioning is explicit: autonomous data processing, visual insights, and webpage building are listed as target use cases. Google AI Edge provides the path for local deployment on laptop hardware with 16GB and 32GB VRAM.

For the agent stack, Gemma 4 12B is the most realistic open-weight 12B model for local coding-agent use on consumer hardware. It changes what local-first agent workflows look like when the model and weights stay on your machine — no API latency, no data leaving your environment, no per-token cost. The 256K context window means it can handle large codebases or long documents without the context chunking that smaller-window models require.

Practical upgrade list: pull the Gemma 4 12B checkpoint from Hugging Face and run it through LM Studio or Ollama on a laptop with 16GB VRAM; compare one coding task output against your current local model; test the 256K context on a long codebase or document understanding task; and use Google AI Edge for the managed local deployment path if you prefer a one-command install.

[42:00] Kimi Code CLI — TypeScript-native terminal coding agent with native MCP support

Moonshot AI released Kimi Code CLI on June 5, 2026 as an MIT-licensed open-source terminal AI coding agent written in TypeScript. The project is the successor to the older kimi-cli and is distributed via npm or a single install script that needs no Node.js pre-installed. On macOS or Linux: `curl -fsSL https://code.kimi.com/kimi-code/install.sh | bash`. On Windows: `irm https://code.kimi.com/kimi-code/install.ps1 | iex`. The global npm install requires Node.js 24.15.0 or later.

Kimi Code CLI reads and edits code, runs shell commands, searches files, fetches web pages, and chooses its next step based on feedback — the standard coding agent loop. Out of the box it works with Moonshot AI's Kimi models and can be configured to use other compatible providers. The feedback-driven execution model runs read-only operations automatically and asks for confirmation on file edits or shell commands — an approval flow that keeps risky actions under developer control.

Notable features include a fast TUI ready in milliseconds, video input for dropping screen recordings into chat, AI-native MCP configuration via `/mcp-config`, subagents for parallel work (coder, explore, and plan subagents in isolated contexts), and lifecycle hooks for gating tool calls, auditing decisions, or triggering notifications. The MCP configuration via `/mcp-config` is the feature that ties it to the agent stack: you can add and authenticate MCP servers from inside the CLI without external configuration files.

Version 0.11.0 published June 5, 2026. The project has 1,902 GitHub stars and active development.

Practical upgrade list: install Kimi Code CLI and verify with `kimi --version`; connect it to your Kimi API key or Moonshot AI OAuth; test one MCP server configuration via `/mcp-config`; run one subagent in parallel against a codebase task; and compare execution quality against your current CLI agent.

[50:00] A2A Protocol v1.0 — the formal agent interoperability layer

The Agent-to-Agent Protocol reached v1.0 in 2026 under the Linux Foundation, establishing a formal specification for how agents from different frameworks discover each other, establish communication channels, and delegate tasks. The protocol defines "agent cards" — JSON capability manifests — for agent discovery, and a task-based state machine for long-running interactions using JSON-RPC 2.0. Originally launched by Google, A2A is now governed by the Linux Foundation alongside MCP.

The MCP versus A2A distinction is the key mental model: MCP standardizes how an agent connects to external tools, databases, and data sources — it is about what an agent can do. A2A standardizes how agents communicate with each other — it is about how agents work together. MCP is already widely adopted in the agent stack. A2A v1.0 is the complementary protocol that will enable cross-framework agent handoff without custom integration code for every pair.

The a2aproject/A2A repository has 24,153 stars and active development as of June 6, 2026. For the agent stack, A2A v1.0 is the interoperability layer that will let a Claude Code session delegate to a Hermes agent, or an OpenClaw agent hand off to a Codex thread — without building a custom integration for each pair. The protocol has reached sufficient maturity that builders should be aware of it when designing multi-agent workflows.

Practical upgrade list: read the A2A v1.0 specification on the a2aproject/A2A GitHub repo to understand agent card structure and task state machine semantics; if you are building a multi-agent workflow, design the agent handoff points with A2A agent cards in mind; and test one cross-framework agent delegation if you have two different agent runtimes available.

[58:00] Practical queue

For Hermes Agent, download the desktop app installer and run it against your existing gateway; test OAuth remote connect if you have a hosted Hermes; explore the web admin panel to audit MCP servers and credentials. For Codex, upgrade to rust-v0.137.0 and test multi-agent v2 runtime choice persistence across a spawn and resume cycle. For Claude Code, add `fallbackModel` to your config with two or three alternatives; test the glob `"*"` deny rule for full tool lockout. For Gemma 4 12B, pull the checkpoint from Hugging Face and run it on a 16GB VRAM machine; compare one coding task against your current local model. For Kimi Code CLI, install it and connect one MCP server via `/mcp-config`. For A2A, read the v1.0 spec and identify one multi-agent handoff point in your workflow where A2A agent cards could replace a custom integration.
```

---

## Chapters

- 00:00 — Intro: Hermes v0.16.0 desktop app, Codex 0.137, Claude Code 2.1.167, Gemma 4 12B, project radar
- 02:00 — Hermes Agent v0.16.0: native desktop app, OAuth remote connect, and web admin panel
- 16:00 — Codex rust-v0.137.0: multi-agent v2, parallel web search, and enterprise controls
- 26:00 — Claude Code 2.1.166/2.1.167: fallback model chains and glob tool-name deny rules
- 34:00 — Gemma 4 12B: encoder-free multimodal model in the 16GB VRAM sweet spot
- 42:00 — Kimi Code CLI: TypeScript-native terminal coding agent with native MCP support
- 50:00 — A2A Protocol v1.0: the formal agent interoperability layer
- 58:00 — Practical queue

---

## Primary Links

- Hermes Agent v0.16.0: see Hermes Agent v0.16.0 story above
- Codex rust-v0.137.0: https://github.com/openai/codex/releases/tag/rust-v0.137.0
- Claude Code changelog: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
- Claude Code npm: https://www.npmjs.com/package/@anthropic-ai/claude-code
- Gemma 4 12B: https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12B/
- Kimi Code CLI: https://github.com/MoonshotAI/kimi-code
- A2A Protocol: https://github.com/a2aproject/A2A
- awesome-ai-agents-2026: https://github.com/Zijian-Ni/awesome-ai-agents-2026

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.1`, published 2026-06-03T19:35:12Z from GitHub releases. Recent episode version tags detected: `v2026.6.1`. No new stable release available. `v2026.6.2-beta.1` is a prerelease and excluded from stable coverage.
- **Hermes Agent** — Latest stable verified: `v2026.6.5` / `v0.16.0`, published 2026-06-06T00:55:58Z from GitHub releases. Recent episode version tags detected: `v2026.5.29.2`. Selected missing version: `v2026.6.5`.
- **OpenAI Codex app/CLI** — Latest stable verified: `rust-v0.137.0`, published 2026-06-04T01:17:20Z from GitHub releases. Recent episode version tags detected: `rust-v0.135.0`. Selected missing version: `rust-v0.137.0`.
- **Claude Code CLI** — Latest npm `latest` verified: `2.1.167`, published 2026-06-06; npm `stable` dist-tag verified as `2.1.153`. Recent episode version tags detected: `2.1.165`. Selected missing versions from npm `latest`: `2.1.166`, `2.1.167`.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags. Latest build as of 2026-06-06. Antigravity CLI launched May 19, 2026 at Google I/O as the successor to Gemini CLI. No version-tagged releases tracked to date.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.1`
- **Hermes Agent** — `v2026.6.5`
- **OpenAI Codex** — `rust-v0.137.0`
- **Claude Code CLI** — `2.1.167` (npm latest) / `2.1.153` (npm stable)
- **Antigravity CLI** — Continuous delivery (launched 2026-05-19)
