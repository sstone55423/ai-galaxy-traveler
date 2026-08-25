# Zenodo Deposit Plan

*Working document, 2026-08-25. Supersedes the four-paper "frozen deposit" plan of 08-20,
which assumed a dependency ordering the citation graph does not permit.*

## The dependency finding

All sixteen papers are reviewed as of 2026-08-25. The intra-series citation graph is
**strongly cyclic**: every paper is cited by at least 4 siblings (minimum: the Fermi
paper at 4; maxima: payload 13, ethics 12, vehicle 11, lineage-network 11), and the
densest citers (ethics and lineage-network at 14 outbound each) are themselves among
the most-cited. No citation-respecting deposit order exists, and none is needed:

**Reserve all sixteen DOIs first, then deposit order becomes a readiness question,
not a dependency question.** Zenodo reserves a record's DOI at draft time, before
publication. With sixteen drafts open and sixteen DOIs reserved, every cross-reference
can carry its final DOI before any paper publishes.

## Readiness gates

- **Review** — complete for all sixteen (waves 1–4, 2026-08-18 → 08-25).
- **Deep re-scans** — security and ethics, in that order (user-directed, pending).
  Their fixes may ripple into siblings that quote them; all ripples land before
  anything publishes.
- **Bibliographic sweep** — `chase_preprints` re-run immediately before each wave.
  As of 08-25: 23 unique arXiv-only works across the series, 0 with venues yet
  (nearly all are Jul–Aug 2026). Preprint citations are not defects — astro and ML
  norms both accept them — the sweep just catches free upgrades (as Cheng et al.
  acquired KDD). arXiv journal_ref lags author updates; before the final wave,
  cross-check the two 2022 items (Bai, Ezell) against Crossref by title as well.
- **Cold gap** — nothing deposits in the same week it was substantively revised,
  and (author decision, 2026-08-25) the whole series matures for a while before any
  deposit: the radar keeps its daily sweep, findings keep being worked, and the
  waves below fire only when the author calls the maturation period done. The
  pre-wave checklist (re-scans landed ✓ 08-25, sweep re-run, checks clean) stands.

## Wave structure

- **Wave 1 — fourteen papers** (all but ethics and security): vehicle, payload,
  bootstrapping, analytical engineering, computational engineering, DNA mission-ledger,
  governance, governed-amendment, Fermi, knowledge-growth, lineage-network, subsystem
  budget, routing, speciation. Publish together, after (a) both deep re-scans have
  landed and their sibling ripples are committed, (b) fermi/speciation have had their
  cold week plus a checks-clean re-read, (c) the sweep is re-run. Publishing together
  freezes the cross-quotation surface once, coherently — the dominant defect class all
  through review was stale sibling quotes, and a trickle of deposits would mint them.
- **Wave 2 — ethics and security**, two to four weeks later. Both carry the newest and
  most volatile bibliographies (payload's preprints are ML-cultural and stable; security's
  eight and ethics' two are fresh enough that a few weeks materially raises the odds of
  venue upgrades), and both will then be cold after their re-scans. Security deposits
  last: newest text, largest inbound surface, most preprints.

Within a wave there is no ordering constraint. If a symbolic order is wanted for the
record, the vehicle paper goes first — it is the series' entry point.

## Mechanics

- **DOIs**: cite the reserved (version-1) DOI in cross-references — it is permanent.
  The concept DOI (all-versions) exists only after first publish; add concept-DOI links
  on the site afterwards. Corrections after deposit go out as Zenodo new versions.
- **Series block**: extend `make_papers.py` to append a uniform "Papers in this series"
  endnote with the sixteen DOIs, rather than editing prose cross-references — the house
  style names siblings in prose ("the vehicle paper") and that should not change.
- **License**: the deferred split (CC BY 4.0 for papers, MIT for code) becomes due at
  the first deposit — Zenodo requires a license field. User decision.
- **JBIS**: before depositing whichever paper is submitted to JBIS, confirm JBIS's
  prior-posting policy. If it is restrictive, hold that one paper out of wave 1;
  everything else is unaffected.
- **Metadata**: per-paper record metadata (title, byline S. Stone, abstract as
  description, keywords, related-identifier links among the sixteen and to cited arXiv
  IDs) can be generated from the sources; upload itself is the user's step (API token
  or web UI).

## Current per-paper bibliographic exposure (arXiv-only refs / total)

- 0: bootstrapping, analytical engineering, computational engineering, governance,
  routing, speciation, subsystem budget
- 1: amendment (Talmon), lineage-network (Gomez)
- 2: vehicle (Maraqten, Parisi), DNA mission-ledger (Anđel, Nagaraj), ethics (Ezell,
  Klotz), knowledge-growth (Chen, Wang)
- 3: fermi (Curtis, Ivliev, Klotz)
- 6: payload (Bai, Li, Nijjer, Papadopoulos, Si, Zhan)
- 8: security (Gans, Li, Mao, Nagaraj, Papadopoulos, Shang, Zhan, Zou)
