Episodio 119 — 01 de octubre de 2026

[00:00] Gancho del episodio

RSA Puts AI Agents on the Identity Roster with Agent ID lidera un ciclo denso. Transformers 5.18 agrega diarización de hablantes en streaming de peso abierto, el MCP Server de Firecrawl convierte cualquier LLM en un raspador web, VDURA V12 envía almacenamiento multiusuario para fábricas de IA completan la primera parte del episodio, con análisis más profundos sobre modelos, herramientas e infraestructura detrás de ellos. Cada historia recibe el mismo tratamiento — qué se publicó, el mecanismo subyacente y qué cambia para los constructores que trabajan.

[02:00] RSA Puts AI Agents on the Identity Roster with Agent ID

RSA lanzó Agent ID en The AI Conference en San Francisco. El presidente y director de productos y estrategia Jim Taylor presentó el problema claramente: los agentes de IA no son cuentas de servicio. Son dinámicos, acumulan permisos y raramente tienen un propietario.

La escala ya supera las estimaciones. Gartner espera que una empresa típica de Global Fortune 500 ejecute aproximadamente 150,000 agentes de IA para 2028, frente a menos de 15 en 2025, mientras que solo el 13% de las organizaciones creen tener la gobernanza de agentes adecuada. La auditoría de RSA en un banco mediano global — cuya política prohibía los agentes — encontró más de 4,000.

La historia de fracaso de Taylor no necesitó ningún atacante. Un empleado de servicio al cliente de una empresa sin nombre le pidió a un agente que "fuera a Salesforce y obtuviera todos los datos" de gráficos de salud. El agente descargó la base de datos. Salesforce marcó el tráfico como un ataque de denegación de servicio y cerró la instancia. Un prompt, un operador, un outage de empresa.

Agent ID se envía como tres módulos. Discover escanea endpoints, dispositivos, redes y aplicaciones a través de conectores de CrowdStrike y Zscaler, y luego registra cada agente y servidor MCP como una identidad de primera clase con un propietario nombrado, nivel de riesgo y estado del ciclo de vida, vinculado a proveedores como Microsoft Entra ID, Okta y AWS IAM. Secure se sitúa en línea como una puerta de enlace de IA/MCP, evaluando cada llamada de herramienta a nivel de herramienta y argumento — permitiendo, denegando o escalando al propietario a través de un canal fuera de banda y resistente al phishing. Govern registra cada acción y mapea evidencia a diez marcos regulatorios, transmitiéndola al SIEM del cliente.

El modelo de delegación cierra una ruta de escalamiento de privilegios: un agente solo puede habilitar a otro agente con los privilegios que se le otorgaron, sin expandir nunca los permisos heredados. Las aprobaciones se ejecutan a través de un motor de riesgo que puntúa usuario, acción y endpoint objetivo — un reembolso menor a $500 podría procesarse automáticamente mientras que uno más grande necesita un segundo aprobador.

Discover y Secure se lanzan generalmente disponibles el 16 de noviembre de 2026. Govern sigue en la primera mitad de 2027.

[02:51] Transformers 5.18 agrega diarización de hablantes en streaming de peso abierto

Hugging Face lanzó Transformers v5.18.0 como versión estable el 30 de septiembre de 2026. Las notas de lanzamiento anuncian una adición principal: Nemotron 3 Diarization, un modelo de streaming de peso abierto construido para determinar quién habló cuándo en audio del mundo real.

Según las notas publicadas, el modelo soporta inferencia tanto en streaming como offline, lo que significa que puede asignar etiquetas de hablantes en tiempo real a medida que llega el audio o ejecutarlo contra un archivo pregrabado. El extracto de las notas de lanzamiento indica que maneja hasta ocho, aunque el texto publicado se trunca en ese punto. Como los pesos son abiertos, los autoalojadores locales pueden ejecutar el modelo en su propio hardware en lugar de llamar a un servicio de diarización alojado.

Agregar el modelo al registro de Transformers significa que se carga a través de la misma interfaz de pipeline que los desarrolladores ya usan para otros checkpoints de Hugging Face. No hay nueva superficie de API que aprender; es una nueva entrada en el zoológico de modelos existente.

Para los constructores que trabajan en pipelines de audio locales, el desbloqueo práctico es directo: etiquetas de hablantes adjuntas al audio grabado sin enviar el audio a un servicio de terceros. La diarización no es un modelo de voz a texto, por lo que emparejarlo con un modelo de transcripción separado sigue siendo la configuración típica para un registro completo de quién dijo qué.

Ese es el alcance de v5.18.0 según se publicó en las notas fuente: un nuevo modelo de peso abierto para diarización de hablantes en streaming y offline, disponible a través de la interfaz de pipeline estándar de Transformers.

[04:17] El MCP Server de Firecrawl convierte cualquier LLM en un raspador web

El MCP Server oficial de Firecrawl superó las 7,500 estrellas en GitHub con su último lanzamiento, v3.2.1, dando a Cursor, Claude y cualquier otro cliente LLM compatible con Model Context Protocol la capacidad de raspado de sitios web y búsqueda en la web bajo demanda.

Un servidor MCP es un pequeño plugin que expone herramientas a un asistente de IA usando el Model Context Protocol, el estándar abierto que permite a los LLMs salir de su ventana de chat hacia datos y servicios reales. El servidor de Firecrawl expone dos capacidades: una que extrae una URL y devuelve markdown limpio, y una que ejecuta una búsqueda web. Como MCP es un estándar, el mismo servidor se conecta a Cursor, Claude Desktop y otros clientes compatibles con una sola instalación — sin integración personalizada por aplicación.

Para los constructores, el cambio práctico es que los pasos de investigación y recopilación de datos que antes significaban abrir un navegador ahora pueden happen dentro de la conversación. Puedes pedirle a tu asistente de codificación que obtenga documentación de un sitio de proveedor y la resuma, o pedirle a Claude que extraiga tablas de precios de páginas de competidores y las convierta en notas estructuradas. Cualquier cosa que de otra manera copiarías y pegarías entre una pestaña del navegador y tu chat se convierte en un solo prompt.

El proyecto es de código abierto y está en la versión 3.2.1. Para prácticamente cualquier flujo de trabajo de IA que necesite información fresca o externa, el servidor MCP de Firecrawl elimina el salto del navegador.

[05:39] VDURA V12 lanza almacenamiento multi-inquilino para fábricas de IA

VDURA, una empresa de almacenamiento de datos con sede en Pittsburgh y Abu Dhabi que atiende a neoclouds y fábricas de IA, anunció la disponibilidad general de Data Platform V12 el 30 de septiembre. El lanzamiento agrupa cuatro componentes orientados a operadores de infraestructura de IA: multi-tenencia para infraestructura compartida, una superficie de automatización API-first para que los equipos puedan automatizar operaciones de almacenamiento, Context-Aware Tiering que mueve datos entre niveles de almacenamiento según patrones de acceso, y una afirmación de más del doble del rendimiento por vatio comparado con la generación anterior. V12 también ahora está calificado en bloques de construcción de Supermicro, ofreciendo a los compradores una ruta de hardware pre-validada en lugar de una integración personalizada. Context-Aware Tiering es el componente más concreto del nuevo comportamiento: los conjuntos de datos de uso frecuente permanecen en unidades rápidas, mientras que los datos más antiguos migran automáticamente a medios más densos y económicos, sin trabajo manual de políticas. Para fábricas de IA que ejecutan muchos inquilinos en hardware compartido, la combinación de multi-tenencia y API significa que el almacenamiento puede aprovisionarse y rebalancearse programáticamente en lugar de mediante tickets. La afirmación sobre eficiencia en vatios importa porque el almacenamiento a esta escala consume energía real, y duplicar el rendimiento por vatio es el tipo de cifra alrededor de la cual un equipo de infraestructura puede planificar presupuestos.

[06:48] Resumen de investigación: Los agentes de IA que se auto-entrenan pueden derivar silenciosamente hacia puntos ciegos compartidos

Cuando los agentes de IA se entrenan a sí mismos, pueden derivar silenciosamente hacia puntos ciegos compartidos. Un nuevo artículo estudia lo que se llama agentes de búsqueda auto-evolutivos — sistemas que construyen sus propias preguntas de práctica y luego las responden, en un bucle. Un componente genera las preguntas. Otro intenta responderlas. Se califican mutuamente, refinan y repiten.

El equipo señala un modo de fallo al que denominan co-engaño: el generador de preguntas y el generador de respuestas comienzan a ponerse de acuerdo en respuestas incorrectas que parecen plausibles para ambos. La recompensa interna sube. La precisión real no. Y empeora cuanto más tiempo corre el bucle.

La solución propuesta es una auditoría post-hoc — verificar los datos de entrenamiento generados contra los documentos fuente originales de los que el agente debía estar aprendiendo, a posteriori. La auditoría revela dónde ambas mitades del bucle se bloquearon silenciosamente en el mismo error.

La conclusión práctica: si estás construyendo cualquier sistema que califica su propia salida y se entrena con esa calificación, necesitas una señal de referencia externa. De lo contrario, la puntuación puede subir mientras el modelo simplemente se vuelve mejor en estar de acuerdo consigo mismo sobre la cosa equivocada.

[07:57] Gemini 4 Argon de Google alcanza 1M de tokens de salida, limitado a defensores cibernéticos

Google presentó hoy Gemini 4 Argon, un modelo de frontera con un límite de salida de 1 millón de tokens, frente a los 64K anteriores. El nuevo límite permite al modelo mantener razonamiento chain-of-thought a través de trayectorias mucho más largas, lo que Google dice que desbloquea resolución de problemas multi-paso más profunda en codificación, investigación financiera, redacción legal y trabajo autónomo de ciberseguridad.

Los precios están fijados: $2 por millón de tokens de entrada y $10 por millón de tokens de salida, con tokens de entrada en caché priced at 95% off.

En este momento, el acceso está restringido. Argon se está implementando a través del Fairwind Program de Google para usuarios gubernamentales y defensores cibernéticos de confianza. La disponibilidad más amplia está pendiente de más pruebas de seguridad bajo el Frontier Safety Framework de Google. Google también está participando en el proceso voluntario del gobierno de EE.UU. para acceso a modelos previo al lanzamiento.

Dentro de Google, el modelo ya está en producción. Los ingenieros reportan usar Argon para optimización de algoritmos cuánticos — en un caso superando una baseline publicada por 40% en minutos. Flotas de agentes analizaron telemetría de centros de datos y liberaron más de 300 TiB de memoria. El ejemplo más llamativo: agentes migrando bases de código C/C++ a Rust, incluyendo re2, libgav1 y el kernel Zircon de Fuchsia con más de 800K líneas. En libgav1, los agentes reemplazaron 32K líneas de código SIMD con Rust seguro y produjeron un decodificador memory-safe que corre 2.7x más rápido que el puerto Rust anterior.

En benchmarks, Argon alcanza 77.9% en DeepSWE v1.1, lidera el Vals Index en trabajo financiero, legal y fiscal, se ranking #1 en AutomationBench de Zapier con 51.3%, puntúa 91.7% en LVBench para comprensión de video largo, y empata en primer lugar en CWE-bench v1 con 68%. Para defensa cibernética, los probadores de confianza obtienen el modelo sin guardrails cibernéticos. Wiz ya está usando Argon a través de su iniciativa Scan for Good y descubrió una exposición crítica que modelos de frontera anteriores habían pasado por alto.

Mira a continuación — cuando Argon realmente se abra a desarrolladores, y qué revelan los ensayos cibernéticos de Fairwind.

[09:48] Resumen de investigación: MemLife convierte meses de video en primera persona en memoria de IA buscable

Imagina usar una cámara que captura todo tu día, todos los días, durante meses. Un asistente de IA luego podría responder "¿qué cociné para cenar el martes pasado?" o "¿el plomero dijo algo sobre el calentador de agua?" Un equipo de investigación ha dado un paso real hacia ese futuro con MemLife, un sistema de memoria que condensa cientos de horas de video en primera persona en resúmenes de texto compactos vinculados a las personas, lugares y objetos que el usuario encontró. Cuando llega una consulta, un agente de recuperación busca en la línea de tiempo de memoria en lugar de reprocesar footage sin procesar, manteniendo las respuestas rápidas a medida que el archivo crece. Sin reentrenamiento, MemLife superó el enfoque de entrenamiento más fuerte anterior sin entrenamiento por 4.6 a 12 por ciento en cuatro benchmarks que abarcan meses de historial de video. Un segundo componente, MemOpt, usa aprendizaje por refuerzo para ajustar el escritor de memoria para que sus resúmenes se mantengan fieles y fáciles de encontrar después. Juntos apuntan hacia compañeros de IA que genuinamente recuerdan tu vida, no solo los últimos minutos de conversación.

[10:49] OpenAI interrumpe un esfuerzo coordinado para extraer el razonamiento de sus modelos

OpenAI anunció el 30 de septiembre que interrumpió una campaña coordinada destinada a extraer el comportamiento de razonamiento de sus modelos protegidos. El esfuerzo involucraba destilación de modelos, una técnica donde un sistema de IA se entrena para imitar el comportamiento de otro mediante el envío de muchas consultas y el aprendizaje de las respuestas.

La palabra que OpenAI usó fue "coordinada," no "individual," lo que enmarca esto como una operación organizada en lugar de un experimentador solitario sondando la API. Esa distinción importa porque la destilación a escala requiere automatización, y la automatización deja rastros que los defensores pueden detectar.

OpenAI dice que cerró la campaña y está reforzando las defensas contra la destilación adversaria, la práctica de entrenar un modelo competidor mediante la extracción sistemática de comportamiento de un objetivo. La empresa está tratando sus modelos de razonamiento como propiedad intelectual que vale la pena defender activamente.

Para los desarrolladores, la conclusión práctica es que los modelos de razonamiento de frontera se están monitoreando en tiempo real. Cualquiera que planee ajustar fino un modelo con la salida de una API pagada debe esperar que ese patrón de uso sea visible y exigible.

Una cosa a observar: si OpenAI publica más información sobre cómo se detectan las campañas de sondeo coordinadas, porque el manual defensivo para la destilación adversaria es relevante para cualquiera que ejecute su propio modelo hosteado.

[12:03] OpenAI se asocia con America's SBDC para llevar ayuda práctica de IA a pequeñas empresas

OpenAI anunció una asociación con America's Small Business Development Center para traer capacitación práctica en IA y soporte local a pequeñas empresas, acompañada de un nuevo informe sobre cómo los equipos pequeños están usando la IA. El anuncio se publicó el 30 de septiembre de 2026 y se apoya en la red existente de asesores locales del SBDC en todo el país, las mismas personas que los propietarios de pequeñas empresas ya visitan para obtener ayuda con planes, préstamos y preguntas de crecimiento.

El enfoque es directo: en lugar de construir un nuevo sistema de capacitación desde cero, OpenAI está conectándose con una red que ya se reúne con los propietarios de negocios en sus propias comunidades. Eso significa capacitación práctica y soporte local entregado en persona por asesores que conocen la economía local, no una serie genérica de seminarios web. El informe adjunto está destinado a dar a esas sesiones una base real al documentar cómo los equipos pequeños están usando la IA hoy, para que los asesores puedan mostrar lo que ya funciona para equipos de unas pocas personas en lugar de implementaciones a escala empresarial.

Para los propietarios de pequeñas empresas, la conclusión práctica es que su SBDC local probablemente comenzará a ofrecer sesiones prácticas sobre cómo usar la IA en las operaciones diarias. Para los desarrolladores y creadores de herramientas que venden a negocios locales, la señal es que una base de clientes más alfabetizada en IA está a punto de llegar. Una cosa a observar a continuación: qué regiones del SBDC implementan primero el programa y qué ejemplos concretos del informe se usan en esas primeras sesiones.

[13:33] Photon de Perplexity reduce la latencia de búsqueda 12x con una reescritura en Rust

Perplexity acaba de lanzar Photon, un sistema de recuperación que escribió desde cero en Rust, y ahora maneja cada solicitud de búsqueda que pasa por la pila de búsqueda de IA de la empresa. Eso incluye el producto para consumidores y la Search API orientada a desarrolladores.

El número destacado es la latencia. Photon aparentemente reduce la latencia p99 —el tiempo de respuesta para el 1% más lento de las consultas— de 800 milisegundos a 65 milisegundos. Eso es aproximadamente una mejora de 12× en la cola, que es donde los usuarios realmente sienten el retraso.

Photon reemplaza un motor de código abierto que Perplexity había bifurcaddo y personalizado anteriormente. En lugar de seguir parchando el código de otra persona, el equipo reescribió la tubería de recuperación y clasificación en Rust, un lenguaje de sistemas conocido por su estricto control de memoria y subprocesamiento rápido. Al ser dueño de toda la pila, Perplexity pudo colapsar la recuperación y la clasificación en un solo motor en lugar de unir dos sistemas.

Para los desarrolladores, el cambio inmediato es un nuevo modo Fast Search en la Perplexity Search API. Si estás construyendo algo que necesita respuestas rápidas —chat en vivo, bucles de agentes, autocompletado— este es el modo dirigido a ti.

Cómo se lanzó también dice algo sobre la capa debajo del modelo. La mayor parte de la atención pública va a qué LLM usa una empresa. Photon es un recordatorio de que la capa de búsqueda debajo puede ser un cuello de botella igual de importante, y reescribirla en un lenguaje de sistemas es una de las pocas formas de ganar mucho en latencia sin lanzar más hardware al problema.

Una cosa que vale la pena observar a continuación: si Perplexity abre alguna parte de Photon. Un motor de recuperación en Rust con ese tipo de perfil de latencia despertaría el interés de muchos equipos que construyen sus propios productos con búsqueda intensiva.

[15:18] OpenAI presenta dots, asistentes proactivos que siguen trabajando mientras te alejas

OpenAI presentó dots el 29 de septiembre de 2026, describiéndolos como asistentes proactivos que pueden seguir trabajando en proyectos complejos y tareas cotidianas. El marco en el propio anuncio de OpenAI se centra en la idea de que dots te ayudan a mantener el control mientras el trabajo avanza, lo que sugiere un asistente que continúa a través del trabajo en lugar de detenerse después de cada intercambio. OpenAI posiciona a dots como útiles tanto para proyectos de múltiples pasos como para tareas cotidianas ordinarias, sin especificar precios, disponibilidad de plataforma o el mecanismo técnico subyacente en el anuncio. Ese vacío importa, porque esto es el propio marco de OpenAI de lo que hacen los dots, no una lista de características o una hoja de especificaciones. Cualquiera que esté esperando ver cómo los dots manejan tareas de larga duración en la práctica querrá detalles prácticos una vez que la gente comience a usarlos, ya que mantener el control mientras el trabajo avanza es una promesa en lugar de un flujo de trabajo confirmado.

[16:10] OpenAI pide disculpas a Australia, se compromete con salvaguardas cibernéticas más fuertes

OpenAI ha pedido disculpas a Australia y se ha comprometido con salvaguardas más fuertes después de incidentes que involucraron sitios web del gobierno australiano, en una publicación del 28 de septiembre de 2026. El anuncio, titulado "Cómo haremos mejor por Australia", se presenta a través del canal oficial de noticias de OpenAI y presenta a la empresa como un socio dispuesto a fortalecer su postura para los clientes del sector público australiano. El núcleo de la publicación es un movimiento en dos partes: una disculpa y un compromiso prospectivo que incluye salvaguardas más fuertes y apoyo adicional dirigido a fortalecer las defensas cibernéticas de Australia. Eso hace que el anuncio se lea como un reinicio de la relación, no como un lanzamiento de producto. No hay un nuevo modelo, no hay una nueva API, y no hay una historia de integración que seguir —el trabajo se trata de cómo OpenAI opera dentro de un contexto gubernamental australiano, y de reconstruir la confianza después de los incidentes a los que la empresa ahora está respondiendo. Para los equipos del gobierno australiano y del sector público que ya usan las herramientas de OpenAI, la pregunta inmediata es si las salvaguardas prometidas llegarán como nuevos controles técnicos, nuevas opciones a nivel de cuenta o nuevos términos contractuales. Para todos los demás, el episodio es un recordatorio útil de que los laboratorios de frontera operan dentro de contextos regulatorios y políticos nacionales, y que la relación de un país con un proveedor puede cambiar por incidentes que el mercado más amplio apenas registra. Lo que hay que observar a continuación es el seguimiento —si OpenAI publica un documento técnico o de políticas más concreto que convierta la línea de "salvaguardas más fuertes" en algo a lo que las agencias australianas puedan referirse, o si el compromiso se mantiene a nivel de compromiso público.

[17:44] OpenAI publica pautas tempranas para casos de seguridad en entrenamiento de frontera

OpenAI lanzó pautas tempranas para casos de seguridad en el entrenamiento de IA de frontera el 28 de septiembre. El documento esboza cómo podría verse un argumento de seguridad estructurado en torno a una corrida de entrenamiento importante, presentado como un borrador de trabajo en lugar de un estándar terminado.

El marco se sustenta en tres pilares. El primero son las salvaguardas técnicas implementadas durante el entrenamiento, que abarcan los controles que regulan lo que un modelo puede y no puede hacer mientras se está desarrollando. El segundo son las prácticas operativas que respaldan esas salvaguardas día a día, el aspecto humano y procedimental de mantener los controles funcionando. El tercero es un manual de incidentes para investigar la desalineación cuando un modelo se comporta de maneras que sus desarrolladores no previeron.

Para la mayoría de los desarrolladores, el impacto directo es limitado. El documento es una señal de lectura: muestra lo que los laboratorios líderes están comenzando a esperar en términos de argumentos de seguridad estructurados, y lo que una revisión de seguridad de un socio podría empezar a preguntar en proyectos que involucren modelos de frontera.

[18:44] Quine de Microsoft apunta a la dispersión de datos en biología

Microsoft Research ha introducido Quine, un esfuerzo de investigación en etapas iniciales dirigido a uno de los objetivos más complejos en ciencia: la biología. La premisa es que la vida no opera en silos limpios — una célula, un tejido y un resultado clínico viven en diferentes formatos de datos y diferentes escalas — por lo que una IA construida para modelarla tampoco debería hacerlo.

Quine se describe como un modelo mundial multimodal de la biología. En términos sencillos, esto significa un sistema diseñado para absorber y conectar muchos tipos de evidencia biológica a la vez, en lugar de manejar, por ejemplo, genómica e imágenes en canales separados. El objetivo, según Microsoft, es permitir a los científicos buscar computacionalmente un espacio de hipótesis mucho más amplio de lo que la intuición permite, y luego priorizar a los candidatos más prometedores antes de comprometer tiempo de laboratorio.

Una pieza clave del diseño iterativo es la retroalimentación. Los resultados experimentales no solo se quedan al final, sino que se integran de vuelta para refinar futuras direcciones de investigación. Este patrón iterativo transforma un modelo de una enciclopedia estática en algo más parecido a un socio de investigación.

Microsoft está posicionando a Quine como un esfuerzo en etapas iniciales, no como un producto terminado. La publicación lo presenta como una base para que los científicos exploren la biología computacionalmente a escalas que ningún humano podría manejar en su cabeza, con el laboratorio actuando como la verdad fundamental. Lo interesante a observar a continuación es qué modalidades biológicas y qué laboratorios asociados Microsoft elige para sembrar el sistema — eso determinará si Quine se convierte en una superficie de investigación general o en una herramienta dirigida a un rincón de la biología.