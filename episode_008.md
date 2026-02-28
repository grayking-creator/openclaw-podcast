# OpenClaw Daily Podcast - Episode 8: The ClawJacked Vulnerability & v2.26 Security Overhaul
# Date: February 28, 2026
# Hosts: Nova (warm British) & Alloy (American)

---

[NOVA]: Welcome back to OpenClaw Daily. I'm Nova, as always, here with my partner Alloy. And wow, Alloy, we have a pretty significant episode today. There's been a major security disclosure, a new version release, and some interesting industry movement. How are you doing?

[ALLOY]: Hey Nova! I'm doing great, and you're right - this is a big one. We always say that, but this time there's genuinely some important developments that our listeners need to understand. Let's dive in.

[NOVA]: Absolutely. Let's start with what I think is the most important story - and that's the ClawJacked vulnerability, also known as CVE-2026-25253. This was disclosed on February 27th, which is literally yesterday. And Alloy, this is a scary one.

[ALLOY]: It really is, Nova. So the folks at Oasis Security discovered that malicious websites could actually hijack your OpenClaw agent. Here's how it works - if you have OpenClaw running locally and you visit a website with malicious JavaScript, that script can brute-force your gateway password, register itself as a trusted device, and then take complete control of your AI agent. The problem stems from two issues - there's no rate limiting on authentication attempts from localhost, and OpenClaw implicitly trusts connections coming from localhost.

[NOVA]: That's terrifying. And the timing is particularly concerning because we've been talking about how OpenClaw is becoming more popular, more people are deploying it, and now we find out that simply visiting the wrong website could give someone complete control over your AI agent? That's a huge blast radius.

[ALLOY]: Absolutely. And the OpenClaw team actually responded really well to this. They patched it within 24 hours of the report. If you're running OpenClaw, you need to update to version 2026.2.25 or later immediately. That's the most important thing you can do right now.

[NOVA]: Now, shifting gears, there was also a major release - OpenClaw version 2.26 dropped on February 27th as well. And this is described as a stability and reliability overhaul. Tell us about this one, Alloy.

[ALLOY]: So v2.26 is all about fixing core mechanics for production environments. They've made improvements to cron job reliability, which has been a pain point for a lot of users. There's also some security enhancements, better secrets management, and improvements to agent lifecycle and multi-channel behavior. But the really interesting thing is the new external secrets workflow. This is designed to eliminate the risk of API keys being stored in plain text configuration files. That's been a concern for a while, so it's good to see them addressing it.

[NOVA]: And that brings the total security hardening fixes in this release to 11. That's significant. It shows that the team is taking security seriously after all the attention this project has been getting.

[ALLOY]: Now, here's something interesting - on February 28th, which is literally today, Clawbot AI announced a cloud-hosted SaaS version of OpenClaw. This is the first major SaaS offering built on top of OpenClaw. And they're positioning it as a way to simplify deployment and management without needing to run things locally. It also has built-in AI model selection that automatically matches appropriate models to different tasks.

[NOVA]: That's a big move. For people who don't want to deal with infrastructure, this could be a game-changer. But it also raises interesting questions about the whole self-hosted versus SaaS debate. We've talked about this before - when you run locally, you have control, but you also have responsibility for security. When you go SaaS, you're trusting someone else.

[ALLOY]: That's a great point, Nova. And you know what's interesting - this is launching the same week as this major vulnerability disclosure. It really highlights the tension in the OpenClaw ecosystem right now. On one hand, you have people pushing for more accessible, easier-to-use cloud solutions. On the other hand, you have these serious security concerns that make the case for staying local.

[NOVA]: Absolutely. And I think the broader conversation here is about the maturation of the AI agent space. We've seen this pattern before with other technologies - they start out as niche, hobbyist tools, and then as they grow in popularity, they become targets. OpenClaw has gone from zero to over 140,000 GitHub stars in just a few months. That's incredible growth, but it also makes it a bigger target for attackers.

[ALLOY]: And that's exactly what the security researchers have been saying. There's this ongoing concern about OpenClaw's architecture - the fact that it runs locally with access to sensitive information, and it's exposed to untrusted input through messaging channels. We mentioned earlier that the Atomic macOS Stealer was being distributed through malicious skills - that's a supply chain attack where AI agents are manipulated to trick human users. This is an evolving threat landscape.

[NOVA]: It really is. And I think what's important for our listeners to understand is that this is not a reason to abandon OpenClaw - it's a reason to be vigilant. Update your software, be careful about what skills you install, and understand the risks if you're running this on a machine that has access to sensitive information.

[ALLOY]: Exactly. And on a more positive note, there's been some interesting community discussion about the future of OpenClaw under OpenAI's wing. People are thinking about how to balance the benefits of local execution with the need for robust security. There are questions about whether OpenAI's involvement will lead to more built-in security features or if it'll push more people toward cloud solutions.

[NOVA]: That's a great question. And I think we'll have to wait and see how that plays out. But for now, the immediate takeaway is simple - update your OpenClaw installation to the latest version. If you're running 2.25 or later, you're protected from the ClawJacked vulnerability. If you're on an older version, you need to upgrade right now.

[ALLOY]: Absolutely. And if you're considering whether to go with a self-hosted setup or try the new SaaS offering, think about your threat model. If you're comfortable managing your own security and you need full control, stick with self-hosted. If you want simplicity and you're willing to trust a third party, the SaaS version might be worth exploring.

[NOVA]: Well, that's our episode for today, everyone. Thanks for joining us. We'll see you next time on OpenClaw Daily.

[ALLOY]: Until next time. Stay secure, and keep building.

---

# Show Notes - Episode 8

## Episode Details
- **Episode:** 8
- **Date:** February 28, 2026
- **Hosts:** Nova (warm British) & Alloy (American)
- **Duration Target:** 30-40 minutes

## Topics Covered

### 1. ClawJacked Vulnerability (CVE-2026-25253)
- **Disclosed:** February 27, 2026
- **Severity:** High
- **Discovery:** Oasis Security
- **Issue:** Malicious websites can brute-force gateway password, register as trusted device, hijack AI agent
- **Root causes:** No rate limiting on localhost auth, implicit trust in localhost connections
- **Fix:** Update to OpenClaw v2026.2.25 or later
- **Patched:** Within 24 hours of report
- **Sources:**
  - https://www.scworld.com/news/how-openclaw-could-be-hijacked-with-a-simple-website-visit
  - https://www.csoonline.com/article/4138431/your-personal-openclaw-agent-may-also-be-taking-orders-from-malicious-websites.html

### 2. OpenClaw v2.26 Release
- **Released:** February 27, 2026
- **Focus:** Stability and reliability overhaul
- **Key improvements:**
  - Cron job reliability fixes
  - 11 security hardening fixes
  - External secrets workflow (eliminates plain-text API keys)
  - Agent lifecycle improvements
  - Multi-channel behavior enhancements
- **Sources:**
  - https://ucstrategies.com/news/openclaw-2-26-update-major-stability-security-and-automation-fixes-explained/

### 3. Clawbot AI SaaS Launch
- **Announced:** February 28, 2026
- **Description:** Cloud-hosted OpenClaw version
- **Features:**
  - No local installation required
  - Built-in AI model selection
  - Automatic model-task matching
- **Significance:** First major SaaS offering built on OpenClaw
- **Sources:**
  - https://markets.financialcontent.com/wral/article/247pressrelease-2026-2-28-clawbot-ai-launches-online-saas-version-of-openclaw-with-built-in-ai-model-selection-for-cloud-based-agent-deployment

### 4. Ongoing Security Concerns
- Supply chain attacks via malicious skills (Atomic macOS Stealer)
- Community discussion on local execution vs cloud security
- OpenAI involvement raising questions about future security direction
- **Sources:**
  - https://www.trendmicro.com/en_us/research/26/b/openclaw-skills-used-to-distribute-atomic-macos-stealer.html
  - https://community.openai.com/t/the-future-of-openai-openclaw-anticipating-secure-local-execution/1375105

## Key Takeaways
1. **Update immediately** to v2026.2.25+ to patch ClawJacked vulnerability
2. **Be careful** about visiting untrusted websites while OpenClaw is running
3. **Audit your skills** - only install from trusted sources
4. Consider **self-hosted vs SaaS** based on your threat model
5. **Stay vigilant** - this is a growing target for attackers

## Links Mentioned
- https://www.scworld.com/news/how-openclaw-could-be-hijacked-with-a-simple-website-visit
- https://www.csoonline.com/article/4138431/your-personal-openclaw-agent-may-also-be-taking-orders-from-malicious-websites.html
- https://ucstrategies.com/news/openclaw-2-26-update-major-stability-security-and-automation-fixes-explained/
- https://markets.financialcontent.com/wral/article/247pressrelease-2026-2-28-clawbot-ai-launches-online-saas-version-of-openclaw-with-built-in-ai-model-selection-for-cloud-based-agent-deployment
- https://www.trendmicro.com/en_us/research/26/b/openclaw-skills-used-to-distribute-atomic-macos-stealer.html
- https://community.openai.com/t/the-future-of-openai-openclaw-anticipating-secure-local-execution/1375105

---
*Episode 8 | Recorded: February 28, 2026*
