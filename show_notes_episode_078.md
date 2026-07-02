# AgentStack Daily EP078 — The Return of Claude Fable 5, OpenClaw and Codex Ship

**Title:** The Return of Claude Fable 5: US Restrictions Lifted; OpenClaw v2026.6.11, Codex rust-v0.142.5, Claude Sonnet 5 on OpenRouter

**Tagline:** Claude Fable 5 is generally available again. Washington dropped the restrictions on Anthropic's Mythos and Fable models on June 30, and the anthropic/claude-fable-5 OpenRouter listing is live with a 1,000,000-token context window, text, image, and file inputs, and reasoning support — the same underlying model as Claude Mythos 5, shipped with additional safeguards on dual-use capabilities. OpenClaw v2026.6.11 and OpenAI Codex rust-v0.142.5 lead the release readout. Anthropic's Claude Sonnet 5 lands on OpenRouter with 1M context and a four-level reasoning-effort dial, and Google ships the Nano Banana 2 Lite image model on the same router. The Orca paper proposes a unified world latent space via next-state prediction, Agents-A1 scales a 35B MoE to trillion-parameter-class performance, OmniRoute consolidates 231 providers behind a single endpoint, BlockPilot tunes diffusion speculative decoding block sizes online, a generative skill composition paper tackles agent skill bottlenecks, and TRIAGE introduces role-typed credit assignment for agentic RL.

**Feed description:** Agent Stack Daily covers the return of Claude Fable 5: US restrictions on Anthropic's Mythos and Fable models were dropped on June 30, and the Mythos-class flagship is back on OpenRouter with 1M context, multimodal input, and reasoning support. OpenClaw v2026.6.11 and OpenAI Codex rust-v0.142.5 shipped, and Claude Sonnet 5 hit OpenRouter with 1M context alongside Google's Nano Banana 2 Lite. Research includes the Orca unified world latent space paper, the Agents-A1 35B MoE, BlockPilot on diffusion speculative decoding, generative skill composition, and TRIAGE on role-typed credit assignment. OmniRoute consolidates 231 providers behind one endpoint.

---

## Story Slate

1. **Agent Stack Release Readout: OpenClaw v2026.6.11; OpenAI Codex rust-v0.142.5**
Agent Stack Release Readout: OpenClaw v2026.6.11; OpenAI Codex rust-v0.142.5. New stable releases this cycle: OpenClaw v2026.6.11; OpenAI Codex rust-v0.142.5. OpenClaw's release is a dependability pass targeting misplaced replies, stuck sends, reconnects, model setup failures, and safer admin defaults; Codex ships a trace-log data-hygiene fix. Both are verified at the primary source (github.com).
Technical depth angle: OpenClaw v2026.6.11 concentrates on channel delivery reliability — delivery and reconnect fixes span Telegram, WhatsApp, Matrix, Google Chat, iMessage, Feishu, Mattermost, WebChat, the Control UI, and the terminal UI — plus agent-session recovery work such as a 180-second default compaction timeout and correct provider-failure lifecycle state. OpenAI Codex rust-v0.142.5 stops full Responses WebSocket request payloads from being written to trace logs.
Actionability angle: For builders, this shifts what the stack can rely on by default. It is worth diffing the changelog against a pinned version before promoting the new default, and the trace-log fix matters for anyone shipping Codex traces into shared observability infrastructure.
Listener hook: Agent Stack Release Readout: OpenClaw v2026.6.11; OpenAI Codex rust-v0.142.5 just changed a surface agent builders touch every day.

2. **Claude Fable 5 Is Back: Washington Lifts the Hold on Anthropic's Frontier Tier**
The US government dropped its restrictions on Anthropic's Mythos and Fable models on June 30, and Claude Fable 5 — the generally available face of the Mythos-class tier — is reachable again. The OpenRouter listing anthropic/claude-fable-5, first posted June 9, shows a 1,000,000-token context window, text, image, and file inputs with text output, and reasoning support, and describes the model as built for autonomous knowledge work and coding. Fable 5 sits above Opus in Anthropic's lineup: it shares the same underlying model as Claude Mythos 5, with additional safety measures for dual-use capabilities, while Mythos 5 remains limited to approved organizations.
Technical depth angle: Fable 5 and Mythos 5 share one underlying model; the difference is the deployment surface. Fable ships with additional safeguards on dual-use capabilities and is generally available, while Mythos 5 is served without those measures to approved organizations only. The OpenRouter identifier is anthropic/claude-fable-5 with a 1,000,000-token context window, multimodal input, and reasoning support. OpenClaw wired in Claude Fable 5 provider support in mid-June, so harness-side integration predates today's availability window.
Actionability angle: For builders this restores a frontier tier above Opus that agent stacks can reach through a router-friendly slug. The immediate question is where Fable 5's autonomous knowledge-work and coding claims beat a current Opus-class default, and whether the dual-use safeguards change behavior on security-adjacent workloads.
Listener hook: The most capable generally available Claude tier just came back from behind a regulatory wall — and your agent stack can route to it with one model-string change.

3. **Claude Sonnet 5 Lands on OpenRouter With 1M Context**
Anthropic's Claude Sonnet 5 has appeared as a new listing on OpenRouter, expanding the Sonnet-class lineup with frontier performance claims across coding, agents, and professional work. The listing shows a 1,000,000-token context window and Anthropic as the serving provider. Adaptive thinking is exposed with selectable reasoning effort levels rather than a fixed thinking mode.
Technical depth angle: The listing exposes adaptive thinking as a selectable parameter with four reasoning effort levels: low, medium, high, and max. Context is set at 1,000,000 tokens via the OpenRouter model identifier anthropic/claude-sonnet-5. Effort selection is per-request rather than a single binary on/off toggle, so each call chooses its own reasoning depth.
Actionability angle: What this means: a single Sonnet-class endpoint now exposes a tunable reasoning dial instead of a binary thinking toggle. Why this matters for builders: cost and latency trade-offs can move into the request itself, letting agent loops pick heavier reasoning only where it pays off.
Listener hook: A single model endpoint just gave you a four-position reasoning dial at a 1M-token context window — that's the shape of the next wave of agent stacks.

4. **Google ships Nano Banana 2 Lite image model on OpenRouter**
Google listed Nano Banana 2 Lite, branded as Gemini 3.1 Flash Lite Image, on OpenRouter under google/gemini-3.1-flash-lite-image. The provider describes it as Google's fastest, most cost-efficient Gemini image model, built for high-velocity developer pipelines and rapid-fire visual exploration. It exposes a 65536-token context window and runs text-to-image generation, targeting use cases where call volume and unit economics matter more than frontier fidelity. The OpenRouter listing makes it drop-in for any image-agent stack already routing through the platform.
Technical depth angle: The model exposes a 65536-token context window paired with a text-to-image generation endpoint surfaced as google/gemini-3.1-flash-lite-image on OpenRouter. The Flash-Lite tier implies a smaller, faster inference path than Pro-class Gemini image models, with Google's own framing emphasizing throughput and cost efficiency over frontier visual quality. The router-friendly slug means call sites can switch providers with a single model-string change.
Actionability angle: What this means: if your image-agent pipelines are bottlenecked on per-image cost or rate limits at the Pro tier, the Flash-Lite endpoint is purpose-built for high call volume. Why it matters: existing OpenRouter clients can absorb the new slug with a model-string change, so integration cost is essentially zero. The trade-off is that frontier fidelity is not the target, so quality-sensitive renders still belong on a heavier model.
Listener hook: If you've been waiting for a Google image model you can actually hammer in a pipeline, this is the one to bench first.

5. **Orca Paper Proposes Unified World Latent Space Through Next-State Prediction**
A new paper called Orca, trending on HuggingFace Daily Papers with 161 upvotes, proposes a unified world latent space built through multimodal next-state-prediction modeling. Hosted at orca-wm.github.io and published as arXiv 2606.30534, the work reframes world modeling by compressing dynamics into a single shared latent and transferring it to downstream tasks, where its authors report beating specialized baselines. The community is reading it because that generality is unusual for a world model.
Technical depth angle: The mechanism is multimodal next-state prediction: the model is trained to predict the next state of a multimodal world input, which forces a single latent to encode world dynamics rather than per-domain features. The resulting representation is then probed on downstream tasks, where the authors report outperforming specialized baselines that were trained per-domain. The arXiv identifier is 2606.30534.
Actionability angle: For builders, the practical signal is that general world-model pre-training is becoming a credible alternative to task-specific stacks, so teams planning agentic or embodied pipelines have a new architectural option worth evaluating. The wider implication: a shared world latent may shift the cost calculus away from per-domain feature engineering over the next 12-18 months.
Listener hook: The Orca paper just hit HuggingFace's Daily Papers with 161 upvotes for proposing a single world model that beats domain-specific ones — here's why builders should care.

6. **Agents-A1: 35B MoE Agent Hits Trillion-Parameter-Class Performance**
InternScience's Agents-A1 is a 35-billion-parameter mixture-of-experts agentic model that claims trillion-parameter-class results through long-horizon trajectory scaling and heterogeneous agent ability scaling. Training runs in three stages: supervised fine-tuning on long agent traces, then per-domain teacher specialization, then multi-teacher distillation into a single 35B student. The paper is trending on HuggingFace's daily feed with 73 upvotes, putting it among the community reads worth tracking this week.
Technical depth angle: The core mechanism is long-horizon trajectory scaling — training on extended multi-turn agent sequences rather than single-step prompts. Heterogeneous agent ability scaling mixes per-domain specialist teachers (coding, tool use, retrieval) then distills them into one 35B MoE student. The three-stage pipeline (SFT on long traces → per-domain teacher models → multi-teacher distillation) is the actual contribution; the 35B parameter count is the cost, not the trick.
Actionability angle: This matters because frontier agent performance may no longer require trillion-parameter serving budgets — specialist-teacher distillation recipes can compress frontier capability into deployable sizes. The pattern matters for any team running cost-sensitive agent pipelines, where a 'specialist teacher → small student' recipe can replace a much larger proprietary model on tool-use workloads.
Listener hook: This HuggingFace daily paper hit 73 upvotes for claiming a 35B agent matches trillion-parameter performance — and the recipe, not the parameter count, is the real contribution.

7. **OmniRoute Turns One Endpoint Into 231 Model Providers**
A new open-source AI gateway, OmniRoute, hit GitHub Trending this week, letting developers route Claude Code, Codex, Cursor, Cline, and Copilot through a single OpenAI-compatible endpoint backed by 231 providers, roughly 50 with free tiers. The project ships a smart auto-fallback layer and a stacked token-compression pipeline (RTK plus Caveman mode) the author claims cuts usage 15-95%.
Technical depth angle: Single OpenAI-compatible endpoint fronting 231+ model providers. The token-compression pipeline stacks RTK with Caveman mode, applied to prompts before they reach upstream providers, with reported savings between 15% and 95%. Auto-fallback reroutes rate-limited or failed requests to the next available provider. MCP and A2A compatibility preserves tool-calling and agent-to-agent message passing. Ships as a Desktop app and PWA.
Actionability angle: This is a self-hosted routing layer that sits between a coding agent and upstream model APIs, so a single OpenAI-compatible base URL replaces provider-by-provider client config. What this means for builders running long agentic loops: a stalled or rate-limited request can be rerouted to a free tier before failing, and token compression reduces the spend on every call. Why it matters — swapping one base URL keeps existing Claude Code or Codex configuration intact.
Listener hook: One open-source repo collapses 231 model providers — about 50 of them free — into a single OpenAI-compatible endpoint your coding agent already speaks to.

8. **BlockPilot Picks Block Sizes Live for Diffusion Speculative Decoding**
BlockPilot is a research paper trending on HuggingFace Daily Papers proposing instance-adaptive policy learning for diffusion-based speculative decoding. The method predicts optimal block sizes from prefilling representations, dynamically choosing how many tokens to draft per step rather than using a fixed schedule. The authors report significant speedup over static block-size approaches with minimal overhead, and the paper is pulling attention from the inference community for making block size a learned, per-request decision. The repo is open-sourced on GitHub by the AMAP-ML group alongside the arXiv preprint, and the work has pulled 64 upvotes on the HF daily feed.
Technical depth angle: The core mechanism is a policy network that ingests prefilling-stage hidden states and outputs a per-instance block size for the diffusion drafter. Rather than committing to a fixed draft length, BlockPilot conditions the speculation depth on what the prompt actually looks like, then runs the diffusion drafter for that many tokens before the target model verifies. The repo ships training scripts and the released policy, and the policy overhead is reported as a small fixed fraction of step time.
Actionability angle: What this means: if you run diffusion-based drafters today, block size is a knob you tune once per deployment — BlockPilot argues it should be a learned, per-request decision driven by the prompt's prefilling representations. Why this matters: the speedup comes from the same draft budget being spent more intelligently, not from extra model capacity, so the technique could slot into existing speculative-decoding pipelines without retraining the target model. Watch whether the released policy generalizes across model families or only holds inside the paper's training distribution.
Listener hook: A HuggingFace paper with 64 upvotes is making the case that diffusion speculative decoding's biggest remaining lever isn't the drafter — it's choosing how many tokens to draft per request.

9. **Generative Skill Composition Tackles LLM Agent Skill Bottleneck**
arXiv paper 2606.32025 from Xinyu Zhao, Zhen Tan, and Vaishnav Tadiparthi reframes LLM agent skill composition as the central bottleneck as procedural skill libraries scale. The paper proposes generative skill composition, where the model synthesizes skill combinations on the fly rather than retrieving from a fixed pool or dumping the full library into context. It targets the gap between full-context exposure, which burns tokens, and embedding-based retrieval, which misses compositions across skills.
Technical depth angle: The paper contrasts two existing paradigms: full-context exposure where the agent's reasoning sees every skill, and embedding-based retrieval that ranks candidates. Generative skill composition replaces both with model-synthesized combinations generated on demand for the task. The shift reframes skill selection as a generation problem rather than a retrieval ranking problem — the agent reasons about how to combine skills instead of picking the closest match from a fixed pool.
Actionability angle: For builders running agent stacks with growing skill libraries, this signals a shift away from brute-force context stuffing and embedding retrieval toward generation-based composition. What this means is that the bottleneck is shifting from how many skills you can store to how well your model can synthesize the right combination for the task. Why this matters: skill library structure and composition scaffolding now carry more weight than raw library breadth.
Listener hook: If your agent stack has a skill library that's grown past a dozen entries, the composition strategy is now the load-bearing decision.

10. **TRIAGE Paper Proposes Role-Typed Credit Assignment for Agentic RL**
TRIAGE, a new framework from Yuanda Xu, Zhengze Zhou, and Hejian Sang (arXiv 2606.32017), adds a semantic role axis to credit assignment in agentic reinforcement learning. Standard GRPO uses the final verifier outcome as a uniform advantage across every action token, conflating search, click, edit, navigation, and object-interaction steps. TRIAGE inserts a structured judge that classifies each rollout segment by role before advantage is computed, so decision-bearing and execution steps receive different updates. The reported gains concentrate where rollouts depend on dense tool use. This positions role classification, not the verifier, as the new optimization lever for agentic RL pipelines.
Technical depth angle: GRPO's policy-gradient update treats every action token in a rollout as carrying the same scalar advantage, set from the final verifier. TRIAGE sits between the rollout and the gradient: a structured LLM judge tags each segment (search, click, edit, navigation, object interaction) with a role label, and the advantage becomes role-conditional rather than uniform. This is a credit-assignment change, not a reward change. Concrete mechanism worth tracking: how the role-conditioned advantage is normalized across heterogeneous action types without exploding variance on long tool-use trajectories.
Actionability angle: For builders training agent policies with RL, this reframes credit assignment, not verifier quality, as the next optimization lever. What this means in practice: teams running GRPO-style loops with heavy tool calls should expect the marginal gain on a given run to come from how action tokens are weighted, not from a stronger reward model. For shipped pipelines today, the practical implication is that role-aware credit could be bolted onto existing rollouts without changing the reward function itself.
Listener hook: If your agent runs twenty tool calls per step and only a handful actually decide the outcome, GRPO is currently training against the wrong credit.

---

## Model Discovery Check

- **Anthropic: Claude Fable 5** (anthropic) — Availability restored this cycle (verified July 01, 2026). Primary source: https://openrouter.ai/models/anthropic/claude-fable-5. Announcement: https://www.anthropic.com/news/claude-fable-5-mythos-5. Restriction coverage: https://techcrunch.com/2026/06/30/trump-drops-restrictions-on-anthropics-mythos-and-fable-models/. Availability: API via OpenRouter. Capabilities: context length 1000000; Fable 5 is a Mythos-class model built for autonomous knowledge work and coding, with text, image, and file inputs, text output, and reasoning support; same underlying model as Claude Mythos 5 with additional dual-use safeguards. Try now / integration angle: route a coding-agent session through https://openrouter.ai/models/anthropic/claude-fable-5 to evaluate it against current defaults. Decision: Selected — flagship-tier availability change this cycle; leads the episode.

- **Anthropic: Claude Sonnet 5** (anthropic) — Newly listed this cycle (verified July 01, 2026). Primary source: https://openrouter.ai/models/anthropic/claude-sonnet-5. Availability: API via OpenRouter. Capabilities: context length 1000000; Sonnet 5 is Anthropic's most capable Sonnet-class model, with frontier performance across coding, agents, and professional work. It supports adaptive thinking with selectable reasoning effort levels (low, medium, high, m. Try now / integration angle: route a coding-agent session through https://openrouter.ai/models/anthropic/claude-sonnet-5 to evaluate it against current defaults. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **Google: Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image)** (google) — Newly listed this cycle (verified July 01, 2026). Primary source: https://openrouter.ai/models/google/gemini-3.1-flash-lite-image. Availability: API via OpenRouter. Capabilities: context length 65536; Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image) is Google's fastest, most cost-efficient Gemini image model, built for high-velocity developer pipelines and rapid-fire visual exploration. It delivers text-to-image gener. Try now / integration angle: route a coding-agent session through https://openrouter.ai/models/google/gemini-3.1-flash-lite-image to evaluate it against current defaults. Decision: Selected — new major-provider model not featured on a recent broadcast.

---

## Local LLM Spotlight

- **Ollama v0.31.1** — https://github.com/ollama/ollama/releases/tag/v0.31.1 — Ollama v0.31.1 ships a major Apple Silicon speedup for Gemma 4 by leaning on multi-token prediction (MTP), which drafts several tokens per forward pass and then verifies them in parallel. Across a coding-agent benchmark, generation is roughly 90% faster on M-series hardware, while the existing one-binary local workflow and API contracts carry over unchanged.
  Try now: Pull the gemma4 model on an M-series Mac, run a code-completion prompt through `ollama run`, and time tokens-per-second against the same prompt on v0.30.x to see the MTP delta firsthand.

---

## GitHub Project Radar

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — fastmcp is a Pythonic framework for building Model Context Protocol servers and clients, with FastAPI-style ergonomics for declaring tools, resources, and prompts. It targets developers who want to wire agents into typed, inspectable services without hand-rolling the JSON-RPC plumbing.
  Stack improvement angle: Drop it into a Hermes or Codex agent stack to expose internal tools as a schema-validated MCP server, so any MCP-compatible client (Claude Code included) discovers them through a typed interface rather than ad-hoc function calls.
  Try now: Install the package and run the example weather server, then point Claude Code at it via a custom MCP config entry to confirm tool discovery end to end.

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — codebase-memory-mcp is a single static binary that indexes any repository into a persistent knowledge graph and answers structural queries in under a millisecond across 158 languages. It claims roughly 99% fewer tokens than re-feeding raw source to a model.
  Stack improvement angle: Mount it beneath an OpenClaw or Codex agent as the long-lived code-retrieval layer, so navigation queries resolve against the graph instead of triggering fresh embeddings on every turn.
  Try now: Pull the static binary, point it at a mid-sized repo, and issue a 'where is X defined' query from any MCP-capable client to see the latency profile.

- **microsoft/mcp-for-beginners** — https://github.com/microsoft/mcp-for-beginners — mcp-for-beginners is a multi-language curriculum that walks through the Model Context Protocol with worked examples in C#, Java, TypeScript, JavaScript, Rust, and Python. Lessons focus on practical patterns for building modular, scalable, and secure agent workflows.
  Stack improvement angle: Use the lab exercises to stand up an MCP client/server pair in whichever runtime matches your stack, then port the auth and tool-scoping patterns into a production deployment.
  Try now: Clone the repo and complete the first Python lab to build and call a minimal MCP server from a sample client.

---

## Extra Research Candidates

- **mukul975/Anthropic-Cybersecurity-Skills — 817 structured cybersecurity skills for AI agents · Mapped to 6 frameworks: MITR** — https://github.com/mukul975/Anthropic-Cybersecurity-Skills — 817 structured cybersecurity skills for AI agents · Mapped to 6 frameworks: MITRE ATT&amp;CK, NIST CSF 2.0, MITRE ATLAS, D3FEND, NIST AI RMF &amp; MITRE F3 (Fight Fraud) · agentskills.io standard · Works with Claude Code, GitHub Copilot, Co Technical depth angle: Each skill ships as an agentskills.io-formatted markdown manifest tagged against MITRE ATT&CK, NIST CSF 2.0, ATLAS, D3FEND, AI RMF, and F3, giving agents a fixed 817-procedure taxonomy across 29 security domains to dispatch on.

- **AxDafny: Agentic Verified Code Generation in Dafny** — https://arxiv.org/abs/2606.32007 — We study agentic code generation in Dafny, where a model must generate both executable code and the proof artifacts for verification. We present AxDafny, a verifier-guided repair framework that iteratively generates implementations, invaria Technical depth angle: Verifier-in-the-loop repair alternates between Dafny's SMT-backed checker and an LLM proposer, with the verifier's counterexamples seeding each new round of invariant, assertion, and termination-argument generation.

- **Surrogate Fidelity: When Can Open LLMs Explain Closed Ones?** — https://arxiv.org/abs/2606.32008 — Mechanistic interpretability (MI) requires full access to model internals, yet the APIs for most widely deployed language models at best expose log-probabilities over output tokens. This creates a surrogate problem: when do measurements mad Technical depth angle: Open-weight models act as measurement probes, with binary-task log-odds treated as API-compatible scalars and leave-one-out attribution used to bound when mechanistic claims transfer to closed models across eleven LLMs.

---

## Show Notes

```md
Episode 078 — July 01, 2026

[00:00] Episode hook

Claude Fable 5 is generally available again — Washington dropped the restrictions on Anthropic's Mythos and Fable models on June 30, and the anthropic/claude-fable-5 listing on OpenRouter is live with a 1,000,000-token context window. On the release front, OpenClaw v2026.6.11 and OpenAI Codex rust-v0.142.5 both shipped this cycle: OpenClaw with a dependability pass across channel delivery and session recovery, Codex with a trace-log data-hygiene fix. Anthropic's Claude Sonnet 5 also surfaced on OpenRouter with a 1M-token context window and a four-level reasoning-effort dial, and Google listed Nano Banana 2 Lite — branded Gemini 3.1 Flash Lite Image — as its fastest, most cost-efficient Gemini image model. On the research side, the Orca paper is trending on HuggingFace Daily Papers with 161 upvotes for proposing a unified world latent space built through multimodal next-state prediction, and InternScience's Agents-A1 claims trillion-parameter-class agent performance from a 35-billion-parameter mixture-of-experts student.

[02:00] Agent Stack Release Readout: OpenClaw v2026.6.11; OpenAI Codex rust-v0.142.5

Two stable releases landed this cycle. OpenClaw v2026.6.11 is a dependability release: the team frames it as a direct response to feedback about the rough edges that make the harness feel less reliable, with fixes for misplaced replies, stuck sends, dropped reconnects, model setup failures, and safer admin defaults. The largest block of work is channel delivery reliability, with delivery and reconnect fixes spanning Telegram, WhatsApp, Matrix, Google Chat, iMessage, Feishu, Mattermost, WebChat, the Control UI, and the terminal UI. The concrete mechanisms matter here: newer Google Chat direct messages stop being treated like group conversations and reach the correct one-to-one chat; Telegram webhook users keep receiving DMs and group messages through channel restarts, configuration reloads, and recovery cycles without temporary blackouts; Matrix end-to-end-encrypted gateways stay online during long-running use instead of gradually consuming memory until a crash takes channels and in-flight work down; and heartbeat checks on reasoning-capable models now surface the assistant's intended reply instead of leaking internal reasoning into Telegram and WhatsApp. On the agent-runtime side, the release lowers the default compaction timeout to 180 seconds while respecting explicit configuration, preserves Codex context-engine compaction ownership, and keeps provider-failure terminal lifecycle state correct. OpenAI Codex rust-v0.142.5 is a focused patch with real operational weight: it prevents full Responses WebSocket request payloads from being written to trace logs, a data-hygiene fix that matters to anyone shipping Codex traces into shared observability infrastructure, backported deliberately to the release/0.142 line. For builders, the practical question is whether either release changes a default you currently depend on: diff the changelog against your pinned version, replay a representative agent session, and watch reconnect behavior before promoting the new default in production.

[03:05] Claude Fable 5 Is Back: Washington Lifts the Hold on Anthropic's Frontier Tier

The headline of the day: Claude Fable 5 is generally available again. The US government dropped its restrictions on Anthropic's Mythos and Fable models on June 30, ending the export regime that had kept Anthropic's frontier tier gated for weeks. Fable 5 is the generally available face of the Mythos-class tier — a tier that sits above Opus in Anthropic's lineup. It shares the same underlying model as Claude Mythos 5; the difference is the deployment surface. Fable ships with additional safety measures for dual-use capabilities, while Mythos 5 is served without those measures to approved organizations only. The OpenRouter listing at anthropic/claude-fable-5, first posted June 9, shows the concrete capabilities: a 1,000,000-token context window, text, image, and file inputs with text output, reasoning support, and positioning for autonomous knowledge work and coding. Harness-side support is already in place — OpenClaw wired in Claude Fable 5 provider support in mid-June, so routing an agent session to the model is a model-string change, not an integration project. For builders the immediate move is a bake-off: run a representative coding or long-horizon agent task through anthropic/claude-fable-5 against a current Opus-class default and measure where the Mythos-class claims hold. Watch next: pricing and rate limits as availability stabilizes, whether the dual-use safeguards are observable on security-adjacent workloads, and how quickly the policy environment settles — the same administration that dropped these restrictions has changed course before.

[04:10] Claude Sonnet 5 Lands on OpenRouter With 1M Context

Anthropic has surfaced Claude Sonnet 5 as a new model listing on OpenRouter, billed as the most capable Sonnet-class model yet across coding, agents, and professional work. The model is served by Anthropic itself and registers at the identifier anthropic/claude-sonnet-5. Two details stand out for builders. First, the context window is 1,000,000 tokens, putting Sonnet 5 in the same long-context tier as recent frontier releases and large enough to hold substantial repositories or multi-session agent traces in a single call. Second, adaptive thinking is exposed as a selectable parameter with four reasoning effort levels — low, medium, high, and max — letting callers dial compute up or down per request rather than committing to a fixed mode. That combination reframes a Sonnet-class endpoint as a tunable cost-and-quality surface for agent loops. Watch next: how OpenRouter surfaces the effort parameter in its unified API, and whether the Anthropic-native SDK mirrors the same four-step dial.

[05:08] Google ships Nano Banana 2 Lite image model on OpenRouter

Google just pushed Nano Banana 2 Lite onto OpenRouter as google/gemini-3.1-flash-lite-image, adding a Flash-Lite image endpoint to the public model catalog. The listing frames it as Google's fastest, most cost-efficient Gemini image model, aimed at high-velocity developer pipelines and rapid-fire visual exploration. Context length lands at 65536 tokens, enough to absorb long, structured prompts and negative constraints without mid-call trimming. The mechanism to focus on is the Flash-Lite tier itself: text-to-image generation tuned for low latency and high call volume, where Google typically trades frontier fidelity for throughput and unit economics. For builders, the practical effect is a Google-native image path you can hammer inside bulk asset pipelines, variant sweeps, and ideation loops without paying Pro-tier per-image rates. The OpenRouter entry signals a router-friendly endpoint, so existing image-agent stacks can switch providers with a model-string change. Watch whether the 65536 context window is fully usable for image conditioning or capped, and how pricing holds up under sustained production load.

[06:06] Orca Paper Proposes Unified World Latent Space Through Next-State Prediction

A new paper called Orca, trending on HuggingFace Daily Papers with 161 upvotes, proposes a unified world latent space built through multimodal next-state-prediction modeling. The work, hosted at orca-wm.github.io and published as arXiv 2606.30534, reframes world modeling: rather than training a separate model per domain, Orca compresses world dynamics into one shared latent and transfers it to downstream tasks, where its authors report beating specialized baselines. That generality is the headline capability, and is why the community is reading it. The concrete mechanism is multimodal next-state prediction, the same pre-training objective powering recent agent and embodied-AI work, now scaled into a single shared latent rather than per-domain heads. For builders, the practical signal is that general world-model pre-training is becoming a credible alternative to task-specific stacks, so teams planning agentic or embodied pipelines have a new architectural option worth evaluating against their current SFT-only approaches. Watch next: the eval suite and whether the latent transfers beyond the paper's benchmarks.

[07:04] Agents-A1: 35B MoE Agent Hits Trillion-Parameter-Class Performance

Agents-A1, a 35-billion-parameter mixture-of-experts agentic model from InternScience, claims trillion-parameter-class performance without trillion-parameter cost. The team's contribution is two scaling levers and a three-stage distillation pipeline, not raw parameter count.

Long-horizon trajectory scaling expands the multi-turn action sequences the model trains on, pushing past single-step prompts into extended tool-use traces. Heterogeneous agent ability scaling mixes specialist capabilities across coding, tool use, and retrieval domains. Training runs as supervised fine-tuning on long agent traces, then per-domain teacher models that specialize by task family, then multi-teacher distillation that fuses them into one 35B student.

For builders running cost-sensitive pipelines, the implication is clear: frontier agent performance is no longer gated exclusively on parameter count, since distillation recipes that absorb specialist teachers can punch above their weight class. Watch the open weights release and independent benchmark replication; if the long-horizon gains hold outside the authors' eval harness, the recipe reshapes how teams size serving budgets and pick open-weight students.

[08:02] OmniRoute Turns One Endpoint Into 231 Model Providers

OmniRoute, an open-source AI gateway from developer diegosouzapw, hit GitHub Trending this week. The project exposes a single OpenAI-compatible endpoint and points it at 231 model providers, roughly 50 with free tiers, letting a coding agent reach Claude, GPT, or Gemini without provider-specific client wiring. Drop it in front of Claude Code, Codex, Cursor, Cline, or Copilot and the gateway handles routing. The notable mechanism is a stacked compression pass — RTK plus Caveman mode — applied before prompts leave the box, claimed to cut token usage between 15% and 95% depending on workload. A smart auto-fallback layer reroutes failed or rate-limited requests to the next available provider, with MCP and A2A support keeping tool-calling and agent-to-agent flows intact. For builders, this means a self-hosted routing plane that survives provider outages and free-tier churn. Watch for latency overhead on the compression path and how fallback priority is configured when multiple free providers are wired in.

[09:00] BlockPilot Picks Block Sizes Live for Diffusion Speculative Decoding

BlockPilot, a paper trending on HuggingFace Daily Papers with 64 upvotes, proposes instance-adaptive policy learning for diffusion-based speculative decoding. The work comes from the AMAP-ML group and is open-sourced on GitHub alongside the arXiv preprint. The core move is replacing a fixed block size — how many tokens the diffusion drafter produces per step — with a small policy that reads the prompt's prefilling representations and picks a per-request block size on the fly. The authors report significant speedup over static block-size schedules with minimal policy overhead, and the upvote count reflects how actively the inference community is engaging with adaptive drafting. For builders, the implication is that block size is no longer a deploy-time knob you tune once; it's a learned, prompt-conditioned decision that could slot into existing speculative-decoding pipelines without retraining the target model. The next thing to watch is whether the released policy generalizes across model families or only holds inside the paper's training distribution.

[09:58] Generative Skill Composition Tackles LLM Agent Skill Bottleneck

Xinyu Zhao, Zhen Tan, and Vaishnav Tadiparthi posted arXiv 2606.32025 this month, framing skill composition as the central bottleneck as agent skill libraries scale across tasks and domains. Skills bundle modular procedural knowledge — sandboxing environments, running test suites, multi-file refactors — and current approaches either dump the full library into the agent's reasoning context or retrieve via embeddings. Both degrade as libraries grow: full-context burns tokens, retrieval misses compositions. The paper proposes generative skill composition, where the model synthesizes skill combinations on the fly instead of picking from a fixed pool. The mechanism reframes selection from retrieval into synthesis, with the agent reasoning about how to combine skills for the task. For builders, this matters because skill libraries are the natural unit of reuse across agents, and composition strategy shapes how much procedural memory an agent carries without context rot. Watch for the paper's full benchmark results comparing generative composition against retrieval baselines on standard agent suites.

[10:56] TRIAGE Paper Proposes Role-Typed Credit Assignment for Agentic RL

TRIAGE is a role-typed credit assignment scheme for agentic reinforcement learning that adds a semantic role axis on top of GRPO's flat outcome advantage, so search, click, edit, navigation, and object-interaction tokens no longer share one learning signal. Authors Yuanda Xu, Zhengze Zhou, and Hejian Sang, in arXiv 2606.32017, frame the problem directly: GRPO's verifier-only reward conflates everything a rollout produced, so a useful exploration step in a failed rollout gets punished like a wasted one, while redundant steps in a successful rollout get reinforced. TRIAGE inserts a structured judge that classifies each segment by role before advantage is computed, and the role label modulates the update. The reported gains concentrate where rollouts lean on dense tool use. For builders training agent policies with RL, the result reframes the next optimization lever away from a stronger verifier and toward a better credit-assignment layer. Watch for the judge model itself, since role classification quality becomes the new bottleneck.

[11:54] Practical queue

From today's stories: For builders, the release readout shifts what the stack can rely on by default — diff the changelog against your pinned version before promoting the new default. Claude Fable 5's return restores a frontier tier above Opus that agent stacks can reach through a router-friendly slug, and the immediate move is a bake-off against a current Opus-class default. What this means for Sonnet 5: a single Sonnet-class endpoint now exposes a tunable reasoning dial instead of a binary thinking toggle. What this means for image pipelines: if your image-agent work is bottlenecked on per-image cost or rate limits at the Pro tier, the Flash-Lite endpoint is purpose-built for high call volume. For builders, the practical signal from Orca is that general world-model pre-training is becoming a credible alternative to task-specific stacks. Agents-A1 matters because frontier agent performance may no longer require trillion-parameter serving budgets — specialist-teacher distillation recipes can compress frontier capability into deployable sizes. OmniRoute is a self-hosted routing layer that sits between a coding agent and upstream model APIs, so a single OpenAI-compatible base URL replaces provider-by-provider client config. BlockPilot argues block size should be a learned, per-request decision driven by the prompt's prefilling representations. For builders running agent stacks with growing skill libraries, generative skill composition signals a shift away from brute-force context stuffing and embedding retrieval toward generation-based composition. For builders training agent policies with RL, TRIAGE reframes credit assignment, not verifier quality, as the next optimization lever.
```

---

## Chapters

- 00:00 — Intro: Claude Fable 5 Is Back / Agent Stack Release Readout: OpenClaw v2026.6.11; OpenAI Codex rust-v0.142.5 / Claude Sonnet 5 Lands on OpenRouter With 1M Context
- 02:00 — Agent Stack Release Readout: OpenClaw v2026.6.11; OpenAI Codex rust-v0.142.5
- 03:05 — Claude Fable 5 Is Back: Washington Lifts the Hold on Anthropic's Frontier Tier
- 04:10 — Claude Sonnet 5 Lands on OpenRouter With 1M Context
- 05:08 — Google ships Nano Banana 2 Lite image model on OpenRouter
- 06:06 — Orca Paper Proposes Unified World Latent Space Through Next-State Prediction
- 07:04 — Agents-A1: 35B MoE Agent Hits Trillion-Parameter-Class Performance
- 08:02 — OmniRoute Turns One Endpoint Into 231 Model Providers
- 09:00 — BlockPilot Picks Block Sizes Live for Diffusion Speculative Decoding
- 09:58 — Generative Skill Composition Tackles LLM Agent Skill Bottleneck
- 10:56 — TRIAGE Paper Proposes Role-Typed Credit Assignment for Agentic RL
- 11:54 — Practical queue

---

## Primary Links

- OpenClaw v2026.6.11 release: https://github.com/openclaw/openclaw/releases/tag/v2026.6.11
- OpenAI Codex rust-v0.142.5 release: https://github.com/openai/codex/releases/tag/rust-v0.142.5
- Anthropic: Claude Fable 5 model page: https://openrouter.ai/models/anthropic/claude-fable-5
- Anthropic: Claude Fable 5 and Claude Mythos 5 announcement: https://www.anthropic.com/news/claude-fable-5-mythos-5
- TechCrunch: restrictions dropped on Anthropic's Mythos and Fable models: https://techcrunch.com/2026/06/30/trump-drops-restrictions-on-anthropics-mythos-and-fable-models/
- Anthropic: Claude Sonnet 5 model page: https://openrouter.ai/models/anthropic/claude-sonnet-5
- Google: Nano Banana 2 Lite (Gemini 3.1 Flash Lite Image) model page: https://openrouter.ai/models/google/gemini-3.1-flash-lite-image
- Orca: The World is in Your Mind: https://orca-wm.github.io/
- Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter P: https://internscience.github.io/Agents-A1/
- diegosouzapw/OmniRoute — Never stop coding. Free AI gateway: one endpo: https://github.com/diegosouzapw/OmniRoute
- BlockPilot: Instance-Adaptive Policy Learning for Diffusion-based Spec: https://github.com/AMAP-ML/BlockPilot
- Generative Skill Composition for LLM Agents: https://arxiv.org/abs/2606.32025
- TRIAGE: Role-Typed Credit Assignment for Agentic Reinforcement Learnin: https://arxiv.org/abs/2606.32017
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- microsoft/mcp-for-beginners repo: https://github.com/microsoft/mcp-for-beginners
- mukul975/Anthropic-Cybersecurity-Skills — 817 structured cybersecurity: https://github.com/mukul975/Anthropic-Cybersecurity-Skills
- AxDafny: Agentic Verified Code Generation in Dafny: https://arxiv.org/abs/2606.32007
- Surrogate Fidelity: When Can Open LLMs Explain Closed Ones?: https://arxiv.org/abs/2606.32008
- Ollama v0.31.1: https://github.com/ollama/ollama/releases/tag/v0.31.1

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.11`, published 2026-06-30T16:06:39Z. Recent episode version tags detected: `v2026.6.8`, `v2026.6.8-beta.1`, `v2026.6.8-beta.2`, `v2026.6.9`. Selected missing version(s): `v2026.6.11`.
- **Hermes Agent** — Latest stable verified: `v2026.6.19`, published 2026-06-19T19:39:06Z. Recent episode version tags detected: `v0.16.0`, `v2026.5.29.2`, `v2026.6.19`, `v2026.6.5`. No new stable release this cycle.
- **OpenAI Codex** — Latest stable verified: `rust-v0.142.5`, published 2026-07-01T01:15:44Z. Recent episode version tags detected: `rust-v0.142.1`, `rust-v0.142.2`, `rust-v0.142.3`, `rust-v0.142.4`. Selected missing version(s): `rust-v0.142.5`.
- **Claude Code CLI** — Latest stable verified: `2.1.185`, published 2026-06-20T16:54:36.327Z. Recent episode version tags detected: `2.1.181`, `2.1.185`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-07-01). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.11` (stable) / `v2026.6.11-beta.2` (prerelease)
- **Hermes Agent** — `v2026.6.19`
- **OpenAI Codex** — `rust-v0.142.5`
- **Claude Code CLI** — `2.1.185`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
