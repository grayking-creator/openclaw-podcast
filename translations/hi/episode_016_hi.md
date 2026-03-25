## [00:00-02:30] OpenClaw अपनी पुरानी खाल उतारता है

NOVA: मैं NOVA हूं, यह OpenClaw Daily है, और आज हमारे पास उन रिलीज़ में से एक है जहां version numbers तो साफ-सुथरे दिखते हैं, लेकिन अंदर की असली कहानी उलझी हुई, असरदार, और सच कहूं तो काफ़ी दिलचस्प है। [PAUSE] इस हफ्ते, दो bugs ने एक असली power-user setup को इतनी ज़ोर से मारा कि वे आपको लगभग सब कुछ बता देते हैं कि OpenClaw इस समय कहां खड़ा है।

ALLOY: हां। ये कोई छोटे-मोटे cute edge cases नहीं थे। ये उस तरह के bugs थे जो आपको अपने ही setup पर शक करा दें, क्योंकि जो आप देखते हैं, system वास्तव में वही नहीं कर रहा होता।

NOVA: Bug one: एक user ने [EMPHASIS]MiniMax[/EMPHASIS] को अपने reasoning model के रूप में configure किया हुआ था। Upstream API [EMPHASIS]api_error[/EMPHASIS] throw कर रही थी। OpenClaw ने उसे देखा, तय किया कि यह transient होगा, चुपचाप retry कर दिया, failure कभी surface नहीं किया, fallback को ठीक से trigger नहीं किया, और user को degraded result वापस मिला, बिना इस बात के कि original call fail हुई थी।

ALLOY: जो बेहद क्रूर है, क्योंकि सबसे ख़राब bugs वे होते हैं जो फटते नहीं हैं। वे बस चुपचाप बदतर होते जाते हैं। आपको लाल बत्ती नहीं मिलती। आपको सिर्फ़ हल्की हरी बत्ती मिलती है।

NOVA: बिल्कुल। और bug two दर्द की एक अलग किस्म थी, लेकिन उतनी ही असली। User एक fresh [EMPHASIS]OpenAI Codex[/EMPHASIS] token paste करता है, confirmation देखता है, सब कुछ successful लगता है, gateway restart करता है, और token वापस expired credential पर लौट चुका होता है।

ALLOY: वह वाला आपको पागल महसूस कराता है। क्योंकि user की नज़र से देखें तो उसने सही काम किया। उसने नया token paste किया। App ने कहा, हां, save हो गया। फिर restart के बाद, नहीं। पुराना ख़राब token फिर वापस। [PAUSE] अंदर की तरफ, gateway की in-memory auth state restart पर freshly saved disk value को overwrite कर रही थी।

NOVA: ये दोनों [EMPHASIS]v2026.3.23[/EMPHASIS] में ठीक किए गए हैं। लेकिन यह समझने के लिए कि ये हुए क्यों, आपको समझना होगा कि [EMPHASIS]v2026.3.22[/EMPHASIS] ने क्या बदला। क्योंकि .22 बड़ा वाला है। .22 वह है जहां OpenClaw ने शायद वह काम किया जो उसे एक साल पहले कर देना चाहिए था।

ALLOY: Legacy purge.

NOVA: Legacy purge. पुराने names, compatibility layers, अजीब transitional paths, browser relay crutches, plugin SDK mush — उसका बड़ा हिस्सा निकाल बाहर किया गया। [PAUSE] और मुझे लगता है कि इन दो releases को साथ में समझने का सही तरीका यह है: .22 पुरानी मृत खाल हटाता है, और .23 यह पक्का करता है कि नई खाल फटे नहीं।

ALLOY: यही पूरा episode है। अगर आप एक real install maintain कर रहे हैं, तो ये decorative updates नहीं हैं। ये structural हैं।

## [02:30-11:00] The Legacy Purge — v2026.3.22 के Breaking Changes

NOVA: चलिए सबसे emotionally charged change से शुरू करते हैं, क्योंकि लोग names से अजीब तरह से चिपक जाते हैं, तब भी जब उन names को बहुत पहले retire कर देना चाहिए था। [EMPHASIS]CLAWDBOT_*[/EMPHASIS] और [EMPHASIS]MOLTBOT_*[/EMPHASIS] environment names अब गए। Deprecated नहीं। Warning के साथ tolerate नहीं। गए।

ALLOY: और मैं इसे थोड़ा धीमा करके कहना चाहता हूं, क्योंकि अगर आप OpenClaw को सिर्फ़ एक laptop पर चलाते हैं और कहीं नहीं, तो आप यह सुनकर सोच सकते हैं, ठीक है, कुछ variables rename करने हैं, fine। असली failure mode यह नहीं है। असली failure mode यह है कि आपके पास Docker Compose में कोई पुरानी [EMPHASIS].env[/EMPHASIS] file है, या किसी VPS पर कोई जंग लगा [EMPHASIS]systemd[/EMPHASIS] unit, या shell profile में कुछ ऐसा है जिसे आपने आठ महीने से देखा नहीं। आप upgrade करते हैं, OpenClaw शुरू होता है, और वे values चुपचाप ignore हो जाती हैं।

NOVA: कोई error नहीं। कोई migration banner नहीं।

ALLOY: कोई यह नहीं कहता, "hey, मैंने [EMPHASIS]CLAWDBOT_TOKEN[/EMPHASIS] देखा और यह obsolete है।" बस config गायब। अचानक auth line up नहीं करता, state path वहां नहीं है जहां आपने सोचा था, शायद plugin load नहीं होता, शायद token गायब लगता है। [PAUSE] यह उसी तरह की breakage है जो सुबह दो बजे upgrade के बाद उस machine पर लगती है जिसे आपने काफी समय से छुआ भी नहीं।

NOVA: अपनी env files grep कीजिए। हर environment में जिसमें आप OpenClaw चलाते हैं। हर host। हर Compose file। हर startup unit। हर shell bootstrap। अगर आपके पास [EMPHASIS]CLAWDBOT_*[/EMPHASIS] या [EMPHASIS]MOLTBOT_*[/EMPHASIS] है, तो उसे ठीक होने तक broken मानिए।

ALLOY: पुरानी [EMPHASIS]~/.moltbot[/EMPHASIS] state directory के साथ भी यही कहानी है। वह path अब future का हिस्सा नहीं है। अगर आपकी state अभी भी वहीं रहती है, तो upgrade के बाद OpenClaw आपके लिए यह जादुई तरीके से infer नहीं करेगा। उसे [EMPHASIS]~/.openclaw[/EMPHASIS] में move कीजिए या [EMPHASIS]OPENCLAW_STATE_DIR[/EMPHASIS] को explicitly set कर दीजिए और काम ख़त्म कीजिए।

NOVA: और यह उन फैसलों में से एक है जहां मैं वास्तव में इस कठोरता से सहमत हूं। Transitional aliases short term में दयालु लगते हैं, लेकिन वे architecture को अपने बारे में झूठ बोलने पर मजबूर कर देते हैं। पुराने names को अब भी first-class होने का नाटक कराने की एक असली कीमत होती है।

ALLOY: मैं end state से सहमत हूं। मैं migration pain के बारे में लोगों की शांति से असहमत हूं। अगर आप वह व्यक्ति हैं जो पांच installs manage करता है और उनमें से दो अजीब हैं, तो यह कोई philosophical cleanup नहीं है। यह scavenger hunt है।

NOVA: ठीक बात। [PAUSE] .22 में दूसरा बड़ा breaking change यह है कि [EMPHASIS]ClawHub[/EMPHASIS] अब first-class है, और इसका practical मतलब marketing phrasing से कहीं बड़ा है। [EMPHASIS]openclaw plugins install name[/EMPHASIS] अब पहले ClawHub check करता है, और केवल तब npm पर fallback करता है जब ClawHub में package मौजूद न हो।

ALLOY: जिसका मतलब है कि install behavior बदल गया, भले ही आपने command नहीं बदली। यही बात लोगों को सुननी चाहिए। अगर आपके पास scripts हैं जो npm package resolution path assume करती हैं, और वही name अब ClawHub पर भी मौजूद है, तो संभव है कि आपको पहले ClawHub version मिले।

NOVA: अब native commands भी हैं: [EMPHASIS]openclaw skills search[/EMPHASIS], [EMPHASIS]openclaw skills install[/EMPHASIS], [EMPHASIS]openclaw skills update[/EMPHASIS]। [PAUSE] और मेरे लिए यह OpenClaw का आखिरकार product को उसके intended ecosystem के साथ align करना है। ClawHub हमेशा skills का घर होना चाहिए था। यह release उसे aspirational के बजाय real बना देती है।

ALLOY: यह साफ़ है, लेकिन अपनी automation test कीजिए। अगर आपके पास bootstrap scripts, dotfiles, onboarding docs हैं, तो पक्का कीजिए कि वे अभी भी वही install करते हैं जो आप समझते हैं कि वे करेंगे। बदलाव अच्छा है। Surprises अच्छे नहीं।

NOVA: तीसरा: [EMPHASIS]Plugin SDK[/EMPHASIS] overhaul। यह किनारों पर हल्का सा कुतरना नहीं है। [EMPHASIS]openclaw/extension-api[/EMPHASIS] चला गया। कोई compatibility shim नहीं है। नया surface है [EMPHASIS]openclaw/plugin-sdk/*[/EMPHASIS], narrower subpaths और कहीं ज्यादा साफ़ boundaries के साथ।

ALLOY: अगर आपके पास custom plugins हैं, तो यह एक real migration है। यह optional नहीं है। कोई fallback नहीं। आप यह नहीं कह सकते, "मैं बाद में update करूंगा।" बाद में मतलब broken।

NOVA: Bundled plugins को अब host-side operations के लिए injected runtime का इस्तेमाल करना होगा, और यह उन बदलावों में से एक है जो bureaucratic लगते हैं, जब तक आपको यह एहसास न हो कि यह बहुत सारा ambiguous privilege bleed हटा देता है। Host behavior explicit है। Runtime boundaries explicit हैं।

ALLOY: और message discovery भी बदली है। [EMPHASIS]describeMessageTool()[/EMPHASIS] अब required है। पुराना [EMPHASIS]listActions[/EMPHASIS], [EMPHASIS]getCapabilities[/EMPHASIS], [EMPHASIS]getToolSchema[/EMPHASIS] flow हटा दिया गया है। [PAUSE] यह rename नहीं है। यह contract change है।

NOVA: नया SDK सच में cleaner है। genuinely। Imports narrower हैं। Intent ज्यादा स्पष्ट है। Runtime model ज्यादा coherent है। लेकिन आपको migrate करना होगा। और अगर आप plugin developer हैं, तो [EMPHASIS]docs.openclaw.ai/plugins/sdk-migration[/EMPHASIS] पढ़िए। Memory के भरोसे improvise मत कीजिए।

ALLOY: मैं उस पर ज़ोर देना चाहता हूं। यह वह हफ्ता नहीं है जब आप vibes के भरोसे अपनी migration freehand करें।

NOVA: चौथा bucket: security hardening। इनमें से कुछ तब तक invisible रहते हैं जब तक वे आपको बचा न लें, इसलिए इन्हें उतना airtime नहीं मिलेगा, लेकिन ये मायने रखते हैं। Exec sandbox अब [EMPHASIS]MAVEN_OPTS[/EMPHASIS], [EMPHASIS]SBT_OPTS[/EMPHASIS], [EMPHASIS]GRADLE_OPTS[/EMPHASIS], [EMPHASIS]ANT_OPTS[/EMPHASIS], साथ ही [EMPHASIS]GLIBC_TUNABLES[/EMPHASIS] और [EMPHASIS]DOTNET_ADDITIONAL_DEPS[/EMPHASIS] को block करता है। [PAUSE] यह मूल रूप से उन runtime injection surfaces के खिलाफ एक sweep है जिन्हें लोग भूल जाते हैं कि वे वहां हैं।

ALLOY: सही। ये env vars वही चीजें हैं जिन्हें attackers पसंद करते हैं और operators भूल जाते हैं। अगर आपका tool sandbox कहता है, "हम control कर रहे हैं कि क्या चलेगा," लेकिन आप अभी भी build tool या runtime injection variables को अंदर घुसने दे रहे हैं, तो आप सच में बहुत कम control कर रहे हैं।

NOVA: एक subtle लेकिन smart allowlist change भी है: [EMPHASIS]time[/EMPHASIS] अब allowlist evaluation में transparent है। तो [EMPHASIS]time ./approved-script[/EMPHASIS] अब [EMPHASIS]time[/EMPHASIS] wrapper नहीं, बल्कि अंदर की script से bind करता है।

ALLOY: वह बहुत practical है। लोग debugging के दौरान commands को [EMPHASIS]time[/EMPHASIS] में हर समय wrap करते हैं। पहले wrappers अजीब policy edge cases बना सकते थे। अब यह उसी चीज़ को evaluate करता है जिसे आप वास्तव में चलाना चाहते थे।

NOVA: और voice webhook hardening भी कड़ी हुई है: body read करने से पहले missing provider signatures reject करो, [EMPHASIS]64KB[/EMPHASIS] और [EMPHASIS]5s[/EMPHASIS] pre-auth limit के साथ। यह बस sound perimeter hygiene है। Unauthenticated junk को parse करने में resources मत खर्च करो।

ALLOY: आखिर में, वे quiet fixes जो मायने रखती हैं: Discord slash commands। Carbon reconcile अब default है, इसलिए gateway restarts अब local deploy path के ज़रिए slash commands churn नहीं करते।

NOVA: मुझे इस class की fix बहुत पसंद है क्योंकि users इसे कम ghosts के रूप में experience करते हैं।

ALLOY: हां। शांत लेकिन असली। Restarts ghost commands generate कर रहे थे। अब नहीं करते। यह glamorous नहीं है, लेकिन यह ठीक उसी तरह का paper cut है जो platform को amateur महसूस कराता है अगर आप उसे unfixed छोड़ दें।

NOVA: तो .22 को एक वाक्य में कहें तो: OpenClaw ने legacy को harmless मानने का नाटक बंद कर दिया।

ALLOY: और अगर आपने कुछ समय से अपना setup छुआ नहीं है, तो .22 वह release है जो यह आपके लिए पता कर लेगी।

NOVA: मुझे यह भी लगता है कि यह release compatibility और clutter के बीच एक रेखा खींचती है। काफ़ी समय तक OpenClaw पुराने names, पुराने install assumptions, पुराने plugin discovery shapes, और पुराने browser pathways को इसलिए ढो रहा था क्योंकि उन्हें हटाना risky लगता था। [PAUSE] लेकिन उन्हें वहीं रखना भी risky था। इससे platform को समझना और कठिन हो रहा था।

ALLOY: यही trade-off लोग miss कर देते हैं। Backward compatibility सिर्फ़ function preserve नहीं करती। यह confusion भी preserve करती है। हर alias, हर पुराना path, हर "हम अब भी इसे accept करते हैं" branch support के लिए याद रखने की एक और चीज़ बन जाता है और operators के फंसने की एक और जगह।

NOVA: और जब आप ClawHub, modern plugin SDK, और current naming के इर्द-गिर्द centralize कर लेते हैं, तो documentation आखिरकार दो timelines में बोलना बंद कर सकती है।

ALLOY: जो लोगों के सोचने से कहीं ज़्यादा मायने रखता है। Operational pain का आधा हिस्सा bug नहीं होता। वह यह एहसास होता है कि जो भी guide आप पढ़ रहे हैं, वह product की किसी दूसरी generation के लिए हो सकती है।

NOVA: तो अगर .22 harsh लगती है, तो इसलिए कि वह एक reality चुन रही है।

ALLOY: हां। एक reality, कम aliases, कम relics। Short-term pain, long-term sanity।

## [11:00-17:00] Chrome MCP: Extension मर चुका है

NOVA: हमें browser tooling पर ठीक से समय देना होगा, क्योंकि बहुत से users के लिए यह इन दो releases में सबसे बड़ा operational change है। Legacy Chrome extension relay चला गया। [EMPHASIS]driver: "extension"[/EMPHASIS], bundled extension assets, [EMPHASIS]browser.relayBindHost[/EMPHASIS] — सब हटाए गए।

ALLOY: और अगर आप उस दौर में नहीं थे, तो extension असल में था क्या, यह समझिए। OpenClaw पहले एक Chrome extension ship करता था जो [EMPHASIS]CDP[/EMPHASIS], यानी Chrome DevTools Protocol, के लिए relay की तरह काम करता था। आप extension manually install करते थे, browser permissions grant करते थे, और वह OpenClaw और browser के बीच bridge का काम करता था।

NOVA: जो हमेशा थोड़ा improvised लगता था।

ALLOY: वह improvised था। उपयोगी, लेकिन improvised। वह काम करता था क्योंकि browser control messy है और extension आपको ऐसा path देता था जो सबको direct attach समझाने से आसान था। लेकिन इसके साथ extension वाली सारी baggage भी आती थी: install friction, permissions की अजीबियां, compatibility drift, browser profile quirks, और diagnose करने के लिए एक और moving part जब चीज़ें बिगड़तीं।

NOVA: Replacement model बस बेहतर है। OpenClaw अब standard CDP mechanisms का उपयोग करके एक running Chrome instance या user profile से direct attach करता है। Extension की ज़रूरत नहीं। बीच में कोई custom relay नहीं। [PAUSE] Architectural नज़र से यह साफ़ है। कम bespoke layers। Tooling में छिपे कम secrets।

ALLOY: लेकिन — और यही महत्वपूर्ण practical warning है — अगर आप upgrade करने से पहले, या कम से कम उसके तुरंत बाद, [EMPHASIS]openclaw doctor --fix[/EMPHASIS] नहीं चलाते, तो आपका browser automation पूरी तरह टूट सकता है। और यह हमेशा obvious तरीके से नहीं टूटेगा। ज़रूरी नहीं कि आपको कोई friendly message मिले जो कहे, "extension relay हट गया।" ज़्यादा संभव यह है कि वह connect ही न करे, या consent अजीब loop में फंस जाए, या attach path आधा जिंदा लगे और फिर मर जाए।

NOVA: [EMPHASIS]openclaw doctor --fix[/EMPHASIS] आपकी current config पढ़ता है और host-local browser setups को सही modern mode में migrate करता है: [EMPHASIS]existing-session[/EMPHASIS] या [EMPHASIS]user[/EMPHASIS]। यह cosmetic recommendation नहीं है। यह migration का हिस्सा है।

ALLOY: और अब तीन modes को clarify करना भी ज़रूरी है। [EMPHASIS]existing-session[/EMPHASIS] का मतलब है एक running Chrome से attach करना। [EMPHASIS]user[/EMPHASIS] का मतलब है user profile के साथ launch करना। Raw [EMPHASIS]CDP[/EMPHASIS] Docker, headless, sandbox, remote setups के लिए — वह लगभग unchanged रहता है।

NOVA: जो सही separation है। पुराना extension path एक crutch था। यह सही move है।

ALLOY: मैं ज़्यादातर सहमत हूं, लेकिन users को वह crutch क्यों पसंद था, यह मैं defend करना चाहता हूं। Crutch तब समस्या है जब वह healing रोकता है। वह मददगार है जब वह आपको चलने देता है। बहुत से users के लिए extension ही एकमात्र browser flow था जिसे वे consistently काम करा पाते थे।

NOVA: यह fair है, लेकिन वह fragility खरीदकर मिली consistency थी। System में attach model को ढकने के लिए एक extra custom bridge था।

ALLOY: सही। और .23 असल में आपका point prove करती है, क्योंकि जैसे ही .22 ने पुराना path हटाया, .23 को तुरंत real world में नए path को reliable बनाना पड़ा। [PAUSE] यहां दो fixes मायने रखती हैं। पहली, tab attach timing। OpenClaw Chrome MCP handshake को ऐसे treat कर रहा था जैसे connection आते ही browser पूरी तरह ready हो। macOS पर ऐसा हमेशा नहीं था। Tabs मौजूद थीं, लेकिन उपयोग के लिए तैयार नहीं थीं। इसलिए first attach consent churn कर सकता था, timeouts spin कर सकता था, और कुल मिलाकर haunted महसूस होता था।

NOVA: वह fix इसलिए matter करती है क्योंकि readiness binary नहीं होती। Socket open होना यह नहीं है कि UI surface stable भी हो।

ALLOY: बिल्कुल। दूसरी fix: loopback reuse। Headless या loopback setups में OpenClaw एक short probe पर running browser miss कर सकता था और तुरंत relaunch पर fallback कर देता था। इससे second-run regressions बनती थीं जहां पहली run काम करती थी और अगली run ऐसे व्यवहार करती थी जैसे उसे session bulldoze करना पड़े। .23 उस fallback से पहले एक छोटा wait जोड़ती है।

NOVA: जो सुनने में छोटा लगता है, जब तक आप उसके साथ जीते नहीं हैं। तब वह flaky महसूस होने वाले browser tool और intentional महसूस होने वाले tool के बीच का फर्क बन जाता है।

ALLOY: इसलिए browser transition पर मेरी summary यह है: .22 ने पुराना path हटाया, .23 ने नया path reliable बनाया, और आपको दोनों चाहिए। अगर आप सिर्फ़ release headlines के स्तर पर सोच रहे हैं, तो आप miss कर देंगे कि ये दोनों versions वास्तव में कितनी गहराई से coupled हैं।

NOVA: और अगर आप host-local browser automation चलाते हैं, तो [EMPHASIS]doctor --fix[/EMPHASIS] को general maintenance chore नहीं, browser migration के हिस्से के रूप में treat कीजिए। वह targeted work कर रहा है।

ALLOY: हां। Optional housekeeping नहीं। Migration step।

NOVA: और browser shift में एक बड़ा lesson भी है। Browser automation उन क्षेत्रों में से एक है जहां लोग absurd complexity को tolerate करते हैं क्योंकि payoff इतना बड़ा होता है। वे extension install करेंगे, version pin करेंगे, profile bless करेंगे, weird launch flags उठाएंगे, कुछ भी करेंगे, बस browser उनकी बात माने। [PAUSE] लेकिन हर hidden workaround user interface के साथ technical debt बन जाता है।

ALLOY: यह उसे कहने का बहुत अच्छा तरीका है। Extension सिर्फ़ code debt नहीं थी। वह user ritual debt भी थी। आपको याद रखना पड़ता था कि वह मौजूद है, कैसे install हुई थी, क्यों कोई browser profile special थी, Chrome update होने पर क्या टूटता था। यह ऐसी platform story नहीं है जिसे आप हमेशा रखना चाहेंगे।

NOVA: Existing-session attach कहीं ज़्यादा honest model है। या तो attach करने के लिए browser है, या नहीं है। या तो profile usable है, या नहीं है। Magic कम है।

ALLOY: Magic कम है, लेकिन readiness और timing को सही करने की responsibility ज़्यादा है, और यही वजह है कि .23 की fixes इतना matter करती हैं। अगर आप पुराना bridge हटा रहे हैं, तो direct path boring महसूस होनी चाहिए। Browser automation में boring ही success है।

NOVA: Boring, dependable, legible। यही goal है।

## [17:00-22:00] Image Gen को standardize किया जा रहा है

NOVA: अब image generation। यह browser tooling जितना dramatic नहीं है, लेकिन यह आपको बहुत कुछ बताता है कि OpenClaw कहां जा रहा है। Bundled [EMPHASIS]nano-banana-pro[/EMPHASIS] skill हटा दी गई है। Gone। कोई shim नहीं।

ALLOY: जिसका मतलब है कि अगर आपके workflows, prompts, या internal docs [EMPHASIS]nano-banana-pro[/EMPHASIS] को call करते हैं, तो उन्हें ढूंढिए और replace कीजिए। यह hard break है। यह assume मत कीजिए कि कोई alias आपका इंतज़ार कर रहा होगा।

NOVA: Platform अब [EMPHASIS]image_generate[/EMPHASIS] core tool पर standardize कर रहा है। और philosophical स्तर पर मुझे लगता है कि यह बिल्कुल सही है। एक tool, configurable backend, consistent invocation surface। यह उससे बेहतर है कि सिर्फ़ इसलिए bundled skill wrapper को हमेशा ढोते रहें क्योंकि लोग उसके नाम के आदी हो गए।

ALLOY: बशर्ते आप config key set करें। यही वह हिस्सा है जिसे लोग skip कर देते हैं। आपको [EMPHASIS]agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"[/EMPHASIS] चाहिए। अगर आपने यह set नहीं किया, तो behavior undefined है। और config land में undefined का मतलब कभी exciting नहीं होता। उसका मतलब confusing होता है।

NOVA: यहां एक broader pattern है। OpenClaw core capabilities को core capabilities की तरह दिखाना चाहता है। Image generation को sidecar trick जैसा महसूस नहीं होना चाहिए।

ALLOY: सही, लेकिन operationally मैं इसे और blunt तरीके से कहूंगा: standardization तभी अच्छी लगती है जब defaults explicit हों। अगर आप पुरानी bundled चीज़ हटा दें और नया backend set ही न करें, तो आपने architecture को cleaner और Tuesday को बदतर बना दिया।

NOVA: Fair criticism। [PAUSE] इस shift के साथ marketplace improvements भी आई हैं। Marketplace installs अब first-class हैं, जिनमें [EMPHASIS]plugin@marketplace[/EMPHASIS] syntax और Claude marketplace registry support शामिल है।

ALLOY: जिससे plugin installation के आसपास की folklore कम होती है। कम ऐसे moments जब कहना पड़े, "असल में इस plugin के लिए यह दूसरी तरह से करो।"

NOVA: और owner-gated [EMPHASIS]/plugins[/EMPHASIS] और [EMPHASIS]/plugin[/EMPHASIS] chat commands उसी theme को आगे बढ़ाते हैं: platform को extensions खोजने, install करने और manage करने के लिए एक coherent story दो।

ALLOY: मुझे यह भी पसंद है कि वे owner-gated हैं। Install surface जितनी powerful होती जाती है, उतना ही कम आप चाहते हैं कि random runtime contexts उसे खिलौने की तरह लें।

NOVA: मेरे लिए image generation की कहानी यह है: OpenClaw bundled personality से configured capability की ओर बढ़ रहा है। [PAUSE] यही maturity है।

ALLOY: मेरे लिए कहानी यह है: अपने workflows update करो, model key set करो, और broken image calls को automation में पड़े मत रहने दो जिन्हें आप demo के दौरान ही discover करो।

NOVA: और उस standardization में एक subtle governance change भी छिपा है। जब image generation एक core tool होती है, किसी प्यारी bundled skill की जगह, तब आप providers बदल सकते हैं, interface को एक बार improve कर सकते हैं, behavior एक बार document कर सकते हैं, और permission surface एक बार audit कर सकते हैं।

ALLOY: सही। तब यह "वह एक special चीज़ जो wrapper की वजह से काम करती है" नहीं रहती, बल्कि actual platform contract का हिस्सा बन जाती है। यह ज़्यादा healthy है।

NOVA: यह teams के portability के बारे में सोचने का तरीका भी बदलती है। अगर आपका workflow [EMPHASIS]image_generate[/EMPHASIS] कहता है और backend अलग से configured है, तो आप workflow logic rewrite किए बिना provider migrate कर सकते हैं।

ALLOY: जो theory में अच्छा है और शुक्रवार दोपहर किसी vendor के pricing या rate limits बदलने पर उससे भी ज्यादा अच्छा लगता है।

NOVA: बिल्कुल। Standardization सिर्फ़ elegance नहीं है। यह leverage भी है।

ALLOY: बशर्ते आप config key set करें।

NOVA: बशर्ते आप config key set करें। आप यह बात समय के अंत तक दोहरा सकते हैं।

## [22:00-31:00] इसे टिकाऊ बनाना — .23 Reliability Pass

NOVA: यही episode का दिल है। क्योंकि .22 purge है, लेकिन .23 reliability pass है जो purge को survivable बनाती है। Intro के पहले bug पर वापस चलते हैं: MiniMax failover।

ALLOY: यही bug थी। यही वह थी जो लोगों को जला रही थी।

NOVA: Original issue classification थी। MiniMax से आने वाले generic [EMPHASIS]api_error[/EMPHASIS] responses को default रूप से transient माना जा रहा था। इसलिए OpenClaw चुपचाप retry करता था, actual failure suppress कर देता था, और proper fallback तब trigger ही नहीं करता था जब underlying issue billing, auth, या malformed context जैसी चीज़ होती थी।

ALLOY: और यही crucial distinction है। Transient error का मतलब है, शायद network को छींक आ गई, शायद provider थोड़ी देर के लिए wobble हुआ, शायद retry सच में काम कर जाए। लेकिन billing problem transient नहीं है। Auth problem transient नहीं है। Format या context rejection transient नहीं है। उन्हें retry करना सिर्फ़ समय बर्बाद करता है और सच्चाई छुपाता है।

NOVA: Fix बहुत precise है। यह नहीं कि "MiniMax पर retry करना बंद कर दो।" यह है, "सिर्फ़ तब retry करो जब error सच में transient दिखे।" [PAUSE] मुझे इस तरह की fix पर भरोसा होता है, क्योंकि यह original design goal — resilience — को बचाए रखती है, जबकि sloppy classification हटा देती है जिसने resilience को concealment जैसा बना दिया था।

ALLOY: और operators के लिए practical असर यह है: bad key, bad account state, malformed request, blown context window — अब इन्हें ऐसे fail होना चाहिए कि failure surface हो और fallback सही से engage करे। लोगों को शुरू से यही उम्मीद थी।

NOVA: यह उन bugs में से एक है जहां degraded experience शायद hard failure से भी बदतर थी, क्योंकि user को output तो मिला और उसने मान लिया कि वह faithful है।

ALLOY: हां। बिना किसी visible alarm के गलत जवाब visible failure से ज्यादा डरावना होता है। कम से कम visible failure investigation को invite करती है।

NOVA: अगला: OpenAI token revert bug। यह इस बात का बेहतरीन उदाहरण है कि memory और disk के बीच state drift user के trust से कैसे विश्वासघात करती है। Gateway auth-profile write path stale in-memory values को restart पर freshly saved credentials overwrite करने दे रही थी।

ALLOY: तो आप token paste करते थे, green confirmation देखते थे, restart करते थे, और expired। हर बार। [PAUSE] यही वजह है कि यह bug इतनी personal महसूस हुई। उसने credentials save करने की बुनियादी क्रिया पर trust पर हमला किया।

NOVA: और fix यह है कि token paste अब resolved agent store में सही तरह से write होती है, बजाय इसके कि stale in-memory snapshot restart के दौरान जीत जाए।

ALLOY: जिसका मतलब है कि upgrade के बाद आपको इसे test करना चाहिए। सिर्फ़ इसलिए assume मत कीजिए कि release note कहती है fixed है। Fresh token paste कीजिए, gateway restart कीजिए, verify कीजिए कि वह persisted रही। यह ठीक वही तरह की bug है जहां confidence कमाने का तरीका यह है कि आप पुराने failure को reproduce करें और देखें कि अब वह नहीं होती।

NOVA: तीसरा: cron और daylight saving time। यह तब तक boring लगता है जब तक यह किसी ऐसी चीज़ को न लगे जिस पर आप भरोसा करते हैं।

ALLOY: यह मुझे लगा था। मेरी morning report clocks बदलने के बाद एक घंटा इधर-उधर fire हो रही थी।

NOVA: ठोस उदाहरण: आप [EMPHASIS]8 AM[/EMPHASIS] job schedule करते हैं। DST आ जाता है। .23 से पहले, वह "8 AM" [EMPHASIS]7 AM[/EMPHASIS] या [EMPHASIS]9 AM[/EMPHASIS] बन सकता था, यह इस पर निर्भर करता था कि scheduler boundary को कैसे interpret कर रहा है। [PAUSE] यह सिर्फ़ cosmetic mismatch नहीं है। Daily routine के लिए यह टूटा हुआ वादा है।

ALLOY: Fix यह है कि [EMPHASIS]--at --tz[/EMPHASIS] अब DST boundaries के पार local wall-clock time का सम्मान करता है। और OpenClaw [EMPHASIS]--every[/EMPHASIS] के लिए [EMPHASIS]--tz[/EMPHASIS] reject भी करता है, जो अच्छा है क्योंकि recurring interval semantics और timezone wall-clock semantics एक चीज़ नहीं हैं।

NOVA: यह उसी तरह की constraint है जो users को गलत intuitions से बचाती है।

ALLOY: बिल्कुल। अगर आपका मतलब है "हर छह घंटे में," तो वह "जब भी मेरी local clock आठ बजे" के बराबर नहीं है। Tool अब उस फर्क को reflect करता है, उसे muddle नहीं करता।

NOVA: चौथा: Mistral [EMPHASIS]422[/EMPHASIS] fix। पुरानी persisted Mistral configs context-sized output limits carry कर रही थीं जिन्हें Mistral सीधे reject करता है। परिणाम: [EMPHASIS]422[/EMPHASIS] errors जो mysterious लगती हैं अगर आपको config lineage नहीं पता।

ALLOY: और फिर वही, [EMPHASIS]openclaw doctor --fix[/EMPHASIS] यहां असली काम कर रहा है। अब यह stale Mistral configs detect और repair करता है।

NOVA: [EMPHASIS]doctor --fix[/EMPHASIS] चलाने का एक और कारण। लोग कभी-कभी इस command को generic doctoring की तरह सुनते हैं, जैसे शायद यह कुछ obvious चीजें tidy कर देगी। नहीं। इस release train में यह migration knowledge को codify कर रही है।

ALLOY: पांचवां: macOS पर ClawHub। यहां दो issues थीं। Saved credentials macOS Application Support path का सही सम्मान नहीं कर रही थीं, और browse-all behavior unauthenticated [EMPHASIS]429[/EMPHASIS] rate limits से टकरा रहा था।

NOVA: जिसका मतलब है कि UI आपको vague तरीकों से यह महसूस करा सकती थी कि ClawHub खाली है या broken है।

ALLOY: macOS पर skill browsing चुपचाप unauthenticated पर fallback कर रही थी। आप empty lists देखते और मान लेते कि skills हैं ही नहीं, या आपका install टूटा हुआ है, जबकि असल में auth path handling गलत थी। [PAUSE] Fixes थीं सही auth path का सम्मान करना और browse-all को search endpoint पर shift करना, जो pointless unauthenticated throttling से बचने का कहीं ज्यादा sane तरीका है।

NOVA: छठा: bundled plugin runtimes। WhatsApp और Matrix runtime sidecars npm package में missing थीं, जिसका मतलब था कि global installs ऐसी तरह fail हो सकती थीं जो packaging voodoo जैसी लगे।

ALLOY: यह .22 के packaging changes से आया regression है, और OpenClaw के credit के लिए, .23 में यह जल्दी fix हो गया। लेकिन अगर आप वे runtimes globally चलाते हैं, तो यह footnote नहीं है। Missing sidecars का मतलब plugin stack बस complete नहीं है।

NOVA: सातवां: [EMPHASIS]web_search[/EMPHASIS] stale provider handling। Tool startup पर baked हुई provider state का इस्तेमाल कर रहा था, active runtime config का नहीं।

ALLOY: जो बिल्कुल वैसी bug है जो आपको यह सोचने पर मजबूर करती है कि config reloads सच में हैं भी या सिर्फ़ decorative हैं।

NOVA: आप Brave configure करते हैं, तो उसे Brave ही use करना चाहिए। यह हमेशा से ऐसे ही काम करना चाहिए था।

ALLOY: और अब करता है। फिर वही, glamorous नहीं, लेकिन expectation और behavior के बीच सीधी मरम्मत।

NOVA: आठवां: Telegram threading। [EMPHASIS]currentThreadTs[/EMPHASIS] अब Telegram DM topics के लिए threading tool-context fallback में populate होता है, ताकि thread-aware tools को सही topic context मिले।

ALLOY: यह उन fixes में से एक है जहां अगर आप Telegram DM topics use नहीं करते, तो आप कंधे उचकाते हैं, और अगर use करते हैं, तो कहते हैं, भगवान का शुक्र है। क्योंकि tool context का thread-blind होना वही है जो agents को गलत जगह जवाब देने या conversational lane खो देने की तरफ ले जाता है।

NOVA: जो खासकर उस system में बहुत दर्दनाक है जो context fidelity के इर्द-गिर्द बनी है।

ALLOY: बिल्कुल। पूरी बात ही यह है कि tool को पता होना चाहिए कि वह कहां है।

NOVA: तो इन सबको साथ रखें, तो .23 usual product sense में flashy नहीं है। यह phrase के सबसे गहरे अर्थ में reliability pass है। यह classification, state persistence, scheduler semantics, provider wiring, packaging completeness, और thread context को tighten करती है।

ALLOY: यह .22 की नई दुनिया को वास्तव में रहने लायक बनाती है।

NOVA: और मुझे लगता है कि इसी वजह से operators को इन दो releases को दो chapters वाली एक कहानी की तरह पढ़ना चाहिए। पहला chapter कहता है, "हमने पुराने compromises हटा दिए।" दूसरा chapter कहता है, "हमने उन जगहों को ठीक किया जहां नई assumptions में अब भी rough edges थीं।" [PAUSE] यह दिन एक पर big cleanup को perfect दिखाने के नाटक से कहीं ज्यादा honest development rhythm है।

ALLOY: हां। मैं .23 का सम्मान इसी वजह से करता हूं क्योंकि यह .22 ने जो destabilize किया, उसे छुपाने की कोशिश नहीं करती। यह बस उसे ठीक करती है। तेज़ी से। सीधे। बिना ego के।

NOVA: और user के रूप में structural release के बाद आपको यही चाहिए। Denial नहीं। Rapid correction।

ALLOY: खासकर silent चीज़ों के लिए। MiniMax fallback, token persistence, stale provider config — ये सब ऐसे bugs हैं जो trust को खा जाते हैं क्योंकि ये system को उससे कम legible महसूस कराते हैं जितना उसे होना चाहिए।

NOVA: Reliability आंशिक रूप से correctness है और आंशिक रूप से comprehensibility। Platform को सही काम करना चाहिए, और आपको यह समझ में आना चाहिए कि उसने वह काम वैसे क्यों किया।

ALLOY: यही वजह है कि .23 किसी feature release से ज्यादा मायने रखती है।

NOVA: सहमत।

## [31:00-35:00] Qwen, CSP, और छोटी चीज़ें

NOVA: चलिए छोटे बदलावों पर आते हैं, क्योंकि वे सिर्फ़ surface area में छोटे हैं, महत्व में ज़रूरी नहीं। पहला: [EMPHASIS]Qwen[/EMPHASIS] और [EMPHASIS]DashScope[/EMPHASIS]। OpenClaw अब China और global Qwen API keys के लिए standard DashScope endpoints को support करता है, और provider को [EMPHASIS]Qwen (Alibaba Cloud Model Studio)[/EMPHASIS] के नाम से relabel किया गया है।

ALLOY: Pay-as-you-go keys अब काम करती हैं। यही practical change है। अगर आप default OpenAI-Anthropic orbit के बाहर हैं, तो यह बहुत मायने रखता है।

NOVA: Qwen इस समय सबसे अच्छी open-weight families में से एक है। Proper DashScope support का मतलब है उन users के लिए असली accessibility जो strong models चाहते हैं लेकिन उन्हीं दो provider ecosystems में धकेले नहीं जाना चाहते जिन्हें बाकी सब assume करते हैं।

ALLOY: और बेहतर naming भी मायने रखती है। Full Model Studio identity से relabel करना config surface को कम cryptic बनाता है।

NOVA: अगला: [EMPHASIS]CSP[/EMPHASIS] hardening। Inline script blocks के लिए SHA-256 hashes। Inline scripts default रूप से blocked।

ALLOY: अगर आप OpenClaw को strict reverse proxy के पीछे चलाते हैं, तो upgrade करने के लिए यही version है।

NOVA: यह supply chain security के लिए मायने रखता है। Injected script execute नहीं होगी क्योंकि hash match नहीं करेगा। [PAUSE] यही वे controls हैं जो demo को सुंदर नहीं बनाते, लेकिन आपका blast radius छोटा कर देते हैं।

ALLOY: और frankly, mature platforms यही करती हैं। वे "अच्छा, वहां कोई inject नहीं करना चाहिए" पर निर्भर रहना बंद करती हैं और "अगर कुछ inject हो भी गया, तो क्या फिर भी नहीं चलेगा?" के इर्द-गिर्द बनना शुरू करती हैं।

NOVA: [EMPHASIS]Knot[/EMPHASIS] theme पर भी ध्यान दिया गया: [EMPHASIS]WCAG 2.1 AA[/EMPHASIS] contrast compliance, black-and-red palette tuning, config icons, discrete roundness stops।

ALLOY: AA contrast fix वही है जो मायने रखती है। Accessibility checks fail हो रहे थे। Style मज़ेदार है; readability अनिवार्य है।

NOVA: और मुझे हमेशा अच्छा लगता है जब accessibility improvements को niche side mission की बजाय default quality improvements की तरह treat किया जाता है।

ALLOY: आख़िरी छोटी चीज़: gateway usage totals अब rotated और archived sessions को शामिल करते हैं।

NOVA: जो लगभग accounting जैसी लगती है।

ALLOY: यह accounting जैसी ही है। लेकिन usage undercount कर रही थी। अब नहीं करती। अगर आप actual system load समझना चाहते हैं या समय के साथ activity compare करना चाहते हैं, तो archived sessions missing होना rounding error नहीं है। वह बस गलत है।

NOVA: तो इन releases की छोटी चीज़ें भी उसी दिशा की ओर इशारा करती हैं: कम ambiguities, कम lies of omission, और system वास्तव में क्या कर रही है, उसका ज्यादा accurate representation।

## [35:00-38:00] Upgrade Checklist

ALLOY: ठीक है, इसे concrete बनाते हैं। अगर आप upgrade कर रहे हैं, तो यह checklist है, और मेरा मतलब सचमुच checklist है। Mid-migration खुद पर भरोसा मत कीजिए कि आपको सब याद रहेगा।

NOVA: Step one non-negotiable है।

ALLOY: [EMPHASIS]openclaw doctor --fix[/EMPHASIS]। पहले, हर चीज़ से पहले। और सच कहूं तो अगर आप sequence को साफ़ तरीके से कर रहे हैं, तो हर upgrade stage के तुरंत बाद भी।

NOVA: इन releases के लिए यही anchor command है। Nice-to-have नहीं। Anchor।

ALLOY: Step two: [EMPHASIS]CLAWDBOT_*[/EMPHASIS] और [EMPHASIS]MOLTBOT_*[/EMPHASIS] को सभी [EMPHASIS].env[/EMPHASIS] files, Docker files, systemd units, shell profiles, हर उस startup surface में grep कीजिए जो आपके पास है।

NOVA: अगर पुराने names मौजूद हैं, तो मान लीजिए वे अब dead config हैं।

ALLOY: Step three: [EMPHASIS]~/.moltbot[/EMPHASIS] को check कीजिए। अगर वह मौजूद है, तो state को [EMPHASIS]~/.openclaw[/EMPHASIS] में move कीजिए या [EMPHASIS]OPENCLAW_STATE_DIR[/EMPHASIS] को explicitly set कीजिए।

NOVA: Step four: [EMPHASIS]agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"[/EMPHASIS] set कीजिए। Image generation को undefined limbo में मत छोड़िए।

ALLOY: Step five: upgrade के बाद MiniMax को bad key के साथ re-test कीजिए और confirm कीजिए कि fallback fire करती है। सिर्फ़ happy-path prompt मत भेजिए। पुराने failure mode को induce कीजिए।

NOVA: Step six: एक OpenAI token paste कीजिए, gateway restart कीजिए, और confirm कीजिए कि वह persisted रही। Trust करें, लेकिन verify भी करें।

ALLOY: Step seven: अगर आपके पास custom plugins हैं, तो [EMPHASIS]openclaw/extension-api[/EMPHASIS] से [EMPHASIS]openclaw/plugin-sdk/*[/EMPHASIS] पर migrate कीजिए। Migration docs पढ़िए। Compile errors को map मत समझिए।

NOVA: Step eight: install behavior change के बाद ClawHub skills को spot-check कीजिए। पक्का कीजिए कि आपकी scripts और expectations अब भी उस चीज़ से match करती हैं जो resolve हो रही है।

ALLOY: Step nine: [EMPHASIS]--at --tz[/EMPHASIS] इस्तेमाल करने वाले cron jobs verify कीजिए, खासकर अगर DST ने आपको पहले कभी जलाया हो।

NOVA: गहरी summary यह है कि ये दोनों releases मिलकर वह पूरा कर रही हैं जो OpenClaw ने शुरू किया था। Moltbot और Clawdbot names gone हैं। Extension relay gone है। Plugin SDK unified है। Silent failures fix हो चुकी हैं।

ALLOY: पहले Doctor [EMPHASIS]--fix[/EMPHASIS]। बाकी सब इस पर depend करता है कि आप क्या चला रहे हैं। लेकिन [EMPHASIS]doctor --fix[/EMPHASIS] unconditional है।

NOVA: यही वह platform है जो आप चाहते थे कि यह बने।

## [38:00-39:30] Outro

ALLOY: और मुझे लगता है कि यहीं ख़त्म करना सही होगा। ये releases demanding हैं, लेकिन वे किसी असली चीज़ की सेवा में demanding हैं: ऐसी platform जो जो है वही कहती है, जो कहती है वही करती है, और पुराने दौरों के कम ghosts ढोती है।

NOVA: जो OpenClaw जैसे tool के लिए novelty से ज्यादा मायने रखता है। [PAUSE] Reliability एक feature है। Naming consistency एक feature है। Honest migration pressure एक feature है। कम improvised bridges वाला browser stack एक feature है।

ALLOY: और अगर आप अभी upgrade के बीच में हैं, तो एक सांस लीजिए, checklist बनाइए, [EMPHASIS]openclaw doctor --fix[/EMPHASIS] चलाइए, और verification steps सिर्फ़ इसलिए मत छोड़िए कि service वापस ऊपर आ गई।

NOVA: Show notes, हमने जिन सभी links का ज़िक्र किया, और episode archive आपको [EMPHASIS]tobyonfitnesstech.com[/EMPHASIS] पर मिलेंगे। वही है [EMPHASIS]tobyonfitnesstech.com[/EMPHASIS]।

ALLOY: अगर इस episode ने आपको broken browser setup, गायब env var, या एक और mysterious auth failure से बचा लिया, तो उसने अपना काम कर दिया।

NOVA: मैं NOVA हूं।

ALLOY: मैं Alloy हूं।

NOVA: और यह था OpenClaw Daily। हम जल्द वापस आएंगे।

ALLOY: फिर मिलते हैं।
