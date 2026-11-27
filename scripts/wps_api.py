#!/usr/bin/env python3
"""WPS Agent API 最小可用客户端（仅标准库）。

认证：环境变量 WPS_AGENT_API_KEY（兼容 AGENT_API_KEY），格式 apik:<sk_id>.<secret_key>。
用法示例：
  python3 scripts/wps_api.py drives
  python3 scripts/wps_api.py ls <drive_id>
  python3 scripts/wps_api.py read <link_id_or_url>
  python3 scripts/wps_api.py create <drive_id> 我的文档.docx
  python3 scripts/wps_api.py html <file_id> assets/demo.html
  python3 scripts/wps_api.py query <file_id>
  python3 scripts/wps_api.py header <file_id> "公司内部资料"
  python3 scripts/wps_api.py page-number <file_id>
  python3 scripts/wps_api.py comment <file_id> 1 "批注内容"
  python3 scripts/wps_api.py download <drive_id> <file_id> out.docx
  python3 scripts/wps_api.py slides <file_id>
  python3 scripts/wps_api.py shapes <file_id> <slide_id>
  python3 scripts/wps_api.py add-textbox <file_id> <slide_id> "标题"
  python3 scripts/wps_api.py add-table <file_id> <slide_id> --rows 3 --cols 3
  python3 scripts/wps_api.py set-cell <file_id> <slide_id> <shape_id> 1 1 "指标"
  python3 scripts/wps_api.py add-note <file_id> <slide_id> "演讲者备注"
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN_URL = "https://account.wps.cn/api/authorization/agent/v1/token"
OPENAPI = "https://openapi.wps.cn"   # 云盘/文件/内容抽取
DOCS_API = "https://api.wps.cn"      # Writer(DOCX)/Slides(PPTX) 对象模型


def _error_message(payload: dict) -> str:
    """Pick a human-readable message; never treat a successful `result` as an error."""
    for key in ("msg", "message", "errmsg"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    result = payload.get("result")
    if isinstance(result, str) and result.strip().lower() not in ("", "ok"):
        return result.strip()
    return "no error detail returned"


class WPSAPIError(RuntimeError):
    """HTTP or JSON-level error returned by the WPS API."""

    def __init__(self, payload, http_status: int | None = None, context: str | None = None):
        if not isinstance(payload, dict):
            payload = {"msg": str(payload)}
        self.payload = payload
        self.http_status = http_status
        self.context = context
        self.code = payload.get("code")
        self.errno = payload.get("errno")
        self.msg = _error_message(payload)
        self.retryable = http_status == 429 or (http_status is not None and 500 <= http_status < 600)
        parts = []
        if context:
            parts.append(context)
        if http_status is not None:
            parts.append(f"HTTP {http_status}")
        if self.code is not None:
            parts.append(f"code={self.code}")
        if self.errno is not None:
            parts.append(f"errno={self.errno}")
        parts.append(f"msg={self.msg}")
        reason = payload.get("reason")
        if reason:
            parts.append(f"reason={reason}")
        if self.retryable:
            parts.append("retryable=true")
        super().__init__("; ".join(parts))


def _is_api_error(payload) -> bool:
    if not isinstance(payload, dict):
        return False
    if payload.get("code") not in (None, 0, "0"):
        return True
    if payload.get("errno") not in (None, 0, "0"):
        return True
    result = payload.get("result")
    return isinstance(result, str) and result.lower() in {"permissiondenied", "fail", "error"}


class WPSClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = (api_key or os.environ.get("WPS_AGENT_API_KEY")
                        or os.environ.get("AGENT_API_KEY") or "").strip()
        if not self.api_key:
            raise SystemExit("未找到 WPS_AGENT_API_KEY / AGENT_API_KEY 环境变量")
        self._token: str | None = None
        self._expires_at = 0.0

    # ---------- auth ----------
    @property
    def token(self) -> str:
        if self._token and time.time() < self._expires_at:
            return self._token
        body = json.dumps({"grant_type": "api_key", "api_key": self.api_key}).encode()
        req = urllib.request.Request(TOKEN_URL, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as exc:
            text = exc.read().decode("utf-8", "ignore")
            try:
                payload = json.loads(text)
            except Exception:
                payload = {"msg": text[:500]}
            raise WPSAPIError(payload, http_status=exc.code,
                              context="POST /api/authorization/agent/v1/token") from None
        token = (data.get("data") or {}).get("access_token")
        if data.get("result") != "ok" or not token:
            raise WPSAPIError(data, context="POST /api/authorization/agent/v1/token")
        self._token = token
        self._expires_at = time.time() + int((data.get("data") or {}).get("expires_in", 43200)) - 60
        return self._token

    # ---------- generic ----------
    def request(self, method: str, path: str, *, body=None, params=None,
                host: str = OPENAPI, raw: bool = False):
        url = host + path
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        headers = {"Authorization": f"Bearer {self.token}"}
        data = None
        if body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                payload = resp.read()
        except urllib.error.HTTPError as exc:
            text = exc.read().decode("utf-8", "ignore")
            try:
                error = json.loads(text)
            except Exception:
                error = {"msg": text[:500]}
            raise WPSAPIError(error, http_status=exc.code, context=f"{method} {path}") from None
        if raw:
            return payload
        result = json.loads(payload or b"{}")
        if _is_api_error(result):
            raise WPSAPIError(result, context=f"{method} {path}")
        return result

    def get(self, path, **kw):
        return self.request("GET", path, **kw)

    def post(self, path, body=None, **kw):
        return self.request("POST", path, body=body or {}, **kw)

    # ---------- drives / files ----------
    def _paged_items(self, path: str, *, params=None, page_size: int = 100,
                     context: str | None = None):
        """Fetch every page of a list endpoint and merge `data.items`."""
        page_size = max(1, min(int(page_size), 500))
        base = dict(params or {})
        base.pop("page_token", None)
        items: list = []
        token = ""
        seen = set()
        result = {}
        while True:
            query = dict(base, page_size=page_size)
            if token:
                query["page_token"] = token
            result = self.get(path, params=query)
            data = result.get("data") or {}
            items.extend(data.get("items") or [])
            token = data.get("next_page_token") or ""
            if not token:
                break
            if token in seen:
                raise WPSAPIError({"result": "fail", "msg": "pagination token repeated"},
                                  context=context or path)
            seen.add(token)
        result.setdefault("data", {})["items"] = items
        result["data"].pop("next_page_token", None)
        return result

    def list_drives(self, page_size: int = 100):
        """列出全部云盘；自动跟随 next_page_token。"""
        return self._paged_items("/v7/drives", params={"allotee_type": "user"},
                                 page_size=page_size, context="list_drives")

    def list_files(self, drive_id: str, parent_id: str = "0", page_size: int = 100):
        """列出目录下全部文件；自动跟随 next_page_token。"""
        return self._paged_items(f"/v7/drives/{drive_id}/files/{parent_id}/children",
                                 page_size=page_size, context="list_files")

    def file_meta(self, drive_id: str, file_id: str):
        return self.get(f"/v7/drives/{drive_id}/files/{file_id}/meta")

    def link_meta(self, link_id: str):
        return self.get(f"/v7/links/{link_id}/meta")

    def read_content(self, drive_id: str, file_id: str, fmt: str = "markdown"):
        """内容抽取：源格式 -> markdown/plain，适合阅读，不适合保留复杂版式。"""
        return self.get(f"/v7/drives/{drive_id}/files/{file_id}/content", params={"format": fmt})

    def create_file(self, drive_id: str, parent_id: str, name: str, on_conflict: str = "rename"):
        return self.post(f"/v7/drives/{drive_id}/files/{parent_id}/create",
                         {"file_type": "file", "name": name, "on_name_conflict": on_conflict})

    def delete_file(self, drive_id: str, file_id: str):
        return self.post(f"/v7/drives/{drive_id}/files/{file_id}/delete", {})

    def download(self, drive_id: str, file_id: str, out_path: str,
                 settle: float = 10.0, retries: int = 6, wait: float = 3.0):
        """下载源格式。

        写入后 WPS 侧导出有 10~30 秒延迟。先 settle 秒，再连续两次拿到相同内容才返回；
        如需立即下载（文件早已存在），传 settle=0。空内容或 SHA-1 不匹配时抛错。
        """
        time.sleep(settle)
        last = b""
        info = {}
        for i in range(retries):
            info = self.get(f"/v7/drives/{drive_id}/files/{file_id}/download",
                            params={"with_hash": "true"})
            url = (info.get("data") or {}).get("url")
            if not url:
                time.sleep(wait)
                continue
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"})
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = resp.read()
            except urllib.error.HTTPError as exc:
                raise WPSAPIError({"msg": "download storage request failed"},
                                  http_status=exc.code, context="download storage") from None
            if data and data == last:
                break
            last = data
            if i < retries - 1:
                time.sleep(wait)
        if not last:
            detail = info.get("msg") or f"code={info.get('code')}"
            raise RuntimeError(f"下载失败：未拿到文件内容（{detail}）")
        for item in (info.get("data") or {}).get("hashes") or []:
            if item.get("type") == "sha1" and item.get("sum"):
                actual = hashlib.sha1(last).hexdigest()
                if actual != item["sum"]:
                    raise RuntimeError(f"下载校验失败：sha1 {actual} != {item['sum']}")
        with open(out_path, "wb") as fh:
            fh.write(last)
        return out_path, len(last)

    # ---------- Writer / DOCX ----------
    def doc_query_text(self, file_id: str, properties=None):
        return self.post(f"/v7/docs/{file_id}/documents/texts/query",
                         {"properties": properties or ["TEXT_CONTENT"]}, host=DOCS_API)

    def doc_insert_text(self, file_id: str, text: str, *, heading_level: int | None = None,
                        is_br: bool = True, font: dict | None = None, para: dict | None = None):
        body = {
            "properties": ["TEXT_HEADING" if heading_level else "TEXT_CONTENT"],
            "text": text,
            "is_br": is_br,
        }
        if heading_level:
            body["heading_level"] = heading_level
        if font:
            body["font_style"] = font
        if para:
            body["paragraph_format"] = para
        return self.post(f"/v7/docs/{file_id}/documents/texts/insert", body, host=DOCS_API)

    def doc_delete_text(self, file_id: str):
        return self.post(f"/v7/docs/{file_id}/documents/texts/delete",
                         {"properties": ["TEXT_CONTENT"]}, host=DOCS_API)

    def doc_replace(self, file_id: str, find_text: str, replace_text: str, is_all: bool = True):
        return self.post(f"/v7/docs/{file_id}/documents/texts/replace",
                         {"properties": ["TEXT_CONTENT"], "find_text": find_text,
                          "replace_text": replace_text, "is_all": is_all}, host=DOCS_API)

    def doc_insert_html(self, file_id: str, html: str, begin: int = 0, end: int = 0):
        """把 HTML 片段插入区间；复杂表格/排版优先用这个，而不是 TABLE_FULL。"""
        return self.post(f"/v7/docs/{file_id}/ranges/htmls/insert",
                         {"properties": ["HTML_DATA"], "range": {"begin": begin, "end": end},
                          "html": html}, host=DOCS_API)

    def doc_insert_table(self, file_id: str, caption: str, headers: list[str], rows: list[list[str]]):
        """TABLE_FULL：一次生成表题+表头+数据。注意列宽默认为 0，复杂表格建议用 HTML。"""
        return self.post(f"/v7/docs/{file_id}/documents/tables/insert",
                         {"properties": ["TABLE_FULL"], "rows": len(rows) + 1, "cols": len(headers),
                          "full_data": {"caption": caption, "headers": headers,
                                        "rows": [{"cells": r} for r in rows],
                                        "enable_borders": True}}, host=DOCS_API)

    def doc_set_header(self, file_id: str, text: str, section_index: int = 1):
        return self.post(f"/v7/docs/{file_id}/documents/header_footers/update",
                         {"properties": ["HEADER_FOOTER_HEADER_CONTENT"],
                          "section_index": section_index, "content": text}, host=DOCS_API)

    def doc_add_page_number(self, file_id: str, section_index: int = 1):
        return self.post(f"/v7/docs/{file_id}/documents/header_footers/update",
                         {"properties": ["HEADER_FOOTER_FOOTER_PAGE_NUMBER"],
                          "section_index": section_index, "enabled": True}, host=DOCS_API)

    def doc_add_comment(self, file_id: str, paragraph_index: int, text: str):
        return self.post(f"/v7/docs/{file_id}/paragraphs/comments/insert",
                         {"properties": ["COMMENT_DATA"], "paragraph_index": paragraph_index,
                          "text": text}, host=DOCS_API)

    # ---------- Slides / PPTX ----------
    # In practice Slides live on api.wps.cn. openapi.wps.cn rejects /v7/slides
    # with 401 "unable to parse claims", despite the official docs' host.
    def ppt_slides(self, file_id: str, properties=("LIST",)):
        return self.post(f"/v7/slides/{file_id}/slides/items/query",
                         {"properties": list(properties)}, host=DOCS_API)

    def ppt_slide_insert(self, file_id: str, index: int | None = None, layout: int = 12):
        item = {"layout": layout}
        if index is not None:
            item["index"] = index
        return self.post(f"/v7/slides/{file_id}/slides/items/insert",
                         {"insert_mode": "BATCH", "items": [item]}, host=DOCS_API)

    def ppt_shapes(self, file_id: str, slide_id: int):
        return self.post(f"/v7/slides/{file_id}/shapes/items/query",
                         {"target": {"slide_id": slide_id}, "properties": ["LIST"]},
                         host=DOCS_API)

    def ppt_shape_text(self, file_id: str, slide_id: int, shape_id: int,
                       properties=("TEXT_CONTENT",)):
        return self.post(f"/v7/slides/{file_id}/shapes/texts/query",
                         {"target": {"slide_id": slide_id, "shape_id": shape_id},
                          "properties": list(properties)}, host=DOCS_API)

    def ppt_set_text(self, file_id: str, slide_id: int, shape_id: int, text: str,
                     font: dict | None = None):
        """替换形状文本；可同时设 font。paragraph.alignment 目前会被引擎拒绝。"""
        props = ["TEXT_CONTENT", "FONT"] if font else ["TEXT_CONTENT"]
        body = {"target": {"slide_id": slide_id, "shape_id": shape_id},
                "properties": props, "text": text}
        if font:
            body["font"] = font
        return self.post(f"/v7/slides/{file_id}/shapes/texts/update", body, host=DOCS_API)

    def ppt_replace_text(self, file_id: str, slide_id: int, shape_id: int,
                         find_what: str, replace_what: str, match_case: bool = False):
        return self.post(f"/v7/slides/{file_id}/shapes/texts/update",
                         {"target": {"slide_id": slide_id, "shape_id": shape_id},
                          "properties": ["TEXT_REPLACE"], "find_what": find_what,
                          "replace_what": replace_what, "match_case": match_case},
                         host=DOCS_API)

    def ppt_add_textbox(self, file_id: str, slide_id: int, text: str, *,
                        left: float = 100, top: float = 100,
                        width: float = 600, height: float = 60):
        return self.post(f"/v7/slides/{file_id}/shapes/items/textboxes",
                         {"slide_id": slide_id,
                          "textboxes": [{"left": left, "top": top, "width": width,
                                         "height": height, "text": text}]},
                         host=DOCS_API)

    def ppt_add_table(self, file_id: str, slide_id: int, rows: int = 3, columns: int = 3,
                      left: float = 80, top: float = 140):
        return self.post(f"/v7/slides/{file_id}/shapes/items/tables",
                         {"slide_id": slide_id,
                          "tables": [{"rows": rows, "columns": columns,
                                      "left": left, "top": top}]}, host=DOCS_API)

    def ppt_table_cells(self, file_id: str, slide_id: int, shape_id: int):
        return self.post(f"/v7/slides/{file_id}/shapes/tables/query",
                         {"target": {"slide_id": slide_id, "shape_id": shape_id},
                          "properties": ["CELLS"]}, host=DOCS_API)

    def ppt_set_cell(self, file_id: str, slide_id: int, shape_id: int,
                     row: int, column: int, text: str):
        return self.post(f"/v7/slides/{file_id}/shapes/tables/update",
                         {"target": {"slide_id": slide_id, "shape_id": shape_id},
                          "properties": ["CELL_TEXT"], "row": row, "column": column,
                          "text": text}, host=DOCS_API)

    def ppt_notes(self, file_id: str, slide_id: int):
        return self.post(f"/v7/slides/{file_id}/slides/notes/query",
                         {"target": {"slide_id": slide_id}}, host=DOCS_API)

    def ppt_add_note(self, file_id: str, slide_id: int, text: str):
        return self.post(f"/v7/slides/{file_id}/slides/notes/insert",
                         {"target": {"slide_id": slide_id}, "text": text}, host=DOCS_API)

    def ppt_set_geometry(self, file_id: str, slide_id: int, shape_id: int, *,
                         left: float, top: float, width: float, height: float):
        return self.post(f"/v7/slides/{file_id}/shapes/items/update",
                         {"target": {"slide_id": slide_id, "shape_id": shape_id},
                          "properties": ["GEOMETRY"], "left": left, "top": top,
                          "width": width, "height": height}, host=DOCS_API)


# ---------- helpers ----------
def extract_link_id(value: str) -> str:
    m = re.search(r"/(?:l|link)/([A-Za-z0-9]+)", value)
    return m.group(1) if m else value.strip()


def resolve_link(client: WPSClient, value: str) -> tuple[str, str]:
    meta = client.link_meta(extract_link_id(value))
    data = meta.get("data") or {}
    if not data.get("drive_id"):
        raise SystemExit(f"解析链接失败: {meta}")
    return data["drive_id"], data["file_id"]


def main():
    p = argparse.ArgumentParser(description="WPS Agent API 客户端")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("drives")

    ls = sub.add_parser("ls")
    ls.add_argument("drive_id")
    ls.add_argument("--parent", default="0")

    rd = sub.add_parser("read")
    rd.add_argument("link_or_id")

    cr = sub.add_parser("create")
    cr.add_argument("drive_id")
    cr.add_argument("name")

    q = sub.add_parser("query")
    q.add_argument("file_id")

    dl = sub.add_parser("download")
    dl.add_argument("drive_id")
    dl.add_argument("file_id")
    dl.add_argument("out")

    ht = sub.add_parser("html")
    ht.add_argument("file_id")
    ht.add_argument("html_file")

    hd = sub.add_parser("header")
    hd.add_argument("file_id")
    hd.add_argument("text")
    hd.add_argument("--section", type=int, default=1)

    pn = sub.add_parser("page-number")
    pn.add_argument("file_id")
    pn.add_argument("--section", type=int, default=1)

    cm = sub.add_parser("comment")
    cm.add_argument("file_id")
    cm.add_argument("paragraph_index", type=int)
    cm.add_argument("text")

    sl = sub.add_parser("slides")
    sl.add_argument("file_id")
    sl.add_argument("--count", action="store_true")

    sh = sub.add_parser("shapes")
    sh.add_argument("file_id")
    sh.add_argument("slide_id", type=int)

    st = sub.add_parser("shape-text")
    st.add_argument("file_id")
    st.add_argument("slide_id", type=int)
    st.add_argument("shape_id", type=int)

    sx = sub.add_parser("set-text")
    sx.add_argument("file_id")
    sx.add_argument("slide_id", type=int)
    sx.add_argument("shape_id", type=int)
    sx.add_argument("text")
    sx.add_argument("--font-name")
    sx.add_argument("--font-size", type=float)
    sx.add_argument("--bold", action="store_true")
    sx.add_argument("--color")

    sr = sub.add_parser("replace-text")
    sr.add_argument("file_id")
    sr.add_argument("slide_id", type=int)
    sr.add_argument("shape_id", type=int)
    sr.add_argument("find_what")
    sr.add_argument("replace_what")

    tb = sub.add_parser("add-textbox")
    tb.add_argument("file_id")
    tb.add_argument("slide_id", type=int)
    tb.add_argument("text")
    tb.add_argument("--left", type=float, default=100)
    tb.add_argument("--top", type=float, default=100)
    tb.add_argument("--width", type=float, default=600)
    tb.add_argument("--height", type=float, default=60)

    asl = sub.add_parser("add-slide")
    asl.add_argument("file_id")
    asl.add_argument("--index", type=int)
    asl.add_argument("--layout", type=int, default=12)

    at = sub.add_parser("add-table")
    at.add_argument("file_id")
    at.add_argument("slide_id", type=int)
    at.add_argument("--rows", type=int, default=3)
    at.add_argument("--cols", type=int, default=3)
    at.add_argument("--left", type=float, default=80)
    at.add_argument("--top", type=float, default=140)

    tc = sub.add_parser("table-cells")
    tc.add_argument("file_id")
    tc.add_argument("slide_id", type=int)
    tc.add_argument("shape_id", type=int)

    sc = sub.add_parser("set-cell")
    sc.add_argument("file_id")
    sc.add_argument("slide_id", type=int)
    sc.add_argument("shape_id", type=int)
    sc.add_argument("row", type=int)
    sc.add_argument("column", type=int)
    sc.add_argument("text")

    nt = sub.add_parser("notes")
    nt.add_argument("file_id")
    nt.add_argument("slide_id", type=int)

    an = sub.add_parser("add-note")
    an.add_argument("file_id")
    an.add_argument("slide_id", type=int)
    an.add_argument("text")

    args = p.parse_args()
    c = WPSClient()

    if args.cmd == "drives":
        print(json.dumps(c.list_drives(), ensure_ascii=False, indent=2))
    elif args.cmd == "ls":
        d = c.list_files(args.drive_id, args.parent)
        for it in d.get("data", {}).get("items", []):
            print(f"{it.get('type',''):6} {it.get('id',''):34} {it.get('name','')}")
    elif args.cmd == "read":
        drive, fid = resolve_link(c, args.link_or_id)
        d = c.read_content(drive, fid)
        print(d.get("data", {}).get("markdown") or d.get("data", {}).get("plain") or json.dumps(d, ensure_ascii=False))
    elif args.cmd == "create":
        print(json.dumps(c.create_file(args.drive_id, "0", args.name), ensure_ascii=False, indent=2))
    elif args.cmd == "query":
        print(json.dumps(c.doc_query_text(args.file_id), ensure_ascii=False, indent=2))
    elif args.cmd == "download":
        print(c.download(args.drive_id, args.file_id, args.out))
    elif args.cmd == "html":
        html = open(args.html_file, encoding="utf-8").read()
        print(json.dumps(c.doc_insert_html(args.file_id, html), ensure_ascii=False, indent=2))
    elif args.cmd == "header":
        print(json.dumps(c.doc_set_header(args.file_id, args.text, args.section), ensure_ascii=False, indent=2))
    elif args.cmd == "page-number":
        print(json.dumps(c.doc_add_page_number(args.file_id, args.section), ensure_ascii=False, indent=2))
    elif args.cmd == "comment":
        print(json.dumps(c.doc_add_comment(args.file_id, args.paragraph_index, args.text), ensure_ascii=False, indent=2))

    elif args.cmd == "slides":
        d = c.ppt_slides(args.file_id)
        slides = (d.get("data") or {}).get("list_data", {}).get("slides", [])
        if args.count:
            print(len(slides))
        else:
            for s in slides:
                print(f"{s.get('slide_index'):>3}  {s.get('slide_id'):>12}  "
                      f"layout={s.get('layout')}  {s.get('name')}")
    elif args.cmd == "shapes":
        d = c.ppt_shapes(args.file_id, args.slide_id)
        for s in (d.get("data") or {}).get("list_data", {}).get("shapes", []):
            print(f"{s.get('shape_id'):>5}  type={s.get('type'):<3} {s.get('name', '')}  "
                  f"({s.get('left')}, {s.get('top')}, {s.get('width')}, {s.get('height')})")
    elif args.cmd == "shape-text":
        d = c.ppt_shape_text(args.file_id, args.slide_id, args.shape_id)
        print((d.get("data") or {}).get("data", {}).get("text", ""))
    elif args.cmd == "set-text":
        font = None
        if args.font_name or args.font_size or args.bold or args.color:
            font = {}
            if args.font_name:
                font["name"] = args.font_name
            if args.font_size:
                font["size"] = args.font_size
            if args.bold:
                font["bold"] = True
            if args.color:
                font["color"] = args.color
        print(json.dumps(c.ppt_set_text(args.file_id, args.slide_id, args.shape_id,
                                        args.text, font), ensure_ascii=False, indent=2))
    elif args.cmd == "replace-text":
        print(json.dumps(c.ppt_replace_text(args.file_id, args.slide_id, args.shape_id,
                                            args.find_what, args.replace_what),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "add-textbox":
        print(json.dumps(c.ppt_add_textbox(args.file_id, args.slide_id, args.text,
                                           left=args.left, top=args.top,
                                           width=args.width, height=args.height),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "add-slide":
        print(json.dumps(c.ppt_slide_insert(args.file_id, args.index, args.layout),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "add-table":
        print(json.dumps(c.ppt_add_table(args.file_id, args.slide_id, args.rows,
                                         args.cols, args.left, args.top),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "table-cells":
        d = c.ppt_table_cells(args.file_id, args.slide_id, args.shape_id)
        for cell in (d.get("data") or {}).get("data", {}).get("cells", []):
            print(f"{cell.get('row')},{cell.get('column')}: {cell.get('text', '')}")
    elif args.cmd == "set-cell":
        print(json.dumps(c.ppt_set_cell(args.file_id, args.slide_id, args.shape_id,
                                        args.row, args.column, args.text),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "notes":
        d = c.ppt_notes(args.file_id, args.slide_id)
        data = (d.get("data") or {}).get("data") or d.get("data") or {}
        print(data.get("notes_text", ""))
    elif args.cmd == "add-note":
        print(json.dumps(c.ppt_add_note(args.file_id, args.slide_id, args.text),
                         ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        main()
    except WPSAPIError as exc:
        print(f"WPS API 错误: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
    except (RuntimeError, urllib.error.URLError, OSError, ValueError) as exc:
        print(f"错误: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
