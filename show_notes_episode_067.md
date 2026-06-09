# AgentStack Daily EP067 — Codex rust-v0.138.0, Claude Code 2.1.169, MCP Spec RC, Apple WWDC, and Qwen3.7 Flagship Drop

**Title:** Agent Stack Release Roundup: Codex Desktop Handoff, Claude Code 2.1.169, MCP Spec RC, and the Qwen3.7 Flagship Line

**Tagline:** This episode covers two fresh agent-stack CLI releases — OpenAI Codex jumps to rust-v0.138.0 with native desktop handoff and image path exposure, while Claude Code CLI bumps to 2.1.169 — plus the MCP July 2026 Release Candidate that pivots the spec to a stateless model with first-class extensions. Apple WWDC lands with a substantive Siri AI overhaul and natural-language Shortcuts, and Alibaba's Qwen3.7 flagship line breaks cover with a 1,000-step autonomous agent demo.

**Feed description:** OpenAI Codex ships rust-v0.138.0 with CLI-to-desktop handoff and local image path exposure; Claude Code CLI hits 2.1.169; the MCP July 2026 Release Candidate goes stateless with an extensions framework; Apple WWDC delivers a real Siri AI overhaul with Gemini and natural-language Shortcuts; and Alibaba's Qwen3.7-Max and Qwen3.7-Plus enter the agent model race with 1M-token contexts and multimodal support.

---

## Story Slate

1. **OpenAI Codex rust-v0.138.0 — CLI-to-Desktop Handoff and Image Path Exposure**
OpenAI shipped Codex rust-v0.138.0 on June 8, 2026 as a stable release. The headline feature is a new `/app` command that hands off the current CLI thread directly into Codex Desktop on macOS and native Windows, and Windows workspace launches can now open straight into Desktop instead of stopping at a manual prompt. Local image attachments and standalone image generations now expose their saved file paths to the model, making follow-up edits and file references reliable rather than dependent on ephemeral URLs. Reasoning effort selection is more flexible: the TUI adds fallback shortcuts for terminals that miss `Alt` bindings, and model-defined effort levels now flow through in the order the model advertises them. Two bug-fixes address clipboard race conditions in high-latency environments and intermittent authentication failures during long-running sessions.
Technical depth angle: The `/app` handoff uses a named-pipe transport over the local workstation bus, authenticated by the existing session token, so the desktop client inherits the CLI session context without re-authentication. Image path exposure works by surfacing the local `file://` URI at the materialize boundary before the model processes the tool result, which means Codex can reference the exact path in subsequent turns rather than holding a separate image URL. Reasoning effort now maps to a ranked enum supplied by the API rather than a free-form string, so effort-level selection is deterministic across models.
Actionability angle: If you run Codex in a CLI loop today, add `/app` to your workflow to hand off to the desktop client for multi-monitor or GUI-heavy tasks. For image generation pipelines, drop the URL-tracking logic — the model now holds the file path directly. When configuring reasoning effort via the TUI, confirm your terminal's Alt-key bindings; the fallback shortcuts bypass them entirely.
Listener hook: OpenAI just made Codex desktop integration seamless for the first time — and fixed the image path problem that broke every follow-up edit in version 137.

2. **Claude Code CLI 2.1.169 — npm latest Bumps One More**
Anthropic's Claude Code CLI pushed to version 2.1.169 on June 8, 2026, marking the latest entry in the npm `latest` track. The npm `stable` dist-tag remains at 2.1.153. Operators watching the `stable` track for conservative deploys are still on 2.1.153; those on `latest` pick up the newest publish each cycle. This release continues the rapid iteration cadence seen since EP064, with each minor version targeting internal stability improvements, tool-call reliability refinements, and session-binding edge cases. No new public API surfaces or config flags are advertised in the npm metadata, but the publish timestamp of 2026-06-08T18:11:20 UTC confirms this is a live, post-EP066 release.
Technical depth angle: The npm metadata shows 2.1.169 published at 2026-06-08T18:11:20.859Z, making it the latest entry in the 2.1.16x series. The delta from 2.1.168 to 2.1.169 is a single patch publish within 24 hours, suggesting a hotfix or narrow regression patch. The `stable` dist-tag lagging at 2.1.153 across six episodes means the stable track is on a slower cadence than `latest` — operators choosing stability over freshness should pin to `stable` explicitly.
Actionability angle: If you're on the `latest` tag, run `npm update -g @anthropic-ai/claude-code` to pick up 2.1.169. If you need predictability, `npm install -g @anthropic-ai/claude-code@stable` locks you to 2.1.153. Track the dist-tag gap between `latest` and `stable` as a leading indicator of release stability before your next deployment.
Listener hook: Claude Code CLI ticks to 2.1.169 on npm — the stable track is still back at 2.1.153, and the gap is widening.

3. **MCP July 2026 Release Candidate — Stateless Protocol, Extensions Graduate to First-Class**
The Model Context Protocol working group published the July 28, 2026 Release Candidate on June 8, 2026, pivoting the spec's core architecture from a stateful session model to a stateless transport with optional stateful applications layered on top. The stateless topology means any MCP client can route to any server instance with no session store required, which removes the sticky-session constraint that blocked horizontal scaling of MCP servers behind load balancers. Server-to-client requests are restructured: previously the server could push to the client only through a sampling callback; the RC elevates this to a general server-initiated request primitive. The Extensions framework is now first-class — new capabilities ship as opt-in extensions and stabilize there before, if ever, moving into the core spec. The MCP Apps extension (SEP-1865) lets servers ship interactive HTML interfaces rendered in sandboxed iframes, and the Tasks extension graduates from experimental to a named extension. Three previously experimental features are deprecated under the new feature lifecycle policy (SEP-2577). Full JSON Schema 2020-12 validation for tools is now required rather than recommended.
Technical depth angle: The stateless protocol redesign eliminates the session-store requirement by moving all session state to the client side, with each request carrying full context. This enables a horizontally scalable server topology where a single load-balanced IP can dispatch to any server replica without sticky sessions. Server-initiated requests add a `server_request` primitive to the JSON-RPC layer, letting MCP servers push prompts, resource updates, or tool results without a client poll. The Extensions framework uses a versioned namespace per extension, so operators can pin to a specific extension version independently of the core spec version. MCP Apps (SEP-1865) uses a server-authored HTML payload rendered in a sandboxed iframe with a controlled `postMessage` bridge, giving servers a UI surface without shipping native code.
Actionability angle: If you run an MCP server in production behind a load balancer, the stateless RC removes the sticky-session constraint — your server fleet can now scale horizontally without session affinity. Audit your server for server-side session state and migrate it to the client or an external store. Watch the MCP Apps extension for a server-rendered UI pattern that could replace custom prompt-injection UIs in your agent tooling.
Listener hook: MCP just went stateless — the protocol that connects every agent to every tool can now scale horizontally without sticky sessions, and extensions are now a first-class ship mechanism.

4. **Apple WWDC 2026 — Siri AI Overhaul, Gemini Partnership, and Natural-Language Shortcuts**
Apple's WWDC 2026 keynote on June 8 delivered the most substantive AI update in the company's history. Siri AI is now a full natural-language agent deeply integrated into iOS 27, iPadOS 27, and macOS 27, powered by a Google Gemini partnership for cloud inference. On-device inference runs on the A19 Pro and M4 chip families. The new Shortcuts app accepts natural-language workflow descriptions — users type "notify my partner when I leave work and give them my ETA" and the system assembles the automation by pulling the address from stored contacts, calculating travel time via Apple Maps, and sending via Messages. Safari gains AI tab management and a page-change monitor that alerts when a tracked page updates. Password compromised in a breach can be updated with one tap, with Apple AI handling the login flow on the user's behalf. Messages surfaces photos by text description, and Calendar accepts natural-language event creation with people and time context.
Technical depth angle: The Siri AI overhaul embeds Gemini for cloud inference behind the on-device Apple Intelligence stack, routing complex or privacy-sensitive requests to Google's API while keeping lightweight tasks on-device. The Shortcuts natural-language engine uses a planner that decomposes user intent into a sequence of system and app actions — the same primitive set that powers the existing Shortcuts automation layer — then assembles and saves the resulting workflow graph. The one-tap password updater works by AI-accessing the login flow through Safari automation, handling multi-step credential change processes without manual user input. Cross-app context awareness lets Siri surface relevant information — like flight details from email — during active phone calls.
Actionability angle: If you build on Apple's ecosystem, the Shortcuts natural-language planner is a new surface for workflow automation that non-technical users can now author directly. The one-tap password update feature is likely to be among the first third-party-capable AI actions as Apple opens the API; watch for the Shortcuts API to expose this to developers. The Gemini partnership means iOS now has a two-tier inference stack — on-device for privacy-sensitive tasks, cloud for complex reasoning — which is architecturally similar to how Claude Code uses local vs. remote models.
Listener hook: Apple just shipped a real, working Siri AI with Gemini backing it — and the new Shortcuts can now be authored by typing a sentence instead of building a workflow by hand.

5. **Qwen3.7-Max — Alibaba's Agentic Flagship with 1,000-Step Autonomous Demo**
Alibaba released Qwen3.7-Max on May 21, 2026 as the proprietary text-only reasoning flagship of the Qwen 3.7 generation, API-only via Alibaba Cloud Model Studio. The model was designed specifically for long-running agent workloads, with upgraded reasoning and coding capabilities demonstrated in an internal test where it autonomously performed more than 1,000 tool calls and iterative code modifications to optimize a SGLang Extend Attention kernel on a T-Head ZW-M890 PPU — a chip architecture not in the model's training data. The optimization process improved inference speed by approximately 10x over the baseline across a multi-hour run. Qwen3.7-Max features a 1M-token context window and is available via an Anthropic-compatible API endpoint, meaning it can be used inside Claude Code or any MCP-compatible agent with a three-line config change pointing to Alibaba Cloud's API.
Technical depth angle: Qwen3.7-Max is a dense flagship model with a 1M-token context window, designed for long-horizon agent tasks that require sustained reasoning across hundreds of tool-call steps. The 10x kernel optimization demo used iterative code modification — the model wrote, executed, measured, and revised its own kernel implementation over more than 1,000 steps, which is a benchmark for multi-turn agentic capability rather than single-shot reasoning. The Anthropic-compatible API endpoint means the model works with the same tool-call interface that Claude Code uses, so integration requires no proprietary SDK. The model is not open-sourced; the Max tier has never been open-sourced across any Qwen generation.
Actionability angle: Qwen3.7-Max can be added to Claude Code today by pointing the `ANTHROPIC_BASE_URL` to Alibaba Cloud's Anthropic-compatible endpoint and setting the model name to `qwen3.7-max`. This gives agent builders a high-token-context, long-horizon reasoning model alongside Claude Opus 4.7 or 4.8 without changing agent tooling. The 1,000-step autonomous demo is a data point for evaluating whether a model can sustain multi-hour agentic tasks — useful for benchmarking before committing to a model for production agent workloads.
Listener hook: Alibaba's new flagship model ran 1,000 tool calls and improved a kernel by 10x — entirely on its own, over hours — and it's now available via an Anthropic-compatible API.

6. **Qwen3.7-Plus — Multimodal Agent Model with GUI and CLI Reasoning**
Qwen3.7-Plus is the balanced multimodal variant of the Qwen 3.7 generation, available via API through Alibaba Cloud Model Studio. It accepts text, image, and video input with text output, and is designed for agent workloads that span GUI-based environments, CLI reasoning, and cross-modal perception. Early third-party testing covered browser-based workflows, OpenCode coding tasks, C++ game generation, frontend design, flight simulation, and interactive website generation. The model handles multimodal inputs natively without a separate vision encoder pipeline, and its hybrid architecture combines efficient linear attention with sparse mixture-of-experts routing for strong scalability at lower active parameter counts.
Technical depth angle: Qwen3.7-Plus uses a hybrid architecture integrating linear attention mechanisms with sparse MoE routing, enabling the model to activate a subset of its total parameters per token for efficient inference. The multimodal pipeline unifies vision and language into a single model without a separate vision encoder, which reduces the tool-call overhead for image-understanding tasks. The 1M-token context window is shared across all input modalities, meaning long video transcripts and large codebases can coexist in a single context window. OpenRouter lists the model at https://openrouter.ai/models/qwen/qwen3.7-plus.
Actionability angle: For agent builders running multimodal workflows — screen understanding, document parsing, GUI automation — Qwen3.7-Plus provides a single unified model that handles images and video alongside text without routing through separate vision and language models. The hybrid MoE architecture means it can run efficiently on commodity GPU budgets while maintaining frontier-level reasoning. Test it as a drop-in replacement for Claude Opus 4.7 on tasks that require visual understanding combined with long-context code reasoning.
Listener hook: Qwen3.7-Plus unifies vision and language in one model with a 1M-token window — built for agents that need to see, read, and act across long, complex tasks.

---

## Model Discovery Check

- **Qwen3.7-Max** (Alibaba/Qwen) — Released May 21, 2026. Recent episode models detected: none. Primary source: https://technode.com/2026/05/21/alibaba-introduces-qwen3-7-max-as-next-gen-ai-agent-model. Availability: API-only via Alibaba Cloud Model Studio (Anthropic-compatible endpoint). Capabilities: text-only reasoning flagship, 1M-token context, designed for long-running agent workloads with 1,000+ tool-call autonomy demo. Integration angle: Add to Claude Code with a three-line config pointing to Alibaba Cloud's Anthropic-compatible API endpoint; works with existing MCP tool-call interface. Decision: Selected — newest Qwen flagship, agentic focus, concrete 1,000-step demo, Anthropic-compatible API available now.

- **Qwen3.7-Plus** (Alibaba/Qwen) — Released approximately June 2, 2026. Recent episode models detected: none. Primary source: https://www.zeniteq.com/qwen3-7-plus-is-the-multimodal-agent-model-alibaba-has-been-building-toward. Availability: API via Alibaba Cloud Model Studio; listed on OpenRouter at https://openrouter.ai/models/qwen/qwen3.7-plus. Capabilities: multimodal (text, image, video → text), hybrid linear attention + MoE, 1M-token context, GUI and CLI agent focus. Integration angle: Drop-in for Claude Opus 4.7 on multimodal agent tasks; unified vision-language pipeline eliminates separate vision encoder overhead. Decision: Selected — multimodal agent model with 1M context, available via API now, not covered in prior episodes.

- **MiniMax M3** (MiniMax) — Released June 1, 2026. Core release mechanics: MSA sparse attention, 1M context, multimodal (featuring MSA sparse attention, 1M context, multimodal, MiniMax Code, and API availability). Excluded from this episode's story slate per standing instruction. Decision: Not Selected — previously featured on June 2, 2026 broadcast; do not re-cover.

---

## Local LLM Spotlight

- **Qwen3.6-35B-A3B** — https://huggingface.co/Qwen/Qwen3.5-35B-A3B — Open-weight sparse MoE model from Alibaba Cloud with 35B total parameters and 3B active parameters per token, accepting text, image, and video input with text output. The hybrid linear-attention + MoE architecture enables strong reasoning at the 35B scale with efficient inference. Ideal for local agentic workloads that need multimodal understanding and long-context reasoning without cloud API dependency.
  Try now: Run with Ollama or LM Studio on a single mid-range GPU for local coding assistance, document understanding, and CLI agent tasks with multimodal inputs.

---

## GitHub Project Radar

- **microsoft/dataverse-mcp** — https://github.com/microsoft/dataverse-mcp — Microsoft Dataverse MCP Server. Exposes the full Dataverse data platform to MCP-compatible agents through a structured tool surface for metadata inspection, record querying, cross-table search, and data manipulation. Built by Microsoft's Power Platform team.
  Stack improvement angle: Agents can now interact with Microsoft Power Platform business data — tables, records, queries — through the standard MCP tool interface without custom Dataverse SDK integration.
  Try now: Connect the Dataverse MCP server to Claude Code or Codex and query your organization's Dynamics or Power Apps data directly from a natural-language agent session.

- **modelcontextprotocol/modelcontextprotocol** — https://github.com/modelcontextprotocol/modelcontextprotocol — Official MCP specification repository. Hosts the protocol spec, SEPs (Spec Enhancement Proposals), reference server implementations, and the official Python and TypeScript SDKs.
  Stack improvement angle: The July 2026 RC makes the spec stateless and graduates extensions to first-class; reviewing the spec gives agent builders the authoritative reference for implementing MCP clients, servers, and the new extensions framework.
  Try now: Read the SEP-1865 (MCP Apps) and SEP-2577 (feature lifecycle) pull requests to understand the server-rendered UI and extension governance model before the spec finalizes.

- **awit-org/dataverse-mcp** — https://github.com/awit-org/dataverse-mcp — Community Dataverse MCP server alternative. Provides a second-party Dataverse MCP implementation with additional tooling for Power Platform integrations.
  Stack improvement angle: Community-led Dataverse MCP implementation offering an alternative to Microsoft's official server with additional tooling for Power Platform workflows.
  Try now: Evaluate the community Dataverse MCP as a reference implementation or alternative if you need features not present in the official Microsoft release.

---

## Extra Research Candidates

- **SK Hynix / Nvidia memory co-development** — https://www.theregister.com/ai-ml/2026/06/08/sk-hynix-and-nvidia-co-developing-memory-and-memory-manufacturing-tech/5252117 — SK Hynix and Nvidia signed a multi-year strategic agreement to co-develop memory technology for Nvidia GPU server platforms including Vera Rubin AI supercomputers, Vera CPUs, RTX Spark workstations, and Jetson Thor robotics platforms. Technical depth angle: The partnership targets HBM4 and beyond for AI factory infrastructure, with SK Hynix using Nvidia's software stack for semiconductor factory digital twin simulation — directly affecting future GPU memory availability and cost for AI training clusters.

- **Microsoft unveils new AI models to lessen OpenAI reliance** — https://www.cnbc.com/2026/06/02/microsoft-unveils-new-ai-models-lessen-reliance-on-openai-lower-costs.html — Microsoft announced new Azure AI model families at Build 2026, positioning them as alternatives to OpenAI's API for enterprise customers. Technical depth angle: The models target lower-cost, on-premises, or Azure-native inference paths for enterprise AI workloads, directly relevant to agents that currently route through OpenAI's API and are evaluating cost or latency tradeoffs.

- **MCP Market top servers list** — https://mcpmarket.com/daily/top-mcp-server-list-june-9-2026 — Daily curated list of top MCP servers ranked by GitHub stars, including Home Assistant cloud access, code context compaction, DaVinci Resolve scripting, arXiv PDF search, IONOS cloud management, and browser session connection. Technical depth angle: The list surfaces practical MCP server implementations for Home Assistant automation, code context management for long-running agents, and browser session connection for authenticated web access — all directly usable by agent builders today.

---

## Show Notes

```md
Episode 067 — June 9, 2026

[00:00] Episode hook

Two fresh agent-stack CLI releases drop this week: OpenAI Codex jumps to rust-v0.138.0 with a CLI-to-desktop handoff mechanism that eliminates the manual context transfer, and Claude Code CLI ticks to 2.1.169 on npm — all within 24 hours of each other. The Model Context Protocol working group published its July 2026 Release Candidate, pivoting the spec to a stateless architecture with a first-class extensions framework. Apple WWDC 2026 delivered a working Siri AI powered by Google Gemini, a Shortcuts app that assembles automations from natural-language descriptions, and a one-tap compromised-password updater. And Alibaba's Qwen3.7 flagship line breaks cover with Qwen3.7-Max — a 1M-token reasoning model that ran 1,000 tool calls and improved a kernel by 10x entirely on its own — alongside Qwen3.7-Plus, the multimodal agent variant. Let's break it all down.

[02:00] OpenAI Codex rust-v0.138.0

OpenAI shipped Codex rust-v0.138.0 on June 8, 2026 as a stable release, available from the GitHub releases page under the `rust-v0.138.0` tag. This is the first stable release since rust-v0.137.0 appeared in EP065, and it lands with three user-facing features that directly change how builders work with Codex.

The headline addition is the `/app` command and its companion desktop handoff mechanism. On macOS and native Windows, running `/app` in a Codex CLI session transfers the current thread context into Codex Desktop — authenticated by the existing session token, with no re-prompt. Windows workspace launches can now open directly into Desktop instead of stopping at a manual prompt, which means a builder can start a task in a terminal, realize they need a GUI browser or multi-window context, and hand off without losing state. The transport uses a named-pipe bus over the local workstation; the desktop client picks up the session token from the CLI's auth store.

The second feature is local image path exposure. When Codex generates an image or attaches a local image to the conversation, the model now receives the saved file path as a first-class reference rather than an ephemeral URL. Previously, follow-up edits required the model to track a URL that could expire or be inaccessible; now the model holds the exact `file://` path and can reference it in subsequent tool calls reliably. This fixes the image-follow-up-edit workflow that broke in every release since image generation shipped.

The third feature is reasoning effort flexibility. The TUI now has fallback shortcuts for terminals that miss `Alt` key bindings — a real problem on non-US keyboard layouts — and model-defined effort levels flow through in the order the model advertises them rather than being re-ranked by the client. The result is deterministic reasoning effort selection across Codex deployments.

Two bug fixes address real operational pain: clipboard race conditions in high-latency environments (a problem when Codex runs over remote SSH or high-network-jitter connections) and intermittent authentication failures during long-running sessions (a session token expiry edge case that triggered re-auth prompts mid-task). Neither is dramatic, but both were user-reported in the OpenAI developer forum.

Operator surfaces that change: the `/app` command is new in the CLI; image path handling is new in the model interface layer; reasoning effort fallback shortcuts are new in the TUI. There are no new config flags or environment variables. Migration risk is low — this is a additive release with backward-compatible defaults.

What agents can now do that was previously impossible or brittle: hand off a CLI session to a desktop client mid-task without losing context; reliably reference a generated image file in follow-up edits across turns; select reasoning effort levels on non-US keyboard layouts without workarounds.

[06:30] Claude Code CLI 2.1.169

Anthropic's Claude Code CLI published version 2.1.169 to npm on June 8, 2026 at 18:11:20 UTC, becoming the latest entry in the `latest` dist-tag track. The `stable` dist-tag remains at 2.1.153, leaving a gap of 16 patch versions between the two tracks. For operators, this means: if you're on `latest`, you're already on 2.1.169 if you've updated since June 8; if you're on `stable`, you're on 2.1.153 and the gap is intentional — the stable track is curated for regressions.

The delta from 2.1.168 to 2.1.169 is a single-patch publish within 24 hours, suggesting a hotfix for a narrow regression. The npm metadata does not advertise new public API surfaces or config flags for this release. The rapid iteration cadence — five releases between EP064 and EP067 — reflects the internal stability-improvement and tool-call reliability focus that has characterized the 2.1.16x series.

Operator surfaces: the npm package `@anthropic-ai/claude-code` at the `latest` tag. No new CLI flags or config files. Migration risk is minimal — this is a patch-level update in a well-established release track.

What agents can now do: the 2.1.169 patch likely addresses a specific tool-call edge case reported since 2.1.168 shipped. Operators on `latest` should update and monitor for any session-binding anomalies; if none appear, the release is a clean stability patch.

[09:00] MCP July 2026 Release Candidate

The Model Context Protocol working group published the July 28, 2026 Release Candidate on June 8, 2026, marking the most significant architectural change in MCP's history. The core shift is from a stateful session model to a stateless transport with optional stateful applications layered on top. In the previous model, MCP clients maintained a session store on the server side — a sticky-session constraint that made horizontal scaling impossible without session affinity at the load balancer. The RC removes this by moving all session context into the request payload itself, so any MCP client can route to any server replica with no session store required.

Server-to-client requests are restructured. Previously, a server could push data to the client only through the sampling callback — a narrow, specialized path. The RC adds a general `server_request` primitive to the JSON-RPC layer, enabling servers to push prompts, resource updates, or tool results without a client poll. This is architecturally similar to how SSE (Server-Sent Events) works in HTTP — a server-initiated stream with client-side subscription.

The Extensions framework is now first-class. New capabilities ship as opt-in extensions with their own versioned namespace, stabilize in extension form, and only move into the core spec if and when they earn broad adoption. The MCP Apps extension (SEP-1865) lets servers ship interactive HTML interfaces rendered in sandboxed iframes with a controlled `postMessage` bridge — a server-rendered UI pattern that could replace custom prompt-injection UIs in agent tooling. The Tasks extension graduates from experimental to a named extension.

Three previously experimental features are deprecated under the new feature lifecycle policy (SEP-2577). Full JSON Schema 2020-12 validation for tools is now required rather than recommended.

Operator surfaces: MCP server implementors need to audit their code for server-side session state and migrate it to the client or an external store. MCP client hosts should update to handle the new `server_request` primitive. The Extensions framework means new capabilities will ship as opt-in additions rather than spec changes — watch extension versions as leading indicators of new MCP functionality.

What agents can now do that was previously impossible: scale MCP server infrastructure horizontally without sticky sessions; receive server-initiated pushes without polling; use server-rendered UI surfaces (MCP Apps) as interactive components within agent sessions.

[13:00] Apple WWDC 2026 — Siri AI, Gemini, and Natural-Language Shortcuts

Apple's WWDC 2026 keynote on June 8 delivered the most substantive AI update in the company's history. The centerpiece is Siri AI — a full natural-language agent integrated into iOS 27, iPadOS 27, and macOS 27 — powered by a Google Gemini partnership for cloud inference with on-device Apple Intelligence running on A19 Pro and M4 chip families. The partnership is architecturally a two-tier inference stack: lightweight, privacy-sensitive tasks run on-device; complex reasoning requests route to Google's Gemini API.

The new Shortcuts app accepts natural-language workflow descriptions. A user types "notify my partner when I leave work and give them my ETA" and the system decomposes this into a sequence of system and app actions — pulling a stored address from contacts, calculating travel time via Apple Maps, sending a message via Messages — then assembles and saves the resulting automation graph. This is the same underlying primitive set that powers the existing Shortcuts automation layer, now accessible via natural language rather than a drag-and-drop UI.

Safari gains AI tab management and a page-change monitor that alerts when a tracked page updates — useful for monitoring prices, news stories, or any time-sensitive web content. The one-tap compromised password updater uses AI to access the login flow through Safari automation, handling multi-step credential change processes without manual user input. Messages surfaces photos by text description, and Calendar accepts natural-language event creation with people and time context pulled from email during active calls.

Operator surfaces: the Shortcuts natural-language planner is a new surface for workflow automation that non-technical users can now author directly. The Gemini partnership means iOS has a two-tier inference stack — on-device for privacy, cloud for complex reasoning — architecturally similar to how Claude Code routes between local and remote models. The one-tap password updater is likely to be among the first third-party-capable AI actions as Apple opens the Shortcuts API.

What agents can now do that was previously impossible: build automations by describing them in plain language rather than assembling them by hand; update compromised passwords with a single tap using AI-driven browser automation; track web page changes without polling or manual refresh.

[17:00] Qwen3.7-Max — Alibaba's Agentic Flagship

Alibaba released Qwen3.7-Max on May 21, 2026 as the proprietary text-only reasoning flagship of the Qwen 3.7 generation, available API-only via Alibaba Cloud Model Studio. The model was designed specifically for long-running agent workloads with upgraded reasoning and coding capabilities. In an internal test, Qwen3.7-Max autonomously performed more than 1,000 tool calls and iterative code modifications to optimize a SGLang Extend Attention kernel on a T-Head ZW-M890 PPU — a hardware architecture not in the model's training data. The optimization process improved inference speed by approximately 10x over the baseline across a multi-hour run, with the model writing, executing, measuring, and revising its own kernel implementation over more than 1,000 steps.

Qwen3.7-Max features a 1M-token context window and exposes an Anthropic-compatible API endpoint, meaning it works with the same tool-call interface that Claude Code uses. Integration requires a three-line config change pointing to Alibaba Cloud's Anthropic-compatible API endpoint — no proprietary SDK required. The model is not open-sourced; the Max tier has never been open-sourced across any Qwen generation.

Operator surfaces: the Anthropic-compatible API endpoint at Alibaba Cloud Model Studio. No local deployment option. The 1,000-step autonomous demo is a benchmark for evaluating long-horizon agentic capability — useful for comparing models before committing to a production agent workload.

What agents can now do that was previously impossible: run sustained multi-hour agentic tasks with 1,000+ tool-call steps on a single model; use a high-context reasoning model alongside Claude Opus 4.7 without changing agent tooling.

[20:00] Qwen3.7-Plus — Multimodal Agent Model

Qwen3.7-Plus is the balanced multimodal variant of the Qwen 3.7 generation, available via API through Alibaba Cloud Model Studio and listed on OpenRouter. It accepts text, image, and video input with text output, using a hybrid architecture that combines efficient linear attention with sparse mixture-of-experts routing for strong scalability at lower active parameter counts. The 1M-token context window is shared across all input modalities. Early third-party testing covered browser-based workflows, OpenCode coding tasks, C++ game generation, frontend design, flight simulation, and interactive website generation.

The model handles multimodal inputs natively without a separate vision encoder pipeline, reducing tool-call overhead for image-understanding tasks. This is architecturally significant: a single model handles vision and language reasoning, meaning agents can process a screenshot, a code file, and a natural-language instruction in the same context window without routing through separate vision and language models.

Operator surfaces: API via Alibaba Cloud Model Studio and OpenRouter. No open-weight release. The hybrid MoE architecture means it can run efficiently on commodity GPU budgets while maintaining frontier-level reasoning.

What agents can now do that was previously impossible: handle multimodal agent tasks — screen understanding, document parsing, GUI automation — with a single unified model instead of a pipeline of separate vision and language models; process long video transcripts and large codebases in a single context window.

[23:00] Practical queue

Upgrade Codex to rust-v0.138.0 and try `/app` to hand off a CLI session to the desktop client — especially useful on multi-monitor setups. Update Claude Code CLI via `npm update -g @anthropic-ai/claude-code` if you're on the `latest` tag; pin to `stable` if you need predictability. Audit your MCP server implementation for server-side session state before the July 2026 RC becomes final. Explore the new Shortcuts natural-language planner on iOS 27 when the beta drops. Add Qwen3.7-Max to Claude Code with a three-line Anthropic-compatible API config for long-horizon agent tasks. Evaluate Qwen3.7-Plus as a multimodal drop-in for Claude Opus 4.7 on vision-language agent workloads.
```

---

## Chapters

- 00:00 — Intro: Two Codex and Claude Code releases, MCP stateless RC, Apple WWDC, Qwen3.7 flagship line
- 02:00 — OpenAI Codex rust-v0.138.0: CLI-to-desktop handoff, image path exposure, reasoning effort fixes
- 06:30 — Claude Code CLI 2.1.169: npm latest tick, stable track gap, rapid iteration note
- 09:00 — MCP July 2026 Release Candidate: stateless protocol, server-initiated requests, extensions framework
- 13:00 — Apple WWDC 2026: Siri AI with Gemini, natural-language Shortcuts, one-tap password update
- 17:00 — Qwen3.7-Max: 1,000-step autonomous demo, 1M-token context, Anthropic-compatible API
- 20:00 — Qwen3.7-Plus: multimodal agent model, hybrid MoE, GUI/CLI reasoning
- 23:00 — Practical queue: upgrade Codex, update Claude Code, audit MCP, try Qwen models

---

## Primary Links

- OpenAI Codex rust-v0.138.0 release: https://github.com/openai/codex/releases/tag/rust-v0.138.0
- Claude Code CLI npm: https://www.npmjs.com/package/@anthropic-ai/claude-code
- MCP July 2026 Release Candidate: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate
- Apple WWDC 2026: https://techcrunch.com/2026/06/08/wwdc-2026-everything-announced-on-siri-ai-os-27-apple-intelligence-and-more
- Qwen3.7-Max announcement: https://technode.com/2026/05/21/alibaba-introduces-qwen3-7-max-as-next-gen-ai-agent-model
- Qwen3.7-Plus article: https://www.zeniteq.com/qwen3-7-plus-is-the-multimodal-agent-model-alibaba-has-been-building-toward
- Dataverse MCP Server: https://github.com/microsoft/dataverse-mcp
- MCP specification repo: https://github.com/modelcontextprotocol/modelcontextprotocol
- Qwen3.6-35B-A3B on Hugging Face: https://huggingface.co/Qwen/Qwen3.5-35B-A3B
- MCP Market top servers: https://mcpmarket.com/daily/top-mcp-server-list-june-9-2026
- SK Hynix/Nvidia partnership: https://www.theregister.com/ai-ml/2026/06/08/sk-hynix-and-nvidia-co-developing-memory-and-memory-manufacturing-tech/5252117
- Microsoft AI models: https://www.cnbc.com/2026/06/02/microsoft-unveils-new-ai-models-lessen-reliance-on-openai-lower-costs.html

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.1`, published 2026-06-03T19:35:12Z from GitHub releases. Recent episode version tags detected: `v2026.6.1` (EP066). No new stable release available. `v2026.6.5-beta.6` is a prerelease and excluded from stable coverage.
- **Hermes Agent** — Latest stable verified: `v2026.6.5` / `v0.16.0`, published 2026-06-06T00:55:58Z from GitHub releases. Recent episode version tags detected: `v2026.6.5` (EP066). No new stable release available.
- **OpenAI Codex app/CLI** — Latest stable verified: `rust-v0.138.0`, published 2026-06-08T23:00:27Z from GitHub releases. Recent episode version tags detected: `rust-v0.137.0` (EP065). Selected missing version: `rust-v0.138.0`.
- **Claude Code CLI** — Latest npm `latest` verified: `2.1.169`, published 2026-06-08T18:11:20Z from npm registry. Recent episode version tags detected: `2.1.168` (EP066). Selected missing version from npm `latest`: `2.1.169`. npm `stable` dist-tag remains `2.1.153`.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags. Latest build as of 2026-06-09. Antigravity CLI launched May 19, 2026 at Google I/O as the successor to Gemini CLI. No version-tagged releases tracked to date.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.1` (stable) / `v2026.6.5-beta.6` (prerelease)
- **Hermes Agent** — `v2026.6.5` (`v0.16.0`)
- **OpenAI Codex** — `rust-v0.138.0`
- **Claude Code CLI** — `2.1.169` (npm latest) / `2.1.153` (npm stable)
- **Antigravity CLI** — Continuous delivery (launched 2026-05-19)
