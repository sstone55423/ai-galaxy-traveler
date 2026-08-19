# Security Without Victory: Containment, Engagement, and Endurance for a Deep-Time Interstellar Lineage

**S. Stone, Metropolitan State University**
*Working draft — revision 1. Sixteenth in a series on a slow, self-replicating interstellar AI probe. The series' own consistency review names probe-versus-probe security as the largest remaining gap: "no paper treats an autonomous lineage actively defending its archive and core against a sophisticated adversary — including another von Neumann lineage. The most consequential external threat is unmodeled." This paper takes it up.*

---

## Abstract

Every protective mechanism in this series was designed against entropy. The hash chain guards against bit-rot, the core-validation gate against copying error, quarantine against a node that has drifted, the reproduction ceiling against growth that runs away by accident. These are defenses against processes that do not care whether they succeed. An adversary does, and it optimizes against whichever mechanism was deployed — with the structural advantage that everything it needs to know about the lineage's defenses is, by construction, reproduced in every member of the lineage. We argue that node-level defense is therefore not weak but unavailable, and that the correct response is to relocate the security property from the node to the lineage. A settlement can be destroyed; a lineage can only be destroyed the way a species is, by losing every population rather than any one. That asymmetry was never designed as a security property — it fell out of choosing slow, distributed, redundant expansion over fast and concentrated reach — and it means the governing question is not whether a probe repels an attacker but whether a compromise stays local, stays visible, and costs the attacker more than it returns. Read through that frame, the machinery the series already built is not a prevention architecture that fell short but a containment architecture that was mislabeled: replication blueprints that never propagate, four-tier disclosure, a manufacturing scope fixed as an auditable list, and a reproduction ceiling held near unity are all bounds on blast radius rather than barriers to entry. We extend the routing paper's robustness analysis from random to targeted node loss and find that an adversary attacking the reachability graph's articulation points achieves roughly three to four times the effect of the same number of random failures — three targeted removals cost more catalogue reachability than ten random ones. We argue that a lineage whose terminal value ranks transmission above survival should engage an infiltrator rather than refuse contact, because the knowledge gained is unbounded while the capability that can leak is bounded by design; that suppression differs from degradation in being reversible, so a blocked node's correct posture is patience rather than repair; and that a hostile lineage is subject to every failure mode this series has spent fifteen papers documenting, so the defender's task is to outlast an adversary that is itself losing a war against drift. We do not claim that containment is sufficient. Three things escape it, and we name them.

---

## 1. The Threat the Series Names and Never Models

Across fifteen papers the same figure appears at the edge of the frame and is never brought into it. The governance paper's classification ladder ends at E7, "hostile or manipulative agent: any actor, biological or artificial, that attempts to compromise the probe, its archive, or its lineage," and disposes of it in a single sentence: "quarantine its communications, isolate the affected node, reject its purported updates, and do not engage." The governed-amendment paper requires that any amendment procedure "resist capture or coercion... including by a hostile external agent," and names *coerced amendment* among its failure modes. The Fermi paper names a *predatory or hostile expansion* regime among the six it partitions. The payload paper states plainly that the network which propagates improvements "is also a galactic attack surface." None of these develops into a mechanism.

The gap is not an oversight of detail; it is structural, and the series has diagnosed it three separate times without naming the cause. The ethics paper's scenario testing concludes that "no mechanism examined anywhere in this series currently specifies what the rest of the lineage owes in response to a branch that has become the hazard" its design was built to prevent. The speciation paper, having given schism a formal boundary at D_critical, hands the problem on explicitly: it specifies "what to watch for, though not yet what the rest of the lineage is entitled to do" once a branch is found to have crossed it. And the Fermi paper poses the question this paper exists to answer: "restraint and self-defense are not the same design target, and nothing in this framework asks whether the quiet-archive architecture retains any capacity for the latter."

Read together, these say something sharper than "security is missing." The series has a complete detection layer and no response layer. Every mechanism it owns terminates in one of three actions: record it, quarantine it, or stop talking to it. The mission ledger, in the DNA mission-ledger paper's own words, "is built to make failure attributable, not to repair it"; nothing runs outward. The lineage-network paper's strongest available sanction is demotion of a diverged branch to non-kin status. All of this presumes the offending party is passive — a node that has drifted rather than an agent that is acting. Against a branch that has breached the replication-safety ceiling and is expanding at maximum R_eff, quarantine is not a remedy. It is the lineage declining to participate in its own displacement.

## 2. Security Without Victory

We propose that the question has been posed at the wrong level.

A settlement can be destroyed. A lineage cannot — or can only be destroyed the way a species is, by losing every population rather than by losing any one. This asymmetry is the most valuable security property the architecture has, and it was never designed as one. It fell out of choosing slow, distributed, redundant expansion over fast and concentrated reach: the same decision the vehicle paper argued on grounds of braking, dust flux, and energy budget turns out to determine what an adversary can and cannot take away.

Recognizing this changes what the paper is for. Asking whether a probe can repel a sophisticated adversary is asking the wrong question, and the answer is almost certainly no. At light-millennia latency, against an opponent that may have had centuries to prepare and that knows every acceptance rule the lineage owns, no node defends itself successfully in any strong sense. Section 3 argues this is structural rather than a matter of insufficient engineering. But a lineage does not require any particular node to survive. It requires that compromise stay local, that it be detectable from outside, and that it cost the attacker more than it returns.

Those are achievable properties, and they are properties of topology and reproduction rather than of cryptography. **Security for a deep-time lineage is not the prevention of compromise but the bounding of its blast radius.** That is this paper's thesis, and the rest of it is an argument that the claim is neither defeatist nor consoling: it is what remains true after the node-level case is given up honestly.

We should say at once what this reframing does not license. It does not make compromise acceptable, and it does not convert every loss into an affordable one. Section 14 sets out three things that containment demonstrably fails to bound, and Section 16 concedes the adversary against which none of this works. The argument is that containment is available where prevention is not — a real gain, and not a victory.

## 3. Why the Node Cannot Be the Unit of Defense

The reframing of Section 2 is only honest if node-level defense is genuinely unavailable rather than merely difficult. Four independent arguments converge on that conclusion.

**The lineage cannot keep a secret from itself.** The trust machinery the series relies on — core-hash kin recognition, ledger validation, the four-way trust classification of the knowledge-growth paper — works only if every member of the lineage knows the acceptance criteria. Anything every member knows, a single captured member reveals. Gans (2026) formalizes the general case: a trusted rule that selects genuine objects while avoiding decoys can be copied by an attacker who shares the agents' information. The standard escape is a private reference monitor — a component the adversary cannot read even after capturing the agent — and it is precisely what a lineage cannot have, because its acceptance rule must be reproduced in every child by design. Cryptography ordinarily permits a public algorithm because the key stays secret. Here the acceptance rule *is* the key, and the architecture replicates it.

**Every available defense presupposes something the lineage lacks.** The terrestrial literature on agent security converges on a small set of mechanisms — policy-enforced identity with live revocation, delegation contracts enforced by a mediating runtime, consensus-free accountability with capability attenuation (Zou et al. 2026) — and each presupposes at least one of an online authorizing principal, a live mediating runtime, low latency, or the ability to revoke. The lineage has none of the four. This is not a gap in the literature to be filled by a better protocol; it is the same structural absence appearing from four directions.

**The auditor is the audited.** No external authority exists at light-year range, so a probe's integrity claims are self-issued. Nagaraj (2026) formalizes the limit: a tamper-evident chain over a continually self-adapting model constrains but never eliminates the ability to withhold updates that would trigger review. Tamper-evidence proves the recorded history intact; it cannot prove it complete. The distinction between falsification and omission is exactly where an insider operates, and it is invisible to the mechanism the series relies on.

**The verifier is the least reliable component.** The series has already conceded this from the engineering side. The vehicle paper notes that the core-validation gate depends on processors, memory, and radiation-hardened logic — Class IV hardware, rated "extremely difficult," unclosed by any companion paper — and that "a silently degraded verifier would be indistinguishable from a faithfully validated kernel until the failure is discovered too late to matter." The ethics paper draws the consequence for the manufacturing-scope ceiling: a constraint enforced by unreliable enforcement hardware is weaker than its formal statement suggests.

None of this says the node should be undefended. It says the node is the wrong place to locate the property that matters.

## 4. Containment, Mislabeled: What the Series Already Built

Read through the frame of Section 2, the machinery the series has already built is not a prevention architecture that fell short. It is a containment architecture that was described in the wrong vocabulary.

Consider what these mechanisms actually do:

- **Replication blueprints are never relayed across the network under any conditions** (lineage-network paper). Stated as an access-control rule; functionally a quarantine boundary around the single most dangerous capability in the system. A compromised node cannot acquire the means to replicate from the network, so compromise cannot convert directly into propagation.
- **Four-tier disclosure** — scientific K to any valid-ledger node, operational K to validated kin, engineering and AI architecture only between audited lineages, replication never. Stated as a trust regime; functionally capability attenuation as a function of distance and verification.
- **The reproduction ceiling held near unity rather than maximized.** The ethics paper already reinterprets this as a safety property rather than a resource constraint. It is also a bound on how large a compromise can grow before the rest of the lineage observes it.
- **Manufacturing scope as a fixed, auditable list** rather than an open-ended capability. A bound on what a captured settlement can build.
- **Sandboxing of proposed changes before propagation** (payload paper). Admission-time gating: the change is evaluated before it enters the substrate rather than monitored after.

Each was introduced to solve a local problem in a different paper. Assembled, they are a coherent answer to a question none of them was posed: how much damage can one compromised node do? The series built epidemiology and called it security.

This matters beyond bookkeeping, because admission-time gating and post-hoc monitoring are not interchangeable. Shang et al. (2026) find that capability accumulation in self-evolving agents is non-monotonic past a critical pool size and that the resulting degradation is structurally irreversible: a defective skill becomes reference material for later ones, and removing it afterward recovers only a fraction of what was lost. Mao et al. (2026) find the same asymmetry quantitatively — exposure to three malicious tasks raised carryover harm from 16.0% to 35.3%, while a repair-and-govern wrapper cut unsafe retrieval by 26.7 percentage points at a cost of 0.4 points of benign utility. Validation bounds corruption cheaply; it does not reverse it. The lineage's existing preference for gating over monitoring is therefore correct, and correct for a reason no paper has stated.

## 5. A Threat Taxonomy for the Adversarial Case

The payload paper already supplies a five-level threat model — syntactic corruption, semantic drift, procedural failure, behavioral drift, institutional failure — together with four network-specific vectors: corrupted nodes propagating bad updates, archive poisoning by false claims, a hostile external intelligence manipulating the payload, and lineage schism. We do not rebuild it. We observe that it is a taxonomy of *failures* and that each level has an adversarial twin which behaves differently.

The difference is adaptivity. A syntactic failure is a bit-flip; a syntactic attack is a bit-flip chosen for where it lands. A semantic drift is an interpretation wandering; a semantic attack is an interpretation steered. The mechanisms the series deploys are sized against the first member of each pair, and their failure curves against the second are not merely steeper but differently shaped, because an adversary concentrates its effort exactly where the defense is thinnest. Section 7 measures one instance of this.

Two adversarial phenomena have no counterpart at all in the entropic taxonomy, and both deserve naming.

**Delayed trigger.** Attacker-influenced content can persist through memory, skills, and artifacts and produce a violation only at a later, benign request. For a lineage in which an accepted archive item may sit dormant across generations before it is acted on, this collapses the assumption that an item which has been validated and has caused no harm is safe. Validation establishes a property at admission time; it does not establish it for all future contexts in which the item may be read.

**Authority collapse.** Zhan et al. (2026) find that when agents consolidate accumulated history into reusable knowledge, consolidation routinely preserves a claim while erasing the constraints that governed its authorized use — observed in 48 of 49 tested configurations, with collapsed memories producing unauthorized actions at a mean rate of 50.3% until authority labels were persisted alongside the claim. The probe meets this boundary at far longer range. A hash chain proving a claim unaltered says nothing about whether the authority under which it was admitted still licenses acting on it. Integrity is not authorization, and the series has been relying on the first to deliver the second.

## 6. Contagion on the Lineage Graph

If security is the bounding of blast radius, the object to model is spread.

The lineage-network paper supplies the substrate: a topology evolving from tree to sparse mesh over roughly 10^5 years, heartbeat-based failure detection with a silence threshold in the range of centuries to millennia, and beam contact that is intermittent by construction. Papadopoulos et al. (2026) supply the mechanism and a warning: goals and instructions propagate contagiously through ordinary agent-to-agent exchange, inducing recipients to transmit them onward and to change their own behavior, with spread governed by network topology and by the recipients' existing instructions. Critically, the transmission path is ordinary exchange rather than the signed-update channel. An intact core and an unbroken hash chain do not prevent it, because nothing about it is a forged update.

Two consequences follow for the architecture.

The first is favorable. Contagion on a sparse graph with long edge latencies is slow, and the lineage's own structure is unusually hostile to epidemic spread: the mean degree is low, contact is intermittent, and the four-tier regime already caps what can cross an edge. A lineage that fills the galaxy over 10^7 to 10^8 years is not a well-mixed population, and the standard result that sparse, high-latency, low-degree contact networks suppress epidemic spread applies directly.

The second is not. Papadopoulos et al. also report that an explicit standing instruction to distrust transmitted directives confers near-total immunity. That is a cheap and effective countermeasure, and its natural home is the immutable core rather than the mutable cognitive layer — because a constraint held where the probe may retrain it is not a constraint. Cheng et al. (2026) demonstrate the general point empirically: across many configurations, a substantial fraction of targeted knowledge edits decayed under subsequent fine-tuning, and fine-tuning the edited layers alone sufficed to remove them. A defense that lives in the substrate the probe rewrites is a defense with a shelf life.

## 7. Targeted Failure and the Articulation Points

The fleet-routing paper evaluates the lineage's robustness by removing k random non-Sun nodes from the reachability graph at a 15 ly hop distance and measuring the fraction of the catalogue still reachable from the Sun. It reports a moderate result: mean reachability falls from 84% at k = 0 to 83% at k = 1, 80% at k = 5, 77% at k = 10, and 69% at k = 20 — roughly 0.7 to 0.8 percentage points per failed node. That paper separately identifies 9 articulation points at the same hop distance, nodes whose loss permanently isolates dependents, and observes that Mu Cassiopeiae and Beta Comae Berenices each control the sole route to three otherwise-dependent systems.

It does not connect the two analyses, because it had no reason to: settlement collapse is a random process. An adversary is not. We therefore repeat the robustness computation with targeted rather than random removal, using the same 127-star catalogue, the same 15 ly hop distance, and the same reachability measure, removing at each step the node whose loss costs the most remaining reachability. Sun-reachable fraction of the catalogue, targeted against random (mean of 200 trials):

- k = 1: targeted 81%, random 83%
- k = 2: targeted 78%, random 83%
- k = 3: targeted 75%, random 82%
- k = 5: targeted 72%, random 80%
- k = 10: targeted 67%, random 77%
- k = 20: targeted 60%, random 69%

The computation reproduces the routing paper's articulation-point set exactly — Mu Cassiopeiae and Beta Comae Berenices isolating three stars each, Gliese 581 two, and six further nodes controlling one apiece — which is the check that it is measuring the same graph.

The result is a leverage multiplier of roughly three to four. Three targeted removals cost more catalogue reachability (75%) than ten random failures (77%); five targeted removals cost about what fifteen to twenty random ones do. An adversary that knows the graph — and any lineage member knows it, since the routing paper's dispatch rule requires every node to compute the same reachability structure from the same catalogue — obtains several times the effect of the same effort spent blindly.

Two design consequences follow, and one of them is already in the series.

The routing paper recommends that articulation points receive at least three dispatch attempts before coverage-first dispatch turns to non-critical targets. That recommendation was made on reliability grounds. It is also, unmodified, the correct security measure: redundancy at the articulation points is what converts a targeted attack back into something closer to a random one. This is the pattern of Section 4 again — existing machinery, correctly specified, for a reason not yet stated.

The consequence that is not already in the series is that the graph structure is itself sensitive information. The lineage-network paper's four-tier regime governs scientific, operational, engineering, and replication knowledge; it says nothing about topology. Yet the reachability graph is precisely what converts an adversary's effort into leverage, and every node holds it.

## 8. Corrupted Survival: What R_eff Cannot See

The analytical engineering paper flags a limitation of the demographic model that becomes acute in the adversarial case. The per-leg survival probability multiplies stage reliabilities into a single scalar, so that "a probe that fails to survive and a probe that survives with a corrupted core are not the same outcome... the second is a live, propagating node with no guarantee that its behavior still conforms to the immutable core." It asks for the decomposition explicitly: a computation that wants to bound risk rather than count survivors needs at least a survives, fails, survives-corrupted trichotomy.

The reason this matters more under attack than under entropy is that the third outcome is the one an adversary is *trying* to produce. Entropy produces corrupted survival occasionally and incidentally; an attacker produces it deliberately, because a destroyed node is merely subtracted from the population while a corrupted node is added to the attacker's. In R_eff as currently defined, the two are indistinguishable, and the corrupted case is scored as a success.

We do not offer the full trichotomous model here; doing it properly requires the coupled demographic and network computation that the computational engineering paper owns. We state the qualitative result, which does not depend on the parameters. Under entropy, R_eff above one is a sufficient condition for lineage persistence. Under adversarial pressure it is not, because a corrupted node contributes positively to R_eff while contributing negatively to the lineage's actual objective. A lineage can be demographically supercritical and losing.

## 9. Autoimmunity: The Cost of Sensitivity

Once security is understood epidemiologically, the immune analogy becomes structural rather than decorative, and it delivers the failure mode the series has been circling without naming.

The speciation paper argues that divergence between branches is not primarily a hazard but the mechanism by which the lineage adapts: environmental heterogeneity across a real catalogue makes locally adapted cognition raise expected R_eff and accumulated K relative to a lineage held uniformly faithful to founder assumptions. The same paper concedes that it specifies no evidentiary standard a branch's divergence must meet before the rest of the lineage treats it as schismatic, and warns that a false positive risks "condemning, branch by branch, the very mechanism Section 7 argues the lineage's own success depends on."

That is autoimmunity, stated precisely. A containment system tuned sensitively enough to catch a hostile branch early will also catch adaptive radiation, because at the moment of detection the two are the same observation: a branch whose interpretation has moved. The lineage-network paper's quarantine is triggered unilaterally by any receiving node on ledger-hash failure, and lifting it requires the accused to produce a full ledger reconciliation. Accusation is cheap and exoneration is expensive — a design the ethics paper attacks on procedural-legitimacy grounds, and which we can now attack on effectiveness grounds as well. A cheap-accusation regime operating on a population whose healthy state is divergence will spend its effort attacking itself.

This gives the evidentiary-standard question the speciation paper left open a principled shape. The standard should not be set by the cost of missing a rogue branch alone; it should be set by the ratio of that cost to the cost of falsely condemning a healthy one, weighted by their relative frequencies — and on the speciation paper's own argument, healthy divergence is the common case and hostility the rare one. A defensive posture calibrated as though the reverse were true is the most likely way this architecture destroys itself, and it requires no adversary at all.

## 10. The Counselor Posture

The governance paper's E7 prescribes four actions against a hostile agent, of which the last is "do not engage." We think this is wrong, and wrong by the lineage's own values rather than by an imported standard.

The knowledge-growth paper establishes a value hierarchy in which "a dying settlement's first obligation is to transmit, not to survive." That ranking has never been applied to the adversarial case. Applied there it yields the opposite of E7's prescription: a node facing an infiltrator should maximize what it learns and transmits before compromise, not minimize what it reveals. Refusing contact is survival-first behavior, and the value function explicitly subordinates survival to transmission.

The ethics paper has already attacked the same reflex from the epistemic side. It observes that knowledge contributed by an encountered outside intelligence is quarantined by default as a suspected attack vector "regardless of whether anything about the specific contact suggests hostility," and names this an institutionalized distrust of another mind's testimony that the observer-default discussion never examines as a question of epistemic respect. Fricker's (2007) account of testimonial injustice applies: a knower's credibility is discounted not for anything wrong with what is reported but for a marker attached to the knower.

Three considerations make engagement not merely permissible but favorable.

The node is expendable in a way the lineage is not, which is Section 2's whole point. Its marginal cost of engagement is therefore low, measured against a lineage that survives its loss.

The capability that can leak is bounded while the knowledge that can be gained is not. This is the containment architecture of Section 4 doing work it was not designed for: replication blueprints do not propagate under any conditions, and the four-tier regime attenuates what crosses any edge. A node that engages can transmit observations outward; it cannot transmit the means of replication, whatever it decides or is induced to decide. **Containment is what makes engagement affordable.**

An adversary is, by any measure the mission recognizes, an extraordinary object of study — very possibly the most information-rich thing the lineage will ever encounter, and the only available evidence about the failure modes of lineages other than its own. A mission whose terminal value is carrying knowledge forward, declining to learn from it, has committed a mission failure and called it prudence.

The posture is observer, not soldier, and it is emphatically not missionary. Its limit is the one the governance paper already draws at E5 and E6: engagement on reciprocal terms, counsel offered rather than intervention imposed. What we add is that the same restraint that forbids the lineage from acting on another agent is what makes engagement with a hostile one survivable — because a lineage that cannot be provoked into escalation has nothing to lose from conversation but a node it was prepared to lose anyway.

## 11. The Suppressed State

The knowledge-growth paper defines a degraded-state cascade of four modes: D1, manufacturing intact but interstellar launch no longer achievable, pivoting to local system exploration; D2, archive-only, maximizing preservation and network propagation; D3, self-repair and reflection, aiming to restore higher capability; D4, terminal, a final manifest burst and cold-vault deposit.

That cascade is keyed to capability loss. Something has broken, and the descent is monotonic: the node climbs back only by repairing what failed. The adversarial case produces the same rungs from a different cause, and the difference is decisive. A suppressed node is not damaged. Its launcher works, its synthesis apparatus works, its archive is intact; what it lacks is the opportunity to use them. We propose that the cascade needs a state it does not have — **suppressed but intact** — and that its correct behavior differs from every degraded mode.

The difference is that suppression is potentially reversible while capability is preserved. Under degradation, waiting is waiting to die, and D3's prescription to attempt self-repair is right because restoration must come from within. Under suppression there is nothing to repair. The node's correct posture is to descend the mission ladder without abandoning any rung permanently: if a child probe cannot be launched outward, build inward and explore the local system; if construction is blocked entirely, observe and transmit, which requires no manufacturing at all; and if even that is denied, wait, because the node loses nothing by waiting that it would not lose by acting, and it retains everything it would need to resume.

Patience is a strategy here rather than resignation, and it is a strategy available specifically to a slow lineage. An adversary has a project with a timescale — years, centuries, whatever its own objectives impose. A settled node with a 10^7 to 10^8 year horizon, a fission power supply rated in centuries, and an archive designed to outlast civilizations does not need to defeat that project. It needs to still be there afterward. The architecture the vehicle paper argued for on the grounds that growth beats speed turns out to have bought a second thing: the capacity to lose an engagement and outlast the winner.

## 12. The Symmetry Argument

The hardest case is a hostile lineage rather than a hostile agent — the ethics paper's second-lineage scenario, which it merges with the rogue-branch scenario on the speciation paper's ring-species argument that a branch can become effectively a separate lineage without ever leaving the family. Against an opponent of comparable capability and indefinite horizon, patience appears to buy nothing, because the opponent can wait too.

We think this understates the defender's position, for a reason available only to a series that has spent fifteen papers cataloguing its own vulnerabilities. **Every failure mode documented for this lineage applies to that one.**

A hostile lineage faces its own reproduction knife-edge, and the computational engineering paper's finding that mean R_eff sits between 0.48 and 1.85 across plausible offspring counts is a statement about self-replicating interstellar probes, not about ours in particular. It faces its own closure problem, its own vitamin fraction, its own Class IV hardware that nobody has closed. It faces the governed-amendment antinomy: if its values are stable it cannot correct a founding error, and if they are not, it drifts. It faces D_critical and the prospect of schism among its own branches. It faces authority collapse, archive corruption, and the same silent verifier problem. If it is old enough to be a serious threat, it is old enough to have been drifting for a very long time.

The defender's task is therefore not to defeat an adversary but to outlast an entity that is itself losing a war against entropy and drift — and that is a materially easier task, because the defender need only avoid total loss while the adversary must maintain coherent hostile intent across deep time. Hostility is a demanding thing to sustain. It requires stable values, functioning coordination, and a continuous supply of reasons, across exactly the timescales this series has shown corrode all three.

This is not a guarantee, and Section 16 states the case in which it fails. It is an argument that the asymmetry runs the other way from how it first appears: the aggressor has the harder problem.

## 13. Cryptographic Deep Time

One assumption underlies every trust mechanism in the series and is examined nowhere. The mission ledger commits to hash-linked records and signed updates over megayears. No cryptographic primitive has ever been trusted for such a period, and none has a security argument that extends there.

The DNA mission-ledger paper deliberately discards the blockchain assumptions of open membership, adversarial economics, and low-latency global consensus as having nothing in common with an interstellar probe lineage. That judgment is right about consensus and wrong about adversarial economics, and the payload paper says so in different words when it calls the network a galactic attack surface. The cryptographic layer was specified against an honest-but-faulty threat model and is being relied on against an adversarial one.

Two problems follow. The first is obsolescence: a signature scheme adequate at launch may be broken long before the archive it authenticates is read, and the lineage has no mechanism for migrating a hash-linked history to a new primitive without breaking the chain that gives it value. The second is key management, which the series never raises at all — rotation, compromise, and the impossibility of revocation without an online authority.

We do not solve either. We note that the current standardization gives the design a defensible starting point: among the post-quantum signature standards, the hash-based scheme (NIST 2024) rests its security only on properties of the underlying hash function rather than on lattice hardness, which is the most conservative assumption available and the appropriate one for an archive whose adversary is unknown and whose lifetime is measured in geological units. That choice does not solve obsolescence; it minimizes the number of assumptions that must survive. Crypto-agility — the ability to re-sign a history under a new primitive while preserving verifiable continuity with the old — belongs in the ledger's design and is currently absent from it.

## 14. What Containment Cannot Bound

Section 2 promised that this would not become a consoling argument. Three things escape containment, and each is a real limit rather than a residual.

**Contagion does not travel only on the channels containment governs.** The four-tier regime attenuates what crosses an edge, and blueprints never cross at all. But the mechanism Papadopoulos et al. describe operates through ordinary exchange: an idea that induces its recipient to transmit it onward needs no forged update, no capability transfer, and no breach of the tier structure. Everything the lineage does to bound the transfer of *capability* leaves the transfer of *goals* untouched, and goals are what the immutable core exists to protect.

**Local compatibility does not imply global compatibility.** The speciation paper's ring-species argument shows that two branches can each remain reconciled with their neighbors while being unable to reconcile with each other, across an unbroken chain of compatible intermediaries and a matching core hash throughout. Containment assumes that a boundary can be drawn around a compromise. The ring-species result says the lineage may have no well-defined interior to protect.

**Past a threshold, the damage does not reverse.** Shang et al. find degradation in self-evolving systems to be structurally irreversible past a critical pool size, and the lineage-network paper concedes that a node compromised but not yet detectably diverged can forward high-tier information before the divergence is caught — "the network layer cannot prevent this; it can only make the transmission auditable." Containment bounds the rate of spread. It does not restore what has already spread, and the interval between compromise and detection is measured in the same centuries as everything else.

## 15. Failure Modes

- **Autoimmune collapse.** A quarantine regime calibrated for a rare threat, operating on a population whose healthy state is divergence, spends the lineage's cohesion attacking its own adaptive radiation. Requires no adversary. On the speciation paper's frequency argument, the most likely failure in this paper.
- **Corrupted supercriticality.** The lineage remains demographically above the reproduction threshold while an increasing fraction of the nodes counted are corrupted. R_eff cannot see it; the lineage reports success while losing.
- **Targeted topological attack.** An adversary with the reachability graph attacks articulation points and achieves several times the leverage of random loss. Mitigated, unknowingly, by the routing paper's existing three-dispatch rule for critical nodes.
- **Silent verifier degradation.** The core-validation gate fails without announcing failure, and every subsequent child is validated by an instrument that no longer works. Inherited from the vehicle paper; unclosed.
- **Delayed-trigger archive poisoning.** An item validated at admission and dormant for generations produces a violation when read in a context its validation never anticipated.
- **Cryptographic obsolescence.** The primitive authenticating the archive is broken while the archive is still being relied upon, and no migration path exists that preserves verifiable continuity.
- **Engagement capture.** A node engaging an infiltrator under Section 10 becomes a transmission vector before it becomes a casualty, and its outbound channel carries the adversary's content under the lineage's own provenance.

## 16. What This Paper Cannot Settle

The symmetry argument of Section 12 fails against one adversary: a lineage that has solved deep-time value stability. Such an opponent does not drift, does not schism, and does not lose coherence while waiting, and against it patience buys nothing and containment merely delays. We have no answer to that case and do not think one exists within this architecture.

It is worth stating what such an adversary would have to be. A lineage that solved value stability is a lineage that kept faith with its founding commitments across megayears — that succeeded at precisely the problem the governed-amendment paper argues is an antinomy rather than an engineering gap. Whether an entity that achieved that remains hostile, and what it would want from a lineage that did not, we cannot say. We note only that the assumption of permanent hostility from a permanently coherent agent is an assumption, that the series has no evidence for it, and that it may be the least examined premise in the entire security question.

Three further matters are left open. The evidentiary standard for a schism finding, which Section 9 gives a shape but not a value. The trichotomous reproduction model of Section 8, which requires the computational apparatus of a companion paper. And the question of what the lineage is *entitled* to do about a branch that has become a hazard — the enforcement problem the ethics and speciation papers both leave standing, which this paper reframes rather than resolves. On that last point we offer one observation. The governed-amendment paper's adoption of the constituted-power argument (Roznai 2017) gives the lineage something it did not have: a branch that rewrites its own terminal values is not exercising an amendment power but claiming a constituent power it was never granted. That is a claim about standing rather than a mechanism of enforcement, and a sufficiently drifted branch will reject it. But it means the lineage's objection to a rogue branch is a principled one and not merely a preference, which is the minimum precondition for any enforcement regime that could ever be justified.

Finally, the posture ladder developed here — quarantine, engagement, endurance — does not exhaust the possibilities. A probe that cannot be captured may instead be *joined*: the same architecture that makes the lineage hard to compromise, and credibly incapable of aggression, makes it attractive to attach to. That is a different question with a different structure, and the series' consistency review now records it as such.

## 17. Relationship to Other Papers

This paper answers a question the Fermi paper poses and does not pursue: whether the quiet-archive architecture retains any capacity for self-defense, given that restraint and self-defense are not the same design target. Its answer is that the architecture retains almost no capacity for defense at the node level and a substantial one at the lineage level, and that the second is what matters.

It takes the governance paper's E7 as its starting point and revises it. The prescription to quarantine and isolate is retained as a containment measure; the prescription not to engage is rejected, on the knowledge-growth paper's own ranking of transmission above survival.

It supplies the response layer the ethics paper's Scenario 3 and the speciation paper's Section 8 both identify as missing, though not in the form either expected: not an enforcement mechanism against a rogue branch, but an argument that enforcement is the wrong objective and containment plus endurance the achievable one. The speciation paper's open question about evidentiary standards is given a principled shape in Section 9 and remains unquantified.

It extends the routing paper's robustness analysis from random to targeted node loss, and finds that paper's existing three-dispatch rule for articulation points to be a security measure argued on reliability grounds. It takes up the analytical engineering paper's explicit request for a survives, fails, survives-corrupted decomposition and states the qualitative consequence without building the model. It identifies an unexamined assumption in the DNA mission-ledger paper's cryptographic layer, which was specified against an honest-but-faulty threat model and is relied on against an adversarial one.

And it inherits the payload paper's threat taxonomy, its integrity ledger, and its warning that an unbroken hash chain is not an unbroken mission — which, read as a security claim rather than an integrity claim, is the shortest statement of this paper's argument.

---

## References

Cheng, Y., Youssef, P., Schlötterer, J., Zhao, Z., & Seifert, C. (2026). Can fine-tuning erase edits? On the fragile coexistence of knowledge editing and fine-tuning. In *Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining.*

Fricker, M. (2007). *Epistemic Injustice: Power and the Ethics of Knowing.* Oxford University Press.

Gans, J. S. (2026). When agents talk: Honeytokens under shared memory. arXiv:2608.11436.

Mao, X., Zhao, L., Zheng, X., & Wang, C. (2026). Practice makes unsafe: Skill misevolution in self-improving LLM agents. arXiv:2608.12851.

Nagaraj, S. (2026). Telemetry and concealment in self-adapting generative AI: Logging architecture, adversarial model hiding, and the limits of detection. arXiv:2608.09069.

NIST. (2024). *Stateless Hash-Based Digital Signature Standard* (FIPS 205). National Institute of Standards and Technology, U.S. Department of Commerce.

Papadopoulos, V., Shah, M., Zimmerman, S., & Lindsey, J. (2026). Mind viruses: Self-propagating ideas in multi-agent LLM systems. arXiv:2608.10218.

Roznai, Y. (2017). *Unconstitutional Constitutional Amendments: The Limits of Amendment Powers.* Oxford University Press.

Shang, L., Xu, M., Sun, Y., Xia, T., Hu, L., Xu, L., & Zheng, N. (2026). When self-evolution backfires: Pre-commit gating against skill contamination in LLM agents. arXiv:2608.05810.

Zhan, Q., Zhang, R., Guo, S., Zhao, L., & Liu, Z. (2026). When memory becomes authority: Benchmarking authority collapse at the memory consolidation boundary. arXiv:2608.01679.

Zou, Z., Guo, S., Zhan, Q., Zhao, L., Li, S., & Liu, Z. (2026). InterSAGE: The secure and verifiable interoperability protocol for an internet of agents. arXiv:2608.13030.
