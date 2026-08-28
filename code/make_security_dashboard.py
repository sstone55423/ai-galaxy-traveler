"""Generate docs/security_attack_dashboard.html — the security paper's visual.

Targeted node removal on the real 127-star reachability graph: click-to-attack,
greedy-attack replay, articulation-point hardening, and the degree-attack
comparison. All JS computations are re-implementations of routing.py; this
generator embeds a verification block computed by routing.py itself so the
harness (and the page footer) can prove the two agree exactly.

Zero-CDN, single-file, offline. Run:  python code/make_security_dashboard.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import galaxy_sim as gs  # noqa: E402
import routing as rt     # noqa: E402

HOP = 15.0
SUN = 0


def python_reference():
    cat = gs.Catalog()
    G = rt.build_graph(cat, max_hop_ly=HOP)
    n = len(cat.stars)
    base = rt._sun_reachable(G, SUN, frozenset())

    aps = [{"i": i, "lost": len(lost)} for i, lost in rt.articulation_points(G, n, SUN)]

    def greedy(k, forbid=frozenset()):
        removed, seq = set(), []
        for _ in range(k):
            best_r, bi = None, None
            for i in range(1, n):
                if i in removed or i in forbid:
                    continue
                r = rt._sun_reachable(G, SUN, frozenset(removed | {i}))
                if best_r is None or r < best_r:
                    best_r, bi = r, i
            removed.add(bi)
            seq.append({"i": bi, "remaining": best_r})
        return seq

    g12 = greedy(12)
    six = {s["i"] for s in g12[:6]}
    nine = {a["i"] for a in aps}
    g_six = greedy(3, frozenset(six))
    g_nine = greedy(3, frozenset(nine))

    rand = {}
    for k in range(1, 21):
        rr = rt.random_removal_robustness(cat, k, n_trials=200, max_hop_ly=HOP)
        rand[k] = round(rr["mean_frac"], 4)

    deg = sorted(((len(G.get(i, [])), i) for i in range(1, n)), reverse=True)
    deg6 = [{"i": i, "deg": d,
             "cost": base - rt._sun_reachable(G, SUN, frozenset([i]))}
            for d, i in deg[:6]]

    stars = [{"name": s["name"], "x": round(s["x"], 3), "y": round(s["y"], 3),
              "z": round(s["z"], 3), "cat": s.get("category", "")}
             for s in cat.stars]
    return {
        "hop": HOP, "n": n, "baseline": base,
        "aps": aps, "greedy12": g12,
        "hardened6": sorted(six), "hardened9": sorted(nine),
        "greedy3_h6": g_six, "greedy3_h9": g_nine,
        "random_mean_frac": rand, "degree6": deg6, "stars": stars,
    }


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Targeted Removal — Deep Time AI</title>
<style>
  :root{ --bg0:#05060d; --panel:#0e1226; --line:rgba(120,150,220,.18); --txt:#dfe6ff;
         --dim:#93a0c8; --accent:#7fb3ff; --gold:#ffd35e; --green:#7af0a8; --red:#ff7a8a; }
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(1200px 800px at 60% -10%,#0b1022,#05060d);
    color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:18px;font-size:14px}
  h1{font-size:18px;margin:0 0 2px} .sub{color:var(--dim);font-size:12px;margin-bottom:14px}
  .sub a{color:var(--accent);text-decoration:none}
  .wrap{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:15px}
  #controls{width:300px;flex:none}
  #controls h2{font-size:11px;text-transform:uppercase;letter-spacing:.6px;color:var(--dim);margin:12px 0 8px}
  #controls h2:first-child{margin-top:0}
  button{background:#131a36;border:1px solid var(--line);color:var(--txt);border-radius:9px;
    padding:7px 11px;margin:0 6px 6px 0;cursor:pointer;font-size:12.5px}
  button:hover{border-color:var(--accent)}
  .tog{font-size:12.5px;margin:4px 0;color:var(--dim)} .tog input{margin-right:5px}
  #mapp{flex:1;min-width:560px}
  canvas{display:block;background:#080b18;border-radius:10px;width:100%;cursor:crosshair}
  #read{font-size:13px;margin-top:10px;line-height:1.6;min-height:84px}
  #read b{color:var(--gold)} #read .g{color:var(--green)} #read .r{color:var(--red)}
  .note{margin-top:8px;padding:9px 11px;border:1px dashed var(--line);border-radius:9px;color:var(--dim);font-size:12px;line-height:1.5}
  .note b{color:var(--txt)}
  .legend{font-size:11.5px;color:var(--dim);margin-top:6px}
  .legend span{margin-right:14px}
</style></head><body>
<h1>Targeted Removal: Attacking the Reachability Graph</h1>
<div class="sub">The security paper's central computation, live: remove stars from the real 127-star catalogue and watch
what the Sun can still reach. Companion to <a href="papers/security/">“Security Without Victory”</a> and
<a href="papers/routing/">“Three Dispatches”</a> · <a href="index.html">deep-time-ai.org</a></div>
<div class="wrap">
  <div id="controls" class="panel">
    <h2>Attack</h2>
    <button id="bGreedy1">greedy strike ×1</button>
    <button id="bGreedy6">run greedy ×6</button>
    <button id="bDeg">degree attack ×3</button>
    <button id="bReset">reset</button>
    <div class="tog" style="margin-top:6px">…or click any star on the map to remove / restore it.</div>
    <h2>Defense — harden nodes (unremovable)</h2>
    <div class="tog"><label><input type="radio" name="hard" value="0" checked> none</label></div>
    <div class="tog"><label><input type="radio" name="hard" value="6"> the six a greedy attacker reaches first</label></div>
    <div class="tog"><label><input type="radio" name="hard" value="9"> all nine articulation points</label></div>
    <h2>Show</h2>
    <div class="tog"><label><input type="checkbox" id="showAP" checked> articulation points (gold rings)</label></div>
    <div class="tog"><label><input type="checkbox" id="showEdges" checked> edges (15 ly hops)</label></div>
    <div class="note" id="verify"></div>
  </div>
  <div id="mapp" class="panel">
    <canvas id="cv" width="900" height="560"></canvas>
    <div class="legend">
      <span style="color:#7af0a8">● reachable from Sun</span>
      <span style="color:#ff7a8a">● cut off</span>
      <span style="color:#93a0c8">✕ removed</span>
      <span style="color:#ffd35e">◯ articulation point</span>
      <span style="color:#7fb3ff">▣ hardened</span>
    </div>
    <div id="read"></div>
    <div class="note"><b>What the numbers mean.</b> Three targeted removals cost more catalogue reachability than ten random
    failures — a 3–4× leverage multiplier at small k — but articulation-point leverage is finite: from the seventh strike
    onward every removal costs exactly one star. Hardening the six a greedy attacker reaches first only <i>halves</i> the
    advantage (nesting revives three more cut vertices); hardening all nine articulation points removes it entirely. And a
    degree-ordered attack achieves almost nothing here — the six highest-degree stars each cost exactly one — because a
    geometric graph has no hubs: its vulnerability lives in cut vertices, not in degree. Random-failure baseline: mean of
    200 trials per k (precomputed by routing.py and embedded).</div>
  </div>
</div>
<script>
"use strict";
const DATA = __DATA__;
// ---- graph (JS re-implementation of routing.py; verified against DATA at load) ----
function buildGraph(hop){
  const s = DATA.stars, n = s.length, adj = Array.from({length: n}, () => []);
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++){
    const dx = s[i].x - s[j].x, dy = s[i].y - s[j].y, dz = s[i].z - s[j].z;
    if (Math.sqrt(dx*dx + dy*dy + dz*dz) <= hop){ adj[i].push(j); adj[j].push(i); }
  }
  return adj;
}
function reachable(adj, removed){
  if (removed.has(0)) return new Set();
  const seen = new Set([0]), q = [0];
  while (q.length){
    const u = q.pop();
    for (const v of adj[u]) if (!seen.has(v) && !removed.has(v)){ seen.add(v); q.push(v); }
  }
  seen.delete(0); return seen;
}
function sunReach(adj, removed){ return reachable(adj, removed).size; }
function articulation(adj){
  const base = reachable(adj, new Set()), out = [];
  for (const i of base){
    const lost = base.size - 1 - sunReach(adj, new Set([i]));
    if (lost > 0) out.push({i, lost});
  }
  out.sort((a, b) => b.lost - a.lost || a.i - b.i);
  return out;
}
function greedyStep(adj, removed, forbid){
  let best = null, bi = -1;
  const n = adj.length;
  for (let i = 1; i < n; i++){
    if (removed.has(i) || forbid.has(i)) continue;
    const r = sunReach(adj, new Set([...removed, i]));
    if (best === null || r < best){ best = r; bi = i; }
  }
  return bi;
}
if (typeof window !== "undefined")
  window.__test = {buildGraph, sunReach, articulation, greedyStep, DATA};

// ---- state & UI ----
let adj, removed = new Set(), aps = [];
const $ = id => document.getElementById(id);
function hardenedSet(){
  const v = document.querySelector("input[name=hard]:checked").value;
  return new Set(v === "6" ? DATA.hardened6 : v === "9" ? DATA.hardened9 : []);
}
function project(){
  // fit x,y to canvas
  const s = DATA.stars, cv = $("cv");
  let minx = 1e9, maxx = -1e9, miny = 1e9, maxy = -1e9;
  for (const p of s){ minx = Math.min(minx, p.x); maxx = Math.max(maxx, p.x);
                      miny = Math.min(miny, p.y); maxy = Math.max(maxy, p.y); }
  const pad = 26, sc = Math.min((cv.width - 2*pad) / (maxx - minx), (cv.height - 2*pad) / (maxy - miny));
  return p => [pad + (p.x - minx) * sc, cv.height - pad - (p.y - miny) * sc];
}
let P;
function draw(){
  const cv = $("cv"), ctx = cv.getContext("2d");
  ctx.clearRect(0, 0, cv.width, cv.height);
  const hard = hardenedSet(), reach = reachable(adj, removed);
  if ($("showEdges").checked){
    ctx.strokeStyle = "rgba(120,150,220,.10)"; ctx.lineWidth = 1;
    for (let i = 0; i < adj.length; i++){
      if (removed.has(i)) continue;
      for (const j of adj[i]){
        if (j < i || removed.has(j)) continue;
        const a = P(DATA.stars[i]), b = P(DATA.stars[j]);
        ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
      }
    }
  }
  for (let i = 0; i < DATA.stars.length; i++){
    const [px, py] = P(DATA.stars[i]);
    if (removed.has(i)){
      ctx.strokeStyle = "#93a0c8"; ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.moveTo(px-4, py-4); ctx.lineTo(px+4, py+4);
      ctx.moveTo(px+4, py-4); ctx.lineTo(px-4, py+4); ctx.stroke();
      continue;
    }
    ctx.fillStyle = i === 0 ? "#ffd35e" : reach.has(i) ? "#7af0a8" : "#ff7a8a";
    ctx.beginPath(); ctx.arc(px, py, i === 0 ? 5 : 3, 0, Math.PI * 2); ctx.fill();
    if ($("showAP").checked && aps.some(a => a.i === i)){
      ctx.strokeStyle = "#ffd35e"; ctx.lineWidth = 1.4;
      ctx.beginPath(); ctx.arc(px, py, 7, 0, Math.PI * 2); ctx.stroke();
    }
    if (hard.has(i)){
      ctx.strokeStyle = "#7fb3ff"; ctx.lineWidth = 1.4;
      ctx.strokeRect(px - 6, py - 6, 12, 12);
    }
  }
  const sunP = P(DATA.stars[0]);
  ctx.fillStyle = "#ffd35e"; ctx.font = "11px sans-serif"; ctx.textAlign = "left";
  ctx.fillText("Sun", sunP[0] + 8, sunP[1] + 4);
  // readout
  const k = removed.size, r = sunReach(adj, removed), tot = DATA.n - 1;
  const lost = DATA.baseline - r;
  let html = "Removed: <b>" + k + "</b> · Sun reaches <b>" + r + "/" + tot + "</b> (" +
             (100 * r / tot).toFixed(1) + "%) · stars lost beyond the removals themselves: <b>" +
             Math.max(0, lost - k) + "</b>";
  if (k >= 1 && k <= 20){
    const randR = DATA.random_mean_frac[k] * tot;
    const tLoss = DATA.baseline - r, rLoss = DATA.baseline - randR;
    if (rLoss > 0.2){
      const mult = tLoss / rLoss;
      html += "<br>Random-failure baseline at k=" + k + ": " + randR.toFixed(1) +
              " reachable → your attack is <b class='" + (mult > 1.5 ? "r" : "g") + "'>" +
              mult.toFixed(2) + "×</b> as damaging as random loss.";
    }
  }
  $("read").innerHTML = html;
}
function reset(){ removed = new Set(); draw(); }
function init(){
  adj = buildGraph(DATA.hop);
  aps = articulation(adj);
  P = project();
  // self-verification against the embedded python reference
  const okBase = sunReach(adj, new Set()) === DATA.baseline;
  const okAP = aps.length === DATA.aps.length &&
    DATA.aps.every(a => aps.some(b => b.i === a.i && b.lost === a.lost));
  let okGreedy = true; const rm = new Set();
  for (const step of DATA.greedy12.slice(0, 6)){
    const pick = greedyStep(adj, rm, new Set());
    rm.add(pick);
    if (sunReach(adj, rm) !== step.remaining) okGreedy = false;
  }
  $("verify").innerHTML = (okBase && okAP && okGreedy)
    ? "<b style='color:#7af0a8'>✓ self-check passed:</b> this page's JS reproduces routing.py exactly — baseline " +
      DATA.baseline + "/" + (DATA.n - 1) + " reachable at " + DATA.hop + " ly, " + DATA.aps.length +
      " articulation points, and the greedy sequence, all match the embedded Python-computed reference."
    : "<b style='color:#ff7a8a'>✗ self-check FAILED — do not trust this page's numbers.</b>";
  $("bGreedy1").onclick = () => { const i = greedyStep(adj, removed, hardenedSet()); if (i >= 0) removed.add(i); draw(); };
  $("bGreedy6").onclick = () => { const h = hardenedSet();
    for (let s = 0; s < 6; s++){ const i = greedyStep(adj, removed, h); if (i >= 0) removed.add(i); } draw(); };
  $("bDeg").onclick = () => { DATA.degree6.slice(0, 3).forEach(d => removed.add(d.i)); draw(); };
  $("bReset").onclick = reset;
  document.querySelectorAll("input").forEach(i => i.addEventListener("change", draw));
  $("cv").addEventListener("click", ev => {
    const rect = $("cv").getBoundingClientRect();
    const mx = (ev.clientX - rect.left) * $("cv").width / rect.width;
    const my = (ev.clientY - rect.top) * $("cv").height / rect.height;
    let bi = -1, bd = 1e9;
    for (let i = 1; i < DATA.stars.length; i++){
      const [px, py] = P(DATA.stars[i]);
      const d = (px - mx) ** 2 + (py - my) ** 2;
      if (d < bd){ bd = d; bi = i; }
    }
    if (bi >= 0 && bd < 150){
      if (removed.has(bi)) removed.delete(bi);
      else if (!hardenedSet().has(bi)) removed.add(bi);
      draw();
    }
  });
  draw();
}
if (typeof document !== "undefined" && document.getElementById("cv")) init();
</script></body></html>
"""


def main():
    data = python_reference()
    html = TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":")))
    out = os.path.join(HERE, "..", "docs", "security_attack_dashboard.html")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print("wrote %s (%d bytes; baseline %d/%d, %d APs)" %
          (os.path.normpath(out), len(html), data["baseline"], data["n"] - 1, len(data["aps"])))
    print("greedy first six:", [s["remaining"] for s in data["greedy12"][:6]])
    print("hardened-6 greedy x3 remaining:", [s["remaining"] for s in data["greedy3_h6"]])
    print("hardened-9 greedy x3 remaining:", [s["remaining"] for s in data["greedy3_h9"]])
    print("degree-6 costs:", [d["cost"] for d in data["degree6"]])


if __name__ == "__main__":
    main()
