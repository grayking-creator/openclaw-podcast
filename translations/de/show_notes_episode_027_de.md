# EP027 — Dream Stack, KI-Rezepte, Shell-Agenten und die Kosten der Dokumentare
**OpenClaw Daily** | 9. April 2026 | ~33 Min.

## Episodentitel
**Dream Stack, KI-Rezepte, Shell-Agenten und die Kosten der Dokumentare**

## Tagline
OpenClaw 2026.4.9 bringt eine geerdete REM-Backfill-Lane und strukturierte Diary-Timeline, Utah erlaubt KI-psychiatrische Verschreibungen, OpenAI gibt Agenten eine echte Shell, STAT News berichtet, dass KI-Dokumentare leise die Gesundheitskosten erhöhen, und Yahoo setzt seine Suchzukunft auf Claude.

## Story-Übersicht

1. **OpenClaw 2026.4.9 — Der Memory-Stack bekommt eine Dream Replay Lane**
   Das heutige Release konzentriert sich auf das Memory- und Dreaming-System. Die Hauptneuerung ist eine geerdete REM-Backfill-Lane mit einem `rem-harness --path` CLI — du kannst jetzt historische tägliche Notizen zurück durch die Dreaming-Pipeline spielen lassen, damit alter Kontext in Dreams und dauerhaften Speicher zurückgespielt wird, ohne einen separaten Memory-Stack zu pflegen. Die Control UI erhält eine strukturierte Diary-Ansicht mit Timeline-Navigation, Backfill- und Reset-Steuerungen, nachvollziehbaren Dreaming-Zusammenfassungen und einer Scene-Lane mit Beförderungshinweisen. Ebenfalls in diesem Release: Character-Vibes QA-Bewertungsberichte mit parallelen Modellvergleichsläufen, Provider-Auth-Aliase, damit Provider-Varianten Umgebungsvariablen und Auth-Profile teilen können, ohne kernlevel Verdrahtung, und iOS CalVer-Pinning für Release-Züge. Sicherheitsfixes: Browser-Interaktionen können die SSRF-Quarantäne nicht mehr über interaktionsgesteuerte Main-Frame-Navigationen umgehen, und Runtime-Control-Umgebungsvariablen-Überschreibungen aus nicht vertrauenswürdigen Workspace-.env-Dateien sind jetzt blockiert.

2. **Utah erlaubt KI, psychiatrische Medikamente zu verschreiben**
   Legion Health wurde das erste psychische Gesundheitsunternehmen, das von Utahs KI-regulatorischer Sandbox autorisiert wurde, KI zu ermöglichen, psychiatrische Medikamente zu verschreiben. Dies erweitert den Januar-2026-Piloten über routinemäßige Medikamentennachfüllungen hinaus zu vollständigen psychiatrischen Behandlungsentscheidungen. Die KI verschreibt unter ärztlicher Aufsicht im Rahmen der Sandbox — aber die Richtung ist klar: Autonome KI-gestützte medizinische Entscheidungen bewegen sich upstream von Nachfüllungen zu Diagnosen. Es lohnt sich zu diskutieren, wo die Haftung liegt, wenn die KI falsch liegt, und ob die „Sandbox"-Rahmung hier viel politische Arbeit leistet.

3. **OpenAI Responses API — Agenten bekommen eine echte Shell**
   OpenAI hat die Responses API um ein vollständiges Shell-Tool erweitert, das Python, Node.js, Go, Java, Ruby und PHP in gehosteten Container-Workspaces unterstützt. Agenten können jetzt Code schreiben, ihn ausführen, Ausgabe inspizieren und iterieren — alles innerhalb einer verwalteten serverseitigen Umgebung mit Kontextkomprimierung für lang laufende Aufgaben. Außerdem wurden wiederverwendbare „Agent-Skills" eingeführt, die verpackt und über Läufe hinweg referenziert werden können. Dies ist das klarste Signal von OpenAI, dass die Responses API die ernsthafte agentische Oberfläche ist, nicht die Assistants API.

4. **KI-Dokumentare erhöhen die Gesundheitskosten — Und jeder weiß es**
   STAT News berichtet, dass Krankenversicherer und Krankenhäuser privat übereinstimmen, dass KI-gestützte klinische Dokumentare die Kosten durch das erhöhen, was sie „Coding-Intensität" nennen — die KI erkennt mehr abrechenbare Details und codiert Besuche gründlicher, was höhere Erstattungsansprüche bedeutet. Eine Studie fand, dass KI-Dokumentare nur 16 Minuten pro 8-Stunden-Schicht einsparten, trotz steigender Besuchskosten. Der unangenehme Teil: Niemand ist incentiviert, es zu stoppen. Krankenhäuser erhalten mehr Einnahmen, Dokumentar-Anbieter bekommen Verlängerungen, und Versicherer bleiben mit der Rechnung sitzen, die sie nicht sauber der KI zuordnen können.

5. **Yahoo Scout — Claude treibt einen Comeback-Versuch an**
   Yahoo startete Scout, eine KI-Antwortmaschine, gebaut auf Anthropics Claude mit Microsoft Bing-Grundierung, die an Yahoos 250 Millionen US-Nutzer auf Desktop und Mobile ausgerollt wird. Es ist ein direkter Angriff auf Google und ChatGPT-Style-Suche. Für Anthropic ist dies ein weiterer großer Distributionsdeal obendrauf zu Amazon, Google und dem Enterprise-Stack. Für Yahoo ist es eine Wette, dass Clarles Reasoning obendrauf auf Bings Index einen Platz in den KI-Suchkriegen sichern kann. Ob Yahoo genug Markenwert übrig hat, um das relevant zu machen, ist eine andere Frage.

6. **Google startet leise eine Offline-First KI-Diktier-App**
   Google veröffentlichte AI Edge Eloquent — eine kostenlose iOS-App, die ein Gemma-basiertes Modell vollständig auf dem Gerät ausführt, ohne Internetverbindung erforderlich. Es entfernt automatisch Füllwörter und bietet Texttransformationswerkzeuge: Kernpunkte, formell, kurz und lang Modi. Kein Abonnement, unbegrenzte Nutzung, Android kommt. Der interessante Winkel ist nicht die App selbst — es ist, dass Google ein vollständig offline Gemma-Produkt auf iOS vor Android veröffentlicht hat, und es leise tat. Anzeichen eines schneller bewegten Edge-KI-Pushs.

## Shownotes
```md
OPENCLAW DAILY — FOLGE 027 — 9. April 2026

[00:00] INTRO / HOOK
OpenClaw 2026.4.9 bringt eine geerdete REM-Backfill-Lane und Diary-Timeline.
Utah erlaubt KI, Psychopharmaka zu verschreiben. OpenAI gibt Agenten eine echte Shell.
KI-Dokumentare erhöhen die Gesundheitskosten und niemand will es stoppen.
Yahoo setzt seine Suchzukunft auf Claude.

[02:00] STORY 1 — OpenClaw 2026.4.9: Dream Replay Lane und Diary Timeline
Das heutige Release dreht sich alles um Memory-Tiefe.

Die Hauptneuerung ist die geerdete REM-Backfill-Lane — ein `rem-harness
--path` CLI, das es ermöglicht, historische tägliche Notizen zurück durch die
Dreaming-Pipeline zu spielen. Wenn du ARIA (AI Reasoning and Inference Agent) seit Monaten laufen hast,
war dein früher Kontext inaktiv. Mit Backfill können diese alten
Diary-Einträge in Dreams verarbeitet und in den dauerhaften Speicher befördert werden. Der alte
Stack und der neue Stack werden eine kontinuierliche Aufzeichnung.

Die Control UI erhält eine strukturierte Diary-Ansicht mit vollständiger Timeline-
Navigation: Du kannst durch Diary-Einträge scrollen, Backfills
ausführen, den geerdeten Zustand zurücksetzen, nachvollziehbare Dreaming-Zusammenfassungen
inspecten und sehen, welche Szenen für die Beförderung bereitstehen. Die Scene-Lane zeigt
jetzt Beförderungshinweise, damit du sehen kannst, was demnächst vom Kurzzeit-
in den dauerhaften Speicher verschoben wird, bevor es passiert.

QA erhält Character-Vibes-Bewertungsberichte — eine Möglichkeit, parallele Modellvergleichsläufe
während der Live-QA durchzuführen, damit du Verhaltensunterschiede
zwischen Kandidatenmodellen nebeneinander statt sequenziell sehen kannst.

Provider-Auth-Aliase ermöglichen es Provider-Varianten, Umgebungsvariablen, Auth-
Profile und API-Key-Onboarding-Flows zu teilen, ohne kernlevel
Verdrahtung zu benötigen. Wenn du mehrere Varianten desselben Providers betreibst,
wird die Auth-Konfiguration jetzt auf Manifest-Ebene geteilt.

iOS erhält CalVer-Pinning — explizites Versionstracking in
`apps/ios/version.json` mit dokumentiertem `pnpm ios:version:pin`
Workflow für Release-Züge. TestFlight-Iteration bleibt auf derselben
Kurzversion, bis Maintainer absichtlich auf die nächste
Gateway-Version befördern.

Sicherheit: Browser-Interaktionen können die SSRF-Quarantäne nicht mehr
über interaktionsgesteuerte Main-Frame-Navigationen umgehen — die Sicherheitsprüfung läuft jetzt
nach Klick, Evaluate, Hook-ausgelöstem Klick und gebatchten Aktionsflows,
die auf einem neuen Frame landen, erneut. Und Runtime-Control-Umgebungsvariablen-
Überschreibungen sind aus nicht vertrauenswürdigen Workspace-.env-Dateien blockiert,
womit ein Eskalationspfad durch Workspace-Level-Config geschlossen wird.
→ github.com/openclaw/openclaw/releases/tag/v2026.4.9

[09:00] STORY 2 — Utah erlaubt KI, psychiatrische Medikamente zu verschreiben
Utah's regulatorische Sandbox hat sich gerade von routinemäßigen Medikamentennachfüllungen auf
psychiatrische Verschreibungen erweitert. Legion Health ist das erste psychische
Gesundheitsunternehmen, das autorisiert wurde, KI zu ermöglichen,
psychiatrische Medikamentenbestellungen auszustellen — noch unter ärztlicher
Aufsicht, aber die KI trifft die Erstentscheidung.

Der Januar-2026-Pilot war für Niedrigrisiko-Nachfüllungen. Psych-Verschreibungen
sind kategorisch anders: Dosierungsfehler, Medikamentenwechselwirkungen und
Kontraindikationen in der psychiatrischen Versorgung bergen ernsthafte klinische Risiken.
Dass dies als „Sandbox" gerahmt wird, leistet erhebliche regulatorische Arbeit.

Die Haftungsfrage ist genuin ungeklärt: Wenn eine KI
falsch verschreibt und ein Patient geschädigt wird, wer ist verantwortlich? Der Arzt,
der die Aufsicht führte? Das Unternehmen, das die Sandbox betreibt? Der Staat, der
sie autorisierte? Utah hat darauf noch keine klaren Antworten, und sie fügen
mehr Komplexität hinzu, bevor das Framework getestet ist.
→ distilinfo.com/2026/04/01/ai-now-prescribes-mental-health-drugs-in-utah/

[15:00] STORY 3 — OpenAI Responses API: Agenten bekommen eine echte Shell
OpenAIs Responses API bietet jetzt ein gehostetes Shell-Tool — Python,
Node.js, Go, Java, Ruby, PHP — das in verwalteten Container-
Workspaces läuft, die der Agent hochfährt und in denen er ausführt. Der Agent schreibt
Code, führt ihn aus, liest die Ausgabe und iteriert innerhalb einer einzelnen API-Aufruf-
Sequenz. Serverseitige Kontextkomprimierung verhindert, dass lang laufende Aufgaben
Token-Limits erreichen.

Die andere Neuerung sind wiederverwendbare Agent-Skills — verpackte Capability-
Definitionen, die über Läufe hinweg referenziert werden können, ohne sie jedes Mal
neu spezifizieren zu müssen.

Dies ist OpenAI, die eine harte Linie zieht: Die Responses API ist die agentische
Oberfläche für die Zukunft. Die Assistants API erhält dies nicht. Wenn du
autonome Agenten auf OpenAI-Infrastruktur baust, ist der Migrationspfad
klar.
→ openai.com/index/new-tools-for-building-agents/

[21:00] STORY 4 — KI-Dokumentare erhöhen die Gesundheitskosten, und niemand will es stoppen
STAT News berichtet, dass Versicherer und Krankenhäuser beide privat anerkennen,
dass KI-gestützte klinische Dokumentare die Kosten erhöhen — aber es gibt keinen Konsens
darüber, was dagegen zu tun ist.

Der Mechanismus ist „Coding-Intensität": KI-Dokumentare sind gründlicher als
menschliche Notizengeber, erfassen mehr abrechenbare Details und codieren Besuche
vollständiger. Gründlichere Codierung bedeutet höhere Erstattungsansprüche. Eine
Studie fand, dass Dokumentare 16 Minuten pro 8-Stunden-Schicht einsparten, während
sie die Besuchskosten erhöhten. Das ist ein sehr schlechtes Geschäft, wenn das Ziel
Kosteneffizienz ist.

Die unangenehme Dynamik: Krankenhäuser erhalten mehr Einnahmen aus denselben
Patientenbegegnungen, Dokumentar-Anbieter bekommen Verlängerungen, und
Versicherer absorbieren Kosten, die sie nicht sauber der KI zuordnen können.
Niemand in der Kette hat einen direkten finanziellen Anreiz,
zurückzudrängen.

Dies ist eine Vorschau auf ein Muster, das wir anderswo sehen werden: KI optimiert für die
Metriken, auf die sie belohnt wird, und im US-Gesundheitswesen ist die Metrik
Abrechnungscodes.
→ statnews.com/2026/04/08/insurers-providers-agree-ai-scribes-raise-health-care-costs/

[26:00] STORY 5 — Yahoo Scout läuft auf Claude, geht zu 250M Nutzern
Yahoo startete Scout, eine KI-Antwortmaschine, gebaut auf Anthropics Claude
mit Microsoft Bing-Grundierung, die an Yahoos 250 Millionen US-Nutzer
auf Desktop und Mobile ausgerollt wird.

Für Anthropic ist dies ein weiterer großer Vertriebskanal — Claude ist
jetzt die KI-Schicht in Amazon, Google Workspace und Yahoo-Suche.
Breite kommerzielle Veröffentlichung beschleunigt sich. Für Yahoo ist dies
die glaubwürdigste Produktwette seit Jahren. Ob Yahoo genug
Nutzervertrauen und tägliche Gewohnheit hat, um Suchen in Scout-Sitzungen umzuwandeln, ist
eine echte Frage. Aber der zugrunde liegende Stack ist solide.
→ yahooinc.com/press/introducing-yahoo-scout-a-new-ai-answer-engine

[30:00] STORY 6 — Google startet Offline-Gemma-Diktat auf iOS vor Android
Google veröffentlichte AI Edge Eloquent auf iOS — eine kostenlose offline-first
Diktier-App, die ein Gemma-Modell vollständig auf dem Gerät ausführt. Kein Internet,
kein Abonnement, keine Daten verlassen das Telefon. Füllwort-Entfernung,
Kernpunkte / Formell / Kurz / Lang Texttransformationsmodi eingebaut.

Zwei Dinge fallen auf. Erstens: Dies ist ein ernsthaftes On-Device-Gemma-
Deployment, keine Demo. Zweitens: Es wurde auf iOS vor Android veröffentlicht, was
dir etwas darüber sagt, wo Googles Edge-KI-Testumgebung gerade ist.
Android-Version kommt, aber die ersten echten Nutzer sind auf
Apple-Hardware. Leise Veröffentlichung, bedeutungsvolles Signal.
→ techcrunch.com/2026/04/07/google-quietly-releases-an-offline-first-ai-dictation-app-on-ios/

[33:00] OUTRO / SCHLUSS
Das war's für das heutige OpenClaw Daily. Für Shownotes und Transkripte besuche tobyonfitnesstech.com.
```

## Links
- OpenClaw v2026.4.9 Release Notes: https://github.com/openclaw/openclaw/releases/tag/v2026.4.9
- Utah KI-psychiatrische Verschreibungen: https://distilinfo.com/2026/04/01/ai-now-prescribes-mental-health-drugs-in-utah/
- OpenAI Responses API Shell-Tool: https://openai.com/index/new-tools-for-building-agents/
- KI-Dokumentare erhöhen Gesundheitskosten (STAT News): https://www.statnews.com/2026/04/08/insurers-providers-agree-ai-scribes-raise-health-care-costs/
- Yahoo Scout Ankündigung: https://www.yahooinc.com/press/introducing-yahoo-scout-a-new-ai-answer-engine
- Google AI Edge Eloquent (TechCrunch): https://techcrunch.com/2026/04/07/google-quietly-releases-an-offline-first-ai-dictation-app-on-ios/

## Kapitel
- **[00:00] Hook — Dream Stack, KI-Rezepte, Shell-Agenten und die Kosten der Dokumentare**
- **[02:00] OpenClaw 2026.4.9: Dream Replay Lane und Diary Timeline**
- **[09:00] Utah erlaubt KI, psychiatrische Medikamente zu verschreiben**
- **[15:00] OpenAI Responses API: Agenten bekommen eine echte Shell**
- **[21:00] KI-Dokumentare erhöhen die Gesundheitskosten, und niemand will es stoppen**
- **[26:00] Yahoo Scout läuft auf Claude, geht zu 250M Nutzern**
- **[30:00] Google startet Offline-Gemma-Diktat auf iOS vor Android**
- **[33:00] Outro**
