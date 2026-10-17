---
name: design-style-library
version: "1.0.0"
description: "Library of 67 named, production-ready design-system specs (tokens, typography, component rules, WCAG 2.2 AA, do/don't, QA gates) for AI-generated UI: shadcn, Material, Ant, Claude, Codex, bento, brutalism, glassmorphism, claymorphism, neumorphism, riso, neon, retro, editorial and more. Use whenever the user names a visual style or says 'like <product>' (Notion, Linear, Vercel, Stripe…), wants a page to follow one consistent design language, or needs exact color/font/spacing tokens instead of vibe-based guesses. Read INDEX.md first, then only the one style file that matches."
category: design-tools
---

# 设计风格库（67 种）

67 套**已命名、开箱即用**的设计系统规范。每套 = 规则文件（`references/<分类>/<slug>.md`：品牌意图、设计基础、组件族、无障碍、语气、Do/Don't、质量门禁）+ 令牌文件（`references/<分类>/<slug>.tokens.md`：精确色值、字体、字阶、间距）。

> 主题从描述里**生成**（theme-factory），情报从数据库里**检索**（ui-ux-pro-max）；
> 这里提供的是**成品规范**——用户点名风格时，直接照规范落地，不再从零起念头。

## 何时用本库

- 用户**点名**了一种风格或参照物：「按 shadcn 做」「像 Linear 那种」「毛玻璃的」「粗野一点」
- 用户要的页面必须**严格遵循某套设计语言**（品牌手册、竞品复刻、设计系统落地）
- 需要**精确的设计令牌**（十六进制色值、字体栈、间距刻度），不想靠感觉猜
- `ui-ux-pro-max` 检索出方向后，要落成一套**可执行的单风格规范**

## 使用步骤

1. **读 `references/INDEX.md`**：67 行总表 + 「用户这样说 → 先看哪些 slug」速查。 slug 拿不准时只看索引，不要 67 个文件全翻。
2. **读那一个风格的 `<slug>.md`**：理解设计意图与规则（含 Do/Don't 与质量门禁）。
3. **读 `<slug>.tokens.md`**：把精确令牌取出来填进实现（CSS 变量 / Tailwind 配置）。
4. **落地**：结构按 `frontend-design` 的层级方法走，视觉按本库规范走。
5. **自检**：过一遍规范末尾的质量门禁；无障碍（WCAG 2.2 AA、键盘优先、可见焦点态）是不可谈判项。

## 分类速览

| 目录 | 内容 | 数量 |
|---|---|---|
| `references/platform/` | 平台与品牌设计语言（shadcn、Material、Ant、Claude、Codex、Square…） | 10 |
| `references/modern/` | 现代与通用 UI（minimal、premium、editorial、bento 之外的通用风） | 31 |
| `references/texture/` | 材质与印刷质感（毛玻璃、新拟物、粘土、Riso、纸张、手绘） | 11 |
| `references/retro/` | 复古、游戏与实验（粗野、像素、赛博、霓虹、宇宙） | 15 |

## 铁律

1. **单风格原则**：一页只用一套规范；两个风格的需求拆成两页，不在一套 UI 里混搭令牌。
2. **令牌优先**：色值、字体、间距以 `<slug>.tokens.md` 为准，不现场另编；规范未覆盖的少数值，从既有令牌推导并说明推导路径。
3. **可访问性赢**：任何风格规则与 WCAG 2.2 AA 冲突时，按规范要求优先可访问性（对比度不足就调明度保色相）。
4. **规则可执行**：每条 do 配一个 don't；交付前过规范自带的质量门禁，过不了就改实现，不改规范。
5. **不唯风格论**：风格回答「长什么样」，不回答「排什么」——信息层级与动线仍由 `frontend-design` / `design-templates` 决定。

## 上游归属

移植自 [bergside/awesome-design-skills](https://github.com/bergside/awesome-design-skills)（MIT，© Bergside），
67 个技能原样保留（仅剥离上游 CLI 的管理标记、补 `version` / `category` 两个 frontmatter 字段）。
归属与搬运范围详见专家包根目录 `LICENSE`。
