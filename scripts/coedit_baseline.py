#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coedit_baseline.py - local content-addressed pre-image store for co-edit writes.

SAP still owns the exact diff. This store only holds the pre-image of an object we
are about to change, so undo can be a write-forward under CAS instead of a blind
restore. Store is local and must stay out of git: it can contain customer source.

Usage
  python scripts/coedit_baseline.py save --root <project> --object KEY \
      --engine ai-dev --intent CHG-001 --tr DEVK900123 \
      --source-file pre.abap [--pre-hash sha256:...] [--post-hash sha256:...]
  python scripts/coedit_baseline.py attach --root <project> --object KEY \
      --intent CHG-001 --post-hash sha256:...
  python scripts/coedit_baseline.py get --root <project> --hash <sha256>
  python scripts/coedit_baseline.py list --root <project> [--object KEY]

Exit codes: 0 ok, 1 bad input / hash mismatch / missing blob.
"""

import argparse
import gzip
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_VERSION = 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def clean_hash(value):
    return value.strip().lower().removeprefix("sha256:") if value else None


def store_paths(root):
    base = root / ".baseline"
    return base / "blobs" / "sha256", base / "manifest.json"


def read_manifest(path):
    if not path.exists():
        return {"version": MANIFEST_VERSION, "objects": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != MANIFEST_VERSION:
        raise SystemExit(f"unsupported manifest version: {data.get('version')}")
    return data


def write_manifest(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def save(args):
    source = sys.stdin.buffer.read() if args.source_file == "-" else Path(args.source_file).read_bytes()
    sha = digest(source)
    expected = clean_hash(args.pre_hash)
    if expected and expected != sha:
        raise SystemExit(f"pre-hash mismatch: expected {expected}, got {sha}; nothing stored")

    blob_dir, manifest_path = store_paths(args.root)
    blob_dir.mkdir(parents=True, exist_ok=True)
    blob = blob_dir / f"{sha}.gz"
    if not blob.exists():
        blob.write_bytes(gzip.compress(source, mtime=0))

    manifest = read_manifest(manifest_path)
    entry = {
        "id": args.intent or datetime.now(timezone.utc).strftime("auto-%Y%m%dT%H%M%SZ"),
        "object": args.object,
        "locator": args.locator or "main",
        "engine": args.engine,
        "sha256": sha,
        "source_hash": args.pre_hash or None,
        "post_hash": None,
        "tr": args.tr or "$TMP",
        "checked_at": args.checked_at or datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    group = manifest["objects"].setdefault(args.object, [])
    if any(e["id"] == entry["id"] for e in group):
        raise SystemExit(f"intent already stored for {args.object}: {entry['id']}")
    group.append(entry)
    write_manifest(manifest_path, manifest)
    print(f"stored {sha} for {args.object} ({entry['locator']}, {args.engine}, {entry['tr']})")


def attach(args):
    _, manifest_path = store_paths(args.root)
    manifest = read_manifest(manifest_path)
    for entry in manifest["objects"].get(args.object, []):
        if entry["id"] == args.intent:
            entry["post_hash"] = args.post_hash
            entry["verified_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            write_manifest(manifest_path, manifest)
            print(f"attached post-hash to {args.object} / {args.intent}")
            return
    raise SystemExit(f"no entry for {args.object} / {args.intent}")


def get(args):
    _, manifest_path = store_paths(args.root)
    sha = clean_hash(args.hash)
    blob = args.root / ".baseline" / "blobs" / "sha256" / f"{sha}.gz"
    if not blob.exists():
        raise SystemExit(f"no blob for {sha} under {manifest_path.parent}")
    data = gzip.decompress(blob.read_bytes())
    if digest(data) != sha:
        raise SystemExit(f"blob content does not match its hash: {sha}")
    sys.stdout.buffer.write(data)


def list_entries(args):
    _, manifest_path = store_paths(args.root)
    manifest = read_manifest(manifest_path)
    for key, group in manifest["objects"].items():
        if args.object and key != args.object:
            continue
        for entry in group:
            print(f"{key}\t{entry['locator']}\t{entry['engine']}\t{entry['sha256'][:12]}\t{entry['tr']}\t{entry['id']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("save", help="store a pre-image and its manifest entry")
    p.add_argument("--root", type=Path, required=True, help="project/program folder holding .baseline")
    p.add_argument("--object", required=True, help="key: system/client/type/name/locator is recommended")
    p.add_argument("--locator", default="main", help="include or method inside the object")
    p.add_argument("--engine", required=True, help="tool engine that produced the hash")
    p.add_argument("--intent", help="change/intent id; one entry per intent")
    p.add_argument("--tr", help="transport the write used; never guess")
    p.add_argument("--source-file", required=True, help="pre-image file, or - for stdin")
    p.add_argument("--pre-hash", help="source_hash from the tool; verified before storing")
    p.add_argument("--checked-at", help="ISO-8601 observation time; defaults to now")
    p.set_defaults(func=save)

    p = sub.add_parser("attach", help="record the post-hash after a verified write")
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--object", required=True)
    p.add_argument("--intent", required=True)
    p.add_argument("--post-hash", required=True)
    p.set_defaults(func=attach)

    p = sub.add_parser("get", help="write a stored pre-image to stdout")
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--hash", required=True)
    p.set_defaults(func=get)

    p = sub.add_parser("list", help="list manifest entries")
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--object", help="filter by exact object key")
    p.set_defaults(func=list_entries)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
