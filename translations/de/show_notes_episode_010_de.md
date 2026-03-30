# Notizen anzeigen – Episode 10: Die Dokumenten- und Speicherrevolution

## Episodendetails
- **Folge:** 10
- **Datum:** 4. März 2026
- **Gastgeber:** Nova (warmer Brite) & Alloy (Amerikaner)
- **Zieldauer:** 30-35 Minuten
- **Thema:** OpenClaw entwickelt sich von einer Chat-/Agentenplattform zu einer vollständigen Dokumenten- und Speicherplattform

---

## Teil 1 – Aus der Veröffentlichung: OpenClaw 3. März 2026
**Versionshinweise:** https://github.com/openclaw/openclaw/releases/tag/v2026.3.2

Alles in diesem Abschnitt wurde in der Version vom 3. März ausgeliefert:

### 1. PDF-Analysetool *(NEU)*
- Erstklassiges „PDF“-Tool – native Anthropic/Google-Unterstützung (Modell sieht PDF direkt), Extraktions-Fallback für alle anderen
- Konfigurierbar: „agents.defaults.pdfModel“, „pdfMaxBytesMb“, „pdfMaxPages“.
- Was dadurch freigeschaltet wird: Verträge, Rechnungen, Forschungsarbeiten, jedes Dokument, mit dem Sie tatsächlich arbeiten

### 2. Ollama Memory Embeddings *(NEU – tiefer Einblick in die Folge)*
- „memorySearch.provider = „ollama““ – vollständiger lokaler Speicher/RAG-Stack, keine Cloud-API erforderlich
- Zum ersten Mal können Sie alles ausführen – Inferenz UND Speicher –, ohne einen Cloud-Anbieter zu kontaktieren
- Honrs `models.providers.ollama`-Einstellungen für Einbettungsanfragen
- Warum das wichtig ist: Ihr Agent kann sich jetzt Tausende von Interaktionen merken, indem er nur lokale Datenverarbeitung nutzt

### 3. SecretRef-Erweiterung *(NEU)*
– 64 Anmeldeinformationsziele werden jetzt mit SecretRef abgedeckt
- Fail-Fast bei ungelösten Refs auf aktiven Oberflächen – keine stillen Ausfälle
- Deckt ab: Laufzeitsammler, Secrets-Planung/-Anwendung/-Prüfung, Onboarding von SecretInput UX

### 4. Sitzungsanhänge *(NEU)*
- „sessions_spawn“ unterstützt Inline-Dateianhänge (Subagent-Laufzeit)
- Base64/utf8-Kodierung, Lebenszyklusbereinigung, Einschränkungen über „tools.sessions_spawn.attachments“.
– Agenten können Dateien jetzt direkt aneinander weitergeben

### 5. Standardeinstellungen für Telegram-Streaming
- Streaming ist jetzt standardmäßig auf „teilweise“ eingestellt (war „aus“) – Live-Vorschau sofort einsatzbereit für neue Setups
- DM-Streaming verwendet „sendMessageDraft“ für die private Vorschau

### 6. MiniMax-M2.5-Hochgeschwindigkeit
- Erstklassiger Support über Kataloge und Onboarding hinweg – schnellere Variante von MiniMax-M2.5

### 7. CLI-Konfigurationsvalidierung
- „openclaw config validieren --json“ – Fehler vor dem Gateway-Start abfangen
– Detaillierte Pfade ungültiger Schlüssel bei Startfehlern

### 8. Zalo Personal Plugin neu erstellt
- Native „zca-js“-Integration, vollständig im Prozess – kein externer CLI-Transport

### 9. Multimedia Outbound
- Discord, Slack, WhatsApp, Zalo vereint mit gemeinsamer „sendPayload“ + Multimedia-Iteration

### 10. Plugin SDK / STT
- „api.runtime.stt.transcribeAudioFile()“ – Erweiterungen können jetzt Sprache in Text umwandeln

---

## Teil 2 – Diese Woche in OpenClaw

### Artikel 1: OpenClaw übertrifft 250.000 GitHub-Sterne
**Quelle:** ainvest.com – 3. März 2026
**URL:** https://www.ainvest.com/news/openclaw-github-star-count-surpasses-250-000-ai-agent-boom-2603/

OpenClaw erreichte 250.000 GitHub-Sterne – das schnellste KI-Projekt, das diesen Meilenstein erreichte. Der Artikel hebt auch hervor, dass C3.ai (Enterprise AI) die Umsatzprognosen um 30 % verfehlte und einen Personalabbau um 26 % ankündigte. Der Kontrast ist frappierend: Unternehmens-KI gerät ins Straucheln, während selbstgehostete Open-Source-KI explodiert. Als Hauptunterscheidungsmerkmale werden das Local-First-Design und die Multiplattform-Unterstützung von OpenClaw genannt.

### Artikel 2: Inside OpenClaw – Die Architektur, die alles erklärt
**Quelle:** dev.to – 4. März 2026
**URL:** https://dev.to/jiade/inside-openclaw-how-the-worlds-fastest-growing-ai-agent-actually-works-under-the-hood-4p5nEin tiefer technischer Einblick in die Frage, warum OpenClaw gewachsen ist, während Hunderte anderer KI-Agent-Frameworks nicht gewachsen sind. Behandelt: die Pi SDK-Einbettungsstrategie, das zweischichtige Speichersystem, das Lane Queue-Parallelitätsmodell und die Heartbeat-Engine. Die These: Es ist kein Marketing, es ist Architektur. Guter Episodenstoff, um zu erklären, was diese Plattform von LangChain, AutoGPT und anderen unterscheidet.

### Artikel 3: OpenClaw in der realen Welt (Produktionsmuster)
**Quelle:** Trilogy AI / Rahul Subramaniam – 3. März 2026
**URL:** https://trilogyai.substack.com/p/openclaw-in-the-real-world

Der Reality-Check-Artikel. Deckt drei Fehlermodi ab, auf die Menschen nach dem anfänglichen Setup-High stoßen: Der Speicher bricht zusammen, Sie verlieren Arbeit, wenn die Maschine neu startet, und Zuverlässigkeit ist wichtiger als Experimente. Bietet Produktionsmuster für den Übergang von einer „coolen Demo“ zu einem System, auf das Sie tatsächlich angewiesen sind. Stellt eine direkte Verbindung zum Erinnerungsthema von Episode 10 her.

---

## Schlüssel zum Mitnehmen
Diese Version überschreitet eine Schwelle: Dokumentenanalyse + persistenter lokaler Speicher + Dateiweitergabe zwischen Agenten = OpenClaw als zweites Gehirn, nicht nur als Chat-Schnittstelle. Der 250.000-Sterne-Meilenstein und der Artikel über die reale Produktion signalisieren beide dasselbe: Die Leute experimentieren nicht mehr, sie verlassen sich darauf.

## Besprochene Build-Muster
1. **Legal Document Reviewer** – PDF-Tool + Speicher + Slack-Ausgabe
2. **Lokaler Forschungsassistent** – Ollama-Einbettungen + PDF-Tool, Zero-Cloud-API
3. **Sichere Credential-Pipeline** – SecretRef + Sitzungsanhänge für Multi-Agent-Workflows

---
📋 Vollständiges Drehbuch: „openclaw-podcast/episode_010.md“ (3.530 Wörter)
✅ Themenprüfung: Alle Themen wurden anhand der Episoden 0–9 als sauber verifiziert
⏳ **Warte auf Ihre Genehmigung, um mit der Audiogenerierung fortzufahren**