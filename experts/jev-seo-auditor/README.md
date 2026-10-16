# SEO 审计与整改顾问 · 稽网（jev-seo-auditor）

按 **Google 52 条规则**给整站体检：跑开源工具 [jev-seo](https://github.com/AgriciDaniel/jev-seo) 出 PDF / Excel / Markdown 三份报告，带你按优先级逐项整改并复跑验证。分数只用来排整改顺序，不预测排名。

## 它比别人多做的事

jev-seo 负责**查出问题**，稽网负责**把问题改掉**：

1. **零成本预检** —— 花 Jev 的钱之前，先自己查 robots.txt / sitemap / 状态码 / 首页源码，先定位卡在爬取、索引还是内容；
2. **引导跑全量审计** —— 环境自检、密钥与预算开关（标准模式约 1 美分/站，`--full` 约 0.30 美元/站且先问预算）；
3. **解读三份报告** —— PDF 给客户看、Excel 当整改进度表（每条带优先级/改法/官方出处）、Markdown 进仓库；
4. **直接动手整改** —— 读改 robots.txt、sitemap、canonical、JSON-LD、title/meta、模板、图片与脚本，处理关键词自相残杀，优化 LCP/INP/CLS；
5. **复跑验证** —— `rescore` 免费离线重建评分，有条件重跑审计对比前后；
6. **交付客户报告包** —— 三份报告 + 整改记录 + 复跑对比 + 诚实的边界声明。

## 工作流

定目标与预算 → 零成本预检 → 跑 jev-seo 全量审计 → 解读报告 → 按七大区域逐项整改 → 复跑验证 → 交付。

## 七大整改区域

爬取与索引 · 页面元素 · 内容 · 链接 · 结构化数据 · AI 爬虫访问 · 性能与安全。默认顺序：索引拦截 → 死链重定向 → canonical → sitemap → 结构化数据 → title/meta → 内容 → CWV → AI 爬虫 → 外链。

## 目录

```
agents/jev-seo-auditor.md                  # 主理人：persona、六步工作流、边界与命令速查
skills/jev-seo-runbook/SKILL.md            # 运行手册：安装、密钥、命令、成本、报告
skills/jev-seo-runbook/references/
  cli-reference.md                         # CLI 完整语法、环境变量、预算开关、依赖
  report-guide.md                          # 三份报告逐表解读与解读纪律
skills/seo-fix-playbook/SKILL.md           # 整改手册：七区域检测信号→修法→官方出处
skills/seo-fix-playbook/references/
  rules-52-checklist.md                    # 52 条规则按区域的核验清单
  jev-questions.md                         # Jev 判断体系解读与内容整改联动
```

## 上游与归属

- **jev-seo**（github.com/AgriciDaniel/jev-seo，MIT）—— 审计工具本体，需用户自行安装并承担其 API 费用；本包是其编排层，不含其代码；
- **Google Search Central / web.dev** —— 整改依据的官方文档来源；
- 详见 `LICENSE` 归属说明。

## 边界（写死在专家里）

分数只排整改顺序、不预测排名流量；Jev 决定性区间外的答案标 `待验证`；大站为抽样审计（默认 60 页）；不替代 Search Console。
