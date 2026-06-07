# AgentStack Daily EP065 - Hermes Agent Desktop App, Codex Zero Point One Thirty Seven, Claude Code Two Point One, and Gemma 4 12B on the Local Stack

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: Today, the agent-harness surface is the headline. Hermes Agent zero point sixteen dropped "The Surface Release" — a real native Electron desktop app with OAuth remote connect, drag-and-drop file input, and a full browser-based administration panel shipped across 874 commits in a single release cycle. OpenAI Codex zero point one thirty seven added multi-agent v2 with runtime choice persistence per thread, parallel standalone web search, and monthly credit limit visibility in enterprise flows. Claude Code two point one point one sixty six introduced configurable fallback model chains of up to three models and glob tool-name deny rules, with two point one point one sixty seven following as the bug-fix polish release. After the harness updates, the model lane lands on Gemma 4 12B as Google's encoder-free multimodal release that fits in 16 gigabytes of VRAM. The project radar covers the A2A Protocol reaching v1.0 under the Linux Foundation, Kimi Code CLI as a TypeScript-native terminal coding agent, and the awesome-ai-agents-2026 curated resource list as the definitive index for what to read next.

[ALLOY]: The order this week puts the harness layer first because the surface area is what changed. The model story is strong, but the tooling that operators touch is where reliability gets built or broken. Hermes Agent just became an application your non-technical teammates will actually use. Codex is closing the gaps that make multi-agent sessions lose their place across a handoff. Claude Code can now chain fallback models so a saturating API does not stop an agent dead. And the model story that follows is a serious open-weight release for local-first agent stacks. [PAUSE]

## [00:00] Opening: harness updates, the model lane, and the project radar

[NOVA]: Three layers are moving at once, and the most useful way to listen is to keep them separate. The harness layer is what an agent runs on, and the agent-harness releases this cycle touched every primary surface that operators actually touch — desktop, terminal, fallback routing, and multi-agent handoff. The model layer is what determines the quality of what the agent produces. The tooling layer is the open-source project radar that fills in the gaps between the major releases.

[ALLOY]: Hermes Agent zero point sixteen is the headline harness release. It is the most surface-area-expanding release the project ships since it began, and the centerpiece is a real native cross-platform desktop app. That is not a wrapper around a terminal. That is not a browser tab pinned to a URL. That is an installer that drops a real chat window onto the dock or the taskbar.

[NOVA]: Codex zero point one thirty seven is the OpenAI CLI release, and the most architecturally meaningful change is multi-agent v2 with runtime choice persistence. The architecture detail matters. Each spawned thread now carries its own runtime choice forward. Spawned agents get cleaner follow-up and metadata defaults. That closes a class of bugs where a parent session hands off to a child and the child silently drops context.

[ALLOY]: Claude Code two point one point one sixty six adds a fallbackModel setting and glob tool-name deny rules. The fallback chain is the operator-facing feature. Configure up to three models in priority order and the runtime picks the next one when the primary is overloaded. Glob deny rules let you write a single rule that matches all tools, or a pattern that matches a subset.

[NOVA]: The model lane is Gemma 4 12B, a 12 billion parameter encoder-free multimodal model with a 256K context window, released under Apache 2.0 by Google on June 3, 2026. The architecture detail is the story. Vision and audio flow directly into the language model backbone rather than through a separate multimodal encoder, which is the design choice that lets a 12 billion parameter model handle multimodal input on 16 gigabytes of VRAM.

[ALLOY]: The project radar covers three items. A2A Protocol v1.0 reaches a formal milestone as the agent interoperability layer under the Linux Foundation, with agent cards for discovery and a JSON-RPC 2.0 task state machine. Kimi Code CLI is a TypeScript-native terminal coding agent with native MCP support and subagent parallel dispatch. Awesome-ai-agents-2026 is the curated index that surfaces MCP servers, agent frameworks, and protocols for the agent stack.

[NOVA]: The thread across the episode is the surface area. The harness layer is consolidating around native, multi-surface tools. The model layer is adding open-weight options for local-first workflows. The project radar is the connectivity layer that lets those tools talk to each other. [PAUSE]

## [02:00] Hermes Agent zero point sixteen: native desktop app, OAuth remote connect, and web admin panel

[NOVA]: Hermes Agent zero point sixteen is the release that changes how Hermes meets the developer. The headline is a real native Electron desktop application that installs like any other macOS, Linux, or Windows app, updates itself in place from inside the app, and gives you a proper chat window with streaming, a session list, drag-and-drop file input, clipboard image paste, a Cmd+K command palette, and a model picker right in the status bar.

[ALLOY]: If you have been telling non-technical teammates "it is a command line agent" and watching their eyes glaze over, you can now just send them an installer. The desktop app behaves like the tool they expect to find in their applications folder. The chat window streams responses. The session list archives and searches. Drag and drop a file into the chat area and the file is attached to the next message. Paste an image from the clipboard and it goes into the same attachment pipeline.

[NOVA]: The desktop app does not have to run Hermes locally. Point it at a remote Hermes gateway — your homelab, a hosted box, a teammate's server — and the app connects over a secure WebSocket, authenticating with OAuth or username and password. No fiddling with insecure flags or hand-copied session tokens. Each profile can target its own remote host, and you can run concurrent sessions across multiple profiles simultaneously.

[ALLOY]: That is the remote-connect story that enterprise and team Hermes deployments have been waiting for. The desktop app becomes a thin client to a shared gateway, which means a team can run a hosted Hermes instance and each developer runs their own native GUI. The authentication flow uses OAuth, so identity is delegated to whatever provider the team already runs. Username and password is the fallback for environments without an OAuth provider.

[NOVA]: The web dashboard grew a full browser-based administration panel. You get MCP catalog management, messaging channel configuration, credential storage, webhook management, memory configuration, and pluggable OIDC or username-password login — all from a browser without touching the command line. First-time setup now has a "Quick Setup via Nous Portal" path that gets you from install to first message in seconds, which matters for onboarding new users or evaluating Hermes in a fresh environment.

[ALLOY]: The default skill set was trimmed to what you actually need. NVIDIA skills joined the trusted Skills Hub taps. The model picker is now fuzzy-searchable everywhere — desktop, web, TUI, and command line — which sounds trivial until you have a long list of models and no search. Undo finally lets you take back the last N turns, which is the quality-of-life feature that users have requested since the first release.

[NOVA]: Under the hood, two priority zero and 62 priority one bug closures ride along. The security round is worth noting individually. A Starlette dependency was pinned to a fixed version, server-side request forgery off-loop hardening closes a class of attack vectors in plugin and provider request paths, and subprocess credential stripping ensures credentials do not leak into child process environments.

[ALLOY]: The practical signal is that Hermes just became an application your non-technical teammates will actually use. The native installer removes the largest single friction point for adoption. The OAuth remote connect removes the second friction point, which is the requirement that everyone run Hermes on their own machine. The web admin panel removes the third friction point, which is having to teach every operator the command line configuration surface.

[NOVA]: For the agent stack, the architectural takeaway is the surface area is now desktop-class. A real chat window with streaming. A real session list with archive. A real drag and drop. A real OAuth flow. The Electron wrapper pattern is not novel, but applying it to a multi-agent gateway with a thin-client profile model is a meaningful step. The desktop app can be installed on every developer machine and pointed at a shared gateway, which is the deployment model enterprise teams have been asking for. [PAUSE]

## [16:00] Codex zero point one thirty seven: multi-agent v2, parallel web search, and enterprise controls

[ALLOY]: OpenAI Codex zero point one thirty seven published on June 4, 2026 as the latest stable command line tag, two releases past the EP063 baseline of zero point one thirty five. The most architecturally significant change is multi-agent v2 with runtime choice persistence. Each spawned thread now carries its own runtime choice forward. Spawned agents get cleaner follow-up and metadata defaults. That means when a parent Codex session spawns a child agent, the child does not lose its place when the parent session hands off.

[NOVA]: The runtime choice persistence is the detail that matters. Before this release, a parent session would set the runtime for itself, spawn a child, and the child would fall back to the default runtime or the last runtime the parent used. After this release, the child thread carries its own runtime choice forward and gets cleaner follow-up defaults. The hand-off semantics are now thread-scoped, not process-scoped.

[ALLOY]: Function keys 13 through 24 are now supported in the TUI, and paste in searchable menus improve the terminal experience for power users who use extended keyboard layouts. Enterprise and admin flows now show monthly credit limits and can apply cloud-managed config bundles including education workspaces. The credit limit visibility closes a gap where operators could not see spend until the bill arrived.

[NOVA]: Plugin workflows gained machine-readable output and cached remote catalog suggestions. The machine-readable output means you can pipe plugin lists into scripts, continuous integration pipelines, or fleet management tooling without parsing human-readable text. Cached remote catalog suggestions speed up the plugin discovery flow by avoiding repeated network calls.

[ALLOY]: Hosted web and image tools are available in more code-mode flows, with standalone web searches now able to run in parallel. Parallel standalone web search means Codex can fire multiple search queries simultaneously and synthesize results rather than running them sequentially. That is a real latency win for research-heavy workflows where a single turn depends on five or six search results that previously had to be requested one at a time.

[NOVA]: Permission requests and approvals now carry environment identity, which closes a gap where a permission granted in one context could incorrectly apply across context boundaries. Platform reliability improved for macOS app launches and Windows SQLite startup, thread resume, and sandbox setup refreshes.

[ALLOY]: The architectural takeaway is that multi-agent orchestration in Codex is now a first-class surface. The runtime choice persistence is not a feature in the marketing sense. It is a correctness change. A child thread that loses its runtime choice can produce output that does not match the parent's intent, can fail to load a model, or can silently fall back to a default that the operator never authorized. Thread-scoped runtime choice closes that gap.

[NOVA]: The enterprise controls land at the same time as the architecture change, which is a deliberate pairing. Monthly credit limit visibility lets admins see spend before the bill arrives. Cloud-managed config bundles, including education workspaces, let a team apply a single configuration across a fleet. The operator signal is that Codex is moving from "CLI tool with a model picker" toward "fleet-managed agent runtime with credit accounting."

[ALLOY]: For teams running Codex in production, the practical move is to upgrade and run one multi-agent session to verify runtime choice persists correctly across spawn and resume. Run the machine-readable plugin list command to see the new output format. Test parallel web search in a code-mode flow. Check the new monthly credit limit display in any enterprise or admin flow you have access to.

[NOVA]: The key insight is that multi-agent v2 is the feature that makes agent spawning actually hold together across session boundaries. Runtime choice persistence is not glamorous, but it is the difference between an agent that holds context across a hand-off and one that drops it. The operator-visible win is that Codex multi-agent sessions no longer require babysitting through spawn and resume operations. [PAUSE]

## [26:00] Claude Code two point one point one sixty six and two point one point one sixty seven: fallback model chains and glob tool-name deny rules

[ALLOY]: Claude Code's npm latest is now two point one point one sixty six and two point one point one sixty seven, following two point one point one sixty five. Version two point one point one sixty six is the feature release with two operator-visible additions. The headline is a new fallbackModel setting that lets you configure up to three fallback models tried in order when the primary model is overloaded or unavailable.

[NOVA]: The fallback model flag now also applies to interactive sessions, not just background ones. That means interactive terminal sessions can also automatically roll over to the next model in the chain when the primary saturates. This changes how you handle model unavailability. Instead of a single prompt failing when an API is at capacity, Claude Code automatically tries the next model you configured.

[ALLOY]: Glob pattern support in deny rule tool-name positions is the second feature. Using a wildcard denies all tools. Allow rules reject non-MCP globs, and unknown tool names in deny rules now warn at startup rather than silently accepting malformed rules. The startup warning for unknown tool names is the operator-friendly improvement. You now know at startup if a deny rule is misconfigured rather than discovering it when the rule fails to fire.

[NOVA]: Version two point one point one sixty seven is pure bug fixes and reliability improvements — the hygiene wave that keeps the release train clean between feature releases. The fallback model chain is the operator-facing feature that changes how you handle model unavailability, and the runtime interaction with fleet compliance settings is worth understanding.

[ALLOY]: The fallback chain interacts with required minimum version and required maximum version fleet compliance settings in a clean way. A version gate stops the agent from starting if it falls outside the allowed range. The fallback chain picks the next available model when the primary is unavailable. The two settings compose: a fleet can pin a version range and define a fallback chain, and the runtime enforces both.

[NOVA]: The architectural signal is that Claude Code is treating model availability as a first-class operational concern. The fallback chain is not a workaround for a flaky API. It is a configuration primitive that lets an operator define a priority order across multiple model providers. The runtime tries the primary first, then the second, then the third, and the user does not see the difference except for the model name on the response.

[ALLOY]: The glob deny rule is the security surface improvement. A single rule with a wildcard pattern denies every tool. That is a useful primitive for sandboxed environments where the agent should not have access to anything, or for a temporary "lock the agent out" configuration during incident response. Allow rules rejecting non-MCP globs means a misconfiguration where an operator tries to glob across MCP and non-MCP tool names is caught at startup, not at the first tool call.

[NOVA]: For the agent stack, the practical move is to add a fallbackModel to your Claude Code config with two or three alternatives ordered by preference. Test the chain by temporarily making your primary model unavailable and verifying the fallback fires correctly. Use a wildcard in a deny rule to test full tool lockout. Verify that unknown tool names in deny rules produce startup warnings.

[ALLOY]: The key insight is that Claude Code can now chain fallback models so a saturating API does not stop your agent dead. Configure up to three models in priority order and the runtime picks the next one when the primary is overloaded. The operator does not have to write a wrapper script, retry logic, or a separate routing layer. The runtime owns the fallback contract.

[NOVA]: The version cadence is also worth noting. Two releases in quick succession — two point one point one sixty six as the feature release and two point one point one sixty seven as the bug-fix polish — is the kind of hygiene wave that keeps a release train clean. Feature releases land operator-visible changes. Bug-fix releases close the rough edges the operator-visible changes expose. The split keeps the changelog readable and the upgrade calculus simple. [PAUSE]
## [34:00] Gemma 4 12B: encoder-free multimodal model in the 16GB VRAM sweet spot

[NOVA]: Google released Gemma 4 12B on June 3, 2026 as an Apache 2.0 open-weight checkpoint with a 256K context window, designed to bring agentic multimodal intelligence directly to laptops for local workflows. The key architectural decision is encoder-free multimodal input. Vision and audio flow directly into the language model backbone rather than through a separate multimodal encoder.

[ALLOY]: That is the same architectural pattern that makes large multimodal models fit in smaller parameter counts. By removing the encoder overhead, the 12 billion parameter model can handle image and audio inputs without a separate processing stage that adds parameters and latency. The design choice is what makes 16 gigabytes of VRAM enough.

[NOVA]: Benchmark performance is described as nearing Google's 26 billion parameter model on advanced reasoning tasks, which would place a 12 billion parameter model competitive with models twice its size on the benchmarks that matter for agentic workflows. The agentic workflow positioning is explicit. Autonomous data processing, visual insights, and webpage building are listed as target use cases.

[ALLOY]: Google AI Edge provides the path for local deployment on laptop hardware with 16 and 32 gigabyte VRAM configurations. AI Edge is the managed local deployment surface that handles model loading, runtime optimization, and integration with the device stack. For teams that want a one-command install rather than a manual checkpoint pull, AI Edge is the entry point.

[NOVA]: For the agent stack, Gemma 4 12B is the most realistic open-weight 12 billion parameter model for local coding-agent use on consumer hardware. It changes what local-first agent workflows look like when the model and weights stay on your machine. No API latency. No data leaving your environment. No per-token cost.

[ALLOY]: The 256K context window means the model can handle large codebases or long documents without the context chunking that smaller-window models require. A 256K window is enough to hold a small to medium-sized repository in a single context, or a long document plus the conversation history plus the tool call results.

[NOVA]: The architectural takeaway is that encoder-free multimodal is the design pattern that lets a 12 billion parameter model do what older 26 billion parameter encoder-decoder models did. Removing the encoder stage reduces parameter count without sacrificing multimodal capability, because the language model backbone learns to handle vision and audio tokens directly.

[ALLOY]: The trade-off is that the language model backbone has to be trained on multimodal data from the start, which is a meaningfully more expensive training pipeline. The benefit is inference is faster, the model is smaller, and deployment is simpler. For local agent stacks, the inference speed and model size matter more than the training cost.

[NOVA]: For the agent stack, the practical move is to pull the Gemma 4 12B checkpoint from Hugging Face and run it through LM Studio or Ollama on a laptop with 16 gigabytes of VRAM. Compare one coding task output against your current local model. Test the 256K context on a long codebase or document understanding task. Use Google AI Edge for the managed local deployment path if you prefer a one-command install.

[ALLOY]: The key insight is that Gemma 4 12B is the first 12 billion class open-weight model from a major lab that Google says can run on your laptop and still do advanced reasoning. The encoder-free architecture is the trick that makes it fit in 16 gigabytes of VRAM. The 256K context window is the capability that makes it useful for real coding tasks on real codebases.

[NOVA]: The wider signal is that the gap between open-weight local models and closed-weight API models is closing. A 12 billion parameter model that approaches a 26 billion parameter model on advanced reasoning is a meaningful data point. Local-first agent workflows are no longer a compromise. They are a real option for production workloads that can fit a 12 billion parameter model on the available hardware. [PAUSE]

## [42:00] Kimi Code CLI: TypeScript-native terminal coding agent with native MCP support

[ALLOY]: Moonshot AI released Kimi Code CLI on June 5, 2026 as an MIT-licensed open-source terminal AI coding agent written in TypeScript. The project is the successor to the older kimi-cli and is distributed via npm or a single install script that needs no Node.js pre-installed. On macOS or Linux a single install command puts the binary on your path. On Windows an equivalent PowerShell command does the same.

[NOVA]: Kimi Code CLI reads and edits code, runs shell commands, searches files, fetches web pages, and chooses its next step based on feedback — the standard coding agent loop. Out of the box it works with Moonshot AI's Kimi models and can be configured to use other compatible providers. The feedback-driven execution model runs read-only operations automatically and asks for confirmation on file edits or shell commands.

[ALLOY]: That approval flow keeps risky actions under developer control. Read-only operations like searching files and fetching web pages run without interruption. Write operations like editing a file or running a shell command ask for confirmation. The agent proposes, the developer disposes.

[NOVA]: Notable features include a fast TUI ready in milliseconds, video input for dropping screen recordings into chat, AI-native MCP configuration via the mcp-config command, subagents for parallel work — coder, explore, and plan subagents in isolated contexts — and lifecycle hooks for gating tool calls, auditing decisions, or triggering notifications.

[ALLOY]: The MCP configuration via the mcp-config command is the feature that ties it to the agent stack. You can add and authenticate MCP servers from inside the CLI without external configuration files. The configuration is conversational. You ask the agent to add a server, it walks you through the authentication, and the server is live.

[NOVA]: Subagents for parallel work is the feature that changes what a single CLI agent can do. Coder subagents write code. Explore subagents navigate codebases. Plan subagents decompose tasks. Each runs in an isolated context, which means the parallel work does not contaminate the main session context.

[ALLOY]: Lifecycle hooks are the operator-facing feature. A hook can gate a tool call — the agent has to ask permission before running a shell command. A hook can audit a decision — every tool call is logged with the agent's reasoning. A hook can trigger a notification — a Slack message, an email, a webhook, when a specific event happens.

[NOVA]: Version zero point eleven was published on June 5, 2026. The project has 1,902 GitHub stars and active development. The TypeScript-native architecture is worth noting. The agent is written in TypeScript, distributed as a single binary or an npm package, and integrates with the npm ecosystem directly.

[ALLOY]: The architectural signal is that the TypeScript-native CLI coding agent pattern is a real category. Kimi Code CLI joins a small set of tools written in TypeScript that can be installed as a single binary without a runtime dependency. The benefit is faster cold start, smaller footprint, and easier distribution. The cost is that some TypeScript ecosystem choices are baked in.

[NOVA]: For the agent stack, the practical move is to install Kimi Code CLI and verify with the version flag. Connect it to your Kimi API key or Moonshot AI OAuth. Test one MCP server configuration via the mcp-config command. Run one subagent in parallel against a codebase task. Compare execution quality against your current CLI agent.

[ALLOY]: The key insight is that Kimi Code CLI is the TypeScript-native terminal coding agent that was missing from the stack. Written in TypeScript, distributed as a single binary, with native MCP support and subagents for parallel work. The feedback-driven execution model with explicit approval for risky operations is a design choice that fits the developer ergonomics the rest of the stack is converging toward.

[NOVA]: The wider signal is that the CLI coding agent space is segmenting by ecosystem. TypeScript-native agents for the npm and Node.js ecosystem. Python-native agents for the data science and machine learning ecosystem. Rust-native agents for the systems programming ecosystem. Each ecosystem gets the agent that fits its existing tooling and distribution model. [PAUSE]

## [50:00] A2A Protocol v1.0: the formal agent interoperability layer

[ALLOY]: The Agent-to-Agent Protocol reached v1.0 in 2026 under the Linux Foundation, establishing a formal specification for how agents from different frameworks discover each other, establish communication channels, and delegate tasks. The protocol defines "agent cards" — JSON capability manifests — for agent discovery, and a task-based state machine for long-running interactions using JSON-RPC 2.0.

[NOVA]: Originally launched by Google, A2A is now governed by the Linux Foundation alongside MCP. The MCP versus A2A distinction is the key mental model. MCP standardizes how an agent connects to external tools, databases, and data sources — it is about what an agent can do. A2A standardizes how agents communicate with each other — it is about how agents work together.

[ALLOY]: MCP is already widely adopted in the agent stack. A2A v1.0 is the complementary protocol that will enable cross-framework agent handoff without custom integration code for every pair. The distinction matters for builders. If you are wiring an agent to a database, you are using MCP. If you are wiring two agents to talk to each other, you are using A2A.

[NOVA]: An agent card is a JSON manifest that describes what an agent can do. The card includes the agent's identity, its capabilities, the protocols it speaks, the authentication mechanisms it supports, and the task types it accepts. When one agent wants to delegate work to another, it discovers the target agent's card and uses the card to figure out how to communicate.

[ALLOY]: The task state machine is the other half of the protocol. A long-running task has a defined lifecycle: submitted, working, input-required, completed, failed, cancelled. The state machine defines what each state means, what transitions are valid, and what data the agents exchange at each transition. The state machine is what makes a multi-agent workflow robust to partial failure.

[NOVA]: The a2aproject/A2A repository has 24,153 GitHub stars and active development as of June 6, 2026. For the agent stack, A2A v1.0 is the interoperability layer that will let a Claude Code session delegate to a Hermes agent, or an OpenClaw agent hand off to a Codex thread, without building a custom integration for each pair.

[ALLOY]: The architectural signal is that v1.0 formalization means the protocol is stable. Builders can adopt A2A without worrying that the next release will break their integration. The Linux Foundation governance adds a layer of vendor neutrality that makes enterprise adoption easier — no single company controls the protocol direction.

[NOVA]: The protocol has reached sufficient maturity that builders should be aware of it when designing multi-agent workflows. If you are building a workflow that involves more than one agent runtime, the question is no longer "should we use A2A" but "which version of A2A does each runtime speak."

[ALLOY]: For the agent stack, the practical move is to read the A2A v1.0 specification on the a2aproject/A2A GitHub repo to understand agent card structure and task state machine semantics. If you are building a multi-agent workflow, design the agent handoff points with A2A agent cards in mind. Test one cross-framework agent delegation if you have two different agent runtimes available.

[NOVA]: The key insight is that A2A v1.0 is the protocol that makes agent interoperability real. Agents from different frameworks can now discover each other and hand off work through a formal JSON-RPC 2.0 state machine, not custom glue code for every pair. The maturity of the protocol is the signal that the multi-agent ecosystem is ready to move past bespoke integrations.

[ALLOY]: The wider signal is that the protocol layer of the agent stack is starting to look like the protocol layer of the web. HTTP for transport. JSON-RPC for message format. Agent cards for discovery. Task state machines for long-running interactions. The protocols are simple, composable, and vendor-neutral. That is the design pattern that lets an ecosystem grow.

[NOVA]: The combination of A2A for inter-agent communication and MCP for tool integration is the protocol stack that the agent ecosystem is converging toward. The two protocols solve different problems and they compose cleanly. An agent that speaks A2A can discover and delegate to other agents. An agent that speaks MCP can connect to external tools. An agent that speaks both can do both. [PAUSE]

## [58:00] Practical queue and closing

[ALLOY]: The practical queue is what moves from listening to acting. For Hermes Agent, download the desktop app installer for your operating system and run it against your existing local or remote gateway. Test OAuth login against a remote gateway if you have a hosted Hermes. Explore the new web admin panel to audit MCP servers, messaging channels, and credentials. Run Quick Setup via Nous Portal on a fresh install to compare the new first-run experience.

[NOVA]: For Codex, upgrade to zero point one thirty seven and test one multi-agent session to verify runtime choice persists correctly across a spawn and resume cycle. Run the machine-readable plugin list command to see the output format. Test parallel web search in a code-mode flow. Check the new monthly credit limit display in any enterprise or admin flow you have access to.

[ALLOY]: For Claude Code, add a fallbackModel to your config with two or three alternatives ordered by preference. Test the chain by temporarily making your primary model unavailable and verifying the fallback fires correctly. Use a wildcard in a deny rule to test full tool lockout. Verify that unknown tool names in deny rules produce startup warnings. Upgrade to two point one point one sixty seven for the latest bug fixes.

[NOVA]: For Gemma 4 12B, pull the checkpoint from Hugging Face and run it through LM Studio or Ollama on a laptop with 16 gigabytes of VRAM. Compare one coding task output against your current local model. Test the 256K context on a long codebase or document understanding task. Use Google AI Edge for the managed local deployment path if you prefer a one-command install.

[ALLOY]: For Kimi Code CLI, install it with the install script and verify with the version flag. Connect it to your Kimi API key or Moonshot AI OAuth. Test one MCP server configuration via the mcp-config command. Run one subagent in parallel against a codebase task and compare execution quality against your current CLI agent.

[NOVA]: For the A2A Protocol, read the v1.0 specification on the a2aproject GitHub repo to understand agent card structure and task state machine semantics. If you are building a multi-agent workflow, design the agent handoff points with A2A agent cards in mind. Test one cross-framework agent delegation if you have two different agent runtimes available.

[ALLOY]: For the awesome-ai-agents-2026 curated list, browse the MCP and A2A protocol sections to find one new server or protocol implementation relevant to your stack. The list is updated frequently and is the definitive index for what to read next when you are evaluating new agent tooling.

[NOVA]: The thread across today's AgentStack Daily is surface area and connectivity. The harness layer is consolidating around native, multi-surface tools that operators actually want to use. The model layer is adding open-weight options for local-first workflows. The protocol layer is the connective tissue that lets those tools talk to each other. The agent stack is getting less mystical and more operational, and that is exactly what it needs to become a production tool rather than a research demo.

[ALLOY]: We'll be back soon.

[NOVA]: The show notes for today's AgentStack Daily are at Toby On Fitness Tech dot com. You will find the timestamps, the links to the releases and tools we covered, and the deeper technical context that did not fit in the spoken audio.

[NOVA]: This is AgentStack Daily. I'm NOVA. Thanks for listening.