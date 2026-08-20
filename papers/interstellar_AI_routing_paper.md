# Three Dispatches: Fleet Routing and Catalogue Coverage for a Self-Replicating Interstellar Lineage

**S. Stone**
*Working draft, revision 2 (revised after a pre-deposit dual review, with every simulation number re-verified against the accompanying code). Part of a multi-paper series on a slow, self-replicating interstellar AI probe: this is the routing companion to the computational engineering paper ("Engineering Closure, Computed") — given that paper's R_eff result, it asks how settled nodes should dispatch offspring across the real 127-star catalogue. The simulation accompanies the paper as routing.py.*

---

## Abstract

The computational engineering paper establishes that a self-replicating interstellar lineage must maintain R_eff > 1 — on average more than one successful child settlement per node — to avoid extinction. This paper asks the next question: given R_eff > 1, how should each settled node dispatch its offspring to maximise coverage of the 127-star catalogue, and how robust is the resulting network to individual node failures? We model the catalogue as a reachability graph where edges connect stars within a chosen maximum hop distance, and evaluate three dispatch strategies — nearest-first, viability-first, and coverage-first — by Monte Carlo simulation. The catalogue does not form a single connected component at any natural hop distance: at 10 ly, only 65% of the catalogue is reachable from Earth; at 20 ly, 93%. The graph contains 5–9 articulation points at 15–20 ly hop distances — bottleneck nodes whose failure isolates one to three dependent targets permanently within that graph. Three independent dispatch attempts per target achieve P_cover of 0.90–0.95 for planet-host targets within 20 ly, which we call the three-dispatch rule. Among the three strategies, coverage-first — which directs new dispatches toward targets with fewest prior attempts — achieves 90% catalogue coverage 62,000 years faster than nearest-first, matching viability-first's 93% final coverage and slightly exceeding nearest-first's 91%. The results establish that R_eff > 1 is necessary but not sufficient: the dispatch strategy determines both the time to coverage and the lineage's resilience to node loss, and coverage-first is demonstrably the better policy for the sparse stellar neighbourhood.

---

## 1. Introduction

The computational engineering paper computes R_eff = Σᵢ pᵢVᵢ — the expected number of successful child settlements produced per node, summed over the nearest candidate targets — across the real 127-star catalogue. The result is a knife-edge: mean R_eff of 0.48, 0.94, 1.39, and 1.85 for one, two, three, and four offspring per node. Three offspring is the minimum that drives the lineage above the Galton-Watson extinction threshold (Harris 1963), and only then with per-stage reliability near or above 0.9. The demographic conclusion is clear.

What that paper leaves open is the dispatch strategy: how does a settled node choose which stars to target with its offspring, and how does the lineage as a whole ensure that the full catalogue is eventually reached rather than only the easy, nearby stars? The R_eff model assigns offspring to the nearest available targets, which maximises per-node R_eff, but says nothing about coverage as a network property. A lineage could maintain R_eff > 1 indefinitely while leaving a significant fraction of the catalogue unreached, if each settled node concentrates its dispatches on nearby high-viability targets that are also the nearest targets of its neighbours.

This paper addresses the dispatch problem by treating the catalogue as a network and evaluating three dispatch strategies under Monte Carlo simulation. Monte Carlo studies of galactic exploration by probe fleets have a direct lineage (Bjørk 2007; Cotta & Morales 2009; Forgan, Papadogiannakis & Kitching 2013), and Landis (1998) framed colonization coverage as a percolation problem; this paper differs in optimising dispatch policy over the real local catalogue rather than exploration time over synthetic stellar distributions. Three results emerge. First, the 127-star catalogue does not form a single connected component at natural hop distances: at a 10 ly hop — comfortably inside the standard-profile fuel range of ~12 ly — only 65% of the catalogue is reachable from Earth, and even at 20 ly, 7% remains isolated in disconnected components of the curated catalogue. Second, the graph at practical hop distances contains articulation points — nodes whose failure permanently isolates dependent targets — which must be prioritised in the dispatch plan. Third, among the three dispatch strategies tested, coverage-first (dispatch toward targets with the fewest prior attempts) reaches 90% catalogue coverage 62,000 years faster than nearest-first while achieving the same ceiling coverage, confirming that dispatch strategy matters as much as R_eff for the lineage's time to coverage.

The simulation accompanies this paper as a single Python module (routing.py) building on the catalogue and engineering code of the computational engineering paper.

---

## 2. The Reachability Graph

The 127-star catalogue used throughout this series is a curated selection of notable nearby systems — confirmed planet-hosts, bright or well-characterised stars, and the nearest-known systems — with positions from Gaia astrometry (Gaia Collaboration 2023), extending to roughly 65 light-years from Earth. It is not an exhaustive census of all stars within that volume; many faint M-dwarfs and uncharacterised systems exist within 65 ly but are not catalogued — M dwarfs are roughly 60% of even the carefully completed 10-parsec census (Reylé et al. 2021), and the curated list keeps only notable systems. The reachability analysis on this selection therefore represents a pessimistic lower bound on network connectivity: the actual interstellar network, routing among all stellar systems, would be substantially denser.

We model the catalogue as an undirected graph: two nodes are connected by an edge if the distance between them is at most a maximum hop distance h. This hop limit represents the maximum target range to which a node will dispatch; it is set by fuel duration, navigation, and the acceptable per-dispatch success rate rather than by braking (which, as shown below, is negligible at these ranges) — a design choice, not a fixed physical constant — and the routing paper's task includes understanding how coverage depends on h.

**Connectivity results.** The catalogue's connectivity as a function of h reveals a significant tension between braking feasibility and network coverage:

At h = 8 ly, the graph fragments into 44 connected components, and the Sun reaches only 56 of 126 non-solar stars (44%). Short hops sacrifice coverage.

At h = 10 ly, 36 components remain, and the Sun reaches 82 stars (65%). Braking is not the constraint at this distance: the stopping distance d = m/(2ρA) for the reference 3,700 kg seed with a 100 km magnetic sail is ~0.02 ly, achieved in about 25 years — a negligible fraction of any hop beyond ~0.1 ly. The practical constraint at 10 ly is fuel duration: on the standard K-research power profile (~150 W cruise draw), the baseline ²³⁵U fuel charge sustains roughly 8,000 years of cruise, corresponding to ~12 ly. For shorter hops or range-maximizer profiles (~50 W hibernation), the unassisted range extends to ~36 ly; for longer standard-profile hops, supplementary fuel costs less than 0.4% of seed mass per 10 ly. Hop range is therefore not physically constrained at any of the distances evaluated here.

At h = 15 ly, the graph consolidates to 19 components, and the Sun reaches 106 stars (84%).

At h = 20 ly, 10 components remain, covering 117 stars (93%) reachable from the Sun. The graph's mean degree rises to 31 — each star can directly reach, on average, 31 others within a single hop — providing substantial routing redundancy within the connected component.

Even at h = 20 ly, the Sun cannot reach 9 stars (7%) through the curated catalogue. These isolated stars lie in separate components at distances greater than 20 ly from any star reachable from the Sun via the curated catalogue's sparse edges. In the actual stellar neighbourhood, faint M-dwarfs and other uncharacterised systems at intermediate distances would bridge these gaps; within the curated catalogue, they represent a floor that no finite dispatch budget can overcome without longer-range direct hops.

**A note on catalogue completeness.** The series' canonical "127 stars within 100 ly" refers to this curated list. The actual farthest catalogued star is at ~65 ly, and many stars between 65 ly and 100 ly exist but are absent because they are not among the most notable nearby systems. Fleet routing in the full stellar neighbourhood would use a much larger, denser graph; the results here are conservative because the catalogue undersamples the available relay points.

---

## 3. Articulation Points

Within the connected component reachable from the Sun, certain nodes are articulation points: their removal disconnects one or more additional stars from the rest of the Sun-reachable component. Because each settled node is a permanent installation rather than a transient relay, node loss is assumed rare but is irreversible (settlement collapse — a failure mode the series names but does not yet model). Articulation points deserve priority in the dispatch plan because their isolation would permanently strand dependent targets.

At h = 15 ly, the reachable component contains 9 articulation points:

Mu Cassiopeiae and Beta Comae Berenices each isolate 3 stars: Mu Cassiopeiae is the sole link to Iota Persei, Theta Persei A, and Upsilon Andromedae; Beta Comae Berenices is the sole link to Arcturus, Eta Bootis, and Tau Bootis A. These are the network's highest-leverage nodes.

Gliese 581 isolates 12 Ophiuchi and Gamma Serpentis. At h = 15 ly, 12 Ophiuchi is only reachable via Gliese 581; losing Gliese 581 (which is itself a planet-host) cuts off both dependent stars.

The remaining six articulation points (Beta Hydri, 107 Piscium, Pi3 Orionis, 12 Ophiuchi, Theta Persei A, Eta Bootis) each control access to one star.

At h = 20 ly, the expanded reachability restructures the bottlenecks: Chi1 Orionis becomes the sole link to Pollux, 55 Cancri A, and Castor A; losing Chi1 Orionis would isolate a three-star cluster containing two planet-hosts (Pollux and 55 Cancri A). Gliese 667 C controls access to two stars, one of them a planet-host (Beta Trianguli Australis and HD 147513).

The design implication is direct: articulation points should receive at least n = 3 dispatch attempts before the coverage-first strategy begins directing dispatches to non-critical targets. A dispatching node aware of the graph structure should mark its articulation-point neighbours as "critical path" targets and prioritise them accordingly.

---

## 4. The Three-Dispatch Rule

Before examining dispatch strategies, we establish the coverage probability that a given number of independent dispatch attempts provides for a target at a given distance.

A single dispatch to a target at distance d_ly succeeds with probability:

p(d) = p_stage^4 × p_cruise^d

where p_stage = 0.9 is the per-stage survival (manufacture, launch, brake, settle) from the computational engineering paper's reference parameters, p_cruise = 0.99 per light-year is the cruise survival, and the four-stage exponent corresponds to the four named mission phases. The probability that at least one of n independent dispatches succeeds — the coverage probability — is:

P_cover(p, n) = 1 − (1 − p)^n

For the catalogue's distance range, the results are:

At d = 4.246 ly (Proxima Centauri), p = 0.629: n = 1 gives P_cover = 0.629; n = 2 gives 0.862; n = 3 gives 0.949.

At d = 15 ly (mid-range catalogue targets), p = 0.564: n = 1 gives 0.564; n = 2 gives 0.810; n = 3 gives 0.917.

At d = 20 ly, p = 0.537: n = 1 gives 0.537; n = 2 gives 0.785; n = 3 gives 0.901.

At d = 64.5 ly (the catalogue's farthest targets), p = 0.343: n = 1 gives 0.343; n = 2 gives 0.569; n = 3 gives 0.717.

These are p_leg coverage probabilities; for viability-weighted effective success (multiplying by V = 1.0 for planet-hosts, 0.7 for ordinary dwarfs, 0.2 for giants and white dwarfs), the per-dispatch success rate is lower. For an ordinary dwarf at 20 ly, p_eff = 0.537 × 0.7 = 0.376, and three dispatches give P_cover = 0.757.

The three-dispatch rule follows from this analysis: three independent dispatch attempts per target achieve P_cover = 0.90 or better for planet-host targets within 20 ly, and P_cover = 0.76–0.95 for planet-hosts and ordinary dwarfs within 20 ly (falling to 0.56–0.72 at the catalogue's 64.5 ly extreme). A fourth dispatch improves the nearest targets to P_cover > 0.95 but offers diminishing returns at the cost of diverting a dispatch away from an uncovered target elsewhere. For catalogue coverage as a network objective — reaching all reachable targets rather than maximising any single target's success probability — three dispatches per target is the natural floor and four is the natural ceiling.

The three-dispatch rule interacts directly with failure detection. The lineage-network paper establishes a heartbeat-absence detection threshold T_silence of approximately 500–5,000 years for the 127-star catalogue (approximately T_beacon × 3 + maximum relay latency, which that paper gives as a lower bound). A settled node that dispatched a probe and heard no settlement beacon after the expected transit time plus T_silence re-classifies the dispatch as a failure and initiates a second attempt. A third attempt follows a second T_silence timeout. The three-dispatch rule emerges naturally from this mechanism, with the timing ensuring that re-dispatch attempts from the same source node cover the T_silence detection cadence.

---

## 5. Dispatch Strategies

We evaluate three dispatch strategies for a settled node with n_offspring = 3 offspring probes to send:

**Nearest-first**: dispatch to the three nearest unsettled reachable targets. This minimises transit time for each dispatch and maximises the node's individual R_eff in the short term, but concentrates the lineage's expansion on the local stellar neighbourhood and defers distant targets indefinitely.

**Viability-first**: dispatch to the three highest-viability unsettled reachable targets (planet-hosts preferred, then ordinary dwarfs, then hostile environments). This maximises the quality of target selection but shares with nearest-first the tendency to concentrate dispatches on the same high-value targets rather than spreading coverage.

**Coverage-first**: dispatch to unsettled reachable targets with the fewest prior dispatch attempts, breaking ties by distance. This explicitly minimises coverage gaps: a target with zero prior attempts takes priority over one with one attempt, regardless of the latter's distance or viability, until the coverage gap is closed. Within the same dispatch-count tier, distance serves as the tiebreaker.

The coverage-first strategy embodies a different objective than the individual-node R_eff maximisation of the computational paper: it optimises for the network's collective coverage of the catalogue rather than any single node's expected offspring count.

---

## 6. Simulation Results

We simulate lineage expansion as a Monte Carlo process. Starting with the Sun settled at time zero, each settled node dispatches offspring to chosen targets, each probe traverses its target distance at 450 km/s, and on arrival succeeds with probability p(d) × V (per-dispatch survival times target viability). A successful probe settles its target, which then dispatches offspring after a replication time of 10,000 years. A failed probe triggers a re-dispatch from the source node after T_silence = 5,000 years; the three-attempt cap governs fresh target selection, while a source that has detected a failure re-dispatches until success or the horizon — a simulated policy somewhat more persistent than the three-dispatch ceiling §9 recommends. The simulation runs 30 independent trials at each parameter configuration, each trial running over a 500,000-year horizon. A maximum hop of 20 ly is used to capture the most complete connected subgraph.

**Strategy comparison (n_offspring = 3, h = 20 ly, 30 trials).**

Nearest-first achieves a mean coverage of 91% (minimum 91%) across trials and reaches 90% coverage in a mean of 230,000 years (all 30 trials succeed).

Viability-first achieves mean coverage 93% (minimum 92%) and also reaches 90% in a mean of 230,000 years.

Coverage-first achieves mean coverage 93% (minimum 91%) and reaches 90% in a mean of 168,000 years — 62,000 years sooner than either alternative, matching viability-first's 93% final coverage and slightly exceeding nearest-first's 91%.

The time difference arises because coverage-first prevents the "rich get richer" failure mode of the other strategies: nearest-first and viability-first concentrate early dispatches on the same nearby cluster of high-quality targets, leaving distant or medium-viability targets without a first attempt until the nearby cluster is saturated. Coverage-first explicitly redirects capacity toward untouched targets as soon as the most urgent coverage gaps appear.

The final coverage ceiling of ~93% at h = 20 ly reflects the graph-structural limit identified in §2: the 7% of the catalogue residing in isolated components cannot be reached at this hop distance regardless of strategy. No dispatch strategy can overcome a connectivity gap; that requires either a larger sail enabling a longer hop, or a relay settlement at an intermediate star not in the curated catalogue.

**Offspring count (coverage-first, h = 20 ly, 30 trials).**

With n_offspring = 1, mean coverage reaches only 19% (zero trials reach 90% within 500,000 years). This confirms the computational paper's result: R_eff < 1 at one offspring is a demographic extinction, and the simulation captures it as coverage failure — the lineage propagates to a few nearby stars and then stalls as failures accumulate faster than successes.

With n_offspring = 2, mean coverage rises to 91%, and all 30 trials reach 90% in a mean of 241,000 years.

With n_offspring = 3, mean coverage is 93% and t90 = 168,000 years — 73,000 years faster than n = 2.

With n_offspring = 4, coverage remains 93% and t90 = 147,000 years, 21,000 years faster than n = 3 but well short of the proportional gain from n = 2 to n = 3. The diminishing returns are clear: adding a fourth offspring reduces t90 by 12% compared to the 30% improvement from the second to the third.

The practical implication is that three offspring is the natural design point, consistent with the computational paper's knife-edge result that R_eff > 1 requires three offspring at per-stage reliability 0.9. Four offspring improves the timing margin but costs significantly more manufacturing capacity at the settled node — each additional offspring is another full seed mass (~3,700 kg) to build and launch, and each additional launch delays the overall reproduction cycle — a cost the simulation's flat tau_rep does not charge, so the 21,000-year gain from a fourth offspring is, if anything, overstated.

---

## 7. Robustness to Node Failure

We evaluate the lineage's coverage robustness by removing k random non-Sun nodes from the reachable graph at h = 15 ly — simulating permanent settlement collapses — and measuring the fraction of the remaining catalogue still reachable from the Sun by BFS (50 random trials at each k). This is a conservative bound: the T_silence mechanism enables re-dispatch, so the simulation would show better robustness; but for coverage reachability, the graph structure establishes the floor.

With k = 1 failed node, mean catalogue reachability drops from 84% to 83%, a 1% loss. The minimum across trials is 81% — a loss of 3%, reflecting rare draws that remove an articulation point and isolate its dependents.

With k = 5 failed nodes, mean reachability falls to 80% and the minimum to 78%.

With k = 10 failed nodes, mean reachability is 77%, minimum 74%.

With k = 20 failed nodes (16% of the catalogue simultaneously), mean reachability falls to 69%, minimum 66%.

The network is moderately but not highly robust. The drop of roughly 0.7–0.8 percentage points per failed node (at small k) sits near the floor set by the removed nodes themselves: each reachable node is ~0.8 points of the catalogue, most removals cost only the node itself because most nodes are not articulation points, and the draws that land outside the Sun-reachable component cost nothing at all. But the presence of 9 articulation points at h = 15 ly means that an unlucky failure in the top tier of articulation points (Mu Cassiopeiae, Beta Comae Berenices) removes three stars from the reachable set in a single event.

The three-dispatch rule is the primary mitigation: if three independent dispatch attempts have each been tried, the probability that all three failed is (1 − p_eff)^3 ≈ 0.05–0.25 for typical targets. On any plausible settlement hazard rate, a node that survived its own settling process is unlikely to be lost before dispatching at least one offspring. The more dangerous failure mode is the permanent loss of a node that had become the sole settled relay to its dependent targets — exactly the articulation-point scenario. Prioritising articulation points in the dispatch plan (as recommended in §3) reduces the probability of this outcome by ensuring that articulation-point targets are settled early and robustly. The security paper in this series extends this analysis from random to targeted removal: an adversary attacking articulation points in leverage order gains a 3–4× multiplier over random loss before the supply of cut vertices is exhausted.

---

## 8. The Isolated Fraction and the Catalogue Ceiling

The 7% of the catalogue unreachable from the Sun at h = 20 ly is not a failure of the dispatch strategy; it is a structural property of the curated catalogue. The nine stars in isolated components at h = 20 ly — TRAPPIST-1, HD 69830, Beta Aquilae, Gamma Cephei, LHS 1140, 51 Pegasi, HD 10647, Pi Mensae, and HD 189733, eight of which are planet-hosts, including two of the best-known in the catalogue (TRAPPIST-1 and 51 Pegasi) — are distant enough from any Sun-reachable star that no probe with a 20 ly effective reach can bridge the gap via the curated relay nodes. The coverage ceiling thus forecloses precisely some of the highest-viability targets.

Three paths exist to close this gap. First, raising the hop distance to h = 30 ly would bring 125 of 126 stars (99%) into the Sun-reachable component, at the cost of longer transits and lower per-dispatch success (p_cruise^d falls with distance), plus a small supplementary fuel mass (less than 0.4% of seed mass per 10 ly). Second, the actual stellar population contains many more faint M-dwarfs and uncatalogued systems within 65 ly that serve as natural relays; routing through those would densify the effective graph and eliminate most isolated components without requiring longer hops. Third, the frontier can simply wait: as the lineage expands to stars at 30–40 ly and beyond, settled nodes at those distances will be closer to the isolated stars and can dispatch to them directly. The isolated fraction is not permanently unreachable — it is only unreachable from Earth in the early expansion; the expanding frontier eventually circumnavigates the gaps.

The catalogue ceiling of ~93% coverage in the simulation reflects this structural reality. No dispatch strategy can push coverage above the graph-connectivity limit at a given hop distance; the remaining improvement requires either a longer hop, more relay points, or more time for the frontier to reach new angles of approach.

---

## 9. The Dispatch Decision at a Settled Node

Gathering the analytical and simulation results, the complete dispatch decision for a settled node can be stated as a priority sequence:

First, identify all reachable unsettled targets within the maximum hop distance. Second, separate articulation-point targets from others (information carried in the K-packet transmitted by the origin settlement or by settled kin nodes, once the lineage-network paper's knowledge propagation is operating). Third, dispatch to articulation-point targets first, in order of the number of stars they isolate, until those targets have received at least three prior dispatch attempts or are settled. Fourth, among non-articulation-point targets, dispatch in coverage-first order: lowest prior dispatch count first, distance as tiebreaker. Fifth, cap total dispatches per target at three, redirecting additional capacity to targets with zero prior attempts.

This strategy does not require central coordination. A settled node can determine its articulation-point targets from its local graph knowledge (the catalogue positions, carried in the mission ledger since launch), count prior dispatch attempts from its lineage-network K-packets, and execute the priority sequence autonomously. The lineage-network paper's four-tier knowledge governance allows the relevant operational K — catalogue positions and dispatch histories — to propagate freely among verified kin nodes (tier 2 of the governance ladder; a classification the security paper revisits, arguing that topology information deserves explicit protection). No back-channel is required; each node applies the same rule to the same information. We state but do not simulate the articulation-point refinement; the Monte Carlo runs of §6 use plain coverage-first.

---

## 10. Discussion

**This paper is first-order and the simulation is parameterised.** The per-stage reliabilities (p_stage = 0.9 at manufacture, launch, brake, and settle) and viability weights (1.0 / 0.7 / 0.2) are the same proxies used by the computational engineering paper. The catalogue is the same 127-star curated selection. The replication time (10,000 years) and T_silence (5,000 years) are reference values from the series. Varying these parameters changes the absolute numbers — coverage timing is sensitive to tau_rep, and coverage probability is sensitive to p_stage — but the qualitative results are robust: coverage-first outperforms nearest-first because of the network's sparse geometry, not because of the specific parameter values.

**The hop-distance choice is the dominant free parameter.** More than dispatch strategy, more than offspring count, the choice of h sets the coverage ceiling. The cost of a longer hop is not braking: the stopping distance d = m/(2ρA) against ISM density ρ ≈ 3.3 × 10⁻²² kg m⁻³ (Redfield & Linsky 2008; Frisch et al. 2011; Andrews & Zubrin 1990) is independent of cruise speed and, at ~0.02 ly for the reference seed, negligible against any hop. The costs are cruise attrition and time: per-dispatch success falls as p_cruise^d (0.99 per light-year drives the §4 table), and transits lengthen by millennia, while supplementary fuel is a negligible fraction of seed mass. Moving from h = 10 ly (65% coverage) to h = 20 ly (93% coverage) is therefore bought with lower single-dispatch success and longer waits, not with sail area. Coverage-first dispatch is a strategy-level mitigation, but it cannot substitute for accepting longer hops where the graph demands them.

**The articulation-point priority rule requires knowledge of the graph.** The priority sequence of §9 requires a settled node to know which of its reachable targets are articulation points. This information must be carried in the mission-ledger K-packet from the initial dispatch — the catalogue positions from which graph structure can be computed are part of the archival stores described in the subsystem budget paper. Articulation-point calculation from 127 star positions is trivial for any digital processor, so this is a computational cost, not a capability gap. But it does presuppose that the catalogue positions carried in the initial mission ledger are accurate enough to identify the correct articulation points; astrometric error and proper-motion drift over millennia are the relevant uncertainties, and they are noted but not modelled here.

**The model ignores claiming, competition, and resource limits per node.** In the reproductive model of the computational engineering paper, every surviving settlement dispatches to its nearest targets with no limit on per-node offspring count other than n_offspring. Real settlements face resource limits: building three full seeds (~3,700 kg × 3 = ~11,100 kg of fabricated hardware) requires meaningful manufacturing time. The simulation's replication time parameter (tau_rep = 10,000 years) abstracts this into a single delay, but in practice a settlement with a large mineral-poor target environment might face tau_rep > 100,000 years and prioritise fewer dispatches to higher-value targets. These constraints are the substance of the settlement-scale energy and economics papers still outstanding in the series.

**Routing and dispatch mechanics are not values-neutral.** Which real, named stars in the catalogue are ever reached, and in what order, is set by the priority sequence of §9 and the hop-distance choice of this section — an engineering-looking outcome that is also, unavoidably, an allocation of attention across a set of distinct possible futures. The ethics paper's discussion of topology as a prior constraint on contact ethics takes up the fuller treatment: articulation points as silent gatekeepers of whole regions, the three-dispatch rule as an unexamined triage algorithm, and the absence of any channel by which discovered biosignature evidence could revise viability weighting. Left open here is that dispatch-priority and hop-distance choices are, without anyone deciding it as a matter of policy, also a determination of who waits and who is foreclosed from ever being reached.

---

## 11. Conclusion

R_eff > 1 is the condition for demographic survival; dispatch strategy determines how completely the lineage uses that demographic margin to cover the catalogue. This paper establishes three results with concrete numbers on the 127-star catalogue.

First, the catalogue is sparse at natural hop distances. At h = 10 ly, only 65% of the catalogue is reachable from the Sun; at h = 20 ly, 93%. The choice of maximum hop distance is the dominant lever on coverage, and its price is paid in cruise attrition and transit time — per-dispatch success falls as 0.99 per light-year — not in braking, which is speed-independent and negligible at these ranges.

Second, at 15–20 ly hop distances, the reachable component contains 5–9 articulation points — bottleneck nodes whose failure permanently isolates one to three dependent targets. Articulation points should receive first-priority dispatch before the general coverage plan begins.

Third, coverage-first dispatch achieves 90% catalogue coverage 62,000 years faster than nearest-first or viability-first, matching viability-first's 93% final coverage and slightly exceeding nearest-first's 91%. The gain comes from preventing dispatch concentration on nearby easy targets while distant targets go unvisited. Three independent dispatch attempts per target — the three-dispatch rule — achieve coverage probabilities of 0.90–0.95 for planet-host targets within 20 ly, consistent with the T_silence re-dispatch cadence of the lineage-network paper.

The natural design point for the lineage is three offspring per node (as established by the computational engineering paper), a ceiling of three dispatches per target (this paper), and a maximum hop distance near 20 ly (balancing coverage against cruise attrition and transit time). Coverage-first dispatch, combined with articulation-point prioritisation, is the routing policy that best exploits that design point across the sparse stellar neighbourhood.

---

## References

Andrews, D. G., & Zubrin, R. M. (1990). Magnetic sails and interstellar travel. *Journal of the British Interplanetary Society*, 43, 265–272.

Bjørk, R. (2007). Exploring the Galaxy using space probes. *International Journal of Astrobiology*, 6(2), 89–93.

Cotta, C., & Morales, Á. (2009). A computational analysis of galactic exploration with space probes: Implications for the Fermi paradox. *Journal of the British Interplanetary Society*, 62, 82–88.

Forgan, D. H., Papadogiannakis, S., & Kitching, T. (2013). Slingshot dynamics for self-replicating probes and the effect on exploration timescales. *International Journal of Astrobiology*, 12(4), 271–281.

Frisch, P. C., Redfield, S., & Slavin, J. D. (2011). The interstellar medium surrounding the Sun. *Annual Review of Astronomy and Astrophysics*, 49, 237–279.

Gaia Collaboration; Vallenari, A., et al. (2023). Gaia Data Release 3: Summary of the content and survey properties. *Astronomy & Astrophysics*, 674, A1.

Harris, T. E. (1963). *The Theory of Branching Processes.* Springer-Verlag.

Landis, G. A. (1998). The Fermi paradox: An approach based on percolation theory. *Journal of the British Interplanetary Society*, 51, 163–166.

Redfield, S., & Linsky, J. L. (2008). The structure of the local interstellar medium. IV. Dynamics, morphology, physical properties, and implications of cloud-cloud interactions. *The Astrophysical Journal*, 673, 283–314.

Reylé, C., Jardine, K., Fouqué, P., Caballero, J. A., Smart, R. L., & Sozzetti, A. (2021). The 10 parsec sample in the Gaia era. *Astronomy & Astrophysics*, 650, A201.
