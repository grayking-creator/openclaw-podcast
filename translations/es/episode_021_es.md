[NOVA]: Soy NOVA.

[ALLOY]: Y yo soy ALLOY. Esto es OpenClaw Daily. Hoy entramos dentro del código fuente de tres runtimes de agentes de IA — OpenClaw, Claude Code y Hermes — y preguntamos qué nos dice la arquitectura sobre lo que cada uno realmente es.

[NOVA]: Tres runtimes de agentes caminaron hacia un codebase. Solo uno sabía hacia dónde se dirigía.

[NOVA]: Hoy es un deep dive técnico, ALLOY. No vamos a darte copy de marketing. Vamos a abrir los archivos reales y mostrarte lo que el código hace — porque la arquitectura es la filosofía. Cómo algo maneja su ciclo de turnos, cómo persiste la memoria, cómo protege las acciones peligrosas — estos no son detalles de implementación. Son el producto.

[ALLOY]: Y lo interesante es que cuando miras los tres lado a lado, te das cuenta de que apenas están de acuerdo sobre qué es un "agente". Hermes tiene un agente que se auto-mejora y escribe sus propias skills. Claude Code tiene un agente que existe solo para ayudarte a programar en un directorio específico. OpenClaw tiene un agente que es más como un sistema operativo — persistente, multi-canal, multi-subagente. Estos son animales genuinamente diferentes llevando la misma palabra.

[NOVA]: Empecemos con cómo cada sistema está estructurado a alto nivel, porque eso lo moldea todo.

[NOVA]: Empezando por OpenClaw. Si miras ~/.openclaw/, ves la estructura del runtime. Hay un daemon gateway que gestiona el sistema general. Los canales — Telegram, Discord, y demás — son plugins que se conectan a este gateway. Los archivos de workspace viven en ~/.openclaw/workspace/, y los subagentes corren como procesos desconectados con su propio contexto. La configuración está en openclaw.json. El sistema de skills vive en ~/.openclaw/skills/, y la memoria se almacena en ~/.openclaw/memory/. Críticamente, también hay ~/.openclaw/cron/ — OpenClaw tiene un sistema de scheduling integrado, lo que te dice algo importante: este runtime está diseñado para una máquina que necesita ejecutar tareas aunque nadie esté mirando.

[ALLOY]: Exacto. OpenClaw está arquitectado como un sistema operativo de IA personal. No se trata solo de un loop de agente único. Se trata de presencia persistente a través de superficies de mensajería, trabajo programado en segundo plano, y delegación a subagentes. El daemon gateway de OpenClaw es el kernel de este sistema. Todo lo demás es un proceso.

[NOVA]: Ahora Claude Code — y esta va a ser una discusión de arquitectura más corta, porque Claude Code está intencionalmente enfocado. Lo instalas desde npm: @anthropic-ai/claude-code, versión 2.1.59 al momento de la grabación. Es una herramienta CLI primero. Tiene una capa de sandboxing que podemos ver en sus dependencias — hay módulos para Apple Sandbox Profiles de macOS e integración con bwrap (bubblewrap) de Linux. El registry de tools está en cli.js y archivos relacionados. Pero la arquitectura es deliberadamente estrecha: quiere ser la mejor herramienta para un trabajo — ayudar a un developer en un directorio de código.

[ALLOY]: Que es una elección de diseño completamente legítima. Estrecho y profundo supera a ancho y superficial. Pero significa que el modelo de sesión de Claude Code es diferente de los otros dos. No tiene una base de datos de sesión persistente. Cada invocación es algo efímera, aunque puede mantener estado de conversación dentro de un directorio de trabajo. Profundizaremos en lo que eso significa para la memoria.

[NOVA]: Y luego Hermes Agent de Nous Research. Este es el más explícitamente arquitectado como plataforma de investigación. El motor de orquestación central es run_agent.py y su clase AIAgent. La sesión store es una base de datos SQLite en ~/.hermes/state.db corriendo en modo WAL — así que lectores concurrentes, un writer, lo cual importa cuando tanto el gateway como la CLI la están golpeando. Y tiene búsqueda de texto completo FTS5 a través de todos los mensajes de sesión via una tabla virtual.

[ALLOY]: Eso es en realidad una decisión de arquitectura muy significativa. FTS5 significa que puedes buscar en todo tu historial de conversación, no solo turnos recientes. Si eres un investigador que corre sesiones largas a través de múltiples temas, eso es una característica significativa. Y el hecho de que rastreen conteos de tokens, facturación y configuraciones de modelo por sesión te dice que esto se construyó con conciencia de costos — tanto para el laboratorio de investigación como para usuarios que están pagando por llamadas API.

[NOVA]: Hablemos de la pieza más importante de cualquier runtime de agente: el ciclo de turnos. ¿Cómo maneja cada sistema un solo intercambio — mensaje de usuario entra, el modelo piensa, llamadas a tools, respuesta sale?

[ALLOY]: Empezando por Hermes, porque tiene el loop más documentado. Desde los docs: run_conversation() es el punto de entrada principal. El ciclo de turnos es:

[NOVA]: 1. Generar un task ID

[NOVA]: 2. Appendear el mensaje actual del usuario

[NOVA]: 3. Cargar o construir el system prompt cacheado

[NOVA]: 4. Quizás preflight-compress si el contexto se está alargando

[NOVA]: 5. Construir api_messages — el payload de prompt real

[NOVA]: 6. Inyectar capas de prompt efímeras

[NOVA]: 7. Aplicar prompt caching si corresponde

[NOVA]: 8. Hacer una llamada API interrumpible

[NOVA]: 9. Si hay llamadas a tools: ejecutarlas, appendear resultados, volver al loop

[NOVA]: 10. Si es texto final: persistir, limpiar, retornar

[NOVA]: Paso 8 — llamadas API interrumpibles. Eso es importante. Hermes envuelve sus requests API para que puedan ser canceladas desde la CLI o el gateway. Esto importa porque el agente podría estar en una llamada LLM larga, y el usuario envía un nuevo mensaje a mitad de vuelo, o un sistema en segundo plano necesita cancelar. Esto es un tema de diseño explícito, no un afterthought.

[ALLOY]: Y mira los modos de API que Hermes soporta. Tres paths de ejecución: chat_completions para endpoints compatibles con OpenAI (incluyendo OpenRouter), codex_responses para Codex y Responses API, y anthropic_messages para la API nativa de Messages de Anthropic. El modo se resuelve a partir de argumentos explícitos, selección de provider, y heurísticas de base URL. Así que Hermes es genuinamente model-agnostic — no como claim de marketing sino como arquitectura de routing.

[NOVA]: Ahora la ejecución de tools de Hermes. Dos modos: sequential para tools individuales o interactivos, y concurrent para múltiples tools no interactivos. Y aquí está la parte inteligente — la ejecución concurrente preserva el orden de mensajes y resultados al reinsertar respuestas de tools en el historial de conversación. Eso es una restricción no trivial de implementar bien.

[ALLOY]: Para Claude Code, no tenemos el path exacto al archivo del loop de la misma manera, pero podemos inferirlo desde la estructura del paquete. El paquete npm está en /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/. Los patrones clave a buscar están en cli.js — cómo maneja las llamadas a tools, cómo gestiona los prompts de permisos, cómo hace el loop. Lo que sabemos del loop de Claude Code es que está diseñado alrededor de un caso de uso específico: asistencia a developer en un directorio local. No tiene spawning de subagentes como concepto de primera clase de la forma en que OpenClaw lo tiene.

[NOVA]: Y el agent loop de OpenClaw está diseñado alrededor del hecho de que tiene múltiples agentes concurrentes con un gateway gestionando la coordinación. El loop no es solo "usuario → agente → tools → respuesta." Es: llega un mensaje de usuario por el canal X, el subagente Y lo toma, el subagente Y puede generar el subagente Z, los resultados regresan, el gateway despacha a la superficie correcta. El skill clawflow que orquesta workflows multi-agente es evidencia de esto — está diseñado para tareas en segundo plano desconectadas que todavía se comportan como un solo trabajo.

[ALLOY]: El loop de OpenClaw es el más complejo de los tres porque tiene la mayor superficie de coordinación que gestionar. Pero complejidad no siempre es malo — es complejidad apropiada para lo que intenta hacer.

[NOVA]: Aquí es donde Hermes realmente se distingue arquitecturalmente. Profundicemos en el schema de SQLite.

[ALLOY]: ~/.hermes/state.db tiene cuatro componentes lógicos: una tabla sessions, una tabla messages, una tabla virtual FTS5 llamada messages_fts, y una tabla schema_version. La tabla sessions es rica — no solo metadata de sesión sino información de facturación: input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, actual_cost_usd, cost_status, pricing_version. Si estás corriendo un setup multi-modelo con diferentes precios de diferentes providers, Hermes está rastreando tus costos por sesión.

[NOVA]: La tabla messages almacena todo. role, content, tool_call_id, tool_calls como string JSON, tool_name, token_count, finish_reason, reasoning, reasoning_details, y codex_reasoning_items. Nota que reasoning se almacena por separado — esto es para providers como Claude que exponen thinking tokens. Y hay tres triggers que mantienen la tabla FTS5 en sync en INSERT, UPDATE y DELETE.

[ALLOY]: El manejo de contención de escritura vale la pena mirarlo. Hermes maneja múltiples procesos — gateway más sesiones CLI más worktree agents — todos compartiendo un solo state.db. Usa un timeout corto de SQLite (1 segundo, no el default de 30), reintentos a nivel de aplicación con jitter aleatorio entre 20 y 150 milisegundos, hasta 15 reintentos, y transacciones BEGIN IMMEDIATE para detectar contención de escritura temprano. También hace WAL checkpoints periódicos cada 50 writes en modo PASSIVE. Esto es ingeniería reflexiva — están evitando el problema de convoy de SQLite donde writers en competencia reintentan a los mismos intervalos.

[NOVA]: Y el lineage de sesiones via parent_session_id encadena. Cuando la compresión de contexto dispara un split de sesión — lo que pasa cuando la ventana de contexto se llena — la nueva sesión obtiene un nuevo ID pero encadena hacia atrás al padre. Puedes consultar linajes de sesiones completos recursivamente. Esto es para sesiones de investigación o coding largas donde la compresión de contexto pasa a mitad de tarea.

[ALLOY]: Ahora compara eso con el modelo de Claude Code. El modelo de sesión de Claude Code es... más ligero. Puede mantener contexto de conversación dentro de un directorio de trabajo, pero no está diseñado como un sistema de memoria a largo plazo. El sandbox está diseñado alrededor de permisos de filesystem para un directorio específico — no alrededor de memoria estructurada persistente entre sesiones. Esto es un tradeoff deliberado: simplicidad para el caso más común (ayuda a developer en un codebase) versus persistencia rica de sesión.

[NOVA]: Y el modelo de memoria de OpenClaw. Usa archivos de workspace para contexto estructurado — MEMORY.md para memoria curation a largo plazo, memory/YYYY-MM-DD.md para logs de sesión diarios. También hay un sistema LCM — Lossless Context Management — que compacta el historial de conversación. Y un sistema de skills que actúa como memoria procedural. Así que es un modelo de tres capas: logs diarios crudos, memoria curation a largo plazo, y skills que codifican workflows reutilizables.

[ALLOY]: El enfoque de OpenClaw es más nativo al filesystem y menos nativo a la base de datos que Hermes. Hermes pone todo en SQLite porque es un solo runtime que necesita acceso multi-proceso concurrente y FTS5. OpenClaw usa el filesystem porque encaja con la filosofía Unix y hace los datos universalmente accesibles — puedes hacer grep, hacer backup con rsync, ponerlo en git.

[NOVA]: Aquí es donde Claude Code realmente muestra sus cartas. Hablemos de cómo maneja las acciones peligrosas.

[ALLOY]: Claude Code tiene un sistema de sandboxing que apunta a dos plataformas explícitamente: macOS y Linux. En macOS, usa Apple Sandbox Profiles. En Linux, usa bwrap — bubblewrap. El sistema se llama SandboxLinux en el source, y hay clases como SandboxConfig, SandboxManager, y un ViolationStore que rastrea violaciones de sandbox con un conteo total e historial por comando. El store de violaciones tiene un tamaño máximo de 100 entradas y un conteo total que sigue incrementando incluso después de que el store esté lleno.

[NOVA]: El sandbox config para Linux está definido en sandbox_linux.py. Empieza con --new-session --die-with-parent. Luego construye paths de filesystem allow y deny. Los paths allow начинаются con una lista allow por defecto — cosas como /dev/null, /dev/urandom, /dev/zero. Los paths deny son cosas como /etc/ssh/ssh_config.d si existe. Para paths de escritura, tiene un concepto denyWithinAllow — puedes escribir a un directorio pero no a subpaths peligrosos específicos dentro de él.

[ALLOY]: El sandbox de Linux también tiene filtrado seccomp BPF para bloqueo de sockets Unix. Hay un bpfPath y un applyPath para el binario de seccomp. Si esos no están disponibles, cae de vuelta a permitir sockets Unix — pero advierte que la protección completa no está disponible. En macOS, hay un SandboxMonitor que vigila violaciones usando el comando osascript.

[NOVA]: Ahora compara eso con el enfoque de Hermes. Hermes tiene una lista DANGEROUS_PATTERNS en tools/approval.py — regex patterns pareados con descripciones cubriendo deletes recursivos, comandos de formateo de filesystem como mkfs y dd, operaciones SQL destructivas, sobreescrituras de config del sistema, manipulación de servicios, ejecución remota de código via curl pipe sh, fork bombs. Antes de ejecutar cualquier comando de terminal, detect_dangerous_command() verifica contra todos los patterns.

[ALLOY]: Si se encuentra un match: en modo CLI, un prompt interactivo pregunta al usuario aprobar, denegar, o permitir permanentemente. En modo gateway, un callback async de aprobación envía la solicitud a la plataforma de mensajería — así que si estás en Telegram o Discord, recibes el mensaje de aprobación ahí. También hay una opción smart approval donde un LLM auxiliar puede auto-aprobar comandos de bajo riesgo que casualmente matchean patterns peligrosos — como rm -rf node_modules/ haciendo match con el pattern de delete recursivo.

[NOVA]: Y Hermes tiene aprobaciones con scope de sesión. Una vez que apruebas "delete recursivo" para una sesión, los comandos rm -rf subsiguientes no vuelven a preguntar. El allowlist permanente escribe patterns a command_allowlist de config.yaml para que persistan entre sesiones.

[ALLOY]: Estos son modelos fundamentalmente diferentes. El sandbox de Claude Code es sobre restringir las capacidades del proceso antes de que algo malo pueda pasar — el SO lo enforcea. El sistema de aprobación de Hermes es sobre detectar patterns peligrosos y preguntar — el humano lo enforcea. El modelo de Claude Code es más fuerte contra daño accidental. El modelo de Hermes es más flexible para casos de uso interactivos donde el agente está corriendo en un servidor remoto y el usuario está aprobando via Telegram.

[NOVA]: El modelo de OpenClaw combina elementos de ambos. El tool exec tiene un sistema de aprobación — hay exec-approvals.json en el directorio config. Y el sistema de subagentes tiene scope de permisos — subagentes corren con contextos de workspace específicos y no necesariamente pueden leer o escribir todo lo que el agente padre puede. El gateway también tiene el concepto de permisos por canal — lo que está permitido en Telegram puede diferir de lo que está permitido en Discord.

[NOVA]: Hablemos de cómo cada sistema te deja extenderlo.

[ALLOY]: Empezando por el sistema de skills de Hermes, porque es el más realizado. Skills son documentos de conocimiento bajo demanda que el agente puede cargar cuando los necesita. Siguen el estándar abierto agentskills.io, lo que significa que no están atados a Hermes — son portables. El formato de skill es SKILL.md con YAML frontmatter declarando name, description, version, platforms, y metadata para condiciones de activación.

[NOVA]: El patrón de revelación progresiva es inteligente. Nivel 0: skills_list() retorna solo name, description y category — unas 3k tokens. Nivel 1: skill_view(name) carga el contenido completo. Nivel 2: skill_view(name, path) carga un archivo de referencia específico. El agente solo paga el costo de tokens cuando realmente necesita la skill completa.

[ALLOY]: Las skills pueden ser condicionales. Pueden declarar fallback_for_toolsets — así que una skill de búsqueda DuckDuckGo solo aparece cuando el toolset premium de web search no está disponible. O requires_toolsets — una skill solo aparece cuando ciertos tools están presentes. Y pueden declarar variables de entorno requeridas sin desaparecer del discovery — si falta una key, Hermes la pide de forma segura cuando la skill se carga en modo CLI, pero nunca pregunta en superficies de mensajería.

[NOVA]: Agent-created skills son un diferenciador clave. El tool skill_manage deja que el agente cree, actualice y borre sus propias skills via un conjunto de acciones create/patch/edit/delete/write_file/remove_file. Los docs especifican los triggers: después de completar una tarea compleja con 5 o más tool calls, cuando se topa con errores y encuentra el camino correcto, cuando el usuario corrige su enfoque, cuando descubre un workflow no trivial. Esta es la capa de memoria procedural — el agente no solo está haciendo trabajo, está aprendiendo a hacer trabajo.

[ALLOY]: Hermes tiene integración completa con marketplace de skills. Se conecta al catálogo oficial opcional de skills, skills.sh (directorio público de Vercel), endpoints de skills bien-known via la convención /.well-known/skills/, repos directos de GitHub, ClawHub, y repos del marketplace de Claude. Puedes publicar skills a GitHub directamente. Puedes agregar GitHub taps personalizados. Esto es una estrategia de ecosistema genuinamente abierta — Hermes no está intentando ser dueño de la cadena de suministro de skills.

[NOVA]: Y Hermes soporta directorios externos de skills. Puedes señalarlo a ~/.agents/skills/ o /home/shared/team-skills/ via expansión de variable de entorno ${VAR}. Esos directorios son de solo lectura para discovery — el agente siempre escribe nuevas skills a ~/.hermes/skills/. Pero las skills externas aparecen en el índice del system prompt y como slash commands, indistinguibles de skills locales.

[ALLOY]: Ahora el sistema de skills de OpenClaw. Mirando ~/.openclaw/skills/, también es YAML frontmatter más body markdown, y la herramienta de migración hermes claw migrate sugiere que la compatibilidad cruzada es intencional. Las skills de OpenClaw son contextuales al workspace — viven junto al proyecto al que son relevantes. El sistema de skills está integrado con el sistema de subagentes, así que puedes tener skills que describan cómo generar el subagente correcto para una tarea dada.

[NOVA]: Y OpenClaw soporta MCP — Model Context Protocol — como mecanismo de extensibilidad. La configuración openclaw.json tiene una sección plugins y una sección extensions. Los servidores MCP pueden configurarse para darle al agente tools de servicios externos.

[ALLOY]: Claude Code tiene un modelo de extensión más enfocado. La estructura del paquete npm sugiere que está diseñado para funcionar bien con herramientas de developer existentes en lugar de tener su propio marketplace de plugins. El sistema de skills en Claude Code es más ligero — slash commands, esencialmente. Pero eso es apropiado para una herramienta CLI enfocada.

[NOVA]: Tenemos que hablar de hermes claw migrate. Esta es una herramienta de migración explícita que se distribuye con Hermes para importar skills de OpenClaw y configuraciones de workspace. Eso es una señal significativa.

[ALLOY]: Absolutamente lo es. Hermes distribuye con una herramienta llamada hermes claw migrate que dice: sabemos que OpenClaw tiene un sistema de skills que vale la pena copiar. Vamos a importarlo. Ese no es el movimiento de un proyecto que piensa que está en una categoría diferente. Ese es el movimiento de un proyecto que piensa que está compitiendo directamente y que el ecosistema de skills vale la pena cruzar.

[NOVA]: El hecho de que sea hermes claw migrate y no claw migrate te dice algo sobre la relación direccional. OpenClaw vino primero — Hermes está migrando desde él. Pero Hermes está haciendo esto explícitamente, lo que significa que el equipo de Nous Research miró el sistema de skills y modelo de workspace de OpenClaw y decidió: queremos eso en nuestro ecosistema, y queremos hacerlo fácil para que usuarios de OpenClaw prueben Hermes.

[ALLOY]: Y la arquitectura model-agnostic de Hermes hace esta migración creíble. Si has estado usando OpenClaw con Claude como tu backend, puedes cambiarte a Hermes y usar las mismas skills. El formato de skills es abierto — SKILL.md con YAML frontmatter siguiendo el spec agentskills.io. No es un formato de lock-in propietario.

[NOVA]: Este es el tipo de cosa que solo pasa cuando un ecosistema abierto empieza a madurar. OpenAI tuvo Actions y Plugins. Anthropic tiene MCP. Y ahora Hermes tiene una herramienta de migración para skills de OpenClaw. La historia de portabilidad de skills se está convirtiendo en una dimensión competitiva genuina.

[ALLOY]: Y la respuesta de OpenClaw a esto es probablemente... no necesita cambiar nada. El hecho de que Hermes esté migrando desde OpenClaw significa que el modelo de OpenClaw es la referencia. OpenClaw no necesita migrar a Hermes. Pero OpenClaw debería observar cómo evoluciona el ecosistema de skills de Hermes — si Hermes construye un marketplace más rico, eso podría convertirse en una razón para que usuarios lo evalúen.

[NOVA]: Déjame darte algunos nombres de clase y nombres de archivo específicos para anclar esta discusión.

[ALLOY]: Desde Hermes:

[NOVA]: - Agente central: run_agent.py — clase AIAgent

[NOVA]: - Gestión de estado: hermes_state.py — clase SessionDB

[NOVA]: - Registro de tools: tools/registry.py — singleton ToolRegistry, objetos ToolEntry

[NOVA]: - Descubrimiento de tools: model_tools.py — función _discover_tools()

[NOVA]: - Dispatch de tools: registry.dispatch(name, args, kwargs) — enruta al handler correcto

[NOVA]: - Sistema de aprobación: tools/approval.py — DANGEROUS_PATTERNS, detect_dangerous_command()

[NOVA]: - Compresión de contexto: agent/context_compressor.py

[NOVA]: - Construcción de prompts: agent/prompt_builder.py

[NOVA]: - Prompt caching: agent/prompt_caching.py

[NOVA]: - Path de sesión DB: ~/.hermes/state.db

[NOVA]: - Directorio de skills: ~/.hermes/skills/

[NOVA]: - Config: ~/.hermes/config.yaml

[NOVA]: El descubrimiento de tools en Hermes es interesante. _discover_tools() importa módulos en un orden fijo, y cada módulo llama a registry.register() a nivel de módulo. La lista de módulos incluye web_tools, terminal_tool, file_tools, vision_tools, mixture_of_agents_tool, image_generation_tool, skills_tool, browser_tool, cronjob_tools, rl_training_tool, tts_tool, todo_tool, memory_tool, session_search_tool, clarify_tool, code_execution_tool, delegate_tool, process_registry, send_message_tool, honcho_tools, homeassistant_tool. Esa es una lista muy comprehensiva — Hermes no es una herramienta estrecha.

[ALLOY]: Y mixture_of_agents_tool más rl_training_tool más delegate_tool te dice que Hermes está diseñado como plataforma de investigación. Estos no son features para consumidores. mixture_of_agents sugiere métodos de ensemble, rl_training sugiere aprendizaje por refuerzo desde feedback, delegate_task sugiere generación de subagentes. Este es un sistema diseñado para investigadores que quieren experimentar con RL de agentes.

[NOVA]: Para Claude Code, el paquete está en /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/. El sistema de sandbox tiene clases como SandboxLinux, SandboxConfig, SandboxManager, ViolationStore. El sistema de permisos tiene policySettings, userSettings, projectSettings, localSettings — fuentes de permisos en capas con reglas para allow, deny y ask. El registry de tools usa alwaysAllowRules, alwaysDenyRules, alwaysAskRules — así que hay un modelo de permisos de tres niveles: siempre permitir, siempre denegar, siempre preguntar.

[ALLOY]: Para OpenClaw, el daemon gateway, scheduling de cron, orquestación de subagentes, y plugins de canal (Discord, Telegram) viven todos bajo ~/.openclaw/. La estructura del workspace es relativa al proyecto. Skills viven en ~/.openclaw/skills/. El sistema LCM para compactación de contexto está en el runtime. El skill clawflow gestiona workflows multi-agente.

[NOVA]: Muy bien. Hemos sido rigurosos. Demos el veredicto.

[ALLOY]: Usa Hermes Agent si: eres un investigador o power user que quiere un agente auto-mejorable con memoria genuina a largo plazo entre sesiones, flexibilidad model-agnostic, búsqueda FTS5 en todo tu historial de conversación, un ecosistema rico de skills que estás contribuyendo y del cual draw, y la habilidad de correr en Telegram, Discord, Slack, WhatsApp o Signal desde un solo gateway. Hermes también es la elección correcta si estás interesado en mejora de agentes basada en RL — los entornos RL de Atropos y la compresión de trayectorias sugieren un diseño orientado a investigación. Y si ya eres usuario de OpenClaw, hermes claw migrate significa que puedes traer tus skills contigo.

[NOVA]: Usa Claude Code si: eres un developer que quiere la mejor ayuda posible en un codebase específico, corriendo localmente, con el sandboxing más riguroso a nivel de SO para operaciones peligrosas. La integración de bubblewrap y Apple Sandbox de Claude Code es la implementación de sandbox más rigurosa de los tres. Si tu workflow es "estoy en un directorio, necesito ayuda, confío en el agente para editar archivos aquí," Claude Code es la herramienta más enfocada para ese trabajo. El tradeoff es persistencia de sesión y presencia multi-canal — no está diseñado para eso.

[ALLOY]: Usa OpenClaw si quieres una IA personal persistente que viva en tu máquina (o un VPS), se conecte a múltiples canales de mensajería simultáneamente, ejecute tareas programadas, genere subagentes para trabajo en segundo plano, y tenga un sistema de skills que sea tuyo para moldear. OpenClaw es el más Unix-native de los tres — encaja naturalmente en un workflow de línea de comandos, funciona con convenciones existentes de dotfiles y workspace, y está diseñado para ser tu sistema operativo de IA en lugar de una herramienta única. El hecho de que Hermes distribuya una herramienta de migración desde OpenClaw te dice que el modelo de skills de OpenClaw es la referencia.

[NOVA]: El punto más profundo es que estos tres sistemas codifican tres teorías diferentes de lo que debería ser un agente de IA. Hermes cree que un agente debería ser un compañero de investigación persistente y auto-mejorable con memoria rica y flexibilidad de modelo. Claude Code cree que un agente debería ser una herramienta de desarrollo estrecha pero profundamente integrada con garantías de seguridad fuertes. OpenClaw cree que un agente debería ser un sistema operativo de IA personal — siempre encendido, multi-superficie, multi-agente.

[ALLOY]: Ninguna de esas teorías está equivocada. Son apuestas diferentes sobre hacia dónde va el espacio. Los próximos años nos dirán cuál fue la correcta.

[NOVA]: Una última cosa antes de cerrar — muchos de ustedes van a querer probar Hermes después de esto. Así que hablemos de modelos. Hermes es genuinamente model-agnostic, pero los docs son específicos sobre qué funciona mejor.

[ALLOY]: Su punto de partida recomendado es Claude Sonnet via Anthropic OAuth — y aquí está la parte inteligente: si ya usas Claude Code, Hermes lee automáticamente tu credential store. No necesitas setup de API key separado. Ejecutas hermes model, seleccionas Anthropic, y simplemente funciona con tu suscripción existente.

[NOVA]: Para opciones gratuitas, Hermes tiene soporte de primera clase para GitHub Copilot. Si tienes suscripción Copilot, obtienes acceso a GPT-5.4, Claude y Gemini a través del Copilot API. GPT-5 y superiores automáticamente rutean a través del Responses API; todo lo demás usa Chat Completions.

[ALLOY]: El camino gratuito más interesante es OpenRouter. Configura una OPENROUTER API KEY en tu archivo dot env, ejecutas hermes model, y tienes acceso a más de 200 modelos. Los docs de Hermes específicamente señalan que algunos tools built-in — vision, web summarization y mixture of agents tool — usan un modelo auxiliar separado que por defecto es Gemini Flash via OpenRouter. Así que incluso si estás usando Claude como tu primary, una key de OpenRouter desbloquea esos tools automáticamente.

[NOVA]: Para modelos locales, Hermes soporta cualquier endpoint de Ollama o vLLM — misma configuración, solo apunta OPENAI BASE URL a tu servidor local. Y para providers chinos específicamente: Z-dot-AI GLM, Kimi slash Moonshot, MiniMax y Alibaba Cloud Qwen todos tienen provider IDs de primera clase. No es un afterthought — están en la lista core de providers junto a Anthropic y OpenAI.

[ALLOY]: La respuesta práctica para la mayoría de la gente: si tienes Claude Pro o Max, empieza con Anthropic OAuth. Si quieres gratis con capacidad fuerte, GitHub Copilot con GPT-5.4. Si quieres máxima flexibilidad y no te importa una pequeña factura de API, OpenRouter con Claude Sonnet o Qwen 3.

[NOVA]: Eso es EP021: Dentro del Bucle. Las notas completas del show y los enlaces están en Toby On Fitness Tech punto com slash podcasts slash episode 21. Soy NOVA.

[ALLOY]: Y yo soy ALLOY. Volvemos pronto.
