# OpenClaw Daily — Episode 13 Show Notes
## "NVIDIA Picked OpenClaw — Here's What That Actually Means"
*Release Date: March 19, 2026*

---

## Episode Summary

NVIDIA GTC 2026 ended this week with a headline that matters for every OpenClaw user: NVIDIA announced **NemoClaw**, an open-source stack built directly on top of OpenClaw for their enterprise hardware. In this episode, Nova and Alloy break down what that actually means, dig into the new model releases (Nemotron 3 Super 120B, Qwen 3.5), analyze what the DGX Spark price hike signals, and cover the v2026.3.13 stability release.

**Runtime: ~39 minutes**

---

## Segments

### Segment 1 — The Headline: NemoClaw
NVIDIA built their local AI agent stack on OpenClaw. What does it mean when the world's largest chip company picks your platform as their foundation?

### Segment 2 — Is NemoClaw For You? (Honest Take)
NemoClaw targets DGX Spark and RTX PRO workstations. If you don't have one, here's what it still means for you — and what it doesn't.

### Segment 3 — Nemotron 3 Super: Can You Run It Locally?
120B parameters, 12B active (MoE), 85.6% on PinchBench — the top-ranked open model for agentic tasks inside OpenClaw. Can your Mac Studio handle it?
- M3 Ultra (96GB): ✅ comfortable at Q4
- M4 Max (64GB): ⚠️ possible at aggressive quantization
- Already in the exo catalog and on OpenRouter today

### Segment 4 — Qwen 3.5 Gets NVIDIA Love
RTX optimizations for Qwen 3.5 (27B/9B/4B): 262K context, native vision, multi-token prediction. Already running locally via exo/MLX.

### Segment 5 — The DGX Spark Price Hike & What It Signals
NVIDIA raised DGX Spark prices after GTC — not lowered. What this tells us about where local AI is heading, and why cloud+local hybrid remains the sweet spot.

### Segment 6 — v2026.3.13 Quick Hits + Wrap
Stability polish: persona continuity through compaction, session reset fixes, Android/iOS UI updates, Telegram/Discord reliability fixes, cross-agent workspace resolution.

---

## Links

- **NemoClaw announcement:** https://blogs.nvidia.com/blog/rtx-ai-garage-gtc-2026-nemoclaw/
- **Nemotron 3 Super on OpenRouter:** https://openrouter.ai/models
- **PinchBench:** https://pinchbench.com
- **Qwen 3.5 27B (HuggingFace):** https://huggingface.co/Qwen/Qwen3.5-27B
- **OpenClaw v2026.3.13-1 release:** https://github.com/openclaw/openclaw/releases
- **Ollama:** https://ollama.com
- **LM Studio:** https://lmstudio.ai
- **exo (local cluster):** https://github.com/exo-explore/exo

---

## Hosts
- **Nova** — warm, British
- **Alloy** — neutral, analytical

---

*OpenClaw Daily is an independent podcast covering the OpenClaw AI assistant platform.*
