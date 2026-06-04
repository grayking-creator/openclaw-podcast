# AgentStack Daily EP063 — OpenClaw v2026.6.1, Claude Code 2.1.162, Qwen 3.7 Max/Plus, and Agent Memory Infrastructure

**Title:** OpenClaw v2026.6.1, Claude Code 2.1.162, Qwen 3.7 Max/Plus on the Agent Frontier, and Persistent Memory for Every Coding Agent

**Tagline:** OpenClaw v2026.6.1 ships Workboard orchestration, a governed Skill Workshop, and SQLite-backed state recovery. Claude Code 2.1.162 adds waiting-for visibility and permission-rule fixes. Qwen 3.7 Max and Plus split the coding and multimodal lanes. agentmemory gives every agent on your machine a shared memory surface.

**Feed description:** OpenClaw v2026.6.1 brings Workboard multi-agent orchestration, Skill Workshop governance, SQLite-backed channel recovery, and MiniMax M3 provider support. Claude Code 2.1.162 adds `waitingFor` JSON visibility and permission-rule fixes. Qwen 3.7 Max and Plus split the coding-reasoning and multimodal-vision lanes. agentmemory gives every agent on your machine a shared persistent context layer.

---

## Story Slate

1. **OpenClaw v2026.6.1 ships Workboard orchestration, Skill Workshop, SQLite-backed recovery, and provider expansion** — OpenClaw v2026.6.1 landed June 3, 2026 as the latest stable release. Workboard is the headline addition — a multi-agent planning and run-tracking surface with orchestration primitives, task-backed board runs, and task comments in the edit modal. It is the most concrete step OpenClaw has taken toward being a coordination layer rather than a single-agent runtime. A kanban board in Workboard drives actual task decomposition with agent coordination tools for multi-agent planning and run tracking. Skill Workshop adds governed skill authoring to the Control UI with proposal lists, today actions, revision handoff, searchable file previews, review states, locale coverage, and reusable session routing. The skill_workshop agent tool can apply, reject, and quarantine explicit proposals through a guarded review flow; proposals can carry approved support files with scanner, hash, and rollback safeguards; pending proposals can be revised in place with versioned, dated frontmatter. The skill_workshop agent tool is now part of the OpenClaw agent toolset — an agent can initiate a skill proposal, get it reviewed, and have it approved within the OpenClaw runtime without external tooling. Skill Workshop guidance also surfaces in Codex app-server prompts when skill_workshop is available.

Agent and CLI runtime recovery is the third major improvement. Tool calls that get interrupted, stale session bindings, compaction handoffs, and media delivery retries all recover more cleanly across five pull requests. Provider and plugin request paths bound timers, retries, OAuth and device-code lifetimes, media downloads, local service probes, and generated-content polling paths so they cannot hang a run indefinitely. iMessage monitor state, inbound queues, and plugin install ledgers moved to SQLite-backed storage — the plugin install index now persists in SQLite so installed package lookup survives reloads with less filesystem scanning. iOS adds hosted push relay defaults, realtime Talk playback, and a guarded WebSocket ping path for more reliable mobile sessions under variable network conditions. Channel and mobile delivery across Telegram, WhatsApp, iMessage, Slack, Discord, Microsoft Teams, Google Chat, Google Meet, and iOS realtime Talk is steadier with fixes to inbound queues and push relay.

Provider expansion adds MiniMax M3 to the model registry with its 1,000,000-token context window, sparse attention (MSA) architecture, multimodal capabilities, MiniMax Code, and full API availability — OpenClaw-managed agents can route to it through the standard provider interface without custom configuration. Account OAuth endpoints are now included in provider metadata for more complete OAuth flows. Google and Vertex catalog fixes address model browsing and credential-aware catalog loading. OpenRouter now uses SQLite for model metadata caching, meaning catalog state survives restarts and avoids repeated network calls for catalog metadata. Copilot Claude 1M capabilities are recognized. Foundry reasoning alignment addresses reasoning models through Microsoft's Foundry endpoint. OpenAI response replay guards protect against non-deterministic replay edge cases. Skills, session metadata, gateway runtime state, plugin metadata, memory watchers, and store writes do less repeated work on hot paths. Code mode adds internal namespaces for scoped agent and global sessions with exact namespace tool dispatch, plus MCP API files and docs for code-mode integrations.

Technical depth angle: explain Workboard orchestration primitives and task-backed board runs, Skill Workshop proposal/review/rollback flow and skill_workshop agent tool behavior, SQLite-backed iMessage and plugin install ledger recovery, bounded retry and timer semantics for provider and plugin request paths, MiniMax M3 provider registration with MSA for the 1M context window, OpenRouter SQLite model caching behavior, Copilot Claude 1M recognition, and why SQLite-backed state recovery matters for local monitor restarts.

Actionability angle: upgrade OpenClaw to v2026.6.1; open one Workboard, create a task, and verify board state persists across a gateway restart; open Skill Workshop, create one test proposal, and trace the apply/reject flow; verify one channel send (Telegram or Discord) survives a mid-delivery interrupt; check one provider config for MiniMax M3 or OpenRouter SQLite model caching.

Listener hook: OpenClaw is no longer just the runtime — Workboard and Skill Workshop make it the coordination and governance surface for multi-agent work on your machine.

2. **Claude Code 2.1.162 adds waiting-for JSON visibility, Remote Control footer, and permission-rule fixes** — Claude Code's npm `latest` is now 2.1.162, published June 3, 2026. The version range from EP059's 2.1.157 baseline to 2.1.162 includes five releases with concrete operator-visible changes. The most useful new behavior is `claude agents --json` now including a `waitingFor` field showing what a waiting session is blocked on — for example a permission prompt. This makes it possible to build operator tooling that diagnoses why a background agent is stalled without opening the session. Previously, background session stalls were opaque. `/effort` now confirms when the chosen level persists as the default for new sessions. Remote Control shows as a persistent footer pill with a session link instead of a startup message that scrolls away. The Windsurf-to-Devin rebrand is reflected in `/ide`, `/terminal-setup`, and `/scroll-speed`. A silent startup hang when the config directory is read-only or unwritable is fixed — Claude Code now starts with in-memory config and surfaces the error.

WebFetch permission rules now take precedence over preapproved-host auto-allow for explicit deny/ask/allow rules. Windows permission rules now match correctly when spelled with backslashes or case-variant paths, and Read deny rules no longer hide files from Glob and Grep results. An interrupt sent at the very start of a turn in stream-json or SDK sessions is no longer silently dropped. API 400 `no low surrogate in string` errors for classifier side-queries and MCP server descriptions with emoji near truncation boundaries are fixed. MCP per-server timeout config values below 1000ms no longer floor to a 1-second watchdog — sub-1000ms values fall through to the default or `MCP_TOOL_TIMEOUT`, and `claude mcp get` annotates them accordingly. The LSP tool's `workspaceSymbol` operation now accepts a query parameter and passes it to the language server. Several `claude agents` UI issues are resolved: status detail no longer truncates at 60–120 columns on wide terminals, long session names no longer truncate at 40 columns, attach no longer bounces back to the session list on the first try after a background-service restart, Ctrl+V image paste works in the dispatch input and session reply box, and backgrounding with ← no longer silently loses the conversation when the background service cannot start. Failed turns now show a compact warning line instead of a multi-line red error block. Quieter startup groups notices by severity and session info and announcements share a single line per launch.

Technical depth angle: explain waiting-for JSON field semantics and when it appears, permission rule precedence (explicit domain deny/ask/allow vs preapproved-host auto-allow), MCP timeout flooring behavior and why sub-1000ms values now fall through, interrupt handling at turn start in stream-json sessions, LSP workspaceSymbol query parameter contract, and the background service startup race condition that caused ← loses to be fixed.

Actionability angle: upgrade Claude Code to 2.1.162; run `claude agents --json` on one background session and check `waitingFor`; verify one MCP server timeout config below 1000ms is annotated and not flooring to 1 second; test WebFetch explicit domain deny rules against a preapproved host; attach to a background session, interrupt it at the very start of a turn, and verify it shows Interrupted feedback.

Listener hook: five Claude Code releases between 2.1.157 and 2.1.162, but the one you will use every day is `waitingFor` in `claude agents --json` — finally you can see why a background agent is stuck without opening it.

3. **Qwen 3.7 Max and Plus split the coding-reasoning and multimodal-vision lanes** — Qwen 3.7 shipped May 19, 2026 in two distinct variants that matter for different agent workflows. Qwen 3.7 Max targets reasoning, coding, and math — the same lane as Codex, Claude Code, and other coding-focused models. Qwen 3.7 Plus is more optimized for multimodal and vision tasks. The split mirrors the broader industry pattern of differentiated model sizes for different task profiles, but Qwen's open-weight position makes both variants deployable locally on suitable hardware. Qwen 3.7 ships as an agent frontier model — Qwen's own blog frames it as designed for agentic workflows, not just chat completion. The context window and tool-use capabilities are positioned for agent-computer use cases rather than single-turn completion. On OpenRouter, both variants are available through the API. For local deployment, Qwen 3.7 quantizations are available through Ollama, LM Studio, and similar tools. LM Studio's mlx-engine has explicit optimizations for the Qwen 3.5/3.6 family; the 3.7 release suggests those optimizations carry forward for Apple Silicon developers running locally. NVIDIA's DGX Spark messaging highlights Qwen 3.5 optimizations as part of the local agent stack story, which suggests the 3.7 family will follow the same deployment path for local agent computers.

Technical depth angle: explain Qwen 3.7 Max vs Plus capability differentiation, agentic workflow positioning vs single-turn chat, local deployment options (Ollama, LM Studio, llama.cpp), context window and tool-use design for agent-computer use cases, and where the multimodal Plus variant differs architecturally from the Max variant.

Actionability angle: pick one Qwen 3.7 variant based on your primary task — Max for coding and reasoning, Plus for multimodal and vision; try it on OpenRouter API to verify behavior; if running locally, pull a Qwen 3.7 quantization through Ollama or LM Studio and compare code generation quality against your current coding agent model.

Listener hook: Qwen 3.7 is not one model — Max and Plus split the job. If you are routing between coding and multimodal tasks, the naming tells you which lane each variant is built for.

4. **agentmemory gives every coding agent on your machine a shared persistent context layer** — agentmemory is a persistent memory system for AI coding agents that positions itself as the shared memory layer across every agent you run locally. Its stated goal is straightforward: no more re-explaining your project to every new session. The system works with Claude Code, Codex CLI, GitHub Copilot CLI, Cursor, Gemini CLI, Hermes, OpenClaw, pi, OpenCode, and any MCP client — making it one of the most breadth-compatible memory tools in the agent tooling space. The system is built on the iii engine and installs as a global npm package (`@agentmemory/agentmemory`). Once installed, the memory server runs on port 3111. It connects to agents via native plugins, hooks, or MCP — with Claude Code getting native plugin plus 12 hooks plus MCP, Codex getting native plugin plus 6 hooks plus MCP, and OpenClaw and Hermes both getting native plugin plus MCP. All connected agents share the same memory server, which means one agent can write context that another agent reads in a subsequent session. The feature set includes confidence scoring on stored memories, lifecycle management, knowledge graph representation, and hybrid search across stored context. A real-time viewer and an iii Console are included. Agent-specific wiring covers the major players with per-agent connect commands. The repo is actively maintained with recent commits in early June 2026.

Technical depth angle: explain the iii engine architecture and how the shared memory server works across multiple agent types, confidence scoring and lifecycle management for stored memories, knowledge graph representation in the memory layer, hybrid search implementation, and why shared cross-agent memory changes multi-agent workflows on the same machine where different agents work on the same codebase.

Actionability angle: install agentmemory with `npm install -g @agentmemory/agentmemory`; run `agentmemory demo` to seed sample sessions; connect it to your primary coding agent (Claude Code, Codex, or Hermes) with the agent-specific connect command; verify recall across two sessions — write a memory in session one, close the agent, open session two, and query the same memory.

Listener hook: every agent on your machine is starting from a blank slate. agentmemory changes that — one memory server, shared across every agent, so context from last week's work survives into this week's session.

5. **CodeGraphContext v0.4.13 turns any repo into a queryable graph database via CLI or MCP** — CodeGraphContext is an MCP server and CLI toolkit that indexes local code into a graph database to provide context to AI assistants. Version 0.4.13 is the current release. It works in two modes: as a standalone CLI for developers who want to query a code graph directly, and as an MCP server that AI agents like Claude Code, Codex, Gemini, Cursor, and others can call to get code structure answers without guessing from raw text. The indexing engine parses code using tree-sitter nodes and builds a graph of components — functions, classes, methods, parameters, inheritance relationships, function calls, and imports. The CLI mode lets developers run natural language queries against the graph. The MCP mode exposes tools like `get_callers`, `get_callees`, `get_class_hierarchy`, and `get_call_chain` through the MCP protocol. Live file watching (`codegraphcontext watch`) updates the graph in real time as files change. Pre-indexed bundles let you load famous repositories instantly without indexing. Supported languages cover 22 programming languages including Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Dart, Perl, Lua, Scala, Haskell, Elixir, HTML, CSS, and TSX. Multiple graph database backends are supported — FalkorDB Lite (default), KuzuDB, LadybugDB, FalkorDB Remote, Nornic DB, or Neo4j — all available via Docker or native. The dual-mode design means a developer can index a codebase once and use the same graph both from the CLI for manual exploration and from within an AI agent via MCP. Agents that use CodeGraphContext can answer structural questions — who calls this function, what is the class hierarchy, where does this import come from — without guessing from raw text. The graph reduces tool call overhead on larger codebases where a text search would need to run across dozens of files.

Technical depth angle: explain tree-sitter parsing for graph extraction, the dual CLI/MCP architecture, how MCP tools expose graph queries (get_callers, get_callees, class_hierarchy, call_chain), live file watching for incremental graph updates, pre-indexed bundle format and loading, and multi-backend graph storage (FalkorDB, KuzuDB, Neo4j).

Actionability angle: install with `pip install codegraphcontext`; run `codegraphcontext index` on one repo; try a natural language query from the CLI like "what functions call the authentication function?"; connect it to your agent via MCP and ask the same question through the agent to compare the answers.

Listener hook: agents that search code by grepping files get fooled by same-name functions across different classes. CodeGraphContext indexes the actual graph — callers, callees, inheritance, call chains — so your agent knows the difference before it edits.

6. **RepoBrain gives coding agents a lightweight decision and pattern memory layer** — RepoBrain is a lightweight, CLI-first memory system designed specifically for coding agents to remember decisions, patterns, and project state across long-running sessions. It is designed for Claude Code, Codex, and other agents that need to preserve decision context without the overhead of heavier memory systems. RepoBrain focuses on decision recall and pattern storage — when an agent makes a choice about how to solve a problem or structure code, that decision gets stored so a subsequent session can query it and avoid re-debating the same points. The CLI-first design means it runs as a local service without requiring external infrastructure. Agent-specific wiring covers Claude Code and Codex for drop-in integration. The lightweight focus makes it suitable for developers who want memory without the full feature set of larger systems like agentmemory.

Technical depth angle: explain the lightweight memory architecture and how decision storage differs from full knowledge-graph approaches, CLI-first design constraints and what they sacrifice for simplicity, agent-specific wiring for Claude Code and Codex, and how pattern recall changes the context-window efficiency of long-running agent sessions.

Actionability angle: install RepoBrain, run one session with a decision log on a coding problem, then query that decision in a follow-up session to verify the pattern survived context window compaction.

Listener hook: if you have ever had an agent re-solve a problem you already solved last week, RepoBrain is the lightweight fix — decision memory without the full system overhead.

---

## Model Discovery Check

**Lane: OpenRouter / Open-Source / Agent-Focused Models**

Recent episode model coverage detected:
- MiniMax M3 (open-weight, 1M context, MSA/sparse attention, multimodal, MiniMax Code, coding/agentic)
- Opus 4.8 (Anthropic, coding agent model)
- GPT-5.5 (OpenAI)
- Gemini 3.x (Google)

Newly discovered models post-last-update:
- **Qwen 3.7 Max** — Provider: Alibaba Qwen / Qwen Team. Release date: May 19, 2026. Availability: API (OpenRouter, Qwen API), open weights (HuggingFace, Ollama, LM Studio). Architecture: dense transformer, agentic workflow design, long context. Primary source: https://qwen.ai/blog?id=qwen3.7. Decision: **SELECTED** — splits the coding-reasoning lane clearly (Max) from multimodal-vision (Plus), open-weight availability enables local deployment, agentic positioning is directly relevant to the agent stack audience.
- **Qwen 3.7 Plus** — Provider: Alibaba Qwen / Qwen Team. Release date: May 19, 2026. Availability: API (OpenRouter, Qwen API), open weights. Architecture: dense transformer, multimodal optimization. Decision: **SELECTED** — paired with Max as the multimodal counterpart, both variants are on the agent frontier, Plus targets vision tasks that matter for agents that work with documents, screenshots, and diagrams.
- **Microsoft Phi Silica** — Existing on-device Windows component, latest KB update is version 1.2603.373.0. Built for Intel Copilot+ PCs as a compact 3.3B parameter SLM. Decision: **NOT SELECTED** — on-device Windows component, not an API or open-weight model relevant to the agent stack audience; KB updates are patches, not a new model release.

---

## GitHub Project Radar

- **agentmemory** — https://github.com/rohitg00/agentmemory — Persistent shared memory for AI coding agents. GitHub API check on 2026-06-04 showed active development (updated 2 days ago). Built on the iii engine; works with Claude Code, Codex, Copilot CLI, Cursor, Gemini CLI, Hermes, OpenClaw, pi, OpenCode via native plugins, hooks, and MCP. Stack improvement angle: gives every agent on your machine a shared context layer so project knowledge persists across sessions without re-explaining. Try now: install with `npm install -g @agentmemory/agentmemory`, run `agentmemory demo`, connect to your primary agent with the agent-specific connect command, and verify recall across two sessions.

- **CodeGraphContext** — https://github.com/CodeGraphContext/CodeGraphContext — MCP server plus CLI that indexes local code into a graph database for AI agents. Version 0.4.13. Supports 22 languages via tree-sitter parsing; works as standalone CLI and MCP server. Stack improvement angle: gives agents actual call-graph and inheritance data instead of guessing from text search, especially where same-name functions appear in different classes. Try now: `pip install codegraphcontext && codegraphcontext index <repo>` then ask a natural language query about callers or call chains via CLI or MCP.

- **RepoBrain** — https://github.com/bartolli/repo-brain — Lightweight CLI-first memory system for coding agents. Designed for Claude Code, Codex, and other agents to remember decisions, patterns, and project state. Stack improvement angle: lightweight alternative to heavier memory systems, focused on decision and pattern recall for long-running agent sessions. Try now: install and run one session with a decision log, then query it in a follow-up session to verify the decision survived context window compaction.

---

## Extra Research Candidates

- **Codex rust-v0.138.0-alpha.1** — Primary source: https://github.com/openai/codex/releases/tag/rust-v0.138.0-alpha.1. Technical depth angle: alpha release featuring argument-comment-lint, bwrap sandboxing tool, and multi-platform asset binaries; worth watching for the stable tag but not ready for public release coverage.
- **OpenAI workspace-agent policy controls** — Primary source: OpenAI workspace-agent release notes (May 2026). Technical depth angle: explain admin controls for agent publishing, Slack agent follow-up message behavior, guided setup improvements, and app action safeguards for workspace agents.
- **NVIDIA DGX Spark as agent computer** — Primary source: NVIDIA GTC material, DGX Spark product pages. Technical depth angle: explain 128GB unified memory configuration, Nemotron 3 Super 120B open model positioning, Qwen 3.5 optimization path, and how DGX Spark changes local agent hardware requirements.

---

## Show Notes

```md
Episode 63 — June 4, 2026

[00:00] Episode hook

OpenClaw v2026.6.1, Hermes Agent v2026.5.29.2, and Claude Code 2.1.162 drop in the same episode window. The stable OpenClaw tag is v2026.6.1, the Hermes stable tag stays at v2026.5.29.2, and the latest Claude Code npm `latest` is 2.1.162. OpenClaw v2026.6.1 ships Workboard orchestration, a governed Skill Workshop, SQLite-backed state recovery, and MiniMax M3 provider support. Claude Code 2.1.162 adds waiting-for visibility in `claude agents --json` and a batch of permission and interrupt fixes across five releases from 2.1.158 to 2.1.162. Qwen 3.7 Max and Plus split the coding-reasoning and multimodal-vision lanes. agentmemory makes every agent on your machine share a persistent context layer. This is a 60-minute episode — keep the existing builder stories and extend runtime.

[02:00] OpenClaw v2026.6.1 deep dive — Workboard, Skill Workshop, SQLite recovery, and provider expansion

OpenClaw v2026.6.1 landed June 3, 2026 and is the main episode block. The headline addition is Workboard — a multi-agent planning and run-tracking surface with orchestration primitives, task-backed board runs, and task comments in the edit modal. Workboard is not just a task list; it is a full coordination surface that can drive task decomposition and worktree-per-task execution with the right agent wiring. The key shift is that OpenClaw moves from a single-agent runtime toward a multi-agent coordination layer. A kanban board in Workboard is not just status tracking — it drives actual task decomposition with agent coordination tools for multi-agent planning and run tracking.

Skill Workshop adds governed skill authoring to the Control UI. Proposals flow through apply/reject/quarantine controls with rollback metadata. Support files under standard skill folders get scanner, hash, and rollback safeguards. The skill_workshop agent tool is now part of the OpenClaw agent toolset — an agent can initiate a skill proposal, get it reviewed, and have it approved all within the OpenClaw runtime without external tooling. The skill_workshop agent tool can apply, reject, and quarantine explicit proposals through the guarded review flow. Proposals can carry approved support files under standard skill folders with scanner, hash, and rollback safeguards. Pending proposals can be revised in place with versioned, dated proposal frontmatter before approval. The Skill Workshop guidance also surfaces in Codex app-server prompts when skill_workshop is available, which means Codex can prompt for skill governance at the right moment in a run. The Control UI now has a fuller Skill Workshop flow with proposal lists, today actions, revision handoff, searchable file previews, review states, locale coverage, and reusable session routing.

Agent and CLI runtime recovery is the third major improvement area. Tool calls that get interrupted, stale session bindings, compaction handoffs, and media delivery retries all recover more cleanly. The fixes cover interrupted tool calls, stale session bindings, compaction handoffs, and media delivery retries across five pull requests. Provider and plugin request paths bound more timers, retries, OAuth and device-code lifetimes, media downloads, local service probes, and generated-content polling paths before they can hang a run.

iMessage monitor state, inbound queues, and plugin install ledgers moved to SQLite-backed state so restarts recover without duplicate filesystem scanning. The plugin install index is now persisted in SQLite so installed package lookup survives reloads with less filesystem scanning. iOS adds hosted push relay defaults, realtime Talk playback, and a guarded WebSocket ping path for more reliable mobile sessions under variable network conditions. Channel and mobile delivery across Telegram, WhatsApp, iMessage, Slack, Discord, Microsoft Teams, Google Chat, Google Meet, and iOS realtime Talk is steadier with fixes to inbound queues and push relay.

Provider expansion adds MiniMax M3 to the model registry with its 1,000,000-token context window, sparse attention (MSA) architecture, multimodal capabilities, MiniMax Code, and full API availability — OpenClaw-managed agents can route to it through the standard provider interface without custom configuration. Account OAuth endpoints are now included in provider metadata for more complete OAuth flows. Google and Vertex catalog fixes address model browsing and credential-aware catalog loading. OpenRouter now uses SQLite for model metadata caching, which means catalog state survives restarts and avoids repeated network calls for catalog metadata. Copilot Claude 1M capabilities are recognized. Foundry reasoning alignment addresses reasoning models through Microsoft's Foundry endpoint. OpenAI response replay guards protect against non-deterministic replay edge cases. Skills, session metadata, gateway runtime state, plugin metadata, memory watchers, and store writes do less repeated work on hot paths. Code mode adds internal namespaces for scoped agent and global sessions with exact namespace tool dispatch, plus MCP API files and docs for code-mode integrations.

Practical upgrade list: open one Workboard, create a task, and verify board state persists across a gateway restart; run one Skill Workshop proposal through apply and review; verify one interrupted tool call recovers cleanly; check one channel delivery (Telegram or Discord) survives a mid-delivery interrupt; confirm one provider path (MiniMax M3 or OpenRouter) loads correctly; and test iOS Talk playback with the new guarded WebSocket ping path.

[26:00] Claude Code 2.1.162 — waitingFor JSON, permission rules, MCP timeout fixes, and interrupt handling

Claude Code 2.1.162 is five releases past the EP059 baseline of 2.1.157. The most operator-relevant change is `claude agents --json` now showing a `waitingFor` field — it tells you why a background session is stalled, whether it is a permission prompt or another blocker. This makes it possible to build monitoring tooling that diagnoses stalls without requiring a human to attach and inspect.

WebFetch permission rules are now explicit — deny and ask rules take precedence over preapproved-host auto-allow, which closes a gap where a domain could be in the preapproved list and still have explicit rules that should have blocked it. Windows path handling for backslashes and case-variant paths is fixed — Read deny rules now actually hide files from Glob and Grep results. MCP timeout configs below 1000ms no longer floor to 1 second and abort every tool call; they fall through to the default or `MCP_TOOL_TIMEOUT`, and `claude mcp get` annotates them accordingly. The interrupt-at-turn-start fix closes a gap in stream-json and SDK sessions where an Esc pressed immediately after sending a prompt would silently drop the turn and leave it running with no feedback.

`/effort` now confirms when the chosen level persists as the default for new sessions. Remote Control shows as a persistent footer pill with a session link — it no longer appears as a startup message that scrolls away. The Windsurf-to-Devin rebrand is reflected in `/ide`, `/terminal-setup`, and `/scroll-speed`. A silent startup hang when the config directory is read-only or unwritable now shows a diagnostic instead of a blank screen. Quieter startup groups notices by severity and session info and announcements share a single line per launch.

The LSP tool's `workspaceSymbol` operation now accepts a query parameter and passes it to the language server. API 400 `no low surrogate in string` errors for classifier side-queries and MCP server descriptions with emoji near truncation boundaries are fixed. Several `claude agents` UI issues are resolved: status detail no longer truncates at 60–120 columns on wide terminals, long session names no longer truncate at 40 columns, attach no longer bounces back to the session list on the first try after a background-service restart, Ctrl+V image paste works in the dispatch input and session reply box, and backgrounding with ← no longer silently loses the conversation when the background service cannot start. Failed turns now show a compact warning line instead of a multi-line red error block.

Practical test list: run `claude agents --json` on a background session and check `waitingFor`; verify WebFetch explicit deny behavior; test one MCP server with a timeout below 1000ms and confirm it is annotated in `claude mcp get`; send an interrupt at the very start of a turn in a stream-json session and verify Interrupted feedback.

[40:00] Qwen 3.7 Max and Plus — coding-reasoning vs multimodal-vision split on the agent frontier

Qwen 3.7 landed May 19, 2026 as two distinct variants. Max targets reasoning, coding, and math — the same lane as Codex and Claude Code's primary models. Plus targets multimodal and vision tasks. Both are open-weight and available through OpenRouter API and local deployment tools. Qwen's agentic positioning means the models are designed for tool use and agent-computer interaction, not just single-turn completion.

For OpenClaw, Codex, and Claude Code operators, Qwen 3.7 Max is a routing option for coding-heavy workloads. For agents that need to handle images, documents, and visual inputs, Qwen 3.7 Plus fills a different lane than the pure coding models. The split matters for model routing decisions — you pick based on whether the task is primarily code generation or multimodal understanding.

Try it: pull a Qwen 3.7 quantization through Ollama or LM Studio and compare code generation quality against your current coding agent model. For multimodal tasks, try Qwen 3.7 Plus through OpenRouter API with a document or image input.

[51:00] agentmemory — shared persistent context for the full agent stack

agentmemory solves the blank-slate problem across every agent you run. When Claude Code, Codex, Hermes, and OpenClaw all share the same memory server on port 3111, context from last week's work survives into this week's session. The system uses the iii engine, installs as a global npm package, and connects via native plugins, hooks, or MCP depending on the agent.

The most concrete use case is a developer who works on a codebase across multiple agents — Claude Code for high-level refactoring, Codex for shell and file operations, Hermes for orchestrating multi-step tasks. Without a shared memory layer, each agent starts cold. With agentmemory, the context from Claude Code's last session informs what Codex does next.

Install, run the demo, connect to your agent, and verify recall across two sessions.

[61:00] CodeGraphContext v0.4.13 — code graphs for agents and developers

CodeGraphContext indexes code into a graph database and exposes the graph through both a CLI and an MCP server. The dual-mode design means one index serves both human exploration and agent tool calls. The indexing engine parses code using tree-sitter nodes and builds a graph of components — functions, classes, methods, parameters, inheritance relationships, function calls, and imports. The CLI mode lets developers run natural language queries against the graph. The MCP mode exposes tools like `get_callers`, `get_callees`, `get_class_hierarchy`, and `get_call_chain` through the MCP protocol. Live file watching updates the graph in real time as files change. Pre-indexed bundles let you load famous repositories instantly without indexing. The graph reduces tool call overhead on larger codebases where a text search would need to run across dozens of files. Connect it to your agent and ask the same question through the MCP interface to compare the agent's answer against what you got from the CLI.
```

---

## Chapters

- 00:00 — Intro: OpenClaw v2026.6.1, Claude Code 2.1.162, Qwen 3.7, agentmemory
- 02:00 — OpenClaw v2026.6.1 deep dive: Workboard, Skill Workshop, agent recovery, channel stability, provider expansion
- 26:00 — Claude Code 2.1.162: waitingFor JSON, permission rules, MCP timeout fixes, interrupt handling
- 40:00 — Qwen 3.7 Max and Plus: coding-reasoning vs multimodal-vision split, open-weight availability, agentic positioning
- 51:00 — agentmemory: shared persistent context across Claude Code, Codex, Hermes, OpenClaw, and more
- 61:00 — CodeGraphContext v0.4.13: code graphs via CLI and MCP for agents and developers
- 71:00 — RepoBrain: lightweight decision memory for long-running agent sessions

---

## Primary Links

- OpenClaw v2026.6.1: https://github.com/openclaw/openclaw/releases/tag/v2026.6.1
- Claude Code changelog: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
- Claude Code npm: https://www.npmjs.com/package/@anthropic-ai/claude-code
- Hermes Agent v2026.5.29.2: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.29.2
- Codex releases: https://github.com/openai/codex/releases
- Qwen 3.7: https://qwen.ai/blog?id=qwen3.7
- agentmemory: https://github.com/rohitg00/agentmemory
- CodeGraphContext: https://github.com/CodeGraphContext/CodeGraphContext

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.1`, published 2026-06-03T19:35:12Z from GitHub releases. Recent episode version tags detected: `v2026.5.27`. Selected missing version: `v2026.6.1`.
- **Hermes Agent** — Latest stable verified: `v2026.5.29.2` / `v0.15.2`, published 2026-05-29T13:37:26Z from GitHub releases. Recent episode version tags detected: `v2026.5.29.2` (EP059). No new stable release since EP059.
- **OpenAI Codex app/CLI** — Latest stable verified: `rust-v0.135.0`, published 2026-05-28T17:31:35Z from GitHub releases. Recent episode version tags detected: `rust-v0.135.0` (EP059). No stable release since EP059. A prerelease alpha tag (rust-v0.138.0-alpha.1) is visible and excluded.
- **Claude Code CLI** — Latest npm `latest` verified: `2.1.162`, published 2026-06-03; npm `stable` dist-tag remains `2.1.152`. Recent episode version tags detected: `2.1.157` (EP059). Selected missing versions: `2.1.158`, `2.1.159`, `2.1.160`, `2.1.161`, `2.1.162`.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags. Latest build as of 2026-06-04. Antigravity CLI launched May 19, 2026 at Google I/O as the successor to Gemini CLI. No version-tagged releases tracked in prior episodes.

---

## Harness Version Reference

| Harness | Latest Version | Source |
|---------|---------------|--------|
| OpenClaw | `v2026.6.1` | GitHub releases |
| Hermes Agent | `v2026.5.29.2` | GitHub releases |
| OpenAI Codex | `rust-v0.135.0` | GitHub releases |
| Claude Code CLI | `2.1.162` (npm latest) / `2.1.152` (npm stable) | npm registry |
| Antigravity CLI | Continuous delivery (launched 2026-05-19) | antigravity.google |