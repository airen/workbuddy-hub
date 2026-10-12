#!/usr/bin/env python3
"""AI 味自检：机械统计表层信号 + 启发式标记结构信号。

零依赖（仅标准库）。配合 de-ai-rewrite skill 使用。

用法
----
    python3 ai_tell_check.py 稿子.txt                          # 单篇体检
    python3 ai_tell_check.py --before 原文.txt --after 改后.txt # 改前改后对比 + 裁决
    python3 ai_tell_check.py --before 原 --after 改 --facts "186000,11,8 小时"
    python3 ai_tell_check.py 稿子.txt --json
    cat 稿子.txt | python3 ai_tell_check.py -

它数得清词、破折号、模板短语，也能标出结尾总结句、`不是…而是…`、
枚举推进、段落整齐度、模糊归因等结构信号，并对 --facts 给出的
数字/专名做保留检查。

**它读不懂语义。** 结构层的最终判断仍由改写者负责——这个脚本只是
把「改前改后到底动了什么」变成可核对的数字，防止「只换词不动结构」
被当成完成任务。

裁决的四种结果：
    ✅ 结构层确实动了
    ❌ 只动了表层（假去味）
    ⚪ 原文与改后都没有可机械识别的结构特征（no-op 合法）
    🔴 改写新增了结构 AI 味（越改越糟）
    ⚠️ 只改掉一部分，仍有残留（未达标）
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

MAX_BYTES = 5_000_000

# ---------------------------------------------------------------- 词表

# 中文 AI 高频词 / 模板短语（surface 层）
ZH_TELLS = [
    "值得注意的是", "值得一提的是", "总而言之", "综上所述", "归根结底", "总的来说",
    "在当今", "随着", "不仅", "更是", "赋能", "助力", "打造", "至关重要", "不可或缺",
    "毋庸置疑", "让我们", "首先", "其次", "再次", "最后", "深入", "全方位", "一站式",
    "凸显", "彰显", "展现", "体现", "反映了", "见证了", "勾勒", "描绘出",
    "在某种程度上", "在一定程度上", "从某种意义上", "众所周知",
]

# 英文 AI 高频词（surface 层）——用词干正则，覆盖 leveraging / fostered / delves 等变形
EN_TELL_PATTERNS = [
    (r"\bdelv\w*", "delve"), (r"\btapestr\w*", "tapestry"), (r"\btestament\w*", "testament"),
    (r"\bnavigat\w*", "navigate"), (r"\blandscap\w*", "landscape"), (r"\bcrucial\w*", "crucial"),
    (r"\bvital\w*", "vital"), (r"\brobust\w*", "robust"), (r"\bseamless\w*", "seamless"),
    (r"\bleverag\w*", "leverage"), (r"\bfoster\w*", "foster"), (r"\brealm\w*", "realm"),
    (r"\bembark\w*", "embark"), (r"\bbeacon\w*", "beacon"), (r"\bsymphon\w*", "symphony"),
    (r"\bintricat\w*", "intricate"), (r"\bpivotal\w*", "pivotal"),
    (r"\bever-evolving\b", "ever-evolving"), (r"\bin today'?s\b", "in today's"),
    (r"\bmoreover\b", "moreover"), (r"\bfurthermore\b", "furthermore"),
    (r"\bultimately\b", "ultimately"), (r"\bnot just\b", "not just"),
    (r"\bmore than just\b", "more than just"),
    (r"\bit'?s important to note\b", "it's important to note"),
]

# 模糊归因（vague_references 的信号）
VAGUE_ATTR = [
    "专家认为", "专家指出", "业内人士", "业内专家", "多项研究", "研究表明", "研究显示",
    "很多公司", "许多人", "有些人", "有人认为", "不少人", "相关部门", "有关方面",
    "普遍认为", "广泛认为", "一些机构", "某公司", "某个",
]

# 「讲明道理」——强信号：出现即算，不分位置
# 注意「让X明白」要覆盖他/她/人/我们：skill 自己的 §1 示例用的就是「让他明白」，
# 漏掉它会让门禁认不出自己校准用的招牌示例。
MORAL_STRONG = [
    "这告诉我们", "由此可见", "归根结底", "让人明白", "让我们明白", "让他明白",
    "让她明白", "使他明白", "使她明白", "使人明白", "这启示我们",
    "说到底", "意义在于", "价值在于", "道理很简单", "这也说明",
]
# 「讲明道理」——弱信号：只有在段落末句出现、且该段至少两句时才计入。
# 不含「真正的」：它是日常高频词，作为信号会产生可复现的误判（只删一个词就被判"改掉了道理"）。
MORAL_WEAK_TAIL = ["这就是", "关键在于", "本质上", "其实质是", "我们应该", "我们要懂得"]

# 「整齐收尾」——分强弱。判定范围：文末最后 2 句。
# 强信号：本身就是收束词，落在末 2 句即算。
# 注意不要同时收「一切都有了回报」和「有了回报」——后者是前者的子串，会同一句双计。
TIDY_STRONG = [
    "圆满", "如愿", "有了回报", "皆大欢喜", "尘埃落定", "画上句号",
    "未来可期", "充满希望", "值得期待", "更加美好", "一定会",
    "总而言之", "综上所述", "总的来说", "总之", "综上", "归根结底",
]
# 弱信号：日常副词/短语，单独出现不是收尾信号（"终于等到雨停"是叙事，不是收束）。
# 只有落在**最后一句**才算，避免把「正确打开了结尾」的好稿冤枉成未达标。
TIDY_WEAK = ["终于", "从此", "有了答案", "新的开始", "越来越好"]

# 序列词（枚举式推进）——必须带标点边界，且同段内出现 ≥2 个才算
SEQ_WORDS = ["首先", "其次", "再次", "最后", "第一", "第二", "第三", "其一", "其二", "其三"]

# 反退化信号：改写不该新增的连接词/过渡词（只统计句首位置）
DEGRADE_OPENERS = ["然而", "于是", "与此同时", "此外", "因此", "所以", "另外", "而且",
                   "nonetheless", "moreover", "furthermore", "meanwhile", "however"]

SENT_END = re.compile(r"[。！？!?；;\n]+")
CJK = re.compile(r"[\u4e00-\u9fff]")
QUOTED = re.compile(r"[「『“\"][^」』”\"]*[」』”\"]")


# ---------------------------------------------------------------- 工具


def read_text(path: str, max_bytes: int = MAX_BYTES) -> str:
    if path == "-":
        return sys.stdin.read()
    p = Path(path)
    if p.is_dir():
        raise SystemExit(f"[错误] {path} 是目录，不是文件。本脚本只接受文本文件。")
    if not p.is_file():
        raise SystemExit(f"[错误] 找不到文件：{path}")
    # 拒绝符号链接：避免「注释说加固、代码其实跟随链接」的名不副实
    if p.is_symlink():
        raise SystemExit(f"[错误] {path} 是符号链接；出于路径安全考虑拒绝读取。")
    if p.stat().st_size > max_bytes:
        raise SystemExit(f"[错误] {path} 超过 {max_bytes} 字节上限；用 --max-bytes 放宽。")
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def sentences(text: str) -> list[str]:
    return [s for s in (x.strip() for x in SENT_END.split(text)) if s]


def count_literals(text: str, words: list[str]) -> tuple[int, list[str]]:
    total, hits = 0, []
    for w in words:
        n = text.count(w)
        if n:
            total += n
            hits.append(f"{w}×{n}")
    return total, hits


def count_en(text: str) -> tuple[int, list[str]]:
    total, hits = 0, []
    for pat, label in EN_TELL_PATTERNS:
        n = len(re.findall(pat, text, re.I))
        if n:
            total += n
            hits.append(f"{label}×{n}")
    return total, hits


def count_openers(text: str) -> tuple[int, list[str]]:
    """只统计句首位置的连接词/过渡词（原文句中的「所以」不算新增信号）。"""
    total, hits = 0, []
    for w in DEGRADE_OPENERS:
        if CJK.search(w):
            n = len(re.findall(r"(?:^|[。！？；\n])\s*" + re.escape(w), text))
        else:
            n = len(re.findall(r"(?:^|[.!?;\n])\s*" + re.escape(w) + r"\b", text, re.I))
        if n:
            total += n
            hits.append(f"{w}×{n}")
    return total, hits


def count_reader(text: str) -> int:
    """读者称呼。剔掉引号内对话（那是人物之间的「你」），并排除「迷你」这类假命中。"""
    stripped = QUOTED.sub("", text)
    stripped = stripped.replace("迷你", "")
    zh = len(re.findall(r"[你您]", stripped))
    en = len(re.findall(r"\byou\b", stripped, re.I))
    return zh + en


def find_moral(paras: list[str]) -> tuple[int, list[str]]:
    strong, weak, hits = 0, 0, []
    for p in paras:
        for w in MORAL_STRONG:
            n = p.count(w)
            if n:
                strong += n
                hits.append(f"{w}×{n}")
        sents = sentences(p)
        # 弱信号只在「段落至少两句、且命中在末句」时才算——否则单句成段时任何日常词都会命中
        if len(sents) >= 2:
            tail = sents[-1]
            for w in MORAL_WEAK_TAIL:
                if w in tail:
                    weak += 1
                    hits.append(f"{w}×1(段末)")
    return strong + weak, hits


def find_tidy(text: str) -> tuple[int, list[str]]:
    """文末收束信号：强信号看末 2 句，弱信号只看最后一句。"""
    paras = paragraphs(text)
    if not paras:
        return 0, []
    sents = sentences(paras[-1]) or [paras[-1]]
    tail2 = "".join(sents[-2:])
    tail1 = sents[-1]
    n_strong, h_strong = count_literals(tail2, TIDY_STRONG)
    n_weak, h_weak = count_literals(tail1, TIDY_WEAK)
    return n_strong + n_weak, h_strong + h_weak


def find_enumeration(text: str) -> tuple[int, int, list[str]]:
    """返回（编号清单条数, 含≥2个序列词的段落数, 命中词）。"""
    numbered = len(re.findall(r"(?m)^\s*(?:\d+[.、)]|[一二三四五六七八九十]+[、.])", text))
    seq_paras, hits = 0, []
    for p in paragraphs(text):
        found = []
        for w in SEQ_WORDS:
            if re.search(r"(?:^|[。！？；\n])\s*" + re.escape(w) + r"\s*[，、：,:]", p):
                found.append(w)
        if len(found) >= 2:
            seq_paras += 1
            hits.extend(f"{w}×1" for w in found)
    return numbered, seq_paras, hits


def cv(values: list[float]) -> float:
    """变异系数：标准差/均值。越小越整齐（越像 AI）。"""
    if len(values) < 2:
        return 0.0
    m = statistics.mean(values)
    return (statistics.stdev(values) / m) if m else 0.0


# ---------------------------------------------------------------- 体检


def analyze(text: str) -> dict:
    paras = paragraphs(text)
    sents = sentences(text)
    last = paras[-1] if paras else ""

    zh_n, zh_hits = count_literals(text, ZH_TELLS)
    en_n, en_hits = count_en(text)
    vague_n, vague_hits = count_literals(text, VAGUE_ATTR)
    moral_n, moral_hits = find_moral(paras)
    tidy_n, tidy_hits = find_tidy(text)
    enum_n, seq_n, seq_hits = find_enumeration(text)
    degrade_n, degrade_hits = count_openers(text)

    plens = [len(p) for p in paras]
    slens = [len(s) for s in sents]

    contrast = len(re.findall(r"不是[^。！？\n]{0,30}?而是", text)) + \
               len(re.findall(r"并非[^。！？\n]{0,30}?而是", text))

    reader = count_reader(text)
    # 单个 —（非 ——）再分语境：紧邻中文的，多半是漏打了一个破折号的规范标点，不计入表层分；
    # 只有处在拉丁语境里的才是英文式 AI 破折号。
    lone = list(re.finditer(r"(?<!—)—(?!—)", text))
    em_dashes_cjk = sum(
        1 for m in lone
        if (m.start() > 0 and CJK.match(text[m.start() - 1]))
        or (m.end() < len(text) and CJK.match(text[m.end()]))
    )
    em_dashes = len(lone) - em_dashes_cjk
    zh_dashes = len(re.findall(r"——", text))

    return {
        "empty": not text.strip(),
        "surface": {
            "zh_tells": zh_n, "zh_hits": zh_hits,
            "en_tells": en_n, "en_hits": en_hits,
            "em_dashes": em_dashes, "em_dashes_cjk": em_dashes_cjk, "zh_dashes": zh_dashes,
            "total": zh_n + en_n + em_dashes,
        },
        "structure": {
            "stated_theme": {"count": moral_n, "hits": moral_hits[:6], "flag": moral_n > 0},
            "tidy_ending": {"count": tidy_n, "hits": tidy_hits[:6], "flag": tidy_n > 0},
            "vague_references": {"count": vague_n, "hits": vague_hits[:6], "flag": vague_n > 0},
            "single_track": {"numbered": enum_n, "seq_paragraphs": seq_n,
                             "contrast_pairs": contrast, "hits": seq_hits[:6],
                             "flag": enum_n > 0 or seq_n > 0 or contrast > 0},
            "no_reader_address": {"reader_words": reader, "flag": reader == 0,
                                  "informational": True},
            "flat_paragraphs": {"paragraphs": len(paras), "lengths": plens,
                                "cv": round(cv(plens), 3),
                                "flag": len(paras) >= 4 and cv(plens) < 0.20},
        },
        "degrade_risk": {"count": degrade_n, "hits": degrade_hits[:8]},
        "rhythm": {
            "sentences": len(sents),
            "avg_sentence_len": round(statistics.mean(slens), 1) if slens else 0,
            "sentence_len_cv": round(cv(slens), 3),
            "flag": len(sents) >= 4 and cv(slens) < 0.30,
        },
        "last_sentence": last[-40:] if last else "",
    }


def _fact_present(fact: str, text: str) -> bool:
    """数字按边界匹配——否则 `--facts "100"` 会把改后的 `1000` 误判为「保留」。

    边界不对称是有意的：左侧排除 `[\\d.,]`，右侧只排除 `[\\d]`。因为英文句末句点
    （`amount 100.`）若也算边界，会造成假「丢失」。小数延伸（`100` → `100.5`）单独处理：
    只有当**所有**命中都紧跟 `.<数字>` 时才判为「已变更」。
    """
    if fact.isdigit():
        for m in re.finditer(r"(?<![\d.,])" + re.escape(fact) + r"(?![\d])", text):
            if not re.match(r"\.\d", text[m.end():]):
                return True
        return False
    if re.match(r"^\d", fact):
        return re.search(r"(?<![\d.,])" + re.escape(fact), text) is not None
    return fact in text


def check_facts(facts: list[str], before: str, after: str) -> list[dict]:
    out = []
    for f in facts:
        f = f.strip()
        if not f:
            continue
        out.append({"fact": f,
                    "in_before": _fact_present(f, before),
                    "in_after": _fact_present(f, after)})
    return out


# ---------------------------------------------------------------- 输出


def bar(flag: bool) -> str:
    return "🔴 有" if flag else "🟢 无"


def render(label: str, r: dict) -> str:
    if r["empty"]:
        return f"=== {label} ===\n  （空输入）"
    s, st, d, rh = r["surface"], r["structure"], r["degrade_risk"], r["rhythm"]
    lines = [
        f"=== {label} ===",
        "",
        "[L1 表层]",
        f"  中文 AI 词 {s['zh_tells']} 处" + (f"  ({', '.join(s['zh_hits'])})" if s["zh_hits"] else ""),
        f"  英文 AI 词 {s['en_tells']} 处" + (f"  ({', '.join(s['en_hits'])})" if s["en_hits"] else ""),
        f"  英文破折号 —  {s['em_dashes']} 个"
        + f"（中文 —— 另计 {s['zh_dashes']} 个；紧邻中文的单个 — 另计 {s['em_dashes_cjk']} 个，均属中文标点范畴，未计分）",
        "",
        "[L3 结构层]",
        f"  讲明道理     {bar(st['stated_theme']['flag'])}  {st['stated_theme']['count']} 处"
        + (f"  ({', '.join(st['stated_theme']['hits'])})" if st["stated_theme"]["hits"] else ""),
        f"  整齐收尾     {bar(st['tidy_ending']['flag'])}  {st['tidy_ending']['count']} 处"
        + (f"  ({', '.join(st['tidy_ending']['hits'])})" if st["tidy_ending"]["hits"] else ""),
        f"  泛指不点名   {bar(st['vague_references']['flag'])}  {st['vague_references']['count']} 处"
        + (f"  ({', '.join(st['vague_references']['hits'])})" if st["vague_references"]["hits"] else ""),
        f"  单线推进     {bar(st['single_track']['flag'])}  编号 {st['single_track']['numbered']} 条"
        f"，序列段 {st['single_track']['seq_paragraphs']} 个，对比句 {st['single_track']['contrast_pairs']} 处",
        f"  段落整齐度   {bar(st['flat_paragraphs']['flag'])}  {st['flat_paragraphs']['paragraphs']} 段，"
        f"CV={st['flat_paragraphs']['cv']}（≥4 段且 CV<0.20 才算）",
        f"  不对话读者   {st['no_reader_address']['reader_words']} 次「你/您/you」"
        f"（仅参考，不参与裁决；说明文/公文可忽略）",
        "",
        "[节奏]",
        f"  句长参差     {'🟢 参差' if not rh['flag'] else '🔴 单调'}  "
        f"{rh['sentences']} 句，均长 {rh['avg_sentence_len']} 字，CV={rh['sentence_len_cv']}",
        "",
        "[反退化检查：句首连接词/过渡词]",
        f"  {d['count']} 处" + (f"  ({', '.join(d['hits'])})" if d["hits"] else "")
        + "（单篇仅供参考，需与改前对比看增量）",
    ]
    return "\n".join(lines)


# 参与裁决的结构特征（no_reader_address 文体相关，排除在外）
FEATURES = [
    ("stated_theme", "讲明道理"),
    ("tidy_ending", "整齐收尾"),
    ("vague_references", "泛指不点名"),
    ("single_track", "单线推进"),
    ("flat_paragraphs", "段落整齐"),
]


def verdict(before: dict, after: dict, facts: list[dict] | None = None) -> str:
    """给出「到底动没动结构」的裁决——这是本脚本存在的理由。"""
    if before["empty"] or after["empty"]:
        return "\n=== 裁决 ===\n  输入为空，无法裁决。"

    b = {k: before["structure"][k]["flag"] for k, _ in FEATURES}
    a = {k: after["structure"][k]["flag"] for k, _ in FEATURES}
    improved = [n for k, n in FEATURES if b[k] and not a[k]]
    residue = [n for k, n in FEATURES if b[k] and a[k]]
    newly = [n for k, n in FEATURES if not b[k] and a[k]]

    sb, sa = before["surface"]["total"], after["surface"]["total"]
    lines = ["", "=== 裁决 ==="]
    lines.append(f"  表层信号：{sb} → {sa}" + ("  🟢 下降" if sa < sb else
                                              ("  ⚪ 持平" if sa == sb else "  🔴 上升")))

    if not any(b.values()) and not any(a.values()):
        lines += ["", "  ⚪ 结论：原文与改后都没有可机械识别的结构 AI 特征。"]
        lines.append("     若原文确实干净，这是 no-op 合法结果——不要为凑指标硬改。")
        lines.append("     若你确实做了结构改动，请人工确认（本脚本读不懂语义）。")
    elif newly:
        # 只要新增了结构味，就是越改越糟——优先于「改掉了一部分」的措辞
        lines += ["", f"  🔴 结论：改写新增了结构 AI 味（{'、'.join(newly)}）——越改越糟。"]
        if improved:
            lines.append(f"     （虽然也改掉了：{'、'.join(improved)}，但新增的部分抵消了它。）")
        lines.append("     回到反退化规则：不要加连接词、不要改清单、不要加总结句、不要把段落改整齐。")
    elif improved and residue:
        lines += [f"  结构改掉：{'、'.join(improved)}",
                  f"  结构残留：{'、'.join(residue)}",
                  "", "  ⚠️ 结论：只改掉一部分结构，仍有残留——未达标，不要当成完成。",
                  "     回原文逐条看："]
        for k, n in FEATURES:
            if a[k] and after["structure"][k].get("hits"):
                lines.append(f"     · {n}：{', '.join(after['structure'][k]['hits'])}")
    elif improved:
        lines += [f"  结构改掉：{'、'.join(improved)}",
                  "  结构残留：（无）",
                  "", "  ✅ 结论：结构层确实动了。仍需人工复核改动是否自然、事实是否一条未丢。"]
    else:
        lines += [f"  结构残留：{'、'.join(residue)}",
                  "", "  ❌ 结论：只动了表层，结构层一处未改——这是「假去味」。",
                  "     回到 skill 第 2 步：删掉讲道理那句、把结尾打开、把泛指换成具体。"]
        for k, n in FEATURES:
            if b[k] and before["structure"][k].get("hits"):
                lines.append(f"     · 待改 {n}：{', '.join(before['structure'][k]['hits'])}")

    degrade = after["degrade_risk"]["count"] - before["degrade_risk"]["count"]
    if degrade > 0:
        lines.append(f"  🔴 反退化告警：句首新增了 {degrade} 处连接词/过渡词，可能越改越像 AI。")

    if facts:
        missing = [f for f in facts if f["in_before"] and not f["in_after"]]
        # 分子只算「改前有、改后也有」的项，否则改后杜撰项会被算成保留，与"丢失"自相矛盾
        kept = [f for f in facts if f["in_before"] and f["in_after"]]
        denom = [f for f in facts if f["in_before"]]
        lines += ["", f"  事实抽检：{len(kept)}/{len(denom)} 保留"
                  + ("  🟢 全在" if not missing else f"  🔴 丢失：{', '.join(f['fact'] for f in missing)}")
                  + "（仅你枚举的项，非自动事实核验）"]
        invented = [f for f in facts if not f["in_before"] and f["in_after"]]
        if invented:
            lines.append(f"  ⚠️ 改后出现了改前没有的指定项：{', '.join(f['fact'] for f in invented)}")

    lines += ["", "  提示：以上均为启发式判断，会误报也会漏报。读得懂语义的只有改写者本人。"]
    return "\n".join(lines)


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description="AI 味自检（表层机械统计 + 结构启发式）")
    ap.add_argument("files", nargs="*", help="待检查文件（单篇体检）")
    ap.add_argument("--before", help="改前文件")
    ap.add_argument("--after", help="改后文件")
    ap.add_argument("--facts", help="需抽检保留的事实清单，逗号分隔，如 \"186000,11,8 小时\"（人工枚举，非自动核验）")
    ap.add_argument("--max-bytes", type=int, default=MAX_BYTES, help=f"单文件字节上限（默认 {MAX_BYTES}）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    facts = [x for x in (args.facts.split(",") if args.facts else []) if x.strip()]

    if args.before and args.after:
        btext = read_text(args.before, args.max_bytes)
        atext = read_text(args.after, args.max_bytes)
        b, a = analyze(btext), analyze(atext)
        fchk = check_facts(facts, btext, atext) if facts else None
        if args.json:
            print(json.dumps({"before": b, "after": a, "facts": fchk},
                             ensure_ascii=False, indent=2))
        else:
            print(render(f"改前 {args.before}", b))
            print()
            print(render(f"改后 {args.after}", a))
            print(verdict(b, a, fchk))
        return 0

    if not args.files:
        ap.print_help()
        return 2

    out = {}
    for f in args.files:
        r = analyze(read_text(f, args.max_bytes))
        out[f] = r
        if not args.json:
            print(render(f, r))
            print()
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
