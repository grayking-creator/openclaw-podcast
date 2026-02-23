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
