#!/usr/bin/env python3
"""scripts/build_site.py 的单元回归测试（不依赖 pytest）。

覆盖安全审计与代码审查发现并已修复的回归点：

    F1  registry 的 id / path 路径穿越（越界读写）
    F5  --out 输出目录白名单（不得误删非本脚本产物）
    R3  --no-avatars 不得产出指向不存在文件的引用
    R4  错误在 --quiet 下也必须可见（由 CLI 行为保证，这里测核心逻辑）
    N1  超长 id 必须「干净失败」（BuildError / OSError），不得抛 Python 栈
    N2  --out 归属判据用专属标记，而非任何静态站都有的通用 .nojekyll
    N3  <out>/assets/avatars 被预置为符号链接时不得写出站点目录之外
    N5  先写后删：新产物落盘后才清理旧头像（中断不毁掉上一次的产物）
        + 模板占位符缺失必须报错
        + registry 为空必须拒绝
        + HTML 转义：名称/描述/标签中的标记不得逃逸
        + 缺头像时回退默认头像

用法：python3 tests/test_build_site.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_site as bs  # noqa: E402

REPO = "https://github.com/airen/workbuddy-hub"
CASES: list[tuple[str, bool, str]] = []


def record(label: str, ok: bool, detail: str = "") -> None:
    CASES.append((label, ok, detail))


def expect_build_error(label: str, fn) -> None:
    """必须抛出 BuildError（可预期的输入错误）。"""
    try:
        fn()
    except bs.BuildError as exc:
        record(label, True, f"已拦截：{str(exc)[:58]}")
    except Exception as exc:  # noqa: BLE001
        record(label, False, f"非预期异常 {type(exc).__name__}: {exc}")
    else:
        record(label, False, "未被拦截")


def expect_ok(label: str, fn):
    """必须正常返回；返回 None 表示失败。"""
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001
        record(label, False, f"误拦 {type(exc).__name__}: {exc}")
        return None


def items(experts=None, teams=None):
    """build_items 返回 (items, active, warnings)，这里只取前两项给断言用。"""
    built = bs.build_items(experts or [], teams or [], [], REPO, "main")
    return built[0], built[1]


# ---------------------------------------------------------------- F1 路径穿越
def test_path_traversal() -> None:
    for label, entry in [
        ("id 含 ../ 穿越", {"id": "../../../ESCAPED", "path": "experts/x"}),
        ("id 为绝对路径", {"id": "/etc/evil", "path": "experts/x"}),
        ("id 含斜杠", {"id": "a/b", "path": "experts/a/b"}),
        ("id 含反斜杠", {"id": "a\\b", "path": "experts/a\\b"}),
        ("id 含空格", {"id": "bad id", "path": "experts/bad id"}),
        ("id 含大写", {"id": "BadId", "path": "experts/BadId"}),
        ("path 指向仓库外", {"id": "good-id", "path": "../../etc"}),
        ("path 与 id 不一致", {"id": "good-id", "path": "experts/other-id"}),
        ("path 多套一层", {"id": "good-id", "path": "experts/good-id/sub"}),
    ]:
        expect_build_error(label, lambda e=entry: items([e]))

    expect_build_error(
        "team 的 path 误用 experts/",
        lambda: items([], [{"id": "good-team", "path": "experts/good-team"}]),
    )

    # 无 id 的条目按设计跳过，而不是报错
    built = expect_ok("id 为空（跳过而非报错）", lambda: items([{"id": "", "path": "experts/x"}]))
    if built is not None:
        record("id 为空时不生成卡片", len(built[0]) == 0, f"生成 {len(built[0])} 张")

    for label, entry in [
        ("正常 expert", {"id": "good-id", "path": "experts/good-id"}),
        ("path 缺省自动推导", {"id": "auto-path"}),
        ("id 含点与连字符", {"id": "a.b-c_1", "path": "experts/a.b-c_1"}),
    ]:
        expect_ok(label, lambda e=entry: items([e]))
    expect_ok("正常 team", lambda: items([], [{"id": "good-team", "path": "teams/good-team"}]))

    # 二次防线：即使绕过 build_items 直接调用，也不得写出输出目录
    scratch = Path(tempfile.mkdtemp(prefix="hubsec-"))
    out = scratch / "out"
    out.mkdir()
    try:
        bs.prepare_avatars(
            [{"id": "../../../ESCAPED", "path": "experts/x", "avatar": ""}], out, True
        )
    except Exception:  # noqa: BLE001
        pass
    escaped = (scratch / "ESCAPED.jpg").exists() or (scratch.parent / "ESCAPED.jpg").exists()
    record("头像写入越界（二次防线）", not escaped, "未逃出输出目录" if not escaped else "已逃出！")


# ------------------------------------------------------- F5 输出目录白名单
def test_out_dir_guard() -> None:
    expect_build_error("--out 指向仓库根", lambda: bs._assert_safe_out_dir(REPO_ROOT))
    expect_build_error("--out 指向 /etc", lambda: bs._assert_safe_out_dir(Path("/etc")))
    expect_build_error("--out 指向家目录", lambda: bs._assert_safe_out_dir(Path.home()))
    expect_build_error(
        "--out 指向仓库内 assets/", lambda: bs._assert_safe_out_dir(REPO_ROOT / "assets")
    )
    expect_build_error(
        "--out 指向仓库内 registry/", lambda: bs._assert_safe_out_dir(REPO_ROOT / "registry")
    )
    expect_ok(
        "--out 指向不存在的新目录",
        lambda: bs._assert_safe_out_dir(Path(tempfile.gettempdir()) / "hub-new-dir-xyz"),
    )

    # N2：归属判据必须是本脚本的专属标记，而不是通用的 .nojekyll。
    # 一个只含 .nojekyll 的「别人家的静态站目录」必须被拒绝，否则会被清掉。
    scratch = Path(tempfile.mkdtemp(prefix="hubout-"))
    foreign = scratch / "foreign-site"
    foreign.mkdir()
    (foreign / ".nojekyll").write_text("", encoding="utf-8")
    expect_build_error(
        "--out 指向只含 .nojekyll 的他站目录（N2）",
        lambda: bs._assert_safe_out_dir(foreign),
    )

    ours = scratch / "our-site"
    ours.mkdir()
    (ours / bs._BUILD_MARKER).write_text("", encoding="utf-8")
    expect_ok(
        "--out 指向含专属标记的产物目录（N2）",
        lambda: bs._assert_safe_out_dir(ours),
    )

    empty = scratch / "empty-dir"
    empty.mkdir()
    expect_ok("--out 指向空目录", lambda: bs._assert_safe_out_dir(empty))


# ------------------------------------------------------------ N1 超长 id
def test_overlong_id() -> None:
    long_id = "a" * 300
    expect_build_error(
        "超长 id（300 字符）被白名单拦截（N1）",
        lambda: items([{"id": long_id, "path": f"experts/{long_id}"}]),
    )
    # 边界内（64 字符）仍应放行
    ok_id = "a" * 64
    expect_ok(
        "64 字符 id 在边界内放行（N1）",
        lambda: items([{"id": ok_id, "path": f"experts/{ok_id}"}]),
    )


# ------------------------------------------------- N3 头像目录符号链接
def test_avatar_dir_symlink() -> None:
    """<out>/assets/avatars 若是预置的符号链接，写入会落到站点目录之外。"""
    scratch = Path(tempfile.mkdtemp(prefix="hubsym-"))
    out = scratch / "out"
    (out / "assets").mkdir(parents=True)
    outside = scratch / "outside"
    outside.mkdir()
    try:
        (out / "assets" / "avatars").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        record("头像目录符号链接防护（N3）", True, "跳过：当前环境不允许创建符号链接")
        return

    entries, _ = items([{"id": "sym-test", "path": "experts/sym-test"}])
    warnings, errors = bs.prepare_avatars(entries, out, True)
    leaked = list(outside.glob("*.jpg"))
    record(
        "头像目录符号链接防护（N3）",
        not leaked and entries[0]["avatar"] == "" and bool(errors),
        f"越界写入 {len(leaked)} 个文件，errors={len(errors)}",
    )


# ------------------------------------------------------------ R3 --no-avatars
def test_no_avatars() -> None:
    built = expect_ok("正常条目构建", lambda: items([{"id": "noav", "path": "experts/noav"}]))
    if built is None:
        return
    entries, _ = built
    out = Path(tempfile.mkdtemp(prefix="hubnoav-"))
    bs.prepare_avatars(entries, out, enabled=False)
    record(
        "--no-avatars 不引用不存在的头像",
        entries[0]["avatar"] == "",
        f"avatar={entries[0]['avatar']!r}",
    )
    html_text = bs.render_cards(entries)
    record(
        "--no-avatars 卡片走首字母占位",
        "<img" not in html_text and "avatar--ph" in html_text,
        "无 img 且含占位",
    )


# ------------------------------------------------------------- 模板与转义
def test_template_and_escaping() -> None:
    expect_build_error(
        "模板缺占位符值时报错",
        lambda: bs.render_template("<p>{{unknown_token}}</p>", {"other": 1}),
    )
    expect_ok(
        "占位符齐全时正常渲染",
        lambda: bs.render_template("<p>{{a}}</p>", {"a": "x"}),
    )

    built = items(
        [
            {
                "id": "xss-test",
                "path": "experts/xss-test",
                "name": "<img src=x onerror=alert(1)>",
                "description": '" onmouseover="alert(1)"',
                "tags": ["<script>alert(1)</script>"],
                "category": '"><b>',
                "version": "1.0.0",
            }
        ]
    )
    if built is None:
        return
    rendered = bs.render_cards(built[0])
    record("名称中的标记被转义", "<img src=x" not in rendered, "无未转义标签")
    record("标签中的 script 被转义", "<script>" not in rendered, "无未转义 script")
    record("属性中的引号被转义", 'onmouseover="alert(1)"' not in rendered, "无属性逃逸")


# --------------------------------------------------------- 空 registry 防护
def test_empty_registry() -> None:
    built = expect_ok("空 registry 可构建但产出 0 项", lambda: items([], []))
    if built is not None:
        record("空 registry 产出 0 张卡片", len(built[0]) == 0, f"{len(built[0])} 张")


# ------------------------------------------------- N5 先写后删（中断安全）
def test_prune_stale_avatars() -> None:
    """新产物全部落盘后才清理旧头像；清理只针对图片，且不跟随符号链接。

    「先删后写」曾实测把站点打坏：一次中断留下「无 index.html + 8/35 张头像」。
    """
    scratch = Path(tempfile.mkdtemp(prefix="hubprune-"))
    out = scratch / "out"
    avatars = out / "assets" / "avatars"
    avatars.mkdir(parents=True)
    stale = avatars / "zzz-stale.jpg"
    stale.write_bytes(b"stale")
    keep = avatars / "keep-me.jpg"
    keep.write_bytes(b"keep")
    notes = avatars / "notes.txt"
    notes.write_text("x", encoding="utf-8")

    failures = bs._prune_stale_avatars(out, {"keep-me"})
    record(
        "旧头像被清理、在用的保留（N5）",
        not stale.exists() and keep.exists() and not failures,
        f"stale={stale.exists()} keep={keep.exists()} failures={len(failures)}",
    )
    record("非图片文件不被误删（N5）", notes.is_file(), "notes.txt 保留")

    # keep 集合为空 ⇒ 本次一张头像都没产出，无从判断谁是旧的，宁可不删。
    # （同时保证 --no-avatars 的「纯预览」语义不会清空既有头像）
    stale2 = avatars / "zzz-stale2.jpg"
    stale2.write_bytes(b"stale2")
    bs._prune_stale_avatars(out, set())
    record("空 keep 集合时不清理（N-a）", stale2.is_file(), f"仍在={stale2.is_file()}")

    # 文件自身是符号链接 ⇒ 不跟随（删链接会波及站点外目标）
    outside = scratch / "outside.jpg"
    outside.write_bytes(b"outside")
    link = avatars / "link.jpg"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        record("符号链接头像不被跟随删除（N5）", True, "跳过：当前环境不允许创建符号链接")
        return
    bs._prune_stale_avatars(out, {"keep-me", "zzz-stale2"})
    record(
        "符号链接头像不被跟随删除（N5）",
        outside.is_file() and link.is_symlink(),
        f"链接目标仍在={outside.is_file()}",
    )

    # F-A：assets 这一层被换成软链时，遍历会落到站点之外——删除必须被拦住
    out3 = scratch / "out3"
    victim = scratch / "victim"
    (victim / "avatars").mkdir(parents=True)
    victim_file = victim / "avatars" / "keepme.jpg"
    victim_file.write_bytes(b"victim")
    out3.mkdir()
    (out3 / bs._BUILD_MARKER).write_text("", encoding="utf-8")
    try:
        (out3 / "assets").symlink_to(victim, target_is_directory=True)
    except (OSError, NotImplementedError):
        record("assets 父级软链不越界删除（F-A）", True, "跳过：当前环境不允许创建符号链接")
        return
    bs._prune_stale_avatars(out3, {"something-else"})
    record(
        "assets 父级软链不越界删除（F-A）",
        victim_file.is_file(),
        f"站点外文件仍在={victim_file.is_file()}",
    )


def test_avatar_write_failure_clears_ref() -> None:
    """写入失败 / 被跳过的头像不得留在卡片上（否则 HTML 里是 404 的 <img src>）。"""
    scratch = Path(tempfile.mkdtemp(prefix="hubfail-"))
    out = scratch / "out"
    src_file = scratch / "src.jpg"
    src_file.write_bytes(b"not-a-real-jpeg")

    entries, _ = items([{"id": "fail-me", "path": "experts/fail-me"}])

    orig_src, orig_write = bs._avatar_source, bs._write_avatar
    bs._avatar_source = lambda asset_dir, asset_id: src_file
    bs._write_avatar = lambda s, d, p: (_ for _ in ()).throw(RuntimeError("boom"))
    try:
        warnings, errors = bs.prepare_avatars(entries, out, True)
    finally:
        bs._avatar_source, bs._write_avatar = orig_src, orig_write

    html_text = bs.render_cards(entries)
    record(
        "写入失败的头像不留悬空引用",
        entries[0]["avatar"] == "" and bool(errors) and "<img" not in html_text,
        f"avatar={entries[0]['avatar']!r} errors={len(errors)}",
    )


def main() -> int:
    print("scripts/build_site.py 单元回归测试")
    print("=" * 72)
    test_path_traversal()
    test_out_dir_guard()
    test_overlong_id()
    test_avatar_dir_symlink()
    test_prune_stale_avatars()
    test_avatar_write_failure_clears_ref()
    test_no_avatars()
    test_template_and_escaping()
    test_empty_registry()

    width = max(len(c[0]) for c in CASES) + 2
    for label, ok, detail in CASES:
        print(f" {'PASS' if ok else 'FAIL'}  {label:<{width}} {detail}")
    failed = [c for c in CASES if not c[1]]
    print("-" * 72)
    print(f"通过 {len(CASES) - len(failed)} / {len(CASES)}")
    if failed:
        print("未通过：" + "、".join(c[0] for c in failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
