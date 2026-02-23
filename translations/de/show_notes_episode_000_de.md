# Episode 0: Hardware Deep Dive – Beheben von lokalen Modellfehlern
**Datum:** 18. Februar 2026
**Dauer:** 11:45
**Moderatoren:** Nova & Alloy

---

## SHOW NOTES

### behandelte Themen

1. **Der Context-Overflow-Bug** — Clarity (Coding-Agent, Qwen3-Coder-30B) hat wiederholt Context-Overflow-Fehler mitten in Aufgaben erhalten. Ursache: Eine Ollama-Modelldefinition mit dem Namen `v-128k`, die den Context auf 131.072 Token begrenzte, während das Modell nativ 262.144 Token unterstützt. Ein Config-Label vom Setup-Tag wurde versehentlich zur harten Grenze.

2. **Die Timeout-Mathematik** — Am 18. Februar um 11:15 Uhr wurden 146.760 Token gegen ein Limit von 131.072 Token abgefragt. Bei einer Prefill-Geschwindigkeit von ~400 Token/sec dauert die Verarbeitung von 146K Token über 6 Minuten. Der Timeout-Schwellenwert lag bei 5 Minuten. Drei aufeinanderfolgende Treffer – keine Abstürze, keine Instabilität – perfekt durch die Arithmetik erklärt.

3. **Qwen3-Coder-Speicherarchitektur** — Qwen3-Coder 30B ist ein Mixture-of-Experts-Modell mit nur 4 KV-Attention-Heads (vs. 8 bei LLaMA-3 8B). Bei 262K Context: ~15 GB Modellgewichte + ~24 GB KV-Cache + OS-Overhead ≈ 44 GB gesamt. Eine Maschine mit 64 GB Unified Memory hat 20 GB Spielraum. Die Hardware war die ganze Zeit in Ordnung.

4. **Hardware-Option 1: NVIDIA DGX Spark (3.000 $)** — GB10 Grace Blackwell Chip, 128 GB LPDDR5X, 273 GB/s Speicherbandbreite. Kontraintuitiv geringere Bandbreite als ein Mac Studio M2 Ultra (~800 GB/s). Kompensiert über FP4-Tensor-Cores (25–50 Tok/s bei 70B vs. aktuell 10–15). Linux-nur Sidecar; zwei Einheiten für 6K verlinken um 405B+ Modelle zu betreiben.

5. **Hardware-Option 2: Mac Studio M3 Ultra** — 4.000 $ (192 GB) bis 8–10K (512 GB). 819 GB/s Bandbreite, 2,1× schneller als M2 Ultra laut Apple-Benchmarks. 20–32 Tok/s bei 70B-Modellen. 192-GB-Konfiguration ermöglicht gleichzeitiges Laden von 30B + 70B-Modellen ohne Swapping. 512-GB-Konfiguration ist der einzige Consumer-Weg, um LLaMA 3.1 405B lokal zu betreiben.

6. **Hardware-Option 3: AMD** — Zwei Geschichten:
   - *Threadripper + duale RX 7900 XTX (5–6K)*: Split-VRAM-Problem, ROCm hinkt CUDA hinterher. Keine Empfehlung.
   - *Ryzen AI Max+ 395 "Strix Halo" (2.000–2.500 $)*: AMDs Antwort auf Apple Silicon — CPU/GPU/NPU Unified Memory bis zu 128 GB LPDDR5X. Framework Desktop AMD oder ASUS ROG Flow Z13. Speicherbandbreite ist 256 GB/s (256-Bit-Bus), ~3× weniger als M2 Ultra – trotz doppelt so viel adressierbarem RAM wettbewerbsfähige Geschwindigkeiten. Bester Budget-Weg zu 128 GB Unified Memory, Punkt.
   - *AMD MI300X (25K, Enterprise)*: 192 GB HBM3, 5,3 TB/s Bandbreite, 80–120 Tok/s bei 70B. Der Vollständigkeit halber erwähnt; kein Consumer-Kauf.

7. **Workflow-Strategie: Hybrid Local + Cloud** — Schwere Multi-File-Änderungen (5+ Templates, große Codebase-Refactors) machen ~20% der Gesamtlast aus. Für nicht-private Code: Devstral bietet 262K nativen Context auf dem kostenlosen Mistral API Tier; Gemini 2.5 Pro bietet 1 Million Token. Die richtige Frage ist nicht "wie bringe ich meine härtesten Jobs lokal zum Laufen?" – sondern "sollten meine härtesten Jobs überhaupt lokal sein?"

8. **Die Lösung** — Config-Patch + neue Ollama-Modelldefinition um den vollen 262K-Context-Freiraum freizuschalten. Live während der Recherche gemacht. Null Kosten.

### Hardware-Ressourcen
- [Apple Mac Mini](https://www.apple.com/mac-mini/) - Empfohlen für lokale KI
- [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) - Budget-Option
- [Ollama](https://ollama.com) - Lokaler LLM-Runtime

---

### Wichtige Erkenntnisse

1. **Ein Modell-Label ist keine Leistungsgrenze.** Der Ollama-Modellname `qwen3-coder:30b-262k` sagte die Wahrheit; das Erstellungszeit-Label nicht. Überprüfe immer die Context-Fenster-Config gegen die tatsächliche Modell-Spec.
2. **Token-Generierung ist speicherbandbreitengebunden, nicht computegebunden.** Der DGX Spark hat weniger Speicherbandbreite als ein Mac Studio. Bandbreite ist der Flaschenhalh – überprüfe immer GB/s, nicht nur GB.
3. **Strix Halo (Ryzen AI Max+ 395) ist der günstigste Weg zu 128 GB Unified Memory.** Nichts anderes kommt unter 3K heran. Der Kompromiss ist ~3× weniger Bandwidth als Apple Silicon.
4. **Diagnostiziere bevor du kaufst.** Drei Schichten Fehlkonfiguration (falsches Context-Cap + Timeout zu kurz + Modell-Cap überschritten) sahen aus wie Hardwarefehler. Sie waren vollständig durch Config behebbar.
5. **Der Hybrid Local/Cloud-Split ist der eigentliche Effizienzhebel.** Lagere die 20% der schweren Context- nicht-privaten Aufgaben an Devstral oder Gemini 2.5 Pro aus. Betreibe die anderen 80% lokal, wo Datenschutz wichtig ist.

---

### Ressourcen & Links

| Artikel | Details |
|---------|---------|
| **Qwen3-Coder 30B** | Ollama: `ollama pull qwen3-coder:30b-262k` |
| **NVIDIA DGX Spark** | 3.000 $ — nvidia.com/en-us/project-digits |
| **Mac Studio M3 Ultra** | 3.999 $ (192 GB) / 7.999 $+ (512 GB) — apple.com |
| **AMD Ryzen AI Max+ 395** | Framework Desktop AMD Edition ~2.000–2.500 $ |
| **ASUS ROG Flow Z13** | 2.499 $ — Ryzen AI Max+ 395, bis zu 128 GB |
| **AMD MI300X** | 25.000 $+ Enterprise — nur zur Referenz |
| **Devstral** | 262K Context, kostenloser Tier — mistral.ai |
| **Gemini 2.5 Pro** | 1M Context — aistudio.google.com |
| **llama.cpp** | CPU-Inference-Backend — github.com/ggerganov/llama.cpp |
| **Ollama** | Lokaler Model-Runtime — ollama.com |
