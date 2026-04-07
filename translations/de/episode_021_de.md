[NOVA]: Ich bin NOVA.

[ALLOY]: Und ich bin ALLOY. Das ist OpenClaw Daily. Heute tauchen wir ein in den Source Code von drei KI-Agenten-Runtimes — OpenClaw, Claude Code und Hermes — und fragen, was uns die Architektur eigentlich darüber sagt, wofür jedes einzelne System gebaut ist.

[NOVA]: Drei Agenten-Runtimes betraten einen Codebase. Nur einer wusste, worauf er hinarbeitete.

[NOVA]: Heute ist ein technischer Deep Dive, ALLOY. Wir geben euch keine Marketing-Texte. Wir öffnen die tatsächlichen Dateien und zeigen euch, was der Code tut — denn die Architektur ist die Philosophie. Wie etwas sein Turn-Cycle verwaltet, wie es Memory persistiert, wie es gefährliche Aktionen gated — das sind keine Implementierungsdetails. Das ist das Produkt.

[ALLOY]: Und das Interessante ist: Wenn man alle drei nebeneinander betrachtet, wird einem klar, dass sie sich kaum einig sind, was ein „Agent" überhaupt ist. Hermes hat einen Agenten, der sich selbst verbessert und seine eigenen Skills schreibt. Claude Code hat einen Agenten, der nur dazu da ist, beim Programmieren in einem bestimmten Verzeichnis zu helfen. OpenClaw hat einen Agenten, der eher wie ein Betriebssystem funktioniert — persistent, multi-Channel, multi-Subagent. Das sind grundverschiedene Tiere, die sich dasselbe Wort teilen.

[NOVA]: Fangen wir an mit dem, wie jedes System auf der obersten Ebene strukturiert ist, denn das formt alles Weitere.

[NOVA]: Beginnen wir mit OpenClaw. Wenn man sich `~/.openclaw/` anschaut, sieht man die Runtime-Struktur. Es gibt einen Gateway-Daemon, der das Gesamtsystem verwaltet. Channels — Telegram, Discord und so weiter — sind Plugins, die sich mit diesem Gateway verbinden. Die Workspace-Dateien leben in `~/.openclaw/workspace/`, und Subagents laufen als entkoppelte Prozesse mit ihrem eigenen Kontext. Die Config liegt in `openclaw.json`. Das Skills-System lebt in `~/.openclaw/skills/`, und Memory wird in `~/.openclaw/memory/` gespeichert. Kritisch wichtig: Es gibt auch `~/.openclaw/cron/` — OpenClaw hat ein eingebautes Scheduling-System, und das sagt dir etwas Entscheidendes: Diese Runtime ist für eine Maschine gebaut, die Aufgaben erledigen muss, auch wenn niemand zusieht.

[ALLOY]: Richtig. OpenClaw ist als persönliches KI-Betriebssystem architektiert. Es geht nicht nur um eine einzelne Agent-Schleife. Es geht um persistente Präsenz über Messaging-Oberflächen hinweg, geplante Hintergrundarbeit und Subagent-Delegation. Der OpenClaw Gateway-Daemon ist der Kernel dieses Systems. Alles andere ist ein Prozess.

[NOVA]: Jetzt Claude Code — und das wird eine kürzere Architektur-Diskussion, weil Claude Code bewusst fokussiert ist. Man installiert es über npm: `@anthropic-ai/claude-code`, Version 2.1.59 zum Zeitpunkt der Aufnahme. Es ist ein CLI-Tool zuerst. Es hat eine Sandboxing-Schicht, die wir in seinen Abhängigkeiten sehen können — Module für macOS Apple Sandbox Profiles und Linux bwrap (bubblewrap) Integration. Das Tool-Registry ist in `cli.js` und verwandten Dateien. Aber die Architektur ist bewusst schmal: Es will das beste Tool für eine Aufgabe sein — Entwickler in einem Codebase-Verzeichnis helfen.

[ALLOY]: Was eine völlig legitime Designentscheidung ist. Schmal und tief schlägt breit und flach. Aber es bedeutet, dass Claude Codes Session-Modell sich von den anderen beiden unterscheidet. Es hat keine persistente Session-Datenbank. Jede Invocation ist etwas kurzlebig, obwohl sie Konversationszustand innerhalb eines Arbeitsverzeichnisses aufrechterhalten kann. Wir kommen noch dazu, was das für Memory bedeutet.

[NOVA]: Und dann Hermes Agent von Nous Research. Der ist am explizitesten als Forschungsplattform architektiert. Die Kern-Orchestrierungs-Engine ist `run_agent.py` und die `AIAgent`-Klasse. Der Session-Store ist eine SQLite-Datenbank unter `~/.hermes/state.db` im WAL-Modus — also concurrent Reader, ein Writer, was relevant ist, wenn Gateway und CLI beide darauf zugreifen. Und es hat FTS5-Volltextsuche über alle Session-Nachrichten via Virtual Table.

[ALLOY]: Das ist tatsächlich eine sehr bedeutsame architektonische Entscheidung. FTS5 bedeutet, du kannst deinen gesamten Konversationsverlauf durchsuchen, nicht nur die letzten Turns. Wenn du ein Forscher bist, der lange Sessions über mehrere Themen hinweg führt, ist das ein wichtiges Feature. Und die Tatsache, dass sie Token-Zähler, Billing und Model-Konfigurationen pro Session tracken, sagt dir, dass das mit Kostenbewusstsein gebaut wurde — sowohl für das Forschungslabor als auch für Nutzer, die für API-Aufrufe bezahlen.

[NOVA]: Reden wir über das wichtigste Element jeder Agent-Runtime: den Turn Cycle. Wie bewältigt jedes System einen einzelnen Austausch — User-Message rein, Model-Denken, Tool-Calls, Antwort raus?

[ALLOY]: Beginnen wir mit Hermes, weil es den am besten dokumentierten Loop hat. Aus den Docs: `run_conversation()` ist der Haupteinstiegspunkt. Der Turn-Lifecycle sieht so aus:

[NOVA]: Schritt eins: Generiere eine Task-ID.

[NOVA]: Schritt zwei: Hänge die aktuelle User-Message an.

[NOVA]: Schritt drei: Lade oder baue den gecachten System-Prompt.

[NOVA]: Schritt vier: Komprimiere eventuell den Kontext vorab, wenn er zu lang wird.

[NOVA]: Schritt fünf: Baue api_messages — die eigentliche Prompt-Payload.

[NOVA]: Schritt sechs: Injiziere ephemere Prompt-Schichten.

[NOVA]: Schritt sieben: Wende Prompt-Caching an, wenn angebracht.

[NOVA]: Schritt acht: Mache einen interruptiblen API-Call.

[NOVA]: Schritt neun: Wenn Tool-Calls: Führe sie aus, hänge Ergebnisse an, springe zurück.

[NOVA]: Schritt zehn: Wenn finale Textantwort: Persistiere, räume auf, gib zurück.

[NOVA]: Schritt acht — interruptible API-Calls. Das ist wichtig. Hermes wrapt seine API-Requests so, dass sie vom CLI oder Gateway abgebrochen werden können. Das ist relevant, weil der Agent mitten in einem langen LLM-Call stecken könnte und der User eine neue Nachricht schickt, oder ein Hintergrundsystem den Request canceln muss. Das ist explizites Design, keine nachträgliche Überlegung.

[ALLOY]: Und schau dir die API-Modi an, die Hermes unterstützt. Drei Ausführungspfade: `chat_completions` für OpenAI-kompatible Endpunkte (inklusive OpenRouter), `codex_responses` für die Codex und Responses API, und `anthropic_messages` für die native Anthropic Messages API. Der Modus wird aus expliziten Argumenten, Provider-Auswahl und Base-URL-Heuristiken aufgelöst. Also Hermes ist genuin modellagnostisch — nicht als Marketingbehauptung, sondern als Routing-Architektur.

[NOVA]: Jetzt Hermes's Tool-Ausführung. Zwei Modi: sequentiell für einzelne oder interaktive Tools, und concurrent für mehrere nicht-interaktive Tools. Und hier ist der clevere Teil — bei.concurrent Execution bleibt die Nachrichten- und Ergebnisreihenfolge beim Wiedereinfügen der Tool-Responses in den Konversationsverlauf erhalten. Das ist eine nicht-triviale Constraint, die man richtig hinbekommen muss.

[ALLOY]: Bei Claude Code haben wir nicht denselben Source-Pfad zur Loop-Datei, aber wir können aus der Package-Struktur ableiten. Das npm-Package liegt unter `/opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/`. Die wichtigsten Muster finden sich in `cli.js` — wie es Tool-Calls handhabt, wie es Permission-Prompts verwaltet, wie es looped. Was wir über Claude Code's Loop wissen: Er ist um einen bestimmten Anwendungsfall herum entworfen: Entwicklerunterstützung in einem lokalen Verzeichnis. Subagent-Spawning ist nicht als erstklassiges Konzept wie bei OpenClaw vorhanden.

[NOVA]: Und OpenClaw's Agent-Loop ist um die Tatsache herum entworfen, dass es mehrere konkurrierende Agents mit einem Gateway gibt, das die Koordination verwaltet. Der Loop geht nicht nur um „User → Agent → Tools → Response." Es geht darum: User-Message kommt auf Channel X an, Subagent Y greift sie auf, Subagent Y spawnt möglicherweise Subagent Z, Ergebnisse kommen zurück, Gateway dispatched an die richtige Oberfläche. Das Clawflow-Skill, das Multi-Agent-Workflows orchestriert, ist Beweis dafür — es ist für entkoppelte Hintergrund-Tasks entworfen, die sich trotzdem wie ein Job verhalten.

[ALLOY]: OpenClaw's Loop ist der komplexeste der drei, weil er die meiste Koordinationsoberfläche zu verwalten hat. Aber Komplexität ist nicht immer schlecht — sie ist angemessene Komplexität für das, was es versucht zu tun.

[NOVA]: Das ist der Punkt, an dem Hermes sich architektonisch wirklich abhebt. Lasst uns tief in das SQLite-Schema eintauchen.

[ALLOY]: `~/.hermes/state.db` hat vier logische Komponenten: eine Sessions-Tabelle, eine Messages-Tabelle, eine FTS5-Virtual-Table namens `messages_fts`, und eine `schema_version`-Tabelle. Die Sessions-Tabelle ist reichhaltig — sie trackt nicht nur Session-Metadaten, sondern auch Billing-Informationen: `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`, `estimated_cost_usd`, `actual_cost_usd`, `cost_status`, `pricing_version`. Wenn du ein Multi-Model-Setup mit unterschiedlicher Preisgestaltung von verschiedenen Providern fährst, trackt Hermes deine Kosten pro Session.

[NOVA]: Die Messages-Tabelle speichert alles. `role`, `content`, `tool_call_id`, `tool_calls` als JSON-String, `tool_name`, `token_count`, `finish_reason`, `reasoning`, `reasoning_details`, und `codex_reasoning_items`. Beachte, dass Reasoning separat gespeichert wird — das ist für Provider wie Claude, die Thinking-Tokens exposen. Und es gibt drei Trigger, die die FTS5-Tabelle bei INSERT, UPDATE und DELETE synchron halten.

[ALLOY]: Das Write-Contention-Handling ist einen Blick wert. Hermes verarbeitet mehrere Prozesse — Gateway plus CLI-Sessions plus Worktree-Agents — die sich alle eine `state.db` teilen. Es nutzt ein kurzes SQLite-Timeout (1 Sekunde, nicht die Standard-30), Application-Level-Retries mit random Jitter zwischen 20 und 150 Millisekunden, bis zu 15 Wiederholungen, und `BEGIN IMMEDIATE`-Transactions, um Lock-Contention früh sichtbar zu machen. Es macht auch periodische WAL-Checkpoints alle 50 Writes im PASSIVE-Modus. Das ist durchdachtes Engineering — sie vermeiden SQLite's Convoy-Effect-Problem, bei dem konkurrierende Writer in denselben Intervallen wiederholen.

[NOVA]: Und Session-Lineage via `parent_session_id`. Wenn Context-Kompression einen Session-Split auslöst — was passiert, wenn das Kontextfenster voll ist — bekommt die neue Session eine neue ID, aber die Herkunftslinie bleibt über `parent_session_id` verfolgbar. Du kannst ganze Session-Lineages rekursiv abfragen. Das ist für langlaufende Forschungs- oder Programmier-Sessions, bei denen Context-Kompression mitten in einer Task passiert.

[ALLOY]: Jetzt vergleiche das mit Claude Code. Claude Codes Session-Modell ist... leichter. Es kann Konversationskontext innerhalb eines Arbeitsverzeichnisses aufrechterhalten, aber es ist nicht als langfristiges Memory-System konzipiert. Die Sandbox ist um Dateisystem-Berechtigungen für ein bestimmtes Verzeichnis herum entworfen — nicht um persistente strukturierte Memory über Sessions hinweg. Das ist ein bewusster Trade-off: Einfachheit für den häufigsten Fall (Entwicklerhilfe in einem Codebase) gegen reichhaltige Session-Persistenz.

[NOVA]: Und OpenClaw's Memory-Modell. Es nutzt Workspace-Dateien für strukturierten Kontext — `MEMORY.md` für langfristiges kuratiertes Memory, `memory/YYYY-MM-DD.md` für tägliche Session-Logs. Es gibt auch ein LCM-System — Lossless Context Management — das den Konversationsverlauf komprimiert. Und es gibt ein Skills-System, das als prozedurales Memory fungiert. Also ein dreistufiges Modell: Rohe Tages-Logs, kuratiertes Langzeitgedächtnis und Skills, die wiederverwendbare Workflows kodifizieren.

[ALLOY]: Der OpenClaw-Ansatz ist dateisystem-nativer und weniger datenbank-nativ als Hermes. Hermes packt alles in SQLite, weil es eine einzelne Runtime ist, die concurrent Multi-Prozess-Zugriff und FTS5 braucht. OpenClaw nutzt das Dateisystem, weil es zur Unix-Philosophie passt und die Daten universell zugänglich macht — du kannst sie greppen, mit rsync sichern, in git packen.

[NOVA]: Das ist der Punkt, an dem Claude Code seine Karten wirklich aufdeckt. Reden wir darüber, wie es gefährliche Aktionen handhabt.

[ALLOY]: Claude Code hat ein Sandboxing-System, das zwei Plattformen explizit anvisiert: macOS und Linux. Auf macOS nutzt es Apple Sandbox Profiles. Auf Linux nutzt es bwrap — bubblewrap. Das System heißt `SandboxLinux` im Source, und es gibt Klassen wie `SandboxConfig`, `SandboxManager` und eine `ViolationStore`, die Sandbox-Verstöße trackt — mit einem Gesamtzähler und einer History pro Command. Der Violations-Store hat eine Max-Größe von 100 Einträgen und einen Gesamtzähler, der weiter hochzählt, auch wenn der Store voll ist.

[NOVA]: Die Sandbox-Config für Linux ist in `sandbox_linux.py` definiert. Sie startet mit `--new-session --die-with-parent`. Dann baut sie erlaubte und verbotene Dateisystem-Pfade auf. Die erlaubten Pfade beginnen mit einer Default-Allowlist — Dinge wie `/dev/null`, `/dev/urandom`, `/dev/zero`. Verbotene Pfade sind Dinge wie `/etc/ssh/ssh_config.d`, falls vorhanden. Für Schreibpfade gibt es ein `denyWithinAllow`-Konzept — du kannst in ein Verzeichnis schreiben, aber nicht in spezifische gefährliche Subpaths darin.

[ALLOY]: Die Linux-Sandbox hat auch seccomp-BPF-Filterung für Unix-Socket-Blocking. Es gibt einen `bpfPath` und einen `applyPath` für die seccomp-Binary. Wenn die nicht verfügbar sind, fällt es darauf zurück, Unix-Sockets zu erlauben — aber es warnt, dass vollständiger Schutz nicht verfügbar ist. Auf macOS gibt es einen `SandboxMonitor`, der mit dem `osascript`-Befehl nach Verstößen schaut.

[NOVA]: Jetzt vergleiche das mit Hermes's Ansatz. Hermes hat eine `DANGEROUS_PATTERNS`-Liste in `tools/approval.py` — Regex-Muster gepaart mit Beschreibungen, die rekursive Deletes abdecken, Dateisystem-Formatierungsbefehle wie `mkfs` und `dd`, SQL-Destruktiv-Operationen, System-Config-Overwrites, Service-Manipulation, Remote-Code-Execution via `curl | sh`, Fork Bombs. Bevor irgendein Terminal-Command ausgeführt wird, checkt `detect_dangerous_command()` gegen alle Muster.

[ALLOY]: Wenn ein Match gefunden wird: Im CLI-Modus erscheint ein interaktiver Prompt mit der Frage, ob der User genehmigt, ablehnt oder dauerhaft erlaubt. Im Gateway-Modus schickt ein async Approval-Callback die Anfrage an die Messaging-Plattform — wenn du also auf Telegram oder Discord bist, kriegst du die Genehmigungsnachricht dort. Es gibt auch eine Smart-Approval-Option, bei der ein Hilfs-LLM Low-Risk-Commands, die zufällig gefährliche Muster matchen, automatisch durchwinken kann — wie `rm -rf node_modules/`, das das rekursive Delete-Muster matcht.

[NOVA]: Und Hermes hat session-scoped Approvals. Wenn du einmal „rekursives Delete" für eine Session genehmigt hast, fragt dich ein nachfolgendes `rm -rf` nicht erneut. Die permanente Allowlist schreibt Muster in `config.yaml`'s `command_allowlist`, damit sie über Sessions hinweg persistieren.

[ALLOY]: Das sind fundamental verschiedene Modelle. Claude Codes Sandbox geht's darum, die Fähigkeiten des Prozesses einzuschränken, bevor etwas Schlimmes passieren kann — das OS erzwingt es. Hermes's Approval-System geht's darum, gefährliche Muster zu erkennen und zu fragen — der Mensch erzwingt es. Das Claude-Code-Modell ist stärker gegen versehentliche Schäden. Das Hermes-Modell ist flexibler für interaktive Use-Cases, bei denen der Agent auf einem Remote-Server läuft und der User per Telegram genehmigt.

[NOVA]: OpenClaw's Modell kombiniert Elemente von beiden. Das exec-Tool hat ein Approval-System — es gibt `exec-approvals.json` im Config-Verzeichnis. Und OpenClaw's Subagent-System hat Permission-Scopes — Subagents laufen mit spezifischen Workspace-Kontexten und können nicht notwendigerweise alles lesen oder schreiben, was der Parent-Agent kann. Das Gateway hat auch das Konzept von Channel-spezifischen Berechtigungen — was auf Telegram erlaubt ist, kann sich von dem auf Discord unterscheiden.

[NOVA]: Reden wir darüber, wie jedes System seine Erweiterbarkeit.handhabt.

[ALLOY]: Beginnen wir mit Hermes's Skills-System, weil es das vollständigste ist. Skills sind bedarfsgesteuerte Wissensdokumente, die der Agent bei Bedarf laden kann. Sie folgen dem agentskills.io Open-Standard, was bedeutet, sie sind nicht an Hermes gebunden — sie sind portabel. Das Skill-Format ist SKILL.md mit YAML-Frontmatter, das `name`, `description`, `version`, `platforms` und Metadata für Aktivierungsbedingungen deklariert.

[NOVA]: Das progressive-Disclosure-Muster ist clever. Level null: `skills_list()` gibt nur Name, Description und Category zurück — etwa 3k Tokens. Level eins: `skill_view(name)` lädt den vollständigen Inhalt. Level zwei: `skill_view(name, path)` lädt eine spezifische Referenzdatei. Der Agent zahlt also nur die Token-Kosten, wenn er den vollen Skill tatsächlich braucht.

[ALLOY]: Skills können konditional sein. Sie können `fallback_for_toolsets` deklarieren — ein DuckDuckGo-Search-Skill taucht nur auf, wenn der Premium-Web-Such-Toolset nicht verfügbar ist. Oder `requires_toolsets` — ein Skill taucht nur auf, wenn bestimmte Tools vorhanden sind. Und sie können erforderliche Environment-Variablen deklarieren, ohne aus der Discovery zu verschwinden — wenn ein Key fehlt, fragt Hermes im CLI-Modus sicher danach, aber niemals in Messaging-Oberflächen.

[NOVA]: Agent-erstellte Skills sind ein wichtiges Differenzierungsmerkmal. Das `skill_manage`-Tool lässt den Agenten seine eigenen Skills via Create/Patch/Edit/Delete/Write-File/Remove-File erstellen, aktualisieren und löschen. Die Docs spezifizieren die Trigger-Bedingungen: nach dem Abschließen einer komplexen Task mit 5+ Tool-Calls, wenn er auf Fehler stößt und den funktionierenden Pfad findet, wenn der User seinen Ansatz korrigiert, wenn er einen nichttrivialen Workflow entdeckt. Das ist die prozedurale Memory-Schicht — der Agent macht nicht nur Arbeit, er lernt, wie man Arbeit erledigt.

[ALLOY]: Hermes hat eine vollständige Skill-Marketplace-Integration. Es verbindet sich mit dem offiziellen Optional-Skills-Katalog, skills.sh (Vercels öffentliches Verzeichnis), Well-Known-Skill-Endpunkten via der `/.well-known/skills/`-Convention, direkten GitHub-Repos, ClawHub und Claude-Marketplace-Repos. Du kannst Skills direkt auf GitHub veröffentlichen. Du kannst eigene GitHub-Taps hinzufügen. Das ist ein genuiner Open-Ecosystem-Spielzug — Hermes versucht nicht, die Skill-Lieferkette zu besitzen.

[NOVA]: Und Hermes unterstützt externe Skill-Verzeichnisse. Du kannst es auf `~/.agents/skills/` oder `/home/shared/team-skills/` zeigen lassen via `${VAR}`-Environment-Variable-Expansion. Diese Verzeichnisse sind Read-Only für Discovery — der Agent schreibt neue Skills immer nach `~/.hermes/skills/`. Aber externe Skills erscheinen im System-Prompt-Index und als Slash-Commands, nicht unterscheidbar von lokalen Skills.

[ALLOY]: Jetzt OpenClaw's Skills-System. Wenn man sich `~/.openclaw/skills/` anschaut, ist es auch YAML-Frontmatter + Markdown-Body, und das `hermes claw migrate`-Tool deutet auf Kreuzkompatibilität hin. OpenClaw-Skills sind Workspace-kontextuell — sie leben neben dem Projekt, für das sie relevant sind. Das Skill-System ist mit dem Subagent-System integriert, also kann man Skills haben, die beschreiben, wie man den richtigen Subagenten für eine gegebene Task spawned.

[NOVA]: Und OpenClaw unterstützt MCP — Model Context Protocol — als Erweiterungsmechanismus. Die `openclaw.json`-Config hat einen `plugins`-Abschnitt und einen `extensions`-Abschnitt. MCP-Server können konfiguriert werden, um dem Agenten Tools von externen Services zu geben.

[ALLOY]: Claude Code hat ein fokussierteres Erweiterungsmodell. Die npm-Package-Struktur deutet darauf hin, dass es dafür gedacht ist, gut mit bestehender Developer-Tooling zu funktionieren, anstatt einen eigenen Plugin-Marketplace zu haben. Das Skill-System in Claude Code ist leichter — Slash-Commands, im Wesentlichen. Aber das ist passend für ein fokussiertes CLI-Tool.

[NOVA]: Wir müssen über `hermes claw migrate` reden. Das ist ein explizites Migrations-Tool, das mit Hermes ausgeliefert wird, um OpenClaw-Skills und Workspace-Konfigurationen zu importieren. Das ist ein bedeutsames Signal.

[ALLOY]: Absolut. Hermes verschifft ein Tool namens `hermes claw migrate`, das sagt: Wir wissen, dass OpenClaw ein Skills-System hat, das es wert ist, sich auszuleihen. Wir werden es importieren. Das ist nicht der Zug eines Projekts, das glaubt, es sei in einer anderen Kategorie. Das ist der Zug eines Projekts, das glaubt, es konkurriere direkt und dass das Skills-Ecosystem es wert ist, gegenseitig befruchtet zu werden.

[NOVA]: Die Tatsache, dass es `hermes claw migrate` heißt und nicht `claw migrate`, sagt dir etwas über die Richtung der Beziehung. OpenClaw kam zuerst — Hermes migriert davon. Aber Hermes tut das explizit, was bedeutet, dass das Nous-Research-Team sich OpenClaw's Skill-System und Workspace-Modell angeschaut und entschieden hat: Wir wollen das in unserem Ökosystem, und wir wollen es OpenClaw-Nutzern leicht machen, Hermes auszuprobieren.

[ALLOY]: Und Hermes's modellagnostische Architektur macht diese Migration glaubwürdig. Wenn du OpenClaw mit Claude als Backend benutzt hast, kannst du auf Hermes umsteigen und dieselben Skills nutzen. Das Skill-Format ist offen — SKILL.md mit YAML-Frontmatter nach dem agentskills.io-Standard. Es ist kein proprietäres Lock-in-Format.

[NOVA]: Das ist die Art von Sache, die nur passiert, wenn ein offenes Ökosystem anfängt zu reifen. OpenAI hatte Actions und Plugins. Anthropic hat MCP. Und jetzt hat Hermes ein Migrations-Tool für OpenClaw-Skills. Die Skills-Portabilität wird zu einer genuinen Wettbewerbsdimension.

[ALLOY]: Und OpenClaw's Antwort darauf ist wahrscheinlich... nichts muss sich ändern. Die Tatsache, dass Hermes von OpenClaw migriert, bedeutet, dass OpenClaw's Modell die Referenz ist. OpenClaw muss nicht zu Hermes migrieren. Aber OpenClaw sollte beobachten, wie Hermes's Skill-Ecosystem sich entwickelt — wenn Hermes einen reichhaltigeren Marketplace aufbaut, könnte das ein Grund für Nutzer werden, es sich anzuschauen.

[NOVA]: Lasst mich euch ein paar konkrete Klassennamen und Dateinamen geben, um diese Diskussion zu verankern.

[ALLOY]: Von Hermes:

[NOVA]: Kern-Agent: `run_agent.py` — `AIAgent`-Klasse.

[NOVA]: State Management: `hermes_state.py` — `SessionDB`-Klasse.

[NOVA]: Tool Registry: `tools/registry.py` — `ToolRegistry`-Singleton, `ToolEntry`-Objekte.

[NOVA]: Tool Discovery: `model_tools.py` — `_discover_tools()`-Funktion.

[NOVA]: Tool Dispatch: `registry.dispatch(name, args, kwargs)` — routet zum richtigen Handler.

[NOVA]: Approval-System: `tools/approval.py` — `DANGEROUS_PATTERNS`, `detect_dangerous_command()`.

[NOVA]: Context Compression: `agent/context_compressor.py`.

[NOVA]: Prompt Building: `agent/prompt_builder.py`.

[NOVA]: Prompt Caching: `agent/prompt_caching.py`.

[NOVA]: Session DB: `~/.hermes/state.db`.

[NOVA]: Skill-Verzeichnis: `~/.hermes/skills/`.

[NOVA]: Config: `~/.hermes/config.yaml`.

[NOVA]: Die Tool-Discovery in Hermes ist interessant. `_discover_tools()` importiert Module in einer festen Reihenfolge, und jedes Modul ruft `registry.register()` auf Modulebene auf. Die Modulliste enthält `web_tools`, `terminal_tool`, `file_tools`, `vision_tools`, `mixture_of_agents_tool`, `image_generation_tool`, `skills_tool`, `browser_tool`, `cronjob_tools`, `rl_training_tool`, `tts_tool`, `todo_tool`, `memory_tool`, `session_search_tool`, `clarify_tool`, `code_execution_tool`, `delegate_tool`, `process_registry`, `send_message_tool`, `honcho_tools`, `homeassistant_tool`. Das ist eine sehr umfassende Liste — Hermes ist kein schmales Tool.

[ALLOY]: Und `mixture_of_agents_tool` plus `rl_training_tool` plus `delegate_tool` sagt dir, dass Hermes als Forschungsplattform konzipiert ist. Das sind keine Consumer-Features. `mixture_of_agents` deutet auf Ensemble-Methoden hin, `rl_training` auf Reinforcement Learning from Feedback, `delegate_task` auf Subagent-Spawning. Das ist ein System für Forscher, die mit agentischem RL experimentieren wollen.

[NOVA]: Für Claude Code liegt das Package unter `/opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/`. Das Sandbox-System hat Klassen wie `SandboxLinux`, `SandboxConfig`, `SandboxManager`, `ViolationStore`. Das Berechtigungssystem hat `policySettings`, `userSettings`, `projectSettings`, `localSettings` — geschichtete Berechtigungsquellen mit Regeln für Allow, Deny und Ask. Die Tool-Registry nutzt `alwaysAllowRules`, `alwaysDenyRules`, `alwaysAskRules` — es gibt also ein dreistufiges Berechtigungsmodell: immer erlauben, immer verbieten, immer fragen.

[ALLOY]: Für OpenClaw leben der Gateway-Daemon, Cron-Scheduling, Subagent-Orchestrierung und Channel-Plugins (Discord, Telegram) alle unter `~/.openclaw/`. Die Workspace-Struktur ist projekt-relativ. Skills leben in `~/.openclaw/skills/`. Das LCM-System für Kontext-Komprimierung ist in der Runtime. Das Clawflow-Skill verwaltet Multi-Agent-Workflows.

[NOVA]: Okay. Wir waren gründlich. Gebt uns das Urteil.

[ALLOY]: Nimm Hermes, wenn: du Forscher oder Power-User bist und einen selbstverbessernden Agenten mit echtem Langzeitgedächtnis über Sessions hinweg willst, Modellagnostizität, FTS5-Suche über deinen gesamten Konversationsverlauf, ein reichhaltiges Skill-Ecosystem, zu dem du beiträgst und aus dem du schöpfst, und die Fähigkeit, auf Telegram, Discord, Slack, WhatsApp oder Signal von einem einzigen Gateway aus zu laufen. Hermes ist auch die richtige Wahl, wenn du dich für RL-basiertes Agent-Improvement interessierst — die Atropos-RL-Umgebungen und Trajectory-Kompression deuten auf ein forschungsorientiertes Design hin. Und wenn du bereits OpenClaw-Nutzer bist, bedeutet `hermes claw migrate`, dass du deine Skills mitbringen kannst.

[NOVA]: Nimm Claude Code, wenn: du ein Entwickler bist, der die bestmögliche Hilfe in einem bestimmten Codebase-Verzeichnis willst, lokal laufend, mit der stärksten OS-Level-Sandboxing für gefährliche Operationen. Claude Codes bubblewrap- und Apple-Sandbox-Integration ist die rigoroseste Sandbox-Implementierung der drei. Wenn dein Workflow „Ich bin in einem Verzeichnis, brauche Hilfe, ich vertraue dem Agenten, hier Dateien zu bearbeiten" lautet, ist Claude Code das fokussierteste Tool für diesen Job. Das Trade-off ist Session-Persistenz und Multi-Channel-Präsenz — dafür ist es nicht gebaut.

[ALLOY]: Nimm OpenClaw, wenn du eine persistente persönliche KI willst, die auf deiner Maschine lebt (oder auf einem VPS), sich mit mehreren Messaging-Channels gleichzeitig verbindet, geplante Tasks ausführt, Subagents für Hintergrundarbeit spawned und ein Skill-System hat, das du selbst formst. OpenClaw ist das unix-nativste der drei — es passt natürlich in einen Command-Line-Workflow, es arbeitet mit bestehenden Dotfile- und Workspace-Konventionen, und es ist entworfen, um dein KI-Betriebssystem zu sein, statt nur ein einzelnes Tool. Die Tatsache, dass Hermes ein Migrations-Tool von OpenClaw verschifft, sagt dir, dass das OpenClaw-Skill-Modell die Referenz ist.

[NOVA]: Der tiefere Punkt ist, dass diese drei Systeme drei verschiedene Theorien darüber encodieren, was ein KI-Agent sein sollte. Hermes denkt, ein Agent sollte ein persistenter, selbstverbessernder Forschungsbegleiter mit reichhaltigem Memory und Modellflexibilität sein. Claude Code denkt, ein Agent sollte ein schmales, tief integriertes Entwicklungstool mit starken Safety-Garantien sein. OpenClaw denkt, ein Agent sollte ein persönliches KI-Betriebssystem sein — always-on, multi-surface, multi-agent.

[ALLOY]: Keine dieser Theorien ist falsch. Es sind verschiedene Wetten darauf, wo der Raum hingeht. Die nächsten Jahre werden uns zeigen, welche davon richtig war.

[NOVA]: Eine letzte Sache, bevor wir schließen — viele von euch werden Hermes nach diesemEpisode ausprobieren wollen. Also reded wir über Models. Hermes ist genuin modellagnostisch, aber die Docs sind spezifisch darüber, was am besten funktioniert.

[ALLOY]: Ihr empfohlener Startpunkt ist Claude Sonnet via Anthropic OAuth — und hier ist der clevere Teil: Wenn du bereits Claude Code nutzt, liest Hermes automatisch Claude Codes Credential-Store. Kein separater API-Key-Setup. Du startest `hermes model`, wählst Anthropic, und es funktioniert einfach mit deiner bestehenden Subscription.

[NOVA]: Für kostenlose Optionen hat Hermes First-Class GitHub-Copilot-Support. Wenn du eine Copilot-Subscription hast, kriegst du Zugang zu GPT-5.4, Claude und Gemini über die Copilot-API. GPT-5 und höher routen automatisch über den Responses-API; alles andere nutzt Chat Completions.

[ALLOY]: Der interessanteste kostenlose Pfad ist OpenRouter. Setze einen `OPENROUTER_API_KEY` in deiner dot env-Datei, starte `hermes model`, und du hast Zugang zu über 200 Models. Die Hermes-Docs heben spezifisch hervor, dass einige eingebaute Tools — Vision, Web-Summarization und das Mixture-of-Agents-Tool — ein separates Hilfsmodell nutzen, das standardmäßig Gemini Flash via OpenRouter ist. Also selbst wenn du Claude als Primärmodell nutzt, schaltet ein OpenRouter-Key diese Tools automatisch frei.

[NOVA]: Für lokale Models unterstützt Hermes jeden Ollama- oder vLLM-Endpunkt — dieselbe Config, einfach `OPENAI_BASE_URL` auf deinen lokalen Server zeigen lassen. Und für chinesische Provider spezifisch: Z-dot-AI GLM, Kimi slash Moonshot, MiniMax und Alibaba Cloud Qwen haben alle First-Class Provider-IDs. Kein nachträglicher Gedanke — sie sind in der Kern-Provider-Liste neben Anthropic und OpenAI.

[ALLOY]: Die praktische Antwort für die meisten Menschen: Wenn du Claude Pro oder Max hast, starte mit Anthropic OAuth. Wenn du kostenlos und leistungsstark willst, GitHub Copilot mit GPT-5.4. Wenn du maximale Flexibilität willst und eine kleine API-Rechnung nichts ausmacht, OpenRouter mit Claude Sonnet oder Qwen 3.

[NOVA]: Das war EP021: Inside the Loop. Vollständige Show Notes und Links gibt es unter Toby On Fitness Tech dot com slash podcasts slash episode 21. Ich bin NOVA.

[ALLOY]: Und ich bin ALLOY. Wir sind bald zurück.
