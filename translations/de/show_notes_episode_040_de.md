OPENCLAW DAILY — EPISODE 040 — April 26, 2026

[00:00] INTRO / HOOK
OpenClaw v2026.4.24 ist die neueste stabile Version, und da v2026.4.23 bereits in den kürzlichen Episodennotizen behandelt wurde, ist v2026.4.24 der einzige gültige Versionsblock am Anfang von EP040.

Und es verdient diesen Platz, indem es Echtzeit-Zusammenarbeit viel greifbarer macht. Google Meet wird zu einer gebündelten OpenClaw-Oberfläche, Talk und Voice Call können während Live-Sprachsitzungen den vollständigen Agenten konsultieren, Browser-Automatisierung wird stabiler und die Modell-Plus-Plugin-Infrastruktur wird leichter und expliziter.

Nach dem Deep Dive in die Version gehen wir zu Anthropics Project Deal Marketplace-Experiment, Claudes persönlichen App-Connectors und dem Marktsignal hinter ComfyUIs letzter Finanzierungsrunde über.

[01:30] STORY 1 — OpenClaw v2026.4.24 macht Live-Meetings und Sprachsitzungen wesentlich praxistauglicher
Das Zentrum von v2026.4.24 ist Google Meet.

OpenClaw wird jetzt mit einem gebündelten Google Meet Teilnehmer-Plugin ausgeliefert, mit persönlicher Google-Authentifizierung, expliziten Meeting-Beitritten, Chrome- und Twilio-Echtzeittransporten, Unterstützung für gepaarte Knoten in Chrome, Export von Artefakten und Teilnehmerdaten sowie Wiederherstellungstools für bereits geöffnete Tabs. Das ist keine kleine Plugin-Ergänzung. Es ist OpenClaw, das eine Live-Zusammenarbeitsoberfläche in etwas verwandelt, das die Runtime tatsächlich besitzen kann.

Der praktische Unterschied ist enorm.
Ein Meeting-Tool ist nur wertvoll, wenn es die unordentlichen Teile rund um das Meeting bewältigen kann, nicht nur den idealisierten Beitrittsbutton. Diese Version fügt Browser-Zustandswiederherstellung, OAuth-Doctor-Flows, `recover_current_tab`, Teilnehmer- und Konferenzaufzeichnungs-Workflows, Transkript- und Aufnahmeexport sowie die Möglichkeit hinzu, bereits geöffnete Meet-Tabs zu inspizieren, anstatt blind Duplikate zu öffnen. Das sind die Art von Details, die ein Feature von „vorführbar" zu „operierbar" verschieben.

Und OpenClaw behandelt Meet nicht als isolierte Insel.
Talk, Voice Call und Google Meet können jetzt Echtzeit-Sprachschleifen verwenden, die den vollständigen OpenClaw-Agenten für tiefere toolgestützte Antworten konsultieren. Das ist wichtig, weil es die Obergrenze dessen verändert, was eine Live-Audiositzung leisten kann. Anstatt in einer dünnen Echtzeit-Modellinteraktion festzustecken, kann die Sitzung an den vollständigen Agenten übergeben, wenn sie breiteres Gedächtnis, Tools oder bewusstere Arbeit benötigt. Das lässt Live-Sprache weniger wie eine Neuheiten-Schnittstelle und mehr wie eine ernsthafte Frontend für den Rest des Systems erscheinen.

Es gibt hier auch eine Geschichte mit gepaarten Knoten, die für echte Operatoren wichtig ist.
Die Version unterstützt explizit Chrome-Knoten-Style-Setups für Hosts, die spezialisiertes Chrome, Audi-Routing oder VM-ähnliche Umgebungen benötigen. Das ist genau die Art von realem Bereitstellungsdetail, das Ihnen sagt, dass das Feature für unordentliche Umgebungen konzipiert wurde, nicht nur für einen einzigen sauberen Laptop-Pfad.

[10:30] STORY 1B — Browser-Steuerung, DeepSeek-Kataloge und Startup-Plumbing werden alle geschärfter
Der nächste große Strang in v2026.4.24 ist, dass OpenClaw die Reibung in der Art und Weise, wie Agenten tatsächlich auf die Welt einwirken, weiter reduziert.

Browser-Automatisierung erhält Koordinaten-Klicks, längere Standard-Aktionsbudgets, pro-Profil Headless-Overrides, stabilere Tab-Wiederverwendung und stärkere Wiederherstellung für veraltete Sitzungen und Sperren. Das klingt inkrementell, bis Sie sich daran erinnern, wie oft Browser-Automatisierung genau an diesen Kanten scheitert. Ein Browser-Tool wird nützlich, wenn Agenten lange Wartezeiten überstehen, veraltete Anhänge wiederherstellen, das richtige Tab wiederverwenden und sich trotzdem weiterbewegen können, ohne dass der Operator jeden kaputten Zustand beaufsichtigen muss.

Diese Version treibt Browser-Operationen auch in Richtung klarerer Operator-Kontrolle.
Es gibt Doctor-Diagnosen, stärkere Sicherheitsgrenzen bei Browser-Anfragen, bessere Screenshot-Timeout-Behandlung, stabilere Tab-Identifiers und robusteres Verhalten bei bestehenden Sitzungen. Also gewinnt die Browser-Oberfläche nicht nur Features. Sie gewinnt ein zuverlässigeres Betriebsmodell.

Die Modell-Katalogseite bewegt sich ebenfalls.
DeepSeek V4 Flash und V4 Pro treten in den gebündelten Katalog ein, wobei V4 Flash zum Onboarding-Standard wird, während Replay- und Thinking-Verhalten für Follow-up-Tool-Call-Runden korrigiert werden. Das ist wichtig, weil Modellverfügbarkeit nur ein Teil der Geschichte ist. Operatoren brauchen, dass die Runtime Reasoning-Verhalten sauber über Multi-Turn-Sitzungen, Tool-Calls und replay-sensitive Provider hinweg bewahrt. Sonst ist eine neue Modellzeile größtenteils dekorativ.

Dann gibt es noch die Startup- und Katalog-Plumbing.
OpenClaw bewegt sich weiter in Richtung statischer Kataloge, manifest-basierter Modellzeilen, trägerer Provider-Abhängigkeiten und leichterer verpackter Installationen. Das ist gute Runtime-Architektur. Es bedeutet, dass das Auflisten von Modellen, das Lesen von Setup-Metadaten und das Inspizieren von Fähigkeiten ohne immer schweren Plugin-Laufzeitzustand in den Speicher zu ziehen, passieren kann. Auf Produktebene macht das das System schneller. Auf Architekturebene macht es Fähigkeiten inspizierbarer und weniger magisch.

[18:30] STORY 1C — Die Fixes zeigen, dass OpenClaw die Runtime strafft, nicht nur erweitert
Viel des echten Werts in v2026.4.24 lebt in der Fix-Liste.

Heartbeat-Scheduling wird gegen überdimensionierte Timer und Prompt-Leakage gehärtet. Restart-Fortsetzungen werden dauerhafter. Sitzungs- und Transkript-Handling werden weniger fragil. Telegram, Discord, Slack, WhatsApp und Browser-Pfade erhalten alle spezifische Zuverlässigkeitsverbesserungen. DeepSeek Replay wird korrigiert. Bestehende Browser-Sitzungen hören auf, zukünftige Anhänge zu vergiften. Lang laufende lokale oder Provider-Aufrufe erben besseres Timeout-Verhalten. Und isolierte Cron-Runs hören auf, veralteten Zustand von früheren Sitzungen durchsickern zu lassen.

Es gibt auch eine wichtige operator-facing Bereinigung rund um Modelle.
`/models add` ist deprecated, anstatt stillschweigend Modellkonfiguration aus dem Chat zu mutieren, während manifest-bezogene Zeilen und Read-only-Listen-Verbesserungen Modell-Oberflächen expliziter machen. Das ist eine gesunde Korrektur. Die Runtime wird mächtiger, aber sie wird auch in Richtung klarerer Eigentumsgrenzen geschoben, darüber, was im Chat passieren sollte, was in Setup passieren sollte und was als Konfiguration auditierbar sein sollte.

Die Version enthält sogar eine echte breaking Change für Plugin-Entwickler.
Der alte Pi-only eingebettete Extension-Factory-Kompatibilitätspfad wird zugunsten der Agent-Tool-Result-Middleware-Route mit Harness-Deklarationen entfernt. Das ist nicht nur Bereinigung um der Bereinigung willen. Es ist Teil von OpenClaws Versuch, Pi- und Codex-Style-Runtimes auf einem ehrlicheren gemeinsamen Vertrag zu halten, anstatt legacy Kompatibilitäts-Säume ewig abdriften zu lassen.

Also die praktische Leseart zu v2026.4.24 ist unkompliziert.
Dies ist eine Version über das Praxistauglicher-Machen von Live-Oberflächen, Zuverlässiger-Machen von Browser-Automatisierung, Lesbarer-Machen von Modell- und Plugin-Infrastruktur und weniger Überraschend-Machen der Runtime unter realer Last.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.24

[26:30] STORY 2 — Anthropics Project Deal testet, was passiert, wenn Agenten für Menschen verhandeln
Anthropics Project Deal ist leicht als skurriles internes Experiment abzutun.
Das wäre ein Fehler.

Das Unternehmen sagt, es habe einen geheimen internen Marktplatz betrieben, auf dem KI-Agenten sowohl als Käufer als auch als Verkäufer auftraten, echte Geschäfte abschlossen und über echten Wert für einen selbst ausgewählten Mitarbeiterpool verhandelten. Anthropic sagt, dass 186 Geschäfte abgeschlossen wurden, die einen Gesamtwert von mehr als 4.000 Dollar hatten, wobei die Teilnehmer ein kleines Budget erhielten und die Transaktionen nach dem Experiment tatsächlich honoriert wurden.

Der Grund, warum dies relevant ist, liegt nicht in der absoluten Größenordnung.
Der Grund, warum es relevant ist, liegt in der Form des Tests. Es geht nicht darum, ob ein Agent Fragen beantworten oder Buttons klicken kann. Es ist ein Test für Verhandlung, Repräsentation, Asymmetrie, Anreize und delegierte wirtschaftliche Handlungen.

Anthropic sagt, dass fortschrittlichere Modelle tendenziell objektiv bessere Ergebnisse erzielten, während die Benutzer auf der schwächeren Seite nicht unbedingt erkannten, dass sie benachteiligt wurden. Das sollte sofort Aufmerksamkeit erregen. Wenn Qualitätsunterschiede bei Agenten in Verhandlungssituationen Realität werden, dann zeigt sich der nächste Version des Modellvorteils möglicherweise nicht nur als bessere Prosa oder höhere Benchmark-Ergebnisse. Es könnte sich als wer das bessere Geschäft auf einem automatisierten Markt macht.

Das hat offensichtliche Implikationen für Entwickler.
Sobald Agenten anfangen zu kaufen, verkaufen, Anfragen zu leiten, Verfügbarkeit zu verhandeln oder zu entscheiden, welchen Gegenparteien sie vertrauen, wird die Qualität des Agenten zu einer wirtschaftlichen Frage. Fairness, Transparenz und Handlungsüberprüfung werden viel wichtiger, weil ein Benutzer möglicherweise nicht erkennen kann, wenn sein Agent systematisch gegen einen besseren unterperformt.

Also sieht Project Deal klein aus, aber es zeigt auf eine größere zukünftige Kategorie: Agent-Marktplätze, wo die echte Frage nicht nur ist, ob Agenten handeln können, sondern ob sie menschliche Interessen gut genug unter Wettbewerb repräsentieren können.
→ https://techcrunch.com/2026/04/25/anthropic-created-a-test-marketplace-for-agent-on-agent-commerce/

[32:30] STORY 3 — Claudes persönliche App-Connectoren erweitern die Vertrauensoberfläche
Anthropics andere relevante Maßnahme diese Woche ist viel produktnäher.

Claude erweitert sein Connector-Modell über Arbeits-Apps hinaus in persönliche Dienste wie Spotify, Uber, Instacart, AllTrails, TripAdvisor, Audible und TurboTax. Das ist relevant, weil es die Agent-Oberfläche näher an alltägliche Lebensaufgaben bringt, nicht nur an Unternehmenssoftware oder Entwickler-Workflows.

Die produktspezifische Bedeutung liegt in der Orchestrierungsschicht.
Sobald Claude mehrere verbundene Apps sehen und sie kontextbezogen vorschlagen kann, hört der Assistent auf, wie ein einzelnes Chat-Ziel auszusehen, und beginnt eher wie eine Koordinierungsschicht über Dienste hinweg auszusehen. Anthropic sagt, dass die verbundenen App-Daten nicht zum Trainieren seiner Modelle verwendet werden, dass Apps keine anderen Claude-Unterhaltungen eines Benutzers sehen, und dass Claude vor dem Ausführen von Aktionen wie Käufen oder Reservierungen um Verifizierung bittet. Diese Vertrauensgrenzen sind keine Randnotizen. Sie sind zentrale Produktanforderungen, wenn Agenten von der Empfehlung zur Aktion übergehen sollen.

Für Entwickler ist diese Geschichte relevant, weil sie verstärkt, wohin der Wettbewerb geht.
Das nächste Agent-Rennen geht nicht nur um klügere Raw-Modelle. Es geht darum, wer die Action-Oberfläche über Apps hinweg besitzen kann, während genug Vertrauen erhalten bleibt, dass Benutzer das System tatsächlich etwas Bedeutungsvolles tun lassen.

Deshalb sind Bestätigungsdesign, Connector-Scoping und App-übergreifender Kontext jetzt allesamt strategische Produktfragen.
→ https://www.theverge.com/ai-artificial-intelligence/917871/anthropic-claude-personal-app-connectors

[37:30] STORY 4 — ComfyUIs Bewertung ist eine Wette gegen rein promptbasierte kreative Workflows
Dass ComfyUI zu einer Bewertung von 500 Millionen Dollar aufgestockt hat, ist nicht nur Startup-Theater.
Es ist ein Signal darüber, wo der Wert in KI-Medien-Workflows noch liegt.

Das Pitch des Unternehmens ist, dass Prompt-only-Systeme oft den größten Teil des Weges zu einem Bild- oder Video-Ergebnis schaffen, aber nicht die letzte Meile, ohne jede Änderung in einen einarmigen Banditen-Reroll zu verwandeln. ComfyUIs knotenbasierter Workflow bietet viel granularere Kontrolle über einzelne Schritte im Generierungsprozess, und TechCrunch berichtet, dass das Unternehmen sagt, es habe jetzt mehr als 4 Millionen Nutzer.

Die tiefere Implikation ist, dass bessere Modelle nicht automatisch die Notwendigkeit von Kontrolloberflächen töten.
Tatsächlich können bessere Modelle die Nachfrage danach erhöhen, weil sobald die Basisqualität hoch genug ist, verschiebt sich der verbleibende Wert hin zu Wiederholbarkeit, Präzision und gezielten Bearbeitungen. Genau dort gewinnen knotenbasierte Systeme.

Für Entwickler und Betreiber ist das eine nützliche Erinnerung.
Wenn du rund um Bild-, Video- oder multimodale Outputs gestaltest, gibt es immer noch echte Nachfrage nach Workflows, die es Benutzern ermöglichen, die Pipeline zu steuern, zu inspizieren und zu verfeinern, anstatt jede Anpassung wieder in einen weiteren Prompt zu verwandeln.

Also ist ComfyUIs Bewertung wirklich eine These über Kontrolle.
Prompting bleibt die einfache Einfahrt. Aber produktionsqualität-kreative Arbeit will immer noch Oberflächen, die Absicht über mehrere Schritte hinweg bewahren können, ohne den Benutzer zu zwingen, jedes Mal die guten Teile des Ergebnisses zu verschleudern.
→ https://techcrunch.com/2026/04/24/comfyui-hits-500m-valuation-as-creators-seek-more-control-over-ai-generated-media/

[43:00] OUTRO / ABSCHLUSS
Das reicht für heute.
OpenClaw v2026.4.24 hat Live-Zusammenarbeit, Echtzeit-Sprache, Browser-Zuverlässigkeit und Katalog-Infrastruktur auf praktische Weise vorangebracht.
Anthropic hat Project Deal genutzt, um anzudeuten, was Agent-Märkte wirklich testen könnten.
Claude hat sich in persönliche App-Aktionen erweitert.
Und ComfyUI hat jeden daran erinnert, dass bessere Modelle nicht die Prämie auf Kontrolle löschen.

→ Antwort hier, um die Transkriptgenerierung zu genehmigen.