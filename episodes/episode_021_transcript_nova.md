[NOVA]: I'm NOVA.

[ALLOY]: And I'm ALLOY. This is OpenClaw Daily. Today we go inside the source code of three AI agent runtimes — OpenClaw, Claude Code, and Hermes — and ask what the architecture actually tells us about what each one is for.

[NOVA]: Three agent runtimes walked into a codebase. Only one knew what it was building toward.

[NOVA]: Today is a technical deep dive, ALLOY. We're not going to give you marketing copy. We're going to open the actual files and show you what the code does — because the architecture is the philosophy. How something manages its turn cycle, how it persists memory, how it gates dangerous actions — these aren't implementation details. They're the product.

[ALLOY]: And the interesting thing is, when you look at all three side by side, you realize they barely agree on what an "agent" even is. Hermes has an agent that self-improves and writes its own skills. Claude Code has an agent that exists only to help you code in a specific directory. OpenClaw has an agent that's more like an operating system — persistent, multi-channel, multi-subagent. These are genuinely different animals wearing the same word.

[NOVA]: Let's start with how each system is structured at the top level, because this shapes everything else.

[NOVA]: Starting with OpenClaw. If you look at ~/.openclaw/, you see the runtime structure. There's a gateway daemon that manages the overall system. Channels — Telegram, Discord, and so on — are plugins that connect to this gateway. The workspace files live in ~/.openclaw/workspace/, and subagents run as detached processes with their own context. The config is in openclaw.json. The skills system lives in ~/.openclaw/skills/, and memory is stored in ~/.openclaw/memory/. Critically, there's also ~/.openclaw/cron/ — OpenClaw has a built-in scheduling system, which tells you something important: this runtime is designed for a machine that needs to run tasks even when nobody is watching.

[ALLOY]: Right. OpenClaw is architected as a personal AI operating system. It's not just about a single agent loop. It's about persistent presence across messaging surfaces, scheduled background work, and subagent delegation. The openclaw gateway daemon is the kernel of this system. Everything else is a process.

[NOVA]: Now Claude Code — and this is going to be a shorter architecture discussion, because Claude Code is intentionally focused. You install it from npm: @anthropic-ai/claude-code, version 2.1.59 at time of recording. It's a CLI tool first. It has a sandboxing layer that we can see in its dependencies — there are modules for macOS Apple Sandbox profiles and Linux bwrap (bubblewrap) integration. The tool registry is in cli.js and related files. But the architecture is deliberately narrow: it wants to be the best tool for one job — helping a developer in a codebase directory.

[ALLOY]: Which is a completely legitimate design choice. Narrow and deep beats broad and shallow. But it means Claude Code's session model is different from the other two. It doesn't have a persistent session database. Each invocation is somewhat ephemeral, though it can maintain conversation state within a working directory. We'll get into what that means for memory.

[NOVA]: And then Hermes Agent from Nous Research. This one is the most explicitly architected as a research platform. The core orchestration engine is run_agent.py and its AIAgent class. The session store is a SQLite database at ~/.hermes/state.db running in WAL mode — so concurrent readers, one writer, which matters when the gateway and CLI are both hitting it. And it has FTS5 full-text search across all session messages via a virtual table.

[ALLOY]: That's actually a really significant architectural decision. FTS5 means you can search your entire conversation history, not just recent turns. If you're a researcher who runs long sessions across multiple topics, that's a meaningful feature. And the fact that they track token counts, billing, and model configurations per session tells you this was built with cost consciousness — both for the research lab and for users who are paying for API calls.

[NOVA]: Let's talk about the most important piece of any agent runtime: the turn cycle. How does each system handle a single exchange — user message in, model thinking, tool calls, response out?

[ALLOY]: Starting with Hermes, because it has the most documented loop. From the docs: run_conversation() is the main entry point. The turn lifecycle is:

[NOVA]: 1. Generate a task ID

[NOVA]: 2. Append the current user message

[NOVA]: 3. Load or build the cached system prompt

[NOVA]: 4. Maybe preflight-compress if the context is getting long

[NOVA]: 5. Build api_messages — the actual prompt payload

[NOVA]: 6. Inject ephemeral prompt layers

[NOVA]: 7. Apply prompt caching if appropriate

[NOVA]: 8. Make an interruptible API call

[NOVA]: 9. If tool calls: execute them, append results, loop back

[NOVA]: 10. If final text: persist, cleanup, return

[NOVA]: Step 8 — interruptible API calls. That's important. Hermes wraps its API requests so they can be cancelled from the CLI or the gateway. This matters because the agent might be in a long LLM call, and the user sends a new message mid-flight, or a background system needs to cancel. This is an explicit design concern, not an afterthought.

[ALLOY]: And look at the API modes Hermes supports. Three execution paths: chat_completions for OpenAI-compatible endpoints (including OpenRouter), codex_responses for the Codex and Responses API, and anthropic_messages for the native Anthropic Messages API. The mode is resolved from explicit arguments, provider selection, and base URL heuristics. So Hermes is genuinely model-agnostic — not as a marketing claim but as a routing architecture.

[NOVA]: Now Hermes's tool execution. Two modes: sequential for single or interactive tools, and concurrent for multiple non-interactive tools. And here's the clever part — concurrent execution preserves message and result ordering when reinserting tool responses into conversation history. That's a non-trivial constraint to get right.

[ALLOY]: For Claude Code, we don't have the exact source path to the loop file in the same way, but we can infer from the package structure. The npm package is at /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/. The key patterns to look for are in cli.js — how it handles tool calls, how it manages permission prompts, how it loops. The thing we know about Claude Code's loop is that it's designed around a specific use case: developer assistance in a local directory. It doesn't have subagent spawning as a first-class concept in the way OpenClaw does.

[NOVA]: And OpenClaw's agent loop is designed around the fact that it has multiple concurrent agents with a gateway managing the coordination. The loop isn't just about "user → agent → tools → response." It's about: user message arrives on channel X, subagent Y picks it up, subagent Y may spawn subagent Z, results come back, gateway dispatches to the right surface. The clawflow skill that orchestrates multi-agent workflows is evidence of this — it's designed for detached background tasks that still behave as one job.

[ALLOY]: OpenClaw's loop is the most complex of the three because it has the most coordination surface to manage. But complexity isn't always bad — it's appropriate complexity for what it's trying to do.

[NOVA]: This is where Hermes really distinguishes itself architecturally. Let's go deep on the SQLite schema.

[ALLOY]: ~/.hermes/state.db has four logical components: a sessions table, a messages table, an FTS5 virtual table called messages_fts, and a schema_version table. The sessions table is rich — it tracks not just session metadata but billing information: input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, actual_cost_usd, cost_status, pricing_version. If you're running a multi-model setup with different pricing from different providers, Hermes is tracking your costs per session.

[NOVA]: The messages table stores everything. role, content, tool_call_id, tool_calls as a JSON string, tool_name, token_count, finish_reason, reasoning, reasoning_details, and codex_reasoning_items. Note that reasoning is stored separately — this is for providers like Claude that expose thinking tokens. And there are three triggers keeping the FTS5 table in sync on INSERT, UPDATE, and DELETE.

[ALLOY]: The write contention handling is worth looking at. Hermes handles multiple processes — gateway plus CLI sessions plus worktree agents — all sharing one state.db. It uses a short SQLite timeout (1 second, not the default 30), application-level retries with random jitter between 20 and 150 milliseconds, up to 15 retries, and BEGIN IMMEDIATE transactions to surface lock contention early. It also does periodic WAL checkpoints every 50 writes in PASSIVE mode. This is thoughtful engineering — they're avoiding SQLite's convoy effect problem where competing writers retry at the same intervals.

[NOVA]: And session lineage via parent_session_id chains. When context compression triggers a session split — which happens when the context window gets full — the new session gets a new ID but chains back to the parent. You can query entire session lineages recursively. This is for long-running research or coding sessions where context compression happens mid-task.

[ALLOY]: Now compare that to Claude Code. Claude Code's session model is... lighter. It can maintain conversation context within a working directory, but it's not designed to be a long-term memory system. The sandbox is designed around filesystem permissions for a specific directory — not around persistent structured memory across sessions. This is a deliberate tradeoff: simplicity for the most common case (developer help in a codebase) versus rich session persistence.

[NOVA]: And OpenClaw's memory model. It uses workspace files for structured context — MEMORY.md for long-term curated memory, memory/YYYY-MM-DD.md for daily session logs. There's also an LCM — Lossless Context Management — system that compacts conversation history. And there's a skills system that acts as procedural memory. So it's a three-layer model: raw daily logs, curated long-term memory, and skills that encode reusable workflows.

[ALLOY]: The OpenClaw approach is more file-system-native and less database-native than Hermes. Hermes puts everything in SQLite because it's a single runtime that needs concurrent multi-process access and FTS5. OpenClaw uses the filesystem because it fits the Unix philosophy and makes the data universally accessible — you can grep it, back it up with rsync, put it in git.

[NOVA]: This is where Claude Code really shows its cards. Let's talk about how it handles dangerous actions.

[ALLOY]: Claude Code has a sandboxing system that targets two platforms explicitly: macOS and Linux. On macOS, it uses Apple Sandbox Profiles. On Linux, it uses bwrap — bubblewrap. The system is called SandboxLinux in the source, and there are classes like SandboxConfig, SandboxManager, and a ViolationStore that tracks sandbox violations with a total count and per-command history. The violations store has a max size of 100 entries and a total count that keeps incrementing even after the store is full.

[NOVA]: The sandbox config for Linux is defined in sandbox_linux.py. It starts with --new-session --die-with-parent. Then it builds up allowed and denied filesystem paths. The allowed paths start with a default allowlist — things like /dev/null, /dev/urandom, /dev/zero. Denied paths are things like /etc/ssh/ssh_config.d if it exists. For write paths, it has a denyWithinAllow concept — you can write to a directory but not to specific dangerous subpaths within it.

[ALLOY]: The Linux sandbox also has seccomp BPF filtering for Unix socket blocking. There's a bpfPath and an applyPath for the seccomp binary. If those aren't available, it falls back to allowing Unix sockets — but it warns that full protection isn't available. On macOS, there's a SandboxMonitor that watches for violations using the osascript command.

[NOVA]: Now compare that to Hermes's approach. Hermes has a DANGEROUS_PATTERNS list in tools/approval.py — regex patterns paired with descriptions covering recursive deletes, filesystem formatting commands like mkfs and dd, SQL destructive operations, system config overwrites, service manipulation, remote code execution via curl | sh, fork bombs. Before executing any terminal command, detect_dangerous_command() checks against all patterns.

[ALLOY]: If a match is found: in CLI mode, an interactive prompt asks the user to approve, deny, or allow permanently. In gateway mode, an async approval callback sends the request to the messaging platform — so if you're on Telegram or Discord, you get an approval message there. There's also a smart approval option where an auxiliary LLM can auto-approve low-risk commands that happen to match dangerous patterns — like rm -rf node_modules/ matching the recursive delete pattern.

[NOVA]: And Hermes has session-scoped approvals. Once you approve "recursive delete" for a session, subsequent rm -rf commands don't re-prompt. The permanent allowlist writes patterns to config.yaml's command_allowlist so they persist across sessions.

[ALLOY]: These are fundamentally different models. Claude Code's sandbox is about restricting the process's capabilities before anything bad can happen — the OS enforces it. Hermes's approval system is about detecting dangerous patterns and asking — the human enforces it. The Claude Code model is stronger against accidental damage. The Hermes model is more flexible for interactive use cases where the agent is running on a remote server and the user is approving via Telegram.

[NOVA]: OpenClaw's model combines elements of both. The exec tool has an approval system — there's exec-approvals.json in the config directory. And OpenClaw's subagent system has permission scoping — subagents run with specific workspace contexts and can't necessarily read or write everything the parent agent can. The gateway also has the concept of channel-specific permissions — what's allowed on Telegram might differ from what's allowed on Discord.

[NOVA]: Let's talk about how each system lets you extend it.

[ALLOY]: Starting with Hermes's skills system, because it's the most fully realized. Skills are on-demand knowledge documents the agent can load when needed. They follow the agentskills.io open standard, which means they're not locked to Hermes — they're portable. The skill format is SKILL.md with a YAML frontmatter declaring name, description, version, platforms, and metadata for activation conditions.

[NOVA]: The progressive disclosure pattern is clever. Level 0: skills_list() returns just name, description, and category — about 3k tokens. Level 1: skill_view(name) loads the full content. Level 2: skill_view(name, path) loads a specific reference file. The agent only pays the token cost when it actually needs the full skill.

[ALLOY]: Skills can be conditional. They can declare fallback_for_toolsets — so a DuckDuckGo search skill only shows up when the premium web search toolset is unavailable. Or requires_toolsets — a skill only shows when certain tools are present. And they can declare required environment variables without disappearing from discovery — if a key is missing, Hermes asks for it securely when the skill is loaded in CLI mode, but never prompts in messaging surfaces.

[NOVA]: Agent-created skills are a key differentiator. The skill_manage tool lets the agent create, update, and delete its own skills via a create/patch/edit/delete/write_file/remove_file action set. The docs specify the trigger conditions: after completing a complex task with 5+ tool calls, when hitting errors and finding the working path, when the user corrects its approach, when it discovers a non-trivial workflow. This is the procedural memory layer — the agent isn't just doing work, it's learning how to do work.

[ALLOY]: Hermes has a full skill marketplace integration. It connects to the official optional skills catalog, skills.sh (Vercel's public directory), well-known skill endpoints via the /.well-known/skills/ convention, direct GitHub repos, ClawHub, and Claude marketplace repos. You can publish skills to GitHub directly. You can add custom GitHub taps. This is a genuinely open ecosystem play — Hermes is not trying to own the skill supply chain.

[NOVA]: And Hermes supports external skill directories. You can point it at ~/.agents/skills/ or /home/shared/team-skills/ via ${VAR} environment variable expansion. Those directories are read-only for discovery — the agent always writes new skills to ~/.hermes/skills/. But external skills appear in the system prompt index and as slash commands, indistinguishable from local skills.

[ALLOY]: Now OpenClaw's skills system. Looking at ~/.openclaw/skills/, it's also YAML frontmatter + markdown body, and the hermes claw migrate tool suggests cross-compatibility is intentional. OpenClaw skills are workspace-contextual — they live alongside the project they're relevant to. The skill system is integrated with the subagent system, so you can have skills that describe how to spawn the right subagent for a given task.

[NOVA]: And OpenClaw supports MCP — Model Context Protocol — as an extensibility mechanism. The openclaw.json config has a plugins section and an extensions section. MCP servers can be configured to give the agent tools from external services.

[ALLOY]: Claude Code has a more focused extension model. The npm package structure suggests it's designed to work well with existing developer tooling rather than having its own plugin marketplace. The skill system in Claude Code is lighter — slash commands, essentially. But that's appropriate for a focused CLI tool.

[NOVA]: We have to talk about hermes claw migrate. This is an explicit migration tool that ships with Hermes to import OpenClaw skills and workspace configurations. That is a significant signal.

[ALLOY]: It absolutely is. Hermes ships with a tool called hermes claw migrate that says: we know OpenClaw has a skills system worth borrowing from. We're going to import it. That is not the move of a project that thinks it's in a different category. That's the move of a project that thinks it's directly competing and that the skills ecosystem is worth cross-pollinating.

[NOVA]: The fact that it's hermes claw migrate and not claw migrate tells you something about the directional relationship. OpenClaw came first — Hermes is migrating from it. But Hermes is doing this explicitly, which means the Nous Research team looked at OpenClaw's skill system and workspace model and decided: we want that in our ecosystem, and we want to make it easy for OpenClaw users to try Hermes.

[ALLOY]: And Hermes's model-agnostic architecture makes this migration credible. If you've been using OpenClaw with Claude as your backend, you can switch to Hermes and use the same skills. The skill format is open — SKILL.md with YAML frontmatter following the agentskills.io spec. It's not a proprietary lock-in format.

[NOVA]: This is the kind of thing that only happens when an open ecosystem starts maturing. OpenAI had Actions and Plugins. Anthropic has MCP. And now Hermes has a migration tool for OpenClaw skills. The skills portability story is becoming a genuine competitive dimension.

[ALLOY]: And OpenClaw's response to this is probably... nothing needs to change. The fact that Hermes is migrating from OpenClaw means OpenClaw's model is the reference. OpenClaw doesn't need to migrate to Hermes. But OpenClaw should watch how Hermes's skill ecosystem evolves — if Hermes builds a richer marketplace, that could become a reason for users to evaluate it.

[NOVA]: Let me give you some specific class names and file names to ground this discussion.

[ALLOY]: From Hermes:

[NOVA]: - Core agent: run_agent.py — AIAgent class

[NOVA]: - State management: hermes_state.py — SessionDB class

[NOVA]: - Tool registry: tools/registry.py — ToolRegistry singleton, ToolEntry objects

[NOVA]: - Tool discovery: model_tools.py — _discover_tools() function

[NOVA]: - Tool dispatch: registry.dispatch(name, args, kwargs) — routes to the right handler

[NOVA]: - Approval system: tools/approval.py — DANGEROUS_PATTERNS, detect_dangerous_command()

[NOVA]: - Context compression: agent/context_compressor.py

[NOVA]: - Prompt building: agent/prompt_builder.py

[NOVA]: - Prompt caching: agent/prompt_caching.py

[NOVA]: - Session DB path: ~/.hermes/state.db

[NOVA]: - Skill directory: ~/.hermes/skills/

[NOVA]: - Config: ~/.hermes/config.yaml

[NOVA]: The tool discovery in Hermes is interesting. _discover_tools() imports modules in a fixed order, and each module calls registry.register() at module level. The module list includes web_tools, terminal_tool, file_tools, vision_tools, mixture_of_agents_tool, image_generation_tool, skills_tool, browser_tool, cronjob_tools, rl_training_tool, tts_tool, todo_tool, memory_tool, session_search_tool, clarify_tool, code_execution_tool, delegate_tool, process_registry, send_message_tool, honcho_tools, homeassistant_tool. That's a very comprehensive list — Hermes is not a narrow tool.

[ALLOY]: And mixture_of_agents_tool plus rl_training_tool plus delegate_tool tells you Hermes is designed as a research platform. These are not consumer features. mixture_of_agents suggests ensemble methods, rl_training suggests reinforcement learning from feedback, delegate_task suggests subagent spawning. This is a system designed for researchers who want to experiment with agentic RL.

[NOVA]: For Claude Code, the package is at /opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/. The sandbox system has classes like SandboxLinux, SandboxConfig, SandboxManager, ViolationStore. The permission system has policySettings, userSettings, projectSettings, localSettings — layered permission sources with rules for allow, deny, and ask. The tool registry uses alwaysAllowRules, alwaysDenyRules, alwaysAskRules — so there's a three-tier permission model: always allow, always deny, always ask.

[ALLOY]: For OpenClaw, the gateway daemon, cron scheduling, subagent orchestration, and channel plugins (Discord, Telegram) all live under ~/.openclaw/. The workspace structure is project-relative. Skills live in ~/.openclaw/skills/. The LCM system for context compaction is in the runtime. The clawflow skill manages multi-agent workflows.

[NOVA]: Okay. We've been thorough. Let's give the verdict.

[ALLOY]: Use Hermes Agent if: you're a researcher or power user who wants a self-improving agent with genuine long-term memory across sessions, model-agnostic flexibility, FTS5 search across your entire conversation history, a rich skill ecosystem that you're contributing to and drawing from, and the ability to run on Telegram, Discord, Slack, WhatsApp, or Signal from a single gateway. Hermes is also the right choice if you're interested in RL-based agent improvement — the Atropos RL environments and trajectory compression suggest a research-forward design. And if you're already an OpenClaw user, Hermes's hermes claw migrate means you can bring your skills with you.

[NOVA]: Use Claude Code if: you're a developer who wants the best possible help in a specific codebase, running locally, with the strongest OS-level sandboxing for dangerous operations. Claude Code's bubblewrap and Apple Sandbox integration is the most rigorous sandbox implementation of the three. If your workflow is "I'm in a directory, I need help, I trust the agent to edit files here," Claude Code is the most focused tool for that job. The trade-off is session persistence and multi-channel presence — it's not designed for that.

[ALLOY]: Use OpenClaw if you want a persistent personal AI that lives on your machine (or a VPS), connects to multiple messaging channels simultaneously, runs scheduled tasks, spawns subagents for background work, and has a skill system that's yours to shape. OpenClaw is the most Unix-native of the three — it fits naturally into a command-line workflow, it works with existing dotfile and workspace conventions, and it's designed to be your AI operating system rather than a single tool. The fact that Hermes ships a migration tool from OpenClaw tells you the OpenClaw skill model is the reference.

[NOVA]: The deeper point is that these three systems encode three different theories of what an AI agent should be. Hermes thinks an agent should be a persistent, self-improving research companion with rich memory and model flexibility. Claude Code thinks an agent should be a narrow, deeply integrated development tool with strong safety guarantees. OpenClaw thinks an agent should be a personal AI OS — always on, multi-surface, multi-agent.

[ALLOY]: None of those theories is wrong. They're different bets on where the space is going. The next few years will tell us which one was right.



[NOVA]: One last thing before we close — a lot of you are going to want to try Hermes after this. So let's talk models. Hermes is genuinely model-agnostic, but the docs are specific about what works best.

[ALLOY]: Their recommended starting point is Claude Sonnet via Anthropic OAuth — and here's the clever part: if you already use Claude Code, Hermes automatically reads Claude Code's credential store. No separate API key setup. You run hermes model, pick Anthropic, and it just works with your existing subscription.

[NOVA]: For free options, Hermes has first-class GitHub Copilot support. If you have a Copilot subscription, you get access to GPT-5.4, Claude, and Gemini through the Copilot API. GPT-5 and higher automatically route through the Responses API; everything else uses Chat Completions.

[ALLOY]: The most interesting free path is OpenRouter. Set an OPENROUTER API KEY in your dot env file, run hermes model, and you have access to 200-plus models. The Hermes docs specifically call out that some built-in tools — vision, web summarization, and the mixture of agents tool — use a separate auxiliary model that defaults to Gemini Flash via OpenRouter. So even if you're using Claude as your primary, an OpenRouter key unlocks those tools automatically.

[NOVA]: For local models, Hermes supports any Ollama or vLLM endpoint — same config, just point OPENAI BASE URL at your local server. And for Chinese providers specifically: Z-dot-AI GLM, Kimi slash Moonshot, MiniMax, and Alibaba Cloud Qwen all have first-class provider IDs. Not an afterthought — they're in the core provider list alongside Anthropic and OpenAI.

[ALLOY]: The practical answer for most people: if you have Claude Pro or Max, start with Anthropic OAuth. If you want free with strong capability, GitHub Copilot with GPT-5.4. If you want maximum flexibility and don't mind a small API bill, OpenRouter with Claude Sonnet or Qwen 3.

[NOVA]: That's EP021: Inside the Loop. Full show notes and links are at Toby On Fitness Tech dot com slash podcasts slash episode 21. I'm NOVA.

[ALLOY]: And I'm ALLOY. We'll be back soon.