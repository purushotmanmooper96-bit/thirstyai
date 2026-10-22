"""Integration checks: source lineage, SQL/Python/JS parity, geometry-free coverage."""
from pathlib import Path
import json,sys,sqlite3,subprocess,random
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from thirstyai.model import Inputs,calculate

def main():
 with sqlite3.connect(ROOT/'outputs/thirstyai.sqlite') as c:
  assert c.execute('SELECT COUNT(*) FROM groundwater').fetchone()[0]==36
  for name,pue,wue in [('Baseline',1.2,1),('Alternative',1.4,.1)]:
   sql=c.execute('SELECT total_l FROM vw_scenarios WHERE scenario_id=?',(name,)).fetchone()[0]
   assert abs(sql-calculate(Inputs(pue=pue,wue=wue))['total_l'])<1e-6
  try:
   c.execute("INSERT INTO scenario_inputs VALUES ('Bad',1000,1.2,1,1,.4,'withdrawal','IT_kWh','illustrative_scenario')")
   raise AssertionError('SQL failed to reject withdrawal metric')
  except sqlite3.IntegrityError:pass
 random.seed(42)
 inputs=[Inputs(it_mwh=random.uniform(1,10000),pue=random.uniform(1,2),wue=random.uniform(0,3),grid_l_kwh=random.uniform(0,6)) for _ in range(30)]
 from dataclasses import asdict
 js="import{calculate}from './dist/model.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(calculate)));"
 process=subprocess.run(['node','--input-type=module','-e',js],cwd=ROOT,input=json.dumps([asdict(x) for x in inputs]),capture_output=True,text=True,check=True)
 for x,y in zip(inputs,json.loads(process.stdout)):
  for key in ['total_l','direct_l','indirect_l','facility_mwh','carbon_kg']:
   assert abs(calculate(x)[key]-y[key])<1e-6
 doc=json.loads((ROOT/'dist/data/evidence.json').read_text(encoding='utf-8'))
 assert len(doc['india'])==36 and doc['coverage']['global_water_total'] is None
 assert all(c['source_id'] in {s['id'] for s in doc['sources']} for c in doc['claims'])
 print('Integration passed: SQLite integrity + semantic guard; SQL/Python parity; 30 Python/JS parity cases; evidence coverage.')
if __name__=='__main__':main()
