# EP021 — Inside the Loop

**OpenClaw Daily** | April 2, 2026 | ~30 min

Three AI agent runtimes walk into a codebase. Only one knew what it was building toward. We open the actual source files for OpenClaw, Claude Code, and Hermes Agent — and let the architecture tell us what each one is actually for.

---

## Stories This Episode

### 1. Top-Level Architecture: What Each Runtime Actually Is
- **OpenClaw** (`~/.openclaw/`) — a personal AI OS: gateway daemon as kernel, channel plugins, workspace, cron scheduler, subagent processes, skills system
- **Claude Code** — intentionally narrow: a focused CLI developer tool with sandboxing as its primary differentiator
- **Hermes Agent** — explicitly a research platform: `run_agent.py` / `AIAgent` class, SQLite state at `~/.hermes/state.db`, FTS5 full-text search across all sessions

### 2. The Turn Cycle: How Each System Handles a Single Exchange
The Hermes loop in detail: task ID → append user message → load/build system prompt → preflight compress → build api_messages → inject ephemeral layers → apply prompt caching → interruptible API call → tool execution → persist + return.

Key design signal: **interruptible API calls** — Hermes wraps requests to be cancellable mid-flight from CLI or gateway. And three execution backends: `chat_completions`, `codex_responses`, `anthropic_messages` — genuinely model-agnostic at the routing level.

Claude Code's loop: tight, ephemeral, directory-scoped. No subagent spawning as a first-class concept.

OpenClaw's loop: multi-surface coordination. User message → channel → subagent → optional subagent Z → gateway dispatch back to right surface.

### 3. Memory: SQLite vs. Filesystem vs. Three Layers
**Hermes `~/.hermes/state.db`** — rich schema: sessions table with full billing data (`input_tokens`, `output_tokens`, `estimated_cost_usd`, `actual_cost_usd`, `cost_status`), messages table with `reasoning` and `reasoning_details` columns, FTS5 virtual table with three sync triggers, session lineage via `parent_session_id` chains for context-compressed sessions. Write contention solved with 1s timeout + jitter retries + WAL checkpoints every 50 writes.

**Claude Code** — lighter filesystem-based session state; designed around ephemeral help within a working directory.

**OpenClaw** — three-layer model: raw daily logs (`memory/YYYY-MM-DD.md`), curated long-term memory (`MEMORY.md`), and skills for procedural memory. LCM for context compaction. File-system-native by design.

### 4. Safety Architectures: OS Enforcement vs. Pattern Detection
**Claude Code** — macOS Apple Sandbox Profiles + Linux bwrap (bubblewrap). `SandboxLinux`, `SandboxConfig`, `SandboxManager`, `ViolationStore`. Allowed/denied path lists + seccomp BPF for Unix socket blocking. OS enforces it before anything happens.

**Hermes** — `DANGEROUS_PATTERNS` regex list in `tools/approval.py`. Pattern match → interactive prompt (CLI) or async approval callback to Telegram/Discord (gateway). Session-scoped approvals + permanent `command_allowlist` in `config.yaml`. Smart approval: auxiliary LLM can auto-approve low-risk pattern matches.

**OpenClaw** — hybrid: `exec-approvals.json` approval system + channel-specific permission scoping for subagents.

### 5. The Skills Ecosystem — and `hermes claw migrate`
**Hermes skills** follow the [agentskills.io](https://agentskills.io) open standard: `SKILL.md` + YAML frontmatter. Progressive disclosure: Level 0 (name/description, ~3k tokens) → Level 1 (full content) → Level 2 (specific reference file). Conditional skills, fallback skills, required toolsets.

Agent-created skills are a key differentiator — `skill_manage` lets Hermes write its own skills after complex tasks. The agent learns workflows, not just completes them.

Marketplace: official catalog, `skills.sh`, `/.well-known/skills/`, GitHub repos, ClawHub, Claude marketplace repos. External skill directories via env vars. Portable across agents.

**`hermes claw migrate`** — ships with Hermes to import OpenClaw skills and workspace configurations. The signal: Hermes looked at OpenClaw's skill model and decided it was worth cross-pollinating. OpenClaw is the reference.

### 6. The Verdict — Which Runtime Is for You?

**Use Hermes Agent if:** you want a self-improving research companion with long-term memory, model-agnostic flexibility, FTS5 history search, a rich skill ecosystem, and multi-channel presence (Telegram, Discord, Slack, WhatsApp, Signal). Also the right choice if you're interested in RL-based agent improvement (`rl_training_tool`, Atropos environments). OpenClaw users: `hermes claw migrate` brings your skills with you.

**Use Claude Code if:** you're a developer who wants the best focused help in a specific codebase with the strongest OS-level sandboxing. The bubblewrap + Apple Sandbox integration is the most rigorous of the three. Trade-off: no persistent cross-session memory, no multi-channel presence.

**Use OpenClaw if:** you want a persistent personal AI OS — always on, multi-surface, multi-agent, with cron scheduling, skill system, and a Unix-native workspace model. The fact that Hermes ships a migration tool *from* OpenClaw tells you which model is the reference.

---

## Key Files & Classes Referenced

| Runtime | File | Class/Function |
|---------|------|----------------|
| Hermes | `run_agent.py` | `AIAgent` |
| Hermes | `hermes_state.py` | `SessionDB` |
| Hermes | `tools/registry.py` | `ToolRegistry`, `ToolEntry` |
| Hermes | `tools/approval.py` | `DANGEROUS_PATTERNS`, `detect_dangerous_command()` |
| Hermes | `agent/context_compressor.py` | — |
| Hermes | `agent/prompt_builder.py` | — |
| Hermes | `~/.hermes/state.db` | SQLite WAL mode, FTS5 |
| Claude Code | `cli.js` | tool registry, permission layers |
| Claude Code | `sandbox_linux.py` | `SandboxLinux`, `SandboxManager`, `ViolationStore` |
| OpenClaw | `~/.openclaw/` | gateway daemon, channel plugins, cron, workspace |

---

## Model Recommendations (from Hermes docs)

- **Best start:** Claude Sonnet via Anthropic OAuth — auto-reads Claude Code's credential store
- **Free + capable:** GitHub Copilot subscription → GPT-5.4, Claude, Gemini via Copilot API
- **Maximum flexibility:** OpenRouter key → 200+ models; also unlocks vision/web/MoA auxiliary tools
- **Local models:** Any Ollama or vLLM endpoint via `OPENAI_BASE_URL`
- **Chinese providers:** GLM (Z.ai), Kimi/Moonshot, MiniMax, Qwen — first-class provider IDs, not afterthoughts

---

## Subscribe

🎙️ **Apple Podcasts** | **Spotify** | **Pocket Casts** | **Amazon Music**
🌐 [tobyonfitnesstech.com/podcasts/episode-21/](https://tobyonfitnesstech.com/podcasts/episode-21/)
