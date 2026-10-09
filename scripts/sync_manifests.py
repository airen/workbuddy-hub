#!/usr/bin/env python3
"""sync_manifests.py — 为每个资产生成/刷新 manifest.yaml。

manifest.yaml 是 workbuddy-hub 内部的索引/筛选元数据；资产本身的权威定义仍在
WorkBuddy 原生文件（plugin.json / SKILL.md）中。本脚本从原生文件推导 manifest 字段写入。

用法：
    python scripts/sync_manifests.py [--force]

默认只给「还没有 manifest.yaml」的资产生成；--force 会覆盖已有 manifest。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hublib as hub  # noqa: E402

# 写入 manifest 时保留的字段（去掉内部标记与冗余）
KEEP = {
    "skill": ["id", "name", "version", "type", "description", "category", "tags", "status"],
    "expert": ["id", "name", "version", "type", "expert_type", "description", "category",
               "skills", "tags", "status", "platform_category", "upstream", "license"],
    "team": ["id", "name", "version", "type", "description", "category",
             "members", "workflow", "tags", "status", "platform_category", "upstream", "license"],
}


def clean(meta: dict, atype: str) -> dict:
    out = {}
    for k in KEEP.get(atype, []):
        if k in meta and meta[k] is not None and meta[k] != "":
            out[k] = meta[k]
    # 保证必填项存在（列表型字段即使为空也要保留，否则不通过 schema）
    if atype == "expert" and "skills" not in out:
        out["skills"] = meta.get("skills", [])
    if atype == "team" and "members" not in out:
        out["members"] = meta.get("members", [])
    out.setdefault("type", atype)
    out.setdefault("status", "active")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="生成/刷新资产 manifest.yaml")
    ap.add_argument("--force", action="store_true", help="覆盖已有 manifest.yaml")
    args = ap.parse_args()

    count = 0
    for root, meta, atype in hub.iter_assets():
        mpath = root / "manifest.yaml"
        if mpath.exists() and not args.force:
            print(f"[跳过] 已存在 manifest：{root.relative_to(hub.REPO_ROOT)}")
            continue
        if args.force and mpath.exists():
            mpath.unlink()  # 强制刷新时先删除，让 get_meta 回退到原生文件推导
        meta, atype = hub.get_meta(root, atype)
        data = clean(meta, atype)
        mpath.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8",
        )
        print(f"[生成] {root.relative_to(hub.REPO_ROOT)}/manifest.yaml  (来源: {meta.get('_source')})")
        count += 1
    print(f"\n完成：共生成/刷新 {count} 个 manifest.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
