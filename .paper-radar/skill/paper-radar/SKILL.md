---
name: paper-radar
description: "Daily literature radar for the AI Galaxy Traveler interstellar-probe paper series. Sweeps arXiv, OpenAlex and Crossref for work relevant to each of the sixteen papers, screens hits with per-paper agents, verifies every citation, writes a dated digest, stages accepted insertions on a review branch, and emails a summary. Use when asked to run the paper radar, do the daily paper review, check for new relevant literature, or update the series with new papers."
---

# Paper Radar

A daily literature review for the sixteen-paper **AI Galaxy Traveler** series on
slow self-replicating interstellar probes (author: S. Stone, Metropolitan State
University). The paper list lives in `.paper-radar/queries.json`; do not
hard-code a count anywhere else.

Each run: search -> screen -> verify -> digest -> stage on a branch -> email.

**The two rules that matter most:**

1. **Never invent a citation.** Every reference reaching a paper must be verified
   against a resolving DOI or arXiv ID. An unverifiable reference is dropped, not
   guessed at. This is the worst failure available to this workflow: a fabricated
   citation in an academic paper is far more damaging than a missed one.
2. **Never touch the working tree.** Edits are staged on a branch via a
   throwaway git worktree or a sandbox clone. The user's uncommitted work is
   never stashed, moved, committed, or reverted.

---

## Where things run

The repo lives on Scott's computer, not in the cloud container. Every command in
this skill runs in the **device shell** (the `device_bash` tool, which runs on his
machine's Linux VM with connected folders mounted under `$HOME/mnt/`) unless a
step says otherwise. The cloud `bash` shell cannot see the repo at all; do not
look for it there.

Device shell facts that shape the steps below:

- Each call is a fresh `bash -c`; no cwd or env carries over. Re-resolve `$REPO`
  in every call (one line, cheap).
- Calls time out at 120 s by default and 180 s at most (`timeout_ms: 180000`).
  Background processes die when the call returns; `nohup` does not help.
- Files outside `mnt/` (`$HOME`, `/tmp`) persist between calls but are invisible
  to Scott. Keep intermediates there; deliverables go inside the repo.
- Network follows the organisation's egress allowlist. Verified 2026-09-05:
  OpenAlex, arXiv, Crossref and the SMTP host are all reachable from the VM.
  The cloud shell always has network; if a `curl` in the device shell fails on
  a well-known API, verify from the cloud shell instead (verification needs
  only identifiers, no files).
- Deleting files inside `mnt/` is blocked until a person approves it (see Step 5).

---

## Setup

Repo (Windows path):
`C:\Users\sston\OneDrive - Minnesota State\AI\projects\AI galaxy traveler`

In the device shell it is under `$HOME/mnt/` -- either as `mnt/AI galaxy traveler`
directly, or nested, when what is connected is a parent folder
(`mnt/AI/projects/AI galaxy traveler`). Do not assume the shallow form. `$HOME`
is itself `/sessions/<id>`, so the search below covers both spellings.

Resolve the mount first, in every call that needs it:

```bash
REPO=$(find "$HOME/mnt" /sessions/*/mnt -maxdepth 4 -type d -name "AI galaxy traveler" 2>/dev/null |
       while IFS= read -r d; do
         [ -d "$d/.paper-radar" ] && { printf '%s\n' "$d"; break; }
       done)
echo "repo: $REPO"
```

The `.paper-radar` test is what makes a deeper match trustworthy: it confirms
this is the real folder and not a same-named copy, so the search can tolerate
depth without becoming a guess.

**If `$REPO` is empty, STOP.** The search already covered every connected mount
to four levels, so an empty result means the folder genuinely is not there. Do
not improvise a path and do not widen the search. Report plainly that the *AI
galaxy traveler* folder is not connected to this session and that the radar
cannot run without it. This is the most likely cause of a failed scheduled run:
on 2026-09-05 the 06:00 run died here in silence after the folder moved to
`AI/projects/`, and the only outward signs were a missing digest and no morning
email. (A scheduled task only sees the folder if it was created bound to Scott's
computer with that folder attached; if the folder was moved or renamed, the task
needs recreating with the new path.)

If the device shell itself is unreachable (no folders connected, or the computer
is offline), say so and stop. Do not attempt the run from the cloud shell.

Then confirm it is a real git repo, and read the project conventions:

```bash
cd "$REPO" && git rev-parse --is-inside-work-tree && git log --oneline -1
```

Read `CLAUDE.md` at the repo root before writing anything. It is the source of
truth for house style, canonical numbers, and cross-reference naming.
Everything below assumes it.

Set the date once per call, in Scott's timezone, so a late-evening run does not
roll over to tomorrow's date on a UTC clock:

```bash
DATE=$(TZ=America/Chicago date +%F)
```

---

## Step 1 -- Search

A full sweep takes several minutes, longer than one device-shell call. The
script handles this with `--resume`: each invocation works until its `--budget`
expires, appends to the same output file, and reports what remains.

Default the window to the days since the last run
(`.paper-radar/seen.json` -> `last_run`), falling back to 7:

```bash
cd "$REPO"
mkdir -p "$HOME/radar" && rm -f "$HOME/radar/candidates.json"
python3 .paper-radar/search.py --days 7 --out "$HOME/radar/candidates.json" --resume --budget 150
```

Run it with `timeout_ms: 180000`. The last line of stdout is JSON:
`{"status": "...", "remaining": [...]}`. **Repeat the identical command until
`status` is `complete`** -- normally 1-2 calls at this budget on a good day.
Do not proceed while papers remain.

If it still will not complete after ~6 attempts, continue with what you have,
but mark the digest **PARTIAL**, list the unswept papers in it, and **skip Step
6** entirely. A partial sweep marked as seen would silently bury every paper it
never looked at.

**When the sweep is crawling** (one or two papers per call), look at the
per-source lines. `! network error (The read operation timed out)` on the
`arxiv` lines means arXiv's *search* endpoint is slow or rate-limiting that day;
the script retries each query three times with a long timeout, so a dead arXiv
costs a minute or more per paper. This is arXiv's side, not the VM: the `id_list`
endpoint used in Step 3 keeps working. Keep resuming (each call still makes
progress), fall back to PARTIAL if it will not finish, and say in the report
that arXiv was slow. Do not run the sweep from the cloud shell against a copy of
the repo: `seen.json` and the digests must land in the real folder.

Expect roughly 300-450 candidates for a 7-day window. That is normal and
intended: the script is deliberately high-recall because the screening agents,
not the script, are the relevance filter.

Read the candidates file back with `cat` (or `python3 -c` slices) from the device
shell; the screening agents need its contents in their prompts.

---

## Step 2 -- Screen (parallel agents, one per paper)

For every paper with candidates, spawn a **`general-purpose` agent**. Send them
all in a single message so they run concurrently -- sixteen sequential agents is
far too slow for a 6am run.

**Use Opus for screening** (pass `model: "opus"` explicitly rather than relying
on inheritance). This step is the entire relevance filter -- the script does no
semantic judgement at all -- and the failure modes are expensive and quiet: a
missed piece of prior art that a reviewer later finds, or a citation that reads
plausibly but misstates what the paper showed. On the verification run, Opus
caught that a candidate posted five weeks earlier was prior art on the series'
core hypothesis, noticed that another modelled only u = 0.1c and so refused to
claim a result at the series' 450 km/s, declined to judge two records whose
abstracts were missing, and re-routed a near-miss to a different paper in the
series because its target function was inverted. Sonnet is a reasonable economy
if cost matters, but screen its output for a while before trusting it -- and
never let a cheaper model be the last thing between a hallucinated citation and
a published paper.

Give each agent exactly one paper. Its prompt must contain:

- The paper's `title`, `thesis` and `file` (all present in `candidates.json`)
- That paper's candidate list: title, authors, venue, date, DOI/arXiv id, abstract
- The instruction below

> You are screening literature for one paper in an academic series on slow,
> self-replicating interstellar AI probes. The series' overriding rule is
> **realistic physical constraints, not science fiction**.
>
> Paper: {title}
> What it argues: {thesis}
>
> For each candidate, return exactly one verdict:
>
> - **cite** -- directly bears on this paper's argument and is worth adding.
>   Reserve this. A typical day produces zero to two across the whole series.
> - **consider** -- genuinely related and worth the author's attention, but you
>   cannot justify a specific insertion.
> - **ignore** -- everything else.
>
> Be ruthless. These queries are high-recall and most candidates are keyword
> collisions: "Fermi level" is solid-state physics, a "fluorescent probe" is a
> lab reagent, "speciation" is a chemistry term. Topical adjacency is not
> relevance -- a paper on AI in medical writing is not relevant to a paper on a
> probe's knowledge growth merely because both say "knowledge" and "AI".
> Ask: *would this change, support, or challenge a specific claim in the paper?*
> If not, it is `ignore`.
>
> For each **cite**, additionally give:
> - `section`: the section of the paper it belongs in, by name
> - `claim`: the specific existing claim it bears on
> - `insertion`: 1-3 sentences of finished prose in the series' voice --
>   concise, direct, minimal hedging, plain-text math only (`R_eff = Σ p_i V_i`,
>   never LaTeX), no tables, citation in-text as (Author, Year)
> - `reference`: a full reference-list entry
> - `confidence`: high | medium | low
>
> Never state a finding the abstract does not support. If the abstract is
> missing or too thin to judge, say so and use `consider` -- do not guess from
> the title. Return `[]` rather than padding with weak hits: an empty result is
> a perfectly good day's work.

---

## Step 3 -- Verify every citation

Non-negotiable. Applies to every **cite**, and to every **consider** that will
appear in the digest. The screening agent saw only search metadata; it has not
confirmed the work exists as described.

For each item, resolve the identifier and check the metadata independently. This
needs only the identifier, so run it in whichever shell has network (the cloud
`bash` shell always does):

```bash
# by DOI -- OpenAlex needs the key from .paper-radar/.env (OPENALEX_API_KEY);
# without it the call 429s "Insufficient budget". Fall back to Crossref
# (https://api.crossref.org/works/<DOI>) or DataCite (https://api.datacite.org/dois/<DOI>).
KEY=$(grep -s '^OPENALEX_API_KEY=' "$REPO/.paper-radar/.env" | cut -d= -f2-)
curl -s --max-time 20 "https://api.openalex.org/works/https://doi.org/<DOI>?api_key=$KEY" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title'),'|',d.get('publication_year'),'|',((d.get('primary_location') or {}).get('source') or {}).get('display_name'))"

# by arXiv id
curl -s --max-time 20 "https://export.arxiv.org/api/query?id_list=<ID>" | grep -E "<title>|<published>|<name>"
```

Confirm **author, year, and venue** match what the digest will claim -- this is
CLAUDE.md's standing rule ("Verify any new reference by web search before
citing"), applied here.

Drop anything that fails to resolve or whose metadata disagrees, and note the
drop in the digest. **Downgrade `cite` -> `consider`** rather than guessing at a
detail. Note that arXiv must be **https**: plain `http` 301s and returns an
empty body.

---

## Step 4 -- Write the digest

Write to `$REPO/.paper-radar/digests/$DATE.md`, following the template at the
end of this file. Writing a new file into the repo is create-only, so it always
succeeds even when deletion is blocked.

Lead with what matters. If nothing survived screening, say exactly that in one
line and stop -- do not manufacture content. **A quiet day is the expected
result, not a failure.** Padding a digest to look productive wastes the author's
time and trains him to stop reading it.

Every item must carry a resolving link. Mark anything unverified as such,
explicitly.

---

## Step 5 -- Stage accepted insertions on a branch

Only for **high-confidence `cite`** items that survived Step 3. If there are
none, skip this step and say so.

The working tree usually holds uncommitted work, and much of the repo's apparent
diff is CRLF line-ending churn (`core.autocrlf` is unset, so roughly half the
"modified" files differ only in line endings). Therefore:

- **Never** `git add -A`, `git add .`, `git commit -a`, `git stash`, or
  `git checkout` in the user's working tree. A blanket `git add` would sweep
  thousands of phantom line-ending changes into the commit and make the diff
  unreviewable.
- Always name each edited file explicitly in `git add`.

### The delete-permission problem -- read this before trying to commit

The mounted folder is **create/write but no-delete by default**. Git cannot
commit under that restriction: it must unlink its own `.lock` files. The failure
looks like this, and is not a bug in your commands:

```
warning: unable to unlink '.git/index.lock': Operation not permitted
fatal: cannot lock ref 'HEAD': Unable to create '...HEAD.lock': File exists.
```

Deletion may or may not be enabled on any given run. **Probe it first, cheaply,
before creating any worktree:**

```bash
cd "$REPO" && touch ._radar_probe && rm -f ._radar_probe 2>/dev/null \
  && echo "DELETE_OK" || echo "DELETE_BLOCKED"
```

- `DELETE_OK` -> take **Path A** (branch).
- `DELETE_BLOCKED` -> take **Path B** (patch). In an interactive session you may
  instead request delete permission for the connected folder (the
  `device_request_delete_permission` tool, asked once, with the folder root and
  a one-line reason) and re-probe. It needs human approval, so a 6am run must
  assume Path B.

### Path A -- branch (preferred)

```bash
cd "$REPO"
git worktree add "$HOME/radar/wt-$DATE" -b "paper-radar/$DATE" HEAD
```

The worktree is built from `HEAD`, so it sees a **clean tree** and the user's
uncommitted work is untouched. Apply insertions inside `$HOME/radar/wt-$DATE`
only, then:

```bash
cd "$HOME/radar/wt-$DATE"
git add papers/interstellar_AI_fermi_paper.md   # name each file explicitly
git -c user.email=radar@local -c user.name="Paper Radar" \
    commit -m "paper-radar $DATE: <n> insertion(s) across <m> paper(s)"
cd "$REPO" && git worktree remove "$HOME/radar/wt-$DATE"
```

Review command for the user: `git diff main..paper-radar/YYYY-MM-DD`

### Path B -- patch file (fallback, always works)

Clone to VM-local disk, where git has full permissions, and hand back a patch.
Writing a *new* file into the repo is create-only, so it always succeeds:

```bash
rm -rf "$HOME/radar/clone"
git clone -q "$REPO" "$HOME/radar/clone"
cd "$HOME/radar/clone" && git checkout -q -b "paper-radar/$DATE"
# ...apply insertions here...
git add papers/interstellar_AI_fermi_paper.md
git -c user.email=radar@local -c user.name="Paper Radar" \
    commit -q -m "paper-radar $DATE: <n> insertion(s)"
git format-patch main --stdout > "$REPO/.paper-radar/digests/$DATE.patch"
```

Tell the user to apply it with:

```bash
git am .paper-radar/digests/YYYY-MM-DD.patch     # or: git apply --check first
```

Verified: a patch produced this way applies cleanly to a fresh clone.

### Editing rules (both paths)

- Insert the prose into the named section, in the series' voice
- Add the reference to the **References** section, alphabetically
- **No tables. No LaTeX.** Plain-text math only
- Keep canonical numbers identical to CLAUDE.md (cruise ~450 km/s, Proxima
  4.246 ly, 127 stars, R_eff 0.48/0.94/1.39/1.85, seed ~3,700 kg, vitamin ~3%)
- Use CLAUDE.md's cross-reference names ("the DNA mission-ledger paper", never
  "the memory paper")

### If anything goes wrong

**Abandon the branch, keep the digest.** The digest is the deliverable; the
branch is a convenience. Then clean up after yourself -- a half-finished git
operation can leave lock files that break the user's *next* git command on
Windows:

```bash
cd "$REPO"
git worktree remove --force "$HOME/radar/wt-$DATE" 2>/dev/null
git worktree prune
find .git -name "*.lock" -delete 2>/dev/null
```

If that `find -delete` fails with "Operation not permitted", deletion is
blocked: list the stale lock files by path in the report so Scott can remove
them, rather than leaving him to discover them.

Leave the repo exactly as found: same branch, same modified-file count, same
HEAD. Verify it before reporting done.

---

## Step 6 -- Mark seen (last, and only on success)

Only after the digest is written, and only if the sweep completed:

```bash
cd "$REPO"
python3 .paper-radar/search.py --mark-seen-from "$HOME/radar/candidates.json"
```

This is deliberately the final repo write. Everything in `candidates.json` --
including what was screened out -- is recorded so it never resurfaces, which is
what keeps subsequent mornings quiet. Run it too early and a crash mid-run
buries papers that were never reported. The script refuses to mark an
incomplete sweep.

---

## Step 7 -- Email the summary (every run, never blocking)

**This step is mandatory and is part of the run's success criteria.** The
2026-09-14 run wrote a digest, marked the run done, and never sent the email;
nobody knew the run had happened. After the digest is written (and regardless
of whether anything was staged, and even on a PARTIAL day), run in the device
shell:

```bash
cd "$REPO" && python3 .paper-radar/send_digest_email.py
```

It emails a compact summary -- staged titles, flagged titles, counts -- to the
address configured in `.paper-radar/.env` (RADAR_SMTP_* / RADAR_EMAIL_TO).
Send on **quiet days too**: "nothing new today" is itself useful signal, and a
missing email is indistinguishable from a failed run (that is exactly how the
2026-09-05 failure went unnoticed).

With no credentials present the script prints one line and exits 0 without
sending; a send failure must not fail the run. Read the script's output and
report what actually happened: say "sent" only if the script says it sent.
Never invent a delivery confirmation, and never print or log the credential
values. If SMTP is unreachable from the device VM, say so; the digest on disk is
the fallback.

---

## Reporting back

Two or three sentences: how many candidates were swept, what survived, whether a
branch or patch was created, and whether the email went out. Link the digest.
Do not recap the pipeline.

If nothing was found, say so plainly. Do not apologise for a quiet day.

---

## Tuning

- **Queries**: `.paper-radar/queries.json`, hand-curated per paper. Do not
  auto-generate them from paper titles -- naive extraction returns von Neumann
  *algebras* for a von Neumann *probe* query.
- **Too much noise from one paper?** Add the offending phrase to that paper's
  `exclude` list, or to `defaults.exclude` if it is a general homonym. Prefer a
  broad query plus a sharp exclude over a narrow query; it preserves recall.
- **Semantic Scholar**: optional, off unless `S2_API_KEY` is set in the
  environment or in `.paper-radar/.env` (gitignored). Unauthenticated it shares
  a saturated 1000 req/s pool across all anonymous users and mostly returns 429;
  a key buys a private 1 req/s. Apply at
  https://www.semanticscholar.org/product/api#api-key-form
- **Quick health check** when a sweep is slow: from any shell,
  `curl -s --max-time 30 -o /dev/null -w "%{http_code} %{time_total}s\n" "https://export.arxiv.org/api/query?search_query=all:probe&max_results=5"`.
  A `000` after 30 s or a `429` means arXiv search is the problem for the day.
- **Backlog sweep**: `--baseline --since 2015-01-01` for a wide first pass, but
  expect thousands of candidates. Better done one paper at a time:
  `--paper fermi --since 2015-01-01`.
- **Re-surface everything**: `--ignore-seen`, or reset `keys` to `{}` in
  `.paper-radar/seen.json`.
- **This file** is mirrored at `.paper-radar/skill/paper-radar/SKILL.md` in the
  repo. When the skill changes, update both the saved skill and the repo copy.

---

## Digest template

Structure for `.paper-radar/digests/YYYY-MM-DD.md`. Follow the shape, not the
wording. House style applies: concise, direct, no tables, plain-text math,
minimal hedging. Length is a function of what was found. Never pad.

**Quiet day (the common case)** -- this is the whole file:

```markdown
# Paper Radar -- 2026-07-18

Swept 312 candidates across 16 papers (7 days: 2026-07-11 to 2026-07-18).
Nothing met the bar. No branch created.
```

Resist listing near-misses as filler: if something is worth the author's
attention it is a `consider`; if it isn't, it does not belong in the file.

**Normal day:**

```markdown
# Paper Radar -- 2026-07-18

Swept 312 candidates across 16 papers (7 days: 2026-07-11 to 2026-07-18).
**1 insertion staged**, 3 flagged for attention.

Review: `git diff main..paper-radar/2026-07-18`

## Staged

### Fermi paper -- Section 4, the R_eff x D x G reframing

**Title of the Work** -- Author, A. (2026), arXiv:2606.xxxxx
[link](https://arxiv.org/abs/2606.xxxxx) · verified via arXiv API

Bears on: the claim that slow expansion is observationally indistinguishable
from absence.

> Inserted prose exactly as it now appears in the paper.

Reference added: Author, A. (2026). Title of the Work. *arXiv*.

Confidence: high.

## Flagged (no insertion proposed)

- **Title** -- Author, B. (2026), *Journal*
  [doi](https://doi.org/10.xxxx/yyyy) · verified
  One or two sentences on what it revisits and why it is worth reading before
  the next revision; no specific claim to attach it to yet.

## Dropped in verification

- **Some Title** -- DOI 10.xxxx/zzzz did not resolve; not cited.
```

**Rules:**

- Every item carries a resolving link and a note of how it was verified.
- Anything unverified is labelled unverified, or it does not appear.
- Quote insertions verbatim as they appear in the paper, so the digest can be
  read instead of the diff.
- Name the claim each citation bears on. "Relevant to the Fermi paper" is not
  good enough; say which argument and why.
- A PARTIAL sweep says so at the top and lists the unswept papers:

  ```markdown
  > **PARTIAL** -- the sweep did not finish; 4 papers unswept: routing, ethics,
  > speciation, subsystem. Results below cover the other 12. Dedup state was
  > NOT updated, so nothing here is lost; the next run re-checks everything.
  ```
