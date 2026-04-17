#!/usr/bin/env python3
"""
Migrate OpenClaw podcast media from the legacy audio repo into per-language
GitHub release-asset repos.

Features:
- Initializes empty media repos with a README on `main`
- Uploads show art plus all media referenced by the current feed files
- Rewrites a single feed file to GitHub release asset URLs
- Removes only one language's legacy audio files from the old audio repo

This script is designed to be idempotent. Re-running it will clobber existing
release assets with the canonical local files.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse, unquote
from urllib.request import urlopen


WORKSPACE = Path.home() / ".openclaw" / "workspace"
PODCAST_DIR = WORKSPACE / "openclaw-podcast"
LEGACY_AUDIO_DIR = WORKSPACE / "openclaw-podcast-audio"
ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
DOWNLOAD_CACHE_DIR = Path(tempfile.mkdtemp(prefix="openclaw-media-cache-"))

LANG_REPOS = {
    "en": "clawdassistant85-netizen/openclaw-podcast-media-en",
    "es": "clawdassistant85-netizen/openclaw-podcast-media-es",
    "de": "clawdassistant85-netizen/openclaw-podcast-media-de",
    "pt": "clawdassistant85-netizen/openclaw-podcast-media-pt",
    "hi": "clawdassistant85-netizen/openclaw-podcast-media-hi",
}

FEED_PATHS = {
    "en": PODCAST_DIR / "feed.xml",
    "es": PODCAST_DIR / "translations" / "feed_es.xml",
    "de": PODCAST_DIR / "translations" / "feed_de.xml",
    "pt": PODCAST_DIR / "translations" / "feed_pt.xml",
    "hi": PODCAST_DIR / "translations" / "feed_hi.xml",
}

OLD_AUDIO_REPO_PREFIXES = (
    "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/",
    "https://raw.githubusercontent.com/clawdassistant85-netizen/openclaw-podcast-audio/main/",
    "https://github.com/clawdassistant85-netizen/openclaw-podcast-audio/raw/main/",
    "https://media.githubusercontent.com/media/clawdassistant85-netizen/openclaw-podcast-audio/main/",
)
OLD_PODCAST_REPO_PREFIXES = (
    "https://grayking-creator.github.io/openclaw-podcast/",
    "https://raw.githubusercontent.com/grayking-creator/openclaw-podcast/main/",
    "https://github.com/grayking-creator/openclaw-podcast/raw/main/",
    "https://media.githubusercontent.com/media/grayking-creator/openclaw-podcast/main/",
)


@dataclass
class EpisodeAsset:
    episode: int
    old_audio_url: str
    old_guid_url: str | None
    old_cover_url: str | None
    audio_source: Path
    cover_source: Path

    @property
    def tag(self) -> str:
        return f"ep{self.episode:03d}"

    @property
    def audio_asset_name(self) -> str:
        return f"episode_{self.episode:03d}.mp3"

    @property
    def cover_asset_name(self) -> str:
        return f"episode_{self.episode:03d}_cover.png"


@dataclass
class FeedInventory:
    lang: str
    repo: str
    feed_path: Path
    channel_image_url: str
    channel_image_source: Path
    episodes: list[EpisodeAsset]


def log(msg: str) -> None:
    print(msg, flush=True)


def run(cmd: list[str], cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    kwargs = {
        "cwd": str(cwd) if cwd else None,
        "text": True,
        "check": True,
    }
    if capture:
        kwargs["capture_output"] = True
    return subprocess.run(cmd, **kwargs)


def maybe_run(cmd: list[str], cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    kwargs = {
        "cwd": str(cwd) if cwd else None,
        "text": True,
        "check": False,
    }
    if capture:
        kwargs["capture_output"] = True
    return subprocess.run(cmd, **kwargs)


def gh_release_exists(repo: str, tag: str) -> bool:
    result = maybe_run(["gh", "release", "view", tag, "-R", repo], capture=True)
    return result.returncode == 0


def release_asset_url(repo: str, tag: str, asset_name: str) -> str:
    return f"https://github.com/{repo}/releases/download/{tag}/{asset_name}"


def op3_wrap(url: str) -> str:
    return f"https://op3.dev/e/{url}"


def unwrap_op3(url: str) -> str:
    prefix = "https://op3.dev/e/"
    if url.startswith(prefix):
        return url[len(prefix):]
    return url


def strip_known_prefix(url: str, prefixes: Iterable[str]) -> str | None:
    for prefix in prefixes:
        if url.startswith(prefix):
            return url[len(prefix):]
    return None


def resolve_local_path_from_url(url: str, lang: str | None = None) -> Path:
    direct = unwrap_op3(url)
    stripped = strip_known_prefix(direct, OLD_AUDIO_REPO_PREFIXES)
    if stripped:
        path = LEGACY_AUDIO_DIR / unquote(stripped)
        if path.exists():
            return path

    stripped = strip_known_prefix(direct, OLD_PODCAST_REPO_PREFIXES)
    if stripped:
        path = PODCAST_DIR / unquote(stripped)
        if path.exists():
            return path

    parsed = urlparse(direct)
    path = parsed.path.lstrip("/")

    if parsed.netloc in {"raw.githubusercontent.com", "media.githubusercontent.com"}:
        parts = path.split("/")
        if parsed.netloc == "media.githubusercontent.com" and parts and parts[0] == "media":
            parts = parts[1:]
        if len(parts) >= 4:
            owner, repo, branch = parts[0], parts[1], parts[2]
            rel = "/".join(parts[3:])
            if repo == "openclaw-podcast-audio":
                candidate = LEGACY_AUDIO_DIR / rel
                if candidate.exists():
                    return candidate
            if repo == "openclaw-podcast":
                candidate = PODCAST_DIR / rel
                if candidate.exists():
                    return candidate

    if parsed.netloc == "github.com":
        parts = path.split("/")
        if len(parts) >= 5 and parts[2] == "raw" and parts[3] == "main":
            repo = parts[1]
            rel = "/".join(parts[4:])
            if repo == "openclaw-podcast-audio":
                candidate = LEGACY_AUDIO_DIR / rel
                if candidate.exists():
                    return candidate
            if repo == "openclaw-podcast":
                candidate = PODCAST_DIR / rel
                if candidate.exists():
                    return candidate

    basename = Path(unquote(path)).name
    if basename == "cover.png":
        lang_key = lang or "en"
        show_art_candidate = LEGACY_AUDIO_DIR / f"show_art_{lang_key}.png"
        if show_art_candidate.exists():
            return show_art_candidate
        en_show_art_candidate = LEGACY_AUDIO_DIR / "show_art_en.png"
        if en_show_art_candidate.exists():
            return en_show_art_candidate

    alternate_basenames = [basename]
    for needle in ("_full_v2", "_full", "_approved"):
        if needle in basename:
            alternate_basenames.append(basename.replace(needle, ""))

    fallback_dirs = [
        LEGACY_AUDIO_DIR,
        LEGACY_AUDIO_DIR / "audio",
        PODCAST_DIR,
        PODCAST_DIR / "audio",
        PODCAST_DIR / "images",
    ]
    if lang:
        fallback_dirs.append(LEGACY_AUDIO_DIR / "translations" / lang)
        fallback_dirs.append(PODCAST_DIR / "translations" / lang)
    for base in fallback_dirs:
        for alt_name in alternate_basenames:
            candidate = base / alt_name
            if candidate.exists():
                return candidate

    direct_url = unwrap_op3(url)
    suffix = Path(unquote(path)).suffix or ".bin"
    cache_name = f"{hashlib.sha256(direct_url.encode()).hexdigest()[:12]}_{basename or 'asset'}"
    cache_path = DOWNLOAD_CACHE_DIR / cache_name
    if not cache_path.suffix and suffix:
        cache_path = cache_path.with_suffix(suffix)
    if cache_path.exists():
        return cache_path

    with urlopen(direct_url) as response, cache_path.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    return cache_path


def resolve_episode_cover_source(lang: str, episode: int, explicit_cover_url: str | None) -> Path:
    if explicit_cover_url:
        return resolve_local_path_from_url(explicit_cover_url, lang=lang)

    candidates = [
        LEGACY_AUDIO_DIR / f"episode_{episode:03d}_cover_{lang}.png",
        LEGACY_AUDIO_DIR / f"episode_{episode:03d}_cover.png",
        PODCAST_DIR / f"episode_{episode:03d}_cover_{lang}.png",
        PODCAST_DIR / f"episode_{episode:03d}_cover.png",
        PODCAST_DIR / "images" / f"episode_{episode:03d}_cover_{lang}.png",
        PODCAST_DIR / "images" / f"episode_{episode:03d}_cover.png",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        f"Could not resolve cover art for {lang.upper()} EP{episode:03d}"
    )


def parse_feed_inventory(lang: str) -> FeedInventory:
    repo = LANG_REPOS[lang]
    feed_path = FEED_PATHS[lang]
    text = feed_path.read_text(encoding="utf-8")
    root = ET.fromstring(text)
    channel = root.find("channel")
    if channel is None:
        raise RuntimeError(f"No channel element found in {feed_path}")

    channel_img = channel.find(f"{{{ITUNES_NS}}}image")
    if channel_img is None or "href" not in channel_img.attrib:
        raise RuntimeError(f"No channel image found in {feed_path}")

    episodes: list[EpisodeAsset] = []
    for item in channel.findall("item"):
        episode_text = item.findtext(f"{{{ITUNES_NS}}}episode")
        if not episode_text:
            continue

        enclosure = item.find("enclosure")
        if enclosure is None or "url" not in enclosure.attrib:
            raise RuntimeError(f"Episode {episode_text} in {feed_path} is missing enclosure URL")

        cover = item.find(f"{{{ITUNES_NS}}}image")
        guid = item.find("guid")
        episode = int(episode_text)
        audio_url = enclosure.attrib["url"]
        guid_url = None
        if guid is not None and guid.text:
            guid_text = guid.text.strip()
            if guid_text.startswith("http://") or guid_text.startswith("https://"):
                guid_url = guid_text
        cover_url = cover.attrib["href"] if cover is not None and "href" in cover.attrib else None

        episodes.append(
            EpisodeAsset(
                episode=episode,
                old_audio_url=audio_url,
                old_guid_url=guid_url,
                old_cover_url=cover_url,
                audio_source=resolve_local_path_from_url(audio_url, lang=lang),
                cover_source=resolve_episode_cover_source(lang, episode, cover_url),
            )
        )

    episodes.sort(key=lambda ep: ep.episode)
    return FeedInventory(
        lang=lang,
        repo=repo,
        feed_path=feed_path,
        channel_image_url=channel_img.attrib["href"],
        channel_image_source=resolve_local_path_from_url(channel_img.attrib["href"], lang=lang),
        episodes=episodes,
    )


def ensure_repo_initialized(repo: str) -> None:
    view = maybe_run(["gh", "api", f"repos/{repo}/contents"], capture=True)
    if view.returncode == 0:
        return

    log(f"Initializing empty repo {repo}...")
    with tempfile.TemporaryDirectory(prefix="openclaw-media-init-") as tmp:
        repo_dir = Path(tmp) / repo.split("/")[-1]
        run(["git", "clone", f"https://github.com/{repo}.git", str(repo_dir)])
        run(["git", "checkout", "-b", "main"], cwd=repo_dir)
        readme = repo_dir / "README.md"
        readme.write_text(
            f"# {repo.split('/')[-1]}\n\n"
            "GitHub release assets for OpenClaw podcast media.\n",
            encoding="utf-8",
        )
        run(["git", "add", "README.md"], cwd=repo_dir)
        run(["git", "commit", "-m", "Initialize media repo"], cwd=repo_dir)
        run(["git", "push", "-u", "origin", "main"], cwd=repo_dir)


def ensure_release_with_assets(repo: str, tag: str, title: str, assets: dict[str, Path]) -> None:
    with tempfile.TemporaryDirectory(prefix=f"openclaw-release-{tag}-") as tmp:
        temp_dir = Path(tmp)
        upload_paths = []
        for asset_name, source_path in assets.items():
            target_path = temp_dir / asset_name
            shutil.copy2(source_path, target_path)
            upload_paths.append(str(target_path))

        if gh_release_exists(repo, tag):
            run(["gh", "release", "upload", tag, "--repo", repo, "--clobber", *upload_paths])
        else:
            run([
                "gh", "release", "create", tag,
                "--repo", repo,
                "--title", title,
                "--notes", "",
                "--target", "main",
                *upload_paths,
            ])


def upload_inventory(inventory: FeedInventory) -> None:
    ensure_repo_initialized(inventory.repo)
    log(f"Uploading channel art for {inventory.lang.upper()} -> {inventory.repo}")
    ensure_release_with_assets(
        inventory.repo,
        "channel-art",
        "Channel Art",
        {"show_art.png": inventory.channel_image_source},
    )

    for episode in inventory.episodes:
        log(f"Uploading {inventory.lang.upper()} EP{episode.episode:03d}")
        ensure_release_with_assets(
            inventory.repo,
            episode.tag,
            f"EP{episode.episode:03d}",
            {
                episode.audio_asset_name: episode.audio_source,
                episode.cover_asset_name: episode.cover_source,
            },
        )


def rewrite_feed(inventory: FeedInventory) -> None:
    ET.register_namespace("itunes", ITUNES_NS)
    tree = ET.parse(inventory.feed_path)
    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        raise RuntimeError(f"No channel element found in {inventory.feed_path}")

    channel_image = channel.find(f"{{{ITUNES_NS}}}image")
    channel_image_url = release_asset_url(inventory.repo, "channel-art", "show_art.png")
    if channel_image is None:
        channel_image = ET.SubElement(channel, f"{{{ITUNES_NS}}}image")
    channel_image.set("href", channel_image_url)

    episode_map = {episode.episode: episode for episode in inventory.episodes}
    for item in channel.findall("item"):
        episode_text = item.findtext(f"{{{ITUNES_NS}}}episode")
        if not episode_text:
            continue

        episode_num = int(episode_text)
        episode = episode_map.get(episode_num)
        if episode is None:
            continue

        audio_direct = release_asset_url(inventory.repo, episode.tag, episode.audio_asset_name)
        cover_direct = release_asset_url(inventory.repo, episode.tag, episode.cover_asset_name)

        enclosure = item.find("enclosure")
        if enclosure is not None:
            enclosure.set("url", op3_wrap(audio_direct))

        guid = item.find("guid")
        if guid is None:
            guid = ET.SubElement(item, "guid", {"isPermaLink": "false"})
        guid.text = audio_direct
        guid.set("isPermaLink", "false")

        cover = item.find(f"{{{ITUNES_NS}}}image")
        if cover is None:
            cover = ET.SubElement(item, f"{{{ITUNES_NS}}}image")
        cover.set("href", cover_direct)

    ET.indent(tree, space="  ")
    tree.write(inventory.feed_path, encoding="utf-8", xml_declaration=True)


def hi_legacy_audio_paths(feed_inventory: FeedInventory) -> list[Path]:
    paths: set[Path] = set()
    for episode in feed_inventory.episodes:
        paths.add(LEGACY_AUDIO_DIR / "audio" / f"episode_{episode.episode:03d}_hi.mp3")
        paths.add(LEGACY_AUDIO_DIR / "translations" / "hi" / f"episode_{episode.episode:03d}_hi.mp3")

    existing = []
    for path in sorted(paths):
        if path.exists():
            existing.append(path)
    return existing


def remove_legacy_audio(lang: str, feed_inventory: FeedInventory) -> list[Path]:
    if lang != "hi":
        raise RuntimeError("This migration flow only supports legacy removal for Hindi right now.")

    removed: list[Path] = []
    for path in hi_legacy_audio_paths(feed_inventory):
        path.unlink()
        removed.append(path)
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate podcast media into per-language GitHub release repos.")
    parser.add_argument(
        "--upload-all",
        action="store_true",
        help="Upload all published feed assets into all per-language media repos.",
    )
    parser.add_argument(
        "--rewrite-feed",
        choices=["en", "es", "de", "pt", "hi"],
        help="Rewrite one feed to release asset URLs.",
    )
    parser.add_argument(
        "--remove-legacy-audio",
        choices=["hi"],
        help="Remove only one language's legacy audio from the old audio repo.",
    )
    args = parser.parse_args()

    if not (args.upload_all or args.rewrite_feed or args.remove_legacy_audio):
        parser.error("Choose at least one action.")

    inventories = {lang: parse_feed_inventory(lang) for lang in LANG_REPOS}

    if args.upload_all:
        for lang in ["en", "es", "de", "pt", "hi"]:
            upload_inventory(inventories[lang])

    if args.rewrite_feed:
        rewrite_feed(inventories[args.rewrite_feed])
        log(f"Rewrote {args.rewrite_feed.upper()} feed at {inventories[args.rewrite_feed].feed_path}")

    if args.remove_legacy_audio:
        removed = remove_legacy_audio(args.remove_legacy_audio, inventories[args.remove_legacy_audio])
        for path in removed:
            log(f"Removed legacy audio: {path}")


if __name__ == "__main__":
    main()
