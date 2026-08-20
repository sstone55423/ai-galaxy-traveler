"""
engineering.py  --  AI Galaxy Traveler, Phase 6 (computational engineering)
===========================================================================

Turns the four first-order budgets of the engineering-closure paper into actual
numbers, with the reproduction demographics computed across the REAL 127-star
catalogue. Four models:

  1. mass_budget()    -- subsystem mass/power of a notional seed
  2. braking()        -- magnetic-sail deceleration against the ISM
  3. reproduction()   -- R_eff = sum_i p_i V_i across the catalogue, as a
                         Galton-Watson branching process (extinction probability)
  4. closure()        -- closure ratio C, vitamin fraction, material/energy check

All parameters are explicit and adjustable; the defaults are first-order proxies,
clearly labelled. Run `python3 engineering.py` for the demonstration.
"""
from __future__ import annotations
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import galaxy_sim as gs

# ---- constants ----
C = 299_792_458.0
LY = 9.460_730_472e15
YEAR = 31_557_600.0
M_P = 1.674e-27
RHO_ISM = 0.2e6 * M_P            # local ISM mass density ~0.2 atoms/cm^3
SIGMA = 5.670_374e-8             # Stefan-Boltzmann
U235_J_PER_KG = 8.2e13
ASTEROID_BELT_KG = 3.0e21        # ~Solar-System main-belt mass (order of mag)


# ===========================================================================
# 1. MASS & POWER BUDGET
# ===========================================================================
def mass_budget(payload_kg=200.0, rated_kW_thermal=14.0, reactor_alpha_kg_per_kW=8.0,
                radiator_T=400.0, radiator_areal_kg_m2=3.0, shielding_kg=400.0,
                sail_struct_kg=300.0, isru_plant_kg=2000.0, structure_frac=0.20):
    """First-order seed mass breakdown (kg). isru_plant_kg dominates a real seed;
    setting it small models a minimal bootstrap package, large a full factory.
    rated_kW_thermal is the reactor's rated THERMAL output (14 kW th -> 4 kW-e
    at ~28% conversion); reactor mass and the radiator's blackbody floor are
    both sized against it."""
    reactor = reactor_alpha_kg_per_kW * rated_kW_thermal
    fuel_kg = 16.5                                   # ~U-235 for 4 kW-e/300 yr
    rad_area = (rated_kW_thermal * 1000.0) / (0.9 * SIGMA * radiator_T**4)   # m^2 (blackbody floor)
    radiators = rad_area * radiator_areal_kg_m2
    subs = {"nuclear fuel": fuel_kg, "reactor+conversion": reactor,
            "radiators": radiators, "shielding": shielding_kg,
            "magsail structure": sail_struct_kg, "computation+payload": payload_kg,
            "ISRU+manufacturing plant": isru_plant_kg}
    core = sum(subs.values())
    subs["structure/integration"] = core * structure_frac
    total = sum(subs.values())
    subs["_total_kg"] = total
    subs["_radiator_area_m2"] = rad_area
    subs["_dominant"] = max((k for k in subs if not k.startswith("_")),
                            key=lambda k: subs[k])
    return subs


# ===========================================================================
# 2. BRAKING BUDGET  (magnetic sail vs ISM)
# ===========================================================================
def braking(seed_kg, sail_radius_km, v_frac_c=0.0015, rho=RHO_ISM):
    """Stopping distance d=m/(2 rho A) (speed-INDEPENDENT) and time t=m/(rho v A)."""
    A = math.pi * (sail_radius_km * 1000.0) ** 2
    v = v_frac_c * C
    d_m = seed_kg / (2.0 * rho * A)
    t_s = seed_kg / (rho * v * A)
    return {"distance_ly": d_m / LY, "time_yr": t_s / YEAR,
            "sail_area_m2": A, "decel_g": (rho * v * v * A / seed_kg) / 9.80665}


def sail_radius_for(seed_kg, max_distance_ly, rho=RHO_ISM):
    """Effective magsail radius (km) needed to stop within max_distance_ly."""
    A = seed_kg / (2.0 * rho * max_distance_ly * LY)
    return math.sqrt(A / math.pi) / 1000.0


# ===========================================================================
# 3. REPRODUCTION BUDGET  (R_eff across the real catalogue)
# ===========================================================================
def viability(star, V_host=1.0, V_dwarf=0.7, V_hostile=0.2):
    """Target viability V_i in [0,1] from catalogue proxies (resources + braking
    environment). Planet-hosts richer; giants/white dwarfs hostile/poor."""
    cat = star["category"]
    if cat in ("giant", "white-dwarf"):
        return V_hostile
    if cat == "planet-host":
        return V_host
    return V_dwarf


def leg_survival(dist_ly, p_make=0.9, p_launch=0.9, p_brake=0.9, p_settle=0.9,
                 cruise_surv_per_ly=0.99):
    """Probability a dispatched child survives the whole chain to settle."""
    return p_make * p_launch * p_brake * p_settle * (cruise_surv_per_ly ** dist_ly)


def _extinction_prob(success_probs):
    """Galton-Watson extinction prob for one node whose offspring each succeed
    independently: f(z)=prod_i (1 - s_i + s_i z); q = smallest fixed point."""
    q = 0.0
    for _ in range(2000):
        f = 1.0
        for s in success_probs:
            f *= (1.0 - s + s * q)
        if abs(f - q) < 1e-12:
            break
        q = f
    return q


def reproduction(offspring=2, **legkw):
    """Compute R_eff = sum over the `offspring` nearest targets of p_i V_i, for
    every catalogue node, plus the branching extinction probability. Returns
    aggregate statistics across the real 127-star catalogue."""
    cat = gs.Catalog()
    stars = cat.stars
    pos = [(s["x"], s["y"], s["z"]) for s in stars]
    n = len(stars)
    host_kw = {k: legkw.pop(k) for k in ("V_host", "V_dwarf", "V_hostile") if k in legkw}
    reffs, extincts = [], []
    for i in range(n):
        d = sorted(((math.dist(pos[i], pos[j]), j) for j in range(n) if j != i))
        targets = d[:offspring]
        s_list = []
        for dist_ly, j in targets:
            s = leg_survival(dist_ly, **legkw) * viability(stars[j], **host_kw)
            s_list.append(s)
        reffs.append(sum(s_list))
        extincts.append(_extinction_prob(s_list))
    mean_reff = sum(reffs) / n
    frac_above1 = sum(1 for r in reffs if r > 1.0) / n
    mean_ext = sum(extincts) / n
    return {"mean_R_eff": mean_reff, "frac_nodes_R_eff>1": frac_above1,
            "mean_extinction_prob": mean_ext, "offspring": offspring,
            "per_node_R_eff": reffs}


# ===========================================================================
# 4. CLOSURE BUDGET
# ===========================================================================
def closure(child_dry_kg=1000.0, closure_ratio=0.97, t_rep_yr=10_000.0,
            elec_kW=4.0, construct_energy_J_per_kg=5e8):
    """Vitamin fraction, vitamin mass, and the (comfortable) material & energy
    checks. construct_energy ~ refining+fabrication energy per kg of child.
    elec_kW is the ELECTRIC output available as process power (4 kW-e; the
    reactor's 14 kW rating is thermal) -- this reproduces the papers'
    canonical ~10^3 energy margin."""
    vitamin_frac = 1.0 - closure_ratio
    vitamin_kg = vitamin_frac * child_dry_kg
    material_margin = ASTEROID_BELT_KG / child_dry_kg
    energy_available = elec_kW * 1000.0 * t_rep_yr * YEAR
    energy_needed = construct_energy_J_per_kg * child_dry_kg
    return {"vitamin_fraction": vitamin_frac, "vitamin_kg": vitamin_kg,
            "material_margin_x": material_margin,
            "energy_margin_x": energy_available / energy_needed}


# ===========================================================================
#  Demo
# ===========================================================================
def _demo():
    print("=== 1. MASS & POWER BUDGET (reference seed) ===")
    mb = mass_budget()
    for k, v in mb.items():
        if not k.startswith("_"):
            print(f"   {k:<28} {v:8.0f} kg")
    print(f"   {'TOTAL':<28} {mb['_total_kg']:8.0f} kg   "
          f"(dominant: {mb['_dominant']}; radiator {mb['_radiator_area_m2']:.0f} m^2)")

    print("\n=== 2. BRAKING (magsail vs ISM; d = m/(2 rho A), speed-independent) ===")
    for m in (1e3, 1e4):
        for R in (10, 30, 100):
            b = braking(m, R)
            tt = f"{b['time_yr']:,.0f} yr" if b['time_yr'] < 1e6 else f"{b['time_yr']/1e6:.1f} Myr"
            print(f"   {m:>6.0f} kg, {R:>3} km sail : stop in {tt:>10}  over {b['distance_ly']:6.3f} ly")
    print(f"   sail radius to stop a 1 t seed within 0.01 ly: "
          f"{sail_radius_for(1e3, 0.01):.0f} km")

    print("\n=== 3. REPRODUCTION: R_eff across the real 127-star catalogue ===")
    print("   (per-leg survival 0.9 each x cruise 0.99/ly; viability host=1.0/dwarf=0.7/hostile=0.2)")
    for off in (1, 2, 3, 4):
        r = reproduction(offspring=off)
        verdict = "EXPANDS" if r["mean_R_eff"] > 1 else "extinction-prone"
        print(f"   offspring={off}: mean R_eff = {r['mean_R_eff']:.2f}  "
              f"({r['frac_nodes_R_eff>1']*100:3.0f}% of nodes >1, mean extinction "
              f"prob {r['mean_extinction_prob']:.2f})  -> {verdict}")
    print("\n   Sensitivity to per-leg reliability (offspring=3):")
    for p in (0.80, 0.90, 0.95):
        r = reproduction(offspring=3, p_make=p, p_launch=p, p_brake=p, p_settle=p)
        print(f"     per-leg p={p:.2f}: mean R_eff = {r['mean_R_eff']:.2f}  "
              f"-> {'EXPANDS' if r['mean_R_eff']>1 else 'extinction-prone'}")
    print("   -> R_eff sits on a knife-edge: a few % per-leg failure flips the outcome.")

    print("\n=== 4. CLOSURE (capability binds, not material or energy) ===")
    cl = closure()
    print(f"   closure ratio 0.97 -> vitamin fraction {cl['vitamin_fraction']*100:.0f}% "
          f"= {cl['vitamin_kg']:.0f} kg of carried parts per 1 t child")
    print(f"   material margin: a belt outmasses a child by {cl['material_margin_x']:.1e}x")
    print(f"   energy margin:   reactor over t_rep delivers {cl['energy_margin_x']:.1e}x "
          f"the construction energy")


if __name__ == "__main__":
    _demo()
