import unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class EvidenceStatus(unittest.TestCase):
 def test_all_sources_have_hashed_capture(self):
  sources=json.loads((ROOT/'research/sources.json').read_text())
  provenance={r['source_id']:r for r in json.loads((ROOT/'research/provenance.json').read_text())}
  for s in sources:
   with self.subTest(source=s['id']):
    self.assertIn(s['id'],provenance)
    self.assertEqual(len(provenance[s['id']]['sha256']),64)
    self.assertTrue(provenance[s['id']]['retrieved_at'])
 def test_ten_areas_and_honest_global_gap(self):
  text=(ROOT/'docs/evidence_status.md').read_text()
  self.assertEqual(sum(line.startswith('| ') and ('Partial' in line or 'Strong' in line or 'Gap' in line) for line in text.splitlines()),10)
  self.assertIn('does **not** establish a global AI water total',text)
