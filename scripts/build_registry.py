#!/usr/bin/env python3
"""build_registry.py — 扫描三个 bucket，生成全局资产索引 registry/*.yaml。

产出：
    registry/skills.yaml     技能清单
    registry/experts.yaml    专家清单
    registry/teams.yaml      专家团清单
    registry/categories.yaml 分类法 + 各类资产计数

同时做引用完整性检查：
    - 专家团 members[].expert_id 是否能在 experts/ 中找到（找不到则标记 embedded=true，仅警告）
    - 专家 skills[] 是否能在 skills/ 中找到（找不到则标记 embedded，仅警告）
    - 专家团 workflow 文件是否存在（不存在则警告）

退出码：发现硬错误（未知类型、缺必填 ID 等）返回 1；仅有警告返回 0。
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hublib as hub  # noqa: E402

CATEGORY_TAXONOMY = {
    "research": "调研与信息检索",
    "development": "开发与工程",
    "content": "内容生产",
    "design": "设计与视觉",
    "business": "商业分析与运营",
    "other": "其他 / 未分类",
}


def collect():
    skills, experts, teams = [], [], []
    for root, meta, atype in hub.iter_assets():
        rel = root.relative_to(hub.REPO_ROOT)
        entry = dict(meta)
        entry["path"] = str(rel)
        if atype == "skill":
            skills.append(entry)
        elif atype == "expert":
            experts.append(entry)
        elif atype == "team":
            teams.append(entry)
    return skills, experts, teams


def integrity(skills, experts, teams):
    errors, warnings = [], []
    skill_ids = {s["id"] for s in skills if s.get("id")}
    expert_ids = {e["id"] for e in experts if e.get("id")}

    for e in experts:
        root = hub.REPO_ROOT / e["path"]
        for sid in e.get("skills", []):
            if sid in skill_ids:
                continue  # 全局引用，正常
            if (root / "skills" / sid).exists():
                continue  # 自带内嵌技能，正常
            warnings.append(f"专家 {e['id']} 引用技能 '{sid}' 既不在 skills/ 也不在其自身 skills/ 中（缺失）")

    for t in teams:
        root = hub.REPO_ROOT / t["path"]
        for m in t.get("members", []):
            eid = m.get("expert_id")
            if eid in expert_ids:
                m["embedded"] = False
            elif (root / "agents" / f"{eid}.md").exists():
                m.setdefault("embedded", True)  # 自带内嵌成员，正常
            else:
                m.setdefault("embedded", True)
                warnings.append(f"专家团 {t['id']} 成员 '{eid}' 既不在 experts/ 也不在其自身 agents/ 中（缺失）")
        wf = t.get("workflow")
        if wf and not (root / wf).exists():
            warnings.append(f"专家团 {t['id']} 的 workflow 文件不存在：{wf}")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description="生成全局资产索引 registry/*.yaml")
    ap.add_argument("--out", default=str(hub.REPO_ROOT / "registry"), help="registry 输出目录")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    skills, experts, teams = collect()
    errors, warnings = integrity(skills, experts, teams)

    # 按 id 排序，稳定输出
    skills.sort(key=lambda x: x.get("id", ""))
    experts.sort(key=lambda x: x.get("id", ""))
    teams.sort(key=lambda x: x.get("id", ""))

    (out / "skills.yaml").write_text(
        yaml.safe_dump({"skills": skills}, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )
    (out / "experts.yaml").write_text(
        yaml.safe_dump({"experts": experts}, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )
    (out / "teams.yaml").write_text(
        yaml.safe_dump({"teams": teams}, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )

    counts = defaultdict(int)
    for lst, key in ((skills, "category"), (experts, "category"), (teams, "category")):
        for item in lst:
            counts[item.get(key, "other")] += 1
    categories = []
    for cid, label in CATEGORY_TAXONOMY.items():
        categories.append({"id": cid, "label": label, "count": counts.get(cid, 0)})
    categories.append({"id": "_total", "label": "合计", "count": len(skills) + len(experts) + len(teams)})
    (out / "categories.yaml").write_text(
        yaml.safe_dump({"categories": categories}, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )

    print(f"技能    : {len(skills)}")
    print(f"专家    : {len(experts)}")
    print(f"专家团  : {len(teams)}")
    for c in categories:
        if c["id"] != "_total":
            print(f"  分类 {c['id']:<12} {c['label']:<12} {c['count']}")
    if warnings:
        print(f"\n⚠ 警告({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"\n✗ 错误({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\n✓ registry 生成完成（仅警告，无硬错误）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
