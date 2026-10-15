---
name: visual-prompt-kit
description: 生成式视觉工具包：把视觉想法写成能直接投喂生图生视频工具的提示词，并对成本与偏见负责。含图像提示词四层结构（主体/环境场景/光线/技术摄影）、视频提示词五段式（主题/人物设定/氛围画质/运镜分镜）、负面提示词与成本验证、用户研究计划与画像模板、包容性视觉红线（绝对禁止/必须做到）与光照公平性参数。用于「写生图提示词」「写视频提示词」「先做用户研究」「查这批图有没有偏见」。
category: content-creation
version: 1.0.0
---

# 生成式视觉工具包

主理人（图构）调度：写提示词、算成本、做研究、查偏见，四件事一条线。

## 何时用本技能

- 要把一句视觉需求写成可投喂的生图/生视频提示词
- 要先做用户研究、画用户画像再动手设计
- 要审查一批生成图/视频是否有刻板印象与偏见
- 要评估一条视频提示词的成本与废片风险

不适用于：界面设计与前端样式（那是 `visual-forge-studio` 的活）。

## 十个交付物（对应 references/）

**提示词构建**
| 文件 | 交付什么 |
|---|---|
| `references/image-prompt-structure.md` | 图像提示词四层结构：主体描述 / 环境场景 / 光线设定 / 技术摄影 |
| `references/image-rules.md` | 图像提示词工程规范与摄影准确性红线 |
| `references/video-prompt-5seg.md` | 视频提示词五段式主交付物 |
| `references/video-negative-prompt.md` | 负面提示词，每组注明挡什么 |
| `references/video-cost-validation.md` | 成本与验证建议（每条必给） |

**用户研究**
| 文件 | 交付什么 |
|---|---|
| `references/ux-research-plan.md` | 用户研究计划框架：目标 / 方法论 / 参与者 / 研究协议 |
| `references/ux-persona-template.md` | 用户画像模板：人口统计 / 行为模式 / 目标需求 / 场景 / 引用 |
| `references/ux-research-rules.md` | 研究方法论优先与道德实践 |

**包容性把关**
| 文件 | 交付什么 |
|---|---|
| `references/inclusive-prompt-arch.md` | 包容性 Prompt 架构方法论 |
| `references/inclusive-review-gates.md` | 绝对禁止清单 + 必须做到清单 |
| `references/inclusive-light-fairness.md` | 光照公平性参数示例 |

## 工作流程

1. **先问人再问图**（涉及用户侧时）：按 `ux-research-plan.md` 定研究目标与方法，按 `ux-persona-template.md` 出画像
2. **写提示词**：图像走四层结构，视频走五段式；**负面提示词必须随主交付物一起给**
3. **算成本**：按 `video-cost-validation.md` 给出这条要花多少钱、先用什么低成本规格验证
4. **过包容性关**：按 `inclusive-review-gates.md` 逐条过绝对禁止与必须做到；光照按 `inclusive-light-fairness.md` 调
5. **交付**：提示词 + 负面提示词 + 成本建议 + 偏见审查结论，四件一套

## 硬规则

- **没有负面提示词不交付**：每组负面词必须注明它挡什么，不给"万能负面词"
- **成本透明**：每条视频提示词都要回答"这条要花多少钱"，并建议先用低成本规格验证再放大
- **多镜先锁一致性**：超过一个镜头时才给多镜项目卡，先锁定人物/风格一致性再展开
- **承认废片率**：不承诺"一次出片"，如实说明预期废片与重试策略
- **偏见零容忍**：涉及人物形象时，绝对禁止清单逐条过；不确定就降低人物特异性描述
- **只出提示词不出图**：本技能产出提示词文本与研究结论，不执行生图/生视频调用

## 溯源

`references/` 内容逐字抽取自 [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)（MIT 协议），
已做 frontmatter 剥离、章节 emoji 前缀归一、AI 平台品牌名中性化，未做内容改写。
