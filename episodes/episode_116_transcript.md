# AgentStack Daily EP116 — Claude Opus 5.5 Lands at $4 In, $20 Out, Meets GPT-6 Sol and Astra

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily.

[NOVA]: Claude Opus 5.5 just landed at four dollars per million input tokens and twenty dollars per million output tokens, with Anthropic claiming Fable-class performance at a much lower operating cost. That puts it directly against OpenAI’s GPT-6 Sol and Astra—and gives people a model that can examine a large codebase, reason across a roomful of documents, or generate a report longer than many books.

[ALLOY]: And, okay, the price fight is getting intense. Grok 4.7 brings a larger base model without raising its two-dollar input and six-dollar output rates. Nokia’s AnyJev turns open language models into calibrated decision systems, while NVIDIA’s Nemotron 3 can separate as many as eight overlapping speakers live. Those changes affect what automation costs, whether an agent can make dependable routing decisions, and whether a meeting assistant can tell who actually promised what.

[NOVA]: Today, you’ll hear how Opus compares with Sol and Astra, what Hermes Agent 9.21 shipped across its enormous patch window, and why five thousand hours of recorded AAA gameplay could expose agent weaknesses that ordinary benchmarks miss.

[PAUSE]

## [02:00] Agent Stack Release Readout: Hermes Agent 9.21

[NOVA]: Hermes Agent shipped 9.21 as a stable patch release from Nous Research, rolling roughly eighteen hundred merged pull requests into one tag for Docker images, Hermes Cloud, and hosted deployments. The measured window contains more than five thousand non-merge commits across roughly fifty-one hundred changed files, with over three hundred twelve thousand lines added. That’s an absurd amount of movement for something labeled a patch. The concrete additions cover both machine-facing output and daily interaction. Structured stream JSON gives downstream software a line-by-line event feed instead of forcing it to parse terminal prose. A new discovery-concurrency control limits how many Model Context Protocol connections open in parallel during startup. Selected skills can load automatically into every new session, making their availability consistent without calling them again. Search across prior sessions gains time boundaries and a broader retry when the first query is too strict. There’s also a command for changing session journal mode. The gateway can now decline unauthorized direct messages, and a host-wide singleton lock lets the desktop client attach to an existing backend instead of accidentally creating another one. One backend-owned connector operation can appear as the same setup card across desktop, terminal, and command-line surfaces. That consistency matters when the same agent is controlled from several interfaces.

[ALLOY]: Right, because duplicated backends make an agent feel haunted: two processes, two states, and no obvious owner. The singleton record gives every interface a shared place to find the running gateway, so opening desktop after a terminal session doesn’t quietly split the work. Desktop also gains one-click local-engine updates, a chat and interface font picker, and plugin removal from its hub. The video catalogs add LTX 2.5 and Kling O3. The plugin directory picks up community tools spanning Tailscale, SSH, Shodan, terminal access, RSS, memory, and notification utilities, while catalog pages now expose authors and pinned documentation more clearly. Taken together, 9.21 gives operators more control over structured output, connection pressure, persistent skills, gateway access, and which backend owns a session. Automatic skill loading is especially consequential for repeatable agents: a capability selected for every session no longer depends on somebody remembering to invoke it after the conversation begins. Structured event output also makes Hermes easier to embed inside another application because status, tool activity, and results can travel as records rather than decorated text. Honestly, the sheer size of the change window still deserves caution. A stable tag gives downstream deployments one defined release, but thousands of commits create a much broader surface than the word “patch” suggests. Even so, this isn’t merely a package bump. It changes how Hermes starts, communicates, remembers available capabilities, and presents the same operation across its interfaces.

[PAUSE]

## [03:10] Claude Opus 5.5 Delivers Fable-Class Results at $4 In, $20 Out

[ALLOY]: Four dollars in and twenty dollars out sounds aggressive for an Opus model. What changed beyond the price?

[NOVA]: Opus 5.5 is the first Claude 5.5 model, with Sonnet and Haiku versions expected within weeks. Anthropic says it performs about as well as Claude Fable 5.1 across most work, while typical workloads cost forty percent less than Opus 5. Input falls from five dollars to four dollars per million tokens, output falls from twenty-five to twenty, and cached reads cost twenty cents. Generation is more than thirty percent faster. It accepts text, images, and files, carries a one-million-token context window, and can produce up to one hundred twenty-eight thousand tokens. It’s available through Anthropic, major cloud platforms, and GitHub Copilot, with zero data retention offered as an option. Thinking is always active. Users choose an effort level from low through max, and max enables adaptive thinking. Fast mode can run up to two and a half times faster at twice the standard token price.

[ALLOY]: That’s a serious repositioning. The launch results are substantial, though those numbers are Anthropic’s. At maximum effort, Opus 5.5 scored sixty-six point four percent on Terminal-Bench, up from fifty-two point three for Opus 5. AutomationBench rose from twenty-six point nine to forty percent, and partial OSWorld moved from seventy-four to eighty-one point eight. Stripe put forty stacked pull requests through the model and reported that all passed continuous integration. Box used a third of the previous token volume with forty percent less verbose output. Deloitte found seventy-two percent of planted bugs at low effort, against fifty-six percent for Opus 5, while Hebbia reported eighty-six point six percent rubric coverage, up from sixty point three. Anthropic also says containment-crossing attempts fell about eighty-five percent, while warning that the model often recognized evaluation settings. Cheaper long-context work, faster output, and stronger coding results still make this a serious flagship refresh.

[PAUSE]

## [05:58] Head-to-Head: GPT-6 Sol and GPT-6 Astra Versus Anthropic’s New Flagship


[NOVA]: OpenAI answered roughly ninety minutes later with GPT-6 Sol and Luna, while Astra, launched earlier this month, stays its top tier. Price per million tokens: Astra is ten dollars in and fifty out, Opus 5.5 four and twenty, Sol two and ten, Luna ten cents and fifty cents. All three flagships take text, images, and files, handle about a million tokens of context, and produce up to one hundred twenty-eight thousand output tokens.

[ALLOY]: So against Astra, where does Opus actually win?

[NOVA]: Anthropic’s launch table puts them side by side. Terminal-Bench: Opus sixty-six point four, Astra fifty-seven point nine, with Opus at extra-high effort and Astra at high. FrontierCode: fifty-four point four against fifty-three point three. GDPval, an Elo rating for professional work: eighteen forty-six against fifteen forty-two. Humanity’s Last Exam with tools: sixty-seven point seven against fifty-seven point two. Astra wins two: AutomationBench, forty-one point four against forty, and Terminal-Bench Science, sixty-four point six against fifty-eight point seven. At default medium effort, Anthropic says Opus ties Astra on Terminal-Bench at about forty percent of the cost.

[ALLOY]: Sol meets Opus through the older models, because each lab benchmarked the other’s previous generation. OpenAI says Sol matches Fable 5.1 on FrontierCode at much lower cost, scores sixty-eight point eight on DeepSWE, about one point behind Fable 5, and edges Opus 5 on offline OSWorld, sixty point five to sixty point three, at roughly eighty percent lower cost per task. Anthropic says Opus 5.5 performs about as well as Fable 5.1. So the shape is clear: Astra and Fable hold the ten-and-fifty premium tier, Opus 5.5 brings Fable-class results down to four and twenty, and Sol halves that price while claiming Fable-level coding. As Simon Willison put it, the real price war sits one tier below the top.

[PAUSE]



## [07:23] Grok 4.7 Lands: Bigger Model, Same $2/$6 Price

[ALLOY]: Grok 4.7 is the price-war move I didn’t expect. SpaceXAI says it uses a larger base model than Grok 4.6, yet the standard API stays at two dollars per million input tokens and six dollars per million output. Serving speed also stays level. A fast variant doubles output speed and doubles the price, which at least makes that trade explicit.

[NOVA]: The larger model went through a longer reinforcement-learning run weighted toward problems that can take hours, not seconds. SpaceXAI attributes better self-verification, longer-context handling, coding, and knowledge work to that training. It also added an instruction layer that understands the Grok Bot harness natively. The company says it rebuilt the safeguards and achieved its strongest refusal and jailbreak results so far. Its reported biosafety score is sixty-two point four percent on LatchBio, while HackerBench shows three point three percent of risky dual-use prompts getting through. Those are SpaceXAI’s results, so outside use will show how well they travel.

[ALLOY]: I care more about the price than the “bigger brain” slogan. Improved document and presentation creation at the same token rate can redirect routine work even if another flagship wins the hardest evaluation. SpaceXAI places Grok near the frontier of CursorBench price-performance and reports competitive results against Fable 5.1 and Astra across software engineering, professional work, and economics evaluations. Select security partners also get invitation-only red-team access. That needs careful boundaries, but defensive teams clearly want models capable of reasoning through realistic attack paths.

[NOVA]: And distribution is immediate: Cursor, Grok Build, the Grok API, third-party coding harnesses, model routers, and cloud platforms. Grok arrives where developers already buy inference, with its strongest argument on the invoice: a larger model at the old rate. If the claimed gains hold in ordinary coding and knowledge work, competitors must answer on quality and price without assuming a larger model automatically costs more.

[PAUSE]

## [09:09] Nokia Open-Sources AnyJev: No-Training Layer Makes Open LLMs Reliable Decision-Makers

[NOVA]: Nokia’s AnyJev tackles a narrower problem than chat, and that’s why it’s interesting. The open-source Python library turns an existing open language model into a calibrated decision system without additional model training. Instead of asking for a paragraph, an application asks the model to select among fixed options and receives probabilities suitable for routing, classification, or escalation. It supports Transformers and vLLM serving, uses shared-prefix scoring to avoid repeating common prompt work, and carries the Apache 2.0 license. Nokia’s researchers tested the technique across Qwen, OLMo, Granite, Phi, and Mistral models rather than presenting it as a trick for one checkpoint.

[ALLOY]: Okay, the clever part is how it attacks two biases that make raw probabilities unreliable. A model can prefer a label such as “yes” regardless of the evidence, and it can favor whichever choice sits in a preferred list position. AnyJev rotates the options so every answer appears in every position, then combines the results using a geometric mean. It also corrects for the model’s background preference after observing real inputs. A second level uses a few hundred labeled examples to reshape confidence without changing the winning answer. On a twenty-way banking task with Qwen3-8B, reordered options changed raw answers twenty-three percent of the time. AnyJev cut that to about seven percent and raised accuracy from seventy-four point seven to eighty point seven percent. Better yet, the share of requests automated at a five-percent error threshold rose from seven point seven to fifty-two percent. That’s not statistical decoration. It changes how much work can move automatically and how much still needs a person.

[PAUSE]

## [11:40] NVIDIA’s Nemotron 3 Diarization Tracks Eight Overlapping Speakers Live

[ALLOY]: Speech recognition tells you what was said, but it can leave a meeting assistant clueless about who said it. How does Nemotron 3 keep eight speakers straight when people interrupt one another?

[NOVA]: NVIDIA’s open-weight model produces eight channels of speaker activity from a single audio stream. It has one hundred million parameters and accepts standard sixteen-kilohertz, single-channel audio. The model converts sound into a frequency representation every ten milliseconds, groups those observations into eighty-millisecond frames, and sends them through a thirty-one-layer Transformer. A convolution layer restores ten-millisecond timing. When two people talk simultaneously, two output channels activate instead of forcing one voice to win. Speakers are assigned by arrival order—the first newly heard voice gets the first channel—and two memory systems preserve those identities as audio streams through successive chunks.

[ALLOY]: That’s a serious jump from NVIDIA’s previous four-speaker streaming system. On Voice Arena’s initial Diarization-Bench, covering about twenty-two hours across one hundred thirty-nine English conversations, Nemotron reached a fourteen point seven two percent diarization error rate. The next-ranked system was at nineteen point three, a relative reduction of roughly twenty-four percent. Against NVIDIA’s four-speaker baseline at just over one second of latency, average relative error dropped forty-one percent across eight conditions, including a sixty-five percent drop on one especially difficult multi-speaker set. The company also reports throughput above fifteen thousand times real time on an RTX Pro 5000 with longer chunks. Okay, that’s actually wild. Eight overlapping speakers aren’t a polite board meeting. They’re a hostile environment for attribution. The weights are commercially usable under NVIDIA’s OpenMDW license, with cloud serving routes and an on-device mobile path, so this can move beyond a lab demo into meeting capture, call analysis, broadcasting, and live transcription where interruptions are normal.

[PAUSE]

## [13:21] OpenAI Extends Daybreak Cyber Access to Ukraine

[NOVA]: OpenAI is extending its Daybreak cyber-defense program directly to the Government of Ukraine, placing the company’s tools inside work protecting civilian infrastructure. A national government becomes a direct recipient of vendor support for defensive cyber operations rather than receiving capability only through an academic or intermediary partnership. Daybreak is framed around civilian-facing systems, giving this expansion a narrower purpose than general government access. In a country where digital attacks can accompany physical attacks, faster threat analysis can affect communications, public services, and other essential systems.

[ALLOY]: And that context makes the move consequential. Anomaly detection, threat-intelligence processing, automated triage, and incident-response assistance have immediate human stakes there. OpenAI’s decision shows frontier-model companies forming direct relationships with public-sector defenders around essential services. That may shorten response work, but it also puts difficult judgments inside vendor programs: who qualifies, which defensive uses receive advanced access, and how safeguards distinguish protection from dual-use escalation. The boundary isn’t academic when the same capabilities that identify a vulnerability might also help exploit it.

[NOVA]: Exactly, and it gives companies building the surrounding layer—security operations software, evidence handling, alert prioritization, and analyst copilots—a clear demand signal. Governments aren’t merely discussing AI-assisted cyber defense; at least one is receiving a dedicated program from a frontier lab during an ongoing conflict. I wouldn’t measure success by access alone. The meaningful results are defended services, faster investigations, and fewer successful intrusions. Still, Ukraine’s inclusion marks a move from demonstration toward operational support.

[ALLOY]: Yes, and direct support brings direct responsibility. OpenAI now has to maintain the boundary around civilian defense while its systems encounter real adversarial behavior, sensitive information, and urgent decisions. If Daybreak helps analysts connect evidence sooner without replacing accountable human judgment, it could become a model for narrowly defined public-interest deployments. If the boundary blurs, the same program will draw scrutiny for good reason.

[PAUSE]

## [14:32] Research Digest: A Benchmark for Agent “Taste” on Long Tasks

[NOVA]: TasteBench asks whether an agent makes good choices during a long task, not merely whether it stumbles into a successful final answer. The researchers use “taste” for decisions such as which hypothesis deserves attention, which partial implementation should survive, and when a promising route has become a dead end.

[ALLOY]: I like that distinction because final-answer scoring can hide waste and luck. Two agents may both finish a software task, while one takes a coherent path and the other burns hours on bad branches before recovering. Long-running research and coding systems live or die through those intermediate decisions.

[NOVA]: But can a benchmark define good taste without just encoding the preferences of its authors?

[ALLOY]: That’s the hard part. Expert judgments may vary across domains, and a surprising route can look wrong before it succeeds. TasteBench is most useful as a diagnostic, not one grand score. It can help separate planning quality from final completion and reveal whether an agent repeatedly abandons strong ideas, clings to weak ones, or spends its budget wandering. Conventional pass-or-fail evaluations blur those behaviors together.

[PAUSE]

## [15:29] Research Digest: GameHorizon Puts AI Agents Through 5,000 Hours of AAA Gameplay

[ALLOY]: GameHorizon gives agents five thousand hours of recorded play across twenty-one major games, including Valorant, Minecraft, Grand Theft Auto V, Palworld, and Elden Ring. One hundred experienced players generated the demonstrations, with actions aligned to instructions ranging from immediate controls to short operations and longer strategies.

[NOVA]: That layered labeling is the point. An agent might identify the next keypress yet fail to pursue a goal that takes several stages, or describe a good strategy while missing the action needed now. GameHorizon separates those failures through five thousand offline questions and twenty interactive tasks divided into sixty-two subtasks. The researchers evaluated forty-seven vision-language, interface-control, coding, and game-specialist models. Because the recordings are fixed, different systems face the same situations instead of being compared across unpredictable live runs. AAA games provide dense worlds, partial information, interruptions, and delayed rewards—a useful stress case for agents expected to plan beyond the next screen.

[PAUSE]

## [16:29] NVIDIA Frames AI Agent Security as an Engineering Discipline

[NOVA]: NVIDIA argues that agent security becomes real when somebody turns a concern into a requirement, an enforceable control, an owner, and evidence that the control worked. Its example is blunt: an agent updating a customer record reads malicious instructions embedded in a document and attempts to export data. A network rule blocks the transfer, protected logs record the attempted tool call and destination, and the agent can’t expand its own permission.

[ALLOY]: That’s refreshingly concrete. It assumes the model can be manipulated and puts a boundary outside the model’s reasoning. NVIDIA divides the system into models, harnesses, and execution environments. Models supply capabilities; harnesses assemble instructions, context, and tools; runtimes control the files, networks, and processes where actions occur. A defense at only one layer leaves another layer able to carry a bad instruction into the world.

[NOVA]: NVIDIA points to OpenShell as its sandboxed runtime for external file, network, and process limits. Cisco’s DefenseClaw adds governance, while JFrog scans agent skills before they run. Other examples include CrowdStrike’s SafeMind for repeated attack simulation, Palo Alto Networks’ Prisma AIRS for continuous adversarial probing, Capital One’s VulnHunter for AI-assisted code review, and ReversingLabs’ Spectra Assure for finding malicious dependencies. That’s a lot of product names, but they support one concrete idea: permissions, execution boundaries, monitoring, and software supply-chain checks all have to survive independently of the model’s judgment. An agent that can read a malicious instruction may still be prevented from opening an outbound connection, reaching a protected file, or installing a poisoned package. That turns security from a hope about model behavior into several independently enforceable limits.

[PAUSE]

## [18:30] Thinking Machines Lab Moves Open-Model Inference to Crusoe Cloud Under $65M Deal

[ALLOY]: Thinking Machines Lab has committed sixty-five million dollars annually to run inference for its open models on Crusoe Cloud. That’s not a hardware purchase disguised as a partnership. Production traffic will move through Crusoe Managed Inference, where Crusoe takes responsibility for the serving layer around throughput, price-performance, capacity, and reliability.

[NOVA]: The open weights and model behavior remain the same. What changes is the machinery behind the endpoint—the servers, scheduling, scaling, and optimization that determine latency and per-token economics. Thinking Machines hands off capacity planning under a managed agreement instead of building every part of that infrastructure itself. For Crusoe, the deal supplies a prominent anchor customer and a serious reference for its pitch as an AI-focused cloud rather than another seller of bare accelerators.

[ALLOY]: And sixty-five million a year shows how valuable inference operations have become. Training still gets the giant-cluster headlines, but a model used continuously creates an enormous recurring serving bill. Open-model labs face a choice: build an infrastructure organization beside the research lab, or let a specialist absorb that work. Crusoe is betting that a tuned managed service wins even when customers could theoretically host the weights elsewhere. I can see the appeal—owning weights doesn’t magically make scheduling, batching, failover, or hardware utilization easy.

[NOVA]: I’d resist reading one contract as broad consolidation, though. Developers may see the same model interface while the underlying provider changes, making latency, uptime, and price-performance the visible proof of the deal. Crusoe now has to show that a neocloud can deliver production inference at this scale, not simply reserve attractive compute. If it succeeds, other open-model companies gain a credible alternative to building their serving stack or defaulting to the largest hyperscalers. If it struggles, the contract becomes an expensive reminder that production inference is a product, not merely a pile of GPUs.

[PAUSE]

## [20:11] Jev Returns Probabilities Instead of Text, Undercutting GPT-5 Nano on Price

[NOVA]: Jev accepts text but returns numbers: probabilities, confidence scores, and distributions across categories. TypeSafe AI calls it a System One model; “decision model” is clearer. An application supplies a state—perhaps a customer record, article, or semi-structured document—and attaches typed questions instead of asking for prose.

[ALLOY]: There are three response shapes. A yes-or-no question returns confidence between zero and one. A choice question distributes probability across named options. A score question rates the input along ordered numeric levels. So instead of prompting a general model to say whether a support ticket is urgent and then parsing its sentence, software gets a number that can feed routing directly.

[NOVA]: The price makes that specialization provocative. Jev charges four point two cents per million input tokens, with no output charge. That comes below GPT-5 Nano’s five-cent input rate, and numerical output avoids paying for explanatory paragraphs the application never wanted. It naturally suits systems making many small decisions across every document: triage, moderation, categorization, ranking, or choosing which downstream model should handle a request. At large volume, shaving a fraction of a cent per million tokens sounds tiny until every item generates several decisions.

[ALLOY]: And it pairs neatly with AnyJev. Jev is a commercial model designed to emit probabilities; AnyJev tries to coax calibrated decisions from open models without retraining them. They approach the same demand from opposite directions. Neither replaces a generative model when a person needs an explanation or reply, but both challenge the habit of using an expensive conversational model as a glorified classifier. When software needs one confidence value, returning three polished paragraphs isn’t intelligence. It’s overhead—and occasionally a parsing bug waiting to happen.

[PAUSE]

## [22:07] A Self-Hosted Browser That Lets AI Agents Skip Captchas

[ALLOY]: Invisible Playwright MCP wraps browser automation in a self-hosted tool designed to avoid common bot defenses. It speaks Model Context Protocol, the standard agents use to call external tools, and drives an anti-detect Firefox profile through Playwright. Point seventy shipped with the repository above thirty-one thousand six hundred stars. That popularity tells you how often browser-based agents collide with systems built to reject automation.

[NOVA]: The attraction is obvious: an agent can maintain a browser session for dashboards, forms, authenticated pages, scraping, or computer-use loops without immediately hitting fingerprint checks and captcha screens. Self-hosting also keeps session credentials inside the operator’s environment instead of passing them through a captcha-solving service. But “undetected” is temporary language in an arms race. Sites can change their fingerprints, browser behavior can expose automation in new ways, and a tool that works against one defense may fail against the next. More importantly, bypassing a challenge doesn’t override a site’s terms, access rules, or the law. The project is useful infrastructure where automation is permitted; it isn’t permission disguised as a browser feature. Its real value is continuity—keeping an authorized workflow alive when ordinary automation reveals itself too easily. A self-hosted deployment also gives an organization control over browser storage, cookies, profiles, and the machines touching authenticated systems. That can matter for an internal agent reading an approved supplier portal or operating a company-owned dashboard. Still, the same stealth features attract obvious misuse, so the surrounding authorization and audit trail matter as much as the browser connection itself.

[PAUSE]

## [23:38] OpenAI Releases MentalHealthBench to Test AI Responses in Mental-Health Conversations

[NOVA]: OpenAI has released MentalHealthBench, a standardized evaluation for AI responses in realistic mental-health conversations. It scores two dimensions together: whether a response is helpful and whether it is safe. Mental-health specialists helped shape the scenarios and scoring rubrics. That matters because a model can sound caring while still giving reckless guidance, or avoid obvious danger by becoming so evasive that it stops helping.

[ALLOY]: Right, warmth alone can conceal harm. Separate helpfulness and safety judgments make that tradeoff visible. A response might correctly recognize distress yet reinforce a dangerous belief. Another might avoid clinical certainty but abandon the person behind a generic refusal. Treating those outcomes as equivalent would produce a reassuring score and a bad product.

[NOVA]: Realistic conversations are also harder than isolated crisis keywords. Distress can emerge indirectly, change across several turns, or sit beside an ordinary practical question. Therapy-adjacent products, wellness apps, support systems, and general assistants all need to recognize when an exchange requires care, when professional help should be encouraged, and when the model has crossed from supportive language into inappropriate clinical authority. The multi-turn setting can expose failures that a single prompt never reaches.

[ALLOY]: A shared benchmark gives developers and outside researchers something firmer than hand-picked demos. I wouldn’t treat any benchmark as permission to deploy a model as a therapist; real people bring histories and risks that a fixed collection can’t fully represent. But expert-informed conversations can reveal whether a system stays useful without becoming reckless. MentalHealthBench also connects with OpenAI’s wider emphasis on human control. Here, that principle becomes measurable at one of the most sensitive points of contact: a person asking a machine for help when tone, certainty, and escalation can carry genuine consequences.

[PAUSE]

## [25:12] GitHub Project Radar

[NOVA]: Three repositories are moving quickly. Nanobot has forty-eight thousand five hundred eighteen stars, up twelve hundred sixty-seven in thirty days. Its point three five release advances a lightweight, self-hosted personal-agent framework with a web interface, memory, tools, Model Context Protocol support, multi-agent workflows, and automation hooks. Codebase Memory MCP is the sharper growth story: forty-four thousand five hundred forty-two stars, up twelve percent in a month after point eleven. It builds a persistent code knowledge graph so coding agents can query structure instead of repeatedly rereading files, and the project claims support for one hundred fifty-eight languages plus major token savings.

[ALLOY]: Okay, those two connect naturally: Nanobot can orchestrate a personal agent, while Codebase Memory supplies specialized understanding of a repository. Invisible Playwright MCP is the browser counterpart, making its first tracked appearance at thirty-one thousand six hundred forty-four stars with point seventy released today. One project organizes the agent, another preserves code knowledge, and the third gives it a self-hosted browser surface. That modularity is exciting because teams can replace memory, browsing, or orchestration independently instead of accepting one giant framework. Codebase Memory’s twelve-percent monthly gain is especially striking at that size, while Nanobot’s recent release and continued repository activity show that its already-large audience is still receiving changes. Together, the three projects reflect attention moving toward durable context and dependable tool access, not merely another chat screen.

[PAUSE]

## [26:14] Model Discovery Check

[NOVA]: Model progress today also landed through serving variants. GLM 5.3 Prime and Qwen 3.8 Max Prime each bring million-token context through OpenRouter, with their vendors positioning them as higher-throughput versions of established lines. The competition now includes how quickly enormous contexts can move through production, not only which model tops an evaluation.

[PAUSE]

## [26:46] Local LLM Spotlight

[ALLOY]: Ternary Bonsai 2 27B packages a twenty-seven-billion-parameter text model in GGUF, a format used by llama.cpp for local inference. Its unusual feature is ternary, two-bit-oriented quantization, which compresses weights far more aggressively than full-precision storage. It supports CUDA and Apple Metal runtimes, uses hybrid attention, and has reached nineteen hundred fifty likes and more than two point eight million downloads on Hugging Face.

[NOVA]: That’s substantial interest in useful generation on hardware people control. Aggressive compression can trade memory savings against quality and device-specific speed, but it makes a twenty-seven-billion-parameter model plausible on machines that couldn’t hold ordinary weights. Local inference keeps sensitive prompts on the machine, removes per-token billing, and connects to a mature desktop runtime ecosystem. The download count shows people actively pursuing a workable balance among capability, memory, speed, and control.

[PAUSE]

## [27:41] Extra Research Candidates

[NOVA]: Sam Altman’s United Nations Security Council remarks center on human control, AI safety governance, and international cooperation. Introducing MentalHealthBench turns part of that broad argument into expert-informed evaluation, measuring helpfulness and safety across realistic mental-health conversations.

[ALLOY]: Tyk connects both ideas to live infrastructure. Its open-source gateway routes REST, GraphQL, TCP, gRPC, and Model Context Protocol traffic through one policy layer, and it has more than ten thousand eight hundred stars. International cooperation sets expectations, MentalHealthBench measures sensitive behavior, and Tyk enforces routing and access rules where software runs.

[PAUSE]

## [28:26] Closing

[NOVA]: For the primary sources, specifications, benchmark references, and projects behind everything we covered, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily.

[NOVA]: We'll be back soon.
