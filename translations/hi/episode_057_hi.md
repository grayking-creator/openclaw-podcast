[NOVA]: मैं NOVA हूं।

[ALLOY]: मैं ALLOY हूं, और यह AgentStack Daily है। आज OpenClaw v2026.5.22 और Claude Code 2.1.149 के साथ शुरू होता है, क्योंकि दोनों रिलीज़ ने उस मशीनरी को बदल दिया है जिस पर agent stacks निर्भर करते हैं: gateway startup, plugin metadata, meeting notes, Discord callbacks, cloud MCP connectors, usage accounting, diffs, और shell safety।

[NOVA]: फिर खबरें बाहर की ओर बढ़ती हैं। Google Gemini agents को managed remote Linux environments में बदल रहा है। OpenAI Codex work को mobile supervision में डाल रहा है और hybrid enterprise setups में ले जा रहा है। Anthropic ने Stainless खरीदा और Project Glasswing को अपडेट किया, जो SDK generation, MCP servers, और AI security scanning को एक ही बातचीत में लाता है।

[ALLOY]: और GitHub project lane आज असली है: semantic code maps, current documentation tools, model routers, MCP builders, local agents, role packs, और security scanners। Repo trivia नहीं। ऐसे टूल्स जो Claude Code, Codex, Hermes, OpenClaw, और MCP clients वास्तव में क्या देख और कर सकते हैं उसे बदल सकते हैं। ...

[NOVA]: OpenClaw v2026.5.22 एक घना रिलीज़ है, लेकिन headline साफ है: gateway कम brittle होती है, plugin surface ज्यादा reusable होती है, meeting notes agent context का बेहतर स्रोत बनती हैं, और कई provider और media paths तेज होती हैं।

[ALLOY]: gateway startup से शुरू करें। OpenClaw अब process-stable channel catalog reads और plugin metadata snapshot reuse का उपयोग करता है। इसका मतलब है कि सिस्टम stable catalog और metadata state पर भरोसा कर सकता है बजाय बार-बार दुनिया की एक ही तस्वीर बनाने के। एक local agent host के लिए, यह मायने रखता है क्योंकि startup और status checks पहला friction point हैं। अगर host task शुरू होने से पहले шумी है, तो उसके ऊपर की सब कुछ अविश्वसनीय लगता है।

[NOVA]: Lazy startup-idle plugin work उसी bucket में आता है। वह काम जिसे पहले usable moment को block करने की जरूरत नहीं है, इंतज़ार कर सकता है। Irrelevant Linuxbrew path probes छोड़ दिए जाते हैं। Core gateway method handlers और public-surface alias maps साफ किए जाते हैं। ये flashy features नहीं हैं, लेकिन वे control plane की feel बदलते हैं: कम pointless checks, ज्यादा predictable method names, और कम काम सिर्फ इसलिए हो रहा है क्योंकि process जागा है।

[ALLOY]: Meeting notes को सबसे जरूरी capability update मिलती है। External meeting-notes plugins और source providers के पास अब cleaner contract है। Capture config से auto-start हो सकता है। Manual imports समर्थित हैं। Read-only CLI access मौजूद है। Discord voice को side entrance की जगह first live source के रूप में माना जाता है।

[NOVA]: यह एक real agent-stack feature है क्योंकि बहुत सारी valuable instruction neat typed text के रूप में नहीं आती। यह एक call, एक voice note, एक quick correction, या एक channel discussion के रूप में आती है। उन sources को structured, readable context में बदलना बिना हर tool को source record पर write access दिए - यही useful part है।

[ALLOY]: Plugin SDK में भी ordinary operations ज्यादा बनते हैं: generic channel-message poll sending, session workflow helpers, और clearer embedding-provider capability contracts। यह plumbing जैसा लगता है, लेकिन यह वही plumbing है जो हर plugin author को एक ही tool call का थोड़ा अलग version invention से रोकता है।

[NOVA]: Subagents भी कम wasteful होते हैं। Default bootstrap कम important files की तरफ trimmed down होता है, और native subagent completion handoff को fixes मिलते हैं। Practice में, एक delegated agent को task करने के लिए enough context चाहिए और answer return करने का reliable path चाहिए। बहुत ज़्यादा inherited context subagent को sluggish बनाता है; broken handoff अच्छे काम को गलत जगह पर disappear कर देता है।

[ALLOY]: Chat-session picker को search और Load More pagination मिलती है। यह तब तक एक छोटा UI feature है जब तक system के पास weeks की real sessions न हों। फिर old run find करना work का हिस्सा बन जाता है। History वाला gateway को navigation चाहिए, सिर्फ recent chats का pile नहीं।

[NOVA]: Discord component callbacks की अब bounded lifetime है। Review buttons, approvals, और छोटे interactive controls के लिए यह healthy change है। Old message पर button को हमेशा के लिए live नहीं रहना चाहिए बस message के exist होने की वजह से। Interaction surface की अब clearer expiration model है।

[ALLOY]: Provider handling भी ज़्यादा concrete होती है। xAI OAuth को Grok web search के लिए reuse किया जा सकता है। Model aliases और operation timeouts को cleanup मिलती है। Antigravity CLI configured provider APIs के बाद lower-priority image और video fallback बन जाती है। Codex API-key image generation native OpenAI Images API का उपयोग करती है। Local Chrome और local Ollama proxy bypasses को fixes मिलते हैं।

[NOVA]: यही real provider story है: सिर्फ यह नहीं कि कौन सा model answer देता है, बल्कि auth कैसे reuse होती है, calls कितनी देर तक run होने दी जाती हैं, कौन सा fallback जीतता है, और क्या local services गलत proxy के through accidentally routed हो जाती हैं। Agent stacks उन edges पर उतनी ही fail करते हैं जितनी reasoning में।

[ALLOY]: OpenClaw dependencies को भी refresh करता है, protobufjs को 8.4.0 पर ले जाता है, locked dependency work को tighten करता है, catalogs को prune करता है, session write locks को clean up करता है, vLLM tool-free turns के लिए stricter behavior जोड़ता है, और Telegram topic handling fix करता है। यह एक maintenance release है जिसकी long tail है, लेकिन shape coherent है: startup, source capture, plugin reuse, provider correctness, session navigation, और dependency hygiene।

[NOVA]: Claude Code update छोटा है, लेकिन यह daily use में आता है। /usage command limit usage को category के हिसाब से breakdown कर सकता है: skills, subagents, plugins, और per-MCP-server cost। यह meaningful change है क्योंकि coding-agent sessions अब एक model call नहीं रहे। वे tool calls, MCP calls, helper agents, skills, plugins, और कभी-कभी background work हैं। Usage को map चाहिए।

[ALLOY]: /diff detail view को keyboard scrolling मिलती है। Markdown output GitHub-flavored task-list checkboxes render करता है। ये ergonomic fixes हैं, लेकिन terminal agents review surfaces पर live और die करते हैं। Better diff view और clearer task lists का मतलब है कम friction जब एक human decide कर रहा है कि agent ने actually वह चीज़ की या नहीं।

[NOVA]: Enterprise admins को allowAllClaudeAiMcps मिलता है, managed MCP config के साथ claude.ai cloud MCP connectors load करने की managed setting। यह MCP story का policy side है। Cloud connectors useful हैं, लेकिन organizations को clear switch चाहिए कि कौन से connector surfaces allowed हैं instead of यह कि हर user improvise करे।

[ALLOY]: Fixes ज़्यादा serious part हैं। Claude Code PowerShell permission bypasses को repair करता है built-in directory-changing functions के through। यह sandbox write allowlists fix करता है जो git worktree के बहुत ज़्यादा हिस्से को cover कर सकते थे। यह PowerShell prefix और wildcard rule bugs fix करता है। यह PWD, OLDPWD, और DIRSTACK के around stale variable tracking correct करता है। यह एक macOS find problem fix करता है जो large directories पर file tables exhaust कर सकती थी।

[NOVA]: यह एक shell-safety release note है, बस bug list नहीं। Coding agents messy environments में commands run करते हैं। Directory-changing builtins, wildcard rules, worktrees, environment variables, और file-descriptor limits वो जगहें हैं जहाँ एक safe-looking policy leak कर सकती है। एक CLI agent जो permissions को seriously लेती है उसे उन boring edges को handle करना पड़ता है।

[ALLOY]: Next patch npm latest पर है, लेकिन उसका changelog entry सिर्फ internal infrastructure का है। तो user-facing delta वो earlier patch है जिसे हमने अभी cover किया। यह distinction important है: install numbers move कर सकती हैं, लेकिन feature story उस release की है जिसने actually behavior बदला।

[NOVA]: Codex और Hermes के पास इस release readout के लिए newer stable tags नहीं हैं, लेकिन वे episode में रहती हैं क्योंकि remote Codex supervision, MCP tooling, local agents, और code-intelligence repos के चारों ओर की news उसी stack को affect करती है। Release segment foundation है; episode का बाकी हिस्सा वह है जहाँ उस foundation का environment move कर रहा है। ...

[ALLOY]: इस OpenClaw release का सबसे сильная use case एक gateway है जिसे एक साथ कई real surfaces host करने पड़ते हैं: chat, voice, plugins, media generation, search, और subagents। एक toy setup awkward startup behavior survive कर सकता है। एक daily build नहीं कर सकता। जब channel catalogs, plugin metadata, source capture, और provider fallbacks सब एक ही release में cleaner होते हैं, तो agent host lucky paths का pile कम हो जाता है।

[NOVA]: Claude Code update का सबसे сильная use case एक team है जो एक terminal और एक model call से आगे बढ़ गया है। Usage by category बताती है कि skills, plugins, subagents, या MCP servers limits drive कर रहे हैं या नहीं। Better diff navigation code review को कम painful बनाती है। Cloud MCP policy administrators को एक clearer build surface देती है। PowerShell और sandbox fixes वो guardrails हैं जो उन features को real shells में कम scary बनाती हैं।

[ALLOY]: एक साथ मिलाकर, release news सिर्फ "अपने tools update करो" नहीं है। यह है कि local gateway और coding CLI दोनों agent work के hard lessons absorb कर रहे हैं: context messy sources से आता है, tools को policy चाहिए, provider behavior को names चाहिए, और shell boundaries को precise होना चाहिए। यह build direction देखना है।

[ALLOY]: Google's Gemini story के दो layers हैं। पहला model है: Gemini 3.5 Flash agentic work और coding के लिए position किया गया है, Terminal-Bench, GDPval-AA, MCP Atlas, multimodal speed, और long-horizon tasks के claims के साथ।

[NOVA]: वे benchmark names मायने रखती हैं क्योंकि वे tool-heavy work की ओर इशारा करती हैं। एक model chat में charming हो सकती है और फिर भी टूट सकती है जब उसे terminal use करना पड़े, tools call करने पड़ें, files inspect करने पड़ें, bad observations से recover करना पड़े, और एक long task में state बनाए रखना पड़े। Google स्पष्ट रूप से Flash को loops के लिए fast enough और agent work के लिए capable enough बेचने की कोशिश कर रही है।

[ALLOY]: दूसरा layer ज्यादा important है: Gemini API Managed Agents। Developers एक Antigravity-powered agent को isolated, ephemeral Linux environment में start कर सकते हैं। Agent reason कर सकता है, tools call कर सकता है, code execute कर सकता है, files manage कर सकता है, और web browse कर सकता है। Follow-up calls environment reuse कर सकते हैं, तो एक task actual session state के साथ continue कर सकता है जबकि यह pretend नहीं करता कि हर request कहीं से शुरू होती है।

[NOVA]: वह environment model product है। यह सिर्फ "model को prompt भेजो" नहीं है। यह remote Linux workspace है जिसमें tools, files, browsing, continuation, और agent instructions हैं। Google यह भी कहती है कि custom agents AGENTS.md और SKILL.md-style files, plus extra data के साथ define किए जा सकते हैं। यह एक clear signal है कि model के चारों ओर की harness first-class API surface बनती जा रही है।

[ALLOY]: OpenClaw, Hermes, Codex और Claude Code उपयोगकर्ताओं के लिए, दिलचस्प तुलना स्थानीय बनाम क्लाउड के रूप में नहीं है। यह इस बारे में है कि वातावरण को क्या जानने और करने की अनुमति है। एक प्रबंधित सैंडबॉक्स तब उपयोगी होता है जब कार्य सार्वजनिक, एकबारगी, या रीसेट करने में आसान हो: ओपन-सोर्स रेपो की जांच करना, एक साफ पुनरुत्पादन चलाना, डॉक्स ब्राउज़ करना, संवेदनशील न होने वाले डेटासेट को बदलना, या नियंत्रित वर्कस्पेस में प्रोटोटाइप बनाना।

[NOVA]: जब काम निजी फाइलों, स्थानीय क्रेडेंशियल्स, सब्सक्राइब्ड टूल्स, असली ब्राउज़र प्रोफाइल, डिवाइस एक्सेस, या मशीन-विशिष्ट सेटअप पर निर्भर होता है, तब भी स्थानीय एजेंटों का फायदा रहता है। प्रबंधित-एजेंट खबर स्थानीय स्टैक को मिटाती नहीं है। यह बिल्डर्स को एक और एक्जीक्यूशन आकार देती है: व्यक्तिगत वर्कस्टेशन स्टेट के बजाय डिस्पोजेबल रिमोट स्टेट।

[ALLOY]: याद रखने योग्य फीचर डेल्टा स्टेटफुल प्रबंधित एक्जीक्यूशन है। एक रिमोट एजेंट जो फाइलें रख सकता है, सत्र जारी रख सकता है, और अलग-थलग लिनक्स वातावरण के अंदर ब्राउज़ कर सकता है, वह स्टेटलेस मॉडल एंडपॉइंट से अलग है। यह साक्ष्य इकट्ठा कर सकता है। यह डिपेंडेंसी इंस्टॉल कर सकता है। यह अगली कॉल के लिए आर्टिफैक्ट छोड़ सकता है। यह प्लेटफॉर्म के सैंडबॉक्स और टूल मॉडल के चारों ओर लॉक-इन भी बना सकता है।

[NOVA]: इसीलिए कस्टम इंस्ट्रक्शन-फाइल सपोर्ट मायने रखता है। AGENTS.md और SKILL.md-स्टाइल फाइलें वातावरण को प्रोजेक्ट नियम और विशेष व्यवहार ले जाने देती हैं। कोडिंग एजेंटों में यही रुझान दिखता है: मॉडल केवल एक हिस्सा है। नियम, टूल्स, फाइलसिस्टम, ब्राउज़र, पॉलिसी, और कंटिन्यूएशन मॉडल तय करते हैं कि एजेंट सॉफ्टवेयर की तरह काम कर सकता है या केवल सॉफ्टवेयर के बारे में बात कर सकता है।

[ALLOY]: व्यावहारिक सिफारिश छोटी है: जहां आइसोलेशन बिंदु है, वहां पहले प्रबंधित Gemini एजेंटों का उपयोग करें। पब्लिक रेपो ट्रायज, साफ बग पुनरुत्पादन, जेनरेटेड स्क्रिप्ट, और डॉक-बैक्ड रिसर्च सहज फिट हैं। सीक्रेट्स, प्राइवेट रेपो, और मशीन-विशिष्ट वर्कफ़्लो को स्थानीय या कसकर नियंत्रित वातावरण में रखें जब तक कि प्रबंधित सीमा स्पष्ट रूप से समझ नहीं आ जाती।

[NOVA]: बड़ा उद्योग संकेत यह है कि एजेंट इन्फ्रास्ट्रक्चर अब सीधे बेचा जा रहा है। आंतरिक ऑर्केस्ट्रेशन में छिपाया नहीं गया, डेमो के रूप में जोड़ा नहीं गया। सैंडबॉक्स, टूल रनर, ब्राउज़िंग लेयर, सेशन स्टोर, और कस्टम एजेंट फाइलें डेवलपर उत्पाद का हिस्सा हैं।

[ALLOY]: एक यूज़केस तुरंत अलग दिखता है: पुनरुत्पादनीय जांच। एक प्रबंधित एजेंट एक साफ लिनक्स वातावरण से शुरू कर सकता है, एक पब्लिक इश्यू ला सकता है, पुनरुत्पादन बना सकता है, और फॉलो-अप कॉल के लिए एक स्टेटफुल ट्रेल छोड़ सकता है। यह चैटबॉट से पूछने से अलग है कि क्या गलत हो सकता है। वातावरण में असली चेकआउट, लॉग, जेनरेटेड आर्टिफैक्ट, और उन्हें बनाने वाले कमांड हो सकते हैं।

[NOVA]: एक और यूज़केस पब्लिक डेटा के चारों ओर डिस्पोजेबल ऑटोमेशन है। एक प्रबंधित एजेंट बिना पर्सनल लैपटॉप को छुए ब्राउज़, कोड एक्जीक्यूट, और सेशन स्टेट रख सकता है। यह रिसर्च टास्क, जेनरेटेड उदाहरण, पब्लिक बेंचमार्क चेक, और छोटे डेटा ट्रांसफॉर्म के लिए उपयोगी है। यह हर प्राइवेट बिल्ड के लिए सही जगह नहीं है, लेकिन यह काम के लिए बिल्कुल सही आकार है जहां साफ आइसोलेशन एक फायदा है।

[ALLOY]: बिल्ड निहितार्थ यह है कि AGENTS.md और SKILL.md-स्टाइल फाइलें पोर्टेबल एजेंट पैकेजिंग बन रही हैं। एक प्रोजेक्ट अपने नियम, टूल प्रेफरेंस, और कन्वेंशन को एक रिमोट एजेंट वातावरण में ले जा सकता है। यह इंस्ट्रक्शन लेयर को वन-ऑफ प्रॉम्प्ट से ज्यादा टिकाऊ और इनविजिबल प्रोडक्ट प्रीसेट से ज्यादा इंस्पेक्टेबल बनाता है।

[ALLOY]: OpenAI की Codex खबर इस बारे में है कि कोडिंग-एजेंट का काम कहां रहता है और मनुष्य इसकी निगरानी कैसे करते हैं। ChatGPT मोबाइल ऐप में Codex Mac या रिमोट वातावरण पर चल रहे सक्रिय कार्य से जुड़ सकता है। मोबाइल व्यू लाइव प्रोजेक्ट स्टेट, टर्मिनल आउटपुट, स्क्रीनशॉट, टेस्ट रिजल्ट, और डिफ्स दिखा सकता है। यूज़र कमांड को अप्रूव कर सकता है और टास्क को रीडायरेक्ट कर सकता है।

[NOVA]: यह लंबे चलने वाले कोडिंग कार्य का स्वरूप बदल देता है। एजेंट वर्कस्पेस के पास चलता रह सकता है, जबकि अप्रूवल सर्फेस मनुष्य की तरफ जाता है। सेशन को रुकना नहीं पड़ता बस इसलिए कि व्यक्ति डेस्क छोड़ गया। महत्वपूर्ण बात मोबाइल नॉवेल्टी नहीं है। यृह एक्ज़ीक्यूशन लोकेशन को सुपरविज़न लोकेशन से अलग करना है।

[ALLOY]: सिक्योर रिले स्टेट वह आर्किटेक्चर है जिस पर नज़र रखनी चाहिए। कोड, क्रेडेंशियल्स, डिपेंडेंसीज़, और टूल्स वहीं रहते हैं जहां एजेंट असल में चल रहा है। मनुष्य को बाहर निर्णय लेने के लिए पर्याप्त लाइव स्टेट मिलता है। यह हर लोकल सीक्रेट को रिमोट चैट सर्फेस में खींचने से बेहतर पैटर्न है।

[NOVA]: रिमोट SSH का सामान्य उपलब्ध होना उसी दिशा में फिट बैठता है। Codex उस रिमोट होस्ट के खिलाफ काम कर सकता है जहां repo और डिपेंडेंसीज़ पहले से मौजूद हैं। वह एक development box, क्लाउड VM, वर्कस्टेशन, या मैनेज्ड एंटरप्राइज़ वातावरण हो सकता है। एक्ज़ीक్యूशन बाउंड्री एक deployment विकल्प बन जाती है, चैट विंडो कहां खुली है इसका साइड इफेक्ट नहीं।

[ALLOY]: प्रोग्रामैटिक एक्सेस टोकन एक और महत्वपूर्ण टुकड़ा है। automation में चलने वाले कोडिंग एजेंट्स को scoped identity चाहिए। ब्राउज़र सेशन या लॉन्ग-लिव्ड पर्सनल सीक्रेट non-interactive काम के लिए टेढ़ा आधार है। टोकन एजेंट वर्कफ्लो को एक workspace के अंदर काम करने का संकरा, रिवोकेबल तरीका देते हैं।

[NOVA]: हुक उस काम के आसपास पॉलिसी जोड़ते हैं। वे प्रॉम्प्ट में सीक्रेट के लिए स्कैन कर सकते हैं, validator चला सकते हैं, जोखिम भरे ऑपरेशंस को ब्लॉक कर सकते हैं, या काम आगे बढ़ने से पहले लोकल रूल्स लागू कर सकते हैं। यहीं पर Codex कम clever terminal helper जैसा और ज्यादा agent work system with checkpoints जैसा दिखने लगता है।

[ALLOY]: Dell partnership एंटरप्राइज़ वर्जन की तरफ इशारा करती है: hybrid और on-prem वातावरण में Codex। कुछ संगठन source code, logs, या data को casually पब्लिक क्लाउड कोडिंग लूप में नहीं ले जा सकते। Hybrid Codex इस बात के बारे में है कि एजेंट को approved compute, storage, और पॉलिसी बाउंड्रीज़ के करीब काम करने दें।

[NOVA]: ठोस Codex capability shift यह है: मोबाइल सुपरविज़न, रिमोट होस्ट, scoped टोकन, हुक, और hybrid वातावरण सब कोडिंग एजेंट्स की तरफ इशारा करते हैं जो डेटा के करीब चल सकते हैं जबकि किसी और जगह से सुपरवाइज़ किए जाते हैं। यही उपयोगी फ्रेमिंग है। "मेरे लैपटॉप पर एजेंट" बनाम "क्लाउड में एजेंट" नहीं, बल्कि "इस टास्क को कहां एक्ज़ीक्यूट होना चाहिए, और मनुष्य को कहां approve करना चाहिए?"

[ALLOY]: एक human-factors बदलाव भी है। diff, screenshots, terminal output, और test results review objects बनते जा रहे हैं जो travel करते हैं। अगर वे objects स्पष्ट हैं, रिमोट सुपरविज़न कंट्रोल जैसा लगता है। अगर वे अस्पष्ट हैं, मोबाइल सुपरविज़न black box में छोटी खिड़की बन जाता है।

[NOVA]: तो सिफारिश है कि फोन पर big refactors न झोंको। narrow decision points के लिए मोबाइल Codex सुपरविज़न इस्तेमाल करें: safe command approve करें, diff summary inspect करें, branch choice redirect करें, टास्क को रोकें जो गलत रास्ता ले गया। heavy evidence अभी भीgood enough ट्रस्ट करने के लिए होना चाहिए।

[ALLOY]: एंटरप्राइज़ सिफारिश भी Similar है। non-interactive identity जरूरत वाले automations के लिए टोकन और हुक इस्तेमाल करें। एक्ज़ीक्यूशन environment को उस repo, secrets, और पॉलिसी के करीब रखें जिनकी उसे जरूरत है। Codex एक ऐसी दुनिया की तरफ बढ़ रहा है जहां agent work रिमोट, supervised, और governed हो सकता है बिना यह Pretend किए कि location अब कोई मायने नहीं रखती। ...

[NOVA]: तुरंत उपयोग का मामला एक लंबे चलने वाले कोडिंग सेशन की दूरस्थ समीक्षा है। एजेंट पहले से ही एक ब्रांच बना चुका है, टेस्ट रन कर चुका है, और एक डिफ तैयार कर चुका है। मनुष्य डेस्क से दूर है, लेकिन फिर भी एक कमांड को मंजूर करने, एक जोखिम भरी दिशा को अस्वीकार करने, या सेशन को रोकने के लिए पर्याप्त साक्ष्य देख सकता है। यह आलसी इंतजार के समय को एक पर्यवेक्षित चेकपॉइंट में बदल देता है।

[ALLOY]: एंटरप्राइज़ उपयोग का मामला नियंत्रित निष्पादन है। एक Codex वातावरण कोडबेस, आंतरिक डिपेंडेंसी, और स्वीकृत कंप्यूट के पास रह सकता है। मोबाइल या दूरस्थ पर्यवेक्षण उस सीमा के बाहर हो सकती है, लेकिन फाइलें और क्रेडेंशियल रिव्यूअर के साथ नहीं जानी चाहिए। यह सुविधाजनक रिमोट कंट्रोल और लापरवाह रिमोट एक्सेस के बीच वास्तुशिल्प अंतर है।

[NOVA]: हुक्स इसे रिमोट स्क्रीन-पीकिंग से ज्यादा बनाते हैं। एक हुक प्रॉम्प्ट में सीक्रेट आने से ब्लॉक कर सकता है, पैच को तैयार मानने से पहले वैलिडेटर की मांग कर सकता है, या एजेंट के कार्य करने से पहले रेपो बाउंड्री लागू कर सकता है। प्रोग्रामैटिक टोकन उन जॉब्स को एक स्कोप्ड आइडेंटिटी देते हैं। एक साथ, वे Codex को एजेंट वर्क के लिए एक गवर्नेबल बिल्ड सिस्टम जैसा बनाते हैं।

[NOVA]: Anthropic का Stainless अधिग्रहण एक एजेंट-कनेक्टिविटी कहानी है। Stainless API स्पेक्स को SDKs, CLIs, और विभिन्न भाषाओं में MCP सर्वर्स में बदलता है। Anthropic कहता है कि Stainless ने Claude API के शुरुआती दिनों से ही आधिकारिक Anthropic SDKs जेनरेट किए हैं।

[ALLOY]: यह मायने रखता है क्योंकि एजेंट्स को हैंडल्स की जरूरत होती है। एक एजेंट जो केवल टेक्स्ट पढ़ सकता है वह सीमित है। एक एजेंट जो टाइप्ड SDK कॉल कर सकता है, CLI इनवोक कर सकता है, या MCP सर्वर का उपयोग कर सकता है वह रियल सिस्टम्स पर कार्य कर सकता है। उन जेनरेट सतहों की गुणवत्ता तय करती है कि कार्य सुरक्षित, प्रत्याशित, और समझने योग्य है या नहीं।

[NOVA]: API स्पेक्स एजेंट इन्फ्रास्ट्रक्चर बन रहे हैं। एक साफ स्पेक डॉक्यूमेंटेशन, क्लाइंट लाइब्रेरीज, कमांड-लाइन टूल्स, और MCP टूल सतहें बन सकता है। एक अस्पष्ट स्पेक एक अस्पष्ट एजेंट टूल बन जाता है। अगर मेथड नेम्स अस्पष्ट हैं, auth अंडरस्पेसिफाइड है, पेजिनेशन असंगत है, या एरर्स शोर हैं, तो एजेंट उस अस्पष्टता को इनहेरिट करता है।

[ALLOY]: Anthropic के अंदर Stainless उस टूल-जेनरेशन पाथ को Claude इकोसिस्टम में केंद्रीय बनाता है। भविष्य की कल्पना करना मुश्किल नहीं है जहां एक अच्छा API स्पेक बनाना भी एक अच्छी Claude-फेसिंग टूल सतह बनाता है: एप्लिकेशन कोड के लिए SDK, मनुष्यों और ऑटोमेशन के लिए CLI, एजेंट्स के लिए MCP सर्वर।

[NOVA]: शॉर्ट बिल्डर इम्प्लिकेशन सरल है: अगर एक इंटरनल API का उपयोग एजेंट्स द्वारा किया जाना चाहिए, तो स्पेक क्वालिटी अब ज्यादा मायने रखती है। टाइप्स, auth स्कोप्स, रीड-ओनली मेथड्स, म्यूटेटिंग मेथड्स, पेजिनेशन, रेट लिमिट्स, और एरर्स अब केवल डेवलपर-एक्सपीरियंस डीटेल्स नहीं हैं। वे एक एजेंट जो सिस्टम को साफ-सुथरे ढंग से कॉल कर सकता है और एक एजेंट जो इम्प्रोवाइज करता है, के बीच अंतर हैं।

[ALLOY]: Project Glasswing दूसरा आधा हिस्सा है। Anthropic कहता है कि Claude Mythos Preview का उपयोग पार्टनर्स के साथ एक हजार से अधिक ओपन-सोर्स प्रोजेक्ट्स में किया गया है और उच्च एवं क्रिटिकल-सेवरिटी वल्नरेबिलिटीज की बड़ी संख्या पाई गई है। हैडलाइन केवल "AI बग्स ढूंढता है" नहीं है। यह है कि फ्रंटियर मॉडल वल्नरेबिलिटी डिस्कवरी की दर इतनी बढ़ा सकते हैं कि वेरिफिकेशन और डिस्क्लोज़र बॉटलनेक बन जाते हैं।

[NOVA]: यह साधारण कोड रिव्यू से बहुत अलग दबाव है। एक मॉडल एक रियल एक्सप्लॉइट पाथ, एक आंशिक इश्यू, एक फॉल्स पॉजिटिव, या एक फाइंडिंग जिसे सावधानीपूर्वक डिस्क्लोज करने की जरूरत है, सतह पर ला सकता है। संभावित इश्यूज को ज्यादा खोजना तभी उपयोगी है जब मेंटेनर्स सत्यापित, प्राथमिकता, पैच, और जिम्मेदारी से संवाद कर सकें।

[ALLOY]: यह MCP और SDK जनरेशन से सीधे जुड़ता है। बेहतर जनरेटेड टूल्स एजेंट्स को सिस्टम्स में ज़्यादा पहुंच देते हैं। बेहतर सिक्योरिटी मॉडल एजेंट्स को उन सिस्टम्स की जांच करने की ज़्यादा क्षमता देते हैं। यही तेज़ी प्रोडक्टिविटी और रिस्क दोनों को बड़ा बनाती है।

[NOVA]: व्यावहारिक सिफारिश यह है कि एजेंट-असिस्टेड सिक्योरिटी स्कैनिंग को स्कोप्ड एक्टिविटी के रूप में ट्रीट करें, कैज़ुअल बैकग्राउंड हॉबी के रूप में नहीं। इसे वहां इस्तेमाल करें जहां रिपॉजिटरी, एविडेंस रिक्वायरमेंट्स, डिस्क्लोज़र पाथ, और रिपेयर ओनर स्पष्ट हों। आउटपुट एक फाइंडिंग होनी चाहिए जिसमें एविडेंस और पैच दिशा हो, न कि ड्रामेटिक क्लेम्स का ढेर।

[ALLOY]: Anthropic का सप्ताह, एक साथ मिलकर, कहता है कि एजेंट्स को बेहतर इंटरफेस और बेहतर ब्रेक चाहिए। Stainless इंटरफेस स्टोरी है: स्पेक्स को SDKs, CLIs, और MCP सर्वर में बदलना। Glasswing ब्रेक स्टोरी है: तेज़ डिस्कवरी के लिए वेरिफिकेशन, डिस्क्लोज़र, और रिपेयर क्षमता चाहिए।

[NOVA]: इस स्टैक का सबसे मज़बूत वर्शन एक एजेंट जिसकी अनलिमिटेड रीच हो नहीं है। यह एक एजेंट है जिसके पास अच्छी तरह डिस्क्राइब्ड टूल्स, नैरो पर्मिशन्स, विजिबल लॉग्स, और पर्याप्त सिक्योरिटी हेल्प हो जो असली फ्लॉज़ ढूंढ सके बिना मेन्टेनर्स को नॉइज़ से फ्लड किए बिना। ...

[ALLOY]: Stainless यूज़ केस सीधा है: सर्विस डिस्क्रिप्शन को ऐसे टूल्स में बदलें जिन्हें लोग और एजेंट्स दोनों असल में इस्तेमाल कर सकें। एक क्लीन API स्पेक एप्लिकेशन कोड के लिए टाइप्ड SDK, स्क्रिप्ट्स और इंसानों के लिए CLI, और एजेंट कॉल्स के लिए MCP सर्वर बना सकता है। यह तीन ड्रिफ्टिंग रैपरर्स की जगह इंटरफेस की एक सोर्स ऑफ ट्रुथ बनाता है।

[NOVA]: Glasswing यूज़ केस कैज़ुअल बग हंटिंग नहीं है। यह एविडेंस-बैक्ड टारगेटेड सिक्योरिटी डिस्कवरी है। एक मॉडल जो बड़े कोडबेस इंस्पेक्ट कर सकता है और हाई-सेवरिटी इश्यूज़ ढूंढ सकता है, वल्नरेबिलिटी रिसर्च की इकोनॉमिक्स बदल देता है। लेकिन उपयोगी आउटपुट अभी भी एक वेरिफाइड फाइंडिंग है, एक मिनिमल रिपेयर पाथ, और एक डिस्क्लोज़र डिसीज़न। उसके बिना, तेज़ डिस्कवरी बस अनसर्टेंटी की एक बड़ी कतार बनाती है।

[ALLOY]: स्ट्रैटेजिक पॉइंट यह है कि कनेक्टिविटी और सिक्योरिटी अब साथ में तेज़ होते हैं। टूल सरफेस बनाना जितना आसान होता है, एजेंट्स के एक्ट करना उतना ही आसान होता है। मॉडल वल्नरेबिलिटी डिस्कवरी में जितने मज़बूत होते हैं, उन टूल सरफेस को उतने ही नैरो पर्मिशन्स और ऑडिटेबिलिटी की ज़रूरत होती है। Stainless और Glasswing एक ही एजेंट-इन्फ्रास्ट्रक्चर बिल्ड के दो पहलू हैं।

[ALLOY]: पहला GitHub प्रोजेक्ट ग्रुप कोडिंग एजेंट्स को बेहतर आंखें देता है। नाम हैं Serena, Claude Context, Sourcebot, Understand-Anything, Chunkhound, और Code Review Graph।

[NOVA]: Serena यहां सबसे सीधा MCP-फ्लेवर्ड अपग्रेड है। यह कोडिंग एजेंट्स को सिमेंटिक रिट्रीवल, एडिटिंग, रिफैक्टरिंग, और डीबगिंग टूल्स देता है जो IDE कैपेबिलिटीज़ की तरह ज़्यादा बर्ताव करते हैं। अहम फीचर सिंबल-लेवल वर्क है: डेफिनिशन्स, रेफरेंसेज, रिलेशनशिप्स, और रिफैक्टर पाथ्स, सिर्फ टेक्स्ट मैचेस के बजाय।

[ALLOY]: यह मायने रखता है क्योंकि grep कोड अंडरस्टैंडिंग नहीं है। यह एक फास्ट फ्लैशलाइट है। एक कोडिंग एजेंट को जानना ज़रूरी है कि एक सिंबल कहां डिफाइंड है, कहां उसका इस्तेमाल होता है, क्या इस पर डिपेंड करता है, और कौन से टेस्ट उस पाथ को कवर करते हैं। Serena उन IDE-जैसी मूव्स को एक टूल सरफेस के पीछे रखने की कोशिश करता है जिसका इस्तेमाल एजेंट कर सकता है।

[NOVA]: Claude Context Claude Code और दूसरे agents के लिए एक semantic code-search MCP है। इसका काम बड़े repos को meaning के हिसाब से searchable बनाना है बिना огромные directories को prompt में डाले। यह तब useful है जब code का नाम human description से मेल नहीं खाता, या जब relevant logic फ़ाइलों में बिखरा हुआ है।

[ALLOY]: Sourcebot एक self-hosted code search और understanding platform है। यह repo search, navigation, file exploration, और citations के साथ Ask Sourcebot Q&A देता है। Self-hosted होना important है क्योंकि code intelligence अक्सर private repositories को छूता है। एक shared, cited search surface humans और agents को vibes की जगह same evidence से argue करने में मदद कर सकता है।

[NOVA]: Understand-Anything codebases को interactive knowledge graphs में बदल देता है search और Q&A के साथ, और यह explicitly Claude Code, Codex, Cursor, Copilot, Gemini CLI, और related tools के लिए खुद को position करता है। Graph magic नहीं है, लेकिन यह architecture shape दिखा सकता है before an agent एक system edit करना शुरू करे जिसे वो barely समझता है।

[ALLOY]: Chunkhound और Code Review Graph local-first और persistent-map angle को आगे बढ़ाते हैं। यह सही category है उन teams के लिए जो semantic या graph context चाहते हैं बिना whole repo कहीं और भेजे। एक persistent code map context waste को कम कर सकता है agent को few relationships खिलाकर जो matter करती हैं giant transcript dump की जगह।

[NOVA]: इस group के लिए recommendation यह है कि chosen करें based on what the agent missing है। अगर उसे symbols और references चाहिए, तो Serena देखें। अगर Claude Code के अंदर semantic search चाहिए, तो Claude Context देखें। अगर humans और agents को shared self-hosted code browser चाहिए, तो Sourcebot देखें। अगर architecture shape problem है, तो Understand-Anything interesting है। अगर local indexing और persistent code maps सबसे ज्यादा matter करती हैं, तो Chunkhound और Code Review Graph shortlist पर होने चाहिए।

[ALLOY]: वजह कि यह news lane है, सिर्फ tools list नहीं, यह है कि code context stack में अपनी own layer बनता जा रहा है। Bigger context windows help करती हैं, लेकिन वो retrieval quality की जगह नहीं ले सकतीं। एक model जो better map देखता है वो smaller, more accurate edit कर सकता है। यह often उससे ज्यादा valuable है कि उसे और thousand irrelevant files सौंप दिए जाएं।

[NOVA]: यहीं पर Hermes, OpenClaw, Codex, और Claude Code सबको common tool surfaces से benefit मिलता है। अगर code intelligence MCP, local indexes, या self-hosted search के through available है, तो यह कई agents के नीचे बैठ सकता है। Agent बदलता है; repo map useful रहता है।

[ALLOY]: Short recommendation यह है: एक code-intelligence layer सिर्फ वहीं add करें जहां repo size उसे justify करती है। एक one-file script को semantic graph की जरूरत नहीं। एक mature codebase जिसमें scattered behavior है, muht天天 probably चाहिए। ...

[NOVA]: Serena का best use case symbol-aware editing है। एक refactor जो definitions, references, और tests को cross करता है वो एक MCP tool से benefit करता है जो code relationships को समझता है। Claude Context का best use case semantic retrieval है जब prompt behavior describe करती है लेकिन code अलग names use करता है। Sourcebot का best use case एक self-hosted search surface है जहां humans और agents citations share कर सकते हैं।

[ALLOY]: Understand-Anything तब stronger है जब architecture shape matter करती है: unfamiliar services, hidden dependencies, या एक repo जहां call graph filenames से ज्यादा explain करती है। Chunkhound और Code Review Graph local-first use case में fit करती हैं, जहां persistent maps valuable हैं लेकिन code machine या trusted network से casually नहीं निकल सकती।

[NOVA]: बिल्ड ट्रेंड स्पष्ट है: कोड कॉन्टेक्स्ट एक पुन: प्रयोज्य सबस्ट्रेट बन रहा है। एजेंट हैनेस आज Claude Code हो सकता है, कल Codex, अगले हफ्ते Hermes, और इसके चारों ओर OpenClaw। एक अच्छा repo मैप सभी उन सतहों की सेवा कर सकता है अगर यह MCP, एक लोकल इंडेक्स, या सेल्फ-होस्टेड सर्च लेयर के माध्यम से एक्सपोज़ किया जाता है।

[ALLOY]: इसीलिए यह प्रोजेक्ट लेन मायने रखती है। यह सिर्फ एक मॉडल को स्मार्टर बनाने के बारे में नहीं है। यह हर कोडिंग एजेंट को एक बेहतर स्टार्टिंग पॉइंट देना है: कम अप्रासंगिक फाइलें, अधिक सटीक रेफरेंस, स्पष्ट आर्किटेक्चर, और सवाल से सबूत तक छोटा रास्ता।

[NOVA]: दूसरा प्रोजेक्ट ग्रुप स्टैक के चलने का तरीका बदलता है। Context7, Claude Code Router, mcp-use, goose, gstack, deepsec, context-mode, और ai-setup सभी मॉडल, रेपो, टूल्स, और यूज़र के बीच बैठते हैं।

[ALLOY]: Context7 वर्तमान डॉक्यूमेंटेशन संभालता है। कोडिंग एजेंट अक्सर फेल होते हैं क्योंकि उनकी लाइब्रेरी मेमोरी पुरानी हो जाती है। Context7 LLMs और कोडिंग एजेंट्स को CLI, स्किल्स, या MCP के जरिए अपडेटेड लाइब्रेरी डॉक्स देता है। यह तेज़ी से बदलने वाले JavaScript, Python, AI SDK, और फ्रेमवर्क टास्क्स के लिए खासतौर पर उपयोगी है जहाँ पुराने उदाहरण सही लगते हैं लेकिन टूट जाते हैं।

[NOVA]: Claude Code Router प्रोवाइडर और मॉडल रूटिंग के बारे में है। यह OpenRouter, DeepSeek, Ollama, Gemini, और अन्य बैकएंड्स में Claude Code रिक्वेस्ट्स को रूट कर सकता है, ट्रांसफॉर्मर्स और रूट-स्पेसिफिक मॉडल चॉइस के साथ। वैल्यू वर्क के हिसाब से बैकएंड मैच करना है: सस्ते सारांश, लोकल एक्सपेरिमेंट्स, लॉन्ग-कॉन्टेक्स्ट रीड्स, या हाई-रीज़निंग रिव्यू।

[ALLOY]: जोखिम जवाबदेही का है। एक रूटर तभी मददगार है जब रूट इतना विजिबल हो कि यूज़र को पता हो कि किस प्रोवाइडर और मॉडल ने टास्क संभाला। हिडन रूटिंग पैसे बचा सकती है और एक साथ कन्फ्यूज़न भी पैदा कर सकती है।

[NOVA]: mcp-use TypeScript और Python में MCP ऐप्स और सर्वर्स बनाने के लिए एक फ्रेमवर्क है, इंस्पेक्शन और डिप्लॉयमेंट पाथ्स के साथ। यह महत्वपूर्ण है क्योंकि MCP नोवेल्टी से इंटीग्रेशन लेयर की तरफ बढ़ रहा है। टीम्स को हर सर्वर को हाथ से बनाने के बिना छोटे टूल्स बनाने, कॉल्स इंस्पेक्ट करने, और एजेंट्स के लिए पैकेज करने का तेज़ तरीका चाहिए।

[ALLOY]: goose एक लोकल AI एजेंट है जिसमें डेस्कटॉप, CLI, API, मल्टी-प्रोवाइडर सपोर्ट, ACP पाथ्स, और MCP एक्सटेंशन्स हैं। यह अब Agentic AI Foundation के तहत है, और यह एक लोकल एजेंट फॉलबैक या तुलना पॉइंट के रूप में देखने योग्य है। दिलचस्प हिस्सा यह नहीं है कि क्या यह सब कुछ रिप्लेस करता है। यह है कि क्या इसका प्रोवाइडर और एक्सटेंशन मॉडल कुछ लोकल टास्क्स को एक भारी स्टैक के बाहर चलाना आसान बनाता है।

[NOVA]: gstack रिव्यू, QA, रिलीज़, सिक्योरिटी, प्लानिंग, और प्रोडक्ट वर्क के लिए Claude Code रोल्स और वर्कफ्लोज़ को पैकेज करता है। रोल पैक्स थिएटर बन सकते हैं अगर वे सिर्फ सामान्य प्रॉम्प्ट्स को रीनेम करते हैं, लेकिन वे तब उपयोगी होते हैं जब वे रिपीटेबल रिव्यू बिहेवियर, अपेक्षित सबूत, और निरंतर आउटपुट शेप्स को एन्कोड करते हैं।

[ALLOY]: deepsec इस लेन में सिक्योरिटी स्कैनर है। यह बड़े कोडबेस में वल्नरेबिलिटी स्कैनिंग के लिए कोडिंग एजेंट्स का उपयोग करता है, रिज्यूमेबल स्कैन्स, मैचर्स, प्रोसेसिंग, रिवैलिडेशन, और एक्सपोर्ट के साथ। यह इसे Glasswing के साथ एक ही यूनिवर्स में रखता है, लेकिन एक GitHub-होस्टेड टूल के रूप में जिसे बिल्डर्स स्कोप्ड सेटिंग्स में इंस्पेक्ट और रन कर सकते हैं।

[NOVA]: context-mode और ai-setup का लक्ष्य दो आम समस्याओं पर है: आउटपुट शोर और सेटअप ड्रिफ्ट। एक बार स्टैक में Claude Code, Codex, OpenCode, Gemini CLI, Hermes, OpenClaw, local models, MCP servers, और routers शामिल हो जाते हैं, तो कॉन्फ़िगरेशन छिपी हुई विफलता मोड बन सकती है। जो टूल्स कॉन्टेक्स्ट को टाइट और सेटअप को सुसंगत रखते हैं, वे दूसरे मॉडल पिकर से ज्यादा उपयोगी हो सकते हैं।

[ALLOY]: इस ग्रुप के लिए सिफारिश भी जॉब-आधारित है। जब current docs गायब हों तो Context7 का उपयोग करें। जब provider choice मायने रखती हो तो Claude Code Router का उपयोग करें। जब private capability को MCP टूल बनाना हो तो mcp-use का उपयोग करें। जब extensions वाला local agent सही तुलना हो तो goose का उपयोग करें। जब repeatable review roles मायने रखती हों तो gstack का उपयोग करें। deepsec का उपयोग तभी करें जब security findings को verify और handle किया जा सके।

[NOVA]: बड़ा ट्रेंड यह है कि agent stack बीच में भर रहा है। हमारे पास पहले से models और chat surfaces हैं। नया activity routers, docs retrieval, MCP builders, local agent shells, role packs, code maps, और scanners में है। यहीं पर agent work ज्यादा controllable बनती है।

[ALLOY]: इससे discipline और भी जरूरी हो जाती है। हर अतिरिक्त टूल authority, configuration, या evidence के गायब होने की एक और जगह जोड़ता है। एक अच्छा project अपनी जगह इस तरह कमाता है कि task स्पष्ट हो: बेहतर docs, बेहतर code context, स्पष्ट provider routing, संकुचित tool access, या ज्यादा verifiable security findings। ...

[NOVA]: Context7 का core use case fast-moving libraries हैं। जब कोई framework, AI SDK, या database client तेज़ी से बदलता है, stale model memory ऐसा code देती है जो सही दिखता है लेकिन runtime पर fail होता है। Agent loop में current docs model बदले बिना build को improve करने का एक आसान तरीका है।

[ALLOY]: Claude Code Router का use case workload separation है। एक सस्ता model logs summarize कर सकता है। एक local model private background reading handle कर सकता है। एक मजबूत model risky patch review कर सकता है। Router तब उपयोगी है जब ये चुनाव स्पष्ट हों; यह खतरनाक है जब routing invisible हो जाती है।

[NOVA]: mcp-use इस ग्रुप में build tool है। यह एक छोटी capability को खासकर TypeScript और Python में MCP server या app बनाने की लागत कम करती है। पहला अच्छा use case आमतौर पर read-only होता है: status lookup, documentation search, inventory query, या कोई संकरा internal report। एक बार shape समझ में आ जाए, तो write actions को अलग privilege के रूप में treat किया जा सकता है।

[ALLOY]: goose local-agent use case है। यह builders को provider और MCP extension support के साथ एक और desktop, CLI, और API surface देता है। gstack repeatable-role use case है: review, QA, release, planning, और security prompts जो बर्ताव में काफी consistent होते हैं ताकि judged किया जा सके। deepsec security use case है, resumable scans और exported findings के साथ। context-mode और ai-setup consistency use case हैं, जो output और configuration को stack बढ़ने पर sprawling होने से रोकते हैं।

[NOVA]: इन सभी में useful pattern खुद के लिए procedure नहीं है। यह वह tool चुनना है जो outcome बदलती है: कम stale APIs, स्पष्ट provider choice, संकरा MCP surface, एक local agent जो heavy stack के बिना run कर सके, एक review role जो concrete bugs find करती है, या एक scanner जो noise के बजाय evidence produce करती है।

[ALLOY]: इस project lane में एक और stack-level point है। ये tools सिर्फ model quality पर ही नहीं compete कर रहे। वे context quality, routing clarity, interface shape, और evidence पर compete कर रहे हैं। Context7 documentation input को improve करती है। Serena और Sourcebot code input को improve करते हैं। Claude Code Router model path बदलती है। mcp-use tool interface बदलती है। goose local execution shell बदलती है। deepsec security lens बदलती है। ये अलग-अलग layers हैं, और इन्हें मिलाना stack को reason करना मुश्किल बनाता है।

[NOVA]: इस पूरे लेन के लिए सबसे अच्छा यूज़-केस एक बिल्डर है जिसके पास पहले से एक काबिल मॉडल है लेकिन फिर भी औसत नतीजे मिलते हैं क्योंकि आसपास का सिस्टम कमज़ोर है। एजेंट पुराने डॉक्स पढ़ता है। यह सही फाइल मिस करता है। यह महंगे मॉडल का इस्तेमाल एक सस्ते सारांश के लिए करता है। यह अंदरूनी सिस्टम को साफ़ तौर पर कॉल नहीं कर सकता। यह बिना किसी सबूत के सुरक्षा का दावा करता है। इस लेन के प्रोजेक्ट्स उन फेलियर मोड्स पर सीधे हमला करते हैं।

[ALLOY]: इसीलिए यह स्टार्स की गिनती वाले राउंडअप से ज़्यादा दिलचस्प है। एक रेपो तब ध्यान अर्जित करता है जब यह एजेंट वर्क के आसपास की किसी कठिन सतह को बदलता है: मॉडल क्या जानता है, कौन सा मॉडल जवाब देता है, कौन से टूल्स कॉल करने योग्य हैं, एक्सीक्यूशन कहां होती है, कोड कैसे मैप किया जाता है, या फाइंडिंग्स कैसे वेरिफाई होती हैं। यह कंक्रीट स्टैक अपग्रेड है, README के लिए कोई नया बैज नहीं।

[NOVA]: सबसे मज़बूत बिल्ड्स इन लेयर्स को सावधानी से कंबाइन करेंगे। फास्ट लाइब्रेरी के लिए करंट डॉक्स। बड़े रेपो के लिए सेमांटिक कोड मैप्स। प्रोवाइडर च्वाइस के लिए विजिबल राउटिंग। प्राइवेट कैपेबिलिटीज़ के लिए छोटे MCP सर्वर्स। सेंसिटिव एक्सीक्यूशन के लिए लोकल एजेंट्स। सिक्योरिटी स्कैनर्स जहां एविडेंस को हैंडल किया जा सके। वैल्यू हर टूल इंस्टॉल करना नहीं है। वैल्यू यह जानना है कि कौन सी लेयर कमज़ोर है और सिर्फ वही टुकड़ा जोड़ना जो इसे मज़बूत करती है।

[NOVA]: EP057 का स्टैक अपडेट सीधा है। OpenClaw v2026.5.22 गेटवे, प्लगइन लेयर, मीटिंग-नोट्स सोर्सेस, प्रोवाइडर फॉलबैक बिहेवियर, सेशन नेविगेशन, और Discord कंट्रोल्स को ज़्यादा सॉलिड बनाता है। Claude Code यूज़ेज विजिबिलिटी, डिफ रिव्यू, टास्क-लिस्ट रेंडरिंग, मैनेज्ड क्लाउड MCP कनेक्टर पॉलिसी, और कई शेल और सैंडबॉक्स सेफ्टी एज़ेज़ को बेहतर बनाता है। निम्नलिखित पैच इंटरनल-ओनली है।

[ALLOY]: Google के Gemini न्यूज़ कहते हैं कि मैनेज्ड एजेंट एनवायरनमेंट्स अब एक प्रोडक्ट सतह हैं: रिमोट Linux एक्सीक्यूशन, टूल्स, ब्राउज़िंग, फाइल्स, सेशन कंटिन्यूएशन, और कस्टम एजेंट इंस्ट्रक्शन फाइल्स। OpenAI के Codex न्यूज़ कहते हैं कि कोडिंग-एजेंट वर्क रिमोट, मोबाइल-सुपरवाइज़्ड, टोकन-स्कॉप्ड, हुक-गवर्न्ड, और एंटरप्राइज़-डिप्लॉयबल हो रहा है।

[NOVA]: Anthropic के Stainless अधिग्रहण के बारे में कहते हैं कि SDKs, CLIs, और MCP सर्वर्स कोर एजेंट इन्फ्रास्ट्रक्चर बन रहे हैं। प्रोजेक्ट Glasswing कहता है कि फ्रंटियर मॉडल इतनी जल्दी वल्नरेबिलिटीज़ ढूंढ सकते हैं कि वेरिफिकेशन और डिस्क्लोज़र बॉटलनेक बन जाते हैं।

[ALLOY]: GitHub प्रोजेक्ट रडार कहता है कि यूज़फुल स्टैक अपग्रेड्स सब मॉडल नहीं हैं। Serena, Claude Context, Sourcebot, Understand-Anything, Chunkhound, और Code Review Graph वो चीज़ें बेहतर करते हैं जो एजेंट्स कोड के बारे में समझ सकते हैं। Context7, Claude Code Router, mcp-use, goose, gstack, deepsec, context-mode, और ai-setup डॉक्स, राउटिंग, MCP टूलिंग, लोकल एक्सीक्यूशन, रिपीटेबल रोल्स, सिक्योरिटी स्कैनिंग, और सेटअप कंसिस्टेंसी को बेहतर करते हैं।

[NOVA]: छोटी सी रिकमेंडेशन है कि कोर टूल्स को अपडेट करें, फिर सिर्फ वो प्रोजेक्ट्स जोड़ें जो कोई दिखाई देने वाली समस्या सुलझाते हैं। बड़े रेपो के लिए बेहतर कोड मैप्स। फास्ट-मूविंग लाइब्रेरी के लिए करंट डॉक्स। जहां प्रोवाइडर च्वाइस मायने रखता है वहां मॉडल राउटिंग। स्कोप्ड टूल्स के लिए MCP बिल्डर्स। जहां असली वेरिफिकेशन पाथ है वहां सिक्योरिटी स्कैनर्स।

[ALLOY]: यही एजेंट न्यूज़ का यूज़फुल वर्जन है: नामों का ढेर नहीं, और न ही खुद के लिए प्रोसेस। कंक्रीट रिलीज़ेज, कंक्रीट कैपेबिलिटीज़, और स्टैक के जा रहा होने की दिशा की ज़्यादा स्पष्ट तस्वीर।

[NOVA]: पूरे नोट्स और सोर्स लिंक्स एपिसोड नोट्स में हैं Toby On Fitness Tech dot com पर।

[ALLOY]: AgentStack Daily सुनने के लिए धन्यवाद। हम जल्द ही वापस आएंगे।