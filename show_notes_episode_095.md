# AgentStack Daily EP095 — Agent Stack Release Readout: OpenAI Code, GitHub Copilot for JetBrains adds OpenTe, Two GPT-5.6 Settings That Tripled Its AR

**Title:** AgentStack Daily: Agent Stack Release Readout: OpenAI Codex rust-v0.146.0

**Tagline:** Today's stories: Agent Stack Release Readout: OpenAI Codex rust-v0.146.0, GitHub Copilot for JetBrains adds OpenTelemetry controls and model management, Two GPT-5.6 Settings That Tripled Its ARC-AGI-3 Score, and Liquid AI ships two CPU-friendly long-context encoders. Concrete changes across the agent stack — what shipped, the mechanisms underneath, and what each one means for builders working with coding agents, models, and tooling.

**Feed description:** Agent Stack Release Readout: OpenAI Codex rust-v0.146.0, GitHub Copilot for JetBrains adds OpenTelemetry controls and model management, Two GPT-5.6 Settings That Tripled Its ARC-AGI-3 Score, and Liquid AI ships two CPU-friendly long-context encoders. What shipped, how the mechanisms work, and what each change means for agent builders.

---

## Story Slate

1. **Agent Stack Release Readout: OpenAI Codex rust-v0.146.0**
OpenAI shipped Codex rust-v0.146.0 on July 29, 2026, a CLI release that adds named and pinned sessions, support for Agent Plugins manifests with new marketplaces for Amazon Bedrock and Claude Code, forkable threads with paginated history, and a WebSocket bridge from app-server to remote Code Mode hosts. Custom model providers can now run standalone web search, executor-provided skills can be discovered and read securely, and a long list of proxy, MCP, and terminal fixes clean up day-to-day friction.
Technical depth angle: The WebSocket bridge from app-server to remote Code Mode hosts is the standout mechanism — a local Codex client can drive tools, plugins, and approvals on a separate machine without giving up the same surface area. Agent Plugins manifests plus Bedrock and Claude Code marketplaces let one package definition travel across runtimes instead of being rewritten per host.
Actionability angle: For builders running Codex against remote workstations, this release lets a local CLI orchestrate tools and plugins hosted elsewhere over WebSocket, which removes the need for hand-rolled bridges. Teams standardizing on plugin manifests can publish once and distribute across Bedrock and Claude Code marketplaces instead of maintaining separate packages per host. What this matters: fewer one-off integrations, and a clearer path to multi-host workflows.
Listener hook: If you've been wiring Codex into Bedrock or Claude Code by hand, this release hands you shared plugin manifests and a real WebSocket bridge to remote hosts.

2. **GitHub Copilot for JetBrains adds OpenTelemetry controls and model management**
GitHub shipped an update to its Copilot plugin for JetBrains IDEs that gives developers more control and clarity over telemetry configuration and model management. The release enables connecting MCP servers and custom agents inside Claude agent flows, so teams can extend what their AI assistant reaches during a coding session. Together the changes make Copilot's behavior more configurable and more extensible in environments where internal tool access matters.
Technical depth angle: OpenTelemetry is the open standard for shipping app telemetry — logs, traces, and metrics — out to whatever observability stack a team uses. Model management gives a clearer handle on which AI models are wired into the JetBrains plugin. MCP (Model Context Protocol) is Anthropic's open standard for letting an AI agent call external tools and data through a uniform interface.
Actionability angle: For JetBrains users running Copilot, the practical implication is that telemetry can now be tuned to fit existing observability pipelines rather than working around defaults, and any internal tool that already exposes an MCP endpoint becomes reachable from a Claude agent flow without bespoke glue code. This matters most for teams with audit or cost-tracking needs around AI usage data.
Listener hook: If your team runs JetBrains and cares about where your AI telemetry actually goes, this is the update worth a closer look.

3. **Two GPT-5.6 Settings That Tripled Its ARC-AGI-3 Score**
OpenAI shared on July 29 that flipping two API settings tripled GPT-5.6's score on the ARC-AGI-3 benchmark while also improving efficiency. The two settings were retaining reasoning across turns and enabling compaction to summarize older context. The result is a model that solves more puzzle-style reasoning tasks with fewer tokens, achieved through configuration rather than retraining or a new release.
Technical depth angle: Retaining reasoning keeps the model's working thoughts persistent between turns instead of starting fresh, while compaction summarizes older reasoning context to keep token use manageable. Together they let GPT-5.6 build on earlier insights without ballooning cost.
Actionability angle: What this means for builders: a simple API config change, not a new model or retraining, unlocked substantially better performance on hard reasoning work. Why this matters: the gap between default and tuned GPT-5.6 looks large enough that any production reasoning workflow is worth testing with these two settings enabled.
Listener hook: Two checkboxes in OpenAI's API tripled GPT-5.6's hardest-puzzle score — here's what they actually did.

4. **Liquid AI ships two CPU-friendly long-context encoders**
Liquid AI released two open-weight encoder models, the LFM2.5 family at 230 million and 350 million parameters, designed to run long inputs directly on CPUs. The models carry an 8,192-token context window and were converted from causal decoder backbones into bidirectional encoders using bidirectional attention, symmetric non-causal short convolutions, and masked-language training. Liquid AI says the 230-million-parameter model finishes an 8,192-token forward pass on CPU in roughly 28 seconds, about 3.7 times faster than ModernBERT-base in its own benchmark. The company is positioning them for classification, routing, policy linting, and personal-data detection tasks where running on commodity hardware matters.
Technical depth angle: The key move is converting standard causal decoder backbones into bidirectional encoders. Liquid AI replaces one-directional attention with full bidirectional attention, swaps causal short convolutions for symmetric non-causal ones, and retrains with a masked-language objective. That combination is what unlocks an 8,192-token context window on CPU at the speed Liquid AI reports, without needing a GPU.
Actionability angle: Builders who run text classification or routing on commodity hardware now have an open-weight encoder that handles long inputs without a GPU. The CPU-friendly speed profile means a single box can score documents, detect personal data, or lint policies against a large context. It widens the menu of fully local, GPU-free stacks for production text pipelines.
Listener hook: If you've been wanting long-context encoders you can actually run on a laptop or a cheap server, Liquid AI just shipped two.

5. **ComfyUI 0.29.0 streams video instead of buffering it in RAM**
ComfyUI, the open-source node-based interface for running local image and video generation workflows, shipped version 0.29.0 on July 29. The standout fix moves video transcoding off in-memory buffering, so frames no longer pile up in RAM as they are processed. A second change sends the ComfyUI Job Id as a request header to partner nodes, giving external services a clean way to correlate work coming out of a workflow.
Technical depth angle: The video fix replaces a frame-buffering transcode with a streamed transcode. That matters for any workflow producing longer or higher-resolution clips, because buffered video pipelines hit a RAM ceiling fast. The partner-nodes header change is a correlation move: it lets partner services tie a request back to the originating ComfyUI job without guesswork.
Actionability angle: For builders running long video jobs locally, this should reduce the chance that a render blows past available RAM before finishing. The job-ID header is most useful to anyone integrating a partner service that needs to track which output belongs to which run.
Listener hook: If you have ever watched a long ComfyUI video job die because your machine ran out of memory, this release is aimed at exactly that.

6. **NVIDIA Jetson Gets a Venture Capitalist’s Bag Endorsement**
Sarah Guo, founder of AI-focused venture firm Conviction and co-host of the No Priors podcast, highlighted NVIDIA’s Jetson platform in a recent video as a compact way to run AI outside the data center. The pitch — “powerful compute so compact, it’s clutch” — frames the edge-AI kit as a portable rig for builders. NVIDIA published the feature on July 28, 2026, leaning on Guo’s endorsement rather than a new product announcement.
Technical depth angle: Jetson is NVIDIA’s edge AI platform — a small, self-contained computer built around the company’s GPU-style accelerator, designed to run models locally instead of in a data center.
Actionability angle: This matters if you want to build or demo AI in places where cloud connectivity is awkward — a kiosk, a robot, a factory floor, or a pop-up booth. Edge kits keep latency low and data local, but you’re working within the hardware ceiling of a compact machine rather than a server cluster. Worth checking whether an actual Jetson refresh or new developer kit lands to back the “clutch” pitch.
Listener hook: A VC’s pick for the season’s must-carry tech isn’t a new fund — it’s a pocketable AI box.

7. **Intel’s U.S. Advanced Packaging Enables Next-Generation AI Semiconductors**
As AI demands unprecedented "brain power," the semiconductor industry is moving past the era of relying on single, massive chips. Advanced packaging is the essential craft of interconnecting multiple specialized chips together. This allows them to function as a single, powerful unit that runs faster handling the massive workloads of the future.Intel&#8217;s been doing advanced &#8230; The post Intel’s U.S. Advanced Packaging Enables Next-Generation AI Semiconductors appeared first on Newsroom.
Technical depth angle: The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment.
Actionability angle: Test the sourced change against one real workflow before depending on it.
Listener hook: The practical question is what this changes for a builder today.

8. **FCC Adds Foreign-Made Advanced Robots to Its Covered List**
On July 28, the FCC's Public Safety and Homeland Security Bureau added foreign-produced advanced robotic devices to its Covered List, following an Executive Branch interagency determination citing supply-chain, cybersecurity, surveillance, and remote-control risks. Covered devices cannot receive FCC equipment authorization, though a device or class can win conditional approval from the Department of War if it is judged not to pose those risks. The action is a category-based restriction keyed to place of production, not a named-company ban.
Technical depth angle: The Covered List blocks FCC equipment authorization, the regulatory permission US devices need to legally use radio spectrum. Because the rule targets production geography rather than specific manufacturers, any foreign-built advanced robot is presumptively barred unless the Department of War grants a conditional exception.
Actionability angle: For builders and importers of advanced robots, this is a new regulatory gate: foreign-produced devices cannot reach US authorization without a Department of War conditional approval. Watch for the first waiver decisions and any clarifying definition of "advanced robotic devices," because the practical scope lives in those details.
Listener hook: If you're bringing an advanced robot to market in the US and it's built overseas, the FCC just became a much bigger hurdle.

9. **Research digest: Robot Training Without the Robot: Better Capture May Replace the Real-Hardware Anchor**
A new paper called HiFi-UMI tackles a stubborn problem in robot manipulation learning: teaching robots real tasks requires lots of high-quality demonstration data, which is expensive to collect. Today's workaround is to use cheap, robot-free UMI capture data for pre-training and then add a small dose of real-robot demonstrations at the end. The authors ask whether pushing the fidelity of the robot-free data alone could eliminate that final real-robot step, and present HiFi-UMI as their answer — a portable capture setup aimed at higher-fidelity data without the robot.
Technical depth angle: The paper reframes the data scarcity problem in manipulation learning as a fidelity gap rather than a scale gap. Instead of accepting that robot-free UMI capture is too noisy and patching it with real-robot teleoperation at post-training, HiFi-UMI argues that better fidelity in the cheap, scalable capture pipeline is enough to train deployable policies end-to-end on that data alone.
Actionability angle: For robotics researchers, this suggests the binding constraint in learning manipulation policies may be data fidelity tooling rather than total demonstration volume. It also means labs without large real-robot fleets might get a cheaper on-ramp to deployable policies, if the high-fidelity-only claim holds up in replication.
Listener hook: If you've ever wondered why teaching a robot arm is so expensive, this paper argues the missing piece isn't more demos — it's better ones.

10. **Research digest: TurboVLA paper cuts robot-control compute to under 1 GB**
A trending paper on HuggingFace called TurboVLA proposes a leaner way to run vision-language-action models — the AI systems that turn camera views and instructions into robot motion. Instead of routing every frame through a large language model first, it fuses vision and language cues directly into the action output. The result is real-time robot control on a single consumer RTX 4090 graphics card while using under one gigabyte of video memory.
Technical depth angle: TurboVLA replaces the conventional V→L→A pathway — where every visual frame passes through a large language model's representation space — with a direct V+L→A mapping that combines vision and language cues straight into the action output. This sidesteps the per-invocation computational and memory cost of pushing pixels through a full LLM at every robot step. Concretely: 32 Hz control on a single RTX 4090 using less than 1 GB of video memory.
Actionability angle: What this means for builders: faster robot control loops become feasible on affordable, off-the-shelf hardware rather than multi-GPU server setups. Hobby robotics groups and small labs can prototype reactive manipulation without provisioning data-center compute. The open question is generalization — whether the simplified pathway keeps working on messier, less-scripted real-world tasks.
Listener hook: Most robot-control AIs need a small supercomputer; this week's trending paper shows one running at 32 Hz on a single consumer GPU with almost no memory budget.

11. **HKUDS nanobot ships v0.3.0 as a lightweight self-hosted agent framework**
HKUDS has shipped nanobot v0.3.0, an open-source Python framework for building self-hosted personal AI agents. The project now sits at 46,404 GitHub stars and bundles a WebUI, tool calling, memory, MCP support, multi-agent workflows, automation hooks, and chat app connectors into a lightweight package. The latest release landed July 25, with the repository pushed again on July 30. It targets developers who want to run their own agent setup without heavier hosted platforms.
Technical depth angle: Nanobot packages MCP integration, memory, multi-agent workflow primitives, and chat connectors into a single Python project. The MCP layer matters because it lets the agent talk to the same tool ecosystem that many hosted agent stacks already use, which makes swapping in self-hosted tooling more practical.
Actionability angle: What this means: developers who want a self-hosted agent setup with a WebUI, MCP support, and chat connectors can clone the repo and run it themselves rather than rely on a hosted platform. Why this matters: at 46,404 GitHub stars and a fresh release, the project has community traction worth evaluating against your current stack.
Listener hook: If you've wanted to run your own agent setup without a hosted platform, nanobot just hit a fresh release worth a look.

12. **GPT-5.6 is framed as an efficiency release, not a capability one**
OpenAI posted on July 29, 2026 framing GPT-5.6 around efficiency gains spanning models, inference, and agentic workflows, with the pitch being more useful output per dollar. The post carries no public changelog, no benchmark tables, no feature list, and no concrete API or pricing detail, so builders have nothing concrete to act on yet.
Technical depth angle: The release framing ties three areas together — model efficiency, inference efficiency, and agentic workflow throughput — without spelling out which mechanisms moved or by how much.
Actionability angle: This is positioning language rather than a feature drop, so there is nothing to integrate today. It matters because anyone running production agents will want to wait for the real cost and throughput numbers before tuning their stacks.
Listener hook: If you build on OpenAI and you care about cost per task, this is the announcement to watch for real numbers.

13. **OpenAI Grants Free ChatGPT Access to 100,000 Academic Researchers**
OpenAI announced on July 29, 2026 that it is giving 100,000 academic researchers free access to ChatGPT's most advanced AI models. The stated goal is accelerating scientific research, collaboration, and discovery across the academic community. The announcement does not name specific models, explain eligibility, or detail how access will be distributed, leaving the practical shape of the program unclear for now.
Technical depth angle: The announcement references 'ChatGPT's most advanced AI models' without naming any specific model, version, or capability. No changelog, system specifications, or feature list is provided — only the headline figure, the audience, and the stated mission.
Actionability angle: For academic researchers, this means a chance at free access to top-tier ChatGPT models if they land one of the 100,000 slots. The announcement carries no signup details, eligibility criteria, or timeline yet, so the operational shape of the program is still to come.
Listener hook: OpenAI is handing free top-tier ChatGPT access to 100,000 researchers — a move that could quietly reshape how labs draft, review, and discover.

14. **OlmoEarth Platform brings geospatial inference to planetary scale**
AllenAI published a Hugging Face Blog post on July 28, 2026, titled "The OlmoEarth Platform: Geospatial inference at planetary scale." The headline signals a new infrastructure layer for running geospatial inference over planet-sized datasets. Beyond the title, the source material does not provide a changelog, model card, or concrete release notes, so the specifics of what is available to builders today remain thin on the public page.
Technical depth angle: The headline points to a platform framing rather than a single model: geospatial inference implies the system reads geographic and remote-sensing data and produces predictions over large areas, with "planetary scale" suggesting the compute and data pipeline are designed to handle Earth-wide coverage rather than single scenes.
Actionability angle: What this means: a planetary-scale geospatial inference platform is the kind of infrastructure that could let teams run Earth-observation models against continent-sized datasets without stitching together their own pipelines. Why this matters for builders: until AllenAI publishes more details, this is worth bookmarking but not yet something to integrate against.
Listener hook: AllenAI just put a name on planetary-scale geospatial inference — here's what the headline tells us and what it doesn't.

---

## Editorial Mix Check

- flagship_products: 6
- builder_projects: 5
- local_ai: 2
- hardware_compute: 2
- policy_regulation: 1
- research: 2

---

## Model Discovery Check

- **Model lanes scanned** (OpenRouter major providers) — No new or materially updated models detected this cycle (verified July 30, 2026). Primary source: https://openrouter.ai/models. Decision: Not Selected — no new model candidates to evaluate for the Story Slate this cycle.

---

## Local LLM Spotlight

- **moonshotai/Kimi-K3** — https://huggingface.co/moonshotai/Kimi-K3 — Trending open model on Hugging Face; task image-text-to-text; 8822 likes and 387822 downloads. Tags: transformers, safetensors, kimi_k3, feature-extraction, compressed-tensors, conversational, image-text-to-text, custom_code, license:other, eval-results.
  Try now: Read the linked model card before downloading, and choose a runtime or device only after it confirms the license, weight format, context window, benchmarks, and hardware requirements.

---

## GitHub Project Radar

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — High-performance code intelligence MCP server. Indexes codebases into a persistent knowledge graph — average repo in milliseconds. 158 languages, sub-ms queries, 99% fewer tokens. Single static binary `stars: 36,548`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v0.9.0 (2026-07-08)`.
  Why this is on the radar now: v0.9.0 shipped on 2026-07-08 and the repository was updated on 2026-07-30.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — 🚀 The fast, Pythonic way to build MCP servers and clients. `stars: 26,966`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: v3.4.5 (2026-07-27)`.
  Why this is on the radar now: v3.4.5 shipped on 2026-07-27 and the repository was updated on 2026-07-29.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

- **microsoft/mcp-for-beginners** — https://github.com/microsoft/mcp-for-beginners — This open-source curriculum introduces the fundamentals of Model Context Protocol (MCP) through real-world, cross-language examples in .NET, Java, TypeScript, JavaScript, Rust and Python. Designed for `stars: 16,856`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: none published on GitHub as of 2026-07-30`.
  Why this is on the radar now: The repository was updated on 2026-07-29 and enters the radar with 16,856 stars.
  Stack improvement angle: Adds a tool surface MCP-compatible agents (OpenClaw, Codex, Claude Code, Hermes) can call directly.
  Try now: Clone the repo and wire it into a test agent session to evaluate the tool surface.

---

## Extra Research Candidates

- **Gemini API Managed Agents: 3.6 Flash, hooks, and more** — https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/ — We’re announcing even more new capabilities in Managed Agents in Gemini API so developers can build reliable, production-ready agents. Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

- **Default model enablement for Copilot Business and Enterprise** — https://github.blog/changelog/2026-07-29-default-model-enablement-for-copilot-business-and-enterprise — We&#8217;re introducing a global default enablement policy for generally available Copilot models on Copilot Business and Copilot Enterprise plans. Instead of requiring admins to manually turn on each new model&#8230; The post Default model Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

- **GitHub Copilot app usage metrics now expand across report rollups** — https://github.blog/changelog/2026-07-28-github-copilot-app-usage-metrics-now-expand-across-report-rollups — Copilot app usage is now reported across much more of the Copilot usage metrics API. Individual Copilot app activity is now attributed to users in the enterprise-user and organization-user reports.&#8230; The post GitHub Copilot app usage m Technical depth angle: The primary source documents the concrete API and architecture mechanism behind the announcement.

---

## Show Notes

```md
Episode 095 — July 30, 2026

[00:00] Episode hook

Agent Stack Release Readout: OpenAI Codex rust-v0.146.0 headlines a dense cycle. GitHub Copilot for JetBrains adds OpenTelemetry controls and model management, Two GPT-5.6 Settings That Tripled Its ARC-AGI-3 Score, Liquid AI ships two CPU-friendly long-context encoders round out the front of the episode, with deeper cuts across models, tooling, and infrastructure behind them. Each story gets the same treatment — what shipped, the mechanism underneath, and what it changes for working builders.

[02:00] Agent Stack Release Readout: OpenAI Codex rust-v0.146.0

OpenAI shipped Codex rust-v0.146.0 on July 29, 2026, and the release is broad: Agent Plugins manifests plus new marketplaces for Amazon Bedrock and Claude Code, a WebSocket bridge from app-server to remote Code Mode hosts, and forkable threads with paginated history, including temporary forks that don't appear in the thread list. Sessions can now be named from /new or /clear, important threads can be pinned, and users can switch between side conversations without closing them.

For people running Codex against cloud workstations, the WebSocket change is the most concrete win. The app-server can connect to a Code Mode host on a different box over WebSocket rather than expecting local execution, so a thin client on your laptop can drive tools, plugins, and approvals on a heavier remote environment. Standalone web search is now available to compatible custom model providers, so third-party model routes can run their own grounded lookups instead of routing through OpenAI's stack.

The plugin work is where teams will likely feel the biggest shift. Codex now supports the Agent Plugins manifest format and can pull from Amazon Bedrock and Claude Code marketplaces alongside its own workspace publishing flow. An organization that already standardizes on manifests can publish one package definition and have it travel between runtimes instead of rewriting per host. The release also adds a way to discover executor-provided skills and read their associated resources, including explicitly selected skills.

The rest is a long cleanup pass. Proxies are now honored consistently across authentication, plugin downloads, MCP authorization, remote execution, WebSockets, redirects, and LM Studio connections. MCP connections and Apps tools refresh on authentication or config changes, reconnecting closed servers without disturbing healthy ones. Submitted messages, final responses, failed-turn errors, imported timestamps, and approval settings are preserved across interruptions, replay, imports, and forks.

Terminal handling got attention too: nonblocking interrupts, better keyboard behavior, narrow-layout fixes, hyperlinks, and refreshed mention results. On Windows, navigation keys are corrected and sandboxed process trees terminate reliably. Under tight context budgets, more skills are retained and the CLI warns when the skill catalog has to be truncated, which matters for long sessions that gradually accumulate tools.

[03:03] GitHub Copilot for JetBrains adds OpenTelemetry controls and model management

GitHub shipped an update to its Copilot plugin for JetBrains IDEs that gives developers more control and clarity over telemetry configuration and model management. The headline change is improved OpenTelemetry configuration. OpenTelemetry is the open standard for shipping logs, traces, and metrics out to whatever observability stack a team runs, and tuning it lets administrators adjust what gets sent and where it lands instead of accepting defaults.

The update also adds clearer model management, giving developers a more explicit handle on which AI models are wired into their JetBrains environment. Alongside that, the release enables connecting MCP servers and custom agents inside Claude agent flows. MCP — Model Context Protocol — is Anthropic's open standard that lets an AI agent call external tools and data sources through a uniform interface. Custom agents let teams define specialized assistants tuned to a particular workflow.

For builders, the practical upshot is twofold. Teams with audit or cost-tracking needs can now route Copilot telemetry into the same observability pipeline they use for everything else, which makes AI usage visible alongside regular application traffic. And any internal tool that already exposes an MCP endpoint — a proprietary database, an internal API, a company-specific code index — becomes reachable from a Claude agent flow inside JetBrains without writing custom glue code. Worth watching next: whether GitHub brings equivalent model-management and telemetry controls to the VS Code surface.

[04:31] Two GPT-5.6 Settings That Tripled Its ARC-AGI-3 Score

OpenAI published a short post on July 29 explaining how enabling two API settings tripled GPT-5.6's scores on the ARC-AGI-3 benchmark while also improving efficiency. ARC-AGI-3 is the puzzle-style reasoning test designed to resist brute-force pattern matching, so a threefold jump is a real signal rather than a leaderboard nudge.

The two settings are straightforward. The first retains reasoning across turns, meaning the model's working thoughts persist between steps instead of being discarded. The second turns on compaction, which summarizes older reasoning context so token usage stays manageable while the chain of thinking remains available. Together they let GPT-5.6 carry earlier insights forward without paying the full token cost of preserving every prior thought verbatim.

The result, per OpenAI, is higher scores with fewer tokens spent — better puzzle-solving at lower cost, achieved through configuration rather than retraining or a new model release. That is an unusual combination; usually you trade compute for accuracy, not get both at once.

For builders, the practical takeaway is that default GPT-5.6 may be leaving performance on the table on hard reasoning work. If you are already using the model for multi-step problems, agent loops, or anything that benefits from carrying context forward, testing with these two settings enabled is a low-effort experiment that could meaningfully change outcomes. Watch for OpenAI to publish the specific configuration names and full numbers, since those will determine how directly anyone can replicate the result in production.

[06:01] Liquid AI ships two CPU-friendly long-context encoders

Liquid AI released two open-weight encoder models in its LFM2.5 line, sized at 230 million and 350 million parameters, both targeting long-context work directly on CPUs. Each carries an 8,192-token context window, unusually generous for a CPU-targeted encoder and the headline number for anyone evaluating local pipelines.

The technical hook is a conversion recipe. Liquid AI took causal decoder backbones and rebuilt them as bidirectional encoders, swapping one-directional attention for full bidirectional attention, replacing causal short convolutions with symmetric non-causal ones, and retraining with a masked-language objective. That combination lets the models actually use the full 8,192-token window.

Liquid AI reports that the 230-million-parameter model completes an 8,192-token CPU forward pass in roughly 28 seconds, which it says is about 3.7 times faster than ModernBERT-base in its own comparison. Those numbers are vendor results, so real-world speed will depend on the hardware you deploy on, but the direction is clear: long inputs on commodity CPUs are now a stated target.

The company positions the pair for classification, routing, policy linting, and personal-data detection. Those are exactly the jobs where running fully local, without sending text to a hosted model, matters most, from routing support tickets to flagging sensitive fields before storage. With open weights, builders can fine-tune on their own labels and ship the result on a single machine.

The release landed July 28, 2026 on Hugging Face. The next thing worth watching is whether independent benchmarks confirm the CPU speed story on hardware outside Liquid AI's test rig.

[07:35] ComfyUI 0.29.0 streams video instead of buffering it in RAM

ComfyUI, the open-source node-based interface for running local image and video generation workflows, shipped version 0.29.0 on July 29. The release is small but pointed at two specific pain points.

The most concrete change is in the video pipeline. Until now, video transcoding in ComfyUI buffered every frame in RAM before processing. That works for short clips, but a long or high-resolution render can exhaust memory and die mid-job. The new behavior streams the transcode instead, so frames flow through without piling up in RAM.

The second change ships to the partner nodes system. ComfyUI now sends its Job Id as a request header to partner services. For anyone integrating a third-party partner node into a workflow, that header gives the partner a clean way to correlate incoming work with the originating ComfyUI job, instead of guessing from filenames or timing.

Together these are plumbing fixes rather than new features, but both address real frustrations: out-of-memory crashes on long video renders, and unclear attribution when a workflow fans out to external services. Worth updating if either of those has bitten you.

[08:43] NVIDIA Jetson Gets a Venture Capitalist’s Bag Endorsement

NVIDIA’s edge AI platform Jetson got an endorsement from an unusual promoter this week: venture capitalist Sarah Guo. In a video published July 28, 2026, Guo — founder of the AI-focused firm Conviction and co-host of the No Priors podcast — framed Jetson as the season’s must-carry accessory for builders. NVIDIA’s blog picked up the clip with the headline “Powerful Compute So Compact, It’s Clutch.”

The framing matters because edge AI is where a lot of practical work is heading. Robots, drones, kiosks, and inspection rigs can’t always wait for a round trip to a cloud server. Jetson is NVIDIA’s compact, self-contained computer built around its GPU-style accelerators — small enough to fit in a bag, with enough horsepower to run modern AI models locally rather than over a network.

For builders, the appeal is straightforward: you can prototype a model on a Jetson box without booking cloud time, and keep a similar hardware shape as you move from desk to deployment. The trade-off is the usual edge constraint — you’re working within the memory and compute ceiling of a small machine, so model size and efficiency matter more than they would on a server cluster.

The honest caveat: this is a promo post built around a VC’s video clip, not a product launch. NVIDIA’s blog offers no changelog, no new SKU, and no updated specs. So the takeaway is a reminder that Jetson exists and stays small — worth watching for any actual silicon refresh or developer kit update that turns the “clutch” pitch into something concrete to order.

[10:21] Intel’s U.S. Advanced Packaging Enables Next-Generation AI Semiconductors

As AI demands unprecedented "brain power," the semiconductor industry is moving past the era of relying on single, massive chips. Advanced packaging is the essential craft of interconnecting multiple specialized chips together. This allows them to function as a single, powerful unit that runs faster handling the massive workloads of the future.Intel&#8217;s been doing advanced &#8230; The post Intel’s U.S. Advanced Packaging Enables Next-Generation AI Semiconductors appeared first on Newsroom. The primary source supports the specific product or workflow change above; it does not support broader claims about performance, compatibility, or deployment. Test the sourced change against one real workflow before depending on it.

[11:00] FCC Adds Foreign-Made Advanced Robots to Its Covered List

On July 28, the FCC's Public Safety and Homeland Security Bureau added foreign-produced advanced robotic devices to the Covered List, the regulator's roster of equipment that cannot receive FCC authorization to use US radio spectrum. The move followed an Executive Branch interagency determination that pointed to four risk categories: supply-chain integrity, cybersecurity, surveillance potential, and remote-control vulnerabilities.

The practical effect is a hard gate. Any advanced robot produced outside the United States cannot be authorized for sale or operation in the US through the normal FCC process. There is one escape hatch: the Department of War can grant conditional approval for a specific device or device class if it is determined not to pose those risks. So this is not a blanket embargo. It is a presumption against foreign production, with a waiver path attached.

Importantly, the FCC action is category-based, not company-based. The rule looks at where the device was made, not which company made it. That distinction matters because US subsidiaries of foreign robot makers, or US brands outsourcing production overseas, can both be caught depending on where assembly actually happens.

For builders and importers, the open question is scope. The public notice does not pin down what counts as an "advanced robotic device," so the next few weeks of Department of War guidance and any FCC clarification will determine whether this lands as a narrow industrial-robot rule or sweeps in consumer and research hardware. The first conditional approvals will be the cleanest signal of where the line actually falls.

[12:35] Research digest: Robot Training Without the Robot: Better Capture May Replace the Real-Hardware Anchor

Robots that can fold laundry or sort objects usually need thousands of careful demonstrations collected on real hardware, which is slow and expensive. A cheaper alternative is UMI, a portable rig that captures the same kind of motion data without needing the robot itself, but the footage is noisier and less reliable. Today's standard practice is to use that cheap UMI data to pre-train a policy and then add a small dose of real-robot demonstrations as a finishing step. A new paper called HiFi-UMI asks a sharper question: what if the robot-free capture were just made more faithful, so the real-robot anchor could disappear entirely? The authors present HiFi-UMI as a portable capture setup designed for higher fidelity, with policies trained end-to-end on that data alone. The implicit pitch is that the binding constraint in manipulation learning isn't how many demonstrations you collect, but how trustworthy each one is. If the claim holds up, labs without big real-robot fleets get a much cheaper on-ramp to deployable manipulation.

[13:38] Research digest: TurboVLA paper cuts robot-control compute to under 1 GB

TurboVLA, a trending paper on HuggingFace this week, redesigns how robots turn camera views and spoken instructions into motion. Vision-language-action models — AI systems that watch their surroundings, parse a command, and move — usually push every visual frame through a big language model first. That step gives them reasoning power, but it also burns memory and adds latency at every robot tick. TurboVLA takes a different route. Instead of running vision through a large language model before producing actions, it fuses vision and language cues directly into the action output. The headline numbers are striking: the system runs at 32 updates per second on a single consumer RTX 4090 graphics card, while using under one gigabyte of video memory. That's a meaningful unlock for hobbyists, students, and small labs — the kind of setup that fits on a desk rather than filling a server rack. The catch is that the paper's demos are bounded; whether the shortcut holds on messier, less-scripted real-world tasks is the next thing to watch.

[14:43] HKUDS nanobot ships v0.3.0 as a lightweight self-hosted agent framework

HKUDS has shipped nanobot v0.3.0, a Python framework aimed at developers who want to run their own AI agent setup rather than rely on a hosted platform. The project describes itself as ultra-lightweight and self-hosted, and it has accumulated 46,404 GitHub stars.

The release went out July 25, with the repository pushed again five days later on July 30. There is no public changelog for v0.3.0 in the source material, so the practical way to see what shifted is the repository itself and its commit history.

What nanobot bundles, according to its README: a WebUI for talking to the agent, a tools layer for calling external functions, a memory component, MCP support so it can plug into the Model Context Protocol ecosystem, multi-agent workflow primitives, automation hooks, and chat app integrations. The pitch is that all of this ships in a single Python package you can run on your own hardware.

For builders, that means a self-hosted path that already speaks MCP, so you can attach tools and data sources through the same protocol a lot of hosted agents use. The chat app integrations and WebUI give you an interface layer without building one from scratch.

One thing to watch: without a v0.3.0 changelog, the release's actual deltas versus earlier versions live in the commit history, and the project's pace — a fresh push five days after the release — suggests active development worth tracking on GitHub.

[16:12] GPT-5.6 is framed as an efficiency release, not a capability one

OpenAI posted on July 29, 2026 framing GPT-5.6 around efficiency rather than raw capability gains. The post pitches GPT-5.6 as delivering more useful intelligence per dollar through improvements that span the models themselves, the inference stack, and agentic workflows.

That is the substance of the announcement. There is no public changelog attached, no specific feature list, no benchmark tables, and no concrete API or pricing detail in the source material.

For builders, that means this is positioning language rather than a feature drop. There is nothing to integrate today and nothing to retest against until OpenAI publishes the concrete release notes, pricing, and timeline. Anyone shipping production agents on the previous generation should keep an eye out for the cost and throughput numbers once they land, since the framing is explicitly about getting more useful output per dollar.

The headline to carry here is efficiency, not new capability. Watch for the real numbers.

[17:10] OpenAI Grants Free ChatGPT Access to 100,000 Academic Researchers

OpenAI announced on July 29, 2026 that it is giving 100,000 academic researchers free access to ChatGPT's most advanced AI models. The program is framed around accelerating scientific research, collaboration, and discovery.

The announcement does not name the specific models included, describe eligibility criteria, or explain how the 100,000 slots will be distributed. There is no changelog, no pricing detail, and no timeline for when access begins or how long it lasts. The source material is the single announcement page, which only confirms the headline number, the audience, and the stated goal.

What this signals is OpenAI continuing to invest in research-adjacent use cases. Free top-tier access for a large cohort of academics is the kind of move that can shape which tools graduate students, postdocs, and faculty reach for when they draft papers, summarize literature, or brainstorm hypotheses. Whether it materially changes research workflows will depend on details the announcement does not yet provide.

The 100,000 figure is large enough to matter — roughly the size of a major research university's combined faculty and graduate student body. If the access works as advertised, expect a steady stream of papers crediting ChatGPT as a research assistant over the coming year. For now, the headline is the story; the mechanics are still pending.

[18:30] OlmoEarth Platform brings geospatial inference to planetary scale

AllenAI published a post on the Hugging Face Blog on July 28, 2026, titled "The OlmoEarth Platform: Geospatial inference at planetary scale." That is the headline. It positions OlmoEarth as a platform rather than a single model, with geospatial inference as the core capability and planetary scale as the operating target.

Reading the title carefully, "geospatial inference" means the system is meant to take geographic and remote-sensing style data and produce predictions over it, and "planetary scale" signals that the underlying data and compute pipeline are sized for Earth-wide coverage rather than a single city, watershed, or satellite tile. For builders, that framing matters because the hard part of geospatial AI has rarely been the model — it has been ingesting, tiling, and serving continent-sized raster and vector inputs at all.

Beyond the headline and the publish date, the public source does not include a changelog, model card, or concrete release notes. There is no listed model variant, no documented API surface, no stated input formats, and no announced pricing or access tier in the material available here. So while the name and ambition are now on the record, the practical question of what a developer can call, install, or fine-tune today is still left open by AllenAI's announcement.

One thing to watch next: whether AllenAI follows the blog post with model weights, an inference endpoint, or sample notebooks that turn "planetary scale" from a phrase into something a builder can actually run against their own region of interest.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: OpenAI Codex rust-v0.146.0 / GitHub Copilot for JetBrains adds OpenTelemetry controls and model management / Two GPT-5.6 Settings That Tripled Its ARC-AGI-3 Score
- 02:00 — Agent Stack Release Readout: OpenAI Codex rust-v0.146.0
- 03:03 — GitHub Copilot for JetBrains adds OpenTelemetry controls and model management
- 04:31 — Two GPT-5.6 Settings That Tripled Its ARC-AGI-3 Score
- 06:01 — Liquid AI ships two CPU-friendly long-context encoders
- 07:35 — ComfyUI 0.29.0 streams video instead of buffering it in RAM
- 08:43 — NVIDIA Jetson Gets a Venture Capitalist’s Bag Endorsement
- 10:21 — Intel’s U.S. Advanced Packaging Enables Next-Generation AI Semiconductors
- 11:00 — FCC Adds Foreign-Made Advanced Robots to Its Covered List
- 12:35 — Research digest: Robot Training Without the Robot: Better Capture May Replace the Real-Hardware Anchor
- 13:38 — Research digest: TurboVLA paper cuts robot-control compute to under 1 GB
- 14:43 — HKUDS nanobot ships v0.3.0 as a lightweight self-hosted agent framework
- 16:12 — GPT-5.6 is framed as an efficiency release, not a capability one
- 17:10 — OpenAI Grants Free ChatGPT Access to 100,000 Academic Researchers
- 18:30 — OlmoEarth Platform brings geospatial inference to planetary scale

---

## Primary Links

- OpenAI Codex rust-v0.146.0 release: https://github.com/openai/codex/releases/tag/rust-v0.146.0
- GitHub Copilot for JetBrains adds improved OpenTelemetry configuration: https://github.blog/changelog/2026-07-27-github-copilot-for-jetbrains-adds-improvved-opentelemetry-configuration-and-model-management
- How enabling two settings tripled our scores on the ARC-AGI-3 benchmar: https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores
- Copilot code review: Agent skills and MCP now generally available: https://github.blog/changelog/2026-07-29-copilot-code-review-agent-skills-and-mcp-now-generally-available
- Liquid AI releases two open-weight long-context encoders for CPUs: https://huggingface.co/blog/LiquidAI/lfm2-5-encoders
- comfyanonymous/ComfyUI ships v0.29.0: https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.29.0
- Powerful Compute So Compact, It’s Clutch — Build AI Anywhere With NVID: https://blogs.nvidia.com/blog/build-ai-with-nvidia-jetson/
- Intel’s U.S. Advanced Packaging Enables Next-Generation AI Semiconduct: https://newsroom.intel.com/intel-foundry/intels-us-advanced-packaging-enables-next-generation-ai-semiconductors
- FCC adds foreign-produced advanced robots to its Covered List: https://docs.fcc.gov/public/attachments/DA-26-786A1.pdf
- HiFi-UMI: Learning Deployable Manipulation Policies from High-Fidelity: https://cloud.simpleai.tech/simple-world-lab/hifi-umi/
- TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 40: https://h-embodvis.github.io/TurboVLA/
- HKUDS/nanobot — Ultra-lightweight, open-source, self-hosted personal A: https://github.com/HKUDS/nanobot
- How GPT-5.6 fuses frontier intelligence with frontier efficiency: https://openai.com/index/gpt-5-6-frontier-intelligence-efficiency
- Accelerating scientific discovery with ChatGPT for Academic Researcher: https://openai.com/index/chatgpt-for-academic-researchers
- The OlmoEarth Platform: Geospatial inference at planetary scale: https://huggingface.co/blog/allenai/olmoearth-infrastructure
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- microsoft/mcp-for-beginners repo: https://github.com/microsoft/mcp-for-beginners
- Gemini API Managed Agents: 3.6 Flash, hooks, and more: https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/
- Default model enablement for Copilot Business and Enterprise: https://github.blog/changelog/2026-07-29-default-model-enablement-for-copilot-business-and-enterprise
- GitHub Copilot app usage metrics now expand across report rollups: https://github.blog/changelog/2026-07-28-github-copilot-app-usage-metrics-now-expand-across-report-rollups
- moonshotai/Kimi-K3: https://huggingface.co/moonshotai/Kimi-K3

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.7.1`, published 2026-07-13T22:33:14Z. Recent episode version tags detected: `v2026.7.2-beta.1`, `v2026.7.2-beta.2`, `v2026.7.2-beta.3`, `v2026.7.2-beta.5`. No new stable release this cycle.
- **Hermes Agent** — Latest stable verified: `v2026.7.20`, published 2026-07-20T18:35:55Z. Recent episode version tags detected: `v2026.7.1`, `v2026.7.20`, `v2026.7.7`, `v2026.7.7.2`. No new stable release this cycle.
- **OpenAI Codex** — Latest stable verified: `rust-v0.146.0`, published 2026-07-29T01:42:51Z. Recent episode version tags detected: `rust-v0.144.4`, `rust-v0.144.5`, `rust-v0.144.6`, `rust-v0.145.0`. Selected missing version(s): `rust-v0.146.0`.
- **Claude Code CLI** — Latest stable verified: `2.1.212`, published 2026-07-16T19:20:24.324Z. Recent episode version tags detected: `2.1.206`, `2.1.212`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-07-30). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.7.1` (stable) / `v2026.7.2-beta.5` (prerelease)
- **Hermes Agent** — `v2026.7.20`
- **OpenAI Codex** — `rust-v0.146.0`
- **Claude Code CLI** — `2.1.212`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
