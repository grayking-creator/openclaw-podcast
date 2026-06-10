#!/usr/bin/env python3
"""Generate an AgentStack Daily transcript from approved show notes.

This is the explicit show-notes -> transcript artifact step used before
build_episode.py. It calls OpenClaw's configured OpenAI text model directly;
it does not spawn nested OpenClaw agents or background workers.

Environment variables:
  TRANSCRIPT_MODEL   Override the default model (e.g. openai/gpt-5.5,
                     minimax/MiniMax-M3, etc.). Model must support
                     ~8k-10k output tokens for 6,000+ word transcripts.
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
DEFAULT_MODEL = os.environ.get("TRANSCRIPT_MODEL", "minimax/MiniMax-M3")
# How many times to (re)generate when the model produces a draft that fails
# check_episode.py. Each retry feeds the exact QC failures back to the model so
# it repairs them, instead of reporting a failure right after a successful
# generation and leaving a half-built .tmp for a human/agent to salvage.
# Override with TRANSCRIPT_GEN_ATTEMPTS.
DEFAULT_ATTEMPTS = max(1, int(os.environ.get("TRANSCRIPT_GEN_ATTEMPTS", "3")))


def read_text(path: Path, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8")
    return text if limit is None else text[:limit]


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
- The transcript must be at least 5,000 words and should land around 5,200 to 6,500 words — tight and dense, not padded. Expand each story with concrete mechanisms, examples, tradeoffs, capabilities, and real-world reactions — NOT with tests or checklists.
- If reviewer feedback says the episode is "too long", "too much homework", or "do this then do that", that means cut the procedural/test/checklist content and front-loaded operational slog — it does NOT mean drop below the 5,000-word floor. Replace every removed test/checklist block with informational substance: what the thing is, how you actually use it, what it provides, who is using it and how it is landing, and where vendor claims still need confirmation. Keep workflow/capability language dense and avoid lingering on file/document/copy/move/record plumbing.
- Do not make the episode feel like homework. Avoid repeated "run this test", "here is the checklist", "recommended test", or "try this drill" framing. Use checks sparingly only where they explain real migration risk or observed breakage. For model releases, prioritize capabilities, improvement size, real-world reaction, what people are doing with it, and where vendor claims still need independent confirmation.
- If the show notes contain user feedback that a prior draft felt like "do this, then do that" homework, rebuild the structure from scratch. The episode should feel informational and opinionated, not like a migration checklist. Keep the agent-harness coverage concise and informational — do not spend the first 20 minutes on operational validation/tests.
- Do not pad the ending with repeated summaries, repeated "one extra detail" blocks, or near-identical practical-move paragraphs. Every paragraph must advance the episode.
- CLI/agent release coverage = released stable tags ONLY. Do not narrate dist-tags like "npm latest" vs the Anthropic "stable" channel, do not compare "received via update" vs "latest available," and do not frame a story around a package bump or a channel republish. If the only news for a CLI is a dist-tag republish, it is not a story — drop it or skip the segment. Spoken transcript must never say "npm latest" or "received via update" or "latest versus received" for any CLI/agent release.
- Claude Code is a terminal-based AI coding agent. Refer to it in the spoken intro and in any segment about it as "the terminal-based AI coding agent Claude Code" (or equivalent — the words "terminal-based" + "AI coding agent" must appear together the first time it is named per episode). Codex CLI / rust-v0.138.0 is similarly a terminal-based coding agent — say so the first time it is named. Do not introduce either product as a bare "CLI" without that framing.

REQUIRED STRUCTURE — the episode must ALWAYS start with the agent-harness updates, then move to model/other stories (follow this exact order):
1. Opening hook (~150-200 words, before the first timestamped segment): in the first two sentences, name the agent-harness release(s) in SHORTENED form (e.g. OpenClaw "5.28", Claude Code ".159", never "v2026.5.28") and state at least two concrete changes using verbs like added/fixed/tightened/introduced, naming concrete surfaces (sessions, plugins, auth, browser, cron, provider, etc.). No abstract "today we connect the dots" framing.
2. First timestamped segment(s) = the agent-harness updates — OpenClaw, OpenAI Codex, Claude Code CLI, and Hermes Agent wherever they changed this cycle. This is ALWAYS the front of the episode. Deliver it as INFORMATIONAL news: what changed, what it provides, how you actually use it, and real-world reactions/breakage — NOT a list of "run this test, then run that." Keep it concise and dense; do not let it sprawl into operational validation.
3. After the harness updates, cover the flagship model story (the biggest model drop in the show notes, e.g. MiniMax M3) and then the other slate stories in show-note order — same informational depth: what it is, how you use it, what it provides, who is using it and how it is landing, and where vendor claims still need confirmation.
4. The agent-harness updates lead; the model/news stories follow. Never open the episode on a non-harness story.
- HARD: the spoken transcript must name every covered release in SHORTENED form (e.g. "5.28") within the first 320 words — never the full "v2026.5.28".
- HARD: total length 5,200-6,500 words (never below 5,000). If you are short, deepen the model/capability stories with real-world reactions — never by adding tests.
- HARD: end with the show-notes CTA and the EXACT phrase "We'll be back soon." Never "we'll be back next week".
- HARD: never write the words "story slate" or "show notes block" in the spoken transcript, and never write a full version like "2.1.159" or "v2026.5.28" — use the shortened spoken form (".159", "5.28").

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


def run_model(prompt: str, model: str, timeout: int) -> str:
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
                detail = tail_text(stderr_path) or tail_text(stdout_path) or "no output"
                raise RuntimeError(
                    f"Transcript model generation timed out after {timeout}s: {detail[:1600]}"
                ) from exc

        stdout = stdout_path.read_text(encoding="utf-8", errors="ignore")
        stderr = tail_text(stderr_path)

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


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate episode transcript from approved show notes")
    parser.add_argument("episode", type=int)
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"OpenClaw model (default: {DEFAULT_MODEL}). Can also set TRANSCRIPT_MODEL env var.")
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

    attempts = max(1, args.attempts)
    repair_feedback = ""
    last_tmp_path: Path | None = None

    for attempt in range(1, attempts + 1):
        prompt = build_prompt(
            ep_num, show_notes, examples,
            repair_feedback=repair_feedback,
            listener_feedback=listener_feedback,
            current_transcript=current_transcript,
        )
        label = f"attempt {attempt}/{attempts}" + (" (repairing prior QC failures)" if repair_feedback else "")
        print(f"[EP{ep_str}] Generating transcript with {args.model}... {label}", flush=True)

        try:
            text = run_model(prompt, args.model, args.timeout)
            if looks_truncated(text) and len(text.split()) >= 3000:
                print(f"[EP{ep_str}] {label}: draft truncated at {len(text.split())} words — "
                      f"generating continuation and splicing.", flush=True)
                text = complete_truncated_draft(text, ep_num, show_notes, args.model, args.timeout)
            basic_shape_check(text, ep_num)
        except RuntimeError as exc:
            # Generation or basic-shape problem — treat as a repairable failure.
            repair_feedback = f"Generation/shape failure: {exc}"
            print(f"[EP{ep_str}] {label} failed before QC: {exc}", flush=True)
            continue

        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=str(transcript_path.parent),
            delete=False,
            prefix=f".episode_{ep_str}_transcript.",
            suffix=".tmp",
        ) as tmp:
            tmp.write(text)
            tmp_path = Path(tmp.name)

        qc = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "check_episode.py"), str(tmp_path)],
            cwd=str(PODCAST_DIR),
            capture_output=True,
            text=True,
        )
        # Keep QC observable in the build/audio log as before.
        if qc.stdout:
            print(qc.stdout, flush=True)
        if qc.stderr:
            print(qc.stderr, file=sys.stderr, flush=True)

        if qc.returncode == 0:
            tmp_path.replace(transcript_path)
            print(f"[EP{ep_str}] Transcript written: {transcript_path} ({label})", flush=True)
            return 0

        # QC rejected the draft — feed the concrete failures back for repair, and
        # hand the model its OWN failed draft to revise (targeted edits) instead of
        # rerolling from scratch, which oscillates: fixes named issues but breaks
        # others. Revising the draft keeps what already passed.
        qc_text = (qc.stdout or "") + ("\n" + qc.stderr if qc.stderr else "")
        fail_lines = [ln for ln in qc_text.splitlines() if "❌" in ln or "→" in ln]
        repair_feedback = "\n".join(fail_lines).strip() or qc_text.strip()
        current_transcript = text
        if not listener_feedback:
            # No reviewer feedback set; synthesize a minimal revision directive so the
            # failed draft is still shown to the model as the base to revise.
            listener_feedback = "Fix only the QC failures listed below; keep the rest of the draft intact."
        last_tmp_path = tmp_path
        print(f"[EP{ep_str}] {label} failed check_episode.py; will revise this draft to fix {len(fail_lines)} issue(s) and retry.", flush=True)

        # Don't accumulate temp drafts across attempts; keep only the final one.
        if attempt < attempts:
            tmp_path.unlink(missing_ok=True)
            last_tmp_path = None

    raise SystemExit(
        f"Generated transcript still failed check_episode.py after {attempts} attempt(s)."
        + (f" Kept last draft at {last_tmp_path}" if last_tmp_path else "")
    )


if __name__ == "__main__":
    raise SystemExit(main())
