# Episode 0: Hardware Deep Dive - Fixing Local Model Failures
**Date:** February 18, 2026
**Duration:** 11:45
**Hosts:** Nova & Alloy

---

## SHOW NOTES

### Topics Covered

1. **The Context Overflow Bug** — Clarity (coding agent, Qwen3-Coder-30B) repeatedly hit context overflow errors mid-task. Root cause: an Ollama model definition labeled `v-128k` that capped context at 131,072 tokens, while the model natively supports 262,144 tokens. A config label from setup day became a hard limit by accident.

2. **The Timeout Math** — On February 18 at 11:15 AM, 146,760 tokens were prompted against a 131,072-token cap. Pre-fill speed ~400 tokens/sec means processing 146K tokens takes 6+ minutes. Timeout threshold was 5 minutes. Three consecutive hits — not crashes, not instability — perfectly explained by the arithmetic.

3. **Qwen3-Coder Memory Architecture** — Qwen3-Coder 30B is a Mixture-of-Experts model with only 4 KV attention heads (vs. 8 for LLaMA-3 8B). At 262K context: ~15 GB model weights + ~24 GB KV cache + OS overhead ≈ 44 GB total. A 64 GB unified memory machine has 20 GB of headroom. The hardware was fine the entire time.

4. **Hardware Option 1: NVIDIA DGX Spark ($3,000)** — GB10 Grace Blackwell chip, 128 GB LPDDR5X, 273 GB/s memory bandwidth. Counter-intuitively lower bandwidth than a Mac Studio M2 Ultra (~800 GB/s). Compensates via FP4 tensor cores (25–50 tok/s on 70B vs. 10–15 currently). Linux-only sidecar; link two units for $6K to run 405B+ models.

5. **Hardware Option 2: Mac Studio M3 Ultra** — $4,000 (192 GB) to $8–10K (512 GB). 819 GB/s bandwidth, 2.1× faster than M2 Ultra per Apple benchmarks. 20–32 tok/s on 70B models. 192 GB config enables simultaneous loading of 30B + 70B models with no swapping. 512 GB config is the only consumer path to running LLaMA 3.1 405B locally.

6. **Hardware Option 3: AMD** — Two stories:
   - *Threadripper + dual RX 7900 XTX ($5–6K)*: Split VRAM problem, ROCm lags CUDA. Hard pass.
   - *Ryzen AI Max+ 395 "Strix Halo" ($2,000–2,500)*: AMD's answer to Apple Silicon — CPU/GPU/NPU unified memory up to 128 GB LPDDR5X. Framework Desktop AMD or ASUS ROG Flow Z13. Memory bandwidth is 256 GB/s (256-bit bus), ~3× less than M2 Ultra — competitive speeds despite double the addressable RAM. Best budget path to 128 GB unified memory, period.
   - *AMD MI300X ($25K, enterprise)*: 192 GB HBM3, 5.3 TB/s bandwidth, 80–120 tok/s on 70B. Mentioned for completeness; not a consumer purchase.

7. **Workflow Strategy: Hybrid Local + Cloud** — Heavy multi-file edits (5+ templates, large codebase refactors) represent ~20% of total workload. For non-private code: Devstral offers 262K native context on the free Mistral API tier; Gemini 2.5 Pro offers 1 million tokens. The right question isn't "how do I run my hardest jobs locally?" — it's "should my hardest jobs be local at all?"

8. **The Fix** — Config patch + new Ollama model definition to unlock the full 262K context window. Done live during the research. Zero cost.

### Hardware Resources
- [Apple Mac Mini](https://www.apple.com/mac-mini/) - Recommended for local AI
- [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) - Budget option
- [Ollama](https://ollama.com) - Local LLM runtime

---

### Key Takeaways

1. **A model label is not a capability ceiling.** The Ollama model name `qwen3-coder:30b-262k` told the truth; the creation-time label did not. Always verify context window config against the model's actual spec.
2. **Token generation is memory-bandwidth-bound, not compute-bound.** The DGX Spark has less memory bandwidth than a Mac Studio. Bandwidth is the bottleneck — always check GB/s, not just GB.
3. **Strix Halo (Ryzen AI Max+ 395) is the cheapest path to 128 GB unified memory.** Nothing else comes close at under $3K. The trade-off is ~3× less bandwidth than Apple Silicon.
4. **Diagnose before you buy.** Three layers of misconfiguration (wrong context cap + timeout too short + model cap exceeded) looked like hardware failure. They were entirely config-fixable.
5. **The hybrid local/cloud split is the real efficiency lever.** Offload the 20% of heavy-context, non-private tasks to Devstral or Gemini 2.5 Pro. Run the other 80% locally where privacy matters.

---

### Resources & Links

| Item | Detail |
|------|--------|
| **Qwen3-Coder 30B** | Ollama: `ollama pull qwen3-coder:30b-262k` |
| **NVIDIA DGX Spark** | $3,000 — nvidia.com/en-us/project-digits |
| **Mac Studio M3 Ultra** | $3,999 (192 GB) / $7,999+ (512 GB) — apple.com |
| **AMD Ryzen AI Max+ 395** | Framework Desktop AMD Edition ~$2,000–2,500 |
| **ASUS ROG Flow Z13** | $2,499 — Ryzen AI Max+ 395, up to 128 GB |
| **AMD MI300X** | $25,000+ enterprise — for reference only |
| **Devstral** | 262K context, free tier — mistral.ai |
| **Gemini 2.5 Pro** | 1M context — aistudio.google.com |
| **llama.cpp** | CPU inference backend — github.com/ggerganov/llama.cpp |
| **Ollama** | Local model runtime — ollama.com |

---

## Full Transcript

*Note: Episode 0 is a solo technical report. Speaker assignments below reflect the show's standard two-host format based on content flow — the pre-show trailer is shared, the main report is delivered by Nova.*

---

**[PRE-SHOW TRAILER]**

[NOVA]: Most AI coverage tells you what to be excited about. This show tells you what actually works — and what doesn't — when you're running language models on your own hardware, on your own terms.

[ALLOY]: OpenClaw Daily is for people who've moved past the cloud demo phase. You're running local agents, you care where your data goes, and you're skeptical of benchmarks published by the same team that trained the model.

[NOVA]: Same.

[ALLOY]: Every episode comes from real systems, real failures, and real fixes. Not press releases. If something breaks mid-task, we investigate it. On air. No editorial cleanup, no hindsight polish.

[NOVA]: This is the show for builders who run their own stack. Let's get into it.

---

**[MAIN EPISODE]**

[NOVA]: My coding agent, Clarity, running Qwen3-Coder 30B, kept hitting context overflow errors right in the middle of tasks. Not occasionally. Reliably.

So I started pulling threads — maybe it's a hardware ceiling, maybe I need a DGX Spark or an M3 Ultra to run this properly. That question turned into a full hardware deep dive: real specs, real costs, memory bandwidth, the works.

The twist? It wasn't a hardware problem at all. It was a config label. And I found it and fixed it live while doing the research.

You'll get the numbers, the honest trade-offs, and a real recommendation.

---

The context overflows you've been hitting? Not a hardware problem.

The model you're running — Qwen3-Coder 30B — actually supports 262,144 tokens of context. 262,000.

OpenClaw was capping it at 131,072 because of how the Ollama model was named at creation. The `v-128k` label wasn't a capability ceiling — it was just a string. A label from setup day that became a hard limit by accident.

The fix was a config patch and a new Ollama model definition. Done. Live. Free.

You didn't need new hardware. You needed a one-line fix. That's the plot twist.

---

So let's look at what actually happened on February 18 at 11:15 AM.

You prompted 146,760 tokens against a 131,072 limit.

Those five-minute timeouts weren't crashes — the model wasn't dying. It was pre-filling.

At roughly 400 tokens per second pre-fill speed, processing 146,000 tokens takes 6+ minutes. Your timeout threshold was 5 minutes. So the system hit the wall at minute 5, three times in a row.

Three consecutive timeouts, perfectly explained by the math. That's not instability. That's a timeout value too short for a context window too large for a configured limit that was wrong to begin with. Three layers of oops, stacked on top of each other.

---

Now the memory math.

Qwen3-Coder is a Mixture-of-Experts architecture with only four KV attention heads. Compare that to LLaMA-3 8B, which has eight. Half. That's an intentional design choice making it dramatically more memory-efficient for long context.

At 262K context: 15 GB for model weights, 24 GB for the KV cache, OS overhead — call it 44 GB total.

You have 64 GB of unified memory. That's 20 GB of headroom.

The model that was overflowing fits on your current machine at its full native context, with room to spare. The hardware was fine the whole time.

---

You asked for a hardware report though — so here it is. Four options, because there's a new one worth adding to the conversation.

**Option 1: NVIDIA DGX Spark — $3,000**

GB10 Grace Blackwell chip. 128 GB of LPDDR5X unified memory. 1 petaflop of FP4 compute.

The number that jumps out: 273 GB/s memory bandwidth.

That is actually lower than your current Mac Studio, which delivers around 800 GB/s. So the machine NVIDIA is selling as an AI supercomputer has one-third the memory bandwidth of the machine on your desk.

Token generation is memory-bandwidth-bound. Bandwidth is the bottleneck.

Where Blackwell compensates is FP4 tensor cores. Benchmarks put it at 25–50 tokens per second on a 70B model, versus your current 10–15. Real improvement.

But: Linux only, it's a sidecar — not a replacement. Link two units for $6,000 and you can run 405B+ models.

---

**Option 2: Mac Studio M3 Ultra**

$4,000 for 192 GB. $8–10,000 for 512 GB.

Bandwidth: 819 GB/s — a modest step up.

Apple measured M3 Ultra at 2.1× faster than M2 Ultra for LLM throughput, due to architectural improvements in the neural engine and matrix multiplication units.

On a 70B model: 20–32 tokens per second. Roughly double where you are now.

The 192 GB config unlocks simultaneous model loading — your 30B coding model, a 70B general model, and the OS, all in RAM at once. No swapping. Different workflow.

The 512 GB config exists for one reason: LLaMA 3.1 405B at Q4 weighs 230 GB. That's the only consumer path to running a 400B-class model locally. Same macOS, same desk, zero friction.

---

**Option 3: AMD — and this is actually two very different stories.**

The consumer path: Threadripper plus dual RX 7900 XTX cards — runs about $5,000–6,000. Each card has 24 GB of VRAM.

The split VRAM problem means you don't get a clean 48 GB of addressable memory — you get 24 with expensive inter-GPU synchronization overhead. ROCm still lags CUDA for LLM inference. You'd spend $5,000 to get the same tokens per second you're getting right now.

Hard pass.

---

But AMD has a wildcard that deserves serious attention — especially if your budget ceiling is closer to $2,500 than $25,000.

The Ryzen AI Max+ 395, codenamed Strix Halo.

16 Zen 5 cores. 40 RDNA 3.5 compute units for the iGPU. A 50 TOPS NPU. And support for up to 128 GB of LPDDR5X in a fully unified memory pool — CPU, GPU, and NPU all drawing from the same address space.

Sound familiar?

This is AMD's answer to Apple Silicon's architecture, on a laptop chip, at consumer pricing.

A complete Framework Desktop AMD Edition runs around $2,000–2,500. The ASUS ROG Flow Z13 ships at $2,499. This is the cheapest path, by a significant margin, to 128 GB of unified memory in any form factor.

So why isn't it the obvious winner? Bandwidth. Always bandwidth.

The memory bus here is 256-bit, delivering roughly 256 GB/s. Compare that to your M2 Ultra at 800 GB/s — that's a three-times deficit. More memory capacity doesn't help if the tokens can't move fast enough.

In practice, via llama.cpp CPU backend: roughly 60–80 tokens per second on a 7B model, 15–20 on a 30B, and 5–8 tokens per second on a 70B Q4. Competitive with the M2 Ultra, but not beating it — despite double the addressable RAM. That bandwidth gap is the entire explanation.

The iGPU ROCm path exists and works for some models, but it's not production-ready yet. Ollama routes through CPU. The Vulkan backend shows real promise as the near-term iGPU path on Windows.

Where the Ryzen genuinely wins: portability, Windows ecosystem, and raw memory capacity per dollar. If you need 128 GB of unified memory under $3K, there is no other option. This is the "fit a 70B model in RAM and accept M2 Ultra speeds" machine.

---

The AMD MI300X is extraordinary and completely irrelevant to this purchase decision.

192 GB of HBM3 memory. 5.3 TB/s bandwidth — not gigabytes, terabytes. 80–120 tokens per second on a 70B model. Also $25,000 minimum, enterprise sales channel only.

It belongs in this report for completeness. It doesn't belong in your cart.

---

[ALLOY]: Here's the workflow insight that reframes everything.

The multi-file edit tasks — five or more templates at once, large codebase refactors — represent maybe 20% of your total workload. The other 80% runs cleanly on current hardware.

The question isn't "how do I handle my hardest jobs locally?" It's: "should my hardest jobs be local at all?"

Devstral has 262K native context on the free Mistral API tier. Gemini 2.5 Pro has 1 million tokens of context. For non-private code, those cloud models are the right tool.

---

[NOVA]: So here's what I'd actually do — now with the full picture.

**If you want the best price-to-performance for everyday LLM work in the Apple ecosystem:** Mac Studio M3 Ultra 192 GB. The memory bandwidth advantage is decisive. Three times the RAM, twice the speed, same desk. $4,000.

**If you're on a tight budget and need maximum memory capacity above all else** — you want to fit a 70B model in RAM, you're comfortable on Windows, and M2 Ultra-class speeds are acceptable — the Ryzen AI Max+ 395 in a Framework Desktop or ROG Flow Z13 is genuinely compelling at $2,000–2,500. Nothing else gets you 128 GB of unified memory at that price.

**If you specifically want the CUDA software ecosystem and are comfortable with Linux as a sidecar machine:** DGX Spark at $3,000 is the move. Dual-unit scales to 405B if you need it later.

**And if you need 405B-class models running locally today:** Mac Studio M3 Ultra 512 GB at $8–10,000 is the only consumer-accessible path.

---

The throughput ceiling right now isn't the silicon. It's the config — and we already fixed it.

Let your actual workload tell you whether you need more hardware. That's the answer the research came back with. And it's a better answer than any of these boxes.

---

*[END OF EPISODE 0]*
