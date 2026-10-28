Episodio 125 — 25 de octubre de 2026

[00:00] Gancho del episodio

Nous Research publicó Hermes Agent v0.22.5 el 22 de octubre de 2026,ammediendo 81 pull requests fusionados en una versión de corrección para la CLI y los instaladores, la aplicación de Microsoft Store, Docker y Hermes Cloud. Anthropic también abrió el código de sandbox-runtime, el sandbox a nivel de sistema operativo que hay detrás de Claude Code, que restringe el acceso a archivos y a la red para agentes de IA, servidores MCP y herramientas de línea de comandos. OpenRouter añadió Moonshot AI’s Kimi K3.1 Pro con una ventana de contexto de 1.048.576 tokens, mientras que OpenAI introdujo una Decisions API para incorporar la toma de decisiones a las aplicaciones, con énfasis en respuestas rápidas y resultados enfocados. Recursive prosiguió con Flint, un modelo de programación basado en texto y con licencia Apache 2.0, de mezcla de expertos y con 39.800 millones de parámetros totales, de los cuales aproximadamente 2.500 millones están activos por token. Mistral publicó Timestral-209M, un modelo fundacional de series temporales para pronóstico zero-shot, capaz de manejar una o varias series relacionadas e incorporate información externa.

[02:00] Agent Stack Release Readout: Hermes Agent v0.22.5, v0.22.4, v0.22.3

Hermes Agent v0.22.5, publicado por Nous Research el 22 de octubre de 2026, combina 81 pull requests fusionados y 30 issues cerrados, repartidos entre 231 commits que no son de fusión y 804 archivos modificados. Actualiza la CLI y los instaladores, la aplicación de Microsoft Store, Docker y Hermes Cloud.

El cambio más importante es la delegación enchufable. Hermes puede enrutar el trabajo a subagentes mediante mapas de modelos o perfiles, y la ruta seleccionada puede cambiar en cada sesión. Esto ofrece a los desarrolladores una forma de separar distintos modelos o perfiles según la tarea, sin tratar cada backend como parte de la aplicación principal.

El sistema de plugins también gana capacidades. Los plugins pueden exponer comandos slash con opciones seleccionables, marcar Hermes mediante el Model Context Protocol e importar agentes existentes. El flujo de configuración puede ofrecer un importador cuando detecta otro agente, mientras que Desktop incorpora la instalación de plugins con un clic, insignias de nivel y controles para anclar plugins arrastrándolos en su barra lateral.

La gestión de cuentas y sesiones también es más clara. El inicio de sesión ahora utiliza el inicio de sesión de dispositivo simple; los invitados del nivel gratuito pueden transferir su trabajo a una cuenta, y el resultado muestra quién ha iniciado sesión. Los conectores ofrecen la opción de iniciar sesión en lugar de abrir silenciosamente una sesión de invitado. Los planes con ventana de uso incorporan indicadores, tarjetas de límites y recuperación al cambiar de modelo.

Hermes Agent v0.23.0 es el próximo hito que conviene vigilar, ya que Nous Research afirma que contendrá las notas completas y seleccionadas de los cambios acumulados en estas versiones.

[02:35] OpenRouter incluye Kimi K3.1 Pro con una ventana de contexto de 1M tokens

OpenRouter ha incluido Kimi K3.1 Pro, que el registro describe como el modelo multimodal de razonamiento de pesos abiertos estrella de Moonshot AI y como un sucesor postentrenado de Kimi K3. Está diseñado para programación de largo alcance, por lo que ofrece un potencial ajuste especial con el trabajo de software prolongado y los repositorios de código extensos. Su característica más concreta es una ventana de contexto de 1.048.576 tokens. La arquitectura del registro indica que el modelo acepta texto, imágenes y video, y produce texto, de modo que los desarrolladores pueden introducir distintos tipos de material en el mismo prompt. Esto resulta relevante para flujos de trabajo en los que el código, las capturas de pantalla y el video deben fundamentar un mismo resultado. El registro de OpenRouter indica un precio por token de $0.000002 para los prompts, $0.00001 para las finalizaciones y $0.0000002 para las lecturas de entradas almacenadas en caché. La inclusión permite evaluar Kimi K3.1 Pro mediante OpenRouter, tomando como puntos inmediatos de análisis el tamaño del contexto, la entrada multimodal y el costo por token. Moonshot AI describe Kimi K3.1 Pro como un sucesor postentrenado de Kimi K3. Kimi K3.1 Pro acepta texto, imágenes y video, produce texto y tiene una ventana de contexto de 1M tokens. OpenRouter incluye Kimi K3.1 Pro en su registro de modelos.

[03:42] Anthropic abre su sandbox para agentes más allá de los contenedores

Anthropic publicó sandbox-runtime, o srt, como un sandbox de código abierto a nivel de sistema operativo para agentes de IA. El proyecto es el sandbox que hay detrás de Claude Code y admite agentes, servidores MCP y herramientas de línea de comandos sin necesidad de contenedores.

Su función principal es sencilla: restringir el acceso a archivos y a la red disponible para esas herramientas. En macOS utiliza Seatbelt, el mecanismo de aislamiento propio del sistema operativo; en Linux utiliza bubblewrap. Por lo tanto, el mismo enfoque está disponible en dos de los principales entornos de escritorio y servidor, sin obligar a los desarrolladores a contendizar cada agente o herramienta.

Para los desarrolladores, esto cambia la decisión de implementación al ejecutar código controlado por agentes. En lugar de recurrir a un contenedor, un desarrollador puede colocar un agente, un servidor de herramientas o una utilidad de línea de comandos dentro de un sandbox a nivel de sistema operativo, con acceso controlado a archivos y redes. Anthropic también está poniendo a disposición para su inspección y reutilización el enfoque de aislamiento utilizado detrás de Claude Code.

Lo siguiente que conviene observar es cómo combinan los desarrolladores estas restricciones de acceso con las herramientas y los datos específicos que necesitan sus agentes en flujos de trabajo reales.

[04:44] OpenAI lanza una Decisions API para decisiones enfocadas en aplicaciones

OpenAI lanzó la Decisions API, que ofrece a los desarrolladores de aplicaciones una interfaz específica para realizar elecciones automatizadas. La empresa la describe como rápida, enfocada y de bajo costo, con aplicabilidad en distintos tipos de aplicaciones en lugar de.limitarse a un único caso de uso.

Esto es importante porque muchos productos necesitan tomar una decisión pequeña en un momento concreto: qué opción presentar, cómo enrutar una solicitud o qué acción debe realizar una aplicación. La API ofrece a los equipos otro componente que pueden poner a prueba en esos momentos, en lugar de tratar cada decisión como parte de un flujo de trabajo más amplio.

Para los desarrolladores, los siguientes puntos de comprobación son prácticos: con qué rapidez responde la API, si sus decisiones mantienen la coherencia con cargas de trabajo reales y cuánto cuestan esas decisiones al incorporarlas a un producto en funcionamiento.

[05:29] Recursive’s Flint lleva un agente de programación de 39.8B a entornos locales

Recursive lanzó Flint bajo la licencia Apache 2.0, y el repositorio de Unsloth ofrece su checkpoint, configuración del modelo, tokenizador, plantilla de chat y kit de servicio. Flint es un modelo de mezcla de expertos con entrada y salida de texto, diseñado para agentes de programación. Tiene 39.8 mil millones de parámetros en total, con aproximadamente 2.5 mil millones activos por token. Cada capa de mezcla de expertos contiene 256 expertos enrutados, de los cuales se seleccionan seis por token, además de un experto compartido siempre activo. Flint admite razonamiento, uso de herramientas en variasTurnos y llamadas a herramientas compatibles con OpenAI, para tareas como investigar bases de código, corregir errores, implementar funciones y escribir pruebas. Recursive informa un 54.9% en Terminal-Bench 2.1, un 89.7% en SWE-bench Pro v2 y un 74.2% en SWE-bench Verified. La ficha advierte que las configuraciones de evaluación varían, y que el resultado de Flint en Terminal-Bench cuenta como fallidas las soluciones obtenidas mediante recuperación web, mientras que algunas puntuaciones informadas por desarrolladores podrían no aplicar ese ajuste. Los pesos bajo Apache 2.0 están disponibles en el repositorio GGUF de Unsloth, con variantes cuantizadas preparadas para runtimes de NVIDIA y Apple Silicon. Los resultados pueden variar según la precisión del checkpoint y el runtime de inferencia, por lo que la configuración específica de despliegue es importante. Flint todavía puede generar código defectuoso o llamadas a herramientas inapropiadas, por lo que las aplicaciones necesitan sus propios permisos y límites de ejecución. Flint es un modelo de agente de programación basado en texto que admite razonamiento, uso de herramientas en varias turnos y llamadas a herramientas compatibles con OpenAI.

[06:45] Timestral-209M de Mistral permite la predicción probabilística local

Mistral lanzó Timestral-209M, un modelo fundacional de series temporales para hacer predicciones sin reentrenamiento específico para cada tarea. Es el más grande de cuatro tamaños documentados, que van de 5M a 209M parámetros, y el editor afirma que sus resultados de predicción zero-shot lideran en GIFT-Eval, TIME y fev-bench. El modelo puede predecir una sola serie o varias series relacionadas. También acepta entradas adicionales que ya se conocen o están programadas para el futuro, lo que puede ayudar a una aplicación a incorporar contexto más allá del historial objetivo. Su salida probabilística abarca 21 cuantiles, de modo que el software puede solicitar una predicción mediana junto con límites inferiores y superiores, en lugar de tratar una sola predicción como una certeza. Timestral acepta hasta 32,768 pasos temporales históricos y predice hasta 1,024 pasos en una sola pasada. Las predicciones más largas se realizan en bloques. Internamente, agrupa 32 pasos en cada patch e incorpora tanto los valores como los indicadores de observaciones faltantes. Para quienes desarrollan soluciones, el cambio importante es el despliegue local mediante PyTorch, ya sea en CPU o GPU. Mistral también afirma que está liberando el código fuente para ejecutar el modelo y reproducir sus resultados de benchmarks. Esto convierte a Timestral en un componente candidato para servicios locales y entornos de agentes que necesiten rangos de probabilidad, horizontes futuros o varias señales relacionadas, en lugar de una sola estimación puntual. Mistral liberó el checkpoint Timestral-209M y déclaré que estaba liberando el código fuente. Timestral admite predicciones univariadas y multivariadas, covariables del pasado y del futuro conocido, además de predicciones probabilísticas en 21 cuantiles. El editor informa que, en GIFT-Eval, Timestral-209M obtuvo errores MASE y CRPS menores que TimesFM-3. El checkpoint funciona mediante PyTorch en CPU o GPU, y los modelos se liberan bajo una licencia Modified MIT.

[08:26] OpenAI y el equipo de NASK de Polonia colaboran en seguridad de IA

OpenAI y NASK de Polonia anunciaron una alianza el 23 de octubre de 2026, centrada en la seguridad de la IA, la ciberseguridad y la investigación técnica. NASK de Polonia se une a OpenAI para fortalecer las salvaguardas y apoyar un ecosistema digital más resiliente.

No se trata del lanzamiento de un producto, sino de una colaboración entre una empresa de IA y la institución nacional de ciberseguridad de Polonia. Su relevancia inmediata es institucional: la investigación sobre seguridad de la IA y ciberseguridad ahora conecta directamente con una organización dedicada a la seguridad de la infraestructura digital de Polonia.

Para quienes desarrollan soluciones de IA, la señal útil que conviene observar es si la alianza produce salvaguardas concretas, métodos de seguridad o investigación técnica que los equipos puedan aplicar al proteger sistemas reales.

[09:06] Resumen de investigación: METTA permite que los agentes se adapten durante la tarea

METTA, un método de adaptación mejorado con memoria, ayuda a un agente de IA a aprender mientras ya está intentando completar una tarea, en lugar de depender únicamente de las lecciones aprendidas antes de comenzar. Esto importa para sistemas que deben manejar trabajos desconocidos con poca experiencia: pueden actualizar su comportamiento a partir de la interacción reciente y llevar un resumen compacto de episodios anteriores al siguiente intento. Los investigadores probaron el enfoque en tareas no vistas de Meta-World y tareas de PointMaze con contexto largo, donde la recompensa era escasa. En los entornos Meta-World reservados para evaluación, METTA superó una tasa de éxito del 50% y mantuvo bajos los costos de entrenamiento y el tiempo de reloj. En las tareas del laberinto, venció a las líneas base basadas en transformers y mostró una exploración más estructurada. La consecuencia práctica es que un agente puede adaptarse con un presupuesto de entrenamiento bajo y conservar suficiente historial para orientar intentos posteriores, en vez de reconstruir su comprensión desde cero cada vez. La siguiente pregunta es si ese equilibrio entre aprender durante una tarea y recordar entre distintas tareas se mantiene fuera de los entornos de benchmark.

[10:07] SpaceX Super Intelligence abre una red de socios de Grok

SpaceX Super Intelligence presentó un programa oficial para empresas que crean productos, soluciones y servicios con Grok, con el fin de compartir oportunidades y clientes. La SpaceX Super Intelligence Partner Network divide ese trabajo en Transformation Partners, que ayudan a los clientes a desplegar la plataforma Grok en toda la empresa, y Marketplace Partners, que desarrollan plugins e integraciones que conectan Grok con las herramientas que los clientes ya utilizan.

Más de 130 empresas participaron en la fase de acceso anticipado. Transformation Partners están creando capacidad de despliegue mediante un programa de acreditación de Forward Deployed Engineer, con ingenieros formados en más de 30 organizaciones. Marketplace Partners están trabajando en integraciones de productos para la suite de Grok.

Los socios de lanzamiento incluyen Bain & Company, Databricks, NVIDIA, Snowflake, Galatiq, Adapter Group, AHEAD y Alpha FMC. Sus funciones declaradas abarcan desde la transformación empresarial y la entrega hasta las plataformas de datos, la gobernanza, las trazas de auditoría y el contexto específico del negocio. Galatiq, por ejemplo, describe un modelo de entrega en el que los ingenieros definen el alcance y construyen sistemas de producción dentro de los flujos de trabajo de los clientes. Adapter describe la incorporación de la trayectoria completa de un cliente en Grok Bot y Grok Build, de modo que cada turno comience con un contexto más amplio de la misión y no solo con la memoria de trabajo.

Para quienes desarrollan soluciones, la oportunidad práctica es el trabajo conjunto que abarca despliegue, integraciones, datos empresariales y controles operativos. La siguiente prueba será hasta qué punto esas alianzas pasan de los pilotos a un uso recurrente en producción.

[11:27] Resumen de investigación: Un truco de entrenamiento reduce el consumo de memoria de la inferencia repetida de IA

Un nuevo método de post-training llamado BeNice! ayuda a una clase de modelos de IA que pasan información repetidamente por las mismas capas, manteniendo fija la cantidad de parámetros aprendidos. Durante la inferencia, cada pasada generaba antes su propia caché de clave-valor —la información almacenada de tokens anteriores—, por lo que el uso de memoria crecía linealmente con el número de repeticiones. BeNice! entrena al modelo para que la caché de la última pasada puedadiffundirse a la primera, haciendo que las pasadas repetidas sean compatibles con una caché compartida. Los investigadores informan que esto conserva la calidad del modelo y iguala el resultado del ajuste fino estándar con cachés separadas. El hallazgo importa porque las arquitecturas en bucle pueden mejorar la calidad sin agregar simplemente más parámetros, pero su demanda de memoria durante la inferencia había limitado esa ventaja. BeNice! ofrece una forma de conservar el beneficio en calidad a la vez que se evitan cachés duplicadas a lo largo de la profundidad. Los investigadores también découvert que el enfoque puede complementar otros métodos secuenciales que ahorran memoria, lo que sugiere que los equipos podrían combinarlo con técnicas de compresión existentes cuando la eficiencia de memoria sea lo más importante.

[12:27] DeusData lleva inteligencia de código local a los agentes de IA

DeusData publicó codebase-memory-mcp, un proyecto local de inteligencia de código para desarrolladores y agentes de IA. Su última versión es v0.12.1, fechada el 16 de octubre de 2026, y el repositorio recibió nuevos cambios el 24 de octubre. GitHub informa que el proyecto tiene 47,438 estrellas.

El repositorio conecta código, documentación e infraestructura en un grafo persistente. También incluye CBM Lens, herramientas MCP, integraciones con agentes y selección de pruebas consciente de los cambios. En conjunto, estas piezas buscan ayudar a los desarrolladores y agentes de IA a trabajar con una base de código como un cuerpo conectado de información, y no como archivos o instrucciones aisladas.

Para los desarrolladores, la oportunidad más útil es una capa de contexto local que pueda respaldar flujos de trabajo de agentes tanto en código como en documentación. La función de selección de pruebas también podría ayudar a los equipos a dedicar menos esfuerzo a ejecutar pruebas no relacionadas con un cambio. Algo que conviene observar en las próximas etapas es qué tan bien funcionan las integraciones con agentes y la selección consciente de los cambios en proyectos reales.

[13:21] Agensh de Microsoft coordina 1.024 agentes sin un jefe central

Microsoft Research ha puesto Agensh a código abierto, un entorno de múltiples agentes que puede ejecutar hasta 1.024 agentes en ProgramBench sin un orquestador central, es decir, sin un único controlador que asigne el trabajo.

El mecanismo útil es la coordinación compartida. Los trabajadores se autoorganizan mientras se comunican mediante un repositorio Git compartido, un canal de chat y un tablero de hallazgos. En el experimento reportado, Agensh escaló de un agente a 1.024, manteniendo un presupuesto de seis horas en ProgramBench.

Esto ofrece a los desarrolladores un marco de código abierto para explorar equipos grandes y cooperativas de agentes, y para estudiar cómo se coordinan mediante código compartido, conversación y hallazgos registrados. La cifra principal llama la atención, pero el espacio de trabajo compartido y los canales de comunicación son los componentes concretos que los equipos pueden adaptar.

La siguiente pregunta es cómo se comporta este enfoque en tareas fuera de ProgramBench y bajo cargas de trabajo diferentes de las del benchmark reportado.

[14:11] Cognition pone a código abierto un plugin de agente para corregir vulnerabilidades

Cognition ha puesto a código abierto el plugin Devin Vulnerability Fixes para ayudar a los equipos a responder a las vulnerabilidades críticas de ejecución remota de código de esta semana en PHP, Node.js y despliegues de GitLab autohospedados.

La versión incluye tres habilidades de agente con licencia MIT. Inventarían los sistemas afectados, los parchean y los prueban, y luego abren una pull request para cada repositorio. Esto transforma una respuesta amplia ante vulnerabilidades en cambios separados y revisables, en lugar de dejar que los equipos descubran y corrijan manualmente cada repositorio afectado.

El aspecto clave que conviene observar es si las pull requests generadas están listas para la revisión habitual de ingeniería una vez que el plugin haya completado el inventario, el parcheo y las pruebas.

[14:49] El tutorial de Letta construye copilotos de ingeniería con estado

MarkTechPost publicó una guía práctica para crear un copiloto de ingeniería con estado utilizing Letta. El objetivo es ampliar un asistente de IA más allá de la información contenida en su prompt inmediato, de modo que pueda trabajar con contexto persistente y conocimiento reutilizable del proyecto.

En el centro se encuentra una memoria central inspeccionable, que ofrece un lugar visible donde el copiloto puede conservar información. El tutorial también demuestra la recuperación vectorial de archivos: una forma de encontrar material anterior según su significado, sin necesidad de que coincida exactamente con la redacción buscada.

Para tareas más complejas, el copiloto puede utilizar herramientas personalizadas y compartir estado con varios agentes, lo que permite que agentes especializados se coordinen en torno al mismo contexto. También admite respuestas en streaming y flujos de trabajo portables que pueden trasladarse entre entornos.

Para los desarrolladores, el resultado útil es una arquitectura concreta para un asistente de ingeniería capaz de conservar el contexto del proyecto, recuperar información relevante, conectarse con acciones especializadas y mantener un flujo de trabajo reutilizable, en lugar de comenzar desde cero en cada sesión.