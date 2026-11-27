# Recipes

All examples assume:

```bash
export WPS_AGENT_API_KEY='apik:...'
TOKEN=$(python3 -c "from scripts.wps_api import WPSClient;print(WPSClient().token)")
```

Prefer `scripts/wps_api.py` for end-to-end work; the raw requests below show the contract.

## 1. Resolve and read a kdocs share link

```http
GET https://openapi.wps.cn/v7/links/cpSf5NCLgM4i/meta
Authorization: Bearer <token>
```

Response contains `drive_id` and `file_id`. Then:

```http
GET https://openapi.wps.cn/v7/drives/{drive_id}/files/{file_id}/content?format=markdown
Authorization: Bearer <token>
```

`format` may be `markdown` or `plain`. This is read-only extraction.

## 2. List drives and files

```http
GET https://openapi.wps.cn/v7/drives?allotee_type=user&page_size=100
GET https://openapi.wps.cn/v7/drives/{drive_id}/files/0/children?page_size=100
Authorization: Bearer <token>
```

`parent_id=0` is the root. The response items include `type` (`file|folder`), `id`, `name`, `link_url`, `size`, `mtime`.

## 3. Create a DOCX

```http
POST https://openapi.wps.cn/v7/drives/{drive_id}/files/0/create
Authorization: Bearer <token>
Content-Type: application/json

{"file_type":"file","name":"report.docx","on_name_conflict":"rename"}
```

The response `data.id` is the `file_id` used by Writer APIs.

## 4. Write the whole body from HTML (recommended for layout)

```http
POST https://api.wps.cn/v7/docs/{file_id}/ranges/htmls/insert
Authorization: Bearer <token>
Content-Type: application/json

{
  "properties": ["HTML_DATA"],
  "range": {"begin": 0, "end": 0},
  "html": "<h1>标题</h1><p>正文</p><table style=\"width:100%;border-collapse:collapse\">...</table>"
}
```

Limits: 1–500,000 characters. This imports headings, paragraphs, lists, tables, borders, background colors, and basic inline CSS.

For a working template, see `assets/demo.html`.

## 5. Add text with formatting (object model)

```json
{
  "properties": ["TEXT_HEADING"],
  "text": "一、核心结论",
  "heading_level": 2,
  "is_br": true
}
```

```json
{
  "properties": ["TEXT_CONTENT"],
  "text": "这是正文。",
  "is_br": true,
  "font_style": {"bold": true, "font_size": 12},
  "paragraph_format": {"alignment": "wd_paragraph_alignment_justify", "space_after": 6}
}
```

Use `["TEXT_CONTENT"]` for body paragraphs and `["TEXT_HEADING"]` for headings.

## 6. Header, footer, page number

```json
{"properties":["HEADER_FOOTER_HEADER_CONTENT"],"section_index":1,"content":"公司内部资料"}
```

```json
{"properties":["HEADER_FOOTER_FOOTER_PAGE_NUMBER"],"section_index":1,"enabled":true}
```

Endpoint: `POST https://api.wps.cn/v7/docs/{file_id}/documents/header_footers/update`.

Also available: `HEADER_FOOTER_HEADER_FONT`, `HEADER_FOOTER_FOOTER_FONT`, `HEADER_FOOTER_HEADER_ALIGNMENT`, `HEADER_FOOTER_DIFFERENT_FIRST`, `HEADER_FOOTER_DIFFERENT_ODD_EVEN`, `HEADER_FOOTER_PAGE_NUMBER_STYLE`, `HEADER_FOOTER_FULL`.

## 7. Comments

```json
{"properties":["COMMENT_DATA"],"paragraph_index":2,"text":"这条批注由 API 写入。"}
```

Endpoint: `POST https://api.wps.cn/v7/docs/{file_id}/paragraphs/comments/insert`.

For a text range, use `/v7/docs/{file_id}/ranges/comments/insert`.

## 8. Read text and locate paragraphs

```json
{"properties":["TEXT_CONTENT","TEXT_WORD_COUNT","TEXT_PAGE_COUNT"]}
```

Endpoint: `POST /v7/docs/{file_id}/documents/texts/query`.

For structure, use `paragraphs/texts/batch_query` to get paragraph indexes and ranges. Then:

- `paragraphs/texts/update` — change one paragraph
- `ranges/texts/update` — change a character range
- `documents/texts/replace` — global replace
- `documents/texts/search` — find occurrences

## 9. Global replace

```json
{"properties":["TEXT_CONTENT"],"find_text":"旧文本","replace_text":"新文本","is_all":true}
```

Endpoint: `POST /v7/docs/{file_id}/documents/texts/replace`.

## 10. Table (fallback)

```json
{
  "properties": ["TABLE_FULL"],
  "rows": 4,
  "cols": 3,
  "full_data": {
    "caption": "表 1 对比",
    "headers": ["能力","A","B"],
    "rows": [{"cells":["x","y","z"]}],
    "enable_borders": true
  }
}
```

Endpoint: `POST /v7/docs/{file_id}/documents/tables/insert`.

Remember the `tcW=0` caveat; use HTML for portable width.

## 11. Download and verify

```python
from scripts.wps_api import WPSClient
c = WPSClient()
print(c.download("<drive_id>", file_id, "out.docx"))
```

`download()` sleeps, polls, and writes the last stable bytes. It also adds the required Bearer header to the storage URL.

To verify a DOCX structurally:

```python
import zipfile
z = zipfile.ZipFile("out.docx")
print([n for n in z.namelist() if "header" in n or "footer" in n or "comment" in n])
print(z.read("word/document.xml").decode().count("<w:tbl>"))
```

## 12. PPTX read

```json
{"properties":["COUNT"]}
```

```json
{"properties":["LIST"]}
```

Endpoint: `POST https://api.wps.cn/v7/slides/{file_id}/slides/items/query`.

`LIST` returns `slide_id`, `slide_index`, `name`, `layout`.

To edit text: query `shapes/items`, then use `shapes/texts/update`. Shapes support textboxes, pictures, lines, autoshapes, tables, charts, and WebShape; animations, notes, comments, and sections are separate endpoints.

## 13. XLSX read

```http
GET https://openapi.wps.cn/v7/drives/{drive_id}/files/{file_id}/content?format=markdown
```

Returns Markdown tables. Structured write APIs (`/v7/sheets`, `/v7/airsheet`) return 401 with the Agent Key.

## 14. AirPage block editing

AirPage (智能文档) exposes block CRUD:

- `POST /v7/airpage/v2/{file_id}/blocks/batch_get`
- `POST /v7/airpage/v2/{file_id}/blocks/batch_create`
- `POST /v7/airpage/v2/{file_id}/blocks/batch_update`
- `POST /v7/airpage/v2/{file_id}/blocks/batch_delete`

And conversion:

- `POST /v7/airpage/{file_id}/export_to_docx`
- `POST /v7/airpage/{file_id}/export_to_pdf`

Use `scripts/wps_docs.py search 块` for block data structures.

## 15. Look up official docs

```bash
python3 scripts/wps_docs.py search 页眉
python3 scripts/wps_docs.py get 6297
python3 scripts/wps_docs.py sync /tmp/wps-docs
```

The docs API is public and needs no key:
`GET https://open.wps.cn/docs/api/collections/wps365?lang=zh-CN`
`GET https://open.wps.cn/docs/api/doc/{doc_id}?lang=zh-CN&source=dms`
