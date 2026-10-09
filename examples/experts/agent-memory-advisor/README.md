# agent-memory-advisor 使用示例

**类别**：开发与工程 | **版本**：1.0.0
**编排技能**：无内嵌技能

## 场景

要选型智能体记忆方案。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我选一个记忆架构` |
| agent | 选择专家 "智能体记忆选型顾问"（`agent-memory-advisor`）：

1. 按场景分类（写代码/个人智能体/公司大脑）
2. 对比 10 个开源记忆项目
3. 挑出能落地的一套
4. 诊断记忆断环

产出：选型报告 + 断环诊断 |

## 产出

选型报告（推荐方案 + 理由）+ 断环诊断

## 验证

方案与场景匹配；断环有修复建议

## 资产位置

- 定义：`experts/agent-memory-advisor/.codebuddy-plugin/plugin.json`
- 人格：`experts/agent-memory-advisor/agents/agent-memory-advisor.md`
- 元数据：`experts/agent-memory-advisor/manifest.yaml`
