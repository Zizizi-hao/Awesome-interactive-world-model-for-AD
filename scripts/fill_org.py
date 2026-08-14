#!/usr/bin/env python3
"""为 data/*.yaml 中 org 为空的条目按 arXiv 作者信息回填机构。

规则：使用「<末位作者> 团队」作为机构名。

Usage:
    python3 scripts/fill_org.py            # 回填并写入文件
    python3 scripts/fill_org.py --dry-run  # 仅打印待回填内容
"""

import argparse
import re
import sys
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
DATA_FILE = ROOT / "data.yaml"

ATOM = "{http://www.w3.org/2005/Atom}"
API_URL = "https://export.arxiv.org/api/query"
BATCH_SIZE = 30
DELAY = 5
RETRIES = 5


def strip_version(arxiv_id: str) -> str:
    return re.sub(r"v\d+$", "", str(arxiv_id).strip())


def collect_missing() -> list:
    """返回 org 为空且含 arxiv 链接的条目 [(文件路径, arxiv_id, 标题)]。"""
    data = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8")) or {}
    files = [DATA_FILE] + [ROOT / rel for rel in data.get("includes") or []]
    missing = []
    for f in files:
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for p in d.get("papers") or []:
            if str(p.get("org") or "").strip():
                continue
            aid = (p.get("links") or {}).get("arxiv")
            if aid:
                missing.append((f, strip_version(aid), p["title"]))
    return missing


def fetch_authors(ids: list) -> dict:
    """批量查询 arXiv，返回 {arxiv_id: [作者列表]}。"""
    result = {}
    for i in range(0, len(ids), BATCH_SIZE):
        if i:
            time.sleep(DELAY)
        batch = ids[i:i + BATCH_SIZE]
        params = urllib.parse.urlencode({
            "id_list": ",".join(batch),
            "max_results": len(batch),
        })
        req = urllib.request.Request(
            f"{API_URL}?{params}",
            headers={"User-Agent": "awesome-interactive-world-models/1.0"},
        )
        for attempt in range(1, RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    payload = resp.read()
                break
            except Exception as e:
                if attempt == RETRIES:
                    raise
                wait = 15 * attempt
                print(f"  请求失败（{e}），{wait}s 后重试（{attempt}/{RETRIES - 1}）...")
                time.sleep(wait)
        root = ET.fromstring(payload)
        for entry in root.findall(f"{ATOM}entry"):
            raw_id = (entry.findtext(f"{ATOM}id") or "").rsplit("/", 1)[-1]
            if not re.match(r"^\d{4}\.\d{4,5}(v\d+)?$", raw_id):
                continue
            authors = [a.findtext(f"{ATOM}name") or "" for a in entry.findall(f"{ATOM}author")]
            result[strip_version(raw_id)] = authors
        print(f"  已查询 {min(i + BATCH_SIZE, len(ids))}/{len(ids)}")
    return result


def fill_file(path: Path, updates: dict) -> int:
    """在包含对应 arxiv id 的条目块内替换 org 行，返回修改条数。"""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    blocks = []
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("  - title:"):
            if start is not None:
                blocks.append((start, idx))
            start = idx
    if start is not None:
        blocks.append((start, len(lines)))

    changed = 0
    for s, e in blocks:
        m = re.search(r'arxiv:\s*"([^"]+)"', "".join(lines[s:e]))
        if not m:
            continue
        aid = strip_version(m.group(1))
        if aid not in updates:
            continue
        for j in range(s, e):
            if re.match(r"\s*org:", lines[j]):
                indent = lines[j][: len(lines[j]) - len(lines[j].lstrip())]
                lines[j] = f'{indent}org: "{updates[aid]}"\n'
                changed += 1
                break
    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="按 arXiv 末位作者回填空缺机构")
    parser.add_argument("--dry-run", action="store_true", help="仅打印待回填内容")
    args = parser.parse_args()

    missing = collect_missing()
    if not missing:
        print("没有缺少机构的条目。")
        return

    print(f"共 {len(missing)} 条缺少机构，查询 arXiv ...")
    authors = fetch_authors([aid for _, aid, _ in missing])

    updates_by_file = {}
    failed = []
    for f, aid, title in missing:
        auths = authors.get(aid)
        if not auths:
            failed.append((aid, title))
            continue
        updates_by_file.setdefault(f, {})[aid] = f"{auths[-1]} 团队"

    if args.dry_run:
        for f, ups in updates_by_file.items():
            for aid, org in ups.items():
                print(f"  {f.name} | {aid} -> {org}")
    else:
        total = sum(fill_file(f, ups) for f, ups in updates_by_file.items())
        print(f"已回填 {total} 条。")

    if failed:
        print("以下论文未能获取作者（请检查 arXiv 编号）：")
        for aid, title in failed:
            print(f"  {aid}  {title}")


if __name__ == "__main__":
    main()
