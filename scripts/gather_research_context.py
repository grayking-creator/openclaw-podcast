#!/usr/bin/env python3
"""
Gather Research Context — deterministic pre-flight data collection.

Collects past show-notes covered versions, Hacker News AI/dev news, frontier
lab RSS feeds, GitHub releases, OpenRouter model diffs, and package registry
versions. Writes BOTH:

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
    # NOTE: must use the relevance-ranked /search endpoint with a points filter.
    # /search_by_date returns the newest 100 stories (~the last couple of hours),
    # which almost never clear the 35-point bar — that combination silently
    # returns zero stories.
    url = (f"https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=100"
           f"&numericFilters=created_at_i>{three_days_ago},points>=35")
    raw = fetch_url_json(url)
    if not raw or "hits" not in raw:
        return "### Hacker News AI/Developer topics: Failed to fetch\n", []

    relevant = re.compile(
        r"\b(llm|llms|agent|agents|mcp|model context protocol|claude|openai|gpt|llama|gemini|deepseek|minimax|"
        r"local llm|ollama|vllm|hugging|nous|hermes|codex|agentstack|rag|vector|langchain|llamaindex|langgraph|"
        r"qwen|mistral|anthropic|transformer|inference|fine-?tun)\b", re.IGNORECASE)

    matches = []
    for hit in raw["hits"]:
        title = hit.get("title", "") or ""
        points = hit.get("points", 0) or 0
        link = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        if points >= 35 and (relevant.search(title) or relevant.search(link)):
            matches.append({"title": title, "points": points, "url": link,
                            "comments_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}"})
    matches.sort(key=lambda x: x["points"], reverse=True)
    matches = matches[:25]

    md = ["### Hacker News Top AI/Developer Stories (Last 72 hours, Score >= 35):"]
    for m in matches:
        md.append(f"- **{m['title']}** (Score: {m['points']} points)\n  Link: {m['url']}\n  HN Comments: {m['comments_url']}")
    if not matches:
        md.append("- *No high-scoring AI/developer stories found in the last 72 hours.*")
    return "\n".join(md), matches


# ── RSS feeds ────────────────────────────────────────────────────────────────

def get_rss_feeds():
    feeds = {
        "OpenAI News": "https://openai.com/news/rss.xml",
        "Simon Willison's Weblog": "https://simonwillison.net/atom/entries/",
        "Latent Space": "https://www.latent.space/feed",
        "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    }
    md = ["### Major AI Lab & Developer Blog RSS Announcements (Last 72 Hours):"]
    data = {}
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=3)

    for name, url in feeds.items():
        xml_data = fetch_url(url)
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
            md.append(f"- *Failed to parse feed elements: {e}*")

        for it in items:
            md.append(f"- **{it['title']}** (Published: {it['published']})\n  Link: {it['url']}\n  Summary: {it['summary']}")
        if not items:
            md.append("- *No announcements found in the last 72 hours.*")
        data[name] = items
    return "\n".join(md), data


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
    payload = {"generated_at": datetime.now(timezone.utc).isoformat()}

    md, payload["recent_episodes"] = get_recent_episodes_context()
    md_sections.append(md)

    md_sections.append("# UPSTREAM GITHUB RELEASES")
    payload["github_releases"] = {}
    for owner, repo in [("openclaw", "openclaw"), ("NousResearch", "hermes-agent"),
                        ("openai", "codex"), ("ollama", "ollama")]:
        md, rel = get_github_releases(owner, repo)
        md_sections.append(md)
        payload["github_releases"][f"{owner}/{repo}"] = rel

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

    md_sections.append("# GITHUB PROJECT RADAR SUGGESTIONS")
    md, payload["github_radar"] = get_github_radar_suggestions()
    md_sections.append(md)

    try:
        OUTPUT_MD.write_text("\n\n---\n\n".join(md_sections), encoding="utf-8")
        OUTPUT_JSON.write_text(json.dumps(payload, indent=1), encoding="utf-8")
        print(f"Wrote {OUTPUT_MD} and {OUTPUT_JSON}")
    except Exception as e:
        print(f"Error: Failed to write output: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
