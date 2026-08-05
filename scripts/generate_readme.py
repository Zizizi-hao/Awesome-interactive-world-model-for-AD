#!/usr/bin/env python3
"""Generate README.md from data.yaml.

Usage:
    python3 scripts/generate_readme.py
"""

import datetime
import re
import subprocess
import sys
from pathlib import Path

import generate_figure

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data.yaml"
README_FILE = ROOT / "README.md"

FEATURE_ICONS = [
    ("action", "🎮", "动作条件生成"),
    ("realtime", "⚡", "实时推理"),
    ("closedloop", "🔁", "闭环支持"),
    ("longhorizon", "⏳", "长时序一致性"),
]


def esc(text: str) -> str:
    return str(text).replace("|", "\\|")


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_data() -> dict:
    """Load data.yaml and merge the paper lists it references via `includes`."""
    data = load_yaml(DATA_FILE)
    papers = list(data.get("papers") or [])
    for rel in data.get("includes") or []:
        inc_path = ROOT / rel
        if not inc_path.is_file():
            sys.exit(f"Included data file not found: {rel}")
        inc = load_yaml(inc_path) or {}
        inc_papers = inc.get("papers") or []
        for p in inc_papers:
            p.setdefault("_source", rel)
        papers.extend(inc_papers)
    data["papers"] = papers
    return data


def last_updated(data_paths: list) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", *data_paths],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return datetime.date.today().isoformat()


def render_links(links: dict) -> str:
    parts = []
    if links.get("arxiv"):
        parts.append(f"[论文](https://arxiv.org/abs/{links['arxiv']})")
    if links.get("project"):
        parts.append(f"[项目]({links['project']})")
    if links.get("code"):
        parts.append(f"[代码]({links['code']})")
    if links.get("demo"):
        parts.append(f"[演示]({links['demo']})")
    return " \\| ".join(parts) if parts else "—"


def render_features(features: dict) -> str:
    icons = [icon for key, icon, _ in FEATURE_ICONS if features.get(key)]
    return " ".join(icons) if icons else "—"


def render_venue(paper: dict) -> str:
    venue = paper.get("venue")
    if not venue:
        return "—"
    # 年份统一取自 year 字段（首次发表年份），去掉 venue 中内嵌的会议年份
    text = re.sub(r"\s*\b(?:19|20)\d{2}\b", "", str(venue), count=1).strip()
    year = paper.get("year")
    if year:
        m = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", text)
        if m and m.group(1).strip():
            text = f"{m.group(1).strip()} ({year}, {m.group(2).strip()})"
        else:
            text = f"{text} ({year})"
    return esc(text)


def render_paper_row(paper: dict) -> str:
    title, short = paper["title"], paper.get("short")
    if short and title.lower().startswith(short.lower() + ":"):
        title = title[len(short) + 1:].strip()
    name = f"**{esc(short)}**: {esc(title)}" if short else f"**{esc(title)}**"
    venue_year = render_venue(paper)
    org = esc(paper.get("org") or "—")
    return (
        f"| {name} | {venue_year} | {org} | "
        f"{render_features(paper.get('features', {}))} | "
        f"{render_links(paper.get('links', {}))} | {esc(paper.get('note', ''))} |"
    )


def github_anchor(heading: str) -> str:
    anchor = heading.lower()
    anchor = re.sub(r"[^\w\- ]", "", anchor, flags=re.UNICODE)
    return anchor.strip().replace(" ", "-")


def main() -> None:
    generate_figure.main()
    data = load_data()
    meta = data["meta"]
    categories = data["categories"]
    papers = data["papers"]

    data_paths = ["data.yaml"] + [rel for rel in (data.get("includes") or [])]

    known = {c["id"] for c in categories}
    for p in papers:
        if p.get("category") not in known:
            src = p.get("_source", "data.yaml")
            sys.exit(f"Unknown category '{p.get('category')}' in paper: {p.get('title')} ({src})")

    lines = [
        "<!-- ============================================================ -->",
        "<!-- 本文件由 scripts/generate_readme.py 从 data.yaml 自动生成，请勿手动编辑 -->",
        "<!-- ============================================================ -->",
        "",
        f"# {meta['title']}",
        "",
        f"> {meta['subtitle']}",
        "",
        meta["description"].strip(),
        "",
        f"📊 共收录 **{len(papers)}** 篇工作 ｜ 最后更新：{last_updated(data_paths)}",
        "",
        '<p align="center">',
        '  <img src="assets/interactive-world-model.png" alt="交互式世界模型：智能体与世界模型的闭环交互" width="760">',
        "</p>",
        "",
        "## 交互能力图例",
        "",
        "| 图标 | 含义 |",
        "| :---: | :--- |",
    ]
    for _, icon, label in FEATURE_ICONS:
        lines.append(f"| {icon} | {label} |")

    lines += ["", "## 目录", ""]
    for c in categories:
        count = sum(1 for p in papers if p["category"] == c["id"])
        heading = f"{c['name']} {c['name_en']}"
        lines.append(f"- [{heading}](#{github_anchor(heading)})（{count}）")

    for c in categories:
        cat_papers = sorted(
            (p for p in papers if p["category"] == c["id"]),
            key=lambda p: (-p["year"], p["title"]),
        )
        lines += [
            "",
            f"## {c['name']} {c['name_en']}",
            "",
            "| 论文 | 发表 | 机构 | 交互能力 | 链接 | 一句话点评 |",
            "| :--- | :--- | :--- | :---: | :--- | :--- |",
        ]
        lines += [render_paper_row(p) for p in cat_papers]

    lines += [
        "",
        "## 如何贡献",
        "",
        "欢迎通过 Issue / PR 补充或修正条目。论文条目按分类存放在 [`data/`](data/) 目录下"
        "（入口为 [`data.yaml`](data.yaml)），请只修改这些数据文件，"
        "并运行 `python3 scripts/generate_readme.py` 重新生成本文件，"
        "字段规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。",
        "",
        "## License",
        "",
        "本仓库内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可。",
        "",
    ]

    README_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {README_FILE.name} with {len(papers)} papers.")


if __name__ == "__main__":
    main()
