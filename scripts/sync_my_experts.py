#!/usr/bin/env python3
"""
Multi-root sync: keep every local WorkBuddy app's "我的专家" in sync with the
workbuddy-hub catalog.

Background
----------
WorkBuddy keeps a per-app data root, and more than one app can coexist on the same
machine (e.g. `~/.workbuddy-ai` for WorkBuddy AI and `~/.workbuddy` for the older
WorkBuddy). The two never talk to each other: each registers its own `my-experts`
directory marketplace. This script syncs the catalog into every root it is given
(or auto-discovers).

For every expert/team in registry/experts.yaml + registry/teams.yaml, and for
every target root, ensure:
  1. Installed as a plugin under
     <root>/plugins/marketplaces/my-experts/plugins/<id>/
     (copies the package from experts/ or teams/ as-is; the package already
     carries its own .codebuddy-plugin/plugin.json)
  2. Listed in the whitelist
     <root>/experts/custom/<uid>/experts.json
  3. Listed as a recents entry in
     <root>/storage/user-<uid>-personal/global/expert.json
  4. Listed in the marketplace index
     <root>/plugins/marketplaces/my-experts/.codebuddy-plugin/marketplace.json
  5. `my-experts` registered in <root>/plugins/known_marketplaces.json
  6. For plugins ALREADY installed, the app loads them from a **version-keyed cache**
     <root>/plugins/cache/my-experts/<id>/<version>/
     recorded in <root>/plugins/installed_plugins.json. Bumping a package version
     without refreshing this cache makes the app fail with
     "解析失败：未找到 .codebuddy-plugin/plugin.json". Step 6 refreshes
     already-installed plugins only — it never installs a new one for the user.

Target roots are resolved in this order:
  1. `--root PATH` (repeatable) — use exactly these
  2. `$WORKBUDDY_ROOTS` (os.pathsep-separated) — use exactly these
  3. auto-discovery — every `~/.workbuddy*` directory that looks like a data root

Install is ADD-ONLY and idempotent by default: existing plugins are never
overwritten (matching the "never destroy the user's manual state" principle).
Pass `--update` to also re-copy marketplace packages whose version differs from
the repo — that is what a one-off backfill / upgrade run should use. Pass
`--force` to re-copy every package (and its version-keyed cache) unconditionally,
regardless of version — use it to repair content drift when a package was edited
without a version bump. To force a single package to be regenerated, delete its
folder under the marketplace and re-run (with or without `--update`).

Pass `--install-missing <id>` to repair the "marketplace has it, whitelist has it,
but installed_plugins.json doesn't" deadlock: that state arises when a package's
version-keyed cache folder is deleted by hand, which makes the app drop its
installed record too — and neither `install_plugin()` (ADD-ONLY) nor
`sync_plugin_cache()` (registered-only) will re-create it. This flag re-copies the
marketplace package into the cache and re-registers it. It takes an explicit id
(repeatable) because "in marketplace + whitelist" does NOT mean "installed by the
user" — the marketplace lists the whole catalog — so auto-detection would
mass-install dozens of plugins the user never added.

Triggered on-demand by the agent when a new expert/team is created, or when a
root is noticed to have drifted. No scheduled cron (to avoid spending credits).
"""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

HOME = Path(os.environ.get("HOME", os.path.expanduser("~")))
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = Path(os.environ.get("WORKSPACE", SCRIPT_DIR.parent))
REGISTRY = WORKSPACE / "registry"

MARKETPLACE_NAME = "my-experts"
AUTHOR = {"name": "大漠", "email": "damo@example.com"}

# Set by --dry-run. All writes funnel through the helpers below so a dry run
# performs no filesystem mutation.
DRY = False


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, data):
    if DRY:
        print(f"      [dry] write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _copy_tree(src: Path, dst: Path):
    if DRY:
        print(f"      [dry] copy {src} -> {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def _rmtree(path: Path):
    if DRY:
        print(f"      [dry] rm -rf {path}")
        return
    shutil.rmtree(path)


def _read_version(plugin_json: Path):
    data = _read_json(plugin_json, None)
    return data.get("version") if isinstance(data, dict) else None


class Root:
    """One WorkBuddy app data root, e.g. ``~/.workbuddy-ai`` or ``~/.workbuddy``."""

    def __init__(self, base: Path):
        self.base = base
        self.marketplace = base / "plugins" / "marketplaces" / MARKETPLACE_NAME
        self.plugins_dir = self.marketplace / "plugins"
        self.cache_root = base / "plugins" / "cache" / MARKETPLACE_NAME
        self.installed_path = base / "plugins" / "installed_plugins.json"
        self.known_marketplaces_path = base / "plugins" / "known_marketplaces.json"
        self.custom_root = base / "experts" / "custom"
        self.storage = base / "storage"
        self.uid = None
        self.whitelist_path = None
        self.recents_path = None

    def looks_like_data_root(self) -> bool:
        return (self.base / "plugins" / "marketplaces").is_dir() or self.custom_root.is_dir()

    def detect_uid(self) -> bool:
        override = os.environ.get("WORKBUDDY_UID")
        if override:
            self.uid = override
        elif self.custom_root.exists():
            subs = sorted(p for p in self.custom_root.iterdir() if p.is_dir())
            if not subs:
                return False
            self.uid = subs[0].name
        else:
            return False
        self.whitelist_path = self.custom_root / self.uid / "experts.json"
        self.recents_path = self.storage / f"user-{self.uid}-personal" / "global" / "expert.json"
        return True

    def label(self) -> str:
        return str(self.base)


def discover_roots(args) -> list:
    if args.root:
        cands = [Path(p).expanduser() for p in args.root]
    elif os.environ.get("WORKBUDDY_ROOTS"):
        cands = [Path(p).expanduser() for p in os.environ["WORKBUDDY_ROOTS"].split(os.pathsep) if p.strip()]
    else:
        cands = sorted(p for p in HOME.glob(".workbuddy*") if p.is_dir())

    roots = []
    for c in cands:
        r = Root(c)
        if not r.looks_like_data_root():
            print(f"[sync] skip {c} (not a WorkBuddy data root)")
            continue
        if not r.detect_uid():
            print(f"[sync] skip {c} (no custom-experts uid found)")
            continue
        roots.append(r)
    return roots


def load_yaml(path: Path):
    if yaml is not None:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {}


def collect_catalog() -> dict:
    out: dict = {}
    for fname, kind in [("experts.yaml", "experts"), ("teams.yaml", "teams")]:
        p = REGISTRY / fname
        if not p.exists():
            continue
        data = load_yaml(p)
        for item in data.get(kind, []) or []:
            iid = item.get("id")
            if iid:
                out[iid] = {"kind": kind[:-1], "registry_entry": item}
    return out


def resolve_avatar(manifest_dir: Path, expert_id: str):
    av_dir = manifest_dir / "avatars"
    if not av_dir.exists():
        return None
    for c in [expert_id + ext for ext in (".jpg", ".png", ".jpeg")]:
        if (av_dir / c).exists():
            return f"avatars/{c}"
    for c in ["team.jpg", "team.png"]:
        if (av_dir / c).exists():
            return f"avatars/{c}"
    imgs = sorted([p for p in av_dir.iterdir() if p.suffix.lower() in (".jpg", ".png", ".jpeg", ".webp")])
    return f"avatars/{imgs[0].name}" if imgs else None


def resolve_team_lead_avatar(manifest_dir: Path, expert_id: str):
    av_dir = manifest_dir / "avatars"
    if not av_dir.exists():
        return None
    for ext in (".jpg", ".png", ".jpeg"):
        c = f"{expert_id}-team-lead{ext}"
        if (av_dir / c).exists():
            return f"avatars/{c}"
    return None


def resolve_agent(manifest_dir: Path, expert_id: str, kind: str) -> str:
    ag_dir = manifest_dir / "agents"
    if not ag_dir.exists():
        return ""
    if kind == "team":
        for c in [f"{expert_id}-team-lead.md", f"{expert_id}.md"]:
            if (ag_dir / c).exists():
                return c
    c = f"{expert_id}.md"
    if (ag_dir / c).exists():
        return c
    md = sorted(ag_dir.glob("*.md"))
    return md[0].name if md else ""


def build_plugin_json(eid: str, kind: str, manifest: dict) -> dict:
    """Legacy helper: synthesise a plugin.json from a registry entry.

    Kept for reference / external callers. The normal install path copies the
    package's own .codebuddy-plugin/plugin.json verbatim and does not use this.
    """
    name = manifest.get("name", eid)
    desc = manifest.get("description", "")
    version = manifest.get("version", "1.0.0")
    tags = manifest.get("tags", [])
    skills = manifest.get("skills", [])
    mdir = WORKSPACE / ("teams" if kind == "team" else "experts") / eid

    display_name = name
    profession = name  # workspace manifests lack a separate role field

    agents_rel = []
    ag = resolve_agent(mdir, eid, kind)
    if ag:
        agents_rel.append(f"./agents/{ag}")
    for member in (manifest.get("members") or []):
        meid = member.get("expert_id")
        if meid and (mdir / "agents" / f"{meid}.md").exists():
            agents_rel.append(f"./agents/{meid}.md")

    skills_rel = [f"./skills/{s}" for s in skills if (mdir / "skills" / s).exists()]

    avatar = resolve_avatar(mdir, eid)
    assistant_avatar = resolve_team_lead_avatar(mdir, eid) if kind == "team" else avatar

    pj = {
        "name": eid,
        "version": version,
        "description": desc,
        "author": AUTHOR,
        "agents": agents_rel,
        "skills": skills_rel,
        "expertType": "team" if kind == "team" else "agent",
        "agentName": (f"{eid}-team-lead" if kind == "team" else eid),
        "displayName": {"en": eid, "zh": display_name},
        "profession": {"en": eid, "zh": profession},
        "displayDescription": {"en": desc, "zh": desc},
        "defaultInitPrompt": {"zh": f"带我了解一下 {display_name} 能帮你做什么", "en": f"Show me what {display_name} can do for me"},
        "plugin": eid,
        "tags": [{"en": t, "zh": t} for t in tags],
    }
    if avatar:
        pj["avatar"] = avatar
        pj["assistantAvatar"] = assistant_avatar or avatar
    if kind == "team":
        pj["teamMembers"] = [
            {"agentName": m.get("expert_id"), "role": m.get("role", "member")}
            for m in (manifest.get("members") or [])
        ]
    return pj


def install_plugin(root: Root, eid: str, kind: str, manifest: dict, update: bool, force: bool = False):
    """Copy the workspace package into the root's marketplace.

    Returns (status, detail) where status is one of
    installed / updated / refreshed / up-to-date / skipped / ERROR.
    """
    target = root.plugins_dir / eid
    src = WORKSPACE / ("teams" if kind == "team" else "experts") / eid
    if not src.exists():
        return "ERROR", f"source package missing at {src}"

    if not target.exists():
        _copy_tree(src, target)
        return "installed", None

    if force:
        _rmtree(target)
        _copy_tree(src, target)
        return "refreshed", "forced re-copy"

    if not update:
        return "skipped", None

    src_ver = _read_version(src / ".codebuddy-plugin" / "plugin.json")
    tgt_ver = _read_version(target / ".codebuddy-plugin" / "plugin.json")
    if src_ver is not None and src_ver == tgt_ver:
        return "up-to-date", None
    _rmtree(target)
    _copy_tree(src, target)
    return "updated", f"{tgt_ver} -> {src_ver}"


def _id_exists_anywhere(root: Root, eid: str) -> bool:
    """True if <eid> is present in ANY marketplace or cache under this root."""
    mk_root = root.base / "plugins" / "marketplaces"
    if mk_root.exists():
        for mk in mk_root.glob("*/plugins"):
            if (mk / eid).exists():
                return True
    ck_root = root.base / "plugins" / "cache"
    if ck_root.exists():
        for ck in ck_root.glob("*"):
            if (ck / eid).exists():
                return True
    return False


def sync_whitelist(root: Root, catalog_ids: set, prune_orphans: bool = False):
    current = _read_json(root.whitelist_path, [])
    if not isinstance(current, list):
        current = []
    added = sorted(catalog_ids - set(current))
    merged = current + added

    removed = []
    if prune_orphans:
        keep = []
        for eid in merged:
            if eid in catalog_ids or _id_exists_anywhere(root, eid):
                keep.append(eid)
            else:
                removed.append(eid)
        merged = keep

    if added or removed:
        _write_json(root.whitelist_path, merged)
    return len(current), added, removed


def build_recents_entry(root: Root, eid: str, pj: dict) -> dict:
    local_path = str(root.plugins_dir / eid)
    dn = pj.get("displayName") or {}
    prof = pj.get("profession") or {}
    dip = pj.get("defaultInitPrompt") or {}
    avatar_rel = pj.get("avatar")
    asst_avatar_rel = pj.get("assistantAvatar")
    name_zh = dn.get("zh") or dn.get("en") or eid
    return {
        "id": eid,
        "name": name_zh if pj.get("expertType") == "team" else eid,
        "profession": prof.get("zh") or prof.get("en") or name_zh,
        "avatarUrl": f"local-file://local/{local_path}/{avatar_rel}" if avatar_rel else None,
        "defaultInitPrompt": dip.get("zh") or dip.get("en") or pj.get("description", ""),
        "version": pj.get("version", "1.0.0"),
        "pluginName": eid,
        "expertType": pj.get("expertType", "agent"),
        "agentName": pj.get("agentName", eid),
        "localPath": local_path,
        "marketplace": MARKETPLACE_NAME,
        "source": "custom",
        "assistantDisplayName": name_zh,
        "assistantProfession": prof.get("zh") or prof.get("en") or name_zh,
        "assistantAvatarUrl": f"local-file://local/{local_path}/{asst_avatar_rel}" if asst_avatar_rel else None,
    }


def sync_recents(root: Root, catalog_ids: set):
    data = _read_json(root.recents_path, None)
    if not isinstance(data, dict):
        return 0, []
    recents = data.get("recents", [])
    if not isinstance(recents, list):
        return 0, []
    existing_ids = {e.get("id") for e in recents}
    added = []
    for eid in sorted(catalog_ids - existing_ids):
        pj = _read_json(root.plugins_dir / eid / ".codebuddy-plugin" / "plugin.json", None)
        if not isinstance(pj, dict):
            # Not installed yet (e.g. catalog entry without a workspace package); skip.
            continue
        recents.append(build_recents_entry(root, eid, pj))
        added.append(eid)
    if added:
        data["recents"] = recents
        _write_json(root.recents_path, data)
    return len(recents), added


def sync_marketplace_index(root: Root, catalog_ids: set):
    """The '我的专家' UI reads the plugin list from the marketplace index
    (marketplace.json), not from the filesystem directly. New plugins must be
    listed here to show up."""
    mp = root.marketplace / ".codebuddy-plugin" / "marketplace.json"
    data = _read_json(mp, None)
    if not isinstance(data, dict):
        return None, None, []
    plugins = data.get("plugins", [])
    before = len(plugins)
    existing = {p.get("name") for p in plugins}
    added = []
    for eid in sorted(catalog_ids - existing):
        pj = _read_json(root.plugins_dir / eid / ".codebuddy-plugin" / "plugin.json", None)
        desc = pj.get("description", "") if isinstance(pj, dict) else ""
        plugins.append({"name": eid, "source": f"./plugins/{eid}", "description": desc})
        added.append(eid)
    if added:
        data["plugins"] = plugins
        _write_json(mp, data)
    return before, len(plugins), added


def ensure_marketplace_registered(root: Root) -> str:
    """Make sure this root's known_marketplaces.json lists my-experts (additive)."""
    data = _read_json(root.known_marketplaces_path, None)
    if not isinstance(data, dict):
        return "no known_marketplaces.json (skipped)"
    if MARKETPLACE_NAME in data:
        return "already registered"
    data[MARKETPLACE_NAME] = {
        "manifestName": MARKETPLACE_NAME,
        "type": "directory",
        "source": {"source": "directory", "path": str(root.marketplace)},
        "installLocation": str(root.marketplace),
        "description": f"Marketplace from {root.marketplace}",
        "lastUpdated": _now(),
        "autoUpdate": False,
    }
    _write_json(root.known_marketplaces_path, data)
    return "registered"


def sync_plugin_cache(root: Root, catalog_ids: set, force: bool = False):
    """把「已安装」插件的缓存副本刷新到当前声明版本。

    背景：app 按 <cache>/my-experts/<id>/<version>/ 分目录加载插件，
    并把这个 installPath 记在 plugins/installed_plugins.json 里。
    一旦市场里的 plugin.json 改了版本号，旧缓存目录就对不上，app 会报
    「解析失败：未找到 .codebuddy-plugin/plugin.json，请确保该路径文件存在」。

    本步骤只补齐**已经登记在 installed_plugins.json 里的**插件，
    不替用户安装新插件（安装仍由 app 或显式操作触发）。
    force=True 时连缓存目录也强制重拷，用于修复「改了内容但没升版本号」的漂移。
    """
    data = _read_json(root.installed_path, None)
    if not isinstance(data, dict):
        return 0, []
    plugins = data.get("plugins", {})
    if not isinstance(plugins, dict):
        return 0, []
    updated = []
    for eid in sorted(catalog_ids):
        entries = plugins.get(f"{eid}@{MARKETPLACE_NAME}")
        if not entries:
            continue  # 未安装 —— 跳过，不替用户安装
        src = root.plugins_dir / eid
        ver = _read_version(src / ".codebuddy-plugin" / "plugin.json")
        if not ver:
            continue
        dest = root.cache_root / eid / ver
        changed = False
        if force and dest.exists():
            _rmtree(dest)
            changed = True
        if not dest.exists():
            _copy_tree(src, dest)
            changed = True
        entry = entries[0]
        if entry.get("version") != ver or entry.get("installPath") != str(dest):
            entry["version"] = ver
            entry["installPath"] = str(dest)
            changed = True
        if changed:
            entry["lastUpdated"] = _now()
            updated.append(f"{eid} -> {ver}" + (" (forced)" if force else ""))
    if updated:
        _write_json(root.installed_path, data)
    return len(plugins), updated


def install_missing(root: Root, ids) -> tuple:
    """补装**明确指定**的插件：市场里有副本、但 installed_plugins.json 里没登记。

    为什么需要这一步（2026-10-12 实测踩到）：
      清理插件时若连 ``<cache>/my-experts/<id>`` 一起删了，app 会把
      ``installed_plugins.json`` 里的记录一并清掉。而 ``sync_plugin_cache()``
      明确「只刷新**已登记**的插件，不替用户安装新插件」，``install_plugin()``
      又是 ADD-ONLY（见市场目录已存在就 skipped）——于是形成死锁：
      市场有、白名单有、索引有，但插件没被「安装」，app 不加载。
      同步只会报 ``33 skipped`` + ``0 refreshed``，看不出异常。

    ⚠️ **为什么必须显式传 id，而不是「自动找出所有缺登记的」**：
      市场目录里放着**全部** catalog 条目（市场 = 可安装清单），白名单同样
      union 了全部条目。所以「在市场 + 在白名单」**并不等于**「用户装过」——
      按这个判据自动补装，会把用户从没安装过的几十个插件一次性全标成已装
      （2026-10-12 实测：两个根分别会被误装 24 / 23 个）。
      而「曾装过、缓存被手删」与「从未装过」在磁盘上**无法区分**（两者的
      cache 目录都不存在）。所以只能由调用方指名要修哪个 id。

    ``ids`` 是可迭代的插件 id；只处理同时满足「id 在 ids 里」且「市场副本
    存在且带 version」的项，其余安全跳过。返回 ``(补装数量, 明细列表)``。
    """
    data = _read_json(root.installed_path, None)
    if not isinstance(data, dict):
        return 0, []
    plugins = data.get("plugins")
    if not isinstance(plugins, dict):
        plugins = {}
        data["plugins"] = plugins

    done = []
    for eid in sorted(set(ids)):
        key = f"{eid}@{MARKETPLACE_NAME}"
        if plugins.get(key):
            continue  # 已登记 —— 交给 sync_plugin_cache() 处理
        src = root.plugins_dir / eid
        ver = _read_version(src / ".codebuddy-plugin" / "plugin.json")
        if not ver:
            continue  # 市场副本不存在或没有版本号，无从补装
        dest = root.cache_root / eid / ver
        if dest.exists():
            _rmtree(dest)
        _copy_tree(src, dest)
        plugins[key] = [{
            "scope": "user",
            "installPath": str(dest),
            "version": ver,
            "installedAt": _now(),
            "lastUpdated": _now(),
        }]
        done.append(f"{eid} -> {ver}")

    if done:
        _write_json(root.installed_path, data)
    return len(done), done


def main(argv=None) -> int:
    global DRY
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", action="append", metavar="PATH",
                    help="data root to sync (repeatable); overrides auto-discovery")
    ap.add_argument("--update", action="store_true",
                    help="re-copy marketplace packages whose version differs from the repo")
    ap.add_argument("--force", action="store_true",
                    help="re-copy every package and its cache unconditionally (repairs content drift without version bumps)")
    ap.add_argument("--prune-orphans", action="store_true",
                    help="drop whitelist ids that are neither in the catalog nor installed anywhere in that root")
    ap.add_argument("--install-missing", action="append", metavar="ID",
                    help="repair a plugin that is in the marketplace but missing from "
                         "installed_plugins.json (the 'app won't load it' deadlock). "
                         "Repeatable; pass the plugin id, e.g. --install-missing tuwen-forge. "
                         "Takes an explicit id on purpose: 'in marketplace + whitelist' does NOT "
                         "mean 'installed by the user', so auto-detecting would mass-install.")
    ap.add_argument("--dry-run", action="store_true",
                    help="print intended changes without writing anything")
    args = ap.parse_args(argv)
    DRY = args.dry_run

    catalog = collect_catalog()
    if not catalog:
        print(f"[sync] no catalog entries found under {REGISTRY}; aborting.")
        return 1

    roots = discover_roots(args)
    if not roots:
        print("[sync] no WorkBuddy data roots found; aborting.")
        return 1

    print(f"[sync] catalog entries: {len(catalog)}")
    print(f"[sync] roots ({len(roots)}): {', '.join(r.label() for r in roots)}")
    if DRY:
        print("[sync] DRY RUN — nothing will be written")

    catalog_ids = set(catalog.keys())
    rc = 0
    for root in roots:
        print("")
        print(f"[sync] === {root.label()} (uid {root.uid}) ===")
        print(f"[sync] marketplace registration: {ensure_marketplace_registered(root)}")

        installed, updated, refreshed, uptodate, skipped, errors = [], [], [], [], [], []
        for eid, info in catalog.items():
            status, detail = install_plugin(root, eid, info["kind"], info["registry_entry"],
                                            args.update, args.force)
            if status == "installed":
                installed.append(eid)
            elif status == "updated":
                updated.append(f"{eid} ({detail})")
            elif status == "refreshed":
                refreshed.append(eid)
            elif status == "up-to-date":
                uptodate.append(eid)
            elif status == "skipped":
                skipped.append(eid)
            else:
                errors.append(f"{eid}: {detail}")
        print(f"[sync] plugins: {len(installed)} installed, {len(updated)} updated, "
              f"{len(refreshed)} refreshed, {len(uptodate)} up-to-date, "
              f"{len(skipped)} skipped, {len(errors)} errors")
        for x in installed:
            print(f"  + {x}")
        for x in updated:
            print(f"  ~ {x}")
        for x in refreshed:
            print(f"  = {x}")
        for x in errors:
            print(f"  ! {x}")
        if errors:
            rc = 1

        before, added_w, removed_w = sync_whitelist(root, catalog_ids, args.prune_orphans)
        print(f"[sync] whitelist: {before} -> {before + len(added_w) - len(removed_w)} "
              f"(added {len(added_w)}, pruned {len(removed_w)})")
        for x in added_w:
            print(f"  + {x}")
        for x in removed_w:
            print(f"  - {x}")

        rec_before, added_r = sync_recents(root, catalog_ids)
        print(f"[sync] recents: now {rec_before} entries (added {len(added_r)})")

        idx_before, idx_after, added_i = sync_marketplace_index(root, catalog_ids)
        if idx_before is None:
            print("[sync] marketplace index: no marketplace.json (skipped)")
        else:
            print(f"[sync] marketplace index: {idx_before} -> {idx_after} (added {len(added_i)})")

        if args.install_missing:
            n_fix, fixed = install_missing(root, args.install_missing)
            print(f"[sync] install-missing: {n_fix} plugin(s) registered")
            for x in fixed:
                print(f"  + {x}")
            for want in args.install_missing:
                if not any(x.startswith(want + " ") for x in fixed):
                    print(f"  . {want}: 无需处理（已登记，或市场副本不存在）")

        n_inst, cache_updated = sync_plugin_cache(root, catalog_ids, args.force)
        print(f"[sync] plugin cache: {n_inst} installed plugins checked, {len(cache_updated)} refreshed")
        for x in cache_updated:
            print(f"  ~ {x}")

    print("")
    print("[sync] done. UI should reflect new entries after a refresh / app restart.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
