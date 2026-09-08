Episode 111 — 4. September 2026

[00:00] Episode-Einstieg

Agent Stack Release Readout: OpenClaw v2026.9.1 dominiert den Tag: v2026.9.1 bringt konkrete Änderungen an den Oberflächen, mit denen Entwickler täglich arbeiten, mit den Details weiter unten. Ebenfalls in der heutigen Ausgabe: Ling 3.0 Flash Fin startet auf OpenRouter, ein finance-fokussiertes MoE mit 262K Kontext, Ein günstiger Desktop-400GbE-Switch für lokale KI-Cluster, CIQ fügt Agentic Controls und AMD-GPUs zu Fuzzball 4.2 hinzu, plus der Rest eines dicht gedrängten News-Zyklus über Modelle, Tools und Infrastruktur. Jede Geschichte erhält dieselbe Behandlung — was wurde ausgeliefert, der Mechanismus dahinter, und was es für arbeitende Entwickler verändert.

[02:00] Agent Stack Release Readout: OpenClaw v2026.9.1

OpenClaw v2026.9.1, veröffentlicht am 3. September, ist die entwicklerfreundlichste Version, die das Projekt seit einiger Zeit ausgeliefert hat. Die wichtigste Änderung ist visuell: Mermaid-Blöcke rendern jetzt als echte Diagramme in der Control UI und in den nativen macOS-, iOS- und Android-Apps. Auf Mobilgeräten bieten fehlgeschlagene Renderings einen Retry-Button, und jedes Diagramm hat eine Vergrößerungsvorschau, sodass du nicht mehr auf rohen Mermaid-Quellcode in einer Chat-Blase starrst.

Die zweite Änderung betrifft die Installation. Der Standard-npx-Installationspfad führt jetzt eine Quick-Start-Lane aus, die vorhandene Claude Code- oder Codex-Logins und API-Schlüssel erkennt, sie in Echtzeit verifiziert und das Web-Dashboard von einem Vordergrund-Gateway aus öffnet. Der vollständige Setup-Assistent existiert noch, ist aber jetzt als Custom Setup beschriftet, sodass der Standardpfad ein Prompt ist und du direkt chatten kannst.

Die dritte Änderung betrifft Teams. Shared Gateways unterstützen jetzt persönliche Skill-Bibliotheken pro Identität neben dem Workspace-Skill-Set. Du kannst deine eigenen Skills behalten, sie aus ZIP-Archiven importieren und sie pro Identität teilen oder veröffentlichen, was bedeutet, dass derselbe Gateway sowohl gemeinsame Team-Skills als auch private individuelle Skills ohne Konflikte hosten kann.

Die folgenreichste Änderung ist der Updater. `openclaw update` führt jetzt automatisch ein Rollback des npm-Kandidaten durch, wenn die Post-Update-Doctor-Prüfung fehlschlägt. Es bewahrt deine Konfiguration und Secret-Referenzen über ein fehlgeschlagenes Upgrade hinweg auf, übergibt Fehler an einen integrierten Triage-Agenten, wartet auf Plugin-Bereitschaft vor dem Neustart und akzeptiert npm 12 lokale Archive. Von Agenten gestartete Updates können jetzt außerhalb des Gateway-Prozessbaums abgeschlossen werden, sodass sich ein sich selbst aktualisierender Assistant nicht auf dem Host festsetzt. Wenn du auf 2026.8.2 ohne Service Manager bist, weisen die Release Notes darauf hin, einmal `openclaw update --no-restart` auszuführen, um sauber zu landen; danach proceeds the updater ohne einen Gateway-Service weiter, anstatt sich zu weigern.

Gateway-Resilienz rundet es ab. Der Start erholt sich unter Last und mit großen Agent-Rosters. Legacy-Cron-Zeilen, die nicht geparst werden, werden quarantäniert, anstatt den Boot zu blockieren. Migrationswarnungen degradieren das Gateway, anstatt den Start zu verweigern. Lokale Modell-Server werden zu den bevorzugten OOM-Zielen. Windows Gateways bleiben jetzt nach einem Agent-Neustart online.

Schließlich sind Codex-"Allow Always"-Genehmigungen jetzt dauerhaft für MCP-Tools auf OpenClaw-konfigurierten Servern. Genehmigungen folgen der Haltung der Sitzung, und Genehmigungen, die einer aktiven Codex-Platzierung erteilt wurden, werden wiederverwendet, anstatt erneut nachgefragt zu werden, sodass du nicht mehr zweimal hintereinander dieselbe Frage gestellt bekommst.

[03:26] Ling 3.0 Flash Fin landet auf OpenRouter, ein finance-fokussiertes MoE mit 262K Kontext

InclusionAI hat ein finance-fokussiertes Modell auf OpenRouter namens Ling 3.0 Flash Fin veröffentlicht. Es ist ein Mixture-of-Experts-Ableger von Ling 3.0 Flash, mit 5,1 Milliarden aktiven Parametern von insgesamt 124 Milliarden und einem 262.144-Token-Kontextfenster. Die Modellkarte beschreibt es als für reale Investitionsarbeit konzipiert, was es in eine Kategorie einordnet, in der aufgabenspezifisch abgestimmte Modelle auf eine Branche abzielen, anstatt den Generalisten-Rankings hinterherzujagen.

Was für Entwickler zählt, ist die Kombination aus Form und Zugang. Ein 262.144-Token-Fenster ist groß genug, um einen Jahresbericht, mehrere Earnings Calls und eine Research Note in einem einzigen Prompt unterzubringen, ohne aggressives Chunking. Das MoE-Design bedeutet, dass nur etwa 5,1B Parameter pro Token feuern, was Latenz und Kosten näher an einem kleinen Dense-Modell hält, obwohl der gesamte Parameterpool bei 124B liegt. Das ist ein nützliches Profil für Retrieval-Pipelines, die lange Finanzdokumente bei jeder Aktualisierung neu zusammenfassen.

OpenRouter-Exposition ist das Praktische. Jede App, die bereits mit OpenRouter verdrahtet ist, kann Ling 3.0 Flash Fin umschalten, ohne eine separate Hosting-Vereinbarung, was die Hürde für A/B-Tests gegen vorhandene Finance-Prompts senkt. Das Nächste, worauf man achten sollte, ist eine aktualisierte Modellkarte mit konkreten Benchmark-Zahlen — die Beschreibung benennt reale Investitions-Workflows, legt aber noch keine spezifischen Evaluations-Suites fest, also fehlen noch echte Scores, um Erwartungen zu verankern.

[04:51] Ein günstiger Desktop-400GbE-Switch für lokale KI-Cluster

ServeTheHome hat einen Praxistest des MikroTik CRS804-4DDQ-hRM veröffentlicht, eines Vier-Port-400GbE-Switch, den die Seite in seinem eigenen lokalen KI-Cluster betreibt. Das Interessante daran ist das Formfaktor: 400-Gigabit-Ethernet war bisher ein Rechenzentrums-Fabric, die Art von Ding, die man in ein Rack schrauben würde, mit einem Servicevertrag dahinter. MikroTik hat es auf einen Schreibtisch gestellt, auf Annapurna-Labs-Silizium (Marvells Netzwerk-fokussierte Linie), und verkauft es zu der Preisschwelle, für die die Marke bekannt ist.

Für lokale KI-Arbeit ist das wichtig, weil das Netzwerk oft der stille Engpass ist. Wenn du ein Modell über mehrere GPUs verteilst — oder über mehrere Maschinen — verbringen die Karten Zeit damit, aufeinander zu warten. Ein 400Gbps pro Port Fabric bedeutet, dass ein einzelner Switch Daten zwischen Beschleunigern schnell genug bewegt, dass das Netzwerk aufhört, der langsame Teil zu sein.

Der Test ist ein praktischer Blick auf die Verwendung der Box in diesem Umfeld, keine Spec-Sheet-Zusammenfassung. ServeTheHome betreibt sie als Teil eines lokalen KI-Clusters, und das ist der Lastfall, der entscheidet, ob ein Switch wie dieser tatsächlich nützlich oder nur beeindruckend auf dem Papier ist.

Für Entwickler ist die Headline, dass 400GbE sich von Enterprise-exklusiv zu etwas bewegt, das ein kleines Labor oder ein ernsthaftes Home-Setup plausibel kaufen kann. Menschen, die bereits 100GbE- oder 200GbE-Fabric betreiben, müssen sich nicht beeilen — aber wenn du einen Multi-GPU-Build planst und Spielraum bei den Interconnects willst, lohnt es sich, diese Kategorie im Auge zu behalten.

[06:23] CIQ fügt Agentic Controls und AMD-GPUs zu Fuzzball 4.2 hinzu

CIQ, das Enterprise-Software-Unternehmen hinter Rocky Linux, hat am 3. September Fuzzball 4.2 von seinem Hauptsitz in Reno, Nevada, aus veröffentlicht. Fuzzball ist die schlüsselfertige Plattform des Unternehmens für Sovereign KI und High-Performance-Computing – um es einfach auszudrücken, ein vorassembliertes Cluster-Stack, mit dem Organisationen große KI- und wissenschaftliche Aufgaben auf Hardware betreiben können, die sie kontrollieren, ohne Kapazität von einem Hyperscaler mieten zu müssen.

Die wichtigste Änderung ist ein neuer Model Context Protocol Server, oder MCP. MCP ist der offene Standard, der es KI-Agenten ermöglicht, auf strukturierte Weise mit externen Tools zu kommunizieren; Sie haben ihn wahrscheinlich bei Claude Desktop oder IDE-Coding-Assistenten gesehen. Mit Fuzzball 4.2 kann ein KI-Agent den Cluster steuern – Jobs einreichen, den Status prüfen, Ergebnisse abrufen – aber nur, wenn ein Operator für jede Funktion explizit Berechtigungen erteilt hat. Das ist ein bedeutsamer Unterschied zu einem Chatbot, der nur chatten kann, und zu einem Skript, das nur ausführen kann, was fest einprogrammiert wurde.

Die zweite Änderung ist die Unterstützung von AMD GPUs zusätzlich zu der Hardware, auf der Fuzzball bereits lief. Für Entwickler bedeutet das, dass die Plattform nicht mehr an einen einzigen Accelerator-Hersteller gebunden ist – eine Organisation kann die GPU wählen, die zu ihrer Arbeitslast oder ihrem Budget passt.

Innerhalb des Clusters können die Workflows, die Fuzzball orchestriert, nun selbst zusätzliche Arbeit einleiten. Ein Job, der fertig ist, kann eine Folgetask an den Scheduler zurückgeben, anstatt darauf zu warten, dass ein Mensch den nächsten Knopf drückt. Das ist der Wandel hin zu agentic HPC – der Cluster beginnt, seine eigene Warteschlange zu verwalten.

Ein Punkt, den man im Auge behalten sollte: wie sich das Berechtigungsmodell auf diesem MCP Server weiterentwickelt. Jeder Agent-Aufruf an Ihren Cluster ist prüfbar, was genau das ist, was ein On-Prem- oder Sovereign-Stack braucht, aber es bedeutet auch, dass CIQ diese Oberfläche sauber halten muss, wenn neue Funktionen hinzugefügt werden.

[08:12] Research Digest: DRACO trainiert Langzeit-Agenten ohne Verifizierer

Die meisten Agenten-Trainings benötigen ein klares „Hat es funktioniert"-Signal am Ende. Echte mehrstufige Aufgaben haben selten eines. Eine neue Methode namens DRACO von IBM Research umgeht diesen Engpass, indem sie Evaluierungskriterien dynamisch generiert, während ein Modell eine Aufgabe übt, die gesamte Ausführung bewertet, wenn sie fertig ist, und dann mathematisch das Verdienst auf die spezifischen Schritte zurückverteilt, die jedes Kriterium erfüllt haben. Kein externer Richter und kein handgeschriebener Test wird während der Ausführung benötigt. Auf AppWorld, dem Agent-Benchmark, der echte Software simuliert, hob DRACO ein Basismodell um 15,9 Punkte an und übertraf sogar Trainingsläufe, die eine Sparse-Ground-Truth-Reward verwendeten. Die Implikation für Entwickler ist konkret: Agenten können sich nun bei langen Workflows verbessern, bei denen Erfolg unscharf ist oder erst am Ende bekannt ist – von Multi-App-Geschäftsprozessen bis zu Research-Assistenten – ohne dass jemand zuerst einen Checker bauen muss.

[09:04] ChatGPT verbindet sich mit vertrauenswürdigen Gesundheitsdaten für Kliniker

Kliniker können ChatGPT nun auf vertrauenswürdige Gesundheitsdaten ansetzen und Antworten erhalten, die auf echtem Patientenkontext und medizinischer Forschung basieren, anstatt sich auf die allgemeine Trainierung des Modells zu verlassen. OpenAI kündigte die Integration am 1. September an, und sie zog schnell Aufmerksamkeit auf Hacker News auf sich, mit 490 Punkten.

Das Angebot ist praktisch. Ärzte und Pflegeteams verbringen viel ihres Tages mit der Suche nach Informationen über Patientenakten, Labor­systeme und Journale. Ein Chatfenster, das sicher auf diese Quellen zugreifen kann – die Medikamenten­historie eines Patienten abruft, aktuelle Laborwerte oder die neuesten Studienergebnisse – ist ein anderes Tool als ein Allzweck-Assistent, der aus dem Gedächtnis arbeitet.

OpenAI positioniert dies als einen Weg, ChatGPT innerhalb tatsächlicher klinischer Workflows nützlich zu machen, anstatt nur außerhalb davon. Die genaue Liste der vertrauenswürdigen Datenpartner, der verwendete Integrationsstandard und die Compliance-Zertifizierungen hinter dem Connector werden in der Ankündigung nicht dargelegt, daher lohnt es sich zu beobachten, welche Gesundheitssysteme sich zuerst anmelden.

Für Entwickler im Gesundheitsbereich ist die interessante Frage, was als „vertrauenswürdig" gilt. Wenn OpenAIs Hürde hoch ist, werden die Antworten zuverlässiger, aber die Einführung wird langsam sein. Wenn sie sich schnell öffnet, wächst die Angriffsfläche für Datenschutzfehler. Achten Sie auf die erste Welle benannter Partner und die Geschichte zur Datenresidenz, denn diese Kombination wird entscheiden, ob dies ein ruhiges Back-Office-Tool für Kliniker wird oder ein Frontline-Assistent, dem Patienten tatsächlich begegnen.

[10:35] Research Digest: Ein Topologie-Planer entlastet SOC LLMs

Security Operations Center sind die Orte, an denen Analysten Alerts triagieren und Eindringlinge durch Unternehmensnetzwerke jagen, und eine neue Architektur namens SENTINEL-RL adressiert eine spezifische Schwäche bei der Verwendung großer Sprachmodelle dort. Ein LLM-basierter SOC-Analyst muss den gesamten Authentifizierungsgraphen für Tausende von Hosts in seinem Kontextfenster halten und Containment-Aktionen im Freitextformat entscheiden, ohne Garantie, dass diese Aktionen zur tatsächlichen Topologie des Netzwerks passen. SENTINEL-RL teilt die Aufgabe: ein graph-bewusster Encoder und eine trainierte Reinforcement-Learning-Policy übernehmen die Topologie-Reasoning und wählen investigative Aktionen aus, während das LLM nur diese Empfehlungen liest und für Analysten lesbare Zusammenfassungen schreibt. Im LANL Enterprise-Security-Datensatz erreichte die trainierte Policy 0,91 Precision gegen gelabelte Red-Team-Events, was darauf hindeutet, dass der Planer Graph-Level-Reasoning übernehmen kann, während das Sprachmodell in seiner Rolle als Erzählschicht bleibt. Für Sicherheitsteams ist die offene Frage, ob diese Hybrid-Planer-plus-Erzähler-Aufteilung in Live-Produktionsnetzwerken statt in kuratierten Datensätzen standhält.

[11:32] GitHub Copilot streicht einige Modelle am 2. Oktober

GitHub veröffentlichte am 3. September 2026 einen Changelog-Post, der eine bevorstehende Abschaffung über alle Copilot-Erfahrungen hinweg ankündigt – Copilot Chat, Inline-Edits, Ask-Mode, Agent-Mode und Code-Vervollständigungen –, die am 2. Oktober 2026 in Kraft treten soll. Der Post behandelt „ausgewählte Modelle", aber die Zusammenfassung auf GitHubs Blog bricht ab, bevor sie jede Modell-ID auflistet, daher lebt die konkrete Liste innerhalb der verlinkten Changelog-Seite selbst.

Was aus der Ankündigung klar ist, ist der Umfang: Jede Copilot-Oberfläche ist betroffen, nicht nur Chat. Entwickler, die ein bestimmtes Modell für Inline-Vorschläge ausgewählt oder eines in eine Copilot-Agent-Konfiguration eingebunden haben, müssen ihre Einrichtung vor dem 2. Oktober überprüfen, denn sobald ein Modell abgeschafft wird, werden Anfragen an diese ID nicht mehr funktionieren. Der Bruch trifft Chat-Unterhaltungen, Inline-Edits, Ask- und Agent-Modes und Code-Vervollständigungen am selben Tag – überall, wo Copilot mit diesem Modell geantwortet hat.

Der praktische Schritt ist, den GitHub-Changelog-Post zu öffnen, zu sehen, welche Modell-IDs auf der Liste stehen, und jede Stelle zu überprüfen, an der ein Modell festgelegt ist – IDE-Extension-Einstellungen, Repository-Ebene Copilot-Konfiguration und jeden benutzerdefinierten Agent, der ein bestimmtes Modell benennt. Wenn ein festgelegtes Modell auf der Liste steht, wechseln Sie es vor dem 2. Oktober zu einer noch unterstützten Option, damit Vervollständigungen und Agent-Läufe nicht am Morgen des Termins abbrechen.

Für Teams, die Copilot organisationsweit standardisieren, ist dies eine Erinnerung, dass sich die Modelloberfläche, auf der Sie aufbauen, unter Ihnen ändern kann, und ein periodisches Audit festgelegter Modell-IDs lohnt sich als Teil der Plattformwartung.

[13:08] OpenAI investiert $1 Mrd. in Cyberabwehr für essentielle Dienste

OpenAI kündigte am 3. September Daybreak für Frontline Defenders an, eine Verpflichtung von 1 Milliarde Dollar, die sich an die Betreiber wichtiger Versorgungsleistungen richtet — Versorgungsunternehmen, Krankenhäuser und andere kritische Infrastrukturen. Die Rahmung ist wichtig: OpenAI positioniert seine fortschrittlichsten defensiven Modelle als etwas, auf das Mitarbeiter an vorderster Front Zugriff haben sollten, nicht nur gut ausgestattete Enterprise-Sicherheitsteams.

Das Programm bündelt laut der Ankündigung drei Dinge: Zugang zu Frontier-Cyber-KI, Schulung und laufende Unterstützung. OpenAI hat nicht spezifiziert, welche Modelle oder Produkte unter dem Label „Frontier-Cyber-KI" fallen, noch hat das Unternehmen Partneragenturen benannt oder ein Bewerbungsfenster in der Ankündigung selbst geöffnet. Die Summe von 1 Milliarde Dollar ist eine mehrjährige Verpflichtung, die sowohl die Finanzierung von Tools als auch der menschlichen Befähigung umfasst.

Warum jetzt? Die Verteidigungsteams bei wichtigen Versorgungsleistungen haben das Nachsehen bei einer Asymmetrie gehabt. Angreifer haben KI schnell für Phishing, Reconnaissance und Schwachstellenentdeckung übernommen, während viele Verteidiger noch auf Legacy-Tools angewiesen sind. Frontier-Modelle in die Hände der Menschen zu geben, die das Licht am Laufen halten und die Krankenhäuser am Laufen halten, ist das explizite Argument.

Für Entwickler und Sicherheitsteams bei Versorgungsunternehmen, Krankenhäusern oder kommunaler Infrastruktur ist die praktische Frage, ob Daybreak ein Weg zu finanziertem Zugang wird, anstatt another procurement headache. Der Punkt, den es zu beobachten gilt, ist die Ankündigung der ersten Kohorte — wer wird aufgenommen, welche Tools erhalten sie tatsächlich, und wie werden Schulung und Support im Alltag vermittelt.

[14:37] Gemini 3.8 Flash landet in GitHub Copilot

Googles Gemini 3.8 Flash ist jetzt innerhalb von GitHub Copilot verfügbar und bietet Entwicklern eine neue Modelloption für die tägliche Programmierarbeit. Die 3.8-Generation ist der neueste Eintrag in Googles leichter Flash-Stufe, der Familie, die etwas Roheistung gegen schnellere Antworten und niedrigere Kosten eintauscht. In GitHubs frühen Tests performte das Modell stark bei komplexen terminalbasierten Programmieraufgaben, der Art von mehrstufiger CLI-Arbeit, bei der kleinere Modelle historisch Schwierigkeiten hatten.

Das ist wichtig, weil Copilot-Benutzer typischerweise ein Modell basierend auf dem auswählen, was sie tun. Schwerere Modelle tendieren dazu, die Standardwahl für schwieriges Reasoning zu sein, während Flash-Stufen-Optionen nützlich sind, wenn man schnelle Antworten ohne Warten möchte. Terminal-Workflows — Skripte ausführen, Konfigs bearbeiten, Shell-Befehle verketten — belohnen oft ein Modell, das mit dem Tempo des Tippens Schritt hält.

Für Entwickler ist der praktische Schritt einfach. Wenn Sie ein langsameres Flaggschiff-Modell für routinemäßige CLI-Arbeit verwendet haben, ist es wert, dies auszuprobieren. Das Changelog beschreibt GitHubs Bewertung als rigoros statt vibes-basiert, daher basiert das frühe Signal zumindest auf strukturiertem Testen.

Eine Sache, die es zu beobachten gilt, ist, wie sich das Modell bei chaotischen echten Codebasen statt bei kuratierten Eval-Sets schlägt, und ob die Preisgestaltung in der üblichen Flash-Stufen-Kosten-pro-Prompt-Vorteil bleibt. Das Rollout ging am 3. September in Copilot live.

[15:58] GitHub Copilot-Enterprise-Admins können jetzt jedes Modell als Standard festlegen

GitHub gab Enterprise-Administratoren am 2. September 2026 still und leise einen kleinen, aber nützlichen Hebel. Über unternehmensverwaltete Einstellungen kann ein Administrator jetzt jedes verfügbare Modell als Standard für neue Copilot-Unterhaltungen auswählen. Jeder Entwickler in der Organisation erbt diese Wahl automatisch, was die kleine Reibung beseitigt, jede Person zu bitten, bei der ersten Nutzung ihren Modellpicker zu ändern.

Der praktische Effekt ist Standardisierung. Ein Plattformteam, das sich aus Kosten-, Latenz- oder Compliance-Gründen auf ein Modell standardisiert hat, kann es jetzt einmal in den Admin-Einstellungen festlegen, anstatt sich auf unternehmensweite Richtlinien-Standards zu verlassen, die zuvor weniger Optionen hatten. Einzelne Entwickler können das Standardmodell immer noch pro Unterhaltung überschreiben, sodass niemand die Möglichkeit verliert, zu experimentieren, wenn er möchte.

Für einen Teamleiter, der Copilot in einer neuen Abteilung einführt, entfällt damit ein Teil der Onboarding-Paperwork. Für einen Sicherheits- oder Finanzleiter, der die Copilot-Nutzung überprüft, bedeutet dies, dass das Standardmodell in Logs und Abrechnungen das ist, was das Unternehmen tatsächlich gewählt hat, nicht das, was die Plattform in dieser Woche auszuliefern beschlossen hat. Dieser letzte Punkt ist der leise Grund, warum diese Änderung wichtig ist: Das Standardmodell ist jetzt eine Unternehmensentscheidung statt einer globalen.

[17:11] Metas neues Agentenmodell bietet 95% Rabatt im Austausch für Ihre Prompts

Meta hat gerade einen Preis auf etwas gesetzt, das die meisten Labs stillschweigend behandeln: Ihre Konversationshistorie mit einem KI-Modell. Das neue Muse Spark des Unternehmens, das für das Ausführen von Coding-Agenten und anderen autonomen Workflows entwickelt wurde, kostet fast nichts, wenn man Meta mitlesen lässt.

Hier ist das Angebot. Anstatt des Standardtarifs bietet Meta Nutzern ungefähr 95% Rabatt im Durchschnitt im Austausch für das Teilen ihrer Prompts und der Modellantworten. Der Austausch ist explizit und im Voraus — tragen Sie Ihren Traffic zur Entwicklung zukünftiger Modelle bei, zahlen Sie etwa ein Zwanzigstel von dem, was andere Nutzer zahlen. TechCrunch berichtete über das Programm am 3. September.

Das macht Muse Spark zu einem der günstigsten Wege, ein Agentenmodell auf realen Coding-Workloads zu betreiben, und es wird wahrscheinlich unabhängige Entwickler und kleine Teams anziehen, die von etablierteren Agenten-APIs preislich ausgeschlossen waren.

Der Haken ist die Daten. Prompts, die an einen Agenten gesendet werden, der Code schreibt oder bearbeitet, enthalten tendenziell den Code selbst — manchmal proprietär, manchmal unter NDA, manchmal mit Kundeninformationen. Metas Rabatt ist genau deshalb großzügig, weil dieser Traffic hochwertiges Trainingsmaterial für die nächste Generation von Agentenmodellen ist. Wenn Sie dies aktivieren, etikettieren Sie effektiv Ihre private Codebasis als Trainingsbrennstoff.

Für einzelne Entwickler, die an Open-Source- oder persönlichen Projekten arbeiten, ist die Rechnung attraktiv. Für Teams, die Kundencode, interne Tools oder anything under contract bearbeiten, lohnt es sich, die Beitragsbedingungen Zeile für Zeile zu lesen, bevor man den Schalter umlegt. Beobachten Sie, wie Meta angibt, was es aufbewahrt, und ob der Rabattsatz bleibt, wenn mehr Nutzer beitreten.

[18:51] f/prompts.chat — ehem. Awesome ChatGPT Prompts. Prompts teilen, entdecken und sammeln von den Machern von Awesome ChatGPT Prompts.

f.k.a. Awesome ChatGPT Prompts. Teilen, entdecken und sammeln Sie Prompts aus der Community. Kostenlos und Open Source — self-hosting für Ihre Organisation mit vollständiger Datenschutz. Die Primärquelle auf github.com unterstützt nur diese genannten Fakten; nicht unterstützte Spezifikationen werden bewusst weggelassen. Die Primärquelle unterstützt die spezifische Produkt- oder Workflow-Änderung oben; sie unterstützt keine breiteren Behauptungen über Leistung, Kompatibilität oder Bereitstellung. Testen Sie die quellengestützte Änderung anhand eines realen Workflows, bevor Sie sich darauf verlassen.

[19:18] NVIDIA und CrowdStrike stärken die agentische Cybersicherheits-Front

„Wir befinden uns an einem Wendepunkt in der Cybersicherheit", sagte Jensen Huang einem ausverkauften Publikum auf CrowdStrikes Fal.Con 2026 in Las Vegas am Dienstag. Angriffe sind jetzt automatisiert. Die Verteidigung muss es auch sein. Der NVIDIA-Gründer und CEO schloss sich CrowdStrike-CEO und -Gründer George Kurtz an, um CrowdStrike SafeMind anzukündigen, sein agentisches Cybersicherheitssystem, entwickelt von CrowdStrike Cyber [&#8230;]. Der Mechanismus ist eine rechtliche oder Richtliniengrenze, keine API-Änderung. Die quellengestützten Fakten definieren, was vorgeschlagen, entschieden oder erklärt wurde, ohne dies zum universellen Gesetz zu machen. Entwickler sollten die konkrete Regel, Entscheidung oder Zugriffsänderung verfolgen und vermeiden, ein Produkt nur aufgrund einer Schlagzeile zu ändern.