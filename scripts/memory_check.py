#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""memory_check.py - read-only integrity check for the memory system.

The memory system only works if what is written can be read back and trusted.
This script checks that, and never writes to memory or edits a skill/agent.

Checks
  1. required memory files exist (including the knowledge base)
  2. the inbox table parses and matches its declared columns
  3. every inbox row carries evidence and a known status
  4. a row stays under its length budget (a long row is a recurring token cost)
  5. every knowledge entry has Rule / Why / Seen / Confidence / Evidence, a valid
     confidence value, and fits its domain cap
  6. no credential-like strings in any memory file
  7. skill candidates marked draft/testing/active have a real skill folder
  8. project cards are reachable from INDEX.md and stay under their size budget

Usage
  python scripts/memory_check.py            # full report
  python scripts/memory_check.py --brief    # one-line summary

Exit codes
  0  clean or warnings only
  1  at least one issue
"""

import argparse
import re
import sys
from pathlib import Path

from _paths import INDEX, MEM, REPO
SKILL_ROOTS = [
    Path.home() / ".config" / "opencode" / "skills",
    Path.home() / ".agents" / "skills",
    Path.home() / ".copilot" / "skills",
    Path.home() / ".claude" / "skills",
]

REQUIRED_FILES = [
    "README.md",
    "user-profile.md",
    "corrections.md",
    "skill-candidates.md",
    "agent-registry.md",
    "tool-map.md",
    "expertise.md",
    "knowledge/README.md",
]

# file -> (declared column, required columns)
TABLES = {
    "corrections.md": {
        "required": ["date", "ai_did", "correct_behavior", "root_cause",
                     "fix_level", "evidence", "status"],
        "evidence_col": "evidence",
        "status_col": "status",
        "status_allowed": {"open", "drained"},
    },
    "skill-candidates.md": {
        "required": ["candidate", "trigger", "evidence", "target_level", "status"],
        "evidence_col": "evidence",
        "status_col": "status",
        "status_allowed": set(),
    },
}

PROMOTED_STATUS = ("draft", "testing", "active")

# The knowledge base is the durable memory. One entry per rule, capped per domain.
KNOWLEDGE_DIR = MEM / "knowledge"
DOMAIN_CAP = 12
ENTRY_BUDGET = 1200
ENTRY_FIELDS = ("rule", "why", "seen", "confidence", "evidence")
ENTRY_OPTIONAL = ("break it, and",)
CONFIDENCE = {"low", "medium", "high"}
INBOX_CAP = 40

# A memory row is read at every session start, so a long row is a recurring cost.
# Over budget is a warning: shorten the row and move the detail to the card.
ROW_BUDGET = {
    "corrections.md": 240,
}

# A project card is read at the task tier. The budget is a growth guard, not a
# target: if it fires, move dated findings to the project's own reports/.
CARD_BUDGET = 9000

CREDENTIAL_PATTERNS = [
    re.compile(r"(?i)\bpassw(or)?d\b\s*[:=]\s*\S"),
    re.compile(r"(?i)\bapi[_-]?key\b\s*[:=]\s*\S"),
    re.compile(r"(?i)\btoken\b\s*[:=]\s*\S"),
    re.compile(r"(?i)\bsecret\b\s*[:=]\s*\S"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bSAP_PASSWORD\s*[:=]\s*\S"),
]

# A rule that forbids storing a credential legitimately mentions it.
CREDENTIAL_EXEMPT = re.compile(
    r"(?i)never|do not|don't|must not|ห้าม|ไม่เก็บ|ไม่บันทึก|ไม่เขียน|nowhere else"
)

WARN = "warning"
ISSUE = "issue"


def norm(cell: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", cell.strip().lower()).strip("_")


def split_row(line: str) -> list:
    """Split a Markdown table row, tolerating escaped pipes."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def parse_table(path: Path):
    """Return (headers, rows) for the first table in a Markdown file."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return [], []
    for i, line in enumerate(lines):
        if not line.strip().startswith("|"):
            continue
        if i + 1 >= len(lines) or not re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            continue
        headers = [norm(h) for h in split_row(line)]
        rows = []
        for row_line in lines[i + 2:]:
            if not row_line.strip().startswith("|"):
                break
            rows.append(split_row(row_line))
        return headers, rows
    return [], []


def check_files(findings):
    for name in REQUIRED_FILES:
        if not (MEM / name).is_file():
            findings.append((ISSUE, name, "required memory file is missing"))


def resolve_column(headers, name):
    """Exact header, else the first header starting with it ('Evidence (>=2)')."""
    if name in headers:
        return name
    for header in headers:
        if header.startswith(name):
            return header
    return None


def check_tables(findings, warnings):
    for name, spec in TABLES.items():
        path = MEM / name
        if not path.is_file():
            continue
        headers, rows = parse_table(path)
        if not headers:
            findings.append((ISSUE, name, "no Markdown table found"))
            continue
        missing = [c for c in spec["required"] if resolve_column(headers, c) is None]
        if missing:
            findings.append((ISSUE, name, f"missing column(s): {', '.join(missing)}"))
            continue

        width = len(headers)
        bad_width, no_evidence, bad_status = [], [], []
        for n, row in enumerate(rows, start=1):
            if len(row) != width:
                bad_width.append(n)
                continue
            data = dict(zip(headers, row))
            ev_col = resolve_column(headers, spec["evidence_col"])
            ev = data.get(ev_col, "").strip() if ev_col else ""
            if not ev or ev in {"-", "—", "n/a"}:
                no_evidence.append(n)
            col = resolve_column(headers, spec["status_col"]) if spec["status_col"] else None
            if col:
                status = data.get(col, "").strip().lower()
                if spec["status_allowed"] and status not in spec["status_allowed"]:
                    bad_status.append((n, status or "(empty)"))

        if bad_width:
            findings.append((ISSUE, name,
                             f"row(s) with wrong column count: {bad_width}"))
        if no_evidence:
            warnings.append((WARN, name,
                             f"row(s) without evidence: {no_evidence}"))
        for n, status in bad_status:
            findings.append((ISSUE, name,
                             f"row {n} has status '{status}', expected one of "
                             f"{sorted(spec['status_allowed'])}"))


def check_row_length(warnings):
    for name, budget in ROW_BUDGET.items():
        path = MEM / name
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, start=1):
            body = line.strip()
            if not re.match(r"^\|\s*\d{4}-\d{2}-\d{2}", body):
                continue
            if len(body) > budget:
                warnings.append((WARN, name,
                                 f"line {n} is {len(body)} chars (budget {budget}); "
                                 "shorten the row and move detail to the card"))


def parse_entries(path):
    """Split a knowledge file into (title, body) entries at '## ' headings."""
    entries, title, body, fence = [], None, [], False
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            if title is not None:
                entries.append((title, "\n".join(body)))
            title, body = line[3:].strip(), []
        elif title is not None:
            body.append(line)
    if title is not None:
        entries.append((title, "\n".join(body)))
    return entries


def check_knowledge(findings, warnings):
    if not KNOWLEDGE_DIR.is_dir():
        findings.append((ISSUE, "knowledge/", "the knowledge base directory is missing"))
        return
    domains = [p for p in sorted(KNOWLEDGE_DIR.glob("*.md")) if p.name != "README.md"]
    if not domains:
        findings.append((ISSUE, "knowledge/", "no domain file besides README.md"))
        return

    for path in domains:
        entries = parse_entries(path)
        if len(entries) > DOMAIN_CAP:
            warnings.append((WARN, path.name,
                             f"{len(entries)} entries (cap {DOMAIN_CAP}); merge the "
                             "lowest Seen/confidence pair into a neighbour"))
        for title, body in entries:
            low = body.lower()
            missing = [f for f in ENTRY_FIELDS if f"**{f}:**" not in low]
            if missing:
                findings.append((ISSUE, path.name,
                                 f"entry '{title[:40]}' missing {', '.join(missing)}"))
                continue
            match = re.search(r"\*\*confidence:\*\*\s*([a-z]+)", low)
            if match and match.group(1) not in CONFIDENCE:
                findings.append((ISSUE, path.name,
                                 f"entry '{title[:40]}' has confidence "
                                 f"'{match.group(1)}', expected one of "
                                 f"{sorted(CONFIDENCE)}"))
            if not any(f"**{f}:**" in low for f in ENTRY_OPTIONAL):
                warnings.append((WARN, path.name,
                                 f"entry '{title[:40]}' has no 'Break it, and' line — "
                                 "the next agent cannot recognise the symptom"))
            if len(body) > ENTRY_BUDGET:
                warnings.append((WARN, path.name,
                                 f"entry '{title[:40]}' is {len(body)} chars "
                                 f"(budget {ENTRY_BUDGET}); sharpen the rule"))


def check_inbox(warnings):
    path = MEM / "corrections.md"
    if not path.is_file():
        return
    headers, rows = parse_table(path)
    if len(rows) > INBOX_CAP:
        warnings.append((WARN, "corrections.md",
                         f"{len(rows)} rows in the inbox (cap {INBOX_CAP}); drain it "
                         "to knowledge/ and archive the rest"))


def check_cards(warnings):
    root = MEM / "projects"
    if not root.is_dir():
        return
    for card in sorted(root.glob("*/*.md")):
        try:
            size = len(card.read_text(encoding="utf-8"))
        except OSError:
            continue
        if size > CARD_BUDGET:
            warnings.append((WARN, rel_card(card),
                             f"{size} chars (budget {CARD_BUDGET}); move dated "
                             "findings to the project's reports/ and keep the card"))


def rel_card(card):
    try:
        return card.relative_to(MEM).as_posix()
    except ValueError:
        return card.name


def check_credentials(findings, warnings):
    for path in sorted(MEM.rglob("*.md")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, start=1):
            if CREDENTIAL_EXEMPT.search(line):
                continue
            for pattern in CREDENTIAL_PATTERNS:
                if pattern.search(line):
                    findings.append((ISSUE, path.name,
                                     f"line {n} looks like a stored credential"))
                    break


def skill_exists(name: str) -> bool:
    return any((root / name / "SKILL.md").is_file() for root in SKILL_ROOTS)


def check_skill_candidates(warnings):
    path = MEM / "skill-candidates.md"
    if not path.is_file():
        return
    headers, rows = parse_table(path)
    if not headers:
        return
    for row in rows:
        if len(row) != len(headers):
            continue
        data = dict(zip(headers, row))
        status = data.get("status", "").strip().lower()
        # Only an exact status counts; "draft when repeated" is still a candidate.
        if status not in PROMOTED_STATUS:
            continue
        name = data.get("candidate", "").strip().strip("`")
        if name and not skill_exists(name):
            warnings.append((WARN, "skill-candidates.md",
                             f"'{name}' is marked '{status}' but no skill folder exists"))


def norm_text(value: str) -> str:
    """Compare names loosely: 'HCL Interface QA32' == 'hcl-interface-qa32'."""
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def check_index(warnings):
    cards = sorted((MEM / "projects").glob("*/*.md"))
    if not cards:
        return
    if not INDEX.is_file():
        warnings.append((WARN, "INDEX.md",
                         f"not found at {INDEX}; cannot verify project cards"))
        return
    text = norm_text(INDEX.read_text(encoding="utf-8", errors="replace"))
    for card in cards:
        if norm_text(card.stem) not in text:
            warnings.append((WARN, "INDEX.md",
                             f"project card '{card.parent.name}/{card.stem}' "
                             "is not listed"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--brief", action="store_true", help="print a short summary")
    args = ap.parse_args()

    findings, warnings = [], []
    check_files(findings)
    check_tables(findings, warnings)
    check_row_length(warnings)
    check_knowledge(findings, warnings)
    check_inbox(warnings)
    check_cards(warnings)
    check_credentials(findings, warnings)
    check_skill_candidates(warnings)
    check_index(warnings)

    if args.brief:
        print(f"memory_check: issues {len(findings)}, warnings {len(warnings)}")
        for level, name, msg in findings + warnings:
            print(f"  [{level}] {name}: {msg}")
        return 0 if not findings else 1

    print("memory_check report")
    print(f"  root: {MEM}")
    print(f"  files: {len(list(MEM.rglob('*.md')))} markdown")
    print()
    if not findings and not warnings:
        print("  clean")
    for level, name, msg in findings:
        print(f"  [{level}] {name}: {msg}")
    for level, name, msg in warnings:
        print(f"  [{level}] {name}: {msg}")
    print()
    print(f"  issues {len(findings)}, warnings {len(warnings)}")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
