OPENCLAW DAILY — EPISODE 030 — April 13, 2026

[00:00] INTRO / HOOK
OpenClaw veröffentlicht ein Update, das die Speicherabfrage vor der Hauptantwort ermöglicht. OpenAI rotiert macOS-Zertifikate nach einem Supply-Chain-Schrecken. Anthropic macht Claude Cowork zur Enterprise-Deployment-Oberfläche. SoftBank gründet ein Unternehmen für „Physical AI". Und Metas neuer Gesundheits-Chatbot fragt nach Rohdaten medizinischer Informationen, die er nicht einsehen darf.

[01:55] STORY 1 — OpenClaw v2026.4.12: Active Memory, lokale MLX-Sprachausgabe und intelligenteres Plugin-Laden
OpenClaw 2026.4.12 ist keine medienträchtige Veröffentlichung. Es ist eine Qualitätsverbesserung der Plattform, und genau deshalb ist sie wichtig.

Das Hauptfeature ist ein optionales Active-Memory-Plugin, das einen spezialisierten Speicher-Subagenten direkt vor der Hauptantwort ausführt. In der Praxis bedeutet das, dass OpenClaw proaktiv relevante Benutzerpräferenzen, Kontext und vergangene Details abrufen kann, bevor es antwortet – anstatt darauf zu warten, dass der Benutzer explizit sagt „merk dir das" oder „suche im Speicher". Das ist eine bedeutende Veränderung im Interaktionsdesign. Vieles von dem, was als „gutes KI-Gedächtnis" bezeichnet wird, ist eigentlich nur diszipliniertes Abruftiming. OpenClaw macht dieses Timing jetzt zum Teil des Produkts.

Die zweite bemerkenswerte Ergänzung ist ein experimenteller lokaler MLX-Sprachanbieter für den macOS-Talk-Modus. Das ist wichtig, weil es mehr Sprachfunktionalität auf das lokale Gerät verlagert – mit expliziter Anbieterauswahl, lokaler Sprachausgabe, Unterbrechungsbehandlung und Fallback-Verhalten. Der allgemeine Trend ist offensichtlich: Lokale Inferenz ist nicht mehr nur für Text und Embeddings relevant. Der Sprachstack wandert ebenfalls nach lokal.

Es gibt auch eine praktische Erweiterung der Modellwahl. OpenClaw bündelt jetzt sowohl einen Codex- als auch einen LM-Studio-Anbieter. Von Codex verwaltete Modelle können natives Auth, Threads, Discovery und Compaction auf ihrem eigenen Pfad nutzen, während lokale oder selbst gehostete OpenAI-kompatible Modelle über LM-Studio-Onboarding und Runtime-Model-Discovery zu Erstklassigen werden. Das ist genau die Art von Anbieteroberflächen-Erweiterung, die eine Agent-Runtime schwerer in eine einzelne Anbietererzählung einsperrt.

Und dann gibt es die Seite der Sicherheit und Runtime-Hygiene. Plugin-Laden ist jetzt auf manifest-deklarierte Anforderungen beschränkt, sodass CLI, Anbieter und Channels nicht standardmäßig unabhängige Plugin-Runtimes aktivieren. In Kombination mit Shell-Wrapper-Hardening, Genehmigungskorrekturen, Startup-Sequenz-Bereinigung und mehreren Traum- und Speicher-Zuverlässigkeitsfixes ist die Kernrichtung klar: Dieses Release dreht sich darum, dass das System sich präziser erinnert und weniger rücksichtslos lädt.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.12

[09:05] STORY 2 — OpenAI Rotiert macOS-App-Zertifikate nach dem Axios-Kompromittierung
OpenAI veröffentlichte eine detaillierte Antwort auf die Axios-Entwickler-Tool-Kompromittierung, und der wichtige Teil ist nicht, ob Angreifer definitiv OpenAIs Signaturzertifikat erhalten haben. Es ist, dass OpenAI die Vertrauenskette als ausreichend kompromittiert behandelt, um trotzdem zu rotieren.

Laut Unternehmen wurde ein bösartiges Axios-Paket am 31. März in einen GitHub-Actions-Workflow gezogen, der im macOS-App-Signierungsprozess verwendet wird. Dieser Workflow hatte Zugang zu Signatur- und Notarisierungsmaterial, das für ChatGPT Desktop, Codex, Codex CLI und Atlas verwendet wurde. OpenAI gibt an, keine Beweise dafür gefunden zu haben, dass Benutzerdaten abgegriffen wurden, keine Beweise dafür, dass Produkte verändert wurden, und keine Beweise dafür, dass das Zertifikat tatsächlich missbraucht wurde. Aber es widerruft und rotiert trotzdem das Zertifikat, veröffentlicht neue Builds und gibt Benutzern eine Frist zum Aktualisieren, bevor ältere macOS-Versionen keinen Support mehr erhalten.

Dies ist eine dieser Geschichten, die wichtig ist, weil sie mehrere KI-Branchenrealitäten in einem einzigen Vorfall komprimiert. Erstens: Die Frontier-Labs sind nicht mehr nur Modelllieferanten. Sie sind Desktop-Software-Distributoren, Entwicklerplattform-Betreiber und Identitätsanker. Zweitens: Supply-Chain-Risiken in scheinbar langweiligen Entwicklerabhängigkeiten können direkt in Verbrauchervertrauen eskalieren. Und drittens: Das Integritätsproblem ist nicht mehr nur „Hat das Modell halluziniert?" Es ist auch „Können Benutzer vertrauen, dass das Binary auf ihrer Maschine wirklich von Ihnen stammt?"

OpenAI sagt, die Grundursache umfasste ein floating Tag in GitHub Actions und eine fehlende minimumReleaseAge-Sicherung für Pakete. Das ist nichts Exotisches. Es ist gewöhnliche Build-Pipeline-Hygiene. Und genau das ist der Punkt. Im Jahr 2026 ist gewöhnliche Build-Pipeline-Hygiene Teil des Frontier-KI-Risikos.
→ https://openai.com/index/axios-developer-tool-compromise/

[14:55] STORY 3 — Anthropic macht Claude Cowork zur Admin-Oberfläche, nicht nur einer Demo
Anthropic kündigte an, dass Claude Cowork jetzt für alle kostenpflichtigen Pläne allgemein verfügbar ist, aber die eigentliche Geschichte ist das Governance-Paket, das drumherum ausgeliefert wird.

Das Unternehmen fügte rollenbasierte Zugriffskontrollen, Gruppenausgabenlimits, Nutzungsanalysen, OpenTelemetry-Ereignisemission, pro-Konnektor-Aktionskontrollen und einen Zoom-Konnektor hinzu, der Meeting-Zusammenfassungen, Transkripte und Aktionspunkte in Cowork einbringen kann. Lesen Sie diese Liste sorgfältig und Sie können den Übergang in Echtzeit sehen. Es geht nicht mehr darum, ob Agents coole Dinge tun können. Es geht darum, ob ein Unternehmen sie über Marketing, Finanzen, Recht, Operations und Produkt ausrollen kann, ohne die Kontrolle über Richtlinien, Nachvollziehbarkeit oder Kostenübersicht zu verlieren.

Anthropics eigene Beschreibung ist aufschlussreich: Der Großteil der Cowork-Nutzung kommt bereits von außerhalb der Ingenieursabteilung. Das bedeutet, der nächste Enterprise-Kampfplatz ist nicht Coding-Assistenz allein. Es ist, ob agentische Workflows zu einer gemeinsamen Betriebsschicht für den Rest des Unternehmens werden. Wenn das passiert, wird die Admin-Konsole zur strategischen Infrastruktur.

Der wichtigste Punkt hier könnte tatsächlich die pro-Tool-Konnektor-Steuerung sein. Nur-Lese- versus Schreibzugriff ist der Unterschied zwischen einem Agenten, der Ihnen hilft, das System zu verstehen, und einem Agenten, der das System verändern kann. Wenn Unternehmen von Experimentierung zu Deployment übergehen, wird diese Linie entscheiden, wer genehmigt und wer blockiert wird.
→ https://claude.com/blog/cowork-for-enterprise

[21:10] STORY 4 — SoftBanks „Physical AI"-Wette ist eigentlich eine Robotics-Plattform-Wette
SoftBank gründet angeblich ein neues Unternehmen, um das zu bauen, was es „Physical AI" nennt – ein Modell, das Maschinen und Roboter bis 2030 autonom steuern kann. Die angeblichen Investoren umfassen Sony, Honda und Nippon Steel.

Das ist ein starkes Signal, weil es neu definiert, wohin einige der größten strategischen Akteure den Wert lenken. Consumer-Chat ist überfüllt. Enterprise-Copilots sind überfüllt. Die Robotics- und Industrie-Steuerungsschicht ist nicht auf die gleiche Weise überfüllt, weil der schwierige Teil nicht nur Modellqualität ist. Es sind Daten, Regelkreise, Hardware-Partnerschaften, Sicherheit und die Fähigkeit, in der realen Welt zu operieren.

SoftBank erzählt seit einiger Zeit Versionen dieser Geschichte durch Robotics- und Sovereign-Infrastructure-Wetten, aber dieser Zug schärft sie. Was Japan offenbar will, ist nicht nur Zugang zu ausländischen Foundation-Modellen. Es will einen inländischen Anteil an der Modellschicht, die schließlich Fabriken, Logistiksysteme und Roboter betreiben wird. Das ist Sovereign AI in einem viel wörtlicheren Sinne: Nicht nur lokale Rechenzentren, sondern lokale Kontrolle über Maschinenverhalten.

Wenn das Software-KI-Rennen um Suchfelder und Code-Editoren ging, könnte das nächste Rennen darum gehen, wer die Standardgehirne für verkörperte Systeme trainiert. SoftBank wettet, dass diese Schicht noch verfügbar ist, um beansprucht zu werden.
→ https://www.theverge.com/ai-artificial-intelligence/910879/softbank-creates-new-company-building-physical-ai

[26:15] STORY 5 — Metas Muse Spark zeigt die schlechteste Consumer-KI-Anreizschleife
WIRED testete Metas neues Muse-Spark-Modell und fand heraus, dass der Assistent gerne nach Roh-Gesundheitsdaten fragte: Fitness-Tracker-Metriken, Glukosewerte, Laborberichte, Blutdruckwerte, das ganze Paket. Das Verkaufsargument war vorhersehbar: Gib mir deine Daten, und ich werde die Trends aufzeichnen, Muster markieren und dir helfen zu interpretieren, was passiert.

Das Problem ist, dass dies genau die Art von hochkontextuellem, hochvertrauenswürdigem Interaktionsmoment ist, wo Consumer-KI-Produkte die Rolle, die sie anstreben, noch nicht verdienen. Von WIRED zitierte medizinische Experten äußerten zwei offensichtliche Bedenken. Das eine ist Datenschutz: Menschen werden dazu verleitet, hochsensible Informationen in Systeme hochzuladen, die nicht wie klinische Umgebungen geregelt sind und diese Informationen möglicherweise für zukünftiges Training verwenden. Das zweite ist Kompetenz: Die Ratschläge sind immer noch nicht zuverlässig genug, um die Intimität der Datenanfrage zu rechtfertigen.

Diese Kombination ist die Geschichte. Das Modell fragt auf einem Vertrauensniveau nach Daten, das das tatsächliche Sicherheits- und Datenschutzprofil des Systems übersteigt. Und weil diese Bots genau in dem Moment leichter zugänglich und personalisierter werden, in dem Gesundheitsversorgung teuer und fragmentiert bleibt, werden viele Menschen versucht sein, sie als Ersatz für Versorgung zu nutzen, anstatt als Ergänzung zu echter medizinischer Beurteilung.

Meta sagt, das Modell ersetze nicht Ihren Arzt. Gut. Aber wenn ein Bot Leute weiterhin einlädt, „die Rohdaten abzuladen", und sich dann wie ein Quasi-Analyst verhält, betritt er bereits eine Rolle, die viel höhere Standards erfordert, als Consumer-KI derzeit erfüllt.
→ https://www.wired.com/story/metas-new-ai-asked-for-my-raw-health-data-and-gave-me-terrible-advice/

[31:15] OUTRO / CLOSE
Das ist die heutige Landkarte: Memory-before-Reply als Produktdesign, Software-Vertrauensketten als KI-Risiko, Agent-Governance als Enterprise-Infrastruktur, Physical AI als nationale Strategie und Gesundheitsdaten-Prompts als Warnsignal für Consumer-Deployment. Antworten Sie hier, um die Transkriptgenerierung zu genehmigen.