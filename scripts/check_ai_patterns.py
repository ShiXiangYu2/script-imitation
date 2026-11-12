#!/usr/bin/env python3
"""AI 味标记词机检（剧本层）。

改编自 huoren-write check_output.py 的词表，聚焦短剧剧本正文。
判断看密度与违和感，不看单次出现：单类 1 次命中 = NOTE；2~3 次 = WARN；≥4 次或跨 3 类以上 = FAIL。
用法：
    python check_ai_patterns.py <剧本文件>
    python check_ai_patterns.py --self-test
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PATTERNS: dict[str, tuple[str, str]] = {
    # 类名: (正则, 说明)
    "句首连接词": (r"(?:^|(?<=[\n。，；]))\s*(此外|值得注意的是|本质上|事实上|实际上|换言之|总而言之|由此可见|不难看出)[，,]", "删掉，或换成人物口吻的自然衔接"),
    "不是而是模板": (r"不是[^。！？\n]{0,40}而是", "拆成自然短句"),
    "强行升华": (r"(人生的意义|成为自己的光|真正的强大|命运的齿轮|这一刻.{0,8}明白|真正让.{0,10}的不是)", "删掉段尾拔高"),
    "脸谱化反应": (r"(瞳孔地震|倒吸一口凉气|全场哗然|嘴角勾起一抹冷笑|眼中闪过一丝精光)", "换成可见动作"),
    "复用氛围词": (r"(夜色如墨|月光皎洁|空气凝固|时间仿佛静止|心脏漏跳一拍)", "换成当下感知"),
    "万能狠话": (r"(你会后悔的|我不会放过你|你根本不知道我是谁|你这是在玩火)", "换具体威胁（断他的货/绑他的贷）"),
    "万能安抚腔": (r"(我理解你|我就在这|我陪你|慢慢来|不急不乱|如果你需要.{0,12}随时.{0,8}找我)", "按人物关系改：能沉默就沉默"),
    "公文腔动词": (r"(予以|得以|被视为|进行[^。！？\n]{0,8}工作|做出[^。！？\n]{0,8}决定)", "换口语动词"),
    "空泛程度词": (r"(非常|十分|极其|格外|无比|前所未有)", "换具体程度（数量/对比）"),
    "说明书对话": (r"(你知道的?|作为你的|如你所知|我们家族|我们家一直)[^。！？\n]{0,30}", "信息改在冲突中露出"),
}

SELF_TEST = [
    # (文本, 期望级别不为 FAIL 即视为通过机检设计)
    ("陈默把合同拍在桌上，签字。", "PASS"),
    ("此外，值得注意的是，他事实上很愤怒。总而言之，他忍了。换言之，他不想说话。", "FAIL"),
    ("她瞳孔地震，倒吸一口凉气。", "WARN"),
]


def check(text: str) -> dict:
    cat_hits: dict[str, list[int]] = {}
    for cat, (pat, _desc) in PATTERNS.items():
        for m in re.finditer(pat, text):
            lineno = text.count("\n", 0, m.start()) + 1
            cat_hits.setdefault(cat, []).append(lineno)

    notes = {c: l for c, l in cat_hits.items() if len(l) == 1}
    warns = {c: l for c, l in cat_hits.items() if 2 <= len(l) <= 3}
    fails = {c: l for c, l in cat_hits.items() if len(l) >= 4}
    if len(cat_hits) >= 3:
        level = "FAIL"
    elif fails or warns:
        level = "FAIL" if fails else "WARN"
    elif notes:
        level = "NOTE"
    else:
        level = "PASS"
    return {"level": level, "notes": notes, "warns": warns, "fails": fails,
            "cats": cat_hits, "total_lines": text.count("\n") + 1}


def report(r: dict) -> str:
    out = [f"【AI 味机检】 {r['level']}  （{r['total_lines']} 行）"]
    for cat, lines in r["fails"].items():
        out.append(f"  FAIL [{cat}] 命中{len(lines)}次（行 {lines[:8]}）：{PATTERNS[cat][1]}")
    for cat, lines in r["warns"].items():
        out.append(f"  WARN [{cat}] 命中{len(lines)}次（行 {lines[:8]}）：{PATTERNS[cat][1]}")
    for cat, lines in r["notes"].items():
        out.append(f"  NOTE [{cat}] 命中1次（行 {lines}）：{PATTERNS[cat][1]}")
    if r["level"] == "PASS":
        out.append("  无 AI 味标记词，通过。")
    return "\n".join(out)


def self_test() -> bool:
    ok = True
    for text, expected in SELF_TEST:
        got = check(text)["level"]
        mark = "ok" if got == expected else "FAILED"
        if got != expected:
            ok = False
        print(f"  self-test [{mark}] expected={expected} got={got} text={text[:24]}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="AI 味标记词机检")
    ap.add_argument("file", nargs="?", help="剧本/文本文件")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return 0 if self_test() else 1
    if not args.file:
        ap.print_help()
        return 2
    text = Path(args.file).read_text(encoding="utf-8-sig", errors="ignore")
    print(report(check(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
