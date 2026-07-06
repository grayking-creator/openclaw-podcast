#!/usr/bin/env python3
"""
build_episode.py — Pre-greenlight episode builder.

Runs everything needed before ARIA posts review assets to Discord:
  1. QC the approved show notes (check_show_notes.py).
  2. Verify transcript matches the approved story slate from show notes.
  3. Run QC (check_episode.py) — blocks on any ERROR.
  4. Render nova transcript (render_nova.py).
  5. Generate EN audio.
  6. Generate EN cover art (from show notes title).
  7. Copy audio + cover to CDN repo.
  8. Post review URLs to Discord episode channel, then stop for approval.

Does NOT proceed to site/feed publish, translations, or YouTube — that's release_episode_approved.py after approval.

Usage:
    python3 scripts/build_episode.py 29
    python3 scripts/build_episode.py 29 --force-audio   # regenerate even if audio exists
    python3 scripts/build_episode.py 29 --skip-discord  # skip Discord post (dry-run)
    python3 scripts/build_episode.py 29 --force-art     # regenerate bespoke center art module
"""

import argparse
import asyncio
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import release_approval_gate as approval_gate
import release_episode as rel

SCRIPTS_DIR = Path(__file__).parent
PODCAST_DIR = SCRIPTS_DIR.parent
AUDIO_CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-audio"
AUDIO_CDN_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio"
AUDIO_CDN_REPO = "clawdassistant85-netizen/openclaw-podcast-audio"
MEDIA_EN_CDN_DIR = Path.home() / ".openclaw/workspace/openclaw-podcast-media-en"
MEDIA_EN_CDN_BASE = "https://clawdassistant85-netizen.github.io/openclaw-podcast-media-en"
MEDIA_EN_CDN_REPO = "clawdassistant85-netizen/openclaw-podcast-media-en"
MEDIA_EN_START_EPISODE = 57
DISCORD_GUILD_ID = "1475905694145318944"
BUILD_LOG_CHANNEL = "1485243812442804327"
GITHUB_PAGES_SITE_LIMIT_BYTES = 1024 * 1024 * 1024
PAGES_BUILD_POLL_SECONDS = 30
PAGES_BUILD_TIMEOUT_SECONDS = 1800
URL_VERIFY_RETRY_WAIT_SECONDS = 30
URL_VERIFY_MAX_ATTEMPTS = 10


def en_media_target(ep_num):
    """Return the EN media repo that should host this episode's review assets."""
    if ep_num >= MEDIA_EN_START_EPISODE:
        return {
            "dir": MEDIA_EN_CDN_DIR,
            "base": MEDIA_EN_CDN_BASE,
            "repo": MEDIA_EN_CDN_REPO,
            "label": "media-en",
        }
    return {
        "dir": AUDIO_CDN_DIR,
        "base": AUDIO_CDN_BASE,
        "repo": AUDIO_CDN_REPO,
        "label": "audio",
    }


def en_audio_url(ep_num):
    return rel.en_audio_url(ep_num)


def en_cover_url(ep_num):
    return rel.en_cover_url(ep_num)


def en_show_notes_url(ep_num):
    ep_str = f"{ep_num:03d}"
    if rel.is_en_release_asset_episode(ep_num):
        return rel.en_release_asset_url(ep_num, rel.en_release_show_notes_name(ep_num))
    return f"{en_media_target(ep_num)['base']}/show_notes_episode_{ep_str}.md"


def en_transcript_url(ep_num):
    ep_str = f"{ep_num:03d}"
    if rel.is_en_release_asset_episode(ep_num):
        return rel.en_release_asset_url(ep_num, rel.en_release_transcript_name(ep_num))
    return f"{en_media_target(ep_num)['base']}/episode_{ep_str}_transcript.md"


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


def save_review_gate(ep_num, audio_path, duration, audio_url, cover_url):
    state = rel.load_state(ep_num)
    approval_gate.record_review_audio(
        state,
        audio_path=Path(audio_path),
        duration=duration,
        audio_url=audio_url,
        cover_url=cover_url,
    )
    rel.save_state(ep_num, state)


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


def cover_stale_against_art(cover_path: Path, art_path: Path) -> bool:
    """A rendered cover must be refreshed if newer bespoke art exists."""
    if not cover_path.exists() or not art_path.exists():
        return False
    return cover_path.stat().st_mtime < art_path.stat().st_mtime


def assert_feed_sequence(ep_num: int) -> None:
    """Fail closed if we are about to skip over an unpublished episode number."""
    feed_path = PODCAST_DIR / "feed.xml"
    if ep_num <= 0 or not feed_path.exists():
        return
    feed_text = feed_path.read_text()
    existing = {int(m) for m in re.findall(r"<itunes:episode>(\d+)</itunes:episode>", feed_text)}
    if not existing or ep_num in existing:
        return
    expected = 0
    while expected in existing:
        expected += 1
    if ep_num != expected:
        expected_str = f"{expected:03d}"
        prior_draft = PODCAST_DIR / f"show_notes_episode_{expected_str}.md"
        draft_hint = (
            f"\n\nUnreleased prior draft exists: {prior_draft.name}"
            if prior_draft.exists()
            else ""
        )
        raise SystemExit(
            f"❌ Refusing to build EP{ep_num:03d}: feed sequence expects EP{expected:03d} next. "
            f"EP{ep_num:03d} would skip over an unpublished episode."
            f"{draft_hint}\n\n"
            "Choose one recovery path before building:\n"
            f"1. Keep the prior stories: merge EP{expected_str}'s Story Slate into the episode you meant to build, "
            "then build the next expected episode number.\n"
            f"   Helper: python3 scripts/resolve_episode_gap.py prepare-merge --prior {expected} --target {ep_num}\n"
            f"2. Replace the prior stories: archive EP{expected_str}'s draft/assets and reuse EP{expected_str} "
            "for the new story slate, regenerating transcript, audio, cover, translations, and YouTube assets from that replacement.\n"
            f"   Helper: python3 scripts/resolve_episode_gap.py archive {expected} --reason 'replaced before transcript generation'"
        )


def ensure_bespoke_art_module(ep_num: int, force: bool = False) -> Path:
    ep_str = f"{ep_num:03d}"
    art_path = SCRIPTS_DIR / "episode_art" / f"episode_{ep_str}_art.py"

    log(f"\n── Bespoke Art ─────────────────────────────────────────────────────────")
    if art_path.exists() and not force:
        log(f"✅ Bespoke art ready: {art_path.name}")
        post_build_log(f"✅ EP{ep_str} [5/6] Bespoke art ready — {art_path.name}")
        return art_path

    if force and art_path.exists():
        log(f"♻️  Regenerating bespoke art: {art_path.name}")
        post_build_log(f"♻️ EP{ep_str} [5/6] Regenerating bespoke art module…")
    else:
        log("Generating bespoke episode art...")
        post_build_log(f"🎨 EP{ep_str} [5/6] Generating bespoke center art…")

    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "generate_episode_art.py"), str(ep_num)],
        cwd=str(PODCAST_DIR),
    )
    if result.returncode != 0 or not art_path.exists():
        msg = (
            f"❌ EP{ep_str} [5/6] Bespoke art module generation failed — build stopped; "
            "fallback cover art is disabled"
        )
        log(msg)
        post_build_log(msg)
        raise SystemExit(msg)

    log(f"✅ Bespoke art generated: {art_path.name}")
    post_build_log(f"✅ EP{ep_str} [5/6] Bespoke art ready — {art_path.name}")
    return art_path


# ── Step 0: Show-notes QC ────────────────────────────────────────────────────

def run_show_notes_qc(ep_num):
    ep_str = f"{ep_num:03d}"
    show_notes = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    qc_script = SCRIPTS_DIR / "check_show_notes.py"

    if not show_notes.exists():
        raise SystemExit(f"❌ Show notes missing: {show_notes.name}\n   Write show notes before building.")
    if not qc_script.exists():
        raise SystemExit(f"❌ Missing show-notes QC script: {qc_script.name}")

    log("\n── Show notes QC ───────────────────────────────────────────────────────")
    post_build_log(f"🧭 EP{ep_str} [0/7] Validating approved show notes…")
    run([sys.executable, str(qc_script), str(show_notes)])
    assert_feed_sequence(ep_num)
    post_build_log(f"✅ EP{ep_str} [0/7] Show notes QC passed")


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
        msg = (
            f"❌ EP{ep_str} build failed — transcript missing: `{transcript.name}`\n"
            f"Write the transcript from the approved story slate in `show_notes_episode_{ep_str}.md` first."
        )
        post_build_log(msg)
        raise SystemExit(msg)

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
    def slate_match_words(title):
        """Return title words worth matching against spoken transcript text.

        Show notes use exact release tags in story titles, but spoken transcripts
        must shorten or omit those tags for audio QC. Match on the meaningful
        title words instead of forcing full version strings into the script.
        """
        core = re.sub(r"[—–].*", "", title).strip().lower()
        raw_words = re.findall(r"[a-z0-9.]+", core)
        return [
            word
            for word in raw_words
            if not re.fullmatch(r"v?\d+(?:\.\d+){1,}", word)
        ]

    for title in story_titles:
        words = slate_match_words(title)
        if len(words) >= 3:
            # Check that the first significant title words appear in the transcript.
            # This catches stale/wrong transcripts without requiring the audio to
            # read show-note titles verbatim.
            if not all(word in transcript_text for word in words[:3]):
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
    started_at = time.time()
    prior_hash = hashlib.sha256(out_path.read_bytes()).hexdigest() if out_path.exists() else None

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
    if force and out_path.stat().st_mtime < started_at:
        post_build_log(f"❌ EP{ep_str} [4/6] Audio generation did not refresh {out_path.name}")
        raise SystemExit(f"❌ Audio generation did not refresh {out_path.name}")
    if force and prior_hash and hashlib.sha256(out_path.read_bytes()).hexdigest() == prior_hash:
        log(f"ℹ️  Audio generation reproduced identical bytes for {out_path.name}; continuing")
        post_build_log(
            f"ℹ️ EP{ep_str} [4/6] EN audio regenerated deterministically "
            f"with the same hash — continuing"
        )

    size_mb = out_path.stat().st_size // 1024 // 1024
    audio_url = en_audio_url(ep_num)
    log(f"✅ EN audio: {out_path.name} ({size_mb}MB)")
    post_build_log(f"✅ EP{ep_str} [4/6] EN audio done — {size_mb}MB\n{audio_url}")
    return out_path


# ── Step 5: EN cover ─────────────────────────────────────────────────────────

def generate_en_cover(ep_num, force=False):
    """Generate EN cover art from show notes title using the shared renderer in release_episode.py."""
    ep_str = f"{ep_num:03d}"
    out_path = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"

    log(f"\n── EN cover ────────────────────────────────────────────────────────────")

    # Bespoke art is now a required build prerequisite, not a best-effort fallback.
    art_path = ensure_bespoke_art_module(ep_num)

    stale_against_art = cover_stale_against_art(out_path, art_path)
    if out_path.exists() and not force and not stale_against_art:
        log(f"⏭  EN cover already exists — skipping render")
        post_build_log(f"⏭ EP{ep_str} [6/6] EN cover already exists — skipped")
        return out_path
    if stale_against_art and not force:
        log(f"♻️  EN cover is older than {art_path.name} — re-rendering")
        post_build_log(f"♻️ EP{ep_str} [6/6] EN cover is stale vs bespoke art — re-rendering")

    post_build_log(f"🖼 EP{ep_str} [6/6] Rendering cover…")
    sys.path.insert(0, str(SCRIPTS_DIR))
    import release_episode as rel
    rel.generate_en_cover(ep_num)

    if not out_path.exists():
        post_build_log(f"❌ EP{ep_str} [6/6] Cover generation finished but {out_path.name} not found")
        raise SystemExit(f"❌ Cover generation completed but {out_path.name} not found")

    log(f"✅ EN cover: {out_path.name}")
    post_build_log(f"✅ EP{ep_str} [6/6] EN cover done")
    return out_path


# ── Step 6: CDN sync ─────────────────────────────────────────────────────────

def render_cdn_index(cdn_dir):
    episodes = []
    for audio_path in (cdn_dir / "audio").glob("episode_*.mp3"):
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
        "  <title>AgentStack Daily Audio</title>",
        "</head>",
        "<body>",
        "  <h1>AgentStack Daily Audio</h1>",
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


def refresh_github_pages_root(cdn_dir):
    index_html = cdn_dir / "index.html"
    nojekyll = cdn_dir / ".nojekyll"

    index_html.write_text(render_cdn_index(cdn_dir), encoding="utf-8")

    if not nojekyll.exists() or nojekyll.read_text() != "site enabled\n":
        nojekyll.write_text("site enabled\n", encoding="utf-8")


def cdn_payload_bytes(cdn_dir):
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=str(cdn_dir),
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        total = 0
        for raw_rel in result.stdout.split(b"\0"):
            if not raw_rel:
                continue
            path = cdn_dir / raw_rel.decode()
            if path.is_file():
                total += path.stat().st_size
        return total

    total = 0
    for path in cdn_dir.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            total += path.stat().st_size
    return total


def enforce_pages_size_limit(cdn_dir):
    total = cdn_payload_bytes(cdn_dir)
    if total > GITHUB_PAGES_SITE_LIMIT_BYTES:
        raise SystemExit(
            "❌ GitHub Pages CDN is too large to publish reliably "
            f"({total / 1024 / 1024 / 1024:.2f} GiB > 1.00 GiB). "
            "Use a different host before claiming live GitHub Pages URLs."
        )


def sync_to_cdn(ep_num):
    ep_str = f"{ep_num:03d}"
    if rel.is_en_release_asset_episode(ep_num):
        log(f"\n── CDN sync ────────────────────────────────────────────────────────────")
        log(f"Target: EN release assets ({rel.en_release_repo()} / {rel.en_release_tag(ep_num)})")
        rel.upload_en_release_assets(ep_num, include_review_docs=True)
        log("✅ EN release assets uploaded")
        return None

    target = en_media_target(ep_num)
    cdn_dir = target["dir"]
    audio_src = PODCAST_DIR / "audio" / f"episode_{ep_str}.mp3"
    cover_src = PODCAST_DIR / "images" / f"episode_{ep_str}_cover.png"
    show_notes_src = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    transcript_src = PODCAST_DIR / "episodes" / f"episode_{ep_str}_transcript.md"
    audio_dst = cdn_dir / "audio" / f"episode_{ep_str}.mp3"
    cover_dst = cdn_dir / f"episode_{ep_str}_cover.png"
    show_notes_dst = cdn_dir / f"show_notes_episode_{ep_str}.md"
    transcript_dst = cdn_dir / f"episode_{ep_str}_transcript.md"

    log(f"\n── CDN sync ────────────────────────────────────────────────────────────")
    log(f"Target: {target['label']} ({target['repo']})")

    audio_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(audio_src), str(audio_dst))
    log(f"✅ Audio → CDN: {audio_dst.name}")

    shutil.copy2(str(cover_src), str(cover_dst))
    log(f"✅ Cover → CDN: {cover_dst.name}")

    shutil.copy2(str(show_notes_src), str(show_notes_dst))
    log(f"✅ Show notes → CDN: {show_notes_dst.name}")

    shutil.copy2(str(transcript_src), str(transcript_dst))
    log(f"✅ Transcript → CDN: {transcript_dst.name}")

    refresh_github_pages_root(cdn_dir)
    log("✅ GitHub Pages root refreshed")
    enforce_pages_size_limit(cdn_dir)

    # Commit + push CDN repo
    import subprocess as sp
    sp.run(
        [
            "git", "add",
            f"audio/episode_{ep_str}.mp3",
            f"episode_{ep_str}_cover.png",
            f"show_notes_episode_{ep_str}.md",
            f"episode_{ep_str}_transcript.md",
            "index.html",
            ".nojekyll",
        ],
        cwd=str(cdn_dir),
        check=True,
    )
    result = sp.run(["git", "diff", "--cached", "--quiet"], cwd=str(cdn_dir))
    if result.returncode != 0:
        sp.run(["git", "commit", "-m", f"EP{ep_num}: pre-greenlight audio + cover"],
               cwd=str(cdn_dir), check=True)
        sp.run(["git", "push"], cwd=str(cdn_dir), check=True)
        log(f"✅ CDN repo pushed")
    else:
        log(f"ℹ️  CDN repo already up to date")

    return sp.check_output(["git", "rev-parse", "HEAD"], cwd=str(cdn_dir), text=True).strip()


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


def get_pages_build(commit_sha, cdn_repo):
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{cdn_repo}/pages/builds?per_page=10"],
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


def get_pages_build_type(cdn_repo):
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{cdn_repo}/pages", "--jq", ".build_type"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def wait_for_pages_build(ep_num, commit_sha, cdn_repo):
    ep_str = f"{ep_num:03d}"
    deadline = time.time() + PAGES_BUILD_TIMEOUT_SECONDS
    last_status = None

    if get_pages_build_type(cdn_repo) == "workflow":
        log("ℹ️  GitHub Pages uses Actions deployment — falling through to direct URL polling")
        return

    log(f"Waiting for GitHub Pages build for commit {commit_sha[:7]}...")
    while time.time() < deadline:
        build = get_pages_build(commit_sha, cdn_repo)
        if build:
            status = build.get("status") or "unknown"
            if status != last_status:
                log(f"ℹ️  GitHub Pages build status: {status}")
                last_status = status

            if status == "built":
                return
            if status == "errored":
                # Pages API sometimes reports errored when content is already live
                # (e.g. no-op pushes or transient build runner issues). Fall through
                # to direct URL probing rather than hard-stopping here.
                log(f"⚠️  Pages build reported errored for {commit_sha[:7]} — falling back to direct URL check")
                return

        time.sleep(PAGES_BUILD_POLL_SECONDS)

    raise SystemExit(
        f"❌ GitHub Pages build did not finish within {PAGES_BUILD_TIMEOUT_SECONDS // 60} minutes for EP{ep_str}"
    )


def verify_published_urls(ep_num, audio_url, cover_url, show_notes_url=None, transcript_url=None, commit_sha=None, cdn_repo=None):
    ep_str = f"{ep_num:03d}"
    urls = [
        ("audio", audio_url, True),
        ("cover", cover_url, False),
    ]
    if show_notes_url:
        urls.append(("show notes", show_notes_url, False))
    if transcript_url:
        urls.append(("transcript", transcript_url, False))

    log(f"\n── URL verification ─────────────────────────────────────────────────────")
    if commit_sha:
        post_build_log(f"⏳ EP{ep_str} URL verification pending — waiting for GitHub Pages build {commit_sha[:7]}")
        wait_for_pages_build(ep_num, commit_sha, cdn_repo or en_media_target(ep_num)["repo"])
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


# ── Review post dispatch (TELEGRAM ONLY — locked 2026-06-27) ─────────────
# Locked invariant (2026-06-27, post-EP075 routing incident): the
# operator's review surface is Telegram chat id 8319992332 (this DM).
# Discord post paths were removed entirely after a build silently
# routed to the ARIA Discord account instead of the operator's
# Telegram DM. The Telegram post is now mandatory: if the post
# fails, the build aborts loudly. There is no --use-discord fallback.
#
# The target is hardcoded here and in notify_telegram_review.py to
# 8319992332. The HERMES_SESSION_KEY env var (if set) is asserted to
# match; if it doesn't, we abort with a routing-misconfigured error
# before generating any audio. This prevents the same class of
# routing bug from ever silently redirecting a build to a different
# chat.

OPERATOR_TELEGRAM_CHAT_ID = "8319992332"
OPERATOR_TELEGRAM_CHAT_IDS = frozenset({"8319992332"})  # the only valid targets


def assert_telegram_routing() -> None:
    """Pre-flight check: refuse to build if the active session is not the
    operator's home Telegram DM. Catches the case where HERMES_SESSION_KEY
    is set to a different bot's session, or the env was inherited from a
    parent shell that was running for a different account.
    """
    session_key = os.environ.get("HERMES_SESSION_KEY", "")
    if not session_key:
        # No session key set (e.g. running standalone in a venv). Allow
        # but log a warning so the operator can see the routing is
        # ambient.
        log("build_episode: WARN HERMES_SESSION_KEY not set; routing assertion skipped")
        return
    if not session_key.endswith(f":{OPERATOR_TELEGRAM_CHAT_ID}"):
        raise SystemExit(
            f"❌ ROUTING MIS-WIRED: HERMES_SESSION_KEY ends with "
            f"'{session_key.rsplit(':', 1)[-1]}' but the only valid "
            f"AgentStack Daily review target is "
            f"'{OPERATOR_TELEGRAM_CHAT_ID}'. Refusing to build — the "
            f"audio would be posted to the wrong chat. Fix the session "
            f"or the env, do not bypass this check."
        )


def _post_review_listen(ep_num, args, duration, audio_url, cover_url=None,
                        show_notes_url=None, transcript_url=None,
                        verified=False, audio_sha=""):
    """Post the review-listening message to the operator's Telegram DM.

    Telegram chat id 8319992332 is the ONLY valid review target. The
    notifier (notify_telegram_review.py --intent ready) hardcodes the
    same target. If the post fails, the build aborts. There is no
    Discord fallback path; the legacy post_discord_listen() and the
    --use-discord flag were removed after the 2026-06-27 routing
    incident.

    Never post a status update, a plan, or a "run this script
    yourself" message. The Telegram post is the entire review surface;
    it includes the audio hash and a clear approval/reject prompt.
    """
    assert_telegram_routing()
    if args.skip_telegram:
        log("build_episode: --skip-telegram set; review URLs only logged here (NOT recommended for cron-launched runs)")
        return

    summary = _build_review_summary(ep_num)
    cmd = [
        sys.executable, str(Path(__file__).parent / "notify_telegram_review.py"),
        "--ep", str(ep_num),
        "--intent", "ready",
        "--audio-url", audio_url,
        "--audio-file", str(PODCAST_DIR / "audio" / f"episode_{ep_num:03d}.mp3"),
        "--cover-url", cover_url or "",
        "--show-notes-url", show_notes_url or "",
        "--transcript-url", transcript_url or "",
        "--duration", duration,
        "--sha256", audio_sha or "",
        "--summary", summary,
    ]
    if verified:
        cmd.append("--verified")
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        # ABORT, do not silently swallow. The audio has already been
        # generated and is on disk, but the operator has not been
        # notified. The build fails so the morning pipeline exits
        # non-zero and the next morning's cron can re-run after the
        # routing is fixed.
        log(f"❌ Telegram ready-post FAILED (exit {proc.returncode})")
        log(f"   stdout: {proc.stdout}")
        log(f"   stderr: {proc.stderr}")
        raise SystemExit(
            f"❌ EP{ep_num:03d} review Telegram post failed. The audio is "
            f"on disk and on the CDN, but the operator was not notified. "
            f"Check the Telegram bot token, HERMES_SESSION_KEY, and the "
            f"target chat id (must be {OPERATOR_TELEGRAM_CHAT_ID})."
        )
    log(f"✅ EP{ep_num:03d} review Telegram post sent to {OPERATOR_TELEGRAM_CHAT_ID}")


def _build_review_summary(ep_num: int) -> str:
    """Pull ALL slate headlines out of show_notes_episode_NNN.md for the
    Telegram review post. The full slate must be visible: EP080 (2026-07-05)
    truncated 14 stories to 7 bullets and Toby judged the episode 'only 7
    stories' from the review post alone. If the show-notes file is missing,
    fall back to a no-summary post (the Telegram prompt is still actionable;
    the listener can open the show notes URL for context)."""
    ep_str = f"{ep_num:03d}"
    path = PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    if not path.exists():
        return ""
    text = path.read_text(errors="replace")
    # Headlines are `N. **Title**` lines under "## Story Slate" or at the
    # top of the file. Pull every bold-anchored numbered entry.
    bullets: list[str] = []
    for line in text.splitlines():
        m = re.match(r"\s*\d+\.\s+\*\*(.+?)\*\*", line)
        if m:
            bullets.append(m.group(1).strip())
    return "; ".join(bullets)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build episode and post for review")
    parser.add_argument("episode", type=int, help="Episode number (e.g. 29)")
    parser.add_argument("--force-audio", action="store_true",
                        help="Regenerate audio even if episode_XXX.mp3 already exists")
    parser.add_argument("--skip-telegram", action="store_true",
                        help="Skip the Telegram review post (NOT recommended for cron-launched runs)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Build audio + CDN push but do NOT post to Telegram or anywhere else")
    parser.add_argument("--skip-verify", action="store_true",
                        help="Skip public GitHub Pages verification and treat URLs as unverified")
    parser.add_argument("--force-cover", action="store_true",
                        help="Regenerate cover even if episode_XXX_cover.png already exists")
    parser.add_argument("--force-art", action="store_true",
                        help="Regenerate bespoke center art module even if episode_NNN_art.py already exists")
    args = parser.parse_args()

    ep_num = args.episode
    ep_str = f"{ep_num:03d}"

    log(f"\n{'='*60}")
    log(f"AgentStack Daily — EP{ep_str} Build")
    log(f"{'='*60}\n")

    try:
        run_show_notes_qc(ep_num)
        story_count = verify_story_slate(ep_num)
        run_qc(ep_num)
        post_build_log(
            f"🏗 EP{ep_str} build started\n"
            f"✅ Show notes QC passed | ✅ Slate verified ({story_count} stories) | ✅ Transcript QC passed"
        )
        render_nova(ep_num)
        audio_path = generate_en_audio(ep_num, force=args.force_audio)
        ensure_bespoke_art_module(ep_num, force=args.force_art)
        generate_en_cover(ep_num, force=args.force_cover)
        cdn_commit = sync_to_cdn(ep_num)
    except SystemExit as e:
        # Only post to build-log if we haven't already (step functions post their own failures)
        if str(e.code) and not str(e.code).startswith("❌"):
            post_build_log(f"❌ EP{ep_str} build failed — {e.code}\nLog: check the terminal running build_episode.py")
        raise

    duration = get_audio_duration(audio_path)
    media_target = en_media_target(ep_num)
    audio_url = en_audio_url(ep_num)
    cover_url = en_cover_url(ep_num)
    show_notes_url = en_show_notes_url(ep_num)
    transcript_url = en_transcript_url(ep_num)
    # Discord aggressively caches image embeds by URL. Use the CDN commit as a
    # cache-busting query string for Discord-facing cover links so the thumbnail
    # shown in the review message always matches the asset just pushed.
    cover_review_url = f"{cover_url}?v={cdn_commit[:7]}" if cdn_commit else cover_url
    save_review_gate(ep_num, audio_path, duration, audio_url, cover_review_url)
    # Pull the audio SHA that save_review_gate just recorded so the Telegram
    # review post shows the *file* hash (matches what the approval gate
    # verifies), not the CDN commit SHA.
    _state = rel.load_state(ep_num)
    _audio_sha = ((_state or {}).get("review_audio") or {}).get("sha256", "")
    log(f"\n{'='*60}")
    log(f"✅ EP{ep_str} build complete")
    log(f"   Cover: {cover_review_url}")
    log(f"   Audio: {audio_url}")
    log(f"   Review only: website/feed publish waits for approval")
    log(f"   Duration: {duration}")
    log(f"{'='*60}")

    if args.skip_verify:
        post_build_log(
            f"⚠️ EP{ep_str} CDN pushed — URLs UNVERIFIED because --skip-verify was set | "
            f"{duration} | #agent-stack-ep{ep_str} | {show_notes_url} | {transcript_url} | {cover_review_url} | {audio_url}"
        )
        if args.dry_run:
            log(f"\n(--dry-run --skip-verify) UNVERIFIED URLs for #{f'agent-stack-ep{ep_str}'}:")
            log(f"  Show notes: {show_notes_url}")
            log(f"  Transcript: {transcript_url}")
            log(f"  Cover: {cover_review_url}")
            log(f"  Audio: {audio_url}")
        else:
            _post_review_listen(
                ep_num, args, duration, audio_url, cover_url=cover_review_url,
                show_notes_url=show_notes_url, transcript_url=transcript_url,
                verified=False, audio_sha=_audio_sha,
            )
    else:
        post_build_log(
            f"⏳ EP{ep_str} CDN pushed — URLs UNVERIFIED, waiting for GitHub Pages | "
            f"{duration} | #agent-stack-ep{ep_str} | {show_notes_url} | {transcript_url} | {cover_review_url} | {audio_url}"
        )
        verify_published_urls(
            ep_num,
            audio_url,
            cover_url,
            show_notes_url=show_notes_url,
            transcript_url=transcript_url,
            commit_sha=cdn_commit,
            cdn_repo=media_target["repo"],
        )
        if args.dry_run:
            log(f"\n(--dry-run) VERIFIED URLs for #{f'agent-stack-ep{ep_str}'}:")
            log(f"  Show notes: {show_notes_url}")
            log(f"  Transcript: {transcript_url}")
            log(f"  Cover: {cover_review_url}")
            log(f"  Audio: {audio_url}")
        else:
            _post_review_listen(
                ep_num, args, duration, audio_url, cover_url=cover_review_url,
                show_notes_url=show_notes_url, transcript_url=transcript_url,
                verified=True, audio_sha=_audio_sha,
            )
            post_build_log(f"✅ EP{ep_str} done — review URLs verified live | {duration} | #agent-stack-ep{ep_str} | {show_notes_url} | {transcript_url} | {cover_review_url} | {audio_url}")

    log(f"\n⛔ STOP — wait for Toby's ✅ in Telegram before running:")
    log(f"   python3 scripts/launch_approved_release.py {ep_num} --audio-approved-by-telegram --pub-date \"...\"")


if __name__ == "__main__":
    main()
