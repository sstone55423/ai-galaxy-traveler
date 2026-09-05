---
name: paper-radar
description: "Daily literature radar for the AI Galaxy Traveler interstellar-probe paper series. Sweeps arXiv, OpenAlex and Crossref for work relevant to each of the fifteen papers, screens hits with per-paper agents, verifies every citation, writes a dated digest, and stages accepted insertions on a review branch. Use when asked to run the paper radar, do the daily paper review, check for new relevant literature, or update the series with new papers."
---

# Paper Radar

A daily literature review for the fifteen-paper **AI Galaxy Traveler** series on
slow self-replicating interstellar probes (author: S. Stone, Metropolitan State
University).

Each run: search -> screen -> verify -> digest -> stage on a branch.

**The two rules that matter most:**

1. **Never invent a citation.** Every reference reaching a paper must be verified
   against a resolving DOI or arXiv ID. An unverifiable reference is dropped, not
   guessed at. This is the worst failure available to this workflow: a fabricated
   citation in an academic paper is far more damaging than a missed one.
2. **Never touch the working tree.** Edits are staged on a branch via a
   throwaway git worktree. The user's uncommitted work is never stashed, moved,
   committed, or reverted.

---

## Setup

Repo: `C:\Users\sston\OneDrive - Minnesota State\AI\projects\AI galaxy traveler`
In the Linux shell it is mounted under `/sessions/<session>/mnt/`.

Resolve the mount first — the session id changes on every run:

```bash
REPO=$(ls -d /sessions/*/mnt/"AI galaxy traveler" 2>/dev/null | head -1)
echo "repo: $REPO"
```

**If `$REPO` is empty, STOP.** Do not improvise a path, and do not go hunting
the filesystem for a substitute. Report plainly that the *AI galaxy traveler*
folder is not connected to this session and that the radar cannot run without
it. This is the most likely cause of a failed scheduled run.

Then confirm it is a real git repo, and read the project conventions:

```bash
cd "$REPO" && git rev-parse --is-inside-work-tree && git log --oneline -1
```

Read `CLAUDE.md` at the repo root before writing anything. It is the source of
truth for house style, canonical numbers, and cross-reference naming.
Everything below assumes it.

---

## Step 1 — Search

The sandbox kills background processes when the shell call that spawned them
exits (`bwrap --die-with-parent`), and shell calls are capped at ~45s. A full
15-paper sweep takes ~3 minutes, so it **cannot** finish in a single call —
backgrounding it with `nohup` does not work either; it dies silently partway.
The script handles this with `--resume`: each invocation works until its
`--budget` expires, appends to the same output file, and reports what remains.

Default the window to the days since the last run
(`.paper-radar/seen.json` -> `last_run`), falling back to 7:

```bash
cd "$REPO"
rm -f /tmp/candidates.json
python3 .paper-radar/search.py --days 7 --out /tmp/candidates.json --resume --budget 35
```

The last line of stdout is JSON: `{"status": "...", "remaining": [...]}`.
**Repeat the identical command until `status` is `complete`** — normally 3-4
calls. Do not proceed while papers remain.

If it still will not complete after ~8 attempts, continue with what you have,
but mark the digest **PARTIAL**, list the unswept papers in it, and **skip Step
6** entirely. A partial sweep marked as seen would silently bury every paper it
never looked at.

Expect roughly 300-450 candidates for a 7-day window. That is normal and
intended: the script is deliberately high-recall because the screening agents,
not the script, are the relevance filter.

---

## Step 2 — Screen (parallel agents, one per paper)

For every paper with candidates, spawn a **`general-purpose` agent**. Send them
all in a single message so they run concurrently — 15 sequential agents is far
too slow for a 6am run.

**Use Opus for screening** (pass `model: "opus"` explicitly rather than relying
on inheritance). This step is the entire relevance filter — the script does no
semantic judgement at all — and the failure modes are expensive and quiet: a
missed piece of prior art that a reviewer later finds, or a citation that reads
plausibly but misstates what the paper showed. On the verification run, Opus
caught that a candidate posted five weeks earlier was prior art on the series'
core hypothesis, noticed that another modelled only u = 0.1c and so refused to
claim a result at the series' 450 km/s, declined to judge two records whose
abstracts were missing, and re-routed a near-miss to a different paper in the
series because its target function was inverted. Sonnet is a reasonable economy
if cost matters, but screen its output for a while before trusting it — and
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
> - **cite** — directly bears on this paper's argument and is worth adding.
>   Reserve this. A typical day produces zero to two across the whole series.
> - **consider** — genuinely related and worth the author's attention, but you
>   cannot justify a specific insertion.
> - **ignore** — everything else.
>
> Be ruthless. These queries are high-recall and most candidates are keyword
> collisions: "Fermi level" is solid-state physics, a "fluorescent probe" is a
> lab reagent, "speciation" is a chemistry term. Topical adjacency is not
> relevance — a paper on AI in medical writing is not relevant to a paper on a
> probe's knowledge growth merely because both say "knowledge" and "AI".
> Ask: *would this change, support, or challenge a specific claim in the paper?*
> If not, it is `ignore`.
>
> For each **cite**, additionally give:
> - `section`: the section of the paper it belongs in, by name
> - `claim`: the specific existing claim it bears on
> - `insertion`: 1-3 sentences of finished prose in the series' voice —
>   concise, direct, minimal hedging, plain-text math only (`R_eff = Σ p_i V_i`,
>   never LaTeX), no tables, citation in-text as (Author, Year)
> - `reference`: a full reference-list entry
> - `confidence`: high | medium | low
>
> Never state a finding the abstract does not support. If the abstract is
> missing or too thin to judge, say so and use `consider` — do not guess from
> the title. Return `[]` rather than padding with weak hits: an empty result is
> a perfectly good day's work.

---

## Step 3 — Verify every citation

Non-negotiable. Applies to every **cite**, and to every **consider** that will
appear in the digest. The screening agent saw only search metadata; it has not
confirmed the work exists as described.

For each item, resolve the identifier and check the metadata independently:

```bash
# by DOI
curl -s --max-time 20 "https://api.openalex.org/works/https://doi.org/<DOI>" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title'),'|',d.get('publication_year'),'|',((d.get('primary_location') or {}).get('source') or {}).get('display_name'))"

# by arXiv id
curl -s --max-time 20 "https://export.arxiv.org/api/query?id_list=<ID>" | grep -E "<title>|<published>|<name>"
```

Confirm **author, year, and venue** match what the digest will claim — this is
CLAUDE.md's standing rule ("Verify any new reference by web search before
citing"), applied here.

Drop anything that fails to resolve or whose metadata disagrees, and note the
drop in the digest. **Downgrade `cite` -> `consider`** rather than guessing at a
detail. Note that arXiv must be **https**: plain `http` 301s and returns an
empty body.

---

## Step 4 — Write the digest

Write to `$REPO/.paper-radar/digests/YYYY-MM-DD.md`, following
`reference/digest_template.md`.

Lead with what matters. If nothing survived screening, say exactly that in one
line and stop — do not manufacture content. **A quiet day is the expected
result, not a failure.** Padding a digest to look productive wastes the author's
time and trains him to stop reading it.

Every item must carry a resolving link. Mark anything unverified as such,
explicitly.

---

## Step 5 — Stage accepted insertions on a branch

Only for **high-confidence `cite`** items that survived Step 3. If there are
none, skip this step and say so.

The working tree usually holds uncommitted work, and much of the repo's apparent
diff is CRLF line-ending churn (`core.autocrlf` is unset, so roughly half the
"modified" files differ only in line endings — 29 files by `git diff --stat`,
15 by `--ignore-all-space`). Therefore:

- **Never** `git add -A`, `git add .`, `git commit -a`, `git stash`, or
  `git checkout` in the user's working tree. A blanket `git add` would sweep
  thousands of phantom line-ending changes into the commit and make the diff
  unreviewable.
- Always name each edited file explicitly in `git add`.

### The delete-permission problem — read this before trying to commit

The Cowork mount is **create/write but no-delete by default**. Git cannot
commit under that restriction: it must unlink its own `.lock` files. The failure
looks like this, and is not a bug in your commands:

```
warning: unable to unlink '.git/index.lock': Operation not permitted
fatal: cannot lock ref 'HEAD': Unable to create '...HEAD.lock': File exists.
```

Deletion may or may not be enabled for this folder on any given run.
**Probe it first, cheaply, before creating any worktree:**

```bash
cd "$REPO" && touch ._radar_probe && rm -f ._radar_probe 2>/dev/null \
  && echo "DELETE_OK" || echo "DELETE_BLOCKED"
```

- `DELETE_OK` → take **Path A** (branch).
- `DELETE_BLOCKED` → take **Path B** (patch). In an interactive session you may
  instead call the `allow_cowork_file_delete` tool and re-probe, but it needs
  human approval, so a 6am run must assume Path B.

### Path A — branch (preferred)

```bash
cd "$REPO"
DATE=$(date +%F)
git worktree add "/tmp/radar-$DATE" -b "paper-radar/$DATE" HEAD
```

The worktree is built from `HEAD`, so it sees a **clean tree** and the user's
uncommitted work is untouched. Apply insertions inside `/tmp/radar-$DATE` only,
then:

```bash
cd "/tmp/radar-$DATE"
git add papers/interstellar_AI_fermi_paper.md   # name each file explicitly
git -c user.email=radar@local -c user.name="Paper Radar" \
    commit -m "paper-radar $DATE: <n> insertion(s) across <m> paper(s)"
cd "$REPO" && git worktree remove "/tmp/radar-$DATE"
```

Review command for the user: `git diff main..paper-radar/YYYY-MM-DD`

### Path B — patch file (fallback, always works)

Clone to sandbox-local disk, where git has full permissions, and hand back a
patch. Writing a *new* file into the repo is create-only, so it always succeeds:

```bash
DATE=$(date +%F)
rm -rf /tmp/radar-clone
git clone -q "$REPO" /tmp/radar-clone
cd /tmp/radar-clone && git checkout -q -b "paper-radar/$DATE"
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
branch is a convenience. Then clean up after yourself — a half-finished git
operation can leave lock files that break the user's *next* git command on
Windows:

```bash
cd "$REPO"
git worktree remove --force "/tmp/radar-$DATE" 2>/dev/null
git worktree prune
find .git -name "*.lock" -delete 2>/dev/null
```

Leave the repo exactly as found: same branch, same modified-file count, same
HEAD. Verify it before reporting done.

---

## Step 6 — Mark seen (last, and only on success)

Only after the digest is written, and only if the sweep completed:

```bash
cd "$REPO"
python3 .paper-radar/search.py --mark-seen-from /tmp/candidates.json
```

This is deliberately the final step. Everything in `candidates.json` — including
what was screened out — is recorded so it never resurfaces, which is what keeps
subsequent mornings quiet. Run it too early and a crash mid-run buries papers
that were never reported. The script refuses to mark an incomplete sweep.

---

## Step 7 — Email the summary (best-effort, never blocking)

After the digest is written (and regardless of whether anything was staged), run:

    python3 .paper-radar/send_digest_email.py

It emails a compact summary — staged titles, flagged titles, counts — to the
address configured in `.paper-radar/.env` (RADAR_SMTP_* / RADAR_EMAIL_TO). With
no credentials present it prints one line and exits 0; a send failure must not
fail the run. Never print or log the credential values.

## Reporting back

Two or three sentences: how many candidates were swept, what survived, whether a
branch was created. Link the digest. Do not recap the pipeline.

If nothing was found, say so plainly. Do not apologise for a quiet day.

---

## Tuning

- **Queries**: `.paper-radar/queries.json`, hand-curated per paper. Do not
  auto-generate them from paper titles — naive extraction returns von Neumann
  *algebras* for a von Neumann *probe* query.
- **Too much noise from one paper?** Add the offending phrase to that paper's
  `exclude` list, or to `defaults.exclude` if it is a general homonym. Prefer a
  broad query plus a sharp exclude over a narrow query; it preserves recall.
- **Semantic Scholar**: optional, off unless `S2_API_KEY` is set in the
  environment or in `.paper-radar/.env` (gitignored). Unauthenticated it shares
  a saturated 1000 req/s pool across all anonymous users and mostly returns 429;
  a key buys a private 1 req/s. Apply at
  https://www.semanticscholar.org/product/api#api-key-form
- **Backlog sweep**: `--baseline --since 2015-01-01` for a wide first pass, but
  expect thousands of candidates. Better done one paper at a time:
  `--paper fermi --since 2015-01-01`.
- **Re-surface everything**: `--ignore-seen`, or reset `keys` to `{}` in
  `.paper-radar/seen.json`.
