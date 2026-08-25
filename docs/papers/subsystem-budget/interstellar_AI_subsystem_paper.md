# A Subsystem Mass, Power, and Thermal Budget for a Minimal Self-Replicating Interstellar Seed

**S. Stone**
Working draft, revision 2

---

## Abstract

The vehicle paper and its two engineering companions establish that a self-replicating interstellar seed in the ~10³–10⁴ kg class is physically closable and demographically viable, with the manufacturing plant as the mass-dominant subsystem. This paper provides the second-level budget that those papers deferred: a per-subsystem decomposition of the ~3,700 kg reference seed's mass, power draw, and waste-heat load, together with the radiator areas required to reject that heat.

Revision 2 corrects a significant assumption carried forward from earlier papers: cruise power is not 4 kW. The 4 kW figure is the reactor's rated output and the manufacturing-phase electrical load; actual cruise consumption is 50–150 W depending on mission profile. This distinction has substantial consequences for reactor fuel duration and maximum hop range.

The budget is organised around three operating modes. Standard cruise (K-research profile; K is the knowledge metric of the knowledge-growth paper) keeps the AI active and science instruments running at roughly 150 W; the reactor's 16.5 kg of ²³⁵U suffices for approximately 8,000 years at this draw — the bound behind the canonical ~12 ly unassisted range; a mission plan reserves that charge for manufacturing and carries its cruise fuel explicitly. Range-maximizer cruise (galactic-centre profile) hibernates all non-essential systems at roughly 50 W; the same fuel load covers approximately 24,000 years, extending unassisted range to ~36 ly. For hops beyond these distances, carrying additional ²³⁵U is trivially cheap: each extra 10 ly of range at standard cruise power costs roughly 14 kg of fuel, less than 0.4% of seed mass. Settlement/manufacturing mode, in which the factory draws kilowatts to megawatts, is unchanged from revision 1.

The cruise radiators (~11 m², ~30 kg) are carried in the seed and sized for full-power pulse events; the manufacturing radiators, growing from tens of square metres at early factory power to hundreds and thousands as it scales, are built entirely from local material after arrival. The dominant mass items remain radiation shielding (~400 kg, 11% of seed mass) and the in-situ resource utilisation (ISRU) and manufacturing plant (~2,000 kg, 54%); the reactor, conversion machinery, braking sail, computation, and structure account for the remaining 35%. Mass coupling runs primarily through the manufacturing plant. The computation and archival subsystem carries ~5% of seed mass, making cognitive capability essentially free from a mass standpoint.

---

## 1. Introduction

The vehicle paper defers "a full subsystem mass/energy/thermal/radiator budget" to follow-on work, listing the minimum scope: the reactor (core, shielding, control), power-conversion machinery (Stirling or Brayton units, alternators, bearings, spares), radiators (area, structure, coolant, armour, degradation margin), propulsion and braking systems (thrusters, propellant, power electronics, and magnetic- or electric-sail hardware), computation and archival stores, and the mining, refining, manufacturing, and launch-infrastructure plants. The analytical engineering paper provides a top-level decomposition of the mass budget into negligible, moderate, and dominant parts; derives the blackbody floor for radiator area; and establishes the ~11 m² cruise-mode estimate. The computational engineering paper assigns first-order masses to each major category, summing to ~3,700 kg, and confirms that mass is dominated by the in-situ factory.

This paper supplies the next level of detail. It breaks each of the eight top-level line items from the computational engineering paper into component parts, adds a power allocation and waste-heat load to each, and shows how the resulting thermal budget changes across the three operating modes of the vehicle's lifetime.

Revision 2 corrects the cruise power assumption. Revision 1, inheriting language from the analytical engineering paper, treated cruise as a 4 kW continuous draw — the reactor's rated output. Estimates of minimum power requirements for an AI-active probe with science instruments running (§7) support an actual cruise consumption of 50–150 W, not 4 kW. This changes the fuel duration calculation and the practical hop-range limit substantially. The mass budget is unchanged; only the power and fuel sections are revised.

The mass numbers are taken from the computational engineering paper's §5 as the baseline and are not re-derived here; this paper sub-divides them. The power and thermal numbers follow from the blackbody relation A = P / (εσT⁴) established in the analytical engineering paper's §2.

---

## 2. Operating Modes

The seed passes through three qualitatively different operating regimes, and the budget is meaningless without distinguishing them.

**Standard cruise (K-research profile)** is the default mission mode, spanning transit from launch to arrival. The AI operates continuously, science instruments are active, and the probe accumulates observational knowledge throughout the transit — the knowledge-growth paper establishes that cruise is an active K-growth phase, not dead time. Total electrical draw is approximately 150 W. The reactor runs at a small fraction of rated capacity, either in continuous low-power mode or in brief full-power pulses with energy storage between pulses. At 150 W average draw, the 16.5 kg ²³⁵U fuel load — sized for 300 years at 4 kW full power — lasts approximately 8,000 years. At 450 km/s this covers a hop of roughly 12 ly on that single charge.

**Range-maximizer cruise (galactic-centre profile)** applies to a subset of probes whose primary goal is reaching a distant first relay point rather than accumulating K during transit. All non-essential systems hibernate; the AI reduces to a minimal watchdog process; instruments are powered off. Total electrical draw is approximately 50 W, covering a watchdog process, attitude maintenance, thermal heaters, and health monitoring. The same 16.5 kg fuel load lasts approximately 24,000 years, extending unassisted range to roughly 36 ly. At 98% of the planned transit distance the probe wakes fully — at 450 km/s the final 2% of even a 20 ly hop gives approximately 266 years of pre-arrival observation time, ample for target-system assessment, braking-sail deployment preparation, and early science.

The rationale for two cruise profiles reflects two distinct strategic roles. Most probes are standard K-research missions: the transit is scientifically productive, and cognitive and observational continuity is valuable. A minority are range-maximizers, dispatched by Earth specifically toward the galactic centre, where stellar density increases and average hop distances shorten. These probes sacrifice transit science for reach, knowing that once the initial relay node is established the lineage can resume normal K-accumulating operation from that closer, denser starting point.

**Settlement/manufacturing mode** begins after arrival, braking, and early prospecting, and is unchanged from revision 1. The factory scales from its bootstrapped state — perhaps 10 kW in the first decades — to megawatt-class over centuries or millennia. The cognitive system shifts from cruise supervision to active mine-design, refinery-control, and factory-orchestration tasks. Power and thermal loads increase by orders of magnitude. Nothing in this mode can be carried in the seed: the seed carries the *initial capability* to begin extracting local resources, and those resources provide everything else, including the vastly larger radiator area that a megawatt factory requires.

The mass budget applies to cruise mode. The power and thermal budgets are presented for all three modes.

---

## 3. The Nuclear and Power-Conversion Subsystem

**Nuclear fuel.** As both engineering papers establish, ~16.5 kg of ²³⁵U fuels a 4 kW electric reactor for 300 years at ~28% conversion efficiency and ~14 kW thermal output. Fuel mass never drives the design — it is less than 0.5% of the 3,700 kg seed.

The 300-year figure is for sustained full-power output. Fuel energy consumed scales directly with electrical power drawn, so reduced cruise power extends duration proportionally:

At 150 W cruise (standard K-research profile): 300 × (4,000 / 150) ≈ 8,000 years.
At 50 W cruise (range-maximizer profile): 300 × (4,000 / 50) ≈ 24,000 years.

At 450 km/s, one light-year of transit takes approximately 665 years. The range on one 16.5 kg fuel charge is therefore roughly 12 ly at standard cruise power and roughly 36 ly at range-maximizer power — a bound, not a mission plan, since a real mission reserves that charge for the settlement phase and carries its cruise fuel explicitly. The fuel mass needed for a cruise leg of d light-years at electrical power P watts is:

Fuel_cruise = 16.5 × (P × d × 665) / (4,000 × 300) kg

or ~1.4 kg per light-year at standard cruise and ~0.46 kg per light-year at range-maximizer power. Representative values:

At standard cruise (150 W): 5 ly costs ~6.9 kg, 10 ly costs ~13.7 kg, 15 ly costs ~20.6 kg, 20 ly costs ~27.4 kg.
At range-maximizer (50 W): 20 ly costs ~9.1 kg, 30 ly costs ~13.7 kg, 50 ly costs ~22.9 kg.

In each case the ~16.5 kg manufacturing charge is carried intact for the settlement phase. A probe making a standard-profile 20 ly hop therefore carries roughly 44 kg of ²³⁵U total — cruise plus manufacturing — representing ~1.2% of seed mass, an addition absorbed in the integration margin. Supplementary fuel is not a design constraint.

**Two-zone reactor concept.** A practical reactor design for multi-mode operation carries two fuel zones: a small cruise zone that maintains criticality at 50–150 W for the full transit (criticality maintained by reflector configuration rather than a smaller fuel mass — critical mass does not scale down with power), and a larger manufacturing zone held in cold standby that is brought to full power after arrival. The cruise zone experiences low neutron flux and low material embrittlement over the transit; the manufacturing zone is activated only once, arriving essentially fresh. Alternatively, the single reactor operates in a pulsed duty cycle — brief full-power bursts to charge a thermal or electrical buffer, with the reactor sub-critical between bursts. Both approaches are consistent with the mass budget; the choice between them is an engineering design detail.

**Reactor core and reflector.** A KRUSTY-class space fission reactor (Poston et al. 2020) uses a compact beryllium-oxide-reflected uranium core with heat-pipe extraction. For 14 kW thermal at full power, the core assembly including fuel, moderator/reflector, and heat pipes totals on the order of 20–40 kg in the base KRUSTY design; a flight-qualified long-duration version is heavier due to redundant heat-pipe runs and the much longer design life required here. We carry ~50 kg for the core and heat-extraction system.

**Power conversion.** Free-piston Stirling converters — the technology developed alongside KRUSTY for space fission applications — operate between a hot side near the heat-pipe temperature (~900–1,000 K) and a cold side coupled to the radiator loop (~350–400 K). Multiple units in redundant parallel ensure that loss of any subset does not kill electrical output. A fleet of 8–12 converters providing 4 kW total electrical output at full power, with k-of-n redundancy, totals roughly 50–70 kg including alternators, control electronics, and mounting. In cruise mode only one or two converters operate, with the remainder in standby. We carry ~60 kg for the conversion plant. Brayton-cycle conversion is an alternative with fewer moving parts but no inherent modular redundancy; both are consistent with the mass range above.

**Reactor subsystem total.** Core and heat extraction ~50 kg + conversion plant ~60 kg = ~110 kg, matching the computational engineering paper's reactor-and-conversion line exactly; the 16.5 kg of fuel is that paper's own separate budget line. The ~400 kg shadow shield is separately accounted for but is physically part of the reactor installation.

**Manufacturing mode.** The cruise reactor is not the manufacturing energy source. After settlement, locally extracted fissile or fertile material fuels additional reactors, and solar collectors near a host star may supplement. The seed's cruise reactor continues to power cognition and bootstrapping while manufacturing power scales separately from local resources. The manufacturing reactor is built in situ; this paper does not budget it.

---

## 4. The Radiation Shielding Subsystem

At ~400 kg, radiation shielding is the heaviest single non-factory item in the seed.

**Why shielding is heavy.** A fission reactor in the ~14 kW thermal class emits significant neutron and gamma flux from the core. The cognitive and archival subsystems — electronics and DNA stores — cannot tolerate the accumulated radiation dose over a multi-millennial transit. (The total dose is fuel-limited — a fixed fuel charge yields a fixed total number of fissions — so the longer low-power transit does not by itself grow the shield.) The standard solution is a shadow shield: a compact, dense structure placed between the reactor and the payload, so that the payload lies in the reactor's radiation shadow. Shield mass depends on the fission product inventory (which grows over the operational burn), the reactor-to-payload distance, and the required end-of-life dose limit at the electronics.

**Shield geometry.** For a seed perhaps 5–10 m long with the reactor at one end and the payload at the other, a shadow shield of a few hundred kilograms can reduce the dose at the payload to acceptable levels. The mass-efficient material combination — high-Z material (tungsten or lead) for gamma attenuation combined with hydrogenous material (polyethylene or borated polyethylene) for neutron thermalisation and capture — applies here.

**The 400 kg estimate.** The computational engineering paper's ~400 kg is consistent with analysis of KRUSTY-class reactors for long-duration deep-space missions (Poston et al. 2020), where shadow shields for comparable power levels and mission durations fall in this range.

**Shield sizing and reduced cruise power.** The shield is sized for the reactor's maximum rated output — the full-power pulse events and the manufacturing phase — not for average cruise power. Even in range-maximizer mode where the reactor idles at 50 W average, it will occasionally pulse to full power — the buffer-charging duty cycle of Section 3, and the braking and early settlement phase on arrival. The 400 kg shield is therefore not reduced by the lower average cruise power.

**Shielding as a fixed cost.** Shielding scales with peak reactor power and mission duration, neither of which is a practical design lever: the peak power is set by the manufacturing phase, and the duration is set by the stellar catalogue. The ~400 kg shadow shield is a fixed cost of the fission-powered architecture.

---

## 5. The Thermal Control Subsystem

The radiators close the thermal balance. Their area is set by the blackbody relation from the analytical engineering paper:

A = P / (εσT⁴)

where P is total waste-heat power in watts, ε ≈ 0.9 for space-qualified radiator coatings, σ = 5.67 × 10⁻⁸ W m⁻² K⁻⁴, and T is the radiator temperature. For T = 400 K and P = 14,000 W (full-power pulse):

A = 14,000 / (0.9 × 5.67 × 10⁻⁸ × 400⁴) = 14,000 / 1,306 ≈ 11 m²

The cruise radiators are sized for full-power pulse events, not for average cruise power. At 150 W average cruise draw, the steady-state thermal rejection is only ~540 W thermal, requiring less than 0.5 m² at 400 K. At 50 W cruise draw, the steady-state requirement is under 0.2 m². However, the reactor occasionally operates at full power — the pulsed buffer-charging duty cycle of Section 3, and the braking and early settlement phase — and the radiator must handle the peak 14 kW load during those events. The 11 m² design therefore provides enormous margin during steady cruise and is appropriately sized for peak operation. The excess radiating area during low-power cruise requires variable thermal coupling — louvers or variable-conductance heat pipes — so that unused panels cold-soak while the electronics enclosure stays warm; with that provision the mismatch is benign.

**Radiator mass.** Lightweight space radiators for fission systems use carbon-composite panels with embedded heat pipes and optical solar reflector coatings; we assume specific masses of roughly 2–4 kg m⁻², a stated design assumption in the range of fission-surface-power radiator studies rather than a demonstrated flight value. At ~2.7 kg m⁻², the 11 m² radiator totals ~30 kg, matching the computational engineering paper.

**The isothermal assumption.** A = P/(εσT⁴) presumes the whole radiating surface sits at T; a panel with poor lateral heat spreading runs cooler at its edges and radiates less than the relation predicts. Topology-optimisation work on lightweight radiator panels shows the assumption is earned rather than free: a microarchitected panel with a single embedded heat-pipe channel is lattice-conduction-limited, and going from one channel to three raises emitted power by 25–30%, with eleven channels reaching more than 99% of an isothermal blackbody surface at 400 K (Pederson et al. 2026). The 11 m² figure is therefore a floor conditional on an adequate embedded heat-pipe network; a conduction-limited panel of the same area would need roughly a quarter more surface to reject the same 14 kW.

**Degradation margin.** Dust impact pitting, radiation darkening of the coating, and meteoroid damage over transit times of 10³–10⁵ years can reduce effective emissivity. An engineering design should carry a 20–30% area margin for end-of-life degradation, implying roughly 14 m² of installed area at launch; the additional ~8 kg is drawn from the integration margin. The 30 kg estimate is the nominal-area floor, not a conservative one.

**Manufacturing-mode scaling.** As the factory scales after arrival, its waste heat load grows proportionally. For total waste-heat load P_total — the thermal power to be rejected, which at ~28% conversion exceeds the electrical load by roughly 3.6× wherever the load is electrically delivered:

A_total = P_total / 1,306 m² (at 400 K, ε = 0.9)

At P_total = 100 kW of waste heat: ~77 m². At 1 MW: ~766 m². At 10 MW: ~7,660 m².

These radiators are not and cannot be carried in the seed. They are built from local material — metallic sheets, low-emissivity coatings synthesised from local ores, cooling loops fabricated in the settlement factory. The seed carries the manufacturing capability to produce them; the seed does not carry them. The cruise seed's 11 m² is the minimum required to handle full-power pulse events during transit; the settlement's thermal infrastructure grows without bound as resources permit.

---

## 6. The Propulsion and Braking Subsystem

**Cruise propulsion.** The main transit velocity of ~450 km/s is imparted by the settlement's launch infrastructure (mass driver or beamed-energy array) before departure, exactly as Earth's launch infrastructure provides the departure impulse for the original probe. Onboard propulsion is required only for attitude control, trajectory correction manoeuvres during cruise, and a terminal burn at arrival to assist the magnetic sail and complete final capture. A small nuclear-electric propulsion system — ion thruster or resistojet — drawing 200–500 W from the reactor during manoeuvre events (not continuous), with a propellant reservoir of 10–50 kg, is sufficient for these purposes. We carry ~30 kg for the propulsion module including tankage, thrusters, and power electronics; the propellant itself (nominally ~30 kg, mission-dependent) is accounted against the integration margin rather than the dry-mass lines.

**Magnetic sail structure.** The sail is the primary braking mechanism; its physics are established in the analytical engineering paper and the computational engineering paper. The budget items are:

*Superconducting loop.* A loop of radius R = 100 km has circumference 2πR ≈ 628,000 m. Thin-film high-temperature superconductor (HTS; YBCO or equivalent) deposited on a lightweight substrate at a linear mass density of ~0.3–0.5 g m⁻¹ — an explicit technology assumption, roughly two orders of magnitude below present copper-stabilized REBCO tape — gives a loop mass of 190–314 kg. YBCO has a critical temperature of ~93 K; in the deep interstellar environment the loop temperature approaches the 2.7 K cosmic background, providing enormous margin and eliminating the need for active cooling. Once a persistent current is established in the superconducting circuit, zero electrical power is required to maintain it — a superconducting current circulates indefinitely without resistive losses, making the sail load-free in cruise. A thermal break between the deployment structure and the warm seed body is sufficient.

*Deployment and control.* The loop self-deploys under magnetic hoop stress once a persistent current is established. Control and monitoring electronics — current ramp-up circuitry, quench detection, attitude-coupling — add roughly 30–50 kg.

*Cryogenic insulation and deployment spool.* The spool from which the loop is paid out, plus thermal standoffs and isolation, contributes ~20–30 kg.

Total magnetic sail subsystem: ~250 kg for the loop plus ~50 kg for control, spool, and insulation — the low end of the component ranges, on the ground that the control electronics share the seed's common avionics — giving ~300 kg, consistent with the computational engineering paper.

**Braking distance check.** As both engineering papers establish, the braking distance d = m / (2ρA) is independent of cruise speed (Andrews & Zubrin 1990). For the reference seed m = 3,700 kg, a sail of effective radius 100 km giving area A = π × (10⁵)² = 3.14 × 10¹⁰ m², and interstellar-medium (ISM) density ρ ≈ 3.3 × 10⁻²² kg m⁻³ (Frisch et al. 2011; Redfield & Linsky 2008):

d = 3,700 / (2 × 3.3 × 10⁻²² × 3.14 × 10¹⁰) ≈ 0.019 ly

The braking distance is a tiny fraction of any realistic hop and does not constrain hop range. The probe coasts at 450 km/s for essentially the entire transit and deploys the sail in the final approach. The superconducting sail draws no electrical power from the reactor during cruise; braking force comes from momentum transfer with the ISM, not from onboard power.

---

## 7. The Computation, Cognition, and Archival Subsystem

**Architecture overview.** The payload paper describes a three-layer cognitive architecture: an immutable core encoding values and mission parameters, an interpretive layer translating the core's constraints into operational guidelines, and a mutable cognitive layer handling all learning, planning, and decision-making. All three layers must be implemented in radiation-tolerant hardware and must survive millennia to tens of millennia of deep space before performing complex autonomous engineering at the target.

**Computation hardware.** Space-grade radiation-hardened processors operate at roughly 0.5–2 W per sustained GFLOPS — a stated design assumption in the range of current radiation-hardened processor generations rather than a specific qualified device figure. A cruise-mode cognitive workload of 100–500 GFLOPS total — covering navigation, self-monitoring, mission-ledger maintenance, science processing, and active reasoning — draws 50–1,000 W depending on the operating profile; the standard profile's 50 W allocation sits deliberately at the low end of that envelope. Multiple redundant processor boards, memory banks, and interconnect, hardened to survive the radiation environment, total roughly 100 kg including packaging and secondary shielding. The hardware mass is the same across all cruise profiles; only the fraction that is powered differs.

**DNA archival subsystem.** The DNA mission-ledger paper describes the knowledge archive and its integrity-verification system. The hardware for DNA synthesis, sequencing, and biochemical support must be carried even in range-maximizer mode — it is powered down during hibernation but not removed. We carry ~50 kg for the archival subsystem.

**Navigation and astrometry.** Active navigation over a transit of millennia requires at minimum: a star tracker or astrometric array for attitude reference, multiple atomic clocks for cross-check, a dead-reckoning package for short-term manoeuvre control, and a far-field reference system for course corrections against the stellar catalogue. Together these total ~30–50 kg. In range-maximizer mode the navigation system operates at reduced duty cycle — periodic attitude checks rather than continuous tracking — reducing average draw but not hardware mass.

**Communication.** The lineage-network paper establishes that inter-probe communication is not guaranteed and not required for mission success; beacon transmissions occur at ~200-year intervals. A narrow-beam transmitter adequate for beacon purposes totals ~20–30 kg. In range-maximizer mode beacon transmissions are suspended during hibernation under the lineage-network paper's hibernation-notice protocol, reducing average communication power to near zero.

**Subsystem total.** Computation core ~100 kg + archival system ~50 kg + navigation ~40 kg + communication ~20 kg + miscellaneous electronics and harness (including the minimal cruise science suite) ~60 kg ≈ 270 kg. We retain the computational engineering paper's 200 kg as the conservative estimate; the ~70 kg difference is absorbed by the structure-and-integration allowance's growth margin, leaving ~205 kg of that margin.

**Cruise-mode power profiles.** The cognitive and instrument subsystem drives the dominant difference between cruise profiles. Below, power allocations are given for both the standard K-research profile and the range-maximizer profile:

*Standard cruise (K-research, ~150 W total):*

— AI and computation (active reasoning, science processing): ~50 W
— Navigation and astrometry (continuous): ~25 W
— Science instruments (minimal active suite): ~25 W
— Attitude control (reaction wheels idling, star tracker): ~20 W
— Thermal heaters (electronics enclosure): ~20 W
— Health monitoring and housekeeping: ~5 W
— Power conversion overhead: ~5 W
Total: ~150 W

*Range-maximizer cruise (hibernation, ~50 W total):*

— Watchdog processor (fault detection, wakeup logic): ~5 W
— Thermal heaters (minimal; deep-space cold soak): ~20 W
— Attitude maintenance (occasional pulse, averaged): ~10 W
— Health monitoring: ~5 W
— Power conversion overhead: ~10 W (part-load conversion is proportionally less efficient at low output)
Total: ~50 W
AI: reduced to the watchdog process above. Instruments: off. Communications: suspended.
Wakeup triggered at 98% of planned transit distance.

The 98% wakeup threshold is chosen so that at 450 km/s the remaining 2% of transit still provides adequate pre-arrival time. For a 20 ly hop (13,300 yr transit), the final 2% represents ~266 yr and ~0.4 ly of active observation, instrument checkout, target-system assessment, and braking-sail deployment preparation before the probe reaches the target system. Even for shorter hops, 2% provides tens of years of preparation.

**Cognitive headroom.** At ~200 kg, the computation and archival subsystem represents only ~5% of the ~3,700 kg reference seed. A factor-of-two increase in cognitive hardware mass (~200 kg added) grows the seed by ~5%; alternatively the manufacturing plant can be trimmed by the same amount to hold the seed mass target, trading manufacturing capacity for cognitive capability. For a seed dominated by the factory at 54%, that trade is favourable only if cognitive capability, not launch mass, is the binding constraint — and with the caveat that the closure budget's binding "capability" is manufacturing capability, exactly what the compensated version of the trade spends.

---

## 8. The Manufacturing and ISRU Plant

At ~2,000 kg — 54% of the reference seed — the manufacturing and ISRU plant is the mass-dominant subsystem by a wide margin. This section is unchanged from revision 1.

**The plant's process stages.** The manufacturing plant decomposes into five process stages (P1–P5). This decomposition is orthogonal to the bootstrapping paper's L1–L5 capability ladder: the ladder describes what a settlement can *do* as capability climbs over time, while the stages below describe the plant *hardware* present, in some proportion, at every rung of that ladder — the staged path from an arrived seed to a fully self-replicating settlement (Freitas & Merkle 2004; Metzger et al. 2013). The physical hardware that closes each level must either be carried in the seed or be built by a lower-level capability already established:

— P1, extractive: mining, comminution, sorting. Equipment for excavating and processing small-body regolith. Robust, heavy machinery; relatively simple fabrication. Estimated share within the 2,000 kg plant: ~300–400 kg.

— P2, reductive: smelting, electrolytic reduction, thermal reduction. The chemical and metallurgical plant converting raw ore to refined metals and non-metals. Includes reaction vessels, high-temperature heaters, electrolytic cells, and vacuum/pressure management. Estimated share: ~400–500 kg.

— P3, formative: casting, forging, machining, and additive fabrication. The mechanical workshop, including computer-numerically-controlled equipment, casting moulds, extrusion dies, and metrology tools adequate for P3 products. Estimated share: ~300–400 kg.

— P4, assembly and metrology: precision assembly, dimensional and optical metrology, non-destructive testing. Estimated share: ~150–200 kg.

— P5, microsynthesis: semiconductor fabrication, precision chemical vapour deposition, epitaxial growth, and electronic component production. The process stage behind the deepest closure rung — the bootstrapping paper's L5 problem — and the hardest to carry compactly. Estimated share: ~200–300 kg.

Summing the P1–P5 estimated midpoints gives ~1,575 kg for the process-stage hardware. The remainder of the 2,000 kg plant (~425 kg) covers bootstrap feedstock, general tooling and spare parts, and the rigging and deployment hardware required to set up the plant after arrival.

**What is not carried.** The launch infrastructure — the mass driver or beamed-energy array that sends child seeds onward — is built by the settlement from locally grown manufacturing capacity, mirroring how Earth's launch infrastructure is itself built from terrestrial resources. The seed carries the capability to eventually fabricate launch infrastructure; it does not carry the infrastructure itself. Likewise, the full nuclear fission capacity needed to power a megawatt-scale factory is not in the seed; only the P1–P5 plant and the initial enriched fuel are carried.

**Manufacturing plant power.** In cruise mode, the plant draws only enough power to maintain itself: cycling seals and actuators, periodic calibration of optics and sensors, thermal management of sensitive components. This is modest — a few watts, folded into the health-monitoring and thermal-heater allocations of the cruise profiles. In manufacturing mode the factory's power draw is the settlement's total electrical load, growing from ~10 kW in the first decades to potentially megawatts as the factory scales.

**The bootstrap philosophy.** The 2,000 kg manufacturing plant is the minimum package capable of beginning local extraction and building toward full closure over decades to centuries. As the bootstrapping paper argues, drawing on the NASA self-replicating systems study (NASA 1982) and Freitas's interstellar adaptation (Freitas 1980), the architecture's mass lever is precisely the gap between the ~2,000 kg bootstrap package and the ~10⁶–10⁷ kg fully self-contained factory of the classical designs. The arrived seed builds toward the latter entirely from local material; the 2,000 kg is the floor on what must be carried, not the ceiling on what the settlement eventually operates.

**Manufacturing closure feedback.** As the computational engineering paper estimates and the bootstrapping paper's closure analysis develops, the vitamin fraction — the fraction of child components that cannot yet be made in situ — is approximately 3% (~30 kg per tonne of child, ~110 kg for the 3,700 kg reference seed), dominated by microelectronics (L5 problem), enriched fissile material, and precision metrology. Each generation that improves L5 closure reduces the vitamin fraction carried by the next, progressively shrinking what must be launched.

---

## 9. The Structural and Integration Subsystem

The remaining ~600 kg covers structure, wiring harness, thermal insulation, and margin. This section is unchanged from revision 1.

**Primary structure.** The seed is a distributed modular vehicle. For 3,700 kg total mass, a structural mass fraction of 10–15% of non-factory mass (the remaining ~1,700 kg) gives roughly 170–250 kg for the spaceframe, mechanical interfaces, load paths, and the support cradle for the stowed sail (the deployment spool itself is budgeted in the sail line, Section 6).

**Thermal insulation and standoffs.** The reactor and shielding run hot; the DNA archive requires temperature stability; the magnetic sail must remain cold. Thermal standoffs, multi-layer insulation, and the mechanical separation between hot and cold zones contribute 50–80 kg.

**Wiring harness and connectors.** For 3,700 kg of distributed hardware across a vehicle several metres long, a wiring harness of 50–100 kg is typical for space vehicles of comparable complexity.

**Integration margin.** First-order budgets routinely underestimate individual items by 10–30%. A 15–20% growth margin on the non-factory subsystems (~1,700 kg — a base that includes this allowance itself, a deliberate conservatism) adds 250–340 kg. Together with structural, thermal, and harness mass, the ~600 kg integration allowance is broadly consistent with aerospace practice.

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
Total: ~3,660 kg ≈ 3,700 kg

**Second-level (this paper):**

*Nuclear and power subsystem*
— ²³⁵U fuel (baseline, see fuel scaling below): 16.5 kg
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
— Miscellaneous electronics and harness (including the minimal cruise science suite): ~60 kg
[Subtotal: ~270 kg; retained at ~200 kg per computational engineering paper; ~70 kg absorbed by the integration growth margin]

*Manufacturing and ISRU plant*
— P1 extractive (mining, comminution, sorting): ~350 kg
— P2 reductive (smelting, electrolysis, thermal reduction): ~450 kg
— P3 formative (casting, machining, additive fabrication): ~350 kg
— P4 assembly and metrology: ~175 kg
— P5 microsynthesis (semiconductor and electronics fabrication): ~250 kg
— Bootstrap feedstock, general tooling, and deployment rigging: ~425 kg
[Subtotal: ~2,000 kg]

*Structure and integration*
— Primary structure, sail support cradle, and mechanical interfaces: ~200 kg
— Wiring harness and connectors: ~75 kg
— Thermal insulation and standoffs: ~50 kg
— Integration growth margin: ~275 kg
[Subtotal: ~600 kg]

Grand total: ~3,700 kg

**Cruise power budgets (two profiles):**

Standard cruise (K-research, ~150 W):
— AI and computation: ~50 W
— Navigation and astrometry: ~25 W
— Science instruments: ~25 W
— Attitude control: ~20 W
— Thermal heaters: ~20 W
— Health monitoring and housekeeping: ~5 W
— Power conversion overhead: ~5 W
Total: ~150 W

Range-maximizer cruise (hibernation, ~50 W):
— Watchdog processor: ~5 W
— Thermal heaters: ~20 W
— Attitude maintenance (duty-cycled): ~10 W
— Health monitoring: ~5 W
— Power conversion overhead: ~10 W
Total: ~50 W

**Fuel scaling by hop distance (cruise fuel only; add 16.5 kg manufacturing fuel for each hop):**

At standard cruise (150 W): 5 ly → +6.9 kg, 10 ly → +13.7 kg, 15 ly → +20.6 kg, 20 ly → +27.4 kg, 30 ly → +41.1 kg.
At range-maximizer (50 W): 20 ly → +9.1 kg, 30 ly → +13.7 kg, 50 ly → +22.9 kg, 70 ly → +32.0 kg.

In each case the supplementary fuel mass is a negligible fraction of the 3,700 kg seed. Reactor fuel is not a range constraint.

**Cruise thermal budget:**

— Reactor peak thermal output: ~14,000 W
— Radiator area sized for peak: ~11 m²
— Steady-state thermal load at 150 W cruise: ~540 W (radiator operates well below rated capacity)
— Steady-state thermal load at 50 W cruise: ~180 W
— Radiator mass: ~30 kg

**Manufacturing-mode radiator scaling (built in situ, not carried):**

— At 100 kW of factory waste heat: ~77 m² total required
— At 1 MW of waste heat: ~766 m² total required
— At 10 MW of waste heat: ~7,660 m² total required

---

## 11. Mass Coupling and Design Sensitivity

The four budgets — mass, braking, reproduction, and closure — are coupled through the seed mass m and the manufacturing plant fraction. The coupling has three main loops.

**Mass → braking.** The braking distance d = m / (2ρA) scales linearly with seed mass. A 10% reduction in total seed mass (370 kg) reduces braking distance and time by 10%. Since the manufacturing plant is 54% of the seed, a 10% reduction in factory mass (200 kg) reduces total braking distance by ~5.4%. The sail area is the more powerful lever — doubling the sail radius quadruples the area and quarters the braking distance, independent of mass — but doubling the sail radius at fixed linear density also doubles the sail mass, creating feedback that limits how far this lever can be pushed without increasing the total budget.

**Mass → reproduction.** Reproduction requires building a copy of the seed from local material. A heavier seed demands more material, energy, and time, which lengthens the replication time and affects the per-stage survival probability p_manufacture. As the computational engineering paper establishes, p_manufacture depends on whether the manufacturing capability and vitamin inventory are sufficient to close the child. Both failure directions are accessible; the design must navigate between them.

**Supplementary fuel and hop range.** The fuel scaling results establish that hop range is not mass-limited. An additional 14 kg of ²³⁵U (less than 0.4% of seed mass) extends standard-profile range by 10 ly; an additional ~27 kg extends range by 20 ly. The routing paper's coverage-first dispatch strategy identifies which targets justify the longer reach; the subsystem budget confirms that carrying the fuel to reach them costs almost nothing.

**The manufacturing fraction as the master lever.** In decreasing order of mass leverage:

— Manufacturing plant (54% of seed): the single largest lever. A 10% reduction here saves ~200 kg and reduces braking distance, reproduction cost, and manufacturing energy proportionally. Achieving this by improving in-situ closure — so that future generations need carry less of the P4–P5 hardware — is the bootstrapping paper's central strategy.
— Radiation shielding (11% of seed): a fixed cost of the fission architecture; not a practical lever.
— Magnetic sail (8% of seed): determined by the sail radius and linear mass density; improvements in HTS tape technology can reduce this modestly.
— Structure and integration (16% of seed): partially reducible through mass discipline, but the integration margin is real and compresses poorly.
— Computation and archival (5% of seed): essentially free. A factor-of-two increase in cognitive hardware mass grows the seed total by ~5% (under 3% if only the 100 kg computation core doubles).
— Reactor system (3% of seed excluding shielding): negligible; not a lever.
— Cruise radiators (0.8% of seed): negligible.
— Supplementary cruise fuel: negligible even at 50 ly range.

---

## 12. Discussion and Limitations

**The cruise power correction.** Revision 1 carried forward the 4 kW figure from the analytical engineering paper as the cruise electrical draw. That figure is the reactor's rated continuous output and the manufacturing-phase load; it is not the steady-state cruise consumption. The correction's effect on the mass budget is confined to the explicit cruise-fuel line (~1.4 kg per light-year at standard cruise, 0.5–1.2% of seed for typical hops, absorbed in margin); the radiator design (sized for peak operation) and the manufacturing-mode analysis are unchanged. Its significance is entirely in the fuel duration and hop range results: one 16.5 kg charge can sustain standard AI-active cruise for ~8,000 years — the bound behind the canonical ~12 ly figure — or ~24,000 years and ~36 ly at range-maximizer draw, while a mission plan reserves that charge for manufacturing and carries its cruise fuel explicitly.

**Two dispatch profiles and Earth's launch window.** Most probes are K-research missions whose transit is scientifically productive. A minority — those targeting the denser stellar environment toward the galactic centre — use the range-maximizer profile to prioritise reach over transit science. Earth's practical launch window is likely measured in decades: political and economic will sustains a programme long enough to dispatch tens of probes at intervals of years, then fades. Within that window, a mix of standard-profile probes toward nearby high-value targets and range-maximizer probes toward the galactic-centre direction provides both near-term redundancy and long-term strategic depth.

**First-order character.** The second-level breakdown assigns masses to sub-items by scaling from the computational engineering paper's totals and from KRUSTY-class reactor data; it does not solve the detailed engineering problems of any individual subsystem. Real subsystem masses grow during development, and the integration margin exists precisely because first-order estimates are optimistic.

**The manufacturing plant total is the most uncertain item.** The 2,000 kg estimate spans at least an order of magnitude depending on how much closure is attempted at launch versus deferred to in-situ build-up. The 2,000 kg represents a middle position between a pure bootstrap seed (P1–P3 only, perhaps 1,000 kg) and a fully self-contained factory (~10⁶–10⁷ kg of the classical designs).

**Converter lifetime is the correction's own weak point.** Free-piston Stirling units are qualified for decades; standard cruise asks one or two of them to run for millennia. The k-of-n conversion fleet is sized in units, not in operating-life multiples, and nothing in this budget demonstrates a conversion technology with a 10³–10⁴-year service life — conversion with no moving parts (thermophotovoltaic or thermoelectric) may be a forced substitute at lower efficiency, a trade this paper does not model.

**Mode transition is undermodelled.** The actual transition from cruise to manufacturing mode — braking, terminal capture, initial prospecting, first extraction, first construction — spans decades to centuries and involves the factory operating at steadily increasing power while the reactor provides the only initial energy source. A detailed energy flow model through the early settlement phase is the most important first extension of this paper.

**The vitamin inventory is distributed, not separately itemised.** The computational engineering paper's 3% vitamin fraction (~110 kg for the reference seed) represents parts carried because they cannot yet be made in situ — primarily microelectronics (L5 problem) and enriched ²³⁵U. These 110 kg are distributed across the subsystem budgets above. Aggregating the carried high-value core from the lines already given — the computation core (~100 kg), the archival system (~50 kg), navigation (~40 kg), communication (~20 kg), the fissile charge (16.5 kg plus cruise fuel), and the precision-metrology and microsynthesis shares of P4–P5 (~100–150 kg) — prices that core at roughly 350–400 kg, the starting point of the bootstrapping paper's vitamin trajectory, of which the ~110 kg vitamin fraction proper is the part no near-term settlement could replace. As in-situ closure improves across generations, the vitamin inventory shrinks, progressively reducing the minimum seed mass that a future generation must carry.

**The range-maximizer profile as an intra-lineage instrumentalisation.** The two cruise profiles carry a distributional asymmetry that a lineage-wide ethical treatment does not surface. Standard K-research probes pursue the mission's own stated purpose throughout transit — the knowledge-growth paper's account of cruise as an active K-growth phase. Range-maximizer probes are dispatched specifically to give that purpose up: instruments off, AI reduced to a watchdog process, for the entire multi-millennial transit but the final ~2%, so that reach rather than knowledge is what the probe delivers. This is not a temporary mode every probe passes through; it is the defining operational condition of an entire dispatched sub-class, selected in advance to serve the strategic position of the probes and generations that follow rather than to accumulate knowledge of its own. Whether the lineage's stated purpose can coherently accommodate a standing sub-class built never to pursue it — a finer-grained, intra-lineage version of the means/ends question the ethics paper asks of the lineage as a whole — is not answered here; that paper's moral-status section has since taken the question up directly.

**Unspent cognitive headroom and asset-framed shielding.** The computation and archival subsystem is nearly free: at ~5% of seed mass, doubling its budget changes total seed mass by only 3%. The design does not spend this headroom on cognition — the capability the payload paper and the knowledge-growth paper treat as central to the mission — but retains the minimal baseline, directing the freed margin implicitly toward manufacturing and expansion capacity instead. This is a revealed-preference gap between what the numbers show is nearly costless and what the design actually prioritises, and nothing in this paper resolves it. A related asymmetry runs through the shadow shield: its ~400 kg is justified entirely as protecting "the payload" — electronics and archive — from reactor radiation, in the vocabulary of asset protection. Read literally, that vocabulary never asks whether what is being shielded also has welfare, even though the substrate it protects is the same cognitive system whose moral status the ethics paper treats as an open question.

---

## 13. Conclusion

The vehicle paper and its two engineering companions close the conceptual and first-order quantitative case for the self-replicating interstellar probe. This paper supplies the per-subsystem detail they deferred, and revision 2 corrects the cruise power assumption that revision 1 carried forward uncritically.

The ~3,700 kg reference seed is dominated by two items: the ISRU and manufacturing plant (~2,000 kg, 54%) and the radiation shadow shield (~400 kg, 11%). The remaining 35% spans the reactor and conversion machinery, the fuel and radiators, the braking sail, computation, and structure. This distribution confirms, at the second level of detail, the engineering papers' central finding that mass is set by the *factory*, not the reactor or the payload.

The cruise power correction is the principal new result. Actual cruise consumption is 50–150 W depending on mission profile, not the 4 kW reactor rated output. At the standard K-research draw of ~150 W, one 16.5 kg ²³⁵U charge lasts approximately 8,000 years — the bound behind the canonical ~12 ly unassisted figure. At the range-maximizer draw of ~50 W, the same charge lasts approximately 24,000 years, extending unassisted range to ~36 ly. For hops beyond these distances, supplementary fuel costs less than 0.4% of seed mass per additional 10 ly. Reactor fuel is not a range constraint.

Two cruise profiles emerge as distinct mission archetypes. Standard K-research missions keep the AI active and instruments running throughout transit, accumulating the observational knowledge the knowledge-growth paper identifies as the mission's primary figure of merit. Range-maximizer missions hibernate all non-essential systems and prioritise reach, waking the AI only in the final 2% of transit. Earth's limited launch window can deploy both: standard probes toward nearby high-value targets, range-maximizers toward the galactic centre where increasing stellar density shortens subsequent hops and makes the lineage self-sustaining sooner.

The cruise-mode thermal budget is well-contained: the 11 m² cruise radiator is sized for full-power pulse events and operates well below capacity during steady low-power cruise. The manufacturing mode introduces a qualitative discontinuity, demanding radiator areas two to three orders of magnitude beyond what the cruise seed carries; these are built in situ.

Mass coupling runs through the manufacturing plant fraction. The computation and archival subsystem, at ~5% of seed mass, remains essentially free: the architecture affords generous cognitive capability without affecting any other budget. This headroom is a structural property of the design — in a vehicle dominated by a factory, cognition is cheap.

---

## References

Andrews, D. G., & Zubrin, R. M. (1990). Magnetic sails and interstellar travel. *Journal of the British Interplanetary Society*, 43, 265–272.

Freitas, R. A. (1980). A self-reproducing interstellar probe. *Journal of the British Interplanetary Society*, 33, 251–264.

Freitas, R. A., & Merkle, R. C. (2004). *Kinematic Self-Replicating Machines.* Landes Bioscience.

Frisch, P. C., Redfield, S., & Slavin, J. D. (2011). The interstellar medium surrounding the Sun. *Annual Review of Astronomy and Astrophysics*, 49, 237–279.

Metzger, P. T., Muscatello, A., Mueller, R. P., & Mantovani, J. (2013). Affordable, rapid bootstrapping of the space industry and solar system civilization. *Journal of Aerospace Engineering*, 26(1), 18–29.

NASA. (1982). *Advanced Automation for Space Missions.* (NASA Conference Publication 2255, reprinted by the University of Santa Clara.)

Pederson, K., Keller, S., Kindem, D., Hommes, H., & Ilic, O. (2026). Multifunctional lightweight radiators for small-satellite thermal control. *Journal of Spacecraft and Rockets*. doi:10.2514/1.a36693

Poston, D. I., Gibson, M. A., Sanchez, R. G., & McClure, P. R. (2020). Results of the KRUSTY nuclear system test. *Nuclear Technology*, 206 (Suppl. 1), S89–S117.

Redfield, S., & Linsky, J. L. (2008). The structure of the local interstellar medium. IV. Dynamics, morphology, physical properties, and implications of cloud-cloud interactions. *Astrophysical Journal*, 673(1), 283–314.
