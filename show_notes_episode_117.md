# AgentStack Daily EP117 — GPT-6 cracks a 2005 Enigma, Mistral releases 675B on Apache 2.0

**Title:** GPT-6 Astra Cracks a 2005 Enigma as Mistral Releases a 675B Apache 2.0 Flagship

**Tagline:** Mistral drops a 675B open-weight flagship on Apache 2.0 while OpenAI's GPT-6 Astra reportedly decoded an Enigma message that has stumped cryptanalysts since 2005. Mistral also pushed Devstral 2 2512, tuned for long-running coding agents. Claude Opus 5.5 surfaces in GitHub Copilot for agentic coding, and Black Forest Labs ships FLUX 3 Action, a 7B vision-language-action model for robotics. Hermes Agent shipped v2026.9.24 in the harness readout, Ando exited stealth with a Slack-style workspace for humans and AI agents, and Fastino released a 340M open decision model that runs agent guardrails on CPU.

**Feed description:** Mistral releases a 675B open-weight model on Apache 2.0 and ships Devstral 2 2512 for long-running coding agents. OpenAI's GPT-6 Astra reportedly decoded an Enigma message stumping cryptanalysts since 2005. Claude Opus 5.5 lands in GitHub Copilot, Black Forest Labs ships FLUX 3 Action for robotics, Ando exits stealth with a Slack-style workspace for humans and AI agents, Fastino publishes a 340M open decision model for agent guardrails on CPU, and Hermes Agent v2026.9.24 ships in the harness rundown.

---

## Story Slate

1. **Agent Stack Release Readout: Hermes Agent v2026.9.24**
Hermes Agent tagged v0.21.5 on September 24, 2026, rolling approximately 460 merged PRs since v0.21.4 into a single stable artifact for Docker images, Hermes Cloud, and hosted deployments. Measured at commit f97608f178d1ffeca59860195ab7da295f7c8e5f, the window covers 1,610 non-merge commits across 4,828 changed files with about 164,000 lines added and 149,000 removed. Items landing in the window include a Desktop plugin SDK wave, a Simple/Advanced interface mode, a Connectors page replacing the MCP tab, French, German, and Spanish Desktop catalogs with RTL/LTR support, custom model entry, GPT-6 Sol/Terra/Luna and Claude Opus 5.5 in the Nous and OpenRouter catalogs, a Blender Lab integration, and NVIDIA app and Broadcast plugins. Full curated notes ship with v0.22.0.
Technical depth angle: The v2026.9.24 tag pins a single reproducible commit (f97608f178d1ffeca59860195ab7da295f7c8e5f) that Docker, Hermes Cloud, and hosted deployments can base their builds on, replacing the previous rolling-head workflow. Hot-path performance work inside that window touched config loading, the tool registry, gateway message handling, and the model picker.
Actionability angle: This rollup means existing Hermes Cloud, hosted, and Docker users can point at one pinned tag rather than tracking the rolling head. For evaluation or CI, pulling the nousresearch/hermes-agent:v2026.9.24 image gives a reproducible build. The next milestone is v0.22.0, which will collect the full highlight reel and contributor credits. The implications land across Antigravity, Codex, Claude Code, and Hermes stacks alike.
Listener hook: Hermes just dropped a single pinned tag covering 460 pull requests, so anyone running Docker or Hermes Cloud can stop chasing the rolling head.

2. **Mistral's Devstral 2 2512 Targets Long-Running Coding Agents**
Mistral has released Devstral 2 2512, a 123-billion-parameter dense transformer built for software engineering agents that need to reason across large codebases. The model ships as open-source weights and accepts a 262,144-token context window, so it can hold a long task history or a sizable repo in one pass. It is live on OpenRouter under the identifier mistralai/devstral-2512, making it available to anyone routing API traffic through that marketplace. Mistral is pitching it as a leading open-weight option for agentic coding work that previously depended on closed systems.
Technical depth angle: Devstral 2 2512 is a dense transformer at 123 billion parameters, so every parameter participates in each forward pass rather than being split across specialist sub-networks. Its 262,144-token context window is what enables long-horizon agentic work: a coding agent can hold an entire repository plus its running task history in one prompt without summarization.
Actionability angle: Builders running agentic coding workflows through OpenRouter can route to mistralai/devstral-2512 immediately, which makes it a drop-in candidate for long-context repository-scale tasks. The large context window means you can hand the model a whole project plus a multi-step task without aggressive summarization between turns. What this means: the open-weight option is finally sized for the long-running jobs.
Listener hook: If you've ever wanted to point a coding agent at a giant repo without it forgetting what it was doing, Mistral just made that easier to try.

3. **Mistral Ships a 675B Open-Weight Flagship on Apache 2.0**
Mistral has listed Mistral Large 3 2512 on OpenRouter, its most capable model to date. It is a sparse mixture-of-experts model with 41 billion active parameters out of 675 billion total, supports a 262,144-token context window, and ships under the Apache 2.0 license — unusually permissive for a frontier-tier open-weight release.
Technical depth angle: Sparse mixture-of-experts means only 41B of the 675B parameters activate per token, so inference cost tracks the active count rather than the full total. Apache 2.0 permits commercial use, redistribution, and modification with attribution only.
Actionability angle: The Apache 2.0 license lets builders self-host, fine-tune, and ship commercial products without the legal friction that typically pushes teams toward smaller or more restricted models. The 262K context window fits long-document and large-codebase workloads. The next thing worth watching is how the model performs once independent benchmark numbers start landing.
Listener hook: A 675-billion-parameter frontier-tier model just landed on a major routing API under one of the most permissive open-source licenses available.

4. **GPT-6 Astra Solves Enigma Message That Stumped Cryptanalysts Since 2005**
In September 2026, OpenAI's GPT-6 Astra autonomously broke a 1941 German Army Enigma message, designated MVUEH, that had resisted every cryptanalytic attempt since it was posted publicly in 2005. Cryptographer Carter Leffen pointed the model at the Crypto Cellar Research archive of unbroken wartime messages, and GPT-6 Astra selected MVUEH as its target, suspected a relationship to a previously broken message, built its own Enigma simulator and Bombe-style search code in Python and C++, and cracked the cipher in about two days. The result stunned veteran cryptanalyst Frode Weierud, who said the work would take a human researcher weeks or months.
Technical depth angle: The message used a different wheel order (253 vs. 512) than other 10 July 1941 messages, and the left-hand wheel turned over at the 72nd letter, both rare complications. Transcription errors in the original ciphertext had also foiled earlier attempts. GPT-6 Astra used the repeated place name "ROSENOW ROSENOW" as a crib to drive the search, then identified archival references in the German Federal Archives that Weierud himself had to spend weeks finding.
Actionability angle: What this means: a general-purpose model, handed a public archive and an open-ended prompt, independently chained domain modeling, code generation, and archival discovery to outperform veteran specialists on a 21-year cold case. Why this matters: frontier models can now drive open-ended historical, scientific, or forensic investigations that previously demanded years of training, shifting how researchers triage problems that look impossible.
Listener hook: A 21-year-old Enigma cold case fell to GPT-6 Astra in two days, working mostly on its own.

5. **Claude Opus 5.5 lands in GitHub Copilot for agentic coding**
Anthropic's newest Opus model, Claude Opus 5.5, is now available inside GitHub Copilot. The reasoning-capable model handles text and image inputs, writes back text, and carries a 1M-token context window — large enough to hold roughly 1,500 pages of prose. According to Artificial Analysis, it scores 58 on the Intelligence Index (median 26), placing it among the top tier of reasoning models. Pricing is $4 per million input tokens and $20 per million output tokens, with a 95% cache discount. GitHub positions it for agentic coding flows, long-running agentic tasks, and general knowledge work.
Technical depth angle: Opus 5.5 is configured as an adaptive reasoning model set to max effort, with a default fallback to lighter responses when appropriate. It accepts text and image input, returns text, and runs with a 1M-token context window. On Artificial Analysis's Intelligence Index v4.3.2, which combines ten evaluations, it scores 58 against a median of 26 while emitting 260M tokens during the index run — roughly three times the median — so the model spends heavily on reasoning before it answers.
Actionability angle: What this means: a top-tier reasoning model is now reachable from your editor rather than only through an API call. Long refactors, multi-step agentic coding flows, and mixed text-and-image tasks — like pairing a screenshot with a code change — can run end-to-end without leaving Copilot. Why this matters: the 95% cache discount on repeated prefixes helps offset the $20-per-million-output rate that makes the model pricey for chatty workloads.
Listener hook: The most expensive, highest-scoring reasoning model on the Copilot lineup is now one click away from your editor — and the open question is whether the per-task bill is worth the gains.

6. **Ando comes out of stealth with a Slack rival built for humans and AI agents**
Ando, a startup founded by Sara Du, launched a team messaging platform where AI agents get their own identities, inboxes, and the ability to join conversations like coworkers. The company raised $20 million in pre-seed and seed funding from Accel, Index Ventures, and Emergence to take on Slack and Microsoft Teams in the AI-native workplace.
Technical depth angle: Ando treats agents as participants with their own inboxes, channel access, and decision authority — they can browse channels, join conversations unprompted, message humans directly, and synthesize parallel discussions into group chats without a human relay layer.
Actionability angle: For teams experimenting with AI workflows, Ando points to a future where agents coordinate themselves across channels instead of being summoned for each task. Builders can think about how to design agents that participate in conversation rather than wait for instructions, and what that means for visibility and team dynamics.
Listener hook: A messaging app where AI agents show up to meetings, take notes, and message your coworkers without you asking.

7. **Fastino's 340M Open Decision Model Runs Agent Guardrails on CPU**
Fastino Labs shipped GLiNER2.5-Decide, a 340M-parameter open-weight decision model that handles the judgment calls inside AI agent pipelines — routing, triage, tool selection, and guardrails. You feed it text plus a schema of typed questions and it returns structured answers with probability distributions, confidence scores, and feasibility flags. Weights are Apache 2.0 and run on CPU, GPU, or air-gapped environments. A constrained decoder enforces rules across related answers, so a prompt-injection detection automatically forces an unsafe verdict downstream instead of contradictory labels.
Technical depth angle: A non-generative DeBERTa-v3-large encoder scores every permitted label against input plus schema, then a constrained decoder picks the highest-scoring joint assignment that respects declared rules — implications, exclusions, cardinality limits, ordinal bounds — across the whole schema in one pass.
Actionability angle: Builders can replace a hosted LLM-as-judge step inside agent loops with a deterministic, CPU-runnable classifier that returns calibrated probabilities. Apache 2.0 weights plus an air-gapped install profile mean guardrails, routing, and triage can run on a single box or on-prem wherever data residency rules out an API call.
Listener hook: You may never need to call a hosted LLM for the simplest routing, triage, or guardrail decision inside your agent again — Fastino shipped a 340M open-weight model that does it on CPU.

8. **Black Forest Labs Ships FLUX 3 Action: A 7B Robot Brain**
Black Forest Labs has released FLUX 3 Action, a 7-billion-parameter open-weights World Action Model for robot control. Unlike most robot policies that predict actions alone, it jointly predicts video frames and robot motions from camera input, robot state and a text instruction. It tops the RoboLab-120 leaderboard at 42.92%, beating NVIDIA's Cosmos 3 Nano by 6.1 percentage points while using 56% fewer parameters. The DROID policy runs on a 24 GB card with quantization and fits into NVIDIA Jetson for edge deployments. Teams can fine-tune it on their own robot demonstrations using published recipes.
Technical depth angle: FLUX 3 Action extends the FLUX 3 multimodal image backbone into robot control by encoding text, video and robot state into tokens, then decoding future tokens into predicted video frames and action tokens into robot motions. Pretraining on over 95% video tokens gave it strong visual priors; midtraining mixed in 63% action-aligned video from 14 embodiments using a shared 50-dimension end-effector action space called EE50. Guidance distillation eliminates a second inference pass, cutting runtime by roughly half while actually improving task success by 0.6 to 1.08 percentage points.
Actionability angle: Robotics teams can download the DROID policy checkpoint today and run inference or fine-tune on their own arm demonstrations with the published SO-101 LoRA recipe. The model is natively integrated into Hugging Face LeRobot, so deployment on new hardware follows existing tooling rather than custom wiring. Pairing it with a language reasoner like GPT 6 Astra reduced per-task cost to $8.77 and time to just over 8 minutes versus $13.47 and 16 minutes for pure reasoning.
Listener hook: A robot policy that predicts what the world will look like as it moves just took the top spot on a major benchmark while running on hardware you might already own.

9. **Oracle Invokes Force Majeure on New Mexico AI Data Center**
Oracle has cited a force majeure clause on Project Jupiter, a massive New Mexico data center being developed by a unit of Blue Owl Capital. The notice lets Oracle delay payments if the facility misses its 2028 target to come online, rather than walking away as the site's main tenant. The project has already faced public opposition and regulatory setbacks. The move is a rare public signal of how much financial risk cloud providers are hedging as AI infrastructure deadlines tighten.
Technical depth angle: Force majeure is a contract clause that lets one party skip or delay obligations when extraordinary events make performance impractical—usually reserved for natural disasters or supply shocks. Oracle is using it here as a financial hedge: keeping the lease in place but protecting its balance sheet if construction delays push the 2028 target.
Actionability angle: For builders and operators, this is a reminder that AI capacity announcements are backed by long-dated construction contracts that can include escape hatches. What this means is that promised cloud capacity timelines deserve a closer read before you bake them into product plans. Why this matters is that other hyperscaler tenants on similarly delayed sites may reach for the same protection, putting more 2027 and 2028 capacity roadmaps in question.
Listener hook: When a hyperscaler quietly invokes force majeure on a flagship AI build, the entire infrastructure roadmap for the next two years is worth a second look.

10. **Could Monkey Island's grog really dissolve a mug in 35 seconds? A chemist models it.**
A researcher at the University of Groningen has published a paper in the Journal of Geek Studies analyzing whether the fictional grog from the 1990 Lucasfilm Games title The Secret of Monkey Island could really eat through a pewter mug in the roughly 35 seconds it takes in the game. Treating the puzzle as an inverse chemistry problem, the author modeled what the liquid would need to contain and mapped the requirements against the ingredients the game actually lists.
Technical depth angle: The author treats the game as an inverse problem: he times the mug's lifetime in the 2009 Special Edition at about 35 seconds, assumes a 2mm pewter wall (modeled as pure tin), and works backward to estimate the proton supply needed to perforate that wall in that time. That required rate is then matched against the game's listed ingredients, with sulfuric and battery acid emerging as the only plausible drivers.
Actionability angle: It's not a shipping release, but it is a clean example of treating a pop-culture puzzle as a real modeling exercise—measure the behavior, invert to required quantities, then test the proposed inputs. For builders and tinkerers, the template translates: small, well-bounded problems with quantitative constraints can be tackled rigorously without big infrastructure.
Listener hook: If you ever paused Monkey Island long enough to wonder whether grog could really dissolve a pewter mug, a real chemist just ran the numbers.

11. **AI That Thinks in DNA Pushes the Bio-Security Frontier**
Radical Numerics, a startup founded by former Evo and Evo-2 developers, is scaling genomic language models beyond generating DNA to tackle RNA, proteins, and the functional relationships between them. Their models already demonstrate biological chain-of-thought: shown progressively better RNA sequences and their scores, the model self-optimized to scores it had never seen. The team argues this same capability that enables faster vaccine design also lets defenders keep pace with bio-threats. The catch: these same tools lower the barrier for adversaries, making bio-security an active arms race rather than a solved problem.
Technical depth angle: Genomic language models process DNA's four-letter alphabet (ACGT) in sequences up to 3 billion characters long, enabled by long-context innovations from roughly three years ago. Unlike natural language models, biological sequences contain built-in markers for genes and proteins, allowing the same model to generalize across DNA, RNA, and protein without separate training for each modality. In a disclosed experiment, Radical Numerics showed a model progressively improving RNA aptamers with scores, then asked it to continue the trajectory; it generated higher-scoring sequences it had not been shown, demonstrating emergent optimization capabilities the team calls biological chain-of-thought.
Actionability angle: Teams working on therapeutics, diagnostics, or biosensor development should monitor how genomic language models handle multi-modal inputs—DNA, RNA, protein, and structural data—because the same cross-language generalization that enables vaccine design also applies to pathogen detection. The open question is whether defensive toolchains can move faster than the attack surface these models create, especially as open-weight genomic models proliferate.
Listener hook: A startup built by the people who first synthesized a virus from scratch using AI is now arguing that the same technology protecting us is also the one we most need to worry about.

12. **Research digest: Researchers Train Video Models to Track Hidden Objects Like Humans Do**
A paper trending on HuggingFace's daily research feed asks whether video generation models — AI systems that synthesize moving scenes — already understand object permanence, the everyday sense that a ball rolled behind a couch still exists. The team argues these models are a natural place to look for human-like physical intelligence because they have started showing emerged reasoning abilities, but probe after probe shows the prior is mostly missing. Their proposed fix is WROP, a new training dataset built around the same kinds of core-cognition intuitions an infant develops in its first months. The aim is world models that keep objects consistent across occlusions and re-entries, with payoffs for robotics, simulation, and any system that has to predict what happens to things that briefly leave view.
Technical depth angle: The paper probes whether video world models have emerged object permanence and solidity, finds the priors are largely absent, and introduces WROP, a core-cognition inspired training data infrastructure designed to instill those priors in video generation models.
Actionability angle: For builders working on robotics, simulation, or video generation, this is a signal that off-the-shelf video world models may not have basic object permanence built in, which matters for any downstream task that depends on persistent scene state. Watch for WROP-trained checkpoints and follow-up reproductions; if you need an AI that reasons about a scene the way a toddler would, this dataset is the closest existing starting point.
Listener hook: If you've ever wondered why AI video models forget the coffee cup you set on the table two seconds ago, this paper is for you.

13. **Research digest: AI Coding Agents Outperform Hand-Built Robot Planners**
A new study finds that AI coding agents can write robot-planning programs that beat hand-engineered alternatives. Given a task and simulator access, the agents wrote programs that generalized across problem instances in simulated environments. On the subset where hand-written planners exist, the agents hit mean success rates of 56% to 95%, well above the 47% baseline.
Technical depth angle: The key idea is that an LLM-based coding agent iterates inside a physics simulator until it converges on a program that solves an entire family of instances, not just one. The agent effectively replaces the planning engineer, writing a reusable algorithm rather than outputting a single answer.
Actionability angle: Robot developers stuck maintaining bespoke planning pipelines now have a working pattern. What this means is they can hand the planning task to a coding agent, freeze the generated program, and evaluate it on new problem instances, turning what used to be a months-long engineering exercise into a compute-budget question.
Listener hook: If you've ever wondered whether AI can replace months of robotics engineering, this study shows it can, at least for one stubborn class of problems.

14. **OpenAI Releases MentalHealthBench for Evaluating Mental Health AI Responses**
OpenAI introduced MentalHealthBench on September 23, an expert-informed benchmark designed to evaluate how helpful and safe AI systems are across realistic mental health conversations. The benchmark aims to give developers and researchers a standardized way to measure whether AI assistants respond appropriately when users bring up mental health concerns, including situations where a model should recognize limits and route to professional help. It is positioned as a tool for grading model behavior in a sensitive domain where generic accuracy scores miss the point.
Technical depth angle: Rather than testing factual recall, MentalHealthBench focuses on whether AI responses are both helpful and safe in conversational mental health scenarios. The benchmark is built on expert input, meaning mental health professionals shaped the realistic scenarios and graded what counts as a good answer in those exchanges.
Actionability angle: For teams building or deploying AI assistants that touch health-adjacent conversations, this offers a structured way to compare model behavior beyond generic accuracy metrics. The benchmark also signals that domain-specific safety evaluation is becoming a default expectation rather than an afterthought. Wellness, coaching, or triage integrations gain a shared yardstick for testing before shipping.
Listener hook: OpenAI just released a benchmark designed to grade how AI handles real mental health conversations, with test cases shaped by the people who do this work for a living.

---

## Editorial Mix Check

- flagship_products: 9
- builder_projects: 9
- local_ai: 4
- hardware_compute: 5
- policy_regulation: 4
- research: 2

---

## Model Discovery Check

- **Mistral: Devstral 2 2512** (mistralai) — Newly listed this cycle (verified September 25, 2026). Primary source: https://openrouter.ai/models/mistralai/devstral-2512. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 262144 tokens; modality: see primary source. Capabilities: context length 262144; Devstral 2 is a state-of-the-art open-source model by Mistral AI specializing in agentic coding. It is a 123B-parameter dense transformer model supporting a 256K context window. Devstral 2 supports exploring.... Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/mistralai/devstral-2512 and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **Mistral: Mistral Large 3 2512** (mistralai) — Newly listed this cycle (verified September 25, 2026). Primary source: https://openrouter.ai/models/mistralai/mistral-large-2512. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 262144 tokens; modality: see primary source. Capabilities: context length 262144; Mistral Large 3 2512 is Mistral’s most capable model to date, featuring a sparse mixture-of-experts architecture with 41B active parameters (675B total), and released under the Apache 2.0 license.. Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/mistralai/mistral-large-2512 and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

---

## Local LLM Spotlight

- **abenzerps/Qwen-Image-2.1-Uncensored-GGUF** — https://huggingface.co/abenzerps/Qwen-Image-2.1-Uncensored-GGUF — Trending open model on Hugging Face; task text-to-image; 1694 likes and 715906 downloads. Tags: gguf, qwen, image-generation, comfyui, comfyui-gguf, text-to-image, base_model:Qwen/Qwen-Image-2.1, base_model:quantized:Qwen/Qwen-Image-2.1, license:other, region:us.
  Try now: Read the linked model card before downloading, and choose a runtime or device only after it confirms the license, weight format, context window, benchmarks, and hardware requirements.

---

## GitHub Project Radar

- **HKUDS/nanobot** — https://github.com/HKUDS/nanobot — Ultra-lightweight, open-source, self-hosted personal AI agent framework in Python with WebUI, tools, memory, MCP, multi-agent workflows, automation, and chat apps `stars: 48,561`; `stars_delta_30d: +1,310 (+2.8%) since 2026-08-21`; `latest_release: v0.3.5 (2026-09-15)`.
  Why this is on the radar now: v0.3.5 shipped on 2026-09-15 and the repository was updated on 2026-09-25.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — High-performance code intelligence MCP server. Indexes codebases into a persistent knowledge graph — average repo in milliseconds. 158 languages, sub-ms queries, 99% fewer tokens. Single static binary `stars: 44,866`; `stars_delta_30d: +5,111 (+12.9%) since 2026-08-21`; `latest_release: v0.11.0 (2026-09-15)`.
  Why this is on the radar now: v0.11.0 shipped on 2026-09-15 and the repository was updated on 2026-09-24.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

- **ahujasid/mcp-for-blender** — https://github.com/ahujasid/mcp-for-blender — Community plugin to control Blender 3D with any LLM of your choice `stars: 29,315`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: none published on GitHub as of 2026-09-25`.
  Why this is on the radar now: The repository was updated on 2026-09-24 and enters the radar with 29,315 stars.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

---

## Extra Research Candidates

- **Introducing MentalHealthBench** — https://openai.com/index/introducing-mentalhealthbench — MentalHealthBench is an expert-informed benchmark for evaluating helpful and safe AI responses across realistic mental health conversations. Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

- **Kyutai Releases Voice of Reason: A Speech-Native Model that Solves Spoken Math with Reinforcement Learning** — https://www.marktechpost.com/2026/09/22/kyutai-releases-voice-of-reason-a-speech-native-model-that-solves-spoken-math-with-reinforcement-learning/ — Kyutai has released Voice of Reason, 2 open-weight speech-to-speech models built on GLM-4-Voice-9B. Supervised fine-tuning and reinforcement learning lift spoken GSM8K accuracy from 27.3% to 77.1%. There is no transcription step and no text Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

- **abenzerps/Qwen-Image-2.1-Uncensored-GGUF trending on Hugging Face** — https://huggingface.co/abenzerps/Qwen-Image-2.1-Uncensored-GGUF — text-to-image; 1694 likes, 715906 downloads; tags: gguf, qwen, image-generation, comfyui, comfyui-gguf, text-to-image, base_model:Qwen/Qwen-Image-2.1, base_model:quantized:Qwen/Qwen-Image-2.1 Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

---

## Show Notes

```md
Episode 117 — September 25, 2026

[00:00] Episode hook

Hermes Agent v2026.9.24 shipped September 24, 2026 as a single stable artifact, tagged at v0.21.5 and consolidating roughly 460 merged pull requests since v0.21.4, for Docker images, Hermes Cloud, and hosted deployments. Mistral followed with Devstral 2 2512, a 123-billion-parameter open-weight coding model aimed at long-running software engineering agents, and listed Mistral Large 3 2512 on OpenRouter—a 675-billion-parameter sparse mixture-of-experts design with 41 billion active parameters under Apache 2.0. OpenAI's GPT-6 Astra autonomously cracked a 1941 German Army Enigma message, designated MVUEH, that had resisted every cryptanalytic attempt since it was posted publicly in 2005. Anthropic's Claude Opus 5.5 opened inside GitHub Copilot with a 1M-token context window, and Ando emerged from stealth with a Slack competitor built so AI agents get their own identities and inboxes.

[02:00] Agent Stack Release Readout: Hermes Agent v2026.9.24

Hermes Agent tagged v0.21.5 on September 24, 2026 under the v2026.9.24 release tag. The publisher describes it as a patch that rolls up roughly 460 merged pull requests since v0.21.4 into a single stable artifact for downstream consumers — Docker images, Hermes Cloud, and hosted deployments. Measured at commit f97608f178d1ffeca59860195ab7da295f7c8e5f, the window contains 1,610 non-merge commits across 4,828 changed files, with about 164,000 lines added and 149,000 removed. The full curated writeup covering highlights and feature areas since v0.21.0 is deferred to v0.22.0.

The notes flag several areas that landed in the window. On Desktop, that includes a plugin SDK wave covering a composer draft API, session-list and row-decoration slots, sidebar nav prefs, model-pill label providers, typed settings/skills/toolsets/profiles bridges, a sandboxed embed primitive, an appearance-settings slot, and a public event bridge for plugin backends. A Simple/Advanced interface mode sits alongside a Connectors page that replaces the MCP tab, with a "Connect now" path for a freshly installed plugin's MCP servers and onboarding that offers catalog plugins beside connectors. The French, German, and Spanish Desktop catalogs ship complete, and an RTL/LTR text-direction setting arrives. The composer and Settings pickers accept custom model entries, function-key and dictation voice shortcuts are wired in, and the host multiplexer gains per-profile stop/start/restart with a `gateway.standalone` option to opt a profile out.

On the CLI and TUI, a live dock shows the standing `/goal` and queued prompts; webhook deliveries now mirror into the target chat session; hosted `-desktop` images include Bot Screen; and the kanban board gets a two-column ticket modal with markdown task text. The Nous and OpenRouter catalogs pick up GPT-6 Sol/Terra/Luna and Claude Opus 5.5. Official plugins arrive for Blender Lab and the NVIDIA app and Broadcast apps. A long stretch of hot-path performance work touched config loading, the tool registry, gateway message handling, and the model picker, and dozens of community plugins joined the catalog.

For update paths, the publisher points users at `hermes update` for git installs or a re-run of the installer one-liner; Docker and Hermes Cloud images build from `nousresearch/hermes-agent:v2026.9.24`.

[03:19] Mistral's Devstral 2 2512 Targets Long-Running Coding Agents

Mistral has released Devstral 2 2512, and the headline is the size. It is a 123-billion-parameter open-source dense transformer aimed squarely at agentic coding, the category of software work where an AI does not just answer a question but carries a multi-step task through file edits, tool calls, and verification rounds.

The practical lever is the context window. Devstral 2 2512 accepts 262,144 tokens in a single pass. That is large enough to hold a substantial codebase plus a long thread of prior agent actions without forcing the workflow to summarize or drop history. For builders, that matters because the usual failure mode for long-running coding agents is losing the thread of what they were doing; a bigger window pushes that failure further out.

Distribution is straightforward. The model is live on OpenRouter under the identifier mistralai/devstral-2512, so anyone already routing requests through that marketplace can point an agent at it without standing up new infrastructure. Mistral is positioning it as a state-of-the-art open-weight option for software engineering agents, the kind of work that has largely defaulted to closed systems.

For builders, the interesting question is whether a fully open dense transformer at this scale can hold its own against closed coding models on real agent runs, where the work involves tool use, error recovery, and long task chains. Watch for independent benchmarks on real repositories rather than isolated coding puzzles.

[04:46] Mistral Ships a 675B Open-Weight Flagship on Apache 2.0

Mistral has listed Mistral Large 3 2512 on OpenRouter, calling it the company's most capable model to date. The model uses a sparse mixture-of-experts architecture: 41 billion parameters activate per token out of 675 billion total, which means the compute and memory cost of running it is much closer to the 41B figure than to the full 675B. The context window is 262,144 tokens, large enough to hold a long document or a sizeable codebase in a single prompt without aggressive chunking.

The notable detail is the license. Mistral Large 3 2512 ships under Apache 2.0, which permits commercial use, redistribution, and modification with attribution. That is unusually permissive for a frontier-tier open-weight release and removes a lot of the legal friction that pushes teams toward smaller or more restricted models when they want to self-host, fine-tune, or build commercial products on top.

For builders, the practical question is whether the model lives up to its billing once independent evaluations start circulating. The current OpenRouter listing provides context length, architecture details, and the license, and that is the picture right now. Until benchmark numbers arrive, this is the open-weights flag-bearer worth evaluating against whatever you were running before.

[06:01] GPT-6 Astra Solves Enigma Message That Stumped Cryptanalysts Since 2005

For more than two decades, an Enigma message from the Eastern Front sat unsolved on a public research site. On 15 September 2026, cryptographer Carter Leffen pointed OpenAI's GPT-6 Astra at the Crypto Cellar Research archive of unbroken wartime messages and asked it to take a crack at them. The model picked the most promising candidate, MVUEH, a 1941 German Army message that had resisted every attempt since 2005, and broke it in about two days.

The work was almost entirely the model's. GPT-6 Astra noticed that MVUEH likely shared plaintext with another message from the same day, Nr. 173 SIPVX, which Alex Shovkoplyas had cracked in 2017. It then wrote Python and C++ code for an Enigma simulator and Bombe-style search, anchored on the repeated place name "ROSENOW ROSENOW" as a crib. The recovered key differed completely from the daily key used by other 10 July 1941 messages: the wheel order was 253 instead of the usual 512, and the Enigma's left-hand wheel turned over at the 72nd letter, a rare complication that earlier human attempts had not penetrated. The original ciphertext also contained transcription errors that had thrown off prior breaks.

The model also surfaced references to German Federal Archives volumes, RS 3-3/20a and RS 3-3/63b, that match real holdings but were not listed on the Crypto Cellar site. Frode Weierud, the veteran cryptanalyst who runs the archive, said finding those references took him several weeks and called the model's behavior "like a very professional cryptanalyst and archive researcher."

The story drew a Hacker News score of 733 after it was published via OpenAI News on 23 September. For builders, the takeaway is less about cryptography and more about what an agentic model can do when handed an open-ended research target and a public dataset: choose a thread, build its own tools, and run an investigation end to end.

[07:58] Claude Opus 5.5 lands in GitHub Copilot for agentic coding

Anthropic's Claude Opus 5.5 is now selectable inside GitHub Copilot, giving subscribers direct access to the company's top reasoning model through their editor. The GitHub blog positions it for agentic coding, long-running agentic tasks, and knowledge work.

The headline mechanic is an "adaptive reasoning, max effort, default fallback" configuration: the model thinks hard by default and falls back to lighter responses when appropriate. A non-reasoning variant may also exist. Inputs accept text and images, outputs are text, and the context window stretches to 1 million tokens — roughly 1,500 pages of 12-point Arial — large enough to hold a whole codebase or a multi-hour session in a single prompt.

On Artificial Analysis's Intelligence Index v4.3.2, which combines ten evaluations including AA-Briefcase, Terminal-Bench 4.0, SciCode, and Humanity's Last Exam, Opus 5.5 scores 58 against a median of 26. GitHub's Hacker News announcement drew 331 upvotes the same day. The trade-off is verbosity and price: the model emitted 260 million tokens during the index run (median 88 million), pricing sits at $4 per million input tokens and $20 per million output, and an average index task costs $5.98. A 95% cache discount softens that bill for repeated prompt prefixes.

For builders, the practical shift is reach. Long refactors, multi-step agentic coding flows, and mixed text-and-image tasks — pairing a screenshot with a code change, for example — now run inside Copilot without swapping tools. What to watch next is whether Anthropic ships the non-reasoning variant that Artificial Analysis flags as potentially existing, since a cheaper sibling is what would make this model a daily driver rather than a specialist.

[09:39] Ando comes out of stealth with a Slack rival built for humans and AI agents

Ando, a startup founded by Sara Du, came out of stealth on Thursday with a team messaging app that bills itself as a full Slack replacement — but with AI agents treated as first-class teammates rather than bolted-on bots.

The platform gives each agent its own identity and inbox, with channels, DMs, group conversations, and even live transcribed calls. Agents can browse channels, decide which ones to join, enter conversations without being tagged, and message human coworkers on their own when they think something matters. No approvals required.

Du came to the idea after spending 2025 helping companies build MCP servers. People kept asking how to use agents from inside Slack, and the friction — shuffling messages back and forth, feeding agents context, burning tokens — pointed at a deeper design problem. Slack and Teams were built for a world that was starting to pass us by, she said. The bigger issue, in her framing, is "meat proxies" — humans relaying their agent's output to the rest of the company.

Ando raised $20 million in pre-seed and seed funding from Accel, Index Ventures, and Emergence to hire more people and "burn through more tokens." Customers in software, real estate, and finance across 15 countries are already running on it, though most teams are small.

A concrete example of what changes: Du described an agent that noticed two separate channels debating the same problem. Without being asked, it pulled everyone into a group chat, laid out the shared context, and suggested a decision. Agents could better manage people than humans can because they can process a lot more messages in a shorter span of time, she said.

It's not an uncontested space. Slack has rebuilt its bot as an agent, Microsoft has woven Copilot into Teams, and Jack Dorsey's recently launched Buzz targets developers. But Du sees room for something built AI-native rather than retrofitted.

[11:38] Fastino's 340M Open Decision Model Runs Agent Guardrails on CPU

The model is built for the small but expensive judgment calls that sit inside every AI agent — the "which tool should I use," "is this safe," "which bucket does this belong in" moments. Fastino Labs calls it GLiNER2.5-Decide, a 340-million-parameter open-weight decision model released September 24.

Instead of generating text, you hand it content plus a schema of typed questions, and it returns structured answers. Every answer ships with a probability distribution, a confidence score, and feasibility flags. Schemas can express rules across questions, so a detection in one place can force a verdict in another.

The guardrail example shows why that matters. Decoded independently, the model flagged a prompt-injection attack at 0.82 confidence and simultaneously labeled the same prompt safe at 0.52. Joint decoding applies a rule that any detected harm requires an unsafe verdict, collapsing the answer to safety=unsafe and harm_type=prompt_injection together. Downstream code now has one consistent signal to block on.

It's a non-generative classifier built on a DeBERTa-v3-large encoder and fine-tuned from gliner2-large-v1. Weights ship under Apache 2.0; install is pip install gliner2, and it runs on CPU, GPU, or fully air-gapped. Fastino also offers hosted inference through its GLiNER API.

Fastino's internal suite, Fast Decisions, covers 5,100 examples across 17 datasets. GLiNER2.5-Decide averaged 60.1% exact-match, leading the suite on 9 of 17 datasets and beating a 4-billion-parameter Qwen 3.5-class baseline by about 2.6 points. On support intent it scored 75.3%.

Latency at batch one with a 15-label schema: 167 milliseconds p50 on a 48-core Xeon, 38 milliseconds on a V100. Two siblings round out the family — a 1B variant at 59.6% and a 287M multilingual model at 56.7%.

[13:22] Black Forest Labs Ships FLUX 3 Action: A 7B Robot Brain

Black Forest Labs has shipped FLUX 3 Action, a 7-billion-parameter open-weights model that tells robots what to do by imagining what will happen. It reads camera frames, the robot's current state and a text instruction, then generates future video frames and the next chunk of robot motions in a single joint prediction. On the RoboLab-120 leaderboard, which tests 120 tabletop tasks in simulation, FLUX 3 Action scores 42.92% task success, putting it ahead of NVIDIA's Cosmos 3 Nano at 36.8% despite running on a much smaller backbone. The practical speed picture is what makes this interesting. Cosmos 3 Nano needs about 4.7 times more processing time than π0.5 per second of robot motion on a B200. FLUX 3 Action closes that gap with a smaller architecture and guidance distillation. The base checkpoint runs 1.52 to 3.95 times faster than Cosmos 3 Nano in FP8 across workstation and datacenter GPUs, and the step-distilled variant runs up to 2.28 times faster than π0.5 on the same hardware. The tradeoff is that base and guidance-distilled checkpoints predict 2.13 seconds of motion per call versus 1.0 second for π0.5, so the speed advantage depends on your hardware and how much motion your task needs. Memory requirements are the key deployability gate. The full DROID policy needs roughly 32 GB of GPU memory in BF16 on an H200. With FP8 quantization and text encoder offload, it fits on a 24 GB card. Black Forest Labs also integrated the model into Hugging Face LeRobot and supports NVIDIA Jetson for edge scenarios. On real hardware, a blind evaluation with Positronic Robotics on a Franka arm ran 30 trials across 10 DROID tasks. FLUX 3 Action completed 28 of 30 attempts. Cosmos 3 Nano scored 27, DreamZero 20 and π0.5 just 13. Teams can fine-tune the model on their own demonstrations. Black Forest Labs published a DROID recipe and an SO-101 LoRA recipe, showing a pick-and-place skill learned from roughly 200 examples. The weights, code and recipes ship under the FLUX Kommunity License, which permits non-commercial use.

[15:29] Oracle Invokes Force Majeure on New Mexico AI Data Center

Oracle is putting up a financial shield around one of its biggest AI infrastructure bets. The company sent a force majeure notice to the developer of Project Jupiter, a massive data center being built in New Mexico by a unit of Blue Owl Capital. The clause lets Oracle delay payments if the site misses its 2028 target to come online. Oracle is not trying to walk away as the main tenant—it is hedging its obligations while the project faces public opposition and regulatory setbacks.

The framing matters for anyone watching the AI buildout. Force majeure clauses usually live in the background for natural disasters or supply shocks, so seeing a cloud tenant invoke one on an active site signals how much financial exposure rides on every megawatt of capacity. If Oracle is bracing for Project Jupiter to slip past 2028, the company wants optionality on its capital spending rather than a binary ship-or-cancel outcome.

The project has already drawn opposition and permitting friction, and a 2028 deadline starts to look aspirational when power, regulation, and supply chains all push against a builder at once. Oracle's hedge also gives Blue Owl a quiet signal: the anchor tenant wants flexibility, not necessarily a renegotiation of the lease itself.

The practical read is straightforward. Capacity roadmaps are contracts before they are concrete, and this notice is one of the first public signs that a hyperscaler is treating its own commitments that way. Watch whether other tenants on similar projects reach for the same protection when their timelines wobble.

[17:06] Could Monkey Island's grog really dissolve a mug in 35 seconds? A chemist models it.

A chemist at the University of Groningen has actually done the math on one of gaming's most famous puzzles: whether the grog in The Secret of Monkey Island could really eat through a pewter mug in 35 seconds. The paper, published in the Journal of Geek Studies, treats the game's behavior as an inverse problem, starting from the observed corrosion rate and working backward to estimate what the liquid would need to contain.

The author, affiliated with the ENTEG Institute in the Faculty of Science and Engineering, used the 2009 Special Edition distributed through Steam and timed the mug's lifetime with a stopwatch at about 35 seconds. He assumed the mug was pewter, modeled as pure tin, with a 2mm wall thickness chosen as a ballpark because the game offers no measurement. From there, he estimated the proton supply required to perforate that wall within the observed time.

He then matched that requirement against the grog ingredients listed in the game's dialogue: sulfuric acid, battery acid, kerosene, propylene glycol, artificial sweeteners, rum, acetone, red dye No. 2, axle grease, pepperoni, and the mysterious SCUMM. The paper concludes that sulfuric acid and battery acid could plausibly drive the corrosion, while most of the other ingredients are either unlikely to attack tin directly or would actually slow things down by coating the metal surface. The author describes the model as semi-quantitative and notes that none of the listed components explain the bright green color grog turns in the game.

The post drew a Hacker News score of 137, fitting evidence that even a 1990 point-and-click adventure can host a real chemistry problem if someone bothers to take it seriously.

[18:50] AI That Thinks in DNA Pushes the Bio-Security Frontier

Radical Numerics, a new company founded by researchers who previously built the genomic language models Evo and Evo-2 at Arc Institute, is scaling those capabilities to a broader range of biological problems. Those earlier models generated entire bacteriophage genomes from scratch, and the synthesized viruses proved functional in the lab. Now the team, led by CEO Eric Nguyen, is pushing genomic language models beyond DNA into RNA and protein, leveraging the fact that DNA sequences contain natural markers for genes and the sequences that encode proteins. That built-in structure lets the same model handle multiple biological languages before ever training on 3D protein structure, epigenetics, or natural language. In a disclosed experiment, Radical Numerics showed a model progressively improving RNA aptamers paired with performance scores, then asked it to continue the trajectory on its own. The model recapitulated higher-scoring sequences it had not been shown, suggesting it learned not just pattern matching but active optimization in the DNA language. The team argues that the same capabilities driving faster vaccine and therapeutic design also matter for defense. As frontier AI labs flag bio-security alongside cyber-security as a top concern, the question is whether defenders can move fast enough. Radical Numerics is betting on pushing the frontier harder rather than holding back. The company includes Michael Poli, formerly a founding scientist at Liquid AI, as chief AI scientist; Stefano Massaroli, a former postdoc with Yoshua Bengio and founding team member at Liquid AI, as president; and Armin Thomas, a former Stanford postdoc who worked with Chris Ré, as CTO. One thing to watch: how cross-modal generalization in genomic language models plays out in pathogen detection and vaccine development toolchains as both defensive assets and potential attack-surface concerns.

[20:38] Research digest: Researchers Train Video Models to Track Hidden Objects Like Humans Do

A paper trending on HuggingFace's daily research feed asks a surprisingly toddler-level question: do today's video generation models — the AI systems that synthesize moving scenes — actually understand object permanence, the everyday sense that things keep existing when you can't see them? The authors argue that video models are a natural candidate for studying human-like physical intelligence, since recent versions have started showing emerged reasoning abilities. But when they probe those models, the core priors turn out to be largely missing. Their proposed fix is WROP, a new training dataset built around the same kinds of physical intuitions an infant develops in its first months of life. The dataset is meant to teach world models to keep objects consistent across occlusions and re-entries, so a generated video remembers the ball that rolled behind the chair. The wider goal is world models that reason about physical scenes more like people do, with payoffs for robotics, simulation, and any system that has to predict what happens to things that briefly leave view.

[21:42] Research digest: AI Coding Agents Outperform Hand-Built Robot Planners

Robot planning is hard because picking what to do, where to grab, and how to move are tangled together. Engineers usually write these planners by hand, which takes months. A new study asked whether AI coding agents could do the job instead.

The agents, including Claude Code and Codex, were given a task description and simulator access. They wrote programs, not one-shot answers but reusable algorithms, within a fixed budget. The frozen programs were then tested on unseen instances.

Across simulated environments from two robotics benchmarks, the agents beat every alternative. Mean success reached 56% to 95%, while hand-engineered planners managed 47% on the subset where they were available. The agents also held up as object counts grew, the regime where classical planners usually collapse.

The takeaway: robotics teams stuck maintaining bespoke planning code now have a working shortcut. Point an agent at a simulator, let it iterate, freeze the program, ship it. The bottleneck shifts from engineering hours to compute budget.

[22:43] OpenAI Releases MentalHealthBench for Evaluating Mental Health AI Responses

OpenAI published MentalHealthBench on September 23, a benchmark built with input from mental health experts to evaluate how helpful and safe AI systems are in realistic mental health conversations. The goal is to give developers, researchers, and model providers a shared yardstick for grading assistant behavior in a domain where generic accuracy scores miss the point.

Standard benchmarks tend to measure whether a model answered a factual question correctly. Mental health conversations are different: a response can be factually accurate and still be harmful, dismissive, or encouraging of dangerous behavior. OpenAI's framing positions the benchmark as filling that gap, focusing on whether a model responds helpfully while staying within safe boundaries, including knowing when to escalate or recommend professional help rather than improvising.

The scenarios inside MentalHealthBench are realistic conversational situations users actually bring to AI assistants, shaped by practitioners rather than purely synthetic test writers. That expert involvement is the core mechanism: the people who do mental health work for a living decide what a good answer looks like in each exchange, so the benchmark grades behavior the way a clinician would, not the way a multiple-choice test would.

For builders, the practical effect is a comparable score for mental health response quality. A team shipping an AI wellness coach, a therapy-adjacent journaling app, or a triage chatbot can now point to a documented benchmark result rather than relying on impressions or cherry-picked demos. The release also signals that domain-specific safety evaluation is becoming a default expectation in sensitive areas, not an afterthought patched in after launch.

One thing to watch is whether other labs and independent evaluators adopt the benchmark, fork it, or build competing versions, since a single vendor's grading standard is only as useful as the wider community treats it.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: Hermes Agent v2026.9.24 / Mistral's Devstral 2 2512 Targets Long-Running Coding Agents / Mistral Ships a 675B Open-Weight Flagship on Apache 2.0
- 02:00 — Agent Stack Release Readout: Hermes Agent v2026.9.24
- 03:19 — Mistral's Devstral 2 2512 Targets Long-Running Coding Agents
- 04:46 — Mistral Ships a 675B Open-Weight Flagship on Apache 2.0
- 06:01 — GPT-6 Astra Solves Enigma Message That Stumped Cryptanalysts Since 2005
- 07:58 — Claude Opus 5.5 lands in GitHub Copilot for agentic coding
- 09:39 — Ando comes out of stealth with a Slack rival built for humans and AI agents
- 11:38 — Fastino's 340M Open Decision Model Runs Agent Guardrails on CPU
- 13:22 — Black Forest Labs Ships FLUX 3 Action: A 7B Robot Brain
- 15:29 — Oracle Invokes Force Majeure on New Mexico AI Data Center
- 17:06 — Could Monkey Island's grog really dissolve a mug in 35 seconds? A chemist models it.
- 18:50 — AI That Thinks in DNA Pushes the Bio-Security Frontier
- 20:38 — Research digest: Researchers Train Video Models to Track Hidden Objects Like Humans Do
- 21:42 — Research digest: AI Coding Agents Outperform Hand-Built Robot Planners
- 22:43 — OpenAI Releases MentalHealthBench for Evaluating Mental Health AI Responses

---

## Primary Links

- Hermes Agent v2026.9.24 release: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.9.24
- Mistral: Devstral 2 2512 model page: https://openrouter.ai/models/mistralai/devstral-2512
- Mistral: Mistral Large 3 2512 model page: https://openrouter.ai/models/mistralai/mistral-large-2512
- OpenAI GPT–6 Astra breaks Enigma message that has resisted solution si: https://www.cryptocellar.org/bgac/the-mvueh-break.html
- Claude Opus 5.5 Intelligence, Performance and Price Analysis (Max): https://artificialanalysis.ai/models/claude-opus-5-5
- Ando wants to take on Slack with a team messaging app that lets humans: https://techcrunch.com/2026/09/24/ando-eyes-slack-as-it-builds-team-messaging-platform-for-humans-and-agents-to-work-together/
- Fastino Releases GLiNER2.5-Decide: A 340M Open-Weight Decision Model T: https://www.marktechpost.com/2026/09/24/fastino-releases-gliner2-5-decide-a-340m-open-weight-decision-model-that-runs-on-cpu/
- Black Forest Labs Releases FLUX 3 Action: A 7B Open-Weights World Acti: https://www.marktechpost.com/2026/09/24/black-forest-labs-releases-flux-3-action-a-7b-open-weights-world-action-model-that-tops-robolab-120/
- Oracle cites 'force majeure' to shield itself on controversial data ce: https://www.bloomberg.com/news/articles/2026-09-24/oracle-cites-force-majeure-to-shield-itself-on-controversial-data-center
- The science of Monkey Island: can grog dissolve a metal mug that fast?: https://jgeekstudies.org/2026/09/23/the-science-of-monkey-island-can-grog-actually-dissolve-a-metal-mug-that-fast/
- 🔬Bio-security is an AI Arms Race - Eric Nguyen (CEO, Radical Numerics): https://www.latent.space/p/bio-security-is-an-ai-arms-race-eric
- Training Object Permanence in World Models: https://www.object-permanence.world/
- Coding Agents for Generalized Task and Motion Planning Problems: https://arxiv.org/abs/2609.30233
- A Coding Guide to TypeSafe AI Jev: Typed Decisions, Calibrated Confide: https://www.marktechpost.com/2026/09/23/a-coding-guide-to-typesafe-ai-jev/
- Introducing MentalHealthBench: https://openai.com/index/introducing-mentalhealthbench
- HKUDS/nanobot repo: https://github.com/HKUDS/nanobot
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- ahujasid/mcp-for-blender repo: https://github.com/ahujasid/mcp-for-blender
- Kyutai Releases Voice of Reason: A Speech-Native Model that Solves Spo: https://www.marktechpost.com/2026/09/22/kyutai-releases-voice-of-reason-a-speech-native-model-that-solves-spoken-math-with-reinforcement-learning/
- abenzerps/Qwen-Image-2.1-Uncensored-GGUF trending on Hugging Face: https://huggingface.co/abenzerps/Qwen-Image-2.1-Uncensored-GGUF

---

## Release Coverage Check

- **Hermes Agent** — Latest stable verified: `v2026.9.24`, published 2026-09-24T10:09:38Z. Recent episode version tags detected: `v2026.9.11`, `v2026.9.14`, `v2026.9.21`, `v2026.9.7`. Selected missing version(s): `v2026.9.24`.
- **OpenAI Codex** — Latest stable verified: `rust-v0.157.0`, published 2026-09-25T02:31:06Z. Recent episode version tags detected: `rust-v0.153.2`, `rust-v0.155.0`, `rust-v0.155.1`, `rust-v0.156.1`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.274`, published 2026-09-16T22:36:09.883Z. Recent episode version tags detected: `2.1.267`, `2.1.273`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-09-25). Recent episode version tags detected: `@google/antigravity`, `v2.0`.

---

## Harness Version Reference

- **Hermes Agent** — `v2026.9.24`
- **OpenAI Codex** — `rust-v0.157.0`
- **Claude Code CLI** — `2.1.274`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
