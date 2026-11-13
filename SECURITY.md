# Security policy

## Never commit

- passwords, passphrases, PINs, tokens, API keys
- `.env` files or credential stores
- SAP password files or connection credentials
- customer data, production extracts, personal data
- screenshots that contain credentials or customer data

## Allowed (private repository only)

- SAP system IDs, SIDs, and client numbers
- object names, table names, field names, code snippets
- synthetic or public test data

## If something leaks

1. Rotate the credential immediately.
2. Remove it from the working tree and from git history.
3. Record the incident in `memory/corrections.md` (without the secret).
4. If the repository was public, assume it was copied.

## Repository visibility

Keep this repository **private**. If the framework is ever shared, split it into
a generic `ai-teammate` repository (no project data) and a private project
repository.
