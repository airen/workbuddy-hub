"""geo-fanout-tracer 的回归用例：只测解析 + 报告渲染（零网络、零 API Key）。

不调 OpenAI API；用伪造的 Responses API 响应覆盖解析/渲染的关键边界。
在线路径用 monkeypatch 伪造 `_post` / `generate_overview`，同样不产生费用。
跑：`python3 -m unittest tests.test_geo_fanout_tracer -v`
"""
import csv
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

# 把脚本目录加入路径，避免依赖包安装
HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SCRIPTS = REPO / "experts" / "geo-fanout-tracer" / "skills" / "fanout-trace" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import run_fanout  # noqa: E402


def make_run_dir(query="unit test", resp=None, expect_rc=0):
    """用临时目录跑一次离线解析，返回 (run_dir, resp)。"""
    if resp is None:
        resp = _baseline_response()
    tmp = Path(tempfile.mkdtemp(prefix="fanout-"))
    raw = tmp / "raw.json"
    raw.write_text(json.dumps(resp), encoding="utf-8")
    out = tmp / "research"
    rc = run_fanout.main([query, "--from-response", str(raw), "--output", str(out), "--no-model-overview"])
    assert rc == expect_rc, f"CLI 退出码 {rc} (expected {expect_rc})"
    runs = list(out.iterdir())
    assert len(runs) == 1, f"应建立 1 个 run 目录，得到 {len(runs)}"
    return runs[0], resp


def _offline_run(payload, query="q"):
    """把任意 payload 当 raw.json 跑离线解析，返回 (rc, run_dir_or_None)。"""
    tmp = Path(tempfile.mkdtemp(prefix="fanout-"))
    raw = tmp / "raw.json"
    raw.write_text(json.dumps(payload), encoding="utf-8")
    out = tmp / "out"
    rc = run_fanout.main([query, "--from-response", str(raw), "--output", str(out), "--no-model-overview"])
    runs = list(out.iterdir()) if out.exists() else []
    return rc, (runs[0] if runs else None)


def _baseline_response():
    return {
        "id": "resp_unit", "model": "gpt-6.1-sol", "created_at": 1, "status": "completed",
        "output": [
            {"type": "web_search_call", "id": "ws_1",
             "action": {"type": "search", "queries": ["a", "b"],
                        "sources": [{"url": "https://x.com/p", "title": "P"}]},
             "status": "completed"},
            {"type": "message", "id": "msg_1",
             "content": [{"type": "output_text", "text": "hi <script>alert(1)</script> [x](https://y)",
                          "annotations": [
                              {"type": "url_citation", "url": "https://x.com/p",
                               "title": "P", "start_index": 0, "end_index": 2}
                          ]}]},
        ],
        "usage": {"input_tokens": 1, "output_tokens": 2, "total_tokens": 3},
    }


class CountsAndContract(unittest.TestCase):
    def test_baseline_counts(self):
        run_dir, _ = make_run_dir()
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(s["search_call_count"], 1)
        self.assertEqual(s["web_search_call_count"], 1)
        self.assertEqual(s["exposed_query_count"], 2)
        self.assertEqual(s["unique_query_count"], 2)
        self.assertEqual(s["source_url_count"], 1)
        self.assertEqual(s["cited_url_count"], 1)
        self.assertEqual(s["citation_count"], 1)
        self.assertEqual(s["status"], "completed")
        self.assertEqual(s["warnings"], [])

    def test_actions_separate_counts(self):
        resp = _baseline_response()
        resp["output"].append({"type": "web_search_call", "id": "ws_2",
                               "action": {"type": "open_page", "sources": []},
                               "status": "completed"})
        resp["output"].append({"type": "web_search_call", "id": "ws_3",
                               "action": {"type": "find_in_page", "sources": []},
                               "status": "completed"})
        run_dir, _ = make_run_dir(resp=resp)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(s["web_search_call_count"], 3)
        self.assertEqual(s["search_call_count"], 1)
        self.assertEqual(s["action_counts"], {"search": 1, "open_page": 1, "find_in_page": 1})

    def test_open_page_sources_counted_but_action_url_not(self):
        """open_page 的 sources 计入来源；其 action.url 不算来源（契约明确）。"""
        resp = _baseline_response()
        resp["output"].append({"type": "web_search_call", "id": "ws_2",
                               "action": {"type": "open_page",
                                          "url": "https://action-url-only.example",
                                          "sources": [{"url": "https://opened.example", "title": "Opened"}]},
                               "status": "completed"})
        run_dir, _ = make_run_dir(resp=resp)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(s["source_url_count"], 2)  # x.com/p + opened.example
        self.assertNotIn("action-url-only.example", s["source_domains"])

    def test_search_call_without_queries_warns(self):
        resp = _baseline_response()
        resp["output"][0]["action"] = {"type": "search", "sources": []}  # 没 queries
        run_dir, _ = make_run_dir(resp=resp)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(s["search_calls_without_queries"], 1)
        self.assertTrue(any("未暴露搜索词" in w for w in s["warnings"]))

    def test_queries_carry_call_id(self):
        resp = _baseline_response()
        resp["output"].append({"type": "web_search_call", "id": "ws_2",
                               "action": {"type": "search", "queries": ["c"], "sources": []},
                               "status": "completed"})
        run_dir, _ = make_run_dir(resp=resp)
        rows = json.loads((run_dir / "queries.json").read_text(encoding="utf-8"))
        by_id = {}
        for row in rows:
            by_id.setdefault(row["call_id"], []).append(row["query"])
        self.assertEqual(by_id["ws_1"], ["a", "b"])
        self.assertEqual(by_id["ws_2"], ["c"])

    def test_url_dedup_and_tracking_params(self):
        resp = _baseline_response()
        resp["output"][0]["action"]["sources"] = [
            {"url": "https://x.com/p", "title": "P"},
            {"url": "https://x.com/p", "title": "P dup"},
            {"url": "https://x.com/p?utm_source=a", "title": "P tracked"},
        ]
        run_dir, _ = make_run_dir(resp=resp)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(s["source_url_count"], 2)  # 按完整 URL 字符串去重

    def test_subdomains_kept_separate(self):
        resp = _baseline_response()
        resp["output"][0]["action"]["sources"] = [
            {"url": "https://news.x.com/p", "title": "a"},
            {"url": "https://www.news.x.com/p", "title": "b"},
        ]
        run_dir, _ = make_run_dir(resp=resp)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(s["source_domains"], ["news.x.com", "www.news.x.com"])


class SecurityAndEscape(unittest.TestCase):
    def test_url_in_text_does_not_become_active_link_with_quotes(self):
        run_dir, _ = make_run_dir()
        html = (run_dir / "report.html").read_text(encoding="utf-8")
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn('href="https://y"', html)
        self.assertIn("target=\"_blank\"", html)

    def test_html_escape_in_metadata(self):
        resp = _baseline_response()
        resp["model"] = "<img onerror=x>"
        run_dir, _ = make_run_dir(resp=resp)
        html = (run_dir / "report.html").read_text(encoding="utf-8")
        self.assertNotIn("<img onerror=x>", html)
        self.assertIn("&lt;img onerror=x&gt;", html)

    def test_csv_injection_escaped_for_spreadsheet(self):
        """具体断言到行——旧版用 all(... if startswith('=')) 是永真断言（all([])==True）。"""
        resp = _baseline_response()
        resp["output"][0]["action"]["sources"] = [
            {"url": "=cmd|'/c calc'!A1", "title": "=BAD()"},
            {"url": "https://ok.com", "title": "good"},
        ]
        run_dir, _ = make_run_dir(resp=resp)
        with (run_dir / "sources.csv").open(encoding="utf-8-sig", newline="") as f:
            rows = {r["url"]: r for r in csv.DictReader(f)}
        self.assertIn("'=cmd|'/c calc'!A1", rows)          # 该行 URL 被前置单引号
        self.assertEqual(rows["'=cmd|'/c calc'!A1"]["title"], "'=BAD()")
        self.assertIn("https://ok.com", rows)              # 正常 URL 不受影响

    def test_csv_special_characters_round_trip(self):
        resp = _baseline_response()
        resp["output"][0]["action"]["sources"] = [
            {"url": "https://x.com/a,b", "title": 'He said "hi"'},
            {"url": "https://x.com/nl", "title": "line1\nline2"},
        ]
        run_dir, _ = make_run_dir(resp=resp)
        with (run_dir / "sources.csv").open(encoding="utf-8-sig", newline="") as f:
            titles = {r["title"] for r in csv.DictReader(f)}
        self.assertIn('He said "hi"', titles)
        self.assertIn("line1\nline2", titles)

    def test_request_json_does_not_carry_api_key(self):
        run_dir, _ = make_run_dir()
        req = (run_dir / "request.json").read_text(encoding="utf-8")
        self.assertNotIn("OPENAI_API_KEY", req)
        self.assertNotIn("sk-", req)
        d = json.loads(req)
        self.assertIn("input", d)
        self.assertEqual(d["mode"], "offline")

    def test_request_json_has_no_absolute_path(self):
        """导入来源只记文件名，产物可安全分享。"""
        run_dir, _ = make_run_dir()
        d = json.loads((run_dir / "request.json").read_text(encoding="utf-8"))
        self.assertEqual(d["imported_from"], "raw.json")
        self.assertNotIn(str(Path.home()), json.dumps(d))

    def test_garbage_rejected(self):
        tmp = Path(tempfile.mkdtemp())
        bad = tmp / "bad.json"
        bad.write_text('{"not": "an output array"}', encoding="utf-8")
        out = tmp / "out"
        rc = run_fanout.main(["x", "--from-response", str(bad), "--output", str(out), "--no-model-overview"])
        self.assertEqual(rc, 1)


class MalformedInputRobustness(unittest.TestCase):
    """P0：畸形 --from-response 必须优雅退出（绝不裸抛 AttributeError/traceback）：
    能正常渲染的照常产出 report.html，其余以 rc=1 报错。"""

    def test_non_dict_output_item_fails_gracefully(self):
        for payload in ({"output": ["not-a-dict"]}, {"output": [None]}, {"output": [1]}):
            with self.subTest(payload=payload):
                rc, _ = _offline_run(payload)
                self.assertEqual(rc, 1)

    def test_malformed_nested_fields_do_not_crash(self):
        cases = [
            {"output": [{"type": "web_search_call", "id": "ws", "action": "search"}]},
            {"output": [{"type": "web_search_call", "id": "ws", "action": 123}]},
            {"output": [{"type": "web_search_call", "id": "ws",
                         "action": {"type": "search", "sources": ["x"]}}]},
            {"output": [{"type": "web_search_call", "id": "ws",
                         "action": {"type": "search", "queries": [1, 2]}}]},
            {"output": [{"type": "message", "id": "m", "content": ["x"]}]},
            {"output": [{"type": "message", "id": "m",
                         "content": [{"type": "output_text", "text": "t", "annotations": ["x"]}]}]},
            {"output": [{"type": "message", "id": "m",
                         "content": [{"type": "output_text", "text": 123}]}]},
            {"output": [{"type": "message", "id": "m",
                         "content": [{"type": "refusal", "refusal": {"a": 1}}]}]},
        ]
        for payload in cases:
            with self.subTest(payload=payload):
                rc, run_dir = _offline_run(payload)
                self.assertIn(rc, (0, 1))          # 优雅退出，而非 traceback
                self.assertIsNotNone(run_dir)      # 产物照常落盘
                # 关键：报告必须真的产出（旧断言只查 rc，会掩盖 render 阶段的崩溃）
                self.assertTrue((run_dir / "report.html").exists())

    def test_non_dict_action_still_renders_report(self):
        """action 为真值非 dict 时渲染不得崩溃，报告须照常产出。"""
        for action in ("search", 123, True, ["x"]):
            with self.subTest(action=action):
                rc, run_dir = _offline_run({"status": "completed", "output": [
                    {"type": "web_search_call", "id": "ws", "action": action}]})
                self.assertEqual(rc, 0)
                self.assertTrue((run_dir / "report.html").exists())

    def test_non_hashable_action_type_does_not_break_report(self):
        """action.type 非字符串（不可哈希）时，Counter 与 action_labels 都不得崩。"""
        rc, run_dir = _offline_run({"status": "completed", "output": [
            {"type": "web_search_call", "id": "ws",
             "action": {"type": ["x"], "queries": ["a"]}}]})
        self.assertEqual(rc, 0)
        self.assertTrue((run_dir / "report.html").exists())

    def test_non_string_call_id_does_not_break_report(self):
        """id 为不可哈希类型时，索引键归一化后报告仍须产出。"""
        payload = {"status": "completed", "output": [
            {"type": "web_search_call", "id": ["not", "hashable"],
             "action": {"type": "search", "queries": ["q"], "sources": []}},
            {"type": "message", "id": "m", "content": [{"type": "output_text", "text": "t"}]}]}
        rc, run_dir = _offline_run(payload)
        self.assertEqual(rc, 0)
        self.assertTrue((run_dir / "report.html").exists())

    def test_invalid_json_text_rejected(self):
        tmp = Path(tempfile.mkdtemp())
        bad = tmp / "bad.json"
        bad.write_text("{not valid json", encoding="utf-8")
        out = tmp / "out"
        rc = run_fanout.main(["x", "--from-response", str(bad), "--output", str(out), "--no-model-overview"])
        self.assertEqual(rc, 1)

    def test_empty_output_renders_placeholders(self):
        rc, run_dir = _offline_run({"status": "completed", "output": []})
        self.assertEqual(rc, 0)
        html = (run_dir / "report.html").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\{\{[A-Z_]+\}\}", html))  # 无残留占位符
        self.assertIn("没有暴露任何搜索词", html)
        self.assertIn("不含 Web 工具调用", html)


class TransportGuards(unittest.TestCase):
    def test_read_text_limited_enforces_cap(self):
        tmp = Path(tempfile.mkdtemp())
        f = tmp / "f.txt"
        f.write_text("x" * 100, encoding="utf-8")
        with self.assertRaises(ValueError):
            run_fanout.read_text_limited(f, limit=10)
        self.assertEqual(run_fanout.read_text_limited(f, limit=1000), "x" * 100)

    def test_redirect_is_refused(self):
        import urllib.error
        import urllib.request
        handler = run_fanout._NoRedirect()
        req = urllib.request.Request("https://api.openai.com/v1/responses", method="POST")
        with self.assertRaises(urllib.error.HTTPError):
            handler.redirect_request(req, None, 307, "Temporary Redirect", {},
                                     "https://evil.example")


class EnvParsing(unittest.TestCase):
    def test_inline_comment_and_quotes(self):
        tmp = Path(tempfile.mkdtemp())
        env = tmp / ".env"
        env.write_text(
            "OPENAI_API_KEY=sk-plain # prod\n"
            'OPENAI_MODEL="gpt-6.1-sol" # quoted\n'
            "PLAIN=abc#notcomment\n",
            encoding="utf-8")
        vals = run_fanout.load_env_file(env)
        self.assertEqual(vals["OPENAI_API_KEY"], "sk-plain")
        self.assertEqual(vals["OPENAI_MODEL"], "gpt-6.1-sol")
        self.assertEqual(vals["PLAIN"], "abc#notcomment")  # 无空格的 # 不当注释

    def test_empty_value_with_only_comment(self):
        tmp = Path(tempfile.mkdtemp())
        env = tmp / ".env"
        env.write_text("KEY= # only comment\nKEY2=#value\n", encoding="utf-8")
        vals = run_fanout.load_env_file(env)
        self.assertEqual(vals["KEY"], "")       # 等号后先空白再注释 → 空值
        self.assertEqual(vals["KEY2"], "#value")  # 等号后直接 # → 是值


class RefusalAndIncomplete(unittest.TestCase):
    def test_refusal_message_kept(self):
        resp = _baseline_response()
        resp["output"].append({"type": "message", "id": "msg_2",
                               "content": [{"type": "refusal", "refusal": "我拒绝"}]})
        run_dir, _ = make_run_dir(resp=resp)
        a = (run_dir / "answer.md").read_text(encoding="utf-8")
        self.assertIn("我拒绝", a)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertTrue(any("拒绝" in w for w in s["warnings"]))

    def test_incomplete_status_warns(self):
        resp = _baseline_response()
        resp["status"] = "incomplete"
        resp["incomplete_details"] = {"reason": "max_output_tokens"}
        run_dir, _ = make_run_dir(resp=resp, expect_rc=1)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(s["status"], "incomplete")
        self.assertTrue(any("incomplete" in w or "不完整" in w for w in s["warnings"]))

    def test_failed_status_warns_and_rc1(self):
        resp = _baseline_response()
        resp["status"] = "failed"
        run_dir, _ = make_run_dir(resp=resp, expect_rc=1)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertTrue(any("failed" in w for w in s["warnings"]))


class OnlineOverviewPath(unittest.TestCase):
    """在线概览路径：成功要把概览文本渲进 report.html（Critical #1 的回归锁）。"""

    def _run_online(self, resp, overview_text=None, overview_raises=False):
        tmp = Path(tempfile.mkdtemp(prefix="fanout-online-"))
        out = tmp / "out"
        os.environ["OPENAI_API_KEY"] = "sk-fake"
        orig_post, orig_ov = run_fanout._post, run_fanout.generate_overview
        state = {"n": 0}

        def fake_post(key, body, timeout):
            state["n"] += 1
            if state["n"] == 1:
                return json.dumps(resp)
            return json.dumps({"output": [{"type": "message", "id": "m2", "content": [
                {"type": "output_text", "text": overview_text or ""}]}]})

        run_fanout._post = fake_post
        if overview_raises:
            def boom(*a, **k):
                raise RuntimeError("boom")
            run_fanout.generate_overview = boom
        try:
            rc = run_fanout.main(["q", "--output", str(out)])
        finally:
            run_fanout._post, run_fanout.generate_overview = orig_post, orig_ov
            os.environ.pop("OPENAI_API_KEY", None)
        run_dir = list(out.iterdir())[0]
        return rc, run_dir

    def test_overview_success_appears_in_report_html(self):
        rc, run_dir = self._run_online(_baseline_response(), overview_text="这是模型概览正文")
        self.assertEqual(rc, 0)
        html = (run_dir / "report.html").read_text(encoding="utf-8")
        self.assertIn("这是模型概览正文", html)
        self.assertNotIn("本次运行未生成模型概览", html)
        self.assertTrue((run_dir / "overview.md").exists())
        # 概览必须被明确标为"模型生成、仅作参考"（提示注入的最后一环）
        self.assertIn("模型生成 · 仅作参考", html)
        self.assertIn("不是确定性结论", html)

    def test_online_request_json_carries_no_key(self):
        """在线路径的 request.json 也不得含 Key（原用例只覆盖离线，是同义反复）。"""
        _, run_dir = self._run_online(_baseline_response(), overview_text="概览")
        req = (run_dir / "request.json").read_text(encoding="utf-8")
        self.assertNotIn("sk-fake", req)
        self.assertNotIn("Bearer", req)
        self.assertNotIn("Authorization", req)
        self.assertEqual(json.loads(req)["request"]["model"], "gpt-6.1-sol")

    def test_overview_failure_warning_reaches_report_html(self):
        rc, run_dir = self._run_online(_baseline_response(), overview_raises=True)
        self.assertEqual(rc, 1)
        html = (run_dir / "report.html").read_text(encoding="utf-8")
        self.assertIn("概览失败", html)
        s = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertTrue(any("概览失败" in w for w in s["warnings"]))


if __name__ == "__main__":
    unittest.main()
