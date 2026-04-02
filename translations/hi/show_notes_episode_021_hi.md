# EP021 — लूप के अंदर

**OpenClaw Daily** | 2 अप्रैल, 2026 | ~45 मिनट

तीन AI एजेंट रनटाइम — OpenClaw, Claude Code, और Hermes — के सोर्स कोड में कूदते हैं यह एपिसोड। सवाल सीधा है: आर्किटेक्चर क्या बताता है?

---

## इस एपिसोड में

### आर्किटेक्चर का फिलॉसफी है
OpenClaw एक पर्सनल AI ऑपरेटिंग सिस्टम है — गेटवे डीमन इसका कर्नेल है, चैनल प्लगइन प्रोसेस हैं, और क्रॉन शेड्यूलिंग का मतलब यह है कि यह मशीन बिना किसी की निगरानी में भी काम कर सकती है।

Claude Code इंटेंशनली नैरो है — एक डायरेक्टरी में डेवलपर की मदद के लिए बनी, न कि पर्सिस्टेंट मेमोरी या मल्टी-चैनल प्रेजेंस के लिए।

Hermes सबसे रिसर्च-फॉरवर्ड है — SQLite WAL मोड, FTS5 फुल-टेक्स्ट सर्च, टोकन और कॉस्ट ट्रैकिंग, और सेशन लाइनीयर पैरेंट_SESSION_ID चेन के जरिए।

### टर्न साइकिल: तीन अलग-अलग दर्शन
Hermes का लूप सबसे डॉक्यूमेंटेड है — run_conversation() में 10 स्टेप्स, इंटरप्टेबल API कॉल्स, और तीन एक्जीक्यूशन पाथ (chat_completions, codex_responses, anthropic_messages)।

Claude Code का सैंडबॉक्स सबसे सख्त है — macOS पर Apple Sandbox Profiles, Linux पर bubblewrap (bwrap)। यह OS-लेवल सिक्योरिटी है, प्रोसेस की कैपेबिलिटीज़ पहले से सीमित कर देती है।

Hermes का approval सिस्टम अलग काम करता है — dangerous pattern detection के बाद ह्यूमन से पूछता है, CLI मोड में इंटरैक्टिव प्रॉम्प्ट, गेटवे मोड में Telegram/Discord पर मैसेज।

OpenClaw दोनों का मिक्स है — exec tool approval + सबएजेंट परमिशन स्कोपिंग + चैनल-स्पेसिफिक परमिशन।

### मेंमोरी: तीन लेयर्स बनाम डेटाबेस
OpenClaw: फाइल-सिस्टम नेटिव — MEMORY.md, daily session logs, LCM compaction, skills procedural memory।

Hermes: SQLite नेटिव — FTS5 सर्च, WAL मोड, concurrent multi-process access, session lineage chains।

Claude Code: लाइटवेट — वर्किंग डायरेक्टरी में कन्वर्सेशन स्टेट, लॉन्ग-टर्म स्ट्रक्चर्ड मेमोरी नहीं।

### स्किल सिस्टम: ओपन इकोसिस्टम की लड़ाई
Hermes का skills system सबसे समृद्ध है — agentskills.io ओपन स्टैंडर्ड, progressive disclosure (level 0/1/2), conditional skills (fallback_for_toolsets, requires_toolsets), agent-created skills, और एक पूरा marketplace इंटीग्रेशन।

OpenClaw: YAML frontmatter + markdown body, workspace-contextual, subagent सिस्टम के साथ इंटीग्रेटेड।

Claude Code: स्लैश कमांड्स, फोकस्ड CLI इंटरैक्शन के लिए डिज़ाइन।

### Hermes claw migrate: एक सिग्निफिकेंट सिग्नल
Hermes एक explicit migration tool लाता है जो OpenClaw skills और workspace config इम्पोर्ट करता है। यह एक प्रोजेक्ट का मूव नहीं है जो खुद को अलग कैटेगरी में देखता है — यह मूव है जो सीधे कंपीट करने वालों में से एक है।

### कौन कब इस्तेमाल करे
**Hermes** — रिसर्चर/पावर यूज़र जो long-term memory, model-agnosticism, FTS5 सर्च, self-improving agent, और Telegram/Discord/Slack/WhatsApp/Signal एक गेटवे से चाहते हैं।

**Claude Code** — डेवलपर जो एक स्पेसिफिक कोडबेस में सबसे अच्छी मदद चाहते हैं, लोकली रन करते हुए, और strongest OS-level sandboxing के साथ।

**OpenClaw** — वो लोग जो एक persistent personal AI चाहते हैं जो मशीन पर जिये (या VPS), मल्टीपल मैसेजिंग चैनल्स से जुड़े, शेड्यूल्ड टास्क्स रन करे, सबएजेंट्स स्पॉन करे, और एक skill system जो उनका खुद का हो।

---

## चैप्टर्स

`[00:00]` कोल्ड ओपन — तीन एजेंट, एक कोडबेस
`[02:30]` टॉप-लेवल आर्किटेक्चर — तीन सिस्टम कैसे स्ट्रक्चर्ड हैं
`[08:00]` टर्न साइकिल — Hermes का 10-स्टेप लूप
`[16:00]` डेटाबेस डीप-डाइव — Hermes SQLite स्कीमा
`[24:00]` सैंडबॉक्स बनाम Approval — Claude Code vs Hermes मॉडल
`[32:00]` मेंमोरी मॉडल — फाइल-सिस्टम vs डेटाबेस
`[38:00]` स्किल इकोसिस्टम — Hermes claw migrate का मतलब
`[43:00]` वर्डिक्ट — कौन कब
`[50:00]` मॉडल चॉइस — Anthropic OAuth, GitHub Copilot, OpenRouter, लोकल
`[53:00]` आउट्रो

---

## OpenClaw Daily ढूंंढें

- 🌐 [tobyonfitnesstech.com/hi/podcasts/episode-21/](https://tobyonfitnesstech.com/hi/podcasts/episode-21/)
- 🎙️ Spotify · Apple Podcasts · Pocket Casts · Amazon Music · Overcast
- EN, ES, PT, HI, DE फीड्स उपलब्ध

→ Reply on Telegram to approve.
