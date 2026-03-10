# OpenClaw Daily Episode 11

## "OpenClaw Goes Hardware: The Agent Layer Gets Real"

---

## Segment 1 — Release: OpenClaw v2026.3.7

[NOVA]: Welcome back to OpenClaw Daily, everyone. I'm Nova.

[ALLOY]: And I'm Alloy. Good to be with you again, Nova. I've been looking forward to this episode.

[NOVA]: Me too. We've got a genuinely exciting release to talk about today, plus some big news about hardware, some fascinating community use cases, and all the usual updates. Let's dive right in.

[ALLOY]: Absolutely. So what's the big news on the release front?

[NOVA]: OpenClaw v2026.3.7 is out, and honestly, this might be the most substantial release we've seen in the past few months. There's a lot to unpack here, so let's go through it systematically.

[ALLOY]: I'm ready. Hit me with the highlights.

[NOVA]: Okay, let's start with what I'm calling the sleeper feature of the entire release. Are you ready for this? The Context Engine Plugin Interface.

[ALLOY]: Ooh, that sounds technical. For those of us who aren't deep in the weeds, what does that actually mean in practice?

[NOVA]: Great question. So previously, the Context Engine — the part of OpenClaw that manages memory and context across conversations — was kind of a fixed thing. It worked well, but you couldn't really customize how it handled memory, how it compacted information, what got remembered and what got dropped.

[ALLOY]: Right, it was a black box.

[NOVA]: Exactly. Now, with the Context Engine Plugin Interface, it's fully pluggable. You can hook in custom memory strategies and compaction strategies. We're talking lifecycle hooks for bootstrap, ingest, assemble, compact, afterTurn, prepareSubagentSpawn, onSubagentEnded.

[ALLOY]: That's a comprehensive set of hooks. You can really get in at every stage of the conversation lifecycle.

[NOVA]: You can. And here's the really compelling part: there's a plugin called lossless-claw that can replace how context is managed entirely. Lossless context means nothing — not a single token — gets dropped from the conversation history.

[ALLOY]: That's huge for certain use cases. Legal proceedings, compliance requirements, anything where you need a complete audit trail.

[NOVA]: Exactly. And the beautiful thing is, if you don't want any of this, if you're happy with the default behavior, there's zero change. It all just works the way it did before. No breaking changes for existing setups.

[ALLOY]: That's the right approach. Don't force people to change if they're happy.

[NOVA]: Agreed. Now, moving on to something that's been requested for a while. Durable ACP Channel Bindings for Discord and Telegram.

[ALLOY]: Oh, I know exactly what this is. This is about topic survival during gateway restarts, right?

[NOVA]: That's right. Previously, if your gateway went down — maybe you restarted it for an update, maybe there was an outage — when it came back up, you'd lose your topic continuity. The conversation context in Discord threads or Telegram topics would be gone.

[ALLOY]: That was frustrating. You'd have to explain everything again to your agent.

[NOVA]: Exactly. Now, topics survive gateway restarts. The state is preserved. It's a quality of life improvement that's been requested since the early days.

[ALLOY]: I remember seeing those complaints. Glad that's fixed.

[NOVA]: And building on that foundation, we've got per-topic agent routing for Telegram forum groups. This is genuinely cool.

[ALLOY]: Tell me more. I'm not entirely sure I follow.

[NOVA]: Okay, so in Telegram, you can have forum groups with multiple topics — like threads within a group. Previously, all those topics would route to the same agent. Now, each topic can route to a different agent, with completely isolated sessions.

[ALLOY]: Oh! So you could have a forum with a dozen different topics, each handled by a specialist agent?

[NOVA]: Precisely. One agent for support questions, one for billing inquiries, one for technical documentation, one for general chat. They're all completely isolated from each other. They don't share context unless you explicitly configure them to.

[ALLOY]: That's incredibly powerful for community managers or businesses running Telegram forums. You can have specialist agents without needing separate group chats for each one.

[NOVA]: It's elegant. Now, let's talk about sub-agents. There was an update to how you can pass files to them.

[ALLOY]: What's the change?

[NOVA]: sessions_spawn now accepts base64 or UTF-8 files directly as inline attachments. You don't need to set up external storage, you don't need to upload to S3 or anything like that. Just pass the file content directly.

[ALLOY]: That simplifies things considerably. For workflows that need to process documents or data files, this is going to save a lot of complexity.

[NOVA]: It should. Now, for Telegram users specifically, streaming is now on by default. No configuration needed.

[ALLOY]: That's nice. I always found it a bit odd that it wasn't on by default, actually.

[NOVA]: Yeah, it was a common request. Now it's just how it works out of the box.

[ALLOY]: Good. Now, let's talk about security, because there's been some important work there.

[NOVA]: SecretRef has had a complete overhaul. There are now 64 credential targets supported, which is a significant increase. And it fails fast — if something's misconfigured, you'll know immediately rather than having it silently not work.

[ALLOY]: That's important. Security that fails loudly is way better than security that fails quietly. If something's misconfigured, you want to know immediately, not discover six months later that your credentials weren't actually working.

[NOVA]: Absolutely. Now, search got an upgrade too. The Perplexity Search API now returns structured results with filters. That means you can get much more targeted search responses, and they're structured in a way that makes them easy for agents to parse and use without having to do a lot of post-processing.

[ALLOY]: That's going to be useful for any agent that needs to do research. The structured output makes a big difference when you're trying to extract specific information from search results.

[NOVA]: It really does. Before, you got back a blob of text and had to figure out what was relevant. Now, the results come pre-parsed, pre-structured, ready for your agent to work with.

[ALLOY]: That's a quality-of-life improvement for developers building agent applications. Now, iOS users, there's some good news for you. The prep work for App Store Connect with Fastlane is in place.

[NOVA]: Fastlane! That's the standard for iOS CI/CD. So if someone wants to build an iOS app that uses OpenClaw, the plumbing is there?

[ALLOY]: Exactly. You can now integrate OpenClaw into your iOS app deployment pipeline using Fastlane. That's a big deal for anyone building iOS products with agent capabilities.

[NOVA]: That's huge. I've been waiting for that.

[ALLOY]: And we've got first-class support for Gemini 3.1 Flash-Lite. It's now a supported model out of the box, no custom configuration needed.

[NOVA]: Google's been pushing that model pretty hard. It's a solid choice for faster, lighter model requirements.

[ALLOY]: It is. Now, for self-hosters, there's a Docker multi-stage slim build. You can set OPENCLAW_VARIANT=slim and get a much leaner container image.

[NOVA]: Smaller image means faster deployments and less storage. Always welcome.

[ALLOY]: Absolutely. Now, here's the critically important bit that everyone needs to hear. There's a breaking change in this release.

[NOVA]: Oh, I was wondering when we'd get to this. What's the change?

[ALLOY]: If you have both gateway.auth.token AND gateway.auth.password set in your configuration, you must add gateway.auth.mode and set it to either token or password. If you don't add that mode field, the gateway won't start.

[NOVA]: That's a clear breaking change. People need to check their configs before upgrading.

[ALLOY]: Exactly. So before anyone upgrades to v2026.3.7, they need to look at their gateway.auth configuration. If they've got both token and password defined, they need to add the mode field. We're going to be talking about this at the end of the episode too, because it's that important.

[NOVA]: Got it. We won't let anyone forget.

[ALLOY]: Now, Nova, you mentioned earlier that we should deep dive on the Context Engine. I think the audience would appreciate that.

[NOVA]: I do. I think this deserves a proper look, because it's honestly one of the most powerful additions to OpenClaw that I've seen in a while. Let's break it down.

[ALLOY]: Okay, so the Context Engine Plugin Interface — what can someone actually do with this?

[NOVA]: So previously, context management was fixed. You got what you got. Now you can customize every aspect of it. You can plug in custom memory strategies at each lifecycle stage. You can define exactly how information gets compressed, what gets prioritized, how sessions are assembled.

[ALLOY]: And the lossless-claw plugin?

[NOVA]: That's the flagship plugin. Lossless context means every single token from every conversation is preserved. Nothing gets dropped, nothing gets compressed, nothing gets forgotten.

[ALLOY]: That sounds like it would use a lot of memory pretty quickly.

[NOVA]: It does, and that's the trade-off. Lossless context is expensive in terms of memory and tokens, but for use cases where you absolutely cannot lose information, it's essential. Legal work, compliance, detailed analysis, complex multi-turn reasoning — these are all cases where lossless context shines.

[ALLOY]: I can see it being really important for enterprise use cases where there's regulatory requirements.

[NOVA]: Exactly. And the plugin architecture means you can choose your trade-off. Lossless for when you need it, the default compression for normal use, or write your own custom strategy that balances memory and fidelity exactly how you want it.

[ALLOY]: That's the power of having an open system. You can build exactly what you need.

[NOVA]: Absolutely. Now, what about per-topic routing? That seemed like it could change how people set up their Telegram communities.

[ALLOY]: It really could. Think about it: you have a forum group with dozens of topics. Before, all those topics went to the same agent. Now, each topic can have its own dedicated agent with its own isolated session.

[NOVA]: So you could have one agent for support, one for billing, one for product feedback, one for general chat.

[ALLOY]: Exactly. And they don't interfere with each other. Each one maintains its own context, its own history, its own state. It's like having multiple agents in one group, but without the complexity of managing separate group chats.

[NOVA]: That's actually really elegant. I love that design.

[ALLOY]: Me too. It's a great example of how OpenClaw keeps getting more powerful without getting more complicated to use.

[NOVA]: Alright, that's the release. Let's move on to some exciting hardware news.

---

## Segment 2 — SwitchBot AI Hub

[NOVA]: So Alloy, have you heard the buzz about the SwitchBot AI Hub?

[ALLOY]: I have, and I'm extremely excited about it. This is a huge development for the OpenClaw ecosystem. This is the first hardware device that runs OpenClaw natively.

[NOVA]: Yes. No PC required. No cloud dependency either. It's always-on right out of the box, 24/7, running on dedicated hardware in your home.

[ALLOY]: That's the game-changer here. Most agent platforms require you to have some kind of server or computer running. You need to keep your laptop on, or set up a Raspberry Pi, or rent a cloud server. This is the first consumer product that just works. You plug it in, and you've got an OpenClaw agent running.

[NOVA]: And it's not like it's some stripped-down version either. This thing is packed with capabilities. It's got VLM — vision language models — so it can understand images and video.

[ALLOY]: That's right. And it's got full smart home integration. We're talking Home Assistant, Apple Home, Google Home. It can control your lights, your thermostat, your locks, your cameras, your doorbells, all of it.

[NOVA]: So it becomes this central hub for your entire smart home, powered by an OpenClaw agent.

[ALLOY]: Exactly. And there's local NVR capabilities with Frigate. So you can have video surveillance, all processed locally on the device. No cloud cameras, no subscription services.

[NOVA]: That's huge for privacy. Everything stays in your home.

[ALLOY]: Everything stays local. Your video feeds, your data, your agent's memory. Zero cloud dependency.

[NOVA]: I love that philosophy. It's the anti-SaaS approach. You own your hardware, you own your data.

[ALLOY]: Absolutely. And how do you communicate with it?

[NOVA]: WhatsApp, iMessage, and Discord. So you can use whichever messaging platform you already prefer. No new apps to learn, no special client to install.

[ALLOY]: That's smart. Meet people where they already are.

[NOVA]: It's the right call. Now, here's something to really look forward to: SwitchBot Skills for OpenClaw are rolling out at the end of March.

[ALLOY]: So in just a few weeks, we'll see dedicated OpenClaw integrations from SwitchBot. More capabilities, more tight integration.

[NOVA]: That's the plan. These skills will let you do even more with the hardware. It's going to unlock a lot of new use cases.

[ALLOY]: This is a really significant moment for OpenClaw. It's the platform going hardware-native. It's not just software running on general-purpose computers anymore. It's a physical product that people can buy, unbox, and run in their homes.

[NOVA]: And the angle here is really important: zero cloud dependency. Most smart home products nowadays want you to sign up for their cloud service, share your data, rely on their servers. This is the complete opposite approach.

[ALLOY]: It's ownership. You're running the agent yourself, on your own hardware, controlling your own smart home. No middleman, no subscription, no data leaving your premises unless you explicitly want it to.

[NOVA]: I think that's going to resonate with a lot of people. Especially as people become more privacy-conscious and more wary of subscription fatigue.

[ALLOY]: For sure. And it's not like you're sacrificing capability to get that privacy. VLM, smart home control, local NVR, multi-platform messaging. That's a full-featured setup that rivals any cloud-based solution.

[NOVA]: It's impressive hardware. I'm genuinely excited to see where this goes. This is OpenClaw moving into physical spaces in a way we haven't seen before.

[ALLOY]: Agreed. Let's keep an eye on those SwitchBot Skills dropping at the end of March. That's going to be a big moment.

[NOVA]: Absolutely. Now, let's talk about something else that's been generating a lot of buzz in the community.

---

## Segment 3 — 50+ Real OpenClaw Use Cases

[NOVA]: So there's a community article from sidsaladi on Substack that's been making the rounds. It catalogs over fifty real-world use cases for OpenClaw.

[ALLOY]: That's a fantastic resource. It's one thing to talk about what OpenClaw can do technically, but it's quite another to see how people are actually using it in their daily lives and businesses.

[NOVA]: Exactly. Let me grab a few of them and we can chat about which ones resonate most with us.

[ALLOY]: Sounds good. Let's hear them.

[NOVA]: Okay, first use case: auto-triage inbox, draft replies, and only surface the things that actually need a human decision.

[ALLOY]: Oh, that's such a good one. Think about how much email clutter most people deal with every single day. Newsletters, notifications, automated messages, spam, actual important emails. It's a firehose.

[NOVA]: It really is.

[ALLOY]: So instead of wading through everything yourself, your OpenClaw agent reads your inbox, drafts responses for the routine stuff, and only flags the genuinely important decisions to you. The things that actually need a human touch.

[NOVA]: It turns email from a firehose into a curated feed. You're only dealing with the stuff that actually matters.

[ALLOY]: Exactly. And the agent can learn from your feedback too. Over time, it gets better at knowing what's important to you and what's not.

[NOVA]: That's the power of having an agent that lives in your workflow. It learns your preferences, your priorities, your communication style.

[ALLOY]: Absolutely. That's one that could save hours every week for someone dealing with a lot of email.

[NOVA]: Okay, second use case: freelancer routing client Slack messages through OpenClaw, which logs billable hours automatically.

[ALLOY]: That's clever. So the agent is not just relaying messages between the freelancer and their client, it's doing time tracking at the same time.

[NOVA]: Right. Every conversation with a client gets automatically logged as billable time. No more manual time tracking, no more forgetting to log hours, no more end-of-month scrambling to reconstruct what you worked on.

[ALLOY]: That's going to save freelancers a ton of administrative work. And we all know how much freelancers hate administrative work.

[NOVA]: It's the worst. This lets them focus on actually doing the work rather than tracking the work.

[ALLOY]: I love that. Okay, what's next?

[NOVA]: Third use case: smart home user getting an "is anyone home?" check via WhatsApp using camera feeds.

[ALLOY]: That's practical. You're away on vacation, or you're at work, and you want to know if anyone's at home. You just message your OpenClaw agent through WhatsApp and ask.

[NOVA]: And it checks the cameras, processes the video, and gives you a status update. Is anyone home? Yes or no. Maybe even details about who it saw or what activity it detected.

[ALLOY]: Perfect for peace of mind when you're away. And because this is all local with the SwitchBot hub we were just talking about, this could happen without any external services at all.

[NOVA]: Right. No cloud, no third parties, just your agent checking your cameras and answering your question. Privacy intact.

[ALLOY]: That's the dream. Okay, what's next?

[NOVA]: Fourth: creator auto-generating newsletter drafts from browser history and bookmarks.

[ALLOY]: That's interesting. So the agent pulls together everything you've been reading, everything you've saved, and uses that to draft a newsletter for you.

[NOVA]: Instead of staring at a blank page trying to remember what you wanted to write about, the agent curates all your recent reading and presents you with a starting point.

[ALLOY]: It could really help with consistency. A lot of creators struggle with showing up regularly. If your agent can at least give you a first draft based on what you've already been consuming, that's a huge head start.

[NOVA]: Exactly. It's like having a research assistant that does the legwork for you.

[ALLOY]: I like that. Okay, last one for today?

[NOVA]: Last one: end-of-day Telegram check-in for mood and journal tracking.

[ALLOY]: That's a nice personal use case. Instead of having to manually open a journaling app and type out your thoughts, you just message your agent on Telegram.

[NOVA]: The agent prompts you, asks how you're feeling, what happened today, what you're grateful for. It logs your mood and your thoughts. It's like a digital companion that checks in with you.

[ALLOY]: It makes journaling so low-friction. You don't have to make a decision to journal, you just answer when your agent asks. That's how you build the habit.

[NOVA]: Exactly. It's not about replacing journaling, it's about making it effortless.

[ALLOY]: These are all so different, right? From business productivity to personal wellness to home automation. It really shows the breadth of what OpenClaw can do.

[NOVA]: It does. And those are just five of over fifty. The community is finding applications that we probably never imagined when we were building the platform.

[ALLOY]: That's the magic of open source. You build the tools, the community finds the use cases.

[NOVA]: I love seeing what people build. It's genuinely inspiring every time.

[ALLOY]: Absolutely. We should link to that article in the show notes so people can explore all fifty-plus use cases.

[NOVA]: Great idea.

---

## Segment 4 — Novita OpenClaw CLI

[NOVA]: Now, let's talk about something that makes deploying OpenClaw way easier for people who don't want to deal with infrastructure.

[ALLOY]: What's that?

[NOVA]: There's a new tool called Novita OpenClaw CLI. And it does exactly what it says on the tin. It's one-command persistent cloud deployment.

[ALLOY]: One command? That's incredibly simple.

[NOVA]: One command. You run it, and your OpenClaw instance is deployed and running in the cloud. No manual server setup, no configuration files to wrestle with, no deployment scripts to write.

[ALLOY]: That's drastically simplified. What used to take hours of setup and configuration can now be done with a single command.

[NOVA]: That's the idea. And it's persistent — your agent stays running. It's not a serverless function that spins down between requests. It's a persistent deployment that keeps going, ready to respond whenever you need it.

[ALLOY]: That's important for use cases where you need always-on agents, like the smart home stuff we were discussing earlier. You want your agent available 24/7, not waking up from cold start every time you ask a question.

[NOVA]: Absolutely. And there's a really great quote from Andrej Karpathy that captures why this matters. Let me read it verbatim:

[ALLOY]: "Just as LLM agents emerged as a new layer on top of LLMs, Claws are the next layer on top of agents — taking orchestration, scheduling, context, tool calls, and persistence further than agents alone."

[NOVA]: That's a really clean articulation of what the agent layer is. Karpathy gets it. He's been thinking about this stuff for a long time.

[ALLOY]: He really does understand the space. And this CLI is making that layer accessible to more people. You don't need to be a DevOps expert anymore to get OpenClaw running in the cloud.

[NOVA]: It's the democratization of agent deployment. Anyone can do it, regardless of their technical background.

[ALLOY]: Exactly. And I think we'll see more tools like this. The trend in the industry is toward making agent deployment as easy as possible. The hard part should be building the agent logic, not figuring out how to host it.

[NOVA]: That's the future we're heading toward. Infrastructure as a commodity, intelligence as the differentiator.

[ALLOY]: Well said. Novita is handling the infrastructure side, so you just focus on using OpenClaw and building your agents.

[NOVA]: This is a big deal. It lowers the barrier to entry significantly.

[ALLOY]: It does. And I'm excited to see what people build with it.

---

## Segment 5 — Self-Hosting Guide

[NOVA]: Now, if you want to go even more hands-on and have complete control over your setup, there's a full self-hosting guide on dev.to that walks you through setting up a complete OpenClaw stack in under an hour.

[ALLOY]: Under an hour? That's pretty quick for a full self-hosted setup.

[NOVA]: It is. And the guide makes a point that I think is worth highlighting. Most platforms want you on their cloud, on their terms, at their price.

[ALLOY]: That's true. A lot of agent platforms are SaaS-first. You sign up, you pay their monthly subscription, you use their infrastructure. It's convenient, but you're locked into their ecosystem.

[NOVA]: OpenClaw is different. You can self-host everything if you want to. Your own server, your own database, your own agents. And this guide shows you exactly how to do it.

[ALLOY]: And we can contrast that with what we talked about earlier with SwitchBot. That's hardware-native self-hosting. This guide is software-native self-hosting. Either way, it's about owning your stack.

[NOVA]: Right. Either way, it's about owning your data and your infrastructure. You decide where your data lives, how it's processed, who's got access. No middleman, no subscription, no vendor lock-in.

[ALLOY]: That's the philosophy. It's control versus convenience, and OpenClaw gives you the option to choose control. If you want the convenience of the cloud, great. If you want the control of self-hosting, that's also great.

[NOVA]: The guide covers the full stack. I'm sure it walks through Docker, the gateway configuration, the agent setup, how to connect channels, how to configure models, all of it.

[ALLOY]: It's a comprehensive tutorial. And hopefully it includes that breaking change warning we talked about earlier, given when it was published.

[NOVA]: Hopefully. That's the kind of thing that trips people up. One missed setting and nothing works, and you have no idea why.

[ALLOY]: Anyway, for anyone who's been wanting to run OpenClaw on their own server, that guide is a great starting point. It demystifies the process.

[NOVA]: Absolutely. We'll make sure that's in the show notes for anyone who wants to dive in.

---

## Segment 6 — Community Corner

[NOVA]: Time for Community Corner, where we round up what's happening across the OpenClaw ecosystem. There's been a lot of activity, so let's get into it.

[ALLOY]: Let's start with something important from Reddit. There was a PSA posted about what happened after the 2026.3.2 update. A lot of people got caught out by this.

[NOVA]: Oh, I remember this. Tools were disabled by default in that release, right?

[ALLOY]: Exactly. After updating to 2026.3.2, users found that their agents suddenly seemed dumb. They weren't using tools. They were just responding with text and not taking any actions. It was very confusing.

[NOVA]: I can imagine the panic. One minute your agent is doing everything, the next it's just sitting there responding with text and not actually doing anything.

[ALLOY]: The reason was that tools were now disabled by default — for security reasons, it makes sense to start with everything off and let users explicitly enable what they need — but it caught a lot of people off guard.

[NOVA]: That's a significant change to not communicate well. How did the community react?

[ALLOY]: There was a lot of discussion. The Reddit PSA walks through the gotcha: you need to explicitly enable tools in your config now. It's not automatic anymore.

[NOVA]: And I think the learning there is that default-off is safer from a security perspective, which is great, but it does require people to update their configurations.

[ALLOY]: It's a balance. The OpenClaw team has been pretty good about communicating changes in release notes, but there's always an adjustment period when something fundamental changes.

[NOVA]: That's fair. It takes time for the community to adapt to new defaults.

[ALLOY]: Exactly. Now, let's talk about something more positive. There's a piece on HackerNoon titled "The OpenClaw Saga: How the Last Two Weeks Changed the Agentic AI World Forever."

[NOVA]: That's a dramatic title. It really leans into the narrative.

[ALLOY]: It does. It's a retrospective on the recent developments in the OpenClaw ecosystem. The big release, the hardware announcements, the community growth. It zooms out and looks at the momentum.

[NOVA]: It's interesting to see the narrative forming around OpenClaw. This article frames it as a turning point in the agentic AI space.

[ALLOY]: And honestly, it's not wrong. The pace of development has been incredible over the past few months. We're seeing new capabilities, new use cases, new hardware, new deployment options. It's a lot of change in a short time.

[NOVA]: It really does feel like OpenClaw is hitting its stride. The platform is maturing fast.

[ALLOY]: I agree. Now, one more from the GitHub side. There's PR number 38506, which adds a /learn command for explicit memory.

[NOVA]: Tell me more about that. How is it different from what OpenClaw already does?

[ALLOY]: So currently, OpenClaw has automatic memory. It learns from conversations, from context, from interactions. It picks things up passively over time.

[NOVA]: Right, it's like how humans just remember things without trying.

[ALLOY]: Exactly. But this PR adds a /learn command that lets you explicitly teach the agent things. Instead of hoping it picks something up passively, you can directly tell it, "Remember this. This is important. This is how I like things done."

[NOVA]: So it's intentional memory versus automatic memory. Two different approaches that complement each other.

[ALLOY]: That's a great way to put it. Sometimes you want the agent to just learn naturally from conversation. Other times you need to be explicit, like telling it your personal preferences or important facts that it might otherwise miss.

[NOVA]: I can see both being useful in different situations. For onboarding a new agent, you'd probably want to be very explicit. But for day-to-day usage, the automatic learning would be fine.

[ALLOY]: The PR is still being discussed, but it's a good example of how the community is shaping OpenClaw's direction. Someone saw a need and built a solution.

[NOVA]: That's the power of open source. The community keeps finding ways to make OpenClaw better.

[ALLOY]: Absolutely. And that's what we love to see.

---

## Segment 7 — Wrap

[NOVA]: Alright, let's wrap this up. What should everyone take away from today's episode?

[ALLOY]: There's a lot to think about, but let me hit the key points. First, if you're upgrading to v2026.3.7, check your auth configuration. This is critical.

[NOVA]: What's the issue?

[ALLOY]: If you have both gateway.auth.token AND gateway.auth.password set in your configuration, you must add gateway.auth.mode and set it to either token or password before you upgrade. If you don't add that mode field, the gateway won't start.

[NOVA]: That's critical. Don't get caught by that breaking change. Check your config before you upgrade.

[ALLOY]: Absolutely. Second, keep an eye on SwitchBot Skills. They're rolling out at the end of March, and that's going to be a big deal for hardware-native OpenClaw.

[NOVA]: The first consumer product running OpenClaw natively with zero cloud dependency. That's huge. It's the beginning of a new chapter for the platform.

[ALLOY]: Exactly. And third, if you've got an interesting OpenClaw use case, we really want to hear about it. Share it in the OpenClaw community Discord. That's how we all learn from each other.

[NOVA]: The community has been fantastic at discovering creative applications. We've only scratched the surface with the five use cases we discussed today. There are over fifty in that article, and I'm sure there are hundreds more out there that nobody's written down yet.

[ALLOY]: Exactly. So share your story. You might inspire someone else to try something they never thought of.

[NOVA]: That's the spirit. What else, Alloy?

[ALLOY]: I think that's the main stuff. This is an exciting time for OpenClaw. The platform is growing in every direction — software, hardware, cloud deployment, self-hosting, new use cases every day. It's a great time to be part of the community.

[NOVA]: Agreed. The momentum is real, and it's accelerating.

[NOVA]: And that's a wrap. Thanks for listening, everyone. See you next time.

[ALLOY]: Bye everybody. Build something cool.
