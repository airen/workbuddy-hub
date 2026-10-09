# 真实示例：PR 正文

> 本示例由 `pr` 技能（`skills/pr`）的模板产出。素材取自本仓库一次真实提交
> （commit `0a791cf`：examples 改造 + 全量资产迁移），
> 展示模板三段（Summary / Evidence / Merge Danger）如何填写。

---

## Summary

把 `examples/` 从空骨架改造成基于仓库真实资产的使用示例，并完成首次 GitHub 推送。

调用树：

```text
examples 改造
├── single-skill/      # skills/pr 自身的用法示例
├── single-expert/     # experts/lao-dao-editor（内部编排 de-ai-rewrite）
├── expert-team/       # teams/engineering-delivery（六阶段 + G1–G4 门禁）
└── skill-chain/       # to-spec → to-tickets → implement
```

## Evidence

- **Before:** `examples/single-skill/`、`single-expert/`、`expert-team/` 三个目录为空
  （`ls -la` 只显示 `.` 和 `..`）；README 自承「当前阶段尚未填充独立示例」
  **After:** 四个示例目录各含一份 README + 一份真实产物文件；
  `examples/README.md` 有一览表，且与 `registry/*.yaml` 的 46 个资产对得上
- **Before:** `main` 分支只存在于本地，remote 无 `main`
  **After:** `git ls-remote` 返回 `0a791cf... refs/heads/main`，与本地 HEAD 一致
- 测试：`python scripts/validate.py` 46/46 通过；`build_registry.py` 0 错误

## Merge Danger

**Door:** 双向门（文档与示例，无运行时行为，可 revert）

**Blast Radius:** 仅文档层——`examples/`、`README.md`、`docs/`；
不影响 `skills/`、`experts/`、`teams/` 中任何资产的实际定义。
