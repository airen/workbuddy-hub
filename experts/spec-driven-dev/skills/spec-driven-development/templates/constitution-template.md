<!--
SYNC IMPACT REPORT
==================
Version change: (template/unratified) → 1.0.0
Bump rationale: [说明本次建立/修订章程的理由]

Principles defined:
  I.   [原则名]
  II.  [原则名]
  ...

Added sections:
  - [章节名]

Templates reviewed for alignment:
  ✅ .specify/templates/plan-template.md — Constitution Check 关口
  ✅ .specify/templates/spec-template.md
  ✅ .specify/templates/tasks-template.md

Follow-up TODOs: [没有就写 none]
-->

# [项目名] 章程

[一段话说明这个项目是什么、章程管辖什么、对谁有约束力。]

## 核心原则

### I. [原则名]

[祈使句，用 MUST / MUST NOT。说清具体要求。]

**Rationale:** [为什么这条原则存在 —— 违反了会付出什么代价。]

### II. [原则名]

[要求]

**Rationale:** [理由]

### III. [原则名]

[要求]

**Rationale:** [理由]

<!-- 按需增加条款。建议 5–9 条，再多就没人记得住了。 -->

## [约束章节，如：安全与跨平台约束]

- [约束]
- [约束]

## [流程与质量关卡章节，如：开发流程与质量关卡]

- [分支命名、PR 要求、评审要求]

## 治理

本章程在与既有惯例冲突时优先。

- **效力**：原则 I–N 是**有约束力的关卡**。`plan.md` 的 `## Constitution Check` 段落必须对照它们评估；`analyze` 把与 MUST 的冲突视为 `CRITICAL`。违规的解决方式是**改规格、方案或任务**，不是稀释原则。
- **修订**：修改本文档需要 PR + 理由 + 维护者批准 + 按下方策略升版本号。任何修订必须**在同一次变更中**同步到依赖模板，并记录在上方 Sync Impact Report。
- **版本策略（治理的语义化版本）**：
  - `MAJOR` = 向后不兼容的治理变更，或原则被删除/重定义
  - `MINOR` = 新增原则/章节，或实质性扩充指导
  - `PATCH` = 澄清与非语义性打磨
- **合规评审**：每个 PR 与评审都必须核对合规性。新增复杂度或任何偏离**必须**在 PR 中论证（方案类则在 `plan.md` 的 Complexity Tracking 段）。**未经论证的违规阻断合并。**

**Version**: 1.0.0 | **Ratified**: [YYYY-MM-DD] | **Last Amended**: [YYYY-MM-DD]
