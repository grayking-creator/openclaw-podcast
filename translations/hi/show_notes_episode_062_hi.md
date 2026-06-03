Codex `rust-v0.136.0` जून 1 के लिए EP062 में stable CLI release के रूप में अगुवाई करता है, इसके बाद Stanford के viral AI agent guidelines, OpenAI on AWS Bedrock, और एक YC-backed GPU efficiency project हैं। Project radar में hardware के लिए agent OS, terminal context files, और physical agent schedulers शामिल हैं।

[00:00] Opening: CLI releases, institutional guidelines, और cloud distribution
EP062 के लिए useful lane CLI tooling, institutional validation, और real-world infrastructure का मिश्रण है। Codex `rust-v0.136.0` वह stable release है जिसने TUI diagnostics, app-server lifecycle, hook scoping, और SDK improvements पर महत्वपूर्ण प्रगति की। Stanford की CS336 agent guidelines document अप्रत्याशित कहानी है — एक academic course जिसने AI agent conventions publish किए और 24 घंटों से कम में 1,863 stars हासिल किए, जो बताता है कि agents कैसे काम करने चाहिए इसका formalize करना art एक niche educational concern नहीं रहा। OpenAI का frontier models और Codex को AWS Bedrock पर रखना dual-lab Bedrock pattern को पूरा करता है जिस पर enterprise agent stacks भरोसा करने लगे हैं। Expanse from YC P26 एक specific और expensive problem solve करता है: predict करना कि एक job को actually कितने GPU की जरूरत है और उस task पर frontier models को 8x outperform करना real cluster telemetry पर training करके।

[03:00] Codex rust-v0.136.0 release deep dive
Codex `rust-v0.136.0` जून 1 की stable release है, और यह diagnostics और reliability wave है। सबसे operationally useful change `codex doctor` output में है — error messages में अब बेहतर location और cause information है, जो local agents के लिए मायने रखता है जहाँ failure shell environment, remote transport, app-server state, Git repo, या model खुद से आ सकती है। जब कुछ टूटता है, तो "something failed" और "thread inventory check timed out because remote transport did not recover from a network hiccup" के बीच का अंतर debugging और guessing के बीच का अंतर है।

App-server lifecycle handling tighter है। Server ज्यादा cleanly start और stop होता है, startup पर model selection provider configurations में ज्यादा reliable है, और temporary network issue के बाद remote transport connections जल्दी recover होते हैं। यह последняя point worth dwelling on है क्योंकि remote Codex work — मान लीजिए एक iPhone से Windows host supervise करना — तभी practical है अगर transport को WiFi hiccup से बिना full restart के recover करना पड़े। Release यह address करती है।

Hook configuration को named hooks और permission scopes मिलते हैं। पहले, एक operator जो एक ही hook behavior चाहता था multiple projects में, उसे hook configuration block को हर project file में copy करना पड़ता था। Named hooks आपको behavior एक बार define करने और उसे name से configurations में reference करने देते हैं। Permission scopes `/permissions` endpoint के लिए वही काम करते हैं — एक flat permission set की जगह, operators scopes define कर सकते हैं जो different trust levels या different project contexts represent करते हैं।

Python SDK और Node SDK दोनों को thread management, turn handling, और error propagation improvements मिलते हैं। Non-interactive installation `CODEX_NON_INTERACTIVE=1` के जरिए ज्यादा reliably काम करता है, जो उन teams के लिए मायने रखता है जो interactive install script के बजाय configuration management tool के जरिए Codex rollout करना चाहती हैं।

Upgrade recommendation straightforward है: किसी known failing configuration के खिलाफ `codex doctor` output test करें, एक named hook define करें जिसका आप projects में pattern के लिए उपयोग करते हैं, और verify करें कि non-interactive install आपके CI pipeline में काम करता है before इसे automated deployment के लिए rely करने पर।

[11:00] Stanford CS336 AI agent guidelines: जब institutional validation viral हो जाता है
Stanford का CS336 course — "Language Modeling from Scratch" — ने एक formal AI agent guidelines document publish किया जिसे GitHub community ने viral engineering resource के रूप में treat किया। Document cover करता है कि students कैसे tasks decompose करने चाहिए, tools use करने चाहिए, context manage करने चाहिए, outputs verify करने चाहिए, और academic setting में agent quality के बारे में reason करने चाहिए। यह 24 घंटों से कम में 1,863 stars पर पहुंचा, जो एक course assignment artifact के लिए unusually strong signal है।

कहानी यहाँ document के perfect या comprehensive होने के बारे में नहीं है। यह इस बारे में है कि community ने इसे देखा और इसे reference के रूप में treat किया, सिर्फ एक course sample नहीं। यह हमें बताता है कि industry कहाँ है: teams AGENTS.md files, CLAUDE.md files, और similar conventions लिख रही हैं, लेकिन वे इसे scratch से कर रही हैं और clear reference point के बिना। Stanford का document उन्हें एक देता है, भले ही यह academic context से आता है।

Practical move यह है कि इसे पढ़ें, conventions extract करें जो आपकी team पर apply होते हैं, और उन्हें अपने own AGENTS.md के लिए starting point के रूप में use करें। Format adaptable है — principles course context से beyond apply होते हैं — और यह MIT-licensed है means इसे freely foundation के रूप में use किया जा सकता है।

[18:00] OpenAI on AWS Bedrock: ड्यूल-लैब पैटर्न पूर्ण
OpenAI ने GPT-4.5, o-series मॉडल और Codex को AWS Bedrock के माध्यम से उपलब्ध कराया है। Anthropic का Claude पहले से ही Bedrock पर है। इसका मतलब है कि एंटरप्राइज एजेंट स्टैक अब एक ही AWS क्रेडेंशियल, एक ही VPC, एक ही IAM कंट्रोल और एक ही CloudWatch लॉगिंग के माध्यम से दोनों प्रमुख लैब के मॉडल provision कर सकते हैं।

OpenClaw, Hermes और Codex ऑपरेटरों के लिए इसका व्यावहारिक निहितार्थ सीधा है: मल्टी-लैब मॉडल रूटिंग एक कस्टम इंटीग्रेशन प्रोजेक्ट की जगह कॉन्फ़िगरेशन चॉइस बन जाती है। एक टीम जो प्लानिंग टास्क के लिए Claude और कोड जनरेशन के लिए OpenAI का उपयोग करना चाहती है, वह एक ही AWS अकाउंट में, एक ही क्रेडेंशियल रोटेशन और एक ही कंप्लायंस बाउंड्री के साथ ऐसा कर सकती है।

क्लाउड डिस्ट्रीब्यूशन पैटर्न ध्यान देने योग्य है: दोनों लैब ने पहले AWS को चुना। यह बताता है कि एंटरप्राइज AI स्पेंडिंग कहां केंद्रित है और किस क्लाउड प्रोवाइडर पर सबसे ज्यादा भरोसा है।

[25:00] Expanse: क्लस्टर टेलीमेट्री पर ट्रेनिंग से 8 गुना बेहतर GPU प्रेडिक्शन
YC P26 से Expanse एक ऐसी समस्या हल करता है जो HPC ऑपरेटर्स को अच्छी तरह पता है लेकिन सामान्य सॉफ्टवेयर टीमें अक्सर अनदेखा करती हैं: GPU जॉब्स अधिक संसाधन मांगती हैं क्योंकि सबमिटर के पास वास्तविक उपयोग का अनुमान लगाने का कोई अच्छा तरीका नहीं है। नतीजा बर्बाद कंप्यूट है — Expanse की टीम ने नेशनल HPC क्लस्टर पर 59% कंप्यूट वेस्ट मापा, जो केवल एक क्लस्टर पर ही लगभग $8.5 मिलियन प्रति माह है।

Expanse SLURM और Kubernetes नोड्स पर एक हल्का डेमॉन इंस्टॉल करके काम करता है, DCGM और CUPTI के माध्यम से हार्डवेयर टेलीमेट्री इनजेस्ट करता है, और प्रत्येक जॉब चलने से पहले VRAM, उपयोग और मेमोरी जरूरतों का अनुमान लगाता है। मॉडल क्लस्टर-विशिष्ट है — यह उस विशिष्ट क्लस्टर के वास्तविक सबमिशन हिस्ट्री पर फाइन-ट्यून होता है, इसलिए जैसे-जैसे यह अधिक डेटा एकत्र करता है, बेहतर होता जाता है।

बेंचमार्क रिजल्ट आश्चर्यजनक है: GPU रिसोर्स प्रेडिक्शन एक्यूरेसी में Expanse GPT-4.5, Claude Opus 4.8, Gemini 3.5 Pro और Codex 5.3 से 8 गुना बेहतर प्रदर्शन करता है। एजेंट-स्टैक लिसनर्स के लिए दिलचस्प विवरण यह है कि मॉडल का आकार यहां एक्यूरेसी का पूर्वानुमान नहीं करता। कुछ वर्कलोड पर Claude Haiku, Opus से बेहतर प्रदर्शन करता है क्योंकि क्लस्टर टेलीमेट्री पर फाइन-ट्यूनिंग जनरल रीज़निंग क्षमता से अधिक मायने रखती है।

GPU वर्कलोड चलाने वाली टीमों के लिए — ट्रेनिंग, फाइन-ट्यूनिंग, इंफरेंस, बैच प्रोसेसिंग — ROI ठोस है। इंटीग्रेशन नॉन-इनवेसिव है: एक नोड पर डेमॉन इंस्टॉल करें, दो हफ्ते तक वास्तविक रिसोर्स उपयोग के खिलाफ प्रेडिक्शन चलाएं, और तुलना करें।

[33:00] प्रोजेक्ट रडार: एजेंट OS, टर्मिनल कॉन्टेक्स्ट और फिजिकल शेड्यूलिंग
प्रोजेक्ट रडार एजेंट स्टैक के तीन अलग-अलग लेयर्स को कवर करता है।

Anima हार्डवेयर इंटेलिजेंस के लिए एक ओपन-सोर्स Agent OS है। अधिकांश एजेंट डिस्कशन क्लाउड VM मानती हैं, लेकिन IoT डिवाइस, रोबोटिक्स और एज हार्डवेयर पर चलने वाली एजेंट्स को एक अलग OS लेयर की जरूरत है — ऐसी जो डिजिटल टूल कॉल के साथ-साथ सेंसर डेटा, फिजिकल स्टेट और रियल-टाइम कंस्ट्रेंट के बारे में रीज़न कर सके। Anima अभी शुरुआती चरण में है, 116 स्टार्स के साथ, 2 जून को पुश किया गया, लेकिन समस्या का आकार असली है।

ctx एक टर्मिनल कॉन्टेक्स्ट मैनेजर है जो `.ctx.md` फाइलें जनरेट करता है। पैटर्न सरल है: रेपो में एक फाइल जिसे एजेंट हर सेशन की शुरुआत में सिस्टम कॉन्टेक्स्ट के रूप में पढ़ता है, कन्वेंशन, टास्क स्टेट और प्रोजेक्ट नोट्स आगे ले जाता है। यह पूरी नॉलेज ग्राफ मेमोरी सिस्टम जितना शक्तिशाली नहीं है, लेकिन सेट अप और मेंटेन करना भी उतना जटिल नहीं है। जो टीमें फुल मेमोरी आर्किटेक्चर में प्रतिबद्ध हुए बिना कॉन्टेक्स्ट कंटीन्यूइटी चाहती हैं, उनके लिए `.ctx.md` एक व्यावहारिक एंट्री पॉइंट है।

agentgrid AI-संचालित भौतिक मशीनों, टूल्स और डेस्कटॉप के लिए एक खुला शेड्यूलिंग लेयर है। यह एजेंट रनटाइम के नीचे बैठता है और तय करता है कि भौतिक कार्य कब और कैसे भेजे जाते हैं। जिन एजेंट्स को भौतिक हार्डवेयर टाइमिंग को समन्वित करने की जरूरत होती है — सिर्फ डिजिटल टूल्स को कॉल करने के बजाय — एक शेड्यूलिंग लेयर जो भौतिक बाधाओं को समझती है, शुद्ध LLM-संचालित एक्शन लूप से अधिक उपयुक्त है।

[41:00] व्यावहारिक कार्य सूची
Codex के लिए, `codex doctor` चलाएं और आउटपुट की तुलना करें, क्रॉस-प्रोजेक्ट पैटर्न के लिए एक नामित हुक परिभाषित करें, और CI में नॉन-इंटरैक्टिव इंस्टॉल को सत्यापित करें। Stanford के दिशानिर्देशों के लिए, दस्तावेज़ पढ़ें, जो आपकी टीम पर लागू होते हैं उन्हें निकालें, और अपने AGENTS.md को अपडेट करें। AWS मॉडल राउटिंग के लिए, किसी एक लैब को एकमात्र प्रोवाइडर के रूप में चुनने से पहले Anthropic और OpenAI दोनों के लिए Bedrock एंडपॉइंट्स को टेस्ट करें। Expanse के लिए, यदि आप बड़े पैमाने पर GPU वर्कलोड चलाते हैं तो एक क्लस्टर नोड पर इंस्टॉल करें। प्रोजेक्ट रडार के लिए, एक एज डिवाइस पर Anima आज़माएं, एक रेपो में `.ctx.md` जोड़ें, और agentgrid का मूल्यांकन करें जब कार्य में भौतिक हार्डवेयर टाइमिंग शामिल हो।

EP062 का मूल विषय यह है कि इन्फ्रास्ट्रक्चर दृश्यमान हो रहा है: डायग्नोस्टिक्स विफलताओं को समझाने योग्य बनाते हैं, दिशानिर्देश अपेक्षाओं को स्पष्ट करते हैं, क्लाउड डिस्ट्रिब्यूशन मॉडल राउटिंग को एक कॉन्फ़िगरेशन विकल्प बनाता है, और क्लस्टर-विशिष्ट ML कंप्यूट अपव्यय को मापने और ठीक करने योग्य बनाता है। एजेंट स्टैक उन तरीकों से बड़ा हो रहा है जो ऑपरेटर्स के लिए मायने रखते हैं।