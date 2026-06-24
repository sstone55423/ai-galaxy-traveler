# AI Galaxy Traveler — Phase 1: Local Star Simulator

A realistic (no science-fiction) simulation substrate for an AI probe launched
from Earth into the solar neighbourhood. Phase 1 maps the real stars within
**100 light-years** and gives us the geometry + physics engine that later phases
(propulsion, power, autonomy) will plug into.

Everything here is ordinary, checkable physics. Distances are real measured
values; travel times come from special relativity and the relativistic rocket
equations; propulsion sizing uses the Tsiolkovsky equation.

## Files

| File | What it is |
|------|------------|
| `stars_100ly.csv` / `.json` | The catalogue: 127 real stars, with 3D coordinates (light-years) |
| `galaxy_sim.py` | The simulation engine — distances, neighbours, routing, travel-time, propulsion sizing |
| `propulsion.py` | **Phase 2** — the three flyby propulsion models (run it for full mass/energy/fuel detail) |
| `energy.py` | **Phase 3** — power sources, decay/burn-up, k-of-N redundancy, ISM collector |
| `energy_dashboard.html` | **Phase 3** — interactive power & reliability dashboard (open in a browser) |
| `flyby.py` | **Phase 4 sketch** — stellar boomerang + scoop feasibility (run for the verdict) |
| `wanderer.py` | **Phase 4** — slow self-replicating fleet simulator over deep time |
| `wanderer_map.html` | **Phase 4/5** — interactive 3D expansion with a Star-field selector (100 ly / 1 kly / Milky Way / Local Group) |
| `make_starfields.py` | **Phase 5** — ~45 real bright stars (to ~1.3 kly) + procedural Milky Way generator |
| `star_map_3d.html` | Interactive 3D star map (open in any browser, no internet needed) |
| `build_catalog.py` | Regenerates the catalogue from the source data table |
| `make_map.py` | Rebuilds the HTML map from the catalogue |

## The catalogue

- **127 stars**, the nearest systems plus notable named and confirmed
  exoplanet-host stars (46 of them), every one a real catalogued object.
- Positions from standard astrometry (Hipparcos / Gaia DR3 / RECONS nearest-star
  lists). Frame: equatorial Cartesian, Sun at the origin, units = light-years
  (`x` → vernal equinox, `y` → RA 6h, `z` → north celestial pole).
- **Completeness caveat:** this is a *curated subset*, not a full census. A
  complete count within 100 ly runs to several thousand stars, dominated by
  faint red and brown dwarfs that are still being discovered. Nearest-neighbour
  routing therefore sees deliberately sparse "stepping stones" — realistic for
  early planning, and easy to expand later by ingesting the full HYG/Gaia tables.

## The engine

```bash
python3 galaxy_sim.py      # runs a demonstration
```

It can: measure the 3D distance between any two stars, list nearest neighbours,
find the shortest multi-hop route under a maximum single-jump limit, and
estimate travel time three ways — constant cruise speed (Earth clock), the same
on the ship's clock (time dilation), and a constant-proper-acceleration
"torchship" that accelerates to the midpoint then brakes to arrive at rest.

## The 3D map

Double-click `star_map_3d.html`. Drag to rotate, scroll to zoom, click a star
to inspect it, hover to measure its distance from the current origin. Toggle
labels, distance rings (25 / 50 / 100 ly), and auto-rotation; filter to notable
or planet-host stars; search by name. Any star can be set as the measurement
origin, so you can plan legs from waypoints, not just from the Sun.

## What Phase 1 already tells us (the realistic constraints)

These come straight from the engine, for the nearest target, **Proxima Centauri
(4.25 ly)**:

- **Today's speed is hopeless.** At Voyager 1's 17 km/s the trip is **~75,000
  years**. Useful missions need roughly **10–20% of light speed**, where Proxima
  is **~42 / ~21 years** (Earth clock).
- **Acceleration is the hard part, not top speed.** A 1 g "torchship" reaches
  Proxima in **3.5 ship-years** (peaking at 95% c) — but that is a *kinematic
  ideal*. Whether you can actually push a real mass that hard is an energy and
  propellant question, which is the next bullet.
- **Low mass + high exhaust velocity is the whole game.** Mass ratio (fuelled
  vs dry) to reach just 10% c one way: chemical rockets → *impossible*
  (10^300+), ion → 10^260, nuclear-electric → 10^26, **fusion-class exhaust
  (~10,000 km/s) → ~20**. Only fusion or **propellant-less beamed-laser sails**
  (grams of payload, Breakthrough-Starshot style) close the gap — which is
  exactly why you flagged low mass as essential.

## How your open questions map to the next phases

- **Initial speed & how to accelerate slow → fast:** `relativistic_rocket()` and
  the cruise models are the planning tools. Realistic near-term acceleration is
  tiny (ion ≈ 10⁻⁴ g), so Phase 2 will compare slow continuous-thrust profiles
  against a brief, violent beamed-sail boost.
- **Propulsion method:** `mass_ratio()` already ranks the options. Phase 2
  detail: ion, nuclear-electric, fusion, and laser-sail trade studies.
- **Energy regeneration + redundancy for long life:** not yet modelled. Phase 2
  adds a power-vs-time model (radioisotope decay, reactor output) with redundant
  units and a failure/degradation simulation across centuries.
- **Low mass:** `kinetic_energy()` shows energy scales with mass × c² × (γ−1) —
  the lever that makes gram-scale sail probes the most physically honest design.

## Phase 2 — Propulsion (flyby)

Three engines are modelled end-to-end in `propulsion.py`, wired into the engine
demo and into the map's reachable-range shading. Mission profile: **flyby** —
accelerate, then coast past the target (fastest option; a bare sail can't brake).

| Engine | Cruise | → Proxima (4.2 ly) | → Vega (25 ly) | Launch mass | Reach in 100 yr |
|--------|--------|--------------------|----------------|-------------|-----------------|
| Laser sail (Starshot-class) | 20% c | 21 yr | 125 yr | ~1 gram | 71 / 127 stars |
| Fusion rocket (Daedalus-class) | 12% c | 37 yr | 211 yr | ~53,000 t | 25 / 127 stars |
| Nuclear-electric (reactor + ion) | 0.1% c | 4,300 yr | 25,000 yr | ~1,000 t | 0 / 127 stars |

What the physics says (all anchored to real reference designs):

- **Laser sail** is the fastest and by far the lightest — the energy stays on the
  ground in a ~100 GW phased array. The catch is real: it only *flies by* (no
  way to stop), and the array must hold its beam on a gram-scale sail to within
  metres over ~0.1 AU. Only ~16% of the laser energy ends up as sail motion; the
  rest flies off as light — which is fine, because the sail is so light.
- **Fusion rocket** carries its own power source and a real 450 t payload, but
  pays for it with ~50,000 t of D/He-3 fuel — including ~20,000 t of **helium-3**,
  which barely exists on Earth (you'd mine it from the Moon or the gas giants).
- **Nuclear-electric** is the honest slow-boat: millennia to the nearest star.
  Its value isn't speed — it's power, steering and decade-to-century longevity.
  Treat it as a support/utility technology, not the main interstellar drive.

In the 3D map, pick an engine (Sail / Fusion / N·elec) and drag the **time-horizon
slider**: a bubble shows how far that engine reaches, stars beyond it dim out, and
hovering any star shows the flyby time for the selected engine. Every default
(laser power, sail mass, exhaust velocity, mass ratio, reactor specific mass) is
adjustable in `propulsion.py`.

## Phase 3 — Power & redundancy (the probe never stops)

A probe that doesn't stop must carry its energy and run untended for centuries,
with only rare material top-ups from a comet or asteroid. Modelled in
`energy.py` and explorable in `energy_dashboard.html`. Design point: **~4 kW
electric for 300 years**.

- **Source — only a reactor is mass-sane.** A fission reactor needs just
  **~16.5 kg of U-235** (10% burn-up) for 4 kW-e over 300 yr. A Pu-238 RTG would
  need **~283 kg** of Pu-238 (dumping 153 kW of waste heat at launch); Am-241
  ~203 kg. Radioisotopes simply can't hold kilowatts for centuries.
- **Surviving untended is the real problem.** With power-converter MTBF ~50 yr
  and no repair, the chance of still meeting the load at year 300 is ~**0** —
  units almost surely fail, and reaching 95% reliability would take an
  impractical pile of spares. Passive redundancy collapses over centuries.
- **Self-repair is what buys the mission.** Let the AI repair/reconfigure units
  (MTTR ~1 yr — this is where your rare comet/asteroid material earns its keep)
  and per-unit availability rises to ~98%, holding the load with ~12 units. The
  lever is repair, not more spares.
- **The "helium collector," quantified.** A 1 km² interstellar scoop gathers
  ~360 g/yr hydrogen and ~110 g/yr helium, but only **~17 mg/yr of helium-3**
  (≤ ~300 W ideal, and only if you could separate isotopes and micro-fuse them
  in flight). Negligible as fuel — keep ISM scooping and comet/asteroid mining
  as *bonus material*, not the power plan.

In the dashboard, tune load, source, mission life, converter MTBF, redundancy
and the self-repair / ISM toggles, and watch power-vs-time and the probability
the load is met.

## Phase 4 sketch — stellar boomerang + scoop

Idea explored: swing close to stars en route to gravity-assist ("boomerang") off
them and deploy a scoop briefly in the denser gas near the star. Modelled in
`flyby.py`. Both maneuvers are real; the catch is doing them at cruise speed.

The governing rule: **a flyby bends your path by a large angle only if your
speed is below the star's surface escape velocity.** That's ~618 km/s for the
Sun (0.2% c) and ~4,800 km/s for a white dwarf (1.6% c) — both far below a 0.1c
cruise, where the gravitational focal point falls *inside the star*. Only a
neutron star (escape velocity ~59% c) could turn a relativistic probe, and the
nearest is ~400 ly away. A close scoop does gather real mass (grams to ~1 kg of
hydrogen per km² per pass, vs. milligrams per *year* in open space), but it's
bulk H/He — not He-3 — and a 0.1c pass means MW/m² heat and kN–MN of scoop drag.

Where the idea genuinely works: a **slow wanderer** (a few hundred km/s, ~0.002c)
*can* gravity-assist off ordinary stars, linger to scoop reaction mass, and
survive the gentler environment — a patient, self-repairing AI roaming the
galaxy over millennia (which dovetails with the Phase 3 self-repair model). And
using *our own Sun* as a launch "sundiver" Oberth burn is a real way to get fast
at the start. Slow regime and launch regime: yes. Relativistic cruise: no.

## Phase 4 — The self-replicating wanderer (the real architecture)

The goal isn't speed — it's an AI that **learns and grows over deep time**. That
flips the design: instead of one fast probe, a slow **von Neumann (self-
replicating) fleet** crawls star to star at a gravity-assist-navigable speed
(hundreds of km/s) and copies itself at each stop. Individual probes are slow;
the fleet grows exponentially. Modelled in `wanderer.py` and explorable in the
interactive `wanderer_map.html`.

Grounded in Freitas's 1980 self-reproducing-probe study: replication takes
~1,000 years (500 yr seed→factory, 500 yr factory→probe). Over a 10,000-year
horizon at ~450 km/s the fleet settles only the **nearest ~5 systems across ~2
generations** — but that's already self-sustaining exponential growth, and it's
very sensitive to the design: **double the cruise speed and it reaches ~16
systems**; halve the replication time and it reaches ~8.

Extrapolated, the expansion front spans the galaxy (100,000 ly) in **~150 Myr**
at this slow cruise — between Hart's ~1 Myr (for a 0.1c fleet) and Tipler's
~300 Myr. The lesson: a handful of patient, self-repairing seeds blanket the
galaxy given deep time. What keeps it alive isn't speed — it's the **Phase-3
self-repair and error-correction** that preserve each probe across millennia and
keep replication faithful over generations.

Open `wanderer_map.html`, press play, and watch the fleet spread: drag to rotate,
and use the sliders (cruise speed, replication time, offspring per stop, horizon)
and the time scrubber to explore how far the AI gets — and how the levers that
matter are patience and fidelity, not velocity.

The map also has a **Galactic (log) scale** toggle that pulls back to show the
nearest satellite galaxies and Andromeda (2.5 Mly) in their real directions on a
logarithmic radius, each labelled with its flyby crossing time, with a reach-
frontier bubble that grows as you scrub time. The horizon slider now runs all the
way to ~2 Gyr — far enough to watch the reach frontier crawl out toward (and fall
short of) the satellite galaxies, making the intergalactic gulf visible: the whole
100 ly catalogue is a speck against the void to the next galaxy.

A **Colonies keep replicating** checkbox switches from the one-shot branching
tree to persistent, *uncoordinated* production: each colony keeps building probes
every replication period and fires them at its nearest stars from a precomputed
list, with no shared map of who has already settled where. The panel then tracks
probes launched and the redundant-visit fraction, which climbs from ~40% to ~99%
as colonies repeatedly hit already-settled systems — the realistic price of a
swarm with no central coordination.

## Phase 5 — Populating the galaxy

The map's **Star field** selector swaps both what you see and what the fleet can
spread through:

- **100 ly** — the curated real catalogue (127 stars); the fleet hops as before.
- **1 kly** — adds ~45 real famous stars out to ~1,300 ly (Betelgeuse, Rigel,
  Spica, Antares, Polaris, the Pleiades...). Real measured positions; the fleet
  hops through them too.
- **Milky Way** — a modelled galaxy: an exponential disk, four spiral arms and a
  central bulge built from measured density profiles, with the Sun in its real
  place (~26,700 ly from the Galactic Centre, correctly oriented — the centre
  sits toward Sagittarius). Individual distant stars are synthetic; the
  structure, scale and Sun position are real. Here the fleet shows as a green
  **reach frontier** expanding at cruise speed (discrete hops would mislead over
  a sampled galaxy) — watch it crawl across the disk over tens of millions of
  years.
- **Local Group** — the log-scale zoom-out: the 100 ly catalogue is a speck and
  the satellite galaxies + Andromeda sit far out, making the intergalactic gulf
  visible.

Honesty note: beyond the bright nearby stars we cannot have real positions for
the galaxy's hundreds of billions of stars, so the Milky Way field is a
physically-grounded statistical model, not a star-by-star catalogue.

## Suggested next step

Phases 1-4 are done. Natural extensions of the wanderer:
1. **Replication budget** — tie each copy to the Phase-3 reactor fuel + ISRU
   material it actually needs, so a colony can only reproduce where resources
   allow (gating the exponential growth realistically).
2. **Fidelity over generations** — model copy-error vs. error-correction, so the
   AI either degrades or stays faithful across deep time.
3. **Longer horizons** — run the same fleet to 1 Myr / 1 Gyr to watch it cross
   the neighbourhood and approach the Hart-Tipler galactic timescales.
