# 溯问 · AI 搜索取证师（geo-fanout-tracer）

一个手把手带你做 **GEO 证据采集** 的 WorkBuddy 专家：把一个问题直送 OpenAI
Responses API（开启 web_search），抓回它被展开成哪些搜索词、搜索返回了哪些来源、
最终答案引用了哪些页面，生成本地可离线打开的中文取证报告，再把证据翻译成 GEO
内容方向、缺口、Topic Cluster 与竞品/渠道线索。

方法源自开源技能 [`chatgpt-fanout-queries`](https://github.com/JeffLi1993/open-growth-skills/tree/main/chatgpt-fanout-queries)
（MIT，作者 Zimu）。本包**重写实现**：仅用 Python 标准库（零第三方依赖）、中文界面与中文概览，
并完整保留上游"只记录可见证据、绝不反推"的克制原则。

## 它能帮你做什么

1. **Fan-out 取证采集**（`fanout-trace`）：原问题原样直送，保存完整 `raw-response.json`
   后再解析，提取搜索词 / 工具调用 / 来源 URL / 最终引用 / 回答，生成自包含中文 `report.html`。
2. **证据分析**（`fanout-analysis`）：把采集结果对照站内内容，产出**主题覆盖（已覆盖/太浅/缺失）**、
   **内容缺口**、**Topic Cluster 结构**、**内容优先级**与**竞品/渠道线索**。

## 核心立场

- GEO 不是猜模型喜欢什么，而是对**可见证据**做分析、对内容方向做建设。
- 搜索来源 ≠ 最终引用；被引用也不代表更可信，来源顺序不代表重要性。
- 单次结果是**选题线索**，不代表搜索量、排名难度，也不保证被 AI 引用；多组真实问题重复运行更稳。

## 使用前准备

采集需要你自己的 OpenAI API Key，放在项目目录的 `.env` 里（脚本绝不会把 Key 写入任何报告）：

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-6.1-sol
```

依赖：仅 Python 3.8+ 标准库，**无需 pip install**。

## 快速开始

```bash
# 1) 跑一次 fan-out 取证（在线，需 Key）
python3 <skill目录>/scripts/run_fanout.py "best ai ppt maker" --output ./research

# 2) 离线重解析已保存的 Responses API 响应（不需要 Key）
python3 <skill目录>/scripts/run_fanout.py "<原始问题>" \
  --from-response raw-response.json --output ./run

# 3) 仅重建某次运行的 HTML 报告
python3 <skill目录>/scripts/report_template.py <run-目录>
```

也可直接在 WorkBuddy / WorkBuddy AI 里对「溯问」说：

> 用 fan-out 取证分析这个问题：best ai video generator

> 对比这几个问题的 fan-out 结果，找出我站内还没覆盖的主题缺口

## 运行目录产物

每次运行建立一个独立目录，至少包含：

| 文件 | 用途 |
| --- | --- |
| `raw-response.json` | 完整 API 原始响应（先落盘，后解析） |
| `request.json` | 原问题与请求参数，**不含 API Key** |
| `summary.json` | 模型、状态、用量、调用与来源统计、警告 |
| `queries.json` | API 暴露的 fan-out 搜索词 |
| `web-search-calls.json` | 原样保留的 Web Search 工具调用 |
| `sources.csv` | 搜索来源与引用 URL 的并集（去重） |
| `citations.json` | 最终答案里的 URL 引用与原始偏移 |
| `answer.md` | 回答正文与去重引用链接 |
| `overview.md` | 中文概览（可选，第二次请求生成） |
| `report.html` | 自包含、可离线打开的可视化报告 |

## 包结构

```
geo-fanout-tracer/
├── .codebuddy-plugin/plugin.json
├── agents/geo-fanout-tracer.md          # 溯问 persona 与 SOP
├── skills/
│   ├── fanout-trace/                     # 采集：调 API、出报告（零依赖）
│   │   ├── SKILL.md
│   │   ├── .env.example
│   │   ├── references/output-contract.md
│   │   └── scripts/
│   │       ├── run_fanout.py             # 采集 + 解析 + 产物
│   │       └── report_template.py        # 中文 HTML 渲染
│   └── fanout-analysis/                  # 分析：证据 → 内容结论
│       ├── SKILL.md
│       └── references/
├── references/principles.md             # 克制原则（证据纪律 + 安全纪律）
├── avatars/geo-fanout-tracer.jpg
├── manifest.yaml
├── LICENSE
└── README.md
```

## 与「显扬」的关系

仓库里另一位 GEO 专家「显扬」（geo-seo-strategist）是**咨询教学型**：手把手教你怎么
做选题判断、GEO 写作、llms.txt 与度量，纯文档技能、不带脚本。本专家「溯问」是
**证据采集型**：跑真实 API 抓可见搜索轨迹、出可离线报告、把证据变内容结论。两者互补——
可用显扬定方向，用溯问取证据，再回到显扬出内容。

## 许可证与归属

MIT。本包继承并显式保留 `chatgpt-fanout-queries` 的数据契约、计数语义与克制原则；
实现（采集引擎与中文报告）为本包重写。详见 `LICENSE` 与 `references/principles.md`。
