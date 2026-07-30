Episodio 095 — 30 de julio de 2026

[00:00] Introducción del episodio

Lectura de lanzamientos del Agent Stack: OpenAI Codex rust-v0.146.0 lidera un ciclo denso. GitHub Copilot para JetBrains añade controles de OpenTelemetry y gestión de modelos, Dos configuraciones de GPT-5.6 que triplicaron su puntuación en ARC-AGI-3, Liquid AI lanza dos codificadores de contexto largo amigables con CPU completan la primera parte del episodio, con análisis más profundos sobre modelos, herramientas e infraestructura detrás de ellos. Cada historia recibe el mismo tratamiento — qué se lanzó, el mecanismo subyacente y qué cambia para los desarrolladores que trabajan.

[02:00] Lectura de lanzamientos del Agent Stack: OpenAI Codex rust-v0.146.0

OpenAI lanzó Codex rust-v0.146.0 el 29 de julio de 2026, y el lanzamiento es amplio: manifiestos de Agent Plugins además de nuevos mercados para Amazon Bedrock y Claude Code, un puente WebSocket de app-server a hosts remotos de Code Mode, e hilos bifurcables con historial paginado, incluyendo bifurcaciones temporales que no aparecen en la lista de hilos. Las sesiones ahora pueden nombrarse desde /new o /clear, los hilos importantes pueden fijarse y los usuarios pueden cambiar entre conversaciones laterales sin cerrarlas.

Para quienes ejecutan Codex contra estaciones de trabajo en la nube, el cambio de WebSocket es la victoria más concreta. El app-server puede conectarse a un host de Code Mode en una máquina diferente a través de WebSocket en lugar de esperar ejecución local, así que un cliente ligero en tu portátil puede controlar herramientas, plugins y aprobaciones en un entorno remoto más pesado. La búsqueda web independiente ahora está disponible para proveedores de modelos personalizados compatibles, así que las rutas de modelos de terceros pueden ejecutar sus propias búsquedas fundamentadas en lugar de enrutarse a través del stack de OpenAI.

El trabajo de plugins es donde los equipos probablemente sentirán el cambio más grande. Codex ahora soporta el formato de manifiesto de Agent Plugins y puede obtener contenido de los mercados de Amazon Bedrock y Claude Code además de su propio flujo de publicación del workspace. Una organización que ya estandariza en manifiestos puede publicar una definición de paquete y hacer que viaje entre runtimes en lugar de reescribir por host. El lanzamiento también añade una forma de descubrir habilidades proporcionadas por el ejecutor y leer sus recursos asociados, incluyendo habilidades explícitamente seleccionadas.

El resto es un largo paso de limpieza. Los proxies ahora se respetan consistentemente en autenticación, descargas de plugins, autorización MCP, ejecución remota, WebSockets, redirecciones y conexiones de LM Studio. Las conexiones MCP y las herramientas de Apps se actualizan en cambios de autenticación o configuración, reconectando servidores cerrados sin perturbar los que funcionan bien. Los mensajes enviados, respuestas finales, errores de turnos fallidos, marcas de tiempo importadas y configuraciones de aprobación se preservan a través de interrupciones, repeticiones, importaciones y bifurcaciones.

El manejo de terminal también recibió atención: interrupciones no bloqueantes, mejor comportamiento del teclado, correcciones de diseño estrecho, hipervínculos y resultados de menciones actualizados. En Windows, las teclas de navegación están corregidas y los árboles de procesos en sandbox terminan de manera confiable. Bajo presupuestos de contexto ajustados, más habilidades se retienen y el CLI advierte cuando el catálogo de habilidades tiene que truncarse, lo cual importa para sesiones largas que gradualmente acumulan herramientas.

[03:03] GitHub Copilot para JetBrains añade controles de OpenTelemetry y gestión de modelos

GitHub lanzó una actualización de su plugin Copilot para IDEs de JetBrains que da a los desarrolladores más control y claridad sobre la configuración de telemetría y la gestión de modelos. El cambio principal es la configuración mejorada de OpenTelemetry. OpenTelemetry es el estándar abierto para enviar logs, trazas y métricas a cualquier stack de observabilidad que use un equipo, y ajustarlo permite a los administradores modificar qué se envía y dónde llega en lugar de aceptar los valores predeterminados.

La actualización también añade gestión de modelos más clara, dando a los desarrolladores un control más explícito sobre qué modelos de IA están conectados a su entorno de JetBrains. Junto a eso, el lanzamiento permite conectar servidores MCP y agentes personalizados dentro de flujos de agente de Claude. MCP — Model Context Protocol — es el estándar abierto de Anthropic que permite a un agente de IA llamar herramientas externas y fuentes de datos a través de una interfaz uniforme. Los agentes personalizados permiten a los equipos definir asistentes especializados ajustados a un flujo de trabajo particular.

Para los desarrolladores, el resultado práctico es doble. Los equipos con necesidades de auditoría o seguimiento de costos ahora pueden enrutar la telemetría de Copilot al mismo pipeline de observabilidad que usan para todo lo demás, lo que hace visible el uso de IA junto con el tráfico regular de aplicaciones. Y cualquier herramienta interna que ya exponga un endpoint MCP — una base de datos propietaria, una API interna, un índice de código específico de la empresa — se vuelve accesible desde un flujo de agente de Claude dentro de JetBrains sin escribir código de pegamento personalizado. Vale la pena estar atento a si GitHub trae controles equivalentes de gestión de modelos y telemetría a la superficie de VS Code.

[04:31] Dos configuraciones de GPT-5.6 que triplicaron su puntuación en ARC-AGI-3

OpenAI publicó un breve artículo el 29 de julio explicando cómo habilitar dos configuraciones de API triplicó las puntuaciones de GPT-5.6 en el benchmark ARC-AGI-3 mientras también mejoraba la eficiencia. ARC-AGI-3 es la prueba de razonamiento estilo puzzle diseñada para resistir la coincidencia de patrones por fuerza bruta, así que un salto de tres veces es una señal real en lugar de un ajuste en el ranking.

Las dos configuraciones son directas. La primera retiene el razonamiento a través de turnos, lo que significa que los pensamientos de trabajo del modelo persisten entre pasos en lugar de descartarse. La segunda activa la compactación, que resume el contexto de razonamiento más antiguo para que el uso de tokens se mantenga manejable mientras la cadena de pensamiento permanece disponible. Juntas permiten que GPT-5.6 lleve adelante ideas anteriores sin pagar el costo completo de tokens de preservar cada pensamiento previo de forma literal.

El resultado, según OpenAI, es puntuaciones más altas con menos tokens gastados — mejor resolución de puzzles a menor costo, lograda a través de configuración en lugar de reentrenamiento o un nuevo lanzamiento de modelo. Esa es una combinación inusual; usualmente se intercambia computación por precisión, no se obtienen ambas a la vez.

Para los desarrolladores, la conclusión práctica es que el GPT-5.6 por defecto podría estar dejando rendimiento sobre la mesa en trabajo de razonamiento difícil. Si ya estás usando el modelo para problemas de múltiples pasos, bucles de agente o cualquier cosa que se beneficie de llevar el contexto hacia adelante, probar con estas dos configuraciones habilitadas es un experimento de bajo esfuerzo que podría cambiar significativamente los resultados. Estén atentos a que OpenAI publique los nombres específicos de configuración y los números completos, ya que esos determinarán qué tan directamente cualquiera puede replicar el resultado en producción.

[06:01] Liquid AI lanza dos codificadores de contexto largo amigables con CPU

Liquid AI lanzó dos modelos codificadores de peso abierto en su línea LFM2.5, con tamaños de 230 millones y 350 millones de parámetros, ambos apuntando al trabajo de contexto largo directamente en CPUs. Cada uno lleva una ventana de contexto de 8,192 tokens, inusualmente generosa para un codificador dirigido a CPU y el número principal para cualquiera que evalúe pipelines locales.

El gancho técnico es una receta de conversión. Liquid AI tomó los troncos de decodificador causal y los reconstruyó como codificadores bidireccionales, intercambiando la atención unidireccional por atención completamente bidireccional, reemplazando convoluciones cortas causales por unas simétricas no causales, y reentrenando con un objetivo de lenguaje enmascarado. Esa combinación permite que los modelos realmente usen la ventana completa de 8,192 tokens.

Liquid AI informa que el modelo de 230 millones de parámetros completa un paso hacia adelante de 8,192 tokens en CPU en aproximadamente 28 segundos, lo cual dice es aproximadamente 3.7 veces más rápido que ModernBERT-base en su propia comparación. Esos números son resultados del proveedor, por lo que la velocidad en el mundo real dependerá del hardware en el que implementes, pero la dirección es clara: las entradas largas en CPUs de consumo ahora son un objetivo declarado.

La empresa posiciona el par para clasificación, enrutamiento, revisión de políticas y detección de datos personales. Esos son exactamente los trabajos donde ejecutar completamente en local, sin enviar texto a un modelo alojado, importa más, desde el enrutamiento de tickets de soporte hasta el marcado de campos sensibles antes del almacenamiento. Con pesos abiertos, los constructores pueden ajustar fino con sus propias etiquetas e implementar el resultado en una sola máquina.

El lanzamiento llegó el 28 de julio de 2026 en Hugging Face. Lo siguiente que vale la pena vigilar es si los benchmarks independientes confirman la historia de velocidad en CPU en hardware fuera del entorno de prueba de Liquid AI.

[07:35] ComfyUI 0.29.0 transmite video en lugar de almacenarlo en búfer en RAM

ComfyUI, la interfaz de código abierto basada en nodos para ejecutar flujos de trabajo locales de generación de imágenes y video, lanzó la versión 0.29.0 el 29 de julio. El lanzamiento es pequeño pero enfocado en dos puntos de dolor específicos.

El cambio más concreto es en la tubería de video. Hasta ahora, la transcodificación de video en ComfyUI almacenaba en búfer cada fotograma en RAM antes de procesar. Eso funciona para clips cortos, pero una renderización larga o de alta resolución puede agotar la memoria y morir a mitad del trabajo. El nuevo comportamiento transmite la transcodificación en su lugar, por lo que los fotogramas fluyen sin acumularse en RAM.

El segundo cambio llega al sistema de nodos asociados. ComfyUI ahora envía su ID de trabajo como encabezado de solicitud a los servicios asociados. Para cualquier persona que integre un nodo asociado de terceros en un flujo de trabajo, ese encabezado le da al asociado una forma limpia de correlacionar el trabajo entrante con el trabajo de ComfyUI de origen, en lugar de adivinar a partir de nombres de archivos o tiempos.

Juntos, estos son arreglos de fontanería en lugar de nuevas características, pero ambos abordan frustraciones reales: bloqueos por falta de memoria en renderizaciones de video largas, y atribución poco clara cuando un flujo de trabajo se ramifica a servicios externos. Vale la pena actualizar si alguno de estos te ha afectado.

[08:43] NVIDIA Jetson Obtiene el Respaldo de una Capitalista de Riesgo

La plataforma de IA en el borde de NVIDIA, Jetson, recibió un respaldo de un promotor inusual esta semana: la capitalista de riesgo Sarah Guo. En un video publicado el 28 de julio de 2026, Guo —fundadora de la firma enfocada en IA Conviction y copresentadora del podcast No Priors— presentó Jetson como el accesorio imprescindible de la temporada para los constructores. El blog de NVIDIApickup el clip con el título "Potente Computación Tan Compacta, Es Práctica."

El marco importa porque la IA en el borde es donde se dirige mucho trabajo práctico. Los robots, drones, quioscos y equipos de inspección no siempre pueden esperar una ida y vuelta a un servidor en la nube. Jetson es la computadora compacta y autocontenida de NVIDIA construida alrededor de sus aceleradores estilo GPU —lo suficientemente pequeña para caber en una bolsa, con suficiente potencia para ejecutar modelos modernos de IA localmente en lugar de a través de una red.

Para los constructores, el atractivo es directo: puedes prototipar un modelo en una caja Jetson sin reservar tiempo en la nube, y mantener una forma de hardware similar mientras te mueves del escritorio al despliegue. La compensación es la restricción habitual del borde —estás trabajando dentro del techo de memoria y cómputo de una máquina pequeña, por lo que el tamaño del modelo y la eficiencia importan más de lo que lo harían en un clúster de servidores.

La advertencia honesta: esta es una publicación promocional construida alrededor del video de una VC, no un lanzamiento de producto. El blog de NVIDIA no ofrece registro de cambios, no hay nueva SKU, ni especificaciones actualizadas. Así que la conclusión es un recordatorio de que Jetson existe y se mantiene pequeño —vale la pena vigilar cualquier actualización real de silicio o kit de desarrollador que convierta el argumento de "práctico" en algo concreto para ordenar.

[10:21] El Empaque Avanzado de Fabricación Estadounidense de Intel Permite Semiconductores de IA de Próxima Generación

A medida que la IA exige una "potencia cerebral" sin precedentes, la industria de semiconductores está superando la era de depender de chips masivos individuales. El empaque avanzado es la habilidad esencial de interconectar múltiples chips especializados juntos. Esto les permite funcionar como una sola unidad poderosa que funciona más rápido manejando las cargas de trabajo masivas del futuro.Intel ha estado haciendo empaque avanzado... La publicación El Empaque Avanzado de Fabricación Estadounidense de Intel Permite Semiconductores de IA de Próxima Generación apareció primero en Newsroom. La fuente principal respalda el cambio específico de producto o flujo de trabajo anterior; no respalda afirmaciones más amplias sobre rendimiento, compatibilidad o implementación. Prueba el cambio de origen contra un flujo de trabajo real antes de depender de él.

[11:00] La FCC Agrega Robots Avanzados de Fabricación Extranjera a Su Lista Cubierta

El 28 de julio, la Oficina de Seguridad Pública y Seguridad Nacional de la FCC agregó dispositivos robóticos avanzados de producción extranjera a la Lista Cubierta, el registro del regulador de equipos que no pueden recibir autorización de la FCC para usar el espectro de radio de EE.UU. El movimiento siguió una determinación interinstitucional de la Rama Ejecutiva que señaló cuatro categorías de riesgo: integridad de la cadena de suministro, ciberseguridad, potencial de vigilancia y vulnerabilidades de control remoto.

El efecto práctico es una barrera dura. Cualquier robot avanzado producido fuera de los Estados Unidos no puede ser autorizado para venta u operación en los EE.UU. a través del proceso normal de la FCC. Hay una salida de escape: el Departamento de Guerra puede otorgar aprobación condicional para un dispositivo o clase de dispositivo específico si se determina que no presenta esos riesgos. Así que esto no es un embargo general. Es una presunción contra la producción extranjera, con una ruta de exención adjunta.

Es importante que la acción de la FCC se basa en categorías, no en empresas. La regla mira dónde se fabricó el dispositivo, no qué empresa lo fabricó. Esa distinción importa porque las subsidiarias estadounidenses de fabricantes extranjeros de robots, o las marcas estadounidenses que subcontratan la producción al extranjero, ambas pueden verse afectadas dependiendo de dónde ocurre realmente el ensamblaje.

Para constructores e importadores, la pregunta abierta es el alcance. El aviso público no determina qué cuenta como un "dispositivo robótico avanzado", por lo que las próximas semanas de orientación del Departamento de Guerra y cualquier aclaración de la FCC determinarán si esto se establece como una regla estrecha para robots industriales o si abarca hardware de consumo e investigación. Las primeras aprobaciones condicionales serán la señal más clara de dónde cae realmente la línea.

[12:35] Resumen de investigación: Entrenamiento de robots sin el robot: Una mejor captura podría reemplazar el ancla de hardware real

Los robots que pueden doblar ropa o clasificar objetos generalmente necesitan miles de demostraciones cuidadosas recopiladas en hardware real, lo cual es lento y costoso. Una alternativa más barata es UMI, un sistema portátil que captura el mismo tipo de datos de movimiento sin necesidad del robot en sí, pero las imágenes son más ruidosas y menos confiables. La práctica estándar actual es usar esos datos baratos de UMI para pre-entrenar una política y luego agregar una pequeña dosis de demostraciones con robot real como paso final. Un nuevo artículo llamado HiFi-UMI plantea una pregunta más precisa: ¿qué pasaría si la captura sin robot fuera simplemente más fiel, para que el ancla de robot real pudiera desaparecer por completo? Los autores presentan HiFi-UMI como un sistema de captura portátil diseñado para mayor fidelidad, con políticas entrenadas de extremo a extremo solo con esos datos. La propuesta implícita es que la restricción limitante en el aprendizaje de manipulación no es cuántas demostraciones recopilas, sino qué tan confiable es cada una. Si la afirmación se sostiene, los laboratorios sin grandes flotas de robots reales obtienen una rampa de entrada mucho más barata hacia la manipulación desplegable.

[13:38] Resumen de investigación: El documento TurboVLA reduce el cómputo de control de robots a menos de 1 GB

TurboVLA, un artículo trending en HuggingFace esta semana, rediseña cómo los robots convierten vistas de cámara e instrucciones habladas en movimiento. Los modelos de visión-lenguaje-acción — sistemas de IA que observan su entorno, analizan un comando y se mueven — generalmente pasan cada cuadro visual a través de un modelo de lenguaje grande primero. Ese paso les da capacidad de razonamiento, pero también consume memoria y agrega latencia en cada tic del robot. TurboVLA toma un camino diferente. En lugar de ejecutar la visión a través de un modelo de lenguaje grande antes de producir acciones, fusiona señales de visión y lenguaje directamente en la salida de acción. Los números principales son sorprendentes: el sistema funciona a 32 actualizaciones por segundo en una sola tarjeta gráfica de consumo RTX 4090, mientras usa menos de un gigabyte de memoria de video. Eso es un desbloqueo significativo para aficionados, estudiantes y pequeños laboratorios — el tipo de configuración que cabe en un escritorio en lugar de llenar un rack de servidores. La pega es que las demostraciones del artículo son limitadas; si el atajo se mantiene en tareas del mundo real más caóticas y menos guionizadas es lo siguiente a observar.

[14:43] HKUDS lanza nanobot v0.3.0 como un framework de agentes autohospedados ligero

HKUDS ha publicado nanobot v0.3.0, un framework de Python dirigido a desarrolladores que quieren ejecutar su propia configuración de agente de IA en lugar de depender de una plataforma alojada. El proyecto se describe como ultraligero y autohospedado, y ha acumulado 46,404 estrellas en GitHub.

El lanzamiento salió el 25 de julio, con el repositorio actualizado cinco días después el 30 de julio. No hay un changelog público para v0.3.0 en el material de origen, por lo que la forma práctica de ver qué cambió es el repositorio mismo y su historial de commits.

Lo que nanobot incluye, según su README: una WebUI para hablar con el agente, una capa de herramientas para llamar funciones externas, un componente de memoria, soporte para MCP para que pueda conectarse al ecosistema del Model Context Protocol, primitivas de flujo de trabajo multiagente, hooks de automatización e integraciones con aplicaciones de chat. La propuesta es que todo esto viene en un único paquete de Python que puedes ejecutar en tu propio hardware.

Para constructores, eso significa un camino autohospedado que ya habla MCP, para que puedas adjuntar herramientas y fuentes de datos a través del mismo protocolo que usan muchos agentes alojados. Las integraciones con aplicaciones de chat y la WebUI te dan una capa de interfaz sin construir una desde cero.

Una cosa a observar: sin un changelog de v0.3.0, los cambios reales del lanzamiento versus versiones anteriores están en el historial de commits, y el ritmo del proyecto — una actualización fresca cinco días después del lanzamiento — sugiere un desarrollo activo que vale la pena seguir en GitHub.

[16:12] GPT-5.6 se presenta como un lanzamiento de eficiencia, no de capacidades

OpenAI publicó el 29 de julio de 2026 presentando GPT-5.6 en torno a la eficiencia en lugar de ganancias de capacidades brutas. La publicación presenta GPT-5.6 como algo que ofrece más inteligencia útil por dólar a través de mejoras que abarcan los modelos mismos, la pila de inferencia y los flujos de trabajo de agentes.

Ese es el fondo del anuncio. No hay changelog adjunto, no hay lista específica de características, no hay tablas de benchmarks y ningún detalle concreto de API o precios en el material de origen.

Para constructores, eso significa que esto es lenguaje de posicionamiento en lugar de un lanzamiento de características. No hay nada que integrar hoy y nada contra lo que volver a probar hasta que OpenAI publique las notas de lanzamiento concretas, los precios y el cronograma. Cualquiera que esté desplegando agentes de producción en la generación anterior debe estar atento a los números de costo y rendimiento una vez que aparezcan, ya que el posicionamiento es explícitamente sobre obtener más salida útil por dólar.

El titular aquí es eficiencia, no nueva capacidad. Hay que esperar los números reales.

[17:10] OpenAI concede acceso gratuito a ChatGPT a 100,000 investigadores académicos

OpenAI anunció el 29 de julio de 2026 que está dando a 100,000 investigadores académicos acceso gratuito a los modelos de IA más avanzados de ChatGPT. El programa se presenta en torno a acelerar la investigación científica, la colaboración y el descubrimiento.

El anuncio no nombra los modelos específicos incluidos, no describe los criterios de elegibilidad ni explica cómo se distribuirán los 100,000 espacios. No hay changelog, no hay detalle de precios y no hay cronograma para cuándo comienza el acceso o cuánto dura. El material de origen es la página única del anuncio, que solo confirma el número del titular, la audiencia y el objetivo declarado.

Lo que esto señala es que OpenAI continúa invirtiendo en casos de uso cercanos a la investigación. El acceso gratuito de nivel superior para una gran cohorte de académicos es el tipo de movimiento que puede dar forma a qué herramientas eligen los estudiantes de posgrado, postdocs y profesores cuando redactan artículos, sintetizan literatura o generan hipótesis. Si esto cambia materialmente los flujos de trabajo de investigación dependerá de los detalles que el anuncio aún no proporciona.

La cifra de 100,000 es lo suficientemente grande como para ser relevante, aproximadamente del tamaño del cuerpo docente y de estudiantes de posgrado combinados de una importante universidad de investigación. Si el acceso funciona como se anuncia, espere un flujo constante de artículos que crediten a ChatGPT como asistente de investigación durante el próximo año. Por ahora, el titular es la historia; los detalles técnicos aún están pendientes.

[18:30] La plataforma OlmoEarth lleva la inferencia geoespacial a escala planetaria

AllenAI publicó una entrada en el blog de Hugging Face el 28 de julio de 2026, titulada "The OlmoEarth Platform: Geospatial inference at planetary scale." Ese es el titular. Presenta a OlmoEarth como una plataforma en lugar de un modelo único, con la inferencia geoespacial como capacidad central y la escala planetaria como objetivo operativo.

Al leer cuidadosamente el título, "inferencia geoespacial" significa que el sistema está diseñado para procesar datos geográficos y de teledetección y generar predicciones sobre ellos, mientras que "escala planetaria" indica que el pipeline de datos y computación subyacente está dimensionado para cubrir toda la Tierra, en lugar de una sola ciudad, cuenca hidrográfica o mosaico satelital. Para los constructores, ese enfoque importa porque la parte difícil de la IA geoespacial rara vez ha sido el modelo; ha sido la ingestión, división en mosaicos y entrega de entradas raster y vectoriales del tamaño de un continente en todo momento.

Más allá del titular y la fecha de publicación, la fuente pública no incluye un registro de cambios, una tarjeta de modelo ni notas de versión concretas. No hay ninguna variante de modelo listada, ninguna superficie de API documentada, ningún formato de entrada declarado y ningún precio o nivel de acceso anunciado en el material disponible aquí. Entonces, aunque el nombre y la ambición ahora están registrados, la pregunta práctica de qué puede llamar, instalar o ajustar un desarrollador hoy sigue abierta tras el anuncio de AllenAI.

Una cosa a observar a continuación: si AllenAI complementa la publicación del blog con pesos del modelo, un punto de conexión para inferencia o cuadernos de ejemplo que conviertan "escala planetaria" de una frase en algo que un constructor pueda ejecutar realmente contra su propia región de interés.