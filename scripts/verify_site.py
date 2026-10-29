from pathlib import Path
from html.parser import HTMLParser
import collections,csv,gzip,json,re,hashlib
P=Path(__file__).resolve().parents[1]
class CheckHTML(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
h=CheckHTML();html=(P/'index.html').read_text();h.feed(html);duplicates=[k for k,v in collections.Counter(h.ids).items() if v>1];assert not duplicates,duplicates
js=(P/'assets/app.js').read_text();refs=set(re.findall(r"\$\('([^']+)'\)",js));assert not refs-set(h.ids),refs-set(h.ids)
for link in h.links:
 if link.startswith('#') and len(link)>1:assert link[1:] in h.ids,link
 elif not link.startswith(('#','http:','https:','mailto:')):assert (P/link).is_file(),link
meta=json.loads((P/'data/meta.json').read_text());local=json.loads((P/'data/local.json').read_text());g=json.loads((P/'data/geometry.json').read_text());assert len(g['paths'])==len(meta['areas'])==33755;assert len(meta['lads'])==296
for y in range(1995,2026):
 current=json.loads((P/f'data/history/{y}.json').read_text());bands=json.loads((P/f'data/bands/{y}.json').read_text());assert len(current)==len(bands)==33755
 assert sum(v[0] for v in current if v)==meta['annual'][str(y)]['n']
 assert all(sum(bands[i])==v[0] for i,v in enumerate(current) if v)
 for lad,counts in local['bands'][str(y)].items():assert sum(counts.values())==local['history'][str(y)][lad][0]
 assert sum(r[0] for r in local['history'][str(y)].values())==local['coverage'][str(y)]['mapped']
 if y>=2022:
  for k in range(1,7):
   pp=json.loads((P/f'data/policy/{y}_{k}.json').read_text());assert len(pp)==33755
   for i,v in enumerate(pp):
    if v:assert current[i] is not None and 0<=v[2]<=1 and 0<=v[3]<=1 and v[2]+v[3]<=1.000011
   summary=meta['summary'][str(y)][str(k)];assert summary['n']==meta['annual'][str(y)]['n'];assert summary['n_LAD']==296
assert round(meta['summary']['2025']['6']['reform_national_suits'],4)==-.1489
assert round(meta['summary']['2025']['6']['reform_within_suits'],4)==-.0243
# Ensure downloadable tables contain aggregates only, no addresses or transaction keys.
for f in (P/'downloads').glob('*.csv.gz'):
 with gzip.open(f,'rt') as handle:fields=next(csv.reader(handle))
 assert not set(fields)&{'postcode_key','post_code','ppd_row_id','transaction_id','paon','saon','street'}
assert 'sw2123@cam.ac.uk' in html and 'shizhen.wang.21@alumni.ucl.ac.uk' in html
assert 'Stuck in 1991:' in html
result={'status':'PASS','unique_html_ids':len(h.ids),'missing_js_element_ids':[],'history_years':31,'policy_scenarios':24,'lsoa_geometries':33755,'lad_geometries':296,'all_history_counts_reconciled':True,'all_local_band_counts_reconciled':True,'policy_shares_valid':True,'downloads_aggregate_only':True,'citation_and_emails_present':True,'html_sha256':hashlib.sha256(html.encode()).hexdigest(),'js_sha256':hashlib.sha256(js.encode()).hexdigest()}
(P/'SITE_VALIDATION.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
report=json.loads((P/'DATA_VALIDATION.json').read_text());report['data_files']=len(list((P/'data').rglob('*.json')));report['lsoa_lad_multiple_or_unobserved']=33755-sum(a['code'] in local['links'] for a in meta['areas']);(P/'DATA_VALIDATION.json').write_text(json.dumps(report,indent=2))
