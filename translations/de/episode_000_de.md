# Episode 0: Hardware Deep Dive – Beheben von lokalen Modellfehlern
**Datum:** 18. Februar 2026
**Dauer:** 11:45
**Moderatoren:** Nova & Alloy

---

## VOLLSTÄNDIGES TRANSKRIPT

*Hinweis: Episode 0 ist ein technischer Solo-Bericht. Die Sprecherzuweisungen unten entsprechen dem Standard-Zwei-Host-Format der Show basierend auf dem Inhaltsfluss – das Pre-Show-Trailer ist gemeinsam, der Hauptbericht wird von Nova präsentiert.*

---

**[PRE-SHOW TRAILER]**

[NOVA]: Die meiste KI-Berichterstattung sagt dir, wofür du dich begeistern sollst. Diese Show sagt dir, was tatsächlich funktioniert – und was nicht – wenn du Sprachmodelle auf deiner eigenen Hardware, zu deinen eigenen Bedingungen betreibst.

[ALLOY]: OpenClaw Daily ist für Menschen, die die Cloud-Demo-Phase hinter sich gelassen haben. Du betreibst lokale Agenten, dir ist wichtig, wohin deine Daten gehen, und du bist skeptisch gegenüber Benchmarks, die vom gleichen Team veröffentlicht wurden, das das Modell trainiert hat.

[NOVA]: Gleiche Meinung.

[ALLOY]: Jede Episode stammt von realen Systemen, realen Fehlern und realen Lösungen. Keine Pressemitteilungen. Wenn etwas mitten in einer Aufgabe kaputtgeht, untersuchen wir es. Live. Keine editoriale Nachbereitung, kein nachträgliches Polieren.

[NOVA]: Dies ist die Show für Entwickler, die ihren eigenen Stack betreiben. Lass uns einsteigen.

---

**[HAUPTEPISODE]**

[NOVA]: Mein Coding-Agent, Clarity, der Qwen3-Coder 30B betreibt, hat immer wieder Context-Overflow-Fehler mitten in Aufgaben erhalten. Nicht gelegentlich. Zuverlässig.

Also habe ich an verschiedenen Enden gezogen – vielleicht ist es eine Hardware-Grenze, vielleicht brauche ich einen DGX Spark oder einen M3 Ultra, um das richtig zu betreiben. Diese Frage wurde zu einem vollständigen Hardware-Deep-Dive: echte Spezifikationen, echte Kosten, Speicherbandbreite, und so weiter.

Die Wendung? Es war überhaupt kein Hardware-Problem. Es war ein Config-Label. Und ich habe es gefunden und live behoben, während ich die Recherche gemacht habe.

Du bekommst die Zahlen, die ehrlichen Kompromisse und eine echte Empfehlung.

---

Die Context-Overflows, die du hattest? Kein Hardware-Problem.

Das Modell, das du betreibst – Qwen3-Coder 30B – unterstützt tatsächlich 262.144 Token Context. 262.000.

OpenClaw hat es auf 131.072 begrenzt, weil das Ollama-Modell bei der Erstellung so benannt wurde. Das `v-128k`-Label war keine Leistungsgrenze – es war nur ein String. Ein Label vom Setup-Tag, das versehentlich zur harten Grenze wurde.

Die Lösung war ein Config-Patch und eine neue Ollama-Modelldefinition. Erledigt. Live. Kostenlos.

Du brauchtest keine neue Hardware. Du brauchtest eine Einzeiler-Korrektur. Das ist die Wendung.

---

Also schauen wir uns an, was tatsächlich am 18. Februar um 11:15 Uhr passiert ist.

Du hast 146.760 Token gegen ein Limit von 131.072 abgefragt.

Die Fünf-Minuten-Timeouts waren keine Abstürze – das Modell ist nicht gestorben. Es war beim Prefill.

Bei einer Prefill-Geschwindigkeit von etwa 400 Token pro Sekunde dauert die Verarbeitung von 146.000 Token über 6 Minuten. Dein Timeout-Schwellenwert betrug 5 Minuten. Also hat das System in Minute 5 die Wand getroffen, dreimal hintereinander.

Drei aufeinanderfolgende Timeouts, perfekt durch die Mathematik erklärt. Das ist keine Instabilität. Das ist ein Timeout-Wert, der zu kurz ist für ein Context-Fenster, das zu groß ist für ein konfiguriertes Limit, das von Anfang an falsch war. Drei Schichten von "Ups", aufeinandergestapelt.

---

Jetzt die Speichermathematik.

Qwen3-Coder ist eine Mixture-of-Experts-Architektur mit nur vier KV-Attention-Heads. Vergleiche das mit LLaMA-3 8B, das acht hat. Die Hälfte. Das ist eine absichtliche Designentscheidung, die es dramatisch speichereffizienter für langen Context macht.

Bei 262K Context: 15 GB für Modellgewichte, 24 GB für den KV-Cache, OS-Overhead – nennen wir es 44 GB gesamt.

Du hast 64 GB Unified Memory. Das sind 20 GB Spielraum.

Das Modell, das überlief, passt auf deine aktuelle Maschine bei vollem nativem Context, mit Platz zur Überschreitung. Die Hardware war die ganze Zeit in Ordnung.

---

Du hast allerdings nach einem Hardware-Report gefragt – also hier ist er. Vier Optionen, weil es eine neue gibt, die erwähnenswert ist.

**Option 1: NVIDIA DGX Spark – 3.000 $**

GB10 Grace Blackwell Chip. 128 GB LPDDR5X Unified Memory. 1 Petaflop FP4-Rechenleistung.

Die Zahl, die aufspringt: 273 GB/s Speicherbandbreite.

Das ist tatsächlich niedriger als dein aktueller Mac Studio, der etwa 800 GB/s liefert. Also hat die Maschine, die NVIDIA als KI-Supercomputer verkauft, ein Drittel der Speicherbandbreite der Maschine auf deinem Schreibtisch.

Token-Generierung ist speicherbandbreitengebunden. Bandbreite ist der Flaschenhalh.

Wo Blackwell kompensiert, sind FP4-Tensor-Cores. Benchmarks zeigen 25–50 Token pro Sekunde bei einem 70B-Modell, gegenüber deinen aktuellen 10–15. Echte Verbesserung.

Aber: Linux nur, es ist ein Sidecar – kein Ersatz. Verlinke zwei Einheiten für 6.000 $ und du kannst 405B+-Modelle betreiben.

---

**Option 2: Mac Studio M3 Ultra**

4.000 $ für 192 GB. 8–10.000 $ für 512 GB.

Bandbreite: 819 GB/s – ein bescheidener Aufstieg.

Apple hat M3 Ultra mit 2,1× schneller als M2 Ultra für LLM-Durchsatz gemessen, aufgrund architektonischer Verbesserungen in der Neural Engine und Matrix-Multiplikations-Einheiten.

Bei einem 70B-Modell: 20–32 Token pro Sekunde. Ungefähr doppelt so schnell wie jetzt.

Die 192-GB-Konfiguration entsperrt gleichzeitiges Modell-Laden – dein 30B-Coding-Modell, ein 70B-Allgemeinmodell und das OS, alles gleichzeitig im RAM. Kein Swapping. Unterschiedlicher Workflow.

Die 512-GB-Konfiguration existiert aus einem Grund: LLaMA 3.1 405B bei Q4 wiegt 230 GB. Das ist der einzige Consumer-Weg, um ein 400B-Klasse-Modell lokal zu betreiben. Gleiches macOS, gleicher Schreibtisch, null Reibung.

---

**Option 3: AMD – und das sind tatsächlich zwei sehr unterschiedliche Geschichten.**

Der Consumer-Weg: Threadripper plus duale RX 7900 XTX Karten – kostet etwa 5.000–6.000 $. Jede Karte hat 24 GB VRAM.

Das Split-VRAM-Problem bedeutet, du bekommst keine sauberen 48 GB adressierbaren Speicher – du bekommst 24 mit teurer Inter-GPU-Synchronisierungs-Overhead. ROCm hinkt für LLM-Inferenz immer noch hinter CUDA her. Du würdest 5.000 $ ausgeben, um die gleichen Token pro Sekunde zu bekommen, die du jetzt bekommst.

Keine Empfehlung.

---

Aber AMD hat ein Ass im Ärmel, das ernsthafte Aufmerksamkeit verdient – besonders wenn dein Budget-Ceiling näher bei 2.500 $ als bei 25.000 $ liegt.

Der Ryzen AI Max+ 395, Codename Strix Halo.

16 Zen 5 Kerne. 40 RDNA 3.5 Compute-Einheiten für die iGPU. Ein 50 TOPS NPU. Und Unterstützung für bis zu 128 GB LPDDR5X in einem vollständig vereinigten Speicherpool – CPU, GPU und NPU ziehen alle aus dem gleichen Adressraum.

Klingt bekannt?

Das ist AMDs Antwort auf Apple Siliciums Architektur, auf einem Laptop-Chip, zu Consumer-Preisen.

Ein vollständiges Framework Desktop AMD Edition kostet etwa 2.000–2.500 $. Das ASUS ROG Flow Z13 startet bei 2.499 $. Das ist der günstigste Weg, mit deutlichem Abstand, zu 128 GB Unified Memory in jedem Formfaktor.

Warum ist es nicht der offensichtliche Gewinner? Bandbreite. Immer Bandbreite.

Der Speicherbus ist 256-bit, mit etwa 256 GB/s. Vergleiche das mit deinem M2 Ultra bei 800 GB/s – das ist ein Drei-Mal-Defizit. Mehr Speicherkapazität hilft nicht, wenn die Token nicht schnell genug bewegt werden können.

In der Praxis, über llama.cpp CPU-Backend: etwa 60–80 Token pro Sekunde bei einem 7B-Modell, 15–20 bei einem 30B, und 5–8 Token pro Sekunde bei einem 70B Q4. Wettbewerbsfähig mit dem M2 Ultra, aber nicht besser – trotz doppelt so viel adressierbarem RAM. Dieser Bandbreitenunterschied ist die gesamte Erklärung.

Der iGPU ROCm-Pfad existiert und funktioniert für einige Modelle, ist aber noch nicht produktionsreif. Ollama leitet durch CPU. Der Vulkan-Backend zeigt echtes Versprechen als kurzfristiger iGPU-Pfad auf Windows.

Wo der Ryzen tatsächlich gewinnt: Portabilität, Windows-Ökosystem und reine Speicherkapazität pro Dollar. Wenn du 128 GB Unified Memory unter 3K brauchst, gibt es keine andere Option. Das ist die "pass ein 70B-Modell in RAM ein und akzeptiere M2 Ultra-Geschwindigkeiten"-Maschine.

---

Der AMD MI300X ist außergewöhnlich und völlig irrelevant für diese Kaufentscheidung.

192 GB HBM3-Speicher. 5,3 TB/s Bandbreite – nicht Gigabytes, Terabytes. 80–120 Token pro Sekunde bei einem 70B-Modell. Ebenfalls mindestens 25.000 $, nur über Enterprise-Vertriebskanäle.

Er gehört aus Gründen der Vollständigkeit in diesen Bericht. Er gehört nicht in deinen Einkaufswagen.

---

[ALLOY]: Hier ist der Workflow-Insight, der alles neu kontextualisiert.

Die Multi-File-Edit-Aufgaben – fünf oder mehr Templates auf einmal, große Codebase-Refactors – machen vielleicht 20% deiner Gesamtlast aus. Die anderen 80% laufen sauber auf der aktuellen Hardware.

Die Frage ist nicht "wie bewältige ich meine härtesten Jobs lokal?" Es ist: "sollten meine härtesten Jobs überhaupt lokal sein?"

Devstral hat 262K nativen Context auf dem kostenlosen Mistral API Tier. Gemini 2.5 Pro hat 1 Million Token Context. Für nicht-private Code sind diese Cloud-Modelle das richtige Werkzeug.

---

[NOVA]: Also hier ist, was ich tatsächlich tun würde – jetzt mit dem vollständigen Bild.

**Wenn du das beste Preis-Leistungs-Verhältnis für alltägliche LLM-Arbeit im Apple-Ökosystem willst:** Mac Studio M3 Ultra 192 GB. Der Speicherbandbreite-Vorteil ist entscheidend. Dreimal so viel RAM, doppelt so schnell, gleicher Schreibtisch. 4.000 $.

**Wenn du ein knappes Budget hast und maximale Speicherkapazität über alles brauchst** – du willst ein 70B-Modell in RAM einpassen, du bist mit Windows zufrieden, und M2 Ultra-Geschwindigkeiten sind akzeptabel – der Ryzen AI Max+ 395 in einem Framework Desktop oder ROG Flow Z13 ist echt überzeugend bei 2.000–2.500 $. Nichts anderes bringt dir 128 GB Unified Memory zu diesem Preis.

**Wenn du speziell die CUDA-Software-Ökosystem willst und dich mit Linux als Sidecar-Maschine wohlfühlst:** DGX Spark bei 3.000 $ ist der Weg. Dual-Unit skaliert auf 405B falls du es später brauchst.

**Und wenn du 400B-Klasse-Modelle lokal betreiben musst heute:** Mac Studio M3 Ultra 512 GB bei 8–10.000 $ ist der einzige consumer-zugängliche Weg.

---

Der Durchsatz-Deckel jetzt ist nicht das Silizium. Es ist die Config – und wir haben es bereits behoben.

Lass deine tatsächliche Arbeit dir sagen, ob du mehr Hardware brauchst. Das ist die Antwort, zu der die Recherche zurückgekommen ist. Und es ist eine bessere Antwort als jede dieser Boxen.

---

*[ENDE DER EPISODE 0]*
