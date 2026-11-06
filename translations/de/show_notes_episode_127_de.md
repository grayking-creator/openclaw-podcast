Episode 127 — 05. November 2026

[00:00] Episoden-Einstieg

OpenAI hat 948 Linux-Kernel-Schwachstellen gepatcht, nachdem eine autonome Pipeline entwickelt wurde, die lokale Privilege-Escalation-Fehler fand, validierte und dafür Patches generierte. Jedes Problem könnte einem lokalen Angreifer ermöglichen, erhöhte Privilegien zu erlangen, und die Arbeit verdichtet Entdeckung, Validierung und Patch-Generierung zu einem automatisierten System. Astra demonstrierte, wie ein wegweisendes LLM neuronale Netzwerkgewichte durch Anweisungen in natürlicher Sprache inspiziert und direkt bearbeitet, ohne einen benutzerdefinierten Trainingsloop oder Gradientenabstieg; das Experiment des Teams mit Qwen3.5-0.8B deutet auf eine andere Möglichkeit hin, das Modellverhalten zu modifizieren. OpenAI hat auch Images 2.6 veröffentlicht, mit schnellerer Generierung, GIF-Erstellung, präziserer Bearbeitung und neuen API-Steuerungen für ChatGPT, Codex und die API. Hermes Agent 0.22.7 erweitert die Zusammenarbeit, Zeitplanung und Steuerung über CLI, Web-App, Desktop, Docker und Hermes Cloud. Ricursive Intelligence’s Open-Weight-Modell Ripple-65B bietet natives Tool Calling, ein 1.048.576-Token-Kontextfenster und agentic coding, das für den lokalen Einsatz konzipiert ist, mit einem gemeldeten TerminalBench 2.1 Score von 80,52.

[02:00] Agent Stack Release-Bericht: Hermes Agent v0.22.7, v0.22.6

Nous Research hat Hermes Agent v0.22.6 am 2. November 2026 veröffentlicht, gefolgt von v0.22.7 am 3. November. Zusammen erweitern die Releases maßgeblich, wie Nutzer gemeinsame Agentenarbeit organisieren, deren Ausgabe planen und kontrollieren können, was sie tun kann.

Hermes Agent v0.22.6 fügt eine Web-App hinzu, die direkt vom Gateway bereitgestellt wird. Die CLI kann sie öffnen, und Desktop-Nutzer können über ein Web Access-Panel in ihrem Netzwerk oder hinter einem Nous-Login darauf zugreifen. Desktop-Plugins können auch in einem Browser-Tab geladen werden. Das Release bietet die Umbenennung von Gruppen-Chats, deren Auflösung, Erwähnungen und das Einfügen von Anhängen; jedes Profil kann als Abschnitt in der Desktop-Seitenleiste erscheinen.

Die Planungstools werden ebenfalls übersichtlicher. Nutzer können Cron-Jobs abbrechen, wählen, wie ein Job nach einem verpassten Lauf reagiert, und einen Job über den Desktop-Cron-Editor stoppen. Hermes Agent v0.22.7 erlaubt dann Cron-Jobs, in Gruppen-Chats zu posten. Dasselbe Release fügt optionales Lead-Routing für Desktop-Gruppen-Chats hinzu, ein Lead-Badge, Raumzwecke, gemeinsame Notizen, ein einspaltiges Gruppenlayout, das den Live-Status jedes Mitglieds anzeigt, und angeheftete Kanban-Boards, die als Schnellwechsel-Tabs verfügbar sind.

Zwei Schutzmaßnahmen stechen für Entwickler hervor. Skill-spezifische Sperren können verhindern, dass ein Agent autonome Schreibvorgänge an einem ausgewählten Skill vornimmt, und ein Pre-Inference-Hook kann einen Zug blockieren, bevor das Modell aufgerufen wird. Ein angeheftetes Modell einer Sitzung kann auch zurückgesetzt werden, ohne dessen Verlauf zu löschen.

Das nächste Detail, das es zu beachten gilt, ist v0.23.0, wo Hermes plant, kuratierte Notizen zu diesen Funktionsbereichen und den vollständigen Änderungsverlauf ab v0.22.0 zu veröffentlichen.

[02:53] RicursiveAI’s Ripple-65B ist auf OpenRouter verfügbar

OpenRouter listet Ripple-65B-Preview, ein 65B-Modell von RicursiveAI mit nativem Tool Calling, bereitgestellt in BF16. Tool Calling ermöglicht es einem Modell, ein Programm aufzufordern, eine bestimmte Funktion aufzurufen, wodurch das Modell für Workflows relevant wird, die große Dokumente mit externen Aktionen kombinieren. Das Register listet eine Kontextlänge von 1.048.576 Tokens und eine Text-zu-Text-Architektur. Der von OpenRouter angegebene Preis beträgt 0,0000002 $ pro Prompt-Token, 0,0000006 $ pro Completion-Token und 0,00000005 $ pro Cache-Read-Input-Token. Das gibt Entwicklern einen konkreten Kandidaten für Long-Context-Anwendungen, die Tool-Nutzung erfordern. Das Millionen-Token-Fenster ist die Schlagzeilenkapazität, während der Registerpreis eine unkomplizierte Grundlage für die Schätzung der Nutzungskosten bietet. Das gelistete Modell akzeptiert Text und produziert Text, mit einer Kontextlänge von 1.048.576 Tokens. Das Modell ist über seine Listung auf OpenRouter verfügbar.

[03:42] Astra bearbeitet neuronale Netzwerkgewichte direkt

Das Team berichtet, dass GPT-6 Astra rohe neuronale Netzwerkgewichte inspizieren, ableiten kann, was ein Netzwerk gelernt hat, und ausgewählte Gewichte direkt mithilfe von Argumentation in natürlicher Sprache bearbeiten kann, anstatt einen Trainingsloop zu verwenden. In seinem Qwen3.5-0.8B-Experiment identifizierte Astra ein Problem in den Gewichten, das zu Reasoning Loops führte, und änderte dann 0,016 % davon. Mit denselben Sampling-Einstellungen erhöhte die Korrektur die MATH-500-Genauigkeit von 7,9 % auf 48,1 % und verdreifachte die IFEval-Anweisungsfolge-Performance.

Das Team nennt dies Weight-Space Programming, eine Methode, bei der ein Allzweck-LLM Gewichte als bearbeitbare numerische Artefakte behandelt und darüber nachdenkt, was jeder Teil berechnet. Dies könnte die Modellreparatur ohne konventionelle gradientenbasierte Optimierung unterstützen und Ideen über Modellverhalten erweitern, die allein aus Parametern abgeleitet werden können. Die Ergebnisse sind explizit vorläufig, daher ist das nächste, was es zu beobachten gilt, ob gezielte Bearbeitungen reale Modelle über die berichteten Beispiele hinaus konsistent verbessern können.

[04:35] OpenAI hat 948 Linux-Kernel-Schwachstellen gefunden und gepatcht

OpenAI hat eine autonome Pipeline entwickelt, um schwerwiegende Linux-Kernel-Fehler zu finden und zu beheben. Sie fand, validierte und generierte Patches für 948 lokale Privilege-Escalation-Schwachstellen, d.h. Defekte, die es jemandem mit eingeschränktem Zugriff ermöglichen können, höhere Privilegien auf derselben Maschine zu erlangen.

Die konkrete Veränderung ist die Größe der Warteschlange für Kandidaten-Fixes. Anstatt Kernel-Teams die einzelnen Probleme individuell entdecken und reparieren zu lassen, produziert die Pipeline 948 validierte Schwachstellenfälle mit generierten Patches, die von den Maintainern überprüft werden können. OpenAI ist die Organisation hinter der Pipeline, und die Sicherheitsteams des Linux-Kernels sind die offensichtliche Zielgruppe für deren Ergebnisse.

Das nächste, was es zu beobachten gilt, ist, ob diese generierten Patches die Expertenprüfung bestehen und zu akzeptierten Fixes in Linux werden.

[05:18] OpenAI veröffentlicht schnellere Bilder, GIFs und präzisere Bearbeitung

OpenAI hat Images 2.6 am 4. November veröffentlicht, wodurch die Bildgenerierung schneller wird und zwei sichtbare kreative Funktionen hinzugefügt wurden: GIF-Erstellung und präzisere Bearbeitung.

Das Update ist für ChatGPT, Codex und die API verfügbar. Dies bietet den Nutzern eine interaktive Möglichkeit, visuelle Inhalte zu erstellen und zu verfeinern, sowie eine API-Route, um diese Funktionen in Anwendungen einzubetten.

Für Entwickler besteht die konkrete Möglichkeit, Bildgenerierung, GIF-Erstellung oder präzise Bearbeitung in Produkte und Workflows zu integrieren. OpenAI hat auch neue API-Steuerelemente eingeführt, die erweitern, was Entwickler beim Bauen mit dem Modell konfigurieren können. Als Nächstes bleibt abzuwarten, wie diese Steuerelemente bei realen Bildbearbeitungs- und GIF-Generierungsaufgaben abschneiden werden.

[05:59] Ripple-65B bringt agentisches Open-Weight-Coding auf lokale Maschinen

Ricursive Intelligence hat Ripple-65B Preview veröffentlicht, ein universelles Open-Weight-Modell, das laut Unternehmen eine US-Führungsposition im Bereich des agentischen Codings erreicht. Es erzielte 80,52 Punkte auf TerminalBench 2.1 und lag damit vor Reflection Beam 501B, Meta Muse Spark Open 816B, Thinking Machines Inkling 975B und NVIDIA Nemotron 3 Ultra 550B.

Das Modell wurde auf 12 Billionen Tokens vortrainiert und unterstützt Kontextlängen von bis zu einer Million Tokens. Ricursive entwickelte seine dichte Architektur für effizientes Training und Serving auf NVIDIA Hardware, mit dem Ziel, einen starken lokalen Betrieb auf Systemen wie NVIDIA DGX Spark zu ermöglichen. Es ist auf Hugging Face, Together AI, GMI Cloud und OpenRouter verfügbar, wobei Fireworks noch am selben Tag starten soll.

Ricursive berichtet, dass die gesamten Forschungs- und Entwicklungskosten von Ripple, einschließlich Datenaufbereitung, Evaluierung, Debugging und Nachtraining, 32 Millionen US-Dollar betrugen. Um die Code-Effizienz zu verbessern, testete das Unternehmen architektonische Änderungen bei kleineren Modellskalen, bevor es sie hochskalierte, und baute eigene synthetische Datenpipelines, anstatt Nachtrainingsdaten zu kaufen. Als Nächstes bleibt abzuwarten, wie das Modell außerhalb der agentischen Coding-Evaluierung von Ricursive abschneidet, während die Entwicklung hin zu größeren Modellen fortschreitet.

[07:08] ComfyUI liefert Textur- und Dubbing-Nodes aus

ComfyUI hat am 4. November 2026 seine stabile Version v0.44.0 veröffentlicht, die neue kreative Bausteine für Workflows enthält. Die Veröffentlichung fügt Partner Nodes für Patina Texturarbeiten und VEED Synchronisation hinzu, beides von bigcat88 beigesteuert.

Für Nutzer, die mit ComfyUI arbeiten, bieten die Ergänzungen neue knotenbasierte Möglichkeiten, Texturerstellung und Synchronisation in einen Workflow zu integrieren. Die Veröffentlichung aktualisiert auch die Workflow-Vorlagen von ComfyUI auf v0.11.98 und bietet Entwicklern eine aktualisierte Sammlung von Workflow-Startpunkten.

Die verbleibende Änderung ist interne Wartung: Das Projekt hat die Python-Version von pylint auf 3.1 umgestellt. Der kreatorenzentrierte Fokus dieser Veröffentlichung liegt auf dem Paar von Partner Nodes, sodass die nächsten nützlichen Erkenntnisse aus vollständigen Workflows stammen werden, die zeigen, wie die Textur- und Synchronisationsphasen zusammenarbeiten.

[07:52] Wähler verhängen neue Einschränkungen für KI-Rechenzentren

Amerikanische Wähler haben Rechenzentren in mehr als 30 Gemeinden in neun Bundesstaaten abgelehnt oder eingeschränkt. Die Maßnahmen umfassten Moratorien, vollständige Verbote sowie finanzielle oder betriebliche Einschränkungen für Hyperscaler, die Steuervergünstigungen anstreben, wobei einige Abstimmungen direkt auf bereits laufende Projekte reagierten.

Die Ergebnisse waren besonders deutlich in Edgewater, Florida, wo die Bewohner überwältigend die Verankerung eines Rechenzentrumsverbots in der Stadtverfassung unterstützten. In Perry, Ohio, verabschiedeten Wähler eine Maßnahme, die Hyperscalern, die Steuervergünstigungen anstreben, finanzielle und betriebliche Einschränkungen auferlegt.

Der politische Druck weitet sich über lokale Abstimmungen hinaus aus. Demokraten, die in über 130 Bundes- und Gouverneurswahlen antraten, nutzten laut einer Analyse Anti-Tech- oder Anti-Rechenzentrums-Werbung. Der Gouverneur von Texas, Greg Abbott, der kürzlich KI und den Ausbau von Rechenzentren förderte, versprach strengere Vorschriften, verlor aber seine Wahl.

Dieser Widerstand beeinflusst bereits das Kapital. Banken und Vermögensverwalter, die Rechenzentren finanzieren, haben begonnen, lokalen Widerstand als Kreditrisiko zu behandeln, während Hyperscaler Community Liaisons einstellen. Einige Unternehmen versuchen auch, ihre Einrichtungen als „Compute Campuses“ zu bezeichnen, obwohl das Rebranding gemischte Ergebnisse gezeigt hat.

Der nächste Test ist, ob diese lokalen Einschränkungen ändern, wo neue KI-Infrastruktur gebaut wird, welche Projekte Finanzierungen und Anreize sichern können und wie Betreiber reagieren, wenn Gemeinden mehr als nur Branding fordern.

[09:08] SambaNova und Supermicro planen gemischte KI-Inferenzsysteme

SambaNova und Supermicro haben eine strategische Zusammenarbeit angekündigt, um KI-Inferenzsysteme zu bauen und zu verkaufen, die RDUs und GPUs kombinieren. Supermicro plant anfänglich 10.000 SN50 RDU-Chips für dieses Vorhaben.

SambaNova gibt an, dass die Partnerschaft darauf abzielt, agentische KI anzusprechen, wobei Mitbegründer Rodrigo Liang sie als „die nächste Welle der Inferenz“ bezeichnet, die überall laufen muss. Der konkrete Vorschlag ist eine gemischte Systemarchitektur anstelle eines einzelnen Prozessortyps, die die RDU-Chips von SambaNova mit GPUs zusammenführt.

Für Entwickler ist die wichtige Entwicklung die Kombination aus einem benannten Fertigungspartner, einer Produktkategorie und einem anfänglichen Chip-Volumenziel. Als Nächstes bleibt abzuwarten, ob die geplanten 10.000 SN50-Chips in verfügbare Inferenzsysteme übergehen.

[09:52] OpenAI verknüpft neue Rechenzentrums-Campusse mit Netzstabilität

Am 2. November stellte OpenAI das Grid Protectors Program vor, das mit Versorgungsunternehmen zusammenarbeiten wird, um zukünftige Rechenzentrums-Campusse bei der Unterstützung der Netzstabilität zu helfen und die Stromkosten der Verbraucher zu schützen.

Die Initiative adressiert beide Seiten des Wachstums der KI-Infrastruktur: die Bedürfnisse großer Rechenanlagen und deren Auswirkungen auf die Stromkunden, die sie unterstützen. OpenAI positioniert das Programm auf direkte Zusammenarbeit mit Versorgungsunternehmen, anstatt neue Computertechnologie oder eine Software-Veröffentlichung zu präsentieren.

Für Organisationen, die KI-Dienste entwickeln, ist die praktische Implikation, dass Stromzugang, Netzstabilität und Verbraucherkosten Teil der Einsatzplanung sind und keine separaten Anliegen. Das Detail, das es zu beobachten gilt, ist, welche Versorgungsunternehmen und zukünftigen Campusse teilnehmen und welche Schutzmaßnahmen sich aus diesen Vereinbarungen ergeben.

[10:36] Forschungsübersicht: Labor-KI versteht Abläufe, übersieht aber immer noch die physikalischen Details

Aktuelle AI-Modelle können die groben Schritte eines im Video gezeigten Laborverfahrens befolgen, kämpfen aber immer noch mit den physikalischen Details, die zur Ausführung dieser Schritte erforderlich sind. Der BEAKER-Benchmark evaluiert, ob Modelle eine beabsichtigte Aktion mit dem richtigen Teil eines Objekts und einem machbaren Bewegungspfad durch ein Labor verbinden können.

Die Autoren kuratierten manuell Fragen zu Geräte- und Experimentalzustandserkennung, Sicherheit, Apparateaufbau, Betrieb, Prozedurreihenfolge und Schlussfolgerungen aus Bildern und Video. Aktuelle Modelle schnitten bei groben prozeduralen Schritten besser ab als bei Aufgaben, die erforderten, dass Aktionen in bedienbaren Regionen und machbaren Trajektorien – einem Pfad, der beschreibt, wie eine Maschine sich bewegen oder agieren kann – verankert sind.

Dies ist wichtig, da ein autonomes chemisches Labor nicht nur verstehen muss, welches Experiment gerade läuft, sondern auch die Szene wahrnehmen, prozedurale und Sicherheitsbeschränkungen respektieren und Aktionen wählen muss, die in der physischen Welt funktionieren. Zum Beispiel könnte ein System erkennen, dass eine Probe bewegt werden muss, während es immer noch nicht identifizieren kann, was gegriffen werden kann oder wie es zu erreichen ist. BEAKER gibt Forschungsteams eine konkrete Möglichkeit, diese Lücke aufzudecken und zu vergleichen, bevor ähnlichen Modellen die Kontrolle über ein Labor anvertraut wird.

[11:48] OpenAI hat ein Git-Backend für die Entwicklung im Codex-Maßstab entwickelt

OpenAI hat Pando entwickelt, ein Git-kompatibles Backend, das für den Entwicklungsmaßstab konzipiert ist, den Codex ermöglicht.

Die Änderung ist wichtig, weil sie die Repository-Schicht unterhalb der KI-gestützten Codierung adressiert. Git ist das System, das Entwickler verwenden, um Code-Änderungen zu verfolgen und zu verwalten, und Pando wurde entwickelt, um ein kompatibles Backend für die Entwicklung im Codex-getriebenen Maßstab bereitzustellen.

Die konkreten Beweise in der Ankündigung von OpenAI sind der Umfang und der Besitz des Systems: OpenAI hat es gebaut, es ist Git-kompatibel, und die Codex-getriebene Entwicklung setzt seinen Zielmaßstab. Das gibt Entwicklern, die KI-intensive Entwicklungsumgebungen evaluieren, ein spezifisches Infrastrukturmuster zur Betrachtung: ein Git-kompatibles Backend, das um die Arbeitslast herum konzipiert ist, die Codex ermöglicht.

Wie Pando unter realen Repository-Lasten funktioniert, ist der nächste Punkt, den es zu beobachten gilt.

[12:32] OpenAI erwirbt Pierre, um Codex zu erweitern

OpenAI gab am 4. November bekannt, dass es die Pierre Computer Company übernehmen wird. Das Unternehmen sagt, dass die Akquisition die Tools von Codex zum Erstellen, Verstehen und Überprüfen von Code erweitert.

Das gibt dem Deal einen klaren Produktfokus: die Stärkung der Art und Weise, wie Entwickler Software erstellen, bestehende Codebasen inspizieren und Code bewerten. OpenAI nutzt eine Akquisition, um die Rolle von Codex im gesamten Softwareentwicklungsprozess zu erweitern, anstatt die Ankündigung als eigenständige Feature-Veröffentlichung zu präsentieren.

Für Entwickler signalisiert dies eine fortgesetzte Investition in Codex als Ort für praktische Entwicklungsarbeit. Die nützlichsten Fähigkeiten, die bei ihrer Einführung evaluiert werden sollten, sind Code-Erstellung, Code-Verständnis und Code-Review.

[13:10] Together Compiler re-optimiert Inferenz bei wechselndem Datenverkehr

Together AI hat Together Compiler auf den Markt gebracht, ein Agenten-gesteuertes System, das den Forward-Pass eines Inferenzmodells bei wechselndem Datenverkehr kontinuierlich neu optimiert. Der Forward-Pass ist die Modellberechnung, die ihre Ausgabe erzeugt. Together AI berichtet, dass der Compiler bis zu 2,6-mal mehr Tokens pro Sekunde erreichte als die besten InferenceX-Konfigurationen, wobei das Ergebnis in weniger als 24 Stunden pro Modell erzielt wurde.

Dies ist wichtig, weil Inferenz-Entwickler nun einen Optimierungsprozess evaluieren können, der sich an den tatsächlich bedienten Datenverkehr anpasst, anstatt eine abgestimmte Konfiguration unverändert zu lassen. Der nützliche Mechanismus ist die kontinuierliche Agenten-gesteuerte Schleife; die konkreten Beweise sind der gemeldete Durchsatzvergleich und die Optimierungszeit. Eine Sache, die es zu beobachten gilt, ist, ob der gemeldete Gewinn auf verschiedene Modelle und Datenverkehrsmuster übertragbar ist.