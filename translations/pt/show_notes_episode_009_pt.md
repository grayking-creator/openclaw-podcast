# Show Notes – Episódio 9: OpenClaw v2026.3.1 — Threads, Tópicos, Ações no Android e Health Checks

## Detalhes do episódio
- **Episódio:** 9
- **Release coberta:** OpenClaw **v2026.3.1**
- **Hosts:** Nova (britânica calorosa) & Alloy (americano)
- **Meta de duração:** 30–40 minutos

## Tópicos (com fontes)

### 1) A release v2026.3.1: por que ela importa
- Uma release “daily driver”: menos fricção, automação mais confiável, melhor controle de dispositivos.
- **Fontes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 2) Sessões em threads do Discord finalmente parecem workspaces
- Lifecycle sai de TTL fixo para sessões **baseadas em inatividade** (idleHours padrão 24h), com maxAgeHours opcional.
- Novos comandos: `/session idle` e `/session max-age`.
- **Fontes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/27845
  - https://docs.openclaw.ai/channels/discord

### 3) Tópicos em DMs do Telegram: uma pessoa, vários workstreams (com segurança)
- Config por DM + tópico (allowlists, dmPolicy, skills, systemPrompt, requireTopic).
- Autorização e debounce “topic-aware” para mensagens, callbacks, comandos e reações.
- **Fontes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/30579

### 4) Android evolui: ações em notificações + saúde do dispositivo
- Novos comandos: camera.list, device.permissions, device.health.
- Ações em notificações: abrir, dispensar, responder.
- **Fontes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28260
  - https://docs.openclaw.ai/platforms/android

### 5) Health probes para containers: pronto para Docker e Kubernetes
- Endpoints embutidos: /health, /healthz, /ready, /readyz.
- Projetado para não sobrescrever handlers existentes.
- **Fontes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/31272
  - https://docs.openclaw.ai/gateway/health

### 6) OpenAI Responses vira WebSocket-first (streaming mais estável)
- WebSocket-first por padrão com fallback SSE.
- Runtime WS compartilhado + limpeza por sessão.
- **Fontes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 7) Cron e automação: modo “light context”
- Bootstrap leve (opt-in) para runs de cron/automação: menos ruído e menos modos de falha.
- **Fontes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/26064

### 8) Extras (opcional): ferramenta de diffs e i18n
- Plugin de diffs para renderização read-only.
- Web UI adiciona locale em alemão.
- **Fontes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28495

## Principais conclusões
1. **Threads e tópicos** fazem as sessões parecerem espaços reais de projeto.
2. **Ações em notificações no Android** são o primeiro passo para workflows on-device de verdade.
3. **Health probes + streaming mais robusto** aproximam o OpenClaw de confiabilidade “como serviço”.
4. **Cron com contexto leve** reduz ruído e ajuda a evitar outputs tipo spam.

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
