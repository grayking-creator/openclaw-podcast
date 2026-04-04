# EP023 — Die Infrastruktur-Woche

**OpenClaw Daily** | 3. April 2026 | ~32 Min.

300 Milliarden Dollar in einem Quartal. Anthropic zahlt 400 Millionen für ein Team von neun. Google open-source sein bestes Reasoning-Modell. Und das Weltwirtschaftsforum sagt, es sei an der Zeit, AI-Compute wie Stromnetze und Wassersysteme zu behandeln. Fünf Geschichten über die Woche, in der Infrastruktur aufhörte, langweilig zu sein.

---

## Stories in dieser Folge

### 1. OpenClaw v2026.4.2 — Task Flows, Breaking Migrations und YOLO-Modus
Heiß auf den Fersen von v2026.4.1 (letzte Folge behandelt), landet v2026.4.2 mit Breaking-Plugin-Migrations – xAI-Suche und Firecrawl-web_fetch-Config wurden zu plugin-owned Pfaden verschoben, mit `openclaw doctor --fix` für die Migration. Das Hauptfeature: das Task-Flow-Substrat, das dauerhafte Hintergrund-Orchestrierung mit Managed- vs. Mirrored-Sync-Modi, Revisionsverfolgung und `openclaw flows`-Inspektions-/Wiederherstellungsprimitiven wiederherstellt. Managed Child-Task-Spawning mit Sticky-Cancel-Intent lässt externe Orchestrierer sofort aufhören zu planen, während aktive Aufgaben graceful auslaufen. Android erhält Assistant-Rollen-Einstiegspunkte über Google App Actions – OpenClaw vom Assistant-Trigger starten. Und Host-Exec standardisiert jetzt auf YOLO-Modus (security=full, ask=off) – keine Genehmigungsaufforderungen mehr für vertrauenswürdige Hosts.

**Release:** <https://github.com/openclaw/openclaw/releases/tag/v2026.4.2>

### 2. Google veröffentlicht Gemma 4 — Open-Source Reasoning im großen Maßstab
Google hat Gemma 4 herausgebracht, seine leistungsfähigste Open-Model-Familie. Vier Größen: E2B, E4B, 26B MoE und 31B Dense — alle Apache 2.0. Das 31B-Modell rangiert auf Platz drei der Arena-AI-Text-Rangliste. Die E2B- und E4B-Varianten zielen auf Mobile und IoT mit multimodaler Fähigkeit und Latenz-optimierter Offline-Verarbeitung. Aus derselben Forschung wie Gemini 3 gebaut, 400 Millionen Gemma-Downloads bisher und über 100.000 Community-Varianten. Google macht seine beste Reasoning-Technologie kostenlos verfügbar, nicht nur über API.

**Quelle:** <https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/>

### 3. Anthropic übernimmt Coefficient Bio für 400 Mio. USD — Neun Personen, acht Monate alt
Anthropic zahlte über 400 Millionen Dollar in einem All-Stock-Deal für Coefficient Bio, ein Stealth-Biotech-AI-Startup, das vor kaum acht Monaten gegründet wurde mit weniger als 10 Leuten — fast alle ehemalige Genentech-Forscher. Die Übernahme schafft Anthropics Healthcare- und Life-Sciences-Abteilung und signalisiert, wo Frontier-AI-Labs die nächste Monetarisierungsschicht sehen: nicht in Chatbots, sondern in Medikamentenentwicklung und biologischer Forschung, wo allgemeine Reasoning-Modelle Jahre von Wet-Lab-Iteration ersetzen können.

**Quelle:** <https://thenextweb.com/news/anthropic-just-paid-400-million-for-a-startup-with-fewer-than-10-people>

### 4. Q1 2026 Venture-Finanzierung erreicht 300 Mrd. USD — AI verschlingt 80% allen Kapitals
Die Zahlen sind atemberaubend: 300 Milliarden Dollar in globaler Venture-Finanzierung in Q1 2026, mit AI-Startups, die 242 Milliarden nehmen — 80% von allem. Vier der fünf größten Venture-Runden aller Zeiten passierten in einem einzigen Quartal: OpenAI (122 Mrd. USD), Anthropic (30 Mrd. USD), xAI (20 Mrd. USD), Waymo (16 Mrd. USD). Frühphasen-Finanzierung stieg um 40% gegenüber dem Vorjahr. Die Konzentration ist extrem — drei Frontier-Labs und ein selbstfahrendes Unternehmen absorbierten 188 Milliarden Dollar zwischen ihnen. Die Frage ist nicht, ob AI überfinanziert ist; es ist, ob irgendetwas anderes überhaupt finanziert werden kann.

**Quelle:** <https://news.crunchbase.com/venture/record-breaking-funding-ai-global-q1-2026/>

### 5. Der 690 Mrd. USD Infrastruktur-Sprint — und warum das WEF sagt, behandelt es wie ein Stromnetz
Die fünf größten US-Cloud-Anbieter — Microsoft, Alphabet, Amazon, Meta und Oracle — werden zwischen 660 und 690 Milliarden Dollar für AI-Infrastruktur-Capex in 2026 ausgeben, fast eine Verdoppelung gegenüber 2025. China hält Schritt: Alibaba sagte 53 Milliarden über drei Jahre zu, ByteDance plant 23 Milliarden dieses Jahr allein. Das Weltwirtschaftsforum veröffentlichte diese Woche ein Paper, das argumentiert, dass AI-Compute-Infrastruktur als kritische Infrastruktur klassifiziert werden sollte — dieselbe Kategorie wie Stromnetze, Wassersysteme und Telekommunikation — weil Angriffe auf regionale Rechenzentren jetzt physische, nicht nur Cyber-Verwundbarkeiten darstellen. Wenn Regierungen anfangen, eure GPUs als nationale Sicherheitsassets zu bezeichnen, ist die Infrastruktur-Ära nicht coming — sie ist hier.

**Quellen:**
- <https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/>
- <https://www.weforum.org/stories/2026/04/ai-infrastructure-critical-infrastructure/>

---

## Links
- OpenClaw v2026.4.2: <https://github.com/openclaw/openclaw/releases/tag/v2026.4.2>
- Google Gemma 4: <https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/>
- Anthropic / Coefficient Bio: <https://thenextweb.com/news/anthropic-just-paid-400-million-for-a-startup-with-fewer-than-10-people>
- Q1 2026 Venture-Finanzierung: <https://news.crunchbase.com/venture/record-breaking-funding-ai-global-q1-2026/>
- 690 Mrd. USD AI Capex: <https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/>
- WEF AI-Infrastruktur: <https://www.weforum.org/stories/2026/04/ai-infrastructure-critical-infrastructure/>

---

*OpenClaw Daily wird mit OpenClaw produziert. Neue Episoden erscheinen regelmäßig bei Toby On Fitness Tech Punkt com Slash Podcasts Slash OpenClaw.*
