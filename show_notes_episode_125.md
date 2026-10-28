# AgentStack Daily EP125 — Kimi K3.1 Pro brings 1M-token context to agent stacks

**Title:** Kimi K3.1 Pro Brings 1M-Token Context to OpenRouter

**Tagline:** OpenRouter’s listing of Kimi K3.1 Pro puts a 1M-token context window in the spotlight. Anthropic opens its agent sandbox beyond containers, while OpenAI launches a Decisions API for focused application decisions. Recursive’s Flint brings a 39.8B coding agent to local stacks, and Mistral’s Timestral-209M delivers local probabilistic forecasting. The feature lineup also includes Microsoft’s Agensh coordinating 1,024 agents, Cognition’s open-sourced vulnerability-fixing plugin, and research on reducing memory use during repeated inference.

**Feed description:** AgentStack Daily leads with Kimi K3.1 Pro, now listed by OpenRouter with a 1M-token context window. Anthropic’s expanded agent sandbox, OpenAI’s Decisions API, Recursive’s 39.8B Flint coding agent, and Mistral’s Timestral-209M forecasting model are also featured. The release readout covers Hermes Agent v0.22.5, v0.22.4, and v0.22.3, alongside AI-safety work, agent adaptation research, local code intelligence, and coordinated multi-agent systems.

---

## Story Slate

1. **Agent Stack Release Readout: Hermes Agent v0.22.5, v0.22.4, v0.22.3**
Hermes Agent v0.22.5, released by Nous Research on October 22, 2026, rolls 81 merged pull requests into a patch release spanning the CLI and installers, Microsoft Store app, Docker, and Hermes Cloud. Practical additions include account-aware sign-in, usage-window plan controls, pluggable delegation backends, plugin slash commands, agent importing, plugin-based MCP serving, and one-click Desktop plugin installs. The release also improves update recovery and Desktop group-chat status visibility.
Technical depth angle: The most useful mechanism is pluggable delegation: Hermes can route subagents through model maps or profiles, with that routing switchable per session. Plugins can provide slash commands that ask users to choose an option, while MCP serving and agent importing are also available through plugins. Together, these changes give builders clearer extension points for reusable agent workflows and specialized integrations.
Actionability angle: This release gives agent builders more direct ways to package integrations: delegation policies, selectable slash-command workflows, MCP serving, and imported-agent support now meet in the plugin system. Teams can also make sign-in and connector authentication clearer for end users, while plan controls expose usage limits and help recover when a windowed plan reaches its limit. The implications land across Antigravity, Codex, Claude Code, and Hermes stacks alike.
Listener hook: Hermes Agent can now turn delegation rules, MCP serving, and interactive commands into reusable plugins.

2. **OpenRouter lists Kimi K3.1 Pro with a 1M-token context window**
OpenRouter has listed Moonshot AI’s Kimi K3.1 Pro, an open-weight multimodal model described as a post-trained successor to Kimi K3. The registry entry gives it a 1,048,576-token context window and says it is built for long-horizon coding. It accepts text, images, and video, then produces text, making it a candidate for large codebases and mixed-media workflows.
Technical depth angle: The useful mechanism is a large multimodal context: Kimi K3.1 Pro can take text, image, and video as input and return text. Its registry listing specifies a 1,048,576-token context window, while listed per-token prices are $0.000002 for prompts, $0.00001 for completions, and $0.0000002 for cache reads.
Actionability angle: For builders, the listing creates a new option for evaluating long-running coding work and prompts that combine code with images or video. Its unusually large context and itemized token pricing are the practical details to weigh against workload size and cost.
Listener hook: A 1M-token model that can read code, images, and video is now available for evaluation through OpenRouter.

3. **Anthropic Opens Its Agent Sandbox Beyond Containers**
Anthropic has open-sourced sandbox-runtime, the operating-system-level sandbox used behind Claude Code. The tool restricts file and network access for AI agents, MCP servers, and command-line tools without requiring containers. It uses Seatbelt on macOS and bubblewrap on Linux, giving developers a way to limit what agent-driven code can reach while keeping the underlying tools available.
Technical depth angle: Sandbox-runtime applies operating-system isolation rather than container-based isolation. It uses macOS Seatbelt and Linux bubblewrap to restrict file and network access for agents, MCP servers—the services that connect agents to tools and data—and command-line tools. The project is open source and does not require containers.
Actionability angle: Builders can use sandbox-runtime to place agent-controlled tools within explicit file and network restrictions, which is useful when an agent runs code or invokes external commands. The release also gives teams an open-source reference for the sandboxing approach Anthropic uses behind Claude Code.
Listener hook: This gives agent builders a lighter-weight way to control what their software can touch.

4. **OpenAI launches a Decisions API for focused app decisions**
OpenAI has introduced the Decisions API, a new way for developers to add decision-making to applications. OpenAI positions it around three qualities: fast responses, focused results, and low operating cost. The product is aimed at applications across a broad range of use cases rather than a single category, making the API relevant to teams exploring a dedicated layer for automated choices. Builders will want to test how consistently it handles their own decision workloads and how those results translate into useful application behavior.
Technical depth angle: The useful mechanism is a dedicated API that returns decisions for application use. OpenAI describes the service as fast, focused, and low-cost, positioning it as a focused component for building applications that need to make automated choices rather than a general-purpose interface.
Actionability angle: This gives builders a concrete option to test when an application needs decisions without assembling that behavior around every request. The important questions in a trial are response speed, decision quality, and the cost of adding the API to real workflows.
Listener hook: OpenAI is packaging automated decision-making as a focused, cost-conscious API for application builders.

5. **Recursive’s Flint brings a 39.8B coding agent to local stacks**
Recursive has released Flint, a text-based mixture-of-experts model for coding agents, under the Apache 2.0 license. It has 39.8 billion total parameters, with approximately 2.5 billion active per token, and supports reasoning, multi-turn tool use, and OpenAI-compatible tool calls. Unsloth’s GGUF repository provides the checkpoint, configuration, tokenizer, chat template, and serving kit, while separately prepared quantized variants target NVIDIA and Apple Silicon runtimes. Recursive reports strong agentic evaluation results, though the model card warns that evaluation setups vary.
Technical depth angle: Flint activates only a subset of its experts for each token, using six of 256 routed experts per layer plus a shared expert. That helps explain its 39.8B-total, roughly 2.5B-active design. For agent builders, the more important mechanisms are multi-turn tool use, OpenAI-compatible tool calls, and a shared context window for prompts and generated output.
Actionability angle: Builders can use Flint inside a local coding-agent workflow that investigates repositories, proposes fixes, writes tests, and calls tools through a compatible interface. The repository points to quantized variants for NVIDIA and Apple Silicon, making it relevant to local inference. Evaluate the exact checkpoint and runtime you plan to deploy, because the publisher says results vary with precision and inference setup.
Listener hook: Flint gives local coding-agent builders a 39.8B model that activates only about 2.5B parameters per token while supporting multi-turn tools.

6. **Mistral’s Timestral-209M brings local probabilistic forecasting**
Mistral has released Timestral-209M, the largest checkpoint in its family of time-series foundation models for zero-shot forecasting. The model can forecast one or many related series, incorporate extra inputs known today or scheduled for the future, and return probabilities rather than a single prediction. It handles up to 32,768 historical steps, forecasts up to 1,024 steps per pass, and runs locally through PyTorch on a CPU or GPU. Mistral also says it is releasing the source code and reports leading zero-shot results on three forecasting benchmarks.
Technical depth angle: Timestral groups 32 time steps into patches, then uses separate attention for time and the different variables being forecast. Missing-value indicators travel with each patch. The result is a 209M-parameter model that supports probabilistic outputs across 21 quantiles, letting applications request both a median forecast and upper or lower bounds.
Actionability angle: This gives agent builders a practical forecasting component that can run locally and handle uncertainty instead of returning only one number. It is especially relevant for operational systems that need univariate or multivariate forecasts, scheduled inputs, or probability ranges without task-specific retraining.
Listener hook: A local forecasting model with uncertainty estimates could become a useful planning component for agents that act on changing conditions.

7. **OpenAI and Poland’s NASK team up on AI safety**
OpenAI and Poland’s NASK announced a partnership focused on AI safety, security, and technical research. The collaboration is intended to strengthen safeguards and support a more resilient digital ecosystem. This is a research-and-safeguards effort rather than a new AI product, but it gives Poland’s national cybersecurity institution a direct role in shaping how OpenAI approaches AI security. For builders, the next useful evidence will be concrete safeguards, security methods, or research results that emerge from the partnership.
Technical depth angle: The useful mechanism here is institutional collaboration: OpenAI is working with Poland’s NASK across AI safety, security, and technical research. That connects product development with a national cybersecurity organization and gives the partnership a practical focus on stronger safeguards and digital resilience.
Actionability angle: For teams working on AI security, the partnership creates a concrete institutional connection between OpenAI and Poland’s NASK. Its value will be judged by the safeguards, security methods, or research results that can eventually inform real-world AI deployments.
Listener hook: Poland’s national cybersecurity institution is now working directly with OpenAI on how AI systems should be secured.

8. **Research digest: METTA Lets Agents Adapt During the Task**
METTA, a memory-enhanced test-time adaptation method, helps an AI agent learn from experience while it is already attempting a new task. It updates within the current episode and preserves compact summaries across episodes, giving the agent a way to adapt to unfamiliar tasks without repeatedly processing its entire history. On long-context PointMaze tasks, it beat transformer-based baselines and showed more structured exploration.
Technical depth angle: METTA’s key finding is that an agent can adapt during an unseen task while carrying compact episode-level context into later attempts. It achieved effective adaptation on held-out tasks and more structured exploration than transformer-based baselines in long-context sparse-reward mazes, without the cost of attending over the full interaction history.
Actionability angle: For agent builders, METTA points toward systems that update from live interaction and retain compact cross-episode memory rather than replaying everything. That could make long-running agents more practical when each new task arrives with little training history, though benchmark results do not establish behavior in the wild.
Listener hook: This matters if your agent meets unfamiliar tasks and has to learn from limited interaction without reprocessing everything it has done.

9. **SpaceX Super Intelligence opens a Grok partner network**
SpaceX Super Intelligence has launched an official partner network for companies building products, integrations, and enterprise services with Grok. It has two tracks: Transformation Partners, which help organizations deploy Grok, and Marketplace Partners, which build plugins and product integrations. More than 130 companies joined the early-access phase, while engineers have been trained at over 30 organizations through a Forward Deployed Engineer accreditation program.
Technical depth angle: The program connects two implementation paths: trained engineers help customers put the Grok platform into production workflows, while marketplace partners connect Grok to existing tools. Launch partners described enterprise data, coding-agent integration, permissions, audit trails, and business-specific context as the practical areas partners will address together.
Actionability angle: The network creates routes for service firms, software vendors, and deployment specialists to package Grok alongside enterprise data, delivery, governance, and integration work. It may be particularly relevant to organizations seeking production deployments rather than isolated demonstrations.
Listener hook: More than 130 companies are already helping turn Grok into enterprise deployments and integrations.

10. **Research digest: A Training Trick Makes Repeated AI Inference Less Memory-Hungry**
Researchers introduced BeNice!, a post-training method that lets looped AI models reuse the same key-value cache across repeated passes through their layers. Looped models can improve quality without adding parameters, but separate caches for each pass caused inference memory to grow linearly. BeNice! closes that gap while matching the quality of standard fine-tuning with unshared caches.
Technical depth angle: A key-value cache stores information from earlier tokens so a model does not recompute it while generating later tokens. BeNice! trains a looped model so that one cache can be shared across repeated layer passes, rather than creating a separate cache for each pass. The method preserves model quality while addressing the memory growth caused by those duplicate caches.
Actionability angle: This could make looped architectures more practical for inference where memory is the limiting resource, especially when combined with other memory-efficient sequence methods. It also gives teams another approach to explore when they need repeated computation without a proportional increase in parameters.
Listener hook: The same layers can now be reused more than once without forcing the model to keep a separate memory cache for every pass.

11. **DeusData Brings Local Code Intelligence to AI Agents**
DeusData’s codebase-memory-mcp is a local code-intelligence project for developers and AI agents. It connects code, documentation, and infrastructure in a persistent graph, while adding CBM Lens, MCP tools, agent integrations, and change-aware test selection. The repository’s latest release is v0.12.1, dated October 16, 2026, and the project was pushed again on October 24. GitHub reports 47,438 stars, signaling strong developer interest. The practical opportunity is a shared context layer that can help agents work across a codebase and help teams focus testing on relevant changes.
Technical depth angle: The central mechanism is a persistent graph that connects code, documentation, and infrastructure. The project pairs that graph with CBM Lens, MCP tools for agent access, integrations, and change-aware test selection, which uses change information to identify tests worth running.
Actionability angle: Builders can use the project to give AI agents persistent context across code and documentation instead of relying on isolated prompts. Teams may also be able to reduce unnecessary test work by selecting tests around current changes.
Listener hook: This is a local-first way to give coding agents broader project context without sending the whole codebase to a separate service.

12. **Microsoft’s Agensh coordinates 1,024 agents without a central boss**
Microsoft Research has open-sourced Agensh, a multi-agent harness—a framework for coordinating multiple AI agents—for running as many as 1,024 agents on the ProgramBench benchmark without a central orchestrator. Its workers self-organize by sharing a Git repository, a chat channel, and a findings board. The reported experiment scales from one agent to 1,024 within a six-hour budget. Agensh gives builders an open-source way to explore large, cooperative agent workflows, while leaving a clear next question: how well does this coordination work outside ProgramBench?
Technical depth angle: Agensh replaces a central controller with self-organizing workers. Those workers coordinate through three shared resources: a Git repository for code, a chat channel for conversation, and a findings board for recorded results. The reported ProgramBench experiment spans one to 1,024 agents while staying within a six-hour budget.
Actionability angle: For builders, Agensh provides a concrete open-source framework for testing workflows that divide work among many cooperating agents. Its shared repository, chat, and findings board offer specific coordination points to examine when designing such systems.
Listener hook: A thousand agents can share one workspace and coordinate without a central controller deciding every move.

13. **Cognition Open-Sources a Vulnerability-Fixing Agent Plugin**
Cognition released the Devin Vulnerability Fixes plugin, a set of three MIT-licensed agent skills for responding to critical remote-code-execution flaws in PHP, Node.js and self-managed GitLab deployments. The plugin inventories affected systems, patches and tests them, then opens one pull request per repository. That gives engineering teams a concrete way to turn a vulnerability alert into reviewable remediation work instead of manually searching every repository.
Technical depth angle: The plugin contains three MIT-licensed agent skills covering PHP, Node.js and self-managed GitLab deployments. For each affected repository, its workflow covers vulnerability discovery, patching and testing before creating one pull request, making the proposed fix reviewable through the team’s normal code workflow.
Actionability angle: Teams can use the plugin to accelerate remediation of the newly disclosed flaws across multiple repositories. The one pull request per repository makes it easier to review each proposed fix before deployment, so the results still need normal engineering scrutiny.
Listener hook: An open-source agent can now start with the vulnerable repositories, propose fixes and prepare pull requests for review.

14. **Letta Tutorial Builds Stateful Engineering Copilots**
MarkTechPost published a guide to building a stateful engineering copilot with Letta. The tutorial shows how an assistant can retain inspectable core memory, retrieve older information through semantic search, share state across multiple agents, call custom tools, stream responses, and move its workflow between environments. That gives builders a concrete path beyond assistants that rely only on the current prompt and conversation.
Technical depth angle: The key mechanism is persistent, inspectable core memory. The copilot can also search archived information by meaning rather than exact wording, while shared state lets multiple agents coordinate on the same engineering context. Custom tools connect that context to outside actions, and portable workflows make the resulting setup easier to reuse.
Actionability angle: This gives builders a practical pattern for coding assistants that must remember project context, coordinate specialized agents, and use domain-specific tools. The important shift is from one-shot prompting toward workflows whose memory and state remain visible and reusable.
Listener hook: This tutorial shows how to turn a coding assistant into a copilot that remembers, collaborates, and carries its workflow forward.

---

## Editorial Mix Check

- flagship_products: 5
- builder_projects: 8
- local_ai: 2
- hardware_compute: 2
- policy_regulation: 1
- research: 2

---

## Model Discovery Check

- **MoonshotAI: Kimi K3.1 Pro** (moonshotai) — Newly listed this cycle (verified October 25, 2026). Primary source: https://openrouter.ai/models/moonshotai/kimi-k3.1-pro. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 1048576 tokens; modality: text+image+video->text. Capabilities: context length 1048576; Kimi K3.1 Pro is Moonshot AI's flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3, with a 1M-token context window. It is built for long-horizon coding, 3D.... Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/moonshotai/kimi-k3.1-pro and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **flint** — Source checked October 25, 2026. Primary source: https://huggingface.co/unsloth/flint-GGUF. Availability: The Apache 2.0 weights are available through Unsloth’s GGUF repository, with quantized variants prepared for NVIDIA and Apple Silicon runtimes.. params_active: n/a; params_total: n/a; context: n/a; modality: see primary source. Capabilities: Flint is a text-based coding-agent model that supports reasoning, multi-turn tool use, and OpenAI-compatible tool calls. Evidence: publisher_report. Decision: Selected — covered in the numbered slate from a non-OpenRouter source.

- **Timestral-209M** — Source checked October 25, 2026. Primary source: https://huggingface.co/mistralai/Timestral-209M. Availability: The checkpoint runs through PyTorch on a CPU or GPU, and the models are released under a Modified MIT license.. params_active: n/a; params_total: n/a; context: n/a; modality: see primary source. Capabilities: Timestral supports univariate and multivariate forecasting, past-only and known-future covariates, and probabilistic predictions across 21 quantiles. Evidence: publisher_report. Decision: Selected — covered in the numbered slate from a non-OpenRouter source.

---

## Local LLM Spotlight

- **deepseek-ai/DeepSeek-V4.1-Flash-1017** — https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017 — Trending open model on Hugging Face; task image-text-to-text; 2856 likes and 85275 downloads. Tags: transformers, safetensors, deepseek_v41, text-generation, image-text-to-text, license:mit, eval-results, endpoints_compatible, 8-bit, fp8.
  Try now: Read the linked model card before downloading, and choose a runtime or device only after it confirms the license, weight format, context window, benchmarks, and hardware requirements.

---

## GitHub Project Radar

- **HKUDS/nanobot** — https://github.com/HKUDS/nanobot — HKUDS/nanobot is an ultra-lightweight, open-source, self-hosted personal AI agent framework written in Python. It includes a WebUI, tools, memory, MCP, multi-agent workflows, automation, and chat apps. `stars: 49,339`; `stars_delta_30d: +778 (+1.6%) since 2026-09-25`; `latest_release: v0.3.5 (2026-09-15)`.
  Why this is on the radar now: v0.3.5 shipped on 2026-09-15 and the repository was updated on 2026-10-25.
  Stack improvement angle: Nanobot could give an OpenClaw, Codex, Claude Code, or Hermes stack a self-hosted agent layer with persistent memory, MCP access, and multi-agent workflow orchestration.
  Try now: Start by deploying the WebUI and connecting one tool or MCP server through the framework.

- **ahujasid/mcp-for-blender** — https://github.com/ahujasid/mcp-for-blender — ahujasid/mcp-for-blender is a community plugin for controlling Blender with any LLM of your choice. It is not affiliated with the official Blender Foundation. `stars: 32,293`; `stars_delta_30d: +2,978 (+10.2%) since 2026-09-25`; `latest_release: none published on GitHub as of 2026-10-25`.
  Why this is on the radar now: The repository was updated on 2026-10-24 and enters the radar with 32,293 stars.
  Stack improvement angle: The plugin could extend an agent stack with a Blender control plane, letting Codex, Claude Code, Hermes, or OpenClaw orchestrate 3D-scene operations through an LLM.
  Try now: Install the plugin in Blender and test a basic scene operation with your preferred LLM.

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — PrefectHQ/fastmcp is a Pythonic framework for building MCP servers and clients. It provides a direct way to expose tools and data to agent applications. `stars: 28,197`; `stars_delta_30d: +680 (+2.5%) since 2026-09-04`; `latest_release: v4.1.3 (2026-10-20)`.
  Why this is on the radar now: v4.1.3 shipped on 2026-10-20 and the repository was updated on 2026-10-25.
  Stack improvement angle: FastMCP could simplify the MCP integration layer around OpenClaw, Codex, Claude Code, or Hermes by making tool servers and client connections easier to implement.
  Try now: Build a minimal FastMCP server that exposes one tool and connect it to an MCP-compatible client.

---

## Extra Research Candidates

- **Usage metrics API adds usage from tools like OpenCode** — https://github.blog/changelog/2026-10-23-usage-metrics-api-adds-usage-from-tools-like-opencode — The Copilot usage metrics API now reports model usage from more of the tools your developers use with Copilot, including tools like OpenCode that weren&#8217;t previously captured in your reports.&#8230; The post Usage metrics API adds usag Technical depth angle: The Copilot usage metrics API now captures model usage from additional developer tools, including OpenCode, and includes it in the usage reports.

- **Microsoft Open-Sources Agensh: A Multi-Agent Harness for 1,024 Agents** — https://www.marktechpost.com/2026/10/24/microsoft-agensh-multi-agent-harness-1024-agents/ — Microsoft Research open-sourced Agensh, a multi-agent harness with no central orchestrator. Self-organizing workers share a Git repo, chat and a findings board, scaling from 1 to 1,024 agents on ProgramBench under a 6-hour budget. The post  Technical depth angle: Agensh uses self-organizing workers without a central orchestrator, coordinating through a shared Git repository, chat, and findings board while scaling across 1 to 1,024 agents on ProgramBench within a six-hour budget.

- **Google Cloud Launches Agent Compute Engine: A MicroVM per AI Agent** — https://www.marktechpost.com/2026/10/22/google-cloud-agent-compute-engine-microvm-ai-agents/ — Google Cloud announced Agent Compute Engine, a compute service that gives every AI agent its own hardware-isolated microVM with no credentials inside. It already runs Gemini agents and enters preview in the coming months. The post Google Cl Technical depth angle: Agent Compute Engine assigns each agent a hardware-isolated microVM that contains no credentials.

---

## Show Notes

```md
Episode 125 — October 25, 2026

[00:00] Episode hook

Nous Research released Hermes Agent v0.22.5 on October 22, 2026, packaging 81 merged pull requests into a patch release across the CLI and installers, the Microsoft Store app, Docker, and Hermes Cloud. Anthropic also open-sourced sandbox-runtime, the operating-system-level sandbox behind Claude Code, which restricts file and network access for AI agents, MCP servers, and command-line tools. OpenRouter added Moonshot AI’s Kimi K3.1 Pro with a 1,048,576-token context window, while OpenAI introduced a Decisions API for adding decision-making to applications with an emphasis on fast responses and focused results. Recursive followed with Flint, an Apache 2.0-licensed text-based mixture-of-experts coding model with 39.8 billion total parameters and approximately 2.5 billion active per token. Mistral released Timestral-209M, a time-series foundation model for zero-shot forecasting that can handle one or many related series and incorporate external information.

[02:00] Agent Stack Release Readout: Hermes Agent v0.22.5, v0.22.4, v0.22.3

Hermes Agent v0.22.5, shipped by Nous Research on October 22, 2026, combines 81 merged pull requests and 30 closed issues across 231 non-merge commits and 804 changed files. It updates the CLI and installers, Microsoft Store app, Docker, and Hermes Cloud.

The most consequential change is pluggable delegation. Hermes can route work to subagents using model maps or profiles, and the selected routing can change for each session. That gives builders a way to separate different models or profiles by task without treating every backend as part of the core application.

The plugin system also becomes more capable. Plugins can expose slash commands with selectable options, serve Hermes through the Model Context Protocol, and import existing agents. The setup flow can offer an importer when it detects another agent, while Desktop gains one-click plugin installation, tier badges, and drag-to-pin controls in its sidebar.

Account and session handling are clearer too. Sign-in now uses plain device login, free-tier guests can hand their work to an account, and the result shows who is signed in. Connectors offer sign-in rather than silently opening a guest session. Usage-window plans gain gauges, limit cards, and model-switch recovery.

Hermes Agent v0.23.0 is the next milestone to watch because Nous Research says it will contain the full curated notes for the accumulated changes in these releases.

[02:35] OpenRouter lists Kimi K3.1 Pro with a 1M-token context window

OpenRouter has listed Kimi K3.1 Pro, which the registry describes as Moonshot AI’s flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3. It is built for long-horizon coding, giving it a particular potential fit for extended software work and large codebases. Its most concrete feature is a 1,048,576-token context window. The registry architecture says the model accepts text, images, and video and produces text, so developers can bring different kinds of material into the same prompt. That is relevant for workflows where code, screenshots, and video need to inform one result. OpenRouter’s registry lists per-token pricing of $0.000002 for prompts, $0.00001 for completions, and $0.0000002 for cached input reads. The listing makes Kimi K3.1 Pro available for evaluation through OpenRouter, with context size, multimodal input, and token cost as the immediate points to assess. Moonshot AI describes Kimi K3.1 Pro as a post-trained successor to Kimi K3. Kimi K3.1 Pro accepts text, images, and video, produces text, and has a 1M-token context window. OpenRouter lists Kimi K3.1 Pro on its model registry.

[03:42] Anthropic Opens Its Agent Sandbox Beyond Containers

Anthropic has released sandbox-runtime, or srt, as an open-source operating-system-level sandbox for AI agents. The project is the sandbox behind Claude Code and supports agents, MCP servers, and command-line tools without requiring containers.

Its core job is straightforward: restrict the file and network access available to those tools. On macOS, it uses Seatbelt, the operating system’s own sandboxing mechanism; on Linux, it uses bubblewrap. The same approach is therefore available across two major desktop and server environments without making developers containerize each agent or tool.

For builders, this changes the implementation choice around running agent-driven code. Instead of reaching for a container, a developer can place an agent, a tool server, or a command-line utility inside an OS-level sandbox with controlled access to files and networks. Anthropic is also making the sandboxing approach used behind Claude Code available for inspection and reuse.

The next thing to watch is how developers combine these access restrictions with the specific tools and data their agents need in real workflows.

[04:44] OpenAI launches a Decisions API for focused app decisions

OpenAI has launched the Decisions API, giving application builders a dedicated interface for automated choices. The company describes it as fast, focused, and low-cost, with applicability across different kinds of applications rather than one narrow use case.

That matters because many products need a small decision at a specific moment: which option to present, how to route a request, or what action an application should take. The API gives teams another component to test for those moments instead of treating every decision as part of a broader workflow.

For builders, the next proof points are practical: how quickly the API responds, whether its decisions remain consistent on real workloads, and what those decisions cost when incorporated into a live product.

[05:29] Recursive’s Flint brings a 39.8B coding agent to local stacks

Recursive released Flint under the Apache 2.0 license, and Unsloth’s repository provides its checkpoint, model configuration, tokenizer, chat template, and serving kit. Flint is a text-in, text-out mixture-of-experts model designed for coding agents. It has 39.8 billion total parameters, with approximately 2.5 billion active per token. Each mixture-of-experts layer contains 256 routed experts, six selected per token, plus an always-active shared expert. Flint supports reasoning, multi-turn tool use, and OpenAI-compatible tool calls, with tasks that include investigating codebases, fixing bugs, implementing features, and writing tests. Recursive reports 54.9% on Terminal-Bench 2.1, 89.7% on SWE-bench Pro v2, and 74.2% on SWE-bench Verified. The card cautions that evaluation setups vary, and Flint’s Terminal-Bench result counts solutions obtained through web retrieval as unsuccessful while some developer-reported scores may not apply that adjustment. The Apache 2.0 weights are available through Unsloth’s GGUF repository, with quantized variants prepared for NVIDIA and Apple Silicon runtimes. Results can vary with checkpoint precision and inference runtime, so the specific deployment configuration matters. Flint can still produce faulty code or inappropriate tool calls, so applications need their own permissions and execution boundaries. Flint is a text-based coding-agent model that supports reasoning, multi-turn tool use, and OpenAI-compatible tool calls.

[06:45] Mistral’s Timestral-209M brings local probabilistic forecasting

Mistral has released Timestral-209M, a time-series foundation model for forecasting without task-specific retraining. It is the largest of four documented sizes, ranging from 5M to 209M parameters, and the publisher says its zero-shot forecasting results lead on GIFT-Eval, TIME, and fev-bench. The model can forecast a single series or several related series. It also accepts extra inputs that are either already known or scheduled for the future, which can help an application incorporate context beyond the target history. Its probabilistic output spans 21 quantiles, so software can request a median forecast alongside lower and upper bounds rather than treating one prediction as certainty. Timestral accepts up to 32,768 historical time steps and forecasts up to 1,024 steps in one pass. Longer forecasts proceed in blocks. Internally, it groups 32 steps into each patch and embeds both the values and indicators for missing observations. For builders, the important change is local deployment through PyTorch on either a CPU or GPU. Mistral also says it is releasing the source code for running the model and reproducing its benchmark results. That makes Timestral a candidate forecasting component for local services and agent stacks that need probability ranges, future horizons, or several related signals rather than a single point estimate. Mistral released the Timestral-209M checkpoint and said it was releasing the source code. Timestral supports univariate and multivariate forecasting, past-only and known-future covariates, and probabilistic predictions across 21 quantiles. The publisher reports that on GIFT-Eval, Timestral-209M posted lower MASE and CRPS errors than TimesFM-3. The checkpoint runs through PyTorch on a CPU or GPU, and the models are released under a Modified MIT license.

[08:26] OpenAI and Poland’s NASK team up on AI safety

OpenAI and Poland’s NASK announced a partnership on October 23, 2026, covering AI safety, security, and technical research. Poland’s NASK is joining forces with OpenAI to strengthen safeguards and support a more resilient digital ecosystem.

This is not a product launch; it is a collaboration between an AI company and Poland’s national cybersecurity institution. Its immediate significance is institutional: AI safety and security research now connects directly with an organization focused on the security of Poland’s digital infrastructure.

For AI builders, the useful signal to watch is whether the partnership produces concrete safeguards, security methods, or technical research that teams can apply when protecting real systems.

[09:06] Research digest: METTA Lets Agents Adapt During the Task

METTA, a memory-enhanced adaptation method, helps an AI agent learn while it is already trying a task, rather than relying only on lessons learned before the task starts. That matters for systems that must handle unfamiliar jobs with limited experience: they can update their behavior from recent interaction and carry a compact summary of earlier episodes into the next attempt. The researchers tested the approach on unseen Meta-World tasks and long-context PointMaze tasks, where reward was rare. In the held-out Meta-World environments, METTA exceeded a 50% success rate while keeping training costs and wall-clock time low. On the maze tasks, it beat transformer-based baselines and showed more structured exploration. The practical consequence is that an agent can adapt with a low training budget while retaining enough history to guide later attempts, instead of rebuilding its understanding from scratch each time. The next question is whether that balance between learning during a task and remembering across tasks holds up outside benchmark environments.

[10:07] SpaceX Super Intelligence opens a Grok partner network

SpaceX Super Intelligence has introduced an official program for companies building products, solutions, and services with Grok for joint prospects and customers. The SpaceX Super Intelligence Partner Network separates that work into Transformation Partners, which help customers deploy the Grok platform across the enterprise, and Marketplace Partners, which build plugins and integrations that connect Grok to tools customers already use.

More than 130 companies participated in the early-access phase. Transformation Partners are building deployment capacity through a Forward Deployed Engineer accreditation program, with engineers trained at more than 30 organizations. Marketplace Partners are working on product integrations for the Grok suite.

Launch partners include Bain & Company, Databricks, NVIDIA, Snowflake, Galatiq, Adapter Group, AHEAD, and Alpha FMC. Their stated roles range from enterprise transformation and delivery to data platforms, governance, audit trails, and business-specific context. Galatiq, for example, describes a delivery model in which engineers scope and build production systems inside client workflows. Adapter describes bringing a customer’s full trajectory into Grok Bot and Grok Build so each turn starts from broader mission context rather than working memory alone.

For builders, the practical opening is joint work that reaches deployment, integrations, enterprise data, and operational controls. The next proof point is how broadly those partnerships move from pilots into recurring production use.

[11:27] Research digest: A Training Trick Makes Repeated AI Inference Less Memory-Hungry

A new post-training method called BeNice! helps a class of AI models that repeatedly pass information through the same layers while keeping the number of learned parameters fixed. During inference, each pass previously created its own key-value cache—stored information from earlier tokens—causing memory use to grow linearly with the number of repetitions. BeNice! trains the model so that the final pass’s cache can be broadcast into the first pass, making the repeated passes compatible with a shared cache. The researchers report that this preserves the model’s quality, matching standard fine-tuning with separate caches. The result matters because looped architectures can improve quality without simply adding more parameters, but their inference memory demand has limited that advantage. BeNice! offers a way to retain the quality benefit while avoiding duplicate caches across depth. The researchers also found that the approach can complement other memory-saving sequence methods, suggesting that teams could combine it with existing compression techniques when memory efficiency matters most.

[12:27] DeusData Brings Local Code Intelligence to AI Agents

DeusData shipped codebase-memory-mcp, a local code-intelligence project for developers and AI agents. Its latest release is v0.12.1, dated October 16, 2026, and the repository was pushed again on October 24. GitHub reports 47,438 stars for the project.

The repository connects code, documentation, and infrastructure in a persistent graph. It also includes CBM Lens, MCP tools, agent integrations, and change-aware test selection. Together, these pieces are aimed at helping developers and AI agents work with a codebase as a connected body of information rather than as isolated files or prompts.

For builders, the most useful opportunity is a local context layer that can support agent workflows across code and docs. The test-selection feature could also help teams spend less effort running tests unrelated to a change. One thing to watch next is how effectively the agent integrations and change-aware selection work on real projects.

[13:21] Microsoft’s Agensh coordinates 1,024 agents without a central boss

Microsoft Research has open-sourced Agensh, a multi-agent harness that runs as many as 1,024 agents on ProgramBench without a central orchestrator, or single controller assigning the work.

The useful mechanism is shared coordination. Workers self-organize while communicating through a shared Git repository, a chat channel, and a findings board. In the reported experiment, Agensh scaled from one agent to 1,024 while remaining within a six-hour budget on ProgramBench.

That gives builders an open-source framework for exploring large, cooperative agent teams and studying how they coordinate through shared code, conversation, and recorded findings. The headline number is striking, but the shared workspace and communication channels are the concrete pieces teams can adapt.

The next question is how the approach behaves on tasks beyond ProgramBench and under workloads that differ from the reported benchmark.

[14:11] Cognition Open-Sources a Vulnerability-Fixing Agent Plugin

Cognition has open-sourced the Devin Vulnerability Fixes plugin to help teams respond to this week’s critical remote-code-execution flaws in PHP, Node.js and self-managed GitLab deployments.

The release includes three MIT-licensed agent skills. They inventory affected systems, patch and test them, and then open one pull request for each repository. That turns a broad vulnerability response into separate, reviewable changes rather than leaving teams to discover and fix every affected repository by hand.

The key detail to watch is whether the generated pull requests are ready for normal engineering review after the plugin has completed its inventory, patching and testing work.

[14:49] Letta Tutorial Builds Stateful Engineering Copilots

MarkTechPost has published a hands-on guide to building a stateful engineering copilot with Letta. The goal is to extend an AI assistant beyond the information in its immediate prompt so it can work with persistent context and reusable project knowledge.

At the center is inspectable core memory, which provides a visible place for the copilot to retain information. The tutorial also demonstrates archival vector retrieval: a way to find older material according to its meaning rather than requiring an exact wording match.

For more complex work, the copilot can use custom tools and share state with multiple agents, letting specialized agents coordinate around the same context. It also supports streaming responses and portable workflows that can move between environments.

For builders, the useful result is a concrete architecture for an engineering assistant that can retain project context, retrieve relevant information, connect to specialized actions, and preserve a reusable workflow instead of starting fresh in every session.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: Hermes Agent v0.22.5, v0.22.4, v0.22.3 / OpenRouter lists Kimi K3.1 Pro with a 1M-token context window / Anthropic Opens Its Agent Sandbox Beyond Containers
- 02:00 — Agent Stack Release Readout: Hermes Agent v0.22.5, v0.22.4, v0.22.3
- 02:35 — OpenRouter lists Kimi K3.1 Pro with a 1M-token context window
- 03:42 — Anthropic Opens Its Agent Sandbox Beyond Containers
- 04:44 — OpenAI launches a Decisions API for focused app decisions
- 05:29 — Recursive’s Flint brings a 39.8B coding agent to local stacks
- 06:45 — Mistral’s Timestral-209M brings local probabilistic forecasting
- 08:26 — OpenAI and Poland’s NASK team up on AI safety
- 09:06 — Research digest: METTA Lets Agents Adapt During the Task
- 10:07 — SpaceX Super Intelligence opens a Grok partner network
- 11:27 — Research digest: A Training Trick Makes Repeated AI Inference Less Memory-Hungry
- 12:27 — DeusData Brings Local Code Intelligence to AI Agents
- 13:21 — Microsoft’s Agensh coordinates 1,024 agents without a central boss
- 14:11 — Cognition Open-Sources a Vulnerability-Fixing Agent Plugin
- 14:49 — Letta Tutorial Builds Stateful Engineering Copilots

---

## Primary Links

- Hermes Agent v0.22.5 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.5
- Hermes Agent v0.22.4 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.4
- Hermes Agent v0.22.3 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.3
- MoonshotAI: Kimi K3.1 Pro model page: https://openrouter.ai/models/moonshotai/kimi-k3.1-pro
- Meet Anthropic’s sandbox-runtime: OS-Level Sandboxing for AI Agents, N: https://www.marktechpost.com/2026/10/24/anthropic-sandbox-runtime-ai-agent-sandbox/
- Build more responsive apps with the Decisions API: https://openai.com/index/decisions-api
- unsloth/flint-GGUF model repository on Hugging Face: https://huggingface.co/unsloth/flint-GGUF
- mistralai/Timestral-209M model repository on Hugging Face: https://huggingface.co/mistralai/Timestral-209M
- OpenAI and Poland’s NASK partner to advance AI safety and security: https://openai.com/index/openai-nask-ai-safety-security-partnership
- METTA: Memory-Enhanced Test-Time Adaptation for Meta-Reinforcement Lea: https://arxiv.org/abs/2610.31656
- Introducing the SpaceX Super Intelligence Partner Network: https://x.ai/news/partnernetworkannouncement
- BeNice! Closing Looping's Inference-Memory Gap via KV-Sharing: https://arxiv.org/abs/2610.31633
- Securing our frontier model training environment: https://openai.com/index/securing-our-frontier-model-training-environment
- DeusData/codebase-memory-mcp — Local code intelligence for developers : https://github.com/DeusData/codebase-memory-mcp
- Microsoft Open-Sources Agensh: A Multi-Agent Harness for 1,024 Agents: https://www.marktechpost.com/2026/10/24/microsoft-agensh-multi-agent-harness-1024-agents/
- Cognition Open-Sources an Agent Plugin that Helps Secure Systems again: https://www.marktechpost.com/2026/10/24/cognition-devin-vulnerability-fixes-plugin-php2shell-nodejs-gitlab/
- Stateful Agentic Engineering Copilots with Letta: Core Memory, Shared : https://www.marktechpost.com/2026/10/24/stateful-engineering-copilots-letta-tutorial/
- HKUDS/nanobot repo: https://github.com/HKUDS/nanobot
- ahujasid/mcp-for-blender repo: https://github.com/ahujasid/mcp-for-blender
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- Usage metrics API adds usage from tools like OpenCode: https://github.blog/changelog/2026-10-23-usage-metrics-api-adds-usage-from-tools-like-opencode
- Google Cloud Launches Agent Compute Engine: A MicroVM per AI Agent: https://www.marktechpost.com/2026/10/22/google-cloud-agent-compute-engine-microvm-ai-agents/
- deepseek-ai/DeepSeek-V4.1-Flash-1017: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017

---

## Release Coverage Check

- **Hermes Agent** — Latest stable verified: `v0.22.5`, published 2026-10-23T05:28:45Z. Recent episode version tags detected: `v2026.9.14`, `v2026.9.21`, `v2026.9.24`, `v2026.9.7`. Selected missing version(s): `v0.22.5`, `v0.22.4`, `v0.22.3`.
- **OpenAI Codex** — Latest stable verified: `rust-v0.164.0`, published 2026-10-23T04:48:10Z. Recent episode version tags detected: `rust-v0.160.0`, `rust-v0.161.0`, `rust-v0.162.0`, `rust-v0.163.0`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.308`, published 2026-10-22T04:19:48.902Z. Recent episode version tags detected: `2.1.292`, `2.1.304`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-10-25). Recent episode version tags detected: `@google/antigravity`, `v2.0`.

---

## Harness Version Reference

- **Hermes Agent** — `v0.22.5`
- **OpenAI Codex** — `rust-v0.164.0`
- **Claude Code CLI** — `2.1.308`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)


---

## Featured Story Plan

- Story 5: **Recursive’s Flint brings a 39.8B coding agent to local stacks** — prioritize its source-backed capability, comparison when documented, limitations, and practical consequence; no word quota.
- Story 6: **Mistral’s Timestral-209M brings local probabilistic forecasting** — prioritize its source-backed capability, comparison when documented, limitations, and practical consequence; no word quota.

---

## Research Evidence Contract

```json
{
  "policy_version": 1,
  "featured_stories": [
    6,
    5
  ],
  "records": [
    {
      "story": 1,
      "title": "Agent Stack Release Readout: Hermes Agent v0.22.5, v0.22.4, v0.22.3",
      "source_sha256": "4bb45dbcb6be2c5cd5ec7a768e74a0d726c7c76be57acf9e1ae202c9c0686307",
      "source_url": "https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.5",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 2,
      "title": "OpenRouter lists Kimi K3.1 Pro with a 1M-token context window",
      "source_sha256": "7b8be483e7e30d5eda6b491481914efeb1631ebd432e84b5e6b4bc9f0c2270c5",
      "source_url": "https://openrouter.ai/models/moonshotai/kimi-k3.1-pro",
      "model_story": true,
      "model_review": {
        "release_status": "registry_listing",
        "evidence_type": "registry_listing",
        "release_quote": "This model is listed by OpenRouter at https://openrouter.ai/models/moonshotai/kimi-k3.1-pro.",
        "release_span": "S003",
        "change": {
          "status": "supported",
          "claim": "Moonshot AI describes Kimi K3.1 Pro as a post-trained successor to Kimi K3.",
          "quote": "Kimi K3.1 Pro is Moonshot AI's flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3, with a 1M-token context window.",
          "source_span": [
            "S001"
          ],
          "quotes": [
            "Kimi K3.1 Pro is Moonshot AI's flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3, with a 1M-token context window."
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "Kimi K3.1 Pro accepts text, images, and video, produces text, and has a 1M-token context window.",
          "quote": "Kimi K3.1 Pro is Moonshot AI's flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3, with a 1M-token context window.\nContext length: 1048576 tokens.\nRegistry architecture: {\"modality\": \"text+image+video->text\", \"input_modalities\": [\"text\", \"image\", \"video\"], \"output_modalities\": [\"text\"], \"tokenizer\": \"Other\", \"instruct_type\": null}\nRegistry pricing per token in USD: {\"prompt\": \"0.000002\", \"completion\": \"0.00001\", \"input_cache_read\": \"0.0000002\"}",
          "source_span": [
            "S001",
            "S004",
            "S005"
          ],
          "quotes": [
            "Kimi K3.1 Pro is Moonshot AI's flagship open-weight multimodal reasoning model and a post-trained successor to Kimi K3, with a 1M-token context window.",
            "Context length: 1048576 tokens.",
            "Registry architecture: {\"modality\": \"text+image+video->text\", \"input_modalities\": [\"text\", \"image\", \"video\"], \"output_modalities\": [\"text\"], \"tokenizer\": \"Other\", \"instruct_type\": null}\nRegistry pricing per token in USD: {\"prompt\": \"0.000002\", \"completion\": \"0.00001\", \"input_cache_read\": \"0.0000002\"}"
          ]
        },
        "comparison": {
          "status": "unverified",
          "claim": "",
          "quote": "",
          "source_span": []
        },
        "limitations": {
          "status": "unverified",
          "claim": "",
          "quote": "",
          "source_span": []
        },
        "access": {
          "status": "supported",
          "claim": "OpenRouter lists Kimi K3.1 Pro on its model registry.",
          "quote": "This model is listed by OpenRouter at https://openrouter.ai/models/moonshotai/kimi-k3.1-pro.",
          "source_span": [
            "S003"
          ],
          "quotes": [
            "This model is listed by OpenRouter at https://openrouter.ai/models/moonshotai/kimi-k3.1-pro."
          ]
        }
      }
    },
    {
      "story": 3,
      "title": "Anthropic Opens Its Agent Sandbox Beyond Containers",
      "source_sha256": "2070c0b6b4aa9ce1f8aec1439e9295d7a3f71dea1901188f2f4cda9438699f07",
      "source_url": "https://www.marktechpost.com/2026/10/24/anthropic-sandbox-runtime-ai-agent-sandbox/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 4,
      "title": "OpenAI launches a Decisions API for focused app decisions",
      "source_sha256": "6abc0191af3ba48dde13ec3795c8732f486905a7c01b8f688de3b293a2fe39eb",
      "source_url": "https://openai.com/index/decisions-api",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 5,
      "title": "Recursive’s Flint brings a 39.8B coding agent to local stacks",
      "source_sha256": "f68a6cfec36179c0f1c8c241b19f38fbe29a63575ed865a5fa3c565750b1878b",
      "source_url": "https://huggingface.co/unsloth/flint-GGUF",
      "model_story": true,
      "model_review": {
        "release_status": "released",
        "evidence_type": "publisher_report",
        "release_quote": "Flint is released under the Apache 2.0 license.",
        "release_span": "S036",
        "change": {
          "status": "supported",
          "claim": "Recursive released Flint under the Apache 2.0 license, and Unsloth’s repository provides its checkpoint, model configuration, tokenizer, chat template, and serving kit.",
          "quote": "This repository contains the BF16 checkpoint, model configuration, tokenizer, chat template, and an SGLang serving kit.\nFlint is released under the Apache 2.0 license.",
          "source_span": [
            "S010",
            "S036"
          ],
          "quotes": [
            "This repository contains the BF16 checkpoint, model configuration, tokenizer, chat template, and an SGLang serving kit.",
            "Flint is released under the Apache 2.0 license."
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "Flint is a text-based coding-agent model that supports reasoning, multi-turn tool use, and OpenAI-compatible tool calls.",
          "quote": "Flint is Recursive’s mixture-of-experts language model for coding agents, with 39.8 billion total parameters and approximately 2.5 billion active per token.\nFlint supports text input and output, reasoning, and multi-turn tool use.\nFlint supports OpenAI-compatible tool calls.",
          "source_span": [
            "S006",
            "S008",
            "S024"
          ],
          "quotes": [
            "Flint is Recursive’s mixture-of-experts language model for coding agents, with 39.8 billion total parameters and approximately 2.5 billion active per token.",
            "Flint supports text input and output, reasoning, and multi-turn tool use.",
            "Flint supports OpenAI-compatible tool calls."
          ]
        },
        "comparison": {
          "status": "unverified",
          "claim": "",
          "quote": "",
          "source_span": []
        },
        "limitations": {
          "status": "supported",
          "claim": "Flint can still produce faulty code or inappropriate tool calls, so applications need their own permissions and execution boundaries.",
          "quote": "Flint’s supervised fine-tuning included safety-oriented examples, but the model can still produce incorrect or harmful content, faulty code, or inappropriate tool calls.\nTool-using applications should enforce their own permissions and execution boundaries; structured tool-call grammar does not prevent the model from choosing an unsafe or incorrect action.",
          "source_span": [
            "S030",
            "S032"
          ],
          "quotes": [
            "Flint’s supervised fine-tuning included safety-oriented examples, but the model can still produce incorrect or harmful content, faulty code, or inappropriate tool calls.",
            "Tool-using applications should enforce their own permissions and execution boundaries; structured tool-call grammar does not prevent the model from choosing an unsafe or incorrect action."
          ]
        },
        "access": {
          "status": "supported",
          "claim": "The Apache 2.0 weights are available through Unsloth’s GGUF repository, with quantized variants prepared for NVIDIA and Apple Silicon runtimes.",
          "quote": "---\nlicense: apache-2.0\npipeline_tag: text-generation\nbase_model:\nRecursiveSI/flint\ntags:\nflint\nunsloth\n---\nRead our How to Run Flint Guide!\nQuantized variants are prepared separately for NVIDIA and Apple Silicon runtimes.\nFlint is released under the Apache 2.0 license.",
          "source_span": [
            "S001",
            "S011",
            "S036"
          ],
          "quotes": [
            "---\nlicense: apache-2.0\npipeline_tag: text-generation\nbase_model:\nRecursiveSI/flint\ntags:\nflint\nunsloth\n---\nRead our How to Run Flint Guide!",
            "Quantized variants are prepared separately for NVIDIA and Apple Silicon runtimes.",
            "Flint is released under the Apache 2.0 license."
          ]
        }
      }
    },
    {
      "story": 6,
      "title": "Mistral’s Timestral-209M brings local probabilistic forecasting",
      "source_sha256": "78136f38bcfcf3ed596195a2c014f2742d9d0fa9e79982d0c94b70abdd24299d",
      "source_url": "https://huggingface.co/mistralai/Timestral-209M",
      "model_story": true,
      "model_review": {
        "release_status": "released",
        "evidence_type": "publisher_report",
        "release_quote": "Models have been released under a Modified MIT license: See here.",
        "release_span": "S033",
        "change": {
          "status": "supported",
          "claim": "Mistral released the Timestral-209M checkpoint and said it was releasing the source code.",
          "quote": "Timestral is a family of time series foundation models for zero-shot forecasting, available in 5M, 28M, 123M, and 209M parameter versions.\nThis repository contains the 209M checkpoint.\nWe’re releasing the source code in our GitHub repository to make it easy to run Timestral and reproduce our benchmark results.\nModels have been released under a Modified MIT license: See here.",
          "source_span": [
            "S002",
            "S003",
            "S006",
            "S033"
          ],
          "quotes": [
            "Timestral is a family of time series foundation models for zero-shot forecasting, available in 5M, 28M, 123M, and 209M parameter versions.",
            "This repository contains the 209M checkpoint.",
            "We’re releasing the source code in our GitHub repository to make it easy to run Timestral and reproduce our benchmark results.",
            "Models have been released under a Modified MIT license: See here."
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "Timestral supports univariate and multivariate forecasting, past-only and known-future covariates, and probabilistic predictions across 21 quantiles.",
          "quote": "Timestral supports univariate and multivariate forecasting, past-only and known-future covariates, and probabilistic predictions across 21 quantiles.\nIt accepts up to 32,768 historical time steps and forecasts up to 1,024 steps in a single forward pass.\nOutputs: 21 quantiles (0.01, 0.05, 0.1, 0.15, …, 0.85, 0.9, 0.95, 0.99).\nInputs: univariate or multivariate target variates, plus past-only and known-future covariates, numeric or categorical (categorical covariates are target-encoded).",
          "source_span": [
            "S004",
            "S005",
            "S014",
            "S015"
          ],
          "quotes": [
            "Timestral supports univariate and multivariate forecasting, past-only and known-future covariates, and probabilistic predictions across 21 quantiles.",
            "It accepts up to 32,768 historical time steps and forecasts up to 1,024 steps in a single forward pass.",
            "Outputs: 21 quantiles (0.01, 0.05, 0.1, 0.15, …, 0.85, 0.9, 0.95, 0.99).",
            "Inputs: univariate or multivariate target variates, plus past-only and known-future covariates, numeric or categorical (categorical covariates are target-encoded)."
          ]
        },
        "comparison": {
          "status": "supported",
          "claim": "The publisher reports that on GIFT-Eval, Timestral-209M posted lower MASE and CRPS errors than TimesFM-3.",
          "quote": "Timestral-209M compared with other models\n| Benchmark | Metric | Timestral-209M | t0-gamma | TimesFM-3 | Toto-2.0-2.5B | Chronos-2 |\n|---|---|---|---|---|---|---|\n| GIFT-Eval | MASE ↓ | 0.658 | 0.661 | 0.667 | 0.696 | 0.698 |\n| | CRPS ↓ | 0.446 | 0.452 | 0.456 | 0.476 | 0.485 |\n| TIME | MASE ↓ | 0.626 | 0.637 | 0.640 | 0.642 | 0.662 |\n| | CRPS ↓ | 0.522 | 0.534 | 0.536 | 0.539 | 0.556 |\n| fev-bench | SQL skill score ↑ | 50.39 | 49.42 | 48.99 | 44.42 | 47.28 |\n| | MASE skill score ↑ | 39.49 | 37.99 | 37.82 | 32.54 | 35.50 |\nResults across the Timestral family\n| Benchmark | Metric | Timestral-5M | Timestral-28M | Timestral-123M | Timestral-209M |\n|---|---|---|---|---|---|\n| GIFT-Eval |",
          "source_span": [
            "S019"
          ],
          "quotes": [
            "Timestral-209M compared with other models\n| Benchmark | Metric | Timestral-209M | t0-gamma | TimesFM-3 | Toto-2.0-2.5B | Chronos-2 |\n|---|---|---|---|---|---|---|\n| GIFT-Eval | MASE ↓ | 0.658 | 0.661 | 0.667 | 0.696 | 0.698 |\n| | CRPS ↓ | 0.446 | 0.452 | 0.456 | 0.476 | 0.485 |\n| TIME | MASE ↓ | 0.626 | 0.637 | 0.640 | 0.642 | 0.662 |\n| | CRPS ↓ | 0.522 | 0.534 | 0.536 | 0.539 | 0.556 |\n| fev-bench | SQL skill score ↑ | 50.39 | 49.42 | 48.99 | 44.42 | 47.28 |\n| | MASE skill score ↑ | 39.49 | 37.99 | 37.82 | 32.54 | 35.50 |\nResults across the Timestral family\n| Benchmark | Metric | Timestral-5M | Timestral-28M | Timestral-123M | Timestral-209M |\n|---|---|---|---|---|---|\n| GIFT-Eval |"
          ]
        },
        "limitations": {
          "status": "unverified",
          "claim": "",
          "quote": "",
          "source_span": []
        },
        "access": {
          "status": "supported",
          "claim": "The checkpoint runs through PyTorch on a CPU or GPU, and the models are released under a Modified MIT license.",
          "quote": "Inference: PyTorch on CPU or GPU.\nModels have been released under a Modified MIT license: See here.",
          "source_span": [
            "S017",
            "S033"
          ],
          "quotes": [
            "Inference: PyTorch on CPU or GPU.",
            "Models have been released under a Modified MIT license: See here."
          ]
        }
      }
    },
    {
      "story": 7,
      "title": "OpenAI and Poland’s NASK team up on AI safety",
      "source_sha256": "084cc1966482c0671bf7be5f3b79e7ae7b76c61bf9f5bc996599ce29ccd33006",
      "source_url": "https://openai.com/index/openai-nask-ai-safety-security-partnership",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 8,
      "title": "Research digest: METTA Lets Agents Adapt During the Task",
      "source_sha256": "15753bd80cb363ecdeffbe0dbca4bd448785dd2e8af35daadd03d15bc9f64448",
      "source_url": "https://arxiv.org/abs/2610.31656",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 9,
      "title": "SpaceX Super Intelligence opens a Grok partner network",
      "source_sha256": "4e0a51f07d7212faefa610cecfd059f6f5497832680fa6e6f664b82aa4165a65",
      "source_url": "https://x.ai/news/partnernetworkannouncement",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 10,
      "title": "Research digest: A Training Trick Makes Repeated AI Inference Less Memory-Hungry",
      "source_sha256": "94f751ebf74ff2d2cb133b80b4edaa559047974dc096401bdb1b597788231ab3",
      "source_url": "https://arxiv.org/abs/2610.31633",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 11,
      "title": "DeusData Brings Local Code Intelligence to AI Agents",
      "source_sha256": "7f9c105f197bb7f74bef99daa0f68641122ae1944180e39ddbd91cdeeabef67f",
      "source_url": "https://github.com/DeusData/codebase-memory-mcp",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 12,
      "title": "Microsoft’s Agensh coordinates 1,024 agents without a central boss",
      "source_sha256": "aeeee07f5cab5133002af91570962cbe79f5f67435c1a162b313084b49794b42",
      "source_url": "https://www.marktechpost.com/2026/10/24/microsoft-agensh-multi-agent-harness-1024-agents/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 13,
      "title": "Cognition Open-Sources a Vulnerability-Fixing Agent Plugin",
      "source_sha256": "634eedb26cb6874994817fe9bc38ac8704861ae609dc04af3edb99a35c5b412d",
      "source_url": "https://www.marktechpost.com/2026/10/24/cognition-devin-vulnerability-fixes-plugin-php2shell-nodejs-gitlab/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 14,
      "title": "Letta Tutorial Builds Stateful Engineering Copilots",
      "source_sha256": "84f12074dc163ab30eefec0eeec3f765a0da70e5bcea4af965beab42664641aa",
      "source_url": "https://www.marktechpost.com/2026/10/24/stateful-engineering-copilots-letta-tutorial/",
      "model_story": false,
      "model_review": null
    }
  ]
}
```
