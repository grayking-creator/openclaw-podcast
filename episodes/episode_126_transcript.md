# AgentStack Daily EP126 — Gemini 4 Carbon Targets Long-Running Engineering and Cyber Defense

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily.

[NOVA]: Google says Gemini 4 Carbon can stay on a software-engineering or cyber-defense problem for days, work through dead ends, find a vulnerability, determine whether it can actually be exploited, and patch the underlying cause. That’s not a chatbot answering one more question. It’s a model being aimed at the long, messy middle of engineering work—where the first theory is wrong, the codebase is huge, and persistence matters as much as a clever first answer.

[ALLOY]: And that longer horizon is showing up in real systems. Retell’s OpenAI-powered voice agents now handle one hundred million calls a month. NVIDIA has squeezed an eight-billion-parameter model with four billion effective parameters into a four-gigabyte package for local assistants, interactive characters, and embedded interfaces. Anthropic’s platform engineers are separating an agent’s reasoning from the machinery that touches credentials, networks, and tools. Today: Gemini 4 Carbon, OpenAI’s results across mathematics and physics, production voice agents, two very different local-AI hardware pushes, evidence-distorting group memory, more selective agent training, and agents moving deeper into software security and legal contracts.

[PAUSE]

## [02:00] Gemini 4 Carbon targets long-running engineering and cyber defense

[NOVA]: Google announced Gemini 4 Carbon as its next frontier model, built around sustained agentic work rather than isolated prompts. Google says Carbon can run for days, recover from dead ends, trace subtle bugs through large codebases, and produce fixes. Cyber defense is where the claims become unusually specific. Carbon scored eighty-eight-point-two percent on Google’s SEC-bench Pro for vulnerability discovery, fifty-four-point-eight percent on ExploitGym for determining and carrying out exploit paths, and seventy-one percent on Collinear’s CWE-bench for repairing the code behind a weakness. Those are publisher-reported results, but they describe the whole defensive chain: find the flaw, establish whether it’s exploitable, and fix the root cause. Google also says Carbon more than doubled Argon’s success rate on its internal secure-code-generation benchmarks. That’s a much stronger claim than “better at coding,” because secure code depends on following consequences across files, tools, and repeated attempts.

[ALLOY]: The access model reflects the stakes. Carbon is starting with a subset of cyber defenders, then expanding gradually to trusted partners through Google’s Fairwind Program. Developers, businesses, and consumers are supposed to receive access later. Introductory pricing is two dollars per million input tokens and ten dollars per million output tokens, with cached input discounted by ninety-five percent; the later rates are four dollars and twenty dollars. That cache discount matters for a model that keeps revisiting a large repository over a multi-day job. Still, the consequential test won’t be whether Carbon can remain active for days. It’ll be whether that persistence keeps producing accurate progress instead of merely accumulating confident activity. Google’s benchmark numbers make the capability credible enough to watch, while the limited initial deployment gives defenders a chance to see how it behaves against real code, actual exploit paths, and fixes that have to survive outside a benchmark.

[PAUSE]

## [02:32] OpenAI Shares Model Results on Three Scientific Problems

[ALLOY]: OpenAI has put model-produced results in front of academic communities for three very different problems: the Kakeya conjecture in mathematics, the Exponential Time Hypothesis in theoretical computer science, and quantum chromodynamics in physics. NOVA, what changes when a model result is treated as material for researchers rather than presented as a finished scientific answer?

[NOVA]: It changes who carries the burden of proof. A Kakeya result has to survive mathematical scrutiny; work connected to the Exponential Time Hypothesis has consequences for how researchers understand the difficulty of computational problems; and quantum chromodynamics deals with the theory describing interactions among quarks and gluons. OpenAI is asking specialists to examine the reasoning, verify what holds, identify what doesn’t, and extend useful parts. The model output becomes a candidate contribution inside an existing scientific process. It doesn’t become accepted knowledge because the model produced a polished derivation. That distinction is essential when the subject is far beyond casual inspection.

[ALLOY]: I like the ambition, but the academic response is the result that matters now. Three fields receiving model-generated work at once shows that these systems can participate in highly specialized reasoning across distinct scientific languages. Verification determines whether that participation produces a new proof, a useful intermediate observation, a corrected argument, or simply a more interesting question. The valuable possibility is a faster loop between machine-generated ideas and researchers who know where an argument is fragile. The worrying possibility is that fluent work consumes expert attention without advancing the field. OpenAI’s framing puts researchers in the right role: not an audience applauding a machine’s answer, but active investigators deciding what the work can support and what deserves to be built on.

[PAUSE]

## [03:11] Retell’s OpenAI-powered voice agents reach 100M monthly calls

[NOVA]: Retell’s OpenAI-powered voice agents are now handling one hundred million calls every month, according to an OpenAI case study published October twenty-seventh. Retell says GPT-6 Astra led its voice-agent benchmark, while Codex helped the company reach an annual revenue run rate of one-point-six million dollars per employee. The call volume is the harder number to ignore. At one hundred million monthly conversations, small differences in response delay, misunderstood intent, or failed handoffs become enormous operating effects. Voice agents don’t get the luxury of a user rereading a paragraph; they have to follow interruptions, recover from ambiguity, and respond quickly enough that the interaction still feels like a call.

[ALLOY]: Okay, one hundred million is genuinely wild. It moves voice agents out of the “promising demo” category and into infrastructure. The Astra benchmark result comes from Retell, so I’d still treat it as the company’s measured preference rather than a universal ranking. But Retell is measuring models against a workload it actually operates at scale. That gives the result more practical weight than a generic conversational score.

[NOVA]: The revenue-per-employee figure tells a separate story: the company says its use of Codex has helped a relatively small workforce produce a very large revenue run rate. It doesn’t prove that every team gets the same leverage, but it shows how software assistance and an AI-native product can compound. And the two numbers shouldn’t be blurred together. Astra is tied to Retell’s voice-agent performance; Codex is tied to how the company builds and operates. One model is inside the product, another is helping create the product.

[ALLOY]: That separation matters because important AI businesses may use models at several layers simultaneously—customer interaction, engineering, debugging, and internal operations. Retell gives us a production reference with enough traffic to expose problems quickly. What comes next is visible in operating outcomes: whether call volume continues growing without service quality collapsing, and whether that extraordinary revenue-per-employee number holds as the organization and customer demands expand.

[PAUSE]

## [04:02] Anthropic separates the model from the agent’s actions

[NOVA]: Anthropic’s platform engineers are drawing a hard boundary between the model that decides and the system that acts. In an October twenty-seventh interview, Katelyn Lesse and Angela Jiang described the launch of Opus 5.5 and the managed-agent architecture behind the Claude Platform. The model’s reasoning, the harness that keeps work moving, and the sandbox where actions occur are decoupled. That lets the execution layer isolate processes, protect credentials, and control network access without expecting the model itself to enforce every boundary correctly.

[ALLOY]: That sounds obvious only after somebody says it. We don’t let a human analyst carry every production credential merely because they’re good at reasoning, so why would an agent receive unrestricted access just because its model is capable? Separating the brain from the hands means the harness can decide which action is allowed, the sandbox can contain what happens next, and the model can concentrate on choosing a useful step. It also creates a cleaner place for safety classifiers and model routing. Different decisions can be inspected or routed without giving every reasoning path the same authority.

[NOVA]: The difficult part is preserving progress while maintaining that separation. Anthropic’s team described long-running harnesses that continue work across context windows. A model can reach the end of one working context without the overall task losing its place. But continuity has to survive through explicit state held by the managed system; the model can’t simply rely on an infinitely growing conversation. That resembles Carbon’s long-horizon promise from earlier, except Anthropic is emphasizing the operating structure around the model rather than presenting persistence as one model capability.

[ALLOY]: And I’m more comfortable with that framing. A powerful model is still only one component in an agent that can touch code, networks, and credentials. Containment, state preservation, and controlled execution have to remain dependable when the work runs longer and the number of actions grows. Anthropic also distinguishes production safeguards from incidents that happen during training, which keeps two different safety problems from being mashed together. The larger consequence is architectural: managed agents can improve their reasoning models without rebuilding the entire execution boundary, and they can tighten tool controls without retraining the model. That modularity becomes increasingly valuable as agents stay active longer.

[PAUSE]

## [04:57] ASRock’s Radeon AI Pro R9700 targets local workstation inference

[NOVA]: ASRock’s Creator Radeon AI Pro R9700 gives local AI work thirty-two gigabytes of GDDR6 memory, six hundred forty gigabytes per second of bandwidth, and RDNA 4 support for FP8 matrix calculations. FP8 uses eight-bit numbers for model math, reducing the memory and compute required compared with higher-precision formats. The card is built around AMD’s Navi 48 processor with sixty-four compute units, one hundred twenty-eight AI accelerator cores, and a peak clock of two-point-nine-two gigahertz. ASRock rates dense FP8 matrix throughput at three hundred eighty-two-point-seven trillion operations per second, doubling that figure when sparsity lets the hardware skip zeros. A roughly thirty-billion-parameter model can fit with some video memory remaining. That’s the headline use: substantial local inference on a workstation card instead of sending every prompt and model state to a remote service.

[ALLOY]: The physical design may be just as important as the peak number. It’s a dual-slot blower card measuring two hundred seventy-one by one hundred eleven by thirty-nine millimeters, and a standard ATX system can hold as many as four. A blower pushes hot air out of the case, which matters when cards are packed together. The R9700 draws three hundred watts, described in the review as manageable for that design. Linux users can also enable soft error-correcting memory manually for more reliability. But thirty-two gigabytes creates a real tradeoff: AMD’s previous Radeon Pro W7900 carried forty-eight. RDNA 4 brings newer compute features and very strong low-precision throughput, while the smaller memory pool limits how large a model can remain entirely on one card. FP6 and FP4 models are processed as FP8 rather than using those lower precisions natively, too. So this isn’t “more of everything.” It’s a compact, dense workstation option whose value will depend on whether its inference speed and efficiency outweigh the lost capacity. Four cards could create serious local compute, but the single-card fit for the model someone actually needs remains the deciding constraint.

[PAUSE]

## [06:16] NVIDIA’s 4GB Bolt model targets local agent stacks

[ALLOY]: Four gigabytes for a model with eight billion parameters sounds like somebody is trying to make local agents fit where they previously couldn’t. What did NVIDIA actually package into Nemotron 3.5 Bolt?

[NOVA]: It’s an eight-billion-parameter text model with four billion effective parameters, compressed with Q4 K M quantization so the package fits into about four gigabytes. Quantization stores model weights with fewer bits, trading some numerical precision for a dramatic reduction in memory. NVIDIA says Bolt was further trained from Gemma 4 E4B Instruct and targets local voice assistants, device assistants, interactive personas, and embedded interfaces. It supports input and output lengths up to sixty-four thousand tokens, tool calling, an ordinary conversational mode, and reasoning controls. Reasoning can be turned on or off, and an application can set a runtime thinking budget. The model also has a documented way to acknowledge that a tool result is pending, then resume when the result arrives. That detail matters in voice or device interactions, where silent waiting can feel like a broken product.

[ALLOY]: And NVIDIA is claiming a fairly large measured improvement over the base model. In its own Q4 K M evaluation, Bolt scored fifty-five-point-six on MultiChallenge, compared with thirty-nine-point-three-six for Gemma 4 E4B Instruct. That number comes from NVIDIA under its own consistent evaluation harness, so it’s a publisher claim until others reproduce the comparison. Still, this isn’t merely a smaller file. NVIDIA is saying the additional training improved multi-turn behavior while preserving a memory footprint suitable for local deployment. A companion DFlash drafter supports speculative decoding, where a smaller helper proposes tokens so the main model can confirm several at once and respond faster. Access is direct: the model card permits commercial and non-commercial use and provides download instructions and a llama.cpp serving path. Llama.cpp is a lightweight runtime commonly used to run quantized models on local hardware. But the reasoning budget has a sharp edge: NVIDIA warns that restrictive token allocations can cut a thought process off mid-sentence. Four gigabytes makes Bolt easier to place on constrained systems; it doesn’t remove the need to match the available reasoning length to the job.

[PAUSE]

## [07:39] US Investments Add Chip Capacity and an Autonomous Weapons Test Range

[NOVA]: The White House has detailed industrial investments spanning semiconductor production, critical materials, fuel refining, and autonomous-weapons testing. North Carolina is set to receive up to one-point-five billion dollars for expanded semiconductor production. Sibelco is also expanding high-purity quartz and related-material production in Mitchell County. High-purity quartz is upstream of chipmaking, so increasing fabrication capacity without securing essential material inputs would leave part of the same supply chain exposed.

[ALLOY]: And the national-security side is much broader than chips. The administration is invoking the Defense Production Act to release one hundred fifty million dollars for expanded domestic refining capacity, aimed at greater diesel and gasoline production. In Montana, the Department of War is establishing a range for advanced weapons and technology testing, including autonomous weapons as well as space and electronic-warfare systems. That creates a dedicated physical environment for technologies that can’t be evaluated entirely in simulation. Autonomous systems have to encounter communications limits, terrain, interference, and the consequences of acting in the real world.

[NOVA]: The announced dollars are inputs, not finished capacity. A semiconductor facility has to be built, equipped, staffed, supplied, and brought to reliable production. Quartz expansion has to feed material of the required purity into that chain. The Montana range likewise matters only when programs begin using it and the resulting evaluations influence procurement or deployment. But taken together, these investments show AI-related infrastructure reaching far beyond data centers. Chips depend on minerals and factories; autonomous defense depends on physical ranges and communications environments; both depend on long development timelines.

[ALLOY]: That’s why I wouldn’t reduce this to an “AI investment” headline. It’s industrial policy meeting increasingly autonomous software. More domestic chip and material capacity could enlarge the hardware base available to computing systems, while a dedicated weapons range gives autonomous and electronic-warfare programs somewhere to confront physical constraints. The immediate facts are planned funding and facilities. The consequential evidence comes later: operating production lines, actual output, active test programs, and systems that perform under real conditions rather than just inside procurement language.

[PAUSE]

## [08:38] Research digest: Group memory can distort the evidence it preserves

[NOVA]: A group of language models can discuss a problem at length and still lose the useful evidence when one model compresses that exchange into memory. Choosing the rarest claims sounds sensible, but the research found that it performs no better than random selection on average. Choosing claims that look relevant can be worse, because persuasive decoys are relevant too.

[ALLOY]: The stranger result involves social proof. A final decision maker gives more weight to a fact when the memory says many agents supported it. Removing those attributions—or randomly assigning them while preserving the discussion order—improves accuracy. Even the full transcript can perform worse than keeping no notes. So compression alone isn’t the villain. Evidence can be distorted by what gets retained, how distractors remain balanced against support, and which claims appear to carry a crowd behind them.

[NOVA]: That cuts directly into multi-agent systems that treat a summary as neutral shared memory. A concise record can erase disagreement or make repetition resemble independent confirmation. Preserving more text doesn’t automatically rescue the decision. The important distinction is between remembering that several agents said something and retaining the evidence that made the claim credible. Group memory has to carry substance, not merely consensus-shaped metadata.

[ALLOY]: Which is a useful check on agent swarms: adding voices can manufacture confidence faster than knowledge. If one summarizer decides what survives and another model trusts apparent agreement, the group can amplify a plausible mistake without changing the underlying evidence at all.

[PAUSE]

## [09:43] Anthropic trained Claude on illegally obtained Stanford professors' books

[NOVA]: A federal judge ruled in May that Anthropic trained Claude using illegally obtained books written by more than ten Stanford professors, according to reporting published October twenty-seventh. The named authors include Tobias Wolff, Abraham Verghese, Chang-Rae Lee, Daniel Mason, Hayagreeva Rao, and Myra Strober. The dispute sits inside Bartz versus Anthropic and concerns texts that were scraped or pirated for model training. That’s not an abstract argument about whether machine learning is socially useful. It’s a legal boundary around how training material was acquired. A model developer may have a separate argument about whether training on a lawfully obtained work qualifies as fair use, but illegal acquisition creates a different question. The origin of the copy matters.

[ALLOY]: And the human stakes are direct. These are identifiable professors and writers whose books entered a commercial model-development process through copies the ruling described as illegally obtained. The judgment also matters for companies downstream from a model developer. They usually can’t inspect an entire training corpus, yet legal findings about provenance can affect the reputation and economics surrounding the models they rely on. I wouldn’t turn one ruling into a universal description of every training practice or every book in Claude’s data. The concrete finding concerns the works and acquisition conduct before the court. But it reinforces a distinction the industry can’t wave away: the legal analysis of learning from a work is not identical to the legal analysis of obtaining that work through piracy. As model companies compete on data quality and scale, provenance becomes part of the product’s liability story, not a historical detail buried behind the finished model.

[PAUSE]

## [10:37] Research digest: EnvSched Targets More Useful Agent Training Runs

[ALLOY]: Agent training burns through expensive rollouts—complete attempts involving tools, changing states, and checks for success. If only a limited number can be run, how does EnvSched decide which experiences deserve the budget?

[NOVA]: It schedules tasks together with their environments instead of treating task selection as an isolated choice. EnvSched learns from prior rollout history, favors task-environment pairs likely to reveal meaningful reward differences, and spreads work toward tools, interactions, and environments that have received less attention. It represents those pairs in a graph. Some connections reflect shared tools or verification structures within an environment; others represent broader similarity in execution and rewards.

[ALLOY]: Historical results estimate where a new rollout may produce useful variation. Environment quotas and a similarity penalty then keep the batch from filling with near-duplicates. That matters because repeated easy successes don’t teach an agent much, and repeated failures can be equally uninformative. With a fixed compute budget, EnvSched tries to spend more runs where good and bad behavior can actually be distinguished. It’s selection pressure for more informative experience, not simply more experience.

[PAUSE]

## [11:45] Greptile uses GPT-6 Astra to test software workflows

[NOVA]: Greptile is using GPT-6 Astra to move beyond reviewing proposed code and into testing how software behaves through user workflows. That distinction is substantial. A code diff can look reasonable while the resulting application still breaks when a person follows a real sequence across screens, services, or state changes. Workflow testing asks whether the feature works in use, not merely whether the changed lines appear coherent.

[ALLOY]: Greptile is also using OpenAI’s Daybreak for security work, adding vulnerability-oriented investigation to the same broader quality process. Codex addresses another expensive part of the cycle: rework after an issue is found. Together, Astra examines user-facing behavior, Daybreak contributes security analysis, and Codex assists with the code changes needed around those findings. I like the breadth, but three model names don’t automatically equal one smooth system. The value comes from whether their outputs connect cleanly enough to reduce repeated debugging.

[NOVA]: Exactly. Static review, behavioral testing, security investigation, and remediation observe different evidence. A reviewer may identify a suspicious code path; a workflow run may reveal that it fails only after a specific user action; a security agent may show why that state is dangerous; and coding assistance may shorten the correction. Greptile’s announcement places AI across that chain instead of pretending one review comment captures the entire software-quality problem.

[ALLOY]: The next meaningful results will be operational: fewer escaped bugs, less repeated work, and findings that developers accept because they reproduce in the application. Astra’s role is especially interesting because user workflows can reveal failures that source inspection alone misses. But developers still need an understandable connection from observed behavior to the code and proposed correction. If Greptile can preserve that thread, model-assisted review starts looking less like automated commentary and more like a continuous investigation of what software actually does.

[PAUSE]

## [12:43] CodeRabbit uses GPT-6.1 Sol for codebase security review

[NOVA]: CodeRabbit is applying GPT-6.1 Sol to security investigation across complex codebases. Its security agent examines risks and proposes fixes, while developers review both the finding and the remediation before deciding what changes. That human decision point is important: identifying suspicious behavior and producing a safe correction are separate tasks, and an attractive patch can still misunderstand the surrounding system.

[ALLOY]: What does codebase-wide investigation add beyond reviewing the pull request that happens to be open?

[NOVA]: Context. A vulnerability may cross authentication logic, shared libraries, configuration, and a downstream service even when the visible edit touches only one file. Looking across the codebase can connect a local change to those broader relationships. Sol gives CodeRabbit a model for that investigation, while the product keeps the proposed finding and fix in a developer-review workflow. The useful evidence will be whether those findings survive real security scrutiny and whether proposed repairs address root causes without introducing new behavior.

[ALLOY]: That’s the right boundary. Security review shouldn’t become “the model suggested a patch, so merge it.” CodeRabbit is pairing automated exploration with an accountable human choice. If the system can trace a risk across a complicated repository and present a correction with enough context for a developer to judge it, it can compress a very expensive investigation. The model’s reach matters, but the quality of that explanation—and the developer’s ability to challenge it—determines whether the result is useful security work or merely a confident code change.

[PAUSE]

## [13:23] Hermit Teaches AI Agents Without Replacing Their Core

[NOVA]: Infini-AI-Lab has released Hermit under the Apache 2.0 license. Hermit is a harness-adapter framework that improves an agent through an external layer rather than replacing the underlying model or the harness running it. That layer contains instructions, skills, memory, and tools. Feedback from completed tasks can train the adapter while the agent’s core remains unchanged. An agent’s behavior depends on much more than model weights: instructions shape priorities, memory changes what survives between tasks, skills package reusable behavior, and tools determine what actions are available. Improving those surfaces can materially change outcomes without the cost and disruption of replacing the model.

[ALLOY]: I like the separation, because a team can improve the external teaching layer from its own task feedback while the model and harness follow independent release cycles. That’s useful when an existing environment already has integrations, permissions, and operating assumptions nobody wants to rebuild. Hermit treats the surrounding layer as trainable rather than as a static pile of prompts and tool definitions. The open question is whether accumulated feedback remains coherent. A lesson from one task may improve a skill, but instructions and memories can also conflict over time. Hermit’s value will depend on whether it turns experience into reusable behavior without making the adapter bloated or contradictory. Still, the premise is attractive: teach the agent through the layer you control while preserving the model and harness that already work.

[PAUSE]

## [14:14] Legora brings agents into legal contract analysis

[NOVA]: Legora is building what it calls an agentic operating system for legal work, using OpenAI models, ChatGPT, and Codex to expand contract analysis and accelerate legal workflows. Contract review is a concrete capacity problem: legal teams have to locate obligations, compare language, identify unusual provisions, and understand how documents relate, often across a volume that consumes substantial professional time.

[ALLOY]: And “free lawyers for higher-value work” is a familiar promise, so where does capacity actually change? If agents let a legal team analyze more contracts, the benefit may appear as faster diligence, broader review, or more time for judgment and negotiation. But legal analysis isn’t complete because a system extracted a clause. Meaning depends on the agreement, governing context, and consequences for the client.

[NOVA]: Legora’s combination of models, a conversational workspace, and coding assistance suggests a platform rather than one isolated summarization feature. ChatGPT can provide an interactive surface, OpenAI models can support analysis, and Codex can help create or adapt the software workflows around that work. The agentic framing implies tasks can proceed across several steps instead of ending at one generated answer. The evidence worth watching is how much contract volume expands and where lawyers reclaim time without losing control of consequential interpretation. A professional agent has to make its work inspectable because the lawyer remains responsible for the advice. Legora shows AI moving from a feature beside legal work into a coordinated environment around it. Trust will depend on how well that environment supports expert judgment rather than merely producing more text quickly.

[PAUSE]

## [15:10] GitHub Project Radar

[NOVA]: REA leads the radar with four hundred four thousand nine hundred twenty-three stars on its first tracked appearance. Its agents trace application behavior from interfaces down into native binaries, and release 6.8 arrived October twenty-fifth. Nanobot connects a different layer: the lightweight Python framework combines a web interface, memory, tools, MCP support, multi-agent workflows, automation, and chat integrations. Version .4 shipped October twenty-eighth; the repository has forty-nine thousand six hundred twelve stars, up one thousand fifty-one over thirty days.

[ALLOY]: And Codebase Memory MCP connects both ideas to everyday development. It builds a persistent local graph across code, documentation, and infrastructure, then exposes that knowledge to agents for exploration and change-aware test selection. It has forty-seven thousand seven hundred sixty-one stars, up two thousand eight hundred ninety-five—six-point-five percent—in thirty days, with .12.1 as its latest release. REA follows behavior deep into binaries; Codebase Memory preserves relationships across a repository; Nanobot supplies a self-hosted agent layer that can use memory and MCP-connected tools. Together they show local agent systems getting better at retaining structure, following behavior, and coordinating actions.

[PAUSE]

## [16:02] Model Discovery Check

[NOVA]: Gemini 4 Carbon is Google’s selected frontier model for sustained engineering and cyber defense. Google says it can work for days, navigate dead ends, find exploitable vulnerabilities, and produce root-cause fixes. Initial access is limited to selected defenders and expands through the Fairwind Program before broader developer, business, and consumer availability. Google’s published cyber scores and its more-than-twofold internal improvement over Argon make long-horizon performance the defining claim.

[ALLOY]: NVIDIA’s Nemotron 3.5 Bolt takes the opposite deployment angle: eight billion parameters, four billion effective, compressed to a four-gigabyte Q4 package. It supports sixty-four-thousand-token input and output lengths, adjustable reasoning, concise conversation, and tool calls. Commercial and non-commercial use are permitted, with local serving through llama.cpp. NVIDIA reports fifty-five-point-six on MultiChallenge versus thirty-nine-point-three-six for Gemma 4 E4B Instruct under its own evaluation setup.

[PAUSE]

## [16:48] Local LLM Spotlight

[NOVA]: DeepSeek V4.1 Flash 1017 is trending on Hugging Face with three thousand six hundred sixty-eight likes and one hundred sixteen thousand seven hundred seventy downloads. It handles image-and-text input and generates text, so it can reason over visual material as well as written prompts. The repository identifies Transformer and SafeTensors support, eight-bit and FP8 formats, published evaluation results, compatible hosted endpoints, and an MIT license.

[ALLOY]: That combination makes it relevant across local and hosted deployments: open licensing, quantized formats that can reduce memory pressure, and a multimodal surface for tasks involving screenshots, documents, or other images. Runtime fit still depends on the model card’s context, weights, and hardware requirements, but the download count shows substantial interest rather than a model sitting untouched in a registry.

[PAUSE]

## [17:30] Extra Research Candidates

[NOVA]: OpenAI and ServiceNow expand partnership across enterprise workflows, bringing OpenAI models and agents into ServiceNow while making ServiceNow workflows accessible through ChatGPT and Codex. How Check Point accelerates vulnerability research with Daybreak connects the same agent push to security: Check Point says Daybreak helps analysts turn vulnerability intelligence into customer protections faster.

[ALLOY]: Those developments connect enterprise action with security response—agents aren’t only answering questions; they’re entering systems where work is tracked and defenses are produced. Working with academic communities to build scientific understanding adds a third surface, placing results on the Kakeya conjecture, the Exponential Time Hypothesis, and quantum chromodynamics before researchers who can verify and extend them.

[PAUSE]

## [18:05] Closing

[NOVA]: For the supporting sources and more detail behind everything we covered, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.
