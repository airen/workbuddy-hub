# 09 · converge（收敛）

**命令**：`converge`　**频率**：每次 `implement` 之后　**产物**：**只能追加任务到 `tasks.md`**（绝不改代码）

## 它做什么

拿当前**代码库**对照本功能的 `spec.md` / `plan.md` / `tasks.md`，确认**没有任何东西被漏掉**。

## 三条硬约束

1. **append-only** —— 绝不编辑或删除代码
2. **唯一的写操作**是往 `tasks.md` 追加任务
3. **必须在当前 `tasks.md` 跑过 `implement` 之后**才能跑

## 两种结果

### ✅ Converged

没找到缺口。`tasks.md` **逐字节不变**，输出：

```
✅ Converged — the implementation satisfies the spec, plan, and tasks.
```

→ 完工。可以去评审或开 PR。

### 📋 Tasks appended

找到缺口。把缺口作为**新任务追加到 `tasks.md` 的 `## Convergence` 段**，并告诉用户追加了几条。

→ 再跑一次 `implement` 完成它们 → 再跑 `converge`。

**每一轮发现的条目会变少**，重复直到报告 `Converged`。

## 报告格式

先打印**按严重度分级的发现摘要**，再给结论。

## 铁律

> **缺失的验证 ≠ 成功的修复。**

如果某个验收场景没有被验证过，**不许报告为 Converged**。报告必须诚实地落在 `Converged` 或 `Tasks appended` 二者之一，没有第三种。

## 收尾

告诉用户：本轮结论（Converged / 追加了 N 条）、本轮发现了什么、需不需要再循环一轮。
