# AgentStack Daily EP107 — Codex Desktop Adds WebMCP, Messages, Linux, and Multi-Repo Review

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: OpenAI just turned the Codex desktop app into a broader agent workspace. It can discover website tools through WebMCP, review changes across several repositories together, work natively on Linux, and ask before sending an Apple Message. That’s coding, browsing, collaboration, and communication moving into one surface.

[ALLOY]: And cloud agents aren’t waiting politely in another tab. Grok Bot gives multiple agents a shared persistent computer, complete with files, browser state, and logins, so they can keep handling research, invoices, and follow-ups after the laptop closes. That’s exciting—and a shared logged-in machine deserves serious respect.

[NOVA]: Hermes shipped releases 8.27 and 8.19. The newer one rolls up roughly five hundred twenty-five merged pull requests, adds a separate browser window, managed remote updates, more than fifty verified remote tool servers, and tighter controls around installs, secrets, and long-running work.

[ALLOY]: Today: the Qwen4 architectural preview, OpenAI’s first Jalapeño inference-chip results, a tiny glucose model beating systems hundreds of times larger, and two Google chips dividing training from inference. You’ll hear what people can build with them—and where autonomy is getting ahead of governance.

[PAUSE]

## [02:00] Agent Stack Release Readout: Hermes Agent 8.27, 8.19

[NOVA]: Hermes Agent release 8.27 landed August twenty-seventh, superseding the 8.19 baseline and consolidating roughly five hundred twenty-five merged pull requests into one stable release for Docker images, hosted deployments, and fresh installations. The most visible change pulls the desktop Browser out of the chat panel and gives it an independent operating-system window. A browsing session can remain visible, be docked, or close without treating the browser as another piece of conversation output. Remote machines gain managed updating through SSH, plus a fleet-profile rail for organizing them. Those updates pause the gateway through its control socket instead of terminating it while work is active. Local browsing can use the person’s default Chromium profile through a consent gate, which means a site that already has a valid login can be opened without starting a separate authentication session. On Windows, closing that browser path requires approval. Hermes also expanded its remote Model Context Protocol catalog beyond fifty live-verified, vendor-hosted servers. Model Context Protocol is the common interface agents use to reach external tools and data. The catalog now includes services from Cloudflare, Grafana Cloud, Better Stack, and Railway, reducing the need for a local connector between Hermes and those services.

[ALLOY]: That’s a dense release, but the quieter runtime changes may matter more after the first day. Web search and extraction now cache results for a defined lifetime, while tool search can issue several queries and match word variants, so “run” and “running” don’t behave like unrelated concepts. Mac users can opt into operating-system keychain encryption for stored secrets without accepting repeated prompts every time Hermes starts. Lean-tail compression is now enabled by default to shorten responses while preserving useful content. Image-based and package-managed installations refuse unsafe in-place updates, Slack gains controls for link previews, Docker containers can share identities, and terminal environments can come from replaceable backends. The model pickers add GLM five point three Flash, MiniMax M three free, and MiniMax H three Max video. Release 8.19 supplied the earlier foundation: a keyless web tier with free rotation across five vendors and failover between them, plus a fuzzy model picker and a control-P command palette. I like the separate browser window; I like update handling that doesn’t kill a task even more. The breaking plugin-manifest change does mean integrations built against the older schema need adjustment, and legacy command flags are being retired. Hosted tenants receive 8.27 in waves, while self-hosted installations have to rerun the installer to receive the new manifest structure.

[PAUSE]

## [03:19] Codex desktop app adds WebMCP, Messages, Linux, and multi-repo review

[ALLOY]: WebMCP sounds like another protocol label. What did OpenAI actually put in someone’s hands?

[NOVA]: The Codex desktop app can now use Site Tools that a website exposes through WebMCP, allowing ChatGPT Work or Codex to interact with supported site functions through a defined tool interface. That arrived August twenty-fifth and requires the latest desktop app plus a GPT-five point six Sol or Terra subscription; it isn’t available on Luna, Enterprise, or Edu. The extension also moved beyond Chrome to Edge, Brave, Opera, and Vivaldi. All five support tab mentions and browser control, although Opera lacks side chat. Earlier updates filled out the workspace around that browser. Multi-folder projects now have one combined review view for changes across repositories. That’s a meaningful improvement when an application, shared library, and deployment configuration live separately but change together. Generated images gained Focused and Canvas views for comments and refinement. Browser history, address-bar search, selected Chrome text, YouTube questions, and right-click Ask ChatGPT all became usable context, with browsing-history access remaining optional.

[ALLOY]: And Linux is no longer watching through the window. The August eleventh preview supports Ubuntu, Debian, and Fedora across x64 and ARM64, using the native package formats those distributions expect. The app can import instructions, settings, skills, plugins, projects, and recent work from the terminal-based AI coding agent Claude Code, Claude Cowork, and Cursor, with optional updating of imported material. On macOS, an Apple Messages plugin can send from ChatGPT Work or Codex only after approval. Shared snapshots offer a read-only view of local Codex threads, though OpenAI warns its secret-pattern redactor may miss sensitive details. Unified pinned threads also carry across desktop and iOS, while same-workspace Site editing can preserve shared context as a page changes. So yes, the app is becoming a cross-platform agent workspace—but a share button beside local development context still deserves a careful second look.

[PAUSE]

## [05:11] Grok Bot gives agents one persistent cloud computer and 24/7 work

[NOVA]: Grok Bot is a separate xAI agent product, not a button inside ordinary Grok chat. It entered early beta August eleventh and expanded access again August twenty-sixth. A person can create several Bots, message them like coworkers, put them into shared threads, and hand work from one to another. All Bots owned by one user share a persistent cloud computer, including files, browser state, and authenticated sessions. Isolation happens between users, not between a user’s Bots. A research Bot could work in a signed-in browser, pass account information to an operations Bot, and let it process Gmail material while the user’s laptop is closed. Websites don’t need an API or Model Context Protocol server because the Bot can operate their browser interfaces.

[ALLOY]: That’s wild—and the shared machine is both the feature and the reason to pause. xAI says Bots can watch someone perform a workflow once, save it as a routine, absorb corrections, and return to abandoned threads. Clients cover Macs, x64 Windows ten and eleven machines, plus iPhone and iPad; xAI doesn’t list Android. The lowest entry point is Cursor Pro at twenty dollars monthly; SuperGrok starts at thirty. Higher Cursor, SuperGrok, and team plans also qualify, and Bot usage is separate from ordinary Grok or Cursor allowances.

[NOVA]: xAI lists encryption in transit and at rest, a training opt-out, automatic review for sensitive actions, and enterprise controls covering data-loss prevention, certificates, proxies, and networks. Enterprise access remains waitlist-only. Those controls matter because a continuously logged-in agent can encounter much more than its named task.

[ALLOY]: “Always running” is better only when the agent remembers the right state, respects boundaries, and leaves a comprehensible trail. A shared cloud computer makes collaboration between Bots fluid but concentrates their reach. Grok Bot asks people to treat agents as ongoing occupants of a computer, not disposable chat sessions. That’s a much bigger relationship.

[PAUSE]

## [06:52] Alibaba Previews Qwen4 Through Qwen3.8-Flash-Next

[ALLOY]: Alibaba previewed Qwen4 without calling the checkpoint Qwen4. So what exactly is Qwen three point eight Flash Next?

[NOVA]: It’s a multimodal Mixture-of-Experts model from the Qwen Team and an architectural preview of the next generation. Mixture-of-Experts means only part of the network works on each piece of input. The model has a one-hundred-twenty-five-billion-parameter backbone, a fifty-one-billion-parameter N-gram embedding table, and a four-billion-parameter module that predicts several tokens ahead. Alibaba gives the combined total as one hundred eighty billion parameters, but only six billion activate per token. That small active slice drives its efficiency claim. The checkpoint handles text and visual material, while its million-token context capacity targets long documents, codebases, and extended agent work.

[ALLOY]: The N-gram table is the unusual piece. It gives the model dedicated memory for short recurring patterns rather than making the main network rediscover every local relationship. Alibaba also combines Gated DeltaNet with sparse attention, pairing efficient sequence tracking with selective long-range connections. Gated residual paths change how information flows during training, and the Muon optimizer replaces the conventional update step. Alibaba says training cost fell to about one-ninth of Qwen three point seven Plus. That number comes from Alibaba, so it’s a claim until outside work reproduces it.

[NOVA]: And “efficient” doesn’t mean casual-laptop small. The FP8 checkpoint occupies roughly one hundred seventy-three gibibytes. FP8 stores model weights with eight-bit numbers to reduce memory, yet this still points toward data-center graphics processors for serious self-hosting. Six billion active parameters could make serving cheaper than the total size suggests, but the memory footprint remains substantial. This is a runnable preview of Qwen4’s direction, not proof of the finished family’s performance.

[PAUSE]

## [08:13] Orchestration overtakes automation as the CX bottleneck, says Tata Communications

[NOVA]: Tata Communications says adding more conversational AI isn’t fixing customer service when the systems behind it remain disconnected. Gaurav Anand, who leads the company’s Customer Interaction Suite globally, argues that enterprises attached AI to legacy customer-experience software built for linear, human-directed routing. Human representatives now end up reconstructing what an AI already said, which systems it touched, and what the customer was trying to accomplish. A clever assistant becomes another silo if it sees the support conversation but not the transaction, policy, identity, or journey behind it. Anand says the constraint has shifted from obtaining data to creating shared enterprise context: one working understanding connecting identities, interactions, transactions, policies, operational systems, and human staff. Autonomous agents make that gap harder to hide because they exchange information in real time and may act before a person assembles the missing context.

[ALLOY]: That rings true. His conclusion is that orchestration now outranks another round of isolated automation. In plain English, companies need their existing intelligence to coordinate across systems so customers don’t experience the seams. That puts identity resolution, context layers, and agent coordination ahead of simply replacing a chatbot model. It also changes what good service looks like. A customer shouldn’t have to repeat a failed delivery, an earlier promise, and the account history because three agents each inherited a different fragment. Anand is a vendor executive, so this isn’t neutral market measurement. Still, he identifies a recognizable failure: the customer hears one company while its software behaves like six departments meeting for the first time. Faster answers won’t repair that fragmentation; they may only expose it sooner. And once an agent can issue a refund, change an order, or promise a delivery date, disconnected context stops being merely annoying. It becomes an operational liability with a customer attached.

[PAUSE]

## [09:37] The real enterprise AI risk hiding between agents

[ALLOY]: One agent gets a security review. Ten agents start calling one another. How quickly does that become a different problem?

[NOVA]: Very quickly, because possible relationships grow faster than the agent count. A support request might pass through a classifier, customer-record agent, policy agent, and fulfillment agent before a person sees it. Each transfer carries authority, context, and implied approval. Another agent may connect to several existing agents and systems, creating many paths rather than one new link. Reviewing agents separately can miss what the fleet does together. A low-privilege agent may call one with broader access, which triggers a third system. Nobody deliberately granted the first agent the final capability, yet the chain produced it.

[ALLOY]: Later, investigators may see isolated logs but struggle to reconstruct why an action occurred three hops downstream. Governance has to account for reachable paths, not only named components: which agents can contact which systems, what identity each call carries, and how an upstream request becomes a downstream action. One-time approval records age badly as deployments, tools, and permissions change. If ownership stops at each agent’s boundary, the space between them becomes unowned infrastructure.

[NOVA]: Familiar controls can appear healthy separately. Each agent may have an owner, each tool may log requests, and each application may enforce permissions. The combined chain can still produce an unintended outcome because no component sees the entire path. Duplicate records can diverge as agents pass summaries instead of original context, leaving downstream actions based on compressed or outdated accounts.

[PAUSE]

## [11:20] Liquid AI's Pipette Benchmarks Models on the Devices They Actually Run On

[NOVA]: Liquid AI released Pipette, an open-source benchmarking suite for measuring models on the phones, laptops, and other devices where they’ll actually run. Model cards often report quality under server-class conditions and generous numeric precision. Once a model is compressed, placed behind a mobile runtime, and constrained by a real processor and memory system, those headline numbers may predict very little.

[ALLOY]: Pipette treats the model, quantization, runtime, and device as one combined experiment. Quantization means representing a model’s numbers with fewer bits, cutting memory and often increasing speed at the possible cost of quality. That trade changes across chips and software. A model that looks best at full precision on a server may lose to a smaller competitor after both are compressed for one phone.

[NOVA]: Liquid AI partnered with Artificial Analysis as an independent methodology validator. Pipette can report quality and latency for a defined model configuration on specific hardware, and teams can add device profiles because the suite is reproducible and open source. That’s much closer to the decision behind an offline writing assistant, camera feature, or local voice interface: not “Which model leads globally?” but “Which exact package responds fast enough and stays accurate on the device people own?”

Honestly, I’m enthusiastic about that shift because on-device AI has suffered from benchmark teleportation—numbers measured in one environment somehow materialize in marketing for another. Pipette can’t lift a phone’s thermal, memory, or battery ceilings, and its results cover only the configurations measured. But it supplies a shared language for the compromise. Sustained use matters too: a model can look fast for one burst and slow down as a device heats up. Once the model and deployment stack become one observable product, those physical constraints stop hiding behind an abstract leaderboard. That won’t make device choices simple; at least it makes them real. Teams can also compare sustained runs, not only a single cool-device burst.

[PAUSE]

## [12:47] OpenAI's Jalapeño chip posts first inference results

[ALLOY]: OpenAI says Jalapeño delivers industry-leading inference speed and power efficiency. How much can we conclude from the first numbers?

[NOVA]: We can conclude that OpenAI’s custom inference chip has reached the point of producing disclosed performance results. Inference is the computation used when a trained model generates an answer. It’s the recurring expense behind every chatbot reply, code completion, image interpretation, and automated summary. OpenAI says Jalapeño produces higher throughput—more answers per second—and lower latency—less waiting for each answer—than comparable options. Those results were published August twenty-fifth as the first concrete validation of a multi-year effort to design internal silicon.

[ALLOY]: But those are OpenAI’s measurements, so I don’t buy “industry-leading” as settled until independent benchmarks define the workloads and reproduce the comparison. Chip results can change dramatically with model size, numeric format, batching, memory movement, and how much traffic arrives at once. A favorable internal workload doesn’t automatically predict every external application.

[NOVA]: What is already clear is why OpenAI wants the chip. Training gets the giant capital-spending headlines, but inference repeats every time somebody uses the product. More responses per server or fewer watts per response can improve margins at enormous scale. It may eventually affect pricing, response speed, or the size of models OpenAI can serve economically. Owning more of the serving stack also gives OpenAI leverage over capacity planning and outside accelerator road maps. The next useful disclosures are whether Jalapeño remains internal, whether ChatGPT or API traffic runs on it, and how it performs under independently comparable conditions. First silicon results are real progress. They’re not yet a public victory lap.

[PAUSE]

## [14:14] Google's Tiny Glucose Model Beats Rivals Hundreds of Times Its Size

[NOVA]: Google Research and the University of New South Wales Sydney built GlucoFM, a foundation model for continuous glucose-monitor data, with only seven hundred twenty thousand parameters. Across fourteen cohort and task evaluations, it averaged fifty-eight point eight on precision-recall area under the curve, a score useful when important events are less common than ordinary readings. It beat GluFormer at one hundred thirty-five million parameters and MOMENT at three hundred eighty-five million. Those competitors are roughly one hundred ninety and five hundred thirty-five times larger. That’s the kind of tiny-model result that earns attention. Continuous glucose monitors produce a reading every few minutes, but the trace mixes slow biological drift with short spikes caused by meals, exercise, medication, stress, and other events.

[ALLOY]: GlucoFM doesn’t force one general sequence model to untangle everything through scale. It separates the trace into a slow physiological stream and a transient-event stream, encodes them through distinct pathways, and then combines them. It learns first from unlabeled glucose traces through self-supervision, absorbing recurring structures before adaptation to a particular prediction. That matters because medical labels are expensive, cohorts differ, and glucose data is noisy and highly individual. Okay, the size comparison is startling, but I’d resist turning one benchmark win into a clinical revolution. GlucoFM is a research prototype with no announced regulatory clearance, public programming interface, open weights, or device partnership. Nothing here authorizes a medical decision. What it challenges is the assumption that a biomedical foundation model must inherit language-model scale. When the design separates biological processes the way the data behaves, hundreds of millions of generic parameters may be less useful than a small model shaped around the physiology. A model this compact could eventually make continuous analysis easier to place near the sensor or inside constrained health hardware, but the published evaluation establishes research performance, not clinical deployment.

[PAUSE]

## [16:16] Research digest: A Smarter Loop For Teaching Vision Models To Follow Instructions

[NOVA]: VISA is a framework that improves the instructions used to train vision models. It examines an image, removes requirements that can’t be verified, proposes new constraints from stored examples, and checks candidate tasks using executable tools plus structured judgments from a language model.

[ALLOY]: So it doesn’t keep producing more of the same synthetic material?

[NOVA]: Right. When the target vision model fails, the framework diagnoses the weakness and designs later training material around it. That feedback also becomes a reinforcement-learning reward, avoiding a separately trained reward model. On MM-IFEval, a benchmark for multimodal instruction following, VISA-trained models beat strong baselines while preserving results across seven broader multimodal evaluations.

[ALLOY]: That’s the useful result: the data changes in response to what the model still misunderstands. It can sharpen assistants asked to inspect an image, obey several constraints, and return a precise format without trading away broader visual ability. Generated instructions still aren’t automatically trustworthy, but failure diagnosis becomes both curriculum and training signal.

[PAUSE]

## [17:22] xAI's Grok 4.6 Lands on Microsoft Foundry

[ALLOY]: Grok four point six is now in Microsoft Foundry, Azure’s catalog for evaluating and deploying managed AI models. That puts xAI’s flagship inside the same enterprise purchasing and infrastructure surface as competing frontier systems. It has a five-hundred-thousand-token context window and four reasoning-effort settings: low, medium, high, and extra high.

[NOVA]: xAI positions it for long-running agents, coding systems, engineering copilots, research assistants, enterprise automation, and interactive visual work. The context window can hold large bodies of code or documents, but capacity alone doesn’t guarantee useful attention across every token. Foundry makes comparisons easier because organizations can place Grok beside other catalog models within Azure instead of building an entirely separate deployment path.

[ALLOY]: And that distribution may matter almost as much as another benchmark chart. Managed endpoints fit the enterprise controls, purchasing relationships, and governance surfaces customers already use in Azure. Grok Bot is xAI’s persistent-computer bet; Grok four point six on Foundry is the model-supply bet. One gives agents an ongoing machine, while the other gives companies a managed model endpoint. Those are very different trust decisions even though the Grok name sits on both.

Those options can be separated in practice. A company may want Grok’s model without giving a persistent Bot a logged-in computer, or it may want both at different trust levels. Foundry lowers procurement friction, not uncertainty. Quality, latency, data handling, and economics still depend on the workload. But xAI has gained a conventional route into organizations already standardized around Azure identity, billing, monitoring, and deployment. That can turn a model from an interesting outside option into something an existing team can actually purchase and operate without creating a separate infrastructure island. That distinction is central when evaluating xAI’s desktop agent against its hosted model.

[PAUSE]

## [18:17] Research digest: A cheaper way to let AI models think longer

[NOVA]: Prefix Sliding reduces the memory cost of long model reasoning by retaining the original instruction plus only a moving window of recent text.

[ALLOY]: So the model keeps thinking, but it doesn’t drag every earlier thought behind it?

[NOVA]: Exactly. Older intermediate steps are discarded as the model proceeds, placing a ceiling on working memory even when the reasoning chain keeps growing. Researchers report roughly a threefold speed increase without retraining while preserving accuracy. Models trained with the same policy extended beyond one hundred thousand reasoning steps.

[ALLOY]: That doesn’t prove every discarded thought was useless. It suggests much of the middle history stops contributing once the model advances. Long-running agents currently pay repeatedly to carry expanding context through every step, so a stable recent window could reduce memory pressure. The tradeoff is selective forgetting: an early discovery may still matter after it leaves the window.

[PAUSE]

## [19:26] Open WebUI Adds Human-in-the-Loop Tool Approval

[ALLOY]: Open WebUI release .11 adds a human approval gate for tool calls. Because it’s a self-hosted interface used in local-AI systems, attached tools can turn a conversation into action. An administrator enables the capability, and a conversation can switch from automatic execution to a mode where every requested tool call waits for an allow or deny decision. The person responds by button or keyboard shortcut, one call at a time.

[NOVA]: Finally, a local interface is treating the jump from words to actions as a visible event. The choice is remembered when someone returns to the conversation. The documented capability is deliberately narrow: administrator-level enablement, a per-conversation mode, and per-call decisions. It doesn’t claim to be a workspace-wide policy engine. Narrow is fine. A local model that can search files, contact services, or alter data crosses a meaningful boundary when it invokes a tool. Open WebUI now places a decision at that boundary without removing tools entirely. The same conversation can remain useful for analysis while a sensitive action waits for a person. That separation is especially valuable when a model proposes several calls and only one deserves permission. I wouldn’t confuse repeated clicks with complete governance—a persuasive harmful request can still be approved, and approval says nothing about whether the underlying tool is safely designed. But explicit consent makes silent execution less likely and gives human intent a clear opportunity to interrupt the action before it reaches another system.

[PAUSE]

## [20:46] Google Splits Its Eighth-Gen TPU Lineup at Hot Chips

[NOVA]: Google presented its eighth-generation Tensor Processing Unit family at Hot Chips as two workload-specific chips: TPU 8t for training and TPU 8i for inference. Training is the expensive process of teaching a model from data; inference is the repeated work of using that model to produce results. Google is designing separate silicon around those different demands instead of presenting one chip as the universal answer.

[ALLOY]: That split echoes Jalapeño. Once inference becomes a huge recurring workload, optimizing only for giant training runs leaves money and power efficiency on the table. Training favors enormous parallel computation and communication across accelerators. Inference also has to handle response time, serving volume, memory access, and traffic that rises and falls unpredictably. A matched family lets Google tune each chip while keeping related software, networking, and cloud infrastructure around them. Google’s unusual advantage is that it can shape the model software, compiler, data-center network, accelerator, and cloud service together rather than buying every layer from separate vendors.

[NOVA]: I’m interested, but the Hot Chips disclosure establishes the division of labor more clearly than it establishes customer economics. Public conclusions still need Google Cloud availability, workload-specific benchmarks, and pricing. Google’s TPUs generally reach outside developers through its cloud and selected partners, and conference presentations often arrive before broad availability. If 8t lowers the cost of large training clusters while 8i improves serving throughput or latency, Google can turn hardware specialization into visible cloud advantages. It could also allocate expensive training capacity separately from the steadier fleet needed to answer production requests. For now, the firm fact is that Google no longer wants one eighth-generation TPU to represent both jobs. The competitive question is whether customers can see those gains in actual services—and buy them at a price that matters.

[PAUSE]

## [22:08] GitHub Project Radar

[NOVA]: Nanobot arrives with forty-seven thousand four hundred sixty-six stars on its first tracked appearance. It’s an ultra-lightweight, self-hosted Python agent framework combining a web interface, tools, memory, Model Context Protocol support, multi-agent workflows, automation, and chat integrations. Release .3 landed July twenty-fifth, and the repository was active again August twenty-seventh. Codebase Memory MCP is close behind at forty thousand eight hundred seventy stars, up six thousand one hundred twenty-three in thirty days—a seventeen-point-six-percent jump. It turns repositories into persistent knowledge graphs and claims sub-millisecond queries across one hundred fifty-eight languages from a dependency-free static binary.

[ALLOY]: Those two fit together unusually well: Nanobot can coordinate personal agents, while Codebase Memory gives coding agents a durable repository map instead of making them repeatedly read the same files. FastMCP supplies the Python construction layer for custom Model Context Protocol servers. It has twenty-seven thousand four hundred six stars, gained five hundred ninety-five over thirty days, and shipped release three point four in August. Codebase Memory has the strongest traction event with release .10 and that seventeen-point-six-percent growth. FastMCP’s increase is smaller, but its role is foundational: it helps developers expose their own services as tools the other agent systems can call.

[PAUSE]

## [23:34] Model Discovery Check

[NOVA]: Model progress today landed in architecture, serving, and domain adaptation rather than a new general-purpose flagship. Qwen three point eight Flash pairs multimodal reasoning with a million-token context window, while GLM five point three Flash offers native multimodality, efficient coding, and roughly one-point-three-million tokens of context through hosted access.

[PAUSE]

## [24:12] Local LLM Spotlight

[ALLOY]: The selected local release is zai-org/GLM-5.3-Flash, spoken as Z.ai’s GLM five point three Flash. It’s trending on Hugging Face with one thousand two hundred forty-eight likes, thirty-four recorded downloads, and an MIT license. Its published tags cover text generation, conversation, and image-to-text work across English and Chinese, with weights packaged in Safetensors for common transformer runtimes.

[NOVA]: That combination is compelling: long context, multimodal input, and downloadable weights aimed at coding and extended agent tasks without forcing every request through a closed application. “Open” doesn’t erase deployment cost; the weight format, context behavior, benchmark conditions, and hardware requirements determine where it can realistically run. But direct access to the weights gives organizations control over data placement, serving, and modification that an API-only listing can’t provide.

[PAUSE]

## [25:04] Extra Research Candidates

[NOVA]: Radar makes podcasts searchable—and usable by AI agents. Particle’s platform has transcribed and indexed more than one hundred thirty thousand podcasts, exposing their conversations through search, an API, and Model Context Protocol. EDB, meanwhile, argues that governance has to live in the data layer because executable policy can control rapid agent access more reliably than prompt-level requests.

[ALLOY]: Those developments collide neatly: agents can query spoken knowledge as structured data, so access policy has to travel with that data. Perplexity’s Portable Computer covers execution by combining local models, a harness, connectors, and an operating-system-enforced sandbox on NVIDIA DGX Spark. Local steps carry no per-token charge, while the sandbox provides a defined boundary around what those steps can touch.

[PAUSE]

## [25:48] Closing

[NOVA]: For the sources, specifications, project pages, and supporting details behind everything we covered, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily.

[NOVA]: We'll be back soon.
