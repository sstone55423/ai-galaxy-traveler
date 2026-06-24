# AI Galaxy Traveler — Project Guide

Standing context for working in this repo. Read this first.

## What this project is

A realistic simulation and an accompanying nine-paper academic series on a **slow, self-replicating interstellar AI probe** launched from Earth that travels, brakes, settles, repairs itself, reproduces, and carries knowledge forward across deep time.

**The overriding rule, stated everywhere and never to be broken: realistic physical constraints, not science fiction.** Models are first-order and meant to fix orders of magnitude and design direction, not to be engineering specs. When the honest answer is "this barely helps," "this is the hard part," or "this can't yet be known," say so.

Author byline on all papers: **S. Stone, Metropolitan State University.**

## Repository structure

- `papers/` — the academic papers (Markdown). The nine active papers plus the consistency review, two superseded drafts (bootstrap proposal, DNA-storage outline), and `revision_plan.md`.
- `code/` — zero-dependency Python: simulation modules (`galaxy_sim.py`, `propulsion.py`, `energy.py`, `flyby.py`, `wanderer.py`, `engineering.py`) and generators (`build_catalog.py`, `make_map.py`, `make_wanderer.py`, `make_starfields.py`, `make_engineering_dashboard.py`).
- `site/` — zero-dependency Canvas HTML dashboards (`star_map_3d.html`, `energy_dashboard.html`, `wanderer_map.html`, `engineering_dashboard.html`) + data (`stars_100ly.csv/.json`).

## The nine-paper series (body / mind / hands + supporting + synthesis)

1. **Vehicle** — `papers/interstellar_AI_probe_paper.md` — "Growth, Not Speed" (rev 3). The body: propulsion, power, braking, replication. *Foundational paper; the reader's entry point.*
2. **Payload** — `papers/interstellar_AI_payload_paper.md` — "The Payload" (rev 2). The mind: cognition, memory, mission, the immutable core / interpretive layer / mutable cognitive layer.
3. **Bootstrapping** — `papers/interstellar_AI_bootstrap_paper.md` — "From Seed to Factory". The hands: industrial closure, the L1–L5 closure ladder, the vitamin set.
4. **Analytical engineering** — `papers/interstellar_AI_engineering_paper.md` — "Engineering Closure". First-order four-budget model.
5. **Computational engineering** — `papers/interstellar_AI_computational_paper.md` — "Engineering Closure, Computed". Code-backed results; owns the headline R_eff knife-edge.
6. **DNA mission-ledger** — `papers/interstellar_AI_dna_ledger_paper.md` — "DNA Mission Ledgers". Memory substrate + integrity ledger.
7. **Governance** — `papers/interstellar_AI_governance_paper.md` — "Contact, Contamination, and Noninterference". The E0–E7 contact ladder.
8. **Governed amendment** — `papers/interstellar_AI_amendment_paper.md` — "Amending the Unamendable". The deepest open problem.
9. **Fermi** — `papers/interstellar_AI_fermi_paper.md` — "Slow Fire, Silent Galaxy". Synthesis: the R_eff × D × G reframing.

## Writing & formatting conventions (apply to every paper)

- **Markdown, text + references only. NO TABLES.** Render ladders, classifications, and failure-mode lists as bulleted lists (precedent: the governance paper's E0–E7, the bootstrapping paper's L1–L5).
- **Plain-text math, never LaTeX.** Write `R_eff = Σ p_i V_i`, `d = m/(2ρA)`, `10^7 yr` — LaTeX (`\(...\)`, `\[...\]`) does not render in a Markdown viewer.
- **Every reference must be cited in-text.** Verify any new reference (author, year, venue) by web search before citing. After editing, confirm no reference is left uncited and no stray LaTeX remains.
- **Concise, direct prose.** Minimal hedging and filler; remove words that don't change the meaning.

## Canonical numbers — keep identical across all papers

- Cruise **~450 km/s** (the "few hundred km/s" regime); Proxima Centauri **4.246 ly**; catalogue = **127 real stars within 100 ly**.
- Power: a fission reactor delivering **~4 kW electric for 300 yr** needs **~16.5 kg of U-235** (at ~28% conversion, ~14 kW thermal); an equivalent RTG needs ~283 kg Pu-238.
- Braking (magnetic sail vs ISM): **d = m/(2ρA), independent of cruise speed**; ρ ≈ 3.3×10⁻²² kg/m³. A 100 km sail stops a tonne seed in ~7 yr over ~0.005 ly.
- Reproduction: **R_eff = Σ p_i V_i**; expansion requires **R_eff > 1**.
- **Headline knife-edge** (computational paper, across the 127-star catalogue, per-leg ~0.9, viability 1.0 / 0.7 / 0.2 for hosts / dwarfs / hostile): mean R_eff = **0.48 / 0.94 / 1.39 / 1.85** for 1 / 2 / 3 / 4 offspring. Needs ≥3 offspring or per-leg ≳0.9 to escape extinction.
- Closure: reference seed **~3,700 kg** (the in-situ manufacturing plant dominates); mature **vitamin fraction ~3% (~30 kg/tonne)**; material/energy margins ~10¹⁸ / ~10³ — they never bind, capability does.
- Timescales: galaxy fills over **~10⁷–10⁸ yr**; colonization front crosses the disk in **~150 Myr** at 450 km/s (vs Hart ~10⁶ yr at 0.1c, Tipler ~300 Myr).

## Cross-reference naming (use consistently)

"the vehicle paper", "the payload paper", "the bootstrapping paper", "the **analytical engineering paper**", "the **computational engineering paper**", "the **DNA mission-ledger paper**", "the governance paper", "the governed-amendment paper", "the Fermi paper". Do not call the DNA mission-ledger paper "the memory paper" or speak of the two engineering papers as one.

## Locked design decisions (do not contradict)

- The probe **brakes and stops** (feasible *because* it is slow). An arrived probe becomes a **stationary settlement/factory**; the lineage's children carry the frontier. The individual vehicle stops; the lineage never does.
- Child probe = a **mobile bootstrap package**, not a copy of the mature factory. Launch impulse comes from **settlement-built infrastructure** (mass driver / beamed array / solar Oberth), mirroring the Earth launch; onboard nuclear-electric only trims and brakes.
- The mind: **almost-unlimited self-modification of the cognitive layer**, bound by a small **immutable core** of values/goals that every replica must reproduce exactly. **Governed amendment of that core is the deepest open problem — bracketed, not solved.**
- Mission purpose: **carry knowledge forward.** Share with existing/found intelligences short-term; not Earth-centric long-term. No comms back to Earth and none between probes by design (a lineage-network paper is anticipated but unwritten).
- Biology: **capability yes, release no.** DNA synthesis/storage/biomanufacturing/biosphere-backup permitted; directed panspermia / life-seeding disabled by default in the immutable core. Posture is **observer, not missionary** (E0–E7 ladder).

## Code & verification practice

- Modules are **dependency-free**; HTML dashboards are **single-file, zero-CDN** (must open offline). Keep it that way.
- Verify HTML with `node --check` plus a stubbed-DOM `vm` harness; verify Python in-process; cross-check any JS computation against its Python source (e.g., the dashboard's R_eff must match `engineering.py` exactly: 0.48/0.94/1.39/1.85).
- **Mount caution (Cowork only):** the Cowork VM mount can serve torn/partial copies of a file — never trust a single `wc`/read for a baseline; cross-check against git. (In Claude Code on the real filesystem this is not an issue.)

## Open gaps / candidate next papers

Strongest leads first: a **knowledge-growth metric** (the series' figure of merit "growth, not speed" still has no yardstick); the **lineage network / information-sharing** paper (anticipated in the vehicle paper, leaned on by the Fermi synthesis). Then: deep-time navigation & astrometry; the full subsystem mass/power/thermal budget; probe-vs-probe security; settlement-scale failure & resurrection from archive; internal allocation/"economics"; a validation/technology-readiness roadmap; the ethics of creating the lineage; the very-deep-time terminal state; lineage divergence/speciation. Details in `papers/interstellar_AI_series_consistency_review.md`.
