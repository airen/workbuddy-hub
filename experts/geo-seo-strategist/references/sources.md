# 来源与待核实清单（GEO/SEO）

> 本文件汇总专家用到的外部数据点、社区资源与学术出处。**凡是会随时间变化（排名、收录机制、版本、价格、平台规则）或来自二手转述的内容，都标注「待联网复核」**——专家在引用时应优先联网核对最新事实，不要凭记忆下结论。

## 一、数据支撑（来自用户提供的原始文章，建议联网复核原始报告）

- **Semrush（2025）**：基于超过 10 亿条美国用户 clickstream 数据，ChatGPT 对外 referral traffic 在 2025 年增长 **206%**。
  - 状态：原始文章引用 → **待联网复核**（建议查 Semrush 官方博客 / 研究报告原文）。
- **Ahrefs**：研究 3,000 个网站，发现 **63%** 的网站已经收到过来自 AI Chatbot 的访问。
  - 状态：原始文章引用 → **待联网复核**（建议查 Ahrefs 官方研究原文）。

## 二、llms.txt 提案（来自联网检索，待核实）

- **提出者 / 时间**：Jeremy Howard 于 **2024-09-03** 提出 llms.txt 开放性提案。
  - 状态：**待联网复核**（提案原文与版本演进以 llmstxt.org / 官方仓库为准）。
- **2026-08 提案更新**：进一步明确 `/docs/llms.txt` 这类子路径的覆盖范围，并补充用页面链接或 HTTP `Link` 响应头帮助工具发现文件的方式。
  - 状态：**待联网复核**（提案仍在演进，以最新版本为准）。

## 三、社区 GEO 技能 / 工具（来自联网检索，可引用；功能与版本以仓库为准）

- **vespid-ai/geo-skill**（MIT，v0.5.0 起）：开源 GEO 工具包，含 Python CLI（站点审计、生成 robots.txt / llms.txt / JSON-LD）与可复用的 agent skills（Hermes / Claude Code / Codex）。其梳理的"可操作 GEO 清单"被本专家采纳：爬虫允许/禁止策略、sitemap 与 URL 整洁度、产品事实清晰度、FAQ 与文档覆盖、价格清晰度、信任页与实体页、changelog 新鲜度、结构化数据、机器可读内容布局、OSS 仓库可发现性；并按页面原型（首页定位、功能页、定价页、FAQ、文档/帮助中心、changelog、对比页、信任/实体页）逐项处理。覆盖的发现面包括 ChatGPT Search、Bing AI、ByteDance/Bytespider（豆包）。
  - 仓库：https://github.com/vespid-ai/geo-skill
- **yaojingang/yao-geo-skills**：开源 GEO 内容与工作流技能合集，持续更新。
  - 仓库：https://github.com/yaojingang/yao-geo-skills

## 四、学术出处（可引用）

- **GEO 概念起源**：Princeton 等机构 Aggarwal et al.（2024）《GEO: Generative Engine Optimization》——最早系统研究"针对生成式引擎优化内容"的论文。
  - 状态：可引用；具体结论以论文原文为准。

## 五、核心立场（本专家贯穿始终，非外部数据）

- GEO 不是推翻 SEO 另搞一套，而是 SEO 在 AI 问答场景下的延伸。
- GEO 目前**没有稳定、公认的排名公式**；加 FAQ、Schema、TL;DR 不保证 AI 一定引用你。
- 选题的"为什么值得写"是最不该完全交给 AI 的判断环节。
- Google 已说明进入其 AI 概览 / AI 模式不需要额外 AI 文本文件，满足要求也不保证收录或展示；llms.txt 不是流量开关。

## 六、SEO 实操长文（用户提供，本专家的核心素材之一）

- 用户提供了一篇完整的 SEO 实操长文（《现在用 AI 做网站非常简单，真正难的是怎么让客户找到你》），被落地为 `seo-foundations` 技能。核心论点：**先让一张页面跑通（被发现、收录、理解、有排名），再谈 GEO——GEO 不是推翻 SEO，而是 SEO 在 AI 问答场景下的延伸。** 涵盖 Google 四步链路（发现→抓取→收录→排名）、需求→关键词研究、搜索意图看 SERP、页面架构（核心/场景/教程/对比）、工具页 on-page 基础、技术收录清单、Search Console 工作流、内链外链、白帽黑帽、四指标排查。
- 长文中点名的工具与平台（可用性 / 功能 / 数据口径会变化，引用前建议联网复核当前状态）：
  - **Ahrefs 免费关键词生成器**、**OpenSEO 关键词生成器**：扩词、估算搜索次数与竞争。
  - **Google Trends**：看需求上升 / 稳定 / 季节热度（相对热度，非准确人数）。
  - **Google Ads 关键词规划师**：搜索量区间、地区、广告竞争（需登录 Ads 账号；可输入搜索词或竞品网址）。
  - **Google Search Console**：提交 sitemap、网址检查、看展示 / 点击 / 点击率 / 平均排名。
  - **PageSpeed Insights**：页面速度（新站先处理图片太大、首屏慢、按钮无响应、内容跳动）。
  - **AITDK SEO 扩展**：扫描标题 / 说明 / 主标题 / 网址 / 爬虫规则 / sitemap / 图片说明 / 链接。
  - **Google 富媒体搜索结果测试**：校验结构化数据（Schema）代码（页面没有的信息不要编造）。
- Google 官方 SEO 入门指南立场：先为用户做有帮助的内容，再让搜索引擎容易发现和理解（引用以 Google 当前文档为准）。
