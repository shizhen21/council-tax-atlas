/* Renders saved aggregate exports only. No model estimation or new policy rules. */
'use strict';
const ResearchCharts = (() => {
  const colours = ['#247b78','#c87543','#756895','#537da0','#ad6c79','#7d893d','#94784f','#344c61'];
  let data;
  const el = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const nfmt = n => Number(n).toLocaleString('en-GB');
  const asset = path => (window.COUNCIL_RESEARCH_ASSETS || {})[path] || path;
  const group = key => data.groups.find(g => g.key === key);
  const stat = (value,label,note='') => `<div class="result-stat"><b>${esc(value)}</b><span>${esc(label)}</span>${note?`<small>${esc(note)}</small>`:''}</div>`;
  const legend = (id,series) => { el(id).innerHTML = series.map((s,i)=>`<span><i style="background:${s.colour||colours[i%colours.length]}"></i>${esc(s.label)}</span>`).join(''); };
  function chart(id,series,{ylabel='',height=310,format=v=>v.toFixed(1),year=null,zero=false}={}) {
    const width=960,margin={l:66,r:25,t:30,b:47},w=width-margin.l-margin.r,h=height-margin.t-margin.b;
    const finite=series.flatMap(s=>s.points).filter(p=>Number.isFinite(p[0])&&Number.isFinite(p[1]));
    if (!finite.length) {el(id).textContent='No saved observations available.';return;}
    let xmin=Math.min(...finite.map(p=>p[0])),xmax=Math.max(...finite.map(p=>p[0]));
    let vals=series.flatMap(s=>s.points.flatMap(p=>s.ci?[p[2],p[3]]:[p[1]])).filter(Number.isFinite);
    let ymin=Math.min(...vals),ymax=Math.max(...vals);
    if(zero){ymin=Math.min(ymin,0);ymax=Math.max(ymax,0);}
    const pad=(ymax-ymin||1)*.09;ymin-=pad;ymax+=pad;
    const x=v=>margin.l+(v-xmin)/(xmax-xmin||1)*w,y=v=>margin.t+h-(v-ymin)/(ymax-ymin||1)*h;
    let svg=`<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg"><title>${esc(ylabel)}</title><text x="${margin.l}" y="15" font-size="12">${esc(ylabel)}</text>`;
    for(let i=0;i<=4;i++){const v=ymin+(ymax-ymin)*i/4,yp=y(v);svg+=`<line x1="${margin.l}" x2="${width-margin.r}" y1="${yp}" y2="${yp}" stroke="#dce2e2"/><text x="${margin.l-10}" y="${yp+4}" text-anchor="end" font-size="12">${esc(format(v))}</text>`;}
    const ticks=xmax-xmin<6?[Math.ceil(xmin),Math.floor(xmax)]:[Math.ceil(xmin),...Array.from({length:7},(_,i)=>1995+i*5).filter(v=>v>xmin&&v<xmax),Math.floor(xmax)];
    [...new Set(ticks)].forEach(v=>{svg+=`<text x="${x(v)}" y="${height-16}" text-anchor="middle" font-size="12">${v}</text>`;});
    if(zero&&ymin<0&&ymax>0)svg+=`<line x1="${margin.l}" x2="${width-margin.r}" y1="${y(0)}" y2="${y(0)}" stroke="#a9b8b8" stroke-dasharray="4 4"/>`;
    series.forEach((s,i)=>{
      const c=s.colour||colours[i%colours.length],p=s.points;
      if(s.ci){const lower=p.map(r=>`${x(r[0]).toFixed(2)},${y(r[2]).toFixed(2)}`),upper=p.slice().reverse().map(r=>`${x(r[0]).toFixed(2)},${y(r[3]).toFixed(2)}`);svg+=`<polygon points="${[...lower,...upper].join(' ')}" fill="${c}" opacity=".13"/>`;}
      svg+=`<polyline fill="none" stroke="${c}" stroke-width="2.4" ${i>0?'stroke-dasharray="'+(i%2?'7 3':'2 3')+'"':''} points="${p.map(r=>`${x(r[0]).toFixed(2)},${y(r[1]).toFixed(2)}`).join(' ')}"/>`;
      if(p.length<=31)p.forEach(r=>{svg+=`<circle cx="${x(r[0])}" cy="${y(r[1])}" r="2.5" fill="${c}"><title>${esc(s.label)} · ${r[0]}: ${esc(format(r[1]))}</title></circle>`;});
    });
    if(year!==null&&year>=xmin&&year<=xmax)svg+=`<line x1="${x(year)}" x2="${x(year)}" y1="${margin.t}" y2="${margin.t+h}" stroke="#61727c" stroke-dasharray="3 4"/>`;
    el(id).innerHTML=svg+'</svg>';
  }
  function distributions(){
    const year=+el('distributionYear').value;
    el('actualDistribution').src=asset(`assets/research/distribution_${year}_actual.png`);
    el('impliedDistribution').src=asset(`assets/research/distribution_${year}_implied.png`);
    el('actualHeading').textContent=(year===1991?'Reconstructed 1991 values':'Observed transaction-price distribution')+' · '+year;
    el('impliedHeading').textContent='Distribution implied by charges · '+year;
    el('actualDistribution').alt=year===1991?'Reconstructed distribution of 1991 values from April-1993 band-stock counts':`Stock-weighted distribution of ${year} transaction values relative to the Band D median`;
    el('impliedDistribution').alt=`Distribution implied by charging proportions using the ${year===1991?'April-1993':year} stock weights`;
    el('actualCaption').textContent=year===1991?'A reconstruction from April-1993 dwelling-stock band counts.':'Actual prices, relative to the same-year Band D median.';
    const row=data.distribution_summary.find(r=>r.year===year);
    el('distributionFacts').innerHTML=row?stat(row.H_A_ratio.toFixed(2)+'×','Median H/A transaction-price ratio')+stat('3×','Statutory H/A charge ratio')+stat(row.sd_log_actual.toFixed(3)+' / '+row.sd_log_implied.toFixed(3),'Actual / implied log-value dispersion')+stat(nfmt(row.n),'Retained transactions in this figure'):stat('1991','Valuation base')+stat('April 1993','Dwelling-stock band-count reference')+stat('3×','Statutory H/A charge ratio');
  }
  function r2(){
    const mode=el('r2Comparison').value,year=+el('r2Year').value;el('r2YearLabel').textContent=year;
    let series;
    if(mode==='national'){
      series=[{label:group('National').label,points:data.r2.National}];
      el('r2Note').textContent='England-wide annual band-only R², 1995–2025. Each year uses the full England sample, with no geographic subgroups.';
    }else if(mode==='composition'){
      series=[{label:'Observed England',points:data.r2.National},...Object.entries(data.fixed_region).filter(([k])=>!k.toLowerCase().includes('observed')).map(([k,v])=>({label:k,points:v}))];
      el('r2Note').textContent='Fixed regional weights isolate changes in within- and between-region price distributions from changes in the regional composition of transactions. This is a descriptive composition check.';
    }else{
      const keys=mode==='urban'?['National','Urban','Rural']:mode==='regional'?['National','London','Non_London']:['National','EPC_Original','Cross_Period'];
      series=keys.map(key=>({label:group(key).label,points:data.r2[key]}));
      el('r2Note').textContent=mode==='urban'?'Urban and rural status is fixed using the official 2021 LSOA classification. The two samples together account for all 22,680,611 main-model transactions.':mode==='regional'?'London and the rest of England partition the main sample. These are separate within-sample band-only regressions.':'The EPC common sample starts in 2013. Repeat sales form a restricted-sample hedonic check, not a first-difference estimator. Sample composition differs across these series.';
    }
    chart('r2Chart',series,{ylabel:'Band-only R² (%)',year,format:v=>v.toFixed(1)});legend('r2Legend',series);
    el('r2Snapshot').innerHTML=series.map(s=>{const r=s.points.find(r=>r[0]===year);return stat(r?r[1].toFixed(2)+'%':'—',s.label,r?'Year '+year:'No observations in '+year);}).join('');
  }
  function gaps(){
    const key=el('gapSample').value,contrast=el('gapContrast').value;
    const points=data.gaps[key][contrast],series=[{label:group(key).label,points,ci:true}];
    el('gapEngland').disabled=key==='National';
    if(el('gapEngland').checked&&key!=='National')series.push({label:'England',points:data.gaps.National[contrast],ci:true});
    chart('gapChart',series,{ylabel:contrast+' conditional log-price gap',format:v=>v.toFixed(2),zero:true});legend('gapLegend',series);
    const a=points[0],b=points[points.length-1];
    el('gapFacts').innerHTML=stat(a[1].toFixed(3),'Mid-'+Math.floor(a[0])+' · '+contrast+' gap')+stat(b[1].toFixed(3),'Mid-'+Math.floor(b[0])+' · '+contrast+' gap')+stat((100*Math.expm1(b[1])).toFixed(1)+'%','Implied conditional price difference in mid-2025')+stat('['+b[2].toFixed(3)+', '+b[3].toFixed(3)+']','Mid-2025 pointwise 95% interval · log points');
  }
  function context(){
    const key=el('contextSample').value,indices=data.indices[key].Without_Band;
    const name=Object.keys(indices)[0],points=indices[name];
    chart('indexChart',[{label:group(key).label,points,ci:true}],{height:300,ylabel:'Fitted time index',format:v=>v.toFixed(1)});
    el('indexNote').textContent=`${group(key).label}: without-band model time component; mid-${Math.floor(points[0][0])} = 1. Shading is the pointwise 95% interval. This is not the growth of the unadjusted mean transaction price.`;
    const series=Object.entries(data.dispersion[key]).sort(([a],[b])=>a.localeCompare(b)).map(([band,points])=>({label:'Band '+band,points}));
    chart('dispersionChart',series,{height:300,ylabel:'Residual standard deviation · log points',format:v=>v.toFixed(2)});legend('dispersionLegend',series);
  }
  function tax(){
    const annual=Object.values(data.annual_tax).filter(r=>r.year>=2021).sort((a,b)=>a.year-b.year);
    chart('recentEtrChart',[{label:'Mean observed ETR',points:annual.map(r=>[r.year,r.mean_etr_pct])}],{height:280,ylabel:'Mean ETR (%)',format:v=>v.toFixed(2)});
    el('recentEtrTable').innerHTML='<table class="research-table tiny"><thead><tr><th>Year</th><th>Transactions</th><th>Mean ETR (%)</th></tr></thead><tbody>'+annual.map(r=>`<tr><th>${r.year}</th><td>${nfmt(r.n)}</td><td>${r.mean_etr_pct.toFixed(3)}</td></tr>`).join('')+'</tbody></table>';
    const policies=['4','5','6'].map(k=>data.policies_2025[k]);
    const reduction=r=>100*(1-r.reform_within_suits/r.current_within_suits);
    el('policyFacts').innerHTML=policies.map(r=>stat(reduction(r).toFixed(1)+'%',r.policy===4?'Within-LAD regressivity removed · rebanding':r.policy===5?'Within-LAD regressivity removed · multipliers':'Within-LAD regressivity removed · combined')).join('');
    el('policySummaryTable').innerHTML='<table class="research-table tiny"><thead><tr><th>2025 scenario</th><th>National Suits</th><th>Within LAD</th><th>Pay less</th></tr></thead><tbody>'+policies.map(r=>`<tr><th>${esc(r.policy===4?'Rebanding':r.policy===5?'Multipliers':'Combined')}</th><td>${r.reform_national_suits.toFixed(4)}</td><td>${r.reform_within_suits.toFixed(4)}</td><td>${(100*r.share_paying_less).toFixed(2)}%</td></tr>`).join('')+'</tbody></table>';
  }
  function downloads(){
    const files=[['Figures6_9_Table7_Annual_Band_Only_R2.csv.gz','Annual band-only R²'],['Figure7_Table8_Band_Price_Gaps_With_CI.csv.gz','Conditional gaps with intervals'],['Figure8_Annual_Band_Residual_Dispersion.csv.gz','Residual dispersion'],['Continuous_Price_Index_Without_Band.csv.gz','Without-band price index'],['Continuous_Price_Index_With_Band.csv.gz','With-band price indices'],['PARAMETRIC_COEFFICIENTS_With_Band.csv.gz','With-band coefficients'],['PARAMETRIC_COEFFICIENTS_Without_Band.csv.gz','Without-band coefficients'],['SMOOTH_EDF_With_Band.csv.gz','With-band effective degrees of freedom'],['SMOOTH_EDF_Without_Band.csv.gz','Without-band effective degrees of freedom'],['Annual_Spatial_Effects_With_Band.csv.gz','With-band spatial effects'],['Annual_Spatial_Effects_Without_Band.csv.gz','Without-band spatial effects']];
    el('modelDownloads').innerHTML=data.download_groups.map(g=>`<div><h4>${esc(g.label)}</h4>${files.map(([file,title])=>`<a href="downloads/research/${g.key}/${file}">${esc(title)} ↓</a>`).join('')}</div>`).join('');
  }
  async function start(){
    try{
      if(window.COUNCIL_RESEARCH_PREVIEW)data=window.COUNCIL_RESEARCH_PREVIEW;
      else{const response=await fetch('data/research.json?v=20261113-2');if(!response.ok)throw new Error('Result data could not be loaded');data=await response.json();}
      el('gapSample').innerHTML=data.groups.map(g=>`<option value="${g.key}" ${g.key==='Urban'?'selected':''}>${esc(g.label)}</option>`).join('');
      el('gapContrast').innerHTML=Object.keys(data.gaps.National).map(k=>`<option ${k==='H–G'?'selected':''}>${esc(k)}</option>`).join('');
      el('contextSample').innerHTML=data.groups.filter(g=>data.indices[g.key]).map(g=>`<option value="${g.key}">${esc(g.label)}</option>`).join('');
      for(const [id,fn] of [['distributionYear',distributions],['r2Comparison',r2],['gapSample',gaps],['gapContrast',gaps],['gapEngland',gaps],['contextSample',context]])el(id).addEventListener('change',fn);
      el('r2Year').addEventListener('input',r2);
      distributions();r2();gaps();context();downloads();
      el('dataStatus').textContent='Current saved results loaded · eight groups, sixteen model specifications · tax and reform reconciliation passed.';
      document.documentElement.dataset.researchReady='true';
      window.CouncilResearch={chart,data};
    }catch(error){el('dataStatus').textContent='Interactive data could not load. Please serve the full website over HTTP, or open the standalone preview. Tables and downloads below remain available.';el('dataStatus').classList.add('research-error');console.error(error);document.documentElement.dataset.researchError=String(error);}
  }
  start();
  return {chart};
})();

if(location.hash){const t=document.getElementById(location.hash.slice(1));if(t){let e=t;while(e){if(e.tagName==='DETAILS')e.open=true;e=e.parentElement;}}}
