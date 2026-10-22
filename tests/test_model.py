import unittest
from dataclasses import replace
from pathlib import Path
import json, csv
from thirstyai.model import Inputs, calculate, compare, break_even_grid, capacity_energy, project

class AccountingTests(unittest.TestCase):
 def test_known_accounting(self):
  r=calculate(Inputs()); self.assertEqual(r['direct_l'],1_000_000);self.assertEqual(r['indirect_l'],1_200_000);self.assertEqual(r['total_l'],2_200_000)
 def test_withdrawal_rejected(self):
  with self.assertRaises(ValueError):calculate(Inputs(water_metric='withdrawal'))
 def test_wrong_energy_denominator_rejected(self):
  with self.assertRaises(ValueError):calculate(Inputs(wue_denominator='facility_kWh'))
 def test_indirect_double_count_rejected(self):
  with self.assertRaises(ValueError):calculate(Inputs(includes_indirect=True))
 def test_missing_negative_nonfinite_rejected(self):
  for v in [None,-1,float('nan'),float('inf'),True,'1']:
   with self.subTest(v=v),self.assertRaises(ValueError):calculate(Inputs(wue=v))
 def test_pue_below_one_rejected(self):
  with self.assertRaises(ValueError):calculate(Inputs(pue=0.9))
 def test_zero_is_valid(self):
  self.assertEqual(calculate(Inputs(wue=0,grid_l_kwh=0))['total_l'],0)
 def test_zero_baseline_pct_is_null(self):
  b=Inputs(wue=0,grid_l_kwh=0);self.assertIsNone(compare(b,b)['water_saved_pct'])
 def test_alternative_tradeoff(self):
  r=compare(Inputs(),Inputs(pue=1.4,wue=.1));self.assertAlmostEqual(r['water_saved_l'],700000);self.assertEqual(r['energy_change_mwh'],200)
 def test_negative_savings_allowed(self):
  r=compare(Inputs(grid_l_kwh=5),Inputs(pue=1.4,wue=.1,grid_l_kwh=5));self.assertLess(r['water_saved_l'],0)
 def test_break_even(self):self.assertAlmostEqual(break_even_grid(Inputs(),Inputs(pue=1.4,wue=.1)),4.5)
 def test_workload_mismatch(self):
  with self.assertRaises(ValueError):compare(Inputs(),Inputs(it_mwh=2))
 def test_capacity(self):self.assertEqual(capacity_energy(10,.5,8760),43800)
 def test_projection(self):self.assertAlmostEqual(project(Inputs(),.1,0,2026)['total_l'],2420000)
 def test_no_change_projection(self):self.assertEqual(project(Inputs(),0,0,2035)['total_l'],calculate(Inputs())['total_l'])
 def test_projection_bounds(self):
  with self.assertRaises(ValueError):project(Inputs(),.1,.1,2024)

class EvidenceTests(unittest.TestCase):
 def test_india_grain_and_completeness(self):
  root=Path(__file__).resolve().parents[1]
  with (root/'data/processed/india_groundwater_2025.csv').open() as f:rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),36);self.assertEqual(len({r['state'] for r in rows}),36)
  self.assertTrue(all(r['source_id']=='CGWB25' and r['year']=='2025' for r in rows))
 def test_stage_not_recomputed_from_rounded_volumes(self):
  root=Path(__file__).resolve().parents[1]
  with (root/'data/processed/india_groundwater_2025.csv').open() as f:rows=list(csv.DictReader(f))
  row=next(r for r in rows if r['state']=='Lakshadweep')
  self.assertEqual(float(row['extraction_bcm']),0);self.assertEqual(float(row['stage_pct']),57.79)
 def test_claim_lineage(self):
  root=Path(__file__).resolve().parents[1]
  sources={s['id'] for s in json.loads((root/'research/sources.json').read_text(encoding='utf-8'))}
  claims=json.loads((root/'research/claims.json').read_text(encoding='utf-8'))
  self.assertTrue(all(c['source_id'] in sources and c['locator'] and c['caveat'] for c in claims))

if __name__=='__main__':unittest.main()
