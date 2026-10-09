#!/usr/bin/env python3
"""打包专家/专家团/技能为可直接上传到 open.workbuddy.cn 的 zip 文件。"""

import json
import os
import sys
import zipfile
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
OUTPUT_DIR = WORKSPACE / "dist"
OUTPUT_DIR.mkdir(exist_ok=True)


def get_manifest(metadata_path: Path) -> dict | None:
    """读取 manifest.yaml。"""
    try:
        import yaml
    except ImportError:
        return None
    if not metadata_path.exists():
        return None
    with metadata_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collect_assets() -> dict:
    """扫描所有资产，生成 manifest。"""
    result = {"skills": [], "experts": [], "teams": []}

    # 技能
    for skill_dir in sorted((WORKSPACE / "skills").iterdir()):
        if not skill_dir.is_dir():
            continue
        manifest = get_manifest(skill_dir / "manifest.yaml")
        if manifest:
            result["skills"].append({
                "id": skill_dir.name,
                "name": manifest.get("displayName", {}).get("zh", skill_dir.name),
                "category": manifest.get("categoryId", ""),
            })

    # 专家
    for expert_dir in sorted((WORKSPACE / "experts").iterdir()):
        if not expert_dir.is_dir():
            continue
        manifest = get_manifest(expert_dir / "manifest.yaml")
        if manifest:
            result["experts"].append({
                "id": expert_dir.name,
                "name": manifest.get("displayName", {}).get("zh", expert_dir.name),
                "category": manifest.get("categoryId", ""),
            })

    # 专家团
    for team_dir in sorted((WORKSPACE / "teams").iterdir()):
        if not team_dir.is_dir():
            continue
        manifest = get_manifest(team_dir / "manifest.yaml")
        if manifest:
            result["teams"].append({
                "id": team_dir.name,
                "name": manifest.get("displayName", {}).get("zh", team_dir.name),
                "category": manifest.get("categoryId", ""),
            })

    return result


def package_item(asset_type: str, item_id: str) -> Path:
    """打包单个资产为 zip 文件。"""
    source_dir = WORKSPACE / asset_type / item_id
    if not source_dir.is_dir():
        print(f"[ERROR] 找不到资产目录: {source_dir}", file=sys.stderr)
        return None

    output_file = OUTPUT_DIR / f"{item_id}.zip"

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            # 跳过隐藏目录和构建产物
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', '.git')]
            for file in files:
                file_path = Path(root) / file
                arcname = str(file_path.relative_to(WORKSPACE))
                zf.write(file_path, arcname)

    print(f"[OK] 已打包: {output_file} ({output_file.stat().st_size / 1024:.1f}KB)")
    return output_file


def package_all() -> list[Path]:
    """打包所有资产。"""
    assets = collect_assets()
    packages = []

    print(f"\n📦 开始打包 {len(assets['skills'])} 个技能, {len(assets['experts'])} 个专家, {len(assets['teams'])} 个专家团")
    print("=" * 60)

    # 打包技能
    for item in assets["skills"]:
        pkg = package_item("skills", item["id"])
        if pkg:
            packages.append(pkg)

    # 打包专家
    for item in assets["experts"]:
        pkg = package_item("experts", item["id"])
        if pkg:
            packages.append(pkg)

    # 打包专家团
    for item in assets["teams"]:
        pkg = package_item("teams", item["id"])
        if pkg:
            packages.append(pkg)

    # 打包总览
    summary = OUTPUT_DIR / "workbuddy-hub-assets.zip"
    with zipfile.ZipFile(summary, 'w', zipfile.ZIP_DEFLATED) as zf:
        for pkg in packages:
            arcname = f"packages/{pkg.name}"
            zf.write(pkg, arcname)

    print(f"\n📦 已打包总览: {summary} ({len(packages)} 个资产)")
    return packages


if __name__ == "__main__":
    package_all()
