# handoff 使用示例

**类别**：其他 | **版本**：1.0.0

## 场景

会话即将结束或上下文快满时，把进度交给下个 agent。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `交接一下，下个会话继续实现导出功能` |
| agent | 加载 `skills/handoff/SKILL.md`，生成交接文档：

```markdown
# Handoff: 导出功能

## 上下文
- 已完成：Cart 模型
- 待办：export_to_csv()

## 建议加载的技能
- skills/implement/SKILL.md
```

保存到临时目录（不进工作区） |

## 产出

Markdown 交接文档（含上下文、待办、建议技能）

## 验证

文档在临时目录，新 agent 读完能直接接手

## 资产位置

- 定义：`skills/handoff/SKILL.md`
- 元数据：`skills/handoff/manifest.yaml`
