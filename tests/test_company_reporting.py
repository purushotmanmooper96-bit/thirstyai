from contextlib import closing
import csv,sqlite3,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CompanyReportingTests(unittest.TestCase):
 def test_three_distinct_operators(self):
  with (ROOT/'data/processed/company_water_reports.csv').open() as f:rows=list(csv.DictReader(f))
  self.assertEqual({r['company'] for r in rows},{'Google','Microsoft','Meta'})
  self.assertTrue(all(r['locator'] and r['source_id'] and r['confidence'] and r['assurance'] for r in rows))
 def test_missing_wue_not_zero(self):
  with (ROOT/'data/processed/company_water_reports.csv').open() as f:rows=list(csv.DictReader(f))
  self.assertEqual(next(r['value'] for r in rows if r['company']=='Meta' and r['metric']=='WUE'),'')
 def test_comparison_flags(self):
  with closing(sqlite3.connect(ROOT/'outputs/thirstyai.sqlite')) as c, c:
   rows=c.execute("SELECT comparison_flag FROM vw_company_reporting WHERE metric='consumption'").fetchall()
   self.assertTrue(rows and all(r[0]=='DEFINITIONS_PERIODS_OR_SCOPES_DIFFER' for r in rows))
 def test_latest_periods_are_not_aligned(self):
  with closing(sqlite3.connect(ROOT/'outputs/thirstyai.sqlite')) as c, c:
   self.assertGreater(c.execute('SELECT COUNT(DISTINCT period) FROM company_water_reports').fetchone()[0],1)
