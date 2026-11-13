#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""closeout.py - read-only close-out check for one task.

The session-start digest covers the start. This covers the end: the four things that
rot between sessions if nobody looks.

  1. the inbox was drained        (open rows, their age, the row cap)
  2. the project card is current  (the four change-contract answers, last update)
  3. the plan file is real        (exists, and no todo left blocked or open by mistake)
  4. knowledge is still confirmed (no entry older than 180 days)

Usage
  python scripts/closeout.py                          # newest card
  python scripts/closeout.py --project DEMO/ZDEMO01

Exit codes
  0  nothing broken (warnings are human decisions)
  1  an issue: a referenced plan is missing, or a table does not parse
"""

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MEM = REPO / "memory"
CARD_DIR = MEM / "projects"
INBOX = MEM / "corrections.md"
KNOWLEDGE = MEM / "knowledge"

INBOX_AGE_DAYS = 7
INBOX_CAP = 40
CARD_AGE_DAYS = 14
ENTRY_STALE_DAYS = 180
CONTRACT = ("FS", "Change type", "Production", "Target")

WARN, ISSUE = "warning", "issue"


def out(text=""):
    print(text)


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def norm(value):
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def split_row(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def table_rows(path):
    lines = read(path).splitlines()
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        if i + 1 >= len(lines) or not re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            continue
        headers = [re.sub(r"[^a-z0-9]+", "_", h.strip().lower()).strip("_")
                   for h in split_row(line)]
        rows = []
        for row_line in lines[i + 2:]:
            if not row_line.strip().startswith("|"):
                break
            rows.append(split_row(row_line))
        return headers, rows
    return [], []


def pick_card(spec):
    cards = [p for p in sorted(CARD_DIR.glob("*/*.md")) if p.is_file()]
    if not cards:
        return None
    if not spec:
        return max(cards, key=lambda p: p.stat().st_mtime)
    want = norm(spec)
    for card in cards:
        keys = {norm(card.stem), norm(card.parent.name),
                norm(card.parent.name + card.stem)}
        if want in keys:
            return card
    for card in cards:
        if want in norm(card.parent.name + card.stem):
            return card
    return None


def grab_field(lines, label):
    pattern = re.compile(r"^\s*-\s*\*\*" + re.escape(label) + r":\*\*\s*(.*)$", re.I)
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        parts = [match.group(1).strip()]
        for nxt in lines[i + 1:]:
            if not nxt.strip() or re.match(r"^\s*(?:[-*]\s|#)", nxt):
                break
            parts.append(nxt.strip())
        return " ".join(p for p in parts if p).strip()
    return ""


def days_since(moment):
    return max(0, (datetime.now() - moment).days)


# ---------------------------------------------------------------------- checks


def check_inbox(findings, warnings):
    if not INBOX.is_file():
        findings.append((ISSUE, "inbox", "memory/corrections.md is missing"))
        return None
    headers, rows = table_rows(INBOX)
    if not headers:
        findings.append((ISSUE, "inbox", "the inbox table does not parse"))
        return None
    if len(rows) > INBOX_CAP:
        warnings.append((WARN, "inbox",
                         f"{len(rows)} rows (cap {INBOX_CAP}); drain and archive"))
    open_rows, oldest = [], 0
    for row in rows:
        if len(row) != len(headers):
            continue
        data = dict(zip(headers, row))
        if data.get("status", "").strip().lower() != "open":
            continue
        open_rows.append(data)
        try:
            age = (date.today() - date.fromisoformat(data["date"].strip())).days
        except (ValueError, KeyError):
            continue
        oldest = max(oldest, age)
    if oldest > INBOX_AGE_DAYS:
        warnings.append((WARN, "inbox",
                         f"oldest open row is {oldest} days old (drain at "
                         f"{INBOX_AGE_DAYS}); consolidate or drop it"))
    return {"rows": len(rows), "open": len(open_rows), "oldest": oldest}


def check_card(findings, warnings, card):
    if card is None:
        findings.append((ISSUE, "card", f"no project card under {CARD_DIR}"))
        return None
    text = read(card)
    lines = text.splitlines()
    age = days_since(datetime.fromtimestamp(card.stat().st_mtime))
    if age > CARD_AGE_DAYS:
        warnings.append((WARN, "card",
                         f"{card.parent.name}/{card.stem} was updated {age} days ago; "
                         "re-verify the status before trusting it"))
    missing = [label for label in CONTRACT
               if not grab_field(lines, label)]
    if missing:
        warnings.append((WARN, "card",
                         "missing change-contract answer(s): " + ", ".join(missing)
                         + " — ask before the next change"))
    return {"path": card, "text": text, "lines": lines, "age": age}


def check_plan(findings, warnings, card):
    if card is None:
        return None
    plan_ref = grab_field(card["lines"], "Plan")
    if not plan_ref or norm(plan_ref) in {"none", "na", "tbd"}:
        return None
    base = ""
    match = re.search(r"Working directory:\s*`([^`]+)`", card["text"])
    if match:
        base = match.group(1)
    path = Path(plan_ref)
    if not path.is_absolute() and base:
        path = Path(base) / plan_ref
    if not path.is_file():
        findings.append((ISSUE, "plan", f"card points at '{plan_ref}' but it does not exist"))
        return None
    text = read(path)
    open_todo = len(re.findall(r"^\s*-\s*\[ \]", text, re.M))
    blocked = len(re.findall(r"^\s*-\s*\[~\]", text, re.M))
    done = len(re.findall(r"^\s*-\s*\[x\]", text, re.M))
    if blocked:
        warnings.append((WARN, "plan",
                         f"{blocked} todo blocked: a human answer is needed before the "
                         "task can continue"))
    return {"path": path, "open": open_todo, "blocked": blocked, "done": done}


def check_knowledge(warnings):
    if not KNOWLEDGE.is_dir():
        return None
    domains = [p for p in sorted(KNOWLEDGE.glob("*.md")) if p.name != "README.md"]
    entries = 0
    stale = []
    for path in domains:
        text = read(path)
        for block in re.split(r"^## ", text, flags=re.M)[1:]:
            entries += 1
            match = re.search(r"\*\*last confirmed:\*\*\s*(\d{4}-\d{2}-\d{2})",
                              block, re.I)
            if not match:
                continue
            try:
                age = (date.today() - date.fromisoformat(match.group(1))).days
            except ValueError:
                continue
            if age > ENTRY_STALE_DAYS:
                stale.append(block.splitlines()[0].strip()[:40])
    if stale:
        warnings.append((WARN, "knowledge",
                         f"{len(stale)} entr(y/ies) not confirmed in "
                         f"{ENTRY_STALE_DAYS} days; re-verify or archive: "
                         + "; ".join(stale[:3])))
    return {"domains": len(domains), "entries": entries, "stale": len(stale)}


# ------------------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default="", help="project or program, e.g. DEMO/ZDEMO01")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    findings, warnings = [], []
    inbox = check_inbox(findings, warnings)
    card = check_card(findings, warnings, pick_card(args.project))
    plan = check_plan(findings, warnings, card)
    knowledge = check_knowledge(warnings)

    name = "no card"
    if card:
        title = re.search(r"^#\s+(.+)$", card["text"], re.M)
        label = title.group(1).strip() if title else card["path"].stem.upper()
        project = card["path"].parent.name
        name = label if norm(project) == norm(label) else f"{project} / {label}"
    out(f"closeout {date.today().isoformat()} \u00b7 {name}")
    out()

    if inbox:
        out(f"  inbox      {inbox['open']} open, oldest {inbox['oldest']}d, "
            f"{inbox['rows']}/{INBOX_CAP} rows")
    if card:
        out(f"  card       updated {card['age']}d ago")
    if plan:
        out(f"  plan       {plan['path'].name}: {plan['done']} done, "
            f"{plan['open']} open, {plan['blocked']} blocked")
    else:
        out("  plan       none referenced (fine for a short task)")
    if knowledge:
        out(f"  knowledge  {knowledge['entries']} entries in "
            f"{knowledge['domains']} domains, {knowledge['stale']} stale")
    out()

    if not findings and not warnings:
        out("  clean \u2014 commit the close-out and stop")
        return 0

    for level, scope, message in findings + warnings:
        mark = "!" if level == ISSUE else "~"
        out(f"  {mark} {scope}: {message}")
    out()
    out(f"  issues {len(findings)}, warnings {len(warnings)}")
    if not findings:
        out("  warnings are a human decision; they do not block the close-out")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
