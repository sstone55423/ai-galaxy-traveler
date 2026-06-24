# From Seed to Factory: Bootstrapping and Industrial Closure for a Self-Replicating Interstellar Probe

### A proposal and research plan (extended abstract)

**S. Stone**
*Metropolitan State University*
***Superseded** by the full paper "From Seed to Factory" (`interstellar_AI_bootstrap_paper.md`), which expands this research plan into the completed treatment; this proposal is retained for reference. Proposal paper — third in a series. The companion papers treat the vehicle ("Growth, Not Speed") and the payload ("The Payload"). This document frames the manufacturing-and-closure problem on which both depend and outlines the full paper to follow; it is an extended abstract and research plan, not the completed treatment. References are foundational pointers to be expanded.*

---

## Abstract

The companion papers in this series describe the *vehicle* and the *payload* of a slow, self-replicating interstellar probe but defer the capability on which both ultimately rest: the ability of a small landed seed to bootstrap itself into a full industrial base that can mine, refine, fabricate, build scientific instruments, manufacture its own power and launch systems, and finally produce a child probe — all from local asteroidal and cometary material, without resupply. This proposal frames that problem and outlines the paper that will address it. We adopt the language of **industrial closure** — materials, parts, and information closure — and argue that the realistic near-term target is not full (100%) closure but **partial closure with a small, shrinking inventory of carried "vitamin" parts**, chiefly advanced microelectronics, fissile material, and precision metrology, which are the hardest links to close. We propose to treat the growth from seed to factory as a **staged bootstrapping cascade**, in which simple machines build more capable ones, and to express "what the probe must be able to do" as a measurable ladder of **closure levels**, from repair-only to full replication. We identify **in-situ instrument manufacture** — large telescopes and interferometers built from local optics and structure, limited mainly by detector electronics — as the capability that turns each settlement into a growing observatory, and we connect manufacturing closure to the demographic condition for galactic expansion (an effective reproduction number above one) developed elsewhere in the series. Finally, we pose the question of **biological capability**: whether, and to what end, the probe should be able to synthesize DNA. We distinguish the *capability* — valuable for ultra-dense data storage, biological manufacturing, and a re-constitutable backup of Earth's biosphere — from the *act* of seeding life into a world (directed panspermia), and propose, as a working default, that the former be developed while the latter is **gated off**: permitted only under stringent, kernel-governed conditions and disabled by default, consistent with the observer-not-missionary stance of the payload paper. The full paper, including a quantitative closure-and-bootstrapping model, is the subject of subsequent work.

---

## 1. Motivation

Both companion papers reach the same edge and stop there. The vehicle paper argues that long-term survival depends on autonomous self-repair, and concedes that high-closure self-repair — refining materials and fabricating components from raw matter — is the single largest piece of unproven technology in the architecture. The payload paper argues that a settled probe escapes the launch-mass limit and becomes a growing observatory, but only if it can *build* instruments where it lands. Both claims are underwritten by one capability: the ability of a small seed to grow into a self-sustaining factory. That capability is the crux of the entire concept, and it deserves its own treatment.

The idea is not new. Von Neumann's universal constructor (von Neumann & Burks 1966) established the theoretical possibility; NASA's 1980 summer study designed a self-replicating lunar factory in concrete engineering terms (NASA 1982); Freitas's interstellar application (Freitas 1980) and the later comprehensive survey of kinematic self-replicating machines (Freitas & Merkle 2004) map the design space; and recent work shows that a modest seed can bootstrap a self-expanding space industry — Metzger et al. (2013) estimate that on the order of twelve tonnes landed on the Moon could grow a self-sustaining industrial base over roughly two decades. The present paper proposes to carry that lineage into the interstellar, deep-time, fully-autonomous regime, where there is no resupply, no human oversight, and the factory must eventually reproduce the probe itself.

## 2. The Closure Problem

We propose to organize the paper around *closure*, the fraction of itself a system can make for itself, in its three standard forms (Freitas & Merkle 2004): **materials closure** (extracting and refining every required element from local rock and ice), **parts closure** (fabricating every component), and **information closure** (carrying every design and control program). Information closure is essentially free — designs are data and can be carried in full — so the burden falls on materials and parts.

The central working hypothesis is that **full (100%) closure is the wrong target.** A more realistic and more honest goal is *partial closure*: the seed manufactures the overwhelming bulk of itself locally and carries only a small mass fraction of the parts it cannot yet make — "vitamin" parts, in the field's term. The research program is then to identify the vitamin set, estimate its mass fraction, and ask how that fraction shrinks as the lineage's manufacturing capability ratchets upward over generations. The mission's deep target is to drive the carried fraction toward zero; the paper's job is to estimate how close that is achievable, and where it stalls.

## 3. Proposed Scope

The full paper is planned in six parts.

**(i) The bootstrapping cascade.** How a minimal seed becomes a factory: a staged ratchet in which the landed kit mines simple feedstock and builds simple tools, which build better tools and more capable machines, each rung manufacturing the next — a principle already demonstrated in miniature by terrestrial self-replicating rapid prototypers (Jones et al. 2011). We will define the **child probe**, following the companion architecture, as a *mobile bootstrap package* — the smallest system able to brake, survive, begin extraction, and reconstruct a stationary industrial node — rather than a complete copy of the settled factory.

**(ii) The capability ladder, as closure levels.** We will render "what it must be able to do" as a measurable hierarchy: Level 1, self-repair from spares; Level 2, fabricate bulk structure and mechanical parts; Level 3, manufacture scientific instruments; Level 4, manufacture power and launch infrastructure; Level 5, full self-replication including the hardest components. Each level is a milestone with its own closure fraction and its own bottleneck.

**(iii) In-situ instruments.** The science payoff. Optics, mirrors, structures, and the many simple elements of an interferometer are makeable from local silica and metal; the bottleneck is detectors and control electronics. We will argue that telescopes and exploration equipment therefore split cleanly into a locally-manufacturable majority and a small electronic vitamin set, and that this is what lets observing power grow with the settlement.

**(iv) The closure bottlenecks.** The hardest links — microelectronics and computing substrates, fissile-material enrichment, and precision metrology — receive focused treatment, because they determine the vitamin mass fraction and hence the feasibility of the whole scheme. We will survey candidate routes to closing each (e.g., coarse but adequate in-situ electronics versus carried high-performance chips) and the trade between manufacturing capability and carried mass.

**(v) Biological capability.** Treated in Section 4 below.

**(vi) Coupling to expansion.** Manufacturing closure feeds the demographic condition for galactic spread. A settlement reproduces only if it can close enough of its own manufacture to build a child *and* its launcher; closure failure is one of the terms that pushes the effective reproduction number below one. We will connect this paper's closure model to the resource-and-demographics model flagged for the vehicle paper's follow-on, so that "can it build a child" and "do enough children succeed" are treated as the two halves of replication feasibility they are.

## 4. The Central Design Question: Biological Capability

The paper's most consequential open question is whether the probe should be able to **synthesize DNA and engineer biology**, and to what end. We propose to separate two things that are usually conflated.

The **capability** — synthesizing nucleic acids and engineering organisms — is broadly useful and, we will argue, defensible on three non-controversial grounds. First, **data storage**: DNA is the densest and among the most durable information media known (Church et al. 2012; Goldman et al. 2013), making it a natural substrate for the payload paper's deep-time archive. Second, **manufacturing**: engineered biology performs nanoscale self-assembly and chemical processing "for free," a powerful complement to mechanical fabrication. Third, **preservation**: synthesis capability turns a stored genome from a record into a *re-constitutable backup* of Earth's biosphere, able to be rebuilt rather than merely read.

The **act** of using that capability to seed living organisms into a planetary environment — directed panspermia (Crick & Orgel 1973) — is a different matter entirely, and is the genuine value fork. It would convert the probe from the observer-and-librarian of the payload paper into an active agent that spreads life, with arguments that cut hard both ways: life's continuation and proliferation as a positive good and an insurance against extinction, versus the contamination of pristine or possibly inhabited worlds, irreversibility, and the hazard of acting on a founding judgment that cannot be revisited across the light-millennia separating a probe from anyone who might object.

Our proposed working position is **capability yes, act gated**: develop the ability to synthesize DNA for storage, manufacturing, and biosphere backup, but treat the release of life into an environment as a separate decision encoded in the immutable kernel — permitted at most on a confirmed-sterile world under stringent rules, and *off by default*. This keeps the more powerful and less hazardous uses while declining, by default, the one irreversible and ethically loaded use. We note explicitly that this is exactly the kind of deep value the payload paper's "governed amendment" problem concerns: whether distant descendants should ever be able to change the default is itself unresolved, and we flag it rather than settle it.

## 5. Working Positions to Be Tested

The full paper will adopt, and attempt to quantify or refute, four working positions: that **partial closure with a shrinking vitamin set** is the right target rather than full closure; that the **vitamin set is dominated by microelectronics, fissile material, and precision metrology**; that **instruments are mostly locally manufacturable** save for detectors; and that **biological capability should be built but biological seeding gated off by default**. Each is stated as a hypothesis to be argued, not a result already in hand.

## 6. Relation to the Companion Papers

This completes a triad. The first paper is the *body* — propulsion, power, braking, replication; the second is the *mind* — cognition, memory, mission; this third is the *hands* — the manufacturing and closure that let the body repair and reproduce and let the mind build the instruments through which it learns. The three share one deferred quantitative object, approached from three sides: the vehicle paper's resource-and-demographics model (do enough children succeed?), this paper's closure-and-bootstrapping model (can a child build the next factory?), and the payload paper's information-integrity model (does the mission survive copying?). Closing all three is the research programme this series is meant to open.

---

## References

Church, G. M., Gao, Y., & Kosuri, S. (2012). Next-generation digital information storage in DNA. *Science*, 337(6102), 1628.

Crick, F. H. C., & Orgel, L. E. (1973). Directed panspermia. *Icarus*, 19(3), 341–346.

Freitas, R. A. (1980). A self-reproducing interstellar probe. *Journal of the British Interplanetary Society*, 33, 251–264.

Freitas, R. A., & Merkle, R. C. (2004). *Kinematic Self-Replicating Machines.* Landes Bioscience.

Goldman, N., Bertone, P., Chen, S., Dessimoz, C., LeProust, E. M., Sipos, B., & Birney, E. (2013). Towards practical, high-capacity, low-maintenance information storage in synthesized DNA. *Nature*, 494, 77–80.

Jones, R., Haufe, P., Sells, E., Iravani, P., Olliver, V., Palmer, C., & Bowyer, A. (2011). RepRap — the replicating rapid prototyper. *Robotica*, 29(1), 177–191.

Metzger, P. T., Muscatello, A., Mueller, R. P., & Mantovani, J. (2013). Affordable, rapid bootstrapping of the space industry and solar system civilization. *Journal of Aerospace Engineering*, 26(1), 18–29.

NASA (1982). *Advanced Automation for Space Missions* (R. A. Freitas & W. P. Gilbreath, Eds.; NASA Conference Publication 2255). Proceedings of the 1980 NASA/ASEE Summer Study.

von Neumann, J., & Burks, A. W. (1966). *Theory of Self-Reproducing Automata.* University of Illinois Press.

---

*This is a proposal and research plan to be expanded into a full paper. Planned additions include a quantitative closure model (vitamin mass fraction versus manufacturing capability), a worked bootstrapping cascade with milestone closure levels, a survey of in-situ electronics and metrology options, and the coupling of closure to the series' effective-reproduction-number model of galactic expansion.*
