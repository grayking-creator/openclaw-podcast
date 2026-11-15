import tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from add_feed_entry import update_item_link
class LinkUpdateTests(unittest.TestCase):
 def test_update_only_target_and_idempotent(self):
  source='<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"><channel><lastBuildDate>old</lastBuildDate><item><guid>x</guid><link>https://old.test/</link><description>Text. Show notes: https://old.test/</description><pubDate>old</pubDate><itunes:duration>05:16</itunes:duration><enclosure url="https://audio.test/a.mp3"/></item><item><guid>y</guid><link>https://other.test/</link></item></channel></rss>'
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'feed.xml';p.write_text(source);update_item_link(p,'x','https://new.test/');actual=p.read_text();self.assertEqual(actual,source.replace('https://old.test/','https://new.test/'));update_item_link(p,'x','https://new.test/');self.assertEqual(actual,p.read_text())
 def test_missing_guid_leaves_original(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'feed.xml';p.write_text('<rss><channel/></rss>')
   with self.assertRaises(ValueError):update_item_link(p,'no','https://new.test/')
   self.assertEqual(p.read_text(),'<rss><channel/></rss>')
if __name__=='__main__':unittest.main()
