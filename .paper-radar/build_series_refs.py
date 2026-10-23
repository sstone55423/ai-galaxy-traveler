#!/usr/bin/env python3
"""
Paper Radar -- resolve the series' own reference lists to OpenAlex ids.

Writes .paper-radar/series_refs.json, the seed set for search.py's coupling
channel: a new work that cites references the series already relies on is on
topic by construction, whatever words it uses -- the property keyword queries
lack. Tested 2026-10-22: OpenAlex's cites: filter on Church et al. 2012 alone
returned Yang et al. 2026, which was then inserted into the DNA mission-ledger
paper from another channel.

Each reference entry in every paper's "## References" section is parsed for a
DOI, first-author surname, year and title. DOIs resolve in batches of 50; the
rest by title search within the year, accepted only if the returned title
matches closely (token overlap >= 0.8), so a wrong match is skipped rather
than seeded. Re-running is incremental: entries already resolved are kept.

Zero-dependency, per repo convention.

    python3 .paper-radar/build_series_refs.py
"""

import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "series_refs.json")
QUERIES = os.path.join(HERE, "queries.json")
CONTACT = "scott.stone@my.metrostate.edu"
UA = f"paper-radar/1.0 (AI Galaxy Traveler; mailto:{CONTACT})"

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s>\]]+", re.I)


def env_key():
    path = os.path.join(HERE, ".env")
    if not os.path.exists(path):
        return ""
    for line in open(path, encoding="utf-8"):
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""


KEY = env_key()


def get(path, **params):
    params["mailto"] = CONTACT
    if KEY:
        params["api_key"] = KEY
    url = f"https://api.openalex.org/{path}?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            if exc.code == 429 and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            print(f"  ! HTTP {exc.code} for {path}", file=sys.stderr)
            return None
        except Exception as exc:  # noqa: BLE001
            if attempt < 3:
                time.sleep(3)
                continue
            print(f"  ! {exc} for {path}", file=sys.stderr)
            return None
    return None


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def overlap(a, b):
    ta, tb = set(norm(a).split()), set(norm(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


def parse_reference(line):
    """-> dict(doi, author, year, title) from one reference-list entry."""
    doi = DOI_RE.search(line)
    doi = doi.group(0).rstrip(".,;)").lower() if doi else None
    author = line.split(",", 1)[0].strip()
    m = re.search(r"\((\d{4})[a-z]?\)\.\s*(.+)", line)
    year, title = (int(m.group(1)), m.group(2)) if m else (None, "")
    # the title runs to the first full stop or question mark followed by a
    # space and the venue (italic *Venue*, "In ", or an arXiv/URL tail)
    t = re.match(r"(.+?[.?!])\s+(?:\*|In |arXiv|https?://|\[)", title)
    title = (t.group(1) if t else title.split(". ")[0]).strip().rstrip(".")
    title = re.sub(r"[*_]", "", title)
    return {"doi": doi, "author": author, "year": year, "title": title}


def paper_references(path):
    text = open(path, encoding="utf-8").read()
    if "## References" not in text:
        return []
    refs = text.split("## References", 1)[1]
    out = []
    for line in refs.splitlines():
        line = line.strip()
        if re.match(r"^[A-ZÀ-ſ][^,]{0,60}, [A-ZÀ-ſ]", line) or \
                re.match(r"^[A-Z][A-Za-z ]+ \(\d{4}\)", line):
            out.append(line)
    return out


def main():
    cfg = json.load(open(QUERIES, encoding="utf-8"))
    file_to_key = {p["file"]: p["key"] for p in cfg["papers"]}
    prior = {}
    if os.path.exists(OUT):
        for r in json.load(open(OUT, encoding="utf-8")).get("refs", []):
            prior[r["ref"]] = r

    entries = {}
    for path in sorted(glob.glob(os.path.join(REPO, "papers", "interstellar_AI_*_paper.md"))):
        rel = os.path.relpath(path, REPO).replace(os.sep, "/")
        key = file_to_key.get(rel)
        if not key:
            continue
        for line in paper_references(path):
            ref = parse_reference(line)
            ident = ref["doi"] or f"{norm(ref['author'])}|{ref['year']}|{norm(ref['title'])[:60]}"
            e = entries.setdefault(ident, dict(ref, ref=ident, papers=[], id=None))
            if key not in e["papers"]:
                e["papers"].append(key)

    for ident, e in entries.items():
        if ident in prior and prior[ident].get("id"):
            e["id"] = prior[ident]["id"]
            e["resolved_by"] = prior[ident].get("resolved_by")

    todo_doi = [e for e in entries.values() if not e["id"] and e["doi"]]
    for i in range(0, len(todo_doi), 50):
        chunk = {e["doi"]: e for e in todo_doi[i:i + 50]}
        res = get("works", filter="doi:" + "|".join(chunk), select="id,doi,title", **{"per-page": 50})
        for w in (res or {}).get("results", []):
            d = (w.get("doi") or "").lower().replace("https://doi.org/", "")
            if d in chunk:
                chunk[d]["id"] = w["id"].rsplit("/", 1)[-1]
                chunk[d]["resolved_by"] = "doi"
        time.sleep(0.3)

    todo_title = [e for e in entries.values()
                  if not e["id"] and e["title"] and e["year"] and len(norm(e["title"]).split()) >= 3]
    for n, e in enumerate(todo_title, 1):
        res = get("works", filter=f"title.search:{norm(e['title'])[:200]},"
                                  f"publication_year:{e['year'] - 1}-{e['year'] + 1}",
                  select="id,title,publication_year,authorships", **{"per-page": 5})
        # Title alone mis-resolves: a review of Birch (2024) under the book's own
        # title, and a 1976 reply under Hart's (1975) title, both matched at
        # >= 0.83 on the first build. Require the reference's first-author
        # surname in the byline as well.
        surname = norm(e["author"]).split()[0] if norm(e["author"]) else ""

        def byline_ok(w):
            names = norm(" ".join(a.get("raw_author_name") or "" for a in w.get("authorships") or []))
            return bool(surname) and f" {surname} " in f" {names} "

        best = max(((overlap(e["title"], w.get("title")), w) for w in (res or {}).get("results", [])
                    if byline_ok(w)),
                   default=(0, None), key=lambda x: x[0])
        if best[1] is not None and best[0] >= 0.8:
            e["id"] = best[1]["id"].rsplit("/", 1)[-1]
            e["resolved_by"] = f"title ({best[0]:.2f})"
        if n % 25 == 0:
            print(f"  title search {n}/{len(todo_title)}", file=sys.stderr)
        time.sleep(0.25)

    # cited_by_count lets the coupling channel tell a niche reference (a new
    # work citing it is probably on topic) from a classic (Shannon 1948 and
    # Hardin 1968 are cited by everything); see search_coupling.
    ids = [e["id"] for e in entries.values() if e["id"]]
    for i in range(0, len(ids), 50):
        res = get("works", filter="ids.openalex:" + "|".join(ids[i:i + 50]),
                  select="id,cited_by_count,doi", **{"per-page": 50})
        found = {w["id"].rsplit("/", 1)[-1]: w for w in (res or {}).get("results", [])}
        for e in entries.values():
            w = found.get(e["id"])
            if w:
                e["cited_by"] = w.get("cited_by_count")
                # a DOI for title-resolved references too: S2's recommendation
                # channel can only be seeded with DOIs
                if not e.get("doi") and w.get("doi"):
                    e["doi"] = w["doi"].lower().replace("https://doi.org/", "")
        time.sleep(0.25)

    refs = sorted(entries.values(), key=lambda e: (e["author"], e["year"] or 0))
    resolved = [r for r in refs if r["id"]]
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"_note": "Seed set for search.py's coupling channel; rebuild with "
                            "build_series_refs.py after a paper's reference list changes.",
                   "refs": refs}, fh, indent=1, ensure_ascii=False)
    by_doi = sum(1 for r in resolved if r.get("resolved_by") == "doi")
    print(f"{len(refs)} unique references; {len(resolved)} resolved "
          f"({by_doi} by DOI, {len(resolved) - by_doi} by title); "
          f"{len(refs) - len(resolved)} unresolved (books, reports, web pages, preprints "
          f"OpenAlex lacks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
