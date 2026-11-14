#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""session_context.py - one-call session digest (tiered context loader).

The memory system is only worth its cost if reading it is cheap. Reading eight
files one by one costs most of a session's context budget before any work starts.
This script prints the part that must be known *before* choosing a tier:

  - the active project's resume card (status / next step / do-not)
  - memory and registry health, in one line each
  - the open corrections (the ledger is read on purpose - do not skip it)
  - the curated tool rules that are easy to get wrong
  - the size and row count of every file that can be opened on demand

Tiers (see AGENTS.md):
  light  this digest only                    - a question, an analysis, a review
  task   digest + the active project card     - any code, file, or SAP work
  deep   digest + every memory file           - new project, incident, design

Usage
  python scripts/session_context.py                 # brief digest
  python scripts/session_context.py --full          # digest + file map + raw checks
  python scripts/session_context.py --project DEMO/ZDEMO01
  python scripts/session_context.py --no-checks     # skip the two scanners (~0.6s)

Exit codes
  0  digest printed (the digest is information, not a gate)
  1  a required memory file is missing
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MEM = REPO / "memory"
TOOL_MAP = MEM / "tool-map.md"
USER_PROFILE = MEM / "user-profile.md"
CORRECTIONS = MEM / "corrections.md"
CARD_DIR = MEM / "projects"

FIELD_CUT = 240
CORRECTION_CUT = 130
MAX_OPEN = 3

DIGEST_START = "<!-- digest:start -->"
DIGEST_END = "<!-- digest:end -->"

FILES_ON_DEMAND = [
    ("user-profile.md", "how Pongg communicates and decides"),
    ("corrections.md", "inbox: incidents not yet consolidated"),
    ("expertise.md", "the end state, the probes, the scorecard"),
    ("tool-map.md", "authoritative tool per task"),
    ("team-roster.md", "who to delegate to, and when not to"),
    ("skill-candidates.md", "repeated patterns not yet a skill"),
    ("agent-registry.md", "which agent/skill is editable"),
]

KNOWLEDGE_DIR = MEM / "knowledge"


def out(text=""):
    print(text)


def flat(text, cut):
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= cut:
        return text
    window = text[:cut]
    stop = max(window.rfind(". "), window.rfind("; "))
    if stop >= cut * 0.55:
        return window[: stop + 1].rstrip()
    return window[: cut - 1].rstrip() + "\u2026"


def title(text):
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return match.group(1).strip() if match else ""


def rel(path):
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        return path.as_posix()


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def rows_in(text):
    """Count dated data rows in a Markdown table."""
    return len(re.findall(r"^\|\s*\d{4}-\d{2}-\d{2}", text, re.M))


def split_row(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def table_rows(path):
    """Return (headers, rows) of the first Markdown table in the file."""
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


# --------------------------------------------------------------------------- card


def norm(value):
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def all_cards():
    return [p for p in sorted(CARD_DIR.glob("*/*.md")) if p.is_file()]


def pick_card(spec):
    cards = all_cards()
    if not cards:
        return None
    if not spec:
        return max(cards, key=lambda p: p.stat().st_mtime)
    want = norm(spec)
    for card in cards:
        keys = {norm(card.stem), norm(card.parent.name), norm(card.parent.name + card.stem)}
        if want in keys:
            return card
    for card in cards:
        if want in norm(card.parent.name + card.stem):
            return card
    return None


def grab_field(lines, label):
    """Read '- **Label:** value' plus its wrapped continuation lines."""
    pattern = re.compile(r"^\s*-\s*\*\*" + re.escape(label) + r":\*\*\s*(.*)$", re.I)
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        parts = [match.group(1).strip()]
        for nxt in lines[i + 1:]:
            if not nxt.strip():
                break
            # A wrapped value may start with bold text; only a new bullet or a
            # heading ends the field.
            if re.match(r"^\s*(?:[-*]\s|#)", nxt):
                break
            parts.append(nxt.strip())
        return " ".join(p for p in parts if p).strip()
    return ""


def spec_line(card):
    """One line for the program spec next to the card, or '' when there is none."""
    text = read(card)
    base = None
    match = re.search(r"Working directory:\s*`([^`]+)`", text)
    if match:
        base = Path(match.group(1))
    else:
        base = REPO.parent / "Projects" / card.parent.name / card.stem.upper()
    path = base / "spec.md"
    if not path.is_file():
        return ""
    body = read(path)
    meta = {}
    if body.startswith("---"):
        end = body.find("\n---", 3)
        for line in body[3:end].splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip().lower()] = value.strip().strip('"')
    reqs = pending = acs = open_q = 0
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if re.match(r"^REQ-\d+$", cells[0], re.I):
            reqs += 1
            if len(cells) >= 2 and cells[-2].lower() in {"pending", "pending-test"}:
                pending += 1
        elif re.match(r"^AC-\d+$", cells[0], re.I):
            acs += 1
        elif re.match(r"^Q-\d+$", cells[0], re.I) and cells[-1].lower() == "open":
            open_q += 1
    return (f"v{meta.get('spec_version', '?')} \u00b7 {reqs} req "
            f"({pending} pending-test) \u00b7 {acs} ac \u00b7 {open_q} open q "
            f"\u00b7 read spec.md before a change")


def card_block(card, compact=False, pinned=True):
    text = read(card)
    lines = text.splitlines()
    project = card.parent.name
    name = title(text) or card.stem.upper()
    heading = f"{project} / {name}" if norm(project) != norm(name) else name
    status = grab_field(lines, "Status")
    next_step = grab_field(lines, "Next step")
    if compact:
        out(f"{heading} \u00b7 {flat(status, 150) or 'no status'}")
        if next_step:
            out(f"  next: {flat(next_step, 150)}")
        return text
    out(f"PROJECT  {heading}")
    out(f"  card   {rel(card)}" + ("" if pinned else "  (newest; pass --project to pin)"))
    for label, value in (("status", status), ("next", next_step),
                         ("do not", grab_field(lines, "Do not")),
                         ("plan", grab_field(lines, "Plan")),
                         ("approved", grab_field(lines, "Approved scope")),
                         ("stop", grab_field(lines, "Stop condition"))):
        if value and norm(value) not in {"none", "na", "tbd"}:
            out(f"  {label:8} {flat(value, FIELD_CUT)}")
    env = re.search(r"Working directory:\s*`([^`]+)`", text)
    if env:
        out(f"  dir    {env.group(1)}")
    return text


# ------------------------------------------------------------------------ health


def run(script, args, timeout=25):
    try:
        proc = subprocess.run(
            [sys.executable, str(REPO / "scripts" / script)] + args,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout,
        )
        return proc.stdout or ""
    except (OSError, subprocess.SubprocessError):
        return ""


def checks():
    """Return (line, registry_details, memory_details) for the health line."""
    reg = run("registry_check.py", ["--check", "--brief"])
    mem = run("memory_check.py", ["--brief"])
    parts, detail = [], []
    if not reg:
        parts.append("registry n/a")
    else:
        match = re.search(r"^issues:\s*(\d+)\s+warnings:\s*(\d+)", reg, re.M)
        if match:
            parts.append(f"registry {match.group(1)} issues / {match.group(2)} warnings")
            for line in reg.splitlines():
                if line.strip().startswith("!"):
                    detail.append(("registry", line.strip().lstrip("! ").strip()))
    if not mem:
        parts.append("memory n/a")
    else:
        match = re.search(r"issues\s+(\d+),\s+warnings\s+(\d+)", mem)
        if match:
            parts.append(f"memory {match.group(1)} issues / {match.group(2)} warnings")
    return " \u00b7 ".join(parts) or "checks skipped", detail, (reg, mem)


# -------------------------------------------------------------------- corrections


def open_corrections(limit):
    headers, rows = table_rows(CORRECTIONS)
    if not headers:
        return []
    items = []
    for row in rows:
        if len(row) != len(headers):
            continue
        data = dict(zip(headers, row))
        if data.get("status", "").strip().lower() != "open":
            continue
        items.append((data.get("correct_behavior", ""), data.get("fix_level", "")))
    return items[:limit] if limit else items


def knowledge_files():
    if not KNOWLEDGE_DIR.is_dir():
        return []
    return [p for p in sorted(KNOWLEDGE_DIR.glob("*.md")) if p.name != "README.md"]


def card_domains(text):
    """Read 'domains: [a, b]' from a project card (declared competence scope)."""
    match = re.search(r"^domains:\s*\[([^\]]*)\]", text, re.M | re.I)
    if not match:
        return []
    return [d.strip().lower() for d in match.group(1).split(",") if d.strip()]


def entries_in(path):
    return len(re.findall(r"^## ", read(path), re.M))


def knowledge_line(selected=None):
    found = knowledge_files()
    if not found:
        return ""
    everything = sum(entries_in(p) for p in found)
    wanted = {norm(s) for s in (selected or [])}
    picked = [p for p in found if norm(p.stem) in wanted] if wanted else found
    if not picked:
        picked = found
    parts = [f"{p.stem} {entries_in(p)}" for p in picked]
    shown = sum(entries_in(p) for p in picked)
    tail = (f" ({shown} of {everything} entries \u2014 this project's domains)"
            if len(picked) < len(found) else f" ({shown} entries)")
    return f"{' \u00b7 '.join(parts)}{tail}"


def digest_block(path):
    """Read a curated bullet list between the digest markers."""
    text = read(path)
    if DIGEST_START not in text or DIGEST_END not in text:
        return []
    body = text.split(DIGEST_START, 1)[1].split(DIGEST_END, 1)[0]
    return [line.strip()[2:].strip() for line in body.splitlines()
            if line.strip().startswith("- ")]


# -------------------------------------------------------------------------- git


def git_state():
    try:
        branch = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--abbrev-ref", "HEAD"],
                                capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=10)
        status = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain"],
                                capture_output=True, text=True, encoding="utf-8",
                                errors="replace", timeout=10)
        if branch.returncode != 0:
            return ""
        dirty = len([l for l in (status.stdout or "").splitlines() if l.strip()])
        name = (branch.stdout or "").strip() or "?"
        return f"{name} ({dirty} uncommitted)" if dirty else f"{name} (clean)"
    except (OSError, subprocess.SubprocessError):
        return ""


# ------------------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brief", action="store_true", help="digest only (default)")
    ap.add_argument("--tiny", action="store_true",
                    help="light tier: project + status + next + open-correction count")
    ap.add_argument("--full", action="store_true", help="digest + file map + raw checks")
    ap.add_argument("--project", default="", help="project or program, e.g. DEMO/ZDEMO01")
    ap.add_argument("--no-checks", action="store_true", help="skip both scanners")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    from datetime import date
    header = [f"CONTEXT  {date.today().isoformat()}", "opencode", git_state()]
    out(" \u00b7 ".join(h for h in header if h))
    out()

    card = pick_card(args.project)
    if card is None:
        out(f"PROJECT  no card found in {rel(CARD_DIR)}" if CARD_DIR.is_dir()
            else f"PROJECT  memory/projects is missing")
        out()

    if card is not None:
        text = card_block(card, compact=args.tiny, pinned=bool(args.project))
        domains = card_domains(text)
        line = spec_line(card)
        if line:
            out(f"SPEC     {line}")
        out()

    if args.tiny:
        total_open = len(open_corrections(0))
        style = digest_block(USER_PROFILE)
        if style:
            for rule in style[:1]:
                out(f"STYLE    {flat(rule, FIELD_CUT)}")
        health, detail, _ = ("", [], ("", ""))
        if not args.no_checks:
            health, detail, _ = checks()
        issues = re.search(r"(\d+) issues", health)
        if issues and int(issues.group(1)) > 0:
            out(f"HEALTH   {health}")
            for scope, line in detail[:2]:
                out(f"  ! {scope}: {line}")
        if total_open:
            out(f"INBOX    {total_open} open row(s) in {rel(CORRECTIONS)}")
        line = knowledge_line(domains if card is not None else None)
        if line:
            out(f"KNOW     {line}")
        out("FULL     python scripts/session_context.py   (task tier)")
        return 0

    health, detail, raw = ("checks skipped", [], ("", ""))
    if not args.no_checks:
        health, detail, raw = checks()
    out(f"HEALTH   {health}")
    for scope, line in detail[:3]:
        out(f"  ! {scope}: {line}")
    out()

    style = digest_block(USER_PROFILE)
    if style:
        out("STYLE")
        for rule in style:
            out(f"  - {flat(rule, FIELD_CUT)}")
        out()

    items = open_corrections(None if args.full else MAX_OPEN)
    total_open = len(open_corrections(0))
    if total_open:
        shown = len(items)
        extra = total_open - shown
        out(f"INBOX {total_open} open" + (f" (showing {shown})" if extra > 0 else ""))
        for behavior, level in items:
            tag = f"[{level}] " if level else ""
            out(f"  - {tag}{flat(behavior, CORRECTION_CUT)}")
        if extra > 0:
            out(f"  ... {extra} more in {rel(CORRECTIONS)}")
        out()

    line = knowledge_line(domains if card is not None else None)
    if line:
        out(f"KNOWLEDGE  {line}")
        out()

    rules = digest_block(TOOL_MAP)
    if rules:
        out("TOOL RULES")
        for rule in rules:
            out(f"  - {flat(rule, FIELD_CUT)}")
        out()

    if args.full:
        out("FILES (open on demand)")
        for name, why in FILES_ON_DEMAND:
            path = MEM / name
            if not path.is_file():
                out(f"  {name:24} missing")
                continue
            text = read(path)
            out(f"  {rel(path):34} {len(text) / 1000:5.1f}k  {rows_in(text):3d} rows  {why}")
        for path in knowledge_files():
            text = read(path)
            mark = "domain" if not domains or norm(path.stem) in {
                norm(d) for d in domains} else "not loaded"
            out(f"  {rel(path):40} {len(text) / 1000:5.1f}k  "
                f"{len(re.findall(r'^## ', text, re.M)):2d} entries  {mark}")
        for extra_card in all_cards():
            text = read(extra_card)
            out(f"  {rel(extra_card):40} {len(text) / 1000:5.1f}k  card")
        out()

        reg_raw, mem_raw = raw
        if reg_raw:
            out("REGISTRY CHECK (raw)")
            for line in reg_raw.strip().splitlines():
                out(f"  {line}")
            out()
        if mem_raw:
            out("MEMORY CHECK (raw)")
            for line in mem_raw.strip().splitlines():
                out(f"  {line}")
            out()
    else:
        sizes = []
        for name, _ in FILES_ON_DEMAND:
            path = MEM / name
            if path.is_file():
                text = read(path)
                rows = rows_in(text)
                sizes.append(f"{name.replace('.md', '')} {len(text) / 1000:.1f}k"
                             + (f"({rows})" if rows else ""))
        out("ON DEMAND  " + " \u00b7 ".join(sizes))

    missing = [name for name, _ in FILES_ON_DEMAND if not (MEM / name).is_file()]
    if not (MEM / "README.md").is_file():
        missing.append("README.md")
    if missing:
        out()
        out("MISSING  " + ", ".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
