"""WorkBuddy Hub 管理工具共享库。

集中放置资产类型识别、包根定位、原生元数据读取等通用逻辑，
供 import_asset / sync_manifests / build_registry / validate 复用。
"""
from __future__ import annotations

import json
import re
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent  # .../dist（即 workbuddy-hub 仓库根）
BUCKETS = {
    "skill": REPO_ROOT / "skills",
    "expert": REPO_ROOT / "experts",
    "team": REPO_ROOT / "teams",
}
SCHEMA_FOR = {
    "skill": "skill.schema.json",
    "expert": "expert.schema.json",
    "team": "team.schema.json",
}

# WorkBuddy 平台类目 ID → Hub 分类
CATEGORY_ID_MAP = {
    "02-Engineering": "development",
    "04-DataAI": "research",
    "06-ContentCreative": "content",
}
# Skill frontmatter 的 category 字符串 → Hub 分类
SKILL_CATEGORY_MAP = {
    "development-tools": "development",
    "productivity-tools": "other",
    "knowledge-learning": "research",
    "content-creation": "content",
    "design-tools": "design",
    "business-tools": "business",
}


def detect_type(root: Path) -> str | None:
    """根据目录内容判断资产类型：team / expert / skill / None。"""
    pj = root / ".codebuddy-plugin" / "plugin.json"
    if pj.exists():
        try:
            data = json.loads(pj.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        return "team" if data.get("expertType") == "team" else "expert"
    if (root / "SKILL.md").exists():
        return "skill"
    return None


def find_package_root(path: Path) -> Path | None:
    """给定 zip 或目录，返回真正包含资产定义的包根目录。

    - zip：解包到临时目录后，找到含 .codebuddy-plugin 或 SKILL.md 的那一层（处理「外层多套一层」的情况）。
    - 目录：若自身就是包则返回自身；否则在其子目录中寻找。
    """
    if path.is_file() and zipfile.is_zipfile(str(path)):
        tmp = Path(tempfile.mkdtemp(prefix="hub_import_"))
        with zipfile.ZipFile(str(path)) as z:
            z.extractall(tmp)
        for p in sorted(tmp.rglob("*")):
            if p.is_dir() and detect_type(p):
                return p
        subs = [d for d in tmp.iterdir() if d.is_dir()]
        return subs[0] if len(subs) == 1 else tmp
    if path.is_dir():
        if detect_type(path):
            return path
        for sub in sorted(path.iterdir()):
            if sub.is_dir() and detect_type(sub):
                return sub
    return None


def load_plugin_json(root: Path) -> dict | None:
    pj = root / ".codebuddy-plugin" / "plugin.json"
    if pj.exists():
        try:
            return json.loads(pj.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"无法解析 {pj}: {e}")
    return None


_FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def load_skill_frontmatter(root: Path) -> dict:
    sk = root / "SKILL.md"
    if not sk.exists():
        return {}
    text = sk.read_text(encoding="utf-8")
    m = _FRONT_RE.match(text)
    if not m:
        return {}
    try:
        import yaml

        return yaml.safe_load(m.group(1)) or {}
    except Exception:  # noqa: BLE001
        return {}


def load_manifest(root: Path) -> dict | None:
    m = root / "manifest.yaml"
    if m.exists():
        try:
            import yaml

            return yaml.safe_load(m.read_text(encoding="utf-8")) or {}
        except Exception:  # noqa: BLE001
            return None
    return None


def _zh(d, key, default=""):
    v = d.get(key)
    if isinstance(v, dict):
        return v.get("zh") or v.get("en") or default
    return v or default


def get_meta(root: Path, atype: str | None = None) -> tuple[dict, str]:
    """返回归一化后的资产元数据字典与类型。

    优先读取 manifest.yaml；若不存在则从原生文件（plugin.json / SKILL.md）推导。
    返回 dict 含 '_source' 标记来源。
    """
    atype = atype or detect_type(root)
    if atype is None:
        raise RuntimeError(f"无法识别资产类型：{root}")
    man = load_manifest(root)
    if man and isinstance(man, dict) and man.get("id"):
        meta = dict(man)
        meta["_source"] = "manifest.yaml"
        return meta, atype

    # 从原生文件推导
    if atype == "skill":
        fm = load_skill_frontmatter(root)
        meta = {
            "id": fm.get("name"),
            "name": fm.get("display_name") or fm.get("name"),
            "version": str(fm.get("version", "1.0.0")),
            "type": "skill",
            "description": fm.get("description") or fm.get("description_zh") or "",
            "category": SKILL_CATEGORY_MAP.get(fm.get("category"), "other"),
            "tags": [],
            "status": "active",
        }
    else:  # expert / team
        pj = load_plugin_json(root) or {}
        name = _zh(pj, "displayName", pj.get("name")) or pj.get("name")
        description = _zh(pj, "displayDescription", pj.get("description"))
        tags = [t.get("zh") or t.get("en") for t in pj.get("tags", []) if isinstance(t, dict)]
        category = CATEGORY_ID_MAP.get(pj.get("categoryId"), "other")
        if atype == "expert":
            skills = [Path(s).name for s in pj.get("skills", [])]
            meta = {
                "id": pj.get("name"),
                "name": name,
                "version": str(pj.get("version", "1.0.0")),
                "type": "expert",
                "expert_type": pj.get("expertType", "agent"),
                "description": description,
                "category": category,
                "skills": skills,
                "tags": tags,
                "status": "active",
                "platform_category": pj.get("categoryId"),
            }
        else:  # team
            members = []
            for a in pj.get("agents", []):
                aid = Path(a).stem
                if "team-lead" in aid:
                    role, embedded = "coordinator", True
                else:
                    role, embedded = "member", True
                members.append({"expert_id": aid, "role": role, "embedded": embedded})
            nm = pj.get("name", "")
            meta = {
                "id": nm,
                "name": name,
                "version": str(pj.get("version", "1.0.0")),
                "type": "team",
                "description": description,
                "category": category,
                "members": members,
                "workflow": f"agents/{nm}-team-lead.md" if nm else "",
                "tags": tags,
                "status": "active",
                "platform_category": pj.get("categoryId"),
            }
    meta["_source"] = "native"
    return meta, atype


def iter_assets():
    """遍历三个 bucket，产出 (root, meta, atype) 三元组。"""
    for atype, bucket in BUCKETS.items():
        if not bucket.exists():
            continue
        for root in sorted(bucket.iterdir()):
            if not root.is_dir() or root.name.startswith("."):
                continue
            try:
                meta, t = get_meta(root, atype)
            except Exception:  # noqa: BLE001
                continue
            yield root, meta, t
