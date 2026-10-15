#!/usr/bin/env python3
"""生成 workbuddy-hub 资产市场静态站点。

数据源：registry/{experts,teams,skills,categories}.yaml —— 本仓库的派生索引，
        即「单一事实来源」的投影，因此本站点不与任何资产文件重复维护。

产物：  site/index.html          单文件页面（内联 CSS/JS/数据，零外部请求）
        site/assets/avatars/*.jpg 压缩后的头像
        site/.nojekyll            跳过 Jekyll 处理
        site/.hub-site-build      产物归属标记（供下次运行识别本目录）

用法：
    python3 scripts/build_site.py                 # 生成到 ./site
    python3 scripts/build_site.py --out /tmp/site # 指定输出目录
    python3 scripts/build_site.py --no-avatars    # 跳过头像处理（快速预览）

依赖：pyyaml 必需；Pillow 可选（缺失时降级为直接复制原图）。
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_DIR = REPO_ROOT / "registry"
TEMPLATE_PATH = REPO_ROOT / "templates" / "site" / "page.html"
DEFAULT_OUT = REPO_ROOT / "site"

DEFAULT_REPO_URL = "https://github.com/airen/workbuddy-hub"
DEFAULT_SITE_URL = "https://airen.github.io/workbuddy-hub/"
DEFAULT_BRANCH = "main"

AVATAR_SIZE = 256
AVATAR_QUALITY = 82
AVATAR_EXTS = ("jpg", "jpeg", "png", "webp")

TYPE_LABEL = {"expert": "专家", "team": "专家团"}
TYPE_RANK = {"team": 0, "expert": 1}


class BuildError(RuntimeError):
    """构建过程中的可预期错误。"""


def _load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:  # noqa: BLE001
        raise BuildError(
            "缺少 pyyaml，请先安装：pip install -r scripts/requirements.txt"
        ) from exc
    if not path.is_file():
        raise BuildError(f"缺少数据源文件：{path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise BuildError(f"解析失败 {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise BuildError(f"数据源格式异常（顶层应为映射）：{path}")
    return data


def load_registry() -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    experts = _load_yaml(REGISTRY_DIR / "experts.yaml").get("experts") or []
    teams = _load_yaml(REGISTRY_DIR / "teams.yaml").get("teams") or []
    skills = _load_yaml(REGISTRY_DIR / "skills.yaml").get("skills") or []
    categories = _load_yaml(REGISTRY_DIR / "categories.yaml").get("categories") or []
    return experts, teams, skills, categories


def _category_order(categories: list[dict]) -> tuple[list[str], dict[str, str]]:
    """返回分类的展示顺序与 id→label 映射（排除内部统计项 _total）。"""
    order: list[str] = []
    labels: dict[str, str] = {}
    for cat in categories:
        cid = str(cat.get("id") or "").strip()
        if not cid or cid.startswith("_"):
            continue
        order.append(cid)
        labels[cid] = str(cat.get("label") or cid)
    return order, labels


# 资产 id 白名单：小写字母/数字开头，允许 . _ -，不得含路径成分。
# registry 内容可能来自第三方 PR，而 id / path 会被直接拼进文件系统路径，
# 因此必须在入口处（而非使用处）拦下非法值，避免路径穿越。
# 长度上限 64：既是合理命名约束，也避免超长名字触发 ENAMETOOLONG（OSError），
# 让构建在异常输入下仍是「干净失败」而不是抛栈崩溃。
_SAFE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
_BUCKET_FOR = {"expert": "experts", "team": "teams"}

# 本脚本产物目录的专属标记。用它（而非通用的 .nojekyll）判断「这个目录是我建的」，
# 否则任何碰巧含 .nojekyll 的静态站目录都会被当成自己的产物而被清理。
_BUILD_MARKER = ".hub-site-build"


def _safe_id(value: object, kind: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        raise BuildError(f"{kind} 条目缺少 id")
    if ".." in raw or not _SAFE_ID_RE.match(raw):
        raise BuildError(
            f"{kind} 的 id 非法（只允许小写字母、数字与 . _ -，长度 ≤ 64，"
            f"且不得含 ..）：{raw!r}"
        )
    return raw


def _safe_path(rel_path: str, kind: str, asset_id: str) -> str:
    """校验 registry 里的 path：必须恰好是 <bucket>/<id>，且落在仓库根之内。"""
    bucket = _BUCKET_FOR[kind]
    prefix = f"{bucket}/"
    if not rel_path.startswith(prefix) or rel_path[len(prefix):] != asset_id:
        raise BuildError(
            f"{asset_id} 的 path 必须恰好为 {bucket}/{asset_id}，实际为 {rel_path!r}"
        )
    if not (REPO_ROOT / rel_path).resolve().is_relative_to(REPO_ROOT.resolve()):
        raise BuildError(f"{asset_id} 的 path 越出仓库根：{rel_path!r}")
    return rel_path


def _avatar_source(asset_dir: Path, asset_id: str) -> Path | None:
    """在 <asset_dir>/avatars/ 下查找 <id>.<ext> 主头像。

    目录/文件名异常（超长、非法字符等）会抛 OSError，这里吞掉并当作「没有头像」，
    由调用方回退默认头像——单个坏条目不应中断整站构建。
    """
    base = asset_dir / "avatars"
    try:
        if not base.is_dir():
            return None
        for ext in AVATAR_EXTS:
            candidate = base / f"{asset_id}.{ext}"
            if candidate.is_file():
                return candidate
    except OSError:
        return None
    return None


def build_items(
    experts: list[dict],
    teams: list[dict],
    categories: list[dict],
    repo_url: str,
    branch: str,
) -> tuple[list[dict], list[dict], list[str]]:
    """把 registry 条目归一化为站点卡片数据。

    返回 (items, active_categories, warnings)。
    """
    order, labels = _category_order(categories)
    order_index = {cid: i for i, cid in enumerate(order)}
    fallback_cat_index = len(order)

    items: list[dict] = []
    used_categories: dict[str, str] = {}
    warnings: list[str] = []

    for raw, kind in [(e, "expert") for e in experts] + [(t, "team") for t in teams]:
        asset_id = str(raw.get("id") or "").strip()
        if not asset_id:
            warnings.append(f"跳过无 id 的 {kind} 条目")
            continue
        # id 与 path 会参与文件系统路径拼接，先过白名单（见 _safe_id / _safe_path）
        asset_id = _safe_id(asset_id, kind)

        rel_path = str(raw.get("path") or "").strip()
        if not rel_path:
            rel_path = f"{_BUCKET_FOR[kind]}/{asset_id}"
        rel_path = _safe_path(rel_path, kind, asset_id)

        category = str(raw.get("category") or "other").strip() or "other"
        category_label = labels.get(category, category)
        used_categories[category] = category_label

        tags = [str(t) for t in (raw.get("tags") or []) if str(t).strip()]

        item = {
            "id": asset_id,
            "name": str(raw.get("name") or asset_id),
            "type": kind,
            "typeLabel": TYPE_LABEL[kind],
            "description": str(raw.get("description") or "").strip(),
            "category": category,
            "categoryLabel": category_label,
            "tags": tags,
            "version": str(raw.get("version") or ""),
            "path": rel_path,
            "url": f"{repo_url}/tree/{branch}/{rel_path}",
            "avatar": "",
            "skillCount": None,
            "memberCount": None,
            "coordinator": None,
        }

        if kind == "expert":
            item["skillCount"] = len(raw.get("skills") or [])
        else:
            members = raw.get("members") or []
            item["memberCount"] = len(members)
            lead = next(
                (
                    str(m.get("expert_id"))
                    for m in members
                    if isinstance(m, dict) and m.get("role") == "coordinator"
                ),
                None,
            )
            item["coordinator"] = lead

        items.append(item)

    # 排序：分类顺序 → 同分类内专家团在前 → id 字母序，保证输出稳定（幂等）
    items.sort(
        key=lambda it: (
            order_index.get(it["category"], fallback_cat_index),
            TYPE_RANK.get(it["type"], 9),
            it["id"],
        )
    )

    # 分类筛选栏只列出实际有资产的分类，并沿用 registry 中的顺序
    active = [
        {"id": cid, "label": labels.get(cid, cid)}
        for cid in order
        if cid in used_categories
    ]
    for cid, label in used_categories.items():
        if cid not in order:
            active.append({"id": cid, "label": label})

    return items, active, warnings


def _resample_filter():
    try:
        from PIL import Image

        return Image.Resampling.LANCZOS
    except (ImportError, AttributeError):  # noqa: BLE001
        return None


def prepare_avatars(
    items: list[dict], out_dir: Path, enabled: bool
) -> tuple[list[str], list[str]]:
    """压缩头像到 <out>/assets/avatars/，并回填 item['avatar']（相对路径）。

    返回 (warnings, errors)。
    """
    warnings: list[str] = []
    errors: list[str] = []
    avatar_dir = out_dir / "assets" / "avatars"

    default_src = REPO_ROOT / "assets" / "avatars" / "_default.jpg"
    default_rel = "assets/avatars/_default.jpg"

    if not enabled:
        # 不产出任何图片文件，卡片改走首字母占位分支，
        # 否则页面会引用一堆不存在的头像（35 个 404）
        for item in items:
            item["avatar"] = ""
        warnings.append("--no-avatars：未生成头像文件，卡片改显示首字母占位")
        return warnings, errors

    avatar_dir.mkdir(parents=True, exist_ok=True)

    # 若 <out>/assets/avatars 是被预先放置的符号链接，写入会落到站点目录之外。
    # 这里放弃本次头像写入（卡片回退首字母占位），并记入 errors——errors 非空会让
    # 构建以退出码 1 收场：符号链接头像目录属异常状态，应当显式失败而非静默降级。
    if avatar_dir.is_symlink():
        errors.append(
            f"头像目录是符号链接，已跳过头像写入（卡片改首字母占位）：{avatar_dir}"
        )
        return warnings, errors

    pillow_ok = True
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        pillow_ok = False
        warnings.append(
            "未安装 Pillow，头像将直接复制原图（页面体积会明显变大）。"
            "安装：pip install Pillow"
        )

    jobs: dict[str, Path] = {}
    for item in items:
        src = _avatar_source(REPO_ROOT / item["path"], item["id"])
        if src is None:
            if default_src.is_file():
                jobs["_default"] = default_src
                item["avatar"] = default_rel
                warnings.append(f"{item['id']}: 缺少头像，回退默认头像")
            else:
                warnings.append(f"{item['id']}: 缺少头像且无默认头像，卡片将不显示头像")
            continue
        jobs[item["id"]] = src
        item["avatar"] = f"assets/avatars/{item['id']}.jpg"

    # 基准取自 out_dir（而非 avatar_dir.resolve()）：后者在 avatar_dir 是符号链接时
    # 会一并解析到链接目标，从而让「越界检查」失去意义。
    avatar_root = out_dir.resolve() / "assets" / "avatars"
    seen: set[str] = set()
    written: set[str] = set()
    for key, src in sorted(jobs.items()):
        if key in seen:
            continue
        seen.add(key)
        dst = (avatar_dir / f"{key}.jpg").resolve()
        # 双保险：id 已在 build_items 过白名单，这里再断言写入目标未越出头像目录
        if not dst.is_relative_to(avatar_root):
            errors.append(f"头像目标路径越界，已跳过：{dst}")
            continue
        try:
            _write_avatar(src, dst, pillow_ok)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"头像处理失败 {src.name}: {exc}")
            continue
        written.add(key)

    # 没真正落盘的头像不能留在卡片上，否则 HTML 会出现指向不存在文件的 <img src>（404）。
    # 清回空串后卡片自动走首字母占位分支。
    for item in items:
        if item["avatar"] and Path(item["avatar"]).stem not in written:
            item["avatar"] = ""

    return warnings, errors


def _write_avatar(src: Path, dst: Path, pillow_ok: bool) -> None:
    if not pillow_ok:
        # 降级：原样复制，保留扩展名（页面按 <id>.jpg 引用，故统一改名为 .jpg 会失真，
        # 因此这里直接复制为 .jpg 是安全的——浏览器按内容嗅探，JPEG/PNG 均可显示）
        shutil.copyfile(src, dst)
        return

    from PIL import Image, ImageOps

    resample = _resample_filter()
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        elif im.mode == "L":
            im = im.convert("RGB")
        # 居中偏上裁剪：人物/角色头像的视觉重心通常在偏上位置
        im = ImageOps.fit(
            im, (AVATAR_SIZE, AVATAR_SIZE), method=resample, centering=(0.5, 0.4)
        )
        im.save(dst, "JPEG", quality=AVATAR_QUALITY, optimize=True, progressive=True)


_TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")

# 卡片结构在此定义，样式类名见 templates/site/page.html 的 CSS。
# 卡片由 Python 静态渲染进 HTML（而非由 JS 生成），因此禁用 JavaScript 时
# 依然能看到全部资产内容，搜索引擎与 AI 检索也能直接读到文本。
_CARD_TPL = """\
    <a class="card" href="{url}" target="_blank" rel="noopener" data-type="{type}" data-cat="{category}" data-id="{id}">
      {avatar}
      <span class="card-main">
        <span class="card-head">
          <span class="card-name">{name}</span>
          <span class="badge badge--{type}">{type_label}</span>
        </span>
        {description}
        {tags}
        <span class="card-meta">{meta}</span>
      </span>
    </a>"""


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def render_cards(items: list[dict]) -> str:
    cards: list[str] = []
    for i, item in enumerate(items):
        # 首屏前 6 张头像提前加载（覆盖桌面 3 列首行与移动端首屏），保护 LCP；
        # 其余保持 lazy。fetchpriority=high 提示浏览器优先这些资源。
        eager = i < 6
        if item["avatar"]:
            load_attrs = (
                'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
            )
            avatar = (
                f'<img class="avatar" src="{_esc(item["avatar"])}" alt="" '
                f'width="52" height="52" {load_attrs} decoding="async">'
            )
        else:
            initial = (item["name"] or "?")[:1]
            avatar = (
                '<span class="avatar avatar--ph" aria-hidden="true">'
                f"{_esc(initial)}</span>"
            )

        description = (
            f'<span class="card-desc">{_esc(item["description"])}</span>'
            if item["description"]
            else ""
        )

        tags = ""
        if item["tags"]:
            chips = "".join(f'<span class="tag">{_esc(t)}</span>' for t in item["tags"][:3])
            tags = f'<span class="card-tags">{chips}</span>'

        meta = [f'<span class="meta-cat">{_esc(item["categoryLabel"])}</span>']
        if item["skillCount"] is not None:
            meta.append(f"<span>{item['skillCount']} 个技能</span>")
        if item["memberCount"] is not None:
            meta.append(f"<span>{item['memberCount']} 位成员</span>")
        if item["version"]:
            meta.append(f'<span class="meta-ver">v{_esc(item["version"])}</span>')

        cards.append(
            _CARD_TPL.format(
                url=_esc(item["url"]),
                type=_esc(item["type"]),
                category=_esc(item["category"]),
                id=_esc(item["id"]),
                avatar=avatar,
                name=_esc(item["name"]),
                type_label=_esc(item["typeLabel"]),
                description=description,
                tags=tags,
                meta="".join(meta),
            )
        )
    return "\n".join(cards)


def render_category_chips(categories: list[dict]) -> str:
    chips = [
        '<button type="button" data-filter-cat="all" aria-pressed="true">全部分类</button>'
    ]
    for cat in categories:
        chips.append(
            f'<button type="button" data-filter-cat="{_esc(cat["id"])}" '
            f'aria-pressed="false">{_esc(cat["label"])}</button>'
        )
    return "\n    ".join(chips)


def render_template(template_text: str, tokens: dict) -> str:
    missing: list[str] = []

    def _replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in tokens:
            missing.append(key)
            return match.group(0)
        return str(tokens[key])

    rendered = _TOKEN_RE.sub(_replace, template_text)
    if missing:
        raise BuildError(f"模板占位符缺少对应值：{', '.join(sorted(set(missing)))}")
    return rendered


def _assert_safe_out_dir(out_dir: Path) -> None:
    """输出目录必须是「新建目录」或「本脚本自己的产物目录」。

    白名单式判定，比罗列黑名单可靠（黑名单永远列不全：/etc、/usr/lib、
    /Applications、assets/ 等都可能被写入并在随后被清理）：
      - 目录不存在                    → 允许（首次生成）
      - 目录存在且为空                → 允许
      - 目录含本脚本的专属标记文件      → 允许（上次生成留下的）
      - 其它已存在且非空的目录          → 拒绝

    归属判据用专属标记 `_BUILD_MARKER` 而非通用的 `.nojekyll`：后者是任何静态站
    都可能有的文件，拿它当「这是我建的目录」的证据会误判并清理别人的目录。
    """
    resolved = out_dir.resolve()
    if resolved == REPO_ROOT.resolve():
        raise BuildError(f"拒绝把输出目录指向仓库根：{resolved}")
    if not resolved.exists():
        return
    if not resolved.is_dir():
        raise BuildError(f"输出路径已存在但不是目录：{resolved}")
    if (resolved / _BUILD_MARKER).is_file():
        return
    if not any(resolved.iterdir()):
        return
    raise BuildError(
        f"输出目录已存在且不是本脚本的产物目录，拒绝写入：{resolved}"
        f"（需为空目录，或包含上次生成留下的 {_BUILD_MARKER}）"
    )


def _prune_stale_avatars(out_dir: Path, keep_stems: set[str]) -> list[str]:
    """删除本次未再产出的旧头像。

    **刻意在写完全部新产物之后才调用**：先写后删，则即使构建被中断（Ctrl-C、
    进程被杀、CI 超时），输出目录里仍是「上一次的完整产物」，而不是「已删旧的、
    又没写新的」的半成品。反过来（先删后写）会让一次中断把站点彻底打坏——
    曾实测到 `index.html` 消失、35 张头像只剩 8 张。

    只删图片扩展名，且跳过符号链接，绝不触碰其他文件。
    """
    failures: list[str] = []

    # 本次一张头像都没产出 ⇒ 无从判断谁是「旧」的，宁可不删。
    # 同时保证 --no-avatars（纯预览）不会把已有头像清空。
    if not keep_stems:
        return failures

    assets_dir = out_dir / "assets"
    avatar_dir = assets_dir / "avatars"
    # assets 或 avatars 任一层被换成符号链接时，遍历会落到站点目录之外，
    # 此时删除即成为「越界删除原语」——直接放弃清理。
    if assets_dir.is_symlink() or avatar_dir.is_symlink():
        return failures
    if not avatar_dir.is_dir():
        return failures

    root = out_dir.resolve()
    for f in avatar_dir.iterdir():
        if not f.is_file() or f.is_symlink():
            continue
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        if f.stem in keep_stems:
            continue
        # 逐条归属断言：解析后的真实路径必须落在输出目录内（兜住父级软链等绕过）
        if not f.resolve().is_relative_to(root):
            continue
        try:
            f.unlink()
        except OSError as exc:
            failures.append(f"旧头像未能清理（无碍本次产物）：{f.name} — {exc}")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="生成 workbuddy-hub 资产市场静态站点"
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_OUT),
        help=f"输出目录（默认 {DEFAULT_OUT}）",
    )
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL, help="仓库地址")
    parser.add_argument("--site-url", default=DEFAULT_SITE_URL, help="站点公开地址")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="用于源码链接的分支")
    parser.add_argument(
        "--no-avatars",
        action="store_true",
        help="跳过头像压缩（仅生成 HTML，用于快速预览）",
    )
    parser.add_argument("--quiet", action="store_true", help="只输出错误")
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = (REPO_ROOT / out_dir).resolve()

    try:
        _assert_safe_out_dir(out_dir)

        experts, teams, skills, categories = load_registry()
        items, active_categories, build_warnings = build_items(
            experts, teams, categories, args.repo_url.rstrip("/"), args.branch
        )

        if not items:
            raise BuildError("registry 中没有任何资产，拒绝生成空站点")

        out_dir.mkdir(parents=True, exist_ok=True)
        # 归属标记**尽早**写入：万一后续步骤失败，这个半成品目录仍会被认作
        # 「本脚本的产物」，下次运行可直接复用，不必人工清理（见 _assert_safe_out_dir）
        (out_dir / _BUILD_MARKER).write_text(
            "workbuddy-hub site build artifact; safe to delete\n", encoding="utf-8"
        )

        warnings, errors = prepare_avatars(items, out_dir, not args.no_avatars)
        warnings = build_warnings + warnings

        stats = {
            "experts": sum(1 for i in items if i["type"] == "expert"),
            "teams": sum(1 for i in items if i["type"] == "team"),
            "skills": len(skills),
        }

        if not TEMPLATE_PATH.is_file():
            raise BuildError(f"缺少页面模板：{TEMPLATE_PATH}")
        tokens = {
            "stats_experts": stats["experts"],
            "stats_teams": stats["teams"],
            "stats_skills": stats["skills"],
            "total": len(items),
            "category_chips": render_category_chips(active_categories),
            "cards": render_cards(items),
            "repo_url": _esc(args.repo_url.rstrip("/")),
            "site_url": _esc(args.site_url),
        }
        page = render_template(TEMPLATE_PATH.read_text(encoding="utf-8"), tokens)

        (out_dir / "index.html").write_text(page, encoding="utf-8")
        (out_dir / ".nojekyll").write_text("", encoding="utf-8")

        # 新产物已全部落盘，此时才清理旧头像（先写后删，见 _prune_stale_avatars）
        warnings += _prune_stale_avatars(
            out_dir, {Path(it["avatar"]).stem for it in items if it["avatar"]}
        )

    except (BuildError, OSError) as exc:
        # OSError 一并兜住：任何文件系统异常（超长名、权限、只读挂载）都应
        # 以「干净失败」收场（退出码 1 + 一行错误），而不是抛 Python 栈。
        print(f"✗ {exc}", file=sys.stderr)
        return 1

    # 错误必须无条件可见：--quiet 只压制进度信息，不能把失败伪装成成功
    for e in errors:
        print(f"  ✗ {e}", file=sys.stderr)

    if not args.quiet:
        size_kb = len(page.encode("utf-8")) / 1024
        mark = "⚠" if errors else "✓"
        print(
            f"{mark} 站点已生成：{out_dir}\n"
            f"  专家 {stats['experts']} · "
            f"专家团 {stats['teams']} · "
            f"技能 {stats['skills']}\n"
            f"  分类 {len(active_categories)} 个 · "
            f"卡片 {len(items)} 张 · "
            f"index.html {size_kb:.1f} KB"
        )
        for w in warnings:
            print(f"  ⚠ {w}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
