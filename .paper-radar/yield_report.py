#!/usr/bin/env python3
"""
Paper Radar -- yield per channel.

Which channels find the papers that end up in the series? Reads every archived
sweep in .paper-radar/candidates/ (written by search.py on --mark-seen), the
digest for each sweep date, and the papers themselves, and reports for each
channel (and each paper):

    candidates   records the channel delivered to screening
    surfaced     of those, how many appear in that day's digest (any section)
    inserted     of those, how many are now cited in a paper in papers/

"Surfaced" and "inserted" are detected by DOI, arXiv id, or normalized title,
so no manual bookkeeping is needed. A candidate counts for the channel that
first delivered it in that sweep (its found_via); cross-source duplicates are
merged by search.py before this point.

Zero-dependency, per repo convention.

Usage:
    python3 .paper-radar/yield_report.py
    python3 .paper-radar/yield_report.py --by-query      # rank individual queries
    python3 .paper-radar/yield_report.py --json out.json

Written 2026-10-22 after a radar audit that could measure only one week, because
candidate files were deleted after each run.
"""

import argparse
import collections
import glob
import gzip
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ARCHIVE = os.path.join(HERE, "candidates")
DIGESTS = os.path.join(HERE, "digests")
PAPERS = os.path.join(REPO, "papers")


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def title_key(title):
    """First ~8 words of the normalized title: long enough to be specific,
    short enough to survive a subtitle dropped or reworded in a reference."""
    words = norm(title).split()
    return " ".join(words[:8]) if len(words) >= 4 else ""


def load_archives():
    sweeps = {}
    for path in sorted(glob.glob(os.path.join(ARCHIVE, "*.json.gz"))):
        date = os.path.basename(path)[:10]
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            sweeps[date] = json.load(fh)
    return sweeps


def channel_of(rec):
    return (rec.get("found_via") or "unknown").split(":", 1)[0].strip()


def found_in(rec, haystack_norm, haystack_raw):
    doi = (rec.get("doi") or "").lower()
    if doi and doi in haystack_raw:
        return True
    aid = rec.get("arxiv_id")
    if aid and aid in haystack_raw:
        return True
    tk = title_key(rec.get("title"))
    return bool(tk) and f" {tk} " in haystack_norm


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--by-query", action="store_true",
                    help="also rank individual queries by surfaced/inserted")
    ap.add_argument("--json", metavar="PATH", help="write the counts as JSON")
    args = ap.parse_args()

    sweeps = load_archives()
    if not sweeps:
        print(f"No archived sweeps in {ARCHIVE}. search.py writes one on --mark-seen.")
        return 1

    paper_raw = ""
    for path in glob.glob(os.path.join(PAPERS, "*.md")):
        with open(path, encoding="utf-8") as fh:
            paper_raw += fh.read().lower() + "\n"
    paper_norm = " " + norm(paper_raw) + " "

    by_channel = collections.defaultdict(collections.Counter)
    by_paper = collections.defaultdict(collections.Counter)
    by_query = collections.defaultdict(collections.Counter)
    inserted_items = []

    for date, payload in sweeps.items():
        dpath = os.path.join(DIGESTS, f"{date}.md")
        digest_raw = open(dpath, encoding="utf-8").read().lower() if os.path.exists(dpath) else ""
        digest_norm = " " + norm(digest_raw) + " "
        for pkey, block in (payload.get("results") or {}).items():
            for rec in block.get("candidates", []):
                ch = channel_of(rec)
                q = (rec.get("found_via") or "")[:90]
                surfaced = bool(digest_raw) and found_in(rec, digest_norm, digest_raw)
                inserted = found_in(rec, paper_norm, paper_raw)
                for counter in (by_channel[ch], by_paper[pkey], by_query[q]):
                    counter["candidates"] += 1
                    counter["surfaced"] += surfaced
                    counter["inserted"] += inserted
                if not rec.get("abstract"):
                    by_channel[ch]["no_abstract"] += 1
                if inserted:
                    inserted_items.append((date, pkey, ch, (rec.get("title") or "")[:70]))

    def table(title, rows, extra=()):
        print(f"\n{title}")
        print(f"  {'':22s} {'cand':>6s} {'surf':>6s} {'ins':>5s} {'surf%':>6s} {'ins%':>6s}"
              + "".join(f" {e:>8s}" for e in extra))
        for name, c in sorted(rows.items(), key=lambda kv: -kv[1]["candidates"]):
            n = c["candidates"] or 1
            print(f"  {name[:22]:22s} {c['candidates']:6d} {c['surfaced']:6d} {c['inserted']:5d}"
                  f" {100 * c['surfaced'] / n:5.1f}% {100 * c['inserted'] / n:5.1f}%"
                  + "".join(f" {c[e]:8d}" for e in extra))

    print(f"Sweeps archived: {', '.join(sweeps)}")
    table("By channel", by_channel, extra=("no_abstract",))
    table("By paper", by_paper)
    if args.by_query:
        top = {q: c for q, c in by_query.items() if c["surfaced"] or c["inserted"]}
        table("Queries that surfaced or inserted anything", top)
        dead = sum(1 for c in by_query.values() if not c["surfaced"])
        print(f"\n  {dead} of {len(by_query)} queries surfaced nothing across the archive")
    unique = {norm(t) for _, _, _, t in inserted_items}
    print(f"\nInserted into the series: {len(unique)} unique works"
          f" ({len(inserted_items)} candidate records; one work screened for several"
          f" papers counts once per paper above)")
    for item in inserted_items:
        print(f"  {item[0]}  {item[1]:16s} via {item[2]:10s}  {item[3]}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"sweeps": list(sweeps),
                       "by_channel": by_channel, "by_paper": by_paper,
                       "inserted": inserted_items}, fh, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
