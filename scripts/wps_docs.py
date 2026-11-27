#!/usr/bin/env python3
"""Read the official WPS Open Platform docs through their JSON API.

No API key is needed: these are public developer docs.
Examples:
  python3 scripts/wps_docs.py search 页眉
  python3 scripts/wps_docs.py get 6332
  python3 scripts/wps_docs.py sync /tmp/wps-docs
"""
from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://open.wps.cn"
COLLECTION = "wps365"


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "wps-agent-api-skill/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def tree(lang: str):
    url = f"{BASE}/docs/api/collections/{COLLECTION}?lang={urllib.parse.quote(lang)}"
    return get_json(url)["data"]["items"]


def flatten(items, out=None):
    out = out if out is not None else []
    for it in items:
        if it.get("type") == "file" and it.get("docInfo"):
            info = it["docInfo"]
            out.append({
                "id": str(info.get("id")),
                "title": it.get("displayName") or it.get("name"),
                "path": it.get("path", ""),
                "source": info.get("fileSource") or it.get("source") or "dms",
            })
        flatten(it.get("children", []), out)
    return out


def doc_markdown(doc, lang: str):
    url = (f"{BASE}/docs/api/doc/{doc['id']}?lang={urllib.parse.quote(lang)}"
           f"&source={urllib.parse.quote(doc['source'])}")
    data = get_json(url).get("data") or {}
    return data.get("content", "")


def cmd_search(args):
    docs = flatten(tree(args.lang))
    q = args.keyword.lower()
    hits = [d for d in docs if q in d["title"].lower() or q in d["path"].lower()]
    for d in hits[:args.limit]:
        print(f"{d['id']:>6}  {d['title']}  ({d['path']})")
    print(f"-- {len(hits)} hit(s), showing {min(len(hits), args.limit)}")


def resolve(docs, key):
    key = key.strip()
    if key.isdigit():
        for d in docs:
            if d["id"] == key:
                return d
        return {"id": key, "title": f"doc-{key}", "path": "", "source": "dms"}
    exact = [d for d in docs if d["title"] == key]
    if exact:
        return exact[0]
    hits = [d for d in docs if key.lower() in d["title"].lower()]
    if not hits:
        raise SystemExit(f"未找到文档: {key}")
    return hits[0]


def cmd_get(args):
    docs = flatten(tree(args.lang))
    d = resolve(docs, args.key)
    print(doc_markdown(d, args.lang))


def cmd_sync(args):
    docs = flatten(tree(args.lang))
    os.makedirs(args.out, exist_ok=True)

    def fetch(d):
        try:
            text = doc_markdown(d, args.lang)
            name = d["path"].strip("/").replace("/", "__") or d["id"]
            path = os.path.join(args.out, name + ".md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            return d, name + ".md", len(text)
        except Exception as exc:  # keep going; report at the end
            return d, None, str(exc)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(fetch, docs))

    index = [{"id": d["id"], "title": d["title"], "path": d["path"],
              "file": f, "bytes": n} for d, f, n in results if f]
    with open(os.path.join(args.out, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)
    failed = [r for r in results if not r[1]]
    print(f"synced {len(index)} docs -> {args.out}")
    for d, _, err in failed[:10]:
        print(f"FAILED {d['title']}: {err}")


def main():
    p = argparse.ArgumentParser(description="WPS 开放平台官方文档读取器")
    p.add_argument("--lang", default="zh-CN")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="按标题/路径搜索文档")
    s.add_argument("keyword")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_search)

    g = sub.add_parser("get", help="按 doc id 或标题输出 Markdown")
    g.add_argument("key")
    g.set_defaults(func=cmd_get)

    y = sub.add_parser("sync", help="把整套文档同步到本地目录")
    y.add_argument("out")
    y.add_argument("--workers", type=int, default=6)
    y.set_defaults(func=cmd_sync)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
