"""
galaxy_sim.py  --  AI Galaxy Traveler, Phase 1 simulation engine
================================================================

A small, dependency-free engine for reasoning about an interstellar probe
travelling between real stars within ~100 light-years of the Sun.

What it does
------------
  * loads the curated real-star catalogue (stars_100ly.csv)
  * measures distances between any two stars (3D, light-years)
  * finds nearest neighbours
  * plans routes:
        - shortest total-distance path under a maximum single-hop limit
          ("the probe can only target a star within N ly of its current one")
  * estimates travel time with three increasingly realistic models:
        1. constant cruise speed (coordinate time)
        2. constant cruise speed + special-relativity ship clock
        3. constant-proper-acceleration relativistic rocket (accelerate to the
           midpoint, flip, decelerate) -- the realistic "go as fast as you can,
           then slow down to arrive" profile
  * rough propulsion sizing via the Tsiolkovsky rocket equation (mass ratio for
    a required delta-v given an exhaust velocity) -- a hook for Phase 2.

Everything here is ordinary physics. No warp drives, no wormholes. Units are SI
internally; distances are reported in light-years and times in years.

Run `python3 galaxy_sim.py` for a demonstration.
"""

from __future__ import annotations
import csv
import heapq
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import propulsion as prop

# ---- physical constants (SI) ----------------------------------------------
C = 299_792_458.0              # speed of light, m/s
LY = 9.460_730_472e15          # one light-year, m
YEAR = 31_557_600.0            # one Julian year, s
G0 = 9.806_65                  # standard gravity, m/s^2
AU = 1.495_978_707e11          # astronomical unit, m

CATALOG_FILE = "stars_100ly.csv"


# ===========================================================================
#  Catalogue
# ===========================================================================
class Catalog:
    def __init__(self, path: str | None = None):
        if path is None:
            # The catalogue ships in docs/ (it also feeds the dashboards);
            # fall back through the likely locations so `python code/*.py`
            # works from a clean checkout regardless of working directory.
            here = os.path.dirname(os.path.abspath(__file__))
            candidates = [
                os.path.join(here, CATALOG_FILE),
                os.path.join(here, "..", "docs", CATALOG_FILE),
                os.path.join(os.getcwd(), "docs", CATALOG_FILE),
            ]
            path = next((p for p in candidates if os.path.exists(p)),
                        candidates[0])
        self.stars: list[dict] = []
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                for k in ("ra_hours", "dec_deg", "dist_ly", "vmag",
                          "x", "y", "z"):
                    row[k] = float(row[k])
                row["notable"] = str(row["notable"]).lower() == "true"
                self.stars.append(row)
        self._index = {}
        for s in self.stars:
            self._index[s["name"].lower()] = s
            self._index[s["common_name"].lower()] = s

    def __len__(self):
        return len(self.stars)

    def get(self, name: str) -> dict:
        """Look up a star by catalogue name or common name (case-insensitive)."""
        key = name.strip().lower()
        if key in self._index:
            return self._index[key]
        # forgiving partial match
        hits = [s for s in self.stars
                if key in s["name"].lower() or key in s["common_name"].lower()]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            raise KeyError(f"No star matching {name!r}")
        raise KeyError(f"{name!r} is ambiguous: "
                       + ", ".join(h["name"] for h in hits[:6]))

    def names(self):
        return [s["name"] for s in self.stars]


# ===========================================================================
#  Geometry
# ===========================================================================
def distance(a: dict, b: dict) -> float:
    """3D distance between two stars, in light-years."""
    return math.dist((a["x"], a["y"], a["z"]), (b["x"], b["y"], b["z"]))


def distance_from_sun(star: dict) -> float:
    return math.sqrt(star["x"] ** 2 + star["y"] ** 2 + star["z"] ** 2)


def nearest(cat: Catalog, name: str, k: int = 5):
    """Return the k nearest stars to `name` as (star, distance_ly) pairs."""
    origin = cat.get(name)
    others = [(s, distance(origin, s)) for s in cat.stars if s is not origin]
    others.sort(key=lambda t: t[1])
    return others[:k]


def reachable_stars(cat, profile, horizon_yr):
    """Catalogue stars a flyby with `profile` reaches within horizon_yr, sorted."""
    out = []
    for st in cat.stars:
        if st["name"] == "Sun":
            continue
        t = prop.travel_time_yr(profile, distance_from_sun(st))
        if t <= horizon_yr:
            out.append((st, t))
    out.sort(key=lambda x: x[1])
    return out


# ===========================================================================
#  Routing  --  shortest path under a maximum single-hop distance
# ===========================================================================
def shortest_path(cat: Catalog, src: str, dst: str, max_hop_ly: float):
    """
    Dijkstra over the graph whose edges connect any two stars separated by no
    more than `max_hop_ly`. Models a probe that can only re-target a star
    within `max_hop_ly` of its current position (e.g. a navigation/comms or
    fuel-per-leg constraint). Returns (path_names, total_ly) or (None, inf).
    """
    s0, s1 = cat.get(src), cat.get(dst)
    idx = {s["name"]: i for i, s in enumerate(cat.stars)}
    start, goal = idx[s0["name"]], idx[s1["name"]]

    dist = [math.inf] * len(cat.stars)
    prev = [-1] * len(cat.stars)
    dist[start] = 0.0
    pq = [(0.0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == goal:
            break
        su = cat.stars[u]
        for v, sv in enumerate(cat.stars):
            if v == u:
                continue
            w = distance(su, sv)
            if w <= max_hop_ly and d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    if math.isinf(dist[goal]):
        return None, math.inf
    path, u = [], goal
    while u != -1:
        path.append(cat.stars[u]["name"])
        u = prev[u]
    path.reverse()
    return path, dist[goal]


# ===========================================================================
#  Travel-time models
# ===========================================================================
def cruise_time_coordinate(dist_ly: float, frac_c: float) -> float:
    """Years measured by an outside (Earth) observer at constant speed frac_c."""
    return dist_ly / frac_c


def cruise_time_ship(dist_ly: float, frac_c: float) -> float:
    """Years on the probe's own clock at constant speed (special relativity)."""
    return (dist_ly / frac_c) * math.sqrt(1.0 - frac_c ** 2)


def relativistic_rocket(dist_ly: float, accel_g: float):
    """
    Constant-proper-acceleration flight that accelerates to the half-way point
    then decelerates to arrive at rest (a "torchship" profile). Returns a dict
    with Earth time, ship time, and peak speed. This is the realistic upper
    bound for 'start slow, get as fast as possible, then brake to stop'.
    """
    a = accel_g * G0
    d_half = (dist_ly * LY) / 2.0
    # ship (proper) time for the first half: d = (c^2/a)(cosh(a*tau/c) - 1)
    tau_half = (C / a) * math.acosh(d_half * a / C ** 2 + 1.0)
    t_half = (C / a) * math.sinh(a * tau_half / C)       # coordinate time
    v_peak = C * math.tanh(a * tau_half / C)
    return {
        "earth_years": 2.0 * t_half / YEAR,
        "ship_years": 2.0 * tau_half / YEAR,
        "peak_frac_c": v_peak / C,
        "accel_g": accel_g,
    }


# ===========================================================================
#  Propulsion sizing (Phase-2 hook): Tsiolkovsky rocket equation
# ===========================================================================
def mass_ratio(delta_v_ms: float, exhaust_v_ms: float) -> float:
    """
    Wet/dry mass ratio needed for a given delta-v with a given exhaust velocity.
    delta_v = v_e * ln(m_wet/m_dry)  ->  m_wet/m_dry = exp(delta_v / v_e).
    A first sanity check on 'low mass is essential': high exhaust velocity
    (ion / nuclear-electric / fusion) keeps this ratio sane; chemical does not.
    """
    exponent = delta_v_ms / exhaust_v_ms
    if exponent > 700:          # math.exp overflows beyond ~709
        return math.inf
    return math.exp(exponent)


def kinetic_energy(mass_kg: float, frac_c: float) -> float:
    """Relativistic kinetic energy (Joules) to reach speed frac_c."""
    gamma = 1.0 / math.sqrt(1.0 - frac_c ** 2)
    return (gamma - 1.0) * mass_kg * C ** 2


# ===========================================================================
#  Demo
# ===========================================================================
def _demo():
    cat = Catalog()
    print(f"Loaded {len(cat)} stars within 100 ly.\n")

    print("Nearest stars to the Sun:")
    for s, d in nearest(cat, "Sun", 6):
        print(f"  {s['common_name']:<20} {d:6.2f} ly   {s['spectral']}")

    print("\nNearest stars to Sirius:")
    for s, d in nearest(cat, "Sirius", 4):
        print(f"  {s['common_name']:<20} {d:6.2f} ly")

    # Routing example: Sun -> Vega under a maximum single-hop limit.
    straight = distance_from_sun(cat.get('Vega'))
    print(f"\nRoute Sun -> Vega (straight-line {straight:.1f} ly):")
    for hop in (7.0, 12.0):
        path, total = shortest_path(cat, "Sun", "Vega", max_hop_ly=hop)
        if path:
            print(f"  max {hop:.0f} ly/hop: " + " -> ".join(path))
            print(f"     {len(path)-1} legs, {total:.1f} ly travelled")
        else:
            print(f"  max {hop:.0f} ly/hop: no route (stepping stones too sparse)")

    # Travel-time table to Proxima Centauri
    d = distance_from_sun(cat.get("Proxima Centauri"))
    print(f"\nTravel time to Proxima Centauri ({d:.3f} ly):")
    voyager = 17_000.0 / C            # Voyager 1 ~17 km/s, as fraction of c
    for label, f in [("Voyager-1 speed (17 km/s)", voyager),
                     ("1% c", 0.01), ("10% c", 0.10), ("20% c", 0.20)]:
        print(f"  {label:<28} {cruise_time_coordinate(d, f):>12,.0f} yr "
              f"(Earth)   {cruise_time_ship(d, f):>10,.1f} yr (ship)")

    print("\n  Constant-acceleration 'torchship' profiles (accelerate to "
          "midpoint, then brake):")
    for g in (0.01, 0.1, 1.0):
        r = relativistic_rocket(d, g)
        print(f"    {g:>4} g : {r['earth_years']:7.1f} yr Earth, "
              f"{r['ship_years']:7.1f} yr ship, peak {r['peak_frac_c']*100:5.1f}% c")

    # Propulsion sanity check
    print("\nPropulsion sanity check -- mass ratio to reach 10% c (one way):")
    dv = 0.10 * C
    for name, ve in [("Chemical (4.4 km/s)", 4_400),
                     ("Ion thruster (50 km/s)", 50_000),
                     ("Nuclear-electric (500 km/s)", 500_000),
                     ("Fusion (10,000 km/s)", 1.0e7)]:
        mr = mass_ratio(dv, ve)
        if math.isinf(mr):
            shown = "impossible (>1e300)"
        elif mr < 1e6:
            shown = f"{mr:.1f}"
        else:
            shown = f"{mr:.1e}"
        print(f"  {name:<30} mass ratio = {shown}")
    print("  (mass ratio = wet/dry mass; anything above ~20 is impractical -- "
          "this is why 'low mass + high exhaust velocity' is the whole game.)")

    # ---- Phase 2: three flyby propulsion concepts --------------------------
    print("\n=== Phase 2: three flyby engines (defaults = reference designs) ===")
    profs = prop.profiles()
    dprox = distance_from_sun(cat.get("Proxima Centauri"))
    dvega = distance_from_sun(cat.get("Vega"))
    head = f"{'Engine':<18}{'Cruise':>9}{'->Proxima':>12}{'->Vega':>11}{'reach<=100yr':>14}"
    print(head); print("  " + "-"*(len(head)-2))
    for p in profs:
        n100 = len(reachable_stars(cat, p, 100))
        print(f"{p['engine']:<18}{p['cruise_frac_c']*100:>7.2f}%c"
              f"{prop._fmt_years(prop.travel_time_yr(p, dprox)):>12}"
              f"{prop._fmt_years(prop.travel_time_yr(p, dvega)):>11}"
              f"{n100:>12} stars")
    print("  (reach<=100yr = catalogue stars a flyby reaches within a century)")
    print("  Run  python3 propulsion.py  for full mass / energy / fuel detail.")


if __name__ == "__main__":
    _demo()
