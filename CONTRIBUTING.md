# 贡献指南（资产新增与修改规范）

本仓库统一管理 WorkBuddy 的 Skills / Experts / Teams。请按以下规范操作，保证脚本与索引始终可用。

## 1. 新增资产

1. **用模板起步**：复制 `templates/<类型>/` 到 `skills/`、`experts/` 或 `teams/` 下，目录名 = 资产 ID（kebab-case）。
2. **替换占位 ID**：把 `your-skill-id` / `your-expert-id` / `your-team-id` 等全局替换为真实 ID，且与 `plugin.json` 的 `name`、`agentName`、`plugin` 三处一致（专家/团队严格要求一致）。
3. **填内容**：
   - Skill：在 `SKILL.md` 写 frontmatter + 正文，按需放 `references/`、`scripts/`、`assets/`、`evals/`。
   - Expert/Team：填 `plugin.json`、`agents/*.md`、头像（`avatars/`），Team 还需 `settings.json`（`{"agent": "<team-id>-team-lead"}`）。
4. **生成元数据并校验**：
   ```bash
   python scripts/sync_manifests.py --force
   python scripts/build_registry.py
   python scripts/validate.py
   ```
5. 提交前确认 `registry/` 已刷新、无校验报错。

## 2. 修改资产

- 改内容优先改 WorkBuddy 原生文件（`SKILL.md` / `plugin.json` / `agents/*.md`）。
- 改完跑一遍 `sync_manifests.py --force` + `build_registry.py` + `validate.py`，保证 manifest 与索引同步。
- 改了 `version` 记得同步 `plugin.json` 与（如有）`manifest.yaml`，并在 `CHANGELOG.md` 记录。

## 3. 命名与分类

- ID 一律 kebab-case（`market-research`、`deep-research-crew`），全局唯一。
- 分类从 `research / development / content / design / business / other` 中选一个，写入 manifest 的 `category`，并与 `plugin.json` 的 `categoryId` 对齐（映射见 `scripts/_hublib.py` 的 `CATEGORY_ID_MAP`）。

## 4. 状态

- 资产 `status`：`active`（在用）/ `draft`（草稿）/ `deprecated`（弃用）。弃用资产不要直接删除，先置 `deprecated`。

## 5. 上架

- 上架到 open.workbuddy.cn 的是**副本**：在 bucket 内用专家管理技能打包后上传，本地不受影响。
- 上架流程与卡点见 `docs/operations/` 下的各资产上架指引。

## 6. 提交信息

- 推荐前缀：`feat(asset)` / `fix(asset)` / `chore(hub)` / `docs(hub)`。
- 一次提交尽量只动一个资产或一个脚本，便于回溯。
