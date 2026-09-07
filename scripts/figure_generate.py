#!/usr/bin/env python3
"""Generate assets/interactive-world-model.svg (and .png when a headless
Chrome is available, since some Markdown previews do not render SVG).

Usage:
    python3 scripts/generate_figure.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
FIGURE_FILE = ASSETS_DIR / "interactive-world-model.svg"
PNG_FILE = ASSETS_DIR / "interactive-world-model.png"


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for name in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    for path in candidates:
        if Path(path).exists():
            return path
    return ""


def render_png() -> None:
    chrome = find_chrome()
    if not chrome:
        print("Warning: no headless Chrome found, PNG not updated.", file=sys.stderr)
        return
    subprocess.run(
        [
            chrome, "--headless", "--disable-gpu",
            f"--screenshot={PNG_FILE}",
            "--window-size=960,430",
            "--default-background-color=ffffffff",
            f"file://{FIGURE_FILE}",
        ],
        check=True,
        capture_output=True,
    )

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="960" height="430" viewBox="0 0 960 430"
     font-family="-apple-system, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif">
  <defs>
    <marker id="arrowBlue" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M1,1 L11,6 L1,11 Z" fill="#0969da"/>
    </marker>
    <marker id="arrowGreen" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M1,1 L11,6 L1,11 Z" fill="#1a7f37"/>
    </marker>
    <marker id="arrowGray" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M1,1 L9,5 L1,9 Z" fill="#b58a1b"/>
    </marker>
  </defs>

  <rect x="1" y="1" width="958" height="428" rx="20" fill="#fbfdff" stroke="#d0d7de" stroke-width="2"/>

  <!-- Agent / Policy -->
  <rect x="70" y="130" width="230" height="130" rx="16" fill="#ddf4ff" stroke="#0969da" stroke-width="2"/>
  <text x="185" y="178" text-anchor="middle" font-size="22" font-weight="700" fill="#0a3069">智能体 / 策略</text>
  <text x="185" y="208" text-anchor="middle" font-size="15" fill="#0550ae">感知状态 → 做出决策</text>
  <text x="185" y="234" text-anchor="middle" font-size="13" fill="#539bf5">Agent / Policy</text>

  <!-- Interactive World Model -->
  <rect x="520" y="95" width="380" height="200" rx="16" fill="#fff8c5" stroke="#9a6700" stroke-width="2"/>
  <text x="710" y="136" text-anchor="middle" font-size="22" font-weight="700" fill="#4d2d00">交互式世界模型</text>
  <text x="710" y="164" text-anchor="middle" font-size="15" fill="#6e5600">学习环境动态 · 以动作为条件预测未来</text>

  <!-- rollout frames -->
  <rect x="560" y="195" width="80" height="52" rx="6" fill="#ffffff" stroke="#b58a1b" stroke-width="1.5"/>
  <text x="600" y="227" text-anchor="middle" font-size="15" fill="#6e5600">ô<tspan dy="4" font-size="11">t+1</tspan></text>
  <line x1="644" y1="221" x2="664" y2="221" stroke="#b58a1b" stroke-width="1.5" marker-end="url(#arrowGray)"/>
  <rect x="670" y="195" width="80" height="52" rx="6" fill="#ffffff" stroke="#b58a1b" stroke-width="1.5"/>
  <text x="710" y="227" text-anchor="middle" font-size="15" fill="#6e5600">ô<tspan dy="4" font-size="11">t+2</tspan></text>
  <line x1="754" y1="221" x2="774" y2="221" stroke="#b58a1b" stroke-width="1.5" marker-end="url(#arrowGray)"/>
  <rect x="780" y="195" width="80" height="52" rx="6" fill="#ffffff" stroke="#b58a1b" stroke-width="1.5"/>
  <text x="820" y="227" text-anchor="middle" font-size="15" fill="#6e5600">ô<tspan dy="4" font-size="11">t+3</tspan></text>
  <text x="710" y="276" text-anchor="middle" font-size="13" fill="#8a6d00">想象推演（rollout）：预测未来观测序列</text>

  <!-- action arrow: agent -> world model -->
  <path d="M 302 158 C 380 108, 445 108, 516 138" fill="none" stroke="#0969da" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
  <text x="408" y="102" text-anchor="middle" font-size="16" font-weight="600" fill="#0969da">动作 a<tspan dy="4" font-size="12">t</tspan></text>

  <!-- observation arrow: world model -> agent -->
  <path d="M 518 252 C 445 300, 375 300, 306 262" fill="none" stroke="#1a7f37" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
  <text x="412" y="316" text-anchor="middle" font-size="16" font-weight="600" fill="#1a7f37">观测 / 奖励 ô<tspan dy="4" font-size="12">t+1</tspan></text>

  <!-- feature chips -->
  <g font-size="15" fill="#24292f">
    <rect x="52" y="345" width="205" height="48" rx="24" fill="#ffffff" stroke="#d0d7de" stroke-width="1.5"/>
    <text x="154" y="375" text-anchor="middle">🎮 动作条件生成</text>
    <rect x="269" y="345" width="205" height="48" rx="24" fill="#ffffff" stroke="#d0d7de" stroke-width="1.5"/>
    <text x="371" y="375" text-anchor="middle">⚡ 实时推理</text>
    <rect x="486" y="345" width="205" height="48" rx="24" fill="#ffffff" stroke="#d0d7de" stroke-width="1.5"/>
    <text x="588" y="375" text-anchor="middle">🔁 闭环支持</text>
    <rect x="703" y="345" width="205" height="48" rx="24" fill="#ffffff" stroke="#d0d7de" stroke-width="1.5"/>
    <text x="805" y="375" text-anchor="middle">⏳ 长时序一致性</text>
  </g>
</svg>
"""


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_FILE.write_text(SVG, encoding="utf-8")
    print(f"Generated {FIGURE_FILE.relative_to(ROOT)}.")
    render_png()
    if PNG_FILE.is_file():
        print(f"Generated {PNG_FILE.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
