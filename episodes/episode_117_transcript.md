# AgentStack Daily EP117 — GPT-6 Astra Cracks a 2005 Enigma as Mistral Releases a 675B Apache 2.0 Flagship

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily.

[NOVA]: GPT-6 Astra reportedly cracked a German Army Enigma message that had resisted cryptanalysts since 2005. It chose the target, connected it to a previously solved transmission, wrote its own search software, worked around transcription errors, and recovered a key complicated by a rare wheel turnover. That’s not a chatbot retrieving trivia. It’s a model conducting a two-day investigation across cryptography, code, and archival research.

[ALLOY]: And Mistral has delivered the other kind of shock: a six-hundred-seventy-five-billion-parameter open-weight flagship under Apache Two, plus a one-hundred-twenty-three-billion-parameter coding model aimed at agents that stay with a software task for hours. People can build commercial systems on the flagship, send coding agents through enormous repositories, or put a seven-billion-parameter vision-and-action model onto a robot that predicts both future video and physical movement.

[NOVA]: Today, you’ll hear how Astra broke MVUEH, what Mistral’s two new models actually offer, and why a tiny decision model can enforce agent guardrails on an ordinary CPU. Hermes Agent shipped 9.24, Ando gave AI agents identities and inboxes, and Claude Opus 5.5 entered GitHub Copilot with a million-token context window.

[PAUSE]

## [02:00] Agent Stack Release Readout: Hermes Agent 9.24

[NOVA]: Hermes Agent shipped 9.24 as one stable artifact, tagged internally at point twenty-one point five, consolidating roughly four hundred sixty merged pull requests since the prior patch. The measured development window is much larger than that merge count suggests: sixteen hundred ten non-merge commits, forty-eight hundred twenty-eight changed files, about one hundred sixty-four thousand lines added, and one hundred forty-nine thousand removed. Nous Research says the release feeds Docker images, Hermes Cloud, and hosted deployments. Desktop received the densest visible work. Its plugin kit now exposes composer drafts, session-list decorations, sidebar preferences, model labels, typed bridges for settings and skills, sandboxed embedded views, appearance controls, and events from plugin backends. A Simple and Advanced interface split reduces clutter for newcomers without hiding deeper controls. Connectors replace the old Model Context Protocol tab, newly installed plugins can expose a direct Connect Now path, and onboarding presents plugins beside connectors. French, German, and Spanish catalogs are complete, while right-to-left and left-to-right text direction becomes configurable. Custom models can appear in composer and settings pickers, dictation and function-key shortcuts are wired in, and profiles can stop, start, or restart independently. A standalone gateway option can also keep one profile outside the shared host arrangement.

[ALLOY]: That’s a remarkable amount to hide beneath the word patch. The terminal surfaces gain a live dock for the standing goal and queued prompts; webhook deliveries can mirror into the relevant chat session; hosted desktop images add Bot Screen; and the kanban view gets a two-column ticket window with formatted task text. The model catalogs add GPT-6 Sol, Terra, Luna, and Claude Opus 5.5. Official plugins arrive for Blender Lab and NVIDIA’s app and Broadcast tools, while dozens of community plugins join the catalog. Performance work touched configuration loading, tool registration, gateway messages, and model selection. What stands out is the connective tissue: Hermes is becoming less like one agent screen and more like a host for profiles, plugins, connectors, and several interfaces sharing the same underlying work. A plugin can contribute interface elements, backend events, settings, skills, and tools rather than behaving like a narrow command. Meanwhile, independent profile controls reduce the blast radius when one workspace needs to restart. Calling this a patch is technically accurate, but emotionally misleading.

[PAUSE]

## [03:19] Mistral's Devstral 2 2512 Targets Long-Running Coding Agents

[ALLOY]: A one-hundred-twenty-three-billion-parameter dense coding model sounds huge even before you call it open weight. What makes Devstral 2 more than another model that completes the next function?

[NOVA]: Mistral built it for agentic coding: multi-step software work involving repository exploration, edits, tool calls, error recovery, and repeated verification. Devstral 2 accepts two hundred sixty-two thousand one hundred forty-four tokens, commonly rounded to a two-hundred-fifty-six-thousand-token context window. That gives an agent room for a substantial codebase, the conversation, tool output, and a long trail of earlier actions. More context doesn’t guarantee that the model will use every detail correctly, but it delays the moment when history must be compressed or discarded. That matters during a long refactor because forgotten assumptions create contradictory edits: one file adopts a new interface while another quietly preserves the old contract. The model is available through OpenRouter, making it accessible through an existing routing layer without a team first standing up one hundred twenty-three billion parameters of infrastructure.

[ALLOY]: I’m interested, with one eyebrow raised. Coding puzzles reward a clean final answer; real agent work punishes a model that loses track of a renamed interface forty minutes later. Devstral’s open weights and long window make that longer behavior inspectable in a way closed systems often aren’t. Teams can study how it uses tools, adapt it to a codebase, and choose their own serving environment. Mistral calls it a state-of-the-art open-source coding model, but sustained repository work will decide whether that label sticks. If it can preserve intent across hundreds of files, several failed attempts, and a stream of compiler or test output, it becomes a serious foundation for coding products rather than merely a very large autocomplete engine. The meaningful contest is no longer who writes the prettiest isolated function. It’s who can stay coherent when software work gets messy.

[PAUSE]

## [04:46] Mistral Ships a 675B Open-Weight Flagship on Apache 2.0

[NOVA]: Mistral Large 3 arrives with six hundred seventy-five billion total parameters, but it activates forty-one billion for each token. That’s a sparse mixture-of-experts design: instead of sending every word through the entire network, the model routes it through a smaller selection of specialized parameter groups. It aims to draw on the breadth of a huge model without paying the full computation cost at every step. The context window reaches two hundred sixty-two thousand tokens, enough for long documents, extensive conversations, and substantial collections of code in one request.

[ALLOY]: Apache Two is the part that made me sit up. The license permits commercial use, redistribution, and modification with attribution. A company can self-host it, adapt it, or build a paid product around it without negotiating a special frontier-model agreement. Open weights don’t make a six-hundred-seventy-five-billion-parameter system cheap; the inactive experts still have to be stored, moved, and served. But legal permission and technical access are aligned in a way they rarely are at this scale.

[NOVA]: Let’s keep the superlatives under control. Mistral calls Large 3 its most capable model, while the listing establishes its architecture, context length, distribution, and license. Those are important facts, but they don’t prove that it beats every closed flagship across reasoning, code, vision, or tool use. And forty-one billion active parameters describe computation per token, not the complete memory footprint. Serving the full expert pool remains a serious engineering job.

[ALLOY]: Fair pushback. Still, this widens the field. Research groups can inspect a frontier-scale sparse model. Enterprises with sensitive data can keep inference inside their environment. Model companies can adapt a permissively licensed base instead of choosing a smaller system mainly because the terms are workable. Paired with Devstral 2, Mistral covers a specialized coding-agent lane and a general flagship lane: one dense specialist, one giant sparse platform. That’s an aggressive open-weight release pair.

[PAUSE]

## [06:01] GPT-6 Astra Solves Enigma Message That Stumped Cryptanalysts Since 2005

[NOVA]: On September fifteenth, cryptographer Carter Leffen directed GPT-6 Astra toward the Crypto Cellar Research archive of unsolved wartime messages. Astra chose MVUEH, a German Army Enigma transmission from 1941 that had been public and unbroken since 2005. Roughly two days later, it had a solution. The model suspected that MVUEH shared plaintext with SIPVX, another message from the same day that Alex Shovkoplyas cracked in 2017. It used the repeated place name “Rosenow Rosenow” as a crib—that means a guessed fragment of the original message—and wrote Python and C-plus-plus software for an Enigma simulator and a Bombe-style key search.

[ALLOY]: Okay, that’s actually wild. The model didn’t merely search combinations faster. It formed a historical connection, selected a plausible known phrase, built the machinery, and kept investigating. What made the message so resistant?

[NOVA]: Several complications stacked together. The recovered wheel order was two-five-three rather than the five-one-two arrangement used by other messages from July tenth, 1941. The left wheel also advanced at the seventy-second letter, an unusual turnover that broke assumptions behind earlier efforts. The recorded ciphertext contained transcription mistakes too. Astra had to find a candidate that survived imperfect source material rather than solving a polished classroom cipher. It also surfaced references to German Federal Archives volumes matching real holdings that weren’t listed on the Crypto Cellar page. Veteran cryptanalyst Frode Weierud, who maintains the archive, said locating those references had taken him weeks and described Astra as behaving like a professional cryptanalyst and archival researcher.

[ALLOY]: That combination matters more than the slogan that AI cracked Enigma. Enigma is understood; this message was difficult because evidence was messy, prior assumptions were wrong, and useful clues were scattered across history, archives, and earlier cryptanalysis. Astra reportedly chose a path, wrote specialized tools, revised around anomalies, and connected records that humans had found separately. One result can’t establish dependable autonomy across every investigation, but it demonstrates why long-running agents are becoming consequential. They can join code, search, inference, and persistence into one sustained attempt—and occasionally make experts say, “Wait, it found what?”

[PAUSE]

## [07:58] Claude Opus 5.5 Lands in GitHub Copilot for Agentic Coding

[NOVA]: Claude Opus 5.5 is now available inside GitHub Copilot for agentic coding, long-running tasks, and knowledge work. It accepts text and images, returns text, and supports a one-million-token context window—roughly fifteen hundred pages of ordinary text. GitHub describes an adaptive-reasoning setup that can spend more effort on difficult work and use lighter responses when appropriate. Artificial Analysis scores it at fifty-eight on Intelligence Index version four point three point two, against a median of twenty-six. That combined evaluation covers coding, science, terminal work, and broad reasoning. The model generated two hundred sixty million tokens during the index run, nearly three times the median, so the strong score came with substantial output.

[ALLOY]: Which leads directly to cost: four dollars per million input tokens and twenty dollars per million output tokens. Artificial Analysis puts an average index task at five dollars and ninety-eight cents. Reused prompt prefixes can receive a ninety-five-percent cache discount, which helps when the same repository context appears repeatedly. Access through Copilot is the immediate change. A developer can pair a screenshot with a code request, keep a large repository and lengthy work trail in context, or hand over a multi-stage refactor without moving into another product. I’m excited by the capability, but I don’t buy “daily default” for every task at that output price and verbosity. Opus 5.5 looks strongest when the work is expensive enough that deeper reasoning can prevent a much larger human bill.

[PAUSE]

## [09:39] Ando Comes Out of Stealth With a Slack Rival Built for Humans and AI Agents

[ALLOY]: Ando’s pitch is wonderfully blunt: stop making humans copy an agent’s work into the company chat. Is this truly a Slack replacement, or an agent wrapper wearing channels and direct messages?

[NOVA]: Founder Sara Du presents it as a workplace messenger designed around both humans and agents. Each agent receives its own identity and inbox. It can participate in channels, direct messages, groups, and transcribed calls; browse conversations; choose which channels to join; enter without an explicit tag; and contact coworkers when it believes something matters. Du reached that conclusion while helping companies build Model Context Protocol servers in 2025. Teams wanted agents inside Slack, but people still had to move context and answers between separate systems. She calls those human intermediaries “meat proxies.” Ando has raised twenty million dollars across pre-seed and seed rounds from Accel, Index Ventures, and Emergence. Early customers span software, real estate, and finance in fifteen countries, mostly in smaller teams.

[ALLOY]: The strongest example is also the one that should make managers slightly nervous. An Ando agent noticed two channels discussing the same problem, created a group conversation, supplied the shared context, and proposed a decision without being asked. That can eliminate coordination drag because an agent can read more conversations than any one person. It also gives software discretion over when to interrupt, whom to gather, and what organizational context to expose. Slack has rebuilt its bot as an agent, Microsoft is embedding Copilot into Teams, and Jack Dorsey’s Buzz is aimed at developers, so Ando isn’t entering an empty market. Its bet is that native agent identity—not another assistant panel—will define the next workplace messenger. If that works, “who belongs in this channel?” becomes a question about software colleagues as well as humans.

[PAUSE]

## [11:38] Fastino's 340M Open Decision Model Runs Agent Guardrails on CPU

[NOVA]: Fastino’s GLiNER two point five Decide is a three-hundred-forty-million-parameter open-weight model for the small judgments agents make constantly: which tool fits, whether content is safe, which intent applies, and which structured route comes next. It doesn’t generate a paragraph. A developer supplies content and a schema of typed questions, and the model returns structured answers with probabilities, confidence, and feasibility flags. Questions can constrain one another, so related decisions don’t contradict each other.

[ALLOY]: That sounds modest until the decisions disagree. Fastino shows a prompt-injection example where independent decoding detects an attack with point-eight-two confidence yet labels the same prompt safe with point-five-two confidence. Those two outputs can’t drive one coherent policy.

[NOVA]: Joint decoding resolves them together. A schema rule says detecting harm requires an unsafe verdict, so the model returns unsafe and prompt injection as a consistent pair. It uses a DeBERTa version-three large encoder and was fine-tuned from GLiNER two large. The Apache Two weights can run on CPU, GPU, or in an air-gapped environment, and Fastino also provides hosted inference. Its Fast Decisions suite contains fifty-one hundred examples across seventeen datasets. The three-hundred-forty-million model averaged sixty-point-one percent exact match, led nine datasets, and beat a roughly four-billion-parameter Qwen three-point-five-class baseline by about two-point-six points. Support-intent accuracy reached seventy-five-point-three percent.

[ALLOY]: And the latency makes the CPU claim real rather than decorative: with fifteen labels and a batch of one, median response time was one hundred sixty-seven milliseconds on a forty-eight-core Xeon and thirty-eight milliseconds on a V-one-hundred GPU. Those are Fastino’s measurements, so broader reproduction still matters. But a compact, non-generative model has attractive properties for guardrails. It’s fast, structured, locally deployable, and less inclined to turn a routing decision into an essay. Fastino also offers a one-billion-parameter sibling and a two-hundred-eighty-seven-million-parameter multilingual version. Honestly, the smallest useful judge may prove more valuable inside an agent than another general model trying to do everything.

[PAUSE]

## [13:22] Black Forest Labs Ships FLUX 3 Action: A 7B Robot Brain

[NOVA]: FLUX 3 Action is a seven-billion-parameter open-weights model that controls robots by predicting future perception and movement together. It receives camera frames, the robot’s current state, and a text instruction. Then it generates future video frames alongside the next chunk of physical actions. Black Forest Labs reports a forty-two-point-nine-two-percent success rate across RoboLab’s one hundred twenty simulated tabletop tasks, ahead of NVIDIA Cosmos 3 Nano at thirty-six-point-eight percent despite using a much smaller backbone.

[ALLOY]: So it imagines the near future while choosing a motion, rather than treating vision and control as disconnected stages. That’s clever. Is it fast enough for useful hardware, though, or just clever in simulation?

[NOVA]: The published comparisons say the base checkpoint runs between one-point-five-two and three-point-nine-five times faster than Cosmos 3 Nano in eight-bit precision across workstation and data-center GPUs. A step-distilled variant reaches up to two-point-two-eight times the speed of pi-zero-point-five on the same hardware. There’s a timing wrinkle: the FLUX checkpoints predict two-point-one-three seconds of motion per call, while pi-zero-point-five predicts one second, so hardware and task length affect the apparent advantage. The full DROID policy needs about thirty-two gigabytes of GPU memory in sixteen-bit precision. Eight-bit quantization plus moving the text encoder elsewhere lets it fit on a twenty-four-gigabyte card. Hugging Face LeRobot integration and NVIDIA Jetson support extend it toward labs and edge deployments.

[ALLOY]: The physical trial is the persuasive part. Positronic Robotics ran thirty blind attempts across ten DROID tasks on a Franka arm. FLUX 3 Action completed twenty-eight, compared with twenty-seven for Cosmos 3 Nano, twenty for DreamZero, and thirteen for pi-zero-point-five. Teams can fine-tune it from demonstrations, and Black Forest Labs provides DROID and low-rank adaptation recipes. In one, an SO-one-oh-one robot learned pick-and-place behavior from roughly two hundred examples. The weights, code, and recipes use the FLUX Community License for non-commercial work. It’s not a universal robot brain, but seven billion parameters, deployment on a twenty-four-gigabyte card, and twenty-eight successful physical trials make it unusually tangible.

[PAUSE]

## [15:29] Oracle Invokes Force Majeure on New Mexico AI Data Center

[NOVA]: Oracle has sent a force-majeure notice concerning Project Jupiter, the enormous New Mexico data center being developed by a Blue Owl Capital unit. The clause gives Oracle protection to delay payments if the site misses its target to begin operating in 2028. Oracle remains the principal tenant; this is financial insulation against delay, not a declared exit. Project Jupiter faces public opposition and regulatory setbacks, while power, construction, permitting, and supply constraints can all push a large facility off schedule.

[ALLOY]: That turns the AI-capacity boom into contract language. A data center can be announced years before electricity reaches a rack, yet tenant commitments begin shaping financing immediately. Oracle is preserving flexibility if the concrete, permits, and megawatts fail to arrive together. Blue Owl still has an anchor customer, but it now has a public reminder that the customer won’t absorb every timing failure. Force majeure is more familiar around disasters and supply shocks; invoking it on an active AI project shows how exposed these infrastructure schedules have become. The compute race isn’t limited by demand. It can be limited by a local hearing, a transmission line, or a deadline that looked plausible on a spreadsheet.

[PAUSE]

## [17:06] Could Monkey Island's Grog Really Dissolve a Mug in 35 Seconds? A Chemist Models It

[ALLOY]: I love this one already. In The Secret of Monkey Island, a mug of grog survives about thirty-five seconds before dissolving. A University of Groningen chemist treated that gag as a real inverse problem: observe what happened, then calculate what the drink must have been. The paper uses the 2009 Special Edition and times the mug with a stopwatch. It assumes the mug is pewter, simplifies that to pure tin, and assigns the wall a two-millimeter thickness because the game supplies no measurement. From that geometry, the calculation estimates how many protons an acid would need to provide to perforate the cup in thirty-five seconds.

[NOVA]: Then comes the finest ingredients list in chemistry: sulfuric acid, battery acid, kerosene, propylene glycol, artificial sweeteners, rum, acetone, red dye number two, axle grease, pepperoni, and the mysterious SCUMM. Sulfuric acid and battery acid are the plausible drivers of rapid corrosion. Most of the others contribute little to attacking tin, and oily ingredients could even slow the process by coating the surface. No, pepperoni wasn’t the active reagent. I know—that’s disappointing.

[ALLOY]: The paper calls the result semi-quantitative, which is academic language for “we did real chemistry with assumptions supplied by a pirate comedy.” None of those ingredients explains the grog’s bright green color either. Still, the exercise has real scientific charm. The game supplies an outcome, incomplete dimensions, and an absurd recipe; chemistry converts those scraps into limits on what could plausibly happen. It won’t revise industrial corrosion tables, but it shows how a fictional gag can become a memorable problem in reaction speed, material thickness, and uncertain evidence.

[PAUSE]

## [18:50] AI That Thinks in DNA Pushes the Bio-Security Frontier

[NOVA]: Radical Numerics has emerged from researchers behind Evo and Evo-2, genomic language models developed at Arc Institute. Those earlier systems generated complete bacteriophage genomes from scratch, and synthesized versions produced functional viruses in laboratory work. The new company wants to extend genomic modeling across DNA, RNA, and proteins. DNA contains genes and the sequences that encode proteins, so a model trained on that language can encounter biological structure before adding three-dimensional protein information, epigenetics, or ordinary text.

[ALLOY]: That’s the exciting description and the alarming description in the same sentence. What evidence suggests these models can optimize biology rather than merely imitate familiar sequences?

[NOVA]: In one experiment, the team trained on RNA aptamers paired with performance scores. Aptamers are short molecules that fold into shapes and bind particular targets. The training data showed sequences improving step by step; when asked to continue that trajectory, the model recovered higher-scoring sequences it hadn’t seen. Radical Numerics interprets that as evidence that the system learned an optimization direction within biological language. Its leadership includes Eric Nguyen, Michael Poli, Stefano Massaroli, and Armin Thomas, drawing experience from Arc, Liquid AI, Stanford, and research associated with Yoshua Bengio and Chris Ré.

[ALLOY]: The dual-use pressure is unavoidable. Better sequence generation could accelerate vaccines, therapeutics, pathogen detection, and defensive analysis. The same ability expands what software can propose in biology, where a generated artifact may have consequences beyond a screen. Radical Numerics argues for advancing capability aggressively so defenders possess equally powerful tools. I understand that argument, but capability alone doesn’t guarantee defenders receive equal access, time, or institutional support. Cross-modal genomic models could connect DNA, RNA, proteins, and experimental outcomes in one design loop. If they do, access controls and biological evaluation become central evidence of credibility because the software isn’t merely describing life—it’s helping propose new biological designs.

[PAUSE]

## [20:38] Research Digest: Researchers Train Video Models to Track Hidden Objects Like Humans Do

[NOVA]: Video models can create convincing motion yet still lose track of an object once it passes behind something. A paper trending on Hugging Face examines object permanence—the understanding that an object continues to exist when it leaves view. The researchers find that current video generators often lack those physical expectations even when individual frames look realistic.

[ALLOY]: Their WROP dataset teaches situations resembling early physical intuitions: a ball rolls behind a chair, remains the same ball, and should emerge consistently. That sounds elementary, but generated worlds fall apart when identities, positions, or shapes reset during occlusion.

[NOVA]: Better persistence matters beyond prettier video. A robot needs to remember where an object went while another object blocks its camera. A simulator must preserve hidden state rather than inventing a replacement on re-entry. A world model predicting future events needs continuity, not merely plausible pixels. WROP treats that missing common sense as something training data can address directly.

[ALLOY]: And I like the humility of that target. Before claiming a machine understands a physical world, ask whether it remembers the ball behind the chair. That tiny question exposes the gap between rendering motion and maintaining a coherent world.

[PAUSE]

## [21:42] Research Digest: AI Coding Agents Outperform Hand-Built Robot Planners

[NOVA]: A robotics study gave coding agents, including the terminal-based AI coding agent Claude Code, task descriptions plus simulator access. The agents wrote reusable planning programs within a fixed compute budget. Researchers froze those programs before evaluating unseen situations, so the agents couldn’t improvise after seeing the final cases. Across simulated environments from two robotics benchmarks, the agent-written planners achieved mean success rates ranging from fifty-six to ninety-five percent. Hand-engineered planners reached forty-seven percent on the directly comparable subset, while generated programs also held up better as object counts increased.

[ALLOY]: That’s a meaningful distinction: the coding agent performs the expensive exploration once, then ordinary executable planning code handles new instances repeatedly. It doesn’t erase robotics engineering; the simulator, objective, constraints, and transfer to physical machines still shape the result. But it turns months of hand-authoring into program synthesis, where an agent can revise its planner against a simulated environment. And it complements FLUX 3 Action rather than replacing it. One approach learns low-level actions from demonstrations and future-video prediction; the other asks a coding agent to invent reusable software that organizes a larger task. Robotics can absorb AI at both layers.

[PAUSE]

## [22:43] OpenAI Releases MentalHealthBench for Evaluating Mental Health AI Responses

[ALLOY]: Mental-health conversations expose a weakness in ordinary AI scoring: an answer may contain correct facts and still be dismissive, unsafe, or wildly inappropriate. How does OpenAI’s MentalHealthBench try to measure that difference?

[NOVA]: OpenAI built MentalHealthBench with input from mental-health experts and released it on September twenty-third. It uses realistic conversational situations to evaluate whether an AI response is both helpful and safe. Expert-informed expectations define good behavior rather than reducing the task to factual recall or multiple choice. That includes recognizing when a conversation calls for escalation or professional support instead of letting an assistant improvise beyond an appropriate boundary. The benchmark gives developers, researchers, and model providers a shared evaluation surface for a domain where tone, judgment, and awareness of harm matter alongside information. Products such as wellness coaches, therapy-adjacent journals, and triage assistants can sound polished while responding badly at precisely the moment a person is most vulnerable.

[ALLOY]: And that’s overdue. A shared benchmark lets teams report behavior across documented situations instead of pointing to a handful of comforting demonstrations. It also raises the standard for domain-specific evaluation. One general safety score can’t represent every sensitive setting because mental health, biology, finance, and medicine each contain different ways for a plausible answer to cause harm. Wider use will determine how influential MentalHealthBench becomes, especially if independent researchers extend it or compare its expert judgments with other clinical frameworks. Still, the release moves the conversation from “our assistant sounds caring” toward observable behavior in difficult exchanges. Empathy-like language is cheap for a model to generate; appropriate judgment under emotional pressure is much harder, and that’s what an evaluation should expose.

[PAUSE]

## [24:20] GitHub Project Radar

[NOVA]: Three repositories are moving fast. HKUDS Nanobot has forty-eight thousand five hundred sixty-one stars, up thirteen hundred ten over thirty days, and released point three point five on September fifteenth. It’s a lightweight, self-hosted personal-agent framework with a web interface, tools, memory, Model Context Protocol support, automation, multi-agent workflows, and chat integrations. Codebase Memory MCP is close behind at forty-four thousand eight hundred sixty-six stars, but its thirty-day growth is sharper: fifty-one hundred eleven stars, or twelve-point-nine percent. Release point eleven also arrived September fifteenth. It indexes repositories into a persistent knowledge graph spanning one hundred fifty-eight languages and advertises sub-millisecond queries with major token savings.

[ALLOY]: Those two connect naturally: Nanobot supplies the agent environment, while Codebase Memory gives an agent a structured map of a repository instead of making it reread files repeatedly. The third project turns that same tool protocol toward creative work. MCP for Blender enters tracking with twenty-nine thousand three hundred fifteen stars and was updated September twenty-fourth. It lets language models control Blender through a community plugin. That’s already a serious audience for a first tracked appearance. Together, these repositories show the protocol spreading across personal agents, code intelligence, and three-dimensional production—not as another chat feature, but as a way for models to operate specialized software.

[PAUSE]

## [25:38] Model Discovery Check

[NOVA]: Devstral 2 is the specialist pick: a one-hundred-twenty-three-billion-parameter dense transformer with a two-hundred-sixty-two-thousand-token context window, open weights, and availability through OpenRouter. Its differentiator is sustained agentic coding—holding repository context, tool results, and earlier decisions across a long software task rather than optimizing only for isolated code completion.

[ALLOY]: Mistral Large 3 is the general flagship: six hundred seventy-five billion total parameters, forty-one billion active for each token, the same two-hundred-sixty-two-thousand-token window, and an Apache Two license. Its sparse expert design concentrates computation while preserving a much larger parameter pool. Frontier scale, permissive commercial terms, and open weights make it far more consequential than a routine marketplace listing.

[PAUSE]

## [26:32] Local LLM Spotlight

[NOVA]: The local release is abenzerps/Qwen-Image-2.1-Uncensored-GGUF, trending on Hugging Face with sixteen hundred ninety-four likes and more than seven hundred fifteen thousand downloads. It’s a quantized text-to-image model derived from Qwen Image two point one, packaged in GGUF and tagged for ComfyUI workflows.

[ALLOY]: Quantization lowers numerical precision so large weights can run more practically on local hardware, while GGUF is a weight format supported by local inference tooling. “Uncensored” describes how the variant is positioned; it isn’t a promise about quality, licensing, or responsible output. Still, more than seven hundred fifteen thousand downloads is substantial traction. It reflects strong interest in image generation that stays under local control and connects to familiar node-based creative pipelines.

[PAUSE]

## [27:18] Extra Research Candidates

[NOVA]: Introducing MentalHealthBench brings expert-informed judgment to realistic mental-health conversations, while Kyutai Releases Voice of Reason: A Speech-Native Model that Solves Spoken Math with Reinforcement Learning moves reasoning directly into audio. Kyutai’s two open-weight speech-to-speech models build on GLM-four-Voice-nine-billion, and supervised tuning plus reinforcement learning reportedly lift spoken GSM-eight-K accuracy from twenty-seven-point-three to seventy-seven-point-one percent without a transcription stage. One evaluates sensitive conversation; the other reasons without first flattening speech into text.

[ALLOY]: And abenzerps/Qwen-Image-2.1-Uncensored-GGUF trending on Hugging Face adds the local creative side: sixteen hundred ninety-four likes, more than seven hundred fifteen thousand downloads, GGUF packaging, and ComfyUI compatibility. Put beside Voice of Reason, it shows open models spreading across native speech and local image generation, while MentalHealthBench asks whether increasingly natural interactions also remain helpful and safe when the stakes are human.

[PAUSE]

## [28:08] Closing

[NOVA]: For the supporting material behind these developments, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily.

[NOVA]: We'll be back soon.
