# OpenClaw Daily – Episode 12 Shownotizen
**„Kostenlose Frontier-Modelle, multimodales Gedächtnis und Community-Automatisierungen, die Sie umhauen werden“**
📅 12. März 2026
🔗 Veröffentlichung: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11

---

## Episodenzusammenfassung
v2026.3.11 wurde mit zwei Stealth-Free-Frontier-Modellen eingestellt, Googles erstem nativen multimodalen Einbettungsmodell landet in OpenClaw, einem vollständigen Ollama-Onboarding-Assistenten, ACP-Sitzungsfortsetzung für lange Codierungssitzungen und iOS/macOS-App-Optimierung. Plus: ein tiefer Einblick in echte Community-Automatisierungen, die den Leuten viel Zeit sparen.

---

## Community Spotlight – Top-Automatisierungen von BetterClaw

Echte OpenClaw-Benutzer, Echtzeiteinsparung. Aus den BetterClaw Top 10:

1. **Morgenbriefings** – Kalender + E-Mail-Synthese, kontextbezogene Antwortentwürfe, bevor Sie aufwachen
2. **E-Mail-Triage** – Automatisch kategorisieren, Antworten entwerfen, Termine planen – vollständig lokal und privat
3. **Familienkalender-Assistent** – Konflikterkennung, Terminplanung, direkte Nachrichtenübermittlung an die Familie
4. **Selbstheilender Heimserver** – Überwacht Dienste, versucht automatisch Fehlerbehebungen und warnt nur bei unerwarteten Ereignissen
5. **Personal Knowledge Base (RAG)** – Semantische Suche in allen Notizen, Dokumenten und Code

Empfohlener Community-Build: Über 5.000 Notizen, 15 Cron-Jobs, 24 benutzerdefinierte Skripte – vollautomatischer Systemadministrator mit stündlichen Gesundheitsprüfungen, täglichen Briefings und wöchentlichen Sicherheitsüberprüfungen. Kontextbewusstes KI-Argument, nicht nur dumme Skripte.

---

## Neue kostenlose Modelle – Hunter Alpha und Healer Alpha
Beide sind jetzt auf OpenRouter für 0,00 $/Mio. Token verfügbar. (Das kostenlose Kontingent kann vorübergehend sein.)

**Jäger-Alpha**
- 1 Billion Parameter
- 1 Million Token-Kontextfenster
- Optimiert für Agenten-Anwendungsfälle
- https://openrouter.ai/openrouter/hunter-alpha

**Heiler Alpha**
- Omnimodales Grenzgebiet: Sehen, Hören, Denken, Handeln
- 262K Kontextfenster
- https://openrouter.ai/openrouter/healer-alpha

---

## Multimodales Gedächtnis – Gemini Embedding 2
Google kündigte Gemini Embedding 2 am 11. März an. OpenClaw integrierte es noch am selben Tag.
https://deepmind.google/technologies/gemini/

– Erstes natives multimodales Einbettungsmodell – Text, Bilder, Video, Audio, PDFs in einem gemeinsamen Vektorraum
- Native Audio-Unterstützung (kein Transkriptionsschritt)
- 8.192 Token-Eingabelimit (4× vorher)
- Übertrifft Amazon Nova 2 und Voyage Multimodal 3.5 bei Benchmarks
- Konfigurierbare Ausgabedimensionen mit automatischer Neuindizierung bei Änderung
- Striktes Fallback-Gating – keine stille Verschlechterung

Anwendungsfall: Bitten Sie Ihren Agenten, „den Artikel über Bereitstellungspipelines zu finden“ – er zeigt gleichzeitig einen Screenshot, eine Sprachnotiz UND eine Textdatei an. Bedeutung über Schlüsselwörter.

---

## Ollama – Vollständiger erstklassiger Onboarding-Assistent
Ollama erreichte 10 Milliarden Aufrufe: https://ollama.com
In den Community-Anleitungen (dev.to, FreeCodeCamp) führten Tausende von Lesern die manuelle Einrichtung durch. Jetzt ist es in den Assistenten integriert.

Zwei Modi:
- **Lokal** – 100 % offline, alle Rückschlüsse auf dem Gerät, keine Cloud, maximale Privatsphäre
- **Cloud+Lokal** – Hybrid: lokal für schnelle Aufgaben, Cloud für schwere Überlegungen. Intelligentes Modell-Pull-Skipping im Cloud-Modus.

---

## ACP- und Entwicklertools

**ACP-Sitzungsfortsetzung** (`resumeSessionId`)
- Setzen Sie ein Subagenten-Gespräch über Neustarts hinweg fort – ohne erneute Erläuterung des Kontexts
- Wiedergabe des Transkripts auf „loadSession“.
- Weiterleitung von Bildanhängen – visueller Kontext bleibt im Lebenslauf erhalten
- Das ACP-Tool-Streaming enthält jetzt Hinweise zum Dateispeicherort
- Umgebungsvariable „OPENCLAW_CLI“ in untergeordneten Prozessen festgelegt

https://docs.openclaw.ai/acp

---

## App-Updates

**iOS:**
- Neuer Begrüßungsbildschirm mit Live-Agentenübersicht
- Schwebende Steuerelemente durch angedockte Symbolleiste ersetzt
– Der Chat wird in der aufgelösten Hauptsitzung geöffnet – der Kontext bleibt auf allen Geräten bestehen

**macOS:**
- Wechseln Sie zwischen Modellen direkt aus der Konversationsansicht – keine neue Sitzung erforderlich- Präferenzen auf Denkebene bleiben auch bei Neustarts bestehen
- LaunchAgent startet die Härtung neu

**OpenCode Go-Anbieter** – Zen + Go teilen sich jetzt einen Schlüssel im Assistenten-Setup

---

## OpenClaw Backup (gelandet am 8. März)
„
Openclaw-Backup erstellen
Openclaw-Backup-Überprüfung
Openclaw-Backup erstellen --only-config
„
Sichert Konfiguration, Status und Arbeitsbereich. Benutze es.
https://docs.openclaw.ai/cli/backup

---

## Wichtige Links
- Release v2026.3.11: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11
- Hunter Alpha: https://openrouter.ai/openrouter/hunter-alpha
- Heiler Alpha: https://openrouter.ai/openrouter/healer-alpha
- Olama: https://ollama.com
- Gemini-Einbettung 2: https://deepmind.google/technologies/gemini/
- OpenClaw-Dokumente: https://docs.openclaw.ai
- Community Discord: https://discord.com/invite/clawd