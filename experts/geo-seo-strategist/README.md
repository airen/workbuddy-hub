# 显扬 · GEO/SEO 增长顾问（geo-seo-strategist）

一个手把手带你做 GEO 与 SEO 的 WorkBuddy 专家：从选题机会判断、GEO 式写作、机器可读资产（llms.txt / 结构化数据），到效果度量，全程逐步引导，证据优先、不编数据。

## 它能帮你做什么

1. **选题诊断**（`geo-topic-research`）：从产品往下拆出 Topic Pool，再用 Google SERP + 竞品反查（Semrush/Ahrefs）+ 产品相关性 + AI Query 属性，判断哪个主题真值得写。
2. **GEO 式写作**（`geo-content-writing`）：把关键词扩展成真实 Query，写清 Entity，按场景做有证据的 Comparison，并用"答案优先"结构组织文章。
3. **机器可读资产**（`llms-txt-builder`）：生成 llms.txt，补齐 GEO 可发现性清单（爬虫策略、sitemap、实体/信任/定价/FAQ/changelog 页、JSON-LD）。
4. **效果度量**（`geo-measurement`）：分三层（SEO 基础 / AI 可见性 / 业务价值）看 GEO 到底有没有用，诚实归因。

## 核心立场

- GEO 是 SEO 在 AI 问答场景下的延伸，不是推倒重来。
- 比"怎么写"更先要解决的是"为什么值得写这个主题"——这个判断不要完全交给 AI。
- 加 FAQ / Schema / TL;DR 不保证 AI 一定引用你，GEO 目前没有稳定排名公式。
- 一切外部数据带来源、可核实，易变信息（排名、平台规则、版本、价格）先联网复核。

## 包结构

```
geo-seo-strategist/
├── .codebuddy-plugin/plugin.json
├── agents/geo-seo-strategist.md        # 主引导式提示词（四步 SOP + 名词表 + 原则）
├── skills/
│   ├── geo-topic-research/SKILL.md      # 选题机会三步信号法
│   ├── geo-content-writing/SKILL.md     # Query/Entity/Comparison/Evidence/答案结构
│   ├── llms-txt-builder/SKILL.md        # llms.txt + 机器可读资产 + GEO 自检
│   └── geo-measurement/SKILL.md         # 三层验证
├── references/sources.md                # 来源与待联网复核清单
└── avatars/geo-seo-strategist.png
```

## 来源与参考

见 `references/sources.md`：Semrush / Ahrefs 数据、llms.txt 提案、vespid-ai/geo-skill、yaojingang/yao-geo-skills、GEO 论文等，均标注来源与"待联网复核"。
