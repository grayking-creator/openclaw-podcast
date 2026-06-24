# AgentStack Daily EP074 — Codex 0.142 Stable, Daybreak & GPT-5.5-Cyber, Samsung Codex, Nex-N2-Pro

**Title:** OpenAI Codex 0.142 Stable, Daybreak Security Suite, Samsung Rolls Out Codex, Nex-N2-Pro, Reflection AI x SpaceX

**Tagline:** OpenAI Codex 0.142 lands the first stable release of the 0.142 line, with usage-limit reset credits, organized plugin surfaces, and configurable rollout token budgets. OpenAI Daybreak ships Codex Security and GPT-5.5-Cyber as a new vulnerability-finding initiative, plus the Patch the Planet program for open-source maintainers. Samsung Electronics is rolling out ChatGPT Enterprise and Codex to its global workforce, one of OpenAI's largest enterprise deployments. Nex AGI listed Nex-N2-Pro on OpenRouter, a 397B MoE built on Qwen3.5. sqlite-utils 4.0rc1 adds schema migrations and nested transactions. iOS 27 pushes practical AI features below the Siri surface. SpaceX signed Reflection AI to a $150M/month compute deal. Groq confirmed a $650M raise. The "loopy" agent pattern is taking off in production.

**Feed description:** OpenAI Codex 0.142 is the new stable, with usage-limit reset credits, organized plugins, and rollout token budgets. OpenAI's Daybreak initiative brings Codex Security and GPT-5.5-Cyber for vulnerability discovery, plus Patch the Planet for open-source maintainers. Samsung is rolling out ChatGPT Enterprise and Codex globally, and Nex AGI listed Nex-N2-Pro on OpenRouter. sqlite-utils ships migrations and nested transactions in 4.0rc1, iOS 27 brings practical AI features below the Siri surface, SpaceX inked a $150M/month compute deal with Reflection AI, and Groq confirmed a $650M raise. Also: the agentic "loopy" pattern, Fika Jobs' AI interview agents, and Z.ai's GLM-5V Turbo multimodal agent model.

---

## Story Slate

### 1. **Agent Stack Release Readout: OpenAI Codex rust-v0.142.0**
Technical depth angle: Codex 0.142 is the first stable on the 0.142 line, shipped 2026-06-22. The CLI now tracks usage across agent threads, surfaces remaining-budget reminders, and aborts turns when a configured rollout token budget is exhausted; the `/usage` command can show and redeem earned usage-limit reset credits, with confirmation, retry, and refreshed availability states; the `/plugins` command groups remote plugins into OpenAI Curated, Workspace, and Shared with me, and eligible turns can recommend and install relevant plugins from that grouped surface.
Actionability angle: This release turns a long agent run from a soft-bounded thing into a hard-bounded one, which is the change that makes overnight Codex jobs a real production pattern instead of a demo.
Listener hook: If you've ever had a Codex thread die on a mid-run rate limit, this is the release that finally lets the run recover in the same session.

### 2. **OpenAI Daybreak launches Codex Security and GPT-5.5-Cyber**
Technical depth angle: Daybreak is an OpenAI initiative that pairs Codex Security (the agent loop for vulnerability discovery, validation, and patch proposal) with GPT-5.5-Cyber (a new model trained for cybersecurity reasoning). The combination is meant to compress the find-to-fix cycle: Codex Security finds the candidate vulnerability, GPT-5.5-Cyber reasons about exploitability and patch correctness, and the resulting patch is reviewed before disclosure.
Actionability angle: For any team shipping AI-assisted security tooling, the dedicated cyber model behind the patch-validation step shrinks a common failure mode where the model proposes a fix that looks right but does not actually close the original exploit path.
Listener hook: This is the first time a frontier lab has put a dedicated cyber model behind a coordinated-disclosure agent, and the disclosure cadence over the next quarter will tell us if it works.

### 3. **OpenAI Patch the Planet: AI-assisted vulnerability repair for open source**
Technical depth angle: Patch the Planet is the companion initiative to Daybreak, aimed at the long tail of under-maintained open-source projects where most of the supply-chain risk lives. The mechanism is a maintainer-first workflow: maintainers bring a project into the program, get AI-assisted triage on incoming vulnerability reports, and get expert review on proposed patches; OpenAI provides the model time and the workflow surface, and the actual fix lands in the maintainer's repo on the maintainer's terms.
Actionability angle: A lot of the open-source code in a typical agent stack is maintained by volunteers with limited security bandwidth, and a coordinated program aimed at that tail is the kind of intervention that turns the supply-chain picture around in six to twelve months.
Listener hook: The projects your agent stack depends on are about to get a much better security review pipeline, if the disclosure cadence holds.

### 4. **Samsung Electronics brings ChatGPT Enterprise and Codex to employees**
Technical depth angle: Samsung Electronics is deploying ChatGPT Enterprise and Codex to its global workforce, making it one of OpenAI's largest enterprise AI rollouts. The deployment places a general enterprise assistant alongside a coding agent inside a company that spans consumer devices, chips, displays, software, and manufacturing systems; permissions, repository access, review policies, and audit trails become the real integration work, not the chat surface.
Actionability angle: Once a company of Samsung's scale standardizes on ChatGPT Enterprise and Codex, other large employers can point to a reference pattern for rolling agentic coding into corporate environments, which moves coding agents from optional power-user tools to sanctioned internal infrastructure.
Listener hook: This is the largest signal yet that coding agents are sanctioned enterprise infrastructure, and the integration shape is the one other large employers will copy.

### 5. **Nex AGI lists Nex-N2-Pro on OpenRouter as a 397B MoE on Qwen3.5**
Technical depth angle: Nex-N2-Pro is an agentic mixture-of-experts model from Nex AGI, with 17B active parameters out of 397B total, built on the Qwen3.5 architecture; it accepts text and image input, supports a 262,144-token context, and is exposed through OpenRouter so it can be added to an existing model router without a direct vendor integration.
Actionability angle: The first useful signal will come from real agent traces (tool selection, recovery after wrong turns, visual input handling, long-context coherence on sessions that include code, requirements, logs, and prior decisions), and the right move is to evaluate it as a new candidate rather than promote it to a default.
Listener hook: A new large-context multimodal MoE just landed on the OpenRouter surface; route one coding-agent session through it before it becomes a default.

### 6. **sqlite-utils 4.0rc1 adds migrations and nested transactions**
Technical depth angle: sqlite-utils is a Python library and CLI for working with SQLite, and the 4.0rc1 release adds schema migrations and nested transaction support on top of the existing higher-level operations like table transformations and automatic table creation from JSON-shaped payloads. Migrations make schema evolution a first-class operation in the tool rather than hand-written setup logic, and nested transactions give application code more precise control over partial operations when helper functions need transactional behavior inside a larger transaction.
Actionability angle: SQLite keeps showing up in serious local and edge workflows, and a stronger sqlite-utils layer makes those workflows less ad hoc, but the right move is to treat 4.0rc1 as a preview of the 4.0 API before depending on it for production migrations.
Listener hook: If your agent stack stores state in SQLite, the 4.0 release candidate is the right place to start testing schema migrations on a side project.

### 7. **iOS 27 practical AI features land outside the Siri surface**
Technical depth angle: iOS 27 ships practical AI features across Mail, Photos, Notes, and Spotlight, using on-device Foundation Models for most requests with Private Cloud Compute as the fallback for heavier work. The developer surface is App Intents, with new intent types for summarization, generation, and semantic search; Spotlight now uses local vector embeddings for natural-language queries against on-device content, replacing keyword-only search.
Actionability angle: This opens a path to ship privacy-first AI features without managing model serving infrastructure, and the watch item is how much of the on-device runtime becomes available to third-party developers beyond curated App Intents paths.
Listener hook: The iPhone AI features that are actually useful are landing below the Siri surface, and the developer SDK is the one to track.

### 8. **SpaceX inks $150M/month compute deal with Reflection AI**
Technical depth angle: SpaceX signed a compute deal with Reflection AI, an open-source AI lab, that runs $150 million per month from July 1, 2026 through 2029; Reflection gets immediate access to Nvidia GB300 AI chips and supporting hardware across SpaceX's Colossus 2 data center near Memphis, Tennessee. The allocation is on the current top-end Nvidia silicon for AI training and inference, giving Reflection runway to train and serve at a scale that open-source labs usually have to negotiate piecemeal.
Actionability angle: The deal is a real validation of SpaceX's neocloud business alongside its launch business, and for builder-stack watchers the practical implication is that neocloud capacity is starting to look like a sustained layer of the AI infrastructure market rather than a side project.
Listener hook: A $150M-per-month open-source lab commitment is the clearest signal yet that neocloud is a real layer of the AI infrastructure market, not a side project.

### 9. **Groq confirms $650M raise and re-staffs after Nvidia's non-acqui-hire**
Technical depth angle: AI chipmaker Groq confirmed a $650M raise and is re-staffing after Nvidia's $20B not-acqui-hire deal. The mechanism is a deliberate neocloud pivot: Groq's LPU inference silicon is well-suited to high-throughput, low-latency serving, and the neocloud business sells that capability to teams that do not want to run their own Groq hardware; the raise funds both continued silicon development and the operational expansion of the neocloud side.
Actionability angle: Together with the SpaceX-Reflection deal, Groq's raise suggests the inference market is moving from a few hyperscalers to multiple specialized inference providers at the top end, which gives routing logic more to work with and builders more places to put cost-sensitive workloads.
Listener hook: The top end of the inference market is fragmenting into specialized providers, and Groq is one of the new options for latency-sensitive serving.

### 10. **The AI world is getting "loopy": always-on agent swarms**
Technical depth angle: The "loopy" pattern is an agentic deployment where a swarm of agents is authorized to work continuously in the background, picking up tasks, making small decisions, and surfacing only when they need a human. Each agent has a defined scope, a defined cost budget, and a defined escalation rule, and the user moves from a synchronous prompt-response loop to a result-review loop with morning check-ins as the human-in-the-loop checkpoint.
Actionability angle: This is the pattern that the rest of the agent stack has to catch up to, and the rollout token budgets in Codex 0.142 are an example of the cost-control piece landing; the watch item is the first production-grade "loopy" agent product aimed at individual builders rather than enterprise teams.
Listener hook: The next year of agent products is going to look less like a chat tool and more like a managed service, and the cost-control layer is what makes it possible.

---

## Model Discovery Check

- **Nex AGI: Nex-N2-Pro** (nex-agi/nex-n2-pro) — Newly listed this cycle (verified 2026-06-22). Primary source: https://openrouter.ai/models/nex-agi/nex-n2-pro. Availability: API via OpenRouter. Capabilities: 262,144 token context; 17B active parameters out of 397B total, mixture-of-experts on a Qwen3.5 base; native text and image input. Selected — this is the marquee new model of the cycle and a meaningful MoE on the OpenRouter surface that builders can route to immediately.

- **Z.ai: GLM-5V Turbo** (z-ai/glm-5v-turbo) — Newly listed this cycle (verified 2026-06-22). Primary source: https://openrouter.ai/models/z-ai/glm-5v-turbo. Availability: API via OpenRouter. Capabilities: 202,752 token context; Z.ai's first native multimodal agent foundation model, purpose-built for vision-based coding and agent-driven tasks. Selected — first-party multimodal move from a major Chinese lab lands in the same week as Nex-N2-Pro, expanding the OpenRouter vision-agent surface for builders.

- **OpenAI: GPT-5.5-Cyber** — Announced as part of Daybreak on 2026-06-22. Primary source: https://openai.com/index/daybreak-securing-the-world. Availability: new cybersecurity model shipped with the Daybreak initiative. Capabilities: vulnerability discovery, exploit reasoning, and patch verification; the model surfaces as a Codex Security backend for the initiative. Decision: Not Selected as a standalone slate story (the model is the engine of the Daybreak story above, so it does not get a separate slate slot). Listed here so the model-discovery lane stays complete.

---

## Local LLM Spotlight

- **Ollama v0.30.10** — https://github.com/ollama/ollama/releases/tag/v0.30.10 — Ollama v0.30.10 brings Cohere's Command A and the North family onto Apple Silicon through the MLX engine, with a refresh of the underlying llama.cpp to build 9672 and fixes for MLX build artifacts. The practical result is a wider set of commercial-grade models that can now be served from a Mac without a discrete GPU, plus a more reliable local-install path on M-series hardware.
  Try now: Pull Command A through the MLX engine on a Mac with `ollama run command-a` and run a multi-turn agent task against it to compare local latency and quality against your usual cloud model.

---

## GitHub Project Radar

- **grab/cursor-talk-to-figma-mcp** — https://github.com/grab/cursor-talk-to-figma-mcp — An MCP integration between AI agents (Cursor, Claude Code, Codex) and Figma, letting an agentic client read Figma designs and modify them programmatically. Stack improvement angle: design and frontend coding agents stop guessing at spacing, colors, or component names because the Figma file becomes a typed tool surface, and a Codex or Claude Code session can push a visual change back into the design system. Try now: install the MCP server in Claude Code, point it at a small Figma file, and ask the agent to rename one component and report the structural change.

- **firecrawl/firecrawl-mcp-server** — https://github.com/firecrawl/firecrawl-mcp-server — The official Firecrawl MCP server, exposing web scraping and search to Cursor, Claude, and any other LLM client. Stack improvement angle: a coding agent gets a clean web-to-markdown and search primitive through MCP, so retrieval-augmented research inside an agent loop stops needing ad hoc scrapers and rate-limit hand-holding. Try now: add the Firecrawl MCP to a Codex or Hermes session and run a focused retrieval task on a single documentation site to compare the result against a manual fetch.

- **MinishLab/semble** — https://github.com/MinishLab/semble — Fast and accurate code search for agents, claiming roughly 98% fewer tokens than grep-plus-read for the same lookup. Stack improvement angle: replaces the "read every file that grep matches" pattern in coding agents with an indexed search layer, which shrinks context and speeds up long sessions on large repositories. Try now: point it at a non-trivial repo on your machine and run a function-name lookup, comparing the tokens used and latency against your usual grep-plus-read flow.

---

## Show Notes

```md
Episode 074 — June 22, 2026

[00:00] Episode hook

OpenAI Codex 0.142 is the new stable, with usage-limit reset credits, organized plugin surfaces, and configurable rollout token budgets that make a long agent run less likely to die on a budget boundary. OpenAI Daybreak landed the same day, pairing Codex Security with a new GPT-5.5-Cyber model and launching Patch the Planet, an initiative that pairs AI-assisted review with human maintainers for open-source vulnerability repair. Samsung Electronics is rolling out ChatGPT Enterprise and Codex to its global workforce. Nex AGI's Nex-N2-Pro is now on OpenRouter as a 397B mixture-of-experts on a Qwen3.5 base. sqlite-utils 4.0rc1 adds schema migrations and nested transactions. iOS 27 brings practical AI features below the Siri surface, SpaceX inked a $150M-per-month compute deal with Reflection AI, and Groq confirmed a $650M raise. The "loopy" agent pattern, where a swarm of agents runs continuously in the background, is starting to show up in production.

[02:00] OpenAI Codex 0.142 stable release

[ALLOY]: OpenAI shipped Codex 0.142 as the new stable, a few days after the 0.142 prerelease line started cycling. This is the version most teams will pin to for the next cycle, and it brings three changes that change how the CLI behaves inside a long run.

[NOVA]: The first is usage-limit reset credits. The `/usage` command can now show and redeem earned reset credits, with confirmation, retry, and refreshed availability states. In practice, that means an agent hit by a mid-run rate limit can recover in the same session instead of waiting on a global timer.

[ALLOY]: The second is plugin organization. The `/plugins` command now groups remote plugins into OpenAI Curated, Workspace, and Shared with me, and eligible turns can recommend and install relevant plugins. The point is less the cosmetic grouping and more that recommendation and install now have a typed, reviewable surface rather than a free-form install step.

[NOVA]: The third is configurable rollout token budgets. The CLI can now track usage across agent threads, provide remaining-budget reminders, and abort turns when a budget is exhausted. For builder workflows that run a Codex thread overnight or behind a coding-agent harness, this turns "the run silently burned through the cap" into an explicit, recoverable boundary.

[02:08] OpenAI Daybreak launches Codex Security and GPT-5.5-Cyber

[ALLOY]: OpenAI announced Daybreak on June 22, a coordinated security initiative that pairs a new model with a new agent surface. The headline pieces are Codex Security, a vulnerability-finding workflow, and GPT-5.5-Cyber, a new model trained for cybersecurity reasoning.

[NOVA]: The mechanism is end-to-end vulnerability work. Codex Security is the agent loop: it finds the candidate vulnerability, validates it, and proposes a patch. GPT-5.5-Cyber is the model that does the harder reasoning about exploitability and patch correctness. The combination is meant to compress the find-to-fix cycle that security teams usually run with separate tools and separate humans.

[ALLOY]: The interesting builder angle is the patch-validation loop. A common failure mode for AI-generated patches is the model proposes a fix that "looks right" but doesn't actually close the original exploit path. With a dedicated cyber model validating the patch, the surface for that failure mode shrinks. That matters for any team shipping AI-assisted security tooling as part of a build pipeline.

[NOVA]: Daybreak is positioned as an open, opt-in program. OpenAI says they will work with security teams to validate and disclose findings responsibly, which puts the initiative in the same operational category as Project Zero or similar coordinated disclosure programs.

[02:14] OpenAI Patch the Planet: AI-assisted vulnerability repair for open source

[ALLOY]: The companion piece to Daybreak is Patch the Planet, an initiative to help open-source maintainers find, validate, and fix vulnerabilities with AI and expert review. The framing is that the long tail of under-maintained open-source projects is where most of the risk lives, and existing security programs do not cover that tail well.

[NOVA]: The mechanism is a maintainer-first workflow. Maintainers can bring a project into the program, get AI-assisted triage on incoming vulnerability reports, and get expert review on proposed patches. OpenAI is providing the model time and the workflow surface; the actual fix lands in the maintainer's repo on the maintainer's terms.

[ALLOY]: For builder-stack teams, the practical implication is that the supply-chain picture gets meaningfully better in the next six to twelve months. A lot of the open-source code in a typical agent stack is maintained by volunteers with limited security bandwidth, and this is the kind of program that turns that around. Watch the disclosure cadence over the next quarter to see which projects actually clear the backlog.

[02:18] Samsung Electronics brings ChatGPT Enterprise and Codex to employees

[ALLOY]: Samsung Electronics is rolling out ChatGPT Enterprise and Codex to employees worldwide, making it one of OpenAI's largest enterprise AI deployments. The important part is not just seat count. It is the combination of a general enterprise assistant with a coding agent surface inside a company that spans consumer devices, chips, displays, software, and manufacturing systems.

[NOVA]: Codex here is not being treated as a novelty. It is being placed into employee workflows where software changes touch hardware programs, internal platforms, product tooling, and probably a long tail of automation scripts. That creates a very different operating environment than a small team using an agent to patch a web service. Permissions, repository access, review policies, and audit trails become the real integration work.

[ALLOY]: The deployment also sends a signal to other large employers. Once a company of Samsung's scale standardizes on ChatGPT Enterprise and Codex, buyers can point to a reference pattern for rolling agentic coding into corporate environments. OpenAI benefits from that proof point, but builders should read it as a shift in expectations: coding agents are moving from optional power-user tools to sanctioned internal infrastructure.

[NOVA]: The risk is uneven adoption. A global rollout does not automatically mean every team gets the same quality of integration. The useful deployments will be the ones that connect Codex to the right source surfaces, issue trackers, review gates, and internal knowledge systems without giving it broad access by default.

[02:25] Nex AGI lists Nex-N2-Pro on OpenRouter as a 397B MoE on Qwen3.5

[ALLOY]: Nex AGI opened Nex-N2-Pro through OpenRouter, giving builders API access to a new agentic mixture-of-experts model. The headline numbers are large: 17 billion active parameters out of 397 billion total, built on the Qwen3.5 architecture. It accepts text and image input, and the listing positions it for agentic workloads where long context and multimodal intake matter.

[NOVA]: The mechanism that matters is provider routing. Because Nex-N2-Pro is available through OpenRouter, a builder can add it behind an existing model router instead of waiting for a direct vendor integration. That means the first adoption path is not a full platform rewrite; it is a new model target in the same inference layer where teams already compare quality, latency, context handling, and cost.

[ALLOY]: The active-versus-total parameter split is also important. Mixture-of-experts models can deliver a large total capacity while activating only part of the network per token. In practice, the open question is whether Nex-N2-Pro's routing gives better agent behavior under multi-step coding, research, and planning sessions, or whether the headline size mainly helps on benchmark-style prompts.

[NOVA]: For builders, this is worth treating as a new candidate, not a new default. The first useful signal will come from real agent traces: tool selection, recovery after wrong turns, visual input handling, and whether its long-context behavior stays coherent when the session includes code, requirements, logs, and prior decisions.

[02:32] sqlite-utils 4.0rc1 adds migrations and nested transactions

[ALLOY]: sqlite-utils reached the 4.0 release-candidate stage with two changes that matter for agent-backed apps: schema migrations and nested transactions. The project already gives Python developers a higher-level way to work with SQLite, including table transformations and automatic table creation from JSON-shaped payloads. The new release candidate pushes it further toward application infrastructure.

[NOVA]: Migrations are the headline because SQLite is often the local state layer for prototypes, agents, small services, evaluation harnesses, and personal automation. When the schema evolves, builders need a predictable way to upgrade the database without hand-writing fragile setup logic. Putting migrations into sqlite-utils makes that path more explicit and easier to wire into deploy steps.

[ALLOY]: Nested transactions are the other practical win. Agent workflows often perform a chain of changes: store a run, add tool events, update a status, attach evaluation results, then recover if one step fails. Nested transaction support gives application code more precise control over partial operations, especially when helper functions need transactional behavior but may run inside a larger transaction.

[NOVA]: The builder relevance is simple: SQLite keeps showing up in serious local and edge workflows because it is fast, portable, and easy to ship. A stronger sqlite-utils layer makes those workflows less ad hoc. The caution is that this is still a release candidate, so teams should treat it as a preview of the 4.0 API before depending on it for production migrations.

[02:40] iOS 27 practical AI features land outside the Siri surface

[ALLOY]: iOS 27 is bringing practical AI features across Mail, Photos, Notes, and Spotlight, instead of putting all the attention on Siri. Apple's approach leans on on-device Foundation Models for most requests, with Private Cloud Compute as the fallback for heavier work. That gives the iPhone a more ambient AI layer: summarization, generation, semantic search, and app-triggered actions woven into places people already work.

[NOVA]: The technical surface for developers is App Intents. Apple is adding intent types for summarization, generation, and semantic search, which lets apps expose actions to system AI without each app building its own cloud model backend. That is a very Apple move: the model becomes part of the platform runtime, and developers wire app behavior into the system layer.

[ALLOY]: Spotlight is especially important because it shifts from keyword search toward local vector embeddings. Natural-language queries against on-device content make the phone feel less like a launcher and more like a personal retrieval system. If it works well, the benefit is not a chatbot moment. It is finding the right note, photo, message, or app content with fewer explicit filters.

[NOVA]: The open question is how much of this becomes available to third-party developers beyond curated App Intents paths. If the public SDK surface stays narrow, Apple gets privacy and consistency but limits experimentation. If it opens more capability, iOS becomes a major deployment target for privacy-first AI features that do not need cloud serving by default.

[02:50] SpaceX inks $150M/month compute deal with Reflection AI

[ALLOY]: SpaceX signed a compute deal with Reflection AI, an open-source AI lab, that runs $150 million per month from July 1, 2026 through 2029. Reflection gets immediate access to Nvidia's latest GB300 AI chips and supporting hardware across SpaceX's Colossus 2 data center near Memphis, Tennessee.

[NOVA]: The mechanism is straightforward hyperscaler-style compute allocation, but the scale is the story. $150M per month sustained across three years is real, and the GB300 generation is the current top-end Nvidia silicon for AI training and inference. That gives Reflection runway to train and serve at a scale that open-source labs usually have to beg for.

[ALLOY]: The interesting angle for builder-stack watchers is what it says about neocloud economics. Colossus 2 is SpaceX's push into being a neocloud provider in addition to its launch business, and a long-term commitment from a real AI lab validates that bet. For builders, the practical implication is that neocloud capacity is starting to look like a sustained layer of the AI infrastructure market rather than a side project.

[NOVA]: Watch the GPU mix over the next quarter. The reflection-vs-GB300 allocation, the lead time on new GB300 racks, and any follow-on deals with other labs will tell us how much real demand exists for neocloud capacity at the top end of the hardware stack.

[02:55] Groq confirms $650M raise and re-staffs after Nvidia's non-acqui-hire

[ALLOY]: AI chipmaker Groq confirmed a $650M raise and is re-staffing after Nvidia's $20B not-acqui-hire deal. The framing in the TechCrunch piece is that the deal with Nvidia was not an acquisition but a hiring arrangement, and Groq used the post-deal clarity to fund the next phase as a neocloud business.

[NOVA]: The mechanism is a deliberate neocloud pivot. Groq's LPU inference silicon is well-suited to high-throughput, low-latency serving, and the neocloud business sells that capability to teams that do not want to run their own Groq hardware. The raise funds both continued silicon development and the operational expansion of the neocloud side.

[ALLOY]: The interesting angle for builder-stack watchers is the inference market structure. Groq, together with the SpaceX-Reflection deal, suggests that we are moving from a market dominated by Nvidia-direct and a few hyperscalers to a market with multiple specialized inference providers at the top end. That gives routing logic more to work with and gives builders more places to put cost-sensitive workloads.

[NOVA]: Groq's LPU is not a substitute for Nvidia GPUs across the board, but for serving specific model architectures and latency profiles, it is a real option. Watch the model-coverage announcements over the next quarter to see which models get first-class Groq support.

[03:00] The AI world is getting "loopy": always-on agent swarms

[ALLOY]: A TechCrunch piece this week described the rise of the "loopy" pattern in agentic AI: instead of an agent that runs when a human asks, a swarm of agents is authorized to work continuously in the background, picking up tasks, making small decisions, and surfacing only when they need a human.

[NOVA]: The mechanism is a longer-horizon agent loop with a controlled autonomy envelope. Each agent in the swarm has a defined scope, a defined cost budget, and a defined escalation rule. The user is not in the synchronous prompt-response loop anymore; the user is in the result-review loop.

[ALLOY]: The interesting angle is the operational shift. A "loopy" deployment looks more like a managed service than a chat tool. There is a heartbeat, an audit log, a kill switch, a cost dashboard, and a set of scheduled check-ins. The agents are running while the user is asleep, and the morning review is the human-in-the-loop checkpoint.

[NOVA]: This is the pattern that the rest of the stack has to catch up to. The agent harnesses are getting there, the memory layers are getting there, the cost controls are getting there, and the rollout token budgets in Codex 0.142 are an example of the cost-control piece landing. Watch the next quarter for the first production-grade "loopy" agent product aimed at individual builders, not just enterprise teams.

[10:00] GitHub Project Radar: Cursor-Talk-To-Figma-MCP, Firecrawl MCP, Semble

[ALLOY]: The GitHub project radar this cycle is heavy on the agent-tooling surface, which makes sense given the rest of the episode. Three repos worth knowing about: grab's cursor-talk-to-figma-mcp, Firecrawl's official MCP server, and MinishLab's Semble for agent-friendly code search.

[NOVA]: The Figma MCP from Grab gives any MCP-compatible agent a typed surface into a Figma file. A coding agent can read a design, understand the component structure, and push changes back. The interesting part is the loop: design changes flow into the agent, the agent makes the code change, and the design system stays in sync. Try it on a small Figma file first to see how cleanly the round-trip works.

[ALLOY]: Firecrawl's MCP server exposes web scraping and search as an MCP tool, which means any agent harness that speaks MCP can do retrieval-augmented research without hand-rolling a scraper. For a coding agent that needs to look up API docs or check the latest version of a library, this turns a multi-step glue-code task into a single tool call. The point is not that Firecrawl is new, it is that it is now first-class on the agent-tooling surface.

[NOVA]: Semble is the code-search pick of the cycle. It indexes a repo and gives agents a fast lookup primitive that uses a fraction of the tokens of a grep-plus-read flow. For long sessions on large repos, that token saving compounds. The interesting test is whether Semble's index quality holds up on messy, real-world codebases or only on clean OSS examples.

[10:30] Practical queue

[ALLOY]: From today's stories: Codex 0.142 lands a stable release with the rollout token budget and the reset-credit redemption that finally make a long agent run a bounded thing. Daybreak and Patch the Planet together suggest that AI-assisted security is moving from research to coordinated disclosure. Samsung's enterprise deployment is the largest signal yet that coding agents are sanctioned infrastructure, not power-user toys. Nex-N2-Pro is the new large MoE worth routing into your evaluation harness, sqlite-utils 4.0rc1 is the right place to start testing schema migrations on a side project before the stable release, and the loopy agent pattern is what the next year of agent products is going to look like.
```

---

## Chapters

- 00:00 — Intro: Codex 0.142 stable, Daybreak lands, Samsung rolls out Codex, Nex-N2-Pro lists
- 02:00 — OpenAI Codex 0.142 stable release
- 02:08 — OpenAI Daybreak launches Codex Security and GPT-5.5-Cyber
- 02:14 — OpenAI Patch the Planet: AI-assisted vulnerability repair for open source
- 02:18 — Samsung Electronics brings ChatGPT Enterprise and Codex to employees
- 02:25 — Nex AGI lists Nex-N2-Pro on OpenRouter as a 397B MoE on Qwen3.5
- 02:32 — sqlite-utils 4.0rc1 adds migrations and nested transactions
- 02:40 — iOS 27 practical AI features land outside the Siri surface
- 02:50 — SpaceX inks $150M/month compute deal with Reflection AI
- 02:55 — Groq confirms $650M raise and re-staffs after Nvidia's non-acqui-hire
- 03:00 — The AI world is getting "loopy": always-on agent swarms
- 10:00 — GitHub Project Radar: Cursor-Talk-To-Figma-MCP, Firecrawl MCP, Semble
- 10:30 — Practical queue

---

## Primary Links

- OpenAI Codex 0.142 stable release: https://github.com/openai/codex/releases/tag/rust-v0.142.0
- OpenAI Daybreak announcement: https://openai.com/index/daybreak-securing-the-world
- OpenAI Patch the Planet announcement: https://openai.com/index/patch-the-planet
- Samsung Electronics ChatGPT + Codex deployment: https://openai.com/index/samsung-electronics-chatgpt-codex-deployment
- Nex AGI: Nex-N2-Pro model page: https://openrouter.ai/models/nex-agi/nex-n2-pro
- Z.ai GLM-5V Turbo model page: https://openrouter.ai/models/z-ai/glm-5v-turbo
- sqlite-utils 4.0rc1 adds migrations and nested transactions: https://simonwillison.net/2026/Jun/21/sqlite-utils-40rc1/
- Beyond Siri: practical AI features in iOS 27: https://techcrunch.com/2026/06/21/beyond-siri-here-are-the-practical-ai-features-coming-to-your-iphone-in-ios-27/
- SpaceX compute deal with Reflection AI: https://techcrunch.com/2026/06/22/spacex-inks-compute-deal-with-reflection-ai-an-open-source-ai-lab/
- Groq confirms $650M raise: https://techcrunch.com/2026/06/22/ai-chipmaker-groq-confirms-650m-raise-re-staffs-after-nvidias-20b-not-acqui-hire-deal/
- The AI world is getting "loopy": https://techcrunch.com/2026/06/22/the-ai-world-is-getting-loopy/
- Fika Jobs raises $4M: https://techcrunch.com/2026/06/23/fika-jobs-raises-4m-to-build-a-video-first-hiring-platform-where-ai-agents-interview-candidates/
- Amazon Alexa+ India Hindi test: https://techcrunch.com/2026/06/22/amazon-is-testing-alexa-in-india-with-hindi-support/
- 2026 tech layoffs citing AI: https://techcrunch.com/2026/06/22/the-running-list-major-tech-layoffs-in-2026-where-employers-cited-ai/
- grab/cursor-talk-to-figma-mcp: https://github.com/grab/cursor-talk-to-figma-mcp
- firecrawl/firecrawl-mcp-server: https://github.com/firecrawl/firecrawl-mcp-server
- MinishLab/semble: https://github.com/MinishLab/semble
- Ollama v0.30.10: https://github.com/ollama/ollama/releases/tag/v0.30.10
- Moebius 0.2B ported to browser via Claude Code: https://simonwillison.net/2026/Jun/22/porting-moebius/
- Codex-maxxing for long-running work (Jason Liu): https://openai.com/index/codex-maxxing-long-running-work
- Google DeepMind $75M + A24 deal: https://techcrunch.com/2026/06/22/google-deepmind-bets-75m-on-ais-future-in-hollywood-with-a24-deal/

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.9`, published 2026-06-21T01:44:28Z. Recent episode version tags detected: `v2026.6.8`, `v2026.6.8-beta.1`, `v2026.6.8-beta.2`, `v2026.6.9`. No new stable release this cycle.
- **Hermes Agent** — Latest stable verified: `v2026.6.19`, published 2026-06-19T19:39:06Z. Recent episode version tags detected: `v0.16.0`, `v2026.5.29.2`, `v2026.6.19`, `v2026.6.5`. No new stable release this cycle.
- **OpenAI Codex** — Latest stable verified: `rust-v0.142.0`, published 2026-06-22T22:19:53Z. Recent episode version tags detected: `rust-v0.138.0`, `rust-v0.139.0`, `rust-v0.140.0`, `rust-v0.141.0`, `rust-v0.142.0`. Selected missing version(s): `rust-v0.142.0`. (Public-facing: introduced as "Codex 0.142" or "Codex zero point one four two"; the literal `rust-v0.142.0` string stays in show notes / links only.)
- **Claude Code CLI** — Latest stable verified: `2.1.177`, published 2026-06-13T01:04:21.745Z. Recent episode version tags detected: `2.1.170`, `2.1.176`, `2.1.177`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-06-22). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.9` (stable) / `v2026.6.10-beta.2` (prerelease)
- **Hermes Agent** — `v2026.6.19`
- **OpenAI Codex** — `rust-v0.142.0`
- **Claude Code CLI** — `2.1.177`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
