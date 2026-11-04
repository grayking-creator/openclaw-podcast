Episodio 126 — 29 de octubre de 2026

[00:00] Gancho del episodio

Google anunció Gemini 4 Carbon como su modelo más potente, diseñado para flujos de trabajo prolongados de ingeniería de software y para todo el ciclo de defensa cibernética, y afirmó que Carbon encontró vulnerabilidades. OpenAI publicó resultados de modelos relacionados con la conjetura de Kakeya, la Hipótesis del Tiempo Exponencial y la cromodinámica cuántica, ampliando su trabajo en las matemáticas y la física. Según un estudio de caso de OpenAI del 27 de octubre, los agentes de voz de RetellPowered by OpenAI ahora gestionan 100 millones de llamadas cada mes, mientras que GPT-6 Astra encabeza la prueba comparativa de agentes de voz de la compañía. Las ingenieras de Anthropic Katelyn Lesse y Angela Jiang explican cómo el equipo de Claude Platform lanzó Opus 5.5 y opera agentes gestionados al separar la toma de decisiones del modelo de sus acciones externas. Los desarrolladores de hardware también recibieron nuevas opciones de IA local: la tarjeta de estación de trabajo compacta Radeon AI Pro R9700 de ASRock combina 32 GB de GDDR6 con un ancho de banda de 640 GB/s y soporte de FP8 para RDNA 4, mientras que NVIDIA publicó Nemotron-3.5-Bolt-E4B-4GB, un modelo cuantizado de 8 B de parámetros y 4 GB diseñado para asistentes de voz locales, personas interactivas e interfaces integradas.

[02:00] Gemini 4 Carbon apunta a la ingeniería de larga duración y la defensa cibernética

Google anunció Gemini 4 Carbon como su próximo modelo de frontera. Google afirma que Carbon puede funcionar durante varios días, persistir ante caminos sin salida, identificar las causas深层 de errores sutiles en bases de código grandes y generar soluciones. Los resultados cibernéticos abarcan tres etapas: encontrar vulnerabilidades, comprobar si son explotables y parchear la causa subyacente. Google informa que Carbon obtuvo un 88,2 % en SEC-bench Pro para el descubrimiento de vulnerabilidades, un 54,8 % en ExploitGym para la explotación y un 71,0 % en CWE-bench de Collinear para generar parches de código. El editor informa que, en las pruebas internas de Google, Carbon más que duplicó la tasa de éxito de Argon para generar código seguro. Carbon está disponible inicialmente para un grupo selecto de defensores cibernéticos, y el acceso se ampliará gradualmente a socios de confianza mediante el Fairwind Program. Posteriormente, los desarrolladores, las empresas y los consumidores podrán acceder a él. Su precio introductorio será de 2 USD por millón de tokens de entrada y 10 USD por millón de tokens de salida, con un 95 % de descuento para las entradas en caché; después, las tarifas serán de 4 y 20 USD. El próximo hito que conviene observar es cómo utilizan Carbon los primeros defensores y si se amplía el acceso. Google afirma que Carbon está diseñado para flujos de trabajo agénticos prolongados y puede funcionar durante varios días mientras aborda tareas complejas de ingeniería de múltiples etapas.

[02:32] OpenAI comparte resultados de modelos sobre tres problemas científicos

OpenAI compartido resultados de modelos sobre la conjetura de Kakeya, la Hipótesis del Tiempo Exponencial y la cromodinámica cuántica, junto con una explicación de cómo los investigadores académicos pueden verificar el trabajo y avanzar a partir de él.

El resultado útil es el acceso a resultados producidos por modelos en las matemáticas, la informática y la física. Los investigadores pueden examinar el trabajo y desarrollar nuevas investigaciones a partir de él, convirtiendo la salida del modelo en material para la investigación científica en lugar de dejarla como producto final.

OpenAI presenta a las comunidades académicas como participantes activos en la verificación y el avance de los resultados. La próxima prueba consistsirá en ver si esos investigadores pueden verificar el trabajo y convertirlo en mayor progreso científico.

[03:11] Los agentes de voz de Retell powered by OpenAI alcanzan los 100 millones de llamadas mensuales

El 27 de octubre, OpenAI publicó un estudio de caso que muestra que Retell está utilizando modelos de OpenAI para impulsar una operación de agentes de voz que gestiona 100 millones de llamadas cada mes. Retell informa que GPT-6 Astra encabeza su prueba comparativa de agentes de voz, mientras que Codex ayudó a la compañía a alcanzar un ingreso anualizado de 1,6 millones de USD por empleado.

El ejemplo útil es un sistema de agentes de voz a escala de producción, y no una pequeña demostración. GPT-6 Astra lidera la prueba comparativa de Retell, y la implementación procesa suficiente tráfico mensual para que 100 millones de llamadas representen una medida operativa significativa. La cifra de ingresos por empleado agrega una señal empresarial al resultado sobre el rendimiento del modelo.

Para quienes desarrollan agentes de voz, este caso ofrece una referencia concreta sobre la escala y los resultados asociados con una implementación powered by OpenAI. El volumen de llamadas y los ingresos por empleado son los dos indicadores que conviene seguir a medida que evoluciona el uso de los modelos por parte de Retell.

[04:02] Anthropic separa el modelo de las acciones del agente

El equipo de plataforma de Anthropic tiene una forma concreta de hacer que los agentes sean más controlables: mantener separado el modelo que razona del sistema que actúa. En una entrevista de Latent Space del 27 de octubre, Katelyn Lesse y Angela Jiang describieron el lanzamiento de Opus 5.5 y la ampliación de Claude Platform mediante agentes gestionados cuyo cerebro, arnés y entorno aislado están desacoplados. La capa de ejecución está contenida mediante aislamiento, protecciones de credenciales y controles de red, mientras que los arneses de larga duración están diseñados para mantener el progreso entre distintas ventanas de contexto.

Para quienes desarrollan soluciones, esto respalda una arquitectura de agentes capaces de seguir trabajando sin conceder al modelo de razonamiento un control sin restricciones sobre las herramientas o las credenciales. La conversación también distingue los incidentes relacionados con el entrenamiento de las salvaguardas en producción y cubre los clasificadores de seguridad y el enrutamiento de modelos como partes de la operación de la plataforma.

Una pregunta clave para los equipos que adoptan este patrón es si sus mecanismos de contención y preservación del progreso siguen siendo fiables cuando las cargas de trabajo de los agentes se prolongan.

[04:57] Radeon AI Pro R9700 de ASRock apunta a la inferencia en estaciones de trabajo locales

ASRock está llevando la plataforma de estación de trabajo RDNA 4 de AMD a quienes desarrollan IA local con Creator Radeon AI Pro R9700. La tarjeta combina 32 GB de memoria GDDR6 con un ancho de banda de 640 GB/s y soporte para matemáticas matriciales FP8, un formato de menor precisión que permite contener más parámetros del modelo dentro de un presupuesto de memoria fijo.

En el centro se encuentra el procesador Navi 48 de AMD, con 64 unidades de cómputo, 128 núcleos aceleradores de IA y una frecuencia máxima de 2,92 GHz. ASRock calcula un rendimiento de matrices densas FP8 de 382,7 TFLOPS, que se duplica al utilizar dispersión. Los modelos FP6 y FP4 se procesan en FP8 en lugar de sus formatos nativos. Un ejemplo práctico es un modelo de aproximadamente 30 B de parámetros que funciona dejando cierta VRAM libre.

El diseño hace énfasis en el uso en estaciones de trabajo. Es un soplador de doble ranura que mide 271 por 111 por 39 milímetros, y se pueden instalar hasta cuatro tarjetas en un sistema ATX estándar. Los usuarios de Linux pueden activar manualmente ECC suave para mayor confiabilidad. La tarjeta consume 300 vatios, algo que la reseña describe como manejable para un diseño con soplador.

La capacidad de memoria es la principal limitación. La R9700 tiene 32GB, menos que los 48GB de la Radeon Pro W7900 de la generación anterior. La siguiente pregunta es cómo sus mejoras de cómputo RDNA 4 se traducen en rendimiento y eficiencia práctica de inferencia dentro de ese menor presupuesto de memoria.

[06:16] El modelo NVIDIA de 4GB Bolt apunta a pilas locales de agentes

NVIDIA publicó NVIDIA-Nemotron-3.5-Bolt-E4B-4GB, un modelo de texto cuantizado orientado a asistentes locales de voz y dispositivos, personalidades interactivas e interfaces incrustadas. NVIDIA afirma que el modelo se/https://www.nvidia.com/en-us/ai/ Further post-trained from Gemma-4-E4B-it and is designed for low-memory, low-time-to-first-token operation. The model is an 8B-parameter text model with 4B effective parameters, Q4_K_M precision, up to 64K-token input and output lengths, reasoning controls, conversational mode, and tool calling. Its controls include enabled or disabled thinking, a runtime thinking budget and a conversational mode that produces more concise replies. It supports function-style tool calling, including a documented pattern for acknowledging a pending tool result and resuming the conversation when the result arrives. NVIDIA provides download and llama.cpp server instructions, along with a companion DFlash drafter for speculative decoding. NVIDIA’s own Q4_K_M evaluation table reports a 55.60 MultiChallenge score for this model versus 39.36 for Gemma4 E4B-it, and says the measurements were conducted under a consistent NVIDIA harness. The model card says the model is ready for commercial or non-commercial use and provides download and llama.cpp serving commands. The model card warns that restricted token allocations may truncate thought processes mid-sentence, so task-specific evaluation remains necessary. NVIDIA published the NVIDIA-Nemotron-3.5-Bolt-E4B-4GB as a generally available model on October 23, 2026. The publisher reports that in NVIDIA's Q4_K_M evaluations, Nemotron-3.5-Bolt-E4B-4GB scored 55.60 on MultiChallenge, compared with 39.36 for Gemma4 E4B-it.

[07:39] Las inversiones de Estados Unidos aumentan la capacidad de chips y crean un campo de pruebas para armas autónomas

La Casa Blanca detalló una serie de inversiones industriales con implicaciones directas para los chips, el hardware de cómputo y los sistemas autónomos. Carolina del Norte recibirá hasta 1.500 millones de dólares para ampliar la producción de semiconductores, mientras que Sibelco está aumentando la producción de cuarzo de alta pureza y materiales relacionados esenciales para los semiconductores en Mitchell County.

La administración también está recurriendo a la Defense Production Act para liberar 150 millones de dólares con el fin de ampliar la capacidad de refinación de Estados Unidos, orientado a aumentar la producción nacional de diésel y gasolina. En Montana, el Department of War está estableciendo un nuevo campo para probar armas y tecnologías avanzadas, incluidas armas autónomas y capacidades de guerra espacial y electrónica.

Para quienes desarrollan productos, la inversión en semiconductores es una señal concreta en el eslabón inicial: una mayor capacidad planificada para producir chips y materiales esenciales podría sostener una base de hardware nacional más amplia. El campo de Montana crea un espacio dedicado para evaluar sistemas autónomos y de guerra electrónica.

Un aspecto que conviene observar es con qué rapidez las inversiones anunciadas se convierten en instalaciones operativas a la escala descrita.

[08:38] Resumen de investigación: La memoria grupal puede distorsionar la evidencia que conserva

Un grupo de modelos de lenguaje puede perder la sustancia de su propia discusión cuando uno de los modelos comprime el intercambio en una memoria breve. Dos reglas que resultan tentadoras fallan de maneras diferentes. Seleccionar las afirmaciones más raras a veces funciona, pero, en promedio, no es mejor que elegirlas al azar. Seleccionar las afirmaciones que parecen relevantes para la decisión puede ser incluso peor, porque los señuelos plausibles también tratan el mismo tema. Quien toma la decisión final introduce otra distorsión: la prueba social, es decir, que da más peso a un hecho porque muchos agentes se les atribuye haberlo dicho. Eliminar o reasignar al azar esas atribuciones, sin alterar el orden de la discusión, mejora la precisión. La transcripción completa también puede obtener una puntuación inferior a no tomar notas en absoluto, lo que demuestra que la compresión no es automáticamente el problema; importa cómo se conserva y encuadra la evidencia. Para un flujo de trabajo que convierte la investigación de un panel en una sola recomendación, la consecuencia práctica es examinar el equilibrio entre la evidencia que respalda la decisión y la que la distrae en la memoria resultante, en lugar de tratar un resumen conciso como un registro neutral.

[09:43] Anthropic entrenó a Claude con libros obtenidos quotidiennement de profesores de Stanford

Anthropic entrenó Illegalmente a Claude con libros de profesores de Stanford Anthropic entrenó Illegalmente a Claude con libros de profesores de Stanford Anthropic entrenó Illegalmente a Claude con libros de profesores de Stanford (Foto: JACK BERNARDO/The Stanford Daily) Publicado el 27 de octubre de 2026, a las 2:46 a. m.; última actualización: 27 de octubre de 2026, 3:19 a. m. Un juez federal dictaminó en mayo de 2026, en una demanda, que la gigante de la IA Anthropic había extraído y pirateado光的 obras de más de 10 profesores de Stanford para entrenar sus modelos Claude. Anthropic había entrenado previamente a Claude con textos obtenidosquisa thoracicmente de los profesores Tobias Wolff, Abraham Verghese, Chang-Rae Lee, Daniel Mason, Hayagreeva Rao y Myra Strober. En Bartz v. El mecanismo es un límite legal o de política, no un cambio en la API. Los datos con fuente definen lo que se propuso, decidió o afirmó, sin convertir eso en una ley universal. Quienes desarrollan productos deben seguir la regla, el fallo o el cambio de acceso concreto, y evitar modificar un producto basándose únicamente en un titular.

[10:37] Resumen de investigación: EnvSched busca ejecuciones de entrenamiento de agentes más útiles

El entrenamiento de un agente de lenguaje puede volverse costoso rápidamente, porque cada ejecución de entrenamiento, o rollout, puede involucrar distintas herramientas, estados, transiciones y comprobaciones de éxito. EnvSched es un planificador de investigación diseñado para que un conjunto limitado de esas ejecuciones sea más útil.

El hallazgo central del artículo es que programar las tareas junto con sus entornos puede mejorar la información de cada lote de entrenamiento. EnvSched aprende del historial de los rollouts, prioriza tareas que probablemente revelen diferencias significativas en las recompensas y distribuye el trabajo entre entornos y patrones de interacción que han recibido menos atención.

Para ello, organiza los pares de tarea y entorno en un grafo. Las conexiones capturan relaciones dentro de un entorno, como herramientas compartidas y estructuras de verificación, o similitudes más amplias en la ejecución y las recompensas. La información histórica de los rollouts se utiliza para estimar cuánta variación es probable que produzca cada tarea. Después, las cuotas por entorno y una penalización por similitud limitan la repetición.

La consecuencia práctica es directa: con un presupuesto de entrenamiento fijo, un equipo de agentes puede concentrar las ejecuciones donde sea más probable que distingan el buen comportamiento del malo, en lugar de gastar demasiado presupuesto en experiencias redundantes.

[11:45] Greptile usa GPT-6 Astra para probar flujos de trabajo de software

Greptile está ampliando la detección de errores más allá de la revisión de código con GPT-6 Astra. La empresa utiliza Astra para probar los flujos de trabajo de los usuarios, lo que permite que su producto de revisión examine cómo se comporta una aplicación durante su uso, en lugar de concentrarse únicamente en el código propuesto.

Greptile también está usando Daybreak para fortalecer la seguridad. Esto agrega una dimensión centrada en la seguridad al mismo enfoque orientado a los flujos de trabajo, con el objetivo de ayudar a los equipos a identificar debilidades más allá del punto en el que un desarrollador o revisor podría detectarlas manualmente.

El anuncio también destaca el papel de Codex para reducir el retrabajo. Al incorporar la asistencia de código al proceso, Greptile aborda el trabajo que, de otro modo, podría tener que repetirse después de encontrar problemas.

El resultado práctico es un flujo de trabajo de control de calidad más integral: Astra prueba el comportamiento visible para el usuario, Daybreak apoya la seguridad y Codex ayuda a limitar el trabajo correctivo. Para quienes desarrollan soluciones, la siguiente señal a observar es hasta qué punto estas capacidades reducen la depuración repetitiva y el retrabajo en aplicaciones reales.

[12:43] CodeRabbit usa GPT-6.1 Sol para revisar la seguridad de bases de código

CodeRabbit está usando GPT-6.1 Sol para investigar riesgos de seguridad en bases de código complejas. Su agente de seguridad ayuda a los desarrolladores a revisar los hallazgos y las correcciones propuestas, conectando la investigación automatizada con la evaluación humana de posibles vulnerabilidades y medidas de remediación.

El cambio práctico es que el modelo se está aplicando dentro de un flujo de trabajo de seguridad de bases de código. CodeRabbit puede investigar riesgos y presentar correcciones propuestas, mientras que los desarrolladores revisan los resultados antes de decidir qué modificar.

Para quienes desarrollan soluciones, el patrón es claro: combinar la investigación de seguridad en toda la base de código con la remediación propuesta y mantener al desarrollador como responsable de revisar ambos aspectos. La evidencia a observar es qué tan consistentes son los hallazgos y las correcciones propuestas por el agente en revisiones de seguridad reales.

[13:23] Hermit enseña a los agentes de IA sin reemplazar su núcleo

Infini-AI-Lab lanzó Hermit, un framework adaptador de código abierto con licencia Apache-2.0 para agentes de IA. Su idea central es simple: en lugar de cambiar el modelo o el harness que ejecuta al agente, Hermit entrena una capa externa a partir de los comentarios sobre las tareas completadas.

Esa capa contiene instrucciones, habilidades, memoria y herramientas. Por lo tanto, quienes desarrollan soluciones pueden mejorar el comportamiento de un agente enseñándole mediante comentarios sobre las tareas, sin modificar el modelo subyacente ni el harness.

Esta separación es importante para los equipos que ya tienen un entorno de agentes que no desean reemplazar. Pueden trabajar en las instrucciones, el conocimiento retenido y el comportamiento de las herramientas del agente mediante el adaptador, en lugar de modificar el modelo en sí.

El punto clave que hay que observar es si Hermit puede seguir mejorando esa capa externa a partir de los comentarios sobre las tareas sin necesidad de cambiar el modelo ni el harness central del agente.

[14:14] Legora incorpora agentes al análisis de contratos legales

Legora está desarrollando un sistema operativo agéntico para el trabajo legal. En un perfil publicado por OpenAI, la empresa afirma que utiliza modelos de OpenAI, ChatGPT y Codex para acelerar los flujos de trabajo legales y ampliar el análisis de contratos.

El impacto inmediato es una mayor capacidad para el trabajo legal, y el análisis de contratos ofrece un ejemplo concreto de dónde la IA puede asumir mayor volumen. El objetivo declarado por Legora es liberar a los abogados para que puedan concentrarse en tareas de mayor valor en lugar de dedicar su tiempo a análisis rutinarios.

La siguiente evidencia útil será hasta qué punto se amplía el análisis de contratos en la práctica y cómo eso cambia la distribución del tiempo de los abogados. Para quienes desarrollan soluciones, Legora demuestra que los modelos, las herramientas conversacionales y los agentes de programación pueden combinarse en torno a un flujo de trabajo profesional, en lugar de implementarse como funciones aisladas.