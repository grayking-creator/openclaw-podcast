Episode 125 — 25. Oktober 2026

[00:00] Hook der Episode

Nous Research hat Hermes Agent v0.22.5 am 22. Oktober 2026 veröffentlicht. Das Patch-Release umfasst 81 zusammengeführte Pull Requests für die CLI und die Installationsprogramme, die Microsoft Store-App, Docker und Hermes Cloud. Anthropic hat außerdem sandbox-runtime als Open-Source-Projekt veröffentlicht. Dabei handelt es sich um die Sandbox auf Betriebssystemebene hinter Claude Code, die den Datei- und Netzwerkzugriff von KI-Agenten, MCP-Servern und Befehlszeilenwerkzeugen einschränkt. OpenRouter hat Moonshot AI’s Kimi K3.1 Pro mit einem Kontextfenster von 1.048.576 Tokens hinzugefügt, während OpenAI eine Decisions API eingeführt hat, mit der Entscheidungsfindung in Anwendungen ergänzt werden kann – mit Schwerpunkt auf schnellen Antworten und gezielten Ergebnissen. Recursive folgte mit Flint, einem textbasierten Mixture-of-Experts-Codingmodell unter der Apache-2.0-Lizenz, das insgesamt 39,8 Milliarden Parameter und ungefähr 2,5 Milliarden aktive Parameter pro Token besitzt. Mistral hat Timestral-209M veröffentlicht, ein Zeitreihen-Fundierungsmodell für Zero-Shot-Prognosen, das eine oder mehrere verwandte Zeitreihen verarbeiten und externe Informationen einbeziehen kann.

[02:00] Agent Stack Release Readout: Hermes Agent v0.22.5, v0.22.4, v0.22.3

Hermes Agent v0.22.5, veröffentlicht von Nous Research am 22. Oktober 2026, vereint 81 zusammengeführte Pull Requests und 30 geschlossene Issues in 231 Nicht-Merge-Commits und 804 geänderten Dateien. Es aktualisiert die CLI und die Installationsprogramme, die Microsoft Store-App, Docker und Hermes Cloud.

Die folgenreichste Änderung ist die austauschbare Delegierung. Hermes kann Aufgaben mithilfe von Modellzuordnungen oder -profilen an Subagenten weiterleiten, wobei die ausgewählte Weiterleitung für jede Sitzung geändert werden kann. Dadurch können Entwickler unterschiedliche Modelle oder Profile je nach Aufgabe trennen, ohne jedes Backend als Teil der Kernanwendung behandeln zu müssen.

Auch das Plugin-System wird leistungsfähiger. Plugins können Slash-Befehle mit auswählbaren Optionen bereitstellen, Hermes über das Model Context Protocol bereitstellen und vorhandene Agenten importieren. Der Einrichtungsablauf kann einen Importeur anbieten, wenn er einen anderen Agenten erkennt. Desktop erhält außerdem die Installation von Plugins mit einem Klick, Stufenabzeichen und Steuerelemente zum Anheften per Drag-and-Drop in der Seitenleiste.

Die Konten- und Sitzungsverwaltung wird ebenfalls klarer. Die Anmeldung verwendet jetzt die normale Geräteanmeldung, Gastkonten im kostenlosen Tarif können ihre Arbeit einem Konto übergeben, und das Ergebnis zeigt, wer angemeldet ist. Connectors bieten eine Anmeldung an, statt stillschweigend eine Gastsitzung zu öffnen. Tarife mit Nutzungsfenster erhalten Anzeigen, Limit-Karten und eine Wiederherstellungsfunktion beim Modellwechsel.

Hermes Agent v0.23.0 ist der nächste Meilenstein, auf den zu achten ist, da Nous Research nach eigener Angabe die vollständigen kuratierten Hinweise zu den in diesen Releases zusammengefassten Änderungen enthalten wird.

[02:35] OpenRouter listet Kimi K3.1 Pro mit einem 1M-Token-Kontextfenster

OpenRouter hat Kimi K3.1 Pro aufgelistet. Das Registry beschreibt das Modell als Moonshot AIs multimodales Open-Weight-Reasoning-Modell der Spitzenklasse und als nachtrainierten Nachfolger von Kimi K3. Es wurde für längerfristige Coding-Aufgaben entwickelt und eignet sich daher besonders gut für umfangreiche Softwarearbeiten und große Codebasen. Die konkreteste Funktion ist ein Kontextfenster von 1.048.576 Tokens. Laut Registry-Architektur akzeptiert das Modell Text, Bilder und Video und erzeugt Text. Entwickler können somit unterschiedliche Materialien in denselben Prompt einbinden. Das ist relevant für Workflows, in denen Code, Screenshots und Video ein gemeinsames Ergebnis beeinflussen sollen. OpenRouter listet für Kimi K3.1 Pro einen Preis pro Token von 0,000002 US-Dollar für Prompts, 0,00001 US-Dollar für Completions und 0,0000002 US-Dollar für zwischengespeicherte Eingabelesevorgänge. Durch die Auflistung steht Kimi K3.1 Pro über OpenRouter zur Evaluierung bereit. Zunächst sind die Kontextgröße, die multimodale Eingabe und die Tokenkosten zu bewerten. Moonshot AI beschreibt Kimi K3.1 Pro als nachtrainierten Nachfolger von Kimi K3. Kimi K3.1 Pro akzeptiert Text, Bilder und Video, erzeugt Text und verfügt über ein Kontextfenster von 1M Tokens. OpenRouter listet Kimi K3.1 Pro in seiner Modell-Registry.

[03:42] Anthropic öffnet seine Agent-Sandbox über Container hinaus

Anthropic hat sandbox-runtime, kurz srt, als quelloffene Sandbox auf Betriebssystemebene für KI-Agenten veröffentlicht. Das Projekt ist die Sandbox hinter Claude Code und unterstützt Agenten, MCP-Server und Befehlszeilenwerkzeuge, ohne dass Container erforderlich sind.

Die zentrale Aufgabe ist unkompliziert: den für diese Werkzeuge verfügbaren Datei- und Netzwerkzugriff einschränken. Auf macOS verwendet es Seatbelt, den eigenen Sandbox-Mechanismus des Betriebssystems, auf Linux bubblewrap. Dasselbe Konzept steht daher in zwei wichtigen Desktop- und Serverumgebungen zur Verfügung, ohne dass Entwickler jeden Agenten oder jedes Werkzeug in einen Container verpacken müssen.

Für Entwickler verändert dies die Implementierungsoption beim Ausführen von agentengesteuertem Code. Statt einen Container einzusetzen, können Entwickler einen Agenten, einen Toolserver oder ein Befehlszeilen-Dienstprogramm in eine Sandbox auf Betriebssystemebene mit kontrolliertem Zugriff auf Dateien und Netzwerke versetzen. Anthropic stellt außerdem den Sandbox-Ansatz hinter Claude Code zur Überprüfung und Weiterverwendung bereit.

Der nächste Punkt, auf den zu achten ist, ist, wie Entwickler diese Zugriffseinschränkungen in realen Workflows mit den spezifischen Werkzeugen und Daten kombinieren, die ihre Agenten benötigen.

[04:44] OpenAI startet eine Decisions API für gezielte App-Entscheidungen

OpenAI hat die Decisions API eingeführt und damit App-Entwicklern eine dedizierte Schnittstelle für automatisierte Entscheidungen bereitgestellt. Das Unternehmen beschreibt sie als schnell, fokussiert und kostengünstig sowie als für unterschiedliche Arten von Anwendungen geeignet statt nur für einen engen Anwendungsfall.

Das ist wichtig, weil viele Produkte zu einem bestimmten Zeitpunkt eine kleine Entscheidung benötigen: Welche Option soll angezeigt werden, wie soll eine Anfrage weitergeleitet werden oder welche Aktion soll eine Anwendung ausführen? Die API gibt Teams eine weitere Komponente, die sie für solche Momente testen können, statt jede Entscheidung als Teil eines umfassenderen Workflows zu behandeln.

Für Entwickler sind die nächsten praktischen Prüfpunkte: Wie schnell antwortet die API, bleiben ihre Entscheidungen bei realen Workloads konsistent und was kosten diese Entscheidungen, wenn sie in ein livees Produkt integriert werden?

[05:29] Recursive bringt mit Flint einen 39,8B-Coding-Agenten für lokale Stacks

Recursive hat Flint unter der Apache-2.0-Lizenz veröffentlicht, und das Repository von Unsloth stellt dessen Checkpoint, Modellkonfiguration, Tokenizer, Chat-Vorlage und Serving-Kit bereit. Flint ist ein Mixture-of-Experts-Modell mit Text-Input und Text-Output, das für Coding-Agenten konzipiert ist. Es hat insgesamt 39,8 Milliarden Parameter, von denen pro Token ungefähr 2,5 Milliarden aktiv sind. Jede Mixture-of-Experts-Schicht enthält 256 weitergeleitete Experten, von denen pro Token sechs ausgewählt werden, sowie einen stets aktiven Shared Expert. Flint unterstützt Reasoning, die Nutzung von Tools in mehreren Dialogen und OpenAI-kompatible Tool-Aufrufe. Zu den Aufgaben gehören die Untersuchung von Codebasen, die Behebung von Fehlern, die Implementierung von Funktionen und das Schreiben von Tests. Recursive nennt 54,9 % bei Terminal-Bench 2.1, 89,7 % bei SWE-bench Pro v2 und 74,2 % bei SWE-bench Verified. Die Modellkarte weist darauf hin, dass die Evaluierungsumgebungen variieren und Flints Terminal-Bench-Ergebnis Lösungen, die durch Web-Recherche erzielt wurden, als erfolglos wertet, während einige von Entwicklern gemeldete Werte diese Anpassung möglicherweise nicht berücksichtigen. Die Gewichte unter Apache 2.0 sind über das GGUF-Repository von Unsloth verfügbar, einschließlich quantisierter Varianten für NVIDIA- und Apple-Silicon-Laufzeitumgebungen. Die Ergebnisse können je nach Checkpoint-Präzision und Inference-Laufzeit variieren, daher ist die konkrete Deployment-Konfiguration wichtig. Flint kann weiterhin fehlerhaften Code oder unangemessene Tool-Aufrufe erzeugen, weshalb Anwendungen eigene Berechtigungen und Ausführungsgrenzen benötigen. Flint ist ein textbasiertes Coding-Agenten-Modell, das Reasoning, die Nutzung von Tools in mehreren Dialogen und OpenAI-kompatible Tool-Aufrufe unterstützt.

[06:45] Timestral-209M von Mistral bringt lokale probabilistische Prognosen

Mistral hat Timestral-209M veröffentlicht, ein Zeitreihen-Grundlagenmodell für Prognosen ohne aufgabenspezifisches Fine-Tuning. Es ist das größte von vier dokumentierten Größenvarianten mit 5 bis 209 Millionen Parametern. Der Herausgeber erklärt, dass seine Zero-Shot-Prognoseergebnisse bei GIFT-Eval, TIME und fev-bench führend seien. Das Modell kann eine einzelne Zeitreihe oder mehrere miteinander verwandte Zeitreihen prognostizieren. Es akzeptiert außerdem zusätzliche Eingaben, die entweder bereits bekannt sind oder für die Zukunft geplant sind. Dadurch kann eine Anwendung Kontext über die Zielhistorie hinaus einbeziehen. Seine probabilistische Ausgabe umfasst 21 Quantile, sodass Software neben einer Medianprognose auch Unter- und Obergrenzen abrufen kann, statt eine einzelne Vorhersage als Gewissheit zu behandeln. Timestral akzeptiert bis zu 32.768 historische Zeitschritte und prognostiziert in einem Durchgang bis zu 1.024 Schritte. Längere Prognosen werden in Blöcken durchgeführt. Intern gruppiert das Modell jeweils 32 Schritte zu einem Patch und bettet sowohl die Werte als auch Indikatoren für fehlende Beobachtungen ein. Für Entwickler ist die wichtige Neuerung der lokale Einsatz über PyTorch auf einer CPU oder GPU. Mistral erklärt außerdem, den Quellcode für die Ausführung des Modells und die Reproduktion seiner Benchmark-Ergebnisse zu veröffentlichen. Damit kommt Timestral als Prognosekomponente für lokale Dienste und Agent-Stacks infrage, die Wahrscheinlichkeitsbereiche, künftige Zeiträume oder mehrere verwandte Signale benötigen und nicht mit einer einzelnen Punktschätzung auskommen. Mistral hat den Timestral-209M-Checkpoint veröffentlicht und erklärt, auch den Quellcode bereitzustellen. Timestral unterstützt uni- und multivariate Prognosen, Kovariaten nur aus der Vergangenheit sowie bekannte Kovariaten aus der Zukunft und probabilistische Vorhersagen über 21 Quantile. Der Herausgeber berichtet, dass Timestral-209M bei GIFT-Eval niedrigere MASE- und CRPS-Fehler als TimesFM-3 erzielte. Der Checkpoint läuft über PyTorch auf einer CPU oder GPU, und die Modelle werden unter einer modifizierten MIT-Lizenz veröffentlicht.

[08:26] OpenAI und NASK aus Polen gehen eine Partnerschaft für KI-Sicherheit ein

OpenAI und NASK aus Polen haben am 23. Oktober 2026 eine Partnerschaft zu KI-Sicherheit, Cybersicherheit und technischer Forschung angekündigt. NASK aus Polen arbeitet nun mit OpenAI zusammen, um Schutzmaßnahmen zu stärken und ein widerstandsfähigeres digitales Ökosystem zu unterstützen.

Dies ist keine Produkteinführung, sondern eine Zusammenarbeit zwischen einem KI-Unternehmen und der nationalen Cybersicherheitsbehörde Polens. Ihre unmittelbare Bedeutung liegt auf institutioneller Ebene: Die Forschung zu KI-Sicherheit und Cybersicherheit ist nun direkt mit einer Organisation verbunden, die sich auf die Sicherheit der digitalen Infrastruktur Polens konzentriert.

Für KI-Entwickler ist das relevante Signal, das zu beobachten gilt, ob die Partnerschaft konkrete Schutzmaßnahmen, Sicherheitsmethoden oder technische Forschungsergebnisse hervorbringt, die Teams beim Schutz realer Systeme anwenden können.

[09:06] Forschungsdigest: METTA ermöglicht Agenten, sich während einer Aufgabe anzupassen

METTA, eine speichergestützte Adaptationsmethode, hilft einem KI-Agenten, bereits während der Bearbeitung einer Aufgabe zu lernen, statt sich ausschließlich auf Erkenntnisse vor Aufgabenbeginn zu verlassen. Das ist wichtig für Systeme, die unbekannte Aufgaben mit begrenzter Erfahrung bewältigen müssen: Sie können ihr Verhalten aufgrund der jüngsten Interaktion aktualisieren und eine kompakte Zusammenfassung früherer Erfahrungen in den nächsten Versuch mitnehmen. Die Forscher testeten den Ansatz bei bislang unbekannten Meta-World-Aufgaben und PointMaze-Aufgaben mit langem Kontext, in denen Belohnungen selten vorkamen. In den zurückgehaltenen Meta-World-Umgebungen übertraf METTA eine Erfolgsquote von 50 %, während die Trainingskosten und die Wall-Clock-Zeit gering blieben. Bei den Labyrinthaufgaben übertraf es transformerbasierte Baselines und zeigte eine strukturiertere Exploration. Die praktische Folge ist, dass sich ein Agent mit geringem Trainingsbudget anpassen und dabei genügend Historie bewahren kann, um spätere Versuche zu lenken, statt jedes Mal sein Verständnis von Grund auf neu aufzubauen. Die nächste Frage ist, ob diese Balance zwischen Lernen während einer Aufgabe und Erinnern über Aufgaben hinweg auch außerhalb von Benchmark-Umgebungen Bestand hat.

[10:07] SpaceX Super Intelligence eröffnet ein Partnernetzwerk für Grok

SpaceX Super Intelligence hat ein offizielles Programm für Unternehmen eingeführt, die Produkte, Lösungen und Dienste mit Grok entwickeln, um gemeinsam Geschäftschancen und Kunden zu erschließen. Das SpaceX Super Intelligence Partner Network unterteilt diese Arbeit in Transformation Partners, die Kunden dabei unterstützen, die Grok-Plattform im gesamten Unternehmen einzuführen, und Marketplace Partners, die Plugins und Integrationen entwickeln, die Grok mit den von Kunden bereits genutzten Tools verbinden.

Mehr als 130 Unternehmen nahmen an der Frühzugriffsphase teil. Transformation Partners bauen über ein Forward Deployed Engineer-Akkreditierungsprogramm Deployment-Kapazitäten auf; die Ingenieure werden bei mehr als 30 Organisationen geschult. Marketplace Partners arbeiten an Produktintegrationen für die Grok-Suite.

Zu den Launch-Partnern gehören Bain & Company, Databricks, NVIDIA, Snowflake, Galatiq, Adapter Group, AHEAD und Alpha FMC. Ihre genannten Rollen reichen von Unternehmens Transformation und Umsetzung bis hin zu Datenplattformen, Governance, Audit-Protokollen und unternehmensspezifischem Kontext. Galatiq beschreibt beispielsweise ein Bereitstellungsmodell, bei dem Ingenieure Produktionssysteme innerhalb der Workflows von Kunden konzipieren und aufbauen. Adapter beschreibt, die gesamte Entwicklung eines Kunden in Grok Bot und Grok Build einzubringen, damit jeder Dialog mit einem breiteren Aufgabenkontext beginnt und nicht allein auf dem Arbeitsgedächtnis basiert.

Für Entwickler eröffnet sich praktisch die Möglichkeit, bei Deployment, Integrationen, Unternehmensdaten und operativen Kontrollen zusammenzuarbeiten. Der nächste Bewährungspunkt wird sein, wie breit diese Partnerschaften den Übergang von Pilotprojekten zur wiederkehrenden Nutzung in Produktionsumgebungen schaffen.

[11:27] Forschungsdigest: Eine Trainingstechnik macht wiederholte KI-Inferenz speichersparsamer

Eine neue Post-Training-Methode namens BeNice! hilft einer Klasse von KI-Modellen, Informationen wiederholt durch dieselben Schichten zu leiten, ohne dass die Anzahl der gelernten Parameter steigt. Bisher erzeugte jeder Durchgang während der Inferenz seinen eigenen Key-Value-Cache – gespeicherte Informationen früherer Tokens –, wodurch der Speicherbedarf linear mit der Anzahl der Wiederholungen wuchs. BeNice! trainiert das Modell so, dass der Cache des abschließenden Durchgangs in den ersten Durchgang übertragen werden kann und die wiederholten Durchgänge einen gemeinsamen Cache verwenden können. Die Forscher berichten, dass dies die Modellqualität erhält und dem Standard-Fine-Tuning mit separaten Caches entspricht. Das Ergebnis ist wichtig, weil geschleifte Architekturen die Qualität verbessern können, ohne einfach mehr Parameter hinzuzufügen; ihr Speicherbedarf bei der Inferenz hat diesen Vorteil jedoch begrenzt. BeNice! bietet eine Möglichkeit, den Qualitätsvorteil zu erhalten, ohne über die Tiefe hinweg doppelte Caches vorhalten zu müssen. Die Forscher fanden außerdem heraus, dass der Ansatz andere speichersparende Sequenzmethoden ergänzen kann. Somit könnten Teams ihn bei besonders wichtigem Speicherbedarf mit bestehenden Komprimierungstechniken kombinieren.

[12:27] DeusData bringt lokale Code-Intelligenz in KI-Agenten

DeusData hat codebase-memory-mcp veröffentlicht, ein lokales Projekt für Code-Intelligenz, das für Entwickler und KI-Agenten gedacht ist. Die neueste Version ist v0.12.1 vom 16. Oktober 2026, und das Repository wurde am 24. Oktober erneut aktualisiert. GitHub nennt 47.438 Sterne für das Projekt.

Das Repository verbindet Code, Dokumentation und Infrastruktur in einem persistenten Graphen. Es umfasst außerdem CBM Lens, MCP-Tools, Agent-Integrationen und änderungsbewusste Testauswahl. Zusammen sollen diese Bestandteile Entwicklern und KI-Agenten helfen, mit einer Codebasis als vernetztem Informationsgebilde zu arbeiten und nicht mit isolierten Dateien oder Prompts.

Für Entwickler ist die hilfreichste Chance eine lokale Kontextschicht, die Agent-Workflows über Code und Dokumentation hinweg unterstützen kann. Die Funktion zur Testauswahl könnte Teams außerdem dabei helfen, weniger Aufwand für Tests zu betreiben, die nicht mit einer Änderung zusammenhängen. Ein Aspekt, den es als Nächstes zu beobachten gilt, ist, wie effektiv die Agent-Integrationen und die änderungsbewusste Auswahl in echten Projekten funktionieren.

[13:21] Microsofts Agensh koordiniert 1.024 Agenten ohne zentrale Steuerung

Microsoft Research hat Agensh als Open Source veröffentlicht. Es handelt sich um eine Multi-Agent-Plattform, die auf ProgramBench bis zu 1.024 Agenten ohne zentralen Orchestrator oder einzelnen Controller ausführen kann, der die Aufgaben verteilt.

Der nützliche Mechanismus ist die gemeinsame Koordination. Die Arbeitsagenten organisieren sich selbst, während sie über ein gemeinsames Git-Repository, einen Chat-Kanal und ein Findings-Board kommunizieren. Im berichteten Experiment skalierte Agensh von einem auf 1.024 Agenten, während das Zeitbudget von sechs Stunden auf ProgramBench eingehalten wurde.

Damit erhalten Entwickler ein Open-Source-Framework, mit dem sie große, kooperative Agententeams erkunden und untersuchen können, wie diese gemeinsam Code, Konversationen und dokumentierte Ergebnisse koordinieren. Die prominente Zahl ist beeindruckend, aber der gemeinsame Arbeitsbereich und die Kommunikationskanäle sind die konkreten Bestandteile, die Teams übernehmen können.

Die nächste Frage ist, wie sich der Ansatz bei Aufgaben außerhalb von ProgramBench und unter Arbeitslasten verhält, die sich vom berichteten Benchmark unterscheiden.

[14:11] Cognition veröffentlicht ein Plugin zur Behebung von Sicherheitslücken als Open Source

Cognition hat das Devin Vulnerability Fixes Plugin als Open Source veröffentlicht, um Teams dabei zu unterstützen, auf die kritischen Sicherheitslücken mit Remote-Code-Ausführung in dieser Woche in PHP, Node.js und selbst verwalteten GitLab-Installationen zu reagieren.

Die Veröffentlichung umfasst drei Agent-Skills unter der MIT-Lizenz. Sie erfassen betroffene Systeme, patchen und testen sie und öffnen anschließend für jedes Repository einen Pull Request. Dadurch wird eine breite Reaktion auf Sicherheitslücken in getrennte, überprüfbare Änderungen umgewandelt, statt Teams jedes betroffene Repository manuell suchen und reparieren zu lassen.

Der entscheidende Aspekt, auf den zu achten ist, lautet, ob die generierten Pull Requests für eine reguläre technische Überprüfung bereit sind, nachdem das Plugin seine Erfassung, Patch- und Testarbeiten abgeschlossen hat.

[14:49] Letta-Tutorial baut zustandsbehaftete Engineering-Copilots

MarkTechPost hat eine praktische Anleitung veröffentlicht, wie sich mit Letta ein zustandsbehafteter Engineering-Copilot entwickeln lässt. Ziel ist es, einen KI-Assistenten über die Informationen in seinem unmittelbaren Prompt hinaus zu erweitern, damit er mit dauerhaftem Kontext und wiederverwendbarem Projektwissen arbeiten kann.

Im Mittelpunkt steht ein inspizierbarer Core Memory, der dem Copilot einen sichtbaren Ort bietet, an dem er Informationen speichern kann. Das Tutorial zeigt außerdem die Archivierung und Vektorabfrage: eine Möglichkeit, ältere Materialien anhand ihrer Bedeutung zu finden, statt eine exakte Übereinstimmung der Formulierungen zu benötigen.

Für komplexere Aufgaben kann der Copilot benutzerdefinierte Tools verwenden und seinen Zustand mit mehreren Agenten teilen, sodass spezialisierte Agenten auf Basis desselben Kontexts koordinieren können. Er unterstützt außerdem Streaming-Antworten und portable Workflows, die zwischen Umgebungen wechseln können.

Für Entwickler ist das hilfreiche Ergebnis eine konkrete Architektur für einen Engineering-Assistenten, der Projektkontext speichern, relevante Informationen abrufen, spezialisierte Aktionen anbinden und einen wiederverwendbaren Workflow beibehalten kann, statt in jeder Sitzung neu zu beginnen.