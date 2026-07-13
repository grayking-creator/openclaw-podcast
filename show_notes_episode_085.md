# AgentStack Daily EP085 — Codex rust-v0.144.3, Apple Sues OpenAI, vLLM 0.25.0 Defaults Model Runner V2

**Title:** Codex rust-v0.144.3 Lands, vLLM 0.25.0 Defaults Model Runner V2, Apple Sues OpenAI

**Tagline:** OpenAI ships Codex rust-v0.144.3 alongside rust-v0.144.2, and vLLM 0.25.0 promotes Model Runner V2 to default for dense models. Apple filed suit against OpenAI alleging trade secret theft by former employees. Research highlights include Freya-TTS, a 183M flow-matching DiT that outscored larger Turkish TTS stacks, SAGEAgent trimming diagnostic burden 55% on glioma survival prediction, and Agora swapping its agent router for an auction over reasoning steps. A two-agent system posted 0.402 on QANTA 2026, and PAC-ACT applied chunk-level RL post-training to Action Chunking Transformer policies.

**Feed description:** OpenAI ships Codex rust-v0.144.3 and rust-v0.144.2; vLLM 0.25.0 promotes Model Runner V2 to default for dense models. Apple sues OpenAI over alleged trade secret theft by ex-employees. Plus Freya-TTS hits Turkish speech with a 183M flow-matching DiT, SAGEAgent cuts glioma diagnostic burden 55%, Agora moves from a router to an auction over reasoning steps, a two-agent system posts 0.402 on QANTA 2026, PAC-ACT trains Action Chunking Transformer policies with chunk-level RL, and Semantic Pareto-DQN addresses fraud collapse without resampling.

---

## Story Slate

1. **Agent Stack Release Readout: OpenAI Codex rust-v0.144.3, rust-v0.144.2**
On July 13, 2026, OpenAI shipped Codex rust-v0.144.2 — a bug-fix release that reverted a prompting regression in Guardian, the CLI's automated code-review stage. Authored by @dylan-hurd-oai as PR #32672 against the release/0.144 branch, the change restored Guardian's prior auto-review policy, request format, and tool behavior. About 93 minutes later, rust-v0.144.3 followed as a version-only release carrying no additional merged pull requests, republishing the same patched tree on the same branch. Teams running Guardian in CI should pull v0.144.2 to realign with the restored baseline.
Technical depth angle: PR #32672 (release/0.144, author @dylan-hurd-oai) rolls back 'Update auto review prompting' to restore Guardian's prior auto-review policy, request format, and tool behavior together. rust-v0.144.3 is a chained version-only bump — no additional merged pull requests between the two tags, so the patched tree is identical. The 93-minute gap between the 04:39:22Z and 06:12:19Z publish times suggests the version-only release republished the same tree under the release chain rather than waiting on a separate feature cycle.
Actionability angle: If your team pins a Guardian review output schema or runs golden tests against its auto-review comments, pull Codex rust-v0.144.2 to realign with the behavior your assertions were originally written against. Review comment patterns that shifted during the regression window will match the pre-regression baseline after this update, which is the fix rather than a new behavior to learn.
Listener hook: Codex Guardian just got silently reset to its prior prompt — if your CI checks Guardian review output, v0.144.2 is the line your golden tests will pass against again.

2. **Apple sues OpenAI over alleged trade secret theft by ex-employees**
Apple filed suit against OpenAI on July 10, 2026, accusing former employees of stealing trade secrets. The complaint alleges the misconduct was directed by OpenAI's senior leadership, including a longtime former Apple employee. The story drew heavy attention on Hacker News with a score of 1640, signaling developer interest in the legal fight between two major AI players. The case centers on alleged coordinated theft rather than individual departures, raising questions about IP protections as AI talent moves between competitors.
Technical depth angle: The complaint alleges coordinated misconduct directed from OpenAI's senior leadership, involving a longtime former Apple employee now within that leadership tier. Hacker News traction (score 1640) shows the developer community treating this as more than a routine employment dispute. The case turns on whether individual departures were part of an orchestrated recruitment and IP transfer scheme.
Actionability angle: This case signals that AI labs are willing to pursue coordinated theft claims against competitors, not just individual departures. For builders crossing between AI organizations, expect sharper IP enforcement that affects confidentiality terms and post-employment restrictions.
Listener hook: Two of the biggest names in AI are now fighting in court over people, and the developer community noticed fast.

3. **Task-Specific Two-Agent System Tops QANTA 2026 at 0.402**
arXiv paper 2607.09623 from Nirjhar Das and Md. Al-Mamun Provath documents their first-place submission to the QANTA 2026 multimodal quizbowl shared challenge, hosted at the ICML 2026 Workshop on Efficient Multimodal Question Answering. The system is a hosted-only, two-agent architecture built around a GPT-4o-mini-class Tossup agent with confidence calibration and a GPT-4o-class Bonus agent with leadin-aware reasoning and multimodal evidence integration, with no retrieval pipeline and no model ensembles. It earned the top overall QANTA leaderboard score of 0.402, decomposing into a Tossup score of 0.238 and a Bonus Effect score of 0.164, showing that task-specific reasoning policies can outperform heavier stacks under matched inference budgets.
Technical depth angle: Hosted-only two-agent architecture. The Tossup agent runs a GPT-4o-mini-class model with confidence-calibrated answering plus a domain-specific numeric reasoning policy that suppresses overconfident predictions from isolated quantitative clues. The Bonus agent runs a GPT-4o-class model with leadin-aware reasoning, structured relational reasoning, and multimodal evidence integration. No retrieval pipeline and no model ensembles are used. Eval is the QANTA 2026 leaderboard, scored on pyramid-style quizbowl questions with incrementally revealed text and images.
Actionability angle: For builders running hosted agents, this is evidence that decomposing a task into separately-tuned roles and applying explicit confidence calibration can outperform larger single-model or ensembled setups under a fixed inference budget. The two-agent design pattern, with one agent owning decide-when-to-act uncertainty and the other owning exact-answer precision, transfers conceptually to coding and tool-use agents where early-decision errors carry high cost. Why this matters: small, task-specialized hosted models with strong prompting and calibration policies remain competitive with heavier pipelines on benchmarks built around efficiency.
Listener hook: A hosted-only two-agent GPT setup beat the QANTA 2026 quizbowl leaderboard at 0.402 with zero retrieval and zero ensembling, and the design pattern travels straight to coding agent stacks.

4. **PAC-ACT: Chunk-level RL post-training for Action Chunking Transformer policies**
Researchers Yujie Pang and Zudong Li released PAC-ACT (arXiv 2607.09590), a reinforcement-learning post-training framework that targets pretrained Action Chunking Transformer policies for precision industrial contact manipulation. PAC-ACT reformulates policy optimization at the chunk level, builds an ACT-transferred actor-critic architecture, and uses a hybrid behavior-prior constraint to preserve the pretrained action distribution during online fine-tuning. On industrial precision-contact benchmarks it improves task success, contact stability, and force safety while keeping latency and GPU memory low; on the Contour task the proportion of force readings above 60 newtons drops by 46 times versus the behavior-cloned baseline.
Technical depth angle: PAC-ACT applies chunk-level policy optimization on top of a frozen ACT backbone using an ACT-transferred actor-critic architecture. A hybrid behavior-prior constraint preserves the pretrained action distribution during online fine-tuning, so RL exploration stays anchored. Sparse-reward ablations show the behavior prior enables exploration under randomized initial poses. On Contour, peak contact force drops and the share of force readings above 60 newtons falls by 46 times versus the behavior-cloned baseline.
Actionability angle: PAC-ACT turns a pretrained ACT policy into a target for online RL without rewriting the inference stack, which matters for builders already running chunked policies on real-time industrial cells. The behavior-prior constraint is the part worth porting: any chunked policy that needs post-hoc tightening for contact, precision, or safety margins can adopt the same actor-critic overlay. Watch whether the recipe lands in open-source RL post-training toolkits for robotics.
Listener hook: If you ship ACT-style chunked policies into contact-rich cells, PAC-ACT's chunk-level actor-critic and behavior-prior recipe is the post-training layer you can drop on top without paying the VLA latency tax.

5. **SAGEAgent Cuts Diagnostic Burden 55% on Glioma Survival Prediction**
A new clinical agent paper from Chongyu Qu, Can Cui, and Zhengyi Lu introduces SAGEAgent, a self-evolving LLM-based agent that decides which diagnostic modalities to acquire for each glioma patient. Formulated as a sequential decision problem, the agent uses clinical tools that translate numerical predictions into text, episodic memory over similar past cases, and semantic memory that accumulates reusable decision patterns. Evaluated on a glioma cohort combining TCGA-LGG, TCGA-GBM, and BraTS across four modalities, the agent holds competitive survival prediction accuracy while reducing average acquisition burden by 55 percent.
Technical depth angle: SAGEAgent formulates modality acquisition as a sequential decision problem. The LLM-based agent uses three components: clinical tools that translate numerical predictions into text for reasoning, episodic memory that retrieves similar past cases, and semantic memory that accumulates reusable decision patterns from experience. The semantic memory is what makes the agent self-evolving rather than static. Evaluation: glioma cohort combining TCGA-LGG, TCGA-GBM, and BraTS, four diagnostic modalities, 55 percent reduction in average acquisition burden at competitive survival prediction accuracy.
Actionability angle: For builders working on tool-using agents, the relevant pattern is treating expensive data acquisition as a learned policy rather than a fixed pipeline. The episodic-plus-semantic memory split maps cleanly onto retrieval pipelines any agent stack can compose today. Why this matters: it shifts cost-aware reasoning from a downstream concern to a first-class agent capability.
Listener hook: A clinical agent cuts diagnostic acquisition burden in half on glioma without losing prediction accuracy, and the architecture is a clean template for cost-aware tool-using agents.

6. **Freya-TTS: 183M Flow-Matching DiT Beats Larger Turkish TTS Stacks**
Freya-TTS is a compact Turkish-first text-to-speech model documented in arXiv paper 2607.09530 by Ahmet Erdem Pamuk, Ömer Yentür, and Ahmet Tunga Bayrak. It is a 183.2M-parameter non-autoregressive conditional flow-matching Diffusion Transformer that runs inside the frozen latent space of AudioVAE2, replacing the usual phonemizer, grapheme-to-phoneme frontend, and discrete speech tokenizer with a direct character-to-latent pipeline over a 92-symbol Turkish vocabulary. On Freya-TR-Eval, it posts a band-matched 8.0% WER and 3.0% CER while outperforming substantially larger open-source systems. With a real-time factor of 0.11 on consumer GPUs and faster-than-real-time laptop CPU inference, the authors release weights, training code, and the eval suite for edge deployment.
Technical depth angle: A 183.2M-parameter non-autoregressive conditional flow-matching Diffusion Transformer runs inside the frozen continuous latent space of AudioVAE2 (16 kHz encode, 48 kHz decode). The DiT bypasses any phonemizer, grapheme-to-phoneme frontend, or discrete speech tokenizer, ingesting a 92-symbol Turkish character vocabulary directly and producing the full latent sequence simultaneously over a predicted duration. Post-training uses single-speaker voice locking plus short-utterance coverage for conversational robustness.
Actionability angle: What this means for builders: Freya-TTS shows a tokenizer-free, phoneme-free recipe that holds its benchmark performance while collapsing the usual TTS frontend, which simplifies voice synthesis integration at the architecture level. The open weights, training and inference code, and Freya-TR-Eval give anyone building Turkish speech a concrete reference at a fraction of typical parameter counts. Why this matters: a 0.11 real-time factor on consumer GPUs plus faster-than-real-time laptop CPU inference shifts TTS from cloud-only to edge-viable.
Listener hook: A 183M-parameter Turkish TTS matches much bigger open-source stacks and runs faster than real time on a laptop CPU.

7. **Long-Horizon-Terminal-Bench Probes Multi-Hour Agent Tasks**
Long-Horizon-Terminal-Bench, a new benchmark from Zilong Li and collaborators, tests AI agents on forty-six terminal tasks spread across nine categories that cannot be solved in a single shot. The benchmark introduces dense reward-based grading that scores intermediate progress and partial solutions instead of treating an attempt as a binary pass or fail. The work targets a known gap in current agent evaluation: short, minute-scale problems with sparse final-outcome signals. The paper is trending on HuggingFace's daily papers feed with thirty-two community upvotes, hosted at arXiv 2607.08964.
Technical depth angle: The benchmark uses dense reward-based grading on a real shell environment. Agents execute commands, observe output, and accumulate partial credit as environment state advances. Forty-six tasks across nine categories are designed to resist single-shot solutions, so grading spans the full trajectory rather than collapsing to a binary final-outcome check, yielding a non-sparse reward signal usable for training and fine-tuning.
Actionability angle: Current short-horizon agent eval numbers likely overstate capability on the multi-hour engineering jobs that matter in real workflows. What this means is that benchmarks measuring only final outcomes under-credit the partial progress an agent actually makes, which is closer to how real debugging looks. Why this matters: dense grading on long-horizon terminal work gives a more honest read of where agents can and cannot operate over multi-hour stretches.
Listener hook: A new agent benchmark rewards partial progress instead of just final answers, and builders who trust short-horizon eval numbers should hear why it matters.

8. **Semantic Pareto-DQN Tackles Fraud Collapse Without Resampling**
An arXiv paper from Cláudio Lúcio do Val Lopes and Lucca Machado da Silva introduces Semantic Pareto-DQN, a multi-objective reinforcement learning framework aimed at financial anomaly detection under extreme class imbalance. The system encodes transaction features as natural-language narratives via LLMs, then optimizes a vectorial reward that decouples financial efficacy, operational friction, and semantic discovery across a continuous Pareto frontier. Evaluated on E-Commerce fraud and UCI Credit datasets, it breaks the zero-recall trap that single-objective classifiers fall into and beats scalarized baselines on minority-class recall — without distortive data resampling.
Technical depth angle: Heterogeneous transaction features are synthesized into natural-language narratives and encoded by LLMs to produce a scale-invariant state representation. A DQN agent is trained against a vectorial reward covering financial efficacy, operational friction, and semantic discovery, with the continuous Pareto frontier used to navigate asymmetric costs between missed anomalies and false positives. Evaluated on E-Commerce fraud and UCI Credit datasets.
Actionability angle: For teams operating payment or risk pipelines, this signals LLM-encoded transaction narratives plus Pareto-frontier RL as a recall-recovery layer that avoids synthetic minority oversampling. Why this matters: it reframes fraud detection as a multi-objective control problem rather than a binary classification fight against imbalance.
Listener hook: If your fraud model keeps collapsing to the majority class, this paper proposes breaking that trap without touching your training data.

9. **4DR360 Couples Detection and Occupancy via State Reasoning**
A new paper, 4DR360, from Xiaokai Bai, Lianqing Zheng, and Runwei Guan (arXiv 2607.09629) reframes radar-camera fusion for autonomous driving by treating semantic occupancy as a persistent scene state rather than a terminal output. The cross-modal state reasoning paradigm pairs State-guided BEV Enhancement with Doppler-guided Temporal Fusion, then introduces a unified cross-dataset detection-and-occupancy protocol that extends ManTruckScenes with satellite-map-generated occupancy labels and pairs it with OmniHD-Scenes.
Technical depth angle: 4DR360 models semantic occupancy as a persistent scene state propagated through coarse-to-fine stages. State-guided BEV Enhancement conditions intra-frame BEV features on the modeled state. Doppler-guided Temporal Fusion uses 4D radar Doppler cues to preserve state evidence across longer time horizons. The eval protocol extends ManTruckScenes with satellite-map-based occupancy labels and pairs it with OmniHD-Scenes for unified cross-dataset detection-and-occupancy benchmarking.
Actionability angle: What this means for builders: the framework gives perception teams a shared intermediate representation between detection and dense semantic prediction, plus a unified eval yardstick for radar-camera multi-task work instead of stitched-together dataset-specific benchmarks. Why this matters: code, the new occupancy labels, and the cross-dataset protocol release on acceptance, lowering the bar to reproduce or extend.
Listener hook: If you're building perception stacks around sparse-radar fusion or occupancy prediction, 4DR360 hands you a shared state representation and a unified cross-dataset eval protocol in one paper.

10. **Agora Replaces Agent Router With an Auction for Reasoning Steps**
Agora, a new paper by Kaiji Zhou, Ales Leonardis, and Yue Feng (arXiv 2607.09600), proposes an incentive-compatible auction mechanism for allocating reasoning steps in multi-model agent stacks. Agents bid on each step using a rectified competence signal, routing critical logic to the most capable solver rather than the most confident function-matcher. Evaluations across five benchmarks show improvements over single-model, routing, and cascade baselines drawn from comparable candidate pools, with a controllable cost-quality trade-off exposed through a single auction parameter. The work reframes agent orchestration as a market for reasoning rather than a function-call router.
Technical depth angle: Agora replaces function-level routing with an incentive-compatible auction over reasoning steps. Each step is treated as a tradeable item, and agents bid using a rectified competence signal that adjusts for overconfident self-reports. The mechanism exposes a single auction parameter that controls the cost-quality frontier, evaluated across five benchmarks against single-model, routing, and cascade baselines drawn from comparable candidate pools.
Actionability angle: Builder takeaway: the unit of allocation moves from the function or tool call to the reasoning step, with a price attached. This means heterogeneous model pools can tune cost and quality per workload using one auction parameter rather than re-engineering a cascade. The open question is whether rectified competence can be computed cheaply enough to keep the auction in the request hot path.
Listener hook: If your agent stack pays five different models to argue about the same step, you should hear how Agora turns that fight into an auction.

11. **Counting failures in VLMs traced to readout misalignment, not missing knowledge**
arXiv 2607.09544 from Ahmed Oumar El-Shangiti, Abzal Nurgazy, and Hilal AlQuabeh investigates why vision-language models fail at object counting. The authors train probes on activations from four VLMs across five counting datasets and use SVCCA to show that models encode the correct count internally but read it out along misaligned directions. A causal steering intervention validates this, and a detector-guided self-correction loop selectively re-prompts only on predicted failure, lifting counting accuracy by up to 15.6 absolute percentage points without parameter updates.
Technical depth angle: Trains nonlinear probes on internal activations of four VLMs across five counting datasets. SVCCA shows ground-truth-count probes and model-output probes share an activation subspace but read along misaligned directions. A causal steering intervention along count-identified directions improves counting, motivating a detector-guided self-correction loop that re-prompts only on predicted failure.
Actionability angle: A lightweight probe trained on VLM activations can act as a reliability gate before counting-heavy steps, catching failures before they cascade into downstream tool calls. The same read-probe-then-correct loop could wrap any structured-output call where the model likely already has the right internal answer. This reframes a class of VLM errors as alignment problems rather than knowledge gaps.
Listener hook: If your agent counts objects in images, this paper explains why it lies — and shows how to fix it without retraining.

12. **vLLM 0.25.0 ships Model Runner V2 as default for dense models**
vLLM 0.25.0 released July 11, shipping 558 commits from 232 contributors. Model Runner V2 is now the default execution path for all dense models via PR #44443, building on quantized-model support from the previous release. Three mechanisms land alongside: EVS support (#46535), realtime embeddings via #46762, and prefix caching for Mamba hybrid models. For self-hosters running local inference behind agent stacks, dense serving now consolidates onto a single runner with built-in quantization, hybrid prefix caching, and a realtime embedding endpoint.
Technical depth angle: Model Runner V2 becomes the unified execution path for dense models in vLLM 0.25.0, with quantized-model support inherited from the previous release. Three PRs anchor the new surface: #44443 makes MRv2 default, #46535 adds EVS capability, and #46762 introduces a realtime embedding endpoint. Prefix caching now extends to Mamba hybrid models, enabling cache reuse for self-hosted Mamba-based deployments.
Actionability angle: Local inference deployments pinning an older vLLM minor for MRv2 opt-in behavior can now upgrade, since the unified runner is the default for dense models. RAG and realtime retrieval workloads benefit most from the realtime embedding endpoint (#46762) and the Mamba hybrid prefix cache, both of which depend on cross-request state reuse. Production deployments running non-dense architectures will likely stay on the previous runner until MRv2 coverage expands in a future minor.
Listener hook: If you self-host vLLM for an agent stack, your dense-model serving just consolidated onto a single runner and your Mamba hybrid models just got prefix caching.

13. **A decade of VLMs closes the simple-to-complex scene gap**
Researchers Shravan Murlidaran and Miguel P. Eckstein have published arXiv 2607.09654, a decade-long study of vision-language model accuracy from 2017 to 2025. They introduce the Complex Social Behavior dataset, 100 images depicting complex social interactions, and pair it with an MS-COCO sample to evaluate nine VLMs and 20 human descriptions against a gold standard. Pre-MLLMs scored far below the lowest-ranked human descriptions on CSB, while MLLMs landed near the top-ranked humans on both datasets, erasing the gap between simple and complex scene description accuracy. Across five visual-cognitive error types, MLLMs have nearly eliminated object detection, recognition, hallucination, and scene understanding errors, with only spatial dependence remaining as a measurable gap from human performance.
Technical depth angle: CSB is a 100-image curated dataset of complex social interactions paired with an MS-COCO sample. Accuracy is scored against a gold standard for nine VLMs (four pre-MLLM, five MLLM) and 20 human descriptions. Performance decomposes into five visual-cognitive error categories: object detection, recognition, hallucination, scene understanding, and spatial dependence. Spatial dependence measures whether models rely on the same image regions as humans when generating descriptions.
Actionability angle: Builders wiring VLMs into agent pipelines that interpret screenshots, diagrams, or workplace photos get a concrete yardstick for where the visual stack matches humans and where it still diverges. The CSB methodology is replicable locally against your own domain imagery, which matters because pre-MLLM-era accuracy was effectively unmeasurable on complex behavior. For agent pipelines that hinge on human-aligned attention, spatial dependence is the known remaining risk in the visual stack.
Listener hook: A decade-long benchmark shows multimodal LLMs now match top human descriptions on complex social scenes, with only one residual error category left to close.

14. **Training-Free Logit Adaptation Boosts Medical VLMs on OOD Data**
A new training-free method called TCLA corrects inference logits on Medical Vision-Language Models, lifting out-of-distribution performance across nine medical imaging datasets including X-ray, ultrasound, MRI, CT, and histopathology. From authors Tianyou Jiang and Ziyu Zhou, the approach needs only a small support set, stays model-agnostic, and in most cases outperforms existing training-based adaptation methods, including in the 1-shot regime.
Technical depth angle: TCLA is a model-agnostic, training-free few-shot adaptation method that adjusts the inference logits of pretrained Medical VLMs using a small support set. It targets inter-class deconfusion and reduces domain shift without adding trainable parameters, working in extreme low-data regimes like 1-shot, and was evaluated across nine medical imaging modalities.
Actionability angle: For teams building clinical or imaging workflows on top of pretrained Medical VLMs, TCLA offers a way to harden OOD robustness without standing up a fine-tuning pipeline. Why this matters: it sidesteps the instability of 1-shot fine-tuning by operating purely at inference time, so a small support set is all that is required.
Listener hook: If you have been wondering whether medical VLMs can be made robust on out-of-distribution data without fine-tuning, this paper says yes — and at 1-shot.

---

## Model Discovery Check

- **Model lanes scanned** (OpenRouter major providers) — No new or materially updated models detected this cycle (verified July 13, 2026). Primary source: https://openrouter.ai/models. Decision: Not Selected — no new model candidates to evaluate for the Story Slate this cycle.

---

## Local LLM Spotlight

- **Ollama v0.31.2** — https://github.com/ollama/ollama/releases/tag/v0.31.2 — Release 0.31.2 enables flash attention on older NVIDIA compute-capability 6.x GPUs and lets iGPUs offload padded vision models to fit available memory. It hardens GGUF model creation, fixes structured output for thinking models when thinking is disabled, and makes `ollama launch` for Claude Code disable telemetry by default. Loading models from paths containing non-UTF-8 characters is also fixed.
  Try now: Pull a padded vision model such as llava, load it on an older NVIDIA card to confirm flash attention is active, and pair `ollama launch` with Claude Code to verify telemetry is silenced.

---

## GitHub Project Radar

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — High-performance code-intelligence MCP server that indexes a codebase into a persistent knowledge graph in milliseconds and serves sub-millisecond queries across 158 languages with 99% fewer context tokens. Ships as a single static binary with zero external dependencies. `stars: 30,854`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v0.9.0 (2026-07-08)`.
  Why this is on the radar now: version 0.9.0 shipped July 8, the repository was updated July 13, and its first tracked appearance already carries more than thirty thousand stars.
  Stack improvement angle: Wire it in as the primary retrieval MCP for OpenClaw, Codex, Claude Code, or Hermes so cross-file questions hit the knowledge graph instead of re-scanning the tree, dropping prompt tokens by roughly two orders of magnitude.
  Try now: Point it at a medium-sized monorepo, time a typical cross-file refactor query, and compare the result against a raw file-grep baseline.

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — Fast, Pythonic framework for building Model Context Protocol servers and clients, with ergonomics aimed at protocol implementers rather than protocol archaeologists. `stars: 26,168`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v3.4.4 (2026-07-09)`.
  Why this is on the radar now: version 3.4.4 shipped July 9 and the repository enters tracking with more than twenty-six thousand stars.
  Stack improvement angle: Stand up a fastmcp tool server in front of internal APIs or telemetry so Codex and Hermes can reach them through the same MCP envelope as the rest of the agent stack, with shared transport and auth handling.
  Try now: Wrap a single internal REST endpoint as a fastmcp tool and drive it from a Claude Code session to confirm the round-trip end to end.

- **microsoft/mcp-for-beginners** — https://github.com/microsoft/mcp-for-beginners — Open-source curriculum that walks developers through Model Context Protocol fundamentals using real, cross-language examples in .NET, Java, TypeScript, JavaScript, Rust, and Python, with labs focused on practical techniques for building modular, scalable, and secure AI workflows. `stars: 16,742`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: none published on GitHub as of 2026-07-13`.
  Why this is on the radar now: the repository was updated July 9 and enters tracking with more than sixteen thousand stars across a cross-language MCP curriculum.
  Stack improvement angle: Hand the .NET and Rust modules to the engineers owning the non-Python legs of the agent stack so they can ship MCP clients without inheriting Python-specific conventions.
  Try now: Run the TypeScript lab that wires a sample tool server to a local client and trace the message envelope step by step.

---

## Extra Research Candidates

- **TSAI-MetaFraud: A Benchmark Dataset for Financial Fraud Transaction and Behavioral Risk Detection in Metaverse Ecosystems** — https://arxiv.org/abs/2607.09528 — The emergence of metaverse platforms has created virtual economies that introduce new challenges related to fraud, bot activity, and illicit financial behavior. Despite growing interest in trustworthy metaverse analytics, existing datasets  Technical depth angle: A multimodal, multi-task graph benchmark that fuses behavioral, transactional, and graph-structured virtual-economy events and evaluates transaction-fraud detection, cross-modal node classification, temporal link prediction, and weakly supervised fraud detection with graph neural network baselines.

- **Failure as a Process: An Anatomy of CLI Coding Agent Trajectories** — https://arxiv.org/abs/2607.09510 — Large language model (LLM) coding agents are increasingly deployed to autonomously perform software engineering tasks in terminal-based environments, making their reliability a growing concern. Existing empirical studies investigate why cod Technical depth angle: A process-oriented framework that decomposes 1,794 manually annotated Terminal-Bench trajectories from OpenHands, MiniSWE, and Terminus2 into onset, evolution, and recovery phases, yielding 14 findings on epistemic error onset within the first few steps and the unrecoverability of late-stage failures.

- **Beyond Fixed Representations: The Vocabulary and Verifier Gaps in Open-Ended AI** — https://arxiv.org/abs/2607.09560 — Modern AI systems are increasingly being evaluated for their ability to reason, code, prove theorems, use tools, and long-horizon research tasks. These are powerful capabilities, but they share a structural limitation: the representational  Technical depth angle: Characterizes open-ended AI through a vocabulary gap (inventing and stabilizing new representational primitives) and a verifier gap (judging a primitive whose payoff only appears after future reuse), unified under cognitive discrepancy reduction as intra-space versus generative transformations.

---

## Show Notes

```md
Episode 085 — July 13, 2026

[00:00] Episode hook

Apple filed suit against OpenAI on July 10, 2026, alleging former employees stole trade secrets at the direction of OpenAI's senior leadership. OpenAI shipped Codex rust-v0.144.2 on July 13, 2026, a bug-fix release authored by @dylan-hurd-oai as PR #326 that reverted a prompting regression in Guardian, the CLI's automated code-review stage; a follow-up rust-v0.144.3 followed the same day. Nirjhar Das and Md. Al-Mamun Provath's task-specific two-agent system took first place at the QANTA 2026 multimodal quizbowl shared challenge at ICML 2026, scoring 0.402 (arXiv 2607.09623). Yujie Pang and Zudong Li released PAC-ACT (arXiv 2607.09590), a reinforcement-learning post-training framework targeting pretrained Action Chunking Transformer policies. Chongyu Qu, Can Cui, and Zhengyi Lu's SAGEAgent cuts diagnostic burden 55% on glioma survival prediction, while Ahmet Erdem Pamuk, Ömer Yentür, and Ahmet Tunga Bayrak introduced Freya-TTS, a 183.2M-parameter Turkish text-to-speech model.

[02:00] Agent Stack Release Readout: OpenAI Codex rust-v0.144.3, rust-v0.144.2

The paired release landed on July 13, 2026. OpenAI Codex CLI shipped rust-v0.144.2 at 04:39:22Z, followed by rust-v0.144.3 at 06:12:19Z — about 93 minutes apart, both stamped onto the release/0.144 branch and pointing at the same patched tree.

What changed: rust-v0.144.2 reverted a prompting regression in Guardian, Codex's automated code-review stage. Per the release notes, the revert restores three coupled surfaces: Guardian's auto-review policy, the request format it sends, and the tool behavior it relies on. The change lands via PR #32672, authored by @dylan-hurd-oai against release/0.144 and titled 'Revert "Update auto review prompting"'. rust-v0.144.3 is a version-only release — no merged pull requests since v0.144.2, so it republishes the same tree without any additional changelog content.

Why it matters now: Guardian is the review tier most visible to teams running Codex in CI pipelines. When its prompt template shifts, review categories shift with it — comment types you've trained your team to read can disappear or appear without warning, and the diff only surfaces when you compare findings run-to-run. A revert looks like a no-op on paper, but it recalibrates whatever your reviewers have been measuring over the past few weeks.

Two concrete mechanisms. First, the PR is a full rollback rather than a partial patch — the title is literally 'Revert', and the changelog names policy, request format, and tool behavior together, so the post-revert state matches the pre-regression baseline exactly. Second, the release cadence compresses the pair to a single build cycle: the 04:39 and 06:12 timestamps on the same UTC day suggest the build pipeline treats the version-only bump as a chained follow-up rather than a separate feature deploy.

What this means for builders: if you've pinned a Guardian output schema or written assertions against its review comments, pull v0.144.2 and re-run your golden test set — the behavior matches the pre-regression baseline, not whatever shipped briefly between v0.144.1 and v0.144.2. Pipelines that auto-update to new Codex releases will pick this up without any extra config, and the diff going forward is unchanged from the prior baseline behavior your team last observed.

What to watch next: whether OpenAI ships a follow-up that re-documents the prompting model behind Guardian, or whether the team absorbs the reverted change and moves on without a written postmortem.

[03:37] Apple sues OpenAI over alleged trade secret theft by ex-employees

Apple filed suit against OpenAI on July 10, alleging that former Apple employees stole trade secrets before joining the AI lab, with the misconduct directed by OpenAI's senior leadership. The complaint, surfaced through TechCrunch AI and picked up by 9to5Mac, was amplified across Hacker News with a score of 1640 and a discussion thread still active the same day. The filing identifies a longtime former Apple employee who now sits within OpenAI's senior leadership, framing the departures as orchestrated rather than routine job changes.

The legal theory hinges on coordination. Apple claims that recruitment and IP transfer were directed from OpenAI's senior leadership rather than emerging from individual hires acting alone. That framing matters because it converts what could be a series of employment disputes into a single alleged scheme. The involvement of senior leadership, including the named longtime former Apple employee, also raises questions about what those executives knew and when, which could surface through discovery and play out across the active Hacker News thread.

For builders, the case is a reminder that AI talent has become a legal flashpoint. The 1640-score Hacker News thread signals that developers are treating this as more than a routine employment dispute, and the speed of the discussion shows how closely the community tracks movement between major AI organizations. Hiring between competing AI organizations, or onboarding engineers who recently left one, now carries real legal exposure on both sides of the table.

What to watch next: discovery filings that name specific projects or systems allegedly touched by the former employees, and whether OpenAI files a countersuit or motions to dismiss. The Hacker News thread will surface the developer community's reading of each new filing as it drops.

[05:24] Task-Specific Two-Agent System Tops QANTA 2026 at 0.402

arXiv paper 2607.09623, authored by Nirjhar Das and Md. Al-Mamun Provath, lays out their submission to the QANTA 2026 shared challenge, hosted at the ICML 2026 Workshop on Efficient Multimodal Question Answering. The shared task targets multimodal quizbowl systems that must process pyramid-style questions, where clues are incrementally revealed alongside accompanying images, all under realistic efficiency constraints that penalize heavyweight pipelines. Two distinct task formats drive the leaderboard. Tossup questions require the system to choose when to buzz and answer under uncertainty. Bonus questions evaluate exact answer selection and reward human-adoption metrics once the clue category is established.

The paper's headline contribution is a task-specific two-agent architecture that fits inside a hosted-only inference environment and deliberately avoids both a retrieval pipeline and model ensembles. The Tossup agent wraps a GPT-4o-mini-class model, referred to as GPT-4.1-mini in the competition logs, with confidence-calibrated answering plus a domain-specific numeric reasoning policy designed to tamp down overconfident predictions triggered by isolated quantitative clues. The Bonus agent runs a GPT-4o-class model, referred to as GPT-4.1, with leadin-aware reasoning, structured relational reasoning, and multimodal evidence integration, prioritizing exact answer strings.

On the QANTA 2026 leaderboard, the system took the top overall score of 0.402, decomposing into a Tossup score of 0.238 and a Bonus Effect score of 0.164. For builders, this is direct evidence that modest hosted GPT-class models, paired with task-decomposed reasoning policies and explicit confidence calibration, can outperform heavier retrieval or ensembled baselines under matched inference budgets. The follow-on question to watch is whether this two-agent, task-decomposed design pattern carries over to other efficiency-bounded agent benchmarks, since the win demonstrates that small hosted models with explicit calibration can match heavier multi-stage baselines under the same budget.

[07:10] PAC-ACT: Chunk-level RL post-training for Action Chunking Transformer policies

PAC-ACT is a new reinforcement learning post-training framework for pretrained Action Chunking Transformer policies, released on arXiv as paper 2607.09590 by Yujie Pang and Zudong Li. The paper targets precision industrial contact manipulation, where robots must hold reliable policies under pose perturbations and contact-force constraints. Vision-language-action models generalize broadly but carry inference latency and GPU-memory cost that fight real-time industrial control, so the authors anchor on vision-action chunking policies, which are real-time friendly but are typically trained by behavior cloning and degrade under distribution shift in contact-rich tasks.

The mechanism restructures optimization at the chunk level rather than the per-step level, building an ACT-transferred actor-critic architecture on top of a frozen pretrained ACT backbone. A hybrid behavior-prior constraint preserves the pretrained action distribution during online fine-tuning, which keeps online RL exploration anchored to what the base policy already knows how to do.

On industrial precision-contact benchmarks, PAC-ACT improves task success, contact stability, and force safety while retaining the low-latency, low-GPU-memory profile of chunked policies. The headline number from the abstract: on the Contour task, PAC-ACT significantly reduces peak contact force and decreases the proportion of force readings above 60 newtons by 46 times compared to the behavior-cloned baseline. Sparse-reward ablations further show that the behavior-prior constraint enables effective exploration under randomized initial poses, where vanilla RL stalls.

For builders, this is a recipe for tightening force and contact behavior on top of an existing ACT deployment without rewriting the inference stack. The behavior-prior pattern generalizes — any chunked policy that needs post-hoc tightening for contact, precision, or safety margins can adopt the same actor-critic overlay. Watch next: whether the chunk-level actor-critic transfers cleanly to other ACT-style backbones beyond Contour, and whether the behavior-prior recipe lands in open-source RL post-training toolkits for robotics.

[09:00] SAGEAgent Cuts Diagnostic Burden 55% on Glioma Survival Prediction

A new clinical agent paper drops a sequential-decision framework for multimodal survival prediction in glioma. The work comes from Chongyu Qu, Can Cui, and Zhengyi Lu at arXiv 2607.09521, titled SAGEAgent, short for Sequential Acquisition Guided by Experience. The setup is straightforward but useful: a cancer patient's diagnostic workup is an ordered workflow that escalates in clinical burden, from demographics at intake up through genomic profiling that requires specialized tissue analysis. Existing multimodal survival methods either assume every modality is available or handle missing data passively. None of them actively reason about whether acquiring the next modality is actually justified for that specific patient. SAGEAgent formulates modality acquisition as a sequential decision problem. The agent is built as a self-evolving LLM that decides which modality to acquire next for each patient. Three concrete mechanisms carry the architecture. First, clinical tools translate numerical predictions back into text so the LLM can reason over them. Second, an episodic memory retrieves similar past cases to ground each new decision. Third, a semantic memory accumulates reusable decision patterns from accumulated experience. That last piece is what makes the agent self-evolving rather than static. The evaluation combines TCGA-LGG, TCGA-GBM, and BraTS into a glioma cohort with four diagnostic modalities. The headline result: SAGEAgent holds competitive survival prediction accuracy while reducing average acquisition burden by 55 percent compared to using the full modality set. For builder context, the relevant pattern is treating expensive data acquisition as a learned policy rather than a fixed pipeline. The episodic-plus-semantic memory split maps cleanly onto retrieval pipelines you would already build for tool-using agents. Watch next: replication on non-glioma cohorts and how the 55 percent burden reduction holds when the cost model gets recalibrated against real billing and turnaround-time data.

[10:50] Freya-TTS: 183M Flow-Matching DiT Beats Larger Turkish TTS Stacks

Freya-TTS is a compact Turkish-first text-to-speech model from authors Ahmet Erdem Pamuk, Ömer Yentür, and Ahmet Tunga Bayrak, documented in arXiv paper 2607.09530. The work takes a minimalist approach to a usually pipeline-heavy problem: instead of stacking a phonemizer, a grapheme-to-phoneme frontend, and a discrete speech tokenizer, the system models speech end-to-end from a raw 92-symbol Turkish character vocabulary.

The architecture is a 183.2M-parameter non-autoregressive conditional flow-matching Diffusion Transformer, operating inside the frozen continuous latent space of AudioVAE2 — encoded at 16 kHz and decoded to 48 kHz. Because the DiT never touches raw waveforms or discrete tokens, its 183M parameters concentrate on text-to-latent mapping rather than acoustic reconstruction.

Two mechanisms carry most of the lift. First, rule-free end-to-end modeling: the model predicts latents directly from characters, with no phonemizer and no G2P module in the loop. Second, parallel denoising over a predicted duration — the entire latent sequence is generated simultaneously rather than frame-by-frame, which is what makes inference fast. A two-stage post-training recipe adds single-speaker voice locking and short-utterance coverage to harden conversational use.

On the Freya-TR-Eval benchmark, Freya-TTS posts a band-matched word error rate of 8.0% and character error rate of 3.0% — outperforming substantially larger open-source systems at a fraction of their parameter count. It also hits a real-time factor of 0.11 on consumer GPUs and runs faster than real time on a laptop CPU, which makes on-device voice synthesis in Turkish genuinely plausible.

For builders, the takeaway is architectural: a 183M-parameter flow-matching DiT can match or beat much larger TTS stacks when reconstruction is offloaded to a frozen VAE. The open release of weights, training and inference code, and the eval suite gives agent developers a reference point for tokenizer-free, fast speech synthesis. Watch next for replication outside Turkish — the character-only contract is the bet that needs to hold up across other morphologically rich languages.

[12:47] Long-Horizon-Terminal-Bench Probes Multi-Hour Agent Tasks

A new benchmark is trying to expose the gaps in how we measure agent capability on real terminal work. Long-Horizon-Terminal-Bench, from Zilong Li and collaborators, surfaced this week on HuggingFace's daily papers feed and is climbing fast, up thirty-two upvotes at time of recording. The premise is simple and uncomfortable: most terminal benchmarks test agents on short problems that resolve in minutes, grade them only on whether the final answer is correct, and miss everything that happens in between.

Long-Horizon-Terminal-Bench ships forty-six terminal tasks spread across nine categories, built so that no single-shot solution works. The shift that matters is dense reward-based grading: instead of scoring zero or one at the end, the benchmark evaluates intermediate progress and partial solutions, giving credit when an agent moves state forward even if it does not finish. That alone changes what an agent can be trained or fine-tuned against, because the reward signal is no longer sparse and a partly-correct attempt is no longer indistinguishable from a complete failure.

Mechanically, this is a terminal benchmark, so the agent operates against a real shell environment, runs commands, observes output, and accumulates partial credit as the environment state advances. That mirrors how builders actually debug: a partly working build, a partially passing test suite, a build that gets most of the way there. The benchmark is designed to keep grading meaningful across that journey rather than collapsing it to a binary pass or fail.

For builder workflows, the implication is that current short-horizon numbers may overstate agent capability on the multi-hour jobs that actually matter, like staging a release, porting a module, or running a long migration. Watch for follow-up benchmarks that adopt the dense-reward framing on real engineering tasks, and for harness authors to start reporting long-horizon scores alongside their existing evals.

[14:40] Semantic Pareto-DQN Tackles Fraud Collapse Without Resampling

A new arXiv paper, Semantic Pareto-DQN, proposes a multi-objective reinforcement learning approach to one of the hardest problems in production fraud systems: extreme class imbalance that pushes single-objective classifiers into what the authors call fraud collapse, defaulting to the majority class and missing actual anomalies. The paper is authored by Cláudio Lúcio do Val Lopes and Lucca Machado da Silva and is available as arXiv 2607.09641.

The core mechanism replaces scalar rewards with a vectorial reward that decouples three competing objectives: financial efficacy, operational friction, and semantic discovery. Rather than collapsing these into a single weighted sum, the agent maps a continuous Pareto frontier and dynamically navigates the asymmetric cost between missed anomalies and false positives. The state representation is the more novel piece. Heterogeneous transaction features are synthesized into natural-language narratives and then encoded by large language models, producing a scale-invariant state that the authors argue sidesteps the distortive data resampling that traditional imbalanced-learning pipelines rely on.

The headline empirical result is that Semantic Pareto-DQN shatters the zero-recall trap. Evaluated on E-Commerce fraud and UCI Credit datasets, the framework achieves superior minority-class recall against scalarized baselines, trading bounded operational friction for anomaly discovery. The paper frames this as an alternative to resampling, not a replacement for downstream classifiers.

For builders running payment, risk, or transaction pipelines, the implication is that LLM-encoded transaction narratives plus Pareto-frontier optimization can act as a recall recovery layer without synthetic minority oversampling or undersampling of legitimate transactions. Worth watching next: replication on streaming production traffic, the cost profile of running LLM encoding per transaction, and whether the Pareto frontier can be exposed as a tunable policy rather than a research artifact.

[16:24] 4DR360 Couples Detection and Occupancy via State Reasoning

The 4DR360 paper from Xiaokai Bai, Lianqing Zheng, and Runwei Guan, on arXiv 2607.09629, takes a fresh angle on radar-camera fusion for autonomous driving perception. Instead of treating 3D detection and semantic occupancy as separate terminal outputs that decoders produce, the authors reframe occupancy as a persistent scene state that propagates through the network across stages. The result is a cross-modal state reasoning paradigm where detection and occupancy share a common intermediate scene representation rather than competing for the same BEV features.

Two concrete modules drive the architecture. State-guided BEV Enhancement, abbreviated SBE, strengthens intra-frame BEV features by conditioning them on the modeled occupancy state. Doppler-guided Temporal Fusion, or DTF, preserves that state evidence across longer temporal horizons using radar Doppler cues, a natural fit for 4D millimeter-wave radar, which captures velocity alongside sparse spatial returns. Together they give the model coarse-to-fine feature aggregation across both space and time.

The paper also addresses the data bottleneck that has held back radar-camera multi-task work. The authors extend ManTruckScenes with satellite-map-based generated occupancy labels and pair that dataset with OmniHD-Scenes in a unified cross-dataset detection-and-occupancy protocol. Their experiments sweep accuracy, robustness, ablations, and efficiency under one radar-camera multi-task evaluation framework. Code and the new labels are slated for release on acceptance.

For builders, the practical takeaway is twofold. First, persistent-state occupancy modeling offers a way to share compute between detection and dense semantic prediction rather than running two parallel decoders from the same BEV backbone. Second, the unified eval protocol gives perception teams a single yardstick for radar-camera multi-task work instead of stitching together dataset-specific benchmarks.

What to watch next: whether the SBE and DTF modules transfer cleanly to other radar-camera stacks beyond ManTruckScenes and OmniHD-Scenes, and whether the satellite-map-generated occupancy labels hold up across diverse urban and highway regimes.

[18:17] Agora Replaces Agent Router With an Auction for Reasoning Steps

A new paper from Kaiji Zhou, Ales Leonardis, and Yue Feng proposes swapping the function-call router inside a multi-model agent stack for an auction. The work, called Agora, introduces an incentive-compatible auction mechanism that allocates tasks to expert models and tools dynamically. Each reasoning step becomes a tradeable item, and agents bid on it based on their rectified competence. The point is to keep critical logic flowing to the most capable solver rather than the one that just sounds most confident about handling the function call.

Across five benchmarks, Agora improves over matched single-model, routing, and cascade baselines operating from comparable candidate pools. The framework also exposes a controllable cost-quality trade-off through a single auction parameter, which the authors flag as the practical knob for deployment. The motivation is that existing orchestration matches at the level of declared function support and ignores performance variability and cost efficiency between functionally similar alternatives.

For builders running heterogeneous model pools, the shift is the unit of allocation. Most routers decide at the function or tool level; Agora decides at the reasoning-step level and attaches a price to each one. That means the cost-quality frontier becomes tunable per workload rather than locked into a vendor default cascade. The single auction parameter is the lever: push it one way and the stack favors cheap consistent calls, push it the other and expensive specialists absorb the hard reasoning steps.

Next to track: whether the rectified competence signal can be computed cheaply enough to stay in the hot path, and whether any open agent framework ships the auction primitive as a routing backend. The paper is arXiv 2607.09600 from Zhou, Leonardis, and Feng.

[20:01] Counting failures in VLMs traced to readout misalignment, not missing knowledge

A new paper from Ahmed Oumar El-Shangiti, Abzal Nurgazy, and Hilal AlQuabeh at arXiv 2607.09544 puts a microscope on why vision-language models fail at basic counting. The team trained simple probes on internal activations of four VLMs across five counting datasets, and found that nonlinear probes can reliably detect when a model is about to give a wrong count — even though the model often encodes the correct count internally.

The first mechanism is SVCCA, or Singular Vector Canonical Correlation Analysis. Probes trained on ground-truth counts and probes trained on model outputs occupy a partially shared activation subspace, but read out along misaligned directions. In plain terms, the count sits in the model's head, but the answer path is pointing somewhere else entirely.

The second mechanism is a causal steering intervention. Strengthening the direction of count-identified probes measurably improves counting performance, which the authors then validate. From that they propose a detector-guided self-correction loop that selectively re-prompts the model only when an internal error detector predicts failure. It is purely an inference-time intervention — no parameter updates, no fine-tuning — and it lifts counting accuracy by up to 15.6 absolute percentage points across the eval suite.

For builders shipping agents that tally objects in images, this is a research result with immediate production relevance. A lightweight probe trained on activations could act as a reliability gate on counting-heavy steps, catching failures before they cascade into downstream tool calls. It also reframes a class of VLM errors as alignment problems rather than knowledge gaps, opening a new lever for inference-time steering. The same read-probe-then-correct loop could wrap any structured-output call where the model likely has the right internal answer.

Watch next whether the same probe pattern holds for non-counting structured-output tasks like set comparison or threshold reasoning.

[21:52] vLLM 0.25.0 ships Model Runner V2 as default for dense models

vLLM v0.25.0 landed on July 11 as a stable release, packing 558 commits from 232 contributors, 64 of them new to the project. The headline change is that Model Runner V2 is now the default execution path for all dense models, building on the quantized-model support that landed in the previous release. That switch ships behind PR #44443 and makes MRv2 the standard code path for dense serving.

Three concrete mechanisms ride alongside it. First, EVS support lands via #46535, extending the MRv2 path with an additional capability surface. Second, realtime embeddings arrive via #46762, exposing a fresh embedding endpoint for low-latency pipelines running on the same unified runner. Third, prefix caching now covers Mamba hybrid models, which is a notable unlock for anyone self-hosting Mamba-based architectures that previously missed out on prefix-cache reuse.

For builders running local inference behind agent stacks, the practical effect is consolidation. Dense model serving now routes through a single runner with built-in quantization, hybrid prefix caching, and a realtime embedding endpoint on top. If you've been pinning an older vLLM minor because of MRv2 opt-in behavior, this is the release where that pin stops being necessary. RAG pipelines and realtime retrieval workloads get the most direct lift from #46762 and the Mamba hybrid prefix cache, since both depend on reusing computed state across consecutive requests rather than recomputing per call.

The thing to watch next is how MRv2 extends beyond dense coverage. The release notes call out dense models specifically as the new default, so non-dense architectures likely still route through the previous runner. Watch the next minor for broader MRv2 coverage, and benchmark latency on your own model family before flipping a high-traffic production deployment over to the new default.

[23:41] A decade of VLMs closes the simple-to-complex scene gap

A new arXiv paper from researchers Shravan Murlidaran and Miguel P. Eckstein, paper 2607.09654, takes a decade-long look at vision-language model accuracy and error patterns, and the headline is that multimodal large language models have effectively closed the gap between describing simple scenes and complex social behavior scenes. The team introduces a Complex Social Behavior dataset, 100 images depicting complex social interactions, and pairs it with a sample from MS-COCO. They evaluate nine models spanning 2017 to 2025, four pre-MLLM vision-language models and five multimodal LLMs, plus 20 human descriptions scored against a gold standard. The benchmark scores accuracy and breaks performance down into five visual-cognitive error types: object detection, recognition, hallucination, scene understanding, and spatial dependence.

The mechanism is straightforward but useful: a curated complex-image set that exposes where VLMs still differ from humans. Pre-MLLMs scored well below the worst human descriptions on CSB, while MLLMs landed near the top human descriptions on both CSB and MS-COCO, erasing the simpler-versus-complex accuracy gap that used to exist. On the error taxonomy, MLLMs have nearly eliminated object detection, recognition, hallucination, and scene understanding errors on the tested datasets. The remaining gap is spatial dependence: MLLMs occasionally rely on different image regions than humans when generating descriptions.

For builders wiring VLMs into agent pipelines that need to interpret screenshots, diagrams, or workplace photos, this paper offers a concrete measurement of where the visual stack is reliable and where it still diverges from human gaze. CSB-style evaluation is something you can replicate locally against your own domain imagery to surface systematic blind spots before they hit production. The watch-next: how upcoming vision encoders and MLLMs close the spatial dependence gap, and whether attention-region analysis becomes a standard reporting metric alongside scene description accuracy.

[25:30] Training-Free Logit Adaptation Boosts Medical VLMs on OOD Data

Medical Vision-Language Models perform strongly in zero-shot settings, but the same class bias baked in by large-scale pretraining still drags accuracy down on out-of-distribution data, and the existing few-shot fixes typically bolt on extra trainable components that get wobbly in extreme low-data regimes like 1-shot. A new paper from Tianyou Jiang and Ziyu Zhou — TCLA, short for Training-Free Class-wise Logit Adaptation — attacks that gap at inference time. arXiv 2607.09562.

TCLA is a purely training-free, model-agnostic adaptation method that runs on a small support set. The mechanism is straightforward in shape: instead of fine-tuning the VLM's weights, TCLA adjusts the logits the model already emits at inference, sharpening inter-class deconfusion and pulling predictions back toward the medical domain. No new parameters, no fine-tuning loop, no architecture surgery — and the same recipe applies across pretrained Medical VLMs regardless of the backbone.

The headline result, drawn straight from the abstract: across nine datasets spanning X-ray, ultrasound, MRI, CT, and histopathology, TCLA consistently lifts out-of-distribution performance for Medical VLMs, and in most cases outperforms existing training-based adaptation methods. That includes the 1-shot regime where prior approaches tend to destabilize.

For builders shipping clinical or imaging workflows on top of pretrained Medical VLMs, the practical draw is the deployment shape: drop-in inference-time logit correction means OOD robustness can be tuned from a small support set instead of standing up a fine-tuning pipeline. Because TCLA is model-agnostic, a single adaptation wrapper could move between backbones as the underlying VLM is swapped.

Watch next: the abstract claims wins over training-based methods across most cases, so the open question is how those gains hold up when the support set drifts further from the evaluation distribution — and whether the inference-time overhead stays flat at production scale.

[27:20] Practical queue

From today's stories: If your team pins a Guardian review output schema or runs golden tests against its auto-review comments, pull Codex rust-v0.144.2 to realign with the behavior your assertions were originally written against. This case signals that AI labs are willing to pursue coordinated theft claims against competitors, not just individual departures. For builders running hosted agents, this is evidence that decomposing a task into separately-tuned roles and applying explicit confidence calibration can outperform larger single-model or ensembled setups under a fixed inference budget. PAC-ACT turns a pretrained ACT policy into a target for online RL without rewriting the inference stack, which matters for builders already running chunked policies on real-time industrial cells. For builders working on tool-using agents, the relevant pattern is treating expensive data acquisition as a learned policy rather than a fixed pipeline. What this means for builders: Freya-TTS shows a tokenizer-free, phoneme-free recipe that holds its benchmark performance while collapsing the usual TTS frontend, which simplifies voice synthesis integration at the architecture level. Current short-horizon agent eval numbers likely overstate capability on the multi-hour engineering jobs that matter in real workflows. For teams operating payment or risk pipelines, this signals LLM-encoded transaction narratives plus Pareto-frontier RL as a recall-recovery layer that avoids synthetic minority oversampling. What this means for builders: the framework gives perception teams a shared intermediate representation between detection and dense semantic prediction, plus a unified eval yardstick for radar-camera multi-task work instead of stitched-together dataset-specific benchmarks. Builder takeaway: the unit of allocation moves from the function or tool call to the reasoning step, with a price attached. A lightweight probe trained on VLM activations can act as a reliability gate before counting-heavy steps, catching failures before they cascade into downstream tool calls. Local inference deployments pinning an older vLLM minor for MRv2 opt-in behavior can now upgrade, since the unified runner is the default for dense models. Builders wiring VLMs into agent pipelines that interpret screenshots, diagrams, or workplace photos get a concrete yardstick for where the visual stack matches humans and where it still diverges. For teams building clinical or imaging workflows on top of pretrained Medical VLMs, TCLA offers a way to harden OOD robustness without standing up a fine-tuning pipeline.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: OpenAI Codex rust-v0.144.3, rust-v0.144.2 / Apple sues OpenAI over alleged trade secret theft by ex-employees / Task-Specific Two-Agent System Tops QANTA 2026 at 0.402
- 02:00 — Agent Stack Release Readout: OpenAI Codex rust-v0.144.3, rust-v0.144.2
- 03:37 — Apple sues OpenAI over alleged trade secret theft by ex-employees
- 05:24 — Task-Specific Two-Agent System Tops QANTA 2026 at 0.402
- 07:10 — PAC-ACT: Chunk-level RL post-training for Action Chunking Transformer policies
- 09:00 — SAGEAgent Cuts Diagnostic Burden 55% on Glioma Survival Prediction
- 10:50 — Freya-TTS: 183M Flow-Matching DiT Beats Larger Turkish TTS Stacks
- 12:47 — Long-Horizon-Terminal-Bench Probes Multi-Hour Agent Tasks
- 14:40 — Semantic Pareto-DQN Tackles Fraud Collapse Without Resampling
- 16:24 — 4DR360 Couples Detection and Occupancy via State Reasoning
- 18:17 — Agora Replaces Agent Router With an Auction for Reasoning Steps
- 20:01 — Counting failures in VLMs traced to readout misalignment, not missing knowledge
- 21:52 — vLLM 0.25.0 ships Model Runner V2 as default for dense models
- 23:41 — A decade of VLMs closes the simple-to-complex scene gap
- 25:30 — Training-Free Logit Adaptation Boosts Medical VLMs on OOD Data
- 27:20 — Practical queue

---

## Primary Links

- OpenAI Codex rust-v0.144.3 release: https://github.com/openai/codex/releases/tag/rust-v0.144.3
- OpenAI Codex rust-v0.144.2 release: https://github.com/openai/codex/releases/tag/rust-v0.144.2
- Apple sues OpenAI, accuses ex-employees of stealing trade secrets: https://9to5mac.com/2026/07/10/apple-sues-openai-trade-secret-theft/
- Task-Specific Multimodal Question Answering Agents via Confidence Cali: https://arxiv.org/abs/2607.09623
- PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers: https://arxiv.org/abs/2607.09590
- SAGEAgent: A Self-Evolving Agent for Cost-Aware Modality Acquisition i: https://arxiv.org/abs/2607.09521
- FreyaTTS Technical Report: https://arxiv.org/abs/2607.09530
- Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Hori: https://zli12321.github.io/LHTB/index.html
- Semantic Pareto-DQN: A Multi-Objective Reinforcement Learning Framewor: https://arxiv.org/abs/2607.09641
- 4DR360: State Reasoning for Joint 3D Detection and Occupancy Predictio: https://arxiv.org/abs/2607.09629
- Agora: Enhancing LLM Agent Reasoning Via Auction-Based Task Allocation: https://arxiv.org/abs/2607.09600
- The Count Is There, but Misaligned: Understanding and Correcting Count: https://arxiv.org/abs/2607.09544
- vllm-project/vllm ships v0.25.0: https://github.com/vllm-project/vllm/releases/tag/v0.25.0
- Evolution of Accuracy and Visual-Cognitive Errors in a Decade of Visio: https://arxiv.org/abs/2607.09654
- TCLA: Training-Free Class-wise Logit Adaptation for Medical Vision-Lan: https://arxiv.org/abs/2607.09562
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- microsoft/mcp-for-beginners repo: https://github.com/microsoft/mcp-for-beginners
- TSAI-MetaFraud: A Benchmark Dataset for Financial Fraud Transaction an: https://arxiv.org/abs/2607.09528
- Failure as a Process: An Anatomy of CLI Coding Agent Trajectories: https://arxiv.org/abs/2607.09510
- Beyond Fixed Representations: The Vocabulary and Verifier Gaps in Open: https://arxiv.org/abs/2607.09560
- Ollama v0.31.2: https://github.com/ollama/ollama/releases/tag/v0.31.2

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.11`, published 2026-06-30T16:06:39Z. Recent episode version tags detected: `v2026.6.8-beta.2`, `v2026.6.9`, `v2026.7.1-beta.1`, `v2026.7.1-beta.2`. No new stable release this cycle.
- **Hermes Agent** — Latest stable verified: `v2026.7.7.2`, published 2026-07-08T03:11:22Z. Recent episode version tags detected: `v2026.6.5`, `v2026.7.1`, `v2026.7.7`, `v2026.7.7.2`. No new stable release this cycle.
- **OpenAI Codex** — Latest stable verified: `rust-v0.144.3`, published 2026-07-13T06:12:19Z. Recent episode version tags detected: `rust-v0.142.5`, `rust-v0.143.0`, `rust-v0.144.0`, `rust-v0.144.1`. Selected missing version(s): `rust-v0.144.3`, `rust-v0.144.2`.
- **Claude Code CLI** — Latest stable verified: `2.1.197`, published 2026-06-30T13:31:18.806Z. Recent episode version tags detected: `2.1.195`, `2.1.197`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-07-13). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.11` (stable) / `v2026.7.1-beta.6` (prerelease)
- **Hermes Agent** — `v2026.7.7.2`
- **OpenAI Codex** — `rust-v0.144.3`
- **Claude Code CLI** — `2.1.197`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
