# 示例：技能链——一段对话到可运行代码

**引用资产**：`skills/to-spec` → `skills/to-tickets` → `skills/implement`（均为 development 类）

这是三个独立技能接力最常用的一条链路，演示「技能不是孤立功能，而是一条流水线」。

## 触发方式

1. 先说：「写成规格」（或「把刚才聊的整理成方案」）→ `to-spec`
2. 再说：「拆成工单」（或「切成可执行的步骤」）→ `to-tickets`
3. 最后说：「开始实现」（或「按工单做」）→ `implement`

## 输入 / 输出

| 步骤 | 输入 | 输出 |
|---|---|---|
| `to-spec` | 当前对话已讨论过的需求 + 代码库理解 | 一份规格说明，发布到 issue 追踪器 |
| `to-tickets` | 上一步的规格 | 一组曳光弹工单，每张声明自己的阻塞边（blocking edge） |
| `implement` | 工单 + 约定好的接缝（seam） | 按接缝 TDD 实现的代码，跑完类型检查与单测 |

## 过程要点

- `to-spec` **不做访谈**，只综合已经讨论过的内容（访谈用 `interview-me` 类技能）
- `to-tickets` 的工单带阻塞关系：本地是每张工单一个文件、边写成文本，
  真实追踪器上则用原生阻塞链接
- `implement` 收尾时自动调用 `code-review` 技能评审，再把工作提交到当前分支

## 验证

- 规格能回答「做什么、不做什么、验收标准是什么」
- 工单图的阻塞边无环，最小工单集可独立运行
- 实现分支上 `git log` 可见按工单原子提交，测试全绿

## 资产路径

- `skills/to-spec/SKILL.md`
- `skills/to-tickets/SKILL.md`
- `skills/implement/SKILL.md`
- 配套：`skills/tdd/`（循环纪律）、`skills/code-review/`（收尾评审）
