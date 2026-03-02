# Show Notes - Episode 9: OpenClaw v2026.3.1 — Threads, Topics, Android Actions, and Health Checks

## Episode Details
- **Episode:** 9
- **Release Covered:** OpenClaw **v2026.3.1**
- **Hosts:** Nova (warm British) & Alloy (American)
- **Duration Target:** 30-40 minutes

## Topics Covered (with sources)

### 1) The v2026.3.1 Release: Why This One Matters
- A “daily driver” release: fewer paper cuts, more reliable automation, better device control.
- **Sources:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 2) Discord Thread Sessions Finally Behave Like Real Workspaces
- Thread lifecycle moves from fixed TTL to **inactivity-based** sessions (idleHours default 24h), with optional hard maxAgeHours.
- New commands: `/session idle` and `/session max-age`.
- **Sources:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/27845
  - https://docs.openclaw.ai/channels/discord

### 3) Telegram DM Topics: One Person, Multiple Workstreams (Safely)
- Per-DM direct + topic config (allowlists, dmPolicy, skills, systemPrompt, requireTopic).
- Topic-aware authorization + debounce for messages, callbacks, commands, reactions.
- **Sources:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/30579

### 4) Android Nodes Level Up: Notification Actions + Device Health
- New Android node commands: camera.list, device.permissions, device.health.
- Notification actions: open, dismiss, reply.
- **Sources:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28260
  - https://docs.openclaw.ai/platforms/android

### 5) Container Health Probes: Ready for Docker and Kubernetes
- Built-in liveness/readiness endpoints: /health, /healthz, /ready, /readyz.
- Designed to not shadow existing handlers.
- **Sources:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/31272
  - https://docs.openclaw.ai/gateway/health

### 6) OpenAI Responses Goes WebSocket-First (Streaming That Doesn’t Randomly Fall Apart)
- WebSocket-first transport by default with SSE fallback.
- Shared WS runtime wiring + per-session cleanup.
- **Sources:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 7) Cron and Automation Runs: “Light Context” Mode
- Opt-in lightweight bootstrap mode for cron/automation runs to reduce noise and reduce failure modes.
- **Sources:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/26064

### 8) Builder Candy (Optional): A Diffs Tool and Better i18n
- A diffs plugin tool for read-only diff rendering.
- Web UI adds German locale.
- **Sources:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28495

## Key Takeaways
1. **Threads and topics make sessions feel like real project spaces** instead of a pile of chat messages.
2. **Android notification actions** are the first step toward credible on-device assistant workflows.
3. **Health probes + better streaming transports** move OpenClaw closer to “run it like a service” reliability.
4. **Light-context cron** reduces automation noise and helps prevent spammy outputs.

## Links Mentioned
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
- https://github.com/openclaw/openclaw/pull/27845
- https://docs.openclaw.ai/channels/discord
- https://github.com/openclaw/openclaw/pull/30579
- https://github.com/openclaw/openclaw/pull/28260
- https://docs.openclaw.ai/platforms/android
- https://github.com/openclaw/openclaw/pull/31272
- https://docs.openclaw.ai/gateway/health
- https://github.com/openclaw/openclaw/pull/26064
- https://github.com/openclaw/openclaw/pull/28495

---
*Episode 9 | Draft show notes for approval*
