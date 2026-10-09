# 转换规范：mattpocock/skills → WorkBuddy skill

源仓库：`/tmp/mp-skills`（https://github.com/mattpocock/skills，MIT）
产出目录：`/tmp/mp-convert/out/<skill-name>/`

## 一、目标格式

```
<skill-name>/
├── SKILL.md          (必需)
├── references/       (可选，原仓库的附属 .md 放这里)
├── scripts/          (可选，原仓库的脚本放这里)
└── templates/        (可选，模板文件。注意官方叫 templates/，不是 assets/)
```

`SKILL.md` 结构 —— **本地自用**只要三个字段：

```markdown
---
name: <skill-name>
description: <中文描述，一段话>
agent_created: true
---

# <中文标题>

<正文，中文>
```

**要上架应用市场**，按官方上架文档（<https://open.workbuddy.cn/docs/skill>）补全：

```markdown
---
name: <skill-name>
display_name: <中文展示名>
display_name_en: <英文展示名>
description: <写清用途和触发词 —— 模型据此决定何时加载>
description_zh: <简短中文介绍，一行>
description_en: <简短英文介绍，一行>
category: <分类之一>
version: 1.0.0
author: <合作方名称>
---

# <中文标题>

<正文，中文>
```

### frontmatter 规则（硬性）

1. **本地自用**三个字段即可：`name`、`description`、`agent_created: true`。
   **市场发布**再加 `display_name` / `display_name_en` / `description_zh` / `description_en` / `category` / `version` / `author`（其中后四项与 `description_zh` / `description_en` 是官方文档标注的必填项）。
2. `name` **必须等于目录名**，用 kebab-case 英文原名，**不翻译**（如 `code-review`、`grill-me`）。保留原名是为了跟上游对照、方便后续拉更新。
3. `description` 用中文写，必须同时回答三件事：
   - 这个技能**做什么**（第三人称，如「该技能用于…」）
   - **什么时候该用**（触发场景）
   - **触发关键词**（把用户可能说的中文原话也列进去，如「拷问我」「帮我 review 一下」「红绿重构」）
   长度控制在 60–200 字，不要写成一大段。这是模型选择技能的唯一依据，写得越具体命中率越高。
   `description_zh` / `description_en` 是市场卡片上的一行简介，要另外写，**不要**直接把长 description 复制过去。
4. **不要凭印象删字段。** 上游的 `disable-model-invocation`、`user-invocable`、`allowed-tools`
   在 WorkBuddy 里**都是被支持的**（官方上架文档明确列出），要**原样保留**。
   这条是踩过坑的：第一版误判「WorkBuddy 没有等价字段」，把 16 个技能上的
   `disable-model-invocation` 全删了，改变了技能的调用语义。**拿不准就去官方文档或已上架技能的实际 frontmatter 里查证。**
5. **确实要处理的字段**：
   - `argument-hint`：WorkBuddy 无此字段。语义（这个技能需要用户提供什么输入）要**融进 description 或正文开头的「输入」小节**，不能丢。
   - `metadata` / `metadata.credits`：WorkBuddy 无此字段。里面的署名（作者、组织、URL）**不能丢**，移到正文最末尾的「## 来源与致谢」小节。
   - `agents/openai.yaml`（Codex 专属）：直接丢弃。
6. `category` 的合法取值（从市场真实技能反查，**官方文档示例里的 `writing` 不在其中**）：
   `development-tools`、`productivity-tools`、`content-creation`、`data-analysis`、
   `business-operations`、`knowledge-learning`、`collaboration`、`investment-finance`。

## 二、正文转换规则

### 2.1 语言

全文中文。但**技术术语保留英文原词**，首次出现时中文（English）形式，之后可只用中文或只用英文：

| 原文 | 写法 |
| --- | --- |
| seam | 接缝（seam） |
| deep module | 深模块（deep module） |
| tracer bullet | 曳光弹（tracer bullet） |
| red-green-refactor | 红-绿-重构（red-green-refactor） |
| design tree / frontier | 设计树（design tree）/ 前沿（frontier） |
| vertical slice | 垂直切片（vertical slice） |
| blast radius | 影响半径（blast radius） |
| glossary | 术语表（GLOSSARY.md） |

代码块、命令、文件名、字段名、`GLOSSARY.md` / `ADR` / `CONTEXT.md` 等约定名**一律保持原样不翻译**。

### 2.2 交叉引用（重要）

原仓库用 `/xxx` 表示「调用另一个技能」。WorkBuddy 里技能通过 Skill 工具加载，用户也可以用 `/技能名` 触发。统一改成：

- 原文 `` `/tdd` `` → `` `tdd` 技能 `` 或「加载 `tdd` 技能」
- 原文 `Call the Skill tool with "grilling".` → 「调用 Skill 工具加载 `grilling` 技能。」
- 原文 `Call the Skill tool twice, for "grilling" and "domain-modeling".` → 「依次调用 Skill 工具加载 `grilling` 和 `domain-modeling` 两个技能。」
- 原文 `tell the user to run /setup-matt-pocock-skills` → 「提示用户先运行 `setup-matt-pocock-skills` 技能完成本仓库初始化」

### 2.3 Claude Code 专属概念的映射

| 原文 | 改成 |
| --- | --- |
| sub-agent / spawn a sub-agent | 子代理（用 Agent 工具） |
| background agent | 后台子代理 |
| `AGENTS.md` / `CLAUDE.md` | 保留 `AGENTS.md`；提到 `CLAUDE.md` 时写成「`AGENTS.md`（或 `CLAUDE.md`）」 |
| Claude Code hooks | 说明这是 Claude Code 专属，给出等价的手工/脚本方案 |
| `.claude-plugin` | 删掉，与 WorkBuddy 无关 |
| `.scratch/` 目录 | 保留原样（这是作者约定的临时目录名） |
| `docs/agents/issue-tracker.md` | 保留原样（由 `setup-matt-pocock-skills` 生成） |

### 2.4 附属文件

- 原仓库里跟 `SKILL.md` 同级的 `*.md`（如 `tests.md`、`mocking.md`、`ADR-FORMAT.md`、`HTML-REPORT.md`）→ 移到 `references/` 下，**内容同样翻成中文**。
- 原仓库的 `scripts/*`（如 `hitl-loop.template.sh`）→ 移到 `scripts/` 下，**内容保持英文**（是给机器执行的，注释可保留英文）。
- 原仓库的 `agents/openai.yaml` → **直接丢弃**（Codex 专属，与 WorkBuddy 无关）。
- 正文里的相对链接必须改对：`[tests.md](tests.md)` → `[tests.md](references/tests.md)`。
- 大文件（>10k 词）在 SKILL.md 里补一句「用 Grep 在该文件里搜关键词定位」的提示。

### 2.5 保留原意，不要自由发挥

- **不要增删原技能的步骤、阶段、清单项。** 原文有几个 phase 就是几个 phase。
- **不要软化**原文的强硬语气。「Refuse to give up」「Do NOT proceed」这类命令式要保留，中文写成「不许放弃」「未完成不得进入下一阶段」。
- 原文的 ✅ / ❌ / 勾选框 `- [ ]` 保留。
- 原文的 ASCII 图、代码块结构保留。
- 原文的引用块（`> 引语 — 出处`）保留，人名书名不翻译（如 `The Pragmatic Programmer`）。

## 三、样板

两个样板已经写好，转换风格、详略程度、术语处理**一律照抄**：

- `/tmp/mp-convert/out/grilling/SKILL.md` —— 薄技能（正文只有一段纪律）
- `/tmp/mp-convert/out/tdd/SKILL.md` + `references/` —— 中等技能（带附属文件、带清单）

开始转换前**必须先读这两个样板**。

## 四、自检清单

每个技能写完，逐条确认：

- [ ] frontmatter 字段齐全：本地自用 `name` / `description` / `agent_created`；市场发布再补 `display_name` / `display_name_en` / `description_zh` / `description_en` / `category` / `version` / `author`
- [ ] `name` 与目录名完全一致
- [ ] `description` 是中文，含触发场景与关键词，第三人称
- [ ] `description_zh` / `description_en` 是独立写的一行简介，不是把长 description 复制过去
- [ ] `category` 取值在市场真实分类集合内
- [ ] 正文没有残留的 `/tdd`、`/code-review` 这类斜杠引用（已改成「`xxx` 技能」）
- [ ] 正文没有残留的 `argument-hint`、`sub-agent`（裸英文）、`CLAUDE.md`（裸用）
- [ ] **上游的 `disable-model-invocation` / `user-invocable` / `allowed-tools` 已原样保留**（它们是 WorkBuddy 支持的字段）
- [ ] 附属文件已放进 `references/` 或 `scripts/`，正文链接指向 `references/xxx.md` 且文件确实存在
- [ ] 原 `metadata.credits` 的署名已移到文末「## 来源与致谢」
- [ ] 原 `argument-hint` 的语义没有丢
- [ ] frontmatter 能被 YAML 解析器解析（`yaml.safe_load` 跑一遍）
