#!/usr/bin/env python3
"""workbuddy-hub 站点验收自检。

对照 docs/hub-site-spec.md 的验收标准逐条核对。

静态检查（默认执行，无需浏览器）：
    AC2  产物存在（index.html / .nojekyll / 头像）
    AC3  卡片数量与 registry 一致
    AC4  资源引用全为相对路径
    AC5  卡片外链指向的仓库路径真实存在
    AC6  index.html 体积在预算内
    AC7  单张头像体积在预算内
    AC10 生成器幂等

浏览器检查（--browser，需要本机 Chrome）：
    AC8  页面无控制台错误、无 4xx/5xx 资源请求
    AC9  搜索与筛选行为正确

用法：
    python3 tests/verify_site.py              # 静态检查
    python3 tests/verify_site.py --browser    # 含浏览器检查
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = REPO_ROOT / "site"
BUILD_SCRIPT = REPO_ROOT / "scripts" / "build_site.py"

HTML_BUDGET_KB = 250
AVATAR_BUDGET_KB = 40

CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


@dataclass
class Result:
    code: str
    title: str
    ok: bool
    detail: str = ""
    skipped: bool = False  # 环境缺失（如无 Chrome）导致的非阻塞跳过，不计入失败


def _kb(path: Path) -> float:
    return path.stat().st_size / 1024


def _registry_counts() -> tuple[int, int]:
    """从 registry 读期望的专家 / 专家团数量，避免断言写成恒真的弱条件。"""
    import yaml

    def _count(name: str, key: str) -> int:
        data = yaml.safe_load((REPO_ROOT / "registry" / name).read_text(encoding="utf-8"))
        return len(data.get(key) or [])

    return _count("experts.yaml", "experts"), _count("teams.yaml", "teams")


def _site_digest() -> str:
    """对站点目录全部文件（含头像与 .nojekyll）求摘要，用于幂等比对。

    文件在 rglob 与 read_bytes 之间消失（并发重写同一 site/ 时可能发生）不该让
    验收脚本崩掉——跳过即可，缺失会被后续断言暴露。
    """
    digest = hashlib.sha256()
    for path in sorted(SITE_DIR.rglob("*")):
        try:
            if path.is_file():
                digest.update(str(path.relative_to(SITE_DIR)).encode("utf-8"))
                digest.update(path.read_bytes())
        except OSError:
            continue
    return digest.hexdigest()


# --------------------------------------------------------------------------
# 静态检查
# --------------------------------------------------------------------------

def check_static() -> list[Result]:
    results: list[Result] = []

    index = SITE_DIR / "index.html"
    nojekyll = SITE_DIR / ".nojekyll"
    avatar_dir = SITE_DIR / "assets" / "avatars"

    if not index.is_file():
        results.append(Result("AC2", "产物存在", False, f"缺少 {index}"))
        return results

    html = index.read_text(encoding="utf-8")
    avatars = sorted(avatar_dir.glob("*.jpg")) if avatar_dir.is_dir() else []

    # 每张卡片引用的头像文件都必须真实存在——可抓住 --no-avatars 之类产出 404 的情况
    avatar_refs = sorted(set(re.findall(r'<img class="avatar" src="([^"]+)"', html)))
    missing_avatars = [r for r in avatar_refs if not (SITE_DIR / r).is_file()]

    results.append(
        Result(
            "AC2",
            "产物存在",
            bool(avatars) and nojekyll.is_file() and not missing_avatars,
            f"index.html ✓ · .nojekyll {'✓' if nojekyll.is_file() else '✗'} · "
            f"头像文件 {len(avatars)} 张 · 卡片引用 {len(avatar_refs)} 个"
            + ("" if not missing_avatars else f" · 缺失引用 {len(missing_avatars)} 个"),
        )
    )

    cards = re.findall(r'<a class="card"', html)
    experts = re.findall(r'data-type="expert"', html)
    teams = re.findall(r'data-type="team"', html)
    expected_experts, expected_teams = _registry_counts()
    results.append(
        Result(
            "AC3",
            "卡片数量",
            len(cards) == expected_experts + expected_teams
            and len(experts) == expected_experts
            and len(teams) == expected_teams,
            f"共 {len(cards)} 张（专家 {len(experts)}/{expected_experts} · "
            f"专家团 {len(teams)}/{expected_teams}）",
        )
    )

    bad_refs = re.findall(r'(?:href|src)="(/[^"]*)"', html)
    results.append(
        Result(
            "AC4",
            "相对路径引用",
            not bad_refs,
            "无绝对路径引用" if not bad_refs else f"发现 {len(bad_refs)} 处：{bad_refs[:3]}",
        )
    )

    urls = set(re.findall(r'href="(https://github\.com/[^"]+/tree/[^"]+)"', html))
    missing = []
    for url in sorted(urls):
        parts = url.split("/tree/", 1)[1].split("/", 1)
        rel = parts[1] if len(parts) > 1 else ""
        if not (REPO_ROOT / rel).is_dir():
            missing.append(rel)
    results.append(
        Result(
            "AC5",
            "外链路径存在",
            bool(urls) and not missing,
            f"校验 {len(urls)} 条仓库链接"
            + ("" if not missing else f"，缺失：{missing[:3]}"),
        )
    )

    size = _kb(index)
    results.append(
        Result(
            "AC6",
            "页面体积",
            size <= HTML_BUDGET_KB,
            f"{size:.1f} KB / 预算 {HTML_BUDGET_KB} KB",
        )
    )

    if avatars:
        oversize = [p.name for p in avatars if _kb(p) > AVATAR_BUDGET_KB]
        biggest = max(_kb(p) for p in avatars)
        results.append(
            Result(
                "AC7",
                "头像体积",
                not oversize,
                f"最大 {biggest:.1f} KB / 预算 {AVATAR_BUDGET_KB} KB"
                + ("" if not oversize else f"，超标 {len(oversize)} 张"),
            )
        )
    else:
        results.append(Result("AC7", "头像体积", False, "没有生成任何头像"))

    # F10：卡片外链必须新标签打开且带 rel=noopener（防反向标签页攻击）
    anchors = re.findall(r'<a class="card"[^>]*>', html)
    bad = [a for a in anchors if 'target="_blank"' not in a or 'rel="noopener"' not in a]
    results.append(
        Result(
            "AC12",
            "外链属性",
            not bad,
            f"{len(anchors)} 张卡片均 target=_blank + rel=noopener"
            if not bad
            else f"{len(bad)} 张缺属性",
        )
    )

    results.append(check_idempotent())
    return results


def check_idempotent() -> Result:
    """连续两次生成必须逐字节一致——覆盖 index.html、头像与 .nojekyll 全部产物。"""
    digest_before = _site_digest()
    proc = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--quiet"],
        capture_output=True,
        text=True,
        timeout=180,
    )
    if proc.returncode != 0:
        return Result("AC10", "生成器幂等", False, f"重跑生成器失败：{proc.stderr.strip()[:120]}")
    digest_after = _site_digest()
    return Result(
        "AC10",
        "生成器幂等",
        digest_before == digest_after,
        f"两次产物全量 sha256 {'一致' if digest_before == digest_after else '不一致'}",
    )


# --------------------------------------------------------------------------
# 浏览器检查
# --------------------------------------------------------------------------

class _QuietHandler(SimpleHTTPRequestHandler):
    """静默处理：Chrome 主动断连时不必打印堆栈噪音。"""

    def log_message(self, fmt, *args):  # noqa: A003
        pass

    def handle_error(self, request, client_address):
        pass


class _QuietServer(ThreadingHTTPServer):
    """Chrome 会在拿到资源后主动断连，这里不必打印异常堆栈。"""

    def handle_error(self, request, client_address):
        pass


class Server:
    def __init__(self, directory: Path):
        handler = partial(_QuietHandler, directory=str(directory))
        self.httpd = _QuietServer(("127.0.0.1", 0), handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self) -> "Server":
        self.thread.start()
        return self

    def __exit__(self, *exc) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/"


def find_chrome() -> str | None:
    for candidate in CHROME_CANDIDATES:
        if candidate and Path(candidate).is_file():
            return candidate
    for name in ("google-chrome", "chromium", "chromium-browser", "google-chrome-stable"):
        found = shutil.which(name)
        if found:
            return found
    return None


class Browser:
    """极简 CDP 客户端。"""

    def __init__(self, chrome: str, port: int = 9333):
        self.port = port
        self.proc = subprocess.Popen(
            [
                chrome,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-gpu-sandbox",
                "--disable-software-rasterizer",
                "--disable-dev-shm-usage",
                "--hide-scrollbars",
                "--no-first-run",
                "--no-default-browser-check",
                f"--remote-debugging-port={port}",
                f"--user-data-dir={tempfile.mkdtemp(prefix='hubsite-')}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.ws = None
        self.events: list[dict] = []
        self._uid = 0

    def connect(self, timeout: float = 25.0) -> None:
        import websocket  # 延迟导入，静态检查无需该依赖

        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                raw = urllib.request.urlopen(
                    f"http://127.0.0.1:{self.port}/json/list", timeout=2
                ).read()
                target = next(t for t in json.loads(raw) if t["type"] == "page")
                self.ws = websocket.create_connection(
                    target["webSocketDebuggerUrl"],
                    max_size=64 * 1024 * 1024,
                    suppress_origin=True,
                    timeout=30,
                )
                return
            except Exception:
                time.sleep(0.4)
        raise RuntimeError("无法连接到 Chrome 调试端口")

    def send(self, method: str, params: dict | None = None) -> dict:
        self._uid += 1
        mid = self._uid
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            self.events.append(msg)

    def eval(self, expression: str):
        res = self.send(
            "Runtime.evaluate", {"expression": expression, "returnByValue": True}
        )
        if "exceptionDetails" in res:
            raise RuntimeError(f"页面脚本异常：{res['exceptionDetails'].get('text')}")
        return res["result"].get("value")

    def goto(self, url: str, width: int = 1440, height: int = 900, mobile: bool = False) -> None:
        self.send(
            "Emulation.setDeviceMetricsOverride",
            {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": mobile},
        )
        self.events.clear()
        self.send("Page.navigate", {"url": url})
        for _ in range(80):
            try:
                if self.eval("document.readyState") == "complete":
                    break
            except Exception:
                pass
            time.sleep(0.2)
        time.sleep(0.5)
        # 排干缓冲区：goto 之后这一拍内到达的事件（懒加载头像 404、异步异常）只会在
        # 下一次 send 时才被读出；先发一个 no-op 把它们全部读干净，避免漏判（AC8 排水缺口）
        try:
            self.send("Runtime.evaluate", {"expression": "1", "returnByValue": True})
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.6)

    def close(self) -> None:
        try:
            if self.ws:
                self.ws.close()
        except Exception:  # noqa: BLE001
            # 对端已重置连接时 close() 自身也会抛；关闭阶段不该再抛出去
            pass
        finally:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()


def check_browser(url: str) -> list[Result]:
    try:
        import websocket  # noqa: F401  延迟导入，静态检查无需该依赖
    except ImportError:
        # 缺依赖：本机 DX 提示；CI 已装 requirements，不会走到这里。
        # 视为「跳过」而非「失败」——否则无浏览器环境的 runner 会被永久卡死部署。
        return [
            Result(
                "AC8/AC9",
                "浏览器检查",
                True,
                "跳过（缺少 websocket-client，请 pip install -r scripts/requirements.txt）",
                skipped=True,
            )
        ]

    chrome = find_chrome()
    if not chrome:
        # GitHub 托管的 ubuntu-latest 默认无 Chrome：浏览器检查降级为跳过，
        # 不能判失败，否则部署被永久阻断。需要时可装 Chrome 或设 CHROME_PATH。
        return [
            Result(
                "AC8/AC9",
                "浏览器检查",
                True,
                "跳过（未找到 Chrome，设 CHROME_PATH 或在本机运行以获取交互验收）",
                skipped=True,
            )
        ]

    browser = Browser(chrome)
    results: list[Result] = []
    try:
        browser.connect()
        browser.send("Page.enable")
        browser.send("Runtime.enable")
        browser.send("Network.enable")
        browser.send("Log.enable")
        browser.goto(url)

        # --- AC8：控制台错误与失败请求 ---
        console_errors = [
            e for e in browser.events
            if e.get("method") == "Runtime.consoleAPICalled"
            and e["params"].get("type") == "error"
        ]
        log_errors = [
            e for e in browser.events
            if e.get("method") == "Log.entryAdded"
            and e["params"]["entry"].get("level") == "error"
        ]
        bad_responses = [
            e["params"]["response"]
            for e in browser.events
            if e.get("method") == "Network.responseReceived"
            and e["params"]["response"]["status"] >= 400
        ]
        failed = [
            e["params"]
            for e in browser.events
            if e.get("method") == "Network.loadingFailed"
        ]
        # 未捕获异常（JS 崩溃的最常见形态）走 Runtime.exceptionThrown，不产生 console.error，
        # 也不会进 Log——漏掉它 AC8 就会把"页面坏了"判成干净（已实测复现）。
        exceptions = [
            e for e in browser.events if e.get("method") == "Runtime.exceptionThrown"
        ]
        problems = []
        if console_errors:
            problems.append(f"控制台错误 {len(console_errors)} 条")
        if log_errors:
            problems.append(f"日志错误 {len(log_errors)} 条")
        if bad_responses:
            problems.append(f"失败请求 {len(bad_responses)} 条")
        if failed:
            problems.append(f"加载失败 {len(failed)} 条")
        if exceptions:
            problems.append(f"未捕获异常 {len(exceptions)} 条")
        results.append(
            Result(
                "AC8",
                "无错误与失败请求",
                not problems,
                "干净" if not problems else "；".join(problems),
            )
        )

        # --- AC9：筛选与搜索行为 ---
        results.append(_check_filters(browser))
        results.append(_check_search(browser))
        results.append(_check_hash(browser))
        results.append(_check_hash_restore(browser, url))

    except Exception as exc:  # noqa: BLE001
        # 浏览器/连接层异常（Chrome 崩溃、CDP 连接被重置、机器过载）应以一条可读的
        # 失败收场，而不是把 traceback 抛给调用方——曾实测到 ConnectionResetError
        # 让整个验收脚本崩掉、报告一行都没打印出来。
        results.append(
            Result(
                "AC8/AC9",
                "浏览器检查",
                False,
                f"浏览器检查失败：{type(exc).__name__}: {str(exc)[:120]}",
            )
        )
    finally:
        browser.close()
    return results


FILTER_SCRIPT = r"""
(() => {
  const cards = Array.from(document.querySelectorAll('.card'));
  const visible = () => cards.filter(c => !c.hidden);
  const out = {};

  // 1) 类型筛选：专家团
  document.querySelector('[data-filter-type="team"]').click();
  out.teamVisible = visible().length;
  out.teamAllTeams = visible().every(c => c.dataset.type === 'team');

  // 2) 叠加分类筛选：开发与工程
  const devChip = document.querySelector('[data-filter-cat="development"]');
  devChip.click();
  out.teamDevVisible = visible().length;
  out.teamDevOk = visible().every(
    c => c.dataset.type === 'team' && c.dataset.cat === 'development'
  );

  // 3) 回到全部
  document.querySelector('[data-filter-type="all"]').click();
  document.querySelector('[data-filter-cat="all"]').click();
  out.allVisible = visible().length;
  out.total = cards.length;

  // 4) 空状态
  const q = document.getElementById('q');
  q.value = 'zzz-绝对不存在的关键词-zzz';
  q.dispatchEvent(new Event('input', { bubbles: true }));
  out.emptyShown = !document.getElementById('empty').hidden;
  out.emptyVisible = visible().length;

  // 5) 重置按钮
  document.getElementById('reset').click();
  out.afterResetVisible = visible().length;

  return JSON.stringify(out);
})()
"""


def _check_filters(browser: Browser) -> Result:
    data = json.loads(browser.eval(FILTER_SCRIPT))
    problems = []
    if data["teamVisible"] == 0 or not data["teamAllTeams"]:
        problems.append(f"专家团筛选异常（可见 {data['teamVisible']}）")
    if data["teamDevVisible"] == 0 or not data["teamDevOk"]:
        problems.append(f"类型+分类叠加筛选异常（可见 {data['teamDevVisible']}）")
    if data["allVisible"] != data["total"]:
        problems.append(f"回到全部后可见 {data['allVisible']}/{data['total']}")
    if not data["emptyShown"] or data["emptyVisible"] != 0:
        problems.append("空状态未正确显示")
    if data["afterResetVisible"] != data["total"]:
        problems.append(f"重置后可见 {data['afterResetVisible']}/{data['total']}")
    detail = (
        f"专家团 {data['teamVisible']} · 叠加分类 {data['teamDevVisible']} · "
        f"全部 {data['allVisible']}/{data['total']} · 重置 {data['afterResetVisible']}"
    )
    return Result("AC9a", "筛选与空状态", not problems, detail + (" | " + "; ".join(problems) if problems else ""))


SEARCH_SCRIPT = r"""
(() => {
  const cards = Array.from(document.querySelectorAll('.card'));
  const q = document.getElementById('q');
  const visible = () => cards.filter(c => !c.hidden);

  function run(term) {
    q.value = term;
    q.dispatchEvent(new Event('input', { bubbles: true }));
    const vis = visible();
    const lower = term.toLowerCase();
    const allContain = vis.every(c => {
      const hay = [
        c.dataset.id,
        c.querySelector('.card-name') ? c.querySelector('.card-name').textContent : '',
        c.querySelector('.card-desc') ? c.querySelector('.card-desc').textContent : '',
        c.querySelector('.card-tags') ? c.querySelector('.card-tags').textContent : '',
        // 必须与 page.html 的 _hay 口径一致：实现里也含分类中文名
        c.querySelector('.meta-cat') ? c.querySelector('.meta-cat').textContent : ''
      ].join(' ').toLowerCase();
      return hay.indexOf(lower) !== -1;
    });
    return { term, count: vis.length, allContain };
  }

  const out = [run('播客'), run('审查'), run('seo'), run('专家团')];
  document.getElementById('reset').click();
  return JSON.stringify(out);
})()
"""


def _check_search(browser: Browser) -> Result:
    data = json.loads(browser.eval(SEARCH_SCRIPT))
    problems = []
    for row in data:
        if row["count"] == 0:
            problems.append(f"「{row['term']}」零结果")
        if not row["allContain"]:
            problems.append(f"「{row['term']}」命中不含关键词的卡片")
    detail = " · ".join(f"{r['term']}={r['count']}" for r in data)
    return Result("AC9b", "搜索过滤", not problems, detail + (" | " + "; ".join(problems) if problems else ""))


HASH_SCRIPT = r"""
(() => {
  const q = document.getElementById('q');
  q.value = '播客';
  q.dispatchEvent(new Event('input', { bubbles: true }));
  document.querySelector('[data-filter-type="expert"]').click();
  const after = location.hash;
  return JSON.stringify({ hash: after });
})()
"""


def _check_hash(browser: Browser) -> Result:
    data = json.loads(browser.eval(HASH_SCRIPT))
    ok = "q=" in data["hash"] and "type=expert" in data["hash"]
    return Result("AC9c", "URL 状态同步", ok, f"hash = {data['hash'] or '(空)'}")


def _check_hash_restore(browser: Browser, url: str) -> Result:
    """F8：URL hash 能还原筛选状态（分享/刷新保持）。

    先跳到 about:blank 强制一次跨文档加载，再跳到带 hash 的地址，
    验证 q 与类型筛选被正确还原（否则刷新后筛选丢失）。
    """
    browser.send("Page.navigate", {"url": "about:blank"})
    time.sleep(0.3)
    browser.goto(url + "#q=%E6%92%AD%E5%AE%A2&type=expert")  # 播客 + 仅专家
    data = json.loads(
        browser.eval(
            "JSON.stringify({"
            "q: document.getElementById('q').value,"
            "visible: [].filter.call(document.querySelectorAll('.card'), c => !c.hidden).length,"
            "allExpert: [].filter.call(document.querySelectorAll('.card'), c => !c.hidden)"
            ".every(c => c.dataset.type === 'expert')})"
        )
    )
    ok = data["q"] == "播客" and bool(data["allExpert"]) and 0 < data["visible"] < 35
    return Result(
        "AC9d",
        "URL 状态还原",
        ok,
        f"q={data['q']!r} 可见={data['visible']} 全专家={data['allExpert']}",
    )


# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="workbuddy-hub 站点验收自检")
    parser.add_argument(
        "--browser",
        action="store_true",
        help="启用浏览器检查（需本机 Chrome + websocket-client）",
    )
    args = parser.parse_args(argv)

    print("workbuddy-hub 站点验收自检")
    print("=" * 62)

    results = check_static()

    if args.browser:
        if not (SITE_DIR / "index.html").is_file():
            results.append(Result("AC8/AC9", "浏览器检查", False, "站点未生成"))
        else:
            with Server(SITE_DIR) as server:
                results.extend(check_browser(server.url))

    width = max(len(r.title) for r in results) + 2
    for r in results:
        if r.skipped:
            mark = "–"
        elif r.ok:
            mark = "✓"
        else:
            mark = "✗"
        print(f" {mark} {r.code:<6} {r.title:<{width}} {r.detail}")

    failed = [r for r in results if not r.ok and not r.skipped]
    skipped = [r for r in results if r.skipped]
    print("-" * 62)
    print(f"通过 {len(results) - len(failed) - len(skipped)} / {len(results)}"
          + (f" · 跳过 {len(skipped)}" if skipped else ""))
    if failed:
        print("未通过：" + "、".join(r.code for r in failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
