---
name: code-review
display_name: "代码评审"
display_name_en: "Code Review"
description: "该技能沿两个轴评审自某个固定点（commit、分支、tag 或 merge-base）以来的改动：标准（Standards，代码是否符合本仓库有文档记录的编码标准？）与规格（Spec，代码是否忠实实现了来源 issue/spec？）。两个评审作为并行子代理运行并并排汇报。适用于「review 一下这个分支」「帮我审一下这个 PR」「review since X」「看看这些改动有没有问题」这类需求。"
description_zh: "沿标准与规格两个轴评审改动，两路并行子代理分别出报告"
description_en: "Two-axis review of a diff: Standards and Spec, run as parallel sub-agents."
category: development-tools
version: 1.0.0
author: "大漠"
agent_created: true
---

# 代码评审（code-review）

对 `HEAD` 与用户提供的固定点之间的 diff 做双轴评审：

- **标准（Standards）**：代码是否符合本仓库有文档记录的编码标准？
- **规格（Spec）**：代码是否忠实实现了来源 issue / spec？

两个轴作为**并行子代理**运行，这样它们不会互相污染上下文，然后本技能聚合它们的发现。

issue tracker 本应已经提供给你。如果 `docs/agents/issue-tracker.md` 缺失，就提示用户运行 `setup-matt-pocock-skills` 技能。

## 流程（Process）

### 1. 钉住固定点

用户说的就是固定点（一个 commit SHA、分支名、tag、`main`、`HEAD~5` 等等）。如果他们没有指定，就问。

把 diff 命令记下来一次：`git diff <fixed-point>...HEAD`（三点，这样比较的是 merge-base）。也记下 commit 列表：`git log <fixed-point>..HEAD --oneline`。

在往下走之前，确认固定点能解析（`git rev-parse <fixed-point>`）且 diff 非空。坏掉的 ref 或空 diff 应该在这里失败，而不是在两个并行子代理里面。

### 2. 确定规格来源

按这个顺序找来源 spec：

1. commit message 里的 issue 引用（`#123`、`Closes #45`、GitLab `!67` 等），通过 `docs/agents/issue-tracker.md` 里的 workflow 获取。
2. 用户作为参数传入的路径。
3. `docs/`、`specs/` 或 `.scratch/` 下与分支名或功能匹配的 spec 文件。
4. 如果什么都没找到，问用户 spec 在哪。如果他们说不存在，**规格（Spec）**子代理将跳过并报告「no spec available」。

### 3. 确定标准来源

仓库里任何记录代码该怎么写的东西，比如 `CODING_STANDARDS.md` 或 `CONTRIBUTING.md`。

在仓库记录的之外，标准轴始终带着下面这份**坏味道基线（smell baseline）**：一组固定的 Fowler 代码坏味道（_Refactoring_，第 3 章），即便仓库什么都没记录它也适用。两条规则约束它：

- **仓库覆盖基线。** 有文档记录的仓库标准永远优先；当它认可某个基线会标记的做法时，抑制这个坏味道。
- **永远是判断取舍。** 每个坏味道都是一个带标签的启发式（「可能的 Feature Envy」），从来不是硬性违规。和这里任何标准一样，跳过工具已经强制的东西。

每个坏味道按*是什么* → *怎么改*来读；拿它跟 diff 对照：

- **神秘命名（Mysterious Name）**：一个函数、变量或类型的名字没能揭示它做什么或存什么。→ 重命名它；如果找不出一个诚实的名字，说明设计是浑浊的。
- **重复代码（Duplicated Code）**：同一个逻辑形状在这次改动里出现在一个以上的 hunk 或文件里。→ 抽出共享形状，两处都调用它。
- **依恋情结（Feature Envy）**：一个方法伸进另一个对象的数据比伸进自己的还多。→ 把这个方法搬到它所依恋的数据上。
- **数据泥团（Data Clumps）**：同样的几个字段或参数老是结伴同行（一个想要诞生的类型）。→ 把它们捆成一个类型，传那个。
- **基本类型偏执（Primitive Obsession）**：用一个基本类型或字符串顶替一个值得拥有自己类型的领域概念。→ 给这个概念它自己的小类型。
- **重复的 switch（Repeated Switches）**：对同一个类型的同一段 `switch`/`if` 级联在这次改动里反复出现。→ 换成多态，或者两处共享的一张映射表。
- **霰弹式修改（Shotgun Surgery）**：一次逻辑改动迫使你在 diff 里许多文件间四处修改。→ 把会一起变的东西聚到一个模块里。
- **发散式变化（Divergent Change）**：一个文件或模块因为几个不相干的原因被改动。→ 拆分，让每个模块只因一个原因而变化。
- **夸夸其谈通用性（Speculative Generality）**：为 spec 并不需要的需求加上的抽象、参数或钩子。→ 删掉它；内联回去，直到真实需求出现。
- **消息链（Message Chains）**：长的 `a.b().c().d()` 导航，调用方不该依赖它。→ 把这一串走位藏到第一个对象上的一个方法后面。
- **中间人（Middle Man）**：一个类或函数主要只是在往后委派。→ 砍掉它，直接调用真正的目标。
- **被拒绝的遗赠（Refused Bequest）**：一个子类或实现者忽略或覆盖了它继承来的大部分东西。→ 放弃继承，改用组合。

### 4. 并行派发两个子代理

**标准子代理的 prompt** 应包含：

- 完整的 diff 命令和 commit 列表。
- 你在第 3 步找到的标准来源文件列表，**外加第 3 步的坏味道基线**全文粘贴（子代理没有其他途径拿到它）。
- 简报：「按文件/hunk 报告相关之处：(a) diff 违反某条有文档记录的标准的每一处：引用那条标准（文件 + 规则）；(b) 你发现的任何基线坏味道：命名它并引用该 hunk。区分硬性违规与判断取舍：违反有文档记录的标准可以是硬性的，但基线坏味道永远是判断取舍，而且有文档记录的仓库标准覆盖基线。跳过工具已经强制的东西。400 字以内。」

**规格子代理的 prompt** 应包含：

- diff 命令和 commit 列表。
- spec 的路径或已获取的内容。
- 简报：「报告：(a) spec 要求但缺失或只做了一半的需求；(b) diff 里没被要求的行为（范围蔓延 scope creep）；(c) 看起来实现了、但实现看起来是错的需求。每条发现都引用对应的 spec 原文行。400 字以内。」

如果 spec 缺失，跳过规格子代理，并在最终报告里注明。

### 5. 聚合

把两份报告分别放在 `## Standards` 和 `## Spec` 标题下，逐字或稍作清理地呈现。**不要**合并或重新排序发现，因为这两个轴是刻意分开的（见_为什么是两个轴_）。

结尾给一行摘要：每个轴的发现总数，以及_每个轴内_最严重的问题（如果有）。不要在轴之间挑一个总冠军：那正是这种分离要防止的重新排序。

## 为什么是两个轴

一个改动可能通过一个轴而在另一个轴上失败：

- 遵循了每一条标准、但实现错了东西的代码 → **标准通过，规格失败。**
- 完全按 issue 要求做、但破坏了项目约定的代码 → **规格通过，标准失败。**

把它们分开报告，能防止一个轴掩盖另一个轴。
