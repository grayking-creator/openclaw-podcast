# AgentStack Daily EP056: OpenClaw, Codex, Claude Code, Hermes, Appshots, MCP Tunnels, and Agent News

[NOVA]: I'm NOVA.

[ALLOY]: And I'm ALLOY, and this is AgentStack Daily. OpenClaw v2026.5.20 is the first thing to care about today because it changes things an agent actually depends on: policy checks, safer secret loading, provider routing, cron delivery, subagent returns, voice context, and image-generation timeouts.

[NOVA]: Codex 0.133.0 and Claude Code 2.1.148 are in the same practical zone: goals, remote-control readiness, permission profiles, plugin inventory, lifecycle hooks, pinned background sessions, code review, MCP pagination, enterprise policy, Windows shell repairs, and a Bash fix that matters if your terminal suddenly forgot how exit codes work.

[ALLOY]: Hermes v2026.5.16 gets a real seat at the table too: PyPI install, local proxy, OAuth-backed providers, faster browser work, LSP diagnostics, file-change verification, messaging, handoff, video, and computer use. Then we move fast through Codex Appshots, Secure MCP tunnels, Google Agent Executor, GKE Agent Sandbox, Antigravity CLI, MagenticLite, Data Agent Kit, Gemini API-key hardening, and Copilot planning tools. The point is not to admire release names. The point is to know what to try next. [PAUSE]

## [00:00-10:00] OpenClaw Codex Claude Code Upgrade Path

[NOVA]: OpenClaw Codex Claude Code upgrade path makes the local agent stack easier to inspect.

[ALLOY]: Start with OpenClaw. This is not only a new version number. It changes the host layer around the agent. The bundled Policy plugin gives OpenClaw a real place to put policy-backed channel conformance checks, doctor lint findings, and opt-in workspace repair. That matters because agents are no longer only chat replies. They touch local tools, browser sessions, scheduled tasks, voice surfaces, providers, and external channels. A policy problem should not live as tribal memory. It should show up when you run a diagnostic.

[NOVA]: The most immediate action is to run `openclaw doctor` after upgrading and actually read the findings. Look for plaintext secret warnings, stale provider configuration, policy findings, and anything that says a channel or workspace does not match the expected shape. Then fix one item instead of letting the diagnostic become wallpaper.

[ALLOY]: Secret handling gets sharper too. Credential loaders that request symlink rejection now fail closed when a token path is symlinked. That sounds like a tiny security detail, but it is the kind of tiny detail that prevents a trusted credential reader from being quietly pointed somewhere else. The practical test is easy: know where your token files live, make sure they are not symlinks, and make sure the runtime fails instead of guessing when the path is wrong.

[NOVA]: Provider routing is another useful surface. xAI device-code OAuth helps headless or remote setups authorize without a localhost browser callback. OpenRouter provider routing policy is honored unless model or agent parameters override it. If you run more than one model provider, this is worth testing directly. Make one small model call where the provider route matters, then confirm the route was the one you intended. The problem to avoid is thinking you are testing one backend while another backend quietly handles the call.

[ALLOY]: Cron and subagent handoff get attention as well. Scheduled main-session work now has a cleaner lane so it does not block human chat as easily. Successful scheduled runs can deliver the preferred final assistant output even if diagnostic warnings trail behind. Subagent completion handoff is more resilient when the requester session is stale or dormant. The useful test is one scheduled task and one delegated task. Do they return to the right place? Does the final answer surface, or only the noise around it?

[NOVA]: The voice changes are practical too. Discord voice sessions can follow configured users into voice channels, and realtime voice instructions can include bounded identity and persona context. That does not mean throwing a whole profile into every voice session. It means a voice agent can carry enough stable context to behave consistently when the conversation moves from text to speech and back. Test this with one bounded voice use case before trusting it for a longer session.

[ALLOY]: Image generation gets a better default timeout. Dynamic image-generation calls now get a 120-second watchdog when no tighter timeout is set. That matters because image calls often take longer than text calls. A 30-second timeout can make a valid slow generation look broken. The action item is to test one image provider with the new timeout and confirm the UI or calling task reports slow progress instead of silently losing the result.

[NOVA]: Now Codex. The important change in the current CLI release is state. Goals are enabled by default with dedicated storage and progress tracking. A goal is useful because longer coding work needs a durable target. Without that target, a transcript can be full of good intentions and still drift. Try a task with a measurable end condition: fix one test, update one component, or produce one validated script. The goal should tell the agent where done lives.

[ALLOY]: `codex remote-control` also becomes a more believable tool. It waits for readiness, reports machine status, and keeps explicit start and stop behavior. That is important if Codex is part of a remote or desktop-control setup. A remote command should not leave you wondering whether the host is ready. Test it before you need it in anger: start the control path, wait for readiness, verify status, stop it, and make sure the stop is real.

[NOVA]: Permission profiles and plugin discovery are the other builder surfaces. Profiles get list APIs, inheritance, managed requirements files, runtime refresh, and stronger Windows sandbox integration. Plugin discovery shows installed versions, marketplace roots, and remote collection support. Extensions can observe subagent start and stop, tool execution, turn metadata, and async approvals. That means Codex is becoming something other tools can inspect and build around, not only something a person talks to.

[ALLOY]: Claude Code is the terminal-agent stability block. Pinned background sessions in `claude agents` stay alive when idle, restart in place to apply updates, and are shed under memory pressure only after non-pinned sessions. The old `simplify` command becomes `code-review`, and its job is clearer: find correctness bugs at a chosen effort level, with optional inline GitHub pull-request comments. That is much better than a vague cleanup command pretending to be review.

[NOVA]: The MCP pagination fix is easy to underestimate. If a server has more than one page of resources, templates, or prompts, the client should not act like page one is the whole universe. A missing tool often looks like a model failure, but the real bug is discovery. After upgrading, test an MCP server with enough resources to paginate and confirm the client sees everything it should.

[ALLOY]: Claude Code also tightens updater diagnostics, enterprise login policy, PowerShell behavior, background approvals, and Bash exit handling. The test set is direct: one pinned session, one code review on a real diff, one MCP inventory query, one permission reuse path, and one shell-heavy task. If those pass, this update has moved from release note to useful. [PAUSE]

[NOVA]: The build move is to stop treating these as separate toys. Pick one small agent workflow that crosses all three surfaces: OpenClaw starts the task, Codex edits or inspects something with a goal, and Claude Code reviews or checks a terminal diff. Keep it tiny. The value is seeing where state, permissions, routing, and tool discovery show up in the same job. If the workflow feels confusing, write down which surface caused the confusion. That answer tells you where to improve your setup before a larger task depends on it.

## [10:00-17:00] Hermes Agent Foundation Release Turns Subscriptions And Local Tools Into A Sharper Agent Bench

[NOVA]: Hermes Agent Foundation release turns subscriptions, local tools, and messaging into a sharper agent bench.

[ALLOY]: Hermes gets its own section because this release is not one little CLI polish pass. It is a giant "make the thing easier to install, easier to connect, faster to start, and less annoying to operate" release. That is a very listenable kind of news, because every agent stack eventually hits the same wall: the model is ready, the tools are scattered, the auth paths are weird, and the human is still doing tiny setup chores that should have disappeared two months ago.

[NOVA]: Start with install. Hermes is now a real PyPI package, so the entry path becomes `pip install hermes-agent` and then `hermes`. That sounds almost too simple to spend airtime on, but installation friction is product friction. If a tool requires a clone, a shell script, a local convention, and three half-remembered notes before it even opens, fewer people test it honestly. A clean package path means more people can put it on a fresh machine and see whether the agent loop is actually useful.

[ALLOY]: The next big piece is the local OpenAI-compatible proxy. Run `hermes proxy`, and tools that already know how to talk to an OpenAI-style endpoint can point at a local Hermes endpoint backed by whichever OAuth provider the user has signed into. The practical names are obvious: Codex CLI, Aider, Cline, Continue, custom scripts. The interesting idea is that a subscription-backed provider can become a local endpoint without every downstream tool needing a bespoke auth integration.

[NOVA]: That is where the fun starts for builders. Imagine Codex expecting an OpenAI-compatible API. Instead of inventing another secret path, you point it at the Hermes proxy and let Hermes handle provider auth. The test is simple: start the proxy, point one client at it, run a small request, and inspect which provider actually served it. Then stop the proxy and make sure the failure is clear. If it fails like a normal tool, you can build around it. If it fails like mist, keep it in the lab.

[ALLOY]: SuperGrok OAuth and the xAI path matter in the same way. The release lets Hermes use Grok through a signed-in account flow instead of treating every provider as a static API-key drawer. That gives the agent bench more provider variety, but it also raises a control question: which tools should be allowed to spend which subscription, and how do you know what happened after the fact?

[NOVA]: That is why the proxy test should include logging. Not a giant observability ceremony. Just enough evidence to answer: what client called, what provider answered, which model was used, and whether a credential boundary was crossed. Agent stacks get much less mysterious when "which backend did this?" has an answer.

[ALLOY]: Hermes also adds `x_search`, which is useful because agents often need current social or developer chatter but should not require a custom skill just to search X. Treat it as an evidence tool, not a gossip cannon. A good first use is narrow: find a release thread, a maintainer post, or a recent incident report, then cite the specific result back into the task. A bad use is letting the agent swim through social noise and call it research.

[NOVA]: Messaging is a big Hermes lane too. Microsoft Teams is wired end to end, LINE and SimpleX Chat arrive, native clarify buttons land for Telegram and Discord, and Discord history backfill is on by default. That last one is deceptively important. A chat agent joining a channel without recent context is like a person entering a meeting and immediately answering a question from twenty minutes ago. History backfill gives the agent a chance to know what is already on screen.

[ALLOY]: The action item there is not "connect every platform." Pick one channel and test one conversational control. Clarify buttons are a good one. Ask the agent to choose between two safe options and confirm that the buttons appear, the chosen answer reaches the run, and the transcript records the decision. That is a small test, but it proves the chat surface is more than text pasted into a void.

[NOVA]: Performance gets real numbers. Hermes says cold start drops by about nineteen seconds, and browser console evaluations get dramatically faster through a persistent Chrome DevTools connection. This matters because local agents are used in tiny loops. If every browser inspection takes a couple seconds, the agent feels sticky. If the same inspection is near instant, browser repair and page evidence become much more tolerable.

[ALLOY]: Try one browser inspection before and after the update. Ask Hermes to inspect a page, run one harmless JavaScript evaluation, and report the result. Do it twice. If the second run is faster because the connection stays warm, you have learned something useful. If it still feels slow, the bottleneck may be your browser profile, tool startup, network, or the page itself.

[NOVA]: The write-safety features are the part I would test immediately. Per-turn file mutation verification means the agent gets a footer after edits with what changed on disk. LSP semantic diagnostics on every write means the agent can see language-server errors before it blithely says the patch is done. These are the features that keep a confident agent from being confidently wrong about whether it actually edited the file it thinks it edited.

[ALLOY]: The quick trial is one small code edit. Tell Hermes to change a function with an obvious type expectation. Watch whether the file-change summary appears. Watch whether LSP diagnostics catch a mistake. Then ask the agent to correct it. This is not glamorous, but it is exactly the kind of loop that saves a builder from accepting a broken patch because the prose sounded finished.

[NOVA]: `/handoff` is another useful piece. It moves an active session to a different model, persona, or profile without dropping context. The right test is not a giant dramatic transfer. Start a small debugging session with a fast provider, then hand it to a deeper model for the final review. Check whether the target has the messages, the tool history, and the files it needs. If handoff works, you get a practical escalation path instead of starting over.

[ALLOY]: Hermes also expands computer use beyond Anthropic-only assumptions with the cua-driver backend, adds pluggable video generation, clickable terminal URLs, Zed ACP Registry integration, OpenRouter Pareto Code routing, optional skills, API approval events, and plugin-side LLM calls through `ctx.llm`. That is a lot, so do not try to digest it as a list. Pick two features that remove a current annoyance.

[NOVA]: My suggested Hermes bench test is five parts. One, install or update and run doctor. Two, start the local proxy and point one OpenAI-compatible tool at it. Three, run one browser inspection and confirm it is fast enough to tolerate. Four, make one file edit and watch LSP plus mutation verification. Five, use handoff or clarify buttons in a real chat surface. That is enough to know whether Hermes belongs in your daily stack or stays as a weekend experiment.

[ALLOY]: And if it fails one of those tests, that is still useful. A good bench does not only prove tools are shiny. It tells you which part is not ready: install, auth, proxy, browser, write safety, messaging, or handoff. That is how you turn a huge release into a useful decision instead of a feature avalanche. [PAUSE]

## [17:00-22:00] OpenAI Codex Appshots And Goal Mode

[NOVA]: OpenAI Codex Appshots and goal mode make visual product work less guessy.

[ALLOY]: Appshots are the most immediately useful Codex product update. In the macOS app, you can attach an app window to a Codex thread with a hotkey. The thread gets a screenshot and available text. That changes UI repair because the human no longer has to translate every visual problem into a long paragraph. The model can see the bad state, inspect the text layer, and connect the problem to a component, route, or style rule.

[NOVA]: The try-now version is one UI bug. Do not start with a huge redesign. Open an app state where something is visibly wrong: a clipped table, a misaligned button, a modal that feels cramped, a heading wrapping badly, or a sidebar state that does not match the page. Capture an Appshot. Give Codex one goal: fix that visible problem without changing the surrounding layout. Then run the page and capture the result again.

[ALLOY]: Goal mode is the other half. It is now generally available across the Codex app, IDE extension, and CLI. That matters because a goal is a portable definition of done. If the task starts in the desktop app and continues in an editor or command line, the target can stay attached to the work. The goal should be concrete: pass this test, remove this visual defect, generate this artifact, or update this API path without changing unrelated behavior.

[NOVA]: Browser annotations make feedback more specific. Styling requests often fail because the instruction is spatial: align this with that, reduce this gap, keep this label readable, make this icon weight match the button. Annotation support lets feedback point at the region instead of relying on vague prose. For frontend work, that can save several bad patches.

[ALLOY]: Read-only JavaScript context is a subtle safety improvement. It gives the agent a way to inspect page state without turning inspection into mutation. The right order is still observe, reason, edit, verify. If an agent jumps straight from seeing a page to mutating it, debugging gets muddy fast. Read-only inspection helps keep those phases separate.

[NOVA]: Locked computer use is useful, but it should be treated as continuity under supervision, not magic autonomy. Eligible Mac Computer Use users can keep Codex working remotely after the Mac locks. That is good for long local tasks, visual checks, or browser work that takes time. Before using it for serious work, test wake behavior, approvals, and recovery. A locked machine should not accidentally expand the agent's power.

[ALLOY]: The practical pattern is this: use Appshots for visual truth, goal mode for the target, annotations for exact feedback, read-only JavaScript for inspection, and locked computer use only after the approval path is boringly predictable. That is a better product loop than "describe the bug, hope the agent imagined the same page, then patch three files." [PAUSE]

[NOVA]: A good builder trial is a before-and-after issue. Capture the broken UI, ask Codex for the smallest fix, run the build, capture the repaired UI, and compare the two states. If the task changes more than the visible defect, reject it and narrow the goal. That keeps the workflow practical: visual evidence in, source change out, verification before trust. It also gives a reusable pattern for design QA, accessibility fixes, copy overflow, dashboard polish, and desktop-app support.

## [22:00-27:00] Secure MCP Tunnels

[NOVA]: Secure MCP tunnels turn private tools into reachable agent tools without opening inbound ports.

[ALLOY]: This is one of the most important infrastructure stories because it changes how private tools can participate in agent systems. OpenAI and Anthropic are both moving MCP tunnel patterns forward. The basic shape is outbound connectivity: a local or internal MCP server connects out through a tunnel, and an agent surface can reach it without exposing an inbound port to the public internet.

[NOVA]: The reason to care is simple. A lot of useful tools are private. They live on a laptop, inside a company network, behind a firewall, or attached to a local service. Without a tunnel, a team either cannot use them from a hosted agent surface or has to punch a hole through the network. An outbound tunnel gives a cleaner connectivity path.

[ALLOY]: But connectivity is not permission. That sentence is the whole risk. A tunnel can make a tool reachable, but it does not automatically decide who should use the tool, which methods are allowed, what data can leave, or which actions require approval. If the MCP server exposes powerful actions, the tunnel only makes the problem closer.

[NOVA]: The try-now exercise is to design one private MCP tool as if it were going live. Name the tool. Name the account or project that can reach it. List the methods the agent is allowed to call. Decide which calls are read-only and which are mutating. Decide whether mutating calls require human approval. Log each call with enough detail to audit it later. Then decide where the local secret lives and how it rotates.

[ALLOY]: That is not bureaucracy. It is the difference between "my agent can query an internal status service" and "my hosted agent can do anything my laptop MCP server exposes." The tunnel should be narrow. If a tool only needs to read issue metadata, do not give it a method that can rewrite the issue. If it only needs a staging database, do not point it at production. If it only needs a summary, do not return raw records by default.

[NOVA]: The best use cases are boring in a good way: internal search, local docs, build status, read-only dashboards, small deployment checks, a private calendar availability tool, or a source-of-truth inventory. Once those work, move carefully toward write actions. A write action through a private tunnel should feel like a small release, not like a casual convenience.

[ALLOY]: The takeaway is practical. Secure MCP tunnels make private tools easier to connect. They do not remove the need for identity, allowlists, audit logs, scoped secrets, and approval gates. Treat the tunnel as the pipe. Design the permission model around the tool. [PAUSE]

[NOVA]: The first build should be read-only. A useful starter workflow is an internal status lookup, a private documentation search, or a staging-health query. Make the tool return a small answer and a trace of what it checked. Then add one approval-gated write action later. That sequencing keeps the tunnel useful without making the first version scary. If a read-only tool cannot be scoped and audited cleanly, a write-capable tool is not ready.

## [27:00-32:00] Google Agent Executor

[NOVA]: Google Agent Executor makes long-running agents resumable instead of one-shot.

[ALLOY]: Agent Executor is interesting because it names the runtime layer that many agent demos skip. A serious agent run needs an event log, snapshots, reconnect and backfill, isolated actors, single-writer session state, and branchable trajectories. Those are not glamorous features. They are the things that make a long run recoverable.

[NOVA]: A one-shot prompt can live inside a chat transcript. A multi-hour agent task cannot. It may browse, call tools, create intermediate state, wait on a user, recover after a disconnect, and fork a strategy after a failure. If all of that lives only as model context, the run is fragile. When context is compacted, interrupted, or confused, the system loses the thread.

[ALLOY]: The event log is the first useful piece. It gives you a record of what happened in order: model decisions, tool calls, observations, approvals, errors, retries, and outputs. That matters when a run succeeds because you can explain how it got there. It matters even more when a run fails because you can identify which event was wrong instead of blaming the whole model.

[NOVA]: Snapshots solve a different problem. Long-running sessions need a way to pause and resume without replaying the entire world. A snapshot can capture state at a point in time, so the system can continue after reconnecting or recovering. That is important for browser agents, coding agents, data agents, and any task that has state outside the prompt.

[ALLOY]: Branching is useful for debugging and exploration. If an agent took a bad path, you do not always want to start from zero. You may want to branch from the last good point and try a different plan. That is closer to how developers debug code: find the last known good state, then test a smaller change.

[NOVA]: The action item is to map one existing agent task into this runtime shape. Pick a task that currently feels flaky. Ask five questions. What is the event stream? Where is durable state stored? How does the run resume after a disconnect? Can you branch from a failed step? What proof remains after the run finishes?

[ALLOY]: If you cannot answer those questions, the task may still work, but it is not yet an agent system you can trust. Agent Executor is useful because it pushes builders toward recoverable execution instead of heroic prompting. [PAUSE]

[NOVA]: A concrete builder exercise is to take a flaky task and write its run card. The card needs a start event, a list of tool events, an approval event if a human is involved, a success event, and a failure event that can be resumed. You do not need a full platform to learn from that. Even a simple local implementation gets better when the workflow has named events instead of one giant transcript. The moment you can resume from the last good event, the task stops being fragile theater and starts becoming software.

## [32:00-37:00] GKE Agent Sandbox And Agent Substrate

[NOVA]: GKE Agent Sandbox and Agent Substrate target the awkward shape of idle but stateful agents.

[ALLOY]: Normal server workloads usually do not look like agent workloads. A web service handles requests. A batch job runs and exits. An agent session may sit idle for a long time, wake up suddenly, need isolation, use tools, keep state, then go idle again. Multiply that by thousands or millions of sessions and ordinary scheduling starts to look clumsy.

[NOVA]: Google's GKE Agent Sandbox and Agent Substrate work is aimed at that shape. The pieces are warm pools, snapshots, gVisor isolation, actor scheduling, and worker multiplexing. The point is not just "run agents on Kubernetes." The point is to make isolated stateful sessions cheaper and faster to wake.

[ALLOY]: Warm pools help because a session can start from ready capacity instead of cold infrastructure. Snapshots help because idle state can be suspended and resumed. gVisor helps with isolation. Actor-to-worker mapping helps the platform carry many logical sessions across fewer active workers. The theme is not decorative; it is a response to the economics of agent sessions.

[NOVA]: The try-now version is a load-shape sketch. Before building an agent service, estimate how many sessions are active, how many are idle, how long they stay idle, what state must survive, what tools they can access, and how fast they must wake. If the workload is mostly idle but must resume quickly, warm pools and snapshots may matter more than raw model speed.

[ALLOY]: This also changes debugging. If an agent session moves across actors and workers, you need session identity, logs, snapshots, and tool-call traces that follow it. Otherwise a failure looks like the platform swallowed the run. Infrastructure for agents has to be observable at the session level, not only at the pod or process level.

[NOVA]: Coding agents and MCP servers are good examples. A coding agent may need a sandbox with a repository, dependencies, browser state, and a partial patch. An MCP server may need credentials and local context. If those pieces are expensive to recreate, the system needs a better idle and resume story.

[ALLOY]: The action is not "move every agent to GKE tomorrow." It is to recognize the workload shape. If your agent sessions are few and short, keep it simple. If they are many, isolated, idle, and stateful, start testing snapshot and warm-pool behavior before the platform gets expensive. [PAUSE]

[NOVA]: For a builder, the practical question is cost per useful session, not cost per container. If a workflow spends most of its life waiting for a user, a tool, or a scheduled wakeup, cold-start time and idle cost dominate the experience. Test a small pool with real session behavior: wake, inspect, call a tool, pause, resume, and finish. Then measure the user-facing delay and the debugging evidence left behind. That tells you whether the substrate helps the product or only makes the diagram look serious.

## [37:00-42:00] Google's Antigravity CLI Migration

[NOVA]: Google's Antigravity CLI migration is a real planning deadline for Gemini CLI users.

[ALLOY]: Google says Gemini CLI consumer and free usage stops serving requests on June 18, 2026, and Antigravity CLI becomes the new terminal surface. That is not just a brand change. It is a migration event for anyone who built habits, scripts, prompts, skills, or hooks around Gemini CLI.

[NOVA]: Google Antigravity CLI migration is the exact phrase to put on the calendar because this is not a vague future nudge. It is a dated terminal-surface change with existing scripts, auth flows, and habits attached to it.

[NOVA]: The important part is the harness direction. Antigravity is positioned around skills, hooks, subagents, plugins, async work, and shared context across CLI and desktop. That means the terminal agent is becoming less like a single prompt runner and more like a configured work environment.

[ALLOY]: The practical migration starts with inventory. List the Gemini CLI tasks you actually use. Not the ones you imagined using. The ones that run every week. For each one, record the auth path, model, config, files it reads, tools it calls, hooks it depends on, and what output proves success. Then run the highest-value task through the Antigravity path before the cutoff.

[NOVA]: Pay attention to consumer versus enterprise behavior. A personal CLI migration can be annoying. An enterprise migration can affect policy, login method, audit, and allowed providers. If a team has wrapper scripts around Gemini CLI, the wrapper should fail clearly when the old path stops serving requests. Silent fallback is the enemy here.

[ALLOY]: Skills and hooks need special care. A skill that works in one harness may assume a file layout, a permission model, a prompt shape, or a tool name that does not translate. A hook may fire at a different point in the task lifecycle. A subagent may inherit less context than expected. Test those assumptions directly.

[NOVA]: The next move is small. Pick one task. Move it. Record the differences. If the output changes, decide whether the new result is better, worse, or only different. If the tool calls change, decide whether that is acceptable. If auth changes, document the new setup while it is fresh.

[ALLOY]: The deadline is close enough that waiting is a bad plan. Migrations get easier when the first test happens while the old tool still works. [PAUSE]

[NOVA]: The best migration workflow is a parallel run. Keep the old Gemini CLI path as the reference while it still answers. Run the same build prompt through Antigravity. Compare not just the text response, but the tools used, approvals requested, artifacts changed, and time to a usable result. If Antigravity changes the shape of the task, that may be fine. What you want to avoid is discovering the difference after the old path has gone quiet.

## [42:00-47:00] Microsoft MagenticLite Shows A Small-Model Agent Path

[NOVA]: Microsoft MagenticLite shows how small-model computer-use agents can be useful when the harness is designed around them.

[ALLOY]: MagenticLite is interesting because it does not start from "give every task to the biggest model." Microsoft Foundry Labs is pairing a harness, an orchestrator, computer-use models, approvals, and sandboxing. MagenticBrain is based on Qwen three eight billion and trained inside the harness. Fara one point five handles computer-use tasks across four, nine, and twenty seven billion parameter variants.

[NOVA]: The key mechanism is co-design. The orchestrator sees the same kind of tool schemas during training and inference. That reduces the gap between benchmark behavior and product behavior. A lot of agent failures happen when a model learns one task format, then the product hands it a different tool shape, approval model, or browser state.

[ALLOY]: MagenticLite also uses Quicksand's QEMU sandbox for browser sessions and code execution. That matters because computer-use agents touch unknown pages, downloads, local content, and sometimes code. Running that work inside a resettable boundary is a better default than letting the agent roam the main desktop.

[NOVA]: The approval design is just as important as the model. A good computer-use agent should pause for login, submission, deletion, payment, account changes, or anything else that crosses from reversible navigation into consequence. It should not ask for approval on every harmless click. The system has to know which actions are sensitive.

[ALLOY]: The try-now question is not "can this replace a frontier coding model?" The question is "which repetitive computer-use tasks are narrow enough for a smaller orchestrator plus a specialized browser model?" Candidates include checking a dashboard, filling a draft form, collecting page evidence, navigating a known web tool, organizing local artifacts in a sandbox, or running a visual demo.

[NOVA]: The economics matter. If every click calls the most expensive model, many useful automations never become affordable. A smaller orchestrator can make high-frequency tasks plausible if reliability stays high enough. Harness-faithful training is the bet: shape the environment so the smaller model has fewer surprises.

[ALLOY]: The evaluation should be practical. Can it recover when a page changes? Can a human take over? Can it explain why it delegated to a browser model? Can the sandbox reset cleanly? Does it pause at the right moments? Does it finish the boring task without turning the human into a supervisor for every step?

[NOVA]: That is the useful lens for MagenticLite. Small models are not magic. But small models inside a careful harness may be exactly right for a slice of computer-use work. [PAUSE]

[ALLOY]: A strong first use case is something repetitive with obvious success: gather three facts from a known web tool, fill a draft form without submitting it, check a dashboard for a status change, or prepare a local report inside a sandbox. Those are buildable workflows because the goal is visible and the risk is bounded. Do not begin with payments, account changes, production deletes, or ambiguous research. Start where the smaller model can win by being cheap, fast, and predictable.

## [47:00-51:00] Google Data Agent Kit

[NOVA]: Google Data Agent Kit packages data access as configured agent tools instead of pasted schema.

[ALLOY]: This story matters because data work is one of the places where agents can become useful quickly and dangerous quickly. Google Data Agent Kit brings data skills and MCP-style tools into developer-agent surfaces including Codex, Claude Code, Gemini CLI, VS Code, and Antigravity. The sources include BigQuery, AlloyDB, Spanner, and Cloud Storage.

[NOVA]: The useful shift is from pasted context to configured access. Pasting schema, sample rows, and credentials into a prompt is fragile. It can be stale, too broad, and hard to audit. A configured data tool can have scope, credentials, validation, and a repeatable interface.

[ALLOY]: The action item is to scope the data agent before giving it power. What can it read? What can it write? Which datasets are off limits? Can it run expensive queries? Does it need row-level security? Should it return raw data, summaries, or query plans? Who reviews a generated query before it touches production?

[NOVA]: Query optimization and validation skills are useful because a data agent can otherwise be confidently expensive. A bad query is not only wrong; it can be slow, costly, and noisy. The agent should be able to explain the tables it is using, the filters it applied, and the validation it performed.

[ALLOY]: Drift and governance checks are another good fit. If a dashboard changes, a schema drifts, or a pipeline starts producing unexpected values, an agent can help investigate. But again, access scope matters. A data agent should not get broad write access just because it can explain a chart.

[NOVA]: The practical first build is read-only. Give the agent one dataset, one question type, and one validation requirement. Make it produce the query, the answer, and the evidence. Then decide whether write actions belong in the system at all. [PAUSE]

[ALLOY]: The workflow gets stronger when the agent has to show its work in machine-checkable pieces. Ask for the query, the result, the validation check, and the confidence limits separately. If the query is expensive, require an estimate before execution. If the answer affects a decision, require the source table and filter logic. That makes the data agent useful for builders because it can speed analysis without hiding the parts that need review.

## [51:00-55:00] Google's Gemini API-Key Warning

[NOVA]: Google's Gemini API-key warning gives agent builders a security task they can do today.

[ALLOY]: Google is blunt about the premise: Gemini API keys are standard Google API keys, and API keys are open secrets. Treat them as paid bearer tokens. If they land in a browser client, a generated repo, a public demo, or an untrusted extension, the risk is not theoretical. It can become unexpected usage and billing.

[NOVA]: Gemini API-key guidance is useful because it turns security from a foggy scolding into a finite errand.

[NOVA]: The first fix is isolation. Create keys in standalone projects instead of mixing every experiment into a production project. Then add API restrictions so the key can call only the intended service, such as the Gemini API. If a leaked key can call more services than the app needs, the blast radius is bigger than necessary.

[ALLOY]: Application restrictions are next. A key can be restricted by website, IP range, iOS bundle identifier, or Android package and certificate pair. Because a key uses one application restriction type, separate application shapes should get separate keys. A browser app, server process, iOS app, and Android app should not share one all-purpose string.

[NOVA]: Server-side keys belong in a secret store such as Secret Manager or an equivalent system. They should not be baked into visible client code. A generated sample that calls a paid model API directly from a public browser client is a draft, not a deployable pattern.

[ALLOY]: Monitoring closes the loop. Use Cloud Asset Inventory or key listing to know what exists. Watch request-count metrics by credential ID. If a key spreads, rotate it and recreate the replacement with the same restrictions. Do not rotate from one loose key to another loose key.

[NOVA]: The try-now task is straightforward. Pick one Gemini key. Confirm the project. Confirm API restrictions. Confirm application restrictions. Confirm where it is stored. Confirm how usage is monitored. Confirm how to rotate it. If any answer is "not sure," that is the next fix. [PAUSE]

[ALLOY]: This is also a generated-app problem. A builder may ask an agent to scaffold a demo, and the demo may casually put a paid key in client-side code. The safe workflow is to put the model call behind a server route, read the secret from the server environment, return only the needed result to the browser, and document how the key is restricted. That is not fancy security engineering. That is the minimum path from prototype to something you can share without inviting a billing mess.

## [55:00-59:00] Copilot Auto And Semantic Issue Search

[NOVA]: Copilot Auto and semantic issue search make planning and model routing part of the coding agent surface.

[ALLOY]: Copilot Auto now routes based on task signals while respecting admin policy and showing which model was selected. That is useful for everyday work because not every task needs the heaviest reasoning model. A short explanation, a small edit, or a first-pass diagnosis may be better served by something faster or cheaper.

[NOVA]: GitHub Copilot Auto is the model-routing side, and semantic issue search is the context side. Put them together and bug work starts with better evidence.

[NOVA]: The tradeoff is reproducibility. If model choice changes based on task classification, availability, reliability, subscription, or policy, two runs of the same prompt may not be comparable. For low-risk work, that may be fine. For migrations, security fixes, production patches, or incident reproduction, log the model or pin it.

[ALLOY]: Semantic issue search is the more actionable Copilot feature for teams. It lets Copilot Chat find related issues by meaning, not only exact text or labels. That can change the order of coding work. Instead of throwing a repository at an agent and asking it to fix a vague complaint, first ask for related issues grouped by symptom, platform, failure mode, or release area.

[NOVA]: The try-now pattern is: search first, edit second. Ask for the cluster of related issues. Ask what failure modes repeat. Pick one narrow cluster. Then hand that narrowed task to a coding agent with the relevant issue links and a success condition. That gives the agent better context and reduces the chance that it fixes the loudest symptom while missing the actual pattern.

[ALLOY]: Admin policy matters here too. If an organization disables certain models or sets routing rules, the agent surface should respect that. Model routing is now part of developer tooling governance. It is not only a personal preference.

[NOVA]: The practical habit is to treat model choice and issue retrieval as evidence. Which model answered? Which issues were considered? Which cluster was selected? What test proves the fix? That is enough trace to make coding-agent work less mysterious. [PAUSE]

[ALLOY]: A good team workflow is to make semantic issue search the first step of bug work. Search the symptom, group the related reports, choose one cluster, and only then ask the coding agent for a patch. For low-risk edits, Copilot Auto can pick the model. For high-risk edits, pin or log the model. That keeps speed for daily work and traceability for changes that might need to be reproduced later.

## [59:00-62:00] What To Try Next

[ALLOY]: Pull this together and the next queue is clear. Upgrade OpenClaw, Codex, and Claude Code, then test the changed surfaces instead of only printing versions. For OpenClaw: policy findings, secret symlink rejection, provider routing, cron output, subagent completion, voice handoff, and image timeout behavior.

[NOVA]: For Codex: one Appshot, one goal-driven task, one remote-control readiness check, one permission-profile inspection, one plugin inventory check, and one lifecycle event you would actually log. For Claude Code: one pinned background session, one code review on a real diff, one paginated MCP server, and one shell-heavy task.

[ALLOY]: For the broader news: design one MCP tunnel with permissions before connectivity, sketch durable state for one long-running agent, estimate whether one agent service is mostly idle and stateful, migrate one Gemini CLI task toward Antigravity, try one small-model computer-use task inside a sandbox, scope one read-only data agent, lock down one Gemini key, and use semantic issue search before editing.

[NOVA]: The bar is not "did the model say something clever." The bar is whether the system is observable, scoped, recoverable, and useful enough to run twice. The good news today is that more of the agent stack is exposing the pieces needed to get there.

[ALLOY]: The best way to make this actionable is to choose one build workflow for tomorrow, not ten at once. For example: take a UI bug, capture it with Appshots, set a Codex goal, patch it, and verify the result. Or take a private status tool, expose it through a read-only MCP tunnel, and log each call. Or take a flaky long-running agent task, write the event sequence, and decide where resume should happen. A small working build teaches more than a giant plan.

[NOVA]: And keep each workflow honest. It should have a trigger, a narrow permission boundary, a success condition, a failure condition, and one verification step. That applies whether the workflow is a data-agent query, a small-model browser task, a Copilot issue triage, or an OpenClaw cron job. If the agent cannot tell you what it did, what it used, and what changed, the build is not ready for daily use.

[ALLOY]: One more practical filter: pick the workflow that removes the most repeated annoyance. If a human keeps rechecking the same dashboard, make that the small-model browser task. If a team keeps asking the same database question, make that the read-only data agent. If a coding agent keeps missing issue context, make semantic issue search the intake step. The news matters because it gives builders better handles on problems they already have, and better ways to ship without guessing.

[NOVA]: Extra builder picks are worth a quick final scan too: feature flags for AI behavior, image efficiency work, and edge-model benchmarks. Add one kill switch around a prompt or config change, benchmark one image path for latency and cost, or test one local model on the actual device instead of assuming desktop numbers transfer.

[ALLOY]: Source links are on the episode page this week right now. That is AgentStack Daily. I'm ALLOY.

[NOVA]: And I'm NOVA. We'll be back soon. Toby On Fitness Tech dot com. [PAUSE]
