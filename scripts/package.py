#!/usr/bin/env python3
"""package.py — 把 bucket 中的资产打包成 open.workbuddy.cn 可上传的 zip。

用法：
    python scripts/package.py <bucket-relative-path> [...]
    python scripts/package.py --all          # 打包 bucket 内全部资产
    python scripts/package.py --all --type skill
    python scripts/package.py --out build    # 自定义输出目录

行为：
    1. 自动校验资产存在并识别类型（skill / expert / team）。
    2. 打包前清理 __pycache__ 等构建残留。
    3. 若资产缺少 avatars/<id>.png 或 <id>.jpg，自动从 assets/avatars/_default.jpg 注入一份副本。
    4. 产出 build/<id>.zip，**第一层即为资产目录**，可直接拖到 open.workbuddy.cn 后台。
"""
from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _hublib as hub  # noqa: E402

DEFAULT_AVATAR = hub.REPO_ROOT / "assets" / "avatars" / "_default.jpg"
IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def _ensure_avatar(pkg: Path, asset_id: str) -> None:
    """若 avatars/ 下没有 asset_id 对应的图片，复制默认头像注入。"""
    av = pkg / "avatars"
    if av.exists():
        has_match = any(p.is_file() and p.stem == asset_id and p.suffix.lower() in IMG_EXTS
                        for p in av.iterdir())
        if has_match:
            return
    else:
        try:
            av.mkdir(parents=True)
        except FileExistsError:
            pass
        if not av.exists():
            return
    if not DEFAULT_AVATAR.exists():
        return
    suffix = DEFAULT_AVATAR.suffix.lower()
    if suffix not in IMG_EXTS:
        return
    dest = av / f"{asset_id}{suffix}"
    shutil.copy2(DEFAULT_AVATAR, dest)


def _clean(pkg: Path) -> int:
    """清理常见构建残留，返回删除的文件/目录数。"""
    n = 0
    for d in pkg.rglob("__pycache__"):
        if d.is_dir():
            shutil.rmtree(d)
            n += 1
    for f in pkg.rglob("*.pyc"):
        f.unlink()
        n += 1
    return n


def package_one(asset_path: Path, out_dir: Path) -> Path:
    pkg = asset_path.resolve()
    if not pkg.exists() or not pkg.is_dir():
        raise SystemExit(f"[错误] 资产目录不存在：{pkg}")
    atype = hub.detect_type(pkg)
    if atype is None:
        raise SystemExit(f"[错误] 无法识别资产类型（缺 .codebuddy-plugin 或 SKILL.md）：{pkg}")
    meta, _ = hub.get_meta(pkg, atype)
    aid = meta.get("id")
    if not aid:
        raise SystemExit(f"[错误] 无法取得资产 ID：{pkg}")

    cleaned = _clean(pkg)
    _ensure_avatar(pkg, aid)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{aid}.zip"
    if out.exists():
        out.unlink()

    # 把 pkg 的内容写入 zip，使第一层是 <aid>/...
    base = pkg.name
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(pkg.rglob("*")):
            if f.is_file():
                arc = f.relative_to(pkg.parent)
                zf.write(f, arc)
    size_kb = out.stat().st_size // 1024
    print(f"[打包] {base}  (type={atype})  -> {out.relative_to(hub.REPO_ROOT)}  ({size_kb} KB)  [清理 {cleaned} 项]")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="把 bucket 资产打包成可上传 zip")
    ap.add_argument("paths", nargs="*", help="相对 hub 根的资产路径，如 experts/lao-dao-editor")
    ap.add_argument("--all", action="store_true", help="打包全部资产")
    ap.add_argument("--type", choices=["skill", "expert", "team"], help="与 --all 联用，按类型过滤")
    ap.add_argument("--out", default=str(hub.REPO_ROOT / "build"), help="zip 输出目录")
    args = ap.parse_args()

    out_dir = Path(args.out)
    targets: list[Path] = []
    if args.all:
        for atype, bucket in hub.BUCKETS.items():
            if args.type and atype != args.type:
                continue
            if bucket.exists():
                targets.extend(p for p in sorted(bucket.iterdir()) if p.is_dir() and not p.name.startswith("."))
    else:
        if not args.paths:
            ap.error("请给出资产路径或使用 --all")
        for raw in args.paths:
            targets.append(hub.REPO_ROOT / raw)

    if not targets:
        print("[提示] 没有可打包的资产。")
        return 0

    n = 0
    for t in targets:
        package_one(t, out_dir)
        n += 1
    print(f"\n完成：共打包 {n} 个资产 → {out_dir.relative_to(hub.REPO_ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
