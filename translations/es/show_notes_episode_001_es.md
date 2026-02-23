# Episodio 1: La Historia Completa - Notas del Programa

*Publicado: 19 de febrero de 2026 | Duración: ~30 minutos | Presentadores: Nova y Alloy*

---

## Temas Cubiertos

### 1. Noticias de la Fundación y Peter Steinberger
- **14 de febrero de 2026**: Peter Steinberger anunció su incorporación a OpenAI mientras transicionaba OpenClaw a una fundación independiente de código abierto.
- **Compromiso de Sam Altman**: "OpenClaw vivirá en una fundación como un proyecto de código abierto que OpenAI continuará apoyando".
- **Objetivo de Peter**: "construir un agente que incluso mi madre pueda usar".
- OpenAI ha estado patrocinando el proyecto, trabajando en la estructura de la fundación.
- Peter pasó la última semana en San Francisco hablando con los principales laboratorios, obteniendo acceso a investigaciones no publicadas.

### 2. Cobertura Mediática
- **Reuters**: Tendencias de gobernanza de IA de código abierto.
- **Forbes**: Implicaciones comerciales de OpenAI adquiriendo talento.
- **TechCrunch**: Implicaciones técnicas para la comunidad de desarrolladores.
- **The Conversation**: Comparación de OpenClaw/Moltbook con los inicios de las redes sociales.
- **Fortune**: "La contratación de OpenClaw por parte de OpenAI señala una nueva fase en la carrera de los agentes de IA".
- **Nature**: "Los chatbots de IA de OpenClaw están corriendo desenfrenados — estos científicos están escuchando".
- **IBM**: "OpenClaw, Moltbook y el futuro de los agentes de IA".
- **CNBC**: Evolución del nombre (Clawdbot → Moltbot → OpenClaw) y accesibilidad para individuos/equipos pequeños.
- **v2026.2.17**: Se agregó soporte para Anthropic Claude.

### 3. Análisis Profundo de Seguridad
- **CrowdStrike**: Ataques de inyección de prompts dirigidos a sistemas de IA agentes, estudio de caso específico de OpenClaw.
  - Inyección de prompts directa.
  - Inyección indirecta (oculta en documentos/correos/páginas web).
  - Inyección encadenada (explotar una herramienta para plantar una carga útil para otra).
- **Northeastern University**: "Por qué el agente de IA OpenClaw es una pesadilla de privacidad".
- **Kaspersky**: Recomendaciones prácticas: mantener actualizado, ser selectivo con las habilidades, revisar permisos, no ejecutar como root.

### 4. Estadísticas de GitHub
- **Más de 190,000 estrellas en GitHub** en menos de 90 días.
- **#21** en la lista de repositorios con más estrellas en la historia de GitHub.
- **Más de 145,000 estrellas** llegaron en solo 5 días - el crecimiento más rápido en la historia del código abierto.
- **Más de 20,000 bifurcaciones** - comunidad activa construyendo.

### 5. Opciones de Hardware
- **Mac Mini M4 Pro** con 64GB de memoria unificada.
  - Puede ejecutar modelos de 70 mil millones de parámetros.
  - ~10-15 tokens/segundo.
  - Punto ideal: 48-64GB RAM, ~$1500-2000.
- **Ventaja de Apple Silicon**: Arquitectura de memoria unificada - la CPU y la GPU comparten la misma memoria, sin cuello de botella de ancho de banda.
- **Raspberry Pi 5** con 8GB RAM.
  - Modelos de 1 a 3 mil millones de parámetros.
  - ~$80 por la placa + carcasa/fuente de alimentación = ~$100 total.
- **Hardware usado**: Mac Mini M1 16GB ~$300 usado; laptops viejas + GPUs usadas.

### 6. Lanzamientos de Modelos
- **Llama 4** (Meta)
  - Variantes Scout y Maverick.
  - Nativamente multimodal (texto + imágenes).
  - Arquitectura de mezcla de expertos.
  - Disponible en Ollama: `ollama pull llama4`.
- **Qwen3** (Alibaba)
  - Variantes densas y MoE.
  - Hasta 128,000 tokens de contexto.
- **Mistral 3** (Mistral)
  - De 3B a 675B parámetros.
  - 3B funciona en 4GB de RAM.
- **Modo Air Gap de Ollama**: Interruptor para desactivar todas las integraciones de modelos en la nube.

### 7. Comunidad y Ecosistema
- **ClawHub**: Más de 5,700 habilidades publicadas.
  - Pipelines de DevOps, hogar inteligente, seguimiento financiero, gestión de contenido.
- **VoltAgent**: Lista curada de las mejores habilidades y recursos.
- **Krupesh Raut (Medium)**: "Las actualizaciones de febrero de OpenClaw hacen que los asistentes de IA de pago parezcan un chiste".
- **OpenClawn.com**: Nuevo sitio de contenido educativo.

### 8. Opciones de Despliegue
- **Nivel gratuito de Oracle Cloud**: 4 CPUs ARM, 24GB RAM, almacenamiento en bloques persistente - GRATIS.
- **DigitalOcean 1-Click**: Imagen de seguridad reforzada, actualizaciones automáticas.
- **Espectro de autoalojamiento**: Raspberry Pi → hardware reutilizado → Mac Mini dedicado.

---

## Consejos de este Episodio

1. **Ejecuta `openclaw doctor` primero**: verifica toda la configuración, dependencias y ajustes.
2. **Conecta Claude Code a modelos locales vía Ollama**: obtén el razonamiento de Claude con la privacidad de los datos locales.
3. **No lo expongas a internet sin la autenticación adecuada**: usa una VPN (Tailscale/WireGuard) en lugar de vincularlo a interfaces públicas.
4. **Configura controles de acceso basados en roles** para entornos multiusuario (familia/equipo).
5. **Ollama Multi-Model Benchmarker** en Google Colab: compara modelos lado a lado.

---

## Enlaces Mencionados

- [openclaw.ai](https://openclaw.ai)
- [Comunidad de Discord](https://discord.gg/openclaw)
- [ClawHub](https://clawhub.com)
- [OpenClawn.com](https://openclawn.com)
- [Ollama](https://ollama.com)
