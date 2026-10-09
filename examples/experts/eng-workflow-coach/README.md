# eng-workflow-coach 使用示例

**类别**：开发与工程 | **版本**：1.0.0
**编排技能**：ask-matt, setup-matt-pocock-skills, to-spec, to-tickets, implement, implement-spec, wayfinder, triage, tdd, diagnosing-bugs, code-review, codebase-design, domain-modeling, prototype, research, retro, pr, wizard, improve-codebase-architecture, grilling, grill-me, grill-with-docs, handoff, teach, to-questionnaire, wait-what, writing-for-agents, port-agent-skills

## 场景

需要全流程工程指导。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `我要从零做这个功能` |
| agent | 选择专家 "工程流程教练"（`eng-workflow-coach`）：

编排 29 个技能，按场景路由：
- 想法模糊 -> idea-refine
- 需求已清 -> to-spec -> to-tickets -> implement
- 卡住了 -> grilling 拷问到底
- 交付前 -> code-review

产出：完整交付物 |

## 产出

从规格到代码的完整交付

## 验证

全流程覆盖；质量门禁通过

## 资产位置

- 定义：`experts/eng-workflow-coach/.codebuddy-plugin/plugin.json`
- 人格：`experts/eng-workflow-coach/agents/eng-workflow-coach.md`
- 元数据：`experts/eng-workflow-coach/manifest.yaml`
