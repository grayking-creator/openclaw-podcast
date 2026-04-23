OPENCLAW DAILY — EPISODE 036 — 22. April 2026

[00:00] INTRO / HOOK
OpenClaw v2026.4.21 und v2026.4.20 sind die einzigen gültigen Release-Berichte für EP036,
und diese Episode beginnt bewusst damit.
Das neueste stabile Paar ändert den Standardpfad für die Bilderzeugung, Fallback-Logs,
Owner-Only-Befehlsdurchsetzung, Slack- und Browser-Schutzmaßnahmen, den Setup-Flow,
die Session- und Cron-Zustandsbehandlung, Modellpreise, die Kompaktierungssichtbarkeit
und mehrere Laufzeitkanten, die relevant werden, wenn das Produkt echte Arbeit leistet.

Danach gibt es nur zwei externe Themen, die heute wirklich Zeit wert sind:
OpenAIs Images 2.0, weil es praktische Bild-Workflows tatsächlich verändern könnte,
und YouTubes erweiterter Rollout der Ähnlichkeitserkennung, weil Plattform-Identitätsschutz
operativer wird.

[01:30] STORY 1 — OpenClaw v2026.4.21 und v2026.4.20 im Detail
Die Release-Auswahlregel ist hier ungewöhnlich sauber.
Die neuesten stabilen Tags sind v2026.4.21, v2026.4.20, v2026.4.15 und v2026.4.14.
Letzte Episodennotizen haben bereits v2026.4.15 und v2026.4.14 behandelt, daher ist
die einzige gültige OpenClaw-Berichterstattung für EP036 der neueste zusammenhängende
nicht abgedeckte Block: v2026.4.21 und v2026.4.20.

v2026.4.21 ist ein fokussiertes Release, aber es verändert Oberflächen, die Nutzer
tatsächlich spüren.
Der gebündelte Standard-Bilderzeugungsanbieter und die Live-Media-Smoke-Tests
bewegen sich hin zu `gpt-image-2`. Die Docs fügen neuere 2K- und 4K-Größenhinweise hinzu.
Fehlgeschlagene Anbieterkandidaten werden lauter in den Logs, bevor der Fallback
erfolgreich ist. Das ist wichtig, weil die Bilderzeugung einer der einfachsten Orte ist,
an denen sich "es hat letztendlich funktioniert" echten Debugging-Schmerz verstecken kann.

Dasselbe Release verschärft auch Schutzmaßnahmen, die unter Druck relevant sind.
Owner-erzwungene Befehle erfordern jetzt wirklich die Owner-Identität, anstatt durch
Fallback-Pfade zu schlüpfen. Slack-Thread-Aliase werden zuverlässiger beibehalten.
Ungültige Browser-Barrierefreiheitsreferenzen scheitern schnell, anstatt verwirrendes
Downstream-Verhalten zu erzeugen. Gepackte Installationen erhalten einen besseren
Plugin-Doctor-Wiederherstellungspfad. Nichts davon ist aufregend. Alles davon reduziert
Mehrdeutigkeit.

Die praktische Auswirkung ist, dass das Produkt einfacher zu inspizieren wird.
Die Standard-Bildspur ist aktueller, das Fallback-Verhalten ist weniger rätselhaft,
eingeschränkte Befehle entsprechen ihrem eigenen Sicherheitsmodell besser,
Thread-Kontext driftet weniger wahrscheinlich ab, Browser-Automatisierung scheitert
früher, anstatt so zu tun, als ob, und gepackte Installationen erhalten eine sauberere
Wiederherstellungsgeschichte. Das ist genau die Art von Release-Detail, die nach der
Demo mehr relevant ist als während der Demo. Es macht die Software einfacher zu erklären,
einfacher zu debuggen und schwerer falsch zu interpretieren, wenn während echter
Produktionsnutzung etwas Ungewöhnliches passiert.

[11:00] STORY 1B — OpenClaw v2026.4.20 Laufzeit-, Setup- und Zustandsänderungen
v2026.4.20 ist breiter und struktureller.
Der Setup-Assistent erhält einen klareren Sicherheitswarnungsflow, sauberere
API-Key-Eingabeaufforderungen und einen Ladespinner während der Modellkatalog-Abrufe.
Das ist wichtig, weil das Setup der Ort ist, an dem viele Nutzer entscheiden, ob ein
Produkt kompetent oder schlüpfrig wirkt.

Unter der Haube erhalten Session-Store-Einträge jetzt Begrenzungen nach Anzahl und Alter,
sodass Cron- oder Executor-Wechsel nicht still und leise ewig wuchern. Der Cron-Laufzeitzustand
wird in eine separate `jobs-state.json` aufgeteilt, was hilft, git-verfolgte Job-Definitionen
stabil zu halten, während sich der Live-Scheduler-Zustand unabhängig ändert. Es gibt auch
tiered-Modellpreisunterstützung, stärkere System-Prompts, Kompaktierungshinweise und
Korrekturen bei der Exec-Behandlung, dem Codex-Transport und dem Plugin-API-Verhalten.

Die praktische Leseart des Paares ist einfach:
v2026.4.21 verbessert die Ehrlichkeit der Bild- und Schutzmaßnahmenoberflächen,
während v2026.4.20 die Ehrlichkeit von Setup, Zustand und Laufzeitverhalten verbessert.
Das ist die Art von Release-Paar, das im täglichen Gebrauch relevanter ist als in einer
Einzeilen-Überschrift.

[23:30] STORY 2 — OpenAI Images 2.0 und praktische Bild-Workflows
OpenAIs Images 2.0 ist wichtig, weil textlastige Bildarbeit endlich aus dem
Neuigkeits-Bucket herauskommen könnte.
Lesbare Menüs, bessere UI-ähnliche Komposition, dichtere Layouts, stärkere Handhabung
für Poster, Diagramme und strukturierte visuelle Elemente: Das sind keine Nebensachen.
Das sind genau die Aufgaben, die previously Menschen zurück zu manuellen Tools oder
Open-Model-Workflows mit viel Flickwerk um die schwachen Stellen trieben.

Das ersetzt nicht automatisch FLUX-Style- oder andere offene Bild-Workflows.
Offene Systeme sind weiterhin wichtig für lokale Kontrolle, benutzerdefinierte
Modellwahlen, wiederholbare Stiltuning und Eigentum am Generierungspfad.
Aber wenn die Aufgabe schnelle Mock-Interfaces, Thumbnails, Poster, Slides, Diagramme,
Menüs, Anzeigenkonzepte oder andere Text-in-Bild-Arbeit ist, sieht Images 2.0 viel
relevanter aus als ältere Bildmodelle.

Das macht auch das OpenClaw-Release interessanter.
Wenn der gebündelte Pfad sich hin zu `gpt-image-2` bewegt, dann ist die Frage nicht mehr
"hat die App überhaupt Bilderzeugung?"
Die Frage wird "ist der Standardpfad jetzt gut genug, um zu ändern, welche Aufgaben
die Leute ihr anvertrauen?"

[31:00] STORY 3 — YouTube erweitert KI-Ähnlichkeitserkennung
YouTubes tieferer Rollout der Ähnlichkeitserkennung für Prominente und ihre Vertreter
ist ein kürzeres letztes Segment wert, weil es zeigt, wohin die Plattformpolitik geht.
Synthetische Identitätskontrollen werden zur normalen Produktinfrastruktur.
Das löst nicht jedes Deepfake-Video-Problem, aber es zeigt, dass Gesichtsrechte und
letztendlich Stimmrechtesysteme sich von Randfall-Werkzeugen hin zu einem Standardteil
von Medienplattformen bewegen.

[35:30] OUTRO / ABSCHLUSS
Also die Kurzversion von EP036 ist unkompliziert:
OpenClaw hat zwei Releases damit verbracht, das Produkt ehrlicher bedienbar zu machen,
OpenAIs Images 2.0 könnte für praktische textlastige Bildarbeit endlich relevant sein,
und YouTube behandelt synthetischen Ähnlichkeitsmissbrauch wie eine dauerhafte
Plattformaufgabe.

Das reicht für eine Episode.
Kein Füllmaterial nötig.

→ Antwort hier, um die Transkriptgenerierung zu genehmigen.