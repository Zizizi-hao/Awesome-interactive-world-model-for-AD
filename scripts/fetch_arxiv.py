#!/usr/bin/env python3
"""按 scripts/arxiv_config.yaml 抓取 arXiv 近期论文并报告新候选。

已收录（data/*.yaml 中的 arxiv id）与已报告（data/seen_arxiv_ids.txt）的论文会被跳过。

Usage:
    python3 scripts/fetch_arxiv.py            # 正常运行，更新 data/seen_arxiv_ids.txt
    python3 scripts/fetch_arxiv.py --dry-run  # 仅打印候选，不更新状态文件
"""

import argparse
import datetime
import os
import re
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pip install pyyaml")

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = Path(__file__).resolve().parent / "arxiv_config.yaml"
DATA_FILE = ROOT / "data.yaml"
SEEN_FILE = ROOT / "data" / "seen_arxiv_ids.txt"

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"
API_URL = "https://export.arxiv.org/api/query"


def strip_version(arxiv_id: str) -> str:
    return re.sub(r"v\d+$", "", str(arxiv_id).strip())


def fetch_query(search: str, max_results: int, retries: int = 3) -> bytes:
    params = urllib.parse.urlencode({
        "search_query": search,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    req = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={"User-Agent": "awesome-interactive-world-models/1.0"},
    )
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as e:
            if attempt == retries:
                raise
            wait = 15 * attempt
            print(f"请求失败（{e}），{wait}s 后重试（{attempt}/{retries - 1}）...")
            time.sleep(wait)


def parse_entries(xml_bytes: bytes) -> list:
    root = ET.fromstring(xml_bytes)
    entries = []
    for entry in root.findall(f"{ATOM}entry"):
        raw_id = (entry.findtext(f"{ATOM}id") or "").rsplit("/", 1)[-1]
        if not raw_id:
            continue
        primary = entry.find(f"{ARXIV_NS}primary_category")
        entries.append({
            "id": strip_version(raw_id),
            "title": re.sub(r"\s+", " ", entry.findtext(f"{ATOM}title") or "").strip(),
            "abstract": re.sub(r"\s+", " ", entry.findtext(f"{ATOM}summary") or "").strip(),
            "published": (entry.findtext(f"{ATOM}published") or "")[:10],
            "authors": [a.findtext(f"{ATOM}name") or "" for a in entry.findall(f"{ATOM}author")],
            "primary_category": primary.get("term") if primary is not None else "",
        })
    return entries


def existing_arxiv_ids() -> set:
    ids = set()
    data = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8")) or {}
    files = [DATA_FILE] + [ROOT / rel for rel in data.get("includes") or []]
    for f in files:
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for p in d.get("papers") or []:
            aid = (p.get("links") or {}).get("arxiv")
            if aid:
                ids.add(strip_version(aid))
    return ids


def load_seen() -> set:
    if not SEEN_FILE.is_file():
        return set()
    return {
        strip_version(line)
        for line in SEEN_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def append_seen(new_ids) -> None:
    if SEEN_FILE.is_file():
        lines = SEEN_FILE.read_text(encoding="utf-8").splitlines()
    else:
        lines = ["# 已由 scripts/fetch_arxiv.py 报告过的 arXiv id，自动维护，勿手动编辑"]
    lines.extend(sorted(new_ids))
    SEEN_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_authors(authors: list, limit: int = 6) -> str:
    if len(authors) > limit:
        return ", ".join(authors[:limit]) + f" 等（共 {len(authors)} 人）"
    return ", ".join(authors)


def render_report(groups: dict, cfg: dict) -> str:
    total = sum(len(v) for v in groups.values())
    max_chars = cfg.get("abstract_chars", 400)
    lines = [f"共扫描 {len(groups)} 组检索，发现 **{total}** 篇新候选论文（由 `scripts/fetch_arxiv.py` 自动生成）。", ""]
    for name, entries in groups.items():
        if not entries:
            continue
        lines += [f"## {name}", ""]
        for e in entries:
            abstract = e["abstract"]
            if len(abstract) > max_chars:
                abstract = abstract[:max_chars] + "..."
            lines += [
                f"### {e['title']}",
                f"- arXiv: https://arxiv.org/abs/{e['id']}",
                f"- 提交日期: {e['published']} ｜ 主分类: {e['primary_category']}",
                f"- 作者: {format_authors(e['authors'])}",
                f"- 摘要: {abstract}",
                "",
            ]
    lines += [
        "---",
        "收录流程：将候选条目写入 `data/<category>.yaml`（字段规范见 CONTRIBUTING.md），"
        "然后运行 `python3 scripts/generate_readme.py` 重新生成 README。",
    ]
    return "\n".join(lines)


def write_output(has_new: bool, report: Path = None) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a", encoding="utf-8") as f:
        f.write(f"has_new={'true' if has_new else 'false'}\n")
        if report:
            f.write(f"report={report}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="抓取 arXiv 新论文候选")
    parser.add_argument("--dry-run", action="store_true", help="仅打印候选，不更新状态文件")
    args = parser.parse_args()

    cfg = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
    cutoff = (datetime.date.today() - datetime.timedelta(days=cfg.get("lookback_days", 7))).isoformat()
    cat_filter = set(cfg.get("category_filter") or [])
    max_results = cfg.get("max_results_per_query", 100)
    delay = cfg.get("delay_seconds", 3)

    existing = existing_arxiv_ids()
    seen = load_seen()
    reported = set()
    groups = {}
    new_ids = set()

    for i, q in enumerate(cfg.get("queries") or []):
        if i:
            time.sleep(delay)
        print(f"检索: {q['name']} ...")
        entries = parse_entries(fetch_query(q["search"], max_results))
        picked = []
        for e in entries:
            if e["published"] < cutoff:
                continue
            if cat_filter and e["primary_category"] not in cat_filter:
                continue
            if e["id"] in existing or e["id"] in seen or e["id"] in reported:
                continue
            picked.append(e)
            reported.add(e["id"])
        groups[q["name"]] = picked
        new_ids |= reported
        print(f"  命中 {len(entries)} 篇，新增候选 {len(picked)} 篇")

    if not new_ids:
        print("没有新候选论文。")
        write_output(has_new=False)
        return

    report = render_report(groups, cfg)
    if args.dry_run:
        print("\n" + report)
        return

    append_seen(reported)
    report_path = Path(tempfile.gettempdir()) / "arxiv_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\n共 {len(new_ids)} 篇新候选，报告已写入: {report_path}")
    write_output(has_new=True, report=report_path)


if __name__ == "__main__":
    main()
