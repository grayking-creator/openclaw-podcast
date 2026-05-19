# AgentStack Daily EP053 — OpenClaw 2026.5.18, Codex 0.131.0, Copilot Remote Agents, and Claude Search Grounding

## Release Coverage Check

- **OpenClaw** — Latest stable/verified version: `v2026.5.18` from `https://api.github.com/repos/openclaw/openclaw/releases?per_page=10` with prereleases skipped. Recent episode version tags detected: `v2026.4.29`, `v2026.5.2`, `v2026.5.3`, `v2026.5.4`, `v2026.5.5`, `v2026.5.6`, `v2026.5.7`, `v2026.5.12`. Selected missing versions: `v2026.5.18`.
- **Hermes Agent** — Latest stable/verified version: `v2026.5.16` / Hermes Agent 0.14.0 from `https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=10` with prereleases skipped. Recent episode version tags detected: `v2026.5.7`, `v2026.5.16`. Selected missing versions: none.
- **OpenAI Codex app/CLI** — Latest stable/verified version: `rust-v0.131.0` from `https://api.github.com/repos/openai/codex/releases?per_page=10` with prereleases skipped and the OpenAI Codex changelog verified at `https://developers.openai.com/codex/changelog`. Recent episode version tags detected: `rust-v0.130.0`. Selected missing versions: `rust-v0.131.0`.
- **Claude Code CLI** — Latest verified npm package version: `2.1.143` from `npm view @anthropic-ai/claude-code version`; concrete changes verified in Anthropic's Claude Code changelog at `https://code.claude.com/docs/en/changelog`. Recent episode version tags detected: `2.1.141`, `2.1.142`, `2.1.143`. Selected missing versions: none.
- **Candidate verification** — OpenClaw and Codex both have latest-contiguous missing blocks starting at their latest stable release. Hermes Agent and Claude Code CLI stop because their latest verified versions are present in the recent version scan. The selected release candidates for this episode are therefore `v2026.5.18` and `rust-v0.131.0`.

## Episode Title

OpenClaw 2026.5.18, Codex 0.131.0, Copilot Remote Agents, and Claude Search Grounding

## Tagline

Upgrade the agent host, sharpen the Codex CLI, steer Copilot sessions across devices, and ground Claude financial research in richer primary-source search results.

## Feed Description

AgentStack Daily EP053 opens with concrete release work: OpenClaw v2026.5.18 adds typed plugin tooling, faster gateway readiness, dialog-aware browser automation, runtime parity QA, realtime Android Talk Mode, safer media handling, stronger channel delivery, Codex app-server repairs, proxy TLS support, and operator-facing Mac app polish. OpenAI Codex CLI 0.131.0 adds richer TUI controls, unified mentions, plugin marketplace and sharing commands, daemon-managed remote control, configured remote environments, an `openai-codex` Python SDK, `codex doctor`, and tougher sandbox, auth, app-server, and state handling. Then the episode moves to GitHub's May 18 Copilot agent updates for remote CLI steering, cheaper model choices, and one-click Actions repair, followed by Anthropic's API update that gives Claude's web search tool richer SEC filing data for cited financial research workflows.

## Story Slate

### 1. **Agent-stack release readout: OpenClaw v2026.5.18 and Codex rust-v0.131.0 move the host and CLI surfaces**
OpenClaw v2026.5.18 is a host release with visible operator changes: typed simple tool plugins via `defineToolPlugin` and `openclaw plugins init/build/validate`, dialog-aware browser snapshots and `blockedByDialog`, HTTPS managed proxy endpoints, faster gateway readiness, runtime parity QA gates, Android realtime Talk Mode, safer image processing, channel delivery fixes, and several Codex app-server repairs for images, code mode, sandbox network access, model validation, context trimming, and restricted-tool fail-closed behavior. Codex `rust-v0.131.0` adds TUI service-tier/status visibility, unified `@` mentions across files/plugins/skills, plugin marketplace/share workflows, daemon-managed `codex remote-control`, configured remote environments, the `openai-codex` Python SDK, `codex doctor`, and hardening for Windows sandboxing, permission profiles, app-server state, Git/auth helpers, and remote cleanup. Technical depth angle: explain plugin API contracts, browser modal state semantics, readiness gating, QA runtime parity coverage, realtime voice relay/tool bridging, Codex remote-control runtime APIs, Python SDK turn routing and approval modes, TUI permission visibility, sandbox failure modes, and migration risks around Node 22.19 and renamed/deprecated plugin/message surfaces.
Primary release links: https://github.com/openclaw/openclaw/releases/tag/v2026.5.18 and https://github.com/openai/codex/releases/tag/rust-v0.131.0

### 2. **GitHub turns Copilot agents into a multi-surface, lower-cost work queue**
GitHub's May 18 Copilot updates make the agent surface more operational: remote control for Copilot CLI sessions is generally available across mobile, web, VS Code, and JetBrains; cloud agent tasks can use Claude Haiku 4.5 or GPT-5.4-mini at a 0.33x multiplier for simpler work; and failing GitHub Actions runs can hand repair work to Copilot cloud agent from the workflow log page. The practical shift is that Copilot agent sessions are less tied to one terminal or one heavyweight model choice: a builder can start work locally, steer it remotely, approve or deny permissions away from the desk, and reserve stronger models for jobs that need them. Technical depth angle: explain remote session attachment, `copilot --remote`, `/remote on`, `remoteSessions` config, permission-request handling, model-selection entrypoint constraints, task cost multipliers, cloud development environments, workflow-log failure context, and where admin policies gate Business and Enterprise use.
Primary links: https://github.blog/changelog/2026-05-18-remote-control-for-copilot-cli-sessions-now-generally-available-on-mobile-web-and-vs-code/ and https://github.blog/changelog/2026-05-18-copilot-cloud-agent-fast-cost-efficient-models-for-simple-tasks/

### 3. **Anthropic gives Claude web search richer SEC filing data for cited financial agents**
Anthropic's May 18 Claude Platform release note says the web search tool now returns richer SEC filing data, which is a narrow update but a meaningful one for agents that summarize earnings, compare public companies, or run due-diligence flows. The technical point is grounding: financial research agents need primary-source citations and filing-specific retrieval metadata, not generic snippets that blur 10-Ks, 10-Qs, 8-Ks, transcripts, and commentary. Technical depth angle: explain web-search tool result contracts, primary-source citation handling, financial-agent retrieval failure modes, SEC filing specificity, downstream summary/audit requirements, and why an agent should preserve source metadata through notes, reports, and claims rather than collapse filings into unsupported prose.
Primary link: https://docs.anthropic.com/en/release-notes/api

## Extra Research Candidates

- **Copilot Spaces API becomes generally available** — Primary source: https://github.blog/changelog/2026-05-18-copilot-spaces-api-now-generally-available/ and REST docs: https://docs.github.com/en/rest/copilot-spaces. Technical depth angle: explain CRUD APIs for team context containers, collaborator/resource management, and how programmatic Spaces management changes enterprise context hygiene for large Copilot deployments.
- **OpenAI and Dell outline Codex in hybrid and on-prem enterprise environments** — Primary source: https://openai.com/index/dell-codex-enterprise-partnership/. Technical depth angle: explain the technical boundary between Codex agents, governed on-prem data platforms, AI Factory workload infrastructure, system-of-record integration, and the security/latency tradeoffs of bringing agent execution closer to enterprise data.
- **Repository-level Copilot cloud agent configuration gets REST audit surfaces** — Primary source: https://github.blog/changelog/2026-05-18-audit-repository-copilot-cloud-agent-configuration-via-the-rest-api/ and REST index: https://docs.github.com/en/rest/copilot. Technical depth angle: explain configuration inventory, repository policy drift detection, org-scale agent enablement audits, and why API-visible cloud-agent settings matter before enterprises delegate issue, workflow, and branch repair tasks.

## Show Notes

```md
[00:00] Hook — start with the host and the CLI
OpenClaw v2026.5.18 is the first upgrade to inspect because it changes the surfaces an agent host depends on every day: plugin tooling, browser automation, gateway startup, proxy routing, mobile voice, channel delivery, media safety, and Codex app-server behavior. Codex rust-v0.131.0 lands beside it as a CLI and app-server release: more visible status in the TUI, broader mention search, plugin marketplace commands, remote-control plumbing, configured remote environments, a Python SDK, and diagnostics that make support cases less guessy.

The practical read is simple. If OpenClaw is the host, v2026.5.18 improves how agents connect to plugins, browsers, channels, mobile voice sessions, and Codex-backed runtimes. If Codex is the coding surface, 0.131.0 makes the CLI easier to operate in long sessions and gives remote and SDK workflows more explicit contracts. After the release block, the episode turns to GitHub's May 18 Copilot agent changes and Anthropic's API update for richer SEC filing search results.

[02:30] Agent-stack release readout — OpenClaw v2026.5.18
OpenClaw v2026.5.18 is a broad host release, but the first builder-facing change is plugin shape. The release adds `defineToolPlugin` plus `openclaw plugins init`, `openclaw plugins build`, and `openclaw plugins validate` for typed simple tool plugins with generated manifest metadata, optional declarations, and context factories. That makes small plugin work less dependent on hand-written manifest glue. It also matters for deprecation: the release marks older rich-message producer APIs such as legacy interactive and Slack directive paths as deprecated while adding channel presentation capability limits, so plugin authors get a clearer contract for what a renderer can actually show.

The browser changes are small but important for automation reliability. Snapshots now surface pending and recently handled modal dialogs, actions can return `blockedByDialog` when a modal opens, and `browser dialog --dialog-id` can answer a pending dialog. That changes a common failure mode in browser agents: instead of a click silently failing because an alert or confirm dialog seized the page, the automation layer can represent the dialog as state and give the agent an explicit next action.

Gateway startup and proxy behavior also move. Startup logging and plugin-service startup now overlap with channel sidecars while preserving `/readyz` sidecar gating, and restart traces attribute probe, config, runtime, and resource-count costs without changing readiness semantics. For operators, the useful part is not just faster ready time; it is better evidence when a restart is slow. The release also adds HTTPS managed forward-proxy endpoints and scoped `proxy.tls.caFile` trust, which gives deployments a cleaner way to route through TLS-inspected or private proxy paths without turning proxy configuration into a global trust decision.

The QA-Lab work is unusually important. OpenClaw adds first-hour 20-turn and optional 100-turn runtime parity scenarios, `openclaw qa suite --runtime-parity-tier`, tool fixture coverage through `openclaw qa coverage --tools`, live runtime token-efficiency artifacts, and a hard gate for required OpenClaw dynamic runtime-tool drift in the standard Codex-vs-Pi tier. In plain terms: the project is adding release checks that compare runtime behavior, tool vocabulary, token use, and tool coverage instead of treating a smoke test as enough. That is the right direction for agent hosts, where regressions often appear as "the agent used the wrong tool" rather than "the process crashed."

Android Talk Mode gets a major runtime change too. The Android app switches Talk Mode to realtime Gateway relay voice sessions with streaming microphone input, realtime audio playback, tool-result bridging, and on-screen transcripts. This turns mobile voice from a simple input/output wrapper into an active session that can carry tool results back through the Gateway. The risk to test is interruption and latency: streaming voice sessions need clean cancellation, transcript alignment, and tool-result timing that does not leave the user hearing stale output.

The fixes are where many production upgrades will feel the release. Generated media completions now return to Telegram forum topics by preserving topic IDs across requester-agent handoff. Image metadata probing avoids invoking external decoder delegates on unrecognized bytes, and Sharp is installed with fallbacks to native imaging tools, ImageMagick, GraphicsMagick, or ffmpeg. Discord voice sessions keep hearing follow-up turns with OpenAI realtime and prebuffer assistant playback to reduce choppy starts. Message/TTS directives are applied before message-tool sends reach delivery paths, so opt-in rooms get voice notes instead of raw tags.

OpenClaw's Codex app-server repairs are especially relevant for mixed agent stacks. Current inbound image attachments hydrate before queued runs so Responses-backed agents receive channel images as native vision input. Native code mode stays available without forcing code-mode-only, which lets OpenClaw dynamic tool turns complete through the app-server bridge. Network access is preserved for sandboxed Codex code-mode turns when the OpenClaw sandbox allows outbound egress. Per-agent code-mode config is honored in schema, runtime catalog activation, and model payload filtering. Restricted chat or sender policy now fails closed by disabling native code, app, environment, and user MCP surfaces for restricted turns. The pattern is clear: Codex integration is being tightened around policy, media, sandboxing, and model/runtime selection.

Migration notes for OpenClaw v2026.5.18 are concrete. The minimum supported Node.js 22 line rises to 22.19, Pi packages move to 0.75.1, and Docker/Podman builds should prefer `OPENCLAW_IMAGE_APT_PACKAGES` while `OPENCLAW_DOCKER_APT_PACKAGES` remains as a legacy fallback. The Obsidian skill now targets the official `obsidian` CLI rather than the third-party `obsidian-cli`. The repo-local Codex closeout review skill and helper are renamed to `autoreview`. Channel/plugin authors should inspect deprecated message producer surfaces and presentation capability limits before assuming old rich-message controls render the same way everywhere.

[17:30] Agent-stack release readout — Codex rust-v0.131.0
Codex rust-v0.131.0 is the matching CLI-side release. The TUI now exposes data-driven service-tier commands, blended token usage, permissions and approval mode, effective workspace roots, and responsive Markdown tables. That sounds like interface work, but it changes day-to-day operations: during a long run, the operator can see which permission and approval envelope the agent is actually using and which workspace roots are active, instead of reconstructing those facts from config files and memory.

Mentions get broader. `@` search now covers files, directories, plugins, and skills in one picker, backed by app-server plugin metadata. That makes the interaction model closer to how builders actually think: the thing to bring into context may be a file, a directory, a skill, or a plugin, and the agent surface should not make those separate discovery lanes. The risk is context bloat, so the practical recommendation is to use the picker to attach the smallest useful artifact rather than treating it as a bulk import tool.

Plugin workflows also move forward. Codex adds marketplace CLI commands, version-aware sharing, share checkout, clearer shared-workspace buckets, and default-enabled plugin hooks. This is a step toward plugins behaving like managed development artifacts rather than loose local folders. The migration watch item is hook trust and scope: default-enabled hooks are powerful, so plugin provenance, workspace sharing, and version gates matter more as the workflow becomes smoother.

Remote work is a major part of 0.131.0. The release adds daemon-managed `codex remote-control`, runtime enable and disable APIs, status reads, registry-backed and configured remote environments, and app-server/API contracts for remote environments and desktop-owned config namespaces. For users, the capability is remote agent work that can be started, monitored, or managed outside the immediate terminal. For builders integrating Codex, the API contracts matter because remote environments need durable identity, lifecycle, status, and configuration boundaries rather than a best-effort shell process.

The Python SDK is now `openai-codex` / `openai_codex`, with pinned runtime-generated types, concurrent turn routing, approval modes, and integration coverage. That gives Python applications a cleaner way to drive Codex turns and receive notifications by ID instead of treating the CLI as a text-only subprocess. The important mechanism is turn routing: concurrent agent work needs IDs and structured events so approvals, tool activity, and outputs do not cross wires.

Codex also adds `codex doctor` for diagnostics across runtime, auth, terminal, network, config, and local state. This is the kind of command that pays for itself during failed upgrades. Instead of asking whether the failure is a terminal issue, a stale auth token, a network policy, or a local state database problem, the CLI can gather support-ready evidence in one place. The release also makes app-server and local state startup safer by preserving SQLite data, failing closed when state cannot open, adding recovery paths, and softening optional metadata sync failures.

The bug-fix block hardens real failure modes. Windows sandbox behavior improves around deny-read rules, scoped write roots, ineffective firewall policy, and PowerShell edge cases. Managed read restrictions survive permission escalation, and workspace-root permission profile resolution gets cleaned up. Git and auth reliability improve through root worktree hooks, ignoring repo hook and fsmonitor config in helper commands, binding local MCP OAuth callbacks, and revoking superseded login tokens. Remote and Windows cleanup get longer exec-server transport timeouts, quieter `taskkill`, and non-queued plugin reads. The release is less about one flashy capability and more about making long CLI sessions and remote sessions observable, recoverable, and safer.

[29:30] GitHub Copilot agents — remote steering, cheaper models, and Actions repair
GitHub's May 18 Copilot updates are a useful snapshot of where hosted coding agents are going. Remote control for Copilot CLI sessions is now generally available on GitHub Mobile, github.com, VS Code, and JetBrains. The mechanics are explicit: start with `copilot --remote`, enable it inside a session with `/remote on`, or set `remoteSessions` in the Copilot settings file. Once attached, the remote surface can stream session activity, accept queued input, answer permission prompts, stop a session, and let the user steer work away from the original terminal.

That changes the shape of CLI-agent work. A local terminal is still the execution anchor, but the supervision surface can move. The machine needs to stay online, and GitHub's docs call out `/keep-alive` for longer runs. Sessions are user-specific, and Business or Enterprise users may need administrators to enable remote control and CLI policies. Those constraints are important: remote steering is not magic background compute; it is a live local session with a remote control plane and policy gates.

GitHub also expanded Copilot cloud agent model choices with Claude Haiku 4.5 and GPT-5.4-mini, each listed at a 0.33x multiplier. This is the right product direction for coding agents because not every delegated job needs the strongest model. Straightforward dependency bumps, small test fixes, lint failures, or mechanical edits can run on a cheaper model, while design-heavy or ambiguous changes can use a stronger one. The docs say model selection is available from supported entrypoints such as assigning an issue, mentioning `@copilot` in a pull request comment, starting from agent surfaces, GitHub Mobile, or Raycast; where no picker exists, Auto is used.

The third Copilot change is one-click repair for failing GitHub Actions. From a workflow run logs page, Copilot Business and Enterprise subscribers can click Fix with Copilot; the cloud agent investigates the failure, pushes a fix to the branch, and tags the user for review. Technically, that is an agent entrypoint with a strong context bundle: failing job logs, branch state, repository instructions, and cloud development environment. The practical builder implication is that CI failures become a delegatable work item without manually pasting logs into chat. The risk is review discipline: a pushed branch fix still needs code review, test verification, and attention to whether the agent optimized for green CI rather than the right design.

[38:30] Anthropic API — richer SEC filing data in Claude web search
Anthropic's May 18 Claude Platform note says the web search tool now returns richer SEC filing data. That is a focused API update, but it matters for any agent doing financial research, earnings analysis, competitive analysis, or due diligence. The difference between a generic web result and filing-aware search is source quality. An agent needs to know whether it is citing a 10-K, 10-Q, 8-K, proxy statement, or other primary filing, and it needs enough metadata to keep those citations attached through summaries and reports.

The failure mode this addresses is familiar: a model summarizes a financial claim from a search result, then loses the filing identity or mixes primary filings with analyst commentary. Richer SEC filing data gives the tool layer a better chance of carrying primary-source evidence into the model context. Builders should preserve that metadata in their own outputs. If an agent writes a memo, each material claim should point back to the filing, date, company, and section when available. If the agent writes structured research notes, the filing source should remain a first-class field, not a sentence buried in prose.

The practical recommendation is to treat web search results as evidence objects. Keep the URL, title, filing type, date, citation text, and retrieval timestamp. When the agent compares companies or summarizes risk factors, require it to separate primary filings from secondary commentary. For workflows that feed downstream spreadsheets, reports, or decisions, log the citation payload with the final answer. Claude's richer search result is only useful if the application preserves the grounding boundary all the way to the user.

[45:00] Closing — upgrade priorities
For OpenClaw, test v2026.5.18 on the real surfaces that changed: plugin build/validation, browser modal handling, gateway restart readiness, HTTPS proxy trust, Android Talk Mode, Telegram topics, Discord realtime voice, image media handling, and Codex app-server turns with images, sandboxed network, code mode, and restricted sender policy. Also check Node 22.19 compatibility and any local skill references to renamed or deprecated command paths.

For Codex, update to 0.131.0 and exercise the TUI status line, service-tier commands, unified mentions, plugin marketplace/share commands, remote-control flows, configured remote environments, Python SDK turn routing, `codex doctor`, Windows sandbox cases if relevant, and app-server state recovery. For Copilot, use cheaper cloud-agent models for simple repair work, keep remote sessions policy-gated, and review one-click Actions fixes as code changes rather than as final answers. For Claude financial agents, preserve SEC filing metadata and citations as structured evidence, not just text.
```

## Verified Links

- OpenClaw v2026.5.18 release: https://github.com/openclaw/openclaw/releases/tag/v2026.5.18
- OpenClaw releases API: https://api.github.com/repos/openclaw/openclaw/releases?per_page=10
- Hermes Agent releases API: https://api.github.com/repos/NousResearch/hermes-agent/releases?per_page=10
- Hermes Agent v2026.5.16 release: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.16
- OpenAI Codex rust-v0.131.0 release: https://github.com/openai/codex/releases/tag/rust-v0.131.0
- OpenAI Codex changelog: https://developers.openai.com/codex/changelog
- OpenAI Codex releases API: https://api.github.com/repos/openai/codex/releases?per_page=10
- Claude Code npm package: https://www.npmjs.com/package/@anthropic-ai/claude-code
- Claude Code changelog: https://code.claude.com/docs/en/changelog
- GitHub Copilot remote control GA: https://github.blog/changelog/2026-05-18-remote-control-for-copilot-cli-sessions-now-generally-available-on-mobile-web-and-vs-code/
- GitHub Copilot remote steering docs: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/steer-remotely
- GitHub Copilot cloud agent faster models: https://github.blog/changelog/2026-05-18-copilot-cloud-agent-fast-cost-efficient-models-for-simple-tasks/
- GitHub Copilot model selection docs: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/changing-the-ai-model
- GitHub Copilot one-click Actions fixes: https://github.blog/changelog/2026-05-18-one-click-fixes-for-failing-actions-with-copilot-cloud-agent/
- GitHub Copilot session docs: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/start-copilot-sessions
- Anthropic Claude Platform release notes: https://docs.anthropic.com/en/release-notes/api
- Copilot Spaces API GA: https://github.blog/changelog/2026-05-18-copilot-spaces-api-now-generally-available/
- Copilot Spaces REST docs: https://docs.github.com/en/rest/copilot-spaces
- OpenAI and Dell Codex enterprise partnership: https://openai.com/index/dell-codex-enterprise-partnership/
- GitHub Copilot REST API index: https://docs.github.com/en/rest/copilot

## Chapters

- **[00:00] Hook — start with the host and the CLI**
- **[02:30] Agent-stack release readout — OpenClaw v2026.5.18**
- **[17:30] Agent-stack release readout — Codex rust-v0.131.0**
- **[29:30] GitHub Copilot agents — remote steering, cheaper models, and Actions repair**
- **[38:30] Anthropic API — richer SEC filing data in Claude web search**
- **[45:00] Closing — upgrade priorities**

