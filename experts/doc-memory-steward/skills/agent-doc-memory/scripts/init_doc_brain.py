#!/usr/bin/env python3
"""init_doc_brain.py — 在项目里搭一个文档工作区（文档即记忆）。

用法:
    python3 init_doc_brain.py <项目根目录> [--dir docs] [--dry-run]

行为:
    - 默认在 <项目根目录>/docs 下建六类文档骨架
    - **已存在的文件一律不覆盖**（安全，可反复运行）
    - 骨架内容优先取技能自带的 templates/，取不到则用内置兜底

退出码:
    0 成功（含"什么都没做，都已存在"）
    1 参数错误 / 项目目录不存在
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(os.path.dirname(HERE), "templates")

# 目标文件 -> 模板文件名
LAYOUT = [
    ("INDEX.md", "INDEX.md"),
    ("conventions.md", "conventions.md"),
    ("glossary.md", "glossary.md"),
]

SUBDIRS = ["specs", "decisions", "research"]

FALLBACK = {
    "INDEX.md": (
        "# 项目文档索引\n\n"
        "> **干活前先读本文件。** 新建 / 删除 / 改状态文档后，**必须回来更新这里**。\n"
        "> 索引是唯一入口：不在这里登记的文档，等于不存在。\n\n"
        "## 约定与术语\n\n| 文档 | 说明 | 状态 | 更新 |\n|---|---|---|---|\n"
        "| [conventions.md](conventions.md) | 项目怎么干活 | 现行 | |\n"
        "| [glossary.md](glossary.md) | 术语表 | 现行 | |\n\n"
        "## 规格\n\n| 文档 | 说明 | 状态 | 更新 |\n|---|---|---|---|\n\n"
        "## 决策\n\n| 文档 | 说明 | 状态 | 更新 |\n|---|---|---|---|\n\n"
        "## 调研\n\n| 文档 | 说明 | 状态 | 更新 |\n|---|---|---|---|\n"
    ),
    "conventions.md": (
        "# 项目约定\n\n"
        "> 状态: 现行 ｜ 最后更新: ｜ 适用范围: 全项目\n\n"
        "## 技术栈\n\n## 目录结构\n\n## 命名\n\n## 分支 / 提交 / 评审\n\n"
        "## 测试\n\n## 边界与红线\n\n"
    ),
    "glossary.md": (
        "# 术语表\n\n"
        "> 状态: 现行 ｜ 最后更新: ｜ 适用范围: 全项目\n\n"
        "### （术语）\n\n- **指**：\n- **不指**：\n- **别称**：\n"
    ),
}


def read_template(name):
    path = os.path.join(TEMPLATES, name)
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read(), path
    return FALLBACK.get(name, ""), None


def main():
    ap = argparse.ArgumentParser(description="搭建文档工作区骨架")
    ap.add_argument("project", help="项目根目录")
    ap.add_argument("--dir", default="docs", help="文档目录名（默认 docs）")
    ap.add_argument("--dry-run", action="store_true", help="只打印将要做什么，不写文件")
    args = ap.parse_args()

    root = os.path.abspath(args.project)
    if not os.path.isdir(root):
        print(f"[错误] 项目目录不存在: {root}", file=sys.stderr)
        return 1

    docdir = os.path.join(root, args.dir)

    created, skipped = [], []

    # 目录
    for d in [docdir] + [os.path.join(docdir, s) for s in SUBDIRS]:
        if os.path.isdir(d):
            skipped.append(os.path.relpath(d, root) + "/")
        else:
            if not args.dry_run:
                os.makedirs(d, exist_ok=True)
            created.append(os.path.relpath(d, root) + "/")

    # 文件
    for target, tmpl in LAYOUT:
        dest = os.path.join(docdir, target)
        rel = os.path.relpath(dest, root)
        if os.path.exists(dest):
            skipped.append(rel + "  (已存在，未覆盖)")
            continue
        content, src = read_template(tmpl)
        if not args.dry_run:
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)
        created.append(rel + ("  ← 取自 templates/" + os.path.basename(src) if src else "  ← 内置兜底"))

    print(f"文档工作区: {docdir}")
    print(f"模式: {'dry-run（未写盘）' if args.dry_run else '已写盘'}")
    print()
    if created:
        print("新建:")
        for c in created:
            print("  + " + c)
    if skipped:
        print("跳过（已存在）:")
        for s in skipped:
            print("  = " + s)

    print()
    print("下一步（重要，别省）:")
    print("  1. 填 " + os.path.join(args.dir, "conventions.md") + "：技术栈、目录、命名、评审约定")
    print("  2. 把现有文档登记进 " + os.path.join(args.dir, "INDEX.md"))
    print("  3. 在 AGENTS.md / CLAUDE.md 里加「先查后更新」的硬指令")
    print("     （模板见 templates/conventions.md 末尾）")
    print("  4. 之后每次任务收尾更新文档，并同步 INDEX.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
