# 文档即记忆（agent-doc-memory）

把 agent 的记忆做成一个**能读、能改、能提交**的 Markdown 文档工作区，让它干活前先查、干完再更新。

**核心判断**：Agent 记不住你的项目，不是"记忆容量"问题，是**知识没有落在可读、可改、可提交的地方**。

记忆插件把对话切成片段塞进向量库，每次提示注入最相似的几条——这是在解一道错题：它试图用"检索过去的对话"替代"写下当前的事实"。结果你拿到的是每次提示上的 RAG 抽奖，而不是对项目的理解。

正确做法是给 agent 一个文档工作区：

```
prompt → build → forget            记忆插件
prompt → consult → build → update   文档即记忆
```

方法来源：Kevin Liao（Aerovato Research）《Agent 不需要记忆，它们需要文档》及其 Operator Memory 实现。

## 目录结构

```text
agent-doc-memory/
├── SKILL.md                              # 技能定义（WorkBuddy / Claude Code 通用）
├── AGENTS.md                             # Codex / Cursor 等 AGENTS.md 系工具入口
├── README.md                             # 本文件
├── references/
│   ├── 01-why-not-recall.md              # 召回式记忆的 5 类失败 + 何时召回仍然对
│   ├── 02-workspace-layout.md            # 六类文档的结构、判据与示例
│   ├── 03-consult-protocol.md            # 查脑协议
│   ├── 04-update-protocol.md             # 更新协议（三问 + 触发事件）
│   ├── 05-doc-quality.md                 # 好文档标准
│   ├── 06-audit-and-maintenance.md       # 审计与维护
│   └── 07-bootstrap.md                   # 三种场景的落地路径
├── templates/
│   ├── INDEX.md                          # 索引骨架
│   ├── conventions.md                    # 约定骨架（含写进 AGENTS.md 的硬指令）
│   ├── glossary.md                       # 术语表骨架
│   ├── spec.md                           # 规格模板
│   ├── decision.md                       # 决策记录模板
│   └── research.md                       # 调研笔记模板
└── scripts/
    ├── init_doc_brain.py                 # 脚手架：建骨架，已存在文件不覆盖
    └── doc_audit.py                      # 审计：孤儿 / 断链 / 过期
```

## 六类文档

| # | 文档 | 回答的问题 | 关键判据 |
|---|---|---|---|
| ① | `INDEX.md` | 有哪些文档、先读哪个？ | 每条都指向存在的文件 |
| ② | `conventions.md` | 在这个项目里活该怎么干？ | 每条都有"为什么" |
| ③ | `glossary.md` | 这个词在本项目里指什么？ | 有"不指什么" |
| ④ | `specs/` | 要做什么、不做什么、怎么算完成？ | 有不做清单 + 验收标准 |
| ⑤ | `decisions/` | 为什么这么做、放弃了什么？ | 有备选 + 代价 + 重估触发点 |
| ⑥ | `research/` | 这个库 / API 怎么用、坑在哪？ | 结论先行、可复用 |

## 三端安装

| 平台 | 做法 |
|---|---|
| **WorkBuddy** | 把 `agent-doc-memory/` 整个目录拷到 `~/.workbuddy-ai/skills/`，重启后即按 `description` 自动触发。或从应用市场直接安装。 |
| **Claude Code** | 把 `agent-doc-memory/` 拷到 `~/.claude/skills/`（个人级）或项目内 `.claude/skills/`（项目级）。`SKILL.md` 的 frontmatter 是标准 Agent Skills 格式。 |
| **Codex / Cursor** | 把 `AGENTS.md` 拷到项目根目录（或 `~/.codex/AGENTS.md` 作为全局）。若同时保留 `references/`、`templates/`、`scripts/`，AGENTS.md 会引用到它们。 |

> 三个平台读的是同一套协议内核，只是入口文件不同：WorkBuddy 与 Claude 读 `SKILL.md`，Codex 系读 `AGENTS.md`。

## 用法示例

- 「它老是记不住我们项目的约定」→ 建 `docs/conventions.md` + 写进 `AGENTS.md` 的硬指令
- 「每次新会话都要重新解释一遍架构」→ 建 `decisions/`，把历史决策补成记录
- 「我们为什么当初没用 X？」→ 查 `decisions/`，没有就补一篇，并写明代价与重估触发点
- 「这个 SDK 怎么用我查过一次又忘了」→ 建 `research/<sdk>.md`，结论先行
- 「帮我接手这个项目」→ 先跑 `doc_audit.py` 看文档健康度，再按索引读
- 「文档太乱了，没人看」→ 审计孤儿文档与断链，收进索引或删掉

## 常用命令

```bash
# 在项目里建骨架（已存在的文件不会被覆盖）
python3 scripts/init_doc_brain.py /path/to/project

# 审计：孤儿文档 / 断链 / 过期文档
python3 scripts/doc_audit.py /path/to/project
python3 scripts/doc_audit.py /path/to/project --stale-days 60   # 自定义过期阈值
```

## 设计哲学

**记忆不该靠"召回过去"，该靠"写下现在"。** 这套技能的每个设计决定都服务于这一点：

- **六类文档固定分类** = 让 agent 知道"这类知识该放哪"，而不是随手丢进一个筐
- **INDEX.md 唯一入口** = 解决"不知道自己不知道"——agent 能一眼看到项目里有哪些知识，而不需要先猜关键词再搜
- **查 / 更新两份协议** = 把"记住"从运气变成流程
- **纯 Markdown + git** = 可读、可改、可 diff、可 review、可分享、**可审计**
- **更新触发事件表** = 补上 agent 最缺的判据：什么时候该写
- **"没有就不写"** = 与"捕获一切"划清界限，保住信噪比

## 与 RAG 的关系

本技能**不否定 RAG**，而是划清边界：

- **项目自身的知识**（约定、规格、决策、调研、术语）→ **写下来**，用本技能。你有能力也有责任把它写清楚。
- **外部海量非结构化语料**（产品手册、法规全文、论文库）→ **用 RAG**。你没法把它整理成一份份文档，召回是合理的。

详见 `references/01-why-not-recall.md`。

## 来源与致谢

- 核心论点来自 **Kevin Liao（Aerovato Research）** 的文章《Agent 不需要记忆，它们需要文档》（2026-10-03），及其据此实现的 **Operator Memory** 插件（[github.com/aerovato/operator-memory](https://github.com/aerovato/operator-memory)，原文 [liao.gg/blog/agents-dont-need-memory](https://liao.gg/blog/agents-dont-need-memory)）。
- 本技能为面向 agent 的可执行化封装，内容按自己的口径重写与扩充，**无第三方代码依赖、无原文照抄**。

## 许可

本技能为原创方法论封装，**无第三方代码依赖**，可自由分发。作者：大漠。
