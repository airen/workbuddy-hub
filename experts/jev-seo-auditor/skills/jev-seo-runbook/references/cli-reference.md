# jev-seo CLI 完整参考

上游：https://github.com/AgriciDaniel/jev-seo （MIT）。命令通过包内的 `bin/jevseo` 调用，可从任意目录运行。

## 命令一览

| 命令 | 说明 | 花费 |
|---|---|---|
| `bin/jevseo doctor` | 检查依赖与密钥（绝不打印密钥值） | 免费 |
| `bin/jevseo run <url>` | 审计 + 自动摘要 + 渲染三份报告 | 标准约 0.01 USD |
| `bin/jevseo audit <url>` | 爬取 + 52 规则 + Jev + PageSpeed → `audit.json` + `digest.md` | 标准约 0.01 USD |
| `bin/jevseo render <目录>` | 从 `audit.json` 渲染 `report.pdf` / `report.xlsx` / `report.md` | 免费 |
| `bin/jevseo audit <url> --full` | 追加 DataForSEO 数据（排名关键词、估算流量、竞品、引荐域名对比、关键词建议/创意/差距、实时 Google 结果含 AI Overview 引用、LLM 提及） | 追加约 0.30 USD |
| `bin/jevseo audit <url> --full --reuse-dfs <目录>` | 复用此前已采集的 DataForSEO 数据 | 仅 Jev 部分花费 |
| `bin/jevseo rescore <目录>` | 离线重建发现与评分，不重新爬取 | 免费 |

## 输出位置

所有报告写入 `jev-seo-reports/<domain>-<stamp>/`（`<stamp>` 为时间戳）。该目录含：

- `audit.json` —— 全部审计数据（规则命中、爬取事实、Jev 判断、PageSpeed、DFS 数据），三份报告同源生成；
- `digest.md` —— 自动摘要；
- `report.pdf` / `report.xlsx` / `report.md` —— 三份报告。

## 环境变量与 .env

读取顺序：`JEVSEO_ENV_FILE` → `./.env` → 仓库 `.env`。

| 变量 | 必需性 | 说明 |
|---|---|---|
| `TYPESAFE_API_KEY` | 标准模式实际必需 | Jev 模型；缺失则 Jev 部分标「未评估」、分数为部分审计 |
| `PAGESPEED_API_KEY` | 可选 | 提高 PageSpeed 配额；缺失常被限流 |
| `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD` | `--full` 必需 | DataForSEO 凭据 |

## 预算开关

| 开关 | 默认 | 作用 |
|---|---|---|
| `--jev-budget` | 0.25 USD | Jev API 每次请求前检查的硬上限 |
| `--dfs-budget` | 1.00 USD | DataForSEO 硬上限 |

每次调用记入报告的 **cost ledger**，可在报告中核对实际花费。

## 依赖

- Python 3.10+（CI 覆盖 3.10 / 3.12 / 3.13）；
- WeasyPrint + 系统 Pango（PDF）；
- Playwright + chromium（可选，JS 渲染页面）；
- poppler `pdftoppm`（可选，仅 Claude Code 技能用）。

## 离线测试（无需密钥、零花费）

```bash
python -m unittest discover -s tests -v
```

## 技术栈备忘

Python 3.10+、WeasyPrint + Pango（PDF）、Playwright（可选 JS 渲染）、poppler；第三方 API：TypeSafe Jev、Google PageSpeed Insights、DataForSEO；报告内嵌 Inter + JetBrains Mono（SIL OFL）。

上游仓库结构：`SKILL.md`（Claude Code 技能）、`bin/jevseo`（可从任意目录运行）、`jevseo/`（爬取/解析/检查/jev/dfs/psi/评分/CLI）、`jevseo/report/`（视图模型/图表/PDF/XLSX/MD）、`jevseo/templates/`、`references/`（叙述契约、Jev 问题注册表、评估、方法）、`examples/`、`tests/`（离线测试）。
