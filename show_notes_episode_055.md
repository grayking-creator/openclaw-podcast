# AgentStack Daily EP055 - Codex 0.132.0, Claude Code 2.1.145, Gemini Managed Agents, and WebMCP

## Release Coverage Check

- **OpenClaw** - Latest stable/verified version: `2026.5.18` from `https://api.github.com/repos/openclaw/openclaw/releases?per_page=10` with prereleases skipped. Recent episode version tags detected: `2026.5.12`, `2026.5.18`, plus earlier `2026.5.x` tags in the recent tag scan. Selected missing versions: none. Candidate verification: the latest stable release is present in the recent tag scan, so this lane stops there.
- **Hermes Agent** - Latest stable/verified version: `2026.5.16` / Hermes Agent 0.14.0 from `https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=10` with prereleases skipped. Recent episode version tags detected: `2026.5.7`, `2026.5.16`. Selected missing versions: none. Candidate verification: the latest stable release is present in the recent tag scan, so this lane stops there.
- **OpenAI Codex app/CLI** - Latest stable/verified version: `rust-v0.132.0` / Codex CLI 0.132.0 from `https://api.github.com/repos/openai/codex/releases?per_page=10` with prereleases skipped and the OpenAI Codex changelog verified at `https://developers.openai.com/codex/changelog`. Recent episode version tags detected: `rust-v0.130.0`, `rust-v0.131.0`. Selected missing versions: `rust-v0.132.0`. Candidate verification: the latest contiguous uncovered block starts at `rust-v0.132.0` and stops at `rust-v0.131.0`, which is present in the recent tag scan.
- **Claude Code CLI** - Latest verified npm package version: `2.1.145` from `npm view @anthropic-ai/claude-code version`; concrete changes verified from Anthropic's Claude Code GitHub release feed and changelog at `https://code.claude.com/docs/en/changelog`. Recent episode version tags detected: `2.1.141`, `2.1.142`, `2.1.143`, `2.1.144`. Selected missing versions: `2.1.145`. Candidate verification: the latest contiguous uncovered block starts at `2.1.145` and stops at `2.1.144`, which is present in the recent tag scan.
- **Agent-stack release story** - Included. Release coverage leads the episode and includes Codex CLI 0.132.0 plus Claude Code CLI 2.1.145.

## Episode Title

Codex 0.132.0, Claude Code 2.1.145, Gemini Managed Agents, and WebMCP

## Tagline

Codex gets real Python SDK auth and schema-locked resume, Claude Code exposes live agents as JSON, Google ships managed sandboxed agents, Chrome starts standardizing browser tool calls, AI Studio pushes app building into Workspace and Android, DevTools gives coding agents a browser verifier, and GitHub moves Copilot Business onto GPT-5.3-Codex.

## Feed Description

AgentStack Daily EP055 opens with the operator release readout: Codex CLI 0.132.0 adds first-class Python SDK authentication, simpler text turns, richer turn results, schema-constrained `codex exec resume`, faster TUI startup, auth-backed remote executor registration, image-fidelity preservation, goal-loop brakes, multi-session MCP replay fixes, remote websocket keepalives, and Windows install hardening. Claude Code CLI 2.1.145 adds `claude agents --json`, agent IDs in OpenTelemetry spans, GitHub repository and pull-request status in status-line JSON, richer plugin discovery before install, awaiting-input counts in terminal titles, hook payloads for background tasks and session crons, and several permission, MCP, terminal, review, plugin, and skill-loop fixes. Then the episode covers six concrete AgentStack topics: Google Gemini 3.5 Flash GA and Managed Agents, Chrome WebMCP, Google AI Studio's Workspace and Android build updates, Chrome DevTools for agents, and GitHub making GPT-5.3-Codex the base model for Copilot Business and Enterprise.

## Story Slate

### 1. **Agent-stack release readout: Codex CLI 0.132.0 and Claude Code 2.1.145 tighten automation, observability, and live-session control**
Codex 0.132.0 moves the CLI and SDK closer to scriptable production automation: Python clients can log in with API keys, ChatGPT browser/device-code flows, inspect accounts, and log out; text-only turn calls can pass a plain string; handle-based runs return `TurnResult` with collected items, timing, and usage; `codex exec resume --output-schema` lets resumed automations keep session context while enforcing JSON output; and remote sessions get websocket keepalives and repo-relative diffs. Claude Code 2.1.145 adds `claude agents --json` for scripting live session inventories, emits `agent_id` and `parent_agent_id` into `claude_code.tool` spans, enriches status-line JSON with GitHub repo and PR information, previews plugin commands/agents/skills/hooks/MCP/LSP servers before install, and fixes a Bash environment-variable permission bypass.

Technical depth angle: explain auth flows and account state in the Codex Python SDK, `TurnResult` request/response semantics, schema enforcement for resumed CLI automations, websocket keepalive behavior, image-fidelity propagation through app-server turns, Claude Code's JSON live-agent inventory contract, OTEL trace parenting for background subagents, status-line JSON fields, plugin component discovery, hook payload changes, and the permission boundary around shell environment assignments.

Primary links:
- https://github.com/openai/codex/releases/tag/rust-v0.132.0
- https://developers.openai.com/codex/changelog
- https://github.com/anthropics/claude-code/releases/tag/v2.1.145
- https://code.claude.com/docs/en/changelog
- https://www.npmjs.com/package/@anthropic-ai/claude-code

### 2. **Google ships Gemini 3.5 Flash GA and Managed Agents in the Gemini API**
Google's May 19 developer updates put `gemini-3.5-flash` into GA and introduce Managed Agents in the Gemini API: a single API call provisions an Antigravity-harness agent that can reason, use tools, execute code in an isolated Linux environment, and resume interactions with files and state intact. The builder impact is concrete: hosted agent execution becomes an API surface instead of a pile of sandbox, runner, and persistence glue.

Technical depth angle: explain the Interactions API as the managed-agent control plane, persistent isolated environments, follow-up calls that retain files and state, custom instructions and markdown skills, the Antigravity harness relationship, cost/latency placement around Gemini 3.5 Flash, and the operational boundary between managed Google-hosted agents and self-hosted agent harnesses.

Primary links:
- https://ai.google.dev/gemini-api/docs/changelog
- https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights
- https://developers.googleblog.com/all-the-news-from-the-google-io-2026-developer-keynote/

### 3. **Chrome WebMCP gives browser agents an explicit tool contract**
Chrome's WebMCP proposal exposes structured tools from web pages through JavaScript and annotated HTML forms, with JSON Schemas for inputs and outputs, visible execution in the user's page context, page state awareness, and a `tools` Permissions Policy. That changes browser-agent reliability because the agent no longer has to infer every form field, button, and multi-step flow from pixels and accessibility labels alone.

Technical depth angle: explain declarative versus imperative WebMCP APIs, tool discovery, JSON Schema contracts, page-state sharing, visible browser-context execution, sensitive-action confirmation patterns, the same-origin default for the `tools` Permissions Policy, cross-origin iframe opt-in with `allow="tools"`, origin-trial timing in Chrome 149, inspector-extension testing, and the limitation that tools require an open browser tab or webview rather than headless invocation.

Primary link: https://developer.chrome.com/docs/ai/webmcp

### 4. **Google AI Studio turns Workspace apps, Antigravity export, and Android generation into one build loop**
Google AI Studio's I/O update adds Workspace API integration for generated apps, export into Antigravity, a mobile build mode, native Android app generation, an in-browser Android emulator, ADB-based device flows, and Play Internal Test Track publishing. The practical change is continuity: a prototype can start in AI Studio, call Workspace data, move into Antigravity for agentic coding, and land on Android without treating each step as a separate product.

Technical depth angle: explain project-state export from AI Studio into Antigravity, Workspace API access from generated apps, in-browser Android emulator and ADB flows, Play Internal Test Track publishing, and how mobile-to-desktop build continuity changes prototyping workflows.

Primary link: https://blog.google/innovation-and-ai/technology/developers-tools/google-ai-studio-io-2026

### 5. **Chrome DevTools for agents gives coding agents a browser verification lane**
Chrome's DevTools-for-agents material exposes browser verification, emulation, and Lighthouse workflows to coding agents through a managed browser handoff. That matters because coding agents are weakest when they stop at code edits and never inspect the real page state, responsive layout, geolocation behavior, console output, network failures, or performance/accessibility regressions.

Technical depth angle: explain managed browser handoff, responsive and geolocation emulation, active Chrome-session debugging, Lighthouse audit automation, setup handshake, and the difference between browser debugging tools and page-declared WebMCP tools.

Primary link: https://developer.chrome.com/docs/devtools/agents

### 6. **GitHub makes GPT-5.3-Codex the base model for Copilot Business and Enterprise**
GitHub is making GPT-5.3-Codex the base model for Copilot Business and Enterprise, with model approval gates, long-term-support availability through February 4, 2027, premium request multipliers, and GPT-4.1 deprecation timing. For teams, this is not just a model swap. It changes the default fallback behavior, governance surface, and cost planning for enterprise coding-agent usage.

Technical depth angle: explain base-model fallback policy, model approval gates, long-term-support availability through February 4, 2027, premium request multipliers, GPT-4.1 deprecation timing, and how enterprise model governance changes agent reliability and cost planning.

Primary link: https://github.blog/changelog/2026-05-17-gpt-5-3-codex-is-now-the-base-model-for-copilot-business-and-enterprise/

## Extra Research Candidates

None. The three viable candidates above are promoted into the six-topic slate for this draft.

## Show Notes

```md
Codex 0.132 and Claude Code 2.1 lead today's AgentStack Daily because they move concrete operator surfaces: SDK authentication, resumed automation schemas, live-agent JSON, trace IDs, plugin previews, and permission hardening.

[00:00] Opening - start with the changed operator surfaces
NOVA and ALLOY open on the practical changes. Codex now has first-class Python SDK authentication and easier turn APIs, while Claude Code exposes live session state as JSON and adds agent lineage to traces. This is not just a version-number update. It changes how builders script coding agents, resume automations, observe background work, and catch unsafe shell behavior before it becomes an incident.

[02:30] Release readout - Codex 0.132
This Codex release's biggest API change is the Python SDK auth surface. A Python client can now handle API-key login, ChatGPT browser login, device-code flows, account inspection, and logout without outsourcing auth state to a CLI wrapper. That matters for notebooks, CI jobs, internal tools, and hosted developer portals that need to start Codex turns as a real programmatic workflow rather than screen-scraping terminal behavior.

The turn API also gets easier for small automations. Text-only turns can pass a plain string, and handle-based runs now return a richer `TurnResult` with collected items, timing, and usage. That gives agent orchestration code a better return object: what happened, how long it took, what it cost, and what artifacts came back. The practical recipe is straightforward: use the Python SDK for controlled tool entry points, keep the CLI for local repo work, and capture `TurnResult` when you need telemetry or a downstream decision.

The `codex exec resume --output-schema` change is the one to call out for durable workflows. Resuming a session keeps the context that made the agent useful, but the output can still be constrained to a schema. That is the missing bridge for automations that need both memory and machine-readable output: issue triage, migration status, test-result summarization, or a nightly code-health report can resume the same thread and still return validated JSON.

Codex also tightens remote and app-server behavior. Remote executor registration can use standard Codex auth instead of a separate registry credential path. Remote sessions keep websocket connections alive and show repo-relative diff paths again, which makes long-running remote work less likely to look dead or produce unreadable patches. App-server turns preserve requested image fidelity, including original-resolution local images, across user inputs and image-producing tools. That is useful when an agent is inspecting screenshots, UI regressions, diagrams, or generated visual artifacts where low-resolution context changes the answer.

The risk notes are operational. Goal continuations now stop when they hit usage limits or repeated blockers, so agents should burn fewer tokens in a stuck loop. Multi-session TUI replay keeps in-progress MCP calls marked active, and elicitation replies go back to the thread that requested them, which reduces cross-thread confusion. Windows installs get `codex doctor` npm-install detection and MSVC binaries that do not require separate VC++ runtime DLLs. Upgrade tests should cover Python login/logout, a text-only turn, `TurnResult` fields, a schema-constrained resume, remote websocket stability, image-detail preservation, and Windows doctor output if that platform matters.

[17:00] Release readout - Claude Code 2.1
This Claude Code update is smaller than the previous patch, but it lands exactly where operators need it: live inventory, traceability, plugin inspection, and shell safety. `claude agents --json` turns the agent view into a scriptable interface. Status bars, tmux-resurrect flows, session pickers, dashboards, and watchdogs can now query live Claude sessions without parsing terminal UI. The terminal tab title also shows the awaiting-input count, so a background agent that needs human attention is visible outside the TUI.

The tracing update is important for teams running background subagents. `claude_code.tool` OpenTelemetry spans now include `agent_id` and `parent_agent_id`, and trace parenting is fixed so background subagent spans nest under the Agent tool span that dispatched them. That gives observability systems a real lineage tree: main session, dispatched agent, nested tool calls, outcome. It is the difference between "Claude used a tool" and "this specific background worker did the slow thing after this parent turn."

Status-line JSON now includes GitHub repository and PR information when detected. That makes local prompts, terminal status lines, and external monitoring more useful during PR work: the agent can expose which repo and pull request it is operating inside without a separate `gh` probe every time. The `/plugin` Discover and Browse screens now show a plugin's commands, agents, skills, hooks, and MCP/LSP servers before installation. That is a security and ergonomics improvement: builders can inspect what a plugin contributes before bringing it into the runtime.

The permission fix deserves explicit airtime. Claude Code fixed a bypass where bare variable assignments to non-allowlisted environment variables in Bash commands were auto-approved. Shell approval systems often focus on command names, but environment variables can redirect tools, leak data, change auth behavior, or alter execution paths. After upgrading, test an allowlist policy with a harmless non-allowlisted variable assignment and confirm it prompts instead of silently approving.

Other fixes smooth daily use: MCP prompt slash commands now show missing-argument usage instead of raw server validation errors; resize/refocus no longer freezes the spinner and elapsed time; Windows PowerShell resume hints use the right command separator; voice push-to-talk works in the agent view reply pane; task lists render in stable order; non-ASCII Agent Teams names no longer poison API headers; `/review` drops a deprecated Classic Projects GraphQL query; plugin validation catches file paths under `skills:`; Read returns a truncated partial view instead of hard-failing on whole-file token overflow; and forked skills stop infinite self-reinvocation loops.

[29:00] Google Gemini - Gemini 3.5 Flash GA and Managed Agents
Google's May 19 Gemini API update releases `gemini-3.5-flash` as the GA Gemini 3.5 Flash model and introduces Managed Agents in the Gemini API. The useful part for builders is not just the model name. Managed Agents turns hosted agent execution into an API surface: one call provisions an agent powered by the Antigravity harness, gives it an isolated Linux environment, lets it use tools and execute code, and allows follow-up interactions to resume with files and state intact.

That changes the build-vs-buy line for agent infrastructure. If your agent needs code execution, file state, and multi-turn continuity, you no longer have to start by wiring your own sandbox pool, persistence layer, and harness protocol. You can use the Interactions API as the control plane, customize the agent with instructions and markdown skills, and decide later whether a workload belongs in a managed environment or a self-hosted harness.

The tradeoff is control. Managed agents reduce infrastructure friction, but the execution boundary is Google's hosted environment. Self-hosting through an SDK or local agent runner keeps more control over network, filesystem, policy, secrets, and observability. The practical guidance: use Managed Agents for prototypes, bounded tool tasks, and workloads where a hosted isolated Linux environment is acceptable; use self-hosted harnesses when the agent needs private network reachability, custom sandbox rules, or deep local tool integration.

Gemini 3.5 Flash matters because agent runtimes are latency-sensitive. A model that is fast enough for repeated tool-planning loops and strong enough for coding tasks changes how much work you can put into a single managed interaction before the operator experience feels slow. Watch the cost and latency tiers, tool-call behavior, state persistence semantics, and how well follow-up calls preserve working files without hiding too much of the execution trace.

[39:30] Chrome WebMCP - browser-agent tools become explicit
WebMCP is a proposed web standard from Chrome for exposing structured tools to browser agents. Instead of asking an agent to infer the purpose of every button and form field, a page can register tools through JavaScript or annotate HTML forms declaratively. The tool carries JSON Schema inputs and outputs, can share page state, and executes visibly in the user's browser context.

This is the right direction for computer-use reliability. Pixel and DOM actuation is flexible, but it is ambiguous: the agent guesses which control maps to which intent, and every extra click is a failure point. WebMCP makes high-value actions explicit. A travel site can expose a multi-city booking tool. A support app can expose a diagnostic tool. A settings page can expose a safe "run checks" command that would be hard to discover from the UI alone.

The security boundary is part of the design. WebMCP is gated by a `tools` Permissions Policy that defaults to same-origin top-level contexts and disables cross-origin iframes unless they opt in with `allow="tools"`. Sensitive actions can request user interaction with a confirmation dialog. The tool still runs in a visible page or webview, which means there is no headless backdoor path by default. That is a limitation, but also a trust property: users can see the site, the brand, and the action surface.

For builders, the test path is clear. Enable the Chrome local flag or use the Chrome 149 origin trial when available, add one imperative tool or one declarative form annotation, define a tight JSON Schema, test with the Model Context Tool Inspector extension, and verify that the tool returns structured errors an agent can recover from. The biggest watch item is portability: WebMCP is proposed, not finished, so keep tool contracts small and avoid betting your whole agent UX on one draft API.

[48:00] Google AI Studio - Workspace, Antigravity export, and Android generation
Google AI Studio's I/O update matters because it connects several app-building surfaces that normally live apart. Generated apps can integrate with Workspace APIs, projects can export into Antigravity, and the mobile build mode can generate native Android apps with an in-browser emulator, ADB device flows, and Play Internal Test Track publishing.

The builder relevance is continuity. A prototype can begin in AI Studio, touch real Workspace data, move into Antigravity for deeper agentic coding, and continue into an Android test track without forcing the developer to rebuild context at each boundary. That is a different workflow from a chat prototype that produces a zip file and leaves the rest of the product path to manual work.

The caution is governance. Workspace integration means real data and real permissions, so generated apps need explicit OAuth scope review, test-user controls, and a clear handoff from prototype credentials to production credentials. Android generation also needs normal mobile hygiene: package identity, signing, internal distribution, device testing, and telemetry. The useful mental model is not "AI Studio replaces the app pipeline." It is "AI Studio now reaches farther into the app pipeline before the handoff."

[55:30] Chrome DevTools for agents - browser verification becomes part of coding work
Chrome DevTools for agents gives coding agents a browser verification lane: managed browser handoff, responsive emulation, geolocation emulation, active Chrome-session debugging, and Lighthouse automation. This is adjacent to WebMCP, but it solves a different problem. WebMCP is about pages exposing explicit tools. DevTools for agents is about letting a coding agent verify the page it just changed.

That distinction matters. A code agent can pass tests and still ship a broken layout, a console error, a failed network request, an inaccessible control, or a slow page. Browser handoff lets the agent inspect the real runtime surface instead of stopping at source code. Responsive and geolocation emulation make the verification less desktop-only. Lighthouse gives it a structured audit path for performance and accessibility issues.

For teams, this pushes UI work toward a tighter loop: edit code, run the app, inspect real page state, capture browser evidence, then patch. The watch item is how much of that loop becomes reliable and scriptable across frameworks and local dev servers. The more stable it gets, the less acceptable it becomes for coding agents to claim frontend work is finished without looking at the rendered page.

[63:00] GitHub Copilot Business and Enterprise - GPT-5.3-Codex becomes the base model
GitHub is making GPT-5.3-Codex the base model for Copilot Business and Enterprise. The important details are model approval gates, long-term-support availability through February 4, 2027, premium request multipliers, GPT-4.1 deprecation timing, and the way base-model defaults shape fallback behavior for enterprise users.

For individual developers, a model upgrade can feel like a preference. For an organization, it is policy. The base model affects what thousands of users get by default, which workloads consume premium requests, which models need approval, and how long older behavior remains available. Long-term support matters because teams need time to validate code-generation behavior, security review patterns, and internal guidance before an old model disappears.

The practical recommendation is to treat the change as a governance migration, not just a better model announcement. Confirm which models are approved, check premium request multipliers against real usage, identify workflows still depending on GPT-4.1 behavior, and document the fallback path before the deprecation window closes.

[70:00] Close - what to test next
The upgrade checklist is practical. For Codex, test Python SDK auth, string turns, `TurnResult`, schema-constrained resume, remote keepalives, image fidelity, and goal-loop stopping. For Claude Code, test `claude agents --json`, OTEL agent IDs, status-line GitHub fields, plugin preview data, hook payloads, and Bash environment-variable permission prompts. For Gemini Managed Agents, test stateful follow-up interactions and file persistence. For WebMCP and Chrome DevTools, test one high-value browser action plus one rendered-page verification loop. For AI Studio and Copilot, review scopes, handoff paths, approval gates, and cost controls before rolling them into daily work.
```

## Verified Links

- https://github.com/openai/codex/releases/tag/rust-v0.132.0
- https://developers.openai.com/codex/changelog
- https://github.com/anthropics/claude-code/releases/tag/v2.1.145
- https://code.claude.com/docs/en/changelog
- https://www.npmjs.com/package/@anthropic-ai/claude-code
- https://ai.google.dev/gemini-api/docs/changelog
- https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights
- https://developers.googleblog.com/all-the-news-from-the-google-io-2026-developer-keynote/
- https://developer.chrome.com/docs/ai/webmcp
- https://blog.google/innovation-and-ai/technology/developers-tools/google-ai-studio-io-2026
- https://developer.chrome.com/docs/devtools/agents
- https://github.blog/changelog/2026-05-17-gpt-5-3-codex-is-now-the-base-model-for-copilot-business-and-enterprise/

## Chapters

- **[00:00] Opening - start with the changed operator surfaces**
- **[02:30] Release readout - Codex 0.132**
- **[17:00] Release readout - Claude Code 2.1**
- **[29:00] Google Gemini - Gemini 3.5 Flash GA and Managed Agents**
- **[39:30] Chrome WebMCP - browser-agent tools become explicit**
- **[48:00] Google AI Studio - Workspace, Antigravity export, and Android generation**
- **[55:30] Chrome DevTools for agents - browser verification becomes part of coding work**
- **[63:00] GitHub Copilot Business and Enterprise - GPT-5.3-Codex becomes the base model**
- **[70:00] Close - what to test next**
