"""Join only named administrative regions, never guessed facility coordinates."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
MAPPING={'LOC01':'Nevada','LOC03':'Arizona','LOC04':'Arizona','LOC06':'New Mexico','LOC07':'Arizona'}
def overlay(locations,regions):
 index={r['region']:r for r in regions};result=[]
 if len(index)!=len(regions):raise ValueError('Duplicate regional stress grain')
 for loc in locations:
  region=MAPPING.get(loc['location_id'])
  if region is None:continue
  if region not in index:raise ValueError('Missing verified regional context: '+region)
  s=index[region]
  result.append({**loc,'stress_region':region,'stress_score':s['score'],'stress_label':s['label'],'stress_period':'1979-2019 baseline; Aqueduct 4.0 release 2023','stress_source_id':'WRIADMIN','stress_locator':s['locator'],'match_scale':'STATE_PROXY_NOT_FACILITY_OR_BASIN','match_confidence':'Medium','match_caveat':'Named state/region matched to WRI demand-weighted administrative context. Not site stress, actual supply-source risk, or 2025 conditions.'})
 return result

def main():
 with (ROOT/'data/processed/location_water.csv').open(encoding='utf-8') as f:locations=list(csv.DictReader(f))
 with (ROOT/'data/processed/regional_water_stress.csv').open(encoding='utf-8') as f:regions=list(csv.DictReader(f))
 rows=overlay(locations,regions)
 with (ROOT/'data/processed/location_stress_overlay.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,lineterminator='\n',fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(f'{len(rows)} regional-context matches; zero verified facility/basin stress joins.')
if __name__=='__main__':main()
