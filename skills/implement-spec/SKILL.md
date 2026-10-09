---
name: implement-spec
display_name: "整份规格实现"
display_name_en: "Implement Spec"
description: "该技能用于把一份规格说明和它的关联工单在代码里实现出来：把工单读成一张带阻塞关系的任务图，在一条集成分支（integration branch）上并发调度实施者子代理（用 Agent 工具），最后跑一次 code-review 技能并结掉所有工单。适用于「按规格实施」「把整个 spec 做出来」「并发实现」「implement-spec」这类需求。"
description_zh: "把整份规格当任务图，并发调度实施子代理，最后统一评审"
description_en: "Implement a whole spec on one integration branch, running sub-agents across the ready frontier."
category: development-tools
version: 1.0.0
author: "大漠"
disable-model-invocation: true
agent_created: true
---

# 按规格实施（implement-spec）

你已经被提供了一份规格说明。这份规格说明应该有关联的工单，描述如何实施它。

Issue 追踪器应该已经提供给你了。如果没有，提示用户先运行 `setup-matt-pocock-skills` 技能完成本仓库初始化。

目标是在一条单一的**集成分支（integration branch）**上实现整份规格说明，每一张工单都按 issue 追踪器关闭工作的方式来结掉。

工单不是一串步骤。它们是一张带阻塞关系的**任务图（task graph）**。这意味着永远存在一个**前沿（frontier）**，上面是就绪、可以被领走的工单。

与子代理（用 Agent 工具）之间的通信应当稀疏。主要靠**上下文指针（context pointer）**沟通：指向规格说明、工单、研究笔记和之前的提交。不要重复那些已经能通过指针获得的信息。

**实施者子代理（用 Agent 工具）**应尽可能在后台运行，以获得最大并发。

## 步骤

1. 读规格说明和工单，理解这张任务图。

2. （可选）用一个**探索子代理（用 Agent 工具）**做那些工单所需的探索 —— 相关的代码库文件或外部文档。确保探索子代理能保存文件 —— 它应把 markdown 笔记保存到仓库之外、所有后续子代理都能访问的一个目录里。这让**实施者子代理**能专注于实施而不是探索。

3. 创建集成分支。如果 issue 追踪器通过 PR 关闭工作，或者用户要求一个，就在第 5 步第一次合并之后开一个草稿 PR（一个领先 main 还没有提交的分支开不了 PR），标注为关闭这份规格说明和这些工单。

4. 用**实施者子代理**实施每一张工单，每个都在它自己的 worktree、它自己的分支上。每个实施者子代理：
   - 在开始前确认它的 worktree 基于集成分支，如果不是就重置到它上面；
   - 调用 Skill 工具加载 `tdd` 技能来构建这张工单；
   - 在汇报完成之前，把集成分支的顶端合并进它自己的分支

5. 一旦某个**实施者子代理**完成，就用一个**合并子代理（用 Agent 工具）**把它的工作合并到集成分支。

6. 如果这改变了可用工单的**前沿（frontier）**，就再启动更多**实施者子代理**去做那些新工单。这允许最大并发。

7. 一旦所有工单都完成，在集成分支上调用 Skill 工具加载 `code-review` 技能。用一个**实施者子代理**修复代码评审提出的所有问题。

8. 如果存在草稿 PR，把它标记为可供评审。否则，按 issue 追踪器关闭工作的方式逐张结掉工单，并汇报集成分支。

9. 清理所有**实施者子代理**的 worktree。
