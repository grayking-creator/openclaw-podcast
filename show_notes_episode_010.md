# Show Notes — Episode 10: The Document & Memory Revolution

## Episode Details
- **Episode:** 10
- **Date:** March 4, 2026
- **Hosts:** Nova (warm British) & Alloy (American)
- **Duration Target:** 30-35 minutes
- **Theme:** OpenClaw evolves from chat/agent platform into a full document and memory platform

---

## Part 1 — From the Release: OpenClaw March 3, 2026
**Release notes:** https://github.com/openclaw/openclaw/releases/tag/v2026.3.2

Everything in this section shipped in the March 3 release:

### 1. PDF Analysis Tool *(NEW)*
- First-class `pdf` tool — native Anthropic/Google support (model sees PDF directly), extraction fallback for all others
- Configurable: `agents.defaults.pdfModel`, `pdfMaxBytesMb`, `pdfMaxPages`
- What this unlocks: contracts, invoices, research papers, any document you actually work with

### 2. Ollama Memory Embeddings *(NEW — deep dive in episode)*
- `memorySearch.provider = "ollama"` — full local memory/RAG stack, zero cloud API required
- The first time you can run everything — inference AND memory — without touching a cloud provider
- Honrs `models.providers.ollama` settings for embedding requests
- Why this matters: your agent can now remember thousands of interactions using only local compute

### 3. SecretRef Expansion *(NEW)*
- 64 credential targets now covered with SecretRef
- Fail-fast on unresolved refs on active surfaces — no silent failures
- Covers: runtime collectors, secrets planning/apply/audit, onboarding SecretInput UX

### 4. Sessions Attachments *(NEW)*
- `sessions_spawn` supports inline file attachments (subagent runtime)
- Base64/utf8 encoding, lifecycle cleanup, limits via `tools.sessions_spawn.attachments`
- Agents can now pass files directly to each other

### 5. Telegram Streaming Defaults
- Streaming now defaults to `partial` (was `off`) — live preview out of the box for new setups
- DM streaming uses `sendMessageDraft` for private preview

### 6. MiniMax-M2.5-highspeed
- First-class support across catalogs and onboarding — faster variant of MiniMax-M2.5

### 7. CLI Config Validation
- `openclaw config validate --json` — catch errors before gateway startup
- Detailed invalid-key paths in startup errors

### 8. Zalo Personal Plugin Rebuilt
- Native `zca-js` integration, fully in-process — no external CLI transport

### 9. Multi-Media Outbound
- Discord, Slack, WhatsApp, Zalo unified with shared `sendPayload` + multi-media iteration

### 10. Plugin SDK / STT
- `api.runtime.stt.transcribeAudioFile()` — extensions can now do speech-to-text

---

## Part 2 — This Week in OpenClaw

### Article 1: OpenClaw Surpasses 250,000 GitHub Stars
**Source:** ainvest.com — March 3, 2026
**URL:** https://www.ainvest.com/news/openclaw-github-star-count-surpasses-250-000-ai-agent-boom-2603/

OpenClaw hit 250,000 GitHub stars — the fastest AI project to reach that milestone. The article also highlights that C3.ai (enterprise AI) missed revenue forecasts by 30% and announced a 26% workforce reduction. The contrast is striking: enterprise AI stumbling while open-source, self-hosted AI explodes. OpenClaw's local-first design and multi-platform support are cited as key differentiators.

### Article 2: Inside OpenClaw — The Architecture That Explains Everything
**Source:** dev.to — March 4, 2026
**URL:** https://dev.to/jiade/inside-openclaw-how-the-worlds-fastest-growing-ai-agent-actually-works-under-the-hood-4p5n

A deep technical dive into why OpenClaw grew while hundreds of other AI agent frameworks didn't. Covers: the Pi SDK embedding strategy, the two-layer memory system, the Lane Queue concurrency model, and the heartbeat engine. The thesis: it's not marketing, it's architecture. Good episode fodder for explaining what makes this platform different from LangChain, AutoGPT, and others.

### Article 3: OpenClaw In The Real World (Production Patterns)
**Source:** Trilogy AI / Rahul Subramaniam — March 3, 2026
**URL:** https://trilogyai.substack.com/p/openclaw-in-the-real-world

The reality check article. Covers three failure modes people hit after the initial setup high: memory breaks down, you lose work when the machine restarts, and reliability starts mattering more than experimentation. Provides production patterns for moving from "cool demo" to a system you actually depend on. Connects directly to Episode 10's memory theme.

---

## Key Takeaway
This release crosses a threshold: document analysis + persistent local memory + inter-agent file passing = OpenClaw as a second brain, not just a chat interface. The 250K star milestone and the real-world production article both signal the same thing — people aren't experimenting anymore, they're depending on this.

## Build Patterns Discussed
1. **Legal Document Reviewer** — PDF tool + memory + Slack output
2. **Local Research Assistant** — Ollama embeddings + PDF tool, zero cloud API
3. **Secure Credential Pipeline** — SecretRef + sessions attachments for multi-agent workflows

---
📋 Full script: `openclaw-podcast/episode_010.md` (3,530 words)
✅ Topic audit: all topics verified clean against Episodes 0–9
⏳ **Awaiting your approval to proceed to audio generation**
