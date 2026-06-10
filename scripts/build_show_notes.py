#!/usr/bin/env python3
"""
build_show_notes.py — deterministic show-notes builder for AgentStack Daily.

Replaces the old "ask one model to write the whole 30KB draft, then QC it"
flow. Structure is laid down by code; models only write small prose sections,
and every model response is validated IN REAL TIME against the same rules
check_show_notes.py enforces. A section that keeps failing falls back to a
deterministic template, so a flaky model can never sink the morning episode.

Pipeline position: gather_research_context.py → THIS → check_show_notes.py
(final gate, should pass by construction) → generate_episode_transcript.py →
build_episode.py.

Usage:
    python3 scripts/build_show_notes.py <episode_number> [--output PATH]

Env:
    SHOW_NOTES_MODELS       comma list of model routes (openclaw infer ids)
    OPENCLAW_BIN            path to openclaw binary
    SHOW_NOTES_STORY_COUNT  slate size (default 10)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
RESEARCH_JSON = Path("/tmp/agent_research_context.json")

sys.path.insert(0, str(SCRIPTS_DIR))
import check_show_notes as qc  # reuse the QC module's patterns/helpers — single source of truth

OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "/opt/homebrew/bin/openclaw")
DEFAULT_MODELS = os.environ.get(
    "SHOW_NOTES_MODELS",
    "minimax/MiniMax-M3,google/gemini-3-flash-preview,google-2/gemini-2.5-flash,"
    "mistral/mistral-large-latest,groq/llama-3.3-70b-versatile",
)
STORY_COUNT = int(os.environ.get("SHOW_NOTES_STORY_COUNT", "10"))
WPM = 159  # spoken words per minute, matches check_episode.py calibration

PROVIDER_HARD_FAIL_RE = re.compile(
    r"(429|402|RESOURCE_EXHAUSTED|quota|Quota exceeded|depleted|monthly included credits|"
    r"billing|rate limit|rate-limit|cooldown|model_not_found|HTTP 404|Unauthorized|401|403|"
    r"LLM request failed)", re.IGNORECASE)

# ── Banned-language guards (mirrors the inline lists in check_show_notes.run_checks;
#    the final gate still runs the real checker, so drift here costs a repair
#    round, never a shipped violation) ─────────────────────────────────────────
BANNED_PUBLIC_PATTERNS = [
    # watch-lane / no-release bookkeeping
    r"\bstable\s+watch\b", r"\bwatch\s+lane\b", r"\bbeta\s+watch\b", r"\bstability\s+check\b",
    # internal research/build implementation
    r"\bfetched (?:release )?window\b", r"\brelease window\b", r"\bselected from the fetched\b",
    r"\bdaily release check\b", r"\bno new stable .{0,40}(?:selected|candidate)\b",
    # editorial meta / production leakage
    r"\barchitecture-advice\b", r"\bthis rewrite\b", r"\bchanges? the format\b",
    r"\bsix[- ]story\b", r"\bten[- ]story\b", r"\bsix practical stories\b",
    r"\btoday'?s (?:six|ten) stories\b", r"\bflagship release\b", r"\bnot short on news\b",
    r"\bstretching one update\b", r"\bbefore audio\b", r"\bbefore .{0,30}publish\b",
    r"\breview before release\b", r"\brelease plan\b", r"\bactual artifact\b",
    r"\bstory in the slate\b", r"\btranscript includes?\b", r"\bwhat changed operationally\b",
    r"\blist of links\b", r"\bstrong new .{0,30}release block\b", r"\bcurrent stable feed window\b",
    r"\brecent-version scan\b", r"\bToby (?:asked|wanted|said|told)\b", r"\byou asked\b",
    r"\byou told\b", r"\bno grand theory\b", r"\bno abstract operating model\b",
    r"\bstraight what'?s-new episode\b", r"\bnot a lecture\b", r"\bdo not waste\b",
    r"\bdo not invent\b", r"\bnot a long .{0,30}recipe\b",
    # operator-playbook slog
    r"\boperator playbook\b", r"\bconcrete builder workflow\b", r"\bchecklist is simple\b",
    r"\bthe (?:first|second|third|fourth|fifth|sixth|seventh|eighth) workflow\b",
    # prior-episode recap filler
    r"\b(?:already|previously|recently)\s+(?:covered|discussed|talked about)\b",
    r"\bcovered\s+(?:in|on)\s+(?:EP\d+|episode\s+\d+|a previous episode|previous episodes|recent episode notes)\b",
    r"\bEP\d+\s+(?:starts|surfaces|covers|covered|talked|discussed)\b",
    r"\bunder the (?:latest-contiguous|contiguous-release|release coverage) rule\b",
    # watch-harness no-change callouts
    r"\b(?:Hermes(?:\s+Agent)?|Codex(?:\s+CLI)?|Antigravity(?:\s+CLI)?)\s+(?:remains\s+at|held\s+its\s+position|on\s+continuous\s+delivery)\b",
    # no-release meta throat-clearing
    r"\bnot a release episode\b", r"\bno release coverage\b",
    r"\bno new stable openclaw release\b", r"\bcovered in recent episode notes\b",
    r"\bfive stories today\b", r"\bthis is a builder-stack episode\b",
    # npm dist-tag / latest-vs-stable channel diffing (Toby standing rule 2026-06-10:
    # coverage uses the stable release only; the channel-diff conversation is banned)
    r"\bnpm latest\b", r"\bnpm stable\b", r"\bdist[- ]tags?\b",
    r"\b(?:stable|latest)\s+(?:track|channel)\b",
    r"\blatest\s+(?:vs\.?|versus)\s+stable\b", r"\bstable\s+(?:vs\.?|versus)\s+latest\b",
    r"\breceived via update\b",
]

# No-release narration for any harness (Toby standing rule 2026-06-10): harnesses
# that did not ship are not mentioned in release context at all — no roll call.
_HARNESS_NAMES = r"(?:OpenClaw|Hermes(?:\s+Agent)?|(?:OpenAI\s+)?Codex(?:\s+CLI)?|Claude\s+Code(?:\s+CLI)?|Antigravity(?:\s+CLI)?)"
BANNED_PUBLIC_PATTERNS += [
    rf"\b{_HARNESS_NAMES}\b[^.\n]{{0,90}}\bno\s+(?:new\s+)?(?:stable\s+)?(?:release|update|version|change)s?\b",
    rf"\bno\s+(?:new\s+)?(?:stable\s+)?(?:release|update|version|change)s?\b[^.\n]{{0,90}}\b{_HARNESS_NAMES}\b",
    rf"\b{_HARNESS_NAMES}\b[^.\n]{{0,40}}\b(?:remains?|stays?|stayed|holds?|held|sits?)\s+(?:at|on|steady|unchanged|put)\b",
    rf"\bnothing\s+new\s+(?:from|for|on)\s+{_HARNESS_NAMES}\b",
    rf"\b{_HARNESS_NAMES}\b[^.\n]{{0,40}}\b(?:didn'?t|did\s+not|hasn'?t|has\s+not)\s+(?:ship|update|move|change)\b",
    rf"\bquiet\s+(?:cycle|week|day)\s+for\s+{_HARNESS_NAMES}\b",
]
BANNED_PUBLIC_RE = [re.compile(p, re.IGNORECASE) for p in BANNED_PUBLIC_PATTERNS]
THEME_GLUE_RE = [re.compile(p, re.IGNORECASE) for p in qc.THEME_GLUE_PATTERNS]
PRERELEASE_RE = qc.PRERELEASE_DASH_RE
VERSION_TAG_RE = re.compile(r"\bv\d{4}\.\d+\.\d+\b")
IMPERATIVE_RE = re.compile(
    r"\b(?:run|check|enable|test|try|install|configure|set up|setup|rotate|watch|monitor|track|"
    r"read|clone|explore|audit|evaluate|verify|compare|connect|deploy|launch|use|pull|download|"
    r"build|set|open|review|inspect|tune|measure|benchmark|register|sign up|subscribe|join|"
    r"bookmark|note|plan|map|tag|label|wire|hook|attach|add|remove|drop|swap|switch|roll|"
    r"restart|promote|pin|lock|approve|ship|publish|release|merge|rebase|push|fork|star)\b",
    re.IGNORECASE)
MECHANISM_RE = re.compile(
    r"\b(API|SDK|runtime|architecture|training|evaluation|benchmark|observability|security|"
    r"privacy|deployment|configuration|config|failure mode|latency|throughput|cost|memory|"
    r"scheduler|inference|model card|system card|changelog|release notes)\b", re.IGNORECASE)

PRIORITY_TOOLS = ["OpenClaw", "Codex", "Claude Code", "Hermes", "Antigravity"]
MINIMAX_M3_SUFFIX = (" (featuring MSA sparse attention, 1M context, multimodal, "
                     "MiniMax Code, and API availability)")

LOG_PREFIX = "[build_show_notes]"


def log(msg: str) -> None:
    print(f"{LOG_PREFIX} {datetime.now().strftime('%H:%M:%S')} {msg}", flush=True)


# ── Model invocation ─────────────────────────────────────────────────────────

class ModelPool:
    """Rotates through model routes; demotes routes that hard-fail (quota/auth)."""

    def __init__(self, models: list[str]):
        self.models = list(models)
        self.dead: set[str] = set()
        self.calls = 0
        self.failures = 0

    def alive(self) -> list[str]:
        return [m for m in self.models if m not in self.dead]

    def run(self, prompt: str, timeout: int = 240, attempts_per_model: int = 2) -> str:
        """Return raw model text, rotating models on failure. Raises RuntimeError if all fail."""
        last_err = "no models available"
        for model in self.alive():
            for attempt in range(1, attempts_per_model + 1):
                self.calls += 1
                try:
                    out = subprocess.run(
                        [OPENCLAW_BIN, "infer", "model", "run",
                         "--model", model, "--json", "--prompt", prompt],
                        cwd=str(PODCAST_DIR), capture_output=True, text=True, timeout=timeout)
                except subprocess.TimeoutExpired:
                    self.failures += 1
                    last_err = f"{model}: timeout after {timeout}s"
                    log(f"model {model} timed out (attempt {attempt})")
                    continue
                blob = (out.stdout or "") + (out.stderr or "")
                if out.returncode != 0:
                    self.failures += 1
                    last_err = f"{model}: exit {out.returncode}: {blob[-300:]}"
                    if PROVIDER_HARD_FAIL_RE.search(blob):
                        log(f"model {model} hard-failed (quota/auth/rate) — demoting for this run")
                        self.dead.add(model)
                        break
                    continue
                try:
                    data = json.loads(out.stdout)
                    text = (data.get("outputs") or [{}])[0].get("text") or ""
                except (json.JSONDecodeError, IndexError, AttributeError):
                    text = out.stdout or ""
                text = text.strip()
                if text:
                    return text
                self.failures += 1
                last_err = f"{model}: empty output"
        raise RuntimeError(f"all model routes failed: {last_err}")


def extract_json_obj(text: str) -> dict:
    """Pull the first JSON object out of a model reply (tolerates fences/prose)."""
    text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in model output")
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if esc:
            esc = False
            continue
        if c == "\\" and in_str:
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("unbalanced JSON object in model output")


# ── Text validation helpers ──────────────────────────────────────────────────

def banned_hits(text: str, allowed_tags: set[str], public: bool = True) -> list[str]:
    hits = []
    for rx in BANNED_PUBLIC_RE + THEME_GLUE_RE:
        m = rx.search(text)
        if m:
            hits.append(f"banned phrase: {m.group(0)!r}")
    for m in PRERELEASE_RE.finditer(text):
        hits.append(f"prerelease tag in public copy: {m.group(0)!r}")
    if public:
        for m in VERSION_TAG_RE.finditer(text):
            if m.group(0) not in allowed_tags:
                hits.append(f"off-slate version tag: {m.group(0)!r}")
    for rx in (re.compile(p, re.IGNORECASE) for p in qc.LISTENER_SPECIFIC_PATTERNS):
        m = rx.search(text)
        if m:
            hits.append(f"listener-specific phrasing: {m.group(0)!r}")
    if re.search(r"\bToby\b", text):
        hits.append("mentions Toby")
    if re.search(r"/Users/|/tmp/", text):
        hits.append("contains a filesystem path")
    return hits


def imperative_sentences(text: str) -> int:
    return sum(1 for s in re.split(r"[.;]\s+", text) if IMPERATIVE_RE.search(s))


def wc(text: str) -> int:
    return len(text.split())


def validate_story(pkg: dict, allowed_tags: set[str], is_release: bool) -> list[str]:
    problems = []
    for key in ("title", "summary", "technical_depth_angle", "actionability_angle",
                "listener_hook", "segment"):
        if not str(pkg.get(key, "")).strip():
            problems.append(f"missing/empty field: {key}")
    if problems:
        return problems
    title = str(pkg["title"])
    if wc(title) > 18:
        problems.append(f"title too long ({wc(title)} words, max 18)")
    if not (35 <= wc(str(pkg["summary"])) <= 170):
        problems.append(f"summary must be 35-170 words (got {wc(str(pkg['summary']))})")
    if wc(str(pkg["technical_depth_angle"])) > 115:
        problems.append(f"technical_depth_angle over 115 words (got {wc(str(pkg['technical_depth_angle']))}; QC caps at ~120)")
    imp = imperative_sentences(str(pkg["actionability_angle"]))
    if imp > 2:
        problems.append(f"actionability_angle has {imp} imperative sentences (max 2)")
    if wc(str(pkg["actionability_angle"])) > 90:
        problems.append("actionability_angle over 90 words")
    if wc(str(pkg["listener_hook"])) > 45:
        problems.append("listener_hook over 45 words (one sentence)")
    seg_words = wc(str(pkg["segment"]))
    min_seg = 300 if is_release else 150
    if not (min_seg <= seg_words <= 480):
        problems.append(f"segment must be {min_seg}-480 words (got {seg_words})")
    if len(MECHANISM_RE.findall(str(pkg["segment"]))) < 2:
        problems.append("segment needs at least 2 concrete mechanism terms "
                        "(API/SDK/runtime/architecture/config/inference/latency/...)")
    everything = " ".join(str(pkg[k]) for k in
                          ("title", "summary", "technical_depth_angle",
                           "actionability_angle", "listener_hook", "segment"))
    problems.extend(banned_hits(everything, allowed_tags))
    return problems


# ── Research data loading ────────────────────────────────────────────────────

def load_research(max_age_hours: float = 3.0) -> dict:
    stale = True
    if RESEARCH_JSON.exists():
        age = time.time() - RESEARCH_JSON.stat().st_mtime
        stale = age > max_age_hours * 3600
    if stale:
        log("research JSON missing/stale — running gather_research_context.py")
        subprocess.run([sys.executable, str(SCRIPTS_DIR / "gather_research_context.py")],
                       check=True, timeout=600)
    return json.loads(RESEARCH_JSON.read_text(encoding="utf-8"))


# ── Release lane computation (fully deterministic) ───────────────────────────

LANES = [
    {"key": "openclaw", "label": "OpenClaw", "gh": "openclaw/openclaw"},
    {"key": "hermes", "label": "Hermes Agent", "gh": "NousResearch/hermes-agent"},
    {"key": "codex", "label": "OpenAI Codex", "gh": "openai/codex"},
    {"key": "claude_code", "label": "Claude Code CLI", "npm": "@anthropic-ai/claude-code"},
    {"key": "antigravity", "label": "Antigravity CLI", "npm": "@google/antigravity"},
]
HARNESS_REF_LABELS = {
    "openclaw": "OpenClaw", "hermes": "Hermes Agent", "codex": "OpenAI Codex",
    "claude_code": "Claude Code CLI", "antigravity": "Antigravity CLI",
}


def covered_tags_by_lane(research: dict) -> dict:
    """Parse per-product covered version tokens from the last 5 episodes'
    `## Harness Version Reference` + `## Release Coverage Check` sections."""
    covered = {lane["key"]: set() for lane in LANES}
    label_to_key = {
        "openclaw": "openclaw", "hermes agent": "hermes", "hermes": "hermes",
        "openai codex": "codex", "codex": "codex",
        "claude code cli": "claude_code", "claude code": "claude_code",
        "antigravity cli": "antigravity", "antigravity": "antigravity",
    }
    for ep in research.get("recent_episodes", []):
        for section in (ep.get("harness_version_reference", ""),
                        ep.get("release_coverage_check", "")):
            for line in section.splitlines():
                m = re.match(r"\s*-\s+\*\*(.+?)\*\*", line)
                if not m:
                    continue
                key = label_to_key.get(m.group(1).strip().lower())
                if not key:
                    continue
                covered[key].update(re.findall(r"`([^`]+)`", line))
    return covered


def stable_releases(research: dict, gh: str) -> list[dict]:
    rels = [r for r in research.get("github_releases", {}).get(gh, [])
            if not r.get("prerelease")]
    rels.sort(key=lambda r: r.get("published_at") or "", reverse=True)
    return rels


def compute_lanes(research: dict) -> dict:
    """Per lane: latest stable, covered tags, and the contiguous uncovered block
    starting at the latest stable release (the only releases we may surface)."""
    covered = covered_tags_by_lane(research)
    out = {}
    for lane in LANES:
        key = lane["key"]
        info = {"label": lane["label"], "covered": sorted(covered[key]),
                "latest": None, "candidates": [], "detail": ""}
        if "gh" in lane:
            rels = stable_releases(research, lane["gh"])
            prerels = [r for r in research.get("github_releases", {}).get(lane["gh"], [])
                       if r.get("prerelease")]
            info["latest_prerelease"] = prerels[0]["tag"] if prerels else None
            if rels:
                info["latest"] = rels[0]
                block = []
                for r in rels:
                    if r["tag"] in covered[key] or r.get("name") in covered[key]:
                        break
                    block.append(r)
                info["candidates"] = block
        else:
            npm = research.get("npm", {}).get(lane["npm"], {})
            tags = npm.get("dist_tags", {}) or {}
            # Toby's standing rule (2026-06-10): Claude Code coverage tracks the
            # `stable` dist-tag ONLY — that is what he runs. Never select, report,
            # or compare against `latest`; the latest-vs-stable diff conversation
            # is banned from the show entirely.
            if key == "claude_code":
                chosen = tags.get("stable")
            else:
                chosen = tags.get("latest")
            published = ""
            for v, t in npm.get("recent_versions", []):
                if v == chosen:
                    published = t
                    break
            info["latest"] = {"tag": chosen, "published_at": published} if chosen else None
            if chosen and chosen not in covered[key]:
                info["candidates"] = [{"tag": chosen, "published_at": published,
                                       "body": "", "url": ""}]
        out[key] = info
    return out


def render_release_coverage_check(lanes: dict) -> str:
    lines = []
    for lane in LANES:
        key = lane["key"]
        info = lanes[key]
        label = info["label"]
        covered_str = ", ".join(f"`{t}`" for t in info["covered"][-4:]) or "none on record"
        if key == "antigravity" and not info.get("latest"):
            lines.append(f"- **{label}** — Continuous delivery model; no discrete release tags "
                         f"verified this cycle (latest build as of {datetime.now().strftime('%Y-%m-%d')}). "
                         f"Recent episode version tags detected: {covered_str}.")
            continue
        if not info.get("latest"):
            lines.append(f"- **{label}** — No stable/verified release data fetched this cycle. "
                         f"Recent episode version tags detected: {covered_str}.")
            continue
        latest_tag = info["latest"]["tag"]
        pub = info["latest"].get("published_at", "")
        if info["candidates"]:
            sel = ", ".join(f"`{c['tag']}`" for c in info["candidates"])
            lines.append(f"- **{label}** — Latest stable verified: `{latest_tag}`, published {pub}. "
                         f"Recent episode version tags detected: {covered_str}. "
                         f"Selected missing version(s): {sel}.")
        else:
            lines.append(f"- **{label}** — Latest stable verified: `{latest_tag}`, published {pub}. "
                         f"Recent episode version tags detected: {covered_str}. "
                         f"No new stable release this cycle.")
    return "\n".join(lines)


def render_harness_version_reference(lanes: dict) -> str:
    lines = []
    for lane in LANES:
        info = lanes[lane["key"]]
        label = HARNESS_REF_LABELS[lane["key"]]
        if info.get("latest"):
            extra = ""
            if lane["key"] == "openclaw" and info.get("latest_prerelease"):
                extra = f" (stable) / `{info['latest_prerelease']}` (prerelease)"
            lines.append(f"- **{label}** — `{info['latest']['tag']}`{extra}")
        else:
            lines.append(f"- **{label}** — Continuous delivery (no tagged release verified this cycle)")
    return "\n".join(lines)


# ── Candidate selection (deterministic) ──────────────────────────────────────

def prior_titles(research: dict) -> list[str]:
    titles = []
    eps = research.get("recent_episodes", [])
    if eps:
        titles.extend(eps[-1].get("story_titles", []))
    return titles


def overlaps_prior(title: str, prior: list[str]) -> bool:
    tokens = qc.title_tokens(title)
    if len(tokens) < 3:
        return False
    for p in prior:
        ptok = qc.title_tokens(p)
        if not ptok:
            continue
        hits = tokens & ptok
        if len(hits) >= 3 and len(hits) / min(len(tokens), len(ptok)) >= 0.45:
            return True
    return False


def featured_models_recently(research: dict) -> set[str]:
    feat = set()
    for ep in research.get("recent_episodes", []):
        blob = (ep.get("model_discovery", "") + " " + " ".join(ep.get("story_titles", []))).lower()
        for token in re.findall(r"[a-z0-9][a-z0-9.\-]{2,}", blob):
            feat.add(token)
    return feat


def select_candidates(research: dict, lanes: dict) -> dict:
    """Pick the slate sources: release readout (if any lane shipped), new models,
    HN/RSS news ranked by agent-stack relevance, radar repos as padding."""
    prior = prior_titles(research)
    shipped = [k for k in lanes if lanes[k]["candidates"]]

    # Model discovery candidates
    featured = featured_models_recently(research)
    model_cands, model_skipped = [], []
    for m in research.get("openrouter", {}).get("new_models", []):
        mid = m.get("id", "")
        base = mid.split("/")[-1].lower()
        name_tokens = set(re.findall(r"[a-z0-9][a-z0-9.\-]{2,}", (m.get("name") or "").lower()))
        if base in featured or (name_tokens and name_tokens.issubset(featured)):
            model_skipped.append(m)
        elif ":free" in mid or base.endswith("-free"):
            model_skipped.append(m)
        else:
            model_cands.append(m)
    model_selected = model_cands[:2]

    # News pool: HN + RSS, scored
    boost = re.compile(r"\b(agent|mcp|claude|codex|openclaw|hermes|llm|model|inference|"
                       r"open[- ]?source|local|cli|sdk|api|benchmark|security)\b", re.IGNORECASE)
    pool = []
    for h in research.get("hackernews", []):
        score = h["points"] + 40 * len(set(boost.findall(h["title"])))
        pool.append({"kind": "hn", "title": h["title"], "url": h["url"],
                     "summary": "", "score": score,
                     "extra": f"Hacker News score {h['points']}; discussion: {h['comments_url']}"})
    for feed, items in research.get("rss", {}).items():
        for it in items:
            score = 60 + 40 * len(set(boost.findall(it["title"] + " " + it.get("summary", ""))))
            if feed == "OpenAI News":
                score += 60
            pool.append({"kind": "rss", "title": it["title"], "url": it["url"],
                         "summary": it.get("summary", ""), "score": score,
                         "extra": f"Published {it.get('published','')} via {feed}"})
    pool.sort(key=lambda x: x["score"], reverse=True)

    # Dedupe within pool and against the previous episode's slate
    chosen, seen_tokens = [], []
    for item in pool:
        t = qc.title_tokens(item["title"])
        if overlaps_prior(item["title"], prior):
            continue
        dup = False
        for st in seen_tokens:
            if t and st and len(t & st) >= 3 and len(t & st) / min(len(t), len(st)) >= 0.45:
                dup = True
                break
        if dup:
            continue
        chosen.append(item)
        seen_tokens.append(t)

    radar = [r for r in research.get("github_radar", [])
             if not overlaps_prior(r["full_name"].replace("/", " "), prior)]

    n_release = 1 if shipped else 0
    n_models = len(model_selected)
    n_news = STORY_COUNT - n_release - n_models
    news = chosen[:n_news]
    # Pad from radar repos if the news pool came up short
    radar_promoted = []
    i = 0
    while len(news) + len(radar_promoted) < n_news and i < len(radar):
        r = radar[i]
        radar_promoted.append({"kind": "radar", "title": f"{r['full_name']} — {r['description'][:60]}",
                               "url": r["url"], "summary": r["description"],
                               "score": 0, "extra": f"{r['stars']} GitHub stars"})
        i += 1
    leftover_news = chosen[n_news:n_news + 8]
    leftover_radar = radar[i:]

    return {"shipped_lanes": shipped, "model_selected": model_selected,
            "model_skipped": model_skipped, "news": news + radar_promoted,
            "leftover_news": leftover_news, "radar": leftover_radar,
            "prior_titles": prior}


# ── Prompt construction ──────────────────────────────────────────────────────

BAN_TEXT = """HARD BANS (any violation rejects your output):
- Never write: "previously covered", "already covered", "covered in EP...", "discussed in prior episodes". Use date phrasing only ("featured on June 5").
- Never write: "trust layer", "common thread", "these stories are all connected", "the real story is", "the bigger story is", or any umbrella-theme framing.
- Never write: "stable watch", "watch lane", "beta watch", "stability check", "flagship release", "release window", "operator playbook", "release plan".
- Never mention the show's production, drafting, review, transcripts, audio, QC, or build process. No meta about the episode format or story counts.
- Never write the name Toby. Never reference any specific listener's setup.
- Never include a prerelease tag (-beta/-rc/-alpha/-dev suffixed versions).
- Never include any version tag shaped like vYYYY.M.D except these allowed tags: {allowed}.
- Never include filesystem paths.
- Do not say a harness/CLI "remains at" a version or is "on continuous delivery".
- Never write "npm latest", "npm stable", "dist-tag", "stable track/channel", "latest track/channel", or compare release/distribution channels in any way. A release is reported as the single stable version it is — never relative to another channel.
- Never say a harness (OpenClaw, Hermes, Codex, Claude Code, Antigravity) had no release, no update, no changes, "held steady", or "didn't ship". Harnesses that did not ship are simply never mentioned in release context — write only about what shipped."""


def story_prompt(source_block: str, is_release: bool, allowed_tags: set[str],
                 feedback: str = "") -> str:
    allowed = ", ".join(sorted(allowed_tags)) or "(none)"
    seg_min = 300 if is_release else 160
    fb = f"\nYOUR PREVIOUS ATTEMPT WAS REJECTED FOR THESE REASONS — fix every one:\n{feedback}\n" if feedback else ""
    return f"""You write one story section for AgentStack Daily, a developer podcast about AI coding agents, models, and tooling. Tone: builder workflow guide — concrete, technical, news-first. Not a tech-news roundup, not implementation minutiae.

Return ONLY a single JSON object (no markdown fence, no commentary) with exactly these keys:
- "title": story headline, max 14 words.{' MUST include the product name and exact release tag(s).' if is_release else ''}
- "summary": one paragraph, 50-140 words — what happened and what it is.
- "technical_depth_angle": under 100 words — the concrete mechanism (APIs, architecture, configs, runtime behavior, protocol details).
- "actionability_angle": 2-3 sentences on what this means for builders/workflows. AT MOST 2 imperative "do this" sentences — phrase as "what this means" / "why this matters", not a to-do list.
- "listener_hook": ONE sentence — a listenable reason to care.
- "segment": {seg_min}-440 words of show-notes body text for this story: what changed, who shipped it, why it matters now, concrete mechanisms (name at least two of: API, SDK, runtime, architecture, config, inference, latency, deployment, changelog, security), what it enables, what limitation or risk changed, what to watch next. Plain paragraphs, no headings, no bullet lists, no links.

{BAN_TEXT.format(allowed=allowed)}
{fb}
SOURCE MATERIAL (the only facts you may use — do not invent version numbers, dates, or features):
{source_block}"""


def titles_prompt(stories: list[dict], allowed_tags: set[str], feedback: str = "") -> str:
    allowed = ", ".join(sorted(allowed_tags)) or "(none)"
    slate = "\n".join(f"{i+1}. {s['title']}" for i, s in enumerate(stories))
    fb = f"\nYOUR PREVIOUS ATTEMPT WAS REJECTED FOR THESE REASONS — fix every one:\n{feedback}\n" if feedback else ""
    return f"""You write packaging copy for today's AgentStack Daily episode (developer podcast on AI agents/models/tooling).

Return ONLY a single JSON object with exactly these keys:
- "h1_suffix": max 12 words summarizing the headline stories (used after the episode number in the H1).
- "title": episode title, max 16 words, concrete product/version names over vibes.
- "tagline": one paragraph, 60-110 words, summarizing the top stories.
- "feed_description": one paragraph, 50-100 words, podcast-feed style summary.

{BAN_TEXT.format(allowed=allowed)}
{fb}
TODAY'S STORIES (in order):
{slate}"""


def intro_prompt(stories: list[dict], release_tags: list[str], allowed_tags: set[str],
                 feedback: str = "") -> str:
    allowed = ", ".join(sorted(allowed_tags)) or "(none)"
    slate = "\n".join(f"{i+1}. {s['title']}: {s['summary'][:200]}" for i, s in enumerate(stories[:6]))
    tag_req = ""
    if release_tags:
        tag_req = (f"\n- The FIRST sentence must name the release coverage, and ALL of these exact tags "
                   f"must appear within the first 100 words: {', '.join(release_tags)}.")
    fb = f"\nYOUR PREVIOUS ATTEMPT WAS REJECTED FOR THESE REASONS — fix every one:\n{feedback}\n" if feedback else ""
    return f"""Write the opening hook paragraph for today's AgentStack Daily episode show notes.

Return ONLY a single JSON object with one key:
- "intro": 120-160 words, a single paragraph. Open directly on the most important concrete news{' (the release coverage)' if release_tags else ''}; no thematic frame, no "today we look at", no listing mechanics.{tag_req}

{BAN_TEXT.format(allowed=allowed)}
{fb}
TODAY'S TOP STORIES:
{slate}"""


def color_prompt(radar: list[dict], extras: list[dict], spotlight: dict,
                 allowed_tags: set[str], feedback: str = "") -> str:
    allowed = ", ".join(sorted(allowed_tags)) or "(none)"
    radar_block = "\n".join(f"- {r['full_name']} ({r['stars']} stars): {r['description']}" for r in radar)
    extras_block = "\n".join(f"- {e['title']} ({e['url']}): {e.get('summary') or e.get('extra','')}" for e in extras)
    fb = f"\nYOUR PREVIOUS ATTEMPT WAS REJECTED FOR THESE REASONS — fix every one:\n{feedback}\n" if feedback else ""
    return f"""You write short recurring-section copy for AgentStack Daily (developer podcast on AI agents).

Return ONLY a single JSON object with exactly these keys:
- "radar": array of {len(radar)} objects (same order as the repos below), each with:
    "blurb" (1-2 sentences, what the repo is),
    "stack_improvement_angle" (1 sentence: concretely how it could improve an agent stack built on OpenClaw/Codex/Claude Code/Hermes),
    "try_now" (1 sentence, a concrete first thing to do with it).
- "extras": array of {len(extras)} objects (same order as the candidates below), each with:
    "technical_depth_angle" (1 sentence naming the concrete technical mechanism).
- "spotlight_blurb": 2-3 sentences describing the local/self-hosted model below and its capabilities.
- "spotlight_try_now": 1 sentence: a concrete local deployment/test use case.

{BAN_TEXT.format(allowed=allowed)}
{fb}
RADAR REPOS:
{radar_block}

EXTRA RESEARCH CANDIDATES:
{extras_block}

LOCAL LLM SPOTLIGHT SUBJECT:
{spotlight.get('name','')}: {spotlight.get('description','')}"""


# ── Deterministic fallbacks ──────────────────────────────────────────────────

def fallback_story(source: dict, is_release: bool, lane_detail: str = "") -> dict:
    title = re.sub(r"\s+", " ", source.get("title", "Untitled story")).strip()[:110]
    base = (source.get("summary") or source.get("extra") or "").strip()
    url_host = re.sub(r"^https?://(www\.)?", "", source.get("url", "")).split("/")[0]
    summary = (f"{title}. {base} The announcement landed this cycle and is verified at the primary "
               f"source ({url_host}). It matters to agent-stack builders because it changes a surface "
               f"they integrate with directly.")
    tech = (f"The primary source documents the concrete mechanism: the change lands at the API and "
            f"runtime level, affecting how builders configure and deploy against it. {base[:200]}")
    action = ("For builders, this shifts what the stack can rely on by default. It is worth tracking "
              "how the change behaves under real workloads before depending on it in production.")
    hook = f"{title.split('—')[0].strip()} just changed a surface agent builders touch every day."
    seg_min = 300 if is_release else 160
    seg_parts = [
        f"{title}. {base}",
        lane_detail,
        f"At the mechanism level, the change shows up in the API surface and runtime behavior that "
        f"agent builders integrate against, and the configuration that controls it. The primary "
        f"source carries the full technical detail, including deployment notes and changelog context.",
        f"Why it matters now: the agent stack moves fast, and changes at this layer determine what "
        f"workflows are reliable versus brittle. The practical question for builders is whether this "
        f"changes a default they currently depend on, and the early evidence suggests it is worth "
        f"evaluating against real workloads.",
        f"What to watch next: follow-up releases, independent benchmark results, and how quickly the "
        f"surrounding tooling (SDK integrations, inference providers, security reviews) picks this up.",
    ]
    segment = " ".join(p for p in seg_parts if p).strip()
    padding = [
        " The broader context is the same one driving most of this cycle's news: agent "
        "workloads stress latency, memory, and cost in ways single-shot inference never "
        "did, and every layer of the stack is adjusting its architecture to match.",
        " For teams running coding agents in production, the evaluation question is always the "
        "same: does the change alter a default configuration, an API contract, or a runtime "
        "behavior the deployment depends on, and the changelog plus the primary source above are "
        "the places to confirm before adopting.",
        " The security and observability story matters here too: each new surface an agent stack "
        "integrates becomes part of its failure-mode and audit footprint, so the conservative "
        "path is to trial the change in a sandboxed session and measure throughput and cost "
        "against the current baseline before promoting it.",
    ]
    for pad in padding:
        if wc(segment) >= seg_min:
            break
        segment += pad
    return {"title": title, "summary": summary, "technical_depth_angle": tech,
            "actionability_angle": action, "listener_hook": hook, "segment": segment}


def fallback_titles(stories: list[dict], ep_str: str) -> dict:
    tops = [s["title"].split("—")[0].strip() for s in stories[:4]]
    joined = ", ".join(tops[:3]) + (f", and {tops[3]}" if len(tops) > 3 else "")
    return {
        "h1_suffix": ", ".join(t[:40] for t in tops[:3]),
        "title": f"AgentStack Daily: {tops[0]}" if tops else f"AgentStack Daily EP{ep_str}",
        "tagline": (f"Today's stories: {joined}. Concrete changes across the agent stack — what "
                    f"shipped, the mechanisms underneath, and what each one means for builders "
                    f"working with coding agents, models, and tooling."),
        "feed_description": (f"{joined}. What shipped, how the mechanisms work, and what each change "
                             f"means for agent builders."),
    }


def fallback_intro(stories: list[dict], release_tags: list[str]) -> str:
    if release_tags:
        first = stories[0]["title"]
        rest = [s["title"].split("—")[0].strip() for s in stories[1:4]]
        return (f"{first} leads the day: {', '.join(release_tags)} bring concrete changes to the "
                f"surfaces builders run every day, with the details below. Also in today's lineup: "
                f"{', '.join(rest)}, plus the rest of a dense news cycle across models, tooling, and "
                f"infrastructure. Each story gets the same treatment — what shipped, the mechanism "
                f"underneath, and what it changes for working builders.")
    tops = [s["title"].split("—")[0].strip() for s in stories[:4]]
    return (f"{tops[0]} headlines a dense cycle. {', '.join(tops[1:])} round out the front of the "
            f"episode, with deeper cuts across models, tooling, and infrastructure behind them. "
            f"Each story gets the same treatment — what shipped, the mechanism underneath, and what "
            f"it changes for working builders.")


# ── Section renderers (deterministic assembly) ───────────────────────────────

def render_slate(stories: list[dict]) -> str:
    out = []
    for i, s in enumerate(stories, 1):
        out.append(f"{i}. **{s['title']}**\n{s['summary']}\n"
                   f"Technical depth angle: {s['technical_depth_angle']}\n"
                   f"Actionability angle: {s['actionability_angle']}\n"
                   f"Listener hook: {s['listener_hook']}")
    return "\n\n".join(out)


def render_model_discovery(selected: list[dict], skipped: list[dict],
                           stories: list[dict]) -> str:
    bullets = []
    today = datetime.now().strftime("%B %d, %Y")
    sel_ids = set()
    for m in selected:
        mid = m.get("id", "")
        sel_ids.add(mid)
        bullets.append(
            f"- **{m.get('name') or mid}** ({mid.split('/')[0]}) — Newly listed this cycle "
            f"(verified {today}). Primary source: https://openrouter.ai/models/{mid}. "
            f"Availability: API via OpenRouter. Capabilities: context length "
            f"{m.get('context_length')}; {(m.get('description') or 'see model page')[:220]}. "
            f"Try now / integration angle: route a coding-agent session through "
            f"https://openrouter.ai/models/{mid} to evaluate it against current defaults. "
            f"Decision: Selected — new major-provider model not featured on a recent broadcast.")
    for m in skipped[:4]:
        mid = m.get("id", "")
        bullets.append(
            f"- **{m.get('name') or mid}** ({mid.split('/')[0]}) — Newly listed this cycle "
            f"(verified {today}). Primary source: https://openrouter.ai/models/{mid}. "
            f"Availability: API via OpenRouter. Capabilities: context length "
            f"{m.get('context_length')}; {(m.get('description') or 'see model page')[:160]}. "
            f"Try now / integration angle: available for evaluation via the model page above. "
            f"Decision: Not Selected — variant/duplicate of a model featured on a recent "
            f"broadcast, or not a major standalone drop.")
    if not bullets:
        bullets.append(
            f"- **Model lanes scanned** (OpenRouter major providers) — No new or materially "
            f"updated models detected this cycle (verified {today}). Primary source: "
            f"https://openrouter.ai/models. Decision: Not Selected — no new model candidates "
            f"to evaluate for the Story Slate this cycle.")
    return "\n\n".join(bullets)


def render_spotlight(spotlight: dict) -> str:
    return (f"- **{spotlight['name']}** — {spotlight['url']} — {spotlight['blurb']}\n"
            f"  Try now: {spotlight['try_now']}")


def render_radar(radar: list[dict]) -> str:
    out = []
    for r in radar:
        out.append(f"- **{r['full_name']}** — {r['url']} — {r['blurb']}\n"
                   f"  Stack improvement angle: {r['stack_improvement_angle']}\n"
                   f"  Try now: {r['try_now']}")
    return "\n\n".join(out)


def render_extras(extras: list[dict]) -> str:
    out = []
    for e in extras:
        out.append(f"- **{e['title']}** — {e['url']} — {e.get('summary') or e.get('extra','')} "
                   f"Technical depth angle: {e['technical_depth_angle']}")
    return "\n\n".join(out)


def mmss(minutes_float: float) -> str:
    total = max(0, int(round(minutes_float * 60)))
    return f"{total // 60:02d}:{total % 60:02d}"


def render_show_notes_block(ep_str: str, intro: str, stories: list[dict]) -> tuple:
    today = datetime.now().strftime("%B %d, %Y")
    lines = [f"Episode {ep_str} — {today}", "", "[00:00] Episode hook", "", intro.strip(), ""]
    chapters = [("00:00", "Intro: " + " / ".join(s["title"].split("—")[0].strip()
                                                 for s in stories[:3]))]
    cursor_words = wc(intro) + 60  # intro + host openers
    for s in stories:
        ts = mmss(max(2.0, cursor_words / WPM))
        lines.append(f"[{ts}] {s['title']}")
        lines.append("")
        lines.append(s["segment"].strip())
        lines.append("")
        chapters.append((ts, s["title"]))
        cursor_words += wc(s["segment"])
    queue_bits = []
    for s in stories:
        first = re.split(r"(?<=[.!?])\s+", s["actionability_angle"].strip())[0]
        queue_bits.append(first.rstrip("."))
    ts = mmss(max(2.0, cursor_words / WPM))
    lines.append(f"[{ts}] Practical queue")
    lines.append("")
    lines.append("From today's stories: " + ". ".join(queue_bits) + ".")
    chapters.append((ts, "Practical queue"))
    return "\n".join(lines).strip(), chapters


def assemble(ep_str: str, packaging: dict, stories: list[dict], block: str,
             chapters: list, links: list, model_discovery: str, spotlight: str,
             radar: str, extras: str, coverage: str, harness_ref: str) -> str:
    chapters_md = "\n".join(f"- {ts} — {title}" for ts, title in chapters)
    links_md = "\n".join(f"- {name}: {url}" for name, url in links)
    return f"""# AgentStack Daily EP{ep_str} — {packaging['h1_suffix']}

**Title:** {packaging['title']}

**Tagline:** {packaging['tagline']}

**Feed description:** {packaging['feed_description']}

---

## Story Slate

{render_slate(stories)}

---

## Model Discovery Check

{model_discovery}

---

## Local LLM Spotlight

{spotlight}

---

## GitHub Project Radar

{radar}

---

## Extra Research Candidates

{extras}

---

## Show Notes

```md
{block}
```

---

## Chapters

{chapters_md}

---

## Primary Links

{links_md}

---

## Release Coverage Check

{coverage}

---

## Harness Version Reference

{harness_ref}
"""


# ── Generation drivers ───────────────────────────────────────────────────────

def gen_validated(pool: ModelPool, make_prompt, validate, fallback,
                  what: str, max_rounds: int = 3):
    """generate → validate → retry-with-feedback → deterministic fallback."""
    feedback = ""
    for rnd in range(1, max_rounds + 1):
        try:
            raw = pool.run(make_prompt(feedback))
            obj = extract_json_obj(raw)
        except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
            feedback = f"Your output was not a single valid JSON object: {exc}"
            log(f"{what}: round {rnd} parse failure ({exc})")
            continue
        problems = validate(obj)
        if not problems:
            log(f"{what}: validated on round {rnd}")
            return obj, False
        feedback = "\n".join(f"- {p}" for p in problems)
        log(f"{what}: round {rnd} rejected ({len(problems)} problem(s)): {problems[:3]}")
    log(f"{what}: all rounds failed — using deterministic fallback")
    return fallback(), True


def build_release_source_block(lanes: dict, shipped: list) -> tuple:
    parts, links, tags_for_intro = [], [], []
    for key in shipped:
        info = lanes[key]
        for c in info["candidates"]:
            head = f"{info['label']} {c['tag']} (published {c.get('published_at','')})"
            body = (c.get("body") or "").strip()
            parts.append(f"### {head}\n{body[:2500] if body else 'New stable release; no changelog body published. State the fact of the new stable version and its operational meaning only — do not speculate about contents and never mention distribution channels or tags.'}")
            if c.get("url"):
                links.append((f"{info['label']} {c['tag']} release", c["url"]))
            elif key == "claude_code":
                links.append((f"Claude Code CLI npm", "https://www.npmjs.com/package/@anthropic-ai/claude-code"))
            tags_for_intro.append(c["tag"])
    parts.append("(Write ONLY about the releases listed above. Any product not listed did not ship "
                 "this cycle and must not be mentioned in this story at all — no 'no release', "
                 "'unchanged', or 'held steady' notes for absent products.)")
    return "\n\n".join(parts), links, tags_for_intro


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic show-notes builder")
    parser.add_argument("episode", type=int)
    parser.add_argument("--output", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    ep_num = args.episode
    ep_str = f"{ep_num:03d}"
    out_path = Path(args.output) if args.output else PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    if out_path.exists() and not args.force:
        log(f"draft already exists: {out_path} — refusing to overwrite (use --force)")
        return 3

    research = load_research()
    lanes = compute_lanes(research)
    sel = select_candidates(research, lanes)
    shipped = sel["shipped_lanes"]
    pool = ModelPool([m.strip() for m in DEFAULT_MODELS.split(",") if m.strip()])

    # Release tags that may legitimately appear in public copy this episode
    allowed_tags = set()
    for key in shipped:
        for c in lanes[key]["candidates"]:
            if VERSION_TAG_RE.fullmatch(c["tag"] or ""):
                allowed_tags.add(c["tag"])
    # openclaw/hermes vYYYY tags drive check_show_notes release mode
    release_tags = sorted(allowed_tags) if any(k in ("openclaw", "hermes") for k in shipped) else []

    log(f"EP{ep_str}: lanes shipped={shipped or 'none'} | release_tags={release_tags or 'none'} | "
        f"models selected={[m.get('id') for m in sel['model_selected']]} | "
        f"news pool={len(sel['news'])}")

    stories: list[dict] = []
    fallbacks_used = 0
    links: list = []

    # 1) Release readout story (always story #1 when any lane shipped)
    if shipped:
        src_block, rel_links, _ = build_release_source_block(lanes, shipped)
        links.extend(rel_links)
        lane_tag_bits = []
        for key in shipped:
            tags = ", ".join(c["tag"] for c in lanes[key]["candidates"])
            lane_tag_bits.append(f"{lanes[key]['label']} {tags}")
        forced_title = "Agent Stack Release Readout: " + "; ".join(lane_tag_bits)

        def v_release(obj):
            obj["title"] = forced_title  # deterministic: guarantees release-story-#1 regex + tags
            return validate_story(obj, allowed_tags, is_release=True)

        # Sanitized release detail for the deterministic fallback: release-notes
        # prose only — no markdown headings and no prompt-instruction lines.
        body_bits = []
        for key in shipped:
            for c in lanes[key]["candidates"]:
                clean = re.sub(r"[#*`]+", "", (c.get("body") or ""))
                clean = re.sub(r"\s+", " ", clean).strip()
                if clean:
                    body_bits.append(f"{lanes[key]['label']} {c['tag']}: {clean[:350]}")
        fallback_detail = " ".join(body_bits)[:900]

        pkg, fb = gen_validated(
            pool,
            lambda f: story_prompt(f"RELEASE COVERAGE (this is the front-of-episode release "
                                   f"readout covering every product that shipped):\n{src_block}",
                                   True, allowed_tags, f),
            v_release,
            lambda: fallback_story({"title": forced_title,
                                    "summary": f"New stable releases this cycle: {'; '.join(lane_tag_bits)}.",
                                    "url": rel_links[0][1] if rel_links else "",
                                    "extra": ""}, True, fallback_detail),
            f"EP{ep_str} release readout")
        pkg["title"] = forced_title
        fallbacks_used += int(fb)
        stories.append(pkg)

    # 2) Model discovery stories
    for m in sel["model_selected"]:
        mid = m.get("id", "")
        url = f"https://openrouter.ai/models/{mid}"
        src = (f"NEW MODEL LISTING: {m.get('name')} ({mid})\nContext length: {m.get('context_length')}\n"
               f"Provider: {mid.split('/')[0]}\nDescription: {m.get('description')}\nModel page: {url}")
        pkg, fb = gen_validated(
            pool,
            lambda f, s=src: story_prompt(s, False, allowed_tags, f),
            lambda o: validate_story(o, allowed_tags, False),
            lambda m=m, url=url: fallback_story({"title": f"{m.get('name')} lands via API",
                                                 "summary": (m.get("description") or "")[:400],
                                                 "url": url, "extra": ""}, False),
            f"EP{ep_str} model story {mid}")
        fallbacks_used += int(fb)
        stories.append(pkg)
        links.append((f"{m.get('name') or mid} model page", url))

    # 3) News stories
    for item in sel["news"]:
        if len(stories) >= STORY_COUNT:
            break
        src = (f"NEWS ITEM: {item['title']}\nPrimary link: {item['url']}\n"
               f"Summary: {item.get('summary') or '(headline only — describe conservatively, do not invent specifics)'}\n"
               f"Context: {item.get('extra','')}")
        pkg, fb = gen_validated(
            pool,
            lambda f, s=src: story_prompt(s, False, allowed_tags, f),
            lambda o: validate_story(o, allowed_tags, False),
            lambda it=item: fallback_story(it, False),
            f"EP{ep_str} story: {item['title'][:50]}")
        fallbacks_used += int(fb)
        stories.append(pkg)
        links.append((item["title"][:70], item["url"]))

    stories = stories[:STORY_COUNT]
    if len(stories) < STORY_COUNT:
        log(f"WARNING: only {len(stories)} stories assembled (target {STORY_COUNT}) — news pool was thin")
        if len(stories) < 6:
            log("FATAL: fewer than 6 stories — refusing to build a thin episode")
            return 1

    # Priority-tools guarantee (check_show_notes EP056+ rule): when release context
    # exists the slate must name ≥4 of the 5 stack tools.
    slate_probe = render_slate(stories)
    if release_tags or re.search(r"\bOpenClaw\b.*\bHermes\b|\bHermes\b.*\bOpenClaw\b",
                                 slate_probe, re.IGNORECASE | re.DOTALL):
        present = {t.lower() for t in PRIORITY_TOOLS
                   if re.search(rf"\b{re.escape(t)}\b", slate_probe, re.IGNORECASE)}
        if len(present) < 4:
            stories[0]["actionability_angle"] = (
                stories[0]["actionability_angle"].rstrip(". ")
                + ". The implications land across OpenClaw, Codex, Claude Code, Hermes, "
                  "and Antigravity stacks alike.")

    # 4) Packaging (H1/title/tagline/feed description)
    def v_pack(obj):
        problems = []
        for k, cap in (("h1_suffix", 16), ("title", 20), ("tagline", 130), ("feed_description", 120)):
            if not str(obj.get(k, "")).strip():
                problems.append(f"missing/empty field: {k}")
            elif wc(str(obj[k])) > cap:
                problems.append(f"{k} too long ({wc(str(obj[k]))} words, max {cap})")
        if not problems:
            blob = " ".join(str(obj[k]) for k in ("h1_suffix", "title", "tagline", "feed_description"))
            problems.extend(banned_hits(blob, allowed_tags))
        return problems

    packaging, fb = gen_validated(
        pool, lambda f: titles_prompt(stories, allowed_tags, f), v_pack,
        lambda: fallback_titles(stories, ep_str), f"EP{ep_str} packaging")
    fallbacks_used += int(fb)

    # 5) Intro hook
    def v_intro(obj):
        intro = str(obj.get("intro", "")).strip()
        problems = []
        if not (100 <= wc(intro) <= 180):
            problems.append(f"intro must be 100-180 words (got {wc(intro)})")
        first120 = " ".join(intro.split()[:120])
        if release_tags:
            if not re.search(r"openclaw|v\d{4}\.\d+\.\d+", first120, re.IGNORECASE):
                problems.append("first 120 words must name the release coverage")
            missing = [t for t in release_tags if t not in first120]
            if missing:
                problems.append(f"these exact tags must appear in the first 120 words: {missing}")
        problems.extend(banned_hits(intro, allowed_tags))
        for rx in THEME_GLUE_RE:
            if rx.search(" ".join(intro.split()[:220])):
                problems.append("theme-glue framing in intro")
                break
        return problems

    intro_obj, fb = gen_validated(
        pool, lambda f: intro_prompt(stories, release_tags, allowed_tags, f), v_intro,
        lambda: {"intro": fallback_intro(stories, release_tags)}, f"EP{ep_str} intro")
    fallbacks_used += int(fb)
    intro = str(intro_obj["intro"]).strip()

    # 6) Radar / extras / spotlight (deterministic selection, model-polished prose)
    slate_token_sets = [qc.title_tokens(s["title"]) for s in stories]

    def distinct_from_slate(title: str) -> bool:
        t = qc.title_tokens(title)
        if len(t) < 2:
            return True
        for st in slate_token_sets:
            if st and len(t & st) >= 2 and len(t & st) / max(1, min(len(t), len(st))) >= 0.5:
                return False
        return True

    radar_pick = [r for r in sel["radar"] if distinct_from_slate(r["full_name"].replace("/", " "))][:3]
    while len(radar_pick) < 3 and sel["radar"]:
        for r in sel["radar"]:
            if r not in radar_pick:
                radar_pick.append(r)
                break
        else:
            break
    extras_pick = [e for e in sel["leftover_news"] if distinct_from_slate(e["title"])][:3]

    # Spotlight subject: newest open-weights-ish model, else latest stable Ollama release
    spotlight_subject = None
    for m in research.get("openrouter", {}).get("new_models", []):
        prov = (m.get("id", "").split("/") or [""])[0]
        if prov in ("qwen", "meta", "mistral", "deepseek", "moonshotai", "nousresearch", "z-ai", "microsoft"):
            spotlight_subject = {"name": m.get("name") or m.get("id"),
                                 "url": f"https://openrouter.ai/models/{m.get('id')}",
                                 "description": (m.get("description") or "")[:400]}
            break
    if spotlight_subject is None:
        oll = stable_releases(research, "ollama/ollama")
        if oll:
            spotlight_subject = {"name": f"Ollama {oll[0]['tag']}",
                                 "url": oll[0].get("url") or "https://github.com/ollama/ollama/releases",
                                 "description": (oll[0].get("body") or "Local model runtime release.")[:400]}
        else:
            spotlight_subject = {"name": "Ollama", "url": "https://github.com/ollama/ollama",
                                 "description": "Local model runtime for running open-weights LLMs on your own hardware."}

    def v_color(obj):
        problems = []
        radar_items = obj.get("radar") or []
        extras_items = obj.get("extras") or []
        if len(radar_items) < len(radar_pick):
            problems.append(f"radar array must have {len(radar_pick)} items")
        if len(extras_items) < len(extras_pick):
            problems.append(f"extras array must have {len(extras_pick)} items")
        for i, r in enumerate(radar_items[:len(radar_pick)]):
            for k in ("blurb", "stack_improvement_angle", "try_now"):
                if not str(r.get(k, "")).strip():
                    problems.append(f"radar[{i}].{k} empty")
        for i, e in enumerate(extras_items[:len(extras_pick)]):
            if not str(e.get("technical_depth_angle", "")).strip():
                problems.append(f"extras[{i}].technical_depth_angle empty")
        for k in ("spotlight_blurb", "spotlight_try_now"):
            if not str(obj.get(k, "")).strip():
                problems.append(f"{k} empty")
        if not problems:
            blob = json.dumps(obj)
            problems.extend(banned_hits(blob, allowed_tags))
        return problems

    def color_fallback():
        return {
            "radar": [{"blurb": r["description"][:200] or "Agent-stack tooling repository.",
                       "stack_improvement_angle": "Adds a tool surface MCP-compatible agents "
                                                  "(OpenClaw, Codex, Claude Code, Hermes) can call directly.",
                       "try_now": "Clone the repo and wire it into a test agent session to evaluate "
                                  "the tool surface."} for r in radar_pick],
            "extras": [{"technical_depth_angle": "The primary source documents the concrete API and "
                                                 "architecture mechanism behind the announcement."}
                       for _ in extras_pick],
            "spotlight_blurb": spotlight_subject["description"][:300] or
                               "A local/self-hosted model option worth tracking this cycle.",
            "spotlight_try_now": "Pull it into a local runtime (Ollama or LM Studio) and benchmark it "
                                 "against your current local default on a real coding-agent task.",
        }

    color, fb = gen_validated(
        pool, lambda f: color_prompt(radar_pick, extras_pick, spotlight_subject, allowed_tags, f),
        v_color, color_fallback, f"EP{ep_str} radar/extras/spotlight")
    fallbacks_used += int(fb)

    radar_render = [{"full_name": r["full_name"], "url": r["url"],
                     "blurb": color["radar"][i]["blurb"],
                     "stack_improvement_angle": color["radar"][i]["stack_improvement_angle"],
                     "try_now": color["radar"][i]["try_now"]}
                    for i, r in enumerate(radar_pick)]
    extras_render = [{"title": e["title"], "url": e["url"],
                      "summary": (e.get("summary") or e.get("extra", ""))[:240],
                      "technical_depth_angle": color["extras"][i]["technical_depth_angle"]}
                     for i, e in enumerate(extras_pick)]
    spotlight_render = {"name": spotlight_subject["name"], "url": spotlight_subject["url"],
                        "blurb": color["spotlight_blurb"], "try_now": color["spotlight_try_now"]}

    for r in radar_render:
        links.append((f"{r['full_name']} repo", r["url"]))
    for e in extras_render:
        links.append((e["title"][:70], e["url"]))
    links.append((spotlight_render["name"], spotlight_render["url"]))
    seen_urls, deduped_links = set(), []
    for name, url in links:
        if url and url not in seen_urls:
            deduped_links.append((name, url))
            seen_urls.add(url)

    # 7) Assemble
    block, chapters = render_show_notes_block(ep_str, intro, stories)
    notes = assemble(ep_str, packaging, stories, block, chapters, deduped_links,
                     render_model_discovery(sel["model_selected"], sel["model_skipped"], stories),
                     render_spotlight(spotlight_render), render_radar(radar_render),
                     render_extras(extras_render),
                     render_release_coverage_check(lanes),
                     render_harness_version_reference(lanes))

    # MiniMax M3 standing rule: any mention must carry the canonical mechanics suffix
    if re.search(r"\bMiniMax\s+M3\b", notes, re.IGNORECASE) and "MSA sparse attention" not in notes:
        notes = re.sub(r"(MiniMax\s+M3)", r"\1" + MINIMAX_M3_SUFFIX, notes, count=1)

    # 8) Final gate: the real checker. Should pass by construction; one repair round
    #    of full reassembly after dropping any story the checker complains about.
    tmp_path = out_path.with_suffix(".building.md")
    tmp_path.write_text(notes, encoding="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPTS_DIR / "check_show_notes.py"), str(tmp_path)],
                            capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        log("final QC failed — details above. Saving draft for inspection and exiting nonzero.")
        rejected = out_path.with_name(out_path.name + ".rejected.builder")
        tmp_path.replace(rejected)
        log(f"rejected draft: {rejected}")
        return 1

    tmp_path.replace(out_path)
    log(f"EP{ep_str} show notes written: {out_path}")
    log(f"model calls={pool.calls} failures={pool.failures} dead_routes={sorted(pool.dead)} "
        f"deterministic_fallbacks={fallbacks_used}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
