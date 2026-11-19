# Plan: co-edit Tier 3–5 + version close

Approved 2026-11-19. This is a toolkit-doc/script change; there is no customer
program, no FS, no SAP write, and no transport in scope.

**Goal:** finish the gap-closure plan — per-write baseline with safe undo, RAP
sentinel/dirty-frontier navigation, and explicit attribution/preemption — then
cut version v0.8.0.

**Acceptance test (stop condition):** `closeout.py` clean, `registry_check.py
--check` with 0 issues, baseline script round-trip and hash-mismatch test pass,
tag `v0.8.0` pushed, main pushed. GitHub Release stays blocked only by the
credential method, reported — not retried blindly.

**Contract answers:** FS = none (toolkit change); change type = feature
extension; production = not applicable (docs/scripts only); target = this git
repository, no SAP system/client.

## Todos

1. Write `scripts/coedit_baseline.py` (content-addressed pre-image store).
2. Add `.baseline/` to `.gitignore`; document the script in `scripts/README.md`.
3. Test save → get → list and a pre-hash mismatch locally.
4. Add "Baseline and undo" to the co-edit contract: write-triggered pre-image,
   three-way reconcile, forward write under CAS.
5. Add sentinel + dirty frontier to `templates/RAP_INDEX.md` and the contract's
   heavy path (`impact` alone is partial).
6. Add attribution evidence card and safe-point preemption to the contract.
7. Update `docs/coedit-gap-register.md` statuses for Tier 3–5.
8. Update `templates/AGENTS.md` and top `AGENTS.md` pointers.
9. Fold `CHANGELOG.md` Unreleased into `v0.8.0`; update README current release.
10. Run closeout + registry check + git status.
11. Commit, tag `v0.8.0`, push main and tag.
12. Report Release credential blocker and wait for an approved method.
