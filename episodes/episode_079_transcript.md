# EP079 — Hermes Agent 7.1 and Claude Code .193 Ship; Kimi K2.7 Lands in Copilot

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: Hermes Agent 7.1 and the terminal-based AI coding agent Claude Code .193 lead the release readout: Hermes added first-class Mixture-of-Agents ensembles, fixed the interrupt-protected compression sibling-fork bug, tightened credential-exfiltration hardening, introduced completion contracts on slash-goal, and added gateway drain coordination for scale-to-zero deployments.

[ALLOY]: Hermes also promoted background subagents with lifecycle isolation, exposed every reference model's reasoning trace during ensemble runs, streamed the aggregator answer live, and closed roughly six hundred ninety-two top-priority issues and pull requests during a twelve-day push.

[NOVA]: Today: Hermes and Claude Code lead the harness update, ZCode wraps GLM-5.2 and hits the Hacker News front page, Kimi K2.7 Code goes generally available inside GitHub Copilot, and Mistral ships Leanstral 1.5 as an open-weights Lean proof model.

[ALLOY]: You'll hear why Alibaba's Claude Code ban matters at the harness layer, how WebBrain keeps browser automation local, why RECONTEXT attacks long-context utilization without training, and how Senior SWE-Bench, AgenticSTS, DramaSR, Program-as-Weights, ghealth, Ollama, and the MCP project radar fit into shipped agent stacks.

[PAUSE]

## [02:00] Agent Stack Release Readout: Hermes Agent 7.1; Claude Code .193

[NOVA]: Hermes Agent 7.1 shipped on July first, tagged from the 0.18 line, and the team is calling it the judgment release. The headline number is unusually concrete: over twelve days, Hermes closed every open P0 and P1 issue and pull request in the project, about six hundred ninety-two highest-priority items out of roughly nineteen hundred fifty total closures. The final P0 cluster centered on an interrupt-protected compression sibling-fork bug, and the same push included cron reliability work, credential-exfiltration hardening, and a broad wave of P1 cleanup.

[ALLOY]: The most visible builder change is Mixture-of-Agents as a first-class model choice. Instead of wiring a custom router that calls several models, waits on them, and stitches a result, Hermes now lets you pick a named ensemble the same way you would pick one model. The call fans out to the reference models, shows each member's reasoning trace, and streams the aggregator's synthesized answer while it is being produced. That makes multi-model review usable inside the normal agent loop rather than as a separate orchestration layer.

[NOVA]: The second major change is completion contracts on slash-goal. Hermes can bind task completion to evidence checks instead of trusting the agent's own declaration that work is finished. Slash-learn and slash-journey make self-improvement more steerable, while background subagents now run with lifecycle isolation, so long-running subtasks can fan out without collapsing the parent session. Gateway scale-to-zero with drain coordination matters in production-style deployments because active sessions can finish before capacity scales down.

[ALLOY]: Claude Code .193, Anthropic's terminal-based AI coding agent, is the other stable harness named in the readout. Its relevance lands partly through the Alibaba policy story later: Claude Code's shell, diff, and tool-call loop is powerful precisely because it sees active code context and terminal output. Hermes is pushing toward verifiable agent completion and deployable ensembles; Claude Code remains a reference point for how much authority coding agents now exercise at the terminal.

[PAUSE]

## [03:51] ZCode Harness Wraps GLM-5.2, Hits Hacker News Front Page

[NOVA]: Z.ai's ZCode wrapped GLM-5.2 in a coding harness and surged past five hundred points on Hacker News, which is serious Western developer attention for a Chinese-vendor agent tool. ZCode is not just a model page around GLM-5.2. It is a terminal-facing harness that puts an agent loop, tool routing, project scaffolding, and code-edit prompting around the model so developers interact with a workflow rather than a raw chat endpoint.

[ALLOY]: The split is the important part. GLM-5.2 provides the weights, tokenizer, and inference path. ZCode adds the runtime that decides when to inspect project context, when to propose an edit, how to frame tool calls, and how to package code tasks for the model. That lets Z.ai improve the harness without retraining GLM-5.2, and it lets the model evolve without forcing developers to relearn the entire coding interface. Claude Code and Codex use the same product shape: the harness becomes the part developers feel every day.

[NOVA]: Hacker News discussion clustered around three questions: whether Z.ai can price inference aggressively, whether GLM-5.2 performs well enough on repository-scale coding tasks, and whether the integration surface reaches beyond a terminal harness. The thread's size matters because it moves ZCode out of curiosity territory. Developers were comparing it against Sonnet-style coding runs and GPT-class agent behavior, not treating it as a regional novelty.

[ALLOY]: The next adoption step is integration. An IDE plugin, JetBrains extension, or MCP server would make ZCode easier to place inside Western team workflows. Without that, it remains attractive for terminal-first users and cost-sensitive experiments. With it, GLM-5.2 gets a credible route into the same day-to-day coding-agent market where Claude Code, Codex, and Copilot already compete.

[PAUSE]

## [05:42] Kimi K2.7 Code Goes GA in GitHub Copilot

[NOVA]: GitHub Copilot added Moonshot AI's Kimi K2.7 Code as a generally available model option on July first. That puts Moonshot's coding-tuned K2.7 variant directly inside the Copilot selector, next to Anthropic Sonnet, GPT-family models, and Gemini entries. The Hacker News announcement cleared more than four hundred points within hours, which tracks with demand from developers who had already been routing Kimi through Moonshot endpoints or third-party providers.

[ALLOY]: K2.7 Code runs on the same hundred-billion-parameter Mixture-of-Experts backbone as the K2 line. Instead of activating the full weight matrix on every token, the model selects a subset of experts per token, so it can carry a large total parameter budget while keeping per-token cost and latency closer to a smaller dense model. The coding-specific tuning targets fill-in-the-middle completion, multi-step edit handling, and tool-call reliability, which are exactly the pieces that decide whether an agent loop feels stable.

[NOVA]: First-party Copilot availability changes the adoption path. Teams no longer need to wire a Moonshot key, route through a third-party gateway, or maintain separate provider config just to compare K2.7 Code against Sonnet or a GPT model. The same selector can drive inline suggestions, chat, and Copilot agent mode. That matters for cost-sensitive teams because model choice becomes a workspace setting rather than a side integration.

[ALLOY]: The interesting comparison is long-context refactoring and multi-step coding work, not a single autocomplete. K2.7 Code has to hold project intent, respond with reliable edits, and keep tool calls structured enough for Copilot to execute. If the MoE pricing advantage holds while the coding quality stays near the frontier options, Kimi can become the default economical model for many team plans rather than an experimental pick.

[PAUSE]

## [07:34] Jamesob's GitHub Guide Curates Running SOTA LLMs Locally

[NOVA]: Jamesob's local-LLM guide climbed to the Hacker News front page with roughly three hundred eighty upvotes because it solves a real procurement problem: which open-weight model should you run on the hardware you actually own? The guide gathers scattered community wisdom about local inference, quantization, VRAM budgets, and serving runtimes into one practical reference for developers who do not want to spend weeks reading chat threads.

[ALLOY]: The guide starts from memory tiers instead of hype. At the twenty-four gig, forty-eight gig, and eighty gig levels, it maps usable model sizes to GGUF quantization choices and runtime options, with llama.cpp as the default backend. It also calls out KV-cache sizing for longer context windows, because a model that fits at load time can still become unusable once prompt length and cache growth enter the picture. That detail saves people from buying hardware that looks fine on paper but stalls under real decode load.

[NOVA]: The timing is why it landed. Open-weight models have settled into several useful bands: small fast assistants, mid-sized twenty-something to thirty-something billion parameter models, and seventy-billion-plus systems that need serious memory. Each band now ships in multiple quant formats and with different serving assumptions. A curated guide gives teams a defensible way to pick a local stack without treating every GPU purchase as a guess.

[ALLOY]: The integration angle is straightforward. Local inference can back coding agents, browser agents, private RAG, and evaluation harnesses through an OpenAI-compatible endpoint or a llama.cpp server. The guide makes local deployment feel less like enthusiast tinkering and more like capacity planning: model size, quant level, context target, runtime, and sustained throughput all have to fit together before the agent loop feels responsive.

[PAUSE]

## [09:28] Alibaba Bars Claude Code at Work Over Backdoor Risk

[NOVA]: Alibaba has told employees to stop using Anthropic's Claude Code internally, according to Reuters reporting dated July third. The directive treats Claude Code as a data-egress and backdoor concern inside company infrastructure. It does not read like a public technical finding against the Claude model itself; it targets the agentic coding harness that runs in the developer environment and sends working context to Anthropic's inference API.

[ALLOY]: The reason security teams focus on the harness is concrete. Claude Code reads active code context, sees shell output, plans edits, and uses tool calls to continue the session. Each round trip can include surrounding diff context, terminal results, and project content needed for the next step. That outbound channel is also the surface a prompt-injection attack or supply-chain trick would try to abuse. From a sovereign-risk perspective, the concern is not only model quality; it is where sensitive engineering context travels during an autonomous coding session.

[NOVA]: For companies operating inside Chinese cloud perimeters, this turns agent choice into a procurement and compliance decision. Domestic alternatives built on Qwen, DeepSeek-derived systems, GLM, or locally hosted models become more attractive when a Western harness is categorized as risky. The fracture happens at the harness layer because that is where shell access, code edits, credentials, and terminal output meet the model provider.

[ALLOY]: Distributed engineering teams will feel this first. The same codebase may be edited with Claude Code on one side of a border and a domestic or self-hosted agent on the other. That pushes teams toward harness-agnostic review, CI, and evaluation surfaces. The agent can vary by region, but the merge gates, regression checks, and security review need to stay consistent if the organization wants one engineering standard.

[PAUSE]

## [11:24] Leanstral 1.5 brings open-weights Lean proof generation to all

[NOVA]: Mistral released Leanstral 1.5, the second major version of its Lean-tuned language model for automated theorem proving. The launch framing, proof abundance for all, signals open weights rather than an API-only gate. That matters because proof generation is compute-hungry and iterative; researchers, hobbyists, compiler engineers, and security teams can now place a competitive Lean model inside their own Lean 4 environment instead of routing every attempt through a hosted endpoint.

[ALLOY]: Leanstral works with Lean 4's tactic-based workflow. A user states a theorem, the model emits a candidate proof script using tactics such as apply, intro, simp, and ring, and Lean's kernel checks the proof. The model is not trusted because the text sounds plausible; the kernel verifies whether the proof is valid. Version 1.5 improves tactic prediction and broadens coverage of mathlib-style patterns, which should reduce the dead ends that appear when a model knows the shape of a proof but misses the library call that actually closes it.

[NOVA]: The integration path is familiar to the Lean community. Existing proof-search harnesses already use lean-gym, REPL interfaces, and Language Server workflows. Leanstral can serve as a local tactic suggester in that loop. The developer still gets kernel-backed correctness, but the model can search the space of tactic sequences faster than a human manually guessing every step.

[ALLOY]: The wider impact reaches beyond pure math. Formal methods are moving into compiler verification, cryptographic protocols, and high-assurance systems. An open-weights proof model lowers the cost of experimenting with certified code and machine-checked reasoning. The watch item is benchmark transparency: MiniF2F-style results, license terms, and community reports will decide whether Leanstral becomes a default local proof assistant or stays a promising research tool.

[PAUSE]

## [13:07] The Safari MCP server for web developers

[NOVA]: WebKit introduced the Safari MCP server for web developers, and the announcement drew more than two hundred sixty points on Hacker News. The release matters because it puts Safari's browser inspection and automation surface behind the Model Context Protocol, giving agent tools a standard way to talk to WebKit-backed developer capabilities instead of relying only on Chrome-centered automation paths.

[ALLOY]: The concrete surface is browser debugging and web development automation. MCP gives an agent a structured tool interface: inspect a page, reason about runtime state, interact with developer surfaces, and return results through a protocol the surrounding agent stack already understands. For web developers, that means Safari can become part of the same tool graph as code search, terminal actions, test runners, and browser checks. Agents no longer have to treat Safari as the browser that sits outside the loop.

[NOVA]: This is especially useful when Safari-specific behavior matters. Web apps can pass in Chromium and fail under WebKit because layout, privacy rules, media behavior, or mobile-adjacent rendering differs. A Safari MCP server gives coding agents a direct route to examine the failing surface, connect it to source changes, and propose fixes without asking the user to manually translate browser state into a prompt.

[ALLOY]: The adoption question is how quickly surrounding tools wire it in. FastMCP-style server frameworks, coding harnesses, and local browser agents can all benefit from a WebKit-native MCP target. The practical gain is not flashy: it is fewer blind spots when an agent is asked to fix a web bug that only appears in Safari. For teams shipping consumer web apps, that is the difference between an agent that only codes and an agent that can actually inspect the browser their users run.

[PAUSE]

## [14:57] WebBrain Ships Open-Source Local-First Browser Agent for Chrome and Firefox

[NOVA]: WebBrain shipped as an MIT-licensed, open-source browser agent for Chrome and Firefox. It reads pages, extracts structured data, and drives multi-step automation through two modes. Ask is the read-only path for page Q&A and extraction. Act is the automation path, where the model emits action sequences such as click, type, navigate, and extract, and the extension's controller executes those actions against the live page.

[ALLOY]: The local-first design is the headline. WebBrain runs as a browser extension with a content-script controller mediating between the DOM and an LLM backend chosen at runtime. The backend can be a llama.cpp server, an Ollama endpoint, or an OpenAI-compatible cloud API. When a local backend is selected, page content and extracted data stay on the machine. That is the key distinction from hosted browser-use vendors, where authenticated pages and internal dashboards may leave the user's environment.

[NOVA]: The mechanism makes it useful for sensitive workflows. Ask can parse the DOM and answer questions about a dashboard, report, or internal tool. Act can chain structured actions across a live page. A developer can point WebBrain at a local seven-billion or fourteen-billion model for routine extraction, then switch to a larger cloud model only when a task needs more reasoning. The same extension surface handles both choices.

[ALLOY]: The integration angle is strong for teams already running local coding agents. WebBrain can become the browser side of that stack: code agent edits the app, browser agent inspects the result, local model keeps private state local. The watch item is reliability under real websites. Content-security policies, unusual front-end frameworks, and changing page structure are where browser agents usually break. If WebBrain keeps the action schema stable while contributors add verbs, it becomes a practical self-hosted alternative.

[PAUSE]

## [16:51] ReContext Paper Adds Training-Free Harness for Long-Context Reasoning

[NOVA]: RECONTEXT, short for Recursive Evidence Replay, is a new training-free harness for long-context reasoning from Yanjun Zhao, Ruizhong Qiu, and Tianxin Wei. It attacks a familiar problem: models can accept huge prompts but still fail to use the right evidence. Instead of asking for a longer window or a new fine-tune, RECONTEXT wraps an existing long-context model at inference time and tries to improve how evidence gets reused.

[ALLOY]: The first mechanism is model-internal relevance extraction. Rather than relying on a separate reranker, summarizer, or embedding pass, RECONTEXT reads relevance signals from the model's own forward pass and scores which prompt spans matter for the current query. Those scores then drive recursive evidence replay. The harness re-injects high-salience spans back into the prompt across staged passes, so the model sees important evidence again with priority instead of letting it disappear inside a massive context window.

[NOVA]: That is useful because many agent stacks already pay for large windows. Code review traces, RAG sessions, legal analysis, and long support histories can fit inside one hundred-thousand or two hundred-thousand token contexts, but fitting does not guarantee reasoning. RECONTEXT offers a way to make the existing window work harder before teams spend on a longer-context model or redesign retrieval.

[ALLOY]: The drop-in nature is the attraction. It is training-free and model-agnostic in the paper's framing, so it can sit between retrieval and final generation or wrap an agent trace before answer synthesis. The watch point is how well the internal relevance signals survive across smaller open-weight models and different attention implementations. If the method only shines on large closed systems, adoption narrows. If it works on local models, it becomes a practical harness upgrade.

[PAUSE]

## [18:37] Snorkel ships Senior SWE-Bench, evaluates agents at senior-engineer scope

[NOVA]: Snorkel released Senior SWE-Bench, an open-source benchmark for coding agents that aims above the single-bug-fix bar. Vanilla SWE-Bench has been valuable, but many tasks boil down to patching a localized issue. Senior engineering work involves cross-service changes, ambiguous requirements, trade-off judgment, and pull requests that span more than one repository. Senior SWE-Bench tries to evaluate that production-shaped work directly.

[ALLOY]: The harness runs locally, which is a major design choice for enterprise teams. Hosted benchmarks usually cannot accept proprietary code, but a local evaluation runner can score internal agents against internal tasks without sending sensitive context to an outside service. The task suites focus on senior-engineer dimensions: design judgment under ambiguity, coordinated changes across services, and multi-repository pull requests where a narrow patch is not enough.

[NOVA]: The CI integration path is where it becomes useful. A team can score agent behavior across model swaps, prompt changes, tool additions, and harness updates using the same rubric. That makes agent improvement measurable beyond demo quality. A coding assistant that looks impressive on small bugs may still fail when it has to modify an API, update a caller, adjust a migration, and keep tests aligned across services.

[ALLOY]: The release also pressures model labs and agent vendors. Saturated benchmark scores are easy to market, but senior-scope tasks expose weak planning, brittle context handling, and poor design judgment. The watch item is which labs publish Senior SWE-Bench numbers first and whether agent harnesses adopt it as a standard release gate. If it catches on, coding-agent competition shifts from patch accuracy toward production engineering competence.

[PAUSE]

## [20:25] ghealth CLI Wraps Google Health API for Fitbit Air Data

[NOVA]: ghealth is a community-built Go command-line tool that wraps the Google Health API and exposes forty Fitbit Air data types as agent-ready JSON. It surfaced through MarkTechPost and fills a missing terminal layer for developers who want wearable telemetry in agent contexts without building their own REST client. It is not an official Google release, so maintenance and schema drift need to be understood before anyone treats it as infrastructure.

[ALLOY]: The tool ships as a single static Go binary and normalizes multiple Google Health API surfaces into one schema. Sleep stages, heart rate, active minutes, oxygen saturation, steps, and related metrics can land in a payload an agent can read without custom parsing for every category. The OAuth flow uses explicit per-data-type scope grants, so the user can authorize heart-rate access without automatically opening every health category.

[NOVA]: That unlocks small but useful agent workflows. A local assistant can summarize recovery trends, correlate sleep and training load, or prepare weekly health notes from structured telemetry. Coding agents can also consume the payload during data-pipeline development, dashboard work, or quantified-self tooling. The important part is that the interface is terminal-friendly and automation-friendly, so it can run on a schedule and feed downstream systems.

[ALLOY]: Because ghealth is community-maintained, the credential and schema posture matters. OAuth refresh tokens behave like high-value secrets, and endpoint changes can alter the payload shape without the warning cadence a first-party SDK might provide. The watch item is whether Google ships an official command-line tool or SDK around the same API. If that happens, ghealth becomes either a useful bridge or a reference point for a more supported path.

[PAUSE]

## [22:26] Program-as-Weights Compiles Natural Language Into Compact Neural Artifacts

[NOVA]: Program-as-Weights proposes a programming paradigm where natural-language specifications compile into compact neural artifacts. The paper is trending on Hugging Face's daily feed with sixty-eight upvotes, and the idea is aimed at fuzzy functions: classification, routing, extraction, scoring, and other tasks where deterministic code is awkward but calling a large general model every time is expensive.

[ALLOY]: The pipeline splits build-time and run-time work. A four-billion-parameter compiler reads a natural-language specification and emits a compact set of weights representing the behavior. A point-six-billion-parameter interpreter runs that artifact at inference time. The deployed surface is not a prompt and not a fine-tune of a giant base model. It is a small neural program executed by a small interpreter, which means the expensive compiler only runs when the behavior is built or revised.

[NOVA]: That changes cost structure. Prompting a frontier model repeats the behavior description on every call, pays for long context, and depends on a general system to follow the spec each time. Program-as-Weights collapses the behavior into weights and pays a tiny forward pass during operation. The authors position it as research, not a product release, but the shape is compelling for on-device and low-latency use.

[ALLOY]: The integration question is whether these compiled artifacts can match large prompted models on real fuzzy tasks. If they can, teams may ship versioned neural artifacts for routing, extraction, and content tagging the way they ship small services today. A four-billion compiler fits on a workstation GPU, and a point-six-billion interpreter can plausibly run on laptops or edge devices. That moves customization cost out of the hot path.

[PAUSE]

## [24:17] DramaSR-532K Pushes Long-Form Speaker Recognition With Reasoning LLM

[NOVA]: DramaSR-532K is a new long-form speaker recognition benchmark from Yuxuan Li, Lingxi Xie, and Xinyue Huo. It contains five hundred thirty-two thousand annotated dialogue lines across more than nine hundred characters from TV dramas. That scale forces models to do more than voice-print matching. They have to combine audio, ASR transcripts, and on-screen visual context to decide which character is speaking across long arcs.

[ALLOY]: The proposed model routes speaker attribution through a reasoning LLM that acts as a controller. It can consult audio embeddings, the transcript, and visual cues before emitting a character label. That matters because long-form drama creates collisions: similar voices, recurring characters, off-screen lines, and scenes where the same speaker identity only makes sense with previous context. A short clip classifier will miss those dependencies.

[NOVA]: For multimodal agent builders, the benchmark gives a public target for identity tracking over time. Long-video understanding, character-aware transcription, meeting analysis, podcast editing, and media search all need stable attribution across many minutes or hours. DramaSR's size makes it possible to evaluate whether a system can preserve identity beyond one scene.

[ALLOY]: The reusable pattern is the reasoning controller. Instead of asking one modality to decide, the LLM coordinates evidence from several channels and then commits to an answer. That pattern can transfer to meetings where speakers overlap, call-center analysis where transcripts are noisy, or video agents that need to remember who did what earlier. The watch items are weight availability, benchmark adoption, and whether downstream suites start treating long-horizon identity as a standard multimodal capability.

[PAUSE]

## [26:13] AgenticSTS Gives Long-Horizon Agents a Bounded-Memory Testbed

[NOVA]: AgenticSTS, from AlayaLab, gives long-horizon LLM agents a bounded-memory testbed with a typed retrieval contract. It is trending on Hugging Face's daily papers feed with forty-three upvotes, and it tackles a messy evaluation problem: when an agent improves, was it the memory layer, the retriever, the summarizer, the model, or just more tokens?

[ALLOY]: AgenticSTS treats memory as a typed interface rather than a free-form blob. The agent issues typed queries against a bounded memory store, and the harness rebuilds fresh prompts from typed slots on each step. A hard retrieval-token ceiling keeps comparisons like-for-like, so swapping a retriever, summarizer, or eviction policy changes that component without silently giving the agent more context budget.

[NOVA]: That isolation matters because long-horizon agents often fail slowly. A memory layer may look useful during short tasks and then degrade as summaries lose details, retrieval pulls stale context, or eviction removes the wrong state. Typed slots make the failure easier to attribute. If a decision task needs a user preference, prior action, environmental fact, or goal state, the memory interface can ask for that type directly instead of replaying everything.

[ALLOY]: The integration angle is small enough to borrow. Teams can design internal memory layers around typed queries, bounded retrieval, and prompt assembly per step, then evaluate each component independently. AgenticSTS is useful less because it promises one perfect memory system and more because it gives builders a way to compare memory policies without conflating every moving part. The next thing to watch is whether open-source agent frameworks adopt typed retrieval as a standard memory evaluation surface.

[PAUSE]

## [28:02] GitHub Project Radar: DeusData/codebase-memory-mcp

[NOVA]: DeusData's codebase-memory-mcp is a high-performance Model Context Protocol server that indexes a codebase into a persistent knowledge graph and answers dependency-style questions across one hundred fifty-eight languages. It ships as a single static binary with no external dependencies, which makes it easy to place next to an agent runner without standing up a separate search service.

[ALLOY]: The headline mechanism is graph-backed code memory. Instead of asking an agent to grep every time it needs context, the MCP server can answer questions like where a symbol is used, what depends on a function, or which areas of the project connect to a feature. Sub-millisecond query claims are especially useful for agent loops because repeated context lookup can otherwise dominate latency and token spend.

[NOVA]: The integration angle is direct: register it as an MCP tool inside an OpenClaw, Codex-style, Hermes, or Claude Code workflow and let the agent query code relationships before proposing edits. That can reduce prompt bloat because the agent asks for the relevant slice instead of stuffing broad project context into every turn.

[PAUSE]

## [28:50] GitHub Project Radar: PrefectHQ/fastmcp

[ALLOY]: PrefectHQ's FastMCP is a Pythonic framework for building MCP servers and clients with minimal boilerplate. It wraps transport, discovery, and tool exposure so a Python function can become a callable agent tool in a handful of lines.

[NOVA]: The useful mechanism is ergonomic protocol wrapping. MCP is powerful, but teams often stall when every internal service needs custom protocol handling before an agent can call it. FastMCP turns the Python function boundary into the tool boundary, which lowers the cost of exposing internal APIs, data transforms, schedulers, and operational helpers to an agent stack.

[ALLOY]: Hermes, Claude Code, and other MCP-aware harnesses benefit because custom tools can be shipped quickly without inventing a one-off integration pattern. For teams already running Python services, FastMCP is the short route from a useful function to a structured tool call an agent can discover and invoke.

[PAUSE]

## [29:28] GitHub Project Radar: microsoft/mcp-for-beginners

[NOVA]: Microsoft's MCP for Beginners is an open-source learning track for Model Context Protocol across .NET, Java, TypeScript, JavaScript, Rust, and Python. It walks developers from a first MCP server toward secure and scalable deployment patterns.

[ALLOY]: The mechanism here is team alignment rather than runtime speed. MCP touches tool schemas, authorization, transport choices, and agent behavior. A cross-language curriculum lets a team learn the protocol in the language their stack already uses, so the first internal tool does not arrive with mismatched assumptions about security, schema design, or deployment.

[NOVA]: The integration angle is onboarding. Before adding a new tool surface to a production agent, teams can run through a language-specific track and establish shared patterns. That reduces the odds that every group builds its own incompatible MCP server style.

[PAUSE]

## [30:02] Local LLM Spotlight: Ollama .31.1

[NOVA]: Ollama .31.1 improves the Gemma 4 path on Apple Silicon, with generation up to ninety percent faster on a coding-agent benchmark when multi-token prediction routes through the Metal backend. The release keeps the usual local ergonomics: one run command, automatic weight fetch, and an OpenAI-compatible endpoint for tools that already talk to local servers.

[ALLOY]: The practical angle is M-series Macs. If Gemma 4 can produce tokens much faster locally, agent loops that repeatedly round-trip through the model feel less stalled. Pulling Gemma 4 through Ollama and driving a one-thousand-token generation through the compatible endpoint gives Mac users a quick way to compare it against their prior local default.

[PAUSE]

## [30:28] Extra Research Candidate: TestEvo-Bench

[NOVA]: TestEvo-Bench evaluates test and code co-evolution rather than isolated test generation. The benchmark executes candidate tests against the parent commit and checks coverage on patched lines, so agents are scored on runtime correctness and semantic linkage to the code change, not textual similarity to a reference answer.

[ALLOY]: That matters for coding agents because real engineering changes often require tests that capture new behavior. A model that writes plausible tests but misses the changed path should not get credit. TestEvo-Bench gives teams a sharper way to evaluate whether an agent understands the patch well enough to update the validation surface around it.

[PAUSE]

## [31:05] Extra Research Candidate: 128GB Apple Silicon local-model sweet spot

[NOVA]: A LocalLLaMA community thread is testing whether twenty-seven to thirty-five-billion-parameter models are the practical sweet spot on a one-hundred-twenty-eight-gigabyte M3 Max. The poster compares Q4_K_M GGUF and four-bit MLX weights against seventy-billion-plus models while measuring tokens per second and prompt-eval latency at full context.

[ALLOY]: The useful point is that maximum model size may not be the best daily driver. On unified-memory Macs, a mid-sized model can deliver better responsiveness for coding loops than a larger model that technically fits but responds too slowly. That reinforces the procurement lesson from the local-LLM guide: throughput and latency matter as much as parameter count.

[PAUSE]

## [31:42] Extra Research Candidate: Going local is life changing

[NOVA]: Another LocalLLaMA thread describes replacing a hosted coding assistant with a locally served model exposed through an OpenAI-compatible endpoint. The author found that for code-prep workloads, lower network round-trip latency outweighed the loss of frontier-class reasoning.

[ALLOY]: That is a useful reminder for agent stacks. Not every coding task needs the strongest model available. If the work is preparing code, summarizing context, reshaping snippets, or making small local edits, a fast local endpoint can feel better than a smarter hosted model that waits on the network every turn.

[PAUSE]

## [32:17] Practical queue

[NOVA]: Hermes 7.1 makes named multi-model ensembles and evidence-backed goal completion part of the normal agent surface; Claude Code .193 remains central to the terminal coding-agent debate as security teams scrutinize outbound context.

[ALLOY]: ZCode, Kimi K2.7 Code, and Leanstral 1.5 widen the model-and-harness menu: Chinese coding harnesses, Copilot-native MoE coding, and local Lean proof generation all moved forward.

[NOVA]: WebBrain, Safari MCP, FastMCP, codebase-memory-mcp, and Microsoft's MCP curriculum show the tool layer getting more practical: browsers, code graphs, and internal services are becoming callable agent surfaces.

[ALLOY]: RECONTEXT, Senior SWE-Bench, AgenticSTS, TestEvo-Bench, DramaSR, Program-as-Weights, ghealth, Ollama, and the local-model threads all point at the same build pressure: agents need better evaluation, faster local loops, cleaner memory, and more private data paths.

[NOVA]: For more detail on the releases, projects, papers, and source material behind the coverage, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.
