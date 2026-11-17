#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""specs_sync.py - mirror every program spec into the instance.

The contract is edited next to the program
(`Projects/<PROJECT>/<PROGRAM>/spec.md`) because that is where the work happens.
The toolkit repository does not carry customer data, so the specs are mirrored into
the git-ignored instance (`workspace/specs/`) with a sha256 manifest. The mirror is
generated: never edit it by hand, and read the program copy during work.

Usage
  python scripts/specs_sync.py            # check (default), exit 1 on drift
  python scripts/specs_sync.py --write    # rebuild workspace/specs from Projects/
  python scripts/specs_sync.py --list     # one line per mirrored program

Exit codes
  0  the mirror matches the program specs
  1  drift, a missing file, or Projects/ not found
"""

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

from _paths import PROJECTS, REPO, SPECS

MIRROR = SPECS
MANIFEST = MIRROR / "manifest.json"
STATIC = {"README.md"}

# Refuse to mirror a credential-shaped value: a private mirror is one visibility
# change away from public and git history cannot be taken back. The assignment form
# needs a real value, so prose like "never store SAP_PASSWORD in config" is safe.
CREDENTIAL_SHAPE = re.compile(
    r"(?im)^\s*(?:SAP_PASSWORD|PASSWORD|PASSWD|PWD|TOKEN|API[_-]?KEY|SECRET|CLIENT_SECRET)"
    r"\s*[:=]\s*(?!\s*(?:<|\"\"|''|\?|none|na|tbd|\$\{|@secret\b))\S{4,}"
    r"|(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,})"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|Bearer\s+[A-Za-z0-9._-]{20,}"
)


def credential_in(path):
    """True when a file carries a credential-shaped assignment or token."""
    try:
        return bool(CREDENTIAL_SHAPE.search(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeError):
        return False


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def front_matter(path):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    data = {}
    for line in text[3:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip().lower()] = value.strip().strip('"')
    return data


def collect():
    """Every spec.md under Projects, with the files that belong to it."""
    found = {}
    if not PROJECTS.is_dir():
        return found
    for spec in sorted(PROJECTS.glob("*/*/spec.md")):
        program_dir = spec.parent
        key = f"{program_dir.parent.name}/{program_dir.name}"
        files = {"spec.md": spec}
        changelog = program_dir / "CHANGELOG.md"
        if changelog.is_file():
            files["CHANGELOG.md"] = changelog
        fs_index = program_dir / "spec" / "FS_INDEX.md"
        if fs_index.is_file():
            files["FS_INDEX.md"] = fs_index
        # spec/source (the customer FS) is deliberately NOT mirrored: it is the
        # customer's document and this repository must not carry customer data.
        blocked = []
        for name, path in list(files.items()):
            if credential_in(path):
                print(f"specs mirror: refusing {key}/{name} (credential-shaped value)",
                      file=sys.stderr)
                blocked.append(name)
                del files[name]
        meta = front_matter(spec)
        found[key] = {
            "spec_version": meta.get("spec_version", "?"),
            "status": meta.get("status", "?"),
            "files": files,
            "blocked": blocked,
        }
    return found


def manifest_of(found):
    data = {"generated_by": "scripts/specs_sync.py", "programs": {}}
    for key in sorted(found):
        entry = found[key]
        data["programs"][key] = {
            "spec_version": entry["spec_version"],
            "status": entry["status"],
            "files": {
                name: {"sha256": sha256(path), "bytes": path.stat().st_size}
                for name, path in sorted(entry["files"].items())
            },
        }
    return data


def check():
    """Compare the mirror with Projects. Returns a result dict, never prints."""
    found = collect()
    if not PROJECTS.is_dir():
        return {"programs": 0, "files": 0, "drift": [("-", "Projects/", "missing")],
                "found": {}, "manifest": None}
    wanted = manifest_of(found)
    try:
        current = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        current = None

    drift = []
    if current is None:
        drift.append(("-", "manifest.json", "missing"))
    else:
        have_programs = current.get("programs", {})
        for key, entry in wanted["programs"].items():
            if key not in have_programs:
                drift.append((key, "-", "not mirrored"))
                continue
            have_files = have_programs[key].get("files", {})
            for name, meta in entry["files"].items():
                path = MIRROR / key / name
                if name not in have_files:
                    drift.append((key, name, "not in manifest"))
                elif not path.is_file():
                    drift.append((key, name, "missing"))
                elif sha256(path) != meta["sha256"]:
                    drift.append((key, name, "differs"))
            for name in have_files:
                if name not in entry["files"]:
                    drift.append((key, name, "stale"))
        for key in have_programs:
            if key not in wanted["programs"]:
                drift.append((key, "-", "stale program"))

    for key, entry in found.items():
        for name in entry.get("blocked", []):
            drift.append((key, name, "credential-shaped value; not mirrored"))

    return {"programs": len(found), "files": sum(len(v["files"]) for v in found.values()),
            "drift": drift, "found": found, "manifest": wanted}


def write():
    """Rebuild specs/ from Projects. Static files (README.md) are kept."""
    result = check()
    found = result["found"]
    if MIRROR.exists():
        for child in MIRROR.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            elif child.name not in STATIC and child.name != "manifest.json":
                child.unlink()
    MIRROR.mkdir(parents=True, exist_ok=True)
    for key, entry in sorted(found.items()):
        for name, path in sorted(entry["files"].items()):
            target = MIRROR / key / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    MANIFEST.write_text(json.dumps(result["manifest"], indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8", newline="\n")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="rebuild the mirror")
    ap.add_argument("--check", action="store_true", help="check only (default)")
    ap.add_argument("--list", action="store_true", help="one line per program")
    args = ap.parse_args()

    # FIX: never delete a good mirror when the source tree is missing.
    if args.write and not PROJECTS.is_dir():
        print(f"specs mirror not written: {PROJECTS} is missing; existing mirror kept",
              file=sys.stderr)
        return 1

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    result = write() if args.write else check()
    if args.write:
        print(f"specs mirror written: {result['programs']} programs, "
              f"{result['files']} files -> {MIRROR}")
        return 0

    if args.list:
        for key in sorted(result["found"]):
            entry = result["found"][key]
            print(f"  {key:32} spec {entry['spec_version']:5} {entry['status']:8} "
                  f"{len(entry['files'])} file(s)")
        return 0

    print(f"specs mirror: {result['programs']} programs, {result['files']} files")
    if not result["drift"]:
        print("  in sync")
        return 0
    for key, name, reason in result["drift"][:12]:
        print(f"  ! {key:32} {name:28} {reason}")
    if len(result["drift"]) > 12:
        print(f"  ... and {len(result['drift']) - 12} more")
    print("  run: python scripts/specs_sync.py --write")
    return 1


if __name__ == "__main__":
    sys.exit(main())
