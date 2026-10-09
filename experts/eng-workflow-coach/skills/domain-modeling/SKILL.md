---
name: domain-modeling
display_name: "领域建模"
display_name_en: "Domain Modeling"
description: "主动构建并磨利项目的领域模型：挑战术语、打磨模糊用语、就地更新 GLOSSARY.md、按需记录 ADR。适用于「这个术语到底指什么」「帮我理一下领域模型」「写个 ADR」「更新术语表」「domain modeling」这类需求。"
description_zh: "主动构建并磨利项目的领域模型，就地更新术语表与 ADR"
description_en: "Build and sharpen a project's domain model; update GLOSSARY.md and ADRs inline."
category: development-tools
version: 1.0.0
author: "大漠"
agent_created: true
---

# 领域建模（domain-modeling）

在设计的过程中主动构建并磨利项目的领域模型。这是一门*主动的*纪律：挑战术语、发明边界情况（edge case）场景，并在术语表（glossary）和决策一旦成形的那一刻就把它们写下来。（仅仅*读* `GLOSSARY.md` 拿词汇不算本技能：那是任何技能都能做的一行习惯。本技能用在你要*改变*模型的时候，而不只是消费它。）

## 文件结构

大多数仓库只有一个上下文（context）：

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

如果仓库根目录存在一个 `GLOSSARY-MAP.md`，说明这个仓库有多个上下文。这份映射表指出每个上下文住在哪里：

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← 系统级决策
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← 上下文特有的决策
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

惰性创建文件：只在有东西可写的时候才建。如果没有 `GLOSSARY.md`，就在第一个术语被敲定时创建它。如果没有 `docs/adr/`，就在需要第一个 ADR 时创建它。

## 会话进行中

### 拿术语表来挑战

当用户使用的术语跟 `GLOSSARY.md` 里已有的语言冲突时，立刻指出来。「你的术语表把 'cancellation' 定义为 X，但你似乎指的是 Y。到底是哪个？」

### 打磨模糊用语

当用户使用含糊或含义过载的术语时，提出一个精确的规范术语。「你说 'account'：你指的是 Customer 还是 User？这是两个不同的东西。」

### 讨论具体场景

在讨论领域关系时，用具体的场景对它们做压力测试。发明一些能探到边界情况、并迫使用户把概念之间的边界说清楚的场景。

### 与代码互相印证

当用户说明某个东西是怎么运作的，去核对代码是否同意。如果发现矛盾，把它摆到台面上：「你的代码取消的是整张 Order，但你刚说可以部分取消。哪个是对的？」

### 就地更新 GLOSSARY.md

当一个术语被敲定时，就地更新 `GLOSSARY.md`。不要攒起来批量处理：发生时就记下来。使用 [GLOSSARY-FORMAT.md](references/GLOSSARY-FORMAT.md) 里的格式。

`GLOSSARY.md` 应当完全不含实现细节。不要把 `GLOSSARY.md` 当作规格说明、草稿本，或者实现决策的存放处。它是术语表，仅此而已。

### 谨慎地提议写 ADR

只有在以下三条全部成立时，才提议创建一个 ADR：

1. **难以逆转**：以后改主意要付出的代价是实打实的
2. **脱离上下文会让人意外**：未来的读者会纳闷「他们当初为什么要这么做？」
3. **是一次真正取舍的结果**：确实存在备选方案，而你出于特定理由选了其中一个

三条里缺任何一条，就跳过 ADR。使用 [ADR-FORMAT.md](references/ADR-FORMAT.md) 里的格式。
