#!/usr/bin/env python3
"""import_asset.py — 把单个资产（zip 或目录）导入到 workbuddy-hub 的正确 bucket。

用法：
    python scripts/import_asset.py <path-to-zip-or-dir> [--dry-run] [--force]

行为：
    1. 自动识别资产类型（team / expert / skill）。
    2. 定位真正的包根目录（处理「外层多套一层」的情况）。
    3. 移动到 <bucket>/<id>/，其中 <id> 取自资产自身 ID。
    4. 若目标已存在且非 --force，则报错退出。

注意：被导入的原始文件/目录不会被删除；如需把外层包装目录（如含 _manifest.json、
上架报告 的父目录）收进 archive/，请另行处理。
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hublib as hub  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="导入单个资产到 workbuddy-hub")
    ap.add_argument("path", help="zip 文件或已解压的资产目录")
    ap.add_argument("--dry-run", action="store_true", help="只打印将要执行的动作，不实际移动")
    ap.add_argument("--force", action="store_true", help="目标已存在时覆盖")
    args = ap.parse_args()

    src = Path(args.path).resolve()
    if not src.exists():
        print(f"[错误] 路径不存在：{src}", file=sys.stderr)
        return 1

    pkg = hub.find_package_root(src)
    if pkg is None:
        print(f"[错误] 在 {src} 中找不到有效的资产包（需含 .codebuddy-plugin 或 SKILL.md）", file=sys.stderr)
        return 1

    atype = hub.detect_type(pkg)
    if atype is None:
        print(f"[错误] 无法识别资产类型：{pkg}", file=sys.stderr)
        return 1

    meta, _ = hub.get_meta(pkg, atype)
    aid = meta.get("id")
    if not aid:
        print(f"[错误] 无法取得资产 ID（manifest/plugin.json/name 缺失）：{pkg}", file=sys.stderr)
        return 1

    dest = hub.BUCKETS[atype] / aid
    print(f"[识别] 类型={atype}  ID={aid}  名称={meta.get('name')}")
    print(f"[定位] 包根：{pkg}")
    print(f"[目标] {dest}")

    if dest.exists():
        if not args.force:
            print(f"[错误] 目标已存在：{dest}（使用 --force 覆盖）", file=sys.stderr)
            return 1
        print(f"[覆盖] 先删除已有目标：{dest}")

    if args.dry_run:
        print("[dry-run] 未执行实际移动。")
        return 0

    if args.force and dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(pkg), str(dest))
    print(f"[完成] 已移动到 {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
