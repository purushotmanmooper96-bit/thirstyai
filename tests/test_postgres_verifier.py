import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from verify_postgres import compare_rows
class PostgresComparison(unittest.TestCase):
 def test_order_and_tolerance(self):
  self.assertTrue(compare_rows([('b',None),('a',2200000.)],[('a',2200000.0000001),('b',None)]))
 def test_mismatch_is_failure(self):
  self.assertFalse(compare_rows([('a',1.)],[('a',2.)]))
  self.assertFalse(compare_rows([('a',None)],[('a',0)]))
  self.assertFalse(compare_rows([('a',1.)],[]))
