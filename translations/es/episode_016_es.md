## [00:00-02:30] OpenClaw muda de piel

NOVA: Soy NOVA, esto es OpenClaw Daily, y hoy tenemos uno de esos releases donde los números de versión se ven ordenados, pero la historia real debajo es desordenada, importante y, honestamente, bastante fascinante. [PAUSE] Esta semana, dos bugs golpearon un setup real de power-user con suficiente fuerza como para contarte casi todo lo que necesitas saber sobre dónde está OpenClaw en este momento.

ALLOY: Sí. Estos no eran edge cases tiernos y pequeños. Eran el tipo de bugs que te hacen dudar de tu propio setup, porque lo que ves no es lo que el sistema en realidad está haciendo.

NOVA: Bug uno: un usuario tenía [EMPHASIS]MiniMax[/EMPHASIS] configurado como su modelo de razonamiento. La API upstream estaba devolviendo [EMPHASIS]api_error[/EMPHASIS]. OpenClaw vio eso, decidió que debía ser transitorio, lo reintentó en silencio, nunca mostró la falla, nunca activó correctamente el fallback, y el usuario recibió un resultado degradado sin tener idea de que la llamada original había fallado.

ALLOY: Lo cual es brutal, porque los peores bugs son los que no explotan. Simplemente empeoran en silencio. No recibes una luz roja. Recibes una luz verde más tenue.

NOVA: Exactamente. Y el bug dos era una clase distinta de dolor, pero igual de real. El usuario pega un token nuevo de [EMPHASIS]OpenAI Codex[/EMPHASIS], ve la confirmación, todo parece exitoso, reinicia el gateway, y el token se revierte a la credencial expirada.

ALLOY: Ese te hace sentir loco. Porque desde la perspectiva del usuario, hizo lo correcto. Pegó el token nuevo. La app dijo: sí, guardado. Luego, después del restart, no. Otra vez el token viejo y malo. [PAUSE] Bajo el capó, el estado de auth en memoria del gateway estaba sobrescribiendo en el restart el valor recién guardado en disco.

NOVA: Ambos están corregidos en [EMPHASIS]v2026.3.23[/EMPHASIS]. Pero para entender por qué ocurrieron, necesitas entender qué cambió [EMPHASIS]v2026.3.22[/EMPHASIS]. Porque .22 es la grande. .22 es OpenClaw haciendo algo que probablemente debió haber hecho hace un año.

ALLOY: La purga del legado.

NOVA: La purga del legado. Los nombres viejos, las capas de compatibilidad, los caminos de transición raros, las muletas del browser relay, la masa amorfa del plugin SDK: una gran parte fue arrancada. [PAUSE] Y creo que la manera correcta de enmarcar estas dos releases juntas es esta: .22 quita la piel muerta, y .23 se asegura de que la piel nueva no se agriete.

ALLOY: Ese es todo el episodio. Si estás manteniendo una instalación real, estas no son actualizaciones decorativas. Son estructurales.

## [02:30-11:00] La purga del legado — Breaking Changes de v2026.3.22

NOVA: Empecemos con el cambio más cargado emocionalmente, porque la gente se apega de forma rarísima a los nombres, incluso cuando esos nombres debieron haberse retirado para siempre hace mucho tiempo. Los nombres de entorno [EMPHASIS]CLAWDBOT_*[/EMPHASIS] y [EMPHASIS]MOLTBOT_*[/EMPHASIS] desaparecieron. No están deprecated. No se toleran con una advertencia. Desaparecieron.

ALLOY: Y quiero bajar un poco el ritmo ahí, porque si ejecutas OpenClaw en una sola laptop y en ningún otro lado, podrías escuchar eso y pensar, ok, renombro algunas variables, bien. Ese no es el modo real de falla. El modo real de falla es que tienes un archivo [EMPHASIS].env[/EMPHASIS] viejo en Docker Compose, o una unidad [EMPHASIS]systemd[/EMPHASIS] toda oxidada en un VPS, o algo en un perfil de shell que no has mirado en ocho meses. Haces upgrade, OpenClaw arranca, y esos valores se ignoran en silencio.

NOVA: Sin error. Sin banner de migración.

ALLOY: Nada de “oye, vi [EMPHASIS]CLAWDBOT_TOKEN[/EMPHASIS] y eso es obsoleto”. Solo config faltante. De pronto auth ya no cuadra, la ruta del state no está donde pensabas, tal vez un plugin no carga, tal vez un token parece ausente. [PAUSE] Este es el tipo de ruptura que te pega a las dos de la mañana después de un upgrade en una máquina a la que no tocabas desde hace tiempo.

NOVA: Haz grep a tus archivos de env. Cada ambiente donde ejecutas OpenClaw. Cada host. Cada archivo de Compose. Cada unidad de arranque. Cada bootstrap de shell. Si tienes [EMPHASIS]CLAWDBOT_*[/EMPHASIS] o [EMPHASIS]MOLTBOT_*[/EMPHASIS], trata eso como roto hasta corregirlo.

ALLOY: Misma historia con el viejo directorio de state [EMPHASIS]~/.moltbot[/EMPHASIS]. Esa ruta ya no es parte del futuro. Si tu state sigue viviendo ahí, OpenClaw no va a inferirlo mágicamente por ti después del upgrade. Muévelo a [EMPHASIS]~/.openclaw[/EMPHASIS] o define [EMPHASIS]OPENCLAW_STATE_DIR[/EMPHASIS] explícitamente y termina con eso.

NOVA: Y esta es una de esas decisiones en las que, de hecho, estoy de acuerdo con la dureza. Los aliases de transición se sienten amables en el corto plazo, pero hacen que la arquitectura mienta sobre sí misma. Hay un costo real en fingir que los nombres viejos siguen siendo de primera clase.

ALLOY: Estoy de acuerdo con el estado final. No estoy de acuerdo con lo tranquilos que se ponen algunos sobre el dolor de la migración. Si eres la persona que administra cinco instalaciones y dos de ellas son raras, esto no es una limpieza filosófica. Es una búsqueda del tesoro.

NOVA: Justo. [PAUSE] El segundo gran breaking change en .22 es que [EMPHASIS]ClawHub[/EMPHASIS] ahora es first-class, y el significado práctico de eso es mayor de lo que la redacción de marketing hace sonar. [EMPHASIS]openclaw plugins install name[/EMPHASIS] ahora revisa ClawHub primero, y solo cae a npm si ClawHub no tiene el paquete.

ALLOY: Lo que significa que el comportamiento de instalación cambió, incluso si no cambiaste tu comando. Esa es la parte que la gente necesita oír. Si tienes scripts que asumen una ruta de resolución de paquetes por npm, y ese mismo nombre ahora existe en ClawHub, puede que obtengas primero la versión de ClawHub.

NOVA: También hay comandos nativos ahora: [EMPHASIS]openclaw skills search[/EMPHASIS], [EMPHASIS]openclaw skills install[/EMPHASIS], [EMPHASIS]openclaw skills update[/EMPHASIS]. [PAUSE] Y para mí, esto es OpenClaw por fin alineando el producto con el ecosistema que pretendía tener. ClawHub siempre debió ser el hogar de las skills. Esta release convierte eso en algo real en vez de aspiracional.

ALLOY: Está más limpio, pero prueba tu automatización. Si tienes scripts de bootstrap, dotfiles, docs de onboarding, asegúrate de que todavía instalen lo que crees que instalan. El cambio es bueno. Las sorpresas no.

NOVA: Tercero: la renovación total del [EMPHASIS]Plugin SDK[/EMPHASIS]. Esto no es un mordisquito en los bordes. [EMPHASIS]openclaw/extension-api[/EMPHASIS] desapareció. No hay compatibility shim. La nueva superficie es [EMPHASIS]openclaw/plugin-sdk/*[/EMPHASIS], con subpaths más estrechos y límites mucho más claros.

ALLOY: Si tienes plugins personalizados, esta es una migración real. No es opcional. No hay fallback. No puedes decir: “lo actualizo después”. Después significa roto.

NOVA: Los plugins empaquetados también ahora tienen que usar el runtime inyectado para operaciones del lado del host, que es uno de esos cambios que suenan burocráticos hasta que te das cuenta de que elimina mucho sangrado ambiguo de privilegios. El comportamiento del host es explícito. Los límites del runtime son explícitos.

ALLOY: Y el descubrimiento de mensajes también cambió. [EMPHASIS]describeMessageTool()[/EMPHASIS] ahora es obligatorio. El flujo viejo de [EMPHASIS]listActions[/EMPHASIS], [EMPHASIS]getCapabilities[/EMPHASIS], [EMPHASIS]getToolSchema[/EMPHASIS] fue eliminado. [PAUSE] Eso no es un rename. Eso es un cambio de contrato.

NOVA: El SDK nuevo de hecho es más limpio. De verdad. Los imports son más específicos. La intención es más clara. El modelo de runtime es más coherente. Pero sí tienes que migrar. Y si eres desarrollador de plugins, ve a leer [EMPHASIS]docs.openclaw.ai/plugins/sdk-migration[/EMPHASIS]. No improvises de memoria.

ALLOY: Quiero subrayar eso. Esta no es la semana para hacer tu migración a pulso basándote en vibes.

NOVA: Cuarto bloque: endurecimiento de seguridad. Algunas de estas cosas son invisibles hasta que te salvan, lo que significa que no van a recibir tanto tiempo al aire, pero importan. El exec sandbox ahora bloquea [EMPHASIS]MAVEN_OPTS[/EMPHASIS], [EMPHASIS]SBT_OPTS[/EMPHASIS], [EMPHASIS]GRADLE_OPTS[/EMPHASIS], [EMPHASIS]ANT_OPTS[/EMPHASIS], además de [EMPHASIS]GLIBC_TUNABLES[/EMPHASIS] y [EMPHASIS]DOTNET_ADDITIONAL_DEPS[/EMPHASIS]. [PAUSE] Eso es básicamente una barrida contra superficies de inyección de runtime que la gente olvida que existen.

ALLOY: Exacto. Estas env vars son el tipo de cosa que a los atacantes les encanta y a los operadores se les olvida. Si tu sandbox de herramientas dice “estamos controlando lo que se ejecuta”, pero todavía estás dejando que variables de inyección de build tools o runtime se cuelen, en realidad no estás controlando mucho.

NOVA: También hay un cambio sutil pero inteligente en la allowlist: [EMPHASIS]time[/EMPHASIS] ahora es transparente en la evaluación de la allowlist. Así que [EMPHASIS]time ./approved-script[/EMPHASIS] se vincula al script interno, no al wrapper [EMPHASIS]time[/EMPHASIS].

ALLOY: Ese es tan práctico. La gente envuelve comandos en [EMPHASIS]time[/EMPHASIS] constantemente durante debugging. Antes, los wrappers podían crear edge cases raros de policy. Ahora evalúa la cosa que realmente querías ejecutar.

NOVA: Y el endurecimiento de voice webhook también se puso más estricto: rechazar firmas faltantes del provider antes de leer el body, con un límite pre-auth de [EMPHASIS]64KB[/EMPHASIS] y [EMPHASIS]5s[/EMPHASIS]. Lo cual es simplemente buena higiene de perímetro. No gastes recursos parseando basura no autenticada.

ALLOY: Por último, sobre las correcciones silenciosas que importan: los comandos slash de Discord. Carbon reconcile ahora es el default, así que los restarts del gateway ya no hacen churn de comandos slash a través de la ruta de deploy local.

NOVA: Me encanta esta clase de corrección porque los usuarios la viven como menos fantasmas.

ALLOY: Sí. Silenciosa pero real. Los restarts estaban generando comandos fantasma. Ahora no. Eso no es glamoroso, pero es exactamente el tipo de cortadita de papel que hace que una plataforma se sienta amateur si la dejas sin corregir.

NOVA: Así que .22 en una sola frase: OpenClaw dejó de fingir que el legado era inofensivo.

ALLOY: Y si no has tocado tu setup en un tiempo, .22 es la release que lo va a descubrir por ti.

NOVA: También creo que esta release traza una línea entre compatibilidad y desorden. Durante mucho tiempo, OpenClaw estuvo cargando nombres viejos, supuestos viejos de instalación, formas viejas de descubrimiento de plugins y caminos viejos de browser porque quitarlos se sentía arriesgado. [PAUSE] Pero dejarlos en su lugar también era arriesgado. Hacía que la plataforma fuera más difícil de razonar.

ALLOY: Ese es el trade-off que la gente no ve. La compatibilidad hacia atrás no solo preserva la función. También preserva la confusión. Cada alias, cada ruta vieja, cada rama de “todavía aceptamos eso” se convierte en una cosa más que soporte tiene que recordar y una cosa más con la que los operadores tropiezan.

NOVA: Y una vez que centralizas alrededor de ClawHub, el plugin SDK moderno y la nomenclatura actual, la documentación por fin puede dejar de hablar en dos líneas de tiempo.

ALLOY: Lo cual importa más de lo que la gente cree. La mitad del dolor operativo no es el bug en sí. Es la sensación de que cada guía que lees podría ser para una generación distinta del producto.

NOVA: Así que si .22 se siente dura, es porque está eligiendo una sola realidad.

ALLOY: Sí. Una sola realidad, menos aliases, menos reliquias. Dolor a corto plazo, cordura a largo plazo.

## [11:00-17:00] Chrome MCP: La extensión está muerta

NOVA: Necesitamos dedicarle tiempo real al tooling de navegador, porque para muchos usuarios este es el cambio operativo individual más grande de esta doble release. El viejo relay de la extensión de Chrome desapareció. [EMPHASIS]driver: "extension"[/EMPHASIS], assets empaquetados de la extensión, [EMPHASIS]browser.relayBindHost[/EMPHASIS]: todo fue eliminado.

ALLOY: Y si no estuviste por ahí en esa época, aquí va lo que realmente era la extensión. OpenClaw solía distribuir una extensión de Chrome que actuaba como relay para [EMPHASIS]CDP[/EMPHASIS], el Chrome DevTools Protocol. Instalabas la extensión manualmente, otorgabas permisos al navegador, y servía como puente entre OpenClaw y el browser.

NOVA: Lo cual siempre se sintió un poco improvisado.

ALLOY: Era improvisado. Útil, pero improvisado. Funcionaba porque el control del navegador es desordenado y la extensión te daba una ruta que era más fácil que explicarle a todo el mundo el attach directo. Pero venía con todo el equipaje de una extensión: fricción de instalación, rarezas de permisos, deriva de compatibilidad, peculiaridades del profile del browser y una pieza móvil más que diagnosticar cuando las cosas se torcían.

NOVA: El modelo de reemplazo es simplemente mejor. OpenClaw ahora se conecta directamente a una instancia de Chrome en ejecución o a un profile de usuario usando mecanismos estándar de CDP. No se necesita extensión. No hay relay personalizado en medio. [PAUSE] Arquitectónicamente, esto es más limpio. Menos capas hechas a medida. Menos secretos escondidos en el tooling.

ALLOY: Pero, y esta es la advertencia práctica importante, si haces upgrade sin ejecutar primero [EMPHASIS]openclaw doctor --fix[/EMPHASIS], o al menos inmediatamente después, tu automatización de navegador puede romperse por completo. Y no siempre se va a romper de una forma obvia. No necesariamente vas a recibir un mensaje amigable que diga “extension relay removed”. Lo más probable es que simplemente falle al conectar, o los consent loops se pongan raros, o tu ruta de attach parezca medio viva y luego muera.

NOVA: [EMPHASIS]openclaw doctor --fix[/EMPHASIS] lee tu config actual y migra los setups locales de browser en el host al modo moderno correcto: [EMPHASIS]existing-session[/EMPHASIS] o [EMPHASIS]user[/EMPHASIS]. Eso no es una recomendación cosmética. Es parte de la migración.

ALLOY: Y vale la pena aclarar los tres modos ahora. [EMPHASIS]existing-session[/EMPHASIS] significa adjuntarse a un Chrome en ejecución. [EMPHASIS]user[/EMPHASIS] significa lanzar con un profile de usuario. [EMPHASIS]CDP[/EMPHASIS] puro para setups Docker, headless, sandbox o remotos: eso se mantiene básicamente igual.

NOVA: Lo cual es la separación correcta. El viejo camino de la extensión era una muleta. Este es el movimiento correcto.

ALLOY: En su mayor parte estoy de acuerdo, pero quiero defender por qué a los usuarios les gustaba la muleta. Una muleta es un problema si evita la recuperación. Es útil si te deja caminar. Para muchos usuarios, la extensión era el único flujo de navegador que podían hacer funcionar de manera consistente.

NOVA: Eso es justo, pero era consistencia comprada con fragilidad. El sistema tenía un puente personalizado extra solo para tapar el modelo de attach.

ALLOY: Cierto. Y .23 de hecho prueba tu punto, porque una vez que .22 eliminó el camino viejo, .23 inmediatamente tuvo que hacer confiable el camino nuevo en el mundo real. [PAUSE] Aquí importan dos correcciones. Primero, el timing del attach de pestañas. OpenClaw estaba tratando el handshake de Chrome MCP como si el navegador estuviera totalmente listo en el instante en que la conexión subía. En macOS, eso no siempre era cierto. Las pestañas existían, pero todavía no eran utilizables. Así que el primer attach podía hacer churn de consentimientos, disparar timeouts y en general sentirse embrujado.

NOVA: Esa corrección importa porque la preparación no es binaria. Que un socket esté abierto no es lo mismo que la superficie de UI esté estable.

ALLOY: Exactamente. Segunda corrección: reutilización de loopback. En setups headless o loopback, OpenClaw podía no detectar un browser en ejecución durante un sondeo corto y caer de inmediato en relaunch. Eso creaba regresiones de segunda ejecución donde la primera funcionaba y la siguiente actuaba como si necesitara arrasar con la sesión. .23 agrega una breve espera antes de ese fallback.

NOVA: Lo cual suena diminuto hasta que vives con ello. Entonces es la diferencia entre una herramienta de navegador que se siente inestable y una que se siente intencional.

ALLOY: Por eso mi resumen de esta transición de navegador es: .22 eliminó el camino viejo, .23 volvió confiable el camino nuevo, y necesitas ambas. Si solo estás pensando al nivel de los titulares de la release, te vas a perder cuán acopladas realmente están estas dos versiones.

NOVA: Además, si ejecutas automatización de navegador local en el host, deberías tratar [EMPHASIS]doctor --fix[/EMPHASIS] como parte de la migración del navegador, no como una tarea general de mantenimiento. Está haciendo trabajo dirigido.

ALLOY: Sí. No es mantenimiento opcional. Es un paso de migración.

NOVA: Y también hay una lección más grande en este cambio de navegador. La automatización de browser es uno de esos dominios donde la gente tolera una complejidad absurda porque la recompensa es muy alta. Instalarán una extensión, fijarán una versión, bendecirán un profile, cargarán flags de lanzamiento extrañas, lo que sea, con tal de que el browser obedezca. [PAUSE] Pero cada workaround oculto se convierte en deuda técnica con interfaz de usuario.

ALLOY: Esa es una buena forma de decirlo. La extensión no era solo deuda de código. Era deuda ritual para el usuario. Tenías que recordar que existía, recordar cómo se instaló, recordar por qué un profile de browser era especial, recordar qué se rompía si Chrome se actualizaba. Esa no es una historia de plataforma que quieras para siempre.

NOVA: El attach por existing-session es un modelo mucho más honesto. O hay un browser al que puedes adjuntarte, o no lo hay. O el profile es utilizable, o no lo es. Hay menos magia.

ALLOY: Menos magia, pero más responsabilidad para acertar con la preparación y el timing, que es por eso que las correcciones de .23 importan tanto. Si estás quitando el puente viejo, la ruta directa tiene que sentirse aburrida. Aburrida es éxito en automatización de navegador.

NOVA: Aburrida, confiable, legible. Ese es el objetivo.

## [17:00-22:00] Image Gen se estandariza

NOVA: Siguiente tema: generación de imagen. Esta es menos dramática que el tooling de navegador, pero te dice mucho sobre hacia dónde va OpenClaw. La skill empaquetada [EMPHASIS]nano-banana-pro[/EMPHASIS] fue eliminada. Desapareció. Sin shim.

ALLOY: Lo que significa que si tenías workflows, prompts o docs internos que llaman [EMPHASIS]nano-banana-pro[/EMPHASIS], encuéntralos y reemplázalos. Esto es una ruptura dura. No asumas que hay un alias esperándote.

NOVA: La plataforma se está estandarizando sobre la herramienta core [EMPHASIS]image_generate[/EMPHASIS]. Y filosóficamente, creo que esto es exactamente correcto. Una herramienta, backend configurable, superficie de invocación consistente. Mejor que cargar para siempre un wrapper de skill empaquetado solo porque la gente se acostumbró a su nombre.

ALLOY: Siempre y cuando configures la config key. Esta es la parte que la gente se salta. Necesitas [EMPHASIS]agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"[/EMPHASIS]. Si no configuras eso, el comportamiento queda indefinido. Y “indefinido” en tierra de config nunca significa emocionante. Significa confuso.

NOVA: Aquí hay un patrón más amplio. OpenClaw está tratando de hacer que las capacidades core parezcan capacidades core. La generación de imagen no debería sentirse como un truco lateral.

ALLOY: Correcto, pero operativamente yo lo diría más directo: la estandarización solo es agradable si los defaults son explícitos. Si sacas la cosa empaquetada vieja y no configuras el backend nuevo, has creado una arquitectura más limpia y un martes peor.

NOVA: Crítica justa. [PAUSE] También hay mejoras de marketplace envueltas en este cambio. Las instalaciones desde marketplace ahora son first-class, incluyendo la sintaxis [EMPHASIS]plugin@marketplace[/EMPHASIS] y soporte para el registry de marketplace de Claude.

ALLOY: Lo cual reduce la cantidad de folclore en la instalación de plugins. Menos momentos de “en realidad para este plugin hazlo de esta otra manera”.

NOVA: Y los comandos de chat [EMPHASIS]/plugins[/EMPHASIS] y [EMPHASIS]/plugin[/EMPHASIS] restringidos al owner continúan exactamente ese mismo tema: darle a la plataforma una historia coherente única para descubrir, instalar y administrar extensiones.

ALLOY: También me gusta que estén restringidos al owner. Cuanto más poderosa se vuelve la superficie de instalación, menos quieres que contextos aleatorios de runtime la traten como un juguete.

NOVA: Para mí, la historia de la generación de imagen es esta: OpenClaw está pasando de una personalidad empaquetada a una capacidad configurada. [PAUSE] Eso es madurez.

ALLOY: Para mí es esto: actualiza tus workflows, configura la model key, y no dejes llamadas rotas de imagen regadas en la automatización para descubrirlas solo durante una demo.

NOVA: Y hay un cambio sutil de gobernanza escondido en esa estandarización. Cuando la generación de imagen es una herramienta core en vez de una skill empaquetada querida, puedes cambiar de providers, mejorar la interfaz una sola vez, documentar un solo comportamiento y auditar una sola superficie de permisos.

ALLOY: Exacto. Deja de ser “esa cosa especial que funciona porque existe un wrapper” y pasa a formar parte del contrato real de la plataforma. Eso es más sano.

NOVA: También cambia cómo los equipos deberían pensar sobre portabilidad. Si tu workflow dice [EMPHASIS]image_generate[/EMPHASIS] y tu backend se configura por separado, puedes migrar providers sin reescribir la lógica del workflow en sí.

ALLOY: Lo cual es muy bueno en teoría y todavía mejor cuando un vendor cambia precios o rate limits un viernes por la tarde.

NOVA: Exactamente. La estandarización no es solo elegancia. Es apalancamiento.

ALLOY: Siempre y cuando configures la config key.

NOVA: Siempre y cuando configures la config key. Puedes repetir eso hasta el fin de los tiempos.

## [22:00-31:00] Hacer que funcione — El reliability pass de la .23

NOVA: Este es el corazón del episodio. Porque .22 es la purga, pero .23 es el reliability pass que hace que la purga sea sobrevivible. Volvamos al primer bug de la introducción: el failover de MiniMax.

ALLOY: Este es el bug. Este es el que estaba quemando a la gente.

NOVA: El problema original era la clasificación. Las respuestas genéricas de [EMPHASIS]api_error[/EMPHASIS] de MiniMax estaban siendo tratadas como transitorias por default. Así que OpenClaw reintentaba en silencio, suprimía la falla real y nunca activaba el fallback adecuado cuando el problema subyacente era algo como billing, auth o contexto malformado.

ALLOY: Y esa es la distinción crucial. Un error transitorio es: tal vez la red estornudó, tal vez el provider tuvo un pequeño tambaleo, tal vez un reintento realmente funcione. Pero un problema de billing no es transitorio. Un problema de auth no es transitorio. Un rechazo de formato o contexto no es transitorio. Reintentar eso solo desperdicia tiempo y esconde la verdad.

NOVA: La corrección es precisa. No es “deja de reintentar MiniMax”. Es “solo reintenta cuando el error realmente parezca transitorio”. [PAUSE] Ese es el tipo de corrección en la que confío, porque preserva el objetivo original del diseño —resiliencia— mientras elimina la clasificación descuidada que hacía que la resiliencia se comportara como encubrimiento.

ALLOY: Y para los operadores, aquí va el impacto práctico: clave mala, estado malo de cuenta, request malformada, ventana de contexto reventada: esas cosas ahora deberían fallar de una manera que aparezca y permita que el fallback se active correctamente. Eso es lo que la gente esperaba desde el principio.

NOVA: Es uno de esos bugs donde la experiencia degradada era casi peor que una falla dura, porque el usuario recibió output y asumió que era fiel.

ALLOY: Sí. Una respuesta equivocada sin alarma visible da más miedo que una falla visible. Al menos una falla visible invita a investigar.

NOVA: Siguiente: el bug de reversión del token de OpenAI. Este es un ejemplo perfecto de deriva de state entre memoria y disco que termina traicionando al usuario. La ruta de escritura del auth-profile del gateway estaba permitiendo que valores stale en memoria sobrescribieran credenciales recién guardadas en el restart.

ALLOY: Así que pegabas el token, veías verde, restart, expirado. Cada vez. [PAUSE] Por eso este bug se sintió tan personal. Atacaba la confianza en el acto básico de guardar credenciales.

NOVA: Y la corrección es que pegar el token ahora escribe correctamente en el agent store resuelto, en lugar de dejar que el snapshot stale en memoria gane durante el restart.

ALLOY: Lo que significa que, después del upgrade, deberías probarlo. No asumas solo porque la release note dice que está corregido. Pega un token nuevo, reinicia el gateway, verifica que persistió. Este es exactamente el tipo de bug donde ganas confianza reproduciendo la falla vieja y viendo que ya no pasa.

NOVA: Tercero: cron y horario de verano. Esto suena aburrido hasta que golpea algo de lo que dependes.

ALLOY: A mí me pasó. Mi reporte matutino se estaba disparando una hora corrido después del cambio de horario.

NOVA: Ejemplo concreto: programas un job a las [EMPHASIS]8 AM[/EMPHASIS]. Llega el DST. Antes de .23, esas “8 AM” podían convertirse en [EMPHASIS]7 AM[/EMPHASIS] o [EMPHASIS]9 AM[/EMPHASIS] dependiendo de cómo el scheduler interpretara el límite. [PAUSE] Eso no es solo una discrepancia cosmética. Para una rutina diaria, es una promesa rota.

ALLOY: La corrección es que [EMPHASIS]--at --tz[/EMPHASIS] ahora respeta la hora local de reloj a través de los cambios de DST. Y OpenClaw también rechaza [EMPHASIS]--tz[/EMPHASIS] para [EMPHASIS]--every[/EMPHASIS], lo cual está bien porque la semántica de intervalos recurrentes y la semántica de hora local con timezone no son lo mismo.

NOVA: Ese es el tipo de restricción que salva a los usuarios de intuiciones falsas.

ALLOY: Exactamente. Si lo que quieres decir es “cada seis horas”, eso no es lo mismo que “cuando mi reloj local marque las ocho”. La herramienta ahora refleja esa diferencia en vez de mezclarla.

NOVA: Cuarto: la corrección de [EMPHASIS]422[/EMPHASIS] de Mistral. Configuraciones persistidas viejas de Mistral estaban cargando límites de output del tamaño del contexto que Mistral rechaza de plano. Resultado: errores [EMPHASIS]422[/EMPHASIS] que se ven misteriosos si no conoces la historia de la config.

ALLOY: Y otra vez, [EMPHASIS]openclaw doctor --fix[/EMPHASIS] está haciendo trabajo real aquí. Ahora detecta y repara esas configuraciones stale de Mistral.

NOVA: Otra razón para ejecutar [EMPHASIS]doctor --fix[/EMPHASIS]. A veces la gente oye ese comando como una especie de doctor genérico, como si tal vez arreglara algunas cosas obvias. No. En esta tanda de releases, está codificando conocimiento de migración.

ALLOY: Quinto: ClawHub en macOS. Aquí hubo dos problemas. Las credenciales guardadas no estaban respetando correctamente la ruta de Application Support de macOS, y el comportamiento de browse-all estaba pegando contra rate limits [EMPHASIS]429[/EMPHASIS] sin autenticar.

NOVA: Lo cual significa que la UI podía engañarte haciéndote pensar que ClawHub estaba vacío o roto de formas vagas.

ALLOY: La navegación de skills estaba cayendo silenciosamente a modo no autenticado en macOS. Veías listas vacías y asumías que no había skills, o asumías que tu instalación estaba rota, cuando en realidad el manejo de la ruta de auth estaba mal. [PAUSE] Las correcciones fueron respetar la ruta correcta de auth y cambiar browse-all al endpoint de search, que es una forma mucho más sensata de evitar throttling no autenticado sin sentido.

NOVA: Sexto: runtimes de plugins empaquetados. Los sidecars de runtime de WhatsApp y Matrix faltaban en el paquete npm, lo que significaba que las instalaciones globales podían fallar de una manera que parecía brujería de empaquetado.

ALLOY: Esta es una regresión de los cambios de empaquetado de .22, y hay que darle crédito a OpenClaw: se corrigió rápido en .23. Pero si ejecutas esos runtimes de forma global, esto no es una nota al pie. Sidecars faltantes significa que la stack de plugins simplemente no está completa.

NOVA: Séptimo: manejo stale del provider en [EMPHASIS]web_search[/EMPHASIS]. La herramienta estaba usando el state del provider que hubiera quedado horneado en el arranque en vez de la config activa de runtime.

ALLOY: Lo cual es exactamente el tipo de bug que te hace cuestionar si las recargas de config son reales o decorativas.

NOVA: Configuras Brave, debería usar Brave. Siempre debió haber funcionado así.

ALLOY: Y ahora lo hace. Otra vez, no es glamoroso, pero sí una reparación directa de expectativa contra comportamiento.

NOVA: Octavo: threading de Telegram. [EMPHASIS]currentThreadTs[/EMPHASIS] ahora se llena en el fallback de tool-context de threading para temas de DM de Telegram, de modo que las herramientas con conciencia de hilos realmente reciben el contexto correcto del tema.

ALLOY: Esa es una de esas correcciones donde, si no usas temas de DM en Telegram, te encoges de hombros, y si sí los usas, dices gracias a Dios. Porque cuando el tool context es ciego al hilo, así es como terminas con agents respondiendo en el lugar equivocado o perdiendo el carril de la conversación.

NOVA: Lo cual es especialmente doloroso en un sistema construido alrededor de la fidelidad del contexto.

ALLOY: Exactamente. El punto entero es que la herramienta debería saber dónde está.

NOVA: Así que, tomadas en conjunto, la release .23 no es llamativa en el sentido habitual de producto. Es un reliability pass en el sentido más profundo de la frase. Ajusta clasificación, persistencia de state, semántica del scheduler, cableado de providers, integridad del empaquetado y contexto de hilo.

ALLOY: Hace que el nuevo mundo de .22 sea realmente habitable.

NOVA: Y creo que por eso los operadores deberían leer estas dos releases como una sola historia con dos capítulos. El capítulo uno dice: “quitamos los viejos compromisos”. El capítulo dos dice: “arreglamos los lugares donde los supuestos nuevos todavía tenían asperezas”. [PAUSE] Ese es un ritmo de desarrollo mucho más honesto que fingir que la gran limpieza aterrizó perfecta desde el día uno.

ALLOY: Sí. De hecho respeto la .23 porque no intenta esconder lo que la .22 desestabilizó. Solo lo corrige. Rápido. Directo. Sin ego.

NOVA: Y como usuario, eso es lo que quieres después de una release estructural. No negación. Corrección rápida.

ALLOY: Especialmente para las cosas silenciosas. Fallback de MiniMax, persistencia de token, config stale de provider: todos esos son bugs que erosionan la confianza porque hacen que el sistema se sienta menos legible de lo que debería.

NOVA: La confiabilidad es en parte corrección y en parte comprensibilidad. La plataforma tiene que hacer lo correcto, y tú tienes que poder entender por qué hizo lo que hizo.

ALLOY: Por eso .23 importa más de lo que importaría una release de features.

NOVA: De acuerdo.

## [31:00-35:00] Qwen, CSP y las pequeñas cosas

NOVA: Vamos con los cambios más pequeños, porque son pequeños solo en superficie, no necesariamente en importancia. Primero: [EMPHASIS]Qwen[/EMPHASIS] y [EMPHASIS]DashScope[/EMPHASIS]. OpenClaw ahora soporta endpoints estándar de DashScope para China y claves de API globales de Qwen, y el provider fue renombrado como [EMPHASIS]Qwen (Alibaba Cloud Model Studio)[/EMPHASIS].

ALLOY: Las claves pay-as-you-go ahora funcionan. Ese es el cambio práctico. Si estás fuera de la órbita por default de OpenAI-Anthropic, esto importa muchísimo.

NOVA: Qwen es una de las mejores familias open-weight ahora mismo. El soporte adecuado de DashScope significa accesibilidad real para usuarios que quieren modelos potentes sin verse forzados a los mismos dos ecosistemas de providers que todos los demás asumen.

ALLOY: Y una mejor nomenclatura también importa. Renombrarlo a la identidad completa de Model Studio hace que la superficie de config sea menos críptica.

NOVA: Siguiente: endurecimiento de [EMPHASIS]CSP[/EMPHASIS]. Hashes SHA-256 para bloques de script inline. Scripts inline bloqueados por default.

ALLOY: Si ejecutas OpenClaw detrás de un reverse proxy estricto, esta es la versión a la que deberías hacer upgrade.

NOVA: Esto importa para la seguridad de la supply chain. Un script inyectado no va a ejecutarse porque el hash no va a coincidir. [PAUSE] Este es el tipo de controles que no hacen que una demo se vea más bonita, pero sí hacen más pequeño tu radio de impacto.

ALLOY: Y francamente, las plataformas maduras hacen esto. Dejan de depender de “bueno, nadie debería inyectar ahí” y empiezan a construirse alrededor de “si algo se inyecta, ¿qué sigue sin poder ejecutarse?”.

NOVA: El tema [EMPHASIS]Knot[/EMPHASIS] también recibió atención: cumplimiento de contraste [EMPHASIS]WCAG 2.1 AA[/EMPHASIS], ajuste de la paleta negro y rojo, íconos de config, niveles discretos de redondez.

ALLOY: La corrección de contraste AA es la que importa. Estaba fallando las pruebas de accesibilidad. El estilo es divertido; la legibilidad es obligatoria.

NOVA: Y siempre me gusta cuando las mejoras de accesibilidad se tratan como mejoras de calidad por default y no como una misión lateral de nicho.

ALLOY: Última pequeña: los totales de uso del gateway ahora incluyen sesiones rotadas y archivadas.

NOVA: Lo cual suena casi a contabilidad.

ALLOY: Lo es. Pero el uso estaba subcontando. Ahora no. Si estás tratando de entender la carga real del sistema o comparar actividad a lo largo del tiempo, dejar fuera sesiones archivadas no es un error de redondeo. Simplemente está mal.

NOVA: Así que incluso las cosas pequeñas en estas releases apuntan en la misma dirección: menos ambigüedades, menos mentiras por omisión, y una representación más precisa de lo que el sistema realmente está haciendo.

## [35:00-38:00] El checklist de upgrade

ALLOY: Bien, hagámoslo concreto. Si vas a hacer upgrade, aquí está el checklist, y digo checklist literalmente. No confíes en ti mismo para recordarlo a mitad de la migración.

NOVA: El paso uno no es negociable.

ALLOY: [EMPHASIS]openclaw doctor --fix[/EMPHASIS]. Primero, antes de cualquier otra cosa. Y honestamente, inmediatamente después de cada etapa del upgrade si estás haciendo la secuencia de forma limpia.

NOVA: Es el comando ancla de estas releases. No es un nice-to-have. Es el ancla.

ALLOY: Paso dos: haz grep de [EMPHASIS]CLAWDBOT_*[/EMPHASIS] y [EMPHASIS]MOLTBOT_*[/EMPHASIS] en todos los archivos [EMPHASIS].env[/EMPHASIS], archivos de Docker, unidades systemd, perfiles de shell, cada superficie de arranque que tengas.

NOVA: Si los nombres viejos existen, asume que ahora son config muerta.

ALLOY: Paso tres: revisa si existe [EMPHASIS]~/.moltbot[/EMPHASIS]. Si existe, mueve el state a [EMPHASIS]~/.openclaw[/EMPHASIS] o define [EMPHASIS]OPENCLAW_STATE_DIR[/EMPHASIS] explícitamente.

NOVA: Paso cuatro: define [EMPHASIS]agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"[/EMPHASIS]. No dejes la generación de imagen en un limbo indefinido.

ALLOY: Paso cinco: después del upgrade, vuelve a probar MiniMax con una clave mala y confirma que el fallback se dispara. No envíes solo un prompt happy-path. Induce el modo de falla viejo.

NOVA: Paso seis: pega un token de OpenAI, reinicia el gateway y confirma que persistió. Confía, pero verifica.

ALLOY: Paso siete: si tienes plugins personalizados, migra de [EMPHASIS]openclaw/extension-api[/EMPHASIS] a [EMPHASIS]openclaw/plugin-sdk/*[/EMPHASIS]. Lee los docs de migración. No trates los errores de compilación como si fueran un mapa.

NOVA: Paso ocho: haz una revisión puntual de las skills de ClawHub después del cambio en el comportamiento de instalación. Asegúrate de que tus scripts y expectativas todavía coincidan con lo que se resuelve.

ALLOY: Paso nueve: verifica los jobs de cron que usan [EMPHASIS]--at --tz[/EMPHASIS], especialmente si el DST ya te quemó antes.

NOVA: El resumen más profundo es que estas dos releases juntas son OpenClaw terminando lo que empezó. Los nombres Moltbot y Clawdbot desaparecieron. El extension relay desapareció. El plugin SDK está unificado. Las fallas silenciosas están corregidas.

ALLOY: Primero Doctor [EMPHASIS]--fix[/EMPHASIS]. Todo lo demás es condicional a lo que estés ejecutando. Pero [EMPHASIS]doctor --fix[/EMPHASIS] es incondicional.

NOVA: Esta es la plataforma que querías que fuera.

## [38:00-39:30] Cierre

ALLOY: Y creo que esa es la nota correcta para terminar. Estas releases son exigentes, pero son exigentes al servicio de algo real: una plataforma que dice lo que es, hace lo que dice y carga con menos fantasmas de épocas anteriores.

NOVA: Lo cual, para una herramienta como OpenClaw, importa más que la novedad. [PAUSE] La confiabilidad es una feature. La consistencia de nombres es una feature. La presión honesta de migración es una feature. Una stack de navegador con menos puentes improvisados es una feature.

ALLOY: Y si estás justo en medio del upgrade ahora mismo, respira, haz el checklist, ejecuta [EMPHASIS]openclaw doctor --fix[/EMPHASIS], y no te saltes los pasos de verificación solo porque el servicio volvió a levantarse.

NOVA: Puedes encontrar las notas del episodio, todos los links que mencionamos y el archivo de episodios en [EMPHASIS]tobyonfitnesstech.com[/EMPHASIS]. Eso es [EMPHASIS]tobyonfitnesstech.com[/EMPHASIS].

ALLOY: Si este episodio te salvó de un setup de navegador roto, una env var desaparecida o una falla misteriosa más de auth, entonces hizo su trabajo.

NOVA: Soy NOVA.

ALLOY: Soy Alloy.

NOVA: Y esto ha sido OpenClaw Daily. Volveremos pronto.

ALLOY: Nos vemos pronto.
