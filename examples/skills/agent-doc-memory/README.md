# agent-doc-memory 使用示例

**类别**：其他 | **版本**：1.0.0

## 场景

项目文档散乱，agent 记不住上下文。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我建一个文档记忆工作区` |
| agent | 加载 `skills/agent-doc-memory/SKILL.md`：

1. 扫描现有文档
2. 创建 INDEX.md 索引
3. 创建 GLOSSARY.md 术语表
4. 审计孤儿文档和断链 |

## 产出

文档工作区（INDEX.md, GLOSSARY.md, ADR/, specs/ 等）

## 验证

新 agent 进入后能查 INDEX.md 快速理解项目

## 资产位置

- 定义：`skills/agent-doc-memory/SKILL.md`
- 元数据：`skills/agent-doc-memory/manifest.yaml`
