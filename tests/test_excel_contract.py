"""Cross-check the native verifier's fixtures and shipped formula cells, not Excel caches."""
import json, unittest
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from thirstyai.model import Inputs, calculate

ROOT = Path(__file__).resolve().parents[1]
class ExcelContract(unittest.TestCase):
 def test_native_case_expectations_match_python(self):
  cases=json.loads((ROOT/'tests/fixtures/excel_cases.json').read_text())
  for case in cases:
   with self.subTest(case=case['name']):
    args=dict(zip(('it_mwh','pue','wue','grid_l_kwh','carbon_kg_kwh'),case['inputs']))
    if isinstance(case['expected'][0],str):
     with self.assertRaises(ValueError):calculate(Inputs(**args))
    else:
     result=calculate(Inputs(**args))
     for key,expected in zip(('facility_mwh','direct_l','indirect_l','total_l','carbon_kg'),case['expected']):
      self.assertAlmostEqual(result[key],expected)
 def test_shipped_outputs_are_formulas_not_cached_constants(self):
  ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
  with ZipFile(ROOT/'excel/ThirstyAI_Audit.xlsx') as z:
   sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
  cells={c.attrib['r']:c for c in sheet.findall('.//s:c',ns)}
  for row in range(7,12):
   formula=cells[f'F{row}'].find('s:f',ns)
   self.assertIsNotNone(formula)
   self.assertIn('Invalid input',formula.text)
   self.assertIn('COUNT($B$7:$B$11)=5',formula.text)
