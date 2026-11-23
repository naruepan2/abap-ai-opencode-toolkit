#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools_now.py - what can I actually call right now, and with what authority?

The OpenCode tool-snapshot plugin rewrites registries/tools-full.json whenever an
MCP server connects, disconnects, or the tool list changes (mcp.* / tool.* /
session.* events, throttled to once a minute). This script turns that snapshot into
a decision: which ADT server is live, what it can do, and which one to use.

A live tool list says nothing about permission. `SAPWrite` can be absent because the
engine cannot write or because the launcher did not pass -AllowWrites, and those are
different problems. So the script also reads the launcher command from the OpenCode
MCP config, joins it to the SAP profile, and prints the armed posture
(write / transport / data / sql / package ceiling) next to each server.

Usage
  python scripts/tools_now.py            # human summary + recommended path
  python scripts/tools_now.py --json     # machine-readable
  python scripts/tools_now.py --check    # exit 1 on a policy violation (no ADT server / two writers)
  python scripts/tools_now.py --file X   # read a fixture instead of the registry

Exit codes
  0  a usable path was found
  1  no ADT server or two writers armed on the same client

Posture is best-effort: when the config is missing or the command does not use
sap-mcp.ps1, the server is reported with posture "unknown" and the write flag falls
back to the engine guess. Never treat a guess as permission.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REG = REPO / "registries"
SNAPSHOT = REG / "tools-snapshot.json"
FULL = REG / "tools-full.json"

# Where the launcher command and the SAP profiles live. Outside the repo on purpose:
# the repo is shareable, the config carries customer hostnames and usernames.
MCP_CONFIG = Path(os.environ.get(
    "OPENCODE_MCP_CONFIG", Path.home() / ".config" / "opencode" / "opencode.json"))
SAP_PROFILES = Path(os.environ.get(
    "SAP_PROFILES", Path.home() / ".config" / "opencode" / "sap" / "profiles.json"))

# PowerShell switches sap-mcp.ps1 understands -> posture key.
LAUNCH_SWITCHES = {
    "-AllowWrites": "write",
    "-AllowTransportWrites": "transport",
    "-AllowDataPreview": "data",
    "-AllowFreeSql": "sql",
    "-AllowGitWrites": "git",
}

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
    "SAPQuery": {"data", "sql"},
    "SAPTransport": {"transport"},
    "SAPGit": {"git"},
    "SAPContext": {"deps"},
    "SAPLint": {"lint"},
    # ATC, ABAP Unit, CDS test cases, dumps and SQL traces. There is no debugger:
    # stepping lives in ai-dev (debugger_attach / debugger_step / debugger_get_variables).
    "SAPDiagnose": {"syntax", "atc", "unit", "trace"},
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


def _try_load(path):
    try:
        return load(path)
    except (OSError, ValueError):
        return {}


def _mcp_servers(config):
    """Both config shapes: V2 mcp.servers.<name>, and the older mcp.<name>."""
    mcp = config.get("mcp") or {}
    servers = dict(mcp.get("servers") or {})
    for name, entry in mcp.items():
        if name in ("servers", "timeout") or not isinstance(entry, dict):
            continue
        servers.setdefault(name, entry)
    return servers


def _enabled(entry):
    if "disabled" in entry:
        return not entry["disabled"]
    return entry.get("enabled", True)


def _command_of(entry):
    command = entry.get("command") or ""
    if isinstance(command, list):
        return " ".join(str(part) for part in command)
    return str(command)


def launch_posture():
    """namespace -> what the launcher actually armed, from config + profile.

    Returns {} when the config is absent (another machine, a fixture run). An entry
    with posture "unknown" means the config exists but this server is not a
    sap-mcp.ps1 launch, so the switches cannot be read.
    """
    config = _try_load(MCP_CONFIG)
    if not config:
        return {}
    profiles = (_try_load(SAP_PROFILES).get("profiles") or {})
    found = {}
    for name, entry in _mcp_servers(config).items():
        command = _command_of(entry)
        posture = {
            "profile": "",
            "engine": "",
            "system": "",
            "client": "",
            "packages": "",
            "write": False,
            "transport": False,
            "data": False,
            "sql": False,
            "git": False,
            "enabled": _enabled(entry),
            "known": False,
            # The -Allow* switches live in the arc-1 branch of sap-mcp.ps1; ai-dev
            # exits earlier with its full tool set, so its write power is not a switch.
            "flags_apply": False,
        }
        if "sap-mcp.ps1" in command:
            profile = re.search(r"-Profile\s+(\S+)", command)
            engine = re.search(r"-Engine\s+(\S+)", command)
            posture["profile"] = profile.group(1) if profile else ""
            posture["engine"] = engine.group(1) if engine else ""
            switches = set(re.findall(r"-[A-Za-z]+", command))
            for switch, key in LAUNCH_SWITCHES.items():
                if switch in switches:
                    posture[key] = True
            # sap-mcp.ps1 hard-codes some flags off; honour the file rather than the
            # switch list once it declares them.
            profile_entry = profiles.get(posture["profile"]) or {}
            posture["system"] = str(profile_entry.get("system_id") or "")
            posture["client"] = str(profile_entry.get("client") or "")
            posture["packages"] = str(profile_entry.get("allowed_packages") or "")
            posture["known"] = bool(posture["profile"])
            posture["flags_apply"] = posture["engine"] == "arc1"
        found[name] = posture
    return found


def collect(full, posture=None):
    posture = posture or {}
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
            "posture": None,
            # FIX: a server disabled in config can linger in the tool snapshot.
            "disabled": False,
        })
        override = OVERRIDES.get(ns, {})
        entry.update({k: v for k, v in override.items() if k in ("role", "allow_write")})
        entry["tools"] += 1
        entry["caps"] |= caps_for(engine, tool.get("name", ""), tool.get("id", ""))
    # A launcher we can read beats any guess. A launcher we cannot read leaves the
    # guess in place, but marks it so the printer can say "unknown" instead of lying.
    for ns, entry in servers.items():
        armed = posture.get(ns)
        if not armed:
            continue
        entry["posture"] = armed
        # FIX: config is authority. A disabled server is never a writer/analyser,
        # even while the stale snapshot still lists its tools.
        if armed["known"] and not armed.get("enabled", True):
            entry["disabled"] = True
            entry["allow_write"] = False
            continue
        if armed["known"] and armed.get("flags_apply"):
            entry["allow_write"] = bool(armed["write"])
    return servers


def decide(servers):
    # FIX: a disabled server is not part of the usable path.
    adt = [s for s in servers.values() if not s.get("disabled")]
    writers = [s for s in adt if s["allow_write"]]
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

    # Two live readers are free. Two write-armed servers on one system/client are not:
    # ADT serialises true concurrency with a lock (423), but a sequential
    # read-modify-write from two engines has no conflict detection and loses an update.
    conflicts = {}
    for s in writers:
        armed = s.get("posture") or {}
        key = (armed.get("system") or "", armed.get("client") or s["client"])
        if not all(key):
            continue
        conflicts.setdefault(key, []).append(s["namespace"])

    warnings = []
    for (system, client), names in sorted(conflicts.items()):
        if len(names) > 1:
            warnings.append(
                f"two write-armed servers on {system or '?'}/{client}: "
                + ", ".join(sorted(names))
                + " - write each object from one engine")
    for s in writers:
        armed = s.get("posture") or {}
        if armed.get("known") and armed.get("packages") in ("", "*"):
            warnings.append(f"{s['namespace']}: package ceiling is unrestricted")
    unknown = [s["namespace"] for s in adt
               if s.get("posture") is None or not s["posture"].get("known")]
    if unknown:
        warnings.append("posture unknown for " + ", ".join(sorted(unknown))
                        + " - do not assume read-only")
    for ns, s in servers.items():
        if s.get("disabled"):
            warnings.append(f"{ns}: disabled in config but still in tool snapshot "
                            "- restart the service or ignore the stale snapshot")
    if not adt:
        warnings.append("no ADT server live")
    return {"path": path, "writers": writers, "testers": testers,
            "readers": readers, "warnings": warnings,
            "write_conflicts": ["/".join(k) for k, v in conflicts.items() if len(v) > 1]}


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
    servers = collect(full, {} if args.file else launch_posture())
    decision = decide(servers)

    age = None
    stamp = snapshot.get("generated_at") or full.get("generated_at")
    if stamp:
        try:
            then = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            age = int((datetime.now(timezone.utc) - then).total_seconds())
        except ValueError:
            age = None

    # FIX: a disabled server is not live; do not count it as a usable server.
    live = [s for s in servers.values() if not s.get("disabled")]
    missing = [ns for ns in args.expect if ns not in {s["namespace"] for s in live}]

    result = {
        "total": full.get("total", len(full.get("tools", []))),
        "snapshot_age_s": age,
        "missing": missing,
        "servers": [
            {"namespace": s["namespace"], "engine": s["engine"], "client": s["client"],
             "role": s["role"], "allow_write": s["allow_write"],
             "tools": s["tools"], "caps": sorted(s["caps"]),
             "posture": ({"profile": s["posture"]["profile"],
                          "system": s["posture"]["system"],
                          "client": s["posture"]["client"],
                          "packages": s["posture"]["packages"],
                          "known": s["posture"]["known"],
                          "flags_apply": s["posture"].get("flags_apply", False),
                          "write": s["posture"]["write"],
                          "transport": s["posture"]["transport"],
                          "data": s["posture"]["data"],
                          "sql": s["posture"]["sql"],
                          "git": s["posture"]["git"]}
                         if s.get("posture") else None)}
            for s in sorted(live, key=lambda x: x["namespace"])
        ],
        "path": decision["path"],
        "warnings": decision["warnings"],
        "write_conflicts": decision["write_conflicts"],
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
            p = s.get("posture")
            if p and p["known"] and p.get("flags_apply"):
                flags = " ".join(
                    f"{key}={str(p[key]).lower() if isinstance(p[key], bool) else p[key]}"
                    for key in ("transport", "data", "sql", "git"))
                print(f"POST   profile {p['profile']} {p['system'] or '?'}/{p['client'] or '?'} "
                      f"pkgs {p['packages'] or '?'} {flags}")
            elif p and p["known"]:
                print(f"POST   profile {p['profile']} {p['system'] or '?'}/{p['client'] or '?'} "
                      f"writes=engine-default (no -Allow* gate, no package ceiling passed)")
            elif p is not None:
                print("POST   unknown (not a sap-mcp.ps1 launch)")
        print(f"PATH   {result['path']}")
        for warning in result["warnings"]:
            print(f"!      {warning}")
        if missing:
            print("!      expected but not live: " + ", ".join(missing))
    if args.check and (not result["servers"] or result["write_conflicts"] or missing):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
