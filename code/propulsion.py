"""
propulsion.py  --  AI Galaxy Traveler, Phase 2 (flyby models)
=============================================================

End-to-end, physics-based models of the three propulsion concepts, sized for a
FLYBY mission (accelerate, then coast past the target -- no braking). Each model
returns a common profile dict so the engine and the 3D map can consume them
uniformly.

Reference designs (defaults are anchored to real, published studies):
  * Laser sail   -> Breakthrough Starshot (100 GW array, ~1 g sail+chip, 4x4 m,
                    ~0.2c).                          [breakthroughinitiatives.org]
  * Fusion rocket-> Project Daedalus (D/He-3 inertial-confinement fusion,
                    ve ~10,000 km/s, two stages, 0.12c, 50,000 t fuel for a
                    450 t payload).                  [British Interplanetary Soc.]
  * Nuclear-electric -> reactor + advanced ion drive (ve ~100 km/s). Honest
                    result: a slow-boat (millennia), whose real value is power,
                    steering and longevity, not raw speed.

All physics here is ordinary: radiation pressure with diffraction-limited beam
fall-off and relativistic Doppler; the relativistic rocket equation; the
Tsiolkovsky equation with a reactor mass penalty. No science fiction.
"""

from __future__ import annotations
import math

# ---- constants (SI) -------------------------------------------------------
C = 299_792_458.0
LY = 9.460_730_472e15
YEAR = 31_557_600.0
G0 = 9.806_65
AU = 1.495_978_707e11

# Engine display colours (used by the 3D map)
COLORS = {"Laser sail": "#5ad1ff", "Fusion rocket": "#ff9d5a",
          "Nuclear-electric": "#b6ff7a"}


# ===========================================================================
#  1. Laser sail  (beam-driven light sail, no onboard propellant)
# ===========================================================================
def laser_sail(total_mass_g=1.0, laser_power_W=100e9, array_diameter_m=10_000.0,
               sail_diameter_m=4.0, wavelength_m=1.06e-6, reflectivity=1.0,
               design_cap_frac_c=0.20):
    """
    Numerically integrate a relativistic light sail pushed by a phased laser
    array. Radiation-pressure force F = 2 P R / c, reduced by:
      * diffraction: once the sail passes the focusing distance
        z_focus = D_array * D_sail / (2 lambda), the array can no longer hold the
        spot on the sail and intercepted power falls as (z_focus / z)^2;
      * relativistic Doppler: as the sail recedes at beta, the force drops by
        (1 - beta)/(1 + beta).
    The laser shuts off at the design speed (default 0.2c). Flyby only -- a bare
    sail cannot decelerate.
    """
    m = total_mass_g / 1000.0
    R = reflectivity
    z_focus = array_diameter_m * sail_diameter_m / (2.0 * wavelength_m)
    cap = design_cap_frac_c * C
    F0 = 2.0 * laser_power_W * R / C            # initial force, N
    dt, z, p, t, e_laser = 0.05, 0.0, 0.0, 0.0, 0.0
    capped = False
    while t < 3600.0:                            # safety: <= 1 hour of firing
        gamma = math.sqrt(1.0 + (p / (m * C)) ** 2)
        v = p / (gamma * m)
        if v >= cap:
            capped = True
            break
        beam = 1.0 if z <= z_focus else (z_focus / z) ** 2
        if beam < 1e-4:                          # beam too weak to matter
            break
        beta = v / C
        F = F0 * beam * (1.0 - beta) / (1.0 + beta)
        p += F * dt
        z += v * dt
        e_laser += laser_power_W * dt            # energy the array expends
        t += dt
    gamma = math.sqrt(1.0 + (p / (m * C)) ** 2)
    v = p / (gamma * m)
    sail_ke = (gamma - 1.0) * m * C ** 2
    return {
        "engine": "Laser sail",
        "cruise_frac_c": v / C,
        "accel_time_yr": t / YEAR,
        "accel_dist_ly": z / LY,
        "peak_accel_g": (F0 / m) / G0,
        "launch_mass_kg": m,
        "energy_J": e_laser,
        "decelerates": False,
        "extra": {"reached_design_speed": capped,
                  "focus_distance_AU": z_focus / AU,
                  "sail_kinetic_J": sail_ke,
                  "beam_efficiency": sail_ke / e_laser if e_laser else 0.0},
        "notes": ("Propellant-less; energy stays on the ground. Cannot brake -- "
                  "seconds at the target. Needs a ~100 GW array held on a "
                  "gram-scale sail to within metres over ~0.1 AU."),
    }


# ===========================================================================
#  2. Fusion rocket  (Project Daedalus design point, scaled to payload)
# ===========================================================================
def fusion_rocket(payload_t=450.0, exhaust_v_ms=1.0e7, cruise_frac_c=0.12,
                  fuel_t=50_000.0, dry_t=2_700.0, burnup=0.15,
                  he3_fraction=0.40, accel_time_yr=3.8):
    """
    Anchored to Project Daedalus: a two-stage D/He-3 inertial-confinement fusion
    rocket. Cruise speed (0.12c) is the published design value -- two-stage
    staging is what lifts it above the ~0.094c a single stage gives at this mass
    ratio. Masses scale linearly with payload from the 450 t reference. Energy is
    the fusion energy released (D/He-3 ~3.5e14 J per kg reacted x burn-up).
    """
    scale = payload_t / 450.0
    fuel_t *= scale
    dry_t *= scale
    fuel_kg = fuel_t * 1000.0
    total_t = payload_t + dry_t + fuel_t
    e_fusion = fuel_kg * burnup * 3.5e14          # J
    # accel distance: 0 -> cruise over accel_time, average speed ~ cruise/2
    accel_dist_ly = 0.5 * cruise_frac_c * accel_time_yr
    # implied mass ratio for reference
    mr = total_t / (payload_t + dry_t)
    return {
        "engine": "Fusion rocket",
        "cruise_frac_c": cruise_frac_c,
        "accel_time_yr": accel_time_yr,
        "accel_dist_ly": accel_dist_ly,
        "peak_accel_g": (cruise_frac_c * C) / (accel_time_yr * YEAR) / G0,
        "launch_mass_kg": total_t * 1000.0,
        "energy_J": e_fusion,
        "decelerates": False,
        "extra": {"payload_t": payload_t, "fuel_t": fuel_t,
                  "he3_t": fuel_t * he3_fraction, "dry_t": dry_t,
                  "mass_ratio": mr, "exhaust_v_kms": exhaust_v_ms / 1000.0},
        "notes": ("Carries its power source. ~{:.0f} t of fusion fuel (incl. "
                  "~{:.0f} t of scarce helium-3) per {:.0f} t of payload."
                  ).format(fuel_t, fuel_t * he3_fraction, payload_t),
    }


# ===========================================================================
#  3. Nuclear-electric  (reactor + advanced ion drive)
# ===========================================================================
def nuclear_electric(payload_kg=1000.0, exhaust_v_ms=1.0e5, mass_ratio=20.0,
                     elec_power_MW=10.0, efficiency=0.70,
                     reactor_alpha_kg_per_kW=5.0):
    """
    Fission (or fusion) reactor driving an ion/plasma thruster. Still a rocket:
    delta-v = ve * ln(mass_ratio), but ve is only ~100 km/s, so cruise speed is
    a fraction of a percent of c. The reactor is dead weight carried the whole
    way (specific mass alpha, kg/kW), which caps the practical mass ratio. Burn
    time t = M_prop / mdot, with mdot = 2*eta*P / ve^2.
    """
    dv = exhaust_v_ms * math.log(mass_ratio)       # non-relativistic is fine
    P = elec_power_MW * 1e6
    reactor_kg = reactor_alpha_kg_per_kW * elec_power_MW * 1000.0
    dry_kg = payload_kg + reactor_kg
    prop_kg = dry_kg * (mass_ratio - 1.0)
    m0 = dry_kg * mass_ratio
    mdot = 2.0 * efficiency * P / exhaust_v_ms ** 2
    t_burn = prop_kg / mdot                        # s
    e_elec = P * t_burn
    cruise = dv / C
    return {
        "engine": "Nuclear-electric",
        "cruise_frac_c": cruise,
        "accel_time_yr": t_burn / YEAR,
        "accel_dist_ly": 0.5 * cruise * (t_burn / YEAR),
        "peak_accel_g": (2 * efficiency * P / exhaust_v_ms / m0) / G0,
        "launch_mass_kg": m0,
        "energy_J": e_elec,
        "decelerates": False,
        "extra": {"delta_v_kms": dv / 1000.0, "exhaust_v_kms": exhaust_v_ms / 1000.0,
                  "reactor_t": reactor_kg / 1000.0, "propellant_t": prop_kg / 1000.0,
                  "elec_power_MW": elec_power_MW},
        "notes": ("Best for power, steering and decade-to-century longevity, not "
                  "raw speed. Cruise is a fraction of a percent of c -- a "
                  "slow-boat to the stars."),
    }


# ===========================================================================
#  Shared helpers
# ===========================================================================
def profiles():
    """Return the three default flyby profiles, fastest first."""
    return [laser_sail(), fusion_rocket(), nuclear_electric()]


def travel_time_yr(profile, dist_ly):
    """Total flyby time (years) to a target at dist_ly: accelerate then coast."""
    coast = max(0.0, dist_ly - profile["accel_dist_ly"])
    return profile["accel_time_yr"] + coast / profile["cruise_frac_c"]


def _fmt_years(y):
    if y < 1.0:
        return "<1 yr"
    if y < 1000:
        return f"{y:,.0f} yr"
    if y < 1e6:
        return f"{y/1e3:,.1f} kyr"
    return f"{y/1e6:,.1f} Myr"

def _fmt_mass(kg):
    if kg < 1.0:
        return f"{kg*1000:,.0f} g"
    if kg < 1e6:
        return f"{kg:,.0f} kg"
    return f"{kg/1e3:,.0f} t"


if __name__ == "__main__":
    print("Flyby propulsion profiles (defaults anchored to reference designs)\n")
    hdr = f"{'Engine':<18}{'Cruise':>9}{'Accel':>11}{'Peak g':>10}{'Launch mass':>15}{'Energy (J)':>13}"
    print(hdr); print("-" * len(hdr))
    for p in profiles():
        print(f"{p['engine']:<18}"
              f"{p['cruise_frac_c']*100:>7.2f}%c"
              f"{_fmt_years(p['accel_time_yr']):>11}"
              f"{p['peak_accel_g']:>9.2g}g"
              f"{_fmt_mass(p['launch_mass_kg']):>15}"
              f"{p['energy_J']:>13.2e}")
    print("\nFlyby time to representative targets:")
    targets = [("Proxima Centauri", 4.246), ("Barnard's Star", 5.963),
               ("Sirius", 8.601), ("Tau Ceti", 11.912), ("Vega", 25.04)]
    row = f"{'Target':<20}{'dist':>8}" + "".join(f"{e:>16}" for e in
            ("Laser sail", "Fusion rocket", "Nuclear-electric"))
    print(row); print("-" * len(row))
    profs = profiles()
    for name, d in targets:
        line = f"{name:<20}{d:>6.1f}ly"
        for p in profs:
            line += f"{_fmt_years(travel_time_yr(p, d)):>16}"
        print(line)
