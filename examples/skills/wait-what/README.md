# wait-what 使用示例

**类别**：其他 | **版本**：1.0.0

## 场景

用户说没看懂上一条消息。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `等一下，你在说什么` |
| agent | 加载 `skills/wait-what/SKILL.md`：

1. 用 ASD-STE100 简化英语重讲
2. 补上下文
3. 引用 GLOSSARY.md 里的术语 |

## 产出

简化后的解释，引用 GLOSSARY.md

## 验证

用户说看懂了

## 资产位置

- 定义：`skills/wait-what/SKILL.md`
- 元数据：`skills/wait-what/manifest.yaml`
