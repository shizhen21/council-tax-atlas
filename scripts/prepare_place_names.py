"""Add ONS 2026 best-fit ward reference labels; statistical groups remain unchanged."""
from pathlib import Path
import concurrent.futures,json,urllib.request,urllib.parse,time
P=Path(__file__).resolve().parents[1]
BASE='https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LSOA21_WD26_LAD26_EW_LU/FeatureServer/0/query'
def query(params):
 params={'where':"LSOA21CD LIKE 'E%'",'f':'json',**params}
 url=BASE+'?'+urllib.parse.urlencode(params)
 for attempt in range(3):
  try:
   with urllib.request.urlopen(url,timeout=60) as response:d=json.load(response)
   if 'error' in d:raise RuntimeError(d['error'])
   return d
  except Exception:
   if attempt==2:raise
   time.sleep(2)
n=query({'returnCountOnly':'true'})['count'];print('ONS English LSOA records:',n,flush=True)
def page(offset):return query({'outFields':'LSOA21CD,LSOA21NM,WD26CD,WD26NM,LAD26CD,LAD26NM','returnGeometry':'false','orderByFields':'ObjectId','resultOffset':offset,'resultRecordCount':1000})['features']
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for features in pool.map(page,range(0,n,1000)):
  rows.extend(f['attributes'] for f in features)
assert len(rows)==n
lookup={r['LSOA21CD']:[r['WD26CD'],r['WD26NM'],r['LAD26CD'],r['LAD26NM']] for r in rows};assert len(lookup)==n
m=json.loads((P/'data/meta.json').read_text());missing=[a['code'] for a in m['areas'] if a['code'] not in lookup];assert not missing,missing
assert lookup['E01000089'][1]=='Beam'
record={'source':'Office for National Statistics: LSOA (2021) to Electoral Ward (2026) to LAD (2026) Best Fit Lookup in EW','source_url':'https://www.data.gov.uk/dataset/742f00f4-9567-4bf4-be0a-d827df9c6c2a/lsoa-2021-to-electoral-ward-2026-to-lad-2026-best-fit-lookup-in-ew','reference_date':'2026-05-07','published_date':'2026-10-15','fields':['ward26cd','ward26nm','reference_lad26cd','reference_lad26nm'],'note':'Best-fit ward reference labels aid recognition and search. Ward and LSOA boundaries need not coincide. These links do not replace analytical geography or reallocate transactions.','areas':lookup}
(P/'data/place-names.json').write_text(json.dumps(record,ensure_ascii=False,separators=(',',':')))
print('Saved named ward references for all',len(m['areas']),'English LSOAs.',flush=True)
