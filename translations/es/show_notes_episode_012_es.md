# OpenClaw Daily — Notas del programa del episodio 12
**"Modelos de frontera gratuitos, memoria multimodal y automatizaciones comunitarias que te dejarán boquiabierto"**
📅 12 de marzo de 2026
🔗 Lanzamiento: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11

---

## Resumen del episodio
v2026.3.11 se lanzó con dos modelos de frontera libres y sigilosos, el primer modelo de incrustación multimodal nativo de Google aterriza en OpenClaw, un asistente de incorporación completo de Ollama, reanudación de sesión de ACP para largas sesiones de codificación y pulido de aplicaciones iOS/macOS. Además: una inmersión profunda en las automatizaciones comunitarias reales que ahorran mucho tiempo a las personas.

---

## Comunidad destacada: principales automatizaciones de BetterClaw

Usuarios reales de OpenClaw, tiempo real ahorrado. Del top 10 de BetterClaw:

1. **Reuniones informativas matutinas**: calendario + síntesis de correo electrónico, borradores de respuestas contextuales, antes de despertar
2. **Triaje de correo electrónico**: categorización automática, borrador de respuestas, programación de citas, totalmente local y privado
3. **Asistente de calendario familiar**: detección de conflictos, programación y mensajería familiar directa
4. **Servidor doméstico con autorreparación**: supervisa los servicios, intenta realizar correcciones automáticamente y alerta solo en caso de imprevistos.
5. **Base de conocimientos personales (RAG)**: búsqueda semántica en todas las notas, documentos y códigos

Creación de comunidad destacada: más de 5000 notas, 15 trabajos cron, 24 scripts personalizados: administrador de sistemas totalmente automatizado con controles de estado cada hora, sesiones informativas diarias y auditorías de seguridad semanales. Razonamiento de IA consciente del contexto, no solo guiones tontos.

---

## Nuevos modelos gratuitos: Hunter Alpha y Healer Alpha
Ambos están disponibles ahora en OpenRouter a $0,00/millón de tokens. (El nivel gratuito puede ser temporal).

**Cazador Alfa**
- 1 billón de parámetros
- Ventana de contexto de 1 millón de tokens
- Optimizado para casos de uso agentes
- https://openrouter.ai/openrouter/hunter-alpha

**Sanador Alfa**
- Frontera omnimodal: visión, oído, razonamiento, acción.
- Ventana de contexto de 262K
- https://openrouter.ai/openrouter/healer-alpha

---

## Memoria multimodal: incrustación de Gemini 2
Google anunció Gemini Embedding 2 el 11 de marzo. OpenClaw lo integró el mismo día.
https://deepmind.google/technologies/gemini/

- Primer modelo de incrustación multimodal nativo: texto, imágenes, vídeo, audio y archivos PDF en un espacio vectorial compartido.
- Soporte de audio nativo (sin paso de transcripción)
- Límite de entrada de 8192 tokens (4 × anterior)
- Supera a Amazon Nova 2 y Voyage Multimodal 3.5 en los puntos de referencia
- Dimensiones de salida configurables con reindexación automática al cambiar
- Control de respaldo estricto: sin degradación silenciosa

Caso de uso: pídale a su agente que "busque ese artículo sobre canalizaciones de implementación": aparecerá una captura de pantalla, una nota de voz Y un archivo de texto, todo a la vez. Significado sobre palabras clave.

---

## Ollama: asistente de incorporación completo de primera clase
Ollama alcanzó los 10 mil millones de extracciones: https://ollama.com
Las guías comunitarias (dev.to, FreeCodeCamp) tenían miles de lectores realizando configuraciones manuales. Ahora está integrado en el asistente.

Dos modos:
- **Local**: 100 % fuera de línea, toda la inferencia en el dispositivo, cero nube, máxima privacidad
- **Nube+Local** — Híbrido: local para tareas rápidas, nube para razonamientos pesados. Saltación de modelo inteligente en modo nube.

---

## ACP y herramientas para desarrolladores

**Reanudar sesión de ACP** (`resumeSessionId`)
- Reanudar una conversación con subagente durante los reinicios, sin volver a explicar el contexto.
- Reproducción de transcripción en `loadSession`
- Reenvío de archivos adjuntos de imágenes: contexto visual preservado en el currículum
- La transmisión de herramientas ACP ahora incluye sugerencias de ubicación de archivos
- `OPENCLAW_CLI` env var establecida en procesos secundarios

https://docs.openclaw.ai/acp

---

## Actualizaciones de aplicaciones

**iOS:**
- Nueva pantalla de bienvenida con descripción general del agente en vivo
- Controles flotantes reemplazados por una barra de herramientas acoplada.
- El chat se abre en la sesión principal resuelta: el contexto persiste en todos los dispositivos

**macOS:**
- Cambie de modelo directamente desde la vista de conversación: no se necesita una nueva sesión- Las preferencias a nivel de pensamiento persisten durante los reinicios.
- Refuerzo de reinicio de LaunchAgent

**Proveedor de OpenCode Go**: Zen + Go ahora comparte una clave en la configuración del asistente

---

## OpenClaw Backup (aterrizado el 8 de marzo)
```
creación de copia de seguridad de openclaw
verificación de copia de seguridad de openclaw
creación de copia de seguridad de openclaw --only-config
```
Realiza una copia de seguridad de la configuración, el estado y el espacio de trabajo. Úselo.
https://docs.openclaw.ai/cli/backup

---

## Enlaces clave
- Versión v2026.3.11: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11
- Cazador Alfa: https://openrouter.ai/openrouter/hunter-alpha
- Sanador Alfa: https://openrouter.ai/openrouter/healer-alpha
-Ollama: https://ollama.com
- Incrustación de Géminis 2: https://deepmind.google/technologies/gemini/
- Documentos de OpenClaw: https://docs.openclaw.ai
- Discordia comunitaria: https://discord.com/invite/clawd