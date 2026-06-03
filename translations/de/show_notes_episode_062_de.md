Codex `rust-v0.136.0` führt EP062 als stabile CLI-Version vom 1. Juni an, gefolgt von Stanfords viralen KI-Agent-Richtlinien, OpenAI auf AWS Bedrock und einem von YC unterstützten GPU-Effizienzprojekt. Das Project Radar umfasst Agent-Betriebssysteme für Hardware, Terminal-Kontextdateien und physische Agent-Scheduler.

[00:00] Eröffnung: CLI-Releases, institutionelle Richtlinien und Cloud-Verteilung

Die nützliche Spur für EP062 ist eine Mischung aus CLI-Tools, institutioneller Validierung und realer Infrastruktur. Codex `rust-v0.136.0` ist das stabile Release, das bei TUI-Diagnosen, App-Server-Lebenszyklus, Hook-Scoping und SDK-Verbesserungen den Ausschlag gab. Stanfords CS336 Agent-Richtliniendokument ist die unerwartete Geschichte – ein akademischer Kurs, der KI-Agent-Konventionen veröffentlichte und in weniger als 24 Stunden 1.863 Stars erreichte, was uns sagt, dass die Formalisierung, wie Agenten arbeiten sollten, keine Nischenbildung mehr ist. OpenAI bringt Frontier-Modelle und Codex auf AWS Bedrock und vervollständigt damit das Dual-Lab-Bedrock-Muster, auf das Enterprise-Agent-Stacks zunehmend setzen. Expanse aus YC P26 löst ein spezifisches und teures Problem: die Vorhersage, wie viel GPU ein Job tatsächlich benötigt, und übertrifft dabei Frontier-Modelle um 8x bei dieser Aufgabe, indem es auf realer Cluster-Telemetrie trainiert.

[03:00] Vertiefung: Codex rust-v0.136.0 Release

Codex `rust-v0.136.0` ist das stabile Release vom 1. Juni, und es ist eine Welle bei Diagnose und Zuverlässigkeit. Die operationell nützlichste Änderung betrifft die Ausgabe von `codex doctor` – Fehlermeldungen enthalten jetzt bessere Standort- und Ursacheninformationen, was für lokale Agenten wichtig ist, wo ein Fehler von der Shell-Umgebung, dem Remote-Transport, dem App-Server-Status, dem Git-Repo oder dem Modell selbst kommen kann. Wenn etwas schiefgeht, ist der Unterschied zwischen "etwas ist fehlgeschlagen" und "der Thread-Inventarprüfungs-Check ist wegen eines Netzwerk-Problems beim Remote-Transport abgelaufen" der Unterschied zwischen Debugging und Raten.

Die Handhabung des App-Server-Lebenszyklus ist straffer. Der Server startet und stoppt sauberer, die Modellauswahl beim Start ist über Anbieter-Konfigurationen hinweg zuverlässiger, und Remote-Transport-Verbindungen erholen sich schneller nach temporären Netzwerkproblemen. Dieser letzte Punkt ist es wert, linger wir darauf eingehen, denn Remote-Codex-Arbeit – z.B. die Überwachung eines Windows-Hosts von einem iPhone aus – ist nur praktikabel, wenn der Transport sich von einem WiFi-Problem erholen kann, ohne einen vollständigen Neustart zu erfordern. Das Release adressiert das.

Die Hook-Konfiguration erhält benannte Hooks und Berechtigungsbereiche. Zuvor musste ein Operator, der dasselbe Hook-Verhalten über mehrere Projekte hinweg wollte, den Hook-Konfigurationsblock in jede Projektdatei kopieren. Benannte Hooks ermöglichen es, das Verhalten einmal zu definieren und es über Konfigurationen hinweg per Namen zu referenzieren. Berechtigungsbereiche machen dasselbe für den `/permissions`-Endpunkt – anstatt eines flachen Berechtigungssatzes können Operatoren Bereiche definieren, die verschiedene Vertrauensebenen oder verschiedene Projektkontexte repräsentieren.

Sowohl das Python SDK als auch das Node SDK erhalten Verbesserungen bei Thread-Management, Turn-Handling und Fehlerpropagation. Die nicht-interaktive Installation über `CODEX_NON_INTERACTIVE=1` funktioniert zuverlässiger, was für Teams wichtig ist, die Codex über ein Konfigurationsmanagement-Tool statt über ein interaktives Installationsskript ausrollen möchten.

Die Upgrade-Empfehlung ist straightforward: testen Sie die `codex doctor`-Ausgabe gegen eine bekannte fehlgeschlagene Konfiguration, definieren Sie einen benannten Hook für ein Muster, das Sie über Projekte hinweg verwenden, und verifizieren Sie, dass die nicht-interaktive Installation in Ihrer CI-Pipeline funktioniert, bevor Sie sich darauf für automatisierte Bereitstellung verlassen.

[11:00] Stanford CS336 KI-Agent-Richtlinien: Wenn institutionelle Validierung viral geht

Stanfords CS336-Kurs – „Language Modeling from Scratch" – veröffentlichte ein formales KI-Agent-Richtliniendokument, das die GitHub-Community als virale Engineering-Ressource behandelte. Das Dokument behandelt, wie Studierende Aufgaben zerlegen, Tools verwenden, Kontext verwalten, Ausgaben verifizieren und über Agent-Qualität in einem akademischen Umfeld reasoning sollten. Es erreichte 1.863 Stars in weniger als 24 Stunden, was ein ungewöhnlich starkes Signal für ein Kurs-Assignments-Artefakt ist.

Die Geschichte hier geht nicht darum, dass das Dokument perfekt oder umfassend ist. Es geht darum, dass die Community es sah und als Referenz behandelte, nicht nur als Kursbeispiel. Das sagt uns etwas darüber, wo die Branche steht: Teams schreiben AGENTS.md-Dateien, CLAUDE.md-Dateien und ähnliche Konventionen, aber sie tun es von Grund auf und ohne einen klaren Referenzpunkt. Stanfords Dokument gibt ihnen einen, auch wenn er aus einem akademischen Kontext stammt.

Der praktische Schritt ist, es zu lesen, die Konventionen zu extrahieren, die für Ihr Team gelten, und sie als Ausgangspunkt für Ihre eigene AGENTS.md zu verwenden. Das Format ist anpassbar – die Prinzipien gelten über den Kurskontext hinaus – und die Tatsache, dass es MIT-lizenziert ist, bedeutet, dass es frei als Grundlage verwendet werden kann.

[18:00] OpenAI auf AWS Bedrock: Das Dual-Lab-Muster ist komplett

OpenAI brachte GPT-4.5, die o-Serien-Modelle und Codex über AWS Bedrock verfügbar. Anthropics Claude ist bereits seit einiger Zeit auf Bedrock. Das bedeutet, Enterprise-Agent-Stacks können nun beide Major-Labs-Modelle über dieselben AWS-Anmeldedaten, dieselbe VPC, dieselben IAM-Kontrollen und dasselbe CloudWatch-Logging bereitstellen.

Die praktische Implikation für OpenClaw-, Hermes- und Codex-Operatoren ist straightforward: Multi-Lab-Modell-Routing wird zur Konfigurationsentscheidung statt zu einem Custom-Integrationsprojekt. Ein Team, das Claude für Planungsaufgaben und OpenAI für Codegenerierung verwenden möchte, kann dies im selben AWS-Konto tun, mit derselben Credential-Rotation, denselben Compliance-Grenzen.

Das Cloud-Verteilungsmuster ist bemerkenswert: Beide Labs wählten zuerst AWS. Das sagt etwas darüber aus, wo Enterprise-KI-Ausgaben konzentriert sind und welcher Cloud-Provider das größte Vertrauen von den Teams hat, die KI-Fähigkeiten im großen Maßstab kaufen.

[25:00] Expanse: 8x bessere GPU-Vorhersage durch Training auf Cluster-Telemetrie

Expanse aus YC P26 löst ein Problem, das HPC-Operatoren gut kennen, aber allgemeine Softwareteams oft übersehen: GPU-Jobs fordern mehr Ressourcen an, als sie tatsächlich benötigen, weil der Einreichende keine gute Möglichkeit hat, die reale Nutzung vorherzusagen. Das Ergebnis ist verschwendetes Computing – Exanses Team maß 59% Computing-Verschwendung auf nationalen HPC-Clustern, ungefähr 8,5 Millionen Dollar pro Monat auf einem Cluster allein.

Expanse funktioniert, indem es einen leichtgewichtigen Daemon auf SLURM- und Kubernetes-Knoten installiert, Hardware-Telemetrie durch DCGM und CUPTI ingestiert und die VRAM-, Auslastungs- und Speicheranforderungen jedes Jobs vor seiner Ausführung vorhersagt. Das Modell ist cluster-spezifisch – es fine-tuned auf der tatsächlichen Submission-History dieses spezifischen Clusters, sodass es mit der Zeit besser wird, je mehr Daten es akkumuliert.

Das Benchmark-Ergebnis ist bemerkenswert: Expanse übertrifft GPT-4.5, Claude Opus 4.8, Gemini 3.5 Pro und Codex 5.3 um 8x bei der GPU-Ressourcen-Vorhersage-Genauigkeit. Der interessante Detail für Agent-Stack-Zuhörer ist, dass Modellgröße die Genauigkeit hier nicht vorhersagt. Claude Haiku übertrifft Opus bei einigen Workloads, weil das Fine-Tuning auf Cluster-Telemetrie mehr zählt als allgemeine Reasoning-Fähigkeit.

Für Teams, die GPU-Workloads betreiben – Training, Fine-Tuning, Inferenz, Batch-Verarbeitung – ist der ROI konkret. Die Integration ist nicht-invasiv: Installieren Sie den Daemon auf einem Knoten, führen Sie Vorhersagen gegen die tatsächliche Ressourcennutzung für zwei Wochen durch und vergleichen Sie.

[33:00] Project Radar: Agent-Betriebssystem, Terminal-Kontext und physische Scheduling

Das Project Radar deckt drei verschiedene Schichten des Agent-Stacks ab.

Anima ist ein Open-Source Agent OS für Hardware-Intelligenz. Die meiste Agent-Diskussion nimmt Cloud-VMs an, aber Agenten, die auf IoT-Geräten, Robotik und Edge-Hardware laufen, brauchen eine andere OS-Schicht – eine, die über Sensordaten, physischen Zustand und Echtzeit-Einschränkungen alongside digitaler Tool-Aufrufe reasoning kann. Anima ist früh bei 116 Stars, gepusht am 2. Juni, aber die Form des Problems ist real.

ctx ist ein Terminal-Kontext-Manager, der `.ctx.md`-Dateien generiert. Das Muster ist einfach: Eine Datei im Repo, die der Agent als Systemkontext zu Beginn jeder Session liest, die Konventionen, Task-Status und Projektnotizen vorwärtsträgt. Dies ist weniger leistungsfähig als ein vollständiges Knowledge-Graph-Memory-System, aber auch weniger komplex einzurichten und zu warten. Für Teams, die Kontext-Kontinuität wollen, ohne sich auf eine vollständige Memory-Architektur zu verpflichten, ist `.ctx.md` ein pragmatischer Einstieg.

agentgrid ist eine offene Planungsschicht für KI-gesteuerte physische Maschinen, Tools und Desktops. Sie befindet sich unter der Agent-Laufzeit und entscheidet, wann und wie physische Aktionen ausgelöst werden. Für Agenten, die die zeitliche Koordination physischer Hardware benötigen – nicht nur digitale Tools aufrufen – ist eine Planungsschicht, die physische Einschränkungen versteht, besser geeignet als eine rein LLM-gesteuerte Aktionsschleife.

[41:00] Praktische Warteschlange

Führen Sie für Codex `codex doctor` aus und vergleichen Sie die Ausgabe, definieren Sie einen benannten Hook für ein übergreifendes Projektmuster und verifizieren Sie die nicht-interaktive Installation in CI. Lesen Sie für Stanfords Richtlinien das Dokument, extrahieren Sie, was für Ihr Team gilt, und aktualisieren Sie Ihre AGENTS.md. Testen Sie für AWS-Modell-Routing Bedrock-Endpunkte sowohl für Anthropic als auch für OpenAI, bevor Sie sich auf ein einzelnes Labor als alleinigen Anbieter festlegen. Installieren Sie für Expanse auf einem Cluster-Knoten, wenn Sie GPU-Workloads im großen Maßstab ausführen. Probieren Sie für das Projekt-Radar Anima auf einem Edge-Gerät aus, fügen Sie einem Repo eine `.ctx.md` hinzu und evaluieren Sie agentgrid, wenn die Aufgabe die zeitliche Koordination physischer Hardware beinhaltet.

Das übergreifende Thema von EP062 ist, dass Infrastruktur sichtbar wird: Diagnosen machen Ausfälle erklärbar, Richtlinien machen Erwartungen lesbar, Cloud-Verteilung macht Modell-Routing zu einer Konfigurationsentscheidung, und clusterspezifisches ML macht Verschwendung bei Rechenressourcen messbar und behebbar. Der Agent-Stack wächst auf die Weise, die für Betreiber entscheidend ist.