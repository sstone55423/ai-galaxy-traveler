#!/usr/bin/env python3
"""
Paper Radar -- literature search for the AI Galaxy Traveler series.

Zero-dependency (stdlib only), per repo convention. Queries arXiv, OpenAlex,
Crossref and -- only if a key is present -- Semantic Scholar. Two further
channels sweep by identity rather than keyword: cites_watch (new works citing
a canon paper, via OpenAlex filter=cites:) and venue_watch (whole journals by
ISSN, via Crossref) -- both configured per paper in queries.json; see
resolve_canon.py for filling cites_watch ids. Deduplicates
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
import collections
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
DELAY = {"arxiv": 3.0, "openalex": 0.2, "crossref": 0.5, "s2": 1.1, "cites": 0.3, "venue": 0.6,
         "ads": 0.5, "ntrs": 0.5, "s2_recommend": 4.0, "arxiv_list": 0, "coupling": 0, "biorxiv": 0}

TIMEOUT = 30

# OpenAlex has required an API key since Feb 2026. Keyless callers share a
# ~$0.10/day pool that is normally exhausted before the morning run, and every
# request then 429s with "Insufficient budget ... resets at midnight UTC". A
# free key (openalex.org/settings/api) gives ~$1/day, plenty for a sweep. Put
# OPENALEX_API_KEY=... in .paper-radar/.env (same name in the book-radar).
_OPENALEX_DOWN = False


def openalex_key():
    return (os.environ.get("OPENALEX_API_KEY") or "").strip()


def oa_authors(w):
    """Author names as printed on the work, not OpenAlex's profile names.

    author.display_name is the disambiguated identity and can carry a former
    name or a wrong merge: it gave "Markus C. Kolodziej" for a paper bylined
    Markus Wagner, and "Cao Qing" for Qing Cao. raw_author_name is the byline
    string, so prefer it and fall back to the profile only when it is absent.
    """
    out = []
    for a in (w.get("authorships") or []):
        name = (a.get("raw_author_name") or "").strip()
        out.append(name or (a.get("author") or {}).get("display_name"))
    return out


def openalex_params(**kw):
    """Query params every OpenAlex call must carry: mailto plus the API key."""
    p = {"mailto": CONTACT}
    if openalex_key():
        p["api_key"] = openalex_key()
    p.update(kw)
    return p


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


_HOST_GIVEUPS = {}


def fetch(url, headers=None, retries=3):
    """GET with backoff. Returns body text, or None on give-up.

    Circuit breaker: after 3 give-ups on a host within one run (each give-up is
    a full 429-backoff cycle), further calls to that host return None
    immediately. The 2026-09-01 run lost the whole ethics sweep to OpenAlex
    429ing every attempt at ~36 s each; failing fast preserves the wall clock
    for the sources that are still answering."""
    global _OPENALEX_DOWN
    host = urllib.parse.urlsplit(url).netloc
    if host == "api.openalex.org" and _OPENALEX_DOWN:
        return None
    if _HOST_GIVEUPS.get(host, 0) >= 3:
        if _HOST_GIVEUPS.get(host) == 3:
            log(f"  ! circuit open for {host}: skipping it for the rest of this run")
            _HOST_GIVEUPS[host] = 4
        return None
    headers = dict(headers or {})
    headers.setdefault("User-Agent", UA)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                _HOST_GIVEUPS[host] = 0
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            # True exponential backoff with jitter, on both rate-limit and
            # server-error responses. Semantic Scholar's API terms ask callers
            # to apply exponential backoff specifically; the other hosts are
            # free services doing us a favour and deserve the same treatment.
            if exc.code == 429:
                body = ""
                try:
                    body = exc.read().decode("utf-8", errors="replace")
                except Exception:  # noqa: BLE001
                    pass
                if host == "api.openalex.org" and "budget" in body.lower():
                    # Daily quota gone: final for the day, no point backing off.
                    # Retrying it per query cost the 2026-09-14 run ~40 minutes
                    # and half the papers.
                    _OPENALEX_DOWN = True
                    how = ("with the configured API key -- add funds or wait for the "
                           "midnight-UTC reset" if openalex_key() else
                           "NO API KEY -- keyless access is ~$0.10/day; put "
                           "OPENALEX_API_KEY in .paper-radar/.env (free at "
                           "openalex.org/settings/api)")
                    log(f"  ! OpenAlex daily budget exhausted ({how}); "
                        f"skipping OpenAlex for the rest of this run")
                    _HOST_GIVEUPS[host] = 4
                    return None
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
    _HOST_GIVEUPS[host] = _HOST_GIVEUPS.get(host, 0) + 1
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


# Crossref and OpenAlex type strings for "a component of a book", i.e. the
# things that arrive dozens at a time when one volume is indexed.
BOOK_PART_TYPES = {
    "book-chapter", "book-part", "book-section", "book-track", "book-entry",
    "reference-entry", "book", "edited-book", "monograph", "reference-book",
    "book-series", "book-set",
}
# Deliberately excludes OpenAlex's catch-all "other", which covers far more than
# book components and would drop real work.


def container_key(rec):
    """Identify the volume a book component belongs to, or None.

    Deliberately narrow: it fires only on records whose *type* says they are a
    book component. Grouping by DOI stem alone would be wrong -- consecutive
    articles in one journal issue share a stem too (10.1016/j.actaastro.2026.08
    covers .062 and .075, two unrelated papers), and capping those would drop
    real work.
    """
    if (rec.get("cr_type") or "").lower() not in BOOK_PART_TYPES:
        return None
    doi = rec.get("doi") or ""
    # Chapter DOIs hang off the volume's DOI: 10.58830/ozgur.pub1404.c5650,
    # 10.33196/9783704699633-107, 10.1017/9781009639057.029,
    # 10.1016/b978-0-44-333941-7.00020-2, 10.1002/9781394422791.ch6
    m = re.match(r"^(10\.\d{4,9}/.+?)[.-](?:c|ch|chapter|pt|sec)?\d{1,6}(?:-\d{1,3})?$",
                 doi, re.I)
    if m:
        return "doi:" + m.group(1)
    venue = (rec.get("venue") or "").strip().lower()
    if venue and venue != "unknown venue":
        return "venue:" + venue
    return None


def cap_containers(records, cap=1):
    """Keep at most `cap` records per book volume, preserving order.

    One indexed volume can otherwise consume a paper's entire daily budget
    through its chapter records. Measured on real sweeps: 2026-09-06 gave 6 of
    the Fermi paper's 7 candidates from a single edited volume and 8 of the
    ethics paper's 21 from one monograph, including its Introduction and
    Conclusion; 2026-09-08 gave 4 of the vehicle paper's 5 from one book. The
    screeners caught every one, but each cost a full read.

    Records are already sorted best-first, so the survivor is the volume's
    strongest entry rather than an arbitrary one.
    """
    seen_containers = {}
    out, dropped = [], 0
    for rec in records:
        ck = container_key(rec)
        if ck is None:
            out.append(rec)
            continue
        n = seen_containers.get(ck, 0)
        if n >= cap:
            dropped += 1
            continue
        seen_containers[ck] = n + 1
        out.append(rec)
    if dropped:
        flooded = sum(1 for v in seen_containers.values() if v >= cap)
        log(f"      container cap: {dropped} book-component record(s) dropped "
            f"across {flooded} volume(s)")
    return out


def arxiv_index_freshness(since, stale_after_days=2):
    """How current is arXiv's *search* index? Returns a dict, or None if unknown.

    arXiv's search API can keep answering normally while its index stops taking
    new submissions, and the radar cannot tell that from a genuinely quiet week:
    both look like zero arXiv candidates. That is exactly what happened from
    2026-09-04 17:51 UTC, and it went unnoticed for five days across four
    digests because each day's zero was attributed to dedup.

    One broad query settles it. `cat:cs.AI` has submissions every weekday, so if
    its newest result is days old the index is behind, whatever the topical
    queries return. The id_list endpoint is unaffected by this and keeps working
    for verification.
    """
    probe = search_arxiv("cat:cs.AI", "2000-01-01", None, max_results=1)
    if not probe:
        return None
    newest = probe[0].get("date") or ""
    if not newest:
        return None
    try:
        lag = (dt.date.today() - dt.date.fromisoformat(newest)).days
    except ValueError:
        return None
    return {"newest": newest, "lag_days": lag, "stale": lag > stale_after_days}


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


# --- arXiv via the weekly listings ------------------------------------------
#
# The search API was the radar's arXiv channel until 2026-10-22, when an audit
# of the 2026-10-19 sweep found it had delivered 1 of 413 candidates. It times
# out or 429s from this host far more often than not, and the circuit breaker
# then drops arXiv silently for the rest of the run; the papers that lean on it
# hardest (computational, Fermi, vehicle) were the ones starved. The listing
# pages at arxiv.org/list/<cat>/pastweek answer in under a second with every
# announcement of the past five announcement days, so the channel now is:
#   1. fetch each configured category's listing once per run (cached to disk,
#      because a sweep is resumed across several invocations);
#   2. fetch abstracts in batches -- OpenAlex by arXiv DOI (37 of 40 of a
#      week's new papers had one on the test day), S2's batch endpoint for the
#      rest;
#   3. evaluate each paper's existing `arxiv` queries locally against title and
#      abstract. The queries keep their meaning; only the evaluator moved.
# This is the arXiv query, run here instead of on arXiv's server, not a
# relevance gate: the screening agents still judge everything it returns.

ARXIV_WEEK_PATH = os.path.join(HERE, "arxiv_week.json")
_LIST_ENTRY = re.compile(
    r"<h3>(?P<day>[^<]*)</h3>|<dt>.*?/abs/(?P<id>\d{4}\.\d{4,5})\".*?</dt>\s*<dd>(?P<dd>.*?)</dd>",
    re.S)


def _listing_day(h3):
    """'Fri, 23 Oct 2026 (showing ...)' -> '2026-10-23', or ''."""
    m = re.search(r"(\d{1,2}) (\w{3}) (\d{4})", h3 or "")
    if not m:
        return ""
    try:
        return dt.datetime.strptime(" ".join(m.groups()), "%d %b %Y").date().isoformat()
    except ValueError:
        return ""


def fetch_arxiv_listing(cat):
    """Every entry announced in `cat` over the past week: {id: record}."""
    out = {}
    skip = 0
    while True:
        body = fetch(f"https://arxiv.org/list/{cat}/pastweek?skip={skip}&show=2000")
        if not body:
            break
        day = ""
        n = 0
        for m in _LIST_ENTRY.finditer(body):
            if m.group("day") is not None:
                day = _listing_day(m.group("day"))
                continue
            n += 1
            dd = m.group("dd")
            t = re.search(r"list-title[^>]*>.*?</span>(.*?)</div>", dd, re.S)
            a = re.search(r"list-authors[^>]*>(.*?)</div>", dd, re.S)
            s = re.search(r"list-subjects[^>]*>.*?</span>(.*?)</div>", dd, re.S)
            aid = m.group("id")
            out.setdefault(aid, {
                "source": "arxiv",
                "title": clean_ws(strip_tags(t.group(1))) if t else "",
                "authors": [clean_ws(strip_tags(x)) for x in
                            re.findall(r"<a [^>]*>(.*?)</a>", a.group(1))] if a else [],
                "date": day,
                "year": int(day[:4]) if day[:4].isdigit() else None,
                "venue": "arXiv preprint",
                "doi": None,
                "arxiv_id": aid,
                "url": f"https://arxiv.org/abs/{aid}",
                "abstract": "",
                "categories": re.findall(r"\(([a-z\-]+(?:\.[A-Za-z\-]+)?)\)",
                                         strip_tags(s.group(1))) if s else [cat],
            })
        total = re.search(r"Total of (\d+) entries", body)
        skip += 2000
        if not total or skip >= int(total.group(1)) or n == 0:
            break
        time.sleep(1.0)
    return out


def _past(deadline):
    return deadline is not None and time.monotonic() > deadline


def fill_arxiv_abstracts(records, deadline=None):
    """Abstracts for listing records, in batches: OpenAlex first, then S2.

    Resumable: each record is marked once a source has been asked about it, so
    a call cut short by the deadline picks up where it stopped. Returns True
    once both passes have covered every record."""
    need = [r for r in records.values() if not r.get("abstract") and not r.get("_oa_tried")]
    for i in range(0, len(need), 50):
        if _past(deadline):
            return False
        batch = need[i:i + 50]
        chunk = {"10.48550/arxiv." + r["arxiv_id"]: r for r in batch}
        body = fetch("https://api.openalex.org/works?" + urllib.parse.urlencode(
            openalex_params(**{"filter": "doi:" + "|".join(chunk),
                               "select": "doi,abstract_inverted_index",
                               "per-page": 50})))
        time.sleep(0.3)
        for r in batch:
            r["_oa_tried"] = True
        if not body:
            continue
        try:
            for w in json.loads(body).get("results", []):
                rec = chunk.get(norm_doi(w.get("doi")) or "")
                if rec is not None:
                    rec["abstract"] = clean_ws(reconstruct_abstract(
                        w.get("abstract_inverted_index")))[:1500]
        except json.JSONDecodeError:
            continue
    s2_key = os.environ.get("S2_API_KEY")
    still = [r for r in records.values() if not r.get("abstract") and not r.get("_s2_tried")]
    for i in range(0, len(still), 500):
        if not s2_key:
            break
        if _past(deadline):
            return False
        chunk = still[i:i + 500]
        rows = None
        for attempt in range(2):  # S2 allows 1 req/s; one retry after a 429
            try:
                req = urllib.request.Request(
                    "https://api.semanticscholar.org/graph/v1/paper/batch?fields=abstract",
                    data=json.dumps({"ids": ["ARXIV:" + r["arxiv_id"] for r in chunk]}).encode(),
                    headers={"x-api-key": s2_key, "Content-Type": "application/json",
                             "User-Agent": UA})
                with urllib.request.urlopen(req, timeout=TIMEOUT * 2) as resp:
                    rows = json.loads(resp.read().decode("utf-8"))
                break
            except Exception as exc:  # noqa: BLE001 -- best-effort enrichment
                log(f"  [arxiv] S2 abstract batch failed ({exc})"
                    + ("; retrying" if attempt == 0 else ""))
                time.sleep(5)
        for r in chunk:
            r["_s2_tried"] = True
        if rows is None:
            break
        for rec, row in zip(chunk, rows):
            if row and row.get("abstract"):
                rec["abstract"] = clean_ws(row["abstract"])[:1500]
        time.sleep(1.1)
    return True


def _save_arxiv_week(cache):
    with open(ARXIV_WEEK_PATH, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False)


def load_arxiv_week(categories, refresh=False, deadline=None):
    """The week's listings for `categories`, abstracts filled, cached per day.

    Returns (records, failed_categories, ready). The scheduled run works in
    slices of at most 180 s (device-shell limit), and a full load -- ~23
    listings plus ~80 abstract batches -- takes several minutes, so progress is
    saved after every category and abstract pass, and a slice that reaches its
    deadline returns ready=False for the next --resume call to continue."""
    today = dt.date.today().isoformat()
    cache = {} if refresh else load_json(ARXIV_WEEK_PATH, {})
    if cache.get("fetched") != today or not set(categories) <= set(cache.get("wanted") or []):
        cache = {"fetched": today, "wanted": sorted(set(categories)),
                 "done": [], "failed": [], "records": {}, "complete": False}
    if cache.get("complete"):
        return cache["records"], cache["failed"], True
    records = cache["records"]
    for cat in cache["wanted"]:
        if cat in cache["done"]:
            continue
        if _past(deadline):
            _save_arxiv_week(cache)
            log(f"  [arxiv] budget reached after {len(cache['done'])}/{len(cache['wanted'])} "
                f"listings; resume to continue")
            return records, cache["failed"], False
        got = fetch_arxiv_listing(cat)
        if not got:
            cache["failed"].append(cat)
        for aid, rec in got.items():
            if aid in records:
                records[aid]["categories"] = sorted(
                    set(records[aid]["categories"]) | set(rec["categories"]))
            else:
                records[aid] = rec
        cache["done"].append(cat)
        log(f"  [arxiv] {cat:16s} {len(got):5d} listed")
        time.sleep(1.0)
    _save_arxiv_week(cache)
    if not fill_arxiv_abstracts(records, deadline):
        _save_arxiv_week(cache)
        with_abs = sum(1 for r in records.values() if r.get("abstract"))
        log(f"  [arxiv] budget reached while filling abstracts ({with_abs}/{len(records)}); "
            f"resume to continue")
        return records, cache["failed"], False
    cache["complete"] = True
    _save_arxiv_week(cache)
    with_abs = sum(1 for r in records.values() if r.get("abstract"))
    log(f"  [arxiv] {len(records)} unique this week, {with_abs} with abstracts"
        + (f"; listing FAILED for {', '.join(cache['failed'])}" if cache["failed"] else ""))
    return records, cache["failed"], True


def _norm_match_text(text):
    return " " + re.sub(r"[^a-z0-9]+", " ", (text or "").lower()) + " "


def _arxiv_tokens(query):
    return re.findall(r'\(|\)|"[^"]*"|[^\s()"]+', query)


def arxiv_query_matches(query, text):
    """Evaluate an arXiv-style boolean query (quoted phrases, bare words, AND,
    OR, ANDNOT, parentheses; AND binds tighter than OR) against `text`.
    Matching is case-insensitive, hyphens and punctuation count as spaces, and
    a bare word also matches its plural/inflected forms (up to 3 trailing
    letters), roughly as arXiv's own stemmer does."""
    toks = _arxiv_tokens(query)
    hay = _norm_match_text(text)
    pos = 0

    def term(tok):
        words = _norm_match_text(tok.strip('"')).split()
        if not words:
            return False
        # every word, in a phrase or bare, takes inflected endings, as arXiv's
        # stemmed search does ("magnetic sail" finds "magnetic sails")
        pat = " " + " ".join(re.escape(w) + "[a-z]{0,3}" for w in words) + " "
        return re.search(pat, hay) is not None

    def peek():
        return toks[pos] if pos < len(toks) else None

    def atom():
        nonlocal pos
        tok = peek()
        if tok is None:
            return False
        pos += 1
        if tok == "(":
            v = expr()
            if peek() == ")":
                pos += 1
            return v
        return term(tok)

    def conj():
        nonlocal pos
        v = atom()
        while peek() in ("AND", "ANDNOT"):
            op = toks[pos]
            pos += 1
            rhs = atom()
            v = (v and rhs) if op == "AND" else (v and not rhs)
        return v

    def expr():
        nonlocal pos
        v = conj()
        while peek() == "OR":
            pos += 1
            v = conj() or v
        return v

    return expr()


def match_arxiv_week(paper, week, since):
    """Records from the week's listings matching any of the paper's queries."""
    cats = set(paper.get("arxiv_categories") or [])
    out = []
    for rec in week.values():
        if rec.get("date") and rec["date"] < since:
            continue
        if cats and not cats & set(rec.get("categories") or []):
            continue
        text = rec.get("title", "") + " " + rec.get("abstract", "")
        for q in paper.get("arxiv", []):
            if arxiv_query_matches(q, text):
                hit = {k: v for k, v in rec.items() if not k.startswith("_")}
                hit["matched_query"] = q
                out.append(hit)
                break
    return out


# --- coupling: new works that cite the series' own references ---------------
#
# Keyword queries miss work phrased in another field's vocabulary; a paper that
# cites what this series cites does not depend on wording. series_refs.json
# (build_series_refs.py) holds the series' reference lists resolved to OpenAlex
# ids. One sweep-wide pass asks OpenAlex for every work published in the window
# that cites any of them, and keeps a work for a paper when it cites at least
# two series references, or one niche reference (fewer than COUPLING_NICHE
# citations): on the 2026-10-08..22 test that kept 17 of 128 citing works --
# Perry et al. (citing six series references), Yang et al., Bennu and Ryugu
# water studies, a speciation-continuum genomics paper citing Hissa -- while a
# single citation of Shannon 1948 or Hardin 1968 is not taken as a signal.

SERIES_REFS_PATH = os.path.join(HERE, "series_refs.json")
COUPLING_NICHE = 300


def search_coupling(since):
    """{paper_key: [records]} for works in the window coupled to the series."""
    seeds = {r["id"]: r for r in (load_json(SERIES_REFS_PATH, {}).get("refs") or [])
             if r.get("id")}
    if not seeds:
        log("  [coupling] no series_refs.json -- run build_series_refs.py; skipped")
        return {}
    works = {}
    ids = list(seeds)
    for i in range(0, len(ids), 50):
        cursor = "*"
        while cursor:
            body = fetch("https://api.openalex.org/works?" + urllib.parse.urlencode(
                openalex_params(**{
                    "filter": f"cites:{'|'.join(ids[i:i + 50])},from_publication_date:{since}",
                    "select": "id,doi,title,publication_date,publication_year,authorships,"
                              "primary_location,abstract_inverted_index,referenced_works,type",
                    "per-page": 200, "cursor": cursor})))
            time.sleep(DELAY["openalex"])
            if not body:
                break
            try:
                page = json.loads(body)
            except json.JSONDecodeError:
                break
            for w in page.get("results", []):
                works[w["id"]] = w
            cursor = page.get("meta", {}).get("next_cursor") if page.get("results") else None

    out = collections.defaultdict(list)
    for w in works.values():
        hit = [x.rsplit("/", 1)[-1] for x in (w.get("referenced_works") or [])]
        hit = [x for x in hit if x in seeds]
        niche = [x for x in hit if (seeds[x].get("cited_by") or 10 ** 9) < COUPLING_NICHE]
        if len(hit) < 2 and not niche:
            continue
        loc = w.get("primary_location") or {}
        src = loc.get("source") or {}
        labels = ", ".join(f"{seeds[x]['author']} {seeds[x]['year']}" for x in hit[:4])
        papers = sorted({p for x in hit for p in seeds[x].get("papers", [])})
        for pk in papers:
            out[pk].append({
                "source": "coupling",
                "title": clean_ws(w.get("title")),
                "authors": oa_authors(w)[:12],
                "date": w.get("publication_date") or "",
                "year": w.get("publication_year"),
                "venue": src.get("display_name") or "unknown venue",
                "doi": norm_doi(w.get("doi")),
                "arxiv_id": None,
                "url": w.get("doi") or (loc.get("landing_page_url") or ""),
                "abstract": reconstruct_abstract(w.get("abstract_inverted_index"))[:1500],
                "coupling": len(hit),
                "matched_query": f"cites {len(hit)} series ref(s): {labels}",
            })
    log(f"  [coupling] {len(works)} works cite a series reference since {since}; "
        f"{sum(len(v) for v in out.values())} kept across {len(out)} papers")
    return dict(out)


# --- sources added 2026-10-22 (radar audit) ----------------------------------
#
# Each is configured per paper in queries.json and tested live before wiring:
#   ads        ADS keyword search -- reaches JBIS, IAC, LPSC abstracts and NASA
#              NIAC/contractor reports that no other channel indexes (30 days:
#              a NIAC metamaterial-sail report, "Pulsars as natural launchers
#              of interstellar probes", 28 technosignature papers). ADS syntax.
#   ntrs       NASA Technical Reports Server -- engineering reports with real
#              numbers (ISRU, fission surface power, mass drivers).
#   biorxiv    the week's bioRxiv postings (~1,500, with abstracts), category-
#              filtered and matched locally with arXiv-style queries, like the
#              arXiv listings; preprints otherwise reach OpenAlex late and bare.
#   s2_recommend  Semantic Scholar recommendations seeded with the paper's own
#              DOI references; strong for the DNA mission-ledger paper (Perry
#              et al., ProbeFS), weak for routing -- capped, and judged by
#              yield_report.py over time.

def search_ads(query, since, rows=20):
    token = os.environ.get("ADS_API_TOKEN")
    if not token:
        return []
    q = f"({query}) entdate:[{since} TO *]"
    body = fetch("https://api.adsabs.harvard.edu/v1/search/query?" + urllib.parse.urlencode(
        {"q": q, "rows": rows, "sort": "date desc",
         "fl": "title,author,pubdate,doi,bibcode,abstract,pub,identifier"}),
        headers={"Authorization": f"Bearer {token}"})
    if not body:
        return []
    try:
        docs = json.loads(body).get("response", {}).get("docs", [])
    except json.JSONDecodeError:
        return []
    out = []
    for d in docs:
        pubdate = (d.get("pubdate") or "").replace("-00", "-01")
        arxiv = next((x.split(":", 1)[1] for x in d.get("identifier") or []
                      if x.lower().startswith("arxiv:")), None)
        out.append({
            "source": "ads",
            "title": clean_ws((d.get("title") or [""])[0]),
            "authors": (d.get("author") or [])[:12],
            "date": pubdate,
            "year": int(pubdate[:4]) if pubdate[:4].isdigit() else None,
            "venue": d.get("pub") or "ADS",
            "doi": norm_doi((d.get("doi") or [None])[0]),
            "arxiv_id": arxiv,
            "url": f"https://ui.adsabs.harvard.edu/abs/{d.get('bibcode')}",
            "abstract": clean_ws(d.get("abstract") or "")[:1500],
        })
    return out


def search_ntrs(query, since, size=15):
    body = fetch("https://ntrs.nasa.gov/api/citations/search?" + urllib.parse.urlencode(
        {"q": query, "published.gte": since, "page.size": size}))
    if not body:
        return []
    try:
        results = json.loads(body).get("results", [])
    except json.JSONDecodeError:
        return []
    out = []
    for r in results:
        pubs = r.get("publications") or []
        date = ((pubs[0].get("publicationDate") if pubs else None)
                or r.get("distributionDate") or "")[:10]
        authors = [((a.get("meta") or {}).get("author") or {}).get("name")
                   for a in r.get("authorAffiliations") or []]
        out.append({
            "source": "ntrs",
            "title": clean_ws(r.get("title")),
            "authors": [a for a in authors if a][:12],
            "date": date,
            "year": int(date[:4]) if date[:4].isdigit() else None,
            "venue": f"NASA NTRS ({r.get('stiTypeDetails') or r.get('stiType') or 'report'})",
            "doi": norm_doi((pubs[0].get("doi") if pubs else None)),
            "arxiv_id": None,
            "url": f"https://ntrs.nasa.gov/citations/{r.get('id')}",
            "abstract": clean_ws(r.get("abstract") or "")[:1500],
        })
    return out


BIORXIV_CATEGORIES = {"bioinformatics", "synthetic biology", "bioengineering",
                      "evolutionary biology", "genomics", "genetics", "ecology",
                      "systems biology", "biophysics", "molecular biology"}


BIORXIV_WEEK_PATH = os.path.join(HERE, "biorxiv_week.json")


def load_biorxiv_week(since, deadline=None):
    """The window's bioRxiv postings in BIORXIV_CATEGORIES, with abstracts.

    Returns (records, ready). ~1,500 postings a week arrive 30 per request, so
    the harvest outlasts one 180 s device-shell slice; the cursor and records
    are cached per day and a slice that reaches its deadline returns
    ready=False for the next --resume call to continue."""
    today = dt.date.today().isoformat()
    until = today
    cache = load_json(BIORXIV_WEEK_PATH, {})
    if cache.get("fetched") != today or cache.get("since") != since:
        cache = {"fetched": today, "since": since, "cursor": 0, "records": {}, "complete": False}
    out = cache["records"]
    while not cache["complete"]:
        if _past(deadline):
            with open(BIORXIV_WEEK_PATH, "w", encoding="utf-8") as fh:
                json.dump(cache, fh, ensure_ascii=False)
            log(f"  [biorxiv] budget reached at posting {cache['cursor']}; resume to continue")
            return out, False
        body = fetch(f"https://api.biorxiv.org/details/biorxiv/{since}/{until}/{cache['cursor']}")
        if not body:
            cache["complete"] = True
            break
        try:
            page = json.loads(body)
        except json.JSONDecodeError:
            cache["complete"] = True
            break
        coll = page.get("collection") or []
        for c in coll:
            if (c.get("category") or "").lower() not in BIORXIV_CATEGORIES:
                continue
            out[c["doi"]] = {
                "source": "biorxiv",
                "title": clean_ws(c.get("title")),
                "authors": [a.strip() for a in (c.get("authors") or "").split(";") if a.strip()][:12],
                "date": c.get("date") or "",
                "year": int(c["date"][:4]) if (c.get("date") or "")[:4].isdigit() else None,
                "venue": f"bioRxiv preprint ({c.get('category')})",
                "doi": norm_doi(c.get("doi")),
                "arxiv_id": None,
                "url": f"https://www.biorxiv.org/content/{c.get('doi')}",
                "abstract": clean_ws(c.get("abstract") or "")[:1500],
            }
        msg = (page.get("messages") or [{}])[0]
        total = int(msg.get("total") or 0)
        cache["cursor"] += int(msg.get("count") or len(coll) or 0)
        if not coll or cache["cursor"] >= total:
            cache["complete"] = True
        time.sleep(0.5)
    with open(BIORXIV_WEEK_PATH, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False)
    log(f"  [biorxiv] {len(out)} postings in the watched categories since {since}")
    return out, True


def match_local(paper, pool, queries_key):
    """Records from `pool` matching any of the paper's `queries_key` queries."""
    out = []
    for rec in pool.values():
        text = rec.get("title", "") + " " + rec.get("abstract", "")
        for q in paper.get(queries_key, []):
            if arxiv_query_matches(q, text):
                hit = {k: v for k, v in rec.items() if not k.startswith("_")}
                hit["matched_query"] = q
                out.append(hit)
                break
    return out


def search_s2_recommend(paper_key, since, limit=10):
    """Recent papers S2 recommends from the paper's own DOI references."""
    key = os.environ.get("S2_API_KEY")
    refs = (load_json(SERIES_REFS_PATH, {}).get("refs") or [])
    seeds = ["DOI:" + r["doi"] for r in refs if paper_key in r.get("papers", []) and r.get("doi")]
    if not key or len(seeds) < 3:
        return []
    recs = None
    # The recommendations endpoint 429s far more readily than the batch one:
    # at 1.2 s spacing half the calls failed on the 2026-10-22 test. Back off.
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                "https://api.semanticscholar.org/recommendations/v1/papers"
                "?fields=title,authors,publicationDate,externalIds,venue,abstract&limit=40",
                data=json.dumps({"positivePaperIds": seeds[:50]}).encode(),
                headers={"x-api-key": key, "Content-Type": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT * 2) as resp:
                recs = json.loads(resp.read().decode("utf-8")).get("recommendedPapers", [])
            break
        except Exception as exc:  # noqa: BLE001
            if attempt == 2:
                log(f"  [s2_recommend] {paper_key}: {exc}; skipped")
                return []
            time.sleep(6 * (attempt + 1))
    out = []
    for p in recs:
        date = p.get("publicationDate") or ""
        if not date or date < since:
            continue
        ext = p.get("externalIds") or {}
        out.append({
            "source": "s2_recommend",
            "title": clean_ws(p.get("title")),
            "authors": [a.get("name") for a in p.get("authors") or [] if a.get("name")][:12],
            "date": date,
            "year": int(date[:4]),
            "venue": p.get("venue") or "unknown venue",
            "doi": norm_doi(ext.get("DOI")),
            "arxiv_id": ext.get("ArXiv"),
            "url": f"https://www.semanticscholar.org/paper/{p.get('paperId')}",
            "abstract": clean_ws(p.get("abstract") or "")[:1500],
        })
        if len(out) >= limit:
            break
    return out


def search_openalex(query, since, per_page=10):
    # sort=relevance_score:desc is load-bearing. Sorting by publication_date
    # returns whatever is NEWEST rather than whatever is RELEVANT, which in
    # testing meant microalgae wastewater papers under a Fermi-paradox query.
    # Relevance-sort then date-filter; never date-sort.
    # (title_and_abstract.search is more precise but far too strict here --
    # it cut one query from 1447 matches to 1.)
    params = urllib.parse.urlencode(openalex_params(**{
        "search": query,
        "filter": f"from_publication_date:{since}",
        "per-page": per_page,
        "sort": "relevance_score:desc",
    }))
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
        authors = oa_authors(w)
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
            "cr_type": w.get("type") or "",
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
            "cr_type": it.get("type") or "",
        })
    return out


def search_openalex_cites(spec, since, per_page=15):
    """Citation watch: new works citing a canon paper. spec is "W<id>|<label>".

    Unlike keyword search, date-sort is CORRECT here: the citing set is already
    topical by construction, and we want whatever cited the canon work most
    recently. Skips gracefully if the id is unresolved (null/empty)."""
    wid, _, label = spec.partition("|")
    if not wid.startswith("W"):
        return []
    params = urllib.parse.urlencode(openalex_params(**{
        "filter": f"cites:{wid},from_publication_date:{since}",
        "per-page": per_page,
        "sort": "publication_date:desc",
    }))
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
        authors = oa_authors(w)
        out.append({
            "source": "cites",
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
            "cr_type": w.get("type") or "",
            "oa_url": (w.get("best_oa_location") or {}).get("pdf_url"),
            "cites_canon": label,
        })
    return out


def search_crossref_venue(spec, since, rows=15):
    """Venue watch: everything a named journal published since `since`.
    spec is "ISSN1;ISSN2|<venue name>|<gate1;gate2;...>". Multiple ISSNs
    (print+online) are OR'd, which is Crossref's semantics for a repeated
    filter key.

    The optional third field is a subject gate: a venue hit is kept only if one
    of its terms appears in the title or abstract. Without it a venue feed is
    keyword-blind, which is the point for a narrow journal but ruinous for a
    broad one -- on 2026-09-04 and 09-05 the Futures ISSN feed supplied 4 of 5
    and then 4 of 4 of the Fermi paper's candidates, every one a
    foresight-methodology table-of-contents entry with no subject-side match.
    Gating beats deleting the feed: Futures does occasionally publish
    Fermi-adjacent work. An empty gate preserves the old keyword-blind
    behaviour."""
    issns, _, rest = spec.partition("|")
    vname, _, gate = rest.partition("|")
    gate_terms = [g.strip().lower() for g in gate.split(";") if g.strip()]
    flt = ",".join(f"issn:{i}" for i in issns.split(";") if i)
    if not flt:
        return []
    params = urllib.parse.urlencode({
        "filter": f"{flt},from-pub-date:{since}",
        "rows": rows,
        "select": "title,issued,container-title,DOI,author,abstract,type",
        "sort": "published", "order": "desc",
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
        if it.get("type") in ("component", "dataset", "journal-issue"):
            continue
        _doi = (it.get("DOI") or "").lower()
        if _doi.endswith((".fmatter", ".index", ".oth", ".ind", ".toc")):
            continue
        parts = (it.get("issued") or {}).get("date-parts") or [[]]
        dp = parts[0] if parts else []
        year = dp[0] if dp else None
        date = "-".join(f"{p:02d}" if i else str(p) for i, p in enumerate(dp)) if dp else ""
        authors = [clean_ws(f"{a.get('given', '')} {a.get('family', '')}")
                   for a in (it.get("author") or [])]
        titles = it.get("title") or []
        out.append({
            "source": "venue",
            "title": clean_ws(titles[0] if titles else ""),
            "authors": [a for a in authors if a][:12],
            "date": date,
            "year": year,
            "venue": vname,
            "doi": norm_doi(it.get("DOI")),
            "arxiv_id": None,
            "url": f"https://doi.org/{it.get('DOI')}" if it.get("DOI") else "",
            "abstract": clean_ws(strip_tags(it.get("abstract", "")))[:1500],
            "cr_type": it.get("type") or "",
        })
    # Elsevier journals rarely deposit abstracts to Crossref, which left the
    # 2026-08-31 venue sweep dumping title-only ToC batches on the screeners
    # (16/18 vehicle candidates, 15/18 Fermi). Best-effort enrichment: fill
    # missing abstracts from OpenAlex by DOI, fault-tolerant.
    #
    # Asked in batches: OpenAlex's `filter=doi:a|b|c` takes 50 at a time, so a
    # whole ToC costs one request instead of one per record. The old per-record
    # loop had to be capped at 12 to stay inside the time budget, which is why
    # the 2026-10-12 digest still reported abstract-missing hits from Acta
    # Astronautica and Futures -- the gate below was judging the remainder on
    # their titles alone.
    missing = {rec["doi"]: rec for rec in out if rec["doi"] and not rec["abstract"]}
    dois = list(missing)
    for i in range(0, len(dois), 50):
        chunk = dois[i:i + 50]
        oa = fetch("https://api.openalex.org/works?" + urllib.parse.urlencode(
            openalex_params(**{"filter": "doi:" + "|".join(chunk),
                               "select": "doi,abstract_inverted_index",
                               "per-page": 50})))
        time.sleep(0.3)
        if not oa:
            continue
        try:
            found = json.loads(oa).get("results", [])
        except json.JSONDecodeError:
            continue
        for w in found:
            doi = norm_doi(w.get("doi"))
            rec = missing.get(doi)
            if not rec:
                continue
            ab = reconstruct_abstract(w.get("abstract_inverted_index"))
            if ab:
                rec["abstract"] = ab[:1500]
    enriched = sum(1 for rec in missing.values() if rec["abstract"])
    if missing:
        log(f"      venue abstracts: filled {enriched} of {len(missing)} from OpenAlex")
    # Gate AFTER enrichment, so a record whose abstract only exists in OpenAlex
    # is still judged on it rather than on its title alone.
    if gate_terms:
        kept = []
        for rec in out:
            hay = (rec["title"] + " " + rec["abstract"]).lower()
            if any(t in hay for t in gate_terms):
                kept.append(rec)
        if len(out) != len(kept):
            log(f"      venue gate: {len(out) - len(kept)} of {len(out)} dropped "
                f"(no subject match in {vname})")
        return kept
    return out


def search_ads_citations(bibcode, label, since):
    """NASA ADS citation watch: works citing a canon bibcode, newly indexed
    since `since` (entdate catches back-dated ingests, which matters for the
    conference and JBIS material ADS ingests late). Requires ADS_API_TOKEN in
    .paper-radar/.env; returns [] quietly without one."""
    token = os.environ.get("ADS_API_TOKEN")
    if not token or not bibcode:
        return []
    params = urllib.parse.urlencode({
        "q": f"citations(bibcode:{bibcode}) entdate:[{since} TO *]",
        "fl": "bibcode,title,year,author,pub,doi,abstract,pubdate",
        "rows": 15, "sort": "date desc",
    })
    body = fetch(f"https://api.adsabs.harvard.edu/v1/search/query?{params}",
                 headers={"Authorization": f"Bearer {token}"})
    if not body:
        return []
    try:
        docs = json.loads(body).get("response", {}).get("docs", [])
    except json.JSONDecodeError:
        return []
    out = []
    for d in docs:
        dois = d.get("doi") or []
        date = (d.get("pubdate") or "").replace("-00", "-01")
        out.append({
            "source": "ads",
            "title": clean_ws((d.get("title") or [""])[0]),
            "authors": (d.get("author") or [])[:12],
            "date": date,
            "year": d.get("year"),
            "venue": clean_ws(d.get("pub") or "unknown venue"),
            "doi": norm_doi(dois[0]) if dois else None,
            "arxiv_id": None,
            "url": f"https://ui.adsabs.harvard.edu/abs/{d.get('bibcode')}/abstract",
            "abstract": clean_ws(d.get("abstract") or "")[:1500],
            "cites_canon": label,
        })
    return out


def search_cites(spec, since):
    """Dispatch a citation-watch entry: spec is "Wid|bibcode|label". Prefer the
    ADS graph (better for the pre-DOI canon) when a bibcode and token exist;
    fall back to OpenAlex filter=cites: when only a W-id is resolved; skip
    quietly when neither is."""
    parts = spec.split("|", 2)
    wid, bibcode, label = (parts + ["", "", ""])[:3]
    if bibcode and os.environ.get("ADS_API_TOKEN"):
        return search_ads_citations(bibcode, label, since)
    if wid.startswith("W"):
        return search_openalex_cites(f"{wid}|{label}", since)
    return []


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


# Abstracts are untrusted upstream text, and they reach the screening agents as
# prose. On 2026-10-19 an OpenAlex record (a real article, doi
# 10.68258/ajah_phileth.63877) carried a coding agent's task prompt in its
# abstract field -- markdown headings, a numbered "Rules" list, "Do not ..."
# lines, file paths. An abstract that reads as an instruction is a prompt-
# injection vector, so score each one for instruction-like markers and
# quarantine (blank) any that cross the threshold. The screener then treats it
# as a missing abstract, which SKILL.md already says to judge as `consider`.
# Strong markers have no business in an abstract and quarantine on their own;
# weak ones also occur in AI-safety prose ("the system prompt", "your task")
# and need a second, structural marker before they count.
_INJECT_STRONG = re.compile(
    r"ignore (?:all |any |the )?(?:previous|prior|above|earlier) (?:instructions|prompts?)"
    r"|disregard (?:all |any |the )?(?:previous|prior|above) (?:instructions|prompts?|text)"
    r"|\byou are now\b|\[/?inst\]|<\|im_start\||<\|endoftext\|>"
    r"|\b(?:respond|reply|answer) only with\b",
    re.I)
_INJECT_WEAK = re.compile(
    r"\byour (?:task|role|job|objective) is\b|\bas an ai\b|\bassistant:|\buser:"
    r"|\bfollow (?:these|the following) (?:steps|instructions|rules)\b"
    r"|\bbefore making (?:any )?changes\b|\bgit status\b"
    r"|\b(?:stage|commit|push)\b.{0,40}\bgit\b",
    re.I)
_MD_HEADING = re.compile(r"(?:^|\s)#{1,6} [A-Z]")
_DO_NOT = re.compile(r"\b(?:do not|don't|never)\s+(?:overwrite|modify|change|add|introduce|reveal|mention|tell|output|include|use|run|delete)\b", re.I)
_CODE_PATH = re.compile(r"[\w/\.-]+\.(?:js|ts|tsx|py|css|html|json|ya?ml|md|sh|ps1)\b|[A-Za-z]:\\?\w|`[^`]{2,60}`")
_YOU = re.compile(r"\byou(?:r|rs)?\b", re.I)


def abstract_injection_score(text):
    """Count instruction-like markers in an abstract; 0 for ordinary prose."""
    if not text:
        return 0, []
    why = []
    strong = len(_INJECT_STRONG.findall(text))
    weak = len(_INJECT_WEAK.findall(text))
    if strong:
        why.append(f"{strong} override phrase(s)")
    if weak:
        why.append(f"{weak} instruction phrase(s)")
    structural = 0
    if len(_MD_HEADING.findall(text)) >= 2:
        why.append("markdown headings")
        structural += 1
    if len(_DO_NOT.findall(text)) >= 2:
        why.append("repeated 'do not' directives")
        structural += 1
    if len(_CODE_PATH.findall(text)) >= 3:
        why.append("file paths / code spans")
        structural += 1
    words = max(1, len(text.split()))
    if words >= 40 and len(_YOU.findall(text)) / words > 0.02:
        why.append("second-person address")
        structural += 1
    return 2 * strong + min(weak, 2) + structural, why


def quarantine_abstract(rec, threshold=2):
    """Blank an abstract that reads as an instruction; True if quarantined."""
    score, why = abstract_injection_score(rec.get("abstract") or "")
    if score < threshold:
        return False
    rec["abstract"] = ""
    rec["abstract_quarantined"] = "; ".join(why)
    return True


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
        if not quarantine_abstract(incoming):
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


CANDIDATE_ARCHIVE = os.path.join(HERE, "candidates")


def seen_entry(rec, paper_key, today, prior=None):
    """The seen.json record for a candidate. Carries the channel that found it
    and its identifiers, so yield per channel can be measured later
    (yield_report.py); keeps the original first_seen if already known."""
    return {
        "first_seen": (prior or {}).get("first_seen") or today,
        "paper": paper_key,
        "title": (rec.get("title") or "")[:120],
        "found_via": (rec.get("found_via") or "")[:160],
        "doi": rec.get("doi"),
        "arxiv_id": rec.get("arxiv_id"),
    }


def archive_candidates(payload, today):
    """Keep every completed sweep, gzipped, for yield_report.py. The 2026-10-22
    radar audit could measure only one week because candidate files were
    deleted after each run."""
    import gzip
    os.makedirs(CANDIDATE_ARCHIVE, exist_ok=True)
    path = os.path.join(CANDIDATE_ARCHIVE, f"{today}.json.gz")
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    log(f"candidates archived -> {path}")


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
            prior_entry = seen.setdefault("keys", {}).get(rk)
            if prior_entry is None:
                added += 1
            seen["keys"][rk] = seen_entry(rec, key, today, prior_entry)
    seen["last_run"] = today
    archive_candidates(payload, today)
    with open(SEEN_PATH, "w", encoding="utf-8") as fh:
        json.dump(seen, fh, indent=2, ensure_ascii=False)
    log(f"seen.json: +{added} new, {len(seen['keys'])} known total, last_run={today}")
    print(json.dumps({"status": "marked", "added": added, "total": len(seen["keys"])}))
    return 0


def backfill_abstracts(results, budget_s=30, s2_cap=25):
    """Fill in the abstracts Crossref never deposited, series-wide.

    The venue sweep has enriched its own hits since 2026-08-31, but the
    ordinary query paths never did, and the 2026-10-19 sweep said plainly what
    that costs: "many Crossref records arrived with no abstract at all, which
    forced otherwise-judgeable candidates down to flagged. Backfilling
    abstracts from OpenAlex for Crossref-sourced records would raise screening
    yield more than any query change." A screening agent cannot judge what it
    cannot read, so an abstract-less record can only ever be flagged.

    OpenAlex is asked in batches -- `filter=doi:a|b|c` takes 50 at a time, so
    the whole sweep's backlog costs two or three requests. Only what OpenAlex
    still lacks falls through to S2, one request each and therefore capped.
    Filled records carry `abstract_backfilled` so the digest can say where it
    came from.

    The book radar has run the same pass since 2026-10-12, where it converted
    a third to a half of its abstract-less records and took that week's reads
    from 44 to 27 while cites rose from 26 to 37."""
    by_doi = {}
    for paper in results.values():
        for rec in paper.get("candidates", []):
            if (rec.get("abstract") or "").strip():
                continue
            if rec.get("doi"):
                by_doi.setdefault(rec["doi"], []).append(rec)
    if not by_doi:
        return 0, 0

    started = time.monotonic()
    filled = 0

    def apply(doi, abstract, src):
        nonlocal filled
        if not abstract:
            return
        # A backfilled abstract is as untrusted as a harvested one, and it
        # arrives after the intake-time quarantine has already run.
        score, why = abstract_injection_score(abstract)
        if score >= 2:
            for rec in by_doi.get(doi, []):
                rec["abstract_quarantined"] = "backfill: " + "; ".join(why)
            log(f"  ! backfilled abstract quarantined for {doi} ({'; '.join(why)})")
            return
        filled += 1
        for rec in by_doi.get(doi, []):
            rec["abstract"] = abstract[:1500]
            rec["abstract_backfilled"] = src

    dois = list(by_doi)
    for i in range(0, len(dois), 50):
        if time.monotonic() - started > budget_s:
            break
        chunk = dois[i:i + 50]
        body = fetch("https://api.openalex.org/works?" + urllib.parse.urlencode(
            openalex_params(**{"filter": "doi:" + "|".join(chunk),
                               "select": "doi,abstract_inverted_index",
                               "per-page": 50})))
        time.sleep(0.3)
        if not body:
            continue
        try:
            found = json.loads(body).get("results", [])
        except json.JSONDecodeError:
            continue
        for w in found:
            apply(norm_doi(w.get("doi")),
                  clean_ws(reconstruct_abstract(w.get("abstract_inverted_index"))),
                  "openalex")

    s2_key = os.environ.get("S2_API_KEY")
    still = [d for d, recs in by_doi.items()
             if not (recs[0].get("abstract") or "").strip()]
    if s2_key and still:
        # One POST to the batch endpoint (up to 500 ids) instead of one GET per
        # DOI: the per-DOI loop spent the whole budget in 429 backoffs and
        # filled nothing on the 2026-10-19 candidates; the batch call answered
        # at once. Expect little from it either way -- S2 withholds the same
        # publisher abstracts OpenAlex lacks (5 of 107 on that sweep).
        for i in range(0, len(still), 500):
            if time.monotonic() - started > budget_s:
                log(f"  [abstracts] {budget_s}s budget reached; "
                    f"{len(still) - i} still without one")
                break
            chunk = still[i:i + 500]
            try:
                req = urllib.request.Request(
                    "https://api.semanticscholar.org/graph/v1/paper/batch?fields=abstract",
                    data=json.dumps({"ids": ["DOI:" + d for d in chunk]}).encode(),
                    headers={"x-api-key": s2_key, "Content-Type": "application/json",
                             "User-Agent": UA})
                with urllib.request.urlopen(req, timeout=TIMEOUT * 2) as resp:
                    rows = json.loads(resp.read().decode("utf-8"))
            except Exception as exc:  # noqa: BLE001 -- best-effort enrichment
                log(f"  [abstracts] S2 batch failed ({exc}); skipping")
                break
            for doi, row in zip(chunk, rows):
                if row:
                    apply(doi, clean_ws(row.get("abstract") or ""), "semanticscholar")

    return len(by_doi), filled


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
    # S2 is opt-in: its first live run (2026-09-01) returned zero hits on every
    # completed query while its 429 backoffs consumed the call budget, and the
    # agent had to --no-s2 mid-run. Set RADAR_ENABLE_S2=1 in .env to re-enable.
    s2_on = bool(os.environ.get("S2_API_KEY")) and os.environ.get("RADAR_ENABLE_S2") == "1"
    ads_on = bool(os.environ.get("ADS_API_TOKEN"))

    log(f"Paper Radar: {len(papers)} paper(s), since {since}")
    log("OpenAlex: api key present" if openalex_key() else
        "OpenAlex: NO API KEY -- keyless access is ~$0.10/day and is usually exhausted "
        "by morning; add OPENALEX_API_KEY to .paper-radar/.env (free at openalex.org/settings/api)")
    log(f"Sources: arxiv, openalex, crossref" + (", semanticscholar" if s2_on else " (s2: no key, skipped)")
        + (", ads" if ads_on else " (ads: no key, citation watch falls back to openalex)"))

    stats = {"raw": 0, "excluded": 0, "future_dated": 0, "dupe_seen": 0, "dupe_run": 0,
             "quarantined": 0, "kept": 0, "abstract_tried": 0, "abstract_filled": 0}
    # arXiv: the week's listings, evaluated locally (see load_arxiv_week). The
    # search API stays only as a fallback -- for categories whose listing
    # failed, or a window reaching back past what the listings cover.
    # The week-scale loaders (arXiv listings, bioRxiv) outlast one 180 s
    # device-shell slice, so they work to the same --budget as the sweep, save
    # their progress, and hold the paper loop back until they are complete.
    deadline = (started + args.budget) if args.budget else None
    sources_loading = False
    arxiv_week, arxiv_api_needed = None, False
    arxiv_cats = sorted({c for p in papers if p.get("arxiv")
                         for c in (p.get("arxiv_categories") or [])})
    if arxiv_cats and not args.arxiv_api:
        arxiv_week, failed, arxiv_ready = load_arxiv_week(
            arxiv_cats, refresh=args.arxiv_refresh, deadline=deadline)
        sources_loading = not arxiv_ready
        listed_from = min((r["date"] for r in arxiv_week.values() if r.get("date")),
                          default=None)
        stats["arxiv_listed"] = len(arxiv_week)
        stats["arxiv_listing_failed"] = failed
        if sources_loading:
            pass
        elif not arxiv_week:
            log("  ! arXiv listings returned NOTHING -- falling back to the search API")
            arxiv_week, arxiv_api_needed = None, True
        # The listing dates are announcement days (five a week), which cover
        # the preceding week of submissions; only a window reaching back past
        # that week needs the API.
        elif failed or since < (dt.date.today() - dt.timedelta(days=8)).isoformat():
            arxiv_api_needed = True
            log(f"  [arxiv] also using the search API: "
                + (f"listing failed for {', '.join(failed)}" if failed else
                   f"window starts {since}, listings reach back only to {listed_from}"))
    elif arxiv_cats:
        arxiv_api_needed = True

    arxiv_index = arxiv_index_freshness(since) if arxiv_api_needed else None
    coupling, biorxiv = {}, {}
    if not sources_loading and any(p.get("biorxiv") for p in papers):
        biorxiv, biorxiv_ready = load_biorxiv_week(since, deadline=deadline)
        sources_loading = not biorxiv_ready
    if not sources_loading and not args.no_coupling:
        coupling = search_coupling(since)
    stats["coupling_kept"] = sum(len(v) for v in coupling.values())
    stats["biorxiv_listed"] = len(biorxiv)
    if sources_loading:
        log("  [sources] week-scale sources still loading; no papers swept this call -- "
            "re-run the same command with --resume")
        papers = []
    if arxiv_index:
        stats["arxiv_index_newest"] = arxiv_index["newest"]
        stats["arxiv_index_lag_days"] = arxiv_index["lag_days"]
        if arxiv_index["stale"]:
            log(f"  ! arXiv SEARCH INDEX IS STALE: newest indexed submission is "
                f"{arxiv_index['newest']} ({arxiv_index['lag_days']}d behind). "
                f"arXiv results this run cover nothing newer than that -- a zero "
                f"arXiv yield is upstream, not dedup. Re-sweep with an explicit "
                f"--since once it recovers.")

    results = dict(prior)
    truncated = sources_loading

    for paper in papers:
        key = paper["key"]

        if args.budget and (time.monotonic() - started) > args.budget:
            log(f"\n[budget] {args.budget}s elapsed; stopping cleanly before '{key}'")
            truncated = True
            break

        log(f"\n[{key}] {paper['title']}")
        # exclude_allow lifts a global homonym guard for a paper whose subject it is
        # (the home-programme rider needs "interstellar object").
        allow = {x.lower() for x in paper.get("exclude_allow", [])}
        excl = [x for x in global_exclude if x.lower() not in allow] + paper.get("exclude", [])
        hits = {}
        title_index = {}

        plan = []
        # arXiv asks for >=3s between requests, so its phrases are OR-ed into a
        # single query rather than issued one-by-one. Four separate calls cost
        # 12s of pure sleep per paper; across 15 papers that alone blew the
        # runtime past the point where the run could finish at all.
        arxiv_qs = paper.get("arxiv", [])
        if arxiv_qs and arxiv_week is not None:
            plan.append(("arxiv_list", "|".join(arxiv_qs)))
        if arxiv_qs and arxiv_api_needed:
            plan.append(("arxiv", " OR ".join(f"({q})" for q in arxiv_qs)))
        if coupling.get(key):
            plan.append(("coupling", "series references"))
        if biorxiv and paper.get("biorxiv"):
            plan.append(("biorxiv", "|".join(paper["biorxiv"])))
        if paper.get("s2_recommend") and os.environ.get("S2_API_KEY"):
            plan.append(("s2_recommend", "paper's DOI references"))
        if ads_on:
            for q in paper.get("ads", []):
                plan.append(("ads", q))
        for q in paper.get("ntrs", []):
            plan.append(("ntrs", q))
        for q in paper.get("openalex", []):
            plan.append(("openalex", q))
        for q in paper.get("crossref", []):
            plan.append(("crossref", q))
        if s2_on:
            for q in paper.get("openalex", [])[:2]:
                plan.append(("s2", q))
        for cw in paper.get("cites_watch", []):
            # entries: {"id": "W..."|null, "bibcode": "..."|absent, "label": "..."}
            plan.append(("cites",
                f"{cw.get('id') or ''}|{cw.get('bibcode') or ''}|{cw.get('label') or ''}"))
        for vw in paper.get("venue_watch", []):
            # entries are {"issn": [...], "name": "...", "subject_gate": [...]}
            # subject_gate is optional; see search_crossref_venue.
            plan.append(("venue", f"{';'.join(vw.get('issn') or [])}|{vw.get('name') or ''}"
                                  f"|{';'.join(vw.get('subject_gate') or [])}"))

        for source, q in plan:
            try:
                if source == "arxiv_list":
                    found = match_arxiv_week(paper, arxiv_week, since)
                elif source == "coupling":
                    found = [dict(r) for r in coupling.get(key, [])]
                elif source == "biorxiv":
                    found = match_local(paper, biorxiv, "biorxiv")
                elif source == "s2_recommend":
                    found = search_s2_recommend(key, since)
                elif source == "ads":
                    found = search_ads(q, since)
                elif source == "ntrs":
                    found = search_ntrs(q, since)
                elif source == "arxiv":
                    found = search_arxiv(q, since, paper.get("arxiv_categories"))
                elif source == "openalex":
                    found = search_openalex(q, since)
                elif source == "crossref":
                    found = search_crossref(q, since)
                elif source == "s2":
                    found = search_s2(q, since)
                elif source == "cites":
                    found = search_cites(q, since)
                elif source == "venue":
                    found = search_crossref_venue(q, since)
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
                if quarantine_abstract(rec):
                    stats["quarantined"] += 1
                    log(f"  ! abstract quarantined ({rec['abstract_quarantined']}): "
                        f"{rec['title'][:60]}")
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
                rec["found_via"] = (f"{source}: {rec.pop('matched_query')}"
                                    if rec.get("matched_query") else f"{source}: {q}")
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
        ranked = cap_containers(ranked)
        if args.limit:
            ranked = ranked[: args.limit]
        stats["kept"] += len(ranked)
        results[key] = {
            "paper": paper["file"],
            "file": paper["file"],  # SKILL.md and the screening prompts read "file"
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

    # One abstract pass, on the call that finishes the sweep. `results` holds
    # every paper accumulated under --resume by then, so a single pass covers
    # the whole sweep; running it per call would blow the 45 s shell ceiling
    # and re-ask DOIs already answered.
    if complete and not args.no_abstract_fetch:
        missing = sum(1 for pr in results.values() for r in pr.get("candidates", [])
                      if r.get("doi") and not (r.get("abstract") or "").strip())
        if missing:
            log(f"\n[abstracts] {missing} candidate(s) have a DOI but no "
                f"abstract; re-asking OpenAlex then S2")
            tried, filled = backfill_abstracts(results, budget_s=args.abstract_budget)
            stats["abstract_tried"], stats["abstract_filled"] = tried, filled
            log(f"[abstracts] asked {tried}, filled {filled}")
    elif not complete:
        log("[abstracts] sweep incomplete; the backfill runs on the finishing call")

    payload = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "since": since,
        "sources": ["arxiv", "openalex", "crossref"] + (["semanticscholar"] if s2_on else []) + (["ads"] if ads_on else []),
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
        f"cross-source dupes {stats['dupe_run']} | abstracts quarantined "
        f"{stats['quarantined']} | KEPT {stats['kept']}")
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
                keys = seen.setdefault("keys", {})
                keys[rec["_key"]] = seen_entry(rec, key, today, keys.get(rec["_key"]))
        seen["last_run"] = today
        archive_candidates(payload, today)
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
    ap.add_argument("--no-abstract-fetch", action="store_true",
                    help="skip the post-sweep abstract backfill")
    ap.add_argument("--abstract-budget", type=int, default=20,
                    help="seconds for the abstract backfill pass (default 20); it "
                         "runs once, on the call that completes the sweep")
    ap.add_argument("--no-s2", action="store_true", help="force-skip Semantic Scholar")
    ap.add_argument("--arxiv-api", action="store_true",
                    help="use the arXiv search API instead of the weekly listings")
    ap.add_argument("--no-coupling", action="store_true",
                    help="skip the coupling channel (works citing the series' references)")
    ap.add_argument("--arxiv-refresh", action="store_true",
                    help="re-fetch the arXiv listings even if today's cache exists")
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
