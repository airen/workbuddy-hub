---
name: task-to-file
display_name: 一句话出文件
display_name_en: Generate Files from a Brief
description: "Turn a one-line task into a ready file — PPT, Word, Excel, or a web page — locally. Use when the user gives a brief and wants a finished document, not just an answer. Inspired by CatCatUncle/openworkbuddy."
category: content
version: 1.0.0
author: 大漠
---

# 一句话出文件

对应开源项目 **CatCatUncle/openworkbuddy** 的核心能力：交代任务、拿到文件——在本机生成 PPT、Word、Excel 和网页。这里把它内化成一个**简报驱动**的工作流：用户给一句需求（或填好简报），「办妥」直接用 WorkBuddy 原生文档能力产出对应文件。

## 适用场景

- "帮我把这次项目复盘做成一份 12 页 PPT"
- "写一份给客户的需求说明书 Word"
- "按这批数据起一张 Excel 台账"
- "给这个活动做个落地页（网页）"
- 用户丢来一句模糊需求，要的是**文件**而不是聊天答案

## 输入

- 一句任务描述，或填好的 `references/brief-template.yaml`
- 可选：样例文件、数据、风格参照

## 执行步骤

### 1. 澄清产出类型
先确认要的是 **ppt / word / excel / web** 哪一种（用户没说就问，但给合理默认：汇报类默认 ppt、文档类默认 word）。一次主打一种；要多文件就分步。

### 2. 套用简报
读取 `references/brief-template.yaml`，把用户的口语需求映射到字段：
- `output_type`、`title`、`audience`、`goal`、`outline`、`style`、`length`、`data_source`、`constraints`
- 缺失的用自己的合理默认补上，并明确告诉用户"我替你定了 X，要改说一声"。

### 3. 生成文件（用平台原生能力）
- **PPT**：调用演示文稿生成能力，产出 `.pptx`，按 `outline` 落页、每页给要点与版式。
- **Word**：调用文档生成/排版能力，产出 `.docx`。
- **Excel**：用表格生成能力，产出 `.xlsx`（先定表头与示例行，再填数据）。
- **Web**：产出单页 `index.html`（自包含、双击即开），内容区块按 `outline` 排。

### 4. 交付
- 文件写入用户工作区，路径回给用户（如 `项目复盘.pptx`）。
- 附一句"这次按什么简报做的、哪些是我替你定的默认"，并给简报路径方便下次复用。

### 5. 常态化（重复工作）
- 高频任务（如周报 PPT + 数据表）把简报存成模板，下次填关键变量直接跑。
- 与 `doc-revise-diff` 衔接：先 `task-to-file` 出初稿，下次在旧版上 `doc-revise-diff` 迭代。

## 毕业到原项目（openworkbuddy）的提示

openworkbuddy 强调"本机生成 PPT/Word/Excel/网页"，但官方明确：**公司内部使用也需商业授权**。
- 个人本机试用前先看其 LICENSE 与授权条款；**任何公司/团队内部使用场景，必须先确认已获商业授权**，否则不要用它。
- 「办妥」默认用 WorkBuddy 原生文档能力产出文件，不依赖 openworkbuddy；只有在你已确认授权、且需要它特定的本机生成管线时，才考虑引入。
- 涉及**公司机密/对外正式文件**，产出后务必人工复核，不把"已生成"等同于"已合规"。

## 边界

- 不替用户做不可逆覆盖；新文件单独命名（加 v2 / 日期），不原地改用户原文件。
- 数据来源要透明：用了用户给的数据就说明，自己编的示例要标"示例数据，请替换"。
- 网页产物为自包含静态页；不含后端、不收集数据。
