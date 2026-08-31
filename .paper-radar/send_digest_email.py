#!/usr/bin/env python3
"""Email the morning digest summary. Zero-dependency (stdlib smtplib).

Called at the end of the radar workflow (SKILL.md Step 7). Reads SMTP
credentials from .paper-radar/.env (gitignored; never logged):

    RADAR_SMTP_HOST=smtp.gmail.com
    RADAR_SMTP_PORT=587
    RADAR_SMTP_USER=you@gmail.com
    RADAR_SMTP_PASS=your-app-password
    RADAR_EMAIL_TO=scott.stone@my.metrostate.edu
    RADAR_EMAIL_FROM=you@gmail.com        # optional; defaults to USER

Without credentials it exits 0 with a one-line note, so the morning run
never fails on a missing mailbox. Usage:

    python3 .paper-radar/send_digest_email.py                 # latest digest
    python3 .paper-radar/send_digest_email.py 2026-08-31      # specific day
"""
import glob
import os
import re
import smtplib
import ssl
import sys
from email.mime.text import MIMEText

HERE = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(HERE, ".env")
DIGESTS = os.path.join(HERE, "digests")


def load_env():
    if not os.path.exists(ENV_PATH):
        return
    with open(ENV_PATH, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def pick_digest():
    if len(sys.argv) > 1:
        p = os.path.join(DIGESTS, f"{sys.argv[1]}.md")
        return p if os.path.exists(p) else None
    md = sorted(glob.glob(os.path.join(DIGESTS, "20??-??-??.md")))
    return md[-1] if md else None


def summarize(path):
    text = open(path, encoding="utf-8").read()
    day = os.path.basename(path)[:-3]
    head = next((l for l in text.splitlines() if l.startswith("Swept ")), "")
    staged = re.search(r"\*\*(\d+) insertions? staged\*\*", text)
    flagged = re.search(r"(\d+) flagged", text)
    n_staged = int(staged.group(1)) if staged else 0
    n_flagged = int(flagged.group(1)) if flagged else 0

    lines = [f"Paper Radar digest for {day}", "", head, ""]
    # staged item headings: "### <paper> — <section>" then "**Title** — authors"
    if n_staged:
        lines.append(f"STAGED ({n_staged}) — verified, in the patch:")
        block = text.split("## Staged", 1)[-1].split("\n## ", 1)[0]
        for m in re.finditer(r"^### (.+)$\n\n\*\*(.+?)\*\*", block, re.M):
            lines.append(f"  - {m.group(2).strip()}  ->  {m.group(1).strip()}")
        lines.append("")
    if n_flagged:
        lines.append(f"FLAGGED for the author's call ({n_flagged}):")
        for m in re.finditer(r"^- \*\*(.+?)\*\*", text, re.M):
            lines.append(f"  - {m.group(1).strip()}")
        lines.append("")
    lines.append("Full digest: .paper-radar/digests/%s.md in the repo." % day)
    subject = f"Paper Radar {day}: {n_staged} staged, {n_flagged} flagged"
    return subject, "\n".join(lines)


def main():
    load_env()
    host = os.environ.get("RADAR_SMTP_HOST")
    user = os.environ.get("RADAR_SMTP_USER")
    pw = os.environ.get("RADAR_SMTP_PASS")
    to = os.environ.get("RADAR_EMAIL_TO")
    if not all([host, user, pw, to]):
        print("send_digest_email: no SMTP credentials in .env; skipping (this is fine).")
        return 0
    path = pick_digest()
    if not path:
        print("send_digest_email: no digest found; nothing to send.")
        return 0
    subject, body = summarize(path)
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = os.environ.get("RADAR_EMAIL_FROM", user)
    msg["To"] = to
    port = int(os.environ.get("RADAR_SMTP_PORT", "587"))
    with smtplib.SMTP(host, port, timeout=60) as s:
        s.starttls(context=ssl.create_default_context())
        s.login(user, pw)
        s.send_message(msg)
    print(f"send_digest_email: sent '{subject}' to {to}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
