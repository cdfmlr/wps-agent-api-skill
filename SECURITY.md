# Security Policy

## Reporting a vulnerability

Please report security issues privately through GitHub Security Advisories
(**Security → Report a vulnerability**). Do not open a public issue for leaked
keys, document data, or account identifiers.

## Secrets and private data

- `WPS_AGENT_API_KEY` / `AGENT_API_KEY` are read from the environment only.
- Never commit `.env` files, API keys, exported private documents, or screenshots
  containing account data.
- If a key is exposed, revoke it in the WPS account center and rotate it.

## Scope

This is an unofficial client for WPS endpoints. Security of the WPS service
itself is out of scope for this repository.
