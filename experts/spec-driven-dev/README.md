# 章立言 · 规格驱动开发教练

把模糊需求固化成可执行规格，再让 AI 动手写代码 —— 方法论来自 GitHub Spec Kit。

## 类型

Agent 型（单个 AI 专家）

## 它解决什么问题

给 AI 一段模糊提示词，它会信心十足地写 3000 行代码，然后做错一半方向；接着开始"修 bug"，越修越乱，最后推倒重来。

**那不是 AI 的问题，是流程的问题。** 这个专家做的事只有一件：**在动手写代码之前，把结构立起来。**

> 代码服务规格，不是规格服务代码。

## 功能

### 三条独立入口

| 入口 | 什么时候用 | 产出 |
|---|---|---|
| **SDD（九步）** | 建功能 / 建应用 | 规格 → 方案 → 任务 → 实现 → 收敛 |
| **Bug 修复** | 修一个坏掉的行为 | 诊断 → 限定范围修复 → 验证（`verified`/`partial`/`failed`） |
| **想法评估** | 判断一个想法值不值得投入 | `go` / `needs-clarification` / `kill` |

### SDD 九步主线

```
constitution → specify → clarify → plan → checklist → tasks → analyze → implement → converge
```

- **constitution**（每项目一次）：立工程原则，作为后面每一关的尺子
- **specify**：写规格，聚焦 WHAT/WHY，绝不写技术栈
- **clarify**：一次最多问 5 个针对性问题，答案回写规格
- **plan**：技术方案、数据模型、接口契约、章程合规关卡
- **checklist**：生成"需求的单元测试"
- **tasks**：拆成有依赖顺序、可并行、可追溯的任务清单
- **analyze**：只读地交叉检查 spec/plan/tasks，报告冲突与缺口
- **implement**：按阶段执行（大功能分阶段跑）
- **converge**：验证实现是否真的满足规格，只追加任务，绝不改代码

### 产物落盘结构

```
.specify/
├── memory/constitution.md
├── templates/
├── bugs/<slug>/
└── assessments/<slug>/
specs/NNN-feature-slug/
├── spec.md · plan.md · tasks.md · research.md · data-model.md · quickstart.md
├── checklists/requirements.md
└── contracts/
```

## 使用示例

- 我有个想法，先别写代码，帮我把规格立起来
- 给这个项目立一份开发章程，约束后面所有实现
- 检查我的规格、方案和任务清单是否一致，把漏洞找出来

## 附带能力

- **内置方法论知识库**（`skills/spec-driven-development/`）：12 份参考文档 + 5 套官方模板 + 脚手架脚本
- **脚手架脚本**：`scripts/scaffold.sh init|feature|bug|assess <项目根> [slug]`，自动铺目录、取下一个三位编号、拷模板

## 头像

头像已自动生成在 `avatars/` 目录下。如需替换为自定义头像，要求：
- 格式：PNG（推荐）或 JPG
- 尺寸：512×512 px
- 大小：单张不超过 500KB

## 来源与许可

方法论、命令语义与模板改写自 [github/spec-kit](https://github.com/github/spec-kit)（MIT License），详见 `skills/spec-driven-development/references/UPSTREAM-LICENSE.md`。

## 安装

将专家包目录放到专家目录下：

```
/Users/damo/.workbuddy-ai/plugins/marketplaces/my-experts/plugins/spec-driven-dev/
```

然后运行注册命令使其可见：

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 打包分享

```bash
zip -r spec-driven-dev.zip spec-driven-dev/
```
