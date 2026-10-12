#!/usr/bin/env python3
"""package_upload.py —— 【已弃用】请改用 scripts/package.py。

历史问题（2026-10-10 定位）：
    本脚本用 `arcname = file_path.relative_to(WORKSPACE)` 计算包内路径，并跳过所有
    点开头的目录。两个后果：
      1. zip 第一层变成 `experts/<id>/`、`teams/<id>/`（多套一层包装目录）；
      2. `.codebuddy-plugin/` 整个被跳过 —— plugin.json 根本没进包。

    平台据此报「解析失败：未找到 .codebuddy-plugin/plugin.json」/「文件类型不符合要求」。
    当时 build/ 下 51 个 zip 里有 47 个是坏的。

现在本脚本只做一件事：把调用转发给正确的 scripts/package.py。
（package.py 保证第一层即资产目录、包含 .codebuddy-plugin/、并自动注入缺失头像。）

用法（等价于直接调用 package.py）：
    python scripts/package_upload.py                # == package.py --all
    python scripts/package_upload.py --type skill   # == package.py --all --type skill
    python scripts/package_upload.py experts/lao-dao-editor
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main(argv: list[str]) -> int:
    print(
        "[弃用] scripts/package_upload.py 会产出缺少 .codebuddy-plugin/plugin.json 的坏包，\n"
        "       已转发到 scripts/package.py。请直接使用：python scripts/package.py --all\n",
        file=sys.stderr,
    )
    import package  # noqa: PLC0415  (同目录的 scripts/package.py)

    args = list(argv)
    # 无参数时等价于 --all；保留 --type / --out / 显式路径的语义
    if not args:
        args = ["--all"]
    sys.argv = ["package.py", *args]
    return package.main()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
