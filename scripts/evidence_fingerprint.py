#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stable content fingerprint for a run evidence set.

Hashes file bytes, never mtime or clock. Paths are stored relative to --root so a
manifest survives a machine change. The hash carries its engine and locator beside it:
never compare a digest produced by a different engine.

Usage
  python scripts/evidence_fingerprint.py --root <dir> --files a.md,b.json \
      --engine local-sha256 --locator RUN-001
  python scripts/evidence_fingerprint.py --root <dir> --files a.md,b.json \
      --engine local-sha256 --locator RUN-001 --check <manifest.json>
  python scripts/evidence_fingerprint.py --self-test
"""
import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

VERSION = 1


def build(root, files, engine, locator):
    root = Path(root).resolve()
    records = []
    for raw in files:
        p = (root / raw).resolve()
        if root not in p.parents and p != root:
            raise ValueError(f"path escapes root: {raw}")
        if not p.is_file():
            raise FileNotFoundError(f"missing evidence file: {raw}")
        data = p.read_bytes()
        records.append({
            "path": p.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        })
    records.sort(key=lambda r: r["path"])
    payload = {
        "version": VERSION,
        "engine": engine,
        "locator": locator,
        "files": records,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False).encode("utf-8")
    payload["digest"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--files", default="")
    ap.add_argument("--engine", default="local-sha256")
    ap.add_argument("--locator", default="")
    ap.add_argument("--check")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.txt").write_text("alpha", encoding="utf-8")
            (root / "b.txt").write_text("beta", encoding="utf-8")
            base = build(root, ["b.txt", "a.txt"], "test", "RUN-1")
            assert base == build(root, ["a.txt", "b.txt"], "test", "RUN-1"), "order changed digest"
            (root / "a.txt").write_text("alpha!", encoding="utf-8")
            changed = build(root, ["a.txt", "b.txt"], "test", "RUN-1")
            assert changed["digest"] != base["digest"], "byte change not detected"
            try:
                build(root, ["../escape.txt"], "test", "RUN-1")
            except ValueError:
                pass
            else:
                raise AssertionError("path escape not refused")
        print("evidence-fingerprint: self-test OK")
        return 0

    files = [x for x in a.files.split(",") if x]
    if not files:
        ap.error("--files is required unless --self-test")
    current = build(a.root, files, a.engine, a.locator)
    if a.check:
        expected = json.loads(Path(a.check).read_text(encoding="utf-8"))
        if expected.get("digest") != current["digest"]:
            print(json.dumps({"ok": False, "reason": "evidence_stale",
                              "expected": expected.get("digest"),
                              "actual": current["digest"]}, indent=2))
            return 1
        print(json.dumps({"ok": True, "digest": current["digest"]}, indent=2))
        return 0
    print(json.dumps(current, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError, OSError) as exc:
        print(json.dumps({"ok": False, "reason": "unreadable",
                          "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
