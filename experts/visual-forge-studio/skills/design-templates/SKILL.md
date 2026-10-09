---
name: design-templates
display_name: 设计模板骨架
display_name_en: Design Templates
description: "Provides Markdown design templates inspired by products like Notion and Figma to structure interface thinking: landing pages, dashboards and settings pages, plus a fill-in skeleton for any new screen. Use when starting a page from scratch or when a design needs a proven structure to build on."
category: design-tools
version: 1.0.0
author: 大漠
---

# 设计模板骨架

用现成的结构起步，而不是从空白页开始空想。

> 模板解决的是"从哪开始"，不是"最终长什么样"。填完模板之后，仍然要按内容调整。

## 适用场景

- 要从零设计落地页 / 仪表盘 / 设置页
- 团队需要统一的设计文档格式
- 需求已明确，只是缺一个结构起点
- 想把设计思路写清楚再交给实现

## 输入

- 页面类型（落地页 / 仪表盘 / 设置页 / 其他）
- 内容清单与目标
- 是否已有品牌规范

## 执行步骤

### 步骤 1 — 选骨架

| 页面类型 | 骨架顺序 |
|---|---|
| 落地页 | 首屏价值主张 → 社会证明 → 功能 / 卖点 → 使用场景 → 价格 → FAQ → 结尾行动 |
| 仪表盘 | 顶部总览指标 → 主要图表区 → 明细列表 → 侧边筛选与操作 |
| 设置页 | 分组导航 → 每组一组配置项 → 危险操作区单独置底 |
| 表单页 | 分步（信息多时）→ 每步一组相关字段 → 校验提示 → 提交与结果 |

### 步骤 2 — 用模板填空

以落地页为例，逐节填写：

```
## 首屏
一句话价值：<这东西是什么、给谁、带来什么结果>
主行动：<按钮文案>
次行动：<有就写，没有就删掉这一项>
视觉焦点：<主图 / 产品截图 / 动效>

## 社会证明
可用的真实证据：<客户名 / 数据 / 评价，必须真实，没有就删掉这一节>

## 卖点（3 个，每个一段）
1. <解决了什么问题> → <带来的结果>
2. …
3. …

## FAQ
<用户真正会犹豫的问题，不是自己想被问的问题>
```

### 步骤 3 — 删掉没有内容的节

**没有真实社会证明就删掉那一节**，不要放一排灰色的假 logo。空节的视觉占位会稀释真正的卖点。

### 步骤 4 — 标注每节的目标与判据

每节写下：这一节要让用户产生什么想法 / 动作，以及怎么判断它有效（如点击率、停留时长）。

### 步骤 5 — 转成实现

结构确认后按 `frontend-design` 落实到布局与代码。模板到此结束，不要继续在 Markdown 里"设计"。

## 输出

- 填好的页面模板（每节有内容、目标、判据）
- 被删掉的节及其原因
- 交给实现的说明

## 反模式

- **照抄模板不删空节**：假的社会证明比没有更伤信任
- **把模板当最终设计**：模板只解决起点
- **FAQ 写自己想被问的问题**：要写用户真正犹豫的点
- **在 Markdown 里细化到像素**：模板之后应进入实现
- **每节没有判据**：无法判断哪一段该改

## 参考

- 结构落实用 `frontend-design`；配色与字体用 `theme-factory`。
