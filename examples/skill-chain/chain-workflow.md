# 真实示例：技能链跑一遍长什么样

> 以本仓库「新增一个技能」的真实流程为素材，
> 演示 `to-spec` → `to-tickets` → `implement` 三步接力。

---

## 第 1 步：to-spec —— 对话沉淀成规格

**触发**：「把刚才聊的写成规格」

**对话上下文**：用户与 agent 讨论「给 hub 新增一个技能要满足什么条件」。

**产出**（发布到 issue 追踪器，打 `ready-for-agent` 标签）：

```markdown
## Problem Statement

新增技能时，作者不知道该填哪些字段，
导致 registry 索引与原生文件对不上。

## Solution

SKILL.md frontmatter 必填 name / display_name / description /
version / author；manifest.yaml 由 sync_manifests.py 派生，不手写。

## Seams（接缝）

- 最高接缝：`scripts/build_registry.py` 的输出 diff（0 错误即过）
```

## 第 2 步：to-tickets —— 规格拆成带阻塞边的工单

**触发**：「拆成工单」

**产出**（每张工单一个文件，声明阻塞边）：

```text
ticket-1: 写 SKILL.md frontmatter（无前置依赖）
ticket-2: 跑 sync_manifests.py --force（阻塞于 ticket-1）
ticket-3: 跑 build_registry.py 验证索引（阻塞于 ticket-2）
```

## 第 3 步：implement —— 按工单在接缝上 TDD 实现

**触发**：「开始实现」

**循环**（红 → 绿 → 重构，每个 ticket 一轮）：

1. 在最高接缝（`build_registry.py` 输出）上先看到「缺这个技能」的报错（红）
2. 写 frontmatter + 跑 sync（绿）
3. 收尾调用 `code-review` 技能评审，`git commit` 原子提交

**收尾证据**：`build_registry.py` 0 错误；`git log` 可见
`feat(skills): 新增 xxx` 单 commit。
