from contextlib import closing
"""Execute PostgreSQL schema and compare every view to the reproduced SQLite database.
Requires psycopg 3; standard PG* environment variables; never prints credentials.
--load replaces only ThirstyAI tables inside thirstyai_db, in one transaction.
"""
from pathlib import Path
import argparse,math,os,sqlite3,sys
ROOT=Path(__file__).resolve().parents[1]
VIEWS=('vw_india_context','vw_scenarios','vw_company_reporting')
TABLES=('sources','groundwater','scenario_inputs','company_water_reports')
def equivalent(left,right):
 if len(left)!=len(right):return False
 return all((math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-6) if isinstance(a,(float,int)) and isinstance(b,(float,int)) else a==b) for a,b in zip(left,right))
def compare_rows(expected,actual):
 # Match complete rows; repeated first-column values must not depend on row order.
 if len(expected)!=len(actual):return False
 unmatched=list(actual)
 for row in expected:
  for index,candidate in enumerate(unmatched):
   if equivalent(row,candidate):unmatched.pop(index);break
  else:return False
 return True

def analysis_statements(text):
 clean='\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('--'))
 statements=[part.strip() for part in clean.split(';') if part.strip()]
 if any(not statement.upper().startswith('SELECT ') for statement in statements):
  raise ValueError('Only the checked-in SELECT analysis queries are supported')
 return statements

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--load',action='store_true');args=parser.parse_args()
 if os.environ.get('PGDATABASE')!='thirstyai_db':raise SystemExit('Set PGDATABASE=thirstyai_db. No other database will be modified.')
 try:import psycopg
 except ImportError:raise SystemExit('Install optional driver: python -m pip install "psycopg[binary]>=3.2,<4"')
 with closing(sqlite3.connect(ROOT/'outputs/thirstyai.sqlite')) as local,psycopg.connect(connect_timeout=15) as pg:
  if args.load:
   pg.execute((ROOT/'sql/postgresql_schema.sql').read_text(encoding='utf-8'))
   for table in reversed(TABLES):pg.execute('DELETE FROM '+table)
   # Exercise the exact seed files documented for pgAdmin, not a bypass via SQLite copying.
   for filename in ('sources_seed.sql','seed.sql','scenario_seed.sql','company_seed.sql'):
    pg.execute((ROOT/'sql'/filename).read_text(encoding='utf-8'))
  failed=False
  for view in VIEWS:
   cursor=local.execute('SELECT * FROM '+view);expected=cursor.fetchall();cols=[x[0] for x in cursor.description]
   actual=pg.execute('SELECT * FROM '+view)
   passed=cols==[x.name for x in actual.description] and compare_rows(expected,actual.fetchall())
   print(('PASS' if passed else 'FAIL')+' '+view+f' ({len(expected)} expected rows)');failed|=not passed
  for index,statement in enumerate(analysis_statements((ROOT/'sql/analysis.sql').read_text(encoding='utf-8')),1):
   expected=local.execute(statement).fetchall();actual=pg.execute(statement).fetchall()
   passed=compare_rows(expected,actual)
   print(('PASS' if passed else 'FAIL')+f' analysis query {index} ({len(expected)} expected rows)');failed|=not passed
  if failed:raise SystemExit(1)
 print('PASS PostgreSQL / SQLite parity; SQLite scenarios also checked against Python by reproduce.py')
if __name__=='__main__':
 try:main()
 except Exception as exc:print('FAIL PostgreSQL verification: '+type(exc).__name__+'. Check server, environment variables and schema; credentials are not logged.',file=sys.stderr);raise SystemExit(1)
