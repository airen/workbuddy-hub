# 自动化办公助手 · 办妥（office-automation）

> 核心一句话：**AI 办公最让人心动的，是把手头那份文件往前推进。**

「办妥」是一个 WorkBuddy 单 Agent 专家，内置 5 个技能，灵感来自 5 个开源项目，已把它们的能力**内化**成可在 WorkBuddy 里直接落地的玩法。

| 技能 | 对应开源项目 | 解决的具体工作 |
|---|---|---|
| `doc-revise-diff` | [genspark-ai/genoffice](https://github.com/genspark-ai/genoffice) | 改文档/表格/PPT，AI 修改可看差异、可回退 |
| `task-to-file` | [CatCatUncle/openworkbuddy](https://github.com/catcatuncle/openworkbuddy) | 交代一句任务，拿到 PPT/Word/Excel/网页文件 |
| `excel-nl-edit` | [menahishayan/MS-Office-AI](https://github.com/menahishayan/ms-office-ai) | 在 Excel 里用自然语言请求更新单元格 |
| `doc-triage` | [nyxtron/paperless-aissist](https://github.com/nyxtron/paperless-aissist) | 整理存量文档：AI 分类、标题生成、字段提取、OCR |
| `office-sdk-embed` | [dream-num/univer](https://github.com/dream-num/univer) | 给内部工具加办公能力：嵌入表格与文档编辑 SDK |

## 怎么用

1. 在 WorkBuddy 里召唤「办妥」（或把它加入你的专家列表）。
2. **先用一份样例文件试跑一项每天重复的工作**——比如"把我上周周报整理成 PPT + Excel 数据表"。
3. 办妥会读取对应技能的模板/脚本，直接把文件往前推进，并告诉你这次做了什么、下次怎么复用、哪些能常态化。

## 每个技能交付什么

- `doc-revise-diff`：离线 `diff-viewer.html`（词级差异 + 回退）+ 改文档工作流
- `task-to-file`：`brief-template.yaml` 任务简报模板 + 一句话出文件工作流
- `excel-nl-edit`：自然语言改 Excel 食谱手册 + 用表格工具实操
- `doc-triage`：分类/字段提取 schema + AI 整理提示词
- `office-sdk-embed`：Univer 嵌入代码片段 + 内部工具集成清单

## 关于"毕业到原项目"

这 5 个开源项目很多需要自备运行环境、API Key 或商业授权（如 openworkbuddy 公司内部使用需商业授权、MS-Office-AI 需 Node.js + Gemini Key、paperless-aissist 需先有 Paperless-ngx、univer 功能授权需逐项看）。「办妥」先把能在 WorkBuddy 内直接落地的玩法给你跑通；需要更深能力时，每个技能里都标了**前置条件与授权提示**，让你自己判断要不要毕业到原项目。

## 文件结构

```
experts/office-automation/
├── .codebuddy-plugin/plugin.json
├── manifest.yaml
├── agents/office-automation.md        # 人设 + 路由 + 工作流
├── README.md
├── avatars/office-automation.jpg
└── skills/
    ├── doc-revise-diff/   references/diff-viewer.html
    ├── task-to-file/      references/brief-template.yaml
    ├── excel-nl-edit/     references/excel-edit-cookbook.md
    ├── doc-triage/        references/triage-schema.csv + classification-prompt.md
    └── office-sdk-embed/  references/univer-quickstart.ts + integration-checklist.md
```
