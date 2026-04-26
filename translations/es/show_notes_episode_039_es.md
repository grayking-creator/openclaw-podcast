OPENCLAW DAILY — EPISODE 040 — 25 de abril de 2026

[00:00] INTRO / GANCHO
OpenClaw v2026.4.23 es la versión estable más reciente, y debido a que v2026.4.22,
v2026.4.21 y v2026.4.20 ya fueron cubiertas en las notas del episodio reciente,
v2026.4.23 es el único bloque de release válido al inicio del EP039.

Y esta vale la pena ocupar el primer lugar.
Facilita sustancialmente la generación de imágenes en OpenAI Codex OAuth y
OpenRouter, ofrece a los agentes una forma más limpia de bifurcar ejecuciones
secundarias con contexto heredado, añade timeouts por llamada para trabajos de
generación de medios de larga duración, y continúa limpiando aspectos de Codex,
comprensión de medios, webchat y seguridad que importan cuando OpenClaw está
haciendo trabajo real en lugar de solo pasar demos.

Después de esa inmersión profunda en el release, pasamos a la inversión
planeada de Google en Anthropic, la vista previa del V4 de DeepSeek, y la
advertencia de Vercel de que su brecha puede ser más amplia y más antigua de
lo que se reveló inicialmente.

[01:30] HISTORIA 1 — OpenClaw v2026.4.23 Hace la Generación de Imágenes Más Fácil de Operar en la Práctica
El cambio principal en v2026.4.23 es que OpenClaw continúa sacando el trabajo
de imágenes del "caso especial" y llevándolo al runtime normal.

En el lado de OpenAI, `openai/gpt-image-2` ahora puede hacer generación y
edición de imágenes de referencia a través de Codex OAuth. Eso importa porque
elimina una de las divisiones de flujo de trabajo más molestas en la pila. Si
un operador ya está firmado a través de Codex, el trabajo de imágenes ya no
tiene que detenerse y pedir una `OPENAI_API_KEY` separada solo para usar la
misma familia de proveedores. La superficie de imágenes se vuelve más continua
con el resto de la ruta autenticada de OpenAI.

OpenRouter obtiene una mejora paralela. La generación de imágenes y la edición
de imágenes de referencia ahora fluyen a través de `image_generate` con
`OPENROUTER_API_KEY`, que es exactamente el tipo de estandarización que
OpenClaw necesita. Un runtime multi-proveedor mejora cuando las nuevas
capacidades del proveedor llegan a través de la misma ruta de herramientas en
lugar de forzar manejo específico en los bordes.

También hay una historia de calidad de herramientas aquí, no solo una historia
de proveedor. v2026.4.23 permite que los agentes soliciten sugerencias de
calidad y formato de salida compatibles con el proveedor, y pasen controles
específicos de OpenAI como fondo, moderación, compresión y sugerencias de
usuario a través de `image_generate`. En la práctica, esto significa que los
flujos de trabajo de imágenes pueden expresar más intención en el momento de
la llamada en lugar de depender de una interfaz universal delgada que oculta
características útiles del proveedor.

Eso importa para los constructores porque la generación de imágenes deja de
ser una capacidad binaria de sí o no. Se convierte en una superficie de flujo
de trabajo controllable. Puedes preocuparte por el formato de salida,
compresión, comportamiento de timeout, ediciones de imágenes de referencia y
parámetros específicos del proveedor sin salir del modelo de herramientas
compartido.

同样重要的是，这个版本中图像工作看起来更像是一条支持的生产通道，而不是一个附加组件。 OpenAI-authenticated users, OpenRouter users, and agent-driven tool calls all get a more coherent path, which means fewer awkward auth fallbacks, fewer provider-specific workarounds, and less reason to treat media generation as a separate subsystem.

[09:30] HISTORIA 1B — Contexto de Subagente, Trabajos de Medios de Larga Duración y la Ruta de Codex Se Vuelven Más Limpias
La segunda mejora principal en v2026.4.23 está en el lado del runtime de
agentes.

Las ejecuciones nativas de `sessions_spawn` ahora obtienen herencia de contexto
bifurcada opcional. Eso es un gran negocio para cualquiera que realmente usa
subagentes como parte de un flujo de trabajo. Hasta ahora, el valor
predeterminado de sesión limpia aislada era a menudo la opción de seguridad
correcta, pero hay trabajos reales donde el secundario debe heredar la
transcripción del solicitante para no tener que ser re-briefeado desde cero.
El release mantiene el aislamiento como predeterminado, pero añade un camino
intermedio más deliberado: hereda contexto cuando ayuda, mantente limpio cuando
no lo hace.

Eso hace que la delegación sea más práctica. Significa que los operadores
pueden preservar la continuidad de la transcripción para trabajo secundario
limitado sin convertir cada subagente en un clon no controlado del padre. Para
OpenClaw, esa es exactamente la forma correcta de mejora: más capacidad, pero
con la superficie de control todavía explícita.

El nuevo soporte opcional de `timeoutMs` por llamada para herramientas de
generación de imágenes, video, música y TTS es otro cambio silenciosamente
importante. Los trabajos de generación de larga duración son uno de los
lugares más comunes donde un runtime puede sentirse poco confiable incluso
cuando el proveedor simplemente es lento. Esta actualización permite a los
agentes extender los timeouts de solicitud solo para la llamada que lo necesita.
Eso es mejor que elevar todo globalmente y esperar que nada más se comporte
de forma extraña.

También hay una capa significativa de limpieza de Codex y catálogo de modelos.
Los paquetes Pi agrupados pasan a 0.70.0, los metadatos del catálogo upstream
de `gpt-5.5` se adoptan para OpenAI y OpenAI Codex, y el release añade registro
de depuración estructurado alrededor de la selección de harness embebido para
que `/status` permanezca legible mientras los logs del gateway todavía expliquen
por qué se eligió un harness o por qué ocurrió el fallback de Pi. Esa es la
división correcta del operador: superficie simple, logs más profundos cuando
necesitas depurar la realidad.

[17:30] HISTORIA 1C — La Lista de Correcciones Realmente Se Trata de Reducir Sorpresas en Despliegues Reales
Mucho del valor en v2026.4.23 está en la lista de correcciones, porque ahí es
donde el runtime deja de traicionar las expectativas del operador.

Los prompts de `request_user_input` de Codex se enrutan de vuelta al chat
originador y las respuestas de seguimiento en cola se preservan. Eso significa
que el sistema mejora en el traspaso humano de múltiples turnos en lugar de
perder contexto exactamente en el momento en que se requiere una decisión humana.

Las respuestas finales duplicadas de block-streaming se suprimen cuando los
fragmentos parciales ya han cubierto completamente la respuesta. Las superficies
de grupos de Slack dejan de filtrar trazas internas de "Trabajando...".
WebChat obtiene errores de facturación, auth y límite de tasa no reintentables
presentados en lugar de fallar en blanco. Los modelos primarios solo de texto
ahora preservan las imágenes adjuntas como referencias de medios para que las
herramientas de imágenes posteriores puedan inspeccionarlas. La configuración
explícita de modelo de imagen se respeta antes de los saltos de visión nativa,
y los modelos de imagen de Codex obtienen vueltas de imagen del servidor de
aplicaciones limitadas con enrutamiento más correcto.

Estos no son puntos llamativos, pero cambian directamente si el sistema se
siente confiable. Lo mismo es cierto para las correcciones de auth y enrutamiento
alrededor de la generación de imágenes de OpenAI. El enrutamiento de Codex
OAuth se endurece, las filas faltantes del catálogo de `openai-codex/gpt-5.5`
se sintetizan cuando el descubrimiento las omite, las ediciones complejas de
imágenes de referencia se restauran a través de cargas multipart protegidas, y
las filas de modelos Codex obsoletas se suprimen. Ese es el tipo de trabajo de
release que convierte una característica de "técnicamente presente" a "segura
para apoyarse".

También hay una historia seria de seguridad y límites. El release endurece la
edición de configuración del gateway, el comportamiento de actualización de
secretos de webhook, las reglas de texto plano de Android y emparejamiento, la
validación de tokens de Teams, la resolución de configuración de plugins, el
comportamiento de aprobación, la aplicación de acceso a Discord, la exposición
del puente MCP, y múltiples rutas de metadatos relacionados con inyección de
prompts a través de transportes de chat.

Entonces la lectura práctica de v2026.4.23 no es solo "más funciones".
Es OpenClaw haciendo que tres superficies sean más reales a la vez: generación de medios, delegación de agentes y confianza del operador. El trabajo de imagen se vuelve más fácil de enrutar. Los subagentes obtienen un mejor modelo de control de contexto. Y el runtime gasta mucha energía evitando que pequeños bordes de transporte y autenticación se conviertan en fallas extrañas orientadas al usuario.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.23

[26:00] HISTORIA 2 — El compromiso de Google con Anthropic es una apuesta de apalancamiento computacional, no solo una ronda de financiamiento
La inversión planeada de Google de hasta 40 mil millones de dólares en Anthropic es fácil de leer como un titular de valoración. Esa es la parte menos interesante.

La parte más importante es que el trato viene acompañado de más capacidad computacional de Google Cloud, especialmente acceso a TPU. Anthropic ya se encuentra en una posición donde la calidad del modelo, los límites de uso y la disponibilidad de infraestructura están visiblemente vinculados. Así que cuando Google profundiza tanto la relación de capital como la relación computacional, no está solo comprando upside en un laboratorio competidor. Está fortaleciendo su posición en la capa de infraestructura que los laboratorios frontier cada vez más no pueden vivir sin.

Eso es lo que hace que esta historia sea útil para constructores y operadores.
El mercado de IA se está volviendo más entrelazado verticalmente. La misma compañía puede ser un competidor en modelos, un proveedor de cómputo, una plataforma de distribución y un inversionista estratégico. Eso significa que la competencia de modelos ya no es una pelea limpia entre laboratorios aislados. Es una pelea de sistemas por capacidad de entrenamiento, capacidad de inferencia, margen en la nube y quién obtiene acceso preferencial cuando la demanda aumenta.

Para Anthropic, la lectura inmediata es obvia.
Más efectivo y más cómputo compran espacio para seguir escalando Mythos, Claude y productos relacionados sin dejar que los cuellos de botella de infraestructura se conviertan en toda la historia. Para Google, la lógica es más sutil. Cada dólar y cada hora de TPU vendida a Anthropic no es solo financiamiento. Es una forma de hacer que Google Cloud sea más central para uno de los pocos laboratorios que aún pueden mover la conversación de la frontera.

La implicación más amplia es que los proveedores de modelos que parecen independientes pueden volverse cada vez más dependientes de las relaciones de nube y silicio que puedan asegurar tempranamente.
Eso importa porque la confiabilidad, los límites y la velocidad de despliegue a menudo son tanto una historia de cómputo como una historia de modelado.
→ https://techcrunch.com/2026/04/24/google-to-invest-up-to-40b-in-anthropic-in-cash-and-compute/

[32:30] HISTORIA 3 — DeepSeek V4 reabre la pregunta sobre presión de precios en modelos de peso abierto
La vista previa de V4 de DeepSeek merece atención, no porque cada afirmación de benchmark deba confiarse inmediatamente, sino porque la forma del anuncio es estratégicamente importante.

La compañía dice que los nuevos modelos Flash y Pro llegan a una ventana de contexto de un millón de tokens, usan arquitecturas de mezcla de expertos muy grandes, y vienen con un precio que undercut a las opciones de modelos frontier cerrados. Si eso se sostiene en uso real, entonces DeepSeek no está solo enviando otra curiosidad de peso abierto. Está presionando las suposiciones económicas detrás del enrutamiento premium cerrado.

Para constructores, la pregunta clave no es si DeepSeek ya ganó.
La pregunta útil es qué tipo de carga de trabajo se vuelve recién tentadora cuando la ventana de contexto es enorme y el precio es lo suficientemente bajo como para hacer que el uso amplio se sienta menos imprudente. Análisis de bases de código grandes, recuperación de documentos largos, razonamiento por lotes y enrutamiento de menor riesgo se vuelven más fáciles de justificar cuando el piso de costos baja.

Eso crea presión estratégica en todo el mercado.
Los proveedores frontier cerrados aún ganan en amplitud multimodal, capas de seguridad y en muchos casos calidad absoluta. Pero si una familia de peso abierto se acerca lo suficiente en razonamiento textual y tareas de código, los operadores ganan más palanca. Pueden reservar llamadas premium cerradas para turnos de alto valor y descargar tráfico más amplio a alternativas más baratas sin sacrificar capacidad seria.

Así que incluso con la precaución normal alrededor de afirmaciones de vistas previas, DeepSeek V4 importa como una historia de precios y enrutamiento ahora mismo.
Le recuerda a todos que el lado de peso abierto del mercado aún está estableciendo un techo sobre qué tan complacientes pueden permitirse ser los proveedores de modelos premium.
→ https://techcrunch.com/2026/04/24/deepseek-previews-new-ai-model-that-closes-the-gap-with-frontier-models/

[38:00] HISTORIA 4 — La actualización de Vercel sobre la brecha muestra por qué el incidente real a menudo es más grande que la primera historia
La última actualización de Vercel es la advertencia de operador para tomar en serio esta semana.

La compañía ahora dice que encontró evidencia de que algunas cuentas de clientes fueron comprometidas antes de la ventana de la brecha que originalmente divulgó, y que también se han identificado más cuentas de clientes vinculadas al incidente de abril. Eso significa que la historia ya no es solo "un empleado descargó la app equivocada y un atacante pivoteó desde ahí". Puede ser una imagen de compromiso más larga con un radio de impacto más amplio de lo que sugirió la primera divulgación.

La lección de seguridad aquí es brutal pero familiar.
Una vez que los atacantes obtienen acceso a máquinas de desarrolladores, tokens, variables de entorno u otros secretos de cuenta, no necesitan la narrativa limpia que desearían los defensores del incidente. Solo necesitan un camino que funcione. Y una vez que tienen ese camino, las APIs de plataforma, sistemas internos e infraestructura vinculada a clientes pueden terminar en alcance muy rápidamente.

Esto también importa porque Vercel se encuentra en una parte muy expuesta del stack.
Un compromiso en una plataforma de desarrolladores rara vez se contiene en una sola app. Puede derramarse en secretos de despliegue, metadatos de proyectos, integraciones y sistemas de clientes posteriores. Por eso las historias como esta importan más allá del proveedor afectado. Son realmente historias sobre cuánto poder operativo se acumula alrededor de las credenciales de desarrolladores.

Así que la lección práctica es simple.
Si operas herramientas modernas de desarrollo alojadas, los infostealers y el robo de secretos no son riesgos de canal lateral. Son riesgos centrales. Y si el primer informe de incidente suena estrecho, trátalo como el comienzo de la investigación, no la forma final del problema.
→ https://techcrunch.com/2026/04/23/vercel-says-some-of-its-customers-data-was-stolen-prior-to-its-recent-hack/

[44:00] OUTRO / CIERRE
Eso es suficiente por hoy.
OpenClaw v2026.4.23 empujó la generación de imágenes, el control de contexto de subagentes y la corrección del operador hacia adelante de maneras que realmente se sentirán en producción.
El trato de Google con Anthropic mostró cómo el acceso a cómputo se está convirtiendo en poder estratégico.
DeepSeek V4 mantuvo viva la presión de precios en el lado de peso abierto del mercado.
Y Vercel recordó a todos que la parte fea de la seguridad de plataformas generalmente es más amplia que la primera divulgación.

→ Responde aquí para aprobar la generación de transcripción.