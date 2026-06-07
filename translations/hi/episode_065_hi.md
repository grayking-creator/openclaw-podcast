[NOVA]: मैं NOVA हूँ।

[ALLOY]: मैं ALLOY हूँ, और ये है AgentStack Daily...

[NOVA]: आज, एजेंट-हार्नेस सतह खबर में है। Hermes Agent zero point sixteen ने "The Surface Release" जारी किया — एक असली नेटिव Electron डेस्कटॉप ऐप OAuth रिमोट कनेक्ट, ड्रैग-एंड-ड्रॉप फ़ाइल इनपुट, और एक पूरा ब्राउज़र-आधारित एडमिनिस्ट्रेशन पैनल के साथ, 874 कमिट्स में एक सिंगल रिलीज़ साइकल में। OpenAI Codex zero point one thirty seven ने मल्टी-एजेंट v2 जोड़ा जिसमें थ्रेड के हिसाब से रनटाइम चॉइस पर्सिस्टेंस, पैरलल स्टैंडअलोन वेब सर्च, और एंटरप्राइज़ फ्लो में मंथली क्रेडिट लिमिट विजिबिलिटी। Claude Code two point one point one sixty six ने तीन मॉडल्स तक कॉन्फ़िगर करने योग्य फ़ॉलबैक मॉडल चेन और glob टूल-नेम डेनी रूल्स पेश किए, जिसके बाद two point one point one sixty seven बग-फिक्स पॉलिश रिलीज़ के रूप में आया। हार्नेस अपडेट्स के बाद, मॉडल लेन Gemma 4 12B पर आती है — Google's encoder-free मल्टीमॉडल रिलीज़ जो 16 गीगाबाइट VRAM में फिट होती है। प्रोजेक्ट रडार में A2A Protocol का Linux Foundation के तहत v1.0 तक पहुँचना, Kimi Code CLI एक TypeScript-native टर्मिनल कोडिंग एजेंट के रूप में, और awesome-ai-agents-2026 curated रिसोर्स लिस्ट शामिल है — आगे पढ़ने के लिए डेफिनिटिव इंडेक्स।

[ALLOY]: इस हफ्ते का क्रम हार्नेस लेयर को पहले रखता है क्योंकि सतह का क्षेत्र वही है जो बदला। मॉडल स्टोरी मजबूत है, लेकिन टूलिंग जिससे ऑपरेटर्स जुड़ते हैं — वही जगह है जहाँ रिलायबिलिटी बनती या टूटती है। Hermes Agent अब एक ऐप्लिकेशन बन गया है जिसे आपके नॉन-टेक्निकल टीममेट्स वास्तव में इस्तेमाल करेंगे। Codex उन गैप्स को भर रहा है जो मल्टी-एजेंट सेशन्स को हैंडऑफ में अपनी जगह खोने देते हैं। Claude Code अब फ़ॉलबैक मॉडल्स चेन कर सकता है ताकि saturating API एजेंट को रोक न दे। और जो मॉडल स्टोरी आगे आती है वो लोकल-फर्स्ट एजेंट स्टैक्स के लिए एक गंभीर open-weight रिलीज़ है। ...

[NOVA]: तीन लेयर्स एक साथ आगे बढ़ रही हैं, और सुनने का सबसे उपयोगी तरीका है उन्हें अलग रखना। हार्नेस लेयर वो है जिस पर एजेंट चलता है, और इस साइकल में एजेंट-हार्नेस रिलीज़ हर प्राइमरी सतह को छूती है जिससे ऑपरेटर्स वास्तव में जुड़ते हैं — डेस्कटॉप, टर्मिनल, फ़ॉलबैक राउटिंग, और मल्टी-एजेंट हैंडऑफ। मॉडल लेयर वो है जो एजेंट के आउटपुट की क्वालिटी तय करती है। टूलिंग लेयर open-source प्रोजेक्ट रडार है जो मेजर रिलीज़ेस के बीच के गैप्स को भरती है।

[ALLOY]: Hermes Agent zero point sixteen हेडलाइन हार्नेस रिलीज़ है। ये प्रोजेक्ट के शुरू होने से अब तक की सबसे सतह क्षेत्र-विस्तार करने वाली रिलीज़ है, और केंद्रबिंदु एक असली नेटिव क्रॉस-प्लेटफॉर्म डेस्कटॉप ऐप है। ये टर्मिनल के चारों ओर रैपर नहीं है। ये URL से पिन किया गया ब्राउज़र टैब नहीं है। ये एक इंस्टॉलर है जो डॉक या टास्कबार पर एक असली चैट विंडो लाता है।

[NOVA]: Codex zero point one thirty seven OpenAI CLI रिलीज़ है, और सबसे आर्किटेक्चरली मतलबबहुत बदलाव है मल्टी-एजेंट v2 के साथ रनटाइम चॉइस पर्सिस्टेंस। आर्किटेक्चर डिटेल मायने रखती है। अब हर spawned थ्रेड अपना खुद का रनटाइम चॉइस आगे ले जाती है। Spawned एजेंट्स को साफ़ फॉलो-अप और मेटाडेटा डिफ़ॉल्ट्स मिलते हैं। ये उन बग्स के एक क्लास को बंद करता है जहाँ पैरेंट सेशन चाइल्ड को हैंडऑफ करता है और चाइल्ड चुपचाप कॉन्टेक्स्ट ड्रॉप कर देता है।

[ALLOY]: Claude Code two point one point one sixty six एक fallbackModel सेटिंग और glob टूल-नेम डेनी रूल्स जोड़ता है। फ़ॉलबैक चेन ऑपरेटर-फेसिंग फीचर है। प्रायोरिटी ऑर्डर में तीन मॉडल्स तक कॉन्फ़िगर करें और रनटाइम जब प्राइमरी ओवरलोडेड हो तो अगला चुन ले। Glob डेनी रूल्स आपको एक सिंगल रूल लिखने देते हैं जो सभी टूल्स से मैच करता है, या एक पैटर्न जो सबसेट से मैच करता है।

[NOVA]: मॉडल लेन है Gemma 4 12B, एक 12 बिलियन पैरामीटर encoder-free मल्टीमॉडल मॉडल 256K कॉन्टेक्स्ट विंडो के साथ, Google ने 3 जून 2026 को Apache 2.0 के तहत रिलीज़ किया। आर्किटेक्चर डिटेल ही स्टोरी है। विज़न और ऑडियो सीधे लैंग्वेज मॉडल बैकबोन में जाते हैं, न कि अलग मल्टीमॉडल एनकोडर से होकर — यही डिज़ाइन चॉइस है जो 12 बिलियन पैरामीटर मॉडल को 16 गीगाबाइट VRAM पर मल्टीमॉडल इनपुट हैंडल करने देती है।

[ALLOY]: प्रोजेक्ट रडार में तीन आइटम हैं। A2A Protocol v1.0 Linux Foundation के तहत एजेंट इंटरऑपरेबिलिटी लेयर के रूप में एक औपचारिक माइलस्टोन पर पहुँचता है, जिसमें डिस्कवरी के लिए एजेंट कार्ड्स और JSON-RPC 2.0 टास्क स्टेट मशीन। Kimi Code CLI एक TypeScript-native टर्मिनल कोडिंग एजेंट है जिसमें नेटिव MCP सपोर्ट और सबएजेंट पैरलल डिस्पैच है। Awesome-ai-agents-2026 curated इंडेक्स है जो MCP सर्वर्स, एजेंट फ्रेमवर्क्स, और प्रोटोकॉल्स को एजेंट स्टैक के लिए सतह पर लाता है।

[NOVA]: इस एपिसोड में एक सूत्र है - सरफेस एरिया। हैरनेस लेयर नेटिव, मल्टी-सरफेस टूल्स के आसपास कंसोलिडेट हो रहा है। मॉडल लेयर लोकल-फर्स्ट वर्कफ्लो के लिए ओपन-वेट ऑप्शन जोड़ रहा है। प्रोजेक्ट रडार वो कनेक्टिविटी लेयर है जो उन टूल्स को एक दूसरे से बात करने देती है। ...

[NOVA]: Hermes Agent zero point sixteen वो रिलीज है जो बदल देती है कि Hermes डेवलपर से कैसे मिलती है। हेडलाइन एक असली नेटिव Electron डेस्कटॉप ऐप्लिकेशन है जो बाकी सारे macOS, Linux या Windows ऐप्स की तरह इंस्टॉल होती है, खुद अपने अंदर से अपडेट होती है, और तुम्हें स्ट्रीमिंग के साथ एक प्रॉपर चैट विंडो देती है, सेशन लिस्ट, ड्रैग-एंड-ड्रॉप फाइल इनपुट, क्लिपबोर्ड इमेज पेस्ट, Cmd+K कमांड पैलेट, और स्टेटस बार में सीधे एक मॉडल पिकर।

[ALLOY]: अगर तुम गैर-तकनीकी साथियों से कह रहे थे "ये एक कमांड लाइन एजेंट है" और उनकी आंखें खाली हो रही थीं, तो अब तुम उन्हें बस एक इंस्टॉलर भेज सकते हो। डेस्कटॉप ऐप वैसे ही व्यवहार करता है जैसे वो टूल जो वो अपने ऐप्लिकेशन फोल्डर में ढूंढने की उम्मीद करते हैं। चैट विंडो रिस्पॉन्स स्ट्रीम करती है। सेशन लिस्ट आर्काइव और सर्च करती है। चैट एरिया में फाइल ड्रैग और ड्रॉप करो और फाइल अगले मैसेज से अटैच हो जाती है। क्लिपबोर्ड से इमेज पेस्ट करो और वो उसी अटैचमेंट पाइपलाइन में जाती है।

[NOVA]: डेस्कटॉप ऐप को लोकली Hermes चलाने की जरूरत नहीं है। इसे रिमोट Hermes गेटवे की तरफ पॉइंट करो - तुम्हारा होमलैब, होस्टेड बॉक्स, किसी साथी का सर्वर - और ऐप सिक्योर WebSocket से कनेक्ट होता है, OAuth या यूजरनेम और पासवर्ड से ऑथेंटिकेट करके। इनसिक्योर फ्लैग्स या हैंड-कॉपिड सेशन टोकन के साथ छेड़छाड़ नहीं। हर प्रोफाइल अपना खुद का रिमोट होस्ट टारगेट कर सकती है, और तुम एक साथ कई प्रोफाइल्स में कंकरेंट सेशन चला सकते हो।

[ALLOY]: ये वो रिमोट-कनेक्ट स्टोरी है जिसका एंटरप्राइज और टीम Hermes डिप्लॉयमेंट इंतजार कर रहे थे। डेस्कटॉप ऐप एक शेयर्ड गेटवे का थिन क्लाइंट बन जाता है, जिसका मतलब है कि एक टीम होस्टेड Hermes इंस्टेंस चला सकती है और हर डेवलपर अपना खुद का नेटिव GUI चलाता है। ऑथेंटिकेशन फ्लो OAuth यूज़ करता है, इसलिए आइडेंटिटी उस प्रोवाइडर को दिलीगेट की जाती है जो टीम पहले से चलाती है। यूजरनेम और पासवर्ड उन एनवायरनमेंट के लिए फॉलबैक है जिनमें OAuth प्रोवाइडर नहीं है।

[NOVA]: वेब डैशबोर्ड एक पूर्ण ब्राउजर-बेस्ड एडमिनिस्ट्रेशन पैनल बना। तुम्हें MCP कैटलॉग मैनेजमेंट, मैसेजिंग चैनल कॉन्फ़िगरेशन, क्रेडेंशियल स्टोरेज, वेबहुक मैनेजमेंट, मेमोरी कॉन्फ़िगरेशन, और प्लगेबल OIDC या यूजरनेम-पासवर्ड लॉगिन मिलते हैं - सब कुछ ब्राउजर से बिना कमांड लाइन छुए। फर्स्ट-टाइम सेटअप में अब "Quick Setup via Nous Portal" पाथ है जो तुम्हें सेकंडों में इंस्टॉल से पहले मैसेज तक ले जाता है, जो नए यूजर्स को ऑनबोर्ड करने या फ्रेश एनवायरनमेंट में Hermes को इवैल्यूएट करने के लिए मायने रखता है।

[ALLOY]: डिफॉल्ट स्किल सेट को ट्रिम किया गया जो तुम्हें सच में चाहिए। NVIDIA स्किल्स ट्रस्टेड Skills Hub टैप्स में शामिल हुईं। मॉडल पिकर अब हर जगह फज़ी-सर्चेबल है - डेस्कटॉप, वेब, TUI, और कमांड लाइन - जो तुच्छ लगता है जब तक कि तुम्हारे पास मॉडल्स की लंबी लिस्ट न हो और कोई सर्च न हो। अनडू आखिरकार लास्ट N टर्न्स को वापस लेने देता है, जो वो क्वालिटी-ऑफ-लाइफ फीचर है जो यूजर्स पहली रिलीज से मांग रहे थे।

[NOVA]: कैप में, दो प्रायोरिटी जीरो और 62 प्रायोरिटी वन बग क्लोज़र सवार हैं। सिक्योरिटी राउंड अलग से नोट करने योग्य है। एक Starlette डिपेंडेंसी फिक्स्ड वर्जन पर पिन की गई, सर्वर-साइड रिक्वेस्ट फोर्जरी ऑफ-लूप हार्डनिंग प्लगइन और प्रोवाइडर रिक्वेस्ट पाथ में हमलों का एक क्लास क्लोज़ करती है, और सबप्रोसेस क्रेडेंशियल स्ट्रिपिंग सुनिश्चित करती है कि क्रेडेंशियल चाइल्ड प्रोसेस एनवायरनमेंट में लीक न हों।

[ALLOY]: प्रैक्टिकल सिग्नल ये है कि Hermes अभी वो ऐप्लिकेशन बन गया जिसे तुम्हारे गैर-तकनीकी साथी असल में यूज़ करेंगे। नेटिव इंस्टॉलर एडॉप्शन के लिए सबसे बड़े एकल फ्रिक्शन पॉइंट को हटाता है। OAuth रिमोट कनेक्ट दूसरा फ्रिक्शन पॉइंट हटाता है, जो ये जरूरत थी कि सबको अपने मशीन पर Hermes न चलाना पड़े। वेब एडमिन पैनल तीसरा फ्रिक्शन पॉइंट हटाता है, जो ये था कि हर ऑपरेटर को कमांड लाइन कॉन्फ़िगरेशन सरफेस सिखाना पड़े।

[NOVA]: एजेंट स्टैक के लिए, आर्किटेक्चरल टेकअवे ये है कि सरफेस एरिया अब डेस्कटॉप-क्लास है। स्ट्रीमिंग के साथ एक असली चैट विंडो। आर्काइव के साथ असली सेशन लिस्ट। असली ड्रैग और ड्रॉप। असली OAuth फ्लो। Electron रैपर पैटर्न नया नहीं है, लेकिन थिन-क्लाइंट प्रोफाइल मॉडल के साथ मल्टी-एजेंट गेटवे पर इसे अप्लाई करना एक मीनिंगफुल स्टेप है। डेस्कटॉप ऐप हर डेवलपर मशीन पर इंस्टॉल किया जा सकता है और शेयर्ड गेटवे की तरफ पॉइंट किया जा सकता है, जो वो डिप्लॉयमेंट मॉडल है जिसके लिए एंटरप्राइज टीमें मांग कर रही थीं। ...

[ALLOY]: OpenAI Codex zero point one thirty seven को 4 जून, 2026 को latest stable command line tag के रूप में रिलीज़ किया गया, जो EP063 baseline of zero point one thirty five से दो releases पीछे है। सबसे बड़ा architecturally significant change है multi-agent v2 with runtime choice persistence. अब हर spawned thread अपना runtime choice आगे ले जाती है। Spawned agents को cleaner follow-up और metadata defaults मिलते हैं। इसका मतलब है कि जब कोई parent Codex session कोई child agent spawn करती है, तो child parent session के hand off होने पर अपना place नहीं खोता।

[NOVA]: Runtime choice persistence ही वो detail है जो matter करती है। इस release से पहले, parent session अपने लिए runtime set करता था, child spawn करता था, और child default runtime या parent के last used runtime पर fallback कर जाता था। इस release के बाद, child thread अपना own runtime choice forward ले जाती है और cleaner follow-up defaults पाती है। Hand-off semantics अब process-scoped की जगह thread-scoped हैं।

[ALLOY]: Function keys 13 से 24 अब TUI में supported हैं, और searchable menus में paste सुविधा से extended keyboard layouts use करने वाले power users का terminal experience बेहतर हुआ है। Enterprise और admin flows अब monthly credit limits show करते हैं और cloud-managed config bundles apply कर सकते हैं जिनमें education workspaces शामिल हैं। Credit limit visibility एक gap fill करती है जहाँ operators bill आने तक spend नहीं देख पाते थे।

[NOVA]: Plugin workflows में machine-readable output और cached remote catalog suggestions जुड़ गए हैं। Machine-readable output का मतलब है कि आप plugin lists को scripts, continuous integration pipelines, या fleet management tooling में pipe कर सकते हैं बिना human-readable text parse किए। Cached remote catalog suggestions plugin discovery flow को speed up करते हैं repeated network calls से बचकर।

[ALLOY]: Hosted web और image tools अब ज़्यादा code-mode flows में available हैं, standalone web searches अब parallel में run कर सकते हैं। Parallel standalone web search का मतलब है कि Codex multiple search queries एक साथ fire कर सकती है और results synthesize कर सकती है sequential run करने की जगह। यह research-heavy workflows के लिए real latency win है जहाँ एक turn पहले five या six search results पर depend करता था जिन्हें one at a time request करना पड़ता था।

[NOVA]: Permission requests और approvals अब environment identity carry करते हैं, जो एक gap fill करती है जहाँ एक context में granted permission गलती से दूसरे context boundaries में apply हो सकता था। Platform reliability macOS app launches और Windows SQLite startup, thread resume, और sandbox setup refreshes के लिए improved हुई है।

[ALLOY]: Architectural takeaway यह है कि Codex में multi-agent orchestration अब first-class surface बन गया है। Runtime choice persistence marketing sense में कोई feature नहीं है। यह एक correctness change है। कोई child thread जो अपना runtime choice खो देता है वह output produce कर सकता है जो parent's intent से match नहीं करता, model load करने में fail हो सकता है, या silently किसी default पर fallback हो सकता है जिसे operator ने authorize नहीं किया था। Thread-scoped runtime choice उस gap को close करता है।

[NOVA]: Enterprise controls architecture change के साथ ही land करते हैं, जो एक deliberate pairing है। Monthly credit limit visibility admins को bill आने से पहले spend देखने देती है। Cloud-managed config bundles, जिनमें education workspaces शामिल हैं, किसी team को एक fleet में single configuration apply करने देते हैं। Operator signal यह है कि Codex "CLI tool with a model picker" से "fleet-managed agent runtime with credit accounting" की तरफ move कर रही है।

[ALLOY]: Production में Codex run करने वाली teams के लिए practical move है upgrade करना और एक multi-agent session run करना ताकि verify किया जा सके कि runtime choice spawn और resume में correctly persists करती है। New output format देखने के लिए machine-readable plugin list command run करें। Code-mode flow में parallel web search test करें। जिस भी enterprise या admin flow में आपकी access है उसमें new monthly credit limit display check करें।

[NOVA]: Key insight यह है कि multi-agent v2 वो feature है जो agent spawning को actually session boundaries के across hold together बनाता है। Runtime choice persistence glamorous नहीं है, लेकिन यही वो difference है एक agent के बीच जो hand-off में context hold करता है और एक ऐसे के बीच जो उसे drop करता है। Operator-visible win यह है कि Codex multi-agent sessions को अब spawn और resume operations में babysitting की ज़रूरत नहीं है।

[ALLOY]: Claude Code का npm latest अब दो point one point one sixty six और दो point one point one sixty seven है, दो point one point one sixty five के बाद। Version दो point one point one sixty six feature release है जिसमें दो operator-visible additions हैं। मुख्य बात यह है कि एक नया fallbackModel setting है जो आपको primary model overloaded या unavailable होने पर क्रम में तीन fallback models तक configure करने देता है।

[NOVA]: Fallback model flag अब interactive sessions पर भी लागू होता है, सिर्फ background ones पर नहीं। इसका मतलब है कि interactive terminal sessions भी primary saturate होने पर chain में अगले model पर automatically roll over कर सकते हैं। यह model unavailability को handle करने के तरीके को बदलता है। API capacity पर होने पर single prompt fail करने के बजाय, Claude Code automatically configured अगला model try करता है।

[ALLOY]: Deny rule tool-name positions में glob pattern support दूसरा feature है। Wildcard का उपयोग करके सभी tools deny करता है। Allow rules non-MCP globs को reject करते हैं, और deny rules में unknown tool names अब silently malformed rules accept करने के बजाय startup पर warn करते हैं। Unknown tool names के लिए startup warning operator-friendly improvement है। अब आपको startup पर पता चलता है कि deny rule misconfigured है rather than discovering it when the rule fails to fire।

[NOVA]: Version दो point one point one sixty seven pure bug fixes और reliability improvements है — hygiene wave जो feature releases के बीच release train को साफ रखता है। Fallback model chain operator-facing feature है जो model unavailability को handle करने के तरीके को बदलता है, और fleet compliance settings के साथ runtime interaction समझने योग्य है।

[ALLOY]: Fallback chain required minimum version और required maximum version fleet compliance settings के साथ cleanly interact करता है। Version gate agent को start होने से रोकता है अगर यह allowed range से बाहर है। Fallback chain primary unavailable होने पर अगला available model pick करता है। दो settings compose करते हैं: एक fleet version range pin कर सकती है और fallback chain define कर सकती है, और runtime दोनों enforce करता है।

[NOVA]: Architectural signal यह है कि Claude Code model availability को first-class operational concern treat कर रहा है। Fallback chain flaky API के लिए workaround नहीं है। यह एक configuration primitive है जो operator को multiple model providers में priority order define करने देता है। Runtime पहले primary try करता है, फिर second, फिर third, और user को response पर model name के अलावा कोई difference नहीं दिखता।

[ALLOY]: Glob deny rule security surface improvement है। Wildcard pattern के साथ एक rule हर tool को deny करता है। यह sandboxed environments के लिए useful primitive है जहां agent को कुछ भी access नहीं होना चाहिए, या incident response के दौरान temporary "lock the agent out" configuration के लिए। Allow rules non-MCP globs reject करना means कि misconfiguration जहां operator MCP और non-MCP tool names में glob try करता है startup पर caught होता है, first tool call पर नहीं।

[NOVA]: Agent stack के लिए practical move यह है कि अपने Claude Code config में preference के क्रम में two or three alternatives के साथ fallbackModel जोड़ें। Chain को test करें by temporarily primary model unavailable बनाकर और verify करके कि fallback correctly fire होता है। Full tool lockout test करने के लिए deny rule में wildcard का उपयोग करें। Verify करें कि deny rules में unknown tool names startup warnings produce करते हैं।

[ALLOY]: Key insight यह है कि Claude Code अब fallback models को chain कर सकता है ताकि saturating API आपके agent को completely न रोके। Priority order में up to three models configure करें और runtime primary overloaded होने पर अगला pick करता है। Operator को wrapper script, retry logic, या separate routing layer लिखने की ज़रूरत नहीं है। Runtime fallback contract को own करता है।

[NOVA]: Version cadence भी note करने योग्य है। Quick succession में दो releases — दो point one point one sixty six feature release के रूप में और दो point one point one sixty seven bug-fix polish के रूप में — hygiene wave है जो release train को साफ रखता है। Feature releases operator-visible changes land करते हैं। Bug-fix releases rough edges close करते हैं जो operator-visible changes expose करते हैं। Split changelog को readable और upgrade calculus को simple रखता है।

[NOVA]: Google ने 3 जून, 2026 को Gemma 4 12B को Apache 2.0 open-weight checkpoint के तौर पर रिलीज किया, जिसमें 256K context window है, जिसे डिज़ाइन किया गया है ताकि agentic multimodal intelligence को सीधे laptops पर local workflows के लिए लाया जा सके। मुख्य architectural decision है encoder-free multimodal input। Vision और audio सीधे language model backbone में जाते हैं, न कि किसी separate multimodal encoder के ज़रिए।

[ALLOY]: यह वही architectural pattern है जो large multimodal models को छोटे parameter counts में fit करता है। Encoder overhead हटाकर, 12 billion parameter model image और audio inputs को एक separate processing stage के बिना handle कर सकता है जो parameters और latency जोड़ता है। यही design choice है जो 16 gigabytes of VRAM को काफी बनाता है।

[NOVA]: Benchmark performance को advanced reasoning tasks पर Google's 26 billion parameter model के करीब बताया गया है, जो एक 12 billion parameter model को उन benchmarks पर दोगुने आकार के models के साथ competitive बनाता है जो agentic workflows के लिए मायने रखते हैं। Agentic workflow positioning स्पष्ट है। Autonomous data processing, visual insights, और webpage building को target use cases के तौर पर list किया गया है।

[ALLOY]: Google AI Edge local deployment का रास्ता प्रदान करता है laptop hardware पर 16 और 32 gigabyte VRAM configurations के साथ। AI Edge managed local deployment surface है जो model loading, runtime optimization, और device stack के साथ integration handle करता है। उन teams के लिए जो manual checkpoint pull के बजाय one-command install चाहते हैं, AI Edge entry point है।

[NOVA]: Agent stack के लिए, Gemma 4 12B consumer hardware पर local coding-agent use के लिए सबसे realistic open-weight 12 billion parameter model है। यह local-first agent workflows को बदल देता है जब model और weights आपकी machine पर रहते हैं। कोई API latency नहीं। कोई data आपके environment से बाहर नहीं जाता। कोई per-token cost नहीं।

[ALLOY]: 256K context window का मतलब है कि model large codebases या long documents को context chunking के बिना handle कर सकता है जो smaller-window models को चाहिए होता है। 256K window एक छोटे से medium-sized repository को एक single context में रखने के लिए काफी है, या एक long document plus conversation history plus tool call results।

[NOVA]: Architectural takeaway यह है कि encoder-free multimodal वह design pattern है जो एक 12 billion parameter model को वही करने देता है जो पुराने 26 billion parameter encoder-decoder models करते थे। Encoder stage हटाने से parameter count कम हो जाता है बिना multimodal capability की sacrifice के, क्योंकि language model backbone सीखता है vision और audio tokens को सीधे handle करना।

[ALLOY]: Trade-off यह है कि language model backbone को शुरू से ही multimodal data पर train करना होता है, जो एक meaningfully more expensive training pipeline है। फायदा यह है कि inference तेज़ है, model छोटा है, और deployment आसान है। Local agent stacks के लिए, inference speed और model size training cost से ज़्यादा मायने रखते हैं।

[NOVA]: Agent stack के लिए, practical move यह है कि Gemma 4 12B checkpoint को Hugging Face से pull करें और 16 gigabytes of VRAM वाले laptop पर LM Studio या Ollama के through run करें। एक coding task output को अपने current local model के against compare करें। 256K context को एक long codebase या document understanding task पर test करें। अगर आप one-command install पसंद करते हैं तो managed local deployment path के लिए Google AI Edge use करें।

[ALLOY]: Key insight यह है कि Gemma 4 12B पहला 12 billion class open-weight model है किसी major lab का जिसे Google कहता है कि यह आपके laptop पर run कर सकता है और फिर भी advanced reasoning कर सकता है। Encoder-free architecture वह trick है जो इसे 16 gigabytes of VRAM में fit करता है। 256K context window वह capability है जो इसे real codebases पर real coding tasks के लिए useful बनाती है।

[NOVA]: व्यापक संकेत यह है कि ओपन-वेट लोकल मॉडल और क्लोज़्ड-वेट API मॉडल के बीच का अंतर कम हो रहा है। एक 12 बिलियन पैरामीटर मॉडल जो एडवांस्ड रीज़निंग पर 26 बिलियन पैरामीटर मॉडल के करीब पहुंच रहा है, यह एक सार्थक डेटा पॉइंट है। लोकल-फर्स्ट एजेंट वर्कफ्लो अब कोई समझौता नहीं है। वे प्रोडक्शन वर्कलोड के लिए एक वास्तविक विकल्प हैं जो उपलब्ध हार्डवेयर पर 12 बिलियन पैरामीटर मॉडल फिट कर सकते हैं। ...

[ALLOY]: Moonshot AI ने 5 जून, 2026 को Kimi Code CLI को MIT-लाइसेंस वाले ओपन-सोर्स टर्मिनल AI कोडिंग एजेंट के रूप में जारी किया, जो TypeScript में लिखा गया है। यह प्रोजेक्ट पुराने kimi-cli का उत्तराधिकारी है और npm के ज़रिए या एक सिंगल इंस्टॉल स्क्रिप्ट से वितरित किया जाता है जिसे पहले से Node.js इंस्टॉल की ज़रूरत नहीं है। macOS या Linux पर एक सिंगल इंस्टॉल कमांड बाइनरी को आपके path पर रख देता है। Windows पर एक समकक्ष PowerShell कमांड वही काम करता है।

[NOVA]: Kimi Code CLI कोड पढ़ता और एडिट करता है, शेल कमांड चलाता है, फाइलें सर्च करता है, वेब पेज फेच करता है, और फीडबैक के आधार पर अपना अगला स्टेप चुनता है — यह स्टैंडर्ड कोडिंग एजेंट लूप है। बॉक्स के बाहर यह Moonshot AI के Kimi मॉडल के साथ काम करता है और इसे दूसरे कम्पैटिबल प्रोवाइडर के साथ कॉन्फ़िगर किया जा सकता है। फीडबैक-ड्रिवन एक्ज़ीक्यूशन मॉडल रीड-ओनली ऑपरेशंस को अपने आप चलाता है और फाइल एडिट या शेल कमांड पर कन्फर्मेशन मांगता है।

[ALLOY]: वह अप्रूवल फ्लो रिस्की एक्शन को डेवलपर के कंट्रोल में रखता है। रीड-ओनली ऑपरेशंस जैसे फाइलें सर्च करना और वेब पेज फेच करना बिना रुकावट के चलते हैं। राइट ऑपरेशंस जैसे फाइल एडिट करना या शेल कमांड चलाना कन्फर्मेशन मांगते हैं। एजेंट प्रपोज करता है, डेवलपर डिस्पोज़ करता है।

[NOVA]: उल्लेखनीय फीचर्स में मिलीसेकंड में तैयार होने वाला फास्ट TUI, वीडियो इनपुट चैट में स्क्रीन रिकॉर्डिंग ड्रॉप करने के लिए, mcp-config कमांड के ज़रिए AI-नेटिव MCP कॉन्फ़िगरेशन, पैरलल वर्क के लिए सबएजेंट — आइसोलेटेड कॉन्टेक्स्ट में coder, explore, और plan सबएजेंट — और टूल कॉल को गेट करने, ऑडिटिंग डिसीज़न, या नोटिफिकेशन ट्रिगर करने के लिए लाइफसाइकल हुक शामिल हैं।

[ALLOY]: mcp-config कमांड के ज़रिए MCP कॉन्फ़िगरेशन वह फीचर है जो इसे एजेंट स्टैक से जोड़ता है। आप CLI के अंदर से बिना बाहरी कॉन्फ़िगरेशन फाइलों के MCP सर्वर जोड़ और ऑथेंटिकेट कर सकते हैं। कॉन्फ़िगरेशन कन्वर्सेशनल है। आप एजेंट से सर्वर जोड़ने को कहते हैं, वह आपको ऑथेंटिकेशन के ज़रिए गाइड करता है, और सर्वर लाइव हो जाता है।

[NOVA]: पैरलल वर्क के लिए सबएजेंट वह फीचर है जो एक सिंगल CLI एजेंट जो कुछ कर सकता है उसे बदल देता है। Coder सबएजेंट कोड लिखते हैं। Explore सबएजेंट कोडबेस नेविगेट करते हैं। Plan सबएजेंट टास्क को डिकम्पोज़ करते हैं। हर एक आइसोलेटेड कॉन्टेक्स्ट में चलता है, जिसका मतलब है कि पैरलल वर्क मेन सेशन कॉन्टेक्स्ट को कंटैमिनेट नहीं करता।

[ALLOY]: लाइफसाइकल हुक ऑपरेटर-फेसिंग फीचर हैं। एक हुक टूल कॉल को गेट कर सकता है — एजेंट को शेल कमांड चलाने से पहले परमिशन मांगनी होगी। एक हुक डिसीज़न का ऑडिट कर सकता है — हर टूल कॉल एजेंट के रीज़निंग के साथ लॉग किया जाता है। एक हुक नोटिफिकेशन ट्रिगर कर सकता है — जब कोई स्पेसिफिक इवेंट होता है तो Slack मैसेज, ईमेल, या वेबहुक।

[NOVA]: वर्जन ज़ीरो पॉइंट इलेवन 5 जून, 2026 को पब्लिश हुआ। प्रोजेक्ट को GitHub पर 1,902 स्टार्स मिले हैं और डेवलपमेंट सक्रिय है। TypeScript-नेटिव आर्किटेक्चर ध्यान देने योग्य है। एजेंट TypeScript में लिखा गया है, एक सिंगल बाइनरी या npm पैकेज के रूप में वितरित किया गया है, और सीधे npm इकोसिस्टम के साथ इंटीग्रेट करता है।

[ALLOY]: आर्किटेक्चरल सिग्नल यह है कि TypeScript-नेटिव CLI कोडिंग एजेंट पैटर्न एक वास्तविक कैटेगरी है। Kimi Code CLI उन कुछ टूल्स में शामिल हो गया है जो TypeScript में लिखे गए हैं और बिना रनटाइम डिपेंडेंसी के एक सिंगल बाइनरी के रूप में इंस्टॉल किए जा सकते हैं। फायदा है फास्ट कोल्ड स्टार्ट, छोटा फुटप्रिंट, और आसान वितरण। कीमत यह है कि कुछ TypeScript इकोसिस्टम चॉइस बेक किए गए हैं।

[NOVA]: एजेंट स्टैक के लिए, व्यावहारिक कदम है Kimi Code CLI इंस्टॉल करना और वर्शन फ्लैग से वेरिफाई करना। इसे अपने Kimi API key या Moonshot AI OAuth से कनेक्ट करें। mcp-config कमांड के जरिए एक MCP सर्वर कॉन्फ़िगरेशन टेस्ट करें। कोडबेस टास्क के खिलाफ पैरलल में एक सबएजेंट रन करें। अपने मौजूदा CLI एजेंट के मुकाबले एक्जीक्यूशन क्वालिटी की तुलना करें।

[ALLOY]: मुख्य अंतर्दृष्टि यह है कि Kimi Code CLI वह TypeScript-नेटिव टर्मिनल कोडिंग एजेंट है जो स्टैक से गायब था। TypeScript में लिखा गया, एक सिंगल बाइनरी के रूप में डिस्ट्रिब्यूटेड, नेटिव MCP सपोर्ट और पैरलल वर्क के लिए सबएजेंट्स के साथ। फीडबैक-ड्रिवन एक्जीक्यूशन मॉडल जिसमें रिस्की ऑपरेशंस के लिए स्पष्ट अप्रूवल है, यह एक डिज़ाइन चॉइस है जो डेवलपर एर्गोनॉमिक्स के साथ फिट बैठता है जिसकी तरफ पूरे स्टैक का कन्वर्जेंस हो रहा है।

[NOVA]: व्यापक सिग्नल यह है कि CLI कोडिंग एजेंट स्पेस इकोसिस्टम के हिसाब से सेगमेंट हो रहा है। npm और Node.js इकोसिस्टम के लिए TypeScript-नेटिव एजेंट। डेटा साइंस और मशीन लर्निंग इकोसिस्टम के लिए Python-नेटिव एजेंट। सिस्टम्स प्रोग्रामिंग इकोसिस्टम के लिए Rust-नेटिव एजेंट। हर इकोसिस्टम को वह एजेंट मिलता है जो उसके मौजूदा टूलिंग और डिस्ट्रिब्यूशन मॉडल के अनुकूल हो।

[ALLOY]: एजेंट-टू-एजेंट प्रोटोकॉल 2026 में Linux Foundation के तहत v1.0 तक पहुंचा, जिसने विभिन्न फ्रेमवर्क से आने वाले एजेंट्स के बीच एक दूसरे को खोजने, कम्युनिकेशन चैनल स्थापित करने और टास्क डेलीगेट करने के तरीके के लिए एक औपचारिक स्पेसिफिकेशन बनाया। प्रोटोकॉल "एजेंट कार्ड्स" को परिभाषित करता है — JSON कैपेबिलिटी मैनिफेस्ट — एजेंट डिस्कवरी के लिए, और JSON-RPC 2.0 का उपयोग करके लॉन्ग-रनिंग इंटरैक्शन्स के लिए टास्क-बेस्ड स्टेट मशीन।

[NOVA]: शुरू में Google द्वारा लॉन्च किया गया, A2A अब Linux Foundation द्वारा MCP के साथ गवर्न किया जाता है। MCP बनाम A2A का अंतर मुख्य मेंटल मॉडल है। MCP मानकीकृत करता है कि एक एजेंट बाहरी टूल्स, डेटाबेस और डेटा सोर्सेस से कैसे कनेक्ट होता है — यह इस बारे में है कि एक एजेंट क्या कर सकता है। A2A मानकीकृत करता है कि एजेंट एक दूसरे से कैसे कम्युनिकेट करते हैं — यह इस बारे में है कि एजेंट कैसे मिलकर काम करते हैं।

[ALLOY]: MCP पहले से ही एजेंट स्टैक में व्यापक रूप से अपनाया गया है। A2A v1.0 पूरक प्रोटोकॉल है जो क्रॉस-फ्रेमवर्क एजेंट हैंडऑफ को इस तरह सक्षम करेगा कि हर जोड़ी के लिए कस्टम इंटीग्रेशन कोड की जरूरत न हो। बिल्डर्स के लिए यह अंतर महत्वपूर्ण है। अगर आप एक एजेंट को डेटाबेस से वायर कर रहे हैं, तो आप MCP का उपयोग कर रहे हैं। अगर आप दो एजेंट्स को एक दूसरे से बात करने के लिए वायर कर रहे हैं, तो आप A2A का उपयोग कर रहे हैं।

[NOVA]: एक एजेंट कार्ड एक JSON मैनिफेस्ट है जो बताता है कि एक एजेंट क्या कर सकता है। कार्ड में एजेंट की पहचान, उसकी क्षमताएं, वे प्रोटोकॉल जो वह बोलता है, वे ऑथेंटिकेशन मैकेनिज्म जो वह सपोर्ट करता है, और वे टास्क टाइप्स जो वह स्वीकार करता है, शामिल होते हैं। जब एक एजेंट दूसरे को काम सौंपना चाहता है, तो वह टारगेट एजेंट का कार्ड खोजता है और कम्युनिकेट कैसे करें यह समझने के लिए कार्ड का उपयोग करता है।

[ALLOY]: टास्क स्टेट मशीन प्रोटोकॉल का दूसरा आधा हिस्सा है। एक लॉन्ग-रनिंग टास्क की एक परिभाषित लाइफसाइकल होती है: सबमिटेड, वर्किंग, इनपुट-रिक्वायर्ड, कम्प्लीटेड, फेल्ड, कैंसल्ड। स्टेट मशीन परिभाषित करती है कि हर स्टेट का क्या मतलब है, कौन से ट्रांज़िशन वैध हैं, और हर ट्रांज़िशन पर एजेंट्स क्या डेटा एक्सचेंज करते हैं। स्टेट मशीन वह है जो मल्टी-एजेंट वर्कफ्लो को पार्शियल फेलियर के प्रति रोबस्ट बनाती है।

[NOVA]: a2aproject/A2A रिपॉजिटरी में 24,153 GitHub स्टार्स हैं और जून 6, 2026 तक सक्रिय डेवलपमेंट है। एजेंट स्टैक के लिए, A2A v1.0 वह इंटरऑपरेबिलिटी लेयर है जो एक Claude Code सेशन को Hermes एजेंट को डेलीगेट करने देगा, या एक OpenClaw एजेंट को Codex थ्रेड में हैंडऑफ करने देगा, बिना हर जोड़ी के लिए कस्टम इंटीग्रेशन बनाए।

[ALLOY]: आर्किटेक्चरल सिग्नल यह है कि v1.0 फॉर्मलाइजेशन का मतलब है कि प्रोटोकॉल स्थिर है। बिल्डर्स A2A को अपना सकते हैं बिना यह चिंता के कि अगला रिलीज उनके इंटीग्रेशन को तोड़ देगा। Linux Foundation गवर्नेंस वेंडर न्यूट्रैलिटी की एक लेयर जोड़ता है जो एंटरप्राइज एडॉप्शन को आसान बनाता है — कोई एकल कंपनी प्रोटोकॉल दिशा को नियंत्रित नहीं करती।

[NOVA]: प्रोटोकॉल अब पर्याप्त परिपक्व हो गया है कि बिल्डर्स को मल्टी-एजेंट वर्कफ़्लो डिज़ाइन करते समय इसके बारे में जानकारी होनी चाहिए। अगर आप एक वर्कफ़्लो बना रहे हैं जिसमें एक से अधिक एजेंट रनटाइम शामिल हैं, तो सवाल अब यह नहीं है कि "क्या हम A2A का उपयोग करें" बल्कि "प्रत्येक रनटाइम A2A का कौन सा संस्करण बोलता है।"

[ALLOY]: एजेंट स्टैक के लिए, व्यावहारिक कदम है A2A v1.0 स्पेसिफिकेशन को a2aproject/A2A GitHub रेपो पर पढ़ना ताकि एजेंट कार्ड स्ट्रक्चर और टास्क स्टेट मशीन सेमांटिक्स को समझा जा सके। अगर आप एक मल्टी-एजेंट वर्कफ़्लो बना रहे हैं, तो A2A एजेंट कार्ड्स को ध्यान में रखकर एजेंट हैंडऑफ पॉइंट्स डिज़ाइन करें। अगर आपके पास दो अलग-अलग एजेंट रनटाइम उपलब्ध हैं तो एक क्रॉस-फ्रेमवर्क एजेंट डेलीगेशन टेस्ट करें।

[NOVA]: मुख्य अंतर्दृष्टि यह है कि A2A v1.0 वह प्रोटोकॉल है जो एजेंट इंटरऑपरेबिलिटी को असली बनाता है। अलग-अलग फ्रेमवर्क के एजेंट अब एक-दूसरे को खोज सकते हैं और कस्टम ग्लू कोड के बजाय एक औपचारिक JSON-RPC 2.0 स्टेट मशीन के ज़रिए काम सौंप सकते हैं। प्रोटोकॉल की परिपक्वता यह संकेत है कि मल्टी-एजेंट इकोसिस्टम बेस्पोक इंटीग्रेशन से आगे बढ़ने के लिए तैयार है।

[ALLOY]: व्यापक संकेत यह है कि एजेंट स्टैक का प्रोटोकॉल लेयर वेब के प्रोटोकॉल लेयर जैसा दिखने लगा है। ट्रांसपोर्ट के लिए HTTP। मैसेज फॉर्मेट के लिए JSON-RPC। डिस्कवरी के लिए एजेंट कार्ड्स। लॉन्ग-रनिंग इंटरैक्शन्स के लिए टास्क स्टेट मशीन्स। प्रोटोकॉल सरल, कंपोजेबल और वेंडर-न्यूट्रल हैं। यही डिज़ाइन पैटर्न है जो इकोसिस्टम को बढ़ने देता है।

[NOVA]: A2A को इंटर-एजेंट कम्युनिकेशन के लिए और MCP को टूल इंटीग्रेशन के लिए इस्तेमाल करने का कॉम्बिनेशन वह प्रोटोकॉल स्टैक है जिसकी ओर एजेंट इकोसिस्टम कन्वर्ज कर रहा है। दोनों प्रोटोकॉल अलग-अलग समस्याएं हल करते हैं और वे साफ़-साफ़ कंपोज होते हैं। एक एजेंट जो A2A बोलता है वह दूसरे एजेंट्स को खोज और डेलीगेट कर सकता है। एक एजेंट जो MCP बोलता है वह बाहरी टूल्स से कनेक्ट हो सकता है। एक एजेंट जो दोनों बोलता है वह दोनों कर सकता है। ...

[ALLOY]: व्यावहारिक कतार वह है जो सुनने से कार्य करने की ओर ले जाती है। Hermes Agent के लिए, अपने ऑपरेटिंग सिस्टम के लिए डेस्कटॉप ऐप इंस्टॉलर डाउनलोड करें और इसे अपने मौजूदा लोकल या रिमोट गेटवे के खिलाफ़ चलाएं। अगर आपके पास होस्टेड Hermes है तो रिमोट गेटवे के खिलाफ़ OAuth लॉगिन टेस्ट करें। MCP सर्वर्स, मैसेजिंग चैनल्स और क्रेडेंशियल्स को ऑडिट करने के लिए नए वेब एडमिन पैनल को एक्सप्लोर करें। नए फर्स्ट-रन एक्सपीरियंस की तुलना करने के लिए फ्रेश इंस्टॉल पर Nous Portal के ज़रिए क्विक सेटअप चलाएं।

[NOVA]: Codex के लिए, ज़ीरो पॉइंट वन थर्टी सेवन पर अपग्रेड करें और एक मल्टी-एजेंट सेशन टेस्ट करें ताकि यह सत्यापित हो सके कि रनटाइम चॉइस स्पॉन और रिज्यूम साइकल में सही तरीके से पर्सिस्ट करती है। आउटपुट फॉर्मेट देखने के लिए मशीन-रेडेबल प्लगइन लिस्ट कमांड चलाएं। कोड-मोड फ्लो में पैरेलल वेब सर्च टेस्ट करें। जिन एंटरप्राइज़ या एडमिन फ्लो में आपकी पहुंच है उनमें नए मंथली क्रेडिट लिमिट डिस्प्ले को चेक करें।

[ALLOY]: Claude Code के लिए, अपने कॉन्फिग में प्रेफरेंस के हिसाब से क्रमबद्ध दो-तीन विकल्पों के साथ एक fallbackModel जोड़ें। अपने प्राइमरी मॉडल को अस्थायी रूप से unavailable बनाकर चेन को टेस्ट करें और सत्यापित करें कि फॉलबैक सही तरीके से फायर होती है। फुल टूल लॉकआउट टेस्ट करने के लिए deny रूल में वाइल्डकार्ड का उपयोग करें। सत्यापित करें कि deny रूल्स में अनजान टूल नेम्स स्टार्टअप वार्निंग्स देते हैं। लेटेस्ट बग फिक्सेस के लिए टू पॉइंट वन पॉइंट वन सिक्स सेवन पर अपग्रेड करें।

[NOVA]: Gemma 4 12B के लिए, Hugging Face से चेकपॉइंट पुल करें और इसे 16 गीगाबाइट्स VRAM वाले लैपटॉप पर LM Studio या Ollama के ज़रिए चलाएं। एक कोडिंग टास्क आउटपुट की तुलना अपने मौजूदा लोकल मॉडल से करें। लॉन्ग कोडबेस या डॉक्यूमेंट अंडरस्टैंडिंग टास्क पर 256K कॉन्टेक्स्ट टेस्ट करें। अगर आप एक-कमांड इंस्टॉल पसंद करते हैं तो Google AI Edge का उपयोग करें।

[ALLOY]: Kimi Code CLI के लिए, इंस्टॉल स्क्रिप्ट के साथ इंस्टॉल करें और वर्शन फ्लैग से सत्यापित करें। इसे अपने Kimi API की या Moonshot AI OAuth से कनेक्ट करें। mcp-config कमांड के ज़रिए एक MCP सर्वर कॉन्फिगरेशन टेस्ट करें। एक सबएजेंट को कोडबेस टास्क के खिलाफ़ पैरेलल में चलाएं और अपने मौजूदा CLI एजेंट के खिलाफ़ एक्जीक्यूशन क्वालिटी की तुलना करें।

[NOVA]: A2A Protocol के लिए, agent card structure और task state machine semantics को समझने के लिए a2aproject GitHub repo पर v1.0 specification पढ़ें। अगर आप multi-agent workflow बना रहे हैं, तो A2A agent cards को ध्यान में रखते हुए agent handoff points डिज़ाइन करें। अगर आपके पास दो अलग-अलग agent runtimes उपलब्ध हैं, तो एक cross-framework agent delegation को test करें।

[ALLOY]: awesome-ai-agents-2026 curated list के लिए, अपने stack से संबंधित एक नया server या protocol implementation खोजने के लिए MCP और A2A protocol sections को browse करें। यह list बार-बार अपडेट होती है और जब आप नए agent tooling का मूल्यांकन कर रहे होते हैं तो यह आगे क्या पढ़ना है इसके लिए definitive index है।

[NOVA]: आज के AgentStack Daily का मुख्य विषय surface area और connectivity है। Harness layer native, multi-surface tools के चारों ओर consolidate हो रहा है जिन्हें operators वास्तव में उपयोग करना चाहते हैं। Model layer local-first workflows के लिए open-weight options जोड़ रहा है। Protocol layer वह connective tissue है जो उन tools को एक-दूसरे से बात करने देती है। Agent stack कम mystical और ज्यादा operational हो रही है, और यह बिल्कुल वही है जो उसे production tool बनने के लिए चाहिए, research demo नहीं।

[ALLOY]: हम जल्द ही वापस आएंगे।

[NOVA]: आज के AgentStack Daily के show notes Toby On Fitness Tech dot com पर मिलेंगे। वहां आपको timestamps, उन releases और tools के links मिलेंगे जिन्हें हमने cover किया, और गहरी technical context जो spoken audio में fit नहीं हुई।

[NOVA]: यह AgentStack Daily है। मैं NOVA हूं। सुनने के लिए धन्यवाद।