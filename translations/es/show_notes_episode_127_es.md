Episodio 127 — 05 de noviembre de 2026

[00:00] Gancho del episodio

OpenAI corrigió 948 vulnerabilidades del kernel de Linux después de construir una tubería autónoma que encontró, validó y generó soluciones para fallas de escalada de privilegios locales. Cada problema podría permitir que un atacante local obtuviera privilegios elevados, y el trabajo comprime el descubrimiento, la validación y la generación de parches en un sistema automatizado. Astra demostró un LLM de vanguardia inspeccionando y editando directamente los pesos de redes neuronales a través de instrucciones en lenguaje natural, sin un bucle de entrenamiento personalizado o descenso de gradiente; el experimento Qwen3.5-0.8B del equipo apunta hacia una forma diferente de modificar el comportamiento del modelo. OpenAI también lanzó Images 2.6 con generación más rápida, creación de GIF, edición más precisa y nuevos controles de API en ChatGPT, Codex y la API. Hermes Agent 0.22.7 añade mejoras en la colaboración, la programación y el control en la CLI, la aplicación web, Desktop, Docker y Hermes Cloud. Ripple-65B de Ricursive Intelligence, de peso abierto, aporta llamada de herramientas nativa, una ventana de contexto de 1,048,576 tokens y codificación agéntica diseñada para uso local, con una puntuación reportada de TerminalBench 2.1 de 80.52.

[02:00] Informe de Lanzamiento de Agent Stack: Hermes Agent v0.22.7, v0.22.6

Nous Research lanzó Hermes Agent v0.22.6 el 2 de noviembre de 2026, seguido de v0.22.7 el 3 de noviembre. Juntos, los lanzamientos expanden sustancialmente cómo las personas pueden organizar el trabajo compartido del agente, programar su salida y controlar lo que puede hacer.

Hermes Agent v0.22.6 añade una aplicación web servida directamente por la puerta de enlace. La CLI puede abrirla, y los usuarios de Desktop pueden acceder a ella a través de un panel de Acceso Web en su red o detrás de un inicio de sesión de Nous. Los plugins de Desktop también pueden cargarse dentro de una pestaña del navegador. El lanzamiento añade renombrado de chats grupales, disolución, menciones y pegado de archivos adjuntos; cada perfil puede aparecer como una sección en la barra lateral de Desktop.

Las herramientas de programación también se vuelven más manejables. Los usuarios pueden cancelar tareas cron, elegir cómo responde una tarea después de una ejecución perdida y detener una tarea desde el editor cron de Desktop. Hermes Agent v0.22.7 permite entonces que las tareas cron publiquen en los Chats Grupales. Ese mismo lanzamiento añade enrutamiento de leads opcional para Chats Grupales de Desktop, una insignia de Lead, propósitos de sala, notas compartidas, un diseño de grupo de una sola columna que muestra el estado en vivo de cada miembro y tableros Kanban anclados disponibles como pestañas de cambio rápido.

Dos salvaguardas se destacan para los desarrolladores. Los bloqueos por habilidad pueden impedir que un agente realice escrituras autónomas en una habilidad seleccionada, y un gancho de pre-inferencia puede bloquear un turno antes de que se llame al modelo. El modelo anclado de una sesión también puede restablecerse sin eliminar su historial.

El siguiente detalle a observar es v0.23.0, donde Hermes planea publicar notas curadas que cubran estas áreas de características y el historial completo de cambios desde la v0.22.0 en adelante.

[02:53] Ripple-65B de RicursiveAI llega a OpenRouter

OpenRouter lista Ripple-65B-Preview, un modelo de 65B de RicursiveAI con llamada de herramientas nativa, servido en BF16. La llamada de herramientas permite que un modelo solicite que un programa invoque una función específica, haciendo que el modelo sea relevante para flujos de trabajo que combinan documentos grandes con acciones externas. El registro lista una longitud de contexto de 1,048,576 tokens y una arquitectura de texto a texto. El precio listado de OpenRouter es de $0.0000002 por token de solicitud (prompt), $0.0000006 por token de completado y $0.00000005 por token de entrada de lectura de caché. Eso da a los desarrolladores un candidato concreto para aplicaciones de contexto largo que necesitan el uso de herramientas. La ventana de un millón de tokens es la capacidad principal, mientras que el precio del registro proporciona una base sencilla para estimar los costos de uso. El modelo listado acepta texto y produce texto, con una longitud de contexto de 1,048,576 tokens. El modelo está disponible a través de su listado en OpenRouter.

[03:42] Astra Edita Directamente los Pesos de Redes Neuronales

El equipo informa que GPT-6 Astra puede inspeccionar los pesos brutos de redes neuronales, inferir lo que una red ha aprendido y editar pesos seleccionados directamente utilizando razonamiento en lenguaje natural en lugar de un bucle de entrenamiento. En su experimento Qwen3.5-0.8B, Astra identificó un problema en los pesos que causaba bucles de razonamiento, luego cambió el 0.016% de ellos. Con las mismas configuraciones de muestreo, la corrección elevó la precisión de MATH-500 del 7.9% al 48.1% y triplicó el rendimiento de seguimiento de instrucciones de IFEval.

El equipo llama a esto Weight-Space Programming, un método donde un LLM de propósito general trata los pesos como artefactos numéricos editables y razona sobre lo que cada parte calcula. Esto podría apoyar la reparación de modelos sin la optimización convencional basada en gradiente y podría extender ideas sobre el comportamiento del modelo que pueden inferirse solo a partir de los parámetros. Los resultados son explícitamente preliminares, por lo que lo siguiente a observar es si las ediciones dirigidas pueden mejorar consistentemente los modelos reales más allá de los ejemplos reportados.

[04:35] OpenAI encontró y corrigió 948 vulnerabilidades del kernel de Linux

OpenAI ha construido una tubería autónoma para encontrar y solucionar fallas graves del kernel de Linux. Encontró, validó y generó parches para 948 vulnerabilidades de escalada de privilegios locales, lo que significa defectos que pueden permitir que alguien con acceso limitado obtenga privilegios más altos en la misma máquina.

El cambio concreto es el tamaño de la cola de soluciones candidatas. En lugar de dejar que los equipos del kernel descubran y reparen cada problema individualmente, la tubería produce 948 casos de vulnerabilidad validados con parches generados que los mantenedores pueden revisar. OpenAI es la organización detrás de la tubería, y los equipos de seguridad del kernel de Linux son la audiencia obvia para su producción.

Lo siguiente a observar es si estos parches generados pasan la revisión de expertos y se convierten en soluciones aceptadas en Linux.

[05:18] OpenAI Lanza Imágenes Más Rápidas, GIFs y Edición Más Precisa

OpenAI lanzó Images 2.6 el 4 de noviembre, haciendo la generación de imágenes más rápida al tiempo que añade dos capacidades creativas visibles: la creación de GIF y una edición más precisa.

La actualización está disponible en ChatGPT, Codex y la API. Esto brinda a las personas una ruta interactiva para crear y refinar elementos visuales, así como una ruta de API para integrar esas capacidades en las aplicaciones.

Para los desarrolladores, la oportunidad concreta es añadir la generación de imágenes, la creación de GIF o la edición precisa a productos y flujos de trabajo. OpenAI también ha introducido nuevos controles de API, ampliando lo que los desarrolladores pueden configurar al construir con el modelo. Lo siguiente a observar es cómo se desempeñan esos controles en tareas reales de edición de imágenes y generación de GIF.

[05:59] Ripple-65B lleva la codificación agéntica de peso abierto a las máquinas locales

Ricursive Intelligence ha lanzado Ripple-65B Preview, un modelo de propósito general y de peso abierto que, según la compañía, establece un liderazgo de peso abierto en EE. UU. para la codificación agéntica. Obtuvo una puntuación de 80.52 en TerminalBench 2.1, superando a Reflection Beam 501B, Meta Muse Spark Open 816B, Thinking Machines Inkling 975B y NVIDIA Nemotron 3 Ultra 550B.

El modelo fue preentrenado con 12 billones de tokens y admite longitudes de contexto de hasta un millón de tokens. Ricursive diseñó su arquitectura densa para un entrenamiento y servicio eficientes en hardware NVIDIA, con el objetivo de permitir una operación local robusta en sistemas como NVIDIA DGX Spark. Está disponible en Hugging Face, Together AI, GMI Cloud y OpenRouter, con el lanzamiento de Fireworks programado para más tarde ese mismo día.

Ricursive informa que el costo total de investigación y desarrollo de Ripple, incluyendo el trabajo de datos, la evaluación, la depuración y el post-entrenamiento, fue de $32 millones. Para mejorar la eficiencia de la codificación, la empresa probó cambios arquitectónicos en escalas de modelos más pequeñas antes de ampliarlos, y construyó sus propios canales de datos sintéticos en lugar de comprar datos de post-entrenamiento. Lo siguiente a observar es cómo se desempeña el modelo fuera de la evaluación de codificación agéntica de Ricursive a medida que el desarrollo continúa hacia modelos de mayor escala.

[07:08] ComfyUI lanza nodos de textura y doblaje

ComfyUI lanzó su versión estable v0.44.0 el 4 de noviembre de 2026, con nuevos bloques de construcción creativos para flujos de trabajo. La versión añade Nodos Asociados para el trabajo de textura Patina y el doblaje VEED, ambos aportados por bigcat88.

Para las personas que construyen con ComfyUI, las adiciones proporcionan nuevas formas basadas en nodos para incorporar la creación de texturas y el doblaje en un flujo de trabajo. La versión también actualiza las plantillas de flujo de trabajo de ComfyUI a v0.11.98, ofreciendo a los desarrolladores una colección renovada de puntos de partida para flujos de trabajo.

El cambio restante es de mantenimiento interno: el proyecto cambió la versión de Python de pylint a 3.1. El enfoque de esta versión, orientado al creador, es el par de Nodos Asociados, por lo que la próxima evidencia útil provendrá de flujos de trabajo completos que muestren cómo funcionan juntas las etapas de textura y doblaje.

[07:52] Los votantes imponen nuevas restricciones a los centros de datos de IA

Los votantes estadounidenses rechazaron o restringieron los centros de datos en más de 30 localidades de nueve estados. Las medidas incluyeron moratorias, prohibiciones totales y restricciones financieras u operativas para los hiperescaladores que buscaban exenciones fiscales, con algunos votos respondiendo directamente a proyectos ya en marcha.

Los resultados fueron especialmente claros en Edgewater, Florida, donde los residentes apoyaron masivamente la inclusión de una prohibición de centros de datos en la carta de la ciudad. En Perry, Ohio, los votantes aprobaron una medida que impone restricciones financieras y operativas a los hiperescaladores que buscan exenciones fiscales.

La presión política se está ampliando más allá de las medidas locales en las urnas. Los demócratas que se postularon en más de 130 contiendas federales y gubernatoriales utilizaron publicidad anti-tecnología o anti-centros de datos, según un análisis. El gobernador de Texas, Greg Abbott, quien recientemente promovía la IA y la expansión de centros de datos, prometió una regulación más estricta pero perdió sus elecciones.

Esa oposición ya está afectando al capital. Los bancos y gestores de activos que financian centros de datos han empezado a tratar la resistencia local como un riesgo crediticio, mientras que los hiperescaladores están contratando enlaces comunitarios. Algunas empresas también están intentando describir sus instalaciones como “compute campuses”, aunque el cambio de marca ha tenido resultados mixtos.

La próxima prueba será si estas restricciones locales cambian dónde se construye nueva infraestructura de IA, qué proyectos pueden asegurar financiación e incentivos, y cómo responden los operadores cuando las comunidades exigen más que solo una marca.

[09:08] SambaNova y Supermicro planean sistemas de inferencia de IA con chips mixtos

SambaNova y Supermicro han anunciado una colaboración estratégica para construir y vender sistemas de inferencia de IA que combinan RDUs y GPUs. Supermicro está planeando inicialmente 10,000 chips SN50 RDU para este esfuerzo.

SambaNova dice que la asociación tiene como objetivo abordar la IA agéntica, y el cofundador Rodrigo Liang la califica como “la próxima ola de inferencia” que debe ejecutarse en todas partes. La propuesta concreta es una arquitectura de sistema mixto en lugar de un único tipo de procesador, uniendo los chips RDU de SambaNova con las GPUs.

Para los desarrolladores, el desarrollo importante es la combinación de un socio de fabricación nombrado, una categoría de producto y un objetivo inicial de volumen de chips. Lo siguiente a observar es si los 10,000 chips SN50 planificados se integran en los sistemas de inferencia disponibles.

[09:52] OpenAI vincula nuevos campus de cómputo a la fiabilidad de la red eléctrica

El 2 de noviembre, OpenAI presentó el Grid Protectors Program, que trabajará con las empresas de servicios públicos para ayudar a los futuros campus de cómputo a apoyar la fiabilidad de la red eléctrica y proteger los costos de electricidad de los consumidores.

La iniciativa aborda ambas caras del crecimiento de la infraestructura de AI: las necesidades de las grandes instalaciones de cómputo y su efecto en los clientes de electricidad que las sustentan. OpenAI está posicionando el programa en torno al trabajo directo con las empresas de servicios públicos, en lugar de presentar nueva tecnología de cómputo o un lanzamiento de software.

Para las organizaciones que desarrollan servicios de AI, la implicación práctica es que el acceso a la energía, la fiabilidad de la red y los costos para el consumidor son parte de la planificación de la implementación, no preocupaciones separadas. El detalle a observar es qué empresas de servicios públicos y futuros campus participan y qué protecciones resultan de esos acuerdos.

[10:36] Resumen de investigación: La IA de laboratorio comprende los procedimientos pero aún pasa por alto los detalles físicos

Los modelos actuales de AI pueden seguir los pasos generales de un procedimiento de laboratorio mostrado en video, pero todavía tienen dificultades con los detalles físicos requeridos para ejecutar esos pasos. El BEAKER benchmark evalúa si los modelos pueden conectar una acción prevista con la parte correcta de un objeto y una trayectoria de movimiento factible a través de un laboratorio.

Los autores seleccionaron manualmente preguntas que cubren el reconocimiento de equipos y del estado experimental, seguridad, configuración de aparatos, operación, orden de procedimiento y razonamiento a partir de imágenes y video. Los modelos actuales tuvieron un mejor desempeño en los pasos procedimentales generales que en las tareas que requieren que las acciones se basen en regiones operables y trayectorias factibles —una trayectoria que describe cómo una máquina puede moverse o actuar.

Esto es importante porque un laboratorio químico autónomo no solo debe entender qué experimento está en curso, sino también percibir la escena, respetar las restricciones procedimentales y de seguridad, y elegir acciones que funcionen en el mundo físico. Por ejemplo, un sistema podría reconocer que una muestra necesita moverse, pero aun así no identificar qué se puede agarrar o cómo alcanzarla. BEAKER ofrece a los equipos de investigación una forma concreta de exponer y comparar esa brecha antes de que modelos similares sean confiados con el control del laboratorio.

[11:48] OpenAI construyó un backend de Git para el desarrollo a escala Codex

OpenAI ha construido Pando, un backend compatible con Git diseñado para la escala de desarrollo que Codex hace posible.

El cambio es importante porque aborda la capa de repositorio subyacente a la codificación asistida por AI. Git es el sistema que los desarrolladores usan para rastrear y gestionar los cambios de código, y Pando está diseñado para proporcionar un backend compatible para el desarrollo a escala impulsada por Codex.

La evidencia concreta en el anuncio de OpenAI es el alcance y la propiedad del sistema: OpenAI lo construyó, es compatible con Git, y el desarrollo impulsado por Codex establece su escala objetivo. Eso ofrece a los desarrolladores que evalúan entornos de desarrollo con uso intensivo de AI un patrón de infraestructura específico a considerar: un backend compatible con Git diseñado en torno a la carga de trabajo que Codex hace posible.

El rendimiento de Pando bajo cargas de repositorio reales es el siguiente punto a observar.

[12:32] OpenAI adquiere Pierre para expandir Codex

OpenAI anunció el 4 de noviembre que adquirirá Pierre Computer Company. La compañía dice que la adquisición expande las herramientas de Codex para la construcción, comprensión y revisión de código.

Eso le da al acuerdo un claro enfoque de producto: fortalecer las formas en que los desarrolladores crean software, inspeccionan bases de código existentes y evalúan código. OpenAI está utilizando una adquisición para ampliar el rol de Codex en todo el proceso de desarrollo de software, en lugar de presentar el anuncio como el lanzamiento de una característica independiente.

Para los desarrolladores, esto señala una inversión continua en Codex como un lugar para el trabajo de desarrollo práctico. Las capacidades más útiles a evaluar a medida que lleguen son la creación de código, la comprensión de código y la revisión de código.

[13:10] Together Compiler reoptimiza la inferencia a medida que cambia el tráfico

Together AI lanzó Together Compiler, un sistema impulsado por agentes que continúa reoptimizando la pasada hacia adelante de un modelo de inferencia a medida que cambia el tráfico. La pasada hacia adelante es el cómputo del modelo que produce su salida. Together AI informa que el compilador alcanzó hasta 2.6 veces los tokens por segundo de las mejores configuraciones de InferenceX, con el resultado logrado en menos de 24 horas por modelo.

Esto es importante porque los desarrolladores de inferencia ahora pueden evaluar un proceso de optimización que se adapta al tráfico que realmente atienden, en lugar de dejar una configuración ajustada sin cambios. El mecanismo útil es el bucle continuo impulsado por agentes; la evidencia concreta es la comparación de rendimiento reportada y el tiempo de optimización. Un aspecto a observar es si la ganancia reportada se extiende a diferentes modelos y patrones de tráfico.