# EP030 — Memory First, Machines Next
**OpenClaw Daily** | April 13, 2026 | ~31–34 min

## Episode Title
**Memory First, Machines Next**

## Tagline
OpenClaw ships a release that pulls the right context forward before you answer, OpenAI scrambles after a supply-chain scare, Anthropic turns Cowork into an enterprise control surface, SoftBank makes a national bet on physical AI, and Meta's new health chatbot reminds everyone that consumer AI still wants too much data and deserves too little trust.

## Feed Description
OpenClaw's latest release makes memory retrieval happen before the main reply and pushes more speech and model routing local. Then we dig into OpenAI's macOS certificate rotation, Anthropic turning Cowork into an admin surface, SoftBank's physical-AI bet, and Meta's overreaching health chatbot.

## Story Slate

### 1. **OpenClaw v2026.4.12 — Active Memory, Local Speech, and Plugin Hardening**
OpenClaw's newest stable release is a quality-and-foundation update, but it matters because it changes what the product remembers and how safely it loads capability. The big additions are an optional Active Memory plugin that runs a dedicated memory sub-agent before the main reply, an experimental local MLX speech provider for Talk Mode on macOS, bundled Codex and LM Studio providers, and tighter manifest-based plugin activation so the runtime stops loading unrelated code it does not actually need.

### 2. **OpenAI Rotates macOS Certificates After the Axios Supply-Chain Compromise**
OpenAI says a compromised Axios package touched a GitHub Actions workflow involved in signing ChatGPT Desktop, Codex, Codex CLI, and Atlas for macOS. The company says it found no evidence of user-data exposure or software tampering, but it is revoking and rotating signing material anyway, forcing app updates and turning a developer-tool compromise into a real trust-chain story.

### 3. **Anthropic Makes Claude Cowork Enterprise-Ready**
Claude Cowork is now generally available on all paid plans, and Anthropic is adding the governance layer enterprises actually care about: role-based access controls, group spend limits, usage analytics, OpenTelemetry events, per-connector action controls, and a Zoom connector that pulls meeting summaries and action items directly into workflows. This is Anthropic moving from “look what the agent can do” to “here is how the whole company deploys it without losing visibility or control.”

### 4. **SoftBank Launches a New ‘Physical AI’ Company**
SoftBank is reportedly creating a new company to build a model that can autonomously control machines and robots by 2030, with backing from Japanese industrial giants including Sony, Honda, and Nippon Steel. It is a clean signal that the next AI platform fight is not only about chat and software copilots, but about who owns the foundation model layer for robotics and machine control.

### 5. **Meta's Muse Spark Wants Your Health Data — and Shouldn't Have It**
WIRED tested Meta's new Muse Spark model and found it actively inviting users to paste in blood pressure readings, glucose data, and lab reports so it could chart trends and offer guidance. That is a brutal consumer-AI tension in one story: the bot wants intimate medical context, the privacy protections are weak, and the advice still is not good enough to justify the risk.

## Show Notes
```md
OPENCLAW DAILY — EPISODE 030 — April 13, 2026

[00:00] INTRO / HOOK
OpenClaw ships a release that makes memory retrieval happen before the
main reply. OpenAI rotates macOS certificates after a supply-chain
scare. Anthropic turns Claude Cowork into an enterprise deployment
surface. SoftBank launches a company for “physical AI.” And Meta’s new
health chatbot asks for raw medical data it has not earned the right to
see.

[01:55] STORY 1 — OpenClaw v2026.4.12: Active Memory, Local MLX Speech, and Smarter Plugin Loading
OpenClaw 2026.4.12 is not a flashy media release. It is a platform
quality release, and that is exactly why it matters.

The headline addition is an optional Active Memory plugin that runs a
specialized memory sub-agent right before the main reply. In practice,
that means OpenClaw can proactively pull in relevant user preferences,
context, and past details before answering instead of waiting for the
operator to explicitly say “remember this” or “search memory.” That is a
meaningful change in interaction design. A lot of “good AI memory” is
really just disciplined recall timing. OpenClaw is now making that timing
part of the product.

The second notable addition is an experimental local MLX speech provider
for macOS Talk Mode. That matters because it pushes more voice capability
onto the local device with explicit provider selection, local utterance
playback, interruption handling, and fallback behavior. The general trend
is obvious: local inference is no longer just for text and embeddings.
The voice stack is moving local too.

There is also a practical expansion of model choice. OpenClaw now bundles
both a Codex provider and an LM Studio provider. Codex-managed models can
use native auth, threads, discovery, and compaction on their own path,
while local or self-hosted OpenAI-compatible models become first-class via
LM Studio onboarding and runtime model discovery. That is exactly the kind
of provider-surface widening that makes an agent runtime harder to lock
into one vendor narrative.

And then there is the security and runtime hygiene side. Plugin loading is
now narrowed to manifest-declared needs so the CLI, providers, and
channels do not activate unrelated plugin runtime by default. Combined
with shell-wrapper hardening, approval fixes, startup sequencing cleanup,
and multiple dreaming and memory reliability fixes, the throughline is
clear: this release is about making the system remember more precisely and
load less recklessly.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.12

[09:05] STORY 2 — OpenAI Rotates macOS App Certificates After the Axios Compromise
OpenAI published a detailed response to the Axios developer-tool
compromise, and the important part is not whether attackers definitely got
OpenAI’s signing certificate. It is that OpenAI is treating the trust
chain as compromised enough to rotate anyway.

According to the company, a malicious Axios package was pulled into a
GitHub Actions workflow used in the macOS app-signing process on March 31.
That workflow had access to signing and notarization material used for
ChatGPT Desktop, Codex, Codex CLI, and Atlas. OpenAI says it found no
evidence that user data was accessed, no evidence that its products were
altered, and no evidence that the certificate was actually misused. But it
is still revoking and rotating the cert, publishing new builds, and giving
users a deadline to update before older macOS versions stop receiving
support.

This is one of those stories that matters because it compresses several AI
industry realities into a single incident. First: the frontier labs are
not just model vendors now. They are desktop-software distributors,
developer-platform operators, and identity anchors. Second: supply-chain
risk in seemingly boring developer dependencies can cascade straight into
consumer trust. And third: the integrity problem is no longer just “did
the model hallucinate?” It is also “can users trust that the binary on
their machine is really yours?”

OpenAI says the root cause included a floating tag in GitHub Actions and a
missing minimumReleaseAge safeguard for packages. That is not exotic. It
is ordinary build-pipeline hygiene. Which is the point. In 2026, ordinary
build-pipeline hygiene is now part of frontier AI risk.
→ https://openai.com/index/axios-developer-tool-compromise/

[14:55] STORY 3 — Anthropic Turns Claude Cowork Into an Admin Surface, Not Just a Demo
Anthropic announced that Claude Cowork is now generally available on all
paid plans, but the real story is the governance package shipping around
it.

The company added role-based access controls, group spend limits, usage
analytics, OpenTelemetry event emission, per-connector action controls,
and a Zoom connector that can bring meeting summaries, transcripts, and
action items into Cowork. Read that list carefully and you can see the
transition happening in real time. This is not about whether agents can do
cool things anymore. It is about whether a company can roll them out
across marketing, finance, legal, operations, and product without losing
policy control, auditability, or cost visibility.

Anthropic’s own description is revealing: most Cowork usage is already
coming from outside engineering. That means the next enterprise battleground
is not coding assistance alone. It is whether agentic workflows become a
shared operating layer for the rest of the company. Once that happens, the
admin console becomes strategic infrastructure.

The most important line item here might actually be the per-tool connector
controls. Read-only versus write access is the difference between an agent
that helps you understand the system and an agent that can change the
system. As companies move from experimentation to deployment, that line is
going to decide who gets approved and who gets blocked.
→ https://claude.com/blog/cowork-for-enterprise

[21:10] STORY 4 — SoftBank’s ‘Physical AI’ Bet Is Really a Robotics Platform Bet
SoftBank is reportedly forming a new company to build what it calls
“physical AI” — a model that can autonomously control machines and robots
by 2030. The reported backers include Sony, Honda, and Nippon Steel.

This is a strong signal because it reframes where some of the biggest
strategic players think value is heading. Consumer chat is crowded.
Enterprise copilots are crowded. The robotics and industrial-control layer
is not crowded in the same way, because the hard part is not just model
quality. It is data, control loops, hardware partnerships, safety, and the
ability to operate in the real world.

SoftBank has been telling versions of this story for a while through
robotics and sovereign infrastructure bets, but this move sharpens it.
What Japan appears to want is not merely access to foreign foundation
models. It wants a domestic stake in the model layer that will eventually
run factories, logistics systems, and robots. That is sovereign AI in a
more literal sense: not just local datacenters, but local control over
machine behavior.

If the software AI race was about search boxes and code editors, the next
race may be about who trains the default brains for embodied systems.
SoftBank is betting that layer is still available to be claimed.
→ https://www.theverge.com/ai-artificial-intelligence/910879/softbank-creates-new-company-building-physical-ai

[26:15] STORY 5 — Meta’s Muse Spark Shows the Worst Consumer-AI Incentive Loop
WIRED tested Meta’s new Muse Spark model and found that the assistant was
happy to ask for raw health data: fitness-tracker metrics, glucose
readings, lab reports, blood pressure numbers, the whole thing. The pitch
was predictable: give me your data, and I’ll chart the trends, flag the
patterns, and help you interpret what is happening.

The problem is that this is exactly the kind of high-context, high-trust
interaction where consumer AI products still do not deserve the role they
want. Medical experts quoted by WIRED raised two obvious concerns. One is
privacy: people are being nudged to upload highly sensitive information
into systems that are not governed like clinical environments and may use
that information for future training. The second is competence: the advice
still is not reliable enough to justify the intimacy of the data request.

That combination is the story. The model asks for data at a confidence
level that exceeds the actual safety and privacy posture of the system.
And because these bots are getting easier to access and more personalized
at exactly the moment healthcare remains expensive and fragmented, lots of
people are going to be tempted to use them as a substitute for care,
rather than a supplement to real medical judgment.

Meta says the model is not replacing your doctor. Fine. But if a bot keeps
inviting people to “dump the raw data” and then acts like a quasi-analyst,
it is already stepping into a role that demands much higher standards than
consumer AI currently meets.
→ https://www.wired.com/story/metas-new-ai-asked-for-my-raw-health-data-and-gave-me-terrible-advice/

[31:15] OUTRO / CLOSE
That’s today’s map: memory-before-reply as product design, software trust
chains as AI risk, agent governance as enterprise infrastructure, physical
AI as national strategy, and health-data prompts as a warning sign for
consumer deployment. Reply here to approve transcript generation.
```

## Links
- OpenClaw v2026.4.12: https://github.com/openclaw/openclaw/releases/tag/v2026.4.12
- OpenAI on the Axios developer-tool compromise: https://openai.com/index/axios-developer-tool-compromise/
- Anthropic — Making Claude Cowork ready for enterprise: https://claude.com/blog/cowork-for-enterprise
- SoftBank physical AI report: https://www.theverge.com/ai-artificial-intelligence/910879/softbank-creates-new-company-building-physical-ai
- WIRED on Meta's Muse Spark health-data prompts: https://www.wired.com/story/metas-new-ai-asked-for-my-raw-health-data-and-gave-me-terrible-advice/

## Chapters
- **[0:00] Hook — Memory First, Machines Next**
- **[1:55] OpenClaw v2026.4.12 — Active Memory, Local Speech, and Plugin Hardening**
- **[9:05] OpenAI Rotates macOS Certificates After the Axios Compromise**
- **[14:55] Anthropic Makes Claude Cowork Enterprise-Ready**
- **[21:10] SoftBank Launches a New ‘Physical AI’ Company**
- **[26:15] Meta's Muse Spark Wants Your Health Data — and Shouldn't Have It**
- **[31:15] Outro**

→ Reply here to approve transcript generation.
