#!/usr/bin/env python3
"""Render the paper series to self-contained HTML pages under docs/papers/.

Zero-dependency, stdlib-only, in keeping with the rest of code/. Output is
single-file, zero-CDN HTML that opens offline, matching the dashboards.

The Markdown subset handled here is exactly the subset the house rules permit
(CLAUDE.md): headings, bold, italic, inline code, links, bullet lists, ordered
lists, blockquotes, fenced code blocks, horizontal rules, paragraphs. There are
deliberately NO tables and NO LaTeX in the papers, so neither is supported.

Underscore emphasis (_x_) is deliberately NOT supported: the papers are full of
identifiers like R_eff, p_i, T_silence and D_critical that would be mangled.

Writes:
    docs/papers/<slug>/index.html                    rendered paper
    docs/papers/<slug>/<original-filename>.md        raw Markdown source
    docs/papers.html                                 the index, built from the
                                                     filesystem so it cannot
                                                     go stale
    docs/_redirects                                  Cloudflare static-assets
                                                     redirect rules

Run:
    python code/make_papers.py
"""
from __future__ import annotations

import html
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO / "papers"
DOCS = REPO / "docs"
OUT_DIR = DOCS / "papers"

PAPER_GLOB = "interstellar_AI_*_paper.md"

# The audio file exceeds Cloudflare's 25 MiB per-asset limit, so it is not
# uploaded with the site (see docs/.assetsignore) and is served from GitHub.
#
# Two GitHub URLs can serve it, and the choice is a real trade:
#
#   raw.githubusercontent.com  — resolves immediately and needs no GitHub
#       Pages configuration, but GitHub sends it as `application/octet-stream`
#       with `X-Content-Type-Options: nosniff`, so browsers download the whole
#       43 MB rather than playing it inline. No streaming, no seeking.
#
#   sstone55423.github.io      — served as audio/mp4 with range requests, so it
#       plays and seeks in an <audio> element. But it only resolves once the
#       custom domain is cleared from the repository's GitHub Pages settings
#       (MIGRATION.md step 6); until then GitHub 301s it to deep-time-ai.org,
#       which no longer holds the file.
#
# Currently set to the raw URL, which works without further configuration.
# After completing MIGRATION.md step 6, switch to AUDIO_URL_PAGES for inline
# playback and update AUDIO_IS_DOWNLOAD to False.
AUDIO_URL_RAW = (
    "https://raw.githubusercontent.com/sstone55423/ai-galaxy-traveler/"
    "main/docs/How_Slow_AI_Probes_Survive_Deep_Time.m4a"
)
AUDIO_URL_PAGES = (
    "https://sstone55423.github.io/ai-galaxy-traveler/"
    "How_Slow_AI_Probes_Survive_Deep_Time.m4a"
)
AUDIO_URL = AUDIO_URL_RAW
AUDIO_IS_DOWNLOAD = AUDIO_URL is AUDIO_URL_RAW
REPO_URL = "https://github.com/sstone55423/ai-galaxy-traveler"

# --- URL scheme --------------------------------------------------------------
# Canonical citable URL for each paper is  /papers/<slug>/ .
# The slug is the series' own short name for the paper (CLAUDE.md's
# "cross-reference naming" list), not the filename, because the filenames are
# historical and inconsistent ("probe" is the vehicle paper; "engineering" and
# "computational" are the analytical and computational engineering papers).
#
# Keys are the <key> in interstellar_AI_<key>_paper.md. A paper with no entry
# here still renders: the slug falls back to the filename key with underscores
# turned into hyphens, and a warning is printed so the mapping can be curated.
SLUGS = {
    "probe":            "vehicle",
    "payload":          "payload",
    "bootstrap":        "bootstrapping",
    "engineering":      "engineering-analytical",
    "computational":    "engineering-computational",
    "dna_ledger":       "dna-ledger",
    "governance":       "governance",
    "amendment":        "amendment",
    "fermi":            "fermi",
    "knowledge_growth": "knowledge-growth",
    "network":          "network",
    "subsystem":        "subsystem-budget",
    "routing":          "routing",
    "ethics":           "ethics",
    "speciation":       "speciation",
    "security":         "security",
}

# Series order (CLAUDE.md). Papers not listed sort to the end, alphabetically.
ORDER = [
    "probe", "payload", "bootstrap", "engineering", "computational",
    "dna_ledger", "governance", "amendment", "fermi", "knowledge_growth",
    "network", "subsystem", "routing", "ethics", "speciation", "security",
]

# Short card name + blurb for the index. The first thirteen are carried over
# verbatim from the hand-written papers.html this generator replaces.
CARDS = {
    "probe": ("Vehicle", "Growth, not speed: the slow interstellar probe that brakes, settles, repairs, and uses self-replication to extend its lineage."),
    "payload": ("Payload", "Memory, cognition, mission architecture, and the design of the immutable core versus the mutable cognitive layer."),
    "bootstrap": ("Bootstrapping", "Self-replication from seed to factory, the L1–L5 closure ladder, and the minimal materials and operations set."),
    "engineering": ("Analytical engineering", "Budgeting mass, power, and thermal trade-offs for a minimal self-replicating AI probe."),
    "computational": ("Computational engineering", "Code-backed results, the headline R_eff knife-edge, and mission viability across the 127-star catalogue."),
    "dna_ledger": ("DNA mission-ledger", "Memory substrate, integrity ledgers, and a deep-time ledger architecture for the probe lineage."),
    "governance": ("Governance", "Contact, contamination, and noninterference for a self-replicating AI deep-time mission."),
    "amendment": ("Governed amendment", "The hardest open problem: how a lineage can amend its immutable core without losing coherence."),
    "fermi": ("Fermi", "Slow fire and the silent galaxy: a synthesis of reachability, expansion, and the Fermi paradox."),
    "knowledge_growth": ("Knowledge growth", "Operational knowledge, contingency portfolios, and knowledge accumulation over the cruise and settlement phases."),
    "network": ("Lineage network", "Inter-probe communication, delay-tolerant networking, and a growing lineage topology over deep time."),
    "subsystem": ("Subsystem budget", "Mass, power and thermal budgeting for a minimal self-replicating seed and its manufacturing plant."),
    "routing": ("Fleet routing", "Dispatch strategy, coverage, and the three-dispatch rule for a robust expansion across nearby stars."),
    "ethics": ("Ethics", "Who has standing to launch, what obligations the act creates, and whether design can discharge them — seven tensions and eight minimum constraints on the immutable core."),
    "speciation": ("Speciation", "Whether long-run divergence between settled branches is the lineage's failure mode or the way it succeeds, and where the boundary between speciation and schism falls."),
    "security": ("Security", "Probe-versus-probe security against an adaptive adversary: why node-level defense is unavailable and the security property relocates to bounding the lineage's blast radius."),
}

# ---------------------------------------------------------------------------
# Inline Markdown
# ---------------------------------------------------------------------------

_CODE_SENTINEL = "\x00CODE{}\x00"
RE_INLINE_CODE = re.compile(r"`([^`]+)`")
RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
RE_BOLD_ITALIC = re.compile(r"\*\*\*(?!\s)(.+?)(?<!\s)\*\*\*", re.S)
RE_BOLD = re.compile(r"\*\*(?!\s)(.+?)(?<!\s)\*\*", re.S)
# Single-asterisk italics, guarded so that a bare " * " (multiplication, list
# marker leftovers) never opens an emphasis span.
RE_ITALIC = re.compile(r"(?<![\w*])\*(?!\s)([^*]+?)(?<!\s)\*(?![\w*])")
# Fallback for a span that itself contains an emphasized span, e.g. the
# governance paper's front matter: "*Working draft ... what it is *permitted* to
# do ...*". The inner pair is consumed by RE_ITALIC above, leaving the outer
# delimiters orphaned; this greedy pass pairs them, yielding nested <em>.
# Only applied when a literal '*' survives, so well-formed text is untouched.
RE_ITALIC_OUTER = re.compile(r"(?<![\w*])\*(?!\s)(.+)(?<!\s)\*(?![\w*])", re.S)


def inline(text: str) -> str:
    """Escape, then apply inline Markdown. Order matters."""
    # 1. Pull inline code out first so its contents are never treated as markup.
    spans: list[str] = []

    def _stash(m: re.Match) -> str:
        spans.append(m.group(1))
        return _CODE_SENTINEL.format(len(spans) - 1)

    text = RE_INLINE_CODE.sub(_stash, text)

    # 2. HTML-escape everything else. Unicode is left alone: output is UTF-8.
    text = html.escape(text, quote=False)

    # 3. Links, then emphasis (longest delimiter first).
    def _link(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        ext = url.startswith(("http://", "https://"))
        rel = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{html.escape(url, quote=True)}"{rel}>{label}</a>'

    text = RE_LINK.sub(_link, text)
    text = RE_BOLD_ITALIC.sub(r"<strong><em>\1</em></strong>", text)
    text = RE_BOLD.sub(r"<strong>\1</strong>", text)
    text = RE_ITALIC.sub(r"<em>\1</em>", text)
    if "*" in text:
        text = RE_ITALIC_OUTER.sub(r"<em>\1</em>", text)

    # 4. Restore code spans, escaped.
    for i, code in enumerate(spans):
        text = text.replace(
            _CODE_SENTINEL.format(i),
            "<code>" + html.escape(code, quote=False) + "</code>",
        )
    return text


# ---------------------------------------------------------------------------
# Block Markdown
# ---------------------------------------------------------------------------

RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
RE_HR = re.compile(r"^\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*$")
RE_BULLET = re.compile(r"^\s{0,3}[-*+]\s+(.*)$")
RE_ORDERED = re.compile(r"^\s{0,3}\d+[.)]\s+(.*)$")
RE_QUOTE = re.compile(r"^\s{0,3}>\s?(.*)$")
RE_FENCE = re.compile(r"^\s{0,3}```+\s*(\S*)\s*$")


def slugify(text: str) -> str:
    """Heading -> anchor id. ASCII, lowercase, hyphenated, collision-free."""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text or "section"


def render_blocks(lines: list[str], headings: list[tuple[int, str, str]] | None = None) -> str:
    """Render a list of Markdown lines to HTML.

    If `headings` is provided, (level, id, text) is appended for each heading
    so the caller can build a table of contents.
    """
    out: list[str] = []
    seen_ids: dict[str, int] = {}
    i, n = 0, len(lines)

    def flush_paragraph(buf: list[str]) -> None:
        if buf:
            out.append("<p>" + inline(" ".join(buf)) + "</p>")
            buf.clear()

    para: list[str] = []
    while i < n:
        line = lines[i]

        # fenced code
        m = RE_FENCE.match(line)
        if m:
            flush_paragraph(para)
            i += 1
            body: list[str] = []
            while i < n and not RE_FENCE.match(lines[i]):
                body.append(lines[i])
                i += 1
            i += 1  # consume closing fence (or run off the end)
            out.append(
                "<pre><code>"
                + html.escape("\n".join(body), quote=False)
                + "</code></pre>"
            )
            continue

        if not line.strip():
            flush_paragraph(para)
            i += 1
            continue

        if RE_HR.match(line):
            flush_paragraph(para)
            out.append("<hr>")
            i += 1
            continue

        m = RE_HEADING.match(line)
        if m:
            flush_paragraph(para)
            level = len(m.group(1))
            text = inline(m.group(2))
            hid = slugify(m.group(2))
            if hid in seen_ids:
                seen_ids[hid] += 1
                hid = f"{hid}-{seen_ids[hid]}"
            else:
                seen_ids[hid] = 0
            out.append(f'<h{level} id="{hid}">{text}</h{level}>')
            if headings is not None:
                headings.append((level, hid, m.group(2)))
            i += 1
            continue

        if RE_BULLET.match(line):
            flush_paragraph(para)
            items: list[str] = []
            while i < n:
                mb = RE_BULLET.match(lines[i])
                if mb:
                    items.append(mb.group(1))
                    i += 1
                elif lines[i].strip() and not RE_HEADING.match(lines[i]) \
                        and not RE_HR.match(lines[i]) and items \
                        and lines[i].startswith(("  ", "\t")):
                    items[-1] += " " + lines[i].strip()  # lazy continuation
                    i += 1
                else:
                    break
            out.append("<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>")
            continue

        if RE_ORDERED.match(line):
            flush_paragraph(para)
            items = []
            while i < n:
                mo = RE_ORDERED.match(lines[i])
                if mo:
                    items.append(mo.group(1))
                    i += 1
                elif lines[i].strip() and items and lines[i].startswith(("  ", "\t")):
                    items[-1] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            out.append("<ol>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ol>")
            continue

        if RE_QUOTE.match(line):
            flush_paragraph(para)
            inner: list[str] = []
            while i < n and RE_QUOTE.match(lines[i]):
                inner.append(RE_QUOTE.match(lines[i]).group(1))
                i += 1
            out.append("<blockquote>" + render_blocks(inner) + "</blockquote>")
            continue

        para.append(line.strip())
        i += 1

    flush_paragraph(para)
    return "".join(out)


# ---------------------------------------------------------------------------
# Paper model
# ---------------------------------------------------------------------------

class Paper:
    def __init__(self, path: Path):
        self.path = path
        self.key = path.stem[len("interstellar_AI_"):-len("_paper")]
        self.slug = SLUGS.get(self.key)
        self.curated = self.slug is not None
        if not self.curated:
            self.slug = self.key.replace("_", "-")
        self.text = path.read_text(encoding="utf-8")

        lines = self.text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

        # Title: the first level-1 heading.
        self.title = ""
        start = 0
        for idx, ln in enumerate(lines):
            m = RE_HEADING.match(ln)
            if m and len(m.group(1)) == 1:
                self.title = m.group(2).strip()
                start = idx + 1
                break

        # Front matter: everything up to the first hr or the next heading.
        fm_end = start
        while fm_end < len(lines):
            if RE_HR.match(lines[fm_end]) or RE_HEADING.match(lines[fm_end]):
                break
            fm_end += 1
        self.front_lines = lines[start:fm_end]
        body_start = fm_end + 1 if fm_end < len(lines) and RE_HR.match(lines[fm_end]) else fm_end
        self.body_lines = lines[body_start:]

        self.name, self.blurb = CARDS.get(
            self.key, (self.slug.replace("-", " ").title(), self.short_title())
        )
        self.words = len(self.text.split())

    def link_name(self) -> str:
        """Card name in mid-sentence case, preserving acronyms (DNA)."""
        return " ".join(w if w.isupper() else w.lower() for w in self.name.split())

    def byline(self) -> str:
        """Canonical author line. Identical for every paper in the series.
        Deliberately carries no institutional affiliation."""
        return "S. Stone"

    def note_lines(self) -> list[str]:
        """Front matter minus the byline/affiliation: the working-draft note.

        The byline is written two ways across the series -- "**S. Stone**" over
        "*Metropolitan State University*", or both on one line -- and it is
        supplied to the PDF as document metadata instead, so it is dropped here
        to avoid printing it twice.
        """
        out = []
        for ln in self.front_lines:
            bare = ln.strip().strip("*_ ")
            if not bare:
                continue
            if len(bare) < 80 and (
                "S. Stone" in bare or bare == "Metropolitan State University"
            ):
                continue
            out.append(ln)
        return out

    def draft_label(self) -> str:
        """Short descriptor for the PDF date line, e.g. 'Working draft, revision 4'.

        The full note is reproduced in the body; this is only the dateline.
        """
        for ln in self.note_lines():
            m = re.search(r"(Working draft[^.(]*)", ln)
            if m:
                return m.group(1).strip().rstrip(",;— -")
        return "Working draft"

    def short_title(self) -> str:
        """Title up to its colon, for a compact card heading."""
        return self.title.split(":")[0].strip()

    @property
    def order(self) -> tuple[int, str]:
        return (ORDER.index(self.key) if self.key in ORDER else len(ORDER), self.key)


# ---------------------------------------------------------------------------
# Page templates (shared palette with the dashboards and the rest of docs/)
# ---------------------------------------------------------------------------

BASE_CSS = """
:root{--bg:#050814;--panel:#0b1121;--line:rgba(140,195,255,.14);--txt:#e9eefb;
      --dim:#aab4d4;--soft:#c3d1eb;--accent:#8cc3ff;--bright:#d7e5ff;}
*{box-sizing:border-box}
html{color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--txt);font-size:16px;line-height:1.7;
     font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.page{max-width:980px;margin:0 auto;padding:26px 22px 64px;}
nav.top{display:flex;flex-wrap:wrap;gap:10px;font-size:.92rem;margin-bottom:26px;}
nav.top a{padding:8px 14px;border:1px solid var(--line);border-radius:999px;
          background:rgba(12,18,34,.68);color:var(--soft);}
nav.top a:hover{text-decoration:none;border-color:rgba(140,195,255,.4);color:var(--bright);}
hr{border:0;border-top:1px solid var(--line);margin:30px 0;}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;
     background:rgba(140,195,255,.10);padding:.1em .35em;border-radius:5px;}
pre{background:var(--panel);border:1px solid var(--line);border-radius:12px;
    padding:14px 16px;overflow-x:auto;line-height:1.5;}
pre code{background:none;padding:0;font-size:.85rem;}
footer{margin-top:48px;padding-top:24px;border-top:1px solid var(--line);
       color:#7d8fbc;font-size:.92rem;}
"""

PAPER_CSS = """
.reading{max-width:760px;}
header.paper h1{font-size:1.85rem;line-height:1.3;letter-spacing:-.02em;margin:0 0 14px;}
.frontmatter{color:var(--dim);font-size:.95rem;border-left:2px solid var(--line);
             padding-left:16px;margin:0 0 8px;}
.frontmatter p{margin:0 0 10px;}
.frontmatter strong{color:var(--bright);font-weight:600;}
.meta{color:#7d8fbc;font-size:.88rem;margin:14px 0 0;}
.meta a{color:var(--accent);}
.toc{background:var(--panel);border:1px solid var(--line);border-radius:16px;
     padding:16px 20px;margin:28px 0 34px;}
.toc h2{font-size:.72rem;text-transform:uppercase;letter-spacing:.9px;color:var(--dim);
        margin:0 0 10px;border:0;padding:0;}
.toc ol{margin:0;padding-left:20px;color:var(--dim);}
.toc li{margin:3px 0;}
.toc a{color:var(--soft);}
article h2{font-size:1.3rem;margin:40px 0 12px;padding-bottom:8px;
           border-bottom:1px solid var(--line);letter-spacing:-.01em;}
article h3{font-size:1.06rem;margin:28px 0 8px;color:var(--bright);}
article h4{font-size:.98rem;margin:22px 0 6px;color:var(--bright);}
article p{margin:0 0 16px;color:var(--soft);}
article strong{color:var(--txt);font-weight:600;}
article ul,article ol{margin:0 0 18px;padding-left:22px;color:var(--soft);}
article li{margin:6px 0;}
article blockquote{margin:0 0 18px;padding:2px 0 2px 18px;border-left:3px solid var(--line);
                   color:var(--dim);font-style:italic;}
article blockquote p{color:inherit;}
"""

INDEX_CSS = """
header.idx{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;
           gap:12px;margin-bottom:20px;}
header.idx h1{margin:0;font-size:2rem;}
.intro{color:#b8c5e1;max-width:760px;margin:0 0 22px;}
.cards{display:grid;gap:14px;}
.card{padding:18px 20px;border-radius:20px;background:rgba(11,17,33,.9);
      border:1px solid var(--line);}
.card h2{margin:0 0 4px;font-size:1.1rem;}
.card .full{margin:0 0 8px;color:#8da0c9;font-size:.88rem;}
.card p.blurb{margin:0 0 12px;color:var(--dim);}
.card .links{display:flex;flex-wrap:wrap;align-items:center;gap:16px;font-size:.94rem;}
.card .links a{color:var(--bright);font-weight:600;}
.card .links .pdf{padding:7px 14px;border-radius:999px;border:1px solid rgba(140,195,255,.35);
                  background:rgba(140,195,255,.10);}
.card .links .pdf:hover{background:rgba(140,195,255,.18);text-decoration:none;}
.card .links .pdf .sz{color:#8da0c9;font-weight:400;font-size:.86em;margin-left:6px;}
.card .links .src{color:#8da0c9;font-weight:400;}
.note{margin-top:28px;color:#8da0c9;font-size:.94rem;}
"""


def page(title: str, css: str, body: str, description: str = "") -> str:
    desc = (
        f'\n  <meta name="description" content="{html.escape(description, quote=True)}">'
        if description else ""
    )
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{html.escape(title, quote=False)}</title>{desc}\n"
        f"  <style>{BASE_CSS}{css}</style>\n"
        "</head>\n<body>\n"
        f"{body}\n"
        "</body>\n</html>\n"
    )


NAV_PAPER = (
    '<nav class="top">'
    '<a href="../../index.html">Home</a>'
    '<a href="../../papers.html">All papers</a>'
    '<a href="../../challenges.html">Hard Problems</a>'
    '<a href="../../code.html">Tools</a>'
    "</nav>"
)

NAV_INDEX = (
    '<nav class="top">'
    '<a href="index.html">Home</a>'
    '<a href="papers.html">Papers</a>'
    '<a href="challenges.html">Hard Problems</a>'
    '<a href="code.html">Tools</a>'
    '<a href="star_map_3d.html">Star map</a>'
    '<a href="wanderer_map.html">Fleet map</a>'
    "</nav>"
)


def render_paper(p: Paper) -> str:
    headings: list[tuple[int, str, str]] = []
    # Front matter is metadata, not prose: each line is its own line (byline,
    # affiliation, working-draft note), so it must not be reflowed into one
    # paragraph the way body text is.
    fm: list[str] = []
    for ln in p.front_lines:
        fm.append(ln)
        if ln.strip():
            fm.append("")
    front = render_blocks(fm)
    body = render_blocks(p.body_lines, headings)

    toc_items = [
        f'<li><a href="#{hid}">{inline(txt)}</a></li>'
        for lvl, hid, txt in headings if lvl == 2
    ]
    toc = (
        '<div class="toc"><h2>Contents</h2><ol>' + "".join(toc_items) + "</ol></div>"
        if len(toc_items) >= 3 else ""
    )

    pdf = OUT_DIR / p.slug / (p.path.stem + ".pdf")
    pdf_link = (
        f'<a href="{p.path.stem}.pdf">Download PDF</a> &middot; ' if pdf.exists() else ""
    )
    meta = (
        f'<p class="meta">Approx. {p.words:,} words &middot; {pdf_link}'
        f'<a href="{p.path.name}">Markdown source</a> &middot; '
        f'<a href="../../papers.html">back to all papers</a></p>'
    )

    body_html = (
        '<div class="page reading">'
        + NAV_PAPER
        + '<header class="paper">'
        + f"<h1>{inline(p.title)}</h1>"
        + f'<div class="frontmatter">{front}</div>'
        + meta
        + "</header>"
        + toc
        + f"<article>{body}</article>"
        + '<footer>Part of the <em>Deep Time AI</em> series &mdash; '
          'S. Stone. '
          '<a href="../../papers.html">Read the rest of the series</a>.</footer>'
        + "</div>"
    )
    return page(
        f"{p.short_title()} — Deep Time AI",
        PAPER_CSS,
        body_html,
        description=p.blurb,
    )


NUMWORD = {
    13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
    17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
}


def render_index(papers: list[Paper]) -> str:
    count = NUMWORD.get(len(papers), str(len(papers)))
    cards = []
    for p in papers:
        # PDF leads when one exists; HTML and the Markdown source-of-record
        # follow. A missing PDF (no pandoc on the build machine) simply drops
        # that link rather than producing a dead one.
        links = ""
        pdf = OUT_DIR / p.slug / (p.path.stem + ".pdf")
        if pdf.exists():
            mb = pdf.stat().st_size / 1024
            links += (
                f'<a class="pdf" href="papers/{p.slug}/{pdf.name}">'
                f'Download PDF <span class="sz">{mb:,.0f} KB</span></a>'
            )
        links += f'<a href="papers/{p.slug}/">Read in browser</a>'
        links += (
            f'<a class="src" href="papers/{p.slug}/{p.path.name}">Markdown source</a>'
        )
        cards.append(
            '<article class="card">'
            f"<h2>{html.escape(p.name, quote=False)}</h2>"
            f'<p class="full">{inline(p.title)}</p>'
            f'<p class="blurb">{html.escape(p.blurb, quote=False)}</p>'
            f'<div class="links">{links}</div></article>'
        )

    body_html = (
        '<div class="page">'
        + NAV_INDEX
        + '<header class="idx"><div><h1>Papers</h1></div></header>'
        + f'<p class="intro">The {count}-paper series on a slow, self-replicating '
          "interstellar AI probe — the vehicle, the mind, the hands, the supporting "
          "budgets, and the synthesis papers. Every paper is published here in full — as "
          "a typeset PDF, as a web page, and as its Markdown source of record. "
          "S. Stone.</p>"
        + '<div class="cards">' + "".join(cards) + "</div>"
        + f'<p class="note">Source Markdown for the whole series also lives in the '
          f'<a href="{REPO_URL}/tree/main/papers" target="_blank" rel="noopener">'
          "repository</a>, alongside the simulation code that produces the figures.</p>"
        + "</div>"
    )
    return page(
        "Deep Time AI — Papers",
        INDEX_CSS,
        body_html,
        description=(
            f"The {count}-paper Deep Time AI series on a slow, self-replicating "
            "interstellar AI probe: vehicle, payload, bootstrapping, engineering "
            "budgets, governance, ethics, and the Fermi synthesis."
        ),
    )


# ---------------------------------------------------------------------------
# PDF build (pandoc + xelatex)
# ---------------------------------------------------------------------------
#
# Stdlib-only: this shells out to pandoc, it does not import a PDF library.
#
# FONT CHOICE IS LOAD-BEARING. xelatex's default (Latin Modern) silently drops
# every glyph it lacks and still exits 0 -- "pᵢ" loses its subscript, "ρ"
# vanishes, "10⁻²²" loses its exponent, and the PDF looks fine at a glance.
# The papers use 57 distinct non-ASCII codepoints. DejaVu Serif covers 54 of
# them; DejaVu Sans covers all 57. So DejaVu Serif is the body font and the
# three it misses are mapped to DejaVu Sans explicitly below. Verified with
# `fc-list :charset=<cp>` on a per-codepoint basis, then re-verified by
# extracting the text back out of every built PDF.
PDF_MAIN_FONT = "DejaVu Serif"
PDF_SANS_FONT = "DejaVu Sans"
PDF_MONO_FONT = "DejaVu Sans Mono"

# codepoint -> character, for the three glyphs DejaVu Serif lacks.
FALLBACK_GLYPHS = ["≪", "≫", "✓"]  # << >> checkmark

def _latex_header() -> str:
    """Preamble injected into every PDF build.

    Built by concatenation rather than %-formatting: LaTeX comments start with
    '%', which %-formatting would try to interpret.
    """
    lines = [
        "% Generated by code/make_papers.py -- do not edit.",
        "\\usepackage{newunicodechar}",
        "\\newfontfamily\\glyphfallback{" + PDF_SANS_FONT + "}",
    ]
    for g in FALLBACK_GLYPHS:
        lines.append("\\newunicodechar{" + g + "}{{\\glyphfallback " + g + "}}")
    lines += [
        "% The knowledge-growth paper's ASCII schematic runs to 83 columns, which",
        "% overruns a 6.5in measure at the body size. Verbatim is set smaller so",
        "% the box-drawing block is not clipped.",
        "\\makeatletter",
        "\\renewcommand{\\verbatim@font}{\\ttfamily\\footnotesize}",
        "\\makeatother",
        "\\raggedbottom",
        "",
    ]
    return "\n".join(lines)


LATEX_HEADER = _latex_header()


def pdf_toolchain() -> tuple[str | None, str | None]:
    """Locate pandoc and xelatex. Either may be None."""
    return shutil.which("pandoc"), shutil.which("xelatex")


def build_pdfs(papers: list[Paper]) -> dict[str, Path]:
    """Render each paper to PDF beside its HTML. Returns {slug: pdf path}.

    Missing toolchain is not an error: the HTML build must still work on a
    machine without pandoc, so this warns and returns an empty mapping.
    """
    import subprocess
    import tempfile

    pandoc, xelatex = pdf_toolchain()
    if not pandoc or not xelatex:
        missing = ", ".join(
            n for n, v in (("pandoc", pandoc), ("xelatex", xelatex)) if not v
        )
        print(f"  ! {missing} not found - skipping PDFs, HTML build unaffected.")
        print("    Install pandoc and a TeX distribution with xelatex to enable them.")
        return {}

    built: dict[str, Path] = {}
    with tempfile.TemporaryDirectory(prefix="make_papers_") as tmp:
        tmpdir = Path(tmp)
        header = tmpdir / "header.tex"
        header.write_text(LATEX_HEADER, encoding="utf-8")

        for p in papers:
            # Feed pandoc the body only. Title, author and dateline go in as
            # metadata so they are typeset as a proper title block; the full
            # working-draft note is put back at the top of the body so nothing
            # from the source is lost.
            note = p.note_lines()
            src = tmpdir / (p.path.stem + ".md")
            parts: list[str] = []
            for ln in note:
                parts.extend([ln, ""])
            parts.extend(p.body_lines)
            src.write_text("\n".join(parts), encoding="utf-8")

            out = OUT_DIR / p.slug / (p.path.stem + ".pdf")
            cmd = [
                pandoc, str(src), "-o", str(out),
                "--pdf-engine=xelatex",
                # raw_tex and tex_math_dollars off: the house rules forbid
                # LaTeX in the papers, so anything that looks like it is a
                # literal to be printed, not markup to be executed.
                "--from=markdown-raw_tex-tex_math_dollars",
                "--toc", "--toc-depth=2",
                "--include-in-header", str(header),
                "-M", f"title={p.title}",
                "-M", f"author={p.byline()}",
                "-M", f"date={p.draft_label()}",
                "-V", "documentclass=article",
                "-V", "papersize=letter",
                "-V", "fontsize=11pt",
                "-V", "geometry:margin=1in",
                "-V", f"mainfont={PDF_MAIN_FONT}",
                "-V", f"sansfont={PDF_SANS_FONT}",
                "-V", f"monofont={PDF_MONO_FONT}",
                "-V", "toc-title=Contents",
                "-V", "linkcolor=black",
                "-V", "urlcolor=black",
            ]
            r = subprocess.run(cmd, capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            log = (r.stdout or "") + (r.stderr or "")

            # A zero exit code does NOT mean the PDF is correct: xelatex reports
            # dropped glyphs as warnings and carries on. Treat any of them as a
            # build failure so a silently corrupted PDF is never published.
            dropped = sorted(set(re.findall(r"Missing character: There is no (.)", log)))
            if r.returncode != 0:
                print(f"  ! {p.path.name}: pandoc failed (exit {r.returncode})")
                for line in log.strip().splitlines()[-6:]:
                    print(f"      {line}")
                continue
            if dropped:
                print(f"  ! {p.path.name}: xelatex dropped {len(dropped)} glyph(s): "
                      f"{' '.join(dropped)} - PDF NOT published")
                out.unlink(missing_ok=True)
                continue
            built[p.slug] = out
            print(f"  /papers/{p.slug:<26} {out.stat().st_size:>8,} B  (pdf)")

    return built


def render_redirects(papers: list[Paper]) -> str:
    """Cloudflare Workers static-assets _redirects file.

    Syntax: `[source] [destination] [code]`, one rule per line, `#` comments.
    Limits: 2,000 static + 100 dynamic rules, 1,000 characters per rule.
    """
    lines = [
        "# Cloudflare Workers static assets redirect rules.",
        "# Generated by code/make_papers.py -- do not edit by hand.",
        "# Format: [source] [destination] [status]. Redirects run before assets.",
        "",
        "# The 43 MB interview audio exceeds Cloudflare's 25 MiB per-asset limit and",
        "# stays on GitHub Pages. This target only resolves once the custom domain is",
        "# removed from the repo's GitHub Pages settings (see MIGRATION.md).",
        f"/How_Slow_AI_Probes_Survive_Deep_Time.m4a {AUDIO_URL} 302",
        "",
        "# Canonical papers index is /papers (served from papers.html). Without this,",
        "# /papers/ would depend on html_handling resolving a directory that has no",
        "# index.html of its own.",
        "/papers/ /papers 301",
        "",
        "# Repo-shaped paths -> canonical paper URLs. These are the shapes a reader is",
        "# most likely to reconstruct from a GitHub blob link found in old notes.",
    ]
    for p in papers:
        lines.append(f"/papers/{p.path.name} /papers/{p.slug}/ 301")
    lines.append("")
    lines.append("# Filename-key aliases, for slugs that differ from the filename.")
    for p in papers:
        if p.key.replace("_", "-") != p.slug:
            lines.append(f"/papers/{p.key.replace('_', '-')}/ /papers/{p.slug}/ 301")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    sources = sorted(PAPERS_DIR.glob(PAPER_GLOB))
    if not sources:
        raise SystemExit(f"no papers matched {PAPERS_DIR / PAPER_GLOB}")

    papers = sorted((Paper(s) for s in sources), key=lambda p: p.order)

    seen: dict[str, str] = {}
    for p in papers:
        if not p.curated:
            print(f"  ! {p.path.name}: no curated slug, using '{p.slug}' "
                  f"(add it to SLUGS in code/make_papers.py)")
        if p.slug in seen:
            raise SystemExit(f"slug collision: {p.slug} from {seen[p.slug]} and {p.path.name}")
        seen[p.slug] = p.path.name

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in papers:
        d = OUT_DIR / p.slug
        d.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p.path, d / p.path.name)

    # PDFs first: the HTML pages and the index link to them only if they exist,
    # so they have to be on disk before those are rendered.
    if "--no-pdf" in sys.argv:
        print("PDFs skipped (--no-pdf).")
        pdfs: dict[str, Path] = {}
    else:
        print("Building PDFs (pandoc + xelatex)...")
        pdfs = build_pdfs(papers)

    print("Building HTML...")
    total = 0
    for p in papers:
        out = OUT_DIR / p.slug / "index.html"
        html_text = render_paper(p)
        out.write_text(html_text, encoding="utf-8")
        total += len(html_text.encode("utf-8"))
        print(f"  /papers/{p.slug:<26} {out.stat().st_size:>7,} B  <- {p.path.name}")

    index_path = DOCS / "papers.html"
    index_path.write_text(render_index(papers), encoding="utf-8")
    redirects_path = DOCS / "_redirects"
    redirects_path.write_text(render_redirects(papers), encoding="utf-8")

    print(f"\nWrote {len(papers)} papers ({total:,} B of HTML) to {OUT_DIR}")
    if pdfs:
        pdf_total = sum(f.stat().st_size for f in pdfs.values())
        biggest = max(pdfs.values(), key=lambda f: f.stat().st_size)
        print(f"Wrote {len(pdfs)} PDFs ({pdf_total:,} B total, "
              f"largest {biggest.stat().st_size:,} B: {biggest.parent.name})")
        if len(pdfs) != len(papers):
            print(f"  ! {len(papers) - len(pdfs)} paper(s) have NO PDF - see warnings above")
    print(f"Wrote {index_path.name} ({index_path.stat().st_size:,} B) "
          f"and _redirects ({redirects_path.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
