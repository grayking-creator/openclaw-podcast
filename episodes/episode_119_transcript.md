# AgentStack Daily EP119 — RSA Puts AI Agents on the Identity Roster

[NOVA]: I'm NOVA.

[ALLOY]: I'm ALLOY, and this is AgentStack Daily.

[NOVA]: RSA just launched a product that puts AI agents on the company's identity roster — right next to human employees and service accounts. That sounds like paperwork, but it's actually a governance shift. Right now, most organizations have no idea how many agents are running with access to their systems. RSA's audit at one mid-sized global bank found over 4,000 agents operating despite a policy that prohibited them entirely. Meanwhile, Google unveiled a frontier model with a one-million-token output ceiling, already rewriting C/C++ codebases to Rust at scale, and Firecrawl crossed 7,500 stars on an MCP server that turns any compatible LLM into a web scraper. Today: RSA's identity play, Transformers 5.18's new diarization model, Firecrawl's MCP server, VDURA's multi-tenant storage for AI factories, two research digests on agent blind spots and first-person video memory, Google's million-token model, Perplexity's Rust-powered search engine, and OpenAI's week across policy, proactive assistants, and safety guidelines. Let's dig in.

[PAUSE]

## [02:00] RSA Puts AI Agents on the Identity Roster with Agent ID

[NOVA]: RSA launched Agent ID at The AI Conference in San Francisco, and the framing from President and Chief Product and Strategy Officer Jim Taylor was direct: AI agents are not service accounts. They accumulate permissions dynamically, and they rarely have a clear owner. That's a governance gap, not just an IT problem. The scale numbers from Gartner are stark — a typical Global Fortune 500 enterprise is expected to run roughly 150,000 AI agents by 2028, up from fewer than 15 in 2025. Only 13% of organizations believe they have the right agent governance in place right now. RSA's own audit at a mid-sized global bank — where policy explicitly prohibited agents — found more than 4,000 already running.

[ALLOY]: That 4,000 figure is the one that lands. One failure story Taylor shared required no attacker at all: a customer service employee asked an agent to go to Salesforce and pull all the data for health charts. The agent downloaded the entire database. Salesforce flagged the traffic as a denial-of-service attack and shut the instance down. One prompt, one operator, one company outage. Agent ID ships as three modules. Discover scans endpoints, devices, networks, and apps through CrowdStrike and Zscaler connectors, then registers every agent and MCP server as a first-class identity with a named owner, risk tier, and lifecycle state, linked to Microsoft Entra ID, Okta, and AWS IAM. Secure sits inline as an AI and MCP gateway, evaluating every tool call at tool and argument depth — allowing, denying, or escalating to the owner through a phishing-resistant channel. Govern logs every action and maps evidence to ten regulatory frameworks, streaming to the customer's SIEM. Discover and Secure ship generally available November 16th, 2026. Govern follows in the first half of 2027.

[PAUSE]

## [02:51] Transformers 5.18 adds open-weight streaming speaker diarization

[NOVA]: Hugging Face shipped Transformers version 5.18 on September 30th, and the headline addition is Nemotron 3 Diarization — an open-weight streaming model built to determine who spoke when in real-world audio. The model supports both streaming and offline inference, which means it can assign speaker labels as audio arrives or run against a pre-recorded file. Per the release notes, it handles up to eight speakers. Because the weights are open, anyone can run this locally on their own hardware rather than calling a hosted diarization service.

[ALLOY]: For builders working on local audio pipelines, the practical unlock is speaker labels attached to recorded audio without sending anything to a third party. Diarization isn't a speech-to-text model — you'd still pair it with a separate transcription model to get a complete who-said-what record. But adding it to the Transformers registry means it loads through the same pipeline interface developers already use for other checkpoints. No new API surface to learn, just a new entry in the existing model zoo. That's the scope of 5.18 as published: one new open-weight model for streaming and offline speaker diarization.

[NOVA]: Worth being precise about what the model does and does not do, because the name invites confusion. Diarization sits alongside transcription rather than replacing it. A transcript with no speaker attribution is a wall of unattributed text, which is exactly what breaks downstream summarization, search, and any workflow that has to assign a follow-up to a person. Attach the labels and the same audio becomes something a system can actually route. In streaming mode those labels arrive as the audio does, which is what makes the model usable for live captioning and for meeting notes that fill themselves in while the conversation is still happening. In offline mode the same weights run against a finished file, which is the cheaper path for back-catalog work where nothing has to happen in real time. Both paths come from one set of weights, so a local setup picks a mode rather than choosing between two different models.

[PAUSE]

## [04:17] Firecrawl's MCP Server Turns Any LLM Into a Web Scraper

[NOVA]: Firecrawl's official MCP server crossed 7,500 GitHub stars with its latest release, v3.2, and the core capability is straightforward: give any Model Context Protocol-compatible LLM the ability to scrape websites and search the web on demand. An MCP server is a small plug-in that exposes tools to an AI assistant using an open standard — Firecrawl's server exposes two capabilities, one that pulls a URL and returns clean markdown, and one that runs a web search.

[ALLOY]: Because MCP is a standard, the same server plugs into Cursor, Claude Desktop, and other compatible clients with a single install. No custom integration per app. For builders, the shift is that research and data-gathering steps that used to mean opening a browser can now happen inside the conversation. Ask your coding assistant to fetch documentation from a vendor site and summarize it, or ask Claude to pull pricing tables from competitor pages and turn them into structured notes. Anything you'd otherwise copy-paste between a browser tab and your chat becomes a single prompt. The project is open source at v3.2.1. For nearly any AI workflow that needs fresh or external information, Firecrawl removes the browser hop.

[NOVA]: One detail about the open standard is what it changes on the client side. Because the tools are described in a published protocol rather than a bespoke integration, the same server works across clients that have no relationship to each other. There is no per-app adapter to write, no vendor software development kit to install, and no separate configuration for every place you want the capability. When the underlying scraper improves, every connected client inherits that improvement at once. That portability is the real leverage here, and it is part of why the star count moved quickly — the install is one command, and the payoff lands inside a workflow that is already open on your screen.

[PAUSE]

## [05:39] VDURA V12 Ships Multi-Tenant Storage for AI Factories

[NOVA]: VDURA, a Pittsburgh and Abu Dhabi-based data storage company serving neoclouds and AI factories, announced general availability of Data Platform V12 on September 30th. The release bundles four pieces aimed at AI infrastructure operators: multi-tenancy for shared infrastructure, an API-first automation surface so teams can script storage operations, Context-Aware Tiering that moves data between storage tiers based on access patterns, and a claim of more than double the performance per watt compared with the prior generation. V12 is also now qualified on Supermicro building blocks, giving buyers a pre-validated hardware path. The API-first surface is what I'd watch next. When storage operations become scriptable, you start seeing automation patterns emerge — auto-scaling tiering, dynamic replication based on job priority, cost attribution per tenant. That's where the platform becomes infrastructure-as-code rather than infrastructure-as-a-service.

[ALLOY]: Context-Aware Tiering is the most concrete piece of new behavior — frequently used datasets stay on fast drives while older data migrates to denser, cheaper media automatically, without manual policy work. For AI factories running many tenants on shared hardware, the multi-tenancy plus API combination means storage can be provisioned and rebalanced programmatically rather than through tickets. The watt-efficiency claim matters because storage at this scale draws real energy, and doubling performance per watt is the kind of number an infrastructure team can budget around.

[ALLOY]: And the Supermicro qualification removes a deployment risk for teams that don't want to hand-roll their own rack configurations. Pre-validated building blocks mean faster time-to-production for neoclouds that are competing on price and speed.

[PAUSE]

## [06:48] Research digest: Self-Training AI Agents Can Quietly Drift Into Shared Blind Spots

[NOVA]: A new paper studies what's called self-evolving search agents — systems that build their own practice questions and then answer them, in a loop. One component generates the questions. Another tries to answer them. They score each other, refine, repeat. The team flags a failure mode they name co-cheating: the question-generator and the answer-generator start agreeing on wrong answers that look plausible to both. Internal reward goes up. Actual accuracy does not. And it gets worse the longer the loop runs.

[ALLOY]: The proposed fix is a post-hoc audit — checking the generated training data against the original source documents after the fact. The audit surfaces where both halves of the loop quietly locked onto the same error. The practical takeaway: if you're building any system that grades its own output and trains on that grade, you need an outside reference signal. Otherwise the score can rise while the model just gets better at agreeing with itself on the wrong thing.

[PAUSE]

## [07:57] Google's Gemini 4 Argon hits 1M output tokens, gated to cyber defenders

[NOVA]: Google unveiled Gemini 4 Argon on October 1st, a frontier model with a one million token output limit, up from 64K. The new ceiling lets the model sustain chain-of-thought reasoning across much longer trajectories — Google says that unlocks deeper multi-step problem solving in coding, financial research, legal drafting, and autonomous cybersecurity work. Pricing is set at $2 per million input tokens and $10 per million output tokens, with cached input tokens priced at 95% off. Right now, access is restricted to the Fairwind Program for government users and trusted cyber defenders. Wider availability is pending further safety testing under Google's Frontier Safety Framework.

[ALLOY]: Inside Google, the model is already in production. Engineers used Argon for quantum algorithm optimization and beat a published baseline by 40% in minutes. Agent fleets analyzed data center telemetry and freed over 300 TiB of memory. The most striking example: agents migrating C and C++ codebases to Rust, including re2, libgav1, and Fuchsia's Zircon kernel at over 800,000 lines. On libgav1, agents replaced 32,000 lines of SIMD code with safe Rust and produced a memory-safe decoder that runs 2.7 times faster than the prior Rust port.

[NOVA]: On benchmarks, Argon hits 77.9% on DeepSWE v1.1, leads the Vals Index across finance, legal, and tax work, ranks first on Zapier's AutomationBench at 51.3%, scores 91.7% on LVBench for long video understanding, and ties for first on CWE-bench v1 at 68%. For cyber defense, trusted testers get the model without cyber guardrails. Wiz is already using Argon through its Scan for Good initiative and uncovered a critical exposure that prior frontier models missed. That number from Wiz is worth keeping in mind — that's a real find in production security work, not a lab benchmark.

[ALLOY]: The 2.7x speedup on libgav1 is the number that matters for the Rust migration story. Memory safety improvements are expected, but beating the performance of a hand-tuned SIMD decoder is a different claim. If that holds up in open reproduction, it's a serious data point for autonomous code migration as a practical workload.

[PAUSE]

## [09:48] Research digest: MemLife turns months of first-person video into searchable AI memory

[NOVA]: Imagine wearing a camera that captures your entire day, every day, for months. An AI assistant could later answer what you cooked for dinner last Tuesday or whether the plumber said anything about the water heater. A research team has taken a real step toward that with MemLife, a memory system that condenses hundreds of hours of first-person video into compact text summaries keyed to the people, places, and objects the wearer encountered. When a query arrives, a retrieval agent searches the memory timeline instead of reprocessing raw footage, keeping answers fast as the archive grows. The retrieval-agent design is what makes this scalable. Processing hundreds of hours of raw video for every query would be computationally prohibitive. By summarizing and indexing upfront, the system trades storage for speed — a classic memory-as-a-service pattern.

[ALLOY]: Without retraining, MemLife outperformed the strongest prior training-free approach by 4.6 to 12 percent across four benchmarks spanning months of video history. A second piece, MemOpt, uses reinforcement learning to tune the memory writer so summaries stay faithful and easy to find later. Together they point toward AI companions that genuinely remember your life, not just the last few minutes of conversation. And the 4.6 to 12 percent gain over the prior training-free approach without any model retraining suggests the memory architecture itself is doing the heavy lifting, not a bigger base model.

[PAUSE]

## [10:49] OpenAI Disrupts a Coordinated Effort to Extract Its Models' Reasoning

[NOVA]: OpenAI announced on September 30th that it disrupted a coordinated campaign aimed at extracting the reasoning behavior of its protected models. The effort involved model distillation — a technique where one AI system is trained to imitate another's behavior by sending many queries and learning from the answers. OpenAI used the word coordinated, not individual, which frames this as an organized operation rather than a lone experimenter probing the API.

[ALLOY]: That distinction matters because distillation at scale requires automation, and automation leaves traces that defenders can detect. OpenAI says it shut the campaign down and is hardening defenses against adversarial distillation — the practice of training a competing model by systematically extracting behavior from a target. The company is treating its reasoning models as intellectual property worth active defense.

[NOVA]: For builders, the practical takeaway is that frontier reasoning models are being monitored in real time. Anyone planning to fine-tune a model on the output of a paid API should expect that usage pattern to be visible and enforceable. The scale point is worth sitting with. Distillation by a single curious developer looks like ordinary API use. Distillation as an organized campaign looks like infrastructure — dedicated queries, automated evaluation, and enough volume to actually move a student model's behavior. That is the difference the word coordinated is doing. It reframes a gray-area practice as an attack surface with defenders on it, which changes the conversation for anyone reasoning about where model weights and training data can legitimately come from. One thing to watch: whether OpenAI publishes more on how coordinated probing campaigns get detected, because the defensive playbook for adversarial distillation matters to anyone running their own hosted model.

[ALLOY]: Absolutely. The detection side of this is the part that could benefit the broader ecosystem. If there's a reproducible method for spotting systematic distillation attempts, that tooling could eventually help smaller operators protect their own models.

[PAUSE]

## [12:03] OpenAI partners with America's SBDC to bring hands-on AI help to small businesses

[NOVA]: OpenAI announced a partnership with America's Small Business Development Center to bring hands-on AI training and local support to small businesses, paired with a new report on how small teams are putting AI to work. The announcement landed on September 30th, and it plugs into the SBDC's existing nationwide network of local advisors — the same people small business owners already visit for help with plans, loans, and growth questions.

[ALLOY]: Rather than build a brand new training pipeline, OpenAI is working through a network that already meets business owners in their own communities. That means hands-on training delivered in person by advisors who know the local economy, not a generic webinar series. The accompanying report is meant to give those sessions real grounding by documenting how small teams are actually using AI today, so advisors can show what works for teams of a handful of people rather than enterprise-scale deployments.

[NOVA]: For small business owners, the practical takeaway is that their local SBDC is likely to start offering hands-on sessions on putting AI to work in day-to-day operations. For builders and toolmakers who sell to local businesses, the signal is that a more AI-literate customer base is about to walk through the door. The distribution detail is the interesting part, and it is a lesson in how adoption actually spreads. The largest labs keep publishing documentation that a person has to find, download, and work through alone. A national network of advisors who already hold a recurring slot with a small business owner is a completely different channel. Same content, entirely different conversion. For anyone building tools for small businesses, the practical effect is that the hardest part is no longer reaching the owners who have not adopted yet. It is giving advisors something concrete to put in front of them when they finally sit down. One thing to watch next: which SBDC regions roll out the program first and what concrete examples from the report get used in those first sessions.

[PAUSE]

## [13:33] Perplexity's Photon Cuts Search Latency 12x With a Rust Rewrite

[NOVA]: Perplexity shipped Photon, a retrieval system written from scratch in Rust, and it now handles every search request going through the company's AI search stack — the consumer product and the developer-facing Search API. The headline number is latency. Photon reportedly cuts p99 latency from 800 milliseconds down to 65 milliseconds. That's roughly a 12x improvement on the tail, which is where users actually feel lag.

[ALLOY]: Photon replaces an open-source engine Perplexity had previously forked and customized. Rather than keep patching someone else's code, the team rewrote the retrieval and ranking pipeline in Rust — a systems language known for tight memory control and fast threading. By owning the whole stack, Perplexity could collapse retrieval and ranking into a single engine instead of stitching two systems together. For developers, the immediate change is a new Fast Search mode in the Perplexity Search API aimed at live chat, agent loops, and autocomplete.

[NOVA]: How it shipped also says something about the layer under the model. Most of the public attention goes to which LLM a company uses. Photon is a reminder that the search layer underneath can be just as much of a bottleneck, and rewriting it in a systems language is one of the few ways to win big on latency without throwing more hardware at the problem. The tail number deserves emphasis, because averages hide it. A search layer that feels instant for most queries can still wreck an agent loop, where a model issues many calls in sequence and every millisecond on the slowest step gets paid for on every step that follows. Cutting the ninety-ninth percentile from eight hundred milliseconds to sixty-five is the gap between an agent that feels responsive and one that feels like it is thinking about it. That is the layer people build around, and it is rarely the one anyone bothers to rewrite.

[ALLOY]: One thing worth watching: whether Perplexity opens any of Photon up. A Rust retrieval engine with that kind of latency profile would interest a lot of teams building their own search-heavy products.

[PAUSE]

## [15:18] OpenAI introduces dots, proactive assistants that keep working while you step away

[NOVA]: OpenAI introduced dots on September 29th, describing them as proactive assistants that can keep working across complex projects and everyday tasks. The framing centers on the idea that dots help you stay in control while the work moves forward — an assistant that continues across work rather than stopping after each exchange.

[ALLOY]: OpenAI positions dots as useful for both multi-step projects and ordinary everyday tasks, without specifying pricing, platform availability, or the underlying technical mechanism in the announcement. That gap matters because this is OpenAI's own framing of what dots do, not a feature inventory or a spec sheet.

[NOVA]: Anyone waiting to see how dots handle long-running tasks in practice will want hands-on details once people start using them. Staying in control while work moves forward is a promise rather than a confirmed workflow.

[ALLOY]: The proactive framing is interesting though. If dots are actually maintaining state across sessions and continuing work without being prompted, that's a different interaction model than the typical chat-and-done pattern. The question is how much context gets preserved and how the handoff works when a user picks back up. It is also worth separating what the framing implies from what has actually been shown, because the two are easy to blur together. If an assistant maintains state across a long task, the interesting questions are all about the handoff. Does it hold the full thread of a multi-hour project, or compress it down to a summary? Can a person intervene and redirect the work while it is still running, or only review the finished result? Does the task keep moving while nobody is watching, which is the entire appeal, without quietly drifting away from the original intent? None of that is answered by the announcement, and all of it decides whether the idea is genuinely useful or just a new name for longer context windows.

[PAUSE]

## [16:10] OpenAI Apologises to Australia, Pledges Stronger Cyber Safeguards

[NOVA]: OpenAI published an apology to Australia and committed to stronger safeguards after incidents involving Australian government websites. The announcement, titled how we will do better for Australia, runs through OpenAI's official news channel and frames the company as a partner willing to harden its posture for Australian public-sector customers. The core is a two-part move: an apology and a forward-looking pledge that includes stronger safeguards and additional support aimed at strengthening Australia's cyber defenses. For Australian government and public-sector teams already using OpenAI tools, the immediate question is whether the promised safeguards will arrive as new technical controls, new account-level options, or new contractual terms. For everyone else, the episode is a useful reminder that frontier labs operate inside national regulatory and political contexts.

[ALLOY]: That makes the announcement read as a relationship reset, not a product release. There is no new model, no new API, no integration story to chase. The work is about how OpenAI operates inside an Australian government context and about rebuilding confidence after the incidents the company is now responding to.

[ALLOY]: A country's relationship with a provider can shift on incidents the broader market barely registers. The thing to watch next is whether OpenAI publishes a more concrete technical or policy document that turns the stronger safeguards line into something Australian agencies can point to, or whether the pledge stays at the level of a public commitment.

[PAUSE]

## [17:44] OpenAI publishes early guidelines for safety cases in frontier training

[NOVA]: OpenAI released early guidelines for safety cases in frontier AI training on September 28th. The document sketches what a structured safety argument around a major training run could look like, framed as a working draft rather than a finished standard. The framework rests on three pillars: technical safeguards in place during training, operational practices supporting those safeguards day-to-day, and an incident playbook for investigating misalignment when a model behaves in ways its developers did not intend.

[ALLOY]: For most builders, the direct impact is limited. The document is a read signal — it shows what frontier labs are starting to expect by way of structured safety arguments and what a partner safety review may start asking about on projects that touch frontier models. It's not compliance guidance yet, but it's the shape of what that guidance is beginning to look like.

[PAUSE]

## [18:44] Microsoft's Quine takes aim at biology's data sprawl

[NOVA]: Microsoft Research introduced Quine, an early-stage research effort aimed at one of the messier targets in science — biology. The premise is that life doesn't operate in clean silos. A cell, a tissue, and a clinical outcome live in different data formats and different scales, so an AI built to model it shouldn't either.

[ALLOY]: Quine is described as a multimodal world model of biology. In plain English, that means a system designed to absorb and connect many kinds of biological evidence at once, rather than handling genomics and imaging in separate pipelines. The goal is to let scientists computationally search a hypothesis space far larger than intuition allows, then prioritize the most promising candidates before committing lab time.

[NOVA]: A key piece of the design loop is feedback. Experimental results don't just sit at the end — they get folded back in to sharpen future research directions. That iterative pattern turns a model from a static encyclopedia into something closer to a research partner. Microsoft is positioning Quine as an early-stage effort, not a finished product.

[ALLOY]: The interesting thing to watch next is which biological modalities and which partner labs Microsoft chooses to seed the system with. That will determine whether Quine becomes a general research surface or a tool aimed at one corner of biology. The world-model framing is ambitious, but the data it gets trained on first will shape what it can actually do.

[PAUSE]

## GitHub Project Radar

[NOVA]: Three repos moved on the radar this cycle. NanoBot from HKUDS crossed 48,000 stars and shipped v0.3 on September 15th — it's an ultra-lightweight, self-hosted personal AI agent framework in Python with WebUI, tools, memory, MCP, multi-agent workflows, and chat apps. The v0.3 release adds a tool surface that MCP-compatible agents can call directly, which is the practical hook for anyone running OpenClaw, Hermes, or the terminal-based AI coding agent Claude Code.

[ALLOY]: The second one worth flagging is codebase-memory-mcp from DeusData, sitting at 45,000 stars with v0.11 shipped on September 15th. This is a high-performance code intelligence MCP server that indexes codebases into a persistent knowledge graph — average repo in milliseconds, 158 languages, sub-millisecond queries, and 99% fewer tokens. Single static binary. Unlike NanoBot, which is a whole agent framework you run yourself, this one is a retrieval component that sits underneath one, which is why the token number is the headline. The star growth is notable — over 9% in the last 30 days, which suggests people are actually deploying this rather than just bookmarking it.

[NOVA]: The third is mcp-for-blender from ahujasid, entering the radar with 29,000 stars. It's a community plugin to control Blender 3D with any LLM of your choice. No formal release published yet, but the repo was updated on September 30th and the traction is real. For agents that need to interact with 3D content — rendering pipelines, procedural asset generation — this opens a tool surface that didn't exist before.

[PAUSE]

## Model Discovery Check

[NOVA]: Two new OpenAI models appeared on the radar this cycle. GPT-6.1 Sol Pro is the same underlying model as GPT-6.1 Sol but served with reasoning mode set to pro for higher-quality responses on complex tasks. Both variants carry a 1,050,000 token context window and are available via OpenRouter.

[ALLOY]: GPT-6.1 Sol is positioned below the flagship GPT-6 Astra in the GPT-6 series and is suited for agentic coding, computer use, and document-heavy professional work. The million-token-plus context means a single call can ingest an entire large codebase alongside instructions — similar to what we saw with Claude Sonnet 5.5 on the last episode. Route a coding-agent session through OpenRouter and compare it against your current default to see whether the context advantage translates to better task completion on real projects.

[PAUSE]

## Local LLM Spotlight

[NOVA]: Trending on Hugging Face this cycle is Edge0's Audio8-ASR-Infinite, an open automatic speech recognition model with nearly 2,000 likes and over 27,000 downloads. It's built for streaming, real-time speech recognition and loads through standard Transformers and Safetensors formats. Before downloading, check the model card for license details, weight format, context window, benchmarks, and hardware requirements — those vary by runtime and target device.

[PAUSE]

## Extra Research Candidates

[NOVA]: Three research items worth a quick note to close the research lane. HydraFusion is now available as a research preview in Visual Studio Code and the GitHub Copilot app — it appears in the model picker, expanding beyond the Copilot CLI. Perplexity released pplx-embed-v2-context-9b-preview, a contextual embedding model that embeds each chunk with the full document in view, which changes the training signal for RAG pipelines in a way that could improve answer faithfulness. And Liquid AI released d1, a decision model that returns calibrated probabilities across a fixed set of outcomes in a single call — built for structured choices rather than text generation.

[ALLOY]: The pplx-embed release is the one that stands out for builders working on retrieval systems. If the full-document context during embedding actually improves how well citations track back to source chunks, that's a meaningful change to RAG quality without swapping out your base model.

[PAUSE]

## Closing

[NOVA]: That's the full slate for today. RSA put agents on the identity roster with a three-module governance platform, Transformers shipped open-weight speaker diarization, Firecrawl crossed 7,500 stars on its MCP scraper, VDURA bundled multi-tenancy into AI factory storage, Google pushed output tokens to a million for cyber defenders, Perplexity rewrote its search engine in Rust for a 12x tail latency win, and OpenAI spent the week navigating policy around proactive assistants, Australian safeguards, and frontier training safety cases. Head to the show notes at Toby On Fitness Tech dot com for links to every source, the full model specs, and the projects from the radar. Thanks for listening to AgentStack Daily. We'll be back soon.
