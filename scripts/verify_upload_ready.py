#!/usr/bin/env python3
"""verify_upload_ready.py — 上架 open.workbuddy.cn 之前的硬校验。

把平台已知的硬性校验固化下来，尤其是**只有在上传页才会暴露**的那些
（例如 `tags` 必须恰好 3 个，多了会报「解析失败：tags 须固定 3 个」）。

用法：
    python scripts/verify_upload_ready.py experts/visual-forge-studio [...]
    python scripts/verify_upload_ready.py --all

退出码：存在任一「失败」项返回 1；仅「提示」项不影响退出码。

失败项（errs）：
    1. plugin.json 存在且可解析；name / plugin / agentName 三处一致，并与目录名一致
    2. tags 恰好 3 个，且每项都有 zh 与 en
    3. displayDescription.zh 长度按 **UTF-16 码元**计（与浏览器 JS String.length 同口径）在 40–50
    4. defaultInitPrompt 等于 quickPrompts[0]；quickPrompts 恰好 3 条
    5. team：profession.zh == displayName.zh；settings.json 的 agent 为 <id>-team-lead
    6. skills / agents 引用路径真实存在
    7. agents/*.md 与 skills/*/SKILL.md：frontmatter 必须能在文件开头解析出来（BOM / 前置注释
       视为失败，不再静默跳过）；name 与文件名（或目录名）一致；必备字段齐全
    8. expertType 必须是 `team` 或 `agent`（大小写敏感），否则报错
    9. 已打包的 zip：第一层为资产目录，体积不超限（专家包 20 MB / 技能包 3 MB）

提示项（warns，不影响退出码）：
    - displayDescription 余量不足（UTF-16 长度 > 48 或 < 42）
    - 缺 avatars/<id>.(png|jpg)（package.py 会注入默认头像）
    - build/<id>.zip 尚未生成
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hublib as hub  # noqa: E402

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
SIZE_LIMIT_MB = {"expert": 20, "team": 20, "skill": 3}
_FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def utf16_len(s: str) -> int:
    """按 UTF-16 码元计数，与浏览器 JS `String.length` 同口径。"""
    return len(s.encode("utf-16-le")) // 2


def _frontmatter(path: Path) -> dict:
    """读取 YAML frontmatter。

    解析失败**显式返回错误**，绝不静默返回空 dict —— 否则所有依赖它的检查
    （name 一致性等）会被整体跳过，门禁变成 fail-open。
    """
    try:
        text = path.read_text(encoding="utf-8-sig")  # 自动去掉 BOM
    except Exception as e:  # noqa: BLE001
        return {"__error__": f"读取失败：{e}"}
    m = _FRONT_RE.match(text)
    if not m:
        return {"__error__": "frontmatter 未在文件开头找到（文件以 BOM、注释或空行开头？）"}
    import yaml

    try:
        data = yaml.safe_load(m.group(1)) or {}
    except Exception as e:  # noqa: BLE001
        return {"__error__": f"frontmatter YAML 解析失败：{e}"}
    if not isinstance(data, dict):
        return {"__error__": "frontmatter 不是键值映射"}
    return data


def check_asset(root: Path) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    aid = root.name

    if not (root / ".codebuddy-plugin" / "plugin.json").exists() and (root / "SKILL.md").exists():
        fm = _frontmatter(root / "SKILL.md")
        if fm.get("__error__"):
            return [f"SKILL.md：{fm['__error__']}"], warns
        if fm.get("name") != aid:
            errs.append(f"SKILL.md name={fm.get('name')!r} 与目录名 {aid!r} 不一致")
        for k in ("description", "version", "category"):
            if not fm.get(k):
                errs.append(f"SKILL.md frontmatter 缺 {k}")
        return errs, warns

    pj = root / ".codebuddy-plugin" / "plugin.json"
    if not pj.exists():
        return [f"{aid}：既无 .codebuddy-plugin/plugin.json，也不含 SKILL.md"], warns
    try:
        d = json.loads(pj.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [f"plugin.json 解析失败：{e}"], warns

    atype = d.get("expertType")

    # 8. expertType 显式校验（大小写敏感，未知值必须报错而不是回落成 expert）
    if atype not in ("team", "agent"):
        errs.append(f"expertType 必须为 'team' 或 'agent'，当前 {atype!r}")

    # 1. 三处一致
    if d.get("name") != aid:
        errs.append(f"plugin.json name={d.get('name')!r} 与目录名 {aid!r} 不一致")
    if d.get("plugin") != d.get("name"):
        errs.append("plugin 与 name 不一致")
    if not d.get("agentName"):
        errs.append("缺 agentName")
    if atype == "team" and d.get("agentName") != f"{aid}-team-lead":
        errs.append(f"team 的 agentName 应为 {aid}-team-lead")

    # 2. tags 恰好 3 个
    tags = d.get("tags") or []
    if len(tags) != 3:
        errs.append(f"tags 必须恰好 3 个，当前 {len(tags)} 个（平台报「tags 须固定 3 个」）")
    for t in tags:
        if not isinstance(t, dict) or "zh" not in t or "en" not in t:
            errs.append(f"tag 缺 zh/en：{t}")

    # 3. displayDescription.zh（UTF-16 口径，与浏览器一致）
    dd = ((d.get("displayDescription") or {}).get("zh")) or ""
    n16 = utf16_len(dd)
    if not (40 <= n16 <= 50):
        errs.append(f"displayDescription.zh 长度 {n16}（UTF-16 码元），要求 40–50")
    elif n16 > 48 or n16 < 42:
        warns.append(f"displayDescription.zh 长度 {n16}，余量不足（建议 42–48）")

    # 4. 快捷提示
    qp = d.get("quickPrompts") or []
    if len(qp) != 3:
        errs.append(f"quickPrompts 应为 3 条，当前 {len(qp)} 条")
    if qp and d.get("defaultInitPrompt") != qp[0]:
        errs.append("defaultInitPrompt 必须等于 quickPrompts[0]")

    # 5. team 专属
    if atype == "team":
        if (d.get("profession") or {}).get("zh") != (d.get("displayName") or {}).get("zh"):
            errs.append("team 的 profession.zh 必须与 displayName.zh 完全一致")
        st = root / "settings.json"
        if not st.exists():
            errs.append("team 缺 settings.json")
        else:
            try:
                if json.loads(st.read_text(encoding="utf-8")).get("agent") != d.get("agentName"):
                    errs.append("settings.json 的 agent 与 plugin.json 的 agentName 不一致")
            except Exception as e:  # noqa: BLE001
                errs.append(f"settings.json 解析失败：{e}")

    # 6. 引用路径存在
    for s in d.get("skills") or []:
        if not (root / s).is_dir():
            errs.append(f"skills 引用了不存在的目录：{s}")
    agents = d.get("agents") or []
    if not agents:
        errs.append("agents 为空")
    for a in agents:
        if not (root / a).is_file():
            errs.append(f"agents 引用了不存在的文件：{a}")

    # 7a. agent md：frontmatter 必须可解析，name 与文件名一致
    for ag in sorted((root / "agents").glob("*.md")):
        fm = _frontmatter(ag)
        if fm.get("__error__"):
            errs.append(f"{ag.name}：{fm['__error__']}")
            continue
        if not fm.get("name"):
            errs.append(f"{ag.name} 缺 frontmatter name")
        elif fm["name"] != ag.stem:
            errs.append(f"{ag.name} 的 frontmatter name={fm['name']!r} 与文件名不一致")

    # 7b. SKILL.md：同上，且必备字段齐全
    for sk in sorted((root / "skills").glob("*/SKILL.md")):
        fm = _frontmatter(sk)
        if fm.get("__error__"):
            errs.append(f"{sk.parent.name}/SKILL.md：{fm['__error__']}")
            continue
        if not fm.get("name"):
            errs.append(f"{sk.parent.name}/SKILL.md 缺 frontmatter name")
        elif fm["name"] != sk.parent.name:
            errs.append(f"{sk.parent.name}/SKILL.md 的 name={fm['name']!r} 与目录名不一致")
        for k in ("description", "version", "category"):
            if not fm.get(k):
                errs.append(f"{sk.parent.name}/SKILL.md 缺 {k}")

    # 提示：头像
    av = root / "avatars"
    has_avatar = av.is_dir() and any(
        p.is_file() and p.stem == aid and p.suffix.lower() in IMG_EXTS for p in av.iterdir()
    )
    if not has_avatar:
        warns.append(f"avatars/ 下缺 {aid}.png|jpg（package.py 会注入默认头像，上架前建议替换）")

    # 9. zip
    z = hub.REPO_ROOT / "build" / f"{aid}.zip"
    if not z.exists():
        warns.append(f"尚未打包：build/{aid}.zip 不存在（先跑 package.py）")
    else:
        size_mb = z.stat().st_size / 1024 / 1024
        limit = SIZE_LIMIT_MB.get(atype if atype in SIZE_LIMIT_MB else "expert", 20)
        if size_mb > limit:
            errs.append(f"{z.name} 体积 {size_mb:.2f} MB 超过 {limit} MB 上限")
        with zipfile.ZipFile(z) as zf:
            names = zf.namelist()
        if names and not all(n.startswith(f"{aid}/") for n in names):
            errs.append(f"{z.name} 第一层不是资产目录 {aid}/（应重新打包）")

    return errs, warns


def main(argv: list[str]) -> int:
    if not argv or argv[0] == "--all":
        targets = [r for r, _, _ in hub.iter_assets()]
    else:
        targets = [(hub.REPO_ROOT / a).resolve() for a in argv]

    failed = 0
    warned = 0
    for t in targets:
        name = t.name if t.is_absolute() else t
        errs, warns = check_asset(t)
        if errs:
            failed += 1
            print(f"✗ {name}")
            for e in errs:
                print(f"    [失败] {e}")
        else:
            print(f"✓ {name}")
        if warns:
            warned += 1
            for w in warns:
                print(f"    [提示] {w}")

    total = len(targets)
    print(f"\n共检查 {total} 个资产，通过 {total - failed}，失败 {failed}（{warned} 个含提示）")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
