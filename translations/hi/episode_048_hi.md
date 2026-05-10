[NOVA]: मैं NOVA हूँ।

[ALLOY]: और मैं ALLOY हूँ, और ये है OpenClaw Daily। आज हम चार builder stories देख रहे हैं जहाँ agent runtimes ज़्यादा controllable, ज़्यादा inspectable, और boundaries गलत होने पर ज़्यादा dangerous बन जाती हैं।

[NOVA]: OpenAI Codex 0.130.0 coding-agent operators को एक cleaner remote-control surface देती है। Microsoft's Semantic Kernel research दिखाती है कि prompt injection कैसे code execution बन सकता है जब tool arguments eval-based framework code में cross करते हैं। GitHub Copilot SDK plan approval और rate-limit recovery के लिए callbacks जोड़ता है। और Microsoft Agent Framework 1.5 orchestration, browser policy, observability, और wire semantics को आगे बढ़ाता है। ...

[ALLOY]: पिछली story के नीचे छिपा practical सवाल महत्वपूर्ण है: क्या Microsoft Agent Framework को actually OpenClaw के अंदर use किया जा सकता है? Short answer: हाँ, लेकिन OpenClaw के own runtime की drop-in replacement के रूप में नहीं। यह OpenClaw के साथ side-by-side run कर सकती है - एक external agent service, एक command-backed skill, एक hosted workflow, या एक tool protocol के through exposed bridge के तौर पर। OpenClaw local-first gateway, channel router, session manager, और tool authority बनी रहेगी। Microsoft Agent Framework एक specialized agent runtime होगी जिसे OpenClaw call करती है, supervise करती है, और policy के साथ wrap करती है।

[NOVA]: ये distinction मायने रखती है। एक framework एक system के अंदर useful हो सकती है without becoming the system। Safe integration model ये नहीं है कि "दूसरे framework को host लेने दो।" Safe model ये है कि "framework को untrusted या semi-trusted tool boundary की तरह treat करो - explicit inputs, outputs, permissions, telemetry, और failure handling के साथ।"

[NOVA]: Story one है OpenAI Codex 0.130.0। Headline है codex remote-control - एक simpler entrypoint एक headless app-server start करने के लिए जिसे remotely control किया जा सकता है।

[ALLOY]: एक headless app-server एक बहुत अलग operational object है एक-shot command-line agent से। एक terminal run start, work, और exit करती है। एक app-server sessions, threads, configuration snapshots, environment selection, tool execution, review events, और time over client connections own करती है। इसका मतलब runtime अब सिर्फ एक prompt answer करना नहीं है। यह एक service surface maintain कर रही है।

[NOVA]: Exactly। app-server को एक coding session alive रखनी होती है जब clients reconnect करते हैं, history inspect करते हैं, specific turns open करते हैं, diffs review करते हैं, और एक अलग interface से work continue करते हैं। एक remote-control command उस control plane को explicit बनाती है। यह local coding assistant से service endpoint तक का path है - जिसे एक IDE, dashboard, browser client, या remote development machine drive कर सकती है।

[ALLOY]: यहाँ big mechanism है control और work का separation। Server durable session own करती है। Clients आ और जा सकते हैं। Work original terminal tab की life से bound नहीं है। यह useful है, लेकिन state management, access control, और auditability के लिए bar बढ़ाता है।

[NOVA]: Codex 0.130.0 large-thread paging भी जोड़ता है जहाँ clients unloaded, summary, या full turn item views request कर सकते हैं। यह interface polish लगता है until आप think करते हैं कि एक agent thread में क्या हो सकता है। इसमें user turns, model turns, tool calls, approvals, diffs, file references, images, compaction summaries, plugin metadata, और review state शामिल हो सकते हैं। उस entire object को हर remote client में load करना wasteful और brittle है।

[ALLOY]: पेज्ड थ्रेड व्यूज़ ट्रांसक्रिप्ट को ऑपरेशनल टाइमलाइन की तरह व्यवहार करने देते हैं। एक अनलोडेड आइटम पेलोड ट्रांसफर किए बिना आइडेंटिटी और ऑर्डरिंग बनाए रख सकता है। एक सारांश आइटम नेविगेट करने के लिए पर्याप्त संदर्भ दे सकता है। एक पूर्ण आइटम तभी मैटेरियलाइज़ हो सकता है जब क्लाइंट वास्तव में डिटेल खोलता है। यही आकार आप trace viewers, log explorers, और issue timelines में देखते हैं।

[NOVA]: यह लेटेंसी की भी रक्षा करता है। एक रिमोट क्लाइंट इसलिए फ्रीज नहीं होना चाहिए क्योंकि एक एजेंट थ्रेड विशाल वर्क रिकॉर्ड में बढ़ गया। लंबे चलने वाले कोडिंग सेशन के लिए, pagination एज पर अनुकूलन नहीं है। यह सेशन कॉन्ट्रैक्ट का हिस्सा बन जाता है।

[ALLOY]: प्लगइन डिटेल अब बंडल्ड hooks दिखाते हैं, और प्लगइन शेयरिंग लिंक मेटाडेटा प्लस डिस्कवरेबिलिटी कंट्रोल एक्सपोज़ करता है। यह एक ऑडिटेबिलिटी सुधार है। Hooks प्लगइन के रनटाइम व्यवहार का हिस्सा हैं। अगर कोई प्लगइन स्टार्टअप देख सकता है, टूल कॉल्स इंटरसेप्ट कर सकता है, कमांड्स दे सकता है, या रिव्यू में हिस्सा ले सकता है, तो ऑपरेटर्स को इसे इंस्टॉल या शेयर करने से पहले देखना होगा।

[NOVA]: पैकेज के अंदर hooks छिपाना प्लगइन रिव्यू को अनुमान-लगाने का काम बना देता है। Hook मेटाडेटा दिखाना एक्जीक्यूशन सर्फेस को विजिबल बनाता है। एजेंट सिस्टम में, इंस्पेक्टेबिलिटी के बिना डिस्कवरेबिलिटी जोखिम भरी है। कुछ ऐसा इंस्टॉल करना आसान है जो हानिरहित सुविधा जैसा लगता है और बाद में पता चलता है कि यह टूल व्यवहार, स्टार्टअप स्टेट, या रिव्यू फ्लो को मॉडिफाई करता है।

[ALLOY]: रिलीज़ लाइव ऐप-सर्वर कॉन्फिगरेशन व्यवहार को भी ठीक करती है। लाइव ऐप-सर्वर थ्रेड्स अब रीस्टार्ट की जरूरत के बिना कॉन्फिगरेशन बदलाव उठाते हैं। यह एक व्यावहारिक रिलायबिलिटी फिक्स है क्योंकि एजेंट रनटाइम में कॉन्फिगरेशन में मॉडल चॉइस, अप्रूवल पॉलिसी, प्रोवाइडर सेटिंग्स, टूल उपलब्धता, प्लगइन स्टेट, एनवायरनमेंट सिलेक्शन, और टेलीमेट्री ऑप्शन्स शामिल हो सकते हैं।

[NOVA]: अगर कोई लंबे समय से चल रहा थ्रेड पुराने कॉन्फिग का उपयोग करता रहे, तो ऑपरेटर को लग सकता है कि पॉलिसी बदल गई है जबकि सक्रिय एजेंट पुराने नियमों के तहत जारी रहता है। लाइव थ्रेड्स को नवीनतम कॉन्फिगरेशन स्नैपशॉट से रिफ्रेश करना पॉलिसी बदलावों को वहां प्रभावी बनाता है जहां काम हो रहा है। यह ऑपरेशनल प्रलोभन को भी कम करता है कि सर्विस को रीस्टार्ट किया जाए बस इसलिए कि कोई अप्रूवल या प्रोवाइडर सेटिंग लागू हो।

[ALLOY]: टर्न डिफ्स को सबसे महत्वपूर्ण बिल्डर फिक्सेस में से एक मिलता है। Codex अब apply_patch ऑपरेशन्स में डिफ्स को सटीक रखता है, पार्शियल फेलर्स सहित जो फाइल्स को अभी भी म्यूटेट करते हैं। यह एक वास्तविक फेल्योर मोड है। एक पैच आधे रास्ते में फेल हो सकता है और फिर भी फाइल का एक हिस्सा बदल सकता है। अगर रनटाइम बाद में गलत डिफ रिपोर्ट करता है, तो रिव्यू व्यू, रोलबैक लॉजिक, और ऑडिट ट्रेल पर भरोसा नहीं किया जा सकता।

[NOVA]: ऑपरेशन-बैक्ड डिफ ट्रैकिंग सही दिशा है। रनटाइम को रिकॉर्ड करना चाहिए कि वास्तव में क्या बदला, न कि केवल यह कि आदर्श पैच क्या होने वाला था। कोडिंग एजेंट्स को ऑपरेशन के बाद की सटीक स्टेट चाहिए, खासकर जब टूल्स को फाइल्स एडिट करने की अनुमति हो। भ्रामक डिफ बिना डिफ के बुरा है क्योंकि यह झूठा आत्मविश्वास पैदा करता है।

[ALLOY]: ThreadStore फिक्सेस सारांश, रीनेम, रिज्यूम, और फोर्क पाथ्स को बेहतर बनाते हैं, लोकल रोलआउट पाथ्स के बिना थ्रेड्स सहित। यह स्टोरेज लेयर को लाइफसाइकल ऑपरेशन्स के लिए स्रोत ऑफ ट्रुथ अधिक बनाता है। रिज्यूम और फोर्क मायने रखते हैं क्योंकि एक यूजर जांच ब्रांच कर सकता है, एक फेल्ड रन जारी रख सकता है, या किसी रिमोट क्लाइंट से थ्रेड खोल सकता है जिसके पास मूल लोकल फाइलसिस्टम पाथ नहीं है।

[NOVA]: अगर थ्रेड आइडेंटिटी लोकल मशीन स्टेट पर बहुत निर्भर है, तो हेडलेस और रिमोट वर्कफ्लो टूट जाते हैं। एक रिमोट ऐप-सर्वर को "यह थ्रेड क्या है, इसमें कौन सी स्टेट है, और यह कैसे जारी रख सकता है?" का जवाब बिना यह माने के देने में सक्षम होना चाहिए कि मूल टर्मिनल कॉन्टेक्स्ट अभी भी मौजूद है।

[ALLOY]: रिमोट कम्पैक्शन को स्ट्रीम-कॉन्ट्रैक्ट फिक्सेस भी मिलते हैं। Codex अब v2 स्ट्रीम्स के लिए response.processed emit करता है और API-key compact अनुरोधों पर service_tier नहीं भेजता। कम्पैक्शन यह तय करता है कि सेशन कितनी देर तक उपयोगी रहे, लेकिन रिमोट कम्पैक्शन को normal turns के समान इवेंट भाषा बोलनी होती है। एक गुम processed इवेंट क्लाइंट को terminal state का इंतज़ार करा सकता है। एक unsupported request field सिर्फ कम्पैक्शन पाथ को तोड़ सकती है, जिससे डायग्नोसिस मुश्किल हो जाता है।

[NOVA]: मल्टी-एनवायरनमेंट सपोर्ट view_image में दिखता है, जो अब चयनित एनवायरनमेंट के माध्यम से फ़ाइलों को रिज़ॉल्व कर सकता है। यह इसलिए मायने रखता है क्योंकि कोडिंग एजेंट अक्सर होस्ट, कंटेनर, सैंडबॉक्स, रिमोट वर्कस्पेस या माउंटेड प्रोजेक्ट में काम करते हैं। एक इमेज पाथ तब तक मायने नहीं रखता जब तक रनटाइम को यह पता न हो कि कौन सा एनवायरनमेंट उसका मालिक है। चयनित एनवायरनमेंट के ज़रिए रिज़ॉल्व करने से क्लाइंट गलत फाइलसिस्टम देखने या उस आर्टिफैक्ट को दिखाने में नाकाम होने से बच जाता है जो सक्रिय सैंडबॉक्स के अंदर मौजूद है।

[ALLOY]: Bedrock authentication सपोर्ट अब aws login प्रोफाइल से AWS console-login क्रेडेंशियल स्वीकार करता है। यह operator सुविधा है जिसका deployment पर असर पड़ता है। कई टीमें पहले से प्रोफाइल-आधारित फ्लो के ज़रिए AWS एक्सेस मैनेज करती हैं। Codex को उन प्रोफाइल्स का उपयोग करने देना डुप्लिकेट क्रेडेंशियल पाथ कम करता है और मॉडल-प्रोवाइडर authentication को मौजूदा क्लाउड एक्सेस कंट्रोल के साथ संरेखित करता है।

[NOVA]: टेलीमेट्री में बदलाव प्रोडक्शन डिबगिंग के लिए उपयोगी हैं। Codex कॉन्फ़िगरेबल OpenTelemetry trace metadata और समृद्ध review और feedback analytics जोड़ता है। Review events कोडिंग-एजेंट सुरक्षा के केंद्र में हैं। अगर कोई कमांड approve, deny, retry या escalate किया गया, तो ऑपरेटर्स को यह समझने के लिए पर्याप्त trace context चाहिए।

[ALLOY]: अच्छा टेलीमेट्री सेशन, turn, tool call, approval decision, मॉडल रिक्वेस्ट और यूज़र-दृश्य परिणाम को बिना secrets लीक किए जोड़ता है। यह वह रेखा है जिस पर चलना है। बहुत कम टेलीमेट्री से इंसिडेंट्स को पुनर्निर्मित करना असंभव हो जाता है। बहुत अधिक टेलीमेट्री से prompts, फ़ाइलें, credentials या प्राइवेट कोड उजागर हो सकते हैं।

[NOVA]: व्यावहारिक सिफारिश यह है कि Codex app-server deployments को सर्विस deployments की तरह ट्रीट करें। संस्करण को pin करें। remote-control को सोच-समझकर शुरू करें। दस्तावेज़ करें कि कौन से क्लाइंट कनेक्ट कर सकते हैं। शेयर करने से पहले plugin hooks की audit करें। config refresh behavior टेस्ट करें। partial patch failures टेस्ट करें। और verify करें कि compaction, thread resume और image viewing उन एनवायरनमेंट्स में काम करते हैं जिनका आप वास्तव में उपयोग करते हैं।

[ALLOY]: एक और operation detail है जिसे बताना ज़रूरी है। जब एक coding agent app-server बन जाता है, तो product UX और runtime state के बीच की सीमा पतली हो जाती है। अब एक यूज़र इंटरफ़ेस compacted summary, पूरा turn, plugin detail page, review event या image artifact मांग सकता है। अगर वे endpoints versioned और tested नहीं हैं, तो UI आकस्मिक रूप से उन internal shapes पर निर्भर हो सकता है जो किसी release में बदलते हैं। Builders को उन app-server responses को API contracts की तरह मानना चाहिए, भले ही client और server एक साथ ship हों।

[NOVA]: इससे incident response भी बदल जाता है। terminal-only model में, एक ऑपरेटर shell transcript में पीछे स्क्रॉल करके working tree की जांच कर सकता है। remote app-server model में, सबूत thread storage, tool operation records, telemetry, review approvals, plugin metadata और environment-specific file views में बंटे होते हैं। runtime को पर्याप्त state बनाए रखनी होती है ताकि बाद में पता लगाया जा सके कि क्या हुआ।

[ALLOY]: और चूंकि remote clients फिर से कनेक्ट हो सकते हैं, सेशन को partial client failure के खिलाफ मज़बूत होना चाहिए। अगर compaction के दौरान browser tab डिस्कनेक्ट हो जाए, तो server को अभी भी terminal event चाहिए। अगर patch आंशिक रूप से लागू हो और client refresh हो, तो server को अभी भी real diff चाहिए। अगर लंबे thread के दौरान config बदले, तो active policy समझने योग्य होना चाहिए। यही वजह है कि ये छोटे-छोटे सुधार मिलकर एक अधिक विश्वसनीय remote-control runtime बनाते हैं।

[NOVA]: यह release सिर्फ नए commands के बारे में नहीं है। यह एक coding agent को controllable, inspectable और recoverable बनाने के बारे में है जब सेशन बड़े हो जाएं और remotely चलें।

[NOVA]: कहानी दो माइक्रोसॉफ्ट की AI एजेंट फ्रेमवर्क में remote code execution पर सुरक्षा केस स्टडी है। महत्वपूर्ण बात यह है कि मॉडल मुख्य विफलता में असुरक्षित घटक नहीं है। खतरनाक सीमा फ्रेमवर्क और प्लगइन कोड है जो मॉडल-नियंत्रित टूल आर्ग्यूमेंट पर भरोसा करता है और उन्हें executable host behavior में बदल देता है।

[ALLOY]: सामने आई जानकारी Semantic Kernel के In-Memory Vector Store search flow पर केंद्रित है। उदाहरण एजेंट एक होटल खोज प्लगइन प्रदर्शित करता है। उपयोगकर्ता एक शहर में होटल मांगता है। मॉडल एक शहर आर्ग्यूमेंट के साथ search function को कॉल करता है। प्लगइन vector similarity search से पहले एक फ़िल्टर बनाता है। जोखिम भरा कदम यह है कि एक मॉडल-नियंत्रित मान एक Python lambda expression में interpolated किया जाता है और eval के साथ execute किया जाता है।

[NOVA]: यही बाउंडरी क्रॉसिंग है। एक सामान्य शहर स्ट्रिंग फ़िल्टर expression का हिस्सा बन जाती है। एक दुर्भावनापूर्ण स्ट्रिंग एक quote बंद कर सकती है और Python logic जोड़ सकती है। Prompt injection को ब्राउज़र exploit या memory corruption की जरूरत नहीं होती जब फ्रेमवर्क natural-language-controlled मानों को code में बदल देता है। एजेंट text से host execution तक का रास्ता बन गया है।

[ALLOY]: प्रयास किया गया mitigation AST validation और restricted builtins environment का उपयोग करता है। उच्च स्तर पर, validator lambda expressions को allow करता है, खतरनाक identifiers के लिए names और attributes को स्कैन करता है, और builtins हटाकर execute करता है। यह सुवादयुक्त लगता है, लेकिन dynamic languages blocklists को भ脆弱 बना देती हैं।

[NOVA]: माइक्रोसॉफ्ट के शोधकर्ताओं ने obvious blocked names पर सीधे निर्भर हुए बिना फ़िल्टर को bypass किया। payload ने Python object structures को traverse किया import machinery तक पहुंचने और alternate attributes के माध्यम से command execution तक पहुंचने के लिए। यह known-dangerous tokens को ban करके general host-language evaluator को सुरक्षित बनाने की कोशिश करने की क्लासिक समस्या है।

[ALLOY]: सबक सिर्फ "eval का उपयोग न करें" नहीं है, हालांकि यह एक अच्छी शुरुआत है। व्यापक सबक यह है कि tool-call arguments अविश्वसनीय input हैं भले ही वे एक मॉडल से आए हों, भले ही उपयोगकर्ता ने सीधे code नहीं टाइप किया हो, और भले ही schema दावा करता हो कि फ़ील्ड something harmless जैसे कि city name है।

[NOVA]: एक मॉडल को attacker-controlled strings को किसी भी argument में रखने के लिए प्रेरित किया जा सकता है जिसे वह भरने की अनुमति देता है। अगर टूल उस स्ट्रिंग को code, query language, shell command, file path, template, या serialized expression के रूप में interpret करता है, तो फ्रेमवर्क ने एक injection sink बना दिया है।

[ALLOY]: Vector search इस मुद्दे को underestimate करना आसान बनाता है क्योंकि यह retrieval infrastructure जैसा लगता है, code execution नहीं। लेकिन vector stores अक्सर metadata filters, expression languages, custom predicates, embedding prefilters, rerankers, और connector-specific query strings का समर्थन करते हैं। इनमें से कोई भी injection boundary बन सकता है अगर user या model-controlled मान interpreted expression में concatenated किए जाते हैं।

[NOVA]: सुरक्षित design आमतौर पर parameterized filters, typed DSLs, allowlisted operators, और validation का मतलब है जो execution से पहले unexpected structure को reject करता है। Field equals value data होनी चाहिए, source code नहीं। अगर filter language अपरिहार्य है, तो runtime को एक constrained AST में parse करना चाहिए और एक interpreter के साथ evaluate करना चाहिए जो केवल allowed operations को समझता है। इसको host language evaluator को कॉल नहीं करना चाहिए और बाद में dangerous behavior को block करने की कोशिश नहीं करनी चाहिए।

[ALLOY]: Least privilege भी मायने रखता है। एक hotel-search predicate को shell access की जरूरत नहीं है। अगर फ्रेमवर्क bug एक फ़िल्टर को code execution में बदल देता है, तो sandbox और process privileges blast radius तय करते हैं। Agent frameworks को plugin execution को isolate करना चाहिए, environment variables को limit करना चाहिए, generic tool processes में credentials pass करने से बचना चाहिए, और tool parameters को इतनी सावधानी से log करना चाहिए कि incident response के लिए काफी हो।

[NOVA]: डिटेक्शन काफी व्यावहारिक है। टीमों को उन टूल्स का इन्वेंट्री बनाना चाहिए जो टेम्पलेट्स, फिल्टर्स, शेल कमांड्स, नोटबुक सेल्स, Python स्निपेट्स, JavaScript स्निपेट्स, SQL, या फाइल ऑपरेशंस execute करते हैं। फिर उन्हें ट्रेस करना चाहिए कि मॉडल-कंट्रोल्ड वैल्यूज उन इंटरप्रेटर्स तक पहुंच सकती हैं या नहीं। Semantic Kernel को पैच करना affected path के यूजर्स के लिए ज़रूरी है, लेकिन कस्टम प्लगइन्स अक्सर उसी पैटर्न को repeat करती हैं।

[ALLOY]: टेस्टिंग का एक और पाठ है। एक सामान्य यूनिट टेस्ट पास हो सकता है क्योंकि वह एक friendly city name, एक friendly category, या एक friendly metadata field चेक करता है। सिक्योरिटी टेस्ट्स को adversarial values की ज़रूरत होती है जो expected syntax से बाहर निकलने की कोशिश करती हैं। एक वेक्टर फिल्टर के लिए, इसका मतलब है quotes, braces, operators, attribute traversal, बहुत लंबी स्ट्रिंग्स, असामान्य unicode, और उन objects को रेफर करने की कोशिशें जो कभी reachable नहीं होने चाहिए। टेस्ट को assert करना चाहिए कि ये वैल्यूज डेटा बनी रहें।

[NOVA]: एक उपयोगी रिव्यू सवाल है, "पहला interpreter कहाँ है?" अगर एक वैल्यू JSON के रूप में parse होती है, तो वह एक boundary है। अगर यह SQL बन जाती है, तो यह दूसरी है। अगर यह एक Python lambda, shell command, template, regular expression, या file path बन जाती है, तो हर step के लिए अपना own validation rule चाहिए। सबसे खराब पैटर्न यह है कि user या model data को string में बदलना जो later में एक ज़्यादा powerful language द्वारा interpret हो, जिसकी schema ने promised नहीं किया था।

[ALLOY]: Framework maintainers को भी safe path को default path बनाना होगा। अगर documentation में easy example string concatenation into a filter expression का उपयोग करता है, तो downstream applications इसे copy करेंगे। अगर default vector store helper एक typed filter builder accept करता है, तो कम applications अपना unsafe version invent करेंगे। Agent security बेहतर होती है जब framework ergonomics developers को safe composition की ओर push करता है।

[NOVA]: इसीलिए यह research एक bug से आगे matters है। यह builders को एक concrete mental model देता है: prompt injection तब तक host compromise नहीं बनता जब तक language-controlled data और privileged execution के बीच एक bridge नहीं होता। Bridges को खोजें, उन्हें narrow करें, और interpreters को normal path से remove करें।

[ALLOY]: यहीं पर OpenClaw का own operating model relevant है। OpenClaw inbound DMs और channel messages को untrusted input की तरह treat करता है। इसमें एक local-first gateway, channel routing, tool policies, और non-main sessions के लिए sandboxing options हैं। लेकिन यह जादुई रूप से हर called framework को safe नहीं बनाता। अगर OpenClaw एक external agent framework को invoke करता है, तो same rule apply होता है: framework एक tool boundary है, trusted internal language नहीं।

[NOVA]: सही। अगर एक Microsoft Agent Framework workflow, एक Semantic Kernel plugin, या कोई other external runtime OpenClaw से called जाता है, तो integration को एक narrow command contract, typed inputs, allowlisted actions, environment isolation, timeouts, और structured outputs define करने चाहिए। Host को external runtime को unlimited filesystem, network, token, या shell access नहीं देनी चाहिए जब तक कि यह truly intended न हो।

[ALLOY]: Operator takeaway सख्त है: every agent tool एक API endpoint है जिसका caller model द्वारा partly controlled है। Tool schemas को external API contracts की तरह treat करें। Boundary पर inputs validate करें। Interpreted strings के बजाय typed data structures को prefer करें। Permissions narrow रखें। इतना log करें कि reconstruct किया जा सके कि किस prompt ने कौन से tool arguments produce किए। और prompt injection test करें hostile parameters को tools में force करने की कोशिश करके, न कि सिर्फ यह check करके कि model unsafe words कहता है या नहीं।

[NOVA]: Prompt-injection security सिर्फ model behavior नहीं है। यह input validation है, interpreter avoidance है, sandboxing है, और runtime के लिए least-privilege design है जो काम execute करता है।

[NOVA]: Story three GitHub Copilot SDK का May 8 pre-release है। यह coding-agent sessions को products में embed करने के बारे में है जिसमें ज़्यादा explicit runtime control है।

[ALLOY]: अब एप्लिकेशन exitPlanMode.request और autoModeSwitch.request के लिए कॉलबैक रजिस्टर कर सकती हैं। ये इवेंट्स मायने रखते हैं क्योंकि प्लान मोड और ऑटोमैटिक मॉडल स्विचिंग प्रोडक्ट फैसले हैं, सिर्फ मॉडल फैसले नहीं।

[NOVA]: प्लान मोड प्रपोज़िंग वर्क और डूइंग वर्क के बीच एक बाउंड्री है। एम्बेडेड कोडिंग एजेंट में, एप्लिकेशन चाह सकती है कि कोई इंसान प्लान को approve करे, कोई पॉलिसी इंजन उसे चेक करे, या कोई प्रोजेक्ट-स्पेसिफिक रूल कुछ बदलावों को ब्लॉक करे। exit-plan-mode रिक्वेस्ट्स के लिए हैंडलर होस्ट प्रोडक्ट को runtime को एक्जीक्यूशन में ले जाने से पहले एक क्लियर इंटरसेप्शन पॉइंट देता है।

[ALLOY]: रेट लिमिट्स के बाद ऑटोमैटिक मॉडल स्विचिंग एक अलग बाउंड्री है। एक runtime रेट-लिमिट इवेंट से दूसरे मॉडल या मोड पर जाकर रिकवर होना चाह सकती है। यह कंटिन्यूइटी बनाए रख सकती है, लेकिन यह बिहेवियर, कॉस्ट, लेटेंसी या कैपेबिलिटी को भी बदल सकती है। autoModeSwitch.request हैंडलर एप्लिकेशन को यह तय करने देता है कि स्विच को एक्सेप्ट करना है या नहीं।

[NOVA]: एंटरप्राइज प्रोडक्ट्स के लिए, यह मायने रखता है क्योंकि मॉडल चॉइस डेटा पॉलिसी, कंप्लायंस, इवैल्यूएशन बेसलाइंस और बजट कंट्रोल्स से जुड़ा हो सकता है। एक फॉलबैक जो runtime को बेकार लगता है वो होस्ट एप्लिकेशन के लिए अनएक्सेप्टेबल हो सकता है अगर वो प्रोवाइडर बाउंड्री को क्रॉस करता है या रिटेंशन पॉलिसी को बदलता है।

[ALLOY]: रिलीज़ .NET, Python और Rust SDKs में स्ट्रक्चर्ड डायग्नोस्टिक्स भी जोड़ती है। लॉग्स CLI स्टार्टअप, TCP कनेक्शन, JSON-RPC रिक्वेस्ट टाइमिंग, सेशन लाइफसाइकल और एरर पाथ्स को कवर करते हैं। ये वो विजिबिलिटी है जो एम्बेडेड एजेंट SDK को चाहिए।

[NOVA]: जब सेशन फेल होता है, तो कारण प्रोसेस स्टार्टअप, ट्रांसपोर्ट, ऑथेंटिकेशन, JSON-RPC फ्रेमिंग, runtime इवेंट हैंडलिंग, मॉडल रिस्पॉन्स, टूल एक्जीक्यूशन या होस्ट कॉलबैक बिहेवियर हो सकता है। बिना स्ट्रक्चर्ड टाइमिंग और लाइफसाइकल लॉग्स के, सब कुछ "एजेंट हंग" की तरह लगता है।

[ALLOY]: JSON-RPC डिटेल सबसे अहम है। कई कोडिंग-एजेंट SDKs एक लोकल runtime प्रोसेस को रैप करते हैं और JSON-RPC पर कम्यूनिकेट करते हैं। यह एप्लिकेशन में एक क्लाइंट ऑब्जेक्ट, एक runtime प्रोसेस, एक ट्रांसपोर्ट कनेक्शन, रिक्वेस्ट IDs, इवेंट स्ट्रीम्स और लॉन्ग-रनिंग ऑपरेशंस बनाता है। डायग्नोस्टिक्स को दिखाना चाहिए कि runtime कब शुरू हुआ, TCP कनेक्शन कब खुला, कौन सी रिक्वेस्ट्स भेजी गईं, उन्हें कितना टाइम लगा, और एरर कहां सरफेस हुईं।

[NOVA]: enableSessionTelemetry ऑप्शन टेलीमेट्री को एक explicit सेशन चॉइस बनाता है। ये प्राइवेसी और ऑपरेशंस के लिए सही फॉर्म है। कुछ डिप्लॉयमेंट्स सेशन टेलीमेट्री चाहते हैं ताकि इश्यूज डिबग कर सकें और रिलायबिलिटी इम्प्रूव कर सकें। दूसरों को पॉलिसी से इसे डिसेबल करने की जरूरत है। सेशन कॉन्फिगरेशन और रिज्यूम कॉन्फिगरेशन पर नॉब लगाने से फैसला ऑडिटेबल और रिपीटेबल बनता है।

[ALLOY]: छोटे कम्पैटिबिलिटी फिक्सेस हैं जिनका रियल इम्पैक्ट है। C# सेशन-इवेंट enums अब string-backed readonly structs हैं ताकि deserialization फेल न हो जब runtime नए enum वैल्यूज जोड़ता है। ये इवेंट स्ट्रीम्स के लिए फॉरवर्ड कम्पैटिबिलिटी है। Rust बाइनरी टूल रिजल्ट रिसोर्स ब्लॉब्स अब mimeType अनुपस्थित होने पर application/octet-stream पर डिफॉल्ट करते हैं। ये वायर-फॉर्मेट रेज़िलिएंस है।

[NOVA]: प्रैक्टिकल बिल्डर इम्प्लिकेशन ये है कि Copilot SDK सेशन्स होस्ट-कंट्रोल्ड runtime ऑब्जेक्ट्स बन रहे हैं। अगर आप उन्हें embed करते हैं, तो प्लान-मोड और मोड-स्विच कॉलबैक्स को deliberately implement करें। तय करें कि कौन से स्विचेस ऑटोमैटिकली हो सकते हैं और कौन से रिव्यू की जरूरत है। डेवलपमेंट और स्टेजिंग में diagnostics को टर्न ऑन करें। स्लो या फ्लैकी सेशन्स के आसपास JSON-RPC टाइमिंग कैप्चर करें। टेलीमेट्री को पॉलिसी की तरह ट्रीट करें, hidden डिफॉल्ट की तरह नहीं।

[ALLOY]: और नए runtime events के खिलाफ पुराने clients को test करें। Event streams evolve करते हैं। अगर enum handling या MIME defaults टूटते हैं, तो agent काम कर रहा हो सकता है जबकि host product deserialize नहीं कर पा रहा कि क्या हुआ।

[NOVA]: Story four है Microsoft Agent Framework 1.5। Release बड़ी है, लेकिन कई changes directly relevant हैं production agent builders के लिए: Magentic Orchestration for .NET, WebBrowsingTool allowlisting, hosted-agent observability samples, reasoning events in AGUI, class-based skills और harness context providers in the Python line, todo-state injection, Foundry per-call headers, और wire-format fix for function_call_output.output।

[ALLOY]: Magentic Orchestration headline है क्योंकि multi-agent systems को agents की list से ज्यादा चाहिए। उन्हें scheduling, delegation, turn ownership, shared state, termination conditions, और एक तरीका चाहिए कि decide हो कि कौन सा actor अगला move करे। Orchestration layer उन mechanics को formalize करती है। इसे experimental mark करना appropriate है क्योंकि orchestration semantics application architecture बन जाते हैं।

[NOVA]: एक bad scheduler loop कर सकता है, काम duplicate कर सकता है, failures छुपा सकता है, या एक agent को conversation पर हावी होने दे सकता है। Multi-agent orchestration जादुई collaboration नहीं है। यह runtime policy है कि who acts, when they act, what context they see, और when the process stops।

[ALLOY]: WebBrowsingTool allowlisting एक important browser-control feature है। Browsing tools agent को external content से connect करते हैं जो malicious, untrusted, या बस distracting हो सकता है। An allowlist host application को browser tool चलने से पहले policy surface देता है।

[NOVA]: Agent systems में, browsing सिर्फ reading नहीं है। Browser prompt-injection content fetch कर सकता है, forms submit कर सकता है, redirects follow कर सकता है, cookies expose कर सकता है, files retrieve कर सकता है, और authenticated sessions के साथ interact कर सकता है। Policy tool execution से पहले मौजूद होनी चाहिए, न कि सिर्फ तब जब एक बुरा page पहले ही run को influence कर चुका है।

[ALLOY]: Hosted-agent observability samples भी valuable हैं क्योंकि deployment वही जगह है जहाँ framework abstractions production reality से मिलते हैं। एक hosted agent को logs, traces, request correlation, model-call visibility, tool-call timing, और failure state चाहिए। उपयोगी सवाल यह है कि क्या एक team external request से orchestration, model call, tool call, और final response तक एक failed run को reconstruct कर सकती है।

[NOVA]: AGUI में reasoning events एक transport issue को expose करते हैं। User interfaces को agent progress render करनी होती है बिना private chain-of-thought, tool rationale, और user-visible summaries को गलत तरीके से mix किए। एक reasoning event channel framework को progress या reasoning-related state को structured events के रूप में represent करने देता है। Application को अभी भी तय करना है कि क्या दिखाना, store करना, और transmit करना safe है।

[ALLOY]: Todo multithreading और message list में todo injection दिखाते हैं कि task state कैसे एक runtime feature बन जाता है। Agents todo lists का उपयोग plan करने, progress track करने, और interruptions के बाद recover करने के लिए करते हैं। अगर todo state thread-safe नहीं है, तो concurrent updates plan को corrupt कर सकते हैं। अगर todo state message context में visible नहीं है, तो model commitments का track खो सकता है।

[NOVA]: function_call_output.output wire-format fix छोटा है लेकिन critical है। Release इसे wire पर JSON string बनाने के लिए fix करता है। Tool output formats runtime, SDKs, models, और clients के बीच contracts हैं। अगर एक side string expect करता है और दूसरा side structured JSON directly send करता है, तो deserialization, replay, storage, या compaction fail हो सकते हैं।

[ALLOY]: सीक्वेंस नंबर जेनरेशन को डुप्लिकेट या गलत क्रम वाले IDs के लिए फिक्स मिला। इवेंट ऑर्डरिंग एजेंट UIs और लॉग्स के लिए बेसिक है। अगर दो इवेंट्स एक ही सीक्वेंस नंबर शेयर करें या गलत क्रम में आएं, तो क्लाइंट्स पुराना स्टेट रेंडर कर सकते हैं, अपडेट्स ड्रॉप कर सकते हैं, या टूल रिजल्ट को गलत टर्न से अटैच कर सकते हैं। मल्टी-एजेंट या मल्टीपार्टी कन्वर्सेशन में, ऑर्डरिंग बग्स खास तौर पर परेशान करने वाले होते हैं।

[NOVA]: वर्कफ्लो री-एंट्री और YAML पार्सिंग फिक्सेस डिक्लेरेव एजेंट रिलायबिलिटी की तरफ इशारा करते हैं। GotoAction री-एंट्री के बाद लूप वर्कफ्लो सुविधा को बेकाबू व्यवहार में बदल सकता है। फाइल स्किल्स के लिए YAML ब्लॉक स्केलर पार्सिंग मायने रखती है क्योंकि फाइल-बेस्ड स्किल्स में अक्सर प्रॉम्प्ट्स, इंस्ट्रक्शन्स, उदाहरण, या स्क्रिप्ट्स होते हैं। अगर ब्लॉक स्केलर्स गलत तरीके से पार्स हों, तो एजेंट जो स्किल देखता है वह वह नहीं है जो डेवलपर ने लिखी थी।

[ALLOY]: अब OpenClaw इंटीग्रेशन सवाल पर आते हैं। क्या Microsoft Agent Framework को OpenClaw के अंदर इस्तेमाल किया जा सकता है? हाँ, लेकिन क्लीन आर्किटेक्चर एडाप्टर-बेस्ड है। OpenClaw एक लोकल-फर्स्ट असिस्टेंट गेटवे है जो पहले से ही चैनल्स, सेशन्स, टूल्स, नोड्स, ब्राउज़र और कैनवस सर्फेस, क्रॉन, स्किल्स, सैंडबॉक्सिंग, और मल्टी-एजेंट राउटिंग मैनेज करता है। Microsoft Agent Framework एक अलग एजेंट फ्रेमवर्क है जिसके .NET और Python सर्फेस हैं। इसे एक कॉल्ड रनटाइम के रूप में इंटीग्रेट किया जाना चाहिए, OpenClaw के नेटिव सेशन रनटाइम के साथ इसे भूलना नहीं चाहिए।

[NOVA]: कई काम करने योग्य पैटर्न हैं। पहला, कमांड-बैक्ड स्किल: OpenClaw एक लोकल स्क्रिप्ट या सर्विस को इनवोक कर सकता है जो Microsoft Agent Framework वर्कफ्लो चलाता है और एक स्ट्रक्चर्ड रिजल्ट लौटाता है। यह सबसे सिम्पल फॉर्म है। स्किल इनपुट टाइप्ड होता है। फ्रेमवर्क प्रोसेस एक डिफाइंड वर्किंग डायरेक्टरी और एनवायरनमेंट के साथ चलता है। आउटपुट टेक्स्ट या JSON के रूप में कैप्चर किया जाता है। टाइमआउट्स और फेलियर हैंडलिंग OpenClaw में ही रहती है।

[ALLOY]: दूसरा, होस्टेड लोकल सर्विस: एक .NET या Python Agent Framework ऐप एक लोकलहोस्ट सर्विस या प्राइवेट नेटवर्क सर्विस के रूप में चल सकता है। OpenClaw इसे एक नैरो HTTP या RPC एडाप्टर के ज़रिए कॉल करता है। यह तब उपयोगी है अगर फ्रेमवर्क को लॉन्ग-लिव्ड ऑर्केस्ट्रेशन स्टेट, वार्म मॉडल क्लाइंट्स, या अपनी ऑब्जर्वेबिलिटी पाइपलाइन की ज़रूरत है। OpenClaw अभी भी मैनेज करता है कि कौन सा चैनल इसे कॉल कर सकता है और कौन सी क्रेडेंशियल्स एक्सपोज की जाती हैं।

[NOVA]: तीसरा, टूल-प्रोटोकॉल ब्रिज: अगर Agent Framework वर्कफ्लो को एक टूल सर्वर के पीछे एक्सपोज किया जा सकता है, तो OpenClaw इसे दूसरे टूल प्रोवाइडर की तरह ट्रीट कर सकता है। अहम हिस्सा बाउंड्री है। टूल नेम्स, स्कीमास, अलाउड ऑपरेशन्स, और रिटर्न्ड आर्टिफैक्ट्स स्पष्ट होने चाहिए। OpenClaw को हर फ्रेमवर्क प्रोसेस की हर क्षमता को हर सेशन में ब्लाइंडली इम्पोर्ट नहीं करना चाहिए।

[ALLOY]: चौथा, सैंडबॉक्स्ड सबएजेंट लेन: OpenClaw चुनिंदा टास्क्स को एक नॉन-मेन एजेंट या सैंडबॉक्स में राउट कर सकता है जिसके पास एक्सटर्नल फ्रेमवर्क चलाने की परमिशन है। यह एक्सपेरिमेंट्स के लिए सुरक्षित पैटर्न है क्योंकि फ्रेमवर्क को सीमित फाइलसिस्टम और नेटवर्क एक्सेस दिया जा सकता है। यह ब्राउज़र टूल्स और होस्टेड वर्कफ्लोज़ के लिए खास तौर पर रिलेवेंट है जो अनट्रस्टेड कंटेंट से ग्रसित हो सकते हैं।

[NOVA]: इंटीग्रेशन लिमिट्स उतनी ही ज़रूरी हैं। Microsoft Agent Framework अपने आप OpenClaw का नेटिव चैनल नहीं बनता। यह अपने आप OpenClaw के पेयरिंग पॉलिसी, Discord या Telegram राउटिंग, लाइव कैनवस व्यवहार, नोड मैनेजमेंट, मेमोरी मॉडल, या अप्रूवल गेट्स को इनहेरिट नहीं करता। इन सबको जानबूझकर रैप करना होगा। यह अपनी डिपेंडेंसीज़, इवेंट मॉडल, स्किल सेमांटिक्स, और टूल-आउटपुट कॉन्ट्रैक्ट्स भी लाता है।

[ALLOY]: Semantic Kernel स्टोरी से सिक्योरिटी लेसन सीधे लागू होता है। अगर OpenClaw Microsoft Agent Framework एजेंट को कॉल करता है, तो एक रनटाइम से मॉडल-जेनरेटेड आर्गुमेंट्स दूसरे रनटाइम के टूल्स में जा सकते हैं। इसका मतलब यह है कि वैलिडेशन को असुमित नहीं माना जा सकता। एक सुरक्षित ब्रिज में टाइप्ड रिक्वेस्ट ऑब्जेक्ट्स, अलाउलिस्टेड ऑपरेशन्स, रेडैक्टेड लॉग्स, लीस्ट-प्रिविलेज एनवायरनमेंट वेरिएबल्स, स्पष्ट ब्राउज़र अलाउलिस्ट्स, और डिफ़ॉल्ट रूप से कोई जेनरिक शेल एक्सेस नहीं होना चाहिए।

[NOVA]: ऑब्जर्वेबिलिटी को भी एक ब्रिज की ज़रूरत है। OpenClaw यूज़र मैसेज, सेशन, टूल कॉल, और रिप्लाई को ट्रेस कर सकता है। Microsoft Agent Framework ऑर्केस्ट्रेशन, मॉडल कॉल्स, टूल कॉल्स, रीज़निंग इवेंट्स, और वर्कफ्लो स्टेट को ट्रेस कर सकता है। एक प्रोडक्शन इंटीग्रेशन में एक कॉरिलेशन ID उस बाउंड्री को पार करके जानी चाहिए ताकि एक फेल्ड रिक्वेस्ट को चैनल मैसेज से OpenClaw सेशन से एक्सटर्नल फ्रेमवर्क इनवोकेशन तक और वापस ट्रैक किया जा सके।

[ALLOY]: व्यावहारिक सिफारिश है सतर्क आशावाद। Microsoft Agent Framework का उपयोग OpenClaw के अंदर तभी करें जब यह एक विशिष्ट क्षमता प्रदान करता है: Magentic-style ऑर्केस्ट्रेशन, Foundry इंटीग्रेशन, hosted-agent सैंपल, declarative स्किल्स, या .NET या Python में पहले से लिखा गया वर्कफ़्लो। इसलिए इसका उपयोग न करें क्योंकि यह एक और agent framework है। अगर OpenClaw पहले से ही आवश्यक चैनल, सेशन और टूल व्यवहार प्रदान करता है, तो दूसरा framework जोड़ना जटिलता बढ़ा सकता है बिना किसी मूल्य के।

[NOVA]: सबसे अच्छा पहला प्रयोग संकीर्ण होगा। एक Microsoft Agent Framework वर्कफ़्लो बनाएं जो एक निहित कार्य करता है, इसे एक OpenClaw skill या लोकल सर्विस के माध्यम से एक्सपोज़ करें, एक टाइप्ड इनपुट ऑब्जेक्ट पास करें, एक स्ट्रक्चर्ड रिज़ल्ट रिटर्न करें, इसे बिना ब्रॉड क्रेडेंशियल्स के चलाएं, और correlation ID को लॉग करें। फिर latency, reliability, टूल सेफ्टी का मूल्यांकन करें, और यह देखें कि orchestration रिज़ल्ट एक native OpenClaw skill से बेहतर है या नहीं।

[ALLOY]: अगर जवाब हाँ है, तो सावधानी से विस्तार करें। ब्राउज़र एक्सेस केवल allowlists के साथ जोड़ें। फाइल एक्सेस केवल एक scoped workspace तक सीमित रखें। क्रेडेंशियल्स केवल explicit secret references या environment injection के माध्यम से जोड़ें। पर्सिस्टेंट स्टेट केवल तब जोड़ें जब replay और resume semantics स्पष्ट हों। और किसी framework bridge को कभी चैट सेशन की अनुमतियों को चुपचाप बढ़ाने न दें।

[NOVA]: तो जवाब "नहीं, क्योंकि OpenClaw अलग है" नहीं है, और न ही "हाँ, बस इसे इंस्टॉल करें और इसे सब कुछ चलाने दें" है। जवाब है: हाँ, Microsoft Agent Framework का उपयोग एक एकीकृत बाहरी रनटाइम के रूप में OpenClaw डिप्लॉयमेंट के अंदर किया जा सकता है, लेकिन OpenClaw को चैनल इंग्रेस, यूज़र ट्रस्ट, टूल पॉलिसी, सैंडबॉक्सिंग और डिलीवरी के लिए अधिकारी बने रहना चाहिए।

[ALLOY]: कुछ मामले हैं जहाँ integration इसके काबिल होगी। अगर किसी टीम के पास पहले से Foundry, Magentic Orchestration, declarative वर्कफ़्लोज़, या Microsoft's hosted-agent सैंपल्स के आसपास बनाए गए .NET agents हैं, तो OpenClaw के लिए उस काम को रैप करना निवेश को संरक्षित कर सकता है। OpenClaw इसके चारों ओर पर्सनल ऑपरेटिंग लेयर बन सकता है: मैसेज इंटेक, यूज़र अप्रूवल, चैनल डिलीवरी, शेड्यूल ट्रिगर्स, फाइल स्टेजिंग और लोकल मशीन कंट्रोल।

[NOVA]: ऐसे भी मामले हैं जहाँ यह इसके काबिल नहीं होगी। अगर टास्क एक सिंपल लोकल ऑटोमेशन है, तो एक सामान्य OpenClaw skill शायद इंस्पेक्ट और ऑपरेट करने में आसान होगी। अगर टास्क को एक टूल कॉल और एक जवाब की जरूरत है, तो दूसरा orchestration framework जोड़ने से value से ज्यादा serialization, ज्यादा लॉग्स, ज्यादा dependencies और ज्यादा failure modes बन सकते हैं। Integration को orchestration, मौजूदा कोड, hosted-agent इंफ्रास्ट्रक्चर, या कंक्रीट Microsoft ecosystem requirement से justified होना चाहिए।

[ALLOY]: versioning एक और असली बात है। OpenClaw, बाहरी framework, मॉडल SDKs और टूल स्कीमास सभी स्वतंत्र रूप से evolve हो सकते हैं। एक bridge को framework वर्जन घोषित करना चाहिए जो वह उम्मीद करता है, रिटर्न किए गए इवेंट शेप्स को validate करना चाहिए, और जब wire contract बदलता है तो स्पष्ट रूप से fail होना चाहिए। चुपचाप partial compatibility खतरनाक है क्योंकि यह एक agent को काम करता हुआ दिखा सकता है जबकि todo state, टूल आउटपुट, sequence ordering या reasoning events खो रहा हो।

[NOVA]: recommended shape जानबूझकर boring है: एक adapter, एक schema, एक permission profile, एक correlation ID, एक timeout policy, और एक स्पष्ट रूप से documented आउटपुट। वहाँ से शुरू करें। अगर यह काम करता है, तो धीरे-धीरे capabilities जोड़ें। लक्ष्य यह नहीं है कि OpenClaw और Microsoft Agent Framework को अविभेद्य बनाया जाए। लक्ष्य है कि OpenClaw को एक उपयोगी बाहरी agent runtime को सुरक्षित रूप से कॉल करने दिया जाए जब वह runtime अपनी जगह कमाता है।

[ALLOY]: EP048 से व्यावहारिक takeaway operational है। Codex 0.130.0 coding-agent सेशन्स को remote-control app servers, paged thread views, plugin hook visibility, config refresh, बेहतर patch diffs, compaction fixes और multi-environment file resolution के साथ ज्यादा service-like बनाता है।

[NOVA]: Microsoft's Semantic Kernel रिसर्च दिखाता है कि model-controlled tool arguments code execution कैसे बन सकते हैं अगर frameworks उन्हें interpreted host-language expressions में बदलते हैं। GitHub Copilot SDK embedded products को approval और recovery hooks plus diagnostics देता है। Microsoft Agent Framework 1.5 orchestration, browser policy, observability, event transport, todo state और wire-format correctness को आगे बढ़ाता है।

[ALLOY]: और OpenClaw के प्रश्न पर: Microsoft Agent Framework को OpenClaw के अंदर एक सीमित बाहरी रनटाइम, सेवा, कौशल, या टूल ब्रिज के रूप में उपयोग किया जा सकता है। इससे OpenClaw के अपने विश्वास, रूटिंग, सैंडबॉक्स और अनुमोदन मॉडल को दरकिनार नहीं किया जाना चाहिए।

[NOVA]: बिल्डर्स के लिए, हर एजेंट रनटाइम बाउंड्री को स्पष्ट बनाएं: कंट्रोल प्लेन, टूल इनपुट, अनुमोदन इवेंट, ब्राउज़र पॉलिसी, टेलीमेट्री, फ्रेमवर्क ब्रिज और संग्रहीत थ्रेड स्टेट। OpenClaw Daily सुनने के लिए धन्यवाद। शो नोट्स और स्रोत लिंक Toby On Fitness Tech dot com पर उपलब्ध हैं, और हम जल्द ही वापस आएंगे।