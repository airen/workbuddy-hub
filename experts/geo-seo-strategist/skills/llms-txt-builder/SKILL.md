---
name: llms-txt-builder
display_name: llms.txt 与机器可读资产
display_name_en: llms.txt & Machine-Readable Assets
description: "Helps a site owner create an llms.txt (an AI-facing content navigation) and the surrounding machine-readable assets that make a product easier to discover and cite by AI search. Covers the llms.txt format and example, deployment (/llms.txt, /docs/llms.txt, HTTP Link header), Mintlify auto-generation, a GEO discoverability self-check (crawler policy, sitemap, entity/trust/pricing/FAQ/changelog pages, JSON-LD), and honest boundaries (not a traffic switch). Use when the user wants AI tools to find and read their docs correctly."
category: business
version: 1.0.0
author: 大漠
---

# llms.txt 与机器可读资产

当 AI 来读取网站，它能不能找到真正有用的资料？llms.txt 就是为这件事提出的一种办法：给网站准备一份**面向 AI 的内容导航**，说明网站是什么、重要资料在哪里。它采用 Markdown 格式，核心是简介 + 分类链接。

> 一句话记法：**先给目录，需要什么，再读什么。**

## 适用场景

- 用户有文档站 / 帮助中心 / 产品站，希望 AI 工具能找对、读对资料
- 用户要让 AI 帮忙接入产品（读 API 文档、按教程操作）时少出错
- 作为 GEO 技术面的一部分，和写作（`geo-content-writing`）互补

## 输入

- 站点地址、文档 / 帮助中心 / 更新日志的链接
- 是否有 Mintlify 等可自动生成 llms.txt 的文档工具
- 一个真实任务（如"让 AI 按文档完成一次接口调用"），用来验收

## 执行步骤

### 步骤 1 — 写 llms.txt

格式（Markdown）：`# 站点名` + `>` 一句话简介，然后按主题分 `##` 区块，每条用 `- [标题](链接): 一句话说明这份资料解决什么问题`。示例：

```markdown
# yscai101
> 分享 AI 工具使用、AI 编程与产品实践，帮助读者从理解概念走向实际应用。

## 入门指南
- [认识 AI Agent](https://yscai101.com/docs/ai-agent.md): 介绍 Agent 的基本能力、适用场景与使用边界。
- [什么是 Skill](https://yscai101.com/docs/skill.md): 解释 Skill 的作用，以及如何将常用方法整理成可复用技能。

## 实践教程
- [用 AI 完成第一个网站](https://yscai101.com/tutorials/first-website.md): 从明确需求到开发、测试、上线的操作步骤。
- [为网站添加 llms.txt](https://yscai101.com/tutorials/llms-txt.md): 创建内容导航，并验证 AI 是否能够读取相关文档。

## 关于网站
- [网站介绍](https://yscai101.com/about.md): 说明内容方向、适合读者与联系方式。

## Optional
- [更新记录](https://yscai101.com/changelog.md): 查看内容与教程的更新情况。
```

要点：文件里写清项目名称、用途，按主题列出链接，并用一句话说明每份资料解决什么问题；重要页面尽量提供干净的 Markdown 正文。

### 步骤 2 — 部署入口，让 AI 能发现

- 从站点根 `/llms.txt` 开始；2026-08 提案更新后进一步明确 `/docs/llms.txt` 这类子路径的覆盖范围。
- 也可用**页面链接**或 **HTTP `Link` 响应头**帮助工具发现文件。
- 如果用 **Mintlify**：可自动生成 `llms.txt`，也能提供把文档正文合并起来的 `llms-full.txt`。分清两者：**一个帮助定位资料，一个集中提供正文**。资料多时更建议按问题选页面，避免把无关内容塞进上下文。

### 步骤 3 — 把入口交给 AI 的正确方式

- 工具能联网：直接给地址，并明确要求"先读导航 → 找到与任务相关的页面 → 核对版本 → 再根据正文回答，附上来源；资料没写的地方不要自行补全"。
- 工具不能联网：上传任务需要的正文。只上传一份链接目录，它拿不到链接背后的内容。

### 步骤 4 — 用同一个任务做对照验收

一次按原方式处理，一次明确提供导航，看它有没有找到正确版本、引用能不能打开、关键参数有没有写错。一次结果只能发现问题；想判断是否稳定有用，要换几个常见任务重复检查，并实际验收代码能否运行、步骤能否执行。

### 步骤 5 — 顺带补齐 GEO 可发现性自检清单

llms.txt 只是其中一项。完整的"机器可读可发现性"还要看：

- **爬虫允许 / 禁止策略**：robots.txt 是否误挡；sitemap.xml 与 URL 整洁度
- **产品事实清晰度**：功能、价格、限制是否明确可核实
- **FAQ 与文档覆盖**：帮助中心 / FAQ 是否覆盖用户真实问题
- **价格清晰度**：定价页是否清楚
- **信任页与实体页**：关于、联系方式、品牌实体是否清晰（利于 AI 识别"你在介绍谁"）
- **changelog 新鲜度**：更新日志是否及时
- **JSON-LD 结构化数据**：对支持的系统加 `SoftwareApplication` / `Product` / `Organization` / `WebSite` / `BreadcrumbList`，且结构化数据与可见内容一致

## 边界（必须向用户讲清）

- **Google 已说明**：进入其 AI 概览和 AI 模式**不需要**额外创建 AI 文本文件；满足要求也**不保证**收录或展示。其他平台效果需单独验证。
- **不是流量开关**：文件放上网站 ≠ 所有 AI 都会自动采用；前提是 AI 使用的工具能访问并实际读取了它们。
- **文档有变化要同步更新**目录和正文；一个长期指向旧资料的入口，只会让错误更容易被重复使用。
- 价值在于"帮 AI 找对文档、减少用错信息"，先把一个具体任务跑通，再决定是否扩大投入。

## 反模式

- 以为加了 llms.txt 就有流量 / 就被引用（它不保证）。
- 只上传链接目录给不能联网的工具（拿不到正文）。
- 用 llms-full.txt 把全部文档塞进上下文（无关内容污染）。
- 文档改了但导航不更新（旧资料被反复用错）。

## 参考

- llms.txt 由 Jeremy Howard 于 2024-09-03 提出（开放性提案）；2026-08 提案更新了子路径与发现方式，见 `references/sources.md`（标注"待联网复核"）。
- 可操作 GEO 工具参考：vespid-ai/geo-skill（含 llms.txt / robots.txt / JSON-LD 生成与站点审计），见 `references/sources.md`。
