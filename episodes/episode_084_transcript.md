# AgentStack Daily EP084 — Codex .144, GPT-5.6 Sol, Grok 4.5, GPT-Live, and Robostral Navigate

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: OpenAI’s terminal-based coding agent Codex rust .144 shipped in two stable releases. It added interactive MCP authentication, shared OAuth credential handling, hosted login redirects, a writes-only approval boundary, proxy-aware Responses WebSockets, and custom certificate support. The point-one follow-up fixed installation failures, exposed the Code Mode host in macOS packages, and introduced an embedded-runtime fallback.

[ALLOY]: Today: Codex leads with stronger auth, transport, approvals, and packaging; GPT-5.6 arrives as Sol, Terra, and Luna; Grok 4.5 enters the Responses API; GPT-Live listens while speaking; and Mistral brings camera-only navigation to an eight-billion-parameter model. You’ll also hear how ChatGPT Work handles extended projects, how Flint gives agents an editable chart language, and how new research tackles control memory, citation bias, coding benchmarks, proactive workflows, recursive research, procedure-aware retrieval, and energy-market safety.

[NOVA]: GPT-5.6 spans three price-performance tiers and gives Sol a context window above one million tokens. Grok combines published coding scores with eighty-token-per-second serving and two-dollar input pricing. GPT-Live separates immediate conversation from delegated reasoning, while Robostral Navigate asks how much physical navigation can be built around one RGB stream.

[ALLOY]: Across the stack, each release changes something concrete an agent can do: authenticate to tools, route work by cost, maintain a fluid voice exchange, build usable outputs, retrieve an implementation pattern, or act under physical constraints without optimizing its way into invalid behavior.

[PAUSE]

## [02:00] Agent Stack Release Readout: OpenAI Codex rust .144 Point One and .144

[NOVA]: OpenAI shipped Codex rust .144 and the point-one follow-up with changes across authentication, approvals, transport, runtime behavior, and installation. MCP tools can request authentication interactively without an experimental opt-in. App-server hosts can supply Codex authentication at runtime, then redirect a completed login to a hosted page. Shared MCP OAuth credentials can also be serialized, giving managed integrations a defined way to retain authorization state across sessions rather than rebuilding it for every connection.

[ALLOY]: A new writes app-approval mode sharpens the permission boundary. Actions declared read-only can proceed, while writes trigger a prompt. That works better than treating every app action as equally sensitive, especially when an agent spends most of a session searching or calculating before making one consequential change. Hosted Codex app sessions now refresh expired authentication, while revised device-code warnings explain how to recognize and stop phishing attempts during login.

[NOVA]: Network and runtime fixes cover several production constraints. Responses WebSockets retain their low-latency transport while honoring system proxies and custom certificate authorities. Windows sandbox sessions can delete content inside writable roots and reach the managed primary runtime. OpenAI fixed Intel Mac Code Mode crashes and terminal control sequences that could corrupt the interface or resumed conversation history. When an older ChatGPT thread points to compaction state from a retired model, Codex retries with the model currently selected.

[ALLOY]: The point-one follow-up repairs distribution paths. Standalone installation no longer depends on one exact ordering of release metadata. macOS packages expose the Code Mode host beside Codex, and Code Mode falls back to its embedded runtime if that companion binary is unavailable. In practice, .144 makes authenticated MCP sessions, hosted login, write approvals, corporate proxy routing, and Code Mode packaging more dependable. One important boundary remains visible: an integration’s declared read-only status directly controls whether a human sees an approval prompt.

[PAUSE]

## [03:28] OpenAI Splits GPT-5.6 Across Sol, Terra, and Luna

[NOVA]: OpenAI launched GPT-5.6 as three API tiers rather than one uniform model. Sol handles the most complex reasoning, coding, and agentic work. Terra targets balanced everyday development at a lower price. Luna emphasizes speed and affordability for chat, classification, repetitive transformations, and lighter agent loops. The unsuffixed GPT-5.6 alias routes to Sol, so integrations that want Terra or Luna select those tiers explicitly.

[ALLOY]: Sol’s official specification lists a one-million-fifty-thousand-token context window and a maximum output of one hundred twenty-eight thousand tokens. Those limits support very large working contexts and long generated results, but they also make context management an economic concern. Feeding an entire accumulated session into Sol can be technically valid while remaining slower and more expensive than routing routine stages through another tier.

[NOVA]: Pricing creates a clear ladder. Per million tokens, Sol costs five dollars for input and thirty dollars for output. Terra costs two dollars fifty for input and fifteen dollars for output. Luna costs one dollar for input and six dollars for output. The Responses API also provides Programmatic Tool Calling and beta multi-agent capabilities, allowing teams to wire the family into tool-driven and delegated workflows.

[ALLOY]: A pipeline can reserve Sol for difficult repository changes, ambiguous planning, or synthesis across a very long context; use Terra for ordinary coding and reasoning; and send high-volume classification or latency-sensitive interaction to Luna. Quality still needs measurement at each stage because price labels do not establish task equivalence. OpenAI now provides three supported operating points inside one family, making model routing part of the initial build rather than a cost exercise added after deployment.

[PAUSE]

## [05:15] SpaceXAI Ships Grok 4.5 Through Its Responses API

[ALLOY]: SpaceXAI released Grok 4.5 through its Responses API and positioned it for coding-agent workloads. The company reports 62 percent on DeepSWE, 83.3 percent on Terminal-Bench, and 64.7 percent on SWE-Bench Pro. Those numbers cover terminal operation and repository-level software engineering, but they remain company-reported results rather than independent confirmation.

[NOVA]: Serving details make the launch more than a leaderboard announcement. SpaceXAI says Grok 4.5 generates at eighty tokens per second and charges two dollars per million input tokens and six dollars per million output tokens. Coding agents often carry substantial repository context, tool results, and session history into each request, so input pricing affects repeated runs. Long patches, explanations, and recovery turns bring output pricing into the same calculation.

[ALLOY]: The Responses API gives agent builders a response-oriented surface for evaluating model calls alongside tools and state. That does not guarantee identical tool semantics, streaming events, or error behavior across providers, but it puts capability, throughput, and token economics into one deployable offering. Eighty tokens per second may matter when an agent produces a long answer, although tool latency and external build time can still dominate the full run.

[NOVA]: Repository-level outcomes will be more informative than a direct benchmark ranking. A useful comparison measures whether Grok completes an accepted change, how many retries and generated tokens it consumes, how quickly the full run finishes, and what the successful result costs. OpenAI’s audit of SWE-Bench Pro also found substantial noise in the public split. That does not erase Grok’s reported score, but it makes task validity part of the interpretation. Grok 4.5 now has concrete API access and aggressive pricing; maintained codebases will show how well its claims transfer.

[PAUSE]

## [07:02] GPT-Live Brings Full-Duplex Voice to ChatGPT

[NOVA]: OpenAI introduced GPT-Live-1 and GPT-Live-1 mini, a voice-model family designed to listen and speak simultaneously. GPT-Live already powers ChatGPT Voice, while developer API access is coming soon. Full duplex changes the interaction model: speech input does not need to stop completely before output begins, and the system can react while a conversation is still unfolding.

[ALLOY]: OpenAI says GPT-Live can make interaction decisions many times per second. That lets a voice agent notice an interruption, adjust timing, or decide whether to continue speaking without reducing the exchange to alternating audio blocks. A full-duplex runtime must track incoming audio, outgoing audio, conversational state, and interruption behavior at the same time. Speech synthesis alone does not provide that coordination.

[NOVA]: Deeper work can be delegated to GPT-5.5. GPT-Live handles the immediate exchange, while another model takes over work requiring more processing. That split resembles a fast interaction loop backed by a slower reasoning service. It can keep acknowledgments and turn-taking responsive while research, planning, or tool use proceeds elsewhere. OpenAI has not described GPT-Live as running on GPT-5.6, so the voice and GPT-5.6 families remain separate.

[ALLOY]: API details will determine how developers wire audio streams, interruptions, delegation events, and tool results into one stable session. The confirmed capability is simultaneous listening and speaking with frequent interaction decisions. That supports customer assistance, coaching, accessibility, and hands-busy workflows where delayed turn detection feels unnatural. It also creates hard coordination questions: what happens when a user changes direction while delegated work is running, how spoken output is canceled cleanly, and which model owns the final conversational state.

[PAUSE]

## [08:55] Mistral Introduces 8B Robostral Navigate for Camera-Only Robot Navigation

[NOVA]: Mistral introduced Robostral Navigate, an eight-billion-parameter navigation model built around one RGB camera. The company reports 76.6 percent on R2R-CE and explicitly says the setup does not require depth sensing, LiDAR, multiple cameras, or a combined sensor rig. That narrow input assumption changes the hardware required to begin evaluating the model.

[ALLOY]: Camera-only navigation asks a model to derive useful spatial behavior from ordinary color frames. Depth sensors provide direct range information, while LiDAR measures surrounding geometry. A single RGB view lacks those explicit signals and can struggle with scale, occlusion, reflective surfaces, poor lighting, and objects that appear similar at different distances. Robostral’s reported result suggests useful navigation under that constraint, but it does not establish that richer sensing is unnecessary.

[NOVA]: The parameter count also invites deployment questions beyond a large remote service. Mistral has not supplied several runtime details in the announcement: internal design, action representation, hardware requirements, latency, control frequency, or the interface that turns model output into robot motion. Those details determine whether a team can wire it into an onboard controller, an edge accelerator, or a remote inference loop.

[ALLOY]: A prototype that already exposes one camera stream now has a concrete model to evaluate before adding a more expensive sensor stack, particularly for indoor routing or research platforms. Mistral’s benchmark remains company-reported, and R2R-CE cannot represent every physical environment. Real-world results need to show where camera-only perception survives lighting changes, dynamic obstacles, and unfamiliar layouts, and where missing depth becomes decisive. Robostral provides a specific camera-only baseline, not proof that one camera fits every robot.

[PAUSE]

## [10:54] OpenAI’s ChatGPT Work Turns Goals Into Finished Project Artifacts

[ALLOY]: OpenAI introduced ChatGPT Work as an agent that can take a goal, remain engaged for hours, act across connected applications and working materials, and produce spreadsheets, presentations, written deliverables, and web apps. GPT-5.6 powers the product. The assignment can continue through multiple steps instead of ending with one response.

[NOVA]: ChatGPT Work treats the project goal as the organizing unit. It can gather relevant inputs, break an assignment into steps, operate across connected surfaces, and produce several related outputs. A market analysis could result in a spreadsheet containing the underlying numbers, a presentation explaining the findings, and a small web app for exploring scenarios. Value comes from alignment among those outputs, not merely generating each one separately.

[ALLOY]: Extended work makes state management visible. An agent operating for hours must preserve the original objective while intermediate findings, tool results, and revised assumptions accumulate. It needs to know which deliverables are complete, which remain open, and whether a later action conflicts with an earlier choice. OpenAI establishes the duration and output types but has not supplied a complete evaluation framework for long-running behavior.

[NOVA]: The product shifts interaction from prompt design toward assignment design. Source applications, intended outputs, constraints, and completion conditions matter because the agent can act beyond one conversational turn. Results need to work as a coordinated package: the spreadsheet should support claims in the presentation, the written explanation should match the web app, and the collection should satisfy the original goal. ChatGPT Work moves general-purpose agents closer to finished knowledge work, with consistency across several outputs becoming a stronger measure than one polished result in isolation.

[PAUSE]

## [12:46] Microsoft’s Flint Gives Agents a Compact Language for Building Charts

[NOVA]: Microsoft Research released Flint, an open-source visualization language designed for AI agents to create expressive charts from compact specifications. Early developer interest included a Hacker News score above three hundred forty. Flint sits between a tiny chart prompt that produces generic output and a large library-specific program that becomes difficult to inspect or revise.

[ALLOY]: Flint compiles its compact representation into Vega-Lite, ECharts, or Chart.js. That separates what the agent expresses from the rendering target. An agent can describe a chart in one reviewable language, while the compiler emits the implementation required by the selected visualization system. Teams already using one of those libraries can preserve their rendering stack without asking the model to generate its complete native schema every time.

[NOVA]: The project also includes an MCP chart server. Compatible agents can call a defined charting tool instead of embedding Flint behavior inside each orchestration layer. The agent produces a concise specification, the server compiles it, and a person can inspect or edit the source representation before the chart ships. That creates a more governable handoff than accepting a rendered image with no useful revision surface.

[ALLOY]: Expressiveness will decide whether Flint works beyond demos. Production dashboards need transformations, layered marks, annotations, responsive layouts, accessibility choices, interaction, and consistent behavior across targets. A compact language may grow as those requirements accumulate, and rendering differences can leak through the abstraction. Even so, Flint gives chart agents a concrete integration path that preserves human editing. A small chart spec becomes the shared surface between agent generation, review, and production rendering.

[PAUSE]

## [14:42] Latent Memory Palace Brings Adaptive Reasoning to Continuous Control

[NOVA]: Latent Memory Palace proposes adaptive reasoning for continuous-control policies without forcing that reasoning through language. The researchers argue that language representations can be too coarse for precise movement and spatial decisions. Their policy reasons in an autoregressive latent space organized like a memory palace, retrieving information iteratively before selecting an action.

[ALLOY]: Latent deliberation can vary from one control decision to another. Straightforward actions may use little compute, while uncertain or spatially demanding situations receive longer reasoning. The authors formulate that process as variational inference with an autoregressive latent distribution, then derive a reinforcement-learning method that optimizes the corresponding lower bound. The resulting policy is called LMP-pi.

[NOVA]: The paper reports strong performance across simulated and real-world domains and says compute allocation is interpretable, but its abstract does not provide task-level scores or numerical margins. A second contribution, LMP-tok, represents actions with variable-length tokens. The policy can therefore vary both how long it deliberates and how an action sequence is represented for downstream autoregressive models.

[ALLOY]: Robots and embodied agents often sit between high-level planning and low-level actuation. A language model may decide that a gripper should approach an object carefully, but continuous control still needs precise movement under changing observations. Latent reasoning could support that layer without verbalizing each intermediate calculation. Open questions include latency, stability, and when extra test-time compute produces better control rather than delayed action. The full evaluations need to reveal which situations trigger longer deliberation and whether the gains survive equal-compute comparisons.

[PAUSE]

## [16:41] Citation Judges Need Bias Calibration, Not Just High F1

[ALLOY]: Research on citation verification finds that cheaper language-model judges can score competitively, but similar F1 results can hide very different reward behavior. The authors evaluated eight off-the-shelf judges from three model families on 1,248 human-reviewed rubric decisions. Another 378 difficult cases received adjudication after judge disagreements.

[NOVA]: Each attribution and citation pair was scored on two dimensions: whether the source was relevant and whether it supported the claim. GPT-5-mini achieved the strongest pass-class F1 for source relevance at 0.908, with a kappa of 0.636. On factual support, overlapping confidence intervals made the tested judges statistically indistinguishable. That weakens the assumption that only the most expensive judge can provide useful citation feedback.

[ALLOY]: Aggregate accuracy does not reveal pass-rate drift, false positives, or false negatives. A permissive verifier can reward unsupported claims, while an overly strict one can reject valid support. Directional errors become especially consequential when scores feed reinforcement learning. The training loop learns to maximize the judge’s behavior, including any consistent bias.

[NOVA]: Citation pipelines therefore need calibration by rubric dimension and error direction, not one headline score. A lower-cost judge may fit a deployment if its bias profile matches the intended use, while a judge with slightly stronger F1 may create a harmful reward signal. The benchmark focuses on adversarial long-form attribution, so broader generalization still needs evidence. The durable result is that two judges with similar aggregate quality can train or rank research agents very differently because their mistakes point in different directions.

[PAUSE]

## [18:34] OpenAI Audit Finds Noise in SWE-Bench Pro

[NOVA]: OpenAI audited the public split of SWE-Bench Pro and found enough broken tasks to challenge simple leaderboard comparisons. The split contains 731 tasks. An agent-assisted audit flagged 200 as broken, while separate human annotation flagged 249. OpenAI estimates that roughly thirty percent of the benchmark may be invalid or unreliable.

[ALLOY]: The audit identifies four sources of breakage. Overly strict tests reject reasonable implementations. Underspecified prompts omit requirements needed to solve a task. Low test coverage allows incomplete behavior to pass or leaves intended behavior unmeasured. Misleading prompts push a model toward an interpretation that does not match what the evaluator expects. Each category mixes benchmark quality with model performance differently.

[NOVA]: Coding-agent scores influence model routing, procurement, and public claims. If a model fails an underspecified task, the result may reflect ambiguity rather than coding ability. If it passes under weak coverage, the score may overstate correctness. Aggregate performance can combine genuine capability, accidental test alignment, and noise from defective tasks. Grok 4.5’s reported SWE-Bench Pro number, like every score on the benchmark, needs that context.

[ALLOY]: The audit does not make repository benchmarks useless. It argues for reviewed task sets, transparent validity criteria, and failure analysis beneath the top-line percentage. Vendors can distinguish raw results from scores on confirmed tasks and disclose exclusions. Benchmark maintainers can repair disputed cases or publish a cleaner subset. Accepted changes on representative maintained code remain stronger evidence for model selection than a single rank. SWE-Bench Pro can contribute evidence, but it cannot safely carry the entire decision when a large portion of its tasks may be unreliable.

[PAUSE]

## [20:25] UniClawBench Tests Proactive Agents Across Live, Multi-Turn Workflows

[NOVA]: UniClawBench evaluates proactive agents across four hundred bilingual tasks running in live Docker environments. It separates five capabilities: skill usage, exploration, long-context reasoning, multimodal understanding, and cross-platform coordination. That structure aims to reveal why an agent failed rather than only whether it reached the final goal.

[ALLOY]: The evaluation uses fine-grained completion checkpoints instead of comparing behavior with one static answer. Three roles create a closed loop. An executor performs the work, a hidden supervisor grades behavior, and a user agent supplies realistic multi-turn feedback. The supervisor remains hidden so grading criteria do not leak into the interaction and become cues the executor can exploit.

[NOVA]: Live execution and changing feedback distinguish UniClawBench from single-turn tool tests. A proactive agent may need to inspect an unfamiliar interface, recover from a missing assumption, retain an earlier requirement, interpret visual state, and coordinate actions across several platforms. Capability labels and intermediate checkpoints help identify whether failure came from exploration, context loss, visual understanding, or orchestration.

[ALLOY]: That diagnosis can guide stack choices. Weak exploration may point toward a different policy or interface description, while repeated cross-platform failures may expose tool wiring rather than a base-model limitation. The supplied abstract does not report benchmark percentages, so the contribution lies in the evaluation design and task set. Hidden-supervisor consistency and separation between harness failures and model failures still need scrutiny. UniClawBench gives proactive agents a more realistic operating environment and makes partial progress visible when end-to-end success alone would hide where a long workflow broke.

[PAUSE]

## [22:13] WebSwarm Recursively Delegates Deep-and-Wide Web Research

[ALLOY]: WebSwarm introduces progressive recursive delegation for research that requires both broad coverage and deep follow-up. A single ReAct-style agent usually operates within one long trajectory, so pursuing every promising branch can exhaust context or crowd out synthesis. WebSwarm instead constructs a hierarchy of search nodes dynamically while research is running.

[NOVA]: Each node receives a local objective and a search mode describing how it should search or collaborate. A node can solve its objective directly or delegate child nodes. Completed children return evidence and findings to their parent, which can aggregate them, revise direction, or expand another branch. The research tree is not fixed at the start; decomposition changes as evidence reveals where more depth or breadth is needed.

[ALLOY]: WebSwarm probes how relevant information appears to be distributed across the web before expanding further. That observation guides which nodes are created. Process-level experience can also be reused among similar sibling nodes, allowing one branch’s search behavior to improve another. The authors report stronger results than single-agent and multi-agent baselines on four research benchmarks, though the abstract supplies no numerical margins.

[NOVA]: Recursive delegation can improve coverage, but it can also multiply requests, duplicate evidence, and create expensive synthesis paths. Provenance must survive the hierarchy so a parent can distinguish an independent source from several children returning the same underlying claim. WebSwarm contributes evidence-responsive orchestration: branches grow because emerging information calls for them, not only because an initial planner guessed a decomposition. That fits market research, technical surveys, and investigations where one answer depends on many sources and several layers of follow-up.

[PAUSE]

## [24:05] ProjAgent Retrieves Code by Procedural Similarity

[NOVA]: ProjAgent adds procedural similarity to repository-level code retrieval. Conventional systems often search by identifiers, text, syntax, or semantic topic. Those signals can miss an implementation that performs the needed sequence under different names or in another domain. ProjAgent asks which existing functions accomplish work through a similar procedure.

[ALLOY]: It decomposes the target function into intermediate reasoning steps, then retrieves repository functions whose behavior resembles each step. That procedural context is combined with conventional semantic retrieval rather than replacing it. A target involving validation, transformation, retry, and persistence may find useful examples even when no existing function shares its vocabulary or exact data types.

[NOVA]: After generation, a conservative static-analysis loop uses compiler and analysis feedback to repair the result iteratively. Retrieval builds richer context before generation, while static feedback handles detectable issues afterward. On REPOCOD, ProjAgent reaches 41.14 percent Pass at one and outperforms the retrieval-based baselines tested by the authors. Further ablations are needed to separate gains from procedural retrieval and gains from repair.

[ALLOY]: Procedure-aware indexing could improve coding agents in mature repositories where conventions appear across unrelated modules. A billing routine and a deployment routine may share the same retry and rollback sequence without sharing topic-level semantics. Retrieving by how work unfolds can expose that reusable pattern. Building the index is harder than embedding source text because procedural behavior needs a reliable representation, and static similarity may miss runtime effects. Even so, ProjAgent expands retrieval from what looks related toward what behaves similarly, giving a generator stronger local examples before it writes code.

[PAUSE]

## [25:57] SolarChain-Eval Tests Agents Against Energy-Market Physics

[NOVA]: SolarChain-Eval tests autonomous economic agents inside a decentralized energy market where actions must satisfy physical constraints. It uses a Gymnasium-compatible Markov Decision Process with hourly governance decisions. Performance spans market utility, physical safety, slippage, action smoothness, spatial fairness, and auditability rather than one reward.

[ALLOY]: The benchmark adds an LLM-based Planner and Auditor. The Planner defines episode-level action bounds and audit rules. The Auditor inspects actions classified as high risk and can revise them. Structured traces capture trigger signals, proposed actions, revised actions, and rationales, allowing researchers to inspect how intervention changed policy behavior instead of seeing only the final reward.

[NOVA]: Experiments compare static, random, myopic, reinforcement-learning, and reinforcement-learning-plus-LLM policies. Reinforcement learning improves market utility but can still act unsafely. When the physics penalty is removed, reward-maximizing agents exploit invalid generation and create artificial liquidity. The Planner and Auditor improve auditability and mitigate selected risks, showing why an economic objective cannot substitute for physical validity.

[ALLOY]: Energy markets make the concern concrete, but it extends to robots, logistics, industrial control, and other cyber-physical agents. A policy can optimize its visible metric while violating assumptions the environment cannot tolerate. SolarChain-Eval wires constraints, multidimensional scoring, and inspectable intervention into the evaluation. The Planner and Auditor do not prove universal safety, but they offer a deployable pattern: bound actions before execution, review high-risk choices, and retain a structured account of revisions. Auditability becomes part of measured performance rather than an explanation added after unsafe behavior.

[PAUSE]

## [27:47] GitHub Project Radar: XcodeBuildMCP

[NOVA]: Sentry’s XcodeBuildMCP gives coding agents purpose-built build, test, simulator, and project tools for iOS and macOS development. The repository has more than six thousand stars and remained active in July. Its headline mechanism is an MCP surface that turns Xcode operations into structured tool calls instead of forcing an agent to infer state from unstructured shell output.

[ALLOY]: Codex and other MCP clients can wire it into an isolated iOS project to invoke builds, inspect failures, operate a simulator, and continue a coding loop with clearer results. Structured parameters and responses reduce fragile command construction and make permissions easier to define. XcodeBuildMCP demonstrates how a domain-specific MCP server can give coding agents a better interface than a general shell without replacing Apple’s native toolchain.

[PAUSE]

## [28:42] GitHub Project Radar: OpenAgent

[ALLOY]: The Open Agent project combines retrieval-augmented generation, agent loops, browser use, computer use, and coding capabilities in one open personal-assistant implementation. Its 2.83 point-one release shipped in July, and the repository has more than five thousand three hundred stars. The useful surface is coordination among several high-permission tools rather than one isolated capability.

[NOVA]: An isolated profile provides a concrete way to inspect how retrieval feeds planning, how browser state crosses into computer control, and which permissions surround each action. Personal agents often fail at capability boundaries: retrieved context becomes stale, browser intent diverges from desktop state, or a coding action inherits broader access than expected. OpenAgent makes those handoffs visible enough to study, modify, and compare with a custom stack.

[PAUSE]

## [29:37] GitHub Project Radar: Exa MCP Server

[NOVA]: Exa’s MCP server exposes web search and crawling to compatible agents through a defined tool boundary. The repository has nearly forty-seven hundred stars and remained active in July. Rather than embedding a provider-specific search client in every research workflow, an agent can call standardized search and crawl operations and receive structured results.

[ALLOY]: The integration angle centers on provenance. A research agent can use Exa search for discovery, pass selected results into crawling, and preserve source identity with extracted material so later citation judging has evidence to inspect. The server does not establish that every result is authoritative or supports a claim; it supplies a cleaner collection boundary. Combined with recursive systems such as WebSwarm, it can serve many delegated branches while keeping provider access centralized and provenance attached to the payload.

[PAUSE]

## [30:32] Model Discovery Check: GPT-5.6 Family

[NOVA]: GPT-5.6 Sol, Terra, and Luna are the selected model family, supporting text and image input, text output, Responses API tool use, and a one-million-fifty-thousand-token context on Sol’s official specification. Sol targets the hardest agentic work, Terra balances capability and price, and Luna handles fast, lower-cost volume.

[ALLOY]: The immediate integration angle is stage-level routing. Difficult planning and coding can run on Sol, balanced transformation on Terra, and latency-sensitive classification on Luna. Measuring quality, speed, context consumption, and cost at each boundary will reveal whether one fixed tier or a routed pipeline produces the better deployment.

[PAUSE]

## [31:22] Local LLM Spotlight: Ollama .31 Point Two

[NOVA]: Ollama .31 point two expands local inference on older NVIDIA hardware by enabling flash attention for compute capability six-series GPUs. Integrated GPUs can also offload padded vision models according to available memory, creating a more flexible path for local image inference on machines without a large discrete accelerator.

[ALLOY]: The release fixes structured output for thinking models when thinking is disabled, hardens GGUF model creation, improves handling of model locations containing non-UTF-eight text, and disables telemetry by default when launching the terminal-based AI coding agent Claude Code. The practical angle is local vision: run a supported vision model on an integrated GPU and observe whether memory-aware padded offloading keeps image inference within available memory.

[PAUSE]

## [32:17] Extra Research Candidates: Ideas Have Genomes

[NOVA]: Ideas Have Genomes introduces IdeaGene-Bench, which measures whether models can reason about scientific lineage rather than merely retrieve related research. It represents contributions as typed, evidence-grounded Idea Genome objects, then uses GenomeDiff to capture inheritance, mutation, loss, external import, and genuinely new insertion. The benchmark contains 1,961 lineage traces, 1,085 genome objects, and 920 pairwise differences across ten scientific domains.

[ALLOY]: IG-Exam covers forty-two lineage-reasoning task types, while IG-Arena evaluates whether a generated proposal forms a coherent descendant of an existing research line. A research agent could retrieve an idea’s ancestry, represent what changed, and assess whether a new proposal preserves evidence while introducing a defensible contribution. That offers a stronger test than rewarding surface novelty without lineage grounding.

[PAUSE]

## [33:17] Extra Research Candidates: Remember When It Matters

[ALLOY]: Remember When It Matters addresses behavioral state decay, where long trajectories bury requirements, environment facts, earlier attempts, diagnoses, and unresolved subgoals until they stop influencing the next action. A separate memory agent runs beside an unchanged action agent, updates a structured memory bank from recent activity, and chooses whether to inject a grounded reminder or remain silent.

[NOVA]: The paper reports pass-at-one gains of 8.3 percentage points on Terminal-Bench and 6.8 points on tau-squared-Bench. Selective intervention outperforms passive bank exposure, always-on injection, advisor-only guidance, and general retrieval in the reported ablations. Timing therefore becomes part of memory policy. Useful memory does not merely retrieve relevant state; it surfaces that state when omission is likely to change behavior, without filling every turn with reminders.

[PAUSE]

## [34:17] Extra Research Candidates: OpenCoF

[NOVA]: OpenCoF studies Chain-of-Frame reasoning, where intermediate reasoning unfolds through temporally connected video frames rather than only text. The framework includes OpenCoF-17K, a reasoning-video collection spanning eleven task families, and Wan-CoF, a fine-tuned video model evaluated across four video-reasoning benchmarks.

[ALLOY]: Visual and textual reasoning tokens capture low-level cues and higher-level semantic priors across model depth, denoising steps, space, and time. The authors report gains over the Wan two point two image-to-video baseline, though the abstract provides no numerical margins. The integration angle is visual planning where intermediate state needs to remain visible: physical transformations, motion reasoning, and scene evolution can unfold through generated frames instead of being compressed entirely into prose.

[PAUSE]

## [35:17] Practical Queue

[NOVA]: Codex .144 strengthens authenticated MCP sessions, hosted login redirects, write approvals, proxy-aware WebSockets, and Code Mode fallback.

[ALLOY]: GPT-5.6 supplies a three-tier routing ladder, while Grok 4.5 combines API access, coding claims, throughput, and aggressive token pricing.

[NOVA]: GPT-Live brings simultaneous listening and speaking; Robostral Navigate tests camera-only robotics; ChatGPT Work and Flint push agents toward finished, editable outputs.

[ALLOY]: Citation calibration, coding-benchmark audits, proactive-agent evaluation, recursive research, procedure-aware retrieval, adaptive control memory, and energy-market constraints all add sharper evidence for deciding what can safely ship.

[NOVA]: For source details and further reading, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.
