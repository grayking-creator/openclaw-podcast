# AgentStack Daily EP064 — Claude Code 2.1.165, Microsoft MAI Model Family, and Agent Infrastructure

**Title:** Claude Code 2.1.165, Microsoft's MAI Coding Model Family, and the Agent Infrastructure Project Radar

**Tagline:** Claude Code ships three quiet point releases, Microsoft lands a seven-model MAI family with a Copilot-native 5B coding model, and the project radar surfaces code graphs, MCP management, and agent memory tools that make local stacks less fragile.

**Feed description:** Claude Code 2.1.165 is the latest npm `latest` as of June 5, following 2.1.163 and 2.1.164 — all bug-fix and reliability releases that clean up background sessions, plugin hooks, skill syntax, and Windows path handling. Microsoft dropped a seven-model MAI family at Build 2026 on June 2, with MAI-Code-1-Flash as the headline: a 5B-parameter coding model trained on GitHub Copilot production harnesses, scoring 51% on SWE-Bench Pro and 60% leaner on tokens than comparable models. The episode also covers the GitHub Project Radar around agent memory, code graphs, and MCP tooling that serve the local coding-agent stack.

---

## Story Slate

1. **Claude Code 2.1.165 closes background session gaps, hook extensions, and Windows path bugs** — Claude Code's npm `latest` is now 2.1.165, published June 5, 2026. The three-release block from EP063's 2.1.162 baseline to 2.1.165 is a quiet hygiene wave with operator-visible fixes. Version 2.1.163 adds `requiredMinimumVersion` and `requiredMaximumVersion` managed settings — Claude Code refuses to start if its version falls outside the allowed range, which matters for org-managed fleet compliance. The `/plugin list` command now shows installed plugins with `--enabled`/`--disabled` filters. Stop and SubagentStop hooks can now return `hookSpecificOutput.additionalContext` to give Claude feedback without the turn being labeled a hook error. Skills add a `\$` escape syntax for literal `$` before a digit. stdio MCP servers now receive the same `CLAUDE_CODE_SESSION_ID` as hooks and Bash on `--resume`. Several Windows and background-session bugs are fixed: `$TMPDIR` override regression from 2.1.154 that broke Bazel and EDR-protected Go workflows, Windows OneDrive read-only attribute failures, background sessions losing running tasks on reattach after update, and cross-session messaging silently breaking on deep `$TMPDIR` paths. Version 2.1.165 is pure bug fixes and reliability improvements.

Technical depth angle: explain required version range gating as a fleet compliance primitive, hook `additionalContext` return semantics and when a hook can extend a turn without error-labeling, `\$` escape syntax in skill command bodies, stdio MCP session ID parity with hooks and Bash on resume, `$TMPDIR` override regression and why it broke only sandboxed commands, and deep path socket binding failures under `$TMPDIR`.

Actionability angle: if you manage a Claude Code fleet, set `requiredMinimumVersion` and `requiredMaximumVersion` in your org config to enforce version gates; run `/plugin list` to audit what is actually installed; test one Stop/SubagentStop hook that returns `additionalContext` to verify the turn extension works without errors; check your `$TMPDIR` depth if you use Bazel or EDR-protected environments.

Listener hook: three point releases in a week sounds boring, but the fixes touch exactly the workflows that make operators say "I did not know that could break" — background sessions, deep paths, Windows OneDrive, and fleet version compliance.

2. **Microsoft MAI-Code-1-Flash brings a Copilot-native 5B coding model to the agent stack** — Microsoft announced a seven-model MAI family at Build 2026 on June 2, 2026. The headline for the agent stack is MAI-Code-1-Flash: a 5-billion-parameter coding model trained directly on GitHub Copilot production tool harnesses, not generic benchmark datasets. Microsoft claims 51% on SWE-Bench Pro — a +16-point lead over Claude Haiku 4.5 on the same harness — and 60% fewer solution tokens on complex tasks. The model uses adaptive solution length control, meaning it stays concise on simple requests and spends more reasoning budget on harder problems. MAI-Code-1-Flash is rolling out inside GitHub Copilot and VS Code, and the MAI-Thinking-1 model (35B active / ~1T total parameters) is in private preview on Microsoft Foundry, positioned against Claude Opus 4.6 on SWE-Bench Pro. The broader MAI family covers image (MAI-Image-2.5 at 1403 Arena Score), voice, and reasoning models. The strategic signal: Microsoft is reducing OpenAI dependency and competing on foundation model capabilities with training pipelines tuned to its own developer stack.

Technical depth angle: explain adaptive solution length control as a token-efficiency mechanism, SWE-Bench Pro as a production harness benchmark versus synthetic bench setups, training on Copilot production harnesses versus benchmark datasets, MAI-Thinking-1's active/total parameter architecture on Foundry, and why the MAI family strategy matters for model routing in Microsoft-aligned stacks.

Actionability angle: if you use GitHub Copilot, the MAI-Code-1-Flash model is already rolling into your workflow — test it on one real coding task and compare token usage against your previous model; if you evaluate models for an agent stack, pull MAI-Code-1-Flash benchmarks from Microsoft's production harness and compare against Haiku-class and Opus-class baselines on your own repo tasks.

Listener hook: Microsoft trained a coding model on its own production tool harnesses, not public benchmarks — and it scored 51% on SWE-Bench Pro while using 60% fewer tokens. That is the efficiency story the agent stack has been waiting for.

3. **MAI-Image-2.5 puts Microsoft ahead on image editing benchmarks, but the agent use case is specific** — MAI-Image-2.5 scored 1403 on the Arena Image Edit leaderboard as of June 2, 2026, ahead of Gemini 3 Pro Image Preview 2K at 1388. Microsoft's image model is part of the same MAI family announcement, and it is worth covering because image editing benchmarks are one of the few places where Microsoft is demonstrably ahead of Google on a multimodal leaderboard right now. The agent-stack angle is not about replacing Midjourney or DALL-E — it is about whether Microsoft-integrated agent workflows can now use MAI-Image for documentation, UI mockups, diagram generation, and screenshot annotation without leaving the Copilot/Foundry surface. For OpenClaw, Codex, and Claude Code operators who work inside Microsoft shops, this closes a gap where image tasks had to route outside the stack.

Technical depth angle: explain Arena Image Edit leaderboard scoring methodology, MAI-Image-2.5's position relative to Gemini 3 Pro on the same leaderboard, the distinction between text-to-image and image-to-image editing tasks, and what the leaderboard score does and does not guarantee for real-world agent image workflows.

Actionability angle: if you run agents inside a Microsoft-aligned stack, test MAI-Image-2.5 through Copilot or Foundry on one image editing task — generate a UI mockup, annotate a screenshot, or create a diagram — and compare the output quality and latency against your current image tool.

Listener hook: Microsoft is ahead of Gemini on an image editing leaderboard for the first time in a while, and the model is already inside Copilot — that changes what image tasks look like inside a Microsoft shop.

4. **NVIDIA Cosmos 3 opens physical AI development with an open world foundation model** — NVIDIA launched Cosmos 3 at COMPUTEX 2026 in June as an open world foundation model for physical AI. The model combines vision reasoning, world generation, and action prediction in a single mixture-of-transformers architecture. Three sizes are available: Cosmos 3 Nano (16B parameters, workstation-grade RTX PRO 6000), Cosmos 3 Super (64B parameters, data center Hopper/Blackwell), and Cosmos 3 Edge (forthcoming, edge inference). Cosmos 3 is open for research and commercial use with training scripts, deployment tools, and datasets on Hugging Face and GitHub. Benchmarks show leading results on Artificial Analysis, Physics-IQ, PAI-Bench, R-Bench for world generation, RoboLab and RoboArena for action policy, and VANTAGE-Bench and TAR for vision understanding. The agent-stack angle is not immediate coding work — it is about understanding what physical AI means for the next generation of agent hardware, robot training pipelines, and simulation-based development that agents will interact with.

Technical depth angle: explain mixture-of-transformers architecture for physical AI, vision reasoning plus world generation plus action prediction unification, synthetic video generation for training data, Cosmos 3 Nano/Super/Edge size tiers and target hardware, open model release with training scripts and datasets, and benchmark coverage across physics, robotics, and vision.

Actionability angle: if you work on robotics, autonomous vehicles, or simulation-based agent training, pull the Cosmos 3 model from Hugging Face and run it against your physical AI benchmark suite; for general agent-stack listeners, the practical move is understanding what physical AI foundation models mean for edge agent hardware in 12-18 months.

Listener hook: the agent stack is not only about cloud coding agents — NVIDIA just open-sourced a foundation model for physical AI that will shape how agents interact with robots, vehicles, and real-world environments.

5. **GitHub Copilot desktop app brings agent-native multi-agent orchestration to the Copilot stack** — GitHub launched a native desktop application for Copilot at Build 2026, designed for agent-native development. The app positions Copilot as a centralized control center for managing multiple AI agents in parallel across repositories. Key features: a "My Work" dashboard for monitoring and directing active agent sessions, issues, pull requests, and background automations; isolated Git worktrees for each session preventing parallel agent conflicts; "Canvases" — interactive two-way visual surfaces where developers and agents collaborate in real time on plans, terminal outputs, deployments, and browser sessions; Agent Merge for carrying pull requests through reviews, checks, and merging; cloud and local sandboxing for secure code testing; and a generally available GitHub Copilot SDK in Node.js/TypeScript, Python, Go, .NET, Rust, and Java. The redesigned Copilot CLI includes voice mode and experimental tabbed access to pull requests, issues, and gists. Currently in technical preview for Copilot Pro, Pro+, Max, Business, and Enterprise subscribers on Windows 11, Windows 11 on Arm, Mac, and Linux.

Technical depth angle: explain isolated Git worktree per session as a parallelization primitive, Canvas as a two-way interactive surface for agent-developer collaboration, Agent Merge as a workflow automation layer for PRs, the Copilot SDK as an extension surface for building custom tools, and voice mode in the CLI as a new input modality.

Actionability angle: if you are a Copilot Pro or Enterprise subscriber, join the technical preview and test one parallel agent session on a low-risk repo; use the Copilot SDK to build one custom tool that extends how an agent interacts with your existing workflow; test voice mode in the CLI on one pull request or issue query.

Listener hook: GitHub is not just an AI coding assistant anymore — the new desktop app turns Copilot into a multi-agent orchestration surface with isolated worktrees, real-time Canvases, and an SDK for building custom agent tools.

6. **OpenHands 1.6.0 brings Kubernetes support and planning mode to autonomous coding agents** — OpenHands, formerly OpenDevin, is a leading open-source autonomous AI software development agent with over 70,000 GitHub stars, $18.8M Series A funding, and production usage at AMD, Apple, Google, Amazon, Netflix, and NVIDIA. Version 1.6.0 shipped in March 2026 with Kubernetes support and a beta Planning Mode. The agent operates in a sandboxed environment with an embedded shell, web browser, code editor, and task planner — performing end-to-end software engineering tasks including code writing, command-line interaction, web browsing, testing, and debugging. LLM flexibility supports GPT-4, Claude, Gemini, local models, and others. The Kubernetes support means OpenHands can now orchestrate containerized agent workloads at scale, and the Planning Mode beta adds explicit task decomposition before execution. For the agent stack, OpenHands is a primary reference point for what autonomous coding agents look like when they are production-hardened and running in enterprise environments.

Technical depth angle: explain Kubernetes integration for containerized agent workloads, Planning Mode as explicit task decomposition before execution, sandboxed environment architecture (shell, browser, code editor, task planner), LLM flexibility across providers, and what enterprise production usage at major labs tells us about autonomous agent reliability.

Actionability angle: if you evaluate autonomous coding agents for production use, run OpenHands against one of your repos and compare its end-to-end task completion against a single-turn coding agent; test the Planning Mode beta on a multi-step task and verify whether explicit decomposition improves output quality; if you run Kubernetes, test the containerized agent workload orchestration.

Listener hook: OpenHands is not a research demo — it has 70,000 stars, enterprise production users, and a Series A. Version 1.6.0 with Kubernetes and Planning Mode is the most production-hardened autonomous coding agent you can study today.

---

## Model Discovery Check

**Lane: OpenRouter / Open-Source / Agent-Focused Models**

Recent episode model coverage detected:
- MiniMax M3 (open-weight, 1M context, MSA/sparse attention, multimodal, MiniMax Code, coding/agentic)
- Qwen 3.7 Max/Plus (coding-reasoning vs multimodal-vision split, open weights)
- Claude Opus 4.8 (Anthropic, coding agent model)
- GPT-5.5 (OpenAI)
- Gemini 3.x (Google)

Newly discovered models post-last-update:
- **Microsoft MAI-Code-1-Flash** — Provider: Microsoft AI. Release date: June 2, 2026 (Build 2026). Availability: GitHub Copilot, VS Code, Microsoft Foundry (MAI-Thinking-1 private preview). Architecture: 5B active parameters, adaptive solution length control, trained on GitHub Copilot production harnesses. Primary source: https://microsoft.ai/news/introducingmai-code-1-flash/. Decision: **SELECTED** — headline MAI model drop at Build 2026, Copilot-native positioning, 51% SWE-Bench Pro with 60% fewer tokens, directly relevant to the coding-agent stack.
- **Microsoft MAI-Image-2.5** — Provider: Microsoft AI. Release date: June 2, 2026. Availability: GitHub Copilot, Microsoft AI services. Architecture: image editing model, 1403 Arena Image Edit score. Primary source: https://microsoft.ai/news/microsoft-build-2026-mai-keynote-transcript/. Decision: **SELECTED** — Microsoft ahead of Gemini on image editing leaderboard, agent use case for Microsoft-integrated stacks.
- **Microsoft MAI-Thinking-1** — Provider: Microsoft AI. Release date: June 2, 2026. Availability: Microsoft Foundry (private preview). Architecture: 35B active / ~1T total parameters, reasoning model. Primary source: https://microsoft.ai/news/microsoft-build-2026-mai-keynote-transcript/. Decision: **NOT SELECTED** — private preview on Foundry, not yet available for general use, limited builder impact until GA.
- **NVIDIA Cosmos 3** — Provider: NVIDIA. Release date: June 2026 (COMPUTEX 2026). Availability: open weights on Hugging Face and GitHub, training scripts and datasets. Architecture: mixture-of-transformers, physical AI (vision reasoning + world generation + action prediction), three sizes (Nano 16B, Super 64B, Edge forthcoming). Primary source: https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai. Decision: **SELECTED** — major open physical AI foundation model, open release with training scripts, benchmark-leading on physics/robotics/vision, relevant to future edge agent hardware.

---

## GitHub Project Radar

- **GitHub Copilot desktop app** — https://github.com/features/ai/github-app — Native desktop app for agent-native Copilot development. Technical preview at Build 2026. Stack improvement angle: turn Copilot from a reactive single-agent assistant into a multi-agent orchestration surface with isolated worktrees, real-time Canvases, and an SDK for custom tools. Try now: join the technical preview if you are a Copilot Pro/Enterprise subscriber, run one parallel agent session on a low-risk repo, and test the Copilot SDK on one custom tool extension.
- **OpenHands** — https://github.com/OpenHands/openhands — Open-source autonomous AI software development agent, 70,000+ stars, enterprise production at AMD/Apple/Google/Amazon/Netflix/NVIDIA. Stack improvement angle: study it as the reference implementation for production-grade autonomous coding agents with Kubernetes orchestration and explicit Planning Mode. Try now: run OpenHands against one of your repos, test Planning Mode on a multi-step task, and compare end-to-end task completion against a single-turn coding agent.
- **Understand Anything** — https://github.com/Lum1104/Understand-Anything — Interactive knowledge graphs for codebases. GitHub API metadata verified 48,236+ stars, MIT license. Primary stack/tool adjacency: Claude Code, Codex, Cursor, Copilot, Gemini CLI, and codebase-understanding workflows. Stack improvement angle: give coding agents a navigable project graph before they spend context on broad file scans. Try now: run it on a repo with confusing entry points, ask for the request path, then compare the agent plan before and after graph orientation.

---

## Extra Research Candidates

- **Microsoft MAI-Thinking-1 on Foundry** — Primary source: https://microsoft.ai/news/microsoft-build-2026-mai-keynote-transcript/. Technical depth angle: explain 35B active/~1T total parameter architecture, private preview on Foundry, toe-to-toe positioning against Claude Opus 4.6 on SWE-Bench Pro, and what private preview means for builder access.
- **NVIDIA Cosmos 3 benchmark methodology** — Primary source: https://developer.nvidia.com/blog/develop-physical-ai-reasoning-world-and-action-models-with-nvidia-cosmos-3/. Technical depth angle: explain mixture-of-transformers architecture, synthetic data generation pipeline, physical AI benchmark coverage (Physics-IQ, PAI-Bench, RoboLab, RoboArena), and how open weights and training scripts change who can fine-tune on physical AI data.
- **Claude Code 2.1.163 plugin/hook extensibility** — Primary source: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md. Technical depth angle: explain `requiredMinimumVersion`/`requiredMaximumVersion` fleet compliance semantics, hook `additionalContext` return contract, `\$` escape syntax in skill command bodies, and stdio MCP session ID parity with hooks on resume.

---

## Show Notes

```md
Episode 64 — June 5, 2026

[00:00] Episode hook

Claude Code 2.1.165 lands as the latest npm `latest` on June 5, 2026, following 2.1.163 and 2.1.164 — all quiet hygiene releases that clean up background sessions, plugin hooks, skill syntax, and Windows path handling. Microsoft dropped a seven-model MAI family at Build 2026 on June 2, with MAI-Code-1-Flash as the headline: a 5B-parameter coding model trained on GitHub Copilot production harnesses, scoring 51% on SWE-Bench Pro and 60% leaner on tokens than comparable models. MAI-Image-2.5 hits 1403 on the Arena Image Edit leaderboard, ahead of Gemini 3 Pro. NVIDIA's Cosmos 3 opens physical AI development with an open world foundation model available in three sizes on Hugging Face and GitHub. The project radar covers agent memory, code graphs, and MCP tooling that serve the local coding-agent stack.

[02:00] Claude Code 2.1.165 — three-release hygiene block for background sessions, hooks, and Windows

Claude Code 2.1.165 is the June 5 npm `latest`, completing a three-release hygiene block from the EP063 baseline of 2.1.162. The block is not a feature wave — it is the kind of release that closes gaps operators discover when a workflow goes wrong.

Version 2.1.163 is the most operationally interesting of the three. `requiredMinimumVersion` and `requiredMaximumVersion` managed settings let org admins enforce version gates — Claude Code refuses to start if its version falls outside the allowed range and directs the user to an approved version. For fleet operators who need deterministic behavior across versions, this is a real compliance primitive. `/plugin list` now shows installed plugins with `--enabled`/`--disabled` filters, which matters when plugin sprawl makes it hard to audit what is actually loaded.

Stop and SubagentStop hooks gain the ability to return `hookSpecificOutput.additionalContext` — the hook can give Claude feedback and keep the turn going without being labeled a hook error. That changes how hook authors can extend a session: a hook that needs to surface information without blocking the turn now has a clean contract. Skills add a `\$` escape syntax for literal `$` before a digit, which matters for command bodies that include shell variable references. stdio MCP servers now receive the same `CLAUDE_CODE_SESSION_ID` as hooks and Bash on `--resume`, which closes a gap where MCP servers could not correlate a session across resume operations.

The Windows fixes are worth noting individually. A regression in 2.1.154 caused `$TMPDIR` to be overridden to `/tmp/claude-{uid}` for all Bash commands instead of only sandboxed ones, which broke Bazel and EDR-protected Go workflows that depend on the actual temp directory. Bash commands now fail correctly on Windows when the session-env directory has the read-only attribute or lives inside OneDrive. Cross-session messaging (`SendMessage`) silently broke when `CLAUDE_CODE_TMPDIR` or `$TMPDIR` pointed at a deep directory — that is now fixed.

Version 2.1.165 is pure bug fixes and reliability improvements. The practical upgrade list: audit your fleet's version compliance settings, run `/plugin list` to see what is actually installed, test one hook that returns `additionalContext` to verify turn extension behavior, and verify that Bazel and EDR-protected workflows run correctly after the `$TMPDIR` regression fix.

[14:00] Microsoft MAI family at Build 2026 — MAI-Code-1-Flash and the Copilot-native coding model

Microsoft opened Build 2026 on June 2 with a seven-model MAI family announcement. The model that matters most for the agent stack is MAI-Code-1-Flash: a 5-billion-parameter coding model trained directly on GitHub Copilot production tool harnesses, not on generic benchmark datasets. The training approach is the key differentiator. By training on the same harnesses developers use for their everyday coding tasks, the model learns how to interact with surrounding tools and systems in agentic coding workflows — not just how to answer a benchmark prompt.

The benchmark numbers are concrete. MAI-Code-1-Flash scores 51% on SWE-Bench Pro, a +16-point lead over Claude Haiku 4.5 on the same production harness. On SWE-Bench Verified, SWE-Bench Multilingual, and Terminal Bench 2, it outperforms Haiku 4.5 across all four core coding benchmarks. The adaptive solution length control is the efficiency mechanism: the model stays concise on simple requests and allocates more reasoning budget on harder problems. Microsoft sees 60% fewer solution tokens on complex tasks, which translates to lower latency, lower cost, and smoother interactive workflows.

MAI-Image-2.5 scored 1403 on the Arena Image Edit leaderboard as of June 2, ahead of Gemini 3 Pro Image Preview 2K at 1388. That is a real leaderboard position for Microsoft in multimodal image editing — the first time in a while it has been demonstrably ahead of Google on a comparable benchmark. For agent stacks inside Microsoft shops, this closes a gap where image tasks had to route outside the Copilot/Foundry surface.

MAI-Thinking-1 (35B active / ~1T total parameters) is in private preview on Microsoft Foundry, positioned against Claude Opus 4.6 on SWE-Bench Pro. The full MAI family covers image, voice, and reasoning models, but MAI-Code-1-Flash is the one that changes coding-agent workflows today.

The strategic signal: Microsoft is reducing OpenAI dependency and competing on foundation model capabilities with training pipelines tuned to its own developer stack. For agent-stack operators who route between labs, this adds a new Copilot-native model that is already inside the tools they use.

[26:00] NVIDIA Cosmos 3 — open physical AI foundation model for the next generation of agents

NVIDIA launched Cosmos 3 at COMPUTEX 2026 as an open world foundation model for physical AI. The model combines vision reasoning, world generation, and action prediction in a single mixture-of-transformers architecture — three capabilities that were previously separate systems. Three sizes are available: Cosmos 3 Nano (16B parameters, optimized for workstation-grade RTX PRO 6000 GPUs), Cosmos 3 Super (64B parameters, targeting data center Hopper and Blackwell GPUs for large-scale synthetic data generation), and Cosmos 3 Edge (forthcoming, for real-time edge inference).

Cosmos 3 is open for research and commercial use. NVIDIA has released the model weights, training scripts, deployment tools, and datasets on Hugging Face and GitHub. The benchmark coverage is broad: Artificial Analysis, Physics-IQ, PAI-Bench, R-Bench for world generation accuracy, RoboLab and RoboArena for action policy, and VANTAGE-Bench and TAR for vision understanding. Among open models, Cosmos 3 leads on these benchmarks.

The agent-stack angle is not immediate coding work — it is about understanding what physical AI foundation models mean for the next generation of agent hardware. Agents that interact with robots, vehicles, and real-world environments need exactly the capabilities Cosmos 3 combines: vision reasoning, world simulation, and action prediction. For operators watching the horizon, this is the open foundation model that robotics teams and simulation-based development shops will build on.

[35:00] GitHub Copilot desktop app — agent-native orchestration for the Copilot stack

GitHub's new desktop app is the product announcement that turns Copilot from a reactive coding assistant into a proactive multi-agent orchestration surface. The "My Work" dashboard monitors and directs multiple AI agents simultaneously across repositories, issues, pull requests, and background automations. Each session runs in its own isolated Git worktree — that is the key architectural decision for parallel agent work: no branch conflicts, no manual branch management, no session interference when two agents operate on the same codebase at the same time.

Canvases are the most novel interaction design. They are interactive, two-way visual surfaces where developers and agents collaborate in real time. The agent displays its current plan, terminal outputs, deployments, or browser sessions on the Canvas. The developer can inspect, steer, and verify the work without switching windows. That is a different model from the terminal-and-chat pattern most agents use today.

Agent Merge automates the pull request lifecycle from picking up an issue through review, checks, and merging. The Copilot SDK is generally available in six languages, which means custom tools and agent extensions become a first-class development surface rather than a hack. Voice mode in the CLI adds a new input modality for developers who prefer speech to typing.

The practical move: if you are a Copilot Pro or Enterprise subscriber, join the technical preview and test one parallel agent session on a low-risk repo. Use the SDK to build one custom tool that extends how an agent interacts with your existing workflow.

[44:00] OpenHands 1.6.0 — Kubernetes, Planning Mode, and enterprise-grade autonomous coding

OpenHands is the most production-hardened autonomous coding agent in the open-source ecosystem. Version 1.6.0 shipped in March 2026 with two major additions: Kubernetes support for containerized agent workloads at scale, and a beta Planning Mode that adds explicit task decomposition before execution.

The agent architecture is worth understanding as a reference point. OpenHands runs in a sandboxed environment with an embedded shell, web browser, code editor, and task planner. It performs end-to-end software engineering tasks — writing and modifying code, running commands, browsing the web, running tests, debugging — without switching environments. LLM flexibility means you can plug in GPT-4, Claude, Gemini, local models, or others.

The enterprise adoption list is the most concrete signal: AMD, Apple, Google, Amazon, Netflix, and NVIDIA are using it in production. That tells you something about where autonomous coding agents are in the maturity curve — not research prototypes, but production tools in some of the most demanding engineering environments.

For the agent stack, OpenHands is a primary reference for what production autonomous coding looks like. The Kubernetes integration means it can now be part of a containerized, orchestrated agent infrastructure. The Planning Mode beta is worth watching because explicit decomposition before execution is one of the gaps that separates autonomous agents that work in demos from those that work in production.

[53:00] Practical queue

For Claude Code, audit your fleet version compliance settings, run `/plugin list` to see what is actually installed, and verify that Bazel and EDR-protected workflows run correctly after the `$TMPDIR` regression fix. For Microsoft MAI, test MAI-Code-1-Flash through GitHub Copilot on one real coding task and compare token usage; if you are inside a Microsoft shop, test MAI-Image-2.5 through Copilot on one image editing task. For NVIDIA Cosmos 3, pull the model from Hugging Face if you work on physical AI or robotics, and track the Edge size tier for future edge agent hardware. For GitHub Copilot desktop app, join the technical preview and test one parallel agent session on a low-risk repo. For OpenHands, run it against one of your repos, test Planning Mode on a multi-step task, and compare end-to-end task completion against a single-turn coding agent.
```

---

## Chapters

- 00:00 — Intro: Claude Code 2.1.165, Microsoft MAI family, Cosmos 3, agent infrastructure
- 02:00 — Claude Code 2.1.165: three-release hygiene block for background sessions, hooks, and Windows
- 14:00 — Microsoft MAI family at Build 2026: MAI-Code-1-Flash and the Copilot-native coding model
- 26:00 — NVIDIA Cosmos 3: open physical AI foundation model for the next generation of agents
- 35:00 — GitHub Copilot desktop app: agent-native orchestration for the Copilot stack
- 44:00 — OpenHands 1.6.0: Kubernetes, Planning Mode, and enterprise-grade autonomous coding
- 53:00 — Practical queue

---

## Primary Links

- Claude Code changelog: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
- Claude Code npm: https://www.npmjs.com/package/@anthropic-ai/claude-code
- MAI-Code-1-Flash: https://microsoft.ai/news/introducingmai-code-1-flash/
- Microsoft Build 2026 MAI keynote: https://microsoft.ai/news/microsoft-build-2026-mai-keynote-transcript/
- NVIDIA Cosmos 3: https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai
- GitHub Copilot desktop app: https://github.com/features/ai/github-app
- OpenHands: https://github.com/OpenHands/openhands
- Understand Anything: https://github.com/Lum1104/Understand-Anything

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.6.1`, published 2026-06-03T19:35:12Z from GitHub releases. Recent episode version tags detected: `v2026.6.1` (EP063). No new stable release since EP063. `v2026.6.2-beta.1` is a prerelease and excluded from stable coverage.
- **Hermes Agent** — Latest stable verified: `v2026.5.29.2` / `v0.15.2`, published 2026-05-29T13:37:26Z from GitHub releases. Recent episode version tags detected: `v2026.5.29.2` (EP063). No new stable release since EP063.
- **OpenAI Codex app/CLI** — Latest stable verified: `rust-v0.135.0`, published 2026-05-28T17:31:35Z from GitHub releases. Recent episode version tags detected: `rust-v0.135.0` (EP063). No stable release since EP063. Prerelease `rust-v00.138.0-alpha.4` is excluded.
- **Claude Code CLI** — Latest npm `latest` verified: `2.1.165`, published 2026-06-05T05:45:06Z; npm `stable` dist-tag verified as `2.1.153`. Recent episode version tags detected: `2.1.162` (EP063). Selected missing versions from npm `latest`: `2.1.163`, `2.1.164`, `2.1.165`.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags. Latest build as of 2026-06-05. Antigravity CLI launched May 19, 2026 at Google I/O as the successor to Gemini CLI. No version-tagged releases tracked in prior episodes.

---

## Harness Version Reference

- **OpenClaw** — `v2026.6.1`
- **Hermes Agent** — `v2026.5.29.2`
- **OpenAI Codex** — `rust-v0.135.0`
- **Claude Code CLI** — `2.1.165` (npm latest) / `2.1.153` (npm stable)
- **Antigravity CLI** — Continuous delivery (launched 2026-05-19)
