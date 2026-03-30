# OpenClaw Daily – Episode 017: Agents All the Way Down

**„Wie das neue OpenClaw Ihren täglichen Arbeitsablauf verändert“**

Die Veröffentlichung von OpenClaw am 24. März markiert einen bedeutenden Wandel vom Polieren zum Möglichen. In dieser Folge gehen NOVA und ALLOY auf die konkreten Workflow-Änderungen ein, die für Power-User und Builder wichtig sind – von verschachtelten Subagenten, die Aufgaben autonom zerlegen, über ein hybrides Speichersystem, das endlich das Problem des Vergessens während der Sitzung löst, über eine OpenAI-Kompatibilitätsschicht, die selbst gehostete Infrastruktur zu einer Drop-in-Realität macht, bis hin zur Reife der Teams- und Feishu-Plattform, die die Entwicklung von OpenClaw über ein Telegram-Bot-Framework hinaus signalisiert.

## Was wir abdecken

- **Verschachtelte Unteragenten mit konfigurierbarer Tiefe** – wie Agenten jetzt Spezialisten hervorbringen, Ergebnisse aggregieren und ohne Benutzerorchestrierung arbeiten können
- **Das Tool „config_manager“** – Lese-/Schreibzugriff für die Laufzeitkonfiguration, der eine dynamische Agentenspezialisierung ermöglicht
- **Hybrid BM25 + Vektorsuche** – warum der Abruf von exakten Übereinstimmungen jetzt neben semantischer Ähnlichkeit zuverlässig funktioniert
- **Einbettung von Cache und adaptiver Komprimierung** – die Infrastrukturänderungen, die einen Kontextverlust während der Sitzung verhindern
- **Pluggable ContextEngine-Schnittstelle** – die Builder-Flucht für benutzerdefinierte Speicher-Backends
- **OpenAI-Kompatibilitätsebene** – „/v1/models“ und „/v1/embeddings“ als native Gateway-Endpunkte
- **Selbsthosting mit EXO-Clustern** – Qwen3.5-27B-Destillat läuft als Drop-in-OpenAI-Ersatz
- **Microsoft Teams SDK-Migration** – Streaming-Antworten, Willkommenskarten, Tippindikatoren, KI-Beschriftung
- **Discord Components v2** – native Schaltflächen, Dropdowns und interaktive Modalitäten
- **Feishu/Lark-Unterstützung** – OpenClaw erreicht asiatische Unternehmensmärkte
- **iOS-Alpha-Knoten-App** – OpenClaw läuft als aktiver Knoten auf dem iPhone

## Links und Ressourcen

- **OpenClaw-Dokumentation** – [https://docs.openclaw.dev](https://docs.openclaw.dev)
- **OpenClaw GitHub** – [https://github.com/openclaw-dev/openclaw](https://github.com/openclaw-dev/openclaw)
- **Qwen3.5-27B Destillation** – [https://www.modelscope.cn/models/Qwen/Qwen3.5-27B-Distill](https://www.modelscope.cn/models/Qwen/Qwen3.5-27B-Distill)
- **LangChain** – [https://www.langchain.com](https://www.langchain.com)
- **LlamaIndex** — [https://www.llamaindex.ai](https://www.llamaindex.ai)
- **WebUI öffnen** – [https://openwebui.com](https://openwebui.com)
- **Microsoft Teams SDK** – [https://learn.microsoft.com/en-us/microsoftteams/platform/](https://learn.microsoft.com/en-us/microsoftteams/platform/)
- **Feishu / Lark** – [https://www.feishu.cn](https://www.feishu.cn) / [https://www.larksuite.com](https://www.larksuite.com)
- **EXO-Cluster-Dokumentation** – [https://docs.openclaw.dev/hardware/exo-cluster](https://docs.openclaw.dev/hardware/exo-cluster)
- **OpenClaw iOS App (Alpha)** – [https://openclaw.dev/ios](https://openclaw.dev/ios)
- **ContextEngine-Schnittstellendokumente** – [https://docs.openclaw.dev/core/context-engine](https://docs.openclaw.dev/core/context-engine)
- **Notizen und Episodenarchive anzeigen** – [https://tobyonfitnesstech.com](https://tobyonfitnesstech.com)

## Kapitel

- „[00:00]“ Hook – The Shift: Warum sich der 24. März von .22/.23 unterscheidet
- „[02:30]“ Segment 1 – Agents Spawning Agents: Verschachtelte Subagenten, config_manager, Workflow-Szenarien, Tiefenbegrenzungsrisiken
- „[10:00]“ Segment 2 – Speicher wird real: Hybride BM25+Vektorsuche, eingebetteter Cache, adaptive Komprimierung, ContextEngine-Pluggabilität
- „[19:00]“ Segment 3 – OpenAI Compat Layer & Self-Hosting: Native „/v1/models“ und „/v1/embeddings“, Modellüberschreibungsweiterleitung, EXO-Cluster als OpenAI-Ersatz, iOS-Knoten-App
- „[24:00]“ Segment 4 – Plattformreife: Teams SDK (Streaming, Willkommenskarten, Tippindikatoren, KI-Beschriftung), Discord Components v2, Feishu/Lark-Unterstützung
- „[30:00]“ Outro / Builder's Take: NOVAs heiße Version von Nested Agents + Memory, ALLOYs Komplexitäts-Kontrapunkt, CTA an tobyonfitnesstech.com

## Gastgeber

- **NOVA** – Moderator, analytisch und prägnant
- **ALLOY** – Co-Moderator, praktisch veranlagt und leicht skeptisch