import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('website_publisher', Path(__file__).parents[1] / 'publish_podcast_website_update.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WebsitePublishTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / 'remote.git'
        self.repo = self.root / 'website'
        subprocess.run(['git', 'init', '--bare', str(self.remote)], check=True, capture_output=True)
        self.repo.mkdir()
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.com')
        self.git('remote', 'add', 'origin', str(self.remote))
        sync = self.repo / 'frontend/scripts/sync-podcast-assets.mjs'
        sync.parent.mkdir(parents=True)
        sync.write_text('''import json, pathlib, sys
r=pathlib.Path.cwd()
p=['frontend/src/data/podcast-assets.json','frontend/public/images/podcast/episode_126_cover-320.webp','frontend/public/images/podcast/episode_126_cover-640.webp']
for name in p:
 path=r/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('preview')
print(json.dumps({'paths':p}))
''')
        (self.repo / 'unrelated.txt').write_text('original')
        self.git('add', '.')
        self.git('commit', '-m', 'initial')
        self.git('push', '-u', 'origin', 'main')
        self.staging = self.root / 'staging'
        self.staging.mkdir()
        (self.staging / 'episode_126_cover.png').write_bytes(b'staged original')
        self.env = patch.dict(os.environ, {'WEBSITE_NODE': sys.executable})
        self.env.start()
        self.addCleanup(self.env.stop)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.repo, stderr=subprocess.DEVNULL).decode().strip()

    def publish(self):
        return MODULE.publish(self.repo, self.staging, 126, ['episode_126_cover.png'], 'cover previews', 'refresh feed')

    def test_scoped_and_empty_commits_preserve_unrelated_staged_and_unstaged_work(self):
        (self.repo / 'unrelated.txt').write_text('staged work')
        self.git('add', 'unrelated.txt')
        (self.repo / 'unrelated.txt').write_text('unstaged work')
        self.assertIn('committed', self.publish())
        changed = self.git('diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD').splitlines()
        self.assertEqual(len(changed), 3)
        self.assertNotIn('unrelated.txt', changed)
        self.assertEqual(self.git('show', 'HEAD:unrelated.txt'), 'original')
        self.assertEqual(self.git('show', ':unrelated.txt'), 'staged work')
        self.assertEqual((self.repo / 'unrelated.txt').read_text(), 'unstaged work')
        self.assertIn('empty-deploy', self.publish())
        self.assertEqual(self.git('diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'), '')
        self.assertEqual(self.git('show', ':unrelated.txt'), 'staged work')
        self.assertFalse((self.repo / 'frontend/public/images/podcast/episode_126_cover.png').exists())

    def test_refuses_dirty_asset_paths(self):
        self.publish()
        target = self.repo / 'frontend/src/data/podcast-assets.json'
        target.write_text('pending edit')
        with self.assertRaisesRegex(RuntimeError, 'pending edits'):
            self.publish()
        self.assertEqual(target.read_text(), 'pending edit')

    def test_rejects_path_traversal_wrong_episode_and_local_commits(self):
        for name in ['../episode_126_cover.png', 'episode_127_cover.png']:
            with self.assertRaises(ValueError):
                MODULE.publish(self.repo, self.staging, 126, [name], 'cover', 'empty')
        (self.repo / 'unrelated.txt').write_text('local commit')
        self.git('commit', '-am', 'unpublished work')
        with self.assertRaisesRegex(RuntimeError, 'local commits'):
            self.publish()


if __name__ == '__main__':
    unittest.main()
