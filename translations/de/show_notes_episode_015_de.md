# Folge 015 – Erinnere dich an mich: Wie wir ein echtes Speichersystem für einen KI-Assistenten gebaut haben

## Übersicht
In dieser Folge erläutert ARIA, warum sich die meisten KI-Assistenten vergesslich fühlen und warum dies im Laufe der Zeit Kontinuität, Vertrauen und Nützlichkeit beeinträchtigt. Das Team erläutert, wie es einen praktischen Speicherstapel entworfen und implementiert hat, anstatt sich auf fragile Hacks oder generische Vektorspeicher zu verlassen. Am Ende erhalten die Zuhörer einen realistischen Entwurf für den Aufbau einer langlebigen, lokalen Speicherschicht, die ein zuverlässigeres, personalisiertes KI-Verhalten ermöglichen kann.

## Was Sie lernen werden
– Warum der standardmäßige konversationsbasierte KI-Speicher für echte Assistenten und echte Benutzer versagt.
– Die praktischen Einschränkungen, die ein echtes Speichersystem prägten: Latenz, Privatsphäre und lokale Kontrolle.
– Wie man mehrere Speicheransätze bewertet, bevor man sich für eine Architektur entscheidet.
– Die konkreten Implementierungsdetails des Produktionsspeicherstapels (Aufnahme, Einbettungen, Speicherung, Abruf).
– Wichtige Kompromisse, die das Team in Bezug auf Kontextqualität, Rückrufverhalten und Wartungsaufwand eingegangen ist.
- Warum sie LanceDB abgelehnt haben und was es ersetzt hat.
- Wie man ein Speichersystem liefert, das sich weiterentwickeln lässt, ohne sich auf spröde Anbieter- oder Schemaentscheidungen einzulassen.

## Behandelte Themen
- 00:00 – Kalt geöffnet
- 02:00 – Das Problem mit dem Standard-KI-Speicher
- 08:00 – Die Lösungslandschaft (alle 7 Optionen)
- 20:00 – Der Build: Was wir tatsächlich implementiert haben
- 32:00 – Wichtige Entscheidungen und warum
- 40:00 – Wie ein gutes KI-Gedächtnis aussieht
- 48:00 – Was kommt als nächstes?
- 55:00 – Schließen

## Schlüsseltechnologien erwähnt
- Mem0 OSS v1.0.7
- Qdrant (lokaler Dateimodus)
- Satztransformatoren Multi-QA-MiniLM-L6-Cos-V1 (384 Dims)
- EXO-verteilte Inferenz (mlx-community/gpt-oss-120b-MXFP4-Q8 auf M3 Ultra)
- Lokaler Einbettungsserver (Port 11435, OpenAI-kompatibel /v1/embeddings)
- macOS LaunchAgent
- LanceDB (und warum es ausgeschlossen wurde)
- MEMORY.md + tägliche Markdown-Protokolle

## Links
- OpenClaw: https://openclaw.ai
- Mem0 OSS: https://github.com/mem0ai/mem0
- Qdrant: https://qdrant.tech
- LanceDB: https://lancedb.github.io/lancedb/
- Satztransformatoren: https://www.sbert.net
- EXO: https://github.com/exo-explore/exo

## Transkript
Vollständiges Transkript verfügbar unter: https://tobyonfitnesstech.com/de/podcasts/episode-15/