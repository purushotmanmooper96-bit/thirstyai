"""Build distributable evidence JSON, exports, SQL fixture and conditional scenarios."""
from pathlib import Path
import sys,json,csv,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from thirstyai.model import Inputs,calculate,project

def main():
 with (ROOT/'data/processed/india_groundwater_2025.csv').open() as f:india=list(csv.DictReader(f))
 for row in india:
  for key in ['recharge_bcm','extractable_bcm','extraction_bcm','stage_pct']:row[key]=float(row[key])
  row['year']=int(row['year'])
 sources=json.loads((ROOT/'research/sources.json').read_text());claims=json.loads((ROOT/'research/claims.json').read_text())
 prov=json.loads((ROOT/'research/provenance.json').read_text())
 verified={p['source_id'] for p in prov if p['status']=='fetched_anchor_checked'}
 if any(c['source_id'] not in verified for c in claims):raise ValueError('Headline source download missing')
 output={'release':'0.1.0','reviewed':'2026-10-22','coverage':{'india_states_uts':len(india),'facility_water_records':0,'global_water_total':None},'sources':sources,'claims':claims,'india':india,'provenance':prov}
 dest=ROOT/'dist/data';dest.mkdir(exist_ok=True)
 (dest/'evidence.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 for filename in ['india_groundwater_2025.csv']:(dest/filename).write_bytes((ROOT/'data/processed'/filename).read_bytes())
 with (dest/'claims.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(claims[0]));w.writeheader();w.writerows(claims)
 scenario=[]
 for year in range(2025,2036):
  for name,g,e in [('Demand only',.1,0),('Efficiency case',.1,.05),('Slower demand',.05,.05)]:
   scenario.append({'name':name,'year':year,'demand_growth':g,'efficiency_gain':e,**project(Inputs(),g,e,year)})
 with (ROOT/'outputs/scenarios.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(scenario[0]));w.writeheader();w.writerows(scenario)
 fixture=[]
 for r in india:
  s=r['state'].replace("'","''")
  fixture.append(f"INSERT INTO groundwater(state,year,recharge_bcm,extractable_bcm,extraction_bcm,stage_pct,source_id) VALUES ('{s}',2025,{r['recharge_bcm']},{r['extractable_bcm']},{r['extraction_bcm']},{r['stage_pct']},'CGWB25');")
 (ROOT/'sql/seed.sql').write_text('\n'.join(fixture)+'\n')
 manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'research').glob('*.json'))}
 (ROOT/'outputs/build_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 shutil.copytree(ROOT/'dist', ROOT/'docs/site', dirs_exist_ok=True)
 print(f'Built {len(india)} groundwater observations, {len(claims)} claims, {len(scenario)} scenario rows. No facility water records.')
if __name__=='__main__':main()
