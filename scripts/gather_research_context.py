#!/usr/bin/env python3
"""
Gather Research Context — deterministic pre-flight data collection.

Collects past show-notes covered versions, Hacker News AI/dev news, a
25-feed RSS roster (frontier labs, local-AI projects, compute/hardware
press, practitioner commentary, AI tech press), GitHub releases (harness
lanes + local-AI/inference infra), OpenRouter model diffs, package registry
versions, arXiv + HuggingFace Daily Papers, HuggingFace trending models,
Reddit local-AI communities (r/LocalLLaMA and friends), and GitHub
Trending/Radar repos. Writes BOTH:

  /tmp/agent_research_context.md    human-readable digest (debugging/inspection)
  /tmp/agent_research_context.json  structured data consumed by build_show_notes.py

Python 3.9 compatible, stdlib only.
"""

import urllib.request
import urllib.parse
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET
import email.utils
from pathlib import Path

PODCAST_DIR = Path("/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast")
OUTPUT_MD = Path("/tmp/agent_research_context.md")
OUTPUT_JSON = Path("/tmp/agent_research_context.json")
CACHE_PATH = PODCAST_DIR / "scripts" / "last_seen_models.json"


def fetch_url(url, headers=None):
    if headers is None:
        headers = {}
    if "User-Agent" not in headers:
        headers["User-Agent"] = "OpenClaw-Podcast-Gatherer/3.0"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read()
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def fetch_url_json(url, headers=None):
    data = fetch_url(url, headers)
    if data:
        try:
            return json.loads(data.decode("utf-8", errors="ignore"))
        except Exception as e:
            print(f"Warning: Failed to parse JSON from {url}: {e}", file=sys.stderr)
    return None


# ── Recent episode coverage history ──────────────────────────────────────────

def get_recent_episodes_context():
    ep_pattern = re.compile(r"show_notes_episode_(\d{3})\.md$")
    valid_files = []
    for f in PODCAST_DIR.glob("show_notes_episode_*.md"):
        match = ep_pattern.match(f.name)
        if match:
            valid_files.append((int(match.group(1)), f))
    valid_files.sort(key=lambda x: x[0], reverse=True)
    last_5 = valid_files[:5]
    last_5.reverse()

    md = ["# RECENT EPISODES RELEASE COVERAGE HISTORY\n"]
    data = []
    for ep_num, filepath in last_5:
        md.append(f"## Episode EP{ep_num:03d} ({filepath.name})\n")
        entry = {"episode": ep_num, "file": filepath.name,
                 "release_coverage_check": "", "harness_version_reference": "",
                 "story_titles": [], "model_discovery": ""}
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"## Release Coverage Check\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
            if m:
                entry["release_coverage_check"] = m.group(1).strip()
                md.append("### Release Coverage Check:\n" + m.group(1).strip() + "\n")
            m2 = re.search(r"## Harness Version Reference\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
            if m2:
                entry["harness_version_reference"] = m2.group(1).strip()
                md.append("### Harness Version Reference:\n" + m2.group(1).strip() + "\n")
            m3 = re.search(r"## Model Discovery Check\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
            if m3:
                entry["model_discovery"] = m3.group(1).strip()
            slate_m = re.search(r"## Story Slate\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
            if slate_m:
                entry["story_titles"] = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", slate_m.group(1), re.MULTILINE)
        except Exception as e:
            md.append(f"Failed to read file: {e}\n")
        data.append(entry)
    return "\n".join(md), data


# ── GitHub releases ──────────────────────────────────────────────────────────

def get_github_releases(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=15"
    raw = fetch_url_json(url)
    if not raw:
        return f"### {owner}/{repo} releases: Failed to fetch\n", []

    md = [f"### Latest stable releases for {owner}/{repo}:"]
    data = []
    for rel in raw:
        if not isinstance(rel, dict):
            continue
        tag = rel.get("tag_name", "N/A")
        name = rel.get("name", "N/A")
        pub_date = rel.get("published_at", "")
        is_prerelease = bool(rel.get("prerelease", False))
        body = rel.get("body", "") or ""
        data.append({"tag": tag, "name": name, "published_at": pub_date,
                     "prerelease": is_prerelease, "body": body[:6000],
                     "url": rel.get("html_url", "")})
        status = "PRERELEASE" if is_prerelease else "STABLE"
        md.append(f"- **{tag}** ({name}) - Published: {pub_date} [{status}]")
        if body:
            preview = "\n  ".join(body.splitlines()[:5])
            md.append(f"  *Description Preview:*\n  {preview}")
    return "\n".join(md), data


# ── npm / PyPI ────────────────────────────────────────────────────────────────

def get_npm_version_info(package_name):
    url = f"https://registry.npmjs.org/{urllib.parse.quote(package_name, safe='@/')}"
    raw = fetch_url_json(url)
    if not raw:
        return f"### {package_name} npm versions: Failed to fetch\n", {}

    md = [f"### NPM Registry info for {package_name}:"]
    dist_tags = raw.get("dist-tags", {})
    for tag, val in dist_tags.items():
        md.append(f"- **dist-tag `{tag}`**: {val}")
    time_data = raw.get("time", {})
    versions_time = [(v, t) for v, t in time_data.items() if v not in ("modified", "created")]
    versions_time.sort(key=lambda x: x[1], reverse=True)
    md.append("- **Recent versions published (latest first):**")
    for v, t in versions_time[:10]:
        md.append(f"  - `{v}` (Published: {t})")
    data = {"dist_tags": dist_tags, "recent_versions": versions_time[:15]}
    return "\n".join(md), data


def get_pypi_version_info(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    raw = fetch_url_json(url)
    if not raw:
        return f"### {package_name} PyPI versions: Failed to fetch\n", {}
    md = [f"### PyPI Registry info for {package_name}:"]
    latest = raw.get("info", {}).get("version", "N/A")
    md.append(f"- **Latest version**: {latest}")
    recent = []
    for ver, info_list in raw.get("releases", {}).items():
        if info_list:
            t = info_list[0].get("upload_time_iso_8601")
            if t:
                recent.append((ver, t))
    recent.sort(key=lambda x: x[1], reverse=True)
    md.append("- **Recent PyPI releases (latest first):**")
    for v, t in recent[:5]:
        md.append(f"  - `{v}` (Published: {t})")
    return "\n".join(md), {"latest": latest, "recent_versions": recent[:10]}


# ── OpenRouter models ────────────────────────────────────────────────────────

def get_openrouter_models():
    raw = fetch_url_json("https://openrouter.ai/api/v1/models")
    if not raw or "data" not in raw:
        return "### OpenRouter models: Failed to fetch\n", {"new_models": [], "major_models": []}

    models = raw["data"]
    md = ["### OpenRouter New & Updated Models:"]
    major_providers = ("google", "anthropic", "openai", "meta", "mistral",
                       "microsoft", "minimax", "qwen", "deepseek", "moonshotai",
                       "z-ai", "nousresearch", "x-ai", "amazon", "nvidia")

    current_model_ids = [m.get("id", "") for m in models]
    last_seen_ids = []
    if CACHE_PATH.exists():
        try:
            last_seen_ids = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Failed to read {CACHE_PATH}: {e}", file=sys.stderr)

    new_model_ids = [mid for mid in current_model_ids if mid not in last_seen_ids] if last_seen_ids else []

    def slim(m):
        return {"id": m.get("id", ""), "name": m.get("name", ""),
                "context_length": m.get("context_length"),
                "created": m.get("created"),
                "description": (m.get("description") or "")[:600]}

    new_models = [slim(m) for m in models if m.get("id") in new_model_ids]
    major_models = [slim(m) for m in models
                    if (m.get("id", "").split("/")[0] if "/" in m.get("id", "") else "") in major_providers][:40]

    md.append("\n**NEW MODELS DETECTED THIS CYCLE:**")
    if new_models:
        for nm in new_models:
            md.append(f"- **{nm['id']}** ({nm['name']}) - Context: {nm['context_length']}\n  *Description:* {nm['description'][:150]}")
    else:
        md.append("- *No new models launched since the last check.*")

    md.append("\n**All Available Major Models (Recent First):**")
    for m in major_models:
        md.append(f"- **{m['id']}** ({m['name']}) - Context: {m['context_length']}\n  *Description:* {m['description'][:150]}")

    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps(current_model_ids, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"Warning: Failed to write cache to {CACHE_PATH}: {e}", file=sys.stderr)

    return "\n".join(md), {"new_models": new_models, "major_models": major_models}


# ── Hacker News ──────────────────────────────────────────────────────────────

def get_hacker_news_topics():
    three_days_ago = int(time.time() - 3 * 24 * 3600)
    # NOTE: must use the relevance-ranked /search endpoint.
    # /search_by_date returns the newest 100 stories (~the last couple of hours),
    # which almost never clear the 35-point bar — that combination silently
    # returns zero stories.
    # 2026-07-04: Algolia removed `points` from numericAttributesForFiltering —
    # a server-side `points>=35` filter now 400s and the whole HN lane silently
    # returned zero stories (a direct contributor to the thin EP079 slate).
    # Points are filtered client-side below instead; never re-add the server
    # filter without curl-testing it first.
    url = (f"https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=100"
           f"&numericFilters=created_at_i>{three_days_ago}")
    raw = fetch_url_json(url)
    if not raw or "hits" not in raw:
        return "### Hacker News AI/Developer topics: Failed to fetch\n", []

    # Widened 2026-07-04 (EP079 rejection — "way more news, way more content"):
    # the show's beat is AI, Local AI, Compute, Models, and Harnesses, so the
    # HN filter now also catches hardware/compute and local-inference stories
    # (GPUs, accelerators, quantization, on-device runtimes) that the old
    # model/agent-only regex dropped.
    relevant = re.compile(
        r"\b(llm|llms|agent|agents|mcp|model context protocol|claude|openai|gpt|llama|gemini|deepseek|minimax|"
        r"local llm|ollama|vllm|hugging|nous|hermes|codex|agentstack|rag|vector|langchain|llamaindex|langgraph|"
        r"qwen|mistral|anthropic|transformer|inference|fine-?tun|"
        r"gpu|gpus|nvidia|cuda|rocm|npu|tpu|apple silicon|mlx|metal|"
        r"quantiz\w*|gguf|llama\.cpp|lm studio|open-webui|exo|sglang|"
        r"self-?host\w*|on-?device|edge ai|local-?first|"
        r"data ?cent(?:er|re)s?|semiconductor|accelerator|hbm|"
        r"cerebras|groq|tenstorrent|xai|grok|kimi|moonshot|zhipu|glm|"
        r"open[- ]?weights?|open[- ]?source model|diffusion|whisper|tts|"
        r"speech[- ]to[- ]text|embedding|benchmark)\b", re.IGNORECASE)

    matches = []
    for hit in raw["hits"]:
        title = hit.get("title", "") or ""
        points = hit.get("points", 0) or 0
        link = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        if points >= 35 and (relevant.search(title) or relevant.search(link)):
            matches.append({"title": title, "points": points, "url": link,
                            "comments_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}"})
    matches.sort(key=lambda x: x["points"], reverse=True)
    matches = matches[:40]

    md = ["### Hacker News Top AI/Developer Stories (Last 72 hours, Score >= 35):"]
    for m in matches:
        md.append(f"- **{m['title']}** (Score: {m['points']} points)\n  Link: {m['url']}\n  HN Comments: {m['comments_url']}")
    if not matches:
        md.append("- *No high-scoring AI/developer stories found in the last 72 hours.*")
    return "\n".join(md), matches


# ── RSS feeds ────────────────────────────────────────────────────────────────

def _regex_parse_rss_items(text, cutoff):
    """Last-resort RSS <item> extraction for feeds whose XML is malformed
    (e.g. news.smol.ai embeds unescaped HTML that breaks ElementTree)."""
    items = []
    for block in re.findall(r"<item>(.*?)</item>", text, re.DOTALL)[:20]:
        def field(tag):
            m = re.search(rf"<{tag}[^>]*>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</{tag}>",
                          block, re.DOTALL)
            return (m.group(1).strip() if m else "")
        title = re.sub(r"<[^>]+>", "", field("title"))
        link = field("link")
        desc = re.sub(r"<[^>]+>", "", field("description"))[:300]
        dt = None
        pd = field("pubDate")
        if pd:
            try:
                dt = email.utils.parsedate_to_datetime(pd)
            except Exception:
                pass
        if title and link and dt and dt > cutoff:
            items.append({"title": title, "url": link,
                          "published": dt.isoformat(), "summary": desc.strip()})
    return items


def get_rss_feeds():
    # Roster expanded 2026-07-04 (EP079 rejection — "way more news, way more
    # content"). The show's beat is AI / Local AI / Compute / Models /
    # Harnesses, so the feed pool now covers five lanes: frontier labs,
    # open-model + local-inference projects, compute/hardware press,
    # practitioner commentary, and general AI tech press. Broad feeds carry a
    # relevance filter (regex applied to title+summary) so hardware/press
    # noise doesn't flood the candidate pool — filtered items never reach the
    # builder, and the builder's own scoring handles the rest.
    ai_filter = re.compile(
        r"\b(ai|llm|llms|gpu|gpus|model|models|inference|agent|agents|neural|"
        r"machine learning|deep learning|transformer|accelerator|cuda|rocm|"
        r"data ?cent(?:er|re)s?|hbm|chip|chips|semiconductor|npu|tpu|nvidia|"
        r"openai|anthropic|claude|gemini|llama|qwen|deepseek|mistral|"
        r"training|foundation model|generative|copilot|quantiz\w*)\b",
        re.IGNORECASE)
    feeds = {
        # Frontier lab + partner announcement lanes
        "OpenAI News": ("https://openai.com/news/rss.xml", None),
        "Google AI Blog": ("https://blog.google/innovation-and-ai/technology/ai/rss/", None),
        "Mistral AI Blog": ("https://mistral.ai/rss.xml", None),
        "DeepMind Blog": ("https://deepmind.google/blog/feed/", None),
        "Microsoft Research Blog": ("https://www.microsoft.com/en-us/research/feed/", ai_filter),
        "Qwen Blog": ("https://qwenlm.github.io/blog/index.xml", None),
        # Open models + local inference projects (Local AI lane)
        "Hugging Face Blog": ("https://huggingface.co/blog/feed.xml", None),
        # Compute / hardware lane
        "NVIDIA Blog": ("https://blogs.nvidia.com/feed/", ai_filter),
        "ServeTheHome": ("https://www.servethehome.com/feed/", ai_filter),
        "HPCwire": ("https://www.hpcwire.com/feed/", ai_filter),
        "SemiAnalysis": ("https://semianalysis.com/feed/", None),
        # Practitioner commentary + curated developer signal
        "Simon Willison's Weblog": ("https://simonwillison.net/atom/entries/", None),
        "Latent Space": ("https://www.latent.space/feed", None),
        "Interconnects": ("https://www.interconnects.ai/feed", None),
        "Import AI": ("https://importai.substack.com/feed", None),
        "AI News (smol.ai)": ("https://news.smol.ai/rss.xml", None),
        "Lobsters AI tag": ("https://lobste.rs/t/ai.rss", None),
        # General AI tech press
        "TechCrunch AI": ("https://techcrunch.com/category/artificial-intelligence/feed/", None),
        # No trailing slash — the trailing-slash URL 308s and urllib on 3.9
        # doesn't follow 308 redirects.
        "VentureBeat AI": ("https://venturebeat.com/category/ai/feed", None),
        "Ars Technica AI": ("https://arstechnica.com/ai/feed/", None),
        "The Register AI/ML": ("https://www.theregister.com/software/ai_ml/headlines.atom", None),
        "MarkTechPost": ("https://www.marktechpost.com/feed/", None),
    }
    md = ["### Major AI Lab, Local-AI, Compute & Developer Blog RSS Announcements (Last 72 Hours):"]
    data = {}
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=3)

    # Fetch all feeds in parallel — the roster is now 25 feeds and a serial
    # loop with 15s timeouts risks blowing the fresh-research gate's gather
    # budget when several hosts hang.
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as pool:
        fetched = dict(zip(feeds.keys(),
                           pool.map(lambda nu: fetch_url(nu[0]),
                                    feeds.values())))

    for name, (url, item_filter) in feeds.items():
        xml_data = fetched.get(name)
        items = []
        if not xml_data:
            md.append(f"\n#### {name} feed: Failed to fetch")
            data[name] = items
            continue
        md.append(f"\n#### Latest from {name}:")
        try:
            root = ET.fromstring(xml_data)
            rss_items = root.findall(".//item")
            if rss_items:
                for item in rss_items:
                    title = item.findtext("title", default="Untitled").strip()
                    link = (item.findtext("link") or "").strip()
                    desc = re.sub(r"<[^>]+>", "", item.findtext("description", default="") or "")[:300]
                    dt = None
                    pd = item.findtext("pubDate")
                    if pd:
                        try:
                            dt = email.utils.parsedate_to_datetime(pd)
                        except Exception:
                            pass
                    if dt and dt > cutoff:
                        items.append({"title": title, "url": link, "published": dt.isoformat(), "summary": desc.strip()})
            else:
                ns = "{http://www.w3.org/2005/Atom}"

                def find_first(parent, *names):
                    # Element truthiness is child-count, so `el or fallback` is a
                    # trap: an element with text but no children is falsy. Compare
                    # against None explicitly.
                    for n in names:
                        el = parent.find(n)
                        if el is not None:
                            return el
                    return None

                entries = root.findall(f".//{ns}entry")
                if not entries:
                    entries = root.findall(".//entry")
                for entry in entries:
                    title_el = find_first(entry, f"{ns}title", "title")
                    title = (title_el.text or "Untitled").strip() if title_el is not None else "Untitled"
                    link = ""
                    link_el = find_first(entry, f"{ns}link", "link")
                    if link_el is not None:
                        link = link_el.attrib.get("href", "") or (link_el.text or "").strip()
                    summary_el = find_first(entry, f"{ns}summary", f"{ns}content", "summary", "content")
                    desc = re.sub(r"<[^>]+>", "", summary_el.text or "")[:300] if (summary_el is not None and summary_el.text) else ""
                    pub_el = find_first(entry, f"{ns}published", f"{ns}updated", "published", "updated")
                    dt = None
                    if pub_el is not None and pub_el.text:
                        try:
                            dt = datetime.fromisoformat(pub_el.text.replace("Z", "+00:00"))
                        except Exception:
                            pass
                    if dt and dt > cutoff:
                        items.append({"title": title, "url": link, "published": dt.isoformat(), "summary": desc.strip()})
        except Exception as e:
            # Malformed XML (unescaped HTML entities etc.) — fall back to a
            # regex item extractor before giving up on the feed.
            items = _regex_parse_rss_items(
                xml_data.decode("utf-8", errors="ignore"), cutoff)
            if not items:
                md.append(f"- *Failed to parse feed elements: {e}*")

        if item_filter is not None:
            items = [it for it in items
                     if item_filter.search(it["title"] + " " + it.get("summary", ""))]
        items = items[:15]  # per-feed cap so one prolific press feed can't drown the pool
        for it in items:
            md.append(f"- **{it['title']}** (Published: {it['published']})\n  Link: {it['url']}\n  Summary: {it['summary']}")
        if not items:
            md.append("- *No announcements found in the last 72 hours.*")
        data[name] = items
    return "\n".join(md), data


# ── Academic & research papers (arXiv + HuggingFace Daily Papers) ──────────
# Locked 2026-06-30, post-EP076 feedback (wider-reach research signal).
# Two parallel lanes: arXiv API for cs.AI / cs.CL / cs.LG submissions from the
# last 7 days, plus HuggingFace Daily Papers (community-upvoted, what the AI/ML
# community is actually reading). Both return title + summary + primary URL
# + upvote/community signal. The point of widening the gather pool is to give
# the show-notes builder concrete research/benchmark stories that are not just
# vendor news releases.

def _parse_arxiv_atom(xml_bytes):
    """Parse arXiv API Atom response. Returns list of paper dicts."""
    ns = "{http://www.w3.org/2005/Atom}"
    out = []
    try:
        root = ET.fromstring(xml_bytes)
    except Exception:
        return out
    for entry in root.findall(f"{ns}entry"):
        title_el = entry.find(f"{ns}title")
        title = (title_el.text or "").strip() if title_el is not None else ""
        # arXiv wraps title in newlines; collapse
        title = re.sub(r"\s+", " ", title)
        summary_el = entry.find(f"{ns}summary")
        summary = (summary_el.text or "").strip() if summary_el is not None else ""
        summary = re.sub(r"\s+", " ", summary)
        id_el = entry.find(f"{ns}id")
        arxiv_id = ""
        arxiv_url = ""
        if id_el is not None and id_el.text:
            arxiv_id = id_el.text.strip().split("/")[-1].replace("v1", "").replace("v2", "")
            arxiv_url = f"https://arxiv.org/abs/{arxiv_id}"
        published_el = entry.find(f"{ns}published")
        published = (published_el.text or "").strip() if published_el is not None else ""
        authors = []
        for a in entry.findall(f"{ns}author/{ns}name"):
            if a.text:
                authors.append(a.text.strip())
        if title and arxiv_url:
            out.append({"title": title, "url": arxiv_url, "arxiv_id": arxiv_id,
                        "published": published, "summary": summary[:1500],
                        "authors": authors[:8]})
    return out


def get_arxiv_recent_papers():
    """Fetch the last 7 days of arXiv submissions in cs.AI / cs.CL / cs.LG."""
    # arXiv API supports up to 50 results per call and category-filtered queries.
    # We pick the union of the three core AI/ML categories and sort by submittedDate.
    url = ("https://export.arxiv.org/api/query?search_query="
           "cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.LG"
           "&sortBy=submittedDate&sortOrder=descending&max_results=60")
    xml_data = fetch_url(url)
    if not xml_data:
        return "### arXiv recent submissions: Failed to fetch\n", []
    papers = _parse_arxiv_atom(xml_data)
    # Filter for last 7 days to keep slate fresh
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    fresh = []
    for p in papers:
        if p["published"]:
            try:
                dt = datetime.fromisoformat(p["published"].replace("Z", "+00:00"))
                if dt >= cutoff:
                    fresh.append(p)
            except Exception:
                fresh.append(p)  # include if unparseable
    md = ["### arXiv recent AI/ML submissions (cs.AI / cs.CL / cs.LG, last 7 days):"]
    for p in fresh[:35]:
        md.append(f"- **{p['title']}**\n  Authors: {', '.join(p['authors'][:4])}\n"
                  f"  Published: {p['published']}\n  URL: {p['url']}\n"
                  f"  Abstract preview: {p['summary'][:300]}")
    if not fresh:
        md.append("- *No arXiv papers in the last 7 days.*")
    return "\n".join(md), fresh[:35]


def get_huggingface_papers():
    """Fetch HuggingFace Daily Papers — community-upvoted research highlights."""
    # The /api/papers?days=7 endpoint returns a JSON array of paper objects
    # {id, title, upvotes, ai_summary, projectPage, githubRepo, authors, ...}.
    # Upvotes are a useful filter for "what the practitioner community is
    # actually reading" — analogous to HN points.
    url = "https://huggingface.co/api/papers?days=7"
    raw = fetch_url_json(url)
    if not raw or not isinstance(raw, list):
        return "### HuggingFace Daily Papers: Failed to fetch\n", []
    papers = []
    for item in raw[:40]:
        if not isinstance(item, dict):
            continue
        arxiv_id = item.get("id", "")
        title = (item.get("title") or "").strip()
        if not (title and arxiv_id):
            continue
        upvotes = item.get("upvotes", 0) or 0
        ai_summary = (item.get("ai_summary") or "").strip()
        summary = (item.get("summary") or "").strip()
        project_page = item.get("projectPage", "")
        github_repo = item.get("githubRepo", "")
        authors = [a.get("name", "") for a in (item.get("authors") or []) if a.get("name")][:4]
        # Use the arXiv URL as canonical primary source.
        url_paper = f"https://arxiv.org/abs/{arxiv_id}"
        if project_page:
            url_paper = project_page  # prefer project page if present
        elif github_repo:
            url_paper = github_repo
        papers.append({"title": title, "url": url_paper,
                       "arxiv_id": arxiv_id, "upvotes": upvotes,
                       "ai_summary": ai_summary[:500],
                       "summary": summary[:500], "authors": authors,
                       "published": item.get("publishedAt", "")})
    papers.sort(key=lambda x: x["upvotes"], reverse=True)
    md = ["### HuggingFace Daily Papers (last 7 days, sorted by community upvotes):"]
    for p in papers[:30]:
        md.append(f"- **{p['title']}** (↑{p['upvotes']} HF upvotes)\n"
                  f"  Authors: {', '.join(p['authors'][:4])}\n"
                  f"  URL: {p['url']}\n"
                  f"  Summary: {(p['ai_summary'] or p['summary'])[:300]}")
    if not papers:
        md.append("- *No HuggingFace Daily Papers in the last 7 days.*")
    return "\n".join(md), papers[:30]


# ── GitHub Trending (HTML scrape, narrow to AI/agent topics) ─────────────────
# Locked 2026-06-30 — GitHub trending pages surface fresh AI/agent repos that
# the topic-search GitHub Radar lane misses (e.g. utilities that aren't yet
# tagged model-context-protocol). HTML scrape only — no API endpoint for
# trending.

def get_github_trending():
    """Scrape github.com/trending for today + weekly AI/agent repos."""
    md = ["### GitHub Trending (today + this week, AI/agent adjacent):"]
    data = []
    seen = set()
    for timeframe in ("daily", "weekly"):
        url = f"https://github.com/trending?since={timeframe}"
        # GitHub trending returns HTML; use a Mozilla UA so we get the
        # full repo list (their feed serves the table to any UA).
        html = fetch_url(url, headers={"Accept-Language": "en-US,en;q=0.9"})
        if not html:
            md.append(f"- *github.com/trending ({timeframe}): Failed to fetch*")
            continue
        try:
            text = html.decode("utf-8", errors="ignore")
        except Exception:
            text = ""
        # Each trending card is an <article class="Box-row"> with an <h2>
        # containing <a href="/owner/repo">. Description + star counts follow
        # in sibling <p>/<span> blocks within the same article.
        for m in re.finditer(
            r'<h2[^>]*>\s*<a[^>]*href="/([^"/\?]+/[^"/\?]+)"[^>]*>(.*?)</a>',
            text, re.DOTALL):
            slug = m.group(1).strip()
            name_raw = re.sub(r"<[^>]+>", " ", m.group(2))
            name = re.sub(r"\s+", " ", name_raw).strip()
            if not slug or "/" not in slug:
                continue
            if slug in seen:
                continue
            # Filter to AI/agent/ML/dev-tool topics. The whole list is huge,
            # so we only include repos whose name or slug contains a signal
            # word OR whose description (best-effort) matches.
            slug_lower = slug.lower()
            name_lower = name.lower()
            ai_signal = re.compile(
                r"(agent|llm|gpt|claude|gemini|llama|mistral|qwen|deepseek|"
                r"minimax|hermes|openclaw|mcp|model[- ]context|rag|vector|"
                r"embed|inference|transformer|fine[- ]tun|prompt|tool[- ]use|"
                r"codex|copilot|cursor|diffusion|speech|tts|stt|asr|"
                r"stable[- ]diffusion|sdxl|dalle|whisper|llamaindex|langchain|"
                r"langgraph|semantic[- ]kernel|haystack|chroma|qdrant|weaviate|"
                r"milvus|vllm|sglang|tgi|text[- ]generation|llamacpp|ollama|"
                r"lmstudio|unsloth|axolotl|trl|peft|bitsandbytes|deepspeed|"
                r"megatron|flash[- ]attn|sgl[- ]ang|llama\.cpp|gpt4all|"
                r"openai|anthropic|huggingface|gradio|streamlit|"
                r"router|strix|berkshire|"
                r"video[- ]use|browser[- ]use|cupp|omni|free[- ]for[- ]dev)"
            )
            if not (ai_signal.search(slug_lower) or ai_signal.search(name_lower)):
                continue
            seen.add(slug)
            # Try to grab description (best-effort)
            desc_m = re.search(
                r'<p class="col-9[^"]*"[^>]*>(.+?)</p>', text[m.end():m.end()+3000],
                re.DOTALL)
            desc = ""
            if desc_m:
                desc = re.sub(r"<[^>]+>", "", desc_m.group(1)).strip()
            # Star deltas appear within the article block as "+N stars today/this week".
            stars_m = re.search(
                r'(\d+(?:,\d+)*)\s*stars today',
                text[m.end():m.end()+3000])
            stars = ""
            if stars_m:
                stars = f"+{stars_m.group(1)} stars/{timeframe}"
            if not desc and not stars:
                continue
            md.append(f"- **{slug}** {stars}\n  URL: https://github.com/{slug}\n"
                      f"  Description: {desc[:200] if desc else '(no description)'}")
            data.append({"full_name": slug, "url": f"https://github.com/{slug}",
                         "trending_stars": stars,
                         "description": desc[:400], "timeframe": timeframe})
        if len(data) >= 20:
            break
    if not data:
        md.append("- *No AI/agent-adjacent repos in GitHub Trending.*")
    return "\n".join(md), data[:20]


# ── Reddit local-AI communities (Local AI lane) ─────────────────────────────
# Added 2026-07-04 (EP079 rejection — "way more news, way more content").
# r/LocalLLaMA is the highest-signal community for the show's Local AI /
# Compute pillars: new open-weight drops, quantization results, local
# hardware benchmarks, and runtime releases surface there hours before the
# press covers them. Public .json endpoints, no auth; soft-fail on 403.

def get_reddit_top():
    # Reddit hard-blocks the unauthenticated .json API (403 regardless of UA,
    # verified 2026-07-04), but the Atom feed at /top/.rss serves fine with
    # browser-shaped headers. The feed is already sorted top-of-day, so rank
    # order stands in for the score the JSON API would have given us.
    subreddits = ["LocalLLaMA", "LocalLLM", "MachineLearning", "ollama"]
    per_sub = 8
    ns = "{http://www.w3.org/2005/Atom}"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/126.0.0.0 Safari/537.36"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    md = ["### Reddit local-AI community signal (top of last 24h, rank-ordered):"]
    data = []
    for i, sub in enumerate(subreddits):
        # Reddit 429s back-to-back unauthenticated requests; space them out
        # and retry once on failure (verified 2026-07-04).
        if i:
            time.sleep(10)
        url = f"https://www.reddit.com/r/{sub}/top/.rss?t=day"
        xml_data = fetch_url(url, headers=dict(headers))
        if not xml_data:
            time.sleep(15)
            xml_data = fetch_url(url, headers=dict(headers))
        posts = []
        if xml_data:
            try:
                root = ET.fromstring(xml_data)
                for rank, entry in enumerate(root.findall(f"{ns}entry")):
                    title_el = entry.find(f"{ns}title")
                    title = (title_el.text or "").strip() if title_el is not None else ""
                    if not title:
                        continue
                    link_el = entry.find(f"{ns}link")
                    permalink = link_el.attrib.get("href", "") if link_el is not None else ""
                    content_el = entry.find(f"{ns}content")
                    content_html = (content_el.text or "") if content_el is not None else ""
                    # Link posts carry the external target as the [link] anchor;
                    # self posts point [link] back at the permalink.
                    ext_url = permalink
                    m = re.search(r'<a href="([^"]+)">\s*\[link\]', content_html)
                    if m and "reddit.com" not in m.group(1):
                        ext_url = m.group(1)
                    preview = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", content_html)).strip()
                    preview = re.sub(r"submitted by\s+/u/\S+.*$", "", preview).strip()
                    pub_el = entry.find(f"{ns}published")
                    if pub_el is None:
                        pub_el = entry.find(f"{ns}updated")
                    posts.append({"title": title, "rank": rank + 1,
                                  "subreddit": sub,
                                  "url": ext_url, "permalink": permalink,
                                  "published": (pub_el.text or "").strip() if pub_el is not None else "",
                                  "preview": preview[:400]})
                    if len(posts) >= per_sub:
                        break
            except Exception as e:
                print(f"Warning: Failed to parse r/{sub} feed: {e}", file=sys.stderr)
        md.append(f"\n#### r/{sub} (top of day):")
        for p in posts:
            md.append(f"- **{p['title']}** (#{p['rank']} on r/{sub} today)\n"
                      f"  Link: {p['url']}\n  Thread: {p['permalink']}\n"
                      f"  Preview: {p['preview'][:200]}")
        if not posts:
            md.append("- *No posts (fetch failed or feed empty).*")
        data.extend(posts)
    return "\n".join(md), data


# ── HuggingFace trending models (Models / Local AI lane) ────────────────────
# Added 2026-07-04. New open-weight model drops trend on the HF hub
# immediately — usually a full news cycle before RSS/press coverage. GGUF /
# quantized variants trending is itself a Local AI story signal.

def get_hf_trending_models():
    url = "https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=30"
    raw = fetch_url_json(url)
    if not raw or not isinstance(raw, list):
        return "### HuggingFace trending models: Failed to fetch\n", []
    md = ["### HuggingFace Trending Models (by trending score):"]
    data = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        mid = item.get("id") or item.get("modelId") or ""
        if not mid:
            continue
        tags = item.get("tags") or []
        data.append({
            "id": mid,
            "url": f"https://huggingface.co/{mid}",
            "pipeline_tag": item.get("pipeline_tag", ""),
            "likes": item.get("likes", 0) or 0,
            "downloads": item.get("downloads", 0) or 0,
            "created_at": item.get("createdAt", ""),
            "is_gguf": any("gguf" in str(t).lower() for t in tags),
            "tags": [str(t) for t in tags[:12]],
        })
    for m in data[:25]:
        gguf = " [GGUF]" if m["is_gguf"] else ""
        md.append(f"- **{m['id']}**{gguf} ({m['pipeline_tag'] or 'n/a'}) — "
                  f"{m['likes']} likes, {m['downloads']} downloads\n"
                  f"  URL: {m['url']}\n  Created: {m['created_at']}")
    if not data:
        md.append("- *No trending models returned.*")
    return "\n".join(md), data[:25]


# ── GitHub Project Radar ─────────────────────────────────────────────────────

def get_github_radar_suggestions():
    results = []
    md = ["### GitHub Project Radar Repo Candidates (Trending/MCP/Agent Tools):"]
    queries = [
        ("topic:model-context-protocol", "stars"),
        ("topic:ai-agents pushed:>" + (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%d"), "stars"),
    ]
    seen = set()
    for q, sort in queries:
        url = (f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}"
               f"&sort={sort}&order=desc&per_page=25")
        raw = fetch_url_json(url)
        if not raw or "items" not in raw:
            continue
        for item in raw.get("items", []):
            if not isinstance(item, dict):
                continue
            owner_login = item.get("owner", {}).get("login", "").lower()
            if owner_login in ("github", "git"):
                continue
            full_name = item.get("full_name", "")
            if full_name in seen:
                continue
            seen.add(full_name)
            results.append({"full_name": full_name,
                            "url": item.get("html_url", ""),
                            "stars": item.get("stargazers_count", 0),
                            "description": (item.get("description") or "No description provided.")[:300],
                            "pushed_at": item.get("pushed_at", "")})
            if len(results) >= 16:
                break
        if len(results) >= 16:
            break
    for r in results:
        md.append(f"- **{r['full_name']}** ({r['stars']} stars)\n  URL: {r['url']}\n  Description: {r['description']}")
    return "\n".join(md), results


def main():
    print("Gathering research context for show notes...")
    md_sections = []
    payload: dict = {"generated_at": datetime.now(timezone.utc).isoformat()}

    md, payload["recent_episodes"] = get_recent_episodes_context()
    md_sections.append(md)

    # EP075-incident-class guard (locked 2026-06-27). The fresh-research
    # gate (scripts/fresh_research_gate.py) refuses to build the next
    # episode unless it sees a YouTube counter signal that has advanced
    # since the prior released episode. We populate those fields here so
    # the gate has something to read; the actual hard-fail is in the
    # gate, not in the gatherer.
    youtube_done = PODCAST_DIR / "scripts" / "youtube_uploaded.txt"
    if youtube_done.exists():
        try:
            last_line = youtube_done.read_text(errors="replace").strip().splitlines()
            last_eps = [int(x.strip()) for x in last_line if x.strip().isdigit()]
            if last_eps:
                # The fresh-research gate (scripts/fresh_research_gate.py)
                # compares these against the prior released episode number
                # (also an int). We store them as ints; the gate and the
                # gatherer agree on the type.
                payload["last_uploaded_episode"] = int(max(last_eps))
                payload["youtube_upload_count"] = int(len(last_eps))
        except Exception:
            pass
    if payload.get("last_uploaded_episode") is None and payload.get("recent_episodes"):
        # Fallback: the highest-numbered released show notes file is the
        # last released episode. The YouTube channel is the source of
        # truth normally; the show-notes file system is a backup for
        # environments where the channel sync has not run.
        try:
            payload["last_uploaded_episode"] = int(max(
                int(ep["episode"]) for ep in payload["recent_episodes"]
            ))
        except Exception:
            pass

    md_sections.append("# UPSTREAM GITHUB RELEASES")
    payload["github_releases"] = {}
    for owner, repo in [("openclaw", "openclaw"), ("NousResearch", "hermes-agent"),
                        ("openai", "codex"), ("ollama", "ollama")]:
        md, rel = get_github_releases(owner, repo)
        md_sections.append(md)
        payload["github_releases"][f"{owner}/{repo}"] = rel

    # Local-AI / inference-infrastructure releases (Local AI + Compute lanes,
    # added 2026-07-04). Deliberately a SEPARATE payload key from
    # github_releases: these are news candidates, not harness lanes — the
    # builder's LANES whitelist and release-coverage QC must never treat
    # them as harness releases.
    md_sections.append("# LOCAL-AI / INFERENCE INFRA RELEASES")
    payload["infra_releases"] = {}
    for owner, repo in [("vllm-project", "vllm"), ("sgl-project", "sglang"),
                        ("open-webui", "open-webui"),
                        ("comfyanonymous", "ComfyUI"),
                        ("huggingface", "transformers"),
                        ("mudler", "LocalAI"),
                        ("exo-explore", "exo")]:
        md, rel = get_github_releases(owner, repo)
        md_sections.append(md)
        # News candidates only need the few most recent releases; keep the
        # payload lean (7 repos × 15 full bodies would triple the JSON).
        rel = rel[:5]
        for r in rel:
            r["body"] = (r.get("body") or "")[:2000]
        payload["infra_releases"][f"{owner}/{repo}"] = rel

    md_sections.append("# NPM REGISTRY VERSIONS")
    payload["npm"] = {}
    for pkg in ["@anthropic-ai/claude-code", "@google/antigravity"]:
        md, info = get_npm_version_info(pkg)
        md_sections.append(md)
        payload["npm"][pkg] = info

    md_sections.append("# PYPI REGISTRY VERSIONS")
    payload["pypi"] = {}
    for pkg in ["litellm", "vllm"]:
        md, info = get_pypi_version_info(pkg)
        md_sections.append(md)
        payload["pypi"][pkg] = info

    md_sections.append("# OPENROUTER MODELS")
    md, payload["openrouter"] = get_openrouter_models()
    md_sections.append(md)

    md_sections.append("# HACKER NEWS DEVELOPER DISCUSSIONS")
    md, payload["hackernews"] = get_hacker_news_topics()
    md_sections.append(md)

    md_sections.append("# PRIMARY LAB RSS ANNOUNCEMENTS")
    md, payload["rss"] = get_rss_feeds()
    md_sections.append(md)

    md_sections.append("# ARXIV RECENT SUBMISSIONS")
    md, payload["arxiv_papers"] = get_arxiv_recent_papers()
    md_sections.append(md)

    md_sections.append("# HUGGINGFACE DAILY PAPERS")
    md, payload["huggingface_papers"] = get_huggingface_papers()
    md_sections.append(md)

    md_sections.append("# REDDIT LOCAL-AI COMMUNITIES")
    md, payload["reddit"] = get_reddit_top()
    md_sections.append(md)

    md_sections.append("# HUGGINGFACE TRENDING MODELS")
    md, payload["hf_trending_models"] = get_hf_trending_models()
    md_sections.append(md)

    md_sections.append("# GITHUB TRENDING (AI/AGENT ADJACENT)")
    md, payload["github_trending"] = get_github_trending()
    md_sections.append(md)

    md_sections.append("# GITHUB PROJECT RADAR SUGGESTIONS")
    md, payload["github_radar"] = get_github_radar_suggestions()
    md_sections.append(md)

    # Empty-lane sanity check (added 2026-07-04): the HN lane silently
    # returned zero stories for days after Algolia dropped server-side
    # `points` filtering — a soft per-fetch warning was the only trace, and
    # thin slates shipped. Loudly flag any core lane that comes back empty
    # so the run log shows lane health at a glance.
    core_lanes = {
        "hackernews": len(payload.get("hackernews", [])),
        "rss (all feeds combined)": sum(len(v) for v in payload.get("rss", {}).values()),
        "arxiv_papers": len(payload.get("arxiv_papers", [])),
        "huggingface_papers": len(payload.get("huggingface_papers", [])),
        "hf_trending_models": len(payload.get("hf_trending_models", [])),
        "reddit": len(payload.get("reddit", [])),
        "github_trending": len(payload.get("github_trending", [])),
        "github_radar": len(payload.get("github_radar", [])),
    }
    for lane, n in sorted(core_lanes.items()):
        print(f"lane {lane}: {n} items")
        if n == 0:
            print(f"WARNING: research lane '{lane}' returned ZERO items — "
                  f"check whether the upstream API/feed contract changed "
                  f"(cf. 2026-07-04 HN Algolia points-filter removal).",
                  file=sys.stderr)

    try:
        OUTPUT_MD.write_text("\n\n---\n\n".join(md_sections), encoding="utf-8")
        OUTPUT_JSON.write_text(json.dumps(payload, indent=1), encoding="utf-8")
        print(f"Wrote {OUTPUT_MD} and {OUTPUT_JSON}")
    except Exception as e:
        print(f"Error: Failed to write output: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
