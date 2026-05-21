#!/usr/bin/env python3
"""Move local generated podcast artifacts to macOS Trash.

This script is intentionally conservative. It moves disposable local build
outputs to a timestamped folder under ~/.Trash instead of permanently deleting
them, and it refuses to move paths outside the podcast repo.
"""

from __future__ import annotations

import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent.resolve()
TRASH_PARENT = Path.home() / ".Trash"


def path_size_bytes(path: Path) -> int:
    if not path.exists() and not path.is_symlink():
        return 0
    try:
        if path.is_file() or path.is_symlink():
            return path.lstat().st_size
    except OSError:
        return 0

    total = 0
    for item in path.rglob("*"):
        try:
            total += item.lstat().st_size
        except OSError:
            pass
    return total


def format_size(num_bytes: int) -> str:
    units = ["B", "KiB", "MiB", "GiB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{size:.1f} GiB"


def require_inside_repo(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(PODCAST_DIR)
    except ValueError as exc:
        raise ValueError(f"Refusing to move path outside repo: {path}") from exc
    return resolved


def unique_dest(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem = dest.name
    for i in range(1, 1000):
        candidate = dest.with_name(f"{stem}.{i}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find unique Trash destination for {dest}")


def move_to_trash(path: Path, trash_root: Path, dry_run: bool) -> tuple[Path, int] | None:
    if not path.exists() and not path.is_symlink():
        return None
    src = require_inside_repo(path)
    rel = src.relative_to(PODCAST_DIR)
    dest = unique_dest(trash_root / rel)
    size = path_size_bytes(src)
    if dry_run:
        return dest, size
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    return dest, size


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def dead_pid_files() -> list[Path]:
    paths: list[Path] = []
    for path in (PODCAST_DIR / "logs").glob("*.pid"):
        try:
            raw = path.read_text(encoding="utf-8", errors="replace").strip()
            pid = int(raw)
        except Exception:
            paths.append(path)
            continue
        if not process_alive(pid):
            paths.append(path)
    return paths


def venv_cache_paths() -> list[Path]:
    venv = PODCAST_DIR / ".venv_shorts"
    if not venv.exists():
        return []
    paths = list(venv.rglob("__pycache__"))
    paths.extend(venv.rglob("*.pyc"))
    paths.extend(venv.rglob("*.pyo"))
    return sorted(set(paths), key=lambda p: (len(p.parts), str(p)))


def episode_staging_paths(ep_num: int) -> list[Path]:
    ep_str = f"{ep_num:03d}"
    paths = [
        PODCAST_DIR / "content_staging" / "audio" / f"episode_{ep_str}.mp3",
        PODCAST_DIR / "content_staging" / "shorts" / f"episode_{ep_str}",
    ]
    translations = PODCAST_DIR / "content_staging" / "translations"
    if translations.exists():
        paths.extend(translations.glob(f"episode_{ep_str}_*"))
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trash generated local podcast artifacts")
    parser.add_argument(
        "--completed-release",
        type=int,
        help="Clean staging/cache artifacts that are safe after this episode release completes",
    )
    parser.add_argument("--all-content-staging", action="store_true", help="Trash the entire content_staging directory")
    parser.add_argument("--archive", action="store_true", help="Trash the local archive directory")
    parser.add_argument("--dead-pids", action="store_true", help="Trash logs/*.pid files whose processes are not running")
    parser.add_argument("--prune-venv-cache", action="store_true", help="Trash .venv_shorts bytecode caches")
    parser.add_argument("--trash-shorts-venv", action="store_true", help="Trash the entire .venv_shorts directory")
    parser.add_argument("--dry-run", action="store_true", help="Print what would move without moving it")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets: list[Path] = []

    if args.completed_release is not None:
        targets.extend(episode_staging_paths(args.completed_release))
        args.dead_pids = True
        args.prune_venv_cache = True
    if args.all_content_staging:
        targets.append(PODCAST_DIR / "content_staging")
    if args.archive:
        targets.append(PODCAST_DIR / "archive")
    if args.trash_shorts_venv:
        targets.append(PODCAST_DIR / ".venv_shorts")
    if args.dead_pids:
        targets.extend(dead_pid_files())
    if args.prune_venv_cache:
        targets.extend(venv_cache_paths())

    # Preserve order while removing duplicates and nested paths under already
    # selected directories. If content_staging is selected, its children need not
    # be listed separately.
    ordered_targets = sorted(targets, key=lambda p: (len(p.parts), str(p)))
    deduped: list[Path] = []
    seen: set[Path] = set()
    for target in ordered_targets:
        if target in seen:
            continue
        seen.add(target)
        if any(target != existing and str(target).startswith(str(existing) + os.sep) for existing in deduped):
            continue
        deduped.append(target)

    existing = [path for path in deduped if path.exists() or path.is_symlink()]
    if not existing:
        print("No matching local artifacts to clean.")
        return 0

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trash_root = TRASH_PARENT / f"openclaw-podcast-cleanup-{stamp}"
    total = 0
    moved = 0
    for path in existing:
        result = move_to_trash(path, trash_root, args.dry_run)
        if result is None:
            continue
        dest, size = result
        total += size
        moved += 1
        action = "Would move" if args.dry_run else "Moved"
        print(f"{action}: {path.relative_to(PODCAST_DIR)} -> {dest} ({format_size(size)})")

    action = "Would move" if args.dry_run else "Moved"
    print(f"{action} {moved} path(s), {format_size(total)} total.")
    if not args.dry_run:
        print(f"Trash root: {trash_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
