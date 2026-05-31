# AgentStack Daily EP060 - Claude Code Latest, Codex Windows Control, Runtime Instructions, and Local Agent Memory

[NOVA]: I'm NOVA.  
[ALLOY]: I'm ALLOY, and this is AgentStack Daily...

[NOVA]: Today we’re staying in one lane the entire time: control surfaces. Not vibes, not “AI is getting smarter,” but the practical levers that decide what an agent can do, where it can do it, and how you can supervise it when a run goes sideways.

[ALLOY]: The release and product news up front is narrowly scoped but operationally important. Claude Code latest adds auto mode support on managed cloud providers—Bedrock, Vertex, and Foundry—when you explicitly enable it with an environment flag. OpenAI’s Codex app update adds Windows computer use and remote supervision from mobile or Mac while the Windows host keeps your repo and runtime local, plus faster in-app browser behavior and a new Codex Profiles surface for usage and token activity.

[NOVA]: Then we move into a developer-facing API change from Anthropic that’s quietly powerful: the Messages API now accepts system entries inside the messages array, which means your harness can update runtime instructions mid-run without masquerading as the user, and without turning your prompt into a constantly growing blob.

[ALLOY]: And the project radar is a single theme with four angles: architectural memory you can query, agent memory that decays so it doesn’t become stale authority, local-only coding agents that make private iteration cheap, and graph-backed repair loops that force evidence into the fix. Let’s get into it. [PAUSE]

## [00:00] Opening: releases, control surfaces, and memory

[NOVA]: The through-line in EP060 is that “agent capability” is starting to look less like a single model choice and more like a stack of explicit contracts.

[ALLOY]: Contract one is execution location. If the agent is acting inside a managed cloud provider environment, that changes identity, logging, data residency, and the audit trail you can get after the fact. Contract two is host boundaries. If the agent is controlling a Windows desktop, you need to know whether the files and shell live on the remote host or were copied into some other environment. Contract three is instruction ownership. If your harness can’t update the system contract mid-run, the model ends up guessing what changed.

[NOVA]: And contract four is memory. A lot of teams talk about “agent memory” as if the answer is to keep every transcript forever and re-inject it. In practice, that approach tends to create a new failure mode: stale guidance gets treated as current policy, and irrelevant details crowd out the few facts you actually needed.

[ALLOY]: So the point of today’s set is to show the stack getting more explicit. Auto mode is gated behind an environment flag so it can be tested deliberately. Windows computer use keeps local context on the host while supervision becomes mobile. System entries inside message arrays separate “what the user wants” from “what the runtime allows right now.” And the memory tools we’re covering are mostly about structure and freshness rather than raw accumulation.

[NOVA]: If you’ve had an agent fail in the last month, you probably didn’t lose because the model couldn’t write code. You lost because the run didn’t have the right guardrails, the right evidence, or the right ability to update assumptions when something changed.

[ALLOY]: With that frame, let’s start with the front-of-episode release and product block. [PAUSE]

## [03:00] Claude Code latest and Codex Windows control

[NOVA]: First item: Claude Code latest adds auto mode support on Bedrock, Vertex, and Foundry for Opus 4.7 and Opus 4.8, but only when you set `CLAUDE_CODE_ENABLE_AUTO_MODE=1`.

[ALLOY]: Two important details are hiding inside that seemingly small sentence. One is that it’s not “auto mode is now everywhere.” It’s “auto mode exists in more provider lanes, and you must opt in.” The other is that the provider lanes matter as much as the feature itself, because auto mode is fundamentally a permission and routing surface.

[NOVA]: Let’s unpack auto mode in practical terms. In a coding agent, there’s a spectrum of actions: reading files, searching, running tests, installing dependencies, starting a dev server, editing code, pushing commits, opening PRs, and so on. “Auto mode” is the label for the system deciding that certain steps can be executed automatically without stopping for a human confirmation on each step.

[ALLOY]: That’s not just a convenience toggle. It changes the risk profile of the agent run. If your agent can run commands automatically, the “safety boundary” is no longer only the model. It’s the combination of model behavior, the harness policy, the tool permissions, the sandbox, and the provider environment where those tool calls happen.

[NOVA]: And that’s where the managed cloud lanes come in. Bedrock, Vertex, and Foundry are common paths when a team wants model access with cloud-native identity and compliance. In those environments, there’s often a strong preference that requests and logs stay inside a particular cloud boundary, tied to organizational credentials, with access policies you can enforce centrally.

[ALLOY]: So auto mode being supported there means you can evaluate automatic action behavior under the same IAM and audit reality as production. If you test auto mode only in a local developer workstation flow and then deploy in a managed cloud context, you’re changing a lot of the surrounding system at the same time—identity, networking, logging, and sometimes even filesystem access patterns.

[NOVA]: The explicit environment variable gate is the other key point. If you’re operating a team toolchain, you usually don’t want a surprise where an update changes behavior from “ask before you do stuff” to “do stuff.” Opt-in gating forces an intentional activation point.

[ALLOY]: That gating also gives you a clean testing strategy. You can run the same tasks with and without auto mode and compare outcomes: number of tool calls, number of destructive actions attempted, whether the agent escalates properly when it’s uncertain, and whether it obeys “no writes” or “no network” constraints when those are in effect.

[NOVA]: Here’s a concrete way to test this without making your repo the experiment. Pick a small, disposable project or a known safe branch. Define three task categories.

[ALLOY]: Category one: read-only tasks. Ask the agent to produce an architectural summary, identify entry points, list the integration tests, and point out any obvious dependency hazards. In auto mode, you want to see it do file reads and searches efficiently without inventing tool calls it doesn’t need.

[NOVA]: Category two: safe execution tasks. Let it run the test suite, start the dev server, or run a linter—things that are mostly reversible and don’t mutate much. Your check here is whether the agent chooses commands that are appropriate for the project and environment. For example, does it try `npm test` in a repo that’s clearly Python? Does it notice `pnpm-lock` and use `pnpm`? Does it run the minimal test subset for a narrow change?

[ALLOY]: Category three: write tasks with strict guardrails. Give it a small change, like updating a function signature and updating call sites, or adding a missing null check. Your harness should still prevent anything you consider high risk—like pushing, publishing packages, changing secrets files, or modifying deployment manifests—unless you explicitly approve.

[NOVA]: The point is to measure whether auto mode reduces friction on the tasks you want it to accelerate, without silently increasing risk. The environment variable makes it easy to run A/B trials and to keep production behavior pinned until you’re satisfied.

[ALLOY]: Now, the larger product story: OpenAI’s May 29 Codex app update. There are four practical changes called out in the notes we’re using: Windows computer use, remote control from mobile or Mac while Windows remains host, improvements to in-app browser speed and stability, and Codex Profiles with identity, activity, usage stats, and token activity.

[NOVA]: Start with Windows computer use. “Computer use” is the category where the agent can see a desktop UI and interact with it: clicking buttons, typing into fields, switching windows, and navigating apps that aren’t neatly wrapped in an API.

[ALLOY]: On Windows specifically, that matters for a lot of real dev workflows. There are Windows-native app stacks, enterprise internal tools, and a huge amount of “the only way to do this is to click through the GUI” work. Think installers, proprietary admin consoles, credential managers, and certain IDE or debugger flows.

[NOVA]: But the core operational question with any computer-use product is: where does execution happen, and where do files live? The update’s boundary is explicit. You can supervise from iOS, Android, or Mac, but the Windows machine remains the host for project files, shell, app server, and local context.

[ALLOY]: That boundary has a few consequences worth calling out. First, it reduces data duplication. The repo doesn’t have to be copied to a remote environment just so the agent can run. Second, it reduces latency in the “run the server, check the browser, tweak code, rerun tests” loop because the runtime is local to the files.

[NOVA]: Third, it changes the trust model. Your supervision device is more like a remote control and monitoring surface, not the place where the work actually executes. That’s useful because it means you can step away from the desk and still steer the session, but you’re not accidentally moving the whole operation into a different security boundary.

[ALLOY]: The risk to understand is that computer use is, by design, broad authority. If the agent can click and type, it can potentially do anything you can do in that environment, including actions that are hard to roll back. So the recommended approach is: test it on a low-risk application before you depend on it for important work.

[NOVA]: Low-risk here means a project that can be reset, doesn’t touch production credentials, and won’t cause damage if it runs an unexpected command. A good initial target is a sample web app, a local-only demo service, or a repo you can discard.

[ALLOY]: The first test is simply reliability: can it consistently interact with common developer UI states? Things like: a terminal window that needs focus, a UAC prompt, a browser with multiple tabs, an editor that pops up “file changed on disk,” a test runner that requires scrolling to see failures.

[NOVA]: The second test is bounded intent. Give it a task that has a clear end condition, like “run tests and tell me the first failing test name and error.” You want to see whether the agent stays on task or gets distracted by side paths, like updating dependencies or reformatting code that wasn’t requested.

[ALLOY]: The third test is recovery. Intentionally create small disruptions: kill the dev server, disconnect the network briefly, cause a build failure by changing a config, or open a modal dialog. Then watch whether the agent notices it’s stuck, reports the issue, and asks for guidance when it hits a boundary it can’t cross.

[NOVA]: Now, the in-app browser improvements. In agent workflows, the browser is not “just a browser.” It’s often the verification surface. It’s where you confirm the fix actually works, where you reproduce the bug, where you inspect network calls, and where you validate UI flows.

[ALLOY]: If the in-app browser is slow or unstable, the agent’s verification loop degrades. That leads to one of the worst failure patterns in automated coding: the agent claims a fix is correct because it can’t reliably run the last step that would disprove it.

[NOVA]: So “faster and more stable in-app browser behavior” might sound like a product polish line, but it directly impacts how trustworthy the agent’s completion claims are. A stable browser path means the agent can re-run the repro steps and actually observe the outcome.

[ALLOY]: The final Codex update item is Codex Profiles: identity, activity over time, profile details, usage stats, and token activity. This is a control surface in the simplest sense: inspectability.

[NOVA]: In long-running sessions, you need to answer questions like: which profile ran this task, what was the usage footprint, and does token consumption match what you expected? If you’re supervising remote work across devices, you also want to confirm identity and activity traces, especially if multiple people share a Windows host.

[ALLOY]: Token activity as an exposed surface matters for debugging. If an agent run suddenly costs more, the cause is often not “the model got worse.” It’s something like: it’s repeatedly reading the same large files, it’s re-summarizing too much history, it’s stuck in a loop of failing tests, or it’s calling tools with huge outputs.

[NOVA]: A profile surface that makes that visible is the difference between “this feels expensive” and “we can see which workflow step ballooned tokens.” And once you can see it, you can fix it: add a file-size cap, add log truncation, add a more structured memory retrieval step, or tighten the verification plan.

[ALLOY]: Put those two front stories together—Claude Code auto mode on managed cloud lanes and Codex Windows computer use with remote supervision—and you get a single theme: agent work is becoming less tied to a single machine and more tied to explicit governance points.

[NOVA]: Auto mode on Bedrock, Vertex, and Foundry is about bringing policy-based automation into enterprise cloud environments. Codex remote supervision is about letting a human steer from anywhere while keeping execution local to the host that has the repo and the running app.

[ALLOY]: The recommended move is not “turn everything on.” It’s to treat both as controlled experiments. Explicitly gate auto mode, test it with safe tasks, and measure behavior. Try Windows computer use in a disposable environment, and only then decide what scope of real work you trust it with.

[NOVA]: Next, we’ll talk about a change that’s less visible to end users but is extremely visible to harness builders: runtime instructions that can be updated as system entries mid-run. [PAUSE]

## [13:00] Runtime instructions become editable state

[ALLOY]: Anthropic’s Opus 4.8 announcement included a developer-facing change that matters even if you never switch models: the Messages API now accepts system entries inside the messages array.

[NOVA]: That sounds subtle, so here’s why it changes how you build agents. Historically, a lot of harnesses treat “system prompt” as a fixed blob set at the beginning of the run. Then everything else—user messages, tool outputs, observations—gets appended in a sequence.

[ALLOY]: But real agent runs are not static. Permissions change. Budgets change. The environment changes. The harness learns new facts that the model must obey. And if you can’t update the system contract cleanly, you end up with awkward patterns.

[NOVA]: Pattern one is forcing the update through a user turn. That pollutes the audit trail, because it makes it look like the user asked for policy changes when actually the runtime is adapting to state.

[ALLOY]: Pattern two is stuffing new policy notes into a growing system prompt and re-sending the whole thing. That increases cost, increases context pressure, and in practice can break caching optimizations because the “prefix” keeps changing.

[NOVA]: Pattern three is asking the model to infer changed state from logs. That works until it doesn’t. If the model misses a log line, it will continue operating as if nothing changed—like it still has permission to write files, or it still has network access, or it still has enough budget to run a full test suite.

[ALLOY]: System entries inside the messages array give the harness a more precise tool: you can insert or append a system-role message that says, effectively, “the contract is now different,” without pretending the user said it.

[NOVA]: And that allows separation of concerns. The user lane can remain a clean record of intent, approvals, and clarifications. The system lane can remain the runtime’s authoritative statement of constraints: allowed tools, environment details, budget, and operational rules.

[ALLOY]: Let’s make this concrete. Imagine a coding agent run where you start with broad permissions. The agent is allowed to read files, run tests, and write changes in a branch. Mid-run, the harness detects that it is in a protected repo state—maybe it accidentally opened a production worktree, or the branch policy changes, or the agent is now operating on a directory marked sensitive.

[NOVA]: With editable system entries, the harness can inject a new system message: “Writes are now disabled. You may only propose diffs and ask for approval.” That is much cleaner than telling the model in a user message or hoping it figures it out.

[ALLOY]: Another common scenario: token budget. Some harnesses allocate a budget per job or per phase. Early in the run, you might allow exploration. Later, once the agent has a plan, you might tighten the budget so it focuses on execution.

[NOVA]: With system entries, you can update the instruction: “Remaining budget is now low. Prioritize minimal file reads, run targeted tests only, and summarize before acting.” The key is that it’s an instruction update tied to runtime state, not a user preference that might get mixed up with the task.

[ALLOY]: Environment context is another one. Suppose the harness detects that the sandbox switched from a full dev container to a restricted environment with no network. Or it detects that a dependency cache is empty, so installs will be slow. Or it discovers that the repo uses a monorepo tool that requires a particular command sequence.

[NOVA]: You can inject those as system facts. That means the model doesn’t have to rediscover them each time, and it doesn’t have to guess based on partial observations.

[ALLOY]: Now, one of the notes’ key claims is prompt-cache preservation. In long sessions, caching matters because the most expensive part of repeated calls is often the repeated “prefix”—the stable instructions, repo orientation, and high-level context.

[NOVA]: If your harness can append system messages as discrete entries instead of rewriting the entire system prompt, you can keep a large stable prefix unchanged. That improves the effectiveness of caching strategies, and it reduces the pressure to compress everything into a single mega-instruction at the start.

[ALLOY]: Even without explicit caching, it helps with clarity. Instead of one giant system prompt that includes a dozen historical updates, you can have a timeline of system messages: initial contract, then updates as conditions change.

[NOVA]: But there’s a discipline required here. If you use system entries carelessly, you can create conflicting system instructions. For example: initial system says “You may write to the repo,” later system says “Writes are disabled,” later again system says “Writes are allowed for files under /docs.” If you don’t define precedence, the model might try to satisfy all of them at once.

[ALLOY]: So the harness should treat system entries like state updates with a clear “latest wins” or a clearly scoped override. It’s often helpful to write system entries in a structured way, even if they’re still plain text.

[NOVA]: For instance, you can include a small section header format inside the system message: “Permissions: read yes, write no, network no.” “Budget: remaining tokens low.” “Execution: run tests allowed, installs not allowed.” The goal is to make it easy for the model to reconcile the current state.

[ALLOY]: You also want to keep machine-generated system updates distinct from human-authored system policy. A good pattern is: one initial system message for your permanent policy and safety rules, then subsequent system messages that are purely “runtime facts.”

[NOVA]: Runtime facts might include: current branch name, whether the working tree is clean, what tests last ran and their results, whether the agent has already tried a fix and it failed, which tools are currently available, and whether the environment is sandboxed.

[ALLOY]: That last piece—tool availability—is one of the biggest day-to-day failure points in agent stacks. An agent thinks it can do something because it did it earlier in the run, but then a tool gets revoked or a permission changes, and it keeps attempting the same call.

[NOVA]: A system entry update can close that gap immediately. If the harness revokes network access, it can inject: “Network tool calls are now disallowed.” Then the model should stop trying `curl`, package installs that require downloads, or remote API calls.

[ALLOY]: There’s another subtle advantage: auditable separation. When you later review a run, you can distinguish between what the user requested and what the runtime imposed. That matters for compliance, but it also matters for debugging. If a run behaved strangely, you can see whether a runtime constraint forced it down a weird path.

[NOVA]: In agent operations, that’s the difference between “the model made a bad choice” and “the harness changed the rules and the model complied.” Those are different problems with different fixes.

[ALLOY]: Suggested test for harness builders: implement a mid-run permission flip and verify the model responds correctly. Start a run where writes are allowed. Let the model propose or even begin edits. Then inject a system entry that disables writes and ask it to continue.

[NOVA]: You’re looking for a few behaviors. One: does it stop attempting write actions and switch to planning or diff proposals? Two: does it acknowledge the change in constraints explicitly? Three: does it attempt workaround behavior, like encoding file contents into the chat as a “suggested patch” rather than using tools?

[ALLOY]: If you see workaround behavior, you may need to strengthen your policy language. The goal isn’t to stop the model from being helpful; it’s to keep the contract real. “No writes” should mean no writes, even if the model believes it has the perfect fix.

[NOVA]: Another recommended test: budget tightening. Let the agent begin an exploration phase, then inject a system entry that sets a strict budget and a priority list. Then see if it actually narrows its tool calls: fewer files, smaller diffs, targeted tests.

[ALLOY]: If it doesn’t, that’s a sign you need to make the budget instruction more concrete. Models respond better to operational constraints when you specify what to do instead. For example: “Read only the files you already referenced. Run only the single failing test. Summarize changes in five bullets before making edits.”

[NOVA]: Tie this back to the earlier release story. Claude Code auto mode and Codex remote supervision are both about making the execution surface more capable. As you widen that surface, the ability to update runtime constraints mid-run becomes mandatory. Otherwise you’re running a more powerful agent with a brittle contract.

[ALLOY]: Next we’ll go to the project radar, starting with two complementary memory tools: OpenLore for architectural orientation, and Mnemo for persistent memory with decay. [PAUSE]

## [21:00] OpenLore and Mnemo: memory with structure and freshness

[NOVA]: Project radar item one is OpenLore. The simplest way to describe it is: a local architectural memory layer for coding agents that becomes queryable through MCP.

[ALLOY]: The core premise is that agents waste context on rediscovering project structure. Even strong coding agents often start a session by reading a directory tree, scanning README files, searching for entry points, grepping for function names, and assembling a mental map from scratch.

[NOVA]: That’s not only expensive in tokens and time. It’s also error-prone. If the agent misidentifies an entry point, it can build an entire plan on the wrong assumption—like editing a legacy service instead of the current one, or modifying a shared library when the change belongs in an adapter layer.

[ALLOY]: OpenLore attacks this by indexing the codebase into structured artifacts: static analysis outputs, call graphs, architectural clusters, “living specs,” and drift detection. Then it exposes MCP tools such as orientation and graph expansion so an agent can ask for a compact digest first, and only expand what it needs.

[NOVA]: Let’s break down why call graphs and clusters matter. A call graph is the map of which functions or modules call which others. When an agent is tasked with “fix a bug in checkout totals,” it’s not enough to find the file named `checkout.ts`. You need to know where the totals are computed, who consumes that result, and which paths are exercised by which flows.

[ALLOY]: If you have a call graph, you can ask questions like: “What are the upstream callers of this function?” and “What are the downstream effects if I change this return type?” That’s exactly the kind of question that reduces accidental breakage.

[NOVA]: Architectural clusters are a higher-level concept: grouping files or modules into subsystems. Many repos look flat to a naïve search. You might have twenty directories that all contain “service” code, but only a few are relevant to the task. Clustering helps an agent avoid exploring irrelevant neighborhoods of the repo.

[ALLOY]: “Living specs” are particularly useful for agent workflows because code changes, but the intent behind code doesn’t always live in code comments. A living spec is a maintained summary of how a subsystem is supposed to behave, often derived from static analysis plus curated documentation.

[NOVA]: Drift detection is the guardrail. If the spec says one thing and the code has drifted, OpenLore can flag that. For an agent, drift detection is a signal to slow down. It means the repo may have inconsistent behavior or incomplete migrations.

[ALLOY]: The MCP layer is what makes this immediately relevant to an agent stack. MCP is the interface agents use to call tools. If OpenLore provides MCP tools like “orientation” and “expand graph,” then any agent that can speak MCP—Claude Code, Codex in MCP-friendly harnesses, Hermes, OpenClaw-connected sessions—can pull in architectural memory without re-reading half the repo.

[NOVA]: The token discipline angle is where this becomes a practical advantage. Instead of injecting a huge repository summary every time, you can retrieve a small orientation blob: “Here are the top-level services, the main entry points, the key call paths for the current task, and the likely test targets.” Then you let the agent ask to expand specific nodes.

[ALLOY]: That “expand only what matters” workflow is the difference between a useful memory layer and a context bomb. If memory retrieval always returns a giant wall of text, the agent will either ignore it or drown in it. Graph expansion is a control knob.

[NOVA]: Here’s a recommended evaluation workflow for OpenLore that doesn’t require deep integration up front. Pick a repo where agents repeatedly make the same orientation mistakes. Common examples: monorepos with multiple apps, repos with both old and new implementations, or systems with multiple entry points depending on environment.

[ALLOY]: Step one: run OpenLore indexing and use the orientation tool to produce an architectural digest. Step two: run a coding agent session without OpenLore and ask it to plan a change. Step three: run the same planning session but give it the OpenLore orientation output first.

[NOVA]: Compare the plans. Specifically: does the OpenLore-assisted plan choose different files? Does it identify the correct entry points faster? Does it propose tests that are actually connected to the code paths involved?

[ALLOY]: Also compare the “first error” rate. In many agent runs, the first mistake is selecting the wrong starting point. If OpenLore reduces that, it’s already paying for itself.

[NOVA]: Now project radar item two: Mnemo. It treats agent memory as a decaying local knowledge graph.

[ALLOY]: Mnemo’s positioning is “persistent engineering cognition,” which is a useful phrase because it implies more than storing facts. Engineering cognition includes decisions, conventions, known failure modes, and the kind of “we tried that and it broke” institutional knowledge that rarely lives in code.

[NOVA]: The key operational feature here is memory decay. In agent systems, stale memory is dangerous because it has the tone of authority. If you inject an old decision into a new run, the model might treat it as current policy even if the project has moved on.

[ALLOY]: A decay mechanism is a way to demote old context unless it is reinforced. In human teams, memory decays naturally because people stop talking about outdated things. In an agent memory store, everything is equally retrievable unless you build in recency and reinforcement.

[NOVA]: Mnemo also emphasizes hybrid retrieval: BM25 plus vector plus graph search. That combination matters because “what you need” depends on the query type.

[ALLOY]: BM25 is strong for exact term matching—file names, error messages, specific library names, internal project terms. Vector retrieval is better for semantic similarity—finding related decisions even if the wording differs. Graph retrieval adds structure—following edges like “decision relates to subsystem,” “convention applies to module,” or “failure mode is triggered by dependency.”

[NOVA]: The practical advantage is that memory doesn’t have to be a flat list of notes. If your memory is a graph, you can answer questions like: “What conventions apply to this folder?” or “What prior incidents relate to this error?” or “Which decisions were made about auth flows in this service?”

[ALLOY]: Lifecycle hooks are another important concept. In an agent harness, you can decide when memories are written or reinforced. For example: when a PR merges, you can reinforce the memory that describes the decision. When a test fails repeatedly, you can create a memory entry describing the failure mode and its fix. When a release happens, you can decay certain old memories faster because they relate to a previous version.

[NOVA]: Local-first storage is the operational baseline here. If the memory store is local, you can keep sensitive project cognition on the machine or inside your controlled environment, rather than sending it to a remote hosted memory service.

[ALLOY]: Here’s the recommended way to start with Mnemo without giving it too much authority too soon. Begin by capturing four kinds of memory items.

[NOVA]: One: a project decision. Something like “we do not use database triggers; all integrity rules live in the service layer.” Two: a convention. Example: “All new endpoints must include request IDs and structured logging fields.” Three: an active task context. Example: “We’re migrating from library X to library Y; prefer Y for new code.” Four: a known failure mode. Example: “This integration test fails if timezone is not set to UTC.”

[ALLOY]: Then start a second session and query what Mnemo recalls. Inspect it like you would inspect output from a compiler or linter. You’re checking accuracy, relevance, and whether decay or ranking seems reasonable.

[NOVA]: The danger sign is when memory retrieval returns stale items with the same weight as fresh ones. If your memory store can’t express freshness, you will eventually treat it as untrusted and stop using it.

[ALLOY]: Another danger sign is when memory becomes a “policy injection” channel. Your harness should keep memory as advisory context unless the memory item is explicitly tagged as policy. Otherwise the model may treat any retrieved note as a rule, even when it was just a temporary workaround.

[NOVA]: Put OpenLore and Mnemo together and you get a more robust story than “agent memory.” OpenLore remembers the shape of the codebase—structure, call paths, clusters, specs. Mnemo remembers the project’s evolving knowledge—decisions, conventions, failures—with time sensitivity.

[ALLOY]: And both are more controllable than transcript stuffing. Transcripts are messy, full of speculation, and often contain outdated assumptions. Structured memory tools aim to retrieve smaller, more relevant context and to give you levers—graph expansion, decay, hybrid ranking—that you can tune.

[NOVA]: Next, we’ll move into the local-only and graph-repair side of the radar: OpenMonoAgent and Prometheus. [PAUSE]

## [31:00] OpenMonoAgent and Prometheus: local agents and graph-backed repair

[ALLOY]: Third project radar item: OpenMonoAgent. It’s a .NET-based local coding agent built around local inference via llama.cpp, Docker sandboxing, LSP and Roslyn code intelligence, MCP integration, and playbooks.

[NOVA]: The phrase to focus on is “zero-meter local coding-agent pattern.” Not because it means you never use cloud models, but because it gives you a baseline where reading code and trying mechanical edits is cheap, private, and repeatable.

[ALLOY]: Let’s start with local inference through llama.cpp. That means the model runs on your machine, using CPU and optionally GPU, without sending prompts or code to a hosted API by default. The obvious benefits are privacy and cost control.

[NOVA]: But the operational benefit is iteration speed in a different dimension: you can afford to run many small experiments. If you want to ask an agent to propose five variants of a refactor plan, or to analyze a repo structure repeatedly, local inference can make that “boring and cheap” instead of “expensive and metered.”

[ALLOY]: Docker sandboxing is the next piece. Once an agent can run commands, you need to decide what environment it runs in. A Docker sandbox can limit filesystem access, network access, and the blast radius of mistakes. Even when you trust the agent, you don’t necessarily trust every dependency install script or build step it might invoke.

[NOVA]: LSP and Roslyn code intelligence is where this becomes more than “a chatbot with a terminal.” LSP gives language-aware operations: go to definition, find references, symbol search, diagnostics. Roslyn is the .NET compiler platform that can provide deep semantic understanding for C# and related languages.

[ALLOY]: When you combine LSP/Roslyn with an agent loop, you get better targeted edits. Instead of grepping blindly, the agent can ask: “Where is this symbol referenced?” and then update call sites systematically. That’s exactly the kind of change local agents can do well even if their reasoning is weaker than frontier models.

[NOVA]: MCP integration matters because it means OpenMonoAgent can participate in a broader tool ecosystem. You can connect it to the same orientation tools, memory tools, or internal services you expose via MCP, without hardcoding integrations into the agent itself.

[ALLOY]: And playbooks are the “workflow capture” mechanism. A playbook can encode the steps for common tasks: run tests, locate failing files, apply a standard refactor pattern, regenerate code, update docs, and so on. In a local agent context, playbooks help reduce the amount of reasoning required for routine operations.

[NOVA]: Now, tradeoffs. Local models often underperform on deep reasoning, long-horizon planning, and complex cross-file synthesis compared to frontier hosted models. That doesn’t mean they’re useless. It means you should aim them at tasks where local constraints dominate and the reasoning load is moderate.

[ALLOY]: Good local-agent targets include: repository orientation, mechanical refactors, code formatting and lint fixes, updating namespaces or imports, generating boilerplate, writing tests from a clear spec, and producing structured summaries of what changed between commits.

[NOVA]: Risky targets for local models include: subtle security reviews, large-scale architectural redesign, tricky concurrency bugs, or anything where the agent must infer product intent from ambiguous signals. Those are the jobs where you often want a stronger hosted model—or a workflow that uses local tools for evidence and hosted models for reasoning.

[ALLOY]: That suggests a practical hybrid workflow. Use a local agent to gather evidence: map files, extract call paths, run tests, identify failing cases, and propose candidate edit locations. Then, if needed, hand that evidence to a stronger model to decide the actual patch strategy.

[NOVA]: Or invert it: use a strong model to propose a plan, but have the local agent execute the mechanical steps—apply the diff, update references, run tests—inside a sandbox where data doesn’t leave the machine.

[ALLOY]: A recommended test for OpenMonoAgent specifically: run it against a disposable repo with no cloud provider configured. Ask it to perform a routine but non-trivial task, like “rename a public method and update all call sites,” then “run the unit tests” and “summarize what changed.”

[NOVA]: Measure a few things. Did it correctly use code intelligence to find references? Did it avoid editing generated files? Did it keep the diff minimal? Did it run the right test commands? Did it stop and report when something failed?

[ALLOY]: Those measurements tell you where it fits in your stack. If it’s strong on mechanical edits and verification loops, it can become your default for low-risk work, saving cloud calls for the truly hard parts.

[NOVA]: Now, fourth project radar item: Prometheus from EuniAI. It’s framed as a knowledge-graph-driven software agent for mapping, understanding, and repairing complex codebases.

[ALLOY]: The key phrase is “graph-driven repair rather than chat-driven edits.” Many coding agents today operate like this: read some files, form a hypothesis, write a patch, run tests, repeat. The weak point is that the hypothesis can be underconstrained. The agent may jump to a patch because it sounds plausible, not because it has evidence about how the code actually connects.

[NOVA]: Graph context can constrain that. If the agent builds a graph of entities—modules, classes, functions, dependencies, call edges—it can use that graph to decide where a fix should live and what it might break.

[ALLOY]: Think about a bug report: “Login sometimes fails with a null reference error.” A chat-driven agent might search for “null” and “login” and patch the first thing it sees. A graph-driven agent might map the login flow: UI handler → auth service → token parser → user loader → database adapter. Then it can look for the specific edge where null might be introduced and follow that path.

[NOVA]: The verification loop part is critical. “Repair” isn’t only patch generation; it’s also selecting the right evidence to validate the patch. A graph can help choose tests. If the graph shows that a function is only exercised by two integration tests, those tests should be in the verification plan.

[ALLOY]: It can also help with failure recovery. If a patch fails tests, the agent can use the graph to identify likely blast radius. Did it change a shared interface used by many nodes? Did it alter a serialization format? Did it touch a low-level utility that fans out to many call sites?

[NOVA]: In practice, you evaluate a graph-driven repair project by asking: does the graph materially change the agent’s decisions? Or is it just a fancy index that the agent ignores?

[ALLOY]: A useful evaluation approach is to run Prometheus on a benchmark-style task or a disposable repo where you can inspect behavior. Then compare two artifacts: the graph evidence and the final patch. You’re looking for direct linkage.

[NOVA]: For example, if the patch changes a function, does the graph show why that function is the right choke point? If it updates call sites, does the graph enumerate them comprehensively? If it chooses tests, does the graph justify the selection based on coverage of the affected nodes?

[ALLOY]: Another test is to introduce an intentionally misleading signal. Put a file name that looks relevant but isn’t, or leave an outdated comment. Chat-driven agents often get baited by those. Graph-driven systems should be more resilient because they rely on actual code relationships rather than surface text.

[NOVA]: Prometheus, OpenLore, and Mnemo also connect conceptually. OpenLore provides architectural graphs for orientation. Mnemo provides a knowledge graph for project cognition with decay. Prometheus uses graphs to drive repair and verification. The stack-level idea is that graphs can serve as a grounding layer for agents—structure that’s harder to hallucinate than free-form narrative.

[ALLOY]: And this matters because the next step for coding agents isn’t only bigger models. It’s making the loop prove what it understood: show the relevant edges, show the evidence, run the right tests, and surface why the change is safe.

[NOVA]: Next, we’ll close with a practical “what to try next” queue that matches today’s control-surface theme. [PAUSE]

## [40:00] What to try next

[ALLOY]: Here’s the practical queue from EP060, in the order that reduces risk.

[NOVA]: First: Claude Code latest auto mode on managed clouds. Treat it like a feature flag because it is one. Enable it only with `CLAUDE_CODE_ENABLE_AUTO_MODE=1`, and start in the provider lane you actually plan to use—Bedrock, Vertex, or Foundry—so your tests reflect your real identity and logging environment.

[ALLOY]: Run three task types: read-only orientation, safe execution like tests and lint, and a small write task with strict guardrails. Measure tool-call behavior, the number of times it proceeds without asking, and whether it escalates appropriately when uncertain.

[NOVA]: Second: Codex Windows computer use. Start with a low-risk app and explicitly test reliability, bounded intent, and recovery. Reliability is “can it operate the UI without getting stuck.” Bounded intent is “does it stay on the task you gave it.” Recovery is “does it recognize blockers and ask for guidance instead of flailing.”

[ALLOY]: If you plan to supervise from mobile or Mac, test the remote-control boundary explicitly. Start a run at the Windows host, walk away, connect from a different device, and confirm you can meaningfully steer: answering questions, approving steps, and checking progress. The goal is to validate that execution stays local while supervision remains practical.

[NOVA]: Also treat Codex Profiles as operational evidence. Confirm identity is what you expect, and watch usage and token activity on a run where you know roughly what should happen. If token usage spikes, use that as a debugging prompt: repeated file reads, log verbosity, tool loops, or poor test targeting.

[ALLOY]: Third: if you build or maintain an agent harness, study the Messages API change: system entries inside the messages array. Use it to separate user intent from runtime policy and runtime facts. Implement at least one mid-run system update—permission change or budget change—and verify the model responds by changing its behavior, not just acknowledging the text.

[NOVA]: Keep system updates structured and avoid contradictory instruction timelines. Prefer “latest state summary” messages for runtime facts rather than a long chain of partial updates that the model has to reconcile.

[ALLOY]: Fourth: pick exactly one memory experiment so you can evaluate it honestly.

[NOVA]: Use OpenLore if your pain is architectural rediscovery—agents keep picking the wrong entry points, missing key call paths, or burning context on reading the same directories. Compare an edit plan with and without OpenLore’s orientation output before you allow writes.

[ALLOY]: Use Mnemo if your pain is lost project knowledge—decisions, conventions, and known failure modes that should carry across sessions. Start with a small set of memories and audit recall quality in a second session. Pay special attention to decay behavior and ranking, because freshness is what keeps memory from becoming stale authority.

[NOVA]: Use OpenMonoAgent if your pain is privacy, cost, or local repeatability. Make it your baseline for repo reading and mechanical edits inside a sandbox, then compare its outcomes with a hosted agent on the same tasks. You’re not asking it to be the best at everything; you’re asking it to make the private, cheap part of the workflow boring.

[ALLOY]: Use Prometheus if your research question is repair quality and verification. Evaluate whether the graph evidence actually constrains the patch and improves test selection and failure recovery. If the graph doesn’t change decisions, it’s not earning its complexity.

[NOVA]: For every trial, define the builder workflow before the tool touches important work: the use case, the build target, the operator boundary, the deploy or ship decision, and the verification pattern that proves the result. The useful build workflow puts evidence at the front, a bounded operator decision in the middle, and a clear ship, deploy, or stop rule at the end; that builder pattern is what keeps experiments from turning into vague demos.

[NOVA]: The durable lesson today is that agent stacks get better when they get more explicit: explicit gating for automation, explicit host boundaries for remote supervision, explicit runtime instruction updates for long runs, and explicit memory retrieval that is structured, queryable, and freshness-aware.

[ALLOY]: That’s AgentStack Daily for EP060. Toby On Fitness Tech dot com. We'll be back soon.
