# research 使用示例

**类别**：调研与信息检索 | **版本**：1.0.0

## 场景

需要调研一个问题，产出带来源标注的结论。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `研究一下微信小程序音频支持的格式` |
| agent | 加载 `skills/research/SKILL.md`，执行：

1. 搜索官方文档、社区讨论、测试数据
2. 整理结论到 docs/wechat-audio-formats.md
3. 每条论断标注来源 |

## 产出

带来源标注的 Markdown 研究报告

## 验证

每条结论有至少一个来源；来源可验证

## 资产位置

- 定义：`skills/research/SKILL.md`
- 元数据：`skills/research/manifest.yaml`
