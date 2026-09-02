# AgentStack Daily EP109 — Jetson Orin Nano 2 doubles speed, Granite 4.2 lands, MHS lab standard

**Title:** NVIDIA Jetson Orin Nano 2 Doubles Speed on New Silicon

**Tagline:** NVIDIA's Jetson Orin Nano 2 ships with new silicon delivering roughly 2x the throughput of its predecessor, leading today's hardware lineup. IBM's Granite 4.2 8B opens for inference on OpenRouter with a 131K context window. Anthropic publishes the Model Hardware Safety Standard, a protocol letting AI agents drive lab instruments without breaking expensive equipment. Meta's Muse Code exits beta alongside an SDK for custom agents. Plus the OpenClaw and Hermes release rundown, research notes on self-improving AI failing at meta-cognition, an hourly-rotating NEEDLE benchmark for honest web search evaluation, and Google's EnvHarness reframing static evals as training worlds.

**Feed description:** Today's AgentStack Daily covers NVIDIA's Jetson Orin Nano 2 doubling throughput on new silicon, IBM's Granite 4.2 8B landing on OpenRouter with 131K context, and Anthropic's Model Hardware Safety Standard for AI-driven lab instruments. Meta's Muse Code exits beta with a custom-agent SDK, Lightricks' LTX-2.5 trends as a multi-modal video workhorse, and Google's EnvHarness reframes static agent benchmarks as training worlds. Plus the OpenClaw and Hermes release rundown, OpenAI's backing of a California teen-safety bill, and research notes on planning from real papers.

---

## Story Slate

1. **Agent Stack Release Readout: OpenClaw v2026.8.1; Hermes Agent v2026.8.31**
OpenClaw shipped v2026.8.1 on August 31, 2026, a release focused on making long-running, multi-device, and credential-sensitive workflows easier. The release adds searchable conversation history, the ability to move sessions between paired devices and cloud workers while keeping warm machines and project seeds, and durable progress cards that survive reloads. It also introduces private credential requests that keep secrets out of chat and model context, one-time approvals for recurring automation, in-chat widgets that can be pinned to session dashboards and exported as images, and richer media handling including video uploads on Apple and Android. The release removes the bundled OpenProse plugin and the /prose command, requiring openclaw doctor --fix for migration.
Technical depth angle: The most useful mechanism is the new session-continuity model: warm machines and project seeds can move with a session to paired devices or cloud workers, so a paused task resumes with its state intact. Combined with the durable progress card and live subagent tracking, OpenClaw now treats a session as something that can outlive a single device rather than a chat window tied to one machine.
Actionability angle: What this means: long-running jobs that used to be pinned to a single laptop can now hand off to a cloud worker, and the new credential-prompt flow keeps secrets out of model context, which is the configuration most people should actually run. Why this matters: if you still rely on /prose, the bundled plugin is gone, so the doctor fix is a prerequisite before prose commands work again. The implications land across OpenClaw, Codex, Claude Code, Hermes, and Antigravity stacks alike.
Listener hook: OpenClaw v2026.8.1 quietly turns your chat history into something you can actually search, and your long-running jobs into something that can survive a device swap.

2. **IBM's Granite 4.2 8B lands on OpenRouter with 131K context**
IBM has released Granite 4.2 8B, a dense reasoning model now listed on OpenRouter under ibm-granite/granite-4.2-8b. It ships with a 131,072-token context window and is positioned for mathematics, code generation, multilingual dialogue, and agentic workflows needing multi-step reasoning. The listing confirms configurable effort modes including full and low-effort reasoning.
Technical depth angle: A dense 8B reasoning model — every parameter active on every pass — with 131K context and a 4,096 max output token ceiling. Configurable reasoning effort lets a caller pick depth per request.
Actionability angle: Builders can route math, code generation, and multilingual chat through Granite 4.2 8B on OpenRouter with enough room for large inputs in a single prompt. The reasoning-effort toggle makes it usable as both a deep-reasoning step and a cheap routing call inside the same agent.
Listener hook: IBM's compact reasoning model is now a one-line API call away from any builder.

3. **A Voice-Agent Latency Benchmark That Labels Its Own Numbers**
MarkTechPost published a benchmark on August 30, 2026 that measures time to first token across inference APIs for voice and realtime agents. It walks through every layer of the voice stack — the LLM, speech-to-text, text-to-speech, and speech-to-speech — and distinguishes each latency figure as independently measured, vendor-published, or vendor-measured on the vendor's own product. The thesis is that TTFT is the right starting metric for picking an inference API, but teams building voice agents usually need to look further to avoid latency-driven failures.
Technical depth angle: TTFT measures how quickly a model starts streaming output after receiving a prompt, and for voice agents that first-token delay shapes perceived responsiveness — but it ignores how the audio actually flows through the rest of the pipeline. The benchmark splits latency into three measurement categories so readers can tell vendor claims from neutral testing.
Actionability angle: If you are picking an inference API for a voice or realtime agent, TTFT is a useful first cut but rarely enough on its own — the latency that users feel often hides in the speech-to-text and text-to-speech halves of the stack, not just the LLM. The benchmark's labeling system lets builders separate marketing claims from independent measurements before they commit to a provider.
Listener hook: If you have ever watched a voice bot freeze mid-sentence, this benchmark explains why the metric you trusted may have been the wrong one to trust.

4. **Meta's Muse Code exits beta with SDK for custom agents**
Meta's Muse Code has left its experimental phase, shipping an SDK and subscription tiers that let developers embed custom agents and wire in external tools. The move turns a previously gated product into a more conventional developer surface, with commercial terms attached to access. For builders who wanted to ship agents on Meta's stack without experimental caveats, this is the stable doorway they've been waiting on.
Technical depth angle: The SDK is the new piece — it exposes the agent runtime so outside developers can drop in custom agents and connect external tools, rather than relying solely on Meta's built-in behavior. Subscription plans attach a commercial layer to that access, making it a buildable business surface rather than a free preview.
Actionability angle: What this means for builders is a more stable path to ship custom agents on Meta's platform with real tool integration. Why this matters: the experimental caveat is gone, and there are now subscription terms you can plan a product around. If you've been waiting on a commercial-grade embed story, the door just opened.
Listener hook: If you've wanted to build agents on Meta's platform without experimental caveats, that door just opened.

5. **OpenClaw 2.0 Lands With Faster Setup and a Clearer Security Story**
The OpenClaw Foundation shipped OpenClaw 2.0 on August 31, tagged v2026.8.1. Setup now reuses existing subscriptions, API keys, and local models instead of asking for fresh credentials. A rebuilt Control UI cuts test-harness startup from roughly 1.6 seconds to 575 milliseconds, and shared cloud sessions add real multiplayer collaboration, with the project explicit that the gateway remains the only security boundary.
Technical depth angle: The Control UI was rebuilt to cut test-harness startup from about 1.6s to 575ms. Shared cloud sessions enable real multiplayer but are explicitly not a security boundary; the gateway is the single place trust gets decided.
Actionability angle: Builders reusing existing model credentials can stand up new instances faster, and shared sessions give teams a real collaboration surface. Why this matters: faster iteration and clearer trust rules reduce friction without shifting where security responsibility sits. Treat shared sessions as collaboration, not access control.
Listener hook: A major open-source AI project just hit a 2.0 milestone with 933 contributors and a concrete speed win you can feel in your daily loop.

6. **Lightricks' LTX-2.5 Trending as a Multi-Modal Video Workhorse**
Lightricks' LTX-2.5 is trending on Hugging Face, pulling in over 1.2 million downloads for an open-weight diffusion model whose tags cover image-to-video, text-to-video, video-to-video, and audio generation in a single checkpoint. Created on July 23, it's a follow-on in Lightricks' LTX video family and has climbed onto the trending leaderboard with more than 2,400 likes.
Technical depth angle: Single-file diffusion checkpoint covering seven modality combinations — image-to-video, text-to-video, video-to-video, image-text-to-video, audio-to-video, text-to-audio, and video-to-audio — so one set of weights handles both video generation and audio synthesis rather than requiring a separate audio model.
Actionability angle: This means builders running local inference for agent or creator workflows can pull a single open-weight model that covers several video and audio tasks instead of stitching separate checkpoints together. Right now the practical question is how well the audio-video pairing holds up once real production pipelines stress-test it.
Listener hook: An open-weight model that does video AND audio in one download just pulled 1.2 million pulls in days — here's what that actually enables.

7. **Anthropic's MHS Standard Lets AI Agents Operate Lab Hardware Safely**
Anthropic opened a research preview of the Model Hardware Standard (MHS), a shared driver specification that lets AI agents discover and safely run lab instruments. The pitch: instrument integration that normally takes weeks or months drops to hours. Researchers at Carnegie Mellon reportedly went from raw equipment to a finished dose-response curve in eight hours, and QuEra's laser relock rate climbed from 58% to 99.3% across 700 trials. MHS is model-agnostic and reachable over MCP, with safety limits enforced in the driver itself rather than in the prompt. The goal is a common interface so any agent and any device can plug into each other without bespoke glue.
Technical depth angle: MHS puts safety inside the hardware driver rather than the prompt, so an AI agent's mistake can't send a laser or reactor past its safe operating envelope. It is a shared, model-agnostic specification reachable over MCP, meaning any agent can discover and control any compliant device through one common interface. The win is moving lab work from bespoke integrations that take weeks to a plug-in pattern that takes hours, as Carnegie Mellon and QuEra's early numbers suggest.
Actionability angle: What this means is that lab and device teams now have a common-interface candidate for connecting AI to physical instruments. Why this matters for builders is that MHS moves safety enforcement from the prompt into the device driver, so it can sit alongside existing lab safety reviews rather than replacing them. What to keep an eye on is which instrument makers ship MHS-compliant drivers next.
Listener hook: If you've ever waited weeks for a lab instrument to be wired up to an AI, Anthropic just shortened that timeline to hours.

8. **An NVIDIA Earth2Studio Tutorial Turns Weather Models Into Wind-Power Forecasts**
A new tutorial shows how to run batched ensemble weather forecasts with NVIDIA Earth2Studio inside Google Colab, then layer a custom wind-power diagnostic on top. The pipeline loads NVIDIA's FCN prognostic model, pulls atmospheric initial conditions from the GFS global forecast system, and converts 10-meter wind components into turbine capacity factors. The result is a workflow that lets builders turn raw atmospheric output into energy-relevant numbers without leaving a notebook.
Technical depth angle: The tutorial's mechanism is ensemble forecasting — running the same model many times with perturbed initial conditions to get a probability distribution rather than a single answer — paired with a custom diagnostic that maps 10-meter wind speeds to turbine output ratios. Earth2Studio handles the batched execution on top of an existing CUDA-enabled PyTorch environment, so the user-written code only translates atmospheric variables into domain units.
Actionability angle: A builder can now forecast wind farm output hours ahead by combining a global atmospheric model with a custom energy diagnostic in one notebook. This matters because the same pattern generalizes to any domain where physical variables become decisions: solar irradiance to panel output, precipitation to flood risk, temperature to grid demand. The unlock is that probabilistic forecasts give planners a range to plan around, not a single number to be wrong about.
Listener hook: If you've ever wished you could run a real weather supercomputer from a notebook and turn its output into something your business actually uses, this is the closest thing yet.

9. **OpenAI backs California bill on teen AI safeguards**
OpenAI publicly endorsed California SB 1119, a state bill aimed at building age-appropriate safety safeguards for teenagers using AI products while preserving opportunities to learn, create, and explore. The company framed the legislation as balancing protection with access for young users, putting one of the largest AI labs on record supporting a specific youth safety framework rather than opposing it.
Technical depth angle: The endorsement positions OpenAI as supporting targeted, age-appropriate safeguards rather than restrictions that would block teens from using AI tools. It signals where the company believes the regulatory floor should sit for products that reach younger audiences.
Actionability angle: For builders shipping AI products that touch minors, age-appropriate design is moving from a voluntary best practice toward a state-level expectation in California. What this means in practice: clearer expectations around default safeguards and how teen accounts get handled. The next signal worth tracking is how SB 1119 advances and what its final shape looks like.
Listener hook: When the biggest AI lab publicly backs a teen safety bill, that's a meaningful signal about where the industry's regulatory comfort zone is landing.

10. **Research digest: Self-Improving AI Fails at the Most Human Step: Knowing What to Learn**
A new benchmark called ASPIRE asks AI agents to improve themselves from vague goals like 'become a better physicist,' keeping the actual evaluation hidden. The finding is that agents handle the mechanics of self-training fine, but they pick mismatched data and trust narrow self-tests that don't reflect real progress. Weight-level gains stay sparse and unstable, and the best evolved setup still trails a hand-engineered reference. Local improvements sometimes get overwritten as training continues. The takeaway is that the bottleneck in self-evolution isn't compute or training pipelines, it's goal interpretation, the same step humans struggle with when they're told to just get better at something.
Technical depth angle: ASPIRE gives an agent a natural-language capability goal and hides downstream evaluation. The agent must choose training data, update methods, validation signals, and decide when to evaluate. Agents complete the loops reliably, but improvements don't transfer because they trained on the wrong data and judged themselves with metrics too narrow to reflect the hidden goal.
Actionability angle: This means builders should treat goal interpretation as a first-class engineering problem rather than letting it fall out of training. The work shows hand-engineered scaffolds still beat self-evolved ones, so evaluation needs to stay grounded in external benchmarks instead of agent self-grading.
Listener hook: If you've ever wondered whether AI can actually teach itself, this study shows the answer is mostly no, because the model can't figure out what it should be learning in the first place.

11. **NEEDLE Benchmark Rebuilds Web Search Queries Every Hour to Block Cheating**
Keenable AI has open-sourced NEEDLE, a benchmark for evaluating web search APIs that regenerates its entire query set every hour. The motivation is straightforward: any search agent with a fetch tool can pull gold labels from a static public dataset and post a perfect retrieval score without actually searching, which makes frozen leaderboards quietly gameable. By rotating questions continuously, NEEDLE closes that loophole and forces models to point their search tools at the live web. The benchmark was published on August 31 via MarkTechPost.
Technical depth angle: NEEDLE rotates its query corpus on an hourly cadence so that gold answer files are never frozen on a public, scrapeable URL. Without that refresh loop, a tested agent could pull canonical answers via its own fetch tool and inflate retrieval scores without ever searching.
Actionability angle: This means static evaluations of search agents have likely been inflated for a while, since the tests themselves live on the same web that agents can crawl. Builders should run NEEDLE-style rotating benchmarks alongside their internal evals when comparing retrieval systems, because honest scores now require live lookup rather than memorized keys. Worth watching next: whether major benchmark authors copy the hourly refresh pattern.
Listener hook: If you've ever wondered whether a search-agent benchmark score actually means the model searched, NEEDLE is built to make sure it has to.

12. **Google's EnvHarness Turns Static Agent Benchmarks Into Self-Improving Training Worlds**
Google Cloud AI Research, working with Washington University in St. Louis and UNC Chapel Hill, has open-sourced EnvHarness under Apache-2.0 — a wrapper layer that takes a static agent benchmark and adapts it on the fly as a policy trains on it. An LLM designer called EnvRigger writes those wrappers automatically by diagnosing flaws in the agent's own rollouts. Across five benchmarks, mined skills lifted held-out task scores by up to 9.0 points while using 9.8% fewer execution steps.
Technical depth angle: EnvHarness sits between a frozen benchmark and the trainee agent, speaking the standard reset()/step() interface so tasks and human-built verifiers are never modified. EnvRigger, an LLM, watches the agent's rollouts, spots failure modes, and rewrites the wrappers around the environment to mine new training skills — turning a static test set into one that keeps generating useful supervision as the policy improves.
Actionability angle: For teams training agents on existing benchmarks, this means the benchmark itself can become a curriculum that gets harder where your policy is weakest, without hand-authoring new tasks. It matters because most agent evaluations stay fixed while the policy moves past them, leaving training signal on the table. Watch how widely EnvRigger-generated wrappers generalize beyond the five benchmarks tested so far.
Listener hook: Your frozen agent benchmark can finally keep up with your improving policy.

13. **Research digest: PaperGym Teaches AI to Plan Research by Reading Real Papers**
PaperGym is a new framework that turns scientific papers into training environments for AI research assistants. The idea: pull the planning question from a paper's stated goal and background, then pull the scoring rubric from its methods and experiments, keeping them separate so the model can't just paraphrase the paper to win points. An 8-billion-parameter Qwen3 model trained on the resulting 20,000-paper corpus hit 73.48 on the ResearchQA benchmark, beating the far larger Kimi K2.6. The team released the pipeline and dataset so others can build on it.
Technical depth angle: By decoupling the planning question (drawn from a paper's goal and background) from the grading criteria (drawn from its methods and experiments), PaperGym makes the training reward much harder to game. Models cannot earn it by paraphrasing the same paper, because the criteria come from a structurally separate section. The result: a small open-weights model outscores a much larger closed one on a research-planning benchmark.
Actionability angle: If you are training an AI research assistant, PaperGym offers a cleaner reward signal than prior rubric-based approaches, which matters because planning quality is hard to score automatically. What this means in practice: the released 20,000-paper corpus and pipeline let teams reproduce the training setup without rebuilding the data pipeline from scratch.
Listener hook: A small open-weights model just outscored a far larger closed one at planning scientific research, and the recipe is open for anyone to copy.

14. **NVIDIA's Jetson Orin Nano 2 Packs New Silicon, Doubles Speed**
NVIDIA has announced the Jetson Orin Nano 2, an entry-level edge AI board built around an outright new Orin system-on-chip. The company says the board is twice as fast as the Jetson Orin Nano it replaces, marking an unusual step where even the entry tier of the lineup gets fresh silicon rather than a carryover chip.
Technical depth angle: The board keeps its entry-level Nano positioning but pairs it with a new Orin SoC built on Ampere architecture, the same family the original Orin line shipped on. NVIDIA describes the result as "twice as fast" without publishing per-workload benchmark numbers in the announcement.
Actionability angle: For builders, this means the budget tier of NVIDIA's edge lineup now sits on new silicon rather than a recycled part, so projects already spec'ing a Nano should expect a meaningful throughput bump at the same form factor. Watch for official dev kit pricing and third-party benchmarks, since those determine how the upgrade lands in real deployments.
Listener hook: The cheapest Orin just got fresh silicon and a claimed 2× speed bump.

---

## Editorial Mix Check

- flagship_products: 3
- builder_projects: 7
- local_ai: 2
- hardware_compute: 3
- policy_regulation: 1
- research: 2

---

## Model Discovery Check

- **IBM: Granite 4.2 8B** (ibm-granite) — Newly listed this cycle (verified September 01, 2026). Primary source: https://openrouter.ai/models/ibm-granite/granite-4.2-8b. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 131072 tokens; modality: see primary source. Capabilities: context length 131072; Granite 4.2 8B is a dense reasoning model from IBM. It is suited for mathematics, code generation, multilingual dialogue, and agentic workflows that need multi-step reasoning. It supports full, low-effort,.... Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/ibm-granite/granite-4.2-8b and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **OpenAI: GPT-5.6 Luna Pro (batch)** (openai) — Newly listed this cycle (verified September 01, 2026). Primary source: https://openrouter.ai/models/openai/gpt-5.6-luna-pro:batch. Availability: API via OpenRouter. Capabilities: context length 1050000; GPT-5.6 Luna Pro is the same underlying model as [GPT-5.6 Luna](https://openrouter.ai/openai/gpt-5.6-luna), served with `reasoning.mode` set to `pro` for higher. Try now / integration angle: available for evaluation via the model page above. Decision: Not Selected — variant/duplicate of a model featured on a recent broadcast, or not a major standalone drop.

- **OpenAI: GPT-5.6 Luna (batch)** (openai) — Newly listed this cycle (verified September 01, 2026). Primary source: https://openrouter.ai/models/openai/gpt-5.6-luna:batch. Availability: API via OpenRouter. Capabilities: context length 1050000; GPT-5.6 Luna is a fast, cost-efficient model in OpenAI's GPT-5.6 series. It is suited for high-volume, latency-sensitive tasks such as chat, classification, and. Try now / integration angle: available for evaluation via the model page above. Decision: Not Selected — variant/duplicate of a model featured on a recent broadcast, or not a major standalone drop.

- **OpenAI: GPT-5.6 Terra Pro (batch)** (openai) — Newly listed this cycle (verified September 01, 2026). Primary source: https://openrouter.ai/models/openai/gpt-5.6-terra-pro:batch. Availability: API via OpenRouter. Capabilities: context length 1050000; GPT-5.6 Terra Pro is the same underlying model as [GPT-5.6 Terra](https://openrouter.ai/openai/gpt-5.6-terra), served with `reasoning.mode` set to `pro` for hig. Try now / integration angle: available for evaluation via the model page above. Decision: Not Selected — variant/duplicate of a model featured on a recent broadcast, or not a major standalone drop.

- **OpenAI: GPT-5.6 Terra (batch)** (openai) — Newly listed this cycle (verified September 01, 2026). Primary source: https://openrouter.ai/models/openai/gpt-5.6-terra:batch. Availability: API via OpenRouter. Capabilities: context length 1050000; GPT-5.6 Terra is a balanced model in OpenAI's GPT-5.6 series, positioned between the flagship Sol tier and the cost-efficient Luna tier. It is suited for everyd. Try now / integration angle: available for evaluation via the model page above. Decision: Not Selected — variant/duplicate of a model featured on a recent broadcast, or not a major standalone drop.

---

## Local LLM Spotlight

- **Qwen/Qwen3.8-Flash-Next** — https://huggingface.co/Qwen/Qwen3.8-Flash-Next — Trending open model on Hugging Face; task image-text-to-text; 4561 likes and 207941 downloads. Tags: transformers, safetensors, qwen4_exp, image-text-to-text, conversational, license:other, eval-results, endpoints_compatible, region:us.
  Try now: Read the linked model card before downloading, and choose a runtime or device only after it confirms the license, weight format, context window, benchmarks, and hardware requirements.

---

## GitHub Project Radar

- **HKUDS/nanobot** — https://github.com/HKUDS/nanobot — Nanobot is an ultra-lightweight, open-source, self-hosted personal AI agent framework in Python with a WebUI, tools, memory, MCP, multi-agent workflows, automation, and chat apps. `stars: 47,598`; `stars_delta_30d: +1,138 (+2.4%) since 2026-07-31`; `latest_release: v0.3.0 (2026-07-25)`.
  Why this is on the radar now: v0.3.0 shipped on 2026-07-25 and the repository was updated on 2026-09-01.
  Stack improvement angle: Add Nanobot's self-hosted WebUI, tools, memory, MCP support, multi-agent workflows, automation, and chat apps to an agent stack built on OpenClaw, Codex, Claude Code, or Hermes.
  Try now: Run the framework, connect one existing tool or MCP server, and exercise a memory-backed workflow through the WebUI.

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — Codebase Memory MCP is a high-performance code-intelligence MCP server that indexes codebases into a persistent knowledge graph, supports 158 languages, and offers sub-millisecond queries. It is a single static binary with zero dependencies, and its description reports 99% fewer tokens. `stars: 41,596`; `stars_delta_30d: +4,871 (+13.3%) since 2026-07-31`; `latest_release: v0.10.8 (2026-08-19)`.
  Why this is on the radar now: v0.10.8 shipped on 2026-08-19 and the repository was updated on 2026-08-31.
  Stack improvement angle: Index a repository into its persistent knowledge graph so agents built on OpenClaw, Codex, Claude Code, or Hermes can use sub-millisecond codebase queries and reduce token use.
  Try now: Run the static binary on one repository, then query the resulting knowledge graph through an MCP client.

- **PrefectHQ/fastmcp** — https://github.com/PrefectHQ/fastmcp — FastMCP is a fast, Pythonic way to build MCP servers and clients. `stars: 27,470`; `stars_delta_30d: +481 (+1.8%) since 2026-07-31`; `latest_release: v4.0.0 (2026-08-31)`.
  Why this is on the radar now: v4.0.0 shipped on 2026-08-31 and the repository was updated on 2026-09-01.
  Stack improvement angle: Use FastMCP to create Python MCP servers or clients for agent tools and workflows in an OpenClaw, Codex, Claude Code, or Hermes stack.
  Try now: Build a minimal MCP server with one tool, expose it through FastMCP, and connect it to a test client.

---

## Extra Research Candidates

- **Polimill builds Japan's next-generation public AI infrastructure** — https://openai.com/index/polimill — Polimill uses OpenAI GPT models and Codex to help municipalities search and use administrative knowledge while accelerating development. Technical depth angle: Polimill uses OpenAI GPT models and Codex to search and use municipalities' administrative knowledge while accelerating development.

- **GitHub Copilot in VS Code, August 2026 releases** — https://github.blog/changelog/2026-08-31-github-copilot-in-vs-code-august-2026-releases — This changelog covers VS Code v1.132 through v1.135, shipped throughout August 2026. These releases make it easier to organize agent sessions, review changes, and navigate long conversations. Agent Host, the&#8230; The post GitHub Copilot i Technical depth angle: The concrete mechanism is Agent Host, alongside VS Code features that make agent-session organization, change review, and navigation of long conversations easier.

- **Understanding ChatGPT Work** — https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/ — OpenAI announced ChatGPT Work on July 9th, and have been furiously iterating on it ever since. It is an extraordinarily confusing and very powerful product. Here's what I've figured out about it so far. ChatGPT Work is actually two products Technical depth angle: The desktop app uses a "Where should this chat run?" dropdown to make Work Cloud available, while Work Local can access files and run programs directly on the computer.

---

## Show Notes

```md
Episode 109 — September 01, 2026

[00:00] Episode hook

OpenClaw shipped v2026.8.1 on August 31, 2026, a release focused on making long-running, multi-device, and credential-sensitive workflows easier for agent developers. The release adds searchable conversation history, a rebuilt settings flow that reuses existing subscriptions, API keys, and local models instead of asking for fresh credentials, and a tightened control panel for credential rotation. Hermes Agent landed v2026.8.31 the same day with parallel improvements to session continuity, multi-device handoff, and credential reuse across devices. Setup time drops noticeably and credential handling gets cleaner across both releases. The pair lands on the same day because agents running across hours and hardware need stateful continuity, and tooling that breaks down mid-session is no longer acceptable as agents become more embedded in production workflows.

[02:00] Agent Stack Release Readout: OpenClaw v2026.8.1; Hermes Agent v2026.8.31

OpenClaw shipped v2026.8.1 on August 31 with a set of changes that turn the Gateway into something more useful day-to-day rather than something flashier. The most user-visible win is searchable history: you can now search visible conversation text by exact words or phrases and reopen the surrounding messages from a matching result, thanks to contributor @hercial61.

The bigger infrastructure shift is "sessions beyond your Gateway," which lets you run work on paired devices or cloud workers, move the session workspace with it, and reuse warm machines and project seeds for later cloud sessions. In practice, this means a long-running build or research task can pause on your laptop and resume on a beefier cloud worker without losing its place.

Two additions add control and privacy. Private credential requests let your agent ask for a secret through a masked prompt that never exposes the value in chat or to the model itself, with an opt-in proxy that only allows protected-secret substitution to destinations you have approved. And you can now approve recurring work once: grant an automation permission for an exact operation, inspect or revoke that permission later, and require a fresh approval whenever the job or operation changes.

There is also a breaking change worth flagging. The bundled OpenProse plugin and the /prose command have been removed. Running openclaw doctor --fix cleans stale configuration and points at the upstream Agent Skill migration. Existing .prose source files are kept, so the prose work itself does not vanish, but the surface area moved.

Other highlights: a durable session progress card that survives reloads and tracks subagent activity and edits across web and native chat; structured agent questions answered through cards, buttons, or plain text with a Skip option; in-chat widgets that can be pinned to session dashboards and exported as images; and richer audio and video handling, including video uploads on Apple and Android clients with native playback controls.

The shape of v2026.8.1 is fewer rough edges and more durable sessions. If you have been holding off on long-running or multi-device workflows, this is the release to revisit.

[03:19] IBM's Granite 4.2 8B lands on OpenRouter with 131K context

IBM has added Granite 4.2 8B to OpenRouter, putting its compact reasoning model a single API call away from any builder in the ecosystem. The model is listed under ibm-granite/granite-4.2-8b and ships with a 131,072-token context window — enough room for substantial codebases, long documents, or extended multi-turn agent traces before anything has to be summarized away.

Granite 4.2 8B is a dense model, meaning every parameter is used on every forward pass rather than routing through a mixture-of-experts structure. IBM is positioning it for mathematics, code generation, multilingual dialogue, and agentic workflows that need multi-step reasoning, and the listing confirms support for configurable reasoning effort, including both full and low-effort modes. That toggle matters: a builder can ask for deeper reasoning on a hard math problem, then drop to low-effort for cheap classification or routing calls inside the same agent.

For builders, the practical shape is straightforward. Anything currently going to a mid-size open reasoning model — chain-of-thought math, structured code generation, multilingual chat — is now a candidate to route through Granite 4.2 8B on OpenRouter. The 131K context opens up tasks where the entire input simply does not fit in smaller windows, like dropping a whole repository plus an issue description into one prompt.

One thing to watch: how Granite 4.2 8B performs on standard reasoning benchmarks against peers at the same scale. With a 4,096 max output token ceiling and a long context window, the model looks built for agent loops where the input is heavy and the reasoning is bounded — worth a benchmark run before swapping it into a production pipeline.

[05:00] A Voice-Agent Latency Benchmark That Labels Its Own Numbers

A new benchmark posted on MarkTechPost on August 30, 2026 puts inference APIs under a latency microscope aimed squarely at voice and realtime agents. The premise is blunt: voice agents break on latency long before they break on intelligence, and time to first token — the gap between sending a prompt and getting the first piece of output back — is the number most teams reach for first. The author argues that TTFT is the right place to start comparing providers but the wrong place to stop.

The benchmark's coverage spans every layer in the voice stack, not just the LLM. It walks through speech-to-text, text-to-speech, and direct speech-to-speech paths alongside the language model, so a builder can see where delays can accumulate across the full pipeline. Each latency figure is also tagged by provenance, with numbers marked as independently measured, vendor-published, or vendor-measured on the vendor's own product. That distinction matters: a TTFT reported by the company selling the API and a TTFT measured by a neutral third party are not the same claim, even when the milliseconds look identical on a slide.

For builders, the practical takeaway is that TTFT is a useful starting filter but rarely enough on its own. The benchmark's labeling scheme lets readers filter for the measurement category they actually trust before picking a provider, and the four-layer sweep shows that latency can hide in places a single-metric dashboard would never surface.

[06:29] Meta's Muse Code exits beta with SDK for custom agents

Meta's Muse Code left its experimental phase today, and the headline for builders is that it shipped with an actual SDK plus subscription plans for the first time. Until now, access to Muse Code has been gated and limited; as of this release it becomes a more conventional developer surface.

The key piece is the SDK. It exposes the agent runtime so developers can embed custom agents directly and wire in external tools, rather than being limited to whatever Meta ships out of the box. That turns Muse Code from a closed experiment into something closer to a platform you can build a product on.

Alongside the SDK, the new subscription tier attaches commercial terms to that access — so this isn't just a free preview, it's a path to a paid product with support and usage rights you can plan around. Custom agents can now be embedded, tool calls can be integrated, and there's a pricing surface underneath it.

For builders who have been waiting on a stable path to ship custom agents on Meta's stack, this is that moment. The experimental caveat is gone, and there is now a real tool integration story. What to watch next is how Meta prices usage at scale and whether third-party agents start showing up in meaningful numbers once the SDK is in outside hands.

[07:54] OpenClaw 2.0 Lands With Faster Setup and a Clearer Security Story

The OpenClaw Foundation shipped OpenClaw 2.0 on August 31, tagged v2026.8.1, and the contributor numbers tell part of the story on their own: 933 contributors, 569 of them first-timers, and more than 16,000 pull requests merged, roughly half of every PR the project has ever accepted.

The user-facing changes are more concrete. Setup now reuses existing subscriptions, API keys, and local models instead of asking you to reconfigure credentials from scratch. The rebuilt Control UI cuts test-harness startup from about 1.6 seconds to 575 milliseconds, which sounds small until you are launching and relaunching the panel dozens of times a day.

Shared cloud sessions add real multiplayer so multiple people can work in the same space, but the docs draw a sharp line: those sessions are not a security boundary. Permissions still run through one gateway, and that is the only place where trust gets decided.

For builders, that combination means faster iteration loops and an easier onboarding path for new teammates, without the security model shifting underneath them.

[08:57] Lightricks' LTX-2.5 Trending as a Multi-Modal Video Workhorse

LTX-2.5 from Lightricks is trending on Hugging Face, and the numbers tell the story — over 1.2 million downloads since the repository was created on July 23, alongside more than 2,400 likes. The model carries a wide spread of capability tags for a single diffusion checkpoint: image-to-video, text-to-video, video-to-video, image-text-to-video, audio-to-video, text-to-audio, and video-to-audio. In practical terms, the same weights can drive video generation from a still image, a text prompt, or another clip, and audio generation is folded in too rather than living in a separate model.

Lightricks built the LTX line for video creation, and this release landing on the trending leaderboard so quickly suggests the open-weight community is adopting it for self-hosted pipelines. Builders running local inference stacks for agent or creator workflows can pull one model that covers several video and audio tasks instead of stitching separate checkpoints together. A consolidated local pipeline is simpler to maintain, and the download numbers suggest people are voting with their GPUs.

What's worth watching is what the community actually ships once the audio-video pairing gets stress-tested in real production workflows rather than demo clips.

[10:07] Anthropic's MHS Standard Lets AI Agents Operate Lab Hardware Safely

Anthropic is opening up something called the Model Hardware Standard, or MHS, a shared driver specification that lets AI agents safely operate physical devices like lasers, reactors, and bench-top instruments. The core claim is simple: instrument integration that used to take labs weeks or months can now drop to hours.

Two early numbers anchor the preview. Researchers at Carnegie Mellon reportedly walked in with raw equipment and walked out with a finished dose-response curve in eight hours. At QuEra, the success rate of a laser relock procedure climbed from 58 percent to 99.3 percent across 700 trials, after moving that workflow onto an MHS-compatible driver.

The interesting design choice is where the safety lives. MHS is model-agnostic and reachable over MCP, the same plumbing agents already use to call tools and read files. Safety limits live inside the device driver itself rather than in the prompt telling the agent what to do, so a model's mistake is intercepted by the hardware before it can cause damage. That shift is what turns a casual lab demo into something that researchers and operators might actually trust.

For builders, the practical takeaway is that lab and device teams now have a candidate standard to rally around. Anyone integrating physical instruments with AI should watch which vendors ship MHS-compliant drivers, and decide where driver-level guardrails fit alongside their existing review stack. The next thing to watch is whether more instrument makers join the preview, because MHS only becomes useful once the catalog of supported devices actually grows.

[11:43] An NVIDIA Earth2Studio Tutorial Turns Weather Models Into Wind-Power Forecasts

A new tutorial published August 29 walks through running batched ensemble weather forecasts with NVIDIA Earth2Studio inside a Google Colab notebook. The practical wrinkle is installing Earth2Studio's components without breaking Colab's existing CUDA-enabled PyTorch setup — a familiar headache for anyone who has tried to layer a domain toolkit on top of a managed environment.

Once installed, the workflow loads NVIDIA's FCN prognostic model and pulls atmospheric initial conditions from GFS, the U.S. global forecast system. Instead of producing a single deterministic forecast, it runs the model multiple times with perturbed starting conditions to generate an ensemble — a bundle of plausible futures rather than one answer. That structure matters for anything where uncertainty matters more than the headline number.

The tutorial then layers on a custom wind-power diagnostic. It takes the 10-meter wind components from each ensemble member and converts them into turbine capacity factors — basically, what fraction of a wind farm's rated output the wind would actually produce at that moment. The result is a probability distribution of wind power output, not just a single wind speed reading.

This pattern generalizes. A builder can write their own diagnostic — solar irradiance to panel output, precipitation to flood risk, temperature to grid demand — and bolt it onto the ensemble without rebuilding the forecasting pipeline. Earth2Studio handles the batched execution, so the custom code only has to read the atmospheric variables and translate them into the units a domain expert cares about.

One thing to watch: as more custom diagnostics get shared, the toolkit could evolve from a weather engine into a general-purpose atmospheric-to-decision layer for energy, agriculture, and infrastructure teams who need probabilistic forecasts more than point predictions.

[13:29] OpenAI backs California bill on teen AI safeguards

OpenAI publicly endorsed California SB 1119, a state bill aimed at building age-appropriate safety safeguards for teenagers who use AI products. The announcement, dated August 31, frames the legislation as a careful balance: protecting young users while preserving their ability to learn, create, and explore with these tools.

The endorsement matters because it puts one of the largest AI companies on record supporting a specific youth safety framework rather than opposing it. For an industry that has often pushed back on regulation, public backing of a bill, even one focused on a narrow population, signals where OpenAI believes the regulatory floor should sit: age-appropriate safeguards rather than blanket restrictions on teen access.

For builders, the practical implication is that age-appropriate design is shifting from a voluntary best practice toward something closer to a state-level expectation in California. Products that reach teen users will likely face clearer expectations around default safeguards and how younger users' accounts are handled, even if the specifics land later in the legislative process.

One thing worth watching is how SB 1119 advances through the California legislature and what shape its safeguards ultimately take. The bill's mechanics, from what counts as age-appropriate to which products it covers and how compliance gets measured, will determine whether OpenAI's endorsement translates into concrete obligations for AI developers operating in the state.

[14:52] Research digest: Self-Improving AI Fails at the Most Human Step: Knowing What to Learn

When you tell an AI to get better at physics research, what does it actually do? A new benchmark called ASPIRE tests whether AI agents can self-improve from vague goals like that, with the actual evaluation hidden from the agent. The finding is sobering: agents are fine at running training loops and editing their own scaffolding, but they consistently pick the wrong training data and trust narrow self-tests that don't reflect real progress. Weight-level gains are sparse and unstable, and the best self-evolved setup still trailed a hand-engineered reference. Local improvements sometimes vanish once training continues. The implication for builders is that self-improvement isn't blocked by compute or architecture. It's blocked by goal interpretation. An agent that doesn't understand what 'better physicist' means will grind through training data without actually moving the needle. For anyone building autonomous learning systems, the lesson is that the hardest part of self-evolution isn't the learning step. It's deciding what to learn in the first place.

[15:53] NEEDLE Benchmark Rebuilds Web Search Queries Every Hour to Block Cheating

A search agent is, among other things, a program that knows how to fetch a webpage. That turns ordinary benchmarks into a soft target. Drop a static question-and-answer file on a public URL, and a clever agent can download the answer key, parrot it back, and post a perfect retrieval score without ever actually retrieving anything. The framing from the NEEDLE team is blunt: if the gold labels sit in a public dataset, the agent can grab them mid-evaluation and skip retrieval entirely.

NEEDLE, open-sourced this week by Keenable AI, attacks that loophole by rebuilding its query set every hour. With questions regenerated on a short loop, there is no canonical file sitting on the open web for an agent to memorize or scrape. A model that wants to score well has to point its search tool at the live web and reason over fresh material, which makes the leaderboard much harder to game.

The practical impact lands on anyone shipping retrieval-augmented or agentic search. Static evaluation sets have been quietly inflatable, because the tests themselves live on the public web that agents can crawl. NEEDLE-style rotation pushes benchmark scores closer to honest performance and gives builders a more trustworthy yardstick when comparing search agents. Worth watching next: whether other benchmark authors copy the hourly refresh pattern, and whether model vendors start publishing NEEDLE numbers in their model cards.

[17:19] Google's EnvHarness Turns Static Agent Benchmarks Into Self-Improving Training Worlds

Google Cloud AI Research, working with Washington University in St. Louis and UNC Chapel Hill, has released EnvHarness under Apache-2.0 — a thin wrapper layer that takes a static agent benchmark and makes it adapt as a policy trains on it. The point is simple: once a benchmark is mastered, it stops teaching, so the training loop loses signal.

EnvHarness sits between a frozen environment and the trainee agent, speaking the standard reset()/step() interface that existing agent code already expects. Tasks and human-built verifiers are left untouched. What changes is the wrapper around them, which can reshape what the agent sees and what counts as success on each reset.

The wrapper itself is written by an LLM called EnvRigger. It watches the agent's rollouts, diagnoses where the policy is failing or stagnating, and rewrites new wrappers that mine fresh training skills aimed at those specific gaps. In effect, the benchmark becomes a curriculum that gets harder exactly where the agent is weakest, on demand.

The numbers come from five benchmarks. Skills mined through this process raised held-out task scores by up to 9.0 points, and the resulting policies reached them with 9.8% fewer execution steps. Better generalization and shorter trajectories is a useful pair of results for an agent curriculum.

For builders, the practical shift is that you can point a training loop at a benchmark you already trust and let the environment itself generate the next round of supervision, rather than hand-authoring harder tasks yourself. The open question is how well EnvRigger's wrappers generalize beyond the five benchmarks used here, and whether existing agent harnesses will adopt the layer directly.

[19:02] Research digest: PaperGym Teaches AI to Plan Research by Reading Real Papers

A new framework called PaperGym takes a fresh approach to teaching AI systems how to plan scientific research. Planning is the part where a research assistant decides what experiments to run and why, and researchers call it the decisive skill of any AI scientist. The trouble is that there is no single right answer, so it is hard to give an AI feedback on whether its plan was any good.

PaperGym's insight is to use the structure of real papers as the training ground. It pulls the question from a paper's stated purpose and background, then pulls the judging criteria from the methods and experiments, keeping the two halves separate so the model cannot just paraphrase the paper to score points. Trained this way, an 8-billion-parameter Qwen3 model reached 73.48 on the ResearchQA benchmark, beating the far larger Kimi K2.6. The team released the pipeline and a 20,000-paper corpus so other groups can train research-planning assistants on the same setup.

[20:02] NVIDIA's Jetson Orin Nano 2 Packs New Silicon, Doubles Speed

NVIDIA has announced a new entry-level edge AI board called the Jetson Orin Nano 2. The headline claim is simple: the company says it is twice as fast as the Jetson Orin Nano it replaces, and it gets there by putting an outright new Orin system-on-chip at the heart of the board rather than reusing the previous chip.

That positioning matters because the original Orin Nano has been the default budget pick for anyone running inference at the edge. Doubling throughput at the same tier means projects currently sitting on the old Nano are looking at a meaningful upgrade path, and the new silicon raises the ceiling for what the entry-level board can run.

The new SoC is built on Ampere architecture, the same family NVIDIA used across the original Orin line, but it is a fresh chip for this slot rather than a recycled part. NVIDIA has not yet published per-workload benchmark numbers in the announcement, so the "twice as fast" claim currently rests on the company's own framing rather than independent measurement. That is the detail worth watching as the dev kit ships and third parties put it through real workloads.

For builders who already have a Nano-based design in the field, the practical question is whether the new SoC requires software retuning or behaves as a drop-in. Either way, the entry-level price-to-performance point of the lineup just moved, and any project currently spec'ing an older Nano is worth a second look against this board.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: OpenClaw v2026.8.1; Hermes Agent v2026.8.31 / IBM's Granite 4.2 8B lands on OpenRouter with 131K context / A Voice-Agent Latency Benchmark That Labels Its Own Numbers
- 02:00 — Agent Stack Release Readout: OpenClaw v2026.8.1; Hermes Agent v2026.8.31
- 03:19 — IBM's Granite 4.2 8B lands on OpenRouter with 131K context
- 05:00 — A Voice-Agent Latency Benchmark That Labels Its Own Numbers
- 06:29 — Meta's Muse Code exits beta with SDK for custom agents
- 07:54 — OpenClaw 2.0 Lands With Faster Setup and a Clearer Security Story
- 08:57 — Lightricks' LTX-2.5 Trending as a Multi-Modal Video Workhorse
- 10:07 — Anthropic's MHS Standard Lets AI Agents Operate Lab Hardware Safely
- 11:43 — An NVIDIA Earth2Studio Tutorial Turns Weather Models Into Wind-Power Forecasts
- 13:29 — OpenAI backs California bill on teen AI safeguards
- 14:52 — Research digest: Self-Improving AI Fails at the Most Human Step: Knowing What to Learn
- 15:53 — NEEDLE Benchmark Rebuilds Web Search Queries Every Hour to Block Cheating
- 17:19 — Google's EnvHarness Turns Static Agent Benchmarks Into Self-Improving Training Worlds
- 19:02 — Research digest: PaperGym Teaches AI to Plan Research by Reading Real Papers
- 20:02 — NVIDIA's Jetson Orin Nano 2 Packs New Silicon, Doubles Speed

---

## Primary Links

- OpenClaw v2026.8.1 release: https://github.com/openclaw/openclaw/releases/tag/v2026.8.1
- Hermes Agent v2026.8.31 release: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.31
- IBM: Granite 4.2 8B model page: https://openrouter.ai/models/ibm-granite/granite-4.2-8b
- Lowest-Latency Inference APIs for Voice and Realtime Agents: A Time to: https://www.marktechpost.com/2026/08/30/lowest-latency-inference-apis-for-voice-and-realtime-agents-a-time-to-first-token-ttft-first-benchmark/
- not much happened today: https://news.smol.ai/issues/26-08-31-not-much/
- OpenClaw Releases OpenClaw 2.0: Guided Model Setup, 575 ms Control UI : https://www.marktechpost.com/2026/08/30/openclaw-releases-openclaw-2-0-guided-model-setup-575-ms-control-ui-startup-and-one-trust-boundary-per-gateway/
- deepseek-ai/DeepSeek-V4-Flash-Vision-Exp trending on Hugging Face: https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp
- Lightricks/LTX-2.5 trending on Hugging Face: https://huggingface.co/Lightricks/LTX-2.5
- Anthropic Opens a Research Preview of the Model Hardware Standard (MHS: https://www.marktechpost.com/2026/08/29/anthropic-opens-a-research-preview-of-the-model-hardware-standard-mhs-a-shared-specification-for-ai-agents-to-safely-operate-physical-devices/
- Building Custom Batched Ensemble Weather Forecasting with NVIDIA Earth: https://www.marktechpost.com/2026/08/29/building-custom-batched-ensemble-weather-forecasting-with-nvidia-earth2studio/
- OpenAI supports California’s bill to advance youth AI safety: https://openai.com/index/supporting-california-bill-advance-ai-youth-safety
- Aspire: Can Models Self-Evolve from Vague Goals?: https://arxiv.org/abs/2608.31111
- Keenable AI Open-Sources NEEDLE: A Live Search Benchmark That Rebuilds: https://www.marktechpost.com/2026/08/31/keenable-ai-open-sources-needle-a-live-search-benchmark-that-rebuilds-its-query-set-every-hour/
- Google AI Introduces EnvHarness: A Programmable Layer That Turns Stati: https://www.marktechpost.com/2026/08/30/google-ai-introduces-envharness-a-programmable-layer-that-turns-static-agent-environments-into-adaptive-training-worlds/
- PaperGym: Rubric-Centered Evolution for Research-Plan Generation: https://arxiv.org/abs/2608.31119
- Polimill builds Japan's next-generation public AI infrastructure: https://openai.com/index/polimill
- NVIDIA Announces Jetson Orin Nano 2: Entry-Level Edge Board Gets New A: https://www.servethehome.com/nvidia-announces-jetson-orin-nano-2-entry-level-edge-board-gets-new-ampere-silicon/
- HKUDS/nanobot repo: https://github.com/HKUDS/nanobot
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- PrefectHQ/fastmcp repo: https://github.com/PrefectHQ/fastmcp
- GitHub Copilot in VS Code, August 2026 releases: https://github.blog/changelog/2026-08-31-github-copilot-in-vs-code-august-2026-releases
- Understanding ChatGPT Work: https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/
- Qwen/Qwen3.8-Flash-Next: https://huggingface.co/Qwen/Qwen3.8-Flash-Next

---

## Release Coverage Check

- **OpenClaw** — Latest stable verified: `v2026.8.1`, published 2026-08-31T03:30:51Z. Recent episode version tags detected: `v2026.7.2-beta.5`, `v2026.7.2-beta.7`, `v2026.8.1-beta.2`, `v2026.8.1-beta.3`. Selected missing version(s): `v2026.8.1`.
- **Hermes Agent** — Latest stable verified: `v2026.8.31`, published 2026-08-31T19:29:49Z. Recent episode version tags detected: `v2026.8.18`, `v2026.8.19`, `v2026.8.27`, `v2026.8.3`. Selected missing version(s): `v2026.8.31`.
- **OpenAI Codex** — Latest stable verified: `rust-v0.152.0`, published 2026-09-01T01:58:32Z. Recent episode version tags detected: `rust-v0.147.0`, `rust-v0.148.0`, `rust-v0.149.0`, `rust-v0.150.1`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.236`, published 2026-08-19T18:45:14.539Z. Recent episode version tags detected: `2.1.231`, `2.1.236`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-09-01). Recent episode version tags detected: none on record.

---

## Harness Version Reference

- **OpenClaw** — `v2026.8.1` (stable) / `v2026.9.1-beta.1` (prerelease)
- **Hermes Agent** — `v2026.8.31`
- **OpenAI Codex** — `rust-v0.152.0`
- **Claude Code CLI** — `2.1.236`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)
