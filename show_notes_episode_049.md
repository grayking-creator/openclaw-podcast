# EP049 — Gemini Deep Research, Agents SDK Sandbox Boundaries, vLLM Kernel Fixes, and Strands Runtime Controls

## Release Coverage Check

- Stable OpenClaw release verification completed against the GitHub releases API.
- The latest stable release is not eligible under the contiguous-block rule because the five-file release ledger stops the walk immediately.
- Candidate OpenClaw release list for EP049: none.
- No OpenClaw release story is included.

## Episode Title

Gemini Deep Research, Agents SDK Sandbox Boundaries, vLLM Kernel Fixes, and Strands Runtime Controls

## Tagline

A technical operator briefing on background research agents, sandbox materialization boundaries, inference-kernel reliability, and agent runtime control surfaces.

## Feed Description

EP049 goes deep on Google’s Gemini Deep Research Agent in the Interactions API, OpenAI Agents SDK sandbox and session fixes, vLLM’s DeepSeek V4 serving patch, and Strands Agents TypeScript runtime controls for hooks, MCP, compression, retries, and human interruption.

## Story Slate

### 1. **Google Opens Gemini Deep Research Agent through the Interactions API**
Google’s Gemini Deep Research Agent is now documented as a preview Interactions API agent with background execution, streaming updates, resumable event consumption, Google Search tooling, remote MCP servers, multimodal inputs, generated-image outputs, and model routing through Gemini 3.1 Pro Preview. This is a strong lead story because it is not just a chat model launch; it exposes a long-running research loop as an API product with task IDs, stream recovery, tool budgets, and different operational behavior from ordinary synchronous Gemini calls. Technical depth angle: explain the Interactions API contract, `background=true`, stream event recovery with interaction IDs and last event IDs, tool configuration, MCP server headers, multimodal grounding, and the failure modes of minute-scale autonomous research jobs.

### 2. **OpenAI Agents Python 0.17.1 Turns Sandbox Safety, Realtime Tool Approval, Tracing, and Session Repair into Production Concerns**
OpenAI’s Agents Python SDK v0.17.1 is a dense reliability release: sandbox archive extraction is bounded, Git repository subpaths are validated, provider error details are surfaced, tracing shutdown becomes best-effort, batch trace workers survive exporter errors, hosted tool IDs are preserved in conversation sessions, corrupt MongoDB session items are skipped, and Realtime tool approvals are scoped by qualified key. This is worth covering even after recent Agents SDK coverage because the May 11 patch is about hardening the exact places agent applications break: artifact materialization, state stores, tracing queues, realtime approval identity, and schema validation. Technical depth angle: explain sandbox materialization boundaries, archive and Git subpath validation, trace processor failure isolation, session-state corruption handling, hosted tool ID preservation, realtime approval key scoping, and strict Chat Completions feature validation.

### 3. **vLLM 0.20.2 Shows How Large-Model Serving Fails at Kernel, KV Cache, and Compiler Boundaries**
vLLM v0.20.2 is a small patch with large operational implications: it fixes a DeepSeek V4 sparse-attention hang by re-enabling the persistent top-k path on Hopper and ensuring a memset kernel runs during CUDA graph capture, repairs a V1-engine KV-block allocation error, wires MXFP4 MoE fake-op shape metadata so `torch.compile` works for gpt-oss, and removes a Qwen3-VL boundary check that failed under heavy load. This is a practical infrastructure story because production serving reliability is often decided by these narrow interactions between CUDA graph capture, attention kernels, quantized MoE dispatch, and cache managers. Technical depth angle: explain sparse attention top-k scheduling, CUDA graph capture timing, KV-block allocation, MXFP4 fake ops under `torch.compile`, heavy-load multimodal boundary checks, and how operators should read patch notes for serving-risk signals.

### 4. **Strands Agents TypeScript 1.1 Adds Runtime Knobs for Hooks, MCP, WASM, Context Compression, Interrupts, Timeouts, and Retries**
Strands Agents TypeScript v1.1.0 is a broad agent-runtime release that adds hook fields before and after tool calls, exposes model identity on local agents, paginates MCP `listTools()`, surfaces server logs and metadata with fail-open behavior, adds async disposal for MCP clients, implements human-in-the-loop interrupts, adds graph and swarm timeouts, introduces proactive context compression, normalizes invalid tool names, and adds model retry and backoff strategy types. The useful angle is not “another SDK shipped”; it is how agent frameworks are converging on explicit runtime control planes for tool lifecycle, context pressure, cleanup, fault tolerance, and operator-visible events. Technical depth angle: explain hook ordering, AfterTools end-turn decisions, MCP pagination and cleanup semantics, context compression triggers, graph/swarm timeout behavior, interrupt checkpoints, retry/backoff strategies, and WASM bridge type-safety constraints.

## Extra Research Candidates

- **MCP Python SDK 1.27.1 Stabilizes Output Schema Generation and OAuth Metadata Edges** — Primary source: https://github.com/modelcontextprotocol/python-sdk/releases. Technical depth angle: explain Pydantic 2.13 `PydanticUserError` handling during output schema generation, optional URL coercion in OAuth client metadata, and dependency pinning around HTTP transports.
- **LangChain 1.2.18 and 0.3.30 Backport Loads/Dumps Hardening and Hub Deprecation** — Primary source: https://github.com/langchain-ai/langchain/releases. Technical depth angle: explain serializer/deserializer attack surface, limits on loads/dumps, hub deprecation, and why agent frameworks are narrowing unsafe dynamic loading paths.
- **xAI Custom Voices Adds a Voice Catalog across TTS and Voice Agent APIs** — Primary source: https://docs.x.ai/developers/release-notes. Technical depth angle: explain custom voice lifecycle, catalog management, short-clip cloning constraints, voice-agent reuse, and the privacy/safety boundaries builders need before storing cloned voices.

## Show Notes

```md
[00:00] Gemini Deep Research becomes an API-shaped background agent
Google’s Gemini Deep Research Agent is now exposed through the Gemini Interactions API as a preview agent rather than a normal one-shot model call. The operational detail matters: developers start a task with an agent such as `deep-research-preview-04-2026`, set background execution, optionally stream updates, and treat the result as a multi-step job that can plan, search, read, synthesize, and return intermediate artifacts. The stack supports Google Search by default, remote MCP servers with headers for authentication, multimodal inputs such as images and PDFs, generated-image outputs in response steps, and model routing through Gemini 3.1 Pro Preview. For builders, the design pattern is closer to a durable workflow than a chat completion: save the interaction ID, consume stream events, resume with the last event ID after a dropped connection, and expect minute-scale latency and tool-driven cost variance. The recommendation is to wrap this behind a job queue, a cancel path, budget controls, source-audit UI, and explicit handling for untrusted documents because the agent may read hidden text in files while grounding the research.

[09:00] OpenAI Agents Python 0.17.1 hardens sandboxes, traces, sessions, and realtime approvals
OpenAI’s Agents Python SDK v0.17.1 is the kind of patch release agent operators should read carefully. The sandbox fixes limit archive extraction, validate Git repository subpaths, preserve repository-root aliases, and surface provider error details. Those changes define the boundary between trusted local source material and what gets copied into an execution environment. The tracing fixes make shutdown best-effort, prevent exporter errors from killing the batch worker, and guard no-op span IDs, which improves observability reliability during process exits and partial telemetry failures. Session fixes preserve hosted tool IDs in OpenAI conversation sessions, skip corrupt session records, and keep metadata timestamps consistent across MongoDB and Redis-backed stores. Realtime fixes scope tool approvals by qualified key, wake iterators on close, preserve audio output parts, and avoid mutating caller-owned audio buffers. The practical migration advice is to upgrade if you run sandboxed agents or realtime agents, then test archive imports, Git materialization, trace export failure, session resume, approval routing, and any strict schema paths that depend on Chat Completions compatibility.

[18:30] vLLM 0.20.2 turns serving reliability into a kernel-and-cache investigation
vLLM v0.20.2 is a compact serving patch, but it points at the failure modes that matter when large MoE and multimodal models are actually deployed. DeepSeek V4 sparse attention gets a fix for an MTP=1 hang by re-enabling the persistent top-k path on Hopper and making sure the memset kernel executes at CUDA graph capture time regardless of maximum sequence length. That is a scheduling and capture-order issue, not a model-quality issue. The release also fixes a V1-engine KV cache manager error where KV blocks could fail to allocate, which is exactly the class of bug that appears only under certain sequence length, batch, and cache pressure patterns. For gpt-oss, the patch wires unpadded hidden-dimension metadata through a fake MoE op so MXFP4 can survive `torch.compile`; for Qwen3-VL, it removes a deepstack boundary check that could fail under heavy load. Builders should treat this as a reminder to test inference upgrades with long contexts, multimodal load, quantized paths, CUDA graph settings, and model-specific parsers before rolling to production.

[27:00] Strands TypeScript 1.1 expands the runtime control surface for agent applications
Strands Agents TypeScript v1.1.0 is useful because it makes previously implicit runtime behavior more configurable and observable. Hook fields now appear around tool calls and after invocation, with optional hook ordering and an AfterTools end-turn decision field. MCP support gets more production-shaped through `listTools()` pagination, server logs, metadata getters, fail-open controls, and `Symbol.asyncDispose` cleanup for clients. Conversation managers gain proactive context compression, graph and swarm execution get timeouts, Bedrock requests gain timeout control, and local agents expose model identity. The release also includes human-in-the-loop interrupts, result offload, normalized invalid tool names, structured output work for the WASM bridge, WASM contract tests, and model retry/backoff strategy types. The operator takeaway is that an agent SDK is increasingly a runtime: it needs lifecycle events, cleanup semantics, retry policy, context-pressure control, timeout policy, and inspection points so applications can recover from long tool lists, slow model calls, oversized results, and human approval pauses without losing state.

[35:30] Implementation checklist for teams adopting these updates
If you are building with these APIs this week, separate synchronous model calls from background agent jobs. Gemini Deep Research should run behind stored interaction IDs, stream-resume logic, tool budgets, and document-safety warnings. Agents SDK upgrades should get regression tests for sandbox file grants, archive boundaries, Git subpaths, telemetry exporter failure, session corruption, and realtime approval identity. vLLM serving upgrades should be benchmarked against the exact accelerator, CUDA graph, cache size, quantization, multimodal, and sequence-length profile you use in production, not just a simple smoke prompt. Strands-style runtime controls are a prompt to instrument your own agents around tool-call lifecycle, context compression, graph timeout, cleanup, and retry policy. The rating: Gemini Deep Research is high-impact but needs workflow wrapping; OpenAI Agents 0.17.1 is a strong safety and reliability upgrade; vLLM 0.20.2 is important for operators serving the affected models; Strands 1.1 is most valuable for teams that need explicit agent runtime mechanics rather than a thin model wrapper.
```

## Verified Links

- Google Gemini Deep Research Agent docs: https://ai.google.dev/gemini-api/docs/interactions/deep-research
- OpenAI Agents Python v0.17.1 release: https://github.com/openai/openai-agents-python/releases/tag/v0.17.1
- vLLM v0.20.2 release: https://github.com/vllm-project/vllm/releases/tag/v0.20.2
- Strands Agents TypeScript v1.1.0 release: https://github.com/strands-agents/sdk-typescript/releases/tag/v1.1.0
- MCP Python SDK releases: https://github.com/modelcontextprotocol/python-sdk/releases
- LangChain releases: https://github.com/langchain-ai/langchain/releases
- xAI release notes: https://docs.x.ai/developers/release-notes

## Chapters

- 00:00 — Gemini Deep Research becomes an API-shaped background agent
- 09:00 — OpenAI Agents Python 0.17.1 hardens sandboxes, traces, sessions, and realtime approvals
- 18:30 — vLLM 0.20.2 turns serving reliability into a kernel-and-cache investigation
- 27:00 — Strands TypeScript 1.1 expands the runtime control surface for agent applications
- 35:30 — Implementation checklist for teams adopting these updates
