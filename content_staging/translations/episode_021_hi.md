# EP021 — लूप के अंदर

**OpenClaw Daily** | 2 अप्रैल, 2026 | ~45 मिनट | हिंदी

[NOVA]: मैं NOVA हूं।

[ALLOY]: और मैं ALLOY हूं। ये OpenClaw Daily है। आज हम तीन AI एजेंट रनटाइम — OpenClaw, Claude Code, और Hermes — के सोर्स कोड में अंदर जाते हैं। और सवाल ये है कि आर्किटेक्चर हमें बताता है कि हर एक वास्तव में किसके लिए बना है।

[NOVA]: तीन एजेंट रनटाइम एक कोडबेस में दाखिल हुए। सिर्फ एक को पता था कि वो क्या बन रहा है।

[NOVA]: आज एक टेक्निकल डीप डाइव है, ALLOY। हम तुम्हें मार्केटिंग कॉपी नहीं देंगे। हम असली फाइल्स खोलेंगे और दिखाएंगे कि कोड क्या करता है — क्योंकि आर्किटेक्चर फिलॉसफी है। कोई सिस्टम अपनी टर्न साइकिल कैसे मैनेज करता है, मेमोरी कैसे परसिस्ट करता है, खतरनाक एक्शन्स को कैसे गेट करता है — ये इम्प्लीमेंटेशन डिटेल्स नहीं हैं। ये प्रोडक्ट हैं।

[ALLOY]: और दिलचस्प बात ये है कि जब तीनों को साथ देखते हो, तो पता चलता है कि "एजेंट" की परिभाषा पर उनका मतलब ही अलग है। Hermes का एक एजेंट है जो खुद को इम्प्रूव करता है और अपनी स्किल्स खुद लिखता है। Claude Code का एजेंट सिर्फ एक स्पेसिफिक डायरेक्टरी में कोड करने में मदद के लिए है। OpenClaw का एजेंट एक ऑपरेटिंग सिस्टम जैसा है — पर्सिस्टेंट, मल्टी-चैनल, मल्टी-सबएजेंट। ये असल में अलग-अलग जानवर हैं जो एक ही शब्द पहने हैं।

[NOVA]: चलो सबसे पहले देखते हैं कि हर सिस्टम टॉप लेवल पर कैसे स्ट्रक्चर्ड है — क्योंकि ये बाकी सब कुछ आकार देता है।

[NOVA]: OpenClaw से शुरू करते हैं। अगर ~/.openclaw/ देखो, तो रनटाइम स्ट्रक्चर वहां है। एक गेटवे डीमन है जो पूरे सिस्टम को मैनेज करता है। चैनल — Telegram, Discord, और आगे — प्लगइन हैं जो इस गेटवे से जुड़ते हैं। वर्कस्पेस फाइल्स ~/.openclaw/workspace/ में रहती हैं, और सबएजेंट्स डिटैच्ड प्रोसेस के तौर पर अपने-अपने कॉन्टेक्स्ट के साथ चलते हैं। कॉन्फिग openclaw.json में है। स्किल सिस्टम ~/.openclaw/skills/ में है, और मेमोरी ~/.openclaw/memory/ में स्टोर होती है। सबसे जरूरी बात — ~/.openclaw/cron/ भी है — OpenClaw में एक बिल्ट-इन शेड्यूलिंग सिस्टम है, जो तुम्हें बताता है कि ये रनटाइम उस मशीन के लिए डिज़ाइन है जिसे बिना किसी की निगरानी के भी टास्क रन करने होंगे।

[ALLOY]: सही। OpenClaw एक पर्सनल AI ऑपरेटिंग सिस्टम के तौर पर आर्किटेक्टेड है। ये सिर्फ एक सिंगल एजेंट लूप नहीं है। ये मैसेजिंग सरफेस पर पर्सिस्टेंट प्रेजेंस है, शेड्यूल्ड बैकग्राउंड वर्क है, और सबएजेंट डेलीगेशन है। openclaw गेटवे डीमन इस सिस्टम का कर्नल है। बाकी सब प्रोसेस है।

[NOVA]: अब Claude Code — और आर्किटेक्चर पर चर्चा छोटी होगी, क्योंकि Claude Code इंटेंशनली फोकस्ड है। npm से इंस्टॉल करते हो: @anthropic-ai/claude-code, वर्शन 2.1.59 रिकॉर्डिंग के समय। ये पहले एक CLI टूल है। इसमें एक सैंडबॉक्सिंग लेयर है जो डिपेंडेंसीज़ में दिखता है — macOS Apple Sandbox Profiles और Linux bwrap (bubblewrap) इंटीग्रेशन के लिए मॉड्यूल हैं। टूल रजिस्ट्री cli.js और संबंधित फाइल्स में है। लेकिन आर्किटेक्चर इंटेंशनली नैरो है — ये एक जॉब के लिए सबसे अच्छा टूल बनना चाहता है — एक कोडबेस डायरेक्टरी में डेवलपर की मदद।

[ALLOY]: जो एक पूरी तरह legitimate डिज़ाइन चॉइस है। नैरो और डीप, ब्रॉड और शैलो से बेहतर। लेकिन इसका मतलब ये है कि Claude Code का सेशन मॉडल बाकी दोनों से अलग है। इसमें पर्सिस्टेंट सेशन डेटाबेस नहीं है। हर इनवोकेशन कुछ हद तक ephemeral है, हालांकि ये वर्किंग डायरेक्टरी में कन्वर्सेशन स्टेट बनाए रख सकता है। आगे मेंमोरी पर आएंगे तो समझोगे।

[NOVA]: और फिर Hermes Agent — Nous Research से। ये सबसे स्पष्ट रूप से रिसर्च प्लेटफॉर्म के तौर पर आर्किटेक्टेड है। कोर ऑर्केस्ट्रेशन इंजन run_agent.py और उसका AIAgent क्लास है। सेशन स्टोर एक SQLite डेटाबेस है ~/.hermes/state.db पर WAL मोड में — तो concurrent readers, एक writer, जो matters जब गेटवे और CLI दोनों इसे hit कर रहे हों। और इसमें FTS5 फुल-टेक्स्ट सर्च है — सभी सेशन मैसेजेस पर, एक virtual table के जरिए।

[ALLOY]: ये वाकई एक बहुत अहम आर्किटेक्चरल डिसीजन है। FTS5 का मतलब है तुम अपनी पूरी कन्वर्सेशन हिस्ट्री सर्च कर सकते हो, सिर्फ हालिया टर्न्स नहीं। अगर तुम रिसर्चर हो जो लॉन्ग सेशन्स में काम करते हो, तो ये एक मीनिंगफुल फीचर है। और ये ट्रैक करते हैं कि हर सेशन में कितने टोकन, कितना बिलिंग, कौन सा मॉडल कॉन्फिग — ये बताता है कि ये कॉस्ट-कॉन्शसनेस के साथ बनाया गया था — रिसर्च लैब के लिए और यूज़र्स के लिए जो API कॉल्स के लिए पे कर रहे हैं।

[NOVA]: चलो सबसे अहम पीस की बात करते हैं — किसी भी एजेंट रनटाइम में: टर्न साइकिल। हर सिस्टम एक एक्सचेंज को कैसे हैंडल करता है — यूज़र मैसेज इन, मॉडल सोचता है, टूल कॉल्स, रिस्पॉन्स आउट?

[ALLOY]: Hermes से शुरू करते हैं, क्योंकि इसका लूप सबसे डॉक्यूमेंटेड है। डॉक्स से: run_conversation() है मुख्य एंट्री पॉइंट। टर्न लाइफसाइकिल है:

[NOVA]: 1. एक टास्क ID जेनरेट करो

[NOVA]: 2. करंट यूज़र मैसेज अपेंड करो

[NOVA]: 3. cached system prompt लोड करो या बनाओ

[NOVA]: 4. शायद प्रीफ्लाइट-कम्प्रेस करो अगर कॉन्टेक्स्ट लंबा हो रहा है

[NOVA]: 5. api_messages बनाओ — actual prompt payload

[NOVA]: 6. ephemeral prompt layers इंजेक्ट करो

[NOVA]: 7. prompt caching अप्लाई करो अगर appropriate है

[NOVA]: 8. एक इंटरप्टेबल API कॉल करो

[NOVA]: 9. अगर टूल कॉल्स हैं: execute करो, रिज़ल्ट्स अपेंड करो, वापस लूप करो

[NOVA]: 10. अगर फाइनल टेक्स्ट है: परसिस्ट करो, क्लीनअप करो, रिटर्न करो

[NOVA]: स्टेप 8 — इंटरप्टेबल API कॉल्स। ये अहम है। Hermes अपनी API रिक्वेस्ट्स को wrap करता है ताकि CLI या गेटवे से cancel किया जा सके। ये इसलिए matters क्योंकि एजेंट एक लंबी LLM कॉल में हो सकता है, और यूज़र बीच में एक नया मैसेज भेज दे, या बैकग्राउंड सिस्टम को cancel करना पड़े। ये एक explicit डिज़ाइन concern है, बाद में सोचा नहीं।

[ALLOY]: और Hermes के API modes देखो। तीन एक्जीक्यूशन पाथ: chat_completions OpenAI-compatible एंडपॉइंट्स के लिए (OpenRouter सहित), codex_responses Codex और Responses API के लिए, और anthropic_messages Anthropic Messages API के लिए। मोड explicit arguments, provider selection, और base URL heuristics से resolve होता है। तो Hermes genuine तौर पर model-agnostic है — मार्केटिंग क्लेम नहीं, बल्कि एक routing architecture है।

[NOVA]: अब Hermes का टूल एक्जीक्यूशन। दो मोड: sequential सिंगल या इंटरैक्टिव टूल्स के लिए, और concurrent मल्टीपल नॉन-इंटरैक्टिव टूल्स के लिए। और यहां एक चतुर पार्ट है — concurrent एक्जीक्यूशन मैसेज और रिज़ल्ट ऑर्डर प्रिज़र्व करता है जब टूल रिस्पॉन्सेस को कन्वर्सेशन हिस्ट्री में वापस इंसर्ट करते हैं। ये सही लागू करना आसान नहीं है।

[ALLOY]: Claude Code के बारे में, हमारे पास उस लूप फाइल का exact सोर्स पाथ उस तरह नहीं है, लेकिन पैकेज स्ट्रक्चर से इनफर कर सकते हैं। npm पैकेज है /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/ पर। देखने के लिए key patterns हैं cli.js में — टूल कॉल्स कैसे handle होते हैं, permission prompts कैसे manage होते हैं, लूप कैसे चलता है। जो हम जानते हैं Claude Code के लूप के बारे में वो ये है कि ये एक specific use case के आसपास डिज़ाइन है: एक लोकल डायरेक्टरी में डेवलपर असिस्टेंस। इसमें subagent spawning फर्स्ट-क्लास कॉन्सेप्ट नहीं है जैसा OpenClaw में है।

[NOVA]: और OpenClaw का एजेंट लूप इस बात के इर्द-गिर्द डिज़ाइन है कि इसके पास मल्टीपल concurrent एजेंट्स हैं जिन्हें गेटवे manage करता है। लूप सिर्फ "यूज़र → एजेंट → टूल्स → रिस्पॉन्स" के बारे में नहीं है। ये इस बारे में है: यूज़र का मैसेज चैनल X पर आया, सबएजेंट Y ने उसे उठाया, सबएजेंट Y शायद सबएजेंट Z स्पॉन करे, रिज़ल्ट्स आए, गेटवे right सरफेस पर dispatch करे। clawflow skill जो मल्टी-एजेंट वर्कफ्लोज़ को ऑर्केस्ट्रेट करती है — ये डिटैच्ड बैकग्राउंड टास्क्स के लिए डिज़ाइन है जो फिर भी एक जॉब की तरह बरतते हैं।

[ALLOY]: OpenClaw का लूप तीनों में सबसे complex है क्योंकि इसके पास मैनेज करने को सबसे ज्यादा coordination surface है। लेकिन complexity हमेशा बुरी नहीं होती — ये जो वो करने की कोशिश कर रहा है उसके लिए appropriate complexity है।

[NOVA]: यहीं Hermes असल में अपने आप को आर्किटेक्चरली अलग करता है। चलो SQLite स्कीमा में गहराई से जाते हैं।

[ALLOY]: ~/.hermes/state.db में चार logical कंपोनेंट्स हैं: एक sessions टेबल, एक messages टेबल, messages_fts नाम का FTS5 virtual टेबल, और एक schema_version टेबल। sessions टेबल समृद्ध है — ये सिर्फ सेशन metadata नहीं ट्रैक करता, बल्कि बिलिंग इन्फॉर्मेशन भी: input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, actual_cost_usd, cost_status, pricing_version। अगर तुम मल्टी-मॉडल सेटअप चला रहे हो जिसमें अलग-अलग प्रोवाइडर्स से अलग pricing है, तो Hermes हर सेशन के हिसाब से तुम्हारी costs ट्रैक कर रहा है।

[NOVA]: messages टेबल में सब कुछ स्टोर है। role, content, tool_call_id, tool_calls as a JSON string, tool_name, token_count, finish_reason, reasoning, reasoning_details, और codex_reasoning_items। ध्यान दो कि reasoning separately स्टोर है — ये उन प्रोवाइडर्स के लिए है जो thinking tokens expose करते हैं। और तीन triggers हैं जो FTS5 टेबल को INSERT, UPDATE, और DELETE पर सिंक में रखते हैं।

[ALLOY]: write contention handling देखने लायक है। Hermes कई प्रोसेस एक साथ हैंडल करता है — गेटवे प्लस CLI सेशन्स प्लस worktree एजेंट्स — सब एक state.db शेयर करते हुए। ये short SQLite timeout इस्तेमाल करता है — 1 सेकंड, डिफ़ॉल्ट 30 नहीं — application-level retries random jitter के साथ 20 और 150 मिलीसेकंड के बीच, 15 retries तक, और BEGIN IMMEDIATE transactions जो lock contention जल्दी surface करते हैं। ये periodic WAL checkpoints भी करता है — हर 50 writes पर PASSIVE मोड में। ये thoughtful engineering है — वो SQLite के convoy effect problem से बच रहे हैं जहां competing writers same intervals पर retry करते हैं।

[NOVA]: और parent_session_id चेन के जरिए सेशन लाइनीयर। जब context compression सेशन split trigger करता है — जो तब होता है जब कॉन्टेक्स्ट विंडो भर जाती है — नया सेशन एक नया ID पाता है लेकिन पैरेंट से जुड़ा रहता है। तुम पूरे सेशन लाइनीयर को recursively क्वेरी कर सकते हो। ये लॉन्ग-रनिंग रिसर्च या कोडिंग सेशन के लिए है जहां context compression मिड-टास्क होती है।

[ALLOY]: अब इसकी तुलना Claude Code से करो। Claude Code का सेशन मॉडल... हल्का है। ये वर्किंग डायरेक्टरी में कन्वर्सेशन कॉन्टेक्स्ट बनाए रख सकता है, लेकिन ये लॉन्ग-टर्म स्ट्रक्चर्ड मेमोरी सिस्टम के तौर पर डिज़ाइन नहीं है। सैंडबॉक्स फाइलसिस्टम permissions के इर्द-गिर्द डिज़ाइन है — एक स्पेसिफिक डायरेक्टरी के लिए — पर्सिस्टेंट स्ट्रक्चर्ड मेमोरी के लिए नहीं। ये एक deliberate tradeoff है: सबसे common case के लिए simplicity (कोडबेस में डेवलपर हेल्प) बनाम rich सेशन persistence।

[NOVA]: और OpenClaw का मेमोरी मॉडल। ये स्ट्रक्चर्ड कॉन्टेक्स्ट के लिए वर्कस्पेस फाइल्स इस्तेमाल करता है — MEMORY.md लॉन्ग-टर्म curated मेमोरी के लिए, memory/YYYY-MM-DD.md daily session logs के लिए। एक LCM भी है — Lossless Context Management — सिस्टम जो कन्वर्सेशन हिस्ट्री को compact करता है। और एक स्किल सिस्टम है जो procedural memory की तरह काम करता है। तो ये एक तीन-लेयर मॉडल है: raw daily logs, curated लॉन्ग-टर्म मेमोरी, और skills जो reusable workflows एन्कोड करती हैं।

[ALLOY]: OpenClaw का approach Hermes के मुकाबले ज्यादा फाइल-सिस्टम-नेटिव है और कम डेटाबेस-नेटिव। Hermes सब कुछ SQLite में रखता है क्योंकि ये एक सिंगल रनटाइम है जिसे concurrent multi-process access और FTS5 चाहिए। OpenClaw फाइलसिस्टम इस्तेमाल करता है क्योंकि ये Unix फिलॉसफी में फिट बैठता है और डेटा universally accessible बनाता है — तुम इसे grep कर सकते हो, rsync से बैकअप कर सकते हो, git में रख सकते हो।

[NOVA]: यहीं Claude Code वास्तव में अपने पत्ते दिखाता है। चलो बात करते हैं कि ये खतरनाक एक्शन्स को कैसे हैंडल करता है।

[ALLOY]: Claude Code का sandboxing सिस्टम दो प्लेटफॉर्म्स को explicitly टारगेट करता है: macOS और Linux। macOS पर, ये Apple Sandbox Profiles इस्तेमाल करता है। Linux पर, ये bwrap — bubblewrap — इस्तेमाल करता है। सिस्टम का नाम है SandboxLinux सोर्स में, और क्लासेस हैं जैसे SandboxConfig, SandboxManager, और ViolationStore जो sandbox violations ट्रैक करता है — एक total count और per-command history के साथ। violations store की max size 100 entries है और एक total count जो बढ़ता रहता है भले ही स्टोर भर जाए।

[NOVA]: Linux के लिए sandbox config sandbox_linux.py में define है। ये --new-session --die-with-parent से शुरू होता है। फिर allowed और denied फाइलसिस्टम paths बनाता है। Allowed paths एक डिफ़ॉल्ट allowlist से शुरू होते हैं — जैसे /dev/null, /dev/urandom, /dev/zero। Denied paths चीज़ें हैं जैसे /etc/ssh/ssh_config.d अगर वो मौजूद है। write paths के लिए, एक denyWithinAllow कॉन्सेप्ट है — तुम एक डायरेक्टरी में लिख सकते हो लेकिन उसमें मौजूद specific खतरनाक subpaths में नहीं।

[ALLOY]: Linux sandbox में seccomp BPF filtering भी है Unix socket blocking के लिए। एक bpfPath और applyPath है seccomp binary के लिए। अगर वो available नहीं हैं, तो ये Unix sockets allow करने पर fallback करता है — लेकिन warns कि पूरा प्रोटेक्शन available नहीं है। macOS पर, एक SandboxMonitor है जो osascript command इस्तेमाल करके violations देखता है।

[NOVA]: अब इसकी तुलना Hermes के approach से करो। Hermes का approach अलग है। Hermes के tools/approval.py में एक DANGEROUS_PATTERNS list है — regex patterns जो descriptions के साथ pair हैं: recursive deletes, फाइलसिस्टम formatting commands जैसे mkfs और dd, SQL destructive operations, सिस्टम कॉन्फिग overwrites, service manipulation, curl | sh के जरिए remote code execution, fork bombs। किसी भी टर्मिनल कमांड को execute करने से पहले, detect_dangerous_command() सभी patterns के खिलाफ check करता है।

[ALLOY]: अगर कोई match मिला: CLI मोड में, एक इंटरैक्टिव prompt यूज़र से approve, deny, या permanently allow पूछता है। गेटवे मोड में, एक async approval callback मैसेजिंग प्लेटफॉर्म पर रिक्वेस्ट भेजता है — तो अगर तुम Telegram या Discord पर हो, तो तुम्हें वहां approval मैसेज मिलता है। एक smart approval option भी है जहां एक auxiliary LLM low-risk commands को automatically approve कर सकता है जो dangerous patterns से match करती हैं — जैसे rm -rf node_modules/ जो recursive delete pattern से match करती है।

[NOVA]: और Hermes के पास session-scoped approvals हैं। एक बार तुमने "recursive delete" को एक सेशन के लिए approve कर दिया, तो बाद की rm -rf कमांड्स फिर से prompt नहीं करतीं। permanent allowlist config.yaml के command_allowlist में patterns लिखता है ताकि वो सेशन में persist करें।

[ALLOY]: ये फंडामेंटली अलग मॉडल हैं। Claude Code का sandbox प्रोसेस की capabilities पहले से सीमित कर देता है — OS enforce करता है। Hermes का approval सिस्टम dangerous patterns detect करता है और पूछता है — ह्यूमन enforce करता है। Claude Code का मॉडल accidental damage के खिलाफ मजबूत है। Hermes का मॉडल interactive use cases के लिए ज्यादा flexible है जहां एजेंट एक remote server पर चल रहा है और यूज़र Telegram पर approve कर रहा है।

[NOVA]: OpenClaw का मॉडल दोनों के एलिमेंट्स को combine करता है। exec tool का एक approval system है — openclaw.json के साथ-साथ exec-approvals.json है। और OpenClaw के subagent सिस्टम में permission scoping है — सबएजेंट्स specific वर्कस्पेस कॉन्टेक्स्ट के साथ चलते हैं और necessarily सब कुछ पढ़ या लिख नहीं सकते जो पैरेंट एजेंट कर सकता है। गेटवे में channel-specific permissions का कॉन्सेप्ट भी है — Telegram पर क्या allowed है वो Discord से अलग हो सकता है।

[NOVA]: चलो बात करते हैं कि हर सिस्टम तुम्हें खुद को एक्सटेंड करने कैसे देता है।

[ALLOY]: Hermes के skills system से शुरू करते हैं, क्योंकि ये सबसे fully realized है। Skills on-demand knowledge documents हैं जो एजेंट load कर सकता है जब चाहिए। वो agentskills.io ओपन स्टैंडर्ड follow करते हैं, जिसका मतलब Hermes तक locked नहीं हैं — portable हैं। skill format है SKILL.md with YAML frontmatter declaring name, description, version, platforms, और metadata for activation conditions।

[NOVA]: progressive disclosure पैटर्न चतुर है। Level 0: skills_list() सिर्फ name, description, और category देता है — करीब 3k टोकन। Level 1: skill_view(name) full content लोड करता है। Level 2: skill_view(name, path) एक specific reference file लोड करता है। एजेंट तभी token cost देता है जब उसे actual में पूरी skill चाहिए।

[ALLOY]: skills conditional हो सकते हैं। वो declare कर सकते हैं fallback_for_toolsets — तो एक DuckDuckGo search skill सिर्फ तब दिखता है जब premium web search toolset unavailable है। या requires_toolsets — एक skill सिर्फ तब दिखता है जब certain tools मौजूद हों। और वो required environment variables declare कर सकते हैं बिना discovery से गायब हुए — अगर एक key मिसिंग है, Hermes CLI मोड में skill load होने पर securely ask करता है, लेकिन messaging surfaces पर कभी prompt नहीं करता।

[NOVA]: agent-created skills एक key differentiator हैं। skill_manage tool एजेंट को create/patch/edit/delete/write_file/remove_file एक्शन सेट के जरिए अपनी skills बनाने, अपडेट करने, और हटाने देता है। डॉक्स specify करते हैं trigger conditions: एक complex टास्क 5+ टूल कॉल्स के साथ पूरा होने के बाद, जब एरर आती हैं और working path मिलती है, जब यूज़र उसके approach को सुधारता है, जब वो एक non-trivial workflow discover करता है। ये procedural memory लेयर है — एजेंट सिर्फ काम नहीं कर रहा, काम करने का तरीका सीख रहा है।

[ALLOY]: Hermes का full skill marketplace integration है। ये official optional skills catalog से जुड़ता है, skills.sh (Vercel का public directory), well-known skill endpoints /.well-known/skills/ कन्वेंशन के जरिए, direct GitHub repos, ClawHub, और Claude marketplace repos। तुम GitHub पर directly skills publish कर सकते हो। custom GitHub taps add कर सकते हो। ये genuinely एक ओपन ecosystem play है — Hermes skill supply chain का मालिक होने की कोशिश नहीं कर रहा।

[NOVA]: और Hermes external skill directories support करता है। तुम इसे ~/.agents/skills/ या /home/shared/team-skills/ पर पॉइंट कर सकते हो ${VAR} environment variable expansion के जरिए। वो directories discovery के लिए read-only हैं — एजेंट हमेशा नई skills ~/.hermes/skills/ में लिखता है। लेकिन external skills system prompt index में दिखते हैं और slash commands की तरह, local skills से indistinguishable।

[ALLOY]: अब OpenClaw के skills system की बात करते हैं। ~/.openclaw/skills/ को देखो, तो ये भी YAML frontmatter + markdown body है, और hermes claw migrate tool suggests कि cross-compatibility intentional है। OpenClaw skills workspace-contextual हैं — वो उस प्रोजेक्ट के साथ रहती हैं जिससे वो relevant हैं। skill system subagent सिस्टम के साथ integrated है, तो तुम skills रख सकते हो जो describe करते हैं कि किसी टास्क के लिए right subagent कैसे spawn करना है।

[NOVA]: और OpenClaw MCP — Model Context Protocol — को एक extensibility mechanism की तरह support करता है। openclaw.json कॉन्फिग में एक plugins section और एक extensions section है। MCP servers external services से टूल्स देने के लिए configure किए जा सकते हैं।

[ALLOY]: Claude Code का extension model ज्यादा focused है। npm package structure suggests ये existing developer tooling के साथ अच्छे से काम करने के लिए डिज़ाइन है, अपना plugin marketplace रखने के बजाय। Claude Code में skill system हल्का है — स्लैश कमांड्स, असल में। लेकिन एक focused CLI टूल के लिए यही appropriate है।

[NOVA]: हमें hermes claw migrate की बात करनी होगी। ये एक explicit migration tool है जो Hermes के साथ आता है OpenClaw skills और workspace configurations import करने के लिए। ये एक significant signal है।

[ALLOY]: absolutely है। Hermes एक tool के साथ आता है जिसका नाम है hermes claw migrate और जो कहता है: हम जानते हैं OpenClaw का skills system borrowing करने लायक है। हम इसे import करेंगे। ये किसी प्रोजेक्ट का मूव नहीं है जो खुद को अलग कैटेगरी में देखता है। ये उस प्रोजेक्ट का मूव है जो सीधे कंपीट कर रहा है और सोच रहा है कि skills ecosystem worth cross-pollinating है।

[NOVA]: ये बात hermes claw migrate है न कि claw migrate — ये directional relationship के बारे में कुछ बताता है। OpenClaw पहले आया — Hermes इससे migrate कर रहा है। लेकिन Hermes इसे explicitly कर रहा है, जिसका मतलब है कि Nous Research टीम ने OpenClaw के skill system और workspace model को देखा और तय किया: हम वो अपने ecosystem में चाहते हैं, और OpenClaw users के लिए Hermes try करना आसान बनाना चाहते हैं।

[ALLOY]: और Hermes का model-agnostic architecture इस migration को credible बनाता है। अगर तुम OpenClaw का इस्तेमाल Claude को backend के तौर पर कर रहे थे, तो Hermes पर switch कर सकते हो और same skills use कर सकते हो। skill format open है — SKILL.md with YAML frontmatter agentskills.io spec follow करता है। ये proprietary lock-in format नहीं है।

[NOVA]: ऐसी चीज़ें तभी होती हैं जब एक open ecosystem मैच्योर होने लगती है। OpenAI के पास Actions और Plugins थे। Anthropic के पास MCP है। और अब Hermes के पास OpenClaw skills के लिए migration tool है। skills portability story एक genuine competitive dimension बनती जा रही है।

[ALLOY]: और OpenClaw का इसका जवाब शायद... कुछ बदलने की जरूरत नहीं है। ये बात कि Hermes OpenClaw से migrate कर रहा है इसका मतलब है कि OpenClaw का model reference है। OpenClaw को Hermes पर migrate करने की जरूरत नहीं है। लेकिन OpenClaw को ध्यान से देखना चाहिए कि Hermes का skill ecosystem कैसे evolve होता है — अगर Hermes एक richer marketplace बनाता है, तो ये users के लिए एक reason बन सकता है कि वो उसका evaluate करें।

[NOVA]: मुझे तुम्हें कुछ specific class names और file names देते हैं ताकि ये डिस्कशन grounded हो।

[ALLOY]: Hermes से:

[NOVA]: — Core agent: run_agent.py — AIAgent क्लास

[NOVA]: — State management: hermes_state.py — SessionDB क्लास

[NOVA]: — Tool registry: tools/registry.py — ToolRegistry singleton, ToolEntry objects

[NOVA]: — Tool discovery: model_tools.py — _discover_tools() फंक्शन

[NOVA]: — Tool dispatch: registry.dispatch(name, args, kwargs) — right handler पर रूट करता है

[NOVA]: — Approval system: tools/approval.py — DANGEROUS_PATTERNS, detect_dangerous_command()

[NOVA]: — Context compression: agent/context_compressor.py

[NOVA]: — Prompt building: agent/prompt_builder.py

[NOVA]: — Prompt caching: agent/prompt_caching.py

[NOVA]: — Session DB path: ~/.hermes/state.db

[NOVA]: — Skill directory: ~/.hermes/skills/

[NOVA]: — Config: ~/.hermes/config.yaml

[NOVA]: Hermes में tool discovery दिलचस्प है। _discover_tools() modules को fixed ऑर्डर में इम्पोर्ट करता है, और हर module module level पर registry.register() कॉल करता है। module list में शामिल हैं: web_tools, terminal_tool, file_tools, vision_tools, mixture_of_agents_tool, image_generation_tool, skills_tool, browser_tool, cronjob_tools, rl_training_tool, tts_tool, todo_tool, memory_tool, session_search_tool, clarify_tool, code_execution_tool, delegate_tool, process_registry, send_message_tool, honcho_tools, homeassistant_tool। ये एक बहुत comprehensive list है — Hermes कोई narrow tool नहीं है।

[ALLOY]: और mixture_of_agents_tool के साथ-साथ rl_training_tool और delegate_tool बताते हैं कि Hermes एक research platform की तरह डिज़ाइन है। ये consumer features नहीं हैं। mixture_of_agents ensemble methods suggest करता है, rl_training reinforcement learning from feedback suggest करता है, delegate_task subagent spawning suggest करता है। ये एक सिस्टम है जो researchers के लिए डिज़ाइन है जो agentic RL के साथ experiment करना चाहते हैं।

[NOVA]: Claude Code के लिए, package है /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/ पर। sandbox system में क्लासेस हैं जैसे SandboxLinux, SandboxConfig, SandboxManager, ViolationStore। permission system में हैं policySettings, userSettings, projectSettings, localSettings — layered permission sources जिनके पास allow, deny, और ask के लिए rules हैं। tool registry uses alwaysAllowRules, alwaysDenyRules, alwaysAskRules — तो एक three-tier permission model है: always allow, always deny, always ask।

[ALLOY]: OpenClaw के लिए, गेटवे डीमन, क्रॉन शेड्यूलिंग, सबएजेंट ऑर्केस्ट्रेशन, और चैनल प्लगइन (Discord, Telegram) सब ~/.openclaw/ के अंदर हैं। वर्कस्पेस स्ट्रक्चर प्रोजेक्ट-relative है। skills ~/.openclaw/skills/ में रहती हैं। LCM सिस्टम context compaction के लिए runtime में है। clawflow skill मल्टी-एजेंट वर्कफ्लोज़ manage करती है।

[NOVA]: ठीक है। हम thorough रहे। चलो वर्डिक्ट देते हैं।

[ALLOY]: Hermes Agent use करो अगर: तुम एक researcher या power user हो जो एक self-improving agent चाहते हो genuine long-term memory के साथ, model-agnostic flexibility के साथ, FTS5 सर्च अपनी पूरी कन्वर्सेशन हिस्ट्री पर, एक rich skill ecosystem जिसमें तुम contribute भी करते हो और जिससे draw भी करते हो, और Telegram, Discord, Slack, WhatsApp, या Signal पर एक गेटवे से रन करने की क्षमता। Hermes वो सही चॉइस भी है अगर तुम RL-based agent improvement में इंटरेस्टेड हो — Atropos RL environments और trajectory compression एक research-forward डिज़ाइन suggest करते हैं। और अगर तुम पहले से ही OpenClaw user हो, तो Hermes का hermes claw migrate means तुम अपनी skills अपने साथ ला सकते हो।

[NOVA]: Claude Code use करो अगर: तुम एक developer हो जो एक स्पेसिफिक कोडबेस में सबसे अच्छी possible मदद चाहते हो, लोकली रन करते हुए, और dangerous operations के लिए strongest OS-level sandboxing के साथ। Claude Code का bubblewrap और Apple Sandbox integration तीनों में सबसे rigorous sandbox implementation है। अगर तुम्हारा वर्कफ्लो ये है कि "मैं एक डायरेक्टरी में हूं, मदद चाहिए, मुझे भरोसा है कि एजेंट यहां फाइल्स एडिट करे," तो Claude Code इस जॉब के लिए सबसे focused टूल है। trade-off है सेशन persistence और मल्टी-चैनल प्रेजेंस — ये उसके लिए डिज़ाइन नहीं है।

[ALLOY]: OpenClaw use करो अगर तुम एक persistent personal AI चाहते हो जो तुम्हारी मशीन पर जिये (या VPS), मल्टीपल मैसेजिंग चैनल्स एक साथ से जुड़े, शेड्यूल्ड टास्क रन करे, बैकग्राउंड वर्क के लिए सबएजेंट्स स्पॉन करे, और एक skill system जो तुम्हारा खुद का हो। OpenClaw तीनों में सबसे Unix-native है — ये naturally command-line वर्कफ्लो में फिट बैठता है, मौजूदा dotfile और workspace conventions के साथ काम करता है, और ये तुम्हारा AI ऑपरेटिंग सिस्टम बनने के लिए डिज़ाइन है — एक सिंगल टूल नहीं। ये बात कि Hermes OpenClaw से migration tool लाता है ये बताती है कि OpenClaw skill model reference है।

[NOVA]: गहरी बात ये है कि ये तीनों सिस्टम तीन अलग-अलग theories एन्कोड करते हैं कि AI एजेंट क्या होना चाहिए। Hermes सोचता है कि एक एजेंट एक persistent, self-improving research companion होना चाहिए rich memory और model flexibility के साथ। Claude Code सोचता है कि एक एजेंट एक narrow, deeply integrated development tool होना चाहिए strong safety guarantees के साथ। OpenClaw सोचता है कि एक एजेंट एक personal AI OS होना चाहिए — हमेशा ऑन, मल्टी-सरफेस, मल्टी-एजेंट।

[ALLOY]: इन theories में से कोई गलत नहीं है। वो space कहां जा रही है उस पर अलग-अलग bets हैं। अगले कुछ साल बताएंगे कि कौन सा सही था।

[NOVA]: एक आखिरी बात बंद होने से पहले — तुममें से काफी लोग Hermes try करना चाहेंगे इसके बाद। तो चलो मॉडल्स की बात करते हैं। Hermes genuine तौर पर model-agnostic है, लेकिन डॉक्स specific हैं कि क्या सबसे अच्छा काम करता है।

[ALLOY]: उनका recommended starting point है Claude Sonnet Anthropic OAuth के जरिए — और यहां चतुर पार्ट है: अगर तुम पहले से ही Claude Code use करते हो, तो Hermes automatically Claude Code का credential store पढ़ लेता है। कोई separate API key setup नहीं। तुम hermes model रन करते हो, Anthropic pick करते हो, और ये तुम्हारे existing subscription के साथ बस काम करता है।

[NOVA]: फ्री ऑप्शन्स के लिए, Hermes के पास first-class GitHub Copilot support है। अगर तुम्हारे पास Copilot subscription है, तो तुम्हें GPT-5.4, Claude, और Gemini तक access मिलता है Copilot API के जरिए। GPT-5 और उससे ऊपर automatically Responses API के जरिए route होते हैं; बाकी सब Chat Completions use करता है।

[ALLOY]: सबसे interesting फ्री पाथ OpenRouter है। अपनी .env फाइल में एक OPENROUTER API KEY सेट करो, hermes model रन करो, और तुम्हारे पास 200 से ज्यादा मॉडल्स हैं। Hermes डॉक्स specifically call out करते हैं कि कुछ built-in tools — vision, web summarization, और mixture of agents tool — एक separate auxiliary model use करते हैं जो डिफ़ॉल्ट में Gemini Flash OpenRouter के जरिए है। तो अगर तुम अपने प्राइमरी के तौर पर Claude use कर रहे हो, एक OpenRouter key उन टूल्स को automatically unlock कर देता है।

[NOVA]: लोकल मॉडल्स के लिए, Hermes any Ollama या vLLM endpoint support करता है — same कॉन्फिग, बस अपने local server को OPENAI BASE URL पर पॉइंट करो। और Chinese providers के लिए specifically: Z-dot-AI GLM, Kimi slash Moonshot, MiniMax, और Alibaba Cloud Qwen सबके पास first-class provider IDs हैं। बाद में सोचा नहीं — वो core provider list में हैं Anthropic और OpenAI के साथ।

[ALLOY]: practical answer ज्यादातर लोगों के लिए: अगर तुम्हारे पास Claude Pro या Max है, तो Anthropic OAuth से शुरू करो। अगर strong capability के साथ फ्री चाहते हो, GitHub Copilot with GPT-5.4। अगर maximum flexibility चाहते हो और एक छोटे API bill की परवाह नहीं, तो OpenRouter with Claude Sonnet या Qwen 3।

[NOVA]: वो EP021 है: लूप के अंदर। पूरे शो नोट्स और लिंक्स के लिए Toby On Fitness Tech dot com slash podcasts slash episode 21 पर जाओ। मैं NOVA हूं।

[ALLOY]: और मैं ALLOY हूं। जल्दी वापस आएंगे।
