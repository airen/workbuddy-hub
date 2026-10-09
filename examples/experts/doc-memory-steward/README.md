# doc-memory-steward 使用示例

**类别**：开发与工程 | **版本**：1.0.0
**编排技能**：agent-doc-memory

## 场景

项目知识散落各处，需要建立文档记忆。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我建一个项目知识库` |
| agent | 选择专家 "纪文远"（`doc-memory-steward`），编排 `agent-doc-memory` 技能：

1. 扫描现有文档
2. 创建 INDEX.md
3. 创建 GLOSSARY.md
4. 审计孤儿文档和断链

产出：文档工作区 |

## 产出

文档工作区（INDEX.md, GLOSSARY.md 等）

## 验证

新 agent 能查 INDEX 快速理解项目

## 资产位置

- 定义：`experts/doc-memory-steward/.codebuddy-plugin/plugin.json`
- 人格：`experts/doc-memory-steward/agents/doc-memory-steward.md`
- 元数据：`experts/doc-memory-steward/manifest.yaml`
