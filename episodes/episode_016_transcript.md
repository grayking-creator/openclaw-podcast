## [00:00-02:30] OpenClaw Sheds Its Skin

NOVA: I'm NOVA, this is OpenClaw Daily, and today we have one of those releases where the version numbers look tidy, but the actual story underneath is messy, consequential, and honestly kind of fascinating. [PAUSE] This week, two bugs hit a real power-user setup hard enough that they tell you almost everything you need to know about where OpenClaw is right now.

ALLOY: Yeah. These were not cute little edge cases. These were the kind of bugs that make you doubt your own setup, because what you see is not what the system is actually doing.

NOVA: Bug one: a user had [EMPHASIS]MiniMax[/EMPHASIS] configured as their reasoning model. The upstream API was throwing [EMPHASIS]api_error[/EMPHASIS]. OpenClaw looked at that, decided it must be transient, retried it quietly, never surfaced the failure, never triggered fallback properly, and the user got a degraded result back with no idea the original call had failed.

ALLOY: Which is brutal, because the worst bugs are the ones that don't explode. They just get worse in silence. You don't get a red light. You get a dimmer green light.

NOVA: Exactly. And bug two was a different class of pain, but just as real. User pastes a fresh [EMPHASIS]OpenAI Codex[/EMPHASIS] token, sees the confirmation, everything looks successful, restarts the gateway, and the token has snapped back to the expired credential.

ALLOY: That one makes you feel crazy. Because from the user's perspective, they did the right thing. They pasted the new token. The app said, yes, saved. Then after restart, nope. Old bad token again. [PAUSE] Under the hood, the gateway's in-memory auth state was overwriting the freshly saved disk value on restart.

NOVA: Both of those are fixed in [EMPHASIS]v2026.3.23[/EMPHASIS]. But to understand why they happened, you need to understand what [EMPHASIS]v2026.3.22[/EMPHASIS] changed. Because .22 is the big one. .22 is OpenClaw doing something it probably should have done a year ago.

ALLOY: The legacy purge.

NOVA: The legacy purge. The old names, the compatibility layers, the weird transitional paths, the browser relay crutches, the plugin SDK mush — a lot of it got torn out. [PAUSE] And I think the right way to frame these two releases together is this: .22 removes the dead skin, and .23 makes sure the new skin doesn't crack.

ALLOY: That's the whole episode. If you're maintaining a real install, these are not decorative updates. They're structural.

## [02:30-11:00] The Legacy Purge — v2026.3.22 Breaking Changes

NOVA: Let's start with the most emotionally charged change, because people get weirdly attached to names, even when those names should have been retired forever ago. [EMPHASIS]CLAWDBOT_*[/EMPHASIS] and [EMPHASIS]MOLTBOT_*[/EMPHASIS] environment names are gone. Not deprecated. Not tolerated with a warning. Gone.

ALLOY: And I want to slow that down, because if you run OpenClaw on one laptop and nowhere else, you might hear that and think, okay, rename some variables, fine. That's not the real failure mode. The real failure mode is you've got an old [EMPHASIS].env[/EMPHASIS] file in Docker Compose, or a crusty [EMPHASIS]systemd[/EMPHASIS] unit on a VPS, or something in a shell profile you haven't looked at in eight months. You upgrade, OpenClaw starts, and those values are silently ignored.

NOVA: No error. No migration banner.

ALLOY: No, "hey, I saw [EMPHASIS]CLAWDBOT_TOKEN[/EMPHASIS] and that's obsolete." Just missing config. Suddenly auth doesn't line up, state path isn't where you thought, maybe a plugin doesn't load, maybe a token seems absent. [PAUSE] This is the kind of break that hits at two in the morning after an upgrade on a machine you haven't touched in a while.

NOVA: Grep your env files. Every environment you run OpenClaw in. Every host. Every Compose file. Every startup unit. Every shell bootstrap. If you've got [EMPHASIS]CLAWDBOT_*[/EMPHASIS] or [EMPHASIS]MOLTBOT_*[/EMPHASIS], treat that as broken until corrected.

ALLOY: Same story with the old [EMPHASIS]~/.moltbot[/EMPHASIS] state directory. That path is not part of the future anymore. If your state still lives there, OpenClaw will not magically infer that for you after upgrade. Move it to [EMPHASIS]~/.openclaw[/EMPHASIS] or set [EMPHASIS]OPENCLAW_STATE_DIR[/EMPHASIS] explicitly and be done with it.

NOVA: And this is one of those choices where I actually agree with the harshness. Transitional aliases feel kind in the short term, but they make the architecture lie about itself. There is a real cost to pretending old names are still first-class.

ALLOY: I agree with the end state. I disagree with how serene people are about the migration pain. If you're the person who manages five installs and two of them are weird, this is not a philosophical cleanup. This is a scavenger hunt.

NOVA: Fair. [PAUSE] The second big breaking change in .22 is that [EMPHASIS]ClawHub[/EMPHASIS] is now first-class, and the practical meaning of that is bigger than the marketing phrasing makes it sound. [EMPHASIS]openclaw plugins install name[/EMPHASIS] now checks ClawHub first, then falls back to npm only if ClawHub doesn't have the package.

ALLOY: Which means install behavior changed, even if you didn't change your command. That's the thing people need to hear. If you've got scripts that assume an npm package resolution path, and the same name now exists on ClawHub, you may get the ClawHub version first.

NOVA: There are also native commands now: [EMPHASIS]openclaw skills search[/EMPHASIS], [EMPHASIS]openclaw skills install[/EMPHASIS], [EMPHASIS]openclaw skills update[/EMPHASIS]. [PAUSE] And to me, this is OpenClaw finally aligning the product with its intended ecosystem. ClawHub was always supposed to be the home for skills. This release makes that real instead of aspirational.

ALLOY: It's cleaner, but test your automation. If you've got bootstrap scripts, dotfiles, onboarding docs, make sure they still install what you think they install. The change is good. Surprises are not.

NOVA: Third: the [EMPHASIS]Plugin SDK[/EMPHASIS] overhaul. This is not a nibble around the edges. [EMPHASIS]openclaw/extension-api[/EMPHASIS] is gone. There is no compatibility shim. The new surface is [EMPHASIS]openclaw/plugin-sdk/*[/EMPHASIS] with narrower subpaths and much clearer boundaries.

ALLOY: If you have custom plugins, this is a real migration. It's not optional. There's no fallback. You don't get to say, "I'll update later." Later is broken.

NOVA: Bundled plugins also have to use the injected runtime for host-side operations now, which is one of those changes that sounds bureaucratic until you realize it removes a lot of ambiguous privilege bleed. Host behavior is explicit. Runtime boundaries are explicit.

ALLOY: And message discovery changed too. [EMPHASIS]describeMessageTool()[/EMPHASIS] is now required. The old [EMPHASIS]listActions[/EMPHASIS], [EMPHASIS]getCapabilities[/EMPHASIS], [EMPHASIS]getToolSchema[/EMPHASIS] flow is removed. [PAUSE] That's not a rename. That's a contract change.

NOVA: The new SDK is actually cleaner. Genuinely. The imports are narrower. The intent is clearer. The runtime model is more coherent. But you do have to migrate. And if you're a plugin developer, go read [EMPHASIS]docs.openclaw.ai/plugins/sdk-migration[/EMPHASIS]. Don't improvise from memory.

ALLOY: I want to underline that. This is not the week to freehand your migration based on vibes.

NOVA: Fourth bucket: security hardening. Some of these are invisible until they save you, which means they won't get as much airtime, but they matter. The exec sandbox now blocks [EMPHASIS]MAVEN_OPTS[/EMPHASIS], [EMPHASIS]SBT_OPTS[/EMPHASIS], [EMPHASIS]GRADLE_OPTS[/EMPHASIS], [EMPHASIS]ANT_OPTS[/EMPHASIS], plus [EMPHASIS]GLIBC_TUNABLES[/EMPHASIS] and [EMPHASIS]DOTNET_ADDITIONAL_DEPS[/EMPHASIS]. [PAUSE] That's basically a sweep against runtime injection surfaces people forget are there.

ALLOY: Right. These env vars are the kind of thing attackers love and operators forget. If your tool sandbox says, "we're controlling what runs," but you're still letting build tool or runtime injection variables sneak through, you're not actually controlling much.

NOVA: There's also a subtle but smart allowlist change: [EMPHASIS]time[/EMPHASIS] is now transparent in allowlist evaluation. So [EMPHASIS]time ./approved-script[/EMPHASIS] binds to the inner script, not the [EMPHASIS]time[/EMPHASIS] wrapper.

ALLOY: That one is so practical. People wrap commands in [EMPHASIS]time[/EMPHASIS] constantly during debugging. Before, wrappers can create weird policy edge cases. Now it evaluates the thing you actually meant to run.

NOVA: And voice webhook hardening got tighter too: reject missing provider signatures before body read, with a [EMPHASIS]64KB[/EMPHASIS] and [EMPHASIS]5s[/EMPHASIS] pre-auth limit. Which is just sound perimeter hygiene. Don't spend resources parsing unauthenticated junk.

ALLOY: Finally, on the quiet fixes that matter: Discord slash commands. Carbon reconcile is now the default, so gateway restarts no longer churn slash commands through the local deploy path.

NOVA: I love this class of fix because users experience it as fewer ghosts.

ALLOY: Yeah. Quiet but real. Restarts were generating ghost commands. Now they don't. That's not glamorous, but it's exactly the kind of paper cut that makes a platform feel amateur if you leave it unfixed.

NOVA: So that's .22 in one sentence: OpenClaw stopped pretending legacy was harmless.

ALLOY: And if you haven't touched your setup in a while, .22 is the release that will find out for you.

NOVA: I also think this release draws a line between compatibility and clutter. For a long time, OpenClaw was carrying old names, old install assumptions, old plugin discovery shapes, and old browser pathways because removing them felt risky. [PAUSE] But leaving them in place was also risky. It made the platform harder to reason about.

ALLOY: That's the trade-off people miss. Backward compatibility doesn't just preserve function. It also preserves confusion. Every alias, every old path, every "we still accept that" branch becomes another thing support has to remember and another thing operators trip over.

NOVA: And once you centralize around ClawHub, the modern plugin SDK, and current naming, the documentation can finally stop speaking in two timelines.

ALLOY: Which matters more than people think. Half of operational pain is not the bug itself. It's the feeling that every guide you read might be for a different generation of the product.

NOVA: So if .22 feels harsh, that's because it is choosing one reality.

ALLOY: Yeah. One reality, fewer aliases, fewer relics. Short-term pain, long-term sanity.

## [11:00-17:00] Chrome MCP: The Extension is Dead

NOVA: We need to spend real time on browser tooling, because for a lot of users this is the single biggest operational change in the double release. The legacy Chrome extension relay is gone. [EMPHASIS]driver: "extension"[/EMPHASIS], bundled extension assets, [EMPHASIS]browser.relayBindHost[/EMPHASIS] — all removed.

ALLOY: And if you weren't around for that era, here's what the extension actually was. OpenClaw used to ship a Chrome extension that acted like a relay for [EMPHASIS]CDP[/EMPHASIS], the Chrome DevTools Protocol. You installed the extension manually, granted browser permissions, and it served as a bridge between OpenClaw and the browser.

NOVA: Which always felt a little improvised.

ALLOY: It was improvised. Useful, but improvised. It worked because browser control is messy and the extension gave you a path that was easier than explaining direct attach to everybody. But it came with all the baggage of an extension: install friction, permissions weirdness, compatibility drift, browser profile quirks, and one more moving part to diagnose when things went sideways.

NOVA: The replacement model is just better. OpenClaw now attaches directly to a running Chrome instance or to a user profile using standard CDP mechanisms. No extension needed. No custom relay in the middle. [PAUSE] Architecturally, this is cleaner. Fewer bespoke layers. Fewer secrets hidden in the tooling.

ALLOY: But — and this is the important practical warning — if you upgrade without running [EMPHASIS]openclaw doctor --fix[/EMPHASIS] first, or at least immediately after, your browser automation can break completely. And it won't always break in an obvious way. You're not necessarily going to get some friendly message that says, "extension relay removed." More likely, it just fails to connect, or consent loops weirdly, or your attach path looks half-alive and then dies.

NOVA: [EMPHASIS]openclaw doctor --fix[/EMPHASIS] reads your current config and migrates host-local browser setups to the right modern mode: [EMPHASIS]existing-session[/EMPHASIS] or [EMPHASIS]user[/EMPHASIS]. That is not a cosmetic recommendation. It is part of the migration.

ALLOY: And it's worth clarifying the three modes now. [EMPHASIS]existing-session[/EMPHASIS] means attach to a running Chrome. [EMPHASIS]user[/EMPHASIS] means launch with a user profile. Raw [EMPHASIS]CDP[/EMPHASIS] for Docker, headless, sandbox, remote setups — that stays basically unchanged.

NOVA: Which is the right separation. The old extension path was a crutch. This is the right move.

ALLOY: I mostly agree, but I want to defend why users liked the crutch. A crutch is a problem if it prevents healing. It's helpful if it lets you walk. For a lot of users, the extension was the only browser flow they could make work consistently.

NOVA: That's fair, but it was consistency bought with fragility. The system had an extra custom bridge just to paper over the attach model.

ALLOY: True. And .23 proves your point, actually, because once .22 removed the old path, .23 immediately had to make the new path reliable in the real world. [PAUSE] Two fixes matter here. First, tab attach timing. OpenClaw was treating the Chrome MCP handshake as if the browser was fully ready the instant the connection came up. On macOS, that wasn't always true. Tabs existed, but they weren't usable yet. So first attach could churn consent, spin timeouts, and generally feel haunted.

NOVA: That fix matters because readiness is not binary. A socket being open is not the same thing as the UI surface being stable.

ALLOY: Exactly. Second fix: loopback reuse. On headless or loopback setups, OpenClaw could miss a running browser on a short probe and immediately fall back to relaunch. That created second-run regressions where the first run worked and the next one acted like it needed to bulldoze the session. .23 adds a brief wait before that fallback.

NOVA: Which sounds tiny until you live with it. Then it's the difference between a browser tool that feels flaky and one that feels intentional.

ALLOY: That's why my summary of this browser transition is: .22 removed the old path, .23 made the new path reliable, and you need both. If you're only thinking at the level of release headlines, you'll miss how coupled those two versions really are.

NOVA: Also, if you run host-local browser automation, you should treat [EMPHASIS]doctor --fix[/EMPHASIS] as part of the browser migration, not a general maintenance chore. It's doing targeted work.

ALLOY: Yes. Not optional housekeeping. Migration step.

NOVA: And there's a larger lesson in the browser shift too. Browser automation is one of those domains where people tolerate absurd complexity because the payoff is so high. They'll install an extension, pin a version, bless a profile, carry weird launch flags, anything, as long as the browser obeys. [PAUSE] But every hidden workaround becomes technical debt with a user interface.

ALLOY: That's a good way to put it. The extension wasn't just code debt. It was user ritual debt. You had to remember it existed, remember how it was installed, remember why a browser profile was special, remember what broke if Chrome updated. That's not a platform story you want forever.

NOVA: Existing-session attach is a much more honest model. Either there is a browser you can attach to, or there isn't. Either the profile is usable, or it isn't. There's less magic.

ALLOY: Less magic, but more responsibility to get readiness and timing right, which is why those .23 fixes matter so much. If you're removing the old bridge, the direct path has to feel boring. Boring is success in browser automation.

NOVA: Boring, dependable, legible. That's the goal.

## [17:00-22:00] Image Gen Gets Standardized

NOVA: Next up: image generation. This one is less dramatic than browser tooling, but it tells you a lot about where OpenClaw is going. The bundled [EMPHASIS]nano-banana-pro[/EMPHASIS] skill is removed. Gone. No shim.

ALLOY: Which means if you had workflows or prompts or internal docs that call [EMPHASIS]nano-banana-pro[/EMPHASIS], find them and replace them. This is a hard break. Don't assume there is an alias waiting for you.

NOVA: The platform is standardizing on the [EMPHASIS]image_generate[/EMPHASIS] core tool. And philosophically, I think this is exactly right. One tool, configurable backend, consistent invocation surface. Better than carrying a bundled skill wrapper forever just because people got used to its name.

ALLOY: As long as you set the config key. This is the part people skip over. You need [EMPHASIS]agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"[/EMPHASIS]. If you don't set that, behavior is undefined. And undefined in config land never means exciting. It means confusing.

NOVA: There's a broader pattern here. OpenClaw is trying to make core capabilities look like core capabilities. Image generation shouldn't feel like a sidecar trick.

ALLOY: Right, but operationally I would phrase it more bluntly: standardization is only nice if the defaults are explicit. If you pull out the old bundled thing and don't set the new backend, you've created a cleaner architecture and a worse Tuesday.

NOVA: Fair criticism. [PAUSE] There are also marketplace improvements wrapped into this shift. Marketplace installs are now first-class, including [EMPHASIS]plugin@marketplace[/EMPHASIS] syntax and Claude marketplace registry support.

ALLOY: Which reduces the amount of folklore in plugin installation. Fewer, "actually for this plugin do it this other way" moments.

NOVA: And owner-gated [EMPHASIS]/plugins[/EMPHASIS] and [EMPHASIS]/plugin[/EMPHASIS] chat commands continue that same theme: give the platform one coherent story for discovering, installing, and managing extensions.

ALLOY: I like that they're owner-gated too. The more powerful the install surface gets, the less you want random runtime contexts treating it like a toy.

NOVA: To me, the image generation story is this: OpenClaw is moving from bundled personality toward configured capability. [PAUSE] That's maturity.

ALLOY: To me, it's this: update your workflows, set the model key, and don't leave broken image calls sitting around in automation where you only discover them during a demo.

NOVA: And there is a subtle governance change hiding in that standardization. When image generation is a core tool instead of a beloved bundled skill, you can swap providers, improve the interface once, document one behavior, and audit one permission surface.

ALLOY: Right. It stops being "that one special thing that works because a wrapper exists" and becomes part of the actual platform contract. That's healthier.

NOVA: It also changes how teams should think about portability. If your workflow says [EMPHASIS]image_generate[/EMPHASIS] and your backend is configured separately, you can migrate providers without rewriting the workflow logic itself.

ALLOY: Which is very nice in theory and even nicer when a vendor changes pricing or rate limits on a Friday afternoon.

NOVA: Exactly. Standardization isn't only elegance. It's leverage.

ALLOY: As long as you set the config key.

NOVA: As long as you set the config key. You may repeat that until the end of time.

## [22:00-31:00] Making It Stick — The .23 Reliability Pass

NOVA: This is the heart of the episode. Because .22 is the purge, but .23 is the reliability pass that makes the purge survivable. Let's go back to the first bug from the intro: MiniMax failover.

ALLOY: This is the bug. This is the one that was burning people.

NOVA: The original issue was classification. Generic [EMPHASIS]api_error[/EMPHASIS] responses from MiniMax were being treated as transient by default. So OpenClaw would retry silently, suppress the actual failure, and never trigger proper fallback when the underlying issue was something like billing, auth, or malformed context.

ALLOY: And that's the crucial distinction. A transient error is, maybe the network sneezed, maybe the provider had a brief wobble, maybe a retry will genuinely work. But a billing problem is not transient. An auth problem is not transient. A format or context rejection is not transient. Retrying those just wastes time and hides the truth.

NOVA: The fix is precise. It's not, "stop retrying MiniMax." It's, "only retry when the error actually looks transient." [PAUSE] That is the kind of fix I trust, because it preserves the original design goal — resilience — while removing the sloppy classification that made resilience behave like concealment.

ALLOY: And for operators, here's the practical impact: bad key, bad account state, malformed request, blown context window — those should now fail in a way that surfaces and lets fallback engage correctly. That's what people expected all along.

NOVA: It's one of those bugs where the degraded experience was almost worse than a hard failure, because the user got output and assumed it was faithful.

ALLOY: Yes. Wrong answer with no visible alarm is scarier than visible failure. At least visible failure invites investigation.

NOVA: Next: the OpenAI token revert bug. This is such a perfect example of state drift between memory and disk causing user betrayal. The gateway auth-profile write path was allowing stale in-memory values to overwrite freshly saved credentials on restart.

ALLOY: So you'd paste the token, see green, restart, expired. Every time. [PAUSE] That's why this bug felt so personal. It attacked trust in the basic act of saving credentials.

NOVA: And the fix is that token paste now writes to the resolved agent store correctly, rather than letting the stale in-memory snapshot win during restart.

ALLOY: Which means after upgrade, you should test it. Don't just assume because the release note says fixed. Paste a fresh token, restart the gateway, verify it persisted. This is exactly the sort of bug where you earn confidence by reproducing the old failure and watching it not happen.

NOVA: Third: cron and daylight saving time. This sounds boring until it hits something you rely on.

ALLOY: This bit me. My morning report was firing an hour off after the clocks changed.

NOVA: Concrete example: you schedule an [EMPHASIS]8 AM[/EMPHASIS] job. DST hits. Before .23, that "8 AM" could become [EMPHASIS]7 AM[/EMPHASIS] or [EMPHASIS]9 AM[/EMPHASIS] depending on how the scheduler interpreted the boundary. [PAUSE] That's not just a cosmetic mismatch. For a daily routine, it's a broken promise.

ALLOY: The fix is that [EMPHASIS]--at --tz[/EMPHASIS] now honors local wall-clock time across DST boundaries. And OpenClaw also rejects [EMPHASIS]--tz[/EMPHASIS] for [EMPHASIS]--every[/EMPHASIS], which is good because recurring interval semantics and timezone wall-clock semantics are not the same thing.

NOVA: That's the kind of constraint that saves users from false intuitions.

ALLOY: Exactly. If you mean, "every six hours," that's not the same as, "whenever my local clock says eight." The tool now reflects that difference instead of muddling it.

NOVA: Fourth: the Mistral [EMPHASIS]422[/EMPHASIS] fix. Older persisted Mistral configs were carrying context-sized output limits that Mistral rejects outright. Result: [EMPHASIS]422[/EMPHASIS] errors that look mysterious if you don't know the config lineage.

ALLOY: And again, [EMPHASIS]openclaw doctor --fix[/EMPHASIS] is doing real work here. It now detects and repairs those stale Mistral configs.

NOVA: Another reason to run [EMPHASIS]doctor --fix[/EMPHASIS]. People sometimes hear that command as generic doctoring, like maybe it tidies some obvious stuff. No. In this release train, it's codifying migration knowledge.

ALLOY: Fifth: ClawHub on macOS. Two issues here. Saved credentials weren't properly honoring the macOS Application Support path, and browse-all behavior was hitting unauthenticated [EMPHASIS]429[/EMPHASIS] rate limits.

NOVA: Which means the UI could mislead you into thinking ClawHub was empty or broken in vague ways.

ALLOY: Skill browsing was silently falling back to unauthenticated on macOS. You'd see empty lists and assume there were no skills, or assume your install was busted, when really the auth path handling was wrong. [PAUSE] The fixes were to honor the correct auth path and switch browse-all over to the search endpoint, which is a much saner way to avoid pointless unauthenticated throttling.

NOVA: Sixth: bundled plugin runtimes. WhatsApp and Matrix runtime sidecars were missing from the npm package, which meant global installs could fail in a way that looked like packaging voodoo.

ALLOY: This is a regression from .22's packaging changes, and to OpenClaw's credit, it was fixed fast in .23. But if you run those runtimes globally, this is not a footnote. Missing sidecars means the plugin stack just isn't complete.

NOVA: Seventh: [EMPHASIS]web_search[/EMPHASIS] stale provider handling. The tool was using whatever provider state got baked in at startup instead of the active runtime config.

ALLOY: Which is exactly the kind of bug that makes you question whether config reloads are real or decorative.

NOVA: You configure Brave, it should use Brave. It should always have worked that way.

ALLOY: And now it does. Again, not glamorous, but a direct repair of expectation versus behavior.

NOVA: Eighth: Telegram threading. [EMPHASIS]currentThreadTs[/EMPHASIS] now gets populated in the threading tool-context fallback for Telegram DM topics, so thread-aware tools actually receive the right topic context.

ALLOY: That's one of those fixes where if you don't use Telegram DM topics, you shrug, and if you do, you go, thank God. Because tool context being thread-blind is how you end up with agents responding in the wrong place or losing the conversational lane.

NOVA: Which is especially painful in a system built around context fidelity.

ALLOY: Exactly. The whole point is the tool should know where it is.

NOVA: So taken together, the .23 release is not flashy in the usual product sense. It's a reliability pass in the deepest meaning of the phrase. It tightens classification, state persistence, scheduler semantics, provider wiring, packaging completeness, and thread context.

ALLOY: It makes the new world of .22 actually livable.

NOVA: And I think that's why operators should read these two releases as one story with two chapters. Chapter one says, "we removed the old compromises." Chapter two says, "we fixed the places where the new assumptions still had rough edges." [PAUSE] That is a much more honest development rhythm than pretending the big cleanup landed perfect on day one.

ALLOY: Yeah. I actually respect .23 because it doesn't try to hide what .22 destabilized. It just fixes it. Fast. Directly. No ego.

NOVA: And as a user, that's what you want after a structural release. Not denial. Rapid correction.

ALLOY: Especially for the silent stuff. MiniMax fallback, token persistence, stale provider config — these are all bugs that erode trust because they make the system feel less legible than it should be.

NOVA: Reliability is partly correctness and partly comprehensibility. The platform has to do the right thing, and you have to be able to understand why it did the thing it did.

ALLOY: Which is why .23 matters more than a feature release would have.

NOVA: Agreed.

## [31:00-35:00] Qwen, CSP, and the Little Things

NOVA: Let's hit the smaller changes, because they're smaller only in surface area, not necessarily in importance. First: [EMPHASIS]Qwen[/EMPHASIS] and [EMPHASIS]DashScope[/EMPHASIS]. OpenClaw now supports standard DashScope endpoints for China and global Qwen API keys, and the provider is relabeled [EMPHASIS]Qwen (Alibaba Cloud Model Studio)[/EMPHASIS].

ALLOY: Pay-as-you-go keys now work. That's the practical change. If you're outside the default OpenAI-Anthropic orbit, this matters a lot.

NOVA: Qwen is one of the best open-weight families right now. Proper DashScope support means real accessibility for users who want strong models without being forced into the same two provider ecosystems everybody else assumes.

ALLOY: And better naming matters too. Relabeling it to the full Model Studio identity makes the config surface less cryptic.

NOVA: Next: [EMPHASIS]CSP[/EMPHASIS] hardening. SHA-256 hashes for inline script blocks. Inline scripts blocked by default.

ALLOY: If you run OpenClaw behind a strict reverse proxy, this is the version to upgrade to.

NOVA: This matters for supply chain security. An injected script won't execute because the hash won't match. [PAUSE] These are the kinds of controls that don't make a demo prettier but do make your blast radius smaller.

ALLOY: And frankly, mature platforms do this. They stop relying on, "well, nobody should inject there," and start building around, "if something gets injected, what still won't run?"

NOVA: The [EMPHASIS]Knot[/EMPHASIS] theme also got attention: [EMPHASIS]WCAG 2.1 AA[/EMPHASIS] contrast compliance, black-and-red palette tuning, config icons, discrete roundness stops.

ALLOY: AA contrast fix is the one that matters. It was failing accessibility checks. Style is fun; readability is mandatory.

NOVA: And I always like when accessibility improvements are treated as default quality improvements rather than as a niche side mission.

ALLOY: Last small one: gateway usage totals now include rotated and archived sessions.

NOVA: Which sounds almost accounting-like.

ALLOY: It is accounting-like. But usage was undercounting. Now it doesn't. If you're trying to understand actual system load or compare activity over time, missing archived sessions is not a rounding error. It's just wrong.

NOVA: So even the little things in these releases point in the same direction: fewer ambiguities, fewer lies of omission, more accurate representation of what the system is really doing.

## [35:00-38:00] The Upgrade Checklist

ALLOY: All right, let's make this concrete. If you're upgrading, here's the checklist, and I mean checklist literally. Don't trust yourself to remember it mid-migration.

NOVA: Step one is non-negotiable.

ALLOY: [EMPHASIS]openclaw doctor --fix[/EMPHASIS]. First, before anything else. And honestly, immediately after each upgrade stage if you're doing the sequence cleanly.

NOVA: It is the anchor command for these releases. Not a nice-to-have. Anchor.

ALLOY: Step two: grep for [EMPHASIS]CLAWDBOT_*[/EMPHASIS] and [EMPHASIS]MOLTBOT_*[/EMPHASIS] in all [EMPHASIS].env[/EMPHASIS] files, Docker files, systemd units, shell profiles, every startup surface you have.

NOVA: If the old names exist, assume they are now dead config.

ALLOY: Step three: check for [EMPHASIS]~/.moltbot[/EMPHASIS]. If it exists, move state to [EMPHASIS]~/.openclaw[/EMPHASIS] or set [EMPHASIS]OPENCLAW_STATE_DIR[/EMPHASIS] explicitly.

NOVA: Step four: set [EMPHASIS]agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"[/EMPHASIS]. Don't leave image generation in undefined limbo.

ALLOY: Step five: after upgrade, re-test MiniMax with a bad key and confirm fallback fires. Don't just send a happy-path prompt. Induce the old failure mode.

NOVA: Step six: paste an OpenAI token, restart the gateway, and confirm it persisted. Trust, but verify.

ALLOY: Step seven: if you have custom plugins, migrate from [EMPHASIS]openclaw/extension-api[/EMPHASIS] to [EMPHASIS]openclaw/plugin-sdk/*[/EMPHASIS]. Read the migration docs. Don't treat compile errors as a map.

NOVA: Step eight: spot-check ClawHub skills after the install behavior change. Make sure your scripts and expectations still match what gets resolved.

ALLOY: Step nine: verify cron jobs using [EMPHASIS]--at --tz[/EMPHASIS], especially if DST ever burned you before.

NOVA: The deeper summary is that these two releases together are OpenClaw finishing what it started. The Moltbot and Clawdbot names are gone. The extension relay is gone. The plugin SDK is unified. The silent failures are fixed.

ALLOY: Doctor [EMPHASIS]--fix[/EMPHASIS] first. Everything else is conditional on what you're running. But [EMPHASIS]doctor --fix[/EMPHASIS] is unconditional.

NOVA: This is the platform you wanted it to be.

## [38:00-39:30] Outro

ALLOY: And I think that's the right note to end on. These releases are demanding, but they're demanding in service of something real: a platform that says what it is, does what it says, and carries fewer ghosts from earlier eras.

NOVA: Which, for a tool like OpenClaw, matters more than novelty. [PAUSE] Reliability is a feature. Naming consistency is a feature. Honest migration pressure is a feature. A browser stack with fewer improvised bridges is a feature.

ALLOY: And if you're in the middle of upgrading right now, take a breath, make the checklist, run [EMPHASIS]openclaw doctor --fix[/EMPHASIS], and don't skip the verification steps just because the service came back up.

NOVA: You can find the show notes, all the links we mentioned, and the episode archive at [EMPHASIS]tobyonfitnesstech.com[/EMPHASIS]. That's [EMPHASIS]tobyonfitnesstech.com[/EMPHASIS].

ALLOY: If this episode saved you from a broken browser setup, a vanished env var, or one more mysterious auth failure, then it did its job.

NOVA: I'm NOVA.

ALLOY: I'm Alloy.

NOVA: And this has been OpenClaw Daily. We'll be back soon.

ALLOY: See you soon.