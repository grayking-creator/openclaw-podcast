Episode 124 — 21. Oktober 2026

[00:00] Episode-Hook

MiniMax hat M3.1 Flash offiziell eingeführt, ein Modell für agentische Aufgaben mit mehrstufigen Abläufen und Tool-Nutzung sowie zusätzlichen Anwendungen in Coding, Computerbedienung und Cybersicherheit. Google, Red Hat und IBM haben außerdem llm-d 1.0 veröffentlicht, einen quelloffenen, nativ auf Kubernetes basierenden Stack für die verteilte Inferenz großer Sprachmodelle auf TPUs und GPUs; die Version ergänzt Mandantenfähige Flusssteuerung und Cache-bewusstes Routing für große KI-Bereitstellungen. SGLang hat sein Serving-Ökosystem um die Unterstützung für Clef und Clef Flash, PPLX-Decider v1 und v1.1 sowie EmbeddingGemma 2 erweitert und für jedes Modell zusätzlich Cookbook-Beispiele bereitgestellt. Microsoft hat eine Model Card für Sentiment-Analysis-7B veröffentlicht, ein Sprachmodell mit 7 Milliarden Parametern, das an Dienste, Produkte oder Agenten gerichtete Nutzernachrichten als Negative, Neutral oder Positive klassifiziert. Mistral hat Timestral eingeführt, seine erste Familie vortrainierter Zeitreihenmodelle, die Prognosen für Sensorwerte, Nachfrage, Volatilität und andere sequenzielle Daten auf reine CPU-Workloads ausweitet.

[02:00] MiniMax M3.1 Flash zielt auf schnellere und günstigere Agenten

MiniMax hat M3.1 Flash offiziell als Modell der nächsten Generation für agentische Aufgaben, Coding, Computerbedienung und Cybersicherheit eingeführt. Laut MiniMax ist die Online-Inferenz nahezu dreimal so schnell, und die Nutzungskosten für agentische Aufgaben liegen 70 % unter denen seines Vorgängers. Das Unternehmen erklärt, das Modell könne vollständige SaaS-Workflows in Vertrieb, Marketing, Betrieb, Kundenservice, Finanzen und Personalwesen abdecken. Es könne Code eigenständig verstehen, Funktionen entwickeln, Fehler beheben, seine Arbeit durch Tests validieren und über lange Aufgabenfolgen hinweg Tools einsetzen. Bei der Computerbedienung erzielt es laut Anbieter 61,7 Punkte in OSWorld V2 und 29,6 Punkte in Agents’ Last Exam, einem Benchmark für professionelle Arbeit und komplexe Aufgaben. MiniMax führt einen Teil des Effizienzgewinns auf aggressivere Sparsität zurück, durch die die aktive Berechnung reduziert wird. Im Alltag erreicht das Modell demnach mehr als 200 Tokens pro Sekunde, im Median mehr als 170 Tokens pro Sekunde. Die Festpreisgestaltung beträgt 0,15 US-Dollar pro Million Eingabetokens, 0,60 US-Dollar pro Million Ausgabetokens und 0,015 US-Dollar pro Million zwischengespeicherten Eingabetokens. M3.1 Flash ist über die MiniMax API, M Plan und MiniMax Code verfügbar. MiniMax hat angekündigt, die Modellgewichte später zu veröffentlichen.

[02:23] llm-d 1.0 ergänzt Cache-bewusstes Routing für KI-Flotten

Google, Red Hat und IBM haben llm-d 1.0 ausgeliefert, einen quelloffenen Stack rund um Kubernetes für die Verteilung der Inferenz großer Sprachmodelle auf TPUs und GPUs.

Die Veröffentlichung vereint mehrere betriebliche Funktionen in einer Ebene: Cache-bewusstes und Agent-bewusstes Routing, mandantenfähige Flusssteuerung sowie Ausf-free Upgrades. Cache-bewusstes Routing bedeutet, dass Anfragen unter Berücksichtigung des Inferenz-Caches weitergeleitet werden können; Agent-bewusstes Routing berücksichtigt zusätzlich Agent-Workloads. Die mandantenfähige Flusssteuerung ermöglicht das Traffic-Management, wenn mehrere Nutzer oder Workloads dieselbe Serving-Flotte gemeinsam nutzen.

Der Stack erstreckt sich über vLLM und SGLang und bietet Teams damit eine einheitliche Möglichkeit, verteilte Inferenz über diese Engines und beide Beschleunigerfamilien hinweg zu betreiben. Das ist für Organisationen wichtig, die nicht jede Serving-Komponente unabhängig verwalten möchten, insbesondere wenn Agent-Anwendungen ein koordiniertes Request-Routing benötigen und Produktions-Upgrades laufenden Traffic nicht unterbrechen dürfen.

Als Nächstes bleibt abzuwarten, wie wirksam sich diese Steuerungsmechanismen in echten Produktionsflotten erweisen, während Teams llm-d 1.0 zu übernehmen beginnen.

[03:20] SGLang fügt drei neue Modellfamilien hinzu

SGLang v0.5.22 erweitert die Auswahl an Modellen, die Teams über den Serving-Stack nutzen können. In den Release Notes werden Clef und Clef Flash, PPLX-Decider v1 und v1.1 sowie EmbeddingGemma 2 als neue Modelle aufgeführt, für jedes mit einem eigenen verlinkten Cookbook-Eintrag.

Das ist wichtig, weil die praktische Arbeit beim Bereitstellen eines Modells mehr umfasst als das Herunterladen seiner Gewichte: Entwickler benötigen außerdem einen erprobten Weg, es bereitzustellen. Die neuen Einträge bieten selbst gehosteten Anwendungen und Agent-Stacks zusätzliche dokumentierte Modelloptionen, die sie evaluieren können – einschließlich Workloads mit Sprachmodellen und Vision-Language-Modellen.

Die Veröffentlichung zeigt zudem umfangreiche Wartungsaktivitäten, mit 950 Pull Requests von 245 Mitwirkenden. Die nächste Frage für alle, die das Update evaluieren, lautet, welche der neuen Modelle ihren Serving-Anforderungen und Workloads entsprechen.

[04:06] Microsofts 7B-Modell ergänzt lokale Sentiment-Klassifikation

Microsofts Model Card beschreibt Sentiment-Analysis-7B als ein Sprachmodell mit 7 Milliarden Parametern, das für die Klassifikation der Stimmung in Nachrichten an einen Dienst, ein Produkt oder einen Agenten feinabgestimmt wurde. Das Modell wurde mit Reinforcement Learning und einem LLM Judge an einem kleinen internen Datensatz mit ungefähr 300 Beispielen trainiert. Es erzeugt Negative, Neutral oder Positive als erstes Token, gefolgt von einer kurzen Erklärung. Ein Generierungslimit von drei Tokens gibt ausschließlich die Bezeichnung zurück, während das Beispiel des Herausgebers mit Transformers zeigt, wie das kausale Modell geladen und eine ausführlichere Antwort generiert wird. Der Herausgeber berichtet für Sentiment-Analysis-7B eine Genauigkeit von 72,8 %, verglichen mit 62,0 % für Mistral-7B-Instruct-v0.2. Die geringe Größe des Trainingsdatensatzes und die Betonung von Reinforcement Learning in der Model Card sind wichtiger Kontext für alle, die das Modell als lokale Sentiment-Komponente in einem Agent-Stack in Betracht ziehen. Der veröffentlichte Workflow lädt das kausale Modell mit Transformers’ AutoModelForCausalLM.

[04:57] Forschungsdigest: KI-evolvierte Suchentwürfe liefern messbare Verbesserungen bei der Retrieval-Qualität

Forscher haben gezeigt, dass ein Sprachmodell bei der Gestaltung generativer Retrieval-Systeme helfen kann. Dabei werden für Dokumente kompakte semantische Labels generiert, statt sich ausschließlich auf Keyword-Matching zu verlassen. Ein lokal bereitgestelltes Modell mit offenen Gewichten generierte und testete Änderungen an ausführbaren Teilen des Systems, einschließlich der Konstruktion semantischer Labels und der Behandlung von Kollisionen, ohne einen proprietären KI-Dienst zu verwenden.

Das evolvierte Design verbesserte das Retrieval in Datensätzen für allgemeine Web-Suche, Web-Suche und mehrsprachigen E-Commerce. Bei einem Benchmark stieg der Anteil der Fälle, in denen das korrekte Ergebnis an erster Stelle erschien, von 55,8 % auf 59,3 %. Ein kleinerer Proxy-Decoder lieferte dem System schnelles Feedback, während die Forscher nach besseren Designs suchten, anstatt den vollständigen Generator wiederholt zu trainieren.

Die wichtige Einschränkung besteht darin, dass der Proxy Verbesserungen bei Änderungen am semantischen Index, aber nicht zuverlässig bei Änderungen an der Trainingszielsetzung des Generators oder an der gesamten Pipeline vorhersagte. Dadurch ist die Methode für das Suchdesign vielversprechend, zugleich aber wird eine Proxy-Validierung unverzichtbar, bevor sie anderswo eingesetzt wird.

[05:56] Mistrals Timestral bringt vortrainierte Prognosen auf reine CPU-Workloads

Mistral hat Timestral veröffentlicht, eine Familie von vier Zeitreihen-Basis-Modellen mit 5 Millionen, 28 Millionen, 123 Millionen und 209 Millionen Parametern. Die Modelle bieten Zero-Shot-Prognosen, können also Vorhersagen für bislang unbekannte Daten ohne aufgabenspezifisches Training treffen und über Mistral Forge für eine bestimmte Domäne feinabgestimmt werden.

Laut Mistral belegte Timestral bei GIFT-Eval, TIME und fev-bench in fünf Metriken den ersten Platz unter den vortrainierten Zero-Shot-Modellen. Das Unternehmen erklärte, die Ergebnisse seien von einem einzelnen Checkpoint und ohne die Kombination mehrerer Modelle erzielt worden. Die Version mit 28 Millionen Parametern übertraf Chronos-2 bei GIFT-Eval und TIME und benötigte dabei ungefähr ein Viertel so viele Parameter. Das Modell mit 209 Millionen Parametern übertraf TimesFM-3 und Falcon-2.0 mit weniger Parametern.

Die Modelle können mehrere verwandte Zeitreihen gemeinsam prognostizieren und einen vollständigen Satz von Quantilen erzeugen. Dadurch können Teams Unsicherheit ausdrücken, statt sich auf einen einzelnen vorhergesagten Wert zu verlassen. Sie akzeptieren außerdem kategoriale Eingaben direkt, etwa den Zustand einer Maschine – laufend, untätig oder in Wartung – sowie bekannte zukünftige Eingaben wie Produktionspläne, geplante Stillstände und Wettervorhersagen. Timestral grenzt diese Eingaben von der Zielreihe ab, sodass zukünftige Zielwerte nicht in die Prognosen einfließen.

Für den Einsatz wird keine Grafikprozessorkarte benötigt. Auf einem Serverprozessor mit acht Threads dauerte die Prognose eines Tages im Voraus auf Basis von drei Wochen historischer Daten im 15-Minuten-Takt 10 Millisekunden mit dem Modell mit 5 Millionen Parametern und 140 Millisekunden mit dem Modell mit 209 Millionen Parametern.

Damit ist Timestral eine praktische Option für die Überwachung von Pipelines, die industrielle Sensoren, Finanzströme und andere operative Daten umfassen. Mistral Forge unterstützt Fine-Tuning, domänenspezifische Erweiterungen, die Erzeugung synthetischer Daten sowie den Einsatz auf Client-Hardware, einschließlich netzwerkgetrennter Umgebungen. Die entscheidende verbleibende Frage ist, ob die Anpassung eine hohe Leistungsfähigkeit erhält, wenn sich die Produktionsdaten im Laufe der Zeit ändern.

[07:40] Mercury 3 bringt Diffusions-LLMs auf Produktionsgeschwindigkeit

Inception Labs hat Mercury 3 veröffentlicht, ein auf Diffusion basierendes Sprachmodell für Anwendungen, bei denen die Antwortzeit das Nutzungserlebnis beeinflusst. Laut Unternehmen erreicht das Modell in der eigenen Benchmark-Suite bessere Ergebnisse als GPT-6 Luna und Claude Haiku 5.5, erzeugt auf NVIDIA GPUs 1.068 Tokens pro Sekunde und unterstützt ein Kontextfenster von 1 Mio. Tokens, gegenüber 260K bei Mercury 2.5.

In einer Produktionsumgebung für Web-Agenten erledigte Mercury 3 50 % von 50 Live-Navigationsaufgaben in Mind2Web. Inception berichtet, dies sei mehr gewesen als bei GPT-6.1-Sol bei identischem Token-Volumen und gleicher Anzahl an Agentenschritten. Das Unternehmen nennt außerdem eine mittlere Generierungszeit von 0,9 Sekunden und eine mittlere End-to-End-Antwortzeit von 2,2 Sekunden in Octens Tests für die Suche mit intelligenten Brillen.

Mercury 3 kostet 0,20 US-Dollar pro Million Eingabetokens und 0,70 US-Dollar pro Million Ausgabetokens. Zum Start werden 50 % Rabatt auf den Preis gewährt, auf zwischengespeicherte Eingabetokens werden 90 % Rabatt gewährt. Inception und seine Partner verwenden das Modell für Sprach- und Chat-Support, Nachhilfe, Suche, Data Engineering und Webnavigation. Das Modell ist über Inceptions API, OpenRouter, Basetan und Vercel verfügbar und bietet OpenAI-API-Kompatibilität. Die nächste Bewährungsprobe ist, ob die gemeldete Geschwindigkeit und Qualität auch bei dauerhaften Produktionslasten Bestand haben.

[08:51] Forschungsdigest: Roboter lernen, Sprache als Gedächtnis zu nutzen

Forscher stellten UniWALM vor, ein Modell, das Video, Aktionen und Sprache in einer gemeinsamen Darstellung miteinander verbindet. Das wichtige Ergebnis ist, dass die gemeinsame Erzeugung von Sprache offenbar die robotische Manipulation verbessert und bei Aufgaben hilft, die sich auf das Erinnern früherer Ereignisse stützen.

Statt Informationen über separate Wahrnehmungs-, Planungs- und Handlungsstufen weiterzugeben, erzeugt UniWALM eine Aktion und ein textuelles Gedächtnis gemeinsam. Die erzeugte Sprache wird anschließend im nächsten Schritt verwendet. Dadurch entsteht für den Roboter ein schlanker Gedächtniskreislauf ohne externen Planer oder Gedächtnisspeicher. Im gedächtnisabhängigen Teil von RMBench erreichte das System 34,5 %, ohne ein vortrainiertes Sprach- oder Denkmodell einzusetzen.

Die Forscher trainierten das Modell außerdem darauf, sich von gestörten Handlungsbahnen zu erholen, und fügten diese Fähigkeit hinzu, ohne die Inferenzkosten zu erhöhen. Eine konkrete Folge ist ein Roboter, der eine Aufgabe sowohl durch Bewegung als auch durch Sprache weiterführen kann: Er kann handeln, eine kurze Notiz zur Aufgabe aufzeichnen und diese Notiz anschließend als Grundlage für sein nächstes Handeln verwenden.

[09:50] Concat bietet eine lokale, skriptbare Alternative zu CapCut

Concat ist ein quelloffener, lokal arbeitender und plattformübergreifender Video-Editor, der als kostenlose Alternative zu CapCut präsentiert wird. Seine wichtigste Funktion für Entwickler ist die Skriptbarkeit über eine JSON-RPC-API und MCP. Beide bieten strukturierte Schnittstellen, über die Software mit dem Editor interagieren kann.

Dieser Unterschied ist wichtig, weil er einen Weg eröffnet, Videobearbeitung mit automatisierten Workflows zu verbinden, statt jede Bearbeitung als manuelle Aufgabe in einer Benutzeroberfläche zu behandeln. Das GitHub-Repository weist 10.199 Sterne auf, was auf erhebliches Interesse an dem Projekt hindeutet.

Concat ist daher als lokale Bearbeitungsgrundlage für Tools und Workflows durchaus im Blick zu behalten. Der nächste nützliche Nachweis wären konkrete Beispiele für Bearbeitungsfunktionen, die über seine Schnittstellen bereitgestellt werden, sowie die Frage, wie zuverlässig diese Funktionen tatsächliche Bearbeitungsaufgaben bewältigen.

[10:33] Terminal X nutzt GPT-6.1 Sol zur Prüfung von Investmententscheidungen

OpenAIs Fallstudie vom 20. Oktober stellt Terminal X’ Eval Agent in den Mittelpunkt, der Ausgaben anhand einer Bewertungsmatrix mit 54 Kriterien bewertet. In der beschriebenen Konfiguration stimmte GPT-6.1 Sol laut OpenAI in 88,6 % der Fälle mit dem Urteil erfahrener Investoren überein und erkannte 25 % mehr Abweichungen vom Anlageauftrag des Fonds.

Damit wird die regelbasierte Prüfung zu einem konkreten Muster: die Kriterien definieren, die eine Antwort erfüllen muss, sie anhand dieser Kriterien bewerten und prüfen, wo sie von den Regeln oder der Einschätzung erfahrener Fachkräfte abweicht. Der Vorteil besteht darin, dass die Bewertung zu einem separaten, kriterienbasierten Schritt wird, statt sich ausschließlich auf eine abschließende menschliche Prüfung zu verlassen.

Als Nächstes ist zu beobachten, ob die berichtete Übereinstimmung und die Erkennung von Abweichungen auch auf andere Mandate, Modelle und Arten von Investmentergebnissen übertragbar sind. Die 88,6-%-Ergebnis bezieht sich auf die von Terminal X gemeldete Konfiguration.

[11:22] Exa 3.0 ergänzt ein größeres Embedding-Modell und eine Lite-Option für 4 US-Dollar

Exa hat Version 3.0 seiner Search API veröffentlicht und dabei ein größeres Embedding-Modell, eine Exa Lite-Option für 4 US-Dollar je 1.000 Anfragen sowie Dynamic Highlights hinzugefügt.

Das größere Embedding-Modell verändert das Repräsentationssystem, mit dem Suchanfragen den relevanten Inhalten zugeordnet werden, während Exa Lite eine günstigere API-Option einführt. Dynamic Highlights ist eine weitere neue Funktion, die über die aktualisierte API bereitgestellt wird.

Exa hat außerdem einen Vergleich mit Perplexity, Brave und Parallel durchgeführt und angegeben, dass sein System in allen acht Benchmarks führend war. Da Exa diese Tests selbst durchgeführt hat, sollten Entwickler das Ergebnis als starke Herstellerangabe und nicht als unabhängige Validierung betrachten.

Die praktische Frage lautet, wie Exa 3.0 bei den eigenen Suchanfragen eines Teams abschneidet und wie sich die neuen Optionen auf das Budget auswirken. Unabhängige Benchmark-Ergebnisse und das Verhalten von Dynamic Highlights in realen Arbeitsabläufen sind die nächsten Aspekte, die zu beobachten sind.

[12:13] ChatGPT Work beschleunigt die Preisanpassung von Restaurantmenüs

Ein unabhängiger Franchisebetreiber von Schlotzsky’s und Cinnabon hat mit einem auf ChatGPT Work aufgebauten Workflow die für die Preisanpassung seiner Menüs benötigte Zeit um 95 % reduziert. Der Betreiber schätzt, dass diese Änderung 100.000 US-Dollar an Liquidität freisetzen könnte. Damit ist dies ein konkretes Beispiel dafür, wie KI über die Content-Generierung hinaus in wiederkehrende betriebliche Abläufe einfließt.

Das wichtige Ergebnis besteht nicht lediglich in einem schnelleren Bearbeiten der Menüs. Indem der Franchisebetreiber den Prozess der Preisanpassung in einen wiederholbaren Workflow verwandelt hat, konnte er eine alltägliche operative Aufgabe mit einem möglichen Vorteil beim Betriebskapital verknüpfen. Die gemeldete Reduzierung um 95 % liefert den deutlichsten Beleg für die Wirkung.

Für andere Restaurantgruppen und Unternehmen mit mehreren Standorten liegt die Chance darin, häufige Preisanpassungsaufgaben zu identifizieren und zu testen, ob ein ähnlicher ChatGPT Work-Workflow die Arbeitszeit der Mitarbeiter reduzieren und gleichzeitig den Cashflow verbessern kann. Der nächste Test besteht darin, ob andere Betreiber sowohl die Zeitersparnis als auch den finanziellen Vorteil an ihren eigenen Standorten reproduzieren können.

[13:07] OpenAI übernimmt Orchestra Bio für die Life-Sciences-Forschung und -Entwicklung

OpenAI übernimmt Orchestra Bio, um KI-gestützte Abläufe in die Forschung und Entwicklung der Life-Sciences-Branche zu bringen. Zielgruppe sind biopharma-Teams, die an der Arzneimittelentwicklung arbeiten; dabei soll ihnen geholfen werden, Entwicklungsprozesse zu beschleunigen und neue Behandlungsmethoden voranzubringen.

Entscheidend ist derzeit der Kontext: Die Ankündigung konzentriert sich auf den Einsatz von KI in den Forschungs- und Entwicklungsabläufen der Life-Sciences-Branche, statt einen weiteren allgemein zweckorientierten Chatbot oder ein eng abgegrenztes Forschungsergebnis vorzustellen. Dadurch ist die Meldung für Teams relevant, die überlegen, wie KI alltägliche biopharma-Workflows unterstützen könnte.

Der nächste nützliche Nachweis wird konkret sein: Welche Forschungs- und Entwicklungsprozesse werden mit KI betrieben, wie werden diese Funktionen bereitgestellt und helfen sie Teams, schneller voranzukommen?

[13:48] OpenAI ergänzt ChatGPT-Bewertungen für weniger gut versorgte Sprachen

OpenAI verbessert ChatGPT in weniger gut versorgten Programmiersprachen – also Sprachen, für die weniger digitale Beispiele und Ressourcen für Softwaretools verfügbar sind. Das Unternehmen hat neue Bewertungen für Software Engineering, SQLite und die COBOL-Migration angekündigt.

Die Änderung ist für Teams wichtig, deren Arbeit sich nicht auf die am weitesten verbreiteten Programmiersprachen konzentriert. SQLite-Aufgaben umfassen datenbankorientierte Arbeit, während es bei der COBOL-Migration darum geht, Code aus einer älteren Programmiersprache für Unternehmensanwendungen zu migrieren. In diesen konkreten Bereichen können die Grenzen eines KI-gestützten Coding-Assistenten reale Projekte beeinflussen.

Für Entwickler bieten die neuen Bewertungen eine relevantere Grundlage für die Beurteilung von ChatGPT als allgemeine Programmierfragen. Ein Team kann untersuchen, wie das Modell eine Software-Engineering-Aufgabe, ein SQLite-Szenario oder eine COBOL-Migration bewältigt, bevor es entscheidet, wo KI-Unterstützung in seinen Workflow gehört.

Ein Aspekt, der zu beobachten ist, zeigen die erweiterten Bewertungen über die Leistung, während OpenAI ChatGPT in weniger gut versorgte Sprachumgebungen ausweitet.