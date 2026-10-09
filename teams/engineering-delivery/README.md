# 软件工程交付专家团 · Engineering Delivery Team

> Production-grade engineering delivery for AI coding agents.
> 上游来源：[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)（MIT）

## 类型

Team 型（多角色协作团队） · 分类：技术工程（`02-Engineering`）

## 它是什么

把 Addy Osmani 的 `agent-skills`（25 个覆盖完整开发生命周期的工程技能 + 4 个审查角色 + 7 份检查清单）封装成 WorkBuddy 专家团。

主理人「交付总监 · 齐活林」自己完成 **DEFINE → PLAN → BUILD → SHIP**，然后把变更交给四位**独立**审查专家并行把关，最后汇编结论并给出可执行的交付判断。

## 团队成员

| 成员 | 名字 | 职业 | 职责 |
|------|------|------|------|
| `engineering-delivery-team-lead` | 齐活林 | 交付总监 | 编排调度、生命周期实现、门禁裁决、最终汇编 |
| `engineering-delivery-code-reviewer` | 沈查 | 代码审查官 | 五轴审查：正确性/可读性/架构/安全/性能 |
| `engineering-delivery-test-engineer` | 严过关 | 测试工程师 | 测试策略、覆盖率缺口、Prove-It 缺陷复现 |
| `engineering-delivery-security-auditor` | 安守正 | 安全审计师 | 信任边界、STRIDE、OWASP + LLM Top 10 |
| `engineering-delivery-performance-auditor` | 马迅达 | Web性能审计师 | Core Web Vitals、加载/渲染/网络（仅 Web 项目） |

## 六阶段 SOP

```
Phase 0  澄清与定界      interview-me / idea-refine          （主理人）
Phase 1  规格与约束      spec-driven-development             （主理人）
Phase 2  拆解与上下文    planning-and-task-breakdown         （主理人）
Phase 3  增量实现        incremental-implementation + …      （主理人）
Phase 4  四路并行审查    四位审查专家                        （并行 spawn）
Phase 5  修复与复验      原审查员复验                        （主理人 + 成员）
Phase 6  交付与发布      shipping-and-launch + …             （主理人）
Phase 7  最终报告        汇编 + 门禁结论                     （主理人）
```

**五道门禁**：G1 规格门 → G2 验证门（每个切片）→ G3 审查门 → **G4 阻断门（Critical 未解决禁止发布）** → G5 完成门。

## 内置技能（25 个）

按生命周期分组，完整保留上游 `SKILL.md` 内容：

| 阶段 | 技能 |
|------|------|
| Meta | `using-agent-skills` |
| Define | `interview-me`、`idea-refine`、`spec-driven-development`、`constraint-driven-development` |
| Plan | `planning-and-task-breakdown` |
| Build | `context-engineering`、`source-driven-development`、`incremental-implementation`、`doubt-driven-development`、`frontend-ui-engineering`、`api-and-interface-design` |
| Verify | `test-driven-development`、`browser-testing-with-devtools`、`debugging-and-error-recovery` |
| Review | `code-review-and-quality`、`code-simplification`、`security-and-hardening`、`performance-optimization` |
| Ship | `git-workflow-and-versioning`、`ci-cd-and-automation`、`deprecation-and-migration`、`documentation-and-adrs`、`observability-and-instrumentation`、`shipping-and-launch` |

## 内置检查清单（7 份）

位于 `references/`，技能通过相对路径引用：

`definition-of-done.md` · `testing-patterns.md` · `security-checklist.md` · `performance-checklist.md` · `accessibility-checklist.md` · `observability-checklist.md` · `orchestration-patterns.md`

## 上游斜杠命令 → 本包用法

上游的 9 个命令是薄包装，本包不注册 `commands/`（WorkBuddy 专家包禁止该目录），改为**直接点名技能或成员**：

| 上游命令 | 本包等价用法 |
|---------|-------------|
| `/spec` | 说「先写规格」→ 主理人加载 `spec-driven-development` |
| `/plan` | 说「拆任务」→ 加载 `planning-and-task-breakdown` |
| `/build` | 说「开始实现」→ 加载 `incremental-implementation` |
| `/test` | 说「测试驱动」→ 加载 `test-driven-development` |
| `/constraints` | 说「定质量标准」→ 加载 `constraint-driven-development` |
| `/review` | 说「review 这个改动」→ 调度代码审查官 |
| `/webperf` | 说「看下性能」→ 调度 Web 性能审计师 |
| `/code-simplify` | 说「这段太复杂」→ 加载 `code-simplification` |
| `/ship` | 说「上线前把关」→ Workflow C |

## 使用示例

- 我要做一个新功能，带我走一遍从规格到上线的完整流程
- 帮我审查这次改动：正确性、可读性、架构、安全、性能五个维度都要过一遍
- 上线前帮我做一轮安全检查、性能审计和发布清单核对
- 这个 bug 好难，先帮我造一个能稳定复现的失败测试

## 与上游的差异（重要）

| 项目 | 上游 | 本包 |
|------|------|------|
| 组织形式 | 单一 agent 的技能包 | 专家团（1 主理人 + 4 审查成员） |
| 审查触发 | 斜杠命令 `/review`、`/ship` | 主理人按 SOP 调度，或用户直接点名 |
| 成员间通信 | persona 之间禁止互调（上游规则） | 经主理人中转（WorkBuddy 团队铁律） |
| 斜杠命令 | 9 个 TOML 命令 | 移除，改用技能名/成员名直调 |
| `references/` | 包根目录 | **保持不变**，技能相对路径无需改写 |

## 头像

已生成于 `avatars/`（6 张：团队 1 张 + 成员 5 张）。如需替换：PNG/JPG，512×512，≤500KB。

## 许可

上游 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 为 **MIT** 许可。本包保留其技能与清单内容原文，仅新增专家团编排层。
