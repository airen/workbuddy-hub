# WorkBuddy 兼容性说明

本仓库刻意**不**发明一套与平台冲突的资产格式，而是直接复用 WorkBuddy 的原生打包格式，只在根目录附加一个派生的 `manifest.yaml`。

## 平台原生格式（权威）

| 类型 | 必须文件 | 说明 |
|---|---|---|
| Skill | `SKILL.md`（含 YAML frontmatter） | frontmatter 的 `name`/`description`/`version`/`category` 即权威元数据 |
| Expert（agent） | `.codebuddy-plugin/plugin.json` + `agents/<id>.md` + `avatars/` | `plugin.json` 的 `name`/`plugin`/`agentName` 三处一致 |
| Team | 同上 + `settings.json`（`{"agent":"<id>-team-lead"}`） + 多个 `agents/*.md` | `expertType: "team"` |

平台读取的就是这些文件；上传 zip 时**第一层必须是资产目录**，不能多套一层。

## hub 派生元数据（非权威，可自动生成）

- `manifest.yaml`：每个资产根目录一个，字段见 `schemas/*.json`。由 `sync_manifests.py` 从原生文件推导，**不要手写维护**。
- `registry/*.yaml`：全局索引，由 `build_registry.py` 聚合所有 manifest 生成。

## 字段映射（原生 → manifest）

`scripts/_hublib.py` 负责：

- Expert/Team 的展示名 ← `plugin.json.displayName.zh`
- 描述 ← `plugin.json.displayDescription.zh`
- 标签 ← `plugin.json.tags[].zh`
- 分类 ← `plugin.json.categoryId` 按 `CATEGORY_ID_MAP` 映射到 hub 枚举
- 专家技能列表 ← `plugin.json.skills[]` 的目录名
- 团队成员 ← `plugin.json.agents[]` 的文件名（`team-lead` → `coordinator`）
- Skill 的展示名/描述/分类 ← `SKILL.md` frontmatter

## 平台「不支持」、属于 hub 内部规范的字段

以下字段**不是 WorkBuddy 原生字段**，仅由 hub 自定义并校验，请勿假设平台会读取：

- `manifest.yaml` 整体（平台不读它）
- `id`（hub 用；平台用的是 `plugin.json.name`）
- `category`（hub 枚举；平台用的是 `categoryId` 如 `02-Engineering`）
- `status`（active/draft/deprecated，hub 内部生命周期标记）
- `tags` 在 manifest 中是扁平字符串列表；平台 `tags` 是 `[{zh,en}]` 对象数组

> 因此：**改了 `plugin.json` / `SKILL.md` 后务必跑 `sync_manifests.py --force`**，否则 hub 索引会与平台实际内容脱节。

## 未来：package.py

推荐结构里提到 `scripts/package.py`（打包导出为平台可识别的分发包）。当前版本先实现 `import_asset.py` / `sync_manifests.py` / `build_registry.py` / `validate.py`；`package.py` 作为后续增强，将复用 `expert-manager` 的打包逻辑把 bucket 目录转成上传 zip。
