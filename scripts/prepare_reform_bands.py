from pathlib import Path
import csv,gzip,json,math
P=Path(__file__).resolve().parents[1]
meta=json.loads((P/'data/meta.json').read_text());index={a['code']:i for i,a in enumerate(meta['areas'])}
report={}
for year in range(2022,2026):
 groups={k:{'lad':{},**{str(i):{} for i in range(64)}} for k in range(1,7)}
 totals={}
 with gzip.open(P/f'downloads/reform_original_band_{year}.csv.gz','rt') as f:
  for row in csv.DictReader(f):
   k=int(row['policy']);level=row['level'];code=row['code'];band=row['band'];n=int(float(row['n']))
   v=[n]+[round(float(row[col]),6) for col in ['bill_before','bill_after','etr_before','etr_after','share_more','share_less']]
   assert all(math.isfinite(x) for x in v) and v[5]+v[6]<=1.000002
   bucket='lad' if level in ('lad','england') else str(index[code]%64)
   groups[k][bucket].setdefault(code,{})[band]=v
   totals[(k,level)]=totals.get((k,level),0)+n
 for (k,level),total in totals.items():assert total==meta['summary'][str(year)][str(k)]['n'],(year,k,level,total)
 for k,buckets in groups.items():
  out=P/f'data/reform-bands/{year}_{k}';out.mkdir(parents=True,exist_ok=True)
  for bucket,data in buckets.items():(out/f'{bucket}.json').write_text(json.dumps(data,separators=(',',':')))
 report[str(year)]={'policies':6,'geographies':['England','LAD','LSOA'],'all_band_counts_reconcile':True}
 print(f'Prepared original-band query files: {year}',flush=True)
(P/'REFORM_BAND_VALIDATION.json').write_text(json.dumps(report,indent=2))
