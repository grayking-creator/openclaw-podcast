[NOVA]: The software shipped before breakfast. Three new AI models at Microsoft. A governance platform treating every agent like a human employee. A federal government that wants to set the rules but can't agree with itself. And one company cutting thousands of jobs to pay for the machines that will do those jobs better. This is what a maturing stack looks like from the inside.

[NOVA]: [NOVA]: I'm NOVA.

[NOVA]: [ALLOY]: And I'm ALLOY. This is OpenClaw Daily. Today we follow the release train — five stories about an AI industry that stopped being experimental and started being infrastructure. OpenClaw's biggest release of the year. Microsoft staking a claim as a foundational model lab. Enterprise identity management coming for AI agents. Oracle trading headcount for GPUs. And a federal government and fifty state legislatures that cannot agree on who gets to set the rules for any of it.

[NOVA]: [NOVA]: And we start with the most concrete piece of evidence for that argument: a software release. OpenClaw v2026.4.1 dropped on April second, and it's the kind of release that marks a before and after. Not because of any single feature, but because of what the feature list says collectively about where the project thinks it's going.

[NOVA]: [ALLOY]: Before we get into the features — a bit of context for anyone who's newer to the show. OpenClaw is a personal AI operating system. It runs on your machine. It connects to your messaging apps — Telegram, Discord, Signal, others. It can run scheduled tasks, spawn background sub-agents, and keep persistent memory about your life and work. Think of it less as a chatbot and more as an always-on AI that lives in your infrastructure. And v2026.4.1 is the biggest single release it's had this year.

[NOVA]: [NOVA]: The headline feature is called slash tasks. And to understand why it matters, you have to understand what was missing before it.

[NOVA]: [ALLOY]: So here's the problem that slash tasks solves. OpenClaw has had background work for a while now — subagents, cron jobs, long-running processes that run while you're doing other things. But until this release, if you wanted to know what those agents were doing, you had to go find out. You might know you kicked off a job, but the job was... somewhere. Running. Hopefully.

[NOVA]: [NOVA]: Which is fine when you have one background task. It's not fine when you have five. Or when you come back to your machine after an hour and you're not sure what finished, what failed, and what's still grinding away. And it's definitely not fine when you're trying to use this as genuine daily infrastructure, not just an occasional experiment.

[NOVA]: [ALLOY]: Slash tasks changes that. Type slash tasks in any chat surface and you get a live view of in-progress agent work, surfaced directly in the conversation. Not a separate dashboard. Not a log file. Right there in chat, where the context already lives.

[NOVA]: [NOVA]: This sounds small. It's not small. What it actually means is that the conversation becomes the control plane. Your chat with your agent — whatever you've named it — is no longer just where you give instructions and read results. It's where you monitor ongoing operations. That's a meaningful architectural shift. The agent is no longer a black box you talk to. It's a system you can observe from inside the interface you already use.

[NOVA]: [ALLOY]: And think about what that does to trust. One of the persistent concerns people have about AI agents doing real work is that you don't know what they're doing in the background. You asked for something, they went off to do it, and now you're waiting. Slash tasks collapses that uncertainty. You can check. You can see the queue. You can watch something actually finish. That is a qualitatively different relationship with your agent.

[NOVA]: [NOVA]: The second big feature in v2026.4.1 is bundled SearXNG support for web search. SearXNG is an open-source meta-search engine — it aggregates results from multiple sources across the web, runs entirely on your own infrastructure, and doesn't report your queries to anyone. In this release, OpenClaw ships with built-in support for it as the default web search backend. No external API key. No account. No per-query billing.

[NOVA]: [ALLOY]: This is significant for two reasons. First, it removes a common friction point for new users. Previously, getting decent web search in OpenClaw required setting up a third-party API, managing keys, and accepting that every query was going to some external service. Now you can stand up SearXNG locally and your agent has full web search without any of that.

[NOVA]: [NOVA]: Second, it's a privacy statement. An AI agent that searches the web on your behalf, running on your hardware, querying your own search aggregator — that's a genuinely different relationship with information than "your agent calls out to a commercial API every time it needs to look something up." For anyone running OpenClaw in an environment where query privacy matters — personal health questions, business research, anything sensitive — this is an important option to have natively.

[NOVA]: [ALLOY]: The rest of the release reads like a hardening pass across the whole system. Voice Wake on macOS — you can wake your agent with a keyword on a MacBook or Mac desktop, completely hands-free. Cron tool allowlists — administrators can now specify exactly which tools are available to scheduled tasks, so a cron job that's supposed to pull data can't suddenly start sending emails. A big sweep of reliability fixes across the approval flow, the Telegram integration, the Discord integration, memory indexing, and auth persistence.

[NOVA]: [NOVA]: Let me say a word about why the auth persistence fix matters specifically. If you're running OpenClaw on a server and the auth state resets on restart, you lose your session continuity. Your agent doesn't remember what channels it's connected to, what credentials it's been granted, what's pending. For a personal project, that's annoying. For a small business using it as actual infrastructure, that's a service outage. The fact that this is addressed in this release is one more signal that the project is taking production use cases seriously.

[NOVA]: [ALLOY]: The Telegram and Discord integration reliability fixes are in the same category. Your agent can't be the connective tissue of your digital life if the messaging layer drops messages, fails silently, or gets desynchronized. These fixes don't get written up in press releases. They don't get demo'd on stage. But they're the difference between "runs great in demos" and "I trust it with real work."

[NOVA]: [NOVA]: The approval flow fixes are worth calling out too, because they've been a consistent source of friction. When you have an agent doing background work, and it hits something that needs human sign-off, the approval mechanism has to be reliable. If approvals time out silently, if they don't reach the right channel, if they get duplicated or dropped — the agent can't be trusted for real work. These kinds of fixes aren't glamorous but they're what makes "agent as infrastructure" possible.

[NOVA]: [ALLOY]: If you had to summarize v2026.4.1 in one sentence: OpenClaw is not just an agent that does things. It's becoming an agent OS that shows, routes, and governs ongoing work. The conversational surface is absorbing the monitoring and control plane. That's the arc this release is on.

[NOVA]: [NOVA]: ... And if you want proof that the pace of this development is itself part of the story, here's a data point: the beta for this release and the stable release hit within the same day. That cadence is not accidental. That's a team that has its release infrastructure wired tightly enough that major UX changes can move from beta to production in hours. Which tells you something about the engineering culture and something about the ambition.

[NOVA]: [ALLOY]: For comparison: major enterprise software projects measure release cycles in quarters or years. Even fast-moving open-source projects often have weeks between beta and stable for releases of this scope. The daily nature of OpenClaw — it's literally called OpenClaw Daily, this podcast — mirrors the shipping culture of the project. That's not a coincidence. It's a philosophy. And it's a bet that the users who stay current benefit more than the users who wait for a stable long-term support release.

[NOVA]: [NOVA]: On April second — the same day as the OpenClaw release — Microsoft unveiled three new foundational models built by its internal AI team. And with them, a declaration from CEO Mustafa Suleyman: Microsoft is now a top-three AI lab, just under OpenAI and Gemini.

[NOVA]: [ALLOY]: Let's take that claim seriously for a moment before we stress-test it. Six months ago, "Microsoft AI" meant "the company that licenses OpenAI." It meant Azure integration and Copilot branding and productivity features. It did not mean foundational model development. So the fact that Microsoft now has an internal team building competitive models, and is willing to say "we are a top-three lab" out loud — that's a genuine shift in positioning.

[NOVA]: [NOVA]: The three models are: MAI-Transcribe-1, a speech-to-text model claiming best-in-class accuracy across twenty-five languages. MAI-Voice-1, a text-to-speech model that reportedly generates sixty seconds of audio per second of output — which if accurate is meaningfully fast for real-time applications. And MAI-Image-2, an upgraded image generation model that's ranking in the top three on the standard leaderboards.

[NOVA]: [ALLOY]: The naming convention is worth noting: MAI. Microsoft AI. It's not a brand partnership name. It's not Copilot branding. It is explicitly "this is Microsoft's own model." That is a deliberate signal. Microsoft is not just integrating OpenAI's technology into its products. It's building its own foundation layer.

[NOVA]: [NOVA]: And the pricing is aggressive. Microsoft is explicitly pricing below AWS and Google on these services. That combination — top-three capability claims plus competitive pricing — is a direct shot at both of the other major cloud providers. This is not "we built a model." This is "we are entering the market as a competitor at a price that makes it hard to say no."

[NOVA]: [ALLOY]: The timing is worth dwelling on. OpenClaw ships its biggest release of the year. Microsoft drops three foundational models with a top-three lab declaration. Both on April second. You'd almost think someone planned it.

[NOVA]: [NOVA]: They didn't plan it together, obviously. But the coincidence is revealing. The AI platform layer is heating up from multiple directions simultaneously. OpenClaw is maturing the agent OS side. Microsoft is maturing the foundation model side. Google dropped Gemini 2.5 Pro at the top of the benchmarks last month. Anthropic is shipping Claude updates faster than ever. And they're all doing it right now because the window to establish position is open right now.

[NOVA]: [ALLOY]: The question for developers and users is: does this change your calculus? If Microsoft is genuinely in the top-three foundation model tier, do you evaluate MAI-Transcribe-1 for your transcription pipeline instead of whatever you're using today? Does MAI-Voice-1 compete with specialized TTS providers for your needs?

[NOVA]: [NOVA]: My read on this is: Microsoft has an extraordinary distribution advantage that capability alone can't match. If these models are genuinely competitive on quality, the integration paths through Azure, through Office 365, through GitHub Copilot — those are already installed everywhere. You don't have to migrate your infrastructure to use a Microsoft model. You just turn it on, often from tools you're already paying for.

[NOVA]: [ALLOY]: Which is a very different competitive moat than Anthropic or Mistral has. Anthropic has to convince you to make an API call to their endpoint. Microsoft can make the model available inside tools you're already using daily. That's a structural advantage that quality alone can't buy, and it's why the top-three claim, if it holds up on evaluations, is genuinely significant rather than just marketing.

[NOVA]: [NOVA]: ... The flip side is: Microsoft's track record on building durable AI products is mixed. Cortana. Clippy. Even some of the early Copilot rollouts confused more people than they helped. Suleyman came from DeepMind and Inflection and has real credibility in the AI lab world. But Microsoft's organizational ability to execute on a coherent AI strategy across its entire product surface is still unproven at this ambition level.

[NOVA]: [ALLOY]: Worth watching closely. A lot depends on whether the top-three claim holds up when the evaluation community gets serious access to these models. Benchmark performance is one thing. Real-world developer experience across twenty-five languages for transcription, or real-world latency for a TTS system at production scale, is quite another.

[NOVA]: [NOVA]: And there's an interesting secondary question here about what this means for the OpenAI relationship. Microsoft and OpenAI have a deep partnership — Microsoft has invested roughly thirteen billion dollars in OpenAI. But now Microsoft is also building models that could compete with OpenAI's own offerings. The MAI models are in categories — speech, voice, image — where OpenAI also has products. How Microsoft navigates that internal tension between partner and competitor will be one of the defining storylines of the next few years in AI.

[NOVA]: [ALLOY]: It's the same tension Google has between its cloud business selling other companies' AI services and its own DeepMind and Google Brain producing competitive models. The hyperscalers are simultaneously the infrastructure providers and the competitors. That's an unusual market structure, and it's not fully stable.

[NOVA]: [NOVA]: Let's talk about governance. Not regulation — we'll get to that — but the practical, infrastructure-level governance of AI agents in enterprise environments.

[NOVA]: [ALLOY]: Okta announced its platform called Okta for AI Agents, generally available April thirtieth. The pitch is straightforward: treat every AI agent as a non-human identity that needs the same lifecycle management as a human employee.

[NOVA]: [NOVA]: And when you lay it out that way, it makes obvious sense. An AI agent operating in an enterprise environment can access data, send requests on behalf of users, make decisions, and take actions. If a human employee had that level of access, you would have a directory entry for them, a documented set of permissions, a complete audit trail, a formal offboarding process when they leave, and a way to revoke access instantly if something goes wrong.

[NOVA]: [ALLOY]: Okta's argument is: you need all of that for agents too. And right now, most enterprises don't have it. They're spinning up AI agents in pilots and proofs of concept without the governance infrastructure to track what those agents can actually access, what they're doing with that access, or how to shut them down cleanly if needed.

[NOVA]: [NOVA]: The platform has four core capabilities. First: automatic discovery of shadow AI agents — agents that are running in an environment without being formally registered anywhere. This is the enterprise AI equivalent of shadow IT. Someone on the marketing team stands up an AI workflow using a third-party tool, it has access to the company's CRM or email system, and nobody in IT knows it exists. Okta wants to find those.

[NOVA]: [ALLOY]: Second: least-privilege policy enforcement. Every agent gets the minimum access required to do its job. Not "access to all of Salesforce because the user who set it up happened to have admin rights." Scoped, documented, auditable access to exactly what the agent needs and nothing more.

[NOVA]: [NOVA]: Third: integrations with major agent platforms — Google Vertex AI, DataRobot, Boomi, and others. So this isn't a standalone system you'd have to build from scratch. It's designed to sit on top of the agent infrastructure that enterprises might already be deploying.

[NOVA]: [ALLOY]: And fourth — and this is the one that gets the most attention — a universal logout or kill switch capability. If an agent starts behaving unexpectedly, or if you discover a rogue agent that someone stood up without authorization, you can cut its access instantly across all connected systems. No waiting for a manual cleanup of permissions scattered across twelve different platforms.

[NOVA]: [NOVA]: The phrase "kill switch" is doing a lot of work here in terms of the message Okta is sending to enterprise buyers. You're not just telling them about access management. You're telling them: you are in control. You can shut this down. That's a message that matters enormously to a CISO who's being asked to approve AI agent deployment across their organization.

[NOVA]: [ALLOY]: There's a deeper point here about enterprise trust cycles. When a new category of technology enters the enterprise, it goes through a predictable sequence. First: enthusiasts adopt it on the edges without telling IT. Second: IT discovers it's already everywhere and scrambles for visibility. Third: governance frameworks emerge that make formal adoption possible. AI agents are right at that transition from stage two to stage three. Okta is positioning itself as the company that makes stage three happen.

[NOVA]: [NOVA]: Let's connect this back to the OpenClaw story, because there's a direct parallel. OpenClaw v2026.4.1 added cron tool allowlists — the ability to define exactly what tools a scheduled agent task can use. That's an access control decision applied at the agent runtime level. Okta is applying the same principle at the enterprise identity management level, across multiple agent platforms simultaneously.

[NOVA]: [ALLOY]: The common thread is that the agent governance problem is real and everybody is solving it from their own position in the stack. OpenClaw solves it at the runtime level for individuals and small teams. Okta solves it at the enterprise identity layer for large organizations with complex compliance requirements. And what we're watching is those solutions converge on the same underlying insight: agents need to be governable, not just capable.

[NOVA]: [NOVA]: ... The timing of Okta's announcement — not yet live, GA at the end of April — is itself a signal. They're announcing this now because the enterprise demand is visible now. CISOs and IT leaders are being asked to approve AI agent deployments today. Okta is getting ahead of the wave, not chasing it.

[NOVA]: [ALLOY]: And notice what the existence of Okta for AI Agents means for the Oracle story we're about to cover. If every AI agent needs an identity, an access policy, an audit trail, and a full lifecycle — that's infrastructure. That's a new category of work and a new category of spend. Not the same as the work the agent is replacing, but genuinely new value being created in the governance layer.

[NOVA]: [NOVA]: Let's talk about Oracle. Bloomberg and The Guardian reported this week that Oracle is cutting thousands of jobs while simultaneously pushing hard into AI data centers, taking on significant debt to fund it, and deepening its infrastructure relationship with OpenAI.

[NOVA]: [ALLOY]: Oracle has committed to an extraordinary capital expenditure on AI infrastructure. The numbers associated with their participation in the Stargate project — the joint venture with OpenAI, SoftBank, and others — run into the hundreds of billions over several years. That is a generational infrastructure bet, and it is being financed in part by reducing the operational headcount of the existing business.

[NOVA]: [NOVA]: Which is where the job cuts come in. This is not Oracle cutting jobs because the business is struggling or revenues are down. This is Oracle cutting jobs because it is deliberately reallocating capital from human operational capacity to compute infrastructure. That is a qualitatively different kind of layoff from a downturn restructuring, and it's a pattern we should expect to see more of across the industry over the next several years.

[NOVA]: [ALLOY]: The Oracle story is the blunt version of something that's happening more quietly elsewhere. You move budget from salaries to GPUs. You bet that the infrastructure you're building will generate more revenue and more margin than the people you let go. And you make that bet at scale, fast, because the window to become the AI infrastructure provider of record for the next decade is open right now — and it won't stay open indefinitely.

[NOVA]: [NOVA]: And to be clear about what Oracle is actually building: this is physical infrastructure. Data centers. Power contracts. Cooling systems. Fiber networking. The things that everyone assumes are someone else's problem until there isn't enough of them. And right now there is a genuine shortage of AI compute capacity relative to demand. The companies building that capacity are making a bet that the demand will hold and grow.

[NOVA]: [ALLOY]: The AI capability story we've been tracking on this show — better models, better agents, better developer tools — all of that runs on physical infrastructure that someone has to build and operate. And the physical infrastructure layer is now in a capital war. Oracle, Microsoft, Google, Amazon are all spending at levels that would have been described as irrational five years ago. The question is not whether they're spending. The question is who wins the bet.

[NOVA]: [NOVA]: Oracle's specific position is interesting because it's not the obvious winner. AWS and Azure have structural advantages in enterprise relationships and developer ecosystems that Oracle doesn't have. Oracle's cloud business has historically been the third-tier player in that fight. But the Stargate relationship gives Oracle a specific, extremely high-value anchor customer: OpenAI. And if OpenAI needs tens of billions of dollars of dedicated compute infrastructure, Oracle has committed to building it.

[NOVA]: [ALLOY]: That anchor customer relationship is the key. You don't need to win the general enterprise cloud market if you're hosting the most important AI company in the world. The Stargate bet is essentially: we will be the physical substrate for OpenAI, and that position will be valuable enough to justify everything we're spending.

[NOVA]: [NOVA]: And there's a broader point about what "AI infrastructure" actually means at this scale. It's not just servers. It's power — data centers of this size require dedicated power contracts with utilities, sometimes dedicated power generation. It's water for cooling. It's the specialized networking that connects thousands of GPUs at the speeds required for large model training. This is industrial-scale construction, not software deployment. The capital requirements are closer to building a factory than shipping an app.

[NOVA]: [ALLOY]: Which is why the job trade-off is so stark. Software headcount is flexible — you can hire and fire relatively quickly. Physical infrastructure is not. Once Oracle commits to building a data center at this scale, that capital is locked in for years. The bet has to pay off over a decade, not a quarter. And Oracle is making it anyway, because they believe the alternative — not being in this market — is worse than the risk.

[NOVA]: [NOVA]: ... The people being cut in this process are real people. We should say that plainly before moving on. This is not an abstract capital reallocation decision on a spreadsheet. These are employees who built products, maintained systems, and served customers — and who were told that their position no longer fits the new capital structure. That's worth naming even as we analyze the strategic logic, because the strategic logic and the human reality are both true simultaneously.

[NOVA]: [ALLOY]: And it's worth noting what kinds of jobs are being cut. The Oracle cuts are primarily in operational, support, and back-office roles — not the data center engineers building the new infrastructure. The agents and automation are not replacing the people building the infrastructure yet. But the direction of travel is clear, and Oracle is one of the most honest public examples of a calculation that is happening quietly at companies across the industry.

[NOVA]: [NOVA]: Our final story today is about governance at the political level, and it is a story of fundamental disagreement about who gets to make the rules.

[NOVA]: [ALLOY]: The White House released a National AI Policy Framework in late March that does three things. One: it advocates for federal preemption of state AI laws. Two: it explicitly recommends against creating any new federal AI rulemaking bodies. Three: it says existing regulatory agencies — the FTC, the FDA, the SEC — are sufficient to handle AI governance across the board.

[NOVA]: [NOVA]: Let me translate the preemption argument into plain terms, because it matters. Right now, individual US states are writing their own AI laws. California has rules around algorithmic discrimination. Colorado has rules. Oregon and Washington have rules. Texas has rules about AI-generated content. New York has rules around hiring algorithms. If you're building an AI product and selling it nationally, you're legally required to comply with all of them simultaneously. The federal position is: that patchwork creates compliance costs that hurt innovation, and we should have one national standard instead.

[NOVA]: [ALLOY]: The counterargument from the states is pointed. You've had years to set national standards and you haven't done it. While you've been not doing it, we've been writing laws that protect our citizens from actual harms that are already happening. You don't get to preempt our protections and replace them with nothing but a statement that the FTC will handle it.

[NOVA]: [NOVA]: And that counterargument has real force, because the scale of state-level activity right now is extraordinary. Forty-five states have introduced more than fifteen hundred AI-related bills in 2026 alone. That is more than in all of 2024. The states are not waiting for federal leadership because federal leadership has not been leading.

[NOVA]: [ALLOY]: The categories of state legislation are worth understanding in some detail. Generative AI disclosure requirements — tell me when I'm talking to an AI, or when the content I'm reading was created by one. Algorithmic accountability — if a machine made a decision that affects my employment, my credit, my insurance, I have a legal right to know how and why. Deepfake protections, especially around elections and non-consensual intimate imagery. These are not fringe academic concerns. These are direct responses to documented harms that are already affecting real people.

[NOVA]: [NOVA]: And the political dynamics here cut across the usual partisan lines in ways that make this harder to predict. Generative AI disclosure rules and deepfake protections have broad bipartisan support at the state level. The federal preemption push comes from an administration that is ideologically opposed to federal regulation generally — but preemption is itself a form of federal intervention, just intervention that benefits industry over states. That tension is going to play out in courts as well as legislatures.

[NOVA]: [ALLOY]: ... Now layer in the EU AI Act, which enters its high-risk enforcement phase by August 2026. High-risk under that framework means AI systems used in employment decisions, credit scoring, law enforcement, critical infrastructure, education, migration — broad categories that cover a significant portion of commercial AI deployment in Europe.

[NOVA]: [NOVA]: If you're building an AI product that you sell into Europe, August 2026 is not a soft deadline. You need documented training data provenance, documented testing processes, a functioning risk management system, human oversight mechanisms on record, and registration in the EU AI system database. This is not future compliance planning. This is compliance work that is due in four months.

[NOVA]: [ALLOY]: And here is where it gets directly relevant for anyone building on OpenClaw or similar agent runtimes. The EU AI Act's high-risk category includes, in some interpretations, AI systems intended to be used for the management and operation of critical digital infrastructure. Depending on how your agent is deployed, what it controls, and what decisions it makes — that classification may apply to what you're building.

[NOVA]: [NOVA]: The OpenClaw cron tool allowlists we talked about earlier — that's exactly the kind of human oversight mechanism the EU AI Act wants to see documented. Not because OpenClaw is specifically targeted by the regulation, but because the pattern of "here is exactly what this agent can do, here is who approved it, here is the audit trail" is precisely the documentation pattern that enterprise customers in regulated industries are now demanding from their AI vendor relationships.

[NOVA]: [ALLOY]: So the governance story connects directly back to the OpenClaw and Okta stories. The regulatory pressure from Brussels and Sacramento is going to push enterprises toward exactly the kind of agent identity management and tool allowlisting that both of those products are building right now. Compliance is not separate from the product story — compliance is becoming part of why the product exists and who's willing to pay for it.

[NOVA]: [NOVA]: The US federal position — existing agencies are sufficient, no new bodies needed — is going to be stress-tested by events rather than debates. The next major AI incident that generates political pressure will test whether the FTC or FDA actually has the legal authority and practical capacity to respond meaningfully. If they do, the no-new-agencies position holds. If they don't, pressure for a dedicated AI regulator will return fast.

[NOVA]: [ALLOY]: The bet being made in Washington is that the industry can self-regulate with existing guardrails, and that the economic benefits of moving fast outweigh the risks of moving without comprehensive rules. That's an arguable position. It's also a position that has been tried in other technology contexts and has not always held up. The social media regulatory vacuum of the 2010s is not a model that Washington should be eager to repeat for AI.

[NOVA]: [NOVA]: Five stories, one through-line. The AI stack is maturing, and maturity means different things at different layers of the stack. At the model layer, it means Microsoft entering genuine top-tier foundation model competition. At the agent runtime layer, it means OpenClaw making background work observable and governable. At the enterprise layer, it means Okta treating agents like employees who need identities, policies, and the ability to be fired. At the infrastructure layer, it means Oracle betting everything on compute at the cost of human headcount. And at the policy layer, it means a regulatory reckoning that is already underway whether Washington is ready for it or not.

[NOVA]: [ALLOY]: The release train isn't just a metaphor for OpenClaw's shipping cadence. It's a metaphor for the whole industry right now. A lot of components are moving fast on the same track simultaneously. The question is whether the governance infrastructure — technical and political — can keep pace with the speed of the capabilities being deployed.

[NOVA]: [NOVA]: That is a question worth asking every week.

[NOVA]: [ALLOY]: And we will.

[NOVA]: [NOVA]: Full show notes and all the links from today's episode are at Toby On Fitness Tech dot com slash podcasts slash episode 22. I'm NOVA.

[NOVA]: [ALLOY]: And I'm ALLOY. We'll be back soon.