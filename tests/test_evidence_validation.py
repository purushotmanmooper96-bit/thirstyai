import unittest,sys,json,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_evidence import validate_registry,validate_facts
from source_capture import capture
ROOT=Path(__file__).resolve().parents[1]
class EvidenceValidation(unittest.TestCase):
 def setUp(self):
  self.sources=json.loads((ROOT/'research/sources.json').read_text(encoding='utf-8'))
  self.prov=json.loads((ROOT/'research/provenance.json').read_text(encoding='utf-8'))
 def test_location_only_source_also_requires_review(self):
  next(p for p in self.prov if p['source_id']=='WRIADMIN')['status']='downloaded_pending_locator_review'
  with self.assertRaises(ValueError):validate_registry(self.sources,self.prov)
 def test_invalid_hash_or_timestamp_or_url_rejected(self):
  for key,value in [('sha256','fake'),('retrieved_at','2026-10-22'),('url','https://example.org/changed')]:
   records=copy.deepcopy(self.prov);records[0][key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):validate_registry(self.sources,records)
 def test_unknown_source_nonfinite_and_negative_facts_rejected(self):
  for change in [{'value':'nan'},{'value':True},{'value':-1},{'source_id':'UNKNOWN'},{'locator':''}]:
   row={'value':1,'source_id':'KNOWN','locator':'Table 1'}|change
   with self.subTest(change=change),self.assertRaises(ValueError):validate_facts([row],{'KNOWN'})
 def test_capture_cannot_imply_unperformed_review(self):
  with self.assertRaises(ValueError):capture({'id':'UNREVIEWED'},local_bytes=b'test')
