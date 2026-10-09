# 领域文档（Domain Docs）

工程技能在探索代码库时，应如何消费这个仓库的领域文档。

## 探索之前，先读这些

- 仓库根目录的 **`GLOSSARY.md`**，或者
- 仓库根目录的 **`GLOSSARY-MAP.md`**（如果存在）：它指向每个上下文各一份 `GLOSSARY.md`。把跟主题相关的每一份都读了。
- **`docs/adr/`**：读那些触及你即将动工区域的 ADR。在多上下文仓库里，也检查 `src/<context>/docs/adr/` 里上下文范围内的决策。

如果这些文件任何一个不存在，**静默继续**。不要点出它们缺席；不要建议提前创建它们。`domain-modeling` 技能（经由 `grill-with-docs` 和 `improve-codebase-architecture` 到达）会在术语或决策真正被解决时，惰性地创建它们。

## 文件结构

单上下文仓库（大多数仓库）：

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文仓库（根部存在 `GLOSSARY-MAP.md`）：

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← 全系统决策
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← 上下文专属决策
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## 使用术语表的词汇

当你的产出命名一个领域概念时（在 issue 标题、重构提议、假设、测试名里），使用 `GLOSSARY.md` 中定义的术语。不要漂移到术语表明确回避的同义词上。

如果你需要的概念还不在术语表里，那是一个信号：要么你在发明项目并不使用的语言（重新考虑），要么确实存在一个缺口（记下来给 `domain-modeling` 技能）。

## 标出 ADR 冲突

如果你的产出跟一个已有的 ADR 矛盾，明确地摆出来，而不是默默覆盖：

> _跟 ADR-0007（事件溯源订单）矛盾，但值得重开，因为……_
