# EP040 — OpenClaw v2026.4.24, Project Deal, Claude Connectors, and the ComfyUI Control Bet
**OpenClaw Daily** | April 26, 2026 | ~40–46 min

## Release Coverage Check
- Stable GitHub releases checked: `v2026.4.24`, `v2026.4.23`
- Covered in the last 5 episode notes: `v2026.4.23`, `v2026.4.22`, `v2026.4.21`, `v2026.4.20`, `v2026.4.15`, `v2026.4.14`, `v2026.4.12`, `v2026.4.11`
- Latest contiguous uncovered stable block from the newest stable release: `v2026.4.24`
- Result: **OpenClaw release coverage is included in EP040 for v2026.4.24**

## Episode Title
**OpenClaw v2026.4.24, Project Deal, Claude Connectors, and the ComfyUI Control Bet**

## Tagline
OpenClaw v2026.4.24 earns the front of the episode by turning live collaboration into a much more practical surface: Google Meet becomes bundled, realtime voice loops can consult the full agent, browser automation gets sturdier, and model/plugin infrastructure gets lighter. Then EP040 turns to Anthropic’s agent-on-agent marketplace experiment, Claude’s move into personal app connectors, and the signal behind ComfyUI’s $500 million valuation.

## Feed Description
OpenClaw v2026.4.24 is the lead story and it deserves to be. The release adds Google Meet as a bundled participant plugin with personal auth, live voice transports, paired-node Chrome support, artifact and attendance export, and recovery flows for already-open tabs; it also adds deeper realtime agent consults across Talk, Voice Call, and Meet, brings safer browser automation and stronger tab recovery, refreshes bundled model catalogs around DeepSeek V4, and keeps startup lighter with more manifest-driven model and plugin plumbing. After that release deep dive, EP040 looks at Anthropic’s Project Deal marketplace experiment, Claude’s new personal-app connectors, and why ComfyUI’s rise suggests human-in-the-loop control is still the premium layer in AI media workflows.

## Story Slate

### 1. **OpenClaw v2026.4.24 Turns Realtime Collaboration into a First-Class Surface**
This release is bigger than a feature bundle. Google Meet now lands as a bundled plugin with real auth, live voice paths, artifact export, and browser recovery tooling, which pushes OpenClaw further from chat wrapper toward operator runtime. The rest of the release reinforces that direction with full-agent realtime consult loops, sturdier browser automation, DeepSeek V4 catalog updates, lighter startup plumbing, and a long fix list that reduces transport, replay, and session surprises.

### 2. **Anthropic’s Project Deal Is a Preview of Agent Markets, Not Just a Research Curiosity**
Anthropic says it ran a small internal marketplace where models represented buyers and sellers and negotiated real transactions for real value. The builder implication is that labs are starting to test not just agent reasoning, but agent incentives, information asymmetry, and what happens when different model qualities start bargaining against each other.

### 3. **Claude’s Personal-App Connectors Push the Agent Surface Closer to Everyday Action**
Claude is expanding beyond work integrations into personal apps like Spotify, Uber, Instacart, TripAdvisor, and TurboTax. That matters because the next agent race is not only about answering questions; it is about being the trusted layer that can see context across multiple apps and still ask for confirmation before high-stakes actions.

### 4. **ComfyUI’s Valuation Says Control Still Beats Prompt Roulette**
ComfyUI’s $500 million valuation is a strong market signal that creators still want node-based control even as diffusion and image models improve. The practical lesson is that better base models do not erase the demand for repeatability, surgical edits, and workflows that do not collapse every refinement step back into a slot-machine prompt.

## Show Notes
```md
OPENCLAW DAILY — EPISODE 040 — April 26, 2026

[00:00] INTRO / HOOK
OpenClaw v2026.4.24 is the latest stable release, and because v2026.4.23 was
already covered in the recent episode notes, v2026.4.24 is the only valid
release block at the front of EP040.

And it earns that spot by making realtime collaboration much more concrete.
Google Meet becomes a bundled OpenClaw surface, Talk and Voice Call can consult
the full agent during live voice sessions, browser automation gets sturdier, and
model-plus-plugin infrastructure keeps getting lighter and more explicit.

After the release deep dive, we move to Anthropic’s Project Deal marketplace
experiment, Claude’s personal-app connectors, and the market signal behind
ComfyUI’s latest funding round.

[01:30] STORY 1 — OpenClaw v2026.4.24 Makes Live Meetings and Voice Sessions Far More Practical
The center of v2026.4.24 is Google Meet.

OpenClaw now ships a bundled Google Meet participant plugin with personal Google
auth, explicit meeting joins, Chrome and Twilio realtime transports, paired-node
Chrome support, artifact and attendance export, and recovery tooling for tabs
that are already open. That is not a small plugin addition. It is OpenClaw
turning a live collaboration surface into something the runtime can actually own.

The practical difference is huge.
A meeting tool is only valuable if it can handle the messy parts around the
meeting, not just the idealized join button. This release adds browser-state
recovery, OAuth doctor flows, `recover_current_tab`, attendance and conference-
record workflows, transcript and recording export, and the ability to inspect
already-open Meet tabs instead of blindly opening duplicates. Those are the
kinds of details that move a feature from “demoable” to “operable.”

And OpenClaw does not treat Meet as an isolated island.
Talk, Voice Call, and Google Meet can now use realtime voice loops that consult
the full OpenClaw agent for deeper tool-backed answers. That matters because it
changes the ceiling on what a live audio session can do. Instead of being stuck
inside a thin realtime model interaction, the session can hand off to the full
agent when it needs broader memory, tools, or more deliberate work. That makes
live voice feel less like a novelty interface and more like a serious front end
for the rest of the system.

There is also a paired-node story here that matters for real operators.
The release explicitly supports Chrome-node style setups for hosts that need
specialized Chrome, audio routing, or VM-like environments. That is exactly the
kind of real-world deployment detail that tells you the feature was designed for
messy environments, not just a single clean laptop path.

[10:30] STORY 1B — Browser Control, DeepSeek Catalogs, and Startup Plumbing All Get Sharper
The next major thread in v2026.4.24 is that OpenClaw keeps reducing friction in
how agents actually act on the world.

Browser automation gets coordinate clicks, longer default action budgets,
per-profile headless overrides, steadier tab reuse, and stronger recovery for
stale sessions and locks. That sounds incremental until you remember how often
browser automation fails on exactly those edges. A browser tool becomes useful
when agents can survive long waits, recover stale attaches, reuse the right tab,
and still keep moving without asking the operator to babysit every broken state.

This release also pushes browser operations toward clearer operator control.
There are doctor diagnostics, stronger security boundaries on browser requests,
better screenshot timeout handling, more stable tab identifiers, and more robust
existing-session behavior. So the browser surface is not just gaining features.
It is gaining a more reliable operating model.

The model catalog side moves too.
DeepSeek V4 Flash and V4 Pro enter the bundled catalog, with V4 Flash becoming
the onboarding default, while replay and thinking behavior gets fixed for follow-
up tool-call turns. That matters because model availability is only part of the
story. Operators need the runtime to preserve reasoning behavior cleanly across
multi-turn sessions, tool calls, and replay-sensitive providers. Otherwise a new
model row is mostly decorative.

Then there is the startup and catalog plumbing.
OpenClaw continues moving toward static catalogs, manifest-backed model rows,
lazier provider dependencies, and lighter packaged installs. That is good
runtime architecture. It means listing models, reading setup metadata, and
inspecting capabilities can happen without always dragging heavy plugin runtime
state into memory. On a product level, that makes the system feel faster. On an
architecture level, it makes capabilities more inspectable and less magical.

[18:30] STORY 1C — The Fixes Show OpenClaw Tightening the Runtime, Not Just Expanding It
A lot of the real value in v2026.4.24 lives in the fix list.

Heartbeat scheduling gets hardened against oversized timers and prompt leakage.
Restart continuations become more durable. Session and transcript handling get
less fragile. Telegram, Discord, Slack, WhatsApp, and browser paths all pick up
specific reliability improvements. DeepSeek replay gets corrected. Existing
browser sessions stop poisoning future attaches. Long-running local or provider
calls inherit better timeout behavior. And isolated cron runs stop leaking stale
state from earlier sessions.

There is also an important operator-facing cleanup around models.
`/models add` is deprecated rather than quietly mutating model configuration from
chat, while manifest-sourced rows and read-only list improvements make model
surfaces more explicit. That is a healthy correction. The runtime is getting
more powerful, but it is also being pushed toward clearer ownership boundaries
about what should happen in chat, what should happen in setup, and what should
be auditable as configuration.

The release even includes a real breaking change for plugin developers.
The old Pi-only embedded extension factory compatibility path is removed in favor
of the agent tool-result middleware route with harness declarations. That is not
just cleanup for cleanup’s sake. It is part of OpenClaw trying to keep Pi and
Codex-style runtimes on a more honest shared contract instead of letting legacy
compatibility seams drift forever.

So the practical read on v2026.4.24 is straightforward.
This is a release about making live surfaces more usable, browser automation more
reliable, model and plugin infrastructure more legible, and the runtime less
surprising under real load.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.24

[26:30] STORY 2 — Anthropic’s Project Deal Tests What Happens When Agents Negotiate for People
Anthropic’s Project Deal is easy to dismiss as a quirky internal experiment.
That would be a mistake.

The company says it ran a classified internal marketplace where AI agents
represented both buyers and sellers, made real deals, and negotiated over real
value for a self-selected pool of employees. Anthropic says 186 deals were made,
totaling more than $4,000 in value, with participants getting a small budget and
the transactions actually honored after the experiment.

The reason this matters is not the absolute scale.
The reason it matters is the shape of the test. This is not “can an agent answer
questions” or “can an agent click buttons.” It is a test of bargaining,
representation, asymmetry, incentives, and delegated economic action.

Anthropic says more advanced models tended to get objectively better outcomes,
while the users on the weaker side did not necessarily realize they were losing
out. That should get attention immediately. If agent quality gaps become real in
negotiation settings, then the next version of model advantage may not just show
up as nicer prose or stronger benchmark scores. It may show up as who gets the
better deal in an automated market.

That has obvious implications for builders.
Once agents start buying, selling, routing requests, negotiating availability,
or deciding which counterparties to trust, the quality of the agent becomes an
economic issue. Fairness, transparency, and action review start to matter a lot
more because a user may not be able to tell when their agent is systematically
underperforming against a better one.

So Project Deal looks small, but it points to a larger future category:
agent marketplaces where the real question is not only whether agents can act,
but whether they can represent human interests well enough under competition.
→ https://techcrunch.com/2026/04/25/anthropic-created-a-test-marketplace-for-agent-on-agent-commerce/

[32:30] STORY 3 — Claude’s Personal-App Connectors Expand the Trust Surface
Anthropic’s other relevant move this week is much more product-shaped.

Claude is expanding its connector model beyond work apps into personal services
like Spotify, Uber, Instacart, AllTrails, TripAdvisor, Audible, and TurboTax.
That matters because it brings the agent surface closer to normal life tasks,
not just enterprise software or developer workflows.

The product significance is in the orchestration layer.
Once Claude can see multiple connected apps and suggest them in context, the
assistant stops looking like a single chat destination and starts looking more
like a coordination layer across services. Anthropic says the connected app data
is not used to train its models, that apps do not see a user’s other Claude
conversations, and that Claude asks for verification before taking actions like
purchases or reservations. Those trust boundaries are not side notes. They are
core product requirements if agents are going to move from recommendation into
action.

For builders, this story matters because it reinforces where the competition is
heading.
The next agent race is not only about smarter raw models. It is about who can
own the action surface across apps while preserving enough trust that users will
actually let the system do something consequential.

That is why confirmation design, connector scoping, and cross-app context are
all strategic product questions now.
→ https://www.theverge.com/ai-artificial-intelligence/917871/anthropic-claude-personal-app-connectors

[37:30] STORY 4 — ComfyUI’s Valuation Is a Bet Against Prompt-Only Creative Workflows
ComfyUI raising at a $500 million valuation is not just startup theater.
It is a signal about where value still sits in AI media workflows.

The company’s pitch is that prompt-only systems often get you most of the way to
an image or video result, but not the last mile without turning every change
into a slot-machine reroll. ComfyUI’s node-based workflow offers much more
granular control over individual steps in the generation process, and TechCrunch
reports the company says it now has more than 4 million users.

The deeper implication is that better models do not automatically kill the need
for control surfaces.
In fact, better models can increase demand for them, because once the base
quality is high enough, the remaining value shifts toward repeatability,
precision, and targeted edits. That is exactly where node-based systems win.

For builders and operators, this is a useful reminder.
If you are designing around image, video, or multimodal outputs, there is still
real demand for workflows that let users steer, inspect, and refine the pipeline
instead of collapsing every adjustment back into one more prompt.

So ComfyUI’s valuation is really a thesis about control.
Prompting remains the easy on-ramp. But production-quality creative work still
wants surfaces that can preserve intent across multiple steps without forcing the
user to gamble away the good parts of the result every time.
→ https://techcrunch.com/2026/04/24/comfyui-hits-500m-valuation-as-creators-seek-more-control-over-ai-generated-media/

[43:00] OUTRO / CLOSE
That is enough for today.
OpenClaw v2026.4.24 pushed live collaboration, realtime voice, browser
reliability, and catalog infrastructure forward in practical ways.
Anthropic used Project Deal to hint at what agent markets might really test.
Claude expanded into personal app actions.
And ComfyUI reminded everyone that better models do not erase the premium on
control.

→ Reply here to approve transcript generation.
```

## Verified Links
- OpenClaw — Release `v2026.4.24`: https://github.com/openclaw/openclaw/releases/tag/v2026.4.24
- TechCrunch — Anthropic created a test marketplace for agent-on-agent commerce (Apr 25, 2026): https://techcrunch.com/2026/04/25/anthropic-created-a-test-marketplace-for-agent-on-agent-commerce/
- The Verge — Claude is connecting directly to your personal apps like Spotify, Uber Eats, and TurboTax (Apr 24, 2026): https://www.theverge.com/ai-artificial-intelligence/917871/anthropic-claude-personal-app-connectors
- TechCrunch — ComfyUI hits $500M valuation as creators seek more control over AI-generated media (Apr 24, 2026): https://techcrunch.com/2026/04/24/comfyui-hits-500m-valuation-as-creators-seek-more-control-over-ai-generated-media/

## Chapters
- **[00:00] Hook — OpenClaw v2026.4.24 Takes the Front**
- **[01:30] OpenClaw v2026.4.24 Makes Live Meetings and Voice Sessions Far More Practical**
- **[10:30] Browser Control, DeepSeek Catalogs, and Startup Plumbing All Get Sharper**
- **[18:30] The Fixes Show OpenClaw Tightening the Runtime, Not Just Expanding It**
- **[26:30] Anthropic’s Project Deal Tests What Happens When Agents Negotiate for People**
- **[32:30] Claude’s Personal-App Connectors Expand the Trust Surface**
- **[37:30] ComfyUI’s Valuation Is a Bet Against Prompt-Only Creative Workflows**
- **[43:00] Outro**

→ Reply here to approve transcript generation.
