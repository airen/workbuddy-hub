---
name: geo-topic-research
display_name: GEO 选题机会判断
display_name_en: GEO Topic Opportunity Research
description: "Guides a website or app owner from their product positioning to a defensible list of GEO topics worth writing. Uses a three-signal method: Google SERP intent reading, competitor reverse-lookup with Semrush/Ahrefs, and two judgment filters (product relevance + AI-query fit). Use before writing any GEO content, when the user asks 'what should I write about' or 'is this topic worth it'."
category: content
version: 1.0.0
author: 大漠
---

# GEO 选题机会判断

在动笔写 GEO 文章之前，先回答一个更难的问题：**这个主题到底存不存在 AI / 搜索机会？**

> 一上来就研究"GEO 文章怎么写"（FAQ 怎么加、Entity 怎么布局、TL;DR 怎么写）都是第二步。第一步是选题。AI 能帮你扩词、拆竞品、写初稿，但"为什么偏偏是这个主题"这个判断，不要完全交给 AI——它需要同时理解产品、用户搜索方式、Google 当前认可的内容、竞品真实流量、用户会不会把问题交给 AI，以及这批用户是不是你要的人。

## 适用场景

- 用户说"帮我做 GEO / 我想写几篇能获客的文章"但还没定主题
- 用户拿着一个关键词来问"这个值得写吗"
- 复盘为什么之前的内容没流量也没被 AI 提到

## 输入

- 一句话产品定位（解决谁的什么问题）
- 目标用户画像（行业 / 规模 / 角色 / 痛点）
- 如有：GSC 数据、已知竞品、已有的 Semrush / Ahrefs 账号或截图

## 执行步骤

### 步骤 1 — 从产品往下拆，建立第一版 Topic Pool

**不要先让 AI 给选题。** 先问 AI"帮我推荐 50 个主题"，它会给你一堆语义相关但"未被证明有机会"的词。正确做法是先从产品本身往下拆：

- **核心品类**：产品所在的大类（如 Customer Feedback / Feedback Management）
- **产品功能**：FeedLog、Usersnap 这类产品具备的功能（Feedback Widget / Feedback Board / Roadmap / Changelog）
- **使用场景**：Collect Website Feedback / Manage Feature Requests / Prioritize Feedback
- **用户问题**：How to Collect User Feedback / How to Organize Customer Feedback

把方向扩成第一版 Topic Pool。**这一阶段不纠结 Volume 和 KD**，只回答一个问题：哪些搜索需求离我的产品足够近。

> 边界检查： employee feedback 流量可能很大，但如果你的产品解决的是 SaaS 用户反馈，这批流量即使做起来也难回到产品。所以先问："如果这个 Topic 真给我带来 1000 个用户，他们是不是我真正想要的那批人？"先划边界，再找机会。

### 步骤 2 — 看 Google SERP 在"说什么"，而不是看某一个排名

拿一个候选词（如 `website feedback widget`）去 Google，重点读整个 SERP 传达的信号：

- 前 10 **几乎全是产品 Landing Page** → Google 暗示主要意图是"直接找工具"，硬写 3000 字 Blog 在 Content Type 上可能就错了。
- SERP 里反复出现 **Best Website Feedback Tools / Top Customer Feedback Tools** → 这个关键词背后除了"找一个产品"，还存在"比较、推荐、选型"的内容需求。这是重要信号。

把其中几个与自己产品方向接近、已进入 SERP 的竞品文章 URL 找出来（下一步用）。

### 步骤 3 — 用 Semrush / Ahrefs 反查竞品页面的"真实流量 Topic"

竞品写过 ≠ 这个主题成功过（成熟 SaaS 可能有 500 篇 Blog，大量页面根本没流量）。把步骤 2 找出的具体 URL 放进 Semrush / Ahrefs，看：

- 这个页面到底排名了哪些 Keyword？真正带来流量的是哪些词？
- 一个页面覆盖了多少相关 Query？这些词集中在哪几个 Topic？

这一步常看到只看 Title 看不到的信息。例如竞品标题只是 `Best Website Feedback Widgets`，反查后可能发现它同时在吃：`website feedback widget` / `best website feedback tools` / `customer feedback widget` / `website feedback software` / `best feedback tools for SaaS`……

结论就从"竞品写过一篇 Widget"变成"Website Feedback 下已存在一组被真实搜索验证过的比较 / 选型需求"。**后者才叫 Topic Opportunity**——它既不是 AI 猜的，也不是 Semrush 显示一个词有 Volume 就决定写，而是：Google SERP 告诉你能进什么内容 + 竞品告诉你已有人在做 + Semrush/Ahrefs 告诉你它有没有真正拿到结果。

### 步骤 4 — 三步信号 + 两个判断，确定 GEO Topic

三个信号对上，才继续：

1. **SERP 允许 Blog / Comparison 类内容进入**（不是全 Landing Page）
2. **已有竞品页面验证过这个需求**
3. **Semrush/Ahrefs 显示它真正拿到过流量词**

再叠加两个判断（决定"这个机会是不是我的"）：

- **产品相关性**：带来 1000 个用户是不是你要的人？
- **AI Query 属性**：用户会不会直接把这个问题拿去问 AI？

天然适合 AI 的问题是那些"不在找一个确定答案，而是让 AI 帮自己整理信息 → 比较产品 → 理解差异 → 按场景做判断"的问题，例如：

- `What are the best website feedback widgets for SaaS?`
- `Which feedback tool is best for collecting feature requests?`
- `Canny vs Usersnap: which is better for a small SaaS team?`
- `Is there an open-source alternative to Canny?`

**最终流程固定为**：产品方向 → Topic Pool → Google SERP → 已排名竞品 → Semrush/Ahrefs 反查真实流量 Topic → 产品相关性 → AI Query 属性 → 确定 GEO Topic。这一轮跑完，才进入写作（交给 `geo-content-writing`）。

## 输出：Topic Opportunity 评分卡

给用户一份可勾选的表，每个候选词过一遍：

| 维度 | 信号 | 结论 |
|---|---|---|
| SERP 内容类型 | 全 Landing Page / 出现 Best·Comparison | 允许内容进入？ |
| 竞品验证 | 已排名竞品页面 URL | 有人做过？ |
| 真实流量（Semrush/Ahrefs） | 实际带来流量的词 | 真拿到过结果？ |
| 产品相关性 | 用户是不是你要的人 | 机会是不是你的？ |
| AI Query 属性 | 用户会不会直接问 AI | 优先级高低 |

优先级最高：五个维度全过、且天然适合 AI 提问的主题。

## 反模式

- **先让 AI 给 50 个主题就开写**：语义相关 ≠ 被证明有机会。
- **看到竞品写过就抄结构**：竞品写过 ≠ 成功过，要反查真实流量。
- **只追流量最大的词**：流量大但和产品无关，只是多一批不相关曝光。
- **只看文章 Title 判断**：真正吃到的流量词往往藏在反查数据里。
- **把"为什么是这个主题"完全交给 AI**：方向选错，后面所有 GEO 优化都是在错误方向上努力。

## 参考

- 外部数据点（Semrush 206% ChatGPT referral 增长、Ahrefs 63% 网站收到过 AI 访问等）见 `references/sources.md`，均标注"待联网复核"。
- 社区 GEO 技能合集：yaojingang/yao-geo-skills、vespid-ai/geo-skill（见 `references/sources.md`）。
