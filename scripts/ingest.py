"""Download primary evidence, extract India's table, preserve raw hashes. Stdlib only."""
from pathlib import Path
from html.parser import HTMLParser
import csv
import hashlib
import json
import re
import os
import urllib.request
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
 {'id':'IEA26','title':'Key Questions on Energy and AI (2026)','publisher':'International Energy Agency','url':'https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary','locator':'Executive summary: updated data centre electricity demand outlook','scope':'All data centres; global electricity','licence':'CC BY 4.0 stated by publisher','anchor':'950'},
 {'id':'CGWB25','title':'Findings of Dynamic Groundwater Resources Assessment','publisher':'Ministry of Jal Shakti / PIB','url':'https://www.pib.gov.in/PressReleasePage.aspx?PRID=2206073&lang=1&reg=3','locator':'Annexure I: State-wise ground water resources of India, 2025','scope':'India state/UT annual groundwater; all uses','licence':'Source facts attributed; no blanket licence asserted; raw document excluded','anchor':'156.36'},
 {'id':'GOOGLE25','title':'Measuring the environmental impact of delivering AI at Google Scale','publisher':'Elsworth et al. / Google','url':'https://arxiv.org/html/2508.15734v1','locator':'Section 3.3 and Table 2; May 2025','scope':'Median Gemini Apps text prompt; direct consumptive cooling water','licence':'CC BY 4.0 on article','anchor':'0.26'},
 {'id':'WRI23','title':'Aqueduct 4.0 technical note','publisher':'World Resources Institute','url':'https://www.wri.org/research/aqueduct-40-updated-decision-relevant-global-water-risk-indicators','locator':'Technical note: screening limits and future periods','scope':'Modeled water context, not local facility impact','licence':'Creative Commons stated; dataset-specific terms need review before ingestion','anchor':'prioritization'},
 {'id':'MS24','title':'Next-generation datacenters consume zero water for cooling','publisher':'Microsoft','url':'https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/12/09/sustainable-by-design-next-generation-datacenters-consume-zero-water-for-cooling/','locator':'Mitigating energy impacts; footnote FY2024 withdrawal WUE','scope':'Company design disclosure; not fleet conversion evidence','licence':'Publisher copyright; raw article excluded','anchor':'withdrawal'},
 {'id':'LBNL26','title':'United States Data Center Energy Usage Report: 2025 Update','publisher':'Lawrence Berkeley National Laboratory','url':'https://bies.lbl.gov/publications/united-states-data-center-energy-2025','locator':'Publication abstract; June 2026; Reference Case','scope':'All US data centres; electricity scenarios','licence':'Metadata/facts attributed; full report terms need review','anchor':'649'},
]

class Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.tables=[]; self.rows=[]; self.cells=[]; self.parts=[]; self.incell=False
    def handle_starttag(self, tag, attrs):
        if tag=='table': self.rows=[]
        if tag=='tr': self.cells=[]
        if tag in ('td','th'): self.incell=True; self.parts=[]
    def handle_data(self, text):
        if self.incell: self.parts.append(text)
    def handle_endtag(self, tag):
        if tag in ('td','th'):
            self.cells.append(' '.join(' '.join(self.parts).split())); self.incell=False
        if tag=='tr' and self.cells: self.rows.append(self.cells)
        if tag=='table': self.tables.append(self.rows)


def extract_india(html):
    parser=Tables(); parser.feed(html)
    candidates=[t for t in parser.tables if t and any('Stage of Ground' in c for c in t[0])]
    if not candidates: raise ValueError('Groundwater source schema changed')
    result=[]
    for row in candidates[0]:
        if len(row)>=6 and row[0].isdigit():
            result.append({'state':row[1], 'recharge_bcm':float(row[2]),
                'extractable_bcm':float(row[3]),'extraction_bcm':float(row[4]),'stage_pct':float(row[5]),
                'year':2025,'source_id':'CGWB25','evidence_type':'government_reported',
                'scope':'state_or_UT_all_uses','locator':f'Annexure I row {row[0]}'})
    if len(result)!=36 or len({r['state'] for r in result})!=36:
        raise ValueError('Expected 36 unique state/UT observations; manual review required')
    if not all(0 <= r['stage_pct'] <= 500 for r in result): raise ValueError('Review extraction stage')
    return result


def fetch(source):
    req=urllib.request.Request(source['url'],headers={'User-Agent':'ThirstyAI-Research/0.1 (+source attribution)'})
    with urllib.request.urlopen(req,timeout=30) as response: data=response.read()
    text=data.decode('utf-8',errors='replace')
    is_pdf=data.startswith(b'%PDF')
    is_zip=data.startswith(b'PK')
    if not (is_pdf or is_zip) and source.get('anchor','').lower() not in text.lower(): raise ValueError(f"Source anchor changed: {source['id']}")
    digest=hashlib.sha256(data).hexdigest()
    raw=ROOT/'data/raw/captures'/source['id']/(digest+('.pdf' if is_pdf else '.zip' if is_zip else '.html')); raw.parent.mkdir(parents=True,exist_ok=True); raw.write_bytes(data)
    prior=json.loads((ROOT/'research/provenance.json').read_text(encoding='utf-8'))
    digest=hashlib.sha256(data).hexdigest()
    reviewed=any(p.get('source_id')==source['id'] and p.get('sha256')==digest and p.get('status')=='fetched_anchor_checked' for p in prior)
    status='fetched_anchor_checked' if reviewed else 'downloaded_pending_locator_review'
    return text, {'source_id':source['id'],'url':source['url'],'retrieved_at':datetime.now(timezone.utc).isoformat(),
                  'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'status':status,
                  'raw_path':raw.relative_to(ROOT).as_posix(),
                  'review_note':'Anchor checks detect drift; locator review remains required'}


def main():
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--refresh',action='store_true'); args=parser.parse_args()
    if not args.refresh: raise SystemExit('Use --refresh to retrieve registered public sources')
    # A refresh is an immutable candidate run, never an update of reviewed evidence.
    run=ROOT/'data/raw/refreshes'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    run.mkdir(parents=True)
    provenance=[]
    active_sources=json.loads((ROOT/'research/sources.json').read_text(encoding='utf-8'))
    for source in active_sources:
        try:
            content,record=fetch(source)
            if source['id']=='CGWB25':
                rows=extract_india(content)
                (run/'india_candidate.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
            provenance.append(record)
            print(source['id'],record['status'],record['bytes'])
        except Exception as exc:
            provenance.append({'source_id':source['id'],'status':'fetch_failed','error':str(exc)})
            print(source['id'],'fetch_failed',str(exc))
    (run/'attempt.json').write_text(json.dumps({'sources':active_sources,'captures':provenance},indent=2)+'\n',encoding='utf-8')
    print('Candidate run:',run)
    print('Reviewed registry and processed data unchanged. Use review_refresh.py after reviewing exact bytes/locators.')
    failures=[p['source_id'] for p in provenance if p['status']=='fetch_failed']
    if failures:raise SystemExit('Some downloads failed; reviewed snapshots preserved: '+', '.join(failures))

if __name__=='__main__':main()
