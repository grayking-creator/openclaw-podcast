Folge 126 — 29. Oktober 2026

[00:00] Einstieg der Folge

Google hat Gemini 4 Carbon als sein leistungsstärkstes Modell angekündigt. Es wurde für langlebige Softwareentwicklungs-Workflows und den vollständigen Zyklus der Cybersicherheitsverteidigung entwickelt. Laut Google fand Carbon Schwachstellen. OpenAI hat Modellergebnisse veröffentlicht, die sich auf die Kakeya-Vermutung, die Exponential Time Hypothesis und die Quantenchromodynamik beziehen und somit die Arbeit des Unternehmens auf Mathematik und Physik ausweiten. Laut einer OpenAI-Fallstudie vom 27. Oktober bearbeiten die mit OpenAI betriebenen Sprachagenten von Retell inzwischen jeden Monat 100 Millionen Anrufe, wobei GPT-6 Astra die Sprachagenten-Benchmark des Unternehmens anführt. Die Anthropic-Ingenieurinnen Katelyn Lesse und Angela Jiang erklärten, wie das Team der Claude Platform Opus 5.5 eingeführt hat und verwaltete Agenten betreibt, indem es die Entscheidungsfindung des Modells von seinen externen Aktionen trennt. Auch für Hardwareentwickler gibt es neue lokale KI-Optionen: Die kompakte Radeon AI Pro R9700 Workstation-Grafikkarte von ASRock kombiniert 32 GB GDDR6 mit 640 GB/s Bandbreite und RDNA-4-FP8-Unterstützung. NVIDIA veröffentlichte außerdem Nemotron-3.5-Bolt-E4B-4GB, ein quantisiertes 8B-Parameter-Modell mit 4 GB, das für lokale Sprachassistenten, interaktive Personas und eingebettete Benutzeroberflächen entwickelt wurde.

[02:00] Gemini 4 Carbon zielt auf langlebige Entwicklungs- und Cybersicherheitsaufgaben

Google hat Gemini 4 Carbon als sein Modell der nächsten Generation angekündigt. Laut Google kann Carbon mehrere Tage lang laufen, Sackgassen überstehen, die Ursachen subtiler Fehler in großen Codebeständen ermitteln und Behebungen erstellen. Die Ergebnisse im Bereich Cybersicherheit umfassen drei Phasen: Schwachstellen finden, prüfen, ob sie ausnutzbar sind, und die zugrunde liegende Ursache beheben. Google berichtet, dass Carbon bei der Schwachstellensuche auf SEC-bench Pro 88,2 %, bei der Ausnutzung auf ExploitGym 54,8 % und bei der Erstellung von Codebehebungen auf Colliners CWE-bench 71,0 % erzielte. Der Anbieter berichtet außerdem, dass Carbon in Googles internen Benchmarks die Erfolgsrate von Argon bei der Generierung sicherer Codes mehr als verdoppelte. Carbon ist zunächst für eine Auswahl von Cybersicherheitsexperten verfügbar, whereby der Zugang über das Fairwind Program schrittweise auf vertrauenswürdige Partner ausgeweitet wird. Entwickler, Unternehmen und Verbraucher sollen später Zugang erhalten. Der Einführungspreis liegt bei 2 US-Dollar pro Million Eingabetokens und 10 US-Dollar pro Million Ausgabetokens, wobei zwischengespeicherte Eingaben um 95 % rabattiert werden. Anschließend sollen die Preise bei 4 beziehungsweise 20 US-Dollar liegen. Der nächste zu beobachtende Meilenstein ist, wie die ersten Cybersicherheitsexperten Carbon einsetzen und ob ein breiterer Zugang folgt. Laut Google wurde Carbon für langlebige agentische Workflows entwickelt und kann mehrere Tage lang laufen, während es komplexe, mehrstufige Entwicklungsaufgaben verfolgt.

[02:32] OpenAI stellt Modellergebnisse zu drei wissenschaftlichen Problemen vor

OpenAI hat Modellergebnisse zur Kakeya-Vermutung, zur Exponential Time Hypothesis und zur Quantenchromodynamik sowie eine Darstellung darüber veröffentlicht, wie akademische Forscher die Arbeit überprüfen und darauf aufbauen können.

Der nützliche Outcome besteht darin, dass Ergebnisse aus Mathematik, Informatik und Physik zugänglich sind, die von Modellen erstellt wurden. Forscher können die Arbeit untersuchen und daraus weitere Arbeiten entwickeln, sodass Modellausgaben zu Material für wissenschaftliche investigations werden, statt als Endprodukt zu verbleiben.

OpenAI positioniert akademische Gemeinschaften als aktive Mitwirkende bei der Überprüfung und Weiterentwicklung der Ergebnisse. Die nächste Probe liegt darin, ob diese Forscher die Arbeit verifizieren und in weiteren wissenschaftlichen Fortschritt ummünzen können.

[03:11] Retells mit OpenAI betriebene Sprachagenten erreichen 100 Mio. Anrufe pro Monat

OpenAI hat am 27. Oktober eine Fallstudie veröffentlicht, aus der hervorgeht, dass Retell OpenAI-Modelle für einen Sprachagentenbetrieb einsetzt, der jeden Monat 100 Millionen Anrufe bearbeitet. Retell berichtet, dass GPT-6 Astra die Sprachagenten-Benchmark des Unternehmens anführte, während Codex dem Unternehmen dabei half, einen annual revenue run rate von 1,6 Millionen US-Dollar pro Beschäftigtem zu erreichen.

Das nützliche Beispiel ist ein Sprachagentensystem im Produktionsmaßstab und keine kleine Demonstration. GPT-6 Astra führt Retells Benchmark an, und der Einsatz verarbeitet genügend monatliches Aufkommen, um 100 Millionen Anrufe zu einem aussagekräftigen operativen Messwert zu machen. Die Kennzahl des Umsatzes pro Beschäftigtem ergänzt das Ergebnis zur Modellleistung um ein wirtschaftliches Signal.

Für Entwickler, die Sprachagenten evaluieren, ist dies ein konkreter Referenzpunkt für den Umfang und die Ergebnisse eines mit OpenAI betriebenen Systems. Anrufvolumen und Umsatz pro Beschäftigtem sind die beiden Kennzahlen, die zu verfolgen sind, während Retell die Modelle weiter ausbaut.

[04:02] Anthropic trennt das Modell von den Aktionen des Agenten

Das Plattformteam von Anthropic verfügt über einen konkreten Ansatz, um Agenten steuerbarer zu machen: Das Modell, das Reasonings durchführt, wird von dem System getrennt, das handelt. In einem Interview mit Latent Space vom 27. Oktober beschrieben Katelyn Lesse und Angela Jiang die Einführung von Opus 5.5 sowie den Ausbau der Claude Platform durch verwaltete Agenten, deren Gehirn, Harness und Sandbox voneinander entkoppelt sind. Die Ausführungsebene ist durch Isolation, Schutzmechanismen für Zugangsdaten und Netzwerksteuerungen abgesichert. Langlebige Harnesses sind darauf ausgelegt, den Fortschritt über mehrere Kontextfenster hinweg aufrechtzuerhalten.

Für Entwickler unterstützt dies eine Agentenarchitektur, die weiterarbeiten kann, ohne dem Reasonings-Modell uneingeschränkte Kontrolle über Tools oder Zugangsdaten zu geben. Im Gespräch werden zudem Trainingsvorfälle von Schutzmaßnahmen im Produktivbetrieb getrennt. Außerdem werden Sicherheitsklassifikatoren und Modellrouting als Bestandteile des Plattformbetriebs behandelt.

Eine zentrale Frage für Teams, die dieses Muster übernehmen, lautet, ob seine Eindämmungsmechanismen und Mechanismen zur Fortschrittssicherung auch dann zuverlässig bleiben, wenn Agentenaufgaben länger andauern.

[04:57] ASRocks Radeon AI Pro R9700 zielt auf lokale Workstation-Inferenz

ASRock bringt die RDNA-4-Workstation-Plattform von AMD zu Entwicklern lokaler KI mit der Creator Radeon AI Pro R9700. Die Grafikkarte kombiniert 32 GB GDDR6-Speicher mit 640 GB/s Bandbreite und Unterstützung für FP8-Matrixberechnungen, einem Format mit geringerer Präzision, das Within eines festen Speicherbudgets mehr Modellparameter aufnehmen kann.

Im Zentrum steht der Navi-48-Prozessor von AMD mit 64 Compute Units, 128 KI-Beschleunigungskernen und einem Höchsttakt von 2,92 GHz. ASRock beziffert den Durchsatz dichter FP8-Matrizen mit 382,7 TFLOPS, bei Nutzung von Sparsity mit dem Doppelten. FP6- und FP4-Modelle werden in FP8 statt in ihren nativen Formaten verarbeitet. Ein praktisches Beispiel ist ein Modell mit ungefähr 30 Milliarden Parametern, das noch über einen gewissen VRAM-Reserven verfügt.

Das Design ist auf den Einsatz als Workstation ausgelegt. Es handelt sich um einen Dual-Slot-Blower mit den Maßen 271 × 111 × 39 Millimetern, und in einem Standard-ATX-System können bis zu vier Karten installiert werden. Linux-Nutzer können Soft-ECC manuell aktivieren, um zusätzliche Zuverlässigkeit zu gewährleisten. Die Karte zieht 300 Watt, was der Test als gut beherrschbar für ein Design mit Blower-Lüfter beschreibt.

Die Speicherkapazität ist die zentrale Einschränkung. Die R9700 verfügt über 32 GB, weniger als die 48 GB der Radeon Pro W7900 der vorherigen Generation. Die entscheidende Frage ist nun, wie sich ihre RDNA-4-Rechenverbesserungen bei kleinerem Speicherbudget auf die praktische Inferenz-Durchsatzleistung und Effizienz auswirken.

[06:16] NVIDIAs 4GB-Bolt-Modell ist für lokale Agenten-Stacks bestimmt

NVIDIA hat NVIDIA-Nemotron-3.5-Bolt-E4B-4GB veröffentlicht, ein quantisiertes Textmodell für lokale Sprach- und Geräteassistenten, interaktive Personas und eingebettete Benutzeroberflächen. NVIDIA erklärt, dass das Modell außerdem aus Gemma-4-E4B-it nachtrainiert wurde und für den Betrieb mit wenig Speicher und kurzer Zeit bis zum ersten Token ausgelegt ist. Das Modell ist ein Textmodell mit 8 Milliarden Parametern und 4 Milliarden effektiven Parametern, mit Q4_K_M-Präzision, bis zu 64K Token für Eingabe und Ausgabe, Denksteuerungen, einem Unterhaltungsmodus und Tool Calling. Zu seinen Steuerungsmöglichkeiten gehören ein- und ausgeschaltetes Denken, ein Laufzeit-Denkbudget und ein Unterhaltungsmodus, der knappere Antworten erzeugt. Es unterstützt Function-Style-Tool-Calling, einschließlich eines dokumentierten Musters zum Bestätigen eines ausstehenden Tool-Ergebnisses und Fortsetzen des Gesprächs, sobald das Ergebnis eingeht. NVIDIA stellt Download- und llama.cpp-Serveranweisungen sowie einen begleitenden DFlash Drafter für Speculative Decoding bereit. In NVIDIAs eigener Q4_K_M-Auswertungstabelle weist das Modell einen MultiChallenge-Score von 55,60 auf, gegenüber 39,36 für Gemma4 E4B-it. Laut NVIDIA wurden die Messungen unter einheitlichen Testbedingungen durchgeführt. Die Model Card gibt an, dass das Modell für kommerzielle und nichtkommerzielle Nutzung bereitsteht, und enthält Download- sowie llama.cpp-Serving-Befehle. Die Model Card warnt davor, dass eingeschränkte Token-Zuteilungen Gedankengänge mitten im Satz abschneiden können, weshalb eine aufgabenbezogene Evaluierung weiterhin notwendig sei. NVIDIA veröffentlichte NVIDIA-Nemotron-3.5-Bolt-E4B-4GB am 23. Oktober 2026 als allgemein verfügbares Modell. Der Herausgeber berichtet, dass Nemotron-3.5-Bolt-E4B-4GB in NVIDIAs Q4_K_M-Evaluierungen einen MultiChallenge-Score von 55,60 erzielte, während Gemma4 E4B-it einen Wert von 39,36 erreichte.

[07:39] US-Investitionen erweitern die Chipkapazität und schaffen eine Teststrecke für autonome Waffen

Das Weiße Haus hat eine Reihe industrieller Investitionen mit unmittelbaren Auswirkungen auf Chips, Comput-hardware und autonome Systeme erläutert. North Carolina erhält bis zu 1,5 Milliarden US-Dollar, um die Halbleiterproduktion auszuweiten, während Sibelco in Mitchell County die Produktion von hochreinem Quarz und damit verbundenen Materialien erweitert, die für Halbleiter unverzichtbar sind.

Die Regierung greift außerdem auf den Defense Production Act zurück, um 150 Millionen US-Dollar für eine Erweiterung der US-Raffineriekapazität bereitzustellen. Ziel ist es, die inländische Produktion von Diesel und Benzin zu erhöhen. In Montana richtet das Department of War eine neue Teststrecke für fortschrittliche Waffen und Technologien ein, darunter autonome Waffen sowie Fähigkeiten im Bereich Raum- und elektronischer Kriegsführung.

Für Entwickler ist die Halbleiterinvestition ein konkretes Signal für die vorgelagerte Branche: Mehr geplante Kapazitäten für Chips und wichtige Materialien könnten eine größere inländische Hardwarebasis ermöglichen. Die Teststrecke in Montana schafft einen eigenen Ort für die Bewertung autonomer Systeme und elektronischer Kriegsführung.

Beobachten sollte man, wie schnell die angekündigten Investitionen in betriebsbereite Anlagen in dem beschriebenen Umfang münden.

[08:38] Forschungsdigest: Gruppenspeicher kann die darin bewahrten Belege verzerren

Eine Gruppe von Sprachmodellen kann den Inhalt ihrer eigenen Diskussion verlieren, wenn ein Modell den Austausch in eine kurze Erinnerung komprimiert. Zwei naheliegende Regeln versagen auf unterschiedliche Weise. Die Auswahl der seltensten Behauptungen funktioniert manchmal, ist im Durchschnitt jedoch nicht besser als eine zufällige Auswahl. Die Auswahl von Behauptungen, die für die Entscheidung relevant erscheinen, kann sogar schlechter sein, weil auch plausible Ablenkungsmanöver thematisch passen. Die letzte entscheidende Instanz fügt eine weitere Verzerrung hinzu: sozialer Beweis, also die Tatsache, dass einer Tatsache mehr Gewicht gegeben wird, weil vielen Agenten die Aussage zugeschrieben wird. Werden diese Zuordnungen entfernt oder zufällig neu verteilt, während die Reihenfolge der Diskussion unverändert bleibt, steigt die Genauigkeit. Auch das vollständige Transkript kann schlechter abschneiden als gar keine Notizen. Das zeigt, dass die Komprimierung nicht automatisch das Problem darstellt; entscheidend ist, wie Belege gespeichert und dargestellt werden. Für einen Workflow, der die Forschung eines Panels in eine einzige Empfehlung überführt, lautet die praktische Konsequenz, die Balance unterstützender und ablenkender Belege im entstehenden Speicher zu prüfen, statt eine knappe Zusammenfassung als neutrale Aufzeichnung zu behandeln.

[09:43] Anthropic trainierte Claude mit illegal beschafften Büchern von Stanford-Professoren

Anthropic trainierte Claude illegal mit Büchern von Stanford-Professoren Anthropic trainierte Claude illegal mit Büchern von Stanford-Professoren Anthropic trainierte Claude illegal mit Büchern von Stanford-Professoren (Foto: JACK BERNARDO/The Stanford Daily) Veröffentlicht am 27. Oktober 2026, 2:46 Uhr, zuletzt aktualisiert am 27. Oktober 2026, 3:19 Uhr. Ein Bundesrichter entschied im Mai 2026 in einer Klage, dass der KI-Riese Anthropic illegal die Werke von mehr als zehn Stanford-Professoren aus_scrapte und pirate, um seine Claude-Modelle zu trainieren. Anthropic hatte Claude zuvor mit illegal beschafften Texten der Professoren Tobias Wolff, Abraham Verghese, Chang-Rae Lee, Daniel Mason, Hayagreeva Rao und Myra Strober trainiert. In Bartz v. Bei einem Mechanismus handelt es sich um eine rechtliche oder politische Grenze, nicht um eine API-Änderung. Die belegten Fakten definieren, was vorgeschlagen, entschieden oder erklärt wurde, ohne daraus allgemeines Recht zu machen. Entwickler sollten die konkrete Regel, das Urteil oder die Änderung des Zugriffs verfolgen und ein Produkt nicht aufgrund einer Schlagzeile allein ändern.

[10:37] Forschungsdigest: EnvSched soll Agenten-Trainingsläufe nützlicher machen

Das Training eines Sprachagenten kann schnell teuer werden, da jeder Trainingslauf beziehungsweise Rollout unterschiedliche Tools, Zustände, Übergänge und Erfolgskontrollen einbeziehen kann. EnvSched ist ein Forschungs-Scheduler, der darauf ausgelegt ist, eine begrenzte Zahl solcher Läufe nützlicher zu machen.

Die zentrale Erkenntnis des Papers lautet, dass das gemeinsame Scheduling von Aufgaben und ihren Umgebungen die Informationen in jedem Trainingsbatch verbessern kann. EnvSched lernt aus der Historie der Rollouts, bevorzugt Aufgaben, bei denen wahrscheinlich aussagekräftige Unterschiede in der Belohnung sichtbar werden, und verteilt die Arbeit auf Umgebungen und Interaktionsmuster, denen bislang weniger Aufmerksamkeit geschenkt wurde.

Dazu organisiert EnvSched Aufgaben-Umgebungs-Paare in einem Graphen. Die Verbindungen erfassen entweder Beziehungen innerhalb einer Umgebung, etwa gemeinsame Tools und Verifikationsstrukturen, oder umfassendere Ähnlichkeiten bei der Ausführung und den Belohnungen. Anhand historischer Rollout-Informationen wird geschätzt, wie stark jede Aufgabe voraussichtlich variieren wird. Umgebungsquoten und eine Ähnlichkeitsstrafe begrenzen anschließend Wiederholungen.

Die praktische Konsequenz ist einfach: Bei einem festen Trainingsbudget können ein Team von Agenten seine Läufe dort bündeln, wo sie am ehesten gutes von schlechtem Verhalten unterscheiden, statt einen zu großen Teil des Budgets für redundante Erfahrungen zu verbrauchen.

[11:45] Greptile nutzt GPT-6 Astra zum Testen von Software-Workflows

Greptile erweitert mit GPT-6 Astra die Fehlererkennung über das Code-Review hinaus. Das Unternehmen setzt Astra ein, um Benutzer-Workflows zu testen und seinem Review-Produkt damit die Möglichkeit zu geben, zu untersuchen, wie sich eine Anwendung in der Praxis verhält, statt sich ausschließlich auf den vorgeschlagenen Code zu konzentrieren.

Greptile nutzt Daybreak außerdem, um die Sicherheit zu stärken. Dadurch erhält derselbe workfloworientierte Ansatz eine sicherheitsbezogene Dimension, die Teams dabei unterstützen soll, Schwachstellen auch nach den Bereichen zu erkennen, in denen Entwickler oder Reviewer sie bei einer manuellen Prüfung bemerken würden.

Die Ankündigung hebt außerdem die Rolle von Codex bei der Reduzierung von Nacharbeit hervor. Indem Greptile Codehilfe in den Prozess integriert, adressiert das Unternehmen Aufgaben, die andernfalls nach der Identifizierung von Problemen erneut ausgeführt werden müssten.

Das praktische Ergebnis ist ein umfassenderer Qualitätsprüfungs-Workflow: Astra testet das nutzerseitige Verhalten, Daybreak unterstützt die Sicherheit, und Codex hilft dabei, Korrekturen zu begrenzen. Für Entwickler ist das nächste Signal, auf das zu achten ist, in welchem Umfang diese Funktionen wiederholtes Debugging und Nacharbeit in realen Anwendungen reduzieren.

[12:43] CodeRabbit nutzt GPT-6.1 Sol für die Sicherheitsprüfung von Codebasen

CodeRabbit nutzt GPT-6.1 Sol, um Sicherheitsrisiken in komplexen Codebasen zu untersuchen. Sein Security-Agent unterstützt Entwickler dabei, Ergebnisse und vorgeschlagene Korrekturen zu prüfen, und verbindet automatisierte Untersuchungen mit der menschlichen Bewertung möglicher Schwachstellen und Behebungsmaßnahmen.

Die praktische Veränderung besteht darin, dass das Modell in einen Workflow zur Sicherheitsprüfung von Codebasen integriert wird. CodeRabbit kann Risiken untersuchen und vorgeschlagene Korrekturen präsentieren, während Entwickler die Ergebnisse prüfen, bevor sie entscheiden, was geändert werden soll.

Für Entwickler ist das Muster klar: eine codebaseweite Sicherheitsuntersuchung mit vorgeschlagener Behebung kombinieren und gleichzeitig den Entwickler für die Prüfung beider Aspekte verantwortlich lassen. Entscheidend wird sein, wie zuverlässig sich die Ergebnisse und vorgeschlagenen Korrekturen des Agenten in realen Sicherheitsprüfungen bewähren.

[13:23] Hermit bringt KI-Agenten bei, ohne ihren Kern zu ersetzen

Infini-AI-Lab hat Hermit veröffentlicht, ein auf Apache-2.0 basierendes Open-Source-Framework zur Anbindung von Harness-Adaptern für KI-Agenten. Die zentrale Idee ist einfach: Anstatt das Modell oder den Harness, der den Agenten ausführt, zu verändern, trainiert Hermit anhand von Feedback zu abgeschlossenen Aufgaben eine externe Ebene.

Diese Ebene enthält Anweisungen, Fähigkeiten, Speicher und Tools. Entwickler können das Verhalten eines Agenten daher verbessern, indem sie ihn durch Aufgaben-Feedback unterrichten, während das zugrunde liegende Modell und der Harness unverändert bleiben.

Diese Trennung ist für Teams wichtig, die bereits eine Agentenumgebung haben, die sie nicht ersetzen möchten. Sie können über den Adapter an den Anweisungen des Agenten, seinem gespeicherten Wissen und seinem Tool-Verhalten arbeiten, ohne das Modell selbst zu verändern.

Der entscheidende Punkt ist, ob Hermit diese externe Ebene weiterhin anhand von Feedback zu Aufgaben verbessern kann, ohne Änderungen am Kernmodell oder am Harness des Agenten zu erfordern.

[14:14] Legora bringt Agenten in die rechtliche Vertragsanalyse

Legora entwickelt ein agentenorientiertes Betriebssystem für die Rechtsarbeit. In einem von OpenAI veröffentlichten Profil gibt das Unternehmen an, dass es OpenAI-Modelle, ChatGPT und Codex einsetzt, um rechtliche Workflows zu beschleunigen und die Vertragsanalyse zu erweitern.

Die unmittelbare Auswirkung ist eine höhere Kapazität für rechtliche Aufgaben, wobei die Vertragsanalyse ein konkretes Beispiel dafür ist, wo KI ein größeres Arbeitsvolumen bewältigen kann. Das erklärte Ziel von Legora ist es, Anwälten die Zeit für wertvollere Aufgaben zu geben, statt sie Routineanalysen zu widmen.

Der nächste nützliche Beleg wird sein, wie weit die Vertragsanalyse in der Praxis expandiert und wie sich dies auf die Zeiteinteilung der Anwälte auswirkt. Für Entwickler zeigt Legora, dass Modelle, Gesprächstools und Coding-Agenten围绕 einen professionellen Workflow kombiniert werden können, statt als isolierte Funktionen bereitgestellt zu werden.