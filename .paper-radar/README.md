# Paper Radar

A daily literature review for the fifteen-paper series. Searches arXiv,
OpenAlex and Crossref for work relevant to each paper, screens the hits with one
agent per paper, verifies every citation against a resolving identifier, writes
a dated digest, and stages accepted insertions for review.

Runs at 06:00 daily via a scheduled task. Nothing here edits a paper without
leaving you a diff to review first.

## Layout

```
.paper-radar/
  search.py           the search engine -- stdlib only, no dependencies
  queries.json        hand-curated queries + exclude lists, per paper   <- tune this
  seen.json           dedup ledger; why most mornings are quiet
  digests/            YYYY-MM-DD.md, one per run (+ .patch on the fallback path)
  check_freshness.py  dead-man's switch: has the radar stopped running?
  send_digest_email.py  emails the morning summary (Step 7)
  skill/paper-radar/  the skill source; rebuild the .skill bundle from here
  .env                optional, gitignored: S2_API_KEY=...
```

## Is it still running?

The radar's own failure mode is silence. When the scheduled run dies, no digest
is written and no email arrives — and a missing email is indistinguishable from a
quiet morning with nothing to report. That is not hypothetical: the 06:00 job
died on 2026-09-05 when the repo moved under `AI/projects/` and the mount
resolution stopped finding it, and both that morning and the next passed
unnoticed.

```bash
python3 .paper-radar/check_freshness.py            # print status; exit 1 if stale
python3 .paper-radar/check_freshness.py --email    # ...and send one alert per day
```

Staleness is judged against the clock, not just the calendar: once `--run-hour`
(default 6) plus `--grace-hours` (default 2) has passed, today's run is owed;
before that, only yesterday's is. So it will not cry stale at 05:00, and will not
call a radar that missed this morning fresh at 18:00.

**Run it from a scheduler that is not the radar's own.** A check that only fires
when the radar works cannot report that the radar stopped working. The 06:00 job
is a cloud routine, so a local Windows scheduled task is the right host — the two
then fail independently, which is the whole point.

## Running it by hand

```bash
# a normal 7-day sweep -- repeat until status is "complete" (3-4 calls)
python3 .paper-radar/search.py --days 7 --out /tmp/candidates.json --resume --budget 35

# one paper, wide window
python3 .paper-radar/search.py --paper fermi --since 2015-01-01 --out /tmp/fermi.json --budget 0

# record a finished sweep so it never resurfaces (refuses if incomplete)
python3 .paper-radar/search.py --mark-seen-from /tmp/candidates.json
```

Or just ask Claude to "run the paper radar".

## Design notes

Each of these was learned by watching it fail, not by reasoning about it in
advance. They are recorded so the next person doesn't rediscover them.

**arXiv is https-only.** The documented `http://export.arxiv.org` endpoint 301s
and returns an empty body without `curl -L`, which looks exactly like "no
results" rather than an error.

**Relevance-sort, then date-filter. Never date-sort.** With `sort=published`,
Crossref answered a Fermi-paradox query with Roman book censorship, a German
article about Dubai chocolate shops, and a linguistics paper matching the word
"von". The same query on default relevance sort returns six on-topic papers.

**Crossref publication dates are unreliable.** Live results included papers
dated 2031, 2030 and 2028. Anything more than 120 days out is dropped.

**Dedup keys on arXiv id first.** OpenAlex reports arXiv preprints under DOI
`10.48550/arXiv.NNNN` while arXiv reports a bare id; keying on DOI first made
every preprint appear twice. Titles are matched as a second pass, since a
journal version and its preprint share no identifier at all.

**There is no lexical relevance filter, deliberately.** One was built and
measured against a real 460-candidate sweep. At every threshold it failed: at
0.6 it kept "Basics of Artificial Intelligence and Machine Learning" and
"Digitalizing Mesopotamian Heritage" (both scoring 1.00) while dropping
"Mechanistic World Models" (0.57). A third of records carry no abstract at all,
leaving any lexical test blind to them. Relevance here is semantic, so the
screening agents judge it and the script stays high-recall. The `exclude` lists
in `queries.json` are a different thing: they kill unambiguous homonyms
("Fermi level" is solid-state physics, a "fluorescent probe" is a lab reagent,
"speciation" is also a chemistry term), not weak matches.

**One book can eat a paper's whole day.** When a volume is indexed, its chapters
arrive as separate DOIs and flood that paper's candidate list. On 2026-09-06 a
single Turkish edited volume supplied 6 of the Fermi paper's 7 candidates, and
one monograph supplied 8 of the ethics paper's 21 — including its Introduction
and Conclusion; on 2026-09-08 one book gave 4 of the vehicle paper's 5. The
screeners caught every one, but each cost a full read. `cap_containers` now keeps
one record per volume. It fires only on records whose *type* says book component:
grouping by DOI stem alone would also collapse consecutive articles in one
journal issue (`10.1016/j.actaastro.2026.08` covers `.062` and `.075`, two
unrelated papers), which would drop real work.

**arXiv's search index can freeze while the API keeps answering.** From
2026-09-04 17:51 UTC it stopped taking new submissions; queries still returned
200 with well-formed results, just nothing newer. The radar cannot distinguish
that from a quiet week — both are zero arXiv candidates — so it went unnoticed
for five days across four digests, each day's zero blamed on dedup. Every sweep
now probes `cat:cs.AI` once (it has submissions every weekday) and warns when the
newest indexed item is more than two days old. The `id_list` endpoint used for
verification is unaffected and keeps working. **When the index recovers, re-sweep
with an explicit `--since` covering the outage**: the rolling 7-day window will
otherwise move past those submissions and they will never be seen.

**The sweep cannot finish in one shell call.** Shell calls are capped at ~45s
and the sandbox kills background processes when the spawning call exits
(`bwrap --die-with-parent`) — so `nohup ... &` dies silently partway through,
which is worse than failing, because the digest still looks complete. Hence
`--resume`.

**`--mark-seen` is refused on an incomplete sweep.** Marking papers seen that
were never actually searched would bury them permanently and silently.

**The mount blocks deletes by default**, so git cannot commit (it can't unlink
its own `.lock` files). The skill probes for this and falls back to emitting a
`.patch` file instead of a branch.

## Semantic Scholar (optional)

Off unless a key is present. Unauthenticated, S2 shares a saturated 1000 req/s
pool across all anonymous users and mostly returns 429; a key buys a private
1 req/s. Get one at https://www.semanticscholar.org/product/api#api-key-form
then create `.paper-radar/.env` (already gitignored via the `.env` rule):

```
S2_API_KEY=your-key-here
```

Usage stays around 30 requests/day (15 papers x 2 queries), well inside the
1 req/s cap, which the script enforces with a 1.1s delay plus exponential
backoff. Keys idle for ~60 days get revoked.

## Known limitations

- **~33% of Crossref records carry no abstract**, so screening those falls back
  to the title alone. The agents are told to prefer `consider` over `cite` when
  the abstract is missing rather than guess.
- **Paywalled journals are largely invisible.** Coverage is good for arXiv,
  OpenAlex and open-access work; patchier for closed venues.
- **`seen.json` is permanent.** A paper judged irrelevant today never
  resurfaces, even if a later revision would make it relevant. Use
  `--ignore-seen` for a one-off re-check.
- **The backlog file is stale.** `candidate_papers_backlog.md` still says nine
  papers written; there are now fifteen.
