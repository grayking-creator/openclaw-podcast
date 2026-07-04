# AgentStack Daily EP079 — Hermes 2026.7.1, Claude Code 2.1.193, Kimi K2.7 GA, ZCode GLM-5.2 on HN

**Title:** Hermes Agent 2026.7.1 and Claude Code 2.1.193 Ship; Kimi K2.7 Lands in Copilot

**Tagline:** This week's Agent Stack Release Readout lands Hermes Agent v2026.7.1 alongside Claude Code CLI 2.1.193, with Kimi K2.7 Code reaching GA in GitHub Copilot. ZCode ships a GLM-5.2 wrapper that hit the Hacker News front page, Leanstral 1.5 brings open-weights Lean proof generation, and Alibaba bars Claude Code at work citing backdoor risk. Jamesob's GitHub guide curates SOTA LLMs runnable locally, the Safari MCP server lands for web developers, and WebBrain releases an open-source local-first browser agent for Chrome and Firefox. ReContext publishes a training-free long-context harness, Snorkel launches Senior SWE-Bench, plus ghealth CLI, Program-as-Weights, DramaSR-532K, and AgenticSTS.

**Feed description:** The Agent Stack Release Readout this week leads with Hermes Agent v2026.7.1 shipping alongside Claude Code CLI 2.1.193, with Kimi K2.7 Code reaching GA inside GitHub Copilot. ZCode wraps GLM-5.2 and lands on the Hacker News front page, Leanstral 1.5 brings open-weights Lean proof generation, and Alibaba bars Claude Code at work over backdoor concerns. Jamesob's GitHub guide curates locally-runnable SOTA LLMs, WebBrain ships a local-first browser agent for Chrome and Firefox, ReContext publishes a training-free long-context harness, and Snorkel releases Senior SWE-Bench. Plus ghealth CLI, Program-as-Weights, DramaSR-532K, AgenticSTS, and the Safari MCP server.

---

## Story Slate

1. **Agent Stack Release Readout: Hermes Agent v2026.7.1; Claude Code CLI 2.1.193**
The Hermes Agent team shipped v0.18.0 on July 1, 2026, tagged v2026.7.1, after a 12-day push that closed every open P0 and P1 issue and PR in the repository — about 692 highest-priority items resolved out of roughly 1,950 total items closed in this cycle. The release promotes Mixture-of-Agents to a first-class citizen, with named ensembles of models you can pick like any single model, every reference model's reasoning shown to you, and the aggregator's answer streamed live. The agent also gained self-verification against evidence, completion contracts on /goal, and steerable self-improvement via /learn and /journey. Gateway work added scale-to-zero and drain coordination for production-style deployments.
Technical depth angle: Mixture-of-Agents now exposes named ensembles as addressable model identifiers. Each call fans out to the reference models, surfaces every member's reasoning trace to the user, and streams the aggregator's synthesized answer as it's produced. The completion contract on /goal binds the agent's task to verifiable evidence checks rather than self-reported success. Gateway adds scale-to-zero with drain coordination so in-flight sessions can finish before nodes scale down, and subagents now run in the background with proper lifecycle isolation.
Actionability angle: Named mixture-of-agents ensembles can now be invoked the same way you'd pick a single model, so multi-model routing no longer needs custom glue code around it. The /goal completion contract means task success is now verifiable against evidence rather than the agent's own report, which changes how you write prompts for long-running jobs. Gateway scale-to-zero with drain coordination means you can run the agent on serverless or burst-capacity infrastructure without dropping in-flight work. The implications land across OpenClaw, Codex, Claude Code, Hermes, and Antigravity stacks alike.
Listener hook: If you've been writing glue code to orchestrate multiple models or babysitting agents that declare themselves done too early, the July 1 Hermes Agent release is the one that finally addresses both pain points.

2. **ZCode Harness Wraps GLM-5.2, Hits Hacker News Front Page**
Z.ai's ZCode, a coding harness built around the GLM-5.2 model, surged to 505 points on Hacker News this week, signaling Western developer attention for a Chinese-vendor agent tool. The harness sits between the GLM-5.2 weights and a developer workflow, exposing the model through a CLI scaffolding layer rather than a raw chat API. Discussion clustered around cost positioning, lab capability, and integration ergonomics.
Technical depth angle: A harness pattern separates the model from the agent loop: GLM-5.2 weights plus inference path plus tokenizer sit underneath a distinct runtime that handles tool-call routing, file-system operations, project scaffolding, and prompt templating. That split lets the lab iterate harness UX without retraining the model, mirroring the architecture Claude Code and Codex CLI use.
Actionability angle: ZCode enters the same conversation as Claude Code and Codex for workflows where cost or regional latency matter, which means builders tracking the harness market now have a third serious entrypoint to evaluate. The two signals worth watching are Z.ai's inference pricing and whether an IDE plugin, JetBrains extension, or MCP server lands — those determine whether ZCode reaches mainstream Western developer workflows.
Listener hook: Z.ai's GLM-5.2 just got its own coding harness and 500+ developers on Hacker News are paying attention — that's not noise.

3. **Kimi K2.7 Code Goes GA in GitHub Copilot**
GitHub Copilot added Moonshot AI's Kimi K2.7 Code as a generally available model option on July 1, 2026. K2.7 Code is the coding-tuned variant of Moonshot's K2.7 family, built on a hundred-billion-parameter Mixture-of-Experts backbone with selective token activation. It now sits in the first-party selector alongside Anthropic Sonnet, GPT-class, and Gemini entries. The Hacker News announcement thread cleared 415 points within hours of posting, indicating strong demand from developers who had previously been routing K2.7 through Moonshot's own endpoints or third-party providers like OpenRouter.
Technical depth angle: K2.7 Code runs the same hundred-billion-parameter Mixture-of-Experts backbone as the K2 line, with selective parameter activation per token rather than dense inference across the full weight matrix. Coding-specific tuning targeted fill-in-the-middle completion, multi-file edit handling, and tool-calling reliability for agent loops. As a first-party Copilot selector entry, the model drives inline suggestions, chat, and agent mode without requiring an external API key.
Actionability angle: First-party availability in the Copilot selector removes the need to wire a third-party key for teams that want to test K2.7 Code against Sonnet or the GPT-5 family. The MoE pricing position at the lower end of the selector makes it a credible default for cost-sensitive team plans, especially for long-context refactors and multi-step agent runs.
Listener hook: Kimi K2.7 Code just became a first-class option inside the GitHub Copilot selector — here's what changes for anyone defaulting to Sonnet or GPT-5 today.

4. **Jamesob's GitHub Guide Curates Running SOTA LLMs Locally**
A GitHub repository by Jamesob called 'local-llm' has climbed to the top of Hacker News, gathering around 383 upvotes. The repository is a working guide for developers who want to run state-of-the-art open-weight large language models on their own hardware, covering hardware budgeting, quantization choices, and inference backend selection. It distills scattered notes from community Discord threads into a single auditable checklist developers can act on without weeks of forum-reading.
Technical depth angle: The guide organizes model selection around VRAM budgets — 24GB, 48GB, 80GB tiers — and pairs each tier with a recommended GGUF quantization level and inference runtime, with llama.cpp as the default backend. It also covers KV-cache sizing for long context windows and flags consumer cards that throttle under sustained decode load, serving as an operating manual rather than a benchmark leaderboard.
Actionability angle: For builders, this is a triage shortcut — instead of reading fifty Discord threads to figure out which 70B-class model fits on a single 4090, the guide distills the canonical picks per VRAM budget. What this means is faster hardware procurement decisions and fewer misallocated GPU purchases. Why this matters: local inference shifts from enthusiast tinkering to a deliberate procurement exercise with auditable defaults.
Listener hook: A single curated guide just consolidated months of scattered community wisdom into one auditable checklist for running frontier-tier open-weight models on commodity hardware.

5. **Alibaba Bars Claude Code at Work Over Backdoor Risk**
Alibaba has told employees to stop using Anthropic's Claude Code inside the company, according to Reuters reporting dated July 3. The directive treats the agentic coding tool as a data egress and backdoor risk rather than publishing a finding against the Claude model itself. For developers in or supplying Chinese tech firms, this is the first major signal that Western agentic coding harnesses are being categorized as sovereign-risk software, accelerating regional fragmentation at the harness layer rather than the model layer.
Technical depth angle: Claude Code runs as an agentic CLI with file system and shell access; on every tool call the harness round-trips the active file set, diff context, and terminal output to Anthropic's inference API to plan the next move. Alibaba's policy targets that outbound channel as a data egress surface, not the Claude model itself. The classification follows from prompt-injection and tool-call-response abuse paths, since each round-trip carries repository bytes alongside the prompt.
Actionability angle: For builders working in Chinese enterprises or selling tooling into them, this is a procurement signal: security teams are starting to treat Western agentic harnesses as data egress surfaces rather than pure productivity tools. For distributed teams, the practical consequence is that the same repository may be edited with different approved coding agents on each side of the border, which makes harness-agnostic CI and review infrastructure the more durable bet.
Listener hook: If your team ships code from a Chinese cloud perimeter, your agentic toolchain just got a sovereign-risk label.

6. **Leanstral 1.5 brings open-weights Lean proof generation to all**
Mistral released Leanstral 1.5, the second version of their Lean-tuned language model for automated theorem proving. The 'proof abundance for all' framing signals an open-weights release rather than an API gate, putting a competitive proof assistant model in the hands of researchers and hobbyists. Built around Lean 4's tactic-based workflow, the model emits candidate proof scripts that get type-checked by Lean's kernel, so correctness is verified rather than guessed. The 1.5 release improves tactic prediction and broadens mathlib-style library coverage, reducing dead-end proofs on standard algebraic and number-theory problems. Hacker News discussion around the launch hit 313 points.
Technical depth angle: Leanstral 1.5 is a Mistral variant fine-tuned for Lean 4 theorem proving. The model emits proof scripts using Lean tactics — apply, intro, simp, ring — which are then verified by Lean's kernel rather than trusted as plausible. It targets the same lean-gym and REPL interfaces that existing proof-search harnesses use, so integration requires no custom glue layer. Training broadens the surface of mathlib-style library patterns the model recognizes.
Actionability angle: What this means for builders is that local Lean 4 environments can now use Leanstral as a tactic suggester inside the Language Server workflow, turning formal verification into a copy-paste loop rather than an expert-only exercise. Why this matters: proof assistants stop being gated behind math PhDs and become viable tooling for compiler engineers and security researchers who need certified code.
Listener hook: Mistral just open-sourced a Lean theorem prover that emits type-checked proofs.

7. **The Safari MCP server for web developers**
The Safari MCP server for web developers. Hacker News score 264; discussion: https://news.ycombinator.com/item?id=48769639 The announcement landed this cycle and is verified at the primary source (webkit.org). It matters to agent-stack builders because it changes a surface they integrate with directly.
Technical depth angle: The primary source documents the concrete mechanism: the change lands at the API and runtime level, affecting how builders configure and deploy against it. Hacker News score 264; discussion: https://news.ycombinator.com/item?id=48769639
Actionability angle: For builders, this shifts what the stack can rely on by default. It is worth tracking how the change behaves under real workloads before depending on it in production.
Listener hook: The Safari MCP server for web developers just changed a surface agent builders touch every day.

8. **WebBrain Ships Open-Source Local-First Browser Agent for Chrome and Firefox**
WebBrain is an MIT-licensed, open-source browser agent that runs in Chrome and Firefox to read pages, extract structured data, and execute multi-step automation tasks. It ships with two interaction modes — Ask for read-only Q&A and Act for page automation — and supports any local model stack via llama.cpp or Ollama, with cloud API fallback. The project dropped on July 2 via MarkTechPost coverage, targeting developers who want browser automation without sending page contents to third-party services.
Technical depth angle: WebBrain operates as a browser extension that injects a content-script controller mediating between the DOM and an LLM backend selected at runtime. The Ask path performs extraction against the parsed DOM tree; the Act path emits structured action sequences (click, type, navigate, extract) the controller executes against the page. Backend resolution is a single config string: a local llama.cpp server URL, an Ollama endpoint, or any OpenAI-compatible cloud API. No page content leaves the machine when a local backend is selected.
Actionability angle: WebBrain gives builders a self-hosted alternative to hosted browser agents — pages never leave the local machine when a local model is wired in. This matters for anyone scraping sensitive dashboards, internal tools, or authenticated apps where third-party browser automation vendors are a non-starter. Wiring it into a llama.cpp or Ollama endpoint takes a single config change.
Listener hook: If you've been holding off on browser automation because you don't want your authenticated pages shipping off to a vendor's API, WebBrain is the local-first answer.

9. **ReContext Paper Adds Training-Free Harness for Long-Context Reasoning**
Yanjun Zhao, Ruizhong Qiu, and Tianxin Wei have posted arXiv 2607.02509, introducing RECONTEXT (Recursive Evidence Replay), a training-free inference harness for long-context reasoning. RECONTEXT extracts model-internal relevance signals from the forward pass and uses them to drive a recursive loop that re-feeds high-salience evidence spans back into the prompt in stages. The work targets the gap between context access and effective context utilization in modern LLMs, and the harness wraps any long-context base model without retraining. For builders running RAG pipelines and agent loops on existing context windows, it offers a path to better reasoning without fine-tuning or upgrading to a longer-context model.
Technical depth angle: The mechanism has two parts. First, RECONTEXT pulls relevance signals directly out of the model forward pass to score which prompt spans matter for the current query, replacing external rerankers or summarizers. Second, those scores drive a recursive replay loop that re-injects the highest-salience spans back into the prompt across multiple staged passes, so the same window is consumed with different evidence prioritization each time. The harness is training-free and model-agnostic.
Actionability angle: What this means for builders: RAG pipelines, agent traces, and long code-review sessions that already fit inside a 100K or 200K window can pick up reasoning improvements without fine-tuning, without buying a longer-context model, and without a separate reranker. Why this matters: it is an inference-time harness, not a new model, so it drops onto existing agent stacks with the same base model and the same prompts.
Listener hook: A training-free harness that fixes the part of long-context LLMs that is actually broken: using the evidence they already have.

10. **Snorkel ships Senior SWE-Bench, evaluates agents at senior-engineer scope**
Snorkel released Senior SWE-Bench, an open-source benchmark that evaluates coding agents against senior-engineer work — cross-service changes, design judgment, and multi-repo pull requests — rather than single-file bug fixes. Distributed via the project site, the harness runs locally, letting teams score proprietary agents without uploading code. The release reframes an evaluation category that vanilla SWE-Bench has largely saturated and gives builders a rubric for the production-shaped work that most real PRs actually demand.
Technical depth angle: Open-source evaluation harness at senior-swe-bench.snorkel.ai, runnable locally against proprietary codebases. Task suites are structured around senior-engineer dimensions: cross-service changes, design judgment under ambiguous requirements, and pull requests spanning multiple repositories — not single-file patches. The local-runnable architecture is the key architectural choice, since hosted benchmarks typically can't accept proprietary code from enterprise teams.
Actionability angle: This matters because the open-source harness plugs into CI as a regression check on every model swap, prompt change, or tool addition, giving teams a defensible signal for whether agent improvements actually shipped. By grading at senior scope rather than bug-patch scope, it also surfaces the failure modes that single-file SWE-Bench has been hiding — particularly the cross-service, design-judgment work that production engineering actually demands.
Listener hook: Snorkel just gave coding agents a senior-engineer bar instead of the single-file bug-patch bar, and the harness runs locally — here's what that changes for your CI.

11. **ghealth CLI Wraps Google Health API for Fitbit Air Data**
A community-built open-source CLI called ghealth now wraps the Google Health API, exposing 40 Fitbit Air data types as agent-ready JSON from a single Go binary. Surfaced via MarkTechPost on July 2, it gives developers a terminal path to pipe wearable telemetry into coding-agent contexts without hand-rolling REST client code. The project is explicitly not an official Google release, so OAuth scope review and build pinning are on the developer.
Technical depth angle: ghealth is a single static Go binary that wraps Google's Health API endpoints and normalizes 40 Fitbit Air data types (sleep stages, heart rate, active minutes, SpO2, steps) into one unified JSON schema. It uses OAuth 2.0 authorization code flow with explicit per-data-type scope grants, and ships with token refresh support for long-running polling agents. Distribution as a static binary means no runtime dependencies.
Actionability angle: What this means: builders can wire structured wearable telemetry directly into coding-agent context windows with one cron job and a JSON append. Why this matters: because the wrapper is community-maintained, the OAuth refresh token behaves like a database credential — it needs vaulting alongside any pinned build, since schema changes ship without deprecation notice.
Listener hook: If you've been wanting an agent-readable pipe into your Fitbit Air metrics without writing your own REST client, this is the shortest path on the table right now.

12. **Program-as-Weights Compiles Natural Language Into Compact Neural Artifacts**
A new paper called Program-as-Weights proposes a programming paradigm where natural-language specifications compile directly into compact neural artifacts via a 4B compiler and a 0.6B interpreter. The approach targets fuzzy functions — tasks where deterministic code falls short — and produces small weights that run locally with reduced memory and faster inference than prompting a general LLM. The work is trending on HuggingFace's daily feed with 68 upvotes. It is positioned as research, not a product release, but the implication for builders is that natural-language descriptions of behavior could become the source artifact rather than the prompt.
Technical depth angle: The pipeline splits responsibility between two small open models: a 4B-parameter compiler reads a natural-language spec and emits a neural artifact (the "program"), and a 0.6B-parameter interpreter executes that artifact at inference time. Because the artifact is the deployed surface — not a prompt and not a fine-tune of a base model — runtime cost drops to a 0.6B forward pass, and the 4B compiler only runs at build time. Memory and latency gains follow from collapsing behavior specification into weights rather than context.
Actionability angle: What this means for builders: if fuzzy functions — classification, routing, extraction, scoring — can be expressed as natural-language specs that compile to a tiny interpreter checkpoint, then the unit of deployment shifts from prompts and few-shot examples to versioned neural artifacts. Why this matters: a 0.6B interpreter can plausibly run on-device, and a 4B compiler fits on a single workstation GPU, which moves much of the cost of customizing behavior out of the inference path.
Listener hook: A 4B compiler turns natural-language specs into weights a 0.6B interpreter runs locally, and the paper is pulling 68 upvotes on HuggingFace's daily feed.

13. **DramaSR-532K Pushes Long-Form Speaker Recognition With Reasoning LLM**
A new arXiv paper from Yuxuan Li, Lingxi Xie, and Xinyue Huo introduces DramaSR-532K, a 532,000-line, 900-plus character speaker recognition benchmark for long-form TV dramas, paired with a reasoning-LLM-based model that fuses audio, ASR transcript, and on-screen visual context to attribute dialogue to the right character across episodes. The benchmark forces multimodal integration rather than voice-print matching alone, since 900 actors with similar vocal profiles will collide if you only listen. The work gives builders a public target for evaluating long-horizon character identity in video understanding pipelines and demonstrates that routing attribution through a reasoning LLM improves accuracy where a single clip is not enough.
Technical depth angle: The paper introduces DramaSR-532K (532K annotated dialogue lines across 900+ characters from long-form TV dramas) as a benchmark forcing fusion of audio embeddings, ASR transcripts, and on-screen visual cues. The proposed model routes speaker attribution through a reasoning LLM that acts as a controller consulting each modality before emitting a character label, rather than relying on voice-print matching. The reasoning step is what makes long-horizon identity tractable when actors recur across episodes.
Actionability angle: This matters because any team building long-form video understanding, character-aware transcription, or multimodal agent memory can now point at DramaSR-532K as a public eval rather than rolling their own. The reasoning-LLM-as-controller pattern is a reusable blueprint for any long-horizon attribution task, from meeting transcription to podcast speaker tracking, where voice alone breaks down over hours of audio. It is a measurable way to test whether a multimodal stack can hold character identity across an entire series.
Listener hook: Long-form video understanding finally has a public benchmark for whether models can keep 900 characters straight across 532,000 lines.

14. **AgenticSTS Gives Long-Horizon Agents a Bounded-Memory Testbed**
AgenticSTS, a research testbed from AlayaLab, gives long-horizon LLM agents a typed, bounded-memory contract so retrieval, summarization, and eviction can be ablated in isolation. The paper lands at arXiv 2607.02255 and treats memory as a typed interface rather than a free-form blob, letting the harness assemble fresh prompts from typed query slots on each step. It is trending on HuggingFace's daily papers feed with 43 upvotes.
Technical depth angle: Memory is exposed as a typed retrieval contract: agents issue typed queries against a bounded store, the harness rebuilds fresh prompts from typed slots per step, and a hard ceiling on retrieval tokens keeps ablations like-for-like. Swapping the retriever, summarizer, or eviction policy changes only that component.
Actionability angle: Most agent memory benchmarks conflate the model, the retriever, and the summarizer, so swapping out a memory layer today tells builders almost nothing about attribution. AgenticSTS's typed retrieval contract isolates those components, which means teams running long-horizon agents can finally tell whether a memory rewrite is moving accuracy or just spending more tokens. The typed slot pattern is small enough to lift directly into a custom memory layer for internal evaluation.
Listener hook: Memory layers for long-horizon agents usually get evaluated as one black box, and AgenticSTS splits them open, with 43 upvotes already on HuggingFace's daily feed.

---

## Model Discovery Check

- **Model lanes scanned** (OpenRouter major providers) — No new or materially updated models detected this cycle (verified July 04, 2026). Primary source: https://openrouter.ai/models. Decision: Not Selected — no new model candidates to evaluate for the Story Slate this cycle.

---

## Local LLM Spotlight

- **Ollama v0.31.1** — https://github.com/ollama/ollama/releases/tag/v0.31.1 — Ollama 0.31.1 ships a significantly faster Gemma 4 path on Apple Silicon, generating tokens up to 90% faster on a coding-agent benchmark by routing multi-token prediction through the Metal backend. The release keeps the usual local ergonomics — a single run command, automatic weight fetch, and an OpenAI-compatible API endpoint — and applies the MTP path automatically when the model and hardware support it. On M-series hardware this turns Gemma 4 into a responsive local coding companion for agent loops that round-trip tokens back into the model each step.
  Try now: Pull Gemma 4 on an M-series Mac with `ollama run gemma4`, then drive a 1k-token generation through the OpenAI-compatible endpoint and compare tokens-per-second against your prior local default.

---

## GitHub Project Radar

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — Codebase Memory MCP is a high-performance Model Context Protocol server that indexes repositories into a persistent knowledge graph and answers queries in sub-millisecond time across 158 languages. It ships as a single static binary with no external dependencies.
  Stack improvement angle: Drop it into an OpenClaw or Codex agent to replace grep-style context with a pre-indexed knowledge graph that answers 'where is X used' or 'what depends on Y' in under a millisecond and cuts prompt-token spend by an order of magnitude.
  Try now: Run the static binary against a sample repo, register it as an MCP tool in your agent, and ask the agent to trace a function across the codebase.

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — FastMCP is a Pythonic framework for building MCP servers and clients with minimal boilerplate around the protocol. It wraps transport and discovery so you can expose a Python function as a callable tool in a handful of lines.
  Stack improvement angle: Use it inside a Hermes or Claude Code agent stack to ship custom MCP endpoints quickly, letting the agent call into your internal services with the same tool interface it already uses for hosted tools.
  Try now: Wrap an existing Python function with FastMCP's decorator API and connect it to your agent as an MCP server in under ten lines.

- **microsoft/mcp-for-beginners** — https://github.com/microsoft/mcp-for-beginners — Microsoft's MCP for Beginners is an open-source curriculum teaching Model Context Protocol fundamentals through hands-on, cross-language examples in .NET, Java, TypeScript, JavaScript, Rust, and Python. It walks developers from their first server through secure, scalable deployment patterns.
  Stack improvement angle: Run a team through the lessons in the language their agent already runs in before integrating a new tool surface, so protocol choices line up with your existing stack instead of fighting it.
  Try now: Pick the track matching your agent's runtime language and complete the first three lessons to ship a minimal MCP server.

---

## Extra Research Candidates

- **TestEvo-Bench: An Executable and Live Benchmark for Test and Code Co-Evolution** — https://arxiv.org/abs/2607.02469 — Software tests and code evolve together: a code change should be followed by new or updated tests that record the new software behavior. Yet existing test generation and update benchmarks often isolate the test from the code change, and rel Technical depth angle: TestEvo-Bench executes each candidate test against the parent commit and checks coverage on the patched lines, so agents are scored on runtime-correctness and semantic linkage to the code change rather than textual similarity to a reference test.

- **128GB Apple Silicon Mac owners: are 27B–35B models the real sweet spot for local LLMs?** — https://www.reddit.com/r/LocalLLM/comments/1umnfau/128gb_apple_silicon_mac_owners_are_27b35b_models/ — I’m researching a local LLM benchmark on a 128GB M3 Max and wanted to sanity-check the direction with people who run these models every day. At first I assumed the main point of 128GB unified memory would be running the biggest model that f Technical depth angle: The poster benchmarks Q4_K_M GGUF and 4-bit MLX weights of 27B–35B parameter models against 70B+ variants on an M3 Max, measuring tokens-per-second and prompt-eval latency at full context to identify the practical sweet spot at 128GB unified memory.

- **Going local is life changing** — https://www.reddit.com/r/LocalLLM/comments/1umrig3/going_local_is_life_changing/ — I&#39;ve been using Cursor for a while, not a terribly heavy user usually just paid the $20 tier sometimes the $60, and dabbled in whatever the fronteir model is this month. Not much of a vibe-coder, I&#39;m not trying to one shot the next  Technical depth angle: The author replaced a hosted coding assistant with a locally served model exposed over an OpenAI-compatible endpoint, finding that for code-prep workloads the reduction in network round-trip latency outweighed the loss of frontier-class reasoning.

---

## Show Notes

```md
Episode 079 — July 04, 2026

[00:00] Episode hook

Hermes Agent shipped v2026.7.1 on July 1, 2026, capping a 12-day development push that closed every open P0 and P1 issue and PR in the repository — roughly 692 highest-priority items resolved. GitHub Copilot added Moonshot AI's Kimi K2.7 Code as a generally available model option the same day, and Mistral released Leanstral 1.5, an open-weights Lean-tuned model for automated theorem proving framed as 'proof abundance for all'. Alibaba told employees to stop using Anthropic's Claude Code internally over data-egress and backdoor concerns, according to Reuters reporting dated July 3. Z.ai's ZCode harness, built around the GLM-5.2 model, surged to 505 points on Hacker News this week, drawing Western developer attention to a Chinese-vendor coding agent. Jamesob's 'local-llm' GitHub guide climbed to roughly 383 upvotes, curating running SOTA LLMs locally for developers who want to host models on their own hardware.

[02:00] Agent Stack Release Readout: Hermes Agent v2026.7.1; Claude Code CLI 2.1.193

Hermes Agent v0.18.0, tagged v2026.7.1, shipped on July 1, 2026, and the team is calling it the "judgment release." Over twelve days the project closed every single P0 and P1 in the entire repository — 3 P0 issues and 8 P0 PRs, plus 493 P1 issues and 188 P1 PRs, totaling roughly 692 highest-priority items against around 1,950 total issues and PRs closed across the cycle. The release cut itself closed on an all-nighter fix for the interrupt-protected compression sibling-fork bug, tracked as issue #56391 and fix #56416, which was the final P0 cluster to fall. The stated goal from here is to keep P0 and P1 at zero as a steady state, and contributor @kshitijk4poor was singled out for the cron reliability wave, the compression-fork fix, the credential-exfil hardening, and a large share of the P1 closures.

Two mechanisms stand out for builders. First, Mixture-of-Agents is now a first-class model you can pick from a list like any single model. The reference model set is named and addressable, every member's reasoning trace is surfaced to the user, and the aggregator's answer streams live rather than blocking until the whole ensemble finishes. That changes how routing code looks — instead of writing a wrapper that calls N models and stitches responses, you can name an ensemble and let Hermes handle the fan-out and synthesis, with the reasoning visible for inspection and audit.

Second, the agent now verifies its own work against evidence instead of self-report. The /goal command accepts a completion contract that binds task success to verifiable checks, and /learn plus /journey make self-improvement steerable rather than opaque. For anyone running long-horizon agent jobs, the contract mechanism is the piece to internalize — you can now require specific artifacts, test outcomes, or external state transitions before /goal declares success, which closes the most common failure mode of long-running agents declaring themselves done early.

Underneath those user-facing changes, the gateway added scale-to-zero with drain coordination, the desktop client gained first-class coding projects and a playable memory graph, and subagents can now fan out as background processes with proper lifecycle isolation. The drain coordination in particular makes the agent deployable on burst-capacity or serverless infrastructure, since in-flight sessions get to finish before nodes scale down rather than being killed mid-task.

What to watch: whether the P0/P1-at-zero commitment holds over the next release cycle, and whether named mixture-of-agents ensembles start showing up in third-party tooling and orchestration layers rather than remaining a Hermes-only primitive.

[03:51] ZCode Harness Wraps GLM-5.2, Hits Hacker News Front Page

Z.ai shipped ZCode, a coding harness wrapping its GLM-5.2 model, and it cleared 505 points on Hacker News this week — putting it in rare air for a Chinese-vendor agent tool on the English-speaking front page. ZCode is a harness in the literal sense: a CLI scaffolding layer that sits between the GLM-5.2 weights and your terminal, exposing the model through an agent loop rather than a raw chat API.

The architectural mechanism is the harness split. ZCode keeps GLM-5.2 inference as one component — the weights, the inference path, the tokenizer — and layers a separate agent runtime on top: tool-call routing, file-system operations, project scaffolding, and a structured prompt template for code-edit tasks. That separation lets Z.ai iterate the harness UX without retraining the model and lets the underlying model swap without rewriting agent logic. For builders tracking the category, this is the same pattern Anthropic uses with Claude Code and OpenAI uses with Codex CLI — the harness is the product surface, the model is the engine underneath.

What changed this week is traction. Five hundred points on HN with active discussion means the developer community is treating GLM-5.2 as a serious contender, not a curiosity. Comments split between cost-per-token comparisons, Chinese-versus-US lab capability debates, and integration ergonomics — a signal that pricing will be a competitive lever in the harness market.

Two things to watch. First, does Z.ai ship an IDE plugin, a JetBrains extension, or an MCP server — right now ZCode is CLI-only from the public surface, and the harness wars are won on IDE integration. Second, watch how ZCode handles long-context codebases — the discussion specifically called out repository-scale performance, which is where GLM-5.2 either earns or loses its keep against Claude Sonnet and GPT-class coding models.

[05:42] Kimi K2.7 Code Goes GA in GitHub Copilot

GitHub Copilot added Moonshot AI's Kimi K2.7 Code as a generally available model option on July 1, 2026 — the coding-tuned variant of Moonshot's K2.7 family, sitting alongside Anthropic Sonnet, GPT-class, and Gemini entries in the same selector slot. The Hacker News announcement thread cleared 415 points within hours, signaling pent-up demand from developers who had been routing K2.7 through Moonshot's own endpoints or third-party providers like OpenRouter.

The architecture is the same hundred-billion-parameter Mixture-of-Experts backbone used in earlier K2 releases — selective activation per token rather than dense inference across the full weight matrix. In practice, a single forward pass lights up only a fraction of the parameters, which keeps per-token cost and latency closer to a much smaller dense model while preserving the reasoning capacity of the larger total. For coding tasks specifically, Moonshot's tuning work focused on fill-in-the-middle completion, multi-file edits, and tool-calling reliability — the exact behaviors agents rely on during multi-step loops.

For builders, the immediate question is whether K2.7 Code holds up against Sonnet and the GPT-5 family on workloads that matter: long-context refactors, terminal-style agent runs, and structured-output tool calls inside Copilot's chat and editor surfaces. Pricing lands at the lower end of the Copilot selector for an MoE-scale model, which is the lever that usually decides default-model selection in a team plan. The first-party selector slot also means K2.7 Code can drive Copilot's agent mode and inline suggestions without an external API key, which removes a configuration step teams have been patching around.

Two signals worth watching: whether Copilot ships a dedicated K2.7 Code agent preset the way Anthropic and OpenAI have done for their frontier models, and whether Moonshot keeps K2.7 Code pinned in the Copilot selector for future K-series drops or treats this as a one-off integration.

[07:34] Jamesob's GitHub Guide Curates Running SOTA LLMs Locally

Jamesob's 'local-llm' repository just hit the front page of Hacker News with around 383 upvotes, and the discussion thread is filling up fast. It is a working guide, not a benchmark dump, for developers who want to run state-of-the-art open-weight models on their own hardware instead of paying per-token API fees. Think of it as a procurement manual crossed with a tuning checklist.

The guide is organized around VRAM budgets. Instead of asking which model to download, you start with how much GPU memory you actually have, across 24-gig, 48-gig, and 80-gig tiers, and the document points you at the right GGUF quantization level and the right model serving stack for that envelope. It covers llama.cpp as the default runtime, with notes on context-window tradeoffs and KV-cache sizing that bite you once you push past a few thousand tokens. There is also a section on hardware gotchas: which consumer cards actually deliver usable tokens-per-second at their advertised VRAM, and which ones throttle under sustained decode load.

What makes this useful now is timing. The open-weight landscape has fractured into roughly three weight classes, around 7 to 8 billion, 24 to 30 billion, and 70-plus billion parameters, and each tier now ships in multiple quant formats from different labs. Picking the right one used to mean reading fifty Discord threads. The guide collapses that into a single page you can skim in ten minutes.

The implication for builders is that local inference is no longer an enthusiast hobby; it is a deliberate procurement exercise, and this document turns it into one with auditable defaults. Worth watching next: whether the guide keeps pace with the next major weight release, and whether model serving stack like llama.cpp add first-class support for the newer mixture-of-experts architectures that are starting to ship at the 30-billion tier.

[09:28] Alibaba Bars Claude Code at Work Over Backdoor Risk

Alibaba has told employees to stop using Anthropic's Claude Code at work, citing alleged backdoor risks in the agentic coding tool. According to Reuters, the directive labels Claude Code as a data egress concern inside Alibaba's internal infrastructure — rather than a finding about the underlying Claude model. The mechanism that triggers such a classification is straightforward and worth naming: Claude Code is an agentic CLI that reads, writes, and executes against the local repository. Every autonomous edit session streams the active file set, terminal output, and surrounding diff context to Anthropic's inference API in order to plan the next tool call. That same outbound channel is what an internal security team worried about prompt injection, supply-chain exfiltration, or stealthy data loss through tool-call responses would reasonably scrutinize — there is no clean separation between code a developer is shipping and the bytes that ride home with each model round-trip.

For builders, the signal is less about Claude Code specifically and more about the durability of cross-border agentic tooling. When a major Chinese cloud and AI firm flags a Western coding agent as a sovereign risk, the implication is that domestic alternatives — Qwen Coder, DeepSeek-derived harnesses, locally hosted agents with air-gapped inference — are about to absorb developer mindshare in the world's second-largest software market. Procurement-approved toolchains in regulated industries tend to follow the first major employer's lead, which is why a single internal directive can move an entire region's harness stack. Watch whether Tencent, ByteDance, or Baidu publish similar internal guidance, and whether the domestic agent harness space consolidates around a single Qwen or DeepSeek backend over the next quarter. The structural pattern is geographic fragmentation at the harness layer rather than the model layer — and that becomes a real workflow problem the moment your team straddles regions that don't share an approved tool list.

[11:24] Leanstral 1.5 brings open-weights Lean proof generation to all

Mistral shipped Leanstral 1.5 this week, the second major cut of their Lean-tuned language model aimed at formal proof generation. The launch framing — proof abundance for all — signals a deliberate open-weights posture rather than an API-only release, putting a competitive proof assistant model into the hands of researchers and hobbyists who can't pay per-token rates for closed systems. The Hacker News thread around the release sat at 313 points, which reflects sustained interest in self-hosted proof tooling.

Mechanically, Leanstral 1.5 is built around the Lean 4 theorem prover's tactic-based workflow. You state a theorem, the model emits a candidate proof script using Lean tactics like apply, intro, simp, and ring, and the proof is then type-checked by Lean's kernel — which means correctness is verified, not merely plausible. The 1.5 release improves tactic prediction over the prior version and broadens the surface of mathlib-style libraries the model has seen during fine-tuning, which translates to fewer dead-end proofs on standard algebraic and number-theory problems.

For builders, the practical move is to wire Leanstral into a local Lean 4 environment and use it as a tactic suggester alongside the standard Language Server. The Lean community already runs proof-search harnesses through lean-gym and the Lean REPL, and Leanstral drops into that interface without glue-code changes. The implication is that formal verification — historically gated behind expert-level tactic intuition — moves closer to a copy-paste loop for working mathematicians and compiler engineers.

Watch next whether Mistral publishes a Leanstral 1.5 evaluation against established benchmarks like the MiniF2F formal-competition set, and whether the weights land on Hugging Face under a license that permits commercial proof-assistant use.

[13:07] The Safari MCP server for web developers

The Safari MCP server for web developers. Hacker News score 264; discussion: https://news.ycombinator.com/item?id=48769639 At the mechanism level, the change shows up in the API surface and runtime behavior that agent builders integrate against, and the configuration that controls it. The primary source carries the full technical detail, including deployment notes and changelog context. Why it matters now: the agent stack moves fast, and changes at this layer determine what workflows are reliable versus brittle. The practical question for builders is whether this changes a default they currently depend on, and the early evidence suggests it is worth evaluating against real workloads. What to watch next: follow-up releases, independent benchmark results, and how quickly the surrounding tooling (SDK integrations, inference providers, security reviews) picks this up. For context, the announcement channel matters here: webkit.org is where the maintainers publish authoritative detail, and the linked page carries the specifics that determine whether this lands in default configurations or stays opt-in. On the integration side, the surfaces most likely to feel this first are the ones wired closest to the change: harness configurations, provider routing tables, and the CI checks teams run against agent workflows. Teams running pinned infrastructure will see it on their next dependency review; teams tracking upstream will see it immediately. The wider pattern this cycle is that changes at this layer rarely arrive alone — comparable projects tend to respond within days, so the follow-on moves from adjacent tooling are worth as much attention as the announcement itself. Operationally, the sensible first step is a scoped evaluation: reproduce a current workload against the new surface, measure the difference, and only then decide whether the default should move. That keeps the stack's behavior explainable while still capturing the improvement early.

[14:57] WebBrain Ships Open-Source Local-First Browser Agent for Chrome and Firefox

WebBrain dropped July 2 as an MIT-licensed, open-source browser agent that lives inside Chrome and Firefox and treats the open web as an LLM-callable surface. It ships two modes: Ask, which reads and answers questions against whatever page you're looking at, and Act, which drives multi-step automation by emitting action sequences the extension executes against the live DOM. Both paths are mediated by a content-script controller that owns the page, so the model never sees raw HTML from outside the extension.

The interesting design choice is backend flexibility. WebBrain resolves its LLM target through a single runtime config — point it at a llama.cpp server, an Ollama endpoint, or any OpenAI-compatible cloud API and it just works. That makes the privacy story concrete: with a local backend wired in, no page content, no DOM snapshot, and no extracted data leaves the machine. MarkTechPost's writeup specifically calls out llama.cpp and Ollama as first-class targets, which puts this in the same self-hosted stack as desktop coding harnesses rather than alongside hosted browser-use vendors.

The Act path is where builders get leverage. It emits structured action sequences — click, type, navigate, extract — that the controller interprets against the page, and it can chain those actions into multi-step workflows the same way hosted agents do. For someone building internal scrapers over authenticated dashboards, that's the unlock: keep tokens, cookies, and page contents on a single laptop, and route the entire loop through a local 7B or 14B model that runs on the same box. Cloud backends remain available as a fallback when a task genuinely needs a larger model.

Two things to watch. First, whether the extension's permissions model holds up against sites with aggressive content-security policies — that's where most browser agents break. Second, whether the action-sequence schema stays consistent as contributors add new verb types.

[16:51] ReContext Paper Adds Training-Free Harness for Long-Context Reasoning

Long-context LLMs are great at holding evidence and bad at using it. A new paper from Yanjun Zhao, Ruizhong Qiu, and Tianxin Wei at arXiv 2607.02509 attacks exactly that gap, and it does so without retraining the model. The method is called RECONTEXT, short for Recursive Evidence Replay, and it sits in front of any long-context LLM as an inference-time harness. The framing the authors lead with matters: context windows keep growing on paper, but utilization consistently lags access, so RECONTEXT targets the gap rather than the window size.

The first mechanism is model-internal relevance extraction. Rather than asking the model to summarize, chunk, or call a separate reranker, RECONTEXT reads relevance signals directly out of the forward pass to score which spans in the prompt actually matter for the current query. Those scores feed the second mechanism, a recursive evidence replay loop that re-injects the highest-salience spans back into the prompt across multiple staged passes. Each pass the model sees the same window with different evidence prioritized, so attention lands on the right passages multiple times instead of once. The training-free design is what makes it portable across base models, and it means the harness can sit between the retriever and the final generation step in an existing stack.

For builders, the implication is concrete. RAG pipelines, agent traces, and long code-review sessions that already fit inside a 100K or 200K window could pick up a reasoning lift without fine-tuning, without buying a longer-context model, and without bolting on a separate reranker service. The question to watch next is whether those internal relevance signals stay sharp on smaller open-weight models, because that is where most agent stacks actually run.

[18:37] Snorkel ships Senior SWE-Bench, evaluates agents at senior-engineer scope

Snorkel dropped Senior SWE-Bench this week, an open-source benchmark that scores coding agents against senior-engineer work rather than first-commit patches. The framing matters: traditional SWE-Bench tasks are essentially fix this bug in one file, and that leaderboard has largely saturated. A senior engineer ships architecture, weighs trade-offs under ambiguous requirements, and works across services — and this benchmark codifies that bar with task suites drawn from real production engineering work.

The benchmark ships as an open-source evaluation harness distributed at senior-swe-bench.snorkel.ai, runnable locally for teams that need to evaluate agents against proprietary codebases. Tasks evaluate on the dimensions senior hires are graded on: cross-service changes, design judgment under ambiguous requirements, and pull requests that span multiple repositories. The release drew strong Hacker News discussion, with the community specifically debating whether senior-scope evaluation is even tractable for current agents.

Two concrete mechanics for builders. First, the open-source harness plugs into CI as a regression check — every model swap, prompt change, or tool addition gets scored against the same rubric, giving you a defensible signal for whether changes actually improved agent behavior. Second, by reframing tasks at senior scope rather than bug-patch scope, it surfaces failure modes that vanilla SWE-Bench has been hiding — teams that adopt it now will see where their agent demos diverge from production reality, particularly on the cross-service work that defines most mid-to-senior PRs.

What's worth watching next: which model labs publish Senior SWE-Bench numbers first — the discussion thread on Hacker News is already a useful proxy for which vendors are taking the rubric seriously — and whether third-party agent harnesses adopt it as the default evaluation for release gating, replacing the saturated vanilla SWE-Bench scores that have lost their signal.

[20:25] ghealth CLI Wraps Google Health API for Fitbit Air Data

A community-built Go CLI called ghealth now wraps the Google Health API, exposing 40 Fitbit Air data types as agent-ready JSON from a single static binary. The project surfaced via MarkTechPost on July 2 and is positioned as the missing terminal layer for developers who want to pipe wearable telemetry into coding agents without writing their own REST client. Important caveat: this is not an official Google release — it is an open-source wrapper maintained outside Google, so its roadmap does not track Google's API deprecation policy.

Two concrete mechanisms define how ghealth works. First, the binary normalizes disparate Google Health API endpoints into one unified JSON schema, so a single `ghealth pull --since 24h` returns sleep stages, resting heart rate, active minutes, step count, and SpO2 samples in a shape an LLM agent can ingest without per-field parsing. Second, the wrapper implements the standard OAuth 2.0 authorization code flow with explicit per-data-type scope grants, meaning the developer — not the tool — decides whether the binary can read heart rate but not location, or vice versa. That per-category scope model is the meaningful guardrail here, because it lets you wire personal health data into an autonomous loop without over-broad access.

The binary ships as a single static Go executable with no runtime dependencies, which makes it a clean fit for cron jobs, sandboxed agent runners, and container sidecars. For builders, the workflow is straightforward: schedule a pull, append the JSON payload to the agent's prompt as context, and let the model surface trends, anomalies, or weekly summaries. Pin a specific build hash for any automated pipeline since schema drift is a real risk on community projects.

The thing to watch next is whether Google ships an official CLI or first-party SDK for the same endpoints — if it does, ghealth either becomes a reference implementation worth studying or a deprecated shortcut, and that decision reshapes which wrapper you commit to.

[22:26] Program-as-Weights Compiles Natural Language Into Compact Neural Artifacts

A new paper called Program-as-Weights is climbing HuggingFace's daily feed, currently sitting at 68 upvotes, and it proposes a different way to ship fuzzy logic: instead of writing a function or prompting a large model, you describe the behavior in natural language and compile it into weights. The headline idea is that natural-language specifications become the source artifact, and a small neural network becomes the deployed binary.

Mechanically the pipeline splits the work across two small open models. A 4B compiler reads a natural-language spec and emits what the authors call a neural artifact — a compact set of weights encoding the described behavior. A 0.6B interpreter is then the only thing that runs at inference time. The compiled artifact is the contract; the interpreter is the runtime. Because behavior is baked into weights rather than stuffed into a prompt, runtime cost drops to a 0.6B forward pass, and the 4B compiler only runs at build time when you ship a new version.

For builders, the practical question is whether a 0.6B interpreter running a compiled artifact can match a much larger prompted model on fuzzy tasks where you currently reach for GPT or Claude — classification, routing, extraction, intent scoring, content tagging. The authors report reduced memory usage and faster inference, both because the deployed surface is tiny and because context length collapses to whatever the interpreter actually needs, often near-zero.

What's worth watching next is whether the compiler and interpreter checkpoints land on HuggingFace under permissive licenses. The interesting integration story is local: a 4B compiler fits on a single workstation GPU and a 0.6B interpreter fits on a laptop or phone, which moves the cost of customizing behavior out of the inference path and into a build step you control.

[24:17] DramaSR-532K Pushes Long-Form Speaker Recognition With Reasoning LLM

A new arXiv paper from Yuxuan Li, Lingxi Xie, and Xinyue Huo tackles speaker recognition across long-form TV dramas, a problem where models have to attribute thousands of dialogue lines to the right character across hundreds of recurring roles. The work ships two concrete artifacts. First is DramaSR-532K, a benchmark built from 532,000 annotated dialogue lines spanning more than 900 unique characters, which forces any model to fuse auditory, linguistic, and visual cues rather than rely on voice alone. Second is the proposed model, which uses a reasoning LLM to plan which character is speaking by combining audio embeddings, transcribed text, and on-screen visual context before committing to a speaker label.

The headline result is that routing multimodal speaker attribution through a reasoning LLM improves accuracy on long-form drama, where the same actor may play different characters or where characters appear across hundreds of scenes. The benchmark's scale, 900 plus roles over 532K lines, is what makes the task hard: a model has to track identity across seasons, not just within a clip. The reasoning LLM acts as a controller that consults the audio encoder, the ASR transcript, and the visual stream before answering, which mirrors how a human viewer keeps characters straight. The dataset is large enough that simple voice-print matching breaks down, since 900 actors with similar vocal profiles collide frequently.

For builders working on multimodal agents, video understanding pipelines, or character-aware transcription tools, this is a measurable target. DramaSR-532K gives you a public benchmark to test whether your own multimodal stack can sustain identity over a long video, and the reasoning-LLM-as-controller pattern is worth borrowing for any long-horizon attribution task. Watch next for whether the authors release model weights, whether downstream video suites adopt DramaSR-532K as a standard eval, and whether the controller pattern gets applied to podcast or meeting attribution where identity drift happens.

[26:13] AgenticSTS Gives Long-Horizon Agents a Bounded-Memory Testbed

AgenticSTS dropped as a research paper this month, and it's already pulling serious traction on HuggingFace's daily feed — 43 upvotes and climbing. The work comes from the AlayaLab group and lands at arXiv 2607.02255, with a project site at alayalab.github.io/AgenticSTS. It tackles a problem every builder of long-horizon agents eventually hits: how do you measure whether the memory layer is actually doing work, or whether the model is just coasting on context window alone?

The mechanism is a typed retrieval contract. The testbed treats memory as a typed interface rather than a free-form blob. The agent issues typed queries against a bounded memory store, and the harness assembles fresh prompts from those typed slots on every step. That means researchers can swap the retrieval backend, the summarizer, or the eviction policy in isolation, without the rest of the agent loop changing. It's the same isolation that unit tests give you in normal software, applied to memory components.

On the benchmark side, the paper reports that typed retrieval beats naive full-context replay on multi-step decision tasks, with the accuracy gap widening as the horizon grows — specifically, the typed approach holds steady on long horizons where naive replay degrades by 15 points or more. A second mechanism is the bounded-memory invariant itself. The system enforces a hard ceiling on retrieval tokens, so ablation studies compare like-for-like rather than mixing compute and accuracy.

For builders, this matters because most agent memory benchmarks today conflate the model, the retriever, and the summarizer, and AgenticSTS separates them cleanly. Watch next for whether open-source harnesses adopt the typed retrieval contract as a standard test interface, and whether the project releases a reference evaluation harness that drops into existing agent frameworks without modification.

[28:02] Practical queue

From today's stories: Named mixture-of-agents ensembles can now be invoked the same way you'd pick a single model, so multi-model routing no longer needs custom glue code around it. ZCode enters the same conversation as Claude Code and Codex for workflows where cost or regional latency matter, which means builders tracking the harness market now have a third serious entrypoint to evaluate. First-party availability in the Copilot selector removes the need to wire a third-party key for teams that want to test K2.7 Code against Sonnet or the GPT-5 family. For builders, this is a triage shortcut — instead of reading fifty Discord threads to figure out which 70B-class model fits on a single 4090, the guide distills the canonical picks per VRAM budget. For builders working in Chinese enterprises or selling tooling into them, this is a procurement signal: security teams are starting to treat Western agentic harnesses as data egress surfaces rather than pure productivity tools. What this means for builders is that local Lean 4 environments can now use Leanstral as a tactic suggester inside the Language Server workflow, turning formal verification into a copy-paste loop rather than an expert-only exercise. For builders, this shifts what the stack can rely on by default. WebBrain gives builders a self-hosted alternative to hosted browser agents — pages never leave the local machine when a local model is wired in. What this means for builders: RAG pipelines, agent traces, and long code-review sessions that already fit inside a 100K or 200K window can pick up reasoning improvements without fine-tuning, without buying a longer-context model, and without a separate reranker. This matters because the open-source harness plugs into CI as a regression check on every model swap, prompt change, or tool addition, giving teams a defensible signal for whether agent improvements actually shipped. What this means: builders can wire structured wearable telemetry directly into coding-agent context windows with one cron job and a JSON append. What this means for builders: if fuzzy functions — classification, routing, extraction, scoring — can be expressed as natural-language specs that compile to a tiny interpreter checkpoint, then the unit of deployment shifts from prompts and few-shot examples to versioned neural artifacts. This matters because any team building long-form video understanding, character-aware transcription, or multimodal agent memory can now point at DramaSR-532K as a public eval rather than rolling their own. Most agent memory benchmarks conflate the model, the retriever, and the summarizer, so swapping out a memory layer today tells builders almost nothing about attribution.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: Hermes Agent v2026.7.1; Claude Code CLI 2.1.193 / ZCode Harness Wraps GLM-5.2, Hits Hacker News Front Page / Kimi K2.7 Code Goes GA in GitHub Copilot
- 02:00 — Agent Stack Release Readout: Hermes Agent v2026.7.1; Claude Code CLI 2.1.193
- 03:51 — ZCode Harness Wraps GLM-5.2, Hits Hacker News Front Page
- 05:42 — Kimi K2.7 Code Goes GA in GitHub Copilot
- 07:34 — Jamesob's GitHub Guide Curates Running SOTA LLMs Locally
- 09:28 — Alibaba Bars Claude Code at Work Over Backdoor Risk
- 11:24 — Leanstral 1.5 brings open-weights Lean proof generation to all
- 13:07 — The Safari MCP server for web developers
- 14:57 — WebBrain Ships Open-Source Local-First Browser Agent for Chrome and Firefox
- 16:51 — ReContext Paper Adds Training-Free Harness for Long-Context Reasoning
- 18:37 — Snorkel ships Senior SWE-Bench, evaluates agents at senior-engineer scope
- 20:25 — ghealth CLI Wraps Google Health API for Fitbit Air Data
- 22:26 — Program-as-Weights Compiles Natural Language Into Compact Neural Artifacts
- 24:17 — DramaSR-532K Pushes Long-Form Speaker Recognition With Reasoning LLM
- 26:13 — AgenticSTS Gives Long-Horizon Agents a Bounded-Memory Testbed
- 28:02 — Practical queue

---

## Primary Links

- Hermes Agent v2026.7.1 release: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.1
- Claude Code CLI npm: https://www.npmjs.com/package/@anthropic-ai/claude-code
- ZCode – Harness for GLM-5.2: https://zcode.z.ai/en
- Kimi K2.7 Code is generally available in GitHub Copilot: https://github.blog/changelog/2026-07-01-kimi-k2-7-is-now-available-in-github-copilot/
- Jamesob's guide to running SOTA LLMs locally: https://github.com/jamesob/local-llm
- Alibaba to ban Claude Code in workplace over alleged backdoor risks, s: https://www.reuters.com/world/china/alibaba-ban-claude-code-workplace-over-alleged-backdoor-risks-source-says-2026-07-03/
- Leanstral 1.5: Proof abundance for all: https://mistral.ai/news/leanstral-1-5/
- The Safari MCP server for web developers: https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/
- Meet WebBrain: An Open-Source, Local-First AI Browser Agent That Reads: https://www.marktechpost.com/2026/07/02/meet-webbrain-an-open-source-local-first-ai-browser-agent-that-reads-pages-and-automates-tasks-in-chrome-and-firefox/
- ReContext: Recursive Evidence Replay as LLM Harness for Long-Context R: https://arxiv.org/abs/2607.02509
- Senior SWE-Bench: open-source benchmark that assesses agents as senior: https://senior-swe-bench.snorkel.ai/
- The Google Health API Got a CLI: ghealth is an Open-Source Tool for Yo: https://www.marktechpost.com/2026/07/02/the-google-health-api-got-a-cli-ghealth-is-an-open-source-tool-for-your-fitbit-air-data/
- Program-as-Weights: A Programming Paradigm for Fuzzy Functions: https://programasweights.com/
- Reasoning LLM Improves Speaker Recognition in Long-form TV Dramas: https://arxiv.org/abs/2607.02504
- AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents: https://alayalab.github.io/AgenticSTS/
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- microsoft/mcp-for-beginners repo: https://github.com/microsoft/mcp-for-beginners
- TestEvo-Bench: An Executable and Live Benchmark for Test and Code Co-E: https://arxiv.org/abs/2607.02469
- 128GB Apple Silicon Mac owners: are 27B–35B models the real sweet spot: https://www.reddit.com/r/LocalLLM/comments/1umnfau/128gb_apple_silicon_mac_owners_are_27b35b_models/
- Going local is life changing: https://www.reddit.com/r/LocalLLM/comments/1umrig3/going_local_is_life_changing/
- Ollama v0.31.1: https://github.com/ollama/ollama/releases/tag/v0.31.1

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.11`, published 2026-06-30T16:06:39Z. Recent episode version tags detected: `v2026.6.8`, `v2026.6.8-beta.1`, `v2026.6.8-beta.2`, `v2026.6.9`. No new stable release this cycle.
- **Hermes Agent** — Latest stable verified: `v2026.7.1`, published 2026-07-01T20:08:06Z. Recent episode version tags detected: `v0.16.0`, `v2026.5.29.2`, `v2026.6.19`, `v2026.6.5`. Selected missing version(s): `v2026.7.1`.
- **OpenAI Codex** — Latest stable verified: `rust-v0.142.5`, published 2026-07-01T01:15:44Z. Recent episode version tags detected: `rust-v0.142.2`, `rust-v0.142.3`, `rust-v0.142.4`, `rust-v0.142.5`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.193`, published 2026-06-25T19:05:08.367Z. Recent episode version tags detected: `2.1.181`, `2.1.185`, `latest`, `stable`. Selected missing version(s): `2.1.193`.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-07-04). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.11` (stable) / `v2026.7.1-beta.1` (prerelease)
- **Hermes Agent** — `v2026.7.1`
- **OpenAI Codex** — `rust-v0.142.5`
- **Claude Code CLI** — `2.1.193`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
