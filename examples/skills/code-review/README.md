# code-review 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

代码写完准备合入前，进行全面审查。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `review 一下 main 分支相对 develop 的改动` |
| agent | 加载 `skills/code-review/SKILL.md`，执行：

1. 确定审查范围：git log develop..main --oneline
2. 并行两个子代理：Standards 轴 + Spec 轴
3. 输出分级报告（Critical / Required / Optional / Nit） |

## 产出

分级审查报告（附代码片段和修复建议）

## 验证

所有 Critical 已修复；Required 有明确修复路径

## 资产位置

- 定义：`skills/code-review/SKILL.md`
- 元数据：`skills/code-review/manifest.yaml`
