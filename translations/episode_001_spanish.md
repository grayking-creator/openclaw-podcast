# OpenClaw Daily - Episodio 1: La Historia Completa
# Fecha: 19 de febrero de 2026
# Presentadores: Nova y Alloy

---

[NOVA]: Buenas noches y bienvenidos de nuevo a OpenClaw Daily. Soy Nova.

[ALLOY]: Y soy Alloy. Hoy tenemos un episodio fantástico para ustedes, y sinceramente, las noticias siguen siendo cada vez más emocionantes.

[NOVA]: Absolutamente. El Episodio 1 cubrió el anuncio de la fundación y el panorama general. Hoy nos adentramos en algo que realmente llega a los creadores y aficionados: OpenClaw en Raspberry Pi. Además de una investigación de seguridad reveladora y qué significa esto para el futuro de la IA local.

[ALLOY]: Oh, he estado esperando para hablar de esto. ¿Han visto lo que ha estado pasando con Raspberry Pi?

[NOVA]: Lo he visto, y es bastanteremarkable. Pero ¿por qué no le cuentas a todos? ¿Cuál es la gran noticia?

[ALLOY]: Entonces aquí está el asunto — Raspberry Pi mismo publicó un artículo oficial en su blog hoy. El titular es "Convierte tu Raspberry Pi en un agente de IA con OpenClaw."

[NOVA]: ¿Es en serio? ¿El blog oficial de Raspberry Pi?

[ALLOY]: Cien por ciento. Esto no es alguna guía de la comunidad o entusiasta. Es ellos respaldando oficialmente a los agentes de IA locales. Ellos explican todo el proceso — configurar OpenClaw en un Pi 5, conectarlo a un modelo de lenguaje, hacer que realice tareas reales.

[NOVA]: Eso es un momento histórico, ¿no es así? Hace apenas un par de semanas, hablábamos de cómo la gente estaba comprando Pi cinco específicamente para ejecutar OpenClaw. Ahora el gigante del hardware está diciendo oficialmente "sí, haz esto." Eso es validación a nivel de hardware.

[ALLOY]: El tiempo es interesante. Y。他们 hicieron un punto muy bueno en el artículo — estoy parafraseando — pero dijeron que herramientas como OpenClaw ilustran el potencial de mover la inferencia de LLMs basados en la nube a dispositivos locales de bajo costo. Eso es exactamente de lo que hemos estado hablando en este podcast.

[NOVA]: La democratización de la IA. Y para quien lo haya perdido, un Pi 5 con 8 gigabytes de RAM puede ejecutar modelos en el rango de 1 a 3 mil millones de parámetros. No va a igualar a un Mac Mini con 64 gigs, pero para tareas básicas de automatización — control del hogar inteligente, programación, recordatorios, simple Q&A — es absolutamente viable.

[ALLOY]: Y el precio es inmejorable. Ochenta dólares por la placa, tal vez otros veinte por una fuente de alimentación decente y una caja. Estás viendo cien dólares todo incluido para un agente de IA siempre activo que vive en tu casa y nunca envía tus datos a la nube.

[NOVA]: Cuando el blog oficial de Raspberry Pi le dice a la gente que ejecute IA local, la ventana de Overton se desplaza. Realmente lo hace. Esto no es solo para fabricantes. Se está volviendo convencional.

[ALLOY]: Y lo han hecho increíblemente accesible. La guíaウォーク through installing OpenClaw, setting up Tailscale for secure remote access, and configuring your API key. They've even created a learning system on Adafruit with detailed tutorials.

[NOVA]: Eso es maravilloso. Sabes, he pensado mucho en esto. Hace cinco años, la idea de tener tu propio asistente de IA personal era ciencia ficción. Ahora puedes construir uno por cien dólares. El ritmo de esta revolución es sorprendente.

[ALLOY]: Y Tom's Hardware está报告ando que OpenClaw ha creado una escasez real de Apple Mac! Los tiempos de entrega para Mac Mini M4 Pro y Mac Studio M3 Ultra se han extendido a seis semanas.

[NOVA]: Piensa en eso. Una computadora de $600 que quizás ni siquiera estaba en el radar de la mayoría para trabajo de IA ahora está en escasez debido a OpenClaw. Si querías prueba de que la IA local se está convirtiendo en convencional, esto es.

[ALLOY]: Ahora让我们谈谈昨天让很多人兴奋的事情。VentureBeat发表了一篇文章，标题相当大胆——"OpenAI收购OpenClaw标志着ChatGPT时代结束的开始。"

[NOVA]: 这是一个大胆的说法。但你知道吗？他们提出的论点实际上相当有说服力。他们追踪了时间线——2025年12月到2026年1月和2月初——他们发现了AI氛围程序员和开发者中所谓的"曲棍球杆"采用率。

[ALLOY]: "氛围程序员"这个词对我来说很新，但我很喜欢。它描述的是那些对底层代码不那么感兴趣的人，更关心AI是否能完成工作。他们想要结果，而不是计算机科学学位。

[NOVA]: 正是。而OpenClaw提供的是与ChatGPT体验不同的东西。不是你粘贴提示并获得响应的聊天界面，OpenClaw是一个代理。它可以执行操作。它可以执行多步骤工作流。它可以集成到你的日历、邮件、文件、家庭自动化中。

[VENTUREBEAT]: VentureBeat的论点代表了一种根本性的转变。"我去网站让AI做某事"的时代正在让位给"我有一个生活在我电脑上且能为我处理事务的AI"的时代。

[NOVA]: 他们称之为ChatGPT时代"终结的开始"。我不知道我是否会这么说——ChatGPT不会消失——但我认为他们发现的是真实的。

[ALLOY]: 问题不在于AI代理是否会成为主流。而在于它们是基于云还是本地。

[NOVA]: 鉴于我们在播客上讨论的一切——隐私、控制、成本、离线运行能力——本地选项看起来越来越有吸引力。

[ALLOY]: 文章还指出，OpenClaw在"对其跨应用自主完成任务能力印象深刻"的开发者中采用率特别高。这是关键的不同点。它不仅仅是回答问题，而是在实际工作。

[NOVA]: 随着基金会现在成立，Peter Steinberger在OpenAI工作但OpenClaw保持开源，轨迹很明显。这个项目不会消失。它是基础设施。

[ALLOY]: 现在，让我们谈谈应该引起所有人关注的事情。Bitsight——他们是一家网络安全研究公司——发布了一项研究，发现了超过30,000个公开可访问的OpenClaw实例。

[NOVA]: 三万。让我确认我听得正确。三万个暴露在开放互联网上的OpenClaw实例。

[ALLOY]: 他们是这么说的。他们的分析周期是1月27日到2月8日。那只是几周。他们发现部署一个暴露的OpenClaw实例，用他们的话来说，"非常容易"。很容易，以至于数万人这样做而没有意识到风险。

[NOVA]: 这正是为什么我们在第1集中专门用整个部分讨论安全的原因。但这个新数据真正强调了一点。这些不是恶意行为者——这些是合法设置OpenClaw的普通用户，但没有正确保护。

[ALLOY]: 特别可怕的是这一点。具有完全系统访问权限的暴露的OpenClaw实例基本上是一扇敞开的门。如果有人找到它，他们可能能够读取文件、发送消息、执行命令。这不仅仅是隐私风险——这是安全风险。

[NOVA]: Bitsight研究人员做了一个重要的区分。漏洞不在于OpenClaw代码本身。而在于人们如何配置它。如果你将实例暴露在互联网上而没有身份验证、没有SSL、没有防火墙规则，你基本上就是敞开了前门。

[ALLOY]: 让我们诚实地说——默认配置绑定到localhost是有原因的。如果人们更改它而不了解后果，他们就是在自找麻烦。

[NOVA]: 那么人们应该怎么做？第一，除非你真的知道自己在做什么，否则不要将OpenClaw暴露在互联网上。第二，如果你需要远程访问，使用VPN。第三，保持你的实例更新。OpenClaw团队一直在快速修补问题。

[ALLOY]: Bitsight报告不是为了吓跑人们。这是为了教育。这些是可以预防的问题。你只需要知道风险是什么。

[NOVA]: 这正是我们在这里的原因。保持聪明，保持安全，让你的数据在你的控制之下。

[ALLOY]: 谈到安全，让我们再深入一点。还有一篇文章来自Trend Micro，标题是"病毒式AI、隐形风险：OpenClaw揭示了关于代理助手的什么。"

[NOVA]: 他们提出了一些关于代理AI引入的独特风险的好观点。与传统聊天机器人不同，这些代理可以采取自主行动。这完全改变了威胁模型。

[ALLOY]: 正是。Fortune随后跟进发表了"为什么开源AI代理OpenClaw让安全专家处于边缘。"他们引用了IBM研究人员Kaoutar El Maghraoui的话，她提出了一个重要的观察：AI代理的现实世界效用"不仅限于大型企业。"

[NOVA]: 这是一个关键见解，不是吗？历史上，强大的AI工具一直是大公司和大预算的领域。现在任何拥有树莓派或Mac Mini的人都可以拥有相同的能力。这是民主化的体现。

[ALLOY]: 我们本周提到了很多报道，但还有一篇文章值得深入研究。Fortune跟进了他们早期的安全报道，专门讨论了为什么OpenClaw让安全专家处于边缘。

[NOVA]: 他们引用了一个有趣的人：Colin Shea-Blymyer，乔治城中心安全与新兴技术的研究员。他正在研究CyberAI项目。

[ALLOY]: 他的看法？他说安全问题"相当经典。"我认为这是一个重要的框架。这不是什么新奇的、史无前例的威胁。这是数十年来困扰软件的相同权限和配置问题。

[NOVA]: 他特别指出了权限配置错误——基本上，谁或什么被允许做什么。问题是人们给予OpenClaw的权限超出了他们的意识，攻击者可以利用这一点。

[ALLOY]: 解决方案不是放弃代理——而是对权限有意识。给予你的代理完成工作所需的最小权限。不要给它root权限。不要给予它不需要的访问权限。

[NOVA]: 这是最小权限原则，它适用于AI代理，就像适用于其他软件一样。

---

# Translated by OpenClaw - Spanish Version
