#!/usr/bin/env python3
"""doc_audit.py — 审计文档工作区（文档即记忆）。

因为全是 Markdown，所以它天然可审计——这是召回式记忆（向量库）做不到的。

用法:
    python3 doc_audit.py <项目根目录> [--dir docs] [--stale-days 90] [--fail-on-issue] [--json]

报告三类问题:
    断链     —— 文档里指向了不存在的文件（含 INDEX.md）
    孤儿     —— 项目里的 .md 没被 INDEX.md 收录（写了但没人知道它存在）
    过期     —— 超过 --stale-days 天没更新

退出码:
    0 无问题，或有问题但未指定 --fail-on-issue
    1 有问题且指定了 --fail-on-issue（可进 CI）
    2 参数错误 / 找不到文档目录
"""

import argparse
import json
import os
import re
import sys
import time

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# 围栏代码块（``` 或 ~~~）：里面的"链接"是示例，不参与断链检查
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?^[ \t]*\1[ \t]*$", re.M | re.S)
# 行内代码 `...`：同理，是示例
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next", "target"}
STATUS_RE = re.compile(r"状态\s*[:：]\s*([^\s｜|]+)")


def plain_text(text):
    """去掉围栏代码块与行内代码，避免把文档里的示例链接当成真链接。"""
    return INLINE_CODE_RE.sub(" ", FENCE_RE.sub("\n", text))


def find_docdir(root, explicit):
    if explicit:
        d = os.path.join(root, explicit)
        return d if os.path.isdir(d) else None
    for name in ("docs", "doc", "documentation"):
        d = os.path.join(root, name)
        if os.path.isdir(d):
            return d
    return None


def iter_markdown(docdir):
    for cur, dirs, files in os.walk(docdir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if fn.lower().endswith(".md"):
                yield os.path.join(cur, fn)


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def norm(p):
    return os.path.normpath(p)


def main():
    ap = argparse.ArgumentParser(description="审计文档工作区")
    ap.add_argument("project", help="项目根目录")
    ap.add_argument("--dir", default=None, help="文档目录名（默认自动探测 docs/doc/documentation）")
    ap.add_argument("--stale-days", type=int, default=90, help="过期阈值天数（默认 90）")
    ap.add_argument("--fail-on-issue", action="store_true", help="有问题时以非零码退出")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    root = os.path.abspath(args.project)
    if not os.path.isdir(root):
        print(f"[错误] 项目目录不存在: {root}", file=sys.stderr)
        return 2

    docdir = find_docdir(root, args.dir)
    if not docdir:
        print(f"[错误] 未找到文档目录（试过 docs/ doc/ documentation/）: {root}", file=sys.stderr)
        print("       先用 scripts/init_doc_brain.py 建骨架，或用 --dir 指定。", file=sys.stderr)
        return 2

    index_path = os.path.join(docdir, "INDEX.md")
    all_md = [p for p in iter_markdown(docdir)]
    index_md = index_path if os.path.isfile(index_path) else None

    # ---------- 断链：扫描所有 md 里的相对链接 ----------
    broken = []
    for md in all_md:
        base = os.path.dirname(md)
        text = plain_text(read(md))
        for target in LINK_RE.findall(text):
            t = target.split("#", 1)[0].strip()
            if not t:
                continue
            if t.startswith(("http://", "https://", "mailto:", "tel:", "#", "//")):
                continue
            if not t.lower().endswith(".md"):
                continue
            resolved = norm(os.path.join(base, t))
            if not os.path.exists(resolved):
                broken.append({
                    "from": os.path.relpath(md, root),
                    "target": t,
                    "is_index": md == index_md,
                })

    # ---------- 孤儿：未被 INDEX.md 收录的 md ----------
    indexed = set()
    if index_md:
        base = os.path.dirname(index_md)
        for target in LINK_RE.findall(plain_text(read(index_md))):
            t = target.split("#", 1)[0].strip()
            if t.lower().endswith(".md") and not t.startswith(("http://", "https://")):
                indexed.add(norm(os.path.join(base, t)))

    orphans = []
    for md in all_md:
        if index_md and md == index_md:
            continue
        if norm(md) not in indexed:
            orphans.append(md)

    # ---------- 过期 ----------
    now = time.time()
    cutoff = now - args.stale_days * 86400
    stale = []
    for md in all_md:
        try:
            mtime = os.path.getmtime(md)
        except OSError:
            continue
        if mtime < cutoff:
            text = read(md)
            m = STATUS_RE.search(text)
            stale.append({
                "path": md,
                "days": int((now - mtime) // 86400),
                "status": m.group(1) if m else "",
            })
    stale.sort(key=lambda x: -x["days"])

    # ---------- 输出 ----------
    n_index = len(indexed)
    n_actual = len([p for p in all_md if not (index_md and p == index_md)])
    issues = len(broken) + len(orphans) + len(stale)

    if args.json:
        print(json.dumps({
            "root": root,
            "docdir": docdir,
            "index": index_md,
            "indexed": n_index,
            "actual": n_actual,
            "stale_days": args.stale_days,
            "broken": broken,
            "orphans": [os.path.relpath(p, root) for p in orphans],
            "stale": [{"path": os.path.relpath(s["path"], root), "days": s["days"], "status": s["status"]} for s in stale],
            "issue_count": issues,
        }, ensure_ascii=False, indent=2))
        return 1 if (issues and args.fail_on_issue) else 0

    print(f"文档工作区审计 — {root}")
    idx_rel = os.path.relpath(index_md, root) if index_md else "（缺失！）"
    print(f"索引: {idx_rel} ｜ 收录 {n_index} 篇 ｜ 实际 {n_actual} 篇 ｜ 阈值: {args.stale_days} 天")
    if not index_md:
        print("  ⚠ 没有 INDEX.md —— 没有索引的文档工作区等于没有入口，agent 查不到任何东西。")
    print()

    if broken:
        print(f"[断链] {len(broken)} 处")
        for b in broken:
            flag = " (INDEX!)" if b["is_index"] else ""
            print(f"  {b['from']}  →  {b['target']}（文件不存在）{flag}")
        print()

    if orphans:
        print(f"[孤儿] {len(orphans)} 篇（写了但没登记进 INDEX.md，等于没写）")
        for p in orphans:
            rel = os.path.relpath(p, root)
            days = int((now - os.path.getmtime(p)) // 86400)
            print(f"  {rel}   (未收录, {days} 天前更新)")
        print()

    if stale:
        print(f"[过期] {len(stale)} 篇（超过 {args.stale_days} 天未更新）")
        for s in stale:
            rel = os.path.relpath(s["path"], root)
            st = f", 状态={s['status']}" if s["status"] else ""
            print(f"  {rel}  {s['days']} 天未更新{st}")
        print()

    if issues == 0:
        print("汇总: 无问题 ✅  索引可信，没有孤儿，没有断链，没有过期文档。")
    else:
        print(f"汇总: 断链 {len(broken)} ｜ 孤儿 {len(orphans)} ｜ 过期 {len(stale)}")
        print()
        print("处理原则:")
        print("  · 断链 → 立即修（它会让 agent 得到「没有这方面的知识」的错误结论）")
        print("  · 孤儿 → 登记进索引，或删掉/标废弃")
        print("  · 过期 → 三选一：改对 / 标『过期』/ 标『已废弃』并写明被谁取代")

    return 1 if (issues and args.fail_on_issue) else 0


if __name__ == "__main__":
    sys.exit(main())
