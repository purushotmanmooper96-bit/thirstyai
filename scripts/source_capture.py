"""Capture a reviewed source with a hash. Never implies independent assurance."""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
def capture(source, local_bytes=None):
 if source.get('human_reviewed') is not True or not source.get('review_note'):
  raise ValueError('Explicit human_reviewed=True and a locator review_note are required before capture')
 if local_bytes is None:
  with urllib.request.urlopen(urllib.request.Request(source['url'],headers={'User-Agent':'ThirstyAI Research/0.2'}),timeout=60) as response:raw=response.read()
 else:raw=local_bytes
 digest=hashlib.sha256(raw).hexdigest()
 if source.get('reviewed_sha256')!=digest or not source.get('reviewer'):
  raise ValueError('Exact reviewed_sha256 and reviewer required; download and inspect bytes before capture')
 suffix='.pdf' if raw.startswith(b'%PDF') else '.zip' if raw.startswith(b'PK') else '.html'
 raw_path=ROOT/'data/raw/captures'/source['id']/(digest+suffix)
 raw_path.parent.mkdir(parents=True,exist_ok=True);raw_path.write_bytes(raw)
 sources=json.loads((ROOT/'research/sources.json').read_text(encoding='utf-8'))
 sources=[s for s in sources if s['id']!=source['id']]+[source]
 p=json.loads((ROOT/'research/provenance.json').read_text(encoding='utf-8'))
 for old in p:
  if old['source_id']==source['id']:
   archive=ROOT/'research/reviews/capture_history'/f"{source['id']}-{old['sha256']}.json"
   archive.parent.mkdir(parents=True,exist_ok=True)
   if not archive.exists():archive.write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
 p=[x for x in p if x['source_id']!=source['id']]
 review_path=ROOT/'research/reviews/captures'/f"{source['id']}-{digest}.json"
 review_path.parent.mkdir(parents=True,exist_ok=True)
 if not review_path.exists():
  review_path.write_text(json.dumps({'source_id':source['id'],'sha256':digest,'url':source['url'],'locator':source['locator'],'scope':source['scope'],'reviewer':source['reviewer'],'reviewed_at':datetime.now(timezone.utc).isoformat(),'note':source['review_note']},indent=2)+'\n',encoding='utf-8')
 p.append({'source_id':source['id'],'url':source['url'],'retrieved_at':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'status':'fetched_anchor_checked','review_record':review_path.relative_to(ROOT).as_posix(),'review_note':source.get('review_note','Human reviewed locator; extracted facts, no independent remeasurement')})
 (ROOT/'research/sources.json').write_text(json.dumps(sources,indent=2)+'\n',encoding='utf-8');(ROOT/'research/provenance.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
 return raw
