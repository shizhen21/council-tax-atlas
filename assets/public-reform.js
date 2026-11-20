'use strict';
function initPublicReform(){
 const p=new URLSearchParams(location.search),area=p.get('area'),lsoa=p.get('lsoa'),band=p.get('band');const queryYear=+p.get('year');if(queryYear>=2022&&queryYear<=2025)$('reformQueryYear').value=queryYear;
 if(area&&M.lads[area]){explorerLad=area;$('explorerLad').value=area;explorerNeighbourhoods();}
 if(lsoa){const i=M.areas.findIndex(a=>a.code===lsoa);if(i>=0){explorerLad=M.areas[i].lad||'';$('explorerLad').value=explorerLad;$('explorerLevel').value='lsoa';explorerNeighbourhoods();explorerLsoa=String(i);$('explorerLsoa').value=i;}}
 if(band&&BANDS.includes(band))$('reformQueryBand').value=band;
 renderLocalExplorer().then(syncReformArea).catch(showError);
 $('preferencePolicy').innerHTML=POLICIES.map((x,i)=>'<option value="'+(i+1)+'">'+(i+1)+'. '+esc(x)+'</option>').join('');$('preferencePolicy').value='6';
 try{const saved=JSON.parse(localStorage.getItem('councilAtlasPreference')||'null');if(saved&&[1,2,3,4,5,6].includes(+saved.policy)&&['Support','Oppose','Unsure'].includes(saved.view)){$('preferencePolicy').value=saved.policy;$('preferenceView').value=saved.view;$('preferenceStatus').textContent='Saved on this device: Option '+saved.policy+' · '+saved.view+'.';}}catch(e){}
 function preference(){return{policy:+$('preferencePolicy').value,view:$('preferenceView').value,localAuthority:$('preferenceArea').checked?explorerLad||(explorerLsoa!==''?M.areas[+explorerLsoa]?.lad:null)||null:null,savedAt:new Date().toISOString(),submitted:false};}
 $('preferenceForm').onsubmit=e=>{e.preventDefault();const v=preference();if(!v.view){$('preferenceStatus').textContent='Choose Support, Oppose or Unsure first.';return;}try{localStorage.setItem('councilAtlasPreference',JSON.stringify(v));$('preferenceStatus').textContent='Saved on this device: Option '+v.policy+' · '+v.view+(v.localAuthority?' · '+M.lads[v.localAuthority].name:'')+'. This has not been submitted.';}catch(e){$('preferenceStatus').textContent='This browser could not save the preference. You can download it instead.';}};
 $('downloadPreference').onclick=()=>{const v=preference();if(!v.view){$('preferenceStatus').textContent='Choose a response before downloading.';return;}const url=URL.createObjectURL(new Blob([JSON.stringify(v,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='council-tax-reform-preference.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
}
if(document.documentElement.dataset.atlasReady==='true')initPublicReform();else document.addEventListener('atlas-ready',initPublicReform,{once:true});
