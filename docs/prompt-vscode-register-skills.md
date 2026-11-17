# Prompt: create the two registration skills on VS Code

Use this prompt verbatim in a VS Code agent session. It creates/updates two general
skills; it does **not** register a project, connect to SAP, or read credentials.

Read the current OpenCode versions first if the files are reachable, so the VS Code
copies stay byte-identical in behaviour:

- `<repo>\config\opencode-skills\sap-project-register\SKILL.md`
- `<repo>\config\opencode-skills\sap-program-register\SKILL.md`
- shared contract: `<repo>\docs\catalog.md` §"Registration contract"

(`<repo>` = the toolkit repository root, e.g. the folder containing `install.ps1`.)

VS Code MCP config is at `%APPDATA%\Code\User\mcp.json` —
**read-only, and only for the shape of an `mcp.json` server entry**. Never echo,
copy, resolve, or ask for `${input:...}` values, `SAP_PASSWORD`, user names or
client numbers from it. If a value is needed, ask the user in chat instead.

---

## PROMPT (copy from here)

You are creating two **general** skills for VS Code: `sap-project-register` and
`sap-program-register`. They scaffold folders and manifests for SAP work. They do
not deploy ABAP, do not connect to SAP, do not enable MCP servers, and do not read
or store credentials.

### Step 0 — Read before writing

1. `%APPDATA%\Code\User\mcp.json` — read-only. Use it **only**
   to learn the VS Code MCP entry shape: `servers.<name>` with `type` (`stdio` or
   `http`), `command`/`args` or `url`, `cwd`, and an `env` block. **Never** print,
   copy, resolve or ask the user to paste any `password: true` input,
   `${input:...}` value, SAP user, or client from this file. If any such value is
   needed for a profile, ask the user to type it in chat.
2. The two OpenCode `SKILL.md` files and the shared contract listed above, if they
   exist. Port their rules; do not invent a new design. If a file is missing, stop
   and say which one, rather than guessing the rule.

### Step 1 — Where to write

VS Code loads personal skills from `~\.agents\skills\<name>\SKILL.md`. Create or
overwrite exactly these two files:

- `~\.agents\skills\sap-project-register\SKILL.md`
- `~\.agents\skills\sap-program-register\SKILL.md`

Each file starts with YAML front matter: `name` (exact skill name) and a short
`description` with triggers ("register new project", "new program folder", ...).
Keep the description under 600 characters. Capabilities in one line: scaffold
only; asks for every unknown; never deploys or connects to SAP.

### Step 2 — Shared rules (put in BOTH files, no separate contract file)

- **Question mode:** ask one question at a time with the platform's question UI
  (if available), otherwise as a short single question. Restate values already
  known and ask only what is missing. Validate each answer before the next
  question. Post a multi-field form only if the user explicitly asks to answer all
  at once. Match the user's language. Stop on a blocker; never loop a gate.
- **Never guess** a SID, URL, destination, client, package, transport, program
  name, purpose, FS, or knowledge-domain set. A blank is a blocker, not a default.
- **Never ask for a password** in chat. The user stores it himself via the OS
  keychain / the VS Code `input` prompt defined in `mcp.json`.
- **One artifact per call.** `sap-project-register` creates only the project;
  `sap-program-register` creates only one program and requires the project to
  exist. Stop if the folder already exists.
- **Resolve the target project before any program work.** A program belongs to a
  project; never assume which one. `sap-program-register` must confirm the target
  project with the user (see Step 4) before asking any other input or calling SAP.
- **Normalise codes; do not trust the user's casing.** The user may type `luf` or
  `LuF` when the project is `LUF`. Treat codes as case-insensitive when matching
  and resolve them to the canonical casing from `INDEX.md` / the folder on disk.
  Write the canonical form — see Step 3 and Step 4. Never create a second folder
  just because the casing differed (`LUF` vs `LuF`).

### Step 3 — `sap-project-register` behaviour

Ask at invocation (skip anything already known): project code, SID/description,
ADT URL, SAP Logon destination, SAP user, language, TLS CA path, allowed packages,
test client, and explicit permission to write outside the current project. **Do
not ask for a transport and do not ask for an owner** — no program or SAP object
exists yet.

**Canonical casing:** if the user typed `luf` / `LuF` and a matching project
already exists, use its on-disk casing (`LUF`) — do not create a duplicate. For a
new project, uppercase the code (`LUF`) before writing folder, `INDEX.md`, and
`project.yaml`. The memory card is the one exception: its file name is lowercase
(`luf.md`) because `closeout.py` uppercases the card stem to find the program
folder, while the checks compare codes case-insensitively. If the user's code is
ambiguous after normalising (two folders differ only by case), stop and ask.

Create `Projects/<PROJECT>/` only if absent:

- `README.md` — System / Code client / Test client / Transport (`none`) + empty
  Programs list.
- `AGENTS.md` — scope, System table, empty Programs section, §Conventions with
  "add with date and decision; ask, do not infer", §Deploy "not yet approved",
  §Session start.
- `project.yaml` — `project`, `system`, `code_client`, `test_client`,
  `allowed_packages`, `transport: none`, `archive: _archive`, `sandbox: _sandbox`,
  `scope: project`.
- `_archive/README.md`, `_sandbox/README.md` — one line each. No shared
  archive/sandbox under `Projects`.

INDEX and optional MCP entry (only with user's explicit permission):

- Add the **project row** to the portfolio `INDEX.md`.
- For a new system only: add `<project>-<client>` to
  `~\.config\opencode\sap\profiles.json` using `profiles.example.json` — fields
  `url`, `client`, `user`, `system_id`, `destination`, `language`, `tls_ca`,
  `allowed_packages`; **no password field**.
- In `mcp.json`, follow the observed VS Code shape to add one **disabled** entry
  per chosen engine (`ai-dev`, `arc1`): `type: "stdio"`, `command`/`args` calling
  the existing launcher, and an `env` block. Do not enable during registration.
  If the harness cannot safely write `mcp.json`, print a snippet for the user to
  paste and stop — never force it.
- Tell the user: to use the profile later, set the entry to enabled in `mcp.json`,
  store the secret via the VS Code `input` prompt / OS keychain, then restart the
  MCP host. In VS Code the toggle/config is host-specific — verify the actual
  file, do not assume the OpenCode `enabled:true` rule applies.

Verify: list exact files written; no SAP object was touched.

### Step 4 — `sap-program-register` behaviour

**Resolve the target project FIRST — before any other question or SAP call.**
This skill can be invoked on its own; a program cannot exist without a project,
and guessing one would write the scaffold into the wrong place.

- If the project code is already known from this session or the user's request,
  normalise it against the project list (case-insensitive) and restate the
  **canonical** form for the user to confirm. `luf` / `LuF` must resolve to `LUF`.
- If it is **not known**, ask the user: "จะ register program นี้ภายใต้ project ไหนครับ?"
  Do not infer it from the object name, a recent conversation, or a folder listing.
- If more than one project exists, list the project codes found under `Projects/`
  (read the portfolio `INDEX.md`, do not scan recursively) and let the user pick.
- If the chosen project folder does **not** exist, stop and tell the user to run
  `sap-project-register` first. Do not create the project from this skill.
- Once confirmed, use the on-disk casing of the project folder (never the raw text
  the user typed). Read that project's `project.yaml` for `system`, `code_client`,
  `allowed_packages` and `transport`; use these as the source of truth. Create
  folders and write `INDEX.md` / manifests with the canonical uppercase code; the
  memory card file stays lowercase.

Then ask (skip known values): program name (SAP object name), one-line purpose,
FS path or explicit "none", and explicit permission to write outside the current
program.

**Object lookup (read-only).** After the name is known, use the project's live
`arc1-*` MCP (never hardcode an engine name — confirm system/client first):
`SAPSearch(searchType="tadir_lookup", names=[<name>], objectTypes=[<types>])` for
existence/package, then `SAPTransport(action="list"/"get")` for the TR. Found →
reuse package/TR; not found → new; lookup failed/unclear/no logon → stop and ask,
never claim "does not exist". No SAP writes.

**Transport (optional).** Read `allowed_packages` from `project.yaml`. If it is
missing/empty (older scaffold), ask the user once and record the answer in
`reports/DECISIONS.md` with source — do not edit `project.yaml`. If `$TMP` only,
do not ask for a TR and set `transport: none`. Otherwise offer "has TR / not yet /
use $TMP"; never invent a number.

Create `Projects/<PROJECT>/<PROGRAM>/` only if absent:

- `README.md` — purpose, Status, Pointers, Test focus.
- `AGENTS.md` — scope, System (with transport or "$TMP — no transport"),
  Constraints, Session start. §Deploy "not yet approved" until a writer is named.
- `program.yaml` — `program`, `project`, `status: draft`, `transport`, `spec`,
  `changelog`, `fs`, `fs_version`, `decisions`, `memory`, `scope: program`.
- `spec.md` — from `templates/spec.md`; `status: draft`,
  `implemented_version: -`, `fs_version`/`fs_file` from the FS. No FS →
  `fs_version: none`, `fs_file: none`, `spec_version: 0.1`, open questions are the
  scope; every REQ needs a non-empty FS cell = `none` and process-gate REQ/AC only.
  With FS → copy to `spec/source/` immutable, set `fs_version` to the `V<n>` token
  in the file name.
- `CHANGELOG.md` — one row `| v0 | <date> | scaffold created | pending |`.
- `reports/DECISIONS.md` — header + `D-01` for the scaffold decision.

INDEX and project README: add only the **program row** to portfolio `INDEX.md`
and one line to `Projects/<PROJECT>/README.md` §Programs. Never touch other rows
or MCP config.

**Knowledge domains:** ask once with three bundles — `sap-abap, working-method`
(default) / `sap-abap, sap-data, working-method` (reads tables) / "choose myself"
(then list the real names). Prefill from the purpose; every name must resolve under
the memory `knowledge/*.md` folder.

**Memory card:** create `memory/projects/<PROJECT>/<program>.md` from the memory
template, file name exactly `<program>.md` (lowercase, matches the folder) so
closeout can resolve the spec. Fill the resume card (FS, Change type, Production,
Target, Approved scope, Stop condition, Plan).

Verify: list files written, report the lookup result, no SAP object created or
modified.

### Step 5 — Finish

Report the two file paths created. Confirm: no SAP connection was made during
registration, no password was read or stored, and every unknown was asked of the
user. Do not commit anything to git.

## PROMPT (end)
