"""
energy.py  --  AI Galaxy Traveler, Phase 3: power + redundancy
==============================================================

Power and reliability model for an AI probe that NEVER STOPS and must run
untended for centuries, with only rare resource top-ups from a comet/asteroid.

It answers three questions for a given load + design life:
  1. Which power source can physically do it (radioisotope vs fission reactor),
     and how much fuel/isotope mass that takes (with decay / burn-up).
  2. How redundant the power-conversion system must be to keep meeting the load
     as units fail over time (k-of-N reliability), and why passive redundancy
     alone collapses over centuries -- so self-repair (the rare-ISRU tie-in) is
     what actually buys the mission.
  3. How little an interstellar "helium / ISM collector" contributes (so it
     stays a bonus, not the plan).

All ordinary physics: exponential radioactive decay, fission energy per kg,
binomial k-of-N reliability, steady-state availability with repair.
"""

from __future__ import annotations
import math

YEAR = 31_557_600.0
C = 299_792_458.0
MEV_J = 1.602_176_634e-13

# ---- radioisotope data: thermal specific power (W per gram), half-life (yr) --
ISOTOPES = {
    "Pu-238": {"w_per_g": 0.540, "half_life_yr": 87.7},
    "Am-241": {"w_per_g": 0.114, "half_life_yr": 432.2},
    "Sr-90":  {"w_per_g": 0.460, "half_life_yr": 28.8},
}
# ---- fission fuel: usable energy per kg fully fissioned -----------------------
U235_J_PER_KG = 8.2e13            # ~200 MeV per U-235 fission


# ===========================================================================
#  Source sizing
# ===========================================================================
def reactor_fuel_kg(load_W_e, years, efficiency=0.28, burnup=0.10,
                    j_per_kg=U235_J_PER_KG):
    """Fissile mass to supply a constant electric load for `years` (burn-up
    limited). Energy_thermal = load / eff; fuel = E_th / (j_per_kg * burnup)."""
    e_thermal = (load_W_e / efficiency) * years * YEAR
    return e_thermal / (j_per_kg * burnup)


def rtg_isotope_kg(load_W_e, at_year, isotope="Pu-238", efficiency=0.28):
    """Isotope mass so that, AFTER decay to `at_year`, electric output still
    meets the load. Shows why radioisotopes are brutal for kW over centuries."""
    iso = ISOTOPES[isotope]
    decay = 0.5 ** (at_year / iso["half_life_yr"])
    p_th_needed_now = (load_W_e / efficiency) / decay      # thermal W at launch
    grams = p_th_needed_now / iso["w_per_g"]
    return grams / 1000.0, p_th_needed_now                 # (kg, launch thermal W)


def source_electric_W(t_year, kind, p_e0, life_years=None, isotope="Pu-238",
                      efficiency=0.28):
    """Electric power available at year t.
       reactor: flat p_e0 until fuel life ends, then 0.
       rtg:     p_e0 decays with the isotope half-life."""
    if kind == "reactor":
        return p_e0 if (life_years is None or t_year <= life_years) else 0.0
    hl = ISOTOPES[isotope]["half_life_yr"]
    return p_e0 * 0.5 ** (t_year / hl)


# ===========================================================================
#  Redundancy:  k-of-N power-conversion units
# ===========================================================================
def unit_alive_prob(t_year, mtbf_yr, beta=1.0):
    """Single-unit survival. beta=1 -> exponential; beta>1 -> Weibull wear-out."""
    return math.exp(-((t_year / mtbf_yr) ** beta))


def unit_availability(mtbf_yr, mttr_yr):
    """Steady-state availability of a *repairable* unit (self-repair)."""
    return mtbf_yr / (mtbf_yr + mttr_yr)


def k_of_n(p, N, k):
    """Probability at least k of N independent units are up, each up w.p. p.
    Computed as 1 - P(<=k-1) with a stable pmf recurrence (no huge binomials)."""
    if k <= 0:
        return 1.0
    if k > N or p <= 0.0:
        return 0.0
    if p >= 1.0:
        return 1.0
    pmf = (1.0 - p) ** N           # i = 0
    cdf = pmf
    for i in range(1, k):          # k is small; sum the lower tail
        pmf *= (N - i + 1) / i * (p / (1.0 - p))
        cdf += pmf
    return max(0.0, 1.0 - cdf)


def meets_load_prob(t_year, N, k, mtbf_yr, beta=1.0, repair_mttr_yr=None):
    """Probability the converter bank still delivers >= k units at year t."""
    if repair_mttr_yr is not None:                 # self-repair -> availability
        p = unit_availability(mtbf_yr, repair_mttr_yr)
    else:
        p = unit_alive_prob(t_year, mtbf_yr, beta)
    return k_of_n(p, N, k)


def min_units_for(target_R, t_year, k, mtbf_yr, beta=1.0, repair_mttr_yr=None,
                  N_cap=2000):
    """Smallest N >= k giving reliability >= target_R at year t (or None)."""
    for N in range(k, N_cap + 1):
        if meets_load_prob(t_year, N, k, mtbf_yr, beta, repair_mttr_yr) >= target_R:
            return N
    return None


# ===========================================================================
#  Interstellar / "helium" collector  (his question, quantified)
# ===========================================================================
def ism_collector(area_km2=1.0, frac_c=0.12):
    """Mass swept from the local interstellar cloud per year, and the *ideal*
    D-He3 energy if every collected He-3 atom could be fused (a generous upper
    bound; real extraction needs in-flight isotope separation + micro-fusion)."""
    v = frac_c * C
    A = area_km2 * 1e6                              # m^2
    nH, nHe = 0.19e6, 0.015e6                        # atoms / m^3 (local ISM)
    nHe3 = nHe * 2e-4
    mH, mHe, mHe3 = 1.674e-27, 6.646e-27, 5.008e-27
    g = lambda n, m: n * v * A * m * YEAR * 1000.0   # grams / yr
    he3_atoms_yr = (nHe3 * v * A) * YEAR
    e_ideal_W = he3_atoms_yr * 18.35 * MEV_J / YEAR
    return {"H_g_yr": g(nH, mH), "He_g_yr": g(nHe, mHe), "He3_g_yr": g(nHe3, mHe3),
            "He3_ideal_W": e_ideal_W}


# ===========================================================================
#  Demo: the chosen design point -- ~4 kW electric for 300 years
# ===========================================================================
def _demo():
    LOAD, LIFE, EFF = 4000.0, 300.0, 0.28
    print(f"Design point: {LOAD/1000:.0f} kW electric, untended for {LIFE:.0f} years\n")

    print("1) Can the SOURCE physically do it?")
    u = reactor_fuel_kg(LOAD, LIFE, EFF)
    print(f"   Fission reactor : {u:6.1f} kg of U-235 "
          f"(thermal {LOAD/EFF/1000:.0f} kW, 10% burn-up) -- easily carried.")
    for iso in ("Pu-238", "Am-241"):
        kg, th = rtg_isotope_kg(LOAD, LIFE, iso, EFF)
        print(f"   {iso} RTG     : {kg:6.0f} kg of {iso} "
              f"(dumping {th/1000:.0f} kW of heat at launch) -- isotope is scarce.")
    print("   -> Verdict: only a fission reactor is mass-sane for kW / centuries.\n")

    print("2) Surviving untended: k-of-N power-conversion redundancy")
    k = math.ceil(LOAD / 1000.0)                     # 1 kW per converter unit
    print(f"   Need k={k} converters of 1 kW alive to meet {LOAD/1000:.0f} kW.")
    for mtbf in (30, 50, 100):
        nN = min_units_for(0.95, LIFE, k, mtbf)
        r12 = meets_load_prob(LIFE, 12, k, mtbf)
        msg = f"N={nN}" if nN else "impossible (>2000)"
        print(f"   MTBF {mtbf:>3} yr, NO repair : reliability@300yr with 12 units "
              f"= {r12:6.2%}; for 95% need {msg}")
    print("   -> Passive spares collapse over centuries (units almost surely fail).")
    print("   With SELF-REPAIR (rare-ISRU material, MTTR = 1 yr):")
    for mtbf in (30, 50, 100):
        a = unit_availability(mtbf, 1.0)
        r = meets_load_prob(LIFE, 12, k, mtbf, repair_mttr_yr=1.0)
        print(f"   MTBF {mtbf:>3} yr: unit availability {a:6.3%} -> "
              f"meets load with 12 units = {r:7.3%}")
    print("   -> Self-repair/reconfiguration is what actually buys centuries.\n")

    print("3) 'Helium collector' from the interstellar medium (1 km^2 scoop):")
    for fc in (0.12, 0.20):
        c = ism_collector(1.0, fc)
        print(f"   at {fc*100:.0f}% c: {c['H_g_yr']:5.0f} g/yr H, {c['He_g_yr']:4.0f} g/yr He, "
              f"{c['He3_g_yr']*1000:5.1f} mg/yr He-3  (<= {c['He3_ideal_W']:.0f} W ideal)")
    print("   -> Negligible as fuel; treat ISM + comet/asteroid as bonus material.")


if __name__ == "__main__":
    _demo()
