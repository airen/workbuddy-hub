---
name: retro
display_name: "会话复盘"
display_name_en: "Retro"
description: "该技能对一次编码会话做复盘（retrospective），找出可改进编码 agent 环境（environment）的候选项，以改善后续运行。适用于「复盘一下这次会话」「做个 retro」「agent 哪里可以改进」「怎么让下次跑得更好」「这次为什么这么费劲」这类需求。"
description_zh: "复盘一次编码会话，找出可改进 agent 环境的候选项并按严重度排序"
description_en: "Conduct a retrospective on a coding session and suggest environment improvements."
category: development-tools
version: 1.0.0
author: "大漠"
agent_created: true
---

# 复盘（retro）

用户要求做一次**复盘（retrospective）**。你要为改进编码 agent 的**环境（environment）**提出建议，以改善后续的运行。

## 步骤

1. 调用 Skill 工具加载 `writing-for-agents` 技能，获取写作风格指南。

2. 读用户指定那次会话的第一手材料（primary sources）。这可能意味着在这台机器上翻查会话日志。如果用户没有指定会话，默认用当前这次。

3. 在以下类别里寻找可改进的候选项。

- **导航（Navigation）**：agent 找到正确文件有多容易？文件之间有没有隐藏的依赖？一个**导航指针（navigation pointer）**会不会让它更容易？_什么时候用_：这次会话花了很长时间才找到某条信息。
- **自动化检查（Automated checks）**：有没有能抓住 agent 所犯错误的自动化检查？lint、类型检查、测试、文件系统 linter？先读仓库自己的检查命令（它的 `package.json`/构建工具的 `lint`/`check` 脚本、它的 CI workflow），这样一个「已经存在但没接上、或悄悄坏掉」的检查本身就是发现，而不是重新发明。一个没有**护栏（guardrail）**（没有 pre-commit hook，也没有跑它的 lint/typecheck/test 命令的 CI job）的仓库本身就是一个发现：一个没有 lint 的仓库是一个长期存在、被错过的机会，而不是中性的默认状态。_什么时候用_：agent 犯了一个自动化检查本可以抓住的错误，或者仓库压根没有护栏。
- **编码标准（Coding standards）**：该不该给**评审 agent（reviewer agent）**一条新规则去执行？该不该移除或澄清某条现有规则？先给这个违规分类：**机械式（mechanical）**的（固定的语法模式、被禁用的 API、import 形态、文件位置规则）要得到一个确定性检查，没得商量：在仓库自己的 linter 里加一条自定义规则、加一个 pre-commit hook，或者加一个 CI job，看仓库的语言和现有护栏哪个最省。默认是建检查，而不是写规则。把 `CODING_STANDARDS.md` 留给真正的**判断取舍（judgement calls）**（跨文件一致性、「与周围风格保持一致」、任何护栏都替代不了的东西）。_什么时候用_：评审 agent 没能抓住一个错误。
- **全局 AGENTS.md**：有没有哪些引导性指令应该改放到编码标准（或自动化检查）里？_什么时候用_：AGENTS.md 文件特别大 —— 无论是仓库里的还是用户全局作用域的。
- **工具经济性（Tool economy）**：agent 有没有做昂贵的工具调用，本可以更精简？有没有什么自定义工具（CLI、MCP）特别费 token？_什么时候用_：agent 做了一次昂贵的工具调用。
- **无效项（No-ops）**：找出引导文件里不改变 agent 行为的指令。_什么时候用_：引导文件又大又笨重。
- **信息获取（Information access）**：找出增加 agent 信息获取机会的地方。把 dev server 日志 tee 出来、对第三方服务的只读访问。_什么时候用_：某条关键信息 agent 拿不到。

4. 按严重程度从高到低把这些候选项呈现给用户。

## 参考

### 实现 vs 评审

记住所有工作都经过两个阶段：实现和评审。实现 agent 的**上下文压力（context pressure）**最大。它负责探索、写代码、调试失败。

评审 agent 的上下文压力最小 —— 它拿到的是一个 diff，所以不需要探索。它通常也不需要写代码或调试。

这意味着应该由评审 agent 负责施加编码标准，而不是实现 agent。

### 文件

你在仓库里有几个文件可用：

- `AGENTS.md`（或 `CLAUDE.md`）：这些文件会被推送到在这个仓库里工作的任何 agent 的上下文窗口。它们应当被极其克制地使用，通常只用于指向其他文件的**导航指针（navigation pointers）**。
- `CODING_STANDARDS.md`：这个文件在评审时读，不在实现时读。如果标准文件超过 1,000 行，给 docs 文件夹加**导航指针**。
- Docs：把 docs 当作参考文件，由其他文件指向。写新文档之前先找现有文档。
- Skills：把 skills 用于文档（因为它们的 description 会进入 agent 的上下文窗口），或者用于用户调用的命令。遵循 `writing-for-agents` 技能里的建议。
