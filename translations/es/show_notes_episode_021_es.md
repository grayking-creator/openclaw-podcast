# EP021 — Dentro del Bucle

**OpenClaw Daily** | 2 de abril de 2026 | ~42 min

 Tres sistemas de runtime de agentes de IA, tres filosofías arquitectónicas completamente diferentes. Hoy abrimos el código fuente real de OpenClaw, Claude Code y Hermes Agent, y preguntamos: ¿qué nos dice la arquitectura sobre lo que cada uno realmente es?

---

## Historias de Este Episodio

### Arquitectura de Alto Nivel — Lo Que La Estructura Revela

**OpenClaw** está diseñado como un sistema operativo de IA personal. El daemon gateway es el núcleo; los canales (Telegram, Discord y demás) son plugins que se conectan a él. Los archivos de workspace viven en ~/.openclaw/workspace/, los subagentes corren como procesos desconectados con su propio contexto, y existe ~/.openclaw/cron/ — lo que revela algo importante: este runtime está pensado para una máquina que necesita ejecutar tareas aunque nadie esté mirando.

**Claude Code** es intencionalmente estrecho. Es una herramienta CLI centrada en ayudarte en el directorio donde estás trabajando. Tiene una capa de sandboxing robusta (Apple Sandbox Profiles en macOS, bubblewrap en Linux), pero no tiene spawning de subagentes como concepto de primera clase. Cada invocación es algo efímera, aunque mantiene estado de conversación dentro de un directorio de trabajo.

**Hermes Agent** es la plataforma de investigación más explícita. El motor de orquestación central es run_agent.py con su clase AIAgent. La base de datos SQLite ~/.hermes/state.db corre en modo WAL para acceso concurrente. Y tiene búsqueda de texto completo FTS5 en todos los mensajes de sesión — algo que los otros dos no tienen.

---

### El Ciclo de Turnos — Cómo Cada Sistema Procesa Un Intercambio

**Hermes** tiene el loop más documentado. run_conversation() sigue estos pasos: genera un task ID, appende el mensaje del usuario, carga o construye el system prompt cacheado, posiblemente precompress si el contexto crece, construye los api_messages, inyecta capas efímeras, aplica prompt caching, hace una llamada API interrumpible, ejecuta tools si las hay y vuelve al inicio, o persiste y retorna si es texto final.

El punto clave: las llamadas API interrumpibles. Si el agente está en una llamada LLM larga y el usuario envía un mensaje a mitad de vuelo, o un sistema en segundo plano necesita cancelar, Hermes puede hacerlo. Esto es un diseño explícito, no una ocurrencia de último momento.

**OpenClaw** tiene el loop más complejo porque tiene la mayor superficie de coordinación. El gateway recibe mensajes de múltiples canales, subagentes pueden despertar otros subagentes, los resultados regresan, el gateway despacha a la superficie correcta. El skill clawflow que orquesta workflows multi-agente es evidencia de esto.

**Claude Code** no tiene subagentes. Su modelo es directo: developer + directory + CLI. El sandbox es la característica de seguridad más importante.

---

### La Base de Datos de Hermes — Un Caso de Estudio en Ingeniería

~/.hermes/state.db tiene cuatro componentes lógicos: sessions, messages, messages_fts (FTS5 virtual table), y schema_version.

La tabla sessions es rica. No solo metadata — también información de facturación: input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, actual_cost_usd, cost_status, pricing_version. Si estás corriendo un setup multi-modelo con diferentes precios, Hermes rastrea tus costos por sesión.

La tabla messages almacena todo: role, content, tool_call_id, tool_calls como string JSON, tool_name, token_count, finish_reason, reasoning, reasoning_details, y codex_reasoning_items. El reasoning se almacena por separado — esto es para providers como Claude que exponen thinking tokens.

El manejo de contención de escritura es sofisticado. Hermes corre múltiples procesos — gateway más sesiones CLI más worktree agents — todos compartiendo un solo state.db. Usa un timeout corto de SQLite (1 segundo, no el default de 30), reintentos a nivel de aplicación con jitter aleatorio entre 20 y 150 milisegundos, hasta 15 reintentos, y transacciones BEGIN IMMEDIATE para detectar contención de escritura temprano. También hace WAL checkpoints periódicos cada 50 writes en modo PASSIVE.

Y hay lineage de sesiones via parent_session_id. Cuando la compresión de contexto dispara un split de sesión — pasa cuando la ventana de contexto se llena — la nueva sesión obtiene un nuevo ID pero encadena al padre. Puedes consultar linaje completo de sesiones recursivamente.

---

### Modelos de Seguridad — Sandbox vs. Aprobación

**Claude Code** tiene un sistema de sandboxing que ataca dos plataformas explícitamente: macOS y Linux. En macOS usa Apple Sandbox Profiles. En Linux usa bwrap — bubblewrap. El sistema se llama SandboxLinux en el source, con clases como SandboxConfig, SandboxManager y ViolationStore que rastrea violaciones con conteo total e historial por comando. El store tiene max 100 entradas y un conteo total que sigue incrementando aunque el store esté lleno.

El config del sandbox de Linux define --new-session --die-with-parent, luego construye paths de filesystem allow y deny. Paths allow начинаются con una lista por defecto — cosas como /dev/null, /dev/urandom, /dev/zero. Paths deny son cosas como /etc/ssh/ssh_config.d si existe. Para paths de escritura, tiene un concepto denyWithinAllow — puedes escribir a un directorio pero no a subpaths peligrosos específicos dentro de él. También hay filtrado seccomp BPF para bloqueo de sockets Unix.

**Hermes** tiene un enfoque fundamentalmente diferente. tools/approval.py tiene una DANGEROUS_PATTERNS list — regex patterns pareados con descripciones cubriendo deletes recursivos, comandos de formateo de filesystem como mkfs y dd, operaciones SQL destructivas, sobreescrituras de config del sistema, manipulación de servicios, ejecución remota de código via curl | sh, fork bombs. Antes de ejecutar cualquier comando de terminal, detect_dangerous_command() verifica contra todos los patterns.

Si hay match: en modo CLI, un prompt interactivo pregunta al usuario aprobar, denegar, o permitir permanentemente. En modo gateway, un callback async de aprobación envía la solicitud a la plataforma de mensajería — así que si estás en Telegram o Discord, recibes el mensaje de aprobación ahí. También hay una opción smart approval donde un LLM auxiliar puede auto-aprobar comandos de bajo riesgo que casualmente matchean patterns peligrosos.

**OpenClaw** combina elementos de ambos. El tool exec tiene un sistema de aprobaciones — exec-approvals.json en el directorio config. Y el sistema de subagentes tiene scope de permisos — subagentes corren con contextos de workspace específicos y no necesariamente pueden leer o escribir todo lo que el agente padre puede.

---

### Extensibilidad — Skills, MCP y el Ecosistema

**El sistema de skills de Hermes** es el más realizado de los tres. Skills son documentos de conocimiento bajo demanda que el agente puede cargar cuando los necesita. Siguen el estándar abierto agentskills.io, lo que significa que no están atados a Hermes — son portables. El formato es SKILL.md con YAML frontmatter declarando name, description, version, platforms, y metadata para condiciones de activación.

El patrón de revelación progresiva es elegante. Nivel 0: skills_list() retorna solo name, description y category — unas 3k tokens. Nivel 1: skill_view(name) carga el contenido completo. Nivel 2: skill_view(name, path) carga un archivo de referencia específico. El agente solo paga el costo de tokens cuando realmente necesita la skill completa.

Skills pueden ser condicionales. Pueden declarar fallback_for_toolsets — así que una skill de búsqueda DuckDuckGo solo aparece cuando el toolset premium de web search no está disponible. O requires_toolsets — una skill solo aparece cuando ciertos tools están presentes. Y pueden declarar variables de entorno requeridas sin desaparecer del discovery.

**Agent-created skills** son un diferenciador clave. El tool skill_manage deja que el agente cree, actualice y borre sus propias skills via un conjunto de acciones create/patch/edit/delete/write_file/remove_file. Los triggers especificados: después de completar una tarea compleja con 5+ tool calls, cuando se topa con errores y encuentra el camino correcto, cuando el usuario corrige su enfoque, cuando descubre un workflow no trivial.

**Hermes tiene integración completa con marketplace de skills.** Se conecta al catálogo oficial opcional de skills, skills.sh (directorio público de Vercel), endpoints de skills bien-known via la convención /.well-known/skills/, repos directos de GitHub, ClawHub, y repos del marketplace de Claude. Puedes publicar skills a GitHub directamente. Puedes agregar GitHub taps personalizados. Esto es una estrategia de ecosistema genuinamente abierta.

**OpenClaw** usa archivos de workspace para contexto estructurado — MEMORY.md para memoria curation a largo plazo, memory/YYYY-MM-DD.md para logs de sesión diarios. También hay un sistema LCM — Lossless Context Management — que compacta el historial de conversación. Y un sistema de skills que actúa como memoria procedural. Es un modelo de tres capas: logs diarios crudos, memoria curation a largo plazo, y skills que codifican workflows reutilizables.

**Claude Code** tiene un modelo de extensión más enfocado. La estructura del paquete npm sugiere que está diseñado para trabajar bien con herramientas de developer existentes en lugar de tener su propio marketplace de plugins. El sistema de skills en Claude Code es más ligero — slash commands, esencialmente.

---

### La Señal Más Grande — hermes claw migrate

Este es el detalle que lo cambia todo. Hermes incluye explicitamente una herramienta de migración llamada hermes claw migrate que importa skills de OpenClaw y configuraciones de workspace.

Esto no es accidental. El hecho de que sea "hermes claw migrate" — y no "claw migrate" — te dice algo sobre la relación direccional. OpenClaw vino primero. Hermes está migrando desde él. Pero Hermes está haciendo esto explícitamente, lo que significa que el equipo de Nous Research miró el sistema de skills y workspace model de OpenClaw y decidió: queremos eso en nuestro ecosistema, y queremos hacerlo fácil para que usuarios de OpenClaw prueben Hermes.

Y la arquitectura model-agnostic de Hermes hace esta migración creíble. Si has estado usando OpenClaw con Claude como tu backend, puedes cambiarte a Hermes y usar las mismas skills. El formato de skills es abierto.

---

### Veredicto — Cuándo Usar Cada Uno

**Usa Hermes Agent si:** eres un investigador o power user que quiere un agente auto-mejorable con memoria genuina a largo plazo entre sesiones, flexibilidad model-agnostic, búsqueda FTS5 en todo tu historial de conversación, un ecosistema rico de skills que estás contribuyendo y del cual draw, y la habilidad de correr en Telegram, Discord, Slack, WhatsApp o Signal desde un solo gateway. Hermes también es la elección correcta si estás interesado en mejora de agentes basada en RL — los entornos RL de Atropos y la compresión de trayectorias sugieren un diseño orientado a investigación. Y si ya eres usuario de OpenClaw, hermes claw migrate significa que puedes traer tus skills contigo.

**Usa Claude Code si:** eres un developer que quiere la mejor ayuda posible en un codebase específico, corriendo localmente, con el sandboxing más riguroso a nivel de SO para operaciones peligrosas. La integración de bubblewrap y Apple Sandbox de Claude Code es la implementación de sandbox más rigurosa de los tres. Si tu workflow es "estoy en un directorio, necesito ayuda, confío en el agente para editar archivos aquí," Claude Code es la herramienta más enfocada para ese trabajo.

**Usa OpenClaw si:** quieres una IA personal persistente que viva en tu máquina (o un VPS), se conecte a múltiples canales de mensajería simultáneamente, ejecute tareas programadas, genere subagentes para trabajo en segundo plano, y tenga un sistema de skills que sea tuyo para moldear. OpenClaw es el más Unix-native de los tres — encaja naturalmente en un workflow de línea de comandos, funciona con convenciones existentes de dotfiles y workspace, y está diseñado para ser tu sistema operativo de IA en lugar de una herramienta única.

---

### Modelos Recomendados para Hermes

Si quieres probar Hermes después de esto — el punto de partida recomendado es Claude Sonnet via Anthropic OAuth. Si ya usas Claude Code, Hermes lee automáticamente tu credential store — no necesitas setup de API key separado.

Para opciones gratuitas: Hermes tiene soporte de primera para GitHub Copilot. Si tienes suscripción Copilot, obtienes acceso a GPT-5.4, Claude y Gemini a través del Copilot API. GPT-5 y superiores automáticamente rutean a través del Responses API.

El camino gratuito más interesante es OpenRouter. Configura tu OPENROUTER API KEY en tu archivo dot env, y tienes acceso a más de 200 modelos. Algunos tools built-in — vision, web summarization, y mixture of agents tool — usan un modelo auxiliar separado que por defecto es Gemini Flash via OpenRouter. Así que incluso si usas Claude como tu primary, una key de OpenRouter desbloquea esos tools automáticamente.

Para modelos locales: Hermes soporta cualquier endpoint de Ollama o vLLM — misma configuración, solo apunta OPENAI BASE URL a tu servidor local.

---

## Capítulos

`[00:00]` Gancho — Tres Agentes, Tres Teorías de IA
`[02:30]` Arquitectura de Alto Nivel — OpenClaw, Claude Code, Hermes
`[08:00]` El Ciclo de Turnos — Cómo Cada Sistema Procesa un Intercambio
`[14:00]` La Base de Datos de Hermes — SQLite, FTS5, y Manejo de Contención
`[21:00]` Modelos de Seguridad — Sandbox vs. Aprobación Interactiva
`[28:00]` Skills y Extensibilidad — El Ecosistema de Hermes
`[33:00]` La Señal de hermes claw migrate — Cuándo un Competidor Admira tu Trabajo
`[36:00]` Veredicto — Cuándo Usar Cada Runtime
`[40:00]` Modelos Recomendados para Empezar con Hermes
`[42:00]` Cierre

---

## Encuentra OpenClaw Daily

- 🌐 [tobyonfitnesstech.com/es/podcasts/episode-21/](https://tobyonfitnesstech.com/es/podcasts/episode-21/)
- 🎙️ Spotify · Apple Podcasts · Pocket Casts · Amazon Music · Overcast
- Feeds disponibles en EN, ES, PT, HI, DE

→ Reply on Telegram to approve.
