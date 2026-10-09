---
name: ask-matt
display_name: "技能路由"
display_name_en: "Ask Matt"
description: "该技能是一个路由器（router），根据你此刻的处境告诉你该用哪个技能、走哪条流程：从想法到交付的主流程、分诊 / 诊断 / 寻路这类入口（on-ramp）、代码库维护，以及运行在底层的词汇技能。适用于「我该用哪个技能」「接下来干嘛」「这个情况走什么流程」「下一步做什么」「ask matt」这类需求。"
description_zh: "按你此刻的处境，告诉你该用哪个技能、走哪条流程"
description_en: "A router over the skill set: tells you which skill or flow fits your situation."
category: development-tools
version: 1.0.0
author: "大漠"
agent_created: true
---

# 问一问（Ask Matt）

你不记得每一个技能，所以直接问。

一个**流程（flow）**是穿过这些技能的一条路径。多数路径沿一条**主流程（main flow）**前进，另有两条**入口（on-ramp）**并入其中。其余技能要么独立（standalone），要么是运行在底层的词汇层（vocabulary layer）。

## 主流程：想法 → 交付

多数工作走的就是这条路。你有了一个想法，想把它做出来。

1. **`grill-with-docs` 技能**通过访谈把想法磨锋利。只要你**在一个工作目录里干活**，就从这里开始：它是有状态的，会把学到的东西留在 `GLOSSARY.md` 和 ADR 里。（没有工作目录？改用 `grill-me` 技能，见「独立技能」一节。两者跑的是同一个 `grilling` 原语；`grill-with-docs` 是那个会留下纸面痕迹的，所以只要有仓库可供留痕，它就是两者中更好的那个。）

2. **分支：所有问题都能靠对话解决吗？** 如果某个问题需要一个可运行的答案（状态、业务逻辑、必须亲眼看到的 UI），就绕道做一个原型（prototype），两个方向都由 **`handoff` 技能**搭桥（原型住在它自己的目录里，这正是 `handoff` 的用途；见「阶段边界」）：
   - **`handoff` 技能**送出去，然后针对那个文件开一个全新会话，
   - **`prototype` 技能**用一次性代码回答那个问题，
   - 再用 **`handoff` 技能**把学到的东西送回来，并从原来的想法线程里引用它。

3. **分支：这是一次跨多个会话的构建吗？**
   - **是** → 用 **`to-spec` 技能**（把线程变成一份规格说明），再用 **`to-tickets` 技能**把它切成曳光弹（tracer bullet）工单，每张工单都声明自己的**阻塞边（blocking edge）**。然后按两种方式之一推进这些工单：
     - 每张工单跑一次 **`implement` 技能**，每张之间**清空（`/clear`）**上下文。在本地追踪器上，那是 `.scratch/<feature>/issues/` 下每张工单一个文件，按「阻塞者优先」手工推进；在真实追踪器上，这些边会变成原生的阻塞链接，于是任何阻塞者都已完成的工单都能被领走。每张工单都是自包含的，所以上一张的上下文用完即弃。
     - 用 **`implement-spec` 技能**一口气跑完整个规格。它把工单读成一张**任务图（task graph）**，让实施者子代理（用 Agent 工具）并行跑在就绪的**前沿（frontier）**上，最后把所有东西落到一条**集成分支（integration branch）**上。当你更想编排整个构建、而不是自己一张张驱动工单时，就用它。
   - **否** → 就在原地、在同一个上下文窗口里跑 **`implement` 技能**。

   无论走哪条路，代码都是靠驱动 **`tdd` 技能**（一次一个红-绿切片）建起来的，并以 **`code-review` 技能**收尾 —— 那是对 diff 的两轴评审（标准 + 规格）。`implement` 技能对每张工单都跑这两件事；`implement-spec` 技能的各个实施者各自驱动 `tdd` 技能，它则在集成分支上跑一次 `code-review` 技能。当你只是想在没有完整规格的情况下、测试先行地建一个具体行为时，单独用 **`tdd` 技能**；当你想拿一个固定点（fixed point）去评审某个分支或 PR 时，随时单独用 **`code-review` 技能**。

   当工作以拉取请求（pull request）的形式提交时，**`pr` 技能**塑造 PR 正文：展示改动的最小可视化、证明它可用的前后对比证据，以及一个单向门／双向门（one-way / two-way door）判断。它是模型自动调用的（model-invoked），所以代理只要写 PR 就会去用它。

4. **`retro` 技能**闭合回路。一次构建之后，尤其是跑偏了的那种，它会回看整个会话，并对代理的**环境**提出改动建议，而不是对代码：导航指针、自动化检查、`code-review` 技能执行的编码标准、引导文件（steering file）、工具链。机械性错误变成确定性检查；判断性取舍变成编码标准。下一次构建于是从更好的环境出发。

### 上下文卫生（context hygiene）

把第 1–3 步保持在**同一个不中断的上下文窗口**里（在 `to-tickets` 技能跑完之前不要压缩或清空），这样访谈、规格和工单都建立在同一套思考之上。之后每一次 `implement` 技能都从工单出发、全新开始。`retro` 技能要在它所回看的那个会话里运行，在你清空之前；清空之后，就把它指向那个会话的日志。

这件事的上限是 **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**：模型仍能锐利推理的窗口（在最先进模型上约 150k token）。如果某个会话在 `to-tickets` 技能之前就逼近它，不要在性能退化的情况下硬推；在最近的阶段边界（phase boundary）上做 `compact`（压缩上下文），然后继续（见「阶段边界」）。

## 入口（on-ramp）

一种起点情境：它会产生工作，然后并入主流程。

- **bug 和请求堆成山** → **`triage` 技能**。它让 issue 流经分诊角色（triage role），产出「代理就绪（agent-ready）」的 issue，之后由 **`implement` 技能**接手。

  分诊只针对**不是你创建的** issue：bug 报告、外部进来的功能请求、任何原始到达的东西。`to-tickets` 技能产出的工单已经代理就绪，所以**不要对它们做分诊**。

- **有东西坏了** → **`diagnosing-bugs` 技能**。对付那些难缠的：一眼看不穿的 bug、间歇性抽风（flake）、在两个已知良好状态之间悄悄混进来的回归。它在拿到一个**紧密反馈回路（tight feedback loop）**（一条已经能因*这个* bug 变红的命令）之前，拒绝做任何理论推测，然后用一个回归测试来修。当真正的发现是「没有好的接缝（seam）能把 bug 钉死」时，它的复盘会移交给 **`improve-codebase-architecture` 技能**。

- **一项庞大、迷雾重重的工程：绿地（greenfield）项目或巨型功能构建，大到一次会话装不下** → **`wayfinder` 技能**，这里是认知负荷最高的流程。当从此处到目的地的路还看不见时，它在 issue 追踪器上绘出一张**共享地图（shared map）**，由**决策工单（decision ticket）**构成，一次解决一张，产出**决策，而不是交付物**，直到迷雾被推退、道路变清晰。`grill-with-docs` 技能磨的是你能在一次会话里握住的想法，wayfinder 面对的是你握不住的那种，它更慢、更密，所以只留给那种情况，绝不用于一个范围清晰的功能。

  当地图变得清晰时，**它是移交，不是构建**：在 **`to-spec` 技能**处并入主流程，由它把地图里那些互相关联的决策收敛成一份可构建的计划，然后照常走 `to-tickets` 和 `implement`。把地图直接绕进 `implement` 会跳过这次收敛、把那些互相关联的细节扔掉，所以只有当这项工程最终确实很小的时候，才直接进 `implement`。

## 代码库健康（codebase health）

不是功能开发，只是维护。

- **`improve-codebase-architecture` 技能**，只要你有空档、想让代码库保持适合代理操作的状态，就随时跑它。它把**加深机会（deepening opportunity）**摆到台面上；挑中一个就会*生成一个想法*，你可以带着它到 `grill-with-docs` 技能处进入主流程。它是找出候选者的勘测；**`codebase-design` 技能**（见下）则是你为选中的那个做设计的工坊台（bench）。

## 底层的词汇

两份由模型自动调用的参考资料，运行在其他技能*之下*，各自是自己那套词汇的唯一真相来源。当出问题的是**词**而不是流程时，直接去用它们；或者让上面的技能把它们拉进来。

- **`domain-modeling` 技能**：磨利项目的*领域*语言：挑战一个含糊的词、拆解一个超载的词（「account」身兼三职）、把难以逆转的决策记成 ADR。它是 `grill-with-docs` 技能所驱动的主动纪律，用来让 `GLOSSARY.md` 保持成一份干净的术语表。
- **`codebase-design` 技能**是设计模块*形态*时用的深模块（deep module）词汇（模块、接口、深度、接缝、适配器、杠杆、局部性）：在干净的接缝处，把大量行为藏在一个小接口后面。`tdd` 技能和 `improve-codebase-architecture` 技能都讲这套话。

## 阶段边界（phase boundary）

一个**阶段（phase）**是会话里的一块工作：访谈、实施、QA。在两个阶段之间的**边界（boundary）**上，你有五个选项，而在这之间做选择，是整张地图里最模糊的决策：

- **继续（Continue）**：原地不动。不花成本，不丢东西。
- **`/clear`（清空）**：清空窗口，当这里的一切对接下来都无所谓时。
- **`handoff` 技能**写出一个可携带的 markdown 文件。用途很窄：只用于**新的 harness**、**新的目录**、**同事**，或者**在阶段中途**分叉出一个支线任务。它买到的是可携带性。
- **子代理（用 Agent 工具）**：把一个范围收紧的任务送到它自己的窗口，拿一份报告回来。
- **`/compact`（压缩）**：压缩当前上下文，并用它给一个全新会话播种。它是**默认选项**，位于这棵树的底部，而不是第一伸手去够的那个。

读 [PHASE-BOUNDARIES.md](references/PHASE-BOUNDARIES.md) 了解那棵有序的决策树：五个问题、每个分支背后的理由，以及为什么「一手来源（primary source）成本」让**继续（Continue）**成为最该首先排除的那个。要在边界**上**做决定；阶段中途，要么继续，要么把剩下的拆成子代理。

## 独立技能（standalone）

完全在主流程之外。

- **`grill-me` 技能**：跟 `grill-with-docs` 技能一样不留情面的访谈，但是**无状态的**：它不在本地保存任何东西，也不构建 `GLOSSARY.md`。当你**不在一个工作目录里干活**时（磨一个计划、一个设计、一篇文字，任何底下没有仓库的东西）用它。如果你在工作目录里，改用 `grill-with-docs` 技能：它跑同样的访谈、还会留下纸面痕迹，所以严格来说它是更好的那个。
- **`grilling` 技能**就是访谈原语本身：轮次、前沿，事实是代理的活、决策是你的。`grill-me` 技能和 `grill-with-docs` 技能是两条具名的入口，而 `triage` 技能、`wayfinder` 技能和 `improve-codebase-architecture` 技能都在内部跑它。只有当你想要一个没有任何包装的访谈时，才直接用它。
- **`prototype` 技能**是一个小小的、一次性的程序，用来回答一个设计问题：这个状态模型感觉对吗，或者这个 UI 该长什么样。「一次性」是对代码写法的约束，不是要销毁它的承诺：答案会折进真正的代码里，而原型本身作为一份**一手来源（primary source）**保存在从 main 分出的 `prototype/<name>` 分支上，由实施 issue 指向它。它是主流程第 2 步里的那次绕道，但任何时候一个设计问题在纸面上难以定论，都可以用它。
- **`research` 技能**：把读材料的苦活交给一个**后台子代理**：它对着**一手来源**调查一个问题，然后在仓库里留下一份带引用的 Markdown 文件。它读的时候你继续干活。它产出的文件是要*带进*主流程、在 `grill-with-docs` 技能处使用的东西，因为研究是喂养思考，而不是替代思考。
- **`to-questionnaire` 技能**在你卡住的原因既不在你脑子里、也不在代码库里，而在**别人**那里时登场，它替那个人写一份问卷去填。它是 `grill-me` 技能的逆操作：它不是就主题来访谈你，而是就这次**发送**（发给谁、你需要拿回什么）来访谈你，并把问题对准那个缺口。拿回来的东西是 `grill-with-docs` 技能或 `to-spec` 技能的素材。
- **`wizard` 技能**用于只有**人**才能做的步骤：开通基础设施、设置凭据或 CI secret、在一个陌生的第三方控制台里点来点去、跑一次性的迁移或切换（cutover）。它会生成一个交互式 bash 脚本，逐个打开 URL、逐个捕获取值，并写进 `.env` 和 GitHub secrets，于是这套流程不再是你每次都要向代理重新解释的东西。它由模型自动调用，所以代理一旦撞上只有你能通过的那堵墙就会去用它。如果代理自己就能做，它就该自己做；这个技能是给「人确实在回路里」的场合用的。
- **`wait-what` 技能**是对一条没被听懂的讯息的纠正手段。在任何其他技能里、对话中途用它，代理会带着你缺的那部分上下文，用大白话、并使用 `GLOSSARY.md` 的词汇，把它刚才说的东西重新讲一遍。它是事后补救；`grill-with-docs` 技能是事前根治，因为早早达成一致的一套共同语言，才能从一开始就挡住那些行话。
- **`teach` 技能**：跨多个会话学一个概念，把当前目录当作一个有状态的工作区。
- **`writing-for-agents` 技能**是写「代理要消费的文档」时的参考：技能、AGENTS.md、被指向的文档。

## 前置条件

**`setup-matt-pocock-skills` 技能**：在第一次跑工程流程之前运行，配置其他技能所假定的 issue 追踪器、分诊标签和文档布局。自定义的 issue 追踪器也支持。

## 来源与致谢

本套技能（共 27 个）译自 **Matt Pocock** 的 [`mattpocock/skills`](https://github.com/mattpocock/skills) 仓库，遵循 MIT 许可。

- 原作者：Matt Pocock
- 上游仓库：<https://github.com/mattpocock/skills>
- 许可证：MIT，完整文本见 [references/UPSTREAM-LICENSE.md](references/UPSTREAM-LICENSE.md)
- 转换说明：为适配 WorkBuddy 做了四项改动 —— ① frontmatter 补全为开放平台的市场发布格式（`name` / `display_name` / `display_name_en` / `description` / `description_zh` / `description_en` / `category` / `version` / `author`）；② 正文与附属文档译为简体中文（技术术语保留英文原词）；③ 把 `/xxx` 形式的技能引用改写为「`xxx` 技能」，`sub-agent` 改写为「子代理（用 Agent 工具）」，Codex 专属的 `agents/openai.yaml` 丢弃；④ 上游的 `disable-model-invocation: true`（共 16 个技能）**原样保留** —— WorkBuddy 支持该字段，标记后 AI 不会自动触发、只能由用户手动调用。

`pr` 技能另有一份第三方署名，见 [../pr/references/CREDITS.md](../pr/references/CREDITS.md)。

上游如有更新，可对照本套技能的目录名（与上游同名）逐一 diff。
