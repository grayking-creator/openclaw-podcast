## Episode Title
Local Agents Get Their Hardware Week

## Tagline
Ollama, LM Studio, EXO, DGX Spark, Grok Build, and gateway hardening all moved in ways that matter for local-first agent builders.

## Feed Description
This episode follows six concrete changes in the agent stack: Ollama pushing deeper into local coding-agent runtimes, LM Studio improving Apple Silicon vision inference and remote local servers, NVIDIA positioning DGX Spark as a serious local-agent machine, EXO showing where distributed local inference still needs hardening, xAI shipping Grok Build while redirecting older model slugs to Grok 4.3, and LiteLLM plus Envoy AI Gateway tightening the routing layer that sits between agents and models.

## Story Slate

### 1. **Ollama moves from local model runner toward local coding-agent platform**
- Primary source: https://github.com/ollama/ollama/releases
- What changed: Ollama 0.24 adds Codex App support through the launch command for Codex App. Recent May releases add vision-model support for opencode launch, improve Claude tool-result formatting for local image paths, and cache API show responses to improve median integration load latency by about 6.7x. The 0.30.0 release candidate changes the underlying architecture to directly support llama.cpp, GGUF compatibility, and MLX acceleration on Apple Silicon. Earlier May releases added Gemma 4 MTP speculative decoding in the MLX runner, claiming more than 2x speedup for Gemma 4 31B coding tasks.
- Why it matters: Ollama is not just serving models locally; it is becoming a launch surface for local coding environments and desktop agent integrations.
- Technical depth angle: Explain how GGUF compatibility, llama.cpp alignment, MLX acceleration, API metadata caching, and speculative decoding change latency, model portability, and local coding-agent ergonomics.

### 2. **LM Studio 0.4.13 improves MLX vision inference while DGX support points beyond laptops**
- Primary sources: https://lmstudio.ai/changelog/lmstudio-v0.4.13 and https://lmstudio.ai/blog/dgx-station
- What changed: LM Studio 0.4.13 ships mlx-engine v1.8.1, with performance improvements and parallel predictions for vision-capable models such as Qwen 3.5/3.6 and Gemma 4. LM Studio's DGX Station material describes llmster, LM Link, OpenAI-compatible APIs, Anthropic-compatible APIs, and SDK access as the way to turn a heavy local box into a shared inference endpoint.
- Why it matters: Local AI is splitting into two important patterns: fast desktop experimentation on Apple Silicon and heavier shared inference machines that laptops can call like a local service.
- Technical depth angle: Explain why parallel predictions for vision models matter on MLX, and how LM Link plus headless llmster changes deployment from one laptop running one chat app to a local/private model server exposed to tools.

### 3. **DGX Spark becomes a serious local-agent target**
- Primary sources: https://blogs.nvidia.com/blog/rtx-ai-garage-gtc-2026-nemoclaw/ and https://build.nvidia.com/spark/hermes-agent
- What changed: NVIDIA is explicitly framing DGX Spark and RTX PCs as agent computers for running personal agents locally. Its GTC material calls out Nemotron 3 Nano 4B, Nemotron 3 Super 120B, Qwen 3.5 optimizations, Mistral Small 4, and local agent stacks running through Ollama, LM Studio, and llama.cpp. DGX Spark's 128GB unified memory is positioned as enough for models above 120B parameters, while Nemotron 3 Super is described as a 120B open model with 12B active parameters.
- Why it matters: DGX Spark gives the local stack a middle tier between Mac or RTX desktop inference and renting cloud GPUs forever.
- Technical depth angle: Explain the practical importance of 128GB unified memory, mixture-of-experts active parameters, local tool execution, and the difference between running a chat model locally and running always-on agents locally.

### 4. **EXO plus DGX Spark shows the promise and rough edges of distributed local inference**
- Primary source: https://github.com/exo-explore/exo/issues/1682
- What changed: A closed EXO issue documents DGX Spark joining a local EXO cluster only after two concrete problems were solved: the Rust exo_pyo3_bindings networking module was not compiled on Linux/aarch64, and the libp2p private-network namespace needed to match across nodes. The report confirms the end state: DGX Spark appeared in the EXO dashboard and participated in distributed inference after the Rust networking module and shared namespace were fixed.
- Why it matters: EXO attacks the local-cluster problem directly: make multiple machines behave like one inference pool instead of treating every node as a separate island.
- Technical depth angle: Explain mDNS discovery, libp2p private-network keys, Linux/aarch64 packaging, and why distributed inference depends as much on node discovery and runtime packaging as on raw model speed.

### 5. **Grok Build arrives as a coding-agent CLI, while xAI model redirects create pricing and routing risk**
- Primary sources: https://docs.x.ai/build/overview, https://docs.x.ai/build/cli/headless-scripting, and https://docs.x.ai/developers/migration/may-15-retirement
- What changed: xAI's Grok Build docs describe an interactive coding-agent TUI, headless scripting, streaming JSON output, ACP support through agent stdio, custom model configuration, skills, plugins, hooks, and MCP servers. xAI's May 15 migration redirects retired reasoning model slugs to Grok 4.3 with low reasoning effort and retired non-reasoning slugs to Grok 4.3 with no reasoning effort. grok-code-fast-1 redirects to Grok 4.3, and post-redirect usage is billed at Grok 4.3 pricing: $1.25 per million input tokens and $2.50 per million output tokens.
- Why it matters: Grok Build matters because another major provider is copying the coding-agent CLI/TUI/headless pattern. The pricing story matters because silent redirects can change cost and behavior even when code keeps running.
- Technical depth angle: Explain the agent surface area: TUI, headless mode, streaming JSON, ACP, custom model routing, and deprecated slug redirects. Keep the pricing point concrete and note that the reported $99 plan is not visible in the official docs checked here.

### 6. **LiteLLM and Envoy AI Gateway harden the model-routing layer**
- Primary sources: https://docs.litellm.ai/release_notes/v1.84.0/v1-84-0 and https://aigateway.envoyproxy.io/release-notes/
- What changed: LiteLLM v1.84.0 changes version naming to PEP 440, authenticates pass-through endpoints by default, improves multi-pod budget enforcement, avoids Prisma reconnect freezes, reduces memory footprint by lazy-loading feature routers, adds MCP OAuth and Azure Entra discovery support, and introduces a workflow-runs REST surface. Envoy AI Gateway v0.6.0 graduates core CRDs to v1beta1, adds Anthropic endpoint support on OpenAI-compatible backends, adds Gemini embeddings and context caching, supports MCP per-backend header forwarding, and adds request/response body redaction.
- Why it matters: Local and multi-provider stacks still need a gateway layer. Agents call many models, model names move, budgets drift, and tool servers need authorization.
- Technical depth angle: Explain model gateways as the control plane between agents and inference: auth defaults, spend counters, routing groups, provider normalization, MCP auth/header forwarding, and body redaction.

## Extra Research Candidates

- **Firecrawl: MCP vs CLI for AI agents**
  - Link: https://www.firecrawl.dev/blog/mcp-vs-cli
  - Technical depth angle: Use only as a compact economics sidebar if the episode needs one more sharp tradeoff: CLI has low schema/context overhead and native shell composability; MCP wins on per-user OAuth, persistent sessions, and governance.

- **LM Studio DGX Station guide**
  - Link: https://lmstudio.ai/blog/dgx-station
  - Technical depth angle: Can expand the LM Studio story if more hardware specificity is needed: llmster, LM Link, remote local inference, OpenAI/Anthropic-compatible APIs, and serving large open models from a deskside machine.

- **Envoy AI Gateway v0.6.0 detail page**
  - Link: https://aigateway.envoyproxy.io/release-notes/v0.6
  - Technical depth angle: Use if the gateway segment needs more operational specificity around v1beta1 CRDs, breaking changes, Gemini context caching, Anthropic-on-OpenAI compatibility, and body redaction.

## Show Notes
```md
# OpenClaw Daily EP052: Local Agents Get Their Hardware Week

This episode tracks six concrete moves in the agent stack. The center of gravity is local-first infrastructure: local model runners, Apple Silicon acceleration, DGX Spark as a local-agent machine, EXO distributed inference, coding-agent CLIs, and the gateway layer that keeps model routing from becoming brittle.

[00:00] Ollama moves from model runner toward coding-agent platform

Ollama's recent releases show it becoming more than a local model server. The big items are Codex App support through Ollama Launch, vision-model support for opencode launch, local image-path fixes for Claude tool results, and API show response caching that improves median integration load latency by about 6.7x.

The more important forward-looking item is the 0.30.0 release candidate. Ollama says that version changes the architecture to directly support llama.cpp, allows GGUF file compatibility, and uses MLX to accelerate inference on Apple Silicon. Earlier May work also added Gemma 4 MTP speculative decoding in the MLX runner, with more than 2x speed increase claimed for Gemma 4 31B coding tasks.

The practical read: Ollama is moving closer to being a local runtime layer for coding agents and desktop AI tools. Model portability, MLX acceleration, faster metadata calls, launch integrations, and vision inputs all matter when a local agent has to do real project work instead of just answer prompts.

Sources:
- https://github.com/ollama/ollama/releases

[05:00] LM Studio improves MLX vision inference and points toward shared local servers

LM Studio 0.4.13 ships mlx-engine v1.8.1. The official changelog says it significantly improves performance and adds parallel predictions for vision-capable models including Qwen 3.5/3.6 and Gemma 4. The same release fixes pasted-newline handling and includes security hardening.

That sounds small until you put it next to where LM Studio is going with larger machines. Its DGX Station material describes a headless daemon, llmster, paired with LM Link so one machine can serve local models to other devices. It also calls out LM Studio SDKs, the LM Studio API, and OpenAI-compatible and Anthropic-compatible APIs.

The builder relevance is straightforward: local AI is becoming a two-part stack. A laptop or Mac can be the interface, while a larger local machine handles the model load. For vision agents, MLX parallel prediction improvements matter because screenshots, images, UI state, and multimodal project context are becoming normal inputs, not demos.

Sources:
- https://lmstudio.ai/changelog/lmstudio-v0.4.13
- https://lmstudio.ai/blog/dgx-station

[10:00] DGX Spark becomes a serious local-agent target

NVIDIA's current DGX Spark and RTX messaging is explicitly about local agents. The company is framing these machines as agent computers for running personal agents locally, privately, and without token costs. Its GTC material highlights Nemotron 3 Nano 4B, Nemotron 3 Super 120B, Qwen 3.5 optimizations, Mistral Small 4, and local agent stacks running through Ollama, LM Studio, and llama.cpp.

DGX Spark matters because of memory and deployment shape. NVIDIA describes DGX Spark with 128GB of unified memory, enough for models above 120B parameters. Nemotron 3 Super is described as a 120B open model with 12B active parameters, while smaller models such as Nemotron 3 Nano 4B target more constrained RTX machines.

The point is not that every builder should buy one. The point is that local agent software now has a hardware tier above a single desktop and below rented cloud GPU infrastructure. If local agents are going to keep context private, run all day, and call tools without paying per-token cloud costs for every step, machines like DGX Spark become relevant infrastructure.

Sources:
- https://blogs.nvidia.com/blog/rtx-ai-garage-gtc-2026-nemoclaw/
- https://build.nvidia.com/spark/hermes-agent

[15:00] EXO plus DGX Spark shows distributed local inference is real but still rough

An EXO issue around DGX Spark is more useful than a clean press release because it shows the actual failure mode. The cluster had Macs and a DGX Spark on the same local network, basic connectivity worked, EXO dashboard access worked, and ports were reachable. But the nodes still did not form a working distributed inference cluster.

The reported fix had two parts. First, the Rust exo_pyo3_bindings networking module, which contains libp2p networking, mDNS discovery, and private-network logic, needed to be compiled manually on Linux/aarch64. Second, all nodes needed the same EXO_LIBP2P_NAMESPACE so the libp2p private-network key matched across the cluster.

After that, the DGX Spark appeared in the EXO dashboard and participated in distributed inference. That is the real story: EXO is tackling the right local-cluster problem, but distributed local inference lives or dies on discovery, packaging, namespace alignment, and architecture-specific builds. Raw compute is not enough if the nodes cannot reliably find and trust each other.

Sources:
- https://github.com/exo-explore/exo/issues/1682

[20:00] Grok Build arrives, but model redirects and pricing need attention

xAI's Grok Build docs describe a full coding-agent CLI surface: an interactive TUI, headless scripting, plain/json/streaming-json output, resumable sessions, ACP through Grok agent stdio, custom model configuration, skills, plugins, hooks, and MCP server discovery.

That makes Grok Build part of the same category as other coding-agent CLIs: a terminal-native agent with automation hooks, not just a chat surface. The official docs also show custom model configuration, which matters because builders increasingly want coding-agent shells that can route to different model backends.

The cost and migration story is separate but important. xAI's May 15 retirement page says deprecated reasoning slugs redirect to Grok 4.3 with low reasoning effort, non-reasoning slugs redirect to Grok 4.3 with no reasoning effort, and grok-code-fast-1 redirects to Grok 4.3. The page lists Grok 4.3 API pricing at $1.25 per million input tokens and $2.50 per million output tokens. The practical recommendation is to pin replacement models explicitly rather than letting deprecated slugs silently change behavior and billing.

Sources:
- https://docs.x.ai/build/overview
- https://docs.x.ai/build/cli/headless-scripting
- https://docs.x.ai/developers/migration/may-15-retirement

[25:00] LiteLLM and Envoy harden the model gateway layer

LiteLLM v1.84.0 is a gateway hardening release. The release changes version naming to PEP 440, authenticates pass-through endpoints by default, improves multi-pod budget enforcement, avoids Prisma reconnect freezes, cuts memory footprint through lazy-loaded feature routers, adds MCP OAuth and Azure Entra discovery support, and adds durable workflow run tracking through a workflow-runs API surface.

Envoy AI Gateway v0.6.0 is moving in the same direction from the Kubernetes gateway side. It graduates core CRDs to v1beta1, adds Anthropic endpoint support on OpenAI-compatible backends, adds Gemini embeddings and context caching, supports MCP per-backend header forwarding, adds request/response body redaction, and updates the Envoy/Gateway baseline.

The reason this belongs in a local-agent episode is that local-first does not mean gateway-free. Agents still need routing, auth, budgets, redaction, provider compatibility, and MCP authorization. The more model backends and local runtimes you add, the more important the control plane becomes.

Sources:
- https://docs.litellm.ai/release_notes/v1.84.0/v1-84-0
- https://aigateway.envoyproxy.io/release-notes/
```
