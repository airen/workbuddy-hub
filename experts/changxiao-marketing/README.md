# AI 营销专家 · 长销（changxiao-marketing）

> 核心一句话：**~50 个营销技能，按需组合，一站搞定。**

「长销」是一个 WorkBuddy 单 Agent 专家，内置 7 大类营销玩法（基础 1 + 专项 6），灵感来自 [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) 开源项目，已把它们的能力**内化**成可在 WorkBuddy 里直接交付的成果。需要更深的某个子技能时，再"毕业"到原库按需安装对应模块。

## 七类技能

| 技能 | 覆盖的子技能（原库对应） | 解决的事 |
|---|---|---|
| `product-marketing` | product-marketing（基础） | 产品·受众·定位·价值主张·ICP |
| `conversion-optimization` | cro / signup / onboarding / popups / paywalls | 注册转化、激活、付费墙、漏斗优化 |
| `copywriting-content` | copywriting / copy-editing / emails / social / cold-email | 文案写作、邮件、社媒、冷启动邮件 |
| `seo-discovery` | seo-audit / ai-seo / programmatic-seo / schema | SEO 审计、关键词、结构化数据、规模化 SEO |
| `ads-measurement` | ads / ad-creative / analytics / ab-testing | 投放诊断、广告创意、数据分析、A-B 测试 |
| `growth-retention` | referrals / free-tools / churn-prevention / co-marketing | 推荐裂变、免费工具、流失预防、联运 |
| `monetization-sales` | launch / pricing / revops / sales-enablement | 发布、定价、营收运营、销售赋能 |

## 怎么用

1. 在 WorkBuddy 里召唤「长销」。
2. **先定基础（`product-marketing`）**：你的产品是什么、卖给谁、解决什么问题——这是所有营销动作的前提。
3. **再选专项**：按你当下的卡点（转化/文案/SEO/投放/增长/定价）调对应技能，给可直接落地的成果。

## 文件结构

```
experts/changxiao-marketing/
├── .codebuddy-plugin/plugin.json
├── manifest.yaml
├── agents/changxiao-marketing.md        # 人设 + 路由 + 工作流
├── README.md
├── avatars/changxiao-marketing.jpg
└── skills/
    ├── product-marketing/        references/positioning-canvas.md + icp-template.md
    ├── conversion-optimization/  references/cro-playbook.md
    ├── copywriting-content/      references/copy-frameworks.md + cold-email-template.md
    ├── seo-discovery/            references/seo-audit-checklist.md
    ├── ads-measurement/          references/ad-creative-templates.md + ab-test-plan.md
    ├── growth-retention/         references/retention-loops.md + referral-program.md
    └── monetization-sales/       references/pricing-canvas.md + launch-checklist.md
```

## 关于"毕业到原项目"

`coreyhaines31/marketingskills` 是约 50 个独立 Skill 的合集，强调**按需安装、组合使用**。「长销」已把 7 类常见玩法内化到本专家里，能覆盖大部分日常营销任务。如果你需要某个**特别细分的子技能**（如冷邮件自动化投递、特定广告平台的创意模板），可回原库按需安装对应模块，再让「长销」把它接进整体策略里。
