---
name: improve-codebase-architecture
display_name: "架构深化扫描"
display_name_en: "Improve Codebase Architecture"
description: "该技能扫描一个代码库，找出可以深化（deepening）的地方——把浅模块（shallow module）变成深模块（deep module）的重构——把它们做成一份可视化的 HTML 报告，再就你选中的那一个陪你一路拷问下去。适用于「帮我看看架构」「哪里能重构」「模块太浅了」「提升可测试性」「架构评审」「deepen 一下」这类需求。"
description_zh: "扫描代码库找出可深化之处，出可视化 HTML 报告，再逐项拷问"
description_en: "Scan a codebase for deepening opportunities, present them as an HTML report, then grill through one."
category: development-tools
version: 1.0.0
author: "大漠"
disable-model-invocation: true
agent_created: true
---

# 改进代码库架构（improve-codebase-architecture）

把架构上的摩擦（friction）暴露出来，并提出**深化机会（deepening opportunities）**：那些把浅模块（shallow module）变成深模块（deep module）的重构。目标是可测试性和 AI 可导航性（AI-navigability）。

本技能_以_项目的领域模型为依据（informed），并建立在共享的设计词汇之上：

- 调用 Skill 工具加载 `codebase-design` 技能，获取架构词汇（**module**、**interface**、**depth**、**seam**、**adapter**、**leverage**、**locality**）及其原则（删除测试（deletion test）、「接口就是测试面（the interface is the test surface）」、「一个适配器 = 假想的接缝，两个 = 真实的接缝」）。每一条建议都精确使用这些术语，不要漂移到「component」「service」「API」「boundary」上去。
- `GLOSSARY.md` 里的领域语言为好的接缝（seam）命名；`docs/adr/` 里的 ADR 记录了本技能不应重新翻案的决定。

## 流程（Process）

### 1. 探索

**先定范围，再扫描：YAGNI。** 深化一个模块的回报在于让它未来的改动更容易，所以把额外的权重放在代码库里最近改动过的部分。先决定_往哪看_，再看：

- 如果用户点明了方向（一个模块、一个子系统、一个痛点），就照它走，跳过下面的推断。
- 否则，往回翻一段不短的提交历史（`git log --oneline`），找出代码库的热点——那些反复出现的文件和区域——让这些路径先把你的注意力拉过去。如果改动很分散、没有明显热点，就把网撒得更宽。

先读项目的领域术语表（`GLOSSARY.md`），以及你要触碰那块区域里的任何 ADR。

然后派一个子代理（用 Agent 工具）去走一遍代码库。不要套死板的启发式；有机地探索，并记下你在哪里感到了摩擦：

- 哪里为了理解一个概念，得在许多小模块之间来回跳？
- 哪里的模块是**浅的（shallow）**，接口几乎和实现一样复杂？
- 哪里为了可测试性把纯函数抽了出来，但真正的 bug 却藏在它们被调用的方式里（没有**局部性（locality）**）？
- 哪里的紧耦合模块跨过各自的接缝（seam）在泄漏？
- 代码库的哪些部分没有测试，或者很难通过它们当前的接口去测？

对任何你怀疑是浅的东西应用**删除测试（deletion test）**：删掉它会让复杂度集中，还是只是把它挪个地方？「是的，会集中」才是你想要的信号。

### 2. 把候选做成一份 HTML 报告

写一个自包含的 HTML 文件到操作系统临时目录，这样什么都不会落进仓库。从 `$TMPDIR` 解析临时目录，回退到 `/tmp`（Windows 上是 `%TEMP%`），写到 `<tmpdir>/architecture-review-<timestamp>.html`，让每次运行都拿到一个新文件。为用户打开它（Linux 上是 `xdg-open <path>`，macOS 上是 `open <path>`，Windows 上是 `start <path>`），并告诉他们绝对路径。

报告用**通过 CDN 引入的 Tailwind** 做布局和样式，用**通过 CDN 引入的 Mermaid** 来画那些用图/流/时序能可靠传达结构的图。把 Mermaid 和手写的 CSS/SVG 视觉混着用：当关系是图形状的时候（调用图、依赖、时序）用 Mermaid，当你想要更有编辑感的东西时（质量图、剖面图、折叠动画）用亲手搭的 div/SVG。每个候选都配一幅**前/后（before/after）可视化**。要够视觉化。

对每个候选，渲染一张卡片，包含：

- **Files**：涉及哪些文件/模块
- **Problem**：当前的架构为什么在制造摩擦
- **Solution**：用平实的话描述会改什么
- **Benefits**：用局部性（locality）和杠杆（leverage）来解释，以及测试会如何变好
- **Before / After diagram**：并排、亲手画的，展示「浅」与「深化」
- **Recommendation strength**：`Strong`、`Worth exploring`、`Speculative` 之一，渲染成一个徽章

报告以一节 **Top recommendation** 结尾：你会先动哪个候选，以及为什么。

**领域用 `GLOSSARY.md` 的词汇，架构用 `codebase-design` 技能的词汇。** 如果 `GLOSSARY.md` 定义了「Order」，就谈「the Order intake module」，而不是「the FooBarHandler」，也不是「the Order service」。

**ADR 冲突**：如果某个候选与既有的 ADR 相矛盾，只有当这个摩擦真实到值得重新审视那条 ADR 时才把它摆出来。在卡片里清楚地标注它（例如一个警告框：_"与 ADR-0007 相矛盾，但值得重新打开，因为……"_）。不要罗列每条 ADR 所禁止的每一个理论上的重构。

完整的 HTML 骨架、图示模式和样式指引见 [HTML-REPORT.md](references/HTML-REPORT.md)。

**还不要**提出接口。文件写完之后，问用户：「这里面的哪一个你想深入探索？」

### 3. 拷问循环

用户选定一个候选后，调用 Skill 工具加载 `grilling` 技能，和他们一起走这棵决策树：约束、依赖、深化后模块的形状、接缝（seam）后面坐着什么、哪些测试能活下来。

随着决定逐步成型，副作用就地发生；调用 Skill 工具加载 `domain-modeling` 技能，边聊边让领域模型保持最新：

- **用一个不在 `GLOSSARY.md` 里的概念给深化后的模块命名？** 把这个术语加进 `GLOSSARY.md`。文件不存在就惰性创建它。
- **对话中把一个模糊的术语磨锋利了？** 就地更新 `GLOSSARY.md`。
- **用户用一个承重的理由否掉了这个候选？** 提议写一条 ADR，措辞是：_"要不要我把这条记成一个 ADR，好让未来的架构评审不再重新建议它？"_ 只有当这个理由确实是未来的探索者避免重复建议同一个东西所需要的，才提这个议；跳过那些转瞬即逝的理由（「现在不值得」）和不言自明的理由。
- **想为深化后的模块探索备选接口？** 调用 Skill 工具加载 `codebase-design` 技能，用它的「design-it-twice」平行子代理（用 Agent 工具）模式。
