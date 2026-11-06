# AgentStack Daily EP127 — Astra weight edits and OpenAI’s 948-vulnerability kernel patch

**Title:** OpenAI Patches 948 Linux Kernel Vulnerabilities

**Tagline:** OpenAI found and patched 948 Linux kernel vulnerabilities, while Astra demonstrates a different approach by editing neural network weights directly. OpenAI also ships faster image generation, GIFs, and more precise editing. RicursiveAI’s Ripple-65B arrives on OpenRouter with open-weight agentic coding for local machines. ComfyUI adds texture and dubbing nodes, and Together Compiler re-optimizes inference as traffic shifts. Other developments include voter constraints on AI data centers, mixed-chip inference systems from SambaNova and Supermicro, and OpenAI’s new compute campuses tied to grid reliability.

**Feed description:** OpenAI’s discovery and patching of 948 Linux kernel vulnerabilities anchors today’s developer news, alongside Astra’s direct neural-network weight editing and faster image, GIF, and precision-editing updates. RicursiveAI’s Ripple-65B reaches OpenRouter for local agentic coding, while ComfyUI adds texture and dubbing nodes. We also track mixed-chip inference plans, data-center voting constraints, OpenAI compute-campus grid links, and inference re-optimization as traffic changes.

---

## Story Slate

1. **Agent Stack Release Readout: Hermes Agent v0.22.7, v0.22.6**
Hermes Agent v0.22.6 and v0.22.7 add substantial collaboration, scheduling, and control features across the CLI, webapp, Desktop, Docker, and Hermes Cloud. The releases bring a browser-accessible webapp, richer group chats, scheduled posts, and stronger controls over autonomous work. They also add per-skill write locks and a pre-inference hook that can block a turn. Nous Research published the two patch releases on November 2 and November 3, 2026.
Technical depth angle: The most useful mechanism is browser-based access to the gateway’s webapp, including Desktop plugins loaded in a browser tab. Around it, Hermes adds shared group-chat notes, room purposes, member-state views, pinned Kanban boards, and cron jobs that publish into those rooms. Per-skill locks can prevent autonomous writes, while a pre-inference hook can stop a turn before it reaches the model.
Actionability angle: Teams can now organize shared conversations, attach notes and boards, schedule messages into group chats, and open Hermes capabilities through a browser rather than only the Desktop interface. The added write locks and pre-inference blocking point also give builders clearer ways to constrain agents that handle shared or automated work.
Listener hook: A browser-based agent workspace and scheduled group-chat posts make Hermes more useful for collaborative, unattended workflows.

2. **RicursiveAI’s Ripple-65B arrives on OpenRouter**
OpenRouter lists Ripple-65B-Preview, a 65B-parameter model from RicursiveAI with native tool calling and a context length of 1,048,576 tokens. The registry lists prompt pricing at $0.0000002 per token, completion pricing at $0.0000006, and cache-read input pricing at $0.00000005. That combination gives builders a large-context text model available for tool-driven workflows, although the available evidence is a registry listing rather than a detailed performance report.
Technical depth angle: Ripple-65B-Preview is listed as a text-to-text model served in BF16, with native tool calling for invoking program functions directly. Its registered context length is 1,048,576 tokens, allowing it to process unusually large text inputs in a single context.
Actionability angle: This gives builders a candidate for long-context text workflows that require native tool calling. Treat the listed capacity and pricing as the concrete starting point, then validate the model’s behavior before committing an important workflow.
Listener hook: A million-token context and native tool calling make this one to evaluate for large, tool-driven text applications.

3. **Astra Edits Neural Network Weights Directly**
Astra, a frontier LLM used through natural language, can inspect and directly edit neural-network weights without writing a training loop or using gradient descent. In the team’s Qwen3.5-0.8B experiment, Astra found a weight issue associated with reasoning loops and edited 0.016% of the model’s weights. Under the same sampling settings, MATH-500 rose from 7.9% to 48.1%, while IFEval instruction-following performance tripled. The team calls this Weight-Space Programming: using an LLM’s reasoning to understand a network’s behavior and modify its parameters directly.
Technical depth angle: Instead of sending a model through a conventional optimizer, the LLM receives raw weights, reasons about what parts of the network compute, and edits selected values directly. In Qwen3.5-0.8B, the edit was tiny but changed both math accuracy and instruction following.
Actionability angle: For builders, this suggests a new debugging path: ask a capable LLM to inspect a model’s parameters, explain a failure, and propose a targeted edit before considering retraining. The important next test is whether the approach generalizes beyond the reported games, diffusion models, and Qwen case.
Listener hook: If Astra can repair a reasoning failure by changing a sliver of a model’s weights, AI debugging may no longer be only about retraining.

4. **OpenAI found and patched 948 Linux kernel vulnerabilities**
OpenAI built an autonomous pipeline that found, validated, and generated patches for 948 local privilege-escalation vulnerabilities in the Linux kernel. Local privilege escalation means a flaw that can let someone with limited access gain higher privileges on the same machine. The work gives kernel maintainers and security teams a substantial set of candidate fixes to review, rather than requiring every vulnerability to be located and patched one at a time.
Technical depth angle: The useful mechanism is an autonomous pipeline that handles the full path from discovery to candidate fixes: it finds local privilege-escalation flaws, validates them, and generates patches for the Linux kernel. That turns a large class of kernel vulnerabilities into a concrete review queue, although the patches are still candidates rather than confirmed parts of Linux.
Actionability angle: Kernel maintainers and security teams now have 948 generated patches they can examine for correctness, compatibility, and priority. What this matters is the scale: teams can direct scarce review time toward specific candidate fixes while watching whether they are accepted into Linux.
Listener hook: A thousand fewer paths to gaining administrator-level access is a very tangible result from an AI security pipeline.

5. **OpenAI Ships Faster Images, GIFs, and More Precise Editing**
OpenAI has released Images 2.6, bringing faster image generation, GIF creation, more precise editing, and new API controls. The update is available across ChatGPT, Codex, and the API, so people can use it both through interactive tools and within applications that need image-generation or editing capabilities.
Technical depth angle: The useful change is a combination of speed and broader creative output: Images 2.6 can generate images and GIFs, while its editing is more precise. It also adds API controls, giving developers additional ways to manage image-generation behavior in their applications.
Actionability angle: Builders can now add GIF creation and precise image editing to workflows that already use OpenAI’s image tools. The new API controls also create a path for integrating these capabilities more directly into image-oriented products.
Listener hook: You can make GIFs and edit images more precisely without moving to a separate tool.

6. **Ripple-65B Brings Open-Weight Agentic Coding to Local Machines**
Ricursive Intelligence released Ripple-65B Preview, an open-weight language model designed for agentic coding and efficient local use. The company reports a TerminalBench 2.1 score of 80.52, ahead of several larger U.S. open-weight models. Ripple supports context windows up to 1 million tokens and is available through Hugging Face, Together AI, GMI Cloud, and OpenRouter, with Fireworks scheduled to join later that day. Ricursive also says it developed and trained the model for $32 million in total research and development.
Technical depth angle: Ripple uses a dense, thin-and-deep Transformer architecture optimized for efficient training and serving on NVIDIA hardware. It was pretrained on 12 trillion tokens and combines a one-million-token context limit with architecture changes intended to improve reasoning and inference efficiency. Ricursive also developed its own synthetic training pipelines instead of purchasing posttraining data.
Actionability angle: Builders can now test an open-weight coding model with a one-million-token context window across several hosted platforms and on local systems such as NVIDIA DGX Spark. Its reported coding score and lower-cost training profile make it worth comparing against larger open-weight models for agentic development workflows.
Listener hook: A 65B coding model that targets both strong agent performance and local deployment is now available for hands-on testing.

7. **ComfyUI Ships Texture and Dubbing Nodes**
ComfyUI’s stable v0.44.0 release adds Partner Nodes for Patina texture work and VEED dubbing, giving workflow builders new building blocks for texture creation and spoken-audio tasks. The release also updates the workflow template collection to v0.11.98. Together, the changes expand the kinds of creative pipelines that can be assembled as node-based ComfyUI workflows.
Technical depth angle: The useful mechanism is workflow-level integration: Patina arrives as texture nodes, while VEED arrives as a dubbing node, so creators can place those capabilities directly inside ComfyUI graphs. The template collection also moved to v0.11.98, keeping new workflow building blocks alongside an updated set of starting points.
Actionability angle: ComfyUI builders can now include Patina texture generation and VEED dubbing as explicit stages in creative workflows. The practical move is to test those stages with the refreshed templates and see how they fit into complete projects.
Listener hook: ComfyUI users can now build texture and dubbing directly into the same visual workflow.

8. **Voters impose new constraints on AI data centers**
American voters rejected or restricted data centers in more than 30 localities across nine states, according to Semafor. Residents approved moratoriums, outright bans, and financial or operational constraints on hyperscalers seeking tax breaks. Edgewater, Florida, overwhelmingly backed a charter ban, while Perry, Ohio, approved limits on companies seeking incentives. The results give local opposition more force just as banks and asset managers are treating it as a financing risk.
Technical depth angle: The change is happening through local government rather than a single federal rule. Voters used charter amendments, moratoria, bans, and restrictions on tax breaks, energy use, or hyperscaler operations. That patchwork can affect where data centers can be built, how they are financed, and whether companies qualify for public incentives.
Actionability angle: Data-center developers can no longer treat community opposition as a footnote: site selection, incentives, utilities, and financing may now depend on winning local support. Community engagement and realistic answers to operating costs have become part of project feasibility, not just public relations.
Listener hook: The AI infrastructure race is now running into a direct local political barrier.

9. **SambaNova and Supermicro Plan Mixed-Chip AI Inference Systems**
SambaNova and Supermicro announced a strategic collaboration to build and sell AI inference systems that combine SambaNova’s SN50 RDU chips with GPUs. Supermicro is initially planning for 10,000 SN50 chips, giving the partnership a clear scale target. The announcement frames the systems as infrastructure for the next wave of agentic AI inference, while the next important step is turning the planned collaboration and chip volume into available products.
Technical depth angle: The concrete configuration announced is an AI inference system combining RDUs and GPUs. SambaNova and Supermicro will build and sell those systems, with the collaboration initially planning for 10,000 SN50 RDU chips. The useful point is the mixed-chip design and its stated scale.
Actionability angle: For builders, this collaboration points toward another mixed-chip inference option once the planned systems become available. The next checkpoint is whether the proposed 10,000-chip deployment translates into concrete, commercially available systems.
Listener hook: A 10,000-chip plan makes this more than a laboratory experiment in combining specialized AI chips with GPUs.

10. **OpenAI links new compute campuses to grid reliability**
OpenAI introduced the Grid Protectors Program, an initiative to work with utilities so future computing campuses can support grid reliability and protect consumer electricity costs. The program connects the infrastructure demands of large computing facilities with the utilities that supply their power. For organizations planning AI deployments, it makes grid coordination and the effect on household electricity bills relevant considerations when choosing sites and planning capacity.
Technical depth angle: The announced mechanism is collaboration between OpenAI and utilities. OpenAI says the program will help future compute campuses support grid reliability and protect consumer electricity costs. Its focus is the relationship between new large-scale computing facilities, the power systems serving them, and the bills paid by consumers.
Actionability angle: For teams planning compute deployments, utility relationships and consumer cost impacts now belong in site selection and capacity planning. The point to watch is how participation and protections take shape in specific utility and campus agreements.
Listener hook: As AI infrastructure grows, this program puts electricity reliability and household costs at the center of compute-campus planning.

11. **Research digest: Lab AI understands procedures but still misses the physical details**
Current AI models can follow the broad steps of a laboratory procedure shown in video, but they struggle to identify where an action should occur and whether its physical path is feasible. The BEAKER benchmark tests these capabilities with manually curated questions on laboratory equipment, states, safety, setup, operation, and procedure order. The finding matters because understanding what should happen is not enough for a machine to control real laboratory equipment safely and reliably.
Technical depth angle: The key finding is a gap between procedural understanding and physical actionability. Models can often describe the coarse sequence of an experiment from video, yet may not reliably identify the part of an object that can be manipulated or a feasible path for carrying out the action. That distinction is essential in laboratories, where equipment, experimental state, and safety constraints shape every move.
Actionability angle: Teams can use BEAKER to test whether an AI system can connect a planned laboratory action with a visible, operable target before granting it control. The benchmark also provides a practical way to compare systems on equipment recognition, state changes, safety judgments, and procedure planning rather than relying on general video-question-answering performance alone.
Listener hook: A laboratory robot may understand the recipe while still failing to grasp the right object or route its movement safely.

12. **OpenAI built a Git backend for Codex-scale development**
OpenAI has built Pando, a Git-compatible backend designed for the scale of development that Codex makes possible. The important shift is beneath the coding agent: Pando targets the Git layer that developers rely on to track and manage code changes as AI-assisted development grows. OpenAI’s published description identifies Pando as its own backend and positions Codex-scale development as the design target, giving builders a concrete infrastructure pattern to evaluate.
Technical depth angle: The useful mechanism is Pando’s Git compatibility. It occupies the backend role for Git while targeting the larger development workload that Codex enables. The concrete technical focus is therefore repository management at Codex scale, rather than another change to the coding agent itself.
Actionability angle: For teams adopting Codex, Pando shows why to assess repository infrastructure alongside the coding agent. Git compatibility is the concrete factor to consider when evaluating this approach against an existing development stack.
Listener hook: OpenAI is scaling the code-management layer beneath Codex, not just the model doing the coding.

13. **OpenAI is acquiring Pierre to expand Codex**
OpenAI announced on November 4 that it will acquire Pierre Computer Company, expanding the tools available through Codex for building, understanding, and reviewing code. The acquisition positions OpenAI to broaden how developers can work with code through its coding product. For builders, the important change is OpenAI’s investment in Codex capabilities that span code creation, codebase comprehension, and review.
Technical depth angle: The useful product angle is broader code support inside Codex. OpenAI says the Pierre acquisition expands its abilities across three concrete tasks: building software, understanding existing code, and reviewing code. The announcement frames these as expanded Codex tools rather than describing a separate product or a specific new interface.
Actionability angle: Teams using or evaluating Codex can expect OpenAI to push the product further into the full software-development workflow. The practical takeaway is to evaluate new capabilities around code creation, codebase understanding, and review as they become available.
Listener hook: OpenAI is buying capability to make Codex more useful beyond code generation alone.

14. **Together Compiler Re-optimizes Inference as Traffic Shifts**
Together AI released Together Compiler, an agent-driven system that keeps re-optimizing an inference model’s forward pass as traffic shifts. In its reported comparison, the compiler reached up to 2.6 times the tokens per second of the best InferenceX configurations, with the optimization completed in under 24 hours per model. The release gives inference builders a way to adapt performance to changing traffic rather than leave an optimized configuration fixed.
Technical depth angle: Together Compiler runs an agent-driven loop that repeatedly re-optimizes the inference forward pass—the model computation that produces an output—as traffic changes. Together AI reports up to 2.6 times the throughput, measured in tokens per second, of the best InferenceX configurations, with the result achieved in under 24 hours per model.
Actionability angle: The practical implication is that inference deployments can keep optimization aligned with changing traffic instead of treating tuning as a one-time task. Teams should measure tokens per second on their own workloads, because the reported 2.6-times ceiling comes from a comparison with InferenceX rather than a guarantee for every model.
Listener hook: This is an optimization loop that responds when the traffic changes, not a one-time speed benchmark.

---

## Editorial Mix Check

- flagship_products: 7
- builder_projects: 9
- local_ai: 2
- hardware_compute: 3
- policy_regulation: 2
- research: 1

---

## Model Discovery Check

- **ricursiveAI/Ripple-65B-Preview** (ricursiveai) — Newly listed this cycle (verified November 05, 2026). Primary source: https://openrouter.ai/models/ricursiveai/ripple-65b-preview. Availability: API via OpenRouter. params_active: n/a; params_total: n/a; context: 1048576 tokens; modality: text->text. Capabilities: context length 1048576; Ripple-65B-Preview by ricursiveAI, a 65B model with native tool calling, served in BF16.. Try now / integration angle: Route a coding-agent session through https://openrouter.ai/models/ricursiveai/ripple-65b-preview and compare it with the current default. Decision: Selected — new major-provider model not featured on a recent broadcast.

- **inclusionAI: Ling 3.0 Tiny** (inclusionai) — Newly listed this cycle (verified November 05, 2026). Primary source: https://openrouter.ai/models/inclusionai/ling-3.0-tiny. Availability: API via OpenRouter. Capabilities: context length 262144; Ling 3.0 Tiny is a mixture-of-experts model from InclusionAI, with 1.3B active parameters out of 7.9B total. It is designed for responsive agents, instruction f. Try now / integration angle: available for evaluation via the model page above. Decision: Not Selected — variant/duplicate of a model featured on a recent broadcast, or not a major standalone drop.

---

## Local LLM Spotlight

- **moonshotai/Kimi-K3.1-Pro** — https://huggingface.co/moonshotai/Kimi-K3.1-Pro — Trending open model on Hugging Face; task image-text-to-text; 711 likes and 11658 downloads. Tags: transformers, safetensors, kimi_k31, text-generation, compressed-tensors, conversational, image-text-to-text, custom_code, license:other, eval-results.
  Try now: Read the linked model card before downloading, and choose a runtime or device only after it confirms the license, weight format, context window, benchmarks, and hardware requirements.

---

## GitHub Project Radar

- **HKUDS/nanobot** — https://github.com/HKUDS/nanobot — HKUDS/nanobot is a lightweight open-source personal agent. It provides a compact foundation for adding an agent layer to developer and personal workflows. `stars: 49,845`; `stars_delta_30d: +1,067 (+2.2%) since 2026-10-04`; `latest_release: v0.4.0 (2026-10-28)`.
  Why this is on the radar now: v0.4.0 shipped on 2026-10-28 and the repository was updated on 2026-11-05.
  Stack improvement angle: Could serve as a small, focused worker alongside OpenClaw, Codex, Claude Code, or Hermes for narrowly scoped personal-agent tasks without requiring a large framework.
  Try now: Try running nanobot on one bounded task, such as gathering a brief from a set of local notes, and evaluate the workflow it supports.

- **DeusData/codebase-memory-mcp** — https://github.com/DeusData/codebase-memory-mcp — DeusData/codebase-memory-mcp provides local code intelligence for developers and AI agents by connecting code, documentation, and infrastructure in a persistent graph. It also includes CBM Lens, MCP tools, agent integrations, and change-aware test selection. `stars: 48,151`; `stars_delta_30d: +2,382 (+5.2%) since 2026-10-04`; `latest_release: v0.12.1 (2026-10-16)`.
  Why this is on the radar now: v0.12.1 shipped on 2026-10-16 and the repository was updated on 2026-11-04.
  Stack improvement angle: Its MCP tools and persistent code graph could give OpenClaw, Codex, Claude Code, or Hermes shared repository context, while change-aware test selection could help agents target verification after edits.
  Try now: Start by connecting the repository to its MCP interface and asking the agent to map the relationships among a feature, its documentation, and its infrastructure configuration.

- **ahujasid/mcp-for-blender** — https://github.com/ahujasid/mcp-for-blender — ahujasid/mcp-for-blender is a community plugin for controlling Blender 3D with any LLM of your choice. It is not affiliated with the official Blender Foundation. `stars: 33,360`; `stars_delta_30d: +3,415 (+11.4%) since 2026-10-04`; `latest_release: none published on GitHub as of 2026-11-05`.
  Why this is on the radar now: The repository was updated on 2026-11-04 and enters the radar with 33,360 stars.
  Stack improvement angle: It could add a 3D-scene control tool to an OpenClaw, Codex, Claude Code, or Hermes workflow, allowing the agent to operate Blender through an LLM-facing integration.
  Try now: Install the plugin in a test Blender environment and issue one simple scene modification through the LLM interface.

---

## Extra Research Candidates

- **Soniox STT v6 Adds Agent Text Input and Echo Filtering for Voice Agents** — https://www.marktechpost.com/2026/11/03/soniox-stt-v6-agent-text-input-echo-cancellation/ — Soniox has released Soniox STT v6, the latest generation of its speech-to-text API. Soniox STT v6 is a speech-to-text model that reads what a voice agent says while hearing the caller. It uses that text to recognize short replies and to dro Technical depth angle: Soniox STT v6 uses text supplied from the agent to recognize short caller replies and filter the agent's own voice, with streaming and asynchronous endpoint names stt-rt-v6 and stt-async-v6.

- **Rewarding defenders with bigger bug bounties** — https://openai.com/index/rewarding-defenders-with-bigger-bug-bounties — OpenAI is raising Security Bug Bounty rewards and introducing report quality, loyalty, and priority campaign bonuses for independent security researchers. Technical depth angle: The program combines increased Security Bug Bounty rewards with report-quality, loyalty, and priority-campaign bonuses for independent security researchers.

- **Accelerating engineering for the physical world** — https://openai.com/index/accelerating-engineering-for-the-physical-world — Discover how ChatGPT and Codex are helping engineers accelerate CAD, PCB design, simulation, and other workflows across the physical world. Technical depth angle: The work applies ChatGPT and Codex to engineering workflows spanning CAD, PCB design, simulation, and related physical-world tasks.

---

## Show Notes

```md
Episode 127 — November 05, 2026

[00:00] Episode hook

OpenAI patched 948 Linux kernel vulnerabilities after building an autonomous pipeline that found, validated, and generated fixes for local privilege-escalation flaws. Each issue could let a local attacker gain elevated privileges, and the work compresses discovery, validation, and patch generation into an automated system. Astra demonstrated a frontier LLM inspecting and directly editing neural-network weights through natural-language instructions, without a custom training loop or gradient descent; the team’s Qwen3.5-0.8B experiment points toward a different way to modify model behavior. OpenAI also shipped Images 2.6 with faster generation, GIF creation, more precise editing, and new API controls across ChatGPT, Codex, and the API. Hermes Agent 0.22.7 adds collaboration, scheduling, and control improvements across the CLI, web app, Desktop, Docker, and Hermes Cloud. Ricursive Intelligence’s open-weight Ripple-65B brings native tool calling, a 1,048,576-token context window, and agentic coding designed for local use, with a reported TerminalBench 2.1 score of 80.52.

[02:00] Agent Stack Release Readout: Hermes Agent v0.22.7, v0.22.6

Nous Research shipped Hermes Agent v0.22.6 on November 2, 2026, followed by v0.22.7 on November 3. Together, the releases substantially expand how people can organize shared agent work, schedule its output, and control what it can do.

Hermes Agent v0.22.6 adds a webapp served directly by the gateway. The CLI can open it, and Desktop users can access it through a Web Access pane on their network or behind a Nous sign-in. Desktop plugins can also load inside a browser tab. The release adds group-chat renaming, disbanding, mentions, and attachment pasting; every profile can appear as a section in the Desktop sidebar.

The scheduling tools also become more manageable. Users can cancel cron jobs, choose how a job responds after a missed run, and stop a job from the Desktop cron editor. Hermes Agent v0.22.7 then allows cron jobs to post into Group Chats. That same release adds opt-in lead routing for Desktop Group Chats, a Lead badge, room purposes, shared notes, a single-column group layout that shows each member’s live state, and pinned Kanban boards available as quick-switch tabs.

Two safeguards stand out for builders. Per-skill locks can prevent an agent from making autonomous writes to a selected skill, and a pre-inference hook can block a turn before the model is called. A session’s pinned model can also be reset without deleting its history.

The next detail to watch is v0.23.0, where Hermes plans to publish curated notes covering these feature areas and the full change history from v0.22.0 onward.

[02:53] RicursiveAI’s Ripple-65B arrives on OpenRouter

OpenRouter lists Ripple-65B-Preview, a 65B model from RicursiveAI with native tool calling, served in BF16. Tool calling lets a model request that a program invoke a specific function, making the model relevant to workflows that combine large documents with external actions. The registry lists a context length of 1,048,576 tokens and a text-to-text architecture. OpenRouter’s listed pricing is $0.0000002 per prompt token, $0.0000006 per completion token, and $0.00000005 per cache-read input token. That gives builders a concrete candidate for long-context applications that need tool use. The million-token window is the headline capacity, while the registry price provides a straightforward basis for estimating usage costs. The listed model accepts text and produces text, with a context length of 1,048,576 tokens. The model is available through its listing on OpenRouter.

[03:42] Astra Edits Neural Network Weights Directly

The team reports that GPT-6 Astra can inspect raw neural-network weights, infer what a network has learned, and edit selected weights directly using natural-language reasoning rather than a training loop. In its Qwen3.5-0.8B experiment, Astra identified an issue in the weights that caused reasoning loops, then changed 0.016% of them. With the same sampling settings, the correction raised MATH-500 accuracy from 7.9% to 48.1% and tripled IFEval instruction-following performance.

The team calls this Weight-Space Programming, a method where a general-purpose LLM treats weights as editable numerical artifacts and reasons about what each part computes. This could support model repair without conventional gradient-based optimization and might extend ideas about model behavior that can be inferred from parameters alone. The results are explicitly early, so the next thing to watch is whether targeted edits can consistently improve real models beyond the reported examples.

[04:35] OpenAI found and patched 948 Linux kernel vulnerabilities

OpenAI has built an autonomous pipeline for finding and fixing serious Linux kernel flaws. It found, validated, and generated patches for 948 local privilege-escalation vulnerabilities, meaning defects that can let someone with limited access obtain higher privileges on the same machine.

The concrete shift is the size of the candidate-fix queue. Instead of leaving kernel teams to discover and repair each issue individually, the pipeline produces 948 validated vulnerability cases with generated patches that maintainers can review. OpenAI is the organization behind the pipeline, and Linux kernel security teams are the obvious audience for its output.

The next thing to watch is whether these generated patches pass expert review and become accepted fixes in Linux.

[05:18] OpenAI Ships Faster Images, GIFs, and More Precise Editing

OpenAI released Images 2.6 on November 4, making image generation faster while adding two visible creative capabilities: GIF creation and more precise editing.

The update is available across ChatGPT, Codex, and the API. That gives people an interactive route for making and refining visuals, as well as an API route for embedding those capabilities in applications.

For builders, the concrete opportunity is to add image generation, GIF creation, or precise editing to products and workflows. OpenAI has also introduced new API controls, expanding what developers can configure when they build with the model. One thing to watch next is how those controls perform in real image-editing and GIF-generation tasks.

[05:59] Ripple-65B Brings Open-Weight Agentic Coding to Local Machines

Ricursive Intelligence has released Ripple-65B Preview, a general-purpose, open-weight model that the company says sets a U.S. open-weight lead for agentic coding. It scored 80.52 on TerminalBench 2.1, ahead of Reflection Beam 501B, Meta Muse Spark Open 816B, Thinking Machines Inkling 975B, and NVIDIA Nemotron 3 Ultra 550B.

The model was pretrained on 12 trillion tokens and supports context lengths of up to one million tokens. Ricursive designed its dense architecture for efficient training and serving on NVIDIA hardware, with the goal of enabling strong local operation on systems such as NVIDIA DGX Spark. It is available on Hugging Face, Together AI, GMI Cloud, and OpenRouter, with Fireworks scheduled to launch later that day.

Ricursive reports that Ripple’s full research and development cost, including data work, evaluation, debugging, and posttraining, was $32 million. To improve coding efficiency, the company tested architectural changes at smaller model scales before scaling them up, and it built its own synthetic data pipelines rather than buying posttraining data. The next thing to watch is how the model performs outside Ricursive’s agentic-coding evaluation as development continues toward larger-scale models.

[07:08] ComfyUI Ships Texture and Dubbing Nodes

ComfyUI shipped its stable v0.44.0 release on November 4, 2026, with new creative building blocks for workflows. The release adds Partner Nodes for Patina texture work and VEED dubbing, both contributed by bigcat88.

For people building with ComfyUI, the additions provide new node-based ways to incorporate texture creation and dubbing into a workflow. The release also updates ComfyUI’s workflow templates to v0.11.98, giving builders a refreshed collection of workflow starting points.

The remaining change is internal maintenance: the project switched pylint’s Python version to 3.1. The creator-facing focus of this release is the pair of Partner Nodes, so the next useful evidence will come from complete workflows showing how the texture and dubbing stages work together.

[07:52] Voters impose new constraints on AI data centers

American voters rejected or restricted data centers in more than 30 localities across nine states. The measures included moratoria, outright bans, and financial or operational constraints for hyperscalers seeking tax breaks, with some votes responding directly to projects already underway.

The results were especially clear in Edgewater, Florida, where residents overwhelmingly backed embedding a data-center ban in the city charter. In Perry, Ohio, voters passed a measure imposing financial and operational constraints on hyperscalers seeking tax breaks.

Political pressure is broadening beyond local ballot measures. Democrats running in more than 130 federal and gubernatorial races used anti-tech or anti-data-center advertising, according to one analysis. Texas Gov. Greg Abbott, recently promoting AI and the data-center buildout, promised tougher regulation but lost his election.

That opposition is already affecting capital. Banks and asset managers financing data centers have begun treating local resistance as a credit risk, while hyperscalers are hiring community liaisons. Some companies are also trying to describe their facilities as “compute campuses,” although the rebranding has had mixed results.

The next test is whether these local constraints change where new AI infrastructure gets built, which projects can secure financing and incentives, and how operators respond when communities demand more than branding.

[09:08] SambaNova and Supermicro Plan Mixed-Chip AI Inference Systems

SambaNova and Supermicro have announced a strategic collaboration to build and sell AI inference systems that combine RDUs and GPUs. Supermicro is initially planning for 10,000 SN50 RDU chips for the effort.

SambaNova says the partnership is intended to address agentic AI, with co-founder Rodrigo Liang calling it “the next wave of inference” that has to run everywhere. The concrete proposal is a mixed system architecture rather than a single type of processor, bringing SambaNova’s RDU chips together with GPUs.

For builders, the important development is the combination of a named manufacturing partner, a product category, and an initial chip-volume target. The next thing to watch is whether the planned 10,000 SN50 chips move into available inference systems.

[09:52] OpenAI links new compute campuses to grid reliability

On November 2, OpenAI introduced the Grid Protectors Program, which will work with utilities to help future compute campuses support grid reliability and protect consumer electricity costs.

The initiative addresses both sides of AI infrastructure growth: the needs of large computing facilities and their effect on the electricity customers who support them. OpenAI is positioning the program around direct work with utilities rather than presenting new computing technology or a software release.

For organizations building AI services, the practical implication is that power access, grid reliability, and consumer costs are part of deployment planning, not separate concerns. The detail to watch is which utilities and future campuses take part and what protections result from those agreements.

[10:36] Research digest: Lab AI understands procedures but still misses the physical details

Current AI models can follow the broad steps of a laboratory procedure shown in video, but they still struggle with the physical details required to carry those steps out. The BEAKER benchmark evaluates whether models can connect an intended action with the right part of an object and a feasible movement path through a laboratory.

The authors manually curated questions covering equipment and experimental-state recognition, safety, apparatus setup, operation, procedure order, and reasoning from images and video. Current models performed better on coarse procedural steps than on tasks requiring actions to be grounded in operable regions and feasible trajectories—a path describing how a machine can move or act.

This matters because a self-driving chemical laboratory must not only understand what experiment is underway, but also perceive the scene, respect procedural and safety constraints, and choose actions that work in the physical world. For example, a system might recognize that a sample needs to move while still failing to identify what can be grasped or how to reach it. BEAKER gives research teams a concrete way to expose and compare that gap before similar models are trusted with laboratory control.

[11:48] OpenAI built a Git backend for Codex-scale development

OpenAI has built Pando, a Git-compatible backend designed for the scale of development that Codex makes possible.

The change matters because it addresses the repository layer beneath AI-assisted coding. Git is the system developers use to track and manage code changes, and Pando is designed to provide a compatible backend for development at Codex-driven scale.

The concrete evidence in OpenAI’s announcement is the system’s scope and ownership: OpenAI built it, it is Git-compatible, and Codex-driven development sets its target scale. That gives builders evaluating AI-heavy development environments a specific infrastructure pattern to consider: a Git-compatible backend designed around the workload that Codex makes possible.

How Pando performs under real repository loads is the next point to watch.

[12:32] OpenAI is acquiring Pierre to expand Codex

OpenAI announced on November 4 that it will acquire Pierre Computer Company. The company says the acquisition expands Codex’s tools for building, understanding, and reviewing code.

That gives the deal a clear product focus: strengthening the ways developers create software, inspect existing codebases, and assess code. OpenAI is using an acquisition to broaden Codex’s role across the software-development process rather than presenting the announcement as a standalone feature release.

For builders, this signals continued investment in Codex as a place for practical development work. The most useful capabilities to evaluate as they arrive are code building, code comprehension, and code review.

[13:10] Together Compiler Re-optimizes Inference as Traffic Shifts

Together AI shipped Together Compiler, an agent-driven system that keeps re-optimizing an inference model’s forward pass as traffic shifts. The forward pass is the model computation that produces its output. Together AI reports that the compiler reached up to 2.6 times the tokens per second of the best InferenceX configurations, with the result achieved in under 24 hours per model.

This matters because inference builders can now evaluate an optimization process that adapts to the traffic they actually serve instead of leaving a tuned configuration unchanged. The useful mechanism is the continuing agent-driven loop; the concrete evidence is the reported throughput comparison and optimization time. One thing to watch is whether the reported gain carries over to different models and traffic patterns.
```

---

## Chapters

- 00:00 — Intro: Agent Stack Release Readout: Hermes Agent v0.22.7, v0.22.6 / RicursiveAI’s Ripple-65B arrives on OpenRouter / Astra Edits Neural Network Weights Directly
- 02:00 — Agent Stack Release Readout: Hermes Agent v0.22.7, v0.22.6
- 02:53 — RicursiveAI’s Ripple-65B arrives on OpenRouter
- 03:42 — Astra Edits Neural Network Weights Directly
- 04:35 — OpenAI found and patched 948 Linux kernel vulnerabilities
- 05:18 — OpenAI Ships Faster Images, GIFs, and More Precise Editing
- 05:59 — Ripple-65B Brings Open-Weight Agentic Coding to Local Machines
- 07:08 — ComfyUI Ships Texture and Dubbing Nodes
- 07:52 — Voters impose new constraints on AI data centers
- 09:08 — SambaNova and Supermicro Plan Mixed-Chip AI Inference Systems
- 09:52 — OpenAI links new compute campuses to grid reliability
- 10:36 — Research digest: Lab AI understands procedures but still misses the physical details
- 11:48 — OpenAI built a Git backend for Codex-scale development
- 12:32 — OpenAI is acquiring Pierre to expand Codex
- 13:10 — Together Compiler Re-optimizes Inference as Traffic Shifts

---

## Primary Links

- Hermes Agent v0.22.7 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.7
- Hermes Agent v0.22.6 release: https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.6
- ricursiveAI/Ripple-65B-Preview model page: https://openrouter.ai/models/ricursiveai/ripple-65b-preview
- Astra can read and write weights to improve Qwen: https://rikiyat.github.io/blog/weight-space-programming/
- A thousand fewer paths to root: https://openai.com/index/a-thousand-fewer-paths-to-root/
- Images 2.6: https://openai.com/index/introducing-images-2-6/
- Ripple-65B Preview: U.S. Open-Weight SOTA on Agentic Coding: https://www.ricursive.com/ripple
- comfyanonymous/ComfyUI ships v0.44.0: https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.44.0
- US voters roundly reject data centers in ballot measures: https://www.semafor.com/article/11/04/2026/us-voters-roundly-reject-data-centers-in-ballot-measures
- SambaNova and Supermicro to Build AI Inference Systems Combining RDUs : https://www.hpcwire.com/off-the-wire/sambanova-and-supermicro-to-build-ai-inference-systems-combining-rdus-and-gpus/
- Introducing the Grid Protectors Program: https://openai.com/index/grid-protectors-program
- BEAKER: An Expert-Curated Benchmark for Embodied Brains in Self-Drivin: https://arxiv.org/abs/2611.06911
- Scaling Git at OpenAI: https://openai.com/index/scaling-git-at-openai/
- OpenAI to acquire Pierre Computer Company: https://openai.com/index/openai-to-acquire-pierre/
- Together AI Releases Together Compiler: Agents Make Inference Up to 2.: https://www.marktechpost.com/2026/11/05/together-ai-together-compiler-continual-compilation-ai-inference/
- HKUDS/nanobot repo: https://github.com/HKUDS/nanobot
- DeusData/codebase-memory-mcp repo: https://github.com/DeusData/codebase-memory-mcp
- ahujasid/mcp-for-blender repo: https://github.com/ahujasid/mcp-for-blender
- Soniox STT v6 Adds Agent Text Input and Echo Filtering for Voice Agent: https://www.marktechpost.com/2026/11/03/soniox-stt-v6-agent-text-input-echo-cancellation/
- Rewarding defenders with bigger bug bounties: https://openai.com/index/rewarding-defenders-with-bigger-bug-bounties
- Accelerating engineering for the physical world: https://openai.com/index/accelerating-engineering-for-the-physical-world
- moonshotai/Kimi-K3.1-Pro: https://huggingface.co/moonshotai/Kimi-K3.1-Pro

---

## Release Coverage Check

- **Hermes Agent** — Latest stable verified: `v0.22.7`, published 2026-11-03T21:53:16Z. Recent episode version tags detected: `v2026.9.14`, `v2026.9.21`, `v2026.9.24`, `v2026.9.7`. Selected missing version(s): `v0.22.7`, `v0.22.6`.
- **OpenAI Codex** — Latest stable verified: `rust-v0.166.0`, published 2026-10-29T19:47:53Z. Recent episode version tags detected: `rust-v0.162.0`, `rust-v0.163.0`, `rust-v0.164.0`, `rust-v0.165.0`. No new stable release this cycle.
- **Claude Code CLI** — Latest stable verified: `2.1.311`, published 2026-10-26T19:47:57.395Z. Recent episode version tags detected: `2.1.304`, `2.1.308`, `latest`, `stable`. No new stable release this cycle.
- **Antigravity CLI** — Continuous delivery model; no discrete release tags verified this cycle (latest build as of 2026-11-05). Recent episode version tags detected: `@google/antigravity`, `v2.0`.

---

## Harness Version Reference

- **Hermes Agent** — `v0.22.7`
- **OpenAI Codex** — `rust-v0.166.0`
- **Claude Code CLI** — `2.1.311`
- **Antigravity CLI** — Continuous delivery (no tagged release verified this cycle)


---

## Featured Story Plan

- Story 3: **Astra Edits Neural Network Weights Directly** — prioritize its source-backed capability, comparison when documented, limitations, and practical consequence; no word quota.
- Story 6: **Ripple-65B Brings Open-Weight Agentic Coding to Local Machines** — prioritize its source-backed capability, comparison when documented, limitations, and practical consequence; no word quota.

---

## Research Evidence Contract

```json
{
  "policy_version": 1,
  "featured_stories": [
    3,
    6
  ],
  "records": [
    {
      "story": 1,
      "title": "Agent Stack Release Readout: Hermes Agent v0.22.7, v0.22.6",
      "source_sha256": "59f992b028bf191f2408c5bce556ff0ac1bc63743079e6bdcb00efbdd6512fe4",
      "source_url": "https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.7",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 2,
      "title": "RicursiveAI’s Ripple-65B arrives on OpenRouter",
      "source_sha256": "15cfff8ae0e7ea846da59c26041c4106540e6b3ef430ae123c33798b21cc8958",
      "source_url": "https://openrouter.ai/models/ricursiveai/ripple-65b-preview",
      "model_story": true,
      "model_review": {
        "release_status": "registry_listing",
        "evidence_type": "registry_listing",
        "release_quote": "This model is listed by OpenRouter at https://openrouter.ai/models/ricursiveai/ripple-65b-preview.",
        "release_span": "S002",
        "change": {
          "status": "supported",
          "claim": "OpenRouter lists Ripple-65B-Preview, a 65B model from RicursiveAI with native tool calling, served in BF16.",
          "quote": "Ripple-65B-Preview by ricursiveAI, a 65B model with native tool calling, served in BF16.\nThis model is listed by OpenRouter at https://openrouter.ai/models/ricursiveai/ripple-65b-preview.",
          "source_span": [
            "S001",
            "S002"
          ],
          "quotes": [
            "Ripple-65B-Preview by ricursiveAI, a 65B model with native tool calling, served in BF16.",
            "This model is listed by OpenRouter at https://openrouter.ai/models/ricursiveai/ripple-65b-preview."
          ]
        },
        "capabilities": {
          "status": "supported",
          "claim": "The listed model accepts text and produces text, with a context length of 1,048,576 tokens.",
          "quote": "Context length: 1048576 tokens.\nRegistry architecture: {\"modality\": \"text->text\", \"input_modalities\": [\"text\"], \"output_modalities\": [\"text\"], \"tokenizer\": \"Other\", \"instruct_type\": null}\nRegistry pricing per token in USD: {\"prompt\": \"0.0000002\", \"completion\": \"0.0000006\", \"input_cache_read\": \"0.00000005\"}",
          "source_span": [
            "S003",
            "S004"
          ],
          "quotes": [
            "Context length: 1048576 tokens.",
            "Registry architecture: {\"modality\": \"text->text\", \"input_modalities\": [\"text\"], \"output_modalities\": [\"text\"], \"tokenizer\": \"Other\", \"instruct_type\": null}\nRegistry pricing per token in USD: {\"prompt\": \"0.0000002\", \"completion\": \"0.0000006\", \"input_cache_read\": \"0.00000005\"}"
          ]
        },
        "comparison": {
          "status": "unverified",
          "claim": "",
          "quote": "",
          "source_span": []
        },
        "limitations": {
          "status": "unverified",
          "claim": "",
          "quote": "",
          "source_span": []
        },
        "access": {
          "status": "supported",
          "claim": "The model is available through its listing on OpenRouter.",
          "quote": "This model is listed by OpenRouter at https://openrouter.ai/models/ricursiveai/ripple-65b-preview.",
          "source_span": [
            "S002"
          ],
          "quotes": [
            "This model is listed by OpenRouter at https://openrouter.ai/models/ricursiveai/ripple-65b-preview."
          ]
        }
      }
    },
    {
      "story": 3,
      "title": "Astra Edits Neural Network Weights Directly",
      "source_sha256": "7f1ec324c4654dda0527af233376c3043d2ed908e41c7c2999f7b0e9d1839410",
      "source_url": "https://rikiyat.github.io/blog/weight-space-programming/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 4,
      "title": "OpenAI found and patched 948 Linux kernel vulnerabilities",
      "source_sha256": "928ad5c8e0d488652928fd7c8a5a01c7a33e10471eaf04225d6e25f2527c3413",
      "source_url": "https://openai.com/index/a-thousand-fewer-paths-to-root/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 5,
      "title": "OpenAI Ships Faster Images, GIFs, and More Precise Editing",
      "source_sha256": "467849bac482b7de0f2c7bdb500b24fb70352ad5c5902e79cc071340573e1876",
      "source_url": "https://openai.com/index/introducing-images-2-6/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 6,
      "title": "Ripple-65B Brings Open-Weight Agentic Coding to Local Machines",
      "source_sha256": "9ba13b57e2e098188367f79e1acbcf15b880012666f406557c7b8faa338386cb",
      "source_url": "https://www.ricursive.com/ripple",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 7,
      "title": "ComfyUI Ships Texture and Dubbing Nodes",
      "source_sha256": "d3eba4323b1122ad10bb210b6c82cb4e84808bad04fe2394d528b44c00395c88",
      "source_url": "https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.44.0",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 8,
      "title": "Voters impose new constraints on AI data centers",
      "source_sha256": "6e5580965276f717e528d2e1b17d0788ea74374fe3c7b1d0721e6e1557ff7fe4",
      "source_url": "https://www.semafor.com/article/11/04/2026/us-voters-roundly-reject-data-centers-in-ballot-measures",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 9,
      "title": "SambaNova and Supermicro Plan Mixed-Chip AI Inference Systems",
      "source_sha256": "be1b089ef8bed82665c65b57a325b0fe6232b6e2850613c5358959709bbd2d82",
      "source_url": "https://www.hpcwire.com/off-the-wire/sambanova-and-supermicro-to-build-ai-inference-systems-combining-rdus-and-gpus/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 10,
      "title": "OpenAI links new compute campuses to grid reliability",
      "source_sha256": "a156ccb9fdb49ab0a0034c95938402813b61197d516110912e269819641d6ea0",
      "source_url": "https://openai.com/index/grid-protectors-program",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 11,
      "title": "Research digest: Lab AI understands procedures but still misses the physical details",
      "source_sha256": "22280f583d9c2ae27a8b8e8fdb8844b16de44fe262742820cd60fc74ecbdf7f0",
      "source_url": "https://arxiv.org/abs/2611.06911",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 12,
      "title": "OpenAI built a Git backend for Codex-scale development",
      "source_sha256": "6c2afe73d4521befc2fe577ea7cac490fed25d388b7428a889c1172be31730cf",
      "source_url": "https://openai.com/index/scaling-git-at-openai/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 13,
      "title": "OpenAI is acquiring Pierre to expand Codex",
      "source_sha256": "baa9fa7ba160ca33b70e879f1fd4078dd4012c64019b68cb6d9eb2c1efc2c512",
      "source_url": "https://openai.com/index/openai-to-acquire-pierre/",
      "model_story": false,
      "model_review": null
    },
    {
      "story": 14,
      "title": "Together Compiler Re-optimizes Inference as Traffic Shifts",
      "source_sha256": "19229eecf0a61c63e6171676e499578d60a5c421b357a8b71bcae4f3e75faa0f",
      "source_url": "https://www.marktechpost.com/2026/11/05/together-ai-together-compiler-continual-compilation-ai-inference/",
      "model_story": false,
      "model_review": null
    }
  ]
}
```
