#!/usr/bin/env python3
"""Fill cites_watch OpenAlex ids in queries.json from stored doi/title/year hints.

One-shot, idempotent: entries whose id already starts with "W" are left alone.
Run when the OpenAlex polite-pool quota permits (a hard 429 with a long
Retry-After means try again in a few hours):

    python3 .paper-radar/resolve_canon.py

Each resolution is verified by title match before it is written; an entry that
cannot be verified stays null and the sweep keeps skipping it harmlessly.
Zero-dependency (stdlib only), per repo convention.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
QUERIES_PATH = os.path.join(HERE, "queries.json")
CONTACT = "scott.stone@my.metrostate.edu"
UA = {"User-Agent": f"paper-radar/1.0 (AI Galaxy Traveler; mailto:{CONTACT})"}


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and i < tries - 1:
                wait = 20 * (i + 1)
                print(f"  429; waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(8)


def resolve(entry):
    title, year, doi = entry.get("title", ""), entry.get("year"), entry.get("doi")
    if doi:
        w = get(f"https://api.openalex.org/works/https://doi.org/{doi}?mailto={CONTACT}")
        cands = [w]
    else:
        params = urllib.parse.urlencode({
            "filter": f"title.search:{title},publication_year:{year}",
            "per-page": 5, "mailto": CONTACT})
        cands = get(f"https://api.openalex.org/works?{params}").get("results", [])
    best = None
    for w in cands:
        t = (w.get("display_name") or "").lower()
        if title.lower()[:26] in t:
            if best is None or (w.get("cited_by_count") or 0) > (best.get("cited_by_count") or 0):
                best = w
    return best


def main():
    with open(QUERIES_PATH, encoding="utf-8") as fh:
        q = json.load(fh)
    changed = 0
    for paper in q["papers"]:
        for entry in paper.get("cites_watch", []):
            if (entry.get("id") or "").startswith("W"):
                continue
            time.sleep(6)
            try:
                best = resolve(entry)
            except Exception as exc:
                print(f"  {entry['label']:22s} FAILED: {exc}")
                continue
            if best:
                wid = best["id"].rsplit("/", 1)[-1]
                entry["id"] = wid
                changed += 1
                print(f"  {entry['label']:22s} -> {wid}  cited_by={best.get('cited_by_count')}"
                      f"  '{(best.get('display_name') or '')[:55]}'")
            else:
                print(f"  {entry['label']:22s} UNRESOLVED (no verified title match)")
    if changed:
        with open(QUERIES_PATH, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(q, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    print(f"{changed} id(s) written")


if __name__ == "__main__":
    main()
