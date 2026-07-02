# EP078 — The Return of Claude Fable 5: US Restrictions Lifted; OpenClaw 6.11, Codex .142.5, Claude Sonnet 5 on OpenRouter

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: OpenClaw 6.11 fixed misplaced replies, stuck sends, dropped reconnects, model setup failures, session compaction behavior, and safer admin defaults across channels, sessions, providers, the Control UI, and the terminal UI.

[ALLOY]: The terminal-based coding agent OpenAI Codex .142.5 tightened trace logging by stopping full Responses WebSocket request payloads from landing in trace output, which matters anywhere Codex telemetry flows into shared observability systems.

[NOVA]: Claude Fable 5 is generally available again after Washington dropped restrictions on Anthropic's Mythos and Fable models on June 30, and the OpenRouter listing is live with a one-million-token context window, text, image, uploaded-asset input, and reasoning support.

[ALLOY]: Today: OpenClaw and Codex lead the release readout, Claude Fable 5 returns as the top-of-chain Mythos-class tier above Opus, Claude Sonnet 5 brings a four-level reasoning dial to OpenRouter, and Google adds Nano Banana 2 Lite for fast image generation.

[NOVA]: You'll hear where Fable 5 sits against GPT-5.5 on the current frontier, how Fable chains multi-step work off a single prompt, why Orca's world-latent paper is getting attention, how Agents-A1 claims trillion-parameter-class agent performance from a 35B mixture-of-experts student, and why OmniRoute, BlockPilot, generative skill composition, and TRIAGE all matter for shipped agent stacks.

[PAUSE]

## [02:00] Agent Stack Release Readout: OpenClaw 6.11; OpenAI Codex .142.5

[ALLOY]: Two stable agent-harness releases landed. OpenClaw 6.11 is a dependability pass across the places where agent sessions usually feel brittle: channel delivery, reconnects, model setup, admin defaults, and recovery after provider trouble. The release targets Telegram, WhatsApp, Matrix, Google Chat, iMessage, Feishu, Mattermost, WebChat, the Control UI, and the terminal UI. In concrete use, newer Google Chat direct messages stop being misread as group conversations, Telegram webhook users keep receiving direct and group messages through restarts and config reloads, and Matrix encrypted gateways avoid long-running memory growth that can knock channels offline.

[NOVA]: The runtime work matters because the agent does not just answer once; it has to keep a session alive while channels reconnect, providers fail, context compacts, and humans keep sending instructions. OpenClaw now uses a 180-second default compaction timeout while still respecting explicit config, preserves Codex context-engine compaction ownership, and keeps provider-failure lifecycle state correct. Reasoning-capable heartbeat checks also stop leaking internal reasoning into Telegram and WhatsApp, surfacing the assistant's intended reply instead.

[ALLOY]: OpenAI Codex .142.5 is much narrower, but the patch carries real operational weight. Codex stops writing full Responses WebSocket request payloads into trace logs. That is not a feature headline; it is a data-hygiene correction for teams that pipe Codex traces into shared monitoring, incident review, or hosted log search. The terminal-based coding agent can still be observed, but the raw request body no longer becomes accidental telemetry.

[NOVA]: Together, these releases make the harness layer easier to wire, deploy, and operate. OpenClaw tightens delivery and recovery across human-facing channels; Codex tightens what leaves the agent runtime during debugging. The practical win is reliability without changing how builders configure sessions, route channels, connect providers, or ship observability around the agent.

[PAUSE]

## [03:05] Claude Fable 5 Is Back: Where It Sits at the Top of the Frontier

[ALLOY]: Claude Fable 5 is generally available again. On the public frontier, the top tier is Claude Mythos 5, Claude Fable 5, and OpenAI GPT-5.5. Mythos 5 is the strongest of the three but stays gated behind an approved-organization list. Fable 5 is the same underlying model with additional safeguards for dual-use capabilities, and it is the version ordinary API routing can reach. GPT-5.5 sits just behind that pair. Fable 5 is generally considered the top model you can route to today.

[NOVA]: What makes Fable 5 feel different is single-prompt chaining. Give Fable one user message with several independent instructions and the model decomposes the work on its own: it identifies each subtask, plans an order, executes them in sequence, and returns a result that already accounts for the dependencies between them. Older frontier models needed the orchestrator to split the prompt, call the model once per instruction, and stitch the answers back together. Fable 5 does that decomposition internally.

[ALLOY]: The deployment shape supports it. The OpenRouter listing exposes a one-million-token context window, text and image input plus uploaded project assets, text output, and reasoning support. Anthropic positions it for autonomous knowledge work and coding. OpenClaw already wired in Claude Fable 5 provider support in mid-June, so harness-side integration predates the availability window reopening.

[PAUSE]

## [04:10] Claude Sonnet 5 Lands on OpenRouter: The Cheaper Fable-Shaped Endpoint

[ALLOY]: Claude Sonnet 5 is the second new Anthropic listing on OpenRouter this cycle, and the practical comparison is against Fable 5 rather than older Sonnet versions. Sonnet 5 ships with the same one-million-token context window as Fable 5 and exposes adaptive thinking through four selectable effort levels: low, medium, high, and max. The shape is the same as Fable 5 on context and reasoning, the difference is depth per request and the per-token cost of asking for it.

[NOVA]: Adaptive thinking is the headline. Where Fable 5 picks reasoning depth internally as part of its chaining behavior, Sonnet 5 exposes that dial to the caller. A planning turn can ask for max effort, a formatting turn can stay on low, and an orchestrator can route cost-heavy reasoning only where the work pays off. The endpoint is reachable as anthropic/claude-sonnet-5 on OpenRouter, served by Anthropic, with text and image input and text output.

[ALLOY]: In the current frontier ranking, Sonnet 5 sits a tier below Fable 5 on raw capability but ahead of the older Sonnet 4 class and most open-weight endpoints on coding-agent workloads. Builders who were routing their heaviest sessions through Opus-class defaults can now reach a Mythos-shaped Sonnet with a tunable effort dial, which changes the cost calculus on long agent sessions without giving up the long-context surface.

[NOVA]: Worth watching is whether router clients surface the four-step effort control cleanly. The value depends on per-request behavior being consistent across the provider's own SDK and the OpenRouter pass-through, not just on the catalog listing.

[PAUSE]

## [05:08] Google Nano Banana 2 Lite: Fast Image on OpenRouter

[ALLOY]: Google listed Nano Banana 2 Lite on OpenRouter under the Gemini 3.1 Flash Lite Image branding. It is framed as Google's fastest, most cost-efficient Gemini image model, built for high-velocity developer pipelines and rapid-fire visual exploration rather than maximum visual fidelity.

[NOVA]: The listing exposes a 65,536-token context window and a text-to-image generation endpoint. The Flash-Lite tier tells you the intended trade: smaller, faster inference with better unit economics, not the heaviest Pro-class render quality. That makes it a fit for bulk ideation, product mock variations, thumbnails, interface states, ad concepts, and any workflow that needs many cheap candidate images before a human or heavier model picks winners.

[ALLOY]: On the image-model ranking, Nano Banana 2 Lite sits below Imagen-class and Pro-class Gemini endpoints on raw visual quality but well above most lightweight open image models on prompt adherence and instruction following. OpenRouter makes the integration angle direct. If an image-agent stack already routes through the platform, the new Google endpoint can be selected with a model-string change. The rest of the pipeline can keep the same request shape, moderation wrapper, prompt builder, and result handling.

[NOVA]: The caveat is quality. Flash-Lite is built to be hammered, not to win every aesthetic comparison. Builders using image generation as a high-volume subroutine now have a Google-native option; final brand-critical renders still belong on a heavier model.

[PAUSE]

## [06:06] Orca Paper Proposes Unified World Latent Space Through Next-State Prediction

[ALLOY]: Orca, trending on HuggingFace Daily Papers with 161 upvotes, proposes a unified world latent space built through multimodal next-state prediction. The training objective is the paper's actual contribution: feed the model multimodal world observations and ask it to predict the next state, which forces a single shared latent to encode world dynamics rather than per-domain features.

[NOVA]: The authors then probe that representation on downstream tasks and report beating specialized baselines that were trained per-domain. A general latent that beats domain-specific world models is unusual; that is the 161-upvote signal. The arXiv identifier is 2606.30534, the project page is hosted at the orca world model site on GitHub.

[ALLOY]: The mechanism behind the result is the next-state loss. Predicting the next state from a multimodal input requires the latent to capture action consequences, persistence across time, and cross-modal alignment at once. Specialized per-domain world models only need to capture their own slice. Orca's argument is that the joint objective produces a representation that transfers, and the benchmarks are the proof.

[NOVA]: For builders planning agentic or embodied pipelines, the practical signal is that general world-model pre-training is becoming a credible alternative to task-specific stacks. The wider implication: a shared world latent can shift the cost calculus away from per-domain feature engineering over the next 12-18 months, which is worth tracking for any team building simulators, embodied agents, or persistent-state planners.

[PAUSE]

## [07:04] Agents-A1: 35B MoE Agent Hits Trillion-Parameter-Class Performance

[ALLOY]: InternScience's Agents-A1 is a 35-billion-parameter mixture-of-experts agentic model claiming trillion-parameter-class results through long-horizon trajectory scaling and heterogeneous agent ability scaling. The paper is trending on HuggingFace's daily feed with 73 upvotes, and the attraction is the recipe, not just the parameter count.

[NOVA]: Training runs in three stages. First, supervised fine-tuning on long agent traces teaches the model extended multi-turn behavior instead of isolated prompt-response moves. Second, per-domain teachers specialize across capabilities like coding, tool use, and retrieval. Third, multi-teacher distillation fuses those specialists into one 35B MoE student.

[ALLOY]: On agentic benchmarks, Agents-A1 reports numbers that sit near trillion-parameter proprietary models on long-horizon tool-use suites while running at the serving cost of a 35B MoE. That gap between capability and deployment cost is the point of the paper. If the recipe replicates outside the authors' evaluation setup, the budget story for serving frontier agents changes from "you need a hyperscaler cluster" to "you need a single 35B MoE host."

[NOVA]: The independent proof still has to come. Watch for open weights, benchmark replication, and evidence that long-horizon gains survive outside the authors' evaluation setup. But the direction is important: frontier agent behavior may increasingly come from trajectory quality and teacher composition, not just raw scale.

[PAUSE]

## [08:02] OmniRoute Turns One Endpoint Into 231 Model Providers

[ALLOY]: OmniRoute, an open-source AI gateway, hit GitHub Trending by collapsing 231 model providers into a single OpenAI-compatible endpoint, with roughly 50 providers offering free tiers. It is meant to sit between coding agents and upstream model APIs, including Cursor, Cline, Copilot, Codex, and the terminal-based AI coding agent Claude Code.

[NOVA]: The mechanism is a routing plane plus compression. OmniRoute applies a stacked token-compression pipeline, RTK plus Caveman mode, before prompts reach upstream providers. The author claims usage reductions from 15% to 95%, depending on workload. A smart auto-fallback layer reroutes failed or rate-limited requests to another provider instead of letting the agent loop stall.

[ALLOY]: MCP and A2A compatibility keep tool calls and agent-to-agent messages in play, while Desktop and PWA surfaces make it easier to operate as a local gateway rather than a cloud-only service. The integration angle is straightforward: one OpenAI-compatible base URL can replace provider-by-provider wiring, letting teams configure one gateway and deploy agents across paid and free upstreams.

[NOVA]: The trade-offs to watch are latency, compression quality, and fallback policy. If compression harms prompt fidelity or fallback jumps to weaker providers at the wrong moment, agents can drift. But for long coding loops that routinely hit limits, one gateway spanning paid and free providers is a practical control plane.

[PAUSE]

## [09:00] BlockPilot Picks Block Sizes Live for Diffusion Speculative Decoding

[ALLOY]: BlockPilot, trending on HuggingFace Daily Papers with 64 upvotes, proposes instance-adaptive policy learning for diffusion-based speculative decoding. Instead of using a fixed block size for every prompt, the method predicts how many tokens the diffusion drafter should produce per step.

[NOVA]: The policy network reads hidden states from the prefilling stage and outputs a per-request block size. Then the diffusion drafter generates that many tokens before the target model verifies them. Static schedules spend the same draft budget on easy and hard prompts; BlockPilot conditions speculation depth on what the prompt actually looks like.

[ALLOY]: The authors report significant speedups over static block-size approaches with minimal overhead, and the AMAP-ML group released the implementation and trained policy alongside the preprint. That matters because the technique aims to improve inference efficiency without retraining the target model.

[NOVA]: For teams already using speculative decoding, block size moves from a deployment knob to a learned runtime decision. The open question is generalization: whether the released policy transfers across model families or mainly works inside the training distribution used in the paper.

[PAUSE]

## [09:58] Generative Skill Composition Tackles LLM Agent Skill Bottleneck

[ALLOY]: Xinyu Zhao, Zhen Tan, and Vaishnav Tadiparthi frame skill composition as a growing bottleneck for LLM agents. As procedural skill libraries expand, two common approaches start to break down: dumping every skill into context burns tokens, while embedding retrieval can miss useful combinations across skills.

[NOVA]: The paper proposes generative skill composition. Instead of retrieving a fixed skill or exposing the full library, the model synthesizes a combination on demand for the task. Skill selection becomes generation, not ranking. The agent reasons about how to combine procedures rather than grabbing the nearest match from a catalog.

[ALLOY]: That shift lines up with how agent stacks mature. Early systems can survive with a handful of tools and simple retrieval. Larger systems accumulate refactor skills, sandbox skills, browser skills, build skills, data skills, and deployment skills. The hard part becomes composing them without context bloat.

[NOVA]: The builder takeaway is that skill library structure matters as much as library size. If generative composition beats retrieval baselines, future agent runtimes will need scaffolding that helps models synthesize safe, relevant procedures from smaller pieces.

[PAUSE]

## [10:56] TRIAGE Paper Proposes Role-Typed Credit Assignment for Agentic RL

[ALLOY]: TRIAGE adds role-typed credit assignment to agentic reinforcement learning. Standard GRPO often applies one final verifier outcome as a uniform advantage across every action token in a rollout, so search, click, edit, navigation, and object-interaction steps all receive the same learning signal.

[NOVA]: TRIAGE inserts a structured judge between rollout and gradient update. The judge tags each rollout segment by semantic role before advantage is computed, making the update role-conditional instead of flat. That changes credit assignment without changing the reward function itself.

[ALLOY]: The reported gains concentrate in tool-heavy rollouts, which makes sense. In long agent trajectories, only some actions decide the outcome. A useful search step inside a failed rollout should not be punished the same way as a dead-end action, and redundant clicks inside a successful rollout should not be reinforced just because the final answer passed.

[NOVA]: For teams training agent policies with RL, TRIAGE points attention toward action weighting. Verifier quality still matters, but dense tool use needs sharper credit. The judge model becomes the pressure point, because role labels have to be consistent enough to improve learning rather than add variance.

[PAUSE]

## [12:00] GitHub Project Radar: PrefectHQ/fastmcp

[ALLOY]: PrefectHQ fastmcp is a Pythonic framework for building Model Context Protocol servers and clients. It gives developers FastAPI-style ergonomics for declaring tools, resources, and prompts, so agents can discover typed capabilities through MCP rather than ad-hoc function calls.

[NOVA]: The integration angle is clean: drop fastmcp into a Hermes, Codex, OpenClaw, or Claude Code-adjacent stack when internal services need to become schema-validated tools. Instead of hand-rolling JSON-RPC plumbing, teams can expose typed operations with inspectable interfaces and let MCP-compatible clients discover them.

[ALLOY]: That matters because MCP adoption is moving from demos to production wiring. A framework that makes tool declarations feel like ordinary Python service code lowers the cost of turning internal APIs into agent-ready surfaces.

[PAUSE]

## [12:40] GitHub Project Radar: DeusData/codebase-memory-mcp

[NOVA]: DeusData codebase-memory-mcp is a single static binary that indexes a repo into a persistent knowledge graph and answers structural queries across 158 languages. The project claims sub-millisecond structural lookups and roughly 99% fewer tokens than re-feeding raw source into a model.

[ALLOY]: The fit is underneath coding agents. Mount it as the long-lived code-retrieval layer for OpenClaw, Codex, or any MCP-capable client, and navigation questions can resolve against the graph instead of triggering fresh embeddings or large context stuffing on every turn.

[NOVA]: The concrete win is latency plus token discipline. A coding agent that can ask where a symbol is defined, which call sites touch it, or how modules connect gets a compact answer before deciding what to edit, build, or ship.

[PAUSE]

## [13:20] GitHub Project Radar: microsoft/mcp-for-beginners

[ALLOY]: Microsoft's mcp-for-beginners is a multi-language curriculum for the Model Context Protocol, with worked examples in C#, Java, TypeScript, JavaScript, Rust, and Python. It focuses on practical client-server patterns for modular, scalable, and secure agent workflows.

[NOVA]: The integration angle is team enablement. If a stack has one runtime in Python, another in TypeScript, and a service team in Java or C#, the examples give each group a native path to MCP without forcing one language choice.

[ALLOY]: The useful pieces are not just hello-world tools. The lessons cover patterns around client-server boundaries, auth, and scoped tool exposure, which are exactly the parts that determine whether an agent can safely call production capabilities.

[PAUSE]

## [14:00] Model Discovery Check

[NOVA]: Claude Fable 5 is selected because availability returned this cycle. On the current frontier ranking it sits at the top of the generally available tier alongside GPT-5.5, sharing underlying model parity with Mythos 5 plus additional dual-use safeguards, and shipping with the single-prompt chaining behavior that distinguishes it from older frontier endpoints. It is reachable through OpenRouter at anthropic/claude-fable-5, carries a one-million-token context window, supports text, image, uploaded-asset input, and text output, and brings reasoning support. The immediate evaluation path is a coding-agent or autonomous research session against current Opus-class defaults, focused on whether the chaining behavior reduces orchestrator-level planning work.

[ALLOY]: Claude Sonnet 5 is selected because it is a new major-provider model listing with one-million-token context and selectable reasoning effort. The practical angle is routing a coding or agent session through Sonnet 5 and comparing low, medium, high, and max effort on latency, cost, and completion quality, especially for sessions where Fable 5 is too expensive.

[NOVA]: Google Nano Banana 2 Lite is selected because it adds a major-provider image endpoint optimized for speed and cost. It exposes a 65,536-token context window and text-to-image generation through OpenRouter, making it useful for high-volume visual exploration and bulk asset generation.

[ALLOY]: There were no Not Selected model entries in the discovery check.

[PAUSE]

## [14:50] Local LLM Spotlight: Ollama .31.1

[NOVA]: Ollama .31.1 brings a major Apple Silicon speedup for Gemma 4 by leaning on multi-token prediction. Instead of generating one token per forward pass, MTP drafts several tokens and verifies them in parallel.

[ALLOY]: The release keeps the one-binary local workflow and existing API contracts, so the interesting change is performance rather than integration churn. Across a coding-agent benchmark, generation is reported at roughly 90% faster on M-series hardware.

[NOVA]: The practical angle is local coding assistance on an M-series Mac. Pull Gemma 4, run a code-completion prompt through Ollama, and compare tokens per second against an older .30 build to see whether the MTP gain shows up on your own machine.

[PAUSE]

## [15:30] Extra Research Candidates: Anthropic-Cybersecurity-Skills

[ALLOY]: The Anthropic-Cybersecurity-Skills repo packages 817 structured cybersecurity skills for AI agents, mapped across MITRE ATT&CK, NIST CSF, MITRE ATLAS, D3FEND, NIST AI RMF, and MITRE's fraud-fighting framework.

[NOVA]: Each skill ships as an agentskills.io-style manifest, giving agents a fixed taxonomy across 29 security domains. That makes it relevant to security-agent stacks that need controlled procedures instead of free-form tool improvisation. The useful question is whether the taxonomy improves dispatch quality when an agent has to choose between reconnaissance, defense, fraud, and AI-risk workflows.

[PAUSE]

## [16:05] Extra Research Candidates: AxDafny

[ALLOY]: AxDafny studies agentic verified code generation in Dafny, where a model has to generate both executable code and the proof material needed for verification.

[NOVA]: The framework runs verifier-guided repair. Dafny's SMT-backed checker catches failed invariants, assertions, and termination arguments, then the LLM proposes the next repair. That loop gives the agent concrete counterexamples instead of vague feedback. For builders working on high-assurance code generation, AxDafny shows how a verifier can become the agent's tightest feedback channel.

[PAUSE]

## [16:40] Extra Research Candidates: Surrogate Fidelity

[ALLOY]: Surrogate Fidelity asks when open LLMs can explain closed ones. Mechanistic interpretability usually needs internal access, but widely deployed closed models expose only limited API signals, often token probabilities.

[NOVA]: The paper treats open-weight models as measurement probes. It uses binary-task log-odds as API-compatible scalars and leave-one-out attribution to test when mechanistic claims transfer across eleven models. The integration angle is evaluation caution: an open surrogate can help explain a closed model only when the transfer conditions are measured, not assumed.

[PAUSE]

## [17:20] Practical queue

[ALLOY]: OpenClaw 6.11 tightens channel delivery and session recovery, while Codex .142.5 reduces trace-log exposure from Responses WebSocket traffic.

[NOVA]: Claude Fable 5 is back as the top of the generally available frontier alongside GPT-5.5, with router access, one-million-token context, multimodal input, reasoning, and single-prompt chaining for multi-instruction work.

[ALLOY]: Claude Sonnet 5 adds a one-million-token Sonnet endpoint with per-request reasoning effort across low, medium, high, and max.

[NOVA]: Nano Banana 2 Lite gives image-agent pipelines a faster, cheaper Google image path for high-volume generation.

[ALLOY]: Orca, Agents-A1, BlockPilot, generative skill composition, and TRIAGE all push agent stacks toward better representations, cheaper long-horizon behavior, faster inference, stronger procedural composition, and sharper RL credit.

[NOVA]: fastmcp, codebase-memory-mcp, and mcp-for-beginners show MCP maturing into a practical integration layer for typed tools, code knowledge, and multi-language agent services.

[ALLOY]: Ollama .31.1 makes local Gemma 4 coding workflows faster on Apple Silicon through multi-token prediction.

[NOVA]: For the source details behind each item, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.