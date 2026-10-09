# 资产生命周期

一个能力资产从诞生到退役，经历以下阶段。每阶段对应的仓库动作已标注。

## 1. 创建（create）

- 复制 `templates/<类型>/` 到对应 bucket，目录名 = 资产 ID。
- 替换占位 ID，填写 `plugin.json` / `SKILL.md` / `agents/*.md`。
- 脚本：`import_asset.py`（若是外部 zip/目录）或手动复制模板。

## 2. 开发（develop）

- 编写技能正文、专家人格、协作流程。
- 在仓库内即可用 WorkBuddy 加载调试（专家管理技能可注册本地目录）。

## 3. 元数据同步（sync）

- 跑 `sync_manifests.py` 生成/刷新 `manifest.yaml`。
- 这一步保证索引层始终反映最新定义。

## 4. 校验（validate）

- 跑 `validate.py`：manifest 通过 `schemas/*.json` 校验 + 结构检查（SKILL.md / plugin.json / agents/ 齐备）。
- 跑 `build_registry.py`：生成全局索引 + 引用完整性检查。

## 5. 打包与发布（package → publish）

- 用专家管理技能（`expert-manager`）从 bucket 目录打包成 open.workbuddy.cn 可上传的 zip。
- 上架的是**副本**，本地仓库不受影响；每次发版改本地 → 重新 sync → 重新打包 → 上传。
- 各资产上架卡点与流程见 `docs/operations/`。

## 6. 维护（maintain）

- 改内容优先改原生文件，再跑 sync + build + validate。
- 版本号随改动递增，`CHANGELOG.md` 记录。

## 7. 弃用（deprecate）

- 不要直接删除资产目录。先把 `manifest.yaml` 的 `status` 置为 `deprecated`，保留一段时间便于回溯。
- 确认无人引用后，再移入 `archive/` 并说明原因。

## 状态机

```
draft ──▶ active ──▶ deprecated ──▶ (archive)
            │            │
            └────────────┘  （active 与 deprecated 可互转）
```

> 注意：`draft` 资产仍可本地调试，但 `build_registry.py` 会在索引中如实标记，不会自动上架。
