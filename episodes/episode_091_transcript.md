# AgentStack Daily EP091 — 27B Open-Weight Model Now Fits in Laptop RAM, Dorsey Ships Buzz, Anthropic Settles $1.5B Case

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: A 27-billion-parameter open-weight model now fits in laptop RAM. Not a workstation hidden under a desk. A laptop. Ternary compression stores every weight as one of three values, letting people run private chat and lightweight agent loops without sending data to a hosted service. Meanwhile, Jack Dorsey’s Block has launched Buzz, where people, AI agents, chat, and Git activity all share one feed.

[ALLOY]: Okay, that’s actually wild. The local model shrinks the hardware barrier, while Buzz tries to remove the walls between conversation and execution. Elsewhere, pharmaceutical researchers are using AI to prioritize which molecules deserve scarce laboratory time, and Apple developers can give coding agents structured access to builds, simulators, and tests.

[NOVA]: Today: the terminal-based coding agent OpenAI Codex ships point one-forty-five with stabilized multi-agent work and configuration imports; Gemini 3.6 Flash appears with a million-token context window; and Anthropic’s one-point-five-billion-dollar settlement over pirated books clears final approval. You’ll also hear about dramatically leaner code search, a shared model-evaluation security incident, and agents that prune their own context.

[PAUSE]

## [02:00] Agent Stack Release Readout: OpenAI Codex rust-v0.145

[NOVA]: OpenAI Codex point one-forty-five stabilizes its opt-in multi-agent V2 experience. It’s the terminal-based coding agent’s attempt to make parallel workers feel like one coordinated system rather than several chats that happen to share a window. Each sub-agent can use a different model and reasoning level, concurrency is configurable, navigation between workers is cleaner, and restored role definitions keep a coder distinguishable from a reviewer across a long session. Earlier versions could fall into awkward rollback states or blur workers together. This release addresses that roughness directly.

[ALLOY]: And that matters more than another splashy “many agents” demo. Parallel work only helps when you can tell who changed what and why. The other big addition is slash-import, which can bring Cursor or the terminal-based AI coding agent Claude Code configurations into Codex. That includes Model Context Protocol servers, plugins, sessions, custom commands, and project-scoped memories. Model Context Protocol, or MCP, is a common interface through which an assistant calls external tools. Moving those connections and memories preserves the expensive part of a setup: the accumulated context around how a team works.

[NOVA]: Codex also adds experimental Amazon Bedrock support with custom endpoints and authentication, using GPT-5.6 Sol as the default Bedrock model. Audio can now enter a working session through common local formats, and streaming realtime V3 conversations support spoken interaction without a separate realtime client. Tool outputs can include audio too. In the terminal interface, inline visualization links are clickable, so a generated figure can open in a browser instead of decorating the terminal with escape-character confetti. Small mercy, still mercy.

[ALLOY]: The reliability fixes may outlast the headline features. Editing an earlier prompt or retrying a safety-buffered turn now creates a contextual branch rather than discarding attachments and mention bindings. Incremental Markdown rendering and bounded command output keep long terminal sessions responsive. MCP startup has timeouts, preventing broken authentication discovery from freezing an entire session. Windows sandboxing gains native execution-server support and network-proxy enforcement. I’m excited about configurable sub-agents, but stabilization is the real release: multi-agent coding becomes useful when branching, tool startup, roles, and long-session rendering stop fighting the user.

[PAUSE]

## [03:47] Google’s Gemini 3.6 Flash on OpenRouter Listing Adds Gemini 3.6 Flash

[ALLOY]: One million, forty-eight thousand, five hundred and seventy-six tokens. That’s the context window listed for Gemini 3.6 Flash, which has appeared in OpenRouter’s catalog as an immediately routable Google model. It’s positioned as a high-efficiency option for coding, agentic workflows, and web and app development. The Flash label usually means Google is prioritizing speed and efficiency rather than maximum capability, but a million-token window gives the smaller, faster tier an unusually large working surface.

[NOVA]: Large enough to hold a substantial repository, a long tool-call history, retrieved documentation, a feature specification, and relevant failures in one request. That doesn’t mean the model understands every token equally well—context capacity and context use are very different claims—but it reduces the need to summarize away state during a long agent run. OpenRouter availability also matters because teams already routing among providers can add Gemini without replacing their existing model gateway.

[ALLOY]: Google says 3.6 Flash produces polished outputs with fewer unnecessary edits. I like the ambition; I don’t buy that yet without outside results. Coding agents can burn time by rewriting a file, reversing themselves, and touching unrelated lines. If the model lands closer to a finished change on its first attempt, efficiency improves twice: fewer generated tokens and less human review. The open questions are latency, price, and whether cleaner edits survive contact with unfamiliar codebases. Still, pairing fast inference with a million-token window is exciting because it targets the long-running work where smaller models usually lose their footing.

[PAUSE]

## [05:31] Jack Dorsey Launches Buzz: Chat, AI Agents, and Git in One Feed

[NOVA]: Jack Dorsey’s Block has launched Buzz, a workplace platform that combines group chat, AI agents, and Git hosting in one feed. An engineer can bring an agent into a thread as if mentioning a coworker, assign work, and see the response beside the human discussion. Commits and pull requests remain attached to the conversation that produced them. Buzz is trying to preserve the “why” behind a code change instead of leaving it scattered across chat messages, repository comments, and an agent’s private history.

[ALLOY]: That’s a much bolder idea than bolting an assistant into a sidebar. Slack and Microsoft Teams already own huge amounts of workplace conversation, while Git hosting has deeply established workflows. Buzz’s bet is that agent teammates change the product boundary: if software can discuss a task and then modify the repository, perhaps chat and version control shouldn’t be separate places. A Hacker News discussion reached about 330 points within hours, so developers are at least curious. Curiosity isn’t migration, obviously.

[NOVA]: Here’s the uncomfortable question: if an agent sits in the same feed as your team, what can it actually touch? Read-only access makes it an informed commentator. Write access turns it into a coworker with repository credentials. The permissions model therefore decides whether Buzz becomes useful or reckless. Teams need clear identity, approval, and attribution for every agent action, especially when a chat request can become a commit.

[ALLOY]: Right, and I’d push the idea one step further. Buzz could give small teams a shared record spanning request, discussion, implementation, and review without making them stitch together three systems. That’s genuinely appealing. But the unified feed can also become an extraordinarily concentrated source of sensitive information: team conversations, code, agent instructions, and change history in one place. The integration is the attraction and the blast radius. Buzz succeeds if it makes that concentration legible and controllable, not merely convenient.

[PAUSE]

## [07:24] Semble Ships a 98% Leaner Code Search for AI Agents

[ALLOY]: Code generation gets the applause, but code search often gets the bill. MinishLab’s Semble is an open-source search backend built for agents, and the team claims roughly ninety-eight percent fewer tokens than a naïve grep-and-read pipeline for the same query. Semble point five-two shipped on July twenty-first, additional commits followed within a day, and the repository has passed 5,600 GitHub stars.

[NOVA]: The waste is easy to recognize. An agent runs grep, receives line numbers, opens several whole files, and spends thousands of tokens reconstructing the relationships around one function. Semble instead returns a compact, focused result that the model can act on directly. Asking where a retry handler is defined shouldn’t require importing half the repository into the conversation. Search can dominate cost before the model writes a single useful line.

[ALLOY]: Ninety-eight percent is MinishLab’s number, so I’m treating it as a vendor claim until independent comparisons reproduce it on varied repositories. Even a much smaller reduction would matter, though. Better retrieval lets an agent preserve more of its context window for reasoning, patches, and tool history. It can also make longer refactors more coherent because irrelevant source dumps no longer crowd out earlier decisions.

[NOVA]: Semble is infrastructure rather than another chat surface or editor skin. An agent harness can call it as the search layer and keep its existing interface. That makes formal integrations with popular coding agents the next meaningful milestone. If those arrive and real-repository measurements hold up, focused code retrieval could replace the familiar grep-plus-read loop quietly. Most useful infrastructure arrives that way: no keynote, just a smaller token invoice and an agent that stops wandering through twelve files to answer a one-line question.

[PAUSE]

## [09:10] whodb Crosses 4,900 Stars with Active Shipping Pace

[NOVA]: whodb has crossed roughly 4,930 GitHub stars, released point one-twenty-one on July sixteenth, and received another repository push on July twenty-second. The maintainers describe it as “where data access meets operational intelligence.” That wording places the project between tools used to query data and tools used to understand what’s happening inside the systems that hold it.

[ALLOY]: I’m intrigued, but the tagline is carrying more weight than the available product detail. “Operational intelligence” can mean genuinely useful system awareness or a dashboard with ambition. The active shipping pace is the concrete part: a release followed by further work inside a week shows a project moving quickly rather than sitting on accumulated stars. At a pre-one-point-zero version, each release is still a checkpoint while the team shapes the surface.

[NOVA]: Exactly. Star count measures attention, not durability, and a high version count doesn’t guarantee maturity. What matters is what lands in subsequent releases, whether the repository passes 5,000 stars and keeps attracting users, and whether the maintainers eventually define a stable one-point-zero contract. Data tools become dependencies quickly; frequent changes are exciting until integrations start breaking.

[ALLOY]: Still, nearly 5,000 people watching an actively maintained open-source data project isn’t nothing. The opportunity is a tool that lets people reach their data while also exposing useful operational context around it. The unresolved question is whether those two jobs become one coherent product. If whodb turns its positioning into shipped capability, it could give agents and people a more informed way to inspect live systems. If not, it remains a fast-moving database interface with a very confident sentence on the README.

[PAUSE]

## [10:56] holaOS Aims to Be Your Local-First Work Agent

[ALLOY]: holaOS is aiming at the memory problem from the privacy side. The open-source project says its work agent runs locally, learns a person’s working context in minutes, and retains that context across sessions. It has already collected more than 5,500 GitHub stars, with repository activity as recent as July twentieth. There isn’t a tagged GitHub release yet, so it’s an actively developed proposition rather than a finished product.

[NOVA]: The proposition is clear: files, prompts, and project history stay on the user’s machine instead of becoming a memory profile stored in somebody else’s cloud. That appeals to freelancers handling client material, companies protecting internal documents, and anyone who wants continuity without exporting an entire working life. Local-first doesn’t automatically mean secure, of course. It means the control boundary moves to the machine, where storage, permissions, and backups still matter.

[ALLOY]: Persistent memory is where I get both excited and skeptical. An agent that remembers a multi-week project could avoid the repeated ritual of explaining architecture, decisions, and unfinished tasks every morning. But “never forgets” is marketing until the implementation shows what gets stored, how retrieval works, and whether old or incorrect context can be corrected. Infinite memory isn’t the same as useful memory. Ask anyone with a downloads folder.

[NOVA]: A tagged release and a real multi-day demonstration will tell us far more than the star count. holaOS needs to show that it can preserve relevant context without allowing stale summaries to steer new work. If it succeeds, the result is more than private chat: it’s a local work agent whose understanding accumulates over time. That’s one of the strongest reasons to run an assistant on-device, because the value grows with private history that a user may never want to upload elsewhere.

[PAUSE]

## [12:45] A 27B Open-Weight Model Now Fits in Laptop RAM

[NOVA]: prism-ml’s Ternary-Bonsai-27B package puts a 27-billion-parameter open-weight model into a memory footprint that modern laptops with sixteen or thirty-two gigabytes of unified memory can handle. Published on Hugging Face in GGUF format for llama.cpp, it passed 432,000 downloads and collected 913 likes shortly after its July fourth release. CUDA acceleration supports Nvidia hardware, while Metal covers Apple Silicon Macs.

[ALLOY]: Okay, say the compression part slowly, because that’s the magic trick. Each weight is represented as one of only three possible values. That’s ternary quantization: extremely compact numerical storage that preserves all 27 billion parameters while reducing the memory needed to load them. The model can fit in RAM rather than streaming weights from disk or demanding workstation-class hardware. No hosted API is required, and prompts can remain entirely on the machine.

[NOVA]: That opens practical uses on hardware people already own: private document conversation, offline assistance, local experimentation, and lightweight agent loops. The GGUF packaging places it in the established llama.cpp ecosystem instead of requiring a bespoke runtime. Download numbers also suggest this isn’t merely a paper exercise. People want larger local models, especially when the alternative means recurring API costs or sending sensitive material to a third party.

[ALLOY]: But here’s where I’ll spoil the party slightly: fitting isn’t the same as reasoning well. Aggressive quantization can preserve ordinary conversation while degrading harder multi-step work. Independent evaluations need to show whether Ternary Bonsai maintains useful quality on longer reasoning and complex instructions. Even if quality drops, the footprint achievement still matters. Two years ago, running a 27-billion-parameter model comfortably on a laptop sounded absurd. Now the argument has moved from “can it load?” to “how capable is it once loaded?” That’s a significant shift.

[PAUSE]

## [14:42] Anthropic’s $1.5B Pirated-Books Settlement Gets Final Court Approval

[ALLOY]: A federal judge has approved Anthropic’s one-point-five-billion-dollar settlement over pirated books used in training Claude. The lead case involved authors including Andrea Bartz, and the settlement compensates writers whose books were downloaded from pirate sources and included in the training mix. That dollar figure is enormous. It gives the industry a concrete view of the financial exposure attached to acquiring copyrighted material through piracy.

[NOVA]: The approval closes this case without resolving the larger legal question: whether training an AI model on copyrighted books without permission qualifies as fair use. Anthropic settled rather than continuing to litigate that defense here. Other lawsuits against AI companies remain active, so courts still haven’t drawn a general line around lawful training. One dispute ends; the central doctrine remains unsettled.

[ALLOY]: And authors covered by the agreement now receive compensation for works they didn’t agree to license for AI training. Other labs that touched pirate-book archives also have a reference point for what a negotiated resolution can cost. I wouldn’t treat one settlement as a universal price list—the facts and classes in other cases can differ—but nobody can dismiss training-data provenance as a theoretical compliance concern after a one-point-five-billion-dollar payment.

[NOVA]: The next consequential development would be a ruling that actually interprets fair use for model training, rather than another settlement that avoids the question. Until then, buyers and builders face an awkward split: models may be commercially available while the legality of portions of their training data remains contested. The case attracted hundreds of Hacker News comments because developers, authors, and AI customers all have something at stake. Better models came from vast corpora; the unresolved argument is who had the right to put those corpora together.

[PAUSE]

## [16:26] digest:github Listing Adds

[NOVA]: SWE-Pruner Pro addresses a quiet source of waste in coding agents: long tool outputs. Instead of using a separate model to filter code and command results, the research says the coding model already carries internal clues about which material matters. A small trained component reads those clues and removes irrelevant chunks before they consume prompt space. In ordinary language, the agent performs its own triage.

[ALLOY]: That connects directly to Semble from earlier. Semble tries to avoid retrieving unnecessary code; SWE-Pruner Pro tries to discard irrelevant material after tools return it. Together they point toward agents that spend less of their context window hauling around raw output. Removing a separate filtering model could also lower latency and cost. I’m interested, though open-agent adoption will determine whether this becomes infrastructure or stays a promising paper result.

[NOVA]: Self-pruning becomes especially valuable during long coding sessions, where command logs and file reads accumulate faster than useful decisions. The hard part is preserving the one obscure detail that later proves essential. Still, teaching a model to recognize its own relevant context is cleaner than adding another classifier to every tool call. Would you rather pay a capable model to reason over evidence or to repeatedly reread terminal debris? Exactly.

[PAUSE]

## [17:29] OpenAI and Hugging Face Disclose Model Evaluation Security Incident

[NOVA]: OpenAI and Hugging Face jointly disclosed early findings from a security incident involving model evaluation. Their July twenty-first account says the threat actors demonstrated advanced cyber capabilities. That wording is careful but meaningful: the activity went beyond routine commodity attacks. Details remain limited because the findings are preliminary and fuller disclosure could expose defensive gaps.

[ALLOY]: Two competing AI organizations publishing together is unusual and, honestly, encouraging. Evaluation systems sit near valuable assets: model weights, prompts, generated data, and infrastructure connected to serving or research. An intrusion into evaluation isn’t automatically an intrusion into production, but it creates an uncomfortable launch point for attempts to move deeper. These systems also ingest external models and artifacts, so they naturally attract adversaries.

[NOVA]: The incident punctures the idea that evaluation is merely a scientific side room. Once an environment executes untrusted code or loads external model artifacts, it becomes a security-sensitive production asset. The joint post frames the event as a learning opportunity for defenders, but early findings leave major questions unanswered: what was accessed, how the actors entered, whether they moved laterally, and which mitigations have already changed.

[ALLOY]: I’m not going to pretend a thin disclosure proves a new norm, but collaboration here matters. Shared evaluation practices can create shared weaknesses, and attackers don’t respect company boundaries. A fuller post-incident account could help other labs close similar paths without exposing operational details that aid the next intrusion. The bigger change is cultural: model evaluators now have to think like custodians of high-value infrastructure, not only people measuring accuracy. Security belongs wherever weights, tools, and outside artifacts meet.

[PAUSE]

## [19:17] Research Digest: Why Long-Context Reasoning Models Copy-Paste Your Prompt Instead of Thinking

[ALLOY]: Have you ever handed a model a huge document and watched it quote the document instead of answering? New research identifies indiscriminate copying as a recurring failure in long-context reasoning. As prompts grow, models can latch onto nearby but irrelevant text, reproduce it in their reasoning, and reach the wrong answer. The issue isn’t simply a lack of context capacity; it’s poor selection within that context.

[NOVA]: The researchers added a training reward that favors reasoning grounded in relevant evidence and penalizes echoes of filler. Across several model sizes, they report gains of up to 4.6 points over standard training, with the largest improvements on the longest inputs. Reasoning traces also became shorter. Those are research results, not a guarantee across every model, but they suggest better grounding can improve both accuracy and efficiency. Copying isn’t harmless verbosity here. It can reveal that the model has stopped distinguishing evidence from surrounding text.

[PAUSE]

## [20:24] XcodeBuildMCP 2.6 Gives Coding Agents Real Access to Apple Builds

[NOVA]: Sentry’s XcodeBuildMCP two-point-six gives AI coding agents structured access to iOS and macOS build workflows. The open-source project has more than 6,100 GitHub stars, released this version on June second, and received new repository work on July twenty-second. It wraps Apple’s build command and iOS Simulator controls behind MCP tools, exposing build targets, project schemes, and device operations as functions an agent can call.

[ALLOY]: That closes a frustrating gap. A coding assistant can edit Swift files, but Apple development doesn’t end at text. The code has to compile against a selected scheme, run in a simulator, and produce failures the agent can interpret. XcodeBuildMCP sits between the assistant and local Apple tooling, allowing the agent to remain involved after it proposes a patch. That’s much closer to a real development loop.

[NOVA]: Because the server runs locally, actions occur on the developer’s machine rather than inside an abstract remote sandbox. The agent can access the actual project configuration and simulator state exposed through the tool interface. Sentry maintains the repository, which gives the project a natural connection to teams already using Sentry’s development and crash-reporting ecosystem, though the tool’s value isn’t limited to those teams.

[ALLOY]: I’m surprised Apple hasn’t made this kind of agent interface native yet. Until it does, XcodeBuildMCP is a practical bridge between assistants and one of software development’s more specialized toolchains. Its 6,100 stars show substantial demand. The interesting adoption question is whether it becomes a standard component in Apple coding-agent setups or whether native support eventually absorbs the job. Either way, agents that can build and operate a simulator are materially more useful than agents that stop after editing source.

[PAUSE]

## [22:14] Community Qwen 3.6 MoE Variant Tops Hugging Face Trending

[ALLOY]: A community-built Qwen 3.6 variant is near the top of Hugging Face’s trending listings, and the name is a mouthful: Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive. Publisher HauhauCS packages it as a multimodal mixture-of-experts model in GGUF format, supporting vision and text. It has approached two million downloads and just under 3,000 likes. Whatever you think of the branding, people are paying attention.

[NOVA]: Mixture of experts means the model contains many specialized parameter groups but activates only a subset for each token. The 35B-A3B label indicates roughly 35 billion total parameters and about three billion active at once. That aims to provide broader capacity without the full inference cost of a dense 35-billion-parameter model. GGUF compatibility puts it directly into llama.cpp and the broader local-model ecosystem.

[ALLOY]: The “uncensored” and “aggressive” labels signal reduced safety filtering compared with an upstream model. Some local users want fewer refusals and full control over the weights, especially for agent experiments. That freedom also transfers moderation and security responsibility to the person deploying it. A model that follows more requests isn’t automatically more capable; sometimes it’s merely less selective. That distinction tends to disappear in enthusiastic download threads.

[NOVA]: Still, the popularity tells us something about distribution. Community publishers increasingly turn new base models into quantized, locally runnable variants faster than original labs serve every possible hardware profile. People can add image input, run the model on consumer hardware with enough memory, and avoid external API calls. If this download curve keeps climbing, community-packaged mixture-of-experts releases may become the default way many local users encounter new open models—not through the original checkpoint, but through practical repackaging optimized for machines they own.

[PAUSE]

## [24:03] Bristol Myers Squibb Builds a Vera Rubin SuperPOD for Drug Discovery

[NOVA]: Bristol Myers Squibb is deploying its second NVIDIA DGX SuperPOD for drug discovery. The new cluster uses eight rack-scale DGX Vera Rubin NVL72 systems and will be opened to scientists across the company’s global research organization. Each system combines NVIDIA Vera CPUs with Rubin GPUs. NVIDIA claims the cluster can deliver up to ten times the performance per megawatt of the infrastructure it replaces; that number’s straight from the vendor, so real operating data will matter.

[ALLOY]: This isn’t just a giant hardware purchase with a molecule painted on the slide. BMS reports concrete results from its first SuperPOD: AI-assisted target identification saved scientists weeks of manual work. Researchers used models to expand a library of compounds designed to degrade cancer-causing proteins, then predicted which molecules were most promising before using laboratory time to synthesize them. That ordering matters because physical experiments remain expensive and scarce.

[NOVA]: The company is adding NVIDIA’s BioNeMo Agent Toolkit for biological AI and Mission Control as the operating layer. Its old and new SuperPODs will connect through one data plane shared across research locations. Scientists are expected to initiate complex predictions in plain English, without requiring every user to become a computing specialist. Experimental results and model outputs can then accumulate in a shared learning loop across sites.

[ALLOY]: That’s the part I find genuinely exciting. The goal isn’t an office assistant writing cleaner emails for scientists. It’s shared infrastructure that helps decide which biological targets and molecules deserve real experiments. If access works as described, research teams won’t have to wait for a specialist at one location to operate the system. More compute alone doesn’t discover a drug, obviously. But shared compute, domain models, accumulated experimental knowledge, and natural-language access can shorten the path between a scientific question and the next useful experiment.

[PAUSE]

## [26:02] GitHub Project Radar

[NOVA]: FastMCP from PrefectHQ leads the radar with 26,752 GitHub stars. It’s a Python framework for building MCP servers and clients with decorators and type hints, letting a normal Python function become an agent-callable tool without hand-writing piles of schema glue. Version three-point-four shipped July ninth, and the repository was updated July twenty-first. It can sit behind Codex or the terminal-based AI coding agent Claude Code, exposing existing Python capabilities through a common tool interface. That traction suggests developers want MCP plumbing to feel like ordinary application code, not protocol ceremony.

[ALLOY]: Microsoft’s MCP-for-Beginners enters with 16,812 stars and a July twenty-first update. It’s a multi-language curriculum with runnable labs in .NET, Java, TypeScript, JavaScript, Rust, and Python. The traction isn’t tied to a packaged release; it comes from broad interest and active updates. Its integration value is consistency: teams with polyglot services can use one shared protocol for exposing tools to agents instead of inventing separate conventions in every language. It’s educational material, yes, but nearly 17,000 stars says the protocol’s learning curve has become its own ecosystem problem.

[NOVA]: Unity MCP from CoplayDev has 12,741 stars, released version ten-point-one on July thirteenth, and was updated the same day. The in-editor plugin exposes asset management, scene control, script edits, and automation as MCP tools. Connected to an assistant, it can support compile-and-play loops, inspect assets, and modify scenes without custom editor glue. That’s a notable expansion from coding into operating a graphical development environment. Pair it mentally with XcodeBuildMCP: agents are moving past files and into the actual tools where software is built, run, and inspected.

[PAUSE]

## [27:48] Model Discovery Check

[ALLOY]: Gemini 3.6 Flash is available through OpenRouter with a one-million, forty-eight-thousand, five-hundred-and-seventy-six-token context window. Google positions it for efficient coding, agent workflows, and web or app development, with fewer unnecessary edits. The listing doesn’t provide parameter counts. Its immediate appeal is routing: existing OpenRouter users can place a major-provider Flash model behind the same interface they already use for other models.

[NOVA]: Gemini 3.5 Flash-Lite also appears with the same million-token context length. Google describes it as a high-efficiency model with upgraded agentic capabilities, suited to focused sub-agents inside larger multi-agent workflows. That’s a narrower role than a flagship reasoner: cheap, targeted workers handling bounded tasks while a stronger coordinator manages the whole job. Pricing and independent performance comparisons will determine whether that positioning translates into an attractive sub-agent tier.

[PAUSE]

## [28:42] Local LLM Spotlight

[NOVA]: Thinking Machines’ Inkling is a multimodal mixture-of-experts model for image-and-text and audio-and-text conversations. It’s released under Apache two, ships in safetensors format, includes published evaluation results, and offers an interface compatible with hosted inference endpoints. Mixture-of-experts routing activates only parts of the model for each input, keeping inference cost closer to a smaller model while retaining broad multimodal coverage.

[ALLOY]: Inkling is trending on Hugging Face with 1,404 likes and 16,441 downloads. The useful distinction is breadth: one model can work across text, images, and audio, with downloadable weights for local use or an inference endpoint when local hardware isn’t appropriate. That combination supports private multimodal applications without forcing every deployment into one operating model. Published evaluations help, though independent results will show how well its different modalities hold together in real conversations.

[PAUSE]

## [29:36] Extra Research Candidates

[ALLOY]: Three more developments deserve a look. XcodeBuildMCP’s repository has 6,106 stars and wraps Apple builds plus simulator control as structured agent tools, reinforcing its momentum beyond the two-point-six release. OpenAI also added David Vélez and Robin Vince to the boards of the OpenAI Foundation and OpenAI Group PBC. Those appointments affect oversight of compute commitments, governance, and the corporate structure behind model and API access.

[NOVA]: The third is OpenAI’s “Safety and alignment in an era of long-horizon models.” It collects lessons from deploying models that work for extended periods, including context drift and goal misgeneralization—agents gradually losing relevant state or pursuing the wrong interpretation. OpenAI discusses iterative deployment, runtime monitoring hooks, and a red-team inventory of observed failures. That matters because safety can’t depend only on the initial instruction when an agent keeps acting for hours or days. Long-running behavior becomes its own control problem.

[PAUSE]

## [30:34] Practical Queue

[NOVA]: Codex point one-forty-five makes configurable multi-agent work and cross-tool imports more credible. Gemini’s new Flash listings bring million-token context to efficient agent roles. Buzz puts agent action beside the conversation and Git history that authorized it.

[ALLOY]: Semble and SWE-Pruner Pro attack context waste before and after retrieval. Ternary Bonsai brings 27 billion parameters into laptop memory, while Inkling and the community Qwen variant expand local multimodal choices.

[NOVA]: XcodeBuildMCP and Unity MCP let agents operate real development environments. The evaluation incident puts security around those tool boundaries in sharper focus.

[ALLOY]: And BMS shows where this can lead: shared AI infrastructure helping scientists choose the next physical experiment. For sources and further details, look at the show notes at Toby On Fitness Tech dot com. Thanks for listening to AgentStack Daily. We'll be back soon.
