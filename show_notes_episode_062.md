# AgentStack Daily EP062 - Codex 0.136, Stanford's Agent Guidelines, AWS OpenAI, and GPU Efficiency

## Release Coverage Check

- **OpenClaw** - Latest stable verified: `v2026.5.28`, published 2026-05-30T20:06:10Z from GitHub releases. Recent episode version tags detected: `v2026.5.28`, `v2026.5.27`, `v2026.5.26`. Selected missing versions: none. The beta line (v2026.6.1-beta.1, v2026.5.31-beta.4) is watch material, not stable coverage.
- **Hermes Agent** - Latest stable verified: `v2026.5.29.2` / `v0.15.2`, published 2026-05-29T13:37:26Z from GitHub releases. Recent episode version tags detected: `v2026.5.29.2`. Selected missing versions: none.
- **OpenAI Codex app/CLI** - Latest stable verified: `rust-v0.136.0`, published 2026-06-01T17:31:00Z from GitHub releases. Recent episode version tags detected: `rust-v0.135.0`. Selected missing version: `rust-v0.136.0`. Candidate verification: stable release list begins `rust-v0.136.0` (2026-06-01), `rust-v0.135.0` (2026-05-28); the first matching stable tag in recent notes is `rust-v0.135.0`, so `rust-v0.136.0` is the selected block.
- **Claude Code CLI** - Latest npm `latest` verified: `2.1.160`, published 2026-06-01T17:50:06Z in npm metadata. npm `stable` dist-tag verified as `2.1.150`. Recent episode version tags detected: `2.1.159`. Selected missing version from npm `latest`: `2.1.160`. Note: this episode covers the CLI release only; the standalone Claude Code app for ChatGPT Enterprise/Edu received May 29 updates and is covered as product news within the Codex story.

## Runtime Target

42-50 min. Codex CLI `rust-v0.136.0` as the front release, then three externally-sourced stories — Stanford's AI agent guidelines, OpenAI on AWS, and a YC launch in GPU efficiency — followed by a project radar and a closing on context management for coding agents.

## Episode Title

Codex 0.136, Stanford's Agent Guidelines, AWS OpenAI, and GPU Efficiency

## Tagline

Codex ships a runtime and diagnostics release, Stanford publishes formal AI agent guidelines for academic and builder use, OpenAI puts frontier models and Codex on AWS Bedrock, a YC-backed GPU efficiency project outperforms frontier models by 8x on resource prediction, and the project radar turns agent guidelines, hardware OS, and GPU scheduling into practical workflow additions.

## Feed Description

AgentStack Daily EP062 leads with Codex `rust-v0.136.0`: better TUI diagnostics and error context, improved app-server lifecycle handling, named hooks and permission scopes, Python SDK and Node SDK improvements, and non-interactive installation support. Stanford's CS336 course publishes a formal AI agent guidelines document that reaches 1,863 stars in under 24 hours — institutional validation that agent workflow guidelines are becoming a first-class engineering concern. OpenAI puts GPT-4.5, o3, and Codex on AWS Bedrock, completing the pattern where both major labs distribute through the same cloud. Expanse from YC P26 uses cluster-specific fine-tuned models to predict GPU job resource needs and outperforms frontier LLMs by 8x on that task, backed by real HPC telemetry and SLURM/Kubernetes integration. The project radar covers agent OS for hardware, terminal context managers, MCP workflow templates, and physical agent scheduling.

## Story Slate

### 1. **Codex rust-v0.136.0 improves diagnostics, lifecycle handling, and permission scoping**
Codex `rust-v0.136.0` lands as the stable CLI release for June 1. The headline improvements are TUI diagnostics and error context: `codex doctor` output is more readable, error messages carry better location and cause information, and the TUI rendering is more stable on macOS and Linux. App-server lifecycle handling is tighter: the server starts and stops more cleanly, model selection at startup is more reliable, and remote transport connections recover faster after a network hiccup. Hook configuration gets named hooks and permission scopes, so operators can define a hook once and reference it across multiple configurations instead of pasting the same block into every project. The Python SDK and Node SDK both receive improvements around thread management, turn handling, and error propagation. Non-interactive installation now works more reliably with `CODEX_NON_INTERACTIVE=1`.
Technical depth angle: explain TUI diagnostics as operator evidence, app-server lifecycle boundaries, named hook scoping, SDK thread/turn abstractions, and non-interactive install environment variable behavior.
Actionability angle: run `codex doctor` after upgrading and compare the output to the prior version; define one named hook and scope it across two projects; test non-interactive install in a CI pipeline before promising it as a deployment primitive.
Listener hook: Codex is building a more inspectable and scriptable local agent runtime, and this release moves the needle on exactly the surfaces that annoy operators when they break.
Primary links: https://github.com/openai/codex/releases/tag/rust-v0.136.0, https://github.com/openai/codex/releases/tag/rust-v0.135.0

### 2. **Stanford CS336 publishes formal AI agent guidelines that the community turns into a viral reference**
Stanford's CS336 "Language Modeling from Scratch" course published an AI agent guidelines document — essentially a CLAUDE.md for how students should use and interact with AI coding agents in an academic setting. The document covers task decomposition, tool use conventions, context management, verification expectations, and how to reason about agent output quality. It hit 1,863 stars on GitHub in under 24 hours, which is a strong signal that the broader developer community beyond academia is treating formal agent guidelines as a real engineering need, not just a course assignment.
Technical depth angle: explain why institutional agent guidelines matter for education, reproducibility, and fair evaluation; contrast structured guidelines with informal conventions; describe how a CLAUDE.md-style document can be adapted for non-academic teams.
Actionability angle: read the Stanford document, extract the conventions that apply to your team or project, and write or update a CLAUDE.md or AGENTS.md that codifies how your team expects agents to operate in your codebase.
Listener hook: when a Stanford course publishes AI agent guidelines and the community treats it as a viral engineering resource, it means the industry is formalizing what good agent behavior looks like — and that formalization is worth tracking.
Primary link: https://github.com/stanford-cs336/assignment1-basics/blob/main/CLAUDE.md

### 3. **OpenAI joins Anthropic on AWS Bedrock, completing the dual-lab distribution pattern for agent stacks**
OpenAI made GPT-4.5, the o-series models, and Codex available through AWS Bedrock, completing the dual-lab distribution pattern alongside Anthropic's Claude. For teams running OpenClaw, Hermes, or Codex inside AWS, both major labs' models are now accessible through the same AWS credential, VPC, IAM controls, and CloudWatch logging. Claude Code operators using Bedrock-backed managed cloud auto mode gain a direct path to OpenAI models alongside existing Anthropic integration, making multi-lab model routing a configuration choice rather than a custom integration project.
Technical depth angle: explain Bedrock as a multi-lab model surface, VPC-bound model access, IAM guardrails for agent tool calls, cross-provider routing within one deployment, Claude Code Bedrock auto mode, and the operational difference between two labs behind one cloud credential versus two separate API integrations.
Actionability angle: if your team runs agents inside AWS, test the Bedrock endpoints for both Anthropic and OpenAI models before committing to one lab as the sole provider; compare latency, throughput, and cost across the same task profile.
Listener hook: the AI cloud wars are settling into a practical pattern — both major labs behind one cloud credential — and that changes how enterprise teams should think about model routing.
Primary link: https://openai.com/index/openai-frontier-models-and-codex-are-now-available-on-aws/

### 4. **Expanse from YC P26 outperforms frontier LLMs by 8x on GPU resource prediction using HPC telemetry**
Expanse, a YC P26 company built by former HPC and quantitative fund engineers, tackles a specific and expensive problem: GPU cluster operators waste enormous compute on mispredicted resource requests. The team claims 59% of compute is wasted on national HPC clusters — roughly $8.5 million per month on one cluster alone. Expanse installs as a lightweight daemon on SLURM and Kubernetes nodes, ingests hardware telemetry through DCGM and CUPTI, and predicts the VRAM, utilization, and memory needs of a job before it is submitted. The model is cluster-specific and fine-tuned on actual hardware data, which means it improves over time as it accumulates more submissions from that specific cluster. In Expanse's benchmarks, the approach outperforms GPT-4.5, Claude Opus 4.8, Gemini 3.5 Pro, and Codex 5.3 by 8x on GPU resource prediction accuracy. The interesting data point for agent-stack listeners: model size does not correlate with accuracy here. Claude Haiku outperforms Opus on some workloads.
Technical depth angle: explain DCGM and CUPTI telemetry ingestion, cluster-specific fine-tuning, SLURM and Kubernetes node integration, resource prediction accuracy versus frontier model size, and how Expanse's line-level optimization suggestions work against actual code.
Actionability angle: if you run GPU workloads in HPC or cloud clusters, install Expanse on one node and compare its predictions against your actual resource usage for two weeks; the ROI is concrete and the integration is non-invasive.
Listener hook: the most capable model is not always the best at every task — and a model trained on hardware telemetry can beat frontier models by 8x on the specific job of knowing how much GPU your job actually needs.
Primary links: https://news.ycombinator.com/item?id=48356312, https://www.expanse.co

### 5. **Agent OS for hardware, terminal context managers, and physical agent schedulers hit the project radar**
The project radar covers three different layers of the agent stack. Anima from Fullive-AI is an open-source Agent OS for hardware intelligence — targeting IoT devices, robotics, and edge agents that need to reason about physical state and sensor data alongside digital tools. It is early (116 stars, pushed 2026-06-02) but the stack angle is concrete: agents that run on hardware need a different OS layer than agents that run in a cloud VM. smarthomeo's ctx is a terminal context manager that generates `.ctx.md` files which coding agents read as persistent system context across sessions — a lightweight alternative to full memory systems for teams that want context continuity without a full knowledge graph. agentgrid from hanfeihu is an open scheduling layer for AI-operated physical machines, tools, and desktops — it sits below the agent runtime and decides when and how physical actions get dispatched.
Technical depth angle: explain agent OS for hardware versus cloud VMs, terminal context files as a lightweight persistent layer, and scheduling layers for physical agent actions versus digital tool calls.
Actionability angle: for Anima, try it on a Raspberry Pi or edge device and compare its hardware-reasoning loop against a cloud-hosted agent. For ctx, add one `.ctx.md` file to a repo and observe whether a fresh agent session reads and respects it. For agentgrid, evaluate it when the task involves physical hardware timing, not just digital tool calls.
Listener hook: the agent stack is not only about LLMs and cloud VMs — hardware agents, terminal context, and physical scheduling are real problems that need real tooling.
Primary links: https://github.com/Fullive-AI/Anima, https://github.com/smarthomeo/ctx, https://github.com/hanfeihu/agentgrid

### 6. **Terminal context files and .ctx.md give coding agents persistent working context without a full memory system**
The context management story for coding agents has multiple layers: full knowledge graphs like Understand Anything (EP061), local MCP servers like Argyph (EP061), and now lightweight terminal context files. The `.ctx.md` pattern that projects like ctx use is simple: a file in the repo that the agent reads as system context at the start of each session, carrying forward conventions, task state, and project-specific notes. This is less powerful than a full memory system, but it is also less complex to set up and maintain. For a team that wants context continuity without adopting a full memory layer, the `.ctx.md` approach is a pragmatic entry point.
Technical depth angle: explain the tradeoffs between transcript-only context, lightweight context files, and full knowledge graph memory systems; describe when each layer is sufficient and when it becomes a bottleneck.
Actionability angle: add a `.ctx.md` to one repo with three sections — current task, known conventions, and open questions — then start a fresh agent session and compare what it knows versus what you had to re-explain.
Listener hook: not every team needs a full memory system; sometimes the right answer is a file in the repo that the agent reads before it starts.
Primary link: https://github.com/smarthomeo/ctx

## Model Discovery Check

- **MiniMax M3** — Primary sources: https://www.minimax.io/blog/minimax-m3, https://www.minimax.io/models/text/m3. Launched June 1, 2026 as an open-weight-positioned coding and agent model with MSA sparse attention, up to 1M context, native multimodal capability, MiniMax Code integration, and a live API. Technical report and open weights promised within 10 days of launch. Decision: not selected as a new story for EP062. Core mechanics verified: MSA/sparse attention, 1M context, multimodal, MiniMax Code, API availability.
- **No other major model candidates this cycle** — No other primary model release from checked labs (Anthropic, OpenAI, Google, xAI, Meta, Mistral, Qwen, DeepSeek) met the threshold for a new story slot in this episode. Decision: not selected.

## GitHub Project Radar

- **Stanford CS336 Agent Guidelines** - https://github.com/stanford-cs336/assignment1-basics/blob/main/CLAUDE.md - Formal AI agent guidelines for academic use, adapted from Stanford's CS336 "Language Modeling from Scratch" course. GitHub API check on 2026-06-02 showed 1,863 stars, 2,157 forks, pushed 2026-06-02. Stack improvement angle: use it as a reference when writing or updating your own team's AGENTS.md or CLAUDE.md — it is the most concrete institutional example of what structured agent conventions look like. Try now: read the conventions, extract the three that apply to your current project, and add them to your AGENTS.md.
- **Anima Agent OS** - https://github.com/Fullive-AI/Anima - Open-source Agent OS for hardware intelligence targeting IoT, robotics, and edge agent runtimes. GitHub API check on 2026-06-02 showed 116 stars, pushed 2026-06-02. Stack improvement angle: give hardware agents a structured OS layer instead of running them on bare embedded Linux. Try now: install it on a Raspberry Pi or edge device and compare its hardware-reasoning loop against a cloud-hosted agent running the same task.
- **Expanse** - https://expanse.co - YC P26 company using cluster-specific ML models to predict GPU job resource needs and reduce HPC compute waste. Benchmarks show 8x improvement over frontier LLMs on resource prediction. Stack improvement angle: if you run GPU workloads on HPC or cloud clusters, the ROI is concrete — 59% compute waste is a real number with a real dollar cost. Try now: install on one SLURM or K8s node and run two weeks of predictions against actual resource usage.
- **ctx terminal context manager** - https://github.com/smarthomeo/ctx - Generates `.ctx.md` files that coding agents read as persistent system context across sessions. GitHub API check on 2026-06-01 showed 10 stars, pushed 2026-06-01. Stack improvement angle: add lightweight context persistence to any repo without a full memory system or knowledge graph setup. Try now: add a `.ctx.md` with current task, conventions, and open questions; start a fresh agent session and measure how much you had to re-explain.
- **agentgrid** - https://github.com/hanfeihu/agentgrid - Open scheduling layer for AI-operated physical machines, tools, and desktops. GitHub API check on 2026-06-01 showed 2 stars, pushed 2026-06-01. Stack improvement angle: separate action scheduling from agent runtime for physical tasks that need timing and coordination constraints. Try now: evaluate it when your agent task involves physical hardware timing rather than purely digital tool calls.

## Extra Research Candidates

- **OpenClaw beta watch** - Primary source: https://github.com/openclaw/openclaw/releases. Technical depth angle: track v2026.6.1-beta.1 and v2026.5.31-beta.4 for app-server lifecycle, provider expansion, and input validation changes before they land as stable releases.
- **Claude Code 2.1.160 changelog** - Primary source: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md. Technical depth angle: verify what CLI changes shipped in the jump from 2.1.159 to 2.1.160 and whether any affect local agent workflows.
- **Anthropic Claude 4.8 system card deep dive** - Primary source: https://www.anthropic.com/news/claude-opus-4-8. Technical depth angle: review effort controls, fast-mode pricing, tool efficiency, and safety evaluation methodology for coding-agent task selection.

## Show Notes

```md
Codex `rust-v0.136.0` leads EP062 as the stable CLI release for June 1, followed by Stanford's viral AI agent guidelines, OpenAI on AWS Bedrock, and a YC-backed GPU efficiency project. The project radar covers agent OS for hardware, terminal context files, and physical agent schedulers.

[00:00] Opening: CLI releases, institutional guidelines, and cloud distribution
The useful lane for EP062 is a mix of CLI tooling, institutional validation, and real-world infrastructure. Codex `rust-v0.136.0` is the stable release that moved the needle on TUI diagnostics, app-server lifecycle, hook scoping, and SDK improvements. Stanford's CS336 agent guidelines document is the unexpected story — an academic course that published AI agent conventions and hit 1,863 stars in under 24 hours, which tells us that formalizing how agents should work is no longer a niche educational concern. OpenAI putting frontier models and Codex on AWS Bedrock completes the dual-lab Bedrock pattern that enterprise agent stacks are starting to rely on. Expanse from YC P26 solves a specific and expensive problem: predicting how much GPU a job actually needs and outperforming frontier models by 8x on that task by training on real cluster telemetry.

[03:00] Codex rust-v0.136.0 release deep dive
Codex `rust-v0.136.0` is the June 1 stable release, and it is a diagnostics and reliability wave. The most operationally useful change is in `codex doctor` output — error messages now carry better location and cause information, which matters for local agents where a failure can come from the shell environment, the remote transport, the app-server state, the Git repo, or the model itself. When something breaks, the difference between "something failed" and "the thread inventory check timed out because the remote transport did not recover from a network hiccup" is the difference between debugging and guessing.

App-server lifecycle handling is tighter. The server starts and stops more cleanly, model selection at startup is more reliable across provider configurations, and remote transport connections recover faster after a temporary network issue. That last point is worth dwelling on because remote Codex work — supervising a Windows host from an iPhone, for instance — is only practical if the transport can recover from a WiFi hiccup without requiring a full restart. The release addresses that.

Hook configuration gets named hooks and permission scopes. Previously, an operator who wanted the same hook behavior across multiple projects had to copy the hook configuration block into each project file. Named hooks let you define the behavior once and reference it by name across configurations. Permission scopes do the same thing for the `/permissions` endpoint — instead of one flat permission set, operators can define scopes that represent different trust levels or different project contexts.

The Python SDK and Node SDK both receive thread management, turn handling, and error propagation improvements. Non-interactive installation via `CODEX_NON_INTERACTIVE=1` works more reliably, which matters for teams that want to roll out Codex through a configuration management tool rather than an interactive install script.

The upgrade recommendation is straightforward: test `codex doctor` output against a known failing configuration, define one named hook for a pattern you use across projects, and verify that non-interactive install works in your CI pipeline before relying on it for automated deployment.

[11:00] Stanford CS336 AI agent guidelines: when institutional validation goes viral
Stanford's CS336 course — "Language Modeling from Scratch" — published a formal AI agent guidelines document that the GitHub community treated as a viral engineering resource. The document covers how students should decompose tasks, use tools, manage context, verify outputs, and reason about agent quality in an academic setting. It reached 1,863 stars in under 24 hours, which is an unusually strong signal for a course assignment artifact.

The story here is not about the document being perfect or comprehensive. It is about the fact that the community saw it and treated it as a reference, not just a course sample. That tells us something about where the industry is: teams are writing AGENTS.md files, CLAUDE.md files, and similar conventions, but they are doing it from scratch and without a clear reference point. Stanford's document gives them one, even if it comes from an academic context.

The practical move is to read it, extract the conventions that apply to your team, and use them as a starting point for your own AGENTS.md. The format is adaptable — the principles apply beyond the course context — and the fact that it is MIT-licensed means it can be used freely as a foundation.

[18:00] OpenAI on AWS Bedrock: the dual-lab pattern is complete
OpenAI made GPT-4.5, the o-series models, and Codex available through AWS Bedrock. Anthropic's Claude has been on Bedrock for a while. This means enterprise agent stacks can now provision both major labs' models through the same AWS credential, same VPC, same IAM controls, and same CloudWatch logging.

The practical implication for OpenClaw, Hermes, and Codex operators is straightforward: multi-lab model routing becomes a configuration choice rather than a custom integration project. A team that wants to use Claude for planning tasks and OpenAI for code generation can do that inside the same AWS account, with the same credential rotation, the same compliance boundaries.

The cloud distribution pattern is worth noting: both labs chose AWS first. That says something about where enterprise AI spending is concentrated and which cloud provider has the most trust from the teams that buy AI capabilities at scale.

[25:00] Expanse: 8x better GPU prediction by training on cluster telemetry
Expanse from YC P26 solves a problem that HPC operators know well but general software teams often overlook: GPU jobs request more resources than they actually need because the submitter has no good way to predict real usage. The result is wasted compute — Expanse's team measured 59% compute waste on national HPC clusters, roughly $8.5 million per month on one cluster alone.

Expanse works by installing a lightweight daemon on SLURM and Kubernetes nodes, ingesting hardware telemetry through DCGM and CUPTI, and predicting the VRAM, utilization, and memory needs of each job before it runs. The model is cluster-specific — it fine-tunes on the actual submission history of that specific cluster, so it gets better over time as it accumulates more data.

The benchmark result is striking: Expanse outperforms GPT-4.5, Claude Opus 4.8, Gemini 3.5 Pro, and Codex 5.3 by 8x on GPU resource prediction accuracy. The interesting detail for agent-stack listeners is that model size does not predict accuracy here. Claude Haiku outperforms Opus on some workloads because the fine-tuning on cluster telemetry matters more than general reasoning capability.

For teams running GPU workloads — training, fine-tuning, inference, batch processing — the ROI is concrete. The integration is non-invasive: install the daemon on one node, run predictions against actual resource usage for two weeks, and compare.

[33:00] Project radar: agent OS, terminal context, and physical scheduling
The project radar covers three different layers of the agent stack.

Anima is an open-source Agent OS for hardware intelligence. Most agent discussion assumes cloud VMs, but agents that run on IoT devices, robotics, and edge hardware need a different OS layer — one that can reason about sensor data, physical state, and real-time constraints alongside digital tool calls. Anima is early at 116 stars, pushed June 2, but the shape of the problem is real.

ctx is a terminal context manager that generates `.ctx.md` files. The pattern is simple: a file in the repo that the agent reads as system context at the start of each session, carrying forward conventions, task state, and project notes. This is less powerful than a full knowledge graph memory system, but it is also less complex to set up and maintain. For teams that want context continuity without committing to a full memory architecture, `.ctx.md` is a pragmatic entry point.

agentgrid is an open scheduling layer for AI-operated physical machines, tools, and desktops. It sits below the agent runtime and decides when and how physical actions get dispatched. For agents that need to coordinate physical hardware timing — not just call digital tools — a scheduling layer that understands physical constraints is more appropriate than a pure LLM-driven action loop.

[41:00] Practical queue
For Codex, run `codex doctor` and compare the output, define one named hook for a cross-project pattern, and verify non-interactive install in CI. For Stanford's guidelines, read the document, extract what applies to your team, and update your AGENTS.md. For AWS model routing, test Bedrock endpoints for both Anthropic and OpenAI before committing to one lab as the sole provider. For Expanse, install on one cluster node if you run GPU workloads at scale. For the project radar, try Anima on an edge device, add a `.ctx.md` to one repo, and evaluate agentgrid when the task involves physical hardware timing.

The theme across EP062 is infrastructure becoming visible: diagnostics make failures explainable, guidelines make expectations legible, cloud distribution makes model routing a configuration choice, and cluster-specific ML makes compute waste measurable and fixable. The agent stack is growing up in the ways that matter for operators.
```

## Chapters

- 00:00 Opening: CLI releases, institutional guidelines, and cloud distribution
- 03:00 Codex rust-v0.136.0 release deep dive
- 11:00 Stanford CS336 AI agent guidelines: when institutional validation goes viral
- 18:00 OpenAI on AWS Bedrock: the dual-lab pattern is complete
- 25:00 Expanse: 8x better GPU prediction by training on cluster telemetry
- 33:00 Project radar: agent OS, terminal context, and physical scheduling
- 41:00 Practical queue

## Verified Links

- Codex rust-v0.136.0: https://github.com/openai/codex/releases/tag/rust-v0.136.0
- Codex rust-v0.135.0: https://github.com/openai/codex/releases/tag/rust-v0.135.0
- Stanford CS336 Agent Guidelines: https://github.com/stanford-cs336/assignment1-basics/blob/main/CLAUDE.md
- OpenAI on AWS: https://openai.com/index/openai-frontier-models-and-codex-are-now-available-on-aws/
- Expanse: https://expanse.co
- Expanse HN: https://news.ycombinator.com/item?id=48356312
- Anima Agent OS: https://github.com/Fullive-AI/Anima
- ctx terminal context manager: https://github.com/smarthomeo/ctx
- agentgrid: https://github.com/hanfeihu/agentgrid
- Claude Code npm: https://www.npmjs.com/package/@anthropic-ai/claude-code
- Anthropic Claude Opus 4.8: https://www.anthropic.com/news/claude-opus-4-8