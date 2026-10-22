import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from verify_postgres import compare_rows,analysis_statements
class PostgresComparison(unittest.TestCase):
 def test_order_and_tolerance(self):
  self.assertTrue(compare_rows([('b',None),('a',2200000.)],[('a',2200000.0000001),('b',None)]))
 def test_mismatch_is_failure(self):
  self.assertFalse(compare_rows([('a',1.)],[('a',2.)]))
  self.assertFalse(compare_rows([('a',None)],[('a',0)]))
  self.assertFalse(compare_rows([('a',1.)],[]))

class AnalysisQueries(unittest.TestCase):
 def test_checked_in_queries_are_read_only(self):
  root=Path(__file__).resolve().parents[1]
  self.assertEqual(len(analysis_statements((root/'sql/analysis.sql').read_text(encoding='utf-8'))),5)
  with self.assertRaises(ValueError):analysis_statements('DELETE FROM sources;')
