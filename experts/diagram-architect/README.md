# Diagram Architect · 江图南

把模糊的绘图需求变成可交付的图表：**定图型、定出口，调度五套绘图能力库，过机械质检再交付。**

## 类型

Agent 型（单个 AI 专家）。花名 **江图南**，职业 **图表架构师**，类目 `02-Engineering`。

## 为什么做成 Agent 型

五个上游项目**全都没有 persona 文件**——它们是一个绘图任务的不同工具与阶段，不是独立专家。
强行拆成专家团需要凭空造出五个并不存在的角色，而且它们之间没有真正的并行审查关系。
用户诉求本身（「画个图」）也是**选哪个能力库**的路由问题，正是主理人的职责。

## 内置技能（6 个）

| 技能 | 来源 | 提供什么 | 运行时 |
|---|---|---|---|
| `diagram-architect` | **本包新增** | 入口编排：四个决定（该不该画 / 画哪种 / 画到哪 / 怎么验）+ 全技能路由表 + CJK 硬规矩 + WorkBuddy 渲染边界 | — |
| `diagram-design` | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | **44 种图型**参考、语义模式、编辑风设计系统、强制连接线规则、draw.io/Mermaid/Excalidraw 导入、PNG/SVG 导出 | Python 3 标准库 |
| `svg-diagram` | [bybit-exchange/svg-diagram](https://github.com/bybit-exchange/svg-diagram) | 手写 SVG 家规（布局算术 / 箭头几何 / **CJK 字体栈与字符宽度表**）+ **`svg-lint` 12 项检查闸门** | Node，零依赖 |
| `dashmotion` | [csthink/dashmotion](https://github.com/csthink/dashmotion) | 动画图（流动虚线 + 光点）、`layout.py` 确定性布局、`check_diagram.py` 结构自检、`check_fidelity.py` 保真复核 | Python 3 标准库 |
| `documd-visuals` | [markdown-viewer/skills](https://github.com/markdown-viewer/skills) | **9 套主题配色契约**（含对比度阈值与无障碍/印刷/投影变体）、31 个目标域路由、HTML/CSS 架构图版式、242 个已验证示例 | 见下方「渲染边界」 |
| `archify` | [tt-a1i/archify](https://github.com/tt-a1i/archify) | typed JSON IR → **可交互 HTML**：5 种图型 schema + 渲染器 + 校验门禁 + Before/After 架构对比 | Node，零依赖 |

## 比上游多了什么

上游技能都面向 Claude Code / 文件系统，直接搬进来会「水土不服」。本包补的是它们都没有的那一层：

1. **出口决策**。同一张图落在对话里还是落成文件，尺寸与主题完全不同——上游技能不区分这两者。
   本包定死了三条路径：内联 widget（`viewBox` 必须 `0 0 680 H`）/ 落盘交付 / 两者都要。
2. **主题跟随当前 IDE 主题**。上游的默认皮肤（暖纸底、深色发光底）只在明确要求时才用。
3. **中文优先**。CJK 字体栈、中文字符宽度估算（中文字宽 ≈ 字号，拉丁字母 ≈ 0.58 倍）、竖排禁忌，
   都提到硬约束位置，而不是画完再补的细节。
4. **可证明的质检闸门**。交付前必须跑得动的脚本：`svg-lint`（一条 warning 也算不合格）、
   `check_diagram.py`、`self_check.py`、archify 的 `deliver`。跑不了就如实说「这次只做了人工核对」。
5. **诚实的渲染边界清单**。明确写清哪些能跑、哪些只是参考（见下）。

## 实测过的环境结论

| 结论 | 证据 |
|---|---|
| `svg-lint` 可直接运行 | Node 22，零依赖 |
| `dashmotion` 三个脚本可直接运行 | Python 3.13 标准库 |
| `diagram-design` 五个脚本可直接运行 | Python 3.13 标准库 |
| **`archify` 零依赖，不需要 `npm install`** | `package.json` 里 5 个包全是 `devDependencies`，只服务于上游测试套件；删掉 `node_modules` 后 `doctor` 全绿、`deliver` 正常产出 767 KB 成品 |
| **archify 用 `deliver`，不要用 `finalize`** | `finalize` 的最后一关 `browser-check` 要拉起 Chrome，而 Chrome 自身沙箱在受管环境里初始化不了（`sandbox initialization failed: Operation not permitted`）。关掉外层沙箱复测同样失败，所以不是本环境特有。前三关 `validate` / `deliver` / `check` 全过 |
| **`documd-visuals` 的四种围栏渲染不了** | `plantuml` / `vega` / `echarts` / `infographic` 需要 docu.md 的 Markdown Viewer 实时渲染，WorkBuddy 里没有这条管线。可用的只有它的**裸 HTML 路径**与**9 套主题配色**；其余取设计意图，手写成裸 HTML/SVG |

## 使用示例

- 把这个系统的架构画成一张图，标出主要请求路径
- 把这段流程画成流程图，分支和汇合要一眼看清
- 这张图太丑了，按技术文档的标准重画一版
- 用 dashmotion 把我们的 CI/CD 流程画成会动的图
- 把这段 Mermaid 转成一张能直接用的可交互架构图
- 我要往技术文档里插一张时序图，给我一份能落盘的 SVG

## 交付规范

每次交付给出**四件套**：图型 / 出口 / 质检结论（跑了什么、什么结果；没跑就说明没跑）/ 被预算挤掉的内容。

## 头像

`avatars/diagram-architect.jpg`，512×512，约 88 KB。

## 安装

```bash
python3 <expert-manager>/scripts/register_expert.py <expert-dir>
```

## 打包

```bash
python3 <expert-manager>/scripts/package_expert.py <expert-dir> <输出目录>
```

> 打包必须从**专家目录下的真身**打，输出到目标目录；镜像副本只用于留档，不能拿来打包。

## 许可

本包新增部分 MIT。`skills/` 下五个技能目录是上游开源项目的移植内容，各自保留原许可
（`diagram-design` / `svg-diagram` / `dashmotion` / `archify` 为 MIT，`documd-visuals` 为 CC-BY-4.0）。
搬运范围、版权行与全文位置见 [`LICENSE`](LICENSE)。
