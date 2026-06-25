"""
routing.py  --  AI Galaxy Traveler, fleet routing and coverage
=============================================================

Fleet routing and catalogue coverage for a self-replicating interstellar
probe lineage.  Builds on the 127-star catalogue and the R_eff demographic
model of engineering.py to ask: given R_eff > 1, how should a settled node
dispatch its offspring probes to maximise coverage of the catalogue, ensure
redundancy against dispatch failures, and recover from node loss?

Three models:
  1. graph analysis  -- reachability, connected components, articulation points
  2. coverage_prob() -- analytical redundancy formula P = 1-(1-p)^n
  3. simulate_expansion() -- Monte Carlo fleet expansion under dispatch strategies

Run `python3 routing.py` for the demonstration.
"""
from __future__ import annotations
import math
import collections
import heapq
import random
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import galaxy_sim as gs

# ---- physical constants ----
LY_M   = 9.460_730_472e15     # one light-year, metres
YEAR_S = 31_557_600.0          # one Julian year, seconds
CRUISE_KMS = 450.0             # canonical cruise speed, km/s
CRUISE_MS  = CRUISE_KMS * 1e3 # m/s


# ===========================================================================
# 1. REACHABILITY GRAPH
# ===========================================================================

def build_graph(cat, max_hop_ly=15.0):
    """
    Undirected adjacency list for the catalogue.
    Returns {star_idx: [(neighbor_idx, dist_ly), ...]} for pairs within max_hop_ly.
    """
    stars = cat.stars
    n = len(stars)
    pos = [(s["x"], s["y"], s["z"]) for s in stars]
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            d = math.dist(pos[i], pos[j])
            if d <= max_hop_ly:
                graph[i].append((j, d))
                graph[j].append((i, d))
    return graph


def reachable_from(graph, start_idx):
    """BFS from start_idx; returns frozenset of all reachable indices."""
    visited = {start_idx}
    q = collections.deque([start_idx])
    while q:
        u = q.popleft()
        for v, _ in graph[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
    return frozenset(visited)


def connected_components(graph, n):
    """List of frozensets, one per connected component."""
    seen = set()
    comps = []
    for i in range(n):
        if i not in seen:
            c = reachable_from(graph, i)
            comps.append(c)
            seen.update(c)
    return comps


def articulation_points(graph, n_stars, sun_idx):
    """
    Stars whose removal reduces the number of catalogue nodes reachable from
    sun_idx.  For each candidate removal, rebuilds a pruned graph and re-runs
    BFS.  O(n^2) but fine for n=127.  Returns a list of
      (star_idx, stars_lost: frozenset)
    sorted by descending stars_lost count.
    """
    base = reachable_from(graph, sun_idx)
    aps = []
    for rm in sorted(base):
        if rm == sun_idx:
            continue
        pruned = {i: [(v, d) for v, d in nbrs if v != rm]
                  for i, nbrs in graph.items() if i != rm}
        nr = reachable_from(pruned, sun_idx)
        lost = base - nr - {rm}
        if lost:
            aps.append((rm, frozenset(lost)))
    aps.sort(key=lambda t: -len(t[1]))
    return aps


def graph_summary(cat, max_hop_ly=15.0):
    """Return a dict of key graph statistics."""
    n = len(cat.stars)
    graph = build_graph(cat, max_hop_ly)
    sun_idx = next(i for i, s in enumerate(cat.stars) if s["name"] == "Sun")
    comps = connected_components(graph, n)
    sun_reach = reachable_from(graph, sun_idx)
    degrees = [len(graph[i]) for i in range(n)]
    aps = articulation_points(graph, n, sun_idx)
    return {
        "max_hop_ly": max_hop_ly,
        "n_stars": n,
        "n_components": len(comps),
        "largest_component": max(len(c) for c in comps),
        "sun_reachable": len(sun_reach),
        "sun_reachable_frac": (len(sun_reach) - 1) / (n - 1),
        "mean_degree": sum(degrees) / n,
        "n_articulation_points": len(aps),
        "articulation_points": aps,   # list of (idx, frozenset of lost indices)
    }


# ===========================================================================
# 2. COVERAGE PROBABILITY  (analytical)
# ===========================================================================

def per_dispatch_p(dist_ly, p_stage=0.9, n_stages=4, cruise_per_ly=0.99):
    """
    Probability a single dispatch to dist_ly survives the full mission chain.
    p = p_stage^n_stages * cruise_per_ly^dist_ly
    (n_stages=4: manufacture, launch, brake, settle; cruise reliability separate)
    """
    return (p_stage ** n_stages) * (cruise_per_ly ** dist_ly)


def coverage_prob(p, n):
    """P(at least one of n independent dispatches succeeds) = 1 - (1-p)^n."""
    return 1.0 - (1.0 - p) ** n


def dispatches_needed(p, target=0.95):
    """Minimum n such that coverage_prob(p, n) >= target."""
    for n in range(1, 200):
        if coverage_prob(p, n) >= target:
            return n
    return None


# ===========================================================================
# 3. FLEET EXPANSION SIMULATION  (Monte Carlo)
# ===========================================================================

def _viability(star):
    """Target viability proxy from stellar category (matches engineering.py)."""
    cat = star["category"]
    if cat in ("giant", "white-dwarf"):
        return 0.2
    if cat == "planet-host":
        return 1.0
    return 0.7


def simulate_expansion(cat, strategy="coverage", n_offspring=3, max_hop_ly=15.0,
                       p_stage=0.9, cruise_per_ly=0.99, tau_rep_yr=10_000.0,
                       t_silence_yr=5_000.0, max_time_yr=500_000.0, rng_seed=42):
    """
    Monte Carlo lineage expansion from the Sun across the catalogue.

    strategy: 'nearest'  -- dispatch to the n_offspring nearest unsettled targets
              'viability' -- dispatch to the n_offspring highest-viability targets
              'coverage'  -- prefer targets with fewer prior dispatches (gap-first)

    Returns dict with settled_count, coverage_frac, time_yr_to_90pct,
    time_yr_to_95pct, and per-star settlement times (events list).
    """
    rng_local = random.Random(rng_seed)
    stars = cat.stars
    n = len(stars)
    graph = build_graph(cat, max_hop_ly)
    sun_idx = next(i for i, s in enumerate(stars) if s["name"] == "Sun")

    settled = {sun_idx}
    dispatch_counts = collections.defaultdict(int)
    pq = []          # (arrival_yr, probe_id, source_idx, target_idx, dist_ly)
    probe_id = [0]

    def _dispatch(src, tgt, dist, t_now):
        transit = (dist * LY_M / CRUISE_MS) / YEAR_S
        heapq.heappush(pq, (t_now + transit, probe_id[0], src, tgt, dist))
        dispatch_counts[tgt] += 1
        probe_id[0] += 1

    def _choose(node_idx, n_off):
        cands = [(v, d) for v, d in graph[node_idx] if v not in settled]
        if not cands:
            return []
        if strategy == "nearest":
            cands.sort(key=lambda t: t[1])
        elif strategy == "viability":
            cands.sort(key=lambda t: (-_viability(stars[t[0]]), t[1]))
        elif strategy == "coverage":
            cands.sort(key=lambda t: (dispatch_counts.get(t[0], 0), t[1]))
        else:
            raise ValueError(f"Unknown strategy {strategy!r}")
        # Cap at 3 total dispatches per target to avoid over-concentration
        out = []
        for v, d in cands:
            if len(out) >= n_off:
                break
            if dispatch_counts.get(v, 0) < 3:
                out.append((v, d))
        return out

    # Initial dispatch from Sun
    for tgt, d in _choose(sun_idx, n_offspring):
        _dispatch(sun_idx, tgt, d, 0.0)

    events = [(0.0, stars[sun_idx]["name"])]
    t90 = None
    t95 = None

    while pq:
        arr, _pid, src, tgt, dist = heapq.heappop(pq)
        if arr > max_time_yr:
            break
        if tgt in settled:
            continue
        p = per_dispatch_p(dist, p_stage, 4, cruise_per_ly) * _viability(stars[tgt])
        if rng_local.random() < p:
            settled.add(tgt)
            events.append((arr, stars[tgt]["name"]))
            cov = (len(settled) - 1) / (n - 1)
            if t90 is None and cov >= 0.90:
                t90 = arr
            if t95 is None and cov >= 0.95:
                t95 = arr
            for new_tgt, new_d in _choose(tgt, n_offspring):
                _dispatch(tgt, new_tgt, new_d, arr + tau_rep_yr)
        else:
            # Failure: source re-dispatches after T_silence if still active
            if src in settled and arr + t_silence_yr < max_time_yr:
                _dispatch(src, tgt, dist, arr + t_silence_yr)

    return {
        "strategy": strategy,
        "settled_count": len(settled) - 1,
        "coverage_frac": (len(settled) - 1) / (n - 1),
        "time_yr_to_90pct": t90,
        "time_yr_to_95pct": t95,
        "events": events,
    }


def run_trials(cat, strategy, n_trials=30, **kwargs):
    """Run simulate_expansion n_trials times; return aggregate statistics."""
    results = [simulate_expansion(cat, strategy=strategy, rng_seed=s, **kwargs)
               for s in range(n_trials)]
    covs  = [r["coverage_frac"] for r in results]
    t90s  = [r["time_yr_to_90pct"] for r in results if r["time_yr_to_90pct"]]
    t95s  = [r["time_yr_to_95pct"] for r in results if r["time_yr_to_95pct"]]
    return {
        "strategy": strategy,
        "n_trials": n_trials,
        "mean_coverage": sum(covs) / n_trials,
        "min_coverage": min(covs),
        "mean_t90_yr": sum(t90s) / len(t90s) if t90s else None,
        "n_reach_90pct": len(t90s),
        "mean_t95_yr": sum(t95s) / len(t95s) if t95s else None,
        "n_reach_95pct": len(t95s),
    }


# ===========================================================================
# Demo
# ===========================================================================
def _demo():
    # The CSV lives in docs/ relative to the repo root; try that first.
    _here = os.path.dirname(os.path.abspath(__file__))
    _csv  = os.path.join(_here, "..", "docs", "stars_100ly.csv")
    cat = gs.Catalog(_csv if os.path.exists(_csv) else None)
    stars = cat.stars
    n = len(stars)
    sun_idx = next(i for i, s in enumerate(stars) if s["name"] == "Sun")

    print(f"Catalogue: {n} stars\n")

    # ---- graph connectivity ----
    print("=== 1. REACHABILITY GRAPH ===")
    for h in (8.0, 10.0, 12.0, 15.0, 20.0):
        gs_data = graph_summary(cat, h)
        n_ap = gs_data["n_articulation_points"]
        print(f"  hop={h:4.1f} ly: {gs_data['n_components']:2d} components  "
              f"Sun reaches {gs_data['sun_reachable']:3d}/{n-1} "
              f"({gs_data['sun_reachable_frac']*100:.0f}%)  "
              f"mean_degree={gs_data['mean_degree']:.1f}  "
              f"APs={n_ap}")

    print("\n  Articulation points at hop=15 ly:")
    gs15 = graph_summary(cat, 15.0)
    for idx, lost in gs15["articulation_points"]:
        lost_names = [stars[i]["name"] for i in sorted(lost)]
        print(f"    {stars[idx]['name']:<30} isolates {len(lost)} star(s): "
              f"{', '.join(lost_names)}")

    # ---- coverage probability ----
    print("\n=== 2. COVERAGE PROBABILITY (analytical) ===")
    print("  p_stage=0.9 x4, cruise=0.99/ly")
    print(f"  {'dist_ly':>7}  {'p_disp':>6}  {'n=1':>6}  {'n=2':>6}  "
          f"{'n=3':>6}  {'n=4':>6}  n_needed(p>=0.95)")
    for d in (4.25, 8.0, 15.0, 20.0, 40.0, 64.5):
        p = per_dispatch_p(d)
        n_need = dispatches_needed(p, 0.95)
        print(f"  {d:7.2f}  {p:6.3f}  "
              f"{coverage_prob(p,1):6.3f}  {coverage_prob(p,2):6.3f}  "
              f"{coverage_prob(p,3):6.3f}  {coverage_prob(p,4):6.3f}  "
              f"{n_need}")

    # ---- strategy comparison ----
    print("\n=== 3. FLEET EXPANSION SIMULATION (hop=20 ly, n_off=3, 30 trials) ===")
    for strat in ("nearest", "viability", "coverage"):
        r = run_trials(cat, strat, n_trials=30, max_hop_ly=20.0)
        t90str = (f"{r['mean_t90_yr']/1000:.0f} kyr ({r['n_reach_90pct']}/30)"
                  if r["mean_t90_yr"] else f"never ({r['n_reach_90pct']}/30)")
        print(f"  {strat:<10}: mean_coverage={r['mean_coverage']*100:.0f}%  "
              f"min={r['min_coverage']*100:.0f}%  t90={t90str}")

    # ---- offspring count ----
    print("\n=== 4. OFFSPRING COUNT (coverage strategy, hop=20 ly, 30 trials) ===")
    for off in (1, 2, 3, 4):
        r = run_trials(cat, "coverage", n_trials=30, max_hop_ly=20.0,
                       n_offspring=off)
        t90str = (f"{r['mean_t90_yr']/1000:.0f} kyr ({r['n_reach_90pct']}/30)"
                  if r["mean_t90_yr"] else f"never ({r['n_reach_90pct']}/30)")
        print(f"  n_off={off}: mean_coverage={r['mean_coverage']*100:.0f}%  "
              f"t90={t90str}")


if __name__ == "__main__":
    _demo()
