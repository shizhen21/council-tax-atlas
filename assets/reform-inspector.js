let reformQueryArea=null,reformQueryToken=0;
async function renderReformBandQuery(){
 const token=++reformQueryToken,yy=+$('reformQueryYear').value,k=+$('reformQueryPolicy').value,band=$('reformQueryBand').value,a=reformQueryArea,code=a?.code||'England',name=a?(a.type==='lad'?M.lads[a.code].name:M.areas[a.index].name):'England';
 setText('reformQueryTitle',name+' · '+yy+' · Option '+k);setText('reformBandAnswer','Loading band-level results…');
 const all=await get('reform-bands/'+yy+'_'+k+'/'+(a?.type==='lsoa'?a.index%64:'lad')+'.json');if(token!==reformQueryToken)return;const rows=all[code]||{},v=rows[band];
 if(v){const db=v[2]-v[1],de=v[4]-v[3];$('reformBandAnswer').innerHTML='<p class="eyebrow">'+esc(name)+' · ORIGINALLY BAND '+band+'</p><h3>'+gbp(v[2],2)+' <small>average annual bill after reform</small></h3><div class="band-answer-grid"><div><span>Bill change</span><strong>'+gbp(db,2)+'</strong><small>'+(Math.abs(db)<.005?'No change in the group mean':db<0?'Less per year on average':'More per year on average')+'</small></div><div><span>Mean effective rate after reform</span><strong>'+fmt(v[4],3)+'%</strong><small>'+signed(de,3)+' percentage points</small></div><div><span>Pay less / pay more</span><strong>'+fmt(v[6]*100,1)+'% / '+fmt(v[5]*100,1)+'%</strong><small>Within the selected original band</small></div></div><p class="note">Before reform: '+gbp(v[1],2)+' per year; mean effective rate '+fmt(v[3],3)+'%. These are group averages for observed transactions, not an individual bill quote.</p>';}
 else $('reformBandAnswer').innerHTML='<p class="eyebrow">'+esc(name)+' · ORIGINALLY BAND '+band+'</p><p>No observed transactions in this original band for the chosen area and year. A missing group is not a zero tax bill.</p>';
 $('reformBandTable').innerHTML='<thead><tr><th>Original band</th><th>Bill before (£)</th><th>Bill after (£)</th><th>Bill change (£)</th><th>ETR before (%)</th><th>ETR after (%)</th><th>ETR change (pp)</th><th>Pay less (%)</th><th>Pay more (%)</th></tr></thead><tbody>'+BANDS.map(b=>{const r=rows[b];return '<tr'+(b===band?' class="selected-band"':'')+'><th scope="row">'+b+'</th>'+(r?'<td>'+fmt(r[1],2)+'</td><td>'+fmt(r[2],2)+'</td><td>'+signed(r[2]-r[1],2)+'</td><td>'+fmt(r[3],3)+'</td><td>'+fmt(r[4],3)+'</td><td>'+signed(r[4]-r[3],3)+'</td><td>'+fmt(r[6]*100,1)+'</td><td>'+fmt(r[5]*100,1)+'</td>':'<td colspan="8">No observations</td>')+'</tr>';}).join('')+'</tbody>';
 setText('reformBandSample',BANDS.map(b=>'Band '+b+': '+fmt(rows[b]?.[0]||0)).join(' · '));setText('reformBandQueryNote',(a?.type==='lsoa'?'Ward names are ONS 2026 best-fit reference labels; boundaries can differ from the LSOA. ':'')+'Option '+k+' · '+POLICIES[k-1]+'. Groups use ORIGINAL A–H bands before reform. In Options 4 and 6, properties in the same original band can enter different new bands and face different bills. Effective rates average each annual bill divided by its observed sale price; they are not computed from an average property price. Paying more/less uses the saved £0.01 tolerance.');
}
/* The reform query shares the area chosen in the local-tax tools above. */
function syncReformArea(){
 const index=explorerLsoa===''?null:+explorerLsoa;
 reformQueryArea=index!==null?{type:'lsoa',code:M.areas[index].code,index}:explorerLad?{type:'lad',code:explorerLad}:null;
 if($('parameterArea')){$('parameterArea').value=index!==null?(M.areas[index].lad||''):explorerLad;renderComparison();}
 renderReformBandQuery().catch(showError);
}
function initReformBandQuery(){
 if(!$('reformQueryYear'))return;
 $('reformQueryPolicy').innerHTML=POLICIES.map((n,i)=>'<option value="'+(i+1)+'"'+(i===5?' selected':'')+'>'+(i+1)+'. '+esc(n)+'</option>').join('');
 for(const id of ['reformQueryYear','reformQueryPolicy','reformQueryBand'])$(id).onchange=()=>renderReformBandQuery().catch(showError);
 document.addEventListener('atlas-area-change',syncReformArea);
 $('showReformOnMap').onclick=async()=>{
  try{
   await switchMapView('policy');
   year=+$('reformQueryYear').value;policy=+$('reformQueryPolicy').value;
   populateControls();await updateData();
   if(reformQueryArea)choose(reformQueryArea.type,reformQueryArea.type==='lsoa'?reformQueryArea.index:reformQueryArea.code);
   else choose(null);
   $('explore').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
  }catch(error){showError(error);}
 };
 syncReformArea();
 if(new URLSearchParams(location.search).get('view')==='policy')switchMapView('policy').catch(showError);
}
if(document.documentElement.dataset.atlasReady==='true')initReformBandQuery();else document.addEventListener('atlas-ready',initReformBandQuery,{once:true});
