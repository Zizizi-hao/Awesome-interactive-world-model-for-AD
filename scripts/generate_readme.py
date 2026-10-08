#!/usr/bin/env python3
"""Generate Chinese and English READMEs from shared data.yaml.

Usage:
    python3 scripts/generate_readme.py
"""

import datetime
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data.yaml"
README_FILE = ROOT / "README.md"
README_FILES = {"zh": README_FILE, "en": ROOT / "README.en.md"}
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

FEATURE_ICONS = [
    ("action", "🎮", {"zh": "动作条件生成", "en": "Action-conditioned generation"}),
    ("realtime", "⚡", {"zh": "实时推理", "en": "Real-time inference"}),
    ("closedloop", "🔁", {"zh": "闭环支持", "en": "Closed-loop support"}),
    ("longhorizon", "⏳", {"zh": "长时序一致性", "en": "Long-horizon consistency"}),
]

TEXT = {
    "zh": {
        "generated": "本文件由 scripts/generate_readme.py 从 data.yaml 自动生成，请勿手动编辑",
        "switch": "**简体中文** | [English](README.en.md)",
        "stats": "📊 共收录 **{count}** 篇工作 ｜ 最后更新：{updated}",
        "overview_image": "assets/interactive-world-model1.png",
        "overview_alt": "交互式世界模型：智能体与世界模型的闭环交互",
        "chart_image": "assets/monthly-paper-counts.png",
        "chart_alt": "各类别每月收录篇数",
        "legend": "交互能力图例",
        "legend_header": "| 图标 | 含义 |",
        "contents": "目录",
        "count": "（{count}）",
        "table_header": "| 论文 | 发表 | 机构 | 交互能力 | 链接 | 一句话点评 |",
        "contributing": "如何贡献",
        "contribution_text": (
            "欢迎通过 Issue / PR 补充或修正条目。论文条目按分类存放在 [`data/`](data/) 目录下"
            "（入口为 [`data.yaml`](data.yaml)），请在数据文件中维护中英文点评，"
            "并运行 `python3 scripts/generate_readme.py` 同时重新生成中英文 README，"
            "字段规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。"
        ),
        "license": "本仓库内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可。",
        "links": {"arxiv": "论文", "project": "项目", "code": "代码", "demo": "演示"},
    },
    "en": {
        "generated": "Generated from data.yaml by scripts/generate_readme.py; do not edit manually.",
        "switch": "[简体中文](README.md) | **English**",
        "stats": "📊 **{count}** papers collected | Last updated: {updated}",
        "overview_image": "assets/interactive-world-model.en.svg",
        "overview_alt": "Interactive world models: closed-loop interaction between agents and world models",
        "chart_image": "assets/monthly-paper-counts.en.png",
        "chart_alt": "Monthly paper counts by category",
        "legend": "Interactive capabilities",
        "legend_header": "| Icon | Meaning |",
        "contents": "Contents",
        "count": " ({count})",
        "table_header": "| Paper | Publication | Organization | Capabilities | Links | Summary |",
        "contributing": "Contributing",
        "contribution_text": (
            "Add or correct entries through Issues or pull requests. Papers are stored by category in "
            "[`data/`](data/), with [`data.yaml`](data.yaml) as the entry point. Maintain both Chinese and "
            "English summaries in the data files, then run `python3 scripts/generate_readme.py` to "
            "regenerate both READMEs. See [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md) for the field specification."
        ),
        "license": "This repository's content is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).",
        "links": {"arxiv": "Paper", "project": "Project", "code": "Code", "demo": "Demo"},
    },
}


def localized(item: dict, key: str, language: str) -> str:
    if language == "en":
        return item.get(key + "_en") or item.get(key) or ""
    return item.get(key) or ""


def validate_data(data: dict) -> None:
    """Reject missing translations before either README is overwritten."""
    for key in ("subtitle_en", "description_en"):
        value = data["meta"].get(key)
        if not isinstance(value, str) or not value.strip() or CJK.search(value):
            raise ValueError(f"Missing or non-English meta.{key} in data.yaml")
    known = set()
    for category in data["categories"]:
        known.add(category["id"])
        value = category.get("name_en")
        if not isinstance(value, str) or not value.strip() or CJK.search(value):
            raise ValueError(f"Missing or non-English name_en for category: {category['id']}")
    for paper in data["papers"]:
        source = paper.get("_source", "data.yaml")
        context = f"{paper.get('title')} ({source})"
        if paper.get("category") not in known:
            raise ValueError(f"Unknown category '{paper.get('category')}' in paper: {context}")
        if not isinstance(paper.get("note"), str) or not paper["note"].strip():
            raise ValueError(f"Missing note for paper: {context}")
        value = paper.get("note_en")
        if not isinstance(value, str) or not value.strip() or CJK.search(value):
            raise ValueError(f"Missing or non-English note_en for paper: {context}")
        org_en = paper.get("org_en")
        if CJK.search(str(paper.get("org") or "")) and (
            not isinstance(org_en, str) or not org_en.strip()
        ):
            raise ValueError(f"Missing or non-English org_en for paper: {context}")
        if CJK.search(localized(paper, "org", "en")):
            raise ValueError(f"Missing or non-English org_en for paper: {context}")


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


def last_updated(meta: dict) -> str:
    """Read the date from data.yaml so local generation matches CI after the same commit.

    Do not use `git log` on data files: generating README and committing yaml in one
    commit makes CI see a newer commit date than the pre-commit generation.
    """
    explicit = meta.get("updated")
    if explicit:
        return str(explicit)
    return datetime.date.today().isoformat()


def render_links(links: dict, language: str = "zh") -> str:
    labels = TEXT[language]["links"]
    parts = []
    if links.get("arxiv"):
        parts.append(f"[{labels['arxiv']}](https://arxiv.org/abs/{links['arxiv']})")
    if links.get("project"):
        parts.append(f"[{labels['project']}]({links['project']})")
    if links.get("code"):
        parts.append(f"[{labels['code']}]({links['code']})")
    if links.get("demo"):
        parts.append(f"[{labels['demo']}]({links['demo']})")
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


def render_paper_row(paper: dict, language: str = "zh") -> str:
    title, short = paper["title"], paper.get("short")
    if short and title.lower().startswith(short.lower() + ":"):
        title = title[len(short) + 1:].strip()
    name = f"**{esc(short)}**: {esc(title)}" if short else f"**{esc(title)}**"
    venue_year = render_venue(paper)
    org = esc(localized(paper, "org", language) or "—")
    return (
        f"| {name} | {venue_year} | {org} | "
        f"{render_features(paper.get('features', {}))} | "
        f"{render_links(paper.get('links', {}), language)} | {esc(localized(paper, 'note', language))} |"
    )


def github_anchor(heading: str) -> str:
    anchor = heading.lower()
    anchor = re.sub(r"[^\w\- ]", "", anchor, flags=re.UNICODE)
    return anchor.strip().replace(" ", "-")


def render_readme(data: dict, language: str = "zh") -> str:
    validate_data(data)
    text = TEXT[language]
    meta = data["meta"]
    categories = data["categories"]
    papers = data["papers"]

    lines = [
        "<!-- ============================================================ -->",
        f"<!-- {text['generated']} -->",
        "<!-- ============================================================ -->",
        "",
        f"# {localized(meta, 'title', language)}",
        "",
        text["switch"],
        "",
        f"> {localized(meta, 'subtitle', language)}",
        "",
        localized(meta, "description", language).strip(),
        "",
        text["stats"].format(count=len(papers), updated=last_updated(meta)),
        "",
        '<p align="center">',
        f'  <img src="{text["overview_image"]}" alt="{text["overview_alt"]}" width="760">',
        "</p>",
        "",
        '<p align="center">',
        f'  <img src="{text["chart_image"]}" alt="{text["chart_alt"]}" width="760">',
        "</p>",
        "",
        f"## {text['legend']}",
        "",
        text["legend_header"],
        "| :---: | :--- |",
    ]
    for _, icon, label in FEATURE_ICONS:
        lines.append(f"| {icon} | {label[language]} |")

    lines += ["", f"## {text['contents']}", ""]
    for c in categories:
        count = sum(1 for p in papers if p["category"] == c["id"])
        heading = f"{c['name']} {c['name_en']}" if language == "zh" else c["name_en"]
        lines.append(f"- [{heading}](#{github_anchor(heading)}){text['count'].format(count=count)}")

    for c in categories:
        cat_papers = sorted(
            (p for p in papers if p["category"] == c["id"]),
            key=lambda p: (-p["year"], p["title"]),
        )
        lines += [
            "",
            f"## {c['name']} {c['name_en']}" if language == "zh" else f"## {c['name_en']}",
            "",
            text["table_header"],
            "| :--- | :--- | :--- | :---: | :--- | :--- |",
        ]
        lines += [render_paper_row(p, language) for p in cat_papers]

    lines += [
        "",
        f"## {text['contributing']}",
        "",
        text["contribution_text"],
        "",
        "## License",
        "",
        text["license"],
        "",
    ]

    return "\n".join(lines)


def main() -> None:
    data = load_data()
    try:
        rendered = {language: render_readme(data, language) for language in README_FILES}
    except ValueError as error:
        sys.exit(str(error))
    for language, content in rendered.items():
        path = README_FILES[language]
        path.write_text(content, encoding="utf-8")
        print(f"Generated {path.name} with {len(data['papers'])} papers.")


if __name__ == "__main__":
    main()
