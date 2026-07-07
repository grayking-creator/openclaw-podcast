#!/usr/bin/env python3
"""Generate an AgentStack Daily transcript from approved show notes.

This is the explicit show-notes -> transcript artifact step used before
build_episode.py. It calls OpenClaw's configured OpenAI text model directly;
it does not spawn nested OpenClaw agents or background workers.

Environment variables:
  TRANSCRIPT_MODEL   Override with one model (e.g. openai/gpt-5.5).
  TRANSCRIPT_MODELS  Comma-separated provider fallback list. Models must
                     support ~8k-10k output tokens for 6,000+ word transcripts.
  TRANSCRIPT_GEN_ATTEMPTS  Max regenerate+QC attempts (default: 3).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
DEFAULT_MODEL_SPEC = (
    os.environ.get("TRANSCRIPT_MODEL")
    or os.environ.get("TRANSCRIPT_MODELS")
    # Route order locked 2026-06-29 after EP076 rejection: MiniMax-M3 is the
    # only model in this fleet that has the right editorial register (concrete,
    # direct, no drone-cadence, no listener-facing pin advice, no "for builders"
    # verdict spam). GPT-5.5 reliably produces the rejected pattern; gemini-3
    # and nemotron truncate at the wrong place. New order:
    #   tier 1 (voice match):  minimax/MiniMax-M3
    #   tier 2 (free fallback): google/gemini-3-flash-preview, nvidia/nemotron-3-super-120b-a12b
    #   tier 3 (final fallback, sometimes drone): openai/gpt-5.5
    # Removed from the old list: google-2/gemini-2.5-flash (404),
    # openai/gpt-5.4-mini (connection error), anthropic/claude-sonnet-4-6 (no
    # API key for this agent).
    #   tier 4 (added 2026-07-05, EP080 incident): freecall free-model routes —
    #   minimax (MiniMax-M2.7, 200k ctx long-form), nvidia (DeepSeek V3.2),
    #   groq (Llama 3.3 70B). These use the OpenClaw freecall runner with its
    #   own key resolution, so they survive a same-day outage of the openclaw
    #   infer providers above. (mistral omitted 2026-07-05: no resolvable key
    #   on this machine — probe `freecall mistral` before re-adding.)
    #   tier 5 (added 2026-07-04): exo:auto — the local exo cluster ring (this
    #   Mac + the DGX node, OpenAI-compatible API). Last resort so the morning
    #   still produces a transcript on local weights when every cloud route is
    #   down or quota'd at 6:30 AM.
    or "minimax/MiniMax-M3,google/gemini-3-flash-preview,nvidia/nemotron-3-super-120b-a12b,openai/gpt-5.5,"
       "freecall:minimax,freecall:nvidia,freecall:groq,exo:auto"
)

# Substrings that mean "this route is unusable right now" (provider/transport/
# auth/quota), as opposed to "the model produced a draft that failed QC". A
# route failure demotes the model and tries the next one WITHOUT consuming a
# QC-repair attempt — dead routes must never starve the viable ones (EP071,
# 2026-06-15: 5 of 6 routes were dead and the one working route got a single
# shot).
ROUTE_FAIL_MARKERS = (
    "no text output", "no outputs", "empty transcript",
    "503", "service unavailable", "unavailable", "high demand",
    "404", "not found", "connection error",
    "auth lookup failed", "no api key", "unauthorized", "401", "403",
    "429", "rate limit", "rate-limit", "quota", "resource_exhausted",
    "model_not_found", "llm request failed", "timed out",
)
# How many times to (re)generate when the model produces a draft that fails
# check_episode.py. Each retry feeds the exact QC failures back to the model so
# it repairs them, instead of reporting a failure right after a successful
# generation and leaving a half-built .tmp for a human/agent to salvage.
# Override with TRANSCRIPT_GEN_ATTEMPTS.
# Raised 3→5 on 2026-06-15: EP071 converged 20→5→4→1 QC errors across routes but
# ran out of the 3-repair budget one round short of clean. Strong routes (MiniMax
# M3, gpt-5.5) revise reliably, so a few more rounds let the morning self-finish.
DEFAULT_ATTEMPTS = max(1, int(os.environ.get("TRANSCRIPT_GEN_ATTEMPTS", "5")))


def read_text(path: Path, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    return text if limit is None else text[:limit]


def parse_models(spec: str) -> list[str]:
    models = [m.strip() for m in spec.split(",") if m.strip()]
    if not models:
        raise SystemExit("No transcript models configured")
    return models


def recent_transcript_excerpt(ep_num: int) -> str:
    # One example is enough for format; three 5KB excerpts bloated the input
    # and squeezed the model's output budget on 10-story episodes, causing
    # truncated drafts (EP068, 2026-06-10).
    excerpts: list[str] = []
    for prior in range(ep_num - 1, max(-1, ep_num - 4), -1):
        path = PODCAST_DIR / "episodes" / f"episode_{prior:03d}_transcript.md"
        if path.exists():
            excerpts.append(f"--- EP{prior:03d} format excerpt ---\n{read_text(path, 4000)}")
            break
    return "\n\n".join(excerpts)


def build_prompt(
    ep_num: int,
    show_notes: str,
    examples: str,
    repair_feedback: str = "",
    listener_feedback: str = "",
    current_transcript: str = "",
) -> str:
    ep_str = f"{ep_num:03d}"
    revision_block = ""
    if listener_feedback.strip():
        current_block = ""
        if current_transcript.strip():
            current_block = f"""
Current transcript to revise (change what the feedback asks for; keep what was already good):
--- CURRENT TRANSCRIPT START ---
{current_transcript.strip()}
--- CURRENT TRANSCRIPT END ---
"""
        revision_block = f"""

REVISION TASK (highest priority) — a transcript was already produced and the reviewer listened to the generated audio and left the feedback below. Return a corrected FULL transcript that concretely addresses every point of this feedback while keeping every hard format requirement above. Make the changes the feedback asks for; do not merely reword. Do not narrate the feedback, the revision, or the review process anywhere in the transcript.
--- REVIEWER AUDIO FEEDBACK ---
{listener_feedback.strip()}
--- END REVIEWER AUDIO FEEDBACK ---
{current_block}"""
    repair_block = ""
    if repair_feedback.strip():
        repair_block = f"""

CRITICAL — the previous draft was REJECTED by automated QC (check_episode.py). Return a corrected FULL transcript that fixes every issue below and does not reintroduce any of them. Common fix: never read full patch version numbers aloud (e.g. write "Claude Code latest" or "Claude Code two point one", never "2.1.159"); keep version tags out of the opening; remove any meta/build-process or internal-path language.
--- QC FAILURES TO FIX ---
{repair_feedback.strip()}
--- END QC FAILURES ---
"""
    return f"""
Write the complete AgentStack Daily transcript for EP{ep_str} from the approved show notes.

Return only the transcript markdown. Do not use a code fence. Do not include analysis,
notes, comments, word counts, metadata footers, or build-process narration.

Hard format requirements:
- Save-ready transcript body for episodes/episode_{ep_str}_transcript.md.
- Use alternating speaker turns beginning with [NOVA]: and [ALLOY]:.
- Include timestamped markdown section headings that match the show-note story slate.
- Include [PAUSE] tags between major sections for TTS pacing.
- The first two spoken lines after the title must be exactly shaped as "[NOVA]: I'm NOVA." and "[ALLOY]: I'm ALLOY, and this is AgentStack Daily..."
- The outro must point listeners to the show notes at the site with a CTA like "look at the show notes at Toby On Fitness Tech dot com" — it must contain the phrase "show notes" and the exact site CTA "Toby On Fitness Tech dot com" — and include the exact closing phrase "We'll be back soon."
- Do NOT read the show-notes text/markdown aloud as episode content, and do NOT read source links or URLs aloud anywhere in the transcript (no "h-t-t-p-s", no spoken "dot com slash ...", no reading out a list of links). Describe what is at a source in plain language instead. The only spoken web reference allowed is the "Toby On Fitness Tech dot com" CTA.
- Do not mention Toby, request feedback, drafting, review, build logs, artifacts, internal tools, or local paths anywhere else.
- NEVER narrate the episode's own format or editorial construction. Do not use the word "homework", and never say things like "no homework episode today", "this episode", "today's episode", "the model story in this episode", "in this block/segment", "we'll focus on", or otherwise describe how the show is structured or what kind of episode it is. Just deliver the content directly — the listener should never hear the editorial rules we build it under.
- REQUIRED: within the first 300 words, include one forward-looking line that tells the listener what is coming, anchored on the word "today" or the phrase "you'll hear" (e.g. "Today: <headline one>, <headline two>, and <headline three>."). This is the allowed way to set the agenda — never "this episode" or "today's episode".
- Word choice: keep the vocabulary on builder workflows — how you use it, in practice, what you get, build/configure/deploy/wire/ship. Minimize the literal words "document(s)", "file(s)", "folder(s)", "copy", "move(d)", "storage", "record(s)" — when mechanics involve them, name the concrete surface instead (config, session, payload, API, schema). QC counts these words and fails drafts that lean on file/document plumbing language.
- Use SHORTENED version numbers when spoken, never full ones. For OpenClaw "v2026.5.28" say "5.28" (month dot day); for Claude Code "2.1.159" say ".159" or "two point one". Never read a full version aloud: not "v2026.5.28", not "2026.5.28", not "2.1.159".
- Keep the episode focused on concrete AI/agent/model/tooling news, mechanisms, releases, repos, workflows, and why they matter.
- LENGTH BAND (locked 2026-07-04, EP079 rejection): the floor IS back. Target 4,800-5,200 words to land the show at 30+ minutes, hard ceiling 5,400 words. EP076 (2026-06-29) said "I don't have a floor anymore ... add more stories" and the floor was dropped; EP079 came in at 2,898 words / 19 minutes and Toby rejected it as "unacceptable to deliver." History: EP072 at 8,052 words / 55 min was rejected as drone — DO NOT regress to that. The new range (4,800-5,400) sits below the drone ceiling and above the floor, and is calibrated against EP071 v3 (the 30-minute approval benchmark) and EP075 recovery. If you are short, deepen model/capability stories with concrete mechanisms, benchmark numbers, and integration patterns — never by adding procedural/tests/checklist material. If you are long, cut repeated closing summaries and operational slog. Never extend past 5,400.
- CRITICAL STORY-LEVEL RULE: each story segment uses at most 4 NOVA/ALLOY turns before [PAUSE]. The pattern NOVA-news → ALLOY-implication → NOVA-deeper → ALLOY-builder-relevance → [PAUSE] is the two-voice exposition loop; do not repeat the same opening verb phrase across consecutive stories. Vary the arc per story: NOVA-hard-news → ALLOY-one-implication → NOVA-quick-context → ALLOY-bullet-risk; or ALLOY-news → NOVA-mechanism → ALLOY-bullet-risk → NOVA-watch-next; or a single NOVA monologue for short items.
- HARD WORD BUDGET per story (TTS-spoken body between two [PAUSE] tags, excluding the segment label): 270-320 words target for non-release stories, 350-420 words target for release stories. Anything under 270 (or 350 for release) gets the episode rejected as too short — locked 2026-07-04, EP079 (19-min / 2,898-word rejection). Anything over 320 / 480 is the drone pattern from EP072 — also rejected. Hit the band: dense paragraphs, two concrete mechanisms per story, but no padding filler or repeated closing summaries.
- If reviewer feedback says the episode is "too long", "too much homework", "do this then do that", or "boring drone", the fix is structural surgery on the slate and transcript, not light phrase cleanup. Cut procedural/test/checklist content and front-loaded operational slog. Replace removed content with a tight 270-320 word block (350-420 for release stories), not with more material.
- If reviewer feedback says the episode is "too short" / "needs way more news" / "should be 30 minutes" / "unacceptable length" (locked 2026-07-04, EP079), the fix is to ADD stories to the numbered slate (target 14, not 10) and DEEPEN each story segment to the 270-320 word band — never to lower the floor, never to drop coverage of radar / spotlight / extras. Hit the band, not the floor.
- Do not make the episode feel like homework. Avoid repeated "run this test", "here is the checklist", "recommended test", or "try this drill" framing. Use checks sparingly only where they explain real migration risk or observed breakage. For model releases, prioritize capabilities, improvement size, real-world reaction, what people are doing with it, and where vendor claims still need independent confirmation.
- If the show notes contain user feedback that a prior draft felt like "do this, then do that" homework, rebuild the structure from scratch. The episode should feel informational and opinionated, not like a migration checklist. Keep the agent-harness coverage concise and informational — do not spend the first 20 minutes on operational validation/tests.
- Do not pad the ending with repeated summaries, repeated "one extra detail" blocks, or near-identical practical-move paragraphs. Every paragraph must advance the episode.
- CLI/agent release coverage = released stable tags ONLY. Do not narrate dist-tags like "npm latest" vs the Anthropic "stable" channel, do not compare "received via update" vs "latest available," and do not frame a story around a package bump or a channel republish. If the only news for a CLI is a dist-tag republish, it is not a story — drop it or skip the segment. Spoken transcript must never say "npm latest" or "received via update" or "latest versus received" for any CLI/agent release.
- HARD: NEVER say that a harness (OpenClaw, Hermes, Codex, Claude Code, Antigravity) had no release, no update, no changes, "remains at" a version, "held steady", or "didn't ship" this cycle. Harnesses that did not ship are simply not mentioned in release coverage — silence, not a roll call. Only name a harness in release context when it actually shipped.
- Claude Code is a terminal-based AI coding agent. Refer to it in the spoken intro and in any segment about it as "the terminal-based AI coding agent Claude Code" (or equivalent — the words "terminal-based" + "AI coding agent" must appear together the first time it is named per episode). Codex CLI / rust-v0.138.0 is similarly a terminal-based coding agent — say so the first time it is named. Do not introduce either product as a bare "CLI" without that framing.

REQUIRED STRUCTURE — the episode must ALWAYS start with the agent-harness updates, then move to model/other stories (follow this exact order):
1. Opening hook (~150-200 words, before the first timestamped segment): in the first two sentences, name the agent-harness release(s) in SHORTENED form (e.g. OpenClaw "5.28", Claude Code ".159", never "v2026.5.28") and state at least two concrete changes using verbs like added/fixed/tightened/introduced, naming concrete surfaces (sessions, plugins, auth, browser, cron, provider, etc.). No abstract "today we connect the dots" framing.
2. First timestamped segment(s) = the agent-harness updates — OpenClaw, OpenAI Codex, Claude Code CLI, and Hermes Agent wherever they changed this cycle. This is ALWAYS the front of the episode. Deliver it as INFORMATIONAL news: what changed, what it provides, how you actually use it, and real-world reactions/breakage — NOT a list of "run this test, then run that." Keep it concise and dense; do not let it sprawl into operational validation.
3. After the harness updates, cover the flagship model story (the biggest model drop in the show notes, e.g. MiniMax M3) and then the other slate stories in show-note order — same informational depth: what it is, how you use it, what it provides, who is using it and how it is landing, and where vendor claims still need confirmation.
4. The agent-harness updates lead; the model/news stories follow. Never open the episode on a non-harness story.
- HARD: the spoken transcript must name every covered release in SHORTENED form (e.g. "5.28") within the first 320 words — never the full "v2026.5.28".
- HARD: floor 4,800 words (30-minute target); ceiling 5,400 words (drone ceiling). Both enforced by check_episode.py. EP072 at 8,052 words was rejected as drone; EP079 at 2,898 words was rejected as too short.
- HARD: end with the show-notes CTA and the EXACT phrase "We'll be back soon." Never "we'll be back next week".
- HARD: never write the words "story slate" or "show notes block" in the spoken transcript, and never write a full version like "2.1.159" or "v2026.5.28" — use the shortened spoken form (".159", "5.28").
- EDITORIAL REGISTER (locked 2026-06-29, EP076 rejection): write concrete facts and direct observations. Avoid abstract-noun framings like "The X is the Y" / "the signal is" / "the pattern is" / "the mechanism is" / "the architecture is" / "the strategic read is" / "the practical read is" / "the failure mode is" / "the bottleneck is" / "the risk is" / "the builder relevance is" — use them sparingly (no more than 4 times in one segment, 10 times across the whole episode). If a sentence could start with "This is the X," rewrite it as a concrete observation. Never open with "Today, the X is the Y" — open with the news itself. Do not write listener-facing pin/version-target/back-merge advice (no "you should pin", no "as a target version"). Avoid "for builders" verdicts stacked at the end of paragraphs — write one concrete takeaway per story, not a checklist.

REQUIRED FULL-SURFACE COVERAGE (locked 2026-06-18, EP072 round 3 — Toby: "you're missing the GitHub projects and all of that stuff that's in the show notes"): the transcript must cover EVERY required show-notes section, not just the 10-story numbered slate. After the slate stories, add spoken segments in this order:

  a. **GitHub Project Radar segment** — at minimum 3 repos from the show notes' GitHub Project Radar. One short segment per repo, each ≤320 words, naming the repo, what it does, the headline mechanism, and a concrete integration angle. Total radar block ≤720 words.

  b. **Model Discovery Check segment** — every model marked "Selected" in the show notes' Model Discovery Check gets its own short spoken beat (≤200 words each). Any "Not Selected" entries get one collective beat in a single sentence.

  c. **Local LLM Spotlight segment** — one short segment (≤200 words) on the spotlighted model with the practical "Try now" angle from the show notes.

  d. **Extra Research Candidates segment** — three short segments (one per extra), each ≤200 words, drawn from the show notes' Extra Research Candidates block. If the show lands under 30 minutes after the rest of the script is built, expand each extra to a non-release slate story (≤320 words). If the show lands over 30 minutes, summarize as one tight beat naming each extra in one line.

  e. **Practical queue** — one line per major thread, no checklist, no repeated summaries.

Treat the show notes as the source of truth for what must be spoken. Skipping any of the above is a hard QC failure.

Approved show notes are the source of truth:
--- SHOW NOTES START ---
{show_notes}
--- SHOW NOTES END ---

Recent transcript examples for structure only:
{examples}
{revision_block}{repair_block}
""".strip()


def extract_text_from_json(stdout: str) -> str:
    data = json.loads(stdout)
    outputs = data.get("outputs") or []
    if not outputs:
        raise RuntimeError("OpenClaw model run returned no outputs")
    text = outputs[0].get("text") or ""
    text = text.strip()
    text = re.sub(r"^```(?:markdown|md)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    if not text:
        raise RuntimeError("OpenClaw model run returned empty transcript text")
    return text.strip() + "\n"


def tail_text(path: Path, limit: int = 4000) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text[-limit:].strip()


def terminate_process_group(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except Exception:
        proc.terminate()
    deadline = time.time() + 5
    while time.time() < deadline:
        if proc.poll() is not None:
            return
        time.sleep(0.1)
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except Exception:
        proc.kill()


def _strip_state_banner(text: str) -> str:
    """openclaw prints a benign 'Legacy state migration warnings' banner on
    stderr for every infer call (conflicting plugin metadata for codex/discord).
    Strip it so it never masks the real error tail or muddies route logs."""
    keep = []
    for line in (text or "").splitlines():
        low = line.lower()
        if ("state-migration" in low or "legacy state migration" in low
                or "left plugin install index" in low or "shared sqlite state" in low):
            continue
        keep.append(line)
    return "\n".join(keep).strip()


FREECALL_BIN = "/Users/tobyglennpeters/.openclaw/bin/freecall"


def _run_freecall(spec: str, prompt: str, timeout: int) -> str:
    """Run a prompt through the freecall runner (free-model providers).

    spec is the part after the `freecall:` prefix — a provider/alias
    (minimax, mistral, groq, …), `best` for the cross-provider waterfall,
    or an explicit model id containing `/`. Long-form output needs the
    raised max-tokens budget (reasoning models truncate below 8192).
    """
    cmd = [FREECALL_BIN, spec, prompt, "--timeout", str(timeout), "--max-tokens", "16000"]
    try:
        proc = subprocess.run(
            cmd, cwd=str(PODCAST_DIR), capture_output=True, text=True,
            timeout=timeout + 60,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"LLM request failed: freecall {spec} timed out after {timeout}s") from exc
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "no output").strip()
        raise RuntimeError(f"LLM request failed via freecall {spec}: {detail[:1600]}")
    text = proc.stdout.strip()
    # First line is the routing banner, e.g. "[via llama-3.3-70b-versatile]".
    text = re.sub(r"^\[via [^\]]+\]\s*", "", text)
    # Reasoning models (MiniMax M2.7, DeepSeek) may emit a <think> block.
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    text = re.sub(r"^```(?:markdown|md)?\s*", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    if not text.strip():
        raise RuntimeError(f"LLM request failed: freecall {spec} returned no text output")
    return text.strip() + "\n"


def run_model(prompt: str, model: str, timeout: int) -> str:
    if model.startswith("freecall:"):
        return _run_freecall(model.split(":", 1)[1], prompt, timeout)
    if model.startswith("exo:"):
        # Local exo cluster route (added 2026-07-04). Reuses the builder's
        # HTTP helper; a full transcript needs a large output budget. Route
        # failures raise and are matched by ROUTE_FAIL_MARKERS upstream.
        import build_show_notes as _bsn
        text = _bsn._run_exo(model[4:], prompt, timeout, max_tokens=12000)
        text = re.sub(r"^```(?:markdown|md)?\s*", "", text.strip(), flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        if not text:
            raise RuntimeError("exo route returned empty transcript")
        return text.strip() + "\n"
    cmd = [
        "openclaw",
        "infer",
        "model",
        "run",
        "--model",
        model,
        "--json",
        "--prompt",
        prompt,
    ]

    # Do not capture stdout/stderr with PIPE here. `openclaw infer` can spawn an
    # `openclaw-infer` worker; if a descendant keeps the pipe fd open after the
    # immediate child exits, Python can hang in communicate() until the full
    # timeout even though no artifact will ever be produced.
    with tempfile.TemporaryDirectory(prefix="agentstack-transcript-model-") as tmp_dir:
        stdout_path = Path(tmp_dir) / "stdout.json"
        stderr_path = Path(tmp_dir) / "stderr.log"
        with stdout_path.open("w", encoding="utf-8") as stdout_fh, stderr_path.open("w", encoding="utf-8") as stderr_fh:
            proc = subprocess.Popen(
                cmd,
                cwd=str(PODCAST_DIR),
                stdout=stdout_fh,
                stderr=stderr_fh,
                text=True,
                start_new_session=True,
            )
            try:
                returncode = proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired as exc:
                terminate_process_group(proc)
                detail = _strip_state_banner(tail_text(stderr_path) or tail_text(stdout_path)) or "no output"
                raise RuntimeError(
                    f"Transcript model generation timed out after {timeout}s: {detail[:1600]}"
                ) from exc

        stdout = stdout_path.read_text(encoding="utf-8", errors="ignore")
        stderr = _strip_state_banner(tail_text(stderr_path))

    if returncode != 0:
        detail = (stderr or stdout or "no output").strip()
        raise RuntimeError(f"Transcript model generation failed: {detail[:1600]}")
    try:
        return extract_text_from_json(stdout)
    except (json.JSONDecodeError, RuntimeError) as exc:
        detail = (stderr or stdout or "no output").strip()
        raise RuntimeError(
            f"Transcript model generation returned invalid JSON/text: {exc}; output tail: {detail[-1600:]}"
        ) from exc


def looks_truncated(text: str) -> bool:
    """A complete transcript always ends with the exact closing phrase; a draft
    without it in the tail was cut off by the model's output ceiling."""
    return "We'll be back soon" not in text[-800:]


def complete_truncated_draft(text: str, ep_num: int, show_notes: str, model: str,
                             timeout: int) -> str:
    """Ask the model to write ONLY the missing remainder, then splice. This is
    a much smaller output than a full regeneration, so it cannot itself hit the
    output ceiling. Added 2026-06-10 after EP068 lost three full regenerations
    to truncation."""
    # Trim the partial back to the last complete paragraph boundary.
    cut = text.rfind("\n\n")
    if cut > len(text) * 0.6:
        text = text[:cut].rstrip() + "\n"
    tail = text[-1500:]
    prompt = f"""A podcast transcript was cut off mid-generation. Write ONLY the missing remainder — do not repeat any existing text, do not add commentary or a code fence. Pick up exactly where the partial stops and finish the episode.

Requirements for the remainder:
- Continue the alternating [NOVA]: / [ALLOY]: speaker turns with [PAUSE] between major sections.
- Cover any show-note slate stories not yet covered (compare the partial against the show notes below), then a short practical-queue wrap-up.
- End with the outro: point listeners to the show notes with the exact CTA "Toby On Fitness Tech dot com" and the exact closing phrase "We'll be back soon."
- Never read URLs aloud; never mention Toby outside the CTA; never use full version numbers aloud (shortened spoken forms only); never say "story slate", "show notes block", "this episode", or "today's episode".

--- SHOW NOTES (source of truth) ---
{show_notes}
--- END SHOW NOTES ---

--- FINAL PORTION OF THE PARTIAL TRANSCRIPT (continue from exactly here) ---
{tail}
--- END PARTIAL ---"""
    remainder = run_model(prompt, model, timeout)
    return text.rstrip() + "\n\n" + remainder.strip() + "\n"


def basic_shape_check(text: str, ep_num: int) -> None:
    if "[NOVA]:" not in text or "[ALLOY]:" not in text:
        raise RuntimeError("Generated transcript is missing NOVA/ALLOY speaker turns")
    if "[PAUSE]" not in text:
        raise RuntimeError("Generated transcript is missing [PAUSE] pacing tags")
    if re.search(r"\bToby\b", text) and "Toby On Fitness Tech dot com" not in text:
        raise RuntimeError("Generated transcript appears to mention Toby outside the allowed CTA")
    if "/Users/" in text or "build log" in text.lower():
        raise RuntimeError("Generated transcript contains internal path/build-log language")


def _first_product_mention_is_framed(text: str, product_pattern: str) -> bool:
    match = re.search(product_pattern, text, re.IGNORECASE)
    if not match:
        return True
    window = text[max(0, match.start() - 200):match.end() + 200]
    return bool(
        re.search(r"terminal[- ]based", window, re.IGNORECASE)
        and re.search(r"AI coding agent|coding agent", window, re.IGNORECASE)
    )


def _prefix_first_mention(text: str, product_pattern: str, framed_name: str) -> str:
    if _first_product_mention_is_framed(text, product_pattern):
        return text
    return re.sub(product_pattern, framed_name, text, count=1, flags=re.IGNORECASE)


def apply_deterministic_qc_repairs(text: str) -> tuple[str, list[str]]:
    """Fix small wording-gate misses without spending a full model retry.

    The model is still responsible for substantive rewrites, but first-mention
    framing and a recognizable sign-off are deterministic enough to repair in
    place. This keeps the morning pipeline from burning a long model call when
    the draft already passed the hard content checks.
    """
    fixes: list[str] = []
    original = text

    text = _prefix_first_mention(
        text,
        r"\bClaude Code\b",
        "the terminal-based AI coding agent Claude Code",
    )
    if text != original:
        fixes.append("framed first Claude Code mention")
        original = text

    text = _prefix_first_mention(
        text,
        r"\bCodex CLI\b",
        "the terminal-based coding agent Codex CLI",
    )
    if text != original:
        fixes.append("framed first Codex CLI mention")
        original = text

    # check_episode.py rejects full three-part versions spoken aloud (EP082:
    # the slate headline itself carried 'Claude Code CLI 2.1.195', so every
    # model draft failed this gate twice per run). Shorten deterministically:
    # generic semver 'a.b.c' → 'a.b' (skipping longer dotted chains like
    # IPs), then year calver '2026.x.y[.z]' → 'x.y[.z]' to match the allowed
    # shorten_release_tag() form. An already-short calver point tag like
    # '5.29.2' also collapses to '5.29' — a minor fidelity loss that still
    # reads naturally on air.
    text = re.sub(r"(?<![.\d])(\d{1,3}\.\d{1,3})\.\d{1,4}(?![.\d])", r"\1", text)
    text = re.sub(r"\bv?20\d{2}\.(\d+\.\d+(?:\.\d+)?)\b", r"\1", text)
    if text != original:
        fixes.append("shortened full version numbers for speech")
        original = text

    last_500_words = " ".join(text.split()[-500:])
    has_outro = bool(re.search(
        r"(AgentStack Daily|that'?s? (it|all|a wrap)|thanks? for listening|next (time|episode)|see you|I'?m NOVA)",
        last_500_words,
        re.IGNORECASE,
    ))
    if not has_outro:
        closing = re.search(r"we'll be back soon\.?", text, re.IGNORECASE)
        if closing:
            replacement = "Thanks for listening to AgentStack Daily. We'll be back soon."
            start, end = closing.span()
            text = text[:start] + replacement + text[end:]
        else:
            text = text.rstrip() + "\n\n[NOVA]: Thanks for listening to AgentStack Daily. We'll be back soon.\n"
        fixes.append("added recognizable outro sign-off")

    return text, fixes


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate episode transcript from approved show notes")
    parser.add_argument("episode", type=int)
    parser.add_argument("--model", default=DEFAULT_MODEL_SPEC,
                        help=(
                            "OpenClaw model or comma-separated fallback list "
                            f"(default: {DEFAULT_MODEL_SPEC}). Can also set TRANSCRIPT_MODEL or TRANSCRIPT_MODELS."
                        ))
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--attempts", type=int, default=DEFAULT_ATTEMPTS,
                        help="Max generate+QC attempts before giving up (repairs QC failures between attempts)")
    parser.add_argument("--feedback", default="",
                        help="Reviewer audio feedback — revise the existing transcript to address it (implies regeneration)")
    parser.add_argument("--feedback-file", default="",
                        help="Path to a file containing reviewer audio feedback (alternative to --feedback)")
    args = parser.parse_args()

    ep_num = args.episode
    ep_str = f"{ep_num:03d}"
    show_notes_path = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    transcript_path = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript.md"

    listener_feedback = args.feedback.strip()
    if args.feedback_file:
        fb_path = Path(args.feedback_file)
        if not fb_path.exists():
            raise SystemExit(f"Feedback file not found: {fb_path}")
        listener_feedback = (listener_feedback + "\n" + fb_path.read_text(encoding="utf-8", errors="ignore")).strip()

    if not show_notes_path.exists():
        raise SystemExit(f"Missing show notes: {show_notes_path.name}")
    # Feedback means "revise the existing transcript", so it always regenerates.
    if transcript_path.exists() and not args.force and not listener_feedback:
        print(f"Transcript already exists: {transcript_path}")
        return 0

    show_notes = read_text(show_notes_path)
    examples = recent_transcript_excerpt(ep_num)
    transcript_path.parent.mkdir(parents=True, exist_ok=True)

    # When revising from feedback, hand the model the current transcript as the base.
    current_transcript = ""
    if listener_feedback and transcript_path.exists():
        current_transcript = read_text(transcript_path)
        print(f"[EP{ep_str}] Revising existing transcript to address reviewer audio feedback "
              f"({len(listener_feedback)} chars).", flush=True)

    models = parse_models(args.model)
    dead: set[str] = set()
    # QC-repair attempts (a produced draft that failed check_episode.py) are
    # bounded separately from route tries (a provider/transport failure). Dead
    # routes get skipped, not counted against the repair budget.
    max_qc_repairs = max(1, args.attempts)
    max_route_tries = max(len(models) * 3, max_qc_repairs + len(models))
    print(f"[EP{ep_str}] Transcript routes: {', '.join(models)} "
          f"(QC repairs ≤{max_qc_repairs}, route tries ≤{max_route_tries}).", flush=True)

    # A route is only demoted after 2 strikes — a single transient blip
    # (timeout, momentary 5xx, the openclaw state-migration noise) must never
    # permanently kill a known long-form workhorse like MiniMax M3 (EP071,
    # 2026-06-15: one transient demoted MiniMax and left only short-output routes).
    #
    # Locked 2026-07-01 (post-EP078): the voice-match tier (M3) gets an inline
    # backoff probe on a route-fail marker so a momentary provider blip doesn't
    # burn the strike and demote M3 straight into GPT-5.5 (which produces the
    # drone cadence Toby has rejected twice). One retry with 6-12s sleep on the
    # same blip before counting it as strike 1.
    strikes: dict[str, int] = {}
    DEMOTE_AT = 2
    VOICE_MATCH_TIER = {"minimax/MiniMax-M3"}  # add future voice-match models here
    blip_retries: dict[str, int] = {}  # blip-retry budget per model, separate from strikes
    BLIP_RETRY_BUDGET = 2  # up to 2 inline retries on the same blip before counting a strike
    blip_backoff = 6  # seconds; doubles each retry

    def viable() -> list[str]:
        return [m for m in models if m not in dead]

    repair_feedback = ""
    last_tmp_path: Path | None = None
    qc_repairs = 0
    route_tries = 0
    mi = 0

    while qc_repairs < max_qc_repairs and route_tries < max_route_tries:
        vm = viable()
        if not vm:
            print(f"[EP{ep_str}] all routes demoted (provider/auth/quota failures) — cannot generate", flush=True)
            break
        # Revisions ALWAYS go to the best available route (spec order), never
        # the round-robin (locked 2026-07-07, EP082: a gpt-5.5 draft one error
        # from passing was handed to a weaker freecall route for revision,
        # which regressed it to 8 errors and burned three pipeline runs).
        # Rotation only picks the route for fresh drafts; dead-route demotion
        # still advances vm[0] when the best route hard-fails.
        if repair_feedback:
            model = vm[0]
            advanced_mi = False
        else:
            model = vm[mi % len(vm)]
            mi += 1
            advanced_mi = True
        route_tries += 1
        prompt = build_prompt(
            ep_num, show_notes, examples,
            repair_feedback=repair_feedback,
            listener_feedback=listener_feedback,
            current_transcript=current_transcript,
        )
        label = (f"route try {route_tries} via {model}"
                 + (f" (QC repair {qc_repairs + 1}/{max_qc_repairs})" if repair_feedback else ""))
        print(f"[EP{ep_str}] Generating transcript... {label}", flush=True)

        try:
            text = run_model(prompt, model, args.timeout)
        except RuntimeError as exc:
            msg = str(exc).lower()
            if any(marker in msg for marker in ROUTE_FAIL_MARKERS):
                # Voice-match tier (M3) gets an inline backoff probe on blips so
                # a momentary provider hiccup doesn't burn a strike. EP078
                # blipped M3 twice in a row at 30s apart, demoted it, and the
                # fallback to GPT-5.5 produced the same drone Toby rejected in
                # EP076. Retry the same call up to BLIP_RETRY_BUDGET times with
                # exponential backoff before counting strike 1.
                if model in VOICE_MATCH_TIER and blip_retries.get(model, 0) < BLIP_RETRY_BUDGET:
                    sleep_s = blip_backoff * (2 ** blip_retries.get(model, 0))
                    blip_retries[model] = blip_retries.get(model, 0) + 1
                    print(f"[EP{ep_str}] route {model} blipped — probing voice-match "
                          f"tier with {sleep_s}s backoff (blip-retry "
                          f"{blip_retries[model]}/{BLIP_RETRY_BUDGET}, no strike "
                          f"counted): {str(exc)[:120]}", flush=True)
                    import time
                    time.sleep(sleep_s)
                    # Roll back route_tries (and mi if the round-robin
                    # advanced) so this attempt is free.
                    route_tries -= 1
                    if advanced_mi:
                        mi -= 1
                    continue
                strikes[model] = strikes.get(model, 0) + 1
                if strikes[model] >= DEMOTE_AT:
                    dead.add(model)
                    print(f"[EP{ep_str}] route {model} unusable ({str(exc)[:120]}) — demoting after "
                          f"{strikes[model]} strikes (no QC-repair consumed)", flush=True)
                else:
                    print(f"[EP{ep_str}] route {model} blipped ({str(exc)[:120]}) — strike "
                          f"{strikes[model]}/{DEMOTE_AT}, will retry it (no QC-repair consumed)", flush=True)
                # mi already advanced at loop top → next iteration tries another route
                continue
            # Non-route generation problem — treat as a repairable shape failure.
            repair_feedback = f"Generation/shape failure: {exc}"
            qc_repairs += 1
            print(f"[EP{ep_str}] {label} failed before QC: {exc}", flush=True)
            continue

        # Truncated draft (model hit its output ceiling mid-episode, so the
        # closing phrase is missing from the tail) — splice on a continuation that
        # finishes the remaining stories and the outro, fixing the length and
        # missing-outro QC failures in one shot. Gated on the missing-closing
        # signal (not raw word count) so a complete-but-short draft is not given a
        # second outro.
        try:
            if looks_truncated(text):
                print(f"[EP{ep_str}] {label}: draft is {len(text.split())} words and missing the "
                      f"closing phrase — splicing a continuation.", flush=True)
                text = complete_truncated_draft(text, ep_num, show_notes, model, args.timeout)
        except RuntimeError as exc:
            print(f"[EP{ep_str}] {label}: continuation splice failed ({str(exc)[:120]}); "
                  f"continuing with the partial", flush=True)

        text, deterministic_fixes = apply_deterministic_qc_repairs(text)
        if deterministic_fixes:
            print(f"[EP{ep_str}] {label}: applied deterministic QC repair(s): "
                  f"{', '.join(deterministic_fixes)}.", flush=True)
        try:
            basic_shape_check(text, ep_num)
        except RuntimeError as exc:
            repair_feedback = f"Generation/shape failure: {exc}"
            current_transcript = text
            qc_repairs += 1
            print(f"[EP{ep_str}] {label} failed basic shape check: {exc}", flush=True)
            continue

        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=str(transcript_path.parent), delete=False,
            prefix=f".episode_{ep_str}_transcript.", suffix=".tmp",
        ) as tmp:
            tmp.write(text)
            tmp_path = Path(tmp.name)

        qc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "check_episode.py"), str(tmp_path)],
            cwd=str(PODCAST_DIR), capture_output=True, text=True,
        )
        if qc.stdout:
            print(qc.stdout, flush=True)
        if qc.stderr:
            print(qc.stderr, file=sys.stderr, flush=True)

        if qc.returncode == 0:
            tmp_path.replace(transcript_path)
            print(f"[EP{ep_str}] Transcript written: {transcript_path} ({label})", flush=True)
            return 0

        # QC rejected the draft — hand the model its OWN failed draft to revise
        # (targeted edits keep what already passed) and consume one QC repair.
        qc_text = (qc.stdout or "") + ("\n" + qc.stderr if qc.stderr else "")
        fail_lines = [ln for ln in qc_text.splitlines() if "❌" in ln or "→" in ln]
        repair_feedback = "\n".join(fail_lines).strip() or qc_text.strip()
        current_transcript = text
        if not listener_feedback:
            listener_feedback = "Fix only the QC failures listed below; keep the rest of the draft intact."
        qc_repairs += 1
        rejected_path = transcript_path.parent / f".episode_{ep_str}_transcript.rejected.latest.tmp"
        tmp_path.replace(rejected_path)
        last_tmp_path = rejected_path
        print(f"[EP{ep_str}] {label} failed check_episode.py; will revise to fix "
              f"{len(fail_lines)} issue(s) and retry.", flush=True)

    raise SystemExit(
        f"Generated transcript still failing after {qc_repairs} QC repair(s) / {route_tries} route tries "
        f"(dead routes: {sorted(dead) or 'none'})."
        + (f" Kept last draft at {last_tmp_path}" if last_tmp_path else "")
    )


if __name__ == "__main__":
    raise SystemExit(main())
