# ask-matt 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

不知道下一步该用什么技能。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `我现在该干嘛？` |
| agent | 加载 `skills/ask-matt/SKILL.md`，根据当前处境推荐：
- 想法模糊 -> idea-refine
- 需求已清 -> to-spec
- 代码有问题 -> diagnosing-bugs
- ...（按路由表） |

## 产出

推荐的下一步行动和技能

## 验证

推荐与当前处境匹配

## 资产位置

- 定义：`skills/ask-matt/SKILL.md`
- 元数据：`skills/ask-matt/manifest.yaml`
