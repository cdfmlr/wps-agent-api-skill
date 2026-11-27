# Repository Guidelines

## Project Structure & Module Organization

- `SKILL.md` — Codex skill entrypoint: usage triggers, hard rules, workflows. Keep it short; details go in `references/`.
- `scripts/wps_api.py` — zero-dependency client/CLI for auth, drives, reads, DOCX edits, downloads.
- `scripts/wps_docs.py` — local index of official WPS API docs (`search`, `get`, `sync`).
- `references/` — `endpoints.md`, `gotchas.md`, `recipes.md`.
- `assets/demo.html` — sample HTML for `ranges/htmls/insert`.
- `docs/evaluation-2026-11-27.md` — live-test findings and limits.
- `agents/openai.yaml` — skill UI metadata.

No `src/`, automated tests, or CI yet.

## Build, Test, and Development Commands

Python 3.10+, standard library only; no install step.

```bash
python3 scripts/wps_api.py drives                 # smoke test auth + drives
python3 scripts/wps_api.py read https://www.kdocs.cn/l/...  # extract Markdown
python3 scripts/wps_docs.py search 页眉            # query official docs
python3 -m py_compile scripts/*.py                # syntax check
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

`drives` and `read` require `WPS_AGENT_API_KEY`; never hardcode or echo it.

## Coding Style & Naming Conventions

- 4-space indent; `snake_case` functions/variables, `PascalCase` classes (`WPSClient`), `UPPER_CASE` constants.
- Double quotes, f-strings, type hints (`str | None`), `from __future__ import annotations`.
- CLI subcommands are kebab-case (`page-number`); JSON output uses `ensure_ascii=False, indent=2`.
- Chinese comments/docstrings are fine; user-facing docs are mainly Chinese.
- No linter/formatter. Match existing style, keep lines near 100 chars, avoid new dependencies.

## Testing Guidelines

- No automated tests or CI; do not claim "tests pass" without live verification.
- Smoke test: `python3 scripts/wps_api.py drives` and `python3 scripts/wps_docs.py search 批注`.
- After DOCX writes, download and confirm `header1.xml`, `footer1.xml`, or `comments.xml`.
- New tests: `unittest` under `tests/`, files `test_*.py`, mock HTTP so no key is needed.

## Commit & Pull Request Guidelines

- Use Conventional Commits (`feat:`, `docs:`, `chore:`), imperative lowercase summaries, e.g. `feat: add PPTX text update`.
- Branch from `main`. PRs should explain the change, list verification commands, and include live API evidence or a sample export. Link issues; attach screenshots/PDFs for layout changes.

## Security & Configuration Tips

- Key only from `WPS_AGENT_API_KEY` (or `AGENT_API_KEY`), format `apik:<sk_id>.<secret_key>`.
- Never commit `.env`, keys, or exported private documents; use a scratch drive for write tests.
- Host split: `openapi.wps.cn` for files/content, `api.wps.cn` for `/v7/docs` and `/v7/slides`.

## Agent-Specific Instructions

- Keep `SKILL.md` concise; endpoint details belong in `references/`.
- Preserve verified rules: uppercase `properties`, Bearer auth only, poll downloads after writes, HTML for complex tables.
- Update `docs/evaluation-2026-11-27.md` after live-testing new endpoints.
