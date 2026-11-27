# WPS Agent API pitfalls

Verified against a live Agent Key on 2026-11-27.

## Host split

| Purpose | Host | Example |
| --- | --- | --- |
| Token exchange | `account.wps.cn` | `POST /api/authorization/agent/v1/token` |
| Drives, files, upload, download, content extraction | `openapi.wps.cn` | `/v7/drives/...`, `/v7/links/...` |
| Writer DOCX object model | `api.wps.cn` | `/v7/docs/{file_id}/...` |
| Slides PPTX object model | `api.wps.cn` | `/v7/slides/{file_id}/...` |

Sending `/v7/docs` to `openapi.wps.cn` returns:

```json
{"errno":10000,"msg":"unable to parse claims","result":"permissionDenied"}
```

## Auth

```http
POST https://account.wps.cn/api/authorization/agent/v1/token
Content-Type: application/json

{"grant_type":"api_key","api_key":"apik:<sk_id>.<secret_key>"}
```

Use `Authorization: Bearer <access_token>` afterwards. The token is valid for 12 hours.

- Do **not** add `X-Kso-Date` or `X-Kso-Authorization` unless the app explicitly enables interface signing. For Agent Key auth they are unnecessary and can cause errors.
- `X-Kso-Id-Type: internal|external` is optional; the default works.

## `properties` must be an uppercase array

Official tables show lowercase strings such as `text_content`, but live endpoints require uppercase enum names in an array:

| Works | Fails |
| --- | --- |
| `["TEXT_CONTENT"]` | `"text_content"` |
| `["TEXT_HEADING"]` | `"text_heading"` |
| `["TABLE_FULL"]` | `"table_full"` |
| `["HTML_DATA"]` | `"html_data"` |
| `["COMMENT_DATA"]` | `"comment_data"` |
| `["HEADER_FOOTER_HEADER_CONTENT"]` | `"header_footer_header_content"` |
| `["COUNT"]`, `["LIST"]` (Slides) | `"count"`, `"list"` |

Lowercase gives `400 400000002 unsupported property: ...`.

`properties` itself must be an array. A bare string gives `proto: syntax error`.

## Writes are eventually consistent

Creating a file or writing content returns success before the DOCX export is ready. An immediate download can return the previous version. In live tests, tables/HTML/headers/footers/comments appeared after roughly 10–30 seconds.

Use the bundled `WPSClient.download()` which waits and polls. If writing your own loop, require at least two identical non-empty downloads several seconds apart.

## Download storage URL needs Bearer

`GET /v7/drives/{drive_id}/files/{file_id}/download` returns a storage URL. Fetching it without auth returns:

```json
{"result":"userNotLogin","msg":"userNotLogin"}
```

Add `Authorization: Bearer <token>` to the storage request.

## Tables: prefer HTML

`TABLE_FULL` creates structurally valid tables but sets each cell width to `tcW=0` and grid columns to 360 twips. Word/LibreOffice may collapse the columns into one narrow strip.

For portable complex tables, insert HTML:

```json
{"properties":["HTML_DATA"],"range":{"begin":0,"end":0},
 "html":"<table style=\"width:100%;border-collapse:collapse\">...</table>"}
```

An HTML table produces `tblW=5000 pct` (100%) and sensible grid widths.

`TABLE_COLUMN_WIDTH` / `TABLE_AUTO_FIT` exist, but `col` / `start_col` behavior is inconsistent; a width of `3600` produced 72000-twip columns in one test. Treat them as fine-tuning, not reliable layout control.

## Colors

`font_style.color_index = wd_color_index_red` did not take effect in `texts/insert`, while `bold` and `font_size` did. Use HTML/CSS for color, or an update/style endpoint.

## Content extraction is not a DOCX parser

`/content?format=markdown` is for reading and summarizing. It loses layout and cannot round-trip. Do not use it as “read → modify string → write back” when formatting matters.

The provided link returned `src_format=otl` (online document), not `docx`.

## Spreadsheets

With the Agent Key tested:

- Reading works: `GET /v7/drives/{drive}/files/{file}/content?format=markdown` returns Markdown tables for `.xlsx`.
- Structured writes fail: `/v7/sheets/...` and `/v7/airsheet/...` return `401 unable to parse claims`.

Do not promise Excel automation with this key. Ask for a user OAuth token if spreadsheet writes are required.

## Concurrency and locks

Avoid concurrent writes to the same document. Lock conflicts return:

- `400000005` — lock already held
- `400000006` — release failed or lock missing

Retry sequentially with a short backoff.

## Allowed file extensions for create

`POST /v7/drives/{drive_id}/files/{parent_id}/create` supports names with:
`doc, docx, form, xls, otl, ppt, dbt, xlsx, pptx`
(plus public-cloud-only formats such as `pom, spt, dppt, link, resh, ckt, ddoc, dpdf, dxls, pof, wpsnote`).

Use `on_name_conflict: fail | rename | overwrite | replace`.
