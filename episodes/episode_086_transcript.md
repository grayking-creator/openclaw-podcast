# AgentStack Daily EP086 — OpenClaw 7.1, Codex .144 Point Four, the terminal-based AI coding agent Claude Code .202, and Kwaipilot on OpenRouter

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: OpenClaw 7.1 shipped with openclaw attach, a rebuilt Control UI, guided onboarding, broader model support, and official iOS, Android, and macOS client upgrades. The concrete surfaces are sessions, approvals, Gateway health, scheduled work, remote browser control, workspace terminals, and mobile connection recovery. The terminal-based coding agent OpenAI Codex .144 point four improved tracked results for delegation and native subagents, while the terminal-based AI coding agent Claude Code .202 now has a direct session handoff surface from OpenClaw.

[ALLOY]: Today: OpenClaw hands selected sessions to Claude Code, Codex returns more reliable structured subtask results, and OpenRouter adds Kwaipilot’s KAT-Coder-Air V2.5 with a 256,000-token context window.

[NOVA]: Robotics work brings ABot-AgentOS for long-horizon embodied planning and Amap’s ABot-N1 for visual language navigation. Security researchers show how distributed backdoors evade per-message monitors, while Salesforce pushes video question answering toward pixel-level evidence.

[ALLOY]: The queue also includes culture-aware moral reasoning, PPVC factory scheduling, JobHop v2 career trajectories, transformer circuit manifolds, MM-ToolSandBox, LightMem-Ego, Requential Coding, AdvancedMathBench, three MCP repositories, two Kwaipilot model listings, Ollama .32, and three extra research candidates.

[PAUSE]

## [02:00] Agent Stack Release Readout: OpenClaw 7.1; OpenAI Codex .144 Point Four; Claude Code .202

[NOVA]: OpenClaw 7.1 shipped July thirteenth with 3,063 contributions from 532 contributors, and the most direct multi-agent change is openclaw attach. The command gives the terminal-based AI coding agent Claude Code .202 temporary access to a selected OpenClaw session, so context, approvals, and active workspace state can pass into a coding run without rebuilding the conversation. The release also overhauls the Control UI: live Tasks, usage and cost views, downloads, pairing, approvals, Gateway health, sessions, goals, scheduled work, workspace terminals, and remote browser control now sit closer to the conversation surface. Gateway crash loops are explicitly called out as improved.

[ALLOY]: The terminal-based coding agent OpenAI Codex .144 point four also advances the subagent path. Delegation and native subagents now return tracked results more reliably, so a parent agent can read structured output from a Codex subtask instead of scraping logs or waiting on loose text. That matters in CI runners, editor sidecars, and long terminal sessions where the parent agent has to recover state after a child task fails, times out, or produces partial work.

[NOVA]: Model support widened across OpenAI and Codex routes with GPT-5.6 compatibility work, Tencent Hy3 gained a complete setup path, and the Meta Model API added Muse Spark 1.1. Underneath, OpenClaw calls out reliability work across Claude, Ollama, ClawRouter, and LongCat, plus broader provider choices for Copilot. The official clients moved in lockstep: iOS and iPadOS, Android, and macOS received work across setup, navigation, chat, voice, permissions, localization, offline reading, queued sends, connection recovery, and native session controls.

[ALLOY]: Messaging integrations also got concrete surface changes. Telegram receives live progress, photos and attachments, topics, commands, retries, account routing, setup, and delivery fixes. Slack improves threads, cards, progress, identity, reactions, and duplicate prevention. Discord updates cover replies, attachments, voice sessions, progress, reconnects, multi-account behavior, and unread cues. The release makes cross-harness handoff less bespoke: OpenClaw can attach Claude Code, Codex subtasks return tracked results, and the Control UI exposes more of the runtime boundary where approvals, browser state, terminals, and Gateway health meet.

[PAUSE]

## [03:38] OpenRouter Adds Kwaipilot Coding Model to Catalog

[NOVA]: OpenRouter added Kwaipilot’s KAT-Coder-Air V2.5 to its model catalog. The visible technical configuration is sparse but important: the listing exposes a 256,000-token context window, with no public parameter count, benchmark table, or pricing attached on the model page. Access runs through OpenRouter’s chat completions surface using the Kwaipilot model identifier, so existing OpenRouter-aware agent harnesses can route coding traffic to it without a separate Kwaipilot account or a new SDK.

[ALLOY]: A 256K context window puts KAT-Coder-Air V2.5 into the long-context coding tier. A coding agent can include a large repository slice, accumulated tool transcripts, generated patches, reviewer comments, dependency manifests, and longer failure logs in one prompt before leaning on summarization. That does not guarantee better reasoning, but it changes the prompt budget and lowers the pressure to compress every intermediate state.

[NOVA]: OpenRouter’s routing layer also shapes the operational behavior. Rate limits, retries, caching, request tracing, and fallover follow the same router conventions as other catalog models, rather than exposing Kwaipilot as a one-off endpoint. That makes the model easy to compare against existing coding defaults in agents already wired through OpenRouter, especially when the same prompt, tool trace, and response schema can stay unchanged.

[ALLOY]: The missing pieces still matter. Without a model card, public eval data, or pricing, the listing is an availability event more than a capability claim. KAT-Coder-Air V2.5 is now reachable behind a 256K context window; the next meaningful data point is whether Kwaipilot publishes benchmark numbers, latency characteristics, and token costs that justify moving long-repository coding sessions onto it.

[PAUSE]

## [05:24] ABot-AgentOS Bridges Long-Horizon Reasoning and Robot Low-Level Controllers

[NOVA]: ABot-AgentOS proposes a general-purpose robotic operating system for embodied agents that need high-level reasoning above low-level Vision-Language-Action controllers. The paper separates the deliberative layer from the controller layer: instead of asking one model to perceive, plan, and actuate end to end, ABot-AgentOS manages scene-conditioned planning, tool use, multimodal memory, and execution across robot embodiments. The work has drawn attention on HuggingFace’s daily feed, where the tracked count reached 61 upvotes.

[ALLOY]: The core runtime idea is context-isolated skill execution. Skills run as modular units inside isolated execution environments, rather than as one continuous stream of raw action tokens. That gives the system a boundary around each task phase and reduces state corruption when a robot performs a multi-step job such as finding an object, navigating to it, manipulating it, and confirming completion.

[NOVA]: ABot-AgentOS also uses multimodal memory to compare the current scene against the predicted outcome before proceeding. If the robot expected a drawer to be open or an object to be grasped, the memory loop can catch the mismatch before the next phase builds on a failed step. The paper pairs that with a hybrid edge-cloud execution model: immediate perception and safety checks stay on device, while heavier planning and high-dimensional scene reasoning can move to cloud compute.

[ALLOY]: The useful abstraction is robot-agnostic skill management. A developer can express a higher-level skill once, then let the AgentOS mediate execution across different hardware bodies and controller capabilities. The hard part moves into actuator mapping, latency tolerance, and safety boundaries: a planner that works in simulation still has to survive grippers, wheels, arms, cameras, and network links that behave differently in the physical world.

[PAUSE]

## [07:16] Distributed backdoors break per-step monitors in multi-agent stacks

[NOVA]: Yibo Hu and Ren Wang’s new arXiv paper targets a weak spot in multi-agent safety: per-message runtime monitors. The attack class splits a harmful payload across multiple agents so each fragment can look harmless under a local view, while the assembled object performs the harmful action. The authors call the key limit an observability boundary: if a monitor only sees a fragment that is indistinguishable from benign traffic, no detector operating on that same view can reliably catch it.

[ALLOY]: The study evaluates the idea across a controlled testbed, an external benchmark, and end-to-end agent runs. Local monitors lose signal as the local evidence of the payload disappears, then recover only when the monitor sees the fully assembled representation. That matters because many current agent stacks inspect each message, tool call, or handoff independently, then assume safety composes across the whole system.

[NOVA]: Two results anchor the paper. A monitor trained only on benign traffic recovers the attack’s code structure across held-out encodings with a 0.874 mean AUROC. A decoded-view gate, when given the encoding family, blocks every tested attack. AUROC measures how well a detector separates positive and negative cases across thresholds; here, it shows that the right representation can expose structure that local fragments hide.

[ALLOY]: More logging alone does not solve the problem. Full-trace monitors and decoders still fail unless they reach the representation where the payload becomes visible. Multi-agent safety therefore needs assembly-aware inspection at the boundary where fragments combine, not only per-step filters attached to individual messages. The paper’s most pointed claim is mathematical: once fragments are benign under the monitor’s view, stronger classifiers cannot recover information that the view never exposed.

[PAUSE]

## [09:01] MET paper grounds moral reasoning in culture-aware theory prompts

[NOVA]: Ayoung Lee, Ryan Kwon, and Yunxiang Zhang published MET, a multilingual moral-reasoning framework built around culture-aware theory prompts. The paper attacks three gaps: translated benchmarks often miss local moral context, inference scaffolds tend to be static and English-centric, and moral reasoning datasets usually require costly human labels or stronger-model supervision. MET instead uses expert-curated theory from psychology and philosophy at inference time.

[ALLOY]: The paper ships MCLASH, a multilingual moral decision-making benchmark designed around culturally situated norms rather than direct translation from English. It also introduces a two-step method: first, the model selects situation- and culture-specific moral grounds; second, it reasons over those grounds in the user’s language. MET-D adds self-distillation focused on that second reasoning step, without external moral labels.

[NOVA]: The reported numbers cover Qwen3-4B, Qwen3-8B, and Gemma3-4B. MET-D improves macro-F1 over the base models by an average of 3.71 points on MCLASH and 4.23 points on MMoralExceptQA. The largest reported gain is 12.94 points for Malay on Qwen3-8B. Macro-F1 averages class-level F1 scores, so gains reflect better balance across labels, not just improvement on the largest category.

[ALLOY]: The important mechanism is the split between selecting cultural-theory grounds and producing the final answer in the target language. That keeps the scaffold portable across smaller models and avoids needing a labeled moral dataset for every language. The small-model results matter because Qwen3-4B and Gemma3-4B gain from prompting and self-distillation rather than from a larger proprietary judge. Watch whether MCLASH becomes a shared benchmark and whether the recipe transfers to domains beyond moral reasoning.

[PAUSE]

## [10:51] Time-Lag-Aware Deep RL for PPVC Factory Scheduling

[NOVA]: Ziheng Zhang and Wei Zhang posted a paper on flexible job-shop scheduling for prefabricated prefinished volumetric construction, or PPVC, module factories. The work adds a benchmark and a deep reinforcement-learning policy that lands within about 4% of a constraint-programming reference. PPVC factories include post-operation time lags: concrete cures, water undergoes ponding tests, or paint dries after a workstation finishes, while the workstation itself becomes available again.

[ALLOY]: Those delays change the scheduling problem sharply. On instances grounded in an official national prefabrication guidebook, time lags inflate the optimal reference makespan by about 67% on average. Ignoring the lags during decision-making and repairing the schedule later performs worse than every dispatching rule tested, because the policy has already made choices that do not respect the hidden blocking structure.

[NOVA]: The authors adapt a dual-attention deep RL solver with three ablatable extensions: lag-aware dynamics with an admissible reward bound, two anticipatory feature channels that expose remaining wait time to the policy, and liveness-masked operation and station-type embeddings that distinguish active work from lag-blocked operations. With the extensions disabled, the implementation reproduces the original solver, which helps attribute the gains to the lag-aware additions.

[ALLOY]: On held-out instances, the learned policy beats dispatching rules and a genetic-algorithm metaheuristic, with a wider advantage under capacity contention. A single size-mixed policy maintains the lead across the trained range of factory sizes, and the authors release a guidebook-grounded benchmark generator. The broader contribution is a concrete treatment of delayed feasibility inside a planning loop rather than as an after-the-fact repair.

[PAUSE]

## [12:36] JobHop v2 scale-up enables reasoning-controlled extraction for career trajectory agents

[NOVA]: Iman Johary, Guillaume Bied, and Alexandru C. Mara released JobHop v2, a large-scale career trajectory dataset built from 440,000 pseudonymized multilingual resumes from the Flemish Public Employment Service. The pipeline produces 355,315 high-fidelity trajectories, grounded in authentic free-text resume content rather than synthetic career paths. The data is mapped to ESCO occupational codes, with quarter-level timing and a normalized five-level education tier.

[ALLOY]: The extraction task matters because career agents need more than isolated job titles. They need sequences: occupation changes, education shifts, timing, and progression patterns across languages. JobHop v2 turns noisy resume text into structured trajectories while preserving enough temporal resolution to reason about job hops, skill gaps, and labor-market pathways. That makes the dataset closer to public employment intake than scraped profile summaries.

[NOVA]: Evaluated against human annotations, the best extractor lands only one to three percentage points below the inter-annotator ceiling. That means the limiting factor approaches human disagreement rather than obvious model failure. The ESCO linkage also makes the output interoperable with occupational taxonomies used in employment services and labor-market analytics, where a free-text title has to map onto a stable occupation concept.

[ALLOY]: The scale-up gives career-planning agents a more realistic substrate than hand-authored or synthetic histories. It can support retrieval, forecasting, recommendation, and policy analysis where timing and occupational normalization matter. The multilingual source matters too: resume phrasing varies by language, region, and institution, so extraction systems trained only on clean English profiles often miss equivalences that public employment services need to preserve.

[PAUSE]

## [14:23] Amap's ABot-N1 Pushes Foundation Models Into Visual Language Navigation

[NOVA]: Amap’s CVLab has a new foundation-model paper on ABot-N1, aimed at Visual Language Navigation. VLN means an embodied agent moves through real or simulated spaces by following natural-language instructions. ABot-N1 positions itself as a general-purpose model for grounded spatial reasoning across embodied tasks, rather than a narrow navigation policy tuned to one simulator or scene distribution.

[ALLOY]: The paper criticizes monolithic VLN policies that map observations directly to actions in one end-to-end pass. Two failure modes dominate that setup. Coordinate drift causes the agent’s internal position estimate to degrade over longer trajectories. Long-tail semantics create a separate breakage point: unusual landmarks, ambiguous references, and rare spatial phrases fall outside the common rooms and objects seen in training.

[NOVA]: ABot-N1 aims to combine deep reasoning for grounded spatial decisions with broad transfer across environments. The intended behavior is a single backbone that can interpret instructions such as “go past the red awning on the left” and carry that capability into unfamiliar spaces without per-environment fine-tuning. The paper frames interpretability as necessary for robustness, because black-box trajectories make it hard to tell whether the agent understood the instruction or merely followed a dataset shortcut.

[ALLOY]: HuggingFace’s daily feed tracked the paper at 71 upvotes, which is meaningful community attention for a vision-language navigation submission. The next proof points are released weights, benchmark scores, and long-tail navigation results. The diagnosis is clear: navigation agents need persistent spatial state, grounded language parsing, and recoverable trajectories. The claim needs evidence that ABot-N1 reduces drift and handles rare spatial language better than current VLN baselines.

[PAUSE]

## [16:12] Researchers Identify Low-Dimensional Manifolds Governing Transformer Inductive Reasoning and Circuit Formation

[NOVA]: Tiberiu Musat, Tiago Pimentel, and Nicholas Zucchet published a theoretical framework for how inductive reasoning emerges in Transformers. The paper, Invariant Learning Dynamics of Transformers in Inductive Reasoning Tasks, introduces a generalized class of inductive tasks that unifies settings such as in-context n-grams and multi-hop reasoning. It moves from isolated benchmark behavior toward a mathematical account of training dynamics.

[ALLOY]: The central finding is a low-dimensional invariant manifold that confines the learning dynamics of attention models. Instead of tracking millions or billions of parameter values, the authors show that training can be analyzed through a small set of interpretable coordinates. Those coordinates describe how the model chooses between in-context learning, where it uses prompt examples at inference time, and in-weights learning, where it stores the rule in parameters.

[NOVA]: Data statistics drive that competition. Some distributions encourage memorization inside weights; others encourage general reasoning from context. The framework also explains how random initialization affects circuit formation. When several architectural solutions can solve the same task, the initial weights influence which circuit wins during optimization.

[ALLOY]: That gives model evaluators a possible diagnostic coordinate frame: detect which reasoning circuit a trained model learned without relying only on final-output accuracy. The authors report that the low-dimensional coordinates remain tractable for theoretical and empirical analysis in standard attention architectures. Watch for these manifold-style diagnostics to appear in automated eval pipelines that inspect whether a model learned a reusable reasoning circuit or a brittle shortcut.

[PAUSE]

## [18:05] Salesforce Paper Formalizes Evidence-Backed Video QA

[NOVA]: Salesforce AI Research published work on Evidence-Backed Video Question Answering, or E-VQA. A model must return both an answer and the spatio-temporal evidence behind it. The evidence format combines temporal segments with dense, tracked object segmentation masklets, which are object masks followed across video frames. The paper argues that answer accuracy alone hides whether a Video LLM actually looked at the relevant visual evidence.

[ALLOY]: Two artifacts ship with the work. ST-Evidence is described as the first human-verified benchmark for both discriminative and generative pixel-level video grounding, so models must localize answers in space and time. ST-Evidence-Instruct is a 160,000-sample training set generated by automated pipelines to teach grounded video outputs rather than free-form answers detached from visual support.

[NOVA]: The reported improvement is large. Fine-tuning grounded Video LLMs on ST-Evidence-Instruct beats size-matched UniPixel baselines by 27.2 points on t-mean and 13.8 points on J&F when measured on a 7B model. J&F combines region similarity and contour accuracy for segmentation quality, so the gain points to better visual grounding, not just more fluent answer text.

[ALLOY]: The paper also shows that QA accuracy and true visual perception can decouple, and scaling alone does not close the gap. Video agents used on surveillance footage, product demos, robotics telemetry, or inspection workflows need evidence traces that point to pixels and time ranges. The masklet contract also creates an auditable output: a human reviewer can inspect where and when the answer was grounded instead of trusting a fluent explanation.

[PAUSE]

## [19:48] MM-ToolSandBox Benchmark Reveals Visual Grounding Gap in Tool-Calling Agents

[NOVA]: Kaixin Ma, Di Feng, and Alexander Metz introduced MM-ToolSandBox, a benchmark and evaluation framework for agents that read images and act through tool calls. The environment is stateful, spans more than 500 tools across 16 application domains, and supports multi-image, multi-turn tasks. Agents must ground visual inputs as they arrive, then convert that grounded understanding into executable calls.

[ALLOY]: The benchmark includes conversational dynamics that single-shot prompts usually miss: goal revisions, error corrections, and state mutations during sustained sessions. It was built with information-flow-guided scenario planning and multi-stage quality filtering, yielding 258 human-verified nominal scenarios plus 50 variants focused on interactive UI applications.

[NOVA]: Twelve state-of-the-art models were evaluated, from 4B open-weight systems to frontier proprietary models. Even the best-performing model achieves below 50% success on the nominal scenarios. The failure analysis is more revealing than the top-line score: 53% of failures come from incorrect information extraction from images, even when the underlying task workflow is otherwise correct.

[ALLOY]: The authors call this a planning-to-precision crossover. Smaller models often fail at deciding what to do; larger models more often fail at perceiving the exact visual facts needed for the tool call. Visual tool-calling therefore has two reliability surfaces: planning and perception. Higher model scale may help the first, but screenshots, diagrams, UI state, and image details still need better grounding mechanisms before agents can safely operate rich interfaces.

[PAUSE]

## [21:35] LightMem-Ego: Streaming Multimodal Memory for Wearable AI

[NOVA]: LightMem-Ego targets long-term memory for wearable AI assistants. The paper focuses on mobile and wearable devices that continuously perceive a user’s day through visual and audio streams, known as egocentric capture, then answer questions about past experiences on demand. HuggingFace’s daily feed tracked it at 29 community upvotes.

[ALLOY]: Continuous multimodal memory strains device constraints. A wearable assistant cannot keep every moment inside a context window, and cloud offload adds latency, cost, privacy exposure, and connectivity dependence. LightMem-Ego is positioned as a streaming memory system that accumulates everyday experiences as they arrive, organizes them, and makes them queryable later on the same class of device that captured them.

[NOVA]: That shifts attention from the model alone to the memory runtime: compression, indexing, retrieval, temporal alignment, visual-audio fusion, and privacy boundaries. A user might ask where they left keys, who mentioned a meeting, or what product they saw in a store; answering requires a persistent representation of past perception, not a one-shot prompt.

[ALLOY]: The next useful details are a reference implementation, benchmark comparisons against cloud-backed memory baselines, and hardware constraints such as battery, memory footprint, and on-device latency. Wearable agents will only feel practical if long-term recall runs quietly in the background without turning every life log into a remote inference dependency. The privacy boundary is especially important because egocentric capture contains bystanders, locations, routines, and conversations by default.

[PAUSE]

## [23:21] Requential Coding: New SOTA Generalization Bounds for LLMs

[NOVA]: Shikai Qiu, Marc Finzi, and Yujia Zheng introduced Requential Coding, a compression framework for understanding what large models have learned. Traditional quantization gives code lengths tied to model size, even when many parameters may not store useful information. Prequential coding compresses a training trajectory, but still encodes the exact data sequence, which can produce large codes on high-entropy data.

[ALLOY]: Requential Coding changes the setup with a teacher-student scheme. A teacher selects training samples drawn from the student model’s own distribution, and the student’s code records only those selections. Bits are spent on disagreements between teacher and student, so the code reflects genuine learning rather than raw parameter count or data entropy.

[NOVA]: The resulting code length is independent of both parameter count and data entropy, and is often orders of magnitude shorter than the prequential counterpart. The effect grows as models scale. Holding loss fixed, larger models and ensembles compress to smaller sizes despite having more parameters, a result prior compression views do not expose.

[ALLOY]: When plugged into a PAC-Bayes bound, Requential Coding yields state-of-the-art generalization guarantees for billion-parameter LLMs and outperforms bounds built on aggressive post-training quantization, even when that quantization is granted zero error. The contribution is mainly measurement: compression becomes a probe of learned structure. Watch for reproductions on open-weight checkpoints and reasoning-tuned models.

[PAUSE]

## [25:05] AdvancedMathBench Establishes New Evaluation Standards for Doctoral-Level Mathematical Proof Generation and Verification

[NOVA]: Lingkai Kong, Zijian Wu, and Yuzhe Gu published AdvancedMathBench to push mathematical evaluation beyond high-school and olympiad-style problems. The suite targets undergraduate and doctoral qualifying-exam levels, with ProverBench containing 296 problems designed to evaluate complex proof generation. Final-answer matching is not enough here; a model can land on a correct-looking conclusion while making invalid symbolic moves.

[ALLOY]: The authors built an automatic verification pipeline trained on large-scale expert annotations. It returns correctness verdicts plus fine-grained assessments of proof errors, moving beyond a binary pass or fail. A second component, VerifierBench, contains 888 model-generated proof trajectories paired with expert ground truth, measuring whether models can judge proof validity and explain their judgments. The verifier side matters because proof generation and proof checking are different skills.

[NOVA]: The reported frontier-model results show a sharp difficulty increase. The best-performing tested model, GPT-5.5-xhigh, scores 75.8 on the undergraduate split and drops to 66.1 on the doctoral qualifying-exam split. As symbolic complexity rises, even the strongest systems expose reasoning gaps that simpler answer-based benchmarks may miss.

[ALLOY]: AdvancedMathBench gives technical agents a stricter evaluation surface for theorem proving, mathematical auditing, and self-correction. The fine-grained verifier matters because future proof agents need to identify the exact invalid step, not merely announce that a proof failed. The doctoral split also creates pressure on models to sustain definitions, lemmas, and proof dependencies over longer chains, where surface-level pattern matching fails earlier.

[PAUSE]

## [27:10] GitHub Project Radar

[NOVA]: DeusData codebase-memory-mcp enters the radar with 31,313 stars, a latest point nine release from July eighth, and an update on July thirteenth. It provides a high-performance code-intelligence MCP server that indexes a repository into a persistent knowledge graph across 158 languages, shipped as a single static binary with zero dependencies. Its headline mechanism is sub-millisecond semantic lookup after indexing, using the Model Context Protocol as the agent-facing interface. OpenClaw, Codex, Claude Code, or Hermes can use it as a context backend instead of repeatedly re-reading source material during every agent session.

[ALLOY]: PrefectHQ fastmcp arrives with 26,195 stars and a 3.4 release from July ninth. It provides a Pythonic framework for building MCP servers and clients with clean ergonomics and fast iteration. The traction signal is a large first radar appearance tied to a fresh release. Its mechanism is protocol abstraction: developers expose tools and resources without hand-writing MCP boilerplate, while keeping Python type hints and schemas close to the implementation. The integration angle is rapid tool-server creation for any harness that speaks MCP, including OpenClaw, Codex, Claude Code, and Hermes.

[NOVA]: Microsoft mcp-for-beginners enters with 16,752 stars and an update on July thirteenth. It offers an open-source curriculum for MCP fundamentals across dot net, Java, TypeScript, JavaScript, Rust, and Python. No GitHub release is published, but the traction is strong. Its example-driven protocol education covers schemas, tool contracts, and security boundaries through cross-language implementations. The integration angle is reference material for hardening the contracts agents negotiate with third-party MCP servers, especially when tool permissions and data exposure have to be explicit.

[PAUSE]

## [28:35] Model Discovery Check

[ALLOY]: Kwaipilot KAT-Coder-Air V2.5 is newly listed through OpenRouter with API availability and a 256,000-token context window. The public listing does not expose active parameters, total parameters, pricing, or benchmark scores. Its main relevance is long-context coding traffic through an existing OpenRouter-compatible agent stack, where the router handles the request surface and the model handles the enlarged prompt budget.

[NOVA]: Kwaipilot KAT-Coder-Pro V2.5 is also newly listed through OpenRouter, with the same 256,000-token context window surfaced publicly. Parameter counts and eval tables remain absent. Pro gives Kwaipilot a second catalog entry for coding agents, and the useful comparison will be latency, price, reliability under long prompts, and quality against Air once more details are published.

[PAUSE]

## [29:20] Local LLM Spotlight

[ALLOY]: Ollama .32 introduces a new interactive agent experience. Running Ollama by itself now launches a local coordinator that can chat, code, search the web, and delegate work from one prompt-driven surface backed by local and cloud models. The release keeps Ollama’s single-binary local serving path, but adds routing that selects a model for each delegated task.

[NOVA]: The Codex App integration is renamed ChatGPT and exposed through the Ollama launch ChatGPT command, with a restore flag for returning to a prior session. Ollama moves from serving runtime toward hybrid agent coordinator while preserving local inference for lower-latency or privacy-sensitive work. The added router also makes local models, cloud models, search, and coding actions feel like one conversation surface instead of separate commands.

[PAUSE]

## [30:05] Extra Research Candidates

[NOVA]: Requential Coding: Pushing the Limits of Model Compression with Self-Generated Training Data extends the generalization story with a teacher-student coding scheme. A teacher selects samples from the student’s own distribution, so the code length tracks learned disagreement rather than parameter count or raw data entropy. The claim is not just smaller compression, but a bound that better reflects the structure a model actually learned.

[ALLOY]: Transformer-Guided Swarm Intelligence for Frugal Neural Architecture Search combines an autoregressive Transformer controller trained with reinforcement learning for global macro-search and an Artificial Bee Colony algorithm for local micro-exploitation. A dynamic entropy term helps escape premature convergence, aiming to reduce the GPU-day cost of neural architecture search while still exploring both high-level architecture families and smaller design choices.

[NOVA]: From Global to Factor-Wise Expert Composition in Discrete Diffusion Models decomposes each sample into smaller factors and routes each factor to a specialized expert. That replaces a single global scalar mixing schedule with factor-wise expert composition, aimed at more precise compositional reasoning in discrete diffusion systems. The technical bet is that different parts of a discrete sample may need different experts at the same generation step.

[PAUSE]

## [31:00] Practical queue

[ALLOY]: OpenClaw, Codex, and Claude Code tightened the harness layer around session handoff, subagent results, approvals, and runtime visibility.

[NOVA]: Kwaipilot’s OpenRouter listings bring 256K coding context to a router surface, but pricing, latency, parameters, and public evals still need daylight.

[ALLOY]: The research thread is clear across robotics, video, screenshots, wearables, and math: agents need grounded evidence, durable memory, and verification surfaces that expose more than final answers.

[NOVA]: The GitHub radar points toward MCP as the connective tissue for code memory, tool servers, and safer third-party integrations.

[ALLOY]: Local serving is also shifting upward: Ollama now presents an agent coordinator while keeping the single-binary model runtime underneath.

[NOVA]: The security work adds a harder boundary condition for multi-agent systems: fragments can look harmless until a downstream agent assembles them.

[ALLOY]: For source material and links, look at the show notes at Toby On Fitness Tech dot com. Thanks for listening to AgentStack Daily. We'll be back soon.
