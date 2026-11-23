#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Boundary and known-bad tests for the evidence fingerprint helper.

Run with: python -m unittest discover -s tests -p 'test_*.py'
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "evidence_fingerprint.py"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


class FingerprintTest(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)
        (self.root / "a.txt").write_text("alpha", encoding="utf-8")
        (self.root / "b.txt").write_text("beta", encoding="utf-8")
        self.base = ["--root", str(self.root), "--engine", "test", "--locator", "RUN-1"]

    def tearDown(self):
        self.td.cleanup()

    def fingerprint(self, files):
        r = run(*self.base, "--files", ",".join(files))
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def test_order_independent_and_bytes_recorded(self):
        one = self.fingerprint(["a.txt", "b.txt"])
        two = self.fingerprint(["b.txt", "a.txt"])
        self.assertEqual(one["digest"], two["digest"])
        self.assertEqual([f["path"] for f in one["files"]], ["a.txt", "b.txt"])
        self.assertEqual(one["files"][0]["bytes"], 5)

    def test_known_bad_byte_change_is_detected(self):
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps(self.fingerprint(["a.txt", "b.txt"])),
                            encoding="utf-8")
        (self.root / "a.txt").write_text("alpha!", encoding="utf-8")
        r = run(*self.base, "--files", "a.txt,b.txt", "--check", str(manifest))
        self.assertEqual(r.returncode, 1)
        self.assertEqual(json.loads(r.stdout)["reason"], "evidence_stale")

    def test_path_escape_fails_closed(self):
        r = run(*self.base, "--files", "../escape.txt")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(json.loads(r.stderr)["reason"], "unreadable")

    def test_self_test(self):
        r = run("--self-test")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("self-test OK", r.stdout)


if __name__ == "__main__":
    unittest.main()
