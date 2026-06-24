# AI Galaxy Traveler — Candidate Papers Backlog

*Standing list of possible future papers for the deep-time interstellar AI probe series. Compiled from the papers' own forward-references and from the cross-paper consistency review's gap analysis. Updated 2026-06-24.*

---

## Where the series stands (9 papers written)

1. **Vehicle** — "Growth, Not Speed" (the body)
2. **Payload** — "The Payload" (the mind)
3. **Bootstrapping** — "From Seed to Factory" (the hands)
4. **Analytical engineering** — "Engineering Closure"
5. **Computational engineering** — "Engineering Closure, Computed"
6. **DNA mission-ledger** — "DNA Mission Ledgers"
7. **Governance** — "Contact, Contamination, and Noninterference"
8. **Governed amendment** — "Amending the Unamendable"
9. **Fermi synthesis** — "Slow Fire, Silent Galaxy"

The candidates below are *not yet written*.

---

## Group A — Promised by the existing papers

These are already pointed at by the series and are the most natural next steps.

- **Lineage network / information-sharing.** The delay-tolerant galactic network, messenger-probe "sneakernet," and horizontal (Lamarckian) propagation of design improvements across the lineage. The vehicle paper explicitly flags it as "a subsequent paper," the payload paper sketches the network, and the Fermi synthesis leans on it. *Most anticipated missing sibling.*
- **Deep-time navigation & astrometry.** Targeting and routing to stars whose positions drift over megayears; the vehicle paper notes a mature model must propagate stars through the Galactic potential rather than treating the stellar substrate as static.
- **Full subsystem mass / power / thermal / radiator budget.** The detailed per-subsystem bill of quantities the vehicle paper promised as "a dedicated engineering paper"; the two engineering papers still defer it (they work at order-of-magnitude / seed-total level).

---

## Group B — Surfaced in the cross-paper consistency review

These became evident only on reading the whole series together.

- **Knowledge-growth metric.** The series' figure of merit is "growth, not speed," yet no paper quantifies knowledge accumulation — what the probe learns, at what rate, and how "growth" is measured. The payload paper defines "knowledge" but models no growth curve. *Closes the series' own missing yardstick — strongest single gap.*
- **Settlement-scale power & industrial-energy budget.** The series budgets the ~4 kW cruise/cognition reactor and notes launch needs kW–MW, but never the settlement's industrial power (factory, ISRU, mass-driver launches). The R_eff offspring count is a free input with no energy/throughput model beneath it.
- **Timekeeping & temporal ordering across the lineage.** How nodes keep time, order events, and timestamp across light-delay (and mildly relativistic) separation. The ledger assumes "eventual consistency" but never builds the clock/ordering model.
- **Probe-vs-probe security / adversarial defense in depth.** Defending the archive and core against a sophisticated adversary — including another von Neumann lineage. Governance E7 and the amendment paper's "coerced amendment" name hostile agents; the Fermi paper names a "predatory expansion" regime; none develops the defense.
- **Settlement-scale failure & resurrection.** The middle case between component self-repair (Class I–V) and lineage extinction (R_eff): a settlement that partially collapses and must rebuild itself from its DNA archive.
- **Internal allocation / the "economics" of a settlement.** What governs a settlement's split of effort among self-maintenance, science, archive refresh, and reproduction — i.e., what actually sets the offspring count that drives R_eff.
- **Validation / technology-readiness roadmap.** How the architecture could be incrementally tested — precursor missions, in-solar-system demonstrators, what is prototypable now versus what waits on high-closure manufacturing. The series is all destination, no on-ramp.
- **Ethics of creating the lineage.** Whether it is justified to launch an unsupervised, self-replicating lineage that outlives and acts beyond its creators — Sagan & Newman's actual objection, named in the Fermi paper but never met head-on.
- **Very-deep-time terminal state.** Heat death, the last usable energy, and what "carry knowledge forward" means when there may be no future recipient. A philosophical capstone beyond even the Fermi synthesis.
- **Lineage divergence / speciation.** The long-run evolution of the lineage into multiple probe "species," cultural/design drift, and whether that divergence is failure or success. Named as a failure mode in the amendment and Fermi papers, never examined on its own.

---

## Absorbed / no longer separate

- **Planetary Protection for Autonomous Probes** — folded into the governance paper ("Contact, Contamination, and Noninterference"), which covers it via the E0–E7 ladder and the capability-yes/release-no rule.

---

## Suggested priority

1. **Knowledge-growth metric** — it closes the series' own figure of merit; highest leverage.
2. **Lineage network / information-sharing** — already promised, and the Fermi synthesis depends on it.
3. **Full subsystem budget** and **deep-time navigation** — the remaining concrete engineering gaps the vehicle paper flagged.

Then the rest of Group B as appetite allows. Full rationale and the prioritized consistency-fix list are in `papers/interstellar_AI_series_consistency_review.md` in the project repo.
