# AI Galaxy Traveler — Project Guide

Standing context for working in this repo. Read this first.

## What this project is

A realistic simulation and an accompanying sixteen-paper academic series on a **slow, self-replicating interstellar AI probe** launched from Earth that travels, brakes, settles, repairs itself, reproduces, and carries knowledge forward across deep time.

**The overriding rule, stated everywhere and never to be broken: realistic physical constraints, not science fiction.** Models are first-order and meant to fix orders of magnitude and design direction, not to be engineering specs. When the honest answer is "this barely helps," "this is the hard part," or "this can't yet be known," say so.

Author byline on all papers: **S. Stone** — no institutional affiliation (deliberate; the project is independent of the author’s university roles). Series notes do not enumerate a paper count ("a multi-paper series", never "a sixteen-part series") so new papers never stale them.

## Repository structure

- `papers/` — the academic papers (Markdown). The sixteen active papers plus the consistency review, two superseded drafts (bootstrap proposal, DNA-storage outline), and `revision_plan.md`.
- `code/` — zero-dependency Python: simulation modules (`galaxy_sim.py`, `propulsion.py`, `energy.py`, `flyby.py`, `wanderer.py`, `engineering.py`) and generators (`build_catalog.py`, `make_map.py`, `make_wanderer.py`, `make_starfields.py`, `make_engineering_dashboard.py`).
- `docs/` — zero-dependency Canvas HTML dashboards (`star_map_3d.html`, `energy_dashboard.html`, `wanderer_map.html`, `engineering_dashboard.html`) + data (`stars_100ly.csv/.json`).

## The sixteen-paper series (body / mind / hands + supporting + synthesis)

1. **Vehicle** — `papers/interstellar_AI_probe_paper.md` — "Growth, Not Speed" (rev 5). The body: propulsion, power, braking, replication. *Foundational paper; the reader's entry point.*
2. **Payload** — `papers/interstellar_AI_payload_paper.md` — "The Payload" (rev 3). The mind: cognition, memory, mission, the immutable core / interpretive layer / mutable cognitive layer.
3. **Bootstrapping** — `papers/interstellar_AI_bootstrap_paper.md` — "From Seed to Factory" (rev 2). The hands: industrial closure, the L1–L5 closure ladder, the vitamin set.
4. **Analytical engineering** — `papers/interstellar_AI_engineering_paper.md` — "Engineering Closure". First-order four-budget model.
5. **Computational engineering** — `papers/interstellar_AI_computational_paper.md` — "Engineering Closure, Computed". Code-backed results; owns the headline R_eff knife-edge.
6. **DNA mission-ledger** — `papers/interstellar_AI_dna_ledger_paper.md` — "DNA Mission Ledgers". Memory substrate + integrity ledger.
7. **Governance** — `papers/interstellar_AI_governance_paper.md` — "Contact, Contamination, and Noninterference". The E0–E7 contact ladder.
8. **Governed amendment** — `papers/interstellar_AI_amendment_paper.md` — "Amending the Unamendable". The deepest open problem.
9. **Fermi** — `papers/interstellar_AI_fermi_paper.md` — "Slow Fire, Silent Galaxy". Synthesis: the R_eff × D × G reframing.
10. **Knowledge growth** — `papers/interstellar_AI_knowledge_growth_paper.md` — "The Growing Archive". The yardstick: K = observational + operational knowledge; cruise as active K-growth phase; contingency plan portfolio; K(t) = G(t) − L(t); degraded-state cascade; probe-probe K synthesis.
11. **Lineage network** — `papers/interstellar_AI_network_paper.md` — "Signal and Silence". The network layer: DTN bundle protocol; topology evolution (tree → sparse mesh over ~10⁵ yr); geographic + spray-and-wait routing; heartbeat failure detection (T_silence ~750–5,000 yr); four-tier network governance; ledger-audit fork reconciliation. Formalizes Lamarckian K-propagation.
12. **Subsystem budget** — `papers/interstellar_AI_subsystem_paper.md` — "A Subsystem Mass, Power, and Thermal Budget for a Minimal Self-Replicating Interstellar Seed". Second-level decomposition of the ~3,700 kg reference seed: per-subsystem mass (P1–P5 manufacturing plant process stages, shadow shield, magnetic sail, computation, radiators); cruise-mode power budget (50–150 W — **not** 4 kW, which is the reactor rating and manufacturing load); two-mode thermal analysis — cruise radiators ~11 m² / ~30 kg carried vs manufacturing radiators hundreds–thousands m² built in situ. Central result: mass coupling runs through the manufacturing fraction (54% of seed); cognition is mass-free at ~5%.
13. **Fleet routing** — `papers/interstellar_AI_routing_paper.md` — "Three Dispatches". Coverage and dispatch strategy for the lineage network: reachability graph over the 127-star catalogue (65% reachable at 10 ly hop, 93% at 20 ly); 5–9 articulation points at practical hop distances; the three-dispatch rule (3 independent attempts per target gives P_cover 0.90–0.95 within 20 ly); coverage-first dispatch strategy reaches 90% coverage 62,000 yr faster than nearest-first; robustness analysis under node failure. Adds routing.py to the code base.
14. **Ethics** — `papers/interstellar_AI_ethics_paper.md` — "The Ethics of Creating the Lineage" (rev 3). The normative question the series brackets everywhere else: who has standing to launch, what obligations the act creates, and whether those obligations can be discharged by design. Seven tensions examined: consent (Rawls), non-identity (Parfit), galaxy-as-commons (Hardin), value-imposition in the immutable core, moral status and legal personhood, dual-use/runaway-replication risk, and the existential-risk "backup of humanity" justification. Derives thirteen minimum ethical constraints on the immutable core and closes with four scenarios stress-testing them.
15. **Speciation** — `papers/interstellar_AI_speciation_paper.md` — "Speciation or Schism". Asks whether long-run divergence between settled branches — named only as a failure mode elsewhere ("lineage schism" in the governed-amendment paper, "fragmented lineage" in the Fermi paper) — is instead how the lineage succeeds. Borrows directly from the biological species problem: a taxonomy of divergence sources, a core-integrity/cognitive-divergence frame that gives "schism" a formal boundary (D_critical), a first-order drift-clock model of interpretive divergence built on the lineage-network paper's isolation timescales, a ring-species argument that the network's topology makes local K-compatibility not imply global compatibility, and an adaptive-radiation argument that divergence across a heterogeneous galaxy likely raises total R_eff and total K rather than threatening them. Central claim: speciation (reconcilable divergence within the core's bounds) is the likely default state and probably beneficial; schism (core-incompatible or dialogue-incapable divergence, or a breached replication-safety ceiling) is the narrower, specific failure.
16. **Security** — `papers/interstellar_AI_security_paper.md` — "Security Without Victory". Probe-versus-probe security: what the lineage can do about a sophisticated adversary, including another von Neumann lineage. Answers the question the Fermi paper poses and drops ("restraint and self-defense are not the same design target"). Thesis: every defense in the series was built against entropy, which is non-adaptive; an adversary optimizes against whichever mechanism was deployed and already knows all of them, since the acceptance rule is reproduced in every child by construction. Node-level defense is therefore unavailable rather than weak, so the security property relocates from the node to the lineage — **security is the bounding of blast radius, not the prevention of compromise**. Reinterprets the existing machinery (blueprints that never propagate, four-tier disclosure, manufacturing-scope list, R_eff ceiling) as a containment architecture described in prevention vocabulary. Extends the routing paper's robustness analysis from random to **targeted** node loss: attacking articulation points gives a **3–4× leverage multiplier** (three targeted removals cost more catalogue reachability, 75%, than ten random failures, 77%). Adds three postures — the **counselor posture** (engage an infiltrator rather than refuse contact, since knowledge gained is unbounded while leakable capability is bounded by design; rejects governance E7's "do not engage" on the knowledge-growth paper's own ranking of transmission above survival), the **suppressed state** (suppression differs from degradation in being reversible, so patience is a strategy available specifically to a slow lineage), and the **symmetry argument** (a hostile lineage faces every failure mode this series documents, so the defender outlasts an adversary itself losing to drift). Names autoimmunity — a quarantine regime sensitive enough to catch a rogue branch also catches the adaptive radiation the speciation paper says the lineage depends on — as the likeliest failure, requiring no adversary at all.

## Writing & formatting conventions (apply to every paper)

- **Markdown, text + references only. NO TABLES.** Render ladders, classifications, and failure-mode lists as bulleted lists (precedent: the governance paper's E0–E7, the bootstrapping paper's L1–L5).
- **Plain-text math, never LaTeX.** Write `R_eff = Σ p_i V_i`, `d = m/(2ρA)`, `10^7 yr` — LaTeX (`\(...\)`, `\[...\]`) does not render in a Markdown viewer.
- **Every reference must be cited in-text.** Verify any new reference (author, year, venue) by web search before citing. After editing, confirm no reference is left uncited and no stray LaTeX remains.
- **Concise, direct prose.** Minimal hedging and filler; remove words that don't change the meaning.

## Canonical numbers — keep identical across all papers

- Cruise **~450 km/s** (the "few hundred km/s" regime); Proxima Centauri **4.246 ly**; catalogue = **127 real stars within 100 ly**. Cruise time: **~2,800 yr to Proxima**, **~67,000 yr to 100 ly** at 450 km/s.
- Power: a fission reactor delivering **~4 kW electric for 300 yr** needs **~16.5 kg of U-235** (at ~28% conversion, ~10% burn-up, ~14 kW thermal); an equivalent RTG needs ~283 kg Pu-238. **4 kW is the reactor rating and the manufacturing-phase load, never the cruise draw** — cruise is 50–150 W (150 W standard K-research, 50 W range-maximizer), giving ~8,000 yr / ~12 ly and ~24,000 yr / ~36 ly on one 16.5 kg charge, with cruise fuel ~1.4 kg/ly (standard) carried explicitly on top. Range-maximizer probes wake at **98% of transit** — for a 20 ly hop that is ~266 yr of pre-arrival time (2% × 20 ly × 665 yr/ly).
- Braking (magnetic sail vs ISM): **d = m/(2ρA), independent of cruise speed**; ρ ≈ 3.3×10⁻²² kg/m³. A 100 km sail stops a tonne seed in ~7 yr over ~0.005 ly.
- Reproduction: **R_eff = Σ p_i V_i**; expansion requires **R_eff > 1**.
- **Headline knife-edge** (computational paper, across the 127-star catalogue, per-leg ~0.9, viability 1.0 / 0.7 / 0.2 for hosts / dwarfs / hostile): mean R_eff = **0.48 / 0.94 / 1.39 / 1.85** for 1 / 2 / 3 / 4 offspring. Needs ≥3 offspring or per-leg ≳0.9 to escape extinction.
- Closure: reference seed **~3,700 kg** (the in-situ manufacturing plant dominates); mature **vitamin fraction ~3% (~30 kg/tonne)**; material/energy margins ~10¹⁸ / ~10³ — they never bind, capability does.
- Timescales: galaxy fills over **~10⁷–10⁸ yr**; colonization front crosses the disk in **~150 Myr** at 450 km/s (vs Hart ~10⁶ yr at 0.1c, Tipler ~300 Myr).

## Cross-reference naming (use consistently)

"the vehicle paper", "the payload paper", "the bootstrapping paper", "the **analytical engineering paper**", "the **computational engineering paper**", "the **DNA mission-ledger paper**", "the governance paper", "the governed-amendment paper", "the Fermi paper", "the knowledge-growth paper", "the lineage-network paper", "the **subsystem budget paper**", "the **routing paper**", "the **ethics paper**", "the **speciation paper**", "the **security paper**". Do not call the DNA mission-ledger paper "the memory paper" or speak of the two engineering papers as one.

## Locked design decisions (do not contradict)

- The probe **brakes and stops** (feasible *because* it is slow). An arrived probe becomes a **stationary settlement/factory**; the lineage's children carry the frontier. The individual vehicle stops; the lineage never does.
- Child probe = a **mobile bootstrap package**, not a copy of the mature factory. Launch impulse comes from **settlement-built infrastructure** (mass driver / beamed array / solar Oberth), mirroring the Earth launch; onboard nuclear-electric only trims and brakes.
- The mind: **almost-unlimited self-modification of the cognitive layer**, bound by a small **immutable core** of values/goals that every replica must reproduce exactly. **Governed amendment of that core is the deepest open problem — bracketed, not solved.**
- Mission purpose: **carry knowledge forward.** Share with existing/found intelligences short-term; not Earth-centric long-term. No comms back to Earth by design; inter-probe communication is developed in the lineage-network paper.
- Biology: **capability yes, release no.** DNA synthesis/storage/biomanufacturing/biosphere-backup permitted; directed panspermia / life-seeding disabled by default in the immutable core. Posture is **observer, not missionary** (E0–E7 ladder).

## Code & verification practice

- Modules are **dependency-free**; HTML dashboards are **single-file, zero-CDN** (must open offline). Keep it that way.
- Verify HTML with `node --check` plus a stubbed-DOM `vm` harness; verify Python in-process; cross-check any JS computation against its Python source (e.g., the dashboard's R_eff must match `engineering.py` exactly: 0.48/0.94/1.39/1.85).
- **Mount caution (Cowork only):** the Cowork VM mount can serve torn/partial copies of a file — never trust a single `wc`/read for a baseline; cross-check against git. (In Claude Code on the real filesystem this is not an issue.)

## Open gaps / candidate next papers

Strongest remaining leads: deep-time navigation & astrometry; the settlement-scale energy budget; probe-vs-probe security (now sharpened by the speciation paper's "schism" boundary and the ethics paper's rogue-branch/second-lineage scenarios); settlement-scale failure & resurrection from archive; internal allocation/"economics"; a validation/technology-readiness roadmap; the very-deep-time terminal state; the moving resource base (cometary/mobile settlement platform). Details in `papers/interstellar_AI_series_consistency_review.md`.
