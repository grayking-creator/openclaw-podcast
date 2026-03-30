# Show Notes – Episode 8: Explosion lokaler Modelle und das neue Ollama-Ökosystem

## Episodendetails
- **Folge:** 8
- **Datum:** 28. Februar 2026
- **Gastgeber:** Nova (warmer Brite) & Alloy (Amerikaner)
- **Zieldauer:** 30-40 Minuten

## Behandelte Themen

### 1. Aktualisierungen des Ollama-Ökosystems
- Ollama v0.17.0 und v0.17.4 veröffentlicht
- Verbessertes OpenClaw-Onboarding
- Erweiterte Unterstützung für verschiedene Modelle
- **Quellen:** https://github.com/ollama/ollama/releases, https://phoronix.com/news/ollama-0.17

### 2. Neue lokale Modellversionen
- **LFM 2-24B-A2B:** Größtes effizientes Modell, veröffentlicht mit Ollama 0.17.4
- **Qwen 3.5:** Neue multimodale Open-Source-Familie
- **Gemma 3 12B & Phi-4:** Empfohlen für kleine allgemeine Aufgaben
- **Qwen3 30B A3B, EXAONE 4.0 32B, DeepSeek R1 Distill Llama 70B:** Mittelgroße herausragende Optionen
- **Qwen3-235B & DeepSeek V3.2:** Große Schwergewichte
- **GLM-5:** Führend im Denken (Qualitätsindex 49,64)
- **MiniMax-M2.5:** Starke Leistung
- **GPT-OSS 20B & 120B:** OpenAI-Alternativen mit offenem Gewicht
- **Quellen:** https://whatllm.org/blog/best-open-source-models-february-2026, https://www.sitepoint.com/definitive-guide-local-llms-2026-privacy-tools-hardware/

### 3. Praktische Anwendungsfälle, die Menschen entwickeln
- **Vollständiger Business-Autopilot:** E-Mail, soziale Medien, Kampagnenverfolgung, tägliche Briefings
- **Automatisierte Videoproduktion:** Inhalte analysieren, Muster identifizieren, Erfolge reproduzieren
- **Agent Swarms:** Marktforschung über Nacht, Wettbewerbsinformationen
- **Krypto-Arbitrage-Handel rund um die Uhr:** Autonomer Handel mit Telegram-Updates
- **Autonome App-Entwicklung:** „Erstelle ein Spiel“ → funktionale App mit Tausenden von Benutzern
- **AI Business Advisory Board:** 8 Experten analysieren parallel Daten aus mehreren Quellen
- **Quellen:** https://medium.com/@alexrozdolskiy/10-wild-things-people-actually-built-with-openclaw-e18f487cb3e0

### 4. Einführung von Clawbot AI SaaS
- **Angekündigt:** 28. Februar 2026
- Cloud-gehostetes OpenClaw
- Keine lokale Installation erforderlich
- Integrierte KI-Modellauswahl
- **Quellen:** https://markets.financialcontent.com/wral/article/247pressrelease-2026-2-28-clawbot-ai-launches-online-saas-version-of-openclaw-with-built-in-ai-model-selection-for-cloud-based-agent-deployment

### 5. Sicherheitsupdate (Kurzfassung – am Ende)
- **ClawJacked (CVE-2026-25253):** Offengelegt am 27. Februar, gepatcht innerhalb von 24 Stunden
- **Fix:** Update auf v2026.2.25 oder höher
- **Quellen:** https://www.scworld.com/news/how-openclaw-could-be-hijacked-with-a-simple-website-visit

## Wichtige Erkenntnisse
1. **Lokale Modelle explodieren** – Qwen3, LFM 2, Gemma 3, Phi-4, alles großartige Optionen
2. **Ollama macht es einfach** – v0.17-Updates haben alles verbessert
3. **Die praktische Automatisierung ist da** – Unternehmen laufen über Nacht autonom
4. **SaaS-Option verfügbar** – für diejenigen, die nicht selbst hosten möchten
5. **Aktualisieren Sie Ihre OpenClaw** – beheben Sie die ClawJacked-Schwachstelle

## Links erwähnt
- https://github.com/ollama/ollama/releases
- https://phoronix.com/news/ollama-0.17
- https://whatllm.org/blog/best-open-source-models-february-2026
- https://www.sitepoint.com/definitive-guide-local-llms-2026-privacy-tools-hardware/
- https://medium.com/@alexrozdolskiy/10-wild-things-people-actually-built-with-openclaw-e18f487cb3e0
- https://markets.financialcontent.com/wral/article/247pressrelease-2026-2-28-clawbot-ai-launches-online-saas-version-of-openclaw-with-built-in-ai-model-selection-for-cloud-based-agent-deployment
- https://www.scworld.com/news/how-openclaw-could-be-hijacked-with-a-simple-website-visit

---
*Folge 8 | Aufgenommen: 28. Februar 2026*

### 6. Lokale Modelle für Entwickler
- Keine API-Latenz, keine Ratenbeschränkungen, keine Kosten pro Prototyp-Aufruf
- Code-Datenschutz: Proprietäre Codebasen verlassen niemals die Maschine
- Modellrouting: Fachmodelle den Aufgaben zuordnen (Codierungsmodell für Code, Argumentationsmodell für Analyse)
- Unternehmens-Compliance: Lokal löst Cloud-KI-Verbote in vielen Unternehmen
- **Quellen:** https://www.sitepoint.com/definitive-guide-local-llms-2026-privacy-tools-hardware/

### 7. Was kommt als nächstes – Roadmap 2026
- Multimodale (Text+Bild+Audio+Video) lokale Modelle, die der Mainstream-Qualität nahe kommen
- Sprachnative Agenten: Lokale Sprache mit geringer Latenz wird realisierbar
- Edge-Bereitstellung: leistungsfähige Modelle auf Telefonen, Kameras, Sensoren und Robotern
- Modellkomprimierung ermöglicht KI auf stark eingeschränkter Hardware

### 8. Kostenökonomie der Lokalisierung
- Mittelklasse-Setup (ca. 2.000 US-Dollar Mac Mini 64 GB): Break-Even im Vergleich zu Cloud-API-Kosten in weniger als einem Jahr
- Effizienz von Apple Silicon: geringer Stromverbrauch, hohe Speicherbandbreite
- Kostenlose Cloud-Stufen (NVIDIA NIM usw.) für diejenigen, die nicht bereit sind, Hardware zu kaufen
- Forschung/akademische Nutzung: kostenlose Iteration, Reproduzierbarkeit, Datenschutz

## Wichtige Erkenntnisse aktualisiert1. **Lokale Modelle explodieren** – Qwen3, LFM 2, Gemma 3, Phi-4, alles hervorragende Optionen
2. **Ollama macht es einfach** – aktuelle Updates sorgen für ein reibungsloses Onboarding
3. **Praktische Automatisierung ist real** – Unternehmen laufen über Nacht autonom
4. **Entwicklerwechsel im Gange** – Lokal ersetzt Cloud-APIs für Prototyping und datenschutzrelevante Arbeiten
5. **SaaS-Option verfügbar** – Clawbot AI für diejenigen, die nicht selbst hosten möchten
6. **Aktualisieren Sie Ihr OpenClaw** – beheben Sie die ClawJacked-Schwachstelle (v2026.2.25+)
7. **Die Wirtschaftlichkeit funktioniert** – Hardware amortisiert sich für aktive Benutzer innerhalb eines Jahres