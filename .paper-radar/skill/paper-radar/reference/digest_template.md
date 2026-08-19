# Paper Radar template

Structure for `.paper-radar/digests/YYYY-MM-DD.md`. Follow the shape, not the
wording. House style applies here too: concise, direct, no tables, plain-text
math, minimal hedging.

Length is a function of what was found. A quiet day is three lines. Never pad.

---

## The quiet-day digest (the common case)

```markdown
# Paper Radar — 2026-07-18

Swept 312 candidates across 15 papers (7 days: 2026-07-11 to 2026-07-18).
Nothing met the bar. No branch created.
```

That is the whole file. Resist the urge to list near-misses as filler — if
something is worth the author's attention it is a `consider`, and if it isn't,
it does not belong in the file at all.

---

## The normal digest

```markdown
# Paper Radar — 2026-07-18

Swept 312 candidates across 15 papers (7 days: 2026-07-11 to 2026-07-18).
**1 insertion staged**, 3 flagged for attention.

Review: `git diff main..paper-radar/2026-07-18`

## Staged

### Fermi paper — Section 4, the R_eff × D × G reframing

**Autonomous AI-Cosmoindustry and the Quiet Expansion Filter: A Threshold-Based
Resolution of the Fermi Paradox** — Author, A. (2026), arXiv:2606.xxxxx
[link](https://arxiv.org/abs/2606.xxxxx) · verified via arXiv API

Bears on: the claim that slow expansion is observationally indistinguishable
from absence.

> Inserted prose exactly as it now appears in the paper.

Reference added: Author, A. (2026). Autonomous AI-Cosmoindustry... *arXiv*.

Confidence: high.

## Flagged (no insertion proposed)

- **The Cosmological Hart-Tipler Conjecture** — Author, B. (2026), *Journal*
  [doi](https://doi.org/10.xxxx/yyyy) · verified
  Revisits the Hart/Tipler timescales the vehicle paper cites (~10⁶ yr and
  ~300 Myr). Worth reading before the next revision; no specific claim to
  attach it to yet.

## Dropped in verification

- **Some Title** — DOI 10.xxxx/zzzz did not resolve; not cited.
```

---

## Rules

- **Every item carries a resolving link** and a note of how it was verified.
- **Anything unverified is labelled unverified**, or it does not appear.
- **Quote insertions verbatim** as they appear in the paper, so the digest can
  be read instead of the diff.
- **Name the claim** each citation bears on. "Relevant to the Fermi paper" is
  not good enough — say which argument and why.
- **A PARTIAL sweep says so at the top**, and lists the unswept papers:

  ```markdown
  > **PARTIAL** — the sweep did not finish; 4 papers unswept: routing, ethics,
  > speciation, subsystem. Results below cover the other 11. Dedup state was
  > NOT updated, so nothing here is lost; the next run re-checks everything.
  ```
