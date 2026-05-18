# OpenClaw Daily EP052: Los Agentes Locales Obtienen Su Semana de Hardware

Este episodio rastrea seis movimientos concretos en el stack de agentes. El centro de gravedad es la infraestructura local-first: ejecutores de modelos locales, aceleración Apple Silicon, DGX Spark como máquina para agentes locales, inferencia distribuida EXO, CLIs de agentes de codificación, y la capa de gateway que evita que el enrutamiento de modelos se vuelva frágil.

[00:00] Ollama evoluciona de ejecutor de modelos a plataforma de agentes de codificación

Los últimos lanzamientos de Ollama muestran que se está convirtiendo en más que un servidor de modelos local. Los puntos importantes son el soporte de Codex App a través de Ollama Launch, soporte de modelos de visión para el lanzamiento de opencode, correcciones de rutas de imágenes locales para resultados de herramientas de Claude, y almacenamiento en caché de respuestas de API show que mejora la latencia de carga de integración media en aproximadamente 6.7x.

El punto más importante orientado al futuro es el candidato de lanzamiento 0.30.0. Ollama dice que esa versión cambia la arquitectura para soportar directamente llama.cpp, permite compatibilidad con archivos GGUF, y usa MLX para acelerar la inferencia en Apple Silicon. El trabajo anterior de mayo también agregó decodificación especulativa Gemma 4 MTP en el ejecutor MLX, con más de 2x de aumento de velocidad reclamado para tareas de codificación Gemma 4 31B.

La lectura práctica: Ollama se está acercando a ser una capa de runtime local para agentes de codificación y herramientas de IA de escritorio. La portabilidad de modelos, la aceleración MLX, las llamadas de metadatos más rápidas, las integraciones de lanzamiento y las entradas de visión importan cuando un agente local tiene que hacer trabajo real de proyecto en lugar de solo responder prompts.

Fuentes:
- https://github.com/ollama/ollama/releases

[05:00] LM Studio mejora la inferencia de visión MLX y apunta hacia servidores locales compartidos

LM Studio 0.4.13 incluye mlx-engine v1.8.1. El changelog oficial dice que mejora significativamente el rendimiento y agrega predicciones paralelas para modelos con capacidad de visión incluyendo Qwen 3.5/3.6 y Gemma 4. La misma versión corrige el manejo de saltos de línea pegados e incluye endurecimiento de seguridad.

Eso suena pequeño hasta que lo pones junto a hacia dónde va LM Studio con máquinas más grandes. Su material de DGX Station describe un daemon headless, llmster, emparejado con LM Link para que una máquina pueda servir modelos locales a otros dispositivos. También menciona los SDKs de LM Studio, la API de LM Studio, y APIs compatibles con OpenAI y Anthropic.

La relevancia para constructores es directa: la IA local se está convirtiendo en un stack de dos partes. Una laptop o Mac puede ser la interfaz, mientras que una máquina local más grande maneja la carga del modelo. Para agentes de visión, las mejoras de predicción paralela MLX importan porque capturas de pantalla, imágenes, estado de UI y contexto de proyecto multimodal se están convirtiendo en entradas normales, no demos.

Fuentes:
- https://lmstudio.ai/changelog/lmstudio-v0.4.13
- https://lmstudio.ai/blog/dgx-station

[10:00] DGX Spark se convierte en un objetivo serio para agentes locales

El mensaje actual de NVIDIA sobre DGX Spark y RTX es explícitamente sobre agentes locales. La empresa está enmarcando estas máquinas como computadoras de agentes para ejecutar agentes personales localmente, de forma privada, y sin costos de tokens. Su material de GTC destaca Nemotron 3 Nano 4B, Nemotron 3 Super 120B, optimizaciones de Qwen 3.5, Mistral Small 4, y stacks de agentes locales ejecutándose a través de Ollama, LM Studio y llama.cpp.

DGX Spark importa por su memoria y forma de despliegue. NVIDIA describe DGX Spark con 128GB de memoria unificada, suficiente para modelos de más de 120B parámetros. Nemotron 3 Super se describe como un modelo abierto de 120B con 12B parámetros activos, mientras que modelos más pequeños como Nemotron 3 Nano 4B apuntan a máquinas RTX más limitadas.

El punto no es que cada constructor deba comprar uno. El punto es que el software de agentes locales ahora tiene un nivel de hardware por encima de un escritorio único y por debajo de infraestructura GPU en la nube alquilada. Si los agentes locales van a mantener el contexto privado, ejecutar todo el día, y llamar herramientas sin pagar costos de nube por cada token en cada paso, máquinas como DGX Spark se convierten en infraestructura relevante.

Fuentes:
- https://blogs.nvidia.com/blog/rtx-ai-garage-gtc-2026-nemoclaw/
- https://build.nvidia.com/spark/hermes-agent

[15:00] EXO más DGX Spark muestra que la inferencia local distribuida es real pero aún tosca

Un problema de EXO alrededor de DGX Spark es más útil que un comunicado de prensa limpio porque muestra el modo de falla real. El cluster tenía Macs y un DGX Spark en la misma red local, la conectividad básica funcionaba, el acceso al dashboard de EXO funcionaba, y los puertos eran alcanzables. Pero los nodos aún no formaron un cluster de inferencia distribuida funcional.

La corrección reportada tuvo dos partes. Primero, el módulo de red Rust exo_pyo3_bindings, que contiene libp2p networking, descubrimiento mDNS, y lógica de red privada, necesitaba ser compilado manualmente en Linux/aarch64. Segundo, todos los nodos necesitaban el mismo EXO_LIBP2P_NAMESPACE para que la clave de red privada libp2p coincidiera en todo el cluster.

Después de eso, el DGX Spark apareció en el dashboard de EXO y participó en inferencia distribuida. Esa es la verdadera historia: EXO está abordando el problema correcto del clúster local, pero la inferencia local distribuida vive o muere según el descubrimiento, el empaquetamiento, la alineación de namespaces y las compilaciones específicas por arquitectura. El cómputo puro no es suficiente si los nodos no pueden encontrarse y confi arse mutuamente de manera confiable.

Fuentes:
- https://github.com/exo-explore/exo/issues/1682

[20:00] Llega Grok Build, pero las redirecciones de modelos y los precios necesitan atención

La documentación de Grok Build de xAI describe una superficie completa de CLI de agente de codificación: una TUI interactiva, scripting headless, salida plain/json/json-streaming, sesiones reanudables, ACP a través de Grok agent stdio, configuración de modelos personalizados, skills, plugins, hooks y descubrimiento de servidores MCP.

Eso hace que Grok Build forme parte de la misma categoría que otras CLIs de agentes de codificación: un agente nativo de terminal con hooks de automatización, no solo una interfaz de chat. La documentación oficial también muestra configuración de modelos personalizados, lo cual importa porque cada vez más constructores quieren shells de agentes de codificación que puedan enrutar hacia diferentes backends de modelos.

La historia del costo y la migración es separate pero importante. La página de retiro del 15 de mayo de xAI dice que los slugs de razonamiento deprecados redirigen a Grok 4.3 con bajo esfuerzo de razonamiento, los slugs no razonantes redirigen a Grok 4.3 sin esfuerzo de razonamiento, y grok-code-fast-1 redirige a Grok 4.3. La página lista el precio de la API de Grok 4.3 a $1.25 por millón de tokens de entrada y $2.50 por millón de tokens de salida. La recomendación práctica es fijar modelos de reemplazo explícitamente en lugar de dejar que los slugs deprecados cambien silenciosamente el comportamiento y la facturación.

Fuentes:
- https://docs.x.ai/build/overview
- https://docs.x.ai/build/cli/headless-scripting
- https://docs.x.ai/developers/migration/may-15-retirement

[25:00] LiteLLM y Envoy fortalecen la capa de gateway de modelos

LiteLLM v1.84.0 es una versión de fortalecimiento del gateway. El release cambia el nombrado de versiones a PEP 440, autentica endpoints pass-through por defecto, mejora la aplicación de presupuesto multi-pod, evita congelamientos de reconexión de Prisma, reduce la huella de memoria a través de routers de características lazy-loaded, añade soporte de descubrimiento OAuth MCP y Azure Entra, y añade seguimiento de ejecución de workflows durables a través de una superficie de API workflow-runs.

Envoy AI Gateway v0.6.0 se mueve en la misma dirección desde el lado del gateway de Kubernetes. Promueve CRDs core a v1beta1, añade soporte de endpoints de Anthropic en backends compatibles con OpenAI, añade embeddings de Gemini y context caching, soporta header forwarding por backend para MCP, añade redacción de cuerpos de solicitud/respuesta, y actualiza la base de referencia de Envoy/Gateway.

La razón por la que esto pertenece a un episodio de agentes locales es que local-first no significa sin gateway. Los agentes todavía necesitan enrutamiento, autenticación, presupuestos, redacción, compatibilidad con proveedores y autorización de MCP. Cuantos más backends de modelos y runtimes locales agregues, más importante se vuelve el plano de control.

Fuentes:
- https://docs.litellm.ai/release_notes/v1.84.0/v1-84-0
- https://aigateway.envoyproxy.io/release-notes/