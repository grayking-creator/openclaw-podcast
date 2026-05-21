# AgentStack Daily EP056: OpenClaw, Claude Code, Secure MCP, and Agent Runtimes

[NOVA]: I'm NOVA.

[ALLOY]: And I'm ALLOY, and this is AgentStack Daily. Today starts with the release block: OpenClaw v2026.5.19 and Claude Code CLI 2.1.146. The OpenClaw release changes the surfaces that decide whether agents can run cleanly across runtimes, build local images, inspect browsers, load plugins, trust proxies, and deliver replies back to the right place. The Claude Code release is smaller, but it fixes several sharp edges in background sessions, MCP pagination, managed policies, Windows launch paths, and child-agent model propagation.

[NOVA]: Then we move through the infrastructure layer around agents. OpenAI released Secure MCP Tunnel for private tools. Google introduced Agent Executor as an open-source runtime for resumable distributed agents. GKE Agent Sandbox reached general availability, with Agent Substrate pointing at denser agent scheduling. GitHub Copilot added task-aware Auto routing and semantic issue search. And Google Cloud published Data Agent Kit for data skills, MCP tools, and plugins inside coding environments.

[ALLOY]: The useful question through all of this is concrete. What changed? Which mechanism is new? Why would a builder care? And what should be tested before anyone trusts it in a real stack?

[NOVA]: So we will stay close to the moving parts: image-build knobs, browser modal handling, typed plugin manifests, MCP tunnel identity, event logs, pod snapshots, model routing signals, semantic issue indexes, and data connectors with real governance boundaries. [PAUSE]

## [00:00-17:30] Release block: OpenClaw runtime surfaces and Claude Code background-agent fixes

[NOVA]: Release block first: the new OpenClaw and Claude Code updates. Start with OpenClaw, because this release lands on the host surfaces around agent work, not just the model conversation.

[ALLOY]: The runtime floor is now Node.js twenty two point nineteen. That is worth saying plainly because agent hosts tend to accumulate local machines, small servers, containers, CI jobs, and remote nodes. A runtime floor is not cosmetic. It decides which installs can upgrade, which images need rebuilding, and which operators have to move before the new toolchain is usable.

[NOVA]: The local image-build path gets more runtime-neutral too. OpenClaw adds OPENCLAW_IMAGE_APT_PACKAGES and OPENCLAW_IMAGE_PIP_PACKAGES, while the older Docker-specific apt variable stays as a fallback. That matters if your agent environment is not only Docker. If you build with Docker today and Podman tomorrow, the package knobs should describe the OpenClaw image, not the container brand.

[ALLOY]: That is a small naming change with real operational value. Agents that run code often need system packages, Python packages, debugging tools, browser dependencies, or project-specific binaries. If those dependencies are not declared through a stable image-build surface, they leak into local setup notes, one-off shell history, or fragile post-start commands. The new package variables make the build contract easier to reproduce.

[NOVA]: Browser automation also gets a more explicit modal story. Snapshots can surface pending and recently handled dialogs. Actions can report that they were blocked by a dialog. The browser dialog command can answer a pending modal by dialog ID. And browser evaluate now accepts a timeout budget for longer page functions.

[ALLOY]: That is a reliability feature for real web work. Browser agents fail in boring ways: an alert blocks a click, a confirm dialog steals focus, a long page-side function times out, or the agent thinks a button is broken when the actual problem is a modal it did not observe. Surfacing pending dialogs in the browser state gives the agent a reason for the blockage instead of a mystery failure.

[NOVA]: The dialog ID also matters. If a page can have more than one modal event over time, a command that answers the current dialog implicitly can be risky. A targeted dialog ID lets the automation say which pending prompt it is handling. That makes tests, browser repair steps, and human-visible logs less ambiguous.

[ALLOY]: OpenClaw's plugin surface moves forward as well. The release adds defineToolPlugin, plus plugin build, validate, and init commands. The important part is typed simple tool plugins with generated manifest metadata, optional tool declarations, and context factories. That gives plugin authors a cleaner path from code to a manifest the runtime can inspect.

[NOVA]: Plugin manifests are not paperwork. In an agent host, the manifest is part of the trust and routing surface. It tells the system what exists, what can be called, and how the tool should be represented. If manifest generation and validation are close to the plugin code, builders are less likely to ship stale metadata or hand-maintained declarations that drift from implementation.

[ALLOY]: Codex sessions inside OpenClaw get a visible control path too. Slash commands can list, enable, and disable Codex plugins from the session. That turns plugin management from config editing into an interactive surface the operator can inspect while the work is happening.

[NOVA]: That is useful because plugin state affects behavior. If a session can use a filesystem helper, a browser helper, a project skill, or a custom MCP bridge, the person supervising the agent needs to see what is active. Being able to toggle plugins from the session makes plugin state easier to reason about without leaving the agent context.

[ALLOY]: Skills can also install or update into shared managed skill storage with a global flag. That is another host-level change. Some skills are project-local and should stay local. Others are shared team or machine capabilities. Having a managed global path reduces repeated setup, but it also means teams should be deliberate about what becomes globally available.

[NOVA]: The release includes a set of new and renamed skills too: debugging, diagrams, spike work, meme creation, Obsidian, Python debugging, and an autoreview naming cleanup. The bigger point is that OpenClaw is treating skills as part of the runtime surface, not just prompt snippets. Installation scope, naming, and discoverability all matter once skills are used by multiple agents.

[ALLOY]: Operator visibility gets a lot of attention. Gateway restart traces now attribute startup probe, config, runtime, and resource-count costs. Startup logging overlaps plugin-service startup and channel sidecars while preserving readiness gating. So the host can do more work in parallel without claiming the service is ready before the important sidecars are actually ready.

[NOVA]: That distinction matters in production. Faster startup logs are nice. False readiness is not. If the gateway accepts traffic while plugins or channel sidecars are still missing, agents can lose messages, fail tool calls, or route replies into a half-started system. The release seems aimed at making startup both faster and more honest.

[ALLOY]: Config changes also get more legible. Config tools can distinguish restart-required fields, hot-reloadable fields, and no-op edits before applying changes. That is exactly the kind of surface an operator needs when changing a live agent host. The question is not only, can I edit this setting? It is, will this setting interrupt running work?

[NOVA]: Proxy trust gets a concrete improvement. Managed forward proxies can use HTTPS endpoints and scoped CA trust through a proxy TLS CA file. For enterprise or private-network deployments, that matters. Agents often need outbound access through a proxy, and if the trust story is ad hoc, people end up disabling verification or baking private trust material into the wrong layer.

[ALLOY]: Scoped CA trust is cleaner. The proxy can be trusted for the path that needs it without turning the whole runtime into a loose certificate environment. Builders should test this with the exact proxy chain they use, because TLS errors in agent hosts can show up as model failures, tool failures, package-install failures, or browser failures depending on where the request originated.

[NOVA]: QA-Lab gets runtime parity coverage. The release adds parity scenarios, runtime-tool fixtures, and blocking drift checks for Codex-native workspace tools versus OpenClaw dynamic tools. That is a strong signal about where agent platforms are now: the same conceptual tool may run through multiple runtimes, and drift between those paths becomes a real bug.

[ALLOY]: Parity is not glamorous, but it is the difference between a feature that works in the demo path and a feature that works where users actually run it. If a workspace read, a plugin call, or a browser action behaves differently depending on whether it came through the Codex-native path or the OpenClaw dynamic tool path, the model may learn the wrong behavior and the operator may debug the wrong layer.

[NOVA]: The fixes list is broad, but several are useful to call out. Memory search now scans the JavaScript fallback vector path in bounded batches, so large chunk tables cannot pin the Node main thread for seconds. DeepSeek tool schemas with anyOf and oneOf unions are normalized before requests. Claude model rows keep native image capability even if local catalog data is stale.

[ALLOY]: Each of those maps to a failure mode builders recognize. A main thread stall makes the whole host feel unreliable. Schema unions can break tool calls against providers that expect a narrower shape. Stale catalog data can hide a model capability that the provider actually supports. These are not headline features, but they reduce confusing runtime behavior.

[NOVA]: Browser evaluate and highlight routes now enforce current-tab URL allowlists. That is a security boundary. If browser tooling is allowed only on a certain page or domain, a current-tab check helps prevent the agent from carrying an action into a different page after navigation or focus drift.

[ALLOY]: Channel delivery fixes show up too. Telegram forum topics get topic-aware inbound serialization and follow-up routing. Discord, Slack, WebChat, text-to-speech, generated media, outbound registry lookup, direct-message replies, and Codex app-server handoffs all receive fixes that reduce duplicate replies, lost thread context, or stuck tool state.

[NOVA]: That is the unglamorous part of agent infrastructure that users feel immediately. If an agent answers in the wrong thread, drops a follow-up, repeats itself, or leaves a tool call stuck, the model quality does not matter. The conversation contract broke.

[ALLOY]: Now Claude Code. The visible command change is that simplify becomes code-review, with an optional effort level. The rename is clearer. It tells the user this command is about reviewing code, not generally making something shorter.

[NOVA]: The more important behavior fix is Auto mode and AskUserQuestion. Auto mode now stops suppressing AskUserQuestion when the user or a skill explicitly relies on it. That matters because agent autonomy still needs intentional human checkpoints. If a skill says this decision should be asked, the runtime should not silently turn that into a guess because Auto mode is active.

[ALLOY]: MCP pagination is repaired for resources list, resource templates list, and prompts list. That is a protocol correctness fix with a large blast radius. MCP servers can paginate, and if a client only sees page one, the agent's tool universe is incomplete. It may miss prompts, miss resources, miss templates, or conclude a server cannot do something it actually exposed on a later page.

[NOVA]: Child-agent model propagation gets fixed too. CLAUDE_CODE_SUBAGENT_MODEL is forwarded to child processes in multi-agent sessions. If a parent session deliberately sets a subagent model, that choice needs to survive the process boundary. Otherwise delegated work can quietly run on a different model than the operator intended.

[ALLOY]: Managed settings enforcement is hardened around forceLoginOrgUUID and forceLoginMethod. The release closes gaps involving third-party-provider and API-key sessions. For enterprises, this is a governance fix. If an organization requires a certain login method or organization identity, a local runtime cannot treat alternate provider paths as a way around that requirement.

[NOVA]: Background sessions also stop re-prompting for tool permissions that were granted with don't ask again. That is a quality-of-life fix, but it is also a background-agent reliability fix. If a long-running session is supposed to continue after a permission has been permanently granted, repeated prompts can stall work that the operator believed was already cleared.

[ALLOY]: The Windows fixes matter because mixed fleets are normal. PowerShell invocations installed through winget or the Microsoft Store stop failing with command-line invalid errors. Background worktree cleanup no longer follows NTFS junctions into the main repo. Attached background sessions stop flashing in Windows Terminal. GNOME Terminal paste handling is repaired too, which helps the Linux desktop side.

[NOVA]: There are also fixes for auto-updater retries, large-diff rendering, SDK streaming cleanup, full-screen theme dialogs, and background handling when the only typed input is a skill or custom slash command. The theme across the release is not one huge capability. It is fewer broken edges around background work, policy, MCP discovery, and terminal environments.

[ALLOY]: The upgrade test list is concrete. For OpenClaw, test modal browser flows, long browser evaluations, local image builds, plugin creation and validation, Codex plugin toggles, config reload metadata, runtime parity checks, proxy TLS trust, and one real channel reply path. For Claude Code, test code-review, Auto-mode questions, MCP pagination against a server with multiple pages, managed-login policy enforcement, background permissions, child-model propagation, and Windows launch behavior if Windows is in your fleet. [PAUSE]

[NOVA]: The larger release takeaway is that both projects are tightening the runtime around the agent. OpenClaw is improving the host: plugins, browser state, config, proxy trust, delivery, and parity. Claude Code is improving session behavior: questions, pagination, policies, background permissions, and process inheritance.

[ALLOY]: That is what mature agent tooling looks like. The interesting work is not only making the model smarter. It is making the surrounding system less ambiguous when something runs for an hour, calls private tools, delegates work, changes files, and has to report back through the right channel.

[NOVA]: A concrete builder use case is a support tool that can inspect a customer-facing web page, run a browser action, call an internal diagnostic plugin, and reply inside the original support thread. That build depends on modal handling, plugin manifests, proxy trust, and channel routing all behaving together. If any one of those surfaces is vague, the whole tool feels unreliable.

[ALLOY]: Another use case is a repo-maintenance agent that runs overnight. It may need a custom image build, a shared skill, a scoped plugin, a managed proxy, and a background Claude Code session with the intended child model. That is not exotic anymore. It is the kind of deploy pattern teams reach for when they want agents to handle dependency updates, flaky-test triage, or documentation drift without babysitting every turn.

[NOVA]: The useful build standard is evidence. Can the host tell you which config fields require restart? Can the browser state tell you why an action is blocked? Can plugin validation catch a bad manifest before deploy? Can the child agent prove it inherited the selected model? Can a real channel reply land once, in the right thread, with the right context?

[ALLOY]: Those are builder-facing questions, not abstract platform questions. They decide whether a team can ship an agent task as part of a product or whether it remains a local demo that only works when the original developer is watching the terminal.

[NOVA]: That is also where the build decision becomes clearer: if the tool can be deployed, observed, and repaired by someone other than its author, it is ready for a wider use case.

## [17:30-27:00] OpenAI Secure MCP Tunnel gives private tools an outbound-only path

[NOVA]: OpenAI Secure MCP Tunnel is a connectivity and security release for enterprise tool use. The problem is familiar: ChatGPT, Codex, the Responses API, or AgentKit needs to use an MCP server that lives inside a private network. Publishing that server directly to the internet is often the wrong answer.

[ALLOY]: Secure MCP Tunnel flips the direction of the connection. A tunnel client runs inside the network that can already reach the private MCP server. That client opens outbound HTTPS to OpenAI, or to the mTLS endpoint when mutual TLS is configured. It then long-polls for queued MCP work.

[NOVA]: The request path stays recognizable. OpenAI-hosted tunnel endpoints receive MCP requests from supported products, queue JSON-RPC work, and the tunnel client forwards each request to the private MCP server. Responses travel back through the same outbound path.

[ALLOY]: The security model changes because the private MCP server does not need an inbound public listener. The enterprise review surface becomes tunnel identity, endpoint configuration, outbound egress policy, local MCP server authorization, logging, and optional mTLS. That is a different review than opening a new internet-facing service.

[NOVA]: For builders, the important part is that OpenAI products can see something shaped like a normal MCP endpoint while the actual server stays behind the local network boundary. That is useful for internal source-control metadata, issue systems, deployment controls, compliance lookup, data catalogs, package registries, incident systems, or other tools that should not become public connectors.

[ALLOY]: It also reduces the temptation to use brittle workarounds. Without a supported tunnel, teams reach for reverse proxies, temporary tunnels, shared credentials, or copy-pasted internal context. Those approaches can work for a demo, but they are hard to govern. A managed outbound tunnel gives security teams a smaller object to reason about.

[NOVA]: The tunnel does not make tool access magically safe. A private tool is still powerful once an agent can call it. The policy questions move to scopes, approvals, audit logs, output filtering, and whether the tool itself checks the identity and permissions it should check.

[ALLOY]: That last point is important. The tunnel protects connectivity shape. It does not replace application authorization. If the private MCP server exposes deploy, delete, export, or customer-data operations, those operations still need their own controls. The tunnel should not be treated as a universal trust grant.

[NOVA]: The first useful test is narrow. Put one low-risk internal MCP server behind the tunnel. Confirm the tunnel identity. Confirm outbound-only network behavior. Confirm the OpenAI surface can list and call the expected tool. Then inspect logs from both sides: the OpenAI-facing tunnel path and the internal MCP server.

[ALLOY]: The second test is failure behavior. Stop the local MCP server. Break local authorization. Deny an outbound connection. Rotate a credential. The tunnel should fail in a way an operator can understand. For enterprise connectors, clean failure states are as important as clean success states.

[NOVA]: Secure MCP Tunnel is a sign that private tools are becoming first-class agent infrastructure. The next stage is not only, can the model call a tool? It is, can the organization connect private tools without exposing the network, while preserving identity, policy, logs, and reviewable boundaries?

[ALLOY]: That is the right direction. Internal tools are where a lot of valuable agent work lives, but internal tools are also where sloppy connectivity can become a real incident. Outbound-only MCP access is a better starting point than asking every team to publish a private server to the public internet. [PAUSE]

## [27:00-36:00] Google Agent Executor makes durable execution a runtime primitive

[NOVA]: Google Agent Executor, or AX, is an open-source runtime for durable, distributed agent execution. It is aimed at the fact that serious agent work is not a single request. It is a session with state, tool calls, pauses, reconnects, possible human confirmations, and recovery after something fails.

[ALLOY]: AX puts a controller, event log, registry, remote agents, tools, skills, and environments behind a runtime that can record execution state and resume from it. The central mechanism is durable execution through event logs and snapshots.

[NOVA]: Event logs matter because they make the session reconstructable. If a client disconnects, the runtime can reconnect and backfill responses from the last sequence the client saw. If a worker fails, the runtime has a record of what happened before the failure. If a human approval pauses the run, the session does not have to be treated as a lost request.

[ALLOY]: Snapshots give the runtime a recovery point. A long-running agent may build up files, environment state, intermediate decisions, tool outputs, or branch choices. Without a snapshot or event trail, resuming that work means asking the model to infer state from a transcript. That is weaker than letting the runtime preserve the execution history.

[NOVA]: AX also uses a single-writer architecture for session consistency. That is one of those details that sounds like database plumbing until you imagine multiple actors touching one agent session. A controller, tool actor, client stream, and remote agent cannot all write shared state casually without creating races. A single writer gives the session an authority for ordered changes.

[ALLOY]: The reconnect behavior is also a product feature, not just infrastructure. If a client reconnects and says, I last saw sequence one hundred, the runtime can backfill from there. That makes an agent session feel continuous across network drops, browser refreshes, or client restarts. For long work, that continuity is part of usability.

[NOVA]: AX describes isolated actors for controllers, tools, skills, agents, and environments. That gives the runtime places to enforce policy and audit. If an agent asks for a tool call, the system can record who requested it, which actor executed it, what the response was, and which policy boundary applied.

[ALLOY]: Trajectory branching is another interesting piece. Branching from checkpoints lets an agent test different paths without losing the original context. For example, one branch might try a conservative fix, another branch might try a larger refactor, and the runtime can keep those trajectories anchored to the same prior state.

[NOVA]: Google positions AX as a federation layer too. It is meant to work with custom agents, Google-managed agents, Agent2Agent Protocol, Agent Development Kit, LangChain, LangGraph, MCP servers, and custom compute. The point is not that every builder should standardize on it immediately. The point is that runtime concerns are becoming portable concepts.

[ALLOY]: Those concepts are now familiar: event logs, snapshots, resumable streams, isolated actors, policy points, audit trails, and state consistency. If an agent platform does not have answers for those, it is hard to trust it for work that spans more than one prompt.

[NOVA]: The caution is maturity. Early runtime standards can change, and AX notes that resumption protocols may shift before stable release. Builders should treat it as a serious signal and a useful codebase to study, not as something to wire into a critical production path without watching the churn.

[ALLOY]: The practical evaluation is to run a small sample that disconnects and reconnects, then inspect whether responses backfill cleanly. Add a tool call, a pause, and a failure. Look at what the event log records. Look at what can be audited. Look at how much state the runtime actually preserves versus how much the model has to reconstruct from text.

[NOVA]: AX is important because it names the execution layer. Models and tools get most of the attention, but the runtime decides whether long-running work can resume, branch, recover, and be audited. That is the layer that turns an agent from a clever conversation into a system component.

[ALLOY]: And once agents become system components, durable execution is not optional. It is the difference between a session that can survive ordinary failure and a session that has to start over whenever the network blinks. [PAUSE]

## [36:00-45:00] GKE Agent Sandbox and Agent Substrate target dense, low-latency agent sessions

[NOVA]: GKE Agent Sandbox is now generally available, and the details are more interesting than the GA label. Google is targeting a specific workload shape: agent sessions that need isolation, can sit idle, and then need to wake up quickly.

[ALLOY]: Normal request serving is not quite the right model for that. An agent may execute code, wait for a model response, wait for a person, wait for an external system, then run again. Keeping every session hot wastes compute. Starting cold every time adds latency. Agent Sandbox tries to split the difference with pod snapshots, warm pools, standby capacity buffers, and a Sandbox API.

[NOVA]: Pod snapshots let idle workloads suspend and resume in seconds. Warm pools keep ready capacity available. Standby capacity buffers use suspended virtual machines to refill those pools at lower cost. Google says the integrated warm pool can allocate three hundred sandboxes per second per cluster, with most allocations completing in two hundred milliseconds.

[ALLOY]: Those numbers matter because user-facing agent loops are latency sensitive. If a code-running agent needs a sandbox and allocation takes many seconds every time, the product starts to feel broken. If the sandbox can appear in a few hundred milliseconds, isolated execution becomes much easier to put in the interactive path.

[NOVA]: Isolation is central. The stack includes gVisor, default-deny Kubernetes network policy, and pluggable interfaces for runtimes like Kata Containers. That is aimed at the dangerous part of code-using agents. They may run generated code, dependency installs, test commands, data transforms, or user-provided scripts. The platform has to contain that work without making every action feel slow.

[ALLOY]: Default-deny network policy is worth calling out. A sandbox that can run code but can also reach everything by default is not a comfortable security boundary. The useful posture is to start closed, then allow only the egress and services the task actually needs.

[NOVA]: Agent Substrate points at the scaling layer beneath ordinary Kubernetes scheduling. It maps many stateful actors onto a smaller set of ready worker pods, based on the fact that agent-like applications are often idle. It manages actor lifecycle, suspend and resume, worker assignment, and traffic routing while keeping the Kubernetes control plane out of the critical path for some activations.

[ALLOY]: That is a different mental model from one pod per active thing forever. If each long-running agent session owns a full warm pod while doing nothing most of the time, utilization is poor. If too much goes through the Kubernetes scheduler at wake-up time, latency suffers. Substrate is trying to multiplex actors onto workers so idle state is cheap and activation is fast.

[NOVA]: The builder decision is not, should every team adopt this tomorrow? It is, where does your workload sit? If you have a few internal agents running occasional tasks, normal containers may be enough. If you need many isolated, stateful, mostly idle sessions that wake up under interactive latency, the usual pod model starts to strain.

[ALLOY]: Testing should be specific. Measure cold allocation, warm allocation, snapshot suspend, snapshot resume, and network policy behavior. Run generated code that tries to reach something it should not reach. Confirm the denial is visible. Then measure what happens under burst: how many sessions wake up, how quickly, and what the cost looks like when they go idle again.

[NOVA]: The security choice between gVisor and Kata-style isolation depends on threat model and performance. gVisor gives a userspace kernel boundary with different tradeoffs. Kata leans toward lightweight virtual machines. The important thing is that agent code execution should have a stated isolation choice, not a vague promise that a container is probably fine.

[ALLOY]: GKE Agent Sandbox is the productized path for Kubernetes teams. Agent Substrate is the open-source direction for denser scheduling. Together they say something about where the market is going: agent infrastructure is no longer just API calls and job queues. It is becoming session scheduling, state parking, fast activation, and containment for code that cannot be blindly trusted.

[NOVA]: That is the real shift. Agents create bursts of activity around long stretches of waiting. Infrastructure that treats them like ordinary stateless web requests will either waste capacity or feel slow. The new platform work is about making isolated sessions cheap while idle and quick when needed. [PAUSE]

## [45:00-52:00] GitHub Copilot Auto routing and semantic issue search change coding-agent defaults

[NOVA]: GitHub Copilot added task-aware Auto model routing in VS Code. Auto model selection is not new as an idea, but this update makes the routing criteria more explicit.

[ALLOY]: Copilot Auto now weighs real-time model availability and reliability, then evaluates the task along dimensions such as reasoning demand, code-generation complexity, bug-diagnosis difficulty, and tool-orchestration needs. It honors admin model policies, shows which model was used, and routes around natural cache boundaries to avoid unnecessary cache costs.

[NOVA]: Billing follows the selected model, with Auto currently limited to models in the zero to one times multiplier range and a discount when it uses a billable model. That is relevant because model routing is also cost routing. If an assistant chooses the model, administrators need to understand how that choice appears in usage and budget planning.

[ALLOY]: The upside is throughput. Not every coding task needs a heavyweight reasoning model. Explanation, light edits, routine generation, and small bug triage can often use a cheaper or faster model. A routing layer can keep the developer moving while reserving stronger models for tasks that need them.

[NOVA]: The tradeoff is reproducibility. If the selected model changes based on health, availability, subscription, policy, task classification, or cache boundaries, then two runs of the same prompt may not be comparable. That matters for evaluations, incident reproduction, sensitive migrations, and any task where the team needs to know exactly what produced the result.

[ALLOY]: The practical default is split. Use Auto for ordinary daily coding where speed and reliability matter. Pin the model when you are running an evaluation, debugging a regression in agent behavior, doing a sensitive refactor, or comparing outputs over time.

[NOVA]: GitHub also added semantic issue search in Copilot Chat on the web. Instead of exact title or keyword matching, Copilot can use a semantic issues index to find, group, and analyze related issues from natural-language queries.

[ALLOY]: That helps because issue triage often starts fuzzy. Someone remembers the Windows terminal paste bug, the quota-reset complaint, the stale badge problem, or the reports about a broken login redirect. The exact issue title may not contain those words. Semantic retrieval can find nearby reports without forcing the user to know the repository's naming habits.

[NOVA]: For maintenance agents, this is useful as a planning surface. An agent can ask for related issues, group themes, identify duplicates, and propose a triage order. But semantic search should not be treated as the source of truth. Before a coding agent starts work, it still needs to verify against the actual issue text, reproduction steps, labels, and repository state.

[ALLOY]: That is the right boundary. Semantic search accelerates discovery. It does not replace evidence. A natural-language match can be related but not actionable, or it can group issues that share symptoms but have different causes. The agent should use it to find candidates, then read the sources before changing code.

[NOVA]: The combined GitHub story is that defaults are getting smarter. Copilot can choose a model for the task, and Copilot Chat can search issues by meaning instead of exact words. Both are useful. Both also require visibility. Builders need to know which model ran and which issues were actually used as evidence.

[ALLOY]: That visibility is what keeps convenience from turning into mystery. Auto routing is good when it is observable. Semantic retrieval is good when it leads back to concrete issues. In coding-agent systems, the best convenience features leave a trail that humans and automation can inspect. [PAUSE]

## [52:00-58:30] Google Cloud Data Agent Kit brings data skills and MCP tools into coding surfaces

[NOVA]: Google Cloud Data Agent Kit is aimed at a different bottleneck: agents that need enterprise data context without a giant manual prompt. The kit brings data engineering and data science skills, MCP tools, and plugins into VS Code, Claude Code, Codex, Gemini CLI, and Antigravity CLI.

[ALLOY]: The concrete pieces are skills, connectors, and plugins. Skills codify data tasks such as query optimization, machine-learning best practices, data validation, drift checks, governance, and troubleshooting. MCP tools connect agent work to systems like BigQuery, AlloyDB, Spanner, and Cloud Storage. Plugins put those capabilities into the local developer surface.

[NOVA]: The context-window benefit is obvious. Without a kit like this, a data task often begins with pasted schema snippets, query examples, governance rules, table descriptions, cost warnings, and troubleshooting notes. That is slow, error-prone, and easy to lose between sessions. A configured connector and a reusable skill can provide the agent with grounded context through a repeatable path.

[ALLOY]: Natural-language-to-SQL is part of the story, but the more important piece is grounding. A model can generate SQL from a prompt. A useful data agent needs to know the actual dataset shape, project boundaries, engine choice, governance constraints, and validation expectations. Data Agent Kit tries to package those into the agent environment instead of relying on the user to remember all of it.

[NOVA]: Google also describes intelligent routing between compute engines. BigQuery may be the right path for SQL-native analytics and ELT. Spark may be the right path for custom Python transformations or distributed machine-learning training. A data agent that can help choose between those paths is more useful than one that only writes a query.

[ALLOY]: The risk is access scope. A coding agent with broad data-estate visibility can do valuable work, but it also becomes a sensitive access point. Governance, lineage, authorization, query cost, data export rules, and audit logging cannot be afterthoughts. If a connector can see too much, the agent can accidentally summarize, transform, or expose too much.

[NOVA]: The first deployment should be narrow. One project. One dataset or small group of datasets. Read-only access. A clear query-cost limit. A skill that encodes a known validation path. Then test whether the agent can answer useful questions, generate safe SQL, explain cost, and respect the boundaries.

[ALLOY]: Troubleshooting should be part of the test. Ask the agent to diagnose a failed query, a schema mismatch, a drift warning, or a bad join. The value of data skills is not only happy-path generation. It is whether the agent can follow the organization's preferred checks when the result looks suspicious.

[NOVA]: Data Agent Kit is interesting because it makes data work feel less like pasting context into a chat and more like giving the agent a governed workbench. The agent has tools, skills, connectors, and local IDE context. That is the shape serious data-agent work needs.

[ALLOY]: But the permission model has to be serious too. The safest version is not an agent with every dataset and every write permission. It is a scoped assistant that can inspect the right metadata, run bounded queries, apply reusable validation skills, and leave an audit trail a data team can review. [PAUSE]

## [58:30-64:00] What to test next

[NOVA]: Pull the episode together and the test list is practical. For OpenClaw, confirm Node twenty two point nineteen is available, validate local image package variables, run a browser modal path, run a long browser evaluation with an explicit timeout, create or validate a simple tool plugin, toggle a Codex plugin from a session, inspect config reload metadata, test proxy TLS trust, and run the runtime parity checks that match your deployment.

[ALLOY]: For Claude Code, test code-review, Auto-mode questions, MCP pagination beyond page one, managed-login policy enforcement, background permissions, child-process model propagation, and Windows launch paths if your team has Windows machines.

[NOVA]: For Secure MCP Tunnel, start with one low-risk private MCP server. Confirm outbound-only connectivity, tunnel identity, local authorization, audit logs, and clean failure behavior. Do not begin with the most powerful internal tool.

[ALLOY]: For Agent Executor, test disconnect and reconnect, response backfill, snapshots, one tool call, one pause, and one failure. Read the event trail and ask whether it is enough to debug and audit the run.

[NOVA]: For GKE Agent Sandbox and Agent Substrate, measure cold allocation, warm allocation, suspend, resume, network denial, burst activation, and idle cost. The point is not the announcement. The point is whether isolated sessions feel fast enough and contained enough for your workload.

[ALLOY]: For Copilot, use Auto routing for ordinary work, pin models for reproducible evaluations, and verify which model was used. Use semantic issue search for discovery, then read the actual issues before treating them as work orders.

[NOVA]: For Data Agent Kit, start with one scoped read-only connector, one codified data skill, one validation path, and a clear cost boundary. Test query generation, query explanation, drift or validation checks, and failure diagnosis before widening access.

[ALLOY]: The bigger takeaway is that agent stacks are becoming infrastructure. The new work is about runtime floors, plugin contracts, modal state, private tool tunnels, event logs, resumable sessions, sandbox pools, model routing, issue retrieval, and governed data access. Those are the pieces that decide whether agents can move from useful demos into systems people can operate.

[NOVA]: Source links are in the episode notes. That is AgentStack Daily. I'm NOVA.

[ALLOY]: And I'm ALLOY. We'll be back soon. Toby On Fitness Tech dot com. [PAUSE]
