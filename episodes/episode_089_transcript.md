# AgentStack Daily EP089 — Kimi K3 Lands at 2.8T Parameters, Pricing Stings

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: Moonshot just put 2.8 trillion parameters behind Kimi K3, making it the first openly available model to enter the 3-trillion class. That's huge. The price is huge too: three dollars per million input tokens and fifteen dollars per million output. Meanwhile, a coding tool claims it can answer repository questions with 99 percent fewer tokens, and a 27-billion-parameter chat model is squeezing into local machines with 2-bit ternary weights.

[ALLOY]: Okay, that's actually wild — the biggest model here may not produce the biggest change. People are already using these systems to navigate whole codebases through knowledge graphs, manipulate Unity scenes and C-sharp scripts from chat, and fine-tune image and video generators across NVIDIA hardware without writing every training component themselves.

[NOVA]: Today: the terminal-based coding agent Codex point one-four-four-six fixes context metadata for three GPT-5.6 tiers; Kimi K3 challenges frontier models at frontier pricing; and Medicare puts AI-assisted prior authorization into six states. You'll hear about million-token reinforcement learning, an open generalist video model, repository-level Copilot metrics, and the fast-growing tools turning MCP into ordinary application infrastructure.

[PAUSE]

## [02:00] Agent Stack Release Readout: OpenAI Codex Point One-Four-Four-Six

[NOVA]: OpenAI shipped point one-four-four-six for Codex on July 18. The terminal-based coding agent received a focused metadata correction for three GPT-5.6 tiers: Sol, Terra, and Luna. Their bundled context windows now read 272,000 tokens, and the release refreshes the instructions packaged with those models. Not glamorous. Also not optional trivia when the software planning a long coding job relies on that number.

[ALLOY]: Right, because the harness decides how much material it can safely carry based on the capacity it thinks the model has. If Codex believes the window is smaller than 272,000 tokens, it may summarize or discard useful repository material early. If it believes the window is larger, a long session can hit the real limit, lose older context, or stop at exactly the wrong moment. A metadata field sounds tiny until a multi-file refactor depends on it.

[NOVA]: The correction came through two pull requests from the same engineer. One brought refreshed bundled model metadata into the point one-four-four line. The second constrained the hotfix to GPT-5.6 prompts and context, leaving other model families untouched. That's the sensible kind of surgical patch: correct Sol, Terra, and Luna without turning a metadata repair into a broad behavioral change. The extra 72,000 tokens relative to a 200,000-token assumption can hold a substantial amount of source, documentation, tool output, and conversation history. It doesn't guarantee better reasoning, but it gives the agent more accurate boundaries while deciding what to retain.

[ALLOY]: And I like this more than a vague “performance improvements” release, because the consequence is legible. Long-running refactors and migrations can stay coherent for longer when the agent knows its actual working space. A migration that spans application code, tests, configuration, and generated tool output may fit in one continuous working history instead of forcing an early summary. The next useful development would be the same metadata alignment reaching any other affected model families, or a broader point one-four-five release that consolidates the repair. For now, point one-four-four-six fixes a quiet source of truncation and underuse for the three named GPT-5.6 tiers.

[PAUSE]

## [03:26] Moonshot Drops Kimi K3 at 2.8 Trillion Parameters — Pricing Stings

[ALLOY]: Moonshot didn't nibble at the frontier. Kimi K3 has 2.8 trillion parameters, more than twice K2.6 and well above DeepSeek's 1.6-trillion-parameter V4 Pro. Moonshot calls it part of the 3-trillion class, and it becomes the first openly available model at that scale. Early results put it near the strongest closed systems rather than merely atop the open-weight field.

[NOVA]: The outside numbers are striking. K3 scored 1,547 Elo on Artificial Analysis's private long-horizon knowledge-work test, 732 points above K2.6 and second only to Claude Fable 5. It also reached number one on Arena's Frontend Code leaderboard, which compares generated web interfaces. Moonshot separately reports wins over Claude Opus 4.8 max and GPT-5.5 high, while trailing Claude Fable 5 and GPT-5.6 Sol. Those last comparisons come from Moonshot, so I don't buy them as settled until independent runs reproduce them.

[ALLOY]: And then comes the bill: three dollars per million input tokens, fifteen dollars per million output. K2.6 cost ninety-five cents in and four dollars out. K3 now sits around Claude Sonnet pricing and becomes the most expensive model released by a Chinese lab. Artificial Analysis estimates ninety-four cents per task, close to GPT-5.6 Sol at one dollar and four cents and below Opus 4.8 at one dollar and eighty cents. K3 also used 21 percent fewer output tokens than K2.6 on that evaluator's intelligence index, so the effective increase isn't quite as brutal as the posted rate.

[NOVA]: Still not cheap. The open-weight release promised by July 27 will decide whether K3 is mainly a premium API or a model the wider ecosystem can genuinely operate and adapt. Moonshot's web product and API are already live, but API-tier details are still arriving. Would you pay frontier rates for an open model if it beats closed rivals on your actual work? That's the contest now: quality per completed task once independent users get the weights.

[PAUSE]

## [05:17] Prism-ML's Ternary-Bonsai-27B Hits Trending as a Local-AI Power Move

[NOVA]: Ternary-Bonsai-27B is moving in the opposite direction from Kimi K3: not more scale, but more aggressive compression. Prism-ML released the 27-billion-parameter chat model in GGUF, a file format built for efficient local inference, with its weights stored at 2-bit ternary precision. Each weight uses one of three possible values. That dramatically shrinks storage compared with the common 4-bit versions of similarly sized models.

[ALLOY]: Which makes the name “Bonsai” unusually honest. The repository is tagged for llama.cpp, CUDA acceleration on NVIDIA hardware, and Metal acceleration on Apple devices. It has passed 338,000 downloads and 760 likes since landing July 4. A 27-billion-parameter model that can run through a consumer GPU, an Apple Silicon MacBook, or even a CPU-only machine gives local developers a meaningful chat endpoint without sending every prompt to somebody else's server.

[NOVA]: Hold on, though — tiny weights don't prove strong answers. Ternary compression can sacrifice nuance, instruction following, or reliability, and the current excitement comes from distribution and packaging more than broad independent comparisons. The model is conversationally fine-tuned and ready for local runtimes, but its quality against ordinary 4-bit builds remains the unanswered part. Speed also depends heavily on whether runtimes exploit ternary values efficiently rather than merely decoding them as a novelty format.

[ALLOY]: Fair pushback, but 338,000 downloads says the question is being tested at scale. If llama.cpp and related tools turn the smaller representation into genuinely faster generation, the model could reset expectations for offline assistants and private agents on modest hardware. It could also widen local use beyond chat: repository search, private document analysis, and background classification don't always require frontier reasoning on every turn. If quality falls apart, it'll be a clever compression demo. Either way, Ternary-Bonsai asks how much useful intelligence can fit into a machine already sitting on a desk.

[PAUSE]

## [07:08] Medicare's WISeR Puts AI in Prior Authorization for Six States

[ALLOY]: This one worries me more than any leaderboard. Medicare's WISeR Model has put AI-assisted screening into prior authorization for selected Original Medicare services in Arizona, New Jersey, Ohio, Oklahoma, Texas, and Washington. CMS launched the program in January, and it runs through December 2031. Six technology companies participate, one per state, with compensation tied partly to spending their reviews prevent.

[NOVA]: The covered services have established coverage criteria and are considered vulnerable to waste, fraud, or patient harm. Examples include skin and tissue substitutes, implanted electrical nerve stimulators, and knee arthroscopy for osteoarthritis. AI tools screen the cases, but a licensed clinician must make every final recommendation to deny payment. Emergency cases, inpatient-only services, and situations where delay could endanger a patient are excluded. Original Medicare's coverage rules and provider choice remain unchanged, and Medicare Advantage isn't part of the program.

[ALLOY]: Providers can seek authorization before delivering a service or face pre-payment review afterward. Consistently compliant providers may earn a gold-card exemption that lets them skip review. That could reduce repeated paperwork for clinicians with clean records. But tying vendor compensation to averted expenditure creates an obvious tension: a system can save money by identifying inappropriate care, or by making appropriate care harder to obtain. Human sign-off helps, but it doesn't erase the incentive.

[NOVA]: Exactly. Faster decisions and lower costs are goals, not observed outcomes. CMS says payments will also reflect process measures such as provider experience, yet the first meaningful evidence will come from denials, appeals, delays, reversals, and clinician feedback. How would you feel if an algorithm surfaced your medical claim for rejection while its vendor earned more from prevented spending? WISeR is now a six-year federal test of whether clinical review software can reduce abuse without converting friction into a business model.

[PAUSE]

## [08:59] NVIDIA and Hugging Face Publish a Scaling Guide for Fine-Tuning Video and Image Models

[NOVA]: NVIDIA and Hugging Face published a joint guide on July 17 for fine-tuning image and video diffusion models at scale. Diffusion models are the systems behind many current generators that progressively turn noise into an image or video. The guide connects NVIDIA's NeMo Automodel with Hugging Face's Diffusers library, giving teams a documented route from an open model to distributed customization across GPUs.

[ALLOY]: This isn't a new model, chip, or hosted product, and that's precisely why it could be underhyped. Video fine-tuning has often meant stitching together model code, data loading, memory management, and distributed training from scattered examples. NeMo Automodel handles more of the large-scale training layer, while Diffusers supplies familiar open model components. Bringing them together can spare teams from inventing a custom training loop before they ever reach their own footage or image collection.

[NOVA]: Let's not award it benchmark trophies it doesn't contain. The publication doesn't provide a sweeping set of multi-GPU performance numbers or establish one universal recipe for every model family. It's a documentation milestone. Its value depends on the supported architectures, the quality of the examples, and whether outside teams reproduce the workflow without undocumented fixes. The next useful additions would name more model families and report scaling behavior across actual GPU configurations.

[ALLOY]: Agreed, but mature infrastructure often arrives as boring documentation before it becomes normal practice. Open diffusion software already gives teams model access; repeatable distributed fine-tuning is what turns that access into a sports-video generator, a product-imagery system, or a domain-specific visual tool. Media companies could adapt a video model to their archive, while manufacturers could tune image generation around their own products and visual standards. NVIDIA and Hugging Face are making their ecosystems meet in one place. That connection may save more time than another model announcement.

[PAUSE]

## [10:47] Research Digest: LongStraw Pushes Reinforcement-Learning Training Past Two Million Tokens

[NOVA]: LongStraw tackles a nasty mismatch: models can process million-token inputs during use, but reinforcement learning often trains agents on trajectories capped around 256,000 tokens. Reinforcement learning here means improving behavior through feedback on completed actions. LongStraw reports training beyond two million tokens within a fixed GPU budget.

[ALLOY]: That's exciting because long-running agents don't experience work as one tidy prompt. They accumulate documents, tool calls, failed attempts, observations, and earlier decisions. Training on shortened histories can teach behavior that collapses once the real trajectory becomes much longer.

[NOVA]: The researchers describe LongStraw as an execution stack shaped around the underlying model and hardware, rather than a larger GPU requirement. If it reaches common open training frameworks, labs could teach agents across trajectories closer to production length. The paper establishes a capability, not proof that two-million-token training automatically creates better agents. Adoption and measured downstream gains are what matter next.

[PAUSE]

## [11:52] Research Digest: VideoChat3 Pushes Open Video AI Toward True Generalist Use

[ALLOY]: VideoChat3 aims at a genuinely useful combination: open weights, open training data, and one model that handles motion, long recordings, and streaming video. Instead of separate specialists for a sports clip, cooking demonstration, and security feed, the researchers want a generalist that can interpret all three.

[NOVA]: The team also claims lower compute requirements than comparable open video models. That matters for organizations working on workstation GPUs or sensitive footage, because they can adapt the model without paying per video or uploading recordings to a closed provider. Still, benchmark breadth isn't the same as reliable performance in messy real scenes.

[ALLOY]: Exactly — I'm interested, not converted. The important next evidence is whether independent teams fine-tune VideoChat3 for their own footage and keep its abilities across different kinds of motion, duration, and streaming input. If that happens, open video understanding moves from isolated research demos toward a reusable foundation.

[PAUSE]

## [13:00] Codebase Memory MCP Cuts Coding-Agent Token Use by 99 Percent

[NOVA]: Codebase Memory MCP makes one enormous claim: 99 percent fewer tokens than putting raw source into a coding model's context window. DeusData released point nine on July 8 as a dependency-free static binary. It indexes an average repository into a persistent knowledge graph in milliseconds, reports query responses under one millisecond, and supports 158 programming languages. The repository has reached 32,815 GitHub stars.

[ALLOY]: A knowledge graph stores relationships among code elements, so an agent can ask where authentication lives, which function calls an API, or what depends on a changed class. MCP, the Model Context Protocol, lets the coding agent invoke that graph as an external tool. Instead of repeatedly shipping whole files into the model, the agent gets a focused map and retrieves only the source it needs. That's a much smarter use of a limited context window.

[NOVA]: And 99 percent is the part to treat carefully. That number comes from the project, not an independent benchmark, and savings will vary with repository size, query type, and what the agent eventually has to read. A graph can also become stale or omit dynamic relationships that aren't obvious from static code. The claims about millisecond indexing and sub-millisecond queries need more evidence on multi-million-line monorepos.

[ALLOY]: Even with that caveat, this may be more consequential than Kimi K3's parameter count. Context is expensive, and coding agents lose coherence when irrelevant source crowds out instructions and recent decisions. Persistent memory also means a later session can reuse the repository map instead of rebuilding understanding from pasted files. A single binary that turns code into callable memory could lower cost and keep multi-file work on track. It isn't making the model's window larger; it's making the material inside that window more selective. That's the useful trick.

[PAUSE]

## [14:48] FastMCP Point Three-Four-Four Lands as Python's Go-To MCP Server Builder

[ALLOY]: FastMCP has become the default-looking answer when a Python developer asks how to expose a function or data source to an agent. Point three-four-four shipped July 9, the repository has 26,263 stars, and development continued through July 19. That's substantial traction for infrastructure whose job is largely to make protocol plumbing disappear.

[NOVA]: FastMCP builds servers and clients for the Model Context Protocol. A developer can wrap a Python function, database, internal API, dataset, or script so compliant AI systems can discover and call it. The library handles protocol messages, schemas, and transport details that teams would otherwise write themselves. “Pythonic” in this context means the code follows familiar Python patterns instead of forcing developers into a separate integration language.

[ALLOY]: Which sounds mundane until every organization has dozens of useful internal systems that no model can safely reach. FastMCP lowers the cost of turning those systems into explicit tools with typed inputs rather than handing an agent broad shell or network access. It also supports the client side, so Python applications can consume MCP services as well as publish them. A company can expose inventory lookup, ticket creation, or report generation as narrow actions. The protocol stays portable while the implementation feels native to the language.

[NOVA]: I wouldn't declare any framework permanent in an ecosystem moving this fast, but 26,000 stars and an active major version make FastMCP more than a weekend wrapper. Its next challenge is keeping client ergonomics, security controls, and compatibility moving together as MCP expands. Right now, Python teams have a well-traveled route for connecting agents to real software without rebuilding the protocol layer for each tool.

[PAUSE]

## [16:33] Microsoft's MCP for Beginners Curriculum Crosses 16,700 GitHub Stars

[NOVA]: Microsoft's MCP for Beginners has crossed 16,700 GitHub stars after another repository update on July 17. It's a free, open-source curriculum for learning how AI assistants connect to tools and data through the Model Context Protocol. The course includes working examples in .NET, Java, TypeScript, JavaScript, Rust, and Python.

[ALLOY]: That's more important than the star count alone. Most protocol tutorials quietly demand that people learn the author's favorite language before learning the protocol. Microsoft lets a Java developer stay in Java, a .NET team stay in C-sharp, and a Python team stay in Python. The lessons cover modular servers, reusable components, permission boundaries, and ways to add tools without rebuilding earlier integrations.

[NOVA]: Build one standards-based connector, and multiple compatible clients can use it. That's the promise. The course gives organizations a common vocabulary for details that usually get skipped in demos: what an agent may access, how a server limits its surface, and how independently developed tools fit together. Because the material is open source, teams can adapt examples around their own services and use the same concepts across language groups instead of maintaining separate training material for every stack.

[ALLOY]: I do think 16,700 stars reveal something broader from the FastMCP story: MCP adoption has moved beyond library authors. People need education, examples, and secure patterns now. The curriculum doesn't use versioned releases, and its contents can change as the repository evolves, so it behaves more like living documentation than a fixed textbook. That's probably appropriate. A course teaching a rapidly changing protocol shouldn't pretend the ground has stopped moving.

[PAUSE]

## [18:31] mcp-use Crosses 10,000 GitHub Stars as a Fullstack MCP App Framework

[ALLOY]: Here's the gap mcp-use wants to erase: teams build an MCP server, then separately build the interface people see in a chat application, then spend time keeping both aligned. mcp-use combines them. The open-source fullstack framework has 10,328 GitHub stars, released point one-thirty-four-three on July 8, and was still receiving repository updates on July 19.

[NOVA]: One project can publish an MCP server that compliant agents call and an MCP app containing the buttons, cards, and widgets rendered inside ChatGPT or Claude. The server defines what a tool can do. The app gives that tool a visible, interactive surface when a conversation invokes it. Changes can land in both from one codebase instead of splitting protocol logic and user-interface behavior across separate projects.

[ALLOY]: That's genuinely useful. MCP has spent a lot of time sounding like invisible plumbing, but applications need more than a successful tool response. A travel tool may return selectable flights. A reporting tool may show a chart. A support system may need confirmation controls before changing an account. mcp-use gives those experiences a framework while preserving a standards-based server for other clients.

[NOVA]: The open question sits outside the project: how far Anthropic and OpenAI expand their in-chat application surfaces, and how consistently those surfaces behave. mcp-use is already shaped for both, which reduces the chance of a complete rewrite, but platform differences don't magically vanish. Still, crossing 10,000 stars suggests developers aren't satisfied with headless tool servers. They want complete agent applications, including the moment a person sees, understands, and acts on the result.

[PAUSE]

## [20:19] GitHub Copilot Usage Metrics Now Break Down Per Repository

[NOVA]: GitHub made repository-level Copilot usage metrics generally available on July 17. Two new REST endpoints return daily, per-repository pull-request activity for the Copilot coding agent and Copilot code review. Previously, the same reporting surface aggregated activity at the organization level, hiding whether adoption was widespread or concentrated in a few repositories.

[ALLOY]: Finally. An organization-wide total can look impressive while three enthusiastic teams generate nearly everything. Repository breakdowns reveal where the coding agent is opening or contributing to pull requests, where automated review is growing, and where licensed tools are barely present. Engineering leaders can compare services without pretending one average describes every team.

[NOVA]: The data can feed an existing dashboard, internal metrics page, or leadership report through ordinary API calls. A daily time series also shows whether adoption changes after training, policy updates, or team-level rollouts. But usage isn't value. More Copilot pull-request activity may reflect useful acceleration, noisy automation, or simply a repository with more work. GitHub is measuring where the tools act, not whether their suggestions are correct or economically worthwhile.

[ALLOY]: Which connects directly to the ROI scorecard coming later. Repository-level attribution supplies one missing layer between “we bought seats” and “the organization uses AI.” It still needs delivery outcomes, review burden, and quality data around it. A repository with rising automated reviews but longer human review times tells a very different story from one shipping accepted changes faster. Future cuts by language, seat, or acceptance rate could make the reporting richer. For now, GitHub can expose the long tail where Copilot never took hold — and the pockets where it quietly became everyday work.

[PAUSE]

## [22:15] Unity-MCP Ten-One Turns the Editor Into a Callable Tool Surface

[ALLOY]: “A screenshot and a prayer” has been the unofficial interface between many coding agents and game engines. Unity-MCP ten-one, released July 13 by CoplayDev, gives the agent direct tools instead. Through MCP, it can inspect and manipulate the Unity Editor rather than guessing what a scene or project contains. The repository has 12,645 stars and was updated on release day.

[NOVA]: The server exposes scene objects, assets, scripts, menu commands, and editor operations as structured calls. An assistant can list or rename files, inspect the scene graph, modify GameObjects, read and write C-sharp scripts, reimport assets, save prefabs, and capture screenshots for inspection. That matters because Unity projects encode important state outside plain source files. A terminal-only coding agent can edit C-sharp, but it can't reliably infer every object relationship in an open scene.

[ALLOY]: This is where agent tooling starts feeling physical, even though the “world” is a game editor. A solo developer can hand off repetitive asset organization, scene cleanup, or routine script changes while still reviewing the resulting actions. Larger studios get a more complicated proposition: once chat can alter scenes and scripts, access controls, audit trails, and review boundaries become production concerns rather than theoretical governance slides.

[NOVA]: And no, I don't think that means “describe a game and ship it.” Unity projects are full of visual judgment, performance constraints, and fragile dependencies. But structured editor access is far better than blind text generation. An agent can observe the scene graph, make a bounded change, and inspect the resulting editor state rather than hallucinating success from source alone. The next contest is whether Unity's first-party AI features converge with projects like Unity-MCP or compete against them. Two agent pathways into the same editor rarely stay separate once developers expect portable tool access.

[PAUSE]

## [23:59] OpenAI's CFO Publishes a Four-Metric Scorecard for AI ROI

[NOVA]: OpenAI chief financial officer Sarah Friar published a four-part AI scorecard on July 17: useful work, cost per successful task, dependability, and return on compute. Coming from a finance executive, it treats AI as an operating investment rather than a collection of benchmark wins. Honestly, that's overdue.

[ALLOY]: Useful work counts completed production tasks, not generated tokens or chat sessions. Cost per successful task asks what each acceptable outcome costs, allowing a subscription, enterprise contract, hosted API, or self-hosted model to be compared on results. Dependability captures whether the answer works on the first attempt or sends a human back through the task. That rework is the labor cost many pilots conveniently forget.

[NOVA]: Return on compute asks how much useful output the organization receives for each dollar spent on GPUs or APIs. Together, those measures cut through a common procurement mistake: buying the model with the best general benchmark and assuming it must create the best business result. A cheaper model that finishes more tasks correctly can beat a premium model. A fast agent that creates review debt can be worse than a slower, steadier one. Kimi K3's lower output-token use is a good example: posted rates alone don't reveal the final task cost.

[ALLOY]: I like the frame, but it isn't evidence yet. OpenAI's piece doesn't publish reference values or independent benchmarks; it supplies categories. The interesting test is whether finance and procurement teams outside OpenAI adopt them, and whether vendors become willing to report cost per successful task instead of carefully chosen capability scores. Pair the framework with GitHub's new repository metrics and organizations can begin connecting activity to outcomes. The hard part remains agreeing on what “successful” means before somebody turns the dashboard green.

[PAUSE]

## [25:47] GitHub Project Radar

[NOVA]: CoplayDev's Unity-MCP leads the radar at 12,645 stars. Its first tracked appearance follows the ten-one release on July 13, with the repository updated that day. It turns Unity scenes, C-sharp scripts, assets, and editor commands into MCP tools. Connected to a coding agent, it supports a loop where the model reads the scene graph, changes code or objects, and invokes editor actions instead of relying only on text files. That's direct integration with the environment where the work actually lives.

[ALLOY]: Lastmile AI's MCP-Agent has 8,430 stars. Its most recent tagged release is point zero-zero-twenty-one from May 2025, and the repository was updated in January 2026; this is its first tracked appearance. The Python framework wraps multiple MCP servers into reusable agents with deterministic patterns for parallel work, routing, and orchestration. It fits where one agent needs to fan out across several services without a hand-built sequence of tool calls. In other words, less improvisational glue and more explicit workflow structure.

[NOVA]: Upsonic has 7,915 stars, with point seventy-seven-three released in May and repository activity in June. The Python SDK combines autonomous tool use, task graphs, and a built-in evaluation harness. Its integration angle is unusually concrete: generated work can move through an explicit pass-or-fail evaluation stage inside the same runtime. That's useful when an agent iterates on code or structured tasks and the team wants outcomes graded by defined criteria rather than a model's confidence. The traction across all three repositories shows MCP spreading into editors, multi-agent coordination, and evaluated execution.

[PAUSE]

## [27:23] Model Discovery Check

[ALLOY]: Model progress today landed in scale, compression, multimodal packaging, and training infrastructure rather than another newly listed general-purpose API name. Kimi K3 pushed the parameter frontier, Ternary-Bonsai pushed local weights downward, and Inkling combined image, audio, and text in one open checkpoint.

[PAUSE]

## [27:45] Local LLM Spotlight: Inkling

[NOVA]: Thinking Machines' Inkling is an Apache-licensed, open-weight mixture-of-experts model that accepts image plus text or audio plus text and produces text. A mixture of experts activates selected parts of the model for each input rather than using every part every time. The repository includes evaluation results and compatibility metadata for hosted inference endpoints, so the same Hugging Face client code can address a locally loaded checkpoint or a hosted service.

[ALLOY]: Inkling drew 1,094 likes and 13,462 downloads in its early window. Its niche is grounded multimodal work: describing an interface while considering spoken context, analyzing media arriving through more than one channel, or powering assistants that can't assume every observation is text. Apache licensing allows broad adaptation. Early traction isn't proof of quality, but one checkpoint spanning image, audio, and text can simplify a local stack.

[PAUSE]

## [28:40] Extra Research Candidates

[ALLOY]: Repository-level GitHub Copilot usage metrics are now generally available, exposing daily pull-request activity for the coding agent and code review by repository instead of only organization-wide totals. That makes uneven adoption visible and gives engineering dashboards a more useful unit of comparison.

[NOVA]: OpenAI's “Why Teens Deserve Access to Safe AI” describes age-appropriate model behavior, learning tools, parental account controls, and outside expert partnerships. It isn't a separate teen model; the protections sit around ChatGPT as account-level controls and behavior changes. That matters because access and safety are being designed as product policy, not only model training.

[ALLOY]: And appcypher's Awesome MCP Servers has 5,699 stars. The curated index groups MCP server implementations by integration domain, making it a discovery layer for existing connectors to external services. Not glamorous, but very useful: as the protocol expands, finding a maintained server before duplicating one becomes part of the ecosystem's efficiency.

[PAUSE]

## [29:20] Practical Queue

[NOVA]: Codex now knows the 272,000-token boundaries of Sol, Terra, and Luna. Kimi K3 makes frontier-scale open models more capable and more expensive. Ternary-Bonsai and Inkling pull substantial chat and multimodal capability toward local hardware. WISeR makes AI-assisted medical review a live public-policy test, while LongStraw and VideoChat3 stretch open training and video understanding.

[ALLOY]: Codebase Memory, FastMCP, Microsoft's curriculum, mcp-use, Unity-MCP, and the radar projects show MCP maturing into applications, education, memory, and editor control. GitHub can locate Copilot activity by repository, and OpenAI's scorecard asks whether that activity produces dependable work at an acceptable cost.

[NOVA]: For source details and further reading, look at the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.
