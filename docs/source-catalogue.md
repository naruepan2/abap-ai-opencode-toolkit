# Source catalogue — provenance only

> On-demand reference. `docs/memory-decisions.md` owns decisions and status; this file
> owns **where an idea came from and when it was last checked**. Never put a decision
> here, and never put a URL/licence in the decision register — cross-link by D-ID.
> New source → add the provenance row **before** any idea row. Unknown → literal
> `UNVERIFIED` plus the read-only check that would settle it; never fill a plausible
> value. Source facts are tier-3 evidence; live state comes from a `--check` run.

## Row format

| Source | URL @ ref | Version read | Read on | Licence | Evidence basis (what was read) | Ideas landed as | Checked | Pin | Delta |
|---|---|---|---|---|---|---|---|---|---|
| GSD Core | `@opengsd/gsd-core` — GitHub URL UNVERIFIED | `v1.23.0` | 2026-11-23 | MIT¹ | README, context-engineering note, ADR-22, ADR-1671, `gsd-verifier.md`, temporal-context read in full; test names as signal | D-10…D-17, D-27 | 2026-11-23 | `v1.23.0` | none |
| opencode-mem | `tickernelz/opencode-mem` — exact URL UNVERIFIED | UNVERIFIED | 2026-11-23 | MIT¹ | README read in full from GitHub; vector/embedding infrastructure deliberately excluded | D-18…D-24 (identity HYPOTHESIS) | 2026-11-23 | UNVERIFIED | none |
| OpenViking | URL UNVERIFIED | UNVERIFIED | 2026-11-23 | **AGPLv3**¹ | README + concept docs 03/07/08 read in full; implementation tree not read | D-05, D-08 — re-expressed, **no code copied** | 2026-11-23 | UNVERIFIED | none |
| abap-skills | `likweitan/abap-skills` — URL UNVERIFIED | UNVERIFIED | 2026-11-22 | MIT¹ | all text files read; 129 SVG icons + `AppList.json` treated as data | D-21…D-23, Clean Core gates | 2026-11-22 | UNVERIFIED | none |
| V9.4 embedded SQL memory | `workspace/memory/reports/v94-memory-design-20261123.md` (local) | UNVERIFIED | 2026-11-23 | local design, provenance not asserted — **not** the toolkit's MIT | 1,080-line master + 58-line addendum read in full; harness + smoke result inspected; no machinery implemented | D-29 (deferred with triggers) | 2026-11-23 | report file | none |
| Copilot improvement register | `D:\abap-copilot-kit\docs\reference\improvement-register.md` (read-only, D-30) | UNVERIFIED | 2026-11-23 | local register, provenance not asserted | full file read; evidence tiers + source rows | D-30; provenance columns re-expressed here | 2026-11-23 | file bytes | new V9.4 section since first read |
| SQLite engine | Python `sqlite3` / Node `node:sqlite` — built into installed runtimes | Python 3.15.2 / Node 26.13.1 | 2026-11-23 | runtime standard library | version probed via `--version`; no DB adopted | D-29 only | 2026-11-25 | runtime versions | none |
| GSD-style note freshness | sourced from the GSD review above | as GSD | as GSD | as GSD | `source_revision` / `reviewed_source_revision` pair via the Copilot register row above | D-05/D-08 freshness vocabulary | as GSD | as GSD | none |
| humanizer / thai-humanizer | vendor skills on the OpenCode harness; upstream URLs UNVERIFIED | UNVERIFIED | 2026-11-25 | MIT (from each SKILL.md) | frontmatter and front-matter bytes read; body 34,132 + 23,691 B not re-expressed | D-31 cited, not adopted | 2026-11-25 | installed skill versions | none |

¹ Licence values for the first five rows are **quoted from the read-only Copilot register** (`improvement-register.md:37-41`), not independently verified against each upstream repo here. Treat as `UNVERIFIED` until checked at source; the two open licence cells already say UNVERIFIED. AGPL row carries the explicit "do not copy code" consequence (`improvement-register.md:43-44`).

Placeholder for an unverifiable source (X post, scratch paper, an unnamed "second brain" repo):

```
| <name> | UNVERIFIED | UNVERIFIED | UNVERIFIED | not asserted | seen in conversation only, no file read | none until verified | UNVERIFIED | UNVERIFIED | none |
```

## Re-check workflow — no new log

1. **Trigger** — a release note/changelog entry is noticed during normal work, an inbox row names the source, or a D-29 numeric trigger fires. No watcher, cron, hook bus or auto-fetch.
2. **Bounded read** — read the changelog/diff summary only (lazy read, D-16). Compare the `Pin`; unchanged → update `Checked`, write `Delta = none`, stop.
3. **Classify** against the decision register:
   - `NO_OVERLAP` / `WORDING` → update this row only; no D-row.
   - `MECHANISM` → one `corrections.md` inbox row (≤240 chars, `open`) naming the source + section; close-out picks one outcome.
   - `CONFLICT` → update `memory-decisions.md` with a reason **before** changing the rule; never keep both behaviours alive.
   - `NEW_STORE` (DB/vectors/daemon) → D-18 and D-29 gates apply; a new release alone never reopens them.
4. **One reviewer**, read-only, with `file:line` evidence (`templates/subagent-brief.md`). Blocked → `BLOCKED: <question>` in the plan and wait; two failures → stop.
5. **Decision** — new D-row only if behaviour actually changes; otherwise just the revision stamp in this row. Rejected ideas keep the one-line reason forever; never delete.
6. **Commit** — provenance cells, status cell and commit hash in the **same** commit. Git history is the timeline; never a row per check.
7. **Revisit** — only on the triggers in step 1. Staleness is a warning, not a broken install.

## Rules

- This file never authorises a write, an install, an MCP toggle or a SAP action.
- Do not copy code or substantial text from an AGPL source; re-express and cite. MIT: re-express and cite; if code is copied, carry the notice.
- Do not mark a Copilot-side row `APPLIED` from this side; harnesses stay separate (D-25/D-30).
- Do not create a second provenance file or a second decision log. One row per source, edited in place.
- No new always-loaded bytes: this file is read on demand only (tier `deep` or new-idea arrival); never add its rules to `AGENTS.md`, `profile.md` or a skill description.
