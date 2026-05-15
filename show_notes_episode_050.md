# AgentStack Daily EP050 — What's New in Agent Releases: Hermes Tenacity, Claude Code Agent View, ADK Resume, and Copilot Tasks

## Release Coverage Check

- OpenClaw lane: OpenClaw is the runtime baseline for this episode: channel handling, tools, browser actions, local commands, media, memory, background jobs, and proof-of-work reporting. The release spotlight is Hermes Agent plus Claude Code.
- Hermes Agent lane: primary source `https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=10`; latest stable/verified version: v2026.5.7. Selected release coverage: v2026.5.7.
- OpenAI Codex lane: primary source `https://api.github.com/repos/openai/codex/releases?per_page=10`; latest stable/verified version checked: rust-v0.130.0; no new Codex release selected for this episode.
- Claude Code CLI lane: primary sources `https://registry.npmjs.org/@anthropic-ai/claude-code/latest`, `https://code.claude.com/docs/en/changelog`, and `https://github.com/anthropics/claude-code/releases`; latest stable/verified version: v2.1.141 / npm 2.1.141. Selected release coverage: v2.1.141 through v2.1.129.
- Outside update lane: Google ADK long-running agents tutorial and GitHub Copilot agent-task REST API public preview.

## Episode Title

AgentStack Daily EP050 — What's New in Agent Releases

## Tagline

Hermes v2026.5.7, Claude Code v2.1.141, Google ADK resume mechanics, and GitHub Copilot cloud agent tasks headline a feature-first agent tooling update.

## Feed Description

This AgentStack Daily episode covers what is new in LLM and agent tooling: Hermes Agent v2026.5.7 adds durable boards, worker health checks, checkpoint pruning, gateway resume, no-agent cron, provider plugins, platform allowlists, and MCP fixes; Claude Code v2.1.141 through v2.1.129 adds the agent view, hook JSON updates, plugin and workload-identity controls, MCP repairs, and background-agent permission fixes; Google ADK documents pause-and-resume agents with persisted state; and GitHub exposes Copilot agent tasks through REST endpoints.

## Story Slate

### 1. **Release readout: Hermes Agent v2026.5.7 and Claude Code v2.1.141 add the week's most useful agent-operator features**
Hermes v2026.5.7 leads the episode with multi-agent Kanban updates, `/goal`, Checkpoints v2, gateway auto-resume, deterministic cron support, provider plugins, platform allowlists, role policies, MCP repairs, and security defaults. Claude Code v2.1.141 through v2.1.129 adds the `claude agents` view, project-scoped `--cwd` filtering, hook output contracts, plugin source controls, workload identity scoping, MCP reconnect behavior, background-agent permission fixes, and plan-mode safety.

Technical depth angle: compare the actual changed surfaces — commands, release notes, runtime behavior, checkpoint semantics, platform policy, MCP transport reliability, hook JSON contracts, permission inheritance, and upgrade tests.

Primary links:
- https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.7
- https://github.com/anthropics/claude-code/releases/tag/v2.1.141
- https://code.claude.com/docs/en/changelog
- https://registry.npmjs.org/@anthropic-ai/claude-code/latest

### 2. **Google ADK: pause-and-resume agents get a practical state model**
Google's May 12 ADK tutorial shows how to persist `current_step`, write progress through `ToolContext.state`, back sessions with SQLite or Cloud SQL, resume from webhooks, and test delayed continuation. The update matters because long-running agents need explicit state, not just a long transcript.

Technical depth angle: explain the ADK session-service model, state writes through tools, instruction interpolation, webhook wakeups, database-backed resume, and how this changes reliability for agents that wait on approvals or external events.

Primary link: https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/

### 3. **GitHub Copilot agent tasks: cloud coding work becomes a REST-addressable feature**
GitHub's agent-task endpoints let teams start Copilot coding tasks, choose a model, create a branch or pull request, inspect task state, and gate the result through normal repository review. The feature turns Copilot agent work into an API-managed repository object instead of a one-off chat interaction.

Technical depth angle: cover the REST request/response contract, task lifecycle states, model choice, branch and pull-request artifacts, token/scope constraints, CI/review gating, and failure modes for cloud-hosted coding tasks.

Primary link: https://docs.github.com/rest/agent-tasks/agent-tasks?apiVersion=2026-03-10#start-a-task

## Extra Research Candidates

- **OpenAI Codex rust-v0.130.0 release checks** — Primary link: https://github.com/openai/codex/releases
  Technical depth angle: verify whether Codex release deltas should return in a later episode by comparing tag history, CLI/runtime behavior, sandbox defaults, model routing, and repository-task ergonomics.
- **Anthropic Claude Code changelog follow-up** — Primary link: https://code.claude.com/docs/en/changelog
  Technical depth angle: monitor new hook, MCP, plugin, and permission-mode changes after v2.1.141, with attention to command behavior and project-level managed settings.
- **GitHub Copilot coding agent docs** — Primary link: https://docs.github.com/en/copilot
  Technical depth angle: track how Copilot coding agent tasks connect to pull requests, branch policy, enterprise permissions, model selection, CI checks, and API availability.

## Show Notes

```md
AgentStack Daily EP050 opens with the current agent-tooling stack in plain English, then moves into the week's release spotlight: Hermes Agent v2026.5.7 and Claude Code v2.1.141 through v2.1.129. OpenClaw is the runtime baseline in the episode, while Hermes and Claude Code carry the fresh release headlines. The goal is straightforward: what changed, what was added, why it matters, and what to test after upgrading.

[00:00] Opening — What's new in the agent stack
NOVA and ALLOY introduce the week's agent and LLM tooling updates. The headline changes are Hermes board durability, worker visibility, checkpoint pruning, gateway resume, deterministic cron, provider plugins, platform policy, MCP transport fixes, Claude Code agent visibility, richer hook output, plugin controls, workload identity scoping, MCP repairs, and background-agent permission fixes. OpenClaw remains the operator runtime in the story, while Hermes and Claude Code carry the fresh release headlines today.

[02:30] Release readout — Hermes Agent v2026.5.7
Before the release details, the episode defines the major tools in practical language. OpenClaw is the operator/runtime/channel/tool/browser/media/proof layer. Hermes is the multi-agent board for delegation, durability, task state, and worker health. Claude Code is the terminal-local coding agent with hooks, MCP, project settings, and background agents. Codex is the repo-focused coding, patch, and review lane. Google ADK is an app framework for long-running agents that need persisted state and pause/resume behavior. GitHub Copilot agent tasks are GitHub-hosted async coding tasks exposed through API, branch, status, and pull-request surfaces.

Hermes v2026.5.7 is the main release block. The concrete additions include multi-agent Kanban improvements, worker heartbeats, stale-task reclaim, Darwin zombie detection, `/goal`, Checkpoints v2, checkpoint pruning, disk guardrails, gateway auto-resume, source reload behavior, `no_agent` cron mode, provider plugins, OAuth/SSE/MCP repairs, WhatsApp stranger rejection, platform allowlists, guild-scoped Discord role policy, and safer redaction defaults. Treat each item as a product delta. Kanban plus ownership means the board can show who has a task rather than burying status inside a transcript. Heartbeats and stale reclaim mean a vanished worker becomes a detectable condition. Darwin zombie detection closes a local reliability gap on macOS. `/goal` gives a run a named target. Checkpoint pruning and disk guardrails reduce persistence clutter. Gateway auto-resume makes restarts less destructive. `no_agent` cron lets deterministic checks run without a model. Provider plugins make integration less hard-coded. MCP fixes around OAuth, SSE, keepalives, stale pipes, image results, and reconnects make tool calls less brittle. Platform allowlists, WhatsApp stranger rejection, Discord role scope, and redaction defaults tighten who can trigger work and what data leaks. The practical takeaway is a release test list: board state, worker health, resume, cron, plugin loading, MCP transport, and channel policy. Also mention the migration shape. After upgrading, the useful questions are concrete: does a running board show live ownership, does a dead worker get reclaimed, does a checkpoint resume with the latest task state, does pruning keep disk use bounded, does a gateway restart preserve user-visible work, does a script-only cron produce the expected notification, do provider plugins load cleanly, do MCP tools reconnect after auth refresh or transport interruption, and do channel allowlists block the wrong sender. That keeps the segment focused on new features and verification.

[19:00] Release readout — Claude Code v2.1.141 through v2.1.129
Claude Code's recent versions add visible agent management and cleaner extension surfaces. The biggest listener-facing item is `claude agents`, plus project filtering through `claude agents --cwd`. Hooks gain JSON output fields such as `terminalSequence`, direct `args`, and better continuation behavior around blocked tool use. Plugin source controls, HTTPS source cloning, managed-setting migration, `CLAUDE_PROJECT_DIR`, `ANTHROPIC_WORKSPACE_ID`, workload identity scoping, MCP server preservation after clear, concurrent OAuth refresh improvements, and background-agent permission inheritance all point to a tool that is becoming easier to operate in real projects. The practical test list is simple: can you see running and blocked agents, do hooks still enforce policy, do MCP servers survive expected lifecycle events, do plugin controls behave as configured, and do background agents inherit the intended permission mode?

[29:00] Google ADK update — persisted state for pause-and-resume agents
The Google ADK item is a feature update about state. The tutorial shows a long-running agent using `current_step`, `ToolContext.state`, a session service, SQLite for local development, Cloud SQL for more durable deployments, and external wakeups such as webhooks. The significance is that an agent can pause for approval, payment, customer input, or another external signal and resume from explicit state instead of relying on a huge replayed transcript. The episode should cover the mechanism: tools write state, instructions can interpolate state, a database-backed session service keeps the important fields, and the app can test whether the next action is safe.

[39:00] GitHub Copilot agent tasks — coding work gets an API surface
GitHub's Copilot agent-task REST API public preview turns cloud coding tasks into addressable objects. The docs show task creation, model choice, repository context, branch or pull-request output, task status inspection, and a lifecycle that can be gated by normal repository review. The important change is not that Copilot can write code; it is that Copilot coding work can be started, tracked, and reviewed through a platform API. Mention the constraints: API versioning, authentication and token scope, enterprise or repository policy, status states, branch artifacts, CI checks, and human review before merge.

[47:00] Close — what to test next
The takeaway is a concise test checklist. For Hermes, test worker health, stale reclaim, checkpoints, gateway resume, cron mode, platform allowlists, redaction, and MCP reconnects. For Claude Code, test `claude agents`, `--cwd`, hooks, plugin policy, workload identity, MCP lifecycle, and background-agent permissions. For ADK, test persisted state after a delay. For Copilot tasks, test task creation, status polling, pull-request creation, and CI/review gating. These are the new surfaces worth checking this week.
```

## Chapters

- 00:00 — What's new in the agent stack
- 02:30 — Tool map and Hermes Agent v2026.5.7 release readout
- 19:00 — Claude Code v2.1.141 through v2.1.129 release readout
- 29:00 — Google ADK pause-and-resume state model
- 39:00 — GitHub Copilot agent-task REST API
- 47:00 — Upgrade tests and closing takeaways
