OPENCLAW DAILY — EPISODE 041 — 27. April 2026

[00:00] INTRO / HOOK
Heute schreiben wir die Tagesordnung um, denn es gibt jetzt OpenClaw v2026.4.25,
und das ist ein viel besserer Einstieg, als zu versuchen, eine beliebige Enterprise-KI-M&A-
Meldung auf den ersten Platz zu zwängen.

Diese Version ist kein einzelnes sauberes Headline. Es ist ein System-Release. Voice wird ernsthafter.
Plugin-Start wird kälter und schneller. Observability wird breiter. Browser-Automatisierung wird sicherer.
Setup wird glatter. Install- und Update-Pfade werden schwerer zu brechen. Und die Codex-Integration
kommt einen weiteren Schritt näher an natives App-Server-Verhalten.

Dann nutzen wir das als Brücke zu Codex selbst. Die Codex-App ist nicht mehr nur ein IDE-Helfer.
Der Funktionsumfang beginnt, wie eine Engineering-Workspace auszusehen: Worktrees, App-Server-Threads,
Sticky Environments, Permission Profiles, Automations, Plugin Marketplaces, eingebautes Git, Terminals
und ein In-App-Browser für visuelles Feedback.

Danach zoomen wir heraus: Meta reserviert zukünftige Kapazitäten von einem Space-Solar-Startup,
denn KI-Compute wird zum Energie-Logistik-Problem. Und wir enden damit, dass Autohersteller KI in
tatsächlichen Design- und Simulationsschleifen nutzen, nicht nur um hübsche Auto-Renderings zu erstellen.

[02:00] STORY 1 — OpenClaw v2026.4.25 Makes the Runtime Feel More Production-Ready
OpenClaw v2026.4.25 ist ein großes Release, aber das Thema ist überraschend klar:
Mache den Agent-Runtime im echten Leben einfacher zu betreiben.

Das erste offensichtliche Element ist Voice. Dieses Release verbessert TTS in der gesamten Stack.
Es gibt `/tts latest` zum Lautlesen der neuesten Antwort, Chat-scoped Controls wie `/tts chat on`,
`/tts chat off` und `/tts chat default`, per-Agent- und per-Account-Overrides, und eine größere
Provider-Oberfläche: Azure Speech, Xiaomi, Local CLI TTS, Inworld, Volcengine oder BytePlus Seed Speech
und ElevenLabs v3.

Das ist wichtig, weil Voice keine Novelty-Layer mehr ist. Wenn Agents in WhatsApp, Telegram,
Discord, Anrufen, Talk Mode und Live-Collaboration-Oberflächen unterwegs sind, muss Voice per
Kontext konfigurierbar sein. Das Voice, das du für einen persönlichen Assistenten willst, ist nicht
notwendigerweise das Voice, das du in einem Gruppenchat, einem Telefonanruf, einem Feishu-Workflow
oder einem Bot-Account willst. v2026.4.25 bewegt TTS in Richtung dieses realistischeren Modells:
geteilte Provider-Credentials, aber lokale Kontrolle über Voice, Provider, Persona, Account und
Channel-Verhalten.

Das zweite große Element ist Plugin-Startup. OpenClaw verlagert Plugin-Startup, Provider-Discovery,
Install-Metadaten und Repair-Flows auf eine persistierte Cold Registry. Einfach ausgedrückt:
Normaler Startup sollte nicht eine große Plugin-Universe durchsuchen und eine Menge Runtime-Code
importieren müssen, nur um Fragen zu beantworten wie: Was ist installiert, welchem Provider gehört
dieses Modell, oder welche Setup-Optionen sind verfügbar.

Das ist nicht glamourös, aber es ist genau die Art von Engineering, die einen Runtime schnell und
vorhersehbar macht. Das Release fügt `openclaw plugins registry` hinzu, ändert `plugins list`, um
standardmäßig die Cold Registry zu lesen, aktualisiert den Index nach Chat- und CLI-Plugin-Änderungen
und weist Operatoren auf Registry Repair anstatt auf alte Break-Glass-Switches hin. Der
Produkt-Point ist einfach: Plugin-Systeme sind nur mächtig, wenn sie nicht jeden Startup,
Status-Check oder Setup-Prompt in einen langsamen Full-Runtime-Scan verwandeln.

Das dritte Element ist Observability. OpenTelemetry-Coverage erweitert sich über Model-Calls,
Token-Nutzung, Tool-Loops, Harness-Runs, Exec-Prozesse, Outbound-Delivery, Context-Assembly und
Memory Pressure. Der wichtige Detail ist, dass das Release die Attributes bounded und low-cardinality
hält. Es versucht, Grafana, Prometheus, Traces und Metrics nützlich zu machen, ohne Prompts,
Responses, Session-Identifiers, Command-Text, Recipient-Data oder raw Provider-Request-IDs zu
leaken.

Das ist die richtige Richtung für Agent-Infrastruktur. Wenn Agents Jobs ausführen, Tools aufrufen,
Subagents spawnen, Nachrichten senden, Browser-Tabs verwalten und Modelle von mehreren Providern
nutzen sollen, müssen Operatoren grundlegende Fragen beantworten können: Wo ist die Latenz
hingegangen, welcher Agent verbraucht Tokens, schlagen Model-Calls fehl, hat ein Exec-Prozess
aufgehangen, ist eine Delivery fehlgeschlagen, wächst die Context-Assembly, steigt der
Memory Pressure. Aber Diagnostics können nicht zu einem zweiten Data Leak werden.

Browser-Automatisierung bekommt ebenfalls ein meaningful Reliability Pass: Sicherere Tab-URLs in
Agent-Responses, iframe-aware Role Snapshots, CDP-native Role Snapshot Fallback,
Cursor-clickable Detection, Target Attach Preparation, tiefere `browser doctor --deep`-Untersuchung,
Headless One-Shot Launch Support und mehr Tuning für langsame Hosts wie Raspberry Pi. Das ist eine
Builder Story, weil Browser-Automatisierung einer der Orte ist, wo Agents magisch aussehen, wenn es
funktioniert, und fragil, wenn nicht. Bessere Refs, bessere Diagnostics und sichereres Tab-Handling
sind die langweiligen Dinge, die Computer-Use Agents nutzbar machen.

Das Control UI und der Setup-Flow bekommen ebenfalls praktischen Schliff: PWA-Install-Support,
Web-Push-Benachrichtigungen für Gateway-Chat, Crestodian First-Run Repair, TUI-Setup,
Context-Mode-Auswahl, Fortschrittsanzeigen und eine kürzere Startup-Begrüßung.
Und die Install/Update-Hardening-Liste ist riesig: Windows Scheduled-Task-Verhalten,
macOS LaunchAgent Token Rotation, Linux Service-Setup, Docker-Packaging, Node Service Restarts,
Bundled Plugin Runtime Dependencies, Mixed-Version Gateway Verification, Low-Disk-Warnungen und
Post-Update Doctor Repairs.

Der Takeaway ist, dass v2026.4.25 nicht versucht, mit einer einzelnen Demo zu gewinnen. Es versucht,
OpenClaw als tägliches Agent-Betriebssystem zuverlässiger zu machen. Voice, Plugins, Diagnostics,
Browser Control, Setup, Updates, Codex und Channels haben sich alle weiterentwickelt.

→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.25

[12:00] STORY 2 — Codex Is Turning into a Real App Platform
Die interessanteste Begleitgeschichte ist Codex, weil v2026.4.25 ein paar Codex-spezifische
Änderungen enthält und OpenAIs eigener Codex-Changelog in dieselbe Richtung zeigt.

OpenClaw erfordert jetzt Codex App-Server 0.125.0 oder neuer für den Codex Harness. Es deckt native
MCP `PreToolUse`-, `PostToolUse`- und `PermissionRequest`-Payloads durch den OpenClaw Hook Relay ab.
Es bringt Prompts und `agents_list` bei, native Codex App-Server-Verfügbarkeit anzuzeigen, sodass
Agents den nativen `/codex`-Path bevorzugen können, anstatt auf ältere Codex ACP-Paths
zurückzufallen, es sei denn, ACP ist explizit. Es fixt auch moderne Codex Reasoning Controls,
bereitet native Codex Sub-Agent-Metadaten vor, verbessert App-Server Error Handling und
verschärft Codex Media- und Approval-Grenzen.

Das klingt eng, bis man es damit verbindet, was Codex selbst wird. OpenAIs Codex CLI 0.125.0 fügt
App-Server-Integrations-Arbeit rund um Unix-Socket-Transport, pagination-friendly Resume und Fork,
Sticky Environments, Remote Thread Config und Thread Store Plumbing, Plugin Marketplace Install und
Upgrade, und Permission Profiles hinzu, die Round-Trip durch TUI-Sessions, User Turns, MCP
Sandbox State, Shell Escalation und App-Server-APIs machen.

Die App-Feature-Docs machen die Produktform klarer. Die Codex-App wird als Desktop-Erlebnis für das
parallele Arbeiten an Codex-Threads beschrieben, mit Projects, Worktrees, Automations, Git-Features
und einem integrierten Terminal. Du kannst lokale Tasks direkt in einem Project ausführen,
Experimente in Git Worktrees isolieren oder Remote Cloud Work ausführen. Der Diff-Pane lässt dich
Änderungen überprüfen, inline kommentieren, Chunks stage oder reverten, committen, pushen und Pull
Requests erstellen. Das Terminal ist auf das Project oder Worktree begrenzt, und Codex kann
Terminal-Output lesen, sodass ein fehlgeschlagener Test oder ein laufender Dev-Server Teil des
Thread-Kontexts wird.

Der In-App-Browser ist ein weiteres wichtiges Element. Er bietet dem Benutzer und Codex eine gemeinsam gerenderte Ansicht einer Webseite innerhalb des Threads. Das bedeutet, dass eine Frontend-Aufgabe eine visuelle Vorschau und visuelle Kommentare enthalten kann, ohne ständig zwischen Editor, Terminal, Browser und Chat wechseln zu müssen. Er ist nicht dafür gedacht, Ihren eingeloggten persönlichen Browser für alles zu ersetzen, aber für lokale Dev-Server, dateibasierte Vorschauen und öffentliche Seiten schließt er die Schleife zwischen Codeänderung, visueller Überprüfung und Folgeanweisungen.

Das ist die größere Geschichte: Coding-Agents bewegen sich von Autovervollständigung und Chat zu Arbeitsflächen. Die Features, die wichtig sind, umfassen nicht nur Modellqualität. Es sind Isolation, Überprüfung, Genehmigungen, Observability, Umgebungsverwaltung, Threading, Resume/Fork-Verhalten und die Fähigkeit, mehrere Arbeitselemente auszuführen, ohne den aktuellen Checkout des Benutzers zu überschreiben.

Deshalb ist Codex App-Server-Unterstützung innerhalb von OpenClaw wichtig. Wenn Codex zu einer nativen App-Plattform für Engineering-Aufgaben wird, dann möchte OpenClaw Arbeit durch den besten verfügbaren Rahmen dorthin leiten, Berechtigungsereignisse bewahren, Hooks behandeln und native Verfügbarkeit für Agents bereitstellen. Die interessante Frage ist nicht mehr „Kann eine KI eine Funktion schreiben?" Sie lautet „Kann ein KI-Arbeitsbereich einen chaotischen Software-Job von Intent über Diff bis Test, Überprüfung und Deployment ohne Kontrollverlust durchführen?"

→ https://developers.openai.com/codex/changelog
→ https://developers.openai.com/codex/app/features
→ https://developers.openai.com/codex/app/browser

[21:00] STORY 3 — Meta Reserves Space-Beamed Solar Capacity for AI Data Centers
Jetzt zoom heraus von Software-Operationen zu Energie-Operationen.

Meta hat eine Kapazitätsreservierung mit Overview Energy unterzeichnet, einem Startup, das an Satelliten arbeitet, die Solarenergie im Orbit sammeln und Nahinfrarotlicht auf große Solarfarmen herabstrahlen würden. Diese Solarfarmen würden dann das Licht in Strom umwandeln, unter Verwendung terrestrischer Solarinfra struktur, und möglicherweise Solarstrom nachts für Rechenzentrumskunden produzieren.

Die Schlagzeile ist seltsam, aber der Druck darunter ist sehr normal: KI-Rechenzentren benötigen enorme Mengen zuverlässiger Elektrizität. TechCrunch berichtet, dass Metas Rechenzentren im Jahr 2024 mehr als 18.000 Gigawattstunden Strom verbraucht haben und dass das Unternehmen sich verpflichtet hat, 30 Gigawatt erneuerbare Energiequellen aufzubauen, mit Fokus auf industrieller Großskaliger Solar. Die Herausforderung ist, dass KI-Computing nicht bei Sonnenuntergang aufhört.

Overview's Ansatz unterscheidet sich von klassischen Mikrowellen-Weltraum-Solar-Konzepten. Das Unternehmen spricht davon, gesammelte orbitale Solarenergie in einen breiten Nahinfrarotstrahl umzuwandeln, der auf große Solaranlagen gerichtet ist, anstatt einen dichten Strahl auf einen kleinen Empfänger zu feuern. Die Meta-Reservierung ist für bis zu einem Gigawatt zukünftiger Leistung. Overview plant eine Demonstration im niedrigen Erdorbit 2028 und hofft, um 2030 mit dem Start von Satelliten für die Meta-Verpflichtung zu beginnen.

Der Zeitplan ist wichtig. Dies ist keine kurzfristige Lösung für die heutigen Netzwerkengpässe. Es ist ein Signal. Hyperscaler kaufen nicht mehr nur GPUs, Rechenzentrumsstandorte und Netzwerke. Sie kaufen zukünftige Energie-Optionalität.

Die Builder-Lektion ist, dass KI-Produktstrategie und Energiestrategie verschmelzen. Jeder Always-On-Agent, Videogenerator, Echtzeit-Assistent, Langkontext-Workflow und Hintergrundautomatisierungsloop hat ein Stromprofil. Der Benutzer sieht einen Button. Der Operator sieht einen Modellaufruf. Das Infrastrukturteam sieht einen Cluster. Das Energieteam sieht Last, Intermittenz, Netzwerkbeschränkungen, Batterien, Genehmigungen und langfristige Stromverträge.

Also unabhängig davon, ob Weltraum-Solar in Overview's Zeitplan Realität wird, ist Metas Schritt interessant, weil er zeigt, wie weit die Suche nach KI-Strom expandiert. Die Zukunft von Compute könnte genauso sehr von Strombeschaffung abhängen wie von Chips.

→ https://techcrunch.com/2026/04/27/meta-inks-deal-for-solar-power-at-night-beamed-from-space/

[29:00] STORY 4 — AI-Designed Cars Move from Concept Art into Industrial Feedback Loops
Die letzte Geschichte ist eine bessere Version einer KI-in-der-Industrie-Geschichte, weil es nicht nur darum geht, Bilder zu machen. Es geht darum, Feedback-Schleifen zu verkürzen.

The Verge berichtet darüber, wie GM, Nissan und Neural Concept KI im Fahrzeugdesign und in der Fahrzeugentwicklung einsetzen. Der alte Fahrzeugentwicklungszyklus kann fünf Jahre oder länger dauern: Skizzen, Design-Reviews, 3D-Modelle, Ton, Simulation, Engineering, Software, Fertigungsbeschränkungen und weitere Reviews. Dieser Zyklus ist schmerzhaft, wenn Vorschriften, Zölle, E-Auto-Anreize, Verbrauchernachfrage und Softwareanforderungen schneller wechseln als das Autoprogramm.

GM's Designer verwenden Tools wie Vizcom, um menschliche Skizzen schneller in reichhaltigere 3D-Modelle und Animationen umzuwandeln. Der Schlüssel-Detail ist, dass die menschliche Skizze immer noch den Prozess startet. KI hilft dem Team, Möglichkeiten früher zu sehen, mehr Richtungen zu vergleichen und internes visuelles Material zu erstellen, ohne auf eine langsame Übergabekette zu warten.

Der operativere Teil ist Simulation. Neural Concept verwendet neuronale Netzwerke, um numerische Strömungsmechanik zu beschleunigen. The Verge berichtet, dass Jaguar Land Rover aerodynamische Jobs beschrieb, die früher vier Stunden dauerten und jetzt etwa eine Minute dauern, und GM entwickelt einen KI-gesteuerten virtuellen Windkanal, der Designern near-instant Feedback zu Luftwiderstand geben kann, wenn sich Oberflächen ändern.

Das ist die wichtige Verschiebung. Wenn aerodynamisches Feedback ankommt, während Designer noch Formen erkunden, können schlechte Richtungen früher verworfen und vielversprechende verfeinert werden, bevor das Design eingefroren wird. KI ist wertvoll, nicht weil sie ein Auto einmal zeichnet, sondern weil sie dem Team ermöglicht, mehr Versionen zu testen, während die Kosten für Änderungen noch gering sind.

Nissan's Winkel ist softwaredefinierte Fahrzeuge. Es verwendet Code-Generierungstools für Softwareaufgaben auf niedrigerer Ebene wie Unit-Tests, mit dem Ziel, Entwicklungsgeschwindigkeit und -qualität zu verbessern. Das ist wichtig, weil moderne Autos zunehmend Softwaresysteme sind, und Softwareintegration ist dort, wo Programme abrutschen können.

Die Vorsicht ist, dass diese Workflows immer noch menschliche Aufsicht benötigen. Schnellere Iteration kann bessere Produkte schaffen, aber sie kann auch schlechte Annahmen verstärken oder den Druck auf Arbeiter erhöhen. Der nützliche Rahmen ist, dass KI in industrielle Schleifen eintritt, wo das Output nicht das finale Artefakt ist. Das Output ist ein früheres Signal, das Menschen hilft zu entscheiden, was als nächstes zu tun ist.

→ https://www.theverge.com/transportation/918411/gm-ai-car-design-nissan-neural-concept

[36:00] OUTRO / CLOSE
Das war die Episode.

OpenClaw v2026.4.25 führt, weil es die Runtime über Sprachausgabe, Plugins,
Observability, Browser-Automatisierung, Setup, Updates und Codex produktionsreifer
erscheinen lässt. Codex selbst entwickelt sich zu einer echten Engineering-App-
Plattform mit Worktrees, Automatisierungen, Git-Review, App-Server-Threads,
Berechtigungsprofilen und Browser-Workflows direkt in der App. Metas Raumfahrt-
Solar-Wette zeigt, wie seltsam die KI-Infrastrukturplanung wird, wenn Strom zum
Engpass wird. Und KI-gestaltete Autos zeigen das stärkste industrielle KI-Muster:
nicht einmalige Generierung, sondern schnellere, menschlich überwachte
Feedback-Schleifen.

→ Antworten Sie hier, um die Transkriptgenerierung zu genehmigen.