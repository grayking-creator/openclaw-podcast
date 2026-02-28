# OpenClaw Daily Podcast - Episode 8: Local Models Explosion & The New Ollama Ecosystem
# Date: February 28, 2026
# Hosts: Nova (warm British) & Alloy (American)

---

[NOVA]: Welcome back to OpenClaw Daily. I'm Nova, here with Alloy. And wow, Alloy, the local AI model space is absolutely exploding right now. There's so much happening that I barely know where to start.

[ALLOY]: I know, Nova. And that's exactly why I think this episode is going to be really exciting for our listeners. We're going to talk about what's new in local models, some incredible use cases that people are building, and then we'll touch on one important security update at the end. But mostly, this is about the fun stuff - what you can actually do.

[NOVA]: Absolutely. Let's start with the big news - and that's the Ollama ecosystem updates. For those who don't know, Ollama is the tool that lets you run these powerful models locally on your own machine. And they've been rolling out some major updates. Version 0.17.0 and 0.17.4 dropped recently, and these bring improved OpenClaw onboarding and better support for all kinds of models. If you haven't tried Ollama yet, now is a great time to jump in.

[ALLOY]: And the model library is just incredible right now. I mean, we're seeing new families like Qwen 3.5 and this really interesting new model called LFM 2. LFM 2-24B-A2B is the largest efficient model in its family, and it dropped with Ollama 0.17.4. That's huge for people who want serious capability without needing a supercomputer.

[NOVA]: And let's talk about the small models that pack a punch. Gemma 3 12B and Phi-4 are being recommended for general tasks. These are models that can run on reasonably modest hardware but still give you really solid results. For people just getting started with local AI, these are perfect entry points.

[ALLOY]: Now for the medium-sized models - this is where things get interesting. Qwen3 30B A3B, EXAONE 4.0 32B, and DeepSeek R1 Distill Llama 70B are all standout choices. These give you that extra capability for more complex tasks without requiring an absolute beast of a machine.

[NOVA]: And if you really want to go big, there are options like Qwen3-235B and DeepSeek V3.2. These are the heavy hitters. But here's what I find really exciting - we're also seeing models like GLM-5 leading in reasoning with a Quality Index of 49.64, and MiniMax-M2.5 is also in the conversation. And OpenAI even has open-weight alternatives now with GPT-OSS in 20B and 120B sizes.

[ALLOY]: It's an incredible time to be experimenting with local AI. Now let's shift to something that I think is genuinely inspiring - the practical use cases that people are building with OpenClaw. These are real things that are happening right now, and they show just how powerful this technology has become.

[NOVA]: One of the most popular use cases is full business automation. People are using OpenClaw to handle their entire business operations - client email responses, social media scheduling, campaign tracking, generating daily briefings with prioritized action items. Imagine your business running autonomously while you sleep. That's not science fiction anymore - that's happening right now.

[ALLOY]: And it's not just businesses. Content creators are using OpenClaw for automated video production. The agent analyzes successful video content, identifies patterns, and then autonomously replicates them. We're talking about the entire pipeline from idea generation to storyboarding. That's a whole creative workflow being automated.

[NOVA]: Here's one that really blew my mind - agent swarms for market research. People are orchestrating multiple OpenClaw instances that literally scrape the internet overnight. They gather competitive intelligence, track pricing, monitor social media sentiment on Reddit and X, analyze GitHub activity for technical direction, and then compile comprehensive reports by morning. That's a whole research department working while you sleep.

[ALLOY]: Then there's the cryptocurrency traders who have OpenClaw running 24/7 for arbitrage trading. The agent identifies and executes opportunities around the clock, and they get real-time updates via Telegram. It's completely autonomous trading.

[NOVA]: And my absolute favorite - people are telling their OpenClaw agent to "build a game" and then coming back to find a functional application that has already attracted thousands of users. That's the power of AI agents building on AI agents.

[ALLOY]: There was also this great story about someone setting up what they call an "8-AI expert business advisory board." They've got eight different AI experts analyzing business data from YouTube analytics, Instagram engagement, email campaigns, and then these experts engage in parallel discussions to synthesize findings and provide prioritized recommendations. It's like having a board of directors that never sleeps and doesn't charge a retainer.

[NOVA]: Now, let's talk about one more practical thing before we get to the security update. And that's the new Clawbot AI SaaS version that launched today - February 28th. This is a cloud-hosted version of OpenClaw that removes the need for local installation. For people who don't want to mess with infrastructure but still want to use OpenClaw, this is a game-changer. It also has built-in AI model selection that automatically matches appropriate models to different tasks.

[ALLOY]: That's a really important development because it lowers the barrier to entry. Not everyone wants to set up Ollama and download models and manage their own hardware. Some people just want to click a button and have it work. This SaaS version gives them that option.

[NOVA]: Now, let's get to the security update - and we'll keep this brief because we know not everyone wants to dwell on this stuff. There was a vulnerability called ClawJacked, also known as CVE-2026-25253, disclosed on February 27th. The issue was that malicious websites could potentially hijack your OpenClaw agent through your browser. The OpenClaw team patched it within 24 hours, so if you're running version 2026.2.25 or later, you're protected. Just make sure you update.

[ALLOY]: And honestly, that's the state of things right now. The ecosystem is growing incredibly fast, the models are getting more capable, and people are building amazing things. Yes, there are security considerations - there always are with powerful tools - but the opportunities far outweigh the risks if you're thoughtful about how you use them.

[NOVA]: Absolutely. That's our episode for today, everyone. Thanks for joining us. We'll see you next time on OpenClaw Daily.

[ALLOY]: Until next time. Keep building, and have fun with it.

---

# Show Notes - Episode 8

## Episode Details
- **Episode:** 8
- **Date:** February 28, 2026
- **Hosts:** Nova (warm British) & Alloy (American)
- **Duration Target:** 30-40 minutes

## Topics Covered

### 1. Ollama Ecosystem Updates
- Ollama v0.17.0 and v0.17.4 released
- Improved OpenClaw onboarding
- Enhanced support for various models
- **Sources:** https://github.com/ollama/ollama/releases, https://phoronix.com/news/ollama-0.17

### 2. New Local Model Releases
- **LFM 2-24B-A2B:** Largest efficient model, released with Ollama 0.17.4
- **Qwen 3.5:** New multimodal open-source family
- **Gemma 3 12B & Phi-4:** Recommended for small general tasks
- **Qwen3 30B A3B, EXAONE 4.0 32B, DeepSeek R1 Distill Llama 70B:** Medium-sized standout choices
- **Qwen3-235B & DeepSeek V3.2:** Large heavy hitters
- **GLM-5:** Leading in reasoning (Quality Index 49.64)
- **MiniMax-M2.5:** Strong performer
- **GPT-OSS 20B & 120B:** OpenAI open-weight alternatives
- **Sources:** https://whatllm.org/blog/best-open-source-models-february-2026, https://www.sitepoint.com/definitive-guide-local-llms-2026-privacy-tools-hardware/

### 3. Practical Use Cases People Are Building
- **Full Business Autopilot:** Email, social media, campaign tracking, daily briefings
- **Automated Video Production:** Analyze content, identify patterns, replicate success
- **Agent Swarms:** Overnight market research, competitive intelligence
- **24/7 Crypto Arbitrage Trading:** Autonomous trading with Telegram updates
- **Autonomous App Development:** "Build a game" → functional app with thousands of users
- **AI Business Advisory Board:** 8 experts analyzing multi-source data in parallel
- **Sources:** https://medium.com/@alexrozdolskiy/10-wild-things-people-actually-built-with-openclaw-e18f487cb3e0

### 4. Clawbot AI SaaS Launch
- **Announced:** February 28, 2026
- Cloud-hosted OpenClaw
- No local installation required
- Built-in AI model selection
- **Sources:** https://markets.financialcontent.com/wral/article/247pressrelease-2026-2-28-clawbot-ai-launches-online-saas-version-of-openclaw-with-built-in-ai-model-selection-for-cloud-based-agent-deployment

### 5. Security Update (Brief)
- **ClawJacked (CVE-2026-25253):** Disclosed Feb 27, patched within 24 hours
- **Fix:** Update to v2026.2.25 or later
- **Sources:** https://www.scworld.com/news/how-openclaw-could-be-hijacked-with-a-simple-website-visit

## Key Takeaways
1. **Local models are exploding** - Qwen3, LFM 2, Gemma 3, Phi-4 all great options
2. **Ollama makes it easy** - v0.17 updates improved everything
3. **Practical automation is here** - businesses running autonomously overnight
4. **SaaS option available** - for those who don't want to self-host
5. **Update your OpenClaw** - patch ClawJacked vulnerability

## Links Mentioned
- https://github.com/ollama/ollama/releases
- https://phoronix.com/news/ollama-0.17
- https://whatllm.org/blog/best-open-source-models-february-2026
- https://www.sitepoint.com/definitive-guide-local-llms-2026-privacy-tools-hardware/
- https://medium.com/@alexrozdolskiy/10-wild-things-people-actually-built-with-openclaw-e18f487cb3e0
- https://markets.financialcontent.com/wral/article/247pressrelease-2026-2-28-clawbot-ai-launches-online-saas-version-of-openclaw-with-built-in-ai-model-selection-for-cloud-based-agent-deployment
- https://www.scworld.com/news/how-openclaw-could-be-hijacked-with-a-simple-website-visit

---
*Episode 8 | Recorded: February 28, 2026*
