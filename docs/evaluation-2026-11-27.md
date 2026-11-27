# WPS 开放平台 Agent API 实测评估

> 实测日期：2026-11-27
> 测试对象：`https://www.kdocs.cn/l/cpSf5NCLgM4i`（接入说明）中的 Agent API Key
> 结论先行：**能用，而且对复杂 DOCX 很强。** DOCX 读写已全部实测通过；PPTX 读写也已实测通过；XLSX 可以读（内容抽取），但传统表格/智能表格的写接口目前返回 401。

---

## 1. 一句话结论

这套 API 不是“只能读文档”的摘要接口，而是**接近 Word/PPT 对象模型的 REST API**：

- **DOCX**：98 个 Writer 接口，段落/区间/表格/图片/形状/页眉页脚/目录/题注/书签/域/批注/修订/内容控件/公式/OLE/水印/保护/HTML/WordML 都能改。
- **PPTX**：52 个 Slides 接口，幻灯片、形状、文本框、图表、动画、备注、评论、分节都能改。
- **文件层**：列盘、列目录、新建、上传、下载、复制、移动、删除、权限、版本都能做。
- **XLSX / 智能表格 / 多维表格**：接口文档齐全，但当前 Agent Key 调用返回 `401 unable to parse claims`，需要用户 OAuth token 或等平台放开。

对“python-docx 写起来费劲”的场景，**WPS API 明显更省事**，尤其是页眉页脚、批注、域、内容控件、目录、修订、公式、浮动形状和水印。

---

## 2. 实测通过的链路

### 2.1 读取官方接入说明文档

- `POST /api/authorization/agent/v1/token` 换取 AccessToken：成功，12 小时有效。
- `GET /v7/links/cpSf5NCLgM4i/meta`：成功，拿到 `drive_id=<drive_id>`、`file_id=<file_id>`。
- `GET /v7/drives/{drive_id}/files/{file_id}/content?format=markdown`：成功，`src_format=otl`，返回完整 Markdown。

这说明**分享链接 → drive_id/file_id → 内容抽取**这条链路是通的。

### 2.2 找到当前 Key 能操作的盘

```http
GET /v7/drives?allotee_type=user&page_size=100
```

返回当前账号的两个私有盘：`我的云文档`、`自动上传文档`（具体 ID 省略）。

### 2.3 DOCX 端到端写读

在一个空白 DOCX 上依次验证：

| 操作 | 接口 | 结果 |
|---|---|---|
| 新建 DOCX | `POST /v7/drives/{drive}/files/0/create` | ✅ |
| 写标题/正文 | `POST /v7/docs/{file}/documents/texts/insert` | ✅ 支持 `heading_level`、`font_style`、`paragraph_format` |
| 插入完整表格 | `POST /v7/docs/{file}/documents/tables/insert`（`TABLE_FULL`） | ✅ 表题+表头+数据+边框一次生成 |
| 全文替换 | `POST /v7/docs/{file}/documents/texts/replace` | ✅ 返回 `replaced: true` |
| 设置页眉 | `POST /v7/docs/{file}/documents/header_footers/update` | ✅ `header1.xml` 出现页眉文字 |
| 页脚页码 | 同上，`HEADER_FOOTER_FOOTER_PAGE_NUMBER` | ✅ `footer1.xml` 出现 `PAGE` 域 |
| 段落批注 | `POST /v7/docs/{file}/paragraphs/comments/insert` | ✅ `comments.xml` 出现批注 |
| 区间插入 HTML | `POST /v7/docs/{file}/ranges/htmls/insert` | ✅ 整篇正文+100% 宽表格一次写入 |
| 查询全文 | `POST /v7/docs/{file}/documents/texts/query` | ✅ 可查正文、字数、页数 |
| 下载 DOCX | `GET /v7/drives/{drive}/files/{file}/download` | ✅ 下载地址需带 Bearer |

**产物**：本地生成了 `WPS-API-HTML-测试.docx`（正文由一段 HTML 写入，含页眉、页码、批注）。仓库不附带在线链接，可用 `scripts/wps_api.py` 重新生成。

### 2.4 PPTX 读写

读取：

```http
POST /v7/slides/{file_id}/slides/items/query
{"properties":["COUNT"]}   -> 15 张
{"properties":["LIST"]}    -> 每张的 slide_id / slide_index / name / layout
```

写入：在一个新建的空白 PPTX 上逐项实测。

| 操作 | 接口 | 结果 |
|---|---|---|
| 新建 PPTX | `POST /v7/drives/{drive}/files/0/create` | ✅ 自带 1 页标题版式 |
| 插入幻灯片 | `slides/items/insert`（`layout: 12`） | ✅ |
| 改标题/副标题 | `shapes/texts/update` + `FONT` | ✅ 文字、字号、加粗、颜色 |
| 批量插文本框 | `shapes/items/textboxes` | ✅ 返回 `shape_ids` |
| 插 3×3 表格 | `shapes/items/tables` | ✅ |
| 写单元格 | `shapes/tables/update` `CELL_TEXT` | ✅ 1-based `row`/`column` |
| 查找替换 | `shapes/texts/update` `TEXT_REPLACE` | ✅ |
| 追加文本 | `shapes/texts/append` | ✅ |
| 改形状位置尺寸 | `shapes/items/update` `GEOMETRY` | ✅ |
| 演讲者备注 | `slides/notes/insert` / `query` | ✅ |
| 下载校验 | `GET /v7/drives/.../download` | ✅ 2 页 + `notesSlide1.xml` |

**产物**：本地生成了 `WPS-API-PPT-测试.pptx`（2 页；标题页含 2 个文本框，第二页含 3×3 表格和文本框，第 1 页有演讲者备注）。仓库不附带在线链接。

注意两点：

- Slides 实际走 `api.wps.cn`；官方文档写 `openapi.wps.cn`，但实测后者返回 401。
- `properties` 同样必须是大写数组；文档里的小写字符串或标量会报 `unsupported property` / protobuf 解析错误。

### 2.5 XLSX 的现状

```http
GET /v7/sheets/{file_id}/worksheets
GET /v7/airsheet/{file_id}/worksheets
```

两个都在 `openapi.wps.cn` 返回：

```json
{"errno":10000,"msg":"unable to parse claims","result":"permissionDenied"}
```

换 `api.wps.cn` 则 404。结论：**传统表格/智能表格服务与 DOCX/PPTX 不是同一套 token 校验，当前 Agent Key 过不去。**

不过，**读 Excel 是可以的**：走内容抽取接口即可，例如 `test.xlsx` 返回：

```json
{"src_format":"xlsx","markdown":"## Sheet1\n| -5 | -4 | ... |"}
```

所以现状是：**Excel 能读成 Markdown，但不能用结构化接口写回。** 若需要自动改 Excel，需要另配用户 OAuth token，或向平台确认是否支持 Agent Key。

---

## 3. 能力地图

从官方文档站抓取并解析了 **1541 篇**文档，去重后的接口数量大致如下：

| 域 | 接口数 | 说明 |
|---|---:|---|
| Writer / DOCX | 98 | 文字文档对象模型 |
| Slides / PPTX | 52 | 幻灯片、形状、图表、动画 |
| Drive / File | 46 | 盘、目录、上传下载、权限、版本 |
| Sheets / XLSX | 43 | 传统电子表格（当前 Key 401） |
| DBSheet / 多维表格 | 40 | 记录、字段、视图、Webhook（当前 Key 未验证） |
| AirSheet / 智能表格 | 31 | 单元格、条件格式、数据校验（当前 Key 401） |
| AirPage / 智能文档 | 22 | 块级 CRUD、Markdown/HTML 转块、导出 DOCX/PDF |
| 其他 | 很多 | 通讯录、消息、日历、审批、邮箱、待办、会议等 |

### Writer（DOCX）重点能力

- **文本**：全文查询/插入/删除/替换/查找；段落查询/插入/更新/删除；区间查询/插入/更新/删除。
- **表格**：插入、删除、查询、更新；单元格内容/字体/对齐/背景/合并/拆分；行高、列宽、边框、排序、自动调整。
- **图片/形状**：嵌入图片、浮动形状、OLE 对象的插入/查询/更新/删除。
- **页面**：节、页面设置、页眉页脚、页码、首页不同、奇偶页不同。
- **结构**：目录、题注、书签、超链接、域、脚注尾注、索引项。
- **协作**：批注/评论、修订查询与接受/拒绝、文档保护。
- **高级**：内容控件、数学公式、水印、文档样式、内置属性。
- **万能入口**：`ranges/htmls/insert` 可插入最多 50 万字符 HTML；`ranges/xmls/insert` 可插入 WordML/XML。

### Slides（PPTX）重点能力

- 幻灯片：插入/删除/查询/更新、复制、排序、分节。
- 形状：文本框、图片、线条、自选图形、表格、图表、WebShape。
- 内容：形状文本、表格结构、图表结构、动画绑定。
- 备注/评论/标签：均可读写。

### AirPage（智能文档）

- 块级 `batch_get / batch_create / batch_update / batch_delete`。
- Markdown 或 HTML 转文档块。
- 导出 DOCX / PDF / HTML / Markdown。

---

## 4. 推荐怎么用

### 场景 A：从零生成一份复杂 DOCX

推荐顺序：

1. `create` 新建 `.docx`。
2. **优先用 `ranges/htmls/insert` 写整篇正文**（标题、段落、表格、颜色、宽度一次搞定）。
3. 再用对象模型补：页眉、页脚页码、目录、批注、题注、域。
4. `download` 轮询下载并校验。

实测：用 HTML 生成的表格是 `tblW=100%`，列宽正常；而 `TABLE_FULL` 生成的表格单元格宽度是 `0`，在 Word/LibreOffice 里容易挤成一列。

### 场景 B：改一份已有 DOCX

1. `documents/texts/query` 拿全文。
2. `paragraphs/texts/query` / `batch_query` 拿段落索引与区间。
3. `paragraphs/texts/update`、`ranges/texts/update` 精准改。
4. `documents/texts/replace` 做全局替换。
5. `comments/insert` 加批注，`revisions/update` 接受/拒绝修订。

**不要**用内容抽取接口做“读出来 → 改字符串 → 整篇写回”，那会丢格式。内容抽取只适合阅读/总结。

### 场景 C：改 PPTX

1. `slides/items/query` 拿 `slide_id`（不是 1-based 的 `slide_index`）。
2. `shapes/items/query` 拿 `shape_id`、类型和位置。
3. `shapes/texts/update` 改文字/字体；`TEXT_REPLACE` 做页内替换；`shapes/texts/append` 追加。
4. `shapes/items/textboxes` / `tables` 插新内容；`shapes/items/update` 改位置尺寸。
5. `shapes/tables/query` + `update` 读写单元格（1-based）。
6. `slides/items/insert` 插空白页（`layout: 12`）；`slides/notes/*` 写备注。
7. `slides/animations/*` 做动画。

段落对齐更新目前不稳定：`paragraph.alignment` 传 `pp_align_center` 等值会返回 `invalid alignment`；文字和字体正常。

---

## 5. 实测踩到的坑（很重要）

1. **两个 Host 分工不同**
   - `openapi.wps.cn`：云盘、文件、内容抽取、新建、下载。
   - `api.wps.cn`：Writer / Slides 对象模型（DOCX/PPTX 的 `/v7/docs`、`/v7/slides`）。
   - 把 `/v7/docs` 发到 `openapi.wps.cn` 会 401 `unable to parse claims`。

2. **`properties` 必须是大写枚举数组**
   - 文档里写的是小写字符串，例如 `"text_content"`，实际会报 `unsupported property`。
   - 实测可用：`["TEXT_CONTENT"]`、`["TEXT_HEADING"]`、`["TABLE_FULL"]`、`["HTML_DATA"]`、`["COUNT"]`、`["LIST"]`。

3. **不需要 KSO-1 签名**
   - 文档标了 `X-Kso-Date` / `X-Kso-Authorization`，但 Agent Key 场景不用带；带了反而可能报错。

4. **写入后导出有延迟**
   - 新建/插入后立刻下载，可能拿到旧版本；表格、HTML、页眉页脚、批注大约要等 10–30 秒才出现在 DOCX 里。
   - 正确做法：轮询下载，直到文件大小稳定（`wps_api.py` 已内置）。

5. **下载地址需要带 Authorization**
   - `download` 返回的存储 URL 直接 `curl` 会 `userNotLogin`；必须加 `Authorization: Bearer <token>`。

6. **`TABLE_FULL` 的列宽是 0**
   - 生成结构正确，但 `tcW=0`，部分渲染器会挤成一列。
   - 复杂表格优先用 HTML；如果非要用 `TABLE_FULL`，插入后再用 `TABLE_AUTO_FIT` / `TABLE_COLUMN_WIDTH` 调，但实测列宽参数比较难控。

7. **颜色枚举有坑**
   - `font_style.color_index = wd_color_index_red` 在 insert 里没有生效；`bold`、`font_size` 正常。
   - 颜色建议用 HTML/CSS，或者插入后用样式接口处理。

8. **内容抽取不是 DOCX 解析器**
   - 测试用的分享链接返回 `src_format=otl`，抽取结果是 Markdown，适合阅读/总结，不适合回写保格式。

9. **本地预览缺字体**
   - 用 LibreOffice 转 PDF 时中文显示为方框，是本机缺 `宋体/SimHei`，不是文档问题；WPS 云端打开正常。

---

## 6. 和 python-docx 怎么选

| 维度 | python-docx | WPS 开放平台 API |
|---|---|---|
| 页眉页脚 / 页码 | 能做，但字段和节处理麻烦 | 原生 `header_footers/update` |
| 批注 / 修订 | 基本没有或要 hack | 原生增删改查、接受/拒绝 |
| 内容控件 / 域 / 目录 | 很麻烦 | 原生接口 |
| 公式 / 浮动形状 / 水印 | 很难 | 原生接口 |
| 复杂 HTML 排版 | 要自己转换 | `ranges/htmls/insert` 直接吃 HTML |
| 离线 / 无网络 | ✅ | ❌ 需要网络 |
| 细粒度 XML 控制 | ✅ 最强 | 受接口能力约束 |
| 速度 | 本地快 | 有网络往返 + 导出延迟 |
| 版式保真 | 取决于自己写得好不好 | WPS 自家引擎生成，DOCX 兼容性通常更好 |

**建议**：本地批处理、纯文本/简单表格继续用 python-docx；复杂版式、页眉页脚、批注、目录、修订、PPT 这类，优先用 WPS API。

---

## 7. 可复用代码

### `scripts/wps_api.py`

仅标准库，无第三方依赖。Key 只从环境变量读取，不落盘。

```bash
export WPS_AGENT_API_KEY='apik:...'

python3 scripts/wps_api.py drives
python3 scripts/wps_api.py ls <drive_id>
python3 scripts/wps_api.py read https://www.kdocs.cn/l/cpSf5NCLgM4i
python3 scripts/wps_api.py create <drive_id> 测试.docx
python3 scripts/wps_api.py query <file_id>
python3 scripts/wps_api.py html <file_id> assets/demo.html
python3 scripts/wps_api.py header <file_id> "WPS Agent API 示例"
python3 scripts/wps_api.py page-number <file_id>
python3 scripts/wps_api.py comment <file_id> 1 "整篇正文由 HTML 写入。"
python3 scripts/wps_api.py download <drive_id> <file_id> out.docx

python3 scripts/wps_api.py slides <file_id>
python3 scripts/wps_api.py shapes <file_id> <slide_id>
python3 scripts/wps_api.py add-textbox <file_id> <slide_id> "标题"
python3 scripts/wps_api.py add-table <file_id> <slide_id> --rows 3 --cols 3
python3 scripts/wps_api.py add-note <file_id> <slide_id> "备注"
```

### 完整示例

新建 DOCX → 写入 `assets/demo.html` → 页眉/页码/批注 → 下载的完整命令见项目根目录 `README.md` 的「快速开始」。

---

## 8. 安全备注

- 全程没有把 Key 写入任何文件，也没有回显完整 Key。
- 测试产生的临时文档已清理；仓库和公开页面均不保留演示文档链接或账号标识。
