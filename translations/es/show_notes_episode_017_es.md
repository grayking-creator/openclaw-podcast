# OpenClaw Daily — Episodio 017: Agentes hasta el final

**"Cómo el nuevo OpenClaw cambia su flujo de trabajo diario"**

El lanzamiento de OpenClaw del 24 de marzo marca un cambio significativo del pulido a la posibilidad. En este episodio, NOVA y ALLOY analizan los cambios concretos en el flujo de trabajo que son importantes para los usuarios avanzados y los constructores: desde subagentes anidados que descomponen las tareas de forma autónoma, hasta un sistema de memoria híbrido que finalmente resuelve el problema de olvido a mitad de sesión, una capa de compatibilidad OpenAI que hace que la infraestructura autohospedada sea una realidad inmediata, hasta la madurez de las plataformas Teams y Feishu que señala la evolución de OpenClaw más allá de un marco de bot de Telegram.

## Qué cubrimos

- **Subagentes anidados con profundidad configurable**: cómo los agentes ahora pueden generar especialistas, agregar resultados y operar sin la orquestación del usuario.
- **La herramienta `config_manager`**: lectura/escritura de configuración en tiempo de ejecución que permite la especialización dinámica del agente
- **Búsqueda vectorial híbrida BM25 +**: por qué la recuperación de coincidencia exacta ahora funciona de manera confiable junto con la similitud semántica
- **Incrustación de caché y compactación adaptativa**: los cambios de infraestructura que evitan la pérdida de contexto a mitad de sesión
- **Interfaz ContextEngine conectable**: la trampilla de escape del constructor para backends de memoria personalizados
- **Capa de compatibilidad OpenAI** — `/v1/models` y `/v1/embeddings` como puntos finales de puerta de enlace nativos
- **Autohospedaje con clústeres EXO**: Qwen3.5-27B destilado se ejecuta como un reemplazo directo de OpenAI
- **Migración del SDK de Microsoft Teams**: transmisión de respuestas, tarjetas de bienvenida, indicadores de escritura, etiquetado de IA
- **Componentes de Discord v2**: botones nativos, menús desplegables y modales interactivos
- **Soporte de Feishu/Lark** — OpenClaw llega a los mercados empresariales asiáticos
- **aplicación de nodo alfa de iOS**: OpenClaw se ejecuta como un nodo activo en iPhone

## Enlaces y recursos

- **Documentación de OpenClaw** — [https://docs.openclaw.dev](https://docs.openclaw.dev)
- **OpenClaw GitHub** — [https://github.com/openclaw-dev/openclaw](https://github.com/openclaw-dev/openclaw)
- **Destilado Qwen3.5-27B** — [https://www.modelscope.cn/models/Qwen/Qwen3.5-27B-Distill](https://www.modelscope.cn/models/Qwen/Qwen3.5-27B-Distill)
- **LangChain** — [https://www.langchain.com](https://www.langchain.com)
- **LlamaIndex** — [https://www.llamaindex.ai](https://www.llamaindex.ai)
- **Abrir WebUI** — [https://openwebui.com](https://openwebui.com)
- **SDK de Microsoft Teams** — [https://learn.microsoft.com/en-us/microsoftteams/platform/](https://learn.microsoft.com/en-us/microsoftteams/platform/)
- **Feishu / Alondra** — [https://www.feishu.cn](https://www.feishu.cn) / [https://www.larksuite.com](https://www.larksuite.com)
- **Documentación del clúster EXO** — [https://docs.openclaw.dev/hardware/exo-cluster](https://docs.openclaw.dev/hardware/exo-cluster)
- **Aplicación OpenClaw para iOS (Alfa)** — [https://openclaw.dev/ios](https://openclaw.dev/ios)
- **Documentos de la interfaz de ContextEngine** — [https://docs.openclaw.dev/core/context-engine](https://docs.openclaw.dev/core/context-engine)
- **Mostrar notas y archivos de episodios** — [https://tobyonfitnesstech.com](https://tobyonfitnesstech.com)

## Capítulos

- Gancho `[00:00]` — El cambio: Por qué el 24 de marzo es diferente de .22/.23
- `[02:30]` Segmento 1: Agentes que generan agentes: subagentes anidados, config_manager, escenarios de flujo de trabajo, riesgos de límite de profundidad
- `[10:00]` Segmento 2: la memoria se vuelve real: búsqueda híbrida BM25+vectorial, incrustación de caché, compactación adaptativa, capacidad de conexión de ContextEngine
- `[19:00]` Segmento 3: Capa de compatibilidad OpenAI y autohospedaje: `/v1/models` y `/v1/embeddings` nativos, reenvío de anulación de modelo, clúster EXO como reemplazo de OpenAI, aplicación de nodo iOS
- `[24:00]` Segmento 4: Madurez de la plataforma: SDK de Teams (transmisión, tarjetas de bienvenida, indicadores de escritura, etiquetado de IA), componentes de Discord v2, soporte para Feishu/Lark
- `[30:00]` Outro / Opinión del constructor: la versión actual de NOVA de los agentes anidados + memoria, el contrapunto de complejidad de ALLOY, CTA para tobyonfitnesstech.com

## Anfitriones

- **NOVA** — Anfitrión, analítico y conciso
- **ALLOY** — Coanfitrión, práctico y ligeramente escéptico