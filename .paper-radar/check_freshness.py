#!/usr/bin/env python3
"""Dead-man's switch for the radar. Zero-dependency (stdlib only).

The radar's own failure mode is silence. When the 06:00 run dies -- as it did
on 2026-09-05 and 2026-09-06, when the scheduled job could no longer find the
repo after it moved under AI/projects/ -- there is no error anywhere. No digest
is written, no email arrives, and a missing email looks exactly like a quiet
morning with nothing to report. Both mornings passed unnoticed.

So this check must NOT be part of the radar run: a check that only fires when
the radar works cannot report that the radar stopped working. Run it from an
independent scheduler (a local Windows task is ideal, since the 06:00 job is a
cloud routine and the two then fail independently).

    python3 .paper-radar/check_freshness.py            # print status, exit 1 if stale
    python3 .paper-radar/check_freshness.py --email    # ...and send one alert per day
    python3 .paper-radar/check_freshness.py --max-age 2 --quiet

Exit codes: 0 fresh, 1 stale, 2 cannot tell (missing/unreadable ledger).
"""
import argparse
import datetime
import glob
import json
import os
import re
import smtplib
import ssl
import sys
from email.mime.text import MIMEText

HERE = os.path.dirname(os.path.abspath(__file__))
SEEN = os.path.join(HERE, "seen.json")
DIGESTS = os.path.join(HERE, "digests")
ENV_PATH = os.path.join(HERE, ".env")
# Records the date of the last alert so an hourly scheduler sends one mail a day,
# not twenty-four. Gitignored: it is machine state, not project history.
ALERT_STATE = os.path.join(HERE, ".freshness_alert")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def parse_day(s):
    if not s or not DATE_RE.match(str(s)):
        return None
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def last_run_from_ledger():
    """The ledger's own record of the last completed sweep."""
    if not os.path.exists(SEEN):
        return None, "seen.json not found"
    try:
        with open(SEEN, encoding="utf-8") as fh:
            return parse_day(json.load(fh).get("last_run")), None
    except (json.JSONDecodeError, OSError) as exc:
        return None, f"seen.json unreadable ({exc})"


def newest_digest():
    """Newest dated digest on disk, as a cross-check on the ledger.

    These can disagree, and the disagreement is informative: a digest with no
    ledger update means the sweep died before Step 6, and a ledger update with
    no digest means it died between Step 6 and the write.
    """
    days = sorted(
        d for d in (
            parse_day(os.path.basename(p)[:-3])
            for p in glob.glob(os.path.join(DIGESTS, "20??-??-??.md"))
        ) if d
    )
    return days[-1] if days else None


def expected_run_date(now, run_hour, grace_hours):
    """The date of the most recent run that *should* have finished by `now`.

    Staleness is a function of the clock, not just the calendar. A flat
    "N days behind" rule is wrong at both ends of the day: at 05:00 it calls
    the radar stale before the 06:00 job has had its chance, and at 18:00 it
    calls a radar that plainly missed this morning fresh. So: once the run
    hour plus a grace period has passed, today's run is owed; before that, only
    yesterday's is.
    """
    if now.hour >= run_hour + grace_hours:
        return now.date()
    return now.date() - datetime.timedelta(days=1)


def build_report(run_hour, grace_hours):
    now = datetime.datetime.now()          # local time == the author's clock
    expected = expected_run_date(now, run_hour, grace_hours)
    ledger, err = last_run_from_ledger()
    digest = newest_digest()

    if ledger is None and digest is None:
        return 2, f"paper-radar: CANNOT TELL -- {err or 'no digests and no ledger date'}", None

    # Judge on whichever marker is most recent: the radar is "working" if either
    # a sweep completed or a digest landed.
    latest = max(d for d in (ledger, digest) if d is not None)
    behind = (expected - latest).days

    bits = [f"last_run={ledger or 'none'}", f"newest_digest={digest or 'none'}"]
    if ledger and digest and ledger != digest:
        bits.append("MISMATCH (a run ended between the digest write and Step 6)")
    detail = ", ".join(bits)

    if behind <= 0:
        return 0, (f"paper-radar: FRESH -- up to date as of {expected} "
                   f"(owed run: {expected}). {detail}"), None

    subject = f"Paper Radar STALE: {behind} missed run(s), last was {latest}"
    body = "\n".join([
        f"The paper radar has missed {behind} scheduled run(s).",
        f"It is {now:%Y-%m-%d %H:%M} local; the {run_hour:02d}:00 run for "
        f"{expected} should have finished by now.",
        f"The most recent completed run is {latest}.",
        "",
        f"  {detail}",
        "",
        "The radar fails silently: no digest and no email look identical to a",
        "quiet day with nothing to report. Likely causes, most common first:",
        "",
        "  1. The 06:00 cloud routine cannot find the repo (the folder moved,",
        "     was renamed, or is no longer connected to that routine).",
        "  2. The routine is loading a stale copy of the skill.",
        "  3. The machine was off or offline at 06:00.",
        "",
        "To run it by hand, ask Claude Code to 'run the paper radar'.",
    ])
    return 1, (f"paper-radar: STALE -- {behind} missed run(s); owed {expected}, "
               f"last was {latest}. {detail}"), (subject, body)


def already_alerted_today():
    try:
        with open(ALERT_STATE, encoding="utf-8") as fh:
            return fh.read().strip() == datetime.date.today().isoformat()
    except OSError:
        return False


def record_alert():
    try:
        with open(ALERT_STATE, "w", encoding="utf-8") as fh:
            fh.write(datetime.date.today().isoformat())
    except OSError:
        pass  # best-effort; a repeated mail is better than a crash


def send_alert(subject, body):
    load_env()
    host = os.environ.get("RADAR_SMTP_HOST")
    user = os.environ.get("RADAR_SMTP_USER")
    pw = os.environ.get("RADAR_SMTP_PASS")
    to = os.environ.get("RADAR_EMAIL_TO")
    if not all([host, user, pw, to]):
        print("  (no SMTP credentials in .env; alert not sent)")
        return
    if already_alerted_today():
        print("  (alert already sent today; not repeating)")
        return
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = os.environ.get("RADAR_EMAIL_FROM", user)
    msg["To"] = to
    try:
        with smtplib.SMTP(host, int(os.environ.get("RADAR_SMTP_PORT", "587")),
                          timeout=60) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(user, pw)
            s.send_message(msg)
    except Exception as exc:  # a mail failure must not mask the staleness verdict
        print(f"  (alert send failed: {exc})")
        return
    record_alert()
    print(f"  (alert sent to {to})")


def main():
    ap = argparse.ArgumentParser(description="Report whether the paper radar has gone stale.")
    ap.add_argument("--run-hour", type=int, default=6,
                    help="local hour the radar is scheduled to run (default 6)")
    ap.add_argument("--grace-hours", type=int, default=2,
                    help="hours after --run-hour before a missing run counts as "
                         "stale (default 2, so a slow or retried sweep is not "
                         "reported as a failure)")
    ap.add_argument("--email", action="store_true",
                    help="send an alert if stale (at most one per day)")
    ap.add_argument("--quiet", action="store_true",
                    help="print nothing when fresh; useful for a scheduled task")
    args = ap.parse_args()

    code, line, alert = build_report(args.run_hour, args.grace_hours)
    if not (args.quiet and code == 0):
        print(line)
    if code == 1 and args.email and alert:
        send_alert(*alert)
    return code


if __name__ == "__main__":
    sys.exit(main())
