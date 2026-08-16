# AgentStack Daily EP102 — Qwen's 2.4T Open-Weight Model Lands on O, NIST Asks How to Modernize the National , ChatGPT Desktop Finally Arrives on Linux

**Title:** AgentStack Daily: Qwen's 2.4T Open-Weight Model Lands on OpenRouter

**Tagline:** Today's stories: Qwen's 2.4T Open-Weight Model Lands on OpenRouter, NIST Asks How to Modernize the National Vulnerability Database, ChatGPT Desktop Finally Arrives on Linux, and Jensen Huang Tops Glassdoor's 2026 Best CEOs List. Concrete changes across the agent stack — what shipped, the mechanisms underneath, and what each one means for builders working with coding agents, models, and tooling.

**Feed description:** Qwen's 2.4T Open-Weight Model Lands on OpenRouter, NIST Asks How to Modernize the National Vulnerability Database, ChatGPT Desktop Finally Arrives on Linux, and Jensen Huang Tops Glassdoor's 2026 Best CEOs List. What shipped, how the mechanisms work, and what each change means for agent builders.

---

## Story Slate

1. **Qwen's 2.4T Open-Weight Model Lands on OpenRouter**
Qwen has listed a new open-weight model on OpenRouter: Qwen3.8 2.4T A95B. It is a sparse mixture-of-experts design with 95 billion active parameters out of 2.4 trillion total, and a 1 million token context window. The model card calls it the open-weight variant of Qwen3.8 Max, Qwen's closed hosted model.
Technical depth angle: Sparse mixture-of-experts means only a slice of the model's weights fires on any given request — here 95B of 2.4T — which keeps per-query compute manageable despite the very large total. The 1M-token context window lets the model hold long documents or codebases inside a single prompt.
Actionability angle: What this means: builders who can host open weights gain a new very-long-context option reachable through OpenRouter, without paying closed-API prices to run it. Why this matters: the listing puts MoE-scale long context in an open package, which is the dimension worth probing first.
Listener hook: A 2.4-trillion-parameter Qwen model with a million-token context is now reachable through one OpenRouter call.

2. **NIST Asks How to Modernize the National Vulnerability Database**
NIST has opened a public request for information on modernizing the National Vulnerability Database as artificial intelligence and machine-consumable security data reshape vulnerability management. The notice asks stakeholders to identify priorities, opportunities, and challenges around scalability, automation, interoperability, transparency, and utility. The database remains the U.S. government's standards-based repository for vulnerability data. Comments are due October 13, 2026, under docket NIST-2026-0100.
Technical depth angle: The useful mechanism is public consultation. NIST is asking stakeholders to identify priorities, opportunities, and challenges across scalability, automation, interoperability, transparency, and utility. The notice contains no selected architecture, implementation plan, or changed database behavior.
Actionability angle: What this means: Organizations that work with vulnerability data can respond to the request and describe priorities or challenges in those five areas. Why it matters: The request creates a public input channel, but it does not announce a technical redesign.
Listener hook: If your work depends on vulnerability data, this is a direct opportunity to tell NIST what the National Vulnerability Database needs to handle better.

3. **ChatGPT Desktop Finally Arrives on Linux**
OpenAI has released a dedicated ChatGPT desktop application for Linux, closing a long-standing gap in its platform coverage. The app is being distributed through openai.com/codex/, and the August 11 announcement drew a 141-point Hacker News thread. Linux users had previously relied on the web client or unofficial community packages; this marks OpenAI's first official native desktop client for the operating system.
Technical depth angle: The release is a native Linux desktop client from OpenAI, surfaced via the Codex product page rather than the main ChatGPT marketing site. The supplied source material does not detail the underlying framework, packaging format, distribution method, or feature set, so further mechanism claims would be speculation.
Actionability angle: Linux developers and daily-driver users now have an official OpenAI desktop client to install alongside their other native apps, rather than working around the absence with browser tabs or third-party builds. For teams standardizing on Linux workstations, this removes one longstanding reason to keep a separate ChatGPT workflow.
Listener hook: If you've been running ChatGPT in a browser tab on Linux because there was no official option, that era is over.

4. **Jensen Huang Tops Glassdoor's 2026 Best CEOs List**
NVIDIA founder and CEO Jensen Huang has been ranked number one on Glassdoor's 2026 Best CEOs list, with 99% of employees approving of his leadership. The ranking, announced August 12, is built directly from anonymous employee reviews rather than outside analyst scores or financial metrics. The unusually high approval rate stands out at one of the AI industry's most-watched companies.
Technical depth angle: The ranking's mechanism is direct anonymous employee review on Glassdoor, where workers rate senior leadership and the approval percentage determines placement. With 99% approval, Huang's score signals unusually consistent internal sentiment from his own workforce. The source does not detail Glassdoor's exact weighting beyond employees voting on leadership performance.
Actionability angle: What this means is that NVIDIA now carries a public signal of internal stability during a period when AI-related hiring is intense across the industry. Why this matters for builders and partners weighing the competitive landscape is that one of the central companies in AI infrastructure is also reporting unusually strong employee sentiment from its own workforce.
Listener hook: Curious which company leads the AI pack by employee vote? The answer just dropped, and 99% of its workforce approved.

5. **Research digest: AI Agents Falter When Work Spans Multiple Tools**
A new IBM Research benchmark called VAKRA puts frontier AI agents through realistic enterprise-style work: chaining together over 8,000 live APIs across 62 domains while respecting tool-use policies. The headline finding is that performance drops sharply once a task requires reasoning across multiple sources — agents handle single tool calls fine but stumble when they have to combine results, disambiguate entities, or refuse questions that violate a policy. The failures cluster at the language reasoning step, not at tool invocation itself.
Technical depth angle: The plain-language finding is that agent failures aren't about calling APIs — they're about the language reasoning between calls, like picking the right 'Acme' out of several and grounding answers across sources. As soon as a task requires combining multiple sources or honoring a usage policy, that language step becomes the bottleneck.
Actionability angle: For builders, this means single-step agent workflows over well-scoped APIs are realistic today, but anything that crosses systems or brushes a policy line still calls for human review. The bottleneck is now clearly the language reasoning between tool calls, not the calls themselves.
Listener hook: Frontier agents can call the right tools — they just can't always figure out which 'Acme' you meant.

6. **Grok 4.6**
xAI announced Grok 4.6 on August 13, 2026, framing it as a significant new entry in the "AI teammate" category — software designed to work alongside people rather than just answer prompts. The announcement drew 553 points on Hacker News after Latent Space surfaced it. However, xAI did not publish a changelog, benchmark numbers, or feature list alongside the announcement, so the practical details for builders remain sparse.
Technical depth angle: The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment.
Actionability angle: Test the sourced change against one real workflow before depending on it.
Listener hook: The practical question is what this changes for a builder today.

7. **Research digest: Drones that follow directions get better at improvising**
Researchers unveiled DreamFly, a system that teaches drones to navigate unfamiliar spaces using natural-language instructions. The aerial agent plans a few steps ahead, executes one move, then replans based on what it sees. On the OpenFly benchmark, it outperformed every prior method, clearing around 29 percent of tasks in environments it had never encountered during training, suggesting progress toward rescue, inspection, and delivery drones that can adapt in real time.
Technical depth angle: The key insight is that rolling replanning beats committing to a full route. The drone drafts a short sequence of moves, executes only the first one, then re-checks the scene, which means it can recover when the view changes mid-flight. It also learns to recognize when it has actually reached the goal, rather than guessing.
Actionability angle: For builders working on embodied AI or robotics, this is a useful reference for how to pair language instructions with continuous visual replanning rather than locked-in trajectories. It also signals that drone navigation is moving from scripted routes toward more flexible, language-driven autonomy.
Listener hook: A drone that can take a verbal detour and actually make it.

8. **GitHub ships Agent Plugins 1.0 across VS Code, Copilot CLI, and the Copilot app**
GitHub released Agent Plugins 1.0 on August 6, letting developers build a plugin once and run it across VS Code, the Copilot CLI, and the Copilot app. Five launch partners — AWS, Anysphere, Microsoft, OpenAI, and Vercel — are named in the changelog post from August 12, signaling the format is meant to extend beyond GitHub's own surfaces.
Technical depth angle: The cross-client model means a single packaged plugin loads inside VS Code, the Copilot CLI, and the Copilot app without separate builds per environment.
Actionability angle: For builders maintaining agent tooling, one package can now reach developers in their editor, on the command line, and inside the Copilot app at once. Why this matters: partner plugins from AWS, Anysphere, Microsoft, OpenAI, and Vercel will be the first real signal of what useful cross-client agents look like.
Listener hook: Build your agent plugin once and it works in your editor, your terminal, and the Copilot app.

9. **OpenAI's enterprise study finds AI moving from chat to autonomous execution**
OpenAI published new research on August 12 examining how enterprises are actually adopting agentic AI. The headline finding: leading companies are moving beyond asking AI for help and into letting it carry out work. The piece centers on tools like ChatGPT and Codex, and argues a small group of frontier firms is pulling ahead by figuring out execution-style AI faster than the rest of the market.
Technical depth angle: The plain finding is a shift from conversational assistance to agentic execution — AI systems that plan and act on multi-step tasks inside enterprise workflows rather than only responding to single prompts.
Actionability angle: The practical read for builders is that enterprise demand is concentrating on agentic patterns where the model plans, uses tools, and finishes multi-step work, not single-turn chat. What this means is that products aimed at enterprises need to support autonomy and tool use rather than just Q&A. The takeaway is that simpler chatbot patterns may carry less weight with enterprise buyers over time.
Listener hook: The companies actually shipping AI into real workflows are doing something measurably different from the ones still running chatbot pilots.

10. **RingCentral puts ChatGPT Work and Codex inside its engineering and ops stack**
RingCentral is featured in an OpenAI case study published on August 12 describing how the cloud communications company uses ChatGPT Work and Codex to speed up AI product development and consolidate operational intelligence across its engineering and operations teams. The piece frames the deployment as a way to centralize how work gets done, from shipping product to running day-to-day operations.
Technical depth angle: Two named OpenAI tools in active use: ChatGPT Work for general team workflows and Codex as a coding-focused assistant, deployed together across engineering and operations so the same AI surface area supports both building software and running the business.
Actionability angle: What this means: a real customer is leaning on ChatGPT Work and Codex across both product and operations, not just one team. Why this matters for builders: enterprise validation of a twin-tool pattern, pairing a general work assistant with a coding assistant, looks like a workable template for centralizing AI inside a single company.
Listener hook: One of the bigger names in business phone and contact center is betting on ChatGPT Work plus Codex for both code and operations.

11. **DeepMind puts sign language AI in users' hands**
DeepMind announced SL2T, a sign-language-to-text model, on August 12, 2026, built to power new sign language features for Deaf and hard of hearing users. The post frames SL2T as a direct bridge from signed to written communication, and positions it as a user-facing capability rather than a research demo. DeepMind calls it a breakthrough, and the emphasis is on getting the technology into the hands of the community it serves first.
Technical depth angle: SL2T translates signed input into written text. That is the full mechanism the announcement describes — the source material does not detail architecture, training data, supported sign languages, or accuracy figures.
Actionability angle: Right now this is an announcement rather than a deployment spec, so there is nothing for builders to wire up yet. The thing to watch is which DeepMind surface — app, tool, or external API — first delivers SL2T-powered features, and whether outside developers will get access at all.
Listener hook: A frontier lab is leading with an accessibility use case, and sign language is the headline product rather than a footnote.

12. **llama.cpp**
Hacker News score 352; discussion: https://news.ycombinator.com/item?id=49267928; headline-only source — insufficient for a full story The primary source at llama.app supports only these stated facts; unsupported specifications are deliberately omitted. The primary source at llama.app supports only these stated facts; unsupported specifications are deliberately omitted.
Technical depth angle: The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment.
Actionability angle: Test the sourced change against one real workflow before depending on it.
Listener hook: The practical question is what this changes for a builder today.

13. **Apple Silicon and macOS VMs: Faster LLM Inference with llama.cpp**
Hacker News score 303; discussion: https://news.ycombinator.com/item?id=49259339; headline-only source — insufficient for a full story The primary source at github.com supports only these stated facts; unsupported specifications are deliberately omitted. The primary source at github.com supports only these stated facts; unsupported specifications are deliberately omitted.
Technical depth angle: The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment.
Actionability angle: Test the sourced change against one real workflow before depending on it.
Listener hook: The practical question is what this changes for a builder today.

14. **Evolve your marketing with new AI tools**
Learn how new AI and agentic experiences across Google Ads and Google Analytics can simplify your marketing workflow. The primary source at blog.google supports only these stated facts; unsupported specifications are deliberately omitted.
Technical depth angle: The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment.
Actionability angle: Test the sourced change against one real workflow before depending on it.
Listener hook: The practical question is what this changes for a builder today.

---

## Editorial Mix Check

- flagship_products: 7
- builder_projects: 5
- local_ai: 2
- hardware_compute: 2
- policy_regulation: 1
- research: 2

---

## Model Discovery Check

- **Qwen: Qwen3.8 2.4T A95B** (qwen) — Newly listed this cycle (verified August 13, 2026). Primary source: https://openrouter.ai/models/qwen/qwen3.8-2.4t-a95b. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 1000000 tokens; modality: see primary source. Capabilities: context length 1000000; Qwen3.8 2.4T A95B is an open-weight sparse mixture-of-experts model from Qwen and the open-weight variant of [Qwen3.8 Max](https://openrouter.ai/qwen/qwen3.8-max), with 95 billion active parameters out of 2.4 trillion total. It is.... Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/qwen/qwen3.8-2.4t-a95b and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **DeepSeek: DeepSeek V4 Pro 0813** (deepseek) — Newly listed this cycle (verified August 13, 2026). Primary source: https://openrouter.ai/models/deepseek/deepseek-v4-pro-0813. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 1048576 tokens; modality: see primary source. Capabilities: context length 1048576; DeepSeek V4 Pro 0813 is a large-scale mixture-of-experts model from DeepSeek. This is the GA release of DeepSeek V4 Pro.. Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/deepseek/deepseek-v4-pro-0813 and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **NVIDIA: Nemotron 3.5 Lightning** (nvidia) — Newly listed this cycle (verified August 13, 2026). Primary source: https://openrouter.ai/models/nvidia/nemotron-3.5-lightning. Availability: API via OpenRouter. Capabilities: context length 1048576; NVIDIA Nemotron 3.5 Lightning is an open mixture-of-experts model from NVIDIA, with 3B active parameters out of 30B total. It is suited for high-throughput agen. Try now / integration angle: available for evaluation via the model page above. Decision: Not Selected — variant/duplicate of a model featured on a recent broadcast, or not a major standalone drop.

- **NVIDIA: Nemotron 3.5 Lightning (free)** (nvidia) — Newly listed this cycle (verified August 13, 2026). Primary source: https://openrouter.ai/models/nvidia/nemotron-3.5-lightning:free. Availability: API via OpenRouter. Capabilities: context length 1000000; NVIDIA Nemotron 3.5 Lightning is an open mixture-of-experts model from NVIDIA, with 3B active parameters out of 30B total. It is suited for high-throughput agen. Try now / integration angle: available for evaluation via the model page above. Decision: Not Selected — variant/duplicate of a model featured on a recent broadcast, or not a major standalone drop.

---

## Local LLM Spotlight

- **meta-models/Muse-Glimmer-30B** — https://huggingface.co/meta-models/Muse-Glimmer-30B — Trending open model on Hugging Face; task image-text-to-text; 1352 likes and 121042 downloads. Tags: transformers, safetensors, muse_glimmer, image-text-to-text, conversational, arxiv:2504.13181, arxiv:2602.06036, license:apache-2.0, eval-results, endpoints_compatible.
  Try now: Read the linked model card before downloading, and choose a runtime or device only after it confirms the license, weight format, context window, benchmarks, and hardware requirements.

---

## GitHub Project Radar

- **HKUDS/nanobot** — https://github.com/HKUDS/nanobot — Ultra-lightweight, open-source, self-hosted personal AI agent framework in Python with WebUI, tools, memory, MCP, multi-agent workflows, automation, and chat apps `stars: 46,928`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v0.3.0 (2026-07-25)`.
  Why this is on the radar now: v0.3.0 shipped on 2026-07-25 and the repository was updated on 2026-08-13.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — High-performance code intelligence MCP server. Indexes codebases into a persistent knowledge graph — average repo in milliseconds. 158 languages, sub-ms queries, 99% fewer tokens. Single static binary `stars: 38,763`; `stars_delta_30d: +7,909 (+25.6%) since 2026-07-13`; `latest_release: v0.10.3 (2026-08-13)`.
  Why this is on the radar now: v0.10.3 shipped on 2026-08-13 and the repository was updated on 2026-08-13.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — 🚀 The fast, Pythonic way to build MCP servers and clients. `stars: 27,202`; `stars_delta_30d: +1,034 (+4.0%) since 2026-07-13`; `latest_release: v3.4.7 (2026-08-10)`.
  Why this is on the radar now: v3.4.7 shipped on 2026-08-10 and the repository was updated on 2026-08-11.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

---

## Extra Research Candidates

- **From assistance to execution: How enterprises put AI to work** — https://openai.com/index/how-enterprises-put-ai-to-work — OpenAI research reveals how enterprises are adopting agentic AI, using ChatGPT and Codex, and how frontier firms are pulling ahead in AI adoption. Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

- **Daybreak models are now available on AWS** — https://openai.com/index/daybreak-models-are-now-available-on-aws — OpenAI and AWS are making Daybreak cybersecurity capabilities available through Amazon Bedrock to support enterprise security workflows. Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

- **MAI-Code-1.1-Flash available in GitHub Copilot** — https://github.blog/changelog/2026-08-11-mai-code-1-1-flash-available-in-github-copilot — MAI-Code-1.1-Flash, Microsoft&#8217;s latest small-tier coding model, is now rolling out in GitHub Copilot. Building on MAI-Code-1-Flash, it adds native vision support for image understanding and delivers improvements across coding quality, Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

---

## Show Notes

```md
Episode 102 — August 13, 2026

[00:00] Episode hook

Qwen's 2.4T Open-Weight Model Lands on OpenRouter headlines a dense cycle. NIST Asks How to Modernize the National Vulnerability Database, ChatGPT Desktop Finally Arrives on Linux, Jensen Huang Tops Glassdoor's 2026 Best CEOs List round out the front of the episode, with deeper cuts across models, tooling, and infrastructure behind them. Each story gets the same treatment — what shipped, the mechanism underneath, and what it changes for working builders.

[02:00] Qwen's 2.4T Open-Weight Model Lands on OpenRouter

Qwen has listed a new open-weight model on OpenRouter, the routing service that lets one API key reach many providers. The model is Qwen3.8 2.4T A95B, described on the model card as a sparse mixture-of-experts — meaning only a fraction of its total weights fire on any given request. The card lists 95 billion active parameters out of 2.4 trillion total, plus a 1 million token context window, so a single prompt can hold very long documents or code.

The listing calls the model the open-weight variant of Qwen3.8 Max, which is the closed hosted version run inside Qwen's own API. That distinction is the practical news: anyone who can stand up the weights — on their own hardware or through a third-party host — can access the same underlying design, while Max stays a closed endpoint.

The model card does not include release notes or a changelog beyond the basic stats, so behavior claims stay thin. What is clear from the listing itself: a very large open-weight Qwen model with MoE economics and a long context window is now reachable through OpenRouter's catalog.

[02:00] NIST Asks How to Modernize the National Vulnerability Database

NIST has opened a public request for information on modernizing the National Vulnerability Database. Published in the Federal Register on August 12, 2026, under docket NIST-2026-0100, the notice asks stakeholders to describe priorities, opportunities, and challenges in five areas: scalability, automation, interoperability, transparency, and utility.

The National Vulnerability Database remains the U.S. government's standards-based repository for vulnerability data. NIST's stated context is that artificial intelligence and machine-consumable security data are reshaping vulnerability management, prompting the agency to gather input on how the database can improve.

This is a consultation, not a technical rollout. The notice does not describe a selected architecture, implementation, or changed database behavior. Comments close October 13, 2026, giving vulnerability-data users a dated opportunity to contribute to the public record before the modernization discussion advances.

[02:47] ChatGPT Desktop Finally Arrives on Linux

OpenAI has released a dedicated ChatGPT desktop application for Linux, ending one of the longer-running gaps in its desktop lineup. The app is being offered through openai.com/codex/, and the announcement quickly generated a 141-point Hacker News thread when it broke on August 11, with TechCrunch AI among the outlets covering the launch.

Linux users who wanted ChatGPT on the desktop had until now been limited to the web client running in a browser or to unofficial community packages. With this release, OpenAI is shipping its own native client for the operating system, distributed through the same Codex page that has hosted the company's developer tooling.

For developers running Linux as their primary workstation, the practical change is straightforward: there is now an officially supported desktop install path from OpenAI itself, rather than a workaround. The strong Hacker News reception, with the thread reaching 141 points shortly after publication, suggests pent-up demand from a developer audience that has long asked for parity with macOS and Windows. Worth watching next is how broadly OpenAI distributes the build and whether the Linux client ships in lockstep with future macOS and Windows updates or trails behind.

[03:59] Jensen Huang Tops Glassdoor's 2026 Best CEOs List

Jensen Huang, NVIDIA's founder and CEO, took the number one spot on Glassdoor's 2026 Best CEOs ranking, with 99% of employees approving of his leadership. The list dropped on August 12, and unlike many CEO rankings, it is built directly from anonymous employee reviews submitted on Glassdoor, not from outside analyst scores or financial metrics.

An approval rate that high stands out as unusually strong internal sentiment at a company closely tied to the AI industry. The methodology matters because it reflects what employees report day to day, rather than how the market values the company's stock or strategy. For workers across AI, the practical read is that the leadership of a central AI company is well-regarded by its own workforce, a useful signal as the industry competes for talent and partnerships. Worth watching whether Huang holds the spot next year.

[04:52] Research digest: AI Agents Falter When Work Spans Multiple Tools

Agents that chain tools together break down long before the conversation gets complicated. A new IBM Research benchmark called VAKRA tested frontier and open-weight models on more than 8,000 real APIs across 62 domains, asking them to plan multi-step work while respecting tool-use policies. The headline number: performance dropped by more than half as soon as tasks required reasoning across multiple sources, compared to single-step tool calls. The failures weren't at the tool layer — models made the right API calls — they clustered at the language step, like figuring out which company a user means or grounding an answer in the right document. On questions that should have been refused under a policy, accuracy also collapsed. For builders piloting agents that touch internal docs and live business APIs, single-step workflows are realistic today, but anything that crosses systems or brushes a policy line still wants a human in the loop.

[05:49] Grok 4.6

xAI announced Grok 4.6 on August 13, 2026, framing it as a significant new entry in the "AI teammate" category — software designed to work alongside people rather than just answer prompts. The announcement drew 553 points on Hacker News after Latent Space surfaced it. However, xAI did not publish a changelog, benchmark numbers, or feature list alongside the announcement, so the practical details for builders remain sparse. The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment. Test the sourced change against one real workflow before depending on it.

[06:28] Research digest: Drones that follow directions get better at improvising

Drones that can follow spoken or written directions through unfamiliar spaces took a step forward this week. Researchers built a system called DreamFly that lets an aerial drone look around, plan a few steps ahead, decide when it has arrived, and replan mid-flight when the view changes. The key is treating navigation as a rolling decision rather than locking in a full route from the start.

The team tested DreamFly on a public drone navigation benchmark and it beat every prior method, clearing around 29 percent of tasks in completely new environments it had never seen during training. That unseen-environment number matters because real deployment means the drone rarely sees the exact buildings and trees from practice.

In practice, this is the kind of system that could one day let a rescue coordinator tell a drone to fly past the broken chimney and check behind the green roof, and the drone would actually pull it off.

[07:27] GitHub ships Agent Plugins 1.0 across VS Code, Copilot CLI, and the Copilot app

GitHub published Agent Plugins 1.0 on August 6, with the changelog post landing on August 12. The release puts the same plugin format into three GitHub surfaces: VS Code, the Copilot CLI, and the Copilot app. The headline capability is straightforward — build a plugin once, and it works across all compatible agent clients, rather than maintaining a separate build for each.

Five launch partners are named in the changelog: AWS, Anysphere, Microsoft, OpenAI, and Vercel. Each one ships agent products of its own, and their participation is the clearest hint that GitHub is aiming this format beyond a GitHub-only audience.

The practical shift is for builders who maintain agent tooling. One package can now reach developers in their editor, on the command line, and inside the Copilot app. The changelog does not detail plugin mechanics or permission models, so the exact authoring surface is worth checking in GitHub's plugin docs before committing to a build.

What to watch next is which partner plugins actually ship first out of AWS, Anysphere, Microsoft, OpenAI, and Vercel. Those releases will show what cross-client agent work looks like in practice, and whether the format holds up beyond GitHub's own clients.

[08:41] OpenAI's enterprise study finds AI moving from chat to autonomous execution

OpenAI published a new research piece on August 12 about how enterprises are putting AI to work, and the framing is blunt: the companies pulling ahead aren't using AI for assistance anymore, they're using it for execution. The piece centers on agentic AI — systems that can plan and carry out multi-step tasks, built on tools like ChatGPT and Codex — rather than just respond to prompts.

The core finding is that a small slice of frontier firms is moving faster than the rest of the market. According to the research, these leaders are weaving agentic AI into actual business workflows, while most companies are still figuring out the basics.

Why this matters now is the shift in vocabulary. OpenAI is framing the winning pattern as execution, not assistance, which means the model is being trusted to take action across steps rather than only suggest the next one. For builders watching enterprise demand, the signal is that agentic patterns are where attention is concentrating — a different brief than building a chatbot.

One thing to watch is whether the gap between frontier firms and laggards widens or closes as agentic tooling becomes more accessible. The report's whole argument is that execution-style AI is where the advantage now lives, and that pilot-mode thinking will be left behind.

[10:03] RingCentral puts ChatGPT Work and Codex inside its engineering and ops stack

RingCentral is the subject of a new OpenAI case study published on August 12, and the headline is that the cloud communications company is running both ChatGPT Work and Codex across its engineering and operations teams. The framing from OpenAI is that RingCentral is using these tools to accelerate AI product development and to centralize operational intelligence, meaning the same AI surface area is supporting the people who build software and the people who run the business day to day.

The case study is short on specifics, but the two named tools are concrete. ChatGPT Work is positioned as the general team workflow layer. Codex is the coding-focused assistant. Put together, RingCentral is using a twin-tool pattern: one assistant for everyday work and one tuned for shipping code, deployed across two of the most important functions inside a software company.

For listeners who run their own teams, the useful takeaway is the pattern, not the press release. A company the size of RingCentral is publicly betting that pairing a general work assistant with a coding assistant can centralize AI use across both engineering and operations. That is a signal that enterprise buyers are starting to think about AI as one shared capability inside a company, not a separate purchase for each department.

One thing to watch: a case study is a customer's story, not a product roadmap. What is documented here is that RingCentral is using ChatGPT Work and Codex. What is not yet clear is how deep the integration goes, what measurable results the company is reporting, and whether the case study points to deeper OpenAI features or to a more general template other large teams can copy.

[11:48] DeepMind puts sign language AI in users' hands

DeepMind published a new sign-language-to-text model called SL2T on August 12, 2026, calling it a breakthrough aimed at Deaf and hard of hearing users. The post frames SL2T as the engine behind new sign language features shipping to real users, not a research demo. The pitch is direct: take signed input, return written text, and put that capability in front of the community it serves first.

The source material is short on deployment detail. DeepMind has not yet specified which product surface will carry SL2T, which sign languages it covers, or whether external developers will get an API; the announcement is built around the model and the user-facing features it enables rather than around a developer handoff.

The interesting shift is framing. A frontier lab is leading with an accessibility use case rather than treating it as a footnote — sign language is the headline product, not a side feature. Watch for DeepMind to share where SL2T lands in its apps and whether outside builders will be able to plug into it.

[12:53] llama.cpp

Hacker News score 352; discussion: https://news.ycombinator.com/item?id=49267928; headline-only source — insufficient for a full story The primary source at llama.app supports only these stated facts; unsupported specifications are deliberately omitted. The primary source at llama.app supports only these stated facts; unsupported specifications are deliberately omitted. The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment. Test the sourced change against one real workflow before depending on it.

[13:22] Apple Silicon and macOS VMs: Faster LLM Inference with llama.cpp

Hacker News score 303; discussion: https://news.ycombinator.com/item?id=49259339; headline-only source — insufficient for a full story The primary source at github.com supports only these stated facts; unsupported specifications are deliberately omitted. The primary source at github.com supports only these stated facts; unsupported specifications are deliberately omitted. The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment. Test the sourced change against one real workflow before depending on it.

[13:52] Evolve your marketing with new AI tools

Learn how new AI and agentic experiences across Google Ads and Google Analytics can simplify your marketing workflow. The primary source at blog.google supports only these stated facts; unsupported specifications are deliberately omitted. The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment. Test the sourced change against one real workflow before depending on it.
```

---

## Chapters

- 00:00 — Intro: Qwen's 2.4T Open-Weight Model Lands on OpenRouter / NIST Asks How to Modernize the National Vulnerability Database / ChatGPT Desktop Finally Arrives on Linux
- 02:00 — Qwen's 2.4T Open-Weight Model Lands on OpenRouter
- 02:00 — NIST Asks How to Modernize the National Vulnerability Database
- 02:47 — ChatGPT Desktop Finally Arrives on Linux
- 03:59 — Jensen Huang Tops Glassdoor's 2026 Best CEOs List
- 04:52 — Research digest: AI Agents Falter When Work Spans Multiple Tools
- 05:49 — Grok 4.6
- 06:28 — Research digest: Drones that follow directions get better at improvising
- 07:27 — GitHub ships Agent Plugins 1.0 across VS Code, Copilot CLI, and the Copilot app
- 08:41 — OpenAI's enterprise study finds AI moving from chat to autonomous execution
- 10:03 — RingCentral puts ChatGPT Work and Codex inside its engineering and ops stack
- 11:48 — DeepMind puts sign language AI in users' hands
- 12:53 — llama.cpp
- 13:22 — Apple Silicon and macOS VMs: Faster LLM Inference with llama.cpp
- 13:52 — Evolve your marketing with new AI tools

---

## Primary Links

- Qwen: Qwen3.8 2.4T A95B model page: https://openrouter.ai/models/qwen/qwen3.8-2.4t-a95b
- DeepSeek: DeepSeek V4 Pro 0813 model page: https://openrouter.ai/models/deepseek/deepseek-v4-pro-0813
- NIST asks how AI should modernize the National Vulnerability Database: https://www.federalregister.gov/documents/2026/08/12/2026-16371/request-for-information-rfi-on-modernizing-the-national-vulnerability-database-in-the-age-of
- Muse Glimmer: 30B-parameter model optimized for always-on local agent : https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model
- ChatGPT Desktop (Codex Desktop) for Linux: https://openai.com/codex/
- meta-models/Muse-Glimmer-30B-GGUF trending on Hugging Face: https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF
- Lightricks/LTX-2.5 trending on Hugging Face: https://huggingface.co/Lightricks/LTX-2.5
- nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 trending on Hugging: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4
- NVIDIA CEO Tops Glassdoor’s 2026 List of Best CEOs: https://blogs.nvidia.com/blog/nvidia-life-glassdoor-best-ceo-2026/
- VAKRA: Evaluating Multi-Hop Reasoning Across APIs and Retrieval Under : https://arxiv.org/abs/2608.12282
- Grok 4.6: https://x.ai/news/grok-4-6
- Grok Bot: https://x.ai/bot
- DreamFly: Causal Memory and Receding-Horizon Diffusion Planning for Ae: https://arxiv.org/abs/2608.12308
- Agent Plugins 1.0 in VS Code, Copilot CLI, and the Copilot app: https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app
- From assistance to execution: How enterprises put AI to work: https://openai.com/index/how-enterprises-put-ai-to-work
- How RingCentral builds AI-native work from engineering to ops: https://openai.com/index/ringcentral
- Putting sign language AI into users’ hands: https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/
- MAI-Code-1.1-Flash available in GitHub Copilot: https://github.blog/changelog/2026-08-11-mai-code-1-1-flash-available-in-github-copilot
- Per-model token breakdown in the usage report: https://github.blog/changelog/2026-08-11-per-model-token-breakdown-in-the-usage-report
- Apple Silicon and macOS VMs: Faster LLM Inference with llama.cpp: https://github.com/trycua/cua/blob/main/blog/gpu-passthrough-macos-vms.md
- llama.cpp: https://llama.app
- Evolve your marketing with new AI tools: https://blog.google/products/ads-commerce/google-ads-analytics-ai-updates/
- HKUDS/nanobot repo: https://github.com/HKUDS/nanobot
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- Daybreak models are now available on AWS: https://openai.com/index/daybreak-models-are-now-available-on-aws
- meta-models/Muse-Glimmer-30B: https://huggingface.co/meta-models/Muse-Glimmer-30B

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.34`, published 2026-08-08T07:22:14Z. Recent episode version tags detected: `v2026.7.2-beta.2`, `v2026.7.2-beta.3`, `v2026.7.2-beta.5`, `v2026.7.2-beta.7`. No new stable release this cycle.
- **Hermes Agent** — Latest stable verified: `v2026.8.3`, published 2026-08-03T16:57:52Z. Recent episode version tags detected: `v2026.7.30`, `v2026.7.7`, `v2026.7.7.2`, `v2026.8.3`. No new stable release this cycle.
- **OpenAI Codex** — Latest stable verified: `rust-v0.147.0`, published 2026-08-07T01:41:49Z. Recent episode version tags detected: `rust-v0.145.0`, `rust-v0.146.0`, `rust-v0.146.1`, `rust-v0.147.0`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.223`, published 2026-08-05T22:51:13.206Z. Recent episode version tags detected: `2.1.220`, `2.1.221`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-08-13). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.34` (stable) / `v2026.7.2-beta.7` (prerelease)
- **Hermes Agent** — `v2026.8.3`
- **OpenAI Codex** — `rust-v0.147.0`
- **Claude Code CLI** — `2.1.223`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
