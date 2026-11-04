# AgentStack Daily EP126 — Gemini 4 Carbon, 100M Voice Calls, and Local AI Hardware

**Title:** Gemini 4 Carbon Targets Long-Running Engineering and Cyber Defense

**Tagline:** Gemini 4 Carbon targets long-running engineering and cyber defense work, while OpenAI shares model results on three scientific problems. Retell’s OpenAI-powered voice agents reach 100 million monthly calls, and Anthropic separates a model from an agent’s actions. Local AI gets two hardware pushes: ASRock’s Radeon AI Pro R9700 for workstation inference and NVIDIA’s 4GB Bolt for local agent stacks. Research on group-memory distortion and EnvSched training runs addresses evidence quality and useful agent training.

**Feed description:** Gemini 4 Carbon leads the agent and model news, alongside OpenAI’s results on three scientific problems and Retell’s milestone of 100 million monthly calls for its OpenAI-powered voice agents. Anthropic’s model-action separation, ASRock’s Radeon AI Pro R9700, NVIDIA’s 4GB Bolt, and Legora’s legal-contract agents bring fresh tools to the conversation. Research digests cover group memory, EnvSched training runs, Greptile, and CodeRabbit security review.

---

## Story Slate

1. **Gemini 4 Carbon targets long-running engineering and cyber defense**
Google announced Gemini 4 Carbon as its strongest model, focused on sustained software-engineering workflows and the full cybersecurity defense cycle. Google reports that Carbon found vulnerabilities, validated exploitable risks, and produced working fixes on three external benchmarks. It can also run for days while pursuing complex multi-step engineering tasks. Carbon is entering a limited preview with cyber defenders and trusted partners rather than opening immediately to developers, businesses, and consumers.
Technical depth angle: Carbon’s useful mechanism is sustained agentic execution: AI that keeps working across days, persists through dead ends, and tackles multi-step tasks such as tracing subtle bugs across large codebases and low-level systems. Google says this allows Carbon to move beyond isolated code generation toward end-to-end engineering and cyber-defense work.
Actionability angle: Teams can plan for Carbon as a future candidate for long-running software-engineering and cyber-defense workflows, but practical evaluation remains limited to the initial defender cohort and trusted partners. For defenders, the relevant question is whether its vulnerability-finding, exploit-validation, and patch-generation results hold up on their own systems before broader access arrives.
Listener hook: Carbon is the rare AI release aimed directly at multi-day engineering work and the entire vulnerability-to-patch cycle.

2. **OpenAI Shares Model Results on Three Scientific Problems**
OpenAI has published model results connected to the Kakeya conjecture, the Exponential Time Hypothesis, and quantum chromodynamics. The announcement shares results spanning mathematics, computer science, and physics, along with a path for researchers to verify and build on the work. The useful distinction is that the scientific output is presented as material for academic scrutiny, allowing researchers to examine the results and develop them further.
Technical depth angle: OpenAI reports model results on three named research problems, then points academic researchers toward verifying and building on them. The practical contribution is the availability of model-produced scientific work that can enter a verification loop and support follow-on research.
Actionability angle: For research teams, these results provide concrete material to examine and extend across mathematics, computer science, and physics. For scientific-AI teams, the workflow to evaluate is whether model outputs can move directly into domain researchers’ verification and follow-on work.
Listener hook: A model’s scientific output becomes useful when researchers can challenge it and extend it.

3. **Retell’s OpenAI-powered voice agents reach 100M monthly calls**
Retell is using OpenAI models to power voice agents that handle 100 million calls each month, according to OpenAI’s October 27 case study. GPT-6 Astra topped Retell’s voice-agent benchmark, while Codex helped the company reach a $1.6 million annual revenue run rate per employee. The deployment connects model performance with a large operating workload and a measurable business result.
Technical depth angle: Retell’s own benchmark placed GPT-6 Astra at the top. The deployment handles 100 million calls per month, and the case study reports that Codex helped Retell reach a $1.6 million annual revenue run rate per employee. Together, those figures provide concrete evidence of both model performance and commercial scale.
Actionability angle: For builders, Retell’s deployment is a concrete reference point for OpenAI-powered voice agents operating at high call volumes. Call volume and revenue per employee are the two metrics to follow as the deployment develops.
Listener hook: A voice-agent operation is handling 100 million calls a month while posting $1.6 million in annual revenue run rate per employee.

4. **Anthropic separates the model from the agent’s actions**
Anthropic engineers Katelyn Lesse and Angela Jiang detailed how the Claude Platform team launched Opus 5.5 and operates managed agents by separating the model’s “brain” from the agent’s “hands.” Their design decouples reasoning, the execution harness, and the sandbox, with isolation, credential protection, and network controls around actions. The conversation also covers scaling APIs, keeping long-running agents moving across context windows, and differentiating training incidents from production safeguards.
Technical depth angle: Anthropic’s useful mechanism is a three-way separation: the model supplies reasoning, the harness coordinates the agent, and the sandbox contains its actions. The conversation also names isolation, credential protection, and network controls as containment mechanisms, while long-running harnesses preserve progress across context windows.
Actionability angle: This gives builders a clearer deployment pattern: separate the reasoning model from the system that executes tools, then constrain credentials and network access around that execution layer. Long-running agent design must also account for preserving progress across context windows, rather than treating a larger prompt as the only solution.
Listener hook: The useful takeaway is architectural: the model that decides and the system that acts can be built, secured, and scaled separately.

5. **ASRock’s Radeon AI Pro R9700 targets local workstation inference**
ASRock’s Creator Radeon AI Pro R9700 gives workstation builders a compact AMD option for local AI inference: 32GB GDDR6, 640 GB/s memory bandwidth, and RDNA 4 support for FP8 matrix math. The dual-slot blower is designed for multi-card ATX workstations, while Linux soft ECC can add reliability when manually enabled. ASRock built the card around AMD’s Navi 48 processor, which combines 64 compute units with 128 AI accelerator cores.
Technical depth angle: FP8 support is the key mechanism for fitting useful AI workloads into 32GB of memory. The card reaches a peak of 382.7 TFLOPS for dense FP8 matrix math, while FP6 and FP4 weights are processed at FP8. That makes a roughly 30B-parameter model possible on one card. Matrix operations use WMMA on the same compute units as vector math, rather than separate matrix cores.
Actionability angle: For teams building local inference, the R9700 is most relevant when a model needs substantial memory but the system must remain a standard ATX workstation. Its 32GB ceiling makes a roughly 30B-parameter model plausible with lower-precision weights, while Linux-only soft ECC and support for up to four cards suit reliability-conscious, multi-GPU deployments.
Listener hook: This is a 300-watt workstation card built to make substantial AI models fit into a local desktop rather than a server rack.

6. **NVIDIA’s 4GB Bolt model targets local agent stacks**
NVIDIA has published NVIDIA-Nemotron-3.5-Bolt-E4B-4GB, a quantized text model designed for local voice assistants, interactive personas, and embedded interfaces. NVIDIA describes it as an 8B-parameter model with 4B effective parameters, Q4_K_M precision, and up to 64K tokens for input and output. It adds controls for reasoning, conversational responses, and tool calling, including asynchronous tool workflows. The model is available for commercial or non-commercial use, with llama.cpp serving examples and a companion DFlash drafter for speculative decoding.
Technical depth angle: The useful mechanism is a compact, quantized model paired with runtime controls: chat-template settings can enable or disable thinking, set a thinking budget, and toggle a concise conversational mode. It supports function-style tool calls and a documented pending-result pattern for asynchronous tools. NVIDIA also provides a llama.cpp server path and a companion DFlash drafter.
Actionability angle: This makes the model a candidate for local assistants and agent stacks where memory use, tool interaction, and response latency matter more than frontier-scale capacity. Builders can pair it with an OpenAI-compatible client or the supplied llama.cpp server setup, while treating reasoning-budget limits and task-specific evaluation as deployment requirements.
Listener hook: A compact NVIDIA model is giving local agents a more practical path to tool use, voice interaction, and controllable reasoning.

7. **US Investments Add Chip Capacity and an Autonomous Weapons Test Range**
The White House detailed major US industrial commitments aimed at rebuilding domestic production. North Carolina will receive up to $1.5 billion to expand semiconductor production, alongside Sibelco’s expansion of high-purity quartz and related materials essential to semiconductors. In Montana, the Department of War is establishing a testing range for advanced technologies, including autonomous weapons and electronic warfare. These projects could strengthen the physical supply chain for AI hardware while creating a dedicated venue for testing autonomous systems.
Technical depth angle: The semiconductor commitment includes up to $1.5 billion for expanded chip production, while Sibelco is increasing output of high-purity quartz and related materials in Mitchell County. The Montana range will support testing of autonomous weapons, space and electronic warfare, supersonic and hypersonic technologies. Together, the projects address both upstream materials and a specialized environment for evaluating advanced systems.
Actionability angle: Teams planning AI hardware deployments can factor in the possibility of greater domestic semiconductor and materials capacity as these investments take effect. Builders working on autonomous systems may also have a new specialized test range to consider. The key issue is how quickly the committed funding becomes staffed, operating facilities.
Listener hook: AI’s physical infrastructure is now receiving industrial-scale investment, from semiconductor materials to testing grounds for autonomous systems.

8. **Research digest: Group memory can distort the evidence it preserves**
Compressing a language model group’s discussion into a short memory can make the final decision worse, even when the team had useful evidence. Two intuitive rules failed: keeping the rarest claims sometimes captured the useful facts, but keeping claims relevant to the decision criteria also pulled in plausible decoys because they were on topic. The deeper problem was social proof—the final model gave extra weight to facts attributed to many agents. Removing those attribution tags, or randomly reassigning them while keeping the discussion order fixed, improved accuracy. The research also found that a complete transcript could perform worse than taking no notes at all. This matters for any workflow that asks one model to distill another model group’s reasoning: a concise summary may preserve facts while distorting their importance. A concrete consequence is to evaluate memory systems on the balance of evidence they retain, rather than assuming that rarity or topical relevance is enough.
Technical depth angle: The central mechanism is evidence balance. Rarity and relevance do not reliably identify which claims should survive into a final decision memory, especially when distractors stay on topic. The final model also treats attribution as social proof, giving claims more weight when many agents are associated with them. Accuracy improves when that attribution is removed or randomized, so preserving evidence is not enough; preserving its relative significance is also essential.
Actionability angle: This means memory summaries for multi-agent decisions need to preserve which evidence is decisive, not merely which claims are rare or topically relevant. For a panel-to-one-model workflow, test the retained evidence mix and sensitivity to agent attribution before trusting the summary.
Listener hook: If you use a model to compress expert or agent discussion, a shorter summary may not be a safer decision input.

9. **Anthropic trained Claude on illegally obtained Stanford professors' books**
Anthropic illegally trained Claude with Stanford professors’ books Anthropic illegally trained Claude with Stanford professors’ books Anthropic illegally trained Claude on books from Stanford professors (Photo: JACK BERNARDO/The Stanford Daily) Published Oct. 27, 2026, 2:46 a.m., last updated Oct. 27, 2026, 3:19 a.m. AI giant Anthropic illegally scraped and pirated the work of over 10 Stanford professors to train its Claude models, a federal judge ruled in a May 2026 lawsuit. Anthropic previously trained Claude on illegally obtained texts from professors Tobias Wolff, Abraham Verghese, Chang-Rae Lee, Daniel Mason, Hayagreeva Rao and Myra Strober. In Bartz v.
Technical depth angle: The mechanism is a legal or policy boundary, not an API change. The sourced facts define what was proposed, decided, or stated without turning that into universal law.
Actionability angle: Builders should track the concrete rule, ruling, or access change and avoid changing a product based only on a headline.
Listener hook: The practical consequence depends on what the policy actually changes, not the loudest interpretation.

10. **Research digest: EnvSched Targets More Useful Agent Training Runs**
EnvSched, a new online scheduler for training language agents, focuses limited rollout budgets on tasks that are likely to reveal meaningful differences in rewards while also covering environments that have received less attention. It learns from past training runs and considers the relationships among tasks and their environments, including shared tools, states, and verification systems. The goal is to produce batches that contain more useful learning signals and less repeated work.
Technical depth angle: The key finding is that scheduling training work at the environment level can make a fixed rollout budget more useful. EnvSched favors tasks with predicted reward variation and environments that have been underexplored. It also uses environment quotas and a similarity penalty to prevent batches from concentrating too heavily on the same kinds of work.
Actionability angle: For teams training agents across multiple tool-driven environments, scheduling is another lever for improving data efficiency. Teams can measure not only which tasks yield successful runs, but also which combinations of tasks and environments provide informative differences and broader coverage.
Listener hook: This matters because training agents can waste much of its budget repeating nearly identical experiences.

11. **Greptile uses GPT-6 Astra to test software workflows**
Greptile is extending bug detection beyond code review by using GPT-6 Astra to test user workflows. Its Daybreak capability is used to strengthen security, while Codex helps reduce rework. Together, these tools target different stages of software quality: exercising how users interact with an application, checking for security weaknesses, and helping address the work that otherwise has to be repeated.
Technical depth angle: The useful mechanism is broader application testing, not just inspection of proposed code changes. Greptile uses GPT-6 Astra to test user workflows, Daybreak to strengthen security, and Codex to reduce rework. In practical terms, the system checks whether an application works for users and addresses problems that might otherwise surface after code review.
Actionability angle: This makes Greptile more relevant to teams that want automated checks to cover workflow behavior and security, not only code-level suggestions. The next thing to watch is how much rework Codex actually prevents as these capabilities are used across real projects.
Listener hook: Greptile is moving from finding issues in code to testing what happens when people actually use the software.

12. **CodeRabbit uses GPT-6.1 Sol for codebase security review**
CodeRabbit is using GPT-6.1 Sol to investigate security risks across complex codebases. Its security agent surfaces findings and proposed fixes, giving developers a way to review both potential vulnerabilities and possible remediations. The OpenAI announcement presents this as a practical application of the model inside a code-security workflow, rather than as a standalone security tool.
Technical depth angle: The useful mechanism is an agent that examines a codebase for security risks, then presents findings and proposed fixes for developer review. That gives teams a structured path from investigation to remediation while keeping a developer in the decision-making loop.
Actionability angle: Builders can use this pattern for security-focused coding workflows: have an agent investigate risks across a codebase, attach proposed fixes to its findings, and let developers evaluate the recommendations. Teams should judge the approach by the quality of the findings and fixes during their own review process.
Listener hook: This is a concrete example of an AI security agent helping with the work of understanding and fixing risks in real codebases.

13. **Hermit Teaches AI Agents Without Replacing Their Core**
Infini-AI-Lab released Hermit, an Apache-2.0 open-source framework that adds a trainable layer around an existing AI agent. The adapter develops instructions, skills, memory, and tools from feedback on completed tasks while leaving the agent’s underlying model and harness unchanged. This gives builders a way to improve an agent’s behavior without replacing its model or rebuilding its agent environment.
Technical depth angle: Hermit’s useful mechanism is an external adapter layer: it learns instructions, skills, memory, and tool use from task feedback. The underlying model and harness stay unchanged, so improvements happen around the agent rather than inside its core model or execution framework.
Actionability angle: This means builders can focus on teaching an existing agent through task feedback rather than changing its model or harness. That makes it worth testing Hermit when an agent already works but needs better instructions, retained knowledge, or tool behavior.
Listener hook: Hermit offers a practical route to adapting AI agents without tearing down the systems they already use.

14. **Legora brings agents into legal contract analysis**
Legora is building what it calls an agentic operating system for legal work, according to an OpenAI profile. The company uses OpenAI models, ChatGPT, and Codex to accelerate legal workflows and expand contract analysis. Legora’s goal is to handle more of this work while freeing lawyers to focus on higher-value tasks, making legal services a concrete new setting for AI-assisted professional work.
Technical depth angle: Legora combines OpenAI models with ChatGPT and Codex in legal workflows. The practical emphasis is expanding contract analysis and accelerating legal work so lawyers can devote more time to higher-value tasks.
Actionability angle: Legora’s approach makes legal workflow automation and larger-scale contract analysis the relevant areas for teams to evaluate. The key question is how effectively those capabilities can expand routine legal work while shifting lawyer time toward higher-value judgment.
Listener hook: This is a concrete example of AI agents moving into a high-stakes professional workflow rather than remaining a general-purpose assistant.

---

## Editorial Mix Check

- flagship_products: 7
- builder_projects: 10
- local_ai: 2
- hardware_compute: 3
- policy_regulation: 4
- research: 2

---

## Model Discovery Check

- **Gemini 4** — Source checked October 29, 2026. Primary source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/. Availability: Carbon is initially available to a subset of cyber defenders, with access gradually expanding to trusted partners through the Fairwind Program.. params_active: n/a; params_total: n/a; context: n/a; modality: see primary source. Capabilities: Google says Carbon is built for sustained agentic workflows and can run for days while pursuing complex, multi-step engineering tasks. Evidence: publisher_report. Decision: Selected — covered in the numbered slate from a non-OpenRouter source.

- **NVIDIA-Nemotron-3.5-Bolt-E4B-4GB** — Source checked October 29, 2026. Primary source: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB. Availability: The model card says the model is ready for commercial or non-commercial use and provides download and llama.cpp serving commands.. params_active: n/a; params_total: n/a; context: n/a; modality: see primary source. Capabilities: The model is an 8B-parameter text model with 4B effective parameters, Q4_K_M precision, up to 64K-token input and output lengths, reasoning controls, conversational mode, and tool calling. Evidence: publisher_report. Decision: Selected — covered in the numbered slate from a non-OpenRouter source.

---

## Local LLM Spotlight

- **deepseek-ai/DeepSeek-V4.1-Flash-1017** — https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017 — Trending open model on Hugging Face; task image-text-to-text; 3668 likes and 116770 downloads. Tags: transformers, safetensors, deepseek_v41, text-generation, image-text-to-text, license:mit, eval-results, endpoints_compatible, 8-bit, fp8.
  Try now: Read the linked model card before downloading, and choose a runtime or device only after it confirms the license, weight format, context window, benchmarks, and hardware requirements.

---

## GitHub Project Radar

- **morluto/rea** — https://github.com/morluto/rea — REA is an agent-based reverse-engineering project for analyzing behavior from application interfaces down to native binaries. It supports investigations that combine iterative agent reasoning with lower-level program inspection. `stars: 404,923`; `stars_delta_30d: n/a — first tracked appearance`; `latest_release: rea-agents-6.8.0 (2026-10-25)`.
  Why this is on the radar now: rea-agents-6.8.0 shipped on 2026-10-25 and the repository was updated on 2026-10-29.
  Stack improvement angle: REA could give OpenClaw, Codex, Claude Code, or Hermes agents a structured workflow for tracing application behavior, validating hypotheses, and documenting findings across interface and binary layers.
  Try now: Install REA, select a small sample application, and have an agent map its behavior before attempting binary-level analysis.

- **HKUDS/nanobot** — https://github.com/HKUDS/nanobot — Nanobot is an ultra-lightweight, open-source, self-hosted personal AI agent framework written in Python. It includes a WebUI, tools, memory, MCP support, multi-agent workflows, automation, and chat integrations. `stars: 49,612`; `stars_delta_30d: +1,051 (+2.2%) since 2026-09-25`; `latest_release: v0.4.0 (2026-10-28)`.
  Why this is on the radar now: v0.4.0 shipped on 2026-10-28 and the repository was updated on 2026-10-29.
  Stack improvement angle: Nanobot could extend an agent stack with a self-hosted Python layer for persistent memory, MCP-connected tools, multi-agent orchestration, and automated chat workflows.
  Try now: Deploy a minimal Nanobot instance with one tool and one MCP server, then test a short tool-using workflow through its WebUI.

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — Codebase Memory MCP provides local code intelligence by connecting code, documentation, and infrastructure in a persistent graph. Its CBM Lens, MCP tools, agent integrations, and change-aware test selection help developers navigate and assess codebase changes. `stars: 47,761`; `stars_delta_30d: +2,895 (+6.5%) since 2026-09-25`; `latest_release: v0.12.1 (2026-10-16)`.
  Why this is on the radar now: v0.12.1 shipped on 2026-10-16 and the repository was updated on 2026-10-29.
  Stack improvement angle: Codebase Memory MCP could give OpenClaw, Codex, Claude Code, or Hermes agents a persistent, locally queryable graph for code exploration and targeted test selection.
  Try now: Connect Codebase Memory MCP to a small repository and ask an agent to identify code, documentation, and infrastructure relationships affected by one change.

---

## Extra Research Candidates

- **OpenAI and ServiceNow expand partnership across enterprise workflows** — https://openai.com/index/openai-servicenow-partnership-expansion — OpenAI and ServiceNow expand their partnership to bring OpenAI models and agents into ServiceNow and ServiceNow workflows into ChatGPT and Codex. Technical depth angle: The partnership expansion integrates OpenAI models and agents with ServiceNow workflows while connecting ServiceNow workflows to ChatGPT and Codex.

- **How Check Point accelerates vulnerability research with Daybreak** — https://openai.com/index/check-point-daybreak — With OpenAI Daybreak, Check Point speeds up the research behind new security protections, enabling its analysts to turn vulnerability intelligence into customer defenses faster. Technical depth angle: OpenAI Daybreak accelerates Check Point’s vulnerability research process so analysts can convert vulnerability intelligence into customer security protections more quickly.

- **Working with academic communities to build scientific understanding** — https://openai.com/index/building-scientific-understanding-with-academic-communities — OpenAI shares model results on the Kakeya conjecture, Exponential Time Hypothesis, and quantum chromodynamics—and how researchers can verify and build on them. Technical depth angle: The research shares model results for the Kakeya conjecture, Exponential Time Hypothesis, and quantum chromodynamics to support verification and further scientific work.

---

## Show Notes

```md
Episode 126 — October 29, 2026

[00:00] Episode hook

Google announced Gemini 4 Carbon as its strongest model, built for sustained software-engineering workflows and the full cybersecurity defense cycle, and said Carbon found vulnerabilities. OpenAI published model results tied to the Kakeya conjecture, the Exponential Time Hypothesis, and quantum chromodynamics, extending its work across mathematics and physics. Retell’s OpenAI-powered voice agents now handle 100 million calls each month, according to an October 27 OpenAI case study, with GPT-6 Astra topping the company’s voice-agent benchmark. Anthropic engineers Katelyn Lesse and Angela Jiang explained how the Claude Platform team launched Opus 5.5 and operates managed agents by separating the model’s decision-making from its external actions. Hardware developers also received new local-AI options: ASRock’s compact Radeon AI Pro R9700 workstation card pairs 32GB GDDR6 with 640 GB/s bandwidth and RDNA 4 FP8 support, while NVIDIA published Nemotron-3.5-Bolt-E4B-4GB, a 4GB quantized 8B-parameter model designed for local voice assistants, interactive personas, and embedded interfaces.

[02:00] Gemini 4 Carbon targets long-running engineering and cyber defense

Google announced Gemini 4 Carbon as its next frontier model. Google says Carbon can run for days, persist through dead ends, root-cause subtle bugs across large codebases, and produce fixes. The cyber results cover three stages: finding vulnerabilities, checking whether they are exploitable, and patching the underlying cause. Google reports that Carbon scored 88.2% on SEC-bench Pro for vulnerability discovery, 54.8% on ExploitGym for exploitation, and 71.0% on Collinear’s CWE-bench for producing code fixes. The publisher reports that on Google’s internal benchmarks, Carbon more than doubled Argon’s success rate for generating secure code. Carbon is initially available to a subset of cyber defenders, with access gradually expanding to trusted partners through the Fairwind Program. Developers, businesses, and consumers are slated to receive access later. Its introductory price is set at $2 per million input tokens and $10 per million output tokens, with cached inputs discounted by 95%; afterward, the rates will be $4 and $20. The next milestone to watch is how the initial defenders use Carbon and whether broader access follows. Google says Carbon is built for sustained agentic workflows and can run for days while pursuing complex, multi-step engineering tasks.

[02:32] OpenAI Shares Model Results on Three Scientific Problems

OpenAI has shared model results on the Kakeya conjecture, the Exponential Time Hypothesis, and quantum chromodynamics, along with an account of how academic researchers can verify the work and build on it.

The useful outcome is access to model-produced results across mathematics, computer science, and physics. Researchers can examine the work and develop further work from it, turning model output into material for scientific investigation rather than leaving it as the final product.

OpenAI is positioning academic communities as active participants in checking and advancing the results. The next test is whether those researchers can verify the work and turn it into further scientific progress.

[03:11] Retell’s OpenAI-powered voice agents reach 100M monthly calls

OpenAI published a case study on October 27 showing that Retell is using OpenAI models to power a voice-agent operation handling 100 million calls each month. Retell reports that GPT-6 Astra topped its voice-agent benchmark, while Codex helped the company reach a $1.6 million annual revenue run rate per employee.

The useful example is a production-scale voice-agent system rather than a small demonstration. GPT-6 Astra leads Retell’s benchmark, and the deployment processes enough monthly traffic to make 100 million calls a meaningful operating measure. The revenue-per-employee figure adds a business signal to the model-performance result.

For builders looking at voice agents, this is a concrete reference for the scale and results associated with an OpenAI-powered deployment. Call volume and revenue per employee are the two indicators to follow as Retell’s use of the models develops.

[04:02] Anthropic separates the model from the agent’s actions

Anthropic’s platform team has a concrete way to make agents more controllable: keep the model that reasons separate from the system that acts. In an October 27 Latent Space interview, Katelyn Lesse and Angela Jiang described launching Opus 5.5 and scaling the Claude Platform through managed agents whose brain, harness, and sandbox are decoupled. The execution layer is contained with isolation, credential protections, and network controls, while long-running harnesses are designed to maintain progress across context windows.

For builders, this supports an architecture for agents that can keep working without giving the reasoning model unrestricted control over tools or credentials. The conversation also separates training incidents from production safeguards and covers safety classifiers and model routing as part of operating the platform.

A key question for teams adopting this pattern is whether its containment and progress-preservation mechanisms remain dependable as agent workloads run longer.

[04:57] ASRock’s Radeon AI Pro R9700 targets local workstation inference

ASRock is bringing AMD’s RDNA 4 workstation platform to local AI builders with the Creator Radeon AI Pro R9700. The card pairs 32GB of GDDR6 memory with 640 GB/s of bandwidth and support for FP8 matrix math, a lower-precision format that can hold more model parameters within a fixed memory budget.

At the heart is AMD’s Navi 48 processor, with 64 compute units, 128 AI accelerator cores, and a 2.92GHz peak clock. ASRock rates dense FP8 matrix throughput at 382.7 TFLOPS, with twice that figure when using sparsity. FP6 and FP4 models are processed at FP8 rather than at their native formats. One practical example is a roughly 30B-parameter model running with some VRAM to spare.

The design emphasizes workstation use. It is a dual-slot blower measuring 271 by 111 by 39 millimeters, and up to four cards can be installed in a standard ATX system. Linux users can manually enable soft ECC for additional reliability. The card draws 300 watts, which the review describes as manageable for a blower-style design.

Memory capacity is the main constraint. The R9700 has 32GB, less than the previous-generation Radeon Pro W7900’s 48GB. The next question is how its RDNA 4 compute improvements translate into practical inference throughput and efficiency within that smaller memory budget.

[06:16] NVIDIA’s 4GB Bolt model targets local agent stacks

NVIDIA published NVIDIA-Nemotron-3.5-Bolt-E4B-4GB, a quantized text model aimed at local voice and device assistants, interactive personas, and embedded interfaces. NVIDIA says the model was further post-trained from Gemma-4-E4B-it and is designed for low-memory, low-time-to-first-token operation. The model is an 8B-parameter text model with 4B effective parameters, Q4_K_M precision, up to 64K-token input and output lengths, reasoning controls, conversational mode, and tool calling. Its controls include enabled or disabled thinking, a runtime thinking budget, and a conversational mode that produces more concise replies. It supports function-style tool calling, including a documented pattern for acknowledging a pending tool result and resuming the conversation when the result arrives. NVIDIA provides download and llama.cpp server instructions, along with a companion DFlash drafter for speculative decoding. NVIDIA’s own Q4_K_M evaluation table reports a 55.60 MultiChallenge score for this model versus 39.36 for Gemma4 E4B-it, and says the measurements were conducted under a consistent NVIDIA harness. The model card says the model is ready for commercial or non-commercial use and provides download and llama.cpp serving commands. The model card warns that restricted token allocations may truncate thought processes mid-sentence, so task-specific evaluation remains necessary. NVIDIA published the NVIDIA-Nemotron-3.5-Bolt-E4B-4GB as a generally available model on October 23, 2026. The publisher reports that in NVIDIA's Q4_K_M evaluations, Nemotron-3.5-Bolt-E4B-4GB scored 55.60 on MultiChallenge, compared with 39.36 for Gemma4 E4B-it.

[07:39] US Investments Add Chip Capacity and an Autonomous Weapons Test Range

The White House detailed a set of industrial investments with direct implications for chips, computing hardware, and autonomous systems. North Carolina will receive up to $1.5 billion to expand semiconductor production, while Sibelco is expanding production of high-purity quartz and related materials essential to semiconductors in Mitchell County.

The administration is also invoking the Defense Production Act to release $150 million for expanded US refining capacity, aimed at increasing domestic production of diesel and gasoline. In Montana, the Department of War is establishing a new range for testing advanced weapons and technologies, including autonomous weapons and space and electronic warfare capabilities.

For builders, the semiconductor investment is a concrete upstream signal: more planned capacity for chips and essential materials could support a larger domestic hardware base. The Montana range creates a dedicated venue for evaluating autonomous and electronic-warfare systems.

One thing to watch is how quickly the announced investments become operating facilities at the described scale.

[08:38] Research digest: Group memory can distort the evidence it preserves

A group of language models can lose the substance of its own discussion when one model compresses the exchange into a short memory. Two tempting rules fail in different ways. Selecting the rarest claims sometimes works, but on average it is no better than choosing at random. Selecting claims that seem relevant to the decision can be worse because plausible decoys are also on topic. The final decision maker adds another distortion: social proof, meaning it gives extra weight to a fact because many agents are credited with saying it. Removing or randomly reassigning those attributions, while leaving the order of the discussion unchanged, improves accuracy. The full transcript can also score below taking no notes at all, showing that compression is not automatically the problem; how evidence is retained and framed matters. For a workflow that turns a panel’s research into one recommendation, the practical consequence is to inspect the balance of supporting and distracting evidence in the resulting memory, rather than treating a concise summary as a neutral record.

[09:43] Anthropic trained Claude on illegally obtained Stanford professors' books

Anthropic illegally trained Claude with Stanford professors’ books Anthropic illegally trained Claude with Stanford professors’ books Anthropic illegally trained Claude on books from Stanford professors (Photo: JACK BERNARDO/The Stanford Daily) Published Oct. 27, 2026, 2:46 a.m., last updated Oct. 27, 2026, 3:19 a.m. AI giant Anthropic illegally scraped and pirated the work of over 10 Stanford professors to train its Claude models, a federal judge ruled in a May 2026 lawsuit. Anthropic previously trained Claude on illegally obtained texts from professors Tobias Wolff, Abraham Verghese, Chang-Rae Lee, Daniel Mason, Hayagreeva Rao and Myra Strober. In Bartz v. The mechanism is a legal or policy boundary, not an API change. The sourced facts define what was proposed, decided, or stated without turning that into universal law. Builders should track the concrete rule, ruling, or access change and avoid changing a product based only on a headline.

[10:37] Research digest: EnvSched Targets More Useful Agent Training Runs

Training a language agent can become expensive quickly because each training run, or rollout, may involve different tools, states, transitions, and checks for success. EnvSched is a research scheduler designed to make a limited set of those runs more useful.

The paper’s central finding is that scheduling tasks together with their environments can improve the information in each training batch. EnvSched learns from rollout history, favors tasks likely to reveal meaningful reward differences, and spreads work across environments and interaction patterns that have received less attention.

To do that, it organizes task-environment pairs in a graph. Connections capture either relationships within an environment, such as shared tools and verification structures, or broader similarities in execution and rewards. Historical rollout information is used to estimate how much variation each task is likely to produce. Environment quotas and a similarity penalty then limit repetition.

The practical consequence is straightforward: with a fixed training budget, an agent team can concentrate runs where they are most likely to distinguish good behavior from bad, rather than spending too much of the budget on redundant experiences.

[11:45] Greptile uses GPT-6 Astra to test software workflows

Greptile is expanding bug detection beyond code review with GPT-6 Astra. The company is using Astra to test user workflows, giving its review product a way to examine how an application behaves in use rather than focusing only on the code being proposed.

Greptile is also using Daybreak to strengthen security. That adds a security-focused dimension to the same workflow-oriented approach, aimed at helping teams identify weaknesses beyond the point where a developer or reviewer might notice them manually.

The announcement also highlights Codex’s role in reducing rework. By bringing code assistance into the process, Greptile is addressing work that may otherwise need to be repeated after issues are found.

The practical result is a broader quality-checking workflow: Astra tests user-facing behavior, Daybreak supports security, and Codex helps limit corrective work. For builders, the next signal to watch is the extent to which these capabilities reduce repeated debugging and rework in real applications.

[12:43] CodeRabbit uses GPT-6.1 Sol for codebase security review

CodeRabbit is using GPT-6.1 Sol to investigate security risks across complex codebases. Its security agent helps developers review findings and proposed fixes, connecting automated investigation with human evaluation of possible vulnerabilities and remediations.

The practical shift is that the model is being applied inside a codebase-security workflow. CodeRabbit can investigate risks and surface proposed fixes, while developers review the results before deciding what to change.

For builders, the pattern is clear: combine codebase-wide security investigation with proposed remediation, then keep the developer responsible for reviewing both. The evidence to watch is how consistently the agent’s findings and proposed fixes hold up in real security reviews.

[13:23] Hermit Teaches AI Agents Without Replacing Their Core

Infini-AI-Lab has released Hermit, an Apache-2.0 open-source harness adapter framework for AI agents. Its central idea is simple: instead of changing the model or the harness that runs the agent, Hermit trains an external layer from feedback on completed tasks.

That layer contains instructions, skills, memory, and tools. Builders can therefore improve how an agent behaves by teaching it through task feedback while keeping the underlying model and harness unchanged.

This separation matters for teams that already have an agent environment they do not want to replace. They can work on the agent’s instructions, retained knowledge, and tool behavior through the adapter rather than modifying the model itself.

The key point to watch is whether Hermit can keep improving that external layer from task feedback without requiring changes to the agent’s core model or harness.

[14:14] Legora brings agents into legal contract analysis

Legora is building an agentic operating system for legal work. In a profile published by OpenAI, the company says it uses OpenAI models, ChatGPT, and Codex to accelerate legal workflows and expand contract analysis.

The immediate impact is greater capacity for legal work, with contract analysis providing a concrete example of where AI can take on more volume. Legora’s stated goal is to free lawyers to focus on higher-value work rather than spend their time on routine analysis.

The next useful evidence is how far contract analysis expands in practice and how that changes the allocation of lawyers’ time. For builders, Legora demonstrates that models, conversational tools, and coding agents can be combined around a professional workflow rather than deployed as isolated features.
```

---

## Chapters

- 00:00 — Intro: Gemini 4 Carbon targets long-running engineering and cyber defense / OpenAI Shares Model Results on Three Scientific Problems / Retell’s OpenAI-powered voice agents reach 100M monthly calls
- 02:00 — Gemini 4 Carbon targets long-running engineering and cyber defense
- 02:32 — OpenAI Shares Model Results on Three Scientific Problems
- 03:11 — Retell’s OpenAI-powered voice agents reach 100M monthly calls
- 04:02 — Anthropic separates the model from the agent’s actions
- 04:57 — ASRock’s Radeon AI Pro R9700 targets local workstation inference
- 06:16 — NVIDIA’s 4GB Bolt model targets local agent stacks
- 07:39 — US Investments Add Chip Capacity and an Autonomous Weapons Test Range
- 08:38 — Research digest: Group memory can distort the evidence it preserves
- 09:43 — Anthropic trained Claude on illegally obtained Stanford professors' books
- 10:37 — Research digest: EnvSched Targets More Useful Agent Training Runs
- 11:45 — Greptile uses GPT-6 Astra to test software workflows
- 12:43 — CodeRabbit uses GPT-6.1 Sol for codebase security review
- 13:23 — Hermit Teaches AI Agents Without Replacing Their Core
- 14:14 — Legora brings agents into legal contract analysis

---

## Primary Links

- Gemini 4 Carbon: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/
- Three new discoveries in mathematics, computer science, and physics: https://openai.com/index/building-scientific-understanding-with-academic-communities/
- Retell uses OpenAI models to help power 100M monthly calls: https://openai.com/index/retell-ai
- How Anthropic ships the #1 LLM in the World safely: Separating the Bra: https://latent.space/p/how_anthropic_ships_the_1_llm_in_the_world_safely_separating_the_brain_from_the_hands/
- ASRock Creator Radeon AI Pro R9700 Review: Workstation Inference, AMD : https://www.servethehome.com/asrock-creator-radeon-ai-pro-r9700-review-workstation-inference-amd-style/
- nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB model repository on Hugging Fa: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB
- From Coast to Coast, President Trump Is Putting American Industry Back: https://www.whitehouse.gov/releases/2026/10/from-coast-to-coast-president-trump-is-putting-american-industry-back-on-the-map/
- Rare, Relevant, and Still Wrong: How Memory Fails LLM Group Decisions: https://arxiv.org/abs/2610.37624
- Anthropic trained Claude on illegally obtained Stanford professors' bo: https://stanforddaily.com/2026/10/27/professors-books-pirated-to-train-claude/
- EnvSched: Environment-Aware Scheduling for Rollout-Efficient Agent Rei: https://arxiv.org/abs/2610.37609
- Greptile takes bug detection beyond code review with GPT-6 Astra: https://openai.com/index/greptile-code-review-codex-astra
- GPT-6.1 Sol helps CodeRabbit strengthen security across complex codeba: https://openai.com/index/gpt-6-1-sol-coderabbit-code-security
- Infini-AI-Lab Releases Hermit, an Open-Source Harness Adapter Framewor: https://www.marktechpost.com/2026/10/29/infini-ai-lab-hermit-harness-adapter-framework/
- Legora is building the agentic operating system for legal work: https://openai.com/index/legora
- morluto/rea repo: https://github.com/morluto/rea
- HKUDS/nanobot repo: https://github.com/HKUDS/nanobot
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- OpenAI and ServiceNow expand partnership across enterprise workflows: https://openai.com/index/openai-servicenow-partnership-expansion
- How Check Point accelerates vulnerability research with Daybreak: https://openai.com/index/check-point-daybreak
- Working with academic communities to build scientific understanding: https://openai.com/index/building-scientific-understanding-with-academic-communities
- deepseek-ai/DeepSeek-V4.1-Flash-1017: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017

---

## Release Coverage Check

- **Hermes Agent** — Latest stable verified: `v0.22.5`, published 2026-10-23T05:28:45Z. Recent episode version tags detected: `v2026.9.14`, `v2026.9.21`, `v2026.9.24`, `v2026.9.7`. No new stable release this cycle.
- **OpenAI Codex** — Latest stable verified: `rust-v0.165.0`, published 2026-10-27T20:09:38Z. Recent episode version tags detected: `rust-v0.161.0`, `rust-v0.162.0`, `rust-v0.163.0`, `rust-v0.164.0`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.308`, published 2026-10-22T04:19:48.902Z. Recent episode version tags detected: `2.1.304`, `2.1.308`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-10-29). Recent episode version tags detected: `@google/antigravity`, `v2.0`.

---

## Harness Version Reference

- **Hermes Agent** — `v0.22.5`
- **OpenAI Codex** — `rust-v0.165.0`
- **Claude Code CLI** — `2.1.308`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)


---

## Featured Story Plan

- Story 1: **Gemini 4 Carbon targets long-running engineering and cyber defense** — prioritize its source-backed capability, comparison when documented, limitations, and practical consequence; no word quota.
- Story 6: **NVIDIA’s 4GB Bolt model targets local agent stacks** — prioritize its source-backed capability, comparison when documented, limitations, and practical consequence; no word quota.

---

## Research Evidence Contract

```json
{
  "policy_version": 1,
  "featured_stories": [
    6,
    1
  ],
  "records": [
    {
      "story": 1,
      "title": "Gemini 4 Carbon targets long-running engineering and cyber defense",
      "source_sha256": "ffaab79dfa44427599f9ac919948df43a16d4fe0c191e4dc55b7f057b268f7e6",
      "source_url": "https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/",
      "model_story": true,
      "model_review": {
        "release_status": "preview",
        "evidence_type": "publisher_report",
        "release_quote": "We’re continuing to gather feedback and iterate on guardrails before making Carbon available to developers, businesses, and consumers via our product surfaces as soon as possible.",
        "release_span": "S010",
        "change": {
          "status": "supported",
          "claim": "Google announced Gemini 4 Carbon as its next frontier model.",
          "quote": "SVP, Google DeepMind and Chief AI Architect, Google \nToday, we’re announcing the next frontier model: Gemini 4 Carbon, our strongest model with state-of-the-art cybersecurity and long horizon capabilities.",
          "source_span": [
            "S002"
          ],
          "quotes": [
            "SVP, Google DeepMind and Chief AI Architect, Google \nToday, we’re announcing the next frontier model: Gemini 4 Carbon, our strongest model with state-of-the-art cybersecurity and long horizon capabilities."
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "Google says Carbon is built for sustained agentic workflows and can run for days while pursuing complex, multi-step engineering tasks.",
          "quote": "Improving coding and reasoning for challenging, long-horizon tasks \nDesigned to take on much harder, long-horizon engineering problems, Carbon is built for sustained agentic workflows.\nInternally, our teams have seen Carbon run for days to persist through dead ends to tackle complex, multi-step engineering tasks like root-causing and patching subtle bugs across large codebases and low-level systems.",
          "source_span": [
            "S012",
            "S013"
          ],
          "quotes": [
            "Improving coding and reasoning for challenging, long-horizon tasks \nDesigned to take on much harder, long-horizon engineering problems, Carbon is built for sustained agentic workflows.",
            "Internally, our teams have seen Carbon run for days to persist through dead ends to tackle complex, multi-step engineering tasks like root-causing and patching subtle bugs across large codebases and low-level systems."
          ]
        },
        "comparison": {
          "status": "supported",
          "claim": "The publisher reports that on Google’s internal benchmarks, Carbon more than doubled Argon’s success rate for generating secure code.",
          "quote": "On internal benchmarks, Carbon achieves more than 2x uplift in success rate for generating secure code over Argon.",
          "source_span": [
            "S019"
          ],
          "quotes": [
            "On internal benchmarks, Carbon achieves more than 2x uplift in success rate for generating secure code over Argon."
          ]
        },
        "limitations": {
          "status": "unverified",
          "claim": "",
          "quote": "",
          "source_span": []
        },
        "access": {
          "status": "supported",
          "claim": "Carbon is initially available to a subset of cyber defenders, with access gradually expanding to trusted partners through the Fairwind Program.",
          "quote": "Starting this week, we will make Carbon available to a subset of cyber defenders and will gradually phase access to additional trusted partners through our Fairwind Program .\nWe’re continuing to gather feedback and iterate on guardrails before making Carbon available to developers, businesses, and consumers via our product surfaces as soon as possible.",
          "source_span": [
            "S009",
            "S010"
          ],
          "quotes": [
            "Starting this week, we will make Carbon available to a subset of cyber defenders and will gradually phase access to additional trusted partners through our Fairwind Program .",
            "We’re continuing to gather feedback and iterate on guardrails before making Carbon available to developers, businesses, and consumers via our product surfaces as soon as possible."
          ]
        }
      }
    },
    {
      "story": 2,
      "title": "OpenAI Shares Model Results on Three Scientific Problems",
      "source_sha256": "75b409385f4cc49e78c35bd7b95d2437cee7c7bb1be009df2278ae25906b0d1f",
      "source_url": "https://openai.com/index/building-scientific-understanding-with-academic-communities/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 3,
      "title": "Retell’s OpenAI-powered voice agents reach 100M monthly calls",
      "source_sha256": "5ac3ef2b3f66f7af154ebbb39d168c06f2e49fe7dc27473c12b330dc4c121868",
      "source_url": "https://openai.com/index/retell-ai",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 4,
      "title": "Anthropic separates the model from the agent’s actions",
      "source_sha256": "a3d01b51175357069a92414de88c5994c4bd8b1b087122abbdcc095953cdc8ce",
      "source_url": "https://latent.space/p/how_anthropic_ships_the_1_llm_in_the_world_safely_separating_the_brain_from_the_hands/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 5,
      "title": "ASRock’s Radeon AI Pro R9700 targets local workstation inference",
      "source_sha256": "6b3dc3d5ec436580cc7ba2592454b5231c190887bda848e542ae9d4c0b1e988c",
      "source_url": "https://www.servethehome.com/asrock-creator-radeon-ai-pro-r9700-review-workstation-inference-amd-style/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 6,
      "title": "NVIDIA’s 4GB Bolt model targets local agent stacks",
      "source_sha256": "80bd39081c033d56bf3e8a07ea5bae776fe036446ac80f4d6529c935718a43f3",
      "source_url": "https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB",
      "model_story": true,
      "model_review": {
        "release_status": "released",
        "evidence_type": "publisher_report",
        "release_quote": "Model Version(s)\nGA (10/23/2026)\nQuick Start Guide",
        "release_span": "S049",
        "change": {
          "status": "supported",
          "claim": "NVIDIA published the NVIDIA-Nemotron-3.5-Bolt-E4B-4GB as a generally available model on October 23, 2026.",
          "quote": "NVIDIA-Nemotron-3.5-Bolt-E4B-4GB is a small language model (SLM) further post-trained from Gemma-4-E4B-it by NVIDIA.\nRelease Date\nHugging Face 10/23/2026 via https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB\nBuild.NVIDIA.com 10/23/2026 via https://build.nvidia.com/nvidia/nemotron-3.5-bolt-e4b\nReference(s)\nNVIDIA Nemotron 3 model family on Hugging Face\nNVIDIA Nemotron 3.5 Bolt E4B 4GB Technical Report\nNVIDIA Nemotron 3.5 Bolt E4B 4GB Technical Blog\nModel Architecture\nArchitecture Type: Gemma 4\nNetwork Architecture: Gemma-4-E4B\nNumber of model parameters: 8B (4B effective parameters)\nModel Design\nModel Version(s)\nGA (10/23/2026)\nQuick Start Guide",
          "source_span": [
            "S002",
            "S034",
            "S049"
          ],
          "quotes": [
            "NVIDIA-Nemotron-3.5-Bolt-E4B-4GB is a small language model (SLM) further post-trained from Gemma-4-E4B-it by NVIDIA.",
            "Release Date\nHugging Face 10/23/2026 via https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB\nBuild.NVIDIA.com 10/23/2026 via https://build.nvidia.com/nvidia/nemotron-3.5-bolt-e4b\nReference(s)\nNVIDIA Nemotron 3 model family on Hugging Face\nNVIDIA Nemotron 3.5 Bolt E4B 4GB Technical Report\nNVIDIA Nemotron 3.5 Bolt E4B 4GB Technical Blog\nModel Architecture\nArchitecture Type: Gemma 4\nNetwork Architecture: Gemma-4-E4B\nNumber of model parameters: 8B (4B effective parameters)\nModel Design",
            "Model Version(s)\nGA (10/23/2026)\nQuick Start Guide"
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "The model is an 8B-parameter text model with 4B effective parameters, Q4_K_M precision, up to 64K-token input and output lengths, reasoning controls, conversational mode, and tool calling.",
          "quote": "| | |\n|:---|:---|\n| Total Parameters | 8B (4B effective) |\n| Architecture | Gemma-4-E4B |\n| Precision | Q4_K_M |\n| Context Length | Input: up to 64K tokens; output: up to 64K tokens |\n| Inputs / Outputs | Text / text |\n| Deployment | llama.cpp (recipe pending) |\n| Reasoning Mode | Chat-template controls (enable_thinking=True/False) and runtime thinking budget |\n| Conversational Mode | Chat-template controls (conversational_mode=True/False) |\n| Recommended Sampling | Temperature 1.0, top_p 0.95 in both thinking modes |\n| Best For | Local voice and device assistants, interactive personas, and embedded interfaces |\n| License | OpenMDW-1.1 |\nModel Overview\nBolt-E4B exposes reasoning control through chat-template kwargs: thinking enabled (the default), thinking disabled for direct answers, and a runtime thinking budget.\nBolt-E4B supports a conversational mode.\nConversational mode can be combined with thinking enabled and disabled mode, as well as tool-calling.",
          "source_span": [
            "S008",
            "S053",
            "S062",
            "S067"
          ],
          "quotes": [
            "| | |\n|:---|:---|\n| Total Parameters | 8B (4B effective) |\n| Architecture | Gemma-4-E4B |\n| Precision | Q4_K_M |\n| Context Length | Input: up to 64K tokens; output: up to 64K tokens |\n| Inputs / Outputs | Text / text |\n| Deployment | llama.cpp (recipe pending) |\n| Reasoning Mode | Chat-template controls (enable_thinking=True/False) and runtime thinking budget |\n| Conversational Mode | Chat-template controls (conversational_mode=True/False) |\n| Recommended Sampling | Temperature 1.0, top_p 0.95 in both thinking modes |\n| Best For | Local voice and device assistants, interactive personas, and embedded interfaces |\n| License | OpenMDW-1.1 |\nModel Overview",
            "Bolt-E4B exposes reasoning control through chat-template kwargs: thinking enabled (the default), thinking disabled for direct answers, and a runtime thinking budget.",
            "Bolt-E4B supports a conversational mode.",
            "Conversational mode can be combined with thinking enabled and disabled mode, as well as tool-calling."
          ]
        },
        "comparison": {
          "status": "supported",
          "claim": "The publisher reports that in NVIDIA's Q4_K_M evaluations, Nemotron-3.5-Bolt-E4B-4GB scored 55.60 on MultiChallenge, compared with 39.36 for Gemma4 E4B-it.",
          "quote": "| Benchmark | Nemotron-3.5\nBolt-E4B\nBF16 | Gemma4\nE4B-it\nBF16 | Qwen3.5\n4B\nBF16 | Nemotron-3\nNano-4B\nBF16 | Nemotron-3.5\nBolt-E4B-4GB\nQ4_K_M | Gemma4\nE4B-it\nQ4_K_M | Qwen3.5\n4B\nQ4_K_M | Nemotron-3\nNano-4B\nQ4_K_M |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n| MultiChallenge | 53.10 | 42.08 | 51.76 | 35.30 | 55.60 | 39.36 | 52.23 | 34.53 |\n| RoleBench | 67.05 | 49.95 | 53.66 | 12.02 | 71.21 | 60.51 | 52.35 | 10.86 |\n| RoleMRC | 80.63 | 74.62 | 65.81 | 47.00 | 79.12 | 75.24 | 62.61 | 45.84 |\n| EQ-Bench v3 | 39.40 | 41.17 | 32.92 | 19.31 | 38.15 | 39.77 | 32.07 | 19.45 |\n| Brevity Benchmark | 82.52 | 79.99 | 75.35 | 73.60 | 82.84 | 78.49 | 75.17 | 70.98 |\n| BFCL-v3 | 68.51 | 66.39 |\nNote:\nEvaluations are conducted in reasoning mode except for RoleBench, EQ-Bench v3, and RULER.\nAccuracy numbers are measured by NVIDIA under a consistent harness (NeMo Gym); they may differ from vendors' self-reported numbers.",
          "source_span": [
            "S024",
            "S028",
            "S031"
          ],
          "quotes": [
            "| Benchmark | Nemotron-3.5\nBolt-E4B\nBF16 | Gemma4\nE4B-it\nBF16 | Qwen3.5\n4B\nBF16 | Nemotron-3\nNano-4B\nBF16 | Nemotron-3.5\nBolt-E4B-4GB\nQ4_K_M | Gemma4\nE4B-it\nQ4_K_M | Qwen3.5\n4B\nQ4_K_M | Nemotron-3\nNano-4B\nQ4_K_M |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n| MultiChallenge | 53.10 | 42.08 | 51.76 | 35.30 | 55.60 | 39.36 | 52.23 | 34.53 |\n| RoleBench | 67.05 | 49.95 | 53.66 | 12.02 | 71.21 | 60.51 | 52.35 | 10.86 |\n| RoleMRC | 80.63 | 74.62 | 65.81 | 47.00 | 79.12 | 75.24 | 62.61 | 45.84 |\n| EQ-Bench v3 | 39.40 | 41.17 | 32.92 | 19.31 | 38.15 | 39.77 | 32.07 | 19.45 |\n| Brevity Benchmark | 82.52 | 79.99 | 75.35 | 73.60 | 82.84 | 78.49 | 75.17 | 70.98 |\n| BFCL-v3 | 68.51 | 66.39 |",
            "Note:\nEvaluations are conducted in reasoning mode except for RoleBench, EQ-Bench v3, and RULER.",
            "Accuracy numbers are measured by NVIDIA under a consistent harness (NeMo Gym); they may differ from vendors' self-reported numbers."
          ]
        },
        "limitations": {
          "status": "supported",
          "claim": "The model card warns that restricted token allocations may truncate thought processes mid-sentence, so task-specific evaluation remains necessary.",
          "quote": "Limits and Recommendations for Runtime Budget Control\nRestricted token allocations may truncate thought processes mid-sentence.\nWhile output clarity is typically maintained, task-specific output evaluation remains necessary.",
          "source_span": [
            "S071",
            "S072"
          ],
          "quotes": [
            "Limits and Recommendations for Runtime Budget Control\nRestricted token allocations may truncate thought processes mid-sentence.",
            "While output clarity is typically maintained, task-specific output evaluation remains necessary."
          ]
        },
        "access": {
          "status": "supported",
          "claim": "The model card says the model is ready for commercial or non-commercial use and provides download and llama.cpp serving commands.",
          "quote": "This model is ready for commercial or non‑commercial use.\nhf download \"$MODEL_REPO\" \"$MODEL_FILE\" \\\n  --local-dir \"$MODEL_DIR\"\ndocker run --rm --gpus all \\\n  -p 8000:8000 \\\n  -v \"$MODEL_DIR:/models:ro\" \\\n  ghcr.io/ggml-org/llama.cpp:server-cuda13-b11459 \\\n  -m \"/models/$MODEL_FILE\" \\\n  --alias nemotron-bolt \\\n  --host 0.0.0.0 \\\n  --port 8000 \\\n  -c 65536 \\\n  -ngl 999 \\\n  --jinja",
          "source_span": [
            "S007",
            "S015",
            "S017"
          ],
          "quotes": [
            "This model is ready for commercial or non‑commercial use.",
            "hf download \"$MODEL_REPO\" \"$MODEL_FILE\" \\\n  --local-dir \"$MODEL_DIR\"",
            "docker run --rm --gpus all \\\n  -p 8000:8000 \\\n  -v \"$MODEL_DIR:/models:ro\" \\\n  ghcr.io/ggml-org/llama.cpp:server-cuda13-b11459 \\\n  -m \"/models/$MODEL_FILE\" \\\n  --alias nemotron-bolt \\\n  --host 0.0.0.0 \\\n  --port 8000 \\\n  -c 65536 \\\n  -ngl 999 \\\n  --jinja"
          ]
        }
      }
    },
    {
      "story": 7,
      "title": "US Investments Add Chip Capacity and an Autonomous Weapons Test Range",
      "source_sha256": "27f9e15e7192e9525273519d298a07487396787521671e79059aa23725b6ab6f",
      "source_url": "https://www.whitehouse.gov/releases/2026/10/from-coast-to-coast-president-trump-is-putting-american-industry-back-on-the-map/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 8,
      "title": "Research digest: Group memory can distort the evidence it preserves",
      "source_sha256": "8c136eeee49f499a751b0268884c362f9ed15c216ffdcea1dfd9b35f408a8c0b",
      "source_url": "https://arxiv.org/abs/2610.37624",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 9,
      "title": "Anthropic trained Claude on illegally obtained Stanford professors' books",
      "source_sha256": "06c8b98a797b2a2466b76957d99ac5fcf06857cfaf16d365d2f546ba1d1397d1",
      "source_url": "https://stanforddaily.com/2026/10/27/professors-books-pirated-to-train-claude/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 10,
      "title": "Research digest: EnvSched Targets More Useful Agent Training Runs",
      "source_sha256": "2ce5247a42cb0c20b6e1b1b3c73e89d6c0fbeda87246f485072fc800a0186e47",
      "source_url": "https://arxiv.org/abs/2610.37609",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 11,
      "title": "Greptile uses GPT-6 Astra to test software workflows",
      "source_sha256": "12e660cef9961572c31b38b8ce3911cc0c72948d1624987ec89f585f9d14e286",
      "source_url": "https://openai.com/index/greptile-code-review-codex-astra",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 12,
      "title": "CodeRabbit uses GPT-6.1 Sol for codebase security review",
      "source_sha256": "1dc74029a868e30b2b4a31f465c22c7b61c4ac22b862da44c6ca2b76e75f98ee",
      "source_url": "https://openai.com/index/gpt-6-1-sol-coderabbit-code-security",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 13,
      "title": "Hermit Teaches AI Agents Without Replacing Their Core",
      "source_sha256": "cfc5f406439fd3a130255817e96b2c5fd5ee8c2d61dc019e8713bdb9ae07a291",
      "source_url": "https://www.marktechpost.com/2026/10/29/infini-ai-lab-hermit-harness-adapter-framework/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 14,
      "title": "Legora brings agents into legal contract analysis",
      "source_sha256": "9ee07b0efd8780e40bdad3a192d67850dffb1ec6cc760f147bfbcf0ac4508419",
      "source_url": "https://openai.com/index/legora",
      "model_story": false,
      "model_review": null
    }
  ]
}
```
