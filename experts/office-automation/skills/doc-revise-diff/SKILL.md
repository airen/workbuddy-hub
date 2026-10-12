---
name: doc-revise-diff
display_name: 改文档看差异可回退
display_name_en: Revise Docs with Diff & Rollback
description: "Revise Office documents (Word/Excel/PPT) with visible, word-level diffs and one-click rollback. Use when the user wants to change a doc, see exactly what changed, and be able to revert. Inspired by genspark-ai/genoffice."
category: content
version: 1.0.0
author: 大漠
---

# 改文档看差异可回退

对应开源项目 **genspark-ai/genoffice** 的核心能力：改文档、表格、PPT，AI 修改可查看差异、可回退。这里把它内化成一个**可落地的工作流**——在 WorkBuddy 里真正把文档改好，并用离线工具把"改了什么 / 怎么回退"讲清楚。

## 适用场景

- "帮我把这份需求文档改成 v2，标出改了哪些地方"
- "上周的周报你帮我改一版，我要能对照旧版、能退回"
- "这两份文案哪里不一样？"
- "把这段删掉、那段扩写，改完给我新旧对比"

## 输入

- 用户要改的源文件（Word / Excel / PPT / 或 Markdown、纯文本）
- 修改意图（口述或清单）：删哪、改哪、加哪、语气/格式要求
- 是否要"保留旧版可回退"（默认要）

## 执行步骤

### 1. 取旧版、定新版
- 若用户给的是 Office 原文件（.docx/.xlsx/.pptx），用 WorkBuddy 的**文档处理技能**（tencent-docx / 表格处理技能）读取并修改，产出 `xxx-v2.<ext>`，同时**保留原文件不动**。
- 若用户给的是 Markdown / 纯文本，直接读文本改。

### 2. 生成差异说明
- 改完不要只丢一个新文件，要给用户一份**旧 → 新 的差异说明**：列出每处改动（"第 2 段：删去…；第 5 节：新增…"）。
- 对文本 / Markdown 类内容：用本技能的离线工具 `references/diff-viewer.html` 做**词级差异**展示，红=删除、绿=新增，并支持一键复制/下载任一版本（即"回退"）。

### 3. 交付
- 改好的文件：`xxx-v2.<ext>`（Office）或 `xxx-v2.md`（文本）
- 差异说明：聊天内列出 +（文本类）附 `diff-viewer.html` 让用户自己贴新旧文看
- 回退方式：旧版原文件仍在；文本类也可在 diff-viewer 里"复制旧版"一键还原

### 4. 常态化（重复工作）
- 若用户每周都改同类文档（如周报、需求稿），把这次的修改意图沉淀成一份**修订简报模板**（可复用），下次填好直接跑。

## 离线工具：`diff-viewer.html`

路径：`skills/doc-revise-diff/references/diff-viewer.html`
- 纯前端，数据存浏览器 `localStorage`，**不联网、不需要 key**
- 左贴旧版、右贴新版（或导入 .txt/.md），点「查看差异」出词级对比
- 「复制旧版（回退）」「下载旧版 .txt」即实现回退；「复制/下载新版」取改后结果
- 适合文档/文案/代码类文本对比；Office 二进制建议先导出文本或直接在 Office 技能里改完看差异说明

## 毕业到原项目（genoffice）的提示

genoffice 支持**原生 Office 格式**的 AI 修改与差异/回退，能力更深。但使用前需确认：
- 它有自己的运行环境/部署要求（以官方仓库 `genspark-ai/genoffice` 最新说明为准）
- 涉及**上传/处理用户文档**时，确认数据流向与隐私合规，别把敏感文档交给不明确的服务
- 本技能已在 WorkBuddy 内用原生文档能力覆盖"改 + 看差异 + 回退"的主流程；只有当你需要**原生 Office 内联差异UI、复杂格式保真**等更深能力时，再考虑部署 genoffice。

## 边界

- 不替用户做不可逆的覆盖/删除；旧版默认保留。
- 涉及法律/合同/对外正式文书的改版，改动点要标清楚让用户自己审，不下"已合规"结论。
- 大段扫描件 PDF（图片型）的差异比对超出本技能范围，转 `doc-triage` 先做 OCR/结构化。
