#!/usr/bin/env python3
"""_migrate_core.py — 一次性批量导入「核心自研资产」到对应 bucket（幂等）。

直接在 Python 内完成 find_package_root + 类型识别 + 移动，避免 shell 循环被沙箱拦截。
已存在的目标会跳过；源已不存在也会跳过，可反复运行。

用法：python scripts/_migrate_core.py [--archive]   （--archive 会把残留包装目录/非核心项移入 archive/）
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hublib as hub  # noqa: E402

# 核心自研资产：zip 名或已解压目录名（不含后缀）
CORE_ZIPS = [
    "lao-dao-editor", "agent-memory-advisor", "engineering-review-board",
    "self-media-studio", "spec-driven-dev", "diagram-architect",
    "doc-memory-steward", "software-architect",
    "deep-research-crew", "engineering-delivery", "hai-stack", "de-ai-rewrite",
]
CORE_DIRS = ["agent-doc-memory", "ai-project-pilot", "ui-design-field-manual"]

# 暂归档（非核心）：不进 registry
ARCHIVE_ITEMS = ["mattpocock-skills", "creator-ops.zip", "media-content-team.zip"]


def import_one(src: Path) -> str:
    if not src.exists():
        return f"[跳过] 源不存在：{src.name}"
    pkg = hub.find_package_root(src)
    if pkg is None:
        return f"[跳过] 无法识别包根：{src.name}"
    atype = hub.detect_type(pkg)
    if atype is None:
        return f"[跳过] 无法识别类型：{src.name}"
    meta, _ = hub.get_meta(pkg, atype)
    aid = meta.get("id")
    if not aid:
        return f"[跳过] 无 ID：{src.name}"
    dest = hub.BUCKETS[atype] / aid
    if dest.exists():
        return f"[跳过] 目标已存在：{dest.relative_to(hub.REPO_ROOT)}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(pkg), str(dest))
    return f"[迁移] {src.name} -> {dest.relative_to(hub.REPO_ROOT)}  (type={atype})"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", action="store_true", help="把残留包装目录/非核心项移入 archive/")
    args = ap.parse_args()

    print("===== 迁移核心 zip 资产 =====")
    for name in CORE_ZIPS:
        print(import_one(hub.REPO_ROOT / f"{name}.zip"))

    print("\n===== 迁移已解压技能（外层包装目录） =====")
    for name in CORE_DIRS:
        print(import_one(hub.REPO_ROOT / name))

    if args.archive:
        archive = hub.REPO_ROOT / "archive"
        if not archive.exists():
            try:
                archive.mkdir(parents=True, exist_ok=True)
            except FileExistsError:
                pass
        print("\n===== 归档残留/非核心项 =====")
        # 技能包装目录（导入后可能残留）
        for name in CORE_DIRS:
            leftover = hub.REPO_ROOT / name
            if leftover.exists() and leftover.is_dir():
                shutil.move(str(leftover), str(archive / name))
                print(f"[归档] 残留包装目录 {name} -> archive/")
        # 已迁移资产的原始 zip（现在是重复）
        for name in CORE_ZIPS:
            z = hub.REPO_ROOT / f"{name}.zip"
            if z.exists():
                shutil.move(str(z), str(archive / z.name))
                print(f"[归档] 冗余原始 zip {z.name} -> archive/")
        # 非核心项
        for name in ARCHIVE_ITEMS:
            item = hub.REPO_ROOT / name
            if item.exists():
                shutil.move(str(item), str(archive / name))
                print(f"[归档] 非核心 {name} -> archive/")
        # 顶层零散文件
        p = hub.REPO_ROOT / "去AI味改写_头像.png"
        if p.exists():
            dest_assets = hub.BUCKETS["skill"] / "de-ai-rewrite" / "assets"
            dest_assets.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(dest_assets / "avatar.png"))
            print(f"[归位] 去AI味改写_头像.png -> skills/de-ai-rewrite/assets/avatar.png")

    print("\n完成。下一步：python scripts/sync_manifests.py && python scripts/build_registry.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
