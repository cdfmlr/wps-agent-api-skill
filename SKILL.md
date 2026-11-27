---
name: wps-agent-api-skill
description: Read, create, and edit WPS/Kingsoft Office files (DOCX/PPTX and kdocs share links) through the WPS Open Platform Agent API. Use for complex Word/PPT edits such as headers and footers, comments, TOCs, fields, content controls, tables, HTML layout, or when python-docx is awkward. The Agent Key can read XLSX but structured spreadsheet writes currently return 401.
metadata:
  short-description: Edit WPS Office files via Agent API
---

# WPS Agent API

Use the bundled standard-library client; no `pip install` is needed.

## Prerequisites

- `WPS_AGENT_API_KEY` (or `AGENT_API_KEY`) must be set, format `apik:<sk_id>.<secret_key>`.
- If the key is missing, stop and ask the user to set it up themselves. Point them to the official guide (https://www.kdocs.cn/l/cpSf5NCLgM4i) and the key page (https://account.wps.cn/usercenter/agent-identity). Never ask them to paste the key into chat.
- Never print, echo, or write the key into files or the repository. Only check that it exists.
- Network access to `account.wps.cn`, `openapi.wps.cn`, and `api.wps.cn`.
- Docs lookup (`scripts/wps_docs.py`) also needs `open.wps.cn`.
- Downloads fetch the storage URL returned by the API (observed: `hwc-bj.ag.wps.cn`); allowlist it, or permit `*.wps.cn` when egress filtering is enabled.

## Hard rules

1. **Two hosts.**
   - `https://openapi.wps.cn`: drives, files, content extraction, create, download.
   - `https://api.wps.cn`: Writer (`/v7/docs`) and Slides (`/v7/slides`) object models.
   - Sending `/v7/docs` to `openapi.wps.cn` returns `401 unable to parse claims`.
2. **`properties` is an uppercase array.** Use `["TEXT_CONTENT"]`, `["TEXT_HEADING"]`, `["TABLE_FULL"]`, `["HTML_DATA"]`, `["COUNT"]`, `["LIST"]`. The lowercase strings shown in some official docs return `unsupported property`.
3. **Do not add KSO-1 headers** for Agent Key auth. `Authorization: Bearer <access_token>` is sufficient.
4. **Writes are eventually consistent.** Export to DOCX can lag 10–30 seconds. Poll the download until the bytes stabilize before validating.
5. **Download URLs need auth.** The storage URL returned by the download API requires `Authorization: Bearer <token>`; otherwise it returns `userNotLogin`.
6. **Prefer HTML for complex layout.** `ranges/htmls/insert` produces portable tables (`tblW=100%`). `TABLE_FULL` creates `tcW=0` cells that can collapse in Word/LibreOffice.
7. **XLSX is read-only with this key.** Read via content extraction. `/v7/sheets` and `/v7/airsheet` writes return `401 unable to parse claims`.
8. **Failures raise `WPSAPIError`.** Non-zero `code`/`errno` and HTTP errors are exceptions; the CLI exits 1. There is no automatic retry, so handle 429/5xx at the call site.

## Quick start

```bash
python3 scripts/wps_api.py drives
python3 scripts/wps_api.py ls <drive_id>
python3 scripts/wps_api.py read https://www.kdocs.cn/l/<link_id>
python3 scripts/wps_api.py create <drive_id> demo.docx
python3 scripts/wps_api.py html <file_id> assets/demo.html
python3 scripts/wps_api.py header <file_id> "公司内部资料"
python3 scripts/wps_api.py page-number <file_id>
python3 scripts/wps_api.py comment <file_id> 1 "批注内容"
python3 scripts/wps_api.py query <file_id>
python3 scripts/wps_api.py download <drive_id> <file_id> out.docx
```

## Standard DOCX workflow

1. Resolve a share link with `/v7/links/{link_id}/meta` when the user gives a kdocs URL.
2. Create a blank `.docx` with `POST /v7/drives/{drive_id}/files/0/create`.
3. Write the body with `POST /v7/docs/{file_id}/ranges/htmls/insert` at range `{begin:0,end:0}`.
4. Add headers, page numbers, and comments with `header_footers/update` and `paragraphs/comments/insert`.
5. Download with the bundled poll-until-stable helper, then verify the DOCX parts (`header1.xml`, `footer1.xml`, `comments.xml`) when correctness matters.

For a ready-made example, read [references/recipes.md](references/recipes.md).

## Editing an existing DOCX

1. `documents/texts/query` to read content and word/page counts.
2. `paragraphs/texts/query` or `paragraphs/texts/batch_query` to get paragraph indexes and ranges.
3. `paragraphs/texts/update`, `ranges/texts/update`, or `documents/texts/replace` to change content.
4. `comments/insert`, `revisions/update`, `tocs/insert`, `header_footers/update` for document-level features.

Do **not** round-trip through content extraction (`/content?format=markdown`) when formatting matters; it loses layout.

## PPTX

Read and write are both live-tested. Slides live on `https://api.wps.cn`; the official docs' `openapi.wps.cn` returns 401.

- List: `POST /v7/slides/{file_id}/slides/items/query` with `{"properties":["COUNT"]}` or `["LIST"]`. Use the returned `slide_id`, not the 1-based `slide_index`.
- Shapes: `POST /v7/slides/{file_id}/shapes/items/query` with `{"target":{"slide_id":...},"properties":["LIST"]}`.
- Text: read `shapes/texts/query`; replace with `shapes/texts/update` (`TEXT_CONTENT`), find/replace with `TEXT_REPLACE`, append with `shapes/texts/append`.
- New content: `shapes/items/textboxes`, `shapes/items/tables`, `slides/items/insert` (blank layout `12`).
- Tables: read `shapes/tables/query` with `["CELLS"]`; write a cell with `shapes/tables/update` `["CELL_TEXT"]` and 1-based `row`/`column`.
- Notes: `slides/notes/insert|query|update|append`.
- Font updates work (`name`, `size`, `bold`, `color` as `#RRGGBB`). Paragraph `alignment` updates return `invalid alignment`; avoid them for now.

CLI: `slides`, `shapes`, `shape-text`, `set-text`, `add-textbox`, `add-slide`, `add-table`, `table-cells`, `set-cell`, `notes`, `add-note`.

## Official docs lookup

Do not browse the docs site page by page. Use the bundled helper:

```bash
python3 scripts/wps_docs.py search 页眉
python3 scripts/wps_docs.py get 6332
python3 scripts/wps_docs.py sync /tmp/wps-docs
```

## References

- [references/endpoints.md](references/endpoints.md): capability map and the most useful endpoints.
- [references/gotchas.md](references/gotchas.md): host/token/enum/export pitfalls and error meanings.
- [references/recipes.md](references/recipes.md): request bodies for common DOCX/PPTX workflows.
