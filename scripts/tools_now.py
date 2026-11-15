#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools_now.py - what can I actually call right now?

The OpenCode tool-snapshot plugin rewrites registries/tools-full.json whenever an
MCP server connects, disconnects, or the tool list changes (mcp.* / tool.* /
session.* events, throttled to once a minute). This script turns that snapshot into
a decision: which ADT server is live, what it can do, and which one to use.

Usage
  python scripts/tools_now.py            # human summary + recommended path
  python scripts/tools_now.py --json     # machine-readable
  python scripts/tools_now.py --check    # exit 1 on a policy violation / stale data
  python scripts/tools_now.py --file X   # read a fixture instead of the registry

Exit codes
  0  a usable path was found
  1  no ADT server, a stale snapshot, or two writers for the same client
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REG = REPO / "registries"
SNAPSHOT = REG / "tools-snapshot.json"
FULL = REG / "tools-full.json"

# Namespace -> engine. Keep working through the ai-dev rename.
ENGINES = (
    ("arc1", ("arc1-",)),
    ("ai-dev", ("ai-dev-", "ds4-", "gsd-")),
)

# Client -> role. 100/110/120 are development clients; 900 is the test client.
ROLES = {"100": "code", "110": "code", "120": "code", "900": "test"}

# A namespace can override the defaults here (role, allow_write).
OVERRIDES = {}

ARC1_CAPS = {
    "SAPRead": {"read"},
    "SAPSearch": {"search"},
    "SAPWrite": {"write"},
    "SAPActivate": {"activate"},
    "SAPNavigate": {"deps"},
    "SAPQuery": {"data"},
    "SAPTransport": {"transport"},
    "SAPGit": {"git"},
    "SAPContext": {"deps"},
    "SAPLint": {"lint"},
    "SAPDiagnose": {"syntax", "atc", "unit", "debug"},
    "SAPManage": {"manage"},
}

AI_DEV_RULES = (
    ("read", ("get_source", "get_program", "get_class", "get_include", "get_table",
              "get_structure", "get_cds", "get_object")),
    ("search", ("search", "grep")),
    ("write", ("write", "edit", "update", "create", "delete")),
    ("activate", ("activate",)),
    ("transport", ("transport",)),
    ("atc", ("atc",)),
    ("unit", ("unit",)),
    ("syntax", ("syntax",)),
    ("lint", ("lint",)),
    ("deps", ("context", "reference", "dependenc", "where")),
    ("data", ("table_contents", "run_query", "query", "sql")),
    ("git", ("git",)),
    ("debug", ("debug", "dump", "trace", "profil")),
)


def engine_of(namespace):
    for engine, prefixes in ENGINES:
        if namespace.startswith(prefixes):
            return engine
    return None


def client_of(namespace):
    match = re.search(r"-(\d{3})$", namespace)
    return match.group(1) if match else ""


def caps_for(engine, name, tool_id):
    hay = f"{name} {tool_id}".lower()
    if engine == "arc1":
        return set(ARC1_CAPS.get(name, ()))
    found = set()
    for cap, needles in AI_DEV_RULES:
        if any(needle in hay for needle in needles):
            found.add(cap)
    return found


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def collect(full):
    servers = {}
    for tool in full.get("tools", []):
        ns = tool.get("namespace") or "opencode"
        engine = engine_of(ns)
        if not engine:
            continue
        entry = servers.setdefault(ns, {
            "namespace": ns,
            "engine": engine,
            "client": client_of(ns),
            "role": ROLES.get(client_of(ns), "unknown"),
            "allow_write": engine == "ai-dev" and ROLES.get(client_of(ns), "unknown") == "code",
            "tools": 0,
            "caps": set(),
        })
        override = OVERRIDES.get(ns, {})
        entry.update({k: v for k, v in override.items() if k in ("role", "allow_write")})
        entry["tools"] += 1
        entry["caps"] |= caps_for(engine, tool.get("name", ""), tool.get("id", ""))
    return servers


def decide(servers):
    adt = list(servers.values())
    writers = [s for s in adt if s["allow_write"] and s["role"] == "code"]
    testers = [s for s in adt if s["role"] == "test"]
    readers = [s for s in adt if not s["allow_write"]]
    analysers = [s for s in readers if s["engine"] == "arc1"] or readers
    if not adt:
        path = "none - enable an ADT MCP (ai-dev or arc1) before any SAP call"
    elif not writers and not testers:
        path = "read-only - analyse with " + ", ".join(s["namespace"] for s in readers)
    else:
        parts = []
        if writers:
            parts.append("write=" + writers[0]["namespace"])
        if testers:
            parts.append("verify=" + testers[0]["namespace"])
        if analysers:
            parts.append("analyse=" + analysers[0]["namespace"])
        path = " · ".join(parts)
    warnings = []
    if len(writers) > 1:
        warnings.append("more than one code writer is live; pick one per task")
    if any(s["engine"] == "arc1" and s["allow_write"] for s in adt):
        warnings.append("arc1 has allow_write=true; keep it read-only unless a skill needs it")
    if not adt:
        warnings.append("no ADT server live")
    return {"path": path, "writers": writers, "testers": testers,
            "readers": readers, "warnings": warnings}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default="", help="tools-full.json fixture")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--expect", action="append", default=[],
                    help="namespace that must be live (repeatable); --check fails if missing")
    args = ap.parse_args()

    full_path = Path(args.file) if args.file else FULL
    if not full_path.is_file():
        print(f"no tool snapshot at {full_path}; start a session first", file=sys.stderr)
        return 1
    full = load(full_path)
    snapshot = load(SNAPSHOT) if SNAPSHOT.is_file() and not args.file else {}
    servers = collect(full)
    decision = decide(servers)

    age = None
    stamp = snapshot.get("generated_at") or full.get("generated_at")
    if stamp:
        try:
            then = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            age = int((datetime.now(timezone.utc) - then).total_seconds())
        except ValueError:
            age = None

    missing = [ns for ns in args.expect if ns not in servers]

    result = {
        "total": full.get("total", len(full.get("tools", []))),
        "snapshot_age_s": age,
        "missing": missing,
        "servers": [
            {"namespace": s["namespace"], "engine": s["engine"], "client": s["client"],
             "role": s["role"], "allow_write": s["allow_write"],
             "tools": s["tools"], "caps": sorted(s["caps"])}
            for s in sorted(servers.values(), key=lambda x: x["namespace"])
        ],
        "path": decision["path"],
        "warnings": decision["warnings"],
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        age_text = (f"{age}s ago" if age is not None and age < 120
                else (f"{age // 60}m ago" if age is not None else "unknown"))
        print(f"TOOLS  {result['total']} total · snapshot {age_text}")
        if not result["servers"]:
            print("ADT    none")
        for s in result["servers"]:
            write = "write" if s["allow_write"] else "read-only"
            print(f"ADT    {s['namespace']:<22} {s['engine']:<6} client {s['client'] or '?':<3} "
                  f"{s['role']:<7} {write:<9} {s['tools']:>3} tools")
            print(f"CAPS   {' '.join(s['caps'])}")
        print(f"PATH   {result['path']}")
        for warning in result["warnings"]:
            print(f"!      {warning}")
        if missing:
            print("!      expected but not live: " + ", ".join(missing))
    if args.check and (not result["servers"] or len(decision["writers"]) > 1 or missing):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
