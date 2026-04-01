# EP020 — Die Infrastructure Release

**OpenClaw Daily** | 1. April 2026 | ~32 Min

OpenClaw hat diese Woche aufgehört, ein raffiniertes Werkzeug zu sein, und ist stattdessen zur Infrastruktur geworden. Fünf Geschichten, die erklären, wie es dazu kam — und was das für alle bedeutet, die darauf aufbauen.

---

## Geschichten dieser Folge

### 1. OpenClaw v2026.3.31 — Das Platform-Release
Das folgenreichste OpenClaw-Update seit Monaten. Wichtige Änderungen:
- **Kontrollzentrum für Hintergrundaufgaben** — ACP, Subagents, Cron und CLI-Hintergrundausführung vereint unter einem SQLite-basierten Ledger mit `openclaw flows list|show|cancel`
- **Plugin-Sicherheit standardmäßig geschlossen** — kritische Sicherheitsbefunde bei gefährlichem Code blockieren jetzt Installationen; explizites `--dangerously-force-unsafe-install` erforderlich, um dies zu überschreiben
- **Node-Pairing und Genehmigung getrennt** — Node-Befehle bleiben deaktiviert, bis das Pairing explizit genehmigt wird (Pairing allein reicht nicht mehr aus)
- **Gateway-Authentifizierung gehärtet** — trusted-proxy lehnt gemischte Shared-Token-Konfigurationen ab; local-direct-Fallback erfordert das konfigurierte Token
- **QQ Bot-Kanal** — gebündelter erstklassiger Pfad in das Tencent-Ökosystem
- **Matrix-Streaming-Antworten** — Teilantworten werden jetzt aktualisiert, anstatt den Chat zu fluten
- **MCP Remote HTTP/SSE-Unterstützung** — Tool-Oberflächen über Remote-Transporte bereitstellen
- **Android-Benachrichtigungsweiterleitung** — Paketfilterung, Ruhezeiten, Ratenbegrenzung
- **Leerlauf-Stream-Timeout** — hängende Model-Streams werden sauber abgebrochen
- **ACPX MCP-Bridge gehärtet** — explizite Default-Off-Konfiguration, dokumentierte Vertrauensgrenze
- Breaking: `qwen-portal-auth` entfernt; Konfigurationen, die älter als 2 Monate sind, werden nicht mehr automatisch migriert

📎 [Release-Notizen: openclaw/openclaw v2026.3.31](https://github.com/openclaw/openclaw/releases/tag/v2026.3.31)

---

### 2. OpenClaws China-Fimmel — und Pekings Antwort
OpenClaw wurde in China viral („Lobster" im chinesischen Tech-Jargon), mit GitHub-Stars, die kurzzeitig React überholten. Tencent veranstaltete Pop-up-Installations-Events. Dann kamen die „Lobster-Opfer" — Benutzer, die Dateien verloren, Rechnungen angehäuft oder sensible Daten an KI-Agenten ohne Schutzmaßnahmen offengelegt haben. Peking reagierte mit einem Verbot für Mitarbeiter staatseigener Unternehmen, das Tool zu nutzen.

📎 [The Wire China: How the OpenClaw Frenzy Is Testing China's AI Commitment](https://www.thewirechina.com/2026/03/29/how-the-openclaw-frenzy-is-testing-chinas-ai-commitment/)
📎 [PCWorld security warning: Don't install OpenClaw](https://www.pcworld.com/article/3064874/openclaw-ai-is-going-viral-dont-install-it.html)

---

### 3. Microsoft 365 + OpenClaw — Enterprise-Validierung
Microsoft integriert OpenClaw aktiv in Microsoft 365 und bringt persönliche KI-Agenten zu den etwa 400 Millionen Enterprise-Nutzern. Dies positioniert OpenClaw als Agent-Schicht für die Unternehmensproduktivität — nicht nur als Hobbyisten-Tool.

📎 [Windows Central: Microsoft's new OpenClaw AI agents for Microsoft 365](https://www.windowscentral.com/artificial-intelligence/microsoft-openclaw-will-add-personal-ai-agents-in-microsoft-365)

---

### 4. Perplexity Personal Computer — Lokale KI, die bei dir lebt
Perplexity hat den „Personal Computer" gestartet — einen dedizierten KI-Agenten auf einem Mac mini mit dauerhaftem, kontinuierlichem Zugriff auf deine lokalen Dateien und Anwendungen. Immer an, immer kontextbewusst, vollständig lokal. Kein Cloud-Upload erforderlich.

📎 [r/LocalLLaMA: Local-first agent stacks in 2026](https://www.reddit.com/r/LocalLLaMA/comments/1s6f15f/localfirst_agent_stacks_in_2026_whats_actually/)

---

### 5. Das 297-Milliarden-Dollar-Quartal
Q1 2026 hat jeden Risikokapital-Rekord zunichte gemacht. 297 Milliarden Dollar weltweit investiert, 81 % in KI-Unternehmen. Die vier größten Runden: OpenAI (120 Mrd. $), Anthropic (30 Mrd. $), xAI (20 Mrd. $), Waymo (16 Mrd. $). CoreWeave sicherte sich eine Finanzierungsfazilität von 8,5 Milliarden Dollar. Das Crunchbase Unicorn Board hat in einem einzigen Quartal 900 Milliarden Dollar an Wert hinzugefügt.

📎 [Crunchbase: Q1 2026 Shatters Venture Funding Records](https://news.crunchbase.com/venture/record-breaking-funding-ai-global-q1-2026/)
📎 [TechFundingNews: CoreWeave lands $8.5B](https://techfundingnews.com/coreweave-lands-8-5b-wall-street-ai-cloud/)

---

## Kapitel

`[00:00]` Hook — Der Plattform-Moment
`[02:30]` OpenClaw v2026.3.31 — Wenn ein Werkzeug zur Infrastruktur wird
`[14:00]` OpenClaws China-Fimmel und die staatliche Reaktion
`[21:00]` Microsoft 365-Integration — Enterprise-Validierung oder Risikonormalisierung?
`[27:00]` Perplexity Personal Computer — Lokale KI, die bei dir lebt
`[33:00]` Das 297-Milliarden-Dollar-Quartal — KIs größter Finanzierungscoup
`[39:00]` Outro — Agenten am Wendepunkt

---

## OpenClaw Daily finden

- 🌐 [tobyonfitnesstech.com/de/podcasts/episode-20](https://tobyonfitnesstech.com/de/podcasts/episode-20)
- 🎙️ Spotify · Apple Podcasts · Pocket Casts · Amazon Music · Overcast
- EN, ES, PT, HI, DE-Feeds verfügbar

→ Reply on Telegram to approve.
