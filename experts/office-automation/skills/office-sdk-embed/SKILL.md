---
name: office-sdk-embed
display_name: 给内部工具嵌办公能力
display_name_en: Embed Office SDK into Internal Tools
description: "Add in-app spreadsheet/document/slide editing to internal tools via an embeddable office SDK. Use when the user (typically a developer) wants to put editable Office-like capabilities inside their own system. Inspired by dream-num/univer."
category: content
version: 1.0.0
author: 大漠
---

# 给内部工具嵌办公能力

对应开源项目 **dream-num/univer** 的核心能力：面向开发者的 SDK，可嵌入表格与文档编辑。这里把它整理成一份**开发者向**的接入指引——当团队想在自己的后台/知识库/低代码平台里加"在线表格/文档编辑"时，「办妥」给出起步代码与集成清单。

## 适用场景

- "我们后台想加个能在线编辑的表格，不用导出 Excel 再传"
- "知识库里想直接嵌文档编辑器"
- 开发者来问"怎么把办公能力嵌进我们的系统"

## 输入

- 目标系统形态（Web 后台 / 低代码平台 / 内部工具）、前端框架
- 想要的能力（表格 / 文档 / 幻灯片 / 协同）
- 数据归属与权限要求

## 执行步骤

### 1. 先过授权（最重要）
读取 `references/integration-checklist.md` 的「授权与合规」一节，先和用户确认：
- **功能授权需逐项看**：univer 各模块（Sheets/Docs/Slides/协同/公式）授权可能不同，先核对要用的功能在不在范围内。
- 自托管 vs 云、开源协议是否允许公司内部商用、是否要采购授权。

### 2. 给起步代码
读取 `references/univer-quickstart.ts`，按用户的前端框架给一份**可运行的嵌入示例**（创建实例 → 挂载 UI → 建/载表格 → 与业务系统对接的钩子）。
- 明确标注：Univer API 迭代较快，包名/路径/参数以官方最新文档为准。

### 3. 走集成清单
用 `integration-checklist.md` 陪用户逐项过：依赖与构建、容器样式、数据打通（getData/load 序列化）、鉴权、性能与协同、监控与版本锁定。

### 4. 衔接其他技能
- `task-to-file` 产出的 .xlsx/.docx 可导入嵌入编辑器继续协同。
- `doc-triage` 的清单可放进嵌入表格做看板。
- `excel-nl-edit` 的"自然语言改表"可接一层指令解析，调用 univer API 落地。

## 毕业到原项目（univer）的提示

- univer 是**开发者 SDK**，不是开箱即用的办公应用；嵌入需要前端工程能力。
- **功能授权需逐项看**，商用前务必核对授权范围与协议，必要时走采购。
- 「办妥」给的是接入思路与起步代码；真正落地由贵司开发按官方文档完成。

## 边界

- 这是开发者向技能，非给最终用户直接产文件；最终用户要的是文件本身，请路由到 `task-to-file` / `excel-nl-edit`。
- 涉及公司内部系统安全、数据出境、采购合规的，只给检查项与提示，不替用户做合规拍板。
- 代码示例标注"示意/以官方为准"，不保证与最新版本一字不差。
