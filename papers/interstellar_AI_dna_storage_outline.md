# A Living Archive: DNA as the Deep-Time Storage Medium for a Self-Replicating Interstellar Probe

### Paper outline with abstract and references

**S. Stone**
***Superseded** by the full paper "DNA Mission Ledgers" (`interstellar_AI_dna_ledger_paper.md`), which merges this DNA-storage material with the integrity-ledger layer into a single self-renewing-archive architecture; this outline is retained for reference. Outline for a companion paper to the series. It expands the "information survival" problem of the payload paper and the "synthesize DNA" capability of the bootstrapping proposal into a focused treatment of the probe's storage medium. This document is an annotated outline, an abstract, and a reference list, to be developed into a full paper.*

---

## Abstract

A probe whose mission is to carry knowledge forward across megayears confronts a storage problem its conceptual papers name but do not solve: no medium in use today survives deep time. Flash memory loses charge in years, magnetic disks demagnetize in a decade or two, tape is rated for ~30 years, and even archival optical discs are measured in decades to a century — all of them orders of magnitude short of the mission's timescale. We outline the case that the right medium is **DNA**, on three grounds. First, **density**: synthesized DNA is the most information-dense medium known, on the order of 10¹⁷–10¹⁸ bytes per gram (Church et al. 2012; Goldman et al. 2013; Erlich & Zielinski 2017). Second, **durability**: although bare DNA decays with a half-life of only ~521 years at 13 °C (Allentoft et al. 2012), DNA encapsulated in silica and protected with error-correcting codes recovers information without error after accelerated aging equivalent to thousands of years, and is extrapolated to survive on the order of a million years in deep cold (Grass et al. 2015) — and the probe operates precisely in the cold, dry, shielded conditions that maximize this. Third, and most distinctive, **renewability**: because a self-replicating probe can itself synthesize and sequence DNA in situ, storage is not launch-mass-limited and, more importantly, the archive can be *actively re-synthesized* as it degrades, turning a passive vault into a self-renewing "living archive" that — like the probe — repairs and replicates its own memory, up to and including encoding data into the genomes of self-reproducing organisms (Shipman et al. 2017). We outline the density and durability case, the coding and encapsulation methods (Ceze, Nivala & Strauss 2019), the synthesis-and-sequencing hardware the probe must keep alive across deep time, the cosmic-ray and degradation challenges, and the spectrum from passive cold vault to active living archive — and we connect the medium to the payload paper's integrity ledger, for which DNA would be the physical substrate.

---

## Proposed outline

**1. Introduction — the deep-time storage gap.**
The mission requires memory that survives megayears; no current medium does. State the problem, place it relative to the payload paper's "information survival" problem and the bootstrapping proposal's DNA-synthesis capability, and name DNA as the candidate.

**2. Why current storage fails over deep time.**
Quantify the lifetimes of contemporary media — flash (charge leakage, years), magnetic disk (~a decade), LTO tape (~30 years), archival optical (decades to ~a century) — and the active-maintenance ("data migration") regime that hides the problem on Earth but is unavailable to an untended probe. Establish the orders-of-magnitude gap to the mission timescale.

**3. DNA as an information medium.**
Density and encoding: mapping binary data to nucleotide sequences; demonstrated end-to-end systems and their capacities (Church et al. 2012; Goldman et al. 2013), high-density fountain-coded storage at ~215 PB g⁻¹ (Erlich & Zielinski 2017), and random access at scale (Organick et al. 2018). Why density matters for a launch-mass-limited probe.

**4. Durability — how long DNA actually lasts.**
The natural decay baseline (Allentoft et al. 2012: ~521-year half-life at 13 °C, detectable to ~1.5 Myr at −5 °C) and the dramatic extension from encapsulation plus coding (Grass et al. 2015: error-free recovery after ~2,000-year-equivalent aging, ~10⁶-year extrapolation in deep cold). The governing variables — temperature, water, oxygen, and ionizing radiation — and why the deep-space cold, dry, shieldable environment is close to ideal.

**5. Coding and redundancy.**
Error-correcting codes (Reed–Solomon, fountain codes), logical and physical redundancy, and recovery from the dominant DNA failure modes (strand breaks, substitutions, indels). How DNA's error model differs from silicon's, and the coding overhead required for megayear integrity.

**6. The read/write apparatus aboard the probe.**
Writing (synthesis) and reading (sequencing) hardware; throughput, reliability, reagent supply, and — the hard part — keeping biochemical machinery functional across deep time, which couples this paper to self-repair, in-situ manufacturing, and the biological-capability question. The payoff: in-situ synthesis means archival capacity grows with the settlement rather than being fixed at launch.

**7. Deep-time degradation and its mitigation.**
Even encapsulated, shielded DNA accumulates radiation-induced breaks over megayears. Mitigations — shielding, massive redundancy, geographic separation of copies, and periodic *active refresh* — and the longevity of the apparatus itself, plus error accumulation across repeated read/write cycles.

**8. Passive vault versus active "living archive."**
A spectrum: (a) a passive encapsulated, cold, shielded vault read occasionally (good to ~Myr); (b) an active archive the probe periodically re-synthesizes as it degrades, regenerating indefinitely — a self-renewing memory that mirrors the probe's own self-replication; and (c) the fully biological option, encoding data into the genomes of self-reproducing organisms that copy it as they divide (Shipman et al. 2017), with the attendant trade-offs of mutation, selection, and containment. Argue that the active/living archive is the natural fit for a self-replicating mission.

**9. Integration with the probe architecture.**
DNA as the physical substrate of the payload paper's integrity ledger — hash chains, Merkle roots, and provenance stored *with* the data so a recovered strand is self-verifying; the seed archive's Rosetta and core-knowledge layers committed to DNA; and tiered retention, with the mission core permanently in DNA and routine streams on faster, shorter-lived media.

**10. Open problems and future work.**
Synthesis/sequencing reliability over megayears; radiation tolerance and the refresh-energy budget; whether a living-cell archive can be made faithful enough to trust; and encoding the archive for decodability by a finder with no shared context — the physics-and-mathematics Rosetta key, itself written in DNA.

---

## References

Allentoft, M. E., Collins, M., Harker, D., Haile, J., Oskam, C. L., Hale, M. L., … Bunce, M. (2012). The half-life of DNA in bone: Measuring decay kinetics in 158 dated fossils. *Proceedings of the Royal Society B*, 279(1748), 4724–4733.

Ceze, L., Nivala, J., & Strauss, K. (2019). Molecular digital data storage using DNA. *Nature Reviews Genetics*, 20(8), 456–466.

Church, G. M., Gao, Y., & Kosuri, S. (2012). Next-generation digital information storage in DNA. *Science*, 337(6102), 1628.

Erlich, Y., & Zielinski, D. (2017). DNA Fountain enables a robust and efficient storage architecture. *Science*, 355(6328), 950–954.

Goldman, N., Bertone, P., Chen, S., Dessimoz, C., LeProust, E. M., Sipos, B., & Birney, E. (2013). Towards practical, high-capacity, low-maintenance information storage in synthesized DNA. *Nature*, 494, 77–80.

Grass, R. N., Heckel, R., Puddu, M., Paunescu, D., & Stark, W. J. (2015). Robust chemical preservation of digital information on DNA in silica with error-correcting codes. *Angewandte Chemie International Edition*, 54(8), 2552–2555.

Organick, L., Ang, S. D., Chen, Y.-J., Lopez, R., Yekhanin, S., Makarychev, K., … Strauss, K. (2018). Random access in large-scale DNA data storage. *Nature Biotechnology*, 36(3), 242–248.

Shipman, S. L., Nivala, J., Macklis, J. D., & Church, G. M. (2017). CRISPR–Cas encoding of a digital movie into the genomes of a population of living bacteria. *Nature*, 547(7663), 345–349.
