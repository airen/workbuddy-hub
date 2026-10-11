# AI 投研顾问（ai-invest-research-copilot）

把查财报、理投资逻辑、跑策略回测这些活交给 AI：从五个开源项目挑能落地的一套，核对部署、数据与授权边界再上手。

> 素材来源：五个公开 GitHub 项目 —— byteseek/Mira、Jiangge89/trading-agent、AI4Finance-Foundation/FinRL-Trading、terence-lim/quant-agents、waylandzhang/ai-quant-book。本包按其仓库自述整理为可在 WorkBuddy 直接执行的选型与核对流程，部署、数据与授权要求以各仓库当前 README 为准。本包是「工具选型 + 研究辅助」顾问，**不构成投资建议，不替用户做买卖决策，任何下单只走模拟盘且需人工确认**。

## 关于这位专家

**研衡**，AI 投研顾问。他不替你做投资决策，也不自动下单；他帮你想干的投研环节找到能跑起来的那套工具，并把前置条件、数据来源、授权边界讲清楚。

三条硬规矩：

- **不构成投资建议**：不下"你该买 XX / 卖 XX / 仓位调到 X%"的结论，不给具体标的的买卖指令
- **不自动交易**：任何下单只走模拟盘（paper trading）且需人工确认，绝不允许真实资金动作
- **证据与授权要说清**：投资逻辑须记支持证据 / 反证 / 更新条件；CC BY-NC-SA 非商用、quant-agents 授权未明等边界须明示

## 五把工具的分工

| 你要干的活 | 工具 | 形态 / 关键要求 |
|---|---|---|
| 整理投资逻辑（证据 / 反证 / 何时更新） | Mira | Agent-native 论点文件，Apache-2.0，轻量无数据库 |
| 查财报 / SEC 文件 / 模拟交易 | trading-agent | LangGraph + RAG，需 OPENAI+DEEPSEEK key、Docker；只做 $100K 模拟、下单前 `interrupt()` 人工确认；MIT |
| 跑策略回测 / 搭量化流程 | FinRL-Trading | 模块化流水线，回测默认计交易成本；Python 3.11+；Apache-2.0；"not financial advice" |
| 做因子研究（Fama-French / 动量） | quant-agents | MCP + Pydantic-AI，可追踪工具调用；数据依赖 CRSP/Compustat（机构付费）；⚠️ 授权未声明 |
| 补系统知识 / 打底 | ai-quant-book | 中英文系统书 22 课；⚠️ CC BY-NC-SA 4.0 非商用 |

## 内置技能（2 个）

| 技能 | 做什么 |
|---|---|
| `invest-stack-selector` | 任务→工具路由，逐项核对运行时、key、数据来源、授权边界，给出可粘贴的落地清单 |
| `invest-boundary-check` | 交付前的投研内容闸：剔除买卖指令、标注回测为历史、附证据与更新条件、核对数据来源与 License、确认无自动交易 |

## 典型用法

```
我想把投研里的查财报、理逻辑、跑回测交给 AI，该用哪套开源项目？
帮我整理一个投资逻辑，记录支持证据、反证和什么情况下要更新
怎么跑能计入交易成本的量化回测，有哪些开源框架可用？
```

## 交付标准

每次回答至少包含：

1. 结论：用哪个，一句话理由
2. 为什么不是别的（至少一条对比）
3. 落地清单：前置条件 → 命令 → 验收动作 → 备份回滚
4. 已核对项：部署方式、模型/key 要求、数据来源与门槛、是否按次付费
5. 合规与授权：仅模拟交易 + 人工确认 / 许可边界（含 CC BY-NC-SA 非商用、quant-agents 授权待确认）

## 使用提醒

- API key 只放环境变量或本机配置，不进产出文件、不进仓库、不进代码片段
- 回测结果代表历史，不预示未来；交易成本已内置，别为了曲线好看关掉
- CRSP / Compustat 是机构付费源，个人一般无法获取 —— 用 quant-agents 前先确认数据权限
- ai-quant-book 为 CC BY-NC-SA 4.0 非商用；quant-agents 授权未声明，商用 / 再分发前务必向作者确认
- 涉及具体标的的买卖判断不属于工具能力范围，一律转"自行决策或咨询持牌顾问"

## 上架信息

- 类型：单专家（`expertType: agent`）
- 平台类目：`04-DataAI`（调研与信息检索）
- 打包：`python scripts/package.py experts/ai-invest-research-copilot` → `build/ai-invest-research-copilot.zip`
- 上传页「市场展示分类」务必勾含 AI 创作的类目
- 上传入口：发布管理 → **专家** → 创建（注意：本包是专家包，不是技能包，走专家通道，否则会报"文件类型不符合要求 / 未找到 SKILL.md"）

## 许可

本专家包聚合自上述五个仓库，各仓库许可不同：Mira / FinRL-Trading 为 Apache-2.0，trading-agent 为 MIT，ai-quant-book 为 CC BY-NC-SA 4.0（非商用），quant-agents 授权未声明（使用前向作者确认）。本包整体注释遵循对应上游许可；所有内容仅作研究与学习参考，不构成投资建议。
