#!/usr/bin/env python3
"""
build_episode.py — Pre-greenlight episode builder.

Runs everything needed before ARIA posts review assets to Discord:
  1. Verify transcript matches the approved story slate from show notes.
  2. Run QC (check_episode.py) — blocks on any ERROR.
  3. Render nova transcript (render_nova.py).
  4. Generate EN audio.
  5. Generate EN cover art (from show notes title).
  6. Copy audio + cover to CDN repo.
  7. Post review URLs to Discord episode channel, then stop for approval.

Does NOT proceed to site/feed publish, translations, or YouTube — that's release_episode_approved.py after approval.

Usage:
    python3 scripts/build_episode.py 29
    python3 scripts/build_episode.py 29 --force-audio   # regenerate even if audio exists
    python3 scripts/build_episode.py 29 --skip-discord  # skip Discord post (dry-run)
"""

import argparse
import asyncio
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
CDN_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio"
CDN_REPO = "clawdassistant85-netizen/openclaw-podcast-audio"
DISCORD_GUILD_ID = "1475905694145318944"
BUILD_LOG_CHANNEL = "1485243812442804327"
GITHUB_PAGES_SITE_LIMIT_BYTES = 1024 * 1024 * 1024
PAGES_BUILD_POLL_SECONDS = 30
PAGES_BUILD_TIMEOUT_SECONDS = 1800
URL_VERIFY_RETRY_WAIT_SECONDS = 30
URL_VERIFY_MAX_ATTEMPTS = 10


def log(msg):
    print(msg, flush=True)


def post_build_log(msg, token=None):
    """Post a progress or failure message to the build-log Discord channel."""
    try:
        _token = token or load_env_key("DISCORD_BOT_TOKEN")
        data = json.dumps({"content": msg}).encode()
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{BUILD_LOG_CHANNEL}/messages",
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bot {_token}",
                "Content-Type": "application/json",
                "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
            },
        )
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception as e:
        log(f"⚠️  build-log post failed: {e}")


def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd or PODCAST_DIR)
    if result.returncode != 0:
        raise SystemExit(f"❌ Command failed: {' '.join(str(c) for c in cmd)}")


def load_env_key(name):
    env_file = Path.home() / ".openclaw/.env"
    for line in env_file.read_text().splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip()
    return ""


# ── Step 1: Story slate verification ────────────────────────────────────────

def verify_story_slate(ep_num):
    """
    Verify that the transcript matches the approved story slate from show notes.
    This is the safeguard against using a stale/wrong transcript file.
    """
    ep_str = f"{ep_num:03d}"
    transcript = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript.md"
    show_notes = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"

    if not show_notes.exists():
        raise SystemExit(f"❌ Show notes missing: {show_notes.name}\n   Write show notes before building.")

    if not transcript.exists():
        raise SystemExit(
            f"❌ Transcript missing: {transcript.name}\n"
            f"   Write the transcript from the approved story slate in show_notes_episode_{ep_str}.md first."
        )

    # Extract story titles from the Story Slate section
    notes_text = show_notes.read_text()
    slate_m = re.search(r"## Story Slate\s*\n(.*?)(?=\n##|\Z)", notes_text, re.DOTALL)
    if not slate_m:
        log("⚠️  No '## Story Slate' section in show notes — skipping slate check")
        return 0

    story_titles = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", slate_m.group(1), re.MULTILINE)
    if not story_titles:
        log("⚠️  No numbered story titles in Story Slate — skipping slate check")
        return 0

    transcript_text = transcript.read_text().lower()
    missing = []
    for title in story_titles:
        # Strip everything after an em-dash (subtitle/detail) and check 3-word phrase
        core = re.sub(r"[—–].*", "", title).strip()
        words = core.lower().split()
        if len(words) >= 3:
            # Check that at least 3 consecutive words appear in the transcript
            phrase = " ".join(words[:3])
            if phrase not in transcript_text:
                missing.append(title)
        elif words:
            if words[0] not in transcript_text:
                missing.append(title)

    if missing:
        msg = (
            f"❌ EP{ep_str} build failed — story slate mismatch\n"
            + "\n".join(f"  • {s}" for s in missing)
            + f"\nTranscript does not match approved slate in show_notes_episode_{ep_str}.md"
        )
        log(msg)
        post_build_log(msg)
        raise SystemExit(1)

    log(f"✅ Story slate verified ({len(story_titles)} stories match transcript)")
    return len(story_titles)


# ── Step 2+3: QC + nova render ───────────────────────────────────────────────

def run_qc(ep_num):
    ep_str = f"{ep_num:03d}"
    transcript = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript.md"
    log(f"\n── QC ──────────────────────────────────────────────────────────────────")
    run([sys.executable, str(SCRIPTS_DIR / "check_episode.py"), str(transcript)])
    log(f"✅ QC passed")


def render_nova(ep_num):
    ep_str = f"{ep_num:03d}"
    transcript = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript.md"
    log(f"\n── Render nova ─────────────────────────────────────────────────────────")
    post_build_log(f"🎙 EP{ep_str} [3/6] Rendering nova transcript…")
    run([sys.executable, str(SCRIPTS_DIR / "render_nova.py"), str(transcript)])
    nova = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript_nova.md"
    if not nova.exists():
        post_build_log(f"❌ EP{ep_str} [3/6] render_nova.py ran but {nova.name} not found")
        raise SystemExit(f"❌ render_nova.py ran but {nova.name} not found")
    log(f"✅ Nova transcript rendered: {nova.name}")
    post_build_log(f"✅ EP{ep_str} [3/6] Nova transcript rendered")


# ── Step 4: EN audio ─────────────────────────────────────────────────────────

def generate_en_audio(ep_num, force=False):
    ep_str = f"{ep_num:03d}"
    nova = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript_nova.md"
    out_path = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"

    log(f"\n── EN audio ────────────────────────────────────────────────────────────")

    if out_path.exists() and not force:
        size_mb = out_path.stat().st_size // 1024 // 1024
        log(f"⏭  EN audio already exists ({size_mb}MB) — skipping (use --force-audio to regenerate)")
        post_build_log(f"⏭ EP{ep_str} [4/6] EN audio already exists ({size_mb}MB) — skipped")
        return out_path

    log(f"Generating EN audio from {nova.name}...")
    log(f"(This takes 10-20 minutes)")
    post_build_log(f"🔊 EP{ep_str} [4/6] Generating EN audio… (10-20 min, next update on completion)")

    sys.path.insert(0, str(PODCAST_DIR))
    import generate_audio as ga
    ga.AUDIO_DIR = PODCAST_DIR / "audio"
    asyncio.run(ga.generate_podcast_audio(str(nova), f"episode_{ep_str}"))

    if not out_path.exists():
        post_build_log(f"❌ EP{ep_str} [4/6] Audio generation finished but {out_path.name} not found")
        raise SystemExit(f"❌ Audio generation completed but {out_path.name} not found")

    size_mb = out_path.stat().st_size // 1024 // 1024
    log(f"✅ EN audio: {out_path.name} ({size_mb}MB)")
    post_build_log(f"✅ EP{ep_str} [4/6] EN audio done — {size_mb}MB")
    return out_path


# ── Step 5: EN cover ─────────────────────────────────────────────────────────

def generate_en_cover(ep_num, force=False):
    """Generate EN cover art from show notes title using the shared renderer in release_episode.py."""
    ep_str = f"{ep_num:03d}"
    out_path = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"

    log(f"\n── EN cover ────────────────────────────────────────────────────────────")

    # Always ensure bespoke center art exists before deciding whether the cover can be reused.
    art_path = SCRIPTS_DIR / "episode_art" / f"episode_{ep_str}_art.py"
    if not art_path.exists():
        log(f"Generating episode art via Claude...")
        post_build_log(f"🎨 EP{ep_str} [5/6] Generating center art via Claude…")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "generate_episode_art.py"), str(ep_num)],
            cwd=str(PODCAST_DIR),
        )
        if result.returncode != 0 or not art_path.exists():
            post_build_log(f"❌ EP{ep_str} [5/6] generate_episode_art.py failed — cover will use fallback")
            log(f"⚠️  Art generation failed — cover will use fallback strata design")
        else:
            log(f"✅ Episode art generated: {art_path.name}")
    else:
        log(f"✅ Episode art ready: {art_path.name}")

    if out_path.exists() and not force:
        log(f"⏭  EN cover already exists — skipping render")
        post_build_log(f"⏭ EP{ep_str} [5/6] EN cover already exists — skipped")
        return out_path

    post_build_log(f"🖼 EP{ep_str} [5/6] Rendering cover…")
    sys.path.insert(0, str(SCRIPTS_DIR))
    import release_episode as rel
    rel.generate_en_cover(ep_num)

    if not out_path.exists():
        post_build_log(f"❌ EP{ep_str} [5/6] Cover generation finished but {out_path.name} not found")
        raise SystemExit(f"❌ Cover generation completed but {out_path.name} not found")

    log(f"✅ EN cover: {out_path.name}")
    post_build_log(f"✅ EP{ep_str} [5/6] EN cover done")
    return out_path


# ── Step 6: CDN sync ─────────────────────────────────────────────────────────

def render_cdn_index():
    episodes = []
    for audio_path in (CDN_DIR / "audio").glob("episode_*.mp3"):
        match = re.fullmatch(r"episode_(\d{3})\.mp3", audio_path.name)
        if match:
            episodes.append(int(match.group(1)))

    episodes = sorted(set(episodes), reverse=True)
    lines = [
        "<!doctype html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"utf-8\">",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "  <title>OpenClaw Podcast Audio</title>",
        "</head>",
        "<body>",
        "  <h1>OpenClaw Podcast Audio</h1>",
    ]

    if episodes:
        latest = episodes[0]
        lines += [
            f"  <p>Latest: <a href=\"audio/episode_{latest:03d}.mp3\">EP{latest:03d} audio</a> | "
            f"<a href=\"episode_{latest:03d}_cover.png\">cover</a></p>",
            "  <ul>",
        ]
        for ep in episodes[:12]:
            lines.append(
                f"    <li>EP{ep:03d}: <a href=\"audio/episode_{ep:03d}.mp3\">audio</a> | "
                f"<a href=\"episode_{ep:03d}_cover.png\">cover</a></li>"
            )
        lines.append("  </ul>")
    else:
        lines.append("  <p>No episodes published yet.</p>")

    lines += [
        "  <p><a href=\"audio/\">Browse audio/</a></p>",
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(lines)


def refresh_github_pages_root():
    index_html = CDN_DIR / "index.html"
    nojekyll = CDN_DIR / ".nojekyll"

    index_html.write_text(render_cdn_index(), encoding="utf-8")

    if not nojekyll.exists() or nojekyll.read_text() != "site enabled\n":
        nojekyll.write_text("site enabled\n", encoding="utf-8")


def cdn_payload_bytes():
    total = 0
    for path in CDN_DIR.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            total += path.stat().st_size
    return total


def enforce_pages_size_limit():
    total = cdn_payload_bytes()
    if total > GITHUB_PAGES_SITE_LIMIT_BYTES:
        raise SystemExit(
            "❌ GitHub Pages CDN is too large to publish reliably "
            f"({total / 1024 / 1024 / 1024:.2f} GiB > 1.00 GiB). "
            "Use a different host before claiming live GitHub Pages URLs."
        )


def sync_to_cdn(ep_num):
    ep_str = f"{ep_num:03d}"
    audio_src = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    cover_src = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    audio_dst = CDN_DIR / "audio" / f"episode_{ep_str}.mp3"
    cover_dst = CDN_DIR / f"episode_{ep_str}_cover.png"

    log(f"\n── CDN sync ────────────────────────────────────────────────────────────")

    shutil.copy2(str(audio_src), str(audio_dst))
    log(f"✅ Audio → CDN: {audio_dst.name}")

    shutil.copy2(str(cover_src), str(cover_dst))
    log(f"✅ Cover → CDN: {cover_dst.name}")

    refresh_github_pages_root()
    log("✅ GitHub Pages root refreshed")
    enforce_pages_size_limit()

    # Commit + push CDN repo
    import subprocess as sp
    sp.run(
        ["git", "add", f"audio/episode_{ep_str}.mp3", f"episode_{ep_str}_cover.png", "index.html", ".nojekyll"],
        cwd=str(CDN_DIR),
        check=True,
    )
    result = sp.run(["git", "diff", "--cached", "--quiet"], cwd=str(CDN_DIR))
    if result.returncode != 0:
        sp.run(["git", "commit", "-m", f"EP{ep_num}: pre-greenlight audio + cover"],
               cwd=str(CDN_DIR), check=True)
        sp.run(["git", "push"], cwd=str(CDN_DIR), check=True)
        log(f"✅ CDN repo pushed")
    else:
        log(f"ℹ️  CDN repo already up to date")

    return sp.check_output(["git", "rev-parse", "HEAD"], cwd=str(CDN_DIR), text=True).strip()


# ── Step 7: Discord ──────────────────────────────────────────────────────────

def get_audio_duration(audio_path):
    import subprocess as sp
    try:
        out = sp.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(audio_path)
        ], text=True).strip()
        secs = int(round(float(out)))
        m, s = divmod(secs, 60)
        return f"{m}:{s:02d}"
    except Exception:
        return "?:??"


def verify_url(url, timeout=20, stream_check=False):
    headers = {}
    method = "HEAD"
    if stream_check:
        # Exercise the real audio delivery path instead of only checking metadata.
        method = "GET"
        headers["Range"] = "bytes=0-0"
    req = urllib.request.Request(url, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, dict(r.headers)


def get_pages_build(commit_sha):
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{CDN_REPO}/pages/builds?per_page=10"],
            capture_output=True,
            text=True,
            check=True,
        )
        builds = json.loads(result.stdout)
    except Exception:
        return None

    for build in builds:
        if build.get("commit") == commit_sha:
            return build
    return None


def wait_for_pages_build(ep_num, commit_sha):
    ep_str = f"{ep_num:03d}"
    deadline = time.time() + PAGES_BUILD_TIMEOUT_SECONDS
    last_status = None

    log(f"Waiting for GitHub Pages build for commit {commit_sha[:7]}...")
    while time.time() < deadline:
        build = get_pages_build(commit_sha)
        if build:
            status = build.get("status") or "unknown"
            if status != last_status:
                log(f"ℹ️  GitHub Pages build status: {status}")
                last_status = status

            if status == "built":
                return
            if status == "errored":
                raise SystemExit(
                    f"❌ GitHub Pages build failed for EP{ep_str} ({commit_sha[:7]})"
                )

        time.sleep(PAGES_BUILD_POLL_SECONDS)

    raise SystemExit(
        f"❌ GitHub Pages build did not finish within {PAGES_BUILD_TIMEOUT_SECONDS // 60} minutes for EP{ep_str}"
    )


def verify_published_urls(ep_num, audio_url, cover_url, commit_sha=None):
    ep_str = f"{ep_num:03d}"
    urls = [
        ("audio", audio_url, True),
        ("cover", cover_url, False),
    ]

    log(f"\n── URL verification ─────────────────────────────────────────────────────")
    if commit_sha:
        post_build_log(f"⏳ EP{ep_str} URL verification pending — waiting for GitHub Pages build {commit_sha[:7]}")
        wait_for_pages_build(ep_num, commit_sha)
    else:
        log("⚠️  No CDN commit SHA available; falling back to direct URL verification")

    for attempt in range(1, URL_VERIFY_MAX_ATTEMPTS + 1):
        failures = []
        for label, url, stream_check in urls:
            try:
                status, headers = verify_url(url, stream_check=stream_check)
                log(f"✅ {label}: {status} {url}")
            except Exception as e:
                failures.append((label, url, str(e)))
                log(f"⚠️  {label} failed verification on attempt {attempt}: {e}")

        if not failures:
            post_build_log(f"✅ EP{ep_str} URLs verified live on GitHub Pages")
            return True

        if attempt < URL_VERIFY_MAX_ATTEMPTS:
            post_build_log(
                f"⏳ EP{ep_str} URLs still unverified (attempt {attempt}/{URL_VERIFY_MAX_ATTEMPTS}) "
                f"— retrying in {URL_VERIFY_RETRY_WAIT_SECONDS}s"
            )
            time.sleep(URL_VERIFY_RETRY_WAIT_SECONDS)
        else:
            details = "\n".join(f"  • {label}: {url} — {err}" for label, url, err in failures)
            post_build_log(f"❌ EP{ep_str} URL verification failed after {URL_VERIFY_MAX_ATTEMPTS} attempts\n{details}")
            raise SystemExit(f"❌ URL verification failed after {URL_VERIFY_MAX_ATTEMPTS} attempts\n{details}")


def post_discord_listen(ep_num, duration, audio_url, cover_url=None, verified=False):
    ep_str = f"{ep_num:03d}"
    ep_channel_name = f"openclaw-ep{ep_str}"
    token = load_env_key("DISCORD_BOT_TOKEN")

    log(f"\n── Discord post ─────────────────────────────────────────────────────────")

    def discord_request(method, path, body=None):
        url = f"https://discord.com/api/v10{path}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
        })
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())

    try:
        channels = discord_request("GET", f"/guilds/{DISCORD_GUILD_ID}/channels")
    except Exception as e:
        log(f"⚠️  Discord API error — post manually: {e}")
        log(f"   {audio_url}")
        if cover_url:
            log(f"   {cover_url}")
        return

    ep_channel = next((c for c in channels if c.get("name") == ep_channel_name), None)
    if not ep_channel:
        log(f"⚠️  Discord channel #{ep_channel_name} not found — post manually:")
        log(f"   {audio_url}")
        if cover_url:
            log(f"   {cover_url}")
        return

    status = "✅ verified" if verified else "⏳ not yet verified"
    msg = ""
    if cover_url:
        msg += f"Review cover ({status}): {cover_url}\n"
    msg += (
        f"EP{ep_str} review audio ready ({status}) — listen before approving:\n"
        f"{audio_url}\n"
        f"Duration: {duration}\n"
    )
    msg += (
        "\nWebsite/feed publish does not happen until approval.\n"
        f"\nReply ✅ to start the approved release flow (EN publish + translations + video builds), "
        f"or ❌ to rebuild.\n\n"
        f"When approved, run:\n"
        f"```\npython3 scripts/release_episode_approved.py {ep_num} --pub-date \"...\"\n```"
    )
    discord_request("POST", f"/channels/{ep_channel['id']}/messages", {"content": msg})
    log(f"✅ Posted to #{ep_channel_name}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build episode and post for review")
    parser.add_argument("episode", type=int, help="Episode number (e.g. 29)")
    parser.add_argument("--force-audio", action="store_true",
                        help="Regenerate audio even if episode_XXX.mp3 already exists")
    parser.add_argument("--skip-discord", action="store_true",
                        help="Skip Discord post (print URL instead)")
    parser.add_argument("--skip-verify", action="store_true",
                        help="Skip public GitHub Pages verification and treat URLs as unverified")
    parser.add_argument("--force-cover", action="store_true",
                        help="Regenerate cover even if episode_XXX_cover.png already exists")
    args = parser.parse_args()

    ep_num = args.episode
    ep_str = f"{ep_num:03d}"

    log(f"\n{'='*60}")
    log(f"OpenClaw Daily — EP{ep_str} Build")
    log(f"{'='*60}\n")

    try:
        story_count = verify_story_slate(ep_num)
        run_qc(ep_num)
        post_build_log(
            f"🏗 EP{ep_str} build started\n"
            f"✅ Slate verified ({story_count} stories) | ✅ QC passed"
        )
        render_nova(ep_num)
        audio_path = generate_en_audio(ep_num, force=args.force_audio)
        generate_en_cover(ep_num, force=args.force_cover)
        cdn_commit = sync_to_cdn(ep_num)
    except SystemExit as e:
        # Only post to build-log if we haven't already (step functions post their own failures)
        if str(e.code) and not str(e.code).startswith("❌"):
            post_build_log(f"❌ EP{ep_str} build failed — {e.code}\nLog: check the terminal running build_episode.py")
        raise

    duration = get_audio_duration(audio_path)
    audio_url = f"{CDN_BASE}/audio/episode_{ep_str}.mp3"
    cover_url = f"{CDN_BASE}/episode_{ep_str}_cover.png"
    log(f"\n{'='*60}")
    log(f"✅ EP{ep_str} build complete")
    log(f"   Cover: {cover_url}")
    log(f"   Audio: {audio_url}")
    log(f"   Review only: website/feed publish waits for approval")
    log(f"   Duration: {duration}")
    log(f"{'='*60}")

    if args.skip_verify:
        post_build_log(
            f"⚠️ EP{ep_str} CDN pushed — URLs UNVERIFIED because --skip-verify was set | "
            f"{duration} | #openclaw-ep{ep_str} | {cover_url} | {audio_url}"
        )
        if args.skip_discord:
            log(f"\n(--skip-discord --skip-verify) UNVERIFIED URLs for #{f'openclaw-ep{ep_str}'}:")
            log(f"  Cover: {cover_url}")
            log(f"  Audio: {audio_url}")
        else:
            post_discord_listen(ep_num, duration, audio_url, cover_url=cover_url, verified=False)
    else:
        post_build_log(
            f"⏳ EP{ep_str} CDN pushed — URLs UNVERIFIED, waiting for GitHub Pages | "
            f"{duration} | #openclaw-ep{ep_str} | {cover_url} | {audio_url}"
        )
        verify_published_urls(ep_num, audio_url, cover_url, commit_sha=cdn_commit)
        if args.skip_discord:
            log(f"\n(--skip-discord) VERIFIED URLs for #{f'openclaw-ep{ep_str}'}:")
            log(f"  Cover: {cover_url}")
            log(f"  Audio: {audio_url}")
        else:
            post_discord_listen(ep_num, duration, audio_url, cover_url=cover_url, verified=True)
            post_build_log(f"✅ EP{ep_str} done — review URLs verified live | {duration} | #openclaw-ep{ep_str} | {cover_url} | {audio_url}")

    log(f"\n⛔ STOP — wait for Toby's ✅ in Discord before running:")
    log(f"   python3 scripts/release_episode_approved.py {ep_num} --pub-date \"...\"")


if __name__ == "__main__":
    main()
