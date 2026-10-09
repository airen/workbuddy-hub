# 02 · specify（写规格）

**命令**：`specify`　**频率**：每个功能一次　**产物**：`specs/NNN-slug/spec.md` + `specs/NNN-slug/checklists/requirements.md`

## 唯一铁律

> **聚焦 WHAT 与 WHY，把 HOW 挡在门外。**

规格里出现「用 Vite + SQLite 实现」「暴露 REST 接口」「用 React 组件」——**越界了**。那是 `plan` 的活。

判断方法：这句话，**一个完全不懂技术的人能不能听懂并且同意？** 能，就是规格；不能，就是方案。

## 执行步骤

### 1. 编号与目录

扫描 `specs/` 下已有目录，取下一个三位编号，生成语义化 slug：

```
specs/001-photo-album-organizer/
specs/002-user-auth/
```

> 三位数会自动进位（999 → 1000），不要硬截断。slug 用 kebab-case，从用户描述里提炼，不要照抄整句话。

> **可选**：如果项目是 git 仓库且用户希望按分支管理，建同名分支 `001-photo-album-organizer`。

### 2. 从模板生成 spec.md

拷 `templates/spec-template.md` 到目标目录，逐段填。**不要删掉模板的 HTML 注释** —— 它们是你的检查清单。

### 3. 写用户故事（最重要的部分）

每个用户故事必须：

| 要求 | 说明 |
|---|---|
| **带优先级** | P1 / P2 / P3…，P1 最关键 |
| **可独立测试** | 只实现这一个故事，也能交付一个有价值的 MVP |
| **有 Why this priority** | 说清为什么它排在这个位置 |
| **有 Independent Test** | 怎么单独验证它（"通过 X 操作即可完整验证，并交付 Y 价值"） |
| **有验收场景** | Given / When / Then 格式，至少 2 条 |

**"独立可测试"是硬要求**：能独立开发、独立测试、独立部署、独立演示。做不到就说明故事切错了 —— 重新切。

### 4. 写需求

- **功能需求**用 `FR-001`、`FR-002`… 编号，每条以 `System MUST …` / `Users MUST be able to …` 开头。
- **不确定的，标记不猜**：
  ```
  - **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
  ```
- **关键实体**（如果涉及数据）：只写它代表什么、有哪些关键属性，**不写表结构、不写字段类型**。

### 5. 写成功标准

`SC-001`… 编号，必须**可度量**且**技术无关**：

- ✅ "用户能在 2 分钟内完成账号创建"
- ✅ "系统在 1000 并发用户下无性能退化"
- ❌ "系统使用 Redis 缓存"（这是方案，不是标准）
- ❌ "用户体验良好"（不可度量）

### 6. 写边界情况与假设

- **Edge Cases**：边界条件、错误场景。
- **Assumptions**：当描述没说清时你选的"合理默认值"**必须显式列出来**，让用户有机会推翻。例如「假设用户有稳定网络」「假设 v1 不做移动端」。

### 7. 维护内建质量清单

`checklists/requirements.md` 是**规格质量的单元测试**，由 `specify` 创建、`clarify` 重新评估。它和用户自定义的 checklist 生命周期不同，**不要混用**。

## 自检（写完必过）

- [ ] 没有任何遗留的 `[NEEDS CLARIFICATION]` 标记（或已明确列出待用户回答）
- [ ] 每条需求都可测试、无歧义
- [ ] 每条成功标准可度量
- [ ] 全文没有出现具体技术栈 / 框架 / API 设计
- [ ] 每个用户故事都能独立交付价值
- [ ] 所有"合理默认值"都进了 Assumptions 段

## 收尾

告诉用户：规格文件路径、有几个用户故事（优先级分布）、有几个 `[NEEDS CLARIFICATION]`、**建议下一步跑 `clarify`**（如果有待澄清项）。
