# Tool map

> Task -> authoritative tool -> fallback. One line per task, so a session never
> chooses a tool by memory. The `## Digest` block below is printed verbatim at
> session start; keep it to a few lines.

## Digest

- Read source through the SAP MCP, not a console dump (encoding).
- One object, one writer per session: readers may overlap, writers may not.
- Run `scripts/tools_now.py` before the first SAP call; it names the live servers and
  the posture each launcher armed.

## Tasks

| Task | Tool | Fallback |
|---|---|---|
| Read ABAP source | (your ADT MCP) | SAP GUI |
| Table data | | |
| Transport | | |
