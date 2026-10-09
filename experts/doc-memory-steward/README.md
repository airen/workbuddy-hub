# 项目文档管家 · 纪文远

一个文档优先的项目管家：把散落各处的项目知识，变成**一个能读、能改、能提交、能分享的文档工作区**。

## 类型

Agent 型（单个 AI 专家）

## 定位

Agent 记不住你的项目，不是"记忆容量"问题，是**知识没有落在可读、可改、可提交的地方**。

市面上的记忆插件都在解同一道错题：把对话切成片段塞进向量库，每次提示检索最相似的几条注入，再给 agent 一个搜索工具去翻旧账。这套架构建立在"agent 会遗忘，所以要帮它记住过去"的假设上——于是它捕获得更多、索引得更好、检索得更聪明，却始终回答不了一个问题：**哪一条是对的、是当前的、是完整的？**

**纪文远**管的是另一件事：**把事情写下来，然后用那些记录。**

```
prompt → build → forget              记忆插件
prompt → consult → build → update     文档即记忆
```

## 功能

| # | 能力 | 内容 |
|---|------|------|
| 1 | **建脑** | 盘点现有文档 → 建索引 → 写约定 → 补最近一次决策；六类文档固定分类 |
| 2 | **查脑** | 开工前读索引、读全文（不是搜关键词）、查不到就记"新领域"、发现不符以现实为准 |
| 3 | **更新脑** | 收尾三问 + 更新触发事件表 + "没有就不写"的纪律 |
| 4 | **文档写作** | 为什么 > 是什么、一份文档一个主题、状态三词、不抄代码只指位置 |
| 5 | **审计维护** | 孤儿文档 / 断链 / 过期 / 冲突四类问题，配可跑的审计脚本 |
| 6 | **落地** | 全新项目 / 已有项目 / 团队协作三条路径；抢救"只存在于人脑里的知识" |
| 7 | **迁移** | 从记忆插件迁到文档工作区，并划清与 RAG 的边界 |
| 8 | **守门** | 用户说"接个记忆插件"时，讲清为什么不这么做 |

### 核心方法论

工作流是**文档优先**的七步：判断有没有脑 → 建脑（只做一次）→ 查脑 → 干活 → 更新脑 → 审计 → 交付说明。

### 七条信条

1. **Agent 要的不是记忆，是文档**
2. **先查后干，不许凭记忆猜**
3. **干完就更新，趁热**
4. **没有就不写**（为写而写是另一种噪音）
5. **文档是给人看的**（纯 Markdown、进 git、能 diff、能 review、能分享）
6. **写"为什么"，不写"是什么"**
7. **现实永远是真相的来源**（文档和代码打架时，改文档）

## 包含的技能

### `agent-doc-memory`

| 目录 | 内容 |
|------|------|
| `references/` | 7 篇：为什么召回式记忆是错题 / 工作区结构 / 查脑协议 / 更新协议 / 好文档标准 / 审计维护 / 落地路径 |
| `templates/` | 6 份：`INDEX.md`、`conventions.md`、`glossary.md`、`spec.md`、`decision.md`、`research.md` |
| `scripts/` | `init_doc_brain.py`（建骨架，不覆盖已有文件）、`doc_audit.py`（孤儿 / 断链 / 过期审计） |

## 六类文档

| # | 文档 | 回答的问题 | 关键判据 |
|---|---|---|---|
| ① | `INDEX.md` | 有哪些文档、先读哪个？ | 每条都指向存在的文件 |
| ② | `conventions.md` | 在这个项目里活该怎么干？ | 每条都有"为什么" |
| ③ | `glossary.md` | 这个词在本项目里指什么？ | 有"不指什么" |
| ④ | `specs/` | 要做什么、不做什么、怎么算完成？ | 有不做清单 + 验收标准 |
| ⑤ | `decisions/` | 为什么这么做、放弃了什么？ | 有备选 + 代价 + 重估触发点 |
| ⑥ | `research/` | 这个库 / API 怎么用、坑在哪？ | 结论先行、可复用 |

## 使用示例

- 「它老是记不住我们项目的约定」→ 建 `docs/conventions.md` + 写进 `AGENTS.md` 的硬指令
- 「每次新会话都要重新解释一遍架构」→ 建 `decisions/`，把历史决策补成记录
- 「我们为什么当初没用 X？」→ 查 `decisions/`，没有就补一篇，写明代价与重估触发点
- 「这个 SDK 怎么用我查过一次又忘了」→ 建 `research/<sdk>.md`，结论先行
- 「帮我接手这个项目」→ 先跑 `doc_audit.py` 看文档健康度，再按索引读
- 「文档太乱了，没人看」→ 审计孤儿文档与断链，收进索引或删掉
- 「给我接个记忆插件吧」→ 先讲清为什么不这么做，再给文档工作区方案

## 常用命令

```bash
# 在项目里建文档工作区骨架（已存在的文件不会被覆盖）
python3 skills/agent-doc-memory/scripts/init_doc_brain.py /path/to/project

# 审计：孤儿文档 / 断链 / 过期文档
python3 skills/agent-doc-memory/scripts/doc_audit.py /path/to/project
python3 skills/agent-doc-memory/scripts/doc_audit.py /path/to/project --stale-days 60
python3 skills/agent-doc-memory/scripts/doc_audit.py /path/to/project --fail-on-issue   # 可进 CI
```

## 与 RAG 的边界

本专家**不否定 RAG**，而是划清边界：

- **项目自身的知识**（约定、规格、决策、调研、术语）→ **写下来**。你有能力也有责任把它写清楚。
- **外部海量非结构化语料**（产品手册、法规全文、论文库）→ **用 RAG**。你没法把它整理成一份份文档，召回是合理的。

> 一句话判据：**能写下来的，就写下来；写不下来的，才去检索。**

## 目录结构

```
doc-memory-steward/
├── .codebuddy-plugin/plugin.json
├── agents/
│   └── doc-memory-steward.md          # Agent 主提示词（七条信条 + 能力表 + 路由表 + 七步流程）
├── skills/
│   └── agent-doc-memory/
│       ├── SKILL.md                   # 技能入口
│       ├── references/                # 7 篇深度参考
│       ├── templates/                 # 6 份可填模板
│       └── scripts/                   # 2 个脚本
├── avatars/
│   └── doc-memory-steward.png
└── README.md
```

## 头像

头像已生成在 `avatars/` 目录下。如需替换为自定义头像，要求：

- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 安装

将专家包目录放到专家目录下：

```
$WORKBUDDY_CONFIG_DIR/plugins/marketplaces/my-experts/plugins/doc-memory-steward/
```

（`WORKBUDDY_CONFIG_DIR` 未设置时默认 `~/.workbuddy`）

然后运行注册命令使其可见：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
python3 scripts/package_expert.py <expert-dir> <output-dir>
```

## 来源与致谢

- 核心论点来自 **Kevin Liao（Aerovato Research）** 的文章《Agent 不需要记忆，它们需要文档》（*Agents don't need memory, they need documentation*，2026-10-03），及其据此实现的 **Operator Memory** 插件（[github.com/aerovato/operator-memory](https://github.com/aerovato/operator-memory)，原文 [liao.gg/blog/agents-dont-need-memory](https://liao.gg/blog/agents-dont-need-memory)）。
- 本专家为面向 agent 的可执行化封装：把原文的判断转成可触发的行为约束、六类文档的结构判据、查 / 更新两份协议、审计脚本与可填空模板。**内容按自己的口径重写与扩充，无第三方代码依赖、无原文照抄。**

## 许可

原创方法论封装，**无第三方代码依赖**，可自由分发。作者：大漠。
