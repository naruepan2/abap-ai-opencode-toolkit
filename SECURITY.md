# Security policy

## Never commit

- passwords, passphrases, PINs, tokens, API keys
- `.env` files or credential stores
- SAP password files or connection credentials
- customer data, production extracts, personal data
- screenshots that contain credentials or customer data

## Allowed in the instance only

- SAP system IDs, SIDs, and client numbers
- object names, table names, field names, code snippets
- synthetic or public test data

The instance is `workspace/` (memory cards, knowledge, mirrored specs). It is
git-ignored here and stays on this machine or in its own private repository. The
toolkit (`scripts/`, `templates/`, `docs/`, `config/`) carries none of the above:
templates use placeholders, examples use `example-100`.

## If something leaks

1. Rotate the credential immediately.
2. Remove it from the working tree and from git history.
3. Record the incident in `workspace/memory/corrections.md` (without the secret).
4. If the repository was public, assume it was copied.

## Repository visibility

The toolkit is publishable (MIT); the instance is not. `workspace/` is git-ignored
and must never be added to this repository. Before the toolkit goes public, purge
customer data from the history (see the roadmap) — files removed in a later commit
are still readable in earlier ones.
