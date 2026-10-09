# deep-research-crew 使用示例

**类别**：调研与信息检索 | **版本**：1.0.0
**成员数**：7 | **主理人**：`deep-research-crew-team-lead`

## 场景

需要深度研究并产出带源报告。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我研究一下 LLM 的微调方案` |
| agent | 选择专家团 "深度研究专家团"（`deep-research-crew`）：

七角色流水线：
1. 导航 -> 2. 清洗 -> 3. 解构 -> 4. 归档 -> 5. 溯源 -> 6. 审核 -> 7. 写作

产出：带源报告 |

## 产出

带来源标注的研究报告

## 验证

每条论断有出处；来源可验证

## 资产位置

- 定义：`teams/deep-research-crew/settings.json` + `agents/*.md`（7 名成员）
- 元数据：`teams/deep-research-crew/manifest.yaml`
