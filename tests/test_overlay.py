import unittest,sys,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from overlay import overlay
class OverlayTests(unittest.TestCase):
 def test_overlay_uses_only_exact_named_regions(self):
  with (ROOT/'data/processed/location_water.csv').open() as f:l=list(csv.DictReader(f))
  with (ROOT/'data/processed/regional_water_stress.csv').open() as f:r=list(csv.DictReader(f))
  result=overlay(l,r)
  self.assertEqual(len(result),5)
  self.assertTrue(all(x['match_scale']=='STATE_PROXY_NOT_FACILITY_OR_BASIN' for x in result))
  self.assertFalse(any('latitude' in x or 'longitude' in x for x in result))
 def test_unmatched_is_not_assigned_safe(self):self.assertEqual(overlay([{'location_id':'UNKNOWN'}],[]),[])
 def test_duplicate_region_rejected(self):
  with self.assertRaises(ValueError):overlay([],[{'region':'Arizona'},{'region':'Arizona'}])
