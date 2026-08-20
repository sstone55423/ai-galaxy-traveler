import json, os, build_catalog as bc
rows = bc.build()
stars = [{"x": round(r["x"],2), "y": round(r["y"],2), "z": round(r["z"],2),
          "c": r["category"]} for r in rows]

HTML = r'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Galaxy Traveler - Engineering Closure Dashboard</title>
<style>
  :root{ --bg0:#05060d; --panel:#0e1226; --line:rgba(120,150,220,.18); --txt:#dfe6ff;
         --dim:#93a0c8; --accent:#7fb3ff; --gold:#ffd35e; --green:#7af0a8; --red:#ff7a8a; }
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(1200px 800px at 60% -10%,#0b1022,#05060d);
    color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:18px;font-size:14px}
  h1{font-size:18px;margin:0 0 2px} .sub{color:var(--dim);font-size:12px;margin-bottom:14px}
  .wrap{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:15px}
  #controls{width:300px;flex:none}
  #controls h2{font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:var(--dim);margin:14px 0 8px}
  #controls h2:first-child{margin-top:0}
  .fld{margin-bottom:11px}
  .fld label{display:flex;justify-content:space-between;font-size:12px;color:var(--dim);margin-bottom:4px}
  .fld label b{color:var(--txt)}
  input[type=range]{width:100%;accent-color:var(--accent)}
  #right{flex:1;min-width:440px;display:flex;flex-direction:column;gap:14px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  .card h3{margin:0 0 8px;font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim)}
  .big{font-size:30px;font-weight:700;font-variant-numeric:tabular-nums}
  .verdict{display:inline-block;margin-left:8px;font-size:13px;padding:2px 10px;border-radius:20px;vertical-align:middle}
  .row{display:flex;justify-content:space-between;padding:2px 0;color:var(--dim);font-size:12.5px}
  .row b{color:var(--txt);font-variant-numeric:tabular-nums}
  canvas{width:100%;display:block}
  .chartttl{font-size:12px;color:var(--dim);margin:0 0 8px}
  .legend{display:flex;gap:14px;font-size:11px;color:var(--dim);margin-top:6px;flex-wrap:wrap}
  .legend i{display:inline-block;width:11px;height:3px;border-radius:2px;margin-right:5px;vertical-align:middle}
  .note{font-size:11.5px;color:var(--dim);line-height:1.5;margin-top:6px}
</style></head><body>
<h1>Engineering Closure &mdash; explore the knife-edge</h1>
<div class="sub">Four interlocking budgets for the self-replicating wanderer. R_eff is computed live across the real 127-star catalogue.</div>

<div class="wrap">
  <div id="controls" class="panel">
    <h2>Reproduction</h2>
    <div class="fld"><label>Offspring per node <b><span id="offV">3</span></b></label>
      <input type="range" id="off" min="1" max="5" step="1" value="3"></div>
    <div class="fld"><label>Per-leg reliability <b><span id="pV">0.90</span></b></label>
      <input type="range" id="p" min="0.70" max="1.00" step="0.01" value="0.90"></div>
    <div class="fld"><label>Cruise survival / ly <b><span id="crV">0.99</span></b></label>
      <input type="range" id="cr" min="0.95" max="1.00" step="0.005" value="0.99"></div>
    <div class="fld"><label>Ordinary-dwarf viability <b><span id="vdV">0.70</span></b></label>
      <input type="range" id="vd" min="0.30" max="1.00" step="0.05" value="0.70"></div>

    <h2>Braking &amp; seed</h2>
    <div class="fld"><label>Seed mass <b><span id="mV">3,700</span> kg</b></label>
      <input type="range" id="m" min="3" max="7" step="0.05" value="3.568"></div>
    <div class="fld"><label>Magsail radius <b><span id="RV">100</span> km</b></label>
      <input type="range" id="R" min="10" max="200" step="5" value="100"></div>
    <div class="fld"><label>Cruise speed <b><span id="vV">450</span> km/s</b></label>
      <input type="range" id="v" min="50" max="600" step="10" value="450"></div>

    <h2>Power &amp; closure</h2>
    <div class="fld"><label>Reactor rated power (thermal; ~28% to electric) <b><span id="kwV">14</span> kW</b></label>
      <input type="range" id="kw" min="0.6" max="3" step="0.02" value="1.146"></div>
    <div class="fld"><label>ISRU plant mass <b><span id="isruV">2,000</span> kg</b></label>
      <input type="range" id="isru" min="2.3" max="6" step="0.05" value="3.301"></div>
    <div class="fld"><label>Closure ratio <b><span id="clV">0.97</span></b></label>
      <input type="range" id="cl" min="0.50" max="1.00" step="0.01" value="0.97"></div>
  </div>

  <div id="right">
    <div class="panel card">
      <h3>Reproduction &mdash; R_eff across the real catalogue</h3>
      <div><span class="big" id="reff">0.00</span><span class="verdict" id="verdict"></span></div>
      <div class="row">Nodes with R_eff &gt; 1 <b id="frac">0%</b></div>
      <div class="row">Mean per-node extinction probability <b id="ext">0.00</b></div>
      <p class="chartttl" style="margin-top:12px">Knife-edge: mean R_eff vs per-leg reliability</p>
      <canvas id="chart" width="640" height="220"></canvas>
      <div class="legend">
        <span><i style="background:#7af0a8"></i>offspring 4</span>
        <span><i style="background:#7fb3ff"></i>offspring 3</span>
        <span><i style="background:#ffd35e"></i>offspring 2</span>
        <span><i style="background:#ff7a8a"></i>R_eff = 1 (extinction threshold)</span>
        <span><i style="background:#fff"></i>your setting</span>
      </div>
    </div>
    <div class="grid">
      <div class="panel card">
        <h3>Braking (magsail vs ISM)</h3>
        <div class="row">Stopping distance <b id="bd">0 ly</b></div>
        <div class="row">Braking time <b id="bt">0 yr</b></div>
        <div class="row">Peak deceleration <b id="bg">0 g</b></div>
        <div class="row">Sail for 0.01 ly stop <b id="bsail">0 km</b></div>
        <p class="note">Stopping distance d = m/(2&rho;A) is independent of cruise speed; only time scales with it.</p>
      </div>
      <div class="panel card">
        <h3>Seed mass budget</h3>
        <div class="row">Total seed mass <b id="mtot">0 kg</b></div>
        <div class="row">Dominant subsystem <b id="mdom">&mdash;</b></div>
        <div class="row">Radiator area <b id="mrad">0 m&sup2;</b></div>
        <div class="row">Reactor + conversion <b id="mreac">0 kg</b></div>
        <p class="note" id="mnote"></p>
      </div>
      <div class="panel card">
        <h3>Closure</h3>
        <div class="row">Vitamin fraction <b id="cvf">0%</b></div>
        <div class="row">Vitamin mass carried <b id="cvm">0 kg</b></div>
        <div class="row">Material margin <b id="cmm">0&times;</b></div>
        <div class="row">Energy margin <b id="cem">0&times;</b></div>
        <p class="note">Material and energy never bind; capability (closure) does.</p>
      </div>
      <div class="panel card">
        <h3>Verdict</h3>
        <p class="note" id="bigverdict"></p>
      </div>
    </div>
  </div>
</div>

<script>
const STARS = __STARS_JSON__;
const RHO=0.2e6*1.674e-27, C=299792458.0, LY=9.4607e15, YEAR=3.15576e7, SIGMA=5.670374e-8;
const BELT=3.0e21, U=8.2e13;
// precompute nearest-6 neighbours per node (positions fixed)
const NB = STARS.map((s,i)=>{
  const a=[]; for(let j=0;j<STARS.length;j++){ if(j===i)continue; const t=STARS[j];
    a.push({d:Math.hypot(s.x-t.x,s.y-t.y,s.z-t.z),c:t.c}); }
  a.sort((x,y)=>x.d-y.d); return a.slice(0,6);
});
const viab=(c,vd)=> (c==='giant'||c==='white-dwarf')?0.2 : c==='planet-host'?1.0 : vd;
const legSurv=(d,p,cr)=> p*p*p*p*Math.pow(cr,d);
function extinct(sl){ let q=0; for(let k=0;k<400;k++){ let f=1; for(const s of sl) f*=(1-s+s*q);
  if(Math.abs(f-q)<1e-12)break; q=f; } return q; }
function repro(off,p,cr,vd){
  let sum=0,above=0,esum=0,n=STARS.length;
  for(let i=0;i<n;i++){ const sl=[]; for(let k=0;k<off&&k<NB[i].length;k++){ const o=NB[i][k];
      sl.push(legSurv(o.d,p,cr)*viab(o.c,vd)); }
    const r=sl.reduce((a,b)=>a+b,0); sum+=r; if(r>1)above++; esum+=extinct(sl); }
  return {mean:sum/n, frac:above/n, ext:esum/n};
}
function braking(m,Rkm,vkms){ const A=Math.PI*Math.pow(Rkm*1000,2), v=vkms*1000;
  return {d:m/(2*RHO*A)/LY, t:m/(RHO*v*A)/YEAR, g:(RHO*v*v*A/m)/9.80665, A}; }
function sailFor(m,dly){ const A=m/(2*RHO*dly*LY); return Math.sqrt(A/Math.PI)/1000; }
function massBudget(kW,isru){ const reactor=8*kW, fuel=16.5,
  rad=(kW*1000)/(0.9*SIGMA*Math.pow(400,4)), radiators=rad*3, ship=400+300+200;
  const subs={fuel,reactor,radiators,shield:400,sail:300,pay:200,isru};
  let core=fuel+reactor+radiators+400+300+200+isru; const struct=0.2*core;
  const total=core+struct;
  const named={fuel:fuel,'reactor+conversion':reactor,radiators:radiators,shielding:400,
    'magsail structure':300,'computation+payload':200,'ISRU+manufacturing plant':isru,'structure/integration':struct};
  let dom='',dm=0; for(const k in named) if(named[k]>dm){dm=named[k];dom=k;}
  return {total,reactor,radArea:rad,dom}; }
function closure(childKg,kW,cr){ const vf=1-cr; const t=1e4*YEAR;
  return {vf, vk:vf*childKg, mm:BELT/childKg, em:(kW*1000*t)/(5e8*childKg)}; }

// ---- chart (knife-edge) ----
function chart(){
  const cv=document.getElementById('chart'),dpr=Math.min(window.devicePixelRatio||1,2);
  const W=cv.clientWidth||640,H=220; cv.width=W*dpr;cv.height=H*dpr; const x=cv.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0);
  x.clearRect(0,0,W,H);
  const ml=40,mr=12,mt=8,mb=22,pw=W-ml-mr,ph=H-mt-mb;
  const xmin=0.70,xmax=1.0,ymax=3.0;
  const X=p=>ml+pw*(p-xmin)/(xmax-xmin), Y=r=>mt+ph*(1-Math.min(r,ymax)/ymax);
  x.strokeStyle='rgba(120,150,220,.15)';x.fillStyle='#93a0c8';x.font='10px sans-serif';x.lineWidth=1;
  for(let r=0;r<=3;r++){const py=Y(r);x.beginPath();x.moveTo(ml,py);x.lineTo(W-mr,py);x.stroke();x.fillText(r.toFixed(0),6,py+3);}
  for(let p=0.7;p<=1.001;p+=0.1){const px=X(p);x.fillText(p.toFixed(1),px-7,H-7);}
  // R_eff=1 threshold
  x.strokeStyle='rgba(255,122,138,.8)';x.setLineDash([5,4]);x.beginPath();x.moveTo(ml,Y(1));x.lineTo(W-mr,Y(1));x.stroke();x.setLineDash([]);
  const cr=parseFloat(cr_i.value),vd=parseFloat(vd_i.value);
  const cols={2:'#ffd35e',3:'#7fb3ff',4:'#7af0a8'};
  for(const off of [2,3,4]){ x.beginPath(); x.strokeStyle=cols[off]; x.lineWidth=2;
    for(let i=0;i<=60;i++){ const p=xmin+(xmax-xmin)*i/60; const r=repro(off,p,cr,vd).mean;
      const px=X(p),py=Y(r); i?x.lineTo(px,py):x.moveTo(px,py);} x.stroke(); }
  // current setting marker
  const off=parseInt(off_i.value),p=parseFloat(p_i.value),r=repro(off,p,cr,vd).mean;
  x.fillStyle='#fff';x.beginPath();x.arc(X(p),Y(r),4,0,Math.PI*2);x.fill();
}

const $=id=>document.getElementById(id);
const off_i=$('off'),p_i=$('p'),cr_i=$('cr'),vd_i=$('vd'),m_i=$('m'),R_i=$('R'),v_i=$('v'),kw_i=$('kw'),isru_i=$('isru'),cl_i=$('cl');
function render(){
  const off=parseInt(off_i.value),p=parseFloat(p_i.value),cr=parseFloat(cr_i.value),vd=parseFloat(vd_i.value);
  const m=Math.pow(10,parseFloat(m_i.value)),R=parseFloat(R_i.value),v=parseFloat(v_i.value);
  const kW=Math.pow(10,parseFloat(kw_i.value)),isru=Math.pow(10,parseFloat(isru_i.value)),clr=parseFloat(cl_i.value);
  // labels
  $('offV').textContent=off; $('pV').textContent=p.toFixed(2); $('crV').textContent=cr.toFixed(3); $('vdV').textContent=vd.toFixed(2);
  $('mV').textContent=Math.round(m).toLocaleString(); $('RV').textContent=R; $('vV').textContent=v;
  $('kwV').textContent=Math.round(kW); $('isruV').textContent=Math.round(isru).toLocaleString(); $('clV').textContent=clr.toFixed(2);
  // reproduction
  const rr=repro(off,p,cr,vd);
  $('reff').textContent=rr.mean.toFixed(2);
  const exp=rr.mean>1;
  const vd2=$('verdict'); vd2.textContent=exp?'EXPANDS':'extinction-prone';
  vd2.style.background=exp?'rgba(122,240,168,.16)':'rgba(255,122,138,.16)';
  vd2.style.color=exp?'#7af0a8':'#ff7a8a';
  $('frac').textContent=Math.round(rr.frac*100)+'%'; $('ext').textContent=rr.ext.toFixed(2);
  // braking
  const b=braking(m,R,v);
  $('bd').textContent=b.d<0.001?(b.d*LY/1.496e11).toFixed(0)+' AU':b.d.toFixed(3)+' ly';
  $('bt').textContent=b.t<1000?Math.round(b.t)+' yr':(b.t/1e3).toFixed(1)+' kyr';
  $('bg').textContent=b.g.toExponential(1)+' g'; $('bsail').textContent=Math.round(sailFor(m,0.01))+' km';
  // mass
  const mb=massBudget(kW,isru);
  $('mtot').textContent=Math.round(mb.total).toLocaleString()+' kg';
  $('mdom').textContent=mb.dom; $('mrad').textContent=mb.radArea.toFixed(0)+' m²'; $('mreac').textContent=Math.round(mb.reactor)+' kg';
  $('mnote').textContent='A minimal bootstrap seed shrinks the ISRU plant; a full factory grows it toward ~10⁷ kg.';
  // closure -- process power is the ELECTRIC output (4 kW-e at the 14 kW
  // thermal rating), matching engineering.py's closure(elec_kW=4.0) exactly.
  const cc=closure(m,kW*(4/14),clr);
  $('cvf').textContent=Math.round(cc.vf*100)+'%'; $('cvm').textContent=Math.round(cc.vk).toLocaleString()+' kg';
  $('cmm').textContent=cc.mm.toExponential(1)+'×'; $('cem').textContent=cc.em.toExponential(1)+'×';
  // big verdict
  $('bigverdict').innerHTML = exp
    ? `At these settings the lineage <b style="color:#7af0a8">expands</b> (R_eff = ${rr.mean.toFixed(2)} &gt; 1): each settled node yields more than one successful child, so the front spreads as a branching process.`
    : `At these settings the lineage is <b style="color:#ff7a8a">extinction-prone</b> (R_eff = ${rr.mean.toFixed(2)} &le; 1): too many children fail or reach sterile targets. Raise offspring or per-leg reliability to cross R_eff = 1.`;
  chart();
}
[off_i,p_i,cr_i,vd_i,m_i,R_i,v_i,kw_i,isru_i,cl_i].forEach(el=>el.addEventListener('input',render));
window.addEventListener('resize',chart);
render();
</script></body></html>'''

html = HTML.replace('__STARS_JSON__', json.dumps(stars, separators=(',',':')))
_out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'docs', 'engineering_dashboard.html')
open(_out, 'w', encoding='utf-8').write(html)
print('Wrote', os.path.normpath(_out), len(html), 'bytes,', len(stars), 'stars')
