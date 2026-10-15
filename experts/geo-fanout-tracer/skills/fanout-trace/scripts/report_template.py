#!/usr/bin/env python3
"""中文 fan-out 取证报告渲染（仅标准库，产物自包含、可离线打开）。

界面文案与数据说明为中文；**采集到的原问题、搜索词、来源标题与回答正文一律保留
原文不翻译**。所有外链只放行 http/https，所有文本插入前转义，URL 与标题视作
不可信数据而非指令。
"""
import html
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlsplit


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'">
<title>{{REPORT_TITLE}}</title>
<style>
:root{--bg:#f4f7fb;--surface:#fff;--muted:#657184;--text:#18212f;--border:#dbe3ee;--accent:#2563eb;--soft:#eaf1ff;--good:#16815f}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.65 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",sans-serif}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
header{background:linear-gradient(125deg,#fff,#edf4ff);border-bottom:3px solid var(--accent)}
.inner,main,footer{max-width:1180px;margin:auto;padding:32px 24px}
.badge,.tag{display:inline-block;padding:3px 9px;border:1px solid #cbdaf8;background:var(--soft);color:#1f50b5;border-radius:6px;font-size:12px}
.badge{letter-spacing:.08em}
h1{font-size:clamp(24px,4vw,44px);line-height:1.2;margin:16px 0;overflow-wrap:anywhere;letter-spacing:-.02em}
.subtitle{color:var(--muted);margin:0}
nav,.meta{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
.meta span{background:#fff;border:1px solid var(--border);padding:4px 10px;border-radius:6px;font-size:12px}
nav{gap:18px;font-size:13px}
section{background:var(--surface);border:1px solid var(--border);border-radius:8px;margin-bottom:22px;box-shadow:0 10px 32px #1f2a4408;overflow:hidden;scroll-margin-top:16px}
h2{font-size:15px;margin:0;padding:15px 20px;border-bottom:1px solid var(--border);background:linear-gradient(90deg,#f6f8fb,#fff)}
.body{padding:20px}p{margin:0 0 14px}
.muted,.note{color:var(--muted);font-size:13px}.note{margin:12px 0 0}
.verdict{padding:16px 18px;background:var(--soft);border-left:3px solid var(--accent);margin-bottom:20px;font-size:15px;line-height:1.8}
.verdict p:last-child{margin-bottom:0}
.overview-query{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-bottom:8px}
.overview-query span{color:var(--muted);font-size:12px}
.overview-query code{font-size:14px;font-weight:700;color:var(--text);overflow-wrap:anywhere}
.overview-note{color:var(--muted);font-size:13px}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.kpi{background:linear-gradient(160deg,#fbfcff,#f2f6fd);border:1px solid var(--border);border-radius:8px;padding:14px}
.kpi span{display:block;color:var(--muted);font-size:12px}
.kpi strong{display:block;font-size:28px;line-height:1.25;margin:4px 0}
.kpi small{color:var(--muted);font-size:12px}
.root-query{background:#f8fafd;border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:6px;padding:12px 14px;margin-bottom:18px;overflow-wrap:anywhere}
.root-query span{display:block;color:var(--muted);font-size:12px;margin-bottom:4px}
.branch-list{list-style:none;margin:0;padding:0;counter-reset:branch}
.branch{display:grid;grid-template-columns:42px minmax(0,1fr);gap:6px 12px;padding:14px;border:1px solid var(--border);border-radius:8px;margin-bottom:10px;background:linear-gradient(160deg,#fff,#fafcff)}
.branch:before{content:counter(branch);counter-increment:branch;display:flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;background:var(--soft);color:#1f50b5;font-weight:700;font-size:14px}
.query{font-size:15px;font-weight:600;overflow-wrap:anywhere;margin:0}
.branch-meta{grid-column:2;display:flex;gap:10px;flex-wrap:wrap;align-items:center;font-size:12px}
.tag.positive{border-color:#bfe3d3;background:#eafaf3;color:#0f6b4f}
.domains{display:grid;grid-template-columns:1fr 1fr;gap:10px 22px}
.domain-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 10px;align-items:center;font-size:13px}
.domain-row>span:first-child{overflow-wrap:anywhere}
.count{color:var(--muted);font-size:12px;white-space:nowrap}
.track{grid-column:1/-1;height:7px;background:#eef2f8;border-radius:99px;overflow:hidden}
.fill{height:100%;background:linear-gradient(90deg,#4f8bf7,#2563eb);border-radius:99px}
.toolbar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
.toolbar input,.toolbar select{border:1px solid var(--border);border-radius:6px;padding:7px 10px;font:inherit;font-size:13px;background:#fff;color:var(--text)}
.toolbar label{font-size:12px;color:var(--muted)}
.table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:8px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--border);vertical-align:top}
thead th{background:#f6f8fb;font-size:12px;color:var(--muted);white-space:nowrap}
tbody tr:last-child td{border-bottom:0}
.url{display:block;color:var(--muted);font-size:12px;overflow-wrap:anywhere}
.answer{max-width:78ch}
.answer table{margin:0 0 14px;font-size:13px}
.answer h3{font-size:16px;margin:18px 0 8px}
pre{white-space:pre-wrap;word-break:break-word;background:#f6f8fb;border:1px solid var(--border);border-radius:6px;padding:12px;font-size:12px;overflow-x:auto}
.notes{margin:14px 0 0;padding-left:20px;color:var(--muted);font-size:13px}
.call{border:1px solid var(--border);border-radius:8px;padding:14px;margin-bottom:12px;background:#fcfdff}
.call-title{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:6px}
.appendix{box-shadow:none;background:transparent}
.appendix>h2{background:transparent;color:var(--muted);font-size:13px;padding:12px 20px}
.appendix>details+details{border-top:1px solid var(--border)}
.appendix>details>summary{padding:12px 20px;color:var(--muted);font-size:13px;cursor:pointer}
.appendix>details[open]>summary{color:var(--text)}
.appendix>details>.body{padding-top:4px;background:var(--surface)}
footer{color:var(--muted);font-size:12px}
@media(max-width:700px){.inner,main,footer{padding:24px 16px}.kpis{grid-template-columns:1fr 1fr}.domains{grid-template-columns:1fr}.body{padding:16px}.toolbar{align-items:stretch}.toolbar input{width:100%}.toolbar label{width:100%}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:#fff;font-size:11px}.inner,main,footer{max-width:none;padding:14px 0}section{box-shadow:none;break-inside:avoid}.kpis,.branch,.call{break-inside:avoid}nav,.toolbar{display:none}section{overflow:visible}.table-wrap{overflow:visible}table{min-width:0}a{color:inherit}.body{padding:12px}.domains{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<header><div class="inner"><span class="badge">FAN-OUT 取证报告</span><h1>{{QUERY}}</h1>
<p class="subtitle">一个问题被展开成哪些搜索词、搜索返回了哪些来源、最终答案引用了哪些页面。</p>
<div class="meta">{{META}}</div>
<nav aria-label="报告导航"><a href="#overview">概览</a><a href="#fanout">搜索词展开</a><a href="#domains">来源域名</a><a href="#sources">来源与引用</a><a href="#appendix">明细与原始文件</a></nav></div></header>
<main>
<section id="overview"><h2>概览</h2><div class="body"><div class="verdict">{{OVERVIEW}}</div><div class="kpis">{{KPI_CARDS}}</div></div></section>

<section id="fanout"><h2>搜索词展开</h2><div class="body">
<div class="root-query"><span>原始问题（原样保留，未改写）</span><strong>{{QUERY}}</strong></div>
<ol class="branch-list">{{QUERY_BRANCHES}}</ol>
<p class="note">站点限定词（site: 之类）单独标注，仅用于展示；导出的 <code>queries.json</code> 保留每条搜索词的完整原文。</p>
</div></section>

<section id="domains"><h2>来源域名分布</h2><div class="body">
<p class="muted">按搜索来源中出现的完整 URL 数排序。"已引用"列统计其中有多少个 URL 出现在最终答案的引用里。</p>
<div class="domains">{{DOMAIN_BARS}}</div>
</div></section>

<section id="sources"><h2>来源与最终引用</h2><div class="body">
<div class="toolbar"><label for="source-search">搜索来源</label>
<input id="source-search" type="search" placeholder="输入域名、标题或 URL">
<label for="source-filter">筛选</label>
<select id="source-filter"><option value="all">全部 URL</option><option value="cited">仅已引用</option><option value="uncited">仅未引用</option></select>
<span id="source-count" class="muted" role="status"></span></div>
<div class="table-wrap"><table class="sources"><thead><tr>
<th scope="col">页面 / URL</th><th scope="col">域名</th><th scope="col">来源归属</th><th scope="col">最终引用</th>
</tr></thead><tbody>{{SOURCE_ROWS}}</tbody></table></div>
<p id="no-results" class="note" hidden>没有匹配的来源，换个关键词或筛选条件试试。</p>
<p class="note">出现在搜索来源里 ≠ 被答案引用；被引用也不代表该来源更可信。URL 按完整字符串去重（含跟踪参数），因此计数不一定等于不同页面的数量。</p>
</div></section>

<section id="appendix" class="appendix"><h2>明细 · 按需展开</h2>
<details id="answer"><summary>查看最终答案</summary><div class="body">
<p class="muted">下面是模型返回的原始回答，本报告未对其中的产品、版本与价格做任何复核。</p>
<div class="answer table-wrap">{{ANSWER_HTML}}</div>
<details><summary>查看原始 Markdown</summary><pre>{{ANSWER_RAW}}</pre></details>
</div></details>
<details id="calls"><summary>查看搜索调用记录</summary><div class="body">{{CALL_RECORDS}}
<p class="note">来源归属到具体工具调用；一次调用含多条搜索词时，记录本身不指明每个来源由哪条词产生。</p>
</div></details>
<details id="notes"><summary>数据说明与原始文件</summary><div class="body">{{WARNINGS}}
<div class="table-wrap"><table><tbody>{{DATA_NOTES}}</tbody></table></div>
<ul class="notes">
<li>本报告只呈现这次响应里暴露的搜索轨迹，不代表模型完整的内部检索过程，也不描述其它任何一次运行。</li>
<li>搜索词计数含重复；去重按完整文本。搜索来源与最终引用分别独立计数。</li>
<li>未暴露的搜索词一律留空并记警告，绝不反推或重构。域名保留子域名，不向上归并。</li>
<li>引用偏移是相对 <code>raw-response.json</code> 里原始文本块的偏移，不是相对本报告。</li>
</ul>
<nav aria-label="原始文件">{{ARTIFACT_LINKS}}</nav>
</div></details>
</section>
</main>
<footer>Fan-out 取证报告 · 生成于 {{GENERATED_AT}} · 方法源自开源技能 chatgpt-fanout-queries（MIT，作者 Zimu），本包重写实现</footer>
<script>
(()=>{const search=document.querySelector('#source-search'),filter=document.querySelector('#source-filter'),rows=[...document.querySelectorAll('.sources tbody tr')];
function update(){let count=0;for(const row of rows){const match=row.textContent.toLowerCase().includes(search.value.trim().toLowerCase())&&(filter.value==='all'||(filter.value==='cited')===(row.dataset.cited==='true'));row.hidden=!match;if(match)count++;}
document.querySelector('#source-count').textContent=count+' / '+rows.length+' 个 URL';document.querySelector('#no-results').hidden=count!==0;}
search.addEventListener('input',update);filter.addEventListener('change',update);update();
window.addEventListener('beforeprint',()=>rows.forEach(row=>row.hidden=false));window.addEventListener('afterprint',update);})();
</script>
</body>
</html>
"""


def esc(value):
    return html.escape("" if value is None else str(value), quote=True)


def _action_of(call):
    """取 web_search_call 的 action；非 dict（含真值非 dict，如字符串/数字）一律视为空，
    避免渲染阶段崩溃导致 report.html 静默缺失。"""
    action = call.get("action") if isinstance(call, dict) else None
    return action if isinstance(action, dict) else {}


def _call_id(call):
    """取 web_search_call 的 id 作为索引键；非字符串（list/dict 等不可哈希）一律返回 None，
    避免拿它当 dict key 时抛 TypeError 导致 report.html 半残。"""
    cid = call.get("id") if isinstance(call, dict) else None
    return cid if isinstance(cid, str) else None


def link(url, label=None):
    """只放行来自不可信研究内容的 http/https 链接。"""
    try:
        parts = urlsplit(url)
        valid = parts.scheme.lower() in {"http", "https"} and bool(parts.netloc)
    except ValueError:
        valid = False
    if not valid:
        return esc(label or url)
    return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label or url)}</a>'


def inline(text):
    """一个刻意做小的、不含 HTML 的 Markdown 子集；不支持的语法原样保留。"""
    parts, offset = [], 0
    for match in re.finditer(r'\[([^\]\n]+)\]\((https?://[^\s)]+)\)', text):
        parts.append(esc(text[offset:match.start()]))
        parts.append(link(match.group(2), match.group(1)))
        offset = match.end()
    parts.append(esc(text[offset:]))
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', ''.join(parts))


def answer_html(text):
    """可读的段落与简单表格，不执行任何内嵌 HTML。"""
    blocks = []
    for block in re.split(r'\n\s*\n', text.strip()):
        lines = block.splitlines()
        if not lines:
            continue
        if len(lines) >= 2 and lines[0].startswith('|') and re.fullmatch(r'[\s|:\-]+', lines[1]):
            rows = [[inline(cell.strip()) for cell in line.strip().strip('|').split('|')] for line in lines]
            head = ''.join(f'<th scope="col">{cell}</th>' for cell in rows[0])
            body = ''.join('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>' for row in rows[2:])
            blocks.append(f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')
        elif len(lines) == 1 and lines[0].startswith('#'):
            blocks.append(f'<h3>{inline(lines[0].lstrip("# "))}</h3>')
        elif all(line.startswith('- <http') and line.endswith('>') for line in lines):
            blocks.append('<ul>' + ''.join(f'<li>{link(line[3:-1])}</li>' for line in lines) + '</ul>')
        else:
            blocks.append('<p>' + '<br>'.join(inline(line) for line in lines) + '</p>')
    return ''.join(blocks) or '<p class="muted">本次响应不含答案文本。</p>'


def render_html(report, request=None, artifact_names=(), overview=None):
    s = report['summary']
    queries, calls, sources = report['queries'], report['calls'], report['sources']
    request = request or {}
    settings = request.get('request') or {}
    generated = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    recorded = request.get('recorded_at') or '未记录'
    call_numbers = {_call_id(call): i for i, call in enumerate(calls, 1)}
    search_numbers = {_call_id(call): i for i, call in enumerate(
        (call for call in calls if _action_of(call).get('type') == 'search'), 1)}
    has_overview = bool(overview and overview.strip())
    overview_html = (f'<div class="overview-query"><span>原始问题</span><code>{esc(s["query"])}</code></div>'
                     + (f'<p>{esc(overview.strip())}</p>' if has_overview
                        else '<p>本次运行未生成模型概览。下方卡片仍展示已记录的计数。</p>'))
    if has_overview:
        # 概览来自不可信的网页内容，必须在报告里标明其性质（不能只写在 principles.md）。
        overview_html += ('<p class="overview-note"><strong>模型生成 · 仅作参考</strong>：本段由模型基于'
                          '不可信的网页内容概括，可能受来源页面影响，不是确定性结论，也不代表本报告的计数。</p>')
    if s['warnings']:
        overview_html += '<p class="overview-note"><strong>提示：</strong>本次记录含有警告，详见「数据说明」。</p>'
    cards = [(s['exposed_query_count'], '暴露的搜索词', f"去重 {s['unique_query_count']} 条"),
             (s['search_call_count'], '搜索调用', f"Web 工具调用 {s['web_search_call_count']} 次"),
             (s['source_url_count'], '来源 URL', f"覆盖 {len(s['source_domains'])} 个域名"),
             (s['cited_url_count'], '引用 URL', f"答案中 {s['citation_count']} 处引用")]
    branches = []
    for row in queries:
        pattern = r'(?<!\S)site([:.])(\S+)'
        matches = list(re.finditer(pattern, row['query'], re.I))
        display_query = re.sub(pattern, '', row['query'], flags=re.I).strip()
        domain_meta = ''.join(
            f'<span class="tag">{"站点限定" if match.group(1) == ":" else "域名提及"}：{esc(match.group(2))}</span>'
            for match in matches
        )
        google_query = row['query']
        google_url = 'https://www.google.com/search?' + urlencode({'q': google_query})
        google_link = (f'<a href="{esc(google_url)}" target="_blank" rel="noopener noreferrer"'
                       f' title="{esc(google_query)}" aria-label="在 Google 中搜索：{esc(google_query)}">Google 复核 ↗</a>')
        branches.append(f'<li class="branch"><p class="query">{esc(display_query or "仅域名信息")}</p>'
                        + f'<div class="branch-meta">{domain_meta}{google_link}</div></li>')
    call_html = []
    action_labels = {'search': '搜索', 'open_page': '打开页面', 'find_in_page': '页内查找'}
    for index, call in enumerate(calls, 1):
        action = _action_of(call)
        cid = _call_id(call)
        terms = [row for row in queries if row['call_id'] == cid]
        count = sum(cid in row['search_call_ids'] for row in sources if cid)
        extra = ''
        if action.get('type') == 'search' and not terms:
            extra = '<p class="note">这次搜索调用没有暴露它的搜索词。</p>'
        elif action.get('type') != 'search':
            extra = f'<pre>{esc(json.dumps(action, ensure_ascii=False, indent=2))}</pre>'
        heading = (f'搜索 {search_numbers.get(cid)}'
                   if action.get('type') == 'search' else f'Web 操作 {index}')
        # action.type 可能非字符串（不可哈希），先归一化再当 dict key 用
        atype = action.get('type')
        atype = atype if isinstance(atype, str) else ''
        call_html.append(f'<article class="call" id="call-{index}"><div class="call-title"><strong>{heading}</strong>'
                         f'<span class="tag">{esc(action_labels.get(atype, "其它操作"))}</span>'
                         f'<span class="muted">状态：{esc(call.get("status"))}</span></div>'
                         f'<p>{len(terms)} 条搜索词 · {count} 个来源 URL</p>'
                         f'<details class="technical"><summary>技术细节</summary>'
                         f'<code>{esc(call.get("id"))}</code></details>{extra}</article>')
    domains = Counter(row['domain'] or '未知域名' for row in sources if row['in_search_sources'])
    domain_cited = Counter(row['domain'] or '未知域名' for row in sources if row['in_search_sources'] and row['cited'])
    max_count = max(domains.values(), default=1)
    bars = ''.join(f'<div class="domain-row"><span>{esc(name)}</span><span class="count">{count} / {domain_cited[name]} 已引用</span>'
                   f'<div class="track"><div class="fill" style="width:{count / max_count * 100:.2f}%"></div></div></div>'
                   for name, count in sorted(domains.items(), key=lambda item: (-item[1], item[0])))
    source_rows = []
    for row in sorted(sources, key=lambda item: (not item['cited'], item['domain'], item['url'])):
        attribution = '、'.join(
            f'搜索 {search_numbers[cid]}' if cid in search_numbers else f'Web 操作 {call_numbers[cid]}'
            for cid in row['search_call_ids'] if cid in call_numbers
        )
        attribution = attribution or ('搜索来源' if row['in_search_sources'] else '仅引用')
        citation = f'<span class="tag positive">已引用 · {row["citation_count"]} 处</span>' if row['cited'] else '<span class="muted">未引用</span>'
        url_caption = '<span class="url">' + esc(row['url']) + '</span>' if row['title'] else ''
        source_rows.append(f'<tr data-cited="{str(row["cited"]).lower()}"><td>{link(row["url"], row["title"] or row["url"])}'
                           f'{url_caption}</td>'
                           f'<td>{esc(row["domain"])}</td><td>{esc(attribution)}</td><td>{citation}</td></tr>')
    usage = s.get('usage') or {}
    notes = [('原始问题', s['query']), ('记录时间', recorded), ('报告生成时间', generated),
             ('模型 / 响应状态', f'{s["model"]} / {s["status"]}'), ('响应 ID', s['response_id']),
             ('推理强度 / 搜索模式', f'{(settings.get("reasoning") or {}).get("effort", "未记录")} / {settings.get("tool_choice", "未记录")}'),
             ('按动作类型的调用', json.dumps(s['action_counts'], ensure_ascii=False)),
             ('未暴露搜索词的调用数', s['search_calls_without_queries']),
             ('Token 用量（输入 / 输出 / 合计）', ' / '.join(str(usage.get(k, '未记录')) for k in ('input_tokens', 'output_tokens', 'total_tokens')))]
    slots = {
        'REPORT_TITLE': esc(s['query'] + ' · Fan-out 取证报告'), 'QUERY': esc(s['query']),
        'GENERATED_AT': esc(generated),
        'META': ''.join(f'<span>{esc(label)}：{esc(value)}</span>' for label, value in [('模型', s['model']), ('记录时间', recorded), ('响应状态', s['status'])]),
        'OVERVIEW': overview_html,
        'KPI_CARDS': ''.join(f'<div class="kpi"><span>{esc(label)}</span><strong>{esc(value)}</strong><small>{esc(detail)}</small></div>' for value, label, detail in cards),
        'QUERY_BRANCHES': ''.join(branches) or '<li class="branch">本次响应没有暴露任何搜索词。</li>',
        'CALL_RECORDS': ''.join(call_html) or '<p class="muted">本次响应不含 Web 工具调用。</p>',
        'DOMAIN_BARS': bars or '<p class="muted">本次响应不含来源域名。</p>',
        'SOURCE_ROWS': ''.join(source_rows), 'ANSWER_HTML': answer_html(report['answer']), 'ANSWER_RAW': esc(report['answer']),
        'WARNINGS': ''.join(f'<p class="verdict">{esc(warning)}</p>' for warning in s['warnings']),
        'DATA_NOTES': ''.join(f'<tr><th scope="row">{esc(label)}</th><td>{esc(value)}</td></tr>' for label, value in notes),
        'ARTIFACT_LINKS': ''.join(f'<a href="{esc(name)}">{esc(name)}</a>' for name in artifact_names),
    }
    return re.sub(r'\{\{([A-Z_]+)\}\}', lambda match: slots[match.group(1)], TEMPLATE)


def write_html_report(path, report):
    path = path if isinstance(path, Path) else Path(path)
    request_path = path / 'request.json'
    request = json.loads(request_path.read_text(encoding='utf-8')) if request_path.exists() else {}
    overview_path = path / 'overview.md'
    overview = overview_path.read_text(encoding='utf-8') if overview_path.exists() else None
    artifacts = [name for name in ('request.json', 'summary.json', 'queries.json', 'web-search-calls.json',
                                   'sources.csv', 'citations.json', 'answer.md', 'overview.md',
                                   'raw-response.json', 'overview-response.json') if (path / name).is_file()]
    output = path / 'report.html'
    output.write_text(render_html(report, request, artifacts, overview), encoding='utf-8')
    return output


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description='从已保存的运行目录重建 report.html，不调用 API、不改原始记录。')
    parser.add_argument('run_dir', type=Path)
    args = parser.parse_args(argv)
    try:
        summary = json.loads((args.run_dir / 'summary.json').read_text(encoding='utf-8'))
        response = json.loads((args.run_dir / 'raw-response.json').read_text(encoding='utf-8'))
        report = extract_for_report(response, summary['query'])
        for warning in summary.get('warnings', []):
            if isinstance(warning, str) and warning not in report['summary']['warnings']:
                report['summary']['warnings'].append(warning)
        print(write_html_report(args.run_dir, report))
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'无法生成报告（{type(error).__name__}）。请检查 run 目录里的 raw-response.json 与 summary.json。\n')
    return 0


def extract_for_report(response, query):
    """从 run_fanout.py 导入解析，避免重复实现。"""
    import importlib.util
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location('run_fanout', os.path.join(here, 'run_fanout.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.extract(response, query)


if __name__ == '__main__':
    raise SystemExit(main())
