# OpenClaw Daily — Episode 12 Show Notes
**"Free Frontier Models, Multimodal Memory & Community Automations That'll Blow Your Mind"**
📅 March 12, 2026
🔗 Release: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11

---

## Episode Summary
v2026.3.11 dropped with two stealth free frontier models, Google's first native multimodal embedding model lands in OpenClaw, a full Ollama onboarding wizard, ACP session resume for long coding sessions, and iOS/macOS app polish. Plus: a deep dive into real community automations saving people serious time.

---

## Community Spotlight — Top Automations from BetterClaw

Real OpenClaw users, real time saved. From the BetterClaw top 10:

1. **Morning Briefings** — Calendar + email synthesis, context-aware draft responses, before you wake up
2. **Email Triage** — Auto-categorize, draft responses, schedule appointments — fully local and private
3. **Family Calendar Assistant** — Conflict detection, scheduling, direct family messaging
4. **Self-Healing Home Server** — Monitors services, attempts fixes automatically, alerts only on the unexpected
5. **Personal Knowledge Base (RAG)** — Semantic search across all notes, docs, and code

Featured community build: 5,000+ notes, 15 cron jobs, 24 custom scripts — fully automated sysadmin with hourly health checks, daily briefings, and weekly security audits. Context-aware AI reasoning, not just dumb scripts.

---

## New Free Models — Hunter Alpha & Healer Alpha
Both available now on OpenRouter at $0.00/M tokens. (Free tier may be temporary.)

**Hunter Alpha**
- 1 trillion parameters
- 1 million token context window
- Optimized for agentic use cases
- https://openrouter.ai/openrouter/hunter-alpha

**Healer Alpha**
- Frontier omni-modal: vision, hearing, reasoning, action
- 262K context window
- https://openrouter.ai/openrouter/healer-alpha

---

## Multimodal Memory — Gemini Embedding 2
Google announced Gemini Embedding 2 on March 11. OpenClaw integrated it same day.
https://deepmind.google/technologies/gemini/

- First native multimodal embedding model — text, images, video, audio, PDFs in one shared vector space
- Native audio support (no transcription step)
- 8,192 token input limit (4× previous)
- Outperforms Amazon Nova 2 and Voyage Multimodal 3.5 on benchmarks
- Configurable output dimensions with auto-reindex on change
- Strict fallback gating — no silent degradation

Use case: Ask your agent "find that article about deployment pipelines" — it surfaces a screenshot, a voice note, AND a text file, all at once. Meaning over keywords.

---

## Ollama — Full First-Class Onboarding Wizard
Ollama hit 10 billion pulls: https://ollama.com
Community guides (dev.to, FreeCodeCamp) had thousands of readers doing manual setup. Now it's built into the wizard.

Two modes:
- **Local** — 100% offline, all inference on-device, zero cloud, maximum privacy
- **Cloud+Local** — Hybrid: local for quick tasks, cloud for heavy reasoning. Smart model pull skipping in cloud mode.

---

## ACP & Developer Tooling

**ACP Session Resume** (`resumeSessionId`)
- Resume a subagent conversation across restarts — no re-explaining context
- Transcript replay on `loadSession`
- Image attachment forwarding — visual context preserved on resume
- ACP tool streaming now includes file-location hints
- `OPENCLAW_CLI` env var set in child processes

https://docs.openclaw.ai/acp

---

## App Updates

**iOS:**
- New welcome screen with live agent overview
- Floating controls replaced with docked toolbar
- Chat opens in resolved main session — context persists across devices

**macOS:**
- Switch models directly from conversation view — no new session needed
- Thinking-level preferences persist across restarts
- LaunchAgent restart hardening

**OpenCode Go provider** — Zen + Go now share one key in the wizard setup

---

## OpenClaw Backup (landed March 8)
```
openclaw backup create
openclaw backup verify
openclaw backup create --only-config
```
Backs up config, state, and workspace. Use it.
https://docs.openclaw.ai/cli/backup

---

## Key Links
- Release v2026.3.11: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11
- Hunter Alpha: https://openrouter.ai/openrouter/hunter-alpha
- Healer Alpha: https://openrouter.ai/openrouter/healer-alpha
- Ollama: https://ollama.com
- Gemini Embedding 2: https://deepmind.google/technologies/gemini/
- OpenClaw docs: https://docs.openclaw.ai
- Community Discord: https://discord.com/invite/clawd
