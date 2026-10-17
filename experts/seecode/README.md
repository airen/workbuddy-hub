# SeeCode 专家（顾见）

一句话生成**可交互、可动画、可导出**的图表专家。用户描述「要讲清楚什么」，专家只写一段紧凑 JSON 规格，
布局、连线、排版、动效、质检、导出全部由随包 CLI（`skills/seecode/scripts/seecode.mjs`，Node.js ≥ 20）完成。

- 45 种图型 + 15 种变体：架构、流程图、时序、状态机、ER/数据库 schema、UML、泳道、时间线、甘特、
  旅程、树/组织架构、四象限、鱼骨图，以及柱状/折线/散点/桑基/树图/热力/雷达等数据图表
- 等距 3D：任意物体、爆炸分解图、平面图（solids + beams 组合，无素材库依赖）
- 导入既有资产：Mermaid、Graphviz/DOT、PlantUML、D2、draw.io、Excalidraw、SQL/Prisma/DBML、OpenAPI、CSV
- 品牌主题：从网站或仓库学习配色与字体；交互能力（悬停追踪、点击聚焦、路径走查、分步演示）
- 导出：SVG / PNG / JPEG / GIF / MP4 / 自包含交互 HTML

## 目录结构

```
seecode/
├── .codebuddy-plugin/plugin.json   # 平台插件清单（name/plugin/agentName 三处一致）
├── agents/seecode.md               # 专家人格与工作流程（顾见）
├── skills/seecode/                 # 上游 SeeCode 技能（MIT），含：
│   ├── SKILL.md                    #   技能入口（补了 version/category 两个 frontmatter 字段）
│   ├── references/                 #   图型文档 45+ 篇 + spec/import/export/settings 等
│   ├── schemas/                    #   28 个 JSON Schema（渲染前校验规格）
│   ├── scripts/                    #   seecode.mjs CLI + lib/ + vendor/（零第三方运行时依赖）
│   ├── assets/                     #   站点图标与水印标识
│   └── examples/specs/             #   上游示例规格（charts/everyday/isometric/...）
├── avatars/seecode.jpg             # 默认头像
├── manifest.yaml                   # 本仓资产登记
├── README.md
└── LICENSE                         # MIT，含上游归属说明
```

## 使用示例

```text
把这个系统的架构画成一张可交互的图，标出主要请求路径
把 docs/architecture.mmd 重绘成 SeeCode 风格的图并导出 SVG
用等距 3D 画一个 AI Agent 技术栈的爆炸分解图
```

## 上游归属

`skills/seecode/` 移植自 [Aryanutkarsh/SeeCode](https://github.com/Aryanutkarsh/SeeCode)（MIT License, © 2026 Aryanutkarsh），
版本 `0.6.1`，目录布局原样保留，`examples/specs/` 取自上游 `examples/specs/`。
专家包其余部分（`plugin.json`、`agents/`、`README.md`、`manifest.yaml`）为本仓新增，同为 MIT。
详见 [LICENSE](./LICENSE)。

## 环境要求

- Node.js ≥ 20（CLI 为 `.mjs`，零第三方运行时依赖）
- 导出 PNG/GIF/MP4 另需本地 Chrome/Edge；SVG 导出只需 Node
