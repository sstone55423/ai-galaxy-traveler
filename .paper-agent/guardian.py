#!/usr/bin/env python3
"""Consistency-guardian agent for the interstellar-AI paper series.

A LangChain tool-calling agent (Claude via langchain-anthropic) that reviews one
paper against the series' house rules. It runs the deterministic checks in
checks.py as a tool, then adds the semantic layer regex cannot do:

  * cross-reference RESOLUTION — when a paper says "the routing paper's
    dispatch mechanics", does the routing paper actually contain that?
  * canonical-number IN CONTEXT — is a stated figure a contradiction of the
    canonical value, or a different quantity that merely looks similar?
  * naming judgment — is a flagged shorthand a real inconsistency or acceptable?

Retrieval here is structural (a section-header index + line-addressed excerpt
reads), not vector embeddings: cross-reference resolution needs exact section
titles, and this keeps the tool free of an embedding model/API — the only
network call is the chat model.

Usage:
    python .paper-agent/guardian.py papers/interstellar_AI_amendment_paper.md
    python .paper-agent/guardian.py --model claude-opus-4-8 <paper>

Requires: pip install -r .paper-agent/requirements.txt, and Claude credentials
(ANTHROPIC_API_KEY, or `ant auth login`).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import checks  # local, zero-dependency

REPO = Path(__file__).resolve().parent.parent
PAPERS = REPO / "papers"

# Canonical short-name → filename, so the agent can resolve "the routing paper".
SHORT_NAMES = {
    "vehicle": "interstellar_AI_probe_paper.md",
    "payload": "interstellar_AI_payload_paper.md",
    "bootstrapping": "interstellar_AI_bootstrap_paper.md",
    "analytical engineering": "interstellar_AI_engineering_paper.md",
    "computational engineering": "interstellar_AI_computational_paper.md",
    "DNA mission-ledger": "interstellar_AI_dna_ledger_paper.md",
    "governance": "interstellar_AI_governance_paper.md",
    "governed-amendment": "interstellar_AI_amendment_paper.md",
    "Fermi": "interstellar_AI_fermi_paper.md",
    "knowledge-growth": "interstellar_AI_knowledge_growth_paper.md",
    "lineage-network": "interstellar_AI_network_paper.md",
    "subsystem budget": "interstellar_AI_subsystem_paper.md",
    "routing": "interstellar_AI_routing_paper.md",
    "ethics": "interstellar_AI_ethics_paper.md",
    "speciation": "interstellar_AI_speciation_paper.md",
}


def _resolve(name: str) -> Path | None:
    p = Path(name)
    if p.is_absolute() and p.exists():
        return p
    cand = REPO / name
    if cand.exists():
        return cand
    cand = PAPERS / name
    if cand.exists():
        return cand
    low = name.lower().replace(" paper", "").strip()
    low = re.sub(r"^the\s+", "", low).strip()
    for short, fn in SHORT_NAMES.items():
        s = short.lower()
        if low == s or low in s or s in low:
            return PAPERS / fn
    return None


# --------------------------------------------------------------------------- #
# Tools (plain functions; wrapped with @tool below once LangChain is imported) #
# --------------------------------------------------------------------------- #
def _run_deterministic_checks(paper: str) -> str:
    path = _resolve(paper)
    if not path:
        return f"ERROR: could not resolve paper {paper!r}"
    findings = checks.review_paper(path)
    return json.dumps(findings, ensure_ascii=False, indent=2)


def _list_section_headers(paper: str) -> str:
    path = _resolve(paper)
    if not path:
        return f"ERROR: could not resolve paper {paper!r}"
    text = path.read_text(encoding="utf-8")
    heads = [
        f"L{text.count(chr(10), 0, m.start()) + 1}: {m.group(1).strip()}"
        for m in re.finditer(r"^(#{1,3}\s+.*)$", text, re.M)
    ]
    return "\n".join(heads) if heads else "(no headers found)"


def _read_excerpt(paper: str, start_line: int = 1, num_lines: int = 40) -> str:
    path = _resolve(paper)
    if not path:
        return f"ERROR: could not resolve paper {paper!r}"
    lines = path.read_text(encoding="utf-8").splitlines()
    start = max(1, int(start_line))
    end = min(len(lines), start + int(num_lines) - 1)
    return "\n".join(f"{i}: {lines[i - 1]}" for i in range(start, end + 1))


def _list_papers(_: str = "") -> str:
    return "\n".join(f"{short}: {fn}" for short, fn in SHORT_NAMES.items())


SYSTEM_PROMPT = """You are the consistency guardian for a fifteen-paper academic \
series on a slow, self-replicating interstellar AI probe (author: S. Stone). \
You review ONE paper at a time against the series' house rules.

House rules (from the project guide):
- Markdown, references only, NO TABLES, NO LaTeX (plain-text math only, e.g. \
`R_eff = Σ p_i V_i`, `10^7 yr`).
- Every reference must be cited in-text; no dangling or uncited references.
- Canonical numbers must be identical across all papers: cruise ~450 km/s; \
Proxima 4.246 ly; catalogue = 127 stars within 100 ly; reference seed ~3,700 kg; \
mature vitamin fraction ~3%; ~4 kW electric / ~16.5 kg U-235; the R_eff headline \
quad 0.48 / 0.94 / 1.39 / 1.85 for 1/2/3/4 offspring; per-node extinction \
0.88 / 0.37 / 0.14 for 2/3/4 offspring.
- Cross-references use canonical names: "the vehicle paper", "the DNA \
mission-ledger paper" (never "the memory paper"), "the governed-amendment \
paper", "the lineage-network paper", "the routing paper", "the governance \
paper", the "analytical engineering paper" vs "computational engineering paper" \
(never merged). When a paper refers to another paper's content by description \
("the routing paper's dispatch mechanics"), that content should actually exist \
in the named paper.

Your workflow:
1. Call run_deterministic_checks on the target paper. These are precise, \
already-verified regex/parse findings — carry the real ones forward.
2. For each deterministic finding, decide if it is a true issue or acceptable, \
citing the evidence. Deterministic findings are candidates, not verdicts.
3. Add SEMANTIC findings regex cannot catch. In particular: pick 2-4 places \
where the paper refers to ANOTHER paper by description, and verify with \
list_section_headers / read_excerpt on that other paper that the referenced \
content actually exists. Flag any that do not resolve.
4. Spot-check any stated canonical number against the list above using \
read_excerpt for context — flag genuine contradictions, ignore different \
quantities that merely resemble a canonical value.

Output a concise Markdown report:
  ## Guardian review: <paper>
  ### Confirmed issues (ranked)   — one bullet each: `severity · Lline · what · fix`
  ### Cross-reference resolution  — which described references you checked and whether they resolve
  ### Dismissed / acceptable      — deterministic flags you judged fine, with why
Keep it tight. Do not invent findings. Ground every claim in a tool result."""


def build_agent(model: str):
    from langchain.agents import AgentExecutor, create_tool_calling_agent
    from langchain_anthropic import ChatAnthropic
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.tools import tool

    run_deterministic_checks = tool(_run_deterministic_checks)
    run_deterministic_checks.name = "run_deterministic_checks"
    run_deterministic_checks.description = (
        "Run the precise regex/parse consistency checks on a paper (by filename "
        "or canonical short-name). Returns a JSON list of findings."
    )
    list_section_headers = tool(_list_section_headers)
    list_section_headers.name = "list_section_headers"
    list_section_headers.description = (
        "List the '#'/'##'/'###' headers (with line numbers) of a paper — use to "
        "resolve a cross-reference to another paper's actual sections."
    )
    read_excerpt = tool(_read_excerpt)
    read_excerpt.name = "read_excerpt"
    read_excerpt.description = (
        "Read a line-numbered excerpt of a paper: (paper, start_line, num_lines)."
    )
    list_papers = tool(_list_papers)
    list_papers.name = "list_papers"
    list_papers.description = "List the series' canonical short-names and filenames."

    tools = [run_deterministic_checks, list_section_headers, read_excerpt, list_papers]
    llm = ChatAnthropic(model=model, max_tokens=4096)  # no temperature: 4.8 rejects non-default
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Review this paper: {paper}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=12)


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Consistency-guardian agent")
    ap.add_argument("paper", help="paper filename or canonical short-name")
    ap.add_argument("--model", default="claude-opus-4-8")
    args = ap.parse_args(argv)

    if not _resolve(args.paper):
        print(f"Could not resolve paper: {args.paper!r}\nKnown papers:\n{_list_papers()}")
        return 2

    try:
        executor = build_agent(args.model)
    except ImportError as e:
        print("LangChain is not installed. Run:\n"
              "  pip install -r .paper-agent/requirements.txt\n"
              f"(import error: {e})")
        return 1

    result = executor.invoke({"paper": args.paper})
    print("\n" + "=" * 70 + "\n")
    print(result["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
