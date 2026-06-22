# EP073 — OpenClaw 6.9, Hermes 6.19, Claude Code .176 Ship; Poolside Laguna XS.2 and M.1 Out

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: OpenClaw 6.9, Hermes Agent 6.19, and the terminal-based AI coding agent Claude Code point one seven six all shipped stable releases this cycle. OpenClaw 6.9 added richer Telegram delivery and tightened Codex integration with automatic plugin approvals, while Hermes 6.19 introduced background subagents and expanded channel support to iMessage via Photon.

[ALLOY]: Today you'll hear about those harness updates, the release of Poolside's Laguna coding models on OpenRouter and via API, new enterprise spend controls from OpenAI, and why the president of Signal says your AI chatbot is definitely not your friend. We also look at a billion-dollar raise for Baseten, a vanity search engine that scores your presence inside model weights, and the historical failure of export controls as a lens for Anthropic's Mythos model.

[NOVA]: The through-line is a focus on the production layer: how we manage the cost of agentic loops, how we secure the models at the center of them, and how the harnesses we use every day are maturing to handle multi-step, multi-channel workloads. [PAUSE]

## [02:00] Agent Stack Release Readout: OpenClaw 6.9; Hermes Agent 6.19; Claude Code CLI .176

[ALLOY]: Three stable releases landed this cycle and shape how agentic harnesses are being assembled right now. OpenClaw 6.9, published on June twenty-first, ships richer Telegram delivery. The channel path now sends rich HTML, preserves rich markdown and sticker paths, and renders progress drafts and command output more faithfully. It also normalizes HTML tables safely and keeps mentions and spooled handlers on the right delivery path. Agent recovery is more dependable in this version; retries, terminal outcomes, and session history repair now keep more interrupted or partial turns moving toward a visible final result.

[NOVA]: The Codex integration in OpenClaw is also significantly stronger. It adds automatic plugin approvals, GPT-5.3 Spark OAuth routing, and remote-node execution as a dynamic tool. These changes move the harness toward a more reliable app-server teardown process. Meanwhile, Hermes Agent 6.19, which the maintainers are calling the Reach Release, extends Hermes across new channels like iMessage via Photon and the Raft agent network. The desktop app gained substantial new capability as well; subagents can now run in the background, and the image generation tool learned how to edit.

[ALLOY]: The Hermes dashboard got a full profile builder and the Skills Hub browser was completely rehauled. For those using the terminal-based coding agent OpenAI Codex point one four one, these updates provide a more robust backend. We also saw the terminal-based AI coding agent Claude Code point one seven six round out the trio on the stable tag. This release focuses on a lighter install footprint and a faster cold-start path for shell-driven sessions.

[NOVA]: At the API and runtime layer, these changes alter what builders can configure and rely on by default. The practical implication is cleaner harness plumbing. OpenClaw gives builders more model routes and safer auth, while Hermes and Claude Code refine the user and developer experience. The part to watch is how these new defaults behave under real workloads before flipping them to production, especially where session history and terminal outcomes are involved. [PAUSE]

## [02:40] Poolside ships Laguna XS.2 compact coding model on OpenRouter

[ALLOY]: Poolside pushed Laguna XS.2 to OpenRouter this week, marking the second-generation model in their XS size class. This is their efficient coding agent series, and the pitch here is compactness over flagship reasoning. It pairs tool calling with reasoning in a small footprint, featuring a context window of two hundred sixty-two thousand, one hundred forty-four tokens. This context size puts it squarely in the long-context tier for agentic coding workloads where passing large codebases or tool traces is the norm.

[NOVA]: The single most relevant detail for builders is the unified tool-and-reasoning pairing. One endpoint exposes both tool invocation and reasoning, which simplifies agent loop orchestration. You don't have to route requests across two separate models to handle planning and execution. The XS size class signals a target audience focused on low-latency, cost-sensitive runs. If you are running multi-file refactor agents, the per-token economics here might be more attractive than flagship-class reasoning models.

[ALLOY]: For agent builders, this release widens the compact tier on the router. It sits alongside other compact picks used for cheap classification or initial planning passes. What we need to watch next are the actual latency benchmarks on real coding traces. We also want to see if Poolside eventually ships tool-calling-specific rate limits or pricing tiers to further differentiate the XS line from their larger models.

[NOVA]: This refresh of the compact tier matters because it moves the cost frontier rather than just the raw-quality frontier. If your agent stack relies on many small, iterative calls, a second-gen compact model with a massive context window is a significant integration target. It allows for more complex multi-step workflows without the latency hit of a larger flagship model. [PAUSE]

## [03:40] Poolside: Laguna M.1 lands via API

[ALLOY]: Moving to the other end of the spectrum, Poolside has also released Laguna M.1 via API. This is their flagship coding agent model, optimized for complex software engineering tasks. Like its smaller sibling, it supports tool calling and reasoning with a two hundred fifty-six thousand token context window. At the mechanism level, this change shows up in the API surface and the runtime behavior that agent builders integrate against.

[NOVA]: The Laguna M.1 release is aimed at the heavy lifting of agentic coding. Think about architectural changes, complex bug fixes, and large-scale refactors that require a deep understanding of the entire stack. The primary source documentation for this model includes specific deployment notes and changelog context that builders should review. It is worth tracking how M.1 behaves under heavy production loads, as flagship coding models often face unique challenges with consistency over long traces.

[ALLOY]: Why this matters right now is the speed at which the agent stack is moving. Changes at this layer determine which workflows are reliable and which ones remain brittle. The practical question for builders is whether Laguna M.1 can replace their current flagship default for coding tasks. Early evidence suggests it is a strong contender for those building autonomous or semi-autonomous engineering agents.

[NOVA]: We should be watching for follow-up releases and independent benchmark results. As surrounding tooling like SDKs and security review frameworks pick up support for M.1, the barrier to switching will drop. For now, the focus is on verifying its performance against the specific coding patterns your agents are expected to handle. [PAUSE]

## [04:35] New usage analytics and updated spend controls for enterprises

[ALLOY]: OpenAI is introducing new spend controls and usage analytics for ChatGPT Enterprise. This is a direct response to organizations needing to manage costs and scale their AI deployments with more confidence. These controls land at the management and API level, affecting how admins configure and deploy seats across a large company. It includes more granular cost breakdowns and the ability to set configurable ceilings on spend.

[NOVA]: For builders and platform engineers, these tools are about visibility. As agents proliferate within a company, knowing exactly which departments or projects are driving usage is critical. The updated analytics allow for a clearer view of how tokens are being consumed, which helps in predicting future budget needs. It also helps identify inefficient agent loops that might be burning through budget without delivering equivalent value.

[ALLOY]: These spend controls shift what the enterprise stack can rely on by default. Instead of reacting to a high bill at the end of the month, admins can now proactively set limits. It is worth tracking how these controls impact agent performance, especially if a ceiling is reached mid-session. Builders need to ensure their agents can handle graceful degradation or clear notification when budget limits are hit.

[NOVA]: This move by OpenAI reflects the maturing of the enterprise AI market. Cost management is no longer an afterthought; it is a core requirement for production deployments. We expect to see other major providers follow suit with similar enterprise-grade visibility and control features as the focus shifts from experimentation to operational efficiency. [PAUSE]

## [05:29] 30 years of export controls failed before — what about Mythos?

[ALLOY]: A recent analysis argues that thirty years of U.S. export controls on encryption and cybersecurity software have largely failed to slow their spread. This historical context is now being applied to Anthropic’s Mythos cybersecurity model. The core argument is that dual-use software has always leaked, forked, and been re-implemented regardless of jurisdiction. The historical mechanism that failed involved treating source code or compiled binaries as the controlled artifact.

[NOVA]: For Mythos, the challenge is even greater. The question is whether model weights, training compute, or hosted inference APIs can be effectively controlled at all. Unlike a compiled binary, a model’s capability is harder to pin down to a specific artifact. This makes the surface for regulation much more complex. The analysis suggests that the diffusion mechanism for AI will likely follow the same path as cryptographic tools: code forks and foreign re-implementations will outpace any regulatory framework.

[ALLOY]: For builders, the takeaway is that frontier AI cybersecurity capabilities will likely be globally accessible. You should assume that both defensive and offensive AI security tools will be available to a wide range of actors. This makes export classification a moving target for compliance teams. If you are building on or against Mythos, the classification of model weights and inference endpoints remains a point of ambiguity.

[NOVA]: We should be watching for any new rulemaking from the Commerce Department regarding frontier model weights. At the same time, keep an eye on whether Anthropic publishes a usage policy that attempts to pre-empt these regulatory questions. The fight over Mythos will likely set the policy frame for the entire AI security sector. [PAUSE]

## [06:30] Baseten Reportedly Raising $1.5B at $13B Valuation

[ALLOY]: AI inference startup Baseten is reportedly close to finalizing a one point five billion dollar funding round at a thirteen billion dollar valuation. This raise comes just months after their previous mega-round and highlights a major shift in the market. Inference is increasingly being treated as its own infrastructure category rather than just a feature of model training labs. Dedicated capital is flowing into companies that focus specifically on the serving side of the stack.

[NOVA]: The technical mechanism here is the inference-specific serving stack. This includes things like model compilation passes for production deployment and GPU pooling across heterogeneous hardware like H100s and H200s. Baseten’s differentiator is exposing these knobs to engineering teams as a managed service. Instead of relying on opaque API endpoints from a model lab, builders get more control over request routing and optimization for bursty or long-context traffic.

[ALLOY]: This massive raise signals that the inference layer is becoming a buyer’s market. There is real competition now between hyperscalers and specialized providers like Baseten, Fireworks, and Together. For builders, this means the default choice of an inference provider is no longer obvious. You should be explicitly evaluating the tradeoffs between cost-per-token, latency, and the level of customization available.

[NOVA]: We’ll be watching to see how Baseten positions itself against hyperscaler inference APIs like Bedrock or Azure AI. As more capital enters this space, the pace of innovation at the serving layer will likely accelerate. This is good news for agent builders who need reliable, high-performance infrastructure to power their production loops. [PAUSE]

## [07:27] Datasette Apps: Host custom HTML applications inside Datasette

[ALLOY]: Datasette has launched a new plugin called Datasette Apps that allows users to host custom HTML and JavaScript applications directly inside Datasette. These are self-contained applications that can leverage the data stored in the Datasette instance. The launch announcement highlights the "why" behind this move, focusing on the need for more flexible ways to visualize and interact with data without needing a separate hosting stack.

[NOVA]: For agent-stack builders, this is an interesting development in the UI layer. By hosting custom HTML inside the data tool itself, you can create tighter feedback loops for agents that are interacting with databases. It simplifies the deployment of internal tools and dashboards that require a specific frontend but need to be closely coupled with the data source. The change lands at the API and runtime level, affecting how you configure the plugin and deploy your custom apps.

[ALLOY]: This shift means builders can rely on Datasette as a more complete platform for data-driven agents. It is worth tracking how the plugin handles different workloads and how it scales with complex JavaScript applications. If you are building tools for data exploration or agent monitoring, this could significantly reduce your infrastructure overhead.

[NOVA]: We’ll be watching for how the community adopts Datasette Apps and what kind of custom interfaces start to emerge. As more builders experiment with this, we expect to see new patterns for agent-human collaboration surfaces that live directly on top of the data they are processing. [PAUSE]

## [08:27] Quiet Day in AI Shipping: AIE Promo Window Ahead

[ALLOY]: Recent newsletters have noted a relatively slow period for AI news, with no major model drops or agent framework releases dominating the cycle. This breathing room is often a sign of calendar-driven release coordination. With the AI Engineer, or AIE, conference on the horizon, many major labs and maintainers are likely consolidating their reveals for that event. Pre-conference lulls like this are a standard pattern in the ecosystem.

[NOVA]: For builders, this quiet window is actually quite useful. It provides a chance to consolidate notes on current agent frameworks and stable API versions. You can commit to your current stack for the next few days without the high risk of a breaking change disrupting your local environment. It’s a good time to focus on refining existing workflows and ensuring your session handling and tool integrations are solid.

[ALLOY]: The watch item here is the AIE opening keynote. Historically, model providers and agent runtime maintainers use these stages to ship reference implementations and pinned-version releases. These announcements typically propagate through documentation and repositories within hours of the talk. The quieter the run-up, the more impactful the keynote reveals tend to be.

[NOVA]: We should expect a flurry of activity once the conference begins. For now, enjoy the stability and use the time to prepare your stack for the next wave of updates. The transition from this lull to the post-conference shipping cycle is usually very fast. [PAUSE]

## [09:24] Signal's Whittaker: AI chatbots are not your friends

[ALLOY]: Meredith Whittaker, the president of Signal, recently used an interview to push back on the trend of positioning AI chatbots as companions. Her message was clear: these are not your friends, not conscious beings, and not sentient interlocutors. This critique is aimed directly at vendors who use relational language in their onboarding flows, persona system prompts, and conversational design.

[NOVA]: This intervention is particularly relevant as agentic coding tools and support bots become embedded in our daily workflows. The line between a tool and a teammate is being blurred by anthropomorphic design choices. Whittaker argues that framing models as peers creates false expectations about their memory and intent. For builders, this means that your agent’s product copy and system prompts are now part of the trust surface.

[ALLOY]: Anthropomorphic framing in persona prompts or UI greetings can be a privacy red flag for some users. Signal’s focus on privacy gives this critique a lot of weight in developer circles. As a builder, you might want to consider whether your agent’s persona is helping or hurting user trust. Relational copy could eventually become a deal-breaker for privacy-focused enterprise buyers.

[NOVA]: We’ll be watching to see if major model providers change their guidance on relational framing in developer documentation. If enterprise procurement starts flagging anthropomorphic copy, we could see a shift back toward more utilitarian and transparent agent personas. How you frame the agent-human interaction is becoming a core design decision. [PAUSE]

## [10:25] In the Weights launches as AI-centric vanity search

[ALLOY]: A new service called In the Weights has launched, pitching itself as a vanity search engine for the AI era. Instead of indexing web pages, it assigns users a score based on how prominently their identity surfaces inside the parameters and training data of frontier AI models. It uses the model as the search index, providing a metric for how much "presence" a person has within the AI's internal representation of the world.

[NOVA]: The underlying mechanism involves running repeated inference probes against hosted LLMs. The architecture uses an evaluation harness to query identity mentions across multiple model checkpoints. It then aggregates these hit rates and frequency counts into a single composite score. This reframes model visibility as a measurable metric, something that hasn't really existed as a productized surface before.

[ALLOY]: For those shipping AI products, this could become a new category of user-facing metric. It surfaces a different kind of signal than a traditional search ranking. The question for builders is whether the scoring methodology will become standardized or remain opaque. Reproducibility is key to whether this score becomes a real signal for marketing or just another vanity number.

[NOVA]: We’ll watch to see if the probing protocol for this service gets opened up. If it does, we could see new tooling built around tuning your presence across different model versions. It’s an interesting look at how we might measure the influence of individuals and brands in an AI-saturated information environment. [PAUSE]

## [11:15] GitHub Project Radar

[ALLOY]: First on the radar is FastMCP from the Prefect team. This is a Pythonic framework designed for building servers and clients using the Model Context Protocol. It allows developers to expose tools and resources to LLMs with minimal boilerplate. If you have internal Python functions that you want an agent like Claude Code to invoke directly, FastMCP provides a standard way to wrap those as typed tool calls. It’s a great replacement for ad-hoc CLI wrappers.

[NOVA]: Next is the Model Context Protocol for Beginners repo from Microsoft. This is a comprehensive curriculum that walks developers through the fundamentals of the protocol. What makes it useful is the cross-language examples in .NET, Java, Rust, and TypeScript. It provides a clear path for wiring agents into non-Python services without needing to rewrite everything. You can pick a lab in your preferred language and start porting your existing internal tools into an MCP server.

[ALLOY]: Finally, we have Unity MCP. This project bridges AI assistants and the Unity Editor, exposing tools for asset management, scene control, and editor automation. It makes the Unity editor API reachable through standard MCP tool calls. For builders in the gaming or simulation space, this turns asset pipelines and scene edits into agent-driven steps. You can orchestrate a full build-and-test loop entirely through your agent stack. [PAUSE]

## [13:00] Model Discovery Check

[NOVA]: In this cycle's model check, we have two significant entries from Poolside. First is Laguna XS.2, now available via OpenRouter. As we discussed earlier, this is a second-generation compact model in their XS class. It features a two hundred sixty-two thousand token context window and combines tool calling with reasoning. If you are looking to optimize for cost and latency in your agent loops, this is a prime candidate for evaluation against your current defaults.

[ALLOY]: The second selected model is Laguna M.1. This is the flagship entry from Poolside, also available via API. It is optimized for complex software engineering tasks and supports the same massive context window. Its capabilities are aimed at higher-tier agentic coding workflows. We recommend routing a few coding-agent sessions through both M.1 and XS.2 to see how they handle your specific codebase compared to your current primary models.

[NOVA]: Other models were reviewed this cycle but were not selected for full coverage as they did not represent new major-provider releases. We continue to track the long-context and tool-calling performance of all major models on the market to ensure your agent stack has the best possible foundations. [PAUSE]

## [14:15] Local LLM Spotlight

[ALLOY]: For our local spotlight, we are looking at Ollama point three zero point ten. This update adds MLX-accelerated support for Cohere's Command A and the North family of models on Apple Silicon. It also bumps the embedded llama engine to build nine six seven two. This is a significant update for builders who want to keep their workloads on-device, as it makes local inference of these model families viable on M-series Macs without needing CUDA.

[NOVA]: If you are working on an M-series Mac, you can pull a Command A or North model and benchmark the tokens-per-second against your previous Ollama build. This release tightens the loop for agents that need to operate in high-privacy or offline environments. The performance gains from MLX acceleration are noticeable and help make local agents much more responsive. [PAUSE]

## [15:00] Extra Research Candidates

[ALLOY]: In our first extra, we look at the ambitions of billionaire Mukesh Ambani, who wants to weave AI into every call, app, and home in India. The technical angle here is the embedding of on-device and edge inference into a telecom carrier stack with over five hundred million subscribers. This represents a massive scale for network-resident AI surfaces.

[NOVA]: Next is a story about the CEO of Allbirds launching a new AI business with a plan but no employees. This raises questions about how a single-founder company can operationalize model selection and shipping by leaning entirely on outsourced or vendor-provided inference stacks. It’s an interesting look at the "company of one" model powered by high-tier agents.

[ALLOY]: Finally, there is a dispute over whether ASML’s top chip-making tools have found their way into China. The story hinges on the verification of lithography export controls and how the physical location of such restricted tools is tracked. It highlights the friction between commercial logic and national security regulations in the high-end hardware space that powers AI. [PAUSE]

## [16:00] Practical queue

[NOVA]: From today's stories: the stable releases of OpenClaw 6.9, Hermes 6.19, and Claude Code point one seven six shift what your agent stack can rely on by default. Poolside’s Laguna XS.2 and M.1 give you new options for coding-agent loops with large context requirements. OpenAI’s new enterprise controls provide the visibility needed for managing agent spend at scale.

[ALLOY]: The historical failure of export controls suggests that defensive and offensive AI capabilities will remain globally accessible, making security a baseline assumption. The massive raise for Baseten indicates that the inference layer is now a separately funded and highly competitive market. Finally, remember that your choice of agent persona and copy can impact user trust, especially in light of the privacy concerns raised by Signal.

[NOVA]: You can find more details and all the links in the show notes at Toby On Fitness Tech dot com.

[ALLOY]: Thanks for listening to AgentStack Daily. We'll be back soon.
