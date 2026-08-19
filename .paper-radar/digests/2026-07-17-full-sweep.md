# Paper Radar — 2026-07-17 (full sweep)

> **Filename note.** `2026-07-17.md` was already taken by yesterday's single-paper
> verification digest, so this run wrote alongside it rather than overwriting it.
> This is the first full 15-paper sweep — it ran a day earlier than the scheduled
> 07-18 start.

Swept 357 candidates across 15 papers (7 days: 2026-07-10 to 2026-07-17).
**1 insertion staged**, 4 further cites proposed but held, 8 flagged for attention.

Delete permission was blocked on the mount, so git could not commit in place.
Staged as a patch instead of a branch:

```
git am .paper-radar/digests/2026-07-17.patch     # or: git apply --check first
```

Verified: the patch applies cleanly to a fresh clone.

## Staged

### Ethics paper — Section 3, *The Non-Identity Problem*

**Two Dogmas of Population Ethics: MacAskill's Existentially Unrestricted Form of
Longtermism and the Value of Existence** — Roberts, M. A. (2026), *Utilitas*
[doi](https://doi.org/10.1017/s0953820826100399) · verified via OpenAlex (Utilitas,
Cambridge University Press, 2026-07-13, article, open access)

Bears on: Section 3's pivot from Parfit to impersonal ethics — "Whether the galaxy is
better with or without the lineage is a question about the value of possible states of
the universe" — and the following claim that existing moral philosophy handles that
question poorly. The paper cites MacAskill (2022) approvingly in Section 16 and
attacks the astronomical-stakes style of argument in Section 15 via Gottlieb's
buck-passing critique. Roberts is a second, independent line of attack on the same
target: Gottlieb attacks what those arguments *do* rhetorically, Roberts attacks their
*premise*. The paper currently has only the first.

> The gap is live rather than merely historical. Roberts (2026) argues that the
> population-ethics mainstream has assumed rather than grounded its resolution of the
> Narveson-inspired value-of-existence controversy, and that the principles
> underwriting the existentially unrestricted longtermism of MacAskill (2022) — which
> Section 16 invokes — function as dogma rather than as an established result, leaving
> open an existentially restricted longtermism she takes to be more attractive. The
> distinction bears directly on the launch decision: that a galaxy filled with
> probe-descendants is better than one containing none is not a corollary of caring
> about the deep future but a separate and contested commitment, and the lineage's
> impersonal justification cannot borrow the first to establish the second.

Reference added: Roberts, M. A. (2026). Two dogmas of population ethics: MacAskill's
existentially unrestricted form of longtermism and the value of existence. *Utilitas*.
Advance online publication.

Confidence: high. Every clause is supported by the abstract, which was read in full.

**Two edits made to the screening agent's proposed prose**, both to avoid asserting
more than the source does: it had glossed "existentially restricted" as longtermism
"which weights the long-run future without treating the creation of new worthwhile
existence as itself a gain" — a reasonable reading of the Narveson position but not
stated in the abstract — and it had invented a figure, "a galaxy containing 10^12
probe-descendants", which is both unsourced and inconsistent with the paper's own
"quadrillions" in Section 16. Both were cut.

## Cites proposed but not staged

Four more cites cleared verification but are **medium** confidence, so per the
workflow they are reported rather than staged. All four are unrefereed single-author
or small-team arXiv preprints — the judgement to make is whether the series cites
preprints at all, which is yours, not the radar's.

- **Interference and Retention in Continual Learning** — Störk, J. (2026),
  arXiv:2607.09202 [link](https://arxiv.org/abs/2607.09202) · verified via arXiv API
  (Julius Störk, 2026-07-10)
  → **payload paper**, Section 3. A learning-theoretic argument for the immutable-core
  partition, which the paper currently motivates only from instrumental convergence
  (Omohundro, Bostrom). Störk models forgetting as interference and reports that
  disjoint task supports eliminate it structurally while overlapping supports leave an
  unavoidable distortion floor. If that holds, a core defended by penalty terms erodes
  at a floor rate no tuning removes; a core the cognitive layer cannot write to has no
  such floor. Results are stated for the frozen-feature regime — worth checking the
  scope of the "unavoidable floor" claim in the full text before it carries weight.

- **From Observation to Insight: Mechanistic World Models and the Quest for Autonomous
  Discovery** — Posner, I., Lei, A., & Schölkopf, B. (2026), arXiv:2607.12474
  [link](https://arxiv.org/abs/2607.12474) · verified via arXiv API (2026-07-14)
  → **knowledge-growth paper**, Section 2. Supports the epistemic stack's ordering of
  *Model* below *Knowledge*, which currently rests on assertion alone: "prediction
  alone does not constitute scientific discovery"; understanding depends on reusable
  explanatory mechanism. Note the reference list here is otherwise entirely published
  work (Shannon 1948, Howard 1966, Settles 2012, Schmidhuber 2007).

- **Heterogeneous Agent Cohorts for Safe Open-Ended Exploration with Runtime Constraint
  Memory** — Liu, T. (2026), arXiv:2607.11226 [link](https://arxiv.org/abs/2607.11226)
  · verified via arXiv API (Tengjiao Liu, 2026-07-13)
  → **speciation paper**, Section 8. An existence proof for the monitoring-not-
  suppression design implication: a validator enforcing hard constraints at a gateway
  while proposal generation runs free. The section currently argues this from the
  biological analogy alone, and Section 9 concedes the bimodal architecture "has no
  organismal analogue" — so biology cannot supply the support even in principle.
  Sandbox scale, N = 20, minutes not 10^5 yr. Cite as existence proof for the
  mechanism, not as evidence about rates.

- **Towards Species-Agnostic Legal Reasoning? Animal Rightsholding and the Legal
  Grammar of Moral Status** — Junqueira, R. (2026), OSF Preprints
  [doi](https://doi.org/10.31219/osf.io/zw3uq_v1) · verified via OpenAlex (Robert
  Junqueira, 2026-07-13, **preprint, no venue**)
  → **ethics paper**, Section 9. Separates moral considerability from rightsholding: a
  right requires a specified interest, a duty-bearer, a representative, a forum, a
  remedy, an evidentiary route, and a review mechanism. Section 9's functional-standing
  recommendation supplies the first; the core's design must name the rest — and the
  lineage-network paper's inter-branch protocol is the only candidate forum the series
  has, which T_silence ~500–5,000 yr may leave unavailable for millennia. Weakest
  provenance in this batch: unrefereed v1 preprint, animal law, only the structural
  point transfers.

## Flagged (no insertion proposed)

- **Making It to First: The Random Access Problem in DNA Storage** — Boruchovsky, A.,
  Elishco, O., Gabrys, R., Gruica, A., Tamo, I., & Yaakobi, E. (2026), *IEEE
  Transactions on Information Theory* [doi](https://doi.org/10.1109/tit.2026.3699871) ·
  verified via OpenAlex
  Best lead in the batch for the **DNA mission-ledger paper**. Random access is a named
  concern there — reading one record without amplifying the pool — and this is a
  top-venue treatment of exactly that. The sweep record carried no abstract, so it was
  not judged on content; if the results bound coverage depth or read cost it is likely
  a real citation. Highest-priority retrieval.

- **The Great Cosmic Silence: What Does the Fermi Paradox Tell About the Future of
  Humanity?** — Patomäki, H. (2026), *Global Policy*
  [doi](https://doi.org/10.1111/1758-5899.70214) · **verified via Crossref only** —
  404s in OpenAlex, registered 2026-07-17, too new to be indexed
  Locates the Fermi bottleneck in institutional time horizons. Likely fits the **ethics
  paper** better than the Fermi paper: its "governance" is the launching civilization's
  capacity to commit across centuries, not the lineage's G term. Conflating the two
  senses would muddy the R_eff × D × G reframing rather than support it.

- **Structural analysis of aerographite solar sail topologies** — Karlapp, J., &
  Tajmar, M. (2026), *Acta Astronautica*
  [doi](https://doi.org/10.1016/j.actaastro.2026.03.056) · verified via OpenAlex
  (2026-03-30 online; the sweep recorded the 2026-10 issue date)
  A real ultralight-sail line aimed at interstellar precursors. Caveat: the vehicle
  paper's sail is a *magnetic* sail braking against the ISM per d = m/(2ρA), not a
  photon sail, so the burden is on the full text to earn a place.

- **Comparative study of power control methods for a space nuclear electric propulsion
  system with a compact gas-cooled reactor Brayton cycle** — Ma, W., Yang, C., Zeng, Y.,
  Sun, Q., Ye, W., & Yang, X. (2026), *Energy*
  [doi](https://doi.org/10.1016/j.energy.2026.141802) · verified via OpenAlex
  The exact architecture behind the **subsystem budget paper**'s ~4 kW electric at ~28%
  conversion from ~14 kW thermal. Abstract missing, so unjudged. Worth checking two
  numbers: the Brayton loop's conversion efficiency against 28%, and any radiator or
  balance-of-plant mass against the ~11 m² / ~30 kg cruise radiator. May well be a
  MW-class study with nothing to say about a 4 kW bus.

- **Dynamic Agent Skills: A Lifecycle Survey and Taxonomy of Evolving Skill Libraries** —
  Li, Y. (2026), arXiv:2607.10113 [link](https://arxiv.org/abs/2607.10113) · verified
  via arXiv API
  Its eight-stage lifecycle maps nearly one-to-one onto the **knowledge-growth paper**'s
  operational-K acceptance criteria (sandboxed testing, rollback, quarantine-as-
  candidate, ledger provenance). LLM skill stores on human timescales.

- **Genome-wide cline analysis identifies new locus contributing to a barrier to gene
  flow across an Antirrhinum hybrid zone** — Field, D. L., Stankowski, S., Reiter, T.,
  et al. (2026), *PLoS Genetics* [doi](https://doi.org/10.1371/journal.pgen.1012173) ·
  verified via OpenAlex
  Reproductive-barrier loci clustered in seven localized genomic regions while the rest
  of the genome mixes freely — structurally the closest biological near-miss to the
  bimodal core/cognitive-layer architecture the **speciation paper** says has no
  organismal analogue. Too taxon-specific to carry a claim, but it is the counterexample
  to look at.

- **Development of automated biosensor technologies for future biological research beyond
  low Earth orbit** — Lingam, N., Shkurikhina, A., Wu, J. W., Shuman, D. M., & Santa
  Maria, S. R. (2026), *Frontiers in Space Technologies*
  [doi](https://doi.org/10.3389/frspt.2026.1877143) · verified via OpenAlex
  Flown autonomous biology payloads in deep space (BioSentinel, 95+ million km; LEIA to
  the lunar surface in 2027). An existence proof that unsupervised biology-carrying
  hardware is flyable — the precondition the capability-yes/release-no posture presumes.
  Says nothing about planetary protection or containment; likely better routed to the
  **DNA mission-ledger paper** than to governance.

- **Testing Black Holes with Interstellar Missions: II. Flyby Probes** — Fan, Y., Bambi,
  C., Gao, L., Nosirov, A., & Santangelo, A. (2026), arXiv:2607.09077
  [link](https://arxiv.org/abs/2607.09077) · verified via arXiv API
  The only realistic-constraints interstellar mission-design study in the sweep, and its
  companion Paper I assumes deceleration capability — adjacent to the **vehicle paper**'s
  braking argument. Science-return framing only; no mass, power, or closure numbers.

## Dropped in verification

None. Every identifier that reached this digest resolved. One item — Patomäki, DOI
10.1111/1758-5899.70214 — failed OpenAlex and was recovered via Crossref rather than
dropped; it is labelled above.

## Screening notes

- **Zero cites for 11 of 15 papers**, which is the design working. The candidate pool
  is deliberately high-recall and the collisions were the expected ones: "self-
  replicating" as a DNA hairpin milk assay, chemical speciation of radiometals, "Fermi"
  as the gamma-ray telescope, "von Neumann" as operator theory, "ledger" as blockchain,
  vehicle-routing problems, car radiators, "atom probe" tomography. The routing and
  computational papers returned pure noise — 18 and 4 candidates, nothing survived.
- **Several agents deviated from the missing-abstract rule and said so.** Where an
  abstract was missing but venue plus title made the domain plainly disjoint — *Acta
  Materialia* does not publish interstellar-settlement models — they ignored rather than
  parked in `consider`. That judgement looks right and is flagged here so you can
  overturn it.
- **The amendment paper's queries look mistuned.** Its 26 candidates were roughly a
  third Indonesian and European constitutional law, and the batch contained nothing on
  corrigibility, entrenchment/eternity clauses, self-amendment paradoxes, or formal
  verification of invariants under self-improvement — the four veins that would actually
  move that paper. The queries appear to retrieve on surface terms rather than concepts.
  Worth a look at `.paper-radar/queries.json`.
- **One off-list lead**, surfaced by the ethics agent during verification and not in the
  candidate set: *Precautionary Governance of Autonomous AI: Legal Personhood as
  Functional Instrument* (arXiv:2605.12505). The title is close to Section 9's own
  thesis. Not verified by this run — treat as a search suggestion, not a citation.
