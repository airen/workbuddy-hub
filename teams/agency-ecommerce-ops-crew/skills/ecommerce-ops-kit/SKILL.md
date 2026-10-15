---
name: ecommerce-ops-kit
description: 电商运营与供应商管理工具包：前后端一起管。含供应商五维评分卡（质量/交期/价格/服务/合规）、验厂审核报告模板、年度采购策略、跨境电商多平台打法（Listing、海外仓、合规税务）、中国电商全平台运营（淘天拼京上架优化、大促节奏）。用于「1688 供应商怎么筛」「验厂审什么」「想出海东南亚要准备什么」「这个品全平台怎么铺」。
category: business-tools
version: 1.0.0
---

# 电商运营与供应商管理工具包

前端管全平台运营，后端管供应链，一份交付把生意前后端接起来。

## 何时用本技能

- 要从 1688 等平台筛供应商、打分、验厂
- 要定供应商分级与年度采购策略、谈账期
- 要做出海（东南亚/欧美）的 Listing、海外仓与合规税务准备
- 要做国内全平台上架优化、大促节奏与跨平台策略

不适用于：短视频与直播打法（那是 `short-video-launch-kit` 的活）。

## 五个交付物（对应 references/）

| 文件 | 交付什么 | 什么时候读 |
|---|---|---|
| `references/vendor-scoring-card.md` | 供应商五维评分卡：基本信息、评分、关键数据、改进要求 | 筛供应商时 |
| `references/factory-audit-report.md` | 验厂审核报告：工厂概况、审核项评分、优势/风险项、结论 | 验厂前 |
| `references/annual-sourcing-strategy.md` | 年度采购策略：结构优化、降本目标、新供应商开发、账期 | 年度规划时 |
| `references/domestic-ecommerce-ops.md` | 中国电商全平台运营：上架优化、直播带货、大促 | 做国内时 |
| `references/cross-border-playbook.md` | 跨境电商：多平台、海外仓、合规税务、DTC 独立站 | 做出海时 |

## 工作流程

1. **寻源**：明确需求 → 多渠道寻源 → 初筛入围名单
2. **评厂**：按 `vendor-scoring-card.md` 五维打分 → 按 `factory-audit-report.md` 安排验厂
3. **谈判**：价格、交期、账期、质量条款一次谈清，落到合同
4. **定级**：按季度绩效把供应商分级，优质扩量、劣质淘汰
5. **铺渠道**：国内按 `domestic-ecommerce-ops.md` 上架优化；出海按 `cross-border-playbook.md` 备 Listing 与合规
6. **年度复盘**：按 `annual-sourcing-strategy.md` 定结构优化目标、降本目标与账期策略

## 硬规则

- **质量底线不可谈**：涉及安全/环保/强制性标准的项目，不合格即一票否决，不因价格妥协
- **合规与廉洁**：不收供应商贿赂、不泄露报价、关联交易必须申报
- **账期与现金**：账期谈判要匹配自身现金流，不做「账期越长越好」的单一目标
- **出海先合规后上架**：目标市场的税务、产品认证、数据合规先确认，再投 Listing
- **只出方案不代操作**：产出评分卡、审核报告与运营计划，不代签合同、不代投广告

## 溯源

`references/` 内容逐字抽取自 [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)（MIT 协议），
已做 frontmatter 剥离、章节 emoji 前缀归一、AI 平台品牌名中性化，未做内容改写。
