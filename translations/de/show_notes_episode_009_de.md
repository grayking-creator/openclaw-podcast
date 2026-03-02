# Shownotes – Episode 9: OpenClaw v2026.3.1 — Threads, Topics, Android Actions und Health Checks

## Episodendetails
- **Episode:** 9
- **Release:** OpenClaw **v2026.3.1**
- **Hosts:** Nova (warm britisch) & Alloy (amerikanisch)
- **Ziel-Dauer:** 30–40 Minuten

## Themen (mit Quellen)

### 1) v2026.3.1: Warum dieses Release zählt
- Ein „Daily Driver“-Release: weniger Reibung, zuverlässigere Automatisierung, bessere Device-Kontrolle.
- **Quellen:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 2) Discord-Thread-Sessions verhalten sich endlich wie echte Workspaces
- Lifecycle von fixem TTL zu **Inaktivitäts-basierten** Sessions (idleHours Default 24h) + optionales maxAgeHours.
- Neue Commands: `/session idle` und `/session max-age`.
- **Quellen:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/27845
  - https://docs.openclaw.ai/channels/discord

### 3) Telegram DM Topics: Eine Person, mehrere Workstreams (sicher)
- Konfiguration pro DM + Topic (allowlists, dmPolicy, skills, systemPrompt, requireTopic).
- Topic-aware Authorization + Debounce für Messages, Callbacks, Commands, Reactions.
- **Quellen:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/30579

### 4) Android Nodes: Notification Actions + Device Health
- Neue Android-Kommandos: camera.list, device.permissions, device.health.
- Notification Actions: öffnen, verwerfen, antworten.
- **Quellen:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28260
  - https://docs.openclaw.ai/platforms/android

### 5) Container Health Probes: Ready für Docker und Kubernetes
- Built-in Endpoints: /health, /healthz, /ready, /readyz.
- So gebaut, dass bestehende Handler nicht überschrieben werden.
- **Quellen:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/31272
  - https://docs.openclaw.ai/gateway/health

### 6) OpenAI Responses: WebSocket-first Streaming
- WebSocket-first Default mit SSE-Fallback.
- Shared WS Runtime + per-Session Cleanup.
- **Quellen:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 7) Cron & Automation: „Light Context“-Mode
- Opt-in Lightweight Bootstrap für Cron/Automation, weniger Noise und weniger Failure Modes.
- **Quellen:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/26064

### 8) Builder Candy (optional): diffs-Tool & i18n
- diffs-Plugin für read-only Diff-Rendering.
- Web UI bekommt deutsches Locale.
- **Quellen:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28495

## Key Takeaways
1. **Threads und Topics** machen Sessions zu echten Projekt-Spaces.
2. **Android Notification Actions** sind ein wichtiger Schritt zu glaubwürdigen On-Device Workflows.
3. **Health Probes + stabileres Streaming** bringen OpenClaw näher an „Service“-Zuverlässigkeit.
4. **Light-Context Cron** reduziert Noise und hilft gegen spammy Outputs.

## Links
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
