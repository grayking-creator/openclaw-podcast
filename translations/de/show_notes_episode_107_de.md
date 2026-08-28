Episode 107 — 27. August 2026

[00:00] Episode-Einstieg

Hermes Agent v2026.8.27 wurde am 27. August veröffentlicht und konsolidiert etwa 525 zusammengeführte Pull-Requests in einer einzigen Version für Docker-Images, gehostete Bereitstellungen und Neuinstallationen und ersetzt die v2026.8.19-Basislinie vom 19. August. Die für den Benutzer sichtbaren Ergänzungen umfassen einen neu gestalteten Agent-Aufgabenbereich, strukturierte Plan-Diffs, erweitertes Tool-Call-Streaming, einen Hintergrund-Scheduler, der lang laufende Aufgaben über Reconnects hinweg am Leben hält, und einen neuen Dateisystem-Sandbox-Modus, der Schreibzugriffe hinter projektspezifischen Allowlists einschränkt. Im Hintergrund enthält das Release Sicherheitsfixes für die Runtime, aktualisierte Standardwerte für den Model-Router, die Einstellung der Legacy-CLI-Flags und Breaking Changes am Plugin-Manifest, die nachgeschaltete Integratoren vor dem Upgrade patchen müssen. Docker-Images sind auf dieselbe Version gepinnt, gehostete Mandanten werden bis Ende der Woche in Wellen ausgerollt, und Betreiber von Self-Hosted-Installationen müssen das Installationsskript erneut ausführen, um das neue Plugin-Manifest-Schema zu übernehmen.

[02:00] Agent Stack Release-Auslesung: Hermes Agent v2026.8.27, v2026.8.19

Hermes Agent hat am 27. August v2026.8.27 veröffentlicht und etwa 525 zusammengeführte Pull-Requests in ein einzelnes stabiles Tag für Docker-Images, gehostete Bereitstellungen und Neuinstallationen zusammengefasst. Die auffälligste Änderung ist, dass der Desktop-Browser jetzt in seinem eigenen OS-Fenster geöffnet wird, gepaart mit einer verwalteten SSH-Remote-Update-Engine und einem Fleet-Profile-Rail. Browser-Sitzungen befinden sich nicht mehr im Chat-Panel — sie erhalten ein eigenes Fenster, das Sie unabhängig andocken oder schließen können — und Remote-Updates pausieren das Gateway über den Control-Socket, anstatt es mitten in der Aufgabe zu beenden.

Lokales Browsing erhielt einen zustimmungspflichtigen Pfad, der Ihr Standard-Chromium-Profil mit einem Windows-Close-with-Approval-Flow verwendet, sodass Websites, die Ihre angemeldete Browser-Sitzung erfordern, ohne erneute Authentifizierung funktionieren. Der Remote-MCP-Katalog wuchs auf über 50 live-verifizierte vendor-gehostete Server, einschließlich Cloudflare, Grafana Cloud, Better Stack und Railway. MCP ist das Model Context Protocol, der Standard, den KI-Agenten verwenden, um mit externen Tools und Daten zu kommunizieren, sodass eine einzige Hermes-Installation jetzt diese Dienste erreichen kann, ohne eine lokale Bridge.

Websuche und -extraktion erhielten TTL-Ergebnis-Caching, und tool_search führt jetzt Multi-Query-Lookups mit Stemming durch, sodass Wortvarianten wie „runs" und „running" demselben Tool zugeordnet werden. Für Mac-Benutzer entfernt die optionale OS-Keychain-Verschlüsselung für gespeicherte Secrets die macOS-Keychain-Eingabeaufforderungen bei jedem Start. Lean-Tail-Kompression ist jetzt standardmäßig aktiviert und reduziert die Antwort-Ausführlichkeit, ohne nützliche Inhalte zu verlieren.

Weitere veröffentlichte Änderungen: Image- und Paketmanager-Installationen lehnen jetzt unsichere direkte Updates ab, Slack-Link-Unfurl-Steuerungen wurden veröffentlicht, Docker-Container teilen Identitäten, einsteckbare Terminal-Environment-Backends sind hinzugekommen, und die Model-Picker haben GLM-5.3-Flash, MiniMax M3 free und MiniMax H3 Max Video hinzugefügt. Das vorherige Tag v2026.8.19 vom 21. August führte den schlüssellosen Web-Tier ein — kostenlose Fünf-Anbieter-Rotation mit Ring-Failover, sodass Neuinstallationen die Websuche ohne konfigurierte API-Schlüssel nutzen können — plus eine CLI-Politurwelle mit einem Fuzzy-Model-Picker und Ctrl+P-Befehlspalette. Kuratierte Notizen, die v0.20.0 und höher abdecken, werden mit v0.21.0 veröffentlicht.

[03:19] Codex-Desktop-App fügt WebMCP, Messages, Linux und Multi-Repo-Review hinzu

OpenAI's Codex-Desktop-App hatte zwischen Ende Juli und Ende August einen vollen Monat mit Updates, mit Änderungen, die den integrierten Browser, macOS, Linux und die Art und Weise betreffen, wie Multi-Repo-Projekte überprüft werden.

Am 30. Juli fügte die Desktop-Version 26.727 Adressleistenverlauf und Google-Suche im integrierten Browser hinzu, optionalen Browsing-Verlaufszugriff für ChatGPT, Chrome-Tab- und ausgewählten Text-Mentions, YouTube-Fragen und Rechtsklick „Ask ChatGPT". Multi-Folder-Projekte erhielten eine kombinierte Review-Ansicht für Diffs über Repositorys hinweg, und generierte Bilder erhielten Focused- und Canvas-Ansichten zum Kommentieren und Verfeinern. Derselbe Build fügte eine Activity-Ansicht hinzu und verbesserte die Windows-Installationszuverlässigkeit für lange Paketpfade.

Am 11. August veröffentlichte OpenAI eine Linux-Desktop-Vorschau, die Ubuntu, Debian und Fedora auf x64 und ARM64 über .deb- und .rpm-Pakete unterstützt. Die Desktop-App kann auch Anweisungen, Einstellungen, Skills, Plugins, Projekte und aktuelle Arbeit aus Claude Code, Claude Cowork und Cursor importieren, mit optionalem Auto-Update für importierte Arbeit.

Am 20. August fügte die macOS-App ein Apple Messages-Plugin hinzu, das in allen Plänen verfügbar ist, nutzbar von ChatGPT Work oder Codex, mit erforderlicher Genehmigung vor dem Senden. Dasselbe Update führte schreibgeschützte gemeinsame Snapshots lokaler Codex-Threads in jedem Codex-Plan ein, Same-Workspace Site-Co-Editing und URL-Änderungen, einheitliche angeheftete Threads über Desktop und iOS hinweg und breitere Computer History-Verfügbarkeit in Europa. OpenAI warnt, dass der Secret-Pattern-Redactor bei gemeinsamen Snapshots möglicherweise nicht jedes sensible Detail entfernt.

Am 25. August wurde die Browser-Erweiterung von Chrome auf Edge, Brave, Opera und Vivaldi ausgeweitet, mit Tab-Mentions und Browser-Steuerung auf allen fünf, obwohl Opera keinen Side-Chat hat. Der integrierte Desktop-Browser erhielt auch Website-bereitgestellte Site-Tools über WebMCP für ChatGPT Work und Codex. Dieses Feature erfordert die neueste Desktop-App plus ein GPT-5.6 Sol- oder Terra-Abonnement und ist auf Luna, Enterprise oder Edu nicht verfügbar.

[05:11] Grok Bot gibt Agenten einen persistenten Cloud-Computer und Rund-um-die-Uhr-Arbeit

Grok Bot ist xAI's separates Agentenprodukt, kein Modus innerhalb von Grok Chat. Es wurde am 11. August in einer frühen Beta gestartet und der Zugang wurde am 26. August erneut erweitert. Benutzer erstellen mehrere Bots, schreiben ihnen wie Kollegen, setzen sie in gemeinsame Threads ein und lassen einen Bot die Arbeit an einen anderen übergeben.

Die Kern-Architekturentscheidung ist, dass jeder Bot, den ein Benutzer erstellt, einen persistenten Cloud-Computer teilt, einschließlich Dateien, Browser-Zustand und Anmeldungen. Die Isolation ist pro Benutzer und nicht pro Bot. Das ermöglicht es einem Vertriebs-Bot, Konten in einem angemeldeten Browser zu recherchieren, das Ergebnis an einen Betriebs-Bot zu übergeben, der Rechnungen aus Gmail verarbeitet, und fortzufahren, während der Laptop geschlossen ist. Bots können sich auf Websites anmelden, die keine APIs oder MCP-Server haben, und xAI sagt, sie können beobachten, wie ein Benutzer einen Workflow einmal abschließt, ihn als Routine speichern, Korrekturen akzeptieren und Follow-ups auf abgebrochene Threads durchführen.

Download-Clients decken macOS auf Apple Silicon und Intel ab, Windows 10 und 11 auf x64 und iPhone und iPad. Die Produktseite listet keinen Android-Grok-Bot-Client auf.

Der Zugang ist in den Abonnements SuperGrok, SuperGrok Plus und SuperGrok Heavy enthalten, mit dem niedrigsten einzelnen Tier bei 30 $ pro Monat. Dasselbe Produkt ist auch in Cursor Pro, Pro+ und Ultra-Plänen ab 20 $ pro Monat gebündelt, sowie in Cursor Teams Standard und Premium. Die Grok Bot-Nutzung wird separat von der Standard-Grok- oder Cursor-Nutzung abgerechnet. Enterprise-Zugang bleibt auf der Warteliste.

Von xAI aufgeführte Sicherheits- und Kontrollfunktionen umfassen Verschlüsselung bei der Übertragung und im Ruhezustand, ein Training-Opt-out, Auto Review für sensible Aktionen und Enterprise-Kontrollen für DLP, Zertifikate, Proxies und Netzwerk-Kontrollen.

[06:52] Alibaba zeigt Qwen4-Vorschau durch Qwen3.8-Flash-Next

Alibabas Qwen-Team hat Qwen3.8-Flash-Next veröffentlicht, ein Multimodales Mixture-of-Experts-Modell mit 125 Milliarden Parametern, das einen Ausblick auf die kommende Qwen4-Architektur bietet. Die Gesamtzahl beträgt 180 Milliarden Parameter, aufgeteilt in drei Teile: ein 125B-Backbone, eine 51B N-Gramm-Einbettungstabelle und ein 4B Multi-Token-Vorhersagemodul. Pro Token werden nur 6 Milliarden Parameter aktiviert, und genau hier liegt die Effizienzgeschichte.

Vier architektonische Verschiebungen definieren die Vorschau. Eine hybride Schicht kombiniert Gated DeltaNet mit Qwen Sparse Attention für die Sequenzmodellierung. Gated Residual-Verbindungen gestalten den Gradientenfluss durch das Netzwerk neu. Die N-Gramm-Einbettungstabelle gibt dem Modell explizite Kurzstrecken-Musterspeicher, und der Muon-Optimizer ersetzt den Standard-Trainingsschritt. Zusammen reduzieren diese Änderungen den aktiven Rechenaufwand, ohne die Gesamtreichweite des Modells zu verkleinern.

Das Team berichtet von Trainingskosten von etwa einem Neuntel von Qwen3.7-Plus, ein steiler Rückgang, der durch den neuen Optimierer und die hybride Attention erklärt werden kann. Für Selbst-Hoster liegt der FP8-Checkpoint bei 172,78 GiB, was echte Einschränkungen für Consumer-Hardware bedeutet und ernsthafte Deployments in Richtung Rechenzentrum-GPUs treibt.

Was dies für Entwickler bedeutet: Die Vorschau gibt multimodalen Teams einen frühen Einblick in Qwen4s Richtung, insbesondere den hybriden Attention-Ansatz und die N-Gramm-Einbettungstabelle. Der 172,78 GiB FP8-Fußabdruck setzt eine klare Planungsgrenze für Speicher und Arbeitsspeicher. Bis Qwen4 vollständig herauskommt, behandeln Sie die Benchmark-Leistung als richtungsweisend und nicht als endgültig.

[08:13] Orchestrierung überholt Automatisierung als CX-Engpass, sagt Tata Communications

Tata Communications macht geltend, dass die Arbeit an Kundenerlebnissen die vorhandene Infrastruktur überholt hat. Gaurav Anand, der die Customer Interaction Suite weltweit bei Tata Communications leitet, sagt, dass Unternehmen in den letzten Jahren konversationelle KI auf Legacy-Systeme aufgesetzt haben, die nie für agentenbasierte Arbeitslasten entwickelt wurden, und die Nähte beginnen sich zu zeigen.

Das Ergebnis, so Anand in einer VentureBeat-Kolumne vom 27. August 2026, ist, dass menschliche Agenten nun den Großteil der Integrationslast tragen. Sie müssen Kontext aus unzusammenhängenden Tools zusammenfügen, nur um herauszufinden, was ein KI-System einem Kunden bereits mitgeteilt hat. Der Engpass ist nicht mehr der Zugang zu Daten, sondern das Fehlen eines gemeinsamen Unternehmenskontextes, der Kundenidentitäten, Interaktionen, Transaktionen, Richtlinien, Journeys und operative Systeme in einem gemeinsamen Verständnis zusammenführt.

Die traditionelle CX-Architektur wurde für lineare, menschengesteuerte Weiterleitung konzipiert, nicht für die Orchestrierung von Echtzeit-Datenflüssen zwischen autonomen KI-Agenten, Datenlagern und menschlichen Mitarbeitern. Anand rahmt den Wandel als Übergang von Automatisierung zu Orchestrierung als oberste CX-Priorität. Die strategische Frage, schlägt er vor, ist, wie man die Intelligenz koordiniert, die bereits im Unternehmen vorhanden ist, sodass der Kunde die internen Silos nie spürt.

Dieser Rahmen setzt Orchestrierungs-Tools, Identitätsauflösung und Kontextschichten ins Zentrum des nächsten CX-Build-Zyklus, vor einem weiteren Upgrade des Konversationsmodells.

[09:37] Das wahre unternehmerische KI-Risiko, das sich zwischen Agenten versteckt

Das Stück macht eine klare Behauptung: Der gefährliche Teil der unternehmerischen KI ist nicht ein einzelner Agent, der durchdreht, sondern das unsichtbare Netz von Aufrufen zwischen Agenten, das niemand abbildet oder besitzt.

Echte Deployments versenden nicht einen Agenten und schauen zu, wie er läuft. Sie versenden Flotten, wo jeder Agent APIs aufruft, andere Agenten aufruft und in Anwendungen zugreift, die lange bevor ein maschineller Entscheidungsträger existierte, erstellt wurden. Ein Support-Ticket, das früher ein System berührte, könnte jetzt vier Agenten durchlaufen, bevor ein Mensch es sieht, und jeder Übergabepunkt ist eine Genehmigung, die niemand verfasst hat.

Die Mathematik ist das, was dies schmerzhaft macht. Einen zehnten Agenten hinzuzufügen bedeutet nicht zehn Verbindungen hinzuzufügen, es können Dutzende sein, weil jeder Agent jeden anderen Agenten aufrufen könnte, und jeder Aufruf einen weiteren Aufruf irgendwoanders auslösen kann. Die Komplexität vervielfacht sich mit der Anzahl der Pfade zwischen Agenten, nicht mit der Anzahl der Agenten selbst, und niemandes Job ist es, diesen Graphen zu zeichnen.

Governance hat nicht Schritt gehalten. Fragen Sie ein Sicherheitsteam, welche Agenten welche Systeme erreichen können, und Sie bekommen Stille. Fragen Sie, welcher Agent welche nachgelagerte Aktion vor drei Schritten ausgelöst hat, und Sie bekommen mehr Stille. Der Instinkt ist, dies wie eine Checkliste zu behandeln: Genehmigen Sie den Agenten, protokollieren Sie den Agenten, weiter geht's. Aber eine Checkliste überprüft einen Moment in der Zeit, während Komplexität über eine Kette läuft. Ein Stapel von Einmal-Genehmigungen kann einen Workflow nicht regieren, so wenig wie ein einzelnes Gemüse eine Ernährung ausmacht.

Die praktische Erkenntnis für Entwickler: Bevor Sie Agenten-Flotten skalieren, zeichnen Sie den Graphen, welcher Agent welches System erreichen kann. Wenn niemand im Team dieses Bild in unter fünf Minuten skizzieren kann, ist das Deployment bereits zu undurchsichtig, um es zu regieren.

[11:20] Liquid AIs Pipette Benchmarks Modelle auf den Geräten, auf denen sie tatsächlich laufen

Jede Modellkarte im Internet listet Qualitätszahlen, gemessen auf Server-Klasse-Hardware mit voller Präzision. Diese Zahlen sagen selten voraus, wie sich dasselbe Modell verhält, sobald es verkleinert und auf einem Telefon oder Laptop ausgeführt wird. Diese Woche veröffentlichte Liquid AI Pipette, eine Open-Source, reproduzierbare Benchmarking-Suite, die entwickelt wurde, um diese Lücke zu schließen.

Pipette misst vier Variablen gleichzeitig: das Modell, seine Quantisierung, die Runtime und die Geräte-Hardware. Indem diese als ein einzelnes Experiment statt als separate Fragen behandelt werden, produziert es Zahlen, die mehr dem ähneln, was ein Entwickler tatsächlich sieht, wenn er ein Modell auf echte Hardware seitlädt. Liquid AI hat sich mit Artificial Analysis zusammengetan, um als unabhängiger Methodenvalidator zu dienen, was die Suite ehrlich halten soll über das, was sie misst und was nicht.

Für Entwickler, die On-Device-Features ausliefern, ist die praktische Verschiebung, dass Modell- und Quantisierungsentscheidungen jetzt durch gemessene Latenz und Qualität auf einem bestimmten Telefon gestützt werden können, nicht aus einem Paper extrapoliert. Die Suite ist Open-Source, also können Teams ihre eigenen Geräteprofile hinzufügen und die Matrix auf Hardware, die sie tatsächlich ausliefern, erneut ausführen.

Die ehrliche Einschränkung ist, dass Pipette das misst, was es misst; es beseitigt nicht die zugrundeliegenden Hardware-Grenzen, die On-Device-KI einschränken. Aber es gibt jetzt einen öffentlichen, reproduzierbaren Weg, Kandidaten auf dem gleichen Spielfeld zu vergleichen, und das ist das, was den meisten On-Device-Projekten gefehlt hat.

[12:47] OpenAIs Jalapeño-Chip veröffentlicht erste Inferenzergebnisse

OpenAI hat die ersten Leistungszahlen für Jalapeño veröffentlicht, seinen maßgefertigten Chip, der für die Ausführung von KI-Modellen in der Produktion konzipiert wurde. Inferenz, die Arbeit des tatsächlichen Generierens einer Antwort, wenn ein Benutzer auf Senden klickt, ist der teuerste Teil des Betriebs eines modernen KI-Produkts, und Chips, die speziell dafür entwickelt wurden, können schneller und günstiger sein als Allzweck-Grafikprozessoren. Das ist die Wette hinter Jalapeño.

In den am 25. August veröffentlichten Ergebnissen gibt OpenAI an, dass der Chip branchenführende Geschwindigkeit und Energieeffizienz liefert, mit höherem Durchsatz (mehr Antworten pro Sekunde) und niedrigerer Latenz (weniger Wartezeit pro Antwort) als vergleichbare Optionen. Das Unternehmen hat die Ankündigung als erste konkrete Validierung einer mehrjährigen Anstrengung gerahmt, eigene Siliziumlösungen zu entwickeln, anstatt sich vollständig auf Drittanbieter-Beschleuniger zu verlassen.

Die Zahlen sind wichtig, weil nicht das Training, sondern die Inferenz die wiederkehrende Rechnung ist. Ein zweckgebauter Chip, der dieselbe Last mit weniger Strom bewältigt oder mehr Antworten aus jedem Server herausholt, senkt direkt die Kosten für den Betrieb eines Chatbots, eines Coding-Assistenten oder eines gebündelten Zusammenfassungsauftrags in großem Maßstab. Für OpenAI übersetzt sich das in Margen, und für jeden, der auf seine APIs aufbaut, könnte es sich letztendlich in Preisänderungen oder neuen Latenzstufen niederschlagen.

Zwei Dinge sind als nächstes zu beobachten: unabhängige Benchmarks, die die vom Anbieter gelieferten Zahlen bestätigen oder widersprechen, und jedes Signal darüber, ob Jalapeño auf interne OpenAI-Workloads beschränkt ist oder letztendlich externen Datenverkehr über ChatGPT oder die API bedienen wird.

[14:14] Googles winziges Glukosemodell schlägt Konkurrenten, die hunderte Male größer sind

Google Research und die University of New South Wales Sydney haben diese Woche GlucoFM veröffentlicht, ein Foundation-Modell für Daten von kontinuierlichen Glukosemonitoren. Kontinuierliche Glukosemonitoren sind die kleinen Sensoren, die Menschen mit Diabetes tragen, um ihren Blutzucker rund um die Uhr zu verfolgen, und erzeugen alle paar Minuten eine neue Messung.

GlucoFM hat nur 720.000 Parameter, ein Bruchteil der Größe der meisten modernen KI-Systeme, und erreichte dennoch über 14 Kohorten- und Aufgabenauswertungen hinweg durchschnittlich 58,8 bei der Precision-Recall-AUC, und übertraf damit GluFormer, ein 135-Millionen-Parameter-Modell, das für dieselbe Aufgabe entwickelt wurde, sowie MOMENT, ein 385-Millionen-Parameter generales Zeitreihen-Foundation-Modell. Zum Vergleich: GluFormer ist etwa 190-mal größer und MOMENT etwa 535-mal größer als GlucoFM.

Der Trick liegt darin, wie GlucoFM das Signal liest. Anstatt eine Glukosekurve als eine lange undifferenzierte Sequenz zu behandeln, teilt es die Daten in zwei Ströme auf: einen langsamen physiologischen Strom, der Basisliniendrift und längere Trends erfasst, und einen transitorischen Ereignisstrom, der kurzlebige Spitzen durch Mahlzeiten, Bewegung oder Medikamente erfasst. Jeder Strom erhält seinen eigenen Encoding-Pfad, bevor das Modell sie wieder zusammenführt. Das Modell wird in selbstüberwachter Weise vortrainiert, was bedeutet, dass es die Form von Glukosekurven aus unbeschrifteten Daten lernt, bevor ein Feintuning für eine bestimmte Vorhersage erfolgt.

Dies ist wichtig, weil CGM-Daten rauschbehaftet, personspezifisch und voller überlappender Dynamiken sind. Ein allgemeines Zeitreihen-Modell muss diese Trennung von Grund auf mit einem viel größeren Parameterbudget lernen. GlucoFM baut die Trennung in die Architektur ein, und das ist der Grund, warum ein Modell von der Größe eines kleinen Bildklassifikators bei einem klinisch orientierten Benchmark gewinnen kann.

Die Einschränkungen sind real. GlucoFM ist ein Forschungssprototyp ohne FDA- oder gleichwertige behördliche Zulassung, sodass nichts morgen in einer Klinik ankommt. Google hat keine öffentliche API, offene Gewichte oder eine Partnerschaft mit Geräteherstellern angekündigt. Was GlucoFM signalisiert, ist, dass der "größer ist besser"-Standard in der medizinischen KI einen glaubwürdigen Herausforderer hat, wenn die Architektur um die Biologie herum entworfen wird, anstatt von der Sprachverarbeitung übernommen zu werden.

[16:16] Forschung kompakt: Ein intelligenterer Loop zum Unterrichten von Visionsmodellen, Anweisungen zu befolgen

Ein Visionsmodell zur Befolgung komplexer Anweisungen zu trainieren bedeutet normalerweise, große Datensätze zu sammeln und zu hoffen, dass sie genau, vielfältig und schwierig genug sind. Das neue VISA-Framework behandelt diesen Datenerstellungsschritt als einen Loop, den das System selbst verbessert. In jeder Runde inspiziert es ein Bild, verwirft Einschränkungen, die nicht verifiziert werden können, und schlägt neue vor, die aus einem Memory-Bank gezogen werden. Kandidatenanweisungen werden mit ausführbaren Tools und strukturierten Sprachmodell-Richtern überprüft, und etwaige Fehler werden diagnostiziert und zurückgespeist, sodass die nächste Runde genau die Schwächen anvisiert, die das Zielmodell noch zeigt.

Dieses Feedback leistet Doppelarbeit: Es schärft zukünftige Daten und dient gleichzeitig als Belohnungssignal für Reinforcement Learning, sodass kein separates Belohnungsmodell trainiert werden muss. Beim MM-IFEval-Benchmark übertrafen mit VISA trainierte Modelle starke Baselines bei der Anweisungsbefolgung, während sie bei sieben allgemeinen multimodalen Tests stabil blieben. Die praktische Konsequenz ist günstigere, höherwertige Tuning-Daten für jeden, der Visionsassistenten entwickelt, die mehrere Regeln gleichzeitig berücksichtigen müssen, wie das Lesen eines Diagramms und das Beantworten in einem bestimmten Format mit einer Wortbegrenzung.

[17:22] xAIs Grok 4.6 landet auf Microsoft Foundry

xAIs Flaggschiff Grok 4.6 ist jetzt auf Microsoft Foundry verfügbar, Azures Modellkatalog für Enterprise-KI-Bereitstellungen. Die am 26. August angekündigte Integration reiht Grok 4.6 neben anderen Frontier-Modellen für direkten Vergleich und Bereitstellung durch Azures Enterprise-Infrastruktur ein.

Grok 4.6 wird mit einem 500.000-Token-Kontextfenster und vier konfigurierbaren Reasoning-Aufwandsstufen ausgeliefert: niedrig, mittel, hoch und xhoch. xAI beschreibt das Modell als für langlaufende Agents und ehrgeizige interaktive und visuelle Arbeit gebaut, eine Sprache, die signalisiert, dass das Unternehmen auf ernsthafte Agent-Workloads aus ist, anstatt auf Single-Turn-Chat.

Für Entwickler bietet Foundry einen einzigen Ort, um Grok 4.6 mit konkurrierenden Frontier-Modellen zu evaluieren, workloadspezifische Tests durchzuführen und verwaltete Endpunkte unter Enterprise-Sicherheits- und Governance-Kontrollen bereitzustellen. xAI erwähnt spezifisch Coding-Agents, Engineering-Copiloten, Forschungsassistenten und Enterprise-Automatisierung als die Arten von Systemen, auf die das Modell abzielt, wobei Entwickler jetzt im Foundry-Modellkatalog beginnen können.

[18:17] Forschung kompakt: Ein günstigerer Weg, KI-Modellen länger nachdenken zu lassen

Eine neue Technik namens Prefix Sliding könnte KI-Modelle deutlich günstiger machen, wenn sie lange Zeit über schwierige Probleme nachdenken. Heutzutage behält ein Modell, wenn es ausführlich nachdenkt, jeden Zwischengedanken im Arbeitsspeicher, sodass jede Frage teurer wird, je länger es nachdenkt. Die Forscher fanden heraus, dass die meisten dieser Zwischenschritte nicht mehr relevant sind, sobald das Modell weitergemacht hat, daher zahlt man für Kontext, der selten hilft.

Ihr Fix ist dem Geist nach einfach: Nur die ursprünglichen Anweisungen vorne behalten und ein gleitendes Fenster der letzten paar tausend Textteile, den Rest unterwegs verwerfen. Das begrenzt die Speichernutzung unabhängig davon, wie lang die Denkkette wird. Ohne jegliches Neuentraining machte das Anwenden von Prefix Sliding auf bestehende Modelle sie etwa 3x schneller bei gleichzeitig erhaltener Genauigkeit, und das Training mit derselben Richtlinie hob die Decke auf über 100.000 Denkschritte.

Für Entwickler, die Agenten ausliefern, die lange Planungsschleifen benötigen, ist diese Art von Speicherbegrenzung wichtig, weil die Inferenzkosten das sind, was ehrgeizige Denkagenten davon abhält, im großen Maßstab wirtschaftlich zu sein.

[19:26] Open WebUI fügt Human-in-the-Loop-Tool-Genehmigung hinzu

Open WebUI, das selbsthostbare Chat-Frontend, auf dem viele lokale-KI-Stacks aufbauen, hat am 25. August v0.11.1 veröffentlicht. Die einzige dokumentierte Änderung ist ein Human-in-the-Loop-Tool-Genehmigungsablauf.

So funktioniert es: Ein Administrator aktiviert die Funktion in den Einstellungen. Von da an kann jedes Gespräch vom Standardmodus – in dem Tool-Aufrufe ausgeführt werden, sobald das Modell sie anfordert – in einen Modus gewechselt werden, in dem jeder Aufruf pausiert und zuerst den Benutzer fragt. Die Genehmigung oder Ablehnung erfolgt per Button oder Tastenkürzel, ein Aufruf nach dem anderen, und die Wahl wird für den Rest des Gesprächs und für zukünftige Gespräche gespeichert.

Die Versionshinweise enden mitten im Feature, daher konzentriert sich diese Geschichte eng auf die eine dokumentierte Änderung: das Genehmigungsgate pro Aufruf, seine adminseitige Aktivierung und ihren Umschalter pro Gespräch.

Für Self-Hoster ist dies ein echter Sicherheitshebel für jeden Agenten-Workflow. Der praktische Schritt ist, den Admin-Schalter für rein konversationelle Chats ausgeschaltet zu lassen und die Genehmigung pro Gespräch überall einzuschalten, wo das Modell Tools angehängt hat, sodass jeder Aufruf für eine explizite Erlaubnis oder Ablehnung pausiert, anstatt unkontrolliert ausgeführt zu werden. Beobachten Sie, ob zukünftige Versionen die gespeicherte Wahl über ein einzelnes Gespräch hinaus auf arbeitsbereichsweite Standardeinstellungen ausweiten, da die Persistenz im Moment lokal für den Chat ist, in dem der Schalter umgelegt wurde.

[20:46] Google teilt seine achte TPU-Generation auf der Hot Chips auf

Auf der Hot Chips 2026, der jährlichen Konferenz, auf der Chip-Teams ihr neuestes Silizium für ein technisches Publikum vorstellen, diskutierte Google seine Tensor-Processing-Unit-Familie der achten Generation. Laut einem ServeTheHome-Bericht vom 26. August ist die neue Familie nach Workload in zwei Chips aufgeteilt: den TPU 8t für Training und den TPU 8i für Inferenz.

Diese Aufteilung ist die strukturelle Geschichte der Ankündigung. Ein Chip ist für das Unterrichten von Modellen gebaut und der andere für das Bereitstellen von Vorhersagen, und Google präsentiert sie Seite an Seite als passendes Paar. Das Unternehmen sticht auch als einer der wenigen Hyperscaler hervor, die ihre eigene Trainingshardware entwickeln, anstatt Trainingssilizium von externen Anbietern zu beziehen – eine ungewöhnliche Position in der Branche, wo die meisten großen KI-Betreiber ihre Trainingsrechenleistung von Drittanbietern für Chipfertigung kaufen.

Für Entwickler ist die praktische Frage der Zugang. Googles TPUs erreichen typischerweise externe Entwickler über Google Cloud und einen kleinen Kreis von Partnern, und die technischen Tiefenanalysen, die rund um die Hot Chips veröffentlicht werden, geben normalerweise einen Vorgeschmack darauf, was wenige Monate später allgemein verfügbar wird. Die konkreten Signale, auf die Sie achten sollten, sind Google-Cloud-Blogbeiträge und Benchmarkzahlen in Bezug auf die neuen Chips, die zeigen werden, ob die achte Generation die Kosten, den Durchsatz oder die Skalierbarkeit des Trainings oder des Betriebs von Modellen auf Googles Stack verändert.