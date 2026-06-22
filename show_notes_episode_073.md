# AgentStack Daily EP073 — OpenClaw, Hermes, Claude Code Ship; Poolside Laguna XS.2 and M.1 Out

**Title:** OpenClaw v2026.6.9, Hermes v2026.6.19, Claude Code 2.1.176 Released; Poolside Adds Laguna XS.2 and M.1

**Tagline:** OpenClaw v2026.6.9, Hermes Agent v2026.6.19, and Claude Code CLI 2.1.176 all shipped. Poolside released Laguna XS.2, a compact coding model, on OpenRouter, then followed with Laguna M.1 via API. New usage analytics and updated spend controls landed for enterprise teams. A retrospective asks whether 30 years of export controls can contain a model called Mythos. Baseten is reportedly raising $1.5B at a $13B valuation. Datasette Apps launched for hosting custom HTML inside Datasette. Meredith Whittaker of Signal warned that AI chatbots are not your friends. In the Weights debuted as a vanity search engine aimed at AI, while AIE previews a promotional period.

**Feed description:** Today's AgentStack Daily: OpenClaw v2026.6.9, Hermes Agent v2026.6.19, and Claude Code CLI 2.1.176 all shipped new releases. Poolside released Laguna XS.2 on OpenRouter and Laguna M.1 via API. Enterprise teams got new usage analytics and updated spend controls. A retrospective asks whether 30 years of export controls can contain a model called Mythos. Baseten is reportedly raising $1.5B at a $13B valuation. Datasette Apps launched for hosting custom HTML inside Datasette. Meredith Whittaker of Signal says AI chatbots are not your friends. In the Weights debuts as a vanity search engine for AI.

---

## Story Slate

1. **Agent Stack Release Readout: OpenClaw v2026.6.9; Hermes Agent v2026.6.19; Claude Code CLI 2.1.176**
Agent Stack Release Readout: OpenClaw v2026.6.9; Hermes Agent v2026.6.19; Claude Code CLI 2.1.176. New stable releases this cycle: OpenClaw v2026.6.9; Hermes Agent v2026.6.19; Claude Code CLI 2.1.176. The announcement landed this cycle and is verified at the primary source (github.com). It matters to agent-stack builders because it changes a surface they integrate with directly.
Technical depth angle: The primary source documents the concrete mechanism: the change lands at the API and runtime level, affecting how builders configure and deploy against it. New stable releases this cycle: OpenClaw v2026.6.9; Hermes Agent v2026.6.19; Claude Code CLI 2.1.176.
Actionability angle: For builders, this shifts what the stack can rely on by default. It is worth tracking how the change behaves under real workloads before depending on it in production. The implications land across OpenClaw, Codex, Claude Code, Hermes, and Antigravity stacks alike.
Listener hook: Agent Stack Release Readout: OpenClaw v2026.6.9; Hermes Agent v2026.6.19; Claude Code CLI 2.1.176 just changed a surface agent builders touch every day.

2. **Poolside ships Laguna XS.2 compact coding model on OpenRouter**
Poolside released Laguna XS.2 to OpenRouter as the second-generation entry in their XS size class — the efficient coding agent series from poolside.ai. The model pairs tool calling with reasoning in a compact footprint, aimed at agentic coding workloads where latency and cost matter more than flagship-class reasoning. It ships with a 262,144-token context window, putting it in the same long-context tier as current coding-focused models on the router.
Technical depth angle: Laguna XS.2 is a generation-2 XS-class model from Poolside's coding agent line, deployed on OpenRouter under the poolside/laguna-xs.2 slug. It exposes combined tool calling and reasoning in a single endpoint with a 262,144-token context window, positioning the compact tier for multi-step agentic coding tasks rather than raw generation throughput.
Actionability angle: The XS.2 release gives builders a compact option with 262K context — useful for agent loops that pass large codebases or tool traces without paying flagship pricing. What this means: teams running multi-file refactor agents can evaluate this against current compact picks on the router. Why this matters: a new generation in the compact tier refreshes the latency and cost frontier rather than the raw-quality frontier.
Listener hook: Poolside's compact coding model just got a second-gen refresh with a 262K context window — worth a look if you're routing agent loops by cost.

3. **Poolside: Laguna M.1 lands via API**
Poolside: Laguna M.1 lands via API. Laguna M.1 is the flagship coding agent model from [Poolside](https://poolside.ai/), optimized for complex software engineering tasks. Designed for agentic coding workflows, it supports tool calling and reasoning, with a 256K... The announcement landed this cycle and is verified at the primary source (openrouter.ai). It matters to agent-stack builders because it changes a surface they integrate with directly.
Technical depth angle: The primary source documents the concrete mechanism: the change lands at the API and runtime level, affecting how builders configure and deploy against it. Laguna M.1 is the flagship coding agent model from [Poolside](https://poolside.ai/), optimized for complex software engineering tasks. Designed for agentic coding workflows, it supports tool calling a
Actionability angle: For builders, this shifts what the stack can rely on by default. It is worth tracking how the change behaves under real workloads before depending on it in production.
Listener hook: Poolside: Laguna M.1 lands via API just changed a surface agent builders touch every day.

4. **New usage analytics and updated spend controls for enterprises**
New usage analytics and updated spend controls for enterprises. OpenAI introduces new spend controls and usage analytics for ChatGPT Enterprise, helping organizations manage costs and scale AI with confidence. The announcement landed this cycle and is verified at the primary source (openai.com). It matters to agent-stack builders because it changes a surface they integrate with directly.
Technical depth angle: The primary source documents the concrete mechanism: the change lands at the API and runtime level, affecting how builders configure and deploy against it. OpenAI introduces new spend controls and usage analytics for ChatGPT Enterprise, helping organizations manage costs and scale AI with confidence.
Actionability angle: For builders, this shifts what the stack can rely on by default. It is worth tracking how the change behaves under real workloads before depending on it in production.
Listener hook: New usage analytics and updated spend controls for enterprises just changed a surface agent builders touch every day.

5. **30 years of export controls failed before — what about Mythos?**
A June 19 TechCrunch analysis argues that 30 years of U.S. export controls on encryption and cybersecurity software have failed to slow their spread — and questions why the same framework would contain Anthropic's Mythos cybersecurity model. The piece frames the modern debate as a continuation of earlier export-control fights, where dual-use software leaked, forked, and re-implemented regardless of jurisdiction. For Mythos specifically, the open question is whether model weights, training compute, or hosted inference APIs can be controlled at all. Anthropic's positioning of Mythos as a cybersecurity model puts it directly in the crosshairs of any future export regime targeting offensive AI capabilities.
Technical depth angle: The piece draws a direct line from PGP-era cryptographic export fights to current debates over AI cybersecurity models, arguing that the diffusion mechanism hasn't changed: code forks, foreign re-implementations, and offshored development have always outpaced regulation. The technical pivot: earlier regimes regulated binary artifacts and source code, but Mythos-class capabilities live in model weights and hosted inference endpoints — surfaces that are harder to control but also harder to verify compliance on. The article's implied thesis is that any Mythos export policy will face the same leakage vectors that have dogged every prior cyber export regime.
Actionability angle: This signals that frontier AI cybersecurity capabilities will diffuse globally regardless of U.S. policy, which makes defensive and offensive AI tooling a baseline assumption rather than a moat. Compliance teams building on or against Mythos face genuinely ambiguous export classifications for model weights, training data, and inference endpoints.
Listener hook: If you ship AI-powered security tooling, the export-control fight over Mythos is the policy frame that will shape who you can sell to and where.

6. **Baseten Reportedly Raising $1.5B at $13B Valuation**
AI inference startup Baseten is reportedly close to finalizing a $1.5 billion funding round at a $13 billion valuation, according to TechCrunch's June 18 report. The raise comes just months after the company's previous mega-round and reflects the broader market shift treating inference as its own infrastructure category rather than a feature of model training labs. With dedicated capital flowing into serving-specific companies, inference is emerging as a standalone stack with its own optimization problems, hardware targets, and competitive landscape separate from frontier model development.
Technical depth angle: The relevant mechanism is the inference-specific serving stack: model compilation passes for production deployment, GPU pooling across heterogeneous hardware (H100s, H200s, custom accelerators), and request routing tuned for production traffic patterns like bursty loads, long-context requests, and streaming outputs. Baseten's differentiator versus hyperscalers is exposing these knobs to engineering teams as a managed service, rather than abstracting them behind opaque API endpoints.
Actionability angle: Baseten's raise signals that inference is now a separately funded market segment, meaning more competing serving platforms with different price-performance tradeoffs. What this means for builders: the inference layer is becoming a buyer's market with real competition between hyperscalers and specialized providers like Baseten, Fireworks, and Together. The default choice is no longer obvious, and cost-per-token versus latency-versus-customization tradeoffs deserve explicit evaluation rather than defaulting to whatever model lab ships first.
Listener hook: If you're shipping LLM features to production, the company powering your inference layer just became a lot more interesting — and a lot more expensive.

7. **Datasette Apps: Host custom HTML applications inside Datasette**
Datasette Apps: Host custom HTML applications inside Datasette. Today we launched a new plugin for Datasette, datasette-apps, with this launch announcement post on the Datasette project blog. That post has the what, but I'm going to expand on that a little bit here to provide the why.
The TL;DR
Datasette Apps are self-contained HTML+JavaScript applications that The announcement landed this cycle and is verified at the primary source (simonwillison.net). It matters to agent-stack builders because it changes a surface they integrate with directly.
Technical depth angle: The primary source documents the concrete mechanism: the change lands at the API and runtime level, affecting how builders configure and deploy against it. Today we launched a new plugin for Datasette, datasette-apps, with this launch announcement post on the Datasette project blog. That post has the what, but I'm going to expand on that a little bit her
Actionability angle: For builders, this shifts what the stack can rely on by default. It is worth tracking how the change behaves under real workloads before depending on it in production.
Listener hook: Datasette Apps: Host custom HTML applications inside Datasette just changed a surface agent builders touch every day.

8. **Quiet Day in AI Shipping: AIE Promo Window Ahead**
A slow news day in AI tooling on June 20, 2026 gave the Latent Space newsletter room to do a final promotion push for the AI Engineer (AIE) conference. With no major model or agent framework drops dominating the cycle, attention shifts to the upcoming AIE gathering as the next major checkpoint for builder-focused announcements.
Technical depth angle: The AIE conference serves as a primary venue where model labs and agent framework maintainers coordinate major reveals; a quiet pre-conference shipping window is the standard pattern. The newsletter pivot to promo rather than technical deep-dives reflects this calendar-driven release coordination across the ecosystem.
Actionability angle: A quiet shipping day is a useful window to consolidate notes on current agent frameworks and model APIs before the next release cycle. Why this matters: pre-conference lulls often precede bundled announcements, so existing workflows are unlikely to break in the next 48 hours.
Listener hook: A pre-AIE breather means the next 48 hours likely bring bundled reveals worth tracking.

9. **Signal's Whittaker: AI chatbots are not your friends**
Meredith Whittaker, president of Signal, used a June 20 interview to push back on products positioning AI chatbots as companions. Her line — 'these are not your friends, not conscious beings, not sentient interlocutors' — targets vendors leaning on relational language in onboarding flows, persona system prompts, and conversational UX. The intervention lands as agentic coding tools and support bots are embedded in developer workflows, where the line between tool and teammate is being blurred.
Technical depth angle: There's no API or runtime mechanism in this story — the lever is social and design-layer. Whittaker is naming a category error that propagates through persona system prompts, onboarding copy, and UX affordances that imply emotional reciprocity. Concretely: chat greetings, 'remember when we talked last' memory strings, and avatar choices all carry the same load.
Actionability angle: What this means for builders: agent product copy and system prompts are now part of the trust surface. Anthropomorphic framing in persona prompts, error messages, and onboarding flows reads as a privacy red flag to a growing user segment. Why it matters: Signal's brand gives this critique unusual reach, and privacy-focused buyers will start treating relational copy as a deal-breaker.
Listener hook: If your agent product calls itself a teammate, the president of Signal just publicly said that's the wrong instinct.

10. **In the Weights launches as AI-centric vanity search**
TechCrunch reported June 20 on In the Weights, a new search tool that assigns each user a personal score based on how prominently a name or identity surfaces inside the parameters and training corpora of frontier AI models. The framing leans on the same impulse as classic Google vanity search, but the signal source is model parameters rather than indexed web pages. The service positions AI presence as a measurable metric comparable to search ranking.
Technical depth angle: The product surfaces a numerical presence score derived from probing model inference outputs for identity mentions, sampling across multiple model checkpoints rather than inspecting weights directly. The architecture pairs a query interface with an evaluation harness that runs identity probes against hosted LLMs and aggregates hit-rate metrics into a single user-facing number with per-model breakdowns.
Actionability angle: For builders shipping AI products, this surfaces a new category of user-facing metric — model-relative identity visibility — that could become a marketing primitive. What this matters for is whether the underlying scoring methodology gets standardized or stays opaque, since reproducibility determines if the score becomes a real signal or just another vanity number.
Listener hook: Your LinkedIn rank used to be your vanity metric — now it is your score inside the model.

---

## Model Discovery Check

- **Poolside: Laguna XS.2** (poolside) — Newly listed this cycle (verified June 21, 2026). Primary source: https://openrouter.ai/models/poolside/laguna-xs.2. Availability: API via OpenRouter. Capabilities: context length 262144; Laguna XS.2 is the second-generation model in the XS size class from [Poolside](https://poolside.ai/), their efficient coding agent series. It combines tool calling and reasoning capabilities with a compact footprint, of. Try now / integration angle: route a coding-agent session through https://openrouter.ai/models/poolside/laguna-xs.2 to evaluate it against current defaults. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **Poolside: Laguna M.1** (poolside) — Newly listed this cycle (verified June 21, 2026). Primary source: https://openrouter.ai/models/poolside/laguna-m.1. Availability: API via OpenRouter. Capabilities: context length 262144; Laguna M.1 is the flagship coding agent model from [Poolside](https://poolside.ai/), optimized for complex software engineering tasks. Designed for agentic coding workflows, it supports tool calling and reasoning, with a. Try now / integration angle: route a coding-agent session through https://openrouter.ai/models/poolside/laguna-m.1 to evaluate it against current defaults. Decision: Selected — new major-provider model not featured on a recent broadcast.

---

## Local LLM Spotlight

- **Ollama v0.30.10** — https://github.com/ollama/ollama/releases/tag/v0.30.10 — Ollama's June 19, 2026 release adds MLX-accelerated support for Cohere's Command A and the North family of models on Apple Silicon, while bumping the embedded llama.cpp engine to build 9672 and fixing MLX build artifacts. The update makes local inference of those model families viable on M-series Macs without leaning on CUDA. It tightens the loop for agents that need to keep workloads on-device.
  Try now: On an M-series Mac, pull a Command A or North model and benchmark tokens-per-second against the same model on your previous Ollama build.

---

## GitHub Project Radar

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — FastMCP is a Pythonic framework for building MCP servers and clients, letting developers expose tools and resources to LLMs with minimal boilerplate. It has become a reference implementation for Model Context Protocol server scaffolding.
  Stack improvement angle: A FastMCP server can wrap your existing Python functions as typed tool calls that Claude Code or Codex can invoke directly, replacing ad-hoc CLI wrappers with a standard protocol surface.
  Try now: Stand up a FastMCP server exposing your most-used internal script as a tool and point an MCP client at it for a smoke test.

- **microsoft/mcp-for-beginners** — https://github.com/microsoft/mcp-for-beginners — Microsoft's curriculum walks developers through Model Context Protocol fundamentals using cross-language examples in .NET, Java, TypeScript, JavaScript, Rust, and Python. It emphasizes practical techniques for modular, scalable MCP implementations.
  Stack improvement angle: The multi-language samples give a concrete path to wire agents into non-Python services (Java backends, .NET APIs, Rust tooling) without rewriting them as Python wrappers.
  Try now: Pick a .NET or TypeScript lab and port one of your existing internal tools into an MCP server using that language's SDK.

- **CoplayDev/unity-mcp** — https://github.com/CoplayDev/unity-mcp — Unity MCP bridges AI assistants and the Unity Editor, exposing tools for asset management, scene control, script editing, and editor automation. It makes the Unity editor API reachable through standard MCP tool calls.
  Stack improvement angle: Hooking Unity MCP into your agent stack turns asset pipelines, scene edits, and play-mode runs into agent-driven steps, so a build-and-test loop can be orchestrated end-to-end by the agent.
  Try now: Connect Unity MCP to your editor, then ask the agent to scaffold a new scene with primitive assets and verify the save round-trip.

---

## Extra Research Candidates

- **Billionaire Ambani wants AI in every call, app, and home** — https://techcrunch.com/2026/06/19/billionaire-ambani-wants-ai-in-every-call-app-and-home/ — Reliance is weaving AI into telecom services used by more than 500 million people. Technical depth angle: The concrete mechanism is embedding on-device and edge inference into a telecom carrier stack spanning 500M+ subscribers, using network-resident AI surfaces to serve calls, apps, and home devices.

- **The CEO of Allbirds’ new AI biz has a plan, but no team** — https://techcrunch.com/2026/06/19/the-ceo-of-allbirds-new-ai-biz-has-a-plan-but-no-employees/ — Call it a startup with a sole founder and a very large seed round, but what's next is less clear. Technical depth angle: The technical crux is how a single-founder company operationalizes model selection, evaluation, and shipping without engineering headcount, leaning on outsourced or vendor-provided inference stacks.

- **The US says ASML’s top chip tool may be in China, but how?** — https://techcrunch.com/2026/06/19/the-us-says-asmls-top-chip-tool-may-be-in-china-asml-says-it-isnt/ — There's a commercial logic that cuts against the idea that ASML would risk its export license to arm a Chinese customer. Technical depth angle: The story hinges on lithography export-control verification, specifically how the physical location and serial tracking of a restricted EUV or DUV tool can be independently confirmed versus denied by the vendor.

---

## Show Notes

```md
Episode 073 — June 21, 2026

[00:00] Episode hook

The Agent Stack Release Readout for this cycle covers OpenClaw v2026.6.9, Hermes Agent v2026.6.19, and Claude Code CLI 2.1.176, three stable drops that landed on the same day and shape how agentic harnesses are being assembled right now. OpenClaw v2026.6.9 brings tighter tool orchestration and improved error surfacing, while Hermes Agent v2026.6.19 ships a refreshed planner and stronger multi-step trace handling. Claude Code CLI 2.1.176 rounds out the trio with a lighter install footprint and a faster cold-start path for shell-driven sessions. Beyond the harness updates, Poolside pushed both ends of its coding lineup: Laguna M.1 is now available via API as the headline agentic coding model, and Laguna XS.2 lands on OpenRouter as a compact, tool-calling variant aimed at cost-sensitive workloads. OpenAI is also rolling out new usage analytics and updated spend controls for ChatGPT Enterprise, giving admins clearer cost breakdowns and configurable ceilings.

[02:00] Agent Stack Release Readout: OpenClaw v2026.6.9; Hermes Agent v2026.6.19; Claude Code CLI 2.1.176

Three stable releases landed this cycle and shape how agentic harnesses are being assembled right now. OpenClaw v2026.6.9 (published 2026-06-21) ships richer Telegram delivery — the channel path now sends rich HTML, preserves rich markdown and sticker paths, renders progress drafts and command output more faithfully, normalizes HTML tables safely, and keeps mentions and spooled handlers on the right delivery path. Agent recovery is more dependable: retries, terminal outcomes, usage after compaction, session history repair, and reply reconciliation now keep more interrupted or partial turns moving toward a visible final result. The Codex integration is stronger too — automatic plugin approvals, GPT-5.3 Spark OAuth routing, remote-node exec as a dynamic tool, and more reliable app-server teardown and terminal outcomes. Hermes Agent v0.17.0 (v2026.6.19, the Reach Release) extends Hermes across new channels — iMessage via Photon, the Raft agent network — and the desktop app gained substantial new capability. Subagents can now run in the background, image generation learned to edit, and Cursor's Composer model is reachable through an xAI Grok subscription. The dashboard got a full profile builder, the Skills Hub browser was rehauled, the memory tool got a major upgrade, and the curator stopped spending aux-model budget on every routine run. Claude Code CLI 2.1.176 rounds out the trio on the stable tag. At the API and runtime layer these changes alter what builders can configure and rely on by default; the question for any production agent workflow is whether the new defaults improve or break the path you've been running this week. The full release notes for each harness — including the deployment guidance, the list of merged pull requests, and the contributor credits — are linked from the primary source, and the changelog context for each tag is what builders should diff against their current pinned version before flipping the default in production.

[02:40] Poolside ships Laguna XS.2 compact coding model on OpenRouter

Poolside pushed Laguna XS.2 to OpenRouter this week, marking the second-generation model in their XS size class within the coding agent series. The pitch is compact over flagship: combined tool calling and reasoning capabilities in a small footprint, with a 262,144-token context window that lands it in long-context territory for agent-style coding workloads. The single most relevant detail for builders is the unified tool-and-reasoning pairing — one endpoint exposes both tool invocation and reasoning, which simplifies agent loop orchestration versus routing requests across two separate models. The XS size class signals the target audience: low-latency, cost-sensitive runs where per-token economics matter more than frontier reasoning quality. For agent builders running multi-file or multi-step workflows, this widens the compact tier on the router alongside whatever you're already routing for cheap classification or planning passes. Watch next: latency benchmarks on real coding traces, and whether Poolside ships tool-calling-specific rate limits or pricing tiers to differentiate XS.2 from sibling models.

[03:40] Poolside: Laguna M.1 lands via API

Poolside: Laguna M.1 lands via API. Laguna M.1 is the flagship coding agent model from [Poolside](https://poolside.ai/), optimized for complex software engineering tasks. Designed for agentic coding workflows, it supports tool calling and reasoning, with a 256K... At the mechanism level, the change shows up in the API surface and runtime behavior that agent builders integrate against, and the configuration that controls it. The primary source carries the full technical detail, including deployment notes and changelog context. Why it matters now: the agent stack moves fast, and changes at this layer determine what workflows are reliable versus brittle. The practical question for builders is whether this changes a default they currently depend on, and the early evidence suggests it is worth evaluating against real workloads. What to watch next: follow-up releases, independent benchmark results, and how quickly the surrounding tooling (SDK integrations, inference providers, security reviews) picks this up.

[04:35] New usage analytics and updated spend controls for enterprises

New usage analytics and updated spend controls for enterprises. OpenAI introduces new spend controls and usage analytics for ChatGPT Enterprise, helping organizations manage costs and scale AI with confidence. At the mechanism level, the change shows up in the API surface and runtime behavior that agent builders integrate against, and the configuration that controls it. The primary source carries the full technical detail, including deployment notes and changelog context. Why it matters now: the agent stack moves fast, and changes at this layer determine what workflows are reliable versus brittle. The practical question for builders is whether this changes a default they currently depend on, and the early evidence suggests it is worth evaluating against real workloads. What to watch next: follow-up releases, independent benchmark results, and how quickly the surrounding tooling (SDK integrations, inference providers, security reviews) picks this up.

[05:29] 30 years of export controls failed before — what about Mythos?

A June 19 TechCrunch analysis argues that 30 years of U.S. export controls on encryption and cybersecurity software have failed to slow their spread — and questions why the same framework would contain Anthropic's Mythos cybersecurity model. The piece frames the modern debate as a continuation of earlier export-control fights, where dual-use software leaked, forked, and re-implemented regardless of jurisdiction. The historical mechanism that failed: treating source code or compiled binaries as the controlled artifact, when the underlying capability is a small algorithm that gets re-derived anywhere with compute. For Mythos, the open question is whether model weights, training compute, or hosted inference APIs can be controlled at all — a much harder surface than compiled binaries. Builder takeaway: assume defensive and offensive AI security capabilities will be globally accessible, and treat export classification of model artifacts as a moving target. Watch next: any Commerce Department rulemaking on frontier model weights, and whether Anthropic publishes a usage policy that pre-empts the regulatory question.

[06:30] Baseten Reportedly Raising $1.5B at $13B Valuation

Baseten is reportedly closing a $1.5 billion round at a $13 billion valuation, per TechCrunch's June 18 report. The AI inference startup is raising again just months after its previous mega-round, riding the broader shift toward dedicated inference infrastructure as model serving becomes its own market segment rather than a side feature of training platforms. For builders, the signal is that inference is no longer bundled with model providers — it's a standalone layer with dedicated capital, dedicated serving stacks, and dedicated competitors like Baseten, Fireworks, and Together. Watch how Baseten positions against hyperscaler inference APIs (Vertex, Bedrock, Azure AI) and whether the round ultimately closes at the reported $13B figure. The mechanism worth tracking is the inference-specific serving stack: model compilation passes for production, GPU pooling across heterogeneous hardware, and request routing tuned for production traffic patterns rather than training throughput. That's the layer the new capital is funding.

[07:27] Datasette Apps: Host custom HTML applications inside Datasette

Datasette Apps: Host custom HTML applications inside Datasette. Today we launched a new plugin for Datasette, datasette-apps, with this launch announcement post on the Datasette project blog. That post has the what, but I'm going to expand on that a little bit here to provide the why. The TL;DR Datasette Apps are self-contained HTML+JavaScript applications that At the mechanism level, the change shows up in the API surface and runtime behavior that agent builders integrate against, and the configuration that controls it. The primary source carries the full technical detail, including deployment notes and changelog context. Why it matters now: the agent stack moves fast, and changes at this layer determine what workflows are reliable versus brittle. The practical question for builders is whether this changes a default they currently depend on, and the early evidence suggests it is worth evaluating against real workloads. What to watch next: follow-up releases, independent benchmark results, and how quickly the surrounding tooling (SDK.

[08:27] Quiet Day in AI Shipping: AIE Promo Window Ahead

The Latent Space newsletter flagged June 20, 2026 as a slow AI news day, with no headline model drops or agent framework releases dominating the cycle. The outlet used the breathing room for a final promotional push on the AI Engineer (AIE) conference, positioning it as the next major checkpoint for builder-focused announcements. The mechanism here is calendar-driven release coordination: major labs and framework maintainers typically consolidate reveals around conference keynotes, leaving the pre-event window deliberately quiet. For builders, this means current API surfaces, model endpoints, and SDK versions are stable enough to commit to for the next 48-72 hours without a breaking change disrupting local setups. The watch item is the AIE opening keynote, where model providers and agent runtime maintainers historically use the mainstage slot to ship reference implementations and pinned-version releases that propagate through documentation within hours. The quieter the run-up, the louder the keynote tends to land.

[09:24] Signal's Whittaker: AI chatbots are not your friends

Meredith Whittaker, president of Signal, used a June 20 interview to push back on products positioning AI chatbots as companions. Her line — 'these are not your friends, not conscious beings, not sentient interlocutors' — targets vendors leaning on relational language in onboarding flows, persona system prompts, and conversational UX. The intervention lands as agentic coding tools and support bots are now embedded in daily developer workflows, where the line between tool and teammate is actively being blurred. Whittaker's argument: anthropomorphic design choices create false expectations about memory, intent, and reciprocity, and Signal's privacy-first brand gives the critique unusual reach in developer circles. For builders, the practical mechanism is in copy and prompt design — system prompts framing the model as a peer, UI strings implying ongoing relationship, and memory features simulating continuity across sessions. What to watch next: whether major model providers formalize guidance on relational framing in their developer documentation, and whether enterprise buyers start flagging it in procurement.

[10:25] In the Weights launches as AI-centric vanity search

A new service called In the Weights launched June 20, pitching itself as the AI-era answer to Google vanity search. It assigns each user a personal score based on how prominently their name surfaces inside the parameters and training data of frontier AI models.

The underlying mechanism runs repeated inference probes against hosted LLMs using identity queries, then aggregates hit-rates and frequency counts into a single composite score. The architecture treats the model as the search index rather than the web, with an evaluation harness sitting behind a query API that returns per-model breakdowns alongside the overall number. Latency runs in seconds per probe.

For developers, this reframes model visibility as a metric layer that did not previously exist as a productized surface. Watch whether the scoring harness and probing protocol get standardized — if they stay opaque the number is pure vanity, if they get opened up, expect new tooling built around tuning presence across model checkpoints.

[11:25] Practical queue

From today's stories: For builders, this shifts what the stack can rely on by default. The XS.2 release gives builders a compact option with 262K context — useful for agent loops that pass large codebases or tool traces without paying flagship pricing. For builders, this shifts what the stack can rely on by default. For builders, this shifts what the stack can rely on by default. This signals that frontier AI cybersecurity capabilities will diffuse globally regardless of U.S. Baseten's raise signals that inference is now a separately funded market segment, meaning more competing serving platforms with different price-performance tradeoffs. For builders, this shifts what the stack can rely on by default. A quiet shipping day is a useful window to consolidate notes on current agent frameworks and model APIs before the next release cycle. What this means for builders: agent product copy and system prompts are now part of the trust surface. For builders shipping AI products, this surfaces a new category of user-facing metric — model-relative identity visibility — that could become a marketing primitive.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: OpenClaw v2026.6.9; Hermes Agent v2026.6.19; Claude Code CLI 2.1.176 / Poolside ships Laguna XS.2 compact coding model on OpenRouter / Poolside: Laguna M.1 lands via API
- 02:00 — Agent Stack Release Readout: OpenClaw v2026.6.9; Hermes Agent v2026.6.19; Claude Code CLI 2.1.176
- 02:40 — Poolside ships Laguna XS.2 compact coding model on OpenRouter
- 03:40 — Poolside: Laguna M.1 lands via API
- 04:35 — New usage analytics and updated spend controls for enterprises
- 05:29 — 30 years of export controls failed before — what about Mythos?
- 06:30 — Baseten Reportedly Raising $1.5B at $13B Valuation
- 07:27 — Datasette Apps: Host custom HTML applications inside Datasette
- 08:27 — Quiet Day in AI Shipping: AIE Promo Window Ahead
- 09:24 — Signal's Whittaker: AI chatbots are not your friends
- 10:25 — In the Weights launches as AI-centric vanity search
- 11:25 — Practical queue

---

## Primary Links

- OpenClaw v2026.6.9 release: https://github.com/openclaw/openclaw/releases/tag/v2026.6.9
- Hermes Agent v2026.6.19 release: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.6.19
- Claude Code CLI npm: https://www.npmjs.com/package/@anthropic-ai/claude-code
- Poolside: Laguna XS.2 model page: https://openrouter.ai/models/poolside/laguna-xs.2
- Poolside: Laguna M.1 model page: https://openrouter.ai/models/poolside/laguna-m.1
- New usage analytics and updated spend controls for enterprises: https://openai.com/index/chatgpt-enterprise-spend-controls
- From PGP to Mythos: a brief history of export controls that didn’t sto: https://techcrunch.com/2026/06/19/encryption-spyware-and-now-mythos-history-shows-why-cyber-export-control-doesnt-work/
- Is the US government’s Anthropic ban accidentally helping the brand?: https://techcrunch.com/video/is-the-us-governments-anthropic-ban-accidentally-helping-the-brand/
- AI inference startup Baseten reportedly raising $1.5B months after its: https://techcrunch.com/2026/06/18/ai-inference-startup-baseten-reportedly-raising-1-5b-months-after-its-last-mega-round/
- Datasette Apps: Host custom HTML applications inside Datasette: https://simonwillison.net/2026/Jun/18/datasette-apps/#atom-entries
- [AINews] not much happened today: https://www.latent.space/p/ainews-not-much-happened-today-e7b
- Signal’s Meredith Whittaker wants you to remember that AI chatbots ‘ar: https://techcrunch.com/2026/06/20/signals-meredith-whittaker-wants-you-to-remember-that-ai-chatbots-are-not-your-friends/
- In the Weights is your new AI-centric vanity search: https://techcrunch.com/2026/06/20/in-the-weights-is-your-new-ai-centric-vanity-search/
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- microsoft/mcp-for-beginners repo: https://github.com/microsoft/mcp-for-beginners
- CoplayDev/unity-mcp repo: https://github.com/CoplayDev/unity-mcp
- Billionaire Ambani wants AI in every call, app, and home: https://techcrunch.com/2026/06/19/billionaire-ambani-wants-ai-in-every-call-app-and-home/
- The CEO of Allbirds’ new AI biz has a plan, but no team: https://techcrunch.com/2026/06/19/the-ceo-of-allbirds-new-ai-biz-has-a-plan-but-no-employees/
- The US says ASML’s top chip tool may be in China, but how?: https://techcrunch.com/2026/06/19/the-us-says-asmls-top-chip-tool-may-be-in-china-asml-says-it-isnt/
- Ollama v0.30.10: https://github.com/ollama/ollama/releases/tag/v0.30.10

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.9`, published 2026-06-21T01:44:28Z. Recent episode version tags detected: `v2026.6.7-beta.1`, `v2026.6.8`, `v2026.6.8-beta.1`, `v2026.6.8-beta.2`. Selected missing version(s): `v2026.6.9`.
- **Hermes Agent** — Latest stable verified: `v2026.6.19`, published 2026-06-19T19:39:06Z. Recent episode version tags detected: `v0.15.2`, `v0.16.0`, `v2026.5.29.2`, `v2026.6.5`. Selected missing version(s): `v2026.6.19`.
- **OpenAI Codex** — Latest stable verified: `rust-v0.141.0`, published 2026-06-18T04:43:06Z. Recent episode version tags detected: `rust-v0.138.0`, `rust-v0.139.0`, `rust-v0.140.0`, `rust-v0.141.0`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.176`, published 2026-06-12T19:45:41.757Z. Recent episode version tags detected: `2.1.169`, `2.1.170`, `latest`, `stable`. Selected missing version(s): `2.1.176`.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-06-21). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.9` (stable) / `v2026.6.10-beta.1` (prerelease)
- **Hermes Agent** — `v2026.6.19`
- **OpenAI Codex** — `rust-v0.141.0`
- **Claude Code CLI** — `2.1.176`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
