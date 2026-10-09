# 08 · implement（执行）

**命令**：`implement`　**频率**：可多次（大功能分阶段跑）　**产物**：真实代码 + 更新的 `tasks.md` 勾选状态

## 前置关卡

执行前先**读** `checklists/*.md` 的勾选状态当关卡：

- 统计已勾选 / 未勾选数量
- **有任何未勾选项时，必须先问用户**再继续
- **标记是只读的** —— `implement` 绝不能改清单标记

> 对自定义清单，`[x]` 意味着**评审人认可需求质量**，不代表实现完成。别把它当成"任务已完成"来读。

## 执行方式

### 小功能：一次跑完

```
/implement
```

### 大功能：分阶段跑（强烈推荐）

**不要试图一次实现完一个大功能** —— 会压垮上下文，而且中途出错很难定位。用参数限定范围：

```
/implement Implement only the Setup and Foundational phases: project scaffolding and the project/task data model with basic CRUD. Stop before the user-story features.
```

```
/implement Now implement the Kanban board user story: drag-and-drop between columns.
```

**每个阶段跑完必须验证通过，再进下一阶段。**

## 执行顺序

1. 按 `tasks.md` 的**阶段顺序**（Setup → Foundational → 各用户故事 → Polish）
2. 阶段内**尊重 `[P]` 并行标记**（不同文件无依赖的任务可并行）
3. 阶段内尊重任务声明的依赖（如 `T014 depends on T012, T013`）
4. 测试优先的话：**测试先写、确认失败、再写实现让测试通过**

## 每完成一个任务

- 在 `tasks.md` 里把 `- [ ]` 改成 `- [x]`
- 在阶段边界**停下来验证**（Checkpoint），别一口气冲到底

## 实现中发现了规格问题怎么办

**不要就地打补丁。** 记下来，告诉用户，回 `specify` / `clarify` / `plan` / `tasks` 改源头，改完重跑 `analyze`，再继续实现。

## 收尾

告诉用户：
- 完成了哪些阶段 / 哪些任务（`T0xx`–`T0yy`）
- 跑通了什么验证（命令 + 结果）
- 还剩哪些阶段
- **下一步是 `converge`**（不是直接宣布完工）
