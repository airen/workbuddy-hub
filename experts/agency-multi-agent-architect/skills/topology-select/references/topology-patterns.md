# 五种拓扑模式

> 本文内容逐字抽取自 [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)（MIT 协议）。
> 已做：剥 frontmatter、章节 emoji 前缀归一、AI 平台品牌名中性化。未做：任何内容改写。

## 模式 1 — 顺序链（Sequential Chain）

```
Input → Agent A → Agent B → Agent C → Output
```

**适用于：**
- 每一步都依赖上一步的输出
- 任务有自然的线性推进（research → draft → review → publish）
- 调试简单性的优先级高于延迟

**故障模式**：单个智能体故障会让整条流水线停摆。Agent C 看不到 Agent A 的推理——上下文损失在多跳中累积。

**设计规则：**
- 在智能体间传递结构化输出，而非原始散文（减少误读）
- 包含一个简短的"上下文摘要"字段，每个智能体为下游智能体追加
- 设置链的最大长度：>5 个智能体的链通常会出现输出质量退化
- 定义每个智能体接收什么、产出什么，以及不负责什么

---

## 模式 2 — 并行 Fan-Out / Fan-In

```
              ┌→ Agent A ─┐
Input → Router ├→ Agent B ─┤→ Synthesizer → Output
              └→ Agent C ─┘
```

**适用于：**
- 子任务相互独立、可并发运行
- 降低延迟是优先目标
- 对同一输入的多个视角有价值（例如 法务 + 财务 + 技术 评审）

**故障模式**：若某个智能体失败则得到部分结果。Synthesizer 必须优雅地处理缺失分支。若智能体共享可变状态则会出现竞态条件。

**设计规则：**
- Fan-out 中的智能体必须真正独立——不能共享可变状态
- Synthesizer 必须显式处理：全部结果到齐、部分结果、零结果
- 在动手前定义合并策略：投票、加权、拼接，或交由人工
- Fan-out 宽度上限：>7 个并行智能体通常会超出综合质量阈值

---

## 模式 3 — 层级式（Orchestrator-Subagent）

```
                    ┌→ Subagent A
Orchestrator ───────├→ Subagent B
                    └→ Subagent C
         ↑____feedback_____|
```

**适用于：**
- 任务复杂且需要动态拆解
- 子任务集合无法预先确定
- 质量控制需要一个协调判断层

**故障模式**：Orchestrator 成为瓶颈。Orchestrator 的 prompt 复杂度无界增长。Subagent 在各自局部目标上"成功"却彼此矛盾。

**设计规则：**
- Orchestrator 的职责是拆解、委派与综合——而非执行
- Orchestrator 必须维护一个任务台账：委派了什么、给了谁、状态如何、产出是什么
- Subagent 必须返回结构化结果 + 置信度信号，而非仅仅给答案
- Orchestrator 必须检测 subagent 输出之间的矛盾并显式解决
- 限制 orchestrator 上下文窗口的消耗：subagent 输出应被摘要，而非整段追加

---

## 模式 4 — Evaluator-Optimizer 循环

```
Generator → Evaluator → [pass] → Output
     ↑_______[fail + feedback]__|
```

**适用于：**
- 输出质量可度量或可打分
- 预期首轮输出并不完美
- 迭代精炼值得付出延迟/成本的权衡

**故障模式**：若 evaluator 标准不可能满足或自相矛盾则陷入无限循环。Generator 在 N 次迭代后停止改进（收益递减）。Evaluator 与 generator 共享同样的盲点。

**设计规则：**
- Evaluator 必须使用与 Generator 指令不同的评判框架
- 定义硬退出：无论 evaluator 分数如何，最大迭代数（建议：3）
- Evaluator 输出必须结构化：分数、具体失败原因、可执行的反馈
- 记录每次迭代的分数——若分数在连续 2 次迭代中停滞，则退出并上报
- Generator 与 Evaluator 理想上应是不同模型或拥有不同 system prompt

---

## 模式 5 — Mesh / 对等网络（Peer Network）

```
Agent A ⟷ Agent B
  ⟷         ⟷
Agent C ⟷ Agent D
```

**适用于：**
- 智能体需要协商或达成共识
- 没有单个智能体拥有足够上下文来做最终决策
- 模拟多元专家小组的审议

**故障模式**：复杂度最高。循环依赖。共识死锁。智能体互读彼此输出导致上下文指数级增长。极难调试。

**设计规则：**
- 对生产系统来说很少是正确选择——优先默认层级式
- 需要一个 moderator 智能体或终止条件（最大轮数、共识阈值）
- 每个智能体对同侪输出的读取权限应被划定范围：完整逐字记录 vs. 摘要
- 定义显式的共识机制：多数、全体一致、按置信度加权
- 构建熔断器：若 N 轮后仍无共识，则上报人工

---
