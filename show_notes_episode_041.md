# EP041 — OpenClaw v2026.4.25, Codex App-Server, Space Solar, and AI-Designed Cars
**OpenClaw Daily** | April 27, 2026 | ~32–38 min

## Release Selection Verification
- GitHub stable releases checked latest-first from the latest API page: `v2026.4.25`, `v2026.4.24`
- Covered tags found in the last 5 episode notes: `v2026.4.24`, `v2026.4.23`, `v2026.4.22`, plus older carryover references
- Latest contiguous uncovered stable block from the newest stable release: `v2026.4.25`
- Result: EP041 leads with OpenClaw `v2026.4.25`.

## Episode Title
**OpenClaw v2026.4.25, Codex App-Server, Space Solar, and AI-Designed Cars**

## Tagline
OpenClaw’s new release is less about one flashy feature and more about making voice, plugins, observability, browser control, setup, and Codex integration feel production-ready. Then we zoom out to the Codex app becoming a real engineering workspace, Meta reserving space-beamed solar power, and automakers using AI inside the design loop rather than just the concept-art layer.

## Feed Description
EP041 leads with OpenClaw v2026.4.25: a big operational release that upgrades TTS and voice replies, moves plugin startup onto a persisted cold registry, expands OpenTelemetry diagnostics, improves browser automation, adds PWA/Web Push support in the Control UI, hardens installers and updates, and tightens Codex app-server integration. Then we connect that to OpenAI Codex CLI 0.125.0 and the broader Codex app direction: worktrees, app-server transports, sticky environments, permission profiles, plugin marketplaces, built-in Git, automations, and in-app browser workflows. The back half covers Meta’s capacity reservation for space-beamed solar power and why AI data centers are turning energy procurement into product strategy, then closes with GM, Nissan, and Neural Concept showing AI moving into automotive design, simulation, and software validation loops.

## Story Slate

### 1. **OpenClaw v2026.4.25 Is an Operations Release for Voice, Plugins, Observability, Browser Control, and Codex**
This release is packed: `/tts latest`, chat-scoped TTS controls, personas, Azure/Xiaomi/Local CLI/Inworld/Volcengine/ElevenLabs v3 provider coverage, a persisted cold plugin registry, low-cardinality OpenTelemetry spans and metrics, safer browser snapshots and tab handling, PWA/Web Push support, TUI setup flows, update hardening, and deeper Codex hook/app-server support.

### 2. **Codex Is Becoming an App Platform, Not Just a Coding CLI**
OpenAI’s Codex CLI 0.125.0 and the Codex app docs point toward a larger workspace model: app-server transports, remote thread config, sticky environments, permission profiles, plugin marketplace management, worktrees, integrated terminal, built-in Git review, automations, and an in-app browser for visual feedback. The interesting part is the control plane: agents are getting more powerful, but the product is also building more places to review, isolate, approve, fork, resume, and observe their work.

### 3. **Meta’s Space-Solar Reservation Shows AI’s Energy Problem Getting Weird**
Meta has reserved up to a gigawatt of future capacity from Overview Energy, a startup proposing satellites that collect solar energy in orbit and beam near-infrared light down to terrestrial solar farms. The near-term point is not that space solar is solved; it is that AI infrastructure demand is pushing hyperscalers into energy strategies that would have sounded speculative just a few years ago.

### 4. **AI-Designed Cars Move from Concept Art into Industrial Feedback Loops**
GM, Nissan, and Neural Concept show the useful version of industrial AI: faster sketch-to-model workflows, near-instant aerodynamic simulation, AI-assisted virtual wind tunnels, and code-generation help for software-defined vehicles. The important shift is from one-shot generation to feedback loops where humans can explore more options earlier.

## Show Notes
```md
OPENCLAW DAILY — EPISODE 041 — April 27, 2026

[00:00] INTRO / HOOK
Today we are rewriting the slate because there is now an OpenClaw v2026.4.25,
and this is a much better lead than trying to force a random enterprise AI M&A
story into the top slot.

This release is not one clean headline. It is a systems release. Voice gets more
serious. Plugin startup gets colder and faster. Observability gets broader.
Browser automation gets safer. Setup gets smoother. Install and update paths get
harder to break. And Codex integration gets another step closer to native
app-server behavior.

Then we use that as the bridge into Codex itself. The Codex app is not just an
IDE helper anymore. The feature set is starting to look like an engineering
workspace: worktrees, app-server threads, sticky environments, permission
profiles, automations, plugin marketplaces, built-in Git, terminals, and an
in-app browser for visual feedback.

After that we zoom out: Meta is reserving future power from a space-solar
startup, because AI compute is becoming an energy logistics problem. And we end
with automakers using AI in actual design and simulation loops, not just to make
pretty car renders.

[02:00] STORY 1 — OpenClaw v2026.4.25 Makes the Runtime Feel More Production-Ready
OpenClaw v2026.4.25 is a big release, but the theme is surprisingly clear:
make the agent runtime easier to operate in the real world.

The first obvious piece is voice. This release upgrades TTS across the stack.
There is `/tts latest` for reading the latest reply aloud, chat-scoped controls
like `/tts chat on`, `/tts chat off`, and `/tts chat default`, per-agent and
per-account overrides, and a bigger provider surface: Azure Speech, Xiaomi,
Local CLI TTS, Inworld, Volcengine or BytePlus Seed Speech, and ElevenLabs v3.

That matters because voice is not just a novelty layer anymore. If agents are
inside WhatsApp, Telegram, Discord, calls, Talk Mode, and live collaboration
surfaces, voice has to be configurable per context. The voice you want for a
private assistant is not necessarily the voice you want in a group chat, a phone
call, a Feishu workflow, or a bot account. v2026.4.25 moves TTS toward that more
realistic model: shared provider credentials, but local control over voice,
provider, persona, account, and channel behavior.

The second major piece is plugin startup. OpenClaw is moving plugin startup,
provider discovery, install metadata, and repair flows onto a persisted cold
registry. In plain English: normal startup should not need to rummage through a
wide plugin universe and import a bunch of runtime code just to answer questions
like what is installed, what provider owns this model, or what setup choices are
available.

That is not glamorous, but it is exactly the kind of engineering that makes a
runtime feel fast and predictable. The release adds `openclaw plugins registry`,
changes `plugins list` to read the cold registry by default, refreshes the index
after chat and CLI plugin changes, and points operators toward registry repair
instead of old break-glass switches. The product point is simple: plugin systems
are powerful only if they do not turn every startup, status check, or setup
prompt into a slow full-runtime scan.

The third piece is observability. OpenTelemetry coverage expands across model
calls, token usage, tool loops, harness runs, exec processes, outbound delivery,
context assembly, and memory pressure. The important detail is that the release
keeps the attributes bounded and low-cardinality. It is trying to make Grafana,
Prometheus, traces, and metrics useful without leaking prompts, responses,
session identifiers, command text, recipient data, or raw provider request IDs.

That is the right direction for agent infrastructure. If agents are going to run
jobs, call tools, spawn subagents, send messages, manage browser tabs, and use
models from multiple providers, operators need to answer basic questions: where
did latency go, which agent is burning tokens, are model calls failing, did an
exec process hang, did a delivery fail, is context assembly growing, is memory
pressure rising. But diagnostics cannot become a second data leak.

Browser automation also gets a meaningful reliability pass: safer tab URLs in
agent responses, iframe-aware role snapshots, a CDP-native role snapshot
fallback, cursor-clickable detection, target attach preparation, deeper `browser
doctor --deep` probing, headless one-shot launch support, and more tuning for
slow hosts like Raspberry Pi. That is a builder story because browser automation
is one of the places where agents look magic when it works and fragile when it
does not. Better refs, better diagnostics, and safer tab handling are the boring
things that make computer-use agents usable.

The Control UI and setup flow get practical polish too: PWA install support, Web
Push notifications for Gateway chat, Crestodian first-run repair, TUI setup,
context-mode selection, progress indicators, and a shorter startup greeting.
And the install/update hardening list is huge: Windows scheduled-task behavior,
macOS LaunchAgent token rotation, Linux service setup, Docker packaging, Node
service restarts, bundled plugin runtime dependencies, mixed-version gateway
verification, low-disk warnings, and post-update doctor repairs.

The takeaway is that v2026.4.25 is not trying to win with a single demo. It is
trying to make OpenClaw more dependable as a daily agent operating system. Voice,
plugins, diagnostics, browser control, setup, updates, Codex, and channels all
moved forward.

→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.25

[12:00] STORY 2 — Codex Is Turning into a Real App Platform
The most interesting companion story is Codex, because v2026.4.25 includes a
few Codex-specific changes, and OpenAI’s own Codex changelog points in the same
direction.

OpenClaw now requires Codex app-server 0.125.0 or newer for the Codex harness.
It covers native MCP `PreToolUse`, `PostToolUse`, and `PermissionRequest`
payloads through the OpenClaw hook relay. It teaches prompts and `agents_list`
to surface native Codex app-server availability, so agents can prefer the native
`/codex` path instead of falling back to older Codex ACP paths unless ACP is
explicit. It also fixes modern Codex reasoning controls, prepares native Codex
sub-agent metadata, improves app-server error handling, and tightens Codex media
and approval boundaries.

That sounds narrow until you connect it to what Codex itself is becoming.
OpenAI’s Codex CLI 0.125.0 adds app-server integration work around Unix socket
transport, pagination-friendly resume and fork, sticky environments, remote
thread config and thread store plumbing, plugin marketplace install and upgrade,
and permission profiles that round-trip across TUI sessions, user turns, MCP
sandbox state, shell escalation, and app-server APIs.

The app feature docs make the product shape clearer. The Codex app is described
as a desktop experience for working on Codex threads in parallel, with projects,
worktrees, automations, Git features, and an integrated terminal. You can run
local tasks directly in a project, isolate experiments in Git worktrees, or run
remote cloud work. The diff pane lets you review changes, comment inline, stage
or revert chunks, commit, push, and create pull requests. The terminal is scoped
to the project or worktree, and Codex can read terminal output, so a failed test
or running dev server becomes part of the thread context.

The in-app browser is another important piece. It gives the user and Codex a
shared rendered view of a web page inside the thread. That means a frontend task
can include visual preview and visual comments without constantly switching
between the editor, terminal, browser, and chat. It is not meant to replace your
logged-in personal browser for everything, but for local dev servers, file-backed
previews, and public pages, it closes the loop between code change, visual
review, and follow-up instruction.

This is the larger story: coding agents are moving from autocomplete and chat
into work surfaces. The features that matter are not only model quality. They
are isolation, review, approvals, observability, environment management,
threading, resume/fork behavior, and the ability to run multiple pieces of work
without trampling the user’s current checkout.

That is why Codex app-server support matters inside OpenClaw. If Codex is
becoming a native app platform for engineering tasks, then OpenClaw wants to
route work to it through the best available harness, preserve permission events,
handle hooks, and expose native availability to agents. The interesting
question is no longer “can an AI write a function?” It is “can an AI workspace
hold a messy software job from intent to diff to test to review to deployment
without losing control?”

→ https://developers.openai.com/codex/changelog
→ https://developers.openai.com/codex/app/features
→ https://developers.openai.com/codex/app/browser

[21:00] STORY 3 — Meta Reserves Space-Beamed Solar Capacity for AI Data Centers
Now zoom out from software operations to energy operations.

Meta has signed a capacity reservation with Overview Energy, a startup working
on satellites that would collect solar energy in orbit and beam near-infrared
light down to large solar farms. Those solar farms would then convert the light
into electricity using terrestrial solar infrastructure, potentially producing
solar power at night for data-center customers.

The headline is weird, but the pressure underneath it is very normal: AI data
centers need enormous amounts of reliable electricity. TechCrunch reports that
Meta’s data centers used more than 18,000 gigawatt-hours of electricity in 2024,
and that the company has committed to building 30 gigawatts of renewable power
sources with a focus on industrial-scale solar. The challenge is that AI compute
does not stop at sunset.

Overview’s approach is different from classic microwave space-solar concepts.
The company is talking about converting collected orbital solar power into a
broad near-infrared beam aimed at large solar installations, rather than firing a
dense beam at a small receiver. The Meta reservation is for up to one gigawatt
of future power. Overview plans a low-Earth-orbit demonstration in 2028 and hopes
to begin launching satellites for the Meta commitment around 2030.

The timeline matters. This is not a near-term fix for today’s grid bottlenecks.
It is a signal. Hyperscalers are no longer just shopping for GPUs, data-center
sites, and networking. They are shopping for future energy optionality.

The builder lesson is that AI product strategy and energy strategy are merging.
Every always-on agent, video generator, realtime assistant, long-context
workflow, and background automation loop has a power profile. The user sees a
button. The operator sees a model call. The infrastructure team sees a cluster.
The energy team sees load, intermittency, grid constraints, batteries, permitting,
and long-term power contracts.

So whether or not space solar becomes real on Overview’s schedule, Meta’s move
is interesting because it shows how far the search for AI power is expanding.
The future of compute may depend as much on power procurement as on chips.

→ https://techcrunch.com/2026/04/27/meta-inks-deal-for-solar-power-at-night-beamed-from-space/

[29:00] STORY 4 — AI-Designed Cars Move from Concept Art into Industrial Feedback Loops
The last story is a better version of an AI-in-industry story because it is not
just about making pictures. It is about shortening feedback loops.

The Verge reports on how GM, Nissan, and Neural Concept are using AI in vehicle
design and development. The old vehicle-development cycle can take five years or
more: sketches, design reviews, 3D models, clay, simulation, engineering,
software, manufacturing constraints, and more review. That cycle is painful when
regulations, tariffs, EV incentives, consumer demand, and software requirements
change faster than the car program.

GM’s designers are using tools like Vizcom to turn human sketches into richer 3D
models and animations faster. The key detail is that the human sketch still
starts the process. AI is helping the team see possibilities sooner, compare
more directions, and create internal visual material without waiting for a slow
handoff chain.

The more operational part is simulation. Neural Concept uses neural networks to
speed up computational fluid dynamics. The Verge reports that Jaguar Land Rover
described aerodynamic jobs that used to take four hours now taking about one
minute, and GM is developing an AI-powered virtual wind tunnel that can give
designers near-instant feedback on drag as surfaces change.

That is the important shift. If aerodynamic feedback arrives while designers are
still exploring shapes, bad directions can be killed earlier and promising ones
can be refined before the design is frozen. AI is valuable not because it draws a
car once, but because it lets the team test more versions while the cost of
change is still low.

Nissan’s angle is software-defined vehicles. It is using code-generation tools
for lower-level software tasks like unit tests, aiming to improve development
speed and quality. That matters because modern cars are increasingly software
systems, and software integration is where programs can slip.

The caution is that these workflows still need human oversight. Faster iteration
can create better products, but it can also amplify bad assumptions or increase
pressure on workers. The useful framing is that AI is entering industrial loops
where the output is not the final artifact. The output is an earlier signal that
helps humans decide what to do next.

→ https://www.theverge.com/transportation/918411/gm-ai-car-design-nissan-neural-concept

[36:00] OUTRO / CLOSE
That is the episode.

OpenClaw v2026.4.25 is the lead because it makes the runtime feel more
production-ready across voice, plugins, observability, browser automation,
setup, updates, and Codex. Codex itself is turning into a real engineering app
platform, with worktrees, automations, Git review, app-server threads,
permission profiles, and in-app browser workflows. Meta’s space-solar bet shows
how strange AI infrastructure planning gets when power becomes the bottleneck.
And AI-designed cars show the strongest industrial AI pattern: not one-shot
generation, but faster human-supervised feedback loops.

→ Reply here to approve transcript generation.
```

## Verified Links
- OpenClaw — Release `v2026.4.25`: https://github.com/openclaw/openclaw/releases/tag/v2026.4.25
- OpenAI Developers — Codex changelog / Codex CLI 0.125.0: https://developers.openai.com/codex/changelog
- OpenAI Developers — Codex app features: https://developers.openai.com/codex/app/features
- OpenAI Developers — Codex app in-app browser: https://developers.openai.com/codex/app/browser
- TechCrunch — Meta inks deal for solar power at night, beamed from space (Apr 27, 2026): https://techcrunch.com/2026/04/27/meta-inks-deal-for-solar-power-at-night-beamed-from-space/
- The Verge — The AI-designed car is taking shape (Apr 27, 2026): https://www.theverge.com/transportation/918411/gm-ai-car-design-nissan-neural-concept

## Chapters
- **[00:00] Hook — OpenClaw v2026.4.25 Changes the Slate**
- **[02:00] OpenClaw v2026.4.25 Makes the Runtime Feel More Production-Ready**
- **[12:00] Codex Is Turning into a Real App Platform**
- **[21:00] Meta Reserves Space-Beamed Solar Capacity for AI Data Centers**
- **[29:00] AI-Designed Cars Move from Concept Art into Industrial Feedback Loops**
- **[36:00] Outro**

→ Reply here to approve transcript generation.
