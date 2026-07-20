"""Create the one-time line-by-line portrait SVG from the clear PNG asset."""
from __future__ import annotations

import base64
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "deekshith-ascii-clear.png"
OUTPUT = ROOT / "deekshith-ascii-once.svg"


def png_size(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("deekshith-ascii-clear.png is not a valid PNG")
    return struct.unpack(">II", data[16:24])


def stepped(total: float, steps: int) -> tuple[str, str]:
    values = ";".join(f"{total * i / steps:.2f}" for i in range(steps + 1))
    times = ";".join(f"{i / steps:.5f}" for i in range(steps + 1))
    return values, times


def build_svg() -> str:
    data = SOURCE.read_bytes()
    width, height = png_size(data)
    if (width, height) != (666, 820):
        raise ValueError(f"unexpected clear portrait dimensions: {width}x{height}")
    uri = "data:image/png;base64," + base64.b64encode(data).decode("ascii")

    panel_w, panel_h = 760, 720
    image_x, image_y, image_w, image_h = 128, 74, 504, 620
    values, times = stepped(image_h, 58)
    scan = ";".join(f"{image_y + image_h * i / 58 - 3:.2f}" for i in range(59))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{panel_w}" height="{panel_h}" viewBox="0 0 {panel_w} {panel_h}" role="img" aria-labelledby="title desc" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<title id="title">Animated ASCII portrait of Deekshith</title><desc id="desc">A clear ASCII portrait that renders line by line once in a terminal panel.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient><clipPath id="reveal"><rect x="{image_x}" y="{image_y}" width="{image_w}" height="0"><animate attributeName="height" values="{values}" keyTimes="{times}" calcMode="discrete" begin="0.45s" dur="4.35s" fill="freeze" repeatCount="1"/></rect></clipPath><linearGradient id="scan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3fb950" stop-opacity="0"/><stop offset="0.5" stop-color="#3fb950" stop-opacity="0.9"/><stop offset="1" stop-color="#3fb950" stop-opacity="0"/></linearGradient></defs>
<rect width="760" height="720" rx="16" fill="url(#bg)"/><rect x="0.75" y="0.75" width="758.5" height="718.5" rx="15.25" fill="none" stroke="#30363d" stroke-width="1.5"/><line x1="0" y1="46" x2="760" y2="46" stroke="#30363d"/><circle cx="22" cy="23" r="6" fill="#ff5f56"/><circle cx="42" cy="23" r="6" fill="#ffbd2e"/><circle cx="62" cy="23" r="6" fill="#27c93f"/><text x="380" y="29" fill="#8b949e" font-size="15" text-anchor="middle">deekshith06@github: ~$ ascii-portrait.sh</text>
<rect x="24" y="62" width="712" height="610" rx="13" fill="#070a0f" stroke="#252d38"/><image href="{uri}" x="{image_x}" y="{image_y}" width="{image_w}" height="{image_h}" preserveAspectRatio="xMidYMid meet" clip-path="url(#reveal)"/><rect x="{image_x}" y="{image_y - 3}" width="{image_w}" height="3" fill="url(#scan)" opacity="0"><animate attributeName="y" values="{scan}" keyTimes="{times}" calcMode="discrete" begin="0.45s" dur="4.35s" fill="freeze" repeatCount="1"/><animate attributeName="opacity" values="0;0.8;0.8;0" keyTimes="0;0.03;0.96;1" begin="0.45s" dur="4.35s" fill="freeze" repeatCount="1"/></rect>
<g opacity="0"><text x="37" y="699" fill="#3fb950" font-size="14">&gt; portrait loaded successfully</text><rect x="270" y="686" width="8" height="16" fill="#c9d1d9"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" begin="4.85s" repeatCount="indefinite"/></rect><animate attributeName="opacity" from="0" to="1" begin="4.8s" dur="0.2s" fill="freeze"/></g></svg>'''


def main() -> None:
    svg = build_svg()
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
