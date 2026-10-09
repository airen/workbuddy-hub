#!/usr/bin/env python3
"""validate.py — 校验 workbuddy-hub 中的资产格式与结构。

检查项：
    1. 每个资产必须有 manifest.yaml（没有则报错，先跑 sync_manifests.py）。
    2. manifest.yaml 通过对应 schemas/*.json 的 JSON Schema 校验。
    3. 结构检查：
       - skill   : 必须有 SKILL.md
       - expert  : 必须有 .codebuddy-plugin/plugin.json 与至少一个 agents/*.md
       - team    : 同上，且必须有 settings.json

退出码：任一检查失败返回 1；全部通过返回 0。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hublib as hub  # noqa: E402


def main() -> int:
    errors = []
    errored = set()
    schema_cache = {}

    for root, meta, atype in hub.iter_assets():
        rel = root.relative_to(hub.REPO_ROOT)
        name = meta.get("id") or rel

        # 1. manifest 存在性
        mpath = root / "manifest.yaml"
        if not mpath.exists():
            errors.append(f"{rel}: 缺少 manifest.yaml（请先运行 sync_manifests.py）")
            errored.add(rel)
            continue
        try:
            manifest = yaml.safe_load(mpath.read_text(encoding="utf-8")) or {}
        except Exception as e:  # noqa: BLE001
            errors.append(f"{rel}: manifest.yaml 解析失败：{e}")
            errored.add(rel)
            continue

        # 2. schema 校验
        sf = hub.REPO_ROOT / "schemas" / hub.SCHEMA_FOR[atype]
        if sf not in schema_cache:
            schema_cache[sf] = json.loads(sf.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema_cache[sf])
        for err in sorted(validator.iter_errors(manifest), key=lambda x: list(x.path)):
            errors.append(f"{rel}: schema 错误 {list(err.path)} — {err.message}")

        # 3. 结构检查
        if atype == "skill":
            if not (root / "SKILL.md").exists():
                errors.append(f"{rel}: skill 缺少 SKILL.md")
        else:
            if not (root / ".codebuddy-plugin" / "plugin.json").exists():
                errors.append(f"{rel}: {atype} 缺少 .codebuddy-plugin/plugin.json")
            agents = list((root / "agents").glob("*.md")) if (root / "agents").is_dir() else []
            if not agents:
                errors.append(f"{rel}: {atype} 缺少 agents/*.md")
            if atype == "team" and not (root / "settings.json").exists():
                errors.append(f"{rel}: team 缺少 settings.json")

        if errors and errors[-1].startswith(str(rel)):
            errored.add(rel)

    total = sum(1 for _, _, _ in hub.iter_assets())
    passes = total - len(errored)
    print(f"校验资产总数：{total}")
    print(f"通过：{passes}")
    if errors:
        print(f"\n✗ 问题({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\n✓ 全部资产校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
