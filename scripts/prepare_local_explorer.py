from pathlib import Path
import csv,gzip,json
P=Path(__file__).resolve().parents[1];D=P/'data';dl=P/'downloads'
def rows(name):
 with gzip.open(dl/(name+'.csv.gz'),'rt') as f:yield from csv.DictReader(f)
def dump(name,x):
 p=D/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,separators=(',',':'),allow_nan=False))
meta=json.loads((D/'meta.json').read_text());idx={a['code']:i for i,a in enumerate(meta['areas'])};links={r['lsoa21cd']:r['lad26cd'] for r in rows('official_lsoa_lad_unique_links')};history={};bands={};coverage={}
for r in rows('lad_current_fixed2026_1995_2025'):history.setdefault(str(int(float(r['year']))),{})[r['lad26cd']]=[int(float(r['n'])),round(float(r['mean_bill']),2),round(float(r['mean_etr_pct']),5)]
for r in rows('lad_band_counts_1995_2025'):bands.setdefault(str(int(float(r['year']))),{}).setdefault(r['lad26cd'],{})[r['band']]=int(float(r['Freq']))
for r in rows('lad_harmonisation_coverage'):
 yy=str(int(float(r['year'])));coverage[yy]={k:int(float(v)) for k,v in r.items()};assert coverage[yy]['mapped']+coverage[yy]['unresolved']==meta['annual'][yy]['n'];assert sum(x[0] for x in history[yy].values())==coverage[yy]['mapped']
lsoa={}
for r in rows('lsoa_band_counts_1995_2025'):
 yy=str(int(float(r['year'])));i=idx[r['lsoa21cd']];lsoa.setdefault(yy,[None]*len(idx));v=lsoa[yy][i]
 if v is None:v=[0]*8;lsoa[yy][i]=v
 v['ABCDEFGH'.index(r['band'])]=int(float(r['n']))
for yy,values in lsoa.items():
 h=json.loads((D/'history'/f'{yy}.json').read_text());assert all(sum(values[i])==v[0] for i,v in enumerate(h) if v);dump(f'bands/{yy}.json',values)
dump('local.json',{'links':links,'history':history,'bands':bands,'coverage':coverage,'lad_basis':'Fixed LAD2026 from unique LSOA2021 links in the retained August-2026 postcode lookup; ambiguous areas are excluded from local summaries and retained in national totals.'})
f=P/'DATA_VALIDATION.json';report=json.loads(f.read_text());report.update(local_explorer_years=31,local_band_share_years=31,lsoa_band_share_years=31,unique_official_lsoa_lad_links=len(links),lad_harmonisation_2025=coverage['2025'],local_coverage_reconciles=True);f.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
