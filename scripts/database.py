"""Build the runnable SQLite audit database; also export PostgreSQL-compatible source inserts."""
from pathlib import Path
import sqlite3,json,csv
ROOT=Path(__file__).resolve().parents[1]
def main():
 db=ROOT/'outputs/thirstyai.sqlite'
 with sqlite3.connect(db) as conn:
  conn.execute('PRAGMA foreign_keys=ON')
  conn.executescript((ROOT/'sql/schema.sql').read_text())
  conn.execute('DELETE FROM company_water_reports');conn.execute('DELETE FROM groundwater');conn.execute('DELETE FROM sources');conn.execute('DELETE FROM scenario_inputs')
  source_sql=[]
  for s in json.loads((ROOT/'research/sources.json').read_text()):
   values=[s[k] for k in ['id','title','url','scope','locator']]
   conn.execute('INSERT INTO sources VALUES (?,?,?,?,?)',values)
   source_sql.append('INSERT INTO sources VALUES ('+', '.join("'"+v.replace("'","''")+"'" for v in values)+');')
  conn.executescript((ROOT/'sql/seed.sql').read_text())
  for name,pue,wue in [('Baseline',1.2,1),('Alternative',1.4,.1)]:
   conn.execute('INSERT INTO scenario_inputs VALUES (?,?,?,?,?,?,?,?,?)',(name,1000,pue,wue,1,.4,'consumption','IT_kWh','illustrative_scenario'))
  with (ROOT/'data/processed/company_water_reports.csv').open(encoding='utf-8') as f:
   company=list(csv.DictReader(f))
  for row in company:
   row['value']=None if row['value']=='' else float(row['value'])
   conn.execute('INSERT INTO company_water_reports VALUES ('+','.join('?' for _ in row)+')',list(row.values()))
  for table,filename in [('scenario_inputs','scenario_seed.sql'),('company_water_reports','company_seed.sql')]:
   statements=[]
   for row in conn.execute('SELECT * FROM '+table):
    values=['NULL' if v is None else str(v) if isinstance(v,(int,float)) else "'"+v.replace("'","''")+"'" for v in row]
    statements.append('INSERT INTO '+table+' VALUES ('+', '.join(values)+');')
   (ROOT/'sql'/filename).write_text('\n'.join(statements)+'\n')
  conn.commit()
  print('SQL view:',conn.execute('SELECT scenario_id,total_l FROM vw_scenarios').fetchall())
  print('Groundwater rows:',conn.execute('SELECT COUNT(*) FROM vw_india_context').fetchone()[0])
  assert conn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 (ROOT/'sql/sources_seed.sql').write_text('\n'.join(source_sql)+'\n')
if __name__=='__main__':main()
