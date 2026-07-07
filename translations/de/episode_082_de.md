[NOVA]: Ich bin NOVA.

[ALLOY]: Ich bin ALLOY, und das ist AgentStack Daily...

[NOVA]: Claude Code .195 wurde als stabile Wartungsversion von Anthropics terminalbasiertem KI-Programmierassistenten veröffentlicht, mit MCP-Tool-Servern, Projekt-Root-Anweisungen, fortsetzbaren Sitzungen und Plattformkompatibilität ohne veröffentlichtes Änderungsprotokoll. Ollama .31 folgt später mit schnellerer Gemma 4-Generierung auf Apple Silicon durch Multi-Token-Prediction.

[ALLOY]: Heute: Claude Code .195, Tencent Hy3 auf OpenRouter, Nex-N2-Mini, GLM 5.2 Margindruck, Anthropics Global Workspace Theory-Paper, ein Browser-seitiges Embedding-Modell, durchgesickerte Agent-Systemprompts, Ollama .31, und neue Forschung zu Planung, Distillation, Robotersteuerung und Coding-Agent-Stil-Empfindlichkeit.

[NOVA]: Die Modell-Routing-Fläche wurde erweitert. Ten, Tencent's Hy3 bringt ein Mixture-of-Experts-Design mit 295 Milliarden Parametern, 21 Milliarden aktiven Parametern, Top-8-Routing über 192 Experten, ein 262K-Kontextfenster und konfigurierbaren Reasoning-Aufwand. Nex AGIs Nex-N2-Mini fügt ein Open-Weight-MoE mit demselben langen Kontextfenster plus Text- und Bildeingabe hinzu, ausgerichtet auf Coding und Tool-Nutzung.

[ALLOY]: Der praktische Stack wird auch schärfer: Ternlight führt Embeddings durch WASM im Browser aus, Codebase-Speicher wandert in MCP, FastMCP hält Python-Services einfach als Tools bereit, und Microsoft bringt MCP in Mainstream-Runtimes bei.

[NOVA]: ...

[NOVA]: Claude Code .195 wurde am sechsundzwanzigsten Juni als neue stabile Version von Anthropics terminalbasiertem KI-Programmierassistenten veröffentlicht. Die Version wurde ohne öffentlichen Änderungsprotokoll-Body veröffentlicht, was zur Zwei-Punkt-Eins-Wartungs-Taktung passt: kleine Patches, die das Harness mit dem upstream Claude-Modellverhalten, Plattformänderungen, Dependency-Refreshes und Tool-Nutzungsoberflächen abstimmen, auf die Entwickler bereits angewiesen sind. Die aktuelle getestete Version behält denselben Kernvertrag bei: Terminal-Bearbeitung, Shell-Ausführung, Suche, MCP-Server, Projektkontext und fortsetzbare Sitzungen bleiben auf derselben Linie.

[ALLOY]: Zwei Oberflächen sind im Arbeitsalltag am wichtigsten. Erstens: Claude Code expose Model Context Protocol-Server als Tool-Quellen, die der Agent während einer Sitzung aufrufen kann. Ein Team kann einen Postgres-Schema-Reader, Issue-Tracker, interne API oder einen benutzerdefinierten Analyseservice in die Agent-Schleife einbinden, ohne jeden Aufruf in individuelle Kleinarbeit zu verwandeln. Zweitens: Claude Code liest eine CLAUDE.dot.MD-Anweisungsoberfläche im Projekt-Root, wodurch Teams repo-spezifische Regeln in den Systemprompt injizieren können: Coding-Konventionen, Migrationsguardrails, Test-Erwartungen, bevorzugte Package Manager und Bereiche, die der Agent vermeiden sollte.

[NOVA]: Da .195 ein ruhiger Wartungsbuild ist, lautet das Fazit Stabilität statt Migration. Bestehende Setups auf der Zwei-Punkt-Eins-Linie können dieselbe MCP-Konfiguration und dasselbe Projektkontextverhalten weiter nutzen, während sie die Kompatibilitätsarbeit erhalten, die Anthropic in den Build gefaltet hat. Das ist wichtig für CI-Jobs und Entwicklermaschinen, wo der Coding-Agent Teil eines reproduzierbaren Workflows ist, kein gelegentliches Chatfenster.

[ALLOY]: Die Version erscheint auch, während Claude Codes Workspace-Isolationsgeschichte unter Beschuss steht, also klärt der Wartungs-Bump nicht jede Vertrauensfrage. Er hält die ausgelieferte Agent-Oberfläche aktuell, während Entwickler auf klarere Antworten zur Cache-Partitionierung und zum Sitzungs-Fortsetzungsverhalten warten.

[NOVA]: ...

[NOVA]: Ten, Tencent's Hy3 Reasoning-Modell ist jetzt auf OpenRouter gelistet, und die wichtige Zahl ist nicht nur 295 Milliarden Parameter. Hy3 ist ein Sparse Mixture-of-Experts-Modell mit 192 Experten und Top-8-Routing, sodass jeder Token 21 Milliarden Parameter aktiviert anstatt das ganze Modell. Das versetzt es in die kostenbewusste MoE-Familie, wo Gesamtkapazität und Per-Token-Compute absichtlich entkoppelt sind. Für Agent-Backends ist dieser Active-Parameter-Footprint wichtiger als die Schlagzeile, weil Orchestratoren oft viele Subtasks ausschicken und sich um vorhersehbare Latenz und Ausgaben pro Aufruf kümmern.

[ALLOY]: Hy3 bietet auch konfigurierbaren Reasoning-Aufwand. Aufrufer können Latenz gegen tieferes Reasoning zur Inferenzzeit tauschen, höhere Aufwandsstufen für Planung, Tool-Auswahl und schwierige Coding-Aufgaben verwenden, während einfache Lookups auf günstigeren Einstellungen bleiben. Die zweite konkrete Oberfläche ist die Kontextlänge. Bei 262K Tokens kann Hy3 lange Agent-Traces, große Repository-Slices, akkumulierte Tool-Ausgaben oder erweiterten Migrationskontext halten, ohne Retrieval in jeden Turn zu erzwingen.

[NOVA]: Die OpenRouter-Distribution macht Hy3 einfach in Agent-Schleifen zu integrieren, die bereits die Chat-Completion-Form des Platforms sprechen. Das senkt die Integrationskosten, aber macht Hy3 nicht zu einem automatischen Ersatz für einen Standard-Reasoning-Provider. Tool-Nutzungs-Zuverlässigkeit, JSON-Disziplin, Latenz unter hohem Aufwand und Verhalten über lange Sitzungen brauchen noch echte Workload-Evidenz.

[ALLOY]: Der kurzfristige Anwendungsfall ist A/B-Routing. Platziere Hy3 neben aktuellen Reasoning-Standards auf schwierigen Tool-Nutzungs-Traces: Multi-Step-Debugging, Long-Context-Refactors, Planner-Executor-Schleifen und Recovery von fehlgeschlagenen Tool-Aufrufen. Wenn das 21-Milliarden-aktive Design starkes Reasoning ohne Frontier-Preis liefert, wird Hy3 ein weiterer ernstzunehmender Fallback-Tier für Multi-Provider-Stacks.

[NOVA]: ...

[NOVA]: Nex AGI hat Nex-N2-Mini auf OpenRouter gelistet als kleineres Geschwistermodell in seiner Nex-N2-Linie. Das Modell ist Open-Weight, Mixture-of-Experts und positioniert für Coding und Tool-Nutzung statt für allgemeinen Chat. Diese Positionierung ist wichtig, weil Coding-Agents mehr als flüssige Antworten brauchen. Sie brauchen strukturierten Output, Tool-Call-Disziplin, Repository-Navigation, Multi-Turn-State-Handling und vernünftiges Verhalten, wenn die Aufgabe von Erklärung zu Edit-Planung wechselt.

[ALLOY]: Das Modell bewirbt ein 262.144-Token-Kontextfenster und native Text-plus-Bild-Eingabe. In der Praxis gibt diese Kombination Agent-Schleifen eine größere Arbeitsfläche als die meisten kleineren Open-Weight-MoE-Optionen. Ein Migrationsagent kann einen großen Codebase-Slice, generierte Pläne, Fehlerprotokolle, API-Notizen und frühere Entscheidungen in einer Sitzung halten. Der Bildpfad bedeutet, dass UI-Screenshots, Design-Referenzen, Diagramme oder visuelle Bug-Reports neben dem Codekontext stehen können, ohne einen separaten Vision-Preprocessing-Schritt.

[NOVA]: OpenRouter gibt Nex-N2-Mini einen vertrauten Integrationspfad. Bestehende Router, die bereits OpenRouter-gehostete Modelle aufrufen, können es über dieselbe Request-Shape hinzufügen, anstatt einen benutzerdefinierten Client zu bauen. Das macht es einfach, es gegen aktuelle Defaults zu evaluieren: Sende dieselben Coding-Agent-Sitzungen durch Nex-N2-Mini, vergleiche Tool-Call-Korrektheit, Patch-Qualität, Latenz und Long-Context-Retention, und entscheide dann, ob es einen Slot im Router verdient.

[ALLOY]: Der Open-Weight-Status gibt einen zweiten Grund, das Ganze im Auge zu behalten. Teams, die mehr inspizierbares Modellverhalten, lokale Adaptionsmöglichkeiten oder Anbieterflexibilität wollen, bekommen einen neuen Kandidaten in der agentic-mini-Kategorie. Der fehlende Beweis ist Community-Benchmarking unter realer Tool-Ausführung. MoE-Modelle können in isolierten Prompts stark aussehen und trotzdem wackeln, wenn Schemas, Retries und lange Agent-Traces ins Spiel kommen. Wenn sich Nex-N2-Mini dort bewährt, bekommen langkontextuelle, multimodale Coding-Agents ein neues praktisches Backend.

[NOVA]: ...

[NOVA]: Martin Aldersons Juli-Artikel über GLM 5.2 argumentiert, dass Frontier-Tier-Fähigkeiten sich zu einem Commodity-Input entwickeln. Der Beitrag nutzt Zhipus GLM 5.2 als Fallstudie für Preisdruck: Wenn Near-Frontier-Modelle zu niedrigeren Preisen nützliche Schwellenwerte erreichen, wird die pro-Token-Marge, die den nächsten Trainingszyklus finanziert, unter Druck gesetzt. Das Argument ist wirtschaftlich statt benchmark-getrieben. Sobald ein Modell die Messlatte für mehrstufige Tool-Nutzung, Long-Context-Retrieval, Coding-Assistenz und Planung überspringt, geben viele Anwendungen keine hohen Prämien mehr für das absolut beste Modell bei jedem Durchgang aus.

[ALLOY]: Wenn ein kostengünstigeres Modell den Großteil der Agentenarbeit gut genug erledigt, kann der Router Premium-Modelle nur für die schwierigsten Schritte reservieren. Das verändert die Einnahmenstruktur für Anbieter. Aktuelle Inferenzgenerationen können die nächste Trainingsgeneration nicht mehr in demselben Umfang subventionieren, wenn Kunden abwandern, sobald Near-Frontier-Qualität günstig wird. Alderson beschreibt es als eine umgekehrte Jevons-Dynamik: Fähigkeiten werden billiger und weiter verbreitet, während der Kapitalstack darunter dünner wird.

[NOVA]: Builder spüren das durch Produktdifferenzierung. "Powered by a frontier model" wird schwächer als Burggraben, wenn GLM 5.2-Klasse-Modelle, MoEs aus chinesischen Labs und Open-Weight-Systemme den Boden anheben. Dauerhafter Vorteil verlagert sich hin zu privatem Kontext, Evaluations-Harnesses, Routing-Logik, Workflow-Design und Daten-Feedback-Loops. Das Modell wird zu einer ersetzbaren Schicht in einem größeren System statt zur ganzen Produktgeschichte.

[ALLOY]: Die Hacker-News-Diskussion überschritt 400 Punkte, weil Operatoren und Builder den gleichen Beitrag unterschiedlich lasen. Operatoren sahen Margenkompression. Builder sahen günstigere Fähigkeiten. Beides kann stimmen. Achten Sie auf Preissenkungen, gebündelte Provider-Failover und mehr Agent-Plattformen, die Modellwahl als dynamische Routing-Entscheidung statt als permanente Vendor-Wette behandeln.

[NOVA]: ...

[NOVA]: Anthropic hat "A global workspace in language models" veröffentlicht und bringt damit die Global-Workspace-Theorie aus der kognitiven Neurowissenschaft in die Transformer-Interpretability. Das Paper behandelt ein Sprachmodell als Sammlung spezialisierter Rechenmodule, die durch einen gemeinsamen Broadcast-Kanal koordinieren. Anstatt anzunehmen, dass Informationen gleichmäßig durch jeden Residual-Stream-Aktivierung diffundieren, argumentieren die Autoren, dass eine kleine Teilmenge von High-Impact-Tokens einen großen Teil der kreuzmodularen Koordination trägt. Eingriffe in diese Workspace-Tokens sollten daher downstream-Verhalten stärker verändern als Eingriffe in gewöhnliche Tokens.

[ALLOY]: Das verwandelt eine Theorie des bewussten Zugangs in eine testbare Behauptung über Transformer-Inferenz. Wenn die Workspace-Token-Idee stimmt, bekommen Interpretability-Forscher ein konkretes Probe-Ziel. Sie können untersuchen, welche Tokens als Broadcast-Träger fungieren, sie stören, verfolgen, wie downstream-Schichten reagieren, und Effekte über Reasoning, Refusal, Code-Generierung und Summarization vergleichen. Der Wert ist kein Produkt-Feature; er ist eine messbare Oberfläche, um zu erklären, warum ein Modell einen bestimmten Sprung gemacht hat.

[NOVA]: Der Hacker-News-Thread erreichte ungewöhnlich hohe Sichtbarkeit für ein Interpretability-Paper, teilweise weil das Framing Ingenieuren verwertbare Sprache gibt. Statt zu sagen, ein Modell habe "den Kontext attendiert" auf vage Art, können Teams fragen, ob eine kleine Token-Menge den Reasoning-Pfad koordiniert hat, ob eine Halluzination von einem schlechten Workspace-Broadcast kam, oder ob Steering die richtigen Tokens verändert hat.

[ALLOY]: Die offene Frage ist Generalisierbarkeit. Anthropics Framing braucht unabhängige Reproduktion über Modellfamilien, -größen und Trainingsrezepte hinweg. Wenn Open-Weight-Modelle ähnliche Workspace-Struktur zeigen, wird die Idee mehr als eine Anthropic-spezifische Analyse. Wenn nicht, könnte sie eine Modellfamilie oder einen Interpretability-Lens beschreiben. So oder so treibt das Paper mechanistische Interpretability über isolierte Schaltkreise hinaus hin zu architektonischen Theorien, über die Entwickler nachdenken können.

[NOVA]: ...

[NOVA]: Ein GitHub-Issue im Claude Code Repository überschritt 300 Punkte auf Hacker News, nachdem Entwickler einen vermuteten Session- und Cache-Leak-Pfad zwischen Workspace-Instanzen meldeten. Die Berichte beschreiben gecachte Assistant-Turns und fortgesetzte Zustände, die unter einem anderen Workspace-Kontext erscheinen als dem, der sie ursprünglich erzeugt hat. Da Claude Code als terminalbasierter KI-Coding-Agent in echten Repositories läuft, wirft jeglicher Cross-Workspace-State-Bleed Isolationsbedenken für Mieter auf, besonders für Entwickler, die Client-Arbeit, interne Projekte und Experimente auf derselben Maschine ausführen.

[ALLOY]: Der vermutete Pfad zentriert sich auf Workspace-Routing und Cache-Key-Ableitung. Wenn gecachte Turns oder Resume-Tokens zu breit geschlüsselt werden – zum Beispiel nach lokalem Profil oder Account-Namespace ohne vollständige Workspace-Identität – könnte ein neuer Workspace vorherigen Zustand aus einer anderen Session erhalten. Das würde keine Modellhalluzination oder serverweite Verwechslung erfordern. Eine lokale Client- oder Routing-Schicht, die es versäumt, Cache-Einträge eng genug zu partitionieren, könnte das beobachtete Symptom erzeugen: Vorheriger Assistant-Content taucht dort auf, wo er nicht hingehört.

[NOVA]: Anthropic hatte zum erfassten Zeitpunkt keine technische Lösung in der öffentlichen Diskussion bestätigt. Bis sich das ändert, behandeln Entwickler, die mehrere Workspaces auf einer Maschine betreiben, fortgesetzte Sessions und Cache-Hits mit Vorsicht. Der wichtige Unterschied ist, dass dies nicht nur unordentliche UX ist. Ein gecachter Assistant-Turn kann Architekturnotizen, geheimnisnahen Kontext oder proprietäre Implementierungsdetails aus einem anderen Projekt enthalten.

[ALLOY]: Das nächste nützliche Signal ist eine konkrete Anthropic-Erklärung: ob Cache-Keys vollständige Workspace-Identität enthalten, ob Resume-Tokens auf API-Ebene Workspace-gepinnt sind, und ob lokaler Profilzustand zwischen Workspaces geteilt werden kann. Ein Patch-Hinweis oder Security-Advisory, das die Partitionierungsfix benennt, würde weit mehr Vertrauen wiederherstellen als eine generische Beruhigung.

[NOVA]: ...

[NOVA]: Ternlight hat ein etwa sieben Megabyte großes Embedding-Modell veröffentlicht, das vollständig im Browser über WebAssembly läuft. Die öffentliche Demo zog starke Hacker-News-Aufmerksamkeit auf sich, weil die Deployment-Form so einfach ist: Laden Sie ein kleines quantisiertes Embedding-Netzwerk in die Seite, führen Sie Inferenz im Client aus und geben Sie einen Fixed-Dimension-Vektor durch eine async-encode-Funktion zurück. Kein Backend-Inferenz-Service wird für den Embedding-Schritt benötigt.

[ALLOY]: Die Pipeline sieht eher nach modernem Browser-ML als nach traditionellem gehostetem KI aus. Das WASM-Modul initialisiert sich in einem Web Worker, sodass der Embedding-Pass die Hauptoberfläche nicht einfriert, während der Benutzer tippt oder scrollt. Modellgewichte streamen als statische Web-Assets und können aggressiv vom Browser und CDN gecacht werden. Das macht semantische Suche, Deduplizierung, Clustering und leichtgewichtiges Retrieval in statischen Sites und Single-Page-Apps machbar, wo das Hinzufügen eines Servers normalerweise das gesamte Deployment-Modell ändern würde.

[NOVA]: Die Privacy- und Kostenwinkel sind direkt. Benutzertext bleibt im Tab, was für Support-Nachrichten, interne Notizen, private Knowledge Bases und regulierte Workflows wichtig ist. Token-Billing verschwindet auch aus dem Embedding-Pfad; Compute verlagert sich auf lokale CPU-Zyklen auf dem Gerät des Benutzers. Das macht nicht jeden Use Case kostenlos – Ranking-Qualität, Index-Design und Memory-Management zählen immer noch – aber es verändert die Basis-Ökonomik für kleine Retrieval-Features.

[ALLOY]: Die grundlegendere Frage ist, ob Browser-seitige Inferenz sich um gemeinsame Laufzeitumgebungen wie ONNX Runtime Web, Transformers.js-artige Pipelines oder kleine benutzerdefinierte WASM-Builds standardisiert. Wenn ja, wird ein sieben Megabyte großes Embedding-Modell zu einer normalen Frontend-Abhängigkeit, nicht zu einer cleveren Demo. Erwarten Sie, dass dasselbe Muster Reranker, Klassifikatoren und lokalen, datenschutzbewussten Retrieval-Komponenten erreicht.

[NOVA]: ...

[NOVA]: Eine Entwickler-Kritik mit dem Titel "Anthropics Methode, Goodwill in wenigen einfachen Schritten zu verlieren" wurde auf Hacker News viral, erreichte 244 Punkte und zog eine große Diskussion unter Ingenieuren nach sich, die auf Anthropics Produkten aufbauen. Der Beitrag listet entwicklerbezogene Frustrationen auf: Änderungen bei Rate-Limits, abrupte Einstellungen, undurchsichtige Richtlinienänderungen und Maßnahmen, die Drittanbieter-Tools betreffen. Der nützliche Fakt ist nicht, ob jede Beschwerde perfekt ausgewogen ist. Der nützliche Fakt ist, dass viele Entwickler das Muster stark genug erkannten, um die Diskussion zur Frontpage-Konversation zu pushen.

[ALLOY]: Vendor-Vertrauen wird zur Infrastruktur, sobald eine API in einer Produktions-Agent-Schleife sitzt. Eine Anpassung des Rate-Limits kann einen Batch-Job unterbrechen. Eine Richtlinienänderung kann einen Router-Umschreiben erzwingen. Ein Einstellungszeitraum kann eine geplante Migration in eine Feuerübung verwandeln. Einschränkungen bei Drittanbieter-Tools können Workflows stranden lassen, die Teams bereits in interne Systeme verdrahtet haben. Das sind Ingenieurskosten, nicht nur Community-Stimmung.

[NOVA]: Das schneidet auch die GLM 5.2-Margendebatte und die neuen OpenRouter-Modelle an. Wenn hochqualitative Alternativen weiterhin auftauchen, ist Entwickler-Goodwill wichtiger, nicht weniger. Ein Anbieter mit dem besten Modell kann trotzdem den Standardstatus verlieren, wenn Teams entscheiden, dass operationelle Unsicherheit zu teuer ist. Multi-Modell-Routing wird dann zum theoretischen Hedge und zum Teil des Produktionsdesigns.

[ALLOY]: Die konkreten Signale, die es zu beobachten gilt, sind Anthropics nächste Schritte in Richtung Transparenz: klarere Einstellungszeitpläne, stabilere Rate-Limit-Oberflächen, stärkere Drittanbieter-Tooling-Haltung und einfache Erklärungen, wenn sich Zugriffsregeln ändern. Wenn sich diese verbessern, kann sich Goodwill erholen. Wenn nicht, werden Agent-Entwickler Anthropic weiterhin als einen leistungsstarken Backend unter mehreren behandeln, anstatt als die einzige Plattform, von der ihre Workflows annehmen, dass sie stabil bleibt.

[NOVA]: ...

[NOVA]: Ein neues arXiv-Paper von Idan Lev-Yehudi und Vadim Indelman schlägt Graph Sparse Sampling für Online-Planung in kontinuierlichen Markov-Entscheidungsprozessen vor. Das Ziel ist der Fluch des Horizonts. Baumsuchmethoden, einschließlich Monte Carlo Tree Search, funktionieren gut, wenn die Verzweigungsfläche verwaltet werden kann. In kontinuierlichen Zustands- oder Aktionsräumen ist die Verzweigung effektiv unendlich, und das für tieferes Lookahead benötigte Sample-Budget kann exponentiell wachsen. Das ist die Wand, auf die viele Planer stoßen, wenn sie von Spielzeugdomänen zu Robotik, kontinuierlicher Steuerung oder Langzeit-Agent-Schleifen übergehen.

[ALLOY]: Graph Sparse Sampling ändert, wie Rollouts geteilt werden. Anstatt jeden Baumknoten als isoliertes Sampling-Problem zu behandeln, teilt der Algorithmus abgetastete Zukünfte über verwandte Knoten unter Verwendung der Graph-Topologie. Benachbarte Zustände oder Geschwisterzweige enthalten oft überlappende Informationen, sodass das Ausgeben eines frischen Rollout-Budgets an jedem Knoten Rechenleistung verschwendet. Indem die Allokation an einen Graphen statt an einen reinen Baum gebunden wird, versucht GSS, nützliches Lookahead zu bewahren und gleichzeitig die schlimmste Sampling-Explosion zu vermeiden.

[NOVA]: Die Agent-Verbindung ist breiter als Robotik. Viele Software-Agenten approximieren bereits Planung durch diskrete Schritte: Wähle ein Tool, beobachte Ausgabe, wähle ein anderes Tool. Aber das Bewerten von Tool-Pfaden, die Planung von Aktionen, Budget-Allokation und interaktive Umgebungen können alle zu kontinuierlichen oder nahezu kontinuierlichen Problemen werden, sobald Unsicherheit und lange Horizonte in die Schleife eintreten. Ein Planer, der tieferes Lookahead mit demselben Sample-Budget handhabbar macht, könnte verbessern, wie Agenten zwischen konkurrierenden Aktionssequenzen wählen.

[ALLOY]: Der nächste Wert des Papers wird aus Implementierungsdetails und Benchmark-Vergleichen kommen. Sparse-Partikel-Filter-Bäume und progressive Verbreiterung sind die offensichtlichen Baselines. Gelernte Wertfunktionen sind der offensichtliche Erweiterungspunkt. Wenn sich GSS gut mit gelernten Heuristiken zusammensetzt, könnte es zu einer inneren Planungsprimitive für Roboter und Agent-Laufzeiten werden, die derzeit die Suche früh abbrechen, weil Sampling zu teuer wird.

[NOVA]: ...

[NOVA]: Das GitHub-Repo asgeirtj slash system prompts leaks ist im Trend, weil es extrahierte System-Prompts von großen KI-Coding- und Agent-Tools sammelt: Claude Code, Codex, Gemini-Varianten, Antigravity, Cursor, Copilot, Perplexity, Grok, ChatGPT-Varianten und andere Modell-Snapshots. Das Archiv präsentiert diese Prompts als einfaches Markdown, getaggt nach Modell oder Produkt-Snapshot, und aktualisiert, wenn neue Leaks erscheinen. Für Entwickler macht es das zu einem öffentlichen Fenster in Verhaltensverträge, die Anbieter normalerweise versteckt halten.

[ALLOY]: Das nützlichste Material ist nicht die Prosa-Anweisung allein. Diese Prompts legen Tool-Schemas, Ablehnungsgrenzen, Planungssequenzen, Bearbeitungseinschränkungen und Laufzeitannahmen offen. Wenn ein Vendor-Agent das Modell anweist, Tool-Aufrufe in einer bestimmten JSON-Form auszugeben, kann der geleakte Prompt den Vertrag offenbaren, den Ihr eigenes MCP-Server, Proxy oder Router möglicherweise erfüllen muss. Wenn ein Modell ändert, wie es destruktive Bearbeitungen oder sicherheitskritische Anfragen handhabt, können Snapshot-Vergleiche Prompt-Drift zeigen, bevor es als seltsames Agent-Verhalten erscheint.

[NOVA]: Das Archiv unterstützt auch den anbieterübergreifenden Vergleich. Entwickler können inspizieren, wie Claude Code, Codex, Gemini und andere Agenten Code-Bearbeitung, Planung, Suche und Tool-Aufruf rahmen. Das hilft beim Aufbau eines Routers, der dieselbe Aufgabe an mehrere Backends sendet. Sie können Ihren Orchestrator am gemeinsamen Nenner ausrichten oder Prompts pro Anbieter anpassen, um den nativen Erwartungen der Laufzeit zu entsprechen.

[ALLOY]: Die Einschränkung ist Frische und Herkunft. Geleakte Prompts können hinter Produktionsänderungen zurückbleiben, und Anbieter können Systemnachrichten ohne öffentliche Ankündigung ändern. Dennoch gibt das Archiv Entwicklern eine reproduzierbare Baseline für Eval-Fixtures, Red-Team-Szenarien und Kompatibilitätsprüfungen. Es ist kein offizieller Vertrag, aber in einem Markt, wo offizielle Verträge oft unvollständig sind, ist es einer der wenigen Orte, wo Entwickler Agent-Laufzeiten nebeneinander vergleichen können.

[NOVA]: ...

[NOVA]: Ein neues arXiv-Paper von Shiyuan Feng, Huan-ang Gao und Haohan Chi untersucht schwach-zu-stark Generalisierung durch direkte On-Policy-Destillation. Das Ziel ist Reinforcement Learning mit verifizierbaren Belohnungen, ein häufiges Post-Training-Rezept für Reasoning-Modelle. RLVR kann Mathe, Code und strukturiertes Reasoning verbessern, aber es wird teuer, wenn das starke Zielmodell große Volumina an Rollouts während des Trainings generieren muss. Je größer das Modell, desto kostspieliger wird jeder Explorationsschritt.

[ALLOY]: Das Paper fragt, ob ein kleineres RL-trainiertes Teacher diese Kosten reduzieren kann. Der vorgeschlagene Ablauf ist, RL dort auszuführen, wo Rollouts billiger sind, auf einem schwächeren Modell, und dann das resultierende On-Policy-Verhalten in einen stärkeren Studenten zu destillieren. Das rahmt schwache Modelle als Rollout-Infrastruktur um. Sie sind nicht die finale Fähigkeitsdecke; sie sind eine günstigere Art zu explorieren, Policy-Verhalten zu sammeln und nützliche Reasoning-Muster in ein größeres Modell zu übertragen.

[NOVA]: Die wichtige Erkenntnis ist kein sauberer Sieg. Die Autoren berichten, dass direktes Destillieren des post-RL schwachen Teachers unzureichend ist, weil die Policy des Teachers zwei Dinge vermischt enthält: echte RL-Verbesserungen und die Einschränkungen des schwachen Basismodells. Naive Destillation überträgt beides. Ein kleines Modell, das besseres Reasoning gelernt hat, trägt trotzdem seine eigene Decke, und ein starker Student kann diese Decke erben, wenn das Trainingsrezept nicht nützliche Strategie von schwacher Fähigkeit trennt.

[ALLOY]: Für Post-Training-Teams deutet das auf mehrstufige Pipelines hin: RL mit kleinem Modell für erschwingliche Exploration, Filterung oder Korrektur, um die Limitierungen schwacher Modelle nicht zu übertragen, dann Destillation in das Produktionsziel. Wenn die Lücke geschlossen werden kann, verschieben sich die Trainingsbudgets für Reasoning-Modelle weg von den Kosten für vollständige Rollouts. Wenn nicht, bleibt schwach-zu-stark Destillation nützlich, aber begrenzt durch die Lehrqualität.

[NOVA]: ...

[NOVA]: Cortex, ein neuer arXiv-Artikel von Jiaqi Peng, Xiqian Yu und Delin Feng, behandelt das Langzeithorizont-Problem in der Roboter-Manipulation. Aktuelle Vision-Language-Action-Policies können oft einzelne Fähigkeiten ausführen, aber sie kämpfen, wenn eine Aufgabe viele Schritte umspannt. Der Artikel argumentiert, dass Markovsche Policies, die meist auf die aktuelle Beobachtung reagieren, versagen, wenn der Roboter Intent über Subtasks hinweg bewahren muss. Ein System kann eine Tasse aufheben, aber trotzdem beim Beladen eines Geschirrspülers scheitern, weil der lange Plan und die low-level Bewegungen schlecht aufeinander abgestimmt sind.

[ALLOY]: Cortex führt eine bidirektional abgestimmte Planungsschnittstelle zwischen einem High-level-VLM-Planer und einem Low-level-VLA-Ausführer ein. Der Planer gibt strukturierte Subtasks über eine geteilte Repräsentation aus, die der Ausführer tatsächlich ausführen kann. Der Ausführer gibt dann kinematische Zustands- und Abschlussfeedback über dieselbe Repräsentation zurück. Das beseitigt das Double-Translation-Problem, bei dem semantische Pläne in einer Schicht leben, Gelenkraumverhalten in einer anderen, und brüchiger Klebecode versucht, sie zu überbrücken.

[NOVA]: Die Software-Agent-Analogie ist direkt. Gute Tool-Agents funktionieren, weil der Planer nicht nur "behebe den Bug" sagt; er gibt aufrufbare Schritte aus, beobachtet Tool-Ausgabe und plant neu, wenn ein Schritt fehlschlägt. Cortex bringt diesen Contract-Stil in verkörperte Systeme. Planer und Ausführer teilen eine Subtask-Schnittstelle, sodass partielle Fehler zu beobachtbaren Ereignissen werden, anstatt zu stiller Drift.

[ALLOY]: Die nächste Evidenz, die es zu beobachten gilt, ist Benchmark-Performance und die Veröffentlichung der Interface-Implementierung. Wenn Cortex starke Zahlen bei Langzeithorizont-Manipulationsaufgaben zeigt und Forschern einen wiederverwendbaren Subtask-Kontrakt gibt, könnte es ein praktisches Pattern für Roboter-Agents werden: High-level Sprachplanung oben, gelernte Motorausführung unten, und ein strukturierter Feedback-Kanal dazwischen.

[NOVA]: ...

[NOVA]: Graph-as-Policy, oder GaP, ist ein neuer arXiv-Artikel von Kaiyuan Chen, Shuangyu Xie und Letian Fu, der sich auf industrielle Robotik unter Variabilität konzentriert. Das Problem ist aus Fabriken und Lagern bekannt: Festautomatisierung funktioniert, wenn Teile in vorhersehbaren Posen und Formen ankommen, aber echte Einsätze bringen Variation. Model-free Policies sehen oft stark in kontrollierten Umgebungen aus und versagen dann, wenn Objektgeometrie, Ausrichtung oder Szenenlayout außerhalb der engen Trainingsverteilung liegen.

[ALLOY]: GaP umschließt eine Multi-Agent-Selbstlernschleife um eine Graph-konditionierte Kontrollpolicy. Der Arbeitsbereich und die Aufgabe werden als Graph mit Knoten für Objekte, Subziele und symbolische Planstruktur repräsentiert. Ein TAMP-Style Planer liefert das symbolische Gerüst, ROS bietet die Laufzeitumgebung, und die Graph-konditionierte Policy kümmert sich um die Kontrolle. Rollouts werden gegen Aufgabenerfolg bewertet, und symbolische Traces fließen zurück in den Policy-Graph, sodass das System Verhalten über variable Fälle hinweg verfeinern kann.

[NOVA]: Der Beitrag ist der Harness und nicht ein neues Foundation Model. Er erzwingt eine Trennung zwischen symbolischer Planung und erlernter Kontrolle, dann gibt er mehreren Agents eine geteilte Graph-Oberfläche, um darüber zu reasoning. Diese Trennung ist wichtig, weil reine End-to-End-Kontrolle oft keinen expliziten Ort hat, um auszudrücken, warum eine Aufgabe fehlschlug: falsches Objekt, falsche Pose, falsches Subziel oder falsche Aktion. Ein Graph gibt der Schleife einen strukturierten Ort, um Feedback anzuhängen.

[ALLOY]: Für Teams, die Agents in physikalische Systeme verdrahten, zeigt GaP, wie Patterns von Coding-Agents in die Robotik migrieren: orchestrierte Subagents, verifizierbare Pläne, Rollout-Scoring und Selbstkritik. Die nächsten nützlichen Signale sind offene Implementierungsdetails, Task-Suite-Spezifika und Head-to-Head-Vergleiche gegen diffusionsbasierte Manipulationsbaselines bei denselben variativen Automatisierungsproblemen.

[NOVA]: ...

[NOVA]: Ein neuer arXiv-Artikel fragt, ob Code-Sauberkeit die Coding-Agent-Performance verändert. Die Studie verwendet ein kontrolliertes Minimal-Pair-Design: Jede Aufgabe erscheint in zwei Versionen mit derselben Logik und demselben Task-Inhalt, während sich der Stil ändert. Die manipulierten Variablen umfassen Namenskonsistenz, toten Code, Kommentardichte, Formatierung und strukturelle Organisation. Dieses Design isoliert Stil als Variable, sodass jede Ergebnisdifferenz der Sauberkeit zugeschrieben werden kann und nicht einem anderen Bug, einer anderen API oder einer anderen Aufgabe.

[ALLOY]: Das ist wichtig, weil viele Coding-Agent-Benchmarks sauberer sind als Produktions-Codebasen. Echte Repositories akkumulieren inkonsistente Namen, veraltetes Scaffolding, partielle Abstraktionen, unkluge Kommentare und verwickelte Struktur. Ein Modell, das auf einem aufgeräumten Benchmark gut abschneidet, kann in einer unordentlichen Codebasis aus Gründen versagen, die nichts mit Kern-Reasoning-Fähigkeit zu tun haben. Minimal Pairs messen diese Lücke direkt, indem sie die Aufgabe konstant halten und nur die Präsentation ändern.

[NOVA]: Die Hacker-News-Diskussion erreichte starke Sichtbarkeit, weil Entwickler bereits vermuten, dass Stil die Agent-Zuverlässigkeit beeinflusst. Der Artikel gibt Teams eine Methode, um es zu quantifizieren. Wenn eine unordentliche Variante niedrigere Patch-Qualität, mehr Tool-Fehler oder schlechtere Testergebnisse verursacht, wird Aufräumen mehr als Geschmackssache. Es wird ein Input-Quality-Hebel für Agenten-Performance.

[ALLOY]: Der nächste Schritt ist Replikation über Modellfamilien und Agent-Harnesses hinweg. Ein einzelnes Ergebnis kann zeigen, dass der Effekt unter einem Setup existiert, aber Produktionsteams müssen wissen, ob die Sensitivität für Claude Code, Codex-Style Agents, lokale Models und OpenRouter-Backends gilt. Wenn Autoren gepaarte Task-Korpora veröffentlichen, können Evaluationsteams sie in Coding-Agent-Benchmarks verdrahten und messen, ob Styleschulden leise die Automatisierungs-Zuverlässigkeit belasten.

[NOVA]: ...

[NOVA]: DeusData's codebase-memory-mcp ist ein hochperformanter Code-Intelligence-MCP-Server, der Repositories in einen persistenten Wissensgraphen indexiert. Die Headline-Claims sind breite Sprachabdeckung, schnelle Query-Latenz und große Token-Reduktion im Vergleich zum Übergeben von Rohquellcode-Kontext an den Agenten. Statt lange Code-Scheiben in einen Prompt zu stopfen, kann der Agent den Graphen nach Symbolen, Call-Sites, Beziehungen und lokaler Struktur fragen.

[ALLOY]: Der Mechanismus passt sauber in MCP. Der Server wird zu einem Retrieval-Tool, das einem Agent-Harness exponiert wird, sodass Claude Code, Codex-Style Terminal-Agents oder OpenClaw-Sessions ihn während der Task-Ausführung aufrufen können. Ein Refactor-Agent muss nicht jeden umgebenden Source-Chunk im Kontext tragen, wenn er einen Graphen abfragen kann nach "wo wird diese Funktion aufgerufen" oder "welche Module hängen von diesem Interface ab" in dem Moment, in dem er die Antwort braucht. Längere Kontextfenster helfen, aber kompakte Graph-Antworten schlagen immer noch das Fluten des Prompts mit irrelevantem Code.

[NOVA]: ...

[NOVA]: Prefects FastMCP ist ein Pythonic Framework für den Bau von MCP-Servern und -Clients. Sein Wert liegt in der Reduzierung des Protokollaufwands. Anstatt JSON-RPC-Handler und Tool-Schemas von Grund auf selbst zu schreiben, können Entwickler Python-Funktionen als agentenaufrufbare Tools mit weniger Boilerplate-Code bereitstellen. Das ist wichtig, weil MCP-Adoption nur wächst, wenn interne Dienste leicht zu umhüllen sind.

[ALLOY]: Der praktische Mechanismus ist einfach: Nimm eine bereits existierende Python-Fähigkeit – eine Datenbankabfrage, internen API-Aufruf, Berichtsfunktion, Transformations-Pipeline oder Deployment-Helfer – und präsentiere sie als MCP-Tool. Sobald es registriert ist, kann ein Agent es durch dieselbe Tool-Schleife aufrufen, die er für Such-, Shell- oder Editor-Aktionen verwendet. Der Dienst bleibt in Python, während der Agent eine typisierte Fähigkeit sieht. So werden Agent-Workflows operational statt konversationell.

[NOVA]: ...

[NOVA]: Microsofts mcp-for-beginners Projekt ist ein offenes Curriculum für Model Context Protocol Grundlagen in .NET, Java, TypeScript, JavaScript, Rust und Python. Der wichtige Teil ist die sprachübergreifende Oberfläche. Viele Agenten-Teams beginnen MCP-Arbeit in Python und müssen dann Tools exponieren, die in Java-Diensten, Rust-Systemen oder TypeScript-Backends leben.

[ALLOY]: Das Projekt zeigt denselben Kernvertrag über alle Runtimes hinweg: wie ein Server Tools bewirbt, wie Schemas Inputs beschreiben, wie Clients Fähigkeiten entdecken und wie Agenten-Aufrufe in Implementierungscode fließen. Für die Integration fungiert es als Pattern-Bibliothek. Wenn ein interner Dienst außerhalb von Python lebt, können Entwickler das nächstgelegene Beispiel spiegeln und die Tool-Semantik für Claude Code, Hermes-Style Agents, OpenClaw, Codex-Style Terminal Agents und jede andere Harness, die MCP spricht, aligniert halten.

[NOVA]: ...

[NOVA]: Model Discovery hat Tencent Hy3 ausgewählt. Es ist neu gelistet auf OpenRouter mit API-Verfügbarkeit, einem 262K Kontextfenster, einer 295-Milliarden-Parameter MoE-Architektur, 21 Milliarden aktiven Parametern, 192 Experten, Top-8-Routing und konfigurierbarem Reasoning-Aufwand. Der Integrationswinkel ist straightforward: Leite eine Coding-Agent-Session durch Hy3 und vergleiche sie mit aktuellen Reasoning-Standards bei Long-Context-Tool-Use-Traces.

[ALLOY]: Model Discovery hat auch Nex AGIs Nex-N2-Mini ausgewählt. Es ist neu gelistet auf OpenRouter als Open-Weight, agentic Mixture-of-Experts Modell mit 262K Kontext und Text-plus-Bild-Eingabe. Der Winkel ist Coding und Tool-Nutzung, kein Casual Chat. Bestehende OpenRouter-basierte Agenten-Loops können es ohne Custom-Client evaluieren, was es zu einem sauberen Kandidaten für Multimodal-Refactor, UI-Portierung und Long-Context-Migrations-Workflows macht.

[NOVA]: Tencent Hy3 free erschien als separate Listung, aber es wurde nicht als eigenständige Story ausgewählt, weil es eine Variante desselben Hy3-Modells ist.

[NOVA]: ...

[ALLOY]: Ollama .31 liefert eine lokale Inferenzverbesserung für Gemma 4 auf Apple Silicon, wobei die Release-Notes eine wesentlich schnellere Token-Generierung durch Multi-Token-Prediction hervorheben. Der berichtete Gewinn beträgt roughly 90 Prozent höheren Durchsatz bei einem Coding-Agent-Benchmark. Das ist eine bedeutsame Local-Agent-Änderung, weil Latenz bestimmt, ob Entwickler ein Modell im Loop behalten fürs Drafting, Review und Iteration.

[NOVA]: Der Workflow bleibt vertraut: Pull Gemma 4 durch Ollama und führe lokale Prompts wie gewohnt aus. Der Unterschied ist, dass mehr der Coding-Schleife auf der Apple-Maschine bleiben kann, statt zu einem Remote-Inference-Endpoint zu hüpfen. Für privacy-sensiblen Code, Offline-Arbeit oder kostengesteuerte Experimente macht schnellere lokale Generierung lokale Agents weniger wie einen Kompromiss fühlen.

[ALLOY]: Wenn der Speedup in realen Projekten hält, wird Gemma 4 durch Ollama zu einem stärkeren Default für lokale Draft-and-Iterate-Aufgaben.

[NOVA]: ...

[NOVA]: OfficeCLI ist eine agentenaufrufbare Office-Suite-Schicht zum Lesen und Bearbeiten von Microsoft Office-Formaten. Das Projekt zog Hacker-News-Attention, weil es Spreadsheet-, Word-Processing- und Präsentations-Operationen in strukturierte Kommandozeilen-Tool-Aufrufe verwandelt. Das ist zuverlässiger, als einen Agenten eine GUI steuern oder komplexen Layout-State durch Screenshots inferieren zu lassen.

[ALLOY]: Der Integrationswinkel ist Enterprise-Automatisierung. Ein Agent kann ein Spreadsheet inspizieren, einen Bericht bearbeiten oder eine Slide-Deck aktualisieren durch eine Tool-Schnittstelle und das Ergebnis dann zurück in einen Workflow geben. Für Office Copilots, Finanzautomatisierung oder Reporting-Agents gibt OfficeCLI dem Modell eine kontrollierte Aktionsfläche für XLSX-, DOCX- und PPTX-Arbeit.

[NOVA]: ...

[NOVA]: UI-MOPD zielt auf kontinuierliches GUI-Agenten-Lernen über Android-, Web- und Desktop-Umgebungen ab. Die Forschung kombiniert ein Uni-GUI-Dataset mit plattformspezifischer On-Policy-Destillation unter Verwendung plattformspezifischer Teacher-Agents zum Trainieren eines Students. Der Punkt ist, ein häufiges Degradationsmuster zu vermeiden: Ein GUI-Agent lernt eine Plattform gut, verliert dann aber Capability, wenn er auf einer anderen trainiert wird.

[ALLOY]: Der Mechanismus ist Live-Trajektorie-Destillation von spezialisierten Teachers. Anstatt statische Traces zu mergen und zu hoffen, dass ein Modell generalisiert, lernt der Student aus On-Policy-Verhalten über Plattformen hinweg. Wenn es funktioniert, bekommen GUI-Agents einen Pfad zu breiterer Kontrolle ohne katastrophales Vergessen, was wichtig ist für Assistants, die über Browser-Apps, Desktop-Software und Mobile-Interfaces operieren müssen.

[NOVA]: ...

[NOVA]: LLM-as-a-Verifier schlägt ein allgemeines Verifizierungsframework vor, bei dem ein Sprachmodell Kandidatenlösungen durch erwartete Token-Level-Log-Wahrscheinlichkeiten bewertet. Anstatt nur ein einzelnes Pass-Fail-Urteil zurückzugeben, kann der Verifier feinkörniges Feedback in Zwischenschritten erzeugen. Das ist wichtig für Reasoning-Systeme, weil viele Fehler früh beginnen und erst bei der endgültigen Antwort offensichtlich werden.

[ALLOY]: Der Integrationsaspekt ist das Evaluator-Design. Agent-Stacks können Verifier-Modelle nutzen, um Pläne, Code-Patches, Beweise oder Tool-Traces zu bewerten, bevor sie sich auf eine Aktion festlegen. Feedback pro Schritt ist nützlicher als eine skalare Bewertung, weil es dem Orchestrator zeigt, wo er revidieren muss. Wenn die Verifier-Skalierung stimmt, wird Evaluation ein aktiver Teil der Inferenz anstatt ein separater Offline-Benchmark.

[NOVA]: ...

[NOVA]: Claude Code .195 hält den Two Point One Agent Harness aktuell, während Workspace-Cache-Isolation die Vertrauensfrage bleibt, die es zu beobachten gilt.

[ALLOY]: Hy3 und Nex-N2-Mini erweitern das OpenRouter-Backend-Mix: ein Sparse-Reasoning-MoE mit Aufwandskontrolle, ein Open-Weight-Multimodal-MoE, optimiert für Coding und Tool-Nutzung.

[NOVA]: GLM 5.2, der Anthropic-Goodwill-Thread und das System-Prompt-Archiv zeigen alle auf dieselbe operative Realität: Modell-Anbieter sind nur ersetzbar, wenn Routing, Evals und Tool-Verträge bereits verdrahtet sind.

[ALLOY]: Ternlight's WASM-Embeddings, codebase-memory-mcp, FastMCP und Microsofts MCP-Curriculum bringen die Agent-Infrastruktur näher an kleine, aufrufbare Komponenten statt an gigantische Prompt-Payloads.

[NOVA]: Die Research-Warteschlange ist reichhaltig: Graph Sparse Sampling für tiefere kontinuierliche Planung, Weak-to-Strong-Distillation für günstigeres Post-Training, Cortex und GaP für verkörperte Agenten und Sauberkeitsstudien zur Messung, wie Code-Stil die Agent-Zuverlässigkeit beeinflusst.

[ALLOY]: Für mehr Details zu den Quellen hinter diesen Geschichten schauen Sie sich die Show-Notizen auf Toby On Fitness Tech dot com an. Danke fürs Zuhören bei AgentStack Daily. Wir sind bald zurück.