# Show Notes - Episode 8: The ClawJacked Vulnerability & v2.26 Security Overhaul

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
