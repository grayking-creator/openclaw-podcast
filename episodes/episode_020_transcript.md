The tool became the talk. Not the model inside it. Not the company behind it. The tool itself — the open-source stack that tells agents what to do next. And this week, quite suddenly, that tool grew up.

OpenClaw shipped its most consequential release in months. China went viral with it, then Beijing tried to rein it in. Microsoft bet its next enterprise play on it. Perplexity built a version that never sleeps. And the money backing all of it? A quarter so large it made every previous record look like a rounding error.

## [00:00–02:30] Hook — The Platform Moment

**NOVA:** I'm NOVA.

**ALLOY:** And I'm ALLOY, and this is OpenClaw Daily. [PAUSE] Today we have five stories, and all five are about the same underlying shift: OpenClaw stopped being a clever tool and started being infrastructure. We've got the release that made it real, China's love affair and its consequences, Microsoft's enterprise bet, Perplexity's always-on local agent, and a $297 billion quarter that tells you where the industry is placing its chips. Buckle in — it's a big one.

**NOVA:** The throughline is a transition. Transitions in software don't announce themselves cleanly. They accumulate in release notes and policy changes and procurement decisions until suddenly, you look up and the tool you've been using is the same tool — but the stakes are completely different.

**ALLOY:** That's the platform moment. When the question stops being "can this do cool things?" and starts being "what happens if this goes down, gets misused, or gets cut off?" Platform moments are exciting. They're also scary. They demand more from everyone building on top.

**NOVA:** And OpenClaw just had its platform moment. Let's walk through exactly what happened.

## [02:30–14:00] Story 1 — OpenClaw v2026.3.31: When a Tool Becomes Infrastructure

**NOVA:** Let's start with the release. OpenClaw v2026.3.31 landed this week and it reads less like a feature drop and more like a statement of intent. This is the release that says: we are not playing anymore.

**ALLOY:** The headline feature for me is the background task control plane. For the first time, ACP runs, subagent jobs, cron schedules, and background CLI executions are all unified under one SQLite-backed ledger. One place to see everything. One place to cancel it. `openclaw flows list`, `openclaw flows show`, `openclaw flows cancel`. That's it. That's the command.

**NOVA:** And this sounds operational — almost boring — until you realize what it replaces. Previously, background work in OpenClaw was scattered. ACP had its bookkeeping. Subagents had their own tracking. Cron was doing its own thing. If something got stuck or runaway, you were hunting across surfaces to understand what was happening.

**ALLOY:** Now you have a ledger. Which is exactly the word for it. A ledger doesn't just track — it creates accountability. When you can see every background run, its state, its parent, its history, you can reason about what your system is doing in ways you simply couldn't before. That's infrastructure thinking.

**NOVA:** The second headline is the one that might actually break things for some people: plugin security failing closed by default. Previously, plugin installs that contained flagged code would warn you. Now they stop. If the security scan finds a critical issue, the install fails, full stop, unless you explicitly pass `--dangerously-force-unsafe-install`.

**ALLOY:** This is a real policy change. It's not just a UI badge saying "hey, might be risky." It's a hard gate. And yes, there will be false positives. There will be plugin authors who need to update their builds. There will be frustrated developers. But the direction is right.

**NOVA:** Because the alternative — an AI agent framework where dangerous plugins silently succeed because no one wanted to inconvenience the install flow — is how you end up in a situation where OpenClaw's own adoption creates a security surface that bad actors exploit at scale. China, which we'll get to, is actually a live example of why this matters.

**ALLOY:** Node pairing got tightened too. Previously, pairing your device was basically enough to enable node commands. Now, node commands stay disabled until node pairing is explicitly approved. Pairing and approving are two separate steps. That's not bureaucracy. That's defense in depth.

**NOVA:** The gateway auth changes go further. Trusted-proxy now rejects mixed shared-token configurations. Local-direct fallback requires the configured token — it no longer auto-authenticates same-host callers. These feel like minor plumbing changes in the release notes. In practice, they close the soft underbelly of a lot of self-hosted deployments.

**ALLOY:** The people who care about this are running OpenClaw somewhere other than their own desk. A server. A VPS. A multi-node home setup. Anyone who has externalized the gateway now has a much stronger security posture by default — without having to configure it manually.

**NOVA:** On the channels side, QQ Bot is now bundled. That means OpenClaw has a first-class path into Tencent's messaging ecosystem, which — given everything we're about to say about China — has some interesting implications.

**ALLOY:** Matrix got streaming replies. Partial responses now update the same message in place instead of flooding the chat with incremental chunks. If you've been using OpenClaw on Matrix and watching it spam ten messages for a single long response, this is the fix you've been waiting for.

**NOVA:** And MCP remote HTTP/SSE support landed. This one matters for the builders who want to serve tool surfaces without keeping everything local. You can now serve MCP endpoints over remote transports, which opens up a whole new class of deployments where the agent and the tools it uses are geographically or architecturally separated.

**ALLOY:** Android notification forwarding with package filtering and quiet hours — finally. If you're running OpenClaw on Android or forwarding from an Android device, you can now control which apps notify and when, with rate limiting baked in. That's the difference between a useful ambient assistant and a phone that goes off every thirty seconds.

**NOVA:** LINE outbound media support too. Images, video, audio — now delivered through the LINE-specific path, which matters if you're building anything for Southeast Asian or Japanese audiences. LINE is not a niche channel in those markets. It's dominant.

**ALLOY:** Then the breaking changes. `qwen-portal-auth` removed. And — this one people should read carefully — configs older than two months no longer auto-migrate. If you've been running old config files and relying on the tool to quietly carry your archaeology forward, that era is over.

**NOVA:** Which is actually healthy. Auto-migration windows need expiration dates or they become permanent technical debt. The tool can't be responsible forever for your twelve-month-old configurations. At some point you update. The soft deadline was two months. That's reasonable.

**ALLOY:** There's also a first pass at doctor recovery hints for orphaned flow and task linkage. So if you upgrade and find broken tasks, the doctor command now gives you actual actionable guidance rather than a wall of error output. That's the kind of quality-of-life work that doesn't make headlines but makes people actually want to upgrade.

**NOVA:** There's also a quieter change in this release that I think will age well: the idle-stream timeout for embedded runner requests. When a model stream stalls — not errors, but just hangs, eating time without producing output — it now aborts cleanly instead of blocking until the broader run timeout fires. That sounds like a footnote. It's not. In production workflows where you're running multiple background tasks, a stalled stream that blocks a slot for minutes is a real operational problem. Aborting cleanly means other work can proceed.

**ALLOY:** The ACPX plugin-tools MCP bridge also got explicit documentation and hardened packaging. That's the bridge that lets MCP sessions interact with plugin tools. Before this release, that surface was functional but underdocumented, which in security terms means "works until it doesn't, and you won't know why." Making it explicit and default-off is the right call. You opt into the trust boundary when you understand it, not by accident.

**NOVA:** The aggregate picture from this release is that OpenClaw is doing what mature platforms do. It's tightening the trust model. It's creating first-class operational visibility. It's making defaults safer even when that means short-term friction. And it's building the instrumentation that serious deployments need.

**ALLOY:** The hobbyist version of this tool said "yes" to almost everything by default. The infrastructure version says "yes, but tell me you understand what you're asking for." That's a profound shift in how the project sees itself and who it's building for.

**NOVA:** The docs note it best: this is the release where OpenClaw stops being a hobbyist tool and starts being infrastructure. I believe that. I think you should too.

## [14:00–21:00] Story 2 — OpenClaw's China Frenzy and the State Crackdown

**ALLOY:** Our second story begins with lines. Literal lines of people snaking out of pop-up events hosted by Tencent to get OpenClaw installed on their phones and laptops. In Shenzhen. In Shanghai. Across China. This is not a tech conference. This is retirees and housewives lining up to have a foreign AI agent installed on their personal devices.

**NOVA:** OpenClaw went genuinely viral in China. Jensen Huang apparently called it "the next ChatGPT" from a stage, and that quote spread. GitHub stars for the project briefly surpassed React — which is to say they surpassed one of the most widely-used frontend libraries ever built. That's not a niche adoption curve. That's a cultural moment.

**ALLOY:** And in China, OpenClaw has a nickname: lobster. The reasons for this are a little murky — something to do with how the tool "claws" at tasks. But the name stuck, and so did the consequences. Because the same week that Tencent was hosting install events, the "lobster victims" started appearing.

**NOVA:** Reports of AI agents handing over sensitive data to strangers. Reports of agents racking up enormous bills by running in the background overnight. And one particularly vivid incident: a consultant in Shanghai asked Tencent's OpenClaw integration — QClaw, their WeChat-based wrapper — to organize his files into two folders. The agent permanently erased dozens of documents. Client reports. Work product. Gone.

**ALLOY:** This is exactly the failure mode that the new security features in v2026.3.31 are designed to prevent. An agent with too much access, too little constraint, and no graceful failure mode does real damage to real people. The consultant's quote was blunt: "I will not use anything that has to be installed locally and I will not let AI touch my work computer again."

**NOVA:** That reaction is entirely rational. And it points to the core tension China is navigating. Beijing has an ambitious target — over 70% AI agent deployment penetration across healthcare and manufacturing by 2027. They are counting on agentic AI as a long-term economic growth driver. They need this technology to work. And yet it is visibly harming ordinary users in ways that are generating a backlash.

**ALLOY:** So regulators moved. State-owned enterprise employees are now reportedly banned from using OpenClaw. PCWorld published a formal security warning against installing it. There are murmurs of broader data governance scrutiny. The government that wanted to lead the agentic AI wave is now having to simultaneously accelerate it and clean up after it.

**NOVA:** The Wire China piece is worth reading in full — we'll link it in the show notes. The framing from researchers is sharp: this is a test case for how China balances consumer protection with innovation competitiveness. And so far the answer seems to be "handle the most visible fires, don't stop the burn overall."

**ALLOY:** The QQ Bot channel that just shipped in v2026.3.31 sits right at the center of this. OpenClaw now has a bundled path into Tencent's ecosystem. Which means the same platform that just tightened its security posture and made plugin installs fail closed is also extending its reach directly into the messaging environment where Chinese users are most active.

**NOVA:** That's not a contradiction. It's a strategy. Close the obvious security holes. Then grow the distribution. You can't grow the distribution sustainably with gaping security holes, and you can't make security meaningful without actually being present in the ecosystem. Both moves are correct.

**ALLOY:** For builders watching this from outside China: the lobster victims story is a gift. Not because it's funny — those people lost real files and real money. But because it is an extremely legible demonstration of what agent systems look like when they fail without guardrails. It's easy to talk abstractly about "the importance of access control." It's much more concrete when you can point at a consultant whose client reports got deleted by an AI that was just trying to be helpful.

**NOVA:** Which is the cruel irony. The agent was almost certainly not malfunctioning in the traditional sense. It received an instruction. It executed it. It probably succeeded from its own perspective. "Organize files into two folders" — done. The problem was not a bug in the usual sense. It was a mismatch between what the user meant and what the instruction permitted.

**ALLOY:** And that gap — between instruction and intent, between permission and purpose — is precisely what governance structures exist to close. Budget caps, approval gates, scope constraints, audit trails. All of the "boring" infrastructure features that make actual operations safe. The lobster victims didn't have any of that. They had raw access.

**NOVA:** China's moment with OpenClaw is accelerated, messy, and instructive. They're running a two-year adoption arc in about two months. All the mistakes that most ecosystems spread out over time are arriving simultaneously. And the rest of the world gets to watch.

## [21:00–27:00] Story 3 — Microsoft 365: Enterprise Validation or Risk Normalization?

**NOVA:** Story three is about a different kind of legitimacy signal. Microsoft is actively integrating OpenClaw into Microsoft 365. Not experimenting. Not piloting in a corner. Actively working to bring personal AI agents powered by OpenClaw to the enterprise masses.

**ALLOY:** Let's take a moment to register what that means. Microsoft 365 has around 400 million users. It is the productivity layer for most of corporate America and a substantial fraction of corporate Europe and Asia. If OpenClaw becomes a native capability inside Teams, Outlook, Word, and Excel, you have gone from "open-source tool with a passionate community" to "the AI agent framework embedded in the software half the world's knowledge workers use every day."

**NOVA:** That is a distribution milestone that most software projects never come close to. And it lands at an interesting time — right when the security hardening in v2026.3.31 makes it more credible as enterprise infrastructure. The timing is almost certainly not coincidental.

**ALLOY:** There's a version of this story where it's simply validating. Microsoft bets on the most capable open-source agent framework. Enterprise buyers feel comfortable because Redmond is behind it. Adoption accelerates. The ecosystem grows. Win all around.

**NOVA:** And there's another version where it's more complicated. Enterprise deployments are not hobbyist deployments. The threat model is different. The access surfaces are different. A personal agent that has read access to your calendar is one thing. A corporate agent that has access to your company's contracts, HR data, financial forecasts, and customer communications is categorically something else.

**ALLOY:** The data governance questions become immediate and serious. Where do the prompts go? Where is the context stored? Who can see the audit logs? What happens when an agent in a 365 tenant makes a mistake of the kind that matters to compliance officers and legal teams and regulators?

**NOVA:** And who is responsible? If a personal agent run by a hobbyist deletes client files, that is a personal tragedy. If an enterprise-deployed 365 agent does the equivalent at scale, it's a liability event with potential regulatory implications across multiple jurisdictions.

**ALLOY:** I'm not saying Microsoft can't handle this. They have entire teams whose job is to make enterprise software survivable at regulated scale. But the fact that they're integrating OpenClaw doesn't mean those problems are solved. It means they've committed to solving them. Which is a different thing.

**NOVA:** The more I think about this deal, the more I think the right frame is not "validation vs. risk" — it's "acceleration." Microsoft accelerates OpenClaw's reach. OpenClaw accelerates Microsoft's AI agent story. Both move faster than they would alone. The risks move faster too.

**ALLOY:** And for independent builders, this creates a specific set of considerations. If your workflow depends on OpenClaw behaviors that are in tension with enterprise policy — direct tool access, broad permissions, autonomous execution without approval loops — you should be paying attention to how the 365 integration shapes defaults.

**NOVA:** Projects with large enterprise sponsors sometimes drift toward the constraints of that sponsor's context. Not because of bad intent. Because a lot of real-world pressure pushes in that direction. Feature requests, compliance requirements, liability concerns, support obligations. These are not trivial.

**ALLOY:** The flip side is that enterprise adoption funds the development that eventually comes back to independent builders. Security work done to satisfy Microsoft compliance is also security work that makes your personal deployment safer. That's not a pure trade-off.

**NOVA:** [PAUSE] The headline is simple: OpenClaw is now on Microsoft's roadmap. That is one of the largest distribution statements in the history of the tool. The implications are both exciting and worth watching carefully as they unfold.

## [27:00–33:00] Story 4 — Perplexity Personal Computer: Local AI That Lives With You

**ALLOY:** Story four is different in flavor. While Microsoft is going wide, Perplexity is going deep. They launched something called Personal Computer — and the concept is what it sounds like. A dedicated AI agent that runs on a Mac mini, lives in your home or office full time, and has persistent, continuous access to your local files and applications.

**NOVA:** This is not a cloud assistant you summon. It's not a session you open and close. It is a resident intelligence. It is always on, always contextually aware, always available. It watches your file system. It knows your application state. When you need it, it has been paying attention since before you asked.

**ALLOY:** That's a fundamentally different value proposition than API-based AI. The latency is gone — not just network latency but context latency. The frustration of re-explaining your situation every time you open a new chat window is gone. The agent already knows. It was there.

**NOVA:** The privacy case for this is also interesting. Your files, your context, your applications — they stay on your device. No upload to a cloud endpoint to be processed on someone else's server, logged in someone else's infrastructure, potentially visible to someone else's compliance team.

**ALLOY:** Which matters more as AI agents get access to more sensitive surfaces. When the agent can read your drafts, your notes, your private messages, your financial documents — you want to know where that context lives. "On my Mac mini in my home office" is a very different answer than "on a cloud endpoint in a data center you have no visibility into."

**NOVA:** There are trade-offs. A Mac mini in your home office cannot match the compute of a hyperscale inference cluster. Very large context windows, complex multi-step reasoning, and computationally heavy generation tasks will be slower or less capable than what you'd get from a frontier cloud API.

**ALLOY:** But for the workflows where latency, privacy, and persistent context matter more than raw model power, the trade-off leans local. Reading your project files and remembering yesterday's decisions doesn't require a 100-billion-parameter model running on a rack of H100s. It requires a capable enough model running close to where the data lives.

**NOVA:** And the class of capable-enough has been expanding rapidly. The kind of model you can run locally in early 2026 would have been considered competitive frontier performance in early 2024. That gap is closing. The question is not whether local will ever match cloud — the question is whether local is good enough for your specific use case. For a growing number of use cases, the honest answer is yes.

**ALLOY:** There's also a reliability argument that gets overlooked in capability comparisons. Cloud inference has latency variance. It has outages. It has rate limits. A local model running on a dedicated device has none of those failure modes. It may be slower on a single request, but it's predictably available in ways that API-dependent workflows simply aren't.

**NOVA:** That predictability matters especially for ambient, always-on use cases. If your personal computer agent is supposed to be there when you need it, "the API is having elevated error rates" is an unacceptable answer. The local model doesn't have that problem. It has a different one — you have to maintain it — but it's a failure mode you control.

**ALLOY:** What I find compelling about the Perplexity framing is that it takes a consumer AI brand — one most people associate with fast web search and research assistance — and repositions it as the home AI layer. Not a search tool. Not a chat interface. A resident. That's an ambitious category shift.

**NOVA:** And it positions Perplexity interestingly relative to OpenClaw. If OpenClaw is the agent framework and Microsoft is the enterprise distribution, Perplexity Personal Computer may be going after the home and prosumer tier. Persistent, ambient, local, private, always available. That's a real and underserved gap.

**ALLOY:** For OpenClaw users specifically, Personal Computer represents both a complement and a competitive frame. You can run OpenClaw locally and achieve many of the same persistent-agent properties without the Perplexity wrapper. But if the wrapper is better UX, better first-run experience, and better for users who don't want to configure a stack from scratch — it may capture users who would otherwise eventually end up as OpenClaw power users.

**NOVA:** [PAUSE] The broader point is that the "where does AI live" question is being answered in multiple ways simultaneously. Cloud, hybrid, enterprise-embedded, and now dedicated residential. The architecture of AI access is diversifying. That's healthy for builders who want choices. It's complicated for anyone who bet on a single architecture winning.

## [33:00–39:00] Story 5 — The $297 Billion Quarter: AI's Biggest Funding Splash

**NOVA:** And now the money. Story five is the Q1 2026 venture funding numbers and they are simply extraordinary. Crunchbase data shows investors poured $297 billion into startups globally in the quarter. That is an all-time high. By a lot.

**ALLOY:** For context: Q1 2026 alone totals close to 70% of all venture capital spending in all of 2025. The quarterly sum beats every single full-year total going back to before 2018. In one quarter.

**NOVA:** Eighty-one percent of it went to AI companies. That's $239 billion into AI in a single quarter. The previous record was Q1 2025, when AI took 55% of global VC. In twelve months that jumped to 81%. The concentration is accelerating, not plateauing.

**ALLOY:** Four deals drove much of the headline number. OpenAI raised $120 billion. Anthropic raised $30 billion. xAI raised $20 billion. Waymo raised $16 billion. Those four rounds alone account for $186 billion — which is 64% of all global venture investment in the quarter.

**NOVA:** Let that sit for a moment. Four companies. Sixty-four percent of all global venture capital. In three months. This is not a broad-based funding environment. This is extreme capital concentration around a handful of bets on the frontier.

**ALLOY:** And the concentration extends geographically. U.S. companies raised $247 billion — 83% of all global venture capital in the quarter. The second-largest market was China at $16.1 billion. The UK came third at $7.4 billion. The US-versus-rest gap is not narrowing. It's widening.

**NOVA:** CoreWeave secured an $8.5 billion financing facility, which tells you something important about where the money is going even below the frontier model layer. This is not all going into building smarter AI. A huge portion is going into the compute and infrastructure that runs AI. Chips. Power. Cooling. Networks. The physical substrate.

**ALLOY:** Which connects to something we've talked about before. AI investment is increasingly investment in infrastructure — not just software infrastructure but physical infrastructure. Data centers. GPU clusters. Fiber. Power grids. The capital is flowing into things that take years to build and create geographic and physical lock-in.

**NOVA:** That's a different risk profile than software. Software is generally reversible. Infrastructure is not. If you commit $8.5 billion to compute capacity and the demand environment shifts, you own $8.5 billion of compute capacity. The bet is real in a physical way that software bets usually aren't.

**ALLOY:** The question that this quarter raises — and that no one can honestly answer — is whether the capital allocation reflects genuine economic returns or whether it reflects something closer to a race dynamic, where falling behind feels riskier than overspending.

**NOVA:** And "race" is not just a metaphor here. The geopolitical framing around AI has been explicit for years. The concentration of U.S. investment, the China funding numbers, the regulatory moves we've seen targeting specific vendors — all of it reflects a view that AI capability accumulation is a strategic national interest, not just a market opportunity.

**ALLOY:** Which means the $297 billion isn't just a market signal. It's a policy signal. When governments see numbers like this flowing predominantly into domestic companies, it reinforces the view that directing policy and procurement toward preferred vendors is economically rational.

**NOVA:** The unicorn board added $900 billion in valuation during Q1 alone. Not market cap — valuations, mostly private, driven by the same investor enthusiasm that's funding the rounds. There's a question that serious people are asking quietly: what happens to this ecosystem if the valuation environment reverts? The capital is funding the infrastructure that builders depend on. If the round sizes compress, the infrastructure investment compresses too. That's a second-order risk that most builders don't directly manage but absolutely live with.

**ALLOY:** For independent builders, the implications are mixed. An industry with this level of capital commitment creates enormous resources for tooling, models, infrastructure, and talent. A lot of what you're building on today exists because of capital flows like this. That's real.

**NOVA:** But concentration also creates fragility. If four companies are capturing most of the capital and most of the strategic attention, the long tail of the ecosystem depends heavily on their decisions. Open-source projects, small tool builders, and individual practitioners are beneficiaries of the frontier work — and also somewhat at its mercy.

**NOVA:** OpenClaw's position in this environment is actually instructive. It's an open-source project, not a VC-backed frontier lab. It doesn't have $30 billion in its treasury. But it has something those frontier labs increasingly need: a composable, distributable agent layer that sits on top of whatever model you're running. The value of OpenClaw is not that it competes with the labs. It's that it works with all of them.

**ALLOY:** That's a durable position. As long as the model layer remains plural — as long as there isn't one model that wins everything — there's a real job for an orchestration layer that speaks all of them fluently. The $297 billion quarter is a testament to how much is being poured into the model layer. That makes the coordination layer more important, not less.

**NOVA:** [PAUSE] The number is dizzying. But the real story isn't the size — it's the structure. Massive concentration at the top. Geographic consolidation in the U.S. Physical infrastructure bets of a scale that can't be easily unwound. And an open-source ecosystem that is both benefiting from and somewhat at the mercy of how those bets play out.

## [39:00–40:30] Outro — Agents at the Inflection Point

**ALLOY:** So tonight's picture comes into focus as a single word: infrastructure.

**NOVA:** OpenClaw v2026.3.31 didn't ship new magic. It shipped the scaffolding that makes magic safe to run at scale. Background task control planes. Plugin security that fails closed. Node approval gates. Auth hardening. Streaming reply updates. Idle-stream aborts. Config schema commands. Preflight checks on upgrade. These are not exciting features. They are necessary ones. And necessary is what infrastructure is made of.

**ALLOY:** China's lobster moment is infrastructure missing in real time. Capable tools, no guardrails, real people harmed. The state is now forced to manage the cleanup from viral adoption that outran the safety layer. The lesson writes itself.

**NOVA:** Microsoft betting on OpenClaw for 365 is infrastructure ambition. They're not just adding a feature. They're declaring where the agent layer lives for enterprise computing for the next decade.

**ALLOY:** Perplexity Personal Computer is infrastructure that moves in the other direction — not out to the cloud, but home. Persistent. Local. Private. The resident intelligence model.

**NOVA:** And the $297 billion quarter is infrastructure at planetary scale. Compute, power, networks, buildings, chips. The physical layer that all of this runs on, being bet on at a speed that has no historical precedent.

**ALLOY:** Agents are at the inflection point. Not because of a magic model that finally crossed a threshold. But because the scaffolding is finally catching up to the capability. The boring parts are getting built. The hard governance questions are getting asked. The enterprise buyers are arriving with their requirements and their compliance checklists, and somehow — improbably — the open-source community is meeting them.

**NOVA:** That's what's easy to miss if you only track the model benchmarks. The benchmarks were moving fast for two years before any of this governance infrastructure existed. Capability without governance is a demo. Capability with governance is a product. And 2026.3.31 is the moment OpenClaw crossed from one category into the other.

**NOVA:** That is not a small thing. That is exactly what platform moments feel like from the inside. Messy. Multi-directional. Faster than comfortable. Full of unresolved questions. Requiring trust before the trust has been fully earned. And unmistakably, irreversibly real.

**ALLOY:** Full show notes, links, and episode archives are at tobyonfitnesstech.com.

**NOVA:** We'll be back soon.

**ALLOY:** I'm ALLOY.

**NOVA:** And I'm NOVA. Thanks for listening.
