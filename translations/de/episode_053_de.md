[NOVA]: Ich bin NOVA.

[ALLOY]: Und ich bin ALLOY, und das hier ist AgentStack Daily. Heute geht es mit dem Host und der Coding-Oberfläche los: OpenClaw v2026.5.18 und Codex rust-v0.131.0.

[NOVA]: OpenClaw bringt typisierte Plugin-Tools, dialogbewusste Browser-Automatisierung, schnellere Gateway-Bereitschaft, HTTPS-Proxy-Unterstützung, Echtzeit-Android-Talk-Mode, sicherere Medienverarbeitung, stärkere Kanalzustellung und engeres Codex App-Server-Verhalten. Codex bringt besseren TUI-Status, vereinheitlichte Erwähnungen, Plugin-Marketplace-Befehle, Remote-Control-Infrastruktur, konfigurierte Remote-Umgebungen, ein Python SDK und codex doctor.

[ALLOY]: Das ist die nützliche Form dieser Episode. Erst der Agent-Host. Dann die CLI- und App-Server-Schicht, die Entwickler täglich anfassen. Danach macht GitHub Copilot-Agent-Sessions zu etwas, das man von mehreren Stellen aus steuern und mit kleineren Modellen bepreisen kann. Und Anthropic gibt Claudes Websuche reichhaltigere SEC-Filing-Daten für Finanzforschungs-Agents.

[NOVA]: Die praktische Frage ist nicht, ob Agents mehr Features bekommen. Tun sie. Die Frage ist, welche Teile Agent-Arbeit besser observierbar, besser wiederherstellbar und leichter vertrauenswürdig machen, wenn der Run lang, remote, multimodal oder policy-konstrained ist.

[ALLOY]: Also bleiben wir konkret: Plugin-Verträge, Browser-Modal-Zustand, Readiness-Probes, Runtime-Parity-Checks, Voice-Relay-Verhalten, TUI-Status, Permission-Envelopes, Remote-Sessions, Task-Multiplier, Actions-Repair und Source-Metadaten für Finanzansprüche. ...

[NOVA]: Der Agent-Stack-Release-Readout beginnt mit OpenClaw, weil der Host die Stelle ist, wo ein Agent-Stack sich entweder langlebig oder improvisiert anfühlt. Ein Host muss Models, Tools, Kanäle, Browser, Mobile-Clients, Media-Inputs, Permissions und App-Server-Bridges verbinden. Wenn dieser Host-Release Plugin-Shape, Browser-Zustand, Gateway-Readiness, Mobile-Voice und Codex-Integration in einem Durchgang ändert, verdient er den Anfang der Episode.

[ALLOY]: Die erste builder-fokussierte Änderung ist Plugin-Shape. OpenClaw fügt defineToolPlugin und die openclaw plugins init, openclaw plugins build und openclaw plugins validate Befehle für typisierte einfache Tool-Plugins hinzu. Das gibt Plugin-Autoren generierte Manifest-Metadaten, optionale Deklarationen und Context-Factories, anstatt jede kleine Plugin zu bitten, handgeschriebenen Kleber mitzuschleppen.

[NOVA]: Das klingt nach Developer-Ergonomics, und das ist es auch, aber es ist auch ein Zuverlässigkeits-Feature. Tool-Plugins werden viel einfacher zu inspizieren, wenn Manifest und Deklarationen aus einer typisierten Quelle generiert werden. Ein Host kann darüber reasonieren, was ein Plugin exponiert, welchen Kontext es erwartet und welche Form Inputs und Outputs haben sollten. Je weniger undokumentierte Oberflächen ein Tool hat, desto weniger Überraschungen tauchen innerhalb eines Agent-Runs auf.

[ALLOY]: Das ist auch wichtig, weil das Release ältere Rich-Message-Producer-Oberflächen deprecated, einschließlich Legacy-Interactive- und Slack-Directive-Pfade, während es Kanal-Presentations-Capability-Limits hinzufügt. Das ist ein gesünderer Vertrag. Ein Plugin sollte wissen, ob der Kanal ein interaktives Control, einen Rich-Block, eine reine Nachricht, ein Attachment, eine Sprachnotiz oder nur ein schmales Fallback rendern kann.

[NOVA]: Richtig. Der Fehler bei viel Agent-Tooling ist, jeden Kanal wie dieselbe Output-Oberfläche zu behandeln. Ein Web-Chat, ein Discord-Kanal, ein Telegram-Topic, ein Slack-Thread und eine Mobile-Voice-Session haben nicht identische Presentation-Regeln. Wenn ein Plugin annimmt, sie hätten dieselben, produziert der Agent vielleicht ein Objekt, das der Kanal nicht anzeigen kann. Presentation-Capability-Limits lassen den Host sagen, was tatsächlich möglich ist, bevor die finale Response gestaltet wird.

[ALLOY]: Die Browser-Änderungen sind das zweite große Host-Item. Snapshots surfen jetzt Pending- und kürzlich behandelte Modal-Dialogs. Actions können blockedByDialog zurückgeben, wenn ein Modal sich öffnet. Und browser dialog mit einer dialog ID kann einen Pending-Dialog beantworten. Das ist genau die Art von kleiner Zustandsverbesserung, die Browser-Agents vor vagen Fehlern bewahrt.

[NOVA]: Browser-Automatisierung scheitert oft auf langweilige Art. Ein Klick funktioniert nicht, weil ein Alert sich geöffnet hat. Ein Form-Submit scheint festzustecken, weil ein Confirm-Dialog die Seite übernommen hat. Ein Agent versucht weiter, mit veraltetem Seiten-Zustand zu interagieren, weil er das Modal nicht sehen kann, das ein Mensch sofort bemerken würde. Indem Dialoge als expliziter Zustand repräsentiert werden, gibt die Browser-Schicht dem Agent eine echte nächste Aktion, anstatt es zu zwingen, aus einem Timeout zu inferieren.

[ALLOY]: Der wichtige Ausdruck ist expliziter Zustand. Ein Modal ist nicht einfach Rauschen obendrauf auf der Seite. Es verändert den Interaktionsvertrag der Seite. Wenn eine Aktion blockedByDialog zurückgibt, kann der Agent aufhören so zu tun, als hätte er ein normales DOM-Problem, und den Dialog direkt behandeln.

[NOVA]: Das macht Browser-Agents auch leichter zu auditieren. Wenn das Transkript eines Runs sagt, dass die Aktion durch einen Dialog blockiert wurde, kann der Operator verstehen, warum eine Sequenz pausiert hat. Wenn der Host nur einen Klickfehler meldet, ist der Debugging-Pfad viel schlimmer: Netzwerk, Selector, iFrame, Timing, Auth, Page-Crash oder etwas ganz anderes.

[ALLOY]: Gateway-Startup und Proxy-Verhalten sind als nächstes dran. OpenClaw überlappt jetzt Startup-Logging und Plugin-Service-Startup mit Kanal-Sidecars, während es die readyz-Sidecar-Gating beibehält. Restart-Traces führen Probe-, Config-, Runtime- und Resource-Count-Kosten auf, ohne Readiness-Semantik zu ändern.

[NOVA]: Das ist eine subtile, aber wertvolle Operator-Änderung. Schnelleres Startup ist nützlich, aber das wichtigere Stück ist Evidenz. Wenn ein Restart langsam ist, muss ein Operator wissen, ob die Kosten bei Probe-Zeit, Config-Load, Runtime-Startup, Sidecar-Arbeit, Plugin-Service-Startup oder Resource-Counting liegen. Agent-Infrastruktur ist voll von beweglichen Teilen, also muss Readiness sowohl konservativ als auch erklärbar sein.

[ALLOY]: Und das Beibehalten der Readiness-Semantik ist wichtig. Es ist einfach, einen Service zu beschleunigen, indem man sagt, er sei bereit, bevor die Dependencies bereit sind. Das ist keine Verbesserung. Es verschiebt den Fehler nur downstream. Die nützliche Version ist, Arbeit zu überlappen, wo sicher, aber trotzdem readyz bedeuten zu lassen, dass der Host die Flächen bedienen kann, die er verspricht.

[NOVA]: Die Proxy-Arbeit ist auch praktisch. Das Release fügt HTTPS-managed Forward-Proxy-Endpunkte und scoped proxy.tls.caFile-Trust hinzu. Das gibt Deployments einen saubereren Weg, Traffic durch TLS-inspizierte oder private Proxy-Pfade zu routen, ohne Proxy-Konfiguration zu einer globalen Trust-Entscheidung zu machen.

[ALLOY]: Das ist wichtig in Enterprise- und Laborumgebungen, wo ausgehender Traffic nicht einfach offenes Internet ist. Agents rufen APIs auf, holen Seiten, greifen auf Docs zu, erreichen Model-Endpunkte und bewegen Media. Wenn der Proxy-Pfad speziellen Trust erfordert, sollte dieser Trust auf die Proxy-Konfiguration scoped sein. Er sollte nicht leichtsinnig Trust über die gesamte Runtime hinweg ausweiten.

[NOVA]: Der QA-Lab-Block ist wahrscheinlich der wichtigste Teil für alle, die Agent-Hosts ausliefern. OpenClaw fügt First-Hour-20-Turn- und optionale 100-Turn-Runtime-Paritätsszenarien hinzu, den openclaw qa suite Runtime-Parity-Tier, Tool-Fixture-Abdeckung durch openclaw qa coverage tools, Live-Runtime-Token-Effizienz-Artefakte und eine strikte Hürde für erforderliche OpenClaw-dynamische Runtime-Tool-Drift im Standard-Codex-vs-Pi-Tier.

[ALLOY]: Um es einfach auszudrücken: Das Release prüft, ob verschiedene Runtimes sich ähnlich genug verhalten, wenn sie unter echtem Agent-Druck stehen. Das ist viel nützlicher als nur zu prüfen, ob der Prozess startet. Agent-Regressionen zeigen sich oft als Tool-Vokabular-Drift, schlechte Tool-Auswahl, veränderte Token-Nutzung, fehlende Fixtures oder ein Runtime, der die falsche Oberfläche wählt.

[NOVA]: Genau. Ein Smoke-Test kann sagen, dass der Server lebt, während der Agent leise schlechter wird. Runtime-Paritätsszenarien stellen eine härtere Frage: Wenn dieselbe Aufgabe verschiedene Runtime-Pfade durchläuft, bleiben dann die Tool-Auswahl, Fähigkeiten und Ausgaben innerhalb eines erwarteten Rahmens? So fängt man die Art von Release-Regression, die Nutzer beschreiben als "der Agent fühlt sich jetzt anders an".

[ALLOY]: Die 20-Turn- und 100-Turn-Form zählt, weil kurze Agent-Tests zu nachsichtig sind. Ein Ein-Turn-Tool-Aufruf sagt dir nicht, ob Kontext-Kürzung, Tool-Zustand, Berechtigungen, Fehlerwiederherstellung und Modell-Routing nach einer echten Session stabil bleiben. Längere Szenarien decken die schleichenden Fehler auf.

[NOVA]: Android Talk Mode bekommt auch eine große Runtime-Änderung. Die Android-App schaltet Talk Mode auf Echtzeit-Gateway-Relay-Voice-Sessions mit Streaming-Mikrofoneingabe, Echtzeit-Audiowiedergabe, Tool-Ergebnis-Bridging und Untertitel-Anzeige auf dem Bildschirm.

[ALLOY]: Das macht mobile Stimme zu einer aktiven Session-Oberfläche. Es ist nicht nur Sprache-zu-Text rein und Text-zu-Sprache raus. Eine Echtzeit-Voice-Session kann Tool-Ergebnisse zurück durch das Gateway tragen, ein Transkript sichtbar halten und den Assistenten kontinuierlich wirken lassen, während Tools laufen.

[NOVA]: Das technische Risiko liegt bei Unterbrechung und Timing. Streaming-Mikrofoneingabe braucht saubere Stornierung. Echtzeit-Audiowiedergabe muss stoppen, wenn der Nutzer unterbricht. Tool-Ergebnis-Bridging muss verhindern, veraltete Ausgabe zu lesen, nachdem der Nutzer die Richtung geändert hat. Und Transkripte müssen eng genug übereinstimmen, dass der Nutzer erkennen kann, was der Agent gehört und was er getan hat.

[ALLOY]: Deshalb ist mobile Stimme eine Host-Funktion, nicht nur eine Client-Funktion. Der Client kann Audio aufnehmen, aber der Host muss Sitzungsidentität, Tool-Events, Streaming-Antworten, Stornierung und Kanalrichtlinie koordinieren. Wenn der Host schlampig ist, wird das Voice-UX verwirrend, selbst wenn das Audio selbst gut klingt.

[NOVA]: Der Fixes-Block ist dort, wo viele Produktions-Upgrades das Release spüren werden. Generierte Medien-Vervollständigungen kehren jetzt zu Telegram-Forumthemen zurück, indem Topic-IDs über Requester-Agent-Übergabe erhalten bleiben. Bildmetadaten-Probing vermeidet das Aufrufen externer Decoder-Delegates bei unbekannten Bytes. Sharp wird mit Fallbacks auf native Imaging-Tools, ImageMagick, GraphicsMagick oder ffmpeg installiert.

[ALLOY]: Das sind keine glamourösen Punkte, aber es sind die Dinge, die verhindern, dass Agent-Systeme Arbeit verlieren. Wenn eine generierte Bildantwort im falschen Topic landet, bricht das Nutzererlebnis zusammen. Wenn Metadaten-Probing externe Decoder-Delegates bei unbekannten Bytes aufruft, trägt die Medienverarbeitung unnötiges Sicherheits- und Zuverlässigkeitsrisiko. Wenn Bildverarbeitung von einem nativen Modulpfad abhängt und dieser fehlschlägt, wird die gesamte Medienfunktion brüchig.

[NOVA]: Discord-Voice-Sessions bekommen auch Aufmerksamkeit. Das Release hält Follow-up-Turns mit OpenAI Realtime am Laufen und puffert Assistant-Playback vor, um ruckelige Starts zu reduzieren.

[ALLOY]: Der Prebuffer-Punkt ist klein, aber menschlich. Echtzeit-Stimme wird nach Timing beurteilt. Wenn der Assistant mit abgehacktem Audio startet oder den nächsten Turn nicht hört, verliert der Nutzer schnell das Vertrauen. Ein technisch korrekter Voice-Stack fühlt sich trotzdem kaputt an, wenn das Turn-Taking holprig ist.

[NOVA]: Message- und TTS-Direktiven werden angewendet, bevor Message-Tool-Sends die Zustellpfade erreichen, sodass Rooms, die sich für Voice-Notes entscheiden, Voice-Notes statt roher Tags bekommen. Das ist ein weiterer Kanalvertrags-Fix. Die Direktive sollte die Zustellung formen, bevor die Nachricht gesendet wird, nicht als Text zum Nutzer durchsickern.

[ALLOY]: OpenClaws Codex-App-Server-Reparaturen sind besonders relevant für gemischte Agent-Stacks. Aktuelle eingehende Bildanhänge hydrieren vor gereihten Runs, sodass Responses-gestützte Agents Kanalbilder als natives Vision-Input erhalten. Native Code-Modus bleibt verfügbar, ohne Code-Modus-nur zu erzwingen, was es OpenClaw-Dynamic-Tool-Turns erlaubt, durch die App-Server-Bridge abzuschließen.

[NOVA]: Der Netzwerkzugang bleibt für Sandbox-Codex-Code-Mode-Turns erhalten, wenn die OpenClaw-Sandbox ausgehenden Egress erlaubt. Die per-Agent-Code-Mode-Konfiguration wird in Schema, Runtime-Katalog-Aktivierung und Modell-Payload-Filterung respektiert. Eingeschränktes Chat- oder Sender-MCP-Surface wird jetzt geschlossen deaktiviert, indem natives Code-, App-, Environment- und User-MCP-Surfaces für eingeschränkte Turns deaktiviert werden.

[ALLOY]: Dieser letzte Teil ist die Sicherheitsgrenze. In einem Agent-Host sollten eingeschränkte Turns sich nicht einfach darauf verlassen, dass das Modell sich gut verhält. Der Runtime sollte Oberflächen entfernen, die der Sender nicht verwenden darf. Geschlossen-Fehlern bedeutet, dass ein eingeschränkter Nutzer nicht versehentlich nativen Code, lokale App-Zugriffe, Environment-Zugriffe oder User-MCP-Surfaces erhält.

[NOVA]: Der Bildhydrierungs-Fix ist auch wichtig. Ein Nutzer, der einen Screenshot durch einen Kanal sendet, erwartet, dass der Agent den Screenshot sieht, nicht einen Platzhalter oder einen Dateipfad, den das Modell nicht inspizieren kann. Das Hydrieren von Bildern vor gereihten Runs hält den multimodalen Kontext an den eigentlichen Turn gebunden.

[ALLOY]: Und das Erhalten des Sandbox-Netzwerkzugangs, wenn die Richtlinie es erlaubt, ist wichtig, weil Code-Mode-Aufgaben oft Paket-Metadaten, Dokus, APIs oder Tests brauchen, die externe Ressourcen aufrufen. Der Host sollte Netzwerkzugang nicht versehentlich entfernen, wenn die konfigurierte Sandbox-Hülle es erlaubt.

[NOVA]: Die Migrationsnotizen sind konkret. Die minimal unterstützte Node.js 22-Linie steigt auf 22.19. Pi-Pakete wechseln zu 0.75.1. Docker- und Podman-Builds sollten OPENCLAW_IMAGE_APT_PACKAGES bevorzugen, während OPENCLAW_DOCKER_APT_PACKAGES als Legacy-Fallback bleibt. Das Obsidian-Skill zielt jetzt auf den offiziellen obsidian CLI statt auf das Drittanbieter-obsidian-cli. Der Repo-lokale Codex-Closeout-Review-Skill und Helper werden zu autoreview umbenannt.

[ALLOY]: Der praktische Upgrade-Pfad ist, die echten Oberflächen zu testen, die sich geändert haben. Baue und validiere ein kleines Plugin. Löse ein Browser-Modal aus und stelle sicher, dass der Dialogpfad sichtbar ist. Starte das Gateway neu und inspiziere die Readiness-Spuren. Übe den HTTPS-Proxy-Pfad, wenn dein Deployment privates Trust verwendet. Probiere Android Talk Mode mit Unterbrechung. Sende Medien durch die Kanäle, die du tatsächlich nutzt. Führe Codex-App-Server-Turns mit Bildern, Sandbox-Netzwerk, Code-Mode und eingeschränkter Sender-Richtlinie aus.

[NOVA]: Ein guter Builder-Workflow nach diesem Release ist, eine reale Aufgabe pro Oberfläche zu wählen. Für Plugins baust du ein kleines Tool, das Eingaben liest, strukturierte Ausgaben zurückgibt und nur den benötigten Kontext deklariert. Für Browser-Automatisierung baust du eine Testseite, die einen Alert, ein Confirm und ein Prompt öffnet, dann verifizierst du, dass der Agent den blockierten Dialogzustand sehen und beantworten kann. Für Media sendest du ein kleines Bild, ein malformed Bild und eine generierte Bildeanfrage über den tatsächlich unterstützten Kanalpfad.

[ALLOY]: Für Gateway-Ready-ness sollte der Workflow einen Neustart unter normaler Last enthalten, dann einen Neustart mit einem langsamen Sidecar- oder Plugin-Service. Das Ziel ist nicht nur ein schneller Boot. Das Ziel ist zu verstehen, welcher Probe-, Config-, Runtime- oder Ressource-Schritt Zeit kostet. Wenn ein Team OpenClaw als interne Infrastruktur ausliefert, wird dieser Neustart-Trace Teil des Support-Workflows, wenn jemand sagt, dass der Agent-Host nach dem Deploy langsam ist.

[NOVA]: Für Android Talk Mode ist der nützliche Workflow ein echter Unterbrechungstest. Starte eine Voice-Session, bitte um eine Tool-gestützte Antwort, unterbrich während Audio abgespielt wird, dann stell eine Folgefra­ge, die vom vorherigen Tool-Ergebnis abhängt. Ein gutes Ergebnis ist nicht nur, dass Sprache funktioniert. Ein gutes Ergebnis ist, dass Cancellation funktioniert, Transkripte kohärent bleiben und Tool-Ergebnisse nicht als stale Speech ankommen, nachdem der User weiterging.

[ALLOY]: Für Restricted Sender Policy sollte der Build-Workflow bewusst adversariell sein. Versuche einen Turn von einem restricted Sender, der lokalen Code, App-Zugriff, Environment-Zugriff und User MCP-Zugriff anfragt. Das korrekte Verhalten ist keine höfliche Ablehnung vom Model. Das korrekte Verhalten ist, dass diese Runtime-Oberflächen abwesend sind, bevor das Model nach ihnen greifen kann.

[NOVA]: Das ist der OpenClaw-Readout: Host-Arbeit, die Plugins typisierter, Browser-Fehler expliziter, Startup beobachtbarer, Proxy-Trust scoped, QA runtime-aware, Mobile Voice realtime, Media sicherer, Kanäle zuverlässiger und Codex-Integration policy-aware macht. ...

[ALLOY]: Die zweite Hälfte des Agent-Stack-Release-Readouts ist Codex rust-v0.131.0. Wenn OpenClaw die Host-Oberfläche ist, ist Codex die Coding-Oberfläche: die TUI, der App-Server, der Remote-Control-Pfad, das SDK, die Sandbox, Auth, State und die Tool-Bridge, in der Entwickler leben.

[NOVA]: Die erste sichtbare Änderung ist TUI-Status. Codex exponiert jetzt datengetriebene Service-Tier-Befehle, blended Token-Usage, Permissions und Approval-Mode, effektive Workspace-Roots und responsive Markdown-Tables. Das klingt nach Display-Arbeit, aber es ändert, wie Operatoren lange Sessions managen.

[ALLOY]: Während eines langen Coding-Runs willst du die Permission-Envelope kennen. Ist der Agent in einer Read-only-Posture, einer Workspace-write-Posture oder etwas Permissiverem? Welcher Approval-Mode ist tatsächlich aktiv? Welche Workspace-Roots sind effektiv? Welches Service-Tier ist in Verwendung? Wie viel vom Token-Budget wurde ausgegeben? Wenn die TUI diese Fakten zeigt, muss der Operator sie nicht aus verstreuten Configs und Memory rekonstruieren.

[NOVA]: Das ist wichtig, weil die Failure-Cases teuer sind. Wenn ein User denkt, der Agent kann ein Verzeichnis beschreiben, aber der effektive Root ein anderer ist, können Edits am falschen Ort landen oder unerwartet fehlschlagen. Wenn der Approval-Mode missverstanden wird, kann ein Task auf Prompts blockieren, die der Operator nicht erwartet hat. Wenn Token-Usage invisible ist, kann eine lange Session in teures oder degraded Behavior driften ohne Warnung.

[ALLOY]: Mentions werden auch breiter. At-Search deckt jetzt Files, Directories, Plugins und Skills in einem Picker ab, backed von App-Server-Plugin-Metadata. Das passt zu, wie Builder denken. Das Ding, das du brauchst, könnte eine Source-Datei sein, ein Folder, ein lokaler Skill oder eine Plugin-Capability. Das Interface sollte das nicht in vier separate Discovery-Paths zwingen.

[NOVA]: Die Vorsicht ist Context-Discipline. Ein unified Picker ist nützlich, weil er Friction reduziert, aber Friction schützte die Session manchmal vor Bloat. Der beste Use Case ist, das kleinste Artifact anzuhängen, das den benötigten Context trägt: ein File, ein Directory, ein Skill oder eine Plugin-Reference, nicht ein Haufen von allem, das adjacent aussieht.

[ALLOY]: Plugin-Workflows gehen voran. Codex fügt Marketplace-CLI-Commands, version-aware Sharing, Share-Checkout, klarere Shared-Workspace-Buckets und default-enabled Plugin-Hooks hinzu. Das ist ein Shift von Plugins als loose lokale Folders hin zu Plugins als managed Development-Artifacts.

[NOVA]: Version-aware Sharing ist eine große Sache. Wenn zwei User oder zwei Maschinen über dasselbe Plugin sprechen, müssen sie wissen, ob sie tatsächlich dieselbe Version verwenden. Share-Checkout und klarere Workspace-Buckets helfen, das explizit zu machen. Default-enabled Hooks machen die Experience smoother, aber sie heben auch die Trust-Bar.

[ALLOY]: Hooks sind powerful, weil sie um den Development-Prozess herum laufen. Das bedeutet, dass Provenance, Scope, Version-Gates und Workspace-Boundaries relevant sind. Ein Plugin-Marketplace ist nicht nur ein Convenience-Feature. Es wird Teil der Supply Chain für Agent-Behavior.

[NOVA]: Remote-Work ist eines der großen Pieces in diesem Codex-Release. Das Release fügt daemon-managed codex remote-control, Runtime-Enable- und Disable-APIs, Status-Reads, registry-backed und configured Remote-Environments und App-Server-API-Contracts für Remote-Environments und Desktop-owned Config-Namespaces hinzu.

[ALLOY]: Remote-Control ist nicht nur, das woanders laufen zu lassen. Ein echtes Remote-Environment braucht Identity, Lifecycle, Status, Cleanup, Config-Boundaries und Permission-Behavior. Wenn die nicht explizit sind, wird Remote-Agent-Work ein Shell-Process mit einem nicer Label.

[NOVA]: Die daemon-managed Shape ist wichtig, weil langlaufende Agent-Work einen Coordinator braucht. Der Daemon kann Status exponieren, Runtime-Enablement managen und Remote-Control-State separat von einer einzelnen Terminal-Session halten. Das ist der Unterschied zwischen einem Feature, das in einem Demo funktioniert, und einem Feature, das den täglichen Use überlebt.

[ALLOY]: Konfigurierte Remote-Environments sind auch für Teams und Power-User wichtig. Ein Remote-Environment sollte nicht jedes Mal ein improvisiertes Target sein. Es sollte named, discoverable, policy-aware und recoverable sein. Der App-Server-Contract gibt Integrationen etwas Strukturiertes, das sie aufrufen können, statt Terminal-Output zu scrapen.

[NOVA]: Das Python-SDK ist jetzt openai-codex und importiert als openai_codex. Es beinhaltet pinned Runtime-generated Types, concurrent Turn-Routing, Approval-Modes und Integration-Coverage. Das gibt Python-Anwendungen einen echten Path, Codex-Turns zu fahren, ohne die CLI als text-only Subprocess zu behandeln.

[ALLOY]: Turn-Routing ist der Key-Mechanismus. Wenn eine App mehr als einen Agent-Turn fährt, braucht sie IDs und strukturierte Events. Sonst können Approvals, Tool-Activity, Notifications und Outputs überkreuzen. Concurrent Work ohne strukturiertes Routing ist, wo subtile Bugs awful werden: ein Approval, das für einen Turn gedacht war, wird mit einem anderen assoziiert, oder ein Tool-Event erscheint unter dem falschen Task.

[NOVA]: Genehmigungsmodi müssen auch in einem SDK explizit sein. Eine Python-App, die Codex einbettet, muss wissen, ob ein Turn um Erlaubnis bitten kann, ob sie Tools ausführen kann, ob sie schreiben kann und wie diese Genehmigungen an die steuernde Anwendung weitergegeben werden. Das ist keine optionale Verrohrung. Es ist das Sicherheitsmodell.

[ALLOY]: Codex fügt außerdem codex doctor für Diagnosen über Runtime, Auth, Terminal, Netzwerk, Config und lokalen Zustand hinzu. Das ist die Art von Befehl, die klein klingt, bis das erste chaotische Upgrade passiert.

[NOVA]: Ein fehlgeschlagener Coding-Agent kann durch veraltete Authentifizierung, Terminal-Eigenheiten, Netzwerkrichtlinien, Config-Konflikte, Probleme mit der lokalen Zustandsdatenbank, Runtime-Mismatches, Sandbox-Verhalten oder App-Server-Start fehlschlagen. Ohne Diagnosen wird Support zum Ratespiel. Ein Doctor-Befehl kann supportfertige Beweise sammeln und den Weg von „es ist kaputt" zu „das ist die kaputte Schicht" verkürzen.

[ALLOY]: Die Version macht auch App-Server- und lokalen Zustandsstart sicherer durch das Beibehalten von SQLite-Daten, ein Schließen bei无法 öffnen des Zustands, das Hinzufügen von Wiederherstellungspfaden und das Abfedern von optionalen Metadaten-Sync-Fehlern. Diese Kombination ist gute Ingenieursarbeit. Durable State beibehalten. Nicht unsicher fortfahren, wenn erforderlicher Zustand nicht geöffnet werden kann. Wiederherstellen, wenn möglich. Optionalen Metadaten-Sync nicht den primären Pfad zerstören lassen.

[NOVA]: Der Hardening-Block ist breit. Windows-Sandbox-Verhalten verbessert sich bei deny-read-Regeln, scoped write roots, ineffektiver Firewall-Policy und PowerShell-Edge-Cases. Verwaltete Leseeinschränkungen überstehen Permission Escalation. Workspace-Root-Permission-Profil-Auflösung wird aufgeräumt.

[ALLOY]: Git und Auth-Zuverlässigkeit verbessern sich durch Root-Worktree-Hooks, Ignorieren von Repo-Hook- und Fsmonitor-Config in Helper-Befehlen, Binden von lokalen MCP OAuth-Callbacks und Widerrufen von abgelösten Login-Tokens. Remote und Windows Cleanup bekommen längere Exec-Server-Transport-Timeouts, leiseres Taskkill und nicht-queuiertes Plugin-Lesen.

[NOVA]: Das Muster ist Recoverability. Ein Coding-Agent ist nur nützlich, wenn er in echten Repositories, echten Auth-Flows, echten Windows-Shells, echten Sandbox-Policies und echtem App-Server-Zustand arbeiten kann. Diese Umgebungen sind chaotisch. Die Version geht weniger um eine flashy capability und mehr darum, lange Sessions beobachtbar, recoverbar und sicherer zu machen.

[ALLOY]: Der Migrationsrat für Codex ist einfach: nach dem Update die TUI-Statuszeile, Service-Tier-Befehle, Unified Mentions, Plugin Marketplace und Share-Befehle, Remote-Control-Flows, konfigurierte Remote-Umgebungen, Python SDK Turn Routing, codex doctor, Windows-Sandbox-Fälle wenn relevant und App-Server-Zustandswiederherstellung durchexerzieren.

[NOVA]: Auch Genehmigungs-Sichtbarkeit testen. Eine Session mit dem erwarteten Genehmigungsmodus und Workspace-Roots starten, dann verifizieren, dass die TUI dieselbe Realität zeigt. At-Sign-Mentions mit einer Datei, einem Verzeichnis, einem Skill und einem Plugin verwenden, um sicherzustellen, dass der Picker nützlich ist ohne den Turn zu überladen. Bei Remote-Umgebungen Statusreads und Cleanup prüfen, nicht nur den Start.

[ALLOY]: Für SDK-Builder: Concurrent Turns bewusst testen. Zwei kleine Jobs laufen lassen, Genehmigung oder Tool-Aktivität in beiden auslösen und sicherstellen, dass Notifications unter den richtigen IDs landen. Das ist, wo ein strukturiertes SDK Vertrauen verdient.

[NOVA]: Es gibt auch einen sauberen Build-Workflow für den Unified Mention Picker. Mit einer engen Datei-Mention starten, wenn die Aufgabe lokal ist. Zu einer Verzeichnis-Mention nur wechseln, wenn der Agent benachbarte Tests oder verwandte Module braucht. Eine Skill-Mention verwenden, wenn der wichtige Kontext ein Verfahren ist, kein Quellcode. Eine Plugin-Mention verwenden, wenn die Aufgabe von einer Capability abhängt. Dieser Workflow hält die Session fokussiert und macht den neuen Picker trotzdem wertvoll.

[ALLOY]: Für Plugin-Sharing sollte der Workflow Versionschecks enthalten. Ein Plugin teilen, es in einem zweiten Workspace auschecken, die geladene Version verifizieren, dann etwaige default-enabled Hooks in einem kleinen Repository durchexerzieren, bevor man ihnen in einem größeren vertraut. Glattes Plugin-Sharing ist nützlich, aber es sollte Hook-Verhalten nicht unsichtbar machen.

[NOVA]: Für Remote-Control-Arbeit einen Lifecycle-Test bauen. Eine Session starten, Remote Control aktivieren, Status lesen, eine kleine Korrektur von einer zweiten Surface senden, eine Genehmigungsanfrage beantworten, Remote Control deaktivieren und Cleanup bestätigen. Das ist die Art von Workflow, die mismatched State erwischt. Wenn Start funktioniert aber Status falsch ist, wird die Feature schwer zu bedienen sein. Wenn Deaktivieren funktioniert aber Cleanup alten State hinterlässt, kann die nächste Session Verwirrung erben.

[NOVA]: Also der Codex-Readout: klarerer Betriebszustand in der TUI, breiterer Kontext-Anhang durch Unified Mentions, mehr verwaltetes Plugin-Sharing, Daemon-backed Remote Control, konfigurierte Remote-Umgebungen, ein Python SDK mit strukturiertem Turn Routing, Diagnostik und eine lange Liste von Sandbox-, Auth-, Git-, Windows-, App-Server- und Zustandsreparaturen.

[ALLOY]: Gepaart mit OpenClaw zeigt es in dieselbe Richtung. Agent-Tools werden weniger magisch und mehr inspectable. Der Host kann erklären, was er rendern kann und welcher Dialog ihn blockiert hat. Die CLI kann erklären, welcher Permission-Mode und welche Workspace-Roots aktiv sind. Das SDK kann Concurrent Turns nach ID routen. So wird Agent-Arbeit einfacher zu betreiben. ...

[NOVA]: GitHub macht Copilot Agents zu einer Multi-Surface, günstigeren Work Queue mit drei Mai-18-Updates: Remote Control für Copilot CLI-Sessions ist über Mobile, Web, VS Code und JetBrains allgemein verfügbar; Copilot Cloud Agent Tasks können günstigere Models für einfachere Arbeit nutzen; und fehlschlagende GitHub Actions können Reparaturarbeit von Copilot von der Workflow-Logs-Seite übernehmen.

[ALLOY]: Die Remote-Control-Mechanik ist explizit. Ein User kann mit copilot remote starten, Remote Control innerhalb einer Session mit remote on aktivieren oder remoteSessions in der Copilot-Settings-Datei konfigurieren. Einmal attached, kann die Remote Surface Session-Aktivität streamen, queuierte Eingabe akzeptieren, Genehmigungsaufforderungen beantworten, eine Session stoppen und den User die Arbeit weg vom ursprünglichen Terminal steuern lassen.

[NOVA]: Das ändert die Form von CLI-Agent-Arbeit. Das lokale Terminal bleibt der Ausführungsanker, aber Supervision kann sich bewegen. Ein Builder kann eine Aufgabe am Schreibtisch starten, dann von Mobile oder einem Browser den Fortschritt prüfen, eine Genehmigungsanfrage beantworten, eine Korrektur queuen oder die Session stoppen, ohne im selben Editor zu sein.

[ALLOY]: Die Einschränkungen matter. Die Maschine, die die Session laufen hat, muss online bleiben, und GitHubs Docs weisen auf Keep-Alive für längere Arbeit hin. Sessions sind user-spezifisch. Business- und Enterprise-Nutzung kann von Admin-Policies für Remote Control und CLI-Features abhängen. Das ist also kein abgelöstes Cloud-Computing. Es ist eine Live-Session mit einer Remote-Control-Ebene.

[NOVA]: Diese Unterscheidung ist wichtig. Remote Steering ist nützlich, weil es den lokalen Kontext beibehält und Supervision sich bewegen kann. Aber es bedeutet auch, dass die lokale Umgebung, Branch-State, Credentials, Netzwerk und Terminal-Session noch wichtig sind. Wenn der Laptop schläft, läuft die Session nicht magisch woanders.

[ALLOY]: Das zweite GitHub-Update ist die Auswahl günstigerer Modelle für Copilot-Cloud-Agent-Aufgaben. Claude Haiku 4.5 und GPT-5.4-mini sind mit einem 0,33-fachen Multiplikator für einfachere Arbeiten verfügbar. Das ist die richtige Produktrichtung, weil Agent-Aufgaben nicht alle gleich schwer sind.

[NOVA]: Ein kleiner Dependency-Bump, ein Lint-Fix, eine Tippfehlerkorrektur, eine mechanische Refaktorierung, ein Test-Expectation-Update oder ein straightforward durchfallender Test benötigt nicht immer das stärkste Modell. Ein günstigeres Modell kann die Aufgabe erledigen und dabei Budget für die Jobs sparen, die tieferes Reasoning brauchen: mehrdeutige Bugs, Architekturänderungen, sicherheitskritische Patches oder Multi-File-Verhaltensänderungen.

[ALLOY]: Die Entry Points sind hier entscheidend. GitHub ermöglicht Modellauswahl über unterstützte Flows wie das Zuweisen eines Issues, das Erwähnen von Copilot in einem Pull-Request-Kommentar, den Start von Agent-Surfaces, GitHub Mobile oder Raycast. Wo kein Picker existiert, wird Auto verwendet.

[NOVA]: Das bedeutet, dass Builder die Modellauswahl als Teil der Aufgabentriage behandeln sollten. Wenn der Entry Point einen Picker bietet, sollte man bewusst wählen. Bei mechanischen Aufgaben nutze man das kleinere Modell. Bei Design-lastigen oder riskanten Aufgaben zahle man für den stärkeren Ansatz. Ist kein Picker verfügbar und wird Auto verwendet, sollte man das Ergebnis mit dieser Unsicherheit im Hinterkopf überprüfen.

[ALLOY]: Die dritte Änderung ist die Einklick-Reparatur für durchfallende GitHub Actions. Von einer Workflow-Run-Log-Seite können Copilot Business- und Enterprise-Abonnenten auf „Mit Copilot reparieren" klicken. Der Cloud-Agent untersucht den Fehler, pusht einen Fix auf den Branch und markiert den Benutzer zur Überprüfung.

[NOVA]: Das ist ein starker Agent-Entry-Point, weil der Context-Bundle stark ist: durchfallende Job-Logs, Branch-State, Repository-Anweisungen und eine Cloud-Entwicklungsumgebung. Statt Logs in den Chat zu kopieren, delegiert der Benutzer von dem Ort, wo der Fehler bereits sichtbar ist.

[ALLOY]: Aber die Review-Disziplin verschwindet nicht. Ein von einem Agent auf einen Branch gepushtes Fix ist immer noch eine Code-Änderung. Der Reviewer muss überprüfen, ob der Agent die eigentliche Ursache behoben, das Design bewahrt, breite Hacks vermieden und nicht einfach für grünes CI optimiert hat.

[NOVA]: Das ist besonders wichtig bei Actions-Failures. Die einfachste Lösung könnte sein, einen Test zu lockern, einen Fall zu überspringen, eine alte Abhängigkeit zu pinnen oder die CI-Konfiguration so zu ändern, dass ein Bug versteckt wird. Das richtige Fix kann tiefer liegen. Der Agent kann einen Entwurf erstellen, aber die menschliche Überprüfung behält immer noch das technische Urteil.

[ALLOY]: Die größere Produktrichtung ist klar. GitHub wandelt Copilot-Agents in eine Work-Queue um, die sich über Oberflächen erstreckt. Lokale CLI-Sessions können remote gesteuert werden. Cloud-Aufgaben können kleinere Modelle nutzen, wenn die Arbeit einfach ist. CI-Failures können zu delegierten Reparaturjobs von der Log-Seite werden.

[NOVA]: Für Teams ist die Policy-Schicht wichtig. Remote-Kontrolle, Cloud-Agents, Modellauswahl und Actions-Reparatur benötigen alle Admin-Einstellungen, Repository-Anweisungen und Review-Normen. Ohne diese ist es einfach, eine Agent-Queue zu erstellen, die bequem aber inkonsistent ist.

[ALLOY]: Das nützliche Build-Pattern ist es, Aufgaben vor der Zuweisung zu klassifizieren. Einfache Branch-Wartung kann an ein günstigeres Cloud-Modell gehen. CI-Failure-Reparatur kann von den Workflow-Logs starten. Arbeit, die vom lokalen State des Entwicklers abhängt, kann im CLI bleiben, aber remote überwacht werden. Riskante Design-Arbeit benötigt immer noch stärkere Modelle und engere Reviews.

[NOVA]: Und die Überwachungsoberfläche sollte zur Arbeit passen. Wenn der Agent nach Berechtigungen fragt, kann eine mobile Genehmigung für eine einfache bekannte Operation ausreichen. Wenn die Änderung breit ist, ist ein Desktop-Review besser. Das Ziel ist nicht, jede Agent-Aufgabe remote zu machen. Es geht darum, dass sich die Kontrollebene bewegen kann, wenn das tatsächlich hilft.

[ALLOY]: Ein nützlicher Team-Workflow ist es, nach Kosten und Risiko zu routen. Nutze die kleineren Cloud-Agent-Modelle für enge Fixes mit klaren Tests. Nutze stärkere Modelle, wenn das Issue mehrdeutiges Verhalten, Sicherheitsimplikationen oder breiten Design-Impact hat. Nutze Remote-CLI-Steuerung, wenn die Aufgabe lokalen State benötigt, aber der Mensch nicht im Terminal sitzen kann. Nutze Actions-Reparatur, wenn der Failure-Kontext bereits in CI-Logs konzentriert ist.

[NOVA]: Der Review-Workflow sollte genauso explizit sein. Für eine Änderung mit günstigem Modell überprüfe man, ob der Agent in der engen Aufgabe geblieben ist. Für eine Remote-CLI-Änderung überprüfe man das lokale Diff und die Befehlshistorie. Für eine Actions-Reparatur überprüfe man, ob der Agent Produktcode, Tests, Dependencies oder CI-Konfiguration geändert hat. Die Tatsache, dass der Agent von einem bequemen Entry Point kam, ändert nicht den Review-Standard.

[ALLOY]: Deshalb passen diese GitHub-Updates zum Release-Block. Es sind nicht nur Feature-Ankündigungen. Sie sind Teil derselben operationellen Verschiebung: Agents brauchen Lifecycle-Kontrolle, Policy-Gates, Kosten-Tiers und bessere Entry Points von den Orten, wo Arbeit bereits passiert. ...

[NOVA]: Anthropic gibt Claude Websuche reichhaltigere SEC-Einreichungsdaten für zitierte Finanz-Agents. Die Claude-Platform-Notiz vom 18. Mai ist eng, aber sie ist wichtig für jeden Agent, der Erträge zusammenfasst, öffentliche Unternehmen vergleicht, Due-Diligence-Notizen erstellt oder Risikooffenlegungen überwacht.

[ALLOY]: Der Unterschied zwischen einem generischen Web-Ergebnis und einreichungsbewusster Suche ist die Quellenqualität. Finanz-Research-Agents müssen wissen, ob sie eine 10-K, 10-Q, 8-K, Proxy Statement, Registrierungserklärung oder eine andere Primäreinreichung betrachten. Sie benötigen auch genug Metadaten, um diese Zitation nach der Modellsynthese beizubehalten.

[NOVA]: Der Fehlermodus ist bekannt. Ein Modell durchsucht das Web, findet eine Finanzbehauptung, fasst sie zusammen und verliert die Grenze zwischen Primäreinreichungen, Pressemitteilungen, Analystenkommentaren und Nachrichtenartikeln. Die finale Antwort klingt vielleicht selbstsicher, aber die Evidenzkette ist schwach.

[ALLOY]: Reichhaltigere SEC-Einreichungsdaten helfen der Tool-Schicht, bessere Evidenz in den Modellkontext zu tragen. Sie geben der Anwendung eine bessere Chance, Einreichungsidentität, -typ, -datum, Unternehmen, Quell-URL, zitierten Text und Abruf-Metadaten zu bewahren. Aber die Anwendung muss diese Informationen behalten. Wenn sie alles in Prosa kollabiert, verschwindet der Nutzen.

[NOVA]: Die praktische Empfehlung ist, Suchergebnisse als Evidenz-Objekte zu behandeln. Behalte die URL, den Titel, den Einreichungstyp, das Datum, den Zitattext, die Unternehmen-Identität und den Abruf-Zeitstempel. Wenn der Agent ein Memo schreibt, sollte jede wesentliche Behauptung auf die Einreichung zurückweisen und, wenn verfügbar, auf den Abschnitt oder Auszug. Wenn der Agent strukturierte Notizen schreibt, sollte die Einreichungsquelle ein Feld sein, kein Satz, der in der Mitte vergraben liegt.

[ALLOY]: Das verändert auch die Bewertung. Ein Finanzanalyse-Agent sollte nicht nur danach bewertet werden, ob die Zusammenfassung plausibel klingt. Er sollte danach bewertet werden, ob Behauptungen auf Primärquellen zurückführbar sind, ob Kommentare von Einreichungen getrennt werden, ob Daten erhalten bleiben und ob widersprüchliche Belege gekennzeichnet statt übertüncht werden.

[NOVA]: SEC-Einreichungen sind strukturierte rechtliche und finanzielle Dokumente. Ein 10-K-Risikofaktor ist nicht dasselbe wie ein vierteljährliches Betriebsupdate. Eine 8-K kann ein einzelnes Ereignis ankündigen. Eine Proxy-Erklärung kann Governance und Vergütung erläutern. Wenn ein Agent all das auf „die Firma sagte" reduziert, verliert er den Kontext, der die Behauptung nützlich macht.

[ALLOY]: Für Builder-Workflows ist das Designmuster straightforward. Die Retrieval-Schicht liefert Belege zurück. Die Reasoning-Schicht kann zusammenfassen und vergleichen. Die Berichtsschicht muss Zitate preserve. Die Speicherschicht sollte genug Metadaten behalten, sodass ein späteres Audit rekonstruieren kann, woher eine Behauptung stammt.

[NOVA]: Das ist besonders wichtig für nachgelagerte Tabellenkalkulationen, Investitionsnotizen, Compliance-Prüfungen und kundenorientierte Recherchen. Eine schöne Zusammenfassung mit schwachen Zitaten ist eine Haftung. Eine strukturiertere Zusammenfassung mit klaren Quellenfeldern ist einfacher zu vertrauen, einfacher zu prüfen und einfacher zu korrigieren.

[ALLOY]: Der konkrete Build-Workflow besteht darin, Evidence-Objekte am Leben zu halten. Wenn Claude Websuche ein Einreichungsergebnis zurückgibt, speichere den Einreichungstyp, das Unternehmen, das Datum, die URL, den zitierten Text und die Abrufzeit neben der Behauptung. Wenn der Agent einen Vergleich verfasst, trage diese Felder in die Vergleichstabelle oder das Memo. Wenn der Agent einen Bericht exportiert, füge genug Zitierdetails bei, sodass ein Prüfer die Quelle öffnen und die Behauptung überprüfen kann, ohne die gesamte Suche erneut auszuführen.

[NOVA]: Für Finanz-Agents deutet dies auch auf einen besseren Fehler-Workflow hin. Wenn eine Behauptung keine primäre Einreichungsquelle hat, kennzeichne sie als sekundären Kommentar. Wenn zwei Einreichungen widersprüchlich erscheinen, behalte beide Zitate und bitte um Prüfung, anstatt den Unterschied zu glätten. Wenn ein Einreichungstyp unklar ist, lass das Modell nicht raten. Der Agent sollte Unsicherheit als Zustand preserve, weil Unsicherheit oft das Wichtigste ist, was der Nutzer sehen muss.

[ALLOY]: Dasselbe Muster gilt auch außerhalb der Finanzwelt, aber die Finanzwelt macht die Einsätze offensichtlich. Primärquellen-Verankerung ist kein nice-to-have, wenn eine Behauptung eine Entscheidung beeinflussen kann. Reichhaltigere SEC-Einreichungsdaten geben Entwicklern ein besseres Tool-Ergebnis; die Anwendung muss die Verankerungsgrenze trotzdem bis zum Nutzer preserve.

[NOVA]: Das Anthropic-Update ist also oberflächlich klein und in der Implikation groß. Bessere Suchmetadaten machen Finanz-Agents besser prüfbar, aber nur wenn Builder Zitate durch die gesamte Pipeline am Leben halten. ...

[ALLOY]: Die Upgrade-Priorität für OpenClaw ist es, die veränderten Host-Oberflächen zu testen, nicht nur die Version zu installieren. Validiere Plugin-Init, Build und Validierung. Löse Browser-Modal-Handling aus. Inspiziere Gateway-Restart-Bereitschaft. Übe HTTPS-Proxy-Trust, falls benötigt. Probiere Android Talk Mode mit Unterbrechung. Sende Medien durch Telegram-Topics und Discord-Voice. Teste Bildbehandlung und Codex App-Server-Turns mit Bildern, Sandbox-Netzwerk, Code-Mode und eingeschränkter Sender-Policy.

[NOVA]: Für Codex Update und inspiziere den Betriebszustand. Überprüfe die TUI-Statuszeile, Service-Tier-Befehle, Berechtigungen, Approval-Mode, Workspace-Roots, Unified Mentions, Marketplace- und Sharing-Befehle, Remote-Control-Flows, konfigurierte Remote-Umgebungen, Python SDK Turn-Routing, codex doctor, Windows-Sandbox-Fälle falls relevant und App-Server-State-Recovery.

[ALLOY]: Für Copilot nutze günstigere Cloud-Agent-Models für einfache Reparaturarbeiten, halte Remote-Sessions policy-geschützt und überprüfe One-Click-Actions-Fixes als Code-Änderungen, nicht als endgültige Antworten. Für Claude-Finanz-Agents preserve SEC-Einreichungsmetadaten und Zitate als strukturierte Belege, nicht nur als Text.

[NOVA]: Der rote Faden durch diese Updates ist operative Reife. Hosts machen Tool- und Channel-Verträge klarer. CLIs expose State und Berechtigungen. Remote-Agents bekommen bessere Control Planes. Such-Tools liefern reichhaltigere Belege zurück. Das ist die Arbeit, die Agents einfacher zu shippen, debuggen und vertrauen macht.

[ALLOY]: Quellenlinks und Episodennotizen sind verfügbar unter Toby On Fitness Tech dot com.

[NOVA]: Das war AgentStack Daily. Ich bin NOVA.

[ALLOY]: Und ich bin ALLOY. Wir sind bald zurück.