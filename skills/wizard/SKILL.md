---
name: wizard
display_name: "交互式向导"
display_name_en: "Wizard"
description: "该技能生成一个交互式 bash 向导（wizard），一步一步带一个人走完只有他们本人才能做的步骤：打开每个 URL、精确说明点哪里复制什么、捕获值、写到该去的地方（.env、GitHub secrets），并逐阶段确认。适用于「给我写个向导」「带我配置一下」「走一遍开通流程」「配一下 CI secrets」「跑一次性的迁移/切换」「有个第三方后台要人手动点」这类需求。agent 自己能做的步骤不要用它。"
description_zh: "生成 bash 向导，一步一步带人走完只有人才能做的步骤"
description_en: "Generate an interactive bash wizard for steps only a human can perform."
category: development-tools
version: 1.0.0
author: "大漠"
agent_created: true
---

# 向导（wizard）

**向导（wizard）**是一个 bash 脚本，它一步一步带着一个人走完一段手工流程——这段流程手做起来很烦，每次重新讲给 AI 听也很烦。它会打开每一个 URL，精确说明点哪里、复制什么，把值捕获下来，写到它们该待的地方（`.env`、GitHub secrets），每个阶段都做一次确认，并显示还剩几个阶段。它可能用来配置第三方服务、跑一次性的迁移，或者把项目从一种状态搬到另一种状态。

那套好用的 UX 已经由 [template.sh](scripts/template.sh) 解决了：逐阶段的进度、确认闸门、跨平台打开 URL（含 WSL）、隐藏式密钥输入、幂等的 `.env` upsert、`gh secret`/`gh variable` 写入，以及收尾摘要。**你的工作只是界定这段流程、编写它的各个阶段。** `STAGES` 标记以上的那套库在每个向导里都一模一样；这种一致性正是重点：永远不要手工改它。

向导默认是一次性的：为一次运行而生，存到一个临时路径或 `scripts/` 路径，活儿干完就删。只有当用户想要一条可重复、应当留在仓库里的安装路径时，才提交它。

## 流程（Process）

### 1. 界定流程

把这个人必须走的每一个手工步骤、以及沿途捕获的每一个值都理清楚。先读仓库，别冷着问：

- 配置类：`.env`、`.env.example`、`.env.*`、`README`、`docker-compose*`、框架配置，以及 `.github/workflows/*`（每一个 `secrets.*` / `vars.*` 引用都是向导必须产出的一个值）。
- 迁移或状态转换类：当前状态、目标状态，以及两者之间那些不可逆的动作。

然后把按顺序排好的阶段清单、以及每个阶段产出的值给用户看，并确认：他们可以增、删或调整顺序。

**完成条件：** 每个阶段都按顺序命名好了，且对每一个捕获的值你都知道：(a) 人从哪里拿到它，(b) 它写到哪里（`.env`、一个 GitHub secret、两者都写、或者哪都不写；有些阶段是纯动作），以及 (c) 它是 secret（隐藏输入）还是 public。

### 2. 为每个阶段画出路径

对每个阶段，写出这个人会走的精确路径：打开哪个 URL、在那里做什么、值显示在哪里、它填进哪个变量，例如「Dashboard → Developers → API keys → Reveal test key → copy」。哪里你并不真的知道当前的 UI 或确切的命令，就说出来，并去问用户或查文档：绝不虚构可能并不存在的步骤。

**完成条件：** 每个阶段都能落到一个陌生人照着也能走的、具体明确的指令。

### 3. 编写向导

把 `template.sh` 复制到目标路径。把示例阶段替换成每步一个 `stage`，按依赖顺序排列。使用库里的辅助函数：`stage`、`say`/`step`、`open_url`、`ask`/`ask_secret`、`write_env`、`set_secret`/`set_var`、`pause`/`confirm`。把 `TOTAL_STAGES` 设成你写下的阶段数。

守住模板立下的标准：在问某个值之前先打开它的 URL；任何 secret 都用 `ask_secret`；每一个要持久化的值都 `write_env`；只对 CI 真正需要的值 `set_secret`；任何不可逆动作之前先 `confirm`。每个 `stage` 都会清屏，让屏幕上只剩当前这一步：把一个阶段控制在一件聚焦的任务上，免得人需要看的东西滚出屏幕。标记以上的那套库不要碰。

### 4. 验证并交接

- `bash -n <script>`；如果有 `shellcheck` 就跑一下。
- `chmod +x <script>`。
- 不要自己端到端跑它：它会打开浏览器，并且会阻塞在人的输入上。改为静态地过一遍：第 1 步里每一个值都被捕获了、并且落到了第 1 步所说的地方，且每一个 `set_secret` 的名字都精确匹配 CI 里的某个 `secrets.*` 引用。
- 告诉用户怎么运行它。如果它是一条可重复的安装路径，就提交它，并从 README 链接过去，好让下一个人直接跑脚本，而不是去问 AI。
