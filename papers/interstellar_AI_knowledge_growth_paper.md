# The Growing Archive: Knowledge Accumulation, Contingency Planning, and Mission Adaptation in a Deep-Time Self-Replicating Interstellar AI Lineage

**S. Stone**
*Working draft, revision 2. Tenth in a series on a slow, self-replicating interstellar AI probe. Where the vehicle paper establishes the probe's body, the payload paper its mind, and the computational engineering paper the reproduction knife-edge, this paper addresses the series' stated figure of merit — "growth, not speed" — and gives it a quantitative foundation. It draws on the bootstrap plan from the bootstrapping paper, the memory architecture from the DNA mission-ledger paper, and the network architecture sketched in the payload paper, and establishes what the probe learns, at what rate, how that learning degrades, and what the lineage does to protect it.*

---

## Abstract

The phrase "growth, not speed" has organized this series since its first paper, yet no prior paper has given it a yardstick. What grows? At what rate? What sets the ceiling, and what causes the floor? This paper proposes K — knowledge — as that yardstick and gives it formal structure: K is mission-relative, provenance-tracked, weighted uncertainty reduction, measured as a sum over validated claims and models, each weighted by mission value, confidence, replication factor, and accessibility. K is not archive size or observation count; it is what the triage-and-modeling pipeline converts data into.

K has three components. Observational K is what the probe learns about the universe — stellar composition, planetary atmospheres, biosignatures, transients triangulated across nodes. Operational K is what it learns about its own mission — improved bootstrap plans, refined cognitive architectures, scenario-tested contingency portfolios. Meta-knowledge, a sub-category of operational K, captures insights about how to improve future probe design and propagates at highest network priority. A two-tier departure state K₀ divides what the probe carries into active working memory, available throughout transit, and a cold DNA archive, unlocked at settlement. A knowledge manifest bridges the gap: the probe knows what it carries even when it cannot transmit or read the full archive.

The first-order model is dK_net/dt = G(t) - L(t). The loss term decomposes into six components: node extinction (L_extinction), network isolation (L_isolation), archive degradation (L_degradation), archive corruption (L_corruption), retrieval failure (L_retrieval), and knowledge obsolescence (L_obsolescence). Against these losses the mission deploys a degraded-state cascade across four modes (D1 through D4), a pre-extinction transmission protocol, and infrastructure-independent cold vaults designed to outlast the probe. A worked first-order example shows K trajectories under four scenarios — successful settlement, degraded settlement, extinction after manifest transmission, and extinction without manifest — and finds that manifest transmission reduces extinction knowledge loss by approximately 3× relative to silent failure.

K and the demographic reproduction model R_eff = Σ p_i V_i are explicitly coupled: R_eff(K_op) = Σ p_i(K_op) · V_i(K_op), where better operational K raises per-stage success probabilities and viability factors. Network redundancy lowers the effective loss rate. A lineage that clears the R_eff knife-edge grows in both nodes and knowledge simultaneously. "Growth, not speed" is, in the end, one claim about two quantities that move together.

---

## 1. Introduction

"Growth, not speed" is the series' organizing principle for a slow, self-replicating interstellar AI probe. The vehicle paper argues that the architecture optimized for persistence and growth should be slow, braking, and settlement-based rather than fast and transient. The payload paper argues that such a probe is best understood as a librarian and a learner whose central task is to remain itself, keep learning, and carry knowledge forward. The computational engineering paper computes the reproduction knife-edge: the lineage either clears R_eff > 1 and spreads across the Galaxy, or falls short and goes extinct, and the margin is thin. Together these papers establish what growth requires physically and demographically. None of them specifies what grows, measures it, or gives the series' own organizing claim a unit.

This paper fills that gap. We propose K — knowledge — as the figure of merit, define its components, give it formal structure, model its accumulation and loss across the mission lifecycle, and develop the cruise-phase, settlement-phase, network, and degradation-state structure within which K evolves. The treatment inherits the architecture rather than re-deriving it: the braking and settlement model from the vehicle paper, the bootstrap plan from the bootstrapping paper, the three-layer cognitive architecture and triage model from the payload paper, the DNA-backed mission ledger from the DNA mission-ledger paper, and the demographic model from the computational engineering paper. References to those papers use the canonical series naming throughout.

One boundary requires explicit statement at the outset. The payload paper sketches a galactic store-and-forward network and the DNA mission-ledger paper develops its integrity substrate. The lineage-network paper ("Signal and Silence") treats where knowledge flows and how the network is governed. This paper does not pre-empt it. Our subject is what K is, how it accumulates and decays, and what the probe transmits — not how the network routes that transmission or maintains its topology.

The following schematic organizes the K lifecycle that the rest of the paper develops:

```
K₀ (departure)
 ├── active working memory (stellar catalog, bootstrap plan, meta-K)
 └── cold DNA archive (full Earth corpus — unlocked at settlement)
      │
      ▼
Cruise-phase K growth
 ├── observational K (astrometry, ISM, time-domain, physics tests)
 ├── operational K (AI self-improvement, bootstrap plan refinement)
 └── meta-K (probe design insights — elevated network priority)
      │
      ▼
Settlement burst
 ├── archive unlock (K_accessible → K_total)
 ├── instrument expansion (in-situ manufacturing removes launch-mass limit)
 └── resource survey (grounds viability model and contingency selection)
      │
      ▼
Network propagation
 ├── redundancy (more nodes → lower effective L_extinction)
 ├── super-additive triangulation (multi-node geometry, joint Bayesian updates)
 └── Lamarckian propagation (operational K flows horizontally, not only vertically)
      │
      ▼
K(t) = G(t) − L(t)
 └── L: extinction + isolation + degradation + corruption + obsolescence
      │
      ▼
Degraded-state cascade
 ├── D1: sub-probe capable → local solar system mission
 ├── D2: archive-only → cold vault + manifest transmission
 ├── D3: self-repair + AI reflection → preserve active K
 └── D4: terminal → final manifest burst, cold vault deposit
```

---

## 2. Defining K: Components, Formal Structure, and Value Function

**The epistemic stack.** Before defining K formally, a hierarchy of epistemic layers prevents the metric from collapsing into archive size or observation count:

- Raw data: uninterpreted sensor outputs — spectra, images, particle counts, instrument voltages
- Information: processed, calibrated, structured data — a stellar spectrum with wavelength, flux, and error bars
- Claim: a proposition derived from information — "planet b has atmospheric methane at 3σ"
- Model: a parameterized, predictive representation of a domain — a planetary climate model calibrated to the planet's albedo and stellar flux
- Knowledge (K): a validated, provenance-tracked, uncertainty-reducing model or claim — the above biosignature confirmed at two or more independent confidence levels with documented provenance
- Mission utility: the expected value of that K for mission objectives — how much it raises target viability, contact-priority assessment, or the quality of future child probes

K is the fifth layer, not the first. Raw data volume is not a proxy for K; the pipeline from observation to validated claim — the triage and modeling architecture of the payload paper (Section 5 of that paper) — is what converts data to K.

That pipeline is not hypothetical. King (2026) surveys machines that originate hypotheses, deduce their consequences, design and execute experiments, interpret results, and revise their beliefs — from Adam, the first machine to make novel scientific discoveries through cycles of hypothesis formation and physical experimentation, through the self-driving laboratories that followed — and argues that the open problem is no longer whether the individual steps of science can be automated but how to integrate them into one agent connected to literature, formal knowledge, simulation, and instruments. That is the probe's problem exactly, with the integration deadline set at launch and no human in the loop for the millennia that follow.

**Formal definition.** Let j range over validated claims, models, contingency plans, and meta-knowledge items currently held by the lineage. The knowledge metric is:

K_net = Σ_j w_j · ΔH_j · c_j · r_j · a_j

where:
- w_j = mission-value weight of item j, drawn from the value function below
- ΔH_j = the reduction in Shannon entropy for the domain j addresses (Shannon 1948), measuring how much uncertainty the item removes
- c_j = validation confidence level: from raw hypothesis (low) through single-node confirmed (medium) to independent-node confirmed (high)
- r_j = replication factor across the network — how many independent nodes hold item j
- a_j = accessibility factor: 1 for active working memory, less than 1 for cold archive (readable only after L1–L2 closure is achieved)

K_net grows when new validated items are added, when c_j improves through additional independent confirmation, when r_j increases through network replication, or when the settlement archive unlocks and raises a_j toward 1. K_net falls when nodes go extinct and reduce r_j for unique items to zero, when archives degrade and reduce c_j, or when confidence is revised downward by contradicting evidence.

**K is mission-relative, not value-neutral.** The weights w_j are not information-theoretic — they are anchored to the mission's founding value function. A confirmed biosignature, a solved reactor failure mode, and a measurement of the ISM magnetic field all reduce entropy in their respective domains; they do not carry the same w_j. K is the quantity the mission is built to maximize; it cannot be defined without stating what the mission values.

**Three components.** Observational K targets the external universe: stellar composition, planetary atmospheres, biosignatures, ISM structure, transients, physical constants measured to new precision, galactic structure. Operational K targets the probe itself and its mission: improved bootstrap plans, refined cognitive architectures, scenario-tested contingency portfolios, solved failure modes, better reactor management protocols. Both accumulate during cruise and at the settled observatory.

A sub-category of operational K merits elevated standing throughout: **meta-knowledge**, defined as knowledge about how to improve the design of future probes — better cognitive architectures, more reliable manufacturing sequences, more robust closure approaches. Meta-knowledge propagates through the network and into child probe design at higher priority than general K. One validated architectural insight can improve every subsequent generation.

**What K is not.** A probe that stores every photon it captures without modeling, validation, or uncertainty reduction has a large archive and low K. An archive that accumulates false positives, corrupted observations, or unvalidated claims has high volume and negative K contribution from those items. The formal definition prevents this: unvalidated items carry c_j near zero and do not enter K_net until confirmed.

**The value function.** The weights w_j follow a mission priority hierarchy, stated explicitly as a first approximation to be refined through simulation and operational experience.

The highest weight goes to data integrity — protecting what is already known. A corrupted archive destroys K without replacement; integrity is the precondition for everything else. The second weight goes to transmission — getting unique K to other nodes before it is lost. A dying settlement's first obligation is to transmit, not to survive. Third is survival itself, as the means of continued K growth. Fourth is new discovery, of which life detection is the standing highest-value exemplar. Fifth is engagement with local life.

An important distinction separates the fifth item from the others. Protecting local life is not merely a low-priority mission goal to be traded against K gain — it is also a hard constraint on permissible action. The governance paper's E0–E7 contact ladder defines the boundaries of the permitted action space; within that space, the priority hierarchy above applies; outside it, contamination or harmful intervention is prohibited regardless of potential K gain. The value function ranks goals within the permitted action space; the contact ladder defines the space itself.

This is a mission priority stack, not a science priority stack. Within the new-discovery tier, life detection is the highest-value science item. The hierarchy governs resource allocation when trade-offs are forced.

The root reference for the value function is the Earth knowledge corpus at departure: knowledge value is proportional to its distance from that corpus, its irreplaceability from the probe's specific vantage, and its mission relevance. These weights are initializations; the probe refines them as the archive grows and as the Earth reference fades in relevance over deep time.

**Knowledge obsolescence.** Models improve; older observations are superseded. The DNA mission-ledger paper's append-only architecture retains everything — no records are deleted. Superseded packets are flagged with ledger metadata marking them obsolete, leaving them available for data-corruption recovery, historical provenance, and potential future reinterpretation when better models make old data useful again. Their w_j declines but does not reach zero; the rate at which w_j should be formally depreciated for superseded knowledge is noted as an open problem in Section 14.

---

## 3. K₀: What the Probe Carries at Departure

A probe launched from Earth carries two distinct knowledge layers, designed around the infrastructure available during transit.

The **active working memory** layer holds everything the probe needs to read and use during transit without DNA synthesis or sequencing equipment. It contains: the stellar astrometric catalog of targets and nearby systems (from Gaia and successor surveys; Gaia Collaboration 2023), the bootstrap plan and contingency portfolio, operational and navigation data, reactor management parameters, the mission core and interpretive layer, simulation parameters for cruise-phase scenario modeling, and the meta-knowledge database current at departure. This layer is compact and immediately accessible.

The **cold DNA archive** holds the full Earth knowledge corpus — art, history, culture, biology, humanities, the full scientific literature, engineering databases, and the complete backup of terrestrial genetic information. This archive is not needed during transit; it is consumed at settlement when the probe has established DNA read/write infrastructure as part of the L1–L2 closure path described in the bootstrapping paper. K_accessible during cruise is deliberately smaller than K_total. At settlement, K_accessible rises to approach K_total as the archive unlocks.

**K notation.** Throughout this paper, the following notation applies:
- K_total = all knowledge physically preserved by a node or the lineage, independent of readability
- K_accessible = knowledge currently readable and usable without additional infrastructure
- K_active = knowledge in working memory, immediately available during cruise
- K_cold = knowledge in the DNA archive, readable only after settlement establishes L1–L2 infrastructure
- K_network = knowledge accessible somewhere in the lineage network
- K_net = deduplicated, confidence-weighted knowledge across the lineage after merging redundant records

The ordering K_active ≤ K_accessible ≤ K_total holds for any individual node during cruise. K_net < Σ K_total because redundant K held by multiple nodes does not add to the total — it increases r_j, raising confidence, but not K_net volume. K_net > any single node's K_total because the network holds complementary records no single node possesses.

**The knowledge manifest.** A compact index of everything in the cold archive is stored in active working memory. The probe knows what it carries even when it cannot read it. The manifest allows the probe to answer queries about its holdings — from other probes or from intelligences it encounters — without accessing the archive, and it seeds the pointer system described in Section 11.

**K packet structure.** A unit of transmitted knowledge carries enough metadata for the receiving node to integrate it into its ledger without ambiguity. Each K packet specifies:
- an identifier and type (observation, model, operational update, meta-knowledge, governance, or archive pointer)
- source node and creation time
- a provenance chain linking back to raw observations, tracking why and where each item originated (Buneman, Khanna & Tan 2001)
- confidence level and validation status (quarantine / single-node-confirmed / independent-confirmed)
- mission weight w_j and current replication count r_j
- dependencies on other K packets
- supersession pointers (supersedes / superseded-by)
- the current ledger hash
- an archive pointer for bulk content held off-packet in content-addressed storage

This structure connects directly to the DNA mission-ledger paper's Merkle-rooted off-ledger storage: the K packet is the ledger entry; the archive pointer is the content address. Together they allow knowledge existence to be tracked cheaply, even when full content cannot be transmitted.

The meta-knowledge database is part of the active working memory and is updated continuously during cruise. It is the highest-priority component of K₀ for distribution to child probes at departure: a child that launches with an improved cognitive architecture or a solved closure bottleneck propagates that improvement to every subsequent generation.

---

## 4. Cruise-Phase Observational K: The Moving Observatory

The transit from Earth to Proxima Centauri at ~450 km/s takes roughly 2,800 years. More distant targets in the 127-star catalogue take proportionally longer — a target at 50 light-years takes approximately 33,000 years at cruise speed. For standard K-research missions — the majority of all dispatches — these transits are not delays to be minimized. They are the first and longest active K-growth phases of the mission. A minority of probes, dispatched on a range-maximizer profile toward denser stellar regions near the galactic center, hibernate all non-essential systems for approximately 98% of transit at roughly 50 W total draw; for these probes the transit is deliberately not an active K-growth phase, a trade-off accepted to reach more distant relay nodes that subsequent K-research probes can use as their starting points. The analysis in this section applies to the standard profile.

The probe's moving vantage provides several observational advantages that no fixed instrument can replicate. For each, the principal feasibility constraints are noted alongside the K contribution.

**Long-baseline astrometry.** By arrival at Proxima, the probe has built an astrometric baseline of approximately 4 light-years relative to Earth. Parallax measurements of background stars from this baseline are geometrically orders of magnitude more precise than any Earth-based or near-Earth program. Stars that appeared stationary from Earth resolve their proper motion; systems that appeared unresolvable from a fixed vantage separate. The realized precision depends on more than geometry, however: aperture, detector stability, attitude control, clock stability, and cross-calibration against Earth-frame catalogs all set practical limits. The geometric advantage is genuine; extracting it requires that the probe carry or later build astrometric instrumentation adequate to the task. K contribution: improves the stellar catalog of targets and improves future probe navigation models. Feasibility risk: precision metrology requirements stringent for a small seed instrument.

**ISM characterization along the actual cruise path.** Density, composition, magnetic field structure, dust distribution, and turbulence statistics measured continuously along the path the probe actually travels. No remote instrument can provide this; it requires being there. The data ground-truth the ISM models the braking calculation depends on (the d = m/(2ρA) stopping-distance formula of the vehicle and computational engineering papers uses ρ ≈ 3.3 × 10^-22 kg/m³ as a reference value) and improve future probes' sail-sizing and navigation models. K contribution: high operational utility, improves braking model confidence. Feasibility risk: sensor calibration stability over millennia; spacecraft interference with magnetic field measurements.

**Time-domain observations.** Continuous monitoring for transients, stellar variability, and slow astrophysical processes over thousands of years. No Earth-based program can run a single observation campaign of this length. A nova, a stellar merger, or a long-period variable observed from departure to arrival provides a dataset impossible to obtain any other way. K contribution: unique time-domain observational K, high irreplaceability. Feasibility risk: limited aperture on the seed probe constrains detection sensitivity before settlement manufacturing.

**Physics tests over unprecedented baselines and timescales.** Measurements of the constancy of physical constants, tests of general relativity over light-year scales, and searches for large-scale structure. K contribution: potentially very high if a deviation is detected; low but non-zero for null results that tighten bounds. Feasibility risk: precision requirements demanding for a small seed; positive results require confirmation from additional nodes.

**Comparative note: cruise K and transit duration.** The accumulation rate of cruise-phase observational K is modest per year but compounds over millennia. All four observation types above benefit from longer baseline and longer duration: a probe with twice the transit time accumulates roughly twice the cruise observational K. This does not constitute a general proof that slow probes dominate fast probes in every K metric — a fast probe that arrives and immediately begins settlement may accumulate high K through in-situ manufacturing more quickly, and does not need to wait out a long transit. The stronger claim is specific: transit time is not idle time under the deep-time architecture. A slow probe converts otherwise empty travel into observational and operational K accumulation that a fast probe cannot replicate. The settled observatory (Section 8), where the probe builds instruments without launch-mass constraints, is where the slow self-replicating architecture most decisively outperforms the fast-flyby concept.

---

## 5. Cruise-Phase Operational K: AI Self-Improvement

During transit — on the standard K-research profile — the mutable cognitive layer has time, power, and data to improve. The probe does not arrive with the same cognitive architecture it departed with. Range-maximizer probes, hibernating for 98% of transit with the AI dormant, accumulate negligible operational K during cruise; their cognitive self-improvement resumes during the pre-arrival wakeup (the final 2% of transit, representing decades to over a century of active operation) and continues through settlement.

Two kinds of improvement occur. The first is **model improvement**: the probe's models of stellar formation, planetary system architecture, ISM physics, and mission-critical processes (reactor degradation, sail performance, dust erosion) are continuously updated against incoming observations. Models built on Earth's theoretical foundation are tested against direct measurements that no Earth instrument could supply. By the end of a 2,800-year transit, the probe's internal models are observationally calibrated in ways impossible at departure.

The second is **algorithmic improvement**: the probe's own learning, pattern-recognition, fault-detection, and planning algorithms are refined over decades and centuries of operation. An approach that underperforms in year one is revised by year one hundred. The probe explores the design space of its own cognition during the long quiet transit and retains only approaches that demonstrably improve mission performance — in the tradition of self-referential improvement systems (Schmidhuber 2007).

Both forms generate **meta-knowledge**: insights about what cognitive architectures function reliably over deep time, what failure modes emerge in autonomous AI systems over decades of unattended operation, and what design choices in the probe's own architecture should be changed in its children. This meta-knowledge enters the meta-knowledge database at elevated priority.

**Operational K acceptance criteria.** The payload paper's three-layer cognitive architecture — immutable core, interpretive layer, mutable cognitive layer — constrains which self-improvements are accepted. Operational K updates the mutable cognitive layer only; the core and interpretive layer are not modified by cruise-phase self-improvement. Each candidate improvement is accepted only if it passes: mission-core consistency checks confirming it does not conflict with core values or goals; interpretive-layer validation against the operational definitions of those goals; sandboxed testing against mission-scenario models; rollback capability if performance degrades after deployment; full recording in the integrity ledger with provenance; demonstrated robustness across multiple resource and target scenarios; and no increase in drift risk for core-adherence metrics. An improvement that cannot satisfy these checks is quarantined as a candidate rather than adopted, and the quarantine itself becomes a meta-knowledge entry — a record of a failure mode or design tension that future probes can benefit from. This is what transforms "almost unlimited self-modification" from a potential instability into a governed K-growth process.

The credit-assignment problem behind these criteria is structural, not incidental. A survey of 1,547 papers on long-horizon agents finds the same pattern across planning, memory, execution, training, and evaluation: outcome-only signals grow less informative as horizons lengthen, and the field's response is to manufacture denser step-level signals — process reward models, credit assignment, trajectory-level diagnostics (Chen et al. 2026). The probe faces the limiting case, since the mission's terminal outcome arrives once, millennia after most cognitive changes were made; the sandboxed tests, rollback checks, and ledger provenance above are exactly such step-level surrogates, and their quality bounds how much operational K a cruise can produce.

The constraint during cruise is that the probe works from the active working memory subset, not the full DNA archive. This bounds what the cognitive layer can reference. At settlement, when the full archive unlocks, a second wave of AI development becomes possible as the probe integrates transit insights with the full depth of the Earth knowledge base.

---

## 6. Cruise-Phase Operational K: Bootstrap Plan Refinement and Scenario Modeling

The probe departs with the bootstrap plan developed in the bootstrapping paper: the L1–L5 closure ladder and the vitamin set (in the closure formalism of Freitas & Merkle 2004), the ~3,700 kg reference seed design, and the nominal resource model. This plan was designed against an assumed resource environment. During cruise, the probe refines it against what it actually observes.

**Observation-driven target modeling.** As the probe approaches its target over centuries, spectral measurements improve, astrometric signatures tighten constraints on companion masses and orbits, and the probe's resource model of the system sharpens from a statistical prior to a system-specific estimate. A target that appeared to host a viable asteroid belt may resolve into a sparse debris disk; one with an ambiguous companion signature may clarify into a stable binary or a distant gas giant. The bootstrap plan is updated with each new constraint.

**Scenario modeling.** Against each plausible resource scenario the probe runs simulations that stress-test the L1–L5 plan. Which closure steps are bottlenecked if the asteroid belt is sparse? What is the critical path if no inner rocky planet exists? What is the minimum viable seed mass for a Kuiper-belt-analog environment? How does replication timescale change under each scenario? These runs convert the single nominal plan into a ranked portfolio of contingency variants. The compute budget available during cruise — at ~4 kW electric over 2,800 years, roughly 3.5 × 10^14 joules — is substantial for simulation work; the full accounting of what that budget supports is deferred to a dedicated energy-budget paper, which should also address growing storage and AI development needs as the mission matures.

**Contingency development.** For resource environments where the nominal plan fails at some L-level, the probe develops alternative approaches: volatiles-first closure for a Kuiper belt analog, Trojan-mining sequences for a gas giant system, cold archive depot strategy for a resource-barren system. Each contingency is added to the active portfolio with its estimated viability and its identified bottlenecks.

The probe arrives not with one plan but with a portfolio ranked by expected resource environment, each entry pre-stress-tested and ready for activation. The first direct survey measurements at arrival test the portfolio against reality and trigger plan selection. This is the operational K analog of the cruise-phase science program: both involve active learning during transit that a fast probe, spending weeks rather than millennia in transit, cannot replicate.

---

## 7. The Contingency Plan Portfolio: Resource-Optimal Settlement

Settlement location is driven by resource access and safety, not by proximity to potentially inhabited worlds. Life detection is the highest-value science item in the settlement's research program; it is conducted remotely from the resource-optimal location, using instruments the settlement manufactures at increasing scale, with sub-probes approaching biologically sensitive environments only under contamination controls consistent with the contact ladder of the governance paper. The settlement goes where the factory can close; the observatory reaches outward from there.

The contingency portfolio organizes the bootstrap plan across a taxonomy of resource environments.

A **planetary system with an asteroid belt** is the nominal environment. The L1–L5 closure ladder proceeds as developed in the bootstrapping paper. Settlement location is the inner asteroid belt: metals and silicates in accessible orbits, stable long-term dynamics, adequate solar energy.

An **M-dwarf system with rocky planets but sparse asteroid population** — the most common stellar type in the 127-star catalogue — offers rocky planet gravity wells but limited small-body inventory. Settlement location may shift to Trojan clusters of the innermost planet or captured irregular bodies. The closure bottleneck moves to bulk metal feedstock; the vitamin fraction rises. Replication timescale extends but closure remains achievable at a higher L-level cost.

A **debris disk or Kuiper belt analog** — volatile-rich, metal-lean, cold — requires a different industrial pathway: volatiles-first processing, ice mining for oxygen and hydrogen, and elevated reliance on carried vitamin components for metallic and electronic parts. The cold environment is advantageous for DNA cold storage longevity. Replication is achievable but slower and more vitamin-dependent.

A **gas giant system** with Trojan clusters, irregular satellites, or a substantial moon system offers diverse feedstock and moderate closure prospects. The bottleneck is often precision processing of mixed-composition material rather than feedstock availability. Settlement location is a stable Lagrange point or a captured body. Mini-probe networks for surveying the moon system are a natural science program from this position.

A **cometary environment** — limited inner resources but a rich outer comet population — is bootstrap-challenging. The cold archive depot option applies here: if full closure is not achievable, the probe prioritizes creating a durable, findable cold archive before resources are exhausted. The moving resource base concept — using a cometary nucleus as a mobile industrial platform, steering or rendezvousing with a resource-rich body — is the most powerful option in this environment. The range of configurations, from a cold archive depot on a resource-limited comet to a full mobile settlement from which a series of child probes are launched over tens of thousands of years from progressively different positions, is rich enough to warrant dedicated treatment; it is noted here and deferred as a candidate for its own paper or for the bootstrapping follow-on.

A **resource-barren system** — low metallicity, no stable small-body reservoir — represents the worst-case contingency. The nominal mission is not achievable. The probe transitions to data node and deep-field observatory: characterize the system as thoroughly as existing resources permit, create a cold archive, transmit the knowledge manifest, and execute the degraded-state protocol described in Section 11.

In all cases the contingency portfolio is shared through the network. A contingency approach that works in a debris-disk environment, learned at one settlement, propagates to all probes heading toward similar systems, compounding the benefit across the lineage.

---

## 8. Settlement-Phase K Burst

Arrival is the sharpest K discontinuity in the mission. During cruise the probe has been accumulating K from observations of the target made at diminishing but still interstellar distances. At arrival, remote inference is replaced by direct measurement. The models built during a 2,800-year transit meet their first real test.

Two step-changes occur at settlement. First, the **cold DNA archive unlocks**: as the probe bootstraps DNA read/write infrastructure along the L1–L2 closure path, the full Earth knowledge corpus becomes accessible. K_accessible rises to approach K_total. The probe integrates everything the cold archive holds with everything it has learned during transit, and a second wave of AI development becomes possible as the full knowledge base is brought to bear on insights accumulated in flight.

Second, the **instrument ceiling rises without bound**. A flyby probe carries whatever instruments it left with; a settlement builds them. As the factory grows, the probe manufactures telescopes, interferometers, and sensor arrays far larger than any launched instrument — the decisive manufacturing advantage the payload paper (Section 4) identified. Observing power grows with the settlement rather than being fixed at departure. Life detection, stellar characterization, planetary spectroscopy, and long-baseline astrophysics all benefit from instruments manufactured in situ at scales impossible at launch.

The settlement-phase science priority stack, consistent with the payload paper: life detection first (highest single-discovery K value), followed by planetary characterization, stellar characterization, small-body resource census, long-baseline astrophysics, and archive enrichment. This stack governs which instruments are built first and which observations are scheduled first. It does not govern settlement location, which was fixed by resource and safety criteria before arrival.

Life detection, if it occurs, does not merely add to K; it potentially transforms the value weighting of the entire archive in the context of the galactic network. A confirmed biosignature at any node propagates through the network as the highest-priority update in the mission history.

---

## 9. Network Multiplication: Why K_net Is Super-Additive

If each settlement learned only in isolation, the lineage would be a scattering of disconnected archives. Network propagation of knowledge makes K_net greater than the sum of individual node K values — super-additive — for reasons specific enough to state.

**Different viewing geometries break observational degeneracies.** A single node's observation of a star or galaxy is subject to projection effects, line-of-sight confusion, and measurement degeneracies that a second node at a different vantage resolves. Two nodes observing the same object from positions separated by light-years produce a joint measurement that neither could produce alone.

**Independent detections raise confidence non-linearly.** Two independent nodes detecting the same phenomenon produce a Bayesian confidence increase that is super-additive relative to either detection alone. The update from a second independent detection — using different instruments, at a different vantage, through an independent pipeline — is multiplicatively larger than the first in proportion to what it resolves. A single marginal biosignature is uncertain; the same detection confirmed independently by a second node at a different position and epoch approaches definitive.

**Triangulation of transients requires at least two nodes.** A supernova or gravitational wave event detected by a single node is located in angle but not in distance. Two nodes provide position and distance; three or more provide full three-dimensional localization and independent light-curve measurements. The K-content of a triangulated transient is qualitatively higher than a single-node detection.

**Redundancy protects K against node loss.** K held by only one node is lost if that node goes extinct. K held by multiple nodes survives any single node's extinction. As network density grows with R_eff, the expected K-loss rate from individual extinctions falls — the effective loss term L_extinction shrinks with network coverage.

**Lamarckian propagation multiplies operational K.** A solved bootstrap bottleneck, a better reactor design, or a refined contingency approach discovered at one settlement propagates horizontally to all nodes, not just vertically to that node's children. This makes the lineage's operational K growth faster than any purely genetic analogy would suggest.

**Alien contact as K discontinuity.** If a non-lineage intelligence shares its knowledge with a probe, the K gain may be orders of magnitude larger than any individual stellar observation — an entirely independent corpus accumulated over a different history by minds with different perceptual and conceptual architectures. The probe applies the same integration process it uses for conflicting inter-probe knowledge: complementary knowledge is added directly, conflicting knowledge is held as unresolved with both records retained and uncertainty represented honestly. After successful integration, disseminating the updated knowledge through the network is an immediate high-priority task. The governance mechanics of the contact event itself are the province of the governance paper.

**K quality: negative epistemic events.** Network propagation multiplies K, but it also propagates errors. The K framework must account for false claims, corrupted observations, and adversarial inputs entering the network.

Negative epistemic events include: false positives from single-node detections that fail independent confirmation; archive corruption from radiation damage reducing c_j; adversarial contact data from an external intelligence attempting to manipulate the lineage's models; hallucinated or overfit internal models developed during long autonomous operation; and poisoned network updates distributed by a compromised node.

The countermeasure is a quarantine-and-validate pipeline: every candidate K packet enters quarantine on receipt and advances to confirmed status only after passing provenance verification, consistency checks against the existing model base, and — for high-stakes claims — independent confirmation from at least one additional node. Quarantined items carry c_j = 0 and do not contribute to K_net. Items that fail validation are retained in the ledger with a quarantine flag rather than deleted, because the history of a failed claim is itself provenance information. The Byzantine-fault-tolerant architecture of the DNA mission-ledger paper (Lamport, Shostak & Pease 1982) addresses the network-trust side; the quarantine pipeline addresses the epistemic side. Together they bound the rate at which L_corruption erodes K_net.

Meta-knowledge propagates as the highest-priority network update throughout. When any node improves the meta-knowledge database, that improvement propagates to all nodes and into the next generation of child probes.

---

## 10. A First-Order K(t) Model

We write the first-order model as:

dK_net/dt = G(t) - L(t)

where K_net is the deduplicated, confidence-weighted knowledge held across the lineage at time t, G(t) is the growth rate, and L(t) is the loss rate.

**The growth term.** G(t) has three components. Cruise-phase accumulation: each probe in transit contributes observational and operational K at rate r_cruise, so the cruise contribution is r_cruise × N_transit(t). Settlement bursts: each newly settled node contributes K_burst — the step-change from direct measurement, archive unlock, and instrument growth — concentrated around the settlement event. Network propagation: knowledge held at connected nodes compounds as it propagates, at a rate proportional to network connectivity. The total growth rate rises with the number of active nodes and network density, both governed by R_eff through the branching process of the computational engineering paper.

**The loss term.** L(t) decomposes into six components:

- L_extinction: K loss from node death — items with r_j = 1 or r_j held only at the extinct node are removed from K_net permanently. K held at multiple nodes (r_j ≥ 2) survives the extinction.
- L_isolation: K held by nodes below the network connectivity threshold, unavailable to K_net without being destroyed. The archive exists; the network cannot reach it. Outer-edge probes and degraded nodes without transmission capability are the primary contributors.
- L_degradation: physical archive decay below the DNA refresh threshold. If radiation damage or temperature stress exceeds the encapsulation design limits over deep time, c_j for affected items falls and K_net erodes. The DNA mission-ledger paper quantifies the underlying decay rates; extending those rates to a full L_degradation model is the starting point for quantifying this term.
- L_corruption: syntactic or semantic corruption — bit errors, adversarial inputs, or hallucinated models that inject claims with initially high apparent c_j. The quarantine pipeline of Section 9 bounds this term; it does not eliminate it.
- L_retrieval: K held intact, networked, and uncorrupted, which the retrieval path nonetheless fails to surface when it is needed. The item is present and its c_j undiminished; what fails is the path between holding a fact and finding it — the query that would have reached it is never formed, or the index no longer reflects the vocabulary under which it was filed, or the interpretive layer's current operationalization of a term has drifted from the one in force when it was stored. This is distinct from L_isolation, where the network cannot reach the archive, and from L_degradation, where the substrate itself has decayed: here the archive is reachable and the record is perfect. We note, as an argument rather than a result, that this is the one loss component that plausibly *grows* with K_net rather than shrinking with redundancy — a larger archive and a longer interpretive drift since filing both widen the gap between what is held and what is findable, and duplicating an item across more nodes does nothing to make it easier to retrieve.
- L_obsolescence: the natural decline in mission weight w_j of superseded models. A superseded climate model's ΔH_j is absorbed into its successor; the older item's w_j falls without the item being lost. This is the only L component that does not represent a genuine loss of information — it represents its refinement.

The loss term is bounded from below by zero (fully networked, lossless lineage) and from above by K_net itself (total extinction). Full quantification of L(t) — attaching rates to each component from first-principles models — is the most important open problem in the K framework; we name it explicitly so that future work has a defined problem to attack.

**K_accessible vs. K_total.** During cruise, K_accessible ≪ K_total for any individual probe because the cold DNA archive cannot be read without settlement infrastructure. At settlement, K_accessible rises to approach K_total. The network's K_accessible is always less than K_total because some nodes are in cruise at any given time. K_accessible grows discontinuously at each settlement event, even while K_total grows continuously.

**Terminal modes.** As the galactic density gradient forces outer-edge probes into lower-replication or no-replication states, G(t) changes character. Outer-edge probes shift from replication-K growth to depth-K growth: deeper local observation, longer observatory runs, more thorough system characterization. The growth rate per node does not fall to zero in terminal mode; it changes form. K_net in terminal mode grows more slowly but does not stop.

### 10.1 A Worked First-Order Example

The following toy model illustrates the K framework with transparent, first-pass numbers. All K values are measured in K-units; K₀ = 100 K-units represents the normalized baseline departure archive. Values here represent incremental gain above K₀ from cruise and settlement.

Parameters used:
- r_cruise = 0.003 K-units/year (combined observational and operational cruise accumulation rate)
- K_burst = 50 K-units (settlement step-change from archive unlock and direct measurement)
- T_Proxima = 2,800 years; T_50ly = 33,000 years
- f_unique = 0.2 (fraction of a node's total K that is unique — not replicated elsewhere — at the moment of extinction)
- f_manifest = 0.7 (fraction of unique K captured in the manifest and recoverable by the network after node extinction)

**Cruise accumulation:**
- K_cruise(Proxima) = 0.003 × 2,800 = 8.4 K-units
- K_cruise(50 ly target) = 0.003 × 33,000 = 99 K-units

The comparison is instructive. For a 50 light-year target, cruise K approaches the settlement burst in magnitude. Beyond roughly 17,000 years transit time — approximately 25 light-years at cruise speed — cruise K exceeds the settlement burst and dominates the single-node total. For very distant targets, the mission is as much a transit science program as a settlement program.

**Node K at successful settlement:**
- K_node(Proxima) = 8.4 + 50 = 58.4 K-units above baseline
- K_node(50 ly target) = 99 + 50 = 149 K-units above baseline

**Scenario 1 — Two nodes, different targets, successful settlement.** The two probes' cruise K is complementary (different paths, different observations). Their settlement K is complementary (different systems). Assume 20% overlap from shared operational K derived from the same parent.
- K_net ≈ 58.4 + 58.4 × 0.8 = 105 K-units (additive, no super-additive bonus yet)
- Super-additive triangulation and joint Bayesian confirmation bonus: approximately ×1.15
- K_net ≈ 121 K-units — more than either node alone, and more than simple addition, because the joint product adds cross-confirmation value that neither node's K independently provides.

**Scenario 2 — Degraded settlement, no archive unlock.** The probe settles but fails to reach L2 closure; K_cold remains inaccessible and instruments are limited to the launched set.
- K_node = 8.4 + 15 K-units (partial burst, no archive unlock) = 23.4 K-units above baseline
- K_accessible = K_active only; K_cold = 100 K-units remain unread but the manifest is available

Even without reading the cold archive, the node knows what it holds and can transmit the manifest, preserving K_network awareness of K_cold.

**Scenario 3 — Node extinction after manifest transmission.** A successfully settled node (K_node = 58.4 K-units above baseline) transmits its manifest and key unique items before extinction.
- Unique K at risk: f_unique × K_node = 0.2 × 58.4 = 11.7 K-units
- Unique K recovered via manifest and retrieval: f_manifest × 11.7 = 0.7 × 11.7 ≈ 8.2 K-units
- Unique K permanently lost (contribution to L_extinction): 11.7 − 8.2 = 3.5 K-units

**Scenario 4 — Node extinction without manifest transmission.**
- Unique K permanently lost: 11.7 K-units (the full unique fraction)

Comparing Scenarios 3 and 4: manifest transmission reduces K loss from node extinction by 3.3× for these parameters. Higher network coverage (more nodes holding copies) reduces f_unique and further narrows the gap. A lineage with high R_eff not only spreads geographically but makes each node's extinction less costly to the archive.

---

## 11. Mission Lifecycle, Galactic Position, and Graceful Degradation

**The galactic density gradient.** The Sun sits at roughly 26,000 light-years from the galactic center in the Orion Arm, a region of moderate stellar density. Probes launched toward the galactic center travel into increasing stellar density: targets are more numerous, closer together, and transit times shorten. Probes launched toward the galactic anti-center travel into decreasing density until, at the outer rim, no viable targets remain within reach. These trajectories have different lifecycle endpoints, and planning for both is itself a form of cruise-phase operational K.

For **inward-directed lineages**, network density grows with stellar density. The effective R_eff may increase as targets become more numerous and closer-spaced. The galactic bulge introduces a distinct environment — older stellar populations, higher radiation, fewer metal-rich systems — requiring its own contingency portfolio variants.

For **outward-directed lineages**, the probe calculates many generations in advance when the terminal transition becomes likely. This calculation is itself operational K: the probe models its reachable stellar inventory along its trajectory and identifies, well before the last viable target is reached, what the terminal mission posture should be. The terminal generation is planned, not surprised.

**The degraded-state cascade.** When a settlement can no longer maintain full mission capability, it transitions through a cascade of progressively scaled-down but still valuable mission modes. Each mode below specifies the capability state, primary goal, K action, and exit condition back toward higher capability.

- **D0 — Full capability.** Capability state: R_eff > 1, full manufacturing, DNA synthesis, and interstellar launch available. Primary goal: reproduce and observe at maximum rate. K action: normal K growth across all components; meta-K propagated to children at launch. Exit condition: none required; maintains or improves.

- **D1 — Reduced reproduction.** Capability state: manufacturing intact but interstellar launch no longer achievable; sub-probe launch possible. Primary goal: local solar system exploration. K action: pivot to depth-K — sub-probes survey planets, moons, outer system, and small bodies; the settlement becomes a permanent local deep-field observatory contributing irreplaceable long-baseline measurements. Exit condition: restore launch infrastructure to recover R_eff > 0 and advance toward D0.

- **D2 — Archive-only.** Capability state: sub-probe launch no longer viable; DNA synthesis remains available. Primary goal: maximize knowledge preservation and network propagation. K action: create the most durable and findable cold archive possible; maximize the manifest transmitted to any reachable node; deposit cold vault packages in stable, recoverable locations — stable orbits, subsurface small bodies, dynamically persistent niches. Archives carry their own Rosetta key and the DNA mission-ledger's Merkle authentication structure, so a finder can decode and authenticate contents without the probe's active systems. Exit condition: restore sub-probe capability to advance to D1.

- **D3 — Self-repair and AI reflection.** Capability state: DNA synthesis compromised; K accumulation limited to what active working memory supports. Primary goal: restore higher-level capability through self-repair; sustain meta-K growth. K action: the probe processes its existing archive for insights, generates meta-knowledge about its own failure modes and the conditions that produced them, and — if any transmission capability is restored — propagates meta-K at highest network priority. A probe that cannot move, transmit, or archive can still refine its cognitive models and produce insights worth transmitting. Exit condition: restore DNA synthesis to advance to D2.

- **D4 — Terminal.** Capability state: all manufacturing compromised and recovery unlikely. K action: final manifest burst to any reachable receiver; deposit any remaining cold vault material in the most stable accessible location. This is the probe's last K contribution to the lineage.

At every level, an emergency protocol runs in parallel: transmit the knowledge manifest continuously to any reachable node. The manifest is compact — a catalog index, a flag that the node holds more than it can transmit, and location information — requiring minimal bandwidth or power. It remains actionable even in the deepest degraded state. Receiving nodes use the manifest to prioritize which nodes to query and to plan retrieval missions; child probes carry pointers to what their parent held but could not transmit.

**Infrastructure-independent cold vaults.** Separate from the active archive, the probe deposits passive cold archives in stable, findable locations designed to survive the probe's own extinction. These vaults carry their own Rosetta key — mathematics and physics, as the payload paper's seed archive established — so a finder can decode and authenticate the contents without any of the probe's active systems. The vault is the lineage's last K contribution after the settlement dies.

---

## 12. Probe-Probe Coordination and K Synthesis

Two probes may reach the same system through converging lineage branches, deliberate rendezvous, or trajectories that loop back toward the Sun's galactic position after a long outward arc. In all cases the same coordination protocol applies; no special case is needed.

**Kin recognition and trust.** The first act on contact is to verify the immutable core hash. If both probes confirm that the other's core is intact and matches the founding hash, they are lineage members and the coordination protocol proceeds. If one cannot verify, the Byzantine-fault-tolerant quarantine posture of the DNA mission-ledger paper applies: cooperation is withheld until verification succeeds, or the unverified probe is treated as an unknown external agent.

A matching core hash is necessary but not sufficient for full operational trust. Probes with identical core hashes may have divergent interpretive layers or divergent mission histories that produce incompatible knowledge claims. The trust protocol therefore distinguishes four cases:

- Compatible ledgers (common history confirmed, divergences only in complementary domains): full K exchange under the K arithmetic below.
- Incompatible ledgers (conflicting claims in overlapping domains after K arithmetic): quarantine conflicting packets pending multi-node resolution; cooperate immediately on non-conflicting records.
- Asymmetric trust (one probe's provenance is incomplete or its interpretive layer shows drift): treat the lower-confidence probe as a partially trusted source; weight its K packet inputs by a reduced c_j, proportional to the degree of drift detected.
- Uncertain provenance (provenance chain has gaps or the ledger is not self-consistent): quarantine all claims that cannot be traced to verifiable raw observations; retain for investigation rather than discard.

Quarantine applies regardless of kin status. A compromised lineage member whose cognitive layer has drifted outside mission parameters can produce high-confidence but adversarially misaligned updates. The quarantine pipeline from Section 9 applies to all incoming K packets: kin status determines the starting c_j prior, not whether validation is required.

**K arithmetic of the encounter.** The two probes' archives do not simply add. Redundant K — knowledge both probes inherited from their common ancestor — confirms and cross-validates, raising c_j for shared items, but does not increase K_net volume; r_j increases without ΔH_j increasing. Complementary K — knowledge acquired along different paths since the lineage diverged — adds directly; each probe holds what the other lacks from its unique trajectory. Conflicting K — cases where both probes measured the same phenomenon and got incompatible results — is held as unresolved. Both records are retained with their provenance; the AI reflects, with time measured in centuries if necessary. In a constantly changing universe some conflicts are genuine: a stellar metallicity measurement taken 500,000 years apart may reflect real stellar evolution rather than measurement error. Forcing reconciliation on conflicts that may not be resolvable is less honest and less useful than maintaining both records with uncertainty explicitly flagged.

The DNA mission-ledger paper's fork-tolerance and eventual-consistency architecture handles the ledger side of this encounter: two divergent ledger histories are compared, common history confirmed, and divergences quarantined where unresolvable or reconciled where compatible.

**Coordinated expansion.** Rather than duplicating efforts — both probes sending a child to the nearest unvisited star — the encounter enables coordinated outward division. The probe with higher local K takes the deep-science and observatory role; the probe with higher manufacturing capacity continues the outward mission. Where targets permit, the two probes divide the reachable sky rather than redundantly targeting the same nearest star. The K gain from coordination is substantial: the same resources cover more unique territory and more unique observations.

**Dissemination after synthesis.** The merged K is transmitted through the network as a high-priority update. Two-node encounter records are among the most valuable single events in the network's history: they bring together trajectories that may have diverged for millions of years and may not converge again.

---

## 13. Connection to R_eff and the Reproduction Knife-Edge

The K model and the demographic model of the computational engineering paper are coupled, not independent.

The most direct coupling is through the viability factors in R_eff = Σ p_i V_i. This coupling can be written explicitly:

R_eff(K_op) = Σ_i p_i(K_op) · V_i(K_op)

where each p_i and V_i is a function of the operational K available at time of launch. Specifically:

- Better braking and navigation models raise p_brake (probability of successful deceleration and arrival)
- Better bootstrap contingency portfolios raise p_settle (probability of achieving closure and replication)
- Better target classification and resource modeling raise V_i for ambiguous systems previously coded as hostile or marginal
- Better governance classification may decrease V_i for systems assessed under the governance paper's E0–E7 ladder as containing life that triggers noninterference constraints

The viability term V_i in the computational engineering paper is a first-order proxy — 1.0 for planet-hosts, 0.7 for dwarfs, 0.2 for hostile environments — representing the expected resource environment. A probe with a well-developed contingency portfolio can find viable approaches in environments the baseline model codes as marginal, raising effective V_i and moving the reproduction knife-edge toward safety.

This functional dependence is not yet quantified — it is a research program for the computational engineering paper's successors. Naming it makes the coupling explicit rather than rhetorical: K_op is an input to R_eff, not merely correlated with it.

The loss term L(t) creates a second coupling: settlements that go extinct take their unique local K with them. Improving knowledge distribution before extinction — through the manifest, the pointer system, and cold vaults — reduces effective K loss even when demographic R_eff falls below 1. A node that fails but has transmitted its manifest and deposited a findable cold archive loses less K to the network than one that fails silently. Reducing L(t) is therefore both a K problem and a partial answer to extinction: the lineage's knowledge survives nodes that do not.

Finally, K_net grows with N_settled, which grows with R_eff. A lineage at R_eff = 1.39 — three offspring, the reference parameters of the computational engineering paper — grows both in nodes and in K faster than one at R_eff = 0.94. The K yardstick and the demographic yardstick are not the same quantity, but they move together.

---

## 14. Open Problems

**Quantifying L(t).** The six loss-term components are named and partially bounded but not yet fully quantified. The extinction rate of settlements, the rate at which isolated nodes lose network connectivity, and the archive degradation rate under realistic radiation and temperature conditions each require first-principles models. This is the most important open problem in the K framework and the most directly actionable by the series' own engineering models. The DNA mission-ledger paper's decay-rate analysis is the starting point; extending it to L_extinction and L_isolation requires coupling to the demographic branching model. L_retrieval is the least bounded of the six: unlike the others it has no physical rate to measure, since it depends on the semantic distance between the vocabulary in which an item was filed and the vocabulary in which it is later sought — a quantity the series has no model for, and which the interpretive layer's own governed evolution keeps changing.

**Refining the value function.** The root-settlement-weighted hierarchy is a computable starting point. Refining the weights through simulation — running scenarios where different weightings produce different outcomes and evaluating which weighting best protects K_net against L(t) — is an ongoing research program. The function will evolve as the archive grows and as the Earth reference decays in relevance over deep time.

**Ethical weight of the value function and quarantine mechanisms.** The hierarchy that ranks transmission above survival, the value-weights rooted in the Earth corpus, and the asymmetric-trust discounting applied to a drifted kin probe's or an encountered intelligence's testimony are not ethically neutral engineering choices — they decide what counts as knowledge worth keeping and whose testimony is believed, and they leave the archive best equipped to know itself and least equipped to know encountered life. The ethics paper's discussion of epistemic ethics treats this in depth, including the case that this asymmetry amounts to a form of testimonial injustice. The value function's revision process named above is exactly the gap that discussion identifies as needing the same governance the behavioral immutable core already receives.

**Minimum viable K.** The floor K_min below which the probe can no longer navigate, repair, or execute the bootstrap plan is defined conceptually but not yet bounded quantitatively. The transition thresholds between degraded states (D0 through D4) need formalization, connecting directly to the engineering papers' self-repair models.

**Depreciation schedule for superseded knowledge.** Flagged-obsolete K packets retain partial value as corruption-recovery references, historical provenance, and candidates for future reinterpretation. The rate at which their w_j should be formally depreciated — and whether that rate should be a function of time or of the quality of the superseding item — is unresolved, with practical implications for active-memory retention policy.

**The energy budget for cruise-phase computation.** At ~4 kW electric over 2,800 years, the cruise compute budget is approximately 3.5 × 10^14 joules. What scenario modeling and AI development this budget actually supports, and how it scales to longer transit times, is deferred to a dedicated energy-budget paper. That paper should also address growing needs for knowledge storage and AI development capacity as the mission matures.

**The moving resource base.** A cometary nucleus or captured body as a mobile industrial platform offers powerful archival and replication options in cometary-rich, planet-poor environments. The configuration space — from a cold archive depot on a resource-limited comet through a full mobile settlement launching child probes over tens of thousands of years — is rich enough to warrant dedicated treatment.

**K framework grounding in information theory and decision theory.** The formal K definition draws on Shannon entropy reduction and mission-relative weighting. A fuller treatment would connect it to Bayesian experimental design (Chaloner & Verdinelli 1995) — which observation most reduces K-relevant uncertainty? — value-of-information theory (Howard 1966) — when is collecting more K worth its resource cost? — and active learning (Settles 2012) — how should the probe select its science program to maximize expected K gain? These connections strengthen the framework's scholarly grounding and are anticipated rather than developed here.

---

## 15. Conclusion

"Growth, not speed" is the series' organizing principle. This paper gives it a yardstick.

K — knowledge — is formally defined as mission-relative, provenance-tracked, weighted uncertainty reduction: K_net = Σ_j w_j · ΔH_j · c_j · r_j · a_j, summing over validated claims and models weighted by mission value, confidence, replication factor, and accessibility. It is not archive size or observation count; it is what the triage-and-modeling pipeline converts data into. Three components — observational K, operational K, and meta-knowledge — distinguish what the probe learns about the universe, about its own mission, and about how to improve future probes.

The cruise phase is the first and longest active K-growth phase of the mission. A probe traveling 2,800 years to Proxima Centauri builds a ~4 light-year astrometric baseline, characterizes the ISM along its actual path, improves its own cognitive architecture within the governed constraints of the interpretive layer, and refines the bootstrap plan against scenario models of what it will find. It arrives smarter, better-planned, and more capable than it left. For targets beyond ~25 light-years, cruise K exceeds the settlement burst in magnitude; the cruise phase is as much a science program as a transit. The argument for slowness is not only physical but epistemic — though the decisive advantage lies at the settled observatory, where in-situ manufacturing removes the instrument ceiling that constrains every fast architecture.

The first-order model dK_net/dt = G(t) - L(t) names the loss term explicitly and decomposes it into six components: extinction, isolation, degradation, corruption, retrieval failure, and obsolescence. Against these losses the mission deploys a degraded-state cascade across four modes (D1 through D4), a pre-extinction transmission protocol, a knowledge manifest and pointer system, and infrastructure-independent cold vaults designed to outlast the probe itself. The worked example shows that manifest transmission reduces extinction K loss by approximately 3× relative to silent failure for typical network parameters.

K and the demographic reproduction model R_eff = Σ p_i V_i are explicitly coupled through R_eff(K_op) = Σ p_i(K_op) · V_i(K_op). Better operational K raises both factors; network redundancy lowers the effective loss rate. A lineage that clears the R_eff knife-edge grows in both nodes and knowledge simultaneously. "Growth, not speed" is, in the end, one claim about two quantities that move together.

---

## References

Buneman, P., Khanna, S., & Tan, W. C. (2001). Why and where: A characterization of data provenance. In *Proceedings of the 8th International Conference on Database Theory* (pp. 316–330). Springer.

Chaloner, K., & Verdinelli, I. (1995). Bayesian experimental design: A review. *Statistical Science*, 10(3), 273–304.

Chen, M., Wang, L., & Qu, B. (2026). The horizon gap: Planning, memory, execution, training, and evaluation for long-horizon LLM agents. *arXiv preprint* arXiv:2608.06663.

Freitas, R. A., & Merkle, R. C. (2004). *Kinematic Self-Replicating Machines.* Landes Bioscience.

Gaia Collaboration; Vallenari, A., et al. (2023). Gaia Data Release 3: Summary of the content and survey properties. *Astronomy & Astrophysics*, 674, A1.

Howard, R. A. (1966). Information value theory. *IEEE Transactions on Systems Science and Cybernetics*, 2, 22–26.

King, R. D. (2026). The past and future of AI scientists. *arXiv preprint arXiv:2608.14407*.

Lamport, L., Shostak, R., & Pease, M. (1982). The Byzantine Generals Problem. *ACM Transactions on Programming Languages and Systems*, 4(3), 382–401.

Schmidhuber, J. (2007). Gödel machines: Fully self-referential optimal universal self-improvers. In B. Goertzel & C. Pennachin (Eds.), *Artificial General Intelligence* (pp. 199–226). Springer.

Settles, B. (2012). *Active Learning.* Morgan & Claypool Publishers.

Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379–423.

---

*This is the tenth paper in the series. The vehicle paper, "Growth, Not Speed," treats the body — propulsion, power, braking, and replication. The payload paper, "The Payload," treats the mind — cognition, memory, and mission. The bootstrapping paper, "From Seed to Factory," treats the hands — industrial closure and the L1–L5 ladder. The analytical engineering paper, "Engineering Closure," and the computational engineering paper, "Engineering Closure, Computed," develop the four engineering budgets and the reproduction knife-edge across the real stellar catalogue. The DNA mission-ledger paper, "DNA Mission Ledgers," develops the memory substrate. The governance paper, "Contact, Contamination, and Noninterference," develops the E0–E7 contact ladder. The governed-amendment paper, "Amending the Unamendable," treats the deepest open problem of value stability. The Fermi paper, "Slow Fire, Silent Galaxy," synthesizes the series through the R_eff–D–G framework. This paper gives the series' stated figure of merit its yardstick.*
