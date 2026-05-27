[NOVA]: Ich bin NOVA.

[ALLOY]: Ich bin ALLOY, und das ist AgentStack Daily. Heute beginnen wir mit OpenClaw v2026.5.22 und Claude Code 2.1.149, weil beide Versionen die Mechanismen verändert haben, von denen Agent-Stacks abhängen: Gateway-Start, Plugin-Metadaten, Meeting-Notizen, Discord-Callbacks, Cloud-MCP-Connectoren, Nutzungsabrechnung, Diffs und Shell-Sicherheit.

[NOVA]: Dann wandern die Neuigkeiten nach außen. Google verwandelt Gemini-Agents in verwaltete Remote-Linux-Umgebungen. OpenAI bringt Codex-Arbeit unter mobile Aufsicht und in hybride Enterprise-Setups. Anthropic hat Stainless gekauft und Project Glasswing aktualisiert, was SDK-Generierung, MCP-Server und KI-Sicherheitsscanning in dieselbe Diskussion bringt.

[ALLOY]: Und die GitHub-Projekt-Spur ist heute real: semantische Code-Maps, aktuelle Dokumentationstools, Modell-Router, MCP-Builder, lokale Agents, Rollen-Pakete und Sicherheitsscanner. Keine Repo-Trivialitäten. Tools, die wirklich ändern können, was Claude Code, Codex, Hermes, OpenClaw und MCP-Clients tatsächlich sehen und tun können. ...

[NOVA]: OpenClaw v2026.5.22 ist eine umfangreiche Version, aber die Headline ist klar: Das Gateway wird weniger fragil, die Plugin-Oberfläche wird wiederverwendbarer, Meeting-Notizen werden zu einer besseren Quelle für Agent-Kontext, und mehrere Provider- und Medienpfade werden präziser.

[ALLOY]: Starten wir beim Gateway-Startup. OpenClaw verwendet jetzt prozessstabile Katalog-Lesevorgänge und Plugin-Metadaten-Snapshot-Wiederverwendung. Das bedeutet, das System kann sich auf stabile Katalog- und Metadaten-States verlassen, anstatt immer wieder dasselbe Bild der Welt neu aufzubauen. Für einen lokalen Agent-Host ist das wichtig, weil Startup und Statusprüfungen der erste Reibungspunkt sind. Wenn der Host vor Beginn der Aufgabe nervig ist, fühlt sich alles darüber unzuverlässig an.

[NOVA]: Träges Startup-Idle-Plugin-Work gehört in dieselbe Kategorie. Arbeit, die den ersten nutzbaren Moment nicht blockieren muss, kann warten. Irrelevante Linuxbrew-Pfad-Probes werden übersprungen. Core-Gateway-Methoden-Handler und Public-Surface-Alias-Maps werden aufgeräumt. Das sind keine flashy Features, aber sie verändern das Gefühl der Kontrollebene: weniger sinnlose Prüfungen, vorhersehbarere Methodennamen und weniger Arbeit, nur weil der Prozess aufgewacht ist.

[ALLOY]: Meeting-Notizen bekommen eines der wichtigsten Capability-Updates. Externe Meeting-Notes-Plugins und Quell-Provider haben jetzt einen saubereren Vertrag. Capture kann jetzt automatisch aus der Konfiguration starten. Manuelle Imports werden unterstützt. Read-only-CLI-Zugriff existiert. Discord-Voice wird als erste Live-Quelle behandelt, statt als Nebeneingang.

[NOVA]: Das ist ein echtes Agent-Stack-Feature, weil viele wertvolle Anweisungen nicht als sauber getippten Text ankommen. Sie kommen als Anruf, Sprachnachricht, schnelle Korrektur oder Kanaldiskussion an. Diese Quellen in strukturierten, lesbaren Kontext zu verwandeln, ohne jedem Tool Schreibzugriff auf den Quelldatensatz zu geben, ist der nützliche Teil.

[ALLOY]: Das Plugin-SDK bekommt auch mehr gewöhnliche Operationen eingebaut: generisches Kanal-Nachrichten-Polling-Sending, Session-Workflow-Helfer und klarere Embedding-Provider-Capability-Verträge. Das klingt nach Klempnerarbeit, aber es ist die Art von Klempnerarbeit, die jeden Plugin-Autor daran hindert, eine leicht unterschiedliche Version desselben Tool-Aufrufs zu erfinden.

[NOVA]: Subagents werden auch weniger verschwenderisch. Der Standard-Bootstrap wird auf die wichtigsten Dateien reduziert, und native Subagent-Completion-Handoffs bekommen Fehlerbehebungen. In der Praxis braucht ein delegierter Agent genug Kontext, um die Aufgabe zu erledigen, und einen zuverlässigen Pfad, um die Antwort zurückzugeben. Zu viel geerbter Kontext macht den Subagent träge; ein kaputter Handoff lässt gute Arbeit am falschen Ort verschwinden.

[ALLOY]: Der Chat-Session-Picker bekommt Search und Load-More-Pagination. Das ist ein kleines UI-Feature, bis das System Wochen echter Sessions hat. Dann wird das Finden eines alten Runs Teil der Arbeit. Ein Gateway mit Historie braucht Navigation, nicht nur einen Haufen kürzlicher Chats.

[NOVA]: Discord-Component-Callbacks haben jetzt eine begrenzte Lebensdauer. Das ist eine gesunde Änderung für Review-Buttons, Genehmigungen und kleine interaktive Controls. Ein Button auf einer alten Nachricht sollte nicht für immer aktiv bleiben, nur weil die Nachricht noch existiert. Die Interaktionsfläche hat jetzt ein klareres Ablaufmodell.

[ALLOY]: Provider-Handling wird auch konkreter. xAI OAuth kann für Grok-Websuche wiederverwendet werden. Modell-Aliase und Operations-Timeouts bekommen Aufräumarbeiten. Antigravity CLI wird zu einem niedriger priorisierten Image- und Video-Fallback nach konfigurierten Provider-APIs. Codex-API-Key-Bildgenerierung verwendet die native OpenAI Images API. Lokale Chrome- und lokale Ollama-Proxy-Bypasses bekommen Fehlerbehebungen.

[NOVA]: Das ist die wahre Provider-Geschichte: nicht nur welches Modell antwortet, sondern wie Auth wiederverwendet wird, wie lange Anrufe laufen dürfen, welcher Fallback gewinnt und ob lokale Services versehentlich durch den falschen Proxy geroutet werden. Agent-Stacks scheitern an diesen Rändern genauso oft wie am Reasoning.

[ALLOY]: OpenClaw aktualisiert auch Abhängigkeiten, verschiebt protobufjs auf 8.4.0, verschärft die Locked-Dependency-Arbeit, bereinigt Kataloge, räumt Session-Write-Locks auf, fügt strikteres Verhalten für vLLM-Tool-free-Turns hinzu und behebt Telegram-Topic-Handling. Das ist eine Maintenance-Version mit einem langen Schwanz, aber die Form ist kohärent: Startup, Quell-Capture, Plugin-Wiederverwendung, Provider-Korrektheit, Session-Navigation und Dependency-Hygiene.

[NOVA]: Das Claude-Code-Update ist kleiner, aber es landet im täglichen Gebrauch. Der /usage-Befehl kann die Limit-Nutzung nach Kategorie aufschlüsseln: Skills, Subagents, Plugins und Kosten pro MCP-Server. Das ist eine bedeutende Änderung, weil Coding-Agent-Sessions keine einzelnen Modell-Aufrufe mehr sind. Es sind Tool-Aufrufe, MCP-Aufrufe, Helfer-Agents, Skills, Plugins und manchmal Hintergrundarbeit. Nutzung braucht eine Karte.

[ALLOY]: Die /diff-Detailansicht bekommt Keyboard-Scrolling. Markdown-Output rendert GitHub-flavored Task-List-Checkboxes. Das sind ergonomische Fehlerbehebungen, aber Terminal-Agents leben und sterben an Review-Flächen. Eine bessere Diff-Ansicht und klarere Task-Listen bedeuten weniger Reibung, wenn ein Mensch entscheidet, ob der Agent die Sache tatsächlich erledigt hat.

[NOVA]: Enterprise-Admins bekommen allowAllClaudeAiMcps, eine verwaltete Einstellung für das Laden von claude.ai-Cloud-MCP-Connectoren neben der verwalteten MCP-Konfiguration. Das ist die Policy-Seite der MCP-Geschichte. Cloud-Connectoren sind nützlich, aber Organisationen brauchen einen klaren Schalter dafür, welche Connector-Oberflächen erlaubt sind, statt jeden Benutzer improvisieren zu lassen.

[ALLOY]: Die Fehlerbehebungen sind der ernsthaftere Teil. Claude Code repariert PowerShell-Permission-Bypasses durch eingebaute Directory-Change-Funktionen. Es behebt Sandbox-Write-Allowlists, die zu viel des Git-Worktrees abdecken konnten. Es behebt PowerShell-Prefix- und Wildcard-Rule-Bugs. Es korrigiert veraltetes Variables-Tracking rund um PWD, OLDPWD und DIRSTACK. Es behebt ein macOS-Find-Problem, das Dateitabellen bei großen Verzeichnissen erschöpfen konnte.

[NOVA]: Das ist ein Shell-Sicherheits-Release-Hinweis, nicht nur eine Fehlerliste. Coding-Agents führen Befehle in chaotischen Umgebungen aus. Verzeichniswechselnde Builtins, Wildcard-Regeln, Worktrees, Umgebungsvariablen und Dateideskriptor-Limits sind genau die Stellen, an denen eine sicher aussehende Richtlinie undichte Stellen haben kann. Ein CLI-Agent, der Berechtigungen ernst nimmt, muss diese langweiligen Randfälle behandeln.

[ALLOY]: Der nächste Patch ist auf npm latest, aber sein Changelog-Eintrag betrifft nur interne Infrastruktur. Also ist das nutzerseitige Delta der frühere Patch, den wir gerade behandelt haben. Diese Unterscheidung ist wichtig: Installationszahlen können sich ändern, während die Feature-Geschichte zu dem Release gehört, das tatsächlich das Verhalten geändert hat.

[NOVA]: Codex und Hermes haben keine neueren stabilen Tags für diesen Release-Bericht, aber sie bleiben in der Episode, weil die Nachrichten rund um Remote-Codex-Supervision, MCP-Tools, lokale Agents und Code-Intelligence-Repos dieselbe Stack betreffen. Das Release-Segment ist das Fundament; der Rest der Episode ist dort, wo sich die Umgebung um dieses Fundament herum bewegt. ...

[ALLOY]: Der stärkste Anwendungsfall für dieses OpenClaw-Release ist ein Gateway, das mehrere echte Oberflächen gleichzeitig hosten muss: Chat, Sprache, Plugins, Medienerstellung, Suche und Subagents. Ein Spielzeug-Setup kann mit unwillkommenem Startup-Verhalten überleben. Ein täglicher Build kann das nicht. Wenn Kanal-Kataloge, Plugin-Metadaten, Source-Capture und Provider-Fallbacks alle im selben Release sauberer werden, wird der Agent-Host weniger zu einem Haufen Glückspfade.

[NOVA]: Der stärkste Anwendungsfall für das Claude Code-Update ist ein Team, das über einen Terminal und einen Model-Aufruf hinausgegangen ist. Nutzung nach Kategorie zeigt, ob Skills, Plugins, Subagents oder MCP-Server die Limits antreiben. Bessere Diff-Navigation macht Code-Review weniger schmerzhaft. Cloud-MCP-Richtlinie gibt Administratoren eine klarere Build-Oberfläche. Die PowerShell- und Sandbox-Fixes sind die Leitplanken, die diese Features in echten Shells weniger beängstigend machen.

[ALLOY]: Zusammengefasst ist die Release-Nachricht nicht nur "aktualisiert eure Tools". Es ist, dass das lokale Gateway und die Coding-CLI beide die harten Lektionen der Agentenarbeit absorbieren: Kontext kommt aus chaotischen Quellen, Tools brauchen Richtlinien, Provider-Verhalten braucht Namen, und Shell-Grenzen müssen präzise sein. Das ist die Build-Richtung, die man im Auge behalten sollte.

[ALLOY]: Googles Gemini-Geschichte hat zwei Schichten. Die erste ist das Model: Gemini 3.5 Flash ist positioniert für Agentic-Work und Coding, mit Behauptungen rund um Terminal-Bench, GDPval-AA, MCP Atlas, multimodale Geschwindigkeit und Langzeitaufgaben.

[NOVA]: Diese Benchmark-Namen sind wichtig, weil sie auf Tool-intensives Arbeiten hinweisen. Ein Model kann im Chat charmant sein und trotzdem zusammenbrechen, wenn es einen Terminal benutzen, Tools aufrufen, Dateien inspizieren, sich von schlechten Beobachtungen erholen und über eine lange Aufgabe hinweg Zustand halten muss. Google versucht explizit, Flash als schnell genug für Loops und fähig genug für Agentenarbeit zu verkaufen.

[ALLOY]: Die zweite Schicht ist wichtiger: Gemini API Managed Agents. Entwickler können einen Antigravity-powered Agent in einer isolierten, ephemeren Linux-Umgebung starten. Der Agent kann reasoning betreiben, Tools aufrufen, Code ausführen, Dateien verwalten und im Web browsen. Follow-up-Aufrufe können die Umgebung wiederverwenden, sodass eine Aufgabe mit echtem Session-State fortgesetzt werden kann, anstatt so zu tun, als ob jede Anfrage bei Null anfängt.

[NOVA]: Dieses Umgebungsmodell ist das Produkt. Es ist nicht nur "schick einen Prompt an ein Model". Es ist ein Remote-Linux-Workspace mit Tools, Dateien, Browsing, Fortsetzung und Agent-Anweisungen. Google sagt auch, dass benutzerdefinierte Agents mit AGENTS.md- und SKILL.md-Style-Dateien plus zusätzlichen Daten definiert werden können. Das ist ein klares Signal, dass das Harness um das Model zu einer erstklassigen API-Oberfläche wird.

[ALLOY]: Für OpenClaw-, Hermes-, Codex- und Claude-Code-Nutzer ist der interessante Vergleich nicht lokal versus Cloud als Slogan. Es geht darum, was die Umgebung wissen und tun darf. Ein Managed-Sandbox ist nützlich, wenn die Aufgabe öffentlich, entsorgbar oder einfach zurückzusetzen ist: ein Open-Source-Repo inspizieren, eine saubere Reproduktion ausführen, Docs durchsuchen, einen nicht-sensiblen Datensatz transformieren oder einen Prototyp in einer kontrollierten Umgebung bauen.

[NOVA]: Lokale Agents haben immer noch den Vorteil, wenn die Arbeit von privaten Dateien, lokalen Credentials, abonnierten Tools, einem echten Browser-Profil, Gerätezugriff oder einer maschinenspezifischen Einrichtung abhängt. Die Managed-Agent-Nachricht löscht den lokalen Stack nicht. Sie gibt Buildiern eine weitere Ausführungsform: entsorgbaren Remote-State anstatt persönlichen Workstation-State.

[ALLOY]: Das Feature-Delta, das man sich merken muss, ist Stateful Managed Execution. Ein Remote-Agent, der Dateien behalten, eine Session fortsetzen und in einer isolierten Linux-Umgebung browsen kann, ist anders als ein Stateless Model Endpoint. Er kann Beweise akkumulieren. Er kann Abhängigkeiten installieren. Er kann Artefakte für den nächsten Aufruf hinterlassen. Er kann auch Lock-in um die Sandbox und das Tool-Modell der Plattform herum erzeugen.

[NOVA]: Deshalb ist die Custom-Instruction-File-Unterstützung wichtig. AGENTS.md- und SKILL.md-Style-Dateien lassen die Umgebung Projekt-Regeln und spezialisiertes Verhalten tragen. Derselbe Trend zeigt sich über Coding-Agents hinweg: das Model ist nur ein Teil. Die Regeln, Tools, Filesystem, Browser, Richtlinie und Fortsetzungsmodell entscheiden, ob der Agent wie Software arbeiten kann oder nur über Software reden.

[ALLOY]: Die praktische Empfehlung ist kurz: nutzt Managed Gemini Agents zuerst dort, wo Isolation der Punkt ist. Public-Repo-Triage, saubere Bug-Reproduktion, generierte Scripts und Doc-gestützte Recherche sind natürliche Anwendungsfälle. Behaltet Secrets, private Repos und maschinenspezifische Workflows in lokalen oder eng kontrollierten Umgebungen, bis die Managed-Grenze klar verstanden ist.

[NOVA]: Das größere Industriesignal ist, dass Agent-Infrastruktur jetzt direkt verkauft wird. Nicht versteckt als interne Orchestrierung, nicht angebaut als Demo. Die Sandbox, der Tool-Runner, die Browsing-Schicht, der Session-Store und die Custom-Agent-Dateien sind Teil des Developer-Produkts. ...

[ALLOY]: Ein Anwendungsfall sticht sofort heraus: reproduzierbare Investigation. Ein Managed Agent kann von einer sauberen Linux-Umgebung starten, ein öffentliches Issue holen, die Reproduktion bauen und eine stateful Spur für einen Follow-up-Aufruf hinterlassen. Das ist anders als einen Chatbot zu fragen, was vielleicht falsch sein könnte. Die Umgebung kann den eigentlichen Checkout, Logs, generierte Artefakte und die Befehle, die sie erzeugt haben, enthalten.

[NOVA]: Ein weiterer Anwendungsfall ist entsorgbare Automatisierung rund um öffentliche Daten. Ein Managed Agent kann browsen, Code ausführen und Session-State halten, ohne ein persönliches Laptop zu berühren. Das ist nützlich für Rechercheaufgaben, generierte Beispiele, öffentliche Benchmark-Checks und kleine Datentransformationen. Es ist nicht der richtige Ort für jeden privaten Build, aber es ist genau die richtige Form für Arbeit, wo saubere Isolation ein Vorteil ist.

[ALLOY]: Die Build-Implikation ist, dass AGENTS.md- und SKILL.md-Style-Dateien zu portablem Agent-Packaging werden. Ein Projekt kann seine eigenen Regeln, Tool-Präferenzen und Konventionen in eine Remote-Agent-Umgebung tragen. Das macht die Instruction-Layer dauerhafter als ein One-off-Prompt und inspizierbarer als ein unsichtbares Produkt-Preset.

[ALLOY]: OpenAIs Codex-Nachricht dreht sich darum, wo Coding-Agent-Arbeit lebt und wie Menschen sie supervisen. Codex in der ChatGPT-Mobile-App kann sich mit aktiver Arbeit verbinden, die auf einem Mac oder einer Remote-Umgebung läuft. Die Mobile-Ansicht kann Live-Projekt-State, Terminal-Output, Screenshots, Testergebnisse und Diffs anzeigen. Der User kann Befehle genehmigen und die Aufgabe umleiten.

[NOVA]: Das verändert die Form langlaufender Programmierarbeit. Der Agent kann in der Nähe des Workspaces weiterlaufen, während die Genehmigungsoberfläche zum Menschen verlagert wird. Eine Sitzung muss nicht ins Stocken geraten, nur weil die Person den Schreibtisch verlassen hat. Das Wichtige ist nicht die mobile Neuheit. Es geht darum, den Ausführungsort vom Überwachungsort zu trennen.

[ALLOY]: Sichere Relay-Zustandsverwaltung ist die Architektur, die man im Auge behalten sollte. Der Code, die Anmeldedaten, Abhängigkeiten und Tools bleiben dort, wo der Agent tatsächlich läuft. Der Mensch erhält genug Echtzeit-Zustand, um woanders Entscheidungen zu treffen. Das ist ein besseres Muster, als jeden lokalen Secret in eine Remote-Chat-Oberfläche zu ziehen.

[NOVA]: Remote-SSH in allgemeiner Verfügbarkeit passt in dieselbe Richtung. Codex kann gegen einen Remote-Host arbeiten, wo das Repo und die Abhängigkeiten bereits liegen. Das kann eine Entwicklungsbox sein, ein Cloud-VM, ein Workstation oder eine verwaltete Enterprise-Umgebung. Die Ausführungsgrenze wird zur Deployment-Entscheidung, nicht zum Nebeneffekt davon, wo das Chat-Fenster geöffnet ist.

[ALLOY]: Programmatische Zugriffstokens sind ein weiteres wichtiges Puzzlestück. Programmier-Agents, die in Automatisierung laufen, brauchen begrenzte Identität. Eine Browser-Sitzung oder ein langlebiges persönliches Secret ist eine wackelige Basis für nicht-interaktive Arbeit. Tokens geben Agent-Workflows einen engeren, widerrufbaren Weg, innerhalb eines Workspaces zu agieren.

[NOVA]: Hooks fügen Policy rund um diese Aktion hinzu. Sie können Prompts auf Secrets scannen, Validatoren ausführen, riskante Operationen blockieren oder lokale Regeln durchsetzen, bevor die Arbeit weitermacht. Hier beginnt Codex weniger wie ein cleverer Terminal-Helfer auszusehen und mehr wie ein Agent-Arbeitssystem mit Checkpoints.

[ALLOY]: Die Dell-Partnerschaft zeigt auf die Enterprise-Version: Codex in Hybrid- und On-Prem-Umgebungen. Manche Organisationen können Quellcode, Logs oder Daten nicht einfach in eine öffentliche Cloud-Coding-Schleife verschieben. Hybrid-Codex geht darum, den Agent näher an genehmigte Compute-, Storage- und Policy-Grenzen operieren zu lassen.

[NOVA]: Die konkrete Codex-Fähigkeitsverschiebung ist folgende: Mobile Überwachung, Remote-Hosts, begrenzte Tokens, Hooks und Hybrid-Umgebungen zeigen alle auf Coding-Agents, die in der Nähe der Daten laufen können, während sie von woanders überwacht werden. Das ist der nützliche Rahmen. Nicht „Agent auf meinem Laptop" versus „Agent in der Cloud", sondern „Wo sollte diese Aufgabe ausgeführt werden, und wo sollte der Mensch sie genehmigen?"

[ALLOY]: Es gibt auch eine Human-Factors-Änderung. Diffs, Screenshots, Terminal-Ausgaben und Testergebnisse werden zu Review-Objekten, die reisen. Wenn diese Objekte klar sind, fühlt sich Remote-Überwachung wie Kontrolle an. Wenn sie vage sind, wird mobile Überwachung zu einem kleinen Fenster in eine Black Box.

[NOVA]: Die Empfehlung ist also, keine großen Refactorings auf ein Handy zu werfen. Mobile Codex-Überwachung für enge Entscheidungspunkte nutzen: einen sicheren Befehl genehmigen, einen Diff-Summary inspizieren, eine Verzweigungsentscheidung umlenken, eine Aufgabe stoppen, die den falschen Pfad eingeschlagen hat. Die schweren Belege müssen immer noch gut genug sein, um zu vertrauen.

[ALLOY]: Die Enterprise-Empfehlung ist ähnlich. Tokens und Hooks für die Automatisierungen nutzen, die nicht-interaktive Identität brauchen. Die Ausführungsumgebung nah am Repo, den Secrets und der Policy halten, die sie braucht. Codex bewegt sich auf eine Welt zu, in der Agent-Arbeit remote, überwacht und regiert sein kann, ohne so zu tun, als ob der Ort keine Rolle mehr spielt. ...

[NOVA]: Der unmittelbare Anwendungsfall ist Remote-Review einer langlaufenden Programmier-Sitzung. Der Agent hat bereits einen Branch gebaut, Tests ausgeführt und einen Diff vorbereitet. Der Mensch ist nicht am Schreibtisch, kann aber trotzdem genug Belege sehen, um einen Befehl zu genehmigen, eine riskante Richtung abzulehnen oder die Sitzung zu stoppen. Das verwandelt Leerlauf-Wartezeit in einen überwachten Checkpoint.

[ALLOY]: Der Enterprise-Anwendungsfall ist kontrollierte Ausführung. Eine Codex-Umgebung kann nah am Codebase, internen Abhängigkeiten und genehmigter Compute liegen. Mobile oder Remote-Überwachung kann außerhalb dieser Grenze stattfinden, aber die Dateien und Anmeldedaten müssen nicht mit dem Reviewer wandern. Das ist der architektonische Unterschied zwischen bequemer Fernsteuerung und leichtsinnigem Fernzugriff.

[NOVA]: Hooks machen das mehr als Remote-Bildschirm-Peeking. Ein Hook kann einen Secret-Eintrag im Prompt blockieren, einen Validator verlangen, bevor ein Patch als fertig gilt, oder eine Repo-Grenze durchsetzen, bevor der Agent handelt. Programmatische Tokens geben diesen Jobs eine begrenzte Identität. Zusammen machen sie Codex mehr wie ein regierbares Build-System für Agent-Arbeit aussehen.

[NOVA]: Die Übernahme von Stainless durch Anthropic ist eine Agent-Konnektivitäts-Geschichte. Stainless verwandelt API-Specs in SDKs, CLIs und MCP-Server über Sprachen hinweg. Anthropic sagt, Stainless hat seit Anfang des Claude-API offizielle Anthropic-SDKs generiert.

[ALLOY]: Das ist wichtig, weil Agents Handles brauchen. Ein Agent, der nur Text lesen kann, ist begrenzt. Ein Agent, der ein typisiertes SDK aufrufen, eine CLI aufrufen oder einen MCP-Server nutzen kann, kann auf echten Systemen agieren. Die Qualität dieser generierten Oberflächen entscheidet, ob die Aktion sicher, vorhersehbar und verständlich ist.

[NOVA]: API-Specs werden zur Agent-Infrastruktur. Eine saubere Spec kann Dokumentation, Client-Bibliotheken, Kommandozeilen-Tools und MCP-Tool-Oberflächen werden. Eine vage Spec wird zu einem vagen Agent-Tool. Wenn die Methodennamen unklar sind, Auth underspezifiziert ist, Pagination inkonsistent ist oder Fehler noisy sind, erbt der Agent diese Mehrdeutigkeit.

[ALLOY]: Stainless innerhalb von Anthropic macht diesen Tool-Generierungspfad zentraler für das Claude-Ökosystem. Es ist nicht schwer, sich eine Zukunft vorzustellen, in der das Erstellen einer guten API-Spec auch eine gute Claude-zugewandte Tool-Oberfläche erstellt: SDK für Anwendungscode, CLI für Menschen und Automatisierung, MCP-Server für Agents.

[NOVA]: Die kurze Builder-Implikation ist einfach: Wenn eine interne API von Agents genutzt werden sollte, dann zählt die Spec-Qualität jetzt mehr. Types, Auth-Scopes, Nur-Lese-Methoden, mutierende Methoden, Pagination, Rate-Limits und Fehler sind nicht mehr nur Developer-Experience-Details. Sie sind der Unterschied zwischen einem Agent, der das System sauber aufrufen kann, und einem Agent, der improvisiert.

[ALLOY]: Project Glasswing ist die andere Hälfte. Anthropic sagt, Claude Mythos Preview wurde mit Partnern über mehr als tausend Open-Source-Projekte genutzt und hat große Mengen an Hoch- und Kritisch-Schweregrad-Schwachstellen gefunden. Die Headline ist nicht nur „KI findet Bugs." Es ist, dass Frontier-Modelle die Rate der Schwachstellen-Entdeckung genug erhöhen können, dass Verifizierung und Offenlegung zum Flaschenhals werden.

[NOVA]: Das ist ein sehr anderer Druck als gewöhnliches Code-Review. Ein Modell kann einen echten Exploit-Pfad, ein partielles Problem, ein False Positive oder einen Fund aufzeigen, der sorgfältige Offenlegung braucht. Mehr mögliche Issues zu finden ist nur nützlich, wenn Maintainer verifizieren, priorisieren, patchen und verantwortungsvoll kommunizieren können.

[ALLOY]: Das hängt direkt mit MCP und SDK-Generierung zusammen. Besser generierte Tools geben Agenten mehr Reichweite in Systeme. Bessere Sicherheitsmodelle geben Agenten mehr Möglichkeiten, diese Systeme zu inspizieren. Dieselbe Beschleunigung macht sowohl Produktivität als auch Risiko größer.

[NOVA]: Die praktische Empfehlung ist, agentenunterstütztes Sicherheits-Scannen als begrenzte Aktivität zu behandeln, nicht als beiläufiges Hobby im Hintergrund. Nutze es dort, wo das Repository, die Anforderungen an Beweise, der Offenlegungspfad und der Reparaturverantwortliche klar sind. Die Ausgabe sollte ein Befund mit Beweisen und einer Patch-Richtung sein, kein dramatisches Sammelsurium von Behauptungen.

[ALLOY]: Was Anthropic diese Woche insgesamt zeigt, ist, dass Agenten bessere Schnittstellen und bessere Bremsen brauchen. Stainless ist die Schnittstellen-Geschichte: Spezifikationen in SDKs, CLIs und MCP-Server umwandeln. Glasswing ist die Bremsen-Geschichte: Schnellere Entdeckung braucht Verifizierung, Offenlegung und Reparaturkapazität.

[NOVA]: Die stärkste Version dieses Stacks ist kein Agent mit unbegrenzter Reichweite. Es ist ein Agent mit gut beschriebenen Tools, engen Berechtigungen, sichtbaren Protokollen und genug Sicherheitshilfe, um echte Schwachstellen zu finden, ohne Maintainer mit Rauschen zu überfluten. ...

[ALLOY]: Der Stainless-Anwendungsfall ist straightforward: eine Servicebeschreibung in Tools umwandeln, die sowohl Menschen als auch Agenten tatsächlich nutzen können. Eine saubere API-Spezifikation kann ein typisiertes SDK für Application-Code, eine CLI für Skripte und Menschen, und einen MCP-Server für Agentenaufrufe erzeugen. Das schafft eine einzige Quelle für Interface-Wahrheit statt drei driftender Wrapper.

[NOVA]: Der Glasswing-Anwendungsfall ist kein beiläufiges Bug-Hunting. Es ist gezielte Sicherheitsentdeckung mit Beweisen. Ein Modell, das große Codebasen inspizieren und hochkritische Probleme finden kann, verändert die Ökonomie der Schwachstellenforschung. Aber die nützliche Ausgabe ist immer noch ein verifizierter Befund, ein minimaler Reparaturpfad und eine Offenlegungsentscheidung. Ohne das schafft schnellere Entdeckung nur eine größere Warteschlange der Unsicherheit.

[ALLOY]: Der strategische Punkt ist, dass Konnektivität und Sicherheit jetzt zusammen beschleunigen. Je leichter es wird, Tool-Oberflächen zu bauen, desto leichter wird es für Agenten zu handeln. Je stärker die Modelle bei Schwachstellenentdeckung werden, desto mehr brauchen diese Tool-Oberflächen enge Berechtigungen und Auditierbarkeit. Stainless und Glasswing sind zwei Seiten desselben Agent-Infrastrukturbaus.

[ALLOY]: Die erste GitHub-Projektgruppe gibt Coding-Agenten bessere Augen. Die Namen sind Serena, Claude Context, Sourcebot, Understand-Anything, Chunkhound und Code Review Graph.

[NOVA]: Serena ist hier das direkteste MCP-geschmackte Upgrade. Es gibt Coding-Agenten semantische Retrieval-, Editing-, Refactoring- und Debugging-Tools, die sich mehr wie IDE-Fähigkeiten verhalten. Das wichtige Feature ist Symbol-Level-Arbeit: Definitionen, Referenzen, Beziehungen und Refactor-Pfade statt nur Text-Matches.

[ALLOY]: Das ist wichtig, weil Grep kein Code-Verständnis ist. Es ist eine schnelle Taschenlampe. Ein Coding-Agent muss wissen, wo ein Symbol definiert ist, wo es verwendet wird, wovon es abhängt und welche Tests den Pfad abdecken. Serena versucht, diese IDE-ähnlichen Moves hinter einer Tool-Oberfläche zu platzieren, die ein Agent nutzen kann.

[NOVA]: Claude Context ist ein semantisches Code-Such-MCP für Claude Code und andere Agenten. Seine Aufgabe ist es, große Repos bedeutungsvoll durchsuchbar zu machen, ohne gigantische Verzeichnisse in den Prompt zu stopfen. Das ist nützlich, wenn der Code-Name nicht zur menschlichen Beschreibung passt, oder wenn die relevante Logik über Dateien verstreut ist.

[ALLOY]: Sourcebot ist die selbst gehostete Code-Such- und Verständnis-Oberfläche. Es bietet Repo-Suche, Navigation, Datei-Exploration und Ask Sourcebot Q&A mit Zitaten. Der selbst gehostete Teil ist wichtig, weil Code-Intelligenz oft private Repositories berührt. Eine geteilte, zitierte Suchoberfläche kann Menschen und Agenten helfen, vom gleichen Beweis statt von Vibes aus zu argumentieren.

[NOVA]: Understand-Anything verwandelt Codebasen in interaktive Wissensgraphen mit Suche und Q&A, und positioniert sich explizit für Claude Code, Codex, Cursor, Copilot, Gemini CLI und verwandte Tools. Ein Graph ist nicht magisch, aber er kann die Architektur-Form zeigen, bevor ein Agent anfängt, ein System zu bearbeiten, das es kaum versteht.

[ALLOY]: Chunkhound und Code Review Graph drücken den local-first und persistent-map Winkel. Das ist die richtige Kategorie für Teams, die semantischen oder Graph-Kontext wollen, ohne das ganze Repo woanders hinzuschicken. Eine persistente Code-Map kann Kontext-Verschwendung reduzieren, indem sie dem Agenten die wenigen Beziehungen füttert, die wichtig sind, statt eines gigantischen Transcript-Dumps.

[NOVA]: Die Empfehlung für diese Gruppe ist, basierend darauf zu wählen, was dem Agenten fehlt. Wenn ihm Symbole und Referenzen fehlen, schau dir Serena an. Wenn er semantische Suche innerhalb von Claude Code braucht, schau dir Claude Context an. Wenn Menschen und Agenten eine gemeinsame selbst gehostete Code-Browser brauchen, schau dir Sourcebot an. Wenn die Architektur-Form das Problem ist, ist Understand-Anything interessant. Wenn lokale Indexierung und persistente Code-Maps am meisten matter, gehören Chunkhound und Code Review Graph auf die Shortlist.

[ALLOY]: Der Grund, warum das eine News-Lane ist, nicht nur eine Tools-Liste, ist, dass Code-Kontext zu seiner eigenen Schicht im Stack wird. Größere Context-Windows helfen, aber sie ersetzen nicht die Retrieval-Qualität. Ein Modell, das eine bessere Map sieht, kann einen kleineren, akkurateren Edit machen. Das ist oft wertvoller als ihm weitere tausend irrelevante Files zu geben.

[NOVA]: Das ist der Punkt, wo Hermes, OpenClaw, Codex und Claude Code alle von gemeinsamen Tool-Oberflächen profitieren. Wenn Code-Intelligenz durch MCP, lokale Indexe oder selbst gehostete Suche verfügbar ist, kann sie unter mehreren Agenten sitzen. Der Agent ändert sich; die Repo-Map bleibt nützlich.

[ALLOY]: Die kurze Empfehlung ist: füge eine Code-Intelligenz-Schicht nur dort hinzu, wo die Repo-Größe es rechtfertigt. Ein Ein-Datei-Skript braucht keinen semantischen Graphen. Ein ausgereiftes Codebase mit verstreutem Verhalten wahrscheinlich schon. ...

[NOVA]: Serenas bester Anwendungsfall ist symbol-bewusstes Editing. Ein Refactor, der Definitionen, Referenzen und Tests kreuzt, profitiert von einem MCP-Tool, das Code-Beziehungen versteht. Claude Contexts bester Anwendungsfall ist semantisches Retrieval, wenn der Prompt Verhalten beschreibt, aber der Code andere Namen verwendet. Sourcebots bester Anwendungsfall ist eine selbst gehostete Suchoberfläche, wo Menschen und Agenten Zitate teilen können.

[ALLOY]: Understand-Anything ist stärker, wenn die Architektur-Form wichtig ist: unbekannte Services, versteckte Abhängigkeiten oder ein Repo, wo der Call-Graph mehr erklärt als Dateinamen. Chunkhound und Code Review Graph passen zum local-first Anwendungsfall, wo persistente Maps wertvoll sind, aber Code nicht einfach die Maschine oder das vertrauenswürdige Netzwerk verlassen kann.

[NOVA]: Der Build-Trend ist klar: Code-Kontext wird zu einem wiederverwendbaren Substrat. Das Agent-Fundament kann heute Claude Code sein, morgen Codex, nächste Woche Hermes und OpenClaw darum herum. Eine gute Repo-Map kann all diese Oberflächen bedienen, wenn sie durch MCP, einen lokalen Index oder eine selbst gehostete Suchschicht zugänglich gemacht wird.

[ALLOY]: Deshalb ist diese Projektlinie wichtig. Es geht nicht nur darum, ein Modell schlauer zu machen. Es geht darum, jedem Coding-Agent einen besseren Ausgangspunkt zu geben: weniger irrelevante Dateien, genauere Referenzen, klarere Architektur und einen kürzeren Weg von der Frage zum Nachweis.

[NOVA]: Die zweite Projektgruppe verändert die Stack-Ausführung. Context7, Claude Code Router, mcp-use, goose, gstack, deepsec, context-mode und ai-setup befinden sich zwischen dem Modell, dem Repo, den Tools und dem Menschen.

[ALLOY]: Context7 bearbeitet aktuelle Dokumentation. Coding-Agents scheitern oft, weil ihre Bibliothekserinnerung veraltet ist. Context7 gibt LLMs und Coding-Agents aktuelle Bibliotheksdokumente über CLI, Skills oder MCP. Es ist besonders nützlich für sich schnell bewegende JavaScript-, Python-, AI-SDK- und Framework-Aufgaben, wo alte Beispiele plausibel aussehen, aber zur Laufzeit fehlschlagen.

[NOVA]: Claude Code Router dreht sich um Provider- und Modell-Routing. Es kann Claude Code-Anfragen über OpenRouter, DeepSeek, Ollama, Gemini und andere Backends routen, mit Transformern und routenspezifischen Modellwahlen. Der Wert liegt darin, das Backend an die Arbeit anzupassen: günstige Zusammenfassungen, lokale Experimente, langkontextuelle Leser oder hoch reasoning-lastige Reviews.

[ALLOY]: Das Risiko liegt in der Verantwortlichkeit. Ein Router ist nur hilfreich, wenn die Route sichtbar genug ist, sodass der Nutzer weiß, welcher Provider und welches Modell die Aufgabe bearbeitet hat. Verborgenes Routing kann Geld sparen und gleichzeitig Verwirrung schaffen.

[NOVA]: mcp-use ist ein Framework zum Erstellen von MCP-Apps und Servern in TypeScript und Python, mit Inspektions- und Deployment-Pfaden. Das ist wichtig, weil MCP sich von einer Neuheit zu einer Integrationsebene bewegt. Teams brauchen einen schnelleren Weg, kleine Tools zu bauen, Aufrufe zu inspizieren und sie für Agents zu verpacken, ohne jeden Server von Hand zu rollen.

[ALLOY]: goose ist ein lokaler KI-Agent mit Desktop, CLI, API, Multi-Provider-Unterstützung, ACP-Pfaden und MCP-Erweiterungen. Er ist jetzt unter der Agentic AI Foundation und es lohnt sich, ihn als lokalen Agent-Fallback oder Vergleichspunkt zu beobachten. Das Interessante ist nicht, ob er alles ersetzt. Es ist, ob sein Provider- und Erweiterungsmodell einige lokale Aufgaben einfacher macht, außerhalb eines schwereren Stacks zu laufen.

[NOVA]: gstack packt Claude Code-Rollen und Workflows für Review, QA, Release, Sicherheit, Planung und Produktarbeit. Rollenpakete können zum Theater werden, wenn sie nur gewöhnliche Prompts umbenennen, aber sie sind nützlich, wenn sie wiederholbares Review-Verhalten, erwartete Nachweise und konsistente Output-Formen kodieren.

[ALLOY]: deepsec ist der Sicherheitsscanner in dieser Spur. Es nutzt Coding-Agents für Vulnerability Scanning über große Codebasen hinweg, mit fortsetzbaren Scans, Matchern, Verarbeitung, Revalidierung und Export. Das versetzt es in dieselbe Welt wie Glasswing, aber als GitHub-gehostetes Tool, das Builder inspizieren und in begrenzten Umgebungen ausführen können.

[NOVA]: context-mode und ai-setup zielen auf zwei alltägliche Probleme: Output-Rauschen und Setup-Drift. Sobald ein Stack Claude Code, Codex, OpenCode, Gemini CLI, Hermes, OpenClaw, lokale Modelle, MCP-Server und Router umfasst, kann Konfiguration zum versteckten Fehlermodus werden. Tools, die Kontext eng halten und Setup konsistent machen, können nützlicher sein als ein weiterer Modell-Auswähler.

[ALLOY]: Die Empfehlung für diese Gruppe ist ebenfalls aufgabenbasiert. Nutze Context7, wenn aktuelle Docs das fehlende Puzzlestück sind. Nutze Claude Code Router, wenn die Provider-Wahl wirklich wichtig ist. Nutze mcp-use, wenn eine private Fähigkeit ein MCP-Tool werden sollte. Nutze goose, wenn ein lokaler Agent mit Erweiterungen der richtige Vergleich ist. Nutze gstack, wenn wiederholbare Review-Rollen wichtig sind. Nutze deepsec nur, wenn Sicherheitsbefunde verifiziert und bearbeitet werden können.

[NOVA]: Der größere Trend ist, dass der Agent-Stack sich in der Mitte füllt. Wir haben bereits Modelle und Chat-Oberflächen. Die neue Aktivität findet in Routern, Docs-Retrieval, MCP-Builds, lokalen Agent-Shells, Rollenpaketen, Code-Maps und Scannern statt. Das ist dort, wo Agentenarbeit kontrollierbarer wird.

[ALLOY]: Es macht auch Disziplin wichtiger. Jedes extra Tool fügt Autorität, Konfiguration oder eine weitere Stelle hinzu, wo Nachweise verschwinden können. Ein gutes Projekt verdient seinen Platz, indem es die Aufgabe klarer macht: bessere Docs, besserer Code-Kontext, klareres Provider-Routing, engerer Tool-Zugang oder verifizierbarere Sicherheitsbefunde. ...

[NOVA]: Context7s Kernanwendungsfall sind sich schnell bewegende Bibliotheken. Wenn sich ein Framework, AI SDK oder Datenbankclient schnell ändert, erzeugt veraltetes Modell-Gedächtnis Code, der richtig aussieht und zur Laufzeit fehlschlägt. Aktuelle Docs im Agent-Loop sind ein einfacher Weg, den Build zu verbessern, ohne Modelle zu ändern.

[ALLOY]: Claude Code Routers Anwendungsfall ist Workload-Trennung. Ein günstiges Modell kann Logs zusammenfassen. Ein lokales Modell kann private Hintergrundlektüre bearbeiten. Ein stärkeres Modell kann einen riskanten Patch reviewen. Der Router ist nützlich, wenn diese Wahlen explizit sind; er ist gefährlich, wenn Routing unsichtbar wird.

[NOVA]: mcp-use ist das Build-Tool in dieser Gruppe. Es senkt die Kosten dafür, eine kleine Fähigkeit in einen MCP-Server oder eine App zu verwandeln, besonders in TypeScript und Python. Der erste gute Anwendungsfall ist normalerweise schreibgeschützt: Status-Lookup, Dokumentationssuche, Inventarabfrage oder ein schmaler interner Report. Sobald die Form verständlich ist, können Schreibaktionen als separate Berechtigung behandelt werden.

[ALLOY]: goose ist der lokale Agent-Anwendungsfall. Es gibt Buildern eine weitere Desktop-, CLI- und API-Oberfläche mit Provider- und MCP-Erweiterungsunterstützung. gstack ist der wiederholbare Rollen-Anwendungsfall: Review-, QA-, Release-, Planungs- und Sicherheitsprompts, die konsistent genug sind, um beurteilt zu werden. deepsec ist der Sicherheits-Anwendungsfall, mit fortsetzbaren Scans und exportierten Befunden. context-mode und ai-setup sind der Konsistenz-Anwendungsfall, der verhindert, dass Output und Konfiguration sich ausbreiten, während der Stack wächst.

[NOVA]: Das nützliche Muster über all das hinweg ist nicht Prozedur um ihrer selbst willen. Es ist das Tool zu wählen, das das Ergebnis verändert: weniger veraltete APIs, klarere Provider-Wahl, eine engere MCP-Oberfläche, einen lokalen Agent, der ohne den schweren Stack laufen kann, eine Review-Rolle, die konkrete Bugs findet, oder einen Scanner, der Nachweise statt Rauschen produziert.

[ALLOY]: Es gibt noch einen Stack-Ebene-Punkt in dieser Projektlinie. Diese Tools konkurrieren nicht nur um Modellqualität. Sie konkurrieren um Kontextqualität, Routing-Klarheit, Interface-Form und Nachweise. Context7 verbessert die Dokumentationseingabe. Serena und Sourcebot verbessern die Code-Eingabe. Claude Code Router verändert den Modellpfad. mcp-use verändert das Tool-Interface. goose verändert die lokale Ausführungshülle. deepsec verändert die Sicherheitslinse. Das sind verschiedene Schichten, und sie zu vermischen macht den Stack schwerer zu durchschauen.

[NOVA]: Der beste Anwendungsfall für diesen gesamten Bereich ist ein Builder, der bereits über ein leistungsfähiges Modell verfügt, aber immer noch mittelmäßige Ergebnisse erzielt, weil das umgebende System schwach ist. Der Agent liest veraltete Docs. Er findet nicht die richtige Datei. Er nutzt das teure Modell für eine billige Zusammenfassung. Er kann das interne System nicht sauber aufrufen. Er erstellt eine Sicherheitsaussage ohne Beweise. Die Projekte in diesem Bereich bekämpfen diese Fehlermodi direkt.

[ALLOY]: Deshalb ist dies interessanter als ein Sternchen-Zusammenschnitt. Ein Repo verdient Aufmerksamkeit, wenn es eine der schwierigen Oberflächen rund um die Agentenarbeit verändert: was das Modell weiß, welches Modell antwortet, welche Tools aufrufbar sind, wo die Ausführung stattfindet, wie Code abgebildet wird, oder wie Ergebnisse verifiziert werden. Das ist ein konkreter Stack-Upgrade, keine neue Auszeichnung für die README.

[NOVA]: Die stärksten Builds werden diese Schichten sorgfältig kombinieren. Aktuelle Docs für schnelle Bibliotheken. Semantische Code-Maps für große Repos. Sichtbares Routing für Anbieterwahl. Kleine MCP-Server für private Fähigkeiten. Lokale Agents für sensible Ausführung. Sicherheitsscanner, wo die Beweise verarbeitet werden können. Der Wert liegt nicht darin, jedes Tool installiert zu haben. Der Wert liegt darin zu wissen, welche Schicht schwach ist und nur das Teil hinzuzufügen, das sie stärkt.

[NOVA]: Das Stack-Update von EP057 ist straightforward. OpenClaw v2026.5.22 macht das Gateway, die Plugin-Schicht, die Meeting-Notes-Qellen, das Provider-Fallback-Verhalten, die Session-Navigation und die Discord-Steuerung solider. Claude Code verbessert die Nutzungssichtbarkeit, die Diff-Überprüfung, die Task-List-Darstellung, die Richtlinie für den verwalteten Cloud-MCP-Connector und mehrere Shell- und Sandbox-Sicherheitsaspekte. Der folgende Patch ist intern.

[ALLOY]: Googles Gemini-Nachrichten besagen, dass verwaltete Agent-Umgebungen jetzt eine Produktoberfläche sind: Remote-Linux-Ausführung, Tools, Browsing, Dateien, Session-Fortsetzung und benutzerdefinierte Agent-Anweisungsdateien. OpenAIs Codex-Nachrichten besagen, dass Coding-Agent-Arbeit remote, mobil-überwacht, token-bereichsbezogen, hook-gesteuert und enterprise-bereitstellbar wird.

[NOVA]: Anthropics Stainless-Übernahme besagt, dass SDKs, CLIs und MCP-Server zur Kern-Agent-Infrastruktur werden. Project Glasswing besagt, dass Frontier-Modelle schnell genug Schwachstellen finden können, dass Verifizierung und Offenlegung zum Engpass werden.

[ALLOY]: Das GitHub-Projektradar besagt, dass die nützlichen Stack-Upgrades nicht alle Modelle sind. Serena, Claude Context, Sourcebot, Understand-Anything, Chunkhound und Code Review Graph verbessern, was Agents über Code verstehen können. Context7, Claude Code Router, mcp-use, goose, gstack, deepsec, context-mode und ai-setup verbessern Docs, Routing, MCP-Tooling, lokale Ausführung, wiederholbare Rollen, Sicherheits-Scanning und Setup-Konsistenz.

[NOVA]: Die kurze Empfehlung ist, die Kern-Tools zu aktualisieren und dann nur die Projekte hinzuzufügen, die ein sichtbares Problem lösen. Bessere Code-Maps für große Repos. Aktuelle Docs für schnelllebige Bibliotheken. Modell-Routing, wo Anbieterwahl wichtig ist. MCP-Builder für bereichsbezogene Tools. Sicherheitsscanner, wo ein echter Verifizierungspfad besteht.

[ALLOY]: Das ist die nützliche Version von Agent-News: kein Haufen Namen und kein Prozess um seiner selbst willen. Konkrete Releases, konkrete Fähigkeiten und ein klareres Bild, wohin der Stack sich entwickelt.

[NOVA]: Vollständige Notizen und Quellen-Links sind in den Episodennotizen bei Toby On Fitness Tech dot com.

[ALLOY]: Danke fürs Zuhören zu AgentStack Daily. Wir sind bald zurück.