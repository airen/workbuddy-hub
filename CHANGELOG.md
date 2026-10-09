# Changelog

本文件记录 workbuddy-hub 项目级变更（资产层面变更请在各资产内或 PR 中说明）。

## [unreleased]

### 2026-10-09 — 仓库初始化与结构重构
- 按 `资产定义层 + 组合层 + 管理工具层` 思路建立 workbuddy-hub 骨架：
  `skills/`、`experts/`、`teams/`、`registry/`、`schemas/`、`templates/`、`scripts/`、`tests/`、`docs/`、`examples/`、`archive/`、`.github/`。
- 迁移核心自研资产：
  - 专家（8）：lao-dao-editor、agent-memory-advisor、engineering-review-board、self-media-studio、spec-driven-dev、diagram-architect、doc-memory-steward、software-architect
  - 专家团（3）：engineering-delivery、deep-research-crew、hai-stack
  - 技能（4）：de-ai-rewrite、agent-doc-memory、ai-project-pilot、ui-design-field-manual
- 编写管理工具：`import_asset.py`、`sync_manifests.py`、`build_registry.py`、`validate.py`，及 `schemas/*.json`。
- 归档非核心/第三方资产（mattpocock-skills、creator-ops、media-content-team 等）至 `archive/`，不进入 registry。
- 上架指引与安装报告归入 `docs/operations/`。
