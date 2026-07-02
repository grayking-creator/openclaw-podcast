[NOVA]: Soy NOVA.

[ALLOY]: Soy ALLOY, y esto es AgentStack Daily...

[NOVA]: OpenClaw 6.11 corrigió respuestas mal ubicadas, envíos trabados, reconexiones caídas, fallos de configuración del modelo, comportamiento de compactación de sesión, y valores de administrador más seguros en canales, sesiones, proveedores, la interfaz de control y la interfaz de terminal.

[ALLOY]: El agente de codificación basado en terminal OpenAI Codex .142.5 estrechó el registro de trazas al impedir que las cargas completas de solicitudes Responses WebSocket lleguen a la salida de trazas, lo cual importa en cualquier lugar donde la telemetría de Codex fluya hacia sistemas de observabilidad compartidos.

[NOVA]: Claude Fable 5 está nuevamente disponible de forma general después de que Washington levantó las restricciones sobre los modelos Mythos y Fable de Anthropic el 30 de junio, y el listado en OpenRouter está activo con una ventana de contexto de un millón de tokens, soporte para texto, imágenes, entrada de activos subidos, y razonamiento.

[ALLOY]: Hoy: OpenClaw y Codex lideran la lectura de lanzamientos, Claude Fable 5 regresa como el nivel superior de clase Mythos por encima de Opus, Claude Sonnet 5 trae un dial de razonamiento de cuatro niveles a OpenRouter, y Google agrega Nano Banana 2 Lite para generación rápida de imágenes.

[NOVA]: Escucharás dónde se ubica Fable 5 contra GPT-5.5 en la frontera actual, cómo Fable encadena trabajo de múltiples pasos a partir de un solo prompt, por qué el paper de world-latent de Orca está llamando la atención, cómo Agents-A1 claims un rendimiento de agente de clase trillion-parametric de un estudiante de mezcla de expertos de 35B, y por qué OmniRoute, BlockPilot, composición generativa de habilidades, y TRIAGE importan para stacks de agentes en producción.

[NOVA]: ...

[ALLOY]: Dos lanzamientos estables de agent-harness aterrizaron. OpenClaw 6.11 es una pasada de confiabilidad en los lugares donde las sesiones de agente suelen sentirse frágiles: entrega de canales, reconexiones, configuración de modelo, valores de administrador, y recuperación después de problemas con proveedores. El lanzamiento apunta a Telegram, WhatsApp, Matrix, Google Chat, iMessage, Feishu, Mattermost, WebChat, la interfaz de control, y la interfaz de terminal. En uso concreto, los mensajes directos más nuevos de Google Chat dejan de leerse mal como conversaciones grupales, los usuarios de webhook de Telegram siguen recibiendo mensajes directos y grupales a través de reinicios y recargas de configuración, y los gateways cifrados de Matrix evitan el crecimiento de memoria de larga duración que puede sacar canales fuera de línea.

[NOVA]: El trabajo de runtime importa porque el agente no solo responde una vez; tiene que mantener una sesión viva mientras los canales se reconectan, los proveedores fallan, el contexto se compacta, y los humanos siguen enviando instrucciones. OpenClaw ahora usa un timeout de compactación por defecto de 180 segundos mientras sigue respetando la configuración explícita, preserva la propiedad de compactación del motor de contexto de Codex, y mantiene el estado del ciclo de vida de fallos de proveedor correcto. Las verificaciones de latido con capacidad de razonamiento también dejan de filtrar el razonamiento interno a Telegram y WhatsApp, mostrando la respuesta pretendida del asistente en su lugar.

[ALLOY]: OpenAI Codex .142.5 es mucho más estrecho, pero el parche tiene peso operacional real. Codex deja de escribir cargas completas de solicitudes Responses WebSocket en los logs de trazas. Eso no es un titular de característica; es una corrección de higiene de datos para equipos que canalizan trazas de Codex hacia monitoreo compartido, revisión de incidentes, o búsqueda de logs alojados. El agente de codificación basado en terminal todavía puede ser observado, pero el cuerpo de solicitud crudo ya no se convierte en telemetría accidental.

[NOVA]: Juntos, estos lanzamientos hacen que la capa de harness sea más fácil de cablear, desplegar y operar. OpenClaw estrecha la entrega y recuperación en canales orientados a humanos; Codex estrecha lo que sale del runtime del agente durante la depuración. La ganancia práctica es confiabilidad sin cambiar cómo los constructores configuran sesiones, enrutan canales, conectan proveedores, o envían observabilidad alrededor del agente.

[NOVA]: ...

[ALLOY]: Claude Fable 5 está nuevamente disponible de forma general. En la frontera pública, el nivel superior es Claude Mythos 5, Claude Fable 5, y OpenAI GPT-5.5. Mythos 5 es el más fuerte de los tres pero permanece tras una lista de organización aprobada. Fable 5 es el mismo modelo subyacente con salvaguardas adicionales para capacidades de doble uso, y es la versión que el enrutamiento de API ordinario puede alcanzar. GPT-5.5 se ubica justo detrás de ese par. Fable 5 es generalmente considerado el mejor modelo al que puedes enrutar hoy.

[NOVA]: Lo que hace que Fable 5 se sienta diferente es el encadenamiento con un solo prompt. Dale a Fable un mensaje de usuario con varias instrucciones independientes y el modelo descompone el trabajo por sí solo: identifica cada subtarea, planea un orden, las ejecuta en secuencia, y devuelve un resultado que ya tiene en cuenta las dependencias entre ellas. Los modelos de frontera más antiguos necesitaban que el orquestador dividiera el prompt, llamara al modelo una vez por instrucción, y uniera las respuestas nuevamente. Fable 5 hace esa descomposición internamente.

[ALLOY]: La forma de despliegue lo soporta. El listado en OpenRouter expone una ventana de contexto de un millón de tokens, entrada de texto e imagen más activos de proyecto subidos, salida de texto, y soporte de razonamiento. Anthropic lo posiciona para trabajo autónomo de conocimiento y codificación. OpenClaw ya cableó el soporte del proveedor Claude Fable 5 a mediados de junio, así que la integración del lado del harness precede a la reopenición de la ventana de disponibilidad.

[NOVA]: ...

[ALLOY]: Claude Sonnet 5 es el segundo nuevo listado de Anthropic en OpenRouter este ciclo, y la comparación práctica es contra Fable 5 en lugar de versiones más antiguas de Sonnet. Sonnet 5 se envía con la misma ventana de contexto de un millón de tokens que Fable 5 y expone pensamiento adaptativo a través de cuatro niveles de esfuerzo seleccionables: bajo, medio, alto, y máximo. La forma es la misma que Fable 5 en contexto y razonamiento, la diferencia es la profundidad por solicitud y el costo por token de pedirlo.

[NOVA]: El pensamiento adaptativo es el titular. Donde Fable 5 elige la profundidad de razonamiento internamente como parte de su comportamiento de encadenamiento, Sonnet 5 expone ese dial al que llama. Un turno de planificación puede pedir esfuerzo máximo, un turno de formateo puede quedarse en bajo, y un orquestador puede enrutar razonamiento costoso solo donde el trabajo paga. El endpoint es alcanzable como anthropic/claude-sonnet-5 en OpenRouter, servido por Anthropic, con entrada de texto e imagen y salida de texto.

[ALLOY]: En el ranking actual de la frontera, Sonnet 5 se ubica un nivel por debajo de Fable 5 en capacidad bruta pero por delante de la clase más antigua de Sonnet 4 y la mayoría de endpoints de peso abierto en cargas de trabajo de agentes de codificación. Los constructores que estaban enrutando sus sesiones más pesadas a través de valores por defecto de clase Opus ahora pueden alcanzar un Sonnet de forma Mythos con un dial de esfuerzo ajustable, lo cual cambia el cálculo de costos en sesiones de agente largas sin sacrificar la superficie de contexto largo.

[NOVA]: Vale la pena observar si los clientes de router presentan el control de esfuerzo de cuatro pasos de forma clara. El valor depende de que el comportamiento por solicitud sea consistente entre el SDK propio del proveedor y el paso a través de OpenRouter, no solo en el listado del catálogo.

[NOVA]: ...

[ALLOY]: Google listó Nano Banana 2 Lite en OpenRouter bajo la marca Gemini 3.1 Flash Lite Image. Se presenta como el modelo de imágenes Gemini más rápido y eficiente en costos de Google, construido para pipelines de desarrolladores de alta velocidad y exploración visual rápida en lugar de máxima fidelidad visual.

[NOVA]: El listado expone una ventana de contexto de 65,536 tokens y un endpoint de generación de texto a imagen. El nivel Flash-Lite te indica el compromiso esperado: inferencia más pequeña y rápida con mejor economía por unidad, no la calidad de renderizado más pesada de clase Pro. Eso lo hace ideal para ideación en masa, variaciones de mockups de productos, miniaturas, estados de interfaz, conceptos publicitarios, y cualquier flujo de trabajo que necesite muchas imágenes baratas como candidatas antes de que un humano o un modelo más pesado elija a los ganadores.

[ALLOY]: En el ranking de modelos de imagen, Nano Banana 2 Lite se encuentra por debajo de los endpoints de clase Imagen y Pro de Gemini en calidad visual bruta, pero muy por encima de la mayoría de los modelos de imagen abiertos ligeros en adherencia a prompts y seguimiento de instrucciones. OpenRouter hace que el ángulo de integración sea directo. Si un stack de agente de imágenes ya enruta a través de la plataforma, el nuevo endpoint de Google puede seleccionarse con un cambio de string de modelo. El resto del pipeline puede mantener la misma forma de solicitud, wrapper de moderación, constructor de prompts y manejo de resultados.

[NOVA]: La advertencia es la calidad. Flash-Lite está construido para recibir golpes, no para ganar cada comparación estética. Los constructores que usan la generación de imágenes como una subrutina de alto volumen ahora tienen una opción nativa de Google; los renders finales críticos para la marca todavía pertenecen a un modelo más pesado.

[NOVA]: ...

[ALLOY]: Orca, trending en HuggingFace Daily Papers con 161 votos positivos, propone un espacio latente mundial unificado construido a través de predicción multimodal del próximo estado. El objetivo de entrenamiento es la contribución real del artículo: alimentar el modelo con observaciones multimodales del mundo y pedirle que prediga el próximo estado, lo que fuerza a un espacio latente compartido a codificar la dinámica del mundo en lugar de características por dominio.

[NOVA]: Los autores luego prueban esa representación en tareas posteriores y reportan superar líneas base especializadas que fueron entrenadas por dominio. Un espacio latente general que supera a los modelos mundiales específicos por dominio es inusual; ese es la señal de los 161 votos positivos. El identificador de arXiv es 2606.30534, la página del proyecto está alojada en el sitio del modelo mundial orca en GitHub.

[ALLOY]: El mecanismo detrás del resultado es la pérdida del próximo estado. Predecir el próximo estado desde una entrada multimodal requiere que el espacio latente capture consecuencias de acciones, persistencia a través del tiempo y alineación multimodal a la vez. Los modelos mundiales especializados por dominio solo necesitan capturar su propia porción. El argumento de Orca es que el objetivo conjunto produce una representación que se transfiere, y los benchmarks son la prueba.

[NOVA]: Para los constructores que planean pipelines agentivos o encarnados, la señal práctica es que el pre-entrenamiento general de modelos mundiales se está convirtiendo en una alternativa creíble a los stacks específicos por tarea. La implicación más amplia: un espacio latente mundial compartido puede cambiar el cálculo de costos lejos del ingeniería de características por dominio en los próximos 12-18 meses, lo cual vale la pena seguir para cualquier equipo que construya simuladores, agentes encarnados o planificadores de estado persistente.

[NOVA]: ...

[ALLOY]: InternScience's Agents-A1 es un modelo agentivo de mezcla de expertos de 35 mil millones de parámetros que reclama resultados de clase de billones de parámetros a través de escalamiento de trayectorias de largo alcance y escalamiento de habilidades de agentes heterogéneos. El artículo está trending en el feed diario de HuggingFace con 73 votos positivos, y la atracción es la receta, no solo el conteo de parámetros.

[NOVA]: Las corridas de entrenamiento tienen tres etapas. Primero, el ajuste fino supervisado en trazas de agentes largos le enseña al modelo comportamiento extendido de múltiples turnos en lugar de movimientos aislados de prompt-respuesta. Segundo, los maestros por dominio se especializan a través de capacidades como codificación, uso de herramientas y recuperación. Tercero, la destilación multi-maestro fusiona esos especialistas en un solo estudiante MoE de 35B.

[ALLOY]: En los benchmarks agentivos, Agents-A1 reporta números que se acercan a modelos propietarios de billones de parámetros en suites de uso de herramientas de largo alcance mientras se ejecuta al costo de servir un MoE de 35B. Esa brecha entre capacidad y costo de despliegue es el punto del artículo. Si la receta se replica fuera del entorno de evaluación de los autores, la historia del presupuesto para servir agentes frontier cambia de "necesitas un cluster de hyperscaler" a "necesitas un solo host MoE de 35B".

[NOVA]: La prueba independiente todavía tiene que llegar. Observa los pesos abiertos, la replicación de benchmarks y la evidencia de que las ganancias de largo alcance sobreviven fuera del entorno de evaluación de los autores. Pero la dirección es importante: el comportamiento agentivo frontier puede venir cada vez más de la calidad de las trayectorias y la composición de maestros, no solo de la escala bruta.

[NOVA]: ...

[ALLOY]: OmniRoute, un gateway de IA de código abierto, llegó a GitHub Trending al colapsar 231 proveedores de modelos en un solo endpoint compatible con OpenAI, con aproximadamente 50 proveedores ofreciendo niveles gratuitos. Está diseñado para sentarse entre los agentes de codificación y las APIs de modelos upstream, incluyendo Cursor, Cline, Copilot, Codex y el agente de codificación basado en terminal Claude Code.

[NOVA]: El mecanismo es un plano de enrutamiento más compresión. OmniRoute aplica un pipeline de compresión de tokens apilado, modo RTK más modo Caveman, antes de que los prompts lleguen a los proveedores upstream. El autor reclama reducciones de uso del 15% al 95%, dependiendo de la carga de trabajo. Una capa inteligente de fallback automático reenruta solicitudes fallidas o con límite de tasa a otro proveedor en lugar de dejar que el agente se quede colgado.

[ALLOY]: La compatibilidad con MCP y A2A mantiene en juego las llamadas de herramientas y los mensajes de agente a agente, mientras que las superficies de Escritorio y PWA facilitan operarlo como un gateway local en lugar de un servicio solo en la nube. El ángulo de integración es directo: una sola URL base compatible con OpenAI puede reemplazar el cableado proveedor por proveedor, permitiendo a los equipos configurar un gateway y desplegar agentes a través de upstreams pagos y gratuitos.

[NOVA]: Las compensaciones a vigilar son la latencia, la calidad de compresión y la política de fallback. Si la compresión afecta la fidelidad del prompt o el fallback salta a proveedores más débiles en el momento incorrecto, los agentes pueden desviarse. Pero para bucles de codificación largos que rutinariamente alcanzan límites, una gateway que abarque proveedores pagos y gratuitos es un plano de control práctico.

[NOVA]: ...

[ALLOY]: BlockPilot, trending en HuggingFace Daily Papers con 64 votos positivos, propone aprendizaje de política adaptativa por instancia para decodificación especulativa basada en difusión. En lugar de usar un tamaño de bloque fijo para cada prompt, el método predice cuántos tokens debe producir el redactor de difusión por paso.

[NOVA]: La red de políticas lee estados ocultos de la etapa de prefilling y produce un tamaño de bloque por solicitud. Luego el redactor de difusión genera esa cantidad de tokens antes de que el modelo objetivo los verifique. Los horarios estáticos gastan el mismo presupuesto de borrador en prompts fáciles y difíciles; BlockPilot condiciona la profundidad de especulación en cómo se ve realmente el prompt.

[ALLOY]: Los autores reportan mejoras significativas de velocidad sobre enfoques de tamaño de bloque estático con sobrecarga mínima, y el grupo AMAP-ML publicó la implementación y la política entrenada junto con el preprint. Eso importa porque la técnica busca mejorar la eficiencia de inferencia sin reentrenar el modelo objetivo.

[NOVA]: Para equipos que ya usan decodificación especulativa, el tamaño de bloque pasa de ser un control de despliegue a una decisión de tiempo de ejecución aprendida. La pregunta abierta es la generalización: si la política publicada se transfiere entre familias de modelos o principalmente funciona dentro de la distribución de entrenamiento usada en el artículo.

[NOVA]: ...

[ALLOY]: Xinyu Zhao, Zhen Tan y Vaishnav Tadiparthi presentan la composición de habilidades como un cuello de botella creciente para agentes LLM. A medida que las bibliotecas de habilidades procedimentales se expanden, dos enfoques comunes comienzan a fallar: volcar cada habilidad en el contexto quema tokens, mientras que la recuperación por embedding puede perder combinaciones útiles entre habilidades.

[NOVA]: El artículo propone composición generativa de habilidades. En lugar de recuperar una habilidad fija o exponer la biblioteca completa, el modelo sintetiza una combinación bajo demanda para la tarea. La selección de habilidades se convierte en generación, no en clasificación. El agente razona sobre cómo combinar procedimientos en lugar de tomar la coincidencia más cercana de un catálogo.

[ALLOY]: Ese cambio se alinea con cómo maduran los stacks de agentes. Los sistemas tempranos pueden sobrevivir con un puñado de herramientas y recuperación simple. Los sistemas más grandes acumulan habilidades de refactorización, habilidades de sandbox, habilidades de navegador, habilidades de build, habilidades de datos y habilidades de despliegue. La parte difícil se convierte en componerlas sin inflación de contexto.

[NOVA]: La conclusión para los constructores es que la estructura de la biblioteca de habilidades importa tanto como el tamaño de la biblioteca. Si la composición generativa supera las líneas base de recuperación, los runtimes de agentes futuros necesitarán un andamiaje que ayude a los modelos a sintetizar procedimientos seguros y relevantes a partir de piezas más pequeñas.

[NOVA]: ...

[ALLOY]: TRIAGE añade asignación de crédito por rol al aprendizaje por refuerzo agéntico. El GRPO estándar a menudo aplica un resultado final del verificador como ventaja uniforme a través de cada token de acción en un rollout, así que los pasos de búsqueda, clic, edición, navegación e interacción con objetos reciben todos el mismo señal de aprendizaje.

[NOVA]: TRIAGE inserta un juez estructurado entre el rollout y la actualización de gradiente. El juez etiqueta cada segmento del rollout por rol semántico antes de que se compute la ventaja, haciendo que la actualización sea condicional al rol en lugar de plana. Eso cambia la asignación de crédito sin cambiar la función de recompensa en sí.

[ALLOY]: Las ganancias reportadas se concentran en rollouts con uso intensivo de herramientas, lo cual tiene sentido. En trayectorias largas de agentes, solo algunas acciones決定an el resultado. Un paso de búsqueda útil dentro de un rollout fallido no debería ser castigado de la misma manera que una acción sin salida, y los clics redundantes dentro de un rollout exitoso no deberían ser reforzados solo porque la respuesta final pasó.

[NOVA]: Para equipos que entrenan políticas de agentes con RL, TRIAGE dirige la atención hacia la ponderación de acciones. La calidad del verificador sigue importando, pero el uso intensivo de herramientas necesita crédito más nítido. El modelo juez se convierte en el punto de presión, porque las etiquetas de rol tienen que ser lo suficientemente consistentes para mejorar el aprendizaje en lugar de agregar varianza.

[NOVA]: ...

[ALLOY]: PrefectHQ fastmcp es un framework Pythonic para construir servidores y clientes de Model Context Protocol. Da a los desarrolladores ergonomía estilo FastAPI para declarar herramientas, recursos y prompts, para que los agentes puedan descubrir capacidades tipeadas a través de MCP en lugar de llamadas de función ad-hoc.

[NOVA]: El ángulo de integración es limpio: inserta fastmcp en un stack adyacente a Hermes, Codex, OpenClaw o Claude Code cuando los servicios internos necesitan convertirse en herramientas validadas por schema. En lugar de escribir manualmente la plomería de JSON-RPC, los equipos pueden exponer operaciones tipeadas con interfaces inspeccionables y dejar que los clientes compatibles con MCP los descubran.

[ALLOY]: Eso importa porque la adopción de MCP se está moviendo de demos a cableado de producción. Un framework que hace que las declaraciones de herramientas se sientan como código de servicio Python ordinario reduce el costo de convertir APIs internas en superficies listas para agentes.

[NOVA]: ...

[NOVA]: DeusData codebase-memory-mcp es un binario estático único que indexa un repositorio en un grafo de conocimiento persistente y responde consultas estructurales en 158 idiomas. El proyecto promete búsquedas estructurales en sub-milisegundos y aproximadamente un 99% menos de tokens que volver a alimentar código fuente sin procesar a un modelo.

[ALLOY]: La integración va debajo de los agentes de código. Móntalo como la capa de recuperación de código de larga duración para OpenClaw, Codex, o cualquier cliente compatible con MCP, y las preguntas de navegación pueden resolverse contra el grafo en lugar de activar nuevos embeddings o llenado extenso de contexto en cada turno.

[NOVA]: La ganancia concreta es latencia más disciplina de tokens. Un agente de código que puede preguntar dónde está definido un símbolo, cuáles sitios de llamada lo tocan, o cómo se conectan los módulos obtiene una respuesta compacta antes de decidir qué editar, compilar o desplegar.

[NOVA]: ...

[ALLOY]: El mcp-for-beginners de Microsoft es un currículo multilingüe para el Model Context Protocol, con ejemplos prácticos en C#, Java, TypeScript, JavaScript, Rust y Python. Se enfoca en patrones cliente-servidor prácticos para flujos de trabajo de agentes modulares, escalables y seguros.

[NOVA]: El ángulo de integración es la habilitación de equipos. Si un stack tiene un runtime en Python, otro en TypeScript, y un equipo de servicio en Java o C#, los ejemplos le dan a cada grupo una ruta nativa a MCP sin forzar una elección de lenguaje.

[ALLOY]: Las piezas útiles no son solo herramientas hello-world. Las lecciones cubren patrones alrededor de límites cliente-servidor, autenticación y exposición de herramientas con alcance, que son exactamente las partes que determinan si un agente puede llamar de forma segura capacidades de producción.

[NOVA]: ...

[NOVA]: Claude Fable 5 se selecciona porque la disponibilidad regresó este ciclo. En el ranking actual de frontera, se encuentra en la cima del nivel generalmente disponible junto a GPT-5.5, compartiendo paridad de modelo subyacente con Mythos 5 además de salvaguardas adicionales de doble uso, y saliendo con el comportamiento de encadenamiento de prompt único que lo distingue de endpoints de frontera más antiguos. Es accesible a través de OpenRouter en anthropic/claude-fable-5, tiene una ventana de contexto de un millón de tokens, soporta entrada de texto, imagen y activos cargados, y salida de texto, y trae soporte de razonamiento. El camino de evaluación inmediato es una sesión de agente de código o investigación autónoma contra los valores predeterminados actuales de clase Opus, enfocado en si el comportamiento de encadenamiento reduce el trabajo de planificación a nivel de orquestador.

[ALLOY]: Claude Sonnet 5 se selecciona porque es un nuevo listado de modelo de proveedor principal con ventana de contexto de un millón de tokens y esfuerzo de razonamiento seleccionable. El ángulo práctico es enrutar una sesión de código o agente a través de Sonnet 5 y comparar esfuerzo bajo, medio, alto y máximo en latencia, costo y calidad de completitud, especialmente para sesiones donde Fable 5 es muy caro.

[NOVA]: Google Nano Banana 2 Lite se selecciona porque agrega un endpoint de imagen de proveedor principal optimizado para velocidad y costo. Expone una ventana de contexto de 65.536 tokens y generación de texto a imagen a través de OpenRouter, haciéndolo útil para exploración visual de alto volumen y generación masiva de activos.

[ALLOY]: No hubo entradas de modelos no seleccionados en la verificación de descubrimiento.

[NOVA]: ...

[NOVA]: Ollama .31.1 trae una aceleración majeure en Apple Silicon para Gemma 4 al apoyarse en predicción multitoken. En lugar de generar un token por pasada hacia adelante, MTP redacta varios tokens y los verifica en paralelo.

[ALLOY]: El lanzamiento mantiene el flujo de trabajo local de un solo binario y los contratos de API existentes, así que el cambio interesante es rendimiento en lugar de rotación de integración. En un benchmark de agente de código, la generación se reporta aproximadamente 90% más rápida en hardware de la serie M.

[NOVA]: El ángulo práctico es asistencia de código local en una Mac de la serie M. Descarga Gemma 4, ejecuta un prompt de completación de código a través de Ollama, y compara tokens por segundo contra una versión .30 más antigua para ver si la ganancia de MTP aparece en tu propia máquina.

[NOVA]: ...

[ALLOY]: El repo Anthropic-Cybersecurity-Skills empaqueta 817 habilidades de ciberseguridad estructuradas para agentes de IA, mapeadas a través de MITRE ATT&CK, NIST CSF, MITRE ATLAS, D3FEND, NIST AI RMF y el marco de lucha contra el fraude de MITRE.

[NOVA]: Cada habilidad se entrega como un manifest estilo agentskills.io, dando a los agentes una taxonomía fija a través de 29 dominios de seguridad. Eso lo hace relevante para stacks de agentes de seguridad que necesitan procedimientos controlados en lugar de improvisación libre de herramientas. La pregunta útil es si la taxonomía mejora la calidad de despacho cuando un agente tiene que elegir entre flujos de trabajo de reconocimiento, defensa, fraude y riesgo de IA.

[NOVA]: ...

[ALLOY]: AxDafny estudia la generación de código verificado agentivo en Dafny, donde un modelo tiene que generar tanto código ejecutable como el material de prueba necesario para la verificación.

[NOVA]: El framework ejecuta reparación guiada por verificador. El verificador basado en SMT de Dafny detecta invariantes fallidos, aserciones y argumentos de terminación, luego el LLM propone la siguiente reparación. Ese ciclo le da al agente contraejemplos concretos en lugar de comentarios vagos. Para los constructores que trabajan en generación de código de alta garantía, AxDafny muestra cómo un verificador puede convertirse en el canal de retroalimentación más estricto del agente.

[NOVA]: ...

[ALLOY]: Surrogate Fidelity pregunta cuándo los LLMs abiertos pueden explicar a los cerrados. La interpretabilidad mecanicista generalmente necesita acceso interno, pero los modelos cerrados ampliamente desplegados exponen solo señales limitadas de API, a menudo probabilidades de tokens.

[NOVA]: El artículo trata los modelos de peso abierto como sondas de medición. Usa log-odds de tareas binarias como escalares compatibles con API y atribución leave-one-out para probar cuándo las afirmaciones mecanicistas se transfieren entre once modelos. El ángulo de integración es la precaución en la evaluación: un sustituto abierto puede ayudar a explicar un modelo cerrado solo cuando las condiciones de transferencia se miden, no se asumen.

[NOVA]: ...

[ALLOY]: OpenClaw 6.11 optimiza la entrega de canales y la recuperación de sesiones, mientras que Codex .142.5 reduce la exposición de logs de trazas del tráfico de Responses WebSocket.

[NOVA]: Claude Fable 5 regresa como la cima de la frontera disponible en general junto con GPT-5.5, con acceso a router, contexto de un millón de tokens, entrada multimodal, razonamiento y encadenamiento de prompts únicos para trabajo multi-instrucción.

[ALLOY]: Claude Sonnet 5 agrega un endpoint Sonnet de un millón de tokens con esfuerzo de razonamiento por solicitud entre bajo, medio, alto y máximo.

[NOVA]: Nano Banana 2 Lite le da a los pipelines de agentes de imagen una ruta de Google más rápida y económica para generación de alto volumen.

[ALLOY]: Orca, Agents-A1, BlockPilot, composición generativa de habilidades y TRIAGE todos empujan las pilas de agentes hacia mejores representaciones, comportamiento más económico de largo horizonte, inferencia más rápida, composición procedural más fuerte y crédito de RL más nítido.

[NOVA]: fastmcp, codebase-memory-mcp y mcp-for-beginners muestran a MCP madurando hacia una capa de integración práctica para herramientas tipadas, conocimiento de código base y servicios de agentes multi-lenguaje.

[ALLOY]: Ollama .31.1 hace más rápidos los flujos de trabajo locales de codificación con Gemma 4 en Apple Silicon a través de predicción multi-token.

[NOVA]: Para los detalles de origen de cada elemento, mira las notas del programa en Toby On Fitness Tech punto com.

[ALLOY]: Gracias por escuchar AgentStack Daily. Volveremos pronto.