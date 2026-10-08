#!/usr/bin/env python3
"""Render monthly paper-count charts from shared data.

Usage: python scripts/generate_monthly_chart.py [--language all|zh|en]
Requires: pyyaml, matplotlib
"""

import argparse
import datetime
import re
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

from generate_readme import ROOT, last_updated, load_data


def monthly_counts(data):
    cutoff = datetime.date.fromisoformat(last_updated(data["meta"]))
    counts = {category["id"]: Counter() for category in data["categories"]}
    for paper in data["papers"]:
        arxiv = str(paper.get("links", {}).get("arxiv", ""))
        match = re.match(r"^(\d{2})(\d{2})\.", arxiv)
        if not match:
            continue
        year, month = 2000 + int(match[1]), int(match[2])
        if 1 <= month <= 12 and (year, month) <= (cutoff.year, cutoff.month):
            counts[paper["category"]][f"{year:04d}-{month:02d}"] += 1
    first = min((month for counter in counts.values() for month in counter), default=cutoff.strftime("%Y-%m"))
    year, month = map(int, first.split("-"))
    months = []
    while (year, month) <= (cutoff.year, cutoff.month):
        months.append(f"{year:04d}-{month:02d}")
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    return months, counts, cutoff


def render_chart(data, language):
    months, counts, cutoff = monthly_counts(data)
    if language == "zh":
        available = {font.name for font in font_manager.fontManager.ttflist}
        chinese_font = next((name for name in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "WenQuanYi Zen Hei") if name in available), None)
        if not chinese_font:
            raise SystemExit("A Chinese font is needed for the Chinese chart; use --language en or install a CJK font.")
        font = chinese_font
    else:
        font = "DejaVu Sans"
    with plt.rc_context({"font.family": font, "axes.unicode_minus": False}):
        fig, ax = plt.subplots(figsize=(16.13, 7.4), dpi=100)
        fig.subplots_adjust(left=0.05, right=0.977, top=0.90, bottom=0.125)
        colors = {"driving": "#ee7733", "embodied": "#3973e8", "general": "#7b61bf"}
        for category in data["categories"]:
            values = [counts[category["id"]][month] for month in months]
            label = category["name"] if language == "zh" else category["name_en"]
            color = colors.get(category["id"])
            ax.plot(range(len(months)), values, color=color, linewidth=2.7, marker="o", markersize=7, label=label)
            peak = max(values)
            index = values.index(peak)
            ax.annotate(str(peak), (index, peak), xytext=(0, 12), textcoords="offset points", ha="center", fontsize=14, color=color)
        ticks = sorted({0, len(months) - 1} | {i for i, month in enumerate(months) if month.endswith(("-01", "-07"))})
        ax.set_xticks(ticks, [months[i] for i in ticks], fontsize=13)
        ax.set_xlim(-0.4, len(months) - 0.6)
        ax.set_ylim(0, max((max(counter.values(), default=0) for counter in counts.values()), default=0) * 1.22 + 1)
        ax.set_title("各类别每月收录篇数" if language == "zh" else "Monthly paper counts by category", fontsize=22, pad=18)
        ax.set_ylabel("篇数" if language == "zh" else "Papers", fontsize=16)
        ax.grid(axis="y", color="#e5e5e5", linewidth=1)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#cccccc")
        ax.tick_params(axis="both", length=0, colors="#666666")
        ax.tick_params(axis="y", labelsize=15, pad=8)
        ax.legend(loc="upper left", frameon=False, ncol=len(data["categories"]), fontsize=14)
        caption = (
            f"月份取自 arXiv 编号。截至 {cutoff.isoformat()}；当前月份仅统计到更新日。"
            if language == "zh" else
            f"Months are taken from arXiv IDs. Updated {cutoff.isoformat()}; the current month is partial."
        )
        fig.text(0.12, 0.035, caption, fontsize=13, color="#777777")
        name = "monthly-paper-counts.png" if language == "zh" else "monthly-paper-counts.en.png"
        path = ROOT / "assets" / name
        fig.savefig(path, facecolor="white")
        plt.close(fig)
        print(f"Generated assets/{name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=("all", "zh", "en"), default="all")
    args = parser.parse_args()
    data = load_data()
    for language in (("zh", "en") if args.language == "all" else (args.language,)):
        render_chart(data, language)


if __name__ == "__main__":
    main()
