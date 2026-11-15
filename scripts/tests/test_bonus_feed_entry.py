import pathlib
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'add_feed_entry.py'
FIXTURE = '''<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"><channel><lastBuildDate>Fri, 13 Nov 2026 21:00:00 +0000</lastBuildDate>
<item><title>Existing</title><guid>original</guid><pubDate>Fri, 13 Nov 2026 21:00:00 +0000</pubDate><itunes:episode>129</itunes:episode></item></channel></rss>'''

class BonusFeedTests(unittest.TestCase):
    def test_bonus_preserves_numbered_items_and_rejects_duplicate_guid(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'feed.xml'
            p.write_text(FIXTURE)
            args = ['python3', str(SCRIPT), str(p), '--episode-type', 'bonus', '--guid', 'shorts-test', '--title', 'Shorts: Chrome & Poppy', '--description', 'A useful short report on Chrome and agent capabilities.', '--pub-date', 'Sat, 14 Nov 2026 21:00:00 +0000', '--audio-url', 'https://example.com/audio.mp3', '--cover-url', 'https://example.com/cover.png', '--duration', '05:16', '--link', 'https://example.com/notes', '--length', '7580987']
            result = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            items = ET.parse(p).findall('./channel/item')
            self.assertEqual(len(items), 2)
            self.assertEqual(items[0].findtext('title'), 'Shorts: Chrome & Poppy')
            ns = '{http://www.itunes.com/dtds/podcast-1.0.dtd}'
            self.assertEqual(items[0].findtext(ns+'episodeType'), 'bonus')
            self.assertIsNone(items[0].find(ns+'episode'))
            self.assertEqual(items[1].findtext(ns+'episode'), '129')
            original = p.read_bytes()
            self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)
            self.assertEqual(p.read_bytes(), original)

if __name__ == '__main__':
    unittest.main()
