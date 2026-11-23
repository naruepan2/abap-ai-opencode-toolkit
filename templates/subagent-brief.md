# Bounded subagent brief

Use for read-only delegation. Write the brief to disk **before** spawning — a child
works in its own context and cannot see uncommitted parent state. Never inline whole
file bodies: name them as `@path` references.

```markdown
role:            <read-only role>
objective:       <one question, answerable without further delegation>
target:          <system / client / objects in scope>
context:         @path/to/spec.md, @path/to/evidence.json
canonical lines: <file:line quoted verbatim — never paraphrased>
allowed reads:   <objects/files the child may open>
prohibited:      source_write, activation, scope_change, transport_change
required outputs: verdict, findings, evidence_ids, assumptions, limitations, recommended_actions
quality gate:    <what makes the answer usable; what would make it stale>
```

Rules:

- Quote the canonical line being applied. A paraphrase of a predicate, spec row or
  memory entry is not evidence and may drift.
- The brief is a contract, not a conversation dump. If the child needs more context,
  it asks for a named file; it does not guess.
- Reject stale output when spec revision, source hash, target or evidence changed
  after dispatch. Re-issue a new brief; do not patch the old answer.
- Read depth follows the context window: frontmatter/summaries first, full bodies only
  for the named file the question needs.
- The parent re-verifies every decisive fact before acting on it. A subagent result is
  a sample, not an all-clear.
