# Zenodo Deposit Plan

*Working document, 2026-08-25, with an addendum of 2026-09-16 (seventeenth paper and the
September ripple) at the end. Supersedes the four-paper "frozen deposit" plan of 08-20,
which assumed a dependency ordering the citation graph does not permit.*

## The dependency finding

All sixteen papers are reviewed as of 2026-08-25. The intra-series citation graph is
**strongly cyclic**: every paper is cited by at least 4 siblings (minimum: the Fermi
paper at 4; maxima: payload 13, ethics 12, vehicle 11, lineage-network 11), and the
densest citers (ethics and lineage-network at 14 outbound each) are themselves among
the most-cited. No citation-respecting deposit order exists, and none is needed:

**Reserve all eighteen DOIs first, then deposit order becomes a readiness question,
not a dependency question.** Zenodo reserves a record's DOI at draft time, before
publication. With eighteen drafts open and eighteen DOIs reserved, every cross-reference
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
- **Wave 2 — ethics, security, roadmap, and home programme**, two to four weeks later. Both carry the newest and
  most volatile bibliographies (payload's preprints are ML-cultural and stable; security's
  eight and ethics' two are fresh enough that a few weeks materially raises the odds of
  venue upgrades), and both will then be cold after their re-scans. Security deposits
  last: newest text, largest inbound surface, most preprints.

Within a wave there is no ordering constraint. If a symbolic order is wanted for the
record, the vehicle paper goes first — it is the series' entry point.

## Community engagement (decided 2026-08-25)

- **Venice declined**: the 2nd European Interstellar Symposium (IRG/IAA, Dec 2–4 2026,
  abstracts due Sep 7) fits the series but not the author's fall schedule. No abstract.
- **Target: the 10th Interstellar Symposium, October 2027** (IRG/IAA; Atlanta/Georgia
  Tech pending confirmation — irg.space/irg-2027). Abstracts for this series typically
  open in spring; watch for the call.
- Consequence: no external deadline constrains the deposit waves. Sequencing:
  manual review (fall 2026) → deposit waves → JBIS submission → symposium abstract
  against a settled, citable series. The symposium's "original work not previously
  published" clause conventionally excludes repository preprints; confirm by a
  courtesy email to support@irg.space near the call for papers.

## Mechanics

- **DOIs**: cite the reserved (version-1) DOI in cross-references — it is permanent.
  The concept DOI (all-versions) exists only after first publish; add concept-DOI links
  on the site afterwards. Corrections after deposit go out as Zenodo new versions.
- **Series block**: extend `make_papers.py` to append a uniform "Papers in this series"
  endnote with the eighteen DOIs, rather than editing prose cross-references — the house
  style names siblings in prose ("the vehicle paper") and that should not change.
- **License**: the deferred split (CC BY 4.0 for papers, MIT for code) becomes due at
  the first deposit — Zenodo requires a license field. User decision.
- **JBIS**: before depositing whichever paper is submitted to JBIS, confirm JBIS's
  prior-posting policy. If it is restrictive, hold that one paper out of wave 1;
  everything else is unaffected.
- **Metadata**: per-paper record metadata (title, byline S. Stone with ORCID
  0000-0003-2718-6848, abstract as description, keywords, related-identifier links
  among the eighteen and to cited arXiv IDs) can be generated from the sources; upload
  itself is the user's step (API token or web UI).

## Current per-paper bibliographic exposure (arXiv-only refs / total)

- 0: bootstrapping, analytical engineering, computational engineering, governance,
  routing, speciation, subsystem budget
- 1: amendment (Talmon), lineage-network (Gomez), roadmap (Maraqten), home programme (Parisi)
- 2: vehicle (Maraqten, Parisi), DNA mission-ledger (Anđel, Nagaraj), ethics (Ezell,
  Klotz), knowledge-growth (Chen, Wang)
- 3: fermi (Curtis, Ivliev, Klotz)
- 6: payload (Bai, Li, Nijjer, Papadopoulos, Si, Zhan)
- 8: security (Gans, Li, Mao, Nagaraj, Papadopoulos, Shang, Zhan, Zou)

## Addendum 2026-09-16 — the seventeenth paper and the September ripple

- **New paper**: the roadmap paper ("Settlement Zero"), added 2026-09-15 at revision 2
  after a line-level review and a cross-paper audit against all sixteen siblings. It has
  not had the pre-deposit dual review the others had; schedule one before wave 2.
- **Wave assignment**: wave 2, with ethics and security. It is the newest text, its
  argument is entangled with both (standing to launch at S5; capture of settlement zero
  as an inside threat), and its bibliography carries one arXiv-only item (Maraqten).
- **Ripple into wave-1 papers** (all committed 09-15/16): settlement-zero wording pass
  (vehicle, subsystem, Fermi, lineage-network, knowledge-growth, payload, governance,
  DNA mission-ledger); ion-only braking density with every stopping number rescaled
  ~2.9x (vehicle, analytical engineering, computational engineering, routing, subsystem;
  engineering.py and the engineering dashboard); root-degree dispatch results (routing
  rev 3, computational engineering); pre-existing defect fixes (vehicle abstract dust
  ratio, Martin 1978 and Crawford 2011 added; Fermi settlement power restated); and the
  step-6 additions (ethics Section 2 and 20, security Section 7 and 17, governance
  E6 and Section 9). Every wave-1 paper except amendment and speciation was touched.
- **Consequences for the gates**: the cold gap resets for the touched papers from
  09-16; the pre-wave checklist gains a citation audit of the touched papers (every
  reference cited, no orphan citations, no stray LaTeX or tables) and a re-read of the
  braking passages against engineering.py's new defaults; the intra-series citation
  graph is denser (the roadmap paper is cited by twelve siblings), which changes
  nothing about the reserve-all-DOIs-first conclusion.
- **Bibliography**: two new verified references series-wide beyond the roadmap paper's
  own (Slavin & Frisch 2008 in the three braking papers; Martin 1978 and Crawford 2011
  in the vehicle paper). Preprint count is unchanged except the roadmap paper's one.

## Addendum 2026-09-17 — the eighteenth paper

- **New paper**: the home-programme paper ("Founded from Earth"), assembled from the roadmap
  paper's supply track, interstellar-object rider, and fuel budget (each reviewed there before
  moving) plus new sections on the launch platform, scouting, the comet rider, the first probes
  outward, and Earth-era governance. The new sections need their own review before wave 2.
- **Roadmap paper** returns to ~9,500 words with pointers where the material was; its later
  sections are renumbered (12 and 13), and nineteen references moved with the text.
- **Wave assignment**: wave 2, with ethics, security, and roadmap; one arXiv-only reference
  (Parisi 2026, shared with the vehicle paper).

