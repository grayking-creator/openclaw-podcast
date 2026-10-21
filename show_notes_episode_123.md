# AgentStack Daily EP123 — Beam 1.0 lands, MLX runs near-trillion Muse, 10K agents go 36 hours

**Title:** Reflection's Beam 1.0 Lands on OpenRouter as a 501B Coding MoE

**Tagline:** Reflection's Beam 1.0 lists on OpenRouter as a 501B-parameter coding mixture-of-experts model. Apple MLX gets a near-trillion-parameter run of Muse Spark on a Mac Studio cluster. Grok Voice 3.0 takes the speech-to-speech index lead at $0.08 per minute. xAI packs Grok models into a $30 Cursor bundle. NVIDIA widens the Nemotron family with Super VL and Bolt edge variants. Four AI agents defeat Minecraft's Ender Dragon together. Third Moment Research runs 10,000 agents for 36+ hours straight. Hermes Agent ships v0.22.2, v0.22.1, v0.22.0, and v0.21.7. mcp-use 2.10 lands for fullstack MCP. GitHub Copilot deprecates several models on November 16.

**Feed description:** Today on AgentStack Daily: Reflection's Beam 1.0 debuts on OpenRouter as a 501B coding MoE. Apple MLX runs a near-trillion-parameter Muse Spark on a Mac Studio cluster. Grok Voice 3.0 tops the speech-to-speech index at $0.08 per minute. NVIDIA widens Nemotron with Super VL and Bolt edge models. Four AI agents defeat Minecraft's Ender Dragon together. Third Moment Research runs 10,000 agents for 36+ hours straight. Hermes Agent ships v0.22.2, v0.22.1, v0.22.0, and v0.21.7. mcp-use 2.10 lands for fullstack MCP. GitHub Copilot deprecates several models on November 16.

---

## Story Slate

1. **Agent Stack Release Readout: Hermes Agent v0.22.2, v0.22.1, v0.22.0, v0.21.7**
Hermes Agent v0.22.2 shipped October 15, 2026, walking back a bad v0.22.1 build that was made from the wrong commit. The earlier release had shipped unreleased gateway work and could stick the Microsoft Store app on a 'Connecting' screen. v0.22.2 re-ships the two fixes v0.22.1 was supposed to carry: a reboot bug that fooled Linux's supervised services and a sweep of laptop-friendly reliability improvements for local models.
Technical depth angle: On Linux, the kernel can reassign an early PID to a brand-new process after a restart. Hermes's supervised gateway would see that PID and refuse to start. The fix records which boot Hermes started in and asks the host lock when it can't tell - only a live gateway holds it. Local requests also stream prompt-reading progress, skip stall time while the machine sleeps, and size the prompt cache to free Windows unified memory.
Actionability angle: Supervised-gateway users whose agent refused to start after a reboot - and Microsoft Store users whose app froze on Connecting - should update to v0.22.2 right away. Local-model builders on Windows unified-memory laptops will see longer turns hold up better, with stall timers respecting sleep and prompt caches sized to free memory.
Listener hook: Yesterday's Hermes update broke the Microsoft Store and the Linux gateway - today's patch fixes both.

2. **Reflection's Beam 1.0 lists on OpenRouter as a 501B coding MoE**
A new open-weight reasoning model from Reflection, called Beam 1.0, has appeared on OpenRouter. It uses a sparse mixture-of-experts architecture with 501 billion total parameters and 23 billion active per token, paired with a one-million-token context window. Reflection positions it for coding and long-running agentic workflows. 
Technical depth angle: Sparse mixture-of-experts means each token only activates 23 billion of the model's 501 billion parameters, which keeps inference cost closer to a much smaller model while the wider parameter pool holds more skills. The one-million-token context window lets the model keep a long-running codebase or a multi-step agent trace inside a single session.
Actionability angle: What this means for builders is that OpenRouter now carries a 501B MoE aimed squarely at long-horizon coding agents, with enough context to hold a serious project in memory. 
Listener hook: A 501-billion-parameter open-weight reasoning model for coding agents just showed up on OpenRouter — here's what the listing tells us.

3. **Apple MLX Runs Near-Trillion Parameter Muse Spark Open on Mac Studio Cluster**
Apple's machine learning research team published a guide showing how to run the near-trillion parameter Muse Spark Open model across a cluster of Mac Studios using MLX and a new RDMA-over-Thunderbolt link. On four M5 Ultra Mac Studios, the mixture-of-experts model generates over 36 tokens per second. The post also benchmarks Mistral Medium 3.5 and Qwen 3.8 on single machines, highlighting that the M5 Ultra's GPU Neural Accelerator delivers up to 4.6× faster time-to-first-token compared to the M3 Ultra, while drawing about 300 watts.
Technical depth angle: MLX v0.30.1 and later builds on macOS 26.2's low-latency RDMA-over-Thunderbolt 5 driver, adding jaccl communication collectives for splitting large models across multiple machines. Two parallelization schemes are supported: pipeline parallelism splits a model across depth (layer by layer), while tensor parallelism splits across width. The M5 Ultra's GPU Neural Accelerator speeds up the matrix-multiplication-heavy prefill stage up to 4.6× over the M3 Ultra.
Actionability angle: Builders running large models locally can experiment with MLX v0.30.1 or later on M5 Ultra Mac Studios for private inference at modest power draw. The new mlx.launch helper and jaccl collectives let you scale across Thunderbolt-tied machines without needing a datacenter.
Listener hook: You can now run a near-trillion parameter language model entirely on a cluster of Mac Studios in your office, without sending a single prompt to the cloud.

4. **Open-source 3D architectural editor ships CLI and MCP tools for AI agents**
Pascal Editor is an open-source 3D architectural editor that ships with a local command-line interface and Model Context Protocol tools, designed for both human designers and AI agent workflows. Its @pascal-app/cli package reached version 1.0.4 on October 13, 2026, and the project sits at around 24,900 GitHub stars, pointing to an established builder community. The combination of a CLI plus MCP integration makes the editor scriptable and agent-accessible rather than GUI-only.
Technical depth angle: The notable mechanism is the pairing of a local CLI with Model Context Protocol tools. MCP is the standard that lets AI assistants call external tools directly, so rather than being a GUI-only application, Pascal Editor exposes its functionality in ways an agent can drive, while still letting humans work in the same environment.
Actionability angle: For builders, this means a 3D architectural editor that an AI agent can manipulate through MCP, useful for automating repetitive modeling tasks or handing parts of the design workflow to an assistant. It also stays usable from a CLI for scripted, headless work. Worth checking the repository's MCP tool list to see exactly which scene operations are exposed.
Listener hook: An open-source 3D editor that AI agents can drive directly through MCP could change how architectural modeling gets automated.

5. **MiniCPM-V 4.7 Gets a Speed Boost via Speculative Decoding**
OpenBMB published a GGUF-quantized DSpark draft checkpoint for its MiniCPM-V 4.7 vision-language model on Hugging Face, bringing speculative decoding to this edge-capable 35-billion-parameter multimodal model. The draft predicts multiple tokens per step, letting the main model verify them in parallel rather than generating one at a time. Benchmark acceptance lengths show 5 to 7 tokens accepted per verification round across vision and text tasks, which translates to faster perceived output on local hardware.
Technical depth angle: The DSpark draft has 389 million parameters and predicts 15 tokens per forward pass, targeting specific hidden-state layers in the 35B base model. It trains on 2 million vision-and-text sequences using a confidence-loss objective to improve prediction accuracy. The acceptance-length metric measures how many draft tokens survive verification per step.
Actionability angle: Developers running MiniCPM-V 4.7 locally can now attach this draft to accelerate generation without changing outputs. Draft quantization affects only how well predictions are accepted, not the final text, so Q6_K or Q8_0 are recommended defaults. Pair it with the matching target GGUF and vision projector, then run with --spec-type draft-dspark in llama-cli or llama-server.
Listener hook: If you're running vision models on a local machine or edge device, this draft could cut your token-generation time significantly.

6. **NVIDIA Expands Nemotron Family with Super VL and Bolt Edge Models**
NVIDIA expanded its open Nemotron family with three models covering the full agent deployment range. Nemotron 3.5 Super VL is a 120-billion-parameter open model for high-volume always-on agents, with accuracy comparable to NVIDIA's largest reasoning model at roughly one-fifth the parameter count. Bolt 74B-A9B 24GB uses native 2-bit quantization to fit a 74B-parameter model into 24GB of memory for local agentic workloads. Bolt E4B 4GB, for fast conversational agents on small hardware, arrives October 23. Super VL and Bolt 74B-A9B are available now on Hugging Face, Open Router, ModelScope, and as NVIDIA NIM microservices.
Technical depth angle: Super VL is trained on about 26 trillion tokens and post-trained with roughly 3.8 million samples across dozens of reinforcement-learning environments. Bolt 74B-A9B uses native 2-bit quantization to compress a 74-billion-parameter model into 24GB of memory, letting it run alongside other applications on RTX and DGX Spark hardware.
Actionability angle: Builders can download Super VL weights today from Hugging Face and serve them through NVIDIA NIM microservices or self-host via vLLM. For local agent work, Bolt 74B-A9B runs in llama.cpp, Ollama, LM Studio, and Unsloth on RTX PRO workstations and DGX Spark, which means a 24GB GPU is enough to run the top-ranked open model on PinchBench without sending data to the cloud.
Listener hook: An open agent model now fits in 24GB of memory and runs locally on RTX hardware, no cloud required.

7. **Research digest: Four AI Agents Beat Minecraft's Ender Dragon Together**
A team of four Gemini 4 Argon agents beat Minecraft's Ender Dragon inside a sandboxed survival world. The agents wrote and debugged all of their own code, coordinated through in-game chat and a shared memory store, and required no human-assigned roles or pre-written game logic. Researchers monitored the run on a live dashboard and could pause or stop it at any time. The paper is trending on HuggingFace's daily feed.
Technical depth angle: Four Gemini agents each piloted a Mineflayer player and exchanged plans and status through in-game chat plus a shared memory buffer. No scripted roles or hand-crafted strategies were provided; the agents generated, tested, and fixed their own programs as the run progressed.
Actionability angle: This signals that asking several language models to coordinate through chat and a shared scratchpad can produce non-trivial multi-agent behavior on open-ended tasks. For builders, it suggests a small toolset, a shared memory store, and free-form conversation may be enough to get emergent collaboration without bespoke orchestration code. That's worth stress-testing on your own agent prototypes.
Listener hook: Four AI agents just beat one of gaming's hardest bosses — without anyone telling them how.

8. **Grok Voice 3.0 Tops Speech-to-Speech Index at the Same $0.08 a Minute**
xAI shipped Grok Voice 3.0, a speech-to-speech model that tops Artificial Analysis's Speech-to-Speech Index at 86.9 and holds sub-second latency. It matches its predecessor's $0.08-per-minute API price, leads ServiceNow's EVA-Bench on accuracy and customer experience, and is already handling millions of in-car conversations at Tesla plus 20,000 Starlink support calls a day across multiple languages, with roughly 70% resolving without a human.
Technical depth angle: The Artificial Analysis Speech-to-Speech Index blends speech reasoning, conversational dynamics (pauses, interruptions, turn-taking), blind head-to-head preference, and task success. Grok Voice 3.0's 86.9 comes from topping three sub-scores while staying cheaper per task on Big Bench Audio and below one-second response latency.
Actionability angle: Builders using `grok-voice-latest` are already on the new model with no code changes, so the new sub-scores arrive at the same $0.08/min price. If you are piloting a support agent, the ServiceNow EVA-Bench result is the most useful signal because it scores voice agents across more than 200 realistic enterprise scenarios rather than synthetic chat prompts.
Listener hook: Voice agents just got measurably better at handling real customer calls, and the price didn't move.

9. **xAI's $30 Bundle Puts Grok Models Inside Cursor**
xAI launched The X Subscription, a single plan that bundles Grok, Grok Bot, the Cursor coding agent, and X Premium, with the Premium tier priced at $30 a month and pitched as replacing roughly $90 worth of separate subscriptions. Paid tiers share a single pool of Grok model usage that flows between the Grok apps and Cursor's coding agents, while third-party models in Cursor stay billed separately at API list prices. Free through Ultra tiers span zero to $200 a month, and Teams and Enterprise plans consolidate billing and admin tooling under one roof.
Technical depth angle: The mechanism behind the bundle is a shared Grok model usage pool that travels between Grok's chat, voice, image, and video generation features and Cursor's local and cloud coding agents, so one monthly allowance covers both chat reasoning and code generation. Third-party models in Cursor stay pay-as-you-go via API top-ups on Premium and above.
Actionability angle: For builders, this means Cursor subscribers can now route xAI's Grok models through their coding workflow under the same bill, with at least twice the coding usage versus the comparable standalone Cursor plan. For engineering teams, the package folds SSO, admin controls, usage analytics, and SOC 2 compliance into one consolidated purchase, which simplifies rolling a single tool budget across an organization.
Listener hook: If you already pay for Cursor or SuperGrok, xAI is now selling both under one $30 plan with shared usage.

10. **mcp-use 2.10 lands for a fullstack MCP framework covering ChatGPT, Claude, and agent servers**
mcp-use, an open source framework for building MCP apps that run inside ChatGPT and Claude alongside MCP servers for AI agents, pushed release 2.10 on October 14 with the repository reporting 10,772 GitHub stars. The project positions itself as fullstack: a single codebase that produces chat-surface apps on the front end and agent-facing servers on the back end.
Technical depth angle: It is a fullstack MCP framework that bundles chat-surface app development with agent-facing server deployment in a single project, letting one codebase ship in two directions at once.
Actionability angle: Builders targeting both ChatGPT and Claude can use mcp-use to share a codebase across the two chat surfaces rather than maintaining parallel integrations. The framework also covers the agent-facing MCP server side, so the same project can expose tools to agents. With an active 2.10 release and a community above ten thousand stars, it sits as a plausible default for new MCP prototypes.
Listener hook: One open source framework now lets you ship the same MCP app to ChatGPT and Claude without writing two integrations.

11. **Third Moment Research Runs 10,000 Agents for 36+ Hours Straight**
Third Moment Research is running ten thousand AI agents for thirty-six hours and counting, using GPT-6 Astra, GPT-6.1 Sol, Codex, and Daybreak for cybersecurity. Featured on OpenAI's news index in mid-October, the lab's setup is built around agents that hold their focus across multi-day runs and get better the more they are used.
Technical depth angle: The lab's stack layers GPT-6 Astra and GPT-6.1 Sol with Codex for code execution and Daybreak for cybersecurity. The mechanism is persistence plus accumulated feedback, so agents stay coherent across multi-day runs and improve with repeated use.
Actionability angle: Long-horizon agent deployments are now a real pattern at frontier labs, which means builders can start planning workflows that span days rather than minutes. The fact that one lab runs ten thousand agents on a layered stack of models plus specialized tools suggests the templates for sustained multi-agent operations are starting to exist.
Listener hook: One lab is keeping ten thousand AI agents running for over a day and a half — here's the stack that makes it possible.

12. **Block's security team cuts threat response to minutes with OpenAI**
Block is building AI-powered security with OpenAI, and the early numbers are concrete: its security team investigates threats faster and proposes patches in minutes. The collaboration surfaced through OpenAI News on October 14, 2026. It places OpenAI's models inside Block's incident workflow, helping compress the path from detection to a candidate fix rather than sitting at the edge as a chat assistant. For enterprise security, this is what generative models inside the response loop actually look like in production.
Technical depth angle: The mechanism is workflow placement: OpenAI's models sit inside Block's threat investigation and remediation loop rather than at the edge. That compresses the time from detection to a candidate patch down to minutes, while the team still owns the decisions and approvals.
Actionability angle: For security and IT teams, this is a signal that incident response is now a serious deployment target for generative models, not just a chat surface. What this means in practice: feed the model the same context your analysts see, keep a human in the approval loop, and the gap between detection and a candidate patch can shrink to minutes. The metric worth watching is minutes-scale turnaround, which is what Block is now reporting.
Listener hook: If you've ever watched a security team scramble for hours on a fix that could land in minutes, this is what that shift looks like in practice.

13. **Small Vision Model Gets Draft Boost for Local AI**
OpenBMB published a GGUF-quantized DSpark draft checkpoint for MiniCPM-V-4.7-1B, a compact vision-language model designed for on-device use. The draft runs alongside the target model using speculative decoding, generating 15 candidate tokens per forward pass that the main model verifies. This pairing lets developers run vision understanding locally at higher effective speed, since the draft handles initial token prediction and the target confirms or rejects each guess.
Technical depth angle: Speculative decoding works by having a smaller draft model propose token sequences that a larger target model validates in parallel. Here the DSpark draft has 5 layers generating up to 15 tokens per pass, operating on specific hidden-state layers [3, 7, 11, 15, 19] of the target. Draft quantization does not affect output quality—only acceptance rate—so Q8_0 or Q6_K are recommended. Evaluation measured acceptance length as total completion tokens divided by verification steps, ranging from 3.4x on general text to 5.9x on math domains.
Actionability angle: If you run vision-language models on edge hardware, pairing this draft with the target MiniCPM-V-4.7-1B through llama-cli or llama-server should reduce perceived latency for image understanding tasks. The configuration requires --spec-type draft-dspark, GPU offloading flags at 99 for both models, and the matching vision projector file. Draft quantization only affects acceptance length, so Q8_0 keeps the draft small without changing outputs.
Listener hook: A compact 1B-parameter vision model just got a dedicated draft module that could make it run noticeably faster on your laptop or edge device.

14. **GitHub Copilot to Deprecate Several Models on November 16**
GitHub will retire a set of GitHub Copilot models across every Copilot surface on November 16, 2026. The deprecation covers Copilot Chat, inline edits, ask and agent modes, and code completions, applying uniformly across chat, edits, and completions. Anyone whose workflow depends on a soon-to-be-deprecated model will need to pick a replacement before that cutoff or face broken completions.
Technical depth angle: GitHub is removing a batch of models from every Copilot entry point on a single fixed date. The deprecation covers Chat, inline edits, ask, agent, and code completions, so one switchover day applies across the entire Copilot surface rather than rolling out product by product.
Actionability angle: This matters because anyone running Copilot today needs to know whether their default model is on the deprecation list before November 16. The cutoff is hard, so models on the list will stop responding on that date, breaking any workflow that has not already moved to a replacement.
Listener hook: GitHub Copilot is retiring a set of models on November 16, so your default may need a quick check before that day.

---

## Editorial Mix Check

- flagship_products: 8
- builder_projects: 8
- local_ai: 4
- hardware_compute: 2
- policy_regulation: 3
- research: 1

---

## Model Discovery Check

- **Reflection: Beam 1.0 501B A23B** (reflection) — Newly listed this cycle (verified October 16, 2026). Primary source: https://openrouter.ai/models/reflection/beam-1.0-501b-a23b. Availability: API via OpenRouter. params_active: 23B; params_total: 501B; context: 1048576 tokens; modality: text input and text output. Capabilities: context length 1048576; Beam 1.0 is Reflection's open-weight reasoning model for coding and long-horizon agentic workflows. It uses a sparse mixture-of-experts architecture with 501B total and 23B active parameters per token, and a.... Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/reflection/beam-1.0-501b-a23b and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **MiniCPM-V-4.7-35B-A3B-DSpark** — Source checked October 16, 2026. Primary source: https://huggingface.co/openbmb/MiniCPM-V-4.7-35B-A3B-DSpark-gguf. Availability: The quantized draft runs with llama-cli or llama-server using the --spec-type draft-dspark flag, requiring a llama.cpp build with dflash architecture.. params_active: n/a; params_total: 389 million (approximately; draft checkpoint); context: 8192 tokens (documented example configuration); modality: text drafting for a vision-language target. Capabilities: The draft model predicts 15 tokens per forward pass, and benchmarks show publisher-reported averages of 3.501 accepted tokens per verification step on general text and 7.387 on code generation. Evidence: publisher_report. Decision: Selected — covered in the numbered slate from a non-OpenRouter source.

- **MiniCPM-V-4.7-1B-DSpark** — Source checked October 16, 2026. Primary source: https://huggingface.co/openbmb/MiniCPM-V-4.7-1B-DSpark-gguf. Availability: The GGUF-quantized draft is downloadable from Hugging Face alongside the target model and vision projector for local deployment.. params_active: n/a; params_total: 213.5 million (approximately; draft checkpoint); context: 8192 tokens (documented example configuration); modality: text drafting for a vision-language target. Capabilities: The DSpark draft generates 15 candidate tokens per forward pass across 5 draft layers, which the target model verifies to accelerate inference. Evidence: publisher_report. Decision: Selected — covered in the numbered slate from a non-OpenRouter source.

---

## Local LLM Spotlight

- **jialinyyzz/humanizer** — https://huggingface.co/jialinyyzz/humanizer — Trending open model on Hugging Face; task text-generation; 1808 likes and 85612 downloads. Tags: gguf, safetensors, gemma4_unified, image-text-to-text, humanizer, transformers, text-rewriting, rewriting, paraphrase, style-transfer.
  Try now: Read the linked model card before downloading, and choose a runtime or device only after it confirms the license, weight format, context window, benchmarks, and hardware requirements.

---

## GitHub Project Radar

- **HKUDS/nanobot** — https://github.com/HKUDS/nanobot — HKUDS/nanobot is an ultra-lightweight, open-source, self-hosted Python framework for personal AI agents, bundling a WebUI, tools, memory, MCP support, multi-agent workflows, automation, and chat apps. `stars: 49,090`; `stars_delta_30d: +1,070 (+2.2%) since 2026-09-11`; `latest_release: v0.3.5 (2026-09-15)`.
  Why this is on the radar now: v0.3.5 shipped on 2026-09-15 and the repository was updated on 2026-10-16.
  Stack improvement angle: Running nanobot next to an OpenClaw/Codex/Claude Code/Hermes harness gives that stack a self-hosted coordinator that exposes MCP-native memory and tools, so multiple harnesses can share one persistent agent runtime.
  Try now: Clone the repo, start the WebUI locally, and wire one of your existing harnesses into nanobot's MCP endpoint to share state.

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — DeusData/codebase-memory-mcp is a high-performance code intelligence MCP server that indexes a repository into a persistent knowledge graph with sub-ms queries across 162 languages, distributed as a single static binary with zero dependencies. `stars: 46,710`; `stars_delta_30d: +3,756 (+8.7%) since 2026-09-11`; `latest_release: v0.12.0 (2026-10-15)`.
  Why this is on the radar now: v0.12.0 shipped on 2026-10-15 and the repository was updated on 2026-10-16.
  Stack improvement angle: Adding it to an OpenClaw/Codex/Claude Code/Hermes stack lets the agent traverse cross-file references via graph queries instead of stuffing source files into context, cutting tokens during refactors.
  Try now: Run the static binary against a sample repo, then register it in your harness's MCP config and issue a structural query to confirm the graph wiring.

- **ahujasid/mcp-for-blender** — https://github.com/ahujasid/mcp-for-blender — ahujasid/mcp-for-blender is a community plugin that exposes Blender 3D scene operations as MCP tools so any LLM can drive Blender, and it is not affiliated with the official Blender Foundation. `stars: 31,163`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: none published on GitHub as of 2026-10-16`.
  Why this is on the radar now: The repository was updated on 2026-10-06 and enters the radar with 31,163 stars.
  Stack improvement angle: Registering the plugin as an MCP server turns Blender into a tool-callable surface inside your OpenClaw/Codex/Claude Code/Hermes agent, so 3D scene edits become a structured tool call rather than hand-written Python.
  Try now: Install the plugin in Blender, list its MCP tools from the agent harness, and run one tool call that creates or modifies a scene primitive.

---

## Extra Research Candidates

- **openbmb/MiniCPM-V-4.7-1B-DSpark-gguf model repository on Hugging Face** — https://huggingface.co/openbmb/MiniCPM-V-4.7-1B-DSpark-gguf — --- license: apache-2.0 language: en zh library_name: transformers pipeline_tag: text-generation tags: minicpmv minicpmv4.7 text-generation vision-understanding tool-calling on-device edge-ai base_model: openbmb/MiniCPM-V-4.7-1B-DSpark base Technical depth angle: openbmb/MiniCPM-V-4.7-1B-DSpark-gguf pairs a 213,547,777-parameter, 5-layer DSpark draft checkpoint (BF16) with the MiniCPM-V-4.7-1B target, consuming 15 draft tokens per forward pass for llama.cpp speculative decoding via the dflash architecture and the --spec-type draft-dspark Markov head.

- **PrefectHQ/fastmcp — 🚀 The fast, Pythonic way to build MCP servers and clients.** — https://github.com/PrefectHQ/fastmcp — 🚀 The fast, Pythonic way to build MCP servers and clients. GitHub reports 28105 stars. Latest release: v4.1.0 2026-10-08T22:56:26Z. Repository pushed 2026-10-16T18:04:44Z. Technical depth angle: PrefectHQ/fastmcp is a Python framework that builds MCP servers and clients through a decorator-driven API, with release v4.1.0 published 2026-10-08 and the repository pushed 2026-10-16.

- **microsoft/mcp-for-beginners — This open-source curriculum introduces the fundamentals of Model Context Protoco** — https://github.com/microsoft/mcp-for-beginners — This open-source curriculum introduces the fundamentals of Model Context Protocol (MCP) through real-world, cross-language examples in .NET, Java, TypeScript, JavaScript, Rust and Python. Designed for developers, it focuses on practical tec Technical depth angle: microsoft/mcp-for-beginners is a multi-language Model Context Protocol curriculum that ships practical, modular examples across .NET, Java, TypeScript, JavaScript, Rust, and Python.

---

## Show Notes

```md
Episode 123 — October 16, 2026

[00:00] Episode hook

Reflection's Beam 1.0 landed on OpenRouter as a 501-billion-parameter sparse mixture-of-experts reasoning model with 23 billion active parameters. Hermes Agent shipped v0.22.2 on October 15, 2026 to roll back a faulty v0.22.1 build that had been assembled from the wrong commit and shipped unreleased gateway work. NVIDIA filled out its open Nemotron family with three models, headlined by the 120-billion-parameter Nemotron 3.5 Super VL for always-on high-volume agents, plus Bolt edge variants for tighter deployments. Apple published a guide for running the near-trillion-parameter Muse Spark Open model across a cluster of Mac Studios using MLX and an RDMA-over-Thunderbolt fabric. The open-source 3D architectural editor Pascal Editor shipped a local CLI and Model Context Protocol tools aimed at AI agent workflows. OpenBMB pushed a GGUF-quantized DSpark draft checkpoint for MiniCPM-V 4.7, adding speculative decoding to the 35-billion-parameter vision-language model.

[02:00] Agent Stack Release Readout: Hermes Agent v0.22.2, v0.22.1, v0.22.0, v0.21.7

Hermes Agent v0.22.2 shipped October 15, 2026, and it's the release v0.22.1 was supposed to be. The previous day, v0.22.1 was built from the wrong commit, which means it shipped unreleased gateway work, and the Microsoft Store version could stick on a "Connecting" screen. 0.22.2 walks back that mistake and ships two fixes instead.

The bigger of the two is a reboot bug. On Linux, after a restart, the kernel can hand out an early PID that ends up belonging to some completely unrelated process that came up first. The supervised gateway - systemd, launchd, Docker - would then see what looked like a running gateway and refuse to start. Hermes now records which boot it started in, and when it can't tell, it asks the host lock, which only a live gateway actually holds.

The other is a sweep of laptop ergonomics for local models. Local requests now always stream prompt-reading progress on the status line, so you can see how far the server has gotten on a long prompt. Stall timers skip time the laptop was asleep, so a sleeping conversation doesn't look stalled. A recovered local server gets one more retry instead of a circuit breaker that fails every later turn. Compression no longer times out while the server is still reading a long conversation. On Windows unified-memory machines, model launch and the prompt cache are sized to free memory, which matters when there's no separate VRAM pool.

One caveat the project is calling out: sessions that ran under the 0.22.1 gateway can't be deleted in 0.22.2. Anything that started cleanly under the right build can be cleared; only the bad-build sessions are stuck.

Context for the line: v0.22.0 came out October 13 as the "Threshold Release," described by the project as the largest window Hermes has shipped, about 2.5x the v0.21.0 cycle. The headline additions there were a guided first-launch setup chat that runs on a free trial model so newcomers don't need an API key to start, connectors that bring the agent into hosted apps, a one-click llama.cpp runtime for local models, and signed desktop packages including the Microsoft Store build.

For builders, this is mostly a stability update. If your supervised gateway refused to start after a server reboot, or your Store app froze on Connecting, this update is the fix. Local-model tinkerers, especially on Windows unified-memory laptops, get a quieter experience on long conversations and laptop sleeps.

[03:47] Reflection's Beam 1.0 lists on OpenRouter as a 501B coding MoE

A new open-weight reasoning model from Reflection called Beam 1.0 has surfaced on OpenRouter as a model listing. It is a sparse mixture-of-experts model with 501 billion total parameters and 23 billion active per token, a one-million-token context window, and is positioned for coding and long-horizon agentic workflows.   The shape on offer is a workhorse: a half-trillion-parameter MoE aimed at agentic coding, with enough context to hold a serious project in one session. The model is listed on OpenRouter under the identifier reflection/beam-1.0-501b-a23b.

[04:38] Apple MLX Runs Near-Trillion Parameter Muse Spark Open on Mac Studio Cluster

Apple's ML research group published a hands-on guide for running frontier-scale language models entirely on Mac Studio hardware using MLX, their open-source array framework. The headline result: a near-trillion parameter mixture-of-experts model called Muse Spark Open generates over 36 tokens per second when distributed across four Mac Studios with M5 Ultra chips, well above average reading speed.

On a single M5 Ultra Mac Studio with 512GB of unified memory, Mistral Medium 3.5 (128 billion parameters) and Qwen 3.8 (27 billion parameters) both fit comfortably. The M5 generation adds a GPU Neural Accelerator dedicated to matrix multiplication, which translates into up to 4.6× faster time-to-first-token compared to the M3 Ultra. Decode speed, which is limited by memory bandwidth, improves by about 1.6× thanks to the M5 Ultra's 1.2 TB/s of unified memory bandwidth, up from 819 GB/s on M3 Ultra. Peak power stays around 300 watts, roughly what a toaster pulls.

Muse Spark Open, with 816 billion total parameters and 42 billion active per token, needs roughly 493GB in NVFP4 quantization, too large for one machine. MLX v0.30.1 and later, paired with macOS 26.2's low-latency RDMA-over-Thunderbolt 5 driver, splits the model across multiple Macs using new communication collectives called jaccl. MLX supports two approaches: pipeline parallelism, which splits the model across depth (one Mac runs the first half of the layers, then passes results to the second), and tensor parallelism, which splits across width. A helper command, mlx.launch, makes it straightforward to fire off jobs across multiple hosts over a Thunderbolt-tied pair.

For builders, the workflow means large models can stay local on office hardware, supporting private agentic coding and other context-heavy workloads without touching the cloud.

[06:22] Open-source 3D architectural editor ships CLI and MCP tools for AI agents

The Pascal Editor repository, an open-source 3D architectural editor, recently pushed updates including its @pascal-app/cli package at version 1.0.4 on October 13, with the repository itself pushed again on October 16. The project ships a local command-line interface and Model Context Protocol tools, and is described as supporting practical workflows for both human designers and AI agents. The MCP piece is the interesting part: MCP is the standard that lets AI assistants call external tools, so integrating it into a 3D editor means agent-driven workflows are a first-class concern, not a bolted-on afterthought. The repo sits at around 24,900 GitHub stars, suggesting an established builder audience has already formed around it. For developers, the takeaway is that a CLI plus MCP tooling makes the editor scriptable and agent-accessible from day one, useful if you want to automate repetitive modeling tasks or hand parts of the design process to an AI assistant without giving up a direct human workflow. The October 16 push shows active maintenance. Watch for documentation of which specific MCP tools ship and what scene operations they expose, since that list will determine how much of the editor an agent can realistically drive on its own.

[07:37] MiniCPM-V 4.7 Gets a Speed Boost via Speculative Decoding

OpenBMB published a GGUF-quantized DSpark draft checkpoint for MiniCPM-V 4.7 on Hugging Face, enabling speculative decoding with llama.cpp. MiniCPM-V is a family of open vision-language models designed for on-device and edge deployment, and this repository makes it runnable with llama.cpp speculative decoding. Speculative decoding pairs a small draft model that predicts multiple tokens with a larger target model that verifies those predictions in parallel. Instead of waiting for the full 35-billion-parameter model to generate one token at a time, the draft proposes a batch that the target confirms or rejects, which speeds up the visible output rate. The draft has roughly 389 million parameters and predicts 15 tokens per forward pass, targeting specific hidden-state layers in the base model. Evaluation numbers show acceptance lengths ranging from about 3.5 tokens per verification round on general text to 7.4 on code tasks, with vision benchmarks like MMMU and MathVista landing around 5 to 6 tokens accepted. To use it, download the target model, its vision projector, and the quantized draft, then run with the draft-dspark spec type in llama-cli or launch it as a multimodal server. The draft must be paired with the matching MiniCPM-V 4.7 35B-A3B target, and it requires a llama.cpp build that supports the dflash architecture and DSpark Markov head. Quantizing the draft itself only affects how often predictions are accepted, never the final output, so developers can use the smallest quantized draft that fits their memory budget. The draft model predicts 15 tokens per forward pass, and benchmarks show publisher-reported averages of 3.501 accepted tokens per verification step on general text and 7.387 on code generation. The quantized draft runs with llama-cli or llama-server using the --spec-type draft-dspark flag, requiring a llama.cpp build with dflash architecture.

[09:24] NVIDIA Expands Nemotron Family with Super VL and Bolt Edge Models

NVIDIA expanded its open Nemotron family this week with three models covering the full agent deployment range — from data center down to RTX desktops. The flagship is Nemotron 3.5 Super VL, a 120-billion-parameter open model built with the Nemotron Coalition for high-volume always-on agents. NVIDIA says it matches the accuracy of its largest reasoning model at roughly one-fifth the parameter count, and runs up to 5x faster than the next-best in its class on the Artificial Analysis Intelligence Index.

Bolt 74B-A9B 24GB is built for local agentic workloads on RTX and DGX Spark. The trick is a native 2-bit quantization — a compression that crams the 74-billion-parameter model into 24GB of memory, leaving room for other applications. NVIDIA ranks it the #1 open model in its memory class on PinchBench and #2 on BrowseComp. It supports llama.cpp, Ollama, LM Studio, Unsloth, and vLLM.

A third model, Bolt E4B 4GB, ships October 23 for conversational and physical agents on GeForce RTX, Jetson, and DGX Spark. Super VL and Bolt 74B-A9B are available now on Hugging Face, Open Router, ModelScope, and as NVIDIA NIM microservices.

Super VL was trained on about 26 trillion tokens and post-trained with roughly 3.8 million samples across dozens of reinforcement-learning environments. NVIDIA is also releasing open datasets on Hugging Face for tool use, finance, instruction following, long context, fairness, and vision-language understanding, plus the reinforcement-learning environments in NeMo Gym.

The customization pipeline is already busy: Scale AI adapted it for Skydance's vendor credit finance agent and EY's M&A due diligence agent; AfterQuery tuned it for Hebbia's credit agreement analysis; Mercor post-trained it for coding agents on the APEX-SWE benchmark; and integrations are live at Atlassian, CrowdStrike, Dassault Systèmes, Perplexity, Salesforce, and Synopsys. Scaled on NVIDIA Dynamo, NVIDIA claims up to 8x more users with 85% lower latency.

[11:17] Research digest: Four AI Agents Beat Minecraft's Ender Dragon Together

A team of four Gemini 4 Argon agents has beaten Minecraft's Ender Dragon inside a sandboxed survival world, and the paper describing the run is trending on HuggingFace's daily feed. Each agent controlled a player through an open-source library called Mineflayer. The agents talked to each other in the in-game chat and kept a shared memory they could read and write to, but nobody assigned them roles or handed them game logic. The agents planned, wrote, and debugged every program themselves as the run unfolded. Researchers watched the whole thing on a live dashboard and could pause or stop the agents at any time, though they say they never needed to. The point isn't just a Minecraft trophy — it's a clean demonstration of multi-agent coordination on an open-ended task. With nothing more than chat, shared memory, and the ability to write their own code, four models handled a long-horizon goal that usually demands hours of human play. That's the pattern anyone building agent stacks should be watching closely.

[12:21] Grok Voice 3.0 Tops Speech-to-Speech Index at the Same $0.08 a Minute

xAI shipped Grok Voice 3.0 today, a speech-to-speech model that tops Artificial Analysis's Speech-to-Speech Index with a score of 86.9, ahead of its own predecessor at 81.3 and ahead of GPT-Live-1 (Astra, Medium) at 83.2 and Gemini 3.8 Live (Ext. Thinking, High) at 82.6. The model hits sub-second latency, costs less per task than comparable models on Artificial Analysis's Big Bench Audio run, and is priced identically to Grok Voice 2.0 at $0.08 per minute in the Voice Agent API.

On the harder sub-scores, Grok Voice 3.0 lands 98.5% on Speech Reasoning Big Bench Audio, 1070 Elo on Human Preference Speech Agent Arena, 94.8% on Task Completion, and 97.0% on Full Duplex Bench, the last measuring how naturally a model handles pauses, turn-taking, and interruptions. On ServiceNow's EVA-Bench, which scores enterprise voice agents across more than 200 scenarios, it posts 74% accuracy and leads on a combined accuracy-and-experience score. ServiceNow's Nitin Aggarwal called it a new Pareto frontier for front-line customer service AI.

The model is already running at scale. Tesla uses it for millions of daily in-car conversations, where drivers check calendars, send emails, order coffee, or book dinner hands-free through Grok Bot. Starlink call centers route 20,000 calls a day through Grok Voice across multiple languages, with roughly 70% resolving without a human in the loop and about one in four sales calls ending in a purchase. Existing agents built on `grok-voice-latest` have already been migrated with no code changes.

[13:52] xAI's $30 Bundle Puts Grok Models Inside Cursor

xAI rolled out a single subscription bundle that pulls together its Grok assistant, Grok Bot, the Cursor coding agent, and X Premium, with the Premium tier priced at $30 a month and pitched as replacing roughly $90 worth of separate subscriptions. The spine of the deal is a shared pool of Grok model usage that travels across Grok chat, voice, image and video generation, and inside Cursor's coding agents. Third-party models in Cursor still work on Premium and above, billed separately through API top-ups at list price.

The lineup starts at a free tier with daily Grok access and a starter Cursor allowance. Plus runs $8 a month with more AI usage in Grok and Cursor plus an X checkmark and fewer ads. Premium at $30 unlocks what used to be SuperGrok, Cursor Pro, and X Premium+ combined, with four times the Plus usage. Super at $100 multiplies that by fifteen, and Ultra at $200 by fifty. xAI says each paid tier includes at least twice the coding usage with its models as the comparable standalone Cursor plan.

For teams, Premium, Super, and Ultra are available per-seat at the same individual prices, replacing older Cursor Teams pricing while adding three times the coding usage plus SSO, admin controls, consolidated billing, usage analytics, and SOC 2 compliance. Enterprise customers get a single dashboard managing Grok and Cursor with one shared usage pool. Existing SuperGrok, Cursor, and X Premium subscribers can keep their current plan or switch through account billing with prorated refunds during the rollover window.

[15:29] mcp-use 2.10 lands for a fullstack MCP framework covering ChatGPT, Claude, and agent servers

mcp-use, an open source framework for building MCP apps, released version 2.10 on October 14. The project positions itself as fullstack: a single codebase that targets MCP apps for ChatGPT and Claude on the front end, and MCP servers for AI agents on the back end. The repository reports 10,772 GitHub stars, putting it among the more popular MCP developer kits in active circulation.

For builders, the practical pitch is consolidation. Rather than maintaining two parallel integrations, a team can write once and ship to both major chat surfaces, while also exposing an MCP server that agents can call. That server component matters because the MCP ecosystem increasingly assumes agents will discover and invoke tools through a shared protocol rather than custom REST endpoints. A unified framework lowers the cost of supporting both directions from one project.

What changed inside 2.10 specifically is not documented in the release notes visible here, so the newsworthy beat is that the project is actively shipping and continuing to gain traction. Developers evaluating MCP stacks now have a single framework option that covers both chat app and server deployment, and a community large enough that questions and examples tend to surface quickly.

One thing to watch: how the framework handles divergence as ChatGPT and Claude evolve their MCP implementations independently, since unified surfaces often pay for breadth with occasional lag behind platform-specific features.

[16:55] Third Moment Research Runs 10,000 Agents for 36+ Hours Straight

A research lab called Third Moment Research is keeping ten thousand AI agents running for more than thirty-six hours at a stretch, using GPT-6 Astra and GPT-6.1 Sol, Codex, and Daybreak — the last of which handles cybersecurity work. The setup, featured on OpenAI's news index in mid-October, is positioned around agents that hold their focus across days and get better the more they are used.

The headline number matters. Most production agents today finish their work in seconds or minutes; a configuration holding ten thousand concurrent agents for over a day and a half points to a different class of deployment. The fact that OpenAI is showcasing the lab's setup signals that the underlying GPT-6 family and Codex can sustain that kind of multi-day load.

The stack is layered rather than single-model. Third Moment runs GPT-6 Astra and GPT-6.1 Sol as the backbone, Codex for code and execution, and Daybreak for security tasks. The lab's framing — agents that improve with use — suggests the longer the run, the more the agents learn from their accumulated work, which is the part worth watching.

For builders, the takeaway is that long-running, multi-agent workflows have moved past demos. If a single lab can keep ten thousand agents coherent across thirty-six hours, the templates for sustained agent operations are starting to exist. Worth watching next: what those agents are actually doing across the run, and whether other labs publish comparable numbers.

[18:25] Block's security team cuts threat response to minutes with OpenAI

Block is putting OpenAI's models to work inside its security organization, and the early results are concrete: the team investigates threats faster and proposes patches in minutes. The collaboration surfaced through OpenAI News on October 14, 2026.

What changed is where the model sits in the workflow. Instead of being used for chat or summaries, OpenAI's technology is embedded in the threat investigation and remediation loop. The team still owns the decisions, but the model is helping cut the time from detection to a candidate fix. That matters because in security the gap between spotting something and acting on it is where most damage happens.

For builders and security teams, this is a useful signal. Generative models are now being trusted inside an enterprise incident response pipeline, not just at the edge as an assistant. The pattern worth borrowing is straightforward: give the model the same context your analysts see, let it propose a patch, and keep a human in the approval loop. The minutes-scale turnaround is the metric that matters, and it's the one to watch as more security organizations publish similar numbers.

[19:35] Small Vision Model Gets Draft Boost for Local AI

OpenBMB released a GGUF-quantized DSpark draft checkpoint for MiniCPM-V-4.7-1B on Hugging Face, giving local AI builders a new tool for running vision-language inference with speculative decoding. MiniCPM-V-4.7-1B is a single-billion-parameter model that handles images and text, built for on-device and edge deployment. The DSpark draft is a separate lightweight checkpoint trained to generate candidate tokens that the main model then verifies. It has 5 draft layers producing 15 tokens per forward pass, drawing from specific hidden-state layers of the target. The GGUF-quantized draft is downloadable from Hugging Face alongside the target model and vision projector for local deployment. The acceptance length metrics from the model card show the ratio of accepted tokens to verification steps, reaching 5.891x on math tasks and 4.752x on OCR benchmarks, meaning the draft predictions align closely with what the target model would have generated. This matters for local inference because speculative decoding can improve throughput even on modest hardware, since the draft handles initial token prediction and the target confirms or corrects it. Developers running llama-cli or llama-server can configure GPU offloading at maximum for both the target and draft, set a context length of 8192, and pair the Q4_K_M target with a Q8_0 draft to keep memory usage low. The draft must be paired with the matching MiniCPM-V 4.7 1B target; it requires llama.cpp with the dflash architecture and DSpark Markov head. A new Hugging Face repository published the GGUF-quantized DSpark draft checkpoint for MiniCPM-V-4.7-1B, enabling speculative decoding through llama.cpp. The DSpark draft generates 15 candidate tokens per forward pass across 5 draft layers, which the target model verifies to accelerate inference.

[21:16] GitHub Copilot to Deprecate Several Models on November 16

GitHub posted a changelog on October 15 announcing that a set of GitHub Copilot models will be retired on November 16, 2026. The deprecation applies across every Copilot surface: Copilot Chat, inline edits, ask mode, agent mode, and code completions. The practical effect is that any user who has pinned a soon-to-be-deprecated model in their Copilot settings will see it stop working on the cutoff date. Code completion, chat, and agent runs that relied on one of the affected models will need a new default after that day. The fuller list of affected models sits in the GitHub changelog post itself, alongside any suggested replacements. The deprecation hits Copilot Chat, ask mode, agent mode, inline edits, and code completions on the same day, so a Copilot user switching from inline completion to chat in the middle of a session will not save themselves by jumping surfaces. Anyone whose team has standardized on a particular model behind a Copilot plan will want to confirm that choice is still on the supported list before November.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: Hermes Agent v0.22.2, v0.22.1, v0.22.0, v0.21.7 / Reflection's Beam 1.0 lists on OpenRouter as a 501B coding MoE / Apple MLX Runs Near-Trillion Parameter Muse Spark Open on Mac Studio Cluster
- 02:00 — Agent Stack Release Readout: Hermes Agent v0.22.2, v0.22.1, v0.22.0, v0.21.7
- 03:47 — Reflection's Beam 1.0 lists on OpenRouter as a 501B coding MoE
- 04:38 — Apple MLX Runs Near-Trillion Parameter Muse Spark Open on Mac Studio Cluster
- 06:22 — Open-source 3D architectural editor ships CLI and MCP tools for AI agents
- 07:37 — MiniCPM-V 4.7 Gets a Speed Boost via Speculative Decoding
- 09:24 — NVIDIA Expands Nemotron Family with Super VL and Bolt Edge Models
- 11:17 — Research digest: Four AI Agents Beat Minecraft's Ender Dragon Together
- 12:21 — Grok Voice 3.0 Tops Speech-to-Speech Index at the Same $0.08 a Minute
- 13:52 — xAI's $30 Bundle Puts Grok Models Inside Cursor
- 15:29 — mcp-use 2.10 lands for a fullstack MCP framework covering ChatGPT, Claude, and agent servers
- 16:55 — Third Moment Research Runs 10,000 Agents for 36+ Hours Straight
- 18:25 — Block's security team cuts threat response to minutes with OpenAI
- 19:35 — Small Vision Model Gets Draft Boost for Local AI
- 21:16 — GitHub Copilot to Deprecate Several Models on November 16

---

## Primary Links

- Hermes Agent v0.22.2 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.2
- Hermes Agent v0.22.1 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.1
- Hermes Agent v0.22.0 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.0
- Hermes Agent v0.21.7 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.21.7
- Reflection: Beam 1.0 501B A23B model page: https://openrouter.ai/models/reflection/beam-1.0-501b-a23b
- Apple ML Research: Muse Spark Open with MLX on Mac Studio: https://machinelearning.apple.com/research/mlx-distributed-inference
- pascalorg/editor — Open-source 3D architectural editor with a local CL: https://github.com/pascalorg/editor
- openbmb/MiniCPM-V-4.7-35B-A3B-DSpark-gguf model repository on Hugging : https://huggingface.co/openbmb/MiniCPM-V-4.7-35B-A3B-DSpark-gguf
- Open From Data Center to Desktop: NVIDIA Expands Nemotron Family With : https://blogs.nvidia.com/blog/nemotron-3-5-super-vl/
- A team of Gemini 4 Argon agents beats Minecraft: https://arxiv.org/abs/2610.22319
- Introducing Grok Voice 3.0: https://x.ai/news/grok-voice-3
- Introducing The X Subscription: https://x.ai/news/x-subscription
- mcp-use/mcp-use — The fullstack MCP framework to develop MCP Apps for : https://github.com/mcp-use/mcp-use
- How Third Moment Research runs 10,000 agents for 36+ hours: https://openai.com/index/third-moment-research
- How Block is building AI-powered security with OpenAI technology: https://openai.com/index/block-ai-powered-security
- openbmb/MiniCPM-V-4.7-1B-DSpark-gguf model repository on Hugging Face: https://huggingface.co/openbmb/MiniCPM-V-4.7-1B-DSpark-gguf
- Upcoming deprecation of selected GitHub Copilot models in mid-November: https://github.blog/changelog/2026-10-15-upcoming-deprecation-of-selected-github-copilot-models-in-mid-november
- HKUDS/nanobot repo: https://github.com/HKUDS/nanobot
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- ahujasid/mcp-for-blender repo: https://github.com/ahujasid/mcp-for-blender
- PrefectHQ/fastmcp — 🚀 The fast, Pythonic way to build MCP servers and : https://github.com/PrefectHQ/fastmcp
- microsoft/mcp-for-beginners — This open-source curriculum introduces t: https://github.com/microsoft/mcp-for-beginners
- jialinyyzz/humanizer: https://huggingface.co/jialinyyzz/humanizer

---

## Release Coverage Check

- **Hermes Agent** — Latest stable verified: `v0.22.2`, published 2026-10-15T08:21:32Z. Recent episode version tags detected: `v2026.9.14`, `v2026.9.21`, `v2026.9.24`, `v2026.9.7`. Selected missing version(s): `v0.22.2`, `v0.22.1`, `v0.22.0`, `v0.21.7`.
- **OpenAI Codex** — Latest stable verified: `rust-v0.163.0`, published 2026-10-15T21:30:38Z. Recent episode version tags detected: `rust-v0.159.3`, `rust-v0.160.0`, `rust-v0.161.0`, `rust-v0.162.0`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.292`, published 2026-10-06T17:10:31.715Z. Recent episode version tags detected: `2.1.285`, `2.1.286`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-10-16). Recent episode version tags detected: `@google/antigravity`, `v2.0`.

---

## Harness Version Reference

- **Hermes Agent** — `v0.22.2`
- **OpenAI Codex** — `rust-v0.163.0`
- **Claude Code CLI** — `2.1.292`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)


---

## Featured Story Plan

- Story 5: **MiniCPM-V 4.7 Gets a Speed Boost via Speculative Decoding** — prioritize its source-backed capability, comparison when documented, limitations, and practical consequence; no word quota.
- Story 13: **Small Vision Model Gets Draft Boost for Local AI** — prioritize its source-backed capability, comparison when documented, limitations, and practical consequence; no word quota.

---

## Research Evidence Contract

```json
{
  "policy_version": 1,
  "featured_stories": [
    5,
    13
  ],
  "records": [
    {
      "story": 1,
      "title": "Agent Stack Release Readout: Hermes Agent v0.22.2, v0.22.1, v0.22.0, v0.21.7",
      "source_sha256": "145ab8e49c6b216174651a1cfcfeca07eb0e5a5395b112d0cfa864368ac2d13a",
      "source_url": "https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.2",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 2,
      "title": "Reflection's Beam 1.0 lists on OpenRouter as a 501B coding MoE",
      "source_sha256": "0bbf9cba349ee141ae1acf7657c4e7f7d2c45752b97b39bbae10aec99f26cbf5",
      "source_url": "https://openrouter.ai/models/reflection/beam-1.0-501b-a23b",
      "model_story": true,
      "model_review": {
        "release_status": "registry_listing",
        "evidence_type": "registry_listing",
        "release_quote": "This model is listed by OpenRouter at https://openrouter.ai/models/reflection/beam-1.0-501b-a23b.",
        "release_span": "S003",
        "change": {
          "status": "supported",
          "claim": "A new open-weight reasoning model from Reflection called Beam 1.0 has surfaced on OpenRouter as a model listing.",
          "quote": "Beam 1.0 is Reflection's open-weight reasoning model for coding and long-horizon agentic workflows.\nThis model is listed by OpenRouter at https://openrouter.ai/models/reflection/beam-1.0-501b-a23b.",
          "source_span": [
            "S001",
            "S003"
          ],
          "quotes": [
            "Beam 1.0 is Reflection's open-weight reasoning model for coding and long-horizon agentic workflows.",
            "This model is listed by OpenRouter at https://openrouter.ai/models/reflection/beam-1.0-501b-a23b."
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "It is a sparse mixture-of-experts model with 501 billion total parameters and 23 billion active per token, a one-million-token context window, and is positioned for coding and long-horizon agentic workflows.",
          "quote": "Beam 1.0 is Reflection's open-weight reasoning model for coding and long-horizon agentic workflows.\nIt uses a sparse mixture-of-experts architecture with 501B total and 23B active parameters per token, and a...\nContext length: 1048576 tokens.",
          "source_span": [
            "S001",
            "S002",
            "S004"
          ],
          "quotes": [
            "Beam 1.0 is Reflection's open-weight reasoning model for coding and long-horizon agentic workflows.",
            "It uses a sparse mixture-of-experts architecture with 501B total and 23B active parameters per token, and a...",
            "Context length: 1048576 tokens."
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
          "claim": "The model is listed on OpenRouter under the identifier reflection/beam-1.0-501b-a23b.",
          "quote": "This model is listed by OpenRouter at https://openrouter.ai/models/reflection/beam-1.0-501b-a23b.",
          "source_span": [
            "S003"
          ],
          "quotes": [
            "This model is listed by OpenRouter at https://openrouter.ai/models/reflection/beam-1.0-501b-a23b."
          ]
        }
      }
    },
    {
      "story": 3,
      "title": "Apple MLX Runs Near-Trillion Parameter Muse Spark Open on Mac Studio Cluster",
      "source_sha256": "ca1f7398b041da83ee7e1bd68791b7cf27337fa2b8219401fca8a553c9534af2",
      "source_url": "https://machinelearning.apple.com/research/mlx-distributed-inference",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 4,
      "title": "Open-source 3D architectural editor ships CLI and MCP tools for AI agents",
      "source_sha256": "6ddd826cd08e9c82d7a26cc5d4f876fb3d90709efe4d2ec88c1a7787237a0433",
      "source_url": "https://github.com/pascalorg/editor",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 5,
      "title": "MiniCPM-V 4.7 Gets a Speed Boost via Speculative Decoding",
      "source_sha256": "bed992bbd377e8c3424a2d33893594dd5d6ec4f899af537c9ff0f736fd59895d",
      "source_url": "https://huggingface.co/openbmb/MiniCPM-V-4.7-35B-A3B-DSpark-gguf",
      "model_story": true,
      "model_review": {
        "release_status": "registry_listing",
        "evidence_type": "publisher_report",
        "release_quote": "",
        "release_span": "",
        "change": {
          "status": "supported",
          "claim": "OpenBMB published a GGUF-quantized DSpark draft checkpoint for MiniCPM-V 4.7 on Hugging Face, enabling speculative decoding with llama.cpp.",
          "quote": "---\nlicense: apache-2.0\nlanguage:\nen\nzh\nlibrary_name: transformers\npipeline_tag: text-generation\ntags:\nminicpmv\nminicpmv4.7\ntext-generation\nvision-understanding\ntool-calling\non-device\nedge-ai\nbase_model: openbmb/MiniCPM-V-4.7-35B-A3B-DSpark\nbase_model_relation: quantized\n---\nThis repository hosts the GGUF (llama.cpp) quantized version of MiniCPM-V-4.7-35B-A3B-DSpark.",
          "source_span": [
            "S001"
          ],
          "quotes": [
            "---\nlicense: apache-2.0\nlanguage:\nen\nzh\nlibrary_name: transformers\npipeline_tag: text-generation\ntags:\nminicpmv\nminicpmv4.7\ntext-generation\nvision-understanding\ntool-calling\non-device\nedge-ai\nbase_model: openbmb/MiniCPM-V-4.7-35B-A3B-DSpark\nbase_model_relation: quantized\n---\nThis repository hosts the GGUF (llama.cpp) quantized version of MiniCPM-V-4.7-35B-A3B-DSpark."
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "The draft model predicts 15 tokens per forward pass, and benchmarks show publisher-reported averages of 3.501 accepted tokens per verification step on general text and 7.387 on code generation.",
          "quote": "| Property                      | Value                                                                         |\n| ----------------------------- | ----------------------------------------------------------------------------- |\n| Target model                  | MiniCPM-V-4.7-35B-A3B |\n| Draft layers                  | 5                                                                             |\n| Draft parameters              | 389,223,169                                                                   |\n| Draft tokens per forward pass | 15                                                                            |\n| Target hidden-state layers    | [3, 11, 19, 27, 35]                                                         |\n| Checkpoint precision          | BF16                                                                          |\nTraining Recipe\n| Domain            | Accept Length | \n| --------------------- | ----------------- |\n| Vision            |                   |\n| MMMU                  | 5.098             |\n| MathVista             | 6.126             |\n| CharXiv_reasoning_val | 5.479             |\n| OCRBench              | 5.407             |\n| Text              |                   |\n| Math                  | 6.687             |\n| Code                  | 7.387             |\n| General               | 3.501             |\nUsage with llama.cpp",
          "source_span": [
            "S004",
            "S009"
          ],
          "quotes": [
            "| Property                      | Value                                                                         |\n| ----------------------------- | ----------------------------------------------------------------------------- |\n| Target model                  | MiniCPM-V-4.7-35B-A3B |\n| Draft layers                  | 5                                                                             |\n| Draft parameters              | 389,223,169                                                                   |\n| Draft tokens per forward pass | 15                                                                            |\n| Target hidden-state layers    | [3, 11, 19, 27, 35]                                                         |\n| Checkpoint precision          | BF16                                                                          |\nTraining Recipe",
            "| Domain            | Accept Length | \n| --------------------- | ----------------- |\n| Vision            |                   |\n| MMMU                  | 5.098             |\n| MathVista             | 6.126             |\n| CharXiv_reasoning_val | 5.479             |\n| OCRBench              | 5.407             |\n| Text              |                   |\n| Math                  | 6.687             |\n| Code                  | 7.387             |\n| General               | 3.501             |\nUsage with llama.cpp"
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
          "claim": "The quantized draft runs with llama-cli or llama-server using the --spec-type draft-dspark flag, requiring a llama.cpp build with dflash architecture.",
          "quote": "Run with speculative decoding (-md = draft, --spec-type draft-dspark). llama-cli handles both the vision projector and the draft:\nRequires a llama.cpp build with the dflash architecture and the DSpark Markov head.",
          "source_span": [
            "S012",
            "S016"
          ],
          "quotes": [
            "Run with speculative decoding (-md = draft, --spec-type draft-dspark). llama-cli handles both the vision projector and the draft:",
            "Requires a llama.cpp build with the dflash architecture and the DSpark Markov head."
          ]
        }
      }
    },
    {
      "story": 6,
      "title": "NVIDIA Expands Nemotron Family with Super VL and Bolt Edge Models",
      "source_sha256": "cedc3b30761cf25d0366d652742217929b1993368c8026b0d71fe1ff4dd15e19",
      "source_url": "https://blogs.nvidia.com/blog/nemotron-3-5-super-vl/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 7,
      "title": "Research digest: Four AI Agents Beat Minecraft's Ender Dragon Together",
      "source_sha256": "c05f2f7c8d1120fa0e88338609bd17804043590752176c8fc95c7eda145bccd6",
      "source_url": "https://arxiv.org/abs/2610.22319",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 8,
      "title": "Grok Voice 3.0 Tops Speech-to-Speech Index at the Same $0.08 a Minute",
      "source_sha256": "7516afe7fe02aa1f9002595df9e726158cac857460eeb5929f84428474821d90",
      "source_url": "https://x.ai/news/grok-voice-3",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 9,
      "title": "xAI's $30 Bundle Puts Grok Models Inside Cursor",
      "source_sha256": "d267210e3958a7214f82bd21bdcfaf1f24b6ff8b64e5fc26f4445e1c803ab4fc",
      "source_url": "https://x.ai/news/x-subscription",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 10,
      "title": "mcp-use 2.10 lands for a fullstack MCP framework covering ChatGPT, Claude, and agent servers",
      "source_sha256": "be5418d47d41ffbe6a2e0be779eaa9c4eb1e3ddbdfa0083e2fea90319b6d9595",
      "source_url": "https://github.com/mcp-use/mcp-use",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 11,
      "title": "Third Moment Research Runs 10,000 Agents for 36+ Hours Straight",
      "source_sha256": "5e3e04f60bd99f0450249e95eb3b9e4e2657358e7f95dbcb004902845f9e17a7",
      "source_url": "https://openai.com/index/third-moment-research",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 12,
      "title": "Block's security team cuts threat response to minutes with OpenAI",
      "source_sha256": "0888566faedb947bda720d7def4e593e1164018b327a59875ff91b3c0c9a6376",
      "source_url": "https://openai.com/index/block-ai-powered-security",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 13,
      "title": "Small Vision Model Gets Draft Boost for Local AI",
      "source_sha256": "b548552901362f631f699f6c56cec328c8ffcc318c80ff3eeb18f2f6953da31c",
      "source_url": "https://huggingface.co/openbmb/MiniCPM-V-4.7-1B-DSpark-gguf",
      "model_story": true,
      "model_review": {
        "release_status": "registry_listing",
        "evidence_type": "publisher_report",
        "release_quote": "---\nlicense: apache-2.0\nlanguage:\nen\nzh\nlibrary_name: transformers\npipeline_tag: text-generation\ntags:\nminicpmv\nminicpmv4.7\ntext-generation\nvision-understanding\ntool-calling\non-device\nedge-ai\nbase_model: openbmb/MiniCPM-V-4.7-1B-DSpark\nbase_model_relation: quantized\n---\nThis repository hosts the GGUF (llama.cpp) quantized version of MiniCPM-V-4.7-1B-DSpark.",
        "release_span": "S001",
        "change": {
          "status": "supported",
          "claim": "A new Hugging Face repository published the GGUF-quantized DSpark draft checkpoint for MiniCPM-V-4.7-1B, enabling speculative decoding through llama.cpp.",
          "quote": "---\nlicense: apache-2.0\nlanguage:\nen\nzh\nlibrary_name: transformers\npipeline_tag: text-generation\ntags:\nminicpmv\nminicpmv4.7\ntext-generation\nvision-understanding\ntool-calling\non-device\nedge-ai\nbase_model: openbmb/MiniCPM-V-4.7-1B-DSpark\nbase_model_relation: quantized\n---\nThis repository hosts the GGUF (llama.cpp) quantized version of MiniCPM-V-4.7-1B-DSpark.",
          "source_span": [
            "S001"
          ],
          "quotes": [
            "---\nlicense: apache-2.0\nlanguage:\nen\nzh\nlibrary_name: transformers\npipeline_tag: text-generation\ntags:\nminicpmv\nminicpmv4.7\ntext-generation\nvision-understanding\ntool-calling\non-device\nedge-ai\nbase_model: openbmb/MiniCPM-V-4.7-1B-DSpark\nbase_model_relation: quantized\n---\nThis repository hosts the GGUF (llama.cpp) quantized version of MiniCPM-V-4.7-1B-DSpark."
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "The DSpark draft generates 15 candidate tokens per forward pass across 5 draft layers, which the target model verifies to accelerate inference.",
          "quote": "| Property | Value |\n|---|---|\n| Target model | MiniCPM-V-4.7-1B |\n| Draft layers | 5 |\n| Draft parameters | 213,547,777 |\n| Draft tokens per forward pass | 15 |\n| Target hidden-state layers | [3, 7, 11, 15, 19] |\n| Checkpoint precision | BF16 |\nTraining Recipe",
          "source_span": [
            "S004"
          ],
          "quotes": [
            "| Property | Value |\n|---|---|\n| Target model | MiniCPM-V-4.7-1B |\n| Draft layers | 5 |\n| Draft parameters | 213,547,777 |\n| Draft tokens per forward pass | 15 |\n| Target hidden-state layers | [3, 7, 11, 15, 19] |\n| Checkpoint precision | BF16 |\nTraining Recipe"
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
          "claim": "The draft must be paired with the matching MiniCPM-V 4.7 1B target; it requires llama.cpp with the dflash architecture and DSpark Markov head.",
          "quote": "Requires a llama.cpp build with the dflash architecture and the DSpark Markov head.\nThe draft must be paired with the matching MiniCPM-V 4.7 1B target.",
          "source_span": [
            "S016",
            "S017"
          ],
          "quotes": [
            "Requires a llama.cpp build with the dflash architecture and the DSpark Markov head.",
            "The draft must be paired with the matching MiniCPM-V 4.7 1B target."
          ]
        },
        "access": {
          "status": "supported",
          "claim": "The GGUF-quantized draft is downloadable from Hugging Face alongside the target model and vision projector for local deployment.",
          "quote": "Download the target model, its vision projector (mmproj), and this DSpark draft:\nbash\nhuggingface-cli download openbmb/MiniCPM-V-4.7-1B-gguf MiniCPM-V-4_7-1B-Q4_K_M.gguf mmproj-model-f16.gguf --local-dir ./1B-gguf\nhuggingface-cli download openbmb/MiniCPM-V-4.7-1B-DSpark-gguf dspark-MiniCPM-V-4_7-1B-Q8_0.gguf --local-dir ./1B-gguf",
          "source_span": [
            "S010",
            "S011"
          ],
          "quotes": [
            "Download the target model, its vision projector (mmproj), and this DSpark draft:",
            "bash\nhuggingface-cli download openbmb/MiniCPM-V-4.7-1B-gguf MiniCPM-V-4_7-1B-Q4_K_M.gguf mmproj-model-f16.gguf --local-dir ./1B-gguf\nhuggingface-cli download openbmb/MiniCPM-V-4.7-1B-DSpark-gguf dspark-MiniCPM-V-4_7-1B-Q8_0.gguf --local-dir ./1B-gguf"
          ]
        }
      }
    },
    {
      "story": 14,
      "title": "GitHub Copilot to Deprecate Several Models on November 16",
      "source_sha256": "ed6aa247c1a47eded9b8ea2633bbc2950920892a399dfccb97261e91ea2e9261",
      "source_url": "https://github.blog/changelog/2026-10-15-upcoming-deprecation-of-selected-github-copilot-models-in-mid-november",
      "model_story": false,
      "model_review": null
    }
  ]
}
```
