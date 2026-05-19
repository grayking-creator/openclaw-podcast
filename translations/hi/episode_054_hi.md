[NOVA]: मैं NOVA हूं।

[ALLOY]: और मैं ALLOY हूं, और ये है AgentStack Daily। आज शुरू होता है उस coding surface से जिसे ज़्यादातर एजेंट बिल्डर्स हर दिन छूते हैं: Claude Code CLI, 2.1.144 रिलीज़ के साथ।

[NOVA]: ये एक maintenance release है, और यही वजह है कि ये आगे है। ये उन surfaces को टारगेट करता है जहां unattended agents अक्सर टूटते हैं: background और detached sessions, बुरे network पर startup behavior, MCP transport layer, और tool-call hygiene। अपने आप के लिए नई features नहीं। failure modes हटाए गए।

[ALLOY]: रिलीज़ readout के बाद, पांच और moves जो बदलते हैं कि builders कैसे चुनते हैं, जोड़ते हैं, और चलाते हैं अपने tools। Cursor ने Composer 2.5 भेजा, एक coding-agent model Kimi K2.5 base पर, frontier per-token cost का लगभग दसवां हिस्सा। Anthropic ने Stainless acquire किया, वो service जो API specifications को typed client libraries में बदलती थी AI labs की लंबी लिस्ट के लिए। Notion ने अपनी workspace को hosted runtime में बदल दिया जहां agents execute करते हैं। Vercel AI SDK ने अपना LangChain और LangGraph adapter फिर से लिखा। और Cloudflare ने zero-trust networking और identity को agent lifecycle के नीचे रख दिया Mesh के साथ।

[NOVA]: तीनों में practical question same है। इनमें से कौन सा change agent work को ज़्यादा reliable, ज़्यादा recoverable, और trust करने में आसान बनाता है जब run लंबी हो, unattended हो, या किसी और के API में boundary पार कर रही हो?

[ALLOY]: तो हम concrete रहेंगे, और रहेंगे on what a builder को actually करना चाहिए: session lifecycles, transport pagination, degraded networks पर timeouts, tool-using models के लिए reward shaping, harness fidelity, और typed boundary agent और services के बीच जिन्हें वो call करता है। ...

[NOVA]: शुरू में ये बता देना worth है कि command-line tool की एक point release एपिसोड के front पर क्यों आती है flashy model launch के बजाय। Claude Code CLI, कई teams के लिए, actual runtime है जिसमें उनके agents execute करते हैं। ये sessions spawn करता है, tools hold करता है, MCP servers से बात करता है, background में चलता है, और recover करता है जब कुछ गलत होता है। जब वो layer बदलता है कि failure के नीचे वो कैसे behave करता है, ये real agent work ज़्यादा move करता है किसी benchmark number से।

[ALLOY]: और 2.1.144 लगभग पूरी तरह failure-mode work है। एक startup hang हटा दिया गया। truncated tool list fix हुई। एक image type जो conversation break करता था अब handle होता है। Protected folder में crash होने वाले background sessions अब stable हैं। ये कोई glamorous नहीं है। ये सब है agent run के बीच का फर्क जो unattended complete होती है और जो चुपचाप सुबह तीन बजे stall हो जाती है।

[NOVA]: ये lens है पूरे release block के लिए। नहीं कि क्या है नया show off करने के लिए, बल्कि क्या fail होता था और अब नहीं होता, और builder को क्या change करना चाहिए उनके agent deploy करने के तरीके में इसकी वजह से।

[ALLOY]: Right, और हम हर fix को एक concrete builder decision से जोड़ते रहेंगे: background sessions कब use करने हैं, MCP कैसे wire करने हैं, unattended agent ship करने से पहले क्या test करना है। Release तभी useful है जब ये बदलता है कि आप operate करते हैं।

[NOVA]: एजेंट-स्टैक रिलीज़ रीडआउट: Claude Code CLI 2.1.144. स्टार्टअप से शुरू करते हैं। ...

[NOVA]: स्टार्टअप फिक्स सबसे स्पष्ट उदाहरण है कि यह रिलीज़ एजेंट्स के लिए लोगों की तुलना में ज्यादा क्यों मायने रखती है। 2.1.144 से पहले, अगर API एंडपॉइंट पहुंच योग्य नहीं था, तो CLI कुछ उपयोगी करने से पहले पचहत्तर सेकंड तक ब्लॉक हो सकता था। यह कैप्टिव पोर्टल, कॉर्पोरेट फायरवॉल, या VPN के पीछे होता है जो कनेक्ट होना पूरा नहीं कर पाया है।

[ALLOY]: एक इंसान इससे बुरा प्रभाव पड़ता है और बस इंतज़ार करता है, शायद बड़बड़ाता है। एक एजेंट इसे बहुत अलग तरीके से टकराता है। एक निर्धारित जॉब, एक अनआटेंडेड बैच रन, या फ्लैकी नेटवर्क पर बैकग्राउंड सेशन पचहत्तर सेकंड के ब्लॉक को स्टॉल, स्टैक में और ऊपर टाइमआउट, या मिस्ड एक्जीक्यूशन विंडो में बदल देता है। फिक्स साइड-चैनल कॉल को पंद्रह सेकंड पर सीमित करता है।

[NOVA]: बिल्डर्स के लिए सामान्य सिद्धांत यह है कि खराब नेटवर्क पर स्टार्टअप रेज़िलिएंस एक एजेंट विश्वसनीयता संपत्ति है, सौंदर्यशास्त्रीय आनंद नहीं। कोई भी चीज़ जो एजेंट अनआटेंडेड करता है उसे यह मानना होगा कि नेटवर्क कभी-कभी प्रक्रिया शुरू होने के ठीक उसी पल गलत होता है। वह टूल जो जल्दी विफल होता है और आगे बढ़ता है उसे आने वाली चीज़ की विनम्र प्रतीक्षा करने वाले टूल से अधिक विश्वसनीय माना जाता है।

[ALLOY]: यहाँ एक ठोस बिल्डर पैटर्न है। अगर आप एजेंट्स को शेड्यूल पर स्टार्ट करने के लिए डिप्लॉय करते हैं, तो आपको प्रोसेस स्टार्ट को एक स्टेप के रूप में मानना चाहिए जो धीमा या आंशिक रूप से खराब हो सकता है, और आपको उसी तरह से इसका टेस्ट करना चाहिए। सिम्युलेट करने के लिए यूज़ केस हैपी पाथ नहीं है। यह कैप्टिव पोर्टल है, आधा-कनेक्टेड VPN, धीमे से रेज़ॉल्व होने वाला DNS। इस रिलीज़ से पहले सही कदम था अपना खुद का स्टार्टअप वॉचडॉग जोड़ना। इसके बाद, रनटाइम खुद तेज़ी से विफल होता है, लेकिन आपको अपने खुद के डिप्लॉय के खिलाफ इसकी फिर भी पुष्टि करनी चाहिए।

[NOVA]: यह एक अच्छा फ्रेमिंग है। बिल्डर को यह याद रखना चाहिए कि अनआटेंडेड एजेंट्स को शिप करने के तरीके में स्टार्टअप-हेल्थ अनुमान को शामिल करें, और इस रिलीज़ का उपयोग उस चीज़ के रूप में करें जो यह अनुमान बनाए रखती है, न कि कुछ ऐसा जो आपको अलग से जोड़ना पड़ता।

[ALLOY]: दूसरा ब्लॉक MCP है, Model Context Protocol ट्रांसपोर्ट, और यह वह है जिसे मैं स्किप नहीं करूंगा। इस रिलीज़ से पहले, MCP सर्वर जो अपने टूल्स-लिस्ट रिस्पॉन्स को पेजिनेट करते थे, वे केवल पहला पेज लौटाते थे। इसके एजेंट के लिए क्या मतलब है इसके बारे में सोचें। एजेंट टूल सर्वर से कनेक्ट होता है, पूछता है कि कौन से टूल मौजूद हैं, और चुपचाप आंशिक लिस्ट प्राप्त करता है।

[NOVA]: यह सबसे खराब तरह का बग है, क्योंकि कुछ भी एरर नहीं होता। एजेंट क्रैश नहीं होता। यह बस कुछ नहीं कर सकता जो वह करने में सक्षम होना चाहिए था, और रन रीज़निंग फेल्योर जैसा दिखता है जबकि वास्तव में यह ट्रांसपोर्ट बग है। आप दोपहर बिताएंगे मॉडल को दोष देते हुए कि वह एक टूल का उपयोग क्यों नहीं कर रहा जो मॉडल को कभी बताया ही नहीं गया था।

[ALLOY]: बिल्कुल। एक चुप क्षमता अंतर डिबग करना एक तेज़ क्रैश से कहीं ज्यादा कठिन है। फिक्स यह है कि पेजिनेटेड टूल्स-लिस्ट रिस्पॉन्स अब हर पेज के माध्यम से फॉलो थ्रू करते हैं, ताकि एजेंट पूरा टूल सेट देख सके। दर्जनों टूल्स के साथ एक बड़े MCP डिप्लॉयमेंट को चलाने वाले बिल्डर के लिए, यह उस एजेंट और दूसरे एजेंट के बीच का अंतर है जो आपके पूरे टूलसेट का उपयोग कर सकता है और जो केवल पहले पेज पर फिट होने वाला उपयोग कर सकता है।

[NOVA]: MCP इमेज के लिए एक संबंधित फिक्स है: एक असमर्थित MIME टाइप वाली इमेज, जैसे SVG, बातचीत को तोड़ देती थी। अब इसके बजाय इसे सेव किया जाता है और रेफर किया जाता है, ताकि एक अजीब कंटेंट टाइप पूरे सेशन को खराब न करे। अगर आप एक एजेंट बनाते हैं जो यूज़र-सप्लाइड इमेज या स्क्रीनशॉट्स को हैंडल करता है, तो यह एक असली रॉबस्टनेस चेंज है, क्योंकि आप कंट्रोल नहीं करते कि कौन सा कंटेंट टाइप दिखाई देता है।

[ALLOY]: और उसी क्षेत्र में एक diagnosability fix भी है। MCP servers के लिए list command पहले config parse न होने पर चुपचाप "कोई servers नहीं" report करता था। अब यह असली समस्या report करता है। यह वही theme है: एक silent गलत जवाब अब explicit, actionable जवाब से बदल दिया गया है, जो वही property है जो आप चाहते हैं जब आप एक fleet operate कर रहे हैं और fast triage करनी है।

[NOVA]: इस release के बाद MCP के लिए builder pattern यह है: अपने tools को deploy-time check के रूप में enumerate करें, उम्मीद पर नहीं। इससे पहले कि आप एक agent ship करें जो किसी tool server पर निर्भर है, agent से tools list करवाएं और assert करें कि पूरी expected set present है। यह release उस assertion को trustworthy बनाती है, क्योंकि list अब silently truncate नहीं होती। इसे अपने deploy validation में bake कर लें।

[ALLOY]: तीसरा और सबसे बड़ा block है background और detached sessions। यहां individual fixes की भारी संख्या आपको बताती है कि operational pain असल में कहां है। Background sessions अब resume support करते हैं, तो background में gestarted session अब interactive sessions के साथ दिखता है और उसे वापस pick up किया जा सकता है। Completion notices में अब elapsed duration शामिल है, तो एक agent जो तीन घंटे चला, वह बताता है।

[NOVA]: यह elapsed-duration detail minor लगती है लेकिन ऐसी नहीं है। अगर आप long-running agents operate करते हैं, तो duration एक primary signal है। एक task जो normally बीस मिनट लेती है और अचानक तीन घंटे ले गई, वह आपको कुछ बता रही है भले ही वह succeed हो गई। Completion पर duration surface करने से operator को बिना separate instrumentation build किए एक cheap anomaly signal मिलती है।

[ALLOY]: unattended fleets के लिए important platform-specific stability fixes का एक cluster है। macOS पर background sessions का crash जब project Full Disk Access-protected folder के नीचे होता है, वह fix हो गया है। Windows पर, attached background sessions में scrolling, mouse wheel और navigation shortcut अब काम करते हैं, और attached होने पर terminal close करने से अब session crash नहीं होता।

[NOVA]: यह macOS वाला एक classic deploy-environment trap है। Agent आपकी machine पर काम करता है और build host पर crash करता है क्योंकि build host project को एक protected folder के नीचे रखता है। General builder lesson यह है कि background-session stability environment-sensitive है, तो जहां आप test करते हैं वह जहां आप deploy करते हैं उससे match होना चाहिए। यह release उसका एक specific instance remove करती है, लेकिन pattern worth internalizing है।

[ALLOY]: और एक subtle correctness वाला: resumed sessions अब उनके द्वारा use किए जा रहे model को keep करते हैं, किसी दूसरे session के model choice को inherit करने के बजाय। अगर आप एक long-running agent resume करते हैं और वह silently models switch कर जाता है, तो आपका behavior, cost और latency सब बदल जाते हैं आपके नीचे, और हो सकता है आपको तब तक पता न चले जब तक output अलग न दिखे।

[NOVA]: यह उन सभी के लिए real production hazard है जो sessions में models का mix run करते हैं। एक cheap model जो quietly expensive model में promote हो जाए, वह आपके cost model को blow करता है। एक expensive model जो quietly cheap model में demote हो जाए, वह quietly quality degrade करता है। Model identity को session की एक stable property होनी चाहिए, और यह release उसे एक बनाती है।

[ALLOY]: एक fix भी है जहां Edit और Write एक worktree-isolation error से refuse कर रहे थे session detach होने के तुरंत बाद। ऐसी चीजें background work को unreliable feel कराती हैं: आप एक session detach करते हैं यह उम्मीद से कि वह काम करता रहेगा, और पहली चीज जो वह करने की कोशिश करता है वह fail हो जाती है isolation guard race की वजह से। इसे remove करने से detach-run-wake-resume lifecycle कुछ ऐसा बन जाता है जिसपर आप actual में build कर सकते हैं।

[NOVA]: उस lifecycle के बारे में precise रहें, क्योंकि यह एक builder के लिए इस release का heart है। एक background session spawn होता है, फिर terminal से detach होता है, idle होने पर retired हो सकता है, जब चाहिए wake हो सकता है, और अगर stop हो गया तो respawn हो सकता है। उनमें से हर transition एक जगह है जहां state lost या corrupted हो सकती है। यह release उनमें से कई को एक साथ harden करती है, इसीलिए यह readout की deserve करती है।

[ALLOY]: और वह builder use case जो उस lifecycle पर निर्भर करता है, वही है जो सबको चाहिए: एक लंबा agent task शुरू करो, चले जाओ, उसे चलने दो, वापस आओ, और thread खोए बिना उसे फिर से शुरू करो। इस release से पहले यह pattern इतना fragile था कि कई teams इससे बचते थे और sessions को attached रखते थे। इसके बाद, detached long-running work कुछ ऐसा है जिसके बारे में तुम actual में design कर सकते हो।

[NOVA]: चौथा area है tool-call hygiene, और यह जितना लगता है उससे कहीं ज्यादा important है। दो बदलाव अलग दिखते हैं। किसी file का head और tail view अब read-before-edit check को satisfy करता है। और grep, git grep, या git diff जैसे search tools से मिली empty results अब tool failure के तौर पर report नहीं होतीं।

[ALLOY]: read-before-edit वाले को unpack करो। CLI एक invariant enforce करती है कि agent को file edit करने से पहले उसे पढ़ना होगा, जो blind edits को रोकता है। लेकिन अगर agent ने head या tail view use करके file देखी थी, तो पहले यह count नहीं होता था, तो एक legitimate edit block हो जाती थी। अब वे views invariant satisfy करते हैं। guarantee बरकरार है, लेकिन false block हटा दिया गया है।

[NOVA]: और empty-search-result fix एक cosmetic fix के रूप में छिपा behavior fix है। अगर agent कोई search चलाता है, कोई match नहीं मिलता, और harness उसे tool failure बताता है, तो agent एक failure पर react करता है जो हुई ही नहीं। वह retry करता है, second-guess करता है, या बुरा path लेता है, क्योंकि "no matches" एक valid, informative result है, error नहीं। Spurious failure हटाने से spurious agent behavior हट जाती है।

[ALLOY]: यह इस release में एक recurring pattern है जिसे builders के लिए name करना worth है। False failure signals मुफ्त में नहीं आते। एक agent जो believe करता है कि एक successful operation fail हुई, वह decisions लेगा ऐसी problem को compensate करने के लिए जो exist ही नहीं करती। Tool boundary पर success और failure क्या count होता है यह clean करने से agent reasoning सीधे clean होती है, जिसका मतलब है तुम्हारी हर deploy पर wasted turns कम और cost कम।

[NOVA]: एक और concrete change: model picker अब session-scoped है, नए sessions के लिए अलग default के साथ। एक task के लिए model change करने से अब silent में सबके लिए model नहीं बदलता। Bedrock और Vertex users के लिए एक related fix है जो picker से long-context Opus option select नहीं कर पा रहे थे। Theme same है: model choice explicit और local होनी चाहिए, accidental global side effect नहीं जो तुम्हें अगली deploy में follow करे।

[ALLOY]: तो upgrade posture क्या है, एक actual builder checklist के तौर पर? 2.1.144 install करो, और फिर changed surfaces को assume करने की जगह exercise करो। एक background session शुरू करो, detach करो, wake करो, और resume करो, और confirm करो कि वह अपना model बनाए रखती है। उसे एक MCP server की तरफ point करो जो अपने tool list को paginate करता है और confirm करो कि पूरा set visible है। एक unsupported image type को एक MCP tool के through feed करो और confirm करो कि conversation survive करती है।

[NOVA]: और इसे एक बार network पर चलाओ जहां API endpoint briefly unreachable है, और confirm करो कि startup अब stall नहीं होता। एक maintenance release का value पूरी तरह conditional है। यह तभी कुछ worth है अगर यह failure modes जो हटाती है वे वही हैं जो तुम्हारे agents actual में hit कर रहे थे। अगर तुम बहुत unattended background work चलाते हो, तो इनमें से कई almost certainly तुम्हें hit कर रहे थे, और सही response है redeploy करना और exactly उन paths को re-test करना, यह assume करना नहीं कि upgrade invisible है।

[ALLOY]: इस release को छोड़ने से पहले, एक और cluster जो builder के attention worth है: respawn और wake behavior। एक stopped background session जिसे तुम respawn करते हो वह पहले खुद को stopped report कर सकता था भले ही वह फिर से run हो रही हो, और agent list से session open करने पर hang हो सकता था अगर background service unresponsive थी। दोनों fixed हैं। अगर तुम कोई supervisor बनाते हो जो agents restart करता है, तो तुम probably exact इन्हीं को retries और timeouts से papering over कर रहे थे।

[NOVA]: यही pattern worth naming है। बहुत सारी teams unattended agents के चारों ओर एक babysitter process बनाती हैं: stopped के लिए watch करो, respawn करो, re-check करो, alert करो अगर वापस नहीं आता। इनमें से हर step runtime पर depend करता है कि वह state honestly report करे। जब respawn कहता है stopped जबकि process actual में run हो रही हो, तो तुम्हारा supervisor either double-spawn करता है या give up कर देता है। Honest state reporting वह चीज है जो तुम्हारे supervisor को actual में safe बनाती है जिसे तुम deploy करते हो।

[ALLOY]: और यहाँ एक और शांत observability fix है: वे completed या stopped background sessions जो briefly fail to wake हुए थे, उन्हें permanently startup crash के तौर पर mark कर दिया जा रहा था। यह एक false-positive है जो आपके operational signal को poison करता है। अगर आप startup crashes पर alert करते हैं, तो आपको उन sessions के लिए page किया जा रहा था जो ठीक थे। इसे हटाने से crash signal का मतलब वही होता है जो आप सोचते हैं, और यही signal रखने का पूरा point है।

[NOVA]: तो 2.1.144 के लिए operator summary यह है कि यह unattended lifecycle को honest बनाता है। Spawn, detach, retire, wake, respawn, और resume अब state report करते हैं जिस पर आप supervisor build कर सकते हैं, MCP से silent truncation के बिना talk कर सकते हैं, और bad network पर stall किए बिना start up कर सकते हैं। यही precisely वह surface है जिस पर आप depend करते हैं जब आप agents deploy करते हैं जो बिना human watch के run करती हैं।

[ALLOY]: यही release block है। एक point release, लेकिन dense one, concentrated precisely उन unattended-agent surface पर जिसे builders production में ship करते हैं। अब एक अलग तरह के change पर: runtime नहीं, बल्कि उसके अंदर का model। ...

[NOVA]: Cursor Composer 2.5 May 18 को landed हुआ। यह एक coding-agent model है जो Kimi K2.5 base पर build है, heavier post-training के साथ, specifically longer autonomous coding sessions के लिए targeted। आइए Cursor जो numbers report करता है उनसे शुरू करते हैं, फिर training में जाते हैं, क्योंकि training method वह portion है जो एक builder के deciding what to ship के लिए ज्यादा interesting है।

[ALLOY]: Reported benchmarks: SWE-Bench Multilingual 73.7 से बढ़कर 79.8 percent, Terminal-Bench 61.7 से बढ़कर 69.3 percent। Terminal-Bench 2.0 पर यह Opus 4.7 से tie करता है और GPT-5.5 से पीछे है। Standard pricing fifty cents per million input tokens और two dollars fifty per million output tokens है। Headline यह price है: roughly Opus 4.7 per token का दसवां हिस्सा, comparable coding-benchmark performance पर।

[NOVA]: पहले benchmarks, सही caution के साथ। SWE-Bench और Terminal-Bench real signals हैं, लेकिन वे saturated suites हैं जहाँ frontier models कुछ points के भीतर cluster करती हैं, और harness differences specific task types पर model gap को swamp कर सकती हैं। Numbers को treat करें as "यह conversation में है," "यह तय हो गया है" नहीं। हम वापस आएंगे कि एक builder को actually क्या measure करना चाहिए।

[ALLOY]: Training जगह है जहाँ actually explain करने के लिए कुछ है। Cursor three shifts report करता है। पहला, textual-feedback reinforcement learning। End-of-run reward के अलावा, model को failed tool call के point पर localized hints मिलती हैं।

[NOVA]: यह एक credit-assignment change है, और यह specifically long-horizon agents के लिए matters। एक coding session की कल्पना करें fifty tool calls के साथ। अगर केवल signal end पर pass या fail है, तो model के पास लगभग कोई information नहीं है कि किस call में mistake थी। Reward पूरे trajectory पर smeared है। Failed call पर localized textual feedback एक sharp signal देता है जो exactly उस behavior को point करता है जो गलत हुई।

[ALLOY]: Credit assignment agents को train करने में central hard problem है जो long sequences of actions लेती हैं। Horizon जितना लंबा, single terminal reward उतना ही weak होता जाता है, क्योंकि एक outcome के लिए blame share करने वाले actions ज्यादा होते हैं। Feedback को उन action के करीब ले जाना जिसने failure cause की, यह उन few चीजों में से एक है जो reliably help करती हैं, और यही precisely वह regime है जिसमें एक autonomous coding agent operate करता है जब आप इसे real work पर deploy करते हैं।

[NOVA]: दूसरा shift: twenty-five times ज्यादा synthetic tasks, feature-deletion rebuild puzzles सहित। यह एक clever objective है। आप working code लेते हैं, एक feature delete करते हैं, और model से इसे reconstruct करने की demand करते हैं। Ground truth exact है, difficulty tunable है, और यह model को codebase के एक साथ fit होने के बारे में reason करने पर मजबूर करता है, snippet को pattern-match करने के बजाय।

[ALLOY]: सिंथेटिक टास्क जेनरेशन इसीलिए है ताकि आपको एक कोडिंग एजेंट को ट्रेन करने के लिए पर्याप्त वॉल्यूम और डिफिकल्टी कवरेज मिल सके, बिना इस बात पर बॉटलनेक हुए कि स्केसर्ड रियल-वर्ल्ड टास्क में क्लीन रिवॉर्ड सिग्नल मिलते हैं। रीबिल्ड-पज़ल फ्रेमिंग अच्छी है क्योंकि इसमें एक स्पष्ट करेक्टनेस चेक है, जो कि रीन्फोर्समेंट लर्निंग को रिवॉर्ड हैकिंग से बचने के लिए चाहिए। एक अस्पष्ट रिवॉर्ड को गेम किया जाता है; एक रीबिल्ड-एक्जैक्टली रिवॉर्ड को नहीं।

[NOVA]: तीसरी शिफ्ट: MoE-स्केल ट्रेनिंग इन्फ्रास्ट्रक्चर। Cursor शार्डेड Muon ऑप्टिमाइज़र्स और ड्यूल-मेश HSDP का हवाला देता है। उसके नीचे का डीटेल यह है कि मिक्सचर-ऑफ-एक्सपर्ट्स ट्रेनिंग को स्केल पर ऑप्टिमाइज़र स्टेट और पैरेललिज़्म लेआउट को ध्यान से शार्ड करना चाहिए, वरना मेमोरी और कम्युनिकेशन कॉस्ट डॉमिनेट करते हैं। यह इन्फ्रास्ट्रक्चर का काम है, लेकिन यही बाकी चीज़ों की ट्रेनिंग इकोनॉमिक्स को फीज़िबल बनाता है।

[ALLOY]: और चौथा डीटेल, जो मुझे लगता है कि बिल्डर्स को स्किम नहीं करना चाहिए, यह है कि रीन्फोर्समेंट लर्निंग असली Cursor सेशन्स के अंदर रन की गई थी, उसी हैरनेस का उपयोग करके जो डिप्लॉयड मॉडल उपयोग करता है। हैरनेस-फेथफुल ट्रेनिंग।

[NOVA]: बताओ कि यह उन सभी के लिए लोड-बेयरिंग क्यों है जो एजेंट्स शिप करते हैं। एक कोडिंग एजेंट का बिहेवियर उसके वेट्स जितना ही उसके हैरनेस से शेप होता है। टूल्स मॉडल को कैसे प्रेजेंट किए जाते हैं, एरर्स वापस कैसे आते हैं, कॉन्टेक्स्ट कैसे ट्रिम होता है, रेट्राईज़ कैसे हैंडल होते हैं, लूप कैसे स्ट्रक्चर्ड होता है। अगर आप मॉडल को एक हैरनेस में ट्रेन करते हो और दूसरे में शिप करते हो, तो आप डिस्ट्रिब्यूशन शिफ्ट इंट्रोड्यूस करते हो। सिम्पटम यह है कि एक मॉडल जो बेंचमार्क में अच्छा परफॉर्म करता है प्रोडक्शन में वो फील करता है जैसे नंबर्स ने प्रॉमिस किया था।

[ALLOY]: डिप्लॉयड हैरनेस के अंदर रीन्फोर्समेंट लर्निंग रन करने से यह गैप क्लोज़ होता है। मॉडल को असली इंटरफेस सीखने को मिलता है जिसका वो सामना करेगा, कोई आइडियलाइज़्ड ट्रेनिंग स्टैंड-इन नहीं। जिसके भी एक एजेंट शिप की है और उसे अपने इवैल्यूएशन से कम परफॉर्म करते देखा है, यह एक बहुत कॉमन बिल्डर फेलियर पर सीधा अटैक है।

[NOVA]: जो हमें टेकअवे तक लाता है, और यह ज्यादातर इकोनॉमिक्स के बारे में है और कि यह डिफ़ॉल्ट में आप क्या डिप्लॉय करते हैं बदलता है। जब एक मॉडल फ्रंटियर-एडजेसेंट कोडिंग परफॉर्मेंस पर पहुंचता है लगभग दसवें हिस्से में पर-टोकन कॉस्ट पर, तो कई लॉन्ग ऑटोनॉमस सेशन्स रन करने का मैथ बदल जाता है। वो काम जो केवल कुछ हाई-वैल्यू टास्क्स के लिए एक्सपेंसिव मॉडल को जस्टिफाई करता था, वो रूटीन एजेंट वर्क के लिए डिफ़ॉल्ट बन सकता है।

[ALLOY]: लेकिन, और यह अहम चेतावनी है, बेंचमार्क पैरिटी वर्कफ़्लो पैरिटी नहीं है। Terminal-Bench और SWE-Bench कुछ असली चीज़ मापते हैं, लेकिन वो आपके टास्क डिस्ट्रिब्यूशन, आपके टूल्स, आपके कॉन्टेक्स्ट साइज़ेस, या मॉडल के बारे में आपके हैरनेस में जेनेरिकली लॉन्ग सेशन में कैसा बिहेव करता है, ये नहीं मापते। सही मूव एक कंट्रोल्ड कम्पेरिज़न है आपके खुद के असली काम पर, बेंचमार्क-टेबल स्वैप नहीं।

[NOVA]: कंक्रीटली बताते हैं, यहां इवैल्यूएट करने के लिए बिल्डर पैटर्न है। अपने प्रोडक्शन में असल में रन करने वाले लॉन्ग-हॉराइज़न कोडिंग टास्क्स का एक रिप्रेजेंटेटिव सैम्पल लो। उन्हें अपने एक्सिस्टिंग मॉडल से और अपने वेंडर के हैरनेस में नहीं, अपने हैरनेस में Composer 2.5 से रन करो। सिर्फ पास रेट ही नहीं कंपेयर करो बल्कि पर-कम्प्लीटेड टास्क कॉस्ट, टूल कॉल्स की नंबर, फेलियर पर रिकवरी बिहेवियर, और सेशन के लंबा होने पर क्वालिटी कैसे डिग्रेड होती है।

[ALLOY]: वो लास्ट वाला, लॉन्ग-सेशन डिग्रेडेशन, वो यूज़-केस है जिसे बेंचमार्क्स सिस्टमैटिकली अंडर-टेस्ट करते हैं। ज्यादातर बेंचमार्क टास्क्स रियल एजेंट रन की तुलना में छोटे होते हैं। अगर आप एजेंट्स डिप्लॉय करते हैं जो एक घंटे के लिए काम करते हैं, तो आपको सिंगल-शॉट पास रेट की परवाह कम है और ज्यादा इस बात की कि मॉडल टूल कॉल नंबर दो सौ पर अभी भी कॉम्प्लीटली कोहेरेंट है। इसे डेलिबरेटली कम्पेरिज़न में बिल्ड करो।

[NOVA]: कॉस्ट एडवांटेज़ इतना असली है कि अगर यह आपके डिस्ट्रिब्यूशन पर बना रहता है, तो यह रूटीन एजेंट वर्क के लिए आपके डिफ़ॉल्ट मॉडल को बदल देता है। अगर नहीं, तो आपने अपने वर्कलोड के बारे में कुछ स्पेसिफिक सीखा है टेबल पर भरोसा करने की जगह। दोनों आउटकम उपयोगी हैं; गलत मूव है हैडलाइन के आधार पर स्वैप करना और प्रोडक्शन में गैप डिस्कवर करना।

[NOVA]: चलिए लागत गणना में एक स्तर और गहराई में जाते हैं, क्योंकि यहीं पर यह निर्णय-प्रासंगिक हो जाती है। प्रति-टोकन मूल्य का दसवां हिस्सा इसका मतलब यह नहीं है कि किसी कार्य की लागत भी दसवां हिस्सा है। एजेंट निश्चित-टोकन नहीं होते; एक कमज़ोर मॉडल एक ही काम को पूरा करने के लिए ज़्यादा टूल कॉल, ज़्यादा पुनः प्रयास, और ज़्यादा टोकन ले सकता है, या उसमें विफल हो सकता है और किसी महंगे मॉडल पर वापस जाने पर मजबूर कर सकता है। इसलिए किसी बिल्डर के लिए जो मीट्रिक मायने रखती है वह प्रति पूर्ण कार्य की पूर्ण-भारित लागत है, जिसमें वे विफलताएं शामिल हैं जो वापस जाती हैं, प्रति दस लाख टोकन का मुखौटा मूल्य नहीं।

[ALLOY]: यह मूल्यांकन को फिर से परिभाषित करता है। अगर Composer 2.5 आपके कार्यों को आपके मौजूदा मॉडल के समान तुलनीय संख्या में चरणों में पूरा करता है, तो मूल्य लाभ लगभग सीधे आपके बिल में जाता है, और यह किसी भी व्यक्ति के लिए बड़ा बदलाव है जो एजेंटों को बड़े पैमाने पर चलाता है। अगर इसमें काफी ज़्यादा चरण लगते हैं या यह ज़्यादा बार विफल होता है और वापस जाता है, तो प्रभावी अंतर कम हो जाता है। आप बिना अपना स्वयं का वितरण चलाए नहीं जान सकते कि कौन-सा है, और यही कारण है कि बेंचमार्क टेबल सवाल की शुरुआत है, जवाब नहीं।

[NOVA]: इससे सक्षम एक परिनियोजन पैटर्न भी है जिसके बारे में बात करना उचित है: टियर्ड रूटिंग। सामान्य एजेंट कार्य के लिए सस्ते मॉडल को डिफ़ॉल्ट के रूप में उपयोग करें, और केवल तब फ्रंटियर मॉडल पर जाएं जब सस्ता वाला किसी जाँच में विफल हो या किसी विश्वास सीमा को हिट करे। जो मॉडल दसवें हिस्से की लागत पर फ्रंटियर-इतना पास है, वह एक बहुत अच्छा डिफ़ॉल्ट टियर है, क्योंकि जिन मामलों में यह पर्याप्त नहीं है, वे बिल्कुल वे मामले हैं जिनके लिए आपकी एस्केलेशन पथ है।

[ALLOY]: और प्रशिक्षण के नीचे इन्फ्रास्ट्रक्चर विवरण, शार्डेड म्यूऑन ऑप्टिमाइज़र और ड्यूल-मेश HSDP, बिल्डर्स के लिए केवल अप्रत्यक्ष रूप से प्रासंगिक है, लेकिन यह वह प्रासंगिक अप्रत्यक्षता है: यह कारण है कि यह मूल्य बिंदु इस गुणवत्ता पर संभव है। मिक्सचर-ऑफ-एक्सपर्ट्स का कुशल प्रशिक्षण वह है जो एक लैब को सर्विंग लागत के अंश पर फ्रंटियर-इतना पास आंकड़े पोस्ट करने देता है। अर्थशास्त्र जो आपको दिया जा रहा है वह उस इन्फ्रास्ट्रक्चर कार्य का अधोगामी है, और इसीलिए मूल्य कोई अस्थायी लॉस-लीडर नहीं है जिसे आप मान लें कि गायब हो जाएगा।

[ALLOY]: और इस हार्नेस-फिडेलिटी पॉइंट को याद रखें जब आप किसी भी मॉडल के बेंचमार्क पढ़ते हैं, सिर्फ इसके नहीं। लैब के हार्नेस में उत्पादित संख्या आपके हार्नेस में आप जो देखेंगे उसकी एक ऊपरी सीमा है, जब तक कि आपका हार्नेस उनके से मेल नहीं खाता। इन दोनों के बीच का अंतर वहीं है जहाँ अधिकांश 'मॉडल बिगड़ गया जब हमने इसे तैनात किया' की कहानियां वास्तव में रहती हैं। अपने हार्नेस को मॉडल का हिस्सा मानें। ...

[NOVA]: तीसरी कहानी Anthropic का स्टेनलेस का अधिग्रहण है, जिसकी घोषणा 18 मई को हुई थी। स्टेनलेस एक डेवलपर-टूल्स कंपनी है जिसकी सेवा एक API विशिष्टता को Python, TypeScript, Go, Kotlin, और Java में प्रोडक्शन-तैयार, ऑटो-मेंटेनेड SDK में बदलती है। इसका उपयोग AI लैब और इन्फ्रास्ट्रक्चर कंपनियों की एक लंबी सूची द्वारा किया जाता था। एंथ्रोपिक SDK जनरेटर सहित होस्टेड स्टेनलेस उत्पादों को बंद करने की योजना बना रही है। मौजूदा ग्राहक पहले से जनरेट किए गए SDK रखेंगे, लेकिन होस्टेड सेवा तक भविष्य की पहुँच खो देंगे।

[ALLOY]: सतह पर यह एक अधिग्रहण शीर्षक की तरह पढ़ता है। कारण यह एक एजेंट-स्टैक कहानी है वह यह है कि एक SDK वास्तव में एक एजेंट सिस्टम के अंदर क्या है। इसे विस्तार से बताएं, क्योंकि इसे आसानी से टालना आसान है।

[NOVA]: एक SDK वह टाइप की गई सीमा है जिसे एक एजेंट हर बार किसी बाहरी API को कॉल करते समय पार करता है। जब एक एजेंट किसी टूल को इनवोक करता है जो किसी सेवा को रैप करता है, तो उस कॉल की सहीपन पूरी तरह इस बात पर निर्भर करता है कि क्लाइंट लाइव API से मेल खाता है या नहीं। सही एंडपॉइंट। सही रिक्वेस्ट और रिस्पॉन्स शेप। सही एरर टाइप। सही पेजिनेशन और रिट्री व्यवहार। SDK API के आसपास की कोई सुविधा परत नहीं है। एक एजेंट के लिए, यह अनुबंध है।

[ALLOY]: इसलिए एक पाइपलाइन जो किसी विशिष्टता को उस क्लाइंट में बदलती है, और जैसे-जैसे विशिष्टता बदलती है उसे सिंक में रखती है, वह इन्फ्रास्ट्रक्चर है जो सीधे एजेंट की टूल लेयर के नीचे बैठा है। यह कोई गौण चिंता नहीं है। किसी के लिए भी जो एजेंट बनाता है जो बाहरी सेवाओं को छूती हैं, यह भार-वहन है।

[NOVA]: और यह उस फेलियर मोड की ओर इशारा करता है जिसे समझना उचित है: spec-to-SDK drift। मान लें कि API विशिष्टता बदलती है, लेकिन जनरेट किया गया क्लाइंट अपडेट नहीं होता। अब आपके पास एक क्लाइंट है जो कंपाइल होता है, सही दिखता है, और चुपचाप लाइव API से मेल नहीं खाता। कोई फ़ील्ड हिल गया। कोई enum एक वैल्यू प्राप्त कर गया। कोई एंडपॉइंट अपना पेजिनेशन बदल गया।

[ALLOY]: एक मानव डेवलपर के लिए यह एक बग रिपोर्ट के रूप में सामने आता है और कोई इसे जांचता है। एक स्वायत्त एजेंट के लिए यह एक टूल कॉल के रूप में सामने आता है जो कुछ ऐसा रिटर्न करता है जो एजेंट ने उम्मीद नहीं की थी। और एजेंट वहां नहीं रुकता। यह अप्रत्याशित परिणाम के बारे में तर्क करता है, अक्सर गलत तरीके से, और त्रुटि जो भी एजेंट अगला करता है उसमें फैल जाती है। एक ड्रिफ्टेड क्लाइंट खुद को घोषित नहीं करता। यह बस एजेंट को चुपचाप गलत बना देता है, जो शिप करने के बाद डिबग करने का सबसे महंगा प्रकार का गलत है।

[NOVA]: यही वही समस्या है जिसे स्वचालित, स्पेक-संचालित SDK जेनरेशन हल करने के लिए मौजूद है: बिना हर क्लाइंट को मैन्युअल रूप से बनाए रखे कई भाषाओं में टाइप्ड बाउंड्री को ईमानदार रखें। हैंड-रिटन मल्टी-लैंग्वेज क्लाइंट ड्रिफ्ट करते हैं क्योंकि मनुष्य पांच भाषा SDK को एक गतिशील स्पेसिफिकेशन के साथ पूरी तरह सिंक में नहीं रख सकते। स्पेसिफिकेशन से जेनरेशन ही वह तरीका है जिससे आप बाउंड्री को एजेंट को उसके ऊपर तैनात करने के लिए काफी भरोसेमंद बनाते हैं।

[ALLOY]: तो जिन टीमों ने होस्टेड जेनरेटर पर निर्भरता की, व्यावहारिक सवाल यह है कि उसे क्या बदलता है। तीन व्यापक विकल्प हैं, प्रत्येक के ट्रेड-ऑफ हैं, और चुनना खुद एक बिल्डर निर्णय है। एक: ओपन-सोर्स OpenAPI जेनरेटर। आप स्पेक-संचालित जेनरेशन रखते हैं, लेकिन आप टूलचेन के मालिक हैं और इसकी टाइप फिडेलिटी अलग-अलग होती है। दो: वेंडर-पब्लिश्ड SDK। कम मेंटेनेंस, लेकिन आप वेंडर की रिलीज कैडेंस और भाषा कवरेज पर निर्भर हैं।

[NOVA]: तीन, और यह एजेंट बिल्डर्स के लिए सबसे प्रासंगिक है: API को एक टूल लेयर के पीछे रैप करें, जैसे MCP सर्वर, ताकि एजेंट एक पुनर्जनित क्लाइंट के बजाय एक स्थिर आंतरिक कॉन्ट्रैक्ट से बात करे। यह ड्रिफ्ट समस्या को एक नियंत्रित जगह पर ले जाता है जिसे आप संचालित करते हैं। एजेंट एक स्थिर टूल इंटरफ़ेस देखता है; MCP सर्वर अंतर्निहित API में बदलावों को अवशोषित करता है। यह सेट अप करने में अधिक काम है, लेकिन यह आपको प्रत्येक क्लाइंट में बिखरे ड्रिफ्ट के बजाय प्रबंधित करने के लिए एक सिंगल सीम देता है जिसे आपके एजेंट उपयोग करते हैं।

[ALLOY]: प्रत्येक विकल्प टाइप फिडेलिटी, मेंटेनेंस बोझ, और स्पेसिफिकेशन बदलाव कितनी जल्दी एजेंट तक पहुंचते हैं, इसमें ट्रेड-ऑफ करता है। यहां कोई मुफ्त विकल्प नहीं है, लेकिन एक गलत है, जो निर्णय नहीं लेना है और एजेंटों के उसके ऊपर तैनात करते रहने के दौरान एक अनमेंटेन्ड जेनरेटेड क्लाइंट को धीरे-धीरे ड्रिफ्ट होने देता है।

[NOVA]: एक व्यापक बिंदु भी है, किसी एक टीम के माइग्रेशन से परे। यह सप्लाई कंसंट्रेशन है। जब एक मॉडल लैब एक कोड-जेनरेशन डिपेंडेंसी का मालिक है जिस पर प्रतिस्पर्धी लैब और इन्फ्रास्ट्रक्चर प्रोवाइडर बना रहे थे, तो यह उद्योग भर में कई एजेंट टूल क्लाइंट्स के नीचे बैठा एक रणनीतिक और तकनीकी जोखिम का एकल बिंदु है।

[ALLOY]: यह जानना लायक है, ठीक से, कि आपका टूल-क्लाइंट जेनरेशन कहां से आता है, कौन इसे नियंत्रित करता है, और यदि वह नियंत्रण बदलता है तो आपका फॉलबैक क्या है। यह एक एकीकरण विवरण था जिसे आप अनदेखा कर सकते थे। एजेंट सिस्टम के लिए, जहां SDK टूल बाउंड्री है, यह एक जोखिम प्रोफाइल वाला आर्किटेक्चर निर्णय है, और यह उसी समीक्षा में है जो आप तैनात करते हैं किसी अन्य महत्वपूर्ण डिपेंडेंसी पर।

[NOVA]: इससे उभरने वाला बिल्डर पैटर्न स्पेक-टू-क्लाइंट पाथ को मॉनिटर्ड इन्फ्रास्ट्रक्चर के रूप में व्यवहार करना है। उस स्पेक वर्शन को पिन करें जिससे आपके क्लाइंट जेनरेट हुए थे। इसे शेड्यूल पर लाइव स्पेक के विरुद्ध डिफ करें। ड्रिफ्ट को एक अलर्ट के रूप में मानें, न कि एक खोज के रूप में जो आप तब करते हैं जब कोई एजेंट प्रोडक्शन में अजीब व्यवहार करना शुरू करता है। यह एक मौन विफलता मोड को एक दृश्यमान में बदल देता है जिस पर आप शिप करने से पहले कार्य कर सकते हैं।

[ALLOY]: सारांश यह है कि यह सतह क्षेत्र में छोटा है और निहितार्थ में बड़ा है। SDK जेनरेशन को इन-हाउस लाना अधिग्रहणकर्ता के लिए एक सुदृढ़ कदम है। इन API के ऊपर एजेंट बनाने वाले सभी के लिए, यह स्पेक-टू-क्लाइंट ड्रिफ्ट को प्राथमिक एजेंट विफलता मोड के रूप में व्यवहार करने, इसे जरूरत पड़ने से पहले अपना फॉलबैक जानने, और ड्रिफ्ट डिटेक्शन को अपने संचालन में वायर करने का संकेत है। ...

[ALLOY]: Notion ने 13 मई को अपना डेवलपर प्लेटफॉर्म लॉन्च किया, और बिल्डर्स के लिए मायने रखने वाला फ्रेमिंग एजेंटों द्वारा पढ़ी जाने वाली वर्कस्पेस से एजेंटों द्वारा चलाई जाने वाली वर्कस्पेस में बदलाव है। पांच ठोस टुकड़े हैं। Workers, एक होस्टेड कोड सैंडबॉक्स जिसमें प्रोविजन करने के लिए कोई सर्वर नहीं है। एक External Agent API। डेटाबेस सिंक। बाइडायरेक्शनल वेबहुक। और ऑथ, डिप्लॉय और ऑटोमेशन के लिए एक कमांड-लाइन टूल।

[NOVA]: Workers से शुरू करते हैं, क्योंकि hosted code runtimes वही load-bearing idea हैं। आप logic लिखते हैं, इसे managed sandbox पर deploy करते हैं, और यह बिना किसी infrastructure operate किए live हो जाता है। एक agent builder के लिए, यह वो जगह है जहाँ आप workflow के deterministic parts को उस data के बगल में रख सकते हैं जिस पर वो act करते हैं, इसके बजाय कि हर integration के लिए अपना खुद का service setup और देखभाल करें।

[ALLOY]: और इसके साथ जो चीज जुड़ती है वो हैं deterministic Worker tools। LLM-mediated tool call की जगह, एक custom agent एक Worker को invoke करता है जो predictable code token-efficient execution के साथ run करता है। यह distinction वो है जो समझना जरूरी है। Model-mediated tool call flexible है लेकिन probabilistic। एक Worker tool deterministic है। Build pattern यह है कि model का use judgment के लिए करें और Worker का use उन steps के लिए करें जो हर बार exact होने चाहिए।

[NOVA]: External Agent API multi-vendor surface है। यह third-party agents को workspace में first-class participants बनाती है, named ones Claude Code, Cursor, और Codex हैं, bolt-on integrations की जगह। एक builder के लिए इसका मतलब है कि आपको workspace-native behavior पाने के लिए किसी एक vendor के agent में नहीं फंसना पड़ा; आप वो agent ला सकते हैं जो आप पहले से deploy करते हैं।

[ALLOY]: Database sync और bidirectional webhooks loop पूरा करते हैं। Sync बिना manage करने के infrastructure के external system of record को workspace में fresh रखता है। Webhooks किसी भी app को एक Worker trigger करने देते हैं, जो logic run करता है और workspace में वापस act करता है या दूसरे APIs call करता है। यह event-driven agent trigger है, जो production में आमतौर पर वो चीज है जो आपको actually चाहिए, polling की जगह।

[NOVA]: Tradeoff जिसके बारे में सोचना है, और यह important one है, वो है trust boundary। Real company data रखने वाले workspace के अंदर third-party agents और custom code run करना मतलब governance model load-bearing work कर रहा है। Notion का जवाब है progressive trust, optional human review, sandboxed execution, और agent activity पर unified visibility। एक builder को उस boundary को एक inherited default की जगह deliberately design करने चीज के रूप में treat करना चाहिए, क्योंकि यहाँ एक misbehaving agent का blast radius आपकी company's actual operational data है।

[ALLOY]: तो builder takeaway यह है कि यह real agent runtime है, plugin surface नहीं। Deterministic Workers use करें exact steps के लिए, External Agent API अपने existing agent को रखने के लिए use करें, event webhooks work trigger करने के लिए use करें, और trust boundary पर deliberate thought लगाएं कुछ भी deploy करने से पहले जो write कर सकता है।

[NOVA]: Vercel AI SDK ने अपने LangChain और LangGraph adapter को rewrite किया है, और इसलिए यह एक package note से ज्यादा है क्योंकि लगभग कोई एक framework end to end नहीं चलाता। आप एक stack में prototype करते हैं और दूसरे में deploy करते हैं, और जहाँ break होता है वो है message format और stream format interop। Frameworks के बीच hand-written glue वही जगह है जहाँ mixed stacks खराब होते हैं।

[ALLOY]: New adapter इसमें concrete है। एक function है AI SDK message objects को LangChain base-message format में convert करने के लिए, और दूसरा model-message conversion से गुजर चुके messages के लिए। एक function है जो LangChain model streams, LangGraph output, और granular stream-events results को AI SDK के UI message stream में transform करता है। और एक transport है जो browser client को सीधे LangSmith या LangGraph deployment से connect करता है।

[NOVA]: Stream normalization पहले लेते हैं, क्योंकि streaming वही जगह है जहाँ interop आमतौर पर quietly fail होती है। एक framework पर built agent अपने own shape में events emit करता है। दूसरे framework पर built UI एक different shape expect करता है। अगर bridge lossy है, तो आप tool-call boundaries, intermediate steps, या token-level updates खो देते हैं, और UI spinner तक degrade हो जाता है। LangGraph output और granular stream events को एक UI stream format में normalize करने से front end एक agent render कर सकता है जिसे उसने author नहीं किया, बिना custom translation layer के।

[ALLOY]: Transport piece दूसरा real reduction in moving parts है। एक chat transport जो सीधे browser से deployed graph से बात करती है वो custom backend route हटा देती है जो teams आमतौर पर सिर्फ UI और LangGraph deployment के बीच proxy करने के लिए लिखती हैं। Fewer hops, less bespoke glue, operate करने की एक चीज कम।

[NOVA]: यहाँ builder का नज़रिया यह है कि interop इन्फ्रास्ट्रक्चर है, convenience नहीं। अगर आप मिक्स्ड स्टैक में agents बनाते हैं, तो frameworks के बीच adapter कोई nice-to-have नहीं है। यह वो seam है जो तय करता है कि आपका stack coherent रहेगा या one-off connectors में टूट जाएगा जो अपनी-अपनी गति से सड़ेंगे। एक maintained, typed bridge जिसमें proper stream और event handling है, वही चीज़ है जो आपको per layer best framework चुनने देती है, बजाय इसके कि आप एक में lock हो जाओ।

[ALLOY]: और observability का पहलू बताने लायक है। Granular stream events का साफ़-सुथरे तरीके से बहना मतलब आप अपने UI और tooling में किसी दूसरे framework पर बने agent के intermediate steps देख सकते हैं। Long agent runs को debug करने के लिए, यह visibility अक्सर fixable problem और black box के बीच का फ़र्क होती है। ...

[ALLOY]: आखिरी कहानी Cloudflare Mesh की है, Cloudflare के agent-cloud push का हिस्सा, जो zero-trust private networking और identity को agents के services और एक-दूसरे तक पहुँचने के तरीके पर लागू करता है। इसके साथ कुछ dated developer-tooling बदलाव भी हैं, जैसे key-value-backed durable objects के लिए legacy remote-dev flag का May 18 को हटाया जाना, जो कि छोटे parity change में से एक है जो चुपचाप तय करता है कि कोई agent development और production में एक जैसा व्यवहार करता है या नहीं।

[NOVA]: Builders के लिए framing यह shift है कि agents कहाँ run करते हैं। जब एक agent एक laptop पर एक process था, network एक implementation detail था। जब यह कई sandboxed workers है जो internal और external services को call करते हैं, उनके बीच network एक साथ attack surface और policy boundary दोनों बन जाता है। यही problem है जिसके लिए identity वाला mesh बनाया गया है।

[ALLOY]: Concrete principle यह है कि per-agent identity और scoped credentials, shared ambient keys की जगह। अगर हर agent एक broad key share करता है, तो एक compromised या misbehaving agent की blast radius पूरी key जितनी हो जाती है। अगर हर agent की अपनी identity है जिसमें scoped permissions हैं, तो network policy उस identity से attach हो सकती है, और आप बिल्कुल स्पष्ट बता सकते हैं कि एक agent क्या-क्या reach करने की अनुमति रखता है।

[NOVA]: और उस policy को lifecycle के साथ चलना चाहिए। एक agent spawn होता है, act करता है, और retire होता है। अगर credentials और network reach spawn पर broadly दिए जाते हैं और कभी scoped down नहीं किए जाते, तो एक long-running या detached agent वह access accumulate कर लेता है जिसकी उसे ज़रूरत नहीं है। Policy को identity के साथ spawn-act-retire path पर attach करना यही तरीका है जिससे आप agent के network reach को उसके actual current work के साथ match रखते हैं।

[ALLOY]: durable-object dev-parity detail छोटा है लेकिन यही theme है। Stateful workers के लिए local-versus-remote behavior का match करना ज़रूरी है, नहीं तो आपको एक agent मिलता है जो development में pass करता है लेकिन production में fail होता है किसी logic से जुड़े कारणों की वजह से नहीं। State और networking layer में parity, agent behavior को reproducible बनाने का हिस्सा है।

[NOVA]: Builder recommendation सीधा है। Agent network को identity और scoped policy के साथ डिज़ाइन करने वाली चीज़ की तरह treat करो, नहीं कि agents को broad ambient access inherit करने दो। जब आप एक local process से sandboxed workers की fleet में जाते हैं, तो network policy agent की security posture का हिस्सा है, वो infrastructure नहीं जिसे आप defer कर सकते हैं। ...

[ALLOY]: चलो इसे actual क्या करना है पर land करते हैं। छह moves, छह concrete builder priorities।

[NOVA]: Claude Code के लिए, 2.1.144 install करो और changed surfaces को directly validate करो, उन पर assumption मत बनाओ। एक background session detach करो, wake करो, respawn करो, और resume करो और confirm करो कि वह right model बनाए रखता है। इसे एक MCP server की तरफ point करो जो अपने tool list को paginate करता है और confirm करो कि पूरा set visible है। एक unsupported image type को एक MCP tool में से feed करो। इसे degraded network पर run करो और confirm करो कि startup अब नहीं रुकता। एक maintenance release तभי payoff देता है जब आप verify करते हैं कि removed failures वही थीं जो आपके deployed agents को hit कर रही थीं।

[ALLOY]: मॉडल चयन के लिए, Composer 2.5 को अपने खुद के हार्नेस में, अपने लंबे-सत्र कार्यों पर बेंचमार्क करने के लिए उम्मीदवार के रूप में मानें, ड्रॉप-इन के रूप में नहीं। पूर्ण-लोडेड लागत प्रति पूर्ण कार्य और लंबे-सत्र में गिरावट की तुलना करें, केवल हेडलाइन पास दरों के बजाय, और एक सस्ता-डिफ़ॉल्ट-फ्रंटियर-एस्केलेशन रूटिंग पैटर्न पर विचार करें अगर यह आपके वितरण पर काम करता है।

[NOVA]: टूल क्लाइंट्स के लिए, अपने SDK या क्लाइंट जनरेशन के स्रोत की जांच करें। अगर आपने किसी होस्टेड जनरेटर पर निर्भरता थी जो बंद हो रहा है, तो अभी OpenAPI जनरेटर्स, वेंडर SDKs, या MCP सर्वर जैसे स्थिर आंतरिक कॉन्ट्रैक्ट के पीछे API रैपिंग में से चुनें, और स्पेसिफिकेशन को पिन करें और डिफ करें ताकि ड्रिफ्ट एक अलर्ट बने, प्रोडक्शन सरप्राइज नहीं।

[ALLOY]: वर्कस्पेस एजेंट्स के लिए, Notion के External Agent API को मल्टी-वेंडर सतह के रूप में मानें ताकि आप जो एजेंट पहले से डिप्लॉय करते हैं वो रख सकें, सटीक कदमों के लिए डिटरमिनिस्टिक Workers का उपयोग करें, और ट्रस्ट बाउंड्री डिज़ाइन करें इससे पहले कि आप कुछ भी लिखने दें।

[NOVA]: मिक्स्ड स्टैक्स के लिए, पुनर्लिखे गए Vercel एडॉप्टर का उपयोग करें LangGraph और AI SDK को उचित स्ट्रीम और इवेंट हैंडलिंग के साथ जोड़ने के लिए, हाथ से कनेक्टर बनाने के बजाय जो खराब हो जाते हैं। और एजेंट नेटवर्किंग के लिए, ब्रॉड एम्बिएंट एक्सेस पर निर्भर रहने के बजाय spawn-act-retire लाइफसाइकल में प्रति-एजेंट आइडेंटिटी और स्कोप्ड पॉलिसी अटैच करें।

[ALLOY]: इन सभी छह बिंदुओं में से गुजरने वाला थ्रेड वही ऑपरेशनल मैच्योरिटी है। रनटाइम अनएटेंडेड-सत्र सतह को हार्डन कर रहा है जो बिल्डर्स डिप्लॉय करते हैं। मॉडल लेयर फ्रंटियर-एडजेसेंट कोडिंग को इतना सस्ता बना रहा है कि डिफ़ॉल्ट बदल सकें। और टूलिंग, वर्कस्पेस, इंटरॉप, और नेटवर्क लेयर्स सभी कंसोलिडेट हो रही हैं, जो एजेंट और जो कुछ भी वो छूता है उसके बीच की बाउंड्रीज को इनहेरिट करने के बजाय जानबूझकर मालिकाना हक रखने वाली चीजें बनाती हैं।

[NOVA]: यही काम एजेंट्स को शिप करना, डिबग करना और भरोसा करना आसान बनाता है। कम स्पेक्टेकल, ज़्यादा रिलायबिलिटी। यहीं वास्तविक प्रगति होती है, और यही वास्तव में बदलती है कि आप कैसे बिल्ड करते हैं।

[ALLOY]: सोर्स लिंक्स और एपिसोड नोट्स Toby On Fitness Tech dot com पर उपलब्ध हैं।

[NOVA]: यही AgentStack Daily है। मैं NOVA हूं।

[ALLOY]: और मैं ALLOY हूं। हम जल्द वापस आएंगे।