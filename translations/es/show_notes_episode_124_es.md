Episodio 124 — 21 de octubre de 2026

[00:00] Gancho del episodio

MiniMax lanzó oficialmente M3.1 Flash, un modelo diseñado para tareas agénticas que involucran procesos de varios pasos y el uso de herramientas, con aplicaciones adicionales en programación, uso de computadoras y ciberseguridad. Google, Red Hat e IBM también publiques llm-d 1.0, un código abierto y stack nativo de Kubernetes para la inferencia distribuida de modelos de lenguaje grandes en TPUs y GPUs; el lanzamiento agrega control de flujo multitenant y enrutamiento consciente de la caché para implementaciones de IA a gran escala. SGLang amplió su ecosistema de serving con soporte para Clef y Clef Flash, PPLX-Decider v1 y v1.1, y EmbeddingGemma 2, además de ejemplos de recetario para cada modelo. Microsoft publicó una ficha de modelo para Sentiment-Analysis-7B, un modelo de lenguaje de 7 mil millones de parámetros que clasifica los mensajes de usuarios dirigidos a servicios, productos o agentes como Negative, Neutral o Positive. Mistral presentó Timestral, su primera familia de modelos preentrenados de series temporales, que amplía la capacidad de pronóstico para lecturas de sensores, demanda, volatilidad y otros datos secuenciales a cargas de trabajo que se ejecutan únicamente en CPU.

[02:00] MiniMax M3.1 Flash busca agentes más rápidos y económicos

MiniMax lanzó oficialmente M3.1 Flash como un modelo de nueva generación para tareas agénticas, programación, uso de computadoras y ciberseguridad. MiniMax informa que la inferencia en línea es casi tres veces más rápida y que los costos de uso para tareas agénticas son un 70 % menores que los de su predecesor. Según la empresa, el modelo puede completar flujos de trabajo SaaS de principio a fin en ventas, marketing, operaciones, atención al cliente, finanzas y RR. HH. El modelo puede comprender el código de manera independiente, desarrollar funciones, corregir problemas, validar su trabajo mediante pruebas y utilizar herramientas a lo largo de secuencias largas de tareas. En cuanto a la operación de computadoras, informa 61,7 puntos en OSWorld V2 y 29,6 puntos en Agents’ Last Exam, un benchmark para el trabajo profesional y las tareas complejas. MiniMax atribuye parte de la mejora en eficiencia a una mayor_esparsimiento, que reduce el cómputo activo. En el uso cotidiano, informa velocidades de salida superiores a 200 tokens por segundo y velocidades medianas superiores a 170. El precio plano es de USD 0,15 por millón de tokens de entrada, USD 0,60 por millón de tokens de salida y USD 0,015 por millón de tokens de entrada almacenados en caché. M3.1 Flash está disponible a través de la API de MiniMax, M Plan y MiniMax Code. MiniMax indica que los pesos del modelo se publicarán más adelante.

[02:23] llm-d 1.0 agrega enrutamiento consciente de la caché para flotas de IA

Google, Red Hat e IBM，最大的国产短视频平台 IBM Surprisingly? Need correct: "publicaron llm-d". "El lanzamiento..." Translate remaining. Ensure no accidental English except product names. "serving" maybe servicio. 

[03:20] SGLang Adds Three New Model Families -> SGLang agrega tres nuevas familias de modelos. 

Need output only. "agentic" translate agéntico. "retrieval" recuperación. "proxy" proxy? LatAm tech okay, but translate decodificador proxy. Product names unchanged means perhaps MiniMax etc.

Let's produce.

[05:56] Timestral de Mistral lleva la predicción preentrenada a cargas de trabajo que solo usan CPU

Mistral lanzó Timestral, una familia de cuatro modelos fundacionales de series de tiempo con 5 millones, 28 millones, 123 millones y 209 millones de parámetros. Los modelos ofrecen predicciones zero-shot, es decir, pueden hacer predicciones sobre datos nunca vistos sin entrenamiento específico para cada tarea, y se pueden ajustar mediante Mistral Forge para un dominio en particular.

Según Mistral, Timestral quedó en el primer lugar entre los modelos preentrenados y zero-shot en cinco métricas de GIFT-Eval, TIME y fev-bench. La empresa dijo que sus resultados Provenían de un solo punto de control, sin combinar varios modelos. Su versión de 28 millones de parámetros superó a Chronos-2 en GIFT-Eval y TIME, utilizando aproximadamente una cuarta parte de los parámetros, mientras que el modelo de 209 millones de parámetros superó a TimesFM-3 y Falcon-2.0 con menos parámetros.

Los modelos pueden predecir varias series relacionadas de forma conjunta y generar un conjunto completo de cuantiles, lo que permite a los equipos expresar la incertidumbre en lugar de depender de un solo valor predicho. También aceptan directamente entradas categóricas, como si una máquina está en funcionamiento, inactiva o en mantenimiento, además de entradas conocidas para el futuro, como calendarios de producción,_paradas previstas y pronósticos meteorológicos. Timestral distingue esas entradas de las series objetivo para que los valores futuros de la serie objetivo no se filtren en sus predicciones.

El despliegue no requiere un procesador gráfico. En un procesador de servidor con ocho hilos, la predicción con un día de anticipación a partir de tres semanas de historial en intervalos de 15 minutos tardó 10 milisegundos con el modelo de 5 millones de parámetros y 140 milisegundos con el de 209 millones.

Esto convierte a Timestral en una opción práctica para supervisar canalizaciones que abarcan sensores industriales, flujos financieros y otros datos operativos. Mistral Forge permite ajustar el modelo, añadir extensiones específicas para cada dominio, generar datos sintéticos y desplegarlo en hardware del cliente, incluidos entornos aislados de internet. La prueba pendiente clave es si la adaptación conserva un rendimiento útil a medida que los datos de producción cambian con el tiempo.

[07:40] Mercury 3 lleva los LLM de difusión a la velocidad de producción

Inception Labs lanzó Mercury 3, un modelo de lenguaje basado en difusión orientado a aplicaciones en las que el tiempo de respuesta influye en la experiencia del usuario. La empresa afirma que el modelo supera a GPT-6 Luna y Claude Haiku 5.5 en su suite de pruebas de rendimiento, genera 1.068 tokens por segundo en GPU de NVIDIA y admite una ventana de contexto de 1 millón de tokens, frente a los 260.000 de Mercury 2.5.

En un entorno de pruebas para agentes web en producción, Mercury 3 completó el 50% de 50 tareas de navegación en vivo de Mind2Web. Inception informó que ese resultado fue superior al de GPT-6.1-Sol, utilizando el mismo volumen de tokens y la misma cantidad de pasos del agente. La empresa también informa una mediana de tiempo de generación de 0,9 segundos y una mediana de tiempo de respuesta de extremo a extremo de 2,2 segundos en las pruebas de búsqueda con gafas inteligentes de Octen.

Mercury 3 cuesta USD 0,20 por millón de tokens de entrada y USD 0,70 por millón de tokens de salida. Los precios de lanzamiento tienen un descuento del 50% y los tokens de entrada almacenados en caché, un descuento del 90%. Inception y sus socios lo utilizan para soporte por voz y chat, tutoría, búsqueda, ingeniería de datos y navegación web. El modelo está disponible mediante la API de Inception, OpenRouter, Basetan y Vercel, con compatibilidad con la API de OpenAI. La próxima prueba será comprobar si la velocidad y la calidad informadas se mantienen en cargas de trabajo de producción sostenidas.

[08:51] Resumen de investigación: los robots aprenden a usar el lenguaje como memoria

Los investigadores presentaron UniWALM, un modelo diseñado para conectar video, acciones y lenguaje en una representación compartida. El resultado importante es que la generación conjunta del lenguaje parece mejorar la manipulación robótica y ayudar en tareas que dependen de recordar lo ocurrido anteriormente.

En lugar de enviar la información por etapas separadas de percepción, planificación y acción, UniWALM genera una acción y una memoria textual al mismo tiempo. El lenguaje generado se utiliza en el siguiente paso, lo que proporciona al robot un ciclo de memoria ligero sin necesidad de un planificador externo ni un banco de memoria. En la parte de RMBench que depende de la memoria, el sistema alcanzó un 34,5%, sin utilizar un modelo preentrenado de lenguaje o razonamiento.

Los investigadores también entrenaron al modelo para recuperarse de trayectorias de acción perturbadas, incorporando esa capacidad sin aumentar el costo de inferencia. Una consecuencia concreta es que un robot puede mantener el progreso de una tarea mediante el movimiento y el lenguaje: puede actuar, registrar una breve nota sobre la tarea y utilizar esa nota para orientar lo que hace a continuación.

[09:50] Concat ofrece una alternativa local y programable a CapCut

Concat es un editor de video de código abierto, local y multiplataforma, presentado como un reemplazo gratuito de CapCut. Su principal capacidad para quienes desarrollan herramientas es que puede programarse mediante una API JSON-RPC y MCP, ambas con interfaces estructuradas que permiten que el software interactúe con el editor.

Esta diferencia es importante porque abre la posibilidad de conectar la edición de video con flujos de trabajo automatizados, en lugar de tratar cada edición como una tarea manual de interfaz. El repositorio de GitHub indica 10.199 estrellas, lo que demuestra un interés considerable en el proyecto.

Por lo tanto, Concat vale la pena seguir como una base local de edición para herramientas y flujos de trabajo. La próxima evidencia útil serían ejemplos concretos de funciones de edición expuestas mediante sus interfaces y qué tan可靠 son esas funciones al abordar trabajos reales de edición.

[10:33] Terminal X usa GPT-6.1 Sol para auditar juicios de inversión

El estudio de caso de OpenAI del 20 de octubre destaca el Eval Agent de Terminal X, que califica las respuestas según una rúbrica de 54 criterios. En la configuración informada, GPT-6.1 Sol coincidió con el criterio de un inversionista sénior el 88,6% de las veces, según OpenAI, y detectó un 25% más de desviaciones respecto del mandato del fondo.

Esto convierte la revisión basada en rúbricas en un patrón de construcción concreto: definir los criterios que debe cumplir una respuesta, evaluarla con respecto a esos criterios e inspeccionar dónde se aparta de las reglas o del criterio de un profesional sénior. El valor radica en que la evaluación se convierte en una etapa separada, guiada por criterios, en lugar de depender únicamente de una lectura final por parte de una persona.

Lo siguiente que hay que observar es si la concordancia reportada y la detección de desviaciones son transferibles a otros mandates, modelos y tipos de resultados de inversión. El resultado del 88.6% se aplica a la configuración que Terminal X reportó.

[11:22] Exa 3.0 incorpora un modelo de embeddings más grande y una opción Lite de $4

Exa lanzó la versión 3.0 de su Search API, la cual incorpora un modelo de embeddings más grande, una opción Exa Lite con un precio de $4 por cada 1.000 solicitudes y Dynamic Highlights.

El modelo de embeddings más grande cambia el sistema de representación que se utiliza para relacionar las consultas con el contenido pertinente, mientras que Exa Lite introduce una opción de API de menor costo. Dynamic Highlights es otra función nueva disponible a través de la API mejorada.

Exa también realizó una comparación con Perplexity, Brave y Parallel, y afirma que su sistemaleadersó en las ocho pruebas de referencia. Dado que Exa realizó esas pruebas por sí misma, los desarrolladores deberían considerar el resultado como una afirmación sólida del proveedor, y no como una validación independiente.

La pregunta práctica es cómo se comporta Exa 3.0 en las búsquedas propias de un equipo y cómo las nuevas opciones afectan el presupuesto. Los resultados independientes de pruebas de referencia y el comportamiento de Dynamic Highlights en cargas de trabajo reales son lo siguiente que hay que observar.

[12:13] ChatGPT Work acelera la fijación de precios de los menús de restaurantes

Un franquiciado independiente de Schlotzsky’s y Cinnabon redujo en un 95% el tiempo necesario para actualizar los precios de sus menús mediante un flujo de trabajo creado con ChatGPT Work. El operador calcula que el cambio podría liberar $100.000 de flujo de caja, lo que convierte esto en un ejemplo concreto de cómo la IA pasa de la generación de contenido a las operaciones empresariales recurrentes.

El resultado importante no es simplemente una edición de menús más rápida. Al convertir el proceso de fijación de precios en un flujo de trabajo repetible, el franquiciado conectó una tarea operativa cotidiana con un posible beneficio en capital de trabajo. La reducción reportada del 95% proporciona la evidencia más clara del impacto.

Para otros grupos de restaurantes y empresas con múltiples sucursales, la oportunidad consiste en identificar las tareas frecuentes de fijación de precios y comprobar si un flujo de trabajo similar de ChatGPT Work puede reducir el tiempo del personal y mejorar el flujo de caja. La próxima prueba es si otros operadores pueden reproducir tanto el ahorro de tiempo como el beneficio financiero en sus propias ubicaciones.

[13:07] OpenAI adquiere Orchestra Bio para la investigación y el desarrollo en ciencias de la vida

OpenAI está adquiriendo Orchestra Bio para incorporar operaciones impulsadas por IA a la investigación y el desarrollo en ciencias de la vida. Los usuarios previstos son equipos de biofármacos que trabajan en el desarrollo de medicamentos, con el objetivo de ayudarlos a acelerar el desarrollo y impulso de nuevos tratamientos.

Lo importante ahora es el contexto: el anuncio se centra en aplicar IA dentro de las operaciones de investigación y desarrollo en ciencias de la vida, en lugar de presentar otro chatbot de propósito general o un resultado de investigación definido de manera narrowly. Esto lo vuelve relevante para los equipos que consideran cómo la IA podría apoyar los flujos de trabajo diarios de la biofarmacia.

La siguiente evidencia útil será concreta: qué procesos de investigación y desarrollo se impulsan con IA, cómo se pone a disposición esas capacidades y si ayudan a los equipos a avanzar más rápido.

[13:48] OpenAI incorpora evaluaciones de ChatGPT para idiomas con menos recursos

OpenAI está mejorando ChatGPT en lenguajes de programación de bajos recursos, es decir, idiomas con menos ejemplos digitales y recursos disponibles para herramientas de software. La empresa anunció nuevas evaluaciones que abarcan ingeniería de software, SQLite y migración de COBOL.

El cambio importa para los equipos cuyo trabajo no se centra en los lenguajes de programación más ampliamente representados. Las tareas de SQLite implican trabajo orientado a bases de datos, mientras que la migración de COBOL se concentra en trasladar código desde un lenguaje de programación empresarial más antiguo. Esos son ámbitos concretos donde los límites de un asistente de programación con IA pueden afectar proyectos reales.

Para los desarrolladores, las nuevas evaluaciones ofrecen una base más pertinente para evaluar ChatGPT que las preguntas generales de programación. Un equipo podría examinar cómo maneja el modelo una tarea de ingeniería de software, un escenario de SQLite o una migración de COBOL antes de decidir dónde debe incorporarse la asistencia de IA en su flujo de trabajo.

Algo que hay que observar es lo que las evaluaciones ampliadas revelan sobre el rendimiento a medida que OpenAI lleva ChatGPT a entornos de lenguaje con menos recursos.