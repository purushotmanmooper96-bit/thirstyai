"""Capture a reviewed source with a hash. Never implies independent assurance."""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def capture(source, local_bytes=None):
 if source.get('human_reviewed') is not True or not source.get('review_note'):
  raise ValueError('Explicit human_reviewed=True and a locator review_note are required before capture')
 if local_bytes is None:
  with urllib.request.urlopen(urllib.request.Request(source['url'],headers={'User-Agent':'ThirstyAI Research/0.2'}),timeout=60) as response:raw=response.read()
 else:raw=local_bytes
 suffix='.pdf' if raw.startswith(b'%PDF') else '.zip' if raw.startswith(b'PK') else '.html'
 (ROOT/'data/raw').mkdir(exist_ok=True);(ROOT/'data/raw'/(source['id']+suffix)).write_bytes(raw)
 sources=json.loads((ROOT/'research/sources.json').read_text(encoding='utf-8'))
 sources=[s for s in sources if s['id']!=source['id']]+[source]
 p=json.loads((ROOT/'research/provenance.json').read_text(encoding='utf-8'));p=[x for x in p if x['source_id']!=source['id']]
 p.append({'source_id':source['id'],'url':source['url'],'retrieved_at':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'status':'fetched_anchor_checked','review_note':source.get('review_note','Human reviewed locator; extracted facts, no independent remeasurement')})
 (ROOT/'research/sources.json').write_text(json.dumps(sources,indent=2)+'\n',encoding='utf-8');(ROOT/'research/provenance.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
 return raw
