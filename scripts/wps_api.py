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
"""
from __future__ import annotations

import argparse
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
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
        if data.get("result") != "ok":
            raise RuntimeError(f"换取 token 失败: {data}")
        self._token = data["data"]["access_token"]
        self._expires_at = time.time() + int(data["data"].get("expires_in", 43200)) - 60
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
                if raw:
                    return payload
                return json.loads(payload or b"{}")
        except urllib.error.HTTPError as exc:
            text = exc.read().decode("utf-8", "ignore")
            try:
                return json.loads(text)
            except Exception:
                return {"http_status": exc.code, "raw": text[:500]}

    def get(self, path, **kw):
        return self.request("GET", path, **kw)

    def post(self, path, body=None, **kw):
        return self.request("POST", path, body=body or {}, **kw)

    # ---------- drives / files ----------
    def list_drives(self):
        return self.get("/v7/drives", params={"allotee_type": "user", "page_size": 100})

    def list_files(self, drive_id: str, parent_id: str = "0", page_size: int = 100):
        return self.get(f"/v7/drives/{drive_id}/files/{parent_id}/children",
                        params={"page_size": page_size})

    def file_meta(self, drive_id: str, file_id: str):
        return self.get(f"/v7/drives/{drive_id}/files/{file_id}")

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
        如需立即下载（文件早已存在），传 settle=0。
        """
        time.sleep(settle)
        last = b""
        for i in range(retries):
            info = self.get(f"/v7/drives/{drive_id}/files/{file_id}/download", params={"with_hash": "true"})
            url = info.get("data", {}).get("url")
            if not url:
                time.sleep(wait)
                continue
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.token}"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            if data and data == last:
                break
            last = data
            if i < retries - 1:
                time.sleep(wait)
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


if __name__ == "__main__":
    main()
