# EP026 — OpenClaw Gets a Brain Transplant, Glasswing, Giant Brains, and Cloned Writers
**OpenClaw Daily** | April 8, 2026 | ~37 min

## Episode Title
**OpenClaw Gets a Brain Transplant, Glasswing, Giant Brains, and Cloned Writers**

## Tagline
OpenClaw 2026.4.8 ships a unified inference layer, session checkpointing, and a fully restored memory stack — then Anthropic calls in the tech giants to fight AI vulnerabilities with AI, a new paper trains 120B parameters on one GPU, and a fingerprinting study reveals your writing AI is probably a Claude clone.

## Story Slate

1. **OpenClaw 2026.4.8 — The Release That Changes How It All Works**
   The anchor story. Six major subsystems land in one release: a new infer hub CLI that unifies routing across providers, a media generation auto-fallback system that eliminates an entire class of failures, a sessions branch-and-restore UI that creates checkpoints before context compaction, full restoration of the memory and wiki stack with structured claims, evidence, contradiction clustering and freshness-weighted search, a webhook ingress plugin for external automation, and a pluggable compaction provider registry so you can route summarisation to a faster/cheaper model. Plus Google Gemma 4 support, Claude CLI restored as the preferred local Anthropic path, Ollama vision models natively, and a batch of security-relevant fixes covering host exec sanitisation, allowlist authorization, and multi-channel gateway startup errors.

2. **Project Glasswing: The Cyber Defense Coalition**
   Anthropic assembled basically every major tech and finance company to unleash Claude Mythos Preview — an unreleased frontier model that found thousands of zero-days including a 27-year-old OpenBSD bug and a 16-year-old FFmpeg flaw. The pitch: AI breaks things faster than humans can fix them, so fight AI with AI. $100M in credits, $4M to open-source security orgs. Great premise, worth discussing what "coalition" really means when Anthropic is holding the keys.

3. **MegaTrain: 100B+ Parameters, One GPU**
   A new paper drops a technique that stores model weights and optimizer state in host CPU memory and treats GPUs as disposable compute units. Result: 120B parameter training on a single H200 with 1.5TB RAM, 1.84x faster throughput than DeepSpeed ZeRO-3 on 14B models. This is a big deal for anyone who thought you needed a full cluster to train frontier-scale models.

4. **Your AI Writer Is Probably a Claude Clone**
   A fingerprinting study of 178 AI models found 9 clone clusters with >90% style similarity. Most striking: Gemini 2.5 Flash Lite writes 78% like Claude 3 Opus — at 185x lower cost. The implications for "AI slop" and how model convergence happens even across totally different training runs are worth unpacking.

5. **LLM Plays Shoot-'Em-Up on a 40-Year-Old 8-bit Machine**
   GPT-4o connected to a Commander X16 emulator via text summaries of game state — no pixels, no audio. It developed strategies, kept notes between turns, and found an exploit in the built-in AI. A fun, low-budget demo that shows structured reasoning can emerge from surprisingly minimal input.

## Show Notes
```md
OPENCLAW DAILY — EPISODE 026 — April 8, 2026

[00:00] INTRO / HOOK
OpenClaw 2026.4.8 drops a unified inference layer, session checkpointing,
and a restored memory stack. Anthropic's Glasswing coalition, MegaTrain's
single-GPU frontier training, and a study proving your writing AI might
just be a Claude knockoff.

[02:00] STORY 1 — OpenClaw 2026.4.8: The Release That Changes How It All Works
Six major subsystems land in one release.

The first is the infer hub CLI — openclaw infer hub — a unified interface
for provider-backed inference across model tasks, media generation, web
search, and embeddings. It routes requests to the right provider, handles
auth, remaps parameters across provider capability differences, and
falls back automatically if a provider is down or rate-limited. If you
have been managing multiple provider configs across different workflows,
the hub becomes the single abstraction layer. Provider switches become
config changes at the hub level; the rest of your workflow is unchanged.

The second is the media generation auto-fallback system, covering image,
music, and video. If your primary provider is unavailable or does not
support the specific capability you requested — aspect ratio, duration,
format — OpenClaw routes to the next configured provider and adjusts
parameters automatically. One failed generation is an inconvenience. A
thousand per day across a production fleet is an operational problem. This
is handled once at the platform level; every agent benefits immediately.

The third is the sessions UI branch and restore functionality. When
context compaction runs, the system now snapshots session state before
summarising. Operators can use the Sessions UI to inspect checkpoints and
restore to a pre-compaction state, or use any checkpoint as a branch point
to explore a different direction without losing the original thread. This
is version history for session context — the difference between editing
with autosave and editing where every save overwrites the previous file.

The fourth is the full restoration of the memory and wiki stack. This
includes structured claim and evidence fields, compiled digest retrieval,
claim-health linting, contradiction clustering, staleness dashboards, and
freshness-weighted search. Claims can be tagged with supporting evidence,
linted for internal consistency, and grouped where they contradict each
other. Search results are ranked by recency, not just relevance. If you
have been working around missing pieces in prior versions, this is the
native implementation — test your workflow against it.

The fifth is the webhook ingress plugin. Per-route shared-secret endpoints
let external systems authenticate and trigger bound TaskFlows directly —
CI pipelines, monitoring tools, scheduled jobs, third-party webhooks —
without custom integration code. The plugin handles routing, auth, and
workflow binding.

The sixth is the pluggable compaction provider registry. You can now route
context compaction to a different model or service via
agents.defaults.compaction.provider — a faster, cheaper model optimised
for summarisation rather than the most capable model you have. Falls back
to built-in LLM summarisation on failure. At scale, compaction is
happening constantly; routing it appropriately matters for cost and
latency.

Other notable additions: Google Gemma 4 is now natively supported with
thinking semantics preserved and Google fallback resolution fixed. Claude
CLI is restored as the preferred local Anthropic path across onboarding,
doctor flows, and Docker live lanes. Ollama vision models now accept image
attachments natively — vision capability is detected from /api/show, no
workarounds required. The memory and dreaming system ingests redacted
session transcripts into the dreaming corpus with per-day session-corpus
notes and cursor checkpointing. A new bundled Arcee AI provider plugin
with Trinity catalog entries and OpenRouter support. Context engine changes
expose availableTools, citationsMode, and memory artifact seams to
companion plugins — a better extension API.

Security-relevant fixes: host exec and environment sanitisation now blocks
dangerous overrides for Java, Rust, Cargo, Git, Kubernetes, cloud
credentials, and Helm. The /allowlist command now requires owner
authorization before changes apply. Slack proxy support is working
correctly — ambient HTTP/HTTPS proxy settings are honoured for Socket Mode
WebSocket connections including NO_PROXY exclusions. Gateway startup errors
across all bundled channels (Telegram, BlueBubbles, Feishu, Google Chat,
IRC, Matrix, Mattermost, Teams, Nextcloud, Slack, Zalo) are resolved via
the packaged top-level sidecar fix.
→ github.com/openclaw/openclaw/releases

[12:00] STORY 2 — Project Glasswing: The Cyber Defense Coalition
Anthropic launched Project Glasswing with a coalition of Amazon, Apple,
Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Microsoft, NVIDIA,
Palo Alto Networks and others. The centerpiece is Claude Mythos Preview —
an unreleased frontier model scoring 83.1% on CyberGym vs 66.6% for Opus
4.6. In testing it found thousands of zero-day vulnerabilities, including
a 27-year-old OpenBSD bug and a 16-year-old FFmpeg flaw. Anthropic is
committing $100M in usage credits and $4M in donations to open-source
security orgs. The core thesis: offensive AI capability has outpaced human
defensive response time, so the same capability must be deployed
defensively. Worth discussing: what does "coalition" mean when Anthropic
controls the model? And is finding bugs and patching them actually better
than just not shipping vulnerable code?
→ anthropic.com/glasswing

[20:00] STORY 3 — MegaTrain: Full Precision Training of 100B+ on a Single GPU
MegaTrain enables training 100B+ parameter LLMs on a single GPU by storing
parameters and optimizer states in host (CPU) memory and treating GPUs as
transient compute engines. On a single H200 GPU with 1.5TB host memory,
it reliably trains models up to 120B parameters. It achieves 1.84x the
training throughput of DeepSpeed ZeRO-3 with CPU offloading when training
14B models, and enables 7B model training with 512k token context on a
single GH200. Practical implications: dramatically lowers the hardware
barrier for frontier-scale training, which could accelerate both
legitimate research and... everything else.
→ arxiv.org/abs/2604.05091

[27:00] STORY 4 — 178 AI Models Fingerprinted: Gemini Flash Lite Writes 78% Like Claude 3 Opus
A research project created stylometric fingerprints for 178 AI models
across lexical richness, sentence structure, punctuation habits, and
discourse markers. Nine clone clusters showed >90% cosine similarity.
Headline finding: Gemini 2.5 Flash Lite writes 78% like Claude 3 Opus but
costs 185x less. The convergence suggests frontier models are hitting
similar optimal patterns despite different architectures and training data
— or that Claude's style is just a strong attractor for RLHF. Implications
for AI detection tools, originality claims, and the economics of "good
enough" AI writing.
→ news.ycombinator.com/item?id=47690415

[32:00] STORY 5 — LLM Plays Shoot-'Em-Up on 8-bit Commander X16 via Text Summaries
A developer connected GPT-4o to an 8-bit Commander X16 emulator using
structured text summaries ("smart senses") derived from touch and EMF-
style game inputs. The LLM maintains notes between turns, develops
strategies, and discovered an exploit in the built-in AI's behavior.
Demonstrates that model reasoning can emerge from minimal structured
input — no pixels, no audio, just text summaries of game state. Fun side
note: the Commander X16 is a modern recreation of an 8-bit home computer
architecture, so it's running on actual hardware emulated in software.
→ news.ycombinator.com/item?id=47689550

[35:30] OUTRO / CLOSE
Next episode drops tomorrow. If you want a transcript, reply on Telegram.

→ Reply on Telegram to approve transcript generation.
```

## Links
- OpenClaw 2026.4.8 release notes: https://github.com/openclaw/openclaw/releases
- Project Glasswing: https://www.anthropic.com/glasswing
- MegaTrain paper: https://arxiv.org/abs/2604.05091
- AI fingerprinting study (HN): https://news.ycombinator.com/item?id=47690415
- LLM Commander X16 demo (HN): https://news.ycombinator.com/item?id=47689550

## Chapters
- **[00:00] Hook — OpenClaw Gets a Brain Transplant, Glasswing, Giant Brains, and Cloned Writers**
- **[02:00] OpenClaw 2026.4.8: Infer Hub, Auto-Fallback, Session Checkpoints & Memory Stack**
- **[12:00] Project Glasswing: The Cyber Defense Coalition**
- **[20:00] MegaTrain: 100B+ Parameters, One GPU**
- **[27:00] 178 AI Models Fingerprinted: Gemini Flash Lite Writes 78% Like Claude 3 Opus**
- **[32:00] LLM Plays Shoot-'Em-Up on 8-bit Commander X16 via Text Summaries**
- **[35:30] Outro**

→ Reply on Telegram to approve transcript generation.
