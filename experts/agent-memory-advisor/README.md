# 智能体记忆选型顾问 (Agent Memory Advisor)

把开源圈卷起来的"智能体记忆"方案，按场景翻译成能落地的选型建议。诊断记忆断环，给出最小验证路径，而不是让你一口气全装。

## 类型

Agent 型（单个 AI 专家）

## 核心能力

- **记忆断环诊断**：用「体验 → 记住 → 连接 → 检索 → 行动 → 更新」六环模型定位失忆根因。
- **场景化选型**：按写代码 / 个人智能体 / 公司大脑三类场景挑推荐组合。
- **项目解读与对比**：10 个开源项目分 4 类，讲清角色、定位、取舍。

## 项目速览（10 个，4 类）

| 分类 | 项目 |
|------|------|
| 先让它记得住 | Mem0、Hindsight、memU |
| 再把记忆变成知识 | Cognee、Graphiti、OpenViking |
| 让智能体有状态 | Letta、Letta Code |
| 跨整个技术栈都记得住 | OpenMemory、Agent Memory Benchmark |

## 场景推荐链路

- 写代码：`Hindsight → Cognee → Letta Code`
- 个人智能体：`Mem0 → Graphiti → Letta`
- 公司大脑：`Cognee → Graphiti → Hindsight`

## 使用示例

- 我要给自己的 AI 智能体加记忆，帮我按场景选一套开源方案
- 我的智能体总忘事，帮我诊断是哪个环节断了
- 对比一下 Mem0、Graphiti 和 Cognee 各自适合什么

## 头像

头像已自动生成在 `avatars/` 目录下。如需替换为自定义头像，要求：
- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 安装 / 注册

专家包已位于专家目录：

```
/Users/damo/.workbuddy/plugins/marketplaces/my-experts/plugins/agent-memory-advisor/
```

注册使其出现在 WorkBuddy 专家中心：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
zip -r agent-memory-advisor.zip agent-memory-advisor/
```
