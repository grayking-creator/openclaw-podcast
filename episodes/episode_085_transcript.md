# AgentStack Daily EP085 — Codex rust .144 Point Three, vLLM .25, and Apple Sues OpenAI

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: OpenAI shipped rust .144 point two and rust .144 point three for the terminal-based coding agent Codex. The paired release reverted a Guardian prompting regression, restored its automated-review policy, repaired the request shape sent into review, and returned the associated tool behavior to the earlier baseline.

[ALLOY]: Today: Codex restores Guardian’s prior review contract, Apple alleges that OpenAI recruited employees to obtain trade secrets, and vLLM .25 makes Model Runner V2 the default for dense-model serving. You’ll hear how two specialized agents won QANTA, how chunk-level reinforcement learning reduced unsafe robot contact, and how a clinical agent cut diagnostic burden by fifty-five percent.

[NOVA]: Freya-TTS brings fast Turkish speech synthesis to a compact flow-matching transformer. Long-horizon terminal work gets denser evaluation, Agora auctions individual reasoning steps among models, and vision research separates missing knowledge from faulty readout.

[ALLOY]: The wider stack includes fraud detection without resampling, shared radar-camera scene state, medical logit adaptation, three MCP projects, and Ollama .31 point two with broader local inference support. Research into virtual-economy fraud, coding-agent failure trajectories, and open-ended representations rounds out the queue.

[PAUSE]

## [02:00] Agent Stack Release Readout: OpenAI Codex rust .144 Point Three and Point Two

[NOVA]: OpenAI released rust .144 point two for the terminal-based coding agent Codex, then followed about ninety-three minutes later with rust .144 point three. The functional correction arrived in point two: a full rollback of an earlier Guardian prompting update. Guardian is Codex’s automated code-review stage, and the revert restores three connected surfaces—the policy that guides the review, the request shape passed into it, and the tool behavior used while inspecting a change. Teams running Guardian in continuous integration therefore receive a coordinated return to the earlier contract, not a prompt tweak that leaves surrounding behavior out of sync.

[ALLOY]: Guardian findings often feed review dashboards, merge controls, severity filters, and workflows that distinguish correctness issues from style or maintainability comments. A prompting regression can change which categories appear even when the source change and repository config remain identical. The rollback returns those findings to the distribution teams observed before the regression. That matters when automated controls consume Guardian output rather than treating it as informal prose.

[NOVA]: Point three followed from the same release branch and republishes the patched tree without another Guardian change. The two tags belong to one compressed correction cycle rather than separate feature releases. There is no second review policy, new schema, or additional tool contract layered onto the rollback. The later build carries the same functional correction forward.

[ALLOY]: In practice, Codex installations consuming the newer stable build regain Guardian’s prior automated-review behavior. Integrations that classify comments by category, severity, or expected phrasing may see their earlier patterns return. The release stays narrowly centered on review prompting and its coupled request and tool surfaces; it does not redesign Codex review as a whole. The next consequential change would be a revised Guardian policy with an explicit behavioral contract, especially if OpenAI again adjusts how the reviewer selects findings or invokes tools.

[PAUSE]

## [03:37] Apple Sues OpenAI Over Alleged Trade Secret Theft by Ex-Employees

[NOVA]: Apple filed suit against OpenAI on July tenth, alleging that former Apple employees took trade secrets before joining the AI company. The complaint does not frame the departures as unrelated actions by individual hires. Apple alleges coordination from OpenAI’s senior leadership and points to a longtime former Apple employee who now occupies a senior role there. These are allegations, and OpenAI can challenge both the facts and Apple’s legal theory.

[ALLOY]: Coordination changes the scope of the dispute. If the case reaches discovery, Apple can seek communications concerning recruitment, project assignments, access controls, and what executives understood about the employees’ prior work. OpenAI can dispute whether the claimed material qualifies as a protected trade secret, whether anyone transferred it, and whether any leader directed its use. General expertise carried between jobs is legally different from proprietary technical material.

[NOVA]: The technical consequences depend on what Apple identifies with specificity. Later filings could connect the claims to model techniques, training workflows, product capabilities, hardware systems, or internal research programs. They could also remain centered on employment conduct and confidentiality. Nothing in the filing alone proves that protected material entered an OpenAI model, API, or deployed service, regardless of the intense public discussion around the suit.

[ALLOY]: AI labs recruit from a small pool of engineers whose careers cross major competitors, so onboarding controls now sit beside model and product governance. A clean intake process must separate an employee’s accumulated skill from prior-employer material, particularly when the new role closely resembles earlier work. OpenAI’s formal response, any motion to dismiss, and disputes over how precisely Apple must identify the alleged secrets will determine whether the case reaches a named AI capability or stays a broader fight over talent, confidentiality, and executive coordination.

[PAUSE]

## [05:24] Task-Specific Two-Agent System Tops QANTA 2026 at 0.402

[NOVA]: Nirjhar Das and Md. Al-Mamun Provath took first place in the QANTA 2026 multimodal quizbowl challenge with a task-specific two-agent system scoring point four zero two. QANTA reveals pyramid-style clues incrementally and combines text with images. Tossup questions require deciding when confidence is high enough to buzz, while bonus questions emphasize exact answers after the category becomes clearer. Efficiency constraints prevent teams from hiding weak decision policies behind unlimited retrieval or large ensembles.

[ALLOY]: The winning stack uses neither a retrieval pipeline nor a model ensemble. A smaller hosted model handles tossups with confidence-calibrated answering and a numeric-reasoning policy. That policy suppresses premature confidence when one quantitative clue sounds distinctive but does not uniquely identify the answer. The agent controls both answer quality and timing, treating an early buzz as an action under uncertainty rather than ordinary text generation.

[NOVA]: A larger hosted model handles bonuses with lead-in awareness, relational reasoning, and multimodal evidence integration. Role separation lets the bonus agent optimize exact answer strings without carrying the tossup agent’s timing policy. The combined score includes point two three eight from tossups and a point one six four bonus effect.

[ALLOY]: The result shows that explicit task decomposition can outperform a heavier general pipeline under a matched inference budget. A compact model can own frequent decisions when it has calibrated stopping and action policies, while a stronger model handles the smaller set of steps requiring richer synthesis. Support triage, incident escalation, and tool execution can use the same arrangement: one agent judges whether evidence is sufficient, then another resolves the narrowed task. Distinct objectives produced the gain, not simply adding a second model.

[PAUSE]

## [07:10] PAC-ACT: Chunk-Level RL Post-Training for Action Chunking Transformer Policies

[NOVA]: PAC-ACT applies reinforcement-learning post-training to pretrained Action Chunking Transformer policies. Yujie Pang and Zudong Li target industrial contact tasks where a robot must operate in real time, tolerate pose variation, and avoid unsafe forces. Vision-language-action systems can generalize broadly, but their latency and GPU demands can conflict with tight control loops. ACT policies execute more efficiently, though behavior cloning becomes brittle when contact conditions depart from demonstrations.

[ALLOY]: PAC-ACT optimizes complete action chunks instead of treating every control step independently. An actor-critic layer sits on a frozen pretrained ACT backbone, preserving the original deployment path. A hybrid behavior-prior constraint keeps online exploration near actions the controller already considers plausible. Reinforcement learning can search for safer contact behavior without discarding the motion patterns acquired through imitation.

[NOVA]: On precision-contact benchmarks, the method improves success, contact stability, and force safety. In the Contour task, it reduced the proportion of force readings above sixty newtons by a factor of forty-six compared with the behavior-cloned baseline. Sparse-reward experiments also produced useful exploration from randomized initial poses, where ordinary reinforcement learning stalled. Chunk-level rewards connect an entire contact maneuver with its final force and completion outcome.

[ALLOY]: Robotics teams can add the post-training layer to an existing ACT controller without replacing the low-latency inference stack. Chunk rewards naturally express completing an insertion, maintaining contact, or staying below a force threshold. The behavior prior keeps the updated controller tied to demonstrated motion while permitting targeted improvement. Transfer to other ACT backbones, sensors, and physical tasks still needs confirmation, but PAC-ACT offers a concrete bridge between fast imitation policies and online optimization for precision and safety.

[PAUSE]

## [09:00] SAGEAgent Cuts Diagnostic Burden 55% on Glioma Survival Prediction

[NOVA]: SAGEAgent treats diagnostic acquisition for glioma survival prediction as a sequential decision. Chongyu Qu, Can Cui, and Zhengyi Lu model a clinical workflow that can escalate from demographics and imaging to more burdensome genomic analysis. Instead of assuming every modality is present, the agent decides whether another source of evidence is justified for the individual patient.

[ALLOY]: Three components guide that choice. Clinical tools translate numerical predictions into language the reasoning model can use. Episodic memory retrieves similar past patients. Semantic memory retains reusable acquisition policies learned across prior cases. Structured predictors can therefore feed an agent without requiring the language model to interpret raw clinical scores unaided, while the two memory layers separate case similarity from broader decision experience.

[NOVA]: Evaluation combines glioma cohorts from TCGA and BraTS across four modalities. SAGEAgent maintained competitive survival-prediction accuracy while reducing average acquisition burden by fifty-five percent compared with consuming the complete modality set. The agent receives an explicit stopping decision, tying predictive quality to the cost of obtaining more evidence.

[ALLOY]: The design also applies where an agent must decide whether another assay, scan, specialist step, or expensive API call will improve the result enough to justify its cost. Healthcare burden is not one universal scalar: delay, billing, invasiveness, and availability differ across patients and institutions. Replication on other cancers and prospective clinical workflows will show whether the reported reduction survives real cost models and safety constraints. The important capability is learned evidence acquisition rather than passive handling of missing inputs.

[PAUSE]

## [10:50] Freya-TTS: 183M Flow-Matching DiT Beats Larger Turkish TTS Stacks

[NOVA]: Freya-TTS is a Turkish-first speech model with roughly one hundred eighty-three million parameters. Ahmet Erdem Pamuk, Ömer Yentür, and Ahmet Tunga Bayrak remove the phonemizer, grapheme-to-phoneme frontend, and discrete speech tokenizer commonly found in speech stacks. Freya accepts a raw ninety-two-symbol Turkish character vocabulary and generates speech through a non-autoregressive conditional flow-matching Diffusion Transformer.

[ALLOY]: The transformer operates inside the frozen continuous latent space of AudioVAE2. Speech is encoded at sixteen kilohertz and reconstructed at forty-eight kilohertz, leaving Freya’s trainable capacity focused on mapping text into acoustic latents. Parallel denoising generates the latent sequence together rather than emitting frames one at a time. A second post-training phase strengthens single-speaker identity and short conversational utterances.

[NOVA]: On Freya-TR-Eval, the model reports an eight-percent word error rate and a three-percent character error rate, outperforming larger open Turkish speech systems in the authors’ comparison. It reaches a real-time factor of point one one on consumer GPUs and runs faster than real time on a laptop CPU. That makes local Turkish synthesis plausible for voice agents that cannot depend on a remote speech service.

[ALLOY]: The release provides weights, training and inference code, and the evaluation setup. Its compact size comes partly from delegating acoustic reconstruction to the frozen VAE instead of asking the transformer to learn every waveform layer. Character-only input also removes several separately maintained language components. Transfer beyond Turkish remains the larger question, because pronunciation and normalization demands vary across morphologically rich languages. For Turkish deployments, Freya combines modest compute, low latency, and competitive intelligibility in an openly available stack.

[PAUSE]

## [12:47] Long-Horizon-Terminal-Bench Probes Multi-Hour Agent Tasks

[NOVA]: Long-Horizon-Terminal-Bench evaluates agents on forty-six terminal tasks across nine categories, with work designed to require sustained interaction rather than one-shot answers. Zilong Li and collaborators target sessions where an agent must inspect state, execute commands, interpret results, revise its approach, and preserve progress across many turns. A strong initial answer has little value if the agent cannot continue long enough to produce a working result.

[ALLOY]: Dense reward-based grading distinguishes the benchmark from pass-or-fail suites. Intermediate state changes and partial solutions can earn credit even when the final goal remains incomplete. Evaluators can see whether an agent advanced steadily, plateaued, or damaged useful progress late in the trajectory. Dense rewards also provide a richer training signal than assigning the same zero to every unfinished attempt.

[NOVA]: Operating against a real shell makes delayed consequences visible. A locally reasonable action can create trouble many steps later, pressuring context management, planning, and recovery. The benchmark can separate an agent that advances from one that narrates plausible progress while repeatedly returning to the same dead end. It also reveals whether environmental feedback causes a meaningful change in strategy.

[ALLOY]: Terminal-based coding agents need more than high completion rates on brief tasks. Multi-hour work requires maintaining assumptions, detecting state changes, and recovering before an early error compounds. Dense scoring can identify intermediate milestones that predict eventual success and compare partially useful trajectories. In production, an agent that consistently reaches a recoverable near-complete state may deliver more value than one that occasionally finishes but often destroys progress near the end.

[PAUSE]

## [14:40] Semantic Pareto-DQN Tackles Fraud Collapse Without Resampling

[NOVA]: Semantic Pareto-DQN targets fraud collapse, where severe class imbalance pushes a detector toward labeling nearly every transaction as legitimate. Cláudio Lúcio do Val Lopes and Lucca Machado da Silva replace a single scalar objective with a reward vector spanning financial efficiency, operational friction, and semantic discovery. The agent can navigate visible trade-offs instead of hiding them inside one fixed weighted score.

[ALLOY]: Transaction features become natural-language narratives that a language model encodes. Those representations capture relationships among timing, behavior, and transaction context that raw columns may express poorly. A Pareto-oriented deep Q-network then searches for policies balancing missed fraud against false-positive burden without oversampling or undersampling. Training remains closer to the actual transaction stream rather than manufacturing a convenient class distribution.

[NOVA]: Tests on e-commerce and credit-card data show the approach escaping the zero-recall trap while keeping operational friction bounded. High overall accuracy can otherwise conceal a detector that ignores nearly all fraud. Flagging everything is not viable either, because analyst queues and customer interruptions quickly become unmanageable. Pareto optimization exposes several workable operating points rather than presenting one threshold as universally correct.

[ALLOY]: Payment teams can configure different points for different markets, loss levels, or review capacity. A high-risk period may favor recall, while a lower-risk flow may prioritize customer experience. Semantic encoding introduces serving cost and may drift as transaction behavior changes, so latency and stability need independent measurement. Even with those constraints, the method provides a useful way to build fraud policies around competing business outcomes while preserving the original class imbalance.

[PAUSE]

## [16:24] 4DR360 Couples Detection and Occupancy via State Reasoning

[NOVA]: 4DR360 combines radar-camera object detection and semantic occupancy through a shared scene state. Xiaokai Bai, Lianqing Zheng, Runwei Guan, and collaborators avoid isolated decoders that compete for the same sensor features. Detection and occupancy update one common representation, allowing each task to improve the state consumed by the other. A planner can then use one evolving view of the environment.

[ALLOY]: State-guided bird’s-eye-view enhancement feeds occupancy information back into detection features. Doppler-guided temporal fusion uses velocity cues from four-dimensional millimeter-wave radar to maintain scene state across time. Radar contributes distance and motion information in darkness, glare, rain, or partial occlusion, while cameras supply visual detail that radar cannot resolve. Fusion becomes repeated state refinement rather than one concatenation step.

[NOVA]: The authors add occupancy supervision derived from satellite maps, expanding training coverage where dense three-dimensional labels are expensive. Reported results show joint gains in detection and occupancy, suggesting that the shared state does more than reduce duplicated computation. Evidence from one objective can correct the representation used by the other.

[ALLOY]: A unified state can simplify autonomous perception by reducing separate decoding paths and presenting one temporal world representation to planning. Map-derived supervision may become stale around construction or changing streets, and weak radar calibration can carry incorrect motion cues forward. Those constraints require careful deployment handling. Still, 4DR360 offers a concrete integration pattern: wire detection, occupancy, and sensor history around a continuously updated scene state instead of reconciling disconnected outputs after inference.

[PAUSE]

## [18:17] Agora Replaces Agent Router With an Auction for Reasoning Steps

[NOVA]: Agora replaces a conventional multi-model router with an auction over individual reasoning steps. Kaiji Zhou, Ales Leonardis, and Yue Feng let candidate models bid according to rectified competence. Allocation depends on estimated ability for the current step rather than one label attached to an entire request. A session can therefore switch models between planning, calculation, tool selection, and verification.

[ALLOY]: Traditional routers often choose one model at the beginning or escalate through a fixed cascade. Agora can keep inexpensive specialists on routine work and award a difficult step to a stronger bidder without transferring the whole task. One auction parameter controls the cost-quality balance. Rectified competence also reduces the advantage of a model that systematically overstates confidence.

[NOVA]: The authors report improvements over routing and cascade baselines across five benchmarks. A model that performs well on retrieval planning can lose the auction for mathematical verification, while another wins only the steps matching its measured skill. That differs from broad request classification, where one early routing choice governs the complete session even as the reasoning demands change.

[ALLOY]: Heterogeneous stacks can auction tool decisions or verification calls across local and hosted models with different prices, latencies, and strengths. The design adds overhead because the system must estimate competence, allocate the step, and transfer enough context for the winner to act. Savings disappear if bidding costs more than the reasoning being assigned. Agora becomes most useful when competence estimates update from observed results, context transfer stays compact, and auction latency remains low.

[PAUSE]

## [20:01] Counting Failures in VLMs Traced to Readout Misalignment, Not Missing Knowledge

[NOVA]: Research across four vision-language models and five counting datasets finds that many wrong counts occur even when the correct quantity is represented internally. Probes trained on intermediate activations predicted upcoming errors and often recovered the right number. Perception had encoded useful information, but the generation path selected an answer misaligned with that representation.

[ALLOY]: The researchers used singular-vector canonical correlation analysis to compare the direction associated with the correct-count probe against the direction driving the emitted answer. They then steered activations toward the probe direction. Counting accuracy improved, supporting a causal relationship rather than a probe that merely correlated with successful examples. The intervention changes readout without replacing the visual encoder.

[NOVA]: A detector-guided self-correction loop turns the analysis into an inference workflow. The detector estimates whether a count is likely wrong, and uncertain outputs receive another reasoning pass. No parameter update is required, and the paper reports gains above fifteen percentage points in some settings. A vision agent could apply that gate before inserting a count into an inventory payload or robotic action.

[ALLOY]: The findings do not imply that every visual error is a readout problem; some scenes genuinely fail to produce a recoverable internal representation. They do show why final accuracy cannot reveal what a model already knows. Similar probes may help with spatial relations, attribute binding, and structured extraction when useful information exists internally but is decoded poorly. Cross-domain transfer remains difficult, because a narrow probe can become another specialized component that needs calibration.

[PAUSE]

## [21:52] vLLM .25 Ships Model Runner V2 as Default for Dense Models

[NOVA]: vLLM .25 makes Model Runner V2 the default execution path for dense models. The release consolidates standard dense-model serving around the newer runner and expands its quantized execution support. More than five hundred commits from over two hundred contributors landed across model compatibility, serving behavior, and performance. Common dense architectures now use one primary runner rather than requiring separate configuration for older and newer paths.

[ALLOY]: A realtime embedding endpoint adds low-latency representation workloads beside generation. Agents that retrieve context continuously, classify incoming events, or update semantic indexes during a live session can request embeddings through the same vLLM service. That can replace a separate embedding deployment with its own transport, authentication, batching, and capacity plan while retaining workload-specific scheduling.

[NOVA]: Prefix caching now reaches Mamba hybrid models, allowing repeated context to reuse prior computation in architectures combining state-space and transformer components. Long system prompts, shared tool schemas, and recurring retrieval context benefit most. Together, embedding service consolidation, prefix reuse, and broader runner support target recurring serving costs in agent workloads.

[ALLOY]: Model Runner V2 becomes the standard specifically for dense architectures; other families can retain different paths. Custom kernels, uncommon quantization formats, and hybrid designs may still expose compatibility differences. The release gives extension authors one primary dense-model integration surface and gives operators a simpler route for mixed generation and embedding traffic. Independent measurements across popular GPUs will show how much the consolidation improves throughput and latency under real concurrent workloads.

[PAUSE]

## [23:41] A Decade of VLMs Closes the Simple-to-Complex Scene Gap

[NOVA]: Shravan Murlidaran and Miguel P. Eckstein compared nine vision-language systems spanning roughly eight years on a Complex Social Behavior dataset. Older models lost substantial accuracy when scenes shifted from simple objects to intricate human interactions. Recent multimodal language models produced descriptions approaching the strongest human references, narrowing a gap that persisted through earlier generations.

[ALLOY]: The study’s error taxonomy shows sharp reductions in object detection, recognition, and general scene-understanding mistakes. Current models omit fewer important participants and relationships. Complex behavior no longer creates the same drop from simple-scene performance, expanding workflows that can begin with a general multimodal model instead of a separate classifier for every interaction.

[NOVA]: Spatial dependence remains different from human perception. Models can produce an accurate description while relying on image regions that do not match those used by people. A small scene alteration may therefore disturb the model even when a human would consider the changed region irrelevant. Correct language does not guarantee a stable or human-like visual basis.

[ALLOY]: Vision agents can extract higher-level situational meaning from scenes that once needed extensive scaffolding, but consequential deployments still require controlled perturbations and domain validation. Attention-region analysis can reveal whether an answer comes from stable evidence or a shortcut. The decade-long comparison shows that generated descriptions may converge with human performance before the underlying visual dependencies do, so answer scoring alone remains incomplete.

[PAUSE]

## [25:30] Training-Free Logit Adaptation Boosts Medical VLMs on OOD Data

[NOVA]: Training-Free Class-wise Logit Adaptation, or TCLA, improves medical vision-language models when incoming images differ from their pretraining distribution. Tianyou Jiang and Ziyu Zhou use a small support set to correct class-level output bias during inference. The method changes neither model weights nor architecture, allowing an adaptation layer to wrap a deployed backbone without a new fine-tuning cycle for every scanner or clinic.

[ALLOY]: Support examples from a local imaging environment reveal how confidence is skewed across classes. TCLA adjusts those logits before the final selection. That is useful in one-shot and low-data settings where parameter updates can overfit. The base encoder and serving path remain intact while the wrapper changes the decision surface for a particular deployment population.

[NOVA]: Across nine medical datasets covering X-rays, MRI, and CT images, the method consistently improved performance and often exceeded more complex adaptation approaches that require training. The same wrapper can sit around different backbones, allowing teams to compare medical VLMs while retaining one local correction layer.

[ALLOY]: A hospital could maintain small support sets for different scanners or imaging populations and configure the correction during serving. That does not remove the need for clinical validation. Class-wise adjustment cannot recover visual evidence the encoder never captured, and future drift may exceed what the support examples represent. TCLA is most useful as a modular response to predictable output bias, with prospective evaluation still needed for calibration, rare conditions, and changing equipment.

[PAUSE]

## [27:12] GitHub Project Radar: DeusData Codebase Memory MCP

[NOVA]: DeusData’s codebase-memory-mcp builds a persistent knowledge graph from a codebase and exposes it through Model Context Protocol. The point-nine release supports one hundred fifty-eight languages, ships as a single static binary, and reports sub-millisecond graph queries. Instead of rescanning source for every cross-component question, an agent queries indexed relationships among symbols, dependencies, call sites, and implementations.

[ALLOY]: OpenClaw, Codex, the terminal-based AI coding agent Claude Code, or Hermes can use the MCP service when a refactor spans several packages. Teams can wire the graph as the primary retrieval surface, then fetch only the narrow source context needed for implementation. The claimed ninety-nine-percent token reduction will vary by codebase and query, but persistent relationships can sharply reduce repeated ingestion during long coding sessions.

[PAUSE]

## [28:05] GitHub Project Radar: Prefect FastMCP

[NOVA]: Prefect’s FastMCP is a Python framework for building MCP servers and clients without manually implementing every protocol surface. Its three-point-four line wraps tool declarations, transports, schemas, and authentication in Python-oriented APIs. An internal service can participate in the same tool envelope as other MCP integrations without a bespoke adapter for every agent host.

[ALLOY]: A team can place FastMCP in front of telemetry, deployment controls, or an internal REST API, then let multiple agents use one shared contract. It fits Python-heavy stacks that want direct control over tool logic while delegating protocol transport and schema exposure to a maintained framework. One authenticated server can support Codex, Hermes, and other MCP-capable sessions through the same integration.

[PAUSE]

## [28:52] GitHub Project Radar: Microsoft MCP for Beginners

[NOVA]: Microsoft’s mcp-for-beginners teaches Model Context Protocol through .NET, Java, TypeScript, JavaScript, Rust, and Python examples. The labs cover servers, clients, message envelopes, modular tools, and security. Mixed-language teams get a shared protocol reference without assuming that every integration lives in Python.

[ALLOY]: Engineers building a Rust client, a .NET service, and a TypeScript host can compare equivalent flows while retaining native conventions. That helps align tool schemas, authentication, and session behavior before internal capabilities reach production agents. The project is especially useful where Python owns model experimentation but Java, Rust, or .NET owns the APIs and services that agents ultimately invoke.

[PAUSE]

## [29:35] Model Discovery Check

[NOVA]: Context limits, token pricing, tool calling, provider availability, and response latency remain the concrete surfaces that determine whether a hosted model can replace an existing deployment without forcing changes across the surrounding agent contract.

[PAUSE]

## [29:42] Local LLM Spotlight: Ollama .31 Point Two

[ALLOY]: Ollama .31 point two enables flash attention on older NVIDIA GPUs with compute capability six.x and lets integrated GPUs offload padded vision models according to available memory. It also hardens GGUF model creation, repairs structured output for thinking models when thinking is disabled, and fixes loading from model locations containing non-UTF-eight characters.

[NOVA]: Ollama launch now disables telemetry by default when starting the terminal-based AI coding agent Claude Code. Padded vision models such as LLaVA gain a more practical route onto older hardware: flash attention reduces execution overhead, while iGPU offload uses shared memory to fit the model. The release combines broader hardware coverage with cleaner structured responses and a quieter local Claude Code launch path.

[PAUSE]

## [30:47] Extra Research Candidate: TSAI-MetaFraud

[ALLOY]: TSAI-MetaFraud introduces a multimodal, multi-task graph benchmark for fraud in virtual economies. It combines behavioral events, transactions, and graph relationships, then evaluates transaction fraud, cross-modal node classification, temporal link prediction, and weakly supervised detection. Graph-neural-network baselines let teams compare systems that connect suspicious payments with account behavior and social structure rather than scoring each transaction alone.

[PAUSE]

## [31:35] Extra Research Candidate: Failure as a Process

[NOVA]: Failure as a Process analyzes one thousand seven hundred ninety-four manually annotated trajectories from OpenHands, MiniSWE, and Terminus2 on Terminal-Bench. It separates failure into onset, evolution, and recovery. Fourteen findings show many epistemic errors beginning within the first few steps, while failures exposed late are frequently unrecoverable. The framework helps distinguish an early false assumption from the later actions it contaminates.

[PAUSE]

## [32:22] Extra Research Candidate: Beyond Fixed Representations

[ALLOY]: Beyond Fixed Representations describes a vocabulary gap, where a system must invent and stabilize a new representational primitive, and a verifier gap, where that primitive’s value appears only after later reuse. Coding, theorem proving, and long-horizon research all encounter this tension. Durable memory for emerging abstractions and delayed evaluation may matter as much as improving immediate next-step generation.

[PAUSE]

## [33:12] Practical Queue

[NOVA]: Codex restores Guardian’s earlier review behavior, while Apple’s suit places hiring provenance and trade-secret controls beside model and product governance.

[ALLOY]: QANTA, Agora, and Long-Horizon-Terminal-Bench specialize agents by objective, allocate steps by competence, and measure sustained progress.

[NOVA]: PAC-ACT, SAGEAgent, Semantic Pareto-DQN, and TCLA adapt deployed systems through constrained post-training, selective evidence acquisition, multi-objective control, and inference-time correction.

[ALLOY]: Freya-TTS, 4DR360, vLLM, Ollama, and the MCP projects expand local speech, shared scene state, model serving, hardware coverage, and reusable tool integration.

[PAUSE]

[NOVA]: For the research papers, releases, repositories, and supporting details, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.
