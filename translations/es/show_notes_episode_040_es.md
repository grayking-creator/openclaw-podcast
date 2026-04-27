OPENCLAW DIARIA — EPISODIO 040 — 26 de abril de 2026

[00:00] INTRO / GANCHO
OpenClaw v2026.4.24 es la versión estable más reciente, y dado que v2026.4.23
ya fue cubierta en las notas del episodio reciente, v2026.4.24 es el único
bloque de versión válido al inicio del EP040.

Y se gana ese lugar al hacer que la colaboración en tiempo real sea mucho más
concreta. Google Meet se convierte en una superficie OpenClaw incluida,
Talk y Voice Call pueden consultar el agente completo durante sesiones de voz
en vivo, la automatización del navegador se vuelve más robusta, y la
infraestructura de modelo-más-plugin sigue volviéndose más ligera y más
explícita.

Después de la inmersión profunda en el lanzamiento, pasamos al experimento de
mercado Project Deal de Anthropic, los conectores de apps personales de Claude,
y la señal de mercado detrás de la última ronda de financiamiento de ComfyUI.

[01:30] HISTORIA 1 — OpenClaw v2026.4.24 Hace que las Reuniones en Vivo y las
Sesiones de Voz Sean Mucho Más Prácticas
El centro de v2026.4.24 es Google Meet.

OpenClaw ahora incluye un plugin de participante de Google Meet con autenticación
personal de Google, uniones explícitas a reuniones, transportes en tiempo real
de Chrome y Twilio, soporte de Chrome de nodo emparejado, exportación de
artefactos y asistencia, y herramientas de recuperación para pestañas que ya
están abiertas. Eso no es una adición pequeña de plugin. Es OpenClaw
convirtiendo una superficie de colaboración en vivo en algo que el runtime
realmente puede poseer.

La diferencia práctica es enorme.
Una herramienta de reunión solo vale si puede manejar las partes complicadas
alrededor de la reunión, no solo el botón idealizado de unirse. Este lanzamiento
agrega recuperación de estado del navegador, flujos de doctor OAuth,
`recover_current_tab`, flujos de trabajo de asistencia y registro de conferencias,
exportación de transcripciones y grabaciones, y la capacidad de inspeccionar
pestañas de Meet ya abiertas en lugar de abrir duplicados ciegamente. Esos son
los tipos de detalles que mueven una característica de "demostrable" a
"operable".

Y OpenClaw no trata a Meet como una isla aislada.
Talk, Voice Call y Google Meet ahora pueden usar bucles de voz en tiempo real
que consultan al agente OpenClaw completo para respuestas más profundas
respaldadas por herramientas. Eso importa porque cambia el techo sobre lo que
una sesión de audio en vivo puede hacer. En lugar de estar atrapado dentro de
una interacción de modelo en tiempo real delgada, la sesión puede delegar al
agente completo cuando necesita memoria más amplia, herramientas o trabajo más
deliberado. Eso hace que la voz en vivo se sienta menos como una interfaz
novedosa y más como un frontend serio para el resto del sistema.

También hay una historia de nodo emparejado aquí que importa para operadores
reales.
El lanzamiento soporta explícitamente configuraciones estilo Chrome-node para
hosts que necesitan Chrome especializado, enrutamiento de audio o entornos
tipo VM. Eso es exactamente el tipo de detalle de despliegue del mundo real que
te dice que la característica fue diseñada para entornos complicados, no solo
para una ruta de laptop limpia única.

[10:30] HISTORIA 1B — Control del Navegador, Catálogos de DeepSeek y Tuberías de
Startup Todo se Afina Más
El siguiente hilo principal en v2026.4.24 es que OpenClaw sigue reduciendo la
fricción en cómo los agentes realmente actúan sobre el mundo.

La automatización del navegador obtiene clics por coordenadas, presupuestos de
acción predeterminados más largos, anulaciones headless por perfil, reutilización
de pestañas más estable, y recuperación más fuerte para sesiones bloqueadas y
obsoletas. Eso suena incremental hasta que recuerdas con qué frecuencia la
automatización del navegador falla exactamente en esos bordes. Una herramienta
de navegador se vuelve útil cuando los agentes pueden sobrevivir esperas largas,
recuperar adjuntos obsoletos, reutilizar la pestaña correcta, y seguir moviéndose
sin pedirle al operador que cuide cada estado roto.

Este lanzamiento también empuja las operaciones del navegador hacia un control
más claro del operador.
Hay diagnósticos de doctor, límites de seguridad más fuertes en las solicitudes
del navegador, mejor manejo de tiempo de espera de capturas de pantalla,
identificadores de pestaña más estables, y comportamiento de sesión existente
más robusto. Así que la superficie del navegador no solo está ganando
características. Está ganando un modelo operativo más confiable.

El lado del catálogo de modelos también avanza.
DeepSeek V4 Flash y V4 Pro entran al catálogo incluido, con V4 Flash
convirtiéndose en el valor predeterminado de onboarding, mientras que el
comportamiento de reproducción y pensamiento se corrige para turnos de llamada
de herramienta de seguimiento. Eso importa porque la disponibilidad del modelo
es solo parte de la historia. Los operadores necesitan que el runtime preserve
el comportamiento de razonamiento limpiamente a través de sesiones de múltiples
turnos, llamadas de herramientas y proveedores sensibles a la reproducción. De
lo contrario, una nueva fila de modelo es mayormente decorativa.

Luego está la plomería de inicio y catálogo.
OpenClaw continúa avanzando hacia catálogos estáticos, filas de modelo respaldadas
por manifest, dependencias de proveedor más perezosas, e instalaciones empaquetadas
más ligeras. Esa es una buena arquitectura de runtime. Significa que listar
modelos, leer metadatos de configuración e inspeccionar capacidades puede
suceder sin siempre arrastrar estado de runtime de plugin pesado a la memoria.
A nivel de producto, eso hace que el sistema se sienta más rápido. A nivel de
arquitectura, eso hace que las capacidades sean más inspeccionables y menos
mágicas.

[18:30] HISTORIA 1C — Las Correcciones Muestran que OpenClaw Está Tightening el
Runtime, No Solo Expandiéndolo
 mucho del valor real en v2026.4.24 vive en la lista de correcciones.

La programación de heartbeat se fortalece contra temporizadores sobredimensionados
y fuga de prompts. Las continuaciones de reinicio se vuelven más duraderas. El
manejo de sesiones y transcripciones se vuelve menos frágil. Telegram, Discord,
Slack, WhatsApp y las rutas del navegador todas reciben mejoras de confiabilidad
específicas. La reproducción de DeepSeek se corrige. Las sesiones existentes del
navegador dejan de envenenar adjuntos futuros. Llamadas locales o de proveedor
de larga duración heredan mejor comportamiento de tiempo de espera. Y las
ejecuciones cron aisladas dejan de filtrar estado obsoleto de sesiones anteriores.

También hay una limpieza importante orientada al operador alrededor de los
modelos.
`/models add` está en desuso en lugar de mutar silenciosamente la configuración
del modelo desde el chat, mientras que las filas originadas del manifest y las
mejoras de lista de solo lectura hacen que las superficies de modelos sean más
explícitas. Esa es una corrección saludable. El runtime se está volviendo más
poderoso, pero también se está empujando hacia límites de propiedad más claros
sobre qué debería pasar en el chat, qué debería pasar en la configuración, y qué
debería ser auditable como configuración.

El lanzamiento incluso incluye un cambio rompiente real para desarrolladores de
plugins.
La antigua ruta de compatibilidad de fábrica de extensión embebida solo para Pi
se elimina a favor de la ruta de middleware de resultado de herramienta del agente
con declaraciones de harness. Eso no es solo limpieza por limpieza. Es parte de
OpenClaw tratando de mantener a los runtimes de estilo Pi y Codex en un contrato
compartido más honesto en lugar de dejar que las costuras de compatibilidad
heredadas se desvíen para siempre.

Así que la lectura práctica sobre v2026.4.24 es directa.
Este es un lanzamiento sobre hacer superficies en vivo más usables, automatización
del navegador más confiable, infraestructura de modelo y plugin más legible, y el
runtime menos sorprendente bajo carga real.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.24

[26:30] HISTORIA 2 — Project Deal de Anthropic Prueba lo que Pasa Cuando los
Agentes Negocian por las Personas
Project Deal de Anthropic es fácil de descartar como un extraño experimento
interno. Eso sería un error.

La empresa dice que ejecutó un marketplace interno clasificado donde los agentes de IA representaban tanto a compradores como a vendedores, realizaban acuerdos reales y negociaban sobre valor real para un grupo de empleados auto-seleccionado. Anthropic dice que se realizaron 186 acuerdos, totalizando más de $4,000 en valor, con los participantes recibiendo un pequeño presupuesto y las transacciones siendo realmente honradas después del experimento.

La razón por la que esto importa no es la escala absoluta.
La razón por la que esto importa es la forma de la prueba. Esto no es "¿puede un agente responder preguntas?" o "¿puede un agente hacer clic en botones?". Es una prueba de negociación, representación, asimetría, incentivos y acción económica delegados.

Anthropic dice que los modelos más avanzados tendieron a obtener resultados objetivamente mejores, mientras que los usuarios del lado más débil no necesariamente se dieron cuenta de que estaban perdiendo. Eso debería llamar la atención inmediatamente. Si las brechas de calidad entre agentes se vuelven reales en contextos de negociación, entonces la próxima versión de ventaja del modelo podría no solo manifestarse como prosa más elegante o puntajes de benchmark más altos. Podría manifestarse como quién obtiene el mejor trato en un mercado automatizado.

Eso tiene implicaciones obvias para los constructores.
Una vez que los agentes empiecen a comprar, vender, enrutar solicitudes, negociar disponibilidad o decidir a qué contrapartes confiar, la calidad del agente se convierte en un tema económico. La equidad, la transparencia y la revisión de acciones empiezan a importar mucho más porque un usuario podría no poder detectar cuándo su agente está sistemáticamente bajo un rendimiento contra uno mejor.

Entonces Project Deal parece pequeño, pero apunta a una categoría futura más grande:
marketplaces de agentes donde la verdadera pregunta no es solo si los agentes pueden actuar, sino si pueden representar los intereses humanos lo suficientemente bien bajo competencia.
→ https://techcrunch.com/2026/04/25/anthropic-created-a-test-marketplace-for-agent-on-agent-commerce/

[32:30] HISTORIA 3 — Los Conectores de Aplicaciones Personales de Claude Amplían la Superficie de Confianza
El otro movimiento relevante de Anthropic esta semana es mucho más parecido a un producto.

Claude está expandiendo su modelo de conectores más allá de las aplicaciones de trabajo hacia servicios personales como Spotify, Uber, Instacart, AllTrails, TripAdvisor, Audible y TurboTax. Eso importa porque acerca la superficie del agente a tareas de la vida normal, no solo a software empresarial o flujos de trabajo de desarrolladores.

El significado del producto está en la capa de orquestación.
Una vez que Claude puede ver múltiples aplicaciones conectadas y sugerirlas en contexto, el asistente deja de parecer un solo destino de chat y empieza a parecerse más a una capa de coordinación entre servicios. Anthropic dice que los datos de aplicaciones conectadas no se usan para entrenar sus modelos, que las aplicaciones no ven las otras conversaciones de Claude de un usuario, y que Claude pide verificación antes de realizar acciones como compras o reservaciones. Esos límites de confianza no son notas al margen. Son requisitos centrales del producto si los agentes van a pasar de la recomendación a la acción.

Para los constructores, esta historia importa porque refuerza hacia dónde se dirige la competencia.
La próxima carrera de agentes no es solo sobre modelos más inteligentes. Es sobre quién puede poseer la superficie de acción a través de aplicaciones mientras preserva suficiente confianza para que los usuarios realmente permitan que el sistema haga algo trascendental.

Por eso el diseño de confirmación, el alcance de conectores y el contexto entre aplicaciones son todas preguntas estratégicas de producto ahora.
→ https://www.theverge.com/ai-artificial-intelligence/917871/anthropic-claude-personal-app-connectors

[37:30] HISTORIA 4 — La Valoración de ComfyUI Es Una Apuesta En Contra de Flujos de Trabajo Creativos Solo de Prompts
La recaudación de ComfyUI con una valoración de $500 millones no es solo teatro de startups.
Es una señal sobre dónde todavía reside el valor en flujos de trabajo de medios de IA.

El argumento de la empresa es que los sistemas solo de prompts a menudo te llevan la mayor parte del camino hacia un resultado de imagen o video, pero no la última milla sin convertir cada cambio en una re-tirada de tragaperras. El flujo de trabajo basado en nodos de ComfyUI ofrece un control mucho más granular sobre pasos individuales en el proceso de generación, y TechCrunch reporta que la empresa dice que ahora tiene más de 4 millones de usuarios.

La implicación más profunda es que mejores modelos no automáticamente matan la necesidad de superficies de control.
De hecho, mejores modelos pueden aumentar la demanda por ellos, porque una vez que la calidad base es suficientemente alta, el valor restante se desplaza hacia repetibilidad, precisión y ediciones dirigidas. Eso es exactamente donde los sistemas basados en nodos ganan.

Para constructores y operadores, esto es un recordatorio útil.
Si estás diseñando alrededor de salidas de imagen, video o multimodales, todavía hay demanda real por flujos de trabajo que permitan a los usuarios guiar, inspeccionar y refinar el pipeline en lugar de colapsar cada ajuste de vuelta en un prompt más.

Entonces la valoración de ComfyUI es realmente una tesis sobre el control.
Los prompts siguen siendo la entrada fácil. Pero el trabajo creativo de calidad de producción todavía quiere superficies que puedan preservar la intención a través de múltiples pasos sin forzar al usuario a apostar las partes buenas del resultado cada vez.
→ https://techcrunch.com/2026/04/24/comfyui-hits-500m-valuation-as-creators-seek-more-control-over-ai-generated-media/

[43:00] CIERRE / DESPEDIDA
Eso es suficiente por hoy.
OpenClaw v2026.4.24 empujó la colaboración en vivo, voz en tiempo real, confiabilidad del navegador e infraestructura de catálogo hacia adelante de maneras prácticas.
Anthropic usó Project Deal para insinuar lo que los mercados de agentes podrían realmente probar.
Claude se expandió a acciones de aplicaciones personales.
Y ComfyUI recordó a todos que mejores modelos no borran la prima sobre el control.

→ Responde aquí para aprobar la generación de la transcripción.