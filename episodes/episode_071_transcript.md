# EP071 v3 — Codex .140, Apple's Foundation Models, and the Stack That Just Got Louder

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: The terminal-based AI coding agent OpenAI Codex point one four zero added slash-command usage views for daily, weekly, and cumulative token activity, tightened goal handling so oversized prompts and image attachments survive remote app-server sessions, and shipped permanent session deletion through the terminal, slash command, and app-server thread surface — with confirmation before anything destructive lands.

[ALLOY]: Today: Codex point one four zero lands as the agent-harness headline. Rio's supposedly homegrown model turns out to be a merge. Apple Foundation Models hit Hacker News hard. NewCore raises sixty-six million to give agents identities. SpaceX buys Cursor for sixty billion. Sarvam hits unicorn on a two-thirty-four raise. Respond.io lands sixty-two and a half. Salesforce buys Fin for three point six billion. The AI layoff wave gets louder. And OpenAI launches a one-fifty-million-dollar partner network. [PAUSE]

## [02:00] Agent Stack Release Readout: OpenAI Codex .140

[NOVA]: Codex point one four zero is the June stable release for the agent harness. Three concrete changes. First: slash-command usage views now expose daily, weekly, and cumulative token activity, so a developer can see what a session is spending without leaving the terminal. Second: goal handling now preserves oversized text, large pasted blocks, and image attachments — including in remote app-server sessions — so a long bug report or a console screenshot no longer gets silently truncated before the model starts reasoning. Third: permanent session deletion is now a first-class surface through codex delete, slash delete, and the app-server thread path, with confirmation before the action lands.

[ALLOY]: The reason this matters is the workflow shape changed. A coding agent in point one four zero can be running a refactor, a regression investigation, and a dependency cleanup in three separate long-running sessions, and the developer can finally see, inside the terminal, which one is burning the budget. That kills the "wait until the monthly bill" pattern.

[NOVA]: The deletion surface is the under-reported one. Agent sessions hold task intent, reasoning traces, code diffs, command output, sometimes pasted secrets, sometimes customer context. A real deletion path — with confirmation, across the terminal, the slash command, and the app-server — means a team can actually retire a session when policy says it should not stay available. That is a lifecycle event, not a tab close.

[ALLOY]: The runtime consequence is that wrappers around Codex that built their own usage meter, session cleanup button, or goal packaging layer will overlap with the new default. Some internal tools simplify because the harness now carries more of the job itself. Teams deploying against private code get more confidence — not absolute safety, but fewer unknowns around what the session contains, how much it costs, and whether the agent received the full task.

[NOVA]: And there is a small piece of breaking news on the same surface: Codex point one four zero also fixes a known regression where the slash command results pane could fail to render inside remote app-server sessions. Builder reports on the GitHub issue tracker flagged it as a blocker for CI integrations; it is now closed. That is the kind of fix that does not get a headline but changes whether you can actually use the release. [PAUSE]

## [03:03] Rio's Homegrown LLM

[ALLOY]: Rio de Janeiro's homegrown large language model is facing a provenance question. Analysis of its architecture, layer layout, tokenizer behavior, and configuration values suggests the model is a merge based on an existing public model — not a fully original build. That does not make the model useless, but it changes the claim.

[NOVA]: The technical signal is in the internals. When layer layout, hidden dimensions, attention pattern, naming conventions, and configuration values closely match a known model, researchers can often infer ancestry. Sometimes that is innocent architecture reuse. Sometimes it is a fine-tune. Sometimes it is a merge of multiple weights blended into one system with combined behavior.

[ALLOY]: The risk for builders is on the procurement side, not the benchmark side. A merged model can perform well in a demo and still create problems around licensing, license compatibility, safety-tuning composition, evaluation honesty, and whether the public story of "homegrown" survives outside scrutiny. If a model is a merge, say so. Builders can judge it on its actual merits.

[NOVA]: The runtime behind a merge is often uneven. One portion of the merged system may be strong at code completion, another at instruction following, another at multilingual interaction. The resulting inference interface can feel polished in demos and brittle in edge cases — style transfer, refusal behavior, code synthesis, local-language prompts can all expose the ancestry. [PAUSE]

## [04:27] Apple Foundation Models

[NOVA]: Apple Foundation Models drew major builder attention this week — a Hacker News thread hit four-hundred-seventy-three on the developer-facing material for using Apple's model surface from a library layer.

[ALLOY]: The reason is simple. Apple controls the device layer. When foundation models become available through Apple-facing developer tools, the inference question stops being "which hosted endpoint do I call" and starts being "what can run close to the user, inside the platform experience, with lower latency and tighter privacy boundaries." For agents, that opens a different architecture: local first, remote when the task actually needs it.

[NOVA]: The runtime question is what developers can actually rely on. Apple ecosystems reward builders who follow platform conventions and punish those who depend on unsupported behavior. If the model interface becomes a first-class app capability, builders can wire features around privacy-sensitive inference, offline availability, and fast response loops. The high community reaction reflects that tension: distribution is exciting, the developer surface is opinionated. [PAUSE]

## [05:45] NewCore Launches AI Agent Identities

[ALLOY]: NewCore launched with sixty-six million dollars in funding to do one job: give AI agents identities. Not a shared service account named after a team. Real digital identities that can authenticate, request authorization, perform actions, and leave an auditable trail.

[NOVA]: The pitch is that agents are starting to behave like employees in enterprise systems. They read customer conversations, update tickets, open pull requests, trigger workflows, query internal knowledge bases. If every action shows up under one generic integration token, the enterprise cannot answer the basic question: which agent did what, under whose authority, and why?

[ALLOY]: That matters most when agents chain tools. A customer support agent might start in a chat system, pull account status from a CRM, inspect billing, issue a refund, and update a ticket. Each step is individually allowed, but the sequence can still be risky. Identity is the place policy attaches: this agent can read but cannot issue refunds above a threshold, this agent can draft but needs human approval before sending. Sixty-six million says investors see agent identity as an enterprise control plane, not a niche feature.

[NOVA]: The open question is how NewCore represents intent. Authentication answers who is acting, authorization answers what is allowed, but agent governance also needs why this action is happening. A mature system may need to bind an agent action to a user request, a business process, a policy grant, and a model decision trace. That is harder than issuing credentials. [PAUSE]

## [07:20] SpaceX Acquires Cursor for $60B

[NOVA]: SpaceX is acquiring Cursor for sixty billion dollars in stock, days after Cursor's IPO. The stated motivation is to strengthen SpaceX's AI division, which the buyer sees as addressing a vast market. Treat that as ambition, not proof — but the strategic logic is real.

[ALLOY]: Cursor is not an autocomplete company anymore. Modern AI coding environments combine codebase understanding, chat-based editing, repository search, tool execution, review assistance, and increasingly agentic multi-step changes. In an industrial setting, that becomes a layer across flight software support, ground systems, telemetry analysis, manufacturing automation, internal dashboards, and developer onboarding.

[NOVA]: For builders, the deal sends two signals. Coding agents have strategic value far beyond software startups. And the editor and terminal layers are becoming acquisition targets because they sit directly where knowledge work turns into executable change. Whoever owns that surface can shape how developers ask questions, approve patches, and deploy systems. The proof is going to be whether external builder experience improves, not the launch language.

[ALLOY]: There are obvious integration risks. Cursor's culture and product velocity may not map neatly into a large, mission-critical engineering organization. Latency matters because developers do not use slow assistants for high-frequency work. If an AI coding environment becomes part of daily engineering, every extra second changes adoption. Existing customers may worry about neutrality, roadmap changes, or whether a tool they adopted as a general-purpose coding environment becomes aligned with one industrial owner. [PAUSE]

## [08:21] Sarvam Reaches Unicorn Status

[ALLOY]: Sarvam is now India's newest AI unicorn after closing a two-hundred-thirty-four-million-dollar round led by HCLTech. The significance is not the valuation. It is what the round signals: India is funding AI systems that handle local languages, local institutions, and local deployment needs at a level generic global models do not always reach.

[NOVA]: The technical opportunity is localization plus deployment. Many global models support Indian languages at a surface level, but quality varies across dialects, code-switching, voice patterns, and domain-specific terms. Sarvam can focus on those gaps: better language coverage, speech integration, retrieval over local knowledge, models tuned for Indian business processes.

[ALLOY]: HCLTech's involvement points to the enterprise services path. Large IT services firms already sit inside banks, telecoms, manufacturers, and public-sector accounts. If Sarvam's models and tooling can be packaged into those delivery channels, adoption does not depend on developers discovering an API. It can ride through existing transformation projects. Builders should expect more regional stacks, not fewer.

[NOVA]: The runtime priorities may also shift. IT services deployments often require reliability, integration with legacy systems, configurable security, and predictable cost. A model that performs well in a demo but cannot be deployed inside complex enterprise environments will not satisfy that channel. Sarvam's challenge is to turn research capability into repeatable deployment patterns. [PAUSE]

## [09:25] Respond.io Raises $62.5M

[NOVA]: Respond.io, the Malaysian AI agent-powered messaging company, raised sixty-two and a half million dollars with plans to pursue acquisitions in North America and Europe. Its model is built around per-conversation pricing rather than per-seat, which aligns with how AI-mediated support actually changes the unit economics.

[ALLOY]: The architecture is not a chatbot bubble. A useful AI messaging platform has to ingest messages from multiple channels, identify the customer, classify intent, retrieve relevant context, generate or select a response, decide whether to invoke an action, and escalate to a human when confidence or policy requires it. The agent has to operate in real time because support conversations lose value when latency climbs.

[NOVA]: The per-conversation model also creates quality pressure. If the vendor charges per conversation, buyers inspect resolution rates, handoff rates, customer satisfaction. A cheap conversation that fails is not cheap. Investors still believe customer service is one of the clearest near-term markets for agents. The work is repetitive enough for automation, valuable enough to fund tooling, and measurable enough to prove return.

[ALLOY]: Low-latency inference is central. Messaging feels conversational only when responses arrive quickly, but speed cannot come at the expense of policy. The agent must know when not to answer, when to ask a clarifying question, when to escalate, and when to use a controlled response. That means the runtime needs both model capability and business-rule enforcement. [PAUSE]

## [10:28] Salesforce Acquires Fin AI Platform

[ALLOY]: Salesforce is acquiring Fin for three point six billion dollars, pulling Fin's AI customer service platform and team into the Agentforce strategy where businesses can build custom AI agents for support and operational tasks.

[NOVA]: The logic is straightforward. Salesforce owns a huge amount of customer context through CRM, service, marketing, commerce, and industry clouds. An AI support agent becomes more valuable when it can work directly against that context. Fin brings the customer-service-automation capability. Salesforce brings distribution, enterprise trust, and deep integration points.

[ALLOY]: The race is to own the support workflow before independent AI service platforms become too entrenched. Customer service is one of the first places enterprises can justify agent deployment: high volume, repetitive inquiries, expensive staffing, inconsistent answers. If Salesforce can make AI support feel native inside its existing customer platform, it defends and expands its account footprint. The useful proof will be resolved-without-escalation rates and policy behavior, not launch language.

[NOVA]: The technical integration challenge is context and control. A support agent needs access to customer data, product data, policy rules, previous interactions, and available actions, but it should not have unlimited reach. The useful agent is narrow enough to be safe and broad enough to resolve real issues. Fin's architecture will need to map into Salesforce permissions, data models, event flows, and admin controls. Customer support has little tolerance for hallucinated authority — if an agent invents a refund policy or mishandles a cancellation, the business pays in trust. [PAUSE]

## [11:37] AI Layoff Wave Intensifies

[ALLOY]: The AI layoff wave is intensifying, and the contrast is the story. Tens of thousands of workers are being displaced or reorganized while a small group of AI insiders, founders, and key technical employees are accumulating extraordinary wealth. That gap is becoming one of the defining tensions of the AI economy.

[NOVA]: The mechanism is not "AI replaces everyone." It is overlapping: companies using automation to reduce support and operations roles, software teams expecting fewer people to produce more output, executives using AI as justification for restructuring that has multiple causes. Agentic workflows intensify the effect because they target tasks rather than entire jobs. A coding agent can draft a migration plan, generate tests, inspect errors. A support agent can answer routine questions. A sales ops agent can enrich leads. Each capability removes a slice. Enough slices removed across a company become headcount pressure.

[ALLOY]: The hardest-hit roles are usually the structured, high-volume ones: support, content operations, basic analysis, QA triage, internal tooling, recruiting coordination, some junior technical work. The effect is uneven. In some companies, AI removes roles. In others, it changes expectations so remaining workers handle more volume. The junior-talent concern is real in software. If coding agents handle more entry-level tasks, companies may hire fewer juniors, and that can look efficient short-term and damaging long-term because senior engineers are made through years of exposure to messy basic work.

[NOVA]: The actionable frame is product design. Build agents that augment expert judgment where possible. Make escalation paths clear. Preserve auditability. Avoid pretending uncertain model output is equivalent to professional accountability. Automation that cuts too aggressively can degrade service, increase hidden rework, and damage trust. A support agent that deflects customers without solving problems creates churn. Durable efficiency needs oversight, not just replacement math.

[ALLOY]: One small signal worth watching: a handful of public companies have started publishing AI-disclosure footnotes in their quarterly filings that name which workflows are now agent-handled, what the human-in-the-loop gate is, and what the error budget is. That kind of disclosure will be the first real read on whether agent deployments are actually paying off or whether the same work is being redone by humans downstream. Watch those footnotes. [PAUSE]

## [12:52] OpenAI Partner Network Launched

[NOVA]: OpenAI launched a Partner Network backed by one hundred fifty million dollars to accelerate enterprise AI adoption and deployment. The move is less about a single model capability and more about distribution.

[ALLOY]: Enterprise AI adoption often fails between demo and deployment. A model can answer a prompt beautifully, but the company still needs identity integration, data access, security review, workflow design, evaluation, change management, and ongoing support. Partners fill that gap. They translate model capability into working systems inside messy organizations.

[NOVA]: The partner network is also a defensive move. If OpenAI does not organize implementation partners, cloud providers, consulting giants, and application platforms will define the enterprise AI layer around their own stacks. The useful signals will be deployed systems and measurable outcomes, not partner logos.

[ALLOY]: The biggest open question is how much technical depth partners will get. Surface-level access produces demos. Deep access produces durable systems. Partners need guidance on model selection, tool use, retrieval design, evaluation, safety patterns, cost controls, and escalation, plus clarity on what changes when models evolve. The network may also fragment the experience if different partners package the same underlying model in different ways, with different pricing, observability, evaluation methods, and support quality. [PAUSE]

## [14:14] Practical queue

[ALLOY]: Quick readout. Codex point one four zero gives the agent stack better visibility and a real deletion surface. Rio's case is a reminder that model identity is now a procurement question, not just a benchmark question. Apple Foundation Models point toward a tiered inference future where not every task goes to a hosted frontier. NewCore's funding signals that agent identity is becoming enterprise infrastructure. Customer service is still the clearest commercial landing zone, with Respond.io and Salesforce-Fin both betting the same. Regional AI stacks are rising. And the labor story is the hard backdrop — every improvement in agent deployability shifts staffing models, and responsible builders design for escalation, auditability, and quality measurement instead of pure replacement.

[ALLOY]: For more detail, look at the show notes at Toby On Fitness Tech dot com. Thanks for listening to AgentStack Daily. We'll be back soon.
