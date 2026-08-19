# Paper Guardian

A consistency & citation checker for the fifteen-paper series. Two layers:

- **`checks.py`** — deterministic, **stdlib-only** checks. Runs offline, no API,
  no dependencies. This is where the reliable findings come from.
- **`guardian.py`** — a LangChain tool-calling agent (Claude via
  `langchain-anthropic`) that runs `checks.py` as a tool and adds the semantic
  judgments regex cannot make: resolving described cross-references against the
  *actual* sections of the named paper, and judging whether a stated number
  contradicts a canonical value or is merely a lookalike.

Kept deliberately out of the repo's zero-dependency `code/` tree — LangChain is
a heavy dependency; it lives here in its own directory with its own venv.

## What it checks (house rules from `CLAUDE.md`)

- No LaTeX (plain-text math only), no Markdown tables.
- Every reference cited in-text; reference list alphabetical.
- Canonical numbers identical across papers (450 km/s, 4.246 ly, 127 stars,
  ~3,700 kg seed, 4 kW / 16.5 kg U-235, R_eff 0.48/0.94/1.39/1.85, …).
- Canonical cross-reference names (never "the memory paper" for the DNA
  mission-ledger paper; the two engineering papers never merged; etc.).

## Deterministic layer — runs now, no setup

```bash
python .paper-agent/checks.py papers/interstellar_AI_fermi_paper.md
python .paper-agent/checks.py --all
```

Each finding is `severity · Lline · check · message`. `high` = house-rule
violation, `medium` = probable (verify), `low` = FYI. Findings are candidates
for a human (or the agent) to confirm, not verdicts.

Real issues it already surfaces:
- the knowledge-growth paper's reference list has entries (Harris 1963, von
  Neumann 1966, Burleigh, Cerf, Merkle, Metzger, Freitas) never cited in its body;
- several papers use non-canonical cross-reference names ("the amendment paper",
  "the network paper", "the contact-governance paper", "the fleet-routing … paper");
- reference-ordering slips in the Fermi and DNA-ledger papers.

## Agent layer — needs deps + a key

```bash
python -m venv .paper-agent/.venv
.paper-agent/.venv/Scripts/pip install -r .paper-agent/requirements.txt   # Windows
# then provide Claude creds: set ANTHROPIC_API_KEY=...   (or `ant auth login`)
.paper-agent/.venv/Scripts/python .paper-agent/guardian.py papers/interstellar_AI_speciation_paper.md
```

The agent uses `claude-opus-4-8` by default (`--model` to override). Its tools —
`run_deterministic_checks`, `list_section_headers`, `read_excerpt`,
`list_papers` — all work offline; only the model call needs the key. Retrieval
is structural (section-header index), not vector embeddings, so there's no
embedding model to run and cross-reference resolution keys off exact titles.

## Design notes

- The deterministic checks are tuned for **precision over recall**: better to
  miss a subtle issue than bury real ones in noise. The seed-mass check anchors
  on the exact phrase "reference seed" because the subsystem paper legitimately
  states component and delta masses near the word "seed".
- Findings degrade gracefully: `checks.py` is importable (`review_paper(path)
  -> list[dict]`), so it can back a git pre-commit hook without the agent.
