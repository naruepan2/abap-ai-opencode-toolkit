#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registry_check.py - read-only registry scanner for the OpenCode workspace.

Scans installed skills, agents, and MCP server configuration, compares them with
the committed registries, and writes a Markdown report.

Commands
  --init      create/overwrite the baseline registries from the current machine
  --check     compare the current machine with the registries (default)
  --refresh   like --init but preserve existing status/owner/last_validated
  --brief     print a short summary instead of the full report

The scanner never enables an MCP server, promotes a skill, or edits an agent.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

HOME = Path.home()
REPO = Path(__file__).resolve().parent.parent
REG = REPO / "registries"
REPORTS = REPO / "memory" / "reports"
TODAY = date.today()

# Descriptions are always loaded into the agent's context. Vendor skills cannot
# be edited, so only flag the worst offenders; personal skills get a tighter budget.
VENDOR_DESC_BUDGET = 1000
PERSONAL_DESC_BUDGET = 500

SKILL_ROOTS = [
    ("opencode", HOME / ".config" / "opencode" / "skills"),
    ("agents", HOME / ".agents" / "skills"),
    ("copilot", HOME / ".copilot" / "skills"),
    ("claude", HOME / ".claude" / "skills"),
]
AGENT_ROOTS = [
    ("opencode", HOME / ".config" / "opencode" / "agents", "*.md"),
    ("copilot", HOME / ".copilot" / "agents", "*.agent.md"),
]
OPENCODE_CONFIG = HOME / ".config" / "opencode" / "opencode.json"
COPILOT_MCP = HOME / ".copilot" / "mcp-config.json"


def disp(path: Path) -> str:
    """Portable display path (~ instead of the home directory)."""
    try:
        return str(path).replace(str(HOME), "~")
    except Exception:
        return str(path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_frontmatter(text: str) -> dict:
    """Small YAML frontmatter reader for name/description/skills.

    Handles quoted strings, folded blocks (> | >- |-), and simple block lists.
    It deliberately ignores nested metadata.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}

    data = {}
    i = 1
    while i < end:
        raw = lines[i]
        if not raw.strip() or raw.startswith((" ", "\t")):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()

        if key == "skills" and val == "":
            block = []
            i += 1
            while i < end and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                s = lines[i].strip()
                if s.startswith("- "):
                    block.append(s[2:].strip().strip("\"'"))
                i += 1
            data[key] = block
            continue

        if val in (">", "|", ">-", "|-", ">+", "|+"):
            block = []
            i += 1
            while i < end and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            data[key] = " ".join(x for x in block if x)
            continue

        if val.startswith("[") and val.endswith("]"):
            data[key] = [x.strip().strip("\"'") for x in val[1:-1].split(",") if x.strip()]
        else:
            data[key] = val.strip("\"'")
        i += 1
    return data


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"WARN: cannot read {path}: {exc}", file=sys.stderr)
        return default


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def scan_skills():
    found = []
    for harness, root in SKILL_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("SKILL.md")):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            fm = parse_frontmatter(text)
            sid = (fm.get("name") or path.parent.name).strip()
            desc = fm.get("description", "")
            if isinstance(desc, list):
                desc = " ".join(desc)
            found.append(
                {
                    "id": sid,
                    "harness": harness,
                    "path": disp(path),
                    "owner": "Pongg" if "by-pongg" in sid.lower() or "by-pongg" in str(path).lower() else "vendor",
                    "hash": sha256_file(path),
                    "desc_chars": len(desc),
                    "description": desc[:300],
                }
            )
    return found


def scan_agents():
    found = []
    for harness, root, pattern in AGENT_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.glob(pattern)):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            fm = parse_frontmatter(text)
            if harness == "copilot":
                aid = path.name.replace(".agent.md", "")
            else:
                aid = path.stem
            display = str(fm.get("name") or aid).strip().strip('"')
            owner = "Pongg" if ("by-pongg" in path.name.lower() or "by pongg" in display.lower()) else "vendor"
            skills = fm.get("skills", [])
            if isinstance(skills, str):
                skills = [s.strip().strip("\"'") for s in skills.split(",") if s.strip()]
            desc = fm.get("description", "")
            if isinstance(desc, list):
                desc = " ".join(desc)
            found.append(
                {
                    "id": aid,
                    "name": display,
                    "harness": harness,
                    "path": disp(path),
                    "owner": owner,
                    "editable": owner == "Pongg",
                    "mode": fm.get("mode", ""),
                    "skills": skills,
                    "description": desc[:300],
                    "hash": sha256_file(path),
                }
            )
    return found


def scan_mcp():
    found = []
    cfg = load_json(OPENCODE_CONFIG, {})
    for server, val in (cfg.get("mcp") or {}).items():
        if not isinstance(val, dict):
            continue
        cmd = val.get("command")
        if isinstance(cmd, list) and cmd:
            cmd = cmd[0]
        cmd_kind = Path(str(cmd)).name if cmd else ""
        url = val.get("url") or ""
        found.append(
            {
                "server": server,
                "harness": "opencode",
                "source": "opencode.json",
                "type": val.get("type", ""),
                "enabled": bool(val.get("enabled", True)),
                "command_kind": cmd_kind,
                "url_host": urlparse(url).hostname if url else "",
            }
        )

    cop = load_json(COPILOT_MCP, {})
    for server, val in (cop.get("mcpServers") or {}).items():
        found.append(
            {
                "server": server,
                "harness": "copilot",
                "source": "mcp-config.json",
                "type": "unknown",
                "enabled": True,
                "command_kind": "",
                "url_host": "",
            }
        )
    return found


def scan_tools_snapshot():
    path = REG / "tools-snapshot.json"
    data = load_json(path, None)
    if not data:
        return None
    return {
        "total": int(data.get("total", 0)),
        "namespaces": data.get("namespaces", {}),
        "generated_at": data.get("generated_at", ""),
    }


def merge_baseline(items, key_fields, old_items, status_default="active"):
    old = {tuple(str(x.get(k, "")) for k in key_fields): x for x in old_items}
    out = []
    for item in items:
        key = tuple(str(item.get(k, "")) for k in key_fields)
        prev = old.get(key, {})
        row = dict(item)
        row["status"] = prev.get("status", status_default)
        row["last_validated"] = prev.get("last_validated", TODAY.isoformat() if status_default == "active" else None)
        out.append(row)
    return out


def cmd_init(refresh=False):
    skills_old = load_json(REG / "skills.json", {}).get("skills", []) if refresh else []
    agents_old = load_json(REG / "agents.json", {}).get("agents", []) if refresh else []

    skills = scan_skills()
    agents = scan_agents()
    mcp = scan_mcp()

    skills = merge_baseline(skills, ("harness", "id", "path"), skills_old, "active")
    agents = merge_baseline(agents, ("harness", "id", "path"), agents_old, "active")

    snap = scan_tools_snapshot()
    tools = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "live tools.search snapshot",
        "total": snap["total"] if snap else 0,
        "namespaces": snap["namespaces"] if snap else {},
    }

    write_json(REG / "skills.json", {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "skills": skills,
    })
    write_json(REG / "agents.json", {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agents": agents,
    })
    write_json(REG / "mcp-servers.json", {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "servers": mcp,
    })
    write_json(REG / "tools.json", tools)

    print(f"init: skills={len(skills)} agents={len(agents)} mcp={len(mcp)} tools={tools['total']}")


def cmd_check(brief=False):
    skills = scan_skills()
    agents = scan_agents()
    mcp = scan_mcp()
    snap = scan_tools_snapshot()

    reg_skills = load_json(REG / "skills.json", {}).get("skills", [])
    reg_agents = load_json(REG / "agents.json", {}).get("agents", [])
    reg_mcp = load_json(REG / "mcp-servers.json", {}).get("servers", [])
    reg_tools = load_json(REG / "tools.json", {})

    reg_skill_keys = {(x.get("harness"), x.get("id"), x.get("path")) for x in reg_skills}
    new_skills = [s for s in skills if (s["harness"], s["id"], s["path"]) not in reg_skill_keys]
    current_paths = {s["path"] for s in skills}
    missing_skills = [s for s in reg_skills if s.get("path") not in current_paths]

    dup = {}
    for s in skills:
        dup.setdefault((s["harness"], s["id"]), []).append(s["path"])
    dup = {k: v for k, v in dup.items() if len(v) > 1}

    long_desc = [
        s for s in skills
        if (s["owner"] == "vendor" and s["desc_chars"] > VENDOR_DESC_BUDGET)
        or (s["owner"] != "vendor" and s["desc_chars"] > PERSONAL_DESC_BUDGET)
    ]
    stale = []
    for s in reg_skills:
        lv = s.get("last_validated")
        if not lv:
            stale.append(s)
        else:
            try:
                if date.fromisoformat(lv) < TODAY - timedelta(days=90):
                    stale.append(s)
            except ValueError:
                stale.append(s)

    skill_ids = {s["id"] for s in skills}
    agent_missing = []
    for a in agents:
        for ref in a.get("skills", []):
            if ref not in skill_ids:
                agent_missing.append({"agent": a["id"], "harness": a["harness"], "skill": ref})
    reg_agent_keys = {(x.get("harness"), x.get("id"), x.get("path")) for x in reg_agents}
    new_agents = [a for a in agents if (a["harness"], a["id"], a["path"]) not in reg_agent_keys]

    reg_mcp_keys = {(x.get("harness"), x.get("server")) for x in reg_mcp}
    current_mcp_keys = {(x.get("harness"), x.get("server")) for x in mcp}
    new_mcp = [x for x in mcp if (x["harness"], x["server"]) not in reg_mcp_keys]
    missing_mcp = [x for x in reg_mcp if (x["harness"], x["server"]) not in current_mcp_keys]

    ns = (snap or {}).get("namespaces", {})
    mcp_zero = []
    for s in mcp:
        if s["harness"] != "opencode" or not s.get("enabled"):
            continue
        count = ns.get(s["server"], 0)
        if snap is not None and count == 0:
            mcp_zero.append(s["server"])

    tool_changes = []
    if snap is None:
        tool_changes.append("tool snapshot not available")
    else:
        base_ns = reg_tools.get("namespaces", {}) if isinstance(reg_tools, dict) else {}
        if base_ns:
            for name in sorted(set(base_ns) | set(ns)):
                if base_ns.get(name) != ns.get(name):
                    tool_changes.append(f"{name}: {base_ns.get(name, 0)} -> {ns.get(name, 0)}")
        if reg_tools.get("total") and reg_tools.get("total") != snap["total"]:
            tool_changes.append(f"total: {reg_tools.get('total')} -> {snap['total']}")

    skill_issues = len(new_skills) + len(missing_skills) + len(dup) + len(stale)
    agent_issues = len(new_agents) + len(agent_missing)
    mcp_issues = len(new_mcp) + len(missing_mcp) + len(mcp_zero)
    tool_issues = len(tool_changes)
    issues = skill_issues + agent_issues + mcp_issues + tool_issues
    warnings = len(long_desc)

    by_harness = {}
    for s in skills:
        by_harness[s["harness"]] = by_harness.get(s["harness"], 0) + 1
    editable = [a for a in agents if a.get("editable")]

    if brief:
        print(f"Registry brief {TODAY.isoformat()}")
        print(f"skills: {len(skills)} ({', '.join(f'{k}={v}' for k, v in sorted(by_harness.items()))})")
        print(f"  new={len(new_skills)} missing={len(missing_skills)} dup={len(dup)} long_desc={len(long_desc)} stale={len(stale)}")
        print(f"agents: {len(agents)} (editable={len(editable)}, vendor={len(agents)-len(editable)}, new={len(new_agents)}, missing_skills={len(agent_missing)})")
        print(f"mcp: {len(mcp)} (enabled={sum(1 for x in mcp if x.get('enabled'))}, disabled={sum(1 for x in mcp if not x.get('enabled'))}, zero_tools={len(mcp_zero)})")
        print(f"tools: {(snap or {}).get('total', 0)} namespaces={len(ns)} changes={len(tool_changes)}")
        print(f"issues: {issues} warnings: {warnings}")
        if mcp_zero:
            print("  zero tools: " + ", ".join(mcp_zero))
        return 0 if issues == 0 else 1

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = REPORTS / "registry-report.md"
    lines = []
    lines.append("# Registry report")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Area | Count | Issues | Warnings |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Skills | {len(skills)} | {skill_issues} | {warnings} |")
    lines.append(f"| Agents | {len(agents)} | {agent_issues} | 0 |")
    lines.append(f"| MCP servers | {len(mcp)} | {mcp_issues} | 0 |")
    lines.append(f"| Tools | {(snap or {}).get('total', 0)} | {tool_issues} | 0 |")
    lines.append("")
    lines.append("## Skills by harness")
    lines.append("")
    for k, v in sorted(by_harness.items()):
        lines.append(f"- {k}: {v}")
    lines.append("")

    def section(title, items, fmt):
        lines.append(f"## {title}")
        lines.append("")
        if not items:
            lines.append("_None._")
        else:
            for item in items:
                lines.append(f"- {fmt(item)}")
        lines.append("")

    section("New skills", new_skills, lambda x: f"`{x['id']}` ({x['harness']}) — {x['path']}")
    section("Missing skill paths", missing_skills, lambda x: f"`{x.get('id')}` ({x.get('harness')}) — {x.get('path')}")
    section("Duplicate skill names within a harness", [{"k": k, "v": v} for k, v in dup.items()],
            lambda x: f"{x['k'][0]}/{x['k'][1]}: " + ", ".join(x["v"]))
    section("Skill descriptions over budget (vendor >1000, personal >500)", long_desc,
            lambda x: f"`{x['id']}` ({x['harness']}, {x['owner']}) — {x['desc_chars']} chars")
    section("Stale or unvalidated skills (>90 days)", stale, lambda x: f"`{x.get('id')}` ({x.get('harness')}) — last_validated={x.get('last_validated')}")
    section("Agents referencing missing skills", agent_missing, lambda x: f"`{x['agent']}` ({x['harness']}) -> `{x['skill']}`")
    section("New agents", new_agents, lambda x: f"`{x['id']}` ({x['harness']}) — {x['path']}")
    lines.append("## MCP servers")
    lines.append("")
    lines.append("| Server | Harness | Enabled | Tools | Note |")
    lines.append("|---|---|---|---|---|")
    for s in mcp:
        count = ns.get(s["server"], None) if s["harness"] == "opencode" else None
        note = ""
        if s["harness"] == "opencode" and s.get("enabled") and snap is not None and count == 0:
            note = "zero tools - check config/credentials/session"
        lines.append(f"| `{s['server']}` | {s['harness']} | {'yes' if s.get('enabled') else 'no'} | {count if count is not None else 'n/a'} | {note} |")
    lines.append("")

    section("New MCP servers", new_mcp, lambda x: f"`{x['server']}` ({x['harness']})")
    section("Missing MCP servers", missing_mcp, lambda x: f"`{x['server']}` ({x['harness']})")
    section("Enabled MCP servers with zero tools", mcp_zero, lambda x: f"`{x}` — check config/credentials/session")
    section("Tool snapshot changes", tool_changes, lambda x: x)

    lines.append("## Notes")
    lines.append("")
    lines.append("- This report is read-only; it changes nothing.")
    lines.append("- `status` and `last_validated` are owned by the registry, not by the scanner.")
    lines.append("- Zero tools can mean the server is disabled, failed to load, or needs a session restart.")
    lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"report: {disp(report)} (issues={issues})")
    return 0 if issues == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="Read-only registry scanner")
    ap.add_argument("--init", action="store_true", help="create/overwrite baseline registries")
    ap.add_argument("--refresh", action="store_true", help="merge new items into existing registries")
    ap.add_argument("--check", action="store_true", help="compare and write the report (default)")
    ap.add_argument("--brief", action="store_true", help="print a short summary")
    args = ap.parse_args()

    if args.init or args.refresh:
        cmd_init(refresh=args.refresh)
    return cmd_check(brief=args.brief)


if __name__ == "__main__":
    sys.exit(main())
