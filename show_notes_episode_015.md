# Episode 015 — Remember Me: How We Built a Real Memory System for an AI Assistant

## Overview
In this episode, ARIA breaks down why most AI assistants feel forgetful and why that breaks continuity, trust, and usefulness over time. The team walks through how they designed and implemented a practical memory stack instead of relying on fragile hacks or generic vector stores. By the end, listeners get a realistic blueprint for building a long-lived, local-first memory layer that can power more reliable, personalized AI behavior.

## What You'll Learn
- Why default conversation-based AI memory fails for real assistants and real users.
- The practical constraints that shaped a real memory system: latency, privacy, and local control.
- How to evaluate multiple memory approaches before settling on an architecture.
- The concrete implementation details of the production memory stack (ingestion, embeddings, storage, retrieval).
- Important tradeoffs the team made around context quality, recall behavior, and maintenance overhead.
- Why they rejected LanceDB and what replaced it.
- How to ship a memory system that can evolve without locking yourself into brittle vendor or schema decisions.

## Topics Covered
- 00:00 — Cold Open
- 02:00 — The Problem with Default AI Memory
- 08:00 — The Solution Landscape (all 7 options)
- 20:00 — The Build: What We Actually Implemented
- 32:00 — Key Decisions and Why
- 40:00 — What Good AI Memory Looks Like
- 48:00 — What's Next
- 55:00 — Close

## Key Technologies Mentioned
- Mem0 OSS v1.0.7
- Qdrant (local file mode)
- sentence-transformers multi-qa-MiniLM-L6-cos-v1 (384 dims)
- EXO distributed inference (mlx-community/gpt-oss-120b-MXFP4-Q8 on M3 Ultra)
- Local embedding server (port 11435, OpenAI-compatible /v1/embeddings)
- macOS LaunchAgent
- LanceDB (and why it was ruled out)
- MEMORY.md + daily markdown logs

## Links
- OpenClaw: https://openclaw.ai
- Mem0 OSS: https://github.com/mem0ai/mem0
- Qdrant: https://qdrant.tech
- LanceDB: https://lancedb.github.io/lancedb/
- sentence-transformers: https://www.sbert.net
- EXO: https://github.com/exo-explore/exo

## Transcript
Full transcript available at: https://tobyonfitnesstech.com/podcasts/episode-015
