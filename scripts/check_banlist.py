#!/usr/bin/env python3
"""表皮黑名单机检：对标原剧外壳禁用词在新稿中的零重合检查。

仿写铁律（L1 表皮层）：原剧专名、金句、标志性老梗在新稿正文出现 1 处即 FAIL。
用法：
    python check_banlist.py <新剧本文件> --banlist <黑名单文件>
    python check_banlist.py <新剧本文件> --words 词A 词B 词C
    python check_banlist.py --self-test
黑名单文件格式：每行一个禁用词，# 开头为注释，可用「词|类型」两列。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SELF_TEST = [
    # (新稿文本, 黑名单, 期望级别)
    ("老陈把扳手拍在桌上。", ["龙王", "玄铁令"], "PASS"),
    ("他自称赘婿龙王归来。", ["龙王"], "FAIL"),
    ("深夜，修理铺只剩一盏灯。", ["夜色如墨"], "PASS"),
]


def load_banlist(path: str | None, words: list[str] | None) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    if path:
        for line in Path(path).read_text(encoding="utf-8-sig", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            items.append((parts[0], parts[1] if len(parts) > 1 else "未分类"))
    for w in words or []:
        items.append((w, "命令行"))
    return items


def check(text: str, banlist: list[tuple[str, str]]) -> dict:
    hits: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for word, wtype in banlist:
            if word and word in line:
                hits.append({"line": lineno, "word": word, "type": wtype, "text": line.strip()[:60]})
    level = "FAIL" if hits else "PASS"
    return {"level": level, "hits": hits, "checked_words": len(banlist)}


def report(result: dict) -> str:
    lines = [f"【表皮黑名单机检】 {result['level']}  （词表 {result['checked_words']} 项）"]
    for h in result["hits"]:
        lines.append(f"  第{h['line']}行 [{h['type']}] 命中禁用词「{h['word']}」：{h['text']}")
    if result["level"] == "PASS":
        lines.append("  正文与对标原剧外壳零重合，L1 表皮层通过。")
    else:
        lines.append("  L1 表皮层不通过：出现 1 处即回炉（改写该句或换物证载体）。")
    return "\n".join(lines)


def self_test() -> bool:
    ok = True
    for text, ban, expected in SELF_TEST:
        got = check(text, [(w, "test") for w in ban])["level"]
        mark = "ok" if got == expected else "FAILED"
        if got != expected:
            ok = False
        print(f"  self-test [{mark}] expected={expected} got={got} text={text[:20]}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="表皮黑名单机检（零重合）")
    ap.add_argument("file", nargs="?", help="新剧本文件")
    ap.add_argument("--banlist", help="黑名单文件（每行一个词，可带「词|类型」）")
    ap.add_argument("--words", nargs="*", help="命令行直接给禁用词")
    ap.add_argument("--self-test", action="store_true", help="自检")
    args = ap.parse_args()

    if args.self_test:
        return 0 if self_test() else 1
    if not args.file:
        ap.print_help()
        return 2
    ban = load_banlist(args.banlist, args.words)
    if not ban:
        print("黑名单为空：请用 --banlist 或 --words 提供禁用词。")
        return 2
    text = Path(args.file).read_text(encoding="utf-8-sig", errors="ignore")
    print(report(check(text, ban)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
