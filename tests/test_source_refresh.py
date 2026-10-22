import unittest,sys,json,hashlib
from pathlib import Path
from unittest.mock import patch
from io import BytesIO
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import ingest
class RefreshReview(unittest.TestCase):
 def test_changed_bytes_require_review_even_if_anchor_matches(self):
  import tempfile
  raw=b'<html>anchor remains</html>'
  for same in [False,True]:
   with self.subTest(same=same),tempfile.TemporaryDirectory() as d:
    root=Path(d);(root/'research').mkdir()
    digest=hashlib.sha256(raw if same else b'old source').hexdigest()
    (root/'research/provenance.json').write_text(json.dumps([{'source_id':'TEST','sha256':digest,'status':'fetched_anchor_checked'}]),encoding='utf-8')
    with patch.object(ingest,'ROOT',root),patch.object(ingest.urllib.request,'urlopen',return_value=BytesIO(raw)):
     _,record=ingest.fetch({'id':'TEST','url':'https://example.org/research','anchor':'anchor'})
    self.assertEqual(record['status'],'fetched_anchor_checked' if same else 'downloaded_pending_locator_review')
