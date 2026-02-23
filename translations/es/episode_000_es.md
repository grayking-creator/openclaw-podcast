# Episodio 0: Análisis Profundo de Hardware - Solucionando Fallos de Modelos Locales

**Fecha:** 18 de febrero de 2026
**Duración:** 11:45
**Presentadores:** Nova & Alloy

---

## NOTAS DEL EPISODIO

### Temas Cubiertos

1. **El Error de Desbordamiento de Contexto** — Clarity (agente de codificación, Qwen3-Coder-30B) golpeó repetidamente errores de desbordamiento de contexto a mitad de tarea. Causa raíz: una definición de modelo Ollama etiquetada como `v-128k` que limitaba el contexto a 131,072 tokens, mientras que el modelo soporta nativamente 262,144 tokens. Una etiqueta de configuración del día de instalación se convirtió en un límite duro por accidente.

2. **La Matemática del Timeout** — El 18 de febrero a las 11:15 AM, se promovieron 146,760 tokens contra un límite de 131,072. La velocidad de pre-relleno es de ~400 tokens/seg, lo que significa que procesar 146K tokens toma más de 6 minutos. El umbral de timeout era de 5 minutos. Tres golpes consecutivos — no crashes, no inestabilidad — perfectamente explicados por la aritmética.

3. **Arquitectura de Memoria de Qwen3-Coder** — Qwen3-Coder 30B es un modelo de Mezcla de Expertos con solo 4 cabezas de atención KV (vs. 8 para LLaMA-3 8B). A 262K de contexto: ~15 GB de pesos del modelo + ~24 GB de caché KV + overhead del SO ≈ 44 GB en total. Una máquina de memoria unificada de 64 GB tiene 20 GB de margen. El hardware estaba bien todo el tiempo.

4. **Opción de Hardware 1: NVIDIA DGX Spark ($3,000)** — Chip GB10 Grace Blackwell, 128 GB LPDDR5X, 273 GB/s de ancho de banda de memoria. Contrariamente a la intuición, menor ancho de banda que un Mac Studio M2 Ultra (~800 GB/s). Compensa mediante núcleos tensor FP4 (25–50 tok/s en 70B vs. 10–15 actualmente). Solo Linux como accesorio; vincula dos unidades por $6K para ejecutar modelos de 405B+.

5. **Opción 2: Mac Studio M3 Ultra** — $4,000 (192 GB) a $8–10K (512 GB). 819 GB/s de ancho de banda, 2.1× más rápido que M2 Ultra según benchmarks de Apple. 20–32 tok/s en modelos de 70B. La configuración de 192 GB permite cargar simultáneamente modelos de 30B + 70B sin intercambio. La configuración de 512 GB es el único camino de consumidor para ejecutar LLaMA 3.1 405B localmente.

6. **Opción 3: AMD** — Dos historias:
   - *Threadripper + dual RX 7900 XTX ($5–6K)*: Problema de VRAM dividido, ROCm está rezagado respecto a CUDA. Pasaje difícil.
   - *Ryzen AI Max+ 395 "Strix Halo" ($2,000–2,500)*: La respuesta de AMD a Apple Silicon — CPU/GPU/NPO memoria unificada hasta 128 GB LPDDR5X. Framework Desktop AMD o ASUS ROG Flow Z13. El ancho de banda de memoria es de 256 GB/s (bus de 256-bit), ~3× menos que M2 Ultra — velocidades competitivas a pesar del doble de RAM direccionable. Mejor camino presupuestario a memoria unificada de 128 GB, punto.
   - *AMD MI300X ($25K, empresa)*: 192 GB HBM3, 5.3 TB/s de ancho de banda, 80–120 tok/s en 70B. Mencionado por completitud; no es una compra de consumidor.

7. **Estrategia de Flujo de Trabajo: Híbrido Local + Nube** — Las ediciones de múltiples archivos pesados (5+ plantillas, refactorizaciones grandes de codebase) representan ~20% de la carga total de trabajo. Para código no privado: Devstral ofrece 262K contexto nativo en el tier gratuito de Mistral API; Gemini 2.5 Pro ofrece 1 millón de tokens. La pregunta correcta no es "¿cómo ejecuto mis trabajos más difíciles localmente?" — es "¿deberían mis trabajos más difíciles ser locales en absoluto?"

8. **La Solución** — Parche de configuración + nueva definición de modelo Ollama para desbloquear la ventana completa de 262K. Hecho en vivo durante la investigación. Cero costo.

### Recursos de Hardware
- [Apple Mac Mini](https://www.apple.com/mac-mini/) - Recomendado para IA local
- [Raspberry Pi 5](https://www.raspunit.com/products/raspberry-pi-5/) - Opción presupuestaria
- [Ollama](https://ollama.com) - Runtime de LLM local

---

### Conclusiones Clave

1. **Una etiqueta de modelo no es un techo de capacidad.** El nombre del modelo Ollama `qwen3-coder:30b-262k` decía la verdad; la etiqueta del momento de creación no. Siempre verifica la configuración de ventana de contexto contra la especificación real del modelo.
2. **La generación de tokens está limitada por el ancho de banda de memoria, no por la computación.** El DGX Spark tiene menos ancho de banda de memoria que un Mac Studio. El ancho de banda es el cuello de botella — siempre verifica GB/s, no solo GB.
3. **Strix Halo (Ryzen AI Max+ 395) es el camino más barato a 128 GB de memoria unificada.** Nada más se acerca por menos de $3K. La compensación es ~3× menos ancho de banda que Apple Silicon.
4. **Diagnostica antes de comprar.** Tres capas de mala configuración (límite de contexto incorrecto + timeout demasiado corto + límite de modelo excedido) parecían fallo de hardware. Eran enteramente solucionables con configuración.
5. **La división híbrida local/nube es la palanca real de eficiencia.** Descarga el 20% de tareas pesadas de contexto, no privadas a Devstral o Gemini 2.5 Pro. Ejecuta el otro 80% localmente donde la privacidad importa.

---

### Recursos y Enlaces

| Elemento | Detalle |
|---------|---------|
| **Qwen3-Coder 30B** | Ollama: `ollama pull qwen3-coder:30b-262k` |
| **NVIDIA DGX Spark** | $3,000 — nvidia.com/en-us/project-digits |
| **Mac Studio M3 Ultra** | $3,999 (192 GB) / $7,999+ (512 GB) — apple.com |
| **AMD Ryzen AI Max+ 395** | Framework Desktop AMD Edition ~$2,000–2,500 |
| **ASUS ROG Flow Z13** | $2,499 — Ryzen AI Max+ 395, hasta 128 GB |
| **AMD MI300X** | $25,000+ empresa — solo como referencia |
| **Devstral** | 262K contexto, tier gratuito — mistral.ai |
| **Gemini 2.5 Pro** | 1M contexto — aistudio.google.com |
| **llama.cpp** | Backend de inferencia CPU — github.com/ggerganov/llama.cpp |
| **Ollama** | Runtime de modelo local — ollama.com |

---

## Transcripción Completa

*Nota: El Episodio 0 es un informe técnico en solitario. Las asignaciones de presentadores a continuación reflejan el formato estándar de dos presentadores del programa según el flujo de contenido — el avance pre-show es compartido, el informe principal es presentado por Nova.*

---

**[AVANCE PRE-SHOW]**

[NOVA]: La mayoría de la cobertura de IA te dice qué emocionarte. Este programa te dice qué funciona realmente — y qué no — cuando ejecutas modelos de lenguaje en tu propio hardware, en tus propios términos.

[ALLOY]: OpenClaw Daily es para personas que han superado la fase de demo en la nube. Ejecutas agentes locales, te importa a dónde van tus datos, y eres escéptico de los benchmarks publicados por el mismo equipo que entrenó el modelo.

[NOVA]: Lo mismo.

[ALLOY]: Cada episodio viene de sistemas reales, fallos reales y soluciones reales. No comunicados de prensa. Si algo se rompe a mitad de tarea, lo investigamos. En vivo. Sin limpieza editorial, sin pulido retroactivo.

[NOVA]: Este es el programa para constructores que ejecutan su propia infraestructura. Entremos en materia.

---

**[EPISODIO PRINCIPAL]**

[NOVA]: Mi agente de codificación, Clarity, ejecutando Qwen3-Coder 30B, seguía golpeando errores de desbordamiento de contexto justo en medio de las tareas. No ocasionalmente. Fiablemente.

Así que empecé a tirar del hilo — tal vez es un techo de hardware, tal vez necesito un DGX Spark o un M3 Ultra para ejecutar esto correctamente. Esa pregunta se convirtió en un análisis profundo de hardware completo: especificaciones reales, costos reales, ancho de banda de memoria, todo eso.

¿El giro? No era un problema de hardware en absoluto. Era una etiqueta de configuración. Y lo encontré y lo solucioné en vivo mientras hacía la investigación.

Obtendrás los números, las compensaciones honestas y una recomendación real.

---

¿Los desbordamientos de contexto que has estado experimentado? No es un problema de hardware.

El modelo que estás ejecutando — Qwen3-Coder 30B — en realidad soporta 262,144 tokens de contexto. 262,000.

OpenClaw lo estaba limitando a 131,072 debido a cómo se nombró el modelo Ollama en su creación. La etiqueta `v-128k` no era un techo de capacidad — era solo una cadena. Una etiqueta del día de configuración que se convirtió en un límite duro por accidente.

La solución fue un parche de configuración y una nueva definición de modelo Ollama. Hecho. En vivo. Gratis.

No necesitabas hardware nuevo. Necesitabas una corrección de una línea. Ese es el giro argumental.

---

Así que veamos qué pasó realmente el 18 de febrero a las 11:15 AM.

Promoviste 146,760 tokens contra un límite de 131,072.

Esos timeouts de cinco minutos no eran crashes — el modelo no estaba muriendo. estaba pre-rellenando.

A aproximadamente 400 tokens por segundo de velocidad de pre-relleno, procesar 146,000 tokens toma más de 6 minutos. Tu umbral de timeout era de 5 minutos. Así que el sistema golpeó la pared en el minuto 5, tres veces consecutivas.

Tres timeouts consecutivos, perfectamente explicados por la matemática. Eso no es inestabilidad. Es un valor de timeout demasiado corto para una ventana de contexto demasiado grande para un límite configurado que estaba equivocado desde el principio. Tres capas de error, apiladas una sobre otra.

---

Ahora la matemática de la memoria.

Qwen3-Coder es una arquitectura de Mezcla de Expertos con solo cuatro cabezas de atención KV. Compáralo con LLaMA-3 8B, que tiene ocho. La mitad. Esa es una elección de diseño intencional que lo hace dramáticamente más eficiente en memoria para contexto largo.

A 262K de contexto: 15 GB para los pesos del modelo, 24 GB para la caché KV, overhead del SO — digamos 44 GB en total.

Tienes 64 GB de memoria unificada. Eso es 20 GB de margen.

El modelo que estaba desbordándose cabe en tu máquina actual en su contexto nativo completo, con espacio de sobra. El hardware estaba bien todo el tiempo.

---

Sin embargo, pediste un informe de hardware — así que aquí está. Cuatro opciones, porque hay una nueva que vale la pena agregar a la conversación.

**Opción 1: NVIDIA DGX Spark — $3,000**

Chip GB10 Grace Blackwell. 128 GB de memoria unificada LPDDR5X. 1 petaflop de computación FP4.

El número que salta: 273 GB/s de ancho de banda de memoria.

Eso es en realidad menor que tu Mac Studio actual, que entrega alrededor de 800 GB/s. Así que la máquina que NVIDIA vende como una supercomputadora de IA tiene un tercio del ancho de banda de memoria de la máquina en tu escritorio.

La generación de tokens está limitada por el ancho de banda de memoria. El ancho de banda es el cuello de botella.

Donde Blackwell compensa es en los núcleos tensor FP4. Los benchmarks lo ponen en 25–50 tokens por segundo en un modelo de 70B, versus tus actuales 10–15. Mejora real.

Pero: Solo Linux, es un accesorio — no un reemplazo. Vincula dos unidades por $6,000 y puedes ejecutar modelos de 405B+.

---

**Opición 2: Mac Studio M3 Ultra**

$4,000 para 192 GB. $8–10,000 para 512 GB.

Ancho de banda: 819 GB/s — un paso modesto.

Apple midió M3 Ultra como 2.1× más rápido que M2 Ultra para rendimiento de LLM, debido a mejoras arquitecturales en el motor neuronal y las unidades de multiplicación de matrices.

En un modelo de 70B: 20–32 tokens por segundo. Roughly double donde estás ahora.

La configuración de 192 GB desbloquea carga de modelos simultánea — tu modelo de codificación de 30B, un modelo general de 70B, y el SO, todo en RAM a la vez. Sin intercambio. Flujo de trabajo diferente.

La configuración de 512 GB existe por una razón: LLaMA 3.1 405B en Q4 pesa 230 GB. Ese es el único camino de consumidor para ejecutar un modelo de clase 400B localmente. Same macOS, same desk, zero friction.

---

**Opción 3: AMD — y esto es en realidad dos historias muy diferentes.**

El camino de consumidor: Threadripper más tarjetas duales RX 7900 XTX — cuesta alrededor de $5,000–6,000. Cada tarjeta tiene 24 GB de VRAM.

El problema de VRAM dividido significa que no obtienes 48 GB limpios de memoria direccionable — obtienes 24 con overhead de sincronización inter-GPU costoso. ROCm todavía está rezagado respecto a CUDA para inferencia de LLM. Gastarías $5,000 para obtener los mismos tokens por segundo que obtienes ahora.

Pasaje difícil.

---

Pero AMD tiene un comodín que merece atención seria — especialmente si tu techo de presupuesto está más cerca de $2,500 que de $25,000.

El Ryzen AI Max+ 395, nombre clave Strix Halo.

16 núcleos Zen 5. 40 unidades de cómputo RDNA 3.5 para el iGPU. Un NPO de 50 TOPS. Y soporte hasta 128 GB de LPDDR5X en un pool de memoria completamente unificada — CPU, GPU y NPO todas dibujando del mismo espacio de direcciones.

¿Suena familiar?

Esta es la respuesta de AMD a la arquitectura de Apple Silicon, en un chip de laptop, a precios de consumidor.

Un Framework Desktop AMD Edition completo cuesta alrededor de $2,000–2,500. El ASUS ROG Flow Z13 se envía a $2,499. Este es el camino más barato, por un margen significativo, a 128 GB de memoria unificada en cualquier factor de forma.

Entonces, ¿por qué no es el ganador obvio? Ancho de banda. Siempre ancho de banda.

El bus de memoria aquí es de 256-bit, entregando aproximadamente 256 GB/s. Compáralo con tu M2 Ultra a 800 GB/s — eso es un déficit de tres veces. Más capacidad de memoria no ayuda si los tokens no pueden moverse lo suficientemente rápido.

En la práctica, vía backend CPU de llama.cpp: aproximadamente 60–80 tokens por segundo en un modelo de 7B, 15–20 en un 30B, y 5–8 tokens por segundo en un 70B Q4. Competitivo con el M2 Ultra, pero no superándolo — a pesar del doble de RAM direccionable. Esa brecha de ancho de banda es toda la explicación.

El camino de iGPU ROCm existe y funciona para algunos modelos, pero aún no está listo para producción. Ollama enruta a través de CPU. El backend Vulkan muestra promesa real como el camino de iGPU a corto plazo en Windows.

Donde el Ryzen genuinamente gana: portabilidad, ecosistema Windows, y capacidad de memoria cruda por dólar. Si necesitas 128 GB de memoria unificada por menos de $3K, no hay otra opción. Esta es la máquina "cabe un modelo de 70B en RAM y acepta velocidades de M2 Ultra".

---

El AMD MI300X es extraordinario y completamente irrelevante para esta decisión de compra.

192 GB de memoria HBM3. 5.3 TB/s de ancho de banda — no gigabytes, terabytes. 80–120 tokens por segundo en un modelo de 70B. También $25,000 mínimo, solo canal de ventas empresarial.

Pertenece a este informe por completitud. No pertenece a tu carrito.

---

[ALLOY]: Aquí está la perspectiva de flujo de trabajo que replantea todo.

Las tareas de edición de múltiples archivos — cinco o más plantillas a la vez, refactorizaciones grandes de codebase — representan quizás el 20% de tu carga de trabajo total. El otro 80% funciona limpiamente en el hardware actual.

La pregunta no es "¿cómo manejo mis trabajos más difíciles localmente?" Es: "¿deberían mis trabajos más difíciles ser locales en absoluto?"

Devstral tiene 262K contexto nativo en el tier gratuito de Mistral API. Gemini 2.5 Pro tiene 1 millón de tokens de contexto. Para código no privado, esos modelos en la nube son la herramienta correcta.

---

[NOVA]: Así que esto es lo que realmente haría — ahora con la imagen completa.

**Si quieres la mejor relación precio-rendimiento para trabajo cotidiano de LLM en el ecosistema Apple:** Mac Studio M3 Ultra 192 GB. La ventaja del ancho de banda de memoria es decisiva. Tres veces la RAM, el doble de velocidad, mismo escritorio. $4,000.

**Si tienes un presupuesto ajustado y necesitas máxima capacidad de memoria sobre todo** — quieres meter un modelo de 70B en RAM, estás cómodo en Windows, y velocidades de clase M2 Ultra son aceptables — el Ryzen AI Max+ 395 en un Framework Desktop o ROG Flow Z13 es genuinamente convincente a $2,000–2,500. Nada más te da 128 GB de memoria unificada a ese precio.

**Si específicamente quieres el ecosistema de software CUDA y estás cómodo con Linux como máquina accesoria:** DGX Spark a $3,000 es el movimiento. Escala de unidad dual a 405B si lo necesitas después.

**Y si necesitas modelos de clase 405B ejecutándose localmente hoy:** Mac Studio M3 Ultra 512 GB a $8–10,000 es el único camino accesible para consumidores.

---

El techo de rendimiento ahora mismo no es el silicio. Es la configuración — y ya lo solucionamos.

Deja que tu carga de trabajo real te diga si necesitas más hardware. Esa es la respuesta que la investigación dio. Y es una mejor respuesta que cualquiera de estas cajas.

---

*[FIN DEL EPISODIO 0]*
