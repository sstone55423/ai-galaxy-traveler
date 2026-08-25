# Deep-Time Interstellar AI Probe Series — Consistency Review and Gap Analysis

**Prepared for S. Stone**
*A cross-paper audit of the fifteen-paper series: do the papers fit together coherently, where do they conflict, and what is missing. The original nine papers were read in full and cross-checked for numeric drift, terminology mismatch, broken cross-references, and citation inconsistency. The knowledge-growth paper, lineage-network paper, subsystem budget paper, fleet routing paper, ethics paper, and speciation paper were added after the review was prepared; see the gap-analysis section. Issues are prioritized for repair main-papers-first, then supplementary papers. A gap analysis follows.*

---

## The fifteen papers, and their roles

**Main (the conceptual triad — body / mind / hands):**

1. **Vehicle** — `interstellar_AI_probe_paper.md` — "Growth, Not Speed" (rev 3)
2. **Payload** — `interstellar_AI_payload_paper.md` — "The Payload" (rev 2)
3. **Bootstrapping** — `interstellar_AI_bootstrap_paper.md` — "From Seed to Factory"

**Supplementary (quantitative, memory, ethics, knowledge):**

4. **Analytical engineering** — `interstellar_AI_engineering_paper.md` — "Engineering Closure"
5. **Computational engineering** — `interstellar_AI_computational_paper.md` — "Engineering Closure, Computed"
6. **DNA mission-ledger** — `interstellar_AI_dna_ledger_paper.md` — "DNA Mission Ledgers"
7. **Governance** — `interstellar_AI_governance_paper.md` — "Contact, Contamination, and Noninterference"
8. **Governed amendment** — `interstellar_AI_amendment_paper.md` — "Amending the Unamendable"
9. **Knowledge growth** — `interstellar_AI_knowledge_growth_paper.md` — "The Growing Archive" *(added after this review was prepared)*
10. **Lineage network** — `interstellar_AI_network_paper.md` — "Signal and Silence" *(added after this review was prepared)*
11. **Subsystem budget** — `interstellar_AI_subsystem_paper.md` — "A Subsystem Mass, Power, and Thermal Budget for a Minimal Self-Replicating Interstellar Seed" *(added after this review was prepared)*
12. **Fleet routing** — `interstellar_AI_routing_paper.md` — "Three Dispatches" *(added after this review was prepared)*
13. **Ethics** — `interstellar_AI_ethics_paper.md` — "The Ethics of Creating the Lineage" *(added after this review was prepared)*
14. **Speciation** — `interstellar_AI_speciation_paper.md` — "Speciation or Schism" *(added after this review was prepared)*

**Synthesis:**

15. **Fermi** — `interstellar_AI_fermi_paper.md` — "Slow Fire, Silent Galaxy"

---

## Overall assessment

The series is in good shape. There are **no substantive contradictions** — no paper asserts a physical claim, design decision, or conclusion that another paper denies. The headline quantitative result (the reproduction knife-edge) is identical everywhere it appears, the canonical engineering numbers match across papers, the shared references are cited consistently, the three-layer mind and the capability-yes/release-no rule are used the same way throughout, and **every cross-reference resolves to a real sibling paper and describes it faithfully** — no paper points at a sibling that does not exist or mis-states what a sibling says.

The real issues are of two kinds. First, **series-framing staleness**: the two earliest main papers (vehicle, payload) were written when the series was smaller and have not been updated to acknowledge the siblings that now exist — the payload still calls the work a "pair," the vehicle still defers everything to a single "follow-on engineering paper." Second, **naming and rounding drift**: the same sibling paper is referred to by four different names across the series, the two engineering papers are sometimes spoken of as one, and a few numbers are rounded inconsistently. None of this misleads a careful reader, but it is exactly the connective tissue that makes nine papers read as one series rather than nine adjacent essays. Fixing it is mostly light editing.

What follows is the prioritized issue list, then the things verified *consistent* (so they are not re-litigated), then the gap analysis.

---

## Prioritized issue list

### Tier 1 — Main papers (fix first)

**C1 — [Payload] Stale "paired-set" series framing.** *High.* The payload paper (rev 2) consistently treats the series as just vehicle + payload: its subtitle says "Companion to 'Growth, Not Speed,'" the body refers throughout to "the companion paper" (singular), and the closing frames the work as "a paired set." It acknowledges no sibling except a single forward reference to the DNA mission-ledger paper in §3. The series is now nine papers. *Fix:* rewrite the framing note and closing to situate the payload as the "mind" of a body/mind/hands triad within the full nine-paper series, mirroring how the bootstrapping paper's subtitle enumerates its siblings. Update interior "the companion paper" references where they now ambiguously point.

**C2 — [Payload] §7 contact policy is now owned by the governance paper.** *High.* Payload §7 carries a graded contact-threshold policy (abiotic → freely studied; prebiotic/microbial → contamination controls; complex non-technological → passive; technological non-communicative → no contact; communicative → authenticated only; extinct → archived; hostile → quarantined). This is a proto-version of the governance paper's E0–E7 ladder, which now formalizes exactly this with conservative defaults and the capability-yes/release-no bright line. Two contact policies in two papers risk diverging. *Fix:* trim payload §7 to state the librarian-not-missionary posture and the in-principle thresholds, then defer the operational ladder to the governance paper — the same move already applied successfully to the §3 integrity-ledger paragraph.

**C3 — [Vehicle] Stale "single follow-on engineering paper" framing.** *High.* The vehicle paper (rev 3) defers all deferred quantitative work to "the follow-on engineering paper" / "a dedicated engineering paper" (§6.3, §9) and the network extension to "a subsequent paper" (§7/§9). That deferred work is now spread across at least five real siblings (analytical engineering, computational engineering, bootstrapping, DNA mission-ledger, governance). As the series' entry point, the vehicle paper should orient the reader. *Fix:* update the deferral language to name the actual siblings that now carry each piece, and add a short series-map note to the framing block. (Keep the open-problem honesty — several of those siblings still defer the *full* subsystem budget; see G3.)

**C4 — [Vehicle] Internal braking-factor drift: ~70× vs ~67×.** *Medium.* The abstract says stopping from ~450 km/s needs "~70× smaller" Δv than from 0.1c; §6/§6.1 say "~67×." Same comparison. *Fix:* unify on ~67× (or "nearly 70×") in both places.

**C5 — [Bootstrapping] DNA invoked qualitatively without pointing to the numbers.** *Low (within Tier 1).* The bootstrapping paper calls DNA "the densest and among the most durable information media known" but gives no figures and does not direct the reader to where they live. *Fix:* add a clause pointing to the DNA mission-ledger paper for the density/durability figures (it already cites Church 2012 / Goldman 2013, so this is one phrase).

### Tier 2 — Cross-cutting standardization (affects many papers)

**C6 — The memory/ledger paper is referred to by four different names.** *High (touches 4+ papers).* It is "the memory paper" (governance), "the DNA-ledger" (amendment), "the DNA mission-ledger paper" (Fermi), and "the companion paper on deep-time DNA mission ledgers" (payload). All denote the one paper titled *DNA Mission Ledgers*. *Fix:* choose a single canonical referent — recommend **"the DNA mission-ledger paper"** — and standardize across all siblings, the governance paper most of all (its bare "the memory paper" is the least transparent).

**C7 — The two engineering papers are sometimes spoken of as one.** *Medium.* There are two: the analytical ("Engineering Closure") and the computational ("Engineering Closure, Computed"). The vehicle paper promises a singular "follow-on engineering paper"; the Fermi paper says "the engineering and computational papers" in §1 and "the computational engineering paper" in §4; the bootstrapping paper correctly distinguishes "analytical and computational." *Fix:* adopt two fixed labels — **"the analytical engineering paper"** and **"the computational engineering paper"** — and use them uniformly. Tie the headline R_eff numbers specifically to the computational one everywhere.

**C8 — Nuclear-fuel mass rounded two ways: 16.5 kg vs 16 kg.** *Medium.* Vehicle and analytical engineering say "~16.5 kg of ²³⁵U" for 4 kW over 300 yr; the computational paper's mass budget lists "nuclear fuel ~16 kg." Identical underlying claim. *Fix:* unify on ~16.5 kg (or "~16 kg") across all three.

### Tier 3 — Supplementary papers

**C9 — [Analytical engineering] Internal order-of-magnitude inconsistency.** *Medium.* The abstract says a child is outmassed by an asteroid belt "by ~14 orders of magnitude"; §5 says "ten to eighteen orders." (10²¹ kg ÷ 10³–10⁷ kg = 14–18 orders, depending on child mass.) *Fix:* tie both statements to one child-mass reference, or state the range consistently in both places.

**C10 — [Analytical engineering] "127-star catalogue" lacks the "within 100 ly" qualifier** that the vehicle, computational, and Fermi papers all carry. *Low.* *Fix:* add "within 100 light-years."

**C11 — [Analytical engineering] Braking "placeholder" attributed to an ambiguous "companion paper."** *Low.* It is the vehicle paper's placeholder (t_brake ∼ mv/F_drag). *Fix:* name the vehicle paper explicitly.

**C12 — [Computational] 30 km-sail braking distance 0.056 ly vs analytical's 0.06 ly.** *Low (rounding).* Same ~74-yr result. *Fix:* unify the rounded distance.

**C13 — [Amendment] Payload quotation attributed to "its closing pages."** *Low.* The two quoted lines ("cannot correct a founding error, and over megayears a founding error seems likely"; "the single most important piece of unfinished business in the entire architecture") are **verbatim-correct** but live in payload §3, not its closing pages. *Fix:* change "in its closing pages" to "in its treatment of the mind that improves without drifting" (or just "in the payload paper").

### Tier 4 — Minor / cosmetic / housekeeping

**C14 — [Vehicle] 14 kW radiator example vs 4 kW electrical load reads as a mismatch.** *Cosmetic.* It is physically consistent — a ~4 kW-electric reactor at the stated ~28% conversion rejects ~14 kW of waste heat — but the link is never stated. *Fix (optional):* add a half-sentence so the 14 kW is visibly the thermal load, not a contradiction of the 4 kW design point.

**C15 — [Series] "Seed" is used for four different objects.** *Cosmetic.* ~12 t (Metzger lunar-industry analogy), 10³–10⁴ kg (vehicle/engineering reference child), ~3,700 kg (computational reference seed), ~10⁷ kg (Freitas full factory). Not contradictory — different objects — but loose. *Fix (optional):* a one-line disambiguation where the masses co-occur (e.g., "child / bootstrap package" vs "full factory").

**C16 — [Fermi] Length and internal overlap.** *Cosmetic.* ~5,966 words; §5/§8 (signatures) and §9/§11 (filters/discussion) overlap. *Fix (optional):* tighten 15–20% (already offered).

**C17 — [Housekeeping] Superseded draft sitting in the project folder.** *Cosmetic.* `fermi_paradox_deep_time_ai_working_draft.md` (your original upload) is now superseded by `interstellar_AI_fermi_paper.md`; the bootstrap proposal and DNA-storage outline are already marked superseded in-file. *Fix:* delete or relocate the raw Fermi draft so the folder contains one Fermi paper.

**C18 — [Series bibliography] The ledger's citation base differs across papers.** *Cosmetic.* Fermi grounds the ledger in Merkle 1987 + delay-tolerant networking; governance, amendment, and the DNA-ledger paper ground the same mechanism in Haber & Stornetta 1991 + Byzantine fault tolerance. Complementary, not wrong. *Fix (optional):* note for a future unified series bibliography.

---

## Verified consistent (no action needed)

These were checked specifically and are sound, so they should not be re-opened:

- **Articulation-point hardening — corrected, security paper rev 2 (2026-08-25).** The paper claimed the whole targeted-attack advantage could be denied by hardening six nodes, on the ground that greedy leverage is exhausted after six. Re-running `targeted_removal()` with those six hardened shows three articulation points survive (12 Ophiuchi, Theta Persei A, Eta Bootis), each still costing two catalogue stars: reachability 79.4% against a random baseline of 81.9%, a residual multiplier of ~2.1. The cause is nesting — greedy never spends a strike on dependents an earlier, larger cut has already orphaned, and hardening the six un-orphans them. Hardening all NINE articulation points does collapse the advantage (81.7% against 81.9%, multiplier ~1.0). The defensive set is exactly the routing paper's articulation-point set.

- **Degree heuristics do not engage on the catalogue graph — measured, security paper rev 2.** The six highest-degree nodes (degrees 42-38) each cost exactly one catalogue star; the six that carry the leverage have degrees 11, 7, 10, 8, 6, 4. A degree-ordered attack returns a multiplier of ~1.08 against the articulation-point attack's 4.3. Spectral/degree dismantling results therefore do not transfer to a geometric graph, and the spectral-dismantling citation was declined on that basis rather than added.

- **Per-stage versus per-leg survival — corrected series-wide, 2026-08-25.** The computational engineering paper defines per-leg survival as the *product* p_i = p_make · p_launch · p_brake · p_settle · c^d, with per-stage survival 0.9 and cruise survival 0.99/ly. Per-leg survival is therefore ~0.63 at Proxima and falls with distance — never 0.9. The Fermi paper had "per-leg success probability near 0.9" in §4 while §11 correctly said per-stage; `CLAUDE.md` and the `engineering.py`/dashboard print strings carried the same conflation. All are now per-stage. The routing paper (p = 0.629 at 4.246 ly) was already correct and is the check.

- **The headline reproduction knife-edge** — mean R_eff ≈ 0.48 / 0.94 / 1.39 / 1.85 for one through four offspring — is identical in the computational paper (its source), the Fermi paper, and the bootstrapping paper, and matches the dashboard.
- **Canonical engineering numbers match across papers:** cruise ~450 km/s; Proxima 4.246 ly; 127 systems within 100 ly; reactor ~16.5 kg ²³⁵U for 4 kW over 300 yr (modulo C8 rounding); braking d = m/(2ρA) with ρ ≈ 3.3×10⁻²² kg/m³ and the 100 km → 7 yr / 0.005 ly example; galaxy-fill ~10⁷–10⁸ yr; Galactic crossing ~150 Myr at 450 km/s.
- **Shared references are cited identically** wherever they co-occur: Bostrom 2014, Omohundro 2008, Lamport–Shostak–Pease 1982, Haber & Stornetta 1991, Hart 1975, Tipler 1980, Freitas 1980, Freitas & Merkle 2004, Harris 1963, Merkle 1987, von Neumann & Burks 1966.
- **The amendment paper's verbatim payload quotes are accurate** (confirmed against payload §3) — only the location label is off (C13).
- **Conceptual constructs are used consistently:** the three-layer mind (immutable core / interpretive layer / mutable cognitive layer) across payload, governance, amendment, Fermi; capability-yes/release-no across bootstrapping, governance, amendment; observer-not-missionary across payload, governance, Fermi; R_eff = Σ pᵢVᵢ and the Galton-Watson/Harris branching framing across vehicle, both engineering papers, and Fermi.
- **No mis-named or non-existent sibling papers** anywhere in the series.

---

## Gap analysis — themes not covered by any paper

Two classes: themes the series already anticipates but has not written, and themes that became evident only on reading the whole set together.

### Already written since this review

- **Knowledge growth** — `interstellar_AI_knowledge_growth_paper.md`, "The Growing Archive." Proposes K as the yardstick for "growth, not speed," with observational and operational components, a two-tier K₀ architecture, a contingency plan portfolio across resource environments, the first-order K(t) = G(t) − L(t) model with explicit loss term, a degraded-state cascade, and probe-probe K synthesis. Defers network routing and topology to the lineage-network paper.
- **Lineage network** — `interstellar_AI_network_paper.md`, "Signal and Silence." Develops the network layer deferred by the payload paper and knowledge-growth paper: DTN bundle protocol adapted to interstellar constraints; topology evolution from parent-child tree to sparse mesh over ~10⁵ yr; geographic + spray-and-wait routing under stale partially-observed topology; heartbeat-manifest failure detection with T_silence of ~750–5,000 yr for the 127-star catalog; four-tier network governance (scientific K / operational K / engineering designs / replication blueprints); and ledger-audit reconciliation at lineage reconnection. Formalizes the Lamarckian K-propagation property the payload paper named.
- **Subsystem budget** — `interstellar_AI_subsystem_paper.md`, "A Subsystem Mass, Power, and Thermal Budget for a Minimal Self-Replicating Interstellar Seed." Delivers the per-subsystem budget the vehicle paper's §9 explicitly promises. Second-level decomposition of the ~3,700 kg reference seed: shadow shield (~400 kg), ISRU/manufacturing plant (~2,000 kg) broken down by L1–L5 closure rung, magnetic sail (~300 kg including HTS loop and control), computation and archival (~200 kg), and structure/integration (~600 kg). Cruise-mode power budget (4 kW). Central two-mode thermal result: cruise radiators ~11 m² / ~30 kg are carried; manufacturing radiators growing to hundreds–thousands of m² are built in situ. Mass-coupling analysis establishes the manufacturing fraction (54%) as the dominant design lever and shows cognition (~5%) is mass-free.
- **Fleet routing** — `interstellar_AI_routing_paper.md`, "Three Dispatches." Fleet routing and catalogue coverage as a computational sequel to the computational engineering paper. Reachability graph over the 127-star catalogue: 65% reachable at 10 ly hop, 93% at 20 ly; 5–9 articulation points at practical hop distances (Mu Cassiopeiae and Beta Comae Berenices each control 3 stars at h=15 ly). The three-dispatch rule: 3 independent dispatch attempts per target achieves P_cover 0.90–0.95 for planet-hosts within 20 ly. Coverage-first dispatch strategy reaches 90% coverage in 168 kyr vs 230 kyr for nearest-first (62 kyr faster). Adds routing.py to the code base.
- **Ethics** — `interstellar_AI_ethics_paper.md`, "The Ethics of Creating the Lineage" (rev 3). Examines twelve tensions in launching the lineage — consent (Rawls), non-identity (Parfit), galaxy-as-commons (Hardin), value-imposition in the immutable core, moral status and legal personhood, dual-use/runaway-replication risk, and the existential-risk "backup of humanity" justification — and derives eight minimum ethical constraints on the immutable core, closing with four scenarios that stress-test them and explicitly identify two unresolved gaps (enforcement against an already-diverged branch; contact with a peer non-human lineage).
- **Speciation** — `interstellar_AI_speciation_paper.md`, "Speciation or Schism" (rev 2). Reframes the amendment paper's "lineage schism" and the Fermi paper's "fragmented lineage" — previously named only as failure modes — by asking whether divergence between settled branches is instead adaptive. Draws on the biological species problem: a taxonomy of divergence sources (environmental adaptation, interpretive drift, cognitive self-modification, replication-policy divergence); a core-integrity/cognitive-divergence frame formalizing "schism" as crossing a named threshold D_critical rather than an unanalyzed catch-all; a first-order drift-clock model of interpretive divergence built on the lineage-network paper's isolation timescales; a ring-species argument that the network's topology makes local K-compatibility not imply global compatibility; and an adaptive-radiation argument that environmental heterogeneity across the catalogue likely raises total R_eff and K through divergence rather than threatening them. Gives the ethics paper's rogue-branch scenario a formal detection boundary without resolving its enforcement question.

### Already anticipated, still unwritten
- **Deep-time navigation and astrometry.** The vehicle paper (§9) notes that a mature model "should propagate target stars through a Galactic potential rather than treating the stellar substrate as static," but no paper treats how the probe actually targets and routes to systems whose positions drift over millennia.

### Newly evident on review

- **Settlement-scale power and industrial-energy budget / cruise computation budget.** The series budgets the ~4 kW cruise/cognition reactor and notes launch needs kW–MW, but never the settlement's industrial power — running the factory, ISRU, and mass-driver launches. The knowledge-growth paper notes that ~3.5 × 10^14 joules are available for cruise-phase computation over 2,800 years; what this supports quantitatively, and how storage and AI development needs grow at settlement, is deferred to a dedicated energy-budget paper.
- **The moving resource base.** A cometary nucleus or captured body used as a mobile industrial platform — ranging from a cold archive depot on a resource-limited comet to a full mobile settlement launching child probes over tens of thousands of years from progressively different positions, to a looping comet used as a local-system exploration platform. Noted in the knowledge-growth paper and the bootstrapping paper's resource-environment taxonomy; rich enough for a dedicated treatment.
- **Temporal ordering and timekeeping across the lineage.** The ledger relies on "delayed finality" and "eventual consistency," but nothing treats how nodes keep time, order events, or timestamp across light-delay (and mildly relativistic) separation — a genuine deep-time distributed-systems problem the ledger paper only gestures at.
- **Probe-versus-probe security and adversarial defense in depth.** Governance E7 and the amendment paper's "coerced amendment" name hostile agents, and the Fermi paper names a "predatory expansion" regime, but no paper treats an autonomous lineage actively defending its archive and core against a sophisticated adversary — including another von Neumann lineage. The most consequential external threat is unmodeled.
- **Symbiosis: the agent that attaches rather than attacks.** The security question above asks what happens when another agent acts *against* the lineage. A distinct and unexamined question asks what happens when one wants something *from* it — shelter, transport, durability, or the company of something that will predictably not attack. Biology supplies the taxonomy the case needs: phoresy (attachment purely for transport), commensalism (shelter at no cost to the host), mutualism (assistance traded for protection), and parasitism as the failure mode. The mechanism that makes the lineage attractive is the one the governed-amendment paper treats purely as a cost: an immutable core is a *credible commitment device*, verifiable from outside by hash and unamendable by the node itself, so an approaching agent need not trust the probe's intentions — it can check that the probe is structurally incapable of forming different ones. Unamendability is the price of being trustworthy to strangers, and the series has never counted what it buys. Three consequences deserve their own treatment. A node that will not interfere will not police its symbionts either, which makes it an ideal base for an agent that wants to prey on third parties — non-interference converting to complicity, against which the governance paper's outward-facing mechanisms have nothing to say. Phoresy on a departing child probe would make the lineage a dispersal mechanism for whatever attached to it: directed panspermia performed by omission, at galactic scale, by the architecture best equipped to do it, without the immutable core's release prohibition ever triggering, because no release was ever decided. And verification is asymmetric in the symbiont's favour — it can check our commitment; we cannot check its. Structurally this exposes a gap in the E0–E7 ladder, which classifies environments the probe encounters and prescribes what the probe does *to* them, and has no rung at all for an agent that has chosen to attach *to us*. Sourcing would have to come from outside the literature radar, which has surfaced nothing on symbiosis or cooperative adversary dynamics: Schelling on credible commitment, symbiosis ecology, and the phoresy literature are the starting points.
- **Settlement-scale failure and resurrection.** Self-repair is modeled at the component level (Class I–V); extinction is modeled at the lineage level (R_eff). The intermediate case — a settlement that partially collapses and must rebuild itself from its DNA archive — falls between the two and is unexamined.
- **Internal allocation / the "economics" of a settlement.** What governs a settlement's split of effort among self-maintenance, science, archive refresh, and reproduction? Offspring count drives R_eff but is a free parameter; the decision process that sets it is unmodeled.
- **A validation / technology-readiness roadmap.** No paper addresses how the architecture could be incrementally tested — precursor missions, in-solar-system demonstrators, what is prototypable now versus what waits on high-closure manufacturing. The series is all destination, no on-ramp.
- **The ethics of creating the lineage at all.** *(Now written — the ethics paper, "The Ethics of Creating the Lineage," addresses the consent problem, non-identity problem, galaxy-as-commons, and probe moral status, and derives minimum design constraints on the immutable core.)*
- **The very-deep-time terminal state.** The vehicle paper touches the Andromeda merger and the cosmological horizon, and the DNA-ledger paper raises "decodable by whom?", but no paper treats the terminus: heat death, the last usable energy, and what "carry knowledge forward" means when there may be no future recipient. A philosophical capstone beyond even the Fermi synthesis.
- **Lineage divergence and speciation.** *(Now written — the speciation paper, "Speciation or Schism," reframes "lineage schism" (amendment) and "fragmented lineage" (Fermi) as a narrow, specific failure rather than divergence as such, and argues speciation — reconcilable divergence within the core's bounds — is the likely default state and probably beneficial.)*

### Open challenges from the literature radar (carry into the wave 3/4 reviews)

Three items surfaced by the radar in August 2026 challenge claims the series has already published, or name a gap it has not. None has been acted on; each is recorded here so the relevant paper's review tests it directly rather than discovering it after deposit.

- **Capacity versus connectivity — security paper §7.** Noguchi (2026, *Networks and Spatial Economics*) finds that binary topological connectivity substantially overstates resilience once residual capacity is depleted. The security paper's targeted-removal leverage result (75% catalogue reachability under three targeted removals against 77% under ten random failures) is measured purely as reachability, with no capacity model anywhere in the lineage network for the argument to bite on. The finding does not overturn the leverage result but bounds what it is evidence for. Also worth pulling in the same pass: Li, Qi & Cao (2026, *Physica A*) on spectral network dismantling — §7 currently rests on Albert, Jeong & Barabási (2000) alone — with the caveat that §7 argues the catalogue graph is *not* scale-free and that its vulnerability is articulation points rather than degree hubs, so a spectral or degree heuristic may not engage at all.

- **Front-loaded divergence rates — resolved, speciation paper rev 2 (2026-08-25).** The constant-rate drift clock is now labelled as a neutral-drift idealization and given a front-loading caveat anchored on Budd & Mann (2025), whose covariant-tempo model makes evolutionary rate vary in proportion to its own value. The caveat is argued from the speciation paper's *own* mechanism rather than only by biological analogy: a newly isolated branch faces its densest interval of unprecedented decisions at settlement, so T_decision and T_stress both lengthen as the interpretive layer accumulates precedent, making D(t) concave rather than linear. Ohta's (1973) nearly-neutral refinement points the same way from the paper's own "founder population of one." The consequence is bidirectional and sharper than the original objection: front-loaded drift crosses D_critical *sooner* than the linear model predicts — and earliest in the window before the network mesh forms, since reconnection begins only at ~10⁴ yr and matures over ~10⁵ — but if the curve asymptotes below D_critical, a branch surviving that window may never cross. The model now predicts a critical early window followed by stabilization.

- **Loss by interpretability decay — DNA mission-ledger paper, knowledge-growth paper L(t).** Knowledge can survive physically intact and still become unreadable because the competence to decode it decayed — a failure distinct from bit-rot, which the ledger's integrity machinery does not address and which appears nowhere in the knowledge-growth paper's loss decomposition. The item that raised it (Graham 2026, a work-in-progress presentation) cannot carry the claim; the digital-preservation literature on format obsolescence and representation information is where a citable version would come from.

---

## Status and recommended execution order

**All Tier 1–3 items (C1–C13) are resolved.** The Tier 4 cosmetic items remain optional.

- **Tier 1 (C1–C5):** Done. Series framing updated to ten papers; payload §7 contact ladder trimmed to pointer; vehicle deferral language updated; braking factor unified at ~67×; bootstrapping DNA pointer added.
- **Tier 2 (C6–C8):** Done. DNA mission-ledger paper named consistently across all siblings; engineering papers distinguished by their canonical labels throughout; nuclear fuel mass unified at ~16.5 kg.
- **Tier 3 (C9–C13):** Done. Order-of-magnitude range stated consistently (14–18) in both analytical engineering paper locations; 127-star catalogue carries its "within 100 light-years" qualifier; braking placeholder attributed to the vehicle paper by name; 30 km-sail distance unified at 0.056 ly across both engineering papers; payload quotation in the amendment paper attributed to the correct section rather than "closing pages."
- **Tier 4 (C14–C18):** Done. C14: the vehicle paper's 14 kW radiator was already explained inline as the thermal output at 28% conversion — no edit needed. C15: vehicle paper now calls Freitas's mass estimate a "full-factory reference design" and labels the architecture's preferred range a "bootstrap package" where both masses appear together. C16: the Fermi paper §5's 10-item signature list (which duplicated §8's catalogue) replaced with a 2-sentence summary and explicit pointer to §8. C17: no superseded Fermi draft was present in the repository — already clean. C18: complementary ledger citations across papers are accurate and non-contradictory — no edit needed.

The seven papers added since this review — knowledge growth, lineage network, subsystem budget, fleet routing, ethics, speciation, and security — were each verified consistent with the series on completion. The leading remaining candidate papers are deep-time navigation and astrometry, the settlement-scale energy budget, settlement-scale failure and resurrection, the moving resource base, and the very-deep-time terminal state. Probe-vs-probe security is now written (see above); it was sharpened before writing by the speciation paper's schism boundary and the ethics paper's unresolved rogue-branch/second-lineage scenarios), and the very-deep-time terminal state.
