#!/usr/bin/env python3
"""
DGX-owned website deploy helper for AgentStack Daily podcast releases.

This script runs on the website owner machine. The M3 release pipeline stages
podcast cover assets into a temporary directory, then calls this helper over
SSH so websiteBuilder has exactly one writer.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def website_dir() -> Path:
    return Path(os.environ.get("WEBSITEBUILDER_DIR", "~/.openclaw/workspace/websiteBuilder")).expanduser()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish podcast website cover updates from staged files")
    parser.add_argument("--episode", required=True, type=int)
    parser.add_argument("--message", required=True)
    parser.add_argument("--empty-message", required=True)
    parser.add_argument("--staging-dir", required=True)
    parser.add_argument("--cover", action="append", default=[], help="Cover filename staged in --staging-dir")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = website_dir()
    staging = Path(args.staging_dir).expanduser()
    image_dir = repo / "frontend/public/images/podcast"
    if not repo.exists():
        raise FileNotFoundError(f"websiteBuilder repo not found: {repo}")
    if not staging.exists():
        raise FileNotFoundError(f"staging dir not found: {staging}")
    if not args.cover:
        raise RuntimeError("No --cover files provided")

    run(["git", "pull", "--rebase", "--autostash"], cwd=repo)
    image_dir.mkdir(parents=True, exist_ok=True)

    rel_paths: list[str] = []
    for filename in args.cover:
        src = staging / filename
        dst = image_dir / filename
        if not src.exists():
            raise FileNotFoundError(f"Missing staged cover: {src}")
        shutil.copy2(src, dst)
        rel_paths.append(str(dst.relative_to(repo)))

    run(["git", "add", "--"] + rel_paths, cwd=repo)
    diff = run(["git", "diff", "--cached", "--quiet"], cwd=repo, check=False)
    if diff.returncode != 0:
        run(["git", "commit", "-m", args.message], cwd=repo)
        action = "committed"
    else:
        run(["git", "commit", "--allow-empty", "-m", args.empty_message], cwd=repo)
        action = "empty-deploy"

    run(["git", "push", "origin", "main"], cwd=repo)
    head = run(["git", "rev-parse", "--short", "HEAD"], cwd=repo).stdout.strip()
    print(f"websiteBuilder {action} and pushed: {head}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
