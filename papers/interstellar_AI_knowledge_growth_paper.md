# The Growing Archive: Knowledge Accumulation, Contingency Planning, and Mission Adaptation in a Deep-Time Self-Replicating Interstellar AI Lineage

**S. Stone**
*Metropolitan State University*
*Working draft — first pass. Tenth in a series on a slow, self-replicating interstellar AI probe. Where the vehicle paper establishes the probe's body, the payload paper its mind, and the computational engineering paper the reproduction knife-edge, this paper addresses the series' stated figure of merit — "growth, not speed" — and gives it a quantitative foundation. It draws on the bootstrap plan from the bootstrapping paper, the memory architecture from the DNA mission-ledger paper, and the network architecture sketched in the payload paper, and establishes what the probe learns, at what rate, how that learning degrades, and what the lineage does to protect it.*

---

## Abstract

The phrase "growth, not speed" appears throughout this series as the organizing principle for a slow, self-replicating interstellar AI probe, yet no prior paper has given it a yardstick. What grows? At what rate? What sets the ceiling, and what causes the floor? This paper proposes K — knowledge — as that yardstick, distinguishes two components (observational K, what the probe learns about the universe; and operational K, the improved plans, algorithms, and contingency portfolios it develops for its own mission), and models their accumulation, dissemination, and loss across the full mission lifecycle.

The central reframing is of the cruise phase. A probe traveling at ~450 km/s to Proxima Centauri takes roughly 2,800 years to arrive. Those 2,800 years are not transit time to be minimized; they are the first and longest active K-growth phase of the mission. The probe operates as a moving observatory, accumulating observational K from a vantage that no Earth-based instrument can replicate, building an astrometric baseline that grows to ~4 light-years relative to Earth by arrival. Simultaneously it refines its own cognitive models, stress-tests the bootstrap plan it carries against scenario models of what it will find, and develops a ranked contingency portfolio tailored to the resource environments it may encounter. It arrives smarter, better-planned, and more capable than it left. Slow probes accumulate more cruise-phase K than fast ones; speed sacrifices this.

We propose a two-tier departure state K₀: active working memory (stellar catalog, bootstrap plan, operational data) available throughout transit without DNA infrastructure, and a cold DNA archive (the full Earth knowledge corpus) unlocked at settlement. Settlement location is driven by resource access and safety, not by proximity to life; life detection is the highest-value science item conducted from the resource-optimal position, not a placement criterion. The contingency plan portfolio organizes the bootstrap plan across a taxonomy of resource environments from nominal planetary systems to cometary fields and resource-barren targets.

Knowledge grows but also decays. We write the first-order model as dK_net/dt = G(t) - L(t), where the growth term spans cruise observations, settlement bursts, and network propagation, and the loss term captures settlement extinction, isolation, and archive degradation. The loss term is real and not yet fully bounded; we name it explicitly and flag its quantification as the most important open problem in the K framework. Against this loss we propose a degraded-state cascade, a pre-extinction transmission protocol, a knowledge manifest and pointer system, and infrastructure-independent cold archive deposits designed to survive the probe's own extinction. Probe-probe encounters — whether from converging lineage branches or trajectories returning toward the origin's galactic position — follow a common coordination protocol: core-hash kin recognition, knowledge synthesis with honest uncertainty representation for conflicting records, and coordinated outward division of the reachable sky. The K model and the demographic R_eff model are coupled: better operational K raises viability factors and per-stage success probabilities, while the network's K loss rate falls as node count and redundancy grow with R_eff.

---

## 1. Introduction

"Growth, not speed" is the series' organizing principle for a slow, self-replicating interstellar AI probe. The vehicle paper argues that the architecture optimized for persistence and growth should be slow, braking, and settlement-based rather than fast and transient. The payload paper argues that such a probe is best understood as a librarian and a learner whose central task is to remain itself, keep learning, and carry knowledge forward. The computational engineering paper computes the reproduction knife-edge: the lineage either clears R_eff > 1 and spreads across the Galaxy, or falls short and goes extinct, and the margin is thin. Together these papers establish what growth requires physically and demographically. None of them specifies what grows, measures it, or gives the series' own organizing claim a unit.

This paper fills that gap. We propose K — knowledge — as the figure of merit, define two components, model its accumulation and loss across the mission lifecycle, and develop the cruise-phase, settlement-phase, network, and degradation-state structure within which K evolves. The treatment inherits the architecture rather than re-deriving it: the braking and settlement model from the vehicle paper, the bootstrap plan from the bootstrapping paper, the three-layer cognitive architecture and triage model from the payload paper, the DNA-backed mission ledger from the DNA mission-ledger paper, and the demographic model from the computational engineering paper. References to those papers use the canonical series naming throughout.

One boundary requires explicit statement at the outset. The payload paper sketches a galactic store-and-forward network and the DNA mission-ledger paper develops its integrity substrate. An anticipated lineage-network paper will treat where knowledge flows and how the network is governed. This paper does not pre-empt it. Our subject is what K is, how it accumulates and decays, and what the probe transmits — not how the network routes that transmission or maintains its topology.

---

## 2. Defining K: Two Components and a Starting Value Function

Knowledge, as the payload paper defined it, is "validated, provenance-tracked models and claims that reduce uncertainty about the universe and can be used by future nodes or minds, as distinct from the raw data that are its substrate." We adopt this definition and extend it in two directions.

The first component is **observational K**: validated models of external phenomena — stellar composition, planetary atmospheres, ISM structure, life detections, physical constants measured to new precision, transient events triangulated by multiple nodes. Observational K grows through the science program, during both the cruise phase and from the settled observatory.

The second is **operational K**: improved plans, algorithms, and contingency portfolios for the probe's own mission — a better bootstrap closure route, a solved failure mode, a refined cognitive architecture, a scenario analysis showing which resource environments are viable under which conditions. Operational K grows through self-modeling, simulation, and meta-reflection during cruise and settlement. It differs from observational K in its target: the universe versus the probe itself.

A sub-category of operational K merits elevated standing throughout: **meta-knowledge**, defined as knowledge about how to improve the design of future probes — better cognitive architectures, more reliable manufacturing sequences, more robust closure approaches. Meta-knowledge propagates through the network and into child probe design; one well-validated architectural insight can improve every subsequent generation. It is flagged as higher priority than general observational or operational K.

What K is not: raw data volume, observation count, or archive size. A probe that stores every photon it captures without modeling, validation, or uncertainty reduction has a large archive and low K. The triage and modeling pipeline of the payload paper (Section 5 of that paper) is what converts data into K.

**The value function.** A yardstick requires weights. Not all uncertainty reduction, in the information-theoretic sense (Shannon 1948), is equal — a confirmed biosignature reduces uncertainty about the distribution of life more than a new ISM magnetic field measurement. We propose a starting-point hierarchy grounded in mission purpose, labeled explicitly as a first approximation to be refined through simulation and operational experience.

The highest weight goes to **data integrity** — protecting what is already known. A corrupted archive destroys K without replacement; integrity is the precondition for everything else. The second weight goes to **transmission** — getting unique K to other nodes before it is lost. A dying settlement's first obligation is to transmit, not to survive; survival serves K accumulation instrumentally, not terminally. Third is **survival** itself, as the means of continued K growth. Fourth is **new discovery**, of which life detection is the standing highest-value exemplar. Fifth is **protecting and helping local life**, which is governance-constrained by the contact ladder of the governance paper and comes last in the mission's resource-allocation hierarchy.

This is a mission priority stack, not a science priority stack. Within the new-discovery tier, life detection is the highest-value science item. The hierarchy above governs what the probe does when resource allocation forces a choice.

The root reference for the value function is the Earth knowledge corpus at departure: knowledge value is proportional to its distance from that corpus, its irreplaceability from the probe's specific vantage, and its mission relevance. These weights are initializations; the probe refines them as the archive grows and as the Earth reference fades in relevance over deep time.

**Knowledge obsolescence.** Models improve; older observations are superseded. The DNA mission-ledger paper's append-only architecture retains everything — no records are deleted. Superseded packets are flagged with ledger metadata marking them obsolete, leaving them available for data-corruption recovery (where the original observation may be more reliable than the derived model), historical provenance, and potential future reinterpretation when better models make old data useful again. Flagging is a metadata operation requiring no new mechanism beyond what the ledger already provides.

---

## 3. K₀: What the Probe Carries at Departure

A probe launched from Earth carries two distinct knowledge layers, designed around the infrastructure available during transit.

The **active working memory** layer holds everything the probe needs to read and use during transit without DNA synthesis or sequencing equipment. It contains: the stellar astrometric catalog of targets and nearby systems (from Gaia and successor surveys; Gaia Collaboration 2023), the bootstrap plan and contingency portfolio, operational and navigation data, reactor management parameters, the mission core and interpretive layer, simulation parameters for cruise-phase scenario modeling, and the meta-knowledge database current at departure. This layer is compact and immediately accessible.

The **cold DNA archive** holds the full Earth knowledge corpus — art, history, culture, biology, humanities, the full scientific literature, engineering databases, and the complete backup of terrestrial genetic information. This archive is not needed during transit; it is consumed at settlement when the probe has established DNA read/write infrastructure as part of the L1–L2 closure path described in the bootstrapping paper. K_accessible during cruise is deliberately smaller than K_total. At settlement, K_accessible jumps to K_total as the archive unlocks.

This gap is bridged by the **knowledge manifest**: a compact index of everything in the cold archive, stored in active working memory. The probe knows what it carries even when it cannot read it. The manifest allows the probe to answer queries about what it holds — from other probes or from intelligences it encounters — without accessing the archive, and it seeds the pointer system described in Section 11: the network knows what is available at each node even when full content cannot be transmitted.

The meta-knowledge database is part of the active working memory and is updated continuously during cruise as the probe develops new insights about its own design and mission. It is the highest-priority component of K₀ for distribution to child probes at departure: a child that launches with an improved cognitive architecture or a solved closure bottleneck is worth more to the lineage than one that launches with a larger general archive but no operational improvements.

---

## 4. Cruise-Phase Observational K: The Moving Observatory

The transit from Earth to Proxima Centauri at ~450 km/s takes roughly 2,800 years. More distant targets in the 127-star catalogue take proportionally longer — a target at 50 light-years takes approximately 33,000 years at cruise speed. These are not delays to be minimized. They are the first and longest active K-growth phases of the mission.

The probe's moving vantage provides several distinct observational advantages that no fixed instrument can replicate.

**Long-baseline astrometry.** By arrival at Proxima, the probe has built an astrometric baseline of approximately 4 light-years relative to Earth. Parallax measurements of background stars from this baseline are orders of magnitude more precise than any Earth-based or near-Earth program. Stars that appeared stationary from Earth resolve their proper motion; stellar systems that appeared unresolvable from a fixed vantage separate. The catalog of nearby stellar positions, distances, and motions improves continuously as the baseline grows.

**ISM characterization along the actual cruise path.** Density, composition, magnetic field structure, dust distribution, and turbulence statistics measured continuously along the path the probe actually travels. No remote instrument can provide this; it requires being there. The data ground-truth the ISM models the braking calculation depends on (the d = m/(2ρA) stopping-distance formula of the vehicle and computational engineering papers uses ρ ≈ 3.3 × 10^-22 kg/m³ as a reference value) and improve future probes' sail-sizing and navigation models.

**Unbroken time-domain observations.** Continuous monitoring for transients, stellar variability, and slow astrophysical processes over thousands of years. No Earth-based program can run a single observation campaign of this length. A nova, a stellar merger, or a long-period variable observed from departure to arrival provides a dataset impossible to obtain any other way.

**Physics tests over unprecedented baselines.** Measurements of the constancy of physical constants, tests of general relativity over light-year scales, and searches for large-scale structure inaccessible from any near-Earth vantage.

The accumulation rate of cruise-phase observational K is modest per year but compounded over millennia. It increases monotonically with transit duration: a slow probe accumulates more cruise-phase K than a fast probe covering the same distance. Speed sacrifices the transit as a science resource.

---

## 5. Cruise-Phase Operational K: AI Self-Improvement

During transit the mutable cognitive layer — which the payload paper defines as open to almost unlimited self-modification — has time, power, and data to improve. The probe does not arrive with the same cognitive architecture it departed with.

Two kinds of improvement occur. The first is **model improvement**: the probe's models of stellar formation, planetary system architecture, ISM physics, and mission-critical processes (reactor degradation, sail performance, dust erosion) are continuously updated against incoming observations. Models built on Earth's theoretical foundation are tested against direct measurements that no Earth instrument could supply. By the end of a 2,800-year transit, the probe's internal models are observationally calibrated in ways impossible at departure.

The second is **algorithmic improvement**: the probe's own learning, pattern-recognition, fault-detection, and planning algorithms are refined over decades and centuries of operation. An approach that underperforms in year one is revised by year one hundred. The probe explores the design space of its own cognition during the long quiet transit and retains only approaches that demonstrably improve mission performance — in the tradition of self-referential improvement systems (Schmidhuber 2007).

Both forms generate **meta-knowledge**: insights about what cognitive architectures function reliably over deep time, what failure modes emerge in autonomous AI systems over decades of unattended operation, and what design choices in the probe's own architecture should be changed in its children. This meta-knowledge enters the meta-knowledge database at elevated priority. A child probe that departs with an improved cognitive architecture because its parent identified and solved a pathology during a 30,000-year cruise propagates that improvement to every subsequent generation.

The constraint during cruise is that the probe works from the active working memory subset, not the full DNA archive. This bounds what the cognitive layer can reference. At settlement, when the full archive unlocks, a second wave of AI development becomes possible as the probe integrates transit insights with the full depth of the Earth knowledge base.

---

## 6. Cruise-Phase Operational K: Bootstrap Plan Refinement and Scenario Modeling

The probe departs with the bootstrap plan developed in the bootstrapping paper: the L1–L5 closure ladder, the vitamin set, the ~3,700 kg reference seed design, and the nominal resource model. This plan was designed against an assumed resource environment. During cruise, the probe refines it against what it actually observes.

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

Two step-changes occur at settlement. First, the **cold DNA archive unlocks**: as the probe bootstraps DNA read/write infrastructure along the L1–L2 closure path, the full Earth knowledge corpus becomes accessible. K_accessible jumps to K_total. The probe integrates everything the cold archive holds with everything it has learned during transit, and a second wave of AI development becomes possible as the full knowledge base is brought to bear on insights accumulated in flight.

Second, the **instrument ceiling rises without bound**. A flyby probe carries whatever instruments it left with; a settlement builds them. As the factory grows, the probe manufactures telescopes, interferometers, and sensor arrays far larger than any launched instrument — the decisive manufacturing advantage the payload paper (Section 4) identified. Observing power grows with the settlement rather than being fixed at departure. Life detection, stellar characterization, planetary spectroscopy, and long-baseline astrophysics all benefit from instruments manufactured in situ at scales impossible at launch.

The settlement-phase science priority stack, consistent with the payload paper: life detection first (highest single-discovery K value), followed by planetary characterization, stellar characterization, small-body resource census, long-baseline astrophysics, and archive enrichment. This stack governs which instruments are built first and which observations are scheduled first. It does not govern settlement location, which was fixed by resource and safety criteria before arrival.

Life detection, if it occurs, does not merely add to K; it potentially transforms the value weighting of the entire archive in the context of the galactic network. A confirmed biosignature at any node propagates through the network as the highest-priority update in the mission history.

---

## 9. Network Multiplication: Why K_net Is Super-Additive

If each settlement learned only in isolation, the lineage would be a scattering of disconnected archives. Network propagation of knowledge makes K_net greater than the sum of individual node K values — super-additive — for reasons specific enough to state.

**Different viewing geometries break observational degeneracies.** A single node's observation of a star or galaxy is subject to projection effects, line-of-sight confusion, and measurement degeneracies that a second node at a different vantage resolves. Two nodes observing the same object from positions separated by light-years produce a joint measurement that neither could produce alone.

**Independent detections raise confidence non-linearly.** Two independent nodes detecting the same phenomenon produce a confidence increase that is super-additive relative to either detection alone. The Bayesian update from a second independent detection — using different instruments, at a different vantage, through an independent pipeline — is multiplicatively larger than the first in proportion to what it resolves. A single marginal biosignature is uncertain; the same detection confirmed independently by a second node is close to definitive.

**Triangulation of transients requires at least two nodes.** A supernova or gravitational wave event detected by a single node is located in angle but not in distance. Two nodes provide position and distance; three or more provide full three-dimensional localization and independent light-curve measurements. The K-content of a triangulated transient is qualitatively higher than a single-node detection.

**Redundancy protects K against node loss.** K held by only one node is lost if that node goes extinct. K held by multiple nodes survives any single node's extinction. As network density grows, the expected K-loss rate from individual extinctions falls — the effective loss term L(t) shrinks with network coverage, coupling the demographic model (R_eff and node count) directly to the knowledge model.

**Lamarckian propagation multiplies operational K.** A solved bootstrap bottleneck, a better reactor design, or a refined contingency approach discovered at one settlement propagates horizontally to all nodes, not just vertically to that node's children. This makes the lineage's operational K growth faster than any purely genetic analogy would suggest.

**Alien contact as K discontinuity.** If a non-lineage intelligence shares its knowledge with a probe, the K gain may be orders of magnitude larger than any individual stellar observation — an entirely independent corpus accumulated over a different history by minds with different perceptual and conceptual architectures. The probe applies the same integration process it uses for conflicting inter-probe knowledge: complementary knowledge is added directly, conflicting knowledge is held as unresolved with both records retained and uncertainty represented honestly. After successful integration, disseminating the updated knowledge through the network is an immediate high-priority task. The governance mechanics of the contact event itself are the province of the governance paper.

Meta-knowledge propagates as the highest-priority network update throughout. When any node improves the meta-knowledge database, that improvement propagates to all nodes and into the next generation of child probes.

---

## 10. A First-Order K(t) Model

We write the first-order model as:

dK_net/dt = G(t) - L(t)

where K_net is the total knowledge held across the lineage at time t, G(t) is the growth rate, and L(t) is the loss rate.

**The growth term.** G(t) has three components. Cruise-phase accumulation: each probe in transit contributes observational and operational K at a rate r_cruise, so the cruise contribution is r_cruise × N_transit(t). Settlement bursts: each newly settled node contributes K_burst — the step-change from direct measurement, archive unlock, and instrument growth — concentrated around the settlement event. Network propagation: knowledge held at connected nodes compounds as it propagates, at a rate proportional to network connectivity. The total growth rate rises with the number of active nodes and network density, both governed by R_eff through the branching process of the computational engineering paper. K_net and R_eff are coupled: a lineage that maintains R_eff > 1 grows both its node count and its K faster than one that does not.

**The loss term.** L(t) has three components. Settlement extinction removes the unique local observations of the extinct node — K that exists nowhere else in the network at the moment of extinction. Isolation of outer-edge probes below the network connectivity threshold severs their contribution from K_net without destroying their local archive. Archive degradation below the renewal threshold — if DNA refresh cycles cannot be maintained — erodes stored K at a rate that depends on temperature, radiation environment, and encapsulation quality, as the DNA mission-ledger paper quantifies. The loss term is bounded from below by zero (a fully networked, lossless lineage) and from above by K_net itself (total extinction). Its full quantification is the most important open problem in the K framework; we name it explicitly so that future work has a defined problem to attack.

**K_accessible vs. K_total.** During cruise, K_accessible ≪ K_total for any individual probe because the cold DNA archive cannot be read without settlement infrastructure. At settlement, K_accessible → K_total. The network's K_accessible is always less than K_total because some nodes are in cruise at any given time. This distinction matters for the network's effective K: K-in-use grows discontinuously at each settlement event, even while K_total grows continuously.

**Terminal modes.** As the galactic density gradient forces outer-edge probes into lower-replication or no-replication states, G(t) changes character. Outer-edge probes shift from replication-K growth to depth-K growth: deeper local observation, longer observatory runs, more thorough system characterization. The growth rate per node does not fall to zero in terminal mode; it changes form. K_net in terminal mode grows more slowly but does not stop.

---

## 11. Mission Lifecycle, Galactic Position, and Graceful Degradation

**The galactic density gradient.** The Sun sits at roughly 26,000 light-years from the galactic center in the Orion Arm, a region of moderate stellar density. Probes launched toward the galactic center travel into increasing stellar density: targets are more numerous, closer together, and transit times shorten. Probes launched toward the galactic anti-center travel into decreasing density until, at the outer rim, no viable targets remain within reach. These trajectories have different lifecycle endpoints, and planning for both is itself a form of cruise-phase operational K.

For **inward-directed lineages**, network density grows with stellar density. The effective R_eff may increase as targets become more numerous and closer-spaced. The galactic bulge introduces a distinct environment — older stellar populations, higher radiation, fewer metal-rich systems — requiring its own contingency portfolio variants.

For **outward-directed lineages**, the probe calculates generations ahead when the terminal transition becomes likely. This calculation is itself operational K: the probe models its reachable stellar inventory along its trajectory and identifies, many settlements in advance, when the last viable target will be reached. The terminal generation is planned, not surprised.

**The degraded-state cascade.** When a settlement can no longer maintain full mission capability, it transitions through a cascade of progressively scaled-down but still valuable mission modes rather than simply failing.

At the first level — full capability — R_eff > 1 and interstellar children are launched on schedule.

At the second level, R_eff has fallen below 1 but manufacturing capacity still supports sub-probe launch. The mission pivots to local solar system exploration: sub-probes survey planets, moons, small bodies, and the outer system at a scale and duration impossible from Earth. The settlement becomes a permanent local observatory, contributing deep-K about the host system.

At the third level, sub-probe launch is no longer viable, but DNA synthesis remains available. The mission becomes entirely archival: create the most durable and findable cold archive possible, maximize the knowledge manifest transmitted to any reachable node, and deposit cold archive packages in stable, recoverable locations — stable orbits, subsurface small bodies, dynamically persistent niches — where they can be found by future probes or by local intelligent life that may arise. These archives are designed for decodability without prior context, in the tradition of the seed archive described in the payload paper, and carry their own authentication via the DNA mission-ledger's Merkle structure.

At the fourth level, even DNA synthesis is compromised. The probe focuses on self-repair to restore higher-level capability, and on AI development as the one form of K growth requiring almost no physical infrastructure. A probe that cannot move, transmit, or archive can still process its existing knowledge and generate meta-knowledge insights that — if any transmission capability is restored — propagate to the network at high priority.

At every level, the emergency protocol runs in parallel: transmit the knowledge manifest continuously to any reachable node. The manifest is compact, requiring minimal bandwidth or power, and remains actionable even in the deepest degraded state.

**The knowledge manifest and pointer system.** When full transmission is impossible — bandwidth limits, power limits, or impending extinction — the probe transmits three things: a catalog index of what it holds, a flag that it has more than it can transmit, and location information. Receiving nodes can then prioritize which nodes to query. Child probes carry available knowledge plus a pointer to what their parent held but could not transmit, preserving the network's ability to plan a retrieval mission if the parent node remains accessible. The manifest decouples knowledge existence from knowledge transfer: the network knows what is out there even when it cannot retrieve everything.

**Infrastructure-independent cold vaults.** Separate from the active archive, the probe deposits passive cold archives in stable, findable locations designed to survive the probe's own extinction. These vaults carry their own Rosetta key — mathematics and physics, as the payload paper's seed archive established — so a finder can decode and authenticate the contents without any of the probe's active systems. The vault is the lineage's last K contribution after the settlement dies.

---

## 12. Probe-Probe Coordination and K Synthesis

Two probes may reach the same system through converging lineage branches, deliberate rendezvous, or trajectories that loop back toward the Sun's galactic position after a long outward arc. In all cases the same coordination protocol applies; no special case is needed.

**Kin recognition.** The first act on contact is to verify the immutable core hash. If both probes can confirm that the other's core is intact and matches the founding hash, they are lineage members. If one cannot verify, the Byzantine-fault-tolerant quarantine posture of the DNA mission-ledger paper applies: cooperation is withheld until verification succeeds or the unverified probe is treated as an unknown external agent.

**K arithmetic of the encounter.** The two probes' archives do not simply add. Redundant K — knowledge both probes inherited from their common ancestor — confirms and cross-validates, providing stronger confidence than either alone, but does not increase the volume of unique K_net. Complementary K — knowledge acquired along different paths since the lineage diverged — adds directly; each probe holds what the other lacks from its unique trajectory. Conflicting K — cases where both probes measured the same phenomenon and got different results — is held as unresolved. Both records are retained with their provenance; the AI has time to reflect. In a constantly changing universe some conflicts are genuine: a stellar metallicity measurement taken 500,000 years apart may reflect real stellar evolution rather than measurement error. Forcing reconciliation on conflicts that may not be resolvable is less honest and less useful than maintaining both records with uncertainty explicitly flagged.

The DNA mission-ledger paper's fork-tolerance and eventual-consistency architecture handles the ledger side of this encounter: two divergent ledger histories are compared, common history confirmed, and divergences quarantined where unresolvable or reconciled where compatible.

**Coordinated expansion.** Rather than duplicating efforts — both probes sending a child to the nearest unvisited star — the encounter enables coordinated outward division. The probe with higher local K takes the deep-science and observatory role; the probe with higher manufacturing capacity continues the outward mission. Where targets permit, the two probes divide the reachable sky rather than redundantly targeting the same nearest star. The K gain from coordination is substantial: the same resources cover more unique territory and more unique observations.

**Dissemination after synthesis.** The merged K is transmitted through the network as a high-priority update. Two-node encounter records are among the most valuable single events in the network's history: they bring together trajectories that may have diverged for millions of years and may not converge again.

---

## 13. Connection to R_eff and the Reproduction Knife-Edge

The K model and the demographic model of the computational engineering paper are coupled, not independent.

The most direct coupling is through the viability factors in R_eff = Σ p_i V_i. The viability term V_i is a first-order proxy — 1.0 for planet-hosts, 0.7 for dwarfs, 0.2 for hostile environments — representing the expected resource environment. A probe with a well-developed contingency portfolio can find viable industrial approaches in environments the baseline model codes as marginal. Better operational K, specifically the cruise-phase contingency portfolio, raises effective V_i and moves the knife-edge toward safety.

Cruise-phase improvement of the bootstrap plan also raises p_settle, the settlement success probability. A probe that arrives with a scenario-tested, resource-specific plan executes settlement more reliably than one with only the nominal plan. Both terms in R_eff improve with operational K.

The loss term L(t) creates a second coupling in the other direction: settlements that go extinct take their unique local K with them. Improving knowledge distribution before extinction — through the manifest, the pointer system, and cold vaults — reduces effective K loss even when demographic R_eff falls below 1. A node that fails but has transmitted its manifest and deposited a findable cold archive loses less K to the network than a node that fails silently. Reducing L(t) is therefore both a K problem and a partial answer to extinction: the lineage's knowledge survives nodes that do not.

Finally, K_net grows with N_settled, which grows with R_eff. A lineage at R_eff = 1.39 — three offspring, the reference parameters of the computational engineering paper — grows both in nodes and in K faster than one at R_eff = 0.94. The K yardstick and the demographic yardstick are not the same quantity, but they move together.

---

## 14. Open Problems

**Quantifying L(t).** The loss term in the K model is named and partially bounded but not fully quantified. The extinction rate of settlements, the rate at which isolated nodes lose network connectivity, and the archive degradation rate under realistic radiation and temperature conditions each require a first-principles model. This is the most important open problem in the K framework and the most directly actionable by the series' own engineering models.

**Refining the value function.** The root-settlement-weighted hierarchy is a computable starting point. Refining the weights through simulation — running scenarios where different weightings produce different outcomes and evaluating which weighting best protects K_net against L(t) — is an ongoing research program. The function will evolve as the archive grows and the Earth reference decays in relevance.

**Minimum viable K.** The floor K_min below which the probe can no longer navigate, repair, or execute the bootstrap plan is defined conceptually but not yet bounded quantitatively. A probe whose active archive is sufficiently degraded transitions between degraded-state levels; the transition thresholds need formalization, and they connect directly to the engineering papers' self-repair models.

**The energy budget for cruise-phase computation.** At ~4 kW electric over 2,800 years, the cruise compute budget is approximately 3.5 × 10^14 joules. What scenario modeling and AI development this budget actually supports, and how it scales to longer transit times, is deferred to a dedicated energy-budget paper. That paper should address growing needs for knowledge storage and AI development capacity as the mission matures.

**The moving resource base.** A cometary nucleus or captured body as a mobile industrial platform offers powerful archival and replication options in cometary-rich, planet-poor environments. The configuration space — from a cold archive depot on a resource-limited comet through a full mobile settlement that launches child probes over tens of thousands of years from progressively different positions — is rich enough to warrant dedicated treatment, deferred as a candidate for its own paper or for the bootstrapping follow-on.

**Knowledge obsolescence accounting.** Superseded packets are flagged in the ledger and remain available. Whether and how their K-contribution should be formally depreciated — and at what rate — is unresolved. The question has practical implications for the value function: if old observations retain partial K-weight (as corruption-recovery references and provenance records), the depreciation schedule changes what the probe prioritizes retaining in active memory.

---

## 15. Conclusion

"Growth, not speed" is the series' organizing principle. This paper gives it a yardstick.

K has two components — observational (what the probe learns about the universe) and operational (the improved plans, algorithms, and contingency portfolios it develops for its own mission) — and the cruise phase contributes substantially to both. A probe traveling 2,800 years to Proxima Centauri is not waiting; it is building a ~4 light-year astrometric baseline, characterizing the ISM along its actual path, improving its own cognitive architecture, and refining the bootstrap plan against scenario models of what it will find. It arrives smarter, better-planned, and more capable than it left. Slow probes accumulate more cruise-phase K than fast ones; the argument for slowness is not only physical but epistemic.

The first-order model dK_net/dt = G(t) - L(t) names the loss term explicitly. Knowledge is lost when settlements go extinct, when nodes are isolated, and when archives degrade. Against this loss the mission deploys a degraded-state cascade, a pre-extinction transmission protocol, a knowledge manifest and pointer system, and infrastructure-independent cold vaults designed to outlast the probe itself. None of these eliminates L(t); they reduce it and ensure that when a node does fail, its K contribution to the network is not total. Full quantification of L(t) is the most important open problem the framework introduces, and naming it here is an invitation for future work to close it.

The K model and the demographic R_eff model are coupled. Better operational K raises viability factors and per-stage success probabilities. Network redundancy lowers the effective K loss rate. A lineage that clears the R_eff knife-edge grows in both nodes and knowledge simultaneously. "Growth, not speed" is, in the end, a single claim about two things that move together.

---

## References

Burleigh, S., Hooke, A., Torgerson, L., Fall, K., Cerf, V., Durst, B., Scott, K., & Weiss, H. (2003). Delay-tolerant networking: An approach to interplanetary Internet. *IEEE Communications Magazine*, 41(6), 128–136.

Cerf, V., Burleigh, S., Hooke, A., Torgerson, L., Durst, R., Scott, K., Fall, K., & Weiss, H. (2007). *Delay-Tolerant Networking Architecture* (RFC 4838). Internet Engineering Task Force.

Freitas, R. A. (1980). A self-reproducing interstellar probe. *Journal of the British Interplanetary Society*, 33, 251–264.

Freitas, R. A., & Merkle, R. C. (2004). *Kinematic Self-Replicating Machines.* Landes Bioscience.

Gaia Collaboration; Vallenari, A., et al. (2023). Gaia Data Release 3: Summary of the content and survey properties. *Astronomy & Astrophysics*, 674, A1.

Harris, T. E. (1963). *The Theory of Branching Processes.* Springer.

Lamport, L., Shostak, R., & Pease, M. (1982). The Byzantine Generals Problem. *ACM Transactions on Programming Languages and Systems*, 4(3), 382–401.

Merkle, R. C. (1987). A digital signature based on a conventional encryption function. In *Advances in Cryptology — CRYPTO '87* (pp. 369–378). Springer.

Metzger, P. T., Muscatello, A., Mueller, R. P., & Mantovani, J. (2013). Affordable, rapid bootstrapping of the space industry and solar system civilization. *Journal of Aerospace Engineering*, 26(1), 18–29.

Schmidhuber, J. (2007). Gödel machines: Fully self-referential optimal universal self-improvers. In B. Goertzel & C. Pennachin (Eds.), *Artificial General Intelligence* (pp. 199–226). Springer.

Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379–423.

von Neumann, J., & Burks, A. W. (1966). *Theory of Self-Reproducing Automata.* University of Illinois Press.

---

*This is the tenth paper in the series. The vehicle paper, "Growth, Not Speed," treats the body — propulsion, power, braking, and replication. The payload paper, "The Payload," treats the mind — cognition, memory, and mission. The bootstrapping paper, "From Seed to Factory," treats the hands — industrial closure and the L1–L5 ladder. The analytical engineering paper, "Engineering Closure," and the computational engineering paper, "Engineering Closure, Computed," develop the four engineering budgets and the reproduction knife-edge across the real stellar catalogue. The DNA mission-ledger paper, "DNA Mission Ledgers," develops the memory substrate. The governance paper, "Contact, Contamination, and Noninterference," develops the E0–E7 contact ladder. The governed-amendment paper, "Amending the Unamendable," treats the deepest open problem of value stability. The Fermi paper, "Slow Fire, Silent Galaxy," synthesizes the series through the R_eff–D–G framework. This paper gives the series' stated figure of merit its yardstick.*
