# codebase-design 使用示例

**类别**：开发与工程 | **版本**：1.0.0

## 场景

想深化模块设计，提升可测试性。

## 对话片段

| 说话者 | 内容 |
|---|---|
| 用户 | `帮我 deepen 这个模块` |
| agent | 加载 `skills/codebase-design/SKILL.md`：

1. 扫描代码，识别浅模块
2. 输出深化建议（模块边界、接口设计、接缝）
3. 可视化报告（HTML） |

## 产出

深化建议 + 可视化 HTML 报告

## 验证

建议可执行；接口设计提升可测试性

## 资产位置

- 定义：`skills/codebase-design/SKILL.md`
- 元数据：`skills/codebase-design/manifest.yaml`
