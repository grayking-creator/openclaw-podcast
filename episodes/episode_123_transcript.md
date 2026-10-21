# AgentStack Daily EP123 — Beam 1.0 lands, MLX runs near-trillion Muse, 10K agents go 36 hours

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily.

[NOVA]: A half-trillion-parameter coding model just arrived with only twenty-three billion parameters active for each token. Reflection’s Beam 1.0 is listed on OpenRouter with a one-million-token context window, while Apple has shown an eight-hundred-sixteen-billion-parameter model generating more than thirty-six tokens per second across four Mac Studios. Enormous models, but much more deliberate control over which compute wakes up.

[ALLOY]: And the smaller systems may be just as consequential. A compact draft model can accelerate local vision-language generation by proposing fifteen tokens at once. Four autonomous players have defeated Minecraft’s Ender Dragon by talking, sharing memory, and writing their own code. A security team can move from a detected threat to a proposed patch in minutes. Today: Beam 1.0, Apple’s clustered MLX run, faster local vision models, NVIDIA’s expanded Nemotron family, ten thousand agents operating for more than thirty-six hours, and Grok Voice taking the lead in a major speech-to-speech ranking.

[PAUSE]

## [02:00] Agent Stack Release Readout: Hermes Agent .22.2, .22.1, .22.0, .21.7

[NOVA]: Hermes Agent .22.2 shipped October fifteenth to correct a bad .22.1 build from the day before. The earlier package came from the wrong commit and accidentally carried unreleased gateway work. On the Microsoft Store build, that could leave the application stuck at “Connecting.” The replacement rolls that work back and concentrates on two documented fixes. First, Hermes now handles a nasty reboot edge case affecting supervised gateways under systemd, launchd, or Docker. After Linux restarts, the kernel can reuse an early process identifier for an unrelated process. Hermes could mistake that stranger for its own gateway and refuse to start. It now records the boot in which the gateway began. If that record can’t settle the question, Hermes checks the host lock, which only the live gateway should possess. The second fix improves local-model behavior on laptops. Prompt-reading progress remains visible during long requests. Time spent asleep no longer counts against stall timers. A recovered local server gets another attempt instead of leaving later turns behind an open circuit breaker. Conversation compression can continue while the server reads a long prompt. On Windows machines with unified memory, model launch and prompt caching are sized against available memory rather than an imaginary separate pool of video memory.

[ALLOY]: That’s a repair release with a very specific scar behind it. Sessions created under the faulty .22.1 gateway can’t be deleted from .22.2, although sessions begun under the correct build can be cleared normally. The broader foundation came from .22.0, the “Threshold Release,” which Hermes described as roughly two and a half times the size of the .21 cycle. It added a guided first-launch conversation using a free trial model, so a newcomer could begin without bringing an API key; connectors for hosted applications; a one-click llama.cpp runtime for local models; and signed desktop packages, including the Microsoft Store version. The preceding .21.7 release also belongs to this run of stable updates. Put together, the line is moving in two directions at once: easier entry for someone opening Hermes for the first time, and better recovery for people running it as persistent infrastructure. The reboot fix matters most to unattended gateways, while sleep-aware timers and memory sizing make local inference less brittle on ordinary laptops. And yes, shipping the wrong commit is painfully mundane. Correcting it quickly and documenting exactly what escaped is still the right response.

[PAUSE]

## [03:47] Reflection's Beam 1.0 lists on OpenRouter as a 501B coding MoE

[ALLOY]: Five hundred one billion parameters sounds enormous, but only twenty-three billion are active for each token. What does that actually buy Beam 1.0?

[NOVA]: Reflection positions Beam 1.0 as an open-weight reasoning model for coding and long-horizon agent work. Its sparse mixture-of-experts design divides the model into specialized groups and activates only a subset for any given token. That allows a very large total capacity without paying the full dense-model compute cost on every step. The OpenRouter listing gives it a context window of one million forty-eight thousand five hundred seventy-six tokens, with text input and text output. That’s enough room, in principle, to carry a substantial codebase, a long execution history, or an extended agent session without constantly discarding earlier material. Access is through OpenRouter’s API under Reflection’s Beam listing. Because it’s an API listing as well as an open-weight model, teams can place it behind existing agent software without first standing up half-trillion-parameter infrastructure themselves.

[ALLOY]: I like the shape of that offering more than the raw parameter headline. Twenty-three billion active parameters could make operating cost and latency more manageable than the half-trillion total suggests, while the broader expert pool gives the model room to specialize. But I don’t buy the idea that a million-token window automatically becomes a million tokens of useful memory. The listing and positioning statement don’t establish how reliably Beam edits repositories, recovers from failed tool calls, or keeps distant requirements active during a long job. Those behaviors determine whether giant context becomes working memory or expensive storage. Still, a major open-weight coding model with that capacity arriving behind a common API is a serious new option, not a laboratory curiosity. It also gives teams another route between small local coding models and fully closed frontier services.

[PAUSE]

## [04:38] Apple MLX Runs Near-Trillion Parameter Muse Spark Open on Mac Studio Cluster

[NOVA]: Apple’s machine-learning group has shown Muse Spark Open—eight hundred sixteen billion total parameters, with forty-two billion active per token—running at more than thirty-six generated tokens per second across four M5 Ultra Mac Studios. The model occupies roughly four hundred ninety-three gigabytes after compression, so this isn’t one giant desktop pretending to be a data center. MLX distributes the work across Macs connected through low-latency memory transfers over Thunderbolt 5.

[ALLOY]: Okay, that’s actually wild. Thirty-six tokens per second is comfortably above ordinary reading speed, and the cluster still looks like office equipment. How does MLX divide something that large without communication swallowing the gain?

[NOVA]: It supports two layouts. Pipeline parallelism splits the model by depth, so one Mac processes an early group of layers before passing the result onward. Tensor parallelism divides work across the width of the same layers. New communication operations called jaccl move data across the cluster, while mlx.launch starts distributed jobs on connected hosts. A single M5 Ultra Mac Studio with five hundred twelve gigabytes of unified memory can already hold Mistral Medium 3.5 at one hundred twenty-eight billion parameters or Qwen 3.8 at twenty-seven billion. Compared with an M3 Ultra, Apple reports up to four-point-six times faster time to first token and about one-point-six times faster decoding. Matrix acceleration improves the initial prompt pass; the M5 Ultra’s one-point-two-terabyte-per-second memory bandwidth helps sustain generation.

[ALLOY]: Peak power stays around three hundred watts, roughly a toaster, although four premium Macs are still a serious purchase. The compelling use is local work with private code, financial records, medical text, or unreleased product material. MLX, macOS, unified memory, and Thunderbolt now provide a documented route to frontier-scale local inference instead of an improvised cluster. It also makes the memory advantage of these machines much more concrete: unified memory isn’t merely helping one oversized model fit; several computers can pool their capacity and keep generation moving at an interactive pace.

[PAUSE]

## [06:22] Open-source 3D architectural editor ships CLI and MCP tools for AI agents

[ALLOY]: A 3D architectural editor with agent tools sounds useful, but also like a perfect way to let a language model put a staircase through the ceiling.

[NOVA]: Pascal Editor approaches that problem with a local command-line interface and Model Context Protocol tools. Its command package reached 1.0 on October thirteenth, and the repository was updated again on October sixteenth. MCP is the shared protocol that lets an assistant discover and call external tools. Inside a 3D editor, that can turn scene operations into structured actions instead of forcing an agent to simulate the interface or generate an opaque script. The project has roughly twenty-four thousand nine hundred GitHub stars, so it already has a substantial audience. A local command surface also makes repeated operations easier to reproduce across related objects or design revisions.

[ALLOY]: Right, and the combination matters. A person can stay in the visual editor while an agent handles repetitive or precisely described operations through command and MCP surfaces. Architects and artists still need to judge geometry, proportion, circulation, and spatial relationships; agents can carry an instruction across repeated actions. Structured calls also provide a clearer account of what the assistant attempted than a trail of simulated mouse movements.

[NOVA]: I’d still reserve judgment on autonomy until the exposed scene operations are documented in detail. An MCP label explains how a tool is called, not how much of a complex model it can safely revise. Creating one wall is straightforward; preserving constraints while changing a connected building is much harder. Even so, the command interface and protocol layer give agents a real entry point without displacing direct human editing. Structured 3D work is joining the tool ecosystem already spreading through code, documents, and data.

[PAUSE]

## [07:37] MiniCPM-V 4.7 Gets a Speed Boost via Speculative Decoding

[NOVA]: OpenBMB has released a quantized DSpark draft checkpoint that accelerates MiniCPM-V 4.7 through speculative decoding in llama.cpp. The target is the thirty-five-billion-parameter vision-language model, while the draft checkpoint is roughly three hundred eighty-nine million parameters. Instead of making the large target produce every token sequentially, the draft proposes fifteen candidates in one forward pass. The target verifies those candidates together, accepts the matching run, and corrects from the first disagreement. The final answer still comes from the target; the smaller draft changes how quickly candidate text reaches verification. OpenBMB reports an average of 3.501 accepted tokens per verification step on general text and 7.387 on code generation, with vision evaluations around five to six accepted tokens.

[ALLOY]: So the little model isn’t replacing the large one or quietly choosing the answer. It’s making an informed guess about where the target goes next. The draft is tuned to the matching MiniCPM-V 4.7 target, which means it isn’t a universal accelerator for unrelated models. It requires a llama.cpp build supporting the dflash architecture and DSpark Markov head, and the target, vision projector, and draft work as a matched set with an eight-thousand-one-hundred-ninety-two-token example context. That constraint makes the result more credible, not less. OpenBMB supplied a purpose-built predictor and measured how many proposals survive verification across text, code, math, and visual tasks. Quantizing the draft can change how frequently candidates are accepted, but rejected candidates don’t override the target’s output. Several verified tokens per step can make a large local vision model feel much more responsive without moving the image or prompt to a hosted service.

[PAUSE]

## [09:24] NVIDIA Expands Nemotron Family with Super VL and Bolt Edge Models

[NOVA]: NVIDIA has expanded Nemotron with three open models spanning data-center agents and compact edge deployments. Nemotron 3.5 Super VL has one hundred twenty billion parameters and targets always-on, high-volume agents. NVIDIA says it matches the accuracy of its largest reasoning model at about one-fifth the parameter count and runs up to five times faster than the next-best model in its class on Artificial Analysis’s Intelligence Index. That number comes straight from NVIDIA, so I want outside reproduction before treating the race as settled.

[ALLOY]: The range catches me more than the flagship alone. Bolt 74B-A9B uses native two-bit quantization to fit a seventy-four-billion-parameter model into twenty-four gigabytes, leaving capacity for other applications on an RTX system or DGX Spark. NVIDIA ranks it first among open models in its memory class on PinchBench and second on BrowseComp. It supports llama.cpp, Ollama, LM Studio, Unsloth, and vLLM. Bolt E4B, designed for conversational and physical agents, is scheduled for October twenty-third across GeForce RTX, Jetson, and DGX Spark. Super VL and the larger Bolt are available now through Hugging Face, OpenRouter, ModelScope, and NVIDIA’s NIM services.

[NOVA]: Named deployments make this more than a model-family diagram. Super VL was trained on about twenty-six trillion tokens and post-trained with roughly three-point-eight million samples across dozens of reinforcement-learning environments. Scale AI adapted it for Skydance’s vendor-credit finance agent and EY’s merger-and-acquisition due-diligence agent. AfterQuery tuned it for Hebbia’s credit-agreement analysis, while Mercor post-trained it for coding agents on APEX-SWE. Atlassian, CrowdStrike, Dassault Systèmes, Perplexity, Salesforce, and Synopsys are integrating the family. NVIDIA is also releasing datasets for tool use, finance, instruction following, long context, fairness, and vision-language understanding. Its Dynamo claim—up to eight times more users with eighty-five percent lower latency—is still a vendor figure. But open weights, common runtimes, customization assets, and live integrations make the family much more substantial than a leaderboard screenshot.

[PAUSE]

## [11:17] Research digest: Four AI Agents Beat Minecraft's Ender Dragon Together

[ALLOY]: Four Gemini 4 Argon agents have defeated Minecraft’s Ender Dragon in a sandboxed survival world. I know how that sounds, but Minecraft is a brutal long-horizon coordination environment: gathering resources, crafting, navigating, surviving, and recovering from mistakes all compound over hours.

[NOVA]: Each agent controlled one player through the open-source Mineflayer library. They coordinated through in-game chat and shared memory, with no assigned roles and no supplied game logic. The agents planned the run, wrote programs, and debugged those programs as events unfolded.

[ALLOY]: Researchers watched through a live dashboard and could pause or stop the system, though they report that intervention wasn’t needed. The convincing part isn’t the boss fight by itself. Four agents divided labor and preserved useful state using communication, shared memory, and code produced during play.

[NOVA]: It doesn’t prove that the same group stays reliable in business systems, where permissions and consequences are very different. It does show agents adapting together across a task too long and messy to solve with one polished prompt.

[PAUSE]

## [12:21] Grok Voice 3.0 Tops Speech-to-Speech Index at the Same $0.08 a Minute

[NOVA]: Grok Voice 3.0 now leads Artificial Analysis’s Speech-to-Speech Index with a score of 86.9. Grok Voice 2.0 scored 81.3, GPT-Live-1 in its Astra Medium configuration scored 83.2, and Gemini 3.8 Live with extended thinking on high scored 82.6. The new model keeps the same Voice Agent API price as its predecessor: eight cents per minute.

[ALLOY]: That price matters because the performance isn’t confined to one synthetic test. Artificial Analysis records 98.5 percent on Speech Reasoning Big Bench Audio, an Elo score of one thousand seventy in its human-preference speech arena, 94.8 percent task completion, and 97 percent on Full Duplex Bench. Full duplex means the model can manage the untidy parts of conversation—pauses, interruptions, and people speaking over it—rather than waiting politely for a clean audio turn.

[NOVA]: ServiceNow’s EVA-Bench covers more than two hundred enterprise voice-agent scenarios. Grok Voice posts seventy-four percent accuracy there and leads its combined measure of accuracy and user experience. ServiceNow described it as a new frontier in the tradeoff between those goals. I’d still treat the benchmark results as publisher and evaluator claims, especially where configurations differ. The deployments give us another view. Tesla says millions of in-car conversations use the system daily for calendars, email, coffee orders, and dinner bookings.

[ALLOY]: Starlink call centers are routing twenty thousand calls a day through Grok Voice in multiple languages. Roughly seventy percent resolve without a human, and about one-quarter of sales calls end in a purchase. Okay, those are unusually concrete operating numbers. Existing agents using xAI’s rolling Grok Voice endpoint were migrated without code changes. Sub-second latency, unchanged pricing, stronger reported conversational scores, and substantial live traffic make 3.0 more than a model-card win. It puts pressure on voice systems that sound impressive in a demo but become too slow or expensive at call-center scale.

[PAUSE]

## [13:52] xAI's $30 Bundle Puts Grok Models Inside Cursor

[ALLOY]: xAI’s new bundle is aggressive: thirty dollars a month combines the Grok assistant, Grok Bot, Cursor’s coding agent, and X Premium. The company frames that tier as replacing around ninety dollars in separate subscriptions. The products share a pool of Grok usage spanning chat, voice, image and video generation, and coding inside Cursor. Third-party models remain available in Cursor on Premium and higher tiers, but their usage is charged separately through API top-ups at list price. The free tier includes daily Grok access and a starter Cursor allowance. Plus costs eight dollars a month. Premium costs thirty dollars and includes four times the Plus usage. Super costs one hundred dollars with fifteen times the Plus allowance, while Ultra reaches two hundred dollars with fifty times that baseline.

[NOVA]: The team offer may matter more than the consumer bundle. Premium, Super, and Ultra are available per seat at those prices, replacing the older Cursor Teams structure while adding three times the coding usage, single sign-on, administration, consolidated billing, analytics, and SOC 2 compliance. Enterprise accounts get one dashboard and a shared pool spanning Grok and Cursor. Existing subscribers can keep their plans or move during the rollover window with prorated refunds. I’m torn too: bundling can make coding access dramatically cheaper, but it ties social media, general assistance, media generation, and software development to one vendor’s usage pool. Thirty dollars is a sharp acquisition price. Whether people reorganize all four habits around it is the much harder question.

[PAUSE]

## [15:29] mcp-use 2.10 lands for a fullstack MCP framework covering ChatGPT, Claude, and agent servers

[NOVA]: mcp-use two point ten arrived October fourteenth with a broad fullstack pitch: one open-source framework for creating MCP applications that appear in ChatGPT and Claude, while also building MCP servers that other agents can call. The repository has ten thousand seven hundred seventy-two GitHub stars. It’s aiming at both sides of the connection: the interface a person encounters and the tools an agent invokes behind it.

[ALLOY]: That bidirectional scope is the attraction. A team can build the user-facing application and the agent-facing tool surface in the same project instead of maintaining separate frameworks. MCP gives assistants a standard way to discover tools and call them with structured inputs, so the server side can serve multiple agent runtimes rather than one custom integration. Shared project code can also keep the visible controls aligned with the operations the server actually exposes.

[NOVA]: I’m interested, but “write once” always meets platform reality eventually. ChatGPT and Claude can evolve their application surfaces at different speeds, and a unified layer then has to absorb the divergence. Even so, mcp-use has enough adoption to be a credible consolidation choice. The two point ten release continues that work, while its core attraction remains architectural: front-end MCP experiences and back-end agent tools share one codebase. That can reduce duplicated plumbing and keep the interface a person sees closer to the capabilities an agent invokes. It’s a bet that MCP becomes application infrastructure, not merely a connector buried inside an assistant.

[PAUSE]

## [16:55] Third Moment Research Runs 10,000 Agents for 36+ Hours Straight

[NOVA]: Third Moment Research says it is sustaining ten thousand AI agents for more than thirty-six hours at a time. The stack uses GPT-6 Astra and GPT-6.1 Sol as foundation models, Codex for code and execution, and Daybreak for cybersecurity work. OpenAI featured the lab’s setup in its news coverage this month.

[ALLOY]: Ten thousand is the headline, but duration changes the kind of system we’re discussing. Most agents finish in seconds or minutes. Once work spans a day and a half, jobs overlap, information accumulates, and one failed action can affect many later decisions. What do we actually know about how these agents improve over that run?

[NOVA]: Third Moment describes them as holding focus across days and getting better through continued use. The disclosed material supports the scale, duration, and layered model roles, but it doesn’t quantify that improvement. So I wouldn’t turn the phrase into a claim of autonomous learning. What we can say is that the lab has organized different systems around distinct responsibilities rather than expecting one model to handle reasoning, execution, and security equally well.

[ALLOY]: That’s still a significant operational marker. Ten thousand concurrent agents running beyond thirty-six hours require scheduling, state management, and recovery on a different scale from a chat assistant or a one-shot coding task. OpenAI’s decision to highlight the work also shows where its platform ambitions are going: persistent fleets, not isolated prompts. I want the next disclosure to show what useful work survives the whole run and how often humans intervene. Until then, the achievement is sustained orchestration at scale, not proof that ten thousand agents are automatically better than a smaller, carefully designed group.

[PAUSE]

## [18:25] Block's security team cuts threat response to minutes with OpenAI

[ALLOY]: Block’s security team is using OpenAI models inside threat investigation and remediation, with candidate patches now arriving in minutes. That’s a far more consequential placement than asking a chatbot to summarize an alert.

[NOVA]: The model sits between detection and a proposed fix. It receives the investigative context analysts use, helps examine the threat, and produces remediation code while the security team retains decision authority. The human boundary matters because a fast patch can also be a wrong patch, and security changes often touch authentication, permissions, or production access. Block’s reported improvement concerns response time: moving from a detected problem toward a plausible correction in minutes.

[ALLOY]: And minutes can materially change an incident. Attackers exploit delay; defenders traditionally lose time moving among alerts, logs, affected code, and the people authorized to change it. A model that links those surfaces can compress the handoff without becoming the final approver. That’s not glamorous autonomy, but it’s valuable leverage in the period when every additional minute can widen exposure.

[NOVA]: I’d be careful about generalizing from one company’s result, because Block’s internal context and security engineering discipline matter. But the use is concrete and mature: investigation, patch proposal, human judgment. It also reframes enterprise coding agents. The valuable unit isn’t always a completed feature. Sometimes it’s the interval between discovering dangerous behavior and putting a reviewable fix in front of the person responsible for the system. In security, shrinking that interval can matter more than producing a larger volume of code.

[PAUSE]

## [19:35] Small Vision Model Gets Draft Boost for Local AI

[NOVA]: OpenBMB has also released a GGUF-quantized DSpark draft for the much smaller MiniCPM-V 4.7 one-billion-parameter target. The draft checkpoint is about two hundred thirteen and a half million parameters, with five draft layers generating fifteen candidate tokens per forward pass. The target verifies those candidates before they become output. It supports image-and-text work and is designed for on-device or edge deployment, where every saved target-model step can improve responsiveness. OpenBMB reports an acceptance length of 5.891 on math tasks and 4.752 on optical-character-recognition benchmarks. In plain language, several proposed tokens survive each verification step on average.

[ALLOY]: Honestly, this may be the more relatable release. The thirty-five-billion-parameter version proves speculative decoding at substantial scale, but a one-billion-parameter vision model belongs on much more modest hardware. The downloadable set includes the matching target, its vision projector, and the draft, with an eight-thousand-one-hundred-ninety-two-token example context. The documented local configuration pairs a compressed target with a higher-precision draft and supports GPU offloading through llama.cpp. As with the larger checkpoint, the draft is coupled to its target rather than interchangeable with unrelated vision models. Verification remains authoritative, so a rejected proposal costs speed instead of changing the intended output. For local image understanding, document reading, and visual tool use, a two-hundred-million-parameter helper advancing several verified tokens at once can be more valuable than replacing the whole stack with a larger model that no longer fits.

[PAUSE]

## [21:16] GitHub Copilot to Deprecate Several Models on November 16

[NOVA]: GitHub will retire several models from Copilot on November sixteenth. The cutoff applies across Copilot Chat, inline edits, ask mode, agent mode, and code completion, so changing from one Copilot surface to another won’t preserve access to an affected model.

[ALLOY]: That coordinated cutoff is the notable part. Chat, code generation, inline modification, and agent execution all change together. An engineering organization can therefore see behavior shift across several workflows even while the Copilot interface looks unchanged. Shared instructions, internal examples, and team conventions built around a retired model may produce different results after the transition. And because those surfaces support different kinds of work, one underlying catalog change can affect quick completions, conversational explanations, and longer autonomous edits at once.

[NOVA]: GitHub’s changelog identifies the affected models and its supported alternatives. This isn’t a product shutdown; it’s a reminder that a hosted coding assistant’s model catalog is a moving dependency. Copilot may look like one stable service from the outside, but the reasoning systems underneath it can change on a published deadline. November sixteenth is when teams using those models will feel that change. The effects may reach output style, latency, context handling, and the way agent mode approaches a repository, even though the buttons and menus remain familiar.

[PAUSE]

## [22:15] GitHub Project Radar

[NOVA]: Codebase Memory MCP is moving fastest in the radar group: forty-six thousand seven hundred ten stars, up three thousand seven hundred fifty-six—or 8.7 percent—in thirty days. Its .12 release landed October fifteenth. The zero-dependency static binary indexes code across one hundred sixty-two languages into a persistent knowledge graph, letting agents follow cross-file relationships through graph queries instead of repeatedly loading whole files. Nanobot sits even higher at forty-nine thousand ninety stars, up one thousand seventy. Its .3.5 release packages a self-hosted personal-agent framework with a web interface, tools, memory, MCP, automation, chat applications, and multi-agent workflows.

[ALLOY]: Those two fit together: Nanobot can coordinate persistent agents, while Codebase Memory gives them a structured map of a repository. The third project takes MCP somewhere visual. MCP for Blender enters with thirty-one thousand one hundred sixty-three stars and exposes Blender scene operations as callable tools. It’s a community project, not an official Blender Foundation product, but it turns 3D changes into structured agent actions rather than improvised interface control. That echoes Pascal Editor: agent tooling is moving beyond text and code into spatial production systems.

[PAUSE]

## [23:35] Model Discovery Check

[NOVA]: Reflection’s Beam 1.0 is the heavyweight arrival: five hundred one billion total parameters, twenty-three billion active per token, and a one-million-token context window. It accepts and produces text through OpenRouter’s API. Reflection positions the open-weight reasoning model for coding and long-horizon agent workflows, using sparse experts to provide large total capacity without activating the full network on every token.

[ALLOY]: MiniCPM-V 4.7 gets its speed boost through OpenBMB’s larger DSpark checkpoint. The draft has roughly three hundred eighty-nine million parameters, works with an eight-thousand-one-hundred-ninety-two-token configuration, and predicts text for the thirty-five-billion-parameter vision-language target. It proposes fifteen candidates per pass; OpenBMB reports 3.501 accepted tokens on general text and 7.387 on code generation.

[NOVA]: The compact DSpark release has about two hundred thirteen and a half million parameters with the same documented context size. Its five layers propose fifteen text tokens for the one-billion-parameter MiniCPM-V target, including during image-and-text workloads. OpenBMB reports acceptance lengths of 5.891 on math and 4.752 on optical character recognition, making it especially relevant to compact local vision systems.

[PAUSE]

## [24:55] Local LLM Spotlight

[ALLOY]: Humanizer from jialinyyzz is trending on Hugging Face with one thousand eight hundred eight likes and more than eighty-five thousand six hundred downloads. It’s a text-generation and rewriting model built around the Gemma 4 Unified family, distributed in GGUF and Safetensors formats. Its tags cover paraphrasing, style transfer, image-to-text interaction, and general rewriting. The attraction is focused transformation rather than a giant general-purpose agent: existing language can be reshaped in tone or presentation locally. That narrower purpose can also make deployment easier to reason about than handing every rewrite to a broad conversational model. Its model card carries the applicable license, compatible runtime, context limits, hardware needs, and measured behavior for deployment decisions.

[PAUSE]

## [25:40] Extra Research Candidates

[NOVA]: OpenBMB’s one-billion-parameter MiniCPM draft repository goes deeper on the five-layer, two-hundred-thirteen-million-parameter DSpark checkpoint and its fifteen-token proposal cycle. FastMCP offers a Pythonic, decorator-driven route to MCP servers and clients; its 4.1 release landed October eighth, the repository was active October sixteenth, and it has more than twenty-eight thousand stars.

[ALLOY]: Microsoft’s MCP for Beginners connects that tooling to education, with practical examples across .NET, Java, TypeScript, JavaScript, Rust, and Python. FastMCP reduces the framework code needed to expose tools, while the curriculum shows how the same protocol maps across major programming ecosystems.

[PAUSE]

## [26:35] Closing

[NOVA]: For the supporting specifications, sources, and links behind everything you heard, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.
