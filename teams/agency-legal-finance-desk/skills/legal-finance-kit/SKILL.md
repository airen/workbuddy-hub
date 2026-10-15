---
name: legal-finance-kit
description: 法务财税合规工具包：合同、制度、发票三件事一份交付。含合同七类核心条款审查清单（主体资格/标的价款/违约金 585 条/知识产权/保密数据/争议解决）、合同审查意见书模板（风险总评+逐条意见+35 分矩阵）、数据合规三法速查（PIPL/DSL/CSL）、隐私政策九章框架、发票管理制度与月度健康度报告、税务合规红线。用于「审这份合同」「起草隐私政策」「报销发票流程怎么搭」「三法合规要做什么」。
category: business-tools
version: 1.0.0
---

# 法务财税合规工具包

合同审查、合规制度、发票管理三件事一份交付，让业务不等票据、签约不裸奔。

## 何时用本技能

- 要审合同、识别风险敞口、给修改建议
- 要起草隐私政策、用户协议、内部管理制度
- 要确认 PIPL/DSL/CSL 三法合规要求
- 要搭发票开具、收取、报销、归档流程
- 要做月度发票健康度复盘

不适用于：具体诉讼策略与出庭应诉（须转执业律师）。

## 六个交付物（对应 references/）

| 文件 | 交付什么 | 什么时候读 |
|---|---|---|
| `references/contract-review-checklist.md` | 七类核心条款审查清单：主体资格/标的价款/违约/知产/保密数据/争议解决 | 审合同前 |
| `references/contract-opinion-template.md` | 审查意见书模板：风险总评、红黄绿三级意见、35 分风险矩阵 | 出意见时 |
| `references/three-laws-compliance.md` | 数据合规三法体系：PIPL/DSL/CSL 各自要求与适用场景 | 定合规框架时 |
| `references/privacy-policy-template.md` | 隐私政策九章框架：收集/使用/共享/存储/权利/未成年人 | 起草隐私政策时 |
| `references/invoice-management.md` | 发票管理制度：开票权限、时效、类型选择、三单匹配 | 搭流程时 |
| `references/invoice-health-report.md` | 月度发票健康度报告：开票、进项、报销、风险预警 | 月度复盘时 |
| `references/tax-compliance-redlines.md` | 税务合规红线 | **开票前必读** |

## 工作流程

1. **合同初审**：确认主体资格与授权链 → 识别合同类型（买卖/服务/技术开发/劳动/租赁/投资/加盟）→ 定审查重点
2. **逐条审查**：按 `contract-review-checklist.md` 七类逐条过，标红/黄/绿三级
3. **出意见**：按 `contract-opinion-template.md` 写风险总评 + 逐条修改建议 + 缺失条款提醒
4. **合规兜底**：涉及个人信息处理的条款必须符合 PIPL；开源代码要查 GPL 感染性风险
5. **财税落地**：按 `invoice-management.md` 搭流程，红线对照 `tax-compliance-redlines.md`
6. **月度复盘**：出 `invoice-health-report.md`，风险预警前置

## 硬规则

- **先合规后效率**：发票的合规性优先于报销速度；宁可业务等一天，不让票据出一次事
- **一票一验**：发票真伪、抬头、税号、金额必须逐张核验，不批量放过
- **不含糊表述**：「尽快」「适当」「合理」这类词在合同和制度里一律改成可执行的具体标准
- **持续更新**：法律与税规会变，制度文件必须带修订记录与生效日期，不搞「永久有效」
- **不越界**：本工具包产出审查意见与制度草稿，**不构成法律/税务执业意见**；涉约束性事项须转持牌律师/税务师

## 溯源

`references/` 内容逐字抽取自 [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)（MIT 协议），
已做 frontmatter 剥离、章节 emoji 前缀归一、AI 平台品牌名中性化，未做内容改写。
