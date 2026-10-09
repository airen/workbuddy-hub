---
name: diagram-architect
description: 画图请求的总入口与调度层。任何"画个图 / 出张架构图 / 把这段流程画出来 / 做成流程图 / 可视化一下这个系统 / 这张图太丑重画"的请求，先走这里：判定值不值得画、选图型与出口（对话内联 SVG/HTML widget，还是落盘 .svg/.html 交付物）、调度 svg-diagram / diagram-design / dashmotion / documd-visuals / archify 五个能力库、跑质检闸门，最后交付。覆盖流程图、架构图、时序图、状态机、数据流、ER 图、泳道图、时间线、象限图、甘特图、组织架构、看板、用户旅程、鱼骨图、桑基图、爆炸轴测图、Venn、金字塔等 40 余种图型，以及动画图与可交互图。
---

# 图表总入口

一个画图请求进来，**先在这里做四个决定，再去加载任何图型参考**：

| # | 决定 | 去哪一节 |
|---|---|---|
| 1 | 该不该画？画几张？ | §0 |
| 2 | 画哪种图？ | §1 出口决策 → §2 图型路由 |
| 3 | 画到哪？ | §1 |
| 4 | 怎么证明画对了？ | §5 质检闸门 |

不要跳过。跳过 §0 会产出没人看的图；跳过 §1 会把该内联的图写成文件；跳过 §5 会交付一张箭头穿过方框的图。

---

## §0 先问「值不值得画」

最高质量的动作常常是**删**。

- 三列表格能说清的事，**用表格**，不要画图。
- 一句话能说清的事，**直接写那句话**。
- 读者从图里学到的信息不比一段好文字多 → 不画。

判定完还要定**张数**。单图复杂度上限（借 diagram-design 的预算，全包通用）：

| 上限 | 值 |
|---|---|
| 节点 | 9 |
| 箭头 / 转移 | 12 |
| 强调色元素 | 2 |
| 批注标注 | 2 |

超了就**拆成「总览 + 细节」两张**，不要塞进一张。密度目标 4/10：技术信息完整，但不需要配导读。

**动手前先一句话报方案**：图型、尺寸预设、会被预算挤掉什么。用户能回话就让他先改；不能回话就照画，并在交付物旁边注明假设。

---

## §1 出口决策（WorkBuddy 特有，上游技能都没有这一节）

同一张图，**落到哪里**决定它长什么样。先定出口，再定尺寸。

| 出口 | 什么时候用 | 怎么交付 | 硬约束 |
|---|---|---|---|
| **A. 对话内联** | 解释、教学、快速看图、"给我看一眼" | `show_widget`，传原始 SVG/HTML 片段 | SVG 的 `viewBox` **必须以 `0 0 680 ` 开头**；不写 `<html>/<head>/<body>`；无外部依赖 |
| **B. 落盘交付** | 文档配图、归档、分享、要进 git、要插进 md | 写文件 + `present_files` | 单文件自包含；`.html` 会自动开预览面板 |
| **C. 两者都要** | 技术文档里既要给人看又要落盘 | 先 A 后 B，或直接把 B 的产物送进 A | 内联版要重算 `viewBox` 宽度到 680 |

判定顺序：用户说了"文件/保存/给我一份/插到文档里" → **B**；说了"看看/什么样/演示一下" → **A**；没说 → 默认 **A**，交付时补一句"需要落盘的话我存成文件"。

⚠️ **A 与 B 的尺寸不同，不能直接复用**：内联版按 680 宽重排；落盘版按 §4 的尺寸预设走。同一张图两处都要时，**画两次**，不要把一个 viewBox 硬塞进两处。

### 主题必须跟随当前 IDE 主题

- 亮色主题 → 浅底 + 深字；**不要**交付深色底发光图。
- 暗色主题 → 深底 + 浅字，且文字对比度要够。
- 上游技能的默认皮肤（diagram-design 的暖纸 `#f5f4ed`、dashmotion 的 `#020617` 深底）**只在落盘交付且用户明确要那个风格时**才用。内联 widget 一律先对齐当前主题。

---

## §2 图型路由

先判**大类**（静态 / 动画 / 可交互），再进具体图型。

### 2.1 大类判定

| 用户意图里出现 | 走 | 加载 |
|---|---|---|
| 请求、事件、数据、任务、消息在**流动**；"让路径动起来"；"像官网那种会动的图"；"把这段 mermaid 变成动画" | **动画图** | [`dashmotion`](../dashmotion/SKILL.md) |
| 要**点、要探索、要分享链接**、要 Before/After 对比、要导出、要暗/亮主题切换 | **可交互图** | [`archify`](../archify/SKILL.md) |
| 静态的架构/流程/时序/状态/数据流/ER/图表/信息卡 | **静态图** | [`diagram-design`](../diagram-design/SKILL.md) 为主 |
| 要**排版成 markdown 文档里的图**，或需要成套主题配色（含印刷/无障碍/投影变体） | **静态图（文档向）** | [`documd-visuals`](../documd-visuals/SKILL.md) |
| 需要**手写精确坐标的 SVG**、或要过严格几何校验（CJK 标签、箭头间隙、viewBox 裁剪） | **静态图（工程向）** | [`svg-diagram`](../svg-diagram/SKILL.md) |

**动画 vs 静态的判断**：图上有没有「在动的东西」——请求、事件、数据、作业、消息、控制流。有 → 动画（dashmotion）；只有结构 → 静态。
**交互 vs 静态的判断**：读者会不会想「点一下看看」「走一遍路径」「对比两个版本」。会 → archify；不会 → 静态，别为炫技加交互。

### 2.2 静态图型速查（详细清单见 diagram-design 的 44 型表）

| 要表达 | 图型 | 参考 |
|---|---|---|
| 一个系统快照：组件 + 连接 | 架构图 | `diagram-design/references/type-architecture.md` |
| 决策分支 | 流程图 | `type-flowchart.md` |
| 时间上有序的消息 | 时序图 | `type-sequence.md` |
| 状态 + 转移 + 守卫 | 状态机 | `type-state.md` |
| 实体 + 字段 + 关系 | ER / 数据模型 | `type-er.md` |
| 跨职能流程与交接 | 泳道图 | `type-swimlane.md` |
| 时间轴上的事件 | 时间线 | `type-timeline.md` |
| 双轴定位 / 优先级 | 象限图 | `type-quadrant.md` |
| 任务与阶段排期 | 甘特图 | `type-gantt.md` |
| 汇报线 / 归属 / 升级路径 | 组织架构 | `type-org-chart.md` |
| 各状态的在制品与阻塞 | 看板 | `type-kanban.md` |
| 用户跨阶段的经历与感受 | 用户旅程 | `type-journey.md` |
| 因果归因 | 鱼骨图 | `type-fishbone.md` |
| 数量在阶段间分流合并 | 桑基图 | `type-sankey.md` |
| 沿一个轴拆解一个物体 | 爆炸轴测图 | `type-exploded.md` |
| 集合重叠 | Venn | `type-venn.md` |
| 层级或转化流失 | 金字塔 / 漏斗 | `type-pyramid.md` |
| 数据管线 / 血缘 / 角色分工 | 数据流 | `type-data-flow.md` |
| 代码跑在哪：区域 / 主机 / 副本 | 部署图 | `type-deployment.md` |
| 谁依赖谁，含扇入与环 | 依赖图 | `type-dependency.md` |

**完整 44 型清单、语义模式（semantic patterns）、尺寸预设、反模式**：见 [`diagram-design/SKILL.md`](../diagram-design/SKILL.md)。**动手前必须加载被选中图型的 type 参考**——不要凭印象画。

### 2.3 语义模式优先于图型

当**行为、状态、强制、风险**承载含义时（不是纯结构），先加载 `diagram-design/references/semantic-patterns.md` 选一个主模式，再挑最近的图型承载版式。九个已定义模式（扇入排队/瓶颈、阶段框架语义槽、非结构化输入→结构化产物、配对策略评估轨迹、安全铺装路、治理控制目录、补偿性安全层、可追溯块分解、生命周期阶段图）及其对应图型见该文件。

---

## §3 中文与 CJK（本包的第一优先级，不是附注）

上游技能大多以英文标签为前提。中文用户的实际失败点集中在**字体与宽度**两处，所以这两条是硬规矩：

1. **每个落盘 SVG 必须在 `<style>` 里声明 CJK 字体栈**（不可省略，否则 Linux 服务端渲染会掉成豆腐块）：

   ```xml
   <style>
     text { font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans CJK SC', system-ui, sans-serif; }
   </style>
   ```

   `Noto Sans CJK SC` **必须保留**。完整规则与字符宽度表见 [`svg-diagram/SKILL.md`](../svg-diagram/SKILL.md)。

2. **估宽度按中文算，不要按英文算**。同一个字号，一个中文字 ≈ 一个字宽，一个拉丁字母 ≈ 0.58 个字宽：

   | 字号 | 拉丁字符宽 | 中文字符宽 |
   |---|---|---|
   | 10px | 5.5px | 10px |
   | 12px | 7.0px | 12px |

   放标签前先估右边界：`文字右边界 + 10px < 右侧邻居的左边界`。中文标签超宽是这类图最常见的破相方式。

3. **中文标签不要在 SVG 里竖排**（`writing-mode="tb"`）。上游 diagram-design 明确列为反模式。

4. 图内的**技术子标签**（端口、命令、URL）用等宽字体；**人名、模块名**用无衬线，不要整张图都用等宽。

---

## §4 尺寸与版式

### 内联 widget

- SVG `viewBox` **必须**是 `0 0 680 H`（H = 最低元素底边 + 余量）。
- 画布宽度写死 680，高度按内容算；不要用百分比、不要 `width="100%"`。
- 上下左右留白对称；内容不对称时用 `<g transform="translate(dx,0)">` 整体挪，不要去改每个坐标。

### 落盘交付

尺寸预设（`diagram-design/references/output-spec.md` 为准）：

| 预设 | 用途 |
|---|---|
| `doc-inline`（默认） | 文档内嵌 |
| `doc-wide` | 文档宽版 |
| `slide-16x9` / `slide-4x3` | 幻灯片 |
| `social-og` / `social-square` | 社交分享卡 |
| `print-a4-landscape` / `print-a3-landscape` | 打印 |
| `fit` | 贴合内容 |

尺寸预设同时决定 `viewBox` **和**字号阶梯。**只换 viewBox 不换字号 = 字被压扁**。

### 通用几何（所有出口都适用）

- 结构几何落在 **4px 网格**上（原点、宽、高、间距、内边距）。
- 盒子高度从字号推：单行 = `字号 × 3`，每多一行加 `字号 × 1.5`。
- 框内文字垂直居中：`y = 盒 y + 盒高/2 + 字号 × 0.35`（`0.35` 是基线偏移经验值，别和标题的 `0.75` 升部系数搞混）。
- 相邻方块间距 **≥25px**（25–30 推荐），太小箭头退化成点，太大整张图发散。
- 箭头起点离源框 5px、终点离目标框 11px（5px 间隙 + 6px 箭头尖），**两端间隙对称**。
- 画序：背景分组框 → 连接线 → 盒子与文字 → **跨层回环线**（最后画，否则被盒子盖住）。
- 连接线**只能正交**（同轴直线，或 `r=8` 圆角折弯）。**对角线斜插直接判不合格**。

---

## §5 质检闸门（不过不许交付）

「我看着没问题」不算。跑得动的就一定要跑。

| 产物 | 闸门 | 命令 |
|---|---|---|
| 手写 `.svg` | **svg-lint**（12 项检查：转义、viewBox 裁剪、字体栈、盒高、基线、间距、箭头、溢出、重叠、浅底兜底、配色、连接几何） | `node <skill>/svg-diagram/tools/svg-lint/bin/svg-lint.mjs <file>.svg` |
| dashmotion 动画 HTML | **结构自检**（重叠、线穿框、虚线循环接缝、越界、光点脱线、黑填充、端点穿刺、悬空 `begin`） | `python3 <skill>/dashmotion/scripts/check_diagram.py <file>.html` |
| 由 Mermaid 转来的动画 | **保真度复核**（源节点/边/分组标签逐字出现，连接数一致） | `python3 <skill>/dashmotion/scripts/check_fidelity.py <src>.mmd <out>.html` |
| diagram-design 产物 | **自检**（可访问 SVG 契约、单文件安全、动效基础） | `python3 <skill>/diagram-design/scripts/self_check.py <file>.html` |
| archify 可交互图 | **三关门禁**（schema 校验 + 原子交付 + 严格检查） | `node <skill>/archify/bin/archify.mjs deliver <type> <candidate.json> <out.html> --quality showcase --json` |
| 内联 widget | 无法跑脚本 → 走 §6 人工清单，**且必须逐条报出结论** | — |

**判据**：`svg-lint` 必须 `0 errors, 0 warnings`——**一条 warning 也算不合格**。其他脚本必须打印通过。

⚠️ **archify 用 `deliver`，不要用 `finalize`**。`finalize` 的最后一道 `browser-check` 要拉起 Chrome 做真实浏览器检查，而 Chrome 自身的沙箱在受管环境里会起不来（`sandbox initialization failed: Operation not permitted`），这一关**必然失败**。实测 `deliver` 的三关（`validate` / `deliver` / `check`）全过并产出成品，所以走 `deliver`。详见 §8。

跑不动（没有 Node / Python）时，**明确告诉用户「这次只做了人工核对，没跑脚本」**，不要含糊过去。

---

## §6 交付前人工清单

脚本看不到的，靠读数字核对（不是靠"看起来还行"）：

- [ ] `viewBox` 宽高与内容吻合，底部 = 最低元素底边 + 25px，**没有负坐标**
- [ ] 左右留白对称、上下留白可比（20–25px）
- [ ] 每个盒子的文字右边界没侵入右侧邻居
- [ ] 曲线上的标签离曲线最近点 ≥15px（下弯放上面、上弯放下面）
- [ ] 每条连接线**有含义**：要么有标签，要么源与目标从上下文可推
- [ ] 图例在内容区**外**（底部横条或侧边），不在图里飘
- [ ] 强调色只落在 1–2 个元素上
- [ ] `<svg>` 有 `role="img"`，`<title>` 是第一个子元素，`<title>`/`<desc>` 都填了，且 id 带图名前缀
- [ ] 无大面积空白区（间距 ≤30px，viewBox 贴合内容）
- [ ] 主题与当前 IDE 主题一致

---

## §7 全技能路由表

| 技能 | 什么时候加载 | 它提供什么 |
|---|---|---|
| [`diagram-design`](../diagram-design/SKILL.md) | 静态图**默认加载**；需要具体图型的版式规则、编辑风设计系统、从 draw.io/Mermaid/Excalidraw 重绘、导出 PNG/SVG 时 | 44 种图型参考 + 语义模式 + 设计令牌 + 强制连接线规则 + 4 个导入/导出/自检脚本 |
| [`svg-diagram`](../svg-diagram/SKILL.md) | 需要**手写精确坐标**、要过严格几何校验、要 CJK 字体栈与宽度表、要一个可证明的 lint 闸门时 | 布局算术 + 配色语义三元组 + 箭头几何 + `svg-lint`（零依赖 Node，12 项检查） |
| [`dashmotion`](../dashmotion/SKILL.md) | 图上有**在流动的东西**（请求、事件、数据、作业、消息、控制流）；用户说"会动的/动态的/动画"；要转换 Mermaid `flowchart`/`stateDiagram-v2` | Flow 与 Architecture 两模式 + `layout.py` 确定性布局引擎 + `check_diagram.py` 结构自检 + `check_fidelity.py` 保真复核 |
| [`documd-visuals`](../documd-visuals/SKILL.md) | 图要**排进 markdown 文档**；需要**成套主题配色**（默认/编辑/石板/印刷/鲜明/无障碍/高对比/柔和/北欧）；需要 31 个目标域的选型与示例 | 主题配色契约（含对比度阈值）+ HTML/CSS 版式规则 + 图表数据形态指引 + 242 个已验证示例 |
| [`archify`](../archify/SKILL.md) | 要**可交互**（点击节点、追踪上下游、精确路径、角色对比）、要 Before/After 架构对比、要导出分享卡、要暗/亮主题切换 | typed JSON IR + 5 种图型的 schema 与渲染器 + 校验门禁 + 原子交付 |

**加载原则**：先按 §2 定大类，只加载该大类需要的技能 + 被选中图型的那一份参考。**不要一次把五个技能全读进来**——那会稀释判断力，也浪费时间。

---

## §8 本包在 WorkBuddy 里的渲染边界（诚实清单）

上游技能里有相当一部分依赖它们自己的渲染管线。在这里**能跑**和**只是参考**要分清，不要对用户吹牛：

**能直接跑（有本地运行时）**

- `svg-diagram` 的 `svg-lint`——Node，**零依赖**，直接跑。
- `dashmotion` 的 `layout.py` / `check_diagram.py` / `check_fidelity.py`——Python 标准库，直接跑。
- `diagram-design` 的 `self_check.py` / `drawio_extract.py` / `mermaid_extract.py` / `excalidraw_extract.py` / `export_svg.py`——Python 标准库，直接跑。
- `archify` 的 CLI——Node，**实测零依赖，不需要 `npm install`**（`package.json` 里的 5 个包全是 `devDependencies`，只服务于它自己的测试套件）。`doctor` 全绿，`deliver` 产出成品。

**能跑但有一关跑不了**

- `archify` 的 `finalize`：`validate` / `deliver` / `check` 三关通过，**最后一道 `browser-check` 必然失败**——它要拉起 Chrome 做真实浏览器检查，而 Chrome 自身的沙箱在受管环境里初始化不了（`sandbox initialization failed: Operation not permitted`）。关掉外层沙箱也一样，所以这不是本环境特有的限制。**用 `deliver` 代替 `finalize`**；确实需要浏览器级证据时，设 `ARCHIFY_CHROME` 指向一个可用的 Chrome/Chromium 再试。

**只是参考，不能当渲染引擎用**

- `documd-visuals` 的 `plantuml` / `vega` / `echarts` / `infographic` 四种围栏：它们是**给 docu.md 的 Markdown Viewer 实时渲染**的。WorkBuddy 里没有这条管线，写进 markdown 只会显示成代码块。**要用它们的内容，就读它的版式与数据形态，然后手写成裸 HTML/SVG**。
  - 例外：`documd-visuals` 的 **裸 HTML** 路径（系统架构图、卡片、页面版式）和 **9 套主题配色**在 WorkBuddy 里直接可用。
  - 它的 `converting.md` 里那条 `npx @markdown-viewer/documd` 导出命令也依赖外部 CLI，不要默认可用。

判断依据：**产物最终由谁渲染**。WorkBuddy 能渲染的只有「裸 HTML/CSS」「内联 SVG」「浏览器里的自包含 HTML」三类。凡是需要别的引擎解释的语法，都只能取它的设计意图，不能取它的语法。

---

## §9 输出规范

- 交付时一并给出：**图型**、**出口**（内联 / 文件路径）、**质检结论**（跑了什么脚本、什么结果；没跑就说明没跑）、以及**被预算挤掉的内容**。
- 落盘产物用 `present_files` 呈现；HTML 会自动开预览面板。
- 图里的文字用**用户的语言**（中文请求就全中文），只有技术子标签（端口、命令、URL、API 名）保留原文。
- 不要在图里塞图例解释图例；不要给图配一段复述图内容的文字。
