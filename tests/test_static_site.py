import unittest,json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class StaticSite(unittest.TestCase):
 def test_evidence_without_javascript(self):
  html=(ROOT/'dist/index.html').read_text()
  for text in ['<noscript>','Company water disclosures','10,523','Numerical claim register','1979–2019']:
   # JSON numbers are intentionally unformatted in static tables.
   self.assertIn(text.replace('10,523','10523'),html)
  for anchor in ['overview','lab','companies','locations','india','futures','evidence','solutions']:
   self.assertIn('id="'+anchor+'"',html)
  self.assertNotIn('Loading the evidence atlas',html)
 def test_canonical_and_legacy(self):
  html=(ROOT/'docs/index.html').read_text()
  self.assertEqual(html,(ROOT/'dist/index.html').read_text())
  self.assertIn('rel="canonical" href="https://purushotmanmooper96-bit.github.io/thirstyai/"',html)
  legacy=(ROOT/'docs/site/index.html').read_text()
  self.assertIn('location.search+location.hash',legacy)
  self.assertEqual(len(list((ROOT/'docs/site').iterdir())),1)
 def test_scenario_export_warnings(self):
  rows=list(csv.DictReader((ROOT/'outputs/scenarios.csv').open()))
  self.assertTrue(all(r['warning']=='ILLUSTRATIVE INPUTS - NOT MEASUREMENTS' for r in rows))
  app=(ROOT/'dist/app.mjs').read_text()
  self.assertIn("warning:'ILLUSTRATIVE INPUTS — NOT MEASUREMENTS'",app)
  self.assertIn("['ILLUSTRATIVE INPUTS - NOT MEASUREMENTS','year'",app)
  self.assertIn('scenario_warning',json.loads((ROOT/'dist/data/evidence.json').read_text()))
