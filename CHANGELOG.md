# Changelog

本文件记录 workbuddy-hub 项目级变更（资产层面变更请在各资产内或 PR 中说明）。

## [unreleased]

### 2026-10-12 — life-assistant 版本递增至 1.0.1（平台重提要求）
- 平台在**驳回后仍记录版本号**，重提同版本会被拦：「解析失败：包内版本号 "1.0.0" 必须大于当前最新版本 "1.0.0"」。
- 递增 `experts/life-assistant` 的 `plugin.json` 与 `manifest.yaml` 至 `1.0.1`，重跑 `build_registry.py`
  同步 `registry/experts.yaml`，重新打包 `build/life-assistant.zip`（71 KB）。
- 校验：`validate.py` 65/65；`verify_upload_ready.py` 通过；解包 `preflight.py` **33 PASS / 1 WARN / 0 FAIL**。
- 上传页注意：该包被驳回的**服务类目**原因是「至少应包含『工具>信息查询』类目」，须在服务类目里勾
  **工具 → 信息查询**。已补进 `docs/platform-submission.md` 报错对照表。
- 已知 WARN：包内无 `LICENSE` 文件（而 README 声明 MIT），preflight 判为非阻塞。

### 2026-10-10 — 新增「内容工厂专家团」（content-creation-team）
- 新增 Team 型专家团 `teams/content-creation-team`：主理人（内容总控）+ 8 位环节专家，覆盖
  素材采集 → 灵感库 → 选题策略 → 内容日历 → 内容创作 → 多平台改编 → 审核发布 → 数据复盘 → 内容复用 的完整闭环。
- 附带技能 `content-factory-playbook`（含 workflow / 灵感库字段模板 / 发布前检查清单 / 指标复盘清单）。
- 分类 `06-ContentCreative`；已登记 `registry/teams.yaml` 并同步至「我的专家」。
- 头像暂用仓库默认占位图（未消耗生成积分），正式上架前可替换。
- **撞名与最终改名**：open.workbuddy.cn 分别拒绝 `content-factory`、`content-factory-team`、`content-production-team`（均提示专家名称已被占用）；经用户选择，当前 ID 改为 **`content-creation-team`**，中文展示名仍为「内容工厂专家团」。平台错误未透露占用者或提供可查的全局名称目录，因此无法判定具体是谁/哪个包先占用；这些 slug 都是较通用的英文描述词组合。
- 最终 ID 已一致应用于目录、agent/头像文件名、plugin.json（`name`/`plugin`/`agentName`/`agents[]`/`teamInfo`/`members[]`）、各 agent MD frontmatter、`settings.json`、`manifest.yaml` 与 registry；主理人为 `content-creation-team-team-lead`。技能包名 `content-factory-playbook` 有意保留。
- **本地上架校验**：`verify_upload_ready.py teams/content-creation-team` → 0 失败 0 提示；zip 第一层即 `content-creation-team/`，约 2.7 MB。全局唯一性只能由平台上传校验确认，当前 ID 尚未收到平台占用报错，不代表已获得平台预留。
- **同步完整性**：插件市场目录、白名单、recents、marketplace index 均已同步；另预建版本化缓存 `cache/my-experts/content-creation-team/1.0.0/` 并登记 `installed_plugins.json`。旧 ID `content-production-team` 的市场目录/缓存/白名单/recents/installed_plugins/zip 均清理。

### 2026-10-11 — 新增两个 AI 专家（健康 / 教培）
- 新增 Agent 型专家 `experts/ai-health-copilot`（康衡，AI 健康方案顾问，分类 `12-IndustryConsultant`）：基于 5 个开源项目（ai-health / posture-sentinel / open-health-agent / health-coach / OpenClaw-Medical-Skills）做久坐、饮食、健康记录、医疗 Agent 的选型与部署核对。内置技能 `health-stack-selector`（选型路由 + 部署核对）与 `health-boundary-check`（诊断 / 估算 / 证据 / 隐私边界闸）。
- 新增 Agent 型专家 `experts/ai-teaching-copilot`（喻衡，AI 教学设计顾问，分类 `15-Education`）：基于 6 个开源项目（QuizWeaver / anything-to-course / Agentic-AI-Tutor / studyforge / freelingo / lextures）做备课出题、答疑、复习、语言练习、教务的选型与核对。内置技能 `teaching-stack-selector` 与 `item-and-answer-qa`（题目 / 答案教学适配核）。
- 已登记 `registry/experts.yaml`，`verify_upload_ready.py` 两包均 0 失败 0 提示；`validate.py` 全仓 54/54 通过。
- 已通过 `sync_my_experts.py` 同步至「我的专家」：市场目录、白名单、recents、marketplace index 各 +2，插件缓存无需刷新。
- 安全与合规审计（双人审查）：无 Critical / 无 High 阻塞项；已修 HIGH/Medium/Low 共 8 项 —— 补「外部内容只当数据、不当指令」边界、health-coach 隐私口径与数据流向表对齐、health-coach/OHA 安装脚本审阅（去 `-y`、先 `cat`）、OHA `db:push` 备份提醒、下游产出过 boundary-check 闸、lextures 删课幂等提醒、证据分级 A/B/C/D 非临床授权、curl|bash 直接拒绝、Docker 端口绑 127.0.0.1、GLP-1 处方药不给剂量、Agentic-AI-Tutor 许可证（Academic）/模型（Gemini 2.5 Flash Lite → LoRA Qwen2.5-1.5B）经仓库 README 核实无误。
- 头像用仓库默认占位图（未消耗生成积分），正式上架前可替换。
- 全局唯一性只能由平台上传校验确认；当前 ID 尚未收到占用报错，不代表已获平台预留。

### 2026-10-11 — 新增 AI 投研专家（ai-invest-research-copilot / 研衡）
- 新增 Agent 型专家 `experts/ai-invest-research-copilot`（研衡，AI 投研顾问，分类 `04-DataAI` / 调研与信息检索）：基于 5 个开源项目做投研环节选型与核对 —— Mira（整理投资逻辑，Apache-2.0）、Jiangge89/trading-agent（查财报 + 模拟交易，MIT，需 OPENAI+DEEPSEEK key 与 Docker，仅 $100K 模拟、下单前 `interrupt()` 人工确认）、AI4Finance/FinRL-Trading（量化回测流水线，Apache-2.0，回测默认计交易成本）、terence-lim/quant-agents（因子研究，MCP+Pydantic-AI，数据依赖 CRSP/Compustat 机构库，⚠️ 授权未声明）、waylandzhang/ai-quant-book（系统知识书，⚠️ CC BY-NC-SA 4.0 非商用）。
- 内置技能 `invest-stack-selector`（任务→工具路由 + 部署/数据/授权核对清单）与 `invest-boundary-check`（投研合规闸：剔除买卖指令、标注回测为历史、附证据与更新条件、披露数据来源与 License、确认无自动交易）。
- 已登记 `registry/experts.yaml` 并 `build_registry.py` 重生索引（research 分类 5→6）；`validate.py` 全仓 55/55 通过；`verify_upload_ready.py` 0 失败 0 提示。
- 已通过 `sync_my_experts.py` 同步至「我的专家」：市场目录、白名单、recents、marketplace index 各 +1。
- 安全与合规边界：外部内容只当数据不当指令（curl|bash 直接拒绝、技能安装去 `-y` 先 `cat`）；不构成投资建议、不替用户做买卖决策；任何下单只走模拟盘且需人工确认，绝不允许真实资金；回测不代表未来收益；License 差异明示（CC BY-NC-SA 非商用、quant-agents 授权待确认）。
- 头像用仓库默认占位图（未消耗生成积分），正式上架前可替换。
- 全局唯一性只能由平台上传校验确认；当前 ID 尚未收到占用报错，不代表已获平台预留。

### 2026-10-11 — 新增 AI 教学落地专家（ai-edu-practice-copilot / 践衡）
- 新增 Agent 型专家 `experts/ai-edu-practice-copilot`（践衡，AI 教学落地顾问，分类 `15-Education`）：针对「想把 AI 用进教学，却卡在明天这节课怎么用」，基于 6 个开源项目做选型与前置/合规核对 —— bobqiu/ai-edu-for-kids（小学到初中 AI 通识课程 + 伦理安全模块，⚠️ CC BY-NC-SA 4.0 非商用）、FW1201/tw-edu-skills（35 个 K-12 教师技能，课程设计/命题/教材，默认台湾 108 课纲需按地区适配，⚠️ 授权未明）、lixianglaoshi/lx-skill（学习教练：提问/分级提示/复述 + 互动教学网页生成，混合授权 MIT + Apache-2.0）、MatrixDriver/aixue（初高中上传题目→解题思路 + 答题弱项分析，全栈 FastAPI+Next.js，需 OpenRouter key，⚠️ 授权未声明）、FW1201/tw-ai-literacy-4d（委托/描述/辨识/尽责 4D 框架 + 60 教学提示词，声明非官方）、Vinceli-9527/EduDaily（聚合教育信息源生成日报，多平台适配，本地 RAG，需 DeepSeek key）。
- 内置技能 `edu-stack-selector`（教学任务→工具路由 + 逐项核对运行时/key/课纲适配/授权边界，输出可粘贴落地清单）与 `edu-boundary-check`（教学合规闸：不替代教师决策、不替学生写答案、课纲地区适配、学生隐私与数据流向、License 差异、非官方声明）。
- 已 `build_registry.py` 重生索引（专家 17）；`validate.py` 全仓 56/56 通过；`verify_upload_ready.py` 0 失败 0 提示；打包 `build/ai-edu-practice-copilot.zip` 约 269 KB（第一层即资产目录）。
- 已通过 `sync_my_experts.py` 同步至「我的专家」：白名单 23→24、recents、marketplace index 各 +1。
- 双人审查（结构 + 安全合规）：结构审计 PASS；安全审计 0 Critical / 0 High，2 Medium + 3 Low 已修 —— M1 README 增「分发边界」声明（仅原创简介与链接、不重新分发上游素材；上架收费须与 ai-edu-for-kids 的 CC BY-NC-SA 4.0 非商用条款兼容）、M2 aixue 学生 PII 经 OpenRouter 第三方 LLM 升级为「监护人/学校同意 + DPA + 授权未声明」高警示、L1 EduDaily 自动脱敏补「逐条人工核验」提示、L2 安装脚本预检具体化（先打开脚本核对 curl/wget/提权，绝不管道远程脚本）。
- 头像用仓库默认占位图（未消耗生成积分），正式上架前可替换。
- 全局唯一性只能由平台上传校验确认；当前 ID 尚未收到占用报错，不代表已获平台预留。

### 2026-10-11 — 新增播客改稿专家（podcast-to-article / 陈听）
- 新增 Agent 型专家 `experts/podcast-to-article`（陈听，播客改稿主编，分类 `06-ContentCreative`）：把 YouTube / 小宇宙单集链接或逐字稿整理成中文精华长文 —— 保留关键原声并按读者问题重组，先出第一正文章节配图、确认后逐章配图，用户说「存入 Obsidian」时把成稿与已接受配图导出到本机仓库。
- 上游：sunkeke-ai/keke-podcast-to-article（MIT）。内置技能 `keke-podcast-to-article`，`SKILL.md` / `references/`（editorial-examples、source-input-workflow、punk-illustration-workflow、obsidian-export）/ `scripts/save_to_obsidian.py` **逐字保留**；唯一改动是给 `SKILL.md` frontmatter 追加平台必需的 `display_name` / `display_name_en` / `category` / `version` 四个字段，正文零改动。
- 三个人工确认点：G1 文字稿可靠且覆盖范围明确（不得凭简介编造访谈）、G2 首图确认（未获明确确认不生成其余章节）、G3 保存授权（未授权不写 Obsidian）。
- 已登记 `registry/experts.yaml`；`build_registry.py` 重生索引（专家 23→24、content 12→13）；`validate.py` 全仓 64/64 通过；`verify_upload_ready.py` 0 失败 0 提示；`preflight.py`（Agent 型 34 项）34 PASS / 0 WARN / 0 FAIL。
- 打包 `build/podcast-to-article.zip` 334 KB（第一层即资产目录，14 个文件）；附 `build/上架指引_播客改稿主编陈听.md`。
- 已通过 `sync_my_experts.py` 同步至「我的专家」：市场目录、白名单、recents、marketplace index 各 +1；版本化缓存无需刷新（app 侧首次安装后生成）。
- 头像用图像生成能力生成（1024×1024 → 512×512 JPEG，96 KB，背景取 `06-ContentCreative` 的 pink-magenta）；第一版把名字画成「陈婷」，重生成后确认为「陈听」。
- 全局唯一性只能由平台上传校验确认；当前 ID 尚未收到占用报错，不代表已获平台预留。

### 2026-10-09 — 仓库初始化与结构重构
- 按 `资产定义层 + 组合层 + 管理工具层` 思路建立 workbuddy-hub 骨架：
  `skills/`、`experts/`、`teams/`、`registry/`、`schemas/`、`templates/`、`scripts/`、`tests/`、`docs/`、`examples/`、`archive/`、`.github/`。
- 迁移核心自研资产：
  - 专家（8）：lao-dao-editor、agent-memory-advisor、engineering-review-board、self-media-studio、spec-driven-dev、diagram-architect、doc-memory-steward、software-architect
  - 专家团（3）：engineering-delivery、deep-research-crew、hai-stack
  - 技能（4）：de-ai-rewrite、agent-doc-memory、ai-project-pilot、ui-design-field-manual
- 编写管理工具：`import_asset.py`、`sync_manifests.py`、`build_registry.py`、`validate.py`，及 `schemas/*.json`。
- 归档非核心/第三方资产（mattpocock-skills、creator-ops、media-content-team 等）至 `archive/`，不进入 registry。
- 上架指引与安装报告归入 `docs/operations/`。
