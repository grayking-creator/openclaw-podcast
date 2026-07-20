# AgentStack Daily EP089 — Kimi K3 at 2.8T params, Codebase Memory MCP trims tokens 99%

**Title:** Kimi K3 Lands at 2.8T Parameters, Pricing Stings

**Tagline:** Moonshot's Kimi K3 arrives at 2.8 trillion parameters with pricing that pressures Western frontier labs. Prism-ML's Ternary-Bonsai-27B trends on the leaderboards as a local-AI power move for resource-constrained setups. Codebase Memory MCP slashes coding-agent token consumption by 99%, reshaping how developers budget context. NVIDIA and Hugging Face publish a fine-tuning scaling guide for video and image models. Medicare's WISeR pilot places AI in prior-authorization workflows across six states. Research spotlights: LongStraw pushes RL training beyond two million tokens, while VideoChat3 advances open video models toward generalist use. Plus the Agent Stack Release Readout with Codex rust-v0.144.6, FastMCP 3.4.4, and Unity-MCP 10.1.0.

**Feed description:** Today's rundown: Moonshot ships Kimi K3 at 2.8 trillion parameters with steep pricing. Codebase Memory MCP reports a 99% drop in coding-agent token use. Prism-ML's Ternary-Bonsai-27B surges on the local-AI charts. Medicare's WISeR pilot puts AI agents in prior-authorization for six states. NVIDIA teams with Hugging Face on a fine-tuning scaling guide for video and image models. LongStraw and VideoChat3 push research boundaries. Plus the Agent Stack Release Readout covering Codex rust-v0.144.6, FastMCP 3.4.4, and Unity-MCP 10.1.0, and Microsoft's MCP for Beginners crossing 16,700 stars.

---

## Story Slate

1. **Agent Stack Release Readout: OpenAI Codex rust-v0.144.6**
OpenAI shipped Codex CLI rust-v0.144.6 on July 18 with a focused bug fix: bundled model metadata for the GPT-5.6 Sol, Terra, and Luna tiers has been refreshed, and their context windows are corrected to 272,000 tokens. The release lands two small backports from a single engineer and ensures Codex's internal view of these three model variants matches their real specs. For builders using GPT-5.6 inside Codex, this is a foundational correctness fix worth pulling before long sessions.
Technical depth angle: The harness shipped with stale bundled metadata for three GPT-5.6 tiers. The fix refreshes the instructions Codex injects for those models and aligns the reported context window to the true 272,000-token limit. A second PR narrowed the hotfix so only GPT-5.6 prompts and context were touched, leaving other model families on 0.144 unaffected.
Actionability angle: If you run Codex with a GPT-5.6 variant, pull rust-v0.144.6 and re-test a representative session before kicking off long refactors or multi-file migrations. Correct context numbers change how the agent plans and how much of your repo it can hold in working memory, so a short validation pass is worth the time.
Listener hook: If your coding agent thinks it has the wrong amount of memory, every long task is a gamble — this release ends that gamble for GPT-5.6.

2. **Moonshot drops Kimi K3 at 2.8T parameters — pricing stings**
Moonshot AI released Kimi K3 on July 16, 2026, calling it their most capable model yet at 2.8 trillion parameters — the first openly available model in what they call the 3-trillion class. It leapfrogs DeepSeek's 1.6T v4 Pro and leads Arena.ai's Frontend Code leaderboard. Pricing is $3 per million input and $15 per million output, matching Anthropic's Claude Sonnet tier and making it the most expensive Chinese model to date — a significant jump from K2.6's $0.95 and $4. Available now via Moonshot's website and API, with an open-weight release promised by July 27, 2026.
Technical depth angle: Kimi K3 ships with 2.8T parameters — more than double the 1T K2.6 and the largest openly available dense model so far. Independent testing on Artificial Analysis puts its long-horizon knowledge work Elo at 1547, a 732-point jump from K2.6 and second only to Claude Fable 5. K3 also uses 21% fewer output tokens than K2.6 on the Artificial Analysis Intelligence Index, partially offsetting its premium per-token pricing.
Actionability angle: Kimi K3 is live now through Moonshot's website and API, so builders can route long-context coding and reasoning tasks through it today. This release matters because it sets the new baseline for 'open 3T-class' capabilities, but the pricing shift signals that flagship-scale Chinese open-weights may no longer land at bargain rates. Watch the July 27 open-weight drop to see whether community deployment matches the API pricing or arrives with different terms.
Listener hook: The first openly available 3-trillion-parameter model just dropped from a Chinese lab — and the price tag is the most surprising part.

3. **Prism-ML's Ternary-Bonsai-27B Hits Trending as a Local-AI Power Move**
A model called Ternary-Bonsai-27B from publisher prism-ml is trending on the Hugging Face hub. The repository ships a 27-billion-parameter chat model in the GGUF format at 2-bit ternary precision, packaged for llama.cpp and tagged for CUDA and Metal hardware acceleration. It has pulled in over 338,000 downloads and 760-plus likes since appearing on July 4. The compression profile is the story: a 27B model at 2 bits per weight lands as a small downloadable artifact that can be loaded and talked to on consumer Nvidia GPUs, Apple Silicon laptops, and even CPU-only setups through llama.cpp. For hobbyists and agent builders, that puts a previously server-sized chat model within reach of an offline laptop run.
Technical depth angle: A 2-bit ternary quantization stores every weight as one of three values, collapsing file size compared with 4-bit or 8-bit GGUF variants. The GGUF container holds the quantized weights plus the metadata llama.cpp needs to load them on CUDA, Metal, or plain CPU. The trim profile is what lets a 27-billion-parameter chat model fit on a single consumer GPU or Apple Silicon laptop.
Actionability angle: For builders, this means you can pull a 27B chat model and run it on a MacBook or modest Nvidia card without renting a server, treating it as a drop-in local endpoint for prototypes and agent stacks. Watch how llama.cpp, Ollama, and other local runtimes integrate the ternary checkpoint, because the runtime layer decides whether the small footprint actually translates into fast tokens per second.
Listener hook: A 27-billion-parameter chat model is trending on Hugging Face because someone squeezed it down to 2 bits per weight and made it run on a laptop.

4. **Medicare's WISeR puts AI in prior-authorization for six states**
Medicare's WISeR Model, launched by CMS in January 2026 and running through December 2031, uses AI tools to screen selected Original Medicare services before payment in Arizona, New Jersey, Ohio, Oklahoma, Texas, and Washington. Six technology companies participate, one per state, with payments tied to the cost of care their reviews prevent. A licensed clinician must make every final denial recommendation, and emergency services, inpatient-only services, and care where delays pose patient risk are excluded. The central policy question is whether automated screening speeds decisions and reduces waste without rewarding aggressive denials or delaying necessary treatment.
Technical depth angle: The model routes a defined list of Original Medicare services — examples include skin and tissue substitutes, electrical nerve-stimulator implants, and knee arthroscopy for osteoarthritis — through AI-assisted screening before payment, with a licensed clinician required for every final non-payment recommendation. Vendor payments scale with expenditures the reviews avert, then adjust for process measures like provider experience, which is the structural feature worth tracking.
Actionability angle: For healthcare-adjacent builders and policy watchers, WISeR creates a live federal test bed for clinical prior-authorization AI. What this means: how the experience adjustment actually moderates the denial incentive will shape whether future public and commercial payers treat automated authorization as a template or a cautionary tale.
Listener hook: Medicare is now paying six AI vendors based on how much spending their reviews block, and the part worth watching is what happens when appeals and provider-experience scores start landing.

5. **NVIDIA and Hugging Face publish a scaling guide for fine-tuning video and image models**
Hugging Face and NVIDIA posted a joint blog on July 17, 2026, walking through how to fine-tune video and image generation models at scale using NVIDIA's NeMo Automodel alongside the Hugging Face Diffusers library. The post is framed as a practical guide for teams that want to customize diffusion models without writing custom training loops from scratch.
Technical depth angle: The guide pairs NVIDIA's NeMo Automodel with Hugging Face's Diffusers library, framed as a workflow for scaling diffusion model fine-tuning across video and image tasks. Specific supported model families, parameter counts, and benchmark numbers are not provided in the headline announcement.
Actionability angle: This is most useful for teams already running on NVIDIA hardware who want a documented path to fine-tune diffusion models. Why this matters: it lowers the barrier to customizing video and image generators at scale. The guide is the natural entry point for anyone considering a fine-tuning run before committing GPU time.
Listener hook: If fine-tuning your own video or image model felt out of reach, this is a new on-ramp worth a look.

6. **Research digest: LongStraw Pushes RL Training Past 2M Tokens**
LongStraw is a new execution stack that lets reinforcement-learning post-training run over context windows beyond two million tokens while staying within a fixed GPU budget. It targets the widening gap between long-context inference, which already handles around a million tokens, and post-training, which often maxes out at 256K. For AI agents that accumulate tool outputs, documents, and prior decisions over long trajectories, training on shorter windows than deployment creates a real mismatch. LongStraw was highlighted on the HuggingFace daily papers feed, signaling community interest in closing that gap for agent training.
Technical depth angle: LongStraw is an architecture-aware execution stack that fits million-token reinforcement-learning post-training into a fixed GPU budget. It closes the gap between long-context inference and short-context training, so agents can be trained on the full length of trajectories they actually face in production rather than shortened proxies.
Actionability angle: This matters because the gap between training and inference context has been a quiet ceiling on long-horizon agent quality. Agent teams who currently cap training at 256K tokens may see a near-term path to million-token trajectories without new hardware. The next signal is adoption inside the major open RL frameworks.
Listener hook: If you've ever wondered why AI agents seem to lose track of things halfway through a long task, this is about closing that gap at the training step.

7. **Research digest: VideoChat3 Pushes Open Video AI Toward True Generalist Use**
A new paper called VideoChat3 is trending on HuggingFace's daily feed for tackling two stubborn problems in video AI at once: closed models that lock out small teams, and open models that only work on narrow video types. The team released a fully open multimodal model — meaning weights and key training components — that claims to handle motion, long videos, and streaming input without needing separate specialist versions. The pitch is generalist capability plus lower compute demands, so a developer could adapt one base model to sports footage, cooking clips, or security feeds rather than stitching together domain-specific tools. If community testing bears it out, it lowers the bar for anyone who wants to build video understanding into their own product without paying API fees or sending data to a third party.
Technical depth angle: VideoChat3 is a multimodal model trained to handle diverse video inputs — short clips with motion, long-form footage, and live streaming — within a single architecture rather than separate specialist models. The fully open release means weights and training data components are available, addressing the common complaint that open video models keep their most useful pieces behind closed doors. The efficiency claim targets lower compute demands than comparable open models, which is the practical barrier for running this kind of system outside a data center.
Actionability angle: For builders, fully open video models with generalist capability mean you can prototype video understanding on your own footage without paying per-call API fees or sending sensitive video to a third party. Why this matters: smaller teams can experiment with adaptations for specific verticals like sports analytics, security, or education using one base model rather than assembling a stack of narrow tools. The community adoption on real production footage will be the real test, since benchmark numbers and live usability often diverge.
Listener hook: Most open video AI is either locked up or only works on one type of clip — this paper claims to fix both at once.

8. **Codebase Memory MCP Cuts Coding Agent Token Use by 99%**
DeusData released v0.9.0 of codebase-memory-mcp on July 8, an MCP server that turns a software repository into a persistent knowledge graph an AI agent can query in under a millisecond. The single static binary supports 158 programming languages, indexes an average repo in milliseconds, and claims to use 99% fewer tokens than feeding raw source into a model's context window. The repository now sits at 32,815 GitHub stars.
Technical depth angle: The server pre-indexes a repository into a persistent knowledge graph, then serves sub-millisecond lookups over MCP. That replaces "paste code into chat" with "agent asks targeted questions," which keeps prompts short and avoids burning context on irrelevant files. The 99% token reduction claim is the headline mechanism, since context budget is the real bottleneck for long agent runs.
Actionability angle: This matters because context-window pressure is the most common reason a coding agent loses the plot on a large repository — short prompts and focused lookups keep multi-file tasks coherent. For builders, the win is a workflow where the assistant navigates code by query rather than by copy-paste, which changes how long-running agent jobs feel on real projects. The 99% token-savings figure is the headline, but it's worth waiting for third-party benchmarks before committing a serious workflow to it.
Listener hook: If your coding agent keeps running out of context halfway through a task, a 99% drop in token use might be the fix you can install this weekend.

9. **FastMCP v3.4.4 lands as Python's go-to MCP server builder**
FastMCP, the Python library for building MCP servers and clients maintained under the PrefectHQ organization, hit v3.4.4 on July 9, 2026. The repository now sits at 26,263 GitHub stars and was actively pushed again on July 19. MCP — the Model Context Protocol — is the open standard that lets AI assistants call external tools, files, and data sources. FastMCP aims to be the fastest, most idiomatic Python toolkit for publishing those endpoints without hand-rolling protocol plumbing, and the v3.x line is now a default starting point for Python teams wiring internal APIs and databases into the agent stack.
Technical depth angle: FastMCP is the Python library for the Model Context Protocol. Instead of writing raw protocol messages, schemas, and transport plumbing by hand, Python developers use FastMCP to expose functions, datasets, and scripts as MCP servers that any compliant AI client can discover and call.
Actionability angle: Python teams now have a well-supported default for wiring internal APIs, databases, and local scripts into AI agents without rebuilding the protocol layer each time. It matters because every agent project that needs to call external systems hits the same MCP-boilerplate wall, and FastMCP's star count and active release cadence put it past the threshold where it's safe to depend on. For anyone shipping a Python service that an MCP-aware assistant should reach, FastMCP is the path of least resistance.
Listener hook: If you've ever tried to wire a Python service into an AI agent and gotten lost in protocol boilerplate, FastMCP v3.4.4 is the project that finally makes that path feel normal.

10. **Microsoft's MCP for Beginners curriculum crosses 16,700 GitHub stars**
Microsoft's open-source MCP for Beginners curriculum teaches developers the Model Context Protocol, the emerging standard that lets AI assistants connect to external tools and data. The free course ships working examples in .NET, Java, TypeScript, JavaScript, Rust, and Python, and focuses on building modular, scalable, and secure AI workflows. It now sits at over 16,700 GitHub stars after a repository push on July 17, with the lessons evolving as the protocol itself matures.
Technical depth angle: MCP is essentially a universal plug standard for AI: it defines how a model can call external tools and pull in structured context the same way regardless of which language or framework you use. The curriculum teaches you to build servers and clients that follow this protocol, with concrete examples in six languages and a focus on modular, scalable, and secure patterns.
Actionability angle: This means a developer who already knows one of the six covered languages can pick up MCP without a context-switch, and any integration built against the curriculum's patterns stays portable because MCP is a shared standard. Why this matters: this is one of the most-starred MCP teaching resources on GitHub, and the practical patterns it teaches — modular structure, hardened boundaries, room to scale — translate directly into production-ready integrations.
Listener hook: Microsoft's free, multi-language MCP curriculum just passed 16,700 stars — a structured, code-first way for builders to learn the protocol connecting AI to other software.

11. **mcp-use crosses 10,000 GitHub stars as a fullstack MCP app framework**
mcp-use, an open-source fullstack framework for building Model Context Protocol apps and servers, just passed 10,000 GitHub stars at 10,328. The latest release, version 1.34.3, shipped on July 8, 2026, with the repository getting fresh pushes as recently as July 19. It targets builders who want to ship MCP-compatible apps for ChatGPT and Claude, plus standalone MCP servers for AI agents. The framework handles both client and server sides, so a single project can publish capabilities for compliant assistants and embeddable chat-surface widgets.
Technical depth angle: mcp-use is a fullstack framework for the Model Context Protocol — the open standard that lets AI assistants call external tools. A single project can publish an MCP server, which any compliant agent can connect to, and an MCP app, which renders as buttons, cards, or widgets inside ChatGPT and Claude. That collapses the usual split between 'build a server' and 'build a chat-app UI' into one codebase.
Actionability angle: What this means: if you already build MCP tools or data connectors for Claude or ChatGPT, mcp-use gives you one project that publishes both a server for any agent and a chat-surface app at the same time. Builders who have been hand-rolling separate server and front-end codebases can collapse that work into a single repo. The reason to look now is that the framework has cleared 10,000 stars and is shipping regular 1.x releases, which signals a real community rather than a one-off demo.
Listener hook: If you've ever wished you could ship one project that works as both an MCP server for any agent and an app inside ChatGPT or Claude, mcp-use just cleared 10,000 stars.

12. **GitHub Copilot usage metrics now break down per repository**
GitHub has moved repository-level Copilot usage metrics to general availability. Two new REST API endpoints return a daily per-repository breakdown of pull request activity for the Copilot coding agent and Copilot code review, letting teams finally see which repos actually get AI assistance and which ones never see a touch.
Technical depth angle: Two new REST endpoints on the Copilot usage metrics API return daily counts of pull requests touched by the Copilot coding agent and Copilot code review, now scoped to a single repository instead of aggregating at the organization level. Daily time series make per-repo trend charts straightforward.
Actionability angle: Engineering leaders can now attribute Copilot pull request activity to specific repositories rather than averaging across an org, which makes it easier to spot underused teams or repos that quietly became AI-heavy. Why this matters: the data lands as plain REST, so wiring it into an existing dashboard is an afternoon project rather than a custom pipeline.
Listener hook: If you have ever wondered which of your repos is actually using Copilot, GitHub just handed you the receipts.

13. **Unity-MCP 10.1.0 turns your editor into a callable tool surface**
Unity game developers just got a more capable AI co-pilot inside the editor. CoplayDev shipped version 10.1.0 of unity-mcp on July 13, a community-maintained Model Context Protocol bridge that lets large language models manage assets, control scenes, edit scripts, and automate tasks directly inside the Unity Editor. The repository has grown to 12,645 GitHub stars, and the release landed alongside a same-day code push, signaling that MCP-style tooling for game engines is moving from clever demo into everyday workflow.
Technical depth angle: The Model Context Protocol is the same standard that lets assistants call external tools, and unity-mcp uses it to expose Unity's editor functions as callable endpoints. Once wired, an assistant can read project state, mutate scenes and scripts, and trigger editor workflows, replacing copy-paste guessing with real read and write access to the engine.
Actionability angle: For Unity developers, this means AI assistance that actually touches the editor rather than guessing at your project structure. Solo developers and small teams gain faster asset hygiene and scene cleanup, and larger studios should consider prompt governance now that assistants can move scenes and scripts directly.
Listener hook: If you've ever pasted a script back and forth between chat and Unity wondering why the assistant keeps getting your scene wrong, this one's for you.

14. **OpenAI's CFO publishes a four-metric scorecard for AI ROI**
OpenAI CFO Sarah Friar published an AI scorecard on July 17 that measures return on investment through four lenses: useful work, cost per successful task, dependability, and return on compute. The piece reframes AI deployment as a capital project requiring the same line-item discipline as any other infrastructure spend, aimed at finance and procurement teams rather than researchers. It offers a framework, not a benchmark, leaving reference numbers for vendors and analysts to publish later.
Technical depth angle: The scorecard's central move is replacing benchmark scores and token counts with four operational metrics any team can log per project: completed tasks, dollars per successful task, first-attempt accuracy, and useful output per compute dollar. That shift makes AI evaluation vendor-neutral across hosted models, self-hosted weights, and third-party APIs, because all four numbers can be measured without reference to a specific model family.
Actionability angle: For builders and team leads, the scorecard functions as a procurement checklist and a retrospective template, since logging the four numbers per project this quarter reveals which tools earn their seat. What this surfaces is that most pilots underestimate the hidden labor of redoing unreliable AI output, which only becomes visible once dependability is measured as a line item alongside cost.
Listener hook: If you've ever wondered whether your AI subscription actually earns its monthly fee, OpenAI's CFO just published a four-question scorecard you can run this quarter.

---

## Editorial Mix Check

- flagship_products: 3
- builder_projects: 8
- local_ai: 2
- hardware_compute: 2
- policy_regulation: 1
- research: 2

---

## Model Discovery Check

- **Model lanes scanned** (OpenRouter major providers) — No new or materially updated models detected this cycle (verified July 19, 2026). Primary source: https://openrouter.ai/models. Decision: Not Selected — no new model candidates to evaluate for the Story Slate this cycle.

---

## Local LLM Spotlight

- **thinkingmachines/Inkling** — https://huggingface.co/thinkingmachines/Inkling — Inkling is a trending open weights model from thinkingmachines that handles image-text-to-text and audio-text-to-text in a single mixture-of-experts checkpoint, published under Apache-2.0. The repo ships eval results and an endpoints_compatible flag, so you can load it through the Hugging Face stack or hit it via Inference Endpoints with the same client code. It pulled in 1,094 likes and 13,462 downloads in its early window, which is what pushed it into trending.
  Try now: Pull the safetensors checkpoint into a local transformers pipeline, pass it an image plus a short audio clip, and compare its grounded answer against a text-only baseline on three of your own UI screenshots.

---

## GitHub Project Radar

- **CoplayDev/unity-mcp** — https://github.com/CoplayDev/unity-mcp — Unity MCP exposes the Unity Editor to LLM clients as a Model Context Protocol server, letting an agent move scenes, edit scripts, and batch asset operations through structured tool calls. `stars: 12,645`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v10.1.0 (2026-07-13)`.
  Why this is on the radar now: v10.1.0 shipped on 2026-07-13 and the repository was updated on 2026-07-13.
  Stack improvement angle: Wiring Unity MCP behind an OpenClaw or Claude Code session turns a chat into a hands-on game dev loop where the agent can read the scene graph, write C#, and trigger Editor actions without a human clicking menus.
  Try now: Run the Unity MCP server inside a sample Unity 6 project and ask Codex to rename a UI canvas, re-save its prefab, and verify the change via the exposed editor tools.

- **lastmile-ai/mcp-agent** — https://github.com/lastmile-ai/mcp-agent — MCP-Agent is a Python framework that wraps Model Context Protocol servers into reusable agents with deterministic workflow primitives like parallel, route, and orchestrator patterns. `stars: 8,430`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v0.0.21 (2025-05-09)`.
  Why this is on the radar now: v0.0.21 shipped on 2025-05-09 and the repository was updated on 2026-01-25.
  Stack improvement angle: Dropping it inside a Hermes or Claude Code pipeline gives you composable, typed agent graphs instead of hand-rolled tool loops, so multi-server MCP fan-out becomes a single declarative step.
  Try now: Define a ParallelAgent that fans out across two MCP servers and time it against your current sequential tool-call loop on a fixed 10-step task.

- **Upsonic/Upsonic** — https://github.com/Upsonic/Upsonic — Upsonic is a Python SDK for building autonomous agents with first-class support for tool use, task graphs, and a built-in evaluation harness. `stars: 7,915`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v0.77.3 (2026-05-19)`.
  Why this is on the radar now: v0.77.3 shipped on 2026-05-19 and the repository was updated on 2026-06-18.
  Stack improvement angle: Pairing Upsonic's task graph runtime with Codex-style code generation gives the agent a real evaluation step per iteration, so prompt tweaks are graded against concrete pass/fail criteria rather than vibes.
  Try now: Pick one of your agent's existing tasks and re-run it inside Upsonic's eval harness to compare latency and tool-call count against your current baseline.

---

## Extra Research Candidates

- **Repository-level GitHub Copilot usage metrics generally available** — https://github.blog/changelog/2026-07-17-repository-level-github-copilot-usage-metrics-generally-available — The Copilot usage metrics REST API now reports repository-level activity. Two new endpoints return a daily, per-repository breakdown of pull request activity for Copilot coding agent and Copilot code review.&#8230; The post Repository-level Technical depth angle: The Copilot usage metrics REST API ships two new endpoints that return a daily, per-repository breakdown of pull request activity for Copilot coding agent and Copilot code review, enabling org-level dashboards over a fixed window of days.

- **Why teens deserve access to safe AI** — https://openai.com/index/why-teens-deserve-access-safe-ai — Learn how OpenAI is making ChatGPT safer for teens with age-appropriate protections, learning tools, parental controls, and expert partnerships. Technical depth angle: OpenAI layers age-appropriate model behavior, a parental control API, and third-party expert review boards on top of ChatGPT's existing safety stack rather than shipping a new model class, with the controls exposed as account-level toggles.

- **appcypher/awesome-mcp-servers — Awesome MCP Servers - A curated list of Model Context Protocol servers** — https://github.com/appcypher/awesome-mcp-servers — Awesome MCP Servers - A curated list of Model Context Protocol servers GitHub reports 5699 stars. Latest release: no tagged release . Repository pushed 2026-05-06T08:04:35Z. Technical depth angle: awesome-mcp-servers is a curated index of MCP server implementations grouped by integration domain, useful as a discovery layer when you need a server that already wraps a specific external API.

---

## Show Notes

```md
Episode 089 — July 19, 2026

[00:00] Episode hook

Moonshot AI released Kimi K3 on July 16, 2026, putting a 2.8-trillion-parameter open model in front of developers for the first time — the first openly available release that breaks into the 3-trillion class. The pricing is the part that stings: Moonshot is asking for a premium that puts K3 firmly above peers, and early benchmarks suggest it leapfrogs prior open-weight frontier contenders. Pricing details are still trickling in across API tiers. Separately, OpenAI shipped Codex CLI rust-v0.144.6 on July 18, a focused bug fix that refreshes bundled model metadata for the GPT-5.6 Sol, Terra, and Luna tiers and corrects their context windows. And on Hugging Face, prism-ml's Ternary-Bonsai-27B is climbing the trending list — a 27-billion-parameter chat model shipped in GGUF at 2-bit ternary precision, aimed at local inference budgets.

[02:00] Agent Stack Release Readout: OpenAI Codex rust-v0.144.6

OpenAI pushed a small but foundational bug fix to its Codex CLI this week: rust-v0.144.6 landed on July 18 and tightens up the bundled metadata for three GPT-5.6 model tiers — Sol, Terra, and Luna. The fix corrects their context windows to 272,000 tokens and refreshes the bundled instructions that ship with the harness.

That matters because Codex is a coding agent, and an agent that thinks it has more context than it actually does — or less — can quietly misbehave. If the harness claims a 200K window but the real model supports 272K, builders leave usable space on the table. If the harness claims 400K but the model is capped at 272K, the agent will silently truncate long sessions or refuse work that should comfortably fit. Either direction is a footgun. This release lands both sides in the same place, which is what you want from a metadata refresh.

The change came in two pull requests from the same engineer. The first backported refreshed bundled model metadata into the 0.144 line. The second narrowed the hotfix specifically to GPT-5.6 prompts and context, so other model families on the same release stay untouched. For anyone running Codex with a GPT-5.6 variant in production today, this is exactly the kind of update worth pulling before kicking off long-running refactors or multi-file migrations, where the difference between a 200K and a 272K window can mean the agent finishes in one pass instead of stalling out mid-task.

For builders, the practical takeaway is straightforward. If you pin Codex in scripts or CI, bump the version and re-run one representative session to confirm the agent now behaves the way the official GPT-5.6 specs describe. The context number is a real input into how the agent plans, what it can hold in working memory, and how much of your repository it can reason over at once. Worth one line in your release notes, worth a few minutes of testing.

What to watch next: any follow-up patch extending the metadata refresh to other model families on the 0.144 line, or a 0.145 release that consolidates these fixes into a broader drop.

[03:26] Moonshot drops Kimi K3 at 2.8T parameters — pricing stings

Moonshot AI dropped Kimi K3 this morning, and the headline number is 2.8 trillion parameters — the first openly available model in what they're calling the 3-trillion class. To put that in perspective, that's more than double their previous K2.6, and it leapfrogs DeepSeek's 1.6-trillion v4 Pro to claim the open-weight crown by a wide margin.

The bench results are eye-catching. On Artificial Analysis's private long-horizon knowledge work test, K3 scores a benchmark Elo of 1547 — a 732-point jump from K2.6, and second only to Claude Fable 5. It also just took the top spot on Arena.ai's Frontend Code leaderboard, beating Claude Fable 5 in an arena that measures how well models build real-looking web interfaces. Self-reported numbers from Moonshot show K3 beating Claude Opus 4.8 max and GPT-5.5 high, while still trailing Claude Fable 5 and GPT-5.6 Sol.

But here's the catch that actually matters for builders: pricing is $3 per million input tokens and $15 per million output. That puts K3 at the same tier as Anthropic's Claude Sonnet — and makes it the most expensive model a Chinese lab has shipped, a significant jump from K2.6 at $0.95 input and $4 output. On Artificial Analysis's per-task view, K3 lands at $0.94 per task, similar to GPT-5.6 Sol's $1.04 and about half of Opus 4.8's $1.80, though still higher than open-weight peers. The silver lining: K3 uses 21% fewer output tokens than K2.6 on their intelligence index, so the bill grows more slowly than the per-token rate suggests.

You can try it now through Moonshot's website or API, with an open-weight drop promised by July 27. The thing to watch is whether that open release keeps the same pricing math — or whether that's what the community actually gets to run.

[05:17] Prism-ML's Ternary-Bonsai-27B Hits Trending as a Local-AI Power Move

A model called Ternary-Bonsai-27B landed on the Hugging Face trending list on July 4, and the reason it is pulling numbers is the compression. Prism-ML shipped a 27-billion-parameter chat model in the GGUF format with weights stored at 2-bit ternary precision, packaged for llama.cpp and tagged for CUDA and Metal acceleration. It has already cleared 338,000 downloads and 760 likes on the hub.

The headline mechanic is the quantization itself. A 2-bit ternary scheme stores every weight as one of three values, which collapses the file size compared with typical 4-bit GGUF builds of similar models. Stacked together with the conversational fine-tuning the repo is tagged for, that gives builders a chat-ready 27B that fits as a downloadable artifact you can load on a single consumer Nvidia GPU, an Apple Silicon MacBook, or even a CPU-only machine through llama.cpp. The tags on the repo make that explicit.

The community volume signals fast adoption. Local-AI tinkerers watch the trending list for exactly this kind of drop: a model big enough to feel substantial, but small enough that it does not need a rented cluster. For agent builders, the practical pitch is a single local chat endpoint you can swap into a stack without paying per token, and for hobbyists it is a way to keep a capable model running entirely offline.

A few things to watch next: how llama.cpp and Ollama handle the ternary weights on real hardware, whether derivative quants at neighboring precisions appear in the same repo, and how the model's conversation quality holds up against standard 4-bit baselines once head-to-head reviews start landing. If quality holds and the small footprint translates into fast tokens per second, this is the kind of drop that quietly resets expectations for what "local" means.

[07:08] Medicare's WISeR puts AI in prior-authorization for six states

Medicare just put AI inside the prior-authorization desk for some Original Medicare services, and the program is now active in six states. The WISeR Model, which CMS launched in January 2026, runs through December 2031 in Arizona, New Jersey, Ohio, Oklahoma, Texas, and Washington. Six technology companies are participating, one per state, and their payments are tied to the cost of care their reviews prevent.

Here's the concrete change: for a chosen list of services with established coverage criteria and high risk of waste, fraud, or harm, AI tools screen claims before payment. Examples include skin and tissue substitutes, electrical nerve-stimulator implants, and knee arthroscopy for osteoarthritis. Emergency cases and inpatient-only services are excluded, as are situations where a delay would risk patient harm. And crucially, a licensed clinician must make every final recommendation to deny payment. The AI surfaces the case; a human signs off.

Providers can request prior authorization before performing a service, or face pre-payment review after delivery. Providers who stay compliant over time may qualify for a gold-card exemption that skips the review entirely. Coverage rules don't change, Medicare Advantage isn't touched, and beneficiaries keep their choice of Original Medicare provider.

The incentive structure is the part to watch. CMS pays participating vendors based on expenditures their reviews avert, then adjusts that figure for process measures like provider experience. In plain English: the companies earn more when their AI flags more questionable services, so the design has to prove it isn't rewarding aggressive denials or slowing down necessary care. Treat the promised faster decisions and lower costs as goals that need evidence over six years, not as demonstrated outcomes. Watch the first round of appeals data and provider-experience scores; that will be the earliest real signal of whether this actually works.

[08:59] NVIDIA and Hugging Face publish a scaling guide for fine-tuning video and image models

On July 17, Hugging Face and NVIDIA published a joint blog titled 'Fine-tune video and image models at scale with NVIDIA NeMo Automodel and 🤗 Diffusers.' The post is positioned as a practical guide for teams that want to customize diffusion models — the class of generative systems behind most current image and video tools — using infrastructure from both companies working together.

The combination centers on two named pieces: NVIDIA's NeMo Automodel and Hugging Face's Diffusers library. The blog frames the workflow as a way to scale fine-tuning for video and image generation without writing a custom training loop from scratch. That framing matters because fine-tuning video models has historically been a heavy compute lift, and documented recipes have been thin.

For builders, the practical question is what this unlocks today. The blog is a starting point — it does not announce a new model, a new chip, or a hosted service. It is a write-up of how the two stacks can be wired together, with the goal of making large-scale fine-tuning more reproducible for the open community.

One reason this kind of guide lands now: the open-source diffusion ecosystem has matured enough that training code is no longer the bottleneck. Knowing which knobs to turn and how to distribute the workload across GPUs is. Tutorials that document those choices in one place tend to save teams weeks of trial and error.

What to watch next: follow-up posts that name specific supported model families, real benchmark numbers on multi-GPU runs, and any community reproductions. Until those appear, the safest read is that this is a documentation milestone, not a product launch — useful for teams already planning fine-tuning work, and worth a bookmark for everyone else.

[10:47] Research digest: LongStraw Pushes RL Training Past 2M Tokens

Today's research highlight is LongStraw, a new system that lets teams train AI agents with reinforcement learning over context windows past two million tokens — without needing more GPUs than they already have.

Here's the gap it tries to close. Modern inference systems can already handle conversations and documents around a million tokens long. But the training step that teaches agents via reinforcement learning has lagged, often topping out at 256K tokens. For AI agents that juggle long streams of tool calls, documents, and prior decisions, that mismatch matters — you're training on a much shorter memory than the agent will eventually use at runtime.

LongStraw is an architecture-aware execution stack that fits million-token reinforcement-learning post-training into a fixed GPU budget. Think of it as a way to train agents on the kind of sprawling, multi-step trajectories they actually face in production, not on shortened proxies.

What to watch: how quickly the open-source release lands inside the major RL training frameworks, and whether agent labs adopt million-token training as the new default.

[11:52] Research digest: VideoChat3 Pushes Open Video AI Toward True Generalist Use

Video understanding models keep getting better, but there's a catch: most are either locked behind corporate walls or only work well on one type of video. A new paper called VideoChat3, trending on HuggingFace's daily feed, tries to fix both problems at once. The team built a fully open multimodal model that can handle motion, long videos, and streaming input without needing separate specialist versions. In plain English, that means the same model can watch a sports highlight, a cooking tutorial, and a security camera feed and actually understand what's happening in each.

Why it matters: open weights plus open training data means a small team can fine-tune it on their own footage without paying API fees or sending video to a third party. The efficiency angle is the second hook — the paper claims lower compute demands than comparable open models, which matters when you're running it on a workstation GPU rather than a data center.

What to watch: how it holds up on real-world video outside the benchmarks, and whether the community actually picks it up for adaptations.

[13:00] Codebase Memory MCP Cuts Coding Agent Token Use by 99%

A new MCP server called codebase-memory-mcp dropped version 0.9.0 on July 8, and it tackles one of the biggest friction points in AI-assisted coding: giving a model fast, cheap access to your whole codebase. DeusData built it as a single static binary with zero dependencies — you drop it on a machine and it indexes an average repository into a persistent knowledge graph in milliseconds. Once indexed, queries return in under a millisecond across 158 programming languages, and the server claims it uses 99% fewer tokens than feeding raw source into a model's context window.

In plain English, MCP is the protocol that lets an AI assistant call external tools, so this server becomes a tool the agent can ring up whenever it needs to know something about your code. That flips the workflow: instead of pasting files into a chat, an agent can ask the server "where is authentication handled?" or "which functions call this API?" and get a focused answer without dragging thousands of lines of source through the model. For a developer wiring this into any MCP-capable coding agent, the day-to-day change is less copy-pasting snippets and more letting the assistant navigate the repo the way a human would — just faster, and without burning context budget on irrelevant files.

The repository now sits at 32,815 GitHub stars, the binary installs without a runtime to manage, and the v0.9.0 release landed about two weeks ago. Worth watching next: how well the knowledge graph holds up on multi-million-line monorepos, and whether the 99% token-savings claim survives third-party benchmarks. But for anyone whose coding agent keeps running out of context halfway through a task, this is the kind of plumbing worth a weekend install.

[14:48] FastMCP v3.4.4 lands as Python's go-to MCP server builder

FastMCP v3.4.4 dropped on July 9, and the Python library for building MCP servers and clients is now sitting at 26,263 GitHub stars. For context, MCP — the Model Context Protocol — is the open standard that lets AI assistants reach out and call external tools, files, and data sources as if they were native features. FastMCP, maintained under the PrefectHQ organization, is the Python-side toolkit that makes publishing those endpoints feel like writing any other service, and the project bills itself as the fast option as well as the idiomatic one.

The whole point is reducing friction. Instead of hand-rolling protocol messages, schemas, and transport plumbing, a Python developer can use FastMCP to expose a function, a dataset, or a script as an MCP server that any compliant AI client can discover and call. The tagline calls it 'Pythonic,' meaning the library aims to fit the way Python developers already write code rather than imposing a foreign structure. That lowers the activation energy for wrapping internal systems.

The release cadence tells a story. v3.4.4 shipped July 9, and the repository was actively pushed again on July 19. That's not a dormant project. With 26,263 stars, FastMCP has become one of the default starting points for Python teams who want their internal APIs, databases, or local scripts to be reachable from AI agents without rebuilding the wiring each time.

What to watch next: how v3.x evolves, and whether the MCP client side of the ecosystem grows to match the server-side ergonomics FastMCP is shipping on the Python side. The protocol is open, the server tools are maturing, and Python teams now have a well-trodden path into the agent stack.

[16:33] Microsoft's MCP for Beginners curriculum crosses 16,700 GitHub stars

Microsoft's "MCP for Beginners" curriculum has become one of the more popular teaching resources on GitHub, sitting at over 16,700 stars after a repository push on July 17. It's a free, open-source course that walks developers through the Model Context Protocol — the emerging standard that lets AI assistants connect to external tools and data in a predictable, structured way. Think of MCP as a universal plug: instead of writing a custom integration every time you want a model to read a file, query a database, or call an API, you build one MCP server following a common standard so different AI clients can talk to it the same way. Build the connector once, and any AI client that speaks the same protocol can use it.

What makes the curriculum distinctive is its language breadth. Microsoft ships working examples in .NET, Java, TypeScript, JavaScript, Rust, and Python, so a developer can stay inside the stack they already know rather than picking up a new framework just to follow along. The lessons focus on practical techniques for building modular, scalable, and secure AI workflows — meaning you learn patterns for keeping server components small and reusable, hardening the boundaries around what an AI is allowed to touch, and structuring things so additional tools can be added without rewriting earlier work.

The practical value is straightforward: a developer who already knows one of the six covered languages can pick up MCP without a context-switch, and the resulting integrations follow patterns designed to scale as more tools get added. Because the lessons are open source, teams can also fork the curriculum and tailor it for internal training programs.

One thing to watch: the curriculum lives in a fast-moving repository without versioned releases, so lesson structure can shift between visits. Worth pinning a specific commit if you're using it as a long-term reference for production work.

[18:31] mcp-use crosses 10,000 GitHub stars as a fullstack MCP app framework

A fullstack framework for building Model Context Protocol apps just crossed 10,000 GitHub stars. The open-source project mcp-use, sitting at 10,328 stars, shipped release 1.34.3 on July 8, with the repository getting fresh pushes as recently as July 19. That combination of community size and recent activity is the kind of signal that turns a weekend prototype into something a team can build on.

So what is it, in plain terms. The Model Context Protocol, or MCP, is the open standard that lets AI assistants call external tools and pull live data without a custom integration for every model. Most MCP projects stop at the server side — you expose some capabilities, an agent discovers them, and the conversation continues. mcp-use is built to do both sides at once. The same project can publish an MCP server that any compliant agent can connect to, and ship an MCP app — the buttons, cards, and widgets that show up inside ChatGPT or Claude when the assistant decides to use your tool.

That dual-targeting matters because builders have been quietly complaining about the same gap for months: you write the server, then you write a separate chat-app front-end, then you keep both in sync. A single mcp-use project collapses that into one codebase, with the framework handling the protocol plumbing and the chat-surface rendering side by side. In practice, a builder writing a connector only has to maintain one project, and updates land in both the server and the chat-surface widget at the same time.

The thing to watch next is how far Anthropic and OpenAI push their in-chat app surfaces. mcp-use is already shaped for both, so any expansion on either platform should land there without a rewrite.

[20:19] GitHub Copilot usage metrics now break down per repository

GitHub Copilot usage metrics just became meaningfully more useful for teams running the assistant across more than a handful of repositories. On July 17, GitHub moved repository-level usage metrics to general availability, adding two new endpoints to the Copilot usage metrics REST API. Each one returns a daily, per-repository breakdown of pull request activity tied to Copilot coding agent and Copilot code review.

Until now, that same API surface only aggregated at the organization level. A large engineering org could see that Copilot touched a lot of pull requests last week, but could not easily tell whether all of that work concentrated in three repos while many others sat quiet, or whether adoption spread evenly. The new endpoints close that gap by returning a daily time series scoped to a single repository, so teams can chart adoption trends per repo instead of inferring them from an org-wide average.

Practically, this is the data engineering leaders have wanted since the coding agent shipped. You can compare repos side by side, see whether code review coverage is climbing in one service but flat in another, and answer the basic question of where Copilot is actually moving pull requests and where it is not. Because the endpoints are plain REST, integration into an existing dashboard, whether that is a Grafana panel, an internal metrics page, or a weekly leadership summary, is a straightforward afternoon project rather than a custom data pipeline — and the per-repository cuts make it possible to flag the long tail of repos where adoption never took hold at all.

One thing to watch next: GitHub has historically expanded the usage metrics surface in waves, and per-repository is the first cut. Whether seat-level counts, language breakdowns, or acceptance-rate cuts arrive in the same shape will determine how far teams can take this beyond a basic adoption chart.

[22:15] Unity-MCP 10.1.0 turns your editor into a callable tool surface

Unity game developers just got a more capable AI co-pilot inside the editor. CoplayDev shipped version 10.1.0 of unity-mcp on July 13, the bridge that lets large language models talk directly to the Unity Editor through the Model Context Protocol, the same standard increasingly used to wire assistants into development tools.

In plain terms, this means you can hand a coding assistant something better than a screenshot and a prayer. The bridge exposes Unity itself as a callable tool surface, so your assistant can manage assets, control scenes, edit scripts, and automate tasks. In practice that means listing and renaming files, querying and modifying scene objects, reading and writing C# scripts on GameObjects, firing menu commands, and triggering common editor workflows like reimporting assets or capturing screenshots for inspection. The assistant stops guessing at your project structure and reads it instead.

The repository sits at 12,645 stars on GitHub, and the latest push landed the same day as the release. That velocity from a community-maintained project is a signal that MCP-style tooling for game engines is shifting from clever demo into everyday workflow.

For solo developers and small teams, the practical change is that asset hygiene, scene cleanup, and routine refactors stop eating evenings. You describe what you want in chat, review the actions the assistant proposes inside Unity, and ship. For larger studios, the watch item is governance, because once an assistant can manipulate scenes and scripts, the question of who can prompt what moves from theoretical to operational.

Next up worth tracking: whether Unity's own first-party AI features and unity-mcp converge or compete, since two paths into the same editor rarely stay parallel for long.

[23:59] OpenAI's CFO publishes a four-metric scorecard for AI ROI

OpenAI's CFO Sarah Friar published an AI scorecard on July 17 that measures return on investment through four lenses: useful work, cost per successful task, dependability, and return on compute. The framing matters because the author is the finance lead, not a research team — the scorecard treats AI deployment as a capital project with line items, not a science experiment with benchmark scores.

Useful work comes first, asking how many tasks the AI actually completed in production rather than how many tokens it generated. Cost per successful task translates that into economics: a team can compare a consumer subscription against an enterprise contract on outcomes per dollar, not on leaderboard rankings. Dependability is the third pillar, measuring whether the system returns a correct answer on the first attempt or whether humans have to redo the work — the hidden labor line item most pilots underestimate. Return on compute closes the loop by asking how much useful output the organization got per dollar of GPU or API spend, which makes the question vendor-neutral across hosted models, self-hosted weights, or third-party APIs.

For builders and team leads, the scorecard functions as a procurement checklist and an internal retrospective template. A small team can log the four numbers per project this quarter and notice which tools earn their seat and which ones quietly cost more than they save. The piece is short on specific numbers — it offers the framework, not a benchmark — so the practical question becomes whether finance and procurement groups outside the AI bubble adopt the same four-question frame. Watch next: whether OpenAI publishes reference numbers teams can benchmark against, and whether the framework shows up in vendor evaluation guides from independent analysts.

[25:47] Practical queue

From today's stories: If you run Codex with a GPT-5.6 variant, pull rust-v0.144.6 and re-test a representative session before kicking off long refactors or multi-file migrations. Kimi K3 is live now through Moonshot's website and API, so builders can route long-context coding and reasoning tasks through it today. For builders, this means you can pull a 27B chat model and run it on a MacBook or modest Nvidia card without renting a server, treating it as a drop-in local endpoint for prototypes and agent stacks. For healthcare-adjacent builders and policy watchers, WISeR creates a live federal test bed for clinical prior-authorization AI. This is most useful for teams already running on NVIDIA hardware who want a documented path to fine-tune diffusion models. This matters because the gap between training and inference context has been a quiet ceiling on long-horizon agent quality. For builders, fully open video models with generalist capability mean you can prototype video understanding on your own footage without paying per-call API fees or sending sensitive video to a third party. This matters because context-window pressure is the most common reason a coding agent loses the plot on a large repository — short prompts and focused lookups keep multi-file tasks coherent. Python teams now have a well-supported default for wiring internal APIs, databases, and local scripts into AI agents without rebuilding the protocol layer each time. This means a developer who already knows one of the six covered languages can pick up MCP without a context-switch, and any integration built against the curriculum's patterns stays portable because MCP is a shared standard. What this means: if you already build MCP tools or data connectors for Claude or ChatGPT, mcp-use gives you one project that publishes both a server for any agent and a chat-surface app at the same time. Engineering leaders can now attribute Copilot pull request activity to specific repositories rather than averaging across an org, which makes it easier to spot underused teams or repos that quietly became AI-heavy. For Unity developers, this means AI assistance that actually touches the editor rather than guessing at your project structure. For builders and team leads, the scorecard functions as a procurement checklist and a retrospective template, since logging the four numbers per project this quarter reveals which tools earn their seat.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: OpenAI Codex rust-v0.144.6 / Moonshot drops Kimi K3 at 2.8T parameters / Prism-ML's Ternary-Bonsai-27B Hits Trending as a Local-AI Power Move
- 02:00 — Agent Stack Release Readout: OpenAI Codex rust-v0.144.6
- 03:26 — Moonshot drops Kimi K3 at 2.8T parameters — pricing stings
- 05:17 — Prism-ML's Ternary-Bonsai-27B Hits Trending as a Local-AI Power Move
- 07:08 — Medicare's WISeR puts AI in prior-authorization for six states
- 08:59 — NVIDIA and Hugging Face publish a scaling guide for fine-tuning video and image models
- 10:47 — Research digest: LongStraw Pushes RL Training Past 2M Tokens
- 11:52 — Research digest: VideoChat3 Pushes Open Video AI Toward True Generalist Use
- 13:00 — Codebase Memory MCP Cuts Coding Agent Token Use by 99%
- 14:48 — FastMCP v3.4.4 lands as Python's go-to MCP server builder
- 16:33 — Microsoft's MCP for Beginners curriculum crosses 16,700 GitHub stars
- 18:31 — mcp-use crosses 10,000 GitHub stars as a fullstack MCP app framework
- 20:19 — GitHub Copilot usage metrics now break down per repository
- 22:15 — Unity-MCP 10.1.0 turns your editor into a callable tool surface
- 23:59 — OpenAI's CFO publishes a four-metric scorecard for AI ROI
- 25:47 — Practical queue

---

## Primary Links

- OpenAI Codex rust-v0.144.6 release: https://github.com/openai/codex/releases/tag/rust-v0.144.6
- Kimi K3, and what we can still learn from the pelican benchmark: https://simonwillison.net/2026/Jul/16/kimi-k3/
- prism-ml/Ternary-Bonsai-27B-gguf trending on Hugging Face: https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf
- Medicare's WISeR pilot puts AI inside prior-authorization reviews: https://www.cms.gov/priorities/innovation/innovation-models/wiser
- MinishLab/semble — Fast and Accurate Code Search for Agents. Uses ~98%: https://github.com/MinishLab/semble
- Fine-tune video and image models at scale with NVIDIA NeMo Automodel a: https://huggingface.co/blog/nvidia/scale-diffusers-finetuning-nemo-automodel
- LongStraw: Long-Context RL Beyond 2M Tokens under a Fixed GPU Budget: https://github.com/MindLab-Research/longstraw
- VideoChat3: Fully Open Video MLLM for Efficient and Generalist Video U: https://mcg-nju.github.io/VideoChat3
- clidey/whodb — Where data access meets operational intelligence: https://github.com/clidey/whodb
- DeusData/codebase-memory-mcp — High-performance code intelligence MCP : https://github.com/DeusData/codebase-memory-mcp
- PrefectHQ/fastmcp — 🚀 The fast, Pythonic way to build MCP servers and : https://github.com/PrefectHQ/fastmcp
- microsoft/mcp-for-beginners — This open-source curriculum introduces t: https://github.com/microsoft/mcp-for-beginners
- mcp-use/mcp-use — The fullstack MCP framework to develop MCP Apps for : https://github.com/mcp-use/mcp-use
- getsentry/XcodeBuildMCP — A Model Context Protocol (MCP) server and CL: https://github.com/getsentry/XcodeBuildMCP
- Repository-level GitHub Copilot usage metrics generally available: https://github.blog/changelog/2026-07-17-repository-level-github-copilot-usage-metrics-generally-available
- CoplayDev/unity-mcp — Unity MCP acts as a bridge between AI assistants: https://github.com/CoplayDev/unity-mcp
- A scorecard for the AI age: https://openai.com/index/a-scorecard-for-the-ai-age
- lastmile-ai/mcp-agent repo: https://github.com/lastmile-ai/mcp-agent
- Upsonic/Upsonic repo: https://github.com/Upsonic/Upsonic
- Why teens deserve access to safe AI: https://openai.com/index/why-teens-deserve-access-safe-ai
- appcypher/awesome-mcp-servers — Awesome MCP Servers - A curated list o: https://github.com/appcypher/awesome-mcp-servers
- thinkingmachines/Inkling: https://huggingface.co/thinkingmachines/Inkling

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.7.1`, published 2026-07-13T22:33:14Z. Recent episode version tags detected: `v2026.7.1-beta.2`, `v2026.7.1-beta.6`, `v2026.7.2-beta.1`, `v2026.7.2-beta.2`. No new stable release this cycle.
- **Hermes Agent** — Latest stable verified: `v2026.7.7.2`, published 2026-07-08T03:11:22Z. Recent episode version tags detected: `v2026.6.5`, `v2026.7.1`, `v2026.7.7`, `v2026.7.7.2`. No new stable release this cycle.
- **OpenAI Codex** — Latest stable verified: `rust-v0.144.6`, published 2026-07-18T13:51:52Z. Recent episode version tags detected: `rust-v0.144.2`, `rust-v0.144.3`, `rust-v0.144.4`, `rust-v0.144.5`. Selected missing version(s): `rust-v0.144.6`.
- **Claude Code CLI** — Latest stable verified: `2.1.205`, published 2026-07-08T19:34:57.777Z. Recent episode version tags detected: `2.1.202`, `2.1.205`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-07-19). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.7.1` (stable) / `v2026.7.2-beta.3` (prerelease)
- **Hermes Agent** — `v2026.7.7.2`
- **OpenAI Codex** — `rust-v0.144.6`
- **Claude Code CLI** — `2.1.205`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
