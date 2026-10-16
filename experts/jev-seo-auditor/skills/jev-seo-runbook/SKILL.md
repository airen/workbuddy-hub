---
name: jev-seo-runbook
display_name: jev-seo 运行手册
display_name_en: jev-seo Runbook
description: "开源工具 jev-seo 的完整运行手册：安装与依赖自检、密钥与预算开关、audit/render/rescore/--full 全部命令、成本口径、三份报告的产出位置、Claude Code 集成与故障排查。审计前先读这个。"
description_zh: "jev-seo 运行手册：安装自检、密钥与预算、audit/render/rescore/--full 命令、成本口径、报告位置、Claude Code 集成与故障排查。"
description_en: "Complete runbook for the open-source jev-seo SEO audit tool: install, keys, budgets, all commands, costs, report locations, Claude Code integration, and troubleshooting."
category: business
version: 1.0.0
author: 大漠
agent_created: true
---

# jev-seo 运行手册

把「跑一次整站 SEO 体检」的每一步固定成可复现的流程。上游：github.com/AgriciDaniel/jev-seo（MIT）。

## 一、这个工具是什么

给一个**首页 URL**，jev-seo 做四件事：

1. **爬完整站**（遵守 robots.txt 与 Crawl-delay，支持站点地图索引、软 404 检查、llms.txt，默认大站采样 60 页）；
2. **对照 Google 搜索官方文档的 52 条规则逐条核**（分七个区域：爬取与索引、页面元素、内容、链接、结构化数据、AI 爬虫访问、性能与安全；标注「启发式」的规则是编辑惯例，非引擎硬性要求）；
3. **PageSpeed Insights 测 Core Web Vitals**（免费）；
4. **Jev（TypeSafe System One 模型）做内容判断**（13 个页面级 + 5 个站点级问题，保留概率的答案；主页类型由代码设定，不问 Jev）。

最后由代码**评分与排序**，从同一份 `audit.json` 渲染 **PDF / XLSX / Markdown** 三种报告。

## 二、安装与自检

前置：**Python 3.10+**；PDF 渲染需要 Pango（Debian/Ubuntu：`sudo apt install libpango-1.0-0 libpangoft2-1.0-0`；macOS：`brew install pango`；Fedora 通常预装）。

```bash
git clone https://github.com/AgriciDaniel/jev-seo.git && cd jev-seo
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # 填入 TYPESAFE_API_KEY（密钥说明见文件内注释）
bin/jevseo doctor             # 依赖与密钥自检，绝不打印密钥值
```

可选组件：
- **Playwright**（JS 执行后才出现内容的页面，装本地无头 Chromium 渲染）：`pip install playwright && playwright install chromium`；没装就只从原始 HTML 审计这些页面。
- **pdftoppm**（poppler）：仅 Claude Code 技能用来看渲染后的页面。

## 三、密钥（环境变量或 .env，读取顺序 JEVSEO_ENV_FILE → ./.env → 仓库 .env）

| 密钥 | 用途 | 缺失后果 |
|---|---|---|
| `TYPESAFE_API_KEY` | Jev 模型判断 | 无此密钥仍可跑，Jev 部分标「未评估」，分数为部分审计 |
| `PAGESPEED_API_KEY` | PageSpeed 提额 | 缺失时 PageSpeed 常被限流 |
| `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` | `--full` 排名/关键词/外链 | 缺失则 `--full` 不可用 |

## 四、命令总表

| 命令 | 作用 |
|---|---|
| `bin/jevseo doctor` | 依赖与密钥自检 |
| `bin/jevseo run <url>` | 审计 + 自动摘要 + 渲染三份报告 |
| `bin/jevseo audit <url>` | 爬取+规则+Jev+PageSpeed → `audit.json` + `digest.md` |
| `bin/jevseo render <报告目录>` | 从 audit.json 渲染 PDF/XLSX/MD |
| `bin/jevseo audit <url> --full` | 追加 DataForSEO：排名关键词、估算流量、竞品、引荐域名、关键词建议、实时 SERP（含 AI Overview 引用）、LLM 提及 |
| `bin/jevseo audit <url> --full --reuse-dfs <目录>` | 复用此前已采集的 DataForSEO 数据，省钱 |
| `bin/jevseo rescore <报告目录>` | **免费**：离线重建发现与评分 |

`bin/jevseo` 可从任意目录运行。报告输出到 `jev-seo-reports/<domain>-<stamp>/`。

## 五、预算与成本口径（花钱前必须读）

两份付费 API 都有**硬性预算上限**，每次请求前检查，每次调用记入报告的 cost ledger：

| 开关 | 默认 | 说明 |
|---|---|---|
| `--jev-budget` | 0.25 USD | Jev 模型预算上限 |
| `--dfs-budget` | 1.00 USD | DataForSEO 预算上限 |

实际平均成本：

| 环节 | 在哪跑 | 成本 |
|---|---|---|
| 爬取、规则、评分、图表、PDF/XLSX/MD 渲染 | 你的机器 | 免费 |
| JS 渲染（Playwright，可选） | 本地无头 Chromium | 免费 |
| Core Web Vitals / Lighthouse | Google PageSpeed Insights API | 免费 |
| 页面/站点/关键词判断（Jev） | TypeSafe Jev API | 约 **0.00015 USD/页**，标准模式单站约 **0.01 USD** |
| 排名/关键词/竞品/外链/SERP/AI 提及 | DataForSEO API | `--full` 单站约 **0.30 USD** |

## 六、三份报告怎么分工

| 格式 | 给谁 | 内容 |
|---|---|---|
| **PDF** | 客户/上级 | 封面、摘要、计划、流水线、记分卡、影响力 vs 努力矩阵、站点地图、排名、关键词机会、Jev 卡片、质量热力图、投资方向、按区域分类的发现、页面清单、方法、来源（内嵌 Inter + JetBrains Mono，渲染一致） |
| **XLSX** | 执行者当进度表 | Actions（带下拉菜单的可编辑状态追踪）、Summary（实时计数）、Pages、带概率的原始 Jev 判断、Technical、Performance、Rankings、Opportunities、Competitors、SERPs、AI mentions、Charts、Method |
| **Markdown** | GitHub/Obsidian | 图表、Mermaid 饼图、目录行、尺寸化图片，可直接渲染 |

叙述校验（narrative checks）：报告拒绝引用未知行动 ID、标记不在审计数据中的数字、标记不匹配的 effort 区间——**报告里的数字都可以追溯到审计数据**，引用时放心用。

## 七、Claude Code 集成（用户如果在那侧跑）

```bash
ln -s "$PWD" ~/.claude/skills/jev-seo
```

然后 `/jev-seo <网址>`：技能后台跑审计、转发实时进度、读 digest、核查意外发现、写叙述、渲染三份报告。

## 八、可信度与稳定性（2026-09-22 上游实测）

- 规则与爬取事实：独立重新抓取验证全部通过，词数误差 5% 以内；
- DataForSEO 内部一致性精确；PageSpeed 全新独立运行分数完全一致；
- **Jev 可重复性**：同 59 页跑两次，分数平均变化 ≤ 0.03，有把握的页面类型一致 44/44；
- Jev vs 盲审第二法官（仅 decisive 答案）：有帮助性/特异性 28/29、直入主题 23/23、下一步 16/16、关键词相关性 27/30。

**限定**：盲审法官是另一个模型而非人类，证明的是**一致性与合理性**，不是「正确性」；决定性区间之外的答案在所有格式中标 `to verify`。

## 九、局限（必须如实转述）

- 大站按页面上限采样（默认 60 页），报告中会声明；
- Jev 阈值尚未针对人类标签调优；
- PageSpeed 实验室分数运行间会波动，字段数据只对有足够 Chrome 流量的站点存在；
- DataForSEO 的量/难度/流量均为估算值；
- 标「启发式」的规则是编辑惯例，非搜索引擎要求；
- 这是**证据工具**：不预测排名、不测流量收入、不替代 Search Console、不追踪排名随时间变化。

## 十、故障排查

| 症状 | 原因与解法 |
|---|---|
| PDF 渲染报字体/Pango 错 | 装系统 Pango（见第二节） |
| Jev 部分全标「未评估」 | 缺 `TYPESAFE_API_KEY`；补上重跑 |
| PageSpeed 限流 | 补 `PAGESPEED_API_KEY` 提额 |
| JS 页面「内容为空」 | 装 Playwright + chromium 后重跑 |
| `--full` 失败 | 检查 DataForSEO 凭据与 `--dfs-budget` |
| 想重算分数又不想再花钱 | `bin/jevseo rescore <目录>`（离线免费） |
| 复跑 DFS 数据又花钱 | 加 `--reuse-dfs <上次目录>` 复用 |

详细命令语法与输出解读见 `references/cli-reference.md`、`references/report-guide.md`。
