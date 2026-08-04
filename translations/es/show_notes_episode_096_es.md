Episodio 096 — 31 de julio de 2026

[00:00] Gancho del episodio

Lectura del Lanzamiento de Agent Stack: Hermes Agent v2026.7.30 lidera el día: v2026.7.30 trae cambios concretos a las superficies que los builders ejecutan todos los días, con los detalles a continuación. También en la cartelera de hoy: Gemini Robotics 2 trae inteligencia de cuerpo completo a los robots, GitHub Models Retirado: Playground, API y BYOK Desaparecen, Kimi K3 de Moonshot llega como una versión local-AI cuantizada, además del resto de un ciclo de noticias denso en modelos, herramientas e infraestructura. Cada historia recibe el mismo tratamiento — qué se lanzó, el mecanismo debajo y qué cambia para los builders que trabajan.

[02:00] Lectura del Lanzamiento de Agent Stack: Hermes Agent v2026.7.30

Un lanzamiento estable llegó en este ciclo, dando forma a cómo se están ensamblando los arneses agenticos ahora mismo. Hermes Agent v2026.7.30: Fecha de lanzamiento: 30 de julio de 2026 > Lanzamiento de parche. Esta etiqueta agrupa los ~1,000+ PRs fusionados desde v0.19.0 en un lanzamiento estable etiquetado para consumidores downstream (imágenes Docker, despliegues hospedados, instalaciones nuevas). Desde (v0.19.0, 20 de julio): ~2,789 confirmaciones · ~4,748 archivos cambiados · ~442,000 inserciones · ~392,300 eliminaciones en main. Esta ventana está dominada por oleadas de corrección de errores y salvación a través de la puerta de enlace, subsistema de voz, aplicación de escritorio e instalador, además de trabajo continuo en plataforma (canal Buzz/Nostr, generación y entrega de video FLUX3, confiabilidad de medios de Telegram, regresiones del modo de voz). Las notas de lanzamiento completas curadas para esta ventana se enviarán con v0.20.0, que documentará todo desde v0.19.0 en adelante — aspectos destacados, áreas de características y créditos completos de colaboradores. Nada en esta ventana se omite. hermes update curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash Registro de cambios completo: [..v2026.7.30](https://github.com/NousResearch/hermes-agent/compare/..v2026.7.30) En la capa de API y runtime estos cambios alteran lo que los builders pueden configurar y depender por defecto; la pregunta para cualquier flujo de trabajo de agente en producción es si los nuevos valores por defecto mejoran o rompen el camino que has estado ejecutando esta semana. Las notas de lanzamiento completas para cada arnés — incluyendo la guía de despliegue, la lista de pull requests fusionados y los créditos de colaboradores — están vinculadas desde la fuente primaria, y el contexto del changelog para cada etiqueta es lo que los builders deben comparar contra su versión fijada actual antes de cambiar el valor por defecto en producción. Hermes Agent v2026.7.30, publicado el 30-07-2026, es una etiqueta estable: fíjalo explícitamente en lugar de seguir un canal móvil, reproduce una sesión de agente representativa contra la nueva construcción y compara la latencia de llamadas de herramientas, el comportamiento de reconexión y el manejo de aprobaciones con la versión que se está ejecutando actualmente antes de promover el nuevo valor por defecto.

[02:42] Gemini Robotics 2 trae inteligencia de cuerpo completo a los robots

DeepMind publicó Gemini Robotics 2 el 30 de julio, enmarcando el trabajo como traer 'inteligencia de cuerpo completo' a los robots. La afirmación principal es que un sistema puede ahora manejar percepción, planificación y uso de herramientas a través de todo un cuerpo de robot, en lugar de tratar brazos, pinzas y movimiento base como problemas separados. El lanzamiento es en realidad dos modelos: Gemini Robotics 2 y un compañero llamado Gemini Robotics ER 2. Según el blog, ER 2 es la variante construida para razonamiento, colaboración y resolución de tareas del mundo real. DeepMind señaló tres áreas concretas donde los nuevos modelos superan el trabajo anterior. Primero, comprensión de video: los modelos pueden observar demostraciones largas y elegir los pasos que importan. Segundo, orquestación de herramientas: en lugar de solo mover sus propios brazos, el robot puede decidir buscar un implemento diferente o llamar a un agente separado. Tercero, colaboración multi-robot: varios robots pueden dividir un trabajo sin que un humano coreografie cada transferencia. La publicación de DeepMind enmarca el trabajo alrededor de tareas del mundo real en lugar de selección y colocación en mesa. El hilo de Hacker News alcanzó una puntuación de 561 en un día, lo cual es inusualmente alto para un tema de robótica y sugiere que la comunidad de builders piensa que el trabajo está haciendo cosas reales esta vez.

[03:56] GitHub Models Retirado: Playground, API y BYOK Desaparecen

GitHub Models está retirado. A partir del 30 de julio de 2026, el playground, el catálogo de modelos, la API de inferencia y la opción de traer-tu-propia-clave ya no están disponibles para ningún cliente.

Para los desarrolladores, el impacto práctico es directo. Si usabas GitHub Models como una forma rápida de probar diferentes modelos en el navegador, ese punto de entrada desapareció. Si llamabas al endpoint de inferencia de GitHub Models desde tu código, ese endpoint desapareció. Si conectaste claves de proveedores externos a través del flujo BYOK para poder enrutar solicitudes a OpenAI, Anthropic u otros desde una única superficie del lado de GitHub, esa transferencia desapareció también.

La retirada es total en lugar de parcial. GitHub no está cerrando una pieza mientras mantiene el resto vivo; el playground, catálogo, inferencia y BYOK desaparecen juntos. Los clientes que trataron GitHub Models como una capa delgada de conveniencia sobre proveedores externos ahora tienen que hablar con esos proveedores directamente.

El siguiente paso razonable es migrar cualquier uso activo. Los SDKs de proveedores directos y las claves API reemplazan las rutas de inferencia y BYOK. La navegación de modelos se mueve al catálogo propio de cada proveedor o a directorios de terceros. Superficies de prototipado como el playground de OpenAI, la Consola de Anthropic o interfaces de chat específicas de proveedores cubren el caso de uso del playground.

Una cosa a observar: la publicación del changelog deja su cláusula de alcance de cliente truncada, por lo que no está claro si los clientes de nivel pago o empresarial reciben algún camino de continuación o acceso heredado. Si dependías de GitHub Models para un flujo de trabajo en producción, verifica si tus relaciones existentes con proveedores te permiten recoger las llamadas sin re-arquitectar.

[05:32] Las GPUs Inactivas Te Cuestan Dinero — Una Nueva Mirada a la Gestión de Flota

[07:13] Las GPUs Inactivas Te Cuestan Dinero — Una Nueva Mirada a la Gestión de Flota

Una nueva publicación en el blog de Hugging Face, publicada el 30 de julio por Dharma-AI, usa una metáfora de la aviación para argumentar sobre presupuestos: una GPU inactiva es como una aeronave en tierra — un activo que se deprecia y cuesta lo mismo tanto si vuela como si permanece en la pista.

El enfoque importa porque los equipos de IA tienden a presupuestar según la capacidad de cómputo bruta adquirida, no la capacidad de cómputo realmente consumida. La afirmación principal de la publicación es que el tiempo inactivo se ha convertido silenciosamente en el costo dominante para las organizaciones que operan más de un puñado de aceleradores, porque las GPU se deprecian por hora independientemente de la carga de trabajo.

Para los constructores, la conclusión es más conceptual que mecánica. El material disponible no documenta sistemas específicos de programación, políticas de recuperación o puntos de referencia de utilización, por lo que la evidencia útil es el enfoque mismo: tratar la capacidad de los aceleradores como una flota administrada, medir la utilización y diseñar trabajos que llenen los vacíos en lugar de reservar hardware indefinidamente.

Qué observar a continuación: si Dharma-AI complementa con herramientas concretas o casos de estudio que pongan cifras al argumento del costo por inactividad.

[08:16] Jetson como el accesorio 'de moda': Sarah Guo destaca la IA en el borde

NVIDIA puso esta semana un enfoque promocional en su plataforma Jetson de IA en el borde, y la empresa recurrió a una metáfora de la moda para hacerlo. La publicación, publicada el 28 de julio en el blog de NVIDIA bajo el título "Potente capacidad de cómputo tan compacta que es un clutch — Construye IA en cualquier lugar con NVIDIA Jetson," presenta a la inversora Sarah Guo en un video corto enmarcando el kit de desarrollo compacto como un "clutch" — el tipo de accesorio pequeño y elegante que cabe en tu mano y aun así llama la atención.

Guo dirige Conviction, una firma de capital de riesgo nativa de IA, y copresenta el podcast No Priors. En el video, destaca cómo Jetson funciona como plataforma para construcciones de IA en el borde.

Para los constructores, la idea subyacente es directa: "borde" significa que el modelo se ejecuta en el dispositivo mismo en lugar de hacer ping a un servidor remoto. Eso es lo que permite que un robot, cámara, dron o gadget portátil maneje inferencia localmente. El enfoque aquí tiene menos que ver con números de referencia brutos y más con cómo un inversor-operador como Guo habla de la IA en el borde cuando intenta convencer a otros fundadores de que es un objetivo de implementación real, no una demostración de investigación.

La publicación en sí tiene pocos detalles técnicos — no hay una nueva SKU, no hay lanzamiento de SDK, no hay precios, no hay registro de cambios de ningún tipo. Lo interesante es el mensajero: un capitalista de riesgo que respalda empresas nativas de IA respaldando una plataforma de hardware específica en el propio marketing de NVIDIA. Eso es una señal de hacia dónde piensa el capital que va la IA en el borde a continuación, y vale la pena ver rápidamente si estás evaluando API de nube contra inferencia en el dispositivo para una construcción futura.

[09:55] OpenAI describe su manual de IA responsable para Europa

El 31 de julio, OpenAI publicó un artículo titulado 'Avanzando hacia una IA responsable en Europa,' delineando cómo sus prácticas actuales apoyan la gobernanza responsable de la IA en el continente. La publicación agrupa el trabajo en cuatro áreas: seguridad, protección, transparencia y procedencia. OpenAI dice que estos esfuerzos continuarán ejecutándose junto con el AI Act de la UE a medida que la ley avance en sus fases de implementación.

Para los constructores, la señal práctica es que la procedencia, es decir, los metadatos que marcan las imágenes y textos generados por IA, y las divulgaciones de transparencia son cada vez más parte de la línea base europea. OpenAI está enmarcando sus prácticas existentes como el andamiaje para ese cumplimiento en lugar de introducir nuevos compromisos específicos para Europa en esta publicación. El artículo posiciona el trabajo como un programa continuo que sigue el despliegue del AI Act.

El AI Act de la UE se está implementando gradualmente con el tiempo, con diferentes obligaciones que entran en vigencia en diferentes horarios. La publicación de OpenAI señala una inversión continua en mantener sus divulgaciones de seguridad y protección alineadas con esas obligaciones a medida que se implementan. También apunta a la transparencia y procedencia como áreas donde los usuarios europeos pueden esperar ver más visibilidad sobre cómo se identifica y etiqueta el contenido generado por IA.

Qué observar a continuación: a medida que las disposiciones de mayor riesgo del AI Act entren en vigencia, espera requisitos de documentación más concretos sobre procedencia, documentación de modelos y divulgaciones de seguridad para cualquier sistema implementado en el mercado europeo.

[11:18] Resumen de investigación: PhiZero construye un 'lenguaje físico' para predecir cómo se mueve el mundo

PhiZero es un nuevo modelo de investigación que predice cómo se comporta el mundo aprendiendo un lenguaje físico, un vocabulario discreto y compacto de cambios de estado, en lugar de predecir píxeles de video sin procesar. Los modelos de mundo existentes tienden a representar cuadros futuros directamente, lo que deja la física subyacente enterrada dentro de un predictor visual de alta dimensión. Los autores de PhiZero argumentan que los humanos hacen algo diferente: observamos, abstraemos las reglas del movimiento y almacenamos esas reglas en representaciones similares al lenguaje sobre las que podemos razonar. PhiZero intenta reproducir ese truco aprendiendo tokens físicos de experiencia de video en exteriores, y luego usando esos tokens para hacer avanzar los estados del mundo. La esperanza práctica es un modelo que planee y razone sobre resultados más como una persona que como un generador de video. Es una preprint de investigación, no un producto, así que la conclusión es la idea: los tokens discretos para física pueden ser un sustrato más útil que los píxeles para modelos de mundo.

[12:13] Resumen de investigación: Frontis-MA1: Entrenando IA para mejorar el proceso de construir IA

Un equipo está probando si la IA puede mejorar significativamente el proceso de construir IA — y publicando el sandbox para que cualquiera pueda observar. El artículo presenta Frontis-MA1, un modelo de 35 mil millones de parámetros post-entrenado como agente de meta-evolución para ingeniería de aprendizaje automático. Los investigadores construyeron OpenMLE, una pila abierta que convierte la ingeniería de ML en un juego medible con retroalimentación de ejecución.

OpenMLE tiene tres capas. OpenMLE-Gym ejecuta entornos de tareas verificables donde los cambios propuestos realmente se ejecutan. OpenMLE-RL maneja el aprendizaje del operador — enseñándole al modelo cómo dirigir ediciones y búsquedas. OpenMLE-Evo ejecuta búsquedas de largo horizonte para que las mejoras puedan acumularse. Frontis-MA1 se sitúa encima, proponiendo cambios de ingeniería de ML y viendo cuáles realmente funcionan.

El titular no es que la IA se haya mejorado a sí misma — es que la auto-mejora recursiva ahora tiene un banco de pruebas concreto y abierto. La mayor parte del trabajo anterior se mantuvo teórico o vivió detrás de demostraciones cerradas; aquí el gym, el bucle de entrenamiento y el arnés de búsqueda son todos públicos, para que otros laboratorios puedan repetir o extender la misma configuración. El artículo está en tendencia en el feed diario de HuggingFace.

[13:15] Un recorrido por el árbol genealógico de las variantes de atención DeltaNet

Doubleword publicó un recorrido por su blog rastreando la familia de variantes de atención lineal de DeltaNet y argumentando, como dice su título, que Kimi Delta Attention es una extensión natural que un lector cuidadoso podría haber llegado por sí mismo. La publicación apareció en Hacker News el 28 de julio de 2026, generó una discusión de 297 puntos que se ha mantenido activa, y también apareció en la etiqueta de IA de Lobsters.

La publicación presenta el campo como un árbol genealógico en lugar de un puñado de trucos independientes. Su afirmación central es que las variantes de atención recientes parecen menos exóticas una vez que alineas sus predecesores, y que seguir la línea de descendencia es suficiente para predecir hacia dónde es probable que vaya la próxima.

Por qué importa ahora: los anuncios de modelos frontier siguen llegando con mecanismos de atención que parecen un salto de fe a primera vista, y la conclusión práctica para los ingenieros es que la línea de descendencia importa más que cualquier documento individual. Leer primero el árbol genealógico cambia cómo llega cada nueva variante.

Para los constructores que realmente quieren entender lo que está funcionando dentro de modelos como Kimi, la publicación es una útil rampa de entrada. Es una lectura de fin de semana, no un proyecto de investigación, y los hilos de Hacker News y Lobsters junto a ella complementan el contexto.

[14:31] Las habilidades de agente y el soporte MCP de Copilot Code Review llegan a GA

GitHub movió las habilidades de agente de revisión de código de Copilot y el soporte del servidor MCP a disponibilidad general el 29 de julio. Ambas capacidades ahora están abiertas para todos los usuarios de Copilot Pro, Pro+, Business y Enterprise, después de salir de la vista previa pública.

La publicación del changelog carece de detalles. MCP — el Model Context Protocol — es la forma estándar para que los asistentes de IA se conecten a herramientas y fuentes de datos externas. La publicación no define qué significan "habilidades de agente" en este contexto ni lista qué habilidades están incluidas. Tampoco detalla integraciones específicas de MCP, cambios de comportamiento, o qué deberían esperar los constructores diferente de la vista previa.

Para los constructores en los niveles de pago listados, el cambio es que estas características están listas para producción en lugar de ser vista previa. El nivel gratuito de Copilot no se menciona en el lanzamiento. La siguiente observación honesta es cómo los equipos realmente las configuran una vez que estén disponibles, pero el anuncio en sí es lo suficientemente delgado como que cualquiera que planifique un lanzamiento necesitará profundizar en los docs de GitHub en lugar de depender del changelog.

[15:33] La especificación MCP del 2026-07-28 se vuelve sin estado, promete sin eliminaciones repentinas

El Model Context Protocol, el estándar abierto que permite a los asistentes de IA conectarse a herramientas y fuentes de datos externas, recibió una actualización de especificación el 30 de julio. El cambio principal: la capa de transporte se vuelve sin estado, lo que significa que los servidores ya no necesitan mantener estado de sesión entre solicitudes del cliente. Junto con eso, el proyecto adoptó una nueva política que evita que las características se eliminen sin advertencia.

En términos simples, sin estado significa que cada solicitud es independiente en lugar de depender de una sesión recordada en el servidor. Para los constructores que ejecutan servidores MCP, eso cambia el diseño hacia conexiones más simples y predecibles — e igual de importante, elimina una clase de modos de falla que provienen de estados de sesión perdidos o caídos.

La política de deprecación es la mitad más silenciosa del lanzamiento pero tiene peso por sí sola. Las características del protocolo ahora pasarán por un ciclo de deprecación documentado con aviso antes de poder ser eliminadas, dando tiempo a los autores de servidores y clientes para migrar. Es el tipo de promesa de predictibilidad que ayudó a que los estándares web se calmaran, y responde directamente a una preocupación real de cualquiera que esté invirtiendo en integraciones MCP hoy.

La actualización se publicó en el blog de MCP el 30 de julio y generó atención rápida en Hacker News, donde alcanzó una puntuación de 127.

[16:52] avatarin lanza agente de voz retail 24/7 con GPT-Realtime

avatarin ha puesto a trabajar el GPT-Realtime de OpenAI como un agente de voz multilingüe 24/7 para compradores en Yamada Denki, un retailer de electrónica japonés. Los clientes pueden acercarse y hacer preguntas en su propio idioma, y el asistente responde en tiempo real.

Las primeras dos semanas produjeron números llamativos: 30,000 personas usaron el agente, y el 92% de las respuestas de encuestas volvieron positivas. Para un asistente de voz desplegado a escala de consumidor en un entorno retail ocupado, esa es una señal temprana significativa de que los modelos de voz en tiempo real pueden mantenerse bajo tráfico del mundo real.

GPT-Realtime es el modelo de voz a voz de OpenAI, lo que significa que el audio entra y el audio sale sin un paso separado de transcripción de texto en el medio. Esa ruta de voz directa es lo que hace posible una conversación fluida de ida y vuelta, y es la misma familia de capacidades que avatarin ahora ha dirigido a una carga de trabajo retail de alto volumen.

Para los constructores, la historia es un punto de datos concreto en lugar de un anuncio de características. Un agente de voz que sobrevivió 30,000 interacciones reales con compradores con comentarios abrumadoramente positivos está más cerca de estar listo para producción que de ser un demo. La cobertura multilingüe y la disponibilidad las 24 horas son diferenciadores obvios para un despliegue retail, y ambos parecen estar funcionando.

Una cosa que vale la pena observar: si avatarin y Yamada Denki expanden el alcance del agente más allá de preguntas sobre productos hacia devoluciones, quejas o ventas adicionales, donde las conversaciones se vuelven más difíciles y los números de satisfacción serán más difíciles de mantener.

[18:17] Google DeepMind lanza tres modelos de IA física para control de cuerpo completo, destreza y colaboración multi-robot

Google DeepMind ha lanzado Gemini Robotics 2, la capa de inteligencia para su próxima generación de robots. El lanzamiento incluye tres modelos: un modelo visión-lenguaje-acción para control de humanoides de cuerpo completo, Gemini Robotics ER 2 para razonamiento encarnado y orquestación de tareas, y un VLA en dispositivo que se adapta a nuevos cuerpos de robots en horas. Un checkpoint controla Apptronik Apollo 2 y un Franka Duo. Solo ER 2 está disponible públicamente. La publicación Google DeepMind Ships Three Physical AI Models For Whole Body Control, Dexterity And Multi Robot Collaboration apareció primero en MarkTechPost. La fuente primaria respalda el cambio específico de producto o flujo de trabajo indicado anteriormente; no respalda afirmaciones más amplias sobre rendimiento, compatibilidad o implementación. Pruebe el cambio respaldado por la fuente en un flujo de trabajo real antes de depender de él.