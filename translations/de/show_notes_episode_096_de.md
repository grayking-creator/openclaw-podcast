Episoden 096 — 31. Juli 2026

[00:00] Episodeneinstieg

Agent Stack Release-Auswertung: Hermes Agent v2026.7.30 dominiert den Tag: v2026.7.30 bringt konkrete Änderungen für die Oberflächen, mit denen Entwickler täglich arbeiten, mit den Details unten. Ebenfalls heute im Programm: Gemini Robotics 2 bringt Ganzkörper-Intelligenz in Roboter, GitHub Models eingestellt: Playground, API und BYOK weg, Moonshots Kimi K3 erscheint als quantisierter lokaler KI-Download, plus der Rest eines dichten Nachrichtenzyklus rund um Modelle, Tools und Infrastruktur. Jede Geschichte erhält dieselbe Behandlung — was ausgeliefert wurde, der darunterliegende Mechanismus, und was sich für arbeitende Entwickler ändert.

[02:00] Agent Stack Release-Auswertung: Hermes Agent v2026.7.30

Eine stabile Version ist in diesem Zyklus erschienen und formt, wie agentische Anwendungsrahmen gerade jetzt zusammengestellt werden. Hermes Agent v2026.7.30: Veröffentlichungsdatum: 30. Juli 2026 > Patch-Version. Dieses Tag fasst die ~1.000+ zusammengeführten PRs seit v0.19.0 in einer stabil getaggten Version für downstream-Konsumenten zusammen (Docker-Images, gehostete Deployments, Neuinstallationen). Seit (v0.19.0, 20. Juli): ~2.789 Commits · ~4.748 geänderte Dateien · ~442.000 Einfügungen · ~392.300 Löschungen auf main. Dieses Fenster wird von Fehlerbehebungs- und Bereinigungswellen über das Gateway, das Voice-Subsystem, die Desktop-App und den Installer dominiert, plus fortlaufender Plattformarbeit (Buzz/Nostr-Kanal, FLUX3-Videogenerierung und -Bereitstellung, Telegram-Medienzuverlässigkeit, Voice-Mode-Regressionen). Die vollständigen kuratierten Release-Notes für dieses Fenster werden mit v0.20.0 ausgeliefert, das alles von v0.19.0 an dokumentieren wird — Highlights, Feature-Bereiche und vollständige Mitwirkenden-Credits. Nichts in diesem Fenster wird übersprungen. hermes update curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash Vollständiger Änderungsverlauf: [..v2026.7.30](https://github.com/NousResearch/hermes-agent/compare/..v2026.7.30) Auf der API- und Runtime-Ebene ändern diese Änderungen das, was Entwickler standardmäßig konfigurieren und erwarten können; die Frage für jeden Produktions-Agent-Workflow ist, ob die neuen Standardeinstellungen den Pfad verbessern oder unterbrechen, den Sie diese Woche ausgeführt haben. Die vollständigen Release-Notes für jeden Harness — einschließlich der Deployment-Anleitung, der Liste der zusammengeführten Pull Requests und der Mitwirkenden-Credits — sind über die primäre Quelle verlinkt, und der Änderungsverlauf-Kontext für jedes Tag ist das, worüber Entwickler ihre aktuelle gepinnte Version diffen sollten, bevor sie den Standard in der Produktion umstellen. Hermes Agent v2026.7.30, veröffentlicht am 30.07.2026, ist ein stabiles Tag: Pinnen Sie ihn explizit, anstatt einem beweglichen Kanal zu folgen, spielen Sie eine repräsentative Agent-Sitzung gegen den neuen Build, und vergleichen Sie Tool-Call-Latenz, Reconnect-Verhalten und Genehmigungsabwicklung mit der aktuell laufenden Version, bevor Sie den neuen Standard übernehmen.

[02:42] Gemini Robotics 2 bringt Ganzkörper-Intelligenz in Roboter

DeepMind hat am 30. Juli Gemini Robotics 2 veröffentlicht und das Werk als „Ganzkörper-Intelligenz" für Roboter bezeichnet. Die Hauptbehauptung ist, dass ein System nun Wahrnehmung, Planung und Werkzeugnutzung über einen gesamten Roboter-Körper hinweg bewältigen kann, anstatt Arme, Greifer und Basisbewegung als separate Probleme zu behandeln. Die Veröffentlichung umfasst tatsächlich zwei Modelle: Gemini Robotics 2 und einen Begleiter namens Gemini Robotics ER 2. Laut dem Blog ist ER 2 die Variante, die für Reasoning, Zusammenarbeit und die Lösung realer Aufgaben entwickelt wurde. DeepMind hat drei konkrete Bereiche hervorgehoben, in denen die neuen Modelle über frühere Arbeiten hinausgehen. Erstens, Video-Verständnis: Die Modelle können lange Demonstrationen beobachten und die wichtigen Schritte herausfiltern. Zweitens, Werkzeug-Orchestrierung: Anstatt nur seine eigenen Arme zu bewegen, kann der Roboter entscheiden, ein anderes Werkzeug zu holen oder einen separaten Agenten aufzurufen. Drittens, Multi-Roboter-Zusammenarbeit: Mehrere Roboter können eine Aufgabe aufteilen, ohne dass ein Mensch jeden Übergabepunkt choreografiert. Der DeepMind-Post rahmt die Arbeit um reale Aufgaben ein, anstatt um Tabletop-Pick-and-Place. Der Hacker-News-Thread erreichte innerhalb eines Tages einen Score von 561, was für ein Robotik-Thema ungewöhnlich hoch ist und darauf hindeutet, dass die Entwickler-Community diesmal echte Arbeit leistet.

[03:56] GitHub Models eingestellt: Playground, API und BYOK weg

GitHub Models ist eingestellt. Ab dem 30. Juli 2026 sind der Playground, der Modellkatalog, die Inferenz-API und die Bring-Your-Own-Key-Option für keinen Kunden mehr verfügbar.

Für Entwickler ist die praktische Auswirkung straightforward. Wenn Sie GitHub Models als schnellen Weg genutzt haben, verschiedene Modelle im Browser auszuprobieren, ist dieser Einstiegspunkt weg. Wenn Sie den GitHub Models Inferenz-Endpunkt aus Ihrem Code aufgerufen haben, ist dieser Endpunkt weg. Wenn Sie externe Provider-Schlüssel durch den BYOK-Flow verdrahtet haben, damit Sie Anfragen von einer einzelnen GitHub-seitigen Oberfläche an OpenAI, Anthropic oder andere weiterleiten konnten, ist dieser Übergabepunkt ebenfalls weg.

Die Einstellung ist total, nicht partial. GitHub fährt nicht ein Stück herunter, während der Rest am Leben bleibt; Playground, Katalog, Inferenz und BYOK verschwinden alle zusammen. Kunden, die GitHub Models als dünne Komfortschicht über externe Provider behandelt haben, müssen jetzt direkt mit diesen Providern sprechen.

Der vernünftige nächste Schritt ist, jede aktive Nutzung zu migrieren. Direkte Provider-SDKs und API-Schlüssel ersetzen die Inferenz- und BYOK-Pfade. Modell-Durchsuchen move zu den eigenen Katalogen jedes Providers oder zu Verzeichnissen von Drittanbietern. Prototyping-Oberflächen wie der OpenAI Playground, die Anthropic Console oder anbieterspezifische Chat-UIs decken den Playground-Anwendungsfall ab.

Eine Sache zum Beobachten: Der Änderungsverlauf-Post lässt seine Kundenbereichsklausel abgeschnitten, daher ist unklar, ob Kunden mit bezahlten Stufen oder Enterprise-Kunden einen Fortführungsweg oder einen Bestandsschutz erhalten. Wenn Sie sich auf GitHub Models für einen Produktions-Workflow verlassen haben, prüfen Sie, ob Ihre bestehenden Provider-Beziehungen es Ihnen ermöglichen, die Aufrufe zu übernehmen, ohne neu zu architectieren.

[05:32] Moonshots Kimi K3 erscheint als quantisierter lokaler KI-Download

Ein neues Kimi K3-Modell von Moonshot AI trendet diese Woche auf Hugging Face, und es ist die lokale KI-Community, die es sich schnappt. Unsloth hat am 27. Juli eine GGUF-Version von Moonshots Kimi K3 veröffentlicht, und innerhalb weniger Tage hatte es 36.000 Downloads mit 218 Likes erreicht.

Was diesen Drop bemerkenswert macht, ist die Kombination von zwei Dingen: Es ist multimodal — es akzeptiert sowohl Bilder als auch Text zusammen und produziert Text als Antwort — und es wird als GGUF verteilt, das Dateiformat, das Tools wie Ollama, llama.cpp und LM Studio verwenden, um quantisierte Gewichte auf Consumer-Hardware zu laden. Also ist dies keine Cloud-API; es ist etwas, das Sie herunterladen und lokal auf einem Laptop oder einer Heim-GPU-Rig ausführen können.

Diese Kombination war im Open-Weight-Bereich relativ selten. Die meisten lokalfreundlichen Modelle sind immer noch rein textbasiert, daher gibt ein quantisiertes multimodales Release von einem großen Lab wie Moonshot Entwicklern etwas Neues für Offline-Workflows. Screenshots in einen Chat eingeben, gescannte Dokumente parsen oder einen sehfähigen Assistenten betreiben, ohne Daten an einen Drittanbieter-Server zu senden, wird alles praktikabler.

Das Modell ist auf dem Hugging Face Hub als image-text-to-text aufgelistet, mit Tags, die die Transformers-Architektur, GGUF-Verpackung und Konversationstuning bestätigen. Es ist eine Basis-Modell-Quantisierung von Moonshots Kimi K3, verteilt unter einer Lizenz, die als „other" getaggt ist — also sollte jeder, der kommerziell darauf aufbauen möchte, zuerst die Bedingungen prüfen.

Für Leute, die bereits lokale Stacks betreiben, ist der Schritt straightforward: Verweisen Sie Ollama oder llama.cpp auf das unsloth/Kimi-K3-GGUF-Repo und sehen Sie, wie es Bild-Eingaben verarbeitet. Die Download-Zahlen deuten darauf hin, dass diese Woche plenty andere genau das tun.

[07:13] Idle GPUs kosten Sie Geld — Ein neuer Blick auf Fleet Management

Ein neuer Beitrag im Hugging Face Blog, veröffentlicht am 30. Juli von Dharma-AI, verwendet eine Luftfahrtmetapher, um ein Budgetargument vorzubringen: Eine ungenutzte GPU ist wie ein am Boden stehendes Flugzeug – ein abschreibungsintensives Gut, das gleich viel kostet, ob es fliegt oder auf dem Rollfeld steht.

Der Rahmen ist wichtig, weil KI-Teams dazu neigen, ihr Budget um die gekaufte rohe Rechenleistung zu planen, nicht um die tatsächlich genutzte. Die Hauptbehauptung des Beitrags ist, dass Leerlaufzeit für Organisationen, die mehr als eine Handvoll Beschleuniger betreiben, still und leise zur dominanten Kostenquelle geworden ist, weil GPUs stündlich abschreiben, unabhängig von der Arbeitsbelastung.

Für Entwickler ist die Erkenntnis eher konzeptioneller als mechanischer Natur. Das verfügbare Material dokumentiert keine spezifischen Planungssysteme, Rückgewinnungsrichtlinien oder Nutzungs-Benchmarks, daher ist der nützliche Beweis die Rahmung selbst: Behandeln Sie Beschleunigerkapazität als verwaltete Flotte, messen Sie die Nutzung und gestalten Sie Aufträge, die Lücken füllen, anstatt Hardware unbegrenzt zu reservieren.

Was als nächstes zu beobachten ist: Ob Dharma-AI mit konkreten Werkzeugen oder Fallstudien nachlegt, die dem Leerlaufkostenargument Zahlen verleihen.

[08:16] Jetson als das 'Clutch'-Accessoire: Sarah Guo rückt Edge-KI ins Rampenlicht

NVIDIA richtete diese Woche einen Werbescheinwerfer auf seine Jetson Edge-AI-Plattform, und das Unternehmen griff zu einer Modemetapher. Der am 28. Juli auf dem NVIDIA-Blog unter der Überschrift "Leistungsstarke Rechenleistung so kompakt, dass sie clutch ist – Erstellen Sie KI überall mit NVIDIA Jetson" veröffentlichte Beitrag zeigt Investorin Sarah Guo in einem kurzen Video, das das kompakte Entwicklerkit als „Clutch" rahmt – das kleine, stilvolle Accessoire, das in Ihre Hand passt und trotzdem Blicke auf sich zieht.

Guo leitet Conviction, eine KI-native Venture-Capital-Firma, und co-moderiert den No Priors Podcast. Im Video hebt sie hervor, wie Jetson als Plattform für Edge-KI-Entwicklungen funktioniert.

Für Entwickler ist die zugrundeliegende Idee straightforward: „Edge" bedeutet, dass das Modell auf dem Gerät selbst läuft, anstatt einen entfernten Server anzupingen. Das ist es, was einem Roboter, einer Kamera, einer Drohne oder einem Handheld-Gerät ermöglicht, Inferenz lokal zu verarbeiten. Die Rahmung hier ist weniger über rohe Benchmark-Zahlen und mehr darüber, wie eine Investorin-Operatorin wie Guo über Edge-KI spricht, wenn sie versucht, andere Gründer davon zu überzeugen, dass es ein echtes Einsatzziel ist, keine Forschungsdemo.

Der Beitrag selbst ist arm an technischen Details – keine neue SKU, keine SDK-Veröffentlichung, keine Preisgestaltung, kein Änderungsprotokoll jeglicher Art. Das Interessante ist der Bote: Eine Risikokapitalgeberin, die KI-native Unternehmen unterstützt, empfiehlt eine spezifische Hardwareplattform in NVIDIAs eigenem Marketing. Das ist ein Signal dafür, wo Kapital meint, dass Edge-KI als nächstes hingeht, und es lohnt sich ein schnelles Anschauen, wenn Sie Cloud-APIs gegen On-Device-Inferenz für einen zukünftigen Build abwägen.

[09:55] OpenAI skizziert sein Playbook für verantwortungsvolle KI für Europa

Am 31. Juli veröffentlichte OpenAI einen Beitrag mit dem Titel 'Verantwortungsvolle KI in Europa voranbringen', in dem dargelegt wird, wie seine aktuellen Praktiken verantwortungsvolle KI-Governance auf dem Kontinent unterstützen. Der Beitrag gliedert die Arbeit in vier Bereiche: Sicherheit, Schutz, Transparenz und Provenienz. OpenAI sagt, diese Bemühungen werden weiterhin parallel zum EU AI Act laufen, während das Gesetz durch seine Implementierungsphasen geht.

Für Entwickler ist das praktische Signal, dass Provenienz – das heißt die Metadaten, die KI-generierte Bilder und Texte markieren – und Transparenz-Offenlegungen zunehmend Teil der europäischen Baseline sind. OpenAI präsentiert seine bestehenden Praktiken als das Gerüst für diese Compliance, anstatt in diesem Beitrag neue, für Europa spezifische Verpflichtungen einzuführen. Das Stück positioniert die Arbeit als ein kontinuierliches Programm, das die Einführung des AI Act verfolgt.

Der EU AI Act wird über die Zeit eingeführt, wobei verschiedene Verpflichtungen zu verschiedenen Zeitplänen in Kraft treten. Der Beitrag von OpenAI signalisiert fortlaufende Investitionen in die Ausrichtung seiner Sicherheits- und Schutz-Offenlegungen an diese Verpflichtungen, wenn sie in Kraft treten. Er weist auch auf Transparenz und Provenienz als Bereiche hin, in denen europäische Nutzer mehr Einblick erwarten können, wie KI-generierte Inhalte identifiziert und gekennzeichnet werden.

Was als nächstes zu beobachten ist: Wenn die Bestimmungen des AI Act für höheres Risiko in Kraft treten, erwarten Sie konkretere Dokumentationsanforderungen rund um Provenienz, Modelldokumentation und Sicherheits-Offenlegungen für jedes System, das auf dem europäischen Markt eingesetzt wird.

[11:18] Forschungsübersicht: PhiZero baut eine 'Physikalische Sprache' zur Vorhersage, wie sich die Welt bewegt

PhiZero ist ein neues Forschungsmodell, das vorhersagt, wie sich die Welt verhält, indem es eine physikalische Sprache erlernt – ein kompaktes diskretes Vokabular von Zustandsänderungen – anstatt rohe Videopixel vorherzusagen. Bestehende Weltmodelle neigen dazu, zukünftige Frames direkt zu rendern, was die zugrunde liegende Physik in einem hochdimensionalen visuellen Prädiktor vergräbt. Die Autoren von PhiZero argumentieren, dass Menschen etwas anderes tun: Wir beobachten, abstrahieren die Regeln der Bewegung und speichern diese Regeln in sprachähnlichen Repräsentationen, über die wir nachdenken können. PhiZero versucht, diesen Trick zu reproduzieren, indem es physikalische Tokens aus Videoerfahrungen in freier Wildbahn erlernt und dann diese Tokens verwendet, um Weltzustände vorzurollen. Die praktische Hoffnung ist ein Modell, das plant und über Ergebnisse nachdenkt wie eine Person und nicht wie ein Videogenerator. Es ist ein Forschungspreprint, kein Produkt, daher ist die Erkenntnis die Idee: Diskrete Tokens für Physik könnten ein nützlicheres Substrat als Pixel für Weltmodelle sein.

[12:13] Forschungsübersicht: Frontis-MA1: KI trainieren, um den Prozess des KI-Aufbaus zu verbessern

Ein Team testet, ob KI den Prozess des KI-Aufbaus sinnvoll verbessern kann – und veröffentlicht die Sandbox, damit jeder zuschauen kann. Das Paper stellt Frontis-MA1 vor, ein 35-Milliarden-Parameter-Modell, das als Meta-Evolutions-Agent für maschinelles Lernen nachtrainiert wurde. Die Forscher bauten OpenMLE, einen offenen Stack, der ML-Engineering in ein messbares Spiel mit Ausführungsfeedback verwandelt.

OpenMLE hat drei Schichten. OpenMLE-Gym führt überprüfbare Aufgabenumgebungen aus, in denen vorgeschlagene Änderungen tatsächlich ausgeführt werden. OpenMLE-RL bewältigt Operator-Lernen – dem Modell beibringen, wie es Bearbeitungen und Suchen steuert. OpenMLE-Evo führt Langzeit-Suche durch, damit sich Verbesserungen kumulieren können. Frontis-MA1 sitzt oben und schlägt ML-Engineering-Änderungen vor und sieht, welche tatsächlich funktionieren.

Die Hauptüberschrift ist nicht, dass KI sich selbst verbessert hat – es ist, dass rekursive Selbstverbesserung jetzt ein konkretes, offenes Testbed hat. Die meiste vorherige Arbeit blieb theoretisch oder lebte hinter geschlossenen Demos; hier sind Gym, Trainingsschleife und Suchgeschirr alle öffentlich, sodass andere Labore dasselbe Setup wiederholen oder erweitern können. Das Paper trending auf HuggingFace's täglichem Feed.

[13:15] Eine Tour durch den Stammbaum der DeltaNet Attention-Varianten

Doubleword hat einen Blog-Beitrag veröffentlicht, der die DeltaNet-Familie der linearen Attention-Varianten nachverfolgt und argumentiert – wie der Titel sagt –, dass Kimi Delta Attention eine natürliche Erweiterung ist, die ein sorgfältiger Leser selbst hätte ableiten können. Der Beitrag wurde am 28. Juli 2026 auf Hacker News veröffentlicht, löste eine Diskussion mit 297 Punkten aus, die aktiv geblieben ist, und tauchte auch im AI-Tag von Lobsters auf.

Der Beitrag rahmt das Feld als Stammbaum ein, anstatt als Haufen unabhängiger Tricks. Seine zentrale Behauptung ist, dass neuere Attention-Varianten weniger exotisch wirken, sobald man ihre Vorgänger nebeneinanderstellt, und dass das Verfolgen der Abstammung genügt, um vorherzusagen, wohin die nächste wahrscheinlich gehen wird.

Warum es jetzt wichtig ist: Frontier-Modell-Ankündigungen werden weiterhin mit Attention-Mechanismen ausgeliefert, die beim ersten Durchlesen wie ein Glaubenssprung wirken, und der praktische Mehrwert für Ingenieure ist, dass die Abstammung mehr bedeutet als jedes einzelne Paper. Den Stammbaum zuerst zu lesen, verändert, wie jede neue Variante ankommt.

Für Entwickler, die wirklich verstehen wollen, was in Modellen wie Kimi läuft, ist der Beitrag ein nützlicher Einstieg. Es ist ein Wochenendprojekt, keine Forschungsarbeit, und die Hacker News- und Lobsters-Diskussionen dazu liefern zusätzlichen Kontext.

[14:31] Copilot Code Review's Agent Skills und MCP-Support erreichen GA

GitHub hat die Agent-Skills und MCP-Server-Unterstützung von Copilot Code Review am 29. Juli zur allgemeinen Verfügbarkeit gebracht. Beide Funktionen stehen nun allen Copilot Pro, Pro+, Business- und Enterprise-Nutzern offen, nachdem sie die öffentliche Vorschau verlassen haben.

Der Changelog-Beitrag enthält wenige Details. MCP – das Model Context Protocol – ist der Standardweg für KI-Assistenten, sich mit externen Tools und Datenquellen zu verbinden. Der Beitrag definiert nicht, was „Agent-Skills" in diesem Kontext bedeutet, oder listet auf, welche Skills gebündelt sind. Er legt auch keine spezifischen MCP-Integrationen, Verhaltensänderungen oder Unterschiede zur Vorschau dar.

Für Entwickler auf den genannten kostenpflichtigen Stufen ist die Änderung, dass diese Funktionen produktionsreif sind, anstatt Vorschau. Copilot Free wird in der Einführung nicht erwähnt. Der ehrliche nächste Schritt ist zu beobachten, wie Teams sie tatsächlich konfigurieren, sobald sie verfügbar sind, aber die Ankündigung selbst ist dünn genug, dass jeder, der eine Einführung plant, in die GitHub-Dokumentation einsteigen muss, anstatt sich auf den Changelog zu verlassen.

[15:33] MCP's Spezifikation vom 2026-07-28 wird zustandslos und verspricht keine plötzlichen Entfernungen

Das Model Context Protocol, der offene Standard, der es KI-Assistenten ermöglicht, sich in externe Tools und Datenquellen einzustecken, erhielt am 30. Juli ein Spezifikationsupdate. Die wichtigste Änderung: Die Transportschicht wird zustandslos, was bedeutet, dass Server keinen Sitzungszustand zwischen Client-Anfragen beibehalten müssen. Daneben hat das Projekt eine neue Richtlinie angenommen, die verhindert, dass Funktionen ohne Vorwarnung entfernt werden.

In einfachen Worten bedeutet zustandslos, dass jede Anfrage für sich steht, anstatt von einer gespeicherten Sitzung auf dem Server abhängig zu sein. Für Entwickler, die MCP-Server betreiben, verlagert das den Entwurf hin zu einfacheren, vorhersehbareren Verbindungen – und ebenso wichtig, es entfernt eine Klasse von Fehlermodi, die aus abgebrochenen oder verlorenen Sitzungszuständen entstehen.

Die Deprecation-Richtlinie ist der ruhigere Teil der Veröffentlichung, trägt aber eigenes Gewicht. Protokollfunktionen durchlaufen nun einen dokumentierten Deprecation-Zyklus mit Vorankündigung, bevor sie entfernt werden können, was Server- und Client-Autoren Zeit zur Migration gibt. Es ist die Art von Vorhersagbarkeitsversprechen, die Webstandards zur Ruhe kommen ließ, und es beantwortet direkt eine echte Sorge von jedem, der heute in MCP-Integrationen investiert.

Das Update wurde am 30. Juli auf dem MCP-Blog veröffentlicht und zog schnell Aufmerksamkeit auf Hacker News auf sich, wo es einen Score von 127 erreichte.

[16:52] avatarin liefert 24/7-Einzelhandels-Sprachagent mit GPT-Realtime

avatarin hat OpenAI's GPT-Realtime als 24/7-Mehrsprach-Sprachagent für Kunden bei Yamada Denki, einem japanischen Elektronikhändler, eingesetzt. Kunden können einfach hinzutreten und Fragen in ihrer eigenen Sprache stellen, und der Assistent antwortet in Echtzeit.

Die ersten zwei Wochen lieferten beeindruckende Zahlen: 30.000 Menschen nutzten den Agenten, und 92% der Umfrageantworten waren positiv. Für einen Sprachassistenten, der im Einzelhandel im großen Maßstab in einer belebten Umgebung eingesetzt wird, ist das ein bedeutsames erstes Signal, dass Echtzeit-Sprachmodelle unter echtem Verkehr bestehen können.

GPT-Realtime ist OpenAI's Sprach-zu-Sprach-Modell, was bedeutet, dass Audio rein und Audio raus kommt, ohne einen separaten Texttranskriptionsschritt dazwischen. Dieser direkte Sprachpfad macht ein flüssiges Hin-und-Her-Gespräch möglich, und es ist dieselbe Fähigkeitsfamilie, die avatarin nun auf eine hochvolumige Einzelhandelsarbeit ausgerichtet hat.

Für Entwickler ist die Geschichte ein konkreter Datenpunkt, keine Feature-Ankündigung. Ein Sprachagent, der 30.000 Live-Interaktionen mit Einkäufern mit überwältigend positivem Feedback überstanden hat, ist näher an Produktionsreife als an Demo-Ware. Mehrsprachige Abdeckung und Rund-um-die-Uhr-Verfügbarkeit sind offensichtliche Differenzierungsmerkmale für einen Einzelhandelseinsatz, und beides scheint zu funktionieren.

Eine Sache, die es zu beobachten gilt: ob avatarin und Yamada Denki den Scope des Agenten über Produktfragen hinaus auf Retouren, Beschwerden oder Upsells ausweiten, wo Gespräche schwieriger werden und die Zufriedenheitszahlen schwerer zu halten sein werden.

[18:17] Google DeepMind bringt drei physische KI-Modelle für Ganzkörpersteuerung, Geschicklichkeit und Multi-Roboter-Zusammenarbeit auf den Markt

Google DeepMind hat Gemini Robotics 2 veröffentlicht, die Intelligenzschicht für seine nächste Roboter-Generation. Die Veröffentlichung umfasst drei Modelle: ein Vision-Sprache-Aktions-Modell für die Ganzkörper-Steuerung von Humanoiden, Gemini Robotics ER 2 für verkörpertes Reasoning und Aufgaben-Orchestrierung, sowie ein On-Device VLA, das sich in wenigen Stunden an neue Roboter-Körper anpasst. Ein Checkpoint steuert Apptronik Apollo 2 und eine Franka Duo. Nur ER 2 ist öffentlich verfügbar. Der Beitrag Google DeepMind Ships Three Physical AI Models For Whole Body Control, Dexterity And Multi Robot Collaboration erschien zuerst auf MarkTechPost. Die Primärquelle unterstützt die oben beschriebene spezifische Produkt- oder Workflow-Änderung; sie unterstützt keine breiteren Behauptungen über Leistung, Kompatibilität oder Bereitstellung. Testen Sie die quellengestützte Änderung anhand eines echten Workflows, bevor Sie sich darauf verlassen.