"""Build distributable evidence JSON, exports, SQL fixture and conditional scenarios."""
from pathlib import Path
import sys,json,csv,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from thirstyai.model import Inputs,calculate,project
from static_content import insert,WARNING

def main():
 with (ROOT/'data/processed/india_groundwater_2025.csv').open() as f:india=list(csv.DictReader(f))
 for row in india:
  for key in ['recharge_bcm','extractable_bcm','extraction_bcm','stage_pct']:row[key]=float(row[key])
  row['year']=int(row['year'])
 sources=json.loads((ROOT/'research/sources.json').read_text());claims=json.loads((ROOT/'research/claims.json').read_text())
 prov=json.loads((ROOT/'research/provenance.json').read_text())
 verified={p['source_id'] for p in prov if p['status']=='fetched_anchor_checked'}
 if any(c['source_id'] not in verified for c in claims):raise ValueError('Headline source download missing')
 with (ROOT/'data/processed/company_water_reports.csv').open(encoding='utf-8') as f:companies=list(csv.DictReader(f))
 for row in companies:row['value']=None if row['value']=='' else float(row['value'])
 with (ROOT/'data/processed/location_water.csv').open(encoding='utf-8') as f:locations=list(csv.DictReader(f))
 for row in locations:row['value']=float(row['value'])
 with (ROOT/'data/processed/location_stress_overlay.csv').open(encoding='utf-8') as f:overlay=list(csv.DictReader(f))
 output={'scenario_warning':WARNING,'overlay':overlay,'companies':companies,'locations':locations,'release':'0.2.0','reviewed':'2026-10-22','coverage':{'india_states_uts':len(india),'facility_water_records':len(locations),'global_water_total':None},'sources':sources,'claims':claims,'india':india,'provenance':prov}
 dest=ROOT/'dist/data';dest.mkdir(exist_ok=True)
 (dest/'evidence.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 for filename in ['india_groundwater_2025.csv','company_water_reports.csv','location_water.csv','regional_water_stress.csv','location_stress_overlay.csv']:(dest/filename).write_bytes((ROOT/'data/processed'/filename).read_bytes())
 with (dest/'claims.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for c in claims for k in c)));w.writeheader();w.writerows(claims)
 scenario=[]
 for year in range(2025,2036):
  for name,g,e in [('Demand only',.1,0),('Efficiency case',.1,.05),('Slower demand',.05,.05)]:
   scenario.append({'warning':WARNING,'name':name,'year':year,'demand_growth':g,'efficiency_gain':e,**project(Inputs(),g,e,year)})
 with (ROOT/'outputs/scenarios.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(scenario[0]));w.writeheader();w.writerows(scenario)
 fixture=[]
 for r in india:
  s=r['state'].replace("'","''")
  fixture.append(f"INSERT INTO groundwater(state,year,recharge_bcm,extractable_bcm,extraction_bcm,stage_pct,source_id) VALUES ('{s}',2025,{r['recharge_bcm']},{r['extractable_bcm']},{r['extraction_bcm']},{r['stage_pct']},'CGWB25');")
 (ROOT/'sql/seed.sql').write_text('\n'.join(fixture)+'\n')
 manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'research').glob('*.json'))}
 (ROOT/'outputs/build_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 index=ROOT/'dist/index.html';index.write_text(insert(index.read_text(),output),encoding='utf-8')
 # GitHub Pages serves docs/ directly; keep exactly one content URL.
 for item in (ROOT/'dist').iterdir():
  target=ROOT/'docs'/item.name
  if item.is_dir():shutil.copytree(item,target,dirs_exist_ok=True)
  else:shutil.copy2(item,target)
 legacy=ROOT/'docs/site'
 if legacy.exists():shutil.rmtree(legacy)
 legacy.mkdir()
 (legacy/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>ThirstyAI has moved</title><link rel="canonical" href="https://purushotmanmooper96-bit.github.io/thirstyai/"><script>location.replace("../"+location.search+location.hash)</script><meta http-equiv="refresh" content="0;url=../"></head><body><p>ThirstyAI now has one canonical page. <a href="../">Open the evidence atlas</a>.</p><noscript>Use the link above to continue.</noscript></body></html>')
 print(f'Built {len(india)} groundwater observations, {len(claims)} claims, {len(scenario)} scenario rows. {len(locations)} curated company-reported location records.')
if __name__=='__main__':main()
