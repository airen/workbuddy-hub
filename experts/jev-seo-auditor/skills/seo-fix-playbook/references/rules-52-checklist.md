# 52 条规则核验清单（按区域整理）

jev-seo 对照 Google 搜索官方文档的 52 条规则逐条核，分七个区域。本清单是**按区域整理的核验与整改要点**，方便人工复核报告时定位；每条发现的具体规则编号、启发式标记与官方出处，以报告（Excel 的 Actions / PDF 的 Findings）自带信息为准。

> 上游规则库：jev-seo `jevseo/` 检查模块（github.com/AgriciDaniel/jev-seo）。标「启发式」的规则是编辑惯例，不是搜索引擎硬性要求——报告里会标出来，别当成 Google 强制项。

## 区域 1 · 爬取与索引

- robots.txt 是否存在、是否误拦 Googlebot、是否 `Disallow: /` 误封全站；
- robots.txt 是否遵守 Crawl-delay（jev-seo 自己也遵守，爬取礼貌）；
- sitemap.xml 是否存在、可解析、URL 是否覆盖主要页面；是否用站点地图索引；
- 重定向：临时主机重定向（temporary host redirects）单独记录；链式/循环重定向；301 vs 302 用法；
- 主机与 HTTPS 探测：www/non-www 归一、全站 HTTPS；
- 软 404 检查：返回 200 但无实质内容的页面；
- `noindex` 使用：该屏蔽的屏蔽、不该屏蔽的别误加；
- canonical：指向自身首选版本，别指向别站；
- 每个重定向跳点的私有网络防护（jev-seo 自身安全机制）。

## 区域 2 · 页面元素（on-page）

- title 缺失 / 重复 / 过长截断；
- meta description 缺失 / 重复；
- H1 缺失或多个；
- 标题层级跳级；
- 视口与移动适配基础。

## 区域 3 · 内容

- 词数（独立抓取验证，误差 5% 以内）；
- 薄内容页面；
- 站内重复内容；
- 页面主题聚焦度（Jev 辅助判断）。

## 区域 4 · 链接

- 死链（站内 4xx/5xx）；
- 孤页（无内链入口）；
- 重定向链上的链接（该直接链最终地址）；
- 锚文本质量（描述性 vs 「点击这里」）。

## 区域 5 · 结构化数据

- 是否存在 JSON-LD 及类型是否匹配页面（Article / FAQPage / Product+Offer / BreadcrumbList / Organization 等）；
- 富媒体结果要求的必填属性是否齐全；
- FAQ 富结果的使用是否符合说明（FAQ 富结果目前主要对权威政府/健康站点展示，别滥用）；
- 结构化数据是否与页面可见内容一致（编造会被判结构化数据违规）。

## 区域 6 · AI 爬虫访问

- robots.txt 对 AI 爬虫（GPTBot、ClaudeBot、Google-Extended 等）的放行/屏蔽策略；
- `llms.txt` 是否存在（社区提案 llmstxt.org，非 Google 官方标准）；
- AI 爬虫可访问性与普通爬虫一致性。

## 区域 7 · 性能与安全

- Core Web Vitals：LCP / INP / CLS（PageSpeed Insights 实测）；
- HTTPS 全站；
- 安全响应头基础（HSTS 等）；
- 渲染阻塞资源、图片体积等常见性能项。

## 人工复核流程建议

1. 拿报告 Actions 表逐条过：**优先级 → 规则编号/出处 → 是否启发式**；
2. 启发式规则先做业务判断（是否符合自家编辑规范），再决定改不改；
3. 每条改动记「依据哪条规则 + 官方出处 + 验证方法」，进整改记录；
4. 改完跑 `bin/jevseo rescore`（免费）或重跑 `audit`，核对未解决项清零且无新问题。
