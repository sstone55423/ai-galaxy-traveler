# Revision Plan — Interstellar AI Probe Paper

Response to astrophysicist reviewer comments. Items are prioritized P1 (highest)
to P11. Each lists the change, effort (S/M/L), the decision taken, and status.
A short "Disagreements" section records where we pushed back on the reviewer.

## Prioritized changes

**P1 — Soften the categorical claims (precision pass). [S] — DOING NOW.**
Replace absolute statements with graded ones: gravity-assist threshold becomes a
graded deflection criterion (turn angle ∝ v⁻²; depends on hyperbolic-excess speed
and survivable periapsis, not a hard on/off); "uniquely compatible" → "most
internally consistent"; "must be slow" → "must remain in the few-hundred-km/s
regime"; "the same reactor for propulsion and computation" → both favor fission
but at different power scales; "repair is most of the way to replication" →
"necessary but not sufficient"; "deep time is the resource" → keep, add "only if
failure, corruption and replication error are actively controlled."

**P2 — Braking/capture + the settlement-factory architecture. [M] — DOING.**
Decision: the slow probe **brakes and stops**; braking is feasible *because* it is
slow (stopping Δv scales with speed — ~67× less than a 0.1c probe — so magnetic/
electric-sail drag against the stellar wind plus gravity capture becomes viable).
An arrived probe **becomes a stationary settlement/factory**; it does not travel
onward. The colonization frontier advances through the *children* it builds, not
the parent. This reconciles the earlier "the probe doesn't stop" framing: the
*lineage* keeps moving even though each settled node is fixed.

**P3 — Child-probe launch + separate launch Δv from onboard cruise. [M] — DOING.**
Decision: children are launched from **settlement-built launch infrastructure**
(a mass driver or beamed array, and/or a powered Oberth pass of the *local* star)
— mirroring how the first probe leaves Earth. Onboard nuclear-electric is used
only for trajectory trim and terminal braking, not full launch Δv. "Can build a
launcher" therefore becomes part of the replication bill-of-materials (a P7 item).
Also separates the kilowatt-class computation/survival reactor from the much
larger reactor power (or fixed infrastructure) needed for acceleration.

**P4 — Separate fission FUEL mass from reactor-SYSTEM mass. [S] — DOING.**
State plainly: the ~16.5 kg U-235 inventory is the easy part; core, shielding,
power conversion, radiators, control, and spares dominate mass and reliability.

**P5 — Repair-difficulty hierarchy (Class I–V) + repair-replication spectrum. [M] — DOING.**
Add a five-class repair difficulty ladder (modular swap → mechanical fabrication →
high-temperature systems → electronics fabrication → reactor-core refurbishment)
and a closure ratio C = (mass manufacturable in situ)/(child dry mass). Frame
self-repair as a *spectrum* whose top end (Class IV–V) approaches replication.

**P6 — Dust/erosion survivability subsection. [M] — DOING.**
Impact energy ∝ v². A 1 µm grain carries ~700× more energy at 450 km/s than at
Voyager speed, and ~3×10⁶× more at 0.1c (≈4.5 J per grain — like a small pellet).
An independent physical argument *for* slowness.

**P7 — First-order resource-limited replication. [L→first-order] — DOING (first-order).**
Add t_rep = max(t_mine, t_refine, t_manufacture, t_fuel, t_launch) with sensitivity
cases (optimistic 1 kyr / conservative 10 kyr / hard-closure 100 kyr / failed →
"wandering probe only"). Full quantitative model is the **next paper**.

**P8 — Information persistence / fidelity / goal-drift section. [M] — DOING.**
Cover bit-rot, cosmic-ray flips, error-correcting archival kernels, and goal-drift
control across generations. Decision (per D3): Earth-downlink and even inter-probe
communication are **non-goals** for this architecture — each lineage is
self-contained. Network-wide propagation of discoveries / design improvements is
flagged as a **future-paper** direction.

**P9 — Tighten stellar-scooping thermal argument. [S] — DOING.**
Use the ~60 MW/m² grazing heat flux to rule out physical collectors except
electromagnetic geometries. Conclusion ("not a fuel source") unchanged.

**P10 — Mass/energy/radiator budgets. [L] — BRIEF + FUTURE WORK.**
Include only a first-order radiator note (e.g. ~11 m² rejects 14 kW at 400 K;
hundreds of m² at MW-class propulsion power) to discipline P3, and explicitly defer
the complete subsystem budgets to future work (per D1).

**P11 — Local-Group / cosmic-expansion wording precision. [S] — DOING (light).**
Frame the Local Group as the practical domain of *this slow, stepping-stone*
architecture rather than an absolute cosmic limit. Largely already in the draft.

## Disagreements with the reviewer

**D1 (scope — main disagreement).** The reviewer pushes to convert a conceptual
thesis paper into a full first-order *engineering architecture* paper (complete
mass/energy/thermal/radiator/propellant budgets). That is effectively a second,
larger paper. For this pass we recover credibility with the cheap claim-softening
(P1, P4) plus the qualitative gap-fillers (P2, P5, P6, P8); the heavy budgets
(P10, full P7) are scoped as future work, not v2 blockers.

**D2.** P11 is largely already handled in the draft; it is a wording polish, not a
correction of an error — ranked last.

**D3.** The reviewer lists Earth-downlink as a gap. We disagree: for an autonomous
deep-time intelligence, returning data to Earth is **out of scope by design**
(light-millennia delays; Earth's irrelevance after a few centuries). The paper
survives on no communication back to Earth or between probes. Network information-
sharing (improvements found locally flowing back through the lineage) is a genuine
idea but belongs to **additional papers**.

**D4.** "Repair ≠ replication" is right, but a flat statement overcorrects. With the
Class I–V hierarchy, high-end repair-from-raw-material basically *is* replication.
Fix is descriptive: frame self-repair as a difficulty spectrum whose top approaches
replication. (Agreed: a clarity-of-description fix.)

## Status
P1–P9, P11 implemented in paper v2; P7 first-order; P10 brief + deferred. Full
resource-closure model and complete engineering budgets carried to a follow-on
paper.
