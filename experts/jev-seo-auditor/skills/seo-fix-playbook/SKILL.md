---
name: seo-fix-playbook
display_name: SEO 整改手册
display_name_en: SEO Remediation Playbook
description: "把 jev-seo 审计发现变成真实改动的整改手册：七大区域（爬取与索引、页面元素、内容、链接、结构化数据、AI 爬虫、性能与安全）逐区给出检测信号、标准修法与官方出处，含 Jev 内容层问题整改、CWV 优化与复跑验证方法。"
description_zh: "SEO 整改手册：七大区域逐区给检测信号、修法与官方出处；含 Jev 内容层整改、CWV 优化、复跑验证与客户交付包。"
description_en: "Turn jev-seo audit findings into real fixes: seven areas with detection signals, standard remedies and official sources, Jev content fixes, CWV tuning, re-run verification, and client delivery."
category: business
version: 1.0.0
author: 大漠
agent_created: true
---

# SEO 整改手册

审计报告只是起点。这个手册负责把每条发现变成**真实、可验证、有出处**的改动。配套技能 `jev-seo-runbook` 负责把审计跑出来；本手册负责把问题改掉并复跑确认。

## 一、整改总原则

1. **索引优先于体验**：能不能被抓到 → 能不能被索引 → 内容有没有价值 → 体验快不快。被 robots 拦住的页面，优化得再好也进不了索引。
2. **先高影响低努力**：按报告「影响力 vs 努力」矩阵排序；没有矩阵时按本手册的默认优先级。
3. **每条改动附出处**：引用 Google Search Central 官方文档或报告自带出处；启发式规则注明「编辑惯例」。
4. **小步改、次次验**：一次改一个区域，用复跑/rescore 验证后再动下一个；一次全改无法归因。
5. **不确定不硬改**：删页面、改 URL、合并内容是破坏性操作，给选项让用户拍板。

默认优先级（无报告矩阵时）：
**robots/索引拦截 → 死链与重定向 → canonical → sitemap → 结构化数据 → title/meta → 内容（薄/重复/自相残杀）→ CWV → AI 爬虫策略 → 外链与权威**。

## 二、七大区域整改

### 区域 1 · 爬取与索引（先查这里）
| 检测信号 | 标准修法 | 官方出处 |
|---|---|---|
| robots.txt 全站 `Disallow: /` 或误拦 Googlebot | 放行必要路径；只拦该拦的（后台、搜索页、参数页） | Google robots.txt 规范 |
| sitemap.xml 缺失/过期/不含 URL | 建或重建站点地图并提交 Search Console；多站点地图用索引文件 | Google 站点地图文档 |
| 页面 `noindex` 误用 | 移除误加的 `noindex`；确认要屏蔽的（thank-you 页、搜索结果页）才保留 | Google 屏蔽索引文档 |
| canonical 指向别的站/自己 | canonical 必须指向该页首选版本；跨语言/分页各自正确 | Google 合并重复网址文档 |
| 重定向链 / 循环 / 临时重定向滥用 | 301 直连最终地址；清链；临时跳转别长期用 | Google 重定向文档 |
| 软 404（返回 200 的空/无内容页） | 返回真 404，或给实质内容 + 正确状态码 | Google HTTP 网络错误文档 |
| HTTPS/主机跳转问题 | 全站 HTTPS；主机跳转规范化（www/non-www 二选一） | Google 站点移动/HTTPS 文档 |

### 区域 2 · 页面元素（on-page）
- **title**：每页唯一、含主关键词、别超长截断（约 50–60 字符为经验值）；
- **meta description**：每页唯一、写清楚点击理由（不直接影响排名，影响点击率）；
- **H1**：每页恰好一个、与 title 呼应；H2/H3 层级不跳级；
- 修完抽查渲染后的 HTML（curl + 看源码），不只改模板源文件。

### 区域 3 · 内容
- **薄内容**：合并或扩充；没价值就删并做 301（先 Search Console 查流量再删）；
- **重复内容**：canonical 归一；模板页（筛选/排序/参数）用 canonical 或 noindex；
- **关键词自相残杀**（Jev 的「竞争同一搜索的页面对等」）：多页争一个词 → 合并成一页最全的，其余 301 过去，或在 Search Console 看哪页更强再定；
- **E-E-A-T 信号**：作者署名、页面资质、联系方式、更新日期——信任类页面（YMYL）尤其要补。

### 区域 4 · 链接
- 死链（4xx/5xx）：修链或 301；外链死链删掉或换源；
- 孤页（无内链入口）：从相关页补内链，或进 sitemap 并等爬取；
- 锚文本：用描述性文字，别一片「点击这里」；
- 内链结构：重要页离首页点击距离 ≤ 3。

### 区域 5 · 结构化数据（JSON-LD）
- 先确认页面类型，再选类型：文章页 Article、FAQ 页 FAQPage、商品 Product + Offer、面包屑 BreadcrumbList、组织 Organization；
- 用 Google 富媒体结果测试验证后再上线；
- **别为进富媒体编造页面没有的内容**——结构化数据策略明确反对；
- 每条 schema 的必填属性以官方文档为准，报告 Excel 里带具体属性要求。

### 区域 6 · AI 爬虫访问
- robots.txt 里对 AI 爬虫（GPTBot、ClaudeBot、Google-Extended 等）的策略是有意选择：默认放行利于 AI 引用，要屏蔽则显式声明并在文档中记录理由；
- `llms.txt`（llmstxt.org，社区提案、非 Google 官方标准）可给 AI 一个站点导览——当加分项，不当必需品。

### 区域 7 · 性能与安全
- **CWV 三指标**：LCP（加载）≤ 2.5s、INP（交互）≤ 200ms、CLS（视觉稳定）≤ 0.1（75 分位口径，来源 web.dev/vitals）；
- LCP 常见修法：压缩/转 WebP、给首屏图 `fetchpriority="high"`、预加载 LCP 资源、服务端缓存；
- INP 常见修法：砍长任务、拆分 JS、延迟非关键脚本；
- CLS 常见修法：图片/广告位写死宽高、字体 `display:swap` + 预加载、异步注入内容预留空间；
- 安全基线：全站 HTTPS、安全响应头（HSTS 等）、不泄露服务器版本。

## 三、Jev 内容层结论怎么整改

Jev 每页给保留概率的类型化答案，重点看这几个（完整问题表见 `references/jev-questions.md`）：

| Jev 结论倾向 | 整改方向 |
|---|---|
| helpfulness 低 | 补真实经验、数据、示例；删套话 |
| specificity 低 | 给具体数字、步骤、场景，替换泛泛而谈 |
| trust 低 | 署名、资质、来源、联系方式、更新记录 |
| citability 低 | 结论前置、段落自足（可被整段引用） |
| title/meta 与内容不匹配 | 重写 title/description 使其如实概括页面 |
| 竞争同一搜索的页面对等 | 按区域 3 的自相残杀处理合并 |

**纪律**：决定性区间外的答案标 `to verify`，人工看 SERP 复核后再动手；别拿一个概率当铁证。

## 四、复跑验证

```bash
bin/jevseo rescore jev-seo-reports/<domain>-<stamp>/   # 免费离线重建发现与评分
bin/jevseo audit https://<域名>                        # 有条件重跑（约 1 美分）
```

验证口径：
- 分数小步上升即正常（预期不是暴涨）；
- 逐条核对「未解决项」是否清零；
- 检查有没有**新引入**的问题（整改 regression）；
- 有条件时过 2–4 周看 Search Console 抓取/索引数据（收录有延迟，别指望当天见效）。

## 五、给客户的交付包

1. 三份报告：PDF 给看、Excel 当整改进度表、Markdown 归档；
2. 整改记录：每项「改前 → 改后、依据、验证结果」；
3. 复跑对比：分数变化、剩余项、`待验证` 清单；
4. 边界声明（原文可抄）：**分数只用于排整改顺序，不预测排名与流量；本站为抽样审计（大站默认 60 页）；收录与排名变化以 Search Console 与后续复跑为准。**

## 不适用

- 本手册不替代 Search Console 与真实 SERP 观察；
- 不承诺排名、流量、收录时间；
- 破坏性操作（删页、并页、改 URL）必须先给用户选项。
