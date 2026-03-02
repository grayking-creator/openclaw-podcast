# शो नोट्स – एपिसोड 9: OpenClaw v2026.3.1 — Threads, Topics, Android Actions और Health Checks

## एपिसोड विवरण
- **एपिसोड:** 9
- **कवर की गई रिलीज़:** OpenClaw **v2026.3.1**
- **होस्ट:** Nova (warm British) और Alloy (American)
- **ड्यूरेशन लक्ष्य:** 30–40 मिनट

## टॉपिक्स (सोर्स के साथ)

### 1) v2026.3.1 रिलीज़: यह क्यों महत्वपूर्ण है
- “Daily driver” रिलीज़: कम friction, ज्यादा reliable automation, बेहतर device control.
- **सोर्स:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 2) Discord thread sessions अब असली workspaces जैसे व्यवहार करते हैं
- Thread lifecycle fixed TTL से **inactivity-based** sessions में गया (idleHours default 24h), और optional maxAgeHours.
- नए commands: `/session idle` और `/session max-age`.
- **सोर्स:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/27845
  - https://docs.openclaw.ai/channels/discord

### 3) Telegram DM topics: एक व्यक्ति, कई workstreams (सुरक्षित तरीके से)
- Per-DM direct + topic config (allowlists, dmPolicy, skills, systemPrompt, requireTopic).
- Topic-aware authorization + debounce (messages, callbacks, commands, reactions).
- **सोर्स:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/30579

### 4) Android nodes: notification actions + device health
- नए Android commands: camera.list, device.permissions, device.health.
- Notification actions: open, dismiss, reply.
- **सोर्स:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28260
  - https://docs.openclaw.ai/platforms/android

### 5) Container health probes: Docker और Kubernetes के लिए ready
- Built-in endpoints: /health, /healthz, /ready, /readyz.
- Existing handlers को shadow न करने के लिए डिज़ाइन.
- **सोर्स:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/31272
  - https://docs.openclaw.ai/gateway/health

### 6) OpenAI Responses: WebSocket-first (ज़्यादा stable streaming)
- Default WebSocket-first transport, SSE fallback के साथ.
- Shared WS runtime wiring + per-session cleanup.
- **सोर्स:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 7) Cron/automation runs: “Light context” mode
- Opt-in lightweight bootstrap mode ताकि scheduled runs में noise कम हो और failure modes घटें.
- **सोर्स:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/26064

### 8) Builder extras (optional): diffs tool और बेहतर i18n
- Read-only diff rendering के लिए diffs plugin.
- Web UI में German locale.
- **सोर्स:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28495

## Key takeaways
1. **Threads और topics** sessions को असली project spaces जैसा बनाते हैं.
2. **Android notification actions** on-device assistant workflows की दिशा में बड़ा कदम हैं.
3. **Health probes + मजबूत streaming** OpenClaw को “service की तरह” reliable बनाते हैं.
4. **Light-context cron** automation noise कम करता है और spammy outputs से बचाता है.

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
