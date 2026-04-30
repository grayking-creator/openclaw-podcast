# EP043 — OpenClaw v2026.4.27, Voice Agents, and Rapid AI Storage
**OpenClaw Daily** | April 30, 2026 | ~45–50 min

## Release Selection Verification
- Draft collision check: `show_notes_episode_043.md` did not exist when generation started.
- GitHub stable releases checked latest-first from the latest API page: `v2026.4.27`, `v2026.4.26`, `v2026.4.25`, `v2026.4.24`.
- Covered tags found in the last 5 episode notes: `v2026.4.26`, `v2026.4.25`, `v2026.4.24`, `v2026.4.23`, `v2026.4.22`, plus older carryover references.
- Candidate release list under the strict latest-contiguous rule: `v2026.4.27` only. The walk starts at the latest stable release, includes `v2026.4.27`, and stops at the first covered stable release, `v2026.4.26`.
- Result: EP043 leads with OpenClaw `v2026.4.27`.

## Episode Title
**OpenClaw v2026.4.27, Voice Agents, and Rapid AI Storage**

## Tagline
OpenClaw v2026.4.27 is a big operator release: Codex computer-use setup, bundled DeepInfra, channel expansion, Docker GPU passthrough, proxy controls, manifest-backed model catalogs, and a long reliability pass. Then EP043 covers multilingual voice-agent STT and Google’s Rapid Bucket path for PyTorch I/O.

## Feed Description
EP043 starts with OpenClaw v2026.4.27. The release adds Codex Computer Use status/install flows with fail-closed MCP checks, bundles DeepInfra as a provider for model discovery and media generation, expands Tencent Yuanbao and QQBot channel coverage, adds Docker GPU passthrough for sandboxed agents, introduces operator-managed outbound proxy routing, stages non-image chat attachments for agent use, moves startup and model catalogs toward manifest-first metadata, and fixes many real delivery, session, channel, media, plugin, update, and gateway edge cases. After the release deep dive, the episode turns to Deepgram Flux Multilingual and what multilingual streaming STT changes for voice agents, then Google Rapid Bucket, Colossus, gcsfs, and fsspec as an AI training data path.

## Story Slate

### 1. **OpenClaw v2026.4.27 Tightens Computer Use, Providers, Channels, Startup, and Reliability**
OpenClaw v2026.4.27 is the valid release block for EP043 and it should lead the episode. The practical changes are broad: Codex Computer Use setup gains status/install commands and fail-closed MCP checks, DeepInfra becomes a bundled provider, Docker sandboxes can opt into GPU passthrough, non-image chat attachments become agent-readable media paths, outbound proxy routing gets explicit operator controls, and plugin/model startup work keeps moving into manifest-owned metadata. Technical depth angle: explain the changed operator surfaces — `/codex computer-use status/install`, MCP server preflight behavior, `sandbox.docker.gpus`, `proxy.enabled` and `OPENCLAW_PROXY_URL`, manifest-backed model catalogs, plugin activation metadata, channel route normalization, and the reliability fixes that affect Telegram, Slack, Discord media jobs, cron topics, sessions, updates, and gateway startup.

### 2. **Deepgram Flux Multilingual Makes Voice-Agent STT a Turn-Taking Runtime Problem**
Deepgram’s Flux Multilingual adds a single streaming model for ten languages with code switching, language hints, detected-language fields, and configurable end-of-turn behavior. This is more important than a transcription headline because voice agents fail when language routing, endpoint choice, turn detection, and GPU capacity are handled as afterthoughts. Technical depth angle: explain `flux-general-multi`, `/v2/listen` WebSocket semantics, `language_hint`, `TurnInfo.languages`, `eot_threshold`, `eager_eot_threshold`, dedicated self-hosted Engine nodes, `max_streams`, GPU-memory allocation, Flux metrics, and failure modes such as OOM, CPU fallback, dropped calls, and excess concurrency.

### 3. **Google Rapid Bucket Brings Colossus into the PyTorch Data Path**
Google’s April 29 developer post is a useful infrastructure story because it puts numbers and mechanisms behind a common training bottleneck: GPUs waiting on data and checkpoints. Rapid Bucket uses zonal object storage, direct paths into Colossus, persistent bidirectional gRPC streams, and transparent gcsfs/fsspec integration so PyTorch, Lightning, Dask, Hugging Face Datasets, Ray Data, W&B, and vLLM-style workflows can hit the faster storage path without rewriting application code. Technical depth angle: explain fsspec as the Python filesystem abstraction, gcsfs auto-detecting Rapid buckets, BidiReadObject/BidiWriteObject behavior, zonal co-location, checkpoint append support, 15+ TiB/s aggregate throughput claims, 4.8x read and 2.8x write microbenchmarks, the reported 23% training-time gain, and the operational tradeoff between zonal speed and regional durability.

## Show Notes
```md
OPENCLAW DAILY — EPISODE 043 — April 30, 2026

[00:00] INTRO / HOOK
OpenClaw v2026.4.27 is the latest stable release in the GitHub release list, and the recent episode notes already covered v2026.4.26, v2026.4.25, and v2026.4.24. Under the release-selection rule, that means the valid release block for EP043 is exactly v2026.4.27.

This is a dense operator release. Codex Computer Use gets an actual setup path. DeepInfra becomes a bundled provider. Docker sandboxes gain opt-in GPU passthrough. Agent chat attachments are handled more explicitly. Outbound proxy routing becomes an operator-managed setting. Tencent Yuanbao and QQBot expand the channel surface. Plugin startup and model catalogs keep moving toward manifest-owned metadata. And the fix list is a very long tour through the places real agent systems usually break: Telegram, Slack, Discord media jobs, cron delivery, session defaults, plugin runtime deps, provider replay, gateway startup, updates, Windows handoffs, and channel media.


[02:00] STORY 1 — OpenClaw v2026.4.27 Makes Computer Use and Provider Surfaces More Operable
Start with Codex Computer Use, because it is one of the clearest operator-facing changes in the release.

OpenClaw now ships Codex Computer Use setup with status and install commands, marketplace discovery, optional auto-install, and fail-closed MCP checks before Codex-mode turns start. The important phrase is fail-closed. A computer-use feature should not let an agent begin a desktop-control turn while the required MCP server is missing, misconfigured, or invisible to the runtime. That is how users end up debugging phantom capability: the model thinks it can act, the product shell says it can act, but the driver or bridge underneath is not actually ready.

So the release turns setup into a first-class preflight. `/codex computer-use status` is the inspection surface. `/codex computer-use install` is the repair path. Marketplace discovery gives the runtime a way to find the correct integration. The fail-closed MCP checks make the boundary explicit: if the desktop-control server is not available, do not start the turn as if it is. That is boring in the best possible way, because reliable computer use depends on knowing the difference between a capability that exists in the product and a capability that is actually wired up in the current environment.

There is a related documentation change around Codex Computer Use, direct `cua-driver mcp`, and OpenClaw.app’s PeekabooBridge. That matters because desktop control now has multiple possible setup paths. A local app bridge, a direct MCP driver, and a Codex-mode setup all sound similar from the outside, but operationally they can differ in process lifetime, permissions, screenshot availability, input injection, browser focus, and failure recovery. EP043 should explain that the product is trying to make those choices legible instead of leaving them as tribal knowledge.

The second big release area is provider expansion. DeepInfra joins the bundled provider set with `DEEPINFRA_API_KEY` onboarding, dynamic OpenAI-compatible model discovery, image generation and editing, image and audio understanding, TTS, text-to-video, memory embeddings, static catalog metadata, and provider-owned base URL policy. That is not just a new logo in a model dropdown. It expands the kinds of workloads OpenClaw can route through one provider: text, media generation, media understanding, speech, video, and embeddings.

The operator detail is model discovery and provider-owned policy. When a provider is OpenAI-compatible, it is tempting to treat it as just another base URL. But real provider support needs onboarding, catalog metadata, capability flags, media support, auth hints, embedding behavior, fallback semantics, and base URL ownership. Otherwise every compatible endpoint becomes a custom snowflake with surprising model names and half-known capabilities. DeepInfra being bundled means the runtime can expose it as a managed provider surface instead of forcing users to hand-roll every edge.

[11:30] STORY 1B — Sandboxes, Proxies, Attachments, and Device Presence Get Sharper
The Docker sandbox change is small but very important for local AI workflows: OpenClaw adds opt-in `sandbox.docker.gpus` passthrough for Docker sandbox containers when the host runtime supports `--gpus`.

That is the right default shape. GPU access inside a sandbox is powerful and useful, but it should be explicit. Local model serving, image generation, video processing, computer vision, and evaluation jobs often need hardware acceleration. But exposing GPUs to arbitrary sandboxed agent work also widens the resource and driver surface. Making it opt-in gives operators a knob: this sandbox may use the GPU; this other sandbox stays CPU-only. That becomes especially relevant when an agent can install dependencies, run model tooling, or execute long jobs that might monopolize VRAM.

The release also adds operator-managed outbound proxy routing with `proxy.enabled`, `proxy.proxyUrl`, and `OPENCLAW_PROXY_URL`. The notes call out strict `http://` forward-proxy validation, a loopback-only Gateway bypass, and cleanup of proxy environment and dispatcher state on exit. That is a good security shape. It acknowledges that some installations need a controlled outbound path for compliance, inspection, corporate networking, or egress restrictions, but it does not silently route internal Gateway traffic through the same path or leave stale proxy state after shutdown.

Gateway chat attachment behavior improves too. Non-image attachments sent through `chat.send` can now be staged as agent-readable media paths, while unsupported RPC attachment paths are explicit instead of silently dropping files. This matters for agent UX because an attachment that disappears is worse than an attachment that fails clearly. Operators need to know whether a file is readable by the agent, whether it became media, whether the channel provider accepted it, and whether a non-supported path was rejected.

On mobile and paired nodes, iOS and Android now publish authenticated `node.presence.alive` events and expose last-seen fields so background wakes can mark paired nodes recently alive without treating them as connected. That distinction matters in distributed assistant systems. A node can be alive recently without being connected right now. If the runtime collapses those states into one boolean, it either over-promises availability or loses useful liveness information. Last-seen metadata lets scheduling, diagnostics, and UX describe the state more honestly.

[18:30] STORY 1C — Manifest-First Startup and Model Catalogs Reduce Runtime Guesswork
A lot of v2026.4.27 is about moving catalog and plugin metadata out of heavy runtime imports and into manifests.

Bundled plugin manifests now declare explicit `activation.onStartup` behavior. There is also a future-mode gate for disabling deprecated implicit startup sidecar loading, plus compatibility warnings to move plugin authors toward explicit metadata. The practical point is simple: Gateway startup should not import every possible plugin sidecar just to find out whether it has startup work to do. Startup is where slow dependency trees, network checks, stale plugin state, and accidental side effects hurt the most.

The release also wires manifest `modelCatalog.aliases` and `modelCatalog.suppressions` into model-catalog planning. Provider catalogs for Qianfan, Xiaomi, NVIDIA, Cerebras, Mistral, Moonshot, DeepSeek, Tencent TokenHub, StepFun, BytePlus, Volcano Engine, Fireworks, and Together AI move toward plugin manifest rows. This is the same architectural move from another angle: make provider rows, aliases, suppressions, and endpoint metadata inspectable without forcing runtime normalization through a wide plugin universe.

For builders, the lesson is that model catalogs are infrastructure, not just UI. If the product has to answer “which models exist,” “which provider owns this model,” “which aliases are valid,” and “which stale rows should be hidden,” that information should be close to the provider contract. Otherwise every list command, setup flow, gateway boot, and provider discovery path risks doing too much work and returning slightly different answers.

There is a strong SDK and testing story here too. The release exposes focused plugin SDK subpaths for channel routes, channel test helpers, channel target testing, plugin runtime fixtures, provider catalog helpers, media provider capability assertions, and many contract helpers that used to live in repo-only test bridges. That is not directly user-visible, but it is important product hygiene. Extension authors and bundled plugins should test against documented SDK surfaces, not private test directories that can move underneath them.

[25:00] STORY 1D — Reliability Fixes Show Where Agent Runtimes Actually Hurt
The v2026.4.27 fix list is long, and the show should not read every item. Instead, group the fixes by operator pain.

First: channel delivery. Telegram gets better multi-bot native approval routing, bounded outbound Bot API calls, cached bundled plugin alias lookup, and cron topic preservation with `--thread-id`. Slack gets socket-mode ping/pong timeout controls and bounded private file and forwarded attachment downloads. Mattermost stops duplicating regular inbound posts as system events. LINE persists inbound media under managed media storage instead of temporary files that can disappear. These are the kinds of fixes that matter when OpenClaw is not just a local CLI, but a multi-channel assistant that has to survive slow providers, forum topics, file downloads, media retention, and channel-specific semantics.

Second: async media and tasks. Detached `video_generate` and `music_generate` tool contexts stay registered until terminal status, long-running provider jobs remain fresh, and session-scoped task records infer ownership. That fixes a nasty class of product failure where a generation job is still alive at the provider, but the parent chat context or task table thinks it is lost. For Discord-backed media generation especially, the user experience depends on the runtime tracking a long external job across turns.

Third: sessions, models, and replay. `chat.history` and `sessions.list` thinking defaults now align with owning-agent and catalog-aware resolution. DeepSeek V4 reasoning content gets backfilled on replay paths. Anthropic beta headers are constrained to direct public Anthropic endpoints instead of custom compatible providers. Config-heavy tool responses stop replaying giant redacted configs into transcripts. Those all point to the same theme: once agents use multiple providers, tool calls, transcripts, replay, and per-agent defaults, the runtime must preserve enough state to continue correctly without accidentally sending the wrong metadata to the wrong backend.

Fourth: startup, updates, and plugin runtime dependencies. Gateway startup no longer waits for primary model prewarm before starting chat channels. Disabled tracked plugins are skipped during post-update sync. Bundled runtime deps and mirrors get lighter, more cache-aware, and safer during restarts. Plugin inspection loads only the matched plugin. Plugin uninstall plans from metadata instead of runtime-loading everything. This is exactly what operators feel as “OpenClaw starts faster” or “updates do not wedge my instance,” even though the underlying fixes are mostly dependency and metadata discipline.

The release verdict: v2026.4.27 is not a single-feature episode. It is a runtime-operations release. It makes computer use safer to start, providers easier to onboard, sandboxes more capable, channels more explicit, plugin startup less heavy, and long-running jobs harder to lose.

[31:00] STORY 2 — Deepgram Flux Multilingual Makes Voice-Agent STT a Turn-Taking Runtime Problem
Deepgram’s Flux Multilingual is a good voice-agent story because it is not just “more languages.” It changes how builders should think about the speech recognition layer inside realtime agents.

The model is `flux-general-multi`, and Deepgram says it supports English, Spanish, French, German, Hindi, Russian, Portuguese, Japanese, Italian, and Dutch with code switching. The key architectural promise is one streaming connection rather than routing every utterance through separate language-specific recognizers. That matters because a multilingual conversation can change language mid-call, mix languages inside one turn, or start in a language the system did not predict.

The API details are what make it operationally interesting. Flux uses the `/v2/listen` WebSocket path. Language prompting uses `language_hint` to bias recognition. Detected languages appear on `TurnInfo` events through fields such as `languages`. End-of-turn behavior is configurable with thresholds like `eot_threshold`, `eager_eot_threshold`, and `eot_timeout_ms`. Those are not cosmetic flags. They control the voice-agent loop: when to stop listening, when to start generating, when to risk an early response, and when to wait because the user may still be speaking.

For a voice agent, STT latency and turn detection are product behavior. If end-of-turn fires too early, the agent interrupts. If it fires too late, the agent feels sluggish. If code switching is handled by a routing layer outside the model, the system may spend extra time guessing languages and reconnecting streams. If language hints are too narrow, recognition may degrade when the speaker switches. The practical recommendation is to treat STT as part of the runtime loop, not a black-box transcript service.

The self-hosted documentation adds another important angle: Flux wants dedicated infrastructure. Deepgram says Flux must run on a separate Engine instance from other STT and TTS models, must be explicitly enabled in Engine and API TOML files, uses `/v2/listen`, and allocates GPU memory for Flux streams on startup. You select `flux-general-multi` in the `[flux]` section, configure `max_streams`, and monitor `flux_max_streams`, `flux_used_streams`, and `flux_fraction_streams`.

That is exactly the kind of operational detail voice-agent builders need. If `max_streams` is too high, the symptoms are not abstract: delayed responses, dropped calls, API errors, and unstable latency. If the model is accidentally running on CPU, the docs call out high latency, OOM-style failures, and the need for GPU health checks. If Flux is placed on the same Engine node as other models, memory pressure can break unrelated requests. The builder takeaway: multilingual voice agents need capacity planning at the streaming layer, not just a bigger LLM behind the transcript.

[39:00] STORY 3 — Google Rapid Bucket Brings Colossus into the PyTorch Data Path
Google’s Rapid Bucket post is a strong AI infrastructure story because it is about the part of training that is easy to ignore until the GPUs are expensive and idle: feeding data and writing checkpoints.

The core mechanism is Rapid Storage, powered by Google’s Colossus storage architecture, exposed to PyTorch through gcsfs and the fsspec interface. fsspec matters because it is already a common Python filesystem abstraction used around data preparation, checkpoints, and inference tooling: Dask, Pandas, Hugging Face Datasets, Ray Data, PyTorch Lightning, distributed PyTorch paths, Weights & Biases, and vLLM-adjacent workflows. If the storage backend can get faster behind fsspec, a lot of AI code can benefit without custom storage adapters.

Rapid Bucket changes the data path by using dedicated zonal buckets, direct connectivity to underlying Colossus files, and persistent bidirectional gRPC streams through APIs such as BidiReadObject and BidiWriteObject. That replaces the repeated overhead of more traditional REST-style object access with stateful streaming. The post also calls out bucket-type auto-detection in gcsfs, so existing `fsspec.open()` style code can use the faster path when the bucket is Rapid.

The numbers are useful: Google cites 15+ TiB/s aggregate throughput, a 23% training-time improvement in a benchmark using 16 GKE nodes with eight A4 GPUs each, 4.8x read throughput improvement, and 2.8x write throughput improvement in microbenchmarks with 16MB I/O sizes across 48 processes. The exact result for any workload will vary, but the mechanism is clear enough to discuss: fewer network hops, persistent streams, lower per-operation overhead, zonal co-location, and checkpoint append support.

The tradeoff is locality. Zonal co-location is why the fast path works, but it also changes the failure and architecture model. If your training job runs in one zone and the data sits in a Rapid bucket in that zone, the latency profile improves. But you still need to think about regional durability, dataset replication, checkpoint backup, and what happens if the zone becomes unavailable. For production training systems, that means separating the hot training path from the durable archival path. Use the fast zonal bucket to keep accelerators busy; copy important checkpoints and data products to a regional or multi-region durability layer when the workflow requires it.

The OpenClaw-relevant takeaway is that agent and model infrastructure increasingly depends on boring data paths. A model is not just a GPU and a checkpoint. It is object storage, file abstractions, stream protocols, scheduler locality, checkpoint frequency, and recovery strategy. If the data path stalls, the smartest accelerator fleet becomes a very expensive waiting room.

[45:00] OUTRO
The practical takeaway from EP043 is operational control. OpenClaw v2026.4.27 makes computer use, providers, channels, startup, and reliability easier to operate. Deepgram shows that voice agents need streaming and turn-taking controls, not just transcripts. Google shows that AI training performance can hinge on storage protocols, filesystem abstractions, stream protocols, checkpoint behavior, and zonal locality.
```

## Verified Links
- OpenClaw — Release `v2026.4.27`: https://github.com/openclaw/openclaw/releases/tag/v2026.4.27
- OpenClaw — Release API for `v2026.4.27`: https://api.github.com/repos/openclaw/openclaw/releases/tags/v2026.4.27
- Deepgram — Flux Multilingual announcement: https://deepgram.com/learn/deepgram-launches-flux-multilingual-press-release
- Deepgram — Flux Multilingual technical deep dive: https://deepgram.com/learn/flux-multilingual-technical-deep-dive
- Deepgram Docs — Flux feature overview: https://developers.deepgram.com/docs/flux/feature-overview
- Deepgram Docs — Using Flux self-hosted: https://developers.deepgram.com/docs/flux-self-hosted
- Google Developers Blog — Speeding Up AI: Bringing Google Colossus to PyTorch via GCSFS and Rapid Bucket: https://developers.googleblog.com/speeding-up-ai-bringing-google-colossus-to-pytorch-via-gcsfs-and-rapid-bucket/
- Google Cloud Storage Docs — Rapid Bucket: https://docs.cloud.google.com/storage/docs/rapid/rapid-bucket
- fsspec/gcsfs — Rapid storage support benchmarks: https://github.com/fsspec/gcsfs/blob/main/docs/source/rapid_storage_support.rst#performance-benchmarks

## Chapters
- **[00:00] Hook — OpenClaw v2026.4.27 Leads EP043**
- **[02:00] OpenClaw v2026.4.27 Makes Computer Use and Provider Surfaces More Operable**
- **[11:30] Sandboxes, Proxies, Attachments, and Device Presence Get Sharper**
- **[18:30] Manifest-First Startup and Model Catalogs Reduce Runtime Guesswork**
- **[25:00] Reliability Fixes Show Where Agent Runtimes Actually Hurt**
- **[31:00] Deepgram Flux Multilingual Makes Voice-Agent STT a Turn-Taking Runtime Problem**
- **[39:00] Google Rapid Bucket Brings Colossus into the PyTorch Data Path**
- **[45:00] Outro**
