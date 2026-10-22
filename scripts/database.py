"""Build the runnable SQLite audit database; also export PostgreSQL-compatible source inserts."""
from pathlib import Path
import sqlite3,json
ROOT=Path(__file__).resolve().parents[1]
def main():
 db=ROOT/'outputs/thirstyai.sqlite'
 with sqlite3.connect(db) as conn:
  conn.execute('PRAGMA foreign_keys=ON')
  conn.executescript((ROOT/'sql/schema.sql').read_text())
  conn.execute('DELETE FROM groundwater');conn.execute('DELETE FROM sources');conn.execute('DELETE FROM scenario_inputs')
  source_sql=[]
  for s in json.loads((ROOT/'research/sources.json').read_text()):
   values=[s[k] for k in ['id','title','url','scope','locator']]
   conn.execute('INSERT INTO sources VALUES (?,?,?,?,?)',values)
   source_sql.append('INSERT INTO sources VALUES ('+', '.join("'"+v.replace("'","''")+"'" for v in values)+');')
  conn.executescript((ROOT/'sql/seed.sql').read_text())
  for name,pue,wue in [('Baseline',1.2,1),('Alternative',1.4,.1)]:
   conn.execute('INSERT INTO scenario_inputs VALUES (?,?,?,?,?,?,?,?,?)',(name,1000,pue,wue,1,.4,'consumption','IT_kWh','illustrative_scenario'))
  conn.commit()
  print('SQL view:',conn.execute('SELECT scenario_id,total_l FROM vw_scenarios').fetchall())
  print('Groundwater rows:',conn.execute('SELECT COUNT(*) FROM vw_india_context').fetchone()[0])
  assert conn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 (ROOT/'sql/sources_seed.sql').write_text('\n'.join(source_sql)+'\n')
if __name__=='__main__':main()
