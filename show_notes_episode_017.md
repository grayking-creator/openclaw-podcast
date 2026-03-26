# OpenClaw Daily — Episode 017: Agents All the Way Down

**"How the New OpenClaw Changes Your Daily Workflow"**

The March 24 OpenClaw release marks a significant shift from polish to possibility. In this episode, NOVA and ALLOY walk through the concrete workflow changes that matter to power users and builders — from nested sub-agents that decompose tasks autonomously, to a hybrid memory system that finally solves the mid-session forgetting problem, to an OpenAI compat layer that makes self-hosted infrastructure a drop-in reality, to Teams and Feishu platform maturity that signals OpenClaw's evolution beyond a Telegram bot framework.

## What We Cover

- **Nested sub-agents with configurable depth** — how agents can now spawn specialists, aggregate results, and operate without user orchestration
- **The `config_manager` tool** — runtime config read/write that enables dynamic agent specialization
- **Hybrid BM25 + vector search** — why exact-match recall now works reliably alongside semantic similarity
- **Embedding cache and adaptive compaction** — the infrastructure changes that prevent mid-session context loss
- **Pluggable ContextEngine interface** — the builder escape hatch for custom memory backends
- **OpenAI compatibility layer** — `/v1/models` and `/v1/embeddings` as native gateway endpoints
- **Self-hosting with EXO clusters** — Qwen3.5-27B distill running as a drop-in OpenAI replacement
- **Microsoft Teams SDK migration** — streaming replies, welcome cards, typing indicators, AI labeling
- **Discord Components v2** — native buttons, dropdowns, and interactive modals
- **Feishu/Lark support** — OpenClaw reaching Asian enterprise markets
- **iOS alpha node app** — OpenClaw running as an active node on iPhone

## Links & Resources

- **OpenClaw Documentation** — [https://docs.openclaw.dev](https://docs.openclaw.dev)
- **OpenClaw GitHub** — [https://github.com/openclaw-dev/openclaw](https://github.com/openclaw-dev/openclaw)
- **Qwen3.5-27B Distill** — [https://www.modelscope.cn/models/Qwen/Qwen3.5-27B-Distill](https://www.modelscope.cn/models/Qwen/Qwen3.5-27B-Distill)
- **LangChain** — [https://www.langchain.com](https://www.langchain.com)
- **LlamaIndex** — [https://www.llamaindex.ai](https://www.llamaindex.ai)
- **Open WebUI** — [https://openwebui.com](https://openwebui.com)
- **Microsoft Teams SDK** — [https://learn.microsoft.com/en-us/microsoftteams/platform/](https://learn.microsoft.com/en-us/microsoftteams/platform/)
- **Feishu / Lark** — [https://www.feishu.cn](https://www.feishu.cn) / [https://www.larksuite.com](https://www.larksuite.com)
- **EXO Cluster Documentation** — [https://docs.openclaw.dev/hardware/exo-cluster](https://docs.openclaw.dev/hardware/exo-cluster)
- **OpenClaw iOS App (Alpha)** — [https://openclaw.dev/ios](https://openclaw.dev/ios)
- **ContextEngine Interface Docs** — [https://docs.openclaw.dev/core/context-engine](https://docs.openclaw.dev/core/context-engine)
- **Show Notes & Episode Archives** — [https://tobyonfitnesstech.com](https://tobyonfitnesstech.com)

## Chapters

- `[00:00]` Hook — The Shift: Why March 24 is different from .22/.23
- `[02:30]` Segment 1 — Agents Spawning Agents: Nested sub-agents, config_manager, workflow scenarios, depth limit risks
- `[10:00]` Segment 2 — Memory Gets Real: Hybrid BM25+vector search, embedding cache, adaptive compaction, ContextEngine pluggability
- `[19:00]` Segment 3 — OpenAI Compat Layer & Self-Hosting: Native `/v1/models` and `/v1/embeddings`, model override forwarding, EXO cluster as OpenAI replacement, iOS node app
- `[24:00]` Segment 4 — Platform Maturity: Teams SDK (streaming, welcome cards, typing indicators, AI labeling), Discord Components v2, Feishu/Lark support
- `[30:00]` Outro / Builder's Take: NOVA's hot take on nested agents + memory, ALLOY's complexity counterpoint, CTA to tobyonfitnesstech.com

## Hosts

- **NOVA** — Host, analytical and concise
- **ALLOY** — Co-host, practical and slightly skeptical
