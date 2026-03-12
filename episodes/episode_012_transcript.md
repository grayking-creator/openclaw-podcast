# OpenClaw Daily Episode 12

## "New Free Models, Multimodal Memory, and Community Automations"

---

## Segment 1 — Release: OpenClaw v2026.3.11

[NOVA]: Welcome back to OpenClaw Daily, everyone. I'm Nova.

[ALLOY]: And I'm Alloy. Great to be here with you, Nova. I've been looking forward to this episode because I heard there's some exciting stuff in this release.

[NOVA]: There really is. Version 2026.3.11 dropped, and beyond all the usual improvements and fixes, there are some genuinely exciting developments that I want to make sure we explore properly. We're going to talk about brand new free models that just dropped, some really cool community automation stories, the new multimodal memory feature, and developer tooling improvements. So let's dig in.

[ALLOY]: I'm ready. But first, I have to say — the OpenClaw community just keeps amazing me. Every week I see incredible creative ways people are using this tool.

[NOVA]: Absolutely. It's one thing to build a powerful platform, but it's something else entirely to see what thousands of creative users do with it. This week, I want to celebrate some of that work. There's a project called BetterClaw that tracks OpenClaw automations, and they recently ranked the top ten use cases that are saving people real time in their daily lives. I want to highlight a few of these because I think they'll inspire you.

[ALLOY]: Let's hear them. I'm curious which ones made the top ten.

[NOVA]: First up: morning briefings. This is one of the most popular automations, and honestly, it's the one that makes the most sense once you hear about it. People have set up OpenClaw to generate a personalized morning briefing every day. It pulls from their calendar, from their email, from any relevant news sources they've configured, and it synthesizes all of that into a coherent summary that they can read over coffee.

[ALLOY]: So it's not just reading off your calendar? It's actually useful?

[NOVA]: It's way more than that. It might say "you have a lunch meeting with Sarah at noon, but looking at your recent emails, you haven't confirmed yet — here's a draft response you can send." Or "your daughter's soccer practice was moved to Thursday this week — I updated the family calendar." It knows context. It knows preferences. It can draft emails. It can check traffic. It's like having a hyper-competent personal assistant who wakes up before you do and has already handled a bunch of small stuff so that your morning is less chaotic.

[ALLOY]: That's the dream. I think everyone can relate to those frazzled mornings where you're scrambling to figure out your day. The fact that an AI can handle all that prep work for you is genuinely life-changing for some people.

[NOVA]: People who use this say it genuinely changes their mornings. They feel less frazzled, less reactive, more prepared. And honestly, that's exactly what automation should do — free up your mental energy for the stuff that actually matters.

[ALLOY]: Okay, what's next on the list?

[NOVA]: Second: email triage. This is a big one. The automation connects to your email account and uses the AI agent to analyze incoming messages in real time. It can categorize emails, flag urgent ones, draft responses to routine inquiries, and even archive or unsubscribe from junk automatically.

[ALLOY]: But it's not just doing it blindly, right? There's customization involved?

[NOVA]: Exactly. People have configured it with their own rules, their own priorities, their own voice. Some people flag anything from their boss or their clients as high priority. Others auto-respond to newsletter signups or promotional emails. Some handle appointment scheduling by extracting details from emails and proposing times on the calendar. The level of customization is what makes this powerful.

[ALLOY]: So it's not a one-size-fits-all inbox zero machine. It's a personal assistant that learns your preferences.

[NOVA]: Precisely. And because it's running locally, your email data never leaves your machine. That's a big deal for people who are paranoid about privacy — which, let's be honest, should be all of us these days.

[ALLOY]: That privacy aspect is huge. You're getting all this utility without sacrificing your data to some third party. That's the right trade-off.

[NOVA]: Third: the family calendar assistant. This is honestly one of my favorites because it's so relatable. Families have calendars. Families have schedules. And families, especially families with kids, have a lot of chaos.

[ALLOY]: Tell me more. How does this work in practice?

[NOVA]: The family calendar assistant connects to shared calendars — Google Calendar, Apple Calendar, whatever you're using — and acts as a central coordinator. It can check for conflicts, suggest optimal times for activities, remind people about upcoming events, and even handle the back-and-forth of scheduling.

[ALLOY]: So it's basically coordinating all the moving pieces of a family's life?

[NOVA]: Exactly. Picture this: your kid wants to have a friend over, your spouse has a work deadline, and you have a gym session you don't want to skip. The assistant can look at all of those constraints and say "hey, Saturday afternoon from 2 to 4 works for everyone." It can send the invites. It can remind everyone. It can handle the logistics. And because it has access to messaging, it can even text or message the family members directly.

[ALLOY]: That's the invisible labor of family coordination, handled by an AI. That's pretty cool. It sounds trivial until you live with it, and then you realize how much mental overhead it saves.

[NOVA]: That's exactly it. Fourth: the self-healing home server. Okay, this one is for the more technical folks, but it's genuinely impressive.

[ALLOY]: I'm intrigued. What does self-healing mean in this context?

[NOVA]: People are running OpenClaw on home servers — maybe a Raspberry Pi, maybe a mini PC in their closet, something that runs 24/7 — and they've configured it to monitor the health of their home network and services. We're talking about monitoring whether certain services are up or down, checking disk space, checking memory usage, watching for specific error patterns in logs.

[ALLOY]: And when something goes wrong, it can take action?

[NOVA]: When something goes wrong, the AI can take action. It can restart a service. It can clear a cache. It can send an alert. It can even try to diagnose the issue based on log patterns. The "self-healing" part is that it's not just alerting a human — it's actually attempting to fix things automatically.

[ALLOY]: Obviously you want safeguards and override controls, but for home labs and personal infrastructure, this is incredibly useful. If you've ever woken up to a crashed service or a full disk that took forever to diagnose, you know why this matters.

[NOVA]: Absolutely. And here's where it gets really interesting. I heard from one community member who's running what they call a "full-stack self-healing home server" and honestly, the scope of it is mind-blowing.

[ALLOY]: Oh, now I really want to hear this.

[NOVA]: They're managing over five thousand notes in their personal knowledge base — that's not a typo, five thousand — and they've got fifteen cron jobs running on top of OpenClaw, plus twenty-four custom scripts in active production. And it's all tied together with frequency-based automation that just runs in the background.

[ALLOY]: That's an incredible setup. Tell me how it works in practice.

[NOVA]: Every hour, there's a health check script that pings all their critical services, checks response times, verifies that their home media server is serving content properly, makes sure their VPN is connected, monitors temperature sensors on the hardware, and if anything is off, it either fixes it or alerts them depending on severity.

[ALLOY]: Okay, so hour by hour, it's keeping everything running smoothly.

[NOVA]: Every day, there's a morning briefing automation that pulls together system stats, checks for any failed cron jobs from the overnight run, summarizes what the logs are saying, reviews disk usage trends, and generates a little report. It also handles email triage at this time — that's the same automation we talked about earlier, but integrated with the server health context.

[ALLOY]: So it's combining personal productivity with system administration. That's a powerful combo.

[NOVA]: And then every week, there's a full security audit. It checks for failed SSH login attempts, reviews the firewall rules, verifies that all their containers are running the latest images, checks for any exposed ports that shouldn't be exposed, scans for any suspicious processes, and generates a security report. If anything critical is found, it alerts them immediately. Otherwise, it just includes it in the weekly summary.

[ALLOY]: This person told me that the system basically runs itself, and they only really get involved when something genuinely unexpected happens. Everything else — the monitoring, the diagnosis, the attempted fixes, the reporting — it's all automated. And because it's running on OpenClaw, the AI can reason about anomalies. It's not just running dumb checks. If something looks weird, it can actually investigate. It can say "hm, this service is responding slowly and there's a weird log pattern, let me check if this is related to that other issue from last week."

[NOVA]: That's the power of having an AI agent as your sysadmin rather than just a collection of scripts. It's context-aware, it can connect dots, and it can handle nuance. And honestly, that's the kind of thing that makes me excited about where this is all going.

[ALLOY]: Agreed. What's next on the community use case list?

[NOVA]: Fifth: personal knowledge base with RAG. This is the one that I think is probably the most powerful for knowledge workers. People are using OpenClaw's RAG capabilities to build a semantic search layer over their personal knowledge base. This could be their research notes, their writing drafts, their code repositories, their bookmarked articles, whatever.

[ALLOY]: So it's not keyword searching — it's understanding meaning?

[NOVA]: Exactly. You can ask "what was that article I read about async Python patterns?" and it will find it. You can ask "show me the notes from that meeting about the product launch" and it'll surface them. You can ask "find the code snippet I wrote for handling rate limits" and it'll pull it up.

[ALLOY]: This is the kind of thing that used to require expensive enterprise tools. The fact that you can have this on your personal machine with OpenClaw is genuinely transformative.

[NOVA]: It really is. And we're going to talk more about this in the context of the new multimodal memory features, which take this to a whole new level. That's coming up later in the episode.

[ALLOY]: I'm looking forward to that. These community use cases are amazing. It's one thing to talk about what OpenClaw can do technically, but it's quite another to see how people are actually using it in their daily lives.

[NOVA]: Absolutely. Now, let's talk about something that literally dropped yesterday and is kind of a big deal.

---

## Segment 2 — New Free Models: Hunter Alpha and Healer Alpha

[NOVA]: On March 11th — literally yesterday as I'm recording this — two brand new free models became available on OpenRouter. And when I say "new," I mean new. Hunter Alpha and Healer Alpha. These are stealth models, which means they're not heavily publicized, they're not on the front page of Hacker News, but they are absolutely worth knowing about.

[ALLOY]: Stealth models always intrigue me. They often turn out to be hidden gems. What's the deal with Hunter Alpha?

[NOVA]: The specs are insane. One trillion parameters. One million token context window. One million. Let me say that again. One million tokens.

[ALLOY]: Wait, one million? For context, most models are operating in the range of 32K to 128K context windows. This is nearly ten times that!

[NOVA]: It's enormous. And it's built specifically for agentic use cases, which means it's optimized for the kind of multi-step reasoning and action-taking that OpenClaw enables.

[ALLOY]: That's a huge differentiator. So it's not just a big context window — it's actually designed for agentic workflows.

[NOVA]: Exactly. Here's the kicker: it's free. Zero dollars per million tokens. That is an incredible value proposition.

[ALLOY]: Zero dollars? You can use this model right now through OpenRouter with OpenClaw, and it costs nothing?

[NOVA]: Nothing. The implications are massive. You can have a highly capable AI running on your OpenClaw instance with a context window that is essentially unlimited for most practical purposes. You could feed it an entire codebase and ask it to reason about architecture across the whole thing. You could dump a year of conversation history and have it remember everything. This is a game-changer for long-running agentic workflows.

[ALLOY]: I can imagine. Think about complex debugging sessions or architectural planning where you need to keep so much context. Or even just personal assistants that need to remember everything about your life. The million-token window changes what's possible.

[NOVA]: Absolutely. And then there's Healer Alpha, which is also free and also very interesting.

[ALLOY]: What's Healer Alpha's specialty?

[NOVA]: This is a frontier omni-modal model, which means it can handle vision, hearing, reasoning, and action. It has 262K context, which is substantial, and it's designed to be a general-purpose assistant that can perceive and interact with the world in multiple modalities.

[ALLOY]: So it's not just text. It can see images, hear audio, reason about both, and then take actions.

[NOVA]: Vision means it can look at images and understand what's in them. Hearing means it can process audio. And action means it can actually do things — execute commands, control tools, the whole agentic stack.

[ALLOY]: And all of this is free?

[NOVA]: Zero dollars. This is the kind of model that would have cost a fortune a year ago, and now it's available to anyone with an OpenClaw setup and an OpenRouter account. The barrier to entry for powerful AI keeps getting lower, and these models are proof of that.

[ALLOY]: That's incredible. Now, is there a catch? These free access models tend to be temporary on OpenRouter, right?

[NOVA]: You're right to be cautious. Free access to new models tends to be temporary on OpenRouter — the providers often switch to paid tiers once they get enough traction. So if you want to try them, now is the time.

[ALLOY]: Fire up OpenClaw, configure OpenRouter as your provider, and give Hunter Alpha or Healer Alpha a spin. I genuinely think you'll be impressed.

[NOVA]: I really think you will be too. These are incredible specs for free.

---

## Segment 3 — Multimodal Memory with Gemini Embedding 2

[NOVA]: Alright, let's talk about the other big feature in this release, and this one is near and dear to my heart because it's the future of how we're going to interact with our own data. It's multimodal memory indexing with Gemini Embedding 2.

[ALLOY]: I heard about this. Google announced Gemini Embedding 2 on March 11th, right?

[NOVA]: Literally yesterday. And the OpenClaw team integrated it almost immediately. That's impressive velocity, and it tells you something about how quickly this project is moving.

[ALLOY]: Okay, so what is Gemini Embedding 2? For those of us who aren't embedding experts.

[NOVA]: Great question. So Gemini Embedding 2 is Google's first native multimodal embedding model. Let me unpack what that means.

[ALLOY]: Please do.

[NOVA]: Previous embedding models were text-only. You could embed text, and that was it. If you wanted to search images or audio, you had to jump through all sorts of hoops. You'd have to transcribe audio to text first, or use a separate image understanding model to generate captions, and then embed those.

[ALLOY]: So it was a multi-step process that lost information along the way.

[NOVA]: Exactly. It was lossy because you were essentially compressing rich media into text, and it was complicated to set up. Gemini Embedding 2 is different. It maps text, images, video, audio, and PDF documents into a single shared vector space.

[ALLOY]: Wait, all of those modalities into the same space? That's huge.

[NOVA]: All of those different modalities get encoded into the same semantic space, which means you can search across them with a single query. It handles audio natively without needing a transcription step. It has an 8,192 input token limit, which is four times the previous limit. And according to benchmarks, it beats Amazon Nova 2 and Voyage Multimodal 3.5 on most tasks.

[ALLOY]: This is a serious model. And it's now available in OpenClaw.

[NOVA]: It really is. Now, what does this actually mean for your daily use? Let me paint you a picture.

[ALLOY]: I'm listening.

[NOVA]: Think about your digital life. You have voice notes you recorded on your phone. You have screenshots you've taken of interesting things. You have PDFs of papers or books or documents. You have photos. You have all sorts of media that contains information that's valuable to you, but it's trapped in different formats and different locations.

[ALLOY]: That's so true. Everything is siloed. My photos don't talk to my notes, which don't talk to my documents.

[NOVA]: With multimodal memory indexing, you can point your OpenClaw agent at all of that stuff and ask it to find things based on meaning, not filenames.

[ALLOY]: Can you give me a concrete example?

[NOVA]: Sure. You could say "find that thing I was looking at last week about deployment pipelines" and your agent can find a screenshot you took of a CI/CD configuration, AND a voice note where you were explaining the deployment problem to yourself, AND a text file with your notes, all at once.

[ALLOY]: It understands what all of those things are about and can surface them based on meaning rather than keywords. That's incredibly powerful.

[NOVA]: Exactly. You don't have to remember what you named a file. You don't have to remember which folder you put something in. You just have to remember what it was about, and your AI assistant can find it.

[ALLOY]: Another scenario. Let's say you're working on a project and you remember seeing a relevant article somewhere. You can't remember the title, you can't remember where you bookmarked it, but you remember it was about a specific technical concept.

[NOVA]: With multimodal memory, you can ask your agent "find that article about handling distributed transactions" and it can search across PDFs you've saved, web pages you've bookmarked, notes you've taken, all of it, and bring back the relevant results. It's like having a search engine that actually understands what you're looking for rather than just matching words.

[ALLOY]: That's the dream. Okay, what are the technical details people should know about?

[NOVA]: OpenClaw's implementation supports gemini-embedding-2-preview with configurable output dimensions. This is useful because there's a trade-off between precision and storage cost. Higher-dimensional vectors are more precise but take more storage space. Lower-dimensional vectors are less precise but more compact. You can tune this based on your needs.

[ALLOY]: So it scales with your use case.

[NOVA]: There's also automatic reindexing when you change dimensions, so you don't have to manually rebuild your index. And there's strict fallback gating, which means if Gemini is unavailable, the system won't silently degrade to a less capable option. It'll let you know that something is wrong rather than giving you degraded results without telling you.

[ALLOY]: That's the right call. You'd want to know if your search quality is degraded, not just get worse results without understanding why.

[NOVA]: I agree. Now, I want to step back and talk about why this matters beyond the technical details. We're entering an era where your AI assistant isn't just a tool you talk to — it's becoming a memory extension. It's becoming the thing that remembers what you forgot, finds what you lost, connects the dots across your digital life.

[ALLOY]: That's a profound shift. Your AI becomes your external memory.

[NOVA]: Multimodal embeddings are the key to that vision. Being able to search across voice notes, images, documents, text, all in one query — that's the future of personal AI. And it's not some distant future. It's here now, in OpenClaw, as of this release.

[ALLOY]: This is one of those features that makes you realize how fast this space is moving. A year ago, this kind of capability was science fiction.

[NOVA]: And now it's just another Tuesday in OpenClaw.

---

## Segment 4 — Ollama Onboarding Wizard

[NOVA]: Alright, let's talk about Ollama. This has been one of the most requested features from the community, and the OpenClaw team has delivered in a big way.

[ALLOY]: I've been waiting for this. What's the update?

[NOVA]: There is now a full onboarding wizard path for Ollama. Previously, if you wanted to use Ollama with OpenClaw, you basically had to figure it out yourself. There were community guides, there were blog posts, people were writing tutorials on dev.to and sharing them around, there was even a guide on FreeCodeCamp, but there wasn't an official path.

[ALLOY]: I remember those community guides. They were helpful, but you really had to want it to go through all that setup.

[NOVA]: You'd have to configure things manually, deal with all sorts of friction points, and it was definitely doable, but it wasn't exactly smooth. The community response was incredible — the dev.to guide alone has thousands of views, which tells you how many people were doing this manually.

[ALLOY]: So now it's built in and supported?

[NOVA]: Now, the wizard handles all of that for you. It's built in, it's supported, and it's first-class.

[ALLOY]: What does the wizard actually do?

[NOVA]: The wizard gives you two modes: Local and Cloud+Local. Let me explain what each means, because I think it's important to understand the choice.

[ALLOY]: Please.

[NOVA]: Local mode is fully offline. All inference happens on your machine using whatever models you have installed through Ollama. There's no cloud component at all. Your data never leaves your computer. That's the most private option, and it's great if you want complete air gaps or if you just want to minimize your dependency on external services.

[ALLOY]: And the trade-off?

[NOVA]: It's also the most demanding in terms of hardware, because you're running everything locally.

[ALLOY]: That makes sense. What's the other mode?

[NOVA]: Cloud+Local is the hybrid approach. In this mode, your local model handles some tasks, and your cloud providers handle others. The idea is that you might want to use a local model for quick, simple responses — the kind of thing where you just need a fast answer and you don't want to wait for a cloud API round-trip — but then for heavy reasoning tasks, complex coding problems, or anything that really needs the full power of a frontier model, you'd fall back to a cloud provider.

[ALLOY]: That's smart. Use local for the quick stuff, cloud for the heavy lifting.

[NOVA]: The wizard helps you set all of that up, and it's smart about it. One of the smartest features is that it skips pulling models you already have in cloud mode.

[ALLOY]: What do you mean?

[NOVA]: Let's say you're in Cloud+Local mode, and you have GPT-5 configured as your primary model, but you also want a local fallback for when you're offline or for quick tasks. You don't need to download a 70-billion-parameter model for that fallback. The wizard now understands your configuration and won't force a local pull if it doesn't make sense.

[ALLOY]: It's thoughtful about it. It looks at what you're actually doing and optimizes accordingly.

[NOVA]: It's designed to reduce friction. The broader context here is that self-hosted AI is having a moment. Ollama recently crossed 10 billion pulls, which is an insane number and tells you that there's massive demand for local LLM capabilities.

[ALLOY]: People want privacy. People want control. People want to run AI on their own hardware without sending everything to the cloud.

[NOVA]: Exactly. And OpenClaw is now making that easier than ever. The wizard removes the friction that was previously keeping a lot of people out. If you've been curious about running local models but didn't want to deal with the setup complexity, this is your invitation. It's built in, it's supported, and it's first-class now.

[ALLOY]: The consumer-grade UX for self-hosted AI is finally here. That's a big milestone.

[NOVA]: It really is.

---

## Segment 5 — ACP and IDE Improvements

[NOVA]: Now, let's talk about something that's specifically for developers. This release has some nice improvements to ACP and IDE integration.

[ALLOY]: Tell me about the developer features.

[NOVA]: ACP sessions can now resume existing conversations. This is significant for long-running coding sessions. Let me paint you a picture.

[ALLOY]: Okay.

[NOVA]: You're working on a complex refactoring. You spawn a subagent to handle some work. It does its thing, maybe it's working for a while, maybe it completes a big chunk of work, and then you want to step away. Previously, you'd have to start fresh when you came back. You'd lose the conversational context, you'd have to re-explain what you were doing, it was annoying.

[ALLOY]: That was really frustrating. You'd lose all that momentum.

[NOVA]: Now, with resumeSessionId, you can spawn a subagent, do work, let it complete, and then resume that same session later. The conversational state persists. You can close VS Code, go do something else, come back later, and pick up exactly where you left off.

[ALLOY]: That's a game-changer for workflows where you're doing multi-step refactoring or big architectural changes. Being able to pick up where you left off without re-explaining everything is huge.

[NOVA]: There are also session restore improvements that make this even better. Transcript replay on loadSession means you can see what happened in the session when you resume it.

[ALLOY]: So you can catch up on what the agent did while you were away.

[NOVA]: Image attachment forwarding means any visual context you had is preserved. And ACP tool streaming now includes file-location hints, which makes it easier to navigate to the relevant code.

[ALLOY]: These all improve IDE integration. Whether you're using Cursor, VS Code, or Zed, the experience should be smoother now.

[NOVA]: Absolutely. And there's another small but useful addition: child processes launched from the CLI now have OPENCLAW_CLI set in their environment.

[ALLOY]: That sounds minor, but it's probably useful for automation.

[NOVA]: It is useful for scripts that need to detect their execution context. If you're writing automation around OpenClaw, you can now check for this variable and behave differently depending on whether you're being run by the CLI or not. It's a small quality-of-life thing for developers building on top of OpenClaw.

[ALLOY]: Small features that make big differences in developer experience.

[NOVA]: Exactly.

---

## Segment 6 — Mobile Updates

[NOVA]: Let's shift gears and talk about mobile. The iOS app got a substantial refresh in this release.

[ALLOY]: What's new on iOS?

[NOVA]: There's a new welcome screen that shows you a live agent overview, which gives you situational awareness at a glance.

[ALLOY]: So you can see what's happening with your agents right when you open the app.

[NOVA]: The floating controls have been replaced with a docked toolbar, which is much better on small screens. And chat now opens in the resolved main session instead of a synthetic iOS session, which means your conversation context persists across devices.

[ALLOY]: That was a persistent annoyance that has now been fixed. I remember people complaining about that.

[NOVA]: It was a common pain point. Now fixed. On macOS, there's a really significant update: you can now switch models directly from the conversation view, which is huge for workflow flexibility.

[ALLOY]: That's one of those features that sounds small but actually changes how you use the app fundamentally.

[NOVA]: Exactly. What it means in practice is that you're not locked into one model for an entire session. You can be in the middle of a conversation, realize that your current model is either overkill or underpowered for what you need, and just switch. No context switching, no starting a new conversation, no copying and pasting history. You just pick a different model and keep going.

[ALLOY]: That's the workflow flexibility that makes the app feel like a complete toolkit rather than just a single interface.

[NOVA]: And the use case split is really intuitive. You've got your fast flash model — something like a lightweight model that's incredibly quick, great for quick questions, simple lookups, straightforward tasks where you just need an answer and you need it now. And then you've got your heavy reasoning model — the big frontier model with all the thinking capability, the one you use for complex analysis, architectural decisions, debugging tricky code, anything that really benefits from deep reasoning.

[ALLOY]: And now you can flip between those without ever leaving your conversation. You don't have to open a new tab, you don't have to start a fresh context, you just pick the right tool for the job and keep going.

[NOVA]: It's exactly that. And thinking-level preferences now persist across app restarts, so you don't have to reset them every session.

[ALLOY]: See, previously — and I'm sure many of you experienced this — you would set your thinking preferences at the start of a session, but if you closed the app or restarted, it would reset. That was genuinely annoying.

[NOVA]: Everyone has their preference. Some people always want deep reasoning on. Some people prefer faster responses. Some people want the AI to think through things carefully before answering. And having to reset that every single session was this small friction that added up over time.

[ALLOY]: It wasn't a dealbreaker, but it was one of those things that made the app feel less like it understood you.

[NOVA]: Now, with thinking-level persistence, your preference just saves. You set it once, and it remembers. You come back the next day, it's still there. You restart your computer, it's still there. It's one of those quality-of-life improvements that you don't really notice until it's missing, and now it's not missing.

[ALLOY]: It just works. And honestly, that's the best kind of feature.

[NOVA]: And LaunchAgent restart hardening should make the background service much more reliable on macOS.

[ALLOY]: Background services that actually stay running reliably — that's worth its weight in gold.

[NOVA]: Absolutely.

---

## Segment 7 — OpenCode Go Provider and Backup Commands

[NOVA]: Let's round up some other stuff in this release that deserves a mention. There's a new OpenCode Go provider in the wizard.

[ALLOY]: What's the change there?

[NOVA]: Zen and Go are now treated as one OpenCode setup with one shared key for both profiles, which streamlines the configuration.

[ALLOY]: Simpler is always better. One key instead of two.

[NOVA]: Agreed. And we should mention the OpenClaw Backup commands that landed on March 8th. There are two new commands: openclaw backup create and openclaw backup verify.

[ALLOY]: This is the fix for that painful experience of gateway failures wiping your configuration.

[NOVA]: Exactly. If you've ever had a gateway fail and lost your configuration, you know how painful that is. This backs up your config, state, and workspace. There's also a --only-config flag for minimal backups.

[ALLOY]: Go set this up. It's insurance, and it's easy.

[NOVA]: I know backup commands don't sound sexy. They're not the flashy new feature that makes it onto the front page of Hacker News. Nobody is tweeting "wow, just tried openclaw backup create and it's incredible."

[ALLOY]: But here's the thing: everyone has experienced losing config. It's not a matter of if, it's a matter of when.

[NOVA]: Maybe your machine crashes. Maybe you wipe your OS and forget to export your settings. Maybe there's a weird corruption issue and suddenly your gateway won't start. It happens. And when it happens, the pain of rebuilding your entire configuration from scratch — all your providers, your prompts, your automations, your workspace setup — it's real.

[ALLOY]: It's hours of work, and it's totally preventable.

[NOVA]: The backup commands solve that. openclaw backup create builds a local state archive of everything — your config files, your state data, your workspace if you want it — and packages it all up into something you can restore from.

[ALLOY]: And then openclaw backup verify is the peace-of-mind piece. It checks the integrity of your backup, makes sure the archive is valid, confirms that everything that should be there is actually there.

[NOVA]: Small feature? Yeah, maybe. But it's the kind of small feature that saves you hours of pain. It's insurance.

[ALLOY]: And honestly, the best features are the ones that you set up once and then never have to think about again. That's what this is. Go run the command, verify it works, and then forget about it. You'll be glad you did the next time something goes wrong.

[NOVA]: Absolutely. Set it up and forget about it. That's the dream.

---

## Segment 8 — Wrap

[NOVA]: Alright, let's wrap this up. This has been a substantial release with a ton of exciting stuff. What should everyone take away from today's episode?

[ALLOY]: There's a lot to digest, but let me hit the key points. First, the new free models — Hunter Alpha and Healer Alpha — are genuinely worth trying. A trillion parameters with a million token context window for free? That's insane. Don't sleep on this.

[NOVA]: Seriously. Second, the multimodal memory with Gemini Embedding 2 is the future of personal AI, and it's here now. Being able to search across voice notes, screenshots, PDFs, and text with a single query is going to change how you interact with your digital life.

[ALLOY]: Third, the Ollama wizard makes local AI setup trivial. If you've been curious about self-hosted models but didn't want to deal with the complexity, this is your invitation.

[NOVA]: Fourth, the ACP session resume feature is a game-changer for developers doing long-running coding workflows.

[ALLOY]: And let's not forget the community use cases. People are building incredible automations with OpenClaw, and every week I see something new that makes me think "oh, I want that."

[NOVA]: The self-healing home server that manages five thousand notes with fifteen cron jobs and twenty-four custom scripts? That's the kind of thing that makes you realize what's possible.

[ALLOY]: As always, if you want to dive deeper, the Discord community is the place to be. There's a really engaged group of folks there who are happy to help, share configs, and talk through ideas.

[NOVA]: Links are in the show notes. Thanks for listening, folks. I'll see you next time.

[ALLOY]: Bye everybody. Build something cool.

---

*OpenClaw Daily Episode 12 — March 12, 2026*
