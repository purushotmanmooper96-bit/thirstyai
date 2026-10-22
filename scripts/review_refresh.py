"""Promote one explicitly reviewed source capture; refresh never promotes itself."""
import argparse,csv,hashlib,json,os,re,tempfile
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]

def promote(run,source_id,expected_sha,reviewer,note):
 if not reviewer.strip() or not note.strip() or not re.fullmatch('[a-f0-9]{64}',expected_sha):
  raise ValueError('Reviewer, exact locator review note and expected SHA-256 required')
 attempt=json.loads((Path(run)/'attempt.json').read_text(encoding='utf-8'))
 record=next((r for r in attempt['captures'] if r['source_id']==source_id),None)
 if not record or record.get('status') not in ('fetched_anchor_checked','downloaded_pending_locator_review'):
  raise ValueError('No successful candidate for this source')
 sources=json.loads((ROOT/'research/sources.json').read_text(encoding='utf-8'))
 source=next(s for s in sources if s['id']==source_id)
 candidate=next(s for s in attempt['sources'] if s['id']==source_id)
 if source!=candidate:raise ValueError('Registry changed since download; review a fresh candidate')
 raw=(ROOT/record['raw_path']).resolve()
 if not raw.is_relative_to((ROOT/'data/raw/captures').resolve()):raise ValueError('Capture path outside raw captures')
 if hashlib.sha256(raw.read_bytes()).hexdigest()!=expected_sha or record['sha256']!=expected_sha:
  raise ValueError('Reviewed bytes do not match expected hash')
 review={'source_id':source_id,'url':source['url'],'sha256':expected_sha,'locator':source['locator'],
         'reviewer':reviewer,'reviewed_at':datetime.now(timezone.utc).isoformat(),'note':note,
         'scope':source['scope'],'licence':source['licence'],'retrieved_at':record['retrieved_at']}
 review_path=ROOT/'research/reviews/captures'/f'{source_id}-{expected_sha}.json'
 if review_path.exists():
  existing=json.loads(review_path.read_text(encoding='utf-8'))
  if existing['sha256']!=expected_sha:raise ValueError('Immutable review mismatch')
 else:
  review_path.parent.mkdir(parents=True,exist_ok=True)
  with review_path.open('x',encoding='utf-8') as f:json.dump(review,f,indent=2);f.write('\n')
 records=json.loads((ROOT/'research/provenance.json').read_text(encoding='utf-8'))
 # Preserve old reviewed metadata before replacing the current pointer.
 old=next((p for p in records if p['source_id']==source_id),None)
 if old:
  archive=ROOT/'research/reviews/capture_history'/f"{source_id}-{old['sha256']}.json"
  archive.parent.mkdir(parents=True,exist_ok=True)
  if not archive.exists():archive.write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
 current={k:v for k,v in record.items() if k!='raw_path'}
 current.update(status='fetched_anchor_checked',review_note=note,review_record=review_path.relative_to(ROOT).as_posix())
 records=[p for p in records if p['source_id']!=source_id]+[current]
 updates={ROOT/'research/provenance.json':(json.dumps(records,indent=2)+'\n').encode()}
 if source_id=='CGWB25':
  from ingest import extract_india
  import io
  rows=extract_india(raw.read_text(encoding='utf-8'))
  text=io.StringIO(newline='');w=csv.DictWriter(text,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
  updates[ROOT/'data/processed/india_groundwater_2025.csv']=text.getvalue().encode()
 backups={p:p.read_bytes() for p in updates}
 try:
  for path,content in updates.items():
   with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as f:f.write(content);temp=Path(f.name)
   os.replace(temp,path)
 except Exception:
  for path,content in backups.items():path.write_bytes(content)
  raise
 return review

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--run',type=Path,required=True);p.add_argument('--source-id',required=True)
 p.add_argument('--sha256',required=True);p.add_argument('--reviewer',required=True);p.add_argument('--note',required=True)
 a=p.parse_args();promote(a.run,a.source_id,a.sha256,a.reviewer,a.note)
 print('Reviewed capture promoted. Rebuild and inspect changed facts before committing.')
if __name__=='__main__':main()
