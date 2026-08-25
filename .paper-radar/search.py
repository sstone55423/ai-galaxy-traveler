#!/usr/bin/env python3
"""
Paper Radar -- literature search for the AI Galaxy Traveler series.

Zero-dependency (stdlib only), per repo convention. Queries arXiv, OpenAlex,
Crossref and -- only if a key is present -- Semantic Scholar. Deduplicates
against .paper-radar/seen.json and writes ranked candidates to stdout/JSON.

This script FINDS and CHEAPLY FILTERS. It deliberately does NOT judge relevance,
and it never edits a paper -- both are the agent's job (see the paper-radar
skill). Expect ~300-450 candidates from a 7-day sweep; that is the intended
volume, sized for ~20-30 per paper across 15 parallel screening agents.

Why there is no relevance filter here, having tried one:
    A term-coverage filter was built and measured against a real 460-candidate
    sweep. It could not separate signal from noise at any threshold. At 0.6 it
    KEPT "Basics of Artificial Intelligence and Machine Learning" and
    "Digitalizing Mesopotamian Heritage" (both scoring 1.00) while DROPPING
    "Mechanistic World Models" (0.57), which was plausibly relevant. Worse, 33%
    of records carry no abstract, leaving any lexical test blind to a third of
    the corpus. Telling "AI as the Fourth Paradigm of Scientific Discovery"
    from "Basics of AI and ML" is a semantic judgement. Do not re-add a lexical
    relevance gate here; a confidently wrong signal is worse than none. The
    exclude-list in queries.json is different in kind -- it kills unambiguous
    homonyms ("Fermi level"), not weak matches.

Usage:
    python3 .paper-radar/search.py --since 2026-07-10
    python3 .paper-radar/search.py --days 7 --out /tmp/candidates.json
    python3 .paper-radar/search.py --paper fermi --days 90     # single paper
    python3 .paper-radar/search.py --baseline --since 2015-01-01  # first-run sweep
    python3 .paper-radar/search.py --days 7 --mark-seen         # commit dedup state

Notes:
  - arXiv MUST be https. The documented http endpoint 301s and, without -L,
    silently returns an empty body. This bit us during design; do not "simplify".
  - Crossref is the noisiest source by far. Queries in queries.json are
    deliberately narrow, and the exclude-list is load-bearing: an unfiltered
    'von neumann probe' query returns papers about von Neumann ALGEBRAS.
  - Semantic Scholar unauthenticated shares a 1000 req/s pool across all
    anonymous users and returns 429 most of the time. With a key you get 1 req/s
    to yourself. No key -> the source is skipped, not fatal.
"""

import argparse
import datetime as dt
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
QUERIES_PATH = os.path.join(HERE, "queries.json")
SEEN_PATH = os.path.join(HERE, "seen.json")
ENV_PATH = os.path.join(HERE, ".env")

CONTACT = "scott.stone@my.metrostate.edu"
UA = f"paper-radar/1.0 (AI Galaxy Traveler; mailto:{CONTACT})"

# Politeness delays (seconds). arXiv explicitly asks for >=3s between calls.
DELAY = {"arxiv": 3.0, "openalex": 0.2, "crossref": 0.5, "s2": 1.1}

TIMEOUT = 30


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def log(msg):
    print(msg, file=sys.stderr, flush=True)


def load_env():
    """Read .paper-radar/.env if present. Never logged, never committed."""
    if not os.path.exists(ENV_PATH):
        return
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except OSError as exc:
        log(f"  ! could not read .env: {exc}")


def fetch(url, headers=None, retries=3):
    """GET with backoff. Returns body text, or None on give-up."""
    headers = dict(headers or {})
    headers.setdefault("User-Agent", UA)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            # True exponential backoff with jitter, on both rate-limit and
            # server-error responses. Semantic Scholar's API terms ask callers
            # to apply exponential backoff specifically; the other hosts are
            # free services doing us a favour and deserve the same treatment.
            if exc.code == 429:
                wait = (2 ** attempt) * 5 + random.uniform(0, 1)
                log(f"  ! 429 rate-limited, backing off {wait:.1f}s")
                time.sleep(wait)
                continue
            if exc.code in (500, 502, 503, 504):
                time.sleep((2 ** attempt) * 2 + random.uniform(0, 1))
                continue
            log(f"  ! HTTP {exc.code} for {url[:90]}")
            return None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            log(f"  ! network error ({exc}); retry {attempt + 1}/{retries}")
            time.sleep((2 ** attempt) * 2 + random.uniform(0, 1))
    return None


def norm_doi(doi):
    if not doi:
        return None
    d = doi.strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d or None


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def record_key(rec):
    """Stable identity for dedup: arXiv id > DOI > normalized title.

    arXiv is checked FIRST and DataCite arXiv DOIs are unwrapped, because the
    same preprint arrives from arXiv with a bare id and from OpenAlex with DOI
    10.48550/arXiv.NNNN. Keying naively on DOI made those two records look
    distinct and every arXiv preprint was reported twice.
    """
    doi = rec.get("doi")
    if doi:
        m = re.match(r"10\.48550/arxiv\.(.+)$", doi, re.I)
        if m:
            return "arxiv:" + m.group(1).split("v")[0].lower()
    if rec.get("arxiv_id"):
        return "arxiv:" + rec["arxiv_id"].split("v")[0].lower()
    if doi:
        # Zenodo mints a fresh DOI per version, and consecutive deposits of the
        # same work land on adjacent record ids (…21992962 / …21992963), which
        # defeated seen.json dedup on consecutive runs (2026-08-21 / 08-24
        # digests). Collapse the trailing digit IN THE KEY ONLY — the earlier
        # fix collapsed it inside norm_doi, which mangled the record's display
        # DOI and surfaced in the 08-25 digest as "malformed source metadata"
        # (a trailing x the screener had to repair). The stored DOI stays real;
        # only the dedup key is collapsed, in the same "…x" form seen.json
        # already holds from prior runs.
        m = re.match(r"^(10\.5281/zenodo\.\d+)\d$", doi)
        if m:
            return "doi:" + m.group(1) + "x"
        return "doi:" + doi
    return "title:" + norm_title(rec.get("title"))


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text or "")


def clean_ws(text):
    return re.sub(r"\s+", " ", text or "").strip()


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------

def search_arxiv(query, since, categories=None, max_results=50):
    """arXiv Atom API. https only -- see module docstring."""
    q = query
    if categories:
        cats = " OR ".join(f"cat:{c}" for c in categories)
        q = f"({query}) AND ({cats})"
    params = urllib.parse.urlencode({
        "search_query": q,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    body = fetch(f"https://export.arxiv.org/api/query?{params}")
    if not body:
        return []

    out = []
    for entry in re.findall(r"<entry>(.*?)</entry>", body, re.S):
        def grab(tag):
            m = re.search(rf"<{tag}>(.*?)</{tag}>", entry, re.S)
            return clean_ws(strip_tags(m.group(1))) if m else ""

        published = grab("published")
        date = published[:10]
        if date and date < since:
            continue  # sorted desc, but keep scanning: cheap

        idurl = grab("id")
        m = re.search(r"abs/([^v\s]+)(v\d+)?", idurl)
        arxiv_id = m.group(1) if m else None

        authors = re.findall(r"<author>\s*<name>(.*?)</name>", entry, re.S)
        doi_m = re.search(r'<arxiv:doi[^>]*>(.*?)</arxiv:doi>', entry, re.S)

        out.append({
            "source": "arxiv",
            "title": grab("title"),
            "authors": [clean_ws(a) for a in authors],
            "date": date,
            "year": int(date[:4]) if date[:4].isdigit() else None,
            "venue": "arXiv preprint",
            "doi": norm_doi(doi_m.group(1)) if doi_m else None,
            "arxiv_id": arxiv_id,
            "url": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else idurl,
            "abstract": grab("summary")[:1500],
        })
    return out


def search_openalex(query, since, per_page=10):
    # sort=relevance_score:desc is load-bearing. Sorting by publication_date
    # returns whatever is NEWEST rather than whatever is RELEVANT, which in
    # testing meant microalgae wastewater papers under a Fermi-paradox query.
    # Relevance-sort then date-filter; never date-sort.
    # (title_and_abstract.search is more precise but far too strict here --
    # it cut one query from 1447 matches to 1.)
    params = urllib.parse.urlencode({
        "search": query,
        "filter": f"from_publication_date:{since}",
        "per-page": per_page,
        "sort": "relevance_score:desc",
        "mailto": CONTACT,
    })
    body = fetch(f"https://api.openalex.org/works?{params}")
    if not body:
        return []
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return []

    out = []
    for w in data.get("results", []):
        loc = w.get("primary_location") or {}
        src = loc.get("source") or {}
        authors = [
            (a.get("author") or {}).get("display_name")
            for a in (w.get("authorships") or [])
        ]
        out.append({
            "source": "openalex",
            "title": clean_ws(w.get("title") or w.get("display_name")),
            "authors": [a for a in authors if a][:12],
            "date": w.get("publication_date") or "",
            "year": w.get("publication_year"),
            "venue": src.get("display_name") or "unknown venue",
            "doi": norm_doi(w.get("doi")),
            "arxiv_id": None,
            "url": w.get("doi") or (loc.get("landing_page_url") or ""),
            "abstract": reconstruct_abstract(w.get("abstract_inverted_index"))[:1500],
            "cited_by": w.get("cited_by_count"),
            "oa_url": (w.get("best_oa_location") or {}).get("pdf_url"),
        })
    return out


def reconstruct_abstract(inv):
    """OpenAlex ships abstracts as an inverted index. Rebuild word order."""
    if not inv:
        return ""
    positions = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def search_crossref(query, since, rows=8):
    # NO sort=published here. With date-sort this endpoint returned, verbatim:
    # Roman book censorship, a German article about Dubai chocolate shops, and a
    # linguistics paper matching on the word "von". Default relevance sort
    # returns on-topic results for the same query. Do not add a sort param.
    params = urllib.parse.urlencode({
        "query.bibliographic": query,
        "filter": f"from-pub-date:{since}",
        "rows": rows,
        "select": "title,issued,container-title,DOI,author,abstract,type",
        "mailto": CONTACT,
    })
    body = fetch(f"https://api.crossref.org/works?{params}")
    if not body:
        return []
    try:
        items = json.loads(body).get("message", {}).get("items", [])
    except json.JSONDecodeError:
        return []

    out = []
    for it in items:
        if it.get("type") in ("component", "dataset"):
            continue
        # Book front matter, indexes, and "Also of Interest" pages arrive as
        # separate DOIs with these suffixes and never carry abstracts
        # (2026-08-13 digest: one Wiley handbook dumped a third of a day's
        # batch this way). Drop them at ingest.
        _doi = (it.get("DOI") or "").lower()
        if _doi.endswith((".fmatter", ".index", ".oth", ".ind", ".toc")):
            continue
        parts = (it.get("issued") or {}).get("date-parts") or [[]]
        dp = parts[0] if parts else []
        year = dp[0] if dp else None
        date = "-".join(f"{p:02d}" if i else str(p) for i, p in enumerate(dp)) if dp else ""
        authors = [
            clean_ws(f"{a.get('given', '')} {a.get('family', '')}")
            for a in (it.get("author") or [])
        ]
        titles = it.get("title") or []
        containers = it.get("container-title") or []
        out.append({
            "source": "crossref",
            "title": clean_ws(titles[0] if titles else ""),
            "authors": [a for a in authors if a][:12],
            "date": date,
            "year": year,
            "venue": clean_ws(containers[0]) if containers else "unknown venue",
            "doi": norm_doi(it.get("DOI")),
            "arxiv_id": None,
            "url": f"https://doi.org/{it.get('DOI')}" if it.get("DOI") else "",
            "abstract": clean_ws(strip_tags(it.get("abstract", "")))[:1500],
        })
    return out


def search_s2(query, since, limit=20):
    """Semantic Scholar -- optional. Skipped entirely without a key."""
    key = os.environ.get("S2_API_KEY")
    if not key:
        return []
    year_from = since[:4]
    params = urllib.parse.urlencode({
        "query": query,
        "limit": limit,
        "year": f"{year_from}-",
        "fields": "title,year,venue,externalIds,abstract,authors,publicationDate,citationCount",
    })
    body = fetch(
        f"https://api.semanticscholar.org/graph/v1/paper/search?{params}",
        headers={"x-api-key": key},
    )
    if not body:
        return []
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return []
    if "data" not in data:
        return []

    out = []
    for p in data["data"]:
        ext = p.get("externalIds") or {}
        date = p.get("publicationDate") or (str(p.get("year")) if p.get("year") else "")
        if date and date < since:
            continue
        out.append({
            "source": "semanticscholar",
            "title": clean_ws(p.get("title")),
            "authors": [a.get("name") for a in (p.get("authors") or []) if a.get("name")][:12],
            "date": date,
            "year": p.get("year"),
            "venue": p.get("venue") or "unknown venue",
            "doi": norm_doi(ext.get("DOI")),
            "arxiv_id": ext.get("ArXiv"),
            "url": f"https://doi.org/{ext['DOI']}" if ext.get("DOI") else "",
            "abstract": clean_ws(p.get("abstract"))[:1500],
            "cited_by": p.get("citationCount"),
        })
    return out


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        log(f"  ! could not read {path}: {exc}")
        return default


def excluded(title, patterns):
    t = (title or "").lower()
    return any(p.lower() in t for p in patterns)


def merge_record(target, incoming):
    """Fold a duplicate hit into the record we keep.

    Prefer the published version's venue/DOI over the preprint's, keep the
    longest abstract, and remember every source that surfaced the work -- that
    a hit appears in three independent indexes is itself weak relevance signal.
    """
    target.setdefault("also_seen_in", [])
    if incoming.get("source") and incoming["source"] not in target["also_seen_in"]:
        if incoming["source"] != target.get("source"):
            target["also_seen_in"].append(incoming["source"])
    if not target.get("doi") and incoming.get("doi"):
        target["doi"] = incoming["doi"]
        target["url"] = incoming.get("url") or target.get("url")
    if not target.get("arxiv_id") and incoming.get("arxiv_id"):
        target["arxiv_id"] = incoming["arxiv_id"]
    if incoming.get("venue") and target.get("venue") in (None, "", "unknown venue", "arXiv preprint"):
        if incoming["venue"] not in ("unknown venue", ""):
            target["venue"] = incoming["venue"]
    if len(incoming.get("abstract") or "") > len(target.get("abstract") or ""):
        target["abstract"] = incoming["abstract"]
    if incoming.get("cited_by") is not None and target.get("cited_by") is None:
        target["cited_by"] = incoming["cited_by"]
    if incoming.get("oa_url") and not target.get("oa_url"):
        target["oa_url"] = incoming["oa_url"]


def future_dated(rec, grace_days=120):
    """Crossref 'issued' dates are frequently wrong -- testing surfaced papers
    dated 2031, 2030 and 2028. Some lead-time is legitimate (an accepted article
    with a future issue date), so allow a grace window and drop the rest."""
    date = (rec.get("date") or "").strip()
    if not date:
        return False
    limit = (dt.date.today() + dt.timedelta(days=grace_days)).isoformat()
    return date[:10] > limit


def mark_seen_from(path):
    """Record an already-completed sweep in seen.json without re-searching.

    Kept separate from --mark-seen because the agent writes the digest between
    searching and committing dedup state: if the run dies at the digest step we
    must NOT have already marked those papers seen, or they would vanish from
    every future run without ever having been reported.
    """
    payload = load_json(path, None)
    if not payload:
        log(f"FATAL: no candidates file at {path}")
        return 2
    if not payload.get("complete", False):
        log("REFUSING: that sweep is incomplete. Marking it seen would "
            "permanently hide papers that were never searched. Finish the "
            "sweep with --resume first.")
        return 3

    seen = load_json(SEEN_PATH, {"keys": {}, "last_run": None})
    today = dt.date.today().isoformat()
    added = 0
    for key, block in (payload.get("results") or {}).items():
        for rec in block.get("candidates", []):
            rk = rec.get("_key") or record_key(rec)
            if rk not in seen.setdefault("keys", {}):
                added += 1
            seen["keys"][rk] = {
                "first_seen": today,
                "paper": key,
                "title": (rec.get("title") or "")[:120],
            }
    seen["last_run"] = today
    with open(SEEN_PATH, "w", encoding="utf-8") as fh:
        json.dump(seen, fh, indent=2, ensure_ascii=False)
    log(f"seen.json: +{added} new, {len(seen['keys'])} known total, last_run={today}")
    print(json.dumps({"status": "marked", "added": added, "total": len(seen["keys"])}))
    return 0


def run(args):
    load_env()
    cfg = load_json(QUERIES_PATH, None)
    if not cfg:
        log(f"FATAL: no query config at {QUERIES_PATH}")
        return 2

    seen = load_json(SEEN_PATH, {"keys": {}, "last_run": None})
    seen_keys = set(seen.get("keys", {}).keys())

    if args.since:
        since = args.since
    else:
        since = (dt.date.today() - dt.timedelta(days=args.days)).isoformat()

    papers = cfg["papers"]
    if args.paper:
        wanted = [k.strip() for k in args.paper.split(",") if k.strip()]
        papers = [p for p in papers if p["key"] in wanted]
        if not papers:
            log(f"FATAL: no paper matching '{args.paper}'")
            return 2

    out_path = args.out or os.path.join(HERE, "candidates.json")

    # Resume support. The sandbox kills long-running children when the shell
    # call that spawned them exits, so a full 15-paper sweep cannot finish in a
    # single invocation. The agent calls this script repeatedly with --resume;
    # each invocation does as many papers as fit in --budget seconds and appends
    # to the same file. A half-finished sweep is therefore recoverable rather
    # than silently truncated -- the failure mode that matters most here is a
    # digest that LOOKS complete but quietly dropped ten papers.
    prior = {}
    if args.resume and os.path.exists(out_path):
        existing = load_json(out_path, {})
        prior = existing.get("results", {}) or {}
        if prior:
            log(f"resuming: {len(prior)} paper(s) already done -> {sorted(prior)}")
        papers = [p for p in papers if p["key"] not in prior]
        if not papers:
            log("nothing left to do; all papers already in output")
            print(json.dumps({"status": "complete", "papers": len(prior)}))
            return 0

    started = time.monotonic()

    global_exclude = cfg.get("defaults", {}).get("exclude", [])
    if args.no_s2:
        os.environ.pop("S2_API_KEY", None)
    s2_on = bool(os.environ.get("S2_API_KEY"))

    log(f"Paper Radar: {len(papers)} paper(s), since {since}")
    log(f"Sources: arxiv, openalex, crossref" + (", semanticscholar" if s2_on else " (s2: no key, skipped)"))

    stats = {"raw": 0, "excluded": 0, "future_dated": 0, "dupe_seen": 0, "dupe_run": 0, "kept": 0}

    results = dict(prior)
    truncated = False

    for paper in papers:
        key = paper["key"]

        if args.budget and (time.monotonic() - started) > args.budget:
            log(f"\n[budget] {args.budget}s elapsed; stopping cleanly before '{key}'")
            truncated = True
            break

        log(f"\n[{key}] {paper['title']}")
        excl = global_exclude + paper.get("exclude", [])
        hits = {}
        title_index = {}

        plan = []
        # arXiv asks for >=3s between requests, so its phrases are OR-ed into a
        # single query rather than issued one-by-one. Four separate calls cost
        # 12s of pure sleep per paper; across 15 papers that alone blew the
        # runtime past the point where the run could finish at all.
        arxiv_qs = paper.get("arxiv", [])
        if arxiv_qs:
            plan.append(("arxiv", " OR ".join(f"({q})" for q in arxiv_qs)))
        for q in paper.get("openalex", []):
            plan.append(("openalex", q))
        for q in paper.get("crossref", []):
            plan.append(("crossref", q))
        if s2_on:
            for q in paper.get("openalex", [])[:2]:
                plan.append(("s2", q))

        for source, q in plan:
            try:
                if source == "arxiv":
                    found = search_arxiv(q, since, paper.get("arxiv_categories"))
                elif source == "openalex":
                    found = search_openalex(q, since)
                elif source == "crossref":
                    found = search_crossref(q, since)
                elif source == "s2":
                    found = search_s2(q, since)
                else:
                    found = []
            except Exception as exc:  # a bad query must not kill the 6am run
                log(f"  ! {source} query failed ({exc}); continuing")
                found = []

            stats["raw"] += len(found)
            kept_here = 0
            for rec in found:
                if not rec.get("title"):
                    continue
                if excluded(rec["title"], excl):
                    stats["excluded"] += 1
                    continue
                if future_dated(rec):
                    stats["future_dated"] += 1
                    continue
                rk = record_key(rec)
                if rk in seen_keys and not args.ignore_seen:
                    stats["dupe_seen"] += 1
                    continue

                # Secondary title-based dedup: a DOI-bearing journal record and
                # its arXiv preprint share no identifier at all, so id-matching
                # alone still lets the same work through twice.
                nt = norm_title(rec.get("title"))
                if nt and nt in title_index:
                    rk = title_index[nt]
                    if rk in hits:
                        stats["dupe_run"] += 1
                        merge_record(hits[rk], rec)
                        continue

                if rk in hits:
                    stats["dupe_run"] += 1
                    merge_record(hits[rk], rec)
                    continue
                if nt:
                    title_index[nt] = rk
                rec["paper_key"] = key
                rec["found_via"] = f"{source}: {q}"
                rec["_key"] = rk
                hits[rk] = rec
                kept_here += 1

            log(f"  {source:14s} {len(found):3d} hits -> {kept_here:2d} new   ({q[:52]})")
            time.sleep(DELAY.get(source, 0.5))

        ranked = sorted(
            hits.values(),
            key=lambda r: (r.get("date") or "", r.get("cited_by") or 0),
            reverse=True,
        )
        if args.limit:
            ranked = ranked[: args.limit]
        stats["kept"] += len(ranked)
        results[key] = {
            "paper": paper["file"],
            "title": paper["title"],
            "thesis": paper["thesis"],
            "candidates": ranked,
        }
        log(f"  => {len(ranked)} candidate(s) for screening")

    all_keys = [p["key"] for p in cfg["papers"]]
    if args.paper:
        all_keys = [k for k in all_keys if k in [w.strip() for w in args.paper.split(",")]]
    remaining = [k for k in all_keys if k not in results]
    complete = not remaining

    payload = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "since": since,
        "sources": ["arxiv", "openalex", "crossref"] + (["semanticscholar"] if s2_on else []),
        "stats": stats,
        "complete": complete,
        "remaining": remaining,
        "results": results,
    }

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)

    log(f"\n{'=' * 62}")
    log(f"raw hits {stats['raw']} | excluded {stats['excluded']} | "
        f"future-dated {stats['future_dated']} | already-seen {stats['dupe_seen']} | "
        f"cross-source dupes {stats['dupe_run']} | KEPT {stats['kept']}")
    log(f"candidates -> {out_path}")

    if truncated or remaining:
        log(f"INCOMPLETE -- {len(remaining)} paper(s) left: {', '.join(remaining)}")
        log(f"Re-run the same command with --resume to continue.")
    else:
        log("COMPLETE -- all papers swept.")

    # machine-readable line for the agent driving the loop
    print(json.dumps({
        "status": "complete" if complete else "incomplete",
        "done": len(results),
        "remaining": remaining,
        "kept": stats["kept"],
        "out": out_path,
    }))

    if args.mark_seen and not complete:
        log("! refusing --mark-seen on an incomplete sweep "
            "(would permanently hide papers that were never actually searched)")
    elif args.mark_seen:
        today = dt.date.today().isoformat()
        for key, block in results.items():
            for rec in block["candidates"]:
                seen.setdefault("keys", {})[rec["_key"]] = {
                    "first_seen": today,
                    "paper": key,
                    "title": rec["title"][:120],
                }
        seen["last_run"] = today
        with open(SEEN_PATH, "w", encoding="utf-8") as fh:
            json.dump(seen, fh, indent=2, ensure_ascii=False)
        log(f"seen.json updated: {len(seen['keys'])} known records")
    else:
        log("(dry run: seen.json NOT updated -- pass --mark-seen to commit dedup state)")

    return 0


def main():
    ap = argparse.ArgumentParser(description="Paper Radar literature search")
    ap.add_argument("--since", help="ISO date lower bound (YYYY-MM-DD)")
    ap.add_argument("--days", type=int, default=7, help="lookback window if --since omitted")
    ap.add_argument("--paper", help="restrict to paper key(s), comma-separated")
    ap.add_argument("--out", help="output JSON path")
    ap.add_argument("--limit", type=int, help="max candidates per paper")
    ap.add_argument("--resume", action="store_true",
                    help="skip papers already present in --out and append")
    ap.add_argument("--budget", type=int, default=35,
                    help="stop cleanly after N seconds (default 35, to fit the "
                         "sandbox's 45s shell ceiling); 0 disables")
    ap.add_argument("--mark-seen", action="store_true",
                    help="record results in seen.json (refused unless the sweep is complete)")
    ap.add_argument("--ignore-seen", action="store_true", help="do not filter already-seen records")
    ap.add_argument("--no-s2", action="store_true", help="force-skip Semantic Scholar")
    ap.add_argument("--baseline", action="store_true", help="alias: wide first-run sweep")
    ap.add_argument("--mark-seen-from", metavar="PATH",
                    help="record a finished candidates.json in seen.json; no searching")
    args = ap.parse_args()
    if args.mark_seen_from:
        return mark_seen_from(args.mark_seen_from)
    if args.baseline and not args.since:
        args.since = "2015-01-01"
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
