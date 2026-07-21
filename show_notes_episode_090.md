# AgentStack Daily EP090 — NVIDIA Cosmos 3 Edge, Unity MCP 10.1, EU AI Act, Sentry XcodeBuildMCP

**Title:** NVIDIA Cosmos 3 Edge Lands on Hugging Face for Physical AI

**Tagline:** NVIDIA posts Cosmos 3 Edge to Hugging Face, a vision-language model aimed at edge robotics and physical AI on constrained hardware. Unity ships MCP v10.1.0, letting coding assistants drive the Editor directly via tool calls. Sentry's XcodeBuildMCP clears 6,100 GitHub stars as iOS agent tooling matures. The EU AI Act's August 2 transparency obligations take effect this week, with concrete obligations for builders. Plus Microsoft's MCP curriculum ships in six languages, codebase-memory-mcp gives coding agents persistent context, and OpenAI breaks down what goes wrong when agents run for hours without supervision.

**Feed description:** Cosmos 3 Edge from NVIDIA lands on Hugging Face, plus Unity's MCP v10.1.0 gives AI assistants direct Editor access and Sentry's XcodeBuildMCP clears 6,100 stars. The EU AI Act's August 2 transparency rules take effect this week, Microsoft's MCP curriculum ships in six languages, and OpenAI breaks down what goes wrong when agents run for hours. Also: Ternary on huggingface, whodb 0.121.0, codebase-memory-mcp, holaOS at 5,500 stars, and Upsonic 0.77.3.

---

## Story Slate

1. **Agent Stack Release Readout: Hermes Agent v2026.7.20; Claude Code CLI 2.1.206**
Hermes Agent shipped v0.19.0 on July 20, 2026 as the Quicksilver Release, cutting first-turn time-to-first-token by roughly 80 percent across the CLI, gateway, TUI, desktop app, and cron. Cold-start dropped from about 4.3 seconds to roughly 0.9 seconds, reasoning models now stream their thinking live by default, and the desktop app got a 20-plus pull-request speed overhaul including 14× faster streaming markdown and virtualized diffs. Around that spine, Hermes now manages the Nous subscription from the terminal, plugs Bitwarden and 1Password into the agent, lets smart approvals judge flagged commands by default, lets you watch subagents work live, and survives gateway crashes with a durable delivery ledger. The release also rolls up everything from v0.18.1 and v0.18.2.
Technical depth angle: Cold-start latency fell from roughly 4.3 seconds to about 0.9 seconds — an 80 percent cut — by trimming the 'Initializing agent…' path before the first turn reached the model. Reasoning streams live by default so the response box paints per token instead of per line. The desktop app's markdown splitter dropped roughly 14× CPU cost on long replies, with virtualized diffs and pre-warmed profile backends on hover.
Actionability angle: For builders running Hermes all day, the practical shift is that you can keep a terminal pinned alongside your editor without paying the latency tax on every turn. Plugging Bitwarden or 1Password into the agent means credential handoffs stop breaking your flow, and watching subagents live means you can actually supervise parallel runs instead of guessing what they did. The implications land across OpenClaw, Codex, Claude Code, Hermes, and Antigravity stacks alike.
Listener hook: Hermes just cut its first-token latency by 80 percent across every surface, so if it ever felt too slow to live in, this is the release to revisit.

2. **Ternary-huggingface.co listing adds Ternary**
A 27-billion-parameter open-weight language model from prism-ml, packaged as a GGUF file with weights compressed to 2-bit ternary, is climbing Hugging Face's trending models list. The July 4 release has already pulled in over 432,000 downloads and 876 likes, with tags confirming it runs on both CUDA GPUs and Apple's Metal silicon — so it's positioned for local inference on consumer hardware. Because it ships as a GGUF, builders can load it directly through llama.cpp without standing up a custom serving stack.
Technical depth angle: A 27B-parameter dense language model with every weight compressed to one of three values (2-bit ternary quantization), packaged as a GGUF so llama.cpp can stream it from disk on CUDA or Metal hardware without a separate serving stack.
Actionability angle: What this means for builders: a 27B-class conversational model that loads directly in llama.cpp on consumer GPUs and Apple Silicon laptops is now realistic for prototyping local agents. Why this matters: teams experimenting with on-device workflows can test a 27B-tier chat model in two-bit form without standing up a data-center GPU.
Listener hook: A 27-billion-parameter model just showed up small enough to run on your laptop, and it's trending for a reason.

3. **whodb 0.121.0 lands, folding data access and operations signal into one open-source surface**
Open-source project whodb shipped release 0.121.0 on July 16, with the repository seeing continued commits through July 21. Maintained under the clidey GitHub organization and now sitting at 4,931 stars, the project describes itself as 'where data access meets operational intelligence' - positioning itself at the intersection of database tooling and observability. The recent release cadence, with pushes landing between formal version tags, suggests an actively maintained project rather than a parked one. For small teams stitching together SQL clients and metrics dashboards, a self-hostable project that aims to compress both jobs behind a single interface is worth a closer look.
Technical depth angle: whodb's distinguishing mechanism is consolidation: a single self-hosted open-source surface that aims to combine direct data access with operational intelligence - meaning queries and schema work alongside the kind of metrics and signals usually pulled from a separate observability stack. For teams running their own infrastructure, that combination reduces the number of separate tools needed to diagnose slow queries or resource pressure.
Actionability angle: Small teams running their own data stack can evaluate whodb as a self-hosted alternative to running separate SQL and observability tools. The active release cadence (0.121.0 on July 16, with commits through July 21) signals a maintained project worth a closer look. The practical question for builders is whether the consolidated surface actually covers their backend and signal sources well enough to replace two separate tools.
Listener hook: If you've ever lost an afternoon wiring up four tools to answer one question about a slow query, a small open-source project is trying to put that behind a single self-hosted screen.

4. **codebase-memory-mcp gives AI coding assistants a persistent memory layer**
The DeusData project codebase-memory-mcp, an open-source Model Context Protocol server, just shipped release v0.9.0 on July 8, 2026. It indexes source trees into a persistent knowledge graph that coding assistants can query in under a millisecond, supports 158 languages, and reportedly uses 99 percent fewer tokens than raw file retrieval. Shipped as a single static binary with zero runtime dependencies, the repo has accumulated 33,443 GitHub stars with active commits as recent as July 19, signaling strong builder momentum around indexed codebase memory for AI agents.
Technical depth angle: The server pre-builds a persistent knowledge graph from a repo at index time, so the assistant queries a structured local index instead of re-reading files. Queries return in under a millisecond and the design claims roughly 99 percent fewer tokens per lookup versus passing raw source into the model's context window.
Actionability angle: What this means for builders is that an agent can finally answer architectural questions across a large repo without you re-pasting files into every session. It matters especially for monorepo work, where orientation time dominates the loop. The binary is drop-in on a laptop, so pairing it with an MCP-speaking coding assistant is a practical experiment this week.
Listener hook: An open-source server just promised to give every AI coding assistant near-instant, searchable memory of your entire repo — and it's already at 33,000 GitHub stars.

5. **holaOS, a Local-First Work Agent, Crosses 5,500 GitHub Stars**
holaOS, an open-source agent for everyday work, has crossed 5,500 stars on GitHub. The project bills itself as a local-first assistant that learns your working context in minutes and carries it forward across sessions, rather than rebuilding that context every time you open a new chat. The repository is actively maintained, with the most recent push landing on July 20, and is positioned around keeping files, projects, and habits on the user's own machine instead of routing work through remote servers.
Technical depth angle: holaOS's key mechanism is local-first execution paired with persistent working context. Instead of treating each conversation as a fresh session, the agent learns your files, projects, and habits from your own machine and carries that understanding forward, so the assistant picks up where it left off rather than re-onboarding every time you open it.
Actionability angle: holaOS's appeal for builders is the promise of continuity — an assistant that keeps your projects in mind without re-explanation every session. Why this matters: it points at a near future where chat assistants behave more like long-running coworkers than disposable tools. For now, early access means cloning the open-source repo and running from source until a tagged release ships.
Listener hook: If you have ever rage-quit a chat assistant because it forgot everything you taught it five minutes ago, a new local-first agent called holaOS is aiming exactly at that frustration.

6. **NVIDIA Posts Cosmos 3 Edge Introduction on Hugging Face**
NVIDIA published an 'Introducing Cosmos 3 Edge' post on the Hugging Face blog on July 20, 2026. The Edge suffix in the Cosmos world-model family has historically signaled a slimmer variant aimed at on-device and robotics inference rather than full datacenter-scale deployment. The post serves as the public landing page for the new variant, with model card details and weight downloads expected to follow on the same page. Until those specifics land, builders should treat this as a watch item for edge-targeted physical AI work.
Technical depth angle: Cosmos is NVIDIA's world foundation model line aimed at robotics and physical AI scenarios. The 'Edge' suffix in that family has historically marked the slimmer, lower-latency variant intended for on-device inference rather than datacenter-scale training. The Hugging Face blog post is the launch landing page; the model card is where supported inputs, outputs, and target hardware will be spelled out.
Actionability angle: NVIDIA is signaling a new edge-targeted entry in the Cosmos world-model family. This is the slot to watch for builders running Cosmos variants on Jetson-class hardware, on robots, or in latency-tight simulation loops. The model card — once NVIDIA publishes it — will confirm supported inputs, outputs, and precision variants before any integration.
Listener hook: NVIDIA just dropped a new edge-targeted world model on Hugging Face — here's what we know and what to watch for.

7. **EU AI Act transparency rules kick in August 2 — here's what builders need**
The European Commission on July 20 published guidelines explaining how companies should meet the AI Act's transparency obligations, which take effect August 2, 2026. AI providers must design systems that inform users when they're interacting directly with an AI and add machine-readable marks to AI-generated content. Deployers must disclose deepfakes, AI-generated content on public interest matters without human review or editorial responsibility, and use of emotion recognition or biometric categorisation systems. The Commission also released a Code of Practice on Transparency of AI-Generated Content and a Q&A on Article 50 to help companies work through specific scenarios.
Technical depth angle: The two-layer model is what to internalize: human-facing disclosure labels plus machine-detectable provenance marks on every piece of AI-generated or manipulated content. Providers handle the marks; deployers handle the user notifications for deepfakes, public-interest content without human review, and biometric uses. The marks have to be machine-readable so detection tooling can later verify provenance — that's the technical contract the Commission is asking for.
Actionability angle: For anyone shipping interactive AI, generative content tools, or biometric systems into the EU, this changes what 'done' looks like. What this means in practice: interactive products need upfront AI disclosure, generative outputs need machine-readable provenance marks, and emotion or biometric systems need explicit user notice before they run. Why this matters: the obligations start August 2, leaving roughly two weeks to confirm your stack can produce compliant marks and disclosures.
Listener hook: If you ship any AI into the EU, two weeks from now you have to start labeling it — and these are the exact rules.

8. **Research digest: Coding Agents Prune Their Own Context Without Extra Classifiers**
Coding agents hit context walls fast — every tool output, file read, and search result piles into working memory. A new method called SWE-Pruner Pro shows the agent already carries the relevance signal inside its own internal representations, so a small trained head can prune tool output inline without a separate classifier. The paper, trending on HuggingFace's daily feed, swaps the external scoring step for an internal one, which the authors argue is lighter and faster for long coding sessions on big repositories. For builders, this points toward cheaper agent runs that finish before the window collapses.
Technical depth angle: SWE-Pruner Pro replaces the external context-pruning classifier used by earlier work with a small head trained on the agent's own internal activations. Those activations already encode which parts of a tool output matter, so the agent prunes its own context inline rather than routing every chunk through a separate scorer.
Actionability angle: For builders running coding agents on large repos, this means context pruning could become a built-in capability rather than a bolted-on pipeline — lighter overhead and fewer moving parts to maintain. Whether open coding harnesses adopt the technique is the next thing to track.
Listener hook: Coding agents already know which tool output matters — a new method lets them cut the rest without a separate classifier.

9. **Research digest: RAG reframed as a 1980s statistics trick — with a guarantee**
A new paper reframes retrieval-augmented generation — the document-lookup technique behind most AI assistants — as a statistical tool from the 1980s called nearest-neighbor matching. The authors prove that when a transformer downstream of retrieval predicts outcomes, the regret of the resulting decision rule is bounded. The effect: RAG now carries a formal certificate for picking actions, not just answering questions.
Technical depth angle: The paper proves that RAG's retrieval step is statistically equivalent to matching each new case with its closest historical twins in an outcome space. Under that view, the regret of the resulting policy — how much worse it does than a perfect oracle — decomposes into two pieces, and the within-candidate choice piece is bounded by standard guarantees for transformers acting as outcome estimators.
Actionability angle: What this means for builders: any RAG pipeline that picks actions — offers, treatments, fraud flags — now has a theoretical reason to treat retrieval as statistical matching rather than a vibes-based lookup. Why it matters: the link between retrieval quality and decision quality just got tighter, with a formalism that goes beyond traditional retrieval benchmarks.
Listener hook: Turns out the thing AI assistants do to fetch documents is also a 40-year-old statistics technique — and it just got a formal guarantee for making decisions.

10. **Microsoft's open-source curriculum turns MCP fundamentals into hands-on lessons across six languages**
Microsoft pushed updates to its MCP for Beginners curriculum on July 20, an open-source GitHub project that walks developers through the Model Context Protocol using runnable examples in .NET, Java, TypeScript, JavaScript, Rust, and Python. With 16,802 stars and no tagged release, the repo focuses on practical techniques for building modular, scalable, and secure AI workflows across six language stacks.
Technical depth angle: The curriculum treats MCP as a standard way for a model to call external tools and data, then shows client and server patterns in each language's idiomatic form so the same lesson reads as native code for every stack.
Actionability angle: A developer new to MCP can pick their production language and walk through working samples rather than translate SDK docs by hand. This matters because tool-using agents depend on the protocol behaving consistently across runtimes. It also means teams can onboard engineers to MCP regardless of their existing stack.
Listener hook: If you've wanted a single MCP tutorial that doesn't make you learn a new language first, Microsoft just shipped the multi-language version.

11. **Sentry's XcodeBuildMCP Crosses 6,100 Stars on iOS Agent Tools**
Sentry's open-source XcodeBuildMCP — a Model Context Protocol server and CLI that exposes tools for AI agents working on iOS and macOS projects — has crossed 6,100 GitHub stars. The project shipped v2.6.2 on June 2, 2026, and the repository saw another push on July 21, 2026, signaling active maintenance. It packages agent-callable tooling for Apple platform work into a standardized MCP bridge, so coding agents can drive project operations through structured calls instead of hallucinating commands. Sentry maintains it as an open-source utility aimed squarely at the iOS and macOS developer-agent gap.
Technical depth angle: An MCP server is a small program that exposes a set of tools to an AI agent over a standardized protocol — instead of pasting commands or guessing, the agent calls the tools directly and gets structured results back. XcodeBuildMCP packages that pattern for iOS and macOS project work, so an agent can drive project operations through both the MCP bridge and the CLI.
Actionability angle: For iOS and macOS developers using coding agents, this means a workable bridge for letting the agent drive project operations hands-off. It matters because Xcode's CLI surface has historically been one of the roughest spots in agent-driven workflows, and a standardized MCP server is the kind of workaround that quietly catches on.
Listener hook: If your coding agent keeps guessing at Xcode commands instead of running them, Sentry's XcodeBuildMCP is the small open-source bridge worth knowing about.

12. **OpenAI Shares What Goes Wrong When AI Runs for Hours**
On July 20, OpenAI published a post titled 'Safety and alignment in an era of long-horizon models' that shares lessons from deploying AI systems designed to run continuously over long sessions. The piece highlights new safety risks that emerge once a model operates past the single-turn exchange, observed failures from real deployment, and safeguards the team improved through iterative rollout. The framing treats production usage itself, not lab benchmarks, as the alignment loop.
Technical depth angle: Long-horizon deployment surfaces risks that short evaluations don't reach — failure patterns that only appear once a model keeps working across a session. OpenAI's mechanism is iterative deployment: run, watch real usage, patch safeguards, ship again, treated as the alignment loop rather than a wrapper around benchmark testing.
Actionability angle: This matters for builders shipping any system that runs for more than a few minutes: the failure modes that hurt you in production are the ones your evaluation suite was never designed to catch. It argues for designing observability into the system from the start, meaning the ability to see what the model did across a long session and intervene when something goes wrong, rather than bolting it on after a costly incident.
Listener hook: If you've ever wondered what breaks when an AI keeps working for hours without supervision, OpenAI just published what their deployment data actually showed.

13. **Unity MCP v10.1.0 Gives AI Assistants Direct Editor Access**
Unity MCP, the CoplayDev project that bridges AI assistants and the Unity Editor, shipped version 10.1.0 on July 13, 2026. The repository has now crossed 12,700 stars on GitHub, signaling strong adoption among indie developers and small studios. The bridge exposes Unity operations — asset management, scene control, script editing, and task automation — as tools an LLM can invoke directly, removing the copy-paste step between chat and editor.
Technical depth angle: Unity MCP exposes a set of Unity Editor operations as tools that an LLM can call directly through the Model Context Protocol. The bridge mediates between the chat interface and the editor, letting the assistant manage assets, control scenes, edit scripts, and trigger automated task sequences without the developer manually copying code or commands between windows.
Actionability angle: Unity developers can now let an AI assistant drive editor actions directly, which means asset import, scene setup, script edits, and task automation can flow through a single chat interface. For solo devs and small teams, this turns multi-step editor workflows into natural-language requests and reduces context switching. The thing to watch is whether Unity Technologies ships native MCP support into the editor, which would validate and potentially compete with this community bridge.
Listener hook: If you've ever lost twenty minutes to manual Unity scene setup, this bridge turns that chore into a single chat request.

14. **Upsonic v0.77.3 Lands — A Python Framework for Autonomous AI Agents**
Upsonic, a Python framework for building autonomous AI agents, has shipped v0.77.3 (released May 19, 2026), with the GitHub repository pushing new commits as recently as June 18, 2026. The project has pulled in nearly 8,000 GitHub stars. Upsonic aims to give Python builders a managed agent loop — taking a goal, picking steps and tools, and executing — without forcing each team to hand-roll planning and tool-use code from scratch.
Technical depth angle: Upsonic is aimed at the agent loop itself — goal intake, step planning, tool calls, and execution — packaged as a Python library, so builders skip the planning-and-tool-use code most agent projects end up writing by hand. The v0.77.x version line plus June 18 commits indicate active iteration rather than a stalled release.
Actionability angle: Upsonic is worth a look if you're prototyping an autonomous agent service in Python and would rather lean on a managed agent loop than assemble your own planner, tool router, and runner. It fits naturally into a Flask or FastAPI worker, so a common entry point is wrapping it behind an HTTP endpoint that takes a natural-language task and returns a structured result.
Listener hook: A Python framework for autonomous AI agents just shipped v0.77.3, pulled in nearly eight thousand GitHub stars, and is still pushing commits a month later — here's why that combination matters.

---

## Editorial Mix Check

- flagship_products: 2
- builder_projects: 8
- local_ai: 2
- hardware_compute: 2
- policy_regulation: 1
- research: 2

---

## Model Discovery Check

- **Model lanes scanned** (OpenRouter major providers) — No new or materially updated models detected this cycle (verified July 21, 2026). Primary source: https://openrouter.ai/models. Decision: Not Selected — no new model candidates to evaluate for the Story Slate this cycle.

---

## Local LLM Spotlight

- **thinkingmachines/Inkling** — https://huggingface.co/thinkingmachines/Inkling — Inkling is a multimodal open-weights model from Thinking Machines that handles image, text, and audio in a single conversational interface using a Mixture-of-Experts backbone. It ships under Apache-2.0 with safetensors weights and published eval results, so it drops cleanly into a local inference stack. The MoE design keeps active parameter counts low per token, which makes it a practical self-host candidate for teams that need vision plus audio plus chat without paying cloud inference rates.
  Try now: Pull the safetensors checkpoint with the transformers library and run a single image-plus-audio question through the conversational pipeline on one 24GB GPU to validate latency and output quality before wiring it into an agent's tool calls.

---

## GitHub Project Radar

- **CoplayDev/unity-mcp** — https://github.com/CoplayDev/unity-mcp — Unity MCP bridges AI assistants with the Unity Editor, giving LLMs tools to manage assets, control scenes, edit scripts, and automate editor workflows. `stars: 12,709`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v10.1.0 (2026-07-13)`.
  Why this is on the radar now: v10.1.0 shipped on 2026-07-13 and the repository was updated on 2026-07-13.
  Stack improvement angle: It lets an OpenClaw or Claude Code agent drive Unity scenes and asset manipulation directly through the Model Context Protocol instead of stubbed-out editor APIs.
  Try now: Spin up the Unity MCP server inside the Unity Editor and point an MCP-capable agent at it to list and rename scene assets.

- **mcp-use/mcp-use** — https://github.com/mcp-use/mcp-use — mcp-use is the fullstack MCP framework for building MCP apps targeting ChatGPT and Claude plus MCP servers aimed at AI agents. `stars: 10,337`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: mcp-use@1.34.3 (2026-07-08)`.
  Why this is on the radar now: mcp-use@1.34.3 shipped on 2026-07-08 and the repository was updated on 2026-07-20.
  Stack improvement angle: It supplies a unified client and server scaffolding so a Hermes or Codex agent stack can stand up an MCP server with tool routing and shared schema validation out of the box.
  Try now: Clone the repo and run the example client against a local MCP server to watch the request and response flow in real time.

- **lastmile-ai/mcp-agent** — https://github.com/lastmile-ai/mcp-agent — mcp-agent helps you build effective agents using the Model Context Protocol and a small set of reusable workflow patterns. `stars: 8,459`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v0.0.21 (2025-05-09)`.
  Why this is on the radar now: v0.0.21 shipped on 2025-05-09 and the repository was updated on 2026-01-25.
  Stack improvement angle: It gives Claude Code or Hermes agents workflow primitives (sequential, parallel, router) layered on MCP servers, so multi-step pipelines compose without bespoke orchestration glue.
  Try now: Run the parallel-workflow example against a public MCP server to see how the patterns chain tool calls end to end.

---

## Extra Research Candidates

- **appcypher/awesome-mcp-servers — Awesome MCP Servers - A curated list of Model Context Protocol servers** — https://github.com/appcypher/awesome-mcp-servers — Awesome MCP Servers - A curated list of Model Context Protocol servers GitHub reports 5704 stars. Latest release: no tagged release . Repository pushed 2026-05-06T08:04:35Z. Technical depth angle: It indexes servers by transport (stdio versus streamable HTTP) and capability tags, which is what you actually need to filter compatibility with a given runtime.

- **the-open-agent/openagent — ⚡️next-generation personal AI assistant powered by LLM, RAG and agent loops, sup** — https://github.com/the-open-agent/openagent — ⚡️next-generation personal AI assistant powered by LLM, RAG and agent loops, supporting computer-use, browser-use and coding agent, demo: https://demo.openagentai.org GitHub reports 5426 stars. Latest release: v2.83.1 2026-07-08T03:55:03Z.  Technical depth angle: It composes a coding-agent loop, RAG retrieval, and computer-use and browser-use tool calls behind a single LLM-driven state machine.

- **nanbingxyz/5ire — 5ire is a cross-platform desktop AI assistant, MCP client. It compatible with ma** — https://github.com/nanbingxyz/5ire — 5ire is a cross-platform desktop AI assistant, MCP client. It compatible with major service providers, supports local knowledge base and tools via model context protocol servers . GitHub reports 5283 stars. Latest release: v0.15.4 2026-03-1 Technical depth angle: It pairs a desktop MCP client with a local vector store so retrieval happens against on-disk embeddings before the model call.

---

## Show Notes

```md
Episode 090 — July 21, 2026

[00:00] Episode hook

Hermes Agent shipped v2026.7.20 on July 20, 2026 as the Quicksilver Release, cutting first-turn time-to-first-token by roughly 80 percent across the CLI, gateway, TUI, desktop app, and cron jobs. Cold-start latency dropped from seconds to a fraction of a second, and the same build underpins Claude Code CLI 2.1.206 alongside it. The release also brings a streamlined install flow and a tighter startup path on the desktop client, while keeping the gateway's session handoff intact. The same day, NVIDIA posted an 'Introducing Cosmos 3 Edge' piece on Hugging Face, sketching a slimmer world-model variant aimed at on-device runtimes. And whodb 0.121.0, which shipped July 16, folds data access and operations signal into a single open-source surface maintained under the clidey GitHub organization.

[02:00] Agent Stack Release Readout: Hermes Agent v2026.7.20; Claude Code CLI 2.1.206

Hermes Agent shipped v0.19.0 on July 20, and the headline is pure speed. The cold-start Initializing agent screen used to eat about 4.3 seconds before your first turn even reached the model; that figure is now roughly 0.9 seconds, an 80 percent cut that applies to the CLI, the gateway, the TUI, the desktop app, and cron jobs alike. Round two of the speed wave hit what you actually see while waiting. Reasoning models now stream their thinking live by default, so you stop staring at a spinner for thirty seconds, and the response box paints per token instead of per line. Nous Research called this the Quicksilver Release, and the framing fits.

The desktop app got its own twenty-plus performance pull requests. Long replies used to cost fourteen times more CPU in the markdown splitter than they do now, giant diffs used to freeze the review pane until someone virtualized it, and switching sessions no longer thrashes layout. Streaming no longer re-renders the sidebar and every tool row on every token, profile backends pre-warm on hover intent, and boot-hidden panes mount at idle instead of on the cold-start critical path. The TUI renders markdown incrementally.

Around that speed spine sit five real workflow upgrades. You can now manage your Nous subscription without leaving the terminal, plug Bitwarden and 1Password straight into Hermes for credential access, let smart approvals judge flagged commands for you by default, watch your subagents work live, and trust that a finished response survives a gateway crash thanks to a durable delivery ledger. This release also rolls up everything from the v0.18.1 and v0.18.2 infrastructure patch tags into one documented window.

For builders, the practical shift is that Hermes now feels fast enough to live inside, not just visit. Sessions switch like tabs, long thinking traces stream as they happen, and secrets live where the agent does. That means you can keep a Hermes terminal pinned alongside your editor for an entire afternoon instead of treating it as a tool you open, prompt, and close. The thing to watch next is whether the roughly 3,300 closed issues and 2,245 commits actually translate into stability under sustained load, since the speed story is loud but the trust story still has to earn it over weeks of daily use.

[03:32] Ternary-huggingface.co listing adds Ternary

A new open-weight model called Ternary-Bonsai-27B is climbing Hugging Face's trending list, and the name tells you most of what's interesting. It's a 27-billion-parameter language model from a publisher called prism-ml, and it shipped on July 4 packaged as a GGUF file — the format llama.cpp uses to stream models straight off disk for local inference. The "ternary" and "2-bit" tags tell you why people are paying attention: every weight in the network has been compressed down to one of three possible values, which means the file lands at a fraction of the size a normal 27B checkpoint would take. The repository has already crossed 432,000 downloads and 876 likes, and the tags confirm it runs on both CUDA GPUs and Apple's Metal silicon — so it's positioned for both NVIDIA machines and Apple Silicon laptops from day one.

What this enables is straightforward. A 27B-class model normally demands serious hardware, and a two-bit-per-weight compression scheme is exactly the kind of trick that pushes that footprint down into consumer-laptop territory. Because it's a GGUF, you can point llama.cpp at the file today without standing up a custom serving stack, which makes it useful for local agents, offline chat assistants, and any workflow where you want a conversational model running on your own machine instead of round-tripping through an API.

The quality question is the one to watch. Two-bit quantization is aggressive, and the community will want to see whether the model holds up on real conversational tasks or only looks impressive on a download counter. For builders, the practical move is to pull the GGUF, load it through llama.cpp on your own hardware, and see what your machine can actually do with a 27B model in this compressed form — that's the experiment worth running this week.

[05:25] whodb 0.121.0 lands, folding data access and operations signal into one open-source surface

Open source project whodb shipped release 0.121.0 on July 16, with the repository seeing continued commits through July 21. The project lives under the clidey GitHub organization, has accumulated 4,931 stars on GitHub, and describes itself as 'where data access meets operational intelligence.'

That tagline is doing real work. Most tooling splits the two jobs. A database client handles queries, schemas, and writes. An observability stack handles latency, errors, and resource pressure. The repo's positioning suggests the maintainers want to collapse both into a single open-source surface - one place where you can talk to your data and watch the systems serving it.

The framing matters because tooling consolidation is back in fashion. Small teams running their own infrastructure typically stitch together a SQL client, a metrics dashboard, a log viewer, and a connection pool monitor just to answer a question like 'why did this query get slow.' A self-hostable project that aims to put more of that behind one screen reduces the tool-sprawl tax.

The release cadence tells its own story. A tagged version on July 16 followed by pushes five days later is the pattern of a project that's actively used rather than parked, with the team landing work between formal releases instead of batching everything into one drop a quarter.

The community size is worth noting too. Crossing into the high four figures on stars without a major vendor backing puts whodb in the category of tools that have earned a following on their own merit, which is also a rough proxy for the kind of feedback loop that catches bugs before they become incidents.

Watch next: the next release tag and any documentation that clarifies which data backends and operational signals are actually wired in. That detail is the gap between a compelling landing page and something a small team could deploy on a Monday morning.

[07:22] codebase-memory-mcp gives AI coding assistants a persistent memory layer

A new open-source tool called codebase-memory-mcp is trying to give AI coding assistants the equivalent of long-term memory for entire repositories. The project, hosted under DeusData on GitHub, just shipped release v0.9.0 on July 8. It is a Model Context Protocol server — the standard plug-in format used by most modern agentic coding clients — and its job is to turn a source tree into a persistent knowledge graph that the assistant can query over and over.

The numbers are the headline. According to the project, it indexes an average repository in milliseconds, answers queries in under a millisecond, supports 158 programming languages, and uses roughly 99 percent fewer tokens than passing raw files back into the model. That last point matters because context windows are expensive and limited. Instead of stuffing thousands of lines into a prompt, the assistant asks the local server a structured question and gets back only the relevant slice. The whole thing ships as a single static binary with zero runtime dependencies, so a developer can drop it on a laptop and start pointing an agent at a real codebase without setting up a database.

Practically, this means an AI assistant can finally answer questions like "which module owns the payment retry logic" or "where is this deprecated function still called from" without you re-pasting files every session. For teams working in large monorepos, that turns hours of orientation into seconds. The GitHub repo has already accumulated 33,443 stars, and the latest commit landed on July 19, so momentum is clearly still building. Worth watching next: how stable the v1.0 line lands and whether major coding-agent vendors start bundling this kind of indexed memory directly into their products.

[09:08] holaOS, a Local-First Work Agent, Crosses 5,500 GitHub Stars

A new project called holaOS is quietly building a real following on GitHub, where it has crossed 5,500 stars. The repo bills itself as your super agent for work, and the elevator pitch is short: it runs locally, learns your working context in minutes, and does not forget it between sessions.

That local-first framing is the most interesting part. Most assistant tools today route your work through remote servers and rebuild their understanding of you every time you open a new chat window. A local-first agent can keep your files, your open projects, your naming conventions, and your habits on your own machine, and the project explicitly frames that as a feature rather than a tradeoff. The repository describes holaOS as a tool that picks up your working context quickly and carries it forward, which is the kind of continuity that turns a chatbot into something closer to a coworker who has been sitting next to you for months.

The project is actively maintained. The most recent push to the repository landed on July 20, so the codebase is moving, and because it is open source anyone can read the code, file issues, or fork it for their own experiments. There is not yet a tagged release on the repo, so the practical move for now is to clone the repository, follow the setup steps in its README, and run it from source rather than waiting for a packaged installer.

For builders, the appeal is straightforward. If you have ever closed a chat window and lost an hour of carefully explained context, that is the pain point the project is aiming directly at. Worth watching to see whether holaOS stays a developer toy or grows into a more polished daily-driver for non-coders.

[10:58] NVIDIA Posts Cosmos 3 Edge Introduction on Hugging Face

NVIDIA published a post titled "Introducing Cosmos 3 Edge" on the Hugging Face blog on July 20, 2026. The Edge suffix in NVIDIA's Cosmos family has historically signaled the slimmer, lower-latency variants aimed at on-device and robotics inference rather than full datacenter-scale training. That positioning matters because world foundation models are typically heavyweight — Cosmos 3 Edge is positioned as a runnable-on-the-robot option for physical AI scenarios.

The Hugging Face blog post serves as the public introduction page for the new variant. The Cosmos line has been NVIDIA's main world-model family aimed at robotics and autonomous systems work, and the Edge tier is where that family meets on-device deployment. Builders looking for the specifics — supported input types, output formats, and target hardware — should expect the accompanying model card to lay those out in detail. Weight downloads and any precision variants NVIDIA publishes will live on that page alongside the model card.

For builders, the practical signal is straightforward: a new Cosmos entry is aimed at the edge tier. If you are already running Cosmos variants on Jetson-class hardware, on a robot, or inside a simulation loop where latency budgets are tight, this is the slot to watch. If you were waiting for a smaller Cosmos you could fine-tune on a workstation rather than a cluster, this looks like that lane.

The thing to watch next is the model card and the published weight listings. NVIDIA typically publishes the supported input resolution, context length, sampling rate for video outputs, and the recommended inference stack alongside the weights. Until those details land, treat the post as a watch item rather than an integration target — and resist the urge to wire Cosmos 3 Edge into a pipeline until the card confirms it accepts what you intend to feed it.

[12:51] EU AI Act transparency rules kick in August 2 — here's what builders need

On July 20, the European Commission published guidelines explaining how companies should meet the AI Act's transparency rules, which take effect August 2, 2026. The point is straightforward: people should be able to tell when they're talking to an AI, or when content was generated or altered by one — cutting down the risk of deception and manipulation.

Under the AI Act, AI providers have two concrete obligations. First, their systems have to tell users when they're interacting directly with an AI, not a human. Second, AI-generated or manipulated content has to carry machine-readable marks — embedded signals detection tools can pick up later to confirm provenance. The guidelines cover marking and labelling requirements across interactive systems and generative content.

Deployers — the businesses putting these systems in front of users — carry their own duties. They have to tell people when they're being shown a deepfake, when AI-generated content touches matters of public interest without human review or editorial responsibility, and when emotion recognition or biometric categorisation systems are being used on them. Emotion recognition means AI reading faces, voices, or body language to infer feelings; biometric categorisation means sorting people by sensitive traits.

For builders shipping into the EU, this changes what 'done' looks like. Interactive products need visible AI disclosure at the point of use. Generative outputs need machine-readable marks that survive downstream editing. And any emotion or biometric system needs explicit user notice before it runs.

The Commission released a Code of Practice on Transparency of AI-Generated Content alongside a Q&A on Article 50 to walk through specific scenarios. Worth watching next: how aggressively enforcement lands after August 2, and whether the marking standards converge on one technical format providers and deployers can both implement.

[14:40] Research digest: Coding Agents Prune Their Own Context Without Extra Classifiers

Coding agents burn through context fast — every tool call, file read, and search result piles into the working memory until the model runs out of room. New research called SWE-Pruner Pro tackles that problem from the inside out. Existing context-pruning tools for coders attach a separate classifier to score each chunk of tool output. The team behind SWE-Pruner Pro found the agent already knows which parts matter. When the agent reads tool output, its internal activations encode relevance — a signal the model itself carries. So instead of running an outside filter, SWE-Pruner Pro trains a small head on top of the agent's own internal representations to decide what to keep and what to drop, all inside the agent loop. The result is pruning without the extra classifier overhead, which matters for long coding sessions on big repositories. For builders running agents on multi-file refactors or debugging marathons, this could mean cheaper, faster runs that finish before the context window collapses. Integration into open coding harnesses is the next thing to track.

[15:46] Research digest: RAG reframed as a 1980s statistics trick — with a guarantee

Retrieval-augmented generation — the technique AI assistants use to pull documents before answering — just got a new identity. A new paper shows RAG is mathematically equivalent to nearest-neighbor matching, a 1980s statistics method for estimating cause and effect by pairing each new case with its closest historical twins. The paper formalizes that link, then proves a guarantee: when the language model downstream of retrieval acts as the outcome predictor, the regret of the resulting decision rule is bounded. In plain terms, RAG is no longer just a lookup trick — it's a decision-making tool with a statistical certificate. That changes how to think about any RAG pipeline that picks between actions: matching a patient to the best-documented treatment, choosing which offer to show a shopper, flagging a transaction as fraud. The retrieval index becomes a matching engine rather than a similarity search. Looking ahead: empirical tests showing real RAG stacks winning on the new guarantee's terms, and enterprise vendors citing matching-style evaluation instead of pure retrieval benchmarks.

[16:49] Microsoft's open-source curriculum turns MCP fundamentals into hands-on lessons across six languages

Microsoft updated its MCP for Beginners curriculum on July 20, and for developers who want to wire models into real tools, this is a quietly useful drop. The repository, hosted at microsoft/mcp-for-beginners on GitHub, walks developers through the Model Context Protocol using runnable examples across .NET, Java, TypeScript, JavaScript, Rust, and Python. That is six stacks, with the same lessons expressed in each language's idioms, so the focus stays on MCP concepts rather than one vendor's SDK flavor.

The curriculum frames MCP as a standard way for a model to call external tools and data sources, then shows how to build both the client side (the model and its host) and the server side (the tool or service being called) in whichever language already lives in your stack. Modules step through modular design, scalable patterns, and security considerations, which are the three concerns that bite most teams the first time they expose a tool to a model.

The practical pitch is straightforward. A backend engineer on Rust or .NET can read the same lesson their TypeScript colleague is reading, in their own language. The repo has accumulated 16,802 stars, suggesting a wide audience has already vetted the approach and stress-tested the examples. Beginners get a guided path with copy-pasteable code; experienced developers can lift working snippets as scaffolding for production integrations.

The curriculum's emphasis on modular, scalable, and secure patterns means the lessons should stay useful as MCP-aware tools evolve. The repository pushed a fresh commit on July 20, signaling active maintenance rather than a stale snapshot.

There is no tagged release to point at, so the curriculum lives as maintained documentation rather than a versioned artifact. Watch next for which languages Microsoft adds, and whether the curriculum expands into more advanced integration patterns as the broader MCP ecosystem matures.

[18:42] Sentry's XcodeBuildMCP Crosses 6,100 Stars on iOS Agent Tools

Here's a small open-source project that quietly hit 6,100 GitHub stars this month: XcodeBuildMCP, maintained by Sentry. It's a Model Context Protocol server, which is basically a bridge that lets an AI agent call real developer tools instead of just talking about them. The acronym stands for Model Context Protocol — think of it as a standardized way for an agent to ask a server to do something and get a structured answer back.

What XcodeBuildMCP does is narrow and useful: it provides tools for agent use when working on iOS and macOS projects, packaged as both an MCP server and a command-line interface. So when you're using a coding agent on an Apple platform project, you can plug this in and the agent gets a toolbelt for actually driving the work — rather than hallucinating commands or asking you to copy-paste output.

The project shipped v2.6.2 on June 2, 2026, and the repository saw another push on July 21, so it's actively maintained. Sentry open-sourced it, which matters because iOS tooling has historically been one of the roughest spots for agent-driven workflows — Xcode's command line is quirky, build errors are noisy, and project files are fragile. Anything that gives an agent a clean, structured handle on that machinery is worth watching.

What you can build with it: any iOS or macOS workflow where you want your coding agent to drive the project end-to-end — iterating on changes, running operations through the CLI, and getting structured results back — without you babysitting the terminal.

One thing to watch: how quickly the major coding-agent harnesses ship first-class support for plugging in third-party MCP servers like this one, since the integration story still varies by tool.

[20:30] OpenAI Shares What Goes Wrong When AI Runs for Hours

OpenAI posted something on July 20 that's worth a closer look — a piece titled "Safety and alignment in an era of long-horizon models." It isn't a model launch or a benchmark reveal. It's a candid writeup of what the safety team learned from running AI systems over long sessions, and what they think other builders should be paying attention to.

The framing is the interesting part. Most public alignment conversation assumes short exchanges — one prompt, one answer, one evaluation. OpenAI's post is about what changes when a model keeps working for hours, days, or continuously. They say they observed failures during real deployment that wouldn't surface in single-turn testing, and they credit iterative deployment — running the model, watching what actually happens in production, patching safeguards, shipping again — with surfacing both the problems and the fixes.

That loop is the mechanism worth naming. Not a single safety evaluation, but a cycle. Real usage exposes new failure patterns, those patterns inform improved safeguards, the model ships, the cycle repeats. OpenAI is treating that deployment loop as the actual alignment work for long-horizon systems, not a wrapper around lab benchmarks.

For builders shipping agents, automation, or assistants meant to operate for extended sessions, the takeaway is uncomfortable but useful. The failure modes that hurt you in production are the ones your evaluation suite was never designed to catch. That argues for building observability into the system from the start — being able to see what the model did across a long session and intervene when something goes sideways.

What to watch next: whether other labs publish postmortems in the same format, and whether a shared vocabulary for long-horizon failures starts to emerge.

[22:17] Unity MCP v10.1.0 Gives AI Assistants Direct Editor Access

Unity game developers now have a more direct line between their AI assistants and the editor itself. CoplayDev's unity-mcp just shipped version 10.1.0 on July 13, and the repository has now crossed 12,700 stars on GitHub, which is a strong signal that this bridge pattern is resonating with the indie and studio crowd.

The tool works as an MCP — Model Context Protocol — bridge, a standard that lets AI assistants talk to external tools and editors. Instead of copy-pasting code between your chat window and the Unity editor, you give your LLM direct access to a set of Unity operations. That means your assistant can manage assets, control scenes, edit scripts, and automate repetitive editor tasks while you stay in flow.

So what does that look like in practice? A solo developer building a 3D puzzle game can ask their assistant to import a folder of textures, place them across scene objects, and generate a matching script that swaps sprites on a timer — all without bouncing between windows. A small team can wire up nightly asset-validation routines that the AI triggers on demand. The bridge sits between the chat and the editor, so you can watch the changes land in real time.

Players won't see any difference on screen, but for the developer at the editor, the friction of switching contexts drops noticeably. The 12,700-star count puts unity-mcp among the more popular game-engine bridges available right now, and the steady release cadence suggests the maintainers are actively shipping fixes and feature work. Worth watching next: whether Unity Technologies itself builds native MCP support into the editor, and how studios start integrating this into their production pipelines.

[24:02] Upsonic v0.77.3 Lands — A Python Framework for Autonomous AI Agents

If you've been wanting to build autonomous AI agents in Python without hand-rolling the agent loop yourself, Upsonic just got a fresh drop. The open-source framework hit version 0.77.3 on May 19, and the repository has already pulled in nearly eight thousand GitHub stars, putting it on the map of Python agent toolkits.

The pitch is straightforward. Upsonic is a Python framework for building autonomous AI agents — software that takes a goal, decides what steps to run, calls the tools it needs, and finishes the job, with the agent loop managed by the library rather than hand-rolled in your code. For builders who want to skip writing their own planning-and-tool-use plumbing, that is the actual time sink this removes.

Release cadence matters. The repository was pushed as recently as June 18, 2026 — about a month after the v0.77.3 tag on May 19 — so the team is actively iterating rather than sitting on a frozen release. For a framework still in zero-point-x territory, a steady drumbeat of commits is usually the difference between something you can bet a prototype on and something that quietly rots.

What can you actually build with it? The pattern most builders reach for first is a Python service that takes a natural-language task, lets the agent pick a tool or API, executes the step, and returns a structured result — research assistants, support triage, or scheduled reporting jobs where the agent decides the workflow. Because it's pure Python, you can drop it into a Flask or FastAPI service or run it as a worker.

One thing to watch: how long until the next tagged release. If the team keeps shipping point releases every few weeks, this moves from 'interesting experiment' to 'framework I can pick for a real project.'

[25:53] Practical queue

From today's stories: For builders running Hermes all day, the practical shift is that you can keep a terminal pinned alongside your editor without paying the latency tax on every turn. What this means for builders: a 27B-class conversational model that loads directly in llama.cpp on consumer GPUs and Apple Silicon laptops is now realistic for prototyping local agents. Small teams running their own data stack can evaluate whodb as a self-hosted alternative to running separate SQL and observability tools. What this means for builders is that an agent can finally answer architectural questions across a large repo without you re-pasting files into every session. holaOS's appeal for builders is the promise of continuity — an assistant that keeps your projects in mind without re-explanation every session. NVIDIA is signaling a new edge-targeted entry in the Cosmos world-model family. For anyone shipping interactive AI, generative content tools, or biometric systems into the EU, this changes what 'done' looks like. For builders running coding agents on large repos, this means context pruning could become a built-in capability rather than a bolted-on pipeline — lighter overhead and fewer moving parts to maintain. What this means for builders: any RAG pipeline that picks actions — offers, treatments, fraud flags — now has a theoretical reason to treat retrieval as statistical matching rather than a vibes-based lookup. A developer new to MCP can pick their production language and walk through working samples rather than translate SDK docs by hand. For iOS and macOS developers using coding agents, this means a workable bridge for letting the agent drive project operations hands-off. This matters for builders shipping any system that runs for more than a few minutes: the failure modes that hurt you in production are the ones your evaluation suite was never designed to catch. Unity developers can now let an AI assistant drive editor actions directly, which means asset import, scene setup, script edits, and task automation can flow through a single chat interface. Upsonic is worth a look if you're prototyping an autonomous agent service in Python and would rather lean on a managed agent loop than assemble your own planner, tool router, and runner.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: Hermes Agent v2026.7.20; Claude Code CLI 2.1.206 / Ternary-huggingface.co listing adds Ternary / whodb 0.121.0 lands, folding data access and operations signal into one open-source surface
- 02:00 — Agent Stack Release Readout: Hermes Agent v2026.7.20; Claude Code CLI 2.1.206
- 03:32 — Ternary-huggingface.co listing adds Ternary
- 05:25 — whodb 0.121.0 lands, folding data access and operations signal into one open-source surface
- 07:22 — codebase-memory-mcp gives AI coding assistants a persistent memory layer
- 09:08 — holaOS, a Local-First Work Agent, Crosses 5,500 GitHub Stars
- 10:58 — NVIDIA Posts Cosmos 3 Edge Introduction on Hugging Face
- 12:51 — EU AI Act transparency rules kick in August 2 — here's what builders need
- 14:40 — Research digest: Coding Agents Prune Their Own Context Without Extra Classifiers
- 15:46 — Research digest: RAG reframed as a 1980s statistics trick — with a guarantee
- 16:49 — Microsoft's open-source curriculum turns MCP fundamentals into hands-on lessons across six languages
- 18:42 — Sentry's XcodeBuildMCP Crosses 6,100 Stars on iOS Agent Tools
- 20:30 — OpenAI Shares What Goes Wrong When AI Runs for Hours
- 22:17 — Unity MCP v10.1.0 Gives AI Assistants Direct Editor Access
- 24:02 — Upsonic v0.77.3 Lands — A Python Framework for Autonomous AI Agents
- 25:53 — Practical queue

---

## Primary Links

- Hermes Agent v2026.7.20 release: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.20
- Claude Code CLI npm: https://www.npmjs.com/package/@anthropic-ai/claude-code
- prism-ml/Ternary-Bonsai-27B-gguf trending on Hugging Face: https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf
- MinishLab/semble — Fast and Accurate Code Search for Agents. Uses ~98%: https://github.com/MinishLab/semble
- clidey/whodb — Where data access meets operational intelligence: https://github.com/clidey/whodb
- DeusData/codebase-memory-mcp — High-performance code intelligence MCP : https://github.com/DeusData/codebase-memory-mcp
- holaboss-ai/holaOS — Your super agent for work: local-first, learn you: https://github.com/holaboss-ai/holaOS
- Introducing Cosmos 3 Edge: https://huggingface.co/blog/nvidia/cosmos3edge
- Commission publishes guidelines on transparency obligations for provid: https://digital-strategy.ec.europa.eu/en/news/commission-publishes-guidelines-transparency-obligations-providers-and-deployers-certain-ai-systems
- SWE-Pruner Pro: The Coder LLM Already Knows What to Prune: https://github.com/Ayanami1314/swe-pruner-pro
- Vector Search As Nearest Neighbor Matching: RAG-based Policy Learning : https://arxiv.org/abs/2607.18225
- PrefectHQ/fastmcp — 🚀 The fast, Pythonic way to build MCP servers and : https://github.com/PrefectHQ/fastmcp
- microsoft/mcp-for-beginners — This open-source curriculum introduces t: https://github.com/microsoft/mcp-for-beginners
- getsentry/XcodeBuildMCP — A Model Context Protocol (MCP) server and CL: https://github.com/getsentry/XcodeBuildMCP
- Safety and alignment in an era of long-horizon models: https://openai.com/index/safety-alignment-long-horizon-models
- CoplayDev/unity-mcp — Unity MCP acts as a bridge between AI assistants: https://github.com/CoplayDev/unity-mcp
- Upsonic/Upsonic — Build autonomous AI agents in Python.: https://github.com/Upsonic/Upsonic
- mcp-use/mcp-use repo: https://github.com/mcp-use/mcp-use
- lastmile-ai/mcp-agent repo: https://github.com/lastmile-ai/mcp-agent
- appcypher/awesome-mcp-servers — Awesome MCP Servers - A curated list o: https://github.com/appcypher/awesome-mcp-servers
- the-open-agent/openagent — ⚡️next-generation personal AI assistant pow: https://github.com/the-open-agent/openagent
- nanbingxyz/5ire — 5ire is a cross-platform desktop AI assistant, MCP c: https://github.com/nanbingxyz/5ire
- thinkingmachines/Inkling: https://huggingface.co/thinkingmachines/Inkling

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.7.1`, published 2026-07-13T22:33:14Z. Recent episode version tags detected: `v2026.7.1-beta.6`, `v2026.7.2-beta.1`, `v2026.7.2-beta.2`, `v2026.7.2-beta.3`. No new stable release this cycle.
- **Hermes Agent** — Latest stable verified: `v2026.7.20`, published 2026-07-20T18:35:55Z. Recent episode version tags detected: `v2026.6.5`, `v2026.7.1`, `v2026.7.7`, `v2026.7.7.2`. Selected missing version(s): `v2026.7.20`.
- **OpenAI Codex** — Latest stable verified: `rust-v0.144.6`, published 2026-07-18T13:51:52Z. Recent episode version tags detected: `rust-v0.144.3`, `rust-v0.144.4`, `rust-v0.144.5`, `rust-v0.144.6`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.206`, published 2026-07-09T17:54:03.009Z. Recent episode version tags detected: `2.1.202`, `2.1.205`, `latest`, `stable`. Selected missing version(s): `2.1.206`.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-07-21). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.7.1` (stable) / `v2026.7.2-beta.3` (prerelease)
- **Hermes Agent** — `v2026.7.20`
- **OpenAI Codex** — `rust-v0.144.6`
- **Claude Code CLI** — `2.1.206`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
