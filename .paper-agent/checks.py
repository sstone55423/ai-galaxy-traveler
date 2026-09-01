#!/usr/bin/env python3
"""Deterministic consistency checks for the interstellar-AI paper series.

Zero-dependency, stdlib-only, so these run offline and give reproducible
findings. The LangChain agent in guardian.py wraps each of these as a tool and
adds the semantic layer (cross-reference resolution, number-in-context
judgment) on top.

Run standalone:
    python .paper-agent/checks.py papers/interstellar_AI_fermi_paper.md
    python .paper-agent/checks.py --all        # every paper in papers/

Each finding is a dict: {check, severity, line, message}. severity is one of
"high" (a house-rule violation), "medium" (probable, verify), "low" (FYI).
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path


def sortkey(name: str) -> str:
    """Collation key for a surname.

    Reference lists alphabetize by base letter, so "Ćirković" files under C-i
    and correctly precedes "Crawford". Comparing raw code points does the
    opposite ('ć' U+0107 > 'c'), which produced a false ordering complaint on
    the Fermi paper's list. Strip combining marks before comparing.
    """
    decomposed = unicodedata.normalize("NFKD", name.lower())
    return "".join(c for c in decomposed if not unicodedata.combining(c))

REPO = Path(__file__).resolve().parent.parent
PAPERS = REPO / "papers"

# --- Canonical numbers (from CLAUDE.md). Kept identical across all papers. ----
# Each entry: a human label, a regex that captures the value in context, and the
# set of accepted string values. A capture not in the accepted set is flagged.
CANONICAL = [
    (
        "Proxima Centauri distance",
        # tight: the number must sit immediately before the unit, within a short
        # window of "Proxima Centauri", to avoid bleeding into nearby figures.
        re.compile(r"Proxima\s+Centauri[^.\n]{0,18}?(\d+\.\d+)\s*(?:ly|light-?years?)", re.I),
        {"4.246", "4.24"},  # 4.24 tolerated as a rounding of 4.246
    ),
    (
        "catalogue size (stars within 100 ly)",
        re.compile(r"(\d{2,4})\s+(?:real\s+)?stars?\s+within\s+(?:roughly\s+)?100", re.I),
        {"127"},
    ),
    (
        "reference seed mass",
        # Anchor on the canonical phrase "reference seed" with the value adjacent.
        # Bare "seed ... kg" is deliberately NOT matched: the subsystem paper's
        # decomposition legitimately states component and delta masses near "seed".
        re.compile(r"reference\s+seed[^.\n]{0,15}?(?:~|about|roughly\s+)?([\d,]{4,6})\s*kg", re.I),
        {"3,700", "3700"},
    ),
    (
        "cruise power (kW electric)",
        re.compile(r"(\d+(?:\.\d+)?)\s*kW\s+electric", re.I),
        {"4"},
    ),
    (
        "U-235 mass",
        re.compile(r"(\d+(?:\.\d+)?)\s*kg\s+of\s+U-235", re.I),
        {"16.5"},
    ),
    (
        "R_eff headline quad",
        # if the four-value headline is written out, it must be exactly this
        re.compile(r"0\.\d\d[^\n]{0,8}0\.\d\d[^\n]{0,8}1\.\d\d[^\n]{0,8}1\.\d\d"),
        {"MATCH"},  # sentinel: handled specially below
    ),
]

R_EFF_QUAD = "0.48"  # anchor; the full canonical string is 0.48 / 0.94 / 1.39 / 1.85

# --- Cross-reference naming (from CLAUDE.md) ---------------------------------
ALLOWED_PAPER_NAMES = {
    "vehicle", "payload", "bootstrapping", "analytical engineering",
    "computational engineering", "dna mission-ledger", "governance",
    "governed-amendment", "fermi", "knowledge-growth", "lineage-network",
    "subsystem budget", "routing", "ethics", "speciation",
}
# Known non-canonical shorthands → (severity, guidance). Matched as whole words
# inside the phrase before "paper"; guarded so the *correct* longer name (e.g.
# "governed-amendment") does not trip its own shorthand ("amendment").
KNOWN_WRONG = {
    "memory": ("high", 'use "the DNA mission-ledger paper", not "the memory paper"'),
    "engineering": ("high", 'ambiguous — say "analytical engineering paper" or "computational engineering paper"'),
    "network": ("medium", 'canonical name is "the lineage-network paper"'),
    "amendment": ("medium", 'canonical name is "the governed-amendment paper"'),
    "contact-governance": ("medium", 'canonical name is "the governance paper"'),
    "fleet-routing": ("medium", 'canonical name is "the routing paper"'),
}


def _lineno(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def split_body_refs(text: str) -> tuple[str, str]:
    """Return (body, references_block). references_block is '' if absent.

    The block ends at the first horizontal rule after the References heading:
    the papers close with an italic endnote after a '---' separator, and that
    endnote may name works with years ("Hoang et al. (2017)") that must not be
    parsed as reference entries. The endnote stays in the body for citation
    matching."""
    m = re.search(r"^##\s+References\s*$", text, re.M)
    if not m:
        return text, ""
    refs = text[m.end():]
    rule = re.search(r"^---\s*$", refs, re.M)
    if rule:
        return text[: m.start()] + refs[rule.end():], refs[: rule.start()]
    return text[: m.start()], refs


def check_latex(text: str) -> list[dict]:
    findings = []
    patterns = [
        (re.compile(r"\\[a-zA-Z]{2,}"), "LaTeX command (backslash macro)"),
        (re.compile(r"\\\(|\\\)|\\\[|\\\]"), "LaTeX math delimiter"),
        (re.compile(r"\$[^$\n]{1,80}\$"), "dollar-delimited math ($...$)"),
    ]
    for rx, label in patterns:
        for m in rx.finditer(text):
            findings.append({
                "check": "no-latex",
                "severity": "high",
                "line": _lineno(text, m.start()),
                "message": f"{label}: {m.group(0)!r} — series uses plain-text math only",
            })
    return findings


def check_tables(text: str) -> list[dict]:
    findings = []
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"\|\s*:?-{3,}", line) or (line.count("|") >= 2 and re.match(r"^\s*\|.*\|\s*$", line)):
            findings.append({
                "check": "no-tables",
                "severity": "high",
                "line": i,
                "message": f"looks like a Markdown table row: {line.strip()[:70]!r} — render as a bulleted list",
            })
    return findings


def _parse_references(refs: str) -> list[tuple[int, str, str, str]]:
    """Yield (line, raw, surname, year) for each reference entry."""
    out = []
    base_line = 0  # refs block is passed already sliced; caller adds offset
    for i, line in enumerate(refs.splitlines()):
        s = line.strip()
        if not s or s == "---":
            continue
        ym = re.search(r"\((\d{4}[a-z]?)\)", s)
        if not ym:
            continue
        surname = re.split(r",|;|\s&|\s\(", s, maxsplit=1)[0].strip()
        surname = re.sub(r"\.$", "", surname)
        out.append((i, s, surname, ym.group(1)))
    return out


def check_references(text: str) -> list[dict]:
    findings = []
    body, refs = split_body_refs(text)
    if not refs:
        findings.append({"check": "references", "severity": "medium", "line": 1,
                         "message": "no '## References' section found"})
        return findings
    refs_offset = _lineno(text, len(body))  # first line of refs block in whole doc
    entries = _parse_references(refs)

    # (a) uncited references: surname + year should co-occur in the body.
    # Try the full surname, then its first token (handles "Gaia Collaboration",
    # "van den Bergh", organisational authors) to avoid false positives.
    # The window is generous because the series often cites narratively --
    # "Drexler's foundational treatment ... (*Engines of Creation*, 1986)"
    # puts 84 characters between surname and year, which a tighter window
    # wrongly reported as uncited.
    for rel_line, raw, surname, year in entries:
        year_num = year[:4]
        keys = {re.escape(surname)}
        first_tok = surname.split()[0] if surname.split() else surname
        if len(first_tok) >= 4:
            keys.add(re.escape(first_tok))
        near = any(
            re.search(k + r"[^\n]{0,160}?" + year_num, body)
            or re.search(year_num + r"[^\n]{0,160}?" + k, body)
            for k in keys
        )
        if not near:
            findings.append({
                "check": "uncited-reference",
                "severity": "medium",
                "line": refs_offset + rel_line,
                "message": f"reference not obviously cited in text: {surname} ({year}) — verify",
            })

    # (b) alphabetical order of the reference list
    surnames = [sortkey(e[2]) for e in entries]
    ordered = sorted(surnames)
    if surnames != ordered:
        for k in range(1, len(surnames)):
            if surnames[k] < surnames[k - 1]:
                findings.append({
                    "check": "reference-order",
                    "severity": "low",
                    "line": refs_offset + entries[k][0],
                    "message": f"reference list not alphabetical near {entries[k][2]} "
                               f"(follows {entries[k-1][2]})",
                })
                break
    return findings


_CITE_SKIP = {
    "Section", "Sections", "Level", "Class", "Classes", "Scenario", "Scenarios",
    "Tier", "Stage", "Voyager", "Project", "Earth", "Galaxy", "Table", "Figure",
    "The", "In", "As", "At", "See", "By", "On", "For", "If", "But", "This",
    "These", "Those", "With", "From", "Under", "Over", "After", "Before",
    "During", "However", "Also", "Since", "While", "Their", "Its", "What",
    "When", "Where", "Both", "Each", "Per", "Via", "Between", "Within",
}


def check_citation_entries(text: str) -> list[dict]:
    """The reverse direction of check_references (a): every in-text citation
    must have a matching reference entry. Added 2026-09-01 after two separate
    insertion-script failures (Zwitter 2026-08-24; Sensintaffar 2026-09-01)
    left a citation briefly entry-less while every existing check stayed green.
    Matching is by surname token against ALL tokens in the reference block, so
    multi-word surnames ("Rivera León"), co-authors, and organisational
    authors ("Gaia Collaboration", "NAIC Staff") all resolve."""
    findings = []
    body, refs = split_body_refs(text)
    if not refs:
        return findings
    entry_tokens = set()
    for line in refs.splitlines():
        for tok in re.findall(r"[A-Z][\wÀ-ſ-]+", line):
            entry_tokens.add(tok)
    name_cls = r"[A-Z][\wÀ-ſ-]+"
    cited = {}
    # narrative: Surname (2026) / Surname's (2026) / Surname et al. (2026) /
    # Surname and Other (2026) / Surname & Other (2026)
    pat_nar = (name_cls + r"(?:'s)?(?:,? et al\.| and " + name_cls +
               r"| & " + name_cls + r")? \((?:19|20)\d{2}[a-z]?\)")
    for m in re.finditer(pat_nar, body):
        nm = re.match(name_cls, m.group(0)).group(0)
        cited.setdefault(nm, m.start())
    # parenthetical: (Surname 2026; Other & Third 1999, p. 7)
    for m in re.finditer(r"\(([^()]*(?:19|20)\d{2}[a-z]?[^()]*)\)", body):
        for part in m.group(1).split(";"):
            part = part.strip()
            if not re.search(r"(?:19|20)\d{2}", part):
                continue
            pm = re.match(r"(?:e\.g\.,?\s*|cf\.\s*|see\s+)?(" + name_cls + ")", part)
            if pm:
                cited.setdefault(pm.group(1), m.start())
    for name, pos in sorted(cited.items(), key=lambda kv: kv[1]):
        if name in _CITE_SKIP or len(name) < 3:
            continue
        if name not in entry_tokens:
            findings.append({
                "check": "citation-without-entry",
                "severity": "medium",
                "line": _lineno(text, pos),
                "message": f"in-text citation '{name}' has no matching reference entry",
            })
    return findings


def check_cross_reference_naming(text: str) -> list[dict]:
    findings = []
    body, _ = split_body_refs(text)
    # Capture up to 4 words before "paper"; only flag known non-canonical
    # shorthands, so descriptive prose ("the foundational paper", "the companion
    # paper") and regex artifacts spanning a prior "the/this" are left alone.
    for m in re.finditer(r"\bthe\s+([\w'’-]+(?:[\s-][\w'’-]+){0,3}?)\s+paper\b", body):
        phrase = m.group(1)
        if "\n" in phrase:
            continue
        low = phrase.lower()
        for key, (sev, msg) in KNOWN_WRONG.items():
            if not re.search(rf"\b{re.escape(key)}\b", low):
                continue
            if key == "network" and "lineage-network" in low:
                continue
            if key == "amendment" and "governed-amendment" in low:
                continue
            if key == "engineering" and ("analytical" in low or "computational" in low):
                continue
            # Trim the quoted phrase to start at the offending word for clarity.
            kpos = low.find(key)
            shown = phrase[kpos:] if kpos > 0 else phrase
            findings.append({
                "check": "cross-ref-naming",
                "severity": sev,
                "line": _lineno(body, m.start()),
                "message": f'"the {shown} paper": {msg}',
            })
            break
    return findings


def check_canonical_numbers(text: str) -> list[dict]:
    findings = []
    body, _ = split_body_refs(text)
    for label, rx, accepted in CANONICAL:
        for m in rx.finditer(body):
            if accepted == {"MATCH"}:
                # R_eff quad: must contain the exact canonical anchor sequence
                seg = m.group(0)
                if R_EFF_QUAD not in body[max(0, m.start() - 40):m.end() + 40]:
                    findings.append({
                        "check": "canonical-number",
                        "severity": "medium",
                        "line": _lineno(body, m.start()),
                        "message": f"R_eff-like quad {seg!r} — confirm it reads 0.48 / 0.94 / 1.39 / 1.85",
                    })
                continue
            val = m.group(1).replace(",", "").rstrip(".")
            accepted_norm = {a.replace(",", "") for a in accepted}
            if val not in accepted_norm:
                findings.append({
                    "check": "canonical-number",
                    "severity": "high",
                    "line": _lineno(body, m.start()),
                    "message": f"{label}: found {m.group(1)!r}, canonical is {' or '.join(sorted(accepted))}",
                })
    return findings


def _squash(s: str) -> str:
    """Whitespace-insensitive form, so line wrapping never breaks a match."""
    return re.sub(r"\s+", " ", s).strip()


def check_sibling_quotes(text: str, corpus: dict) -> list[dict]:
    """Verbatim quotations of a companion paper that no longer appear in it.

    The commonest defect in this series is a paper describing a companion that
    has since moved; its sharpest form is a quotation of a sentence a sibling
    no longer contains.  Three such breaks were found by hand in one week (the
    governed-amendment paper quoting the bootstrapping paper, and the
    lineage-network paper quoting the payload and knowledge-growth papers), so
    it is worth checking mechanically.

    Heuristic: a long quoted string, in a sentence that names a companion paper,
    which appears verbatim in no other paper in the corpus.  Reported as
    "verify" rather than "error" -- a quotation of an outside source sitting
    next to a cross-reference is a legitimate false positive.
    """
    canonical_names = (
        "vehicle paper", "payload paper", "bootstrapping paper",
        "analytical engineering paper", "computational engineering paper",
        "DNA mission-ledger paper", "governance paper", "governed-amendment paper",
        "Fermi paper", "knowledge-growth paper", "lineage-network paper",
        "subsystem budget paper", "routing paper", "ethics paper",
        "speciation paper", "security paper",
    )
    if not corpus:
        return []
    body, _ = split_body_refs(text)
    haystack = " ".join(_squash(t) for t in corpus.values())
    findings = []
    for m in re.finditer(r"[\"“]([^\"“”]{40,400})[\"”]", body):
        quote = _squash(m.group(1))
        if quote.lower() in haystack.lower():
            continue
        # Only flag when the surrounding sentence actually names a companion.
        start = max(0, m.start() - 260)
        context = body[start:m.end()]
        named = [n for n in canonical_names if n.lower() in context.lower()]
        if not named:
            continue
        findings.append({
            "check": "sibling-quote",
            "severity": "medium",
            "line": _lineno(body, m.start()),
            "message": (
                "quoted text near a reference to %s does not appear verbatim in "
                "any sibling paper -- verify it is an outside source and not a "
                "stale quotation: %r" % (named[0], quote[:70] + ("..." if len(quote) > 70 else ""))
            ),
        })
    return findings


ALL_CHECKS = [
    check_latex,
    check_tables,
    check_references,
    check_citation_entries,
    check_cross_reference_naming,
    check_canonical_numbers,
]

CORPUS_CHECKS = [
    check_sibling_quotes,
]


def review_paper(path: Path, corpus: dict | None = None) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    findings: list[dict] = []
    for fn in ALL_CHECKS:
        findings.extend(fn(text))
    if corpus:
        others = {k: v for k, v in corpus.items() if k != path.name}
        for fn in CORPUS_CHECKS:
            findings.extend(fn(text, others))
    findings.sort(key=lambda f: (f["line"], f["check"]))
    return findings


def _print(path: Path, findings: list[dict]) -> None:
    rank = {"high": 0, "medium": 1, "low": 2}
    findings = sorted(findings, key=lambda f: (rank[f["severity"]], f["line"]))
    print(f"\n=== {path.name} — {len(findings)} finding(s) ===")
    if not findings:
        print("  clean (deterministic checks)")
        return
    for f in findings:
        print(f"  [{f['severity']:6}] L{f['line']:<4} {f['check']}: {f['message']}")


def main(argv: list[str]) -> int:
    try:  # Windows consoles default to cp1252; paper text is UTF-8.
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    # --quotes enables the cross-paper sibling-quote check.  It is opt-in
    # because it is a heuristic: a long quoted string near a companion's name
    # that appears verbatim in no sibling.  That catches genuinely stale
    # quotations (three were found by hand in one week) but also fires on
    # legitimate quotation of outside sources and on deliberate partial quotes,
    # so its output needs triage rather than blind application.
    want_quotes = "--quotes" in argv
    argv = [a for a in argv if a != "--quotes"]
    if not argv:
        argv = ["--all"]
    if argv[0] == "--all":
        paths = sorted(PAPERS.glob("interstellar_AI_*_paper.md"))
    else:
        paths = [Path(a) if Path(a).is_absolute() else REPO / a for a in argv]
    # The whole series, so cross-paper checks can see every sibling even when
    # only one paper is being reviewed.
    corpus = {q.name: q.read_text(encoding="utf-8")
              for q in sorted(PAPERS.glob("interstellar_AI_*.md"))} if want_quotes else None
    total = 0
    for p in paths:
        if not p.exists():
            print(f"  ! not found: {p}")
            continue
        findings = review_paper(p, corpus)
        total += len(findings)
        _print(p, findings)
    print(f"\nTotal findings: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
