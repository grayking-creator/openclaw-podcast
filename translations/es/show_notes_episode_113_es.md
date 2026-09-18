Episodio 113 — 11 de septiembre de 2026

[00:00] Gancho del episodio

DeepSeek lanzó V4.1 Flash hoy, el primer modelo construido sobre su nueva arquitectura Causal Encoder-Decoder — un diseño de mezcla dispersa de expertos que activa 8 mil millones de parámetros por token mientras mantiene el cómputo de inferencia muy por debajo de modelos densos comparables. El lanzamiento viene con un informe técnico completo y pesos abiertos bajo una licencia permisiva, marcando el primer cambio arquitectónico de DeepSeek desde V3. El lanzamiento también llega la misma semana en que OpenAI afirmó que un modelo interno no lanzado resolvió el problema del Premio Millennium de Navier-Stokes, solo para que un matemático de NYU y un colaborador empleado en Anthropic afirmaran públicamente que llegaron al mismo resultado primero — una disputa de prioridad que ahora se extiende a foros abiertos y plantea nuevas preguntas sobre cómo se deben acreditar los avances matemáticos cuando el modelo detrás de la afirmación en sí no ha sido revelado.

[02:00] DeepSeek lanza V4.1 Flash sobre una nueva arquitectura

DeepSeek lanzó V4.1 Flash, un modelo de mezcla dispersa de expertos que es el primero construido sobre la nueva arquitectura Causal Encoder-Decoder (CED) de la empresa. El modelo enruta cada token a través de solo una porción de sus pesos — 8 mil millones de parámetros activos en la entrada, 16 mil millones en la salida — en lugar de ejecutar cada parámetro en cada pasada, que es el movimiento estándar de eficiencia del MoE. Cuenta con una ventana de contexto de un millón de tokens, lo suficientemente grande como para contener un libro largo o una base de código considerable en un solo prompt, y limita las respuestas generadas a 4,096 tokens por llamada. V4.1 Flash aparece en el proveedor propio de DeepSeek en OpenRouter, por lo que las integraciones existentes de OpenRouter pueden apuntar al nuevo id del modelo sin cambios en el SDK. La pregunta interesante para los desarrolladores es cómo CED difiere en la práctica de los diseños basados únicamente en transformers que DeepSeek lanzó antes — V4.1 Flash es el primer modelo sobre la nueva arquitectura, y cómo se desempeñe establecerá las expectativas para lo que se lance después sobre ella.

[02:09] La afirmación de Navier-Stokes de OpenAI se encuentra con una contraafirmación

OpenAI dice que ha resuelto el problema de existencia y suavidad de Navier-Stokes, uno de los siete desafíos del Premio Millennium de $1 millón que han estado abiertos desde mayo de 2000. El resultado fue producido por un modelo no lanzado cuyo nombre la empresa no ha revelado.

En pocos días, surgió una afirmación competitiva. Tristan Buckmaster, profesor de matemáticas en NYU, y Levent Alpöge, un matemático destacado ahora en Anthropic, publicaron un PDF describiendo su propio esfuerzo de casi un año en el mismo problema, realizado en gran medida a través de Claude y el producto Codex de OpenAI, especialmente el modelo GPT-5.6 Sol. Dicen que lograron su avance el 15 de agosto.

Lo que siguió fue una disputa pública sobre la procedencia. Buckmaster escribe que después de que el rumor matemático les informó, contactó a OpenAI y supo que la empresa tenía un equipo paralelo usando un enfoque similar. Cuando preguntó cuándo OpenAI envió su primer prompt, finalmente le dijeron que fue después de que las noticias de su trabajo llegaran a la empresa. Cuando preguntó si el entrenamiento del modelo había tocado sus sesiones de Codex — donde vivía cada borrador del proyecto — OpenAI dijo que el modelo no buscó datos de usuarios, pero no respondió la pregunta sobre el entrenamiento.

OpenAI ofreció esperar a que Buckmaster publicara o tenerle como coautor de su artículo. El episodio, resumido esta semana por el Weblog de Simon Willison, superó los 1,300 votos positivos en Hacker News.

Para matemáticos y desarrolladores, la pregunta abierta no es qué laboratorio cruzó la línea primero. Es si los modelos frontier ya podrían contener rastros de las sesiones de investigación privadas que los clientes creían que eran propias.

[03:46] La aplicación de IA personal Muse de Meta tiene un comienzo lento

La aplicación más nueva de Meta es Muse, presentada como un agente de IA personal — software que maneja tareas en tu nombre en lugar de solo responder preguntas en una ventana de chat. Según TechCrunch AI, el lanzamiento tiene un comienzo más lento que otros lanzamientos recientes de aplicaciones de Meta, incluyendo el asistente Meta AI y Threads. Esa comparación tiene peso porque Meta ha pasado los últimos años intentando posicionarse como una empresa de IA para consumidores creíble, y una aplicación de agente personal es exactamente la categoría hacia la que toda la industria ha estado corriendo.

El lanzamiento sí atrajo la atención de las personas que prestamos más atención a este espacio. Una discusión en Hacker News sobre la noticia subió a 655 puntos, lo que señala curiosidad genuina de una audiencia técnica aunque la tracción principal se ve más suave de lo que Meta probablemente quería. La aplicación en sí está en ai.meta.com/muse, lo que sugiere que Meta la está enmarcando como una extensión de su trabajo en IA en lugar de un producto social independiente.

Para desarrolladores y observadores de IA, el movimiento es marcar y esperar. Las preguntas interesantes son si Meta trata a Muse como una verdadera jugada de plataforma con ganchos profundos en Facebook, Instagram y WhatsApp, o como otra barra lateral experimental. Vale la pena revisarla en unas semanas una vez que los revisores independientes la hayan usado realmente y la curva de adopción temprana se vuelva más clara.

[05:09] Raschka de Ahead of AI disecciona el razonamiento de GPT-6 Astra

El newsletter Ahead of AI de Sebastian Raschka publicó un análisis detallado del GPT-6 Astra de OpenAI, y el artículo rápidamente subió a 512 puntos en Hacker News. Astra es el modelo más capaz de OpenAI dirigido a clientes empresariales, y Raschka se enfoca en dos ideas técnicas que los profesionales siguen preguntando: transformers en bucle y razonamiento oculto.

El artículo cae en el vacío entre el posicionamiento de OpenAI y lo que los ingenieros realmente quieren saber sobre un nuevo modelo. Raschka presenta a Astra como un sistema con razonamiento avanzado, capacidades de uso de computadora, y mejor juicio de escritura y diseño, luego recorre los conceptos arquitectónicos que pueden explicar por qué se comporta de manera diferente a los lanzamientos anteriores de GPT. Ese encuadre importa porque 'razonamiento' y 'uso de computadora' son exactamente las características que se pedirá a los equipos evaluar.

Para los desarrolladores, el valor es tener un análisis cuidadoso en lugar de hojear un anuncio de lanzamiento y una docena de hilos dispersos. Cualquiera que decida si enrutar un flujo de trabajo de producción a través de Astra, o simplemente curioso sobre lo que significa un transformer en bucle en la práctica, obtiene una lectura enfocada.

Raschka publicó el artículo el 9 de septiembre, y el hilo de discusión es un lugar útil para ver qué preguntas arquitectónicas están presionando los profesionales. Vale la pena combinar el artículo con cualquier plan de prueba interno antes de comprometer un flujo de trabajo al nuevo modelo.

[06:27] Cohere Open-Weights 218B Translation Model Across 50 Languages

Cohere ha publicado North Small Translate con pesos abiertos, un modelo de traducción automática que obtiene una puntuación de 83.6 en la evaluación WMT26 de Cohere en 50 idiomas. El modelo utiliza un diseño de Mezcla de Expertos, una forma de construir un modelo con 218 mil millones de parámetros totales pero activando solo unos 25 mil millones de ellos para cualquier token individual de texto. El resto de los parámetros permanecen inactivos hasta que el modelo los necesita, que es cómo un modelo de este tamaño puede ejecutarse con el perfil de costos de uno mucho más pequeño.

Los pesos son gratuitos para uso no comercial, y las licencias comerciales se gestionan a través de Cohere Model Vault o RWS Language Weaver. Para los desarrolladores, esto significa que cualquiera puede descargar y autoalojar el modelo para investigación o herramientas internas, mientras que las empresas que quieran implementar traducción en un producto tienen un camino de proveedor para derechos de producción.

La conclusión práctica: traducción en 50 idiomas en un solo modelo, y la primera opción creíble de pesos abiertos a esta escala que también viene con una ruta comercial clara. Si has estado combinando API de traducción separadas para cubrir un amplio portafolio de idiomas, un modelo que los maneja todos es una arquitectura significativamente más simple.

[07:37] NVIDIA's BioIR Nearly Triples Protein-Folding Throughput on H100s

NVIDIA detailed BioNeMo Inference Runtime, or BioIR, on September 10 — a Python library that speeds up biomolecular structure-prediction models on NVIDIA GPUs while staying inside plain PyTorch.

La cifra principal proviene de un benchmark pareado en 1,000 objetivos de dímeros humanos ejecutándose en sistemas 8xH100. BioIR-acelerado Boltz-2 plegó 58.5K residuos plegados exitosamente por GPU-hora, comparado con 20.2K para una implementación de código abierto compilada con torch en el mismo hardware. Eso representa una ganancia de 2.90x en rendimiento.

BioIR funciona apilando tres optimizaciones. Primero, selecciona kernels personalizados ajustados para la carga de trabajo. Segundo, utiliza captura de CUDA Graph, que graba operaciones GPU repetidas como un solo gráfico reproducible. Tercero, escala réplicas con Ray de manera que coloca una copia completa del modelo por GPU, así cada acelerador ejecuta una instancia completa de Boltz-2 en lugar de una porción.

El runtime no es solo una demostración de investigación. NVIDIA dice que BioIR ya impulsó la reciente expansión de la Base de Datos AlphaFold, produciendo aproximadamente 31 millones de complejos proteicos candidatos dibujados de 4,777 proteomas. Ese es el tipo de carga de trabajo donde una ganancia de 2.90x cambia la frecuencia con la que un laboratorio puede actualizar una base de datos estructural.

Para cualquiera que ejecute Boltz-2 o modelos de plegado similares en hardware H100, BioIR es un reemplazo directo en Python en lugar de un nuevo framework. Mantiene el flujo de trabajo PyTorch que los desarrolladores ya usan mientras exprime más estructuras plegadas de cada GPU-hora. La pregunta abierta es si las mismas ganancias aparecen en otros backbones de predicción estructural más allá de Boltz-2, y si el patrón BioIR llega pronto a más modelos BioNeMo.

[09:10] DeepSeek's V4.1-Flash Squeezes Million-Token Memory Into FP4 Cache

DeepSeek AI lanzó V4.1-Flash el 10 de septiembre de 2026, y el lanzamiento está dirigido a la carga de trabajo que le ha dado dolores de cabeza a todos: ejecuciones de agentes de millones de tokens.

V4.1-Flash es un modelo multimodal de mezcla de expertos. El backbone tiene 552 mil millones de parámetros, con 196 mil millones de parámetros adicionales que DeepSeek etiqueta como Engram, y el modelo acepta una ventana de contexto de un millón de tokens. En términos simples, está construido para leer el contenido de una pequeña biblioteca en texto, código o imágenes en una sola llamada.

La ingeniería interesante está en dos lugares. Primero, compresión de caché KV en FP4. Cada transformador mantiene un bloc de notas temporal llamado caché KV, esencialmente un registro de a qué ha atendido cada token de entrada hasta ahora. FP4 comprime cada número en ese bloc de notas a 4 bits, reduciendo drásticamente la memoria y el ancho de banda necesarios para mantener prompts de millones de tokens activos en la GPU. Segundo, la reutilización de atención entre capas permite que capas adyacentes compartan partes de ese bloc de notas en lugar de recalcularlas desde cero.

Por qué esto importa ahora: los agentes de horizonte largo han hecho que servir LLMs sea un trabajo intensivo en entrada. Las pre-cargas repetidas, donde el modelo relee todo el prompt de un millón de tokens en cada turno, acumulan entradas de caché KV que tensan la memoria GPU, la capacidad SSD y el ancho de banda de interconexión. DeepSeek está apostando a que comprimir el caché y dejar que las capas compartan el estado de atención es una respuesta más barata que comprar más memoria.

Para los desarrolladores, la pregunta práctica es si el almacenamiento en caché FP4 más la atención compartida mantienen el rendimiento en trazas reales de agentes, cosas como repositorios de código, sesiones de navegación de múltiples horas y revisiones largas de documentos, en lugar de solo benchmarks sintéticos de contexto largo. Si lo hace, esperemos una ola de recetas de la comunidad que porten el mismo truco a otros modelos de pesos abiertos.

[10:51] OpenAI and GSA Cut Government AI Costs to Zero

OpenAI y la Administración de Servicios Generales de EE.UU. están implementando un nuevo acuerdo para gobiernos federales, estatales, locales y tribales elegibles. Bajo el arreglo anunciado el 10 de septiembre, las agencias calificadas pagan $0 en tarifas de licencia y reciben un 50% de descuento en costos de uso, además de soporte de defensa cibernética expandido de OpenAI.

La asociación está diseñada para ampliar el acceso a la IA en el sector público mientras aborda las preocupaciones de seguridad que han ralentizado la adopción gubernamental. El soporte de defensa cibernética es explícito en el anuncio, lo que significa que OpenAI está agrupando protecciones técnicas junto con el acceso con descuento en lugar de tratar la seguridad como una contratación separada.

Para los desarrolladores en el espacio govtech, esto reduce la barrera de costo para crear prototipos de servicios impulsados por IA que necesitan interactuar con sistemas gubernamentales. Agencias estatales, locales y tribales que anteriormente no podían justificar presupuestos de IA empresarial ahora tienen un camino financiado para experimentar, y los contratistas que trabajan con esas agencias obtienen una línea base de precios más clara para propuestas.

Lo que vale la pena observar a continuación: cómo se define la elegibilidad en la práctica en miles de jurisdicciones, qué cubre exactamente el "soporte ampliado de defensa cibernética" en su ejecución, y si competidores como Anthropic, Google o fundaciones de código abierto responden con ofertas similares para defender sus propios nichos gubernamentales.

[12:03] OpenAI convierte el harness de Codex en una Agents API administrada

El 10 de septiembre, OpenAI presentó la Agents API, un servicio en la nube administrado para construir y lanzar agentes. Está alimentada por el harness de Codex, que OpenAI ahora expone como un producto hosted en lugar de algo que los desarrolladores ejecutan en sus propias máquinas.

La Agents API maneja tres cosas para los desarrolladores. Primero, orquestación: el servicio secuencia los pasos del agente y enruta el trabajo entre llamadas, para que el desarrollador no tenga que cablear su propio programador o máquina de estados. Segundo, sesiones de larga duración: un agente puede persistir entre interacciones separadas en lugar de reiniciarse cada vez que un usuario regresa. Tercero, uso de herramientas: el agente puede llamar a herramientas y sistemas externos, con el servicio administrado mediando esas llamadas en lugar de que el desarrollador las proxie.

El argumento es directo. En lugar de implementar infraestructura de orquestación para ejecutar un agente, llamas a la Agents API y despliegas un agente basado en la nube. OpenAI opera el harness; el desarrollador se enfoca en lo que se supone que el agente debe hacer y a qué herramientas puede acceder. El lanzamiento posiciona a OpenAI en el mismo carril que otras plataformas de agentes administradas, pero con Codex como motor subyacente en lugar de un runtime genérico.

Lo que sigue para observar: cómo se delimitan los permisos de uso de herramientas y cómo el servicio maneja la autenticación entre el agente y los sistemas externos a los que llama. La Agents API está disponible desde el 10 de septiembre, y es la primera vez que el harness de Codex se ofrece como un producto administrado de propósito general en el que cualquiera puede construir.

[13:35] Resumen de investigación: Una Nueva Receta para Detectar Alucinaciones de IA, y Reducirlas a la Mitad

Los investigadores han construido una nueva forma de señalar cuándo un modelo de IA inventa hechos. Su pipeline verifica una respuesta desde varios ángulos a la vez: un clasificador entrenado juzga si cada afirmación es fiel, una puntuación de incertidumbre marca las partes sobre las que el modelo mismo no está seguro, y un paso de calibración pone esas señales en una escala comparable. En el benchmark estándar HaluEval, el sistema identificó afirmaciones falsas con precisión en respuestas a preguntas, resumen y diálogo.

El equipo también mostró qué hacer una vez que puedes detectar una alucinación. Ajustaron finamente un pequeño modelo de código abierto llamado Qwen2.5-0.5B con una técnica de entrenamiento de preferencias que recompensa al modelo por elegir respuestas verdaderas sobre las inventadas. Eso redujo la tasa de alucinaciones del modelo casi a la mitad.

Para los constructores, esta es una receta práctica: combina un detector con entrenamiento de preferencias, y obtienes un modelo que tanto admite cuándo está adivinando como aprende a adivinar menos.

[14:30] GitHub Copilot agrega integración con Jira y una CLI adaptativa

GitHub publicó un resumen semanal de Copilot el 10 de septiembre, cubriendo cambios desplegados alrededor del 7 de septiembre. Tres elementos aparecen en la publicación. La aplicación Copilot gana integración con Jira, trayendo contexto del rastreador de problemas al espacio de trabajo de Copilot. La CLI de Copilot lanza "orquestación adaptativa de modelos" bajo el nombre Project HydraFusion, dando a la CLI una forma de coordinar modelos adaptativamente a medida que el trabajo cambia en lugar de bloquear a los usuarios a un solo modelo. La publicación también anuncia nueva automatización de agentes dentro de Visual Studio Code, aunque el resumen del changelog se corta antes de que se listen las capacidades específicas. En conjunto, GitHub está posicionando a Copilot más allá de su superficie original de chat único y hacia vínculos más profundos con herramientas de seguimiento de proyectos y elección de modelos dentro de la CLI. Los detalles completos sobre la pieza de VS Code quedan por verse en la publicación enlazada.

[15:18] La Agents API de OpenAI Entra en Beta Pública

OpenAI puso la Agents API en beta pública el 10 de septiembre, y cada desarrollador puede usarla ahora. El argumento es directo: este es el mismo harness e infraestructura que impulsa Codex, abierto para que cualquiera pueda conectarlo a su propio producto.

La división que importa es quién posee qué. OpenAI aloja y mantiene el harness en sí, así que el equipo maneja actualizaciones, parches de runtime y la capa de orquestación. Los desarrolladores deciden dónde se ejecuta el cómputo real del agente. Hay tres opciones: un sandbox administrado por OpenAI, la infraestructura propia del desarrollador, o un sandbox de socio. Ese último control es el que importará a los equipos de datos: si necesitas que el cómputo permanezca dentro de un entorno específico, puedes apuntarlo a tu propia infraestructura en lugar de la ruta administrada.

Es un producto desplegable y en vivo hoy, no una lista de espera. Ese es el cambio significativo: el harness que los constructores ejecutaban ellos mismos ahora es accesible a través de una llamada a la API, con OpenAI asumiendo la responsabilidad de mantenerlo actualizado.

Una cosa que vale la pena observar: cómo OpenAI maneja las actualizaciones del harness una vez que los desarrolladores tienen agentes en producción. Si la orquestación debajo de agentes en vivo cambia, eso se convierte en una pregunta de estabilidad que vale la pena seguir a medida que más equipos desplieguen contra la beta pública.

[16:33] Una API Autoalojada para Descargar TikTok y Douyin Acaba de Llegar a la v5.0.3

Un scraper autoalojado para TikTok y Douyin acaba de lanzar una nueva versión, y la amplitud de formas en que puedes controlarlo es la noticia. Evil0ctal empujó Douyin_TikTok_Download_API v5.0.3 el 11 de septiembre de 2026. El repo ahora supera las 20,000 estrellas en GitHub.

El argumento de la herramienta es simple: descarga videos de TikTok y Douyin sin la marca de agua, y extrae datos estructurados sobre publicaciones, perfiles, comentarios y listas de reproducción mientras estás en ello. Lo que hace interesante a la v5.0.3 es cuántas superficies expone esos datos. Debajo del capó, una API REST asíncrona maneja las solicitudes. Encima de eso, el proyecto incluye un servidor MCP (Model Context Protocol), una CLI y una consola web. Eso significa que el mismo archivo puede ser consultado por un agente, scriptado desde una terminal, o explorado en una pestaña del navegador.

El despliegue es deliberadamente sin fricción: un simple `docker compose up` levanta la API junto con un archivo PostgreSQL, para que los videos obtenidos y los metadatos persistan entre ejecuciones. El proyecto también depende de un pool de identidades auto-regenerativo, que rota las cookies o huellas digitales que el scraper usa para identificarse ante las plataformas. En la práctica, esa rotación es lo que permite que la herramienta sobreviva el constante juego del gato y el ratón de TikTok y Douyin contra los scrapers — la capa de contribución propia del proyecto absorbe los nuevos bloqueos en lugar de dejar que cada usuario tenga que parchear credenciales manualmente.

Para los desarrolladores, lo que destaca es el servidor MCP. Cualquier agente o cliente de chat que ya hable MCP puede tratar las cuentas de TikTok y Douyin como fuentes de datos estructuradas — extrayendo publicaciones, perfiles, comentarios y listas de reproducción bajo demanda — sin necesidad de escribir un scraper desde cero. Los creadores e investigadores que prefieren su propio archivo privado en lugar de una factura mensual de un scraper alojado obtienen un único comando Docker como punto de entrada. Una cosa a seguir: cuánto tiempo el pool de identidades auto-regenerativo mantiene el ritmo ahora que ambas plataformas continúan endureciendo el acceso automatizado.

[18:31] El Agente de Datos de OpenAI convierte archivos de empresa en paneles de control a través del chat

OpenAI ha añadido un Agente de Datos a ChatGPT Work, anunciado el 10 de septiembre a través del canal de noticias de la empresa. El propósito declarado del agente es directo: conectarse a los datos de la empresa, revelar insights y armar paneles de control interactivos a partir de un prompt en lenguaje natural en lugar de una hoja de cálculo o consulta SQL.

Esa última pieza es el cambio significativo. La audiencia que el anuncio menciona es "todos", no analistas, lo que significa que el producto está posicionado para la persona más cercana a la pregunta de negocio que generalmente tiene que presentar una solicitud y esperar. Una interfaz de lenguaje natural que produce tanto una respuesta como un artefacto visual colapsa el traspaso típico entre quien hace la pregunta, el analista y la herramienta de panel de control.

Lo que el anuncio realmente confirma es limitado: un producto llamado Agente de Datos, un hogar dentro de ChatGPT Work, tres capacidades (conectar, descubrir, construir paneles de control) y una interfaz de lenguaje natural. Lo que no especifica es qué fuentes de datos se conectan de forma nativa, si los paneles de control son artefactos editables o productos únicos, o cómo funcionan los controles de acceso.

Para desarrolladores y operadores, la pregunta práctica es si esto reemplaza un flujo de trabajo o añade uno nuevo. La lectura honesta del anuncio es que OpenAI está marcando territorio en la capa de analytics conversacional antes de que los competidores cierren la misma puerta. Vale la pena seguir: cómo el agente maneja las citas de fuentes, y si los paneles de control sobreviven la conversación como entregables independientes.