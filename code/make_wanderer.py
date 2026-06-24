import json, math, build_catalog as bc, make_starfields as sf

rows = bc.build()
local = [{"x": r["x"], "y": r["y"], "z": r["z"], "color": r["color"],
          "common": r["common_name"], "sun": r["name"] == "Sun"} for r in rows]
bright = [{"x": s["x"], "y": s["y"], "z": s["z"], "color": s["color"],
           "common": s["common"], "sun": False} for s in sf.bright_stars()]
galaxy = [{"x": s["x"], "y": s["y"], "z": s["z"], "color": s["c"], "d": s["d"]}
          for s in sf.galaxy_stars(3000)]
gc = sf.gc_marker()

def cart(ra_h, dec_deg, d):
    ra = math.radians(ra_h*15); dec = math.radians(dec_deg)
    return (d*math.cos(dec)*math.cos(ra), d*math.cos(dec)*math.sin(ra), d*math.sin(dec))
GAL_RAW = [("Canis Major Dwarf",7.21,-27.67,25_000,7),("Sagittarius Dwarf",18.92,-30.48,70_000,7),
           ("LMC",5.393,-69.76,165_000,12),("SMC",0.877,-72.80,200_000,9),
           ("Andromeda",0.712,41.27,2_500_000,17),("Triangulum",1.565,30.66,2_730_000,12)]
galaxies = []
for short, ra, dec, d, r in GAL_RAW:
    x,y,z = cart(ra,dec,d); galaxies.append({"short":short,"dist":d,"x":round(x),"y":round(y),"z":round(z),"r":r})

HTML = r'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Galaxy Traveler - Wanderer across the Galaxy</title>
<style>
  :root{ --bg0:#05060d; --panel:rgba(14,18,38,.85); --line:rgba(120,150,220,.18);
         --txt:#dfe6ff; --dim:#93a0c8; --accent:#7fb3ff; --gold:#ffd35e; --violet:#cdbcff; --green:#7af0a8; }
  *{box-sizing:border-box} html,body{margin:0;height:100%;overflow:hidden;background:var(--bg0);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--txt)}
  #view{display:block;width:100vw;height:100vh;cursor:grab} #view.drag{cursor:grabbing}
  .panel{position:absolute;background:var(--panel);border:1px solid var(--line);border-radius:12px;
    padding:13px 15px;backdrop-filter:blur(8px);box-shadow:0 6px 24px rgba(0,0,0,.45)}
  #ctrl{top:14px;left:14px;width:256px;font-size:13px}
  #ctrl h1{margin:0 0 3px;font-size:15px} #ctrl .sub{color:var(--dim);font-size:11px;margin-bottom:11px;line-height:1.5}
  .fld{margin-bottom:11px} .fld label{display:flex;justify-content:space-between;font-size:11.5px;color:var(--dim);margin-bottom:4px}
  .fld label b{color:var(--txt)} input[type=range]{width:100%;accent-color:var(--accent)}
  .seg{display:flex;gap:3px;flex-wrap:wrap} .seg button{flex:1;min-width:54px;padding:6px 0;border-radius:7px;border:1px solid var(--line);
    background:#0a0f24;color:var(--dim);font-size:11px;cursor:pointer}
  .seg button.on{background:var(--accent);color:#04122b;font-weight:650;border-color:var(--accent)}
  .chk{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--dim);cursor:pointer;margin-top:2px}
  .chk input{accent-color:var(--accent)} .chk .hint{color:var(--violet);font-size:10.5px}
  #stat{top:14px;right:14px;width:232px;font-size:12.5px}
  #stat .row{display:flex;justify-content:space-between;padding:3px 0;color:var(--dim)}
  #stat .row b{color:var(--txt);font-variant-numeric:tabular-nums}
  #stat h2{margin:0 0 8px;font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--dim)}
  #modeline{margin-top:8px;border-top:1px solid var(--line);padding-top:8px;font-size:11.5px;color:var(--violet);line-height:1.5}
  #time{bottom:16px;left:50%;transform:translateX(-50%);width:min(680px,92vw);display:flex;align-items:center;gap:12px}
  #play{flex:none;width:38px;height:38px;border-radius:50%;border:1px solid var(--line);background:#0a0f24;color:var(--accent);font-size:15px;cursor:pointer}
  #scrub{flex:1;accent-color:var(--gold)} #tlabel{flex:none;width:108px;text-align:right;font-variant-numeric:tabular-nums;font-size:13px;color:var(--gold)}
  .legend{position:absolute;bottom:16px;left:16px;font-size:11px;color:var(--dim);line-height:1.7}
  .legend i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}
  kbd{background:#0a0f24;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:10px}
  .btn{width:100%;margin-top:10px;padding:8px;border-radius:8px;border:1px solid var(--line);background:#0a0f24;color:var(--txt);font-size:12.5px;cursor:pointer}
  .btn:hover{border-color:var(--gold);color:var(--gold)}
</style></head><body>
<canvas id="view"></canvas>

<div id="ctrl" class="panel">
  <h1>Wanderer across the Galaxy</h1>
  <div class="sub">A self-replicating fleet spreads star to star. <kbd>drag</kbd> rotate &middot; <kbd>scroll</kbd> zoom</div>
  <div class="fld"><label>Star field</label>
    <div class="seg" id="field">
      <button data-f="100ly" class="on">100 ly</button><button data-f="1kly">1 kly</button>
      <button data-f="mw">Milky Way</button><button data-f="lg">Local Group</button></div></div>
  <div class="fld"><label>Cruise speed <b><span id="spdV">450</span> km/s</b></label>
    <input type="range" id="spd" min="50" max="600" step="10" value="450"></div>
  <div class="fld"><label>Replication time <b><span id="bldV">1000</span> yr</b></label>
    <input type="range" id="bld" min="100" max="2000" step="50" value="1000"></div>
  <div class="fld"><label>Offspring per stop <b><span id="offV">2</span></b></label>
    <input type="range" id="off" min="1" max="4" step="1" value="2"></div>
  <div class="fld"><label>Horizon <b><span id="horV">10 kyr</span></b></label>
    <input type="range" id="hor" min="3.301" max="9.301" step="0.01" value="4"></div>
  <label class="chk"><input type="checkbox" id="persist"> Colonies keep replicating <span class="hint">no shared map</span></label>
  <button class="btn" id="reset">Reset to defaults</button>
</div>

<div id="stat" class="panel">
  <h2 id="statTitle">Fleet at <span id="tnow">0 yr</span></h2>
  <div class="row"><span id="lSettled">Systems settled</span> <b id="sSettled">1</b></div>
  <div class="row"><span id="lFlight">Probes in flight</span> <b id="sFlight">0</b></div>
  <div class="row"><span id="lGen">Generations</span> <b id="sGen">0</b></div>
  <div class="row">Reach frontier <b id="sFront">0 ly</b></div>
  <div class="row" id="rowProbes">Probes launched <b id="sProbes">0</b></div>
  <div class="row" id="rowRedun">Redundant visits <b id="sRedun">0</b></div>
  <div id="modeline"></div>
</div>

<div class="legend panel">
  <div><i style="background:#ffd35e"></i>Sun (home)</div>
  <div><i style="background:#7fb3ff"></i>settled colony</div>
  <div><i style="background:#7af0a8"></i>probe in flight / reached</div>
  <div><i style="background:#cdbcff"></i>galaxy</div>
</div>

<div id="time" class="panel">
  <button id="play">&#9658;</button>
  <input type="range" id="scrub" min="0" max="10000" step="10" value="0">
  <span id="tlabel">0 yr</span>
</div>

<script>
const LOCAL=__LOCAL__, BRIGHT=__BRIGHT__, GALAXY=__GALAXY__, GALAXIES=__GAL__, GC=__GC__;
const cv=document.getElementById('view'), ctx=cv.getContext('2d');
let W,H,cx,cy,dpr=Math.min(window.devicePixelRatio||1,2);
const V={yaw:0.65,pitch:0.5,scale:1,panx:0,pany:0};
const P={spd:450,bld:1000,off:2,hor:10000,persist:false};
const KMS_PER_C=299792.458, DEC_UNITS=15.0;

// ---- field configuration -------------------------------------------------
const SUN_NODE={x:0,y:0,z:0,color:'#fff2c0',common:'Sun',sun:true};
const F_LOCAL=LOCAL, F_1KLY=LOCAL.concat(BRIGHT), F_MW=[SUN_NODE].concat(GALAXY);
const FIELDS={
 '100ly':{stars:F_LOCAL,radius:110,  log:false,discrete:true, rings:[[10,'10 ly'],[25,'25 ly'],[50,'50 ly']],label:true},
 '1kly' :{stars:F_1KLY, radius:1100, log:false,discrete:true, rings:[[250,'250 ly'],[500,'500 ly'],[1000,'1 kly']],label:true},
 'mw'   :{stars:F_MW,   radius:80000,log:false,discrete:false,rings:[[10000,'10 kly'],[25000,'25 kly'],[50000,'50 kly']],label:false},
 'lg'   :{stars:F_LOCAL,radius:100,  log:true, discrete:false,rings:[[100,'100 ly'],[1e3,'1 kly'],[1e4,'10 kly'],[1e5,'100 kly'],[1e6,'1 Mly']],label:false},
};
let af='100ly';
let ASTARS=[], APOS=[], ASUN=0, SIM={nodes:[],edges:[]}, tNow=0, playing=true;

function setField(key){ af=key; const F=FIELDS[af];
  ASTARS=F.stars; APOS=ASTARS.map(s=>[s.x,s.y,s.z]);
  ASUN=Math.max(0,ASTARS.findIndex(s=>s.sun));
  fitScale(); recompute(); tNow=0; }
function fitScale(){ const F=FIELDS[af], half=Math.min(W,H)/2*0.9;
  V.scale = F.log ? half/(Math.log10(2.5e6)*DEC_UNITS) : half/F.radius; }

function resize(){ W=cv.clientWidth;H=cv.clientHeight;cv.width=W*dpr;cv.height=H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);cx=W/2;cy=H/2; fitScale(); }
window.addEventListener('resize',resize);

function plotPos(p){ if(!FIELDS[af].log) return p;
  const r=Math.hypot(p[0],p[1],p[2]); if(r<1) return [0,0,0];
  const s=Math.log10(r)*DEC_UNITS/r; return [p[0]*s,p[1]*s,p[2]*s]; }
function project(p){ const cyw=Math.cos(V.yaw),syw=Math.sin(V.yaw),cp=Math.cos(V.pitch),sp=Math.sin(V.pitch);
  const x1=p[0]*cyw-p[1]*syw, y1=p[0]*syw+p[1]*cyw, z1=p[2];
  const y2=y1*cp-z1*sp, z2=y1*sp+z1*cp;
  return {sx:cx+x1*V.scale+V.panx, sy:cy-z2*V.scale+V.pany, depth:y2}; }
const PJ=p=>project(plotPos(p));
const dsun=p=>Math.hypot(p[0],p[1],p[2]);

// ---- discrete fleet sim (operates on a given POS / SUN) ------------------
function hpush(h,x){h.push(x);let i=h.length-1;while(i>0){const p=(i-1)>>1;if(h[p][0]<=h[i][0])break;const t=h[p];h[p]=h[i];h[i]=t;i=p;}}
function hpop(h){const top=h[0],last=h.pop();if(h.length){h[0]=last;let i=0,n=h.length;for(;;){let l=2*i+1,r=l+1,m=i;if(l<n&&h[l][0]<h[m][0])m=l;if(r<n&&h[r][0]<h[m][0])m=r;if(m===i)break;const t=h[m];h[m]=h[i];h[i]=t;i=m;}}return top;}
function simulate(POS,SUN,speedC,buildYr,offspring,horizon,persistent){
  const n=POS.length, nodes=[], edges=[];
  const dist=(i,j)=>Math.hypot(POS[i][0]-POS[j][0],POS[i][1]-POS[j][1],POS[i][2]-POS[j][2]);
  if(!persistent){
    const claimed=new Set([SUN]); const heap=[]; hpush(heap,[0,SUN,0,-1]);
    while(heap.length){ const [t,si,gen]=hpop(heap); if(t>horizon) continue;
      nodes.push({i:si,t,gen}); const tReady=t+buildYr; if(tReady>horizon) continue;
      const cand=[]; for(let j=0;j<n;j++) if(!claimed.has(j)) cand.push(j);
      cand.sort((a,b)=>dist(si,a)-dist(si,b));
      for(let k=0;k<offspring&&k<cand.length;k++){ const j=cand[k]; claimed.add(j);
        const arrive=tReady+dist(si,j)/speedC;
        edges.push({from:si,to:j,depart:tReady,arrive,gen:gen+1,redundant:false});
        if(arrive<=horizon) hpush(heap,[arrive,j,gen+1,si]); } }
    return {nodes,edges};
  }
  const nbrCache={};
  const nbr=i=>{ if(!nbrCache[i]){ const a=[]; for(let j=0;j<n;j++) if(j!==i) a.push(j);
    a.sort((x,y)=>dist(i,x)-dist(i,y)); nbrCache[i]=a; } return nbrCache[i]; };
  const settledT=new Array(n).fill(Infinity);
  const heap=[]; hpush(heap,[0,0,SUN,0,-1]);
  while(heap.length){ const [t,kind,si,gen,extra]=hpop(heap); if(t>horizon) continue;
    if(kind===0){ if(settledT[si]===Infinity){ settledT[si]=t; nodes.push({i:si,t,gen}); hpush(heap,[t+buildYr,1,si,gen,0]); } }
    else { const order=nbr(si); let ptr=extra, launched=0;
      while(launched<offspring && ptr<order.length){ const tgt=order[ptr]; ptr++; launched++;
        const arrive=t+dist(si,tgt)/speedC;
        edges.push({from:si,to:tgt,depart:t,arrive,gen:gen+1,redundant:false});
        if(arrive<=horizon) hpush(heap,[arrive,0,tgt,gen+1,si]); }
      if(ptr<order.length && t+buildYr<=horizon) hpush(heap,[t+buildYr,1,si,gen,ptr]); } }
  for(const e of edges) e.redundant = settledT[e.to] < e.arrive-1e-9;
  return {nodes,edges};
}
function recompute(){ const F=FIELDS[af];
  SIM = F.discrete ? simulate(APOS,ASUN,P.spd/KMS_PER_C,P.bld,P.off,P.hor,P.persist) : {nodes:[],edges:[]};
  const sc=document.getElementById('scrub'); sc.max=P.hor; sc.step=Math.max(1,P.hor/1000); if(tNow>P.hor)tNow=P.hor; }

const genColor=g=> g===0?'#ffd35e':`hsl(${Math.max(140,220-(g-1)*22)},75%,65%)`;
const fmtYr=y=> y<1000?Math.round(y)+' yr' : y<1e6?(y/1e3).toFixed(y<1e4?1:0)+' kyr' : y<1e9?(y/1e6).toFixed(1)+' Myr' : (y/1e9).toFixed(2)+' Gyr';
const fmtLy=d=> d<1000?Math.round(d)+' ly' : d<1e6?(d/1e3).toFixed(0)+' kly' : (d/1e6).toFixed(2)+' Mly';
const hexA=(h,a)=>{const n=parseInt(h.slice(1),16);return `rgba(${(n>>16)&255},${(n>>8)&255},${n&255},${a})`;};

function ring(R,lab){ ctx.beginPath();
  for(let k=0;k<=72;k++){const a=k/72*Math.PI*2;const q=PJ([R*Math.cos(a),R*Math.sin(a),0]);
    k?ctx.lineTo(q.sx,q.sy):ctx.moveTo(q.sx,q.sy);} ctx.strokeStyle='rgba(120,150,220,.13)';ctx.stroke();
  const lp=PJ([R,0,0]); ctx.fillStyle='rgba(140,165,225,.5)';ctx.font='10px sans-serif';ctx.fillText(lab,lp.sx+4,lp.sy-3); }

function draw(){
  const F=FIELDS[af];
  ctx.clearRect(0,0,W,H);
  const g=ctx.createRadialGradient(cx,cy,0,cx,cy,Math.max(W,H)*0.7);
  g.addColorStop(0,'#0b1022');g.addColorStop(1,'#05060d');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  for(const [R,l] of F.rings) ring(R,l);

  const frontierLy=(P.spd/KMS_PER_C)*tNow;

  // satellite galaxies + Andromeda only in Local Group view
  let galReached=0, nearestUn=null;
  if(af==='lg'){
    if(frontierLy>1){ ctx.beginPath();
      for(let k=0;k<=72;k++){const a=k/72*Math.PI*2;const q=PJ([frontierLy*Math.cos(a),frontierLy*Math.sin(a),0]);k?ctx.lineTo(q.sx,q.sy):ctx.moveTo(q.sx,q.sy);}
      ctx.strokeStyle='rgba(122,240,168,.55)';ctx.setLineDash([5,5]);ctx.lineWidth=1.3;ctx.stroke();ctx.setLineDash([]); }
    for(const gx of GALAXIES){ const q=PJ([gx.x,gx.y,gx.z]); const reached=gx.dist<=frontierLy;
      if(reached) galReached++; else if(!nearestUn||gx.dist<nearestUn.dist) nearestUn=gx;
      const grd=ctx.createRadialGradient(q.sx,q.sy,0,q.sx,q.sy,gx.r);
      grd.addColorStop(0,reached?'rgba(122,240,168,.95)':'rgba(205,188,255,.9)');grd.addColorStop(1,'rgba(205,188,255,0)');
      ctx.fillStyle=grd;ctx.beginPath();ctx.arc(q.sx,q.sy,gx.r,0,Math.PI*2);ctx.fill();
      const tc=gx.dist/(P.spd/KMS_PER_C);
      ctx.fillStyle=reached?'#7af0a8':'#cdbcff';ctx.font='11px sans-serif';
      ctx.fillText(`${gx.short} · ${fmtLy(gx.dist)} · ${fmtYr(tc)}`, q.sx+gx.r+4, q.sy+3); }
  }

  // Galactic Centre marker in Milky Way view
  if(af==='mw'){ const q=PJ([GC.x,GC.y,GC.z]);
    const grd=ctx.createRadialGradient(q.sx,q.sy,0,q.sx,q.sy,16);
    grd.addColorStop(0,'rgba(255,226,176,.9)');grd.addColorStop(1,'rgba(255,200,120,0)');
    ctx.fillStyle=grd;ctx.beginPath();ctx.arc(q.sx,q.sy,16,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#ffe2b0';ctx.font='11px sans-serif';ctx.fillText('Galactic Centre', q.sx+12, q.sy+3); }

  // reach frontier ring (Milky Way)
  if(af==='mw' && frontierLy>1){ ctx.beginPath();
    for(let k=0;k<=72;k++){const a=k/72*Math.PI*2;const q=PJ([frontierLy*Math.cos(a),frontierLy*Math.sin(a),0]);k?ctx.lineTo(q.sx,q.sy):ctx.moveTo(q.sx,q.sy);}
    ctx.strokeStyle='rgba(122,240,168,.5)';ctx.setLineDash([5,5]);ctx.lineWidth=1.3;ctx.stroke();ctx.setLineDash([]); }

  // discrete fleet settled set
  const settled=new Set(), genOf={};
  for(const nd of SIM.nodes) if(nd.t<=tNow){settled.add(nd.i);genOf[nd.i]=nd.gen;}

  // fleet edges + probes (discrete fields)
  let inflight=0, launched=0, redun=0;
  if(F.discrete){ for(const e of SIM.edges){ if(e.depart>tNow) continue; launched++;
    const frac=Math.max(0,Math.min(1,(tNow-e.depart)/(e.arrive-e.depart))); const arrived=frac>=1;
    if(arrived && e.redundant){ redun++; continue; }
    const a=PJ(APOS[e.from]), b=PJ(APOS[e.to]);
    const mx=a.sx+(b.sx-a.sx)*frac, my=a.sy+(b.sy-a.sy)*frac;
    ctx.beginPath();ctx.moveTo(a.sx,a.sy);ctx.lineTo(mx,my);
    ctx.strokeStyle=arrived?'rgba(127,179,255,.30)':'rgba(122,240,168,.5)';ctx.lineWidth=1;ctx.stroke();
    if(!arrived){inflight++;ctx.beginPath();ctx.arc(mx,my,2.4,0,Math.PI*2);ctx.fillStyle='#7af0a8';ctx.fill();} } }

  // stars
  let reached=0;
  const order=ASTARS.map((s,i)=>({i,p:PJ(APOS[i])})).sort((a,b)=>b.p.depth-a.p.depth);
  for(const o of order){ const s=ASTARS[o.i], p=o.p;
    if(s.sun){ ctx.fillStyle='#fff2c0';ctx.beginPath();ctx.arc(p.sx,p.sy,3.4,0,Math.PI*2);ctx.fill();
      ctx.strokeStyle='#ffd35e';ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(p.sx,p.sy,7,0,Math.PI*2);ctx.stroke();
      ctx.fillStyle='rgba(255,231,160,.95)';ctx.font='11px sans-serif';ctx.fillText('Sun',p.sx+9,p.sy+3); continue; }
    let lit=false, gen=0;
    if(F.discrete){ lit=settled.has(o.i); gen=genOf[o.i]||0; }
    else if(af==='mw'){ lit = dsun(APOS[o.i])<=frontierLy; if(lit) reached++; }
    const r = lit?3.0:(af==='mw'?1.1:1.5);
    if(lit){ ctx.globalAlpha=1;ctx.beginPath();ctx.arc(p.sx,p.sy,r,0,Math.PI*2);
      ctx.fillStyle = F.discrete?genColor(gen):'#7af0a8'; ctx.fill();
      if(F.label && s.common){ ctx.fillStyle='rgba(223,230,255,.9)';ctx.font='10px sans-serif';ctx.fillText(s.common,p.sx+r+4,p.sy+3);} }
    else { ctx.globalAlpha=(af==='mw'?.55:.5);ctx.beginPath();ctx.arc(p.sx,p.sy,r,0,Math.PI*2);ctx.fillStyle=s.color;ctx.fill();ctx.globalAlpha=1; } }

  // ---- stats ----
  let maxg=0; for(const i of settled) maxg=Math.max(maxg,genOf[i]||0);
  document.getElementById('tnow').textContent=fmtYr(tNow);
  document.getElementById('tlabel').textContent=fmtYr(tNow);
  document.getElementById('scrub').value=tNow;
  document.getElementById('sFront').textContent=fmtLy(frontierLy);
  const showFleet = F.discrete;
  document.getElementById('rowProbes').style.display = showFleet?'flex':'none';
  document.getElementById('rowRedun').style.display = showFleet?'flex':'none';
  const ml=document.getElementById('modeline');
  if(F.discrete){
    document.getElementById('lSettled').textContent='Systems settled';
    document.getElementById('sSettled').textContent=settled.size;
    document.getElementById('lFlight').textContent='Probes in flight';
    document.getElementById('sFlight').textContent=inflight;
    document.getElementById('lGen').textContent='Generations'; document.getElementById('sGen').textContent=maxg;
    document.getElementById('sProbes').textContent=launched.toLocaleString();
    const arr=launched-inflight;
    document.getElementById('sRedun').textContent=redun.toLocaleString()+(arr>0?` (${Math.round(100*redun/arr)}%)`:'');
    ml.innerHTML = af==='100ly'
      ? `Real curated stars within 100 ly. Try <b>1 kly</b>, <b>Milky Way</b>, or <b>Local Group</b>.`
      : `${ASTARS.length-1} real stars out to ~1 kly (named bright stars added). The fleet hops through them.`;
  } else if(af==='mw'){
    document.getElementById('lSettled').textContent='Stars reached';
    document.getElementById('sSettled').textContent=`${reached} / ${ASTARS.length-1}`;
    document.getElementById('lFlight').textContent='Disk crossed'; 
    document.getElementById('sFlight').textContent = frontierLy>=50000?'yes':`${Math.round(100*frontierLy/50000)}%`;
    document.getElementById('lGen').textContent='Galaxy in'; 
    document.getElementById('sGen').textContent=fmtYr(1e5/(P.spd/KMS_PER_C));
    ml.innerHTML = `Modelled Milky Way — real disk/arm/bulge structure &amp; Sun position; individual stars synthetic. The green frontier expands at cruise speed; reaching the far disk takes tens of Myr.`;
  } else { // lg
    document.getElementById('lSettled').textContent='Galaxies reached';
    document.getElementById('sSettled').textContent=`${galReached} / ${GALAXIES.length}`;
    document.getElementById('lFlight').textContent='Nearest unreached';
    document.getElementById('sFlight').textContent = nearestUn?nearestUn.short:'—';
    document.getElementById('lGen').textContent='Galaxy in';
    document.getElementById('sGen').textContent=fmtYr(1e5/(P.spd/KMS_PER_C));
    ml.innerHTML = `Log scale: the 100 ly catalogue is the speck at the centre; satellite galaxies &amp; Andromeda (2.5 Mly) sit far out. A galaxy jump has no stepping stones.`;
  }
}

function loop(){ if(playing){ tNow+=P.hor/720; if(tNow>=P.hor){tNow=P.hor;playing=false;document.getElementById('play').innerHTML='&#9658;';} }
  draw(); requestAnimationFrame(loop); }

let drag=false,lx=0,ly=0;
cv.addEventListener('mousedown',e=>{drag=true;lx=e.clientX;ly=e.clientY;cv.classList.add('drag');});
window.addEventListener('mouseup',()=>{drag=false;cv.classList.remove('drag');});
window.addEventListener('mousemove',e=>{ if(!drag)return; V.yaw+=(e.clientX-lx)*0.005;V.pitch+=(e.clientY-ly)*0.005;
  V.pitch=Math.max(-1.5,Math.min(1.5,V.pitch));lx=e.clientX;ly=e.clientY; });
cv.addEventListener('wheel',e=>{e.preventDefault();V.scale*=Math.exp(-e.deltaY*0.0012);},{passive:false});

function bind(id,key,fmt,after){ const el=document.getElementById(id);
  el.addEventListener('input',()=>{ P[key]=parseFloat(el.value); if(fmt)document.getElementById(id+'V').textContent=fmt(P[key]); if(after)after(); draw(); }); }
bind('spd','spd',v=>v.toFixed(0),recompute);
bind('bld','bld',v=>v.toFixed(0),recompute);
bind('off','off',v=>v.toFixed(0),recompute);
document.getElementById('hor').addEventListener('input',function(){ P.hor=Math.round(Math.pow(10,parseFloat(this.value)));
  document.getElementById('horV').textContent=fmtYr(P.hor); recompute(); draw(); });
document.querySelectorAll('#field button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('#field button').forEach(x=>x.classList.remove('on')); b.classList.add('on');
  setField(b.dataset.f); document.getElementById('play').innerHTML='&#10074;&#10074;'; playing=true; draw(); });
document.getElementById('persist').addEventListener('change',function(){ P.persist=this.checked; recompute(); draw(); });
document.getElementById('scrub').addEventListener('input',e=>{ tNow=parseFloat(e.target.value); playing=false;document.getElementById('play').innerHTML='&#9658;';draw(); });
document.getElementById('play').addEventListener('click',function(){ if(tNow>=P.hor)tNow=0; playing=!playing; this.innerHTML=playing?'&#10074;&#10074;':'&#9658;'; });
document.getElementById('reset').addEventListener('click',()=>{
  P.spd=450; P.bld=1000; P.off=2; P.hor=10000; P.persist=false;
  document.getElementById('spd').value=450; document.getElementById('spdV').textContent='450';
  document.getElementById('bld').value=1000; document.getElementById('bldV').textContent='1000';
  document.getElementById('off').value=2; document.getElementById('offV').textContent='2';
  document.getElementById('hor').value=4; document.getElementById('horV').textContent=fmtYr(10000);
  document.getElementById('persist').checked=false;
  document.querySelectorAll('#field button').forEach(x=>x.classList.toggle('on', x.dataset.f==='100ly'));
  V.yaw=0.65; V.pitch=0.5; V.panx=0; V.pany=0;
  setField('100ly');
  playing=true; document.getElementById('play').innerHTML='&#10074;&#10074;';
  draw();
});

resize(); setField('100ly'); loop();
</script></body></html>'''

html = HTML.replace('__LOCAL__', json.dumps(local, separators=(',',':')))
html = html.replace('__BRIGHT__', json.dumps(bright, separators=(',',':')))
html = html.replace('__GALAXY__', json.dumps(galaxy, separators=(',',':')))
html = html.replace('__GAL__', json.dumps(galaxies, separators=(',',':')))
html = html.replace('__GC__', json.dumps(gc, separators=(',',':')))
open('wanderer_map.html','w',encoding='utf-8').write(html)
print('Wrote wanderer_map.html', len(html), 'bytes;', len(local),'local,',len(bright),'bright,',len(galaxy),'galaxy,',len(galaxies),'galaxies')
import re; open('/tmp/wmap4.js','w').write(re.search(r'<script>(.*?)</script>',html,re.S).group(1))
