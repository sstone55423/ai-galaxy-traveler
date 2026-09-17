"""
engineering.py  --  AI Galaxy Traveler, Phase 6 (computational engineering)
===========================================================================

Turns the four first-order budgets of the engineering-closure paper into actual
numbers, with the reproduction demographics computed across the REAL 127-star
catalogue. Four models:

  1. mass_budget()    -- subsystem mass/power of a notional seed
  2. braking()        -- magnetic-sail deceleration against the ISM (ion density)
  3. reproduction()   -- R_eff = sum_i p_i V_i across the catalogue, as a
                         Galton-Watson branching process (extinction probability)
  4. closure()        -- closure ratio C, vitamin fraction, material/energy check
  5. rider()          -- an active seed riding an interstellar object at ~26 km/s
                         (roadmap paper, Sec. 12): crossing times, active window,
                         stellar-pass intervals, sunlight flux, dormant survival

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
N_H_TOTAL = 0.2e6                # local cloud hydrogen number density, m^-3 (~0.2 cm^-3, mostly neutral)
N_E = 0.07e6                     # local cloud electron/ion density, m^-3 (Slavin & Frisch 2008; Frisch et al. 2011)
RHO_ISM_TOTAL = N_H_TOTAL * M_P  # ~3.3e-22 kg/m^3 -- used by revisions before 2026-09-15
RHO_ION = N_E * M_P              # ~1.2e-22 kg/m^3 -- what a magnetic sail actually sweeps
RHO_ISM = RHO_ION                # default braking density: neutrals assumed uncoupled (roadmap paper, Sec. 9)
SIGMA = 5.670_374e-8             # Stefan-Boltzmann
U235_J_PER_KG = 8.2e13
ASTEROID_BELT_KG = 3.0e21        # ~Solar-System main-belt mass (order of mag)
AU = 1.495_978_707e11            # m
PC = 3.085_677_581e16            # m
SOLAR_CONST_W_M2 = 1361.0        # sunlight flux at 1 AU
CRUISE_YR_PER_LY = 665.0         # 450 km/s cruise: the 0.99/ly survival figure is per 665 yr


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


def root_dispatch(n_root=12, offspring=3, **legkw):
    """Demographics of the ROOT node (the Sun -- settlement zero in the roadmap
    paper), which exists with probability one and can dispatch n_root children
    rather than the `offspring` every later node attempts.  Returns the root's
    own R_eff over its n_root nearest targets, the probability that none of its
    children settles, and a first-order lineage-extinction probability
    q_lineage = prod_i (1 - s_i (1 - q_bar)), where q_bar is the mean
    per-node extinction probability of an ordinary node with `offspring`
    children (i.e. each surviving child founds a branch that dies with
    probability q_bar).  Mean-field: branches are treated as independent."""
    cat = gs.Catalog()
    stars = cat.stars
    pos = [(s["x"], s["y"], s["z"]) for s in stars]
    host_kw = {k: legkw[k] for k in ("V_host", "V_dwarf", "V_hostile") if k in legkw}
    leg_kw = {k: v for k, v in legkw.items() if k not in host_kw}
    sun = next(i for i, s in enumerate(stars) if s["name"] == "Sun")
    d = sorted(((math.dist(pos[sun], pos[j]), j) for j in range(len(stars)) if j != sun))
    s_list = [leg_survival(dist_ly, **leg_kw) * viability(stars[j], **host_kw)
              for dist_ly, j in d[:n_root]]
    q_bar = reproduction(offspring=offspring, **dict(legkw))["mean_extinction_prob"]
    q_lineage = 1.0
    for s in s_list:
        q_lineage *= (1.0 - s * (1.0 - q_bar))
    return {"n_root": n_root, "root_R_eff": sum(s_list),
            "p_no_child_settles": _extinction_prob(s_list),
            "q_bar_ordinary_node": q_bar, "q_lineage": q_lineage,
            "farthest_target_ly": d[n_root - 1][0]}


# ===========================================================================
# 3c. INTERSTELLAR-OBJECT RIDER  (roadmap paper, Sec. 12)
# ===========================================================================
def reactor_duration_yr(load_W_e, fuel_kg=16.5, efficiency=0.28, burnup=0.10,
                        j_per_kg=U235_J_PER_KG):
    """Years a fissile charge sustains a constant electric load -- the inverse
    of energy.reactor_fuel_kg (same efficiency / burn-up / J-per-kg).  With
    the canonical 16.5 kg U-235 charge (4 kW-e for 300 yr) this gives the
    subsystem budget paper's cruise endurances: ~8,000 yr at 150 W (standard
    K-research profile) and ~24,000 yr at 50 W (range-maximizer profile)."""
    return fuel_kg * j_per_kg * burnup * efficiency / load_W_e / YEAR


def dormant_survival(t_yr, cruise_surv_per_ly=0.99, yr_per_ly=CRUISE_YR_PER_LY):
    """Survival over t_yr at the vehicle paper's CRUISE figure, 0.99 per ly
    = per 665 yr at 450 km/s.  That figure is a dust-and-ageing figure for a
    bare seed in cruise; it does NOT apply to a rider buried in an interstellar
    object, whose ageing-only survival the series has no number for.  Used
    here only as an upper-structure illustration."""
    return cruise_surv_per_ly ** (t_yr / yr_per_ly)


def rider(v_kms=26.0, active_yr=None, fuel_kg=16.5, cruise_W=(150.0, 50.0),
          n_star_pc3=0.1, encounter_r_pc=(0.01, 0.1, 0.5, 1.0),
          crossing_au=(122.0, 1000.0, 2000.0, 1e5), flux_au=(10.0, 100.0, 1000.0),
          dormant_yr=(1e5, 1e6), late_wait_yr=5e5, late_r_pc=0.5,
          cruise_surv_per_ly=0.99, **legkw):
    """First-order numbers for a seed riding an interstellar object outbound
    from the Sun at v_kms (26 km/s: 'Oumuamua's hyperbolic excess speed).

    active_yr   -- active-window durations (yr).  None -> derived from fuel_kg
                   and cruise_W via reactor_duration_yr (8,000 / 24,000 yr).
    crossing_au -- radii whose crossing time at v is reported (heliopause 122 AU,
                   1,000 AU, inner Oort 2,000 AU, outer Oort 1e5 AU).
    encounter_r_pc -- stellar-pass radii; mean interval between passes within r
                   of a star = 1 / (n_star * pi r^2 * v)  (n_star in pc^-3).
    flux_au     -- sunlight flux radii (1361 W/m^2 at 1 AU, inverse square).
    dormant_yr  -- dormant-survival horizons at the CRUISE figure
                   cruise_surv_per_ly per 665 yr (see dormant_survival: a
                   dust-and-ageing cruise figure that does not apply to a
                   buried rider -- illustration only).
    late_wait_yr, late_r_pc -- the late-dispatch illustration: expected value
                   = P(pass within late_r_pc during late_wait_yr, taken as
                   min(1, expected passes)) x dormant_survival(late_wait_yr)
                   x the launch-braking-settlement product 0.9^3 (manufacture
                   already observed at settlement zero).  An
                   upper-structure illustration, not an estimate.
    """
    v = v_kms * 1000.0                                      # m/s
    v_pc_yr = v * YEAR / PC
    if active_yr is None:
        active_yr = tuple(reactor_duration_yr(W, fuel_kg=fuel_kg) for W in cruise_W)
    crossing = {au: au * AU / v / YEAR for au in crossing_au}
    window = {t: {"ly": v * t * YEAR / LY, "au": v * t * YEAR / AU} for t in active_yr}
    encounter = {r: 1.0 / (n_star_pc3 * math.pi * r * r * v_pc_yr) for r in encounter_r_pc}
    flux = {au: SOLAR_CONST_W_M2 / (au * au) for au in flux_au}
    dormant = {t: dormant_survival(t, cruise_surv_per_ly) for t in dormant_yr}
    late_interval = 1.0 / (n_star_pc3 * math.pi * late_r_pc ** 2 * v_pc_yr)
    p_pass = min(1.0, late_wait_yr / late_interval)
    s_dormant = dormant_survival(late_wait_yr, cruise_surv_per_ly)
    legkw.setdefault("p_make", 1.0)   # manufacture already observed at settlement zero
    p_legs = leg_survival(0.0, cruise_surv_per_ly=cruise_surv_per_ly, **legkw)
    return {"v_kms": v_kms, "active_yr": tuple(active_yr),
            "crossing_yr": crossing, "window": window,
            "encounter_interval_yr": encounter, "flux_W_m2": flux,
            "dormant_survival": dormant,
            "late_dispatch": {"wait_yr": late_wait_yr, "r_pc": late_r_pc,
                              "p_pass": p_pass, "dormant_survival": s_dormant,
                              "per_leg_product": p_legs,
                              "expected_value": p_pass * s_dormant * p_legs}}


def rider_link_budget(tx_W=100.0, tx_aperture_m=1.0, rx_aperture_m=100.0,
                      wavelength_m=1e-6, dist_ly=1.0):
    """First-order optical link from a rider to settlement zero: Airy half-angle
    1.22 lambda/D, uniform disc, receiver aperture rx_aperture_m.  Returns the
    received power and photon rate (roadmap paper Sec. 12)."""
    theta = 1.22 * wavelength_m / tx_aperture_m
    r_spot = theta * dist_ly * LY
    frac = (rx_aperture_m / 2.0) ** 2 / r_spot ** 2
    p_rx = tx_W * frac
    e_ph = 6.626e-34 * C / wavelength_m
    return {"received_W": p_rx, "photons_per_s": p_rx / e_ph, "spot_radius_m": r_spot}


def rider_reach(r_pc=(0.5, 1.0, 2.0, 3.0), v_release_kms=30.0, gaia_rate_per_myr_1pc=20.0,
                cruise_W=50.0, fuel_kg=16.5, cruise_surv_per_ly=0.99, **legkw):
    """Reach table for a rider's held seeds (roadmap paper Sec. 12).  For each
    reach radius: pass interval on the Gaia rate (Bailer-Jones et al. 2018:
    ~20 encounters within 1 pc per Myr, scaled as r^2), transit at v_release,
    extra cruise fuel at cruise_W (from the fuel model), survival over
    wait+transit at the CRUISE figure (see dormant_survival), and the expected
    value per seed = survival x launch-braking-settlement product."""
    legkw.setdefault("p_make", 1.0)
    p_legs = leg_survival(0.0, cruise_surv_per_ly=cruise_surv_per_ly, **legkw)
    kg_per_yr = fuel_kg / reactor_duration_yr(cruise_W, fuel_kg)
    rows = []
    for r in r_pc:
        interval = 1e6 / (gaia_rate_per_myr_1pc * r * r)
        transit = r * PC / (v_release_kms * 1e3) / YEAR
        surv = dormant_survival(interval + transit, cruise_surv_per_ly)
        rows.append({"r_pc": r, "pass_interval_yr": interval, "transit_yr": transit,
                     "extra_fuel_kg": kg_per_yr * transit, "survival": surv,
                     "ev_per_seed": surv * p_legs})
    return rows


ALPHA_EMITTERS = {  # (mass number, half-life yr, alpha energy MeV)
    "Pu-238": (238, 87.7, 5.59), "Am-241": (241, 432.0, 5.64), "Am-243": (243, 7370.0, 5.44),
    "U-233": (233, 1.59e5, 4.91), "Np-237": (237, 2.14e6, 4.96)}


def alpha_battery(te_efficiency=0.05, isotopes=ALPHA_EMITTERS):
    """Specific thermal power of long-lived alpha emitters and the mass per
    watt-electric at a thermoelectric efficiency (roadmap paper Sec. 12).
    Decay energies are the alpha energy only (daughters neglected)."""
    N_A, MEV = 6.022e23, 1.602e-13
    out = {}
    for name, (A, t_half, E) in isotopes.items():
        lam = math.log(2.0) / (t_half * YEAR)
        w_kg = lam * N_A / (A / 1000.0) * E * MEV
        out[name] = {"half_life_yr": t_half, "W_per_kg_thermal": w_kg,
                     "kg_per_We": 1.0 / (w_kg * te_efficiency)}
    return out


def fuel_from_rock(kg_fissile=250.0, u_ppb=8.0, th_ppb=30.0, u235_frac=0.0072,
                   rho_kg_m3=2000.0, grind_J_per_t=3.6e7, plant_W=5e8):
    """Rock mass needed to mine kg_fissile of U-235 from chondritic rock at
    u_ppb uranium (Lodders 2003: ~8 ppb U, ~30 ppb Th), versus the rock
    needed if all fertile U+Th is bred to fissile; body diameter at rho;
    comminution energy and time at plant_W (roadmap paper Sec. 12)."""
    rock_u235 = kg_fissile / (u_ppb * 1e-9 * u235_frac)
    rock_bred = kg_fissile / ((u_ppb + th_ppb) * 1e-9)
    def diam(m): return 2.0 * (3.0 * m / (4.0 * math.pi * rho_kg_m3)) ** (1.0 / 3.0)
    grind_J = rock_u235 / 1000.0 * grind_J_per_t
    return {"rock_kg_u235_mining": rock_u235, "body_m_u235": diam(rock_u235),
            "rock_kg_breeding": rock_bred, "body_m_breeding": diam(rock_bred),
            "breeding_advantage": rock_u235 / rock_bred,
            "grind_J": grind_J, "grind_yr_at_plant": grind_J / plant_W / YEAR}


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

    print("\n=== 2. BRAKING (magsail vs ISM ions, rho=%.2e kg/m^3; d = m/(2 rho A), speed-independent) ===" % RHO_ISM)
    for m in (1e3, 1e4):
        for R in (10, 30, 100):
            b = braking(m, R)
            tt = f"{b['time_yr']:,.0f} yr" if b['time_yr'] < 1e6 else f"{b['time_yr']/1e6:.1f} Myr"
            print(f"   {m:>6.0f} kg, {R:>3} km sail : stop in {tt:>10}  over {b['distance_ly']:6.3f} ly")
    print(f"   sail radius to stop a 1 t seed within 0.01 ly: "
          f"{sail_radius_for(1e3, 0.01):.0f} km")

    print("\n=== 3. REPRODUCTION: R_eff across the real 127-star catalogue ===")
    print("   (per-stage survival 0.9 each x cruise 0.99/ly; viability host=1.0/dwarf=0.7/hostile=0.2)")
    for off in (1, 2, 3, 4):
        r = reproduction(offspring=off)
        verdict = "EXPANDS" if r["mean_R_eff"] > 1 else "extinction-prone"
        print(f"   offspring={off}: mean R_eff = {r['mean_R_eff']:.2f}  "
              f"({r['frac_nodes_R_eff>1']*100:3.0f}% of nodes >1, mean extinction "
              f"prob {r['mean_extinction_prob']:.2f})  -> {verdict}")
    print("\n   Sensitivity to per-stage reliability (offspring=3):")
    for p in (0.80, 0.90, 0.95):
        r = reproduction(offspring=3, p_make=p, p_launch=p, p_brake=p, p_settle=p)
        print(f"     per-stage p={p:.2f}: mean R_eff = {r['mean_R_eff']:.2f}  "
              f"-> {'EXPANDS' if r['mean_R_eff']>1 else 'extinction-prone'}")
    print("   -> R_eff sits on a knife-edge: a few % per-stage failure flips the outcome.")

    print("\n=== 3b. ROOT DISPATCH (settlement zero; ordinary nodes at offspring=3) ===")
    print("   n_root  root_R_eff  P(no child settles)  q_lineage (mean-field)  farthest target")
    for nr in (3, 6, 12, 24):
        rd = root_dispatch(n_root=nr, offspring=3)
        print(f"   {nr:>6}  {rd['root_R_eff']:>10.2f}  {rd['p_no_child_settles']:>19.3f}  "
              f"{rd['q_lineage']:>22.3f}  {rd['farthest_target_ly']:>10.1f} ly")

    print("\n=== 3c. INTERSTELLAR-OBJECT RIDER (roadmap paper Sec. 12) ===")
    r_2000au = 2000.0 * AU / PC
    rr = rider(encounter_r_pc=(0.01, r_2000au, 0.1, 0.5, 1.0))
    print(f"   body outbound at {rr['v_kms']:.0f} km/s; 16.5 kg U-235 at 150 / 50 W -> "
          f"active {' / '.join(f'{t:,.0f}' for t in rr['active_yr'])} yr")
    print("   crossing times:")
    labels = {122.0: "heliopause (122 AU)", 1000.0: "1,000 AU",
              2000.0: "inner Oort cloud (2,000 AU)", 1e5: "outer Oort edge (1e5 AU)"}
    for au, t in rr["crossing_yr"].items():
        print(f"     {labels.get(au, f'{au:,.0f} AU'):<30} {t:>9,.0f} yr")
    print("   active-window reach:")
    for t, w in rr["window"].items():
        print(f"     {t:>7,.0f} yr : {w['ly']:.2f} ly = {w['au']:,.0f} AU")
    print("   stellar passes (n_star = 0.1 pc^-3; rate = n pi r^2 v):")
    for r, T in rr["encounter_interval_yr"].items():
        rl = "0.0097 pc (2,000 AU)" if r == r_2000au else f"{r:.2f} pc"
        tt = f"{T:,.0f} yr" if T < 1e6 else (f"{T/1e6:.1f} Myr" if T < 1e9 else f"{T/1e9:.1f} Gyr")
        print(f"     within {rl:<20} once per {tt:>12}")
    print("   sunlight flux: " + ", ".join(
        f"{F:.3g} W/m^2 at {au:,.0f} AU" for au, F in rr["flux_W_m2"].items()))
    print("   dormant survival at the CRUISE figure (0.99 per 665 yr; dust-and-ageing,")
    print("   does not apply to a buried rider): " + ", ".join(
        f"{s:.2g} over {t:.0e} yr" for t, s in rr["dormant_survival"].items()))
    ld = rr["late_dispatch"]
    print(f"   late dispatch (upper-structure illustration): P(pass within {ld['r_pc']} pc "
          f"in {ld['wait_yr']:.0e} yr) {ld['p_pass']:.2f} x dormant {ld['dormant_survival']:.1e} "
          f"x launch-brake-settle {ld['per_leg_product']:.2f} = {ld['expected_value']:.1e}")
    for d in (1.0, 2.0):
        lb = rider_link_budget(dist_ly=d)
        print(f"   link 100 W / 1 m -> 100 m at {d:.0f} ly: {lb['received_W']:.1e} W, "
              f"{lb['photons_per_s']:.1e} photons/s")

    print("\n=== 3d. RIDER PROVISIONING AND FUEL (roadmap paper Sec. 12 and Sec. 4) ===")
    print("   reach (release 30 km/s, Gaia 20/Myr within 1 pc, extra fuel at 50 W, survival at the CRUISE figure):")
    print(f"   {'r_pc':>5} {'pass every':>12} {'transit':>10} {'extra kg':>9} {'survival':>9} {'EV/seed':>8}")
    for row in rider_reach():
        print(f"   {row['r_pc']:5.1f} {row['pass_interval_yr']:12,.0f} {row['transit_yr']:10,.0f} "
              f"{row['extra_fuel_kg']:9.0f} {row['survival']:9.2f} {row['ev_per_seed']:8.2f}")
    e_charge = 16.5 * U235_J_PER_KG * 0.28 * 0.10
    print(f"   one charge = {e_charge:.1e} J: " + ", ".join(f"{e_charge/P/YEAR:,.0f} yr at {P:g} W" for P in (150, 10, 1)))
    print("   alpha batteries at 5% thermoelectric (kg per watt-electric):")
    for name, b in alpha_battery().items():
        print(f"     {name:7s} t1/2 {b['half_life_yr']:>9.3g} yr  {b['W_per_kg_thermal']:8.3g} W/kg  {b['kg_per_We']:9.3g} kg/We")
    for kg in (16.5, 250.0):
        fr = fuel_from_rock(kg)
        print(f"   {kg:5.1f} kg U-235 from chondrite: mine {fr['rock_kg_u235_mining']:.1e} kg rock (body ~{fr['body_m_u235']:,.0f} m, "
              f"grind {fr['grind_J']:.1e} J = {fr['grind_yr_at_plant']:.1f} yr at 500 MW); "
              f"breed {fr['rock_kg_breeding']:.1e} kg (~{fr['body_m_breeding']:,.0f} m), advantage {fr['breeding_advantage']:.0f}x")

    print("\n=== 4. CLOSURE (capability binds, not material or energy) ===")
    cl = closure()
    print(f"   closure ratio 0.97 -> vitamin fraction {cl['vitamin_fraction']*100:.0f}% "
          f"= {cl['vitamin_kg']:.0f} kg of carried parts per 1 t child")
    print(f"   material margin: a belt outmasses a child by {cl['material_margin_x']:.1e}x")
    print(f"   energy margin:   reactor over t_rep delivers {cl['energy_margin_x']:.1e}x "
          f"the construction energy")


if __name__ == "__main__":
    _demo()
