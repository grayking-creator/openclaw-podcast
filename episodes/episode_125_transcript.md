# AgentStack Daily EP125 — Kimi K3.1 Pro Brings 1M-Token Context to OpenRouter

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily.

[NOVA]: A million-token context window just landed on OpenRouter through Kimi K3.1 Pro. Moonshot’s flagship open-weight reasoning model can take text, images, and video together, putting whole codebases, interface screenshots, and recorded product behavior inside one working context. That’s an enormous amount of material—but long memory only matters if the model can reason across it without losing the plot.

[ALLOY]: And the surrounding releases make that more than a giant-number headline. Flint brings a thirty-nine-point-eight-billion-parameter coding agent toward local NVIDIA and Apple Silicon systems. Timestral forecasts demand, sensor readings, or market activity locally while returning probability ranges instead of one suspiciously confident number. Anthropic has opened the operating-system sandbox behind the terminal-based AI coding agent Claude Code, and Microsoft has shown one thousand twenty-four agents coordinating without a central boss. Today: Hermes Agent .22.5, .22.4, and .22.3; Kimi K3.1 Pro; safer agent execution; focused application decisions; local coding and forecasting models; and a very large experiment in agents organizing themselves.

[PAUSE]

## [02:00] Agent Stack Release Readout: Hermes Agent .22.5, .22.4, and .22.3

[NOVA]: Nous Research shipped Hermes Agent .22.5 on October twenty-second, following .22.4 and .22.3. The newest patch gathers eighty-one merged pull requests, thirty closed issues, two hundred thirty-one non-merge commits, and changes across eight hundred four files. That work reaches the command-line experience and installers, the Microsoft Store app, Docker, and Hermes Cloud. The most consequential addition is pluggable delegation. Hermes can send work to subagents through model maps or profiles, and the routing can change from one session to another. A session could direct coding toward one profile and research toward another without hard-wiring every backend into the main application. Delegation becomes configurable rather than a permanent architectural choice. The plugin system also expands: plugins can expose slash commands with selectable options, serve Hermes through the Model Context Protocol, and import existing agents. When setup detects another agent, it can offer an importer instead of forcing someone to reconstruct that configuration manually. That combination makes the plugin boundary more useful in both directions: Hermes can consume extensions, and it can present its own capabilities to other compatible applications. It also creates room for narrower subagents that carry different instructions or model characteristics while the main session remains intact.

[ALLOY]: That’s a substantial patch, and the desktop changes make the plumbing visible. Desktop gains one-click plugin installation, tier badges, and drag-to-pin controls in its sidebar. Sign-in moves to a plain device-login flow; guests on the free tier can transfer their work into an account; and the interface shows which account is active. Connectors now offer sign-in directly instead of quietly opening a guest session. Usage-window plans add gauges, limit cards, and a recovery path for switching models. Those pieces reduce the little ambiguities that make an agent feel unreliable: which identity is active, where the session belongs, which plugin is installed, and which model profile receives the work. They also matter when a tool moves from one person’s experiment into a shared environment, because invisible account state and unclear limits become operational problems quickly. Model maps deepen that shared-environment story: one session can delegate without pretending every task deserves the same model or cost profile. Nous says the next milestone, .23, will contain curated notes for the accumulated changes. For now, .22.5 is the concrete release: broader delegation, more capable plugins, clearer identity handling, and updates distributed across every major Hermes surface.

[PAUSE]

## [02:35] OpenRouter lists Kimi K3.1 Pro with a 1M-token context window

[ALLOY]: One million tokens sounds absurdly large. What does Kimi K3.1 Pro actually accept, and where can people use it?

[NOVA]: OpenRouter now lists Kimi K3.1 Pro as Moonshot AI’s flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3. Its context window is exactly one million forty-eight thousand five hundred seventy-six tokens. It accepts text, images, and video, then produces text. That combination is unusually relevant to long-horizon software work. A coding agent could receive a large repository, design documents, screenshots of a failing interface, and video showing the behavior through one model surface. Outside coding, the same input mix could connect a long document archive with diagrams, recorded demonstrations, or visual evidence. The model still has to identify what matters; a million tokens don’t automatically produce a coherent answer. But the capacity reduces the need to discard material before the model has seen it. OpenRouter provides API access now, making this a model applications can route through rather than a future availability promise.

[ALLOY]: And the price tells us what that large window could mean in practice. OpenRouter lists prompt tokens at two dollars per million, completion tokens at ten dollars per million, and cached input reads at twenty cents per million. Cached reads matter when an agent repeatedly revisits the same repository or documentation set: stable material can remain useful across turns without being billed like entirely new input every time. The exciting use isn’t stuffing a million tokens into every request. It’s keeping a long-running investigation intact when the work genuinely spans code, visual evidence, prior decisions, and tool results. That could include tracing a defect across several services while comparing the implementation with product recordings and historical design choices. The costs also make selective reuse more attractive than repeatedly transmitting a giant context from scratch. Kimi K3.1 Pro is available through OpenRouter, carries Moonshot’s open-weight description, and places long context beside multimodal input. Now its reasoning quality across that distance has to earn the giant window.

[PAUSE]

## [03:42] Anthropic Opens Its Agent Sandbox Beyond Containers

[NOVA]: Anthropic has open-sourced sandbox-runtime, shortened to S-R-T, the operating-system-level sandbox used behind the terminal-based AI coding agent Claude Code. It can restrict file and network access for AI agents, Model Context Protocol servers, and command-line tools without requiring each workload to run in a container. On macOS, it relies on Seatbelt, Apple’s built-in sandboxing system. On Linux, it uses bubblewrap. Anthropic’s agent-isolation layer is now available for inspection and reuse outside Claude Code.

[ALLOY]: That gives developers another option when they need tighter boundaries but don’t want a full container around every process. A tool can run as a normal operating-system process while the sandbox narrows which files it can touch and which network destinations it can reach. That can fit desktop agents particularly well, because they often need selective access to a working folder, compiler, or local utility without receiving broad access to the whole machine. Containers still provide valuable isolation and packaging, so they’re not suddenly obsolete. This is a different boundary with a lighter footprint and closer integration with the host operating system.

[NOVA]: Right, and “sandboxed” shouldn’t become a magic word. The policy still has to grant enough access for useful work while denying everything unrelated. An agent editing one repository may need package downloads or a compiler, but it doesn’t need unrestricted access to personal files. Network controls matter for the same reason: a tool may legitimately call one service without needing the entire internet. S-R-T exposes a common project across macOS and Linux even though the operating-system enforcement underneath differs.

[ALLOY]: The open release matters because agents increasingly execute code, launch utilities, and connect to tool servers rather than merely produce text. Anthropic is letting others inspect and reuse an isolation layer built for that reality. That can shorten the distance between a prototype that trusts everything and a product with explicit boundaries. It also gives tool authors a shared sandbox surface instead of leaving every application to invent its own wrapper around operating-system controls. The next generation of agent software won’t be judged only by what it can do; people will care just as much about which files, services, and credentials remain outside its reach.

[PAUSE]

## [04:44] OpenAI launches a Decisions API for focused app decisions

[NOVA]: OpenAI has launched a Decisions API, a dedicated interface for automated choices inside applications. The company describes it as fast, focused, and low-cost. Think about moments where software needs one bounded judgment: choosing which option to display, routing a request, or selecting the next action. Those tasks don’t necessarily need a sprawling autonomous workflow. They need a decision delivered quickly enough to sit directly in the path of a live product.

[ALLOY]: I like the narrower framing. “Put an agent everywhere” can become an excuse to wrap a simple choice in unnecessary machinery. A focused decision interface gives product teams a smaller component to place at one specific point. The value will depend on response time, consistency, and cost under live traffic, because an impressive answer that arrives late can still damage the experience. A routing or personalization choice may happen millions of times, so small differences in latency and price accumulate quickly.

[NOVA]: It also separates deciding from executing. The API can choose an option while the surrounding application retains control over what happens next. That can make the AI contribution easier to identify than it would be inside a broad agent loop. A retailer might use one result to choose an offer, while a support system routes a request to the right queue and keeps the actual business action inside existing software. Product rules still matter, especially where one bad decision affects money, access, or people. OpenAI is aiming across application types rather than naming one narrow vertical, so actual adoption will show whether the strongest fit is personalization, operations, request routing, or something less obvious.

[ALLOY]: And it lands beside Kimi’s enormous context window as an almost comic contrast. One product says, “Bring the whole world into context.” The other says, “Give me the exact choice that needs making.” Both can be useful. AI infrastructure increasingly stretches from giant reasoning surfaces down to a tightly scoped decision embedded between two ordinary application steps. That smaller surface may also make it easier for a product team to understand exactly where an automated judgment changed the customer experience.

[PAUSE]

## [05:29] Recursive’s Flint brings a 39.8B coding agent to local stacks

[NOVA]: Recursive has released Flint under Apache Two, with Unsloth providing the checkpoint, configuration, tokenizer, chat template, serving kit, and quantized GGUF variants for NVIDIA and Apple Silicon runtimes. Flint is a text-based mixture-of-experts coding-agent model with thirty-nine-point-eight billion total parameters, but only about two-point-five billion activate for each token. Each mixture layer routes a token through six of two hundred fifty-six specialists, plus one shared expert that always participates. That keeps broad model capacity while limiting the computation used for each step. Flint supports reasoning, multi-turn tool use, and OpenAI-compatible tool calls. Its intended work includes investigating repositories, fixing bugs, implementing features, writing tests, and continuing after it sees tool results. Recursive reports fifty-four-point-nine percent on Terminal-Bench two point one, eighty-nine-point-seven percent on SWE-bench Pro version two, and seventy-four-point-two percent on SWE-bench Verified. Those are publisher results, and the card cautions that evaluation setups, precision, and inference runtimes can change outcomes.

[ALLOY]: That active-parameter count is what makes local use compelling. Thirty-nine-point-eight billion is large, but each token engages a much smaller slice, while quantized builds further reduce memory requirements. The model card also explains that Flint’s Terminal-Bench result treats solutions obtained through web retrieval as unsuccessful, while some developer figures may apply different rules. So the headline scores stay attached to their setup; they aren’t universal promises. What remains concrete is unusually useful: open weights, local variants, multi-turn tools, and a model designed to act on software rather than merely finish a line. Local execution can keep a private repository closer to the machine running the agent and reduce dependence on a hosted coding service. It doesn’t make the output harmless—Flint can still write faulty code or choose an inappropriate tool call. Pairing it with the explicit access boundaries from Anthropic’s sandbox work is much more convincing than treating either the model or the sandbox as sufficient alone.

[PAUSE]

## [06:45] Mistral’s Timestral-209M brings local probabilistic forecasting

[ALLOY]: Coding agents get most of the attention, but Timestral may reach a completely different class of application. What does a two-hundred-nine-million-parameter forecasting model buy you?

[NOVA]: Mistral’s Timestral-209M predicts future values from time-series data without task-specific retraining. It’s the largest of four documented sizes, ranging from five million to two hundred nine million parameters. It handles one series or several related series and can incorporate covariates—extra signals that help explain the target. Some come from the past; others are known in advance, such as calendars, planned prices, or scheduled events. The model accepts up to thirty-two thousand seven hundred sixty-eight historical steps and forecasts one thousand twenty-four steps in one pass, with longer horizons processed in blocks. It groups thirty-two steps into patches and embeds both observed values and indicators for missing observations. Its twenty-one quantiles provide a median forecast plus a range of lower and higher possibilities, which is more useful for inventory, capacity, energy, or sensor planning than one falsely precise number.

[ALLOY]: Mistral reports leading zero-shot results on GIFT-Eval, TIME, and fev-bench, including lower error than TimesFM-3 on GIFT-Eval. Those figures come from Mistral, with the checkpoint and source code available for running the model and reproducing its evaluations. Timestral works through PyTorch on CPUs or GPUs under a Modified MIT license. Okay, that’s actually a strong local package: one or many related signals, known future events, missing-value awareness, and explicit uncertainty on ordinary processors. A warehouse can combine sales history with planned promotions; a factory can connect multiple sensors; an energy service can expose a likely range instead of pretending weather and demand will obey one line. Flint turns local code into actions, while Timestral turns local histories into probability ranges. Neither needs to become a chat interface to be valuable.

[PAUSE]

## [08:26] OpenAI and Poland’s NASK team up on AI safety

[NOVA]: OpenAI and Poland’s NASK announced a partnership on October twenty-third covering AI safety, security, and technical research. NASK is Poland’s national cybersecurity institution, so this connects an AI company directly with an organization responsible for strengthening the country’s digital resilience. The immediate development is institutional cooperation around safeguards and security research, not a new product.

[ALLOY]: That distinction matters, but the pairing is still worth attention. Model companies understand their systems; national cybersecurity institutions live closer to adversaries, incident response, and public infrastructure. Those perspectives overlap without being interchangeable. Work between them could produce security methods or safeguards shaped by real operational threats rather than abstract risk discussions. The useful evidence will be the technical research and protections that emerge, especially if organizations beyond the partnership can apply them to systems already exposed to attacks.

[NOVA]: And national infrastructure raises different stakes from a consumer assistant. Reliability, incident handling, and resilience sit beside model behavior because failures can affect essential services and public institutions. NASK brings that environment into the collaboration. Poland also becomes a direct participant in shaping how AI security work meets national cyber defense, rather than merely receiving practices developed elsewhere.

[ALLOY]: Exactly. AI safety often sounds detached from the networks and services people already depend on. Connecting it to a national cybersecurity body puts the conversation nearer those systems. The collaboration could also expose tensions between rapid deployment and the slower discipline required around critical infrastructure. If the partnership translates research into concrete defenses, its influence could travel well beyond Poland.

[PAUSE]

## [09:06] Research digest: METTA Lets Agents Adapt During the Task

[ALLOY]: Here’s one I find genuinely exciting: METTA lets an agent learn while it’s already attempting an unfamiliar task instead of depending only on training completed beforehand. How does it keep that from becoming aimless trial and error?

[NOVA]: METTA combines adaptation during the current task with a compact memory of earlier attempts. Recent interaction changes the agent’s behavior, while summaries of past episodes carry useful experience into the next attempt. Researchers evaluated it on unseen Meta-World control tasks and long-context PointMaze environments where rewards were sparse. On held-out Meta-World tasks, METTA exceeded fifty percent success while keeping training expense and wall-clock time low. In PointMaze, it beat transformer-based baselines and explored in a more structured way.

[ALLOY]: So the appeal isn’t endless retraining. It’s a limited learning budget applied while the agent works, with enough retained history to avoid starting from zero each time.

[NOVA]: Benchmark environments are cleaner than the physical and software worlds agents eventually face. Even so, adapting during a task could be crucial when the exact challenge wasn’t represented in the original training distribution.

[PAUSE]

## [10:07] SpaceX Super Intelligence opens a Grok partner network

[NOVA]: SpaceX Super Intelligence has opened an official partner network for companies building products, services, and integrations around Grok. The program separates partners into two groups. Transformation Partners help customers deploy the Grok platform across an enterprise. Marketplace Partners build plugins and integrations connecting Grok to tools customers already use. More than one hundred thirty companies participated during early access, and engineers at over thirty organizations have trained through a Forward Deployed Engineer accreditation program. Named launch partners include Bain and Company, Databricks, NVIDIA, Snowflake, Galatiq, Adapter Group, AHEAD, and Alpha FMC.

[ALLOY]: So this is less about another model launch and more about building a delivery channel. Those partners cover enterprise transformation, data infrastructure, governance, audit trails, and business-specific context—the pieces that decide whether a model reaches recurring work or remains trapped in a pilot. Galatiq describes engineers working inside client workflows to scope and build production systems. Adapter says it can carry a customer’s broader trajectory into Grok Bot and Grok Build, so a new interaction starts with mission context rather than only immediate working memory. Databricks and Snowflake bring data surfaces that already sit inside large organizations, while NVIDIA adds infrastructure reach. The partner count is notable, but production use is the harder measure. Integrating enterprise data and controls, preserving accountability across several companies, and keeping the resulting system useful over time will decide whether the network becomes substantial.

[PAUSE]

## [11:27] Research digest: A Training Trick Makes Repeated AI Inference Less Memory-Hungry

[NOVA]: BeNice is a post-training method for models that repeatedly pass information through the same layers. These looped networks can improve output without adding a fresh set of learned parameters for every pass, but each repetition has traditionally created its own key-value cache—the stored information about earlier tokens. Memory consumption therefore grows with every loop.

[ALLOY]: BeNice trains the model so the final pass’s cache can be broadcast back into the first pass, allowing the repetitions to share one compatible cache. Researchers report quality matching ordinary fine-tuning with separate caches. That could preserve the benefit of repeated computation without duplicating token memory at every depth, and the method can complement other sequence-memory reductions.

[NOVA]: That’s a meaningful efficiency gain if it carries into larger deployments. Looped models trade additional computation for stronger reasoning while keeping their learned parameter count fixed; shared caches make that trade less punishing on memory. More repetitions could then fit on the same hardware without multiplying stored token state at the same rate.

[PAUSE]

## [12:27] DeusData Brings Local Code Intelligence to AI Agents

[NOVA]: DeusData’s codebase-memory-mcp gives developers and AI agents a local graph connecting code, documentation, and infrastructure. The newest release is .12.1, dated October sixteenth, and the repository was updated again on October twenty-fourth. GitHub reports forty-seven thousand four hundred thirty-eight stars. Its purpose is persistent code intelligence: functions, documents, infrastructure, and their relationships remain connected instead of being rediscovered as isolated snippets in every prompt.

[ALLOY]: That changes what an agent can ask. Instead of searching only for matching text, it can follow relationships—what calls a function, which component depends on it, or which documentation belongs to the same subsystem. The project includes CBM Lens, Model Context Protocol tools, agent integrations, and change-aware test selection. That last feature identifies tests related to a change, potentially narrowing attention to the affected surface without claiming that unrelated coverage no longer matters.

[NOVA]: Local operation is attractive for repositories that teams don’t want copied into a remote context service. A persistent graph can also outlive one chat session, giving later agent work access to previously mapped structure. That continuity could help when a change crosses application code, deployment files, and design documentation instead of staying inside one language or directory. The project still has to track changes accurately; stale relationships could send an agent toward outdated conclusions. But its scale shows strong demand for something richer than repeated file search.

[ALLOY]: It also explains why knowledge graphs keep resurfacing next to long-context models. Kimi can hold a huge amount of material, while a graph supplies explicit structure between the pieces. They solve different problems. An agent can use the graph to find the connected slice, then use long context to reason across code, documentation, and surrounding evidence without flattening the whole repository into a bag of text.

[PAUSE]

## [13:21] Microsoft’s Agensh coordinates 1,024 agents without a central boss

[ALLOY]: One thousand twenty-four agents with no central orchestrator sounds either brilliant or like the fastest possible route to a very crowded group chat. How did Microsoft Research coordinate them?

[NOVA]: Agensh lets workers self-organize through three shared surfaces: a Git repository, a chat channel, and a findings board. No single controller assigns every task. In Microsoft’s reported ProgramBench experiment, the open-source harness scaled from one agent to one thousand twenty-four while staying within a six-hour budget. Git carries evolving work, chat supports communication, and the findings board gives workers a place to record discoveries others can use.

[ALLOY]: The absence of one boss is more interesting than the agent count. A central planner can become a bottleneck when hundreds of workers wait for assignments or return results. Shared workspaces let agents discover tasks and react to one another more directly. But decentralization can also create duplicated work, conflicting edits, neglected tasks, or groups converging on the same wrong assumption. ProgramBench demonstrates a coordination design; it doesn’t prove every difficult problem benefits from a thousand workers. Communication itself consumes time and context, so adding agents can eventually add more noise than useful labor.

[NOVA]: Still, Microsoft has released a concrete framework for examining those tradeoffs. Teams can inspect how agents divide labor through shared code, conversation, and recorded findings instead of treating mass coordination as a proprietary stage demo. The thousand-agent headline earns attention. The reusable contribution is a system where coordination emerges from common work surfaces rather than one master process trying to understand and schedule everything.

[PAUSE]

## [14:11] Cognition Open-Sources a Vulnerability-Fixing Agent Plugin

[NOVA]: Cognition has open-sourced the Devin Vulnerability Fixes plugin in response to critical remote-code-execution flaws affecting PHP, Node.js, and self-managed GitLab deployments. The MIT-licensed release contains three agent skills that inventory affected systems, apply patches and tests, then open a separate pull request for each repository. That turns a broad security event into reviewable changes attached to individual codebases instead of one opaque batch operation.

[ALLOY]: Separate pull requests are the right shape for engineering review, but automation doesn’t make a security fix self-approving. The useful contribution is reach: an agent can search across many repositories, identify exposure, prepare changes, and preserve the same review trail teams already use. That matters when a remote-code-execution flaw creates pressure to move quickly across a large software estate. A company with dozens of services may have several affected dependency paths, different build systems, and different owners; preparing one isolated change per repository gives those owners something concrete to inspect. The decisive question remains whether each proposed fix matches the affected project and closes the exposure without breaking surrounding behavior. Cognition’s plugin compresses discovery and patch preparation; human accountability still belongs in the merge decision.

[PAUSE]

## [14:49] Letta Tutorial Builds Stateful Engineering Copilots

[ALLOY]: Letta’s engineering-copilot tutorial tackles a frustration every long-running assistant eventually creates: why does it behave as if the project is new whenever the conversation changes?

[NOVA]: The tutorial builds around inspectable core memory, giving the copilot a visible place to retain project facts instead of hiding everything in opaque conversation state. It adds archival vector retrieval, which finds older material by meaning rather than requiring the same words. A question about an authentication decision, for example, can retrieve a relevant design note even when its phrasing differs. The copilot can also call custom tools, stream responses, share state among specialized agents, and carry portable workflows between environments.

[ALLOY]: Shared state is where the design becomes more than a memory demonstration. One agent can specialize in repository work while another handles documentation or infrastructure, yet both operate against common project context. The architecture preserves decisions, retrieves relevant history, and connects actions to that memory. A copilot could remember why a dependency was rejected, which service owns a data contract, or what constraint shaped an earlier implementation, then bring that history into later work. Persistent context can preserve mistakes too, which is why inspectability matters. If people can see and correct what the copilot remembers, state becomes a maintained project resource rather than an accumulating mystery.

[PAUSE]

## [15:55] GitHub Project Radar

[NOVA]: Nanobot leads at forty-nine thousand three hundred thirty-nine stars, up seven hundred seventy-eight in thirty days. Release .3.5 shipped in September, and the repository was active again October twenty-fifth. It’s an ultra-lightweight, self-hosted Python agent framework with a web interface, tools, memory, Model Context Protocol support, automation, chat integrations, and multi-agent workflows. Ahujasid’s MCP for Blender moves the same ecosystem into three-dimensional creation. The community plugin has thirty-two thousand two hundred ninety-three stars, up two thousand nine hundred seventy-eight in thirty days—a ten-point-two-percent rise—and was updated October twenty-fourth.

[ALLOY]: Those projects stretch agents in opposite directions: Nanobot supplies a persistent self-hosted layer, while MCP for Blender opens a concrete creative environment. FastMCP provides connective tissue. The Python framework for building Model Context Protocol servers and clients has twenty-eight thousand one hundred ninety-seven stars, up six hundred eighty, and shipped release four point one in October. It gives applications a direct way to expose tools and data. Nanobot organizes agents, MCP for Blender gives them a specialized control surface, and FastMCP helps wire those capabilities into compatible clients.

[PAUSE]

## [16:58] Model Discovery Check

[NOVA]: Kimi K3.1 Pro is the long-context selection: one million forty-eight thousand five hundred seventy-six tokens, with text, image, and video input producing text. Moonshot describes it as an open-weight multimodal reasoning model built for long-horizon coding, and OpenRouter provides API access. Listed rates are two dollars per million prompt tokens, ten dollars per million generated tokens, and twenty cents per million cached-input tokens.

[ALLOY]: Flint brings a different kind of accessibility. Its Apache-licensed weights total thirty-nine-point-eight billion parameters, with roughly two-point-five billion active for each token. It’s a text-based coding-agent model supporting reasoning, multi-turn tools, and OpenAI-compatible calls. Unsloth supplies quantized GGUF variants prepared for NVIDIA and Apple Silicon systems, while the model card notes that evaluation outcomes can change with precision and runtime.

[NOVA]: Timestral-209M is the forecasting selection, with two hundred nine million parameters and local PyTorch execution on CPUs or GPUs. It supports single and related time series, known-future and past-only extra signals, and probabilistic predictions across twenty-one quantiles. Mistral reports leading zero-shot results across several forecasting evaluations and released the checkpoint and source code under a Modified MIT license.

[PAUSE]

## [17:51] Local LLM Spotlight

[ALLOY]: DeepSeek V4.1 Flash 1017 is trending on Hugging Face with two thousand eight hundred fifty-six likes and more than eighty-five thousand downloads. It’s listed for image-and-text input producing text, with transformer and safe-tensor support, MIT licensing, evaluation results, compatible hosted endpoints, and weight formats including eight-bit and FP8. Those formats offer different routes for hardware with different memory budgets, while the multimodal input makes the model relevant where pictures and written instructions need to inform one response. The attention around the listing is substantial, and its combination of downloadable weights, endpoint compatibility, and lower-precision formats gives local and hosted deployments several ways to approach it.

[PAUSE]

## [18:28] Extra Research Candidates

[NOVA]: “Usage Metrics API Adds Usage from Tools Like OpenCode” closes a reporting gap in GitHub Copilot analytics: model activity from additional developer tools, including OpenCode, now appears in usage reports. Connect that with “Microsoft Open-Sources Agensh: A Multi-Agent Harness for One Thousand Twenty-Four Agents,” and measurement has to follow work across tools and coordinated workers rather than remain attached to one interface.

[ALLOY]: “Google Cloud Launches Agent Compute Engine: A MicroVM per AI Agent” addresses the execution side of the same problem. Each agent receives a hardware-isolated micro-virtual machine with credentials kept outside it; the service already runs Gemini agents and is expected to enter preview in the coming months. Agensh coordinates large groups, Agent Compute Engine isolates individual workers, and the expanded usage API helps organizations see where model activity occurs.

[PAUSE]

## [19:02] Closing

[NOVA]: For the model listings, project repositories, research papers, release details, and supporting material, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.
