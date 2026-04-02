# EP021 — Inside the Loop

**OpenClaw Daily** | 2. April 2026 | ~40 Min

Drei KI-Agenten-Runtimes. Drei verschiedene Theorien darüber, was ein Agent sein sollte. Wir haben die Source Codes geöffnet — und was wir gefunden haben, ist keine Feature-Liste. Es ist eine Philosophie.

---

## Geschichten dieser Folge

### 1. OpenClaw — Das persönliche KI-Betriebssystem
OpenClaw ist als persönliches KI-Betriebssystem strukturiert. Der Gateway-Daemon bildet den Kern. Channels wie Telegram und Discord sind Plugins. Workspaces und Subagents laufen als entkoppelte Prozesse mit eigener Kontextverwaltung. Skills leben in `~/.openclaw/skills/`, Memory in `~/.openclaw/memory/`. Bemerkenswert: `~/.openclaw/cron/` — ein eingebautes Scheduling-System. Das sagt dir, wofür dieses Runtime gebaut ist: Für eine Maschine, die Aufgaben erledigt, auch wenn niemand zusieht.

**Architektur-Dateien:**
- Gateway, Cron, Subagent-Orchestrierung: `~/.openclaw/`
- Skills: `~/.openclaw/skills/`
- LCM (Lossless Context Management): Runtime-intern
- Config: `openclaw.json`

---

### 2. Claude Code — Fokus aufs Wesentliche
Claude Code ist ein CLI-Tool, das fokussiert sein will — und das ist eine bewusste Entscheidung, kein Mangel. Die npm-Package ist `@anthropic-ai/claude-code`. Die Sandbox-Implementierung ist das bemerkenswerteste Detail: Apple Sandbox Profiles auf macOS, Bubblewrap (bwrap) auf Linux. Die `SandboxLinux`-Klasse mit `SandboxConfig`, `SandboxManager` und `ViolationStore` zeigt ein dreistufiges Berechtigungsmodell: always allow, always deny, always ask. OS-Level Enforcement — die Sicherheitsgarantie kommt von der Prozessisolierung, nicht vom LLM.

**Architektur-Dateien:**
- Package: `/opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/`
- Sandbox: `SandboxLinux`, `SandboxConfig`, `SandboxManager`, `ViolationStore`
- Tool Registry: `cli.js`
- Session-Modell: leichtgewichtig, arbeitsverzeichnisgebunden

---

### 3. Hermes Agent — Die Forschungsplattform
Hermes von Nous Research ist die architektonisch reichste der drei Runtimes. Das Kernstück: `~/.hermes/state.db` — eine SQLite-Datenbank in WAL-Mode mit FTS5-Volltextsuche über alle Konversationsnachrichten. Das Sessions-Schema trackt nicht nur Metadata, sondern auch Billing-Details: Input-Tokens, Output-Tokens, Cache-Tokens, Reasoning-Tokens, geschätzte und tatsächliche Kosten in USD. Das ist Kostenbewusstsein als architektonisches Prinzip.

Die Turn-Logik ist dokumentiert: `run_conversation()` als Haupteinstieg. 10-Schritt-Turn-Lifecycle mit interruptiblen API-Calls — mitten im LLM-Call kann der User eine neue Nachricht schicken oder das Gateway den Request abbrechen. Das ist explizites Design, kein Zufall.

**Architektur-Dateien:**
- AIAgent-Klasse: `run_agent.py`
- State Management: `hermes_state.py` — `SessionDB`-Klasse
- Tool Registry: `tools/registry.py` — `ToolRegistry`-Singleton
- Tool Dispatch: `registry.dispatch(name, args, kwargs)`
- Approval System: `tools/approval.py` — `DANGEROUS_PATTERNS`, `detect_dangerous_command()`
- Context Compression: `agent/context_compressor.py`
- Prompt Building: `agent/prompt_builder.py`
- Prompt Caching: `agent/prompt_caching.py`
- Session DB: `~/.hermes/state.db`
- Skills: `~/.hermes/skills/`
- Config: `~/.hermes/config.yaml`

---

### 4. Der Turn Cycle — Wo sie sich wirklich unterscheiden
**Hermes** hat den am besten dokumentierten Loop. Zehn Schritte von der User-Message bis zur Antwort, inklusive preflight-Kontext-Komprimierung, prompt injection, prompt caching und interruptiblen API-Calls. Die `api_mode`-Router unterstützen `chat_completions`, `codex_responses` und `anthropic_messages` — genuine Modellagnostizität als Routing-Architektur, nicht als Marketingbehauptung.

**Claude Code** ist enger. Keine Subagent-Spawning als erstklassiges Konzept. Keine persistente Session-Datenbank. Jede Invocation ist kurzlebig, aber behält Kontext innerhalb eines Arbeitsverzeichnisses. Das ist das richtige Trade-off für seinen Anwendungsfall — Entwicklerhilfe in einem Codebase-Verzeichnis — aber es ist ein anderes Tier.

**OpenClaw** muss multiple konkurrierende Agents koordinieren. Die Turn-Logik ist nicht nur „User → Agent → Tools → Response" — es ist ein Multi-Agent-System mit Gateway-Dispatch, Subagent-Spawning und Channel-spezifischem Routing.

---

### 5. Memory — Drei komplett verschiedene Modelle
**Hermes** setzt auf SQLite. Alles in `state.db` — Sessions, Messages, Reasoning-Tokens, Billing-Daten, FTS5-Suchindex. Concurrent-Zugriff via WAL-Mode. Write Contention Handling mit 1-Sekunden-Timeout, Application-Level-Retries mit Jitter (20–150ms), bis zu 15 Wiederholungen, `BEGIN IMMEDIATE` Transactions. Session-Lineage via `parent_session_id` — wenn Context-Kompression einen Session-Split auslöst, bleibt die Herkunftslinie nachvollziehbar.

**OpenClaw** nutzt dreistufiges Memory: Tages-Logs (`memory/YYYY-MM-DD.md`), kuratierter Langzeitspeicher (`MEMORY.md`), und Skills als prozedurales Gedächtnis. Dateisystem-nativer als Hermes, weniger datenbank-nativ. Unix-Philosophie: grep-freundlich, rsync-bar, git-trackbar.

**Claude Code** hat das leichteste Session-Modell. Kontext innerhalb eines Arbeitsverzeichnisses, aber keine persistente strukturierte Memory über Sessions hinweg. Bewusste Einfachheit.

---

### 6. Sandbox vs. Approval — Zwei Sicherheitsmodelle
**Claude Code** setzt auf OS-Level-Sandboxing. bubblewrap auf Linux definiert erlaubte/verbotene Pfade, schreibt schützt `denyWithinAllow` für dangerous Subpaths, blockiert Unix-Sockets via seccomp BPF, warnt wenn das BPF-Binary nicht verfügbar ist. Der `ViolationStore` trackt bis zu 100 Einträge. Das Modell: Prozessfähigkeiten einschränken, bevor etwas passieren kann.

**Hermes** setzt auf Pattern-Detection und Genehmigung. `DANGEROUS_PATTERNS` in `tools/approval.py` matcht gegen Regexes für rekursive Deletes, `mkfs`/`dd`, SQL-Destruktiv-Operationen, Config-Overwrites, Service-Manipulation, `curl | sh`-RCE, Fork Bombs. Detektion → interaktive Abfrage (CLI) oder Async-Approval-Callback (Telegram/Discord). Smart Approval nutzt einen Hilfs-LLM, um Low-Risk-Matches automatisch durchzuwinken. Session-scoped Approvals + permanente Allowlist in `config.yaml`.

**OpenClaw** kombiniert beides. `exec-approvals.json` für Approval-getriebene Sicherheit, Subagent-Permission-Scopes, Channel-spezifische Berechtigungen.

Fazit: Claude Code ist stärker gegen versehentliche Schäden. Hermes ist flexibler für interaktive Remote-Use-Cases. Das eine ist kein besseres Modell — sie sind für verschiedene Bedrohungsmodelle gebaut.

---

### 7. Skills-Systeme — Das extension story
**Hermes** hat das vollständigste Skills-System. SKILL.md mit YAML-Frontmatter nach dem agentskills.io-Open-Standard. Progressive Disclosure in drei Stufen (Liste, Vollinhalt, Referenzdatei), conditional Skills via `fallback_for_toolsets` und `requires_toolsets`, agent-erstellte Skills via `skill_manage` Tool. Das ist nicht nur ein Feature — das ist prozedurales Lernen. Der Agent kodifiziert, was er gelernt hat.

Hermes hat auch einen Skill-Marketplace: officieller Optional-Skills-Katalog, skills.sh, ClawHub, Claude Marketplace, GitHub-Repos, `/.well-known/skills/`-Convention. Eine explizite Open-Ecosystem-Wette.

**OpenClaw** hat workspace-kontextuelle Skills in `~/.openclaw/skills/` — ebenfalls YAML-Frontmatter + Markdown, anscheinend kreuzkompatibel. MCP als Erweiterungsmechanismus über `openclaw.json`.

**Claude Code** hat ein leichteres Modell — Slash-Commands. Passend für ein fokussiertes CLI-Tool.

---

### 8. hermes claw migrate — Das Signal, das keiner ignorieren sollte
Hermes verschifft ein Tool namens `hermes claw migrate`, das OpenClaw Skills und Workspace-Konfigurationen importiert. Liest das genau: **Hermes** importiert von **OpenClaw**. Das ist keine Behauptung, dass sie das Gleiche sind. Das ist die Behauptung, dass OpenClaws Skill-Modell die Referenz ist, von der es sich zu migraten lohnt.

Die Modellagnostizität von Hermes macht diese Migration glaubwürdig. OpenClaw-User, die Claude als Backend nutzen, können zu Hermes wechseln und ihre vorhandenen Skills mitnehmen. SKILL.md mit YAML-Frontmatter nach agentskills.io — portabel, nicht proprietär.

Für OpenClaw-User ist das keine schlechte Nachricht. Es ist eine Validierung: das Skill-Modell ist gut genug, dass ein konkurrierendes Projekt es übernehmen will. OpenClaws Antwort darauf: nichts ändern, aber beobachten, wie Hermes das Skill-Ökosystem aufbaut.

---

## Kapitel

`[00:00]` Cold Open — Drei Agenten-Runtimes, drei Theorien
`[02:30]` OpenClaw-Architektur — Das persönliche KI-Betriebssystem
`[08:00]` Claude Code — Fokus und absichtliche Enge
`[14:00]` Hermes Agent — Die Forschungsplattform mit SQLite und FTS5
`[20:00]` Der Turn Cycle — Die fundamentale Architekturentscheidung
`[26:00]` Memory-Modelle — Drei komplett verschiedene Ansätze
`[32:00]` Sicherheitsmodelle — Sandbox vs. Approval
`[38:00]` Skills-Systeme — Progressive Disclosure und agentisches Lernen
`[43:00]` hermes claw migrate — Was das Signal bedeutet
`[47:00]` Das Urteil — Welches System wofür
`[52:00]` Modelle für Hermes — Anthropic OAuth, Copilot, OpenRouter, Local

---

## Das Urteil

**Hermes** — Wenn du Forscher oder Power-User bist und ein selbstverbessernder Agent mit echtem Langzeitgedächtnis, Modellagnostizität, FTS5-Suche, Skill-Ökosystem und Multi-Channel-Support (Telegram, Discord, Slack, WhatsApp, Signal) sein soll. Auch richtig, wenn Atropos RL und Trajectory-Compression dich interessieren. Und wenn du bereits OpenClaw nutzt: `hermes claw migrate` bringt deine Skills mit.

**Claude Code** — Wenn du Entwickler bist und die bestmögliche Hilfe in einem bestimmten Codebase-Verzeichnis willst, lokal laufend, mit der stärksten OS-Level-Sandboxing der drei. bubblewrap und Apple Sandbox Integration ist das rigorous Sandbox-Implementierung. Das Trade-off: keine Session-Persistenz, keine Multi-Channel-Präsenz.

**OpenClaw** — Wenn du eine persistente persönliche KI willst, die auf deiner Maschine lebt, mehrere Messaging-Channels gleichzeitig bedient, geplante Tasks ausführt, Subagents für Hintergrundarbeit spawnt und ein Skill-System hat, das du selbst formst. Das Unix-nativste der drei — passt in bestehende Workflows und Dotfile-Konventionen. `hermes claw migrate` sagt dir, dass das Skill-Modell die Referenz ist.

Die tiefe Erkenntnis: Diese drei Systeme encodieren drei verschiedene Theorien darüber, was ein KI-Agent sein sollte. Hermes: persistent, selbstverbessernd, forschungsorientiert. Claude Code: schmal, tief integriert, entwicklerspezifisch. OpenClaw: persönliches KI-Betriebssystem — always-on, multi-surface, multi-agent.

Keine dieser Theorien ist falsch. Es sind verschiedene Wetten darauf, wo der Raum hingeht.

---

## Modelle für Hermes

**Anthropic OAuth** (empfohlener Startpunkt): Claude Sonnet via existing Claude Code Credential Store — kein separater API-Key nötig.

**GitHub Copilot** (kostenlos mit Subscription): GPT-5.4, Claude und Gemini über Copilot-API. GPT-5+ nutzt automatic den Responses-API-Routing.

**OpenRouter** (maximale Flexibilität): 200+ Modelle. Setze `OPENROUTER_API_KEY` in deiner dot env. Built-in Tools für Vision, Web-Summarization und Mixture-of-Agents nutzen automatisch Gemini Flash via OpenRouter als Hilfsmodell.

**Lokale Models**: Jeder Ollama- oder vLLM-Endpunkt über `OPENAI_BASE_URL`.

**Chinesische Provider**: Z-dot-AI GLM, Kimi/Moonshot, MiniMax, Alibaba Cloud Qwen — First-Class Provider IDs, nicht nachträglich hinzugefügt.

**Praktische Empfehlung**: Claude Pro/Max → Anthropic OAuth. Kostenlos + stark → GitHub Copilot mit GPT-5.4. Maximale Flexibilität → OpenRouter mit Claude Sonnet oder Qwen 3.

---

## OpenClaw Daily finden

- 🌐 [tobyonfitnesstech.com/de/podcasts/episode-21](https://tobyonfitnesstech.com/de/podcasts/episode-21)
- 🎙️ Spotify · Apple Podcasts · Pocket Casts · Amazon Music · Overcast
- EN, ES, PT, HI, DE-Feeds verfügbar

→ Reply on Telegram to approve.
