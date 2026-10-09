# 示例：用「老刀」专家改写 AI 腔文稿

**引用资产**：`experts/lao-dao-editor`（智能体专家，research 类）

## 触发方式

用户在 WorkBuddy 中选择专家「老刀」（`lao-dao-editor`），或对会话说：

- 「去 AI 味」「降 AI 检测率」「人味改写」
- 「这段文字像机器写的，润色自然一点」

## 输入 / 输出

- **输入**：一段带 AI 腔的文稿（机械排比、套话、过度工整的句式）
- **输出**：按资深编辑标准三遍打磨后的自然文本，并标注删改了哪些 AI 腔模式

## 过程

专家内部编排其技能 `de-ai-rewrite`（`skills/de-ai-rewrite`）：

1. 扫描并删除 AI 腔模式（万能开头、无意义转折、同义堆叠）
2. 注入真实人声：具体细节、口语节奏、必要的重复与停顿
3. 第三遍整体校对，确认「像人写的」且原意不丢

## 验证

- 改写后没有「在当今时代」「总而言之」「不仅……而且……」等套话
- 原文的事实性信息（数字、专有名词、结论）逐条保留

## 资产路径

- 专家定义：`experts/lao-dao-editor/.codebuddy-plugin/plugin.json`
- 角色人格：`experts/lao-dao-editor/agents/lao-dao-editor.md`
- 实际干活的是技能：`skills/de-ai-rewrite/`
- 元数据：`experts/lao-dao-editor/manifest.yaml`
