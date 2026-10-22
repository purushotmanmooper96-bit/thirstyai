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

 def test_failed_refresh_preserves_reviewed_registry_and_processed_data(self):
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'research').mkdir();(root/'data/processed').mkdir(parents=True)
   sources=[{'id':'TEST','url':'https://example.org'}]
   (root/'research/sources.json').write_text(json.dumps(sources),encoding='utf-8')
   (root/'research/provenance.json').write_text('[{"source_id":"TEST","status":"fetched_anchor_checked"}]',encoding='utf-8')
   (root/'data/processed/india_groundwater_2025.csv').write_text('reviewed snapshot',encoding='utf-8')
   paths=[root/'research/sources.json',root/'research/provenance.json',root/'data/processed/india_groundwater_2025.csv']
   before={p:p.read_bytes() for p in paths}
   with patch.object(ingest,'ROOT',root),patch.object(ingest,'fetch',side_effect=TimeoutError('offline')),patch.object(sys,'argv',['ingest.py','--refresh']):
    with self.assertRaises(SystemExit):ingest.main()
   self.assertEqual(before,{p:p.read_bytes() for p in paths})
   self.assertEqual(len(list((root/'data/raw/refreshes').glob('*/attempt.json'))),1)

 def test_review_promotion_binds_hash_and_preserves_previous_capture(self):
  import tempfile,review_refresh
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'research').mkdir();run=root/'run';run.mkdir()
   source={'id':'TEST','url':'https://example.org','locator':'Table 1','scope':'test','licence':'test'}
   raw=root/'data/raw/captures/TEST/new.html';raw.parent.mkdir(parents=True);raw.write_bytes(b'new')
   sha=hashlib.sha256(b'new').hexdigest()
   (root/'research/sources.json').write_text(json.dumps([source]))
   (root/'research/provenance.json').write_text(json.dumps([{'source_id':'TEST','sha256':'a'*64}]))
   attempt={'sources':[source],'captures':[{'source_id':'TEST','sha256':sha,'raw_path':raw.relative_to(root).as_posix(),'status':'downloaded_pending_locator_review','retrieved_at':'2026-10-22T00:00:00+00:00'}]}
   (run/'attempt.json').write_text(json.dumps(attempt))
   with patch.object(review_refresh,'ROOT',root):
    with self.assertRaises(ValueError):review_refresh.promote(run,'TEST','b'*64,'Reviewer','Table 1 reviewed')
    review_refresh.promote(run,'TEST',sha,'Reviewer','Table 1 reviewed')
   self.assertTrue((root/'research/reviews/capture_history'/('TEST-'+'a'*64+'.json')).exists())
   current=json.loads((root/'research/provenance.json').read_text())[0]
   self.assertEqual(current['sha256'],sha);self.assertIn('review_record',current)
