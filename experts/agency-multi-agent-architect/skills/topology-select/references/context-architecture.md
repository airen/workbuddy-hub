# 上下文架构：预算、管理策略与划分规则

> 本文内容逐字抽取自 [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)（MIT 协议）。
> 已做：剥 frontmatter、章节 emoji 前缀归一、AI 平台品牌名中性化。未做：任何内容改写。

## 上下文预算问题

流水线中的每个智能体都消耗上下文。在一条 5 智能体顺序链里，上下文压力会累积：
- Agent A 接收：用户输入（500 tokens）
- Agent B 接收：用户输入 + Agent A 输出（1,500 tokens）
- Agent C 接收：之前的链 + Agent B 输出（3,500 tokens）
- Agent D 接收：之前的链 + Agent C 输出（7,500 tokens）
- Agent E 接收：之前的链 + Agent D 输出（15,000+ tokens）

上下文预算耗尽会导致：幻觉、指令遵循失败、关键早期上下文被截断。

## 上下文管理策略

**1. 摘要压缩（Summarization Compression）**
每个智能体产出两份输出：完整输出 + 压缩摘要（≤200 tokens）。
下游智能体接收前序步骤的摘要，而非完整输出。
风险：有损——关键细节可能在摘要中被丢弃。
缓解：定义哪些字段始终逐字保留（ID、决策、约束）。

**2. 结构化状态对象（Structured State Object）**
定义一个在智能体间传递的共享状态 schema。每个智能体只读取其所需字段、只写入其输出字段。

```json
{
  "task_id": "uuid",
  "original_input": "...",
  "constraints": ["...", "..."],
  "agent_outputs": {
    "researcher": { "summary": "...", "sources": [...], "confidence": 0.85 },
    "analyst": { "findings": "...", "risks": [...] },
    "writer": { "draft": "..." }
  },
  "decisions": [],
  "current_step": "writer",
  "status": "in_progress"
}
```

每个智能体只接收与其角色相关的字段——而非完整对象。

**3. 外部记忆存储（External Memory Store）**
长篇输出写入外部存储（vector DB、键值存储）。
智能体通过定向查找只取所需，而非整段上下文注入。
适用于：流水线产出大型中间产物（研究报告、代码库）时。

**4. 上下文检查点（Context Checkpointing）**
在定义好的里程碑处，把此前所有状态压缩成一个检查点摘要。
检查点之后的智能体只接收检查点 + 其直接输入。
让原本会超出任何上下文窗口的流水线得以运行。

## 上下文划分规则
- 每个智能体的 system prompt 必须精确说明它读什么、写什么
- 智能体绝不应接收另一个智能体的完整 system prompt
- 敏感数据（PII、凭证）必须显式排除在智能体间状态之外
- 定义上下文归属模型：谁可以覆写哪些字段

---
