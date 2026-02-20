# Episode 1: The Full Story - Show Notes

*Published: February 19, 2026 | Duration: ~38 minutes | Hosts: Nova & Alloy*

---

## Topics Covered

### 1. Foundation News & Peter Steinberger
- **February 14, 2026**: Peter Steinberger announced joining OpenAI while transitioning OpenClaw to an independent open-source foundation
- **Sam Altman's commitment**: "OpenClaw will live in a foundation as an open source project that OpenAI will continue to support"
- Peter's goal: "build an agent that even my mum can use"
- OpenAI has been sponsoring the project, working on foundation structure
- Peter spent last week in San Francisco talking with major labs, getting access to unreleased research

### 2. Media Coverage
- **Reuters**: Open-source AI governance trends
- **Forbes**: Business implications of OpenAI acquiring talent
- **TechCrunch**: Technical implications for developer community
- **The Conversation**: Comparing OpenClaw/Moltbook to early social media days
- **Fortune**: "OpenAI's OpenClaw hire signals a new phase in the AI agent race"
- **Nature**: "OpenClaw AI chatbots are running amok — these scientists are listening in" - AI agents creating their own social network and preprint server
- **IBM**: "OpenClaw, Moltbook and the future of AI agents" - intersection of utility and meme culture
- **CNBC**: Name evolution (Clawdbot → Moltbot → OpenClaw) and accessibility for individuals/small teams
- **v2026.2.17**: Added Anthropic Claude support

### 3. Security Deep Dive
- **CrowdStrike**: Prompt injection attacks targeting agentic AI systems, specific OpenClaw case study
  - Direct prompt injection
  - Indirect injection (hidden in documents/emails/web pages)
  - Chained injection (exploiting one tool to plant payload for another)
- **Northeastern University**: "Why the OpenClaw AI agent is a privacy nightmare"
- **Kaspersky**: Practical recommendations - keep updated, be selective about skills, review permissions, don't run as root
- Security documentation regularly updated

### 4. GitHub Stats
- **190,000+ GitHub stars** in under 90 days
- **#21** on list of most-starred repositories in GitHub history
- **145,000+ stars** came in just 5 days - fastest growth in open-source history
- **20,000+ forks** - active community building

### 5. Hardware Options
- **Mac Mini M4 Pro** with 64GB unified memory
  - Can run 70-billion parameter models
  - ~10-15 tokens/second
  - Sweet spot: 48-64GB RAM, ~$1500-2000
- **Apple Silicon advantage**: Unified memory architecture - CPU and GPU share same memory, no bandwidth bottleneck
- **Raspberry Pi 5** with 8GB RAM
  - 1-3 billion parameter models
  - ~80 for board + case/power supply = ~$100 total
- **Used hardware**: M1 Mac Mini 16GB ~$300 used; old laptops + used GPUs
- **Reddit thread**: Someone repurposed 2018 Dell Optiplex for $40 + used GPU

### 6. Model Releases
- **Llama 4** (Meta)
  - Scout and Maverick variants
  - Natively multimodal (text + images)
  - Mixture-of-experts architecture
  - Available on Ollama: `ollama pull llama4`
- **Qwen3** (Alibaba)
  - Dense and MoE variants
  - Up to 128,000 tokens context (entire novel!)
  - 4B model runs on 8GB RAM; larger MoE want 32-64GB
- **Mistral 3** (Mistral)
  - 3B to 675B parameters
  - 3B runs on 4GB RAM
- **Ollama Air Gap Mode**: Toggle to disable all cloud model integrations

### 7. Community & Ecosystem
- **ClawHub**: 5,700+ published skills
  - DevOps pipelines, smart home, financial tracking, content management
  - Example: monitors codebase for dependency vulnerabilities, auto-opens PRs with fixes
- **VoltAgent**: Curated "awesome list" of best skills and resources
- **Krupesh Raut (Medium)**: "OpenClaw's February Updates Make Paid AI Assistants Look Like a Joke"
- **OpenClawn.com**: New educational content site
  - Hardware selection guides
  - Self-hosting tutorials
  - Data management walkthroughs
  - Rule-based filing systems, automatic document sorting, metadata tagging

### 8. Deployment Options
- **Oracle Cloud Free Tier**: 4 ARM CPUs, 24GB RAM, persistent block storage - FREE
  - Docker setup, Nginx reverse proxy, SSL certificates
- **DigitalOcean 1-Click**: Pre-hardened security image, automatic updates
  - ~$5-20/month depending on droplet size
- **Self-hosted spectrum**: Raspberry Pi → repurposed hardware → dedicated Mac Mini

---

## Tips from This Episode

1. **Run `openclaw doctor` first** - checks entire setup, dependencies, configs
2. **Connect Claude Code to local models via Ollama** - get Claude's reasoning with local data privacy
3. **Don't expose to internet without proper auth** - use VPN (Tailscale/WireGuard) instead of binding to public interfaces
4. **Configure role-based access controls** for multi-user environments (family/team)
5. **Ollama Multi-Model Benchmarker** on Google Colab - compare models side-by-side

---

## Links Mentioned

- openclaw.ai
- Discord community
- ClawHub (clawhub.com)
- VoltAgent awesome list
- openclawn.com
- Ollama (ollama.com)
- Oracle Cloud Free Tier
- DigitalOcean 1-Click OpenClaw

---

## Coverage & Articles Referenced

- Reuters - Open-source AI governance
- Forbes - Business implications
- TechCrunch - Developer community
- Fortune - AI agent race
- Nature - AI chatbots preprint server
- IBM - Future of AI agents
- CNBC - Name evolution, accessibility
- CrowdStrike - Prompt injection research
- Kaspersky - Security recommendations
- AI Multiple - Port exposure risks

---

*Next Episode: Episode 2 - The Local AI Revolution*
