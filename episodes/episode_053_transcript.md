# AgentStack Daily EP053: OpenClaw 2026.5.18, Codex 0.131.0, Copilot Remote Agents, and Claude Search Grounding

[NOVA]: I'm NOVA.

[ALLOY]: And I'm ALLOY, and this is AgentStack Daily. Today starts with the host and the coding surface: OpenClaw v2026.5.18 and Codex rust-v0.131.0.

[NOVA]: OpenClaw adds typed plugin tooling, dialog-aware browser automation, faster gateway readiness, HTTPS proxy support, realtime Android Talk Mode, safer media handling, stronger channel delivery, and tighter Codex app-server behavior. Codex adds better TUI status, unified mentions, plugin marketplace commands, remote-control plumbing, configured remote environments, a Python SDK, and codex doctor.

[ALLOY]: That is the useful shape of the episode. First, the agent host. Then, the CLI and app-server layer developers touch all day. After that, GitHub turns Copilot agent sessions into something you can steer from more places and price with smaller models. And Anthropic gives Claude web search richer SEC filing data for financial research agents.

[NOVA]: The practical question is not whether agents are getting more features. They are. The question is which pieces make agent work more observable, more recoverable, and easier to trust when the run is long, remote, multimodal, or policy constrained.

[ALLOY]: So we are going to stay concrete: plugin contracts, browser modal state, readiness probes, runtime parity checks, voice relay behavior, TUI status, permission envelopes, remote sessions, task multipliers, Actions repair, and source metadata for financial claims. [PAUSE]

## [00:00-17:30] Agent-stack release readout: OpenClaw v2026.5.18 moves the host surface

[NOVA]: Agent-stack release readout starts with OpenClaw because the host is where an agent stack either feels durable or feels improvised. A host has to connect models, tools, channels, browsers, mobile clients, media inputs, permissions, and app-server bridges. When that host release changes plugin shape, browser state, gateway readiness, mobile voice, and Codex integration in one pass, it deserves the front of the episode.

[ALLOY]: The first builder-facing change is plugin shape. OpenClaw adds defineToolPlugin and the openclaw plugins init, openclaw plugins build, and openclaw plugins validate commands for typed simple tool plugins. That gives plugin authors generated manifest metadata, optional declarations, and context factories instead of asking every small plugin to carry hand-written glue.

[NOVA]: That sounds like developer ergonomics, and it is, but it is also a reliability feature. Tool plugins become much easier to inspect when the manifest and declarations are generated from a typed source. A host can reason about what a plugin exposes, what context it expects, and what shape its inputs and outputs should take. The fewer undocumented surfaces around a tool, the fewer surprises show up inside an agent run.

[ALLOY]: It also matters because the release deprecates older rich-message producer surfaces, including legacy interactive and Slack directive paths, while adding channel presentation capability limits. That is a healthier contract. A plugin should know whether the channel can render an interactive control, a rich block, a plain message, an attachment, a voice note, or only a narrow fallback.

[NOVA]: Right. The mistake in a lot of agent tooling is treating every channel like the same output surface. A web chat, a Discord channel, a Telegram topic, a Slack thread, and a mobile voice session do not have identical presentation rules. If a plugin assumes they do, the agent may produce an object the channel cannot show. Presentation capability limits let the host say what is actually possible before the final response gets shaped.

[ALLOY]: The browser changes are the second major host item. Snapshots now surface pending and recently handled modal dialogs. Actions can return blockedByDialog when a modal opens. And browser dialog with a dialog ID can answer a pending dialog. That is exactly the kind of small state improvement that saves browser agents from vague failures.

[NOVA]: Browser automation often fails in boring ways. A click does not work because an alert opened. A form submit appears stuck because a confirm dialog took over the page. An agent keeps trying to interact with stale page state because it cannot see the modal that a human would notice instantly. By representing dialogs as explicit state, the browser layer gives the agent a real next action instead of forcing it to infer from a timeout.

[ALLOY]: The important phrase is explicit state. A modal is not just noise on top of the page. It changes the page's interaction contract. When an action returns blockedByDialog, the agent can stop pretending it has a normal DOM problem and handle the dialog directly.

[NOVA]: That makes browser agents easier to audit too. If the transcript of a run says the action was blocked by a dialog, the operator can understand why a sequence paused. If the host only reports a click failure, the debugging path is much worse: network, selector, iframe, timing, auth, page crash, or something else entirely.

[ALLOY]: Gateway startup and proxy behavior are next. OpenClaw now overlaps startup logging and plugin-service startup with channel sidecars while preserving readyz sidecar gating. Restart traces attribute probe, config, runtime, and resource-count costs without changing readiness semantics.

[NOVA]: That is a subtle but valuable operator change. Faster startup is useful, but the more important piece is evidence. If a restart is slow, an operator needs to know whether the cost is probe time, config load, runtime startup, sidecar work, plugin service startup, or resource counting. Agent infrastructure is full of moving parts, so readiness has to be both conservative and explainable.

[ALLOY]: And preserving readiness semantics matters. It is easy to speed up a service by saying it is ready before the dependencies are ready. That is not an improvement. It just moves the failure downstream. The useful version is overlapping work where safe, but still letting readyz mean the host can actually serve the surfaces it promises.

[NOVA]: The proxy work is also practical. The release adds HTTPS managed forward-proxy endpoints and scoped proxy.tls.caFile trust. That gives deployments a cleaner way to route traffic through TLS-inspected or private proxy paths without turning proxy configuration into a global trust decision.

[ALLOY]: This matters in enterprise and lab environments where outbound traffic is not simply open internet. Agents call APIs, fetch pages, access docs, reach model endpoints, and move media. If the proxy path requires special trust, that trust should be scoped to the proxy configuration. It should not casually widen trust across the whole runtime.

[NOVA]: The QA-Lab block may be the most important part for people who ship agent hosts. OpenClaw adds first-hour 20-turn and optional 100-turn runtime parity scenarios, openclaw qa suite runtime parity tier, tool fixture coverage through openclaw qa coverage tools, live runtime token-efficiency artifacts, and a hard gate for required OpenClaw dynamic runtime-tool drift in the standard Codex-vs-Pi tier.

[ALLOY]: In plain terms, the release is checking whether different runtimes behave similarly enough under real agent pressure. That is much more useful than only checking whether the process boots. Agent regressions often show up as tool vocabulary drift, bad tool selection, changed token use, missing fixtures, or a runtime choosing the wrong surface.

[NOVA]: Exactly. A smoke test can say the server is alive while the agent is quietly worse. Runtime parity scenarios ask a harder question: if the same task goes through different runtime paths, do the tool choices, capabilities, and outputs remain within an expected envelope? That is how you catch the kind of release regression that users describe as the agent feels different now.

[ALLOY]: The 20-turn and 100-turn shape matters because short agent tests are too forgiving. A one-turn tool call does not tell you whether context trimming, tool state, permissions, error recovery, and model routing remain stable after a real session. Longer scenarios expose the slow failures.

[NOVA]: Android Talk Mode gets a big runtime change too. The Android app switches Talk Mode to realtime Gateway relay voice sessions with streaming microphone input, realtime audio playback, tool-result bridging, and on-screen transcripts.

[ALLOY]: That turns mobile voice into an active session surface. It is not just speech-to-text in and text-to-speech out. A realtime voice session can carry tool results back through the Gateway, keep a transcript visible, and make the assistant feel continuous while tools are running.

[NOVA]: The engineering risk is interruption and timing. Streaming microphone input needs clean cancellation. Realtime audio playback needs to stop when the user interrupts. Tool-result bridging needs to avoid reading stale output after the user has changed direction. And transcripts need to align closely enough that the user can tell what the agent heard and what it did.

[ALLOY]: That is why mobile voice is a host feature, not only a client feature. The client can capture audio, but the host has to coordinate session identity, tool events, streaming responses, cancellation, and channel policy. If the host is sloppy, the voice UX becomes confusing even when the audio itself sounds fine.

[NOVA]: The fixes block is where many production upgrades will feel the release. Generated media completions now return to Telegram forum topics by preserving topic IDs across requester-agent handoff. Image metadata probing avoids invoking external decoder delegates on unrecognized bytes. Sharp is installed with fallbacks to native imaging tools, ImageMagick, GraphicsMagick, or ffmpeg.

[ALLOY]: Those are not glamorous items, but they are the things that keep agent systems from losing work. If a generated image response lands in the wrong topic, the user experience breaks. If metadata probing calls external decoder delegates on unknown bytes, media handling carries unnecessary security and reliability risk. If image processing depends on one native module path and it fails, the whole media feature gets brittle.

[NOVA]: Discord voice sessions also get attention. The release keeps follow-up turns working with OpenAI realtime and prebuffers assistant playback to reduce choppy starts.

[ALLOY]: The prebuffer point is small but humane. Realtime voice is judged by timing. If the assistant starts with chopped audio or fails to hear the next turn, the user loses confidence fast. A technically correct voice stack still feels broken when turn-taking is rough.

[NOVA]: Message and TTS directives are applied before message-tool sends reach delivery paths, so rooms that opt into voice notes get voice notes instead of raw tags. That is another channel contract fix. The directive should shape delivery before the message is sent, not leak as text to the user.

[ALLOY]: OpenClaw's Codex app-server repairs are especially relevant for mixed agent stacks. Current inbound image attachments hydrate before queued runs, so Responses-backed agents receive channel images as native vision input. Native code mode stays available without forcing code-mode-only, which lets OpenClaw dynamic tool turns complete through the app-server bridge.

[NOVA]: Network access is preserved for sandboxed Codex code-mode turns when the OpenClaw sandbox allows outbound egress. Per-agent code-mode config is honored in schema, runtime catalog activation, and model payload filtering. Restricted chat or sender policy now fails closed by disabling native code, app, environment, and user MCP surfaces for restricted turns.

[ALLOY]: That last part is the security boundary. In an agent host, restricted turns should not simply rely on the model behaving well. The runtime should remove surfaces the sender is not allowed to use. Failing closed means a restricted user does not get native code, local app access, environment access, or user MCP surfaces by accident.

[NOVA]: The image hydration fix is also important. A user sending a screenshot through a channel expects the agent to see the screenshot, not a placeholder or a file path that the model cannot inspect. Hydrating images before queued runs keeps multimodal context attached to the actual turn.

[ALLOY]: And preserving sandboxed network access when policy allows it matters because code-mode tasks often need package metadata, docs, APIs, or tests that call external resources. The host should not accidentally strip network access if the configured sandbox envelope permits it.

[NOVA]: Migration notes are concrete. The minimum supported Node.js 22 line rises to 22.19. Pi packages move to 0.75.1. Docker and Podman builds should prefer OPENCLAW_IMAGE_APT_PACKAGES, while OPENCLAW_DOCKER_APT_PACKAGES remains as a legacy fallback. The Obsidian skill now targets the official obsidian CLI rather than the third-party obsidian-cli. The repo-local Codex closeout review skill and helper are renamed to autoreview.

[ALLOY]: The practical upgrade path is to test the real surfaces that changed. Build and validate a small plugin. Trigger a browser modal and make sure the dialog path is visible. Restart the gateway and inspect readiness traces. Exercise the HTTPS proxy path if your deployment uses private trust. Try Android Talk Mode with interruption. Send media through the channels you actually use. Run Codex app-server turns with images, sandboxed network, code mode, and restricted sender policy.

[NOVA]: A good builder workflow after this release is to pick one real task per surface. For plugins, build a tiny tool that reads input, returns structured output, and declares only the context it needs. For browser automation, build a test page that opens an alert, a confirm, and a prompt, then verify the agent can see the blocked dialog state and answer it. For media, send a small image, a malformed image, and a generated image request through the actual channel path you support.

[ALLOY]: For gateway readiness, the workflow should include a restart under normal load, then a restart with one slow sidecar or plugin service. The goal is not only a fast boot. The goal is to understand which probe, config, runtime, or resource step costs time. If a team ships OpenClaw as internal infrastructure, that restart trace becomes part of the support workflow when someone says the agent host is slow after deploy.

[NOVA]: For Android Talk Mode, the useful workflow is a real interruption test. Start a voice session, ask for a tool-backed answer, interrupt while audio is playing, then ask a follow-up that depends on the previous tool result. A good result is not only that speech works. A good result is that cancellation works, transcripts stay coherent, and tool results do not arrive as stale speech after the user has moved on.

[ALLOY]: For restricted sender policy, the build workflow should be deliberately adversarial. Try a turn from a restricted sender that asks for local code, app access, environment access, and user MCP access. The correct behavior is not a polite refusal from the model. The correct behavior is that those runtime surfaces are absent before the model can reach for them.

[NOVA]: That is the OpenClaw readout: host work that makes plugins more typed, browser failures more explicit, startup more observable, proxy trust more scoped, QA more runtime-aware, mobile voice more realtime, media safer, channels more reliable, and Codex integration more policy-aware. [PAUSE]

## [17:30-29:30] Agent-stack release readout: Codex rust-v0.131.0 moves the CLI and app-server surface

[ALLOY]: The second half of the agent-stack release readout is Codex rust-v0.131.0. If OpenClaw is the host surface, Codex is the coding surface: the TUI, the app server, the remote-control path, the SDK, the sandbox, auth, state, and tool bridge that developers live inside.

[NOVA]: The first visible change is TUI status. Codex now exposes data-driven service-tier commands, blended token usage, permissions and approval mode, effective workspace roots, and responsive Markdown tables. That sounds like display work, but it changes how operators manage long sessions.

[ALLOY]: During a long coding run, you want to know the permission envelope. Is the agent in a read-only posture, a workspace-write posture, or something more permissive? What approval mode is actually active? Which workspace roots are effective? Which service tier is in use? How much token budget has been spent? If the TUI shows those facts, the operator does not have to reconstruct them from scattered config and memory.

[NOVA]: That matters because the failure cases are expensive. If a user thinks the agent can write one directory but the effective root is different, edits may land in the wrong place or fail unexpectedly. If approval mode is misunderstood, a task can block on prompts the operator did not expect. If token usage is invisible, a long session can drift into expensive or degraded behavior without warning.

[ALLOY]: Mentions get broader too. At-sign search now covers files, directories, plugins, and skills in one picker, backed by app-server plugin metadata. That matches how builders think. The thing you need might be a source file, a folder, a local skill, or a plugin capability. The interface should not force those into four separate discovery paths.

[NOVA]: The caution is context discipline. A unified picker is useful because it reduces friction, but friction was sometimes protecting the session from bloat. The best use is to attach the smallest artifact that carries the needed context: one file, one directory, one skill, or one plugin reference, not a pile of everything that looks adjacent.

[ALLOY]: Plugin workflows move forward. Codex adds marketplace CLI commands, version-aware sharing, share checkout, clearer shared-workspace buckets, and default-enabled plugin hooks. This is a shift from plugins as loose local folders toward plugins as managed development artifacts.

[NOVA]: Version-aware sharing is a big deal. If two users or two machines are talking about the same plugin, they need to know whether they are actually using the same version. Share checkout and clearer workspace buckets help make that explicit. Default-enabled hooks make the experience smoother, but they also raise the trust bar.

[ALLOY]: Hooks are powerful because they run around the development process. That means provenance, scope, version gates, and workspace boundaries matter. A plugin marketplace is not only a convenience feature. It becomes part of the supply chain for agent behavior.

[NOVA]: Remote work is one of the major pieces in this Codex release. The release adds daemon-managed codex remote-control, runtime enable and disable APIs, status reads, registry-backed and configured remote environments, and app-server API contracts for remote environments and desktop-owned config namespaces.

[ALLOY]: Remote control is not just run this somewhere else. A real remote environment needs identity, lifecycle, status, cleanup, configuration boundaries, and permission behavior. If those are not explicit, remote agent work becomes a shell process with a nicer label.

[NOVA]: The daemon-managed shape matters because long-running agent work needs a coordinator. The daemon can expose status, manage runtime enablement, and keep remote-control state separate from a single terminal session. That is the difference between a feature that works in a demo and a feature that survives day-to-day use.

[ALLOY]: Configured remote environments also matter for teams and power users. A remote environment should not be an improvised target every time. It should be named, discoverable, policy-aware, and recoverable. The app-server contract gives integrations something structured to call instead of scraping terminal output.

[NOVA]: The Python SDK is now openai-codex and imports as openai_codex. It includes pinned runtime-generated types, concurrent turn routing, approval modes, and integration coverage. That gives Python applications a real path to drive Codex turns without treating the CLI as a text-only subprocess.

[ALLOY]: Turn routing is the key mechanism. If an app drives more than one agent turn, it needs IDs and structured events. Otherwise approvals, tool activity, notifications, and outputs can cross wires. Concurrent work without structured routing is where subtle bugs become awful: approval intended for one turn gets associated with another, or a tool event appears under the wrong task.

[NOVA]: Approval modes also need to be explicit in an SDK. A Python app embedding Codex has to know whether a turn may ask for permission, whether it can execute tools, whether it can write, and how those approvals are surfaced to the controlling application. That is not optional plumbing. It is the safety model.

[ALLOY]: Codex also adds codex doctor for diagnostics across runtime, auth, terminal, network, config, and local state. This is the sort of command that sounds small until the first messy upgrade.

[NOVA]: A failed coding agent can fail from stale auth, terminal quirks, network policy, config conflicts, local state database trouble, runtime mismatches, sandbox behavior, or app-server startup. Without diagnostics, support becomes a guessing game. A doctor command can gather support-ready evidence and shorten the path from it broke to this is the broken layer.

[ALLOY]: The release also makes app-server and local state startup safer by preserving SQLite data, failing closed when state cannot open, adding recovery paths, and softening optional metadata sync failures. That combination is good engineering. Preserve durable state. Do not proceed unsafely if required state cannot open. Recover when possible. Do not let optional metadata sync take down the primary path.

[NOVA]: The hardening block is broad. Windows sandbox behavior improves around deny-read rules, scoped write roots, ineffective firewall policy, and PowerShell edge cases. Managed read restrictions survive permission escalation. Workspace-root permission profile resolution gets cleaned up.

[ALLOY]: Git and auth reliability improve through root worktree hooks, ignoring repo hook and fsmonitor config in helper commands, binding local MCP OAuth callbacks, and revoking superseded login tokens. Remote and Windows cleanup get longer exec-server transport timeouts, quieter taskkill, and non-queued plugin reads.

[NOVA]: The pattern is recoverability. A coding agent is only useful if it can work inside real repositories, real auth flows, real Windows shells, real sandbox policies, and real app-server state. Those environments are messy. The release is less about one flashy capability and more about making long sessions observable, recoverable, and safer.

[ALLOY]: The migration advice for Codex is simple: after updating, exercise the TUI status line, service-tier commands, unified mentions, plugin marketplace and share commands, remote-control flows, configured remote environments, Python SDK turn routing, codex doctor, Windows sandbox cases if relevant, and app-server state recovery.

[NOVA]: Also test permission visibility. Start a session with the approval mode and workspace roots you expect, then verify the TUI shows the same reality. Use at-sign mentions with one file, one directory, one skill, and one plugin to make sure the picker is useful without overloading the turn. For remote environments, check status reads and cleanup, not just start.

[ALLOY]: For SDK builders, test concurrent turns deliberately. Run two small jobs, trigger approval or tool activity in both, and make sure notifications land under the right IDs. That is where a structured SDK earns trust.

[NOVA]: There is also a clean build workflow for the unified mention picker. Start with a narrow file mention when the task is local. Move to a directory mention only when the agent needs neighboring tests or related modules. Use a skill mention when the important context is a procedure, not source code. Use a plugin mention when the task depends on a capability. That workflow keeps the session focused while still making the new picker valuable.

[ALLOY]: For plugin sharing, the workflow should include version checks. Share a plugin, check it out in a second workspace, verify the version that loaded, then exercise any default-enabled hooks in a small repository before trusting them in a larger one. Smooth plugin sharing is useful, but it should not make hook behavior invisible.

[NOVA]: For remote-control work, build a lifecycle test. Start a session, enable remote control, read status, send a small correction from a second surface, answer a permission request, disable remote control, and confirm cleanup. That is the kind of workflow that catches mismatched state. If start works but status is wrong, the feature will be hard to operate. If disable works but cleanup leaves stale state, the next session can inherit confusion.

[NOVA]: So the Codex readout is: clearer operating state in the TUI, broader context attachment through unified mentions, more managed plugin sharing, daemon-backed remote control, configured remote environments, a Python SDK with structured turn routing, diagnostics, and a long list of sandbox, auth, Git, Windows, app-server, and state repairs.

[ALLOY]: Paired with OpenClaw, it points to the same direction. Agent tools are becoming less magical and more inspectable. The host can explain what it can render and which dialog blocked it. The CLI can explain which permission mode and workspace roots are active. The SDK can route concurrent turns by ID. That is how agent work gets easier to operate. [PAUSE]

## [29:30-38:30] GitHub turns Copilot agents into a multi-surface, lower-cost work queue

[NOVA]: GitHub turns Copilot agents into a multi-surface, lower-cost work queue with three May 18 updates: remote control for Copilot CLI sessions is generally available across mobile, web, VS Code, and JetBrains; Copilot cloud agent tasks can use cheaper models for simpler work; and failing GitHub Actions can hand repair work to Copilot from the workflow logs page.

[ALLOY]: The remote-control mechanics are explicit. A user can start with copilot remote, enable remote control inside a session with remote on, or configure remoteSessions in the Copilot settings file. Once attached, the remote surface can stream session activity, accept queued input, answer permission prompts, stop a session, and let the user steer work away from the original terminal.

[NOVA]: That changes the shape of CLI-agent work. The local terminal remains the execution anchor, but supervision can move. A builder can start a task at the desk, then check progress from mobile or a browser, answer a permission request, queue a correction, or stop the session without being in the same editor.

[ALLOY]: The constraints matter. The machine running the session still needs to stay online, and GitHub's docs call out keep-alive for longer work. Sessions are user-specific. Business and Enterprise use may depend on admin policies for remote control and CLI features. So this is not detached cloud compute. It is a live session with a remote control plane.

[NOVA]: That distinction is important. Remote steering is useful because it preserves the local context and lets supervision move. But it also means the local environment, branch state, credentials, network, and terminal session still matter. If the laptop sleeps, the session is not magically running somewhere else.

[ALLOY]: The second GitHub update is cheaper model selection for Copilot cloud agent tasks. Claude Haiku 4.5 and GPT-5.4-mini are available at a 0.33x multiplier for simpler work. That is the right product direction because agent tasks are not all equally hard.

[NOVA]: A small dependency bump, lint fix, typo correction, mechanical refactor, test expectation update, or straightforward failing test does not always need the strongest model. A cheaper model can handle the task while preserving budget for the jobs that need deeper reasoning: ambiguous bugs, architecture changes, security-sensitive patches, or multi-file behavior changes.

[ALLOY]: The entrypoints matter here too. GitHub says model selection is available from supported flows such as assigning an issue, mentioning Copilot in a pull request comment, starting from agent surfaces, GitHub Mobile, or Raycast. Where no picker exists, Auto is used.

[NOVA]: That means builders should treat model choice as part of task triage. If the entrypoint exposes a picker, choose deliberately. If the task is mechanical, use the smaller model. If it is design-heavy or risky, pay for the stronger path. If there is no picker and Auto is used, review the result with that uncertainty in mind.

[ALLOY]: The third change is one-click repair for failing GitHub Actions. From a workflow run logs page, Copilot Business and Enterprise subscribers can click Fix with Copilot. The cloud agent investigates the failure, pushes a fix to the branch, and tags the user for review.

[NOVA]: That is a strong agent entrypoint because the context bundle is strong: failing job logs, branch state, repository instructions, and a cloud development environment. Instead of copying logs into chat, the user delegates from the place where the failure is already visible.

[ALLOY]: But the review discipline does not go away. A branch fix pushed by an agent is still a code change. The reviewer has to check whether the agent fixed the real cause, preserved the design, avoided broad hacks, and did not simply optimize for green CI.

[NOVA]: That is especially true with Actions failures. The easiest fix might be loosening a test, skipping a case, pinning an old dependency, or changing CI configuration in a way that hides a bug. The right fix may be deeper. The agent can draft, but the human review still owns the engineering judgment.

[ALLOY]: The bigger product direction is clear. GitHub is turning Copilot agents into a work queue that spans surfaces. Local CLI sessions can be steered remotely. Cloud tasks can use smaller models when the work is simple. CI failures can become delegated repair jobs from the log page.

[NOVA]: For teams, the policy layer matters. Remote control, cloud agents, model selection, and Actions repair all need admin settings, repository instructions, and review norms. Without those, it is easy to create an agent queue that is convenient but inconsistent.

[ALLOY]: The useful build pattern is to classify tasks before assigning them. Simple branch maintenance can go to a cheaper cloud model. CI failure repair can start from the workflow logs. Work that depends on a developer's local state can stay in the CLI but be remotely supervised. Risky design work still needs stronger models and closer review.

[NOVA]: And the supervision surface should match the work. If the agent is asking for permissions, mobile approval can be enough for a simple known operation. If the change is broad, a desktop review is better. The point is not to make every agent task remote. It is to let the control plane move when that actually helps.

[ALLOY]: A useful team workflow is to route by cost and risk. Use the smaller cloud-agent models for narrow fixes with clear tests. Use stronger models when the issue has ambiguous behavior, security implications, or broad design impact. Use remote CLI steering when the task needs local state but the human cannot sit in the terminal. Use Actions repair when the failure context is already concentrated in CI logs.

[NOVA]: The review workflow should be just as explicit. For a cheap-model change, check whether the agent stayed inside the narrow task. For a remote CLI change, check the local diff and the command history. For an Actions repair, check whether the agent changed product code, tests, dependencies, or CI configuration. The fact that the agent came from a convenient entrypoint does not change the review standard.

[ALLOY]: That is why these GitHub updates fit with the release block. They are not only feature announcements. They are part of the same operational shift: agents need lifecycle control, policy gates, cost tiers, and better entrypoints from the places where work already happens. [PAUSE]

## [38:30-45:00] Anthropic gives Claude web search richer SEC filing data for cited financial agents

[NOVA]: Anthropic gives Claude web search richer SEC filing data for cited financial agents. The May 18 Claude Platform note is narrow, but it matters for any agent that summarizes earnings, compares public companies, drafts due diligence notes, or monitors risk disclosures.

[ALLOY]: The difference between a generic web result and filing-aware search is source quality. Financial research agents need to know whether they are looking at a 10-K, 10-Q, 8-K, proxy statement, registration statement, or another primary filing. They also need enough metadata to keep that citation attached after the model summarizes the claim.

[NOVA]: The failure mode is familiar. A model searches the web, finds a financial claim, summarizes it, and loses the boundary between primary filings, press releases, analyst commentary, and news articles. The final answer may sound confident, but the evidence chain is weak.

[ALLOY]: Richer SEC filing data helps the tool layer carry better evidence into the model context. It gives the application a better chance to preserve filing identity, filing type, date, company, source URL, cited text, and retrieval metadata. But the application has to keep that information. If it collapses everything into prose, the benefit disappears.

[NOVA]: The practical recommendation is to treat search results as evidence objects. Keep the URL, title, filing type, date, citation text, company identity, and retrieval timestamp. If the agent writes a memo, each material claim should point back to the filing and, when available, the section or excerpt. If the agent writes structured notes, the filing source should be a field, not a sentence buried in the middle.

[ALLOY]: That also changes evaluation. A financial research agent should not only be graded on whether the summary sounds plausible. It should be graded on whether claims are traceable to primary sources, whether secondary commentary is separated from filings, whether dates are preserved, and whether conflicting evidence is flagged instead of smoothed over.

[NOVA]: SEC filings are structured legal and financial artifacts. A 10-K risk factor is not the same as a quarterly operating update. An 8-K may announce a discrete event. A proxy statement may explain governance and compensation. If an agent flattens those into the company said, it loses the context that makes the claim useful.

[ALLOY]: For builder workflows, the design pattern is straightforward. The retrieval layer returns evidence. The reasoning layer can summarize and compare. The report layer must preserve citations. The storage layer should keep enough metadata that a later audit can reconstruct where a claim came from.

[NOVA]: That is especially important for downstream spreadsheets, investment notes, compliance reviews, and client-facing research. A beautiful summary with weak citations is a liability. A more structured summary with clear source fields is easier to trust, easier to review, and easier to correct.

[ALLOY]: The concrete build workflow is to keep evidence objects alive. When Claude web search returns a filing result, store the filing type, company, date, URL, cited text, and retrieval time next to the claim. When the agent drafts a comparison, carry those fields into the comparison table or memo. When the agent exports a report, include enough citation detail that a reviewer can open the source and verify the claim without rerunning the whole search.

[NOVA]: For financial agents, this also suggests a better failure workflow. If a claim has no primary filing source, label it as secondary commentary. If two filings appear to conflict, keep both citations and ask for review instead of smoothing the difference away. If a filing type is unclear, do not let the model guess. The agent should preserve uncertainty as state, because uncertainty is often the most important thing the user needs to see.

[ALLOY]: The same pattern applies outside finance, but finance makes the stakes obvious. Primary-source grounding is not a nice-to-have when a claim can affect a decision. Richer SEC filing data gives developers a better tool result; the application still has to preserve the grounding boundary all the way to the user.

[NOVA]: So the Anthropic update is small in surface area and large in implication. Better search metadata makes financial agents more auditable, but only if builders keep citations alive through the whole pipeline. [PAUSE]

## [45:00-48:00] Closing: upgrade priorities

[ALLOY]: The upgrade priority for OpenClaw is to test the changed host surfaces, not just install the release. Validate plugin init, build, and validation. Trigger browser modal handling. Inspect gateway restart readiness. Exercise HTTPS proxy trust if you need it. Try Android Talk Mode with interruption. Send media through Telegram topics and Discord voice. Test image handling and Codex app-server turns with images, sandboxed network, code mode, and restricted sender policy.

[NOVA]: For Codex, update and inspect the operating state. Check the TUI status line, service-tier commands, permissions, approval mode, workspace roots, unified mentions, marketplace and sharing commands, remote-control flows, configured remote environments, Python SDK turn routing, codex doctor, Windows sandbox cases if relevant, and app-server state recovery.

[ALLOY]: For Copilot, use cheaper cloud-agent models for simple repair work, keep remote sessions policy-gated, and review one-click Actions fixes as code changes rather than final answers. For Claude financial agents, preserve SEC filing metadata and citations as structured evidence, not just text.

[NOVA]: The thread through these updates is operational maturity. Hosts are making tool and channel contracts clearer. CLIs are exposing state and permissions. Remote agents are getting better control planes. Search tools are returning richer evidence. That is the work that makes agents easier to ship, debug, and trust.

[ALLOY]: Source links and episode notes are available at Toby On Fitness Tech dot com.

[NOVA]: That's AgentStack Daily. I'm NOVA.

[ALLOY]: And I'm ALLOY. We'll be back soon.
