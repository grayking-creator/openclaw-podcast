#!/usr/bin/env python3
"""DGX website writer: import published GitHub covers as WebPs, commit only those paths."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import subprocess
from pathlib import Path


def run(cmd, cwd=None, check=True):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(f"Command failed: {' '.join(map(str, cmd))}\n{result.stdout}\n{result.stderr}")
    return result


def publish(repo, staging, episode, covers, message, empty_message):
    repo, staging = Path(repo).resolve(), Path(staging).resolve()
    if episode < 0 or not covers:
        raise ValueError('An episode and at least one cover are required')
    for name in covers:
        match = re.fullmatch(r'episode_(\d{3,})_cover(?:_(de|es|hi|pt))?\.png', name)
        if not match or int(match[1]) != episode:
            raise ValueError(f'Invalid cover for episode {episode}: {name}')
        if not (staging / name).is_file():
            raise FileNotFoundError(staging / name)
    common = run(['git', 'rev-parse', '--git-common-dir'], repo).stdout.strip()
    lock = (repo / common / 'website-podcast-publish.lock').resolve()
    with lock.open('a') as writer:
        fcntl.flock(writer, fcntl.LOCK_EX)
        if run(['git', 'branch', '--show-current'], repo).stdout.strip() != 'main':
            raise RuntimeError('Website publisher requires the canonical main checkout')
        run(['git', 'fetch', 'origin', 'main'], repo)
        if run(['git', 'merge-base', '--is-ancestor', 'HEAD', 'origin/main'], repo, False).returncode:
            raise RuntimeError('Website main contains local commits; refusing to publish unrelated work')
        run(['git', 'merge', '--ff-only', 'origin/main'], repo)
        sync = repo / 'frontend/scripts/sync-podcast-assets.mjs'
        if not sync.is_file():
            raise RuntimeError('Website GitHub image migration must be deployed before publishing covers')
        paths = ['frontend/src/data/podcast-assets.json']
        for name in covers:
            stem = Path(name).stem
            paths.extend(f'frontend/public/images/podcast/{stem}-{width}.webp' for width in (320, 640))
        if run(['git', 'status', '--porcelain', '--', *paths], repo).stdout.strip():
            raise RuntimeError('Podcast asset paths have pending edits; refusing to overwrite them')
        node = os.environ.get('WEBSITE_NODE', 'node')
        command = [node, str(sync), '--episode', str(episode), '--staging-dir', str(staging)]
        for name in covers:
            command.extend(['--cover', name])
        imported = json.loads(run(command, repo).stdout)
        imported_paths = imported['paths']
        if not imported_paths or not set(imported_paths).issubset(paths):
            raise RuntimeError('Image importer returned unexpected paths')
        run(['git', 'add', '--', *imported_paths], repo)
        changed = run(['git', 'diff', '--cached', '--quiet', '--', *imported_paths], repo, False).returncode
        if changed == 1:
            run(['git', 'commit', '--only', '-m', message, '--', *imported_paths], repo)
            action = 'committed'
        elif changed == 0:
            # --only without paths creates an empty commit without consuming the index.
            run(['git', 'commit', '--allow-empty', '--only', '-m', empty_message], repo)
            action = 'empty-deploy'
        else:
            raise RuntimeError('Unable to inspect podcast asset changes')
        run(['git', 'push', 'origin', 'main'], repo)
        head = run(['git', 'rev-parse', '--short', 'HEAD'], repo).stdout.strip()
        return f'websiteBuilder {action} and pushed: {head}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episode', required=True, type=int)
    parser.add_argument('--message', required=True)
    parser.add_argument('--empty-message', required=True)
    parser.add_argument('--staging-dir', required=True)
    parser.add_argument('--cover', action='append', default=[])
    args = parser.parse_args()
    repo = Path(os.environ.get('WEBSITEBUILDER_DIR', '~/.openclaw/workspace/websiteBuilder')).expanduser()
    print(publish(repo, args.staging_dir, args.episode, args.cover, args.message, args.empty_message))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
