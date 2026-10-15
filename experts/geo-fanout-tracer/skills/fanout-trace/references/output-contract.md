# 输入与输出契约

消费导出的产物或改动实现时，以本文为准。

## 输入

必需的位置参数是一条非空问题。直送在线请求与记录运行时都要逐字保留。已有可选
flag 与默认值属于公开接口：

| 选项 | 默认值 | 含义 |
| --- | --- | --- |
| `--model` | `OPENAI_MODEL`，再退回 `gpt-6.1-sol` | Responses API 模型；显式 flag 优先 |
| `--output` | `research` | 新 run 目录的父目录 |
| `--env-file` | `.env` | 本地 dotenv 文件；进程环境变量优先 |
| `--reasoning-effort` | `low` | `none`/`low`/`medium`/`high`/`xhigh` |
| `--search-mode` | `required` | 强制 web 搜索，或 `auto` 让模型决定 |
| `--max-output-tokens` | `16000` | 正数输出 token 上限 |
| `--timeout` | `180` | 正数客户端超时（秒） |
| `--from-response` | 未设置 | 离线重解析已有 raw Responses API JSON，不调用 API |
| `--no-model-overview` | false | 跳过第二次无工具的模型概览请求 |

在线搜索请求使用单个 `web_search` 工具，请求 `web_search_call.action.sources`，
设 `store=false`，不自动重试。默认在线模式随后向同一模型发第二次无工具请求生成中文概览。
离线模式绝不调用 API。相对的输出与 dotenv 路径相对当前工作目录解析。

`--reasoning-effort` 的取值依模型支持而定，不被支持的取值会返回 HTTP 400。
导入文件与响应体都有 32 MiB 上限；请求**不跟随重定向**（避免把付费 POST 以同一 body 重发到别处）。

离线模式的 `request.json` 只含 `input` / `mode` / `imported_from`（**仅文件名，不含本机路径**）/
`recorded_at`，没有 `request` 对象，因此报告里"推理强度 / 搜索模式"显示"未记录"。

## 运行目录

每次调用建立一个带 UTC 时间戳与随机后缀的独立目录，不覆盖既有 run。已完成或
部分完成的响应都会产出：

| 产物 | 契约 |
| --- | --- |
| `raw-response.json` | 精确 HTTP 响应体，在任何派生解析之前写入；离线模式下为导入文件的精确文本 |
| `request.json` | 输入与请求元数据，不含 API Key |
| `summary.json` | 响应元数据、用量、可观测计数、域名与警告 |
| `queries.json` | 仅 API 暴露的搜索词，每条关联其调用 ID |
| `web-search-calls.json` | 每个返回的 `web_search_call`，原样保留 |
| `sources.csv` | 搜索来源与引用 URL 的并集，按完整 URL 字符串去重 |
| `citations.json` | 最终答案里的 URL 引用注释与原始偏移 |
| `answer.md` | 返回的答案文本 + 去重引用链接列表 |
| `report.html` | 由 run 派生的自包含离线报告 |
| `overview-response.json` | 可选：第二次在线请求的原始响应（有则存在） |
| `overview.md` | 可选：中文概览文本；不是确定性计数的来源 |

`sources.csv` 中 `in_search_sources` 与 `cited` 独立。`search_call_ids` 以分号分隔，
`citation_count` 统计引用注释数，可能触发表格公式的单元格前加单引号。原始 JSON 永不为表格安全而改动。

## 计数语义

- `web_search_call_count` 统计每个 Web Search 工具调用。
- `search_call_count` 统计 `action.type` 为 `search` 的调用。
- 打开页面与页内查找在 `action_counts` 中分别计数。
- `source_url_count` 只统计**搜索动作**返回的 `sources`；`open_page` / `find_in_page` 动作里的
  `action.url`（被打开/查找的页面）不计入来源。非 URL 来源项（如 `type:"api"`）被忽略且不产生警告。
- 一次搜索调用可能暴露多条搜索词，也可能没有。缺失的搜索词计入 `search_calls_without_queries` 并产生警告。
- 域名保留子域名。仅跟踪参数不同的 URL 仍视为不同。
- 引用偏移相对其原始响应内容块，而非拼接后的 Markdown 答案。

退出状态：仅完成响应为 `0`；API/文件/解析失败或未完成响应为 `1`；未配置 API Key 为 `2`；
中断为 `130`。

数据产物在可选的概览请求之前导出；`report.html` 在概览请求之后**统一重渲一次**——成功时纳入
概览文本，失败时纳入净化后的警告，两种情况下都与 `summary.json` 保持一致。概览失败时，研究
产物仍然可用，命令返回 `1`（即使搜索响应状态为 completed）。不要据此当作搜索失败或自动重发。
