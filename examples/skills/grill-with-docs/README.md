# grill-with-docs 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

拷问的同时想留下文档。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `拷问我并顺便把文档写了` |
| agent | 加载 `skills/grill-with-docs/SKILL.md`，边拷问边生成：
- ADR 文件
- 术语表片段（更新 GLOSSARY.md） |

## 产出

ADR 文件 + 更新的 GLOSSARY.md

## 验证

每个关键决策都有 ADR；术语表无歧义

## 资产位置

- 定义：`skills/grill-with-docs/SKILL.md`
- 元数据：`skills/grill-with-docs/manifest.yaml`
