"""Prepare static aggregate data and display geometry without Git/Node or dependencies."""
from pathlib import Path
import csv,gzip,json,struct,math,collections,hashlib
ROOT=Path(__file__).resolve().parents[3]; SITE=Path(__file__).resolve().parents[1];DATA=SITE/'data';DL=SITE/'downloads';ETR=ROOT/'ETR_1021';POL=ETR/'08_Policy_Simulation/results/Six_Policies_2022_2025_Upper_ETR';CH=ETR/'04_Samples_Descriptions/results/Chapter_Data_Updated/CSV'
def dump(name,obj):
 p=DATA/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,separators=(',',':'),ensure_ascii=False,allow_nan=False))
def rows(p):
 with (gzip.open(p,'rt',encoding='utf-8-sig') if str(p).endswith('.gz') else open(p,encoding='utf-8-sig')) as f:yield from csv.DictReader(f)
def num(v):
 try:
  x=float(str(v).replace(',',''));return x if math.isfinite(x) else None
 except (TypeError,ValueError):return None
def norm(r):return {k:(num(v) if num(v) is not None else (None if v in ('NA','','NaN') else v)) for k,v in r.items()}
def roundn(x,n=4):return round(float(x),n)
# Parse the published DBF and shapefile using their documented binary layouts.
shbase=ETR/'08_Policy_Simulation/data/Reference/LSOA2021_Boundaries/LSOA_2021_EW_BGC_V5'
with open(str(shbase)+'.dbf','rb') as f:
 h=f.read(32);n,hs,rs=struct.unpack_from('<IHH',h,4);fields=[]
 while f.tell()<hs-1:
  d=f.read(32)
  if d[0]==13:break
  fields.append((d[:11].split(b'\0')[0].decode(),d[16]))
 f.seek(hs);attrs=[]
 for i in range(n):
  b=f.read(rs);o=1;r={}
  for name,size in fields:r[name]=b[o:o+size].decode('utf-8',errors='replace').strip();o+=size
  attrs.append(r)
meta=[];shapes=[];bounds=[float('inf'),float('inf'),-float('inf'),-float('inf')]
def simplify(pts,tol=50):
 if len(pts)<6:return pts
 # Closed rings are split at a distant point before Douglas-Peucker.
 def dp(a):
  keep={0,len(a)-1};stack=[(0,len(a)-1)]
  while stack:
   lo,hi=stack.pop();x,y=a[lo];ex,ey=a[hi];dx,dy=ex-x,ey-y;den=dx*dx+dy*dy;best=tol*tol;idx=None
   for k in range(lo+1,hi):
    px,py=a[k];t=max(0,min(1,((px-x)*dx+(py-y)*dy)/den)) if den else 0;dd=(px-x-t*dx)**2+(py-y-t*dy)**2
    if dd>best:best=dd;idx=k
   if idx is not None:keep.add(idx);stack.extend([(lo,idx),(idx,hi)])
  return [a[k] for k in sorted(keep)]
 mid=max(range(1,len(pts)-1),key=lambda k:(pts[k][0]-pts[0][0])**2+(pts[k][1]-pts[0][1])**2)
 result=dp(pts[:mid+1])+dp(pts[mid:])[1:]
 return result if len(result)>=4 else pts
with open(str(shbase)+'.shp','rb') as f:
 f.read(100)
 while True:
  h=f.read(8)
  if not h:break
  recno,length=struct.unpack('>ii',h);b=f.read(length*2);a=attrs[recno-1]
  if not a['LSOA21CD'].startswith('E'):continue
  typ=struct.unpack_from('<i',b)[0];assert typ in (5,15),typ
  nparts,npts=struct.unpack_from('<ii',b,36);parts=list(struct.unpack_from('<'+'i'*nparts,b,44))+[npts];off=44+4*nparts;points=list(struct.iter_unpack('<dd',b[off:off+npts*16]));rings=[simplify(points[parts[j]:parts[j+1]]) for j in range(nparts)]
  bx=struct.unpack_from('<dddd',b,4);meta.append({'code':a['LSOA21CD'],'name':a['LSOA21NM'],'cx':float(a['BNG_E']),'cy':float(a['BNG_N']),'b':list(bx)});shapes.append(rings)
  bounds=[min(bounds[0],bx[0]),min(bounds[1],bx[1]),max(bounds[2],bx[2]),max(bounds[3],bx[3])]
assert len(meta)==33755
xmin,ymin,xmax,ymax=bounds
project=lambda x,y:[round((x-xmin)/1000,2),round((ymax-y)/1000,2)]
def svg(rings):return ''.join('M'+'L'.join(f'{x},{y}' for x,y in (project(x,y) for x,y in ring))+'Z' for ring in rings)
for a in meta:
 a['cx'],a['cy']=project(a['cx'],a['cy']);a['b']=[*project(a['b'][0],a['b'][3]),*project(a['b'][2],a['b'][1])]
dump('geometry.json',{'size':[(xmax-xmin)/1000,(ymax-ymin)/1000],'paths':[svg(r) for r in shapes]});del shapes
idx={a['code']:i for i,a in enumerate(meta)}
links=collections.defaultdict(set)
for r in rows(DL/'lsoa_lad_links.csv.gz'):links[r['lsoa21cd']].add(r['lad26cd'])
for a in meta:a['lad']=next(iter(links[a['code']])) if len(links[a['code']])==1 else None
geo=json.loads((ETR/'08_Policy_Simulation/data/Reference/LAD2025_Official.geojson').read_text());lads={}
for f in geo['features']:
 a=f['properties'];code=a['LAD25CD']
 if not code.startswith('E'):continue
 g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']];rings=[simplify(r,100) for poly in polys for r in poly];flat=[p for ring in rings for p in ring];xs=[x for x,y in flat];ys=[y for x,y in flat]
 lads[code]={'name':a['LAD25NM'],'path':svg(rings),'b':[*project(min(xs),max(ys)),*project(max(xs),min(ys))]}
assert len(lads)==296
print('Prepared geometry: 33,755 LSOAs and 296 LADs',flush=True)
annual={str(int(float(r['year']))):norm(r) for r in rows(ETR/'07_Current_ETR_Suits/results/ETR_Upper_Trim_0.5pct/Annual_ETR_And_Suits.csv')}
checks=[];hist={};series=[{} for _ in range(64)]
for r in rows(DL/'lsoa_current_1995_2025.csv.gz'):
 year=str(int(float(r['year'])));i=idx[r['lsoa21cd']];v=[int(float(r['n'])),roundn(r['mean_bill'],2),roundn(r['mean_etr_pct'],5)];hist.setdefault(year,[None]*len(meta))[i]=v;series[i%64].setdefault(str(i),[None]*31)[int(year)-1995]=v
for year,values in hist.items():
 assert sum(r[0] for r in values if r)==int(annual[year]['n']);dump('history/'+year+'.json',values)
for i,bucket in enumerate(series):dump(f'series/{i}.json',bucket)
# Independently compare four existing manuscript map exports.
for r in rows(ETR/'07_Current_ETR_Suits/results/ETR_Upper_Trim_0.5pct/Four_Year_LSOA_Maps/LSOA_Four_Years_ETR.csv'):
 v=hist[str(int(float(r['year'])))][idx[r['lsoa21cd']]];assert v[0]==int(r['n']);assert abs(v[2]-float(r['mean_ETR_pct']))<.000006
poldata={};ladpolicy={};max_discrepancy=0
for r in rows(DL/'lsoa_policy_2022_2025.csv.gz'):
 y=str(int(float(r['year'])));k=str(int(float(r['policy'])));i=idx[r['code']];h=hist[y][i];assert h[0]==int(float(r['n']));assert abs(h[1]-float(r['mean_bill_before']))<.006;assert abs(h[2]-float(r['mean_etr_before']))<.000006
 poldata.setdefault(y+'_'+k,[None]*len(meta))[i]=[roundn(float(r['mean_bill_after'])-float(r['mean_bill_before']),2),roundn(float(r['mean_etr_after'])-float(r['mean_etr_before']),5),roundn(r['share_less'],5),roundn(r['share_more'],5)]
for key,values in poldata.items():dump('policy/'+key+'.json',values)
for r in rows(DL/'lad_policy_2022_2025.csv.gz'):ladpolicy.setdefault(str(int(float(r['year'])))+'_'+str(int(float(r['policy']))),{})[r['code']]=norm(r)
summary={};suits={};multipliers={};thresholds={}
for yy in range(2022,2026):
 folder=POL/f'year_{yy}';summary[str(yy)]={str(int(r['policy'])):norm(r) for r in rows(folder/f'six_policies_core_summary_{yy}.csv')}
 for r in rows(folder/f'six_policies_LAD_Suits_{yy}.csv'):
  key=f'{yy}_{r["policy"]}';suits.setdefault(key,{})[r['lad26cd']]=norm(r)
 for variant,name,bfield in [('5','original_band_prices_and_multipliers.csv','band_original'),('6','new_band_prices_and_multipliers.csv','band_new')]:
  for r in rows(folder/name):multipliers.setdefault(f'{yy}_{variant}',{}).setdefault(r['lad26cd'],{})[r[bfield]]=num(r['multiplier_median'])
 for r in rows(folder/'reband_thresholds.csv'):thresholds.setdefault(str(yy),{}).setdefault(r['lad26cd'],{})[r['band']]=num(r['upper_price'])
# Validate own aggregate differences against the saved policy-map exports.
for r in rows(POL/'LSOA2021_Policy_Annual.csv'):
 y=str(int(r['year']));v=poldata[y+'_'+r['policy']][idx[r['lsoa21cd']]];assert abs(v[0]-float(r['mean_bill_change']))<.006;assert abs(v[1]-float(r['mean_ETR_change_pp']))<.000006
bandD={};bandDNames={}
for r in rows(ETR/'03_Annual_Charges/data/raw/LAD_bandD.csv'):
 code=r['ONS Code '].strip();code='England' if r['Authority']=='England' else code
 if code in lads or code=='England':bandD[code]={str(y):num(r.get(f'{y} to {y+1}')) for y in range(1995,2026)};bandDNames[code]=r['Authority']
stock={};stocknat={r['band']:num(r['official_share_pct']) for r in rows(CH/'Table4_National_Stock_Comparison_2026.csv')}
for r in rows(CH/'Table5_LAD_Band_Validation_Input.csv'):stock.setdefault(r['lad_code'],{})[r['band']]=num(r['share_official'])
trade={}
for r in rows(DL/'selected_transaction_band_shares.csv.gz'):trade.setdefault(str(int(float(r['year']))),{})[r['band']]=int(float(r['Freq']))
localbands={}
for r in rows(DL/'lad_band_counts.csv.gz'):localbands.setdefault(str(int(float(r['year'])))+'_'+r['type'],{}).setdefault(r['lad26cd'],{})[r['band']]=int(float(r['Freq']))
transitions={}
for r in rows(DL/'reband_transitions.csv.gz'):transitions.setdefault(str(int(float(r['year']))),[]).append([r['original'],r['new'],int(float(r['Freq']))])
coverage=[norm(r) for r in rows(CH/'Figure3_England_Annual_Match_Rates.csv')]
neighbour=[norm(r) for r in rows(POL/'Neighbourhood_Policy_Annual.csv')]
# Common map classes across years/policies, in displayed original units.
import numpy as np
quant=lambda vals:np.quantile(vals,np.arange(.1,1,.1)).round(5).tolist()
classes={'etr':quant([v[2] for vs in hist.values() for v in vs if v]),'bill':quant([v[1] for vs in hist.values() for v in vs if v]),'n':quant([v[0] for vs in hist.values() for v in vs if v])}
# A single policy-change scale is held constant across all policies and years.
classes['deltaBill']=500;classes['deltaEtr']=.4
meta_payload={'areas':meta,'lads':lads,'annual':annual,'summary':summary,'ladPolicy':ladpolicy,'suits':suits,'multipliers':multipliers,'thresholds':thresholds,'bandD':bandD,'bandDNames':bandDNames,'stock':stock,'stockNational':stocknat,'trade':trade,'localBands':localbands,'coverage':coverage,'transitions':transitions,'neighbourhood':neighbour,'classes':classes,'schema':{'history':['n','mean_bill_gbp','mean_etr_pct'],'policy':['mean_bill_change_gbp','mean_etr_change_pp','share_less','share_more']},'release':'29 October 2026','geometry_note':'LSOA2021; display geometry simplified at 50 metres. LAD2025 reference polygons match all 296 LAD2026 simulation codes; code coverage verified, boundary equivalence not asserted.'}
dump('meta.json',meta_payload)
manifest={'history_years':31,'policy_years':4,'policies':6,'lsoa_geometries':len(meta),'lad_geometries':len(lads),'history_n_matches_saved_annual':True,'history_matches_existing_four_year_maps':True,'policy_means_match_saved_map_exports':True,'lsoa_lad_multiple_or_unobserved':sum(not a['lad'] for a in meta),'raw_identifiers_exported':False,'geometry_simplification_metres':50,'data_files':len(list(DATA.rglob('*.json')))}
(SITE/'DATA_VALIDATION.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest),flush=True)
