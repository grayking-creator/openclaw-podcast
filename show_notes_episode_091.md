# AgentStack Daily EP091 — 27B in Laptop RAM, Dorsey's Buzz, Anthropic's $1.5B Settlement

**Title:** 27B Open-Weight Model Now Fits in Laptop RAM, Dorsey Ships Buzz, Anthropic Settles $1.5B Case

**Tagline:** A 27-billion-parameter open-weight model now fits inside laptop RAM, a feat that would have sounded fictional two years ago. Jack Dorsey's new app Buzz fuses chat, AI agents, and Git into a single feed. Anthropic's $1.5 billion pirated-books settlement cleared final court approval. Semble shipped a code search engine 98% leaner than peers for AI agents. XcodeBuildMCP 2.6.2 unlocks real iOS build pipelines for coding agents, while OpenAI and Hugging Face disclosed a model-evaluation security incident. Plus Gemini 3.6 Flash surfaces in listings, and Bristol Myers Squibb is building a Vera Rubin SuperPOD for drug discovery.

**Feed description:** A 27-billion-parameter open-weight model now fits in laptop RAM. Jack Dorsey launches Buzz, a chat, AI agents, and Git mashup. Anthropic's $1.5B pirated-books settlement clears final court approval. Semble's 98% leaner code search engine targets AI agents. XcodeBuildMCP 2.6.2 gives coding agents real Apple build access. Plus Gemini 3.6 Flash surfaces in listings, OpenAI and Hugging Face disclose a model-evaluation security incident, and Bristol Myers Squibb deploys Vera Rubin for drug discovery.

---

## Story Slate

1. **Agent Stack Release Readout: OpenAI Codex rust-v0.145.0**
OpenAI Codex rust-v0.145.0 stabilized its opt-in multi-agent V2 experience with configurable sub-agent models, reasoning levels, concurrency, and restored roles. The /import command now migrates Cursor and Claude Code settings, MCP servers, plugins, sessions, commands, and project memories. Amazon Bedrock login with GPT-5.6 Sol as the default model, audio inputs and outputs with streaming realtime V3, and clickable inline visualization links in the terminal also arrived, alongside fixes for branched prompt editing, terminal responsiveness, MCP startup timeouts, and Windows sandbox reliability.
Technical depth angle: The opt-in multi-agent V2 experience is stabilized: each sub-agent now gets a configurable model and reasoning level, concurrency is exposed, and roles are preserved across long sessions so workers stop collapsing into a single context.
Actionability angle: Multi-agent runs are finally stable enough for real work — try a parallel investigation or refactor before trusting it on production code. The /import expansion makes switching from Cursor or Claude Code low-friction, so existing MCP servers and project memories carry over without rebuilding from scratch. The Bedrock and audio pipelines are worth watching as they move out of experimental.
Listener hook: If you've been burned by multi-agent mode before, this is the Codex update that makes parallel sub-agents safe enough to actually use.

2. **Google's Gemini 3.6 Flash on With Million-google listing adds gemini-3.6-flash**
Google has added Gemini 3.6 Flash to OpenRouter's model catalog. The new entry is positioned as a high-efficiency option aimed at coding, agentic workflows, and web and app development. Its headline spec is a one-million-token context window. Google also frames it as producing polished outputs with fewer unnecessary edits, a meaningful claim for agentic coding where file churn eats tokens and time.
Technical depth angle: The model ships with a one-million-token context window and is positioned as a high-efficiency Flash-tier option aimed at coding and agentic workflows. Google also claims it produces polished outputs with fewer unnecessary edits, a behavior that matters in agentic loops where churning on the same lines costs tokens and time.
Actionability angle: Builders using OpenRouter can now route coding and agentic workloads to Gemini 3.6 Flash through the existing interface, taking advantage of the million-token window for large repositories and long agent traces. The practical question is whether the claimed reduction in unnecessary edits holds up on real codebases, so it is worth running it against your own tasks before committing it to a critical path.
Listener hook: A million-token context window from Google, now reachable through OpenRouter, is worth a quick look if you build with long-context agents.

3. **Jack Dorsey launches Buzz: chat, AI agents, and Git in one feed**
Jack Dorsey's Block has launched Buzz, a workplace group chat platform that puts humans and their AI agents in the same conversation alongside Git hosting. The product aims to collapse chat, version control, and agent output into a single feed so engineers can loop a bot into a thread the way they would ping a coworker, then watch commits and pull requests land in the same channel that produced them. The launch hit Hacker News at 330 points within hours and lands in a market already crowded with established chat platforms like Slack and Microsoft Teams.
Technical depth angle: Buzz treats the AI agent as a participant in the group thread rather than an external integration. Git hosting is woven into the same surface, so commits and pull requests stay attached to the chat that produced them instead of living in a separate tool. The core mechanic is collapsing three workspaces, chat, code, and agent runtime, into one shared feed.
Actionability angle: What this means for builders is that small teams may be able to stop stitching together chat, repo, and agent runtime themselves, since Buzz aims to keep those layers in one place. Why this matters: the chat thread becomes the source of truth for both human decisions and agent-driven code changes, which could reshape how engineering teams document their work.
Listener hook: Jack Dorsey's new chat app wants your AI agent to sit in the same thread as your team.

4. **Semble ships a 98% leaner code search for AI agents**
MinishLab's open-source code search tool Semble targets AI coding agents that currently burn tens of thousands of tokens running grep and reading whole files just to locate a function. The release, v0.5.2 on July 21, claims roughly 98% fewer tokens than a naive grep-plus-read pipeline for the same query. The repository has accumulated more than 5,600 GitHub stars, with both a release and additional commits landing within the past 24 hours. Semble positions itself as a backend that any agent harness can call into, rather than a chat product or IDE plugin.
Technical depth angle: Semble replaces the read-the-whole-file step in agent code search with a focused, narrow answer that fits in a small token budget. The 98% reduction comes from skipping file reconstruction entirely rather than retrieving raw text.
Actionability angle: If your agent's token bill is dominated by search, a focused code-search backend is the highest-leverage swap available. What this means for builders: Semble is positioned as a drop-in replacement for the grep-and-read step in any harness. Why it matters: shifting from file-dump search to narrow answer search is the cheapest way to extend an agent's effective context without raising the model's context window.
Listener hook: If you've ever watched a coding agent blow half its context window hunting for one function, this is the tool built to fix that.

5. **whodb crosses 4,900 stars with active shipping pace**
whodb, an open-source GitHub project under user clidey, has reached roughly 4,930 stars and shipped release 0.121.0 on July 16, followed by another repository push on July 22. The project positions itself at the intersection of data access and operational intelligence. With a sub-1.0 version number and shipping activity inside a single week, whodb reads as a fast-iterating project still defining its surface area rather than a settled tool.
Technical depth angle: whodb sits at the intersection of data access and operational intelligence, per its tagline. The technical detail worth noting: version 0.121.0 paired with two repo events in one week indicates a pre-1.0 project in active iteration, where each release is a checkpoint rather than a stable milestone. No specific mechanism or feature set is documented in the source beyond that positioning line.
Actionability angle: What this means: the project is worth a quick evaluation if you work in the data tooling space, since the active pace is the kind of signal that tells you whether the maintainers are building or maintaining. Why this matters: most open-source data tools at this stage either stall before 1.0 or pivot dramatically, so the next ten releases will tell you whether whodb is a real bet or a passing experiment.
Listener hook: An open-source data project called whodb just hit the kind of star count and shipping cadence that builders tend to notice.

6. **holaOS Aims to Be Your Local-First Work Agent**
holaOS is an open-source project on GitHub positioning itself as a super agent for work that runs locally and learns your working context in minutes while retaining it across sessions. With more than 5,500 stars and recent commit activity, it is an emerging option for people who want an AI assistant that lives on their own machine and builds persistent memory of their projects. No tagged release has been published yet, so the project is best understood as actively developed rather than ready to install today.
Technical depth angle: The repository describes a local-first design where the agent figures out your working context within minutes and retains it indefinitely on your own machine, rather than uploading files and prompts to a remote cloud. Persistent memory that never leaves your device is the headline mechanism, and it is what differentiates holaOS from cloud-based work assistants.
Actionability angle: This matters for builders who want a work agent that holds onto project context over weeks without shipping sensitive files to a third party. For teams exploring self-hosted assistants, it is worth starring the repository and watching how the local-first architecture actually performs once a tagged release lands.
Listener hook: A 5,500-star GitHub project is betting that the future of work agents runs on your laptop, not in someone else's cloud.

7. **A 27B Open-Weight Model Now Fits in Laptop RAM**
prism-ml published Ternary-Bonsai-27B-gguf on Hugging Face on July 4, a 27-billion-parameter open-weight model compressed to 2-bit ternary weights and packaged as a GGUF build for llama.cpp. The release supports CUDA and Metal acceleration, runs on Nvidia and Apple Silicon hardware, and has already crossed 432,000 downloads with 913 likes. It demonstrates how aggressively quantized open-weight models can now reach laptop-friendly footprints while staying useful for local chat and lightweight agent workloads.
Technical depth angle: A 27-billion-parameter model is stored in ternary form — each weight is one of three values instead of the typical sixteen at four bits. The full parameter count is preserved while the on-disk and in-memory footprint shrinks enough to fit a 27B chat model into laptop RAM, with CUDA and Metal acceleration so it runs on both Nvidia and Apple Silicon hardware without a hosted API.
Actionability angle: What this means: a 27-billion-parameter open-weight model now genuinely fits in laptop RAM, which makes a private, fully offline conversational assistant practical rather than theoretical. Why this matters: builders who need data to stay on-device can pull the GGUF, point llama.cpp at it, and run on Nvidia or Apple Silicon hardware in minutes.
Listener hook: If you have ever wanted a real-sized language model running privately on your own laptop, this is the release that finally makes that pitch believable.

8. **Anthropic's $1.5B Pirated-Books Settlement Gets Final Court Approval**
A federal judge gave final approval to Anthropic's $1.5 billion settlement over pirated books used to train its Claude models. The deal, in a case brought by authors including Bartz, compensates writers whose works were downloaded from pirate sources and folded into Claude's training data. It ends one lawsuit but leaves open the broader question of whether training AI on copyrighted material without permission counts as fair use — a question still pending in similar lawsuits against other AI companies.
Technical depth angle: The settlement covers authors whose books were downloaded from pirate sources and used in Claude's training corpus. The court approved the dollar amount but did not rule on whether training an AI on copyrighted books without permission is fair use — that question stays open and will be decided case by case in remaining lawsuits. Anthropic's deal resolves exposure for one company without creating a binding precedent.
Actionability angle: This means AI companies whose training pipelines touched pirated text now face a clearer financial exposure model — $1.5 billion for a single class action. Buyers of AI tools have reason to ask vendors whether their training data provenance can survive the same kind of lawsuit, since this settlement could pressure the industry toward licensing book corpora or shifting to licensed-only sources.
Listener hook: A federal court just put a $1.5 billion price tag on training an AI on pirated books — and every other lab is watching what comes next.

9. **digest:github listing adds**
A new paper, SWE-Pruner Pro, argues that coding agents already encode internal signals about which parts of long tool output matter — no external classifier required. A small trained head reads those internal signals and drops irrelevant chunks before they reach the prompt. The upshot is faster, cheaper runs on long coding tasks because pruning happens inside the model instead of as a separate pass.
Technical depth angle: The agent's own internal representations of code relevance, read by a small attached head, drive the pruning decision — replacing a separate external classifier with signals the model already carries.
Actionability angle: What this means: context pruning can move from a bolted-on classifier to something the model handles internally. Why it matters: it points toward lower latency and cost on long coding sessions, and it's worth watching whether open coding agents adopt self-pruning as a default layer.
Listener hook: If your coding agent keeps tripping over its own context, the fix might be hiding inside the model itself.

10. **OpenAI and Hugging Face Disclose Model Evaluation Security Incident**
OpenAI and Hugging Face have jointly published early findings from a security incident that took place during AI model evaluation. The post, dated July 21, 2026, characterizes the threat actors as showing advanced cyber capabilities and frames the disclosure as lessons for defenders. It is deliberately light on technical specifics, signaling an emerging norm of cross-lab security disclosure around evaluation infrastructure.
Technical depth angle: The post shares early findings only and is intentionally vague on technical specifics. Its main concrete claim is that the threat actors showed advanced cyber capabilities — meaning the eval environment was probed by something beyond commodity tooling. No exploit chain, malware family, or attacker attribution is disclosed.
Actionability angle: What this means: the joint disclosure treats evaluation pipelines as production-grade assets — segmented, logged, and audited the same way you would harden any system that handles untrusted code. Why this matters: eval environments are increasingly attractive targets because they sit close to weights and downstream serving infrastructure, so a foothold in eval gets you uncomfortably close to the rest of the stack.
Listener hook: When two of the biggest AI labs team up to publish a security warning, the rest of the industry should probably pay attention.

11. **Research digest: Why long-context reasoning models copy-paste your prompt instead of thinking**
Researchers have identified a pervasive failure mode in long-context reasoning models: instead of working through a problem, they copy chunks of the user's prompt into their reasoning steps. The behavior intensifies as context grows, and models that copy from irrelevant parts of the input are far more likely to reach the wrong answer. The team designed a training reward that scores models for grounding their reasoning in the actual evidence and penalizes them for echoing filler. Across multiple model sizes, the approach added up to 4.6 points over standard training on average, with the largest gains at the longest contexts and shorter reasoning traces as a side benefit.
Technical depth angle: The paper's key claim is that long-context reasoning degrades because models copy indiscriminately from any nearby text, relevant or not, rather than focusing on the evidence that actually answers the question. The fix is a training signal that rewards grounding in real evidence and penalizes echo from filler. The headline number is up to 4.6 points over standard training, with bigger gains at longer contexts.
Actionability angle: For builders using long-context reasoning models, the practical implication is that copy-paste behavior is a leading indicator of wrong answers — especially at longer context lengths. That's worth checking when picking a model or evaluating one in production, because standard accuracy benchmarks may not surface the failure. Watch for grounding-aware training to show up in released reasoning models over the coming months.
Listener hook: If you've ever watched a reasoning model regurgitate your prompt instead of thinking, this paper explains exactly why.

12. **XcodeBuildMCP 2.6.2 Gives Coding Agents Real Access to Apple Builds**
Sentry has released version 2.6.2 of XcodeBuildMCP, a Model Context Protocol server and CLI that lets AI coding agents work with iOS and macOS projects. The repository, which now shows more than 6,100 stars on GitHub, exposes Xcode-related tooling to assistants that speak MCP. The June 2 release and a July 22 repository push signal steady maintenance from Sentry's open source team.
Technical depth angle: XcodeBuildMCP is a local Model Context Protocol server that exposes Xcode tooling as MCP tools a coding agent can call. The CLI companion wraps the same surface for terminal-driven workflows, so the agent and the developer can both drive Apple project work from inside or outside the assistant.
Actionability angle: iOS and macOS developers can wire an MCP-speaking coding assistant straight into their project workflow, so the agent handles more than code edits and stays useful through build and test. For teams already using Sentry, this is a natural extension of their existing toolchain. Why this matters is that AI-assisted Apple platform development now has a concrete, open source bridge rather than a vague promise.
Listener hook: If you build for Apple platforms, your AI assistant can finally reach past code edits into the build itself.

13. **Community Qwen 3.6 MoE Variant Tops Hugging Face Trending**
A community fine-tune of Qwen 3.6 is climbing the Hugging Face trending charts. HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive is a multimodal Mixture-of-Experts model distributed in GGUF format for local inference, with vision and text-to-text capabilities and reduced safety filtering baked into its fine-tune. The naming pattern indicates roughly 35 billion total parameters with about 3 billion active per token, and the listing has racked up close to 2 million downloads and just under 3,000 likes. It's a useful signal of where open-weight consumers are spending attention: repackaged, re-fine-tuned variants of recent base models running locally.
Technical depth angle: The model uses an MoE architecture — roughly 35B total parameters with 3B active per token — packaged as a GGUF quant for llama.cpp local inference. It accepts both image and text input (image-text-to-text), and the 'uncensored' and 'aggressive' tags indicate a community fine-tune with reduced refusal behavior versus the upstream Qwen 3.6 base.
Actionability angle: For builders running local agents, this signals that community-quantized multimodal MoE variants are a realistic option for hobby rigs with consumer GPUs. If you want a vision-capable local model with looser filtering for experimentation, this listing is worth pulling and benchmarking against your current stack.
Listener hook: If you've been waiting for a vision-capable MoE you can actually run at home without an API key, this trending listing is the closest thing to a current answer.

14. **Bristol Myers Squibb Builds a Vera Rubin SuperPOD for Drug Discovery**
Bristol Myers Squibb is deploying a second NVIDIA DGX SuperPOD, this one built from eight DGX Vera Rubin NVL72 systems. The pharmaceutical company says the cluster will be available to scientists across its global research organization for predictions, model training, and agentic workflows spanning the drug-discovery pipeline. Its existing SuperPOD has already helped researchers cut weeks from target-identification work and expand a library of compounds designed to degrade cancer-causing proteins.
Technical depth angle: Each of the eight rack-scale systems combines NVIDIA Vera CPUs with Rubin GPUs. NVIDIA claims the new cluster will deliver up to ten times the performance per megawatt of the infrastructure it replaces, while BioNeMo Agent Toolkit and Mission Control provide biological-AI workflows and a unified operating layer. BMS plans to join the old and new clusters through one data plane shared across its research sites.
Actionability angle: This is a concrete example of enterprise agentic AI moving beyond office automation into scientific infrastructure. The important signal for builders is not just a larger GPU purchase; it is the decision to expose shared compute, models, and accumulated experimental data through plain-English prediction workflows for working scientists.
Listener hook: A drug company is giving every scientist access to a Vera Rubin AI factory, and it already has evidence that the first cluster saved weeks of lab work.

---

## Editorial Mix Check

- flagship_products: 4
- builder_projects: 7
- local_ai: 3
- hardware_compute: 2
- policy_regulation: 1
- research: 2

---

## Model Discovery Check

- **Google: Gemini 3.6 Flash** (google) — Newly listed this cycle (verified July 22, 2026). Primary source: https://openrouter.ai/models/google/gemini-3.6-flash. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 1048576 tokens; modality: see primary source. Capabilities: context length 1048576; Gemini 3.6 Flash is a high-efficiency model from Google for coding, agentic workflows, and web and app development. It is designed to produce polished outputs with fewer unnecessary edits and.... Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/google/gemini-3.6-flash and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **Google: Gemini 3.5 Flash-Lite** (google) — Newly listed this cycle (verified July 22, 2026). Primary source: https://openrouter.ai/models/google/gemini-3.5-flash-lite. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 1048576 tokens; modality: see primary source. Capabilities: context length 1048576; Gemini 3.5 Flash-Lite is a high-efficiency model from Google with upgraded agentic capabilities. It is suited for subagents that execute focused tasks within complex, multi-agent workflows.. Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/google/gemini-3.5-flash-lite and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

---

## Local LLM Spotlight

- **thinkingmachines/Inkling** — https://huggingface.co/thinkingmachines/Inkling — Inkling is a multimodal mixture-of-experts model from Thinking Machines that handles image-text-to-text and audio-text-to-text conversational tasks, released under Apache 2.0 and shipped in safetensors with published eval results and an endpoints-compatible interface. The MoE routing keeps inference cost closer to a smaller model while preserving broad multimodal coverage, so you can load weights locally or hit it through the Hugging Face inference endpoint. It is trending on Hugging Face with 1404 likes and 16441 downloads.
  Try now: Pull the safetensors weights into a local transformers loader and run an image-plus-audio caption through a 4-bit quantized variant to benchmark latency and quality on your workstation GPU.

---

## GitHub Project Radar

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — FastMCP is a Python framework for building Model Context Protocol servers and clients with minimal boilerplate, using decorators and type hints so tool authors can expose functions as MCP-callable resources in a few lines. `stars: 26,752`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v3.4.4 (2026-07-09)`.
  Why this is on the radar now: v3.4.4 shipped on 2026-07-09 and the repository was updated on 2026-07-21.
  Stack improvement angle: Drop FastMCP into a Codex or Claude Code stack so agents register native Python functions as MCP tools, removing the JSON-schema glue that usually clutters the tool layer.
  Try now: Run pip install fastmcp and scaffold a server with the @mcp.tool decorator to expose a custom Python function, then call it from a local Codex or Claude Code session over MCP.

- **microsoft/mcp-for-beginners** — https://github.com/microsoft/mcp-for-beginners — Microsoft's MCP-for-Beginners is a multi-language curriculum covering Model Context Protocol fundamentals through runnable labs in .NET, Java, TypeScript, JavaScript, Rust, and Python, each focused on practical, modular agent workflows. `stars: 16,812`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: none published on GitHub as of 2026-07-22`.
  Why this is on the radar now: The repository was updated on 2026-07-21 and enters the radar with 16,812 stars.
  Stack improvement angle: Hermes and OpenClaw operators can use the cross-language labs to give agents a shared vocabulary for MCP, so polyglot service backends all surface tools through the same protocol.
  Try now: Clone the repo, finish the Python 'MCP Server' lab, and point a Claude Code session at the local server to confirm the round-trip works end to end.

- **CoplayDev/unity-mcp** — https://github.com/CoplayDev/unity-mcp — Unity MCP is an in-Editor plugin that exposes Unity Editor functions, including asset management, scene control, script edits, and automation, as MCP tools for AI assistants. `stars: 12,741`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v10.1.0 (2026-07-13)`.
  Why this is on the radar now: v10.1.0 shipped on 2026-07-13 and the repository was updated on 2026-07-13.
  Stack improvement angle: Wire Unity MCP into a Claude Code or OpenClaw agent and it can drive compile-and-play loops, scene edits, and asset queries without bespoke Editor scripting glue.
  Try now: Install the package via the Unity Package Manager, launch the Editor, and connect Claude Code to it so you can fire a 'play scene' tool call against an empty project.

---

## Extra Research Candidates

- **getsentry/XcodeBuildMCP — A Model Context Protocol (MCP) server and CLI that provides tools for agent use ** — https://github.com/getsentry/XcodeBuildMCP — A Model Context Protocol (MCP) server and CLI that provides tools for agent use when working on iOS and macOS projects. GitHub reports 6106 stars. Latest release: v2.6.2 2026-06-02T20:38:36Z. Repository pushed 2026-07-22T10:09:34Z. Technical depth angle: It wraps xcodebuild and the iOS Simulator CLI behind MCP tool definitions, exposing build targets, schemes, and device lifecycle as structured function calls an agent can invoke.

- **David Vélez and Robin Vince join the boards of the OpenAI Foundation and OpenAI Group PBC** — https://openai.com/index/david-velez-robin-vince-join-openai-boards — David Vélez and Robin Vince join the boards of the OpenAI Foundation and OpenAI Group PBC, bringing global leadership in finance, technology, and governance. Technical depth angle: New independent directors at the OpenAI Foundation and OpenAI Group PBC change the oversight path for compute commitments and equity structure, which downstream agent stacks depend on for stable model and API access.

- **Safety and alignment in an era of long-horizon models** — https://openai.com/index/safety-alignment-long-horizon-models — OpenAI shares lessons from deploying long-running AI models, highlighting new safety risks, observed failures, and improved safeguards through iterative deployment. Technical depth angle: Long-running agent sessions expose context drift and goal misgeneralization, and the piece addresses those failure modes through iterative deployment, runtime monitoring hooks, and a red-team failure inventory.

---

## Show Notes

```md
Episode 091 — July 22, 2026

[00:00] Episode hook

OpenAI Codex rust-v0.145.0 has stabilized its multi-agent V2 experience, introducing granular configuration for sub-agent models, reasoning levels, and concurrency while restoring essential role definitions. This release includes an updated /import command designed to migrate Cursor configurations directly into the Codex environment, streamlining the transition for developers moving between agentic IDEs. Google expanded its model reach by listing Gemini 3.6 Flash on OpenRouter, a high-efficiency model optimized for coding tasks and agentic workflows requiring low-latency responses. Jack Dorsey’s Block has launched Buzz, a workplace platform that integrates group chat, AI agents, and Git hosting into a unified feed to reduce friction between development work and team communication. MinishLab released Semble v0.1.0, an open-source code search tool that claims a 98% reduction in token consumption for AI agents. whodb reached version 0.121.0 on July 16, crossing 4,900 stars on GitHub, while the local-first super agent holaOS gained traction for retaining user context across sessions.

[02:00] Agent Stack Release Readout: OpenAI Codex rust-v0.145.0

OpenAI Codex rust-v0.145.0 shipped this week, and the headline change is real for anyone running multi-agent workflows: the opt-in multi-agent V2 experience is now stabilized. That means the parallel sub-agent mode that used to drag you into weird rollback states finally behaves. You can configure which model each sub-agent uses, set reasoning levels per sub-agent, dial concurrency up or down, and the navigation between agents has been cleaned up so you stop losing track of which worker is doing what. Restored roles mean a coder and a reviewer can stay distinguishable across a long session instead of merging into one blob.

The second piece worth your time is /import. Codex used to only import its own settings. Now you can pull in Cursor or Claude Code configs — MCP servers, plugins, sessions, custom commands, and even project-scoped memories. If you've been bouncing between tools and dreading the rebuild, this is the on-ramp that keeps your context intact.

Two more things to know. Amazon Bedrock support is now experimental, with custom endpoints and authentication, and GPT-5.6 Sol becomes the default Bedrock model — useful if you're routing enterprise traffic through AWS. Audio inputs and tool outputs arrived too, including common local audio formats and streaming realtime V3 conversations, which means you can pipe voice into a working session and hear the model back without bolting on a separate realtime client. The terminal UI also gained clickable inline visualization links so figures open in your browser instead of dumping escape sequences.

Under the hood, the team fixed the worst papercuts. Editing an earlier prompt or retrying a safety-buffered turn now creates a contextual branch instead of nuking attachments and mention bindings. Terminal responsiveness improved for long sessions via incremental Markdown rendering and bounded command output. MCP startup finally has timeouts, so a broken OAuth discovery no longer freezes the whole session, and Windows sandboxing got a real fix with native exec-server support and network-proxy enforcement.

What this means: if you've been holding off on multi-agent because it felt rough, the V2 stabilization is the moment to try it. If you've been trapped in Cursor or Claude Code and wanted Codex without rebuilding your setup, /import is the on-ramp. Watch next whether Bedrock stays experimental or ships broadly, and whether the audio input pipeline shows up in headless CI runs or stays local-only.

[03:47] Google's Gemini 3.6 Flash on With Million-google listing adds gemini-3.6-flash

Google just added Gemini 3.6 Flash to OpenRouter's model catalog, giving developers an immediately routable way to send work through the platform without leaving the interface they already use. The model is positioned as a high-efficiency option from Google, aimed squarely at coding, agentic workflows, and web and app development, with the Flash tier's typical emphasis on efficiency over maximum capability.

The headline spec is the context window: one million, forty-eight thousand, five hundred and seventy-six tokens. That is the full million-token class Google's Flash line has been pushing, and it changes what you can hand to the model in a single call. Drop a large repository in one prompt. Keep a long agent trace, tool call history, and retrieval snippets together without aggressive summarization. Feed a feature spec, the surrounding files, and a failing test in one shot. For agentic loops especially, where every turn accumulates state, the headroom reshapes how you structure prompts rather than just how much you can paste.

Google's description also points at the model's editing behavior, claiming it produces polished outputs with fewer unnecessary edits. That phrasing is doing real work. In agentic coding, models that churn on a file, reverting and rewriting the same lines, eat tokens and time. A model that lands closer to a finished diff on the first pass is cheaper to run, even before any Flash-tier efficiency pricing shows up, and friendlier to review.

Two things worth watching: whether that cleaner-edit behavior holds up on real workloads, with your own codebase and tests in hand, and how latency and cost stack up against other Flash-tier options already on OpenRouter once people start measuring.

[05:31] Jack Dorsey launches Buzz: chat, AI agents, and Git in one feed

Jack Dorsey is shipping a new workplace chat product, and this one treats AI agents like members of the team. Buzz, launched this week from Block, is a group chat platform for the workplace that puts humans and their AI agents in the same conversation, with Git hosting woven in so commits and code review live in the same place as the discussion itself. The idea is to collapse three tools that teams juggle every day, group chat, version control, and agent output, into a single feed. In practice that means an engineer can loop an AI agent into a thread the same way they would ping a coworker, hand it a task, and watch the response unfold in the same channel where the rest of the team is already talking. Because Git is part of Buzz, the commits and pull requests that come out of those conversations stay attached to the chat that produced them, which keeps the why behind every change from drifting into a separate tool. The launch lands in a market already crowded with established chat platforms like Slack and Microsoft Teams. Buzz's bet is that agent teammates deserve a real seat at the table rather than a sidebar widget, and the Hacker News thread around the announcement, sitting at 330 points within hours of going live, suggests developers are at least curious about the approach. For builders, the implication is straightforward. If Buzz delivers on the vision, small teams can stop stitching together chat, repo, and agent runtime themselves and let the platform hold the threads in sync. What to watch next is how the agent permissions model is set up, because giving a bot real write access to your repo turns it from a clever assistant into a coworker with the keys to production.

[07:24] Semble ships a 98% leaner code search for AI agents

If you've watched an AI coding agent grind through a codebase, you've seen the failure mode. It runs grep, reads dozens of files, and burns through tens of thousands of tokens just to find the function definition. A project called semble, from MinishLab, is built to sidestep that loop. The team shipped v0.5.2 on July 21, and the headline claim is roughly 98% fewer tokens than a naive grep-plus-read pipeline for the same query.

That gap matters because search is usually the single most expensive step in an agent's workflow, not the generation. If the model can ask "where is the retry handler defined?" and get back a small, focused answer instead of a multi-thousand-token file dump, the agent stays coherent on longer refactors and the user pays a fraction of the API cost.

The contrast is the whole pitch. Grep returns line numbers, read pulls whole files, and the agent has to mentally reassemble context. Semble skips that reconstruction by handing the model something it can act on directly.

Semble presents itself as a code search backend that any agent harness can call into, rather than a chat product or an IDE plugin. The repo has accumulated more than 5,600 GitHub stars, with both a release and additional commits landing within the past 24 hours.

For builders, the practical question is whether search dominates your agent's token bill today. If it does, this is the highest-leverage swap available, and the natural first step is replacing the grep-and-read stage in your harness with a focused search tool. Watch for credible benchmarks on real repos and for the first formal integrations with popular agent CLIs, which is when a curiosity becomes default infrastructure.

[09:10] whodb crosses 4,900 stars with active shipping pace

A project called whodb surfaced on the radar this week with notable momentum. The open-source repository, hosted under user clidey on GitHub, now sits at roughly 4,930 stars. It shipped release 0.121.0 on July 16, then received another repository push six days later on July 22 — meaning the maintainers shipped more than once inside a single week.

The project describes itself with a short tagline: "where data access meets operational intelligence." That single line tells you the maintainers are aiming at a busy intersection — the overlap between tools that let you query data and tools that help you understand what is happening inside the systems that hold it. The 0.121.0 version number, paired with that week-of-shipping pace, points to a project in active iteration rather than a stable, settled product. Each release reads as a checkpoint, not a milestone, and that is normal at this early stage of a fast-moving project.

For builders, the question is whether whodb becomes worth a real bet. The signals worth watching are concrete and easy to track from the GitHub page. Will the star count cross 5,000 and keep climbing? Will the maintainers commit to a 1.0 release, which would tell you the surface area feels settled? And will the "operational intelligence" half of the tagline turn into shipping capability — or stay a positioning line on the README?

What this lets you do today is straightforward: clone the repo, try the current build, and judge for yourself whether the project deserves a place in your stack. What it lets you build tomorrow depends on what the next ten releases actually deliver — and on whether the maintainers keep that shipping cadence.

[10:56] holaOS Aims to Be Your Local-First Work Agent

holaOS is positioning itself as a different kind of work assistant, and the pitch is simple: it runs locally, learns your working context in minutes, and never forgets it. The project sits on GitHub under the holaboss-ai organization and has already pulled in more than 5,500 stars, with commit activity as recent as July 20.

The framing matters here. Most work agents people talk about today send your files, your prompts, and your project state off to a remote server, then build up a memory profile that lives in someone else's cloud. holaOS is built around the opposite idea. The agent lives on your own machine, figures out what you are working on within minutes, and holds onto that context permanently. That local-first approach is the headline feature, and it is also the main reason a privacy-conscious builder, a freelancer handling client material, or a company worried about leaking internal documents would even look at it.

For now, the repository does not carry a tagged release on GitHub, so the README and commit history are the best window into what is actually being built. Treat it as an actively developed project worth watching rather than a finished product you install today. The interesting question is how the persistent memory will work in practice. Will the agent really retain the full picture of a multi-week project, or will it summarize and prune like every other tool? That is the bet the team is making, and it is the bet that 5,500 GitHub stars suggest a real audience is curious about.

What to watch next: a first tagged release that reveals how the context-learning actually runs, and any demo showing the agent handling a real multi-day project without dropping details.

[12:45] A 27B Open-Weight Model Now Fits in Laptop RAM

A 27-billion-parameter open-weight model is now running comfortably on laptops, and the download counter is climbing fast. The repo, prism-ml/Ternary-Bonsai-27B-gguf, was published on July 4 by the prism-ml team on Hugging Face as a GGUF package that plugs directly into llama.cpp. Within days of release it passed 432,000 downloads and gathered 913 likes, putting it near the top of the trending board.

The headline detail is the compression. The model keeps all 27 billion parameters, but every weight is stored as one of three possible values — a technique called ternary quantization. The aggressive compression is why the file footprint drops into a range that a modern laptop with 16 or 32 gigabytes of unified memory can handle on its own, with no hosted API required and no data leaving the machine. It is the move that puts a 27B chat model into RAM rather than forcing builders to stream weights from disk.

For individual builders and small teams, that is the meaningful line — it is the difference between needing a workstation-class machine and being able to run a 27B model on the laptop you already carry around.

Acceleration support is part of the release. The package runs on CUDA for Nvidia cards and on Metal for Apple Silicon Macs, so builders can pick the hardware they already own. For local chat and lightweight agent loops, the practical recipe is straightforward: pull the GGUF, point llama.cpp at it, and you have a private conversational model running on your own machine in minutes, fully offline.

What to watch next is how well those tightly compressed weights hold up on harder reasoning tasks. Aggressive quantization tends to degrade faster on multi-step chains than on single-turn chat, so independent evaluations on longer-context reasoning tests will be the real signal for whether this is a genuine quality shift or just a footprint story.

[14:42] Anthropic's $1.5B Pirated-Books Settlement Gets Final Court Approval

A federal judge signed off on Anthropic's $1.5 billion settlement over pirated books used to train Claude, ending the lead case brought by authors including Bartz. The deal compensates writers whose books were downloaded from pirate sources and folded into Claude's training data. The court approved the dollar figure, but the ruling does not answer the question it raised: whether training an AI on copyrighted books without permission counts as fair use. That question stays live in similar lawsuits against other AI companies, so this is one chapter closing while the broader fight over training data continues. What makes the settlement concrete is the number. Anthropic is paying $1.5 billion to resolve claims from the author class — works that authors never agreed to license for AI training. For anyone building or buying AI, that figure sets a reference point for what exposure looks like when a model is trained on material scraped from pirated sources. Three things shift in practice. Authors covered by this deal get paid for work showing up inside Claude's training mix. Anthropic has publicly accepted a settlement rather than continuing to litigate a fair-use defense. Every other lab that touched pirated book archives now has a template for what a negotiated resolution costs. The story drew hundreds of comments on Hacker News, a sign of how closely developers, authors, and AI buyers are tracking the outcome. What to watch next: how remaining copyright lawsuits against other AI companies are argued, and whether any of them produce a court ruling that actually defines fair use for AI training. The industry still does not have a clear legal line on training AI on copyrighted text.

[16:26] digest:github listing adds

Coding agents chew through long tool outputs as they read files and run commands, and trimming that context is a real bottleneck on long tasks. A new paper called SWE-Pruner Pro argues you don't need a separate filter to decide what to keep — the agent already knows. The authors find that the model carries internal signals about which pieces of code matter, and a small trained head can read those signals to drop irrelevant chunks before they hit the prompt. In plain terms, the agent does its own triage instead of relying on an outside classifier. That matters because it removes a whole extra model from the loop, which means faster runs and lower cost on long coding sessions. For builders, it points toward a future where context pruning lives inside the model rather than bolted on as a separate stage. Worth watching: whether open coding agents pick up self-pruning as a standard layer, and how it behaves when tool outputs grow even longer.

[17:29] OpenAI and Hugging Face Disclose Model Evaluation Security Incident

OpenAI and Hugging Face jointly published early findings from a security incident that took place during model evaluation. The joint post appeared on July 21, and it pulls back the curtain on something most labs would prefer to keep quiet — what happens when adversarial pressure meets an evaluation pipeline that handles weights, prompts, and downstream infrastructure. The headline takeaway is that the threat actors involved showed advanced cyber capabilities. That's a deliberate, careful phrase. It signals that whoever probed the evaluation environment was not running off-the-shelf malware or commodity tooling. The two labs are framing this as a learning moment for defenders, and that framing matters because evaluation pipelines are increasingly attractive targets. They sit close to model weights, gradient data, and serving infrastructure. A foothold in eval is not the same as a foothold in production, but it gets you uncomfortably close to the rest of the stack. The post is deliberately light on details — it is labeled early findings — and that is itself a useful signal. Labs are working out in real time how much to disclose when an incident touches shared infrastructure or shared evaluation practices, without handing a roadmap to the next attacker. The joint format is also notable: two competing labs publishing a security warning together is rare. What can builders take away? Treat evaluation environments the way you treat any system that ingests untrusted code or external model artifacts: segment the network, log aggressively, audit who can touch weights, and assume that an attacker who lands in eval will try to pivot toward training data or serving endpoints. What to watch next: a fuller post-incident write-up with concrete mitigations, and whether other major labs adopt similar joint disclosure norms.

[19:17] Research digest: Why long-context reasoning models copy-paste your prompt instead of thinking

When you hand a reasoning model a really long document — say, a 200-page contract or a full codebase — it has a habit you wouldn't expect: it starts copy-pasting chunks of your prompt back at you instead of actually working through the problem. New research identifies this as a core failure mode in long-context LLMs, and shows it gets worse the longer the input gets. The root cause isn't capacity — it's that models copy from the prompt indiscriminately, grabbing whatever text is nearby instead of focusing on the evidence that matters. The ones that latch onto irrelevant material tend to answer wrong. The team built a training reward that pays models for grounding their reasoning in evidence that matters and docks them for echoing filler. Across multiple model sizes, that approach added up to 4.6 points over standard training, with the biggest gains at the longest contexts and shorter reasoning traces as a bonus. Watch whether this grounding signal gets adopted in next-gen reasoning models, and whether it holds up on adversarial long inputs.

[20:24] XcodeBuildMCP 2.6.2 Gives Coding Agents Real Access to Apple Builds

Apple platform developers just got a more capable copilot for the trickiest part of their day. Sentry has shipped version 2.6.2 of XcodeBuildMCP, a Model Context Protocol server and CLI that hands an AI agent real access to iOS and macOS projects. The tool sits between a coding assistant and Xcode itself, opening up parts of an Apple build that agents normally cannot reach. GitHub now shows more than 6,100 stars on the repository, and the latest release shipped on June 2 of this year.

In plain English, MCP, the Model Context Protocol, is a standard that lets assistants call external tools through a defined interface. XcodeBuildMCP uses that standard to expose Xcode-related work — the things that happen after a developer hits build or test — to an AI assistant, so an agent on an Apple project can do more than just edit text files. Because it runs as a local server, the assistant stays in the loop while work actually happens on the developer's machine.

What this means for builders is real workflow gain. You can point a coding agent at an iOS app or a macOS project, and instead of stopping at code edits, the assistant can drive the rest of the build loop through the MCP connection. Teams that already run Sentry for crash reporting get an extra reason to keep everything in that ecosystem, since the project is maintained by Sentry's open source team.

The thing to watch next is adoption. The repository was pushed as recently as July 22, which signals steady maintenance, and the more interesting question is whether Apple's own developer tools will start speaking MCP natively. Until then, this project is the most practical bridge between an AI assistant and an Xcode build.

[22:14] Community Qwen 3.6 MoE Variant Tops Hugging Face Trending

A community-built take on Qwen 3.6 is climbing the Hugging Face trending charts this week. The repository is HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive — a multimodal Mixture-of-Experts model distributed in GGUF format, with vision and text-to-text capabilities and reduced safety filtering baked into its fine-tuning.

The '35B-A3B' naming pattern points to the design intent: roughly 35 billion total parameters with about 3 billion active per token, which is the hallmark of an MoE build — large capacity on paper, but cheaper to run per query than a dense model of the same total size. The GGUF tag means it drops straight into the llama.cpp ecosystem, so anyone with a consumer GPU or a high-RAM laptop can load it locally.

Who shipped it: a community publisher called HauhauCS. The engagement numbers are real — close to 2 million downloads and just under 3,000 likes on the hub, with the listing tagged for English, vision, and multimodal use across the qwen3.6 family of tags. The 'uncensored' and 'aggressive' labels point to a fine-tune aimed at local agent work and use cases where developers want fewer refusals than the upstream base model.

What this enables: a multimodal MoE you can run at home, feed images into, and wire into a local agent stack — full control over the weights, no external API call required, and the kind of freedom to experiment that cloud-only models rarely offer. It's a useful snapshot of where the open-weight community spends its energy: repackaging, re-fine-tuning, and redistributing the latest base models in forms the labs themselves don't ship.

One thing to watch: whether the download curve on this listing keeps climbing, which would signal that community-quantized MoE variants are becoming the default way local AI builders consume new base models.

[24:03] Bristol Myers Squibb builds a Vera Rubin SuperPOD for drug discovery

Bristol Myers Squibb is doubling down on AI infrastructure for drug discovery. The pharmaceutical company is deploying its second NVIDIA DGX SuperPOD, this one built from eight rack-scale DGX Vera Rubin NVL72 systems, and it intends to open the cluster to scientists across its global research organization.

Each system combines NVIDIA Vera CPUs with Rubin GPUs. NVIDIA says the new cluster can deliver up to ten times the performance per megawatt of the infrastructure it replaces. BMS is also bringing in the BioNeMo Agent Toolkit for biological AI and Mission Control as the operating layer, then joining the old and new SuperPODs through a single data plane shared across research sites.

The meaningful part is that BMS already has evidence from its first SuperPOD. AI-assisted target identification has saved scientists weeks of manual work. Researchers have used models to expand a library of compounds designed to degrade cancer-causing proteins, and they use predictions to prioritize which molecules are worth synthesizing before spending scarce laboratory time.

Now the company wants those capabilities available without site-specific access barriers or deep computational expertise. Researchers will be able to initiate complex predictions in plain English, while experimental data and model results accumulate into a shared learning loop across locations.

For builders, this is a concrete picture of agentic AI becoming scientific infrastructure. The bet is not simply that more GPUs make research faster. It is that shared compute, domain models, and accumulated experimental knowledge can become an accessible system used at every stage of discovery instead of a specialist resource that scientists wait in line to use.

[25:51] Practical queue

From today's stories: Multi-agent runs are finally stable enough for real work — try a parallel investigation or refactor before trusting it on production code. Builders using OpenRouter can now route coding and agentic workloads to Gemini 3.6 Flash through the existing interface, taking advantage of the million-token window for large repositories and long agent traces. What this means for builders is that small teams may be able to stop stitching together chat, repo, and agent runtime themselves, since Buzz aims to keep those layers in one place. If your agent's token bill is dominated by search, a focused code-search backend is the highest-leverage swap available. What this means: the project is worth a quick evaluation if you work in the data tooling space, since the active pace is the kind of signal that tells you whether the maintainers are building or maintaining. This matters for builders who want a work agent that holds onto project context over weeks without shipping sensitive files to a third party. What this means: a 27-billion-parameter open-weight model now genuinely fits in laptop RAM, which makes a private, fully offline conversational assistant practical rather than theoretical. This means AI companies whose training pipelines touched pirated text now face a clearer financial exposure model — $1.5 billion for a single class action. What this means: context pruning can move from a bolted-on classifier to something the model handles internally. What this means: the joint disclosure treats evaluation pipelines as production-grade assets — segmented, logged, and audited the same way you would harden any system that handles untrusted code. For builders using long-context reasoning models, the practical implication is that copy-paste behavior is a leading indicator of wrong answers — especially at longer context lengths. iOS and macOS developers can wire an MCP-speaking coding assistant straight into their project workflow, so the agent handles more than code edits and stays useful through build and test. For builders running local agents, this signals that community-quantized multimodal MoE variants are a realistic option for hobby rigs with consumer GPUs. Bristol Myers Squibb's second SuperPOD shows agentic AI becoming shared scientific infrastructure rather than an isolated office assistant.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: OpenAI Codex rust-v0.145.0 / Google's Gemini 3.6 Flash on With Million-google listing adds gemini-3.6-flash / Jack Dorsey launches Buzz: chat, AI agents, and Git in one feed
- 02:00 — Agent Stack Release Readout: OpenAI Codex rust-v0.145.0
- 03:47 — Google's Gemini 3.6 Flash on With Million-google listing adds gemini-3.6-flash
- 05:31 — Jack Dorsey launches Buzz: chat, AI agents, and Git in one feed
- 07:24 — Semble ships a 98% leaner code search for AI agents
- 09:10 — whodb crosses 4,900 stars with active shipping pace
- 10:56 — holaOS Aims to Be Your Local-First Work Agent
- 12:45 — A 27B Open-Weight Model Now Fits in Laptop RAM
- 14:42 — Anthropic's $1.5B Pirated-Books Settlement Gets Final Court Approval
- 16:26 — digest:github listing adds
- 17:29 — OpenAI and Hugging Face Disclose Model Evaluation Security Incident
- 19:17 — Research digest: Why long-context reasoning models copy-paste your prompt instead of thinking
- 20:24 — XcodeBuildMCP 2.6.2 Gives Coding Agents Real Access to Apple Builds
- 22:14 — Community Qwen 3.6 MoE Variant Tops Hugging Face Trending
- 24:03 — Bristol Myers Squibb builds a Vera Rubin SuperPOD for drug discovery
- 25:51 — Practical queue

---

## Primary Links

- OpenAI Codex rust-v0.145.0 release: https://github.com/openai/codex/releases/tag/rust-v0.145.0
- Google: Gemini 3.6 Flash model page: https://openrouter.ai/models/google/gemini-3.6-flash
- Google: Gemini 3.5 Flash-Lite model page: https://openrouter.ai/models/google/gemini-3.5-flash-lite
- Jack Dorsey launches Buzz to combine team chat, AI agents and Git host: https://runtimewire.com/article/jack-dorsey-block-buzz-team-chat-ai-agents-git
- MinishLab/semble — Fast and Accurate Code Search for Agents. Uses ~98%: https://github.com/MinishLab/semble
- clidey/whodb — Where data access meets operational intelligence: https://github.com/clidey/whodb
- holaboss-ai/holaOS — Your super agent for work: local-first, learn you: https://github.com/holaboss-ai/holaOS
- prism-ml/Ternary-Bonsai-27B-gguf trending on Hugging Face: https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf
- prism-ml/Bonsai-27B-gguf trending on Hugging Face: https://huggingface.co/prism-ml/Bonsai-27B-gguf
- Judge approves $1.5B Anthropic settlement for pirated books used to tr: https://apnews.com/article/ai-anthropic-copyright-settlement-claude-books-bartz-74b140444023898aeba8579b6e9f0d63
- SWE-Pruner Pro: The Coder LLM Already Knows What to Prune: https://github.com/Ayanami1314/swe-pruner-pro
- OpenAI and Hugging Face address security incident during model evaluat: https://openai.com/index/hugging-face-model-evaluation-security-incident/
- Copy Less, Ground More: Overcoming Repetitive Copying in Long-Context : https://arxiv.org/abs/2607.19345
- DeusData/codebase-memory-mcp — High-performance code intelligence MCP : https://github.com/DeusData/codebase-memory-mcp
- getsentry/XcodeBuildMCP — A Model Context Protocol (MCP) server and CL: https://github.com/getsentry/XcodeBuildMCP
- HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive trending on Hu: https://huggingface.co/HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive
- Bristol Myers Squibb builds a Vera Rubin AI factory: https://blogs.nvidia.com/blog/bristol-myers-squibb-building-life-science-industrys-most-advanced-ai-factory-on-nvidia-vera-rubin/
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- microsoft/mcp-for-beginners repo: https://github.com/microsoft/mcp-for-beginners
- CoplayDev/unity-mcp repo: https://github.com/CoplayDev/unity-mcp
- David Vélez and Robin Vince join the boards of the OpenAI Foundation a: https://openai.com/index/david-velez-robin-vince-join-openai-boards
- Safety and alignment in an era of long-horizon models: https://openai.com/index/safety-alignment-long-horizon-models
- thinkingmachines/Inkling: https://huggingface.co/thinkingmachines/Inkling

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.7.1`, published 2026-07-13T22:33:14Z. Recent episode version tags detected: `v2026.7.1-beta.6`, `v2026.7.2-beta.1`, `v2026.7.2-beta.2`, `v2026.7.2-beta.3`. No new stable release this cycle.
- **Hermes Agent** — Latest stable verified: `v2026.7.20`, published 2026-07-20T18:35:55Z. Recent episode version tags detected: `v2026.7.1`, `v2026.7.20`, `v2026.7.7`, `v2026.7.7.2`. No new stable release this cycle.
- **OpenAI Codex** — Latest stable verified: `rust-v0.145.0`, published 2026-07-21T18:21:04Z. Recent episode version tags detected: `rust-v0.144.3`, `rust-v0.144.4`, `rust-v0.144.5`, `rust-v0.144.6`. Selected missing version(s): `rust-v0.145.0`.
- **Claude Code CLI** — Latest stable verified: `2.1.206`, published 2026-07-09T17:54:03.009Z. Recent episode version tags detected: `2.1.205`, `2.1.206`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-07-22). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.7.1` (stable) / `v2026.7.2-beta.3` (prerelease)
- **Hermes Agent** — `v2026.7.20`
- **OpenAI Codex** — `rust-v0.145.0`
- **Claude Code CLI** — `2.1.206`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
