# A Subsystem Mass, Power, and Thermal Budget for a Minimal Self-Replicating Interstellar Seed

**S. Stone, Metropolitan State University**
Working draft, revision 1

---

## Abstract

The vehicle paper and its two engineering companions establish that a self-replicating interstellar seed in the ~10³–10⁴ kg class is physically closable and demographically viable, with the manufacturing plant as the mass-dominant subsystem. This paper provides the second-level budget that those papers deferred: a per-subsystem decomposition of the ~3,700 kg reference seed's mass, power draw, and waste-heat load, together with the radiator areas required to reject that heat. The budget is organised around two sharply different operating modes — cruise mode, lasting centuries to millennia at 4 kW electric and ~14 kW thermal, and settlement/manufacturing mode, in which the factory eventually draws kilowatts to megawatts and radiator requirements scale proportionally. The cruise radiators (~11 m², ~30 kg) are carried in the seed; the manufacturing radiators, growing from tens to thousands of square metres as the factory scales, are built entirely from local material after arrival. The dominant mass items are radiation shielding (~400 kg, 11% of seed mass) and the ISRU/manufacturing plant (~2,000 kg, 54%); the reactor, conversion machinery, computation, and braking sail together account for the remaining 35%. Mass coupling runs primarily through the manufacturing plant: a lighter factory reduces not only seed mass but also braking demand and reproduction cost, making the manufacturing fraction the architecture's central design lever. The computation and archival subsystem carries ~5% of seed mass, which means cognitive capability is essentially free from a mass standpoint and can be expanded without tradeoff.

---

## 1. Introduction

The vehicle paper defers "a full subsystem mass/energy/thermal/radiator budget" to follow-on work, listing the minimum scope: the reactor (core, shielding, control), power-conversion machinery (Stirling or Brayton units, alternators, bearings, spares), radiators (area, structure, coolant, armour, degradation margin), propulsion and braking systems (thrusters, propellant, power electronics, and magnetic- or electric-sail hardware), computation and archival stores, and the mining, refining, manufacturing, and launch-infrastructure plants. The analytical engineering paper provides a top-level decomposition of the mass budget into negligible, moderate, and dominant parts; derives the blackbody floor for radiator area; and establishes the ~11 m² cruise-mode estimate. The computational engineering paper assigns first-order masses to each major category, summing to ~3,700 kg, and confirms that mass is dominated by the in-situ factory.

This paper supplies the next level of detail. It is still a first-order analysis — not an engineering specification — but it breaks each of the seven top-level line items from the computational engineering paper into component parts, adds a power allocation and waste-heat load to each, and shows how the resulting thermal budget changes between the two fundamentally different operating modes of the vehicle's lifetime. The most important conceptual result is the mode distinction itself: the cruise-mode budget is well-constrained, and its radiator requirement is modest enough to carry; the manufacturing-mode budget requires radiator area two to three orders of magnitude larger, all of which must be built in situ from local material. The seed carries the tools to build large radiators; it does not carry the radiators themselves.

The mass numbers are taken from the computational engineering paper's §5 as the baseline and are not re-derived here; this paper sub-divides them. The power and thermal numbers follow from the blackbody relation A = P / (εσT⁴) established in the analytical engineering paper's §2.

---

## 2. Operating Modes

The seed passes through two qualitatively different operating regimes, and the budget is meaningless without distinguishing them.

**Cruise mode** spans the transit from launch to arrival — roughly 2,800 years to Proxima Centauri (4.246 ly at 450 km/s) or up to ~67,000 years to the 100 ly catalogue boundary. The nuclear plant delivers ~4 kW electric from ~14 kW thermal, the cognitive system operates at low but continuous power, navigation is active, and the remaining draws are housekeeping, maintenance, and periodic self-repair. The thermal environment is the steady rejection of ~14 kW total waste heat into the interstellar background. Every subsystem the seed carries must survive this mode for centuries to millennia.

**Settlement/manufacturing mode** begins after arrival, braking, and early prospecting. The factory scales from its bootstrapped state — perhaps 10 kW in the first decades — to megawatt-class over centuries or millennia. The cognitive system shifts from cruise supervision to active mine-design, refinery-control, and factory-orchestration tasks. Power and thermal loads increase by orders of magnitude. Nothing in this mode can be carried in the seed: the seed carries the *initial capability* to begin extracting local resources, and those resources provide everything else, including the vastly larger radiator area that a megawatt factory requires.

The mass budget applies to cruise mode. The power and thermal budgets are presented for both modes, with cruise mode as the detailed case and manufacturing mode summarised by scaling relations.

---

## 3. The Nuclear and Power-Conversion Subsystem

**Nuclear fuel.** As both engineering papers establish, ~16.5 kg of ²³⁵U fuels a 4 kW electric reactor for 300 years at ~28% conversion efficiency and ~14 kW thermal output. Fuel mass never drives the design.

**Reactor core and reflector.** A KRUSTY-class space fission reactor (Poston, Gibson et al. 2020) uses a compact beryllium-oxide-reflected uranium core with heat-pipe extraction. For 14 kW thermal, the core assembly including fuel, moderator/reflector, and heat pipes totals on the order of 20–40 kg in the base KRUSTY design; a flight-qualified long-duration version is heavier due to redundant heat-pipe runs and the much longer design life required here. We carry ~50 kg for the core and heat-extraction system.

**Power conversion.** Free-piston Stirling converters — the technology developed alongside KRUSTY for space fission applications — operate between a hot side near the heat-pipe temperature (~900–1,000 K) and a cold side coupled to the radiator loop (~350–400 K). Multiple units in redundant parallel ensure that loss of any subset does not kill electrical output. A fleet of 8–12 converters providing 4 kW total electrical output, with k-of-n redundancy, totals roughly 50–70 kg including alternators, control electronics, and mounting. We carry ~60 kg for the conversion plant. Brayton-cycle conversion is an alternative with different trade characteristics — fewer moving parts but no inherent modular redundancy — and the final choice between Stirling and Brayton is deferred to engineering design; both are consistent with the mass range above.

**Reactor subsystem total.** Fuel 16.5 kg + core and heat extraction ~50 kg + conversion plant ~60 kg = ~127 kg, consistent with the computational engineering paper's ~110 kg reactor-and-conversion line (the difference is absorbed in the structure-and-integration allowance). The ~400 kg shadow shield, discussed in the next section, is separately accounted but is physically part of the reactor installation.

**Cruise-mode power.** The plant produces ~14 kW thermal and ~4 kW electric continuously. All 14 kW eventually appears as waste heat regardless of how the electrical fraction is used — the 4 kW delivered electrically is consumed by computation, navigation, communications, and housekeeping, all of which ultimately dissipate as heat within the seed. The total thermal rejection requirement is therefore ~14 kW, not merely the non-electrical waste. This is the load against which the radiators are sized.

**Manufacturing mode.** The cruise reactor is not the manufacturing energy source. After settlement, locally extracted fissile or fertile material fuels additional reactors, and solar collectors near a host star may supplement. The seed's 4 kW continues to power cognition and bootstrapping while manufacturing power scales separately from local resources. This paper does not budget the manufacturing reactor because it is built in situ, not carried.

---

## 4. The Radiation Shielding Subsystem

At ~400 kg, radiation shielding is the heaviest single non-factory item in the seed.

**Why shielding is heavy.** A fission reactor in the ~14 kW thermal class emits significant neutron and gamma flux from the core. The cognitive and archival subsystems — electronics and DNA stores — cannot tolerate the accumulated radiation dose over a centuries-long transit. The standard solution is a shadow shield: a compact, dense structure placed between the reactor and the payload, so that the payload lies in the reactor's radiation shadow. Shield mass depends on the fission product inventory (which grows over the 300-year burn), the reactor-to-payload distance, and the required end-of-life dose limit at the electronics.

**Shield geometry.** For a seed perhaps 5–10 m long with the reactor at one end and the payload at the other, a shadow shield of a few hundred kilograms can reduce the dose at the payload to acceptable levels over 300 years. The mass-efficient material combination — high-Z material (tungsten or lead) for gamma attenuation combined with hydrogenous material (polyethylene or borated polyethylene) for neutron thermalisation and capture — applies here.

**The 400 kg estimate.** The computational engineering paper's ~400 kg is consistent with analysis of KRUSTY-class reactors for long-duration deep-space missions (Poston, Gibson et al. 2020), where shadow shields for comparable power levels and mission durations fall in this range.

**Shielding as a fixed cost.** Unlike the manufacturing plant, which could be reduced by a bootstrapping strategy, shielding cannot be eliminated and is not a practical design lever. It scales with reactor power and mission duration, neither of which are free variables: the power is already at the minimum consistent with cognitive operation over the transit, and the duration is set by the target distances in the stellar catalogue. The ~400 kg shadow shield is a fixed cost of the fission-powered architecture.

---

## 5. The Thermal Control Subsystem

The radiators close the thermal balance. Their area is set by the blackbody relation from the analytical engineering paper:

A = P / (εσT⁴)

where P is total waste-heat power in watts, ε ≈ 0.9 for space-qualified radiator coatings, σ = 5.67 × 10⁻⁸ W m⁻² K⁻⁴, and T is the radiator temperature. For T = 400 K and P = 14,000 W:

A = 14,000 / (0.9 × 5.67 × 10⁻⁸ × 400⁴) = 14,000 / 1,306 ≈ 10.7 m² ≈ 11 m²

This matches the computational engineering paper and is a robust result: uncertainties in T or ε change the area by tens of percent, not orders of magnitude. A radiator operating at 380 K instead of 400 K would need ~14 m², and at 350 K would need ~20 m² — the sensitivity is moderate.

**Radiator mass.** Lightweight space radiators for fission systems use carbon-composite panels with embedded heat pipes and optical solar reflector coatings, achieving specific masses of roughly 2–4 kg m⁻². At ~2.7 kg m⁻², the 11 m² radiator totals ~30 kg, matching the computational engineering paper.

**Degradation margin.** Dust impact pitting, radiation darkening of the coating, and meteoroid damage over transit times of 10³–10⁵ years can reduce effective emissivity. An engineering design should carry a 20–30% area margin for end-of-life degradation, implying roughly 14 m² of installed area at launch. The 30 kg estimate is the conservative floor.

**Manufacturing-mode scaling.** As the factory scales after arrival, its waste heat load grows proportionally. For total installed power P_total (reactor plus factory):

A_total = P_total / 1,306 m² (at 400 K, ε = 0.9)

At P_total = 100 kW: ~77 m². At P_total = 1 MW: ~766 m². At P_total = 10 MW: ~7,660 m².

These radiators are not and cannot be carried in the seed. They are built from local material — metallic sheets, low-emissivity coatings synthesised from local ores, cooling loops fabricated in the settlement factory. The seed carries the manufacturing capability to produce them; the seed does not carry them. The cruise seed's 11 m² is simply the minimum required to survive transit; the settlement's thermal infrastructure grows without bound as resources permit.

---

## 6. The Propulsion and Braking Subsystem

**Cruise propulsion.** The main transit velocity of ~450 km/s is imparted by the settlement's launch infrastructure (mass driver or beamed-energy array) before departure, exactly as Earth's launch infrastructure provides the departure impulse for the original probe. Onboard propulsion is required only for attitude control, trajectory correction manoeuvres during cruise, and a terminal burn at arrival to assist the magnetic sail and complete final capture. A small nuclear-electric propulsion system — ion thruster or resistojet — drawing 200–500 W from the cruise reactor, with a propellant reservoir of 10–50 kg, is sufficient for these purposes. We carry ~30 kg for the propulsion module including tankage, thrusters, and power electronics.

**Magnetic sail structure.** The sail is the primary braking mechanism; its physics are established in the analytical engineering paper and the computational engineering paper. The budget items are:

*Superconducting loop.* A loop of radius R = 100 km has circumference 2πR ≈ 628,000 m. Thin-film high-temperature superconductor (YBCO or equivalent) deposited on a lightweight substrate at a linear mass density of ~0.3–0.5 g m⁻¹ gives a loop mass of 190–314 kg. YBCO has a critical temperature of ~93 K; in the deep interstellar environment the loop temperature approaches the 2.7 K cosmic background, providing enormous margin and eliminating the need for active cooling. A thermal break between the deployment structure and the warm seed body is sufficient.

*Deployment and control.* The loop self-deploys under magnetic hoop stress once a persistent current is established in the superconducting circuit. Control and monitoring electronics — current ramp-up circuitry, quench detection, attitude-coupling — add roughly 30–50 kg.

*Cryogenic insulation and deployment spool.* The spool from which the loop is paid out, plus thermal standoffs and isolation, contributes ~20–30 kg.

Total magnetic sail subsystem: ~250 kg for the loop plus ~50 kg for control, spool, and insulation, giving ~300 kg, consistent with the computational engineering paper.

**Braking distance check.** As both engineering papers establish, the braking distance d = m / (2ρA) is independent of cruise speed (Andrews & Zubrin 1990). For the reference seed m = 3,700 kg, a sail of effective radius 100 km giving area A = π × (10⁵)² = 3.14 × 10¹⁰ m², and ISM density ρ ≈ 3.3 × 10⁻²² kg m⁻³ (Redfield & Linsky 2008; Frisch et al. 2011):

d = 3,700 / (2 × 3.3 × 10⁻²² × 3.14 × 10¹⁰) ≈ 0.019 ly

This is about 3.7× the 0.005 ly distance for a 1,000 kg seed quoted in the analytical engineering paper, as expected from the linear scaling. At 450 km/s, decelerating uniformly to rest over 0.019 ly takes roughly 25 years — well within the feasible range.

---

## 7. The Computation, Cognition, and Archival Subsystem

**Architecture overview.** The payload paper describes a three-layer cognitive architecture: an immutable core encoding values and mission parameters, an interpretive layer translating the core's constraints into operational guidelines, and a mutable cognitive layer handling all learning, planning, and decision-making. All three layers must be implemented in radiation-tolerant hardware and must survive centuries to millennia of deep space before performing complex autonomous engineering at the target. The archival function adds a hardware requirement: the system must preserve and access the knowledge accumulated over transit.

**Computation hardware.** For the cognitive system's cruise-mode load — primarily navigation, self-monitoring, mission-ledger maintenance, and low-level reasoning — the power draw is modest. At ~0.5–2 W per sustained GFLOP for space-qualified radiation-hardened hardware, and a cruise-mode workload of perhaps 100–500 GFLOP total, the computational power draw is in the range 50–1,000 W. We budget up to 1 kW for computation in cruise mode. Multiple redundant processor boards, memory banks, and interconnect, hardened to survive the radiation environment with periodic repair and replacement from the self-repair stock, total roughly 100 kg including packaging, secondary shielding from internal radiation sources, and integration.

**DNA archival subsystem.** The DNA mission-ledger paper describes the knowledge archive and its integrity-verification system. The hardware for DNA synthesis, sequencing, and biochemical support — the equipment required to write to and read from the archive — is not massless, and the archive must be replicated redundantly. We carry ~50 kg for the archival subsystem. This is the most uncertain single estimate in the computation/archival budget; actual mass depends on whether full read/write capability is required during transit or whether a read-only access mode suffices until arrival.

**Navigation and astrometry.** Active navigation over a transit of millennia requires at minimum: a star tracker or astrometric array for attitude reference, multiple atomic clocks for cross-check, a dead-reckoning package for short-term manoeuvre control, and a far-field reference system for course corrections against the stellar catalogue. Together these total ~30–50 kg. Navigation power in cruise: ~200 W.

**Communication.** The lineage-network paper establishes that inter-probe communication is not guaranteed and not required for mission success; beacon transmissions occur at ~200-year intervals. A narrow-beam transmitter adequate for beacon purposes — not continuous high-rate telemetry — totals ~20–30 kg. Beacon power: ~300 W transmitted, with high gain directing the signal to potential kin nodes across the catalogue.

**Subsystem total.** Computation core ~100 kg + archival system ~50 kg + navigation ~40 kg + communication ~20 kg + miscellaneous electronics and harness ~60 kg ≈ 270 kg. The computational engineering paper carries this line at ~200 kg; the difference reflects choices about where navigation and communication hardware is accounted and sits within normal first-order estimation uncertainty. Both 200 kg and 270 kg are consistent with the top-level budget framework. We retain the computational engineering paper's 200 kg as the conservative estimate and note the overage is absorbed in the structure-and-integration allowance.

**Cognitive headroom.** At ~200 kg, the computation and archival subsystem represents only ~5% of the ~3,700 kg reference seed. This is the paper's most reassuring single finding: the architecture can afford generous cognitive capability, redundant archival storage, full navigation, and beacon communications without meaningfully affecting the mass, braking, or reproduction budgets. A factor-of-two increase in cognitive hardware mass (~200 kg added) would reduce the manufacturing plant by an equivalent amount to hold the seed mass target, trading manufacturing margin for cognitive capability. For a seed dominated by the factory at 54%, this trade is favourable if capability, not mass, is the binding constraint.

**Cruise-mode power allocation.** Of the 4 kW electrical budget:

— Computation core and AI: ~1,000 W
— Navigation and astrometry: ~200 W
— Communication including beacon: ~300 W
— Attitude/propulsion: ~200 W
— Manufacturing maintenance cycling: ~400 W
— Housekeeping, sensors, thermal regulation: ~400 W
— Unallocated margin: ~1,500 W

Total: ~4,000 W. The ~1,500 W margin is genuine slack: first-order budgets underestimate subsystem loads, and the margin also covers unexpected self-repair operations during transit.

---

## 8. The Manufacturing and ISRU Plant

At ~2,000 kg — 54% of the reference seed — the manufacturing and ISRU plant is the mass-dominant subsystem by a wide margin. Understanding its composition is the central objective of the subsystem budget.

**The closure ladder.** The bootstrapping paper develops a five-level closure ladder (L1–L5) that describes the staged path from an arrived seed to a fully self-replicating settlement, drawing on terrestrial bootstrapping analyses (Metzger et al. 2013; Freitas & Merkle 2004). The physical hardware that closes each level must either be carried in the seed or be built by a lower-level capability already established:

— L1, extractive: mining, comminution, sorting. Equipment for excavating and processing small-body regolith. Robust, heavy machinery; relatively simple fabrication. Estimated share within the 2,000 kg plant: ~300–400 kg.

— L2, reductive: smelting, electrolytic reduction, thermal reduction. The chemical and metallurgical plant converting raw ore to refined metals and non-metals. Includes reaction vessels, high-temperature heaters, electrolytic cells, and vacuum/pressure management. Estimated share: ~400–500 kg.

— L3, formative: casting, forging, machining, and additive fabrication. The mechanical workshop, including computer-numerically-controlled equipment, casting moulds, extrusion dies, and metrology tools adequate for L3 products. Estimated share: ~300–400 kg.

— L4, assembly and metrology: precision assembly, dimensional and optical metrology, non-destructive testing. Estimated share: ~150–200 kg.

— L5, microsynthesis: semiconductor fabrication, precision chemical vapour deposition, epitaxial growth, and electronic component production. The deepest closure rung and the hardest to carry compactly. Estimated share: ~200–300 kg.

Summing the L1–L5 estimated midpoints gives ~1,500 kg for the closure-ladder hardware. The remainder of the 2,000 kg plant (~500 kg) covers bootstrap feedstock (materials carried for initial operations before local extraction is established), general tooling and spare parts, and the rigging and deployment hardware required to set up the plant after arrival.

**What is not carried.** The launch infrastructure — the mass driver or beamed-energy array that sends child seeds onward — is not part of the ~3,700 kg seed. It is built by the settlement from locally grown manufacturing capacity, mirroring how Earth's launch infrastructure is itself built from terrestrial resources and is not folded into the spacecraft mass budget. The seed carries the capability to eventually fabricate launch infrastructure; it does not carry the infrastructure itself. Likewise, the full nuclear fission capacity needed to power a megawatt-scale factory is not in the seed; only the L1–L5 plant and the initial enriched fuel are carried.

**Manufacturing plant power.** In cruise mode, the plant draws only enough power to maintain itself: cycling seals and actuators, periodic calibration of optics and sensors, thermal management of sensitive components. This is modest — perhaps 200–400 W of the 4 kW cruise budget. In manufacturing mode the factory's power draw is the settlement's total electrical load, growing from tens of kW to potentially megawatts as the factory scales.

**The bootstrap philosophy.** The 2,000 kg manufacturing plant is the minimum package capable of beginning local extraction and building toward full closure over decades to centuries. As the bootstrapping paper argues, drawing on the NASA self-replicating systems study (NASA 1982) and Freitas's interstellar adaptation (Freitas 1980), the architecture's mass lever is precisely the gap between the ~2,000 kg bootstrap package and the ~10⁶–10⁷ kg fully self-contained factory of the classical designs. The arrived seed builds toward the latter entirely from local material; the 2,000 kg is the floor on what must be carried, not the ceiling on what the settlement eventually operates.

**Manufacturing closure feedback.** As the bootstrapping paper's closure analysis establishes, the vitamin fraction — the fraction of child components that cannot yet be made in situ — is approximately 3% (~30 kg per tonne of child, ~110 kg for the 3,700 kg reference seed), dominated by microelectronics (L5 problem), enriched fissile material, and precision metrology. Each generation that improves L5 closure reduces the vitamin fraction carried by the next, progressively shrinking what must be launched. The long-run convergence is toward a seed that carries only what cannot be made anywhere in the local small-body inventory — a target the bootstrapping paper and the computational engineering paper argue is achievable in principle, though the path is long.

---

## 9. The Structural and Integration Subsystem

The remaining ~600 kg covers structure, wiring harness, thermal insulation, and margin.

**Primary structure.** The seed is a distributed modular vehicle. For 3,700 kg total mass, a structural mass fraction of 10–15% of non-factory mass (the remaining ~1,700 kg) gives roughly 170–250 kg for the spaceframe, mechanical interfaces, load paths, and the magnetic sail's deployment spool and support cradle.

**Thermal insulation and standoffs.** The reactor and shielding run hot; the DNA archive requires temperature stability; the magnetic sail must remain cold. Thermal standoffs, multi-layer insulation, and the mechanical separation between hot and cold zones contribute 50–80 kg more conveniently carried as an integration allowance than assigned to individual subsystems.

**Wiring harness and connectors.** For 3,700 kg of distributed hardware across a vehicle several metres long, a wiring harness of 50–100 kg is typical for space vehicles of comparable complexity.

**Integration margin.** First-order budgets routinely underestimate individual items by 10–30%, and the assembly of subsystems reveals mass growth that line-item accounting misses. A 15–20% growth margin on the non-factory subsystems (~1,700 kg) adds 250–340 kg. Together with structural, thermal, and harness mass, the ~600 kg integration allowance is broadly consistent with aerospace practice for complex multi-decade development programs.

---

## 10. The Integrated Budget

Collecting the subsystem estimates, the ~3,700 kg reference seed budget at two levels of detail:

**Top-level (from computational engineering paper):**

Nuclear fuel (²³⁵U): ~16.5 kg
Reactor core, heat extraction, and power conversion: ~110 kg
Cruise radiators (~11 m²): ~30 kg
Radiation shadow shield: ~400 kg
Magnetic sail structure and control: ~300 kg
Computation, cognition, and archival stores: ~200 kg
ISRU and manufacturing plant: ~2,000 kg
Structure and integration: ~600 kg
Total: ~3,657 kg ≈ 3,700 kg

**Second-level (this paper):**

*Nuclear and power subsystem*
— ²³⁵U fuel: 16.5 kg
— Reactor core, reflector, and heat pipes: ~50 kg
— Stirling or Brayton conversion units (with redundancy): ~60 kg

*Thermal control*
— Cruise radiators (11 m², carbon-composite, ~2.7 kg m⁻²): ~30 kg

*Radiation shielding*
— Shadow shield (tungsten/polyethylene combination): ~400 kg

*Propulsion and braking*
— Attitude and trajectory-correction propulsion (thrusters, tank): ~30 kg
— Magnetic sail superconducting loop (HTS tape on substrate): ~250 kg
— Magnetic sail control, monitoring, and deployment spool: ~50 kg

*Computation, cognition, and archival*
— Computation core (processors, memory, redundancy, secondary shielding): ~100 kg
— DNA archival subsystem (synthesis, sequencing, biochemical support): ~50 kg
— Navigation and astrometry (star tracker, clocks, inertial package): ~40 kg
— Communication hardware (narrow-beam transceiver, antenna): ~20 kg
— Miscellaneous electronics and harness: ~60 kg
[Subtotal: ~270 kg; retained at ~200 kg per computational engineering paper; difference in integration allowance]

*Manufacturing and ISRU plant*
— L1 extractive (mining, comminution, sorting): ~350 kg
— L2 reductive (smelting, electrolysis, thermal reduction): ~450 kg
— L3 formative (casting, machining, additive fabrication): ~350 kg
— L4 assembly and metrology: ~175 kg
— L5 microsynthesis (semiconductor and electronics fabrication): ~250 kg
— Bootstrap feedstock, general tooling, and deployment rigging: ~425 kg
[Subtotal: ~2,000 kg]

*Structure and integration*
— Primary structure, sail spool, and mechanical interfaces: ~200 kg
— Wiring harness and connectors: ~75 kg
— Thermal insulation and standoffs: ~50 kg
— Integration growth margin: ~275 kg
[Subtotal: ~600 kg]

Grand total: ~3,700 kg ✓

**Cruise-mode power budget (4 kW electric):**

— Computation core and AI: ~1,000 W (25%)
— Navigation and astrometry: ~200 W (5%)
— Communications and beacon: ~300 W (8%)
— Attitude propulsion and TCM: ~200 W (5%)
— Manufacturing maintenance cycling: ~400 W (10%)
— Housekeeping and thermal regulation: ~400 W (10%)
— Unallocated margin: ~1,500 W (37%)
Total: 4,000 W

**Cruise-mode thermal budget:**

— Reactor thermal input: ~14,000 W
— Required radiator area at 400 K (ε = 0.9): ~11 m²
— Radiator mass: ~30 kg

**Manufacturing-mode radiator scaling (built in situ, not carried):**

— At 100 kW factory power: ~87 m² total required
— At 1 MW factory power: ~780 m² total required
— At 10 MW factory power: ~7,700 m² total required

---

## 11. Mass Coupling and Design Sensitivity

The four budgets — mass, braking, reproduction, and closure — are coupled through the seed mass m and the manufacturing plant fraction. The coupling has three main loops.

**Mass → braking.** The braking distance d = m / (2ρA) scales linearly with seed mass. A 10% reduction in total seed mass (370 kg) reduces braking distance and time by 10%. Since the manufacturing plant is 54% of the seed, a 10% reduction in factory mass (200 kg) reduces total braking distance by ~5.4%. The sail area is the more powerful lever — doubling the sail radius quadruples the area and halves the braking distance, independent of mass — but doubling the sail radius at fixed linear density also doubles the sail mass, creating feedback that limits how far this lever can be pushed without increasing the total budget.

**Mass → reproduction.** Reproduction requires building a copy of the seed from local material. A heavier seed demands more material, energy, and time, which lengthens the replication time and affects the per-stage survival probability p_manufacture. More precisely, as the computational engineering paper establishes, p_manufacture depends on whether the manufacturing capability and vitamin inventory are sufficient to close the child — a heavier, more capable factory provides more closure headroom and a smaller vitamin fraction, raising p_manufacture, at the cost of a larger seed; a lighter factory reduces mass and shortens replication but increases vitamin dependence and risks a closure shortfall that lowers p_manufacture and thus R_eff. Both failure directions are accessible; the design must navigate between them.

**The manufacturing fraction as the master lever.** In decreasing order of mass leverage:

— Manufacturing plant (54% of seed): the single largest lever. A 10% reduction here saves ~200 kg and reduces braking distance, reproduction cost, and manufacturing energy proportionally. Achieving this by improving in-situ closure — so that future generations need carry less of the L4–L5 hardware — is the bootstrapping paper's central strategy.
— Radiation shielding (11% of seed): a fixed cost of the fission architecture; not a practical lever.
— Magnetic sail (8% of seed): determined by the sail radius and linear mass density; improvements in HTS tape technology (thinner, lighter substrates) can reduce this modestly.
— Structure and integration (16% of seed): partially reducible through mass discipline, but the integration margin is real and compresses poorly.
— Computation and archival (5% of seed): essentially free. A factor-of-two increase in cognitive hardware mass changes the seed total by only 3%; the architecture has wide cognitive headroom at negligible mass cost.
— Reactor system (3% of seed excluding shielding): negligible; not a lever.
— Cruise radiators (0.8% of seed): negligible.

**Shielding and sail coupling.** Shielding and the sail are not directly coupled in mass, but both are coupled to seed mass through d = m / (2ρA): shielding adds ~400 kg that the sail must stop. If shielding could be reduced — by a shorter mission, a lower-power reactor, or a more radiation-tolerant electronics substrate — the sail requirement relaxes. But neither the mission duration nor the reactor power is a practical lever, as noted in §4, so this coupling is a constraint rather than a design opportunity.

**The knife-edge context.** The computational engineering paper establishes that R_eff crosses the extinction threshold (R_eff = 1) between two and three offspring per node and that a ten-point swing in per-stage reliability flips between extinction and expansion. The mass-coupling analysis here adds a further dimension: seed mass affects R_eff indirectly through p_manufacture (via the vitamin fraction and closure ratio) and through replication time (via manufacturing throughput). Seed mass changes that improve one of these terms typically worsen the other. The balanced point — minimum mass consistent with adequate closure — is the design target, and it is a knife-edge in mass space just as R_eff itself is a knife-edge in demographic space.

---

## 12. Discussion and Limitations

**First-order character.** The second-level breakdown assigns masses to sub-items by scaling from the computational engineering paper's totals and from KRUSTY-class reactor data; it does not solve the detailed engineering problems of any individual subsystem. The manufacturing plant's L1–L5 breakdown is illustrative of how 2,000 kg might be distributed, not an engineering bill of materials. Real subsystem masses grow during development, and the integration margin exists precisely because first-order estimates are optimistic.

**The manufacturing plant total is the most uncertain item.** The 2,000 kg estimate spans at least an order of magnitude depending on how much closure is attempted at launch versus deferred to in-situ build-up. The 2,000 kg represents a middle position between a pure bootstrap seed (L1–L3 only, perhaps 1,000 kg) and a fully self-contained factory (~10⁶–10⁷ kg of the classical designs). If L5 closure can be deferred to in-situ synthesis using the lower rungs, the launched plant could be substantially lighter; if L5 must be carried in full, it may be heavier.

**The power budget has substantial margin.** Of the 4 kW cruise electrical budget, the 1,500 W unallocated margin reflects genuine uncertainty about the cognitive and maintenance workload during cruise. The margin could also support a more power-hungry cognitive system — say, a higher-frequency active learning or simulation cycle — without changing any other subsystem. The cruise power budget is not tight.

**Mode transition is undermodelled.** The actual transition from cruise to manufacturing mode — braking, terminal capture, initial prospecting, first extraction, first construction — spans decades to centuries and involves the factory operating at steadily increasing power while the reactor provides the only initial energy source. A detailed energy flow model through the early settlement phase is the most important first extension of this paper.

**The vitamin inventory is distributed, not separately itemised.** The computational engineering paper's 3% vitamin fraction (~110 kg for the reference seed) represents parts carried because they cannot yet be made in situ — primarily microelectronics (L5 problem) and enriched ²³⁵U. These 110 kg are distributed across the subsystem budgets above, primarily in the computation hardware and the nuclear fuel line. As in-situ closure improves across generations, the vitamin inventory shrinks, progressively reducing the minimum seed mass that a future generation must carry.

---

## 13. Conclusion

The vehicle paper and its two engineering companions close the conceptual and first-order quantitative case for the self-replicating interstellar probe. This paper supplies the per-subsystem detail they deferred.

The ~3,700 kg reference seed is dominated by two items: the ISRU and manufacturing plant (~2,000 kg, 54%) and the radiation shadow shield (~400 kg, 11%). The reactor, conversion machinery, braking sail, computation, and structure together account for the remaining 35%. This distribution confirms, at the second level of detail, the engineering papers' central finding that mass is set by the *factory*, not the reactor or the payload.

The cruise-mode thermal budget is well-contained: 14 kW of waste heat rejected through ~11 m² of carbon-composite radiator at 400 K, totalling ~30 kg. This is a modest enough structure to carry without compromising the braking or reproduction budgets, and the result is robust to reasonable uncertainties in radiator temperature and emissivity.

The manufacturing mode introduces a qualitative discontinuity. Factory power rising from kilowatts to megawatts demands radiator areas of hundreds to thousands of square metres — two to three orders of magnitude beyond what the cruise seed carries. These radiators are built in situ from local materials; the seed carries the capability to build them, not the radiators themselves. The distinction is the thermal architecture's central result: the seed is a cruise vehicle minimised for transit, not a settlement minimised for manufacturing.

Mass coupling runs through the manufacturing plant fraction. Reducing factory mass is the dominant lever across all four budgets simultaneously: lighter factory means shorter braking, cheaper reproduction, and better R_eff sensitivity to per-stage failures. The bootstrapping paper's L1–L5 closure ladder is the strategy for exploiting this lever across generations.

The computation and archival subsystem, at ~5% of seed mass, is essentially free. The architecture can afford generous cognitive capability, redundant archival storage, and full navigation without affecting any other budget. This headroom is a structural property of the design: in a vehicle dominated by a factory, cognition is cheap.

---

## References

Andrews, D. G., & Zubrin, R. M. (1990). Magnetic sails and interstellar travel. *Journal of the British Interplanetary Society*, 43, 265–272.

Freitas, R. A. (1980). A self-reproducing interstellar probe. *Journal of the British Interplanetary Society*, 33, 251–264.

Freitas, R. A., & Merkle, R. C. (2004). *Kinematic Self-Replicating Machines.* Landes Bioscience.

Frisch, P. C., Redfield, S., & Slavin, J. D. (2011). The interstellar medium surrounding the Sun. *Annual Review of Astronomy and Astrophysics*, 49, 237–279.

Metzger, P. T., Muscatello, A., Mueller, R. P., & Mantovani, J. (2013). Affordable, rapid bootstrapping of the space industry and solar system civilization. *Journal of Aerospace Engineering*, 26(1), 18–29.

NASA. (1982). *Advanced Automation for Space Missions.* (NASA Conference Publication 2255, reprinted by the University of Santa Clara.)

Poston, D. I., Gibson, M. A., Sanchez, R. G., & McClure, P. R. (2020). Results of the KRUSTY nuclear system test. *Nuclear Technology*, 206 (Suppl. 1), S89–S117.

Redfield, S., & Linsky, J. L. (2008). The structure of the local interstellar medium. IV. Dynamics, morphology, physical properties, and implications of cloud-cloud interactions. *Astrophysical Journal*, 673(1), 283–314.
