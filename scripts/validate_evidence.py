"""Fail closed before publishing source-linked evidence, including location overlays."""
from datetime import datetime,timedelta
import math,re

def validate_registry(sources,provenance):
 ids=[s['id'] for s in sources];captures={p['source_id']:p for p in provenance}
 if len(ids)!=len(set(ids)):raise ValueError('Duplicate source ID')
 if len(captures)!=len(provenance):raise ValueError('Duplicate source capture')
 for source in sources:
  ident=source['id'];record=captures.get(ident,{})
  if record.get('status')!='fetched_anchor_checked':raise ValueError('Source requires retrieval / human locator review: '+ident)
  if record.get('url')!=source['url']:raise ValueError('Provenance URL mismatch: '+ident)
  if not re.fullmatch('[a-f0-9]{64}',record.get('sha256','')):raise ValueError('Invalid SHA-256: '+ident)
  try:stamp=datetime.fromisoformat(record['retrieved_at'].replace('Z','+00:00'))
  except (KeyError,ValueError,TypeError) as exc:raise ValueError('Invalid retrieval timestamp: '+ident) from exc
  if stamp.tzinfo is None or stamp.utcoffset()!=timedelta(0):raise ValueError('Retrieval timestamp must be UTC: '+ident)
  if not record.get('bytes',0)>0 or not source.get('locator') or not source.get('licence'):raise ValueError('Incomplete source metadata: '+ident)
 return set(ids)
def validate_facts(rows,source_ids,value_key='value',nullable=False):
 for row in rows:
  if row.get('source_id') not in source_ids or not row.get('locator'):raise ValueError('Unknown source / missing locator')
  value=row.get(value_key)
  if nullable and value is None:continue
  try:
   if isinstance(value,bool) or not math.isfinite(float(value)) or float(value)<0:raise ValueError('Invalid fact value')
  except (TypeError,OverflowError) as exc:raise ValueError('Invalid fact value') from exc
