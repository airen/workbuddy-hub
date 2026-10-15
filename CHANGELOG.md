# Changelog

本文件记录 workbuddy-hub 项目级变更（资产层面变更请在各资产内或 PR 中说明）。

## [unreleased]

### 2026-10-15 — 新增资产市场站点（GitHub Pages 独立访问页）

- **目标**：从 `registry/*.yaml` 自动生成静态单页站点，由 GitHub Actions 部署到 GitHub Pages，
  公开地址 `https://airen.github.io/workbuddy-hub/`，任何人无需安装 WorkBuddy 即可浏览全部专家与专家团。
- **新增交付物**（全部入库）：
  - `scripts/build_site.py` — 生成器：读 registry → 压缩头像（256×256 JPEG q82）→ 服务端渲染卡片 → 写 `site/index.html`
  - `templates/site/page.html` — 单文件模板（内联 CSS/JS，零外部请求，`{{token}}` 占位）
  - `.github/workflows/pages.yml` — CI 构建 + 部署（build / deploy 双 job）
  - `tests/verify_site.py` — 站点验收自检（AC1–AC10，`--browser` 启用真实浏览器 CDP 检查）
  - `tests/test_build_site.py` — 生成器单元回归（AC11，含 9 个路径穿越攻击向量）
  - `docs/hub-site-spec.md` — 规格与验收标准（目标 / 非目标 / 字段映射 / F1–F11 / AC1–AC11 / 风险）
- **改动既有文件**：`.gitignore` 新增 `/site/`（**带前导斜杠**——裸写 `site/` 会连带忽略 `templates/site/`，
  导致 CI 缺模板）；`scripts/requirements.txt` 锁精确版本（`pyyaml==6.0.3 jsonschema==4.26.0 Pillow==12.3.0 websocket-client==1.9.2`）。
- **关键设计约束**：project site 地址含子路径 `/workbuddy-hub/`，页面内所有资源引用**必须相对路径**，
  禁止 `href="/..."` / `src="/..."`（AC4 已断言）。卡片由 Python 服务端渲染（非 JS），
  禁用 JS 仍可浏览全部资产，兼顾 SEO/GEO。产物按 `(分类序, 类型序, id)` 排序，保证幂等逐字节一致（AC10）。
- **四路并行审查**（五轴代码审查 / 安全审计 / 测试覆盖 / 性能审计）后修复：
  - **安全**：F1 路径穿越（HIGH，`id`/`path` 拼进文件系统路径 → 加白名单正则 + `is_relative_to` 归属断言 + `prepare_avatars` 第二道防线）；
    F2 workflow 权限最小化（build 仅 `contents: read`，`pages: write`/`id-token: write` 只在 deploy job）；
    F3 五个第三方 Action 全部 pin 到 commit SHA；F4 依赖锁版本；F5 `--out` 改白名单校验；
    F6 `_clean_out_dir` 不跟随符号链接且失败降级为警告；F7 `checkout` 加 `persist-credentials: false`。
  - **可访问性**：R1 主要控件点击区 ≥44×44 px、分类 chips ≥36×36 px（高于 WCAG 2.1 AA 的 24×24）；
    R2 次要文字色由 `#79818f`（实测 3.93:1 不达标）改为 `#667085`（在 `#ffffff` / `#f5f6f8` 上实测 4.97 / 4.60，达标）。
  - **健壮性**：R3 `--no-avatars` 不再产生失效头像引用（改首字母占位）；R4 `--quiet` 不再吞掉错误输出；
    R5/R6 验收断言加强（AC2 校验每张头像真实存在、AC3 对比 registry 计数、AC10 对**全部**产物做哈希）。
  - **复验二轮（安全审计）**：F1–F7 复验全 PASS；另提 4 条 Low 已一并修掉 ——
    N1 超长 id 不再抛栈（id 白名单加长度上限 64 + `_avatar_source` 与 `main` 兜住 `OSError`）；
    N2 `--out` 归属判据改用本脚本专属标记 `.hub-site-build`（不再拿通用的 `.nojekyll` 当「这是我建的目录」的证据）；
    N3 `<out>/assets/avatars` 被预置为符号链接时拒绝写入；N4 workflow 构建前先 `rm -rf site`。
  - **构建改为「先写后删」（自测发现）**：原实现先删 `index.html` 与旧头像再重写，**一次中断就把站点打成半成品**
    （本次实测到「`index.html` 消失 + 35 张头像只剩 8 张」）。改为新产物全部落盘后才清理陈旧头像
    （`_prune_stale_avatars`），中断时目录内仍是上一次的完整产物。
  - **回归结果**：`tests/test_build_site.py` **33/33** 通过（含 9 个路径穿越/符号链接攻击向量 + 写失败清引用）；`tests/verify_site.py` **13/13** 通过（`--browser` 真实 Chrome CDP 全绿，含 AC8 未捕获异常检测、AC9d URL 还原、AC12 外链属性）。
  - **三轮（测试覆盖 + 性能）补强**：测试覆盖审查抓出 AC8 Critical 缺口 —— 验收此前只断言「网络失败请求」，**不抓页面 JS 运行时未捕获异常**（且 CDP 事件缓冲未排空，晚到异常会漏判）；一并补齐 AC9d（带 `#q=播客&type=expert` 直达、再 `about:blank` 后还原，断言 q 与全部专家态恢复）、AC12（35 张卡片 `target="_blank"` + `rel="noopener"`）、CDP 连接/超时异常降级为可读结论而非栈。性能侧：首屏首行 6 张头像由 `loading="lazy"` 改 `loading="eager" fetchpriority="high"` 优化 LCP；次要文字色 `#6b7280` 实测仅 4.47:1 不达标，**未采用**。
  - **部署门禁修正（终验发现）**：`verify_site.py --browser` 在 GitHub runner（默认无 Chrome）会把「未找到 Chrome」判为失败并**永久阻断部署**；改为缺失 Chrome / websocket-client 时降级为「跳过」（非阻塞），CI 仍强制静态检查（AC2–AC7 / AC10 / AC12），交互检查（AC8 / AC9）在有 Chrome 的本地环境补全（如需 CI 也跑交互检查，可给 build job 加装 chromium 的步骤）。
- **⚠️ 人工前置（无法脚本化）**：仓库 **Settings → Pages → Build and deployment → Source** 选择
  **「GitHub Actions」**，之后 push 到 `main` 即自动构建部署。

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

### 2026-10-15 — 从 agency-agents-zh 引入 10 个专家/专家团（4 团 + 7 单专家，实际产出 10 个资产）

- **来源**：[jnMetaCode/agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)（MIT，277 个中文角色角色库），
  经大漠从 28 个勾选角色中裁决收敛。**不是平移，是按 WorkBuddy 专家包格式重造。**
- **产出（4 个专家团）**：
  - `teams/video-commerce-crew` 短视频直播电商专家团（5 成员，主理人「抖策」）：抖音策略师 / 视频号运营 / 直播教练 / B站 / 剪辑指导
  - `teams/ecommerce-ops-crew` 电商运营专家团（3 成员，主理人「店策」）：中国电商运营 / 跨境电商 / 供应商评估
  - `teams/legal-finance-desk` 法务财税合规团（3 成员，主理人「律衡」）：合同审查 / 制度文件 / 发票管理
  - `teams/generative-visual-studio` 生成式视觉专家团（4 成员，主理人「图构」）：图像提示词 / 视频提示词 / UX 研究 / 包容性视觉
- **产出（6 个单专家）**：`prompt-architect` 构意 · `multi-agent-architect` 织网 · `workflow-architect` 径流 ·
  `brand-guardian` 守一 · `tech-translator` 译码 · `xhs-operator` 薯策
- **重复裁决（与大漠逐项确认后落定）**：
  - 工程四角色 → 弃前端/后端（`engineering-review-board` 82 项技能 + `software-architect` 已覆盖），只留多智能体与工作流架构
  - 设计四角色 → 弃 UI 设计师 / UX 架构师（`visual-forge-studio` + `ui-design-field-manual` 已覆盖），留 UX 研究 + 包容性视觉并入视觉团
  - 平台内容四角色 → 弃知乎/微博/公众号/多平台发布（`media-content-team` + `self-media-studio` + `creator-ops` 已覆盖），只做短视频与直播
  - 提示词工程 / 品牌守护 / 技术翻译 → 三者各自独立成单专家，不塞进任何团
- **品牌清洗（三类分治，实测 8 条断言 + 全量扫描）**：
  - C1 中性化：Claude / ChatGPT / Gemini / Cursor / Midjourney / Sora / Veo / Seedance / Salesforce / Ahrefs / Semrush 等 → 中性表述
  - C2 逐字保留：`ClaudeBot` / `Claude-SearchBot` / `GPTBot` / `PerplexityBot` 等 **真实 crawler user-agent 名**
    （清洗掉会让 GEO 技能失效）。实现上用 `\x00` 数字占位符，避免占位符被后续规则吃掉——第一版用 `§KEEP§` 实测被清空，已修。
  - C3 保留：MCP / AWS / Kubernetes / Docker / Terraform / GitHub 及抖音 / 小红书 / 1688 / 蒲公英等平台专名
  - **坑**：上游 `description` 字段也会进入展示层与路由匹配，必须一并清洗；第一版只洗正文导致 `Sora/Veo/Seedance` 漏网，
    且 `build.py` 自带 `load_body` 覆盖了 `importer.load_source`，两处都修后才清零。
- **合规修正**：剥离上游全部非标准 frontmatter 字段（`emoji` / `color` / `tools` / `services`），
  改写为 WorkBuddy 原生格式（`displayName` / `profession` / `maxTurns`）。
- **许可**：每个资产带 `LICENSE` + 团队包带 `ATTRIBUTION.md`，保留上游 MIT 声明与改造说明。
- **校验结果**：`validate_expert.py`（官方）20/20 通过；`validate.py` 77/77；
  `verify_upload_ready.py` 10/10 通过 **0 提示**（`displayDescription.zh` 43–48 字、`tags` 恰好 3 个、
  `quickPrompts` 恰好 3 条且 `[0]` 等于 `defaultInitPrompt`）。
- **注册**：`.workbuddy` 与 `.workbuddy-ai` **两处配置根各注册 10/10**，各 45 条。
  ⚠️ 注意 `validate_expert.py` / `register_expert.py` 读 `WORKBUDDY_CONFIG_DIR`（缺省 `~/.workbuddy`），
  校验 `.workbuddy-ai` 下的资产会报「不在专家目录下」——**这是默认路径未覆盖，不是该目录无效**，须显式传环境变量。
- **包体积**：503–536 KB（上限 20 MB）。`build/<id>.zip` 第一层即资产目录。
- **头像**：统一用 `assets/avatars/_default.jpg`（255 KB），未用 ImageGen（避免 5–10 credits/张）。

### 2026-10-15（续）— 为上述 10 个资产补齐技能包（skills 从 0 → 10）

- **背景**：第一批只交付了人格（`agents/`），`skills/` 全为空——专家「能聊但不能干活」。
  本次把上游正文里的交付物模板抽成 `SKILL.md` + `references/`，共 **10 个 SKILL.md + 47 个 references、73,929 字**。
- **技能清单**：
  | 资产 | 技能 ID | references |
  |---|---|---:|
  | `xhs-operator` | `xhs-seeding-playbook` | 4（笔记模板/投放排期/合规红线/复盘指标） |
  | `video-commerce-crew` | `short-video-launch-kit` | 7（抖音脚本/排品/话术/千川/算法红线/B站/剪辑） |
  | `ecommerce-ops-crew` | `ecommerce-ops-kit` | 5（评分卡/验厂报告/年度策略/跨境/国内） |
  | `legal-finance-desk` | `legal-finance-kit` | 7（合同七类清单/意见书/三法/隐私政策/发票制度/健康度/税务红线） |
  | `generative-visual-studio` | `visual-prompt-kit` | 10（图像四层/视频五段/负面词/成本/研究计划/画像/包容性三件） |
  | `prompt-architect` | `prompt-eval-loop` | 3（四段模板/设计原则/评测迭代） |
  | `multi-agent-architect` | `topology-select` | 3（五拓扑/上下文架构/硬规则） |
  | `workflow-architect` | `workflow-tree-template` | 2（四视图注册表/发现方法） |
  | `brand-guardian` | `brand-consistency-checklist` | 2（品牌基础/守门规则） |
  | `tech-translator` | `tech-translation-rules` | 3（风格指南/常见模式/五步流程） |
- **references 一律逐字抽取上游原文**，只做三件机械处理：剥 frontmatter、章节 emoji 前缀归一、品牌清洗。
  每个文件头部注明「已做 / 未做」，不冒充原创。
- **踩坑（值得记）**：
  1. **抽取结束边界误匹配代码块内部的 `## `**：上游把 Markdown 模板放在 ```markdown 代码块里，
     块内也有 `## 研究目标` 这类标题。用 `^## ` 当结束正则会把内容截断在代码块中间——
     实测 `ux-research-plan` / `system-prompt-template` / `brand-foundation` 三个被截成 20 字。
     **修法：结束判定必须排除代码块内的行**（用 fence 开关跟踪），`fix_refs.py` 已修。
  2. **「过短」不等于「残缺」**：用尾行比对法逐个对照源章节，确认 12 个短文件全部完整——
     合规红线、算法权重这类清单上游原文本就精炼。没有这一步就会误改好文件。
- **校验**：官方 `validate_expert.py` 20/20（含 skills 引用路径检查）；`validate.py` 77/77；
  `verify_upload_ready.py` 10/10 0 提示；品牌残留扫描 78 个文件 **0 命中**。
- **体积**：508–562 KB（含 skills 后仍远低于 20 MB 上限）。

### 2026-10-15（再续）— 全量改名规避平台名称占用（`xhs-operator` 已被占用）

- **触发**：上传 `xhs-operator` 被平台拒——「专家名称 "xhs-operator" 已被占用」。
  平台对 `name` 是**全平台全局唯一**（不是账号内唯一），通用名极易撞车。
- **处置**：一次性给**全部 10 个**资产加 `agency-` 前缀，而非只改报错那一个。
  理由：其余 9 个同样是通用名（`prompt-architect` / `brand-guardian` / `tech-translator`…），
  逐个撞名再逐个重打包，每次驳回还占版本号，成本远高于一次全改。

| 旧 id | 新 id |
|---|---|
| `video-commerce-crew` | `agency-video-commerce-crew` |
| `ecommerce-ops-crew` | `agency-ecommerce-ops-crew` |
| `legal-finance-desk` | `agency-legal-finance-desk` |
| `generative-visual-studio` | `agency-generative-visual-studio` |
| `prompt-architect` | `agency-prompt-architect` |
| `multi-agent-architect` | `agency-multi-agent-architect` |
| `workflow-architect` | `agency-workflow-architect` |
| `brand-guardian` | `agency-brand-guardian` |
| `tech-translator` | `agency-tech-translator` |
| `xhs-operator` | `agency-xhs-operator` |

- **改名必须同步的 8 处**（漏一处就被校验器抓住）：
  1. 目录名 2. `plugin.json` 的 `name` 3. `plugin` 4. `agentName`
  5. `agents[]` 路径 6. `agents/*.md` 文件名 7. `agents/*.md` frontmatter 的 `name`
  8. `settings.json` 的 `agent`（team）＋ `teamInfo` ＋ `members[].id` ＋ 头像文件名与 `avatar` 字段
- **踩坑（改名连踩三个）**：
  1. **只改文件名不改 frontmatter `name`** → 官方校验器报 `frontmatter name 'x' != filename 'y'`，10 个全挂。
     修 21 个 `agents/*.md` 后才过。
  2. **`avatar` 字段与成员头像路径没跟着改** → 20 个「头像缺失」。补 `avatars/<id>.jpg` + 改字段。
  3. **`rm -rf` 删不掉 `~/.workbuddy*` 下的旧目录** → `safe-delete` 守卫报 `state lock timeout`
     但 **exit code 仍是 0**（假象），实际一个都没删。改用「保留旧目录 + 从 `marketplace.json`
     移除旧 id 条目」达成同等效果，不触碰删除。
- **注册清单被覆盖**：`cp -r` 同步资产后 `.workbuddy` 的 `marketplace.json` 掉回 35 条，
  需重新补写 10 条。最终两处各 **45 条、10/10 全在**。
- **体积变化**：团包 1.3–1.8 MB（成员头像从 0 → 每人一张），单专家 508–525 KB。均远低于 20 MB。
- **校验**：官方 `validate_expert.py` 10/10；`verify_upload_ready.py` 10/10 **0 提示**。
