# OpenClaw Daily EP052: Lokale Agents bekommen ihre Hardware-Woche

Diese Episode verfolgt sechs konkrete Schritte im Agent-Stack. Der Schwerpunkt liegt auf lokaler Infrastruktur: lokale Model-Runner, Apple Silicon Beschleunigung, DGX Spark als lokale Agent-Maschine, EXO verteilte Inferenz, Coding-Agent-CLIs und die Gateway-Schicht, die verhindert, dass das Model-Routing spröde wird.

[00:00] Ollama entwickelt sich vom Model-Runner zum Coding-Agent-Platform

Ollamas letzte Releases zeigen, dass es sich zu mehr als einem lokalen Model-Server entwickelt. Die wichtigsten Punkte sind Codex App-Unterstützung durch Ollama Launch, Vision-Model-Unterstützung für opencode launch, lokale Bildpfad-Fixes für Claude-Tool-Ergebnisse und API-Show-Response-Caching, das die durchschnittliche Integrationslatenz um etwa das 6,7-fache verbessert.

Der wichtigere zukunftsorientierte Punkt ist der Release Candidate 0.30.0. Ollama gibt an, dass diese Version die Architektur ändert, um llama.cpp direkt zu unterstützen, GGUF-Dateikompatibilität ermöglicht und MLX verwendet, um die Inferenz auf Apple Silicon zu beschleunigen. Arbeiten Anfang Mai fügten auch Gemma 4 MTP spekulative Dekodierung im MLX-Runner hinzu, mit einem behaupteten mehr als 2-fachen Geschwindigkeitszuwachs für Gemma 4 31B Coding-Aufgaben.

Die praktische Erkenntnis: Ollama bewegt sich näher daran, eine lokale Runtime-Schicht für Coding-Agents und Desktop-KI-Tools zu werden. Modellportabilität, MLX-Beschleunigung, schnellere Metadatenaufrufe, Launch-Integrationen und Vision-Eingaben spielen alle eine Rolle, wenn ein lokaler Agent echte Projektarbeit leisten muss, anstatt nur Prompts zu beantworten.

Quellen:
- https://github.com/ollama/ollama/releases

[05:00] LM Studio verbessert MLX-Vision-Inferenz und zeigt Richtung gemeinsamer lokaler Server

LM Studio 0.4.13 liefert mlx-engine v1.8.1. Das offizielle Changelog besagt, dass es die Leistung erheblich verbessert und parallele Vorhersagen für visionfähige Modelle einschließlich Qwen 3.5/3.6 und Gemma 4 hinzufügt. Dieselbe Version behebt die Handhabung eingefügter Zeilenumbrüche und enthält Sicherheitshärtung.

Das klingt klein, bis man es neben das setzt, wohin LM Studio mit größeren Maschinen strebt. Sein DGX Station Material beschreibt einen headless Daemon, llmster, gepaart mit LM Link, damit eine Maschine lokale Modelle an andere Geräte bereitstellen kann. Es hebt auch LM Studio SDKs, die LM Studio API und OpenAI-kompatible und Anthropic-kompatible APIs hervor.

Die Relevanz für Entwickler ist straightforward: Lokale KI wird ein zweiteiliger Stack. Ein Laptop oder Mac kann die Schnittstelle sein, während eine größere lokale Maschine die Modelllast übernimmt. Für Vision-Agents sind MLX-parallele Vorhersageverbesserungen wichtig, weil Screenshots, Bilder, UI-Zustand und multimodaler Projektkontext zu normalen Eingaben werden, keine Demos mehr.

Quellen:
- https://lmstudio.ai/changelog/lmstudio-v0.4.13
- https://lmstudio.ai/blog/dgx-station

[10:00] DGX Spark wird ein ernstzunehmendes lokales Agent-Ziel

NVIDIAs aktuelle DGX Spark und RTX-Messaging dreht sich explizit um lokale Agents. Das Unternehmen framing diese Maschinen als Agent-Computer zum Ausführen persönlicher Agents lokal, privat und ohne Token-Kosten. Sein GTC-Material hebt Nemotron 3 Nano 4B, Nemotron 3 Super 120B, Qwen 3.5-Optimierungen, Mistral Small 4 und lokale Agent-Stacks hervor, die durch Ollama, LM Studio und llama.cpp laufen.

DGX Spark ist wichtig wegen Speicher und Einsatzform. NVIDIA beschreibt DGX Spark mit 128GB Unified Memory, genug für Modelle über 120B Parameter. Nemotron 3 Super wird als 120B Open Model mit 12B aktiven Parametern beschrieben, während kleinere Modelle wie Nemotron 3 Nano 4B stärker eingeschränkte RTX-Maschinen anvisieren.

Der Punkt ist nicht, dass jeder Entwickler einen kaufen sollte. Der Punkt ist, dass lokale Agent-Software jetzt eine Hardware-Stufe über einem einzelnen Desktop und unter gemieteter Cloud-GPU-Infrastruktur hat. Wenn lokale Agents den Kontext privat halten, den ganzen Tag laufen und Tools aufrufen sollen, ohne für jeden Schritt Token-Kosten für Cloud-Dienste zu zahlen, werden Maschinen wie DGX Spark zur relevanten Infrastruktur.

Quellen:
- https://blogs.nvidia.com/blog/rtx-ai-garage-gtc-2026-nemoclaw/
- https://build.nvidia.com/spark/hermes-agent

[15:00] EXO plus DGX Spark zeigt, dass verteilte lokale Inferenz real, aber noch rau ist

Ein EXO-Issue rund um DGX Spark ist nützlicher als eine saubere Pressemitteilung, weil er den tatsächlichen Fehlermodus zeigt. Der Cluster hatte Macs und einen DGX Spark im selben lokalen Netzwerk, grundlegende Konnektivität funktionierte, EXO-Dashboard-Zugriff funktionierte und Ports waren erreichbar. Aber die Nodes bildeten trotzdem keinen funktionierenden verteilten Inferenz-Cluster.

Die gemeldete Lösung hatte zwei Teile. Erstens musste das Rust exo_pyo3_bindings Networking-Modul, das libp2p-Networking, mDNS-Discovery und Private-Network-Logik enthält, manuell auf Linux/aarch64 kompiliert werden. Zweitens benötigten alle Nodes denselben EXO_LIBP2P_NAMESPACE, damit der libp2p Private-Network-Key über den Cluster hinweg übereinstimmte.

Danach erschien der DGX Spark im EXO-Dashboard und nahm an verteilter Inferenz teil. Das ist die wahre Geschichte: EXO bewältigt das richtige lokale Cluster-Problem, aber verteilte lokale Inferenz lebt oder stirbt durch Discovery, Packaging, Namespace-Anpassung und architekturspezifische Builds. Rohe Rechenleistung reicht nicht aus, wenn die Knoten sich nicht zuverlässig finden und vertrauen können.

Quellen:
- https://github.com/exo-explore/exo/issues/1682

[20:00] Grok Build ist da, aber Modell-Weiterleitungen und Preisgestaltung erfordern Aufmerksamkeit

Die Grok Build-Dokumentation von xAI beschreibt eine vollständige Coding-Agent-CLI-Oberfläche: eine interaktive TUI, Headless-Scripting, Plain/JSON/Streaming-JSON-Ausgabe, fortsetzbare Sitzungen, ACP über Grok Agent stdio, benutzerdefinierte Modellkonfiguration, Skills, Plugins, Hooks und MCP-Server-Discovery.

Das macht Grok Build zu derselben Kategorie wie andere Coding-Agent-CLIs: ein terminal-nativer Agent mit Automatisierungs-Hooks, nicht nur eine Chat-Oberfläche. Die offizielle Dokumentation zeigt auch benutzerdefinierte Modellkonfiguration, was wichtig ist, weil Entwickler zunehmend Coding-Agent-Shells wollen, die an verschiedene Modell-Backends weiterleiten können.

Die Kosten- und Migrationsgeschichte ist separat, aber wichtig. Die Seite von xAI zur Einstellung am 15. Mai besagt, dass veraltete Reasoning-Slugs auf Grok 4.3 mit geringem Reasoning-Aufwand weiterleiten, Nicht-Reasoning-Slugs auf Grok 4.3 ohne Reasoning-Aufwand weiterleiten und grok-code-fast-1 auf Grok 4.3 weiterleitet. Die Seite listet die Grok 4.3 API-Preise bei 1,25 $ pro Million Input-Tokens und 2,50 $ pro Million Output-Tokens auf. Die praktische Empfehlung ist, Ersatzmodelle explizit zu pinnen, anstatt veraltete Slugs das Verhalten und die Abrechnung still ändern zu lassen.

Quellen:
- https://docs.x.ai/build/overview
- https://docs.x.ai/build/cli/headless-scripting
- https://docs.x.ai/developers/migration/may-15-retirement

[25:00] LiteLLM und Envoy härten die Model-Gateway-Schicht

LiteLLM v1.84.0 ist ein Gateway-Härtungs-Release. Das Release ändert die Versionsbenennung auf PEP 440, authentifiziert Pass-Through-Endpunkte standardmäßig, verbessert die Multi-Pod-Budget-Durchsetzung, vermeidet Prisma-Reconnect-Freezes, reduziert den Speicherbedarf durch Lazy-Loaded-Feature-Router, fügt MCP-OAuth und Azure-Entra-Discovery-Unterstützung hinzu und fügt dauerhaftes Workflow-Run-Tracking durch eine Workflow-Runs-API-Oberfläche hinzu.

Envoy AI Gateway v0.6.0 bewegt sich in dieselbe Richtung von der Kubernetes-Gateway-Seite. Es Graduiert Core CRDs auf v1beta1, fügt Anthropic-Endpunkt-Unterstützung auf OpenAI-kompatiblen Backends hinzu, fügt Gemini-Embeddings und Context-Caching hinzu, unterstützt MCP pro Backend Header-Forwarding, fügt Request/Response-Body-Redaktion hinzu und aktualisiert die Envoy/Gateway-Basislinie.

Der Grund, warum dies in eine Local-Agent-Episode gehört, ist, dass Local-First nicht gateway-frei bedeutet. Agents brauchen immer noch Routing, Auth, Budgets, Redaktion, Provider-Kompatibilität und MCP-Autorisierung. Je mehr Modell-Backends und lokale Runtimes Sie hinzufügen, desto wichtiger wird die Control Plane.

Quellen:
- https://docs.litellm.ai/release_notes/v1.84.0/v1-84-0
- https://aigateway.envoyproxy.io/release-notes/