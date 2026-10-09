# lao-dao-editor 使用示例

**类别**：调研与信息检索 | **版本**：1.0.1
**编排技能**：de-ai-rewrite

## 场景

有 AI 腔文稿需要改写。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `去 AI 味：在当今数字化转型的时代背景下...` |
| agent | 选择专家 "老刀"（`lao-dao-editor`），内部编排 `de-ai-rewrite` 技能：

**第一遍：删除 AI 模式**
- 删"在当今...时代背景下"
- 删"具有至关重要的意义"

**第二遍：注入真实人声**
- 加具体细节和时间
- 加人的反应

**第三遍：校对**
- 确认原意保留
- 确认检测工具看不出 AI 痕迹

产出：自然文本版本 |

## 产出

改写后的自然文本

## 验证

无 AI 套话；事实信息完整；读起来像人写的

## 资产位置

- 定义：`experts/lao-dao-editor/.codebuddy-plugin/plugin.json`
- 人格：`experts/lao-dao-editor/agents/lao-dao-editor.md`
- 元数据：`experts/lao-dao-editor/manifest.yaml`
