# EP020 — The Infrastructure Release

**OpenClaw Daily** | 1 अप्रैल, 2026 | ~32 मिनट

इस हफ्ते OpenClaw एक चतुर टूल से इन्फ्रास्ट्रक्चर बन गया। पांच कहानियां जो बताती हैं कि यह कैसे हुआ — और इसका मतलब उन सभी के लिए क्या है जो इसके ऊपर बना रहे हैं।

---

## इस एपिसोड की कहानियां

### 1. OpenClaw v2026.3.31 — द प्लेटफॉर्म रिलीज़
पिछले महीनों की सबसे अहम OpenClaw अपडेट। मुख्य बदलाव:
- **बैकग्राउंड टास्क कंट्रोल प्लेन** — ACP, सबएजेंट्स, क्रॉन, और बैकग्राउंड CLI एक्जीक्यूशन को `openclaw flows list|show|cancel` के साथ एक SQLite-बैक्ड लेजर में मिलाया गया
- **प्लगइन सिक्योरिटी डिफ़ॉल्ट रूप से बंद** — खतरनाक-कोड की क्रिटिकल खोजें अब इंस्टॉल को ब्लॉक करती हैं; ओवरराइड करने के लिए `--dangerously-force-unsafe-install` जरूरी
- **नोड पेयरिंग बनाम अप्रूवल अलग किए गए** — नोड कमांड तब तक डिसेबल रहेंगे जब तक पेयरिंग को स्पष्ट रूप से अप्रूव नहीं किया जाता (पेयरिंग अकेली काफी नहीं)
- **गेटवे ऑथ हार्डन किया** — ट्रस्टेड-प्रॉक्सी मिक्स्ड शेयर्ड-टोकन कॉन्फिग को रिजेक्ट करता है; लोकल-डायरेक्ट फॉलबैक के लिए कॉन्फिगर्ड टोकन जरूरी
- **QQ बॉट चैनल** — टेंसेंट के इकोसिस्टम में पहले-दर्जे का पाथ बंडल किया गया
- **Matrix स्ट्रीमिंग रिप्लाईज़** — आंशिक रिस्पॉन्स अब चैट में बाढ़ लाने के बजाय जगह पर अपडेट होते हैं
- **MCP रिमोट HTTP/SSE सपोर्ट** — रिमोट ट्रांसपोर्ट पर टूल सरफेस सर्व करें
- **Android नोटिफिकेशन फॉरवर्डिंग** — पैकेज फिल्टरिंग, क्वाइट आवर्स, रेट लिमिटिंग
- **आइडल-स्ट्रीम टाइमआउट** — अटके मॉडल स्ट्रीम अब साफ तरीके से खत्म होते हैं
- **ACPX MCP ब्रिज हार्डन किया** — स्पष्ट डिफ़ॉल्ट-ऑफ कॉन्फिग, डॉक्यूमेंटेड ट्रस्ट बाउंड्री
- ब्रेकिंग: `qwen-portal-auth` हटाया गया; 2 महीने से पुराने कॉन्फिग अब ऑटो-माइग्रेट नहीं होते

📎 [रिलीज़ नोट्स: openclaw/openclaw v2026.3.31](https://github.com/openclaw/openclaw/releases/tag/v2026.3.31)

---

### 2. OpenClaw का चाइना फ्रेंज़ी — और बीजिंग का जवाब
OpenClaw चीन में वायरल हो गया (चीनी टेक स्लैंग में "लॉबस्टर"), GitHub स्टार्स ने ब्रिफ्ली React को पीछे छोड़ दिया। Tencent ने पॉप-अप इंस्टॉल इवेंट्स होस्ट किए। फिर आए "लॉबस्टर विक्टिम्स" — उपयोगकर्ता जिन्होंने फाइलें खो दीं, बिल भर दिए, या संवेदनशील डेटा AI एजेंट्स को बिना गार्डरैल्स के एक्सपोज़ कर दिया। बीजिंग ने जवाब दिया — राज्य के स्वामित्व वाली कंपनियों के कर्मचारियों पर इस टूल का उपयोग करने पर प्रतिबंध लगा दिया।

📎 [The Wire China: How the OpenClaw Frenzy Is Testing China's AI Commitment](https://www.thewirechina.com/2026/03/29/how-the-openclaw-frenzy-is-testing-chinas-ai-commitment/)
📎 [PCWorld सिक्योरिटी वार्निंग: OpenClaw इंस्टॉल न करें](https://www.pcworld.com/article/3064874/openclaw-ai-is-going-viral-dont-install-it.html)

---

### 3. Microsoft 365 + OpenClaw — एंटरप्राइज़ वैलिडेशन
Microsoft OpenClaw को Microsoft 365 में सक्रिय रूप से इंटीग्रेट कर रहा है, जो इसके ~400 मिलियन एंटरप्राइज़ उपयोगकर्ताओं को पर्सनल AI एजेंट्स लाता है। यह OpenClaw को कॉर्पोरेट प्रोडक्टिविटी के लिए एजेंट लेयर के रूप में पोजीशन करता है — सिर्फ एक हॉबिस्ट टूल नहीं।

📎 [Windows Central: Microsoft's new OpenClaw AI agents for Microsoft 365](https://www.windowscentral.com/artificial-intelligence/microsoft-openclaw-will-add-personal-ai-agents-in-microsoft-365)

---

### 4. Perplexity Personal Computer — लोकल AI जो तुम्हारे साथ रहता है
Perplexity ने "Personal Computer" लॉन्च किया — एक Mac mini पर समर्पित AI एजेंट जो तुम्हारी लोकल फाइल्स और ऐप्स तक निरंतर, पर्सिस्टेंट एक्सेस के साथ रहता है। हमेशा ऑन, हमेशा कॉन्टेक्स्टुअली अवेयर, पूरी तरह से लोकल। कोई क्लाउड अपलोड जरूरी नहीं।

📎 [r/LocalLLaMA: Local-first agent stacks in 2026](https://www.reddit.com/r/LocalLLaMA/comments/1s6f15f/localfirst_agent_stacks_in_2026_whats_actually/)

---

### 5. $297 बिलियन का क्वार्टर
Q1 2026 ने हर वेंचर फंडिंग रिकॉर्ड तोड़ दिया। वैश्विक स्तर पर $297B निवेश, AI कंपनियों में 81%। चार सबसे बड़े राउंड: OpenAI ($120B), Anthropic ($30B), xAI ($20B), Waymo ($16B)। CoreWeave ने $8.5B का फाइनेंसिंग फैसिलिटी सिक्योर किया। Crunchbase यूनिकॉर्न बोर्ड ने एक ही क्वार्टर में $900B की वैल्यू जोड़ी।

📎 [Crunchbase: Q1 2026 Shatters Venture Funding Records](https://news.crunchbase.com/venture/record-breaking-funding-ai-global-q1-2026/)
📎 [TechFundingNews: CoreWeave lands $8.5B](https://techfundingnews.com/coreweave-lands-8-5b-wall-street-ai-cloud/)

---

## चैप्टर्स

`[00:00]` हुक — द प्लेटफॉर्म मोमेंट
`[02:30]` OpenClaw v2026.3.31 — जब एक टूल इन्फ्रास्ट्रक्चर बनता है
`[14:00]` OpenClaw का चाइना फ्रेंज़ी और स्टेट क्रैकडाउन
`[21:00]` Microsoft 365 इंटीग्रेशन — एंटरप्राइज़ वैलिडेशन या रिस्क नॉर्मलाइज़ेशन?
`[27:00]` Perplexity Personal Computer — लोकल AI जो तुम्हारे साथ रहता है
`[33:00]` $297 बिलियन का क्वार्टर — AI का सबसे बड़ा फंडिंग स्प्लैश
`[39:00]` आउट्रो — एजेंट्स एट द इन्फ्लेक्शन पॉइंट

---

## OpenClaw Daily ढूंढें

- 🌐 [tobyonfitnesstech.com/hi/podcasts/episode-20/](https://tobyonfitnesstech.com/hi/podcasts/episode-20/)
- 🎙️ Spotify · Apple Podcasts · Pocket Casts · Amazon Music · Overcast
- EN, ES, PT, HI, DE फीड्स उपलब्ध

→ Reply on Telegram to approve.
