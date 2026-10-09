#!/usr/bin/env python3
"""generate_readme.py — 从 registry/*.yaml 生成 README 资产清单。

读取 registry/skills.yaml、experts.yaml、teams.yaml，在 README.md 的
<!-- ASSETS_START --> 与 <!-- ASSETS_END --> 标记之间插入最新清单。
其余 README 内容保持不变。
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hublib as hub  # noqa: E402

README = hub.REPO_ROOT / "README.md"
START = "<!-- ASSETS_START -->"
END = "<!-- ASSETS_END -->"


def _truncate(s: str, n: int = 80) -> str:
    s = (s or "").replace("\n", " ").replace("|", "\\|").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def _grouped(entries: list[dict], key: str) -> list[tuple[str, list[dict]]]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        buckets[e.get(key, "other") or "other"].append(e)
    for v in buckets.values():
        v.sort(key=lambda x: x.get("id", ""))
    return sorted(buckets.items())


def _table(entries: list[dict], title: str) -> str:
    if not entries:
        return f"## {title}\n\n_（暂无）_\n"
    out = [f"## {title}", ""]
    for cat, items in _grouped(entries, "category"):
        out.append(f"### {cat}")
        out.append("")
        out.append("| ID | 名称 | 描述 |")
        out.append("|---|---|---|")
        for it in items:
            out.append(f"| `{it.get('id','')}` | {it.get('name','')} | {_truncate(it.get('description',''), 120)} |")
        out.append("")
    return "\n".join(out)


def _read(name: str) -> list[dict]:
    p = hub.REPO_ROOT / "registry" / name
    if not p.exists():
        return []
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return data.get(name.replace(".yaml", ""), [])


def build_block() -> str:
    skills = _read("skills.yaml")
    experts = _read("experts.yaml")
    teams = _read("teams.yaml")
    cats = _read("categories.yaml")
    total = len(skills) + len(experts) + len(teams)
    cat_counts = {c["id"]: c.get("count", 0) for c in cats if c.get("id") != "_total"}
    parts = [
        START,
        f"**当前共 {total} 个资产**（技能 {len(skills)} / 专家 {len(experts)} / 专家团 {len(teams)}）。",
        "",
    ]
    parts.append(_table(teams, "专家团（Teams）"))
    parts.append(_table(experts, "专家（Experts）"))
    parts.append(_table(skills, "技能（Skills）"))
    parts.append(END)
    return "\n".join(parts)


def main() -> int:
    if not README.exists():
        print(f"[错误] 找不到 {README}", file=sys.stderr)
        return 1
    text = README.read_text(encoding="utf-8")
    block = build_block()
    if START in text and END in text:
        pre, _, rest = text.partition(START)
        _, _, post = rest.partition(END)
        new = pre + block + "\n" + post
    else:
        # 没有标记：把清单追加到文件末尾
        new = text.rstrip() + "\n\n## 资产清单\n\n> 由 `scripts/generate_readme.py` 自动生成。\n\n" + block + "\n"
    README.write_text(new, encoding="utf-8")
    print(f"[更新] README 资产清单已重新生成（{len(_read('skills.yaml'))} skills, "
          f"{len(_read('experts.yaml'))} experts, {len(_read('teams.yaml'))} teams）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
