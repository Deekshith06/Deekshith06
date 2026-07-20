"""Build the equal-size terminal profile card used beside the portrait."""

from __future__ import annotations

import html
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "info-card.svg"
STATIC = bool(os.environ.get("STATIC"))

W, H = 760, 720
PAD, TITLEBAR_H = 26, 46
KEY_X, COLON_X, VAL_X = 28, 180, 208
BG, BG2, FRAME, INNER = "#0d1117", "#111722", "#30363d", "#070a0f"
MUTED, INK, KEY = "#8b949e", "#c9d1d9", "#ffa657"
SECTION, GREEN, ACCENT = "#58a6ff", "#3fb950", "#22d3ee"

ROWS = [
    ("host",),
    ("kv", "Status", "AI/ML Engineer · Full-Stack Developer"),
    ("kv", "Degree", "B.Tech, Computer Science & Engineering"),
    ("kv", "University", "Lovely Professional University"),
    ("kv", "Graduation", "Expected 2027"),
    ("gap",),
    ("sec", "Core Stack"),
    ("kv", "Languages", "Java, Python, C, C++"),
    ("kv", "Frontend", "React, TypeScript, HTML, CSS"),
    ("kv", "Backend", "Spring Boot, Node.js, REST APIs"),
    ("kv", "AI / ML", "Machine Learning, NLP, Computer Vision"),
    ("kv", "Tools", "Git, GitHub, Docker, Vercel"),
    ("gap",),
    ("sec", "Current Focus"),
    ("bul", "Production-focused student projects"),
    ("bul", "Logistics, finance and language AI"),
]


def esc(value: str) -> str:
    return html.escape(value)


def reveal(inner: str, index: int, y: float, width: int = 690) -> str:
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.38 + index * 0.16
    clip_id = f"line{index}"
    return (
        f'<defs><clipPath id="{clip_id}"><rect x="{PAD}" y="{y - 18:.1f}" width="0" height="25">'
        f'<animate attributeName="width" from="0" to="{width}" begin="{delay:.2f}s" dur="0.30s" '
        f'fill="freeze" repeatCount="1"/></rect></clipPath></defs>'
        f'<g clip-path="url(#{clip_id})">{inner}</g>'
    )


def build_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-labelledby="title desc" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<title id="title">Deekshith profile information</title>',
        '<desc id="desc">AI/ML engineer and full-stack developer, B.Tech Computer Science and Engineering student at Lovely Professional University, graduating in 2027.</desc>',
        '<defs><linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="16" fill="url(#ibg)"/>',
        f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="15.25" fill="none" stroke="{FRAME}" stroke-width="1.5"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    for index, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        parts.append(f'<circle cx="{22 + index * 20}" cy="23" r="6" fill="{color}"/>')

    parts.extend(
        [
            f'<text x="{W / 2}" y="29" fill="{MUTED}" font-size="15" text-anchor="middle">deekshith06@github: ~$ neofetch</text>',
            f'<rect x="22" y="60" width="716" height="638" rx="13" fill="{INNER}" stroke="#252d38"/>',
        ]
    )

    y = 91.0
    line_index = 0
    for row in ROWS:
        kind = row[0]
        if kind == "gap":
            y += 10
            continue
        if kind == "host":
            inner = (
                f'<text x="{KEY_X}" y="{y:.1f}" font-size="18" font-weight="800">'
                f'<tspan fill="{GREEN}">deekshith06</tspan><tspan fill="{MUTED}">@</tspan>'
                f'<tspan fill="{ACCENT}">github</tspan></text>'
                f'<line x1="220" y1="{y - 6:.1f}" x2="712" y2="{y - 6:.1f}" stroke="{FRAME}"/>'
            )
            y += 36
        elif kind == "sec":
            title = esc(row[1])
            inner = (
                f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="16" font-weight="800">— {title}</text>'
                f'<line x1="190" y1="{y - 6:.1f}" x2="712" y2="{y - 6:.1f}" stroke="{FRAME}"/>'
            )
            y += 34
        elif kind == "kv":
            key, value = esc(row[1]), esc(row[2])
            inner = (
                f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="15" font-weight="800">{key}</text>'
                f'<text x="{COLON_X}" y="{y:.1f}" fill="{KEY}" font-size="15">:</text>'
                f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="15">{value}</text>'
            )
            y += 31
        elif kind == "bul":
            text = esc(row[1])
            inner = (
                f'<circle cx="{KEY_X + 5}" cy="{y - 5:.1f}" r="3.5" fill="{GREEN}"/>'
                f'<text x="{KEY_X + 22}" y="{y:.1f}" fill="{INK}" font-size="15">{text}</text>'
            )
            y += 29
        else:
            continue
        parts.append(reveal(inner, line_index, y - (36 if kind == "host" else 31)))
        line_index += 1

    mission_y = 593
    mission = (
        f'<rect x="28" y="{mission_y}" width="704" height="82" rx="10" fill="#08120d" stroke="{GREEN}" stroke-opacity="0.8"/>'
        f'<text x="48" y="{mission_y + 31}" fill="{GREEN}" font-size="18">*</text>'
        f'<text x="78" y="{mission_y + 31}" fill="{INK}" font-size="15.5" font-weight="700">I am an AI/ML Engineer and Full-Stack Developer.</text>'
        f'<text x="48" y="{mission_y + 61}" fill="{SECTION}" font-size="18">&gt;</text>'
        f'<text x="78" y="{mission_y + 61}" fill="{INK}" font-size="15.5">Using AI, I build fully working websites.</text>'
    )
    parts.append(reveal(mission, line_index + 1, mission_y + 35, width=704))
    parts.append('</svg>')
    return ''.join(parts)


def main() -> None:
    svg = build_svg()
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT} {len(svg)} bytes; {W}x{H}")


if __name__ == "__main__":
    main()
