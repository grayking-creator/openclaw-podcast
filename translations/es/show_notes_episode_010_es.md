# Show Notes - Episodio 10: La revolución del documento y la memoria

## Detalles del episodio
- **Episodio:** 10
- **Fecha:** 4 de marzo de 2026
- **Anfitriones:** Nova (británico cálido) y Alloy (estadounidense)
- **Duración objetivo:** 30-35 minutos
- **Tema:** OpenClaw evoluciona de una plataforma de chat/agente a una plataforma completa de documentos y memoria

---

## Parte 1 — Del lanzamiento: OpenClaw 3 de marzo de 2026
**Notas de la versión:** https://github.com/openclaw/openclaw/releases/tag/v2026.3.2

Todo lo contenido en esta sección se envió en la versión del 3 de marzo:

### 1. Herramienta de análisis de PDF *(NUEVO)*
- Herramienta `pdf` de primera clase: soporte nativo de Anthropic/Google (el modelo ve el PDF directamente), reserva de extracción para todos los demás
- Configurable: `agents.defaults.pdfModel`, `pdfMaxBytesMb`, `pdfMaxPages`
- Lo que esto desbloquea: contratos, facturas, trabajos de investigación, cualquier documento con el que realmente trabajes.

### 2. Incrustaciones de memoria de Ollama *(NUEVO - inmersión profunda en el episodio)*
- `memorySearch.provider = "ollama"` — memoria local completa/pila RAG, no se requiere API de nube
- La primera vez que puedes ejecutar todo (inferencia Y memoria) sin tocar un proveedor de nube
- Configuración de Honrs `models.providers.ollama` para solicitudes de incrustación
- Por qué esto es importante: su agente ahora puede recordar miles de interacciones usando solo computación local

### 3. Expansión SecretRef *(NUEVO)*
- 64 objetivos de credenciales ahora cubiertos con SecretRef
- Falla rápida en referencias no resueltas en superficies activas: sin fallas silenciosas
- Cubre: recopiladores de tiempo de ejecución, planificación/aplicación/auditoría de secretos, incorporación de SecretInput UX

### 4. Adjuntos de sesiones *(NUEVO)*
- `sessions_spawn` admite archivos adjuntos en línea (tiempo de ejecución de subagente)
- Codificación Base64/utf8, limpieza del ciclo de vida, límites mediante `tools.sessions_spawn.attachments`
- Los agentes ahora pueden pasar archivos directamente entre sí.

### 5. Valores predeterminados de transmisión de Telegram
- La transmisión ahora está predeterminada en "parcial" (estaba "desactivada"): vista previa en vivo lista para usar para nuevas configuraciones
- La transmisión de DM utiliza `sendMessageDraft` para una vista previa privada

### 6. MiniMax-M2.5-alta velocidad
- Soporte de primera clase en catálogos e incorporación: variante más rápida de MiniMax-M2.5

### 7. Validación de configuración CLI
- `openclaw config validar --json` — detecta errores antes del inicio de la puerta de enlace
- Rutas detalladas de claves no válidas en errores de inicio

### 8. Complemento personal de Zalo reconstruido
- Integración nativa `zca-js`, completamente en proceso, sin transporte CLI externo

### 9. Salida multimedia
- Discord, Slack, WhatsApp y Zalo unificados con `sendPayload` compartido + iteración multimedia

### 10. Complemento SDK/STT
- `api.runtime.stt.transcribeAudioFile()` — las extensiones ahora pueden convertir voz a texto

---

## Parte 2: esta semana en OpenClaw

### Artículo 1: OpenClaw supera las 250.000 estrellas de GitHub
**Fuente:** ainvest.com - 3 de marzo de 2026
**URL:** https://www.ainvest.com/news/openclaw-github-star-count-surpasses-250-000-ai-agent-boom-2603/

OpenClaw alcanzó las 250.000 estrellas de GitHub, el proyecto de IA más rápido en alcanzar ese hito. El artículo también destaca que C3.ai (IA empresarial) no cumplió con las previsiones de ingresos en un 30 % y anunció una reducción de la fuerza laboral del 26 %. El contraste es sorprendente: la IA empresarial tropieza mientras la IA autohospedada y de código abierto explota. El diseño local de OpenClaw y el soporte multiplataforma se citan como diferenciadores clave.

### Artículo 2: Dentro de OpenClaw: la arquitectura que lo explica todo
**Fuente:** dev.to - 4 de marzo de 2026
**URL:** https://dev.to/jiade/inside-openclaw-how-the-worlds-fastest-growing-ai-agent-actually-works-under-the-hood-4p5nUna inmersión técnica profunda sobre por qué OpenClaw creció mientras que cientos de otros marcos de agentes de IA no lo hicieron. Cubre: la estrategia de integración del SDK de Pi, el sistema de memoria de dos capas, el modelo de concurrencia de Lane Queue y el motor de latidos. La tesis: no es marketing, es arquitectura. Buen material de episodio para explicar qué diferencia a esta plataforma de LangChain, AutoGPT y otras.

### Artículo 3: OpenClaw en el mundo real (patrones de producción)
**Fuente:** Trilogía AI / Rahul Subramaniam - 3 de marzo de 2026
**URL:** https://trilogyai.substack.com/p/openclaw-in-the-real-world

El artículo de verificación de la realidad. Cubre tres modos de falla que las personas experimentan después de la configuración inicial alta: la memoria se estropea, se pierde trabajo cuando la máquina se reinicia y la confiabilidad comienza a importar más que la experimentación. Proporciona patrones de producción para pasar de una "demostración interesante" a un sistema del que realmente depende. Se conecta directamente al tema de memoria del Episodio 10.

---

## Conclusión clave
Esta versión cruza un umbral: análisis de documentos + memoria local persistente + transferencia de archivos entre agentes = OpenClaw como un segundo cerebro, no solo una interfaz de chat. El hito de las 250.000 estrellas y el artículo sobre la producción en el mundo real indican lo mismo: la gente ya no está experimentando, depende de esto.

## Patrones de construcción discutidos
1. **Revisor de documentos legales**: herramienta PDF + memoria + salida de Slack
2. **Asistente de investigación local**: incrustaciones de Ollama + herramienta PDF, API de nube cero
3. **Secure Credential Pipeline**: archivos adjuntos de sesiones de SecretRef + para flujos de trabajo de múltiples agentes

---
📋 Guión completo: `openclaw-podcast/episode_010.md` (3530 palabras)
✅ Auditoría de temas: todos los temas verificados en limpio con respecto a los episodios 0 a 9
⏳ **Esperando su aprobación para proceder a la generación de audio**