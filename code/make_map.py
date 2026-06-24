import json, build_catalog as bc, propulsion as prop
rows = bc.build()
ENGINES = [{"name": p["engine"], "cruise": round(p["cruise_frac_c"], 6),
            "accel_t": round(p["accel_time_yr"], 3), "accel_d": round(p["accel_dist_ly"], 4),
            "color": prop.COLORS[p["engine"]]} for p in prop.profiles()]

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Galaxy Traveler - Local Stars within 100 ly</title>
<style>
  :root{ --bg0:#05060d; --bg1:#0b1022; --panel:rgba(14,18,38,.82);
         --line:rgba(120,150,220,.18); --txt:#dfe6ff; --dim:#93a0c8;
         --accent:#7fb3ff; --gold:#ffd35e; }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%;overflow:hidden;background:var(--bg0);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--txt)}
  #view{display:block;width:100vw;height:100vh;cursor:grab}
  #view.drag{cursor:grabbing}
  .panel{position:absolute;background:var(--panel);border:1px solid var(--line);
    border-radius:12px;padding:12px 14px;backdrop-filter:blur(8px);font-size:13px;
    box-shadow:0 6px 24px rgba(0,0,0,.45)}
  #hud{top:14px;left:14px;max-width:300px}
  #hud h1{margin:0 0 4px;font-size:15px;font-weight:650;letter-spacing:.2px}
  #hud .sub{color:var(--dim);font-size:11.5px;line-height:1.5}
  #ctrl{top:14px;right:14px;width:232px}
  #ctrl input[type=text]{width:100%;padding:7px 9px;border-radius:8px;border:1px solid var(--line);
    background:#0a0f24;color:var(--txt);font-size:13px;margin-bottom:8px;outline:none}
  #ctrl input[type=text]:focus{border-color:var(--accent)}
  .seg{display:flex;gap:4px;margin-bottom:9px}
  .seg button{flex:1;padding:6px 0;border-radius:7px;border:1px solid var(--line);
    background:#0a0f24;color:var(--dim);font-size:11.5px;cursor:pointer}
  .seg button.on{background:var(--accent);color:#04122b;border-color:var(--accent);font-weight:650}
  .chk{display:flex;align-items:center;gap:7px;margin:6px 0;color:var(--dim);font-size:12.5px;cursor:pointer}
  .chk input{accent-color:var(--accent)}
  #ctrl .btn{width:100%;margin-top:6px;padding:7px;border-radius:8px;border:1px solid var(--line);
    background:#0a0f24;color:var(--txt);font-size:12.5px;cursor:pointer}
  #ctrl .btn:hover{border-color:var(--accent)}
  #legend{bottom:14px;left:14px;font-size:11.5px;line-height:1.7}
  #legend .row{display:flex;align-items:center;gap:7px;color:var(--dim)}
  #legend .dot{width:10px;height:10px;border-radius:50%;display:inline-block;flex:none}
  #info{bottom:14px;right:14px;width:266px;display:none}
  #info h2{margin:0 0 2px;font-size:14px}
  #info .cn{color:var(--dim);font-size:11.5px;margin-bottom:8px}
  #info table{width:100%;border-collapse:collapse;font-size:12px}
  #info td{padding:2px 0;color:var(--dim)} #info td.v{color:var(--txt);text-align:right}
  #info .tag{display:inline-block;margin-top:8px;padding:2px 8px;border-radius:20px;
    font-size:10.5px;background:rgba(127,179,255,.16);color:var(--accent)}
  #info .btn{width:100%;margin-top:10px;padding:7px;border-radius:8px;border:1px solid var(--line);
    background:#0a0f24;color:var(--txt);font-size:12px;cursor:pointer}
  #info .btn:hover{border-color:var(--gold);color:var(--gold)}
  #tip{position:absolute;pointer-events:none;background:rgba(6,9,20,.94);border:1px solid var(--line);
    border-radius:7px;padding:5px 8px;font-size:11.5px;display:none;white-space:nowrap;z-index:9}
  #foot{bottom:14px;left:50%;transform:translateX(-50%);color:var(--dim);font-size:11px;
    background:none;border:none;box-shadow:none;text-align:center}
  kbd{background:#0a0f24;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:10.5px}
  .rsec{margin-top:11px;border-top:1px solid var(--line);padding-top:10px}
  .rlbl{font-size:11.5px;color:var(--dim);margin-bottom:6px}
  #ctrl input[type=range]{width:100%;margin-top:5px;accent-color:var(--accent)}
  #hzval{color:var(--txt)}
</style>
</head>
<body>
<canvas id="view"></canvas>

<div id="hud" class="panel">
  <h1>Local Stars &middot; 100 ly</h1>
  <div class="sub" id="hudsub"></div>
</div>

<div id="ctrl" class="panel">
  <input id="search" type="text" placeholder="Search a star (e.g. Vega)...">
  <div class="seg" id="filter">
    <button data-f="all" class="on">All</button>
    <button data-f="notable">Notable</button>
    <button data-f="host">Planet hosts</button>
  </div>
  <label class="chk"><input type="checkbox" id="ckLabels" checked> Labels (notable)</label>
  <label class="chk"><input type="checkbox" id="ckRings" checked> Distance rings</label>
  <label class="chk"><input type="checkbox" id="ckSpin" checked> Auto-rotate</label>
  <button class="btn" id="reset">Reset view &amp; origin</button>
  <div class="rsec">
    <div class="rlbl">Reachable range &mdash; flyby</div>
    <div class="seg" id="engine">
      <button data-e="-1" class="on">Off</button>
      <button data-e="0">Sail</button>
      <button data-e="1">Fusion</button>
      <button data-e="2">N&middot;elec</button>
    </div>
    <div class="rlbl" style="margin:8px 0 0">Time horizon: <b id="hzval">100 yr</b></div>
    <input type="range" id="horizon" min="1" max="5" step="0.01" value="2">
  </div>
</div>

<div id="legend" class="panel">
  <div class="row"><span class="dot" style="background:#aabfff"></span>O/B hot blue</div>
  <div class="row"><span class="dot" style="background:#cad7ff"></span>A white</div>
  <div class="row"><span class="dot" style="background:#f8f7ff"></span>F yellow-white</div>
  <div class="row"><span class="dot" style="background:#fff4ea"></span>G Sun-like</div>
  <div class="row"><span class="dot" style="background:#ffd2a1"></span>K orange</div>
  <div class="row"><span class="dot" style="background:#ffb56c"></span>M red dwarf</div>
  <div class="row"><span class="dot" style="background:#e8f0ff;box-shadow:0 0 4px #fff"></span>White dwarf</div>
  <div class="row"><span class="dot" style="background:var(--gold)"></span>Measurement origin</div>
</div>

<div id="info" class="panel">
  <h2 id="iName"></h2><div class="cn" id="iCommon"></div>
  <table><tbody id="iBody"></tbody></table>
  <span class="tag" id="iTag"></span>
  <button class="btn" id="setOrigin">Set as measurement origin</button>
</div>

<div id="tip"></div>
<div id="foot" class="panel"><kbd>drag</kbd> rotate &nbsp; <kbd>scroll</kbd> zoom &nbsp; <kbd>click</kbd> select &nbsp; <kbd>hover</kbd> measure from origin</div>

<script>
const STARS = __STARS_JSON__;
const ENGINES = __ENGINES_JSON__;
const SUN = STARS.findIndex(s => s.name === "Sun");
const cv = document.getElementById('view'), ctx = cv.getContext('2d');
let W=0,H=0,cx=0,cy=0,dpr=Math.min(window.devicePixelRatio||1,2);

const V = { yaw:0.65, pitch:0.5, scale:1, panx:0, pany:0,
            spin:true, labels:true, rings:true, filter:'all',
            ref:SUN, sel:-1, hover:-1, engine:-1, horizon:100 };
let proj = [];           // per-frame {sx,sy,depth,i}

function resize(){
  W = cv.clientWidth; H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  cx = W/2; cy = H/2;
  V.scale = Math.min(W,H)/2/100*0.92;
}
window.addEventListener('resize', resize);

function project(s){
  const cy_=Math.cos(V.yaw), sy_=Math.sin(V.yaw),
        cp=Math.cos(V.pitch), sp=Math.sin(V.pitch);
  const x1 = s.x*cy_ - s.y*sy_, y1 = s.x*sy_ + s.y*cy_, z1 = s.z;
  const y2 = y1*cp - z1*sp, z2 = y1*sp + z1*cp;
  return { sx: cx + x1*V.scale + V.panx,
           sy: cy - z2*V.scale + V.pany,
           depth: y2 };
}
const dist3 = (a,b)=>Math.hypot(a.x-b.x,a.y-b.y,a.z-b.z);
const fromSun = s=>Math.hypot(s.x,s.y,s.z);
const reachLy = e=>e.cruise*Math.max(0,V.horizon-e.accel_t)+e.accel_d;
const travelYr = (e,d)=>e.accel_t+Math.max(0,d-e.accel_d)/e.cruise;
const fmtYr = y=>y<1?'<1 yr':y<1000?Math.round(y)+' yr':y<1e6?(y/1e3).toFixed(1)+' kyr':(y/1e6).toFixed(1)+' Myr';
const hexA = (h,a)=>{const n=parseInt(h.slice(1),16);return `rgba(${(n>>16)&255},${(n>>8)&255},${n&255},${a})`;};

function shown(s){
  if(V.filter==='notable') return s.notable;
  if(V.filter==='host') return s.category==='planet-host';
  return true;
}

function draw(){
  ctx.clearRect(0,0,W,H);
  // background glow
  const g = ctx.createRadialGradient(cx,cy,0,cx,cy,Math.max(W,H)*0.7);
  g.addColorStop(0,'#0b1022'); g.addColorStop(1,'#05060d');
  ctx.fillStyle=g; ctx.fillRect(0,0,W,H);

  // distance rings on the equatorial (xy) plane
  if(V.rings){
    ctx.lineWidth=1;
    for(const R of [25,50,100]){
      ctx.beginPath();
      for(let k=0;k<=72;k++){
        const t=k/72*Math.PI*2;
        const p=project({x:R*Math.cos(t), y:R*Math.sin(t), z:0});
        k?ctx.lineTo(p.sx,p.sy):ctx.moveTo(p.sx,p.sy);
      }
      ctx.strokeStyle='rgba(120,150,220,.16)'; ctx.stroke();
      const lp=project({x:R,y:0,z:0});
      ctx.fillStyle='rgba(140,165,225,.5)'; ctx.font='10px sans-serif';
      ctx.fillText(R+' ly', lp.sx+4, lp.sy-3);
    }
  }

  // reachability bubble (orthographic: a sphere about the Sun projects to a circle)
  if(V.engine>=0){
    const e=ENGINES[V.engine], sun=project(STARS[SUN]), R=Math.max(0,reachLy(e)*V.scale);
    ctx.beginPath(); ctx.arc(sun.sx,sun.sy,R,0,Math.PI*2);
    ctx.fillStyle=hexA(e.color,.06); ctx.fill();
    ctx.strokeStyle=hexA(e.color,.55); ctx.lineWidth=1.3; ctx.setLineDash([5,5]);
    ctx.stroke(); ctx.setLineDash([]);
  }

  // project + depth sort (far first)
  proj = STARS.map((s,i)=>{const p=project(s); p.i=i; return p;});
  proj.sort((a,b)=>b.depth-a.depth);

  const refS = STARS[V.ref];
  // measurement line ref -> hovered
  if(V.hover>=0 && V.hover!==V.ref){
    const a=project(refS), b=project(STARS[V.hover]);
    ctx.beginPath(); ctx.moveTo(a.sx,a.sy); ctx.lineTo(b.sx,b.sy);
    ctx.strokeStyle='rgba(255,211,94,.7)'; ctx.lineWidth=1.2; ctx.setLineDash([4,4]);
    ctx.stroke(); ctx.setLineDash([]);
    const d=dist3(refS,STARS[V.hover]);
    ctx.fillStyle='#ffd35e'; ctx.font='12px sans-serif';
    ctx.fillText(d.toFixed(2)+' ly', (a.sx+b.sx)/2+6, (a.sy+b.sy)/2-4);
  }

  for(const p of proj){
    const s=STARS[p.i]; const vis=shown(s);
    const t=(p.depth+100)/200;                 // 0 near .. 1 far
    let r = Math.max(1.5, Math.min(8, 6 - 0.55*s.vmag));
    if(s.notable) r=Math.max(r,3.2);
    r *= (1.2 - 0.55*t);
    let alpha = (1.0 - 0.5*t) * (vis?1:0.10);
    if(V.engine>=0 && p.i!==SUN && fromSun(s) > reachLy(ENGINES[V.engine])) alpha*=0.12;
    if(p.i===SUN){ drawSun(p); continue; }
    ctx.globalAlpha=alpha; ctx.beginPath();
    ctx.arc(p.sx,p.sy,r,0,Math.PI*2); ctx.fillStyle=s.color; ctx.fill();
    if(s.category==='planet-host' && vis){
      ctx.globalAlpha=alpha*0.8; ctx.lineWidth=1;
      ctx.strokeStyle='rgba(127,179,255,.9)'; ctx.beginPath();
      ctx.arc(p.sx,p.sy,r+2.6,0,Math.PI*2); ctx.stroke();
    }
    ctx.globalAlpha=1;
    if(V.labels && vis && s.notable && r>2.2){
      ctx.fillStyle='rgba(223,230,255,.82)'; ctx.font='10.5px sans-serif';
      ctx.fillText(s.common_name, p.sx+r+3, p.sy+3);
    }
  }
  // highlight selected / hover
  for(const idx of [V.sel,V.hover]){
    if(idx<0) continue;
    const p=project(STARS[idx]);
    ctx.beginPath(); ctx.arc(p.sx,p.sy,9,0,Math.PI*2);
    ctx.strokeStyle = idx===V.sel?'#ffd35e':'#7fb3ff'; ctx.lineWidth=1.5; ctx.stroke();
    if(idx===V.hover){
      ctx.fillStyle='rgba(223,230,255,.95)'; ctx.font='11px sans-serif';
      ctx.fillText(STARS[idx].common_name, p.sx+12, p.sy-8);
    }
  }
}

function drawSun(p){
  ctx.globalAlpha=1;
  const grd=ctx.createRadialGradient(p.sx,p.sy,0,p.sx,p.sy,9);
  grd.addColorStop(0,'#fff7d6'); grd.addColorStop(1,'rgba(255,211,94,0)');
  ctx.fillStyle=grd; ctx.beginPath(); ctx.arc(p.sx,p.sy,9,0,Math.PI*2); ctx.fill();
  ctx.fillStyle='#fff2c0'; ctx.beginPath(); ctx.arc(p.sx,p.sy,3.2,0,Math.PI*2); ctx.fill();
  if(V.ref===SUN){ ctx.strokeStyle='#ffd35e'; ctx.lineWidth=1.4;
    ctx.beginPath(); ctx.arc(p.sx,p.sy,11,0,Math.PI*2); ctx.stroke(); }
  ctx.fillStyle='rgba(255,231,160,.95)'; ctx.font='11px sans-serif';
  ctx.fillText('Sun', p.sx+11, p.sy+3);
}

function loop(){ if(V.spin){ V.yaw+=0.0016; } draw(); requestAnimationFrame(loop); }

// ---- picking -------------------------------------------------------------
function pick(mx,my){
  let best=-1, bd=11;
  for(const p of proj){
    const d=Math.hypot(p.sx-mx,p.sy-my);
    if(d<bd){ bd=d; best=p.i; }
  }
  return best;
}

// ---- interaction ---------------------------------------------------------
let drag=false, moved=false, lx=0, ly=0;
cv.addEventListener('mousedown', e=>{drag=true;moved=false;lx=e.clientX;ly=e.clientY;cv.classList.add('drag');});
window.addEventListener('mouseup', e=>{
  if(drag && !moved){ const r=cv.getBoundingClientRect(); const i=pick(e.clientX-r.left,e.clientY-r.top);
    if(i>=0) select(i); }
  drag=false; cv.classList.remove('drag');
});
window.addEventListener('mousemove', e=>{
  const r=cv.getBoundingClientRect(), mx=e.clientX-r.left, my=e.clientY-r.top;
  if(drag){
    const dx=e.clientX-lx, dy=e.clientY-ly;
    if(Math.abs(dx)+Math.abs(dy)>3){ moved=true; V.spin=false; document.getElementById('ckSpin').checked=false; }
    V.yaw += dx*0.005; V.pitch += dy*0.005;
    V.pitch=Math.max(-1.5,Math.min(1.5,V.pitch));
    lx=e.clientX; ly=e.clientY;
  } else {
    const i=pick(mx,my); V.hover=i;
    const tip=document.getElementById('tip');
    if(i>=0){ const s=STARS[i];
      tip.style.display='block'; tip.style.left=(mx+14)+'px'; tip.style.top=(my+14)+'px';
      let extra = '';
      if(V.engine>=0){ const e=ENGINES[V.engine]; extra=` &middot; <span style="color:${e.color}">${fmtYr(travelYr(e,fromSun(s)))}</span>`; }
      tip.innerHTML = `<b>${s.common_name}</b> &middot; ${fromSun(s).toFixed(2)} ly${extra}`;
    } else tip.style.display='none';
  }
});
cv.addEventListener('wheel', e=>{ e.preventDefault();
  const f=Math.exp(-e.deltaY*0.0012); V.scale*=f;
  V.scale=Math.max(0.5,Math.min(60,V.scale));
},{passive:false});

function select(i){
  V.sel=i; const s=STARS[i];
  document.getElementById('info').style.display='block';
  document.getElementById('iName').textContent=s.name;
  document.getElementById('iCommon').textContent=
     (s.common_name!==s.name?s.common_name+' · ':'')+s.spectral;
  const ref=STARS[V.ref];
  const rows=[
    ['Distance from Sun', fromSun(s).toFixed(2)+' ly'],
    ['Distance from '+ref.common_name, dist3(s,ref).toFixed(2)+' ly'],
    ['App. magnitude', s.vmag.toFixed(2)],
    ['RA / Dec', s.ra_hours.toFixed(2)+'h / '+s.dec_deg.toFixed(1)+'°'],
    ['x, y, z (ly)', s.x.toFixed(1)+', '+s.y.toFixed(1)+', '+s.z.toFixed(1)],
  ];
  if(V.engine>=0){ const e=ENGINES[V.engine];
    rows.push(['Flyby time ('+e.name+')', fmtYr(travelYr(e,fromSun(s)))]); }
  document.getElementById('iBody').innerHTML =
    rows.map(r=>`<tr><td>${r[0]}</td><td class="v">${r[1]}</td></tr>`).join('');
  const tag=document.getElementById('iTag');
  const labels={'planet-host':'Known exoplanet host','white-dwarf':'White dwarf',
    'giant':'Giant star','named':'Notable named star','nearest':'Nearby dwarf','sun':'Home'};
  tag.textContent=labels[s.category]||s.category;
}
document.getElementById('setOrigin').onclick=()=>{ if(V.sel>=0){V.ref=V.sel; select(V.sel); updHud();} };

// search
document.getElementById('search').addEventListener('keydown',e=>{
  if(e.key!=='Enter') return;
  const q=e.target.value.trim().toLowerCase(); if(!q) return;
  let i=STARS.findIndex(s=>s.name.toLowerCase()===q||s.common_name.toLowerCase()===q);
  if(i<0) i=STARS.findIndex(s=>s.name.toLowerCase().includes(q)||s.common_name.toLowerCase().includes(q));
  if(i>=0){ select(i); V.hover=i; } else { e.target.value=''; e.target.placeholder='not found - try again'; }
});
// filter buttons
document.querySelectorAll('#filter button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('#filter button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); V.filter=b.dataset.f; updHud();
});
document.getElementById('ckLabels').onchange=e=>V.labels=e.target.checked;
document.getElementById('ckRings').onchange =e=>V.rings =e.target.checked;
document.getElementById('ckSpin').onchange  =e=>V.spin  =e.target.checked;
document.getElementById('reset').onclick=()=>{
  V.yaw=0.65;V.pitch=0.5;V.panx=0;V.pany=0;V.ref=SUN;V.sel=-1;
  resize(); updHud(); document.getElementById('info').style.display='none';
};
document.querySelectorAll('#engine button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('#engine button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); V.engine=parseInt(b.dataset.e); if(V.sel>=0)select(V.sel); updHud();
});
document.getElementById('horizon').addEventListener('input',e=>{
  V.horizon=Math.round(Math.pow(10,parseFloat(e.target.value)));
  document.getElementById('hzval').textContent=fmtYr(V.horizon);
  if(V.sel>=0)select(V.sel); updHud();
});

function updHud(){
  const n=STARS.length, hosts=STARS.filter(s=>s.category==='planet-host').length;
  const labels={all:n+' stars',notable:STARS.filter(s=>s.notable).length+' notable',
                host:hosts+' planet hosts'};
  let reach='';
  if(V.engine>=0){ const e=ENGINES[V.engine];
    const cnt=STARS.filter(s=>s.name!=='Sun'&&fromSun(s)<=reachLy(e)).length;
    reach=`<br><span style="color:${e.color}">${e.name}: ${(e.cruise*100).toFixed(2)}% c &middot; `+
          `reaches ${reachLy(e).toFixed(1)} ly &middot; ${cnt} stars in ${fmtYr(V.horizon)}</span>`;
  }
  document.getElementById('hudsub').innerHTML =
    `${n} systems &middot; ${hosts} exoplanet hosts &middot; from <b style="color:#ffd35e">${STARS[V.ref].common_name}</b><br>`+
    `Showing: ${labels[V.filter]}`+reach;
}

resize(); updHud(); loop();
</script>
</body>
</html>'''

html = HTML.replace('__STARS_JSON__', json.dumps(rows, separators=(',',':')))
html = html.replace('__ENGINES_JSON__', json.dumps(ENGINES, separators=(',',':')))
open('star_map_3d.html','w',encoding='utf-8').write(html)
print('Wrote star_map_3d.html ('+str(len(html))+' bytes,', len(rows), 'stars)')

# extract <script> for a node syntax check
import re
m=re.search(r'<script>(.*?)</script>', html, re.S)
open('/tmp/check.js','w').write(m.group(1))
print('script extracted ->', len(m.group(1)), 'chars')
