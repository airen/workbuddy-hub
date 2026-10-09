# port-agent-skills 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

要把外部 skill 仓库转成 WorkBuddy 格式。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `把这个 Claude Code skill 仓库转成 WorkBuddy 格式` |
| agent | 加载 `skills/port-agent-skills/SKILL.md`：

1. 侦察上游仓库结构
2. 按转换规范批量转换 SKILL.md
3. 校验引用完整性
4. 安装到 skills/ 目录 |

## 产出

转换后的 WorkBuddy skill 包 + 校验报告

## 验证

validate.py 零错误；引用无断链

## 资产位置

- 定义：`skills/port-agent-skills/SKILL.md`
- 元数据：`skills/port-agent-skills/manifest.yaml`
