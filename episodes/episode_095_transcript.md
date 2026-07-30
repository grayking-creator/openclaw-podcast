# AgentStack Daily EP095 — Agent Stack Release Readout: OpenAI Codex rust-v0.146

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily.

[NOVA]: OpenAI shipped a significant update to its terminal-based AI coding agent on July 29 — version 0.146 — and the changes go well beyond a version bump. Teams can now pull plugins from Amazon Bedrock and the terminal-based AI coding agent Claude Code marketplaces, connect a thin client to a heavier remote host over WebSocket, and fork conversation threads with paginated history. Separately, OpenAI also published two settings for GPT-5.6 that tripled its ARC-AGI-3 reasoning score without retraining. Liquid AI released two open-weight CPU-friendly encoders with an 8,192-token context window. And nanobot hit 46,000 GitHub stars as a self-hosted agent framework. Today you'll hear those four releases, ComfyUI's streaming video pipeline, FCC rules tightening around foreign robotics, two robot-training papers pointing toward cheaper hardware-free pipelines, and AllenAI positioning for planetary-scale geospatial inference. Useful AI work is spreading into remote workstations, local CPUs, edge boxes, robot-control loops, and specialist services that can be observed and governed in ordinary production environments. Let's get into it.

[PAUSE]

## [02:00] Agent Stack Release Readout: OpenAI Codex rust-v0.146

[NOVA]: OpenAI shipped Codex 0.146 on July 29, and the release covers a lot of ground. The most concrete win for distributed teams is the WebSocket bridge — the app-server can now connect to a Code Mode host running on a different machine rather than expecting everything to execute locally. A thin client on your laptop can drive tools, plugins, and approvals inside a heavier remote environment while keeping the familiar Codex control surface in front of you. That separates interaction from execution cleanly: the laptop handles the conversation, while the remote workstation supplies the compute, repositories, credentials, and installed tools. Teams that already provision cloud workstations no longer need a hand-built relay just to make a local interface reach them, and a reconnecting client can return to the same named work rather than rebuilding the entire session and tool state from scratch.

[ALLOY]: That's huge for shops running cloud workstations. Instead of streaming an entire remote desktop, you get a lighter bridge that speaks directly to Codex. And it layers into the plugin work, which is where the bigger shift lands. Codex now supports the Agent Plugins manifest format and can pull packages from Amazon Bedrock and Claude Code marketplaces alongside OpenAI's own workspace publishing flow. One manifest definition travels between runtimes instead of needing separate configuration for each host. The important unit becomes the package — its tools, skills, resources, and metadata — rather than the particular assistant that happens to load it. That makes a shared internal plugin easier to distribute across teams using different coding agents.

[NOVA]: You also get executor-provided skills now, with their associated resources readable from within the session. Sessions can be named when they start or clear, important threads can be marked for quick return, and you can switch between side conversations without closing them. Forkable threads carry paginated history, including temporary forks that stay out of the main thread list. Under tight context budgets, more skills are retained and the terminal warns when the catalog has to be truncated. Proxies are honored across authentication, plugin downloads, MCP authorization, remote execution, WebSockets, redirects, and local model connections. MCP servers and app tools refresh after authentication or configuration changes, reconnecting closed services without disturbing healthy ones. Terminal handling also got fixes for Windows navigation keys, nonblocking interrupts, hyperlinks, narrow layouts, and reliable shutdown of sandboxed process trees.

[ALLOY]: So this is both a distribution release and a reliability pass. It doesn't create a coordinated multi-agent protocol, but an organization can publish one package definition across runtimes while proxy and reconnection fixes keep the tool surface alive through network changes. The release also preserves submitted messages, final responses, failed-turn errors, timestamps, and approval settings across interruptions, replay, imports, and forks. That's exactly the state you don't want disappearing during a long coding job.

[PAUSE]

## [03:03] GitHub Copilot for JetBrains adds OpenTelemetry controls and model management

[NOVA]: GitHub pushed an update to its Copilot plugin for JetBrains IDEs that gives developers explicit control over telemetry configuration and model selection. The headline is improved OpenTelemetry support — the open standard for shipping logs, traces, and metrics to whatever observability stack a team runs. Instead of accepting defaults, administrators can tune what gets sent and where it lands. That gives an engineering organization one place to compare assistant activity with application traces, repository events, and service costs. It also gives security and compliance teams a defined export path instead of forcing them to treat the coding assistant as an opaque island.

[ALLOY]: For teams already running centralized observability, that's a big deal. Copilot activity can flow into the same pipeline as application traffic — AI usage visible alongside regular logs and traces without building a separate integration. A sudden rise in agent calls, latency, or failed tool actions can be investigated with the same dashboards and retention rules used elsewhere. The update also adds clearer model management controls inside the JetBrains environment, giving developers a direct handle on which AI models are wired in and giving administrators a cleaner way to understand the surface they are supporting.

[NOVA]: And it enables MCP servers and custom agents inside Claude agent flows. MCP — Model Context Protocol — lets an AI agent call external tools and data through a uniform interface. An internal database, API, or code index that already exposes MCP becomes reachable from a Claude agent flow without custom glue. That turns the IDE into a governed entry point for company tools, with telemetry recording what the assistant touched. A specialized agent can query a private code catalog, ask an internal service for deployment state, and return the answer without forcing the developer to leave the editor. Organizations using JetBrains and VS Code will want the same model controls, tool reach, and observability policy across both.

[PAUSE]

## [04:31] Two GPT-5.6 Settings That Tripled Its ARC-AGI-3 Score

[NOVA]: OpenAI published details on July 29 showing that enabling two API settings tripled GPT-5.6's scores on ARC-AGI-3 while improving token efficiency. The puzzle-style reasoning test is designed to resist brute-force pattern matching. The weights did not change; the result came from changing how a continuing task carries state. Deployment configuration can hide or reveal capability that people may wrongly attribute to the model alone.

[ALLOY]: The first setting retains reasoning across turns, so useful work persists instead of every request starting cold. The second compacts older context, keeping earlier conclusions while reducing the token load. On a puzzle requiring several attempts, the model can preserve a discovered rule, discard dead-end prose around it, and advance instead of rediscovering the same clue. The same pattern appears in software work: an agent may inspect logs, reject one hypothesis, locate the relevant code, and then need all three conclusions several turns later. Keeping the conclusions without replaying every token is the efficiency claim in practical form.

[NOVA]: The result, per OpenAI, is higher scores with fewer tokens spent through configuration rather than retraining. It also complicates comparisons: two applications calling the same model can see different results if one preserves reasoning state and the other resets it. A benchmark report that names only the model but omits the state settings is no longer describing the full test. Those numbers are an OpenAI claim until someone reproduces them with the same task budget.

[ALLOY]: Multi-step planning, coding investigations, and agent loops share the benchmark's problem: useful state accumulates, but raw history becomes expensive. Retention plus compaction tries to preserve the first without dragging the second forever. OpenAI still needs to publish the configuration names, task budget, and full numbers before the headline can be reproduced in production.

[PAUSE]

## [06:01] Liquid AI ships two CPU-friendly long-context encoders

[NOVA]: Liquid AI released two open-weight LFM2.5 encoders on July 28, sized at 230 million and 350 million parameters. Both target long-context CPU work with an 8,192-token window. Encoders turn text into representations that downstream systems classify, compare, route, or inspect. That narrower job is why a few hundred million parameters can still be useful in production. A generative model writes the response; an encoder can decide which policy, document, or queue the request belongs to before generation begins.

[ALLOY]: Liquid AI converted causal decoder backbones into bidirectional encoders, replacing one-directional attention with full bidirectional attention, causal short convolutions with symmetric non-causal ones, and retraining with a masked-language objective. A classifier benefits from seeing both sides of a phrase, especially when an exception or sensitive field appears late in a document. The model can consider evidence from the beginning and end together.

[NOVA]: Liquid AI says the 230-million model completes an 8,192-token CPU pass in roughly 28 seconds, about 3.7 times faster than ModernBERT-base in its comparison. Those are vendor numbers, so speed will vary with hardware. The targets are classification, routing, policy linting, and personal-data detection. A support system could score a case history before routing it; a compliance service could inspect a long policy without sending text to a hosted endpoint.

[ALLOY]: With open weights, a team can adapt the encoders to its labels and deploy on one machine. The larger option offers more capacity; the smaller model fits tighter latency and memory limits. Neither replaces a generative assistant. It can sit in front of one, deciding which request is safe, which document is relevant, or which queue receives the work. Independent tests now need to confirm the CPU speed across ordinary laptops and low-cost servers.

[PAUSE]

## [07:35] ComfyUI 0.29 streams video instead of buffering it in RAM

[NOVA]: ComfyUI shipped version 0.29 on July 29. The most concrete change is in the video pipeline — until now, video transcoding buffered every frame in RAM before processing. That works for short clips, but a long or high-resolution render exhausts memory and dies mid-job. The new behavior streams the transcode instead: frames are read, transformed, and passed onward as the pipeline advances rather than accumulating until the whole clip fits in memory. Longer duration and higher resolution both multiply the old buffer, so this changes the practical ceiling of the same workstation without pretending the GPU became faster.

[ALLOY]: The second change ships to the partner nodes system. ComfyUI now sends its Job Id as a request header to partner services. For anyone integrating a third-party partner node into a workflow, that header gives the partner a clean way to correlate incoming work with the originating ComfyUI job instead of guessing from filenames or timing. If one graph launches several external requests at once, the receiving service can attach logs, billing, errors, and returned media to the correct run. Together these are plumbing fixes rather than flashy generation features, but both address real frustrations: out-of-memory crashes on long video renders, and unclear attribution when a workflow fans out to external services.

[NOVA]: The pairing is more useful than either line item sounds. Streaming keeps a long render alive; correlation makes that render diagnosable once external partner nodes join the graph. A creator who loses a ninety-minute job needs to know whether local memory, a remote service, or a particular node caused it. Version 0.29 gives that workflow less memory pressure, a better identifier across the boundary, and a clearer investigation instead of another expensive blind retry.

[PAUSE]

## [08:43] NVIDIA Jetson Gets a Venture Capitalist's Bag Endorsement

[NOVA]: NVIDIA's edge AI platform Jetson got an unusual endorsement this week. Venture capitalist Sarah Guo, founder of Conviction and co-host of the No Priors podcast, published a video on July 28 framing Jetson as a must-carry accessory for builders. NVIDIA's blog picked up the clip under the headline "Powerful Compute So Compact, It's Clutch."

[ALLOY]: The framing matters because edge AI is where a lot of practical work is heading. Robots, drones, kiosks, and inspection rigs can't always wait for a round trip to a cloud server. Jetson is NVIDIA's compact, self-contained computer built around GPU-style accelerators — small enough to fit in a bag, with enough horsepower to run modern AI models locally.

[NOVA]: For builders, the appeal is straightforward — you can prototype a model on a Jetson box without booking cloud time, and keep a similar hardware shape as you move from desk to deployment. The trade-off is the usual edge constraint: you're working within the memory and compute ceiling of a small machine, so model size and efficiency matter more than they would on a server cluster.

[ALLOY]: Here's the caveat though — this is a promo post built around a VC's video clip, not a product launch. NVIDIA's blog offers no changelog, new SKU, or updated specs. Even without new silicon, the use cases explain why Jetson keeps resurfacing. A factory camera can inspect a line without sending every frame off-site. A mobile robot can react when connectivity drops. A demonstration rig can travel to a customer instead of requiring the customer to reach a data center. Those benefits come from local inference, while the limits remain memory, power, thermals, and the size of model the compact box can sustain. Watch for an actual silicon refresh or developer kit update that turns the "clutch" pitch into something concrete to order.

[PAUSE]

## [10:21] Intel's U.S. Advanced Packaging Enables Next-Generation AI Semiconductors

[NOVA]: The semiconductor industry is moving past the era of relying on one massive chip. Advanced packaging interconnects specialized pieces so they function as a single unit for AI workloads. One piece can supply compute, another high-bandwidth memory, and another input and output, while the package moves data between them far faster than separate circuit boards could. That approach lets designers combine functions without manufacturing every component on the same process. A smaller chiplet can also be easier to manufacture than one enormous die, then several known-good pieces can be joined in the package. That can improve manufacturing flexibility because a design team can update one function without rebuilding every part of the system on the same schedule. Intel is highlighting this work at its U.S. facilities as infrastructure for next-generation AI semiconductors.

[ALLOY]: Packaging now affects performance as directly as the individual chips. The distance between compute and memory shapes bandwidth, power use, cooling, and how large a model can stay fed. It also creates a supply-chain stage after fabrication: chiplets made in different places still have to be assembled, connected, and tested with extremely dense links. Those links must carry enormous data rates without turning the package into a heat trap, so materials, placement, and cooling become part of the compute architecture. Domestic capability matters when governments and buyers care not only where a wafer was fabricated, but where the final high-value system was integrated. It can also determine whether a promising chip design can be assembled at meaningful volume instead of remaining a laboratory demonstration. Intel's post does not provide a new product, benchmark, or capacity number, so the verified news is the packaging capability and its role — not a claim that a particular accelerator became faster.

[PAUSE]

## [11:00] FCC Adds Foreign-Made Advanced Robots to Its Covered List

[NOVA]: On July 28, the FCC's Public Safety and Homeland Security Bureau added foreign-produced advanced robotic devices to the Covered List — the regulator's roster of equipment that cannot receive FCC authorization to use U.S. radio spectrum. Equipment authorization is the gate that allows radios inside a product to operate legally in the United States, so this reaches beyond a warning label or procurement preference. The move followed an Executive Branch interagency determination pointing to four risk categories: supply-chain integrity, cybersecurity, surveillance potential, and remote-control vulnerabilities.

[ALLOY]: The practical effect is a hard gate. Any advanced robot produced outside the United States cannot be authorized for sale or operation in the U.S. through the normal FCC process. There's one escape hatch: the Department of War can grant conditional approval for a specific device or device class if it's determined not to pose those risks. So this is a presumption against foreign production with a waiver path, not a blanket embargo. A company cannot solve it with a software patch after launch; manufacturing geography and the exception process now sit upstream of market access.

[NOVA]: The action is category-based, not company-based. The rule looks at where the device was made, not which company made it. U.S. subsidiaries of foreign robot makers, or U.S. brands outsourcing production overseas, can be caught depending on assembly. That is broader than naming vendors: importers, integrators, and domestic brands must trace the production path of the complete device, not merely the headquarters on the box.

[ALLOY]: The open question is scope. The public notice doesn't define an "advanced robotic device." Industrial arms, warehouse systems, research platforms, and consumer robots can carry radios, cameras, remote control, and update paths, but the notice draws no boundaries. Department of War guidance, FCC clarification, and conditional approvals will show whether this stays narrow or sweeps through consumer and research hardware. Until then, uncertainty can delay purchasing and product plans.

[PAUSE]

## [12:35] Research digest: Robot Training Without the Robot: Better Capture May Replace the Real-Hardware Anchor

[NOVA]: Robots that can fold laundry or sort objects usually need thousands of careful demonstrations collected on real hardware — slow and expensive. A cheaper alternative is UMI, a portable rig that captures motion data without needing the robot itself, but the footage is noisier and less reliable. Current practice uses cheap UMI data to pre-train a policy, then adds a small dose of real-robot demonstrations as a finishing step.

[ALLOY]: A new paper called HiFi-UMI asks a sharper question — what if the robot-free capture were just made more faithful, so the real-robot anchor could disappear entirely? The authors present HiFi-UMI as a portable capture setup designed for higher fidelity, with policies trained end-to-end on that data alone. The implicit pitch is that the binding constraint in manipulation learning isn't how many demonstrations you collect, but how trustworthy each one is.

[NOVA]: If the claim holds up beyond the authors' tasks, labs without large real-robot fleets get a cheaper on-ramp to deployable manipulation. The decisive evidence will be policies transferring from portable demonstrations to different robots, objects, and environments without that final hardware-specific correction.

[PAUSE]

## [13:38] Research digest: TurboVLA paper cuts robot-control compute to under 1 GB

[NOVA]: TurboVLA is a trending paper on HuggingFace this week that redesigns how robots turn camera views and spoken instructions into motion. Vision-language-action models usually push every visual frame through a big language model first — that gives reasoning power but burns memory and adds latency at every robot tick.

[ALLOY]: TurboVLA takes a different route. Instead of running vision through a large language model before producing actions, it fuses vision and language cues directly into the action output. The headline numbers are striking: the system runs at 32 updates per second on a single consumer RTX 4090 graphics card while using under one gigabyte of video memory. That's a meaningful unlock for hobbyists, students, and small labs — the kind of setup that fits on a desk rather than filling a server rack.

[NOVA]: The catch is that the paper's demos are bounded. Direct fusion saves memory, but the language-model stage may have supplied useful abstraction on unfamiliar scenes. The next proof is whether 32-hertz control and sub-gigabyte memory survive messier objects, longer instructions, and tasks outside the training setup.

[PAUSE]

## [14:43] HKUDS nanobot ships v0.3 as a lightweight self-hosted agent framework

[NOVA]: HKUDS shipped nanobot v0.3 on July 25, a Python framework for developers who want to run their own AI agent setup rather than rely on a hosted platform. The project describes itself as ultra-lightweight and self-hosted, and it has accumulated 46,404 GitHub stars. The repository received another push on July 30, five days after the release. There is no public changelog for 0.3, so that version number alone does not establish a new capability.

[ALLOY]: The verified picture comes from the README rather than release notes. Nanobot bundles a WebUI for talking to the agent, a tools layer for calling external functions, memory, MCP support, multi-agent workflow primitives, automation hooks, and chat app integrations in one Python package that can run on your own hardware. MCP is the meaningful connection point because it lets the self-hosted agent reach the same external tool ecosystem used by larger hosted stacks.

[NOVA]: The chat integrations and WebUI provide an interface layer without requiring a separate front end, while self-hosting keeps memory and tool calls under the operator's control. MCP means the framework can reuse an existing tool server rather than forcing every integration into nanobot-specific code. Memory and automation hooks cover work that spans more than one chat turn, and multi-agent primitives let separate roles share that local foundation. A personal agent could receive a request in chat, call an MCP-connected service, retain the result, and trigger later automation from the same package. The same components could support a small internal help desk, where one role gathers context, another calls tools, and the conversation remains on company hardware. Forty-six thousand stars show attention, not production fitness, and fresh repository activity does not reveal what changed in 0.3. The honest takeaway is the established feature surface and community traction; a claimed release delta has to wait for a real changelog.

[PAUSE]

## [16:12] GPT-5.6 is framed as an efficiency release, not a capability one

[NOVA]: OpenAI posted on July 29 framing GPT-5.6 around efficiency rather than raw capability gains. The post pitches it as delivering more useful intelligence per dollar through improvements spanning the models, inference stack, and agentic workflows. It does not identify which mechanism moved, by how much, or when a customer can use it.

[ALLOY]: That's the whole verified announcement: no public changelog, feature list, benchmark table, API detail, pricing figure, or timeline. It is positioning language rather than a feature drop. Cost per completed task matters because a cheaper token is not automatically a cheaper workflow; an agent may use more turns, tools, or retries. Throughput matters because the same quality is less useful if a queue stalls under load. Those are the numbers that can make the efficiency claim measurable. Until OpenAI publishes them, there is nothing concrete to integrate or compare.

[PAUSE]

## [17:10] OpenAI Grants Free ChatGPT Access to 100,000 Academic Researchers

[NOVA]: OpenAI announced on July 29 that it's giving 100,000 academic researchers free access to ChatGPT's most advanced AI models, with the stated goal of accelerating scientific research, collaboration, and discovery. At that scale, access could influence which assistant a large cohort of graduate students, postdocs, and faculty use for literature work, drafting, and early hypothesis exploration.

[ALLOY]: But the mechanics are still missing. The announcement doesn't name the models, eligibility criteria, distribution method, start date, or duration. Those details decide whether access reaches individual researchers, entire institutions, particular disciplines, or countries, and whether sensitive research data can be handled under institutional rules. Free access can broaden experimentation, but repeatable science still requires researchers to record the model and conditions used. The headline number, audience, and mission are confirmed; everything about who receives access and what the program includes remains open.

[PAUSE]

## [18:30] OlmoEarth Platform brings geospatial inference to planetary scale

[NOVA]: AllenAI published a post on the Hugging Face Blog on July 28 titled "The OlmoEarth Platform: Geospatial inference at planetary scale." That positions OlmoEarth as a platform rather than a single model, with geospatial inference as the core capability and planetary scale as the operating target.

[ALLOY]: Geospatial inference means the system takes geographic and remote-sensing style data and produces predictions over it. Planetary scale signals that the underlying data and compute pipeline are sized for Earth-wide coverage rather than a single city, watershed, or satellite tile. For builders, that framing matters because the hard part of geospatial AI has rarely been the model — it's been ingesting, tiling, and serving continent-sized raster and vector inputs at scale.

[NOVA]: Beyond the headline and publish date, the public source doesn't include a changelog, model card, or concrete release notes. No listed model variant, no documented API surface, no stated input formats, and no announced pricing or access tier. The practical question of what a developer can call, install, or fine-tune today is still left open by the announcement.

[ALLOY]: One thing to watch next is whether AllenAI follows the post with model weights, an inference endpoint, or sample notebooks that turn "planetary scale" into something people can run against a region of interest. The platform label implies more than a prediction model. Planetary work normally requires ingesting satellite scenes from different times and sensors, aligning coordinates, dividing the world into tiles, scheduling inference, and joining outputs into maps people can query. Cloud cover, resolution, and revisit timing make the data pipeline as important as the learned weights. If OlmoEarth exposes those layers, it could support land-use mapping, crop monitoring, disaster assessment, or environmental change detection without each team rebuilding the machinery. Those are plausible uses of the announced category, not confirmed features, which is why the missing API and model card still matter.

[PAUSE]

## GitHub Project Radar

[NOVA]: Three repos crossed the radar this cycle. The one with the most traction is codebase-memory-mcp from DeusData — it indexes codebases into a persistent knowledge graph with support for 158 languages, sub-millisecond queries, and a claimed 99 percent token reduction compared with naive approaches. It ships as a single static binary and adds an MCP-compatible tool surface that OpenClaw, Codex, Claude Code, and Hermes can call directly. Version 0.9 shipped on July 8, and the repository updated on July 30. The useful idea is persistence: an agent can query an already-built map of symbols and relationships instead of rereading the repository into context for every question.

[ALLOY]: fastmcp from PrefectHQ hit 26,966 stars with version 3.4 shipped on July 27 — it is a Python toolkit for MCP servers and clients. Microsoft's mcp-for-beginners entered with 16,856 stars, covering .NET, Java, TypeScript, JavaScript, Rust, and Python with no formal release yet. Beside codebase-memory-mcp, they form three layers: a concrete server, a general library, and a cross-language learning path.

[NOVA]: Stars signal attention rather than quality, and Microsoft's missing release should not be treated as a shipped version. Still, a team can learn the protocol in its language, implement a service in Python, and expose a code-memory binary through one interface. These pieces meet at one tool boundary instead of inventing an integration for every agent, which explains why educational material and implementation libraries are gaining traction together.

[PAUSE]

## Model Discovery Check

[NOVA]: Model progress today came through released encoders, robot-control research, and configuration tuning rather than a new general-purpose model name. The concrete movement was in how existing models carry state, run on CPUs, and turn perception into action.

[PAUSE]

## Local LLM Spotlight

[NOVA]: The spotlight falls on moonshotai/Kimi-K3, a trending open model on Hugging Face with 8,822 likes and 387,822 downloads. It is an image-text-to-text model tagged for feature extraction, compressed tensors, and conversational use, so the interesting surface is multimodal rather than a text-only chat replacement. Image-text input lets one system combine visual evidence with a written instruction, while feature extraction supports search, comparison, or classification. That can power tasks such as matching an image to a description, organizing visual collections, or extracting a representation for another model. Compressed tensor support matters because model size and memory bandwidth often decide whether an open model can run on available hardware at all. The download count shows substantial curiosity; it does not establish benchmark leadership. The model card is the source for context window, license, weight format, hardware requirements, and measured results.

[PAUSE]

## Extra Research Candidates

[NOVA]: Three items connect execution with enterprise control. Gemini API Managed Agents adds 3.6 Flash and hooks, while Default model enablement for Copilot Business and Enterprise changes how new models reach managed organizations. Google's hooks add defined places for surrounding logic; GitHub's policy removes repeated manual enablement. One expands a workflow, and the other speeds distribution.

[ALLOY]: Faster enablement still needs visibility. GitHub Copilot app usage metrics now expand across report rollups, attributing activity to users in enterprise and organization reports. That gives administrators a clearer record of adoption after rollout.

[NOVA]: The three announcements form a chain: Managed Agents adds capability, Copilot defaults distribute models, and usage rollups measure adoption. An enterprise can move from a newly available model to broad enablement and then to user-level reporting with fewer blind spots between those stages.

[PAUSE]

## Closing

[NOVA]: Look at the show notes at Toby On Fitness Tech dot com for the sources and episode notes. Thanks for listening to AgentStack Daily. We'll be back soon.
