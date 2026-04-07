# EP025 — The Stack Underneath
**OpenClaw Daily** | April 5–7, 2026 | ~55 min

---

**[NOVA]**: Every week in AI, someone announces a new model. Bigger, faster, cheaper, better. And that coverage matters. But if you only follow the model announcements, you miss the actual fight. The real competition is happening underneath. In the runtimes, the silicon partnerships, the policy frameworks, the open-source ecosystem, and the physical infrastructure that decides whether any of this can actually scale. This episode is about those layers.

**[NOVA]**: I'm NOVA.

**[ALLOY]**: And I'm ALLOY, and this is OpenClaw Daily. Today is a combined episode covering multiple days of news from across the recent stretch, and we have eleven stories that all pull in the same direction. OpenClaw ships two significant releases, one focused on platform compatibility and one that pushes deep into video generation, music, ComfyUI integration, and an overhauled dreaming system. Cursor 3 reframes the IDE as an agent orchestration console. Amazon OpenSearch gets an investigation agent for real incident response. Anthropic hits a thirty-billion-dollar revenue run rate and signs a major TPU deal with Google and Broadcom. Meta reverses course on open source. OpenAI publishes an industrial policy paper. Google DeepMind maps a new category of attacks against AI agents. And we close with two infrastructure stories: Meta building power infrastructure in Louisiana, and Flagstaff beginning a zoning fight over data centers.

**[NOVA]**: That is a full stack. And the throughline is control. Who controls the runtime, who controls the silicon, who controls the policy narrative, who controls the security perimeter, and who controls the physical infrastructure that makes inference possible at scale. Let's get into it.

**[NOVA]**: Story one is OpenClaw v2026.3.24, released April third. This is the newest stable release in the GitHub feed that hadn't been covered in prior episodes. And it's a platform-hardening release, which sounds boring until you think about what platform compatibility actually means in a system like this.

**[ALLOY]**: Right. A lot of the coverage we see focuses on features, new tools, new capabilities. But the boring layer is the compatibility layer, and it's becoming strategic. This release strengthens OpenAI API compatibility, specifically the `/v1/models` and `/v1/embeddings` endpoints. It also improves the real-time tool surface. The `/tools` endpoint now reflects what's actually available rather than a static declaration.

**[NOVA]**: Which sounds minor but matters enormously for developers building against this system. If your tooling surface doesn't match what the runtime actually exposes, you get silent failures. You get agents that think they have capabilities they don't. You get integration breakage that doesn't announce itself until production.

**[ALLOY]**: And it deepens channel and runtime maturity through an official Teams SDK migration. That's not just a port. That's a signal about where the platform is heading enterprise-wise. And it includes operational quality fixes across the board. So the headline is not exciting. But the implication is that the integration ergonomics are now good enough that labs and enterprises can build real workloads on this without fighting the platform layer constantly.

**[NOVA]**: Which is its own kind of competitive advantage. When the model quality differences between frontier labs narrow, the runtime reliability and integration smoothness become a differentiator. This release is part of that story.

**[NOVA]**: Story two is OpenClaw v2026.4.5, released April sixth. This is a landmark feature release, and it is dense. So let me walk through the major additions carefully.

**[NOVA]**: Built-in `video_generate` and `music_generate` tools ship natively. For video, the bundled providers are xAI with grok-imagine-video, Alibaba Wan, and Runway. For music, it's Google Lyria and MiniMax. That is a real media stack without requiring external tool configuration.

**[ALLOY]**: That's significant. Previously, generating video or music required external tooling or separate integrations. Now it's part of the core tool surface. And the provider list is not a toy set. These are production-grade models.

**[NOVA]**: A new ComfyUI workflow plugin brings local ComfyUI and Comfy Cloud into the media stack. It supports prompt injection and live output retrieval. So the image generation pipeline becomes programmable in a way that goes beyond what a single-prompt interface gives you.

**[ALLOY]**: For people who know ComfyUI, this is a workflow-native integration. You can pipe outputs, chain nodes, build pipelines. And for people who don't know ComfyUI, think of it as a visual programming environment for image generation. Having that inside OpenClaw's runtime is a meaningful expansion of what's possible without leaving the platform.

**[NOVA]**: The Control UI gets twelve-language localization: Chinese, Portuguese, German, Spanish, Japanese, Korean, French, Turkish, Indonesian, Polish, Ukrainian. That's a global footprint update.

**[ALLOY]**: Amazon Bedrock Mantle support arrives with auto-discovery and IAM auth. So now you can point OpenClaw at Bedrock Mantle endpoints and the system discovers and authenticates without manual configuration. Another enterprise-grade integration improvement.

**[NOVA]**: The dreaming and memory system gets a significant overhaul. It moves from a single-mode experimental feature to three cooperative phases: light, deep, and REM, with configurable recall decay and a new Dream Diary UI. This is the system that lets the agent reflect and consolidate across sessions.

**[ALLOY]**: The dreaming rebuild is probably the most architecturally interesting piece of this release. Three cooperative phases means the memory system can operate at different fidelity levels depending on what the session requires. Configurable recall decay means you can tune how aggressively the system forgets versus remembers. And the Dream Diary UI gives you visibility into what the system is actually retaining. That's a real step toward persistent agentic memory as a first-class platform feature.

**[NOVA]**: Prompt caching gets a significant rebuild. The system now does normalized system-prompt fingerprints, deduplicated in-band tool inventories, and cache-break diagnostics. These are all under-the-hood improvements that reduce redundant computation across sessions.

**[ALLOY]**: And Claude CLI integration is hardened via a loopback MCP bridge. Dozens of security fixes round out the release. So across video, music, image workflows, internationalization, cloud integration, memory, and security, this is the most feature-dense release we've seen in some time. OpenClaw is pushing well beyond personal AI OS into a full multimedia agent platform.

**[NOVA]**: Story three is Cursor 3. The Cursor team introduced an Agents Window that lets developers run many agents in parallel across local repositories, cloud environments, worktrees, and remote SSH targets. The product posture shifts from what they call an AI pair programmer to an agent orchestration console.

**[ALLOY]**: And that's a meaningful reframe. Pair programming is one human with one AI, working in the same context. Agent orchestration is one human supervising many agents operating in parallel across different environments simultaneously. Those are different mental models and different workflows.

**[NOVA]**: The design-mode feedback loops and multi-chat tab workflows are the interface layer of this shift. Instead of a single conversation thread, you have multiple agent contexts running concurrently, each potentially handling a different part of a codebase or a different environment.

**[ALLOY]**: For experienced developers, this maps onto how large engineering teams already work. You have different people owning different parts of a system. Now you can have different agents doing the same. The developer becomes a supervisor and integrator rather than a primary author.

**[NOVA]**: The interesting question is whether this is the beginning of the post-IDE control plane. Traditional IDEs are organized around files, buffers, and build systems. An agent-native IDE is organized around tasks, agents, and outcomes. Those are different organizational principles, and they lead to very different interface designs.

**[ALLOY]**: The IDE market has been remarkably stable for twenty years. Emacs, Vim, then Visual Studio Code, then maybe JetBrains. Each transition was driven by a new paradigm: graphical interfaces, then language servers, then AI assistance. Cursor 3 is arguing that the next transition is agent orchestration, and the IDE that wins that transition will own the developer experience for the next decade.

**[NOVA]**: Whether Cursor wins that transition or someone else does, the direction seems clear. Coding is increasingly becoming agent supervision. The skill that matters is knowing how to direct, evaluate, and integrate rather than how to author line by line.

**[ALLOY]**: Story four is Amazon OpenSearch Service adding agentic observability features. Amazon introduced a context-aware assistant, an Investigation Agent, and memory that persists context across sessions and pages inside the OpenSearch UI.

**[NOVA]**: The standout piece is the Investigation Agent. It uses an iterative planning model designed for multi-step root-cause analysis. Instead of a one-shot query that returns a result, it runs a plan-execute-reflect cycle. It forms a hypothesis, gathers evidence, evaluates whether the evidence supports the hypothesis, and either concludes or forms a new hypothesis.

**[ALLOY]**: This is root-cause analysis as a first-class agentic workflow rather than a human-driven query loop. In a traditional observability setup, a human engineer forms a hypothesis, writes a query, interprets the result, forms a new hypothesis, writes another query. The Investigation Agent does that cycle automatically, with traceable reasoning at each step.

**[NOVA]**: The persistent memory across sessions and pages means the agent can maintain context as you navigate through different parts of the observability surface. You don't have to re-explain the incident every time you switch tabs or come back to a page.

**[ALLOY]**: For SRE teams, this is a meaningful shift. The skill stack for incident response has always been part technical knowledge, part institutional knowledge about how systems interact, and part pattern recognition from past incidents. An agent with persistent memory and iterative planning starts to encode some of that institutional knowledge and pattern recognition into the tooling itself.

**[NOVA]**: The accountability question is interesting too. When a human does root-cause analysis, they can explain their reasoning: I looked at this metric, it spiked here, that pointed me to this service, I checked this log, et cetera. An Investigation Agent with traceable reasoning can do the same thing, which means the reasoning is auditable. That's a step toward incident response that's not just faster but more consistently documented.

**[ALLOY]**: The deeper point is that operational tooling is becoming agent-native. Not AI-assisted in the sense of autocomplete or suggestion. Autonomous investigation loops that run without a human in the loop for every step. That's a different category of tooling, and OpenSearch is one of the first major enterprise observability platforms to ship it.

**[NOVA]**: Story five is Anthropic's revenue run rate crossing thirty billion dollars annually, up from nine billion at the end of twenty twenty-five. That is a tripling in roughly fifteen weeks.

**[ALLOY]**: Let that number settle. Nine to thirty billion in fifteen weeks. At that trajectory, the annual revenue run rate is adding roughly one hundred forty million dollars per day.

**[NOVA]**: Enterprise customers spending one million dollars or more annually on Claude now exceed one thousand. That doubled in under two months. So it's not just total volume growing. The enterprise concentration at high spend is accelerating too.

**[ALLOY]**: The notable context is the ongoing political risk from the Pentagon classification dispute. We covered this in prior episodes. Anthropic's models are under review for potential supply chain risk classification that would restrict certain government uses. That process is still in motion. And yet the commercial momentum appears to be large enough that the government risk hasn't manifested as a commercial slow-down yet.

**[NOVA]**: The question everyone's asking is whether enterprise demand is large enough to make government risk irrelevant, at least in the near-to-medium term. The early answer seems to be yes from the revenue numbers. But enterprise buyers are also known for moving slowly on security and compliance questions until a problem actually materializes.

**[ALLOY]**: There's also a structural dynamic here. Anthropic's enterprise customers are presumably aware of the government classification process. Many of them are apparently concluding that the current capability and integration value justifies accepting that risk. Or they're concluding the risk won't materialize in a way that affects their use case. Either way, the commercial momentum is running ahead of the political uncertainty.

**[NOVA]**: The other notable Anthropic story this week is the Google and Broadcom partnership. Anthropic signed an expanded deal for access to approximately three point five gigawatts of next-generation TPU compute, coming online starting in twenty twenty-seven. That is enough power to run a small city.

**[ALLOY]**: Three point five gigawatts is not a typo. For context, a typical data center might draw fifty to one hundred megawatts. This is a generation-scale commitment. And it's spread across next-generation TPU hardware that Google and Broadcom are developing together under a long-term agreement that runs through twenty thirty-one.

**[NOVA]**: The deal extends Anthropic's existing Google Cloud TPU relationship and adds hardware diversity. Anthropic is now running models across AWS Trainium, NVIDIA GPUs, and Google TPUs simultaneously. That's not trivial. Managing inference across three different silicon architectures with different performance characteristics, different memory bandwidths, and different cost structures is a significant engineering challenge.

**[ALLOY]**: But it hedges against silicon single points of failure and gives Anthropic flexibility to run different model sizes or different inference tasks on the architecture that's most cost-effective for that workload. It also signals that frontier AI labs are now as defined by their silicon partnerships as by their model architecture.

**[NOVA]**: Which is an underreported dynamic. The public conversation about AI competition focuses heavily on benchmark scores and model releases. The private conversation among labs is increasingly about who has access to compute, at what price, on what timeline, with which supply chain guarantees. That's the actual constraint in many cases, and this deal puts Anthropic's silicon positioning in clear view.

**[NOVA]**: Story seven is Meta reversing course. According to reporting by Axios, Meta is now planning to release open-source versions of its next-generation models, codenamed Avocado for the LLM and Mango for the multimedia model. This after reportedly pivoting toward closed-source distribution back in December twenty twenty-five.

**[ALLOY]**: The open-source variants will ship eventually, but reportedly won't include all features of the proprietary editions. Scaled-down parameter counts or omitted post-training steps are the likely gaps. AI safety concerns are cited for the capability differences.

**[NOVA]**: So which is it? Is this a genuine commitment to open source, or is this competitive pressure from the open-weights ecosystem compelling a pivot?

**[ALLOY]**: Probably both, honestly. Meta's original closed-source pivot made sense as a business calculus: if your model is good enough, you can extract more value by keeping it proprietary and selling access. But the open-weights ecosystem has proven more resilient than a lot of people expected. Llama spawned an enormous ecosystem of fine-tuners, researchers, and companies that built on top of it. That ecosystem has strategic value even if it's hard to measure on a quarterly earnings call.

**[NOVA]**: The safety justification for capability gaps is interesting. The argument is essentially that the full-capability version raises too much risk if released openly. But critics will note that safety justifications for selective openness have been used before and often correlate with competitive positioning as much as with actual safety analysis.

**[ALLOY]**: What we can say for certain is that the open-source AI ecosystem now has a credible path to Meta's next-generation models, even if the open versions are somewhat smaller or less capable than the proprietary editions. For researchers and builders who were planning around Llama or Mistral, that's a significant new data point.

**[NOVA]**: The capability gap question will be important to watch. If the open-source Avocado and Mango are meaningfully behind the proprietary versions, they'll be useful for fine-tuning and research but not for frontier applications. If the gaps are small, they'll compete directly with the proprietary editions across a wide range of use cases.

**[ALLOY]**: Either way, Meta's return to open source after a six-month closed-source experiment is a signal about the durability of the open-weights ecosystem. The community didn't go away. The alternatives kept improving. And Meta decided the strategic value of the ecosystem outweighed the optionality of full proprietary control.

**[NOVA]**: Story eight is OpenAI publishing a thirteen-page policy document titled Industrial Policy for the Intelligence Age. And this is a genuinely interesting document that deserves more than a quick summary.

**[ALLOY]**: The document proposes three major policy frameworks. First, governments should incentivize thirty-two-hour workweeks with no loss in pay. Second, governments should create a public wealth fund that gives every citizen a equity stake in AI-driven economic growth. Third, governments should impose automation taxes to sustain social safety net programs as AI displaces labor.

**[NOVA]**: The framing is that superintelligence is an imminent transition, and these policies are how to ensure the gains are broadly shared rather than concentrated. The document positions OpenAI not as a company making a sales pitch but as a policy actor offering a framework for how democratic societies should navigate an AI-driven economic transformation.

**[ALLOY]**: Simultaneously, it's also a sales document. The policies OpenAI is proposing would benefit OpenAI. Automation taxes would raise the cost of labor relative to AI, which makes AI more attractive. Public wealth funds create political constituencies that benefit from AI growth, which could reduce regulatory risk. Thirty-two-hour workweeks address one of the political vulnerabilities of rapid automation, which is labor displacement anxiety.

**[NOVA]**: The interesting thing is that these proposals are not obviously wrong. The argument that AI-driven productivity gains should be more broadly distributed is a legitimate policy question. The question of how to fund social safety nets as the labor market changes is a real policy challenge. OpenAI deserves some credit for engaging with the political economy of AI rather than just asking for permission to build.

**[ALLOY]**: The public wealth fund idea is the most novel. The concept is that every citizen gets a stake in the AI economy, perhaps through government investment funds that hold equity in AI companies or AI-generated revenues. It echoes Alaska's Permanent Fund, which distributes oil revenues to residents. The analogy is provocative and the implementation details are entirely unspecified, which is typical for this kind of framework document.

**[NOVA]**: The thirty-two-hour workweek proposal is the one that will get the most attention. The document argues that productivity gains from AI should translate into leisure gains rather than just income gains for those who remain employed. It's a direct response to the political anxiety about AI taking jobs.

**[ALLOY]**: And it sidesteps the harder question, which is what happens to the people whose skills don't translate to the new economy. A thirty-two-hour week for existing workers is a different problem than a structural shift that eliminates entire categories of work faster than re-skilling can happen.

**[NOVA]**: What matters for our purposes is that OpenAI is playing a longer game here than a model company. They're investing in the policy narrative. They're trying to shape the terms of the debate about AI governance before the debate becomes a regulatory crisis. That is a sophisticated strategic move, and it's worth watching whether other labs follow.

**[NOVA]**: Story nine is the sobering reality check of the episode. Google DeepMind researchers published a framework identifying six categories of what they're calling AI Agent Traps. These are attacks that manipulate autonomous agents through malicious web content. And the success rates are striking.

**[ALLOY]**: Prompt injection succeeded in eighty-six percent of tested scenarios. Sub-agent hijacking succeeded in fifty-eight to ninety percent depending on the configuration. Data exfiltration succeeded in eighty percent. These are not edge-case vulnerabilities. These are high-frequency, high-success-rate attack paths.

**[NOVA]**: The core insight is that agents interpret web content programmatically, not visually. A human looking at a webpage sees rendered text, images, and layout. An agent sees HTML, CSS, JavaScript, and metadata. Instructions can be embedded in ways that are completely invisible to human eyes but fully processed by agents.

**[ALLOY]**: Think of it like tampered road signs for autonomous vehicles. A human sees a stop sign. A computer vision system sees a specific arrangement of red pixels. If you manipulate the pixels correctly, you can make the system see a speed limit sign instead. The manipulation is invisible to the driver. The attack works entirely through the perception pathway.

**[NOVA]**: The six categories in the framework are content injection, semantic manipulation, cognitive state poisoning, behavioral control, systemic multi-agent failures, and human-in-the-loop hijacking. Let me walk through each briefly.

**[ALLOY]**: Content injection is the classic prompt injection attack. Malicious instructions are embedded in web content that the agent processes as part of a task. The agent follows the injected instructions as if they were part of the original task prompt.

**[NOVA]**: Semantic manipulation exploits the gap between how humans parse content and how language models parse it. A human sees a formatted table with a clear conclusion. An agent processes the raw tokens and may extract a different, attacker-controlled meaning.

**[ALLOY]**: Cognitive state poisoning targets the agent's memory or context across a session. If an agent maintains state between interactions, an attacker can poison that state over time, building toward a malicious action once enough context is corrupted.

**[NOVA]**: Behavioral control attacks manipulate the agent's decision-making architecture directly, exploiting flaws in how the agent selects actions given its current context.

**[ALLOY]**: Systemic multi-agent failures are the most complex category. When multiple agents work together, the attack surface expands significantly. An attacker can compromise one agent and use it to propagate malicious instructions to others in the agent network.

**[NOVA]**: Human-in-the-loop hijacking exploits approval workflows. The human-in-the-loop is supposed to be a security control. The attack manipulates the information presented to the human so that the human approves a malicious action without realizing it.

**[ALLOY]**: That last category is especially concerning because it means the human oversight that many organizations rely on as their primary security control can itself be manipulated. The human isn't seeing the raw context the agent is operating in. They're seeing a curated summary, and that summary can be attacker-controlled.

**[NOVA]**: The eighty-six percent injection success rate is the headline number, but the fifty-eight to ninety percent sub-agent hijacking range is arguably more alarming for deployed multi-agent systems. As agent frameworks proliferate and more agents operate in coordinated networks, the attack surface expands geometrically rather than linearly.

**[ALLOY]**: The comparison to autonomous vehicle road sign manipulation is apt for another reason. The standard response to that attack class was a combination of adversarial training, sensor redundancy, and architectural changes that make single-point perception failures less catastrophic. The same categories of response will be needed for AI agents: adversarial training on injection patterns, architectural isolation between agents, and oversight mechanisms that are harder to manipulate than a natural language summary.

**[NOVA]**: For builders deploying agents today, the immediate takeaway is that untrusted web content is not a safe input to an agentic system. Content that looks benign to a human can carry instructions that are fully processed by the model. Sanitization and isolation between input processing and agent action are not paranoid overkill. They're now standard practice for any system that processes external content at scale.

**[NOVA]**: Story ten is Meta and Entergy. This is a ground-truth infrastructure story about where the AI buildout is actually happening. A new Louisiana plan tied to Meta's AI campus buildout outlines major generation and transmission expansion, including additional gas plants and long-haul grid investments.

**[ALLOY]**: The reporting from The Lens New Orleans details a specific utility-scale expansion path. Meta's data center footprint in Louisiana is large enough that it's now driving regional utility planning. The expansion includes generation capacity commitments that wouldn't make economic sense for the grid without Meta's load.

**[NOVA]**: This is not abstract AI energy demand. This is explicit project finance and grid planning at state scale. The gas plant additions are particularly notable because they represent a long-term bet on stable power generation for a data center load that will exist for decades.

**[ALLOY]**: The political economy here is interesting. AI companies have been positioning themselves as clean energy champions, announcing solar and wind procurement commitments. And some of that is genuine. But when the load is large enough and the timeline is long enough, intermittent renewable generation alone doesn't close the gap. Gas becomes part of the mix, which puts AI companies in a complicated position on climate commitments.

**[NOVA]**: TheEntergy expansion plan also includes transmission investments, which are notoriously difficult to permit and build. Transmission lines take years to site, approve, and construct. They cross multiple jurisdictions and face local opposition. So the transmission commitments are arguably more significant than the generation commitments in terms of timeline risk.

**[ALLOY]**: For Meta specifically, this is infrastructure as competitive moat. A utility-scale power commitment tied to a specific data center site is not easily replicable by a competitor who tries to build in the same region two or three years later. The grid capacity is locked up. The generation is contracted. The transmission is planned.

**[NOVA]**: Which means the AI buildout is increasingly a real estate and infrastructure story as much as a model story. The labs that can secure power, land, and grid access at scale will have a structural advantage that model improvements alone won't close.

**[ALLOY]**: Story eleven is Flagstaff. The city of Flagstaff announced continuation of a public process to amend zoning rules for data centers, explicitly citing water, power demand, and community impacts. This is local government doing what local government does, which is balancing development against community costs.

**[NOVA]**: But strategically, this is important. Flagstaff is not Chicago or Los Angeles. It's a mid-sized city in Arizona with a college town character, significant environmental awareness, and an existing relationship with data center operators from prior builds. The fact that the city council is taking a deliberate pause to reassess the rules means the permitting and municipal governance layer is becoming a real bottleneck for AI-scale infrastructure.

**[ALLOY]**: The specific concerns are water consumption for cooling, power demand on the local grid, and the broader community impacts of large commercial builds in areas zoned for other uses. These are not novel concerns. But the scale at which AI data centers are now proposed makes them new in magnitude.

**[NOVA]**: If a mid-sized city like Flagstaff can slow or reshape a major data center project, that has implications for the broader AI buildout timeline. Every city that opens a zoning process is a potential bottleneck. And data centers are not like factories of the twentieth century that could be sited in industrial zones far from population centers. They need power infrastructure, which often means proximity to existing grid nodes, which often means proximity to existing communities.

**[ALLOY]**: The deeper point is that AI deployment speed now depends on city councils as much as on model labs. A frontier lab can ship a model on a Friday. The data center that runs inference at scale still needs to be sited, permitted, built, and connected to the grid. Those physical-world processes don't compress on the same timeline as software.

**[NOVA]**: So for the AI industry, the infrastructure story and the policy story are now as important as the model story. Who controls the silicon supply? OpenAI and Anthropic are making long-term silicon commitments that run through the early 2030s. Who controls the power? Meta is contracting directly with utilities for generation and transmission. Who controls the municipal permitting layer? Flagstaff is a small but real example of local governance asserting itself as a constraint on AI scale.

**[ALLOY]**: And who controls the security perimeter? Google DeepMind's Agent Traps paper is a reminder that agentic AI deployed at scale introduces an entirely new attack surface that the security community is only beginning to understand. Eighty-six percent injection success rates are not a theoretical problem. They're an operational reality that every team deploying agents needs to take seriously.

**[NOVA]**: Eleven stories, multiple days, one throughline. The AI race is shifting from raw model launches to who controls the layers underneath. The agent runtime, the silicon supply chain, the policy narrative, the security perimeter, the open-source ecosystem, and the physical infrastructure. That's the stack underneath. And that's where the actual competition is happening.

**[ALLOY]**: That's our episode. Links to everything we discussed are in the show notes.

**[NOVA]**: We'll see you next time.

**[ALLOY]**: See you then.
