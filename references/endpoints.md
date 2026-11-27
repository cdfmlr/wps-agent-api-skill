# WPS Agent API endpoint reference

Generated from the official WPS docs API (1,541 pages, 2026-11-27). Methods come from each endpoint's official page.
Use `python3 scripts/wps_docs.py search <keyword>` / `get <doc_id>` for request bodies and full parameter tables.

## Writer / DOCX (98)

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v7/docs/{file_id}/documents/bookmarks/delete` | 删除书签 |
| POST | `/v7/docs/{file_id}/documents/bookmarks/query` | 查询书签 |
| POST | `/v7/docs/{file_id}/documents/bookmarks/update` | 更新书签 |
| POST | `/v7/docs/{file_id}/documents/captions/insert` | 插入题注 |
| POST | `/v7/docs/{file_id}/documents/comments/delete` | 删除批注 |
| POST | `/v7/docs/{file_id}/documents/comments/insert` | 添加批注 |
| POST | `/v7/docs/{file_id}/documents/comments/query` | 查询评论、批注 |
| POST | `/v7/docs/{file_id}/documents/comments/update` | 修改批注 |
| POST | `/v7/docs/{file_id}/documents/content_controls/delete` | 删除内容控件 |
| POST | `/v7/docs/{file_id}/documents/content_controls/insert` | 插入内容控件 |
| POST | `/v7/docs/{file_id}/documents/content_controls/query` | 查询内容控件 |
| POST | `/v7/docs/{file_id}/documents/content_controls/update` | 更新内容控件 |
| POST | `/v7/docs/{file_id}/documents/fields/delete` | 删除域 |
| POST | `/v7/docs/{file_id}/documents/fields/insert` | 插入域 |
| POST | `/v7/docs/{file_id}/documents/fields/query` | 查询域 |
| POST | `/v7/docs/{file_id}/documents/fields/update` | 更新域 |
| POST | `/v7/docs/{file_id}/documents/footnote_endnotes/delete` | 删除脚注尾注 |
| POST | `/v7/docs/{file_id}/documents/footnote_endnotes/insert` | 插入脚注尾注 |
| POST | `/v7/docs/{file_id}/documents/footnote_endnotes/query` | 查询脚注尾注 |
| POST | `/v7/docs/{file_id}/documents/footnote_endnotes/update` | 更新脚注尾注 |
| POST | `/v7/docs/{file_id}/documents/formulas/insert` | 插入数学公式 |
| POST | `/v7/docs/{file_id}/documents/formulas/query` | 查询文档中的数学公式 |
| POST | `/v7/docs/{file_id}/documents/header_footers/query` | 查询页眉页脚 |
| POST | `/v7/docs/{file_id}/documents/header_footers/update` | 更新页眉页脚 |
| POST | `/v7/docs/{file_id}/documents/hyperlinks/delete` | 删除超链接 |
| POST | `/v7/docs/{file_id}/documents/hyperlinks/query` | 查询超链接 |
| POST | `/v7/docs/{file_id}/documents/hyperlinks/update` | 修改超链接 |
| POST | `/v7/docs/{file_id}/documents/images/delete` | 删除嵌入式图片 |
| POST | `/v7/docs/{file_id}/documents/images/insert` | 在文档末尾插入图片 |
| POST | `/v7/docs/{file_id}/documents/images/query` | 查询嵌入式图片信息 |
| POST | `/v7/docs/{file_id}/documents/images/update` | 更新嵌入图片 |
| POST | `/v7/docs/{file_id}/documents/lists/update` | 批量按级别应用列表模板 |
| POST | `/v7/docs/{file_id}/documents/ole/insert` | 在 OLE 对象后插入文本 |
| POST | `/v7/docs/{file_id}/documents/ole/query` | 查询 OLE 内嵌对象 |
| POST | `/v7/docs/{file_id}/documents/protections/query` | 查询文档保护状态 |
| POST | `/v7/docs/{file_id}/documents/protections/update` | 文档保护 |
| POST | `/v7/docs/{file_id}/documents/revisions/query` | 查询修订信息 |
| POST | `/v7/docs/{file_id}/documents/revisions/update` | 操作修订（开关、接受、拒绝） |
| POST | `/v7/docs/{file_id}/documents/sections/delete` | 删除节 |
| POST | `/v7/docs/{file_id}/documents/sections/query` | 查询页面设置 |
| POST | `/v7/docs/{file_id}/documents/sections/update` | 设置页面属性 |
| POST | `/v7/docs/{file_id}/documents/shapes/delete` | 删除浮动形状 |
| POST | `/v7/docs/{file_id}/documents/shapes/insert` | 插入浮动形状 |
| POST | `/v7/docs/{file_id}/documents/shapes/query` | 查询浮动形状 |
| POST | `/v7/docs/{file_id}/documents/shapes/update` | 更新浮动形状 |
| POST | `/v7/docs/{file_id}/documents/styles/delete` | 删除文档样式 |
| POST | `/v7/docs/{file_id}/documents/styles/insert` | 新建文档样式 |
| POST | `/v7/docs/{file_id}/documents/styles/query` | 查询文档样式 |
| POST | `/v7/docs/{file_id}/documents/styles/update` | 修改文档样式 |
| POST | `/v7/docs/{file_id}/documents/tables/delete` | 删除表格 |
| POST | `/v7/docs/{file_id}/documents/tables/insert` | 在文档末尾插入表格 |
| POST | `/v7/docs/{file_id}/documents/tables/query` | 查询表格信息 |
| POST | `/v7/docs/{file_id}/documents/tables/update` | 更新表格 |
| POST | `/v7/docs/{file_id}/documents/texts/delete` | 删除全文内容 |
| POST | `/v7/docs/{file_id}/documents/texts/insert` | 在文档末尾插入文本 |
| POST | `/v7/docs/{file_id}/documents/texts/query` | 查询全文文本 |
| POST | `/v7/docs/{file_id}/documents/texts/replace` | 全文替换 |
| POST | `/v7/docs/{file_id}/documents/texts/search` | 全文查找 |
| POST | `/v7/docs/{file_id}/documents/texts/update` | 更新文档内置属性 |
| POST | `/v7/docs/{file_id}/documents/tocs/delete` | 删除目录 |
| POST | `/v7/docs/{file_id}/documents/tocs/insert` | 插入目录 |
| POST | `/v7/docs/{file_id}/documents/tocs/query` | 查询目录信息 |
| POST | `/v7/docs/{file_id}/documents/tocs/update` | 更新目录 |
| POST | `/v7/docs/{file_id}/documents/watermarks/delete` | 删除水印 |
| POST | `/v7/docs/{file_id}/documents/watermarks/insert` | 插入水印 |
| POST | `/v7/docs/{file_id}/documents/watermarks/query` | 查询水印信息 |
| POST | `/v7/docs/{file_id}/paragraphs/bookmarks/insert` | 在段落插入书签 |
| POST | `/v7/docs/{file_id}/paragraphs/breaks/insert` | 插入分隔符 |
| POST | `/v7/docs/{file_id}/paragraphs/comments/insert` | 在段落添加批注 |
| POST | `/v7/docs/{file_id}/paragraphs/hyperlinks/insert` | 在段落添加超链接 |
| POST | `/v7/docs/{file_id}/paragraphs/images/insert` | 在段落插入图片 |
| POST | `/v7/docs/{file_id}/paragraphs/lists/delete` | 移除段落列表 |
| POST | `/v7/docs/{file_id}/paragraphs/lists/query` | 查询段落列表信息 |
| POST | `/v7/docs/{file_id}/paragraphs/lists/update` | 设置段落列表 |
| POST | `/v7/docs/{file_id}/paragraphs/styles/update` | 设置段落样式 |
| POST | `/v7/docs/{file_id}/paragraphs/tables/insert` | 在段落插入表格 |
| POST | `/v7/docs/{file_id}/paragraphs/texts/batch_query` | 批量查询段落信息（结构、内容、区间） |
| POST | `/v7/docs/{file_id}/paragraphs/texts/delete` | 删除段落内容 |
| POST | `/v7/docs/{file_id}/paragraphs/texts/insert` | 在段落插入文本 |
| POST | `/v7/docs/{file_id}/paragraphs/texts/query` | 查询段落信息 |
| POST | `/v7/docs/{file_id}/paragraphs/texts/update` | 更新段落内容或样式 |
| POST | `/v7/docs/{file_id}/paragraphs/tocs/insert` | 在段落插入目录 |
| POST | `/v7/docs/{file_id}/ranges/bookmarks/insert` | 在区间插入书签 |
| POST | `/v7/docs/{file_id}/ranges/breaks/insert` | 在区间插入分隔符 |
| POST | `/v7/docs/{file_id}/ranges/comments/insert` | 在区间添加批注 |
| POST | `/v7/docs/{file_id}/ranges/htmls/insert` | 在区间插入 HTML |
| POST | `/v7/docs/{file_id}/ranges/hyperlinks/insert` | 在区间添加超链接 |
| POST | `/v7/docs/{file_id}/ranges/images/insert` | 在区间插入图片 |
| POST | `/v7/docs/{file_id}/ranges/indexes/insert` | 标记索引项 |
| POST | `/v7/docs/{file_id}/ranges/lists/update` | 设置区间列表 |
| POST | `/v7/docs/{file_id}/ranges/styles/update` | 设置区间样式 |
| POST | `/v7/docs/{file_id}/ranges/tables/insert` | 在区间插入表格 |
| POST | `/v7/docs/{file_id}/ranges/texts/delete` | 删除区间内容 |
| POST | `/v7/docs/{file_id}/ranges/texts/insert` | 在区间插入文本 |
| POST | `/v7/docs/{file_id}/ranges/texts/query` | 查询区间文字内容 |
| POST | `/v7/docs/{file_id}/ranges/texts/update` | 更新区间文字内容或样式 |
| POST | `/v7/docs/{file_id}/ranges/tocs/insert` | 在区间插入目录 |
| POST | `/v7/docs/{file_id}/ranges/xmls/insert` | 在区间插入 WordML、XML |

## Slides / PPTX (52)

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v7/slides/{file_id}/masters/delete` | 删除母版 |
| POST | `/v7/slides/{file_id}/masters/properties/query` | 查询母版属性 |
| POST | `/v7/slides/{file_id}/masters/properties/update` | 更新母版属性 |
| POST | `/v7/slides/{file_id}/presentations/close` | 关闭演示文稿 |
| POST | `/v7/slides/{file_id}/presentations/properties/query` | 查询演示文稿属性 |
| POST | `/v7/slides/{file_id}/presentations/properties/update` | 更新演示文稿属性 |
| POST | `/v7/slides/{file_id}/presentations/sections/delete` | 删除分节 |
| POST | `/v7/slides/{file_id}/presentations/sections/insert` | 添加分节 |
| POST | `/v7/slides/{file_id}/presentations/sections/query` | 查询分节 |
| POST | `/v7/slides/{file_id}/presentations/sections/update` | 更新分节 |
| POST | `/v7/slides/{file_id}/presentations/tags/delete` | 删除演示文稿标签 |
| POST | `/v7/slides/{file_id}/presentations/tags/insert` | 插入演示文稿标签 |
| POST | `/v7/slides/{file_id}/presentations/tags/query` | 查询演示文稿标签 |
| POST | `/v7/slides/{file_id}/shapes/charts/insert` | 插入图表 |
| POST | `/v7/slides/{file_id}/shapes/charts/query` | 查询图表结构 |
| POST | `/v7/slides/{file_id}/shapes/charts/update` | 更新图表 |
| POST | `/v7/slides/{file_id}/shapes/items/delete` | 删除形状项 |
| POST | `/v7/slides/{file_id}/shapes/items/lines` | 插入线条形状（支持批量） |
| POST | `/v7/slides/{file_id}/shapes/items/picture` | 插入图片形状（单条） |
| POST | `/v7/slides/{file_id}/shapes/items/query` | 查询形状项 |
| POST | `/v7/slides/{file_id}/shapes/items/shapes` | 插入自选图形（支持批量） |
| POST | `/v7/slides/{file_id}/shapes/items/tables` | 插入表格形状（支持批量） |
| POST | `/v7/slides/{file_id}/shapes/items/textboxes` | 插入文本框形状（支持批量） |
| POST | `/v7/slides/{file_id}/shapes/items/update` | 更新形状项 |
| POST | `/v7/slides/{file_id}/shapes/tables/query` | 查询形状表格结构 |
| POST | `/v7/slides/{file_id}/shapes/tables/update` | 更新形状表格 |
| POST | `/v7/slides/{file_id}/shapes/tags/delete` | 删除形状标签 |
| POST | `/v7/slides/{file_id}/shapes/tags/insert` | 插入形状标签 |
| POST | `/v7/slides/{file_id}/shapes/tags/query` | 查询形状标签 |
| POST | `/v7/slides/{file_id}/shapes/texts/append` | 追加形状文本 |
| POST | `/v7/slides/{file_id}/shapes/texts/query` | 查询形状文本 |
| POST | `/v7/slides/{file_id}/shapes/texts/update` | 更新形状文本 |
| POST | `/v7/slides/{file_id}/shapes/webshapes/insert` | 插入 WebShape |
| POST | `/v7/slides/{file_id}/slides/animations/delete` | 删除动画 |
| POST | `/v7/slides/{file_id}/slides/animations/insert` | 绑定动画 |
| POST | `/v7/slides/{file_id}/slides/animations/query` | 查询动画 |
| POST | `/v7/slides/{file_id}/slides/animations/update` | 更新动画 |
| POST | `/v7/slides/{file_id}/slides/comments/delete` | 删除评论 |
| POST | `/v7/slides/{file_id}/slides/comments/insert` | 创建评论 |
| POST | `/v7/slides/{file_id}/slides/comments/query` | 查询评论 |
| POST | `/v7/slides/{file_id}/slides/comments/update` | 更新评论 |
| POST | `/v7/slides/{file_id}/slides/items/delete` | 删除幻灯片项 |
| POST | `/v7/slides/{file_id}/slides/items/insert` | 插入幻灯片项 |
| POST | `/v7/slides/{file_id}/slides/items/query` | 查询幻灯片项 |
| POST | `/v7/slides/{file_id}/slides/items/update` | 更新幻灯片项 |
| POST | `/v7/slides/{file_id}/slides/notes/append` | 追加幻灯片备注 |
| POST | `/v7/slides/{file_id}/slides/notes/insert` | 插入幻灯片备注（创建演讲者备注） |
| POST | `/v7/slides/{file_id}/slides/notes/query` | 查询幻灯片备注 |
| POST | `/v7/slides/{file_id}/slides/notes/update` | 更新幻灯片备注（替换演讲者备注） |
| POST | `/v7/slides/{file_id}/slides/tags/delete` | 删除幻灯片标签 |
| POST | `/v7/slides/{file_id}/slides/tags/insert` | 插入幻灯片标签 |
| POST | `/v7/slides/{file_id}/slides/tags/query` | 查询幻灯片标签 |

## Drive / File (41)

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v7/drives/{drive_id}/close_link` | 盘取消分享 |
| POST | `/v7/drives/{drive_id}/files/batch_copy` | 批量复制文件（夹) |
| POST | `/v7/drives/{drive_id}/files/batch_delete` | 批量删除文件(夹) |
| GET | `/v7/drives/{drive_id}/files/batch_download` | 批量文件下载 |
| POST | `/v7/drives/{drive_id}/files/batch_move` | 批量移动文件（夹) |
| POST | `/v7/drives/{drive_id}/files/{file_id}/close_link` | 关闭文件分享 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/content` | 文档内容抽取 |
| POST | `/v7/drives/{drive_id}/files/{file_id}/delete` | 删除文件 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/download` | 获取文件下载信息 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/meta` | 根据drive_id和file_id获取文件信息 |
| POST | `/v7/drives/{drive_id}/files/{file_id}/open_link` | 开启文件分享 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/path` | 获取文件路径 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/permissions` | 列举文件权限列表 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/permissions/acl` | 获取用户的文件操作权限 |
| POST | `/v7/drives/{drive_id}/files/{file_id}/permissions/batch_create` | 批量授权（单个文件) |
| POST | `/v7/drives/{drive_id}/files/{file_id}/permissions/batch_delete` | 批量移除授权（单个文件) |
| POST | `/v7/drives/{drive_id}/files/{file_id}/rename` | 重命名文件（夹） |
| POST | `/v7/drives/{drive_id}/files/{file_id}/save_as` | 文件另存为 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/sec_label` | 获取文件已设置的密级标签 |
| POST | `/v7/drives/{drive_id}/files/{file_id}/sec_label/attach` | 设置文件密级标签 |
| POST | `/v7/drives/{drive_id}/files/{file_id}/transfer_owner` | 转让文件拥有者 |
| POST | `/v7/drives/{drive_id}/files/{file_id}/update` | 修改文件元数据信息 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/versions` | 获取文件版本列表 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/versions/{version_num}/download` | 获取指定文件版本下载地址 |
| GET | `/v7/drives/{drive_id}/files/{file_id}/versions/{version_num}/meta` | 获取文件版本信息 |
| POST | `/v7/drives/{drive_id}/files/{file_id}/versions/{version_num}/update` | 更新文件版本信息 |
| POST | `/v7/drives/{drive_id}/files/{parent_id}/check_name` | 检查文件名是否已存在 |
| GET | `/v7/drives/{drive_id}/files/{parent_id}/children` | 获取子文件列表 |
| POST | `/v7/drives/{drive_id}/files/{parent_id}/commit_upload` | 提交文件上传完成 |
| POST | `/v7/drives/{drive_id}/files/{parent_id}/create` | 新建文件（夹） |
| POST | `/v7/drives/{drive_id}/files/{parent_id}/create_multipart_upload_task` | 分块上传任务初始化 |
| POST | `/v7/drives/{drive_id}/files/{parent_id}/rapid_upload` | 文件秒传 |
| POST | `/v7/drives/{drive_id}/files/{parent_id}/request_upload` | 请求文件上传信息 |
| GET | `/v7/drives/{drive_id}/meta` | 获取盘信息 |
| POST | `/v7/drives/{drive_id}/open_link` | 盘开启分享 |
| POST | `/v7/drives/{drive_id}/permissions/batch_create` | 盘批量授权 |
| POST | `/v7/drives/{drive_id}/permissions/batch_delete` | 盘批量移除授权 |
| GET | `/v7/drives/{drive_id}/roles` | 获取文档权限角色列表 |
| POST | `/v7/drives/{drive_id}/roles/create` | 新建文档权限角色 |
| POST | `/v7/drives/{drive_id}/roles/{role_id}/delete` | 删除文档权限角色 |
| POST | `/v7/drives/{drive_id}/roles/{role_id}/update` | 更新文档权限角色 |

## AirPage / 智能文档 (22)

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v7/airpage/ap_{file_id}/export_to_html/async_tasks/create` | 创建 AP 导出为 html 的异步任务 |
| POST | `/v7/airpage/ap_{file_id}/export_to_html/async_tasks/{task_id}/cancel` | 取消 AP 导出异步任务 |
| GET | `/v7/airpage/ap_{file_id}/export_to_html/async_tasks/{task_id}/query` | 查询 AP 导出异步任务状态与结果 |
| POST | `/v7/airpage/files` | 智能文档常见问题 |
| POST | `/v7/airpage/v2/{file_id}/blocks` | 查询块 |
| POST | `/v7/airpage/v2/{file_id}/blocks/batch_delete` | 批量删除块 |
| POST | `/v7/airpage/v2/{file_id}/blocks/batch_get` | 批量查询块 |
| POST | `/v7/airpage/v2/{file_id}/blocks/batch_update` | 智能文档常见问题 |
| POST | `/v7/airpage/v2/{file_id}/blocks/convert` | Markdown/HTML 转化为块 |
| POST | `/v7/airpage/v2/{file_id}/blocks/create` | 智能文档常见问题 |
| POST | `/v7/airpage/v2/{file_id}/blocks/delete` | 智能文档常见问题 |
| POST | `/v7/airpage/v2/{file_id}/blocks/update` | 智能文档常见问题 |
| GET | `/v7/airpage/{file_id}` | 获取文档基本信息 |
| POST | `/v7/airpage/{file_id}/anchor_attachment_replace` | 占位附件替换接口（音视频本地文件图片等） |
| POST | `/v7/airpage/{file_id}/export_task/query` | 智能文档常见问题 |
| POST | `/v7/airpage/{file_id}/export_to_docx` | 创建文档转DOCX任务 |
| POST | `/v7/airpage/{file_id}/export_to_html/async_tasks/create` | 创建 AP 导出为 html 的异步任务 |
| POST | `/v7/airpage/{file_id}/export_to_html/async_tasks/{task_id}/cancel` | 取消 AP 导出异步任务 |
| GET | `/v7/airpage/{file_id}/export_to_html/async_tasks/{task_id}/query` | 查询 AP 导出异步任务状态与结果 |
| POST | `/v7/airpage/{file_id}/export_to_markdown` | 创建ap转markdown任务 |
| POST | `/v7/airpage/{file_id}/export_to_markdown_zip` | 创建ap转markdown_zip任务 |
| POST | `/v7/airpage/{file_id}/export_to_pdf` | 创建文档转PDF任务 |

## Sheets / XLSX（当前 Key 401） (42)

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v7/sheets/{file_id}/file_merge` | 合并表格 |
| POST | `/v7/sheets/{file_id}/pivot_tables` | 创建数据透视表 |
| POST | `/v7/sheets/{file_id}/pivot_tables/data` | 获取数据透视表数据 |
| POST | `/v7/sheets/{file_id}/pivot_tables/delete` | 删除数据透视表 |
| POST | `/v7/sheets/{file_id}/pivot_tables/update` | 修改数据透视表 |
| POST | `/v7/sheets/{file_id}/protection_ranges` | 添加区域权限 |
| POST | `/v7/sheets/{file_id}/protection_ranges/batch_delete` | 删除区域权限 |
| POST | `/v7/sheets/{file_id}/protection_ranges/batch_update` | 修改区域权限 |
| GET | `/v7/sheets/{file_id}/users/{user_id}/regional_permission` | 查询区域权限用户权限 |
| POST | `/v7/sheets/{file_id}/worksheets` | 创建工作表 |
| POST | `/v7/sheets/{file_id}/worksheets/batch_delete` | 删除工作表 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/cf_rules` | 创建条件格式 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/cf_rules/batch_delete` | 删除条件格式 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/cf_rules/update` | 修改条件格式 |
| GET | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/chart_info` | 获取图表数据 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/charts` | 创建图表 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/charts/delete` | 删除图表 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/charts/update` | 修改图表 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/copy` | 复制工作表 |
| GET | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/data_validations` | 获取数据校验 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/data_validations/batch_delete` | 删除数据校验 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/data_validations/batch_update` | 修改数据校验 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/filters` | 开启筛选 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/filters/delete` | 关闭筛选 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/filters/update` | 更新筛选 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/float_images` | 创建浮动图片 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/float_images/delete` | 删除浮动图片 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/float_images/update` | 修改浮动图片 |
| GET | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/float_images/{float_image_id}` | 获取浮动图片 |
| GET | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/protection_ranges` | 获取区域权限设置 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/protection_ranges/update_auto_filter` | （工作表）修改区域权限自动筛选开关 |
| GET | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/range_data` | 获取单元格选区数据 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/range_data/batch_delete` | 删除单元格选区数据 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/range_data/batch_update` | 快速开始 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/range_data/find` | 查找单元格 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/range_data/text_to_columns` | 表格数据分列 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/range_sort` | 区域排序 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/range_width_height/update` | 调整行高列宽 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/rows` | 创建数据 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/rows_cols` | 插入行列 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/split_sheet` | 拆分表格 |
| POST | `/v7/sheets/{file_id}/worksheets/{worksheet_id}/update` | 更新工作表 |

## AirSheet / 智能表格（当前 Key 401） (28)

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/v7/airsheet/{file_id}/export/async_tasks/create` | 创建异步导出任务 |
| GET | `/v7/airsheet/{file_id}/export/async_tasks/{task_id}/query` | 查询异步导出任务 |
| POST | `/v7/airsheet/{file_id}/protection_ranges` | （工作表）创建区域权限信息 |
| POST | `/v7/airsheet/{file_id}/protection_ranges/batch_delete` | （工作表）删除区域权限 |
| POST | `/v7/airsheet/{file_id}/protection_ranges/batch_update` | （工作表）修改区域权限 |
| GET | `/v7/airsheet/{file_id}/worksheets` | 获取Sheet列表信息 |
| POST | `/v7/airsheet/{file_id}/worksheets/batch_delete` | 删除工作表 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/cf_rules` | 创建条件格式 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/cf_rules/batch_delete` | 删除条件格式 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/cf_rules/update` | 修改条件格式 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/copy` | 复制工作表 |
| GET | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/data_validations` | 获取数据校验 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/data_validations/batch_delete` | 删除数据校验 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/data_validations/batch_update` | 更新数据校验 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/filters` | 开启筛选 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/filters/delete` | 删除筛选 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/filters/update` | 更新筛选 |
| GET | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/float_images` | 查询浮动图片 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/float_images/delete` | 删除浮动图片 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/float_images/update` | 修改浮动图片 |
| GET | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/float_images/{float_image_id}` | 获取浮动图片 |
| GET | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/protection_ranges` | 获取区域权限列表 |
| GET | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/range_data` | 获取单元格选区数据 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/range_data/batch_delete` | 删除单元格选区数据 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/range_data/batch_update` | 快速开始 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/range_data/find` | 快速开始 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/rows` | （工作表）创建行 |
| POST | `/v7/airsheet/{file_id}/worksheets/{worksheet_id}/update` | 更新工作表 |

## DBSheet / 多维表格（当前 Key 未验证） (39)

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/v7/coop/dbsheet/{file_id}/content_permissions` | 列举自定义角色 |
| GET | `/v7/coop/dbsheet/{file_id}/content_permissions/async_tasks/dGFza19leGFtcGxlXzAwMQ/query` | 获取异步任务结果 |
| GET | `/v7/coop/dbsheet/{file_id}/content_permissions/async_tasks/{task_id}/query` | 获取异步任务结果 |
| POST | `/v7/coop/dbsheet/{file_id}/content_permissions/batch_add/async_tasks/create` | 新增自定义角色 |
| POST | `/v7/coop/dbsheet/{file_id}/content_permissions/batch_modify/async_tasks/create` | 更新自定义角色 |
| POST | `/v7/coop/dbsheet/{file_id}/content_permissions/delete/async_tasks/create` | 删除自定义角色 |
| GET | `/v7/coop/dbsheet/{file_id}/content_permissions/subjects` | 获取权限组成员列表 |
| POST | `/v7/coop/dbsheet/{file_id}/content_permissions/subjects/batch_add` | 批量添加权限组成员 |
| POST | `/v7/coop/dbsheet/{file_id}/content_permissions/subjects/batch_change` | 批量变更权限组成员所属权限组 |
| POST | `/v7/coop/dbsheet/{file_id}/hooks` | 查询全部 Hook 订阅 |
| POST | `/v7/coop/dbsheet/{file_id}/hooks/create` | 创建订阅 |
| POST | `/v7/coop/dbsheet/{file_id}/hooks/{hook_id}/delete` | 取消 Hook 订阅 |
| GET | `/v7/coop/dbsheet/{file_id}/schema` | 快速开始 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/create` | 创建数据表 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/delete` | 删除数据表 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/fields` | 创建字段 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/fields/delete` | 删除字段 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/fields/update` | 更新字段 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records` | 快速开始 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/batch_delete` | 删除记录 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/create` | 快速开始 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/list_by_page` | 按页列举记录 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/disable` | 禁用父子关系（仅对前端生效） |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/enable` | 启用父子关系（仅对前端生效） |
| GET | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/rec_parent_001/children` | 查询子记录列表 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/rec_parent_001/children/batch_bind` | 绑定记录的父子关系 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/rec_parent_001/children/batch_unbind` | 解绑记录的父子关系 |
| GET | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/status` | 查询父子关系是否禁用（仅对前端生效） |
| GET | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/{parent_id}/children` | 查询子记录列表 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/{parent_id}/children/batch_bind` | 绑定记录的父子关系 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/parents/{parent_id}/children/batch_unbind` | 解绑记录的父子关系 |
| GET | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/rec001` | 检索记录 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/search` | 检索多条记录 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/update` | 更新记录 |
| GET | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/records/{record_id}` | 检索记录 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/update` | 更新数据表 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/views` | 创建视图 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/views/{view_id}/delete` | 删除视图 |
| POST | `/v7/coop/dbsheet/{file_id}/sheets/{sheet_id}/views/{view_id}/update` | 更新视图 |

## Drive / auth notes

- `GET /v7/drives?allotee_type=user&page_size=100` — list the operator's drives.
- `GET /v7/links/{link_id}/meta` — resolve a kdocs share link to drive_id/file_id.
- Content extraction: `GET /v7/drives/{drive_id}/files/{file_id}/content?format=markdown`.
- Downloads: `GET /v7/drives/{drive_id}/files/{file_id}/download` returns a storage URL that still needs the Bearer header.

