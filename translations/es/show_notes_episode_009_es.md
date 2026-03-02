# Notas del episodio - Episodio 9: OpenClaw v2026.3.1 — Hilos, Temas, Acciones Android y Chequeos de Salud

## Detalles del episodio
- **Episodio:** 9
- **Versión cubierta:** OpenClaw **v2026.3.1**
- **Hosts:** Nova (británica cálida) y Alloy (estadounidense)
- **Objetivo de duración:** 30–40 minutos

## Temas tratados (con fuentes)

### 1) La release v2026.3.1: por qué importa
- Una release de “uso diario”: menos fricciones, automatización más fiable, mejor control de dispositivos.
- **Fuentes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 2) Las sesiones en hilos de Discord por fin se comportan como workspaces
- El ciclo de vida pasa de TTL fijo a sesiones **por inactividad** (idleHours por defecto 24h), con un maxAgeHours opcional.
- Nuevos comandos: `/session idle` y `/session max-age`.
- **Fuentes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/27845
  - https://docs.openclaw.ai/channels/discord

### 3) Temas en DMs de Telegram: una persona, varios workstreams (con seguridad)
- Config por DM y por tema (allowlists, dmPolicy, skills, systemPrompt, requireTopic).
- Autorización y debounce conscientes del tema para mensajes, callbacks, comandos y reacciones.
- **Fuentes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/30579

### 4) Android sube de nivel: acciones de notificaciones + salud del dispositivo
- Nuevos comandos Android: camera.list, device.permissions, device.health.
- Acciones de notificaciones: abrir, descartar, responder.
- **Fuentes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28260
  - https://docs.openclaw.ai/platforms/android

### 5) Health probes para contenedores: listo para Docker y Kubernetes
- Endpoints integrados: /health, /healthz, /ready, /readyz.
- Diseñado para no “pisar” handlers existentes.
- **Fuentes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/31272
  - https://docs.openclaw.ai/gateway/health

### 6) OpenAI Responses pasa a WebSocket-first (streaming más estable)
- WebSocket-first por defecto con fallback a SSE.
- Runtime WS compartido + limpieza por sesión.
- **Fuentes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1

### 7) Cron y automatización: modo “light context”
- Modo bootstrap ligero (opt-in) para reducir ruido y fallos en runs programados.
- **Fuentes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/26064

### 8) Extras para builders (opcional): herramienta de diffs y mejor i18n
- Plugin diffs para renderizado de diffs en solo lectura.
- La Web UI añade locale alemán.
- **Fuentes:**
  - https://github.com/openclaw/openclaw/releases/tag/v2026.3.1
  - https://github.com/openclaw/openclaw/pull/28495

## Conclusiones clave
1. **Hilos y temas** hacen que las sesiones se sientan como espacios de proyecto reales.
2. **Acciones de notificaciones en Android** abren la puerta a flujos de trabajo creíbles en el dispositivo.
3. **Probes de salud + streaming más robusto** acercan OpenClaw a fiabilidad de “servicio”.
4. **Cron con contexto ligero** reduce ruido y ayuda a evitar salidas tipo spam.

## Enlaces mencionados
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
