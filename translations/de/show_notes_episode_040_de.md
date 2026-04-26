OPENCLAW DAILY — EPISODE 040 — 25. April 2026

[00:00] INTRO / HOOK
OpenClaw v2026.4.23 ist die neueste stabile Version, und da v2026.4.22, v2026.4.21 und v2026.4.20 bereits in den aktuellen Episodennotizen behandelt wurden, ist v2026.4.23 der einzige gültige Versionsblock am Anfang von EP040.

Und diese ist den vorderen Platz wert.
Sie macht die Bilderzeugung über OpenAI Codex OAuth und OpenRouter wesentlich einfacher, bietet Agenten einen saubereren Weg zum Verzweigen von Child-Runs mit vererbtem Kontext, fügt zeitspezifische Timeouts für lang laufende Medien-Generierungsjobs hinzu und bereinigt weiterhin Codex-, Medienverständnis-, Webchat- und Sicherheitsaspekte, die wichtig sind, wenn OpenClaw echte Arbeit leistet, anstatt nur Demos zu präsentieren.

Nach diesem Deep Dive zur Version kommen wir zu Googles geplanter Anthropic-Investition, zur V4-Vorschau von DeepSeek und zur Warnung von Vercel, dass der Breach möglicherweise umfangreicher und älter sein könnte als zunächst bekannt gegeben.

[01:30] STORY 1 — OpenClaw v2026.4.23 Macht Bilderzeugung in der Praxis Einfacher
Die wichtigste Änderung in v2026.4.23 ist, dass OpenClaw die Bildarbeit weiterhin aus dem „Sonderfall"-Bereich in die normale Laufzeit verschiebt.

Auf der OpenAI-Seite kann `openai/gpt-image-2` jetzt Generierung und Referenzbild-Bearbeitung durch Codex OAuth durchführen. Das ist wichtig, weil es eine der lästigsten Workflow-Trennungen im Stack beseitigt. Wenn ein Operator bereits über Codex angemeldet ist, muss die Bildarbeit nicht mehr anhalten und nach einem separaten `OPENAI_API_KEY` fragen, nur um dieselbe Provider-Familie zu nutzen. Die Bildoberfläche wird kontinuierlicher mit dem Rest des authentifizierten OpenAI-Pfads.

OpenRouter erhält ein paralleles Upgrade.
Bilderzeugung und Referenzbild-Bearbeitung fließen jetzt durch `image_generate` mit `OPENROUTER_API_KEY`, was genau die Art von Standardisierung ist, die OpenClaw braucht. Eine Multi-Provider-Laufzeit wird besser, wenn neue Provider-Fähigkeiten über denselben Tool-Pfad landen, anstatt punktuelle Handhabung an den Rändern zu erzwingen.

Es gibt hier auch eine Tool-Qualitätsgeschichte, nicht nur eine Provider-Geschichte.
v2026.4.23 erlaubt es Agenten, provider-unterstützte Qualitäts- und Ausgabeformat-Hinweise anzufordern und OpenAI-spezifische Steuerungen wie Hintergrund, Moderation, Komprimierung und Benutzer-Hinweise durch `image_generate` zu übergeben. In der Praxis bedeutet das, dass Bild-Workflows mehr Intent zur Aufrufzeit ausdrücken können, anstatt sich auf eine dünne universelle Schnittstelle zu verlassen, die nützliche Provider-Funktionen verbirgt.

Das ist wichtig für Builder, weil Bilderzeugung aufhört, eine binäre Ja-oder-Nein-Fähigkeit zu sein.
Sie wird zu einer kontrollierbaren Workflow-Oberfläche. Man kann sich um Ausgabeformat, Komprimierung, Timeout-Verhalten, Referenzbild-Bearbeitungen und provider-spezifische Parameter kümmern, ohne aus dem gemeinsamen Tool-Modell auszusteigen.

Genauso wichtig ist, dass dies die Version ist, in der Bildarbeit weniger wie ein Anhängsel und mehr wie eine unterstützte Produktionsspur aussieht. OpenAI-authentifizierte Benutzer, OpenRouter-Benutzer und agentengesteuerte Tool-Aufrufe erhalten alle einen kohärenteren Pfad, was bedeutet, dass weniger unangenehme Auth-Fallback-Mechanismen, weniger provider-spezifische Workarounds und weniger Gründe, Medienerzeugung als separates Subsystem zu behandeln, erforderlich sind.

[09:30] STORY 1B — Subagent-Kontext, Lang laufende Medien-Jobs und der Codex-Pfad Werden Sauberer
Das zweite große Upgrade in v2026.4.23 liegt auf der Agent-Laufzeitseite.

Native `sessions_spawn`-Läufe erhalten jetzt optionalen verzweigten Kontext-Vererbung.
Das ist eine große Sache für jeden, der Subagenten tatsächlich als Teil eines Workflows verwendet.
Bisher war die sauber-isolierte Sitzung als Standard oft die richtige Sicherheitswahl, aber es gibt echte Jobs, bei denen das Kind das Requester-Transkript erben sollte, damit es nicht von Grund auf neu gebrieft werden muss. Die Version behält Isolation als Standard bei, fügt aber ein bewussteres Mittelgrund hinzu: Kontext vererben, wenn es hilft, sauber bleiben, wenn es nicht hilft.

Das macht Delegation praktischer.
Es bedeutet, dass Operatoren Transkript-Kontinuität für begrenzte Kindarbeit bewahren können, ohne jeden Subagenten in eine unkontrollierte Klon des Elternteils zu verwandeln. Für OpenClaw ist das genau die richtige Form der Verbesserung: mehr Fähigkeit, aber mit der Kontrolloberfläche weiterhin explizit.

Die neue optionale per-Call `timeoutMs`-Unterstützung für Bild-, Video-, Musik- und TTS-Generierungstools ist eine weitere leise wichtige Änderung.
Lang laufende Generierungsjobs sind einer der häufigsten Orte, an denen eine Laufzeit sich wackelig anfühlen kann, selbst wenn der Provider nur langsam ist. Dieses Update erlaubt es Agenten, Anfrage-Timeouts nur für den Aufruf zu verlängern, der es braucht. Das ist besser, als alles global zu erhöhen und zu hoffen, dass nichts anderes seltsam wird.

Es gibt auch eine bedeutende Codex- und Modell-Katalog-Bereinigungsschicht.
Gebündelte Pi-Pakete wechseln zu 0.70.0, upstream `gpt-5.5`-Katalogmetadaten werden für OpenAI und OpenAI Codex übernommen, und die Version fügt strukturiertes Debug-Logging um die eingebettete Harness-Auswahl hinzu, damit `/status` lesbar bleibt, während die Gateway-Logs weiter erklären, warum ein Harness ausgewählt wurde oder warum Pi-Fallback passiert ist. Das ist die richtige Operator-Trennung: einfache Oberfläche, tiefere Logs, wenn man die Realität debuggen muss.

[17:30] STORY 1C — Die Fix-Liste Geht Wirklich Um Über Die Reduzierung Von Überraschungen In Echten Bereitstellungen
Viel vom Wert in v2026.4.23 liegt in der Fix-Liste, denn dort, wo die Laufzeit aufhört, Operator-Erwartungen zu verraten.

Codex `request_user_input`-Prompts werden zurück zur ursprünglichen Chat geleitet und eingereihte Follow-up-Antworten werden bewahrt. Das bedeutet, dass das System besser bei mehrstufigem menschlichem Übergabeprozess wird, anstatt den Kontext genau in dem Moment zu verlieren, in dem eine menschliche Entscheidung erforderlich ist.

Block-Streaming duplizierte letzte Antworten werden unterdrückt, wenn partielle Chunks die Antwort bereits vollständig abgedeckt haben. Slack-Gruppenflächen hören auf, interne „Working..."-Traces zu leaken. WebChat erhält nicht-wiederholbare Abrechnungs-, Auth- und Rate-Limit-Fehler, die an die Oberfläche gebracht werden, anstatt blank zu scheitern. Text-only Primärmodelle bewahren jetzt angehängte Bilder als Medien-Refs auf, damit nachgelagerte Bild-Tools sie weiter inspizieren können. Explizite Bildmodell-Konfiguration wird vor nativen Vision-Skips respektiert, und Codex-Bildmodelle erhalten begrenzte App-Server-Bild-Durchläufe mit korrekterem Routing.

Das sind keine glamourösen Bulletpoints, aber sie verändern direkt, ob das System vertrauenswürdig wirkt.
Das gleiche gilt für die Auth- und Routing-Fixes rund um die OpenAI-Bilderzeugung. Codex OAuth-Routing wird gehärtet, fehlende `openai-codex/gpt-5.5`-Katalogzeilen werden synthetisiert, wenn Discovery sie auslässt, komplexe Referenzbild-Bearbeitungen werden über geschützte Multipart-Uploads wiederhergestellt, und veraltete Codex-Modellzeilen werden unterdrückt.
Das ist die Art von Release-Arbeit, die eine Funktion von „technisch vorhanden" zu „sicher sich darauf zu verlassen" verwandelt.

Es gibt auch eine ernsthafte Sicherheits- und Grenzgeschichte.
Das Release härtet Gateway-Konfigbearbeitung, Webhook-Secret-Refresh-Verhalten, Android- und Pairing-Clearttext-Regeln, Teams-Token-Validierung, Plugin-Setup-Auflösung, Genehmigungsverhalten, Discord-Zugriffsdurchsetzung, MCP-Bridge-Exposition und mehrere prompt-injection-adjazente Metadatenpfade über Chat-Transporte hinweg.

Die praktische Einschätzung zu v2026.4.23 ist nicht nur „mehr Funktionen". Es geht darum, dass OpenClaw drei Bereiche gleichzeitig greifbarer macht: Medienerstellung, Agentendelegation und Vertrauen der Betreiber. Bildarbeit lässt sich einfacher weiterleiten. Subagenten erhalten ein besseres Kontextkontrollmodell. Und die Laufzeitumgebung investiert viel Energie darein, kleine Transport- und Auth-Randfälle daran zu hindern, zu seltsamen, benutzerbezogenen Fehlern zu werden.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.23

[26:00] GESCHICHTE 2 — Googles Anthropic-Engagement ist eine Compute-Hebel-Wette, nicht nur eine Finanzierungsrunde

Googles geplante Investition von bis zu 40 Milliarden Dollar in Anthropic lässt sich leicht als Bewertungsschlagzeile lesen. Das ist der uninteressanteste Aspekt.

Der wichtigere Aspekt ist, dass das Geschäft mit mehr Google-Cloud-Compute-Kapazität einhergeht, insbesondere TPU-Zugang. Anthropic befindet sich bereits in einer Position, in der Modellqualität, Nutzungslimits und Infrastrukturverfügbarkeit sichtbar miteinander verknüpft sind. Wenn Google also sowohl die Kapitalbeziehung als auch die Compute-Beziehung vertieft, kauft es nicht nur Upside in einem rivalisierenden Labor. Es stärkt seine Position in der Infrastrukturebene, die Frontier-Labore zunehmend nicht mehr missen können.

Das macht diese Geschichte für Builder und Betreiber nützlich. Der KI-Markt wird vertikal stärker verflochten. Dasselbe Unternehmen kann Wettbewerber bei Modellen sein, Lieferant von Compute, Distributionsplattform und strategischer Investor. Das bedeutet, dass der Modellwettbewerb kein sauberer Kampf zwischen isolierten Laboren mehr ist. Es ist ein Systemkampf um Trainingskapazität, Inferenzkapazität, Cloud-Margen und darum, wer bei Nachfragespitzen Vorzugszugang erhält.

Für Anthropic ist die unmittelbare Einschätzung offensichtlich. Mehr Cash und mehr Compute kaufen Raum, um Mythos, Claude und verwandte Produkte weiter zu skalieren, ohne dass Infrastruktur-Engpässe die ganze Geschichte werden. Für Google ist die Logik subtiler. Jeder verkaufte Dollar und jede TPU-Stunde an Anthropic ist nicht nur Finanzierung. Es ist ein Weg, Google Cloud zentraler für eines der wenigen Labore zu machen, die die Frontier-Diskussion noch bewegen können.

Die breitere Implikation ist, dass unabhängig wirkende Modellverkäufer zunehmend abhängig von den Cloud- und Silicon-Beziehungen werden könnten, die sie frühzeitig abschließen können. Das ist wichtig, weil Zuverlässigkeit, Limits und Rollout-Geschwindigkeit oft ebenso sehr eine Compute-Geschichte wie eine Modellierungsgeschichte sind.
→ https://techcrunch.com/2026/04/24/google-to-invest-up-to-40b-in-anthropic-in-cash-and-compute/

[32:30] GESCHICHTE 3 — DeepSeek V4 öffnet die Open-Weight-Preisdruckfrage erneut

DeepSeeks V4-Vorschau verdient Aufmerksamkeit, nicht weil jede Benchmark-Behauptung sofort vertrauenswürdig sein sollte, sondern weil die Form der Ankündigung strategisch wichtig ist.

Das Unternehmen gibt an, dass die neuen Flash- und Pro-Modelle auf ein Kontextfenster von einer Million Token drängen, sehr große Mixture-of-Experts-Architekturen verwenden und zu einem Preis angeboten werden, der Frontier-Closed-Modelle unterbietet. Wenn sich das im echten Einsatz bestätigt, dann liefert DeepSeek nicht nur eine weitere Open-Weight-Neugier ab. Es übt Druck auf die wirtschaftlichen Annahmen hinter Premium-Closed-Routing aus.

Für Builder ist die Schlüsselfrage nicht, ob DeepSeek bereits gewonnen hat. Die nützliche Frage ist, welche Art von Workload neu verlockend wird, wenn das Kontextfenster riesig und der Preis niedrig genug ist, um breite Nutzung weniger leichtsinnig erscheinen zu lassen. Große Codebase-Analysen, Long-Document-Retrieval, Batch-Reasoning und Routing mit niedrigerer Tragweite werden alle leichter zu rechtfertigen, wenn die Kostenuntergrenze sinkt.

Das erzeugt strategischen Druck im gesamten Markt. Closed-Frontier-Anbieter gewinnen weiterhin bei multimodaler Breite, Safety-Layern und in vielen Fällen bei absoluter Qualität. Aber wenn eine Open-Weight-Familie bei Text-Reasoning und Code-Aufgaben nah genug herankommt, gewinnen Betreiber mehr Hebel. Sie können Premium-Closed-Aufrufe für hochwertige Turns reservieren und breiteren Traffic zu günstigeren Alternativen auslagern, ohne ernsthafte Fähigkeiten aufzugeben.

Also, trotz der üblichen Vorsicht gegenüber Preview-Behauptungen, DeepSeek V4 ist jetzt als Preis- und Routing-Geschichte relevant. Es erinnert alle daran, dass die Open-Weight-Seite des Marktes weiterhin eine Obergrenze dafür setzt, wie selbstgefällig Premium-Modellanbieter sich leisten können zu sein.
→ https://techcrunch.com/2026/04/24/deepseek-previews-new-ai-model-that-closes-the-gap-with-frontier-models/

[38:00] GESCHICHTE 4 — Vercels Breach-Update zeigt, warum das echte Incident oft größer ist als die erste Geschichte

Vercels neuestes Update ist die Betreiber-Warnung, die man diese Woche ernst nehmen sollte.

Das Unternehmen gibt nun an, Beweise gefunden zu haben, dass einige Kundenkonten vor dem ursprünglich bekannt gegebenen Breach-Zeitfenster kompromittiert wurden, und dass weitere Kundenkonten, die mit dem April-Vorfall in Verbindung stehen, identifiziert wurden. Das bedeutet, die Geschichte ist nicht mehr nur „ein Mitarbeiter lud die falsche App herunter und ein Angreifer pivotierte von dort". Es könnte ein längerfristiges Kompromittierungsbild mit einem größeren Wirkungsradius sein, als die erste Offenlegung vermuten ließ.

Die Sicherheitslektion hier ist brutal, aber vertraut. Sobald Angreifer Zugriff auf Entwicklermaschinen, Tokens, Umgebungsvariablen oder andere Kontosekrets erhalten, brauchen sie nicht die saubere Erzählung, die sich Verteidiger für den Vorfall wünschen. Sie brauchen nur einen Weg, der funktioniert. Und sobald sie diesen Weg haben, können Platform-APIs, interne Systeme und kundenverknüpfte Infrastruktur sehr schnell in den Scope geraten.

Das ist auch wichtig, weil Vercel an einem sehr exponierten Teil des Stacks sitzt. Ein Kompromiss in einer Entwicklerplattform bleibt selten auf eine einzelne App beschränkt. Er kann auf Deployment-Secrets, Projekt-Metadaten, Integrationen und nachgelagerte Kundensysteme übergreifen. Deshalb sind Geschichten wie diese über den betroffenen Anbieter hinaus relevant. Sie sind wirklich Geschichten darüber, wie viel operative Macht sich um Entwickler-Anmeldedaten ansammelt.

Also ist die praktische Erkenntnis einfach. Wenn Sie modernes gehostetes Entwickler-Tooling betreiben, sind Infostealer und Secret-Diebstahl keine Nebenkategorierisiken. Sie sind zentrale Risiken. Und wenn der erste Incident-Bericht eng klingt, behandeln Sie das als den Anfang der Untersuchung, nicht als die endgültige Form des Problems.
→ https://techcrunch.com/2026/04/23/vercel-says-some-of-its-customers-data-was-stolen-prior-to-its-recent-hack/

[44:00] OUTRO / ABSCHLUSS

Das reicht für heute. OpenClaw v2026.4.23 hat Bildgenerierung, Subagent-Kontextkontrolle und Betreiber-Korrektheit in einer Weise vorangebracht, die in der Produktion tatsächlich spürbar sein wird. Googles Anthropic-Deal zeigte, wie Compute-Zugang zur strategischen Macht wird. DeepSeek V4 hielt den Preisdruck auf der Open-Weight-Seite des Marktes aufrecht. Und Vercel erinnerte alle daran, dass der unangenehme Teil der Plattformsicherheit usually usually usually usually breiter ist als die erste Offenlegung.

→ Reply here to approve transcript generation.