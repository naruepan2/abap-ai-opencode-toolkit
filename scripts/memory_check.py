#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""memory_check.py - read-only integrity check for the memory system.

The memory system only works if what is written can be read back and trusted.
This script checks that, and never writes to memory or edits a skill/agent.

Checks
  1. required memory files exist
  2. the Markdown tables parse and match their declared columns
  3. every row carries evidence (a lesson without evidence is an opinion)
  4. no credential-like strings in any memory file
  5. skill candidates marked draft/testing/active have a real skill folder
  6. project cards are reachable from INDEX.md (the navigation model)

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

REPO = Path(__file__).resolve().parent.parent
MEM = REPO / "memory"
INDEX = REPO.parent.parent / "INDEX.md"
SKILL_ROOTS = [
    Path.home() / ".config" / "opencode" / "skills",
    Path.home() / ".agents" / "skills",
    Path.home() / ".copilot" / "skills",
    Path.home() / ".claude" / "skills",
]

REQUIRED_FILES = [
    "README.md",
    "user-profile.md",
    "lessons.md",
    "corrections.md",
    "skill-candidates.md",
    "agent-registry.md",
    "tool-map.md",
]

# file -> (declared column, required columns)
TABLES = {
    "corrections.md": {
        "required": ["date", "ai_did", "correct_behavior", "root_cause",
                     "fix_level", "evidence", "status"],
        "evidence_col": "evidence",
        "status_col": "status",
        "status_allowed": {"open", "closed", "wontfix"},
    },
    "lessons.md": {
        "required": ["date", "what_happened", "evidence", "generalizable", "target"],
        "evidence_col": "evidence",
        "status_col": None,
        "status_allowed": set(),
    },
    "skill-candidates.md": {
        "required": ["candidate", "trigger", "evidence", "target_level", "status"],
        "evidence_col": "evidence",
        "status_col": "status",
        "status_allowed": set(),
    },
}

PROMOTED_STATUS = ("draft", "testing", "active")

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


def check_index(warnings):
    cards = sorted((MEM / "projects").glob("*/*.md"))
    if not cards:
        return
    if not INDEX.is_file():
        warnings.append((WARN, "INDEX.md",
                         f"not found at {INDEX}; cannot verify project cards"))
        return
    text = INDEX.read_text(encoding="utf-8", errors="replace").lower()
    for card in cards:
        if card.stem.lower() not in text:
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
