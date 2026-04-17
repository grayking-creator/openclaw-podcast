OPENCLAW DAILY — EPISODE 033 — April 17, 2026

[00:00] INTRO / HOOK
OpenClaw veröffentlicht ein Update, das seinen Standard-Anthropic-Pfad auf Claude Opus 4.7 umstellt und Gemini-Sprachausgabe hinzufügt. Anthropic bringt Opus 4.7 in die allgemeine Verfügbarkeit mit verbesserten Fähigkeiten für Programmierung und Bildverarbeitung. Salesforce sagt, der Enterprise-Stack der Zukunft ist headless und agentennativ. Roblox verwandelt Spieleentwicklung in eine Planungsschleife. Physical Intelligence sagt, Roboter beginnen zu improvisieren. Und Adobes Zahlen deuten darauf hin, dass KI-Einkaufstraffic endlich zu einem echten Geschäftskanal wird, nicht nur zu einer Spielerei.

[02:00] STORY 1 — OpenClaw v2026.4.15: Bessere Standards, bessere Sprachausgabe, bessere Signale
OpenClaw 2026.4.15 ist wichtig, weil es das Produkt genau an den Stellen verbessert, die ein täglicher Operator tatsächlich spürt.

Die größte sichtbare Änderung ist, dass gebündelte Anthropic-Standards, Aliase und Claude CLI-Standards jetzt auf Claude Opus 4.7 verweisen. Das bedeutet, dass die Plattform schnell mit dem neuesten allgemein verfügbaren Flaggschiff von Anthropic voranschreitet, anstatt die Modellauswahl als nachlaufende Konfigurationsaufgabe zu behandeln. Bei der Sprachausgabe unterstützt das gebündelte Google-Plugin jetzt Gemini-Sprachausgabe, einschließlich Anbieterregistrierung, Stimmenauswahl, WAV-Antwortausgabe und PCM-Telefonieausgabe.

Die Control UI wird ebenfalls operativ nützlicher. Es gibt jetzt eine Model Auth-Statuskarte, die auf einen Blick den OAuth-Token-Status und den Rate-Limit-Druck des Anbieters anzeigt – genau das, was einem Operator hilft zu verstehen, ob ein Fehler an Anmeldedaten, Kontingent oder dem Modell selbst liegt.

Und die Fehlerbehebungsliste ist kein Füllmaterial. Das Release verbessert den vertrauenswürdigen lokalen `MEDIA:`-Passthrough, sodass clientdefinierte Tools keine integrierten Funktionen imitieren können, verbessert die Replay-Wiederherstellung, verstärkt Webchat- und Matrix-Schnittstellen, optimiert Prompt-Budgets für schwächere lokale Modelle und behebt mehrere langschwänzige Runtime-Probleme bei Transkripten, Tool-Schleifen, gebündelten Plugins und Sprachausgabe. So sieht eine ernsthafte Agent-Runtime aus, wenn sie reift: mehr Fähigkeiten, aber auch engere Vertrauensgrenzen.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.15

[07:00] STORY 2 — Claude Opus 4.7: Stärkere Programmierung, bessere Bildverarbeitung und ein Cyber-Schutzzaun-Test
Anthropic sagt, dass Claude Opus 4.7 eine bemerkenswerte Verbesserung gegenüber Opus 4.6 bei fortgeschrittener Softwareentwicklung darstellt, besonders bei schwierigen, langlebigen Aufgaben. Die eigene Formulierung des Unternehmens ist aufschlussreich: Dies ist die Version, die Entwickler schwierigere Aufgaben mit weniger Aufsicht übergeben können, weil sie sorgfältiger plant, Anweisungen genauer befolgt und sich selbst überprüft, bevor sie Ergebnisse meldet.

Anthropic sagt auch, dass Opus 4.7 eine wesentlich bessere Bildverarbeitung hat, mit Unterstützung für hochauflösende Bildverständnis und besserer Ausgabequalität bei professionellen Aufgaben wie Interfaces, Präsentationen und Dokumenten. Der Launch geht also nicht nur um Code. Es geht darum, die Messlatte für multimodale Arbeit zu erhöhen, die poliert aussehen muss, nicht nur korrekt.

Aber der strategisch interessanteste Teil könnte die Sicherheitshaltung sein. Anthropic führt Opus 4.7 mit automatischen Schutzmaßnahmen ein, die darauf abzielen, verbotene oder hochriskante Cybersicherheitsanfragen zu blockieren, während legitime Sicherheitsforscher zu einem Verifizierungsprogramm eingeladen werden. Das macht diesen Launch zu einem Live-Experiment, ob ein Frontier-Lab ein leistungsfähigeres Modell breit herausbringen kann, während es gleichzeitig die gefährlichsten Anwendungsfälle abgrenzt.
→ https://www.anthropic.com/news/claude-opus-4-7

[12:30] STORY 3 — Salesforce Headless 360: Den Enterprise-Stack für Agenten neu aufbauen
Salesforce spricht das Unausgesprochene aus: Wenn Ihre Plattform immer noch annimmt, dass Fortschritt durch einen Menschen entsteht, der durch einen Browser klickt, ist sie nicht bereit für das agentenbasierte Unternehmen.

Ihre Antwort ist Headless 360, eine zerlegte Version des Salesforce-Stacks, die Kernplattformfunktionen als APIs, MCP-Tools und CLI-Befehle bereitstellt. Das Unternehmen sagt, dies umfasst mehr als 60 MCP-Tools und mehr als 30 vorkonfigurierte Coding-Skills, plus eine Experience-Schicht, die reichhaltige Interaktionen über Oberflächen wie Slack, Sprache, WhatsApp und benutzerdefinierte React-Frontends rendern kann.

Der tiefere Punkt ist nicht nur die Tool-Anzahl. Salesforce versucht, die gesamte Schleife zu besitzen: mit Coding-Agenten bauen, Verhalten evaluieren und beobachten, dann dieselbe Geschäftslogik über jede Oberfläche bereitstellen, die der Mensch oder der Agent gerade nutzt. Mit anderen Worten: Der Browser ist nicht mehr der Schwerpunkt. Die Plattform ist es.
→ https://www.salesforce.com/news/stories/salesforce-headless-360-announcement/

[18:00] STORY 4 — Der Roblox Assistant ist kein Spielzeug-Prompt-Feld mehr
Roblox verbessert seinen Assistant, damit er Erstellern helfen kann, Spiele als mehrstufiger Mitarbeiter zu planen, zu bauen und zu testen, anstatt nur eine einzelne Antwort aus einem einzelnen Prompt auszuspucken.

Die wichtigste Neuerung ist der Planning Mode. Anstatt blind eine Idee auszuführen, kann der Assistant den Code und das Datenmodell des Spiels prüfen, klärende Fragen zu Stil und Asset-Wahl stellen und die Anfrage in einen bearbeitbaren Aktionsplan umwandeln, bevor die Implementierung beginnt. Das ist wichtig, weil die Einmal-Generierung oft genau dort scheitert, wo die Absicht des Erstellers noch unklar ist.

Roblox fügt auch Mesh-Generierung hinzu und führt Prozedurale Modelle ein, während die Testschleife Logs lesen, Screenshots erstellen, Eingaben simulieren, Bugs erkennen und diese Erkenntnisse zurück in den Assistant speisen kann, damit er Probleme automatisch beheben kann. Dies ist ein starkes Beispiel dafür, wohin agentenbasiertes Produktdesign geht: nicht nur das Artefakt generieren, sondern am gesamten Workflow darum herum teilnehmen.
→ https://techcrunch.com/2026/04/16/robloxs-ai-assistant-gets-new-agentic-tools-to-plan-build-and-test-games/

[23:00] STORY 5 — Physical Intelligences π0.7 und der Fall für ein allgemeines Roboter-Gehirn
Physical Intelligence hat Forschung zu einem neuen Modell namens π0.7 veröffentlicht, das Roboter anweisen kann, Aufgaben auszuführen, für die sie nie explizit trainiert wurden, indem es Teile des vorherigen Wissens auf neue Weise kombiniert.

Das Heißluftfritteusen-Beispiel ist der Haken. Laut Unternehmen enthielten die Trainingsdaten nur zwei dünn relevante Episoden mit einer Heißluftfritteuse, und das Modell schaffte dennoch einen plausiblen Versuch und führte die Aufgabe dann erfolgreich durch, sobald ein Mensch es durch die Schritte in natürlicher Sprache coachte. Wenn sich das bestätigt, deutet es darauf hin, dass die Skalierungsgeschichte für Robotik beginnen könnte, der bereits bekannten in Sprache und Bildverarbeitung zu ähneln: Sobald Systeme die Remix-Schwelle überschreiten, kann jeder neue Datenblock mehr als eine neue Aufgabe freischalten.

Die Forscher sind vorsichtig, es nicht zu übertreiben. π0.7 hat immer noch Schwierigkeiten mit komplexer mehrstufiger Autonomie, und die Prompt-Qualität ist immer noch sehr wichtig. Aber wenn die zentrale Behauptung stimmt, ist dies eines der klareren Zeichen, dass Robotik sich möglicherweise von routinemäßigem Training zu echt übertragbarer Kompetenz bewegt.
→ https://techcrunch.com/2026/04/16/physical-intelligence-a-hot-robotics-startup-says-its-new-robot-brain-can-figure-out-tasks-it-was-never-taught/

[28:00] STORY 6 — Adobes KI-Traffic-Daten: Der Commerce-Kanal sieht nicht mehr experimentell aus
Adobes neueste Retail-Daten deuten darauf hin, dass KI-Einkaufstraffic nicht mehr nur ein seltsamer Top-of-Funnel-Trend ist. Er beginnt, wie ein echter Commerce-Kanal auszusehen.

Laut Adobe stieg der KI-Traffic zu US-Retail-Webseiten im ersten Quartal gegenüber dem Vorjahr um 393%. Wichtiger ist, dass die Qualität dieses Traffics gegenüber dem Muster des letzten Jahres gekippt ist. Im März 2026 konvertierte KI-Traffic 42% besser als Nicht-KI-Traffic, wobei Nutzer mehr Zeit auf den Webseiten verbrachten, mehr Seiten betrachteten und 37% höhere Einnahmen pro Besuch generierten.

Die Warnung innerhalb der Chance ist, dass viele Einzelhändler immer noch nicht bereit für diesen Traffic sind. Adobe sagt, dass erhebliche Teile von Homepages, Kategorie-Seiten und besonders Produkt-Seiten für LLMs schlecht zugänglich bleiben. Der nächste Optimierungskampf im E-Commerce könnte also nicht nur SEO oder bezahlte Akquise sein. Es könnte sein, ob der KI-Assistent Ihren Katalog tatsächlich korrekt lesen und empfehlen kann.
→ https://techcrunch.com/2026/04/16/ai-traffic-to-us-retailers-rose-393-in-q1-and-its-boosting-their-revenue-too/

[32:30] OUTRO / CLOSE
Das ist die Karte heute: OpenClaw strafft die Runtime um ein neues Standardmodell und einen neuen Sprach-Stack, Anthropic testet, wie man stärkere Fähigkeiten mit Cyber-Schutzzaun herausbringt, Salesforce baut Unternehmenssoftware für Agenten neu auf, Roblox verwandelt Kreation in eine Planungsschleife, Robotik bewegt sich schrittweise zu Transfer-Learning, das tatsächlich überträgt, und Commerce entdeckt, dass KI-Traffic möglicherweise bereits die Gestaltung wert ist.

→ Antworten Sie hier, um die Transkriptgenerierung zu genehmigen.