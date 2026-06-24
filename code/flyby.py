"""
flyby.py  --  AI Galaxy Traveler, Phase 4 sketch: stellar boomerang + scoop
===========================================================================

Assesses the idea of swinging close to stars en route to (a) "boomerang" off
them with a gravity assist and (b) deploy a scoop briefly while deep in the
denser gas near the star.

Both maneuvers are REAL (gravity assists and Oberth burns are how we fly the
solar system; magnetic-sail braking against a stellar wind is a studied idea).
The only science-fiction part is doing them at relativistic cruise speed. This
module quantifies exactly where the line is.

The governing fact: a flyby can bend your path by a large angle ONLY if your
speed is below the star's surface escape velocity. Go faster and the
gravitational "focal point" falls inside the star -- you'd have to pass through
it to turn. So fast probes can't be steered by ordinary stars; slow ones can.
"""

from __future__ import annotations
import math

C = 299_792_458.0
G = 6.674e-11
Msun = 1.989e30
Rsun = 6.957e8
Lsun = 3.828e26
AU = 1.496e11
M_PROTON = 1.674e-27
YEAR = 3.15576e7

# representative bodies: (name, mass, radius)
BODIES = {
    "Sun":          (1.0 * Msun, Rsun),
    "White dwarf":  (0.6 * Msun, 7.0e6),     # ~Earth-sized
    "Neutron star": (1.4 * Msun, 1.2e4),     # ~12 km
}


def escape_velocity(M, R):
    return math.sqrt(2 * G * M / R)


def deflection_deg(M, impact_param_m, v):
    """Gravitational turn angle for a hyperbolic pass (Rutherford form)."""
    return math.degrees(2.0 * math.atan(G * M / (impact_param_m * v * v)))


def focal_impact_km(M, v):
    """Impact parameter giving a ~90 deg turn. If this is < the star's radius,
    a big turn is geometrically impossible (focal point inside the star)."""
    return (G * M / (v * v)) / 1000.0


def can_boomerang(M, R, v, min_turn_deg=10.0):
    """Can a grazing pass bend the path by at least min_turn_deg?"""
    return deflection_deg(M, R, v) >= min_turn_deg


def oberth_infall_kms(M, r_perihelion_m):
    """Upper bound on the 'free' speed gained by diving to perihelion
    (= escape velocity there). A powered burn at perihelion does better, but
    this sets the scale."""
    return escape_velocity(M, r_perihelion_m) / 1000.0


def scoop_pass(perihelion_AU, area_km2=1.0, n0_per_cc=7.0):
    """Mass swept in one close pass through a ~1/r^2 stellar wind.
    Column density of a straight-line pass at impact parameter b through
    n(r)=n0 (r0/r)^2 is pi*n0*r0^2/b. Returns grams of H/He and mg of He-3."""
    b = perihelion_AU * AU
    n0 = n0_per_cc * 1e6                     # -> per m^3
    col = math.pi * n0 * AU * AU / b          # atoms / m^2
    H_atoms = col * (area_km2 * 1e6)
    H_g = H_atoms * M_PROTON * 1000.0
    He_over_H = 0.085                          # interstellar/stellar number ratio
    He3_over_He = 2.0e-4
    He_g = H_g * He_over_H * (4.0 / 1.0)       # mass ~4x per atom
    He3_mg = (H_atoms * He_over_H * He3_over_He) * 5.008e-27 * 1e6
    return {"H_g": H_g, "He_g": He_g, "He3_mg": He3_mg}


def perihelion_flux_kw_m2(r_perihelion_m, L=Lsun):
    return L / (4 * math.pi * r_perihelion_m ** 2) / 1000.0


def scoop_drag_N(perihelion_AU, v, area_km2=1.0, n0_per_cc=7.0):
    """Drag on the scoop while sweeping wind at speed v (force ~ n m v^2 A)."""
    n = n0_per_cc * 1e6 * (1.0 / perihelion_AU) ** 2
    return n * M_PROTON * v * v * (area_km2 * 1e6)


def _demo():
    print("Stellar boomerang + scoop -- where does it stop being science fiction?\n")

    print("1) A flyby bends your path only if speed < star's escape velocity:")
    for name, (M, R) in BODIES.items():
        ve = escape_velocity(M, R)
        turns = "  ".join(f"{fc*100:>4.1f}%c:{deflection_deg(M,R,fc*C):6.1f}°"
                          for fc in (0.001, 0.01, 0.10, 0.20))
        print(f"   {name:<13} v_esc={ve/1000:8.0f} km/s ({ve/C*100:5.2f}%c) | grazing turn  {turns}")
    print(f"   Your cruise 0.1c = {0.1*C/1000:,.0f} km/s -> only a neutron star can turn you,")
    print("   and the nearest is ~400 ly away (none in the 100 ly catalogue).\n")

    print("2) At 0.1c, the impact parameter for a 90° turn vs the star's size:")
    for name, (M, R) in BODIES.items():
        b = focal_impact_km(M, 0.1 * C)
        verdict = "INSIDE the star" if b < R / 1000 else "feasible (but lethal)"
        print(f"   {name:<13} need b={b:8.1f} km  (radius {R/1000:>10,.0f} km) -> {verdict}")

    print("\n3) Brief scoop on a close solar pass (1 km^2), vs survival:")
    for rp in (0.1, 0.02, Rsun / AU):
        s = scoop_pass(rp)
        flux = perihelion_flux_kw_m2(rp * AU)
        drag = scoop_drag_N(rp, 0.1 * C)
        print(f"   perihelion {rp:6.3f} AU: {s['H_g']:7.1f} g H, {s['He3_mg']:6.2f} mg He-3 | "
              f"heat {flux:9.0f} kW/m^2, drag@0.1c {drag:.1e} N")
    print("   -> Real mass (g-kg/pass, vs mg/yr in open space) -- but it's bulk")
    print("      hydrogen, not He-3, and the heat + drag shred a fast, light scoop.\n")

    print("VERDICT")
    print("  * At relativistic cruise (0.1-0.2c): the boomerang fails around normal")
    print("    stars and even white dwarfs (focal point inside the star); only")
    print("    neutron stars / black holes can turn you, and none are near.")
    print("  * The scoop harvests real bulk H/He but not fusion fuel, and the close")
    print("    pass means MW/m^2 heat and huge drag -- plus steering toward the star")
    print("    costs delta-v you don't have at cruise.")
    print("  * WHERE IT WORKS: (a) a SLOW wanderer (v < a few hundred km/s, ~0.002c)")
    print("    CAN gravity-assist off ordinary stars, linger to scoop reaction mass,")
    print("    and survive -- a patient, self-repairing AI roaming the galaxy over")
    print("    millennia. (b) Using OUR Sun as a launch 'sundiver' Oberth burn is a")
    print("    real way to GET fast at the start. Slow regime and launch regime, yes;")
    print("    relativistic cruise, no.")


if __name__ == "__main__":
    _demo()
