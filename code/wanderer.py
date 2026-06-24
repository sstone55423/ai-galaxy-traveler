"""
wanderer.py  --  AI Galaxy Traveler, Phase 4: the slow self-replicating wanderer
================================================================================

A von Neumann (self-replicating) probe fleet crawls between the real catalogue
stars at a slow, gravity-assist-navigable speed and copies itself at each stop.
Individual probes are slow; the FLEET grows exponentially.

Two replication policies:
  * one-shot (default): each colony fires one burst of `offspring` probes to the
    nearest UNCLAIMED stars, using a shared/coordinated claim list (each star is
    targeted once). A clean branching tree.
  * persistent (persistent=True): each colony keeps building probes every
    replication period and sends them to the next stars in its OWN precomputed
    nearest-list, with NO global knowledge of who else has settled where. Stars
    can therefore be visited redundantly -- the realistic cost of an
    uncoordinated swarm. We track probes launched and the redundant fraction.

Grounded in Freitas 1980 (replication ~1000 yr) and Hart/Tipler colonisation
timescales (galaxy in ~1 Myr at 0.1c, ~300 Myr slow).
"""

from __future__ import annotations
import heapq
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import galaxy_sim as gs


def simulate(speed_frac_c=0.0015, build_time_yr=1000.0, offspring=2,
             horizon_yr=10_000.0, start="Sun", persistent=False):
    cat = gs.Catalog()
    stars = cat.stars
    n = len(stars)
    idx = {s["name"]: i for i, s in enumerate(stars)}
    pos = [(s["x"], s["y"], s["z"]) for s in stars]
    sun = idx.get(start, 0)

    def d(i, j):
        return math.dist(pos[i], pos[j])

    nodes, edges = [], []

    if not persistent:
        # ---- one-shot, coordinated (shared claim list) ----------------------
        claimed = {sun}
        heap = [(0.0, sun, 0, -1)]
        while heap:
            t, si, gen, par = heapq.heappop(heap)
            if t > horizon_yr:
                continue
            nodes.append({"star_i": si, "common": stars[si]["common_name"],
                          "t": t, "gen": gen, "parent_i": par})
            t_ready = t + build_time_yr
            if t_ready > horizon_yr:
                continue
            cand = sorted((j for j in range(n) if j not in claimed),
                          key=lambda j: d(si, j))
            for j in cand[:offspring]:
                claimed.add(j)
                arrive = t_ready + d(si, j) / speed_frac_c
                edges.append({"from_i": si, "to_i": j, "depart": t_ready,
                              "arrive": arrive, "gen": gen + 1, "redundant": False})
                if arrive <= horizon_yr:
                    heapq.heappush(heap, (arrive, j, gen + 1, si))
    else:
        # ---- persistent, uncoordinated (per-colony nearest-list, no global) -
        nbr_cache = {}

        def nbr(i):
            if i not in nbr_cache:
                nbr_cache[i] = sorted((j for j in range(n) if j != i),
                                      key=lambda j: d(i, j))
            return nbr_cache[i]

        settled_t = [math.inf] * n
        # event: (time, kind, star, gen, ptr_or_parent); kind 'A'rrive / 'E'mit
        heap = [(0.0, "A", sun, 0, -1)]
        while heap:
            t, kind, si, gen, extra = heapq.heappop(heap)
            if t > horizon_yr:
                continue
            if kind == "A":
                if math.isinf(settled_t[si]):
                    settled_t[si] = t
                    nodes.append({"star_i": si, "common": stars[si]["common_name"],
                                  "t": t, "gen": gen, "parent_i": extra})
                    heapq.heappush(heap, (t + build_time_yr, "E", si, gen, 0))
                # else: redundant arrival -- already settled, nothing to do
            else:  # 'E' emit; extra = pointer into this colony's nearest-list
                order, ptr, launched = nbr(si), extra, 0
                while launched < offspring and ptr < len(order):
                    tgt = order[ptr]; ptr += 1; launched += 1
                    arrive = t + d(si, tgt) / speed_frac_c
                    edges.append({"from_i": si, "to_i": tgt, "depart": t,
                                  "arrive": arrive, "gen": gen + 1,
                                  "redundant": False})
                    if arrive <= horizon_yr:
                        heapq.heappush(heap, (arrive, "A", tgt, gen + 1, si))
                if ptr < len(order) and t + build_time_yr <= horizon_yr:
                    heapq.heappush(heap, (t + build_time_yr, "E", si, gen, ptr))
        # mark redundant: target already settled before this probe arrived
        for e in edges:
            e["redundant"] = settled_t[e["to_i"]] < e["arrive"] - 1e-9

    return {"speed_frac_c": speed_frac_c, "build_time_yr": build_time_yr,
            "offspring": offspring, "horizon_yr": horizon_yr,
            "persistent": persistent, "nodes": nodes, "edges": edges, "n_stars": n}


def summarize(sim):
    nodes, edges, H = sim["nodes"], sim["edges"], sim["horizon_yr"]
    cat = gs.Catalog()
    pos = {i: (s["x"], s["y"], s["z"]) for i, s in enumerate(cat.stars)}
    colonised = len(nodes)
    inflight = sum(1 for e in edges if e["arrive"] > H)
    probes = len(edges)
    redundant = sum(1 for e in edges if e.get("redundant"))
    max_gen = max((nd["gen"] for nd in nodes), default=0)
    far = max(nodes, key=lambda nd: math.dist((0, 0, 0), pos[nd["star_i"]]))
    far_d = math.dist((0, 0, 0), pos[far["star_i"]])
    return {"colonised": colonised, "inflight": inflight, "probes": probes,
            "redundant": redundant,
            "redundant_frac": (redundant / probes) if probes else 0.0,
            "max_gen": max_gen, "front_ly": far_d, "front_name": far["common"]}


def _fmt(y):
    return f"{y:,.0f} yr" if y < 1e6 else f"{y/1e6:,.1f} Myr"


def _demo():
    print("Self-replicating wanderer over 10,000 yr (cruise ~450 km/s, "
          "replication 1000 yr, 2 offspring)\n")
    one = summarize(simulate())
    per = summarize(simulate(persistent=True))
    print(f"  ONE-SHOT (coordinated): {one['colonised']} systems settled, "
          f"{one['probes']} probes, {one['redundant']} redundant "
          f"({one['redundant_frac']*100:.0f}%).")
    print(f"  PERSISTENT (no global knowledge): {per['colonised']} systems settled, "
          f"{per['probes']} probes, {per['redundant']} redundant "
          f"({per['redundant_frac']*100:.0f}%).")
    print("\n  Persistent colonies keep building probes every replication period and")
    print("  fire them at their nearest stars with no shared map -- so the same")
    print("  systems get hit repeatedly. Redundancy is the price of no coordination.")
    # show how redundancy grows with time as the catalogue saturates
    print("\n  Persistent redundancy vs horizon (450 km/s, 1000 yr):")
    for H in (10_000, 30_000, 100_000):
        s = summarize(simulate(horizon_yr=H, persistent=True))
        print(f"    {H:>7,} yr: {s['colonised']:>3} settled, {s['probes']:>5} probes, "
              f"{s['redundant_frac']*100:>4.0f}% redundant")


if __name__ == "__main__":
    _demo()
