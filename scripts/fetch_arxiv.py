#!/usr/bin/env python3
"""按 scripts/arxiv_config.yaml 抓取 arXiv 近期论文并报告新候选。

已收录（data/*.yaml 中的 arxiv id）与已报告（data/seen_arxiv_ids.txt）的论文会被跳过。

Usage:
    python3 scripts/fetch_arxiv.py            # 正常运行，更新 data/seen_arxiv_ids.txt
    python3 scripts/fetch_arxiv.py --dry-run  # 仅打印候选，不更新状态文件
"""

import argparse
import datetime
import http.client
import os
import random
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from email.utils import parsedate_to_datetime

from arxiv_feed import matches_query, parse_feed

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
FEED_URL = "https://rss.arxiv.org/atom/"
USER_AGENT = "awesome-interactive-world-models/1.0 (https://github.com/Zizizi-hao/Awesome-interactive-world-model-for-AD)"
REQUEST_WAIT_BUDGET = 300
_next_request_at = 0.0
NETWORK_ERRORS = (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException)


class RequestDeferred(RuntimeError):
    """服务端要求的冷却时间超出本轮预算；本轮不再请求其他来源。"""


def retry_after_seconds(value: str) -> float:
    if not value:
        return 0
    try:
        return max(0, int(value.strip()))
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=datetime.timezone.utc)
            return max(0, (date - datetime.datetime.now(datetime.timezone.utc)).total_seconds())
        except (TypeError, ValueError, OverflowError):
            return 0


def is_transient(error: Exception) -> bool:
    if isinstance(error, urllib.error.HTTPError):
        return error.code in {408, 429, 500, 502, 503, 504}
    return isinstance(error, NETWORK_ERRORS)


def fetch_url(url: str, retries: int = 3, timeout: int = 60, delay: float = 5) -> bytes:
    """所有来源共享请求间隔和 Retry-After；retries 为总尝试次数。"""
    global _next_request_at
    if retries < 1 or timeout <= 0:
        raise ValueError("retry_attempts 和 timeout_seconds 必须大于 0")
    delay = max(5, delay)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, retries + 1):
        wait = max(0, _next_request_at - time.monotonic())
        if wait > REQUEST_WAIT_BUDGET:
            raise RequestDeferred(f"服务端冷却还需 {wait:.0f}s，超过本轮等待预算；停止所有后续请求")
        if wait:
            time.sleep(wait)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                result = resp.read()
            _next_request_at = time.monotonic() + delay
            return result
        except NETWORK_ERRORS as error:
            wait = delay
            if is_transient(error):
                retry_after = retry_after_seconds(error.headers.get("Retry-After")) if isinstance(error, urllib.error.HTTPError) and error.headers else 0
                wait = max(delay, retry_after, min(90, 15 * 2 ** (attempt - 1))) + random.uniform(0, 3)
            # 最后一次失败也保留冷却期，切换来源不能绕过 Retry-After。
            _next_request_at = time.monotonic() + wait
            if wait > REQUEST_WAIT_BUDGET:
                raise RequestDeferred(f"服务端要求等待 {wait:.0f}s，停止本轮所有后续请求") from error
            if attempt == retries or not is_transient(error):
                raise
            print(f"请求失败（{error}），{wait:.0f}s 后重试（{attempt}/{retries - 1}）...", flush=True)


def strip_version(arxiv_id: str) -> str:
    return re.sub(r"v\d+$", "", str(arxiv_id).strip())


def fetch_query(search: str, max_results: int, retries: int = 3, timeout: int = 60, delay: float = 5) -> bytes:
    params = urllib.parse.urlencode({
        "search_query": search,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    return fetch_url(f"{API_URL}?{params}", retries=retries, timeout=timeout, delay=delay)

def parse_entries(xml_bytes: bytes) -> list:
    root = ET.fromstring(xml_bytes)
    if root.tag != f"{ATOM}feed":
        raise ValueError("arXiv API 返回的不是 Atom feed")
    entries = []
    for entry in root.findall(f"{ATOM}entry"):
        entry_id = entry.findtext(f"{ATOM}id") or ""
        if "/api/errors" in entry_id:
            raise ValueError(entry.findtext(f"{ATOM}summary") or "arXiv API 返回错误 feed")
        raw_id = entry_id.rsplit("/", 1)[-1]
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


def render_report(groups: dict, cfg: dict, failures: dict = None, sources: dict = None) -> str:
    failures = failures or {}
    sources = sources or {}
    total = sum(len(v) for v in groups.values())
    max_chars = cfg.get("abstract_chars", 400)
    query_count = len(cfg.get("queries") or groups)
    api_count = sum(sources.get(name, "API") == "API" for name in groups)
    lines = [f"API 检索完成 **{api_count}/{query_count}** 组，发现 **{total}** 篇新候选论文（由 `scripts/fetch_arxiv.py` 自动生成）。", ""]
    if failures:
        lines += ["> 扫描不完整，不能根据零候选判断没有新论文。", "", "未完成的 API 检索："]
        lines += [f"- {name}：{error}" for name, error in failures.items()]
        lines.append("")
    if "RSS" in sources.values():
        lines += [
            f"> RSS 备用结果仅覆盖最新一期公告，未完成最近 {cfg.get('lookback_days', 7)} 天的完整检索。"
            "匹配范围为标题和摘要，分类包含交叉分类，与 API 的 all 字段和主分类筛选不同。",
            "",
        ]
    for name, entries in groups.items():
        if not entries:
            continue
        lines += [f"## {name}" + ("（RSS 备用结果）" if sources.get(name) == "RSS" else ""), ""]
        for e in entries:
            abstract = e["abstract"]
            if len(abstract) > max_chars:
                abstract = abstract[:max_chars] + "..."
            date_text = f"提交日期: {e['published']}"
            category_text = f"主分类: {e['primary_category']}"
            if e.get("date_label") == "公告日期":
                date_text = f"公告日期: {e['announced']}"
                category_text = "分类（含交叉分类）: " + ", ".join(e["categories"])
            lines += [
                f"### {e['title']}",
                f"- arXiv: https://arxiv.org/abs/{e['id']}",
                f"- {date_text} ｜ {category_text}",
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


def write_output(has_new: bool, report: Path = None, scan_status: str = "success") -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a", encoding="utf-8") as f:
        f.write(f"has_new={'true' if has_new else 'false'}\n")
        f.write(f"scan_status={scan_status}\n")
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
    delay = max(5, cfg.get("delay_seconds", 5))
    retries = cfg.get("retry_attempts", 3)
    timeout = cfg.get("timeout_seconds", 60)
    queries = cfg.get("queries") or []
    if not queries:
        sys.exit("未配置 queries，无法扫描。")

    existing = existing_arxiv_ids()
    seen = load_seen()
    reported = set()
    groups = {}
    failures = {}
    sources = {}
    deferred = False

    def pick(entries, *, feed=False):
        picked = []
        for e in entries:
            date = e.get("announced", "") if feed else e["published"]
            if date < cutoff:
                continue
            categories = set(e.get("categories") or []) if feed else {e["primary_category"]}
            if cat_filter and not categories.intersection(cat_filter):
                continue
            if e["id"] in existing or e["id"] in seen or e["id"] in reported:
                continue
            picked.append(e)
            reported.add(e["id"])
        return picked

    print(f"请求配置：每组最多尝试 {retries} 次，读取超时 {timeout}s，请求间隔至少 {delay}s。", flush=True)
    for i, q in enumerate(queries):
        print(f"检索: {q['name']} ...", flush=True)
        try:
            entries = parse_entries(fetch_query(q["search"], max_results, retries=retries, timeout=timeout, delay=delay))
        except (RequestDeferred, *NETWORK_ERRORS, ET.ParseError, ValueError) as error:
            print(f"  检索失败（{error}）", flush=True)
            failures[q["name"]] = str(error)
            deferred = isinstance(error, RequestDeferred)
            if deferred or is_transient(error):
                # 一组已耗尽重试，暂时停用该 API，避免对后续查询重复施压。
                for pending in queries[i + 1:]:
                    failures[pending["name"]] = "API 暂不可用，本轮停止后续 API 请求"
                break
            continue
        picked = pick(entries)
        groups[q["name"]] = picked
        sources[q["name"]] = "API"
        print(f"  命中 {len(entries)} 篇，新增候选 {len(picked)} 篇", flush=True)

    if failures and cfg.get("rss_fallback", False) and not deferred:
        print("尝试一次 RSS 备用来源（仅最新一期公告，无法补齐 7 天检索）。", flush=True)
        try:
            if not cat_filter:
                raise ValueError("RSS 备用来源需要配置 category_filter")
            url = FEED_URL + "+".join(sorted(cat_filter))
            feed_entries = parse_feed(fetch_url(url, retries=1, timeout=timeout, delay=delay))
            for q in queries:
                if q["name"] not in failures:
                    continue
                # 先完成整组匹配，配置错误时不把未展示的条目加入 seen。
                matched = [e for e in feed_entries if matches_query(e, q)]
                groups[q["name"]] = pick(matched, feed=True)
                sources[q["name"]] = "RSS"
                print(f"  RSS {q['name']}：新增候选 {len(groups[q['name']])} 篇", flush=True)
        except (RequestDeferred, *NETWORK_ERRORS, ET.ParseError, ValueError) as error:
            print(f"  RSS 备用来源失败（{error}）", flush=True)
            for name in failures:
                if sources.get(name) != "RSS":
                    failures[name] += f"；RSS 备用失败：{error}"

    status = "failed" if not groups else "partial" if failures else "success"
    report = render_report(groups, cfg, failures, sources)
    if status == "failed":
        print(f"::error::扫描失败：0/{len(queries)} 组获取到有效结果，无法判断是否有新论文。", flush=True)
    elif status == "partial":
        print("::warning::扫描不完整：部分 API 检索失败；详情见运行摘要。", flush=True)
    elif not reported:
        print("检索成功，没有新候选论文。", flush=True)
    if args.dry_run:
        print("\n" + report)
        if status == "failed":
            raise SystemExit(1)
        return

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(report + "\n")
    report_path = None
    if reported:
        report_path = Path(tempfile.gettempdir()) / "arxiv_report.md"
        report_path.write_text(report, encoding="utf-8")
        # 工作流仅在 Issue 创建成功后才提交这个本地状态文件。
        append_seen(reported)
        print(f"\n共 {len(reported)} 篇新候选，报告已写入: {report_path}", flush=True)
    write_output(has_new=bool(reported), report=report_path, scan_status=status)
    if status == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
