---
name: spec-driven-development
description: "The complete Spec Kit methodology, adapted for WorkBuddy. Use when writing or reviewing a project constitution, a feature specification, clarification questions, a technical plan, a requirements-quality checklist, a dependency-ordered task list, a cross-artifact consistency analysis, an implementation run, a convergence check, a bug-fix assessment, or an idea assessment. Contains the SDD philosophy, the nine-command pipeline, the artifact directory layout, and the official spec/plan/tasks/checklist/constitution templates."
---

# Spec-Driven Development (Spec Kit 方法论)

本技能是「规格驱动开发教练」专家的知识库。它把 GitHub Spec Kit 的方法论、命令语义、模板纪律和产物结构完整搬进来，并改造成**在 WorkBuddy 里可直接执行**的形式。

## 与 Spec Kit CLI 的关键差异（先读这一节）

Spec Kit 原版是一个 Python CLI（`specify-cli`），靠 `specify init` 铺目录、靠各家的斜杠命令（`/speckit-*`、`$speckit-*`、`/skill:speckit-*`）驱动流程。

**在 WorkBuddy 里没有这个 CLI，也不需要它。** 你（agent）就是执行器：

| Spec Kit 原版 | 在 WorkBuddy 里 |
|---|---|
| `specify init my-project --integration <agent>` | 跑 `scripts/scaffold.sh <项目根>` 铺 `.specify/` 与 `specs/` 结构 |
| `/speckit.constitution` 等斜杠命令 | **你直接按 `references/` 里对应章节的规范执行**，把产物写到磁盘 |
| CLI 负责的功能编号、建分支、拷模板 | 你手动做：扫 `specs/` 取下一个编号 → 建 `specs/NNN-slug/` → 从 `templates/` 拷模板 |

**斜杠命令名仍然保留**（`constitution`、`specify`、`clarify`、`plan`、`checklist`、`tasks`、`analyze`、`implement`、`converge`），因为它们是这套方法论的通用语汇 —— 用户说「跑一下 analyze」你要能听懂。但**不要**要求用户去装 CLI 或输入斜杠命令；用户只要说人话，你来编排。

## 三条独立入口（不是三个阶段）

```
① SDD（建功能）      constitution → specify → clarify → plan → checklist → tasks → analyze → implement → converge
② Bug 修复           assess → fix → test
③ 想法评估           intake → research → define → shape → decide
```

**它们是独立入口，不是必须先走的三个步骤。** SDD 是核心；Bug 修复和想法评估是可选扩展，用户需要时才用。

## 路由表

| 用户要什么 | 读哪个文件 |
|---|---|
| 理解这套方法论为什么成立、和"凭提示词祈祷"的区别 | `references/00-philosophy.md` |
| 立/改项目章程（工程原则、质量关卡） | `references/01-constitution.md` + `templates/constitution-template.md` |
| 把想法写成规格（用户故事、验收场景、功能需求、成功标准） | `references/02-specify.md` + `templates/spec-template.md` |
| 澄清规格里的模糊点（一次最多 5 问） | `references/03-clarify.md` |
| 出技术方案（技术栈、架构、数据模型、契约） | `references/04-plan.md` + `templates/plan-template.md` |
| 生成"需求的单元测试"清单 | `references/05-checklist.md` + `templates/checklist-template.md` |
| 把方案拆成有序、可并行的任务清单 | `references/06-tasks.md` + `templates/tasks-template.md` |
| 交叉检查 spec/plan/tasks 是否一致 | `references/07-analyze.md` |
| 按任务清单执行实现 | `references/08-implement.md` |
| 验证实现是否真的满足规格，直到收敛 | `references/09-converge.md` |
| 修一个坏掉的行为（诊断→修复→验证分离） | `references/10-bugfix.md` |
| 判断一个想法值不值得投入 | `references/11-assessment.md` |
| 查 Spec Kit 支持哪些编码代理、各家的命令调用语法 | `references/12-integrations.md` |

## 核心纪律（违反任意一条，这套方法论就失效了）

1. **规格先行，代码在后。** 没有 `spec.md` 就不要开始写实现。
2. **聚焦 WHAT/WHY，把 HOW 挡在门外。** 规格里出现「用 React + Redux 实现」就是越界 —— 那是 `plan` 的活。
3. **不猜，标记。** 推不出来的需求一律写 `[NEEDS CLARIFICATION: 具体缺什么]`，不要用"合理默认值"蒙过去。
4. **每个用户故事必须能独立测试。** 只实现 US1 也要能交付一个可用的 MVP。
5. **一次推进一步，每步给用户看。** 不要一口气从想法冲到实现。
6. **改问题要回到拥有它的那一步。** 需求问题回 `specify`/`clarify`，设计问题回 `plan`，任务问题回 `tasks`；不要在实现里就地打补丁。
7. **`analyze` 只读，`converge` 只追加任务。** 前者绝不改文件，后者绝不改代码。
8. **缺失的验证 ≠ 成功的修复。** 没验证过的东西不许报告为通过。

## 产物目录结构

```
<项目根>/
├── .specify/
│   ├── memory/
│   │   └── constitution.md        # 项目章程（每项目一份）
│   ├── templates/                 # 模板副本
│   ├── bugs/<slug>/               # Bug 修复产物
│   │   ├── assessment.md
│   │   ├── fix.md
│   │   └── verification.md
│   └── assessments/<slug>/        # 想法评估产物
│       ├── intake.md
│       ├── research.md
│       ├── definition.md
│       ├── shape.md
│       └── decision.md
└── specs/
    └── 001-feature-slug/          # 每个功能一个目录，三位编号
        ├── spec.md
        ├── checklists/
        │   └── requirements.md    # 内建规格质量清单（specify/clarify 维护）
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md
        ├── contracts/             # 接口契约（先于实现创建）
        └── tasks.md
```

> 说明：原版 Spec Kit 会把每个功能建在独立 git 分支 `NNN-slug` 上。在 WorkBuddy 里，**分支可选** —— 用户的项目如果不是 git 仓库或不想建分支，就直接建目录。要建分支时用同样的命名。

## 快速上手

```bash
# 1. 铺目录结构（在项目根执行）
bash <skill-dir>/scripts/scaffold.sh /path/to/project

# 2. 然后按 references/ 的顺序推进，产物写进上面那些文件
```

## 相关文档

- 上游项目：https://github.com/github/spec-kit （MIT License）
- 官方文档：https://github.github.io/spec-kit/
- 完整方法论原文：`references/00-philosophy.md`（译自上游 `spec-driven.md`）
