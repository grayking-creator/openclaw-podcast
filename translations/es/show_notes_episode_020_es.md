# EP020 — El Lanzamiento de la Infraestructura

**OpenClaw Daily** | 1 de abril de 2026 | ~32 min

OpenClaw dejó de ser una herramienta inteligente esta semana y pasó a ser infraestructura. Cinco historias que explican cómo ocurrió — y lo que significa para todos los que construyen sobre ella.

---

## Historias de Este Episodio

### 1. OpenClaw v2026.3.31 — El Lanzamiento de la Plataforma
La actualización de OpenClaw más trascendental en meses. Cambios clave:
- **Panel de control de tareas en segundo plano** — ACP, subagentes, cron y ejecución CLI en segundo plano unificados bajo un solo libro mayor respaldado por SQLite con `openclaw flows list|show|cancel`
- **Seguridad de plugins fails closed por defecto** — hallazgos críticos de código peligroso ahora bloquean instalaciones; se requiere `--dangerously-force-unsafe-install` explícito para anular
- **Emparejamiento vs. aprobación de nodos separados** — los comandos de nodo permanecen deshabilitados hasta que el emparejamiento es aprobado explícitamente (emparejar solo ya no es suficiente)
- **Auth de Gateway reforzada** — proxy de confianza rechaza configs de token compartido mixtos; fallback local-direct requiere el token configurado
- **Canal QQ Bot** — ruta de primera clase integrada en el ecosistema de Tencent
- **Respuestas de streaming Matrix** — respuestas parciales ahora se actualizan en su lugar en lugar de inundar el chat
- **Soporte MCP HTTP/SSE remoto** — sirve superficies de herramientas sobre transportes remotos
- **Reenvío de notificaciones Android** — filtrado de paquetes, horas silenciosas, limitación de tasa
- **Timeout de stream inactivo** — streams de modelo bloqueados ahora se abortan limpiamente
- **Puente ACPX MCP reforzado** — config explícita desactivada por defecto, límite de confianza documentado
- Breaking: `qwen-portal-auth` eliminado; configs de más de 2 meses ya no se migran automáticamente

📎 [Notas de lanzamiento: openclaw/openclaw v2026.3.31](https://github.com/openclaw/openclaw/releases/tag/v2026.3.31)

---

### 2. La Fiebre de OpenClaw en China — y la Respuesta de Beijing
OpenClaw se viralizó en China ("langosta" en la jerga tecnológica china), con estrellas de GitHub superando brevemente a React. Tencent organizó eventos de instalación emergentes. Luego vinieron las "víctimas de la langosta" — usuarios que perdieron archivos, acumularon facturas o expusieron datos sensibles a agentes de IA sin salvaguardas. Beijing respondió prohibiendo a los empleados de empresas estatales usar la herramienta.

📎 [The Wire China: Cómo la Fiebre de OpenClaw Está Poniendo a Prueba el Compromiso de China con la IA](https://www.thewirechina.com/2026/03/29/how-the-openclaw-frenzy-is-testing-chinas-ai-commitment/)
📎 [Advertencia de seguridad PCWorld: No instales OpenClaw](https://www.pcworld.com/article/3064874/openclaw-ai-is-going-viral-dont-install-it.html)

---

### 3. Microsoft 365 + OpenClaw — Validación Empresarial
Microsoft está integrando activamente OpenClaw en Microsoft 365, llevando agentes de IA personales a sus ~400 millones de usuarios empresariales. Esto posiciona a OpenClaw como la capa de agentes para la productividad corporativa — no solo una herramienta para aficionados.

📎 [Windows Central: Los nuevos agentes de IA OpenClaw de Microsoft para Microsoft 365](https://www.windowscentral.com/artificial-intelligence/microsoft-openclaw-will-add-personal-ai-agents-in-microsoft-365)

---

### 4. Perplexity Personal Computer — IA Local que Vive Contigo
Perplexity lanzó "Personal Computer" — un agente de IA dedicado en un Mac mini con acceso persistente y continuo a tus archivos y aplicaciones locales. Siempre activo, siempre consciente del contexto, completamente local. No requiere carga a la nube.

📎 [r/LocalLLaMA: Pilas de agentes locales en 2026](https://www.reddit.com/r/LocalLLaMA/comments/1s6f15f/localfirst_agent_stacks_in_2026_whats_actually/)

---

### 5. El Trimestre de $297 Mil Millones
Q1 2026 rompió todos los récords de financiación de venture. Se invirtieron $297B globalmente, 81% en empresas de IA. Las cuatro rondas más grandes: OpenAI ($120B), Anthropic ($30B), xAI ($20B), Waymo ($16B). CoreWeave logró una facilidad de financiación de $8.5B. El Unicorn Board de Crunchbase agregó $900B en valor en un solo trimestre.

📎 [Crunchbase: Q1 2026 Rompe Récords de Financiación de Venture](https://news.crunchbase.com/venture/record-breaking-funding-ai-global-q1-2026/)
📎 [TechFundingNews: CoreWeave obtiene $8.5B](https://techfundingnews.com/coreweave-lands-8-5b-wall-street-ai-cloud/)

---

## Capítulos

`[00:00]` Gancho — El Momento de la Plataforma
`[02:30]` OpenClaw v2026.3.31 — Cuando una Herramienta Se Convierte en Infraestructura
`[14:00]` La Fiebre de OpenClaw en China y la Represión del Estado
`[21:00]` Integración con Microsoft 365 — ¿Validación Empresarial o Normalización del Riesgo?
`[27:00]` Perplexity Personal Computer — IA Local que Vive Contigo
`[33:00]` El Trimestre de $297 Mil Millones — La Mayor Inyección de Financiación de IA
`[39:00]` Cierre — Agentes en el Punto de Inflexión

---

## Encuentra OpenClaw Daily

- 🌐 [tobyonfitnesstech.com/es/podcasts/episode-20/](https://tobyonfitnesstech.com/es/podcasts/episode-20/)
- 🎙️ Spotify · Apple Podcasts · Pocket Casts · Amazon Music · Overcast
- Feeds disponibles en EN, ES, PT, HI, DE

→ Reply on Telegram to approve.
