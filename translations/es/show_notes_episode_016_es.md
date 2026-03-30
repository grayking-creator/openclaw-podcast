# OpenClaw diario — Episodio 016

**Título:** OpenClaw muda su piel  
**Subtítulo:** Análisis profundo de las versiones dobles v2026.3.22 y v2026.3.23

## 1) Resumen del episodio
En este episodio, analizamos las versiones consecutivas 2026.3.22 y 2026.3.23 de OpenClaw, centrándonos en los cambios más significativos para los mantenedores, desarrolladores de complementos y usuarios autohospedados. Desglosamos los puntos de presión de la migración (especialmente el SDK de complementos, las herramientas del navegador y los ecosistemas de matrices/habilidades), qué se interrumpe y qué hacer antes y después de la actualización. El objetivo es un estado de plataforma más limpio y seguro con menos sorpresas en el tiempo de ejecución, mejor comportamiento de autenticación/proxy y valores predeterminados más limpios para la interfaz de usuario, los modelos y las integraciones de extensiones.

## 2) Qué cubrimos
- Aspectos destacados de alto impacto de **v2026.3.22** y **v2026.3.23**
- Por qué `openclaw doctor --fix` se convirtió en el comando de anclaje de actualización
- Detalles de la migración del navegador/Chrome MCP y qué cambió para los flujos de sesiones existentes
- Cambios en el ecosistema de complementos: migración de SDK, comportamiento en tiempo de ejecución y eliminación de capas de compatibilidad antiguas
- Primera instalación del complemento ClawHub y correcciones de compatibilidad con el mercado/complemento
- Guía de migración del complemento Matrix y correcciones de confiabilidad
- Accesibilidad + actualizaciones de pulido de la interfaz de usuario (incluido el ajuste de contraste alineado con WCAG)
- Cambios en el proveedor Qwen/DashScope y limpieza de la configuración del modelo.
- Lista de verificación práctica de secuenciación y verificación de actualizaciones

## 3) Enlaces a notas de la versión
- [OpenClaw v2026.3.22](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22)
- [OpenClaw v2026.3.23](https://github.com/openclaw/openclaw/releases/tag/v2026.3.23)

## 4) Temas clave con enlaces
- [`openclaw doctor --fix`](https://docs.openclaw.ai/gateway/doctor) — punto de entrada de migración y reparación para el entorno, complementos y cambios de configuración conocidos
- [Navegador/Chrome MCP](https://docs.openclaw.ai/tools/browser): actualizaciones sobre archivos adjuntos del navegador de sesión existente y eliminación de la ruta de extensión de Chrome heredada
- [Migración del SDK del complemento](https://docs.openclaw.ai/plugins/sdk-migration): sustitución de supuestos de importación/interoperabilidad heredados con la nueva superficie del SDK
- [Descripción general del SDK del complemento](https://docs.openclaw.ai/plugins/sdk-overview): cómo deben funcionar ahora los límites del tiempo de ejecución del complemento y las API
- [Migración de Matrix](https://docs.openclaw.ai/install/migrating-matrix): se requieren actualizaciones para la nueva pila de complementos de Matrix
- [ClawHub](https://docs.openclaw.ai/tools/clawhub) — nuevo flujo predeterminado para instalación/actualización/búsqueda y compatibilidad de paquetes
- [Guía de migración de OpenClaw](https://docs.openclaw.ai/install/migrating): conceptos básicos más amplios de configuración/migración de estado
- [Qwen/DashScope (Model Studio)](https://www.alibabacloud.com/en/product/modelstudio): cambios de proveedor y actualizaciones de ruta de punto final
- [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/): línea base de accesibilidad para las actualizaciones de control y contraste de la interfaz de usuario en la versión

## 5) Lista de verificación de actualización (9 pasos)
- [] **Haga una copia de seguridad de su configuración/estado actual de OpenClaw** antes de las actualizaciones (incluido `.openclaw` + cualquier estado de complemento personalizado).
- [] **Actualización en secuencia**: instale/actualice a `2026.3.22` primero, luego a `2026.3.23` para que las correcciones de transición lleguen en orden.
- [] **Ejecute `openclaw doctor --fix` inmediatamente después de cada etapa de actualización** para reparar la desviación de la migración y las referencias de configuración obsoletas.
- [] **Cambiar las importaciones de complementos/agentes heredados** de superficies de compatibilidad eliminadas a los nuevos patrones `openclaw/plugin-sdk/*` y modelo de ejecución en tiempo de ejecución.
- [ ] **Migrar instalaciones de complementos y rutas de metadatos** hacia ClawHub (flujos `clawhub:<paquete>` cuando estén disponibles) y actualizar el estado de compatibilidad de habilidades/complementos.
- [] **Actualice la configuración del complemento Matrix** utilizando la guía de migración si proviene de la pila anterior de Matrix.
- [ ] **Migrar la higiene de la configuración**: reemplazar los nombres de entorno heredados y las ubicaciones de estado heredados (`CLAWDBOT_*`/`MOLTBOT_*`, `~/.moltbot`) con equivalentes actuales de OpenClaw.- [] **Revisar la configuración de herramientas del navegador** para cambios en Chrome/MCP del navegador (sesiones existentes, archivo adjunto userDataDir, eliminación de la ruta de retransmisión de extensión).
- [] **Verificar proveedores y UI/accesibilidad después del reinicio** (puntos finales Qwen/DashScope, valores predeterminados del modelo y flujos clave de UI) y ejecutar una breve prueba de humo de las herramientas asistentes.

## 6) Enlaces mencionados
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.22
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.23
- https://docs.openclaw.ai/gateway/doctor
- https://docs.openclaw.ai/tools/browser
- https://docs.openclaw.ai/plugins/sdk-migration
- https://docs.openclaw.ai/plugins/sdk-overview
- https://docs.openclaw.ai/install/migrating-matrix
- https://docs.openclaw.ai/tools/clawhub
- https://docs.openclaw.ai/install/migrating
- https://www.alibabacloud.com/en/product/modelstudio
- https://www.w3.org/TR/WCAG21/

## 7) Dónde encontrarnos
Visítenos en: **[tobyonfitnesstech.com](https://tobyonfitnesstech.com)**