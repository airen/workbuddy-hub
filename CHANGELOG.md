# Changelog

本文件记录 workbuddy-hub 项目级变更（资产层面变更请在各资产内或 PR 中说明）。

## [unreleased]

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
