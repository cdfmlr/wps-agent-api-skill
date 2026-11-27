# WPS Agent API Skill

> 通过 WPS 开放平台 Agent API 读取、创建、编辑 WPS/金山 Office 文档的 Codex Skill + 零依赖 Python 客户端。

**仓库**：<https://github.com/cdfmlr/wps-agent-api-skill>

**Python 3.10+ · 无第三方依赖 · 2026-11-27 实测**

[快速开始](#快速开始) · [能力](#能力) · [作为-Codex-Skill-安装](#作为-codex-skill-安装) · [已知限制](#已知限制) · [免责声明](#免责声明) · [评估报告](docs/evaluation-2026-11-27.md) · [GitHub](https://github.com/cdfmlr/wps-agent-api-skill)

---

## 这是什么

这个项目解决一个具体问题：**用 python-docx 改复杂 Word 文档很费劲。**

页眉页脚、页码、批注、修订、目录、题注、域、内容控件、数学公式、浮动形状、水印……这些在 python-docx 里要么没有 API，要么要手写 OOXML。WPS 开放平台的 Writer API 提供了一套接近 Word 对象模型的 REST 接口，可以直接完成这些操作。

本项目把它封装成：

1. **一个 Codex Skill**：`SKILL.md` 告诉 Agent 什么时候用、怎么用、有哪些坑。
2. **一个零依赖 Python 客户端**：`scripts/wps_api.py`，只用标准库，开箱即用。
3. **一个官方文档查询器**：`scripts/wps_docs.py`，通过 JSON API 读官方文档，不用逐页翻网页。
4. **一套可检索的参考资料**：接口索引、踩坑记录、常用请求体。

---

## 免责声明

本项目是**非官方**的社区项目，与金山办公 / WPS 官方无隶属、合作、赞助或背书关系。

- 本项目只提供客户端代码、Skill 说明和示例，不提供 WPS 服务本身。
- 所有 WPS 相关的账号、API、文档、数据、商标和服务，均归其权利人所有，并受 WPS / 金山办公的相关协议、开放平台条款、隐私政策及适用法律法规约束。
- 使用者调用 WPS API、访问或修改文档时，必须自行确保已获得合法授权，并遵守上述协议与法律；由此产生的账号、数据、权限、费用、合规及法律责任均由使用者自行承担，与本项目及其贡献者无关。
- WPS 服务的可用性、接口变更、限流、收费或停止服务，与本项目无关。

> This is an unofficial community project. It is not affiliated with, endorsed by, or sponsored by Kingsoft/WPS. All WPS-related use is governed by WPS's own terms and applicable laws.

---

## 能力

从官方 1,541 篇文档中整理出的接口规模：

| 域 | 接口数 | 状态 |
|---|---:|---|
| Writer / DOCX | 98 | ✅ 读写已实测 |
| Slides / PPTX | 52 | ✅ 读取已实测；写入接口同 host/token |
| Drive / File | 46 | ✅ 列盘、列目录、创建、下载已实测 |
| Sheets / XLSX | 43 | ⚠️ 只能读；结构化写接口当前 401 |
| DBSheet / 多维表格 | 40 | ⚠️ 需用户 OAuth token，未验证 |
| AirSheet / 智能表格 | 31 | ⚠️ 结构化写接口当前 401 |
| AirPage / 智能文档 | 22 | 文档齐全，未逐项实测 |

### DOCX 重点能力

- **文本**：全文查询/插入/删除/替换/查找；段落和区间的查询/插入/更新/删除。
- **表格**：插入、删除、查询、更新；单元格内容/字体/对齐/背景/合并/拆分；行高、列宽、边框、排序。
- **页面**：节、页面设置、页眉页脚、页码、首页不同、奇偶页不同。
- **结构**：目录、题注、书签、超链接、域、脚注尾注、索引项。
- **协作**：批注/评论、修订查询与接受/拒绝、文档保护。
- **高级**：内容控件、数学公式、OLE 对象、浮动形状、水印、样式、内置属性。
- **万能入口**：`ranges/htmls/insert`（最多 50 万字符 HTML）、`ranges/xmls/insert`（WordML/XML）。

### PPTX 重点能力

- 幻灯片：插入/删除/查询/更新、复制、排序、分节。
- 形状：文本框、图片、线条、自选图形、表格、图表、WebShape。
- 内容：形状文本、表格结构、图表结构、动画绑定。
- 备注、评论、标签：均可读写。

---

## 快速开始

### 1. 配置 Key

```bash
export WPS_AGENT_API_KEY='apik:<sk_id>.<secret_key>'
```

Key 只从环境变量读取，不会写入文件。

### 2. 直接使用脚本

```bash
python3 scripts/wps_api.py drives
python3 scripts/wps_api.py ls <drive_id>
python3 scripts/wps_api.py read https://www.kdocs.cn/l/<link_id>
```

### 3. 生成一份复杂 DOCX

```bash
DRIVE_ID=<drive_id>
FILE_ID=$(python3 scripts/wps_api.py create "$DRIVE_ID" report.docx \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['id'])")

python3 scripts/wps_api.py html "$FILE_ID" assets/demo.html
python3 scripts/wps_api.py header "$FILE_ID" "WPS Agent API 示例"
python3 scripts/wps_api.py page-number "$FILE_ID"
python3 scripts/wps_api.py comment "$FILE_ID" 1 "整篇正文由 HTML 写入。"
python3 scripts/wps_api.py query "$FILE_ID"
python3 scripts/wps_api.py download "$DRIVE_ID" "$FILE_ID" report.docx
```

`assets/demo.html` 包含标题、段落、100% 宽表格、列表和颜色样式。写入后的 DOCX 会带 `header1.xml` / `footer1.xml` 等真实 Word 部件。

实测样例：<https://www.kdocs.cn/l/<demo_link>>

### 4. 查询官方 API 文档

```bash
python3 scripts/wps_docs.py search 页眉
python3 scripts/wps_docs.py get 6297
python3 scripts/wps_docs.py sync /tmp/wps-docs
```

---

## 作为 Codex Skill 安装

```bash
git clone https://github.com/cdfmlr/wps-agent-api-skill.git
cd wps-agent-api-skill
cp -R . "${CODEX_HOME:-$HOME/.codex}/skills/wps-agent-api-skill"
```

安装后在 Codex 中用 `$wps-agent-api-skill` 调用，例如：

```text
用 $wps-agent-api-skill 创建一份带页眉、页脚页码、批注和复杂表格的 DOCX。
```

Skill 的入口是 `SKILL.md`，UI 元数据在 `agents/openai.yaml`。

---

## 典型用法

### 读取 kdocs 分享链接

```bash
python3 scripts/wps_api.py read https://www.kdocs.cn/l/cpSf5NCLgM4i
```

流程：`/v7/links/{link_id}/meta` → `drive_id` / `file_id` → `/content?format=markdown`。

适合阅读、总结、检索，不适合“读出来再写回去”的格式保真场景。

### 修改已有 DOCX

```text
1. documents/texts/query            读全文
2. paragraphs/texts/batch_query     拿段落索引/区间
3. paragraphs/texts/update          改某段
4. ranges/texts/update              改某个字符区间
5. documents/texts/replace          全局替换
6. comments/insert                  加批注
7. revisions/update                 接受/拒绝修订
```

### 读取 PPTX

```http
POST https://api.wps.cn/v7/slides/{file_id}/slides/items/query
{"properties":["COUNT"]}
{"properties":["LIST"]}
```

返回每页的 `slide_id`、`slide_index`、`name`、`layout`。改文字用 `shapes/items/query` + `shapes/texts/update`。

---

## 项目结构

```text
.
├── README.md
├── LICENSE
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── wps_api.py          # 零依赖 WPS API 客户端
│   └── wps_docs.py         # 官方文档 JSON API 查询器
├── references/
│   ├── endpoints.md        # 接口索引（Writer/Slides/File/AirPage...）
│   ├── gotchas.md          # Host、枚举、导出延迟等坑
│   └── recipes.md          # 常用请求体与完整流程
├── docs/
│   └── evaluation-2026-11-27.md   # 首次实测评估报告
└── assets/
    └── demo.html           # DOCX 正文 HTML 模板
```

---

## 核心约定

这几条是实测出来的硬约束，写代码前先看：

| 约束 | 说明 |
|---|---|
| **两个 Host** | 文件/内容抽取走 `openapi.wps.cn`；Writer/Slides 对象模型走 `api.wps.cn` |
| **枚举大写数组** | `["TEXT_CONTENT"]`、`["TABLE_FULL"]`、`["HTML_DATA"]`；小写字符串会报 `unsupported property` |
| **不需要 KSO-1** | Agent Key 场景只带 `Authorization: Bearer <token>` |
| **导出有延迟** | 写入后 10–30 秒 DOCX 才更新；下载要轮询 |
| **下载要带 Bearer** | 存储 URL 直接请求会 `userNotLogin` |
| **复杂表格用 HTML** | `TABLE_FULL` 的 `tcW=0`，部分渲染器会挤成一列 |
| **XLSX 写不了** | `/v7/sheets`、`/v7/airsheet` 用当前 Agent Key 返回 401 |

更多细节见 [references/gotchas.md](references/gotchas.md)。

---

## 已知限制

- **XLSX / 智能表格 / 多维表格写入**：当前 Agent Key 过不了 token 校验，需要用户 OAuth token 或平台后续放开。
- **PPTX 写入**：接口文档齐全，本次只做了读取实测。
- **最终一致性**：写入成功 ≠ 立刻可下载，必须轮询。
- **内容抽取是有损的**：Markdown/plain 适合阅读，不适合格式保真回写。
- **颜色**：`font_style.color_index` 在 insert 中未生效，颜色建议用 HTML/CSS。
- **表格列宽**：`TABLE_COLUMN_WIDTH` / `TABLE_AUTO_FIT` 行为不稳定，复杂表格优先 HTML。

完整评估见 [docs/evaluation-2026-11-27.md](docs/evaluation-2026-11-27.md)。

---

## 开发与验证

### 校验 Skill

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

### 快速自检

```bash
python3 scripts/wps_api.py drives
python3 scripts/wps_docs.py search 批注
```

### 安全

- 不要提交 `.env`、Key、导出的私人文档。
- `WPS_AGENT_API_KEY` 只从环境变量读取。
- 写操作会修改云端文档，批量脚本建议先在小号/测试盘验证。

---

## Contributing

- 欢迎提 Issue / PR。
- 修改后请运行 `quick_validate.py` 和 `scripts/wps_api.py drives` 做基本自检。
- 不要提交 Key、`.env`、私人文档或包含个人信息的导出文件。

## License

本项目采用 [MIT License](LICENSE)。

Copyright (c) 2026 wps-agent-api-skill contributors

MIT 仅覆盖本项目的代码与文档，不覆盖 WPS 服务、API、文档内容、账号数据或商标。WPS 相关使用仍须遵守 WPS 的相关协议（见上文「免责声明」）。
