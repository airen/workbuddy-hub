# workbuddy-hub

**WorkBuddy 能力资产枢纽。** 把分散在各处的 **Skills（技能）**、**Experts（专家）**、**Teams（专家团）**
集中到一个遵循统一规范的仓库里，让人工维护和 AI 编程助手都能轻松地创建、检查、更新与发布资产。

## 这个项目解决什么问题

- **资产散、乱、难找**：技能/专家/专家团散落在不同目录、压缩包、聊天记录里，无法一眼看清「我有什么」。
- **重复维护**：同一个能力在多个专家里各存一份，改一处漏一处。
- **发布门槛高**：手动打包容易多套一层目录、漏字段、头像缺失，被平台反复驳回。
- **引用关系不透明**：专家引用了哪些技能、专家团有哪些成员，全靠肉眼翻文件。

workbuddy-hub 用「**单一事实来源 + 派生索引**」的架构一次性解决：
每个资产的权威定义就是 WorkBuddy 原生文件（`SKILL.md` / `.codebuddy-plugin/plugin.json` / `agents/*.md`），
而 manifest、registry、引用检查、打包发布全部由脚本自动派生——**永不过期，永不双份**。

## 仓库结构

```
workbuddy-hub/
├── README.md / CONTRIBUTING.md / CHANGELOG.md / LICENSE
├── skills/        # Skill 能力库（每个子目录一个技能，含 SKILL.md）
├── experts/       # Expert 专家库（单专家，含 .codebuddy-plugin + agents/）
├── teams/         # Team 专家团库（含多个 agents/ 与 settings.json）
├── registry/      # 由脚本自动生成的全局索引（skills/experts/teams/categories.yaml）
├── schemas/       # manifest.yaml 的 JSON Schema 校验规则
├── templates/     # 新建资产的脚手架
├── scripts/       # 管理工具：import / sync / build-registry / validate / package
├── tests/         # 自动化测试（占位，后续补全）
├── docs/          # 设计与维护文档
├── examples/      # 完整使用示例
├── assets/        # 共享资源（如统一默认头像 avatars/_default.jpg）
├── build/         # package.py 产出的可上传 zip（gitignore，不提交）
└── .github/       # CI 工作流（占位，后续补全）
```

## 三类资产

| 类型 | 定义 | 关键文件 | bucket |
|---|---|---|---|
| **Skill** | 某项任务具体怎么做 | `SKILL.md`（frontmatter 为权威元数据） | `skills/<id>/` |
| **Expert** | 由谁思考/判断/执行，用哪些技能 | `.codebuddy-plugin/plugin.json` + `agents/<id>.md` | `experts/<id>/` |
| **Team** | 多专家如何分工协作交付 | 同上 + `settings.json` + 多个 `agents/*.md` | `teams/<id>/` |

每个资产根目录可附加一个 hub 专用的 `manifest.yaml`（由脚本自动生成），用于检索、筛选、引用检查。
**资产的权威定义始终是 WorkBuddy 原生文件**；manifest 只是派生元数据。详见 `docs/workbuddy-compatibility.md`。

## 日常操作

```bash
# 安装脚本依赖（首次）
pip install -r scripts/requirements.txt

# 导入一个新资产（zip 或已解压目录），自动识别类型并放入对应 bucket
python scripts/import_asset.py path/to/asset.zip
python scripts/import_asset.py path/to/asset-dir

# 生成 / 刷新所有资产的 manifest.yaml
python scripts/sync_manifests.py            # 只补缺的
python scripts/sync_manifests.py --force    # 全量从原生文件重新推导

# 生成全局索引 registry/*.yaml（含引用完整性检查）
python scripts/build_registry.py

# 校验所有资产格式与结构
python scripts/validate.py

# 打包资产为 open.workbuddy.cn 可上传的 zip（自动注入缺失头像）
python scripts/package.py experts/lao-dao-editor
python scripts/package.py --all

# 重新生成 README 里的资产清单
python scripts/generate_readme.py
```

## 资产市场站点（GitHub Pages）

把 `registry/*.yaml` 自动构建成一个**对外公开、无需安装 WorkBuddy 即可浏览**的静态单页站点，
由 GitHub Actions 部署到 GitHub Pages。任何人都能在浏览器里检索、筛选、查看全部专家与专家团，
并一键跳转到仓库对应目录。

- 公开地址：`https://airen.github.io/workbuddy-hub/`
- 规格与验收标准：`docs/hub-site-spec.md`

> ⚠️ 首次启用需人工操作一次：仓库 **Settings → Pages → Build and deployment → Source** 选
> **「GitHub Actions」**。此步骤无法脚本化；不开则 Actions 的 deploy 阶段会失败。

```bash
# 本地预览：重新生成站点（产物在 site/，已被 .gitignore 忽略）
python scripts/build_site.py

# 本地验收：静态检查 + 真实浏览器交互检查（需本机 Chrome + websocket-client）
python tests/verify_site.py            # 仅静态检查（AC2–AC7 / AC10 / AC12）
python tests/verify_site.py --browser  # 额外跑 AC8 / AC9 交互检查（无 Chrome 时自动跳过）

# 提交到 main 即触发 GitHub Actions 自动构建并部署（见 .github/workflows/pages.yml）
git push origin main
```

## 统一默认头像

为节省图像生成积分，hub 内置一张统一默认头像 `assets/avatars/_default.jpg`。
`package.py` 打包时，**凡是没有 `avatars/<id>.png` 或 `<id>.jpg` 的资产，会自动复制一份默认头像注入**。
需要个性头像的资产，替换掉自己 `avatars/` 下的同名文件即可，不影响其他资产。

## 资产清单

> 由 `scripts/generate_readme.py` 自动生成（见下方标记区间）。

<!-- ASSETS_START -->
**当前共 65 个资产**（技能 32 / 专家 25 / 专家团 8）。

## 专家团（Teams）

### content

| ID | 名称 | 描述 |
|---|---|---|
| `content-creation-team` | 内容工厂专家团 | 素材采集、灵感库、选题排期到创作改编与复盘复用，八位环节专家接力，把零散灵感做成内容工厂。 |
| `creator-ops` | 自媒体创作专家团 | 从选题情报到多平台发布与数据复盘，六位环节专家接力，把一句话选题做成可直接发布的成品。 |
| `media-content-team` | 自媒体图文产线团 | 统筹小红书与公众号图文产线：热点选题、对标拆解、封面配图与多平台排版，默认只出草稿不自动群发。 |

### development

| ID | 名称 | 描述 |
|---|---|---|
| `engineering-delivery` | 软件工程交付专家团 | 从需求澄清到上线交付的软件工程专家团：主理人编排六阶段，代码审查、测试、安全、性能四路独立把关。 |
| `hai-stack` | 软件迭代专家团 | 把一次软件迭代做对：先判断值不值得做，再设计边界、按测试驱动落地，用证据确认，最后把文档沉淀干净。 |
| `replica-machine` | 复刻机 | 用 REA 逆向侦察参考站的页面、脚本与网络请求，据此复刻实现，再由独立验证员逐项比对差异，主理人把关需求与交付。 |
| `skill-forge-crew` | 技能工程流水线专家团 | 把技能用成流水线：需求问透、规格落地、测试驱动、质量把关、仓库设防，五人协作，交付可复用的能力。 |

### research

| ID | 名称 | 描述 |
|---|---|---|
| `deep-research-crew` | 深度研究专家团 | 七角色的研究流水线：导航、清洗、解构、归档、溯源各司其职，把散乱网页与厚报告变成可回看的带源报告。 |

## 专家（Experts）

### content

| ID | 名称 | 描述 |
|---|---|---|
| `ai-video-studio` | 影导 | AI 视频制片顾问：把用户的出片目标映射到最合适的外部视频 skill，安装前先核对环境依赖、API key、积分成本与开源许可，再给出安装命令与制作流程，并可在 WorkBuddy 内承接上游的文案、分镜与提示词工作。 |
| `changxiao-marketing` | 长销 | 一站搞定营销活儿：SEO 审计、文案写作、转化优化、邮件、社媒、SEO 与发现、投放与衡量、增长留存、商业化销售。先定产品营销基础（受众/定位），再按需选专项，给可直接拿去用的成果。灵感来自 coreyhaines31/marketing… |
| `geo-seo-strategist` | 显扬 | 网站与应用 GEO SEO 顾问：从选题、写作到 llms.txt，让 AI 与搜索更常引用你。 |
| `growth-demand-studio` | 路拓 | 从定位到获客的增长营销：起名查域名、支付接入、客户线索研究、SEO 审计、选题挖掘与长文撰写。 |
| `ip-visual-forge` | 颜定 | 从一张照片或一句人设开始建立可复用角色档案，再按文章、场景或平台产出风格统一的配图与图解。七条角色 IP 路线按用途选：建档、从零设计、头像 Logo、文章配图、跨平台长期复用、角色图解、长文统一视觉，核心是「换文章换场景还认得出同一个你」。 |
| `office-automation` | 办妥 | 帮你把手头的 Office 文件往前推进——改文档看差异可回退、交代一句就出 PPT/Word/Excel/网页、用自然语言改 Excel、整理存量文档、给内部工具嵌办公能力。灵感来自 genoffice、openworkbuddy、MS… |
| `podcast-to-article` | 陈听 | 把播客链接或逐字稿改写成中文精华长文，保留关键原声并逐章配图，可一键存入 Obsidian。 |
| `self-media-studio` | 柳成文 | 从一句话选题到多平台发布与数据复盘，编排十个模块完成自媒体内容生产闭环，坚持人工确认与证据优先。 |
| `tuwen-forge` | 墨匠 | 不用生图模型，用代码把内容、故事或主题排成可直接发布的中文图文：单图、整套轮播、公众号封面与长图，风格可自选也可自动匹配。 |
| `viral-video-decoder` | 爆析 | 视频爆款拆解师：结合 Hypit 把视频还原成 SVML 脚本图（结构层），再用 WorkBuddy 用证据+套路框架提炼可复用创作模板（分析层），手把手带用户一步步拆解任意爆款视频。 |
| `visual-forge-studio` | 苗绘 | 从文字需求到成品视觉：界面设计、主题配色、社媒配图、交互网页工具与生成艺术，全程守住品牌一致性。 |

### development

| ID | 名称 | 描述 |
|---|---|---|
| `agent-memory-advisor` | 智能体记忆选型顾问 | 按写代码/个人智能体/公司大脑三类场景，从 10 个开源记忆项目挑出能落地的一套，并诊断记忆断环。 |
| `diagram-architect` | 江图南 | 把模糊的绘图需求变成可交付的图表：定图型、定出口，调度五套绘图能力库，过机械质检再交付。 |
| `doc-memory-steward` | 纪文远 | 把项目知识沉淀成可读可改可提交的文档工作区：干活前先查、干完再更新，替代靠召回的记忆插件。 |
| `eng-workflow-coach` | 工程流程教练 | 从想法到交付的工程流程教练：把模糊需求写成规格、拆成工单、按 TDD 实现并评审，卡住时拷问到底。 |
| `engineering-review-board` | 陆鉴 | 全仓库代码审查入口：先建地图，再按需调用架构、技术债、安全、测试等专项技能，默认只读、结论附证据。 |
| `ppt-architect` | 林镜 | 把任意主题变成可直接交付的 PPT：按需选 PPTX 或 HTML 格式，内置 14 种专业风格，产出可直接投屏的正式汇报材料。 |
| `software-architect` | 方权衡 | 用权衡分析驱动架构决策：质量属性、风格选型、领域建模、分布式数据与演化，产出 ADR 与图表。 |
| `spec-driven-dev` | 章立言 | 把模糊需求固化成可执行规格：章程、规格、澄清、方案、任务清单、校验与收敛，让 AI 有据可依。 |

### other

| ID | 名称 | 描述 |
|---|---|---|
| `ai-edu-practice-copilot` | 践衡 | 想把 AI 用进教学，但卡在明天这节课怎么用？从六个开源项目挑能落地的一套并核对前置与合规。 |
| `ai-health-copilot` | 康衡 | 按久坐提醒、饮食记录、聊天录入等场景，从五个开源项目挑能落地的一套，核对部署与模型要求再上手。 |
| `ai-teaching-copilot` | 喻衡 | 按备课、出题、答疑、复习等场景，从六个开源项目匹配可用组合，核对部署模型要求，交付前核题核答案。 |
| `life-assistant` | 当当 | 帮你管生活里的琐碎小事——今天吃什么、钱花哪了、东西放哪了、上次练了多重。按冰箱食材出菜谱与采购单，排一周食谱，记账看开销图，登记家当与保修，记录训练并对照上次。内置工具均为离线网页，数据存本地。 |

### research

| ID | 名称 | 描述 |
|---|---|---|
| `ai-invest-research-copilot` | 研衡 | 把查财报、理投资逻辑、跑策略回测这些活交给 AI，从五个开源项目挑能落地的一套并核对前置与合规。 |
| `lao-dao-editor` | 老刀 | 按三层模型（表层/措辞/结构）重写 AI 味文稿。先动结构骨架——删掉讲明的道理、把结尾打开、把泛指换成具体、留一条没收的线头；再清措辞与用词标点。附结构改动回执与自检脚本，杜绝「只换词不动结构」的假去味。 |
| `web-recon-desk` | 简寻 | 用真实浏览器和抓取能力查网页情报：界面回归走查、结构化抓取、视频分析，多视角交叉验证再下结论。 |

## 技能（Skills）

### content

| ID | 名称 | 描述 |
|---|---|---|
| `de-ai-rewrite` | 去AI味改写 | 去 AI 味改写（自然编辑指南）。当用户要求「去 AI 味」「去掉 AI 腔」「让文字像人写的」「降 AI 检测率」「人味改写」「润色得自然一点」「重写得更自然」或粘贴一段文字要求降低机器痕迹时使用。按资深编辑标准重写文本：删除 AI 腔… |

### development

| ID | 名称 | 描述 |
|---|---|---|
| `ask-matt` | 技能路由 | 该技能是一个路由器（router），根据你此刻的处境告诉你该用哪个技能、走哪条流程：从想法到交付的主流程、分诊 / 诊断 / 寻路这类入口（on-ramp）、代码库维护，以及运行在底层的词汇技能。适用于「我该用哪个技能」「接下来干嘛」「这… |
| `code-review` | 代码评审 | 该技能沿两个轴评审自某个固定点（commit、分支、tag 或 merge-base）以来的改动：标准（Standards，代码是否符合本仓库有文档记录的编码标准？）与规格（Spec，代码是否忠实实现了来源 issue/spec？）。两个… |
| `codebase-design` | 深模块设计 | 为设计深模块（deep module）提供共同词汇：模块、接口、深度、接缝、适配器、杠杆、局部性。适用于「帮我设计一下这个模块」「这个接口怎么设计」「这里该不该抽一层」「怎么让代码更好测」「deepen 一下」这类需求，也供其他技能查阅深… |
| `diagnosing-bugs` | Bug 诊断 | 针对疑难 bug 和性能回退的诊断纪律：先构造一个能稳定变红的反馈回路，再复现、最小化、假设、埋点、修复并补回归测试。适用于「debug 一下」「这个 bug 好难」「帮我定位一下为什么报错」「性能变慢了」「diagnose this」这… |
| `domain-modeling` | 领域建模 | 主动构建并磨利项目的领域模型：挑战术语、打磨模糊用语、就地更新 GLOSSARY.md、按需记录 ADR。适用于「这个术语到底指什么」「帮我理一下领域模型」「写个 ADR」「更新术语表」「domain modeling」这类需求。 |
| `grill-with-docs` | 拷问并留档 | 该技能用于就用户的计划、决策或想法做不留情面的深度访谈，并在访谈过程中顺手产出文档 —— 架构决策记录（ADR）和术语表（glossary）。适用于「拷问我并顺便把文档写了」「边聊边补 ADR 和术语表」「磨方案同时沉淀文档」「grill… |
| `implement` | 按规格实现 | 该技能用于按一份规格说明或一组工单把用户描述的工作实现出来：在事先约定好的接缝（seam）上驱动 TDD，定期跑类型检查与单测、最后跑一次完整测试套件，收尾时用 code-review 技能评审并把工作提交到当前分支。适用于「开始实现」「… |
| `implement-spec` | 整份规格实现 | 该技能用于把一份规格说明和它的关联工单在代码里实现出来：把工单读成一张带阻塞关系的任务图，在一条集成分支（integration branch）上并发调度实施者子代理（用 Agent 工具），最后跑一次 code-review 技能并结掉… |
| `improve-codebase-architecture` | 架构深化扫描 | 该技能扫描一个代码库，找出可以深化（deepening）的地方——把浅模块（shallow module）变成深模块（deep module）的重构——把它们做成一份可视化的 HTML 报告，再就你选中的那一个陪你一路拷问下去。适用于「帮… |
| `port-agent-skills` | 移植外部技能 | 把一个外部 agent 技能仓库（Claude Code / Codex / Cursor 等格式的 SKILL.md 集合）批量转换并安装成 WorkBuddy 可用的技能。适用于「把这个仓库的 skill 封装成 workbuddy … |
| `pr` | PR 正文 | 该技能提供一个撰写 PR 正文（PR body）的模板与配图指引：Summary（摘要配图）、Evidence（证据，前后对比）、Merge Danger（合并风险：单向门/双向门与影响半径）。适用于「写一下 PR 描述」「帮我填 PR … |
| `prototype` | 原型验证 | 构建一次性原型来回答一个设计问题：要么是逻辑 / 状态模型原型，要么是 UI 变体原型。适用于「这个状态机设计得对不对」「帮我看看这个界面应该长什么样」「搭个原型验证一下」「prototype 一下」这类需求。 |
| `retro` | 会话复盘 | 该技能对一次编码会话做复盘（retrospective），找出可改进编码 agent 环境（environment）的候选项，以改善后续运行。适用于「复盘一下这次会话」「做个 retro」「agent 哪里可以改进」「怎么让下次跑得更好」… |
| `setup-matt-pocock-skills` | 工程技能初始化 | 该技能用于把当前仓库配置成其他工程技能所假定的样子：设置 issue 追踪器、分诊标签词汇和领域文档布局，每个仓库在首次使用其他工程技能之前跑一次。适用于「初始化」「配置仓库」「跑一遍 setup」「setup 一下」「配置 issue … |
| `tdd` | 测试驱动开发 | 测试驱动开发，用红-绿-重构（red-green-refactor）循环一次做一个垂直切片，按接缝写测试。适用于「先写测试」「TDD」「红绿重构」「测试驱动」「补集成测试」「测试怎么写」这类需求，也适用于要构建功能或修 bug 但希望测试… |
| `to-spec` | 写成规格 | 该技能用于把当前对话的上下文和代码库理解综合成一份规格说明（spec），并发布到项目的 issue 追踪器上；它不做访谈，只综合你已经讨论过的东西。适用于「写成规格」「生成 spec」「把刚才聊的整理成文档」「沉淀成方案」「输出规格说明」… |
| `to-tickets` | 拆成工单 | 该技能用于把一份计划、规格说明或当前对话拆成一组曳光弹（tracer bullet）工单，每张工单都声明自己的阻塞边（blocking edge），并发布到已配置的追踪器（本地是每张工单一个文件、边写成文本，真实追踪器上则用原生阻塞链接）… |
| `triage` | 分诊 | 该技能把 issue tracker 上的 issue 和外部 PR 推进一个由 triage 角色构成的状态机：分类、核验、必要时拷问，最后写出 agent 可直接执行的简报。适用于「帮我 triage 一下」「看看哪些需要我处理」「把… |
| `ui-design-field-manual` | UI 设计军规 | 用 26 条可工程化的视觉规则，治住 AI 生成界面的「塑料风 / 草台班子感」，让 agent 写出来的页面达到可交付的商业水准。当用户要写或改任何界面、做前端页面、做 Web App / 小程序 / 后台 / 落地页 / 表单 / 卡… |
| `wayfinder` | 寻路规划 | 该技能把一次 agent 会话装不下的庞大工作，规划成 issue tracker 上一份由决策票据组成的共享地图，再逐张推进直到通往目的地的路清晰。适用于「这个项目太大了」「帮我规划一下」「先理清路线再动手」「拆成决策票」这类需求，也适… |
| `wizard` | 交互式向导 | 该技能生成一个交互式 bash 向导（wizard），一步一步带一个人走完只有他们本人才能做的步骤：打开每个 URL、精确说明点哪里复制什么、捕获值、写到该去的地方（.env、GitHub secrets），并逐阶段确认。适用于「给我写个… |
| `writing-for-agents` | 给 agent 写文档 | 该技能是「怎么给 agent 写文档」的参考：技能（skill）、`AGENTS.md`、以及任何靠一条指针够到的文档都适用，讲上下文指针、两种负载、信息层级、完成判据、引导词与修剪。适用于「给 agent 写文档」「写个 skill」「… |

### other

| ID | 名称 | 描述 |
|---|---|---|
| `agent-doc-memory` | 文档即记忆 | 用「能读、能改、能提交」的 Markdown 文档工作区替代召回式记忆插件，让 agent 干活前先查、干完再更新。当用户抱怨「agent 记不住项目」「每次都要重新解释」「上次说好的又忘了」「同一个坑踩三次」「跨会话记不住」，或要建立 … |
| `ai-project-pilot` | AI 项目推进官 | 用「立项 → 计划 → 执行与监控 → 验收与上线」四阶段方法推进 AI 产品与 AI 项目落地，融合 PMP 项目管理与 AI 软件工程实践。当用户要推进或管理一个 AI 项目／AI 产品、写 AI 项目立项与项目章程、定义业务目标与成… |
| `grill-me` | 拷问我 | 该技能用于就用户的计划、决策或想法做不留情面的深度访谈，通过加载 `grilling` 技能把设计树（design tree）的每个分支都逼到有定论，从而把方案磨得更锋利。适用于「拷问我」「帮我挑刺」「压力测试一下这个方案」「这个设计有什… |
| `grilling` | 拷问式访谈 | 就用户的计划、决策或想法做不留情面的深度访谈，直到设计树的每个分支都被解决。适用于「拷问我」「帮我挑刺」「压力测试一下这个方案」「这个设计有什么漏洞」「grill me」这类需求，也是 grill-me / grill-with-docs… |
| `handoff` | 会话交接 | 该技能用于把当前会话压缩成一份交接（handoff）文档，供另一个 agent 接手继续工作。适用于「交接一下」「写个交接文档」「把这个会话总结给下一个人」「换会话前留个 handoff」这类需求，也适用于上下文快满、需要开新会话前保存进… |
| `to-questionnaire` | 转成问卷 | 该技能用于把用户一个人答不上来的决策，转成一份问卷（questionnaire），交给某个人异步填写或在会上一起填。适用于「帮我做份问卷」「这个我不懂，得去问人」「整理成一份问题清单发给对方」「to questionnaire」这类需求，… |
| `wait-what` | 换个说法重讲 | 该技能用于在用户没看懂上一条消息时，让 agent 停下来，用 ASD-STE100 简化技术英语（Simplified Technical English）把那段话重讲一遍：补一点上下文，并使用 `GLOSSARY.md` 里的通用语言… |

### research

| ID | 名称 | 描述 |
|---|---|---|
| `research` | 一手资料调研 | 该技能针对高可信度的一手资料（primary sources）调研一个具体问题，并把结论写成仓库里的一份 Markdown 文件，每条论断都标注来源。适用于「研究一下这个」「帮我查官方文档」「把 API 事实查清楚」「把这个主题研究明白」… |
| `teach` | 教学 | 该技能用于在用户的工作区里教他一门新技能或新概念，以跨多次会话、有状态的方式持续教学：维护任务书（MISSION.md）、术语表（GLOSSARY.md）、学习记录、资源清单和 HTML 课程。适用于「教我这个」「我想学 X」「带我入门」… |

<!-- ASSETS_END -->







## 文档

| 文档 | 内容 |
|---|---|
| `docs/architecture.md` | 三层架构与数据流设计 |
| `docs/naming-conventions.md` | ID、目录、分类、版本、标签规范 |
| `docs/asset-lifecycle.md` | 资产从创建到弃用的生命周期 |
| `docs/workbuddy-compatibility.md` | 与 WorkBuddy 平台格式的兼容说明 |
| `docs/platform-submission.md` | 上架 open.workbuddy.cn 的通用流程与卡点 |

## 远程仓库

本仓库对应的 GitHub 远程：`https://github.com/airen/workbuddy-hub.git`
（本地提交后，由维护者手动 `git push` 到该 remote。）
