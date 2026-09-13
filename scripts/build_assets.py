#!/usr/bin/env python3
"""Build the static profile assets: header banner + tech stack card (dark & light).

The output is committed to assets/, so the README never depends on a third-party
image host at view time. Re-run after changing the stack or the banner text:

    python3 scripts/build_assets.py
"""
import base64
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(
        bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
        a1="#58a6ff", a2="#bc8cff", dot="#ffffff", dot_op="0.06", orb_op="0.30", edge="#30363d",
    ),
    "light": dict(
        bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#656d76",
        a1="#0969da", a2="#8250df", dot="#1f2328", dot_op="0.07", orb_op="0.14", edge="#d0d7de",
    ),
}

NAME = "Desperado"
PROMPT = "~/anhdenday"
ROLES = ("Fullstack Developer", "AI / ML Enthusiast")
LOCATION = "Vietnam"
HANDLE = "github.com/anhdenday"

# (group title, [(skillicons id, label), ...]) — ids: https://skillicons.dev/api/icons
STACK = [
    ("Languages", [("python", "Python"), ("c", "C"), ("java", "Java"), ("php", "PHP")]),
    ("AI / ML", [("tensorflow", "TensorFlow"), ("keras", "Keras"), ("pytorch", "PyTorch"), ("opencv", "OpenCV")]),
    ("Backend & Data", [("flask", "Flask"), ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("git", "Git")]),
]

# skillicons has no Keras icon; draw one in the same tile style (glyph from simple-icons, CC0).
KERAS_GLYPH = (
    "M24 0H0v24h24V0zM8.45 5.16l.2.17v6.24l6.46-6.45h1.96l.2.4-5.14 5.1 5.47 7.94-.2.3h-1.94"
    "l-4.65-6.88-2.16 2.08v4.6l-.19.2H7l-.2-.2V5.33l.17-.17h1.48z"
)
TILE = {"dark": "#242938", "light": "#F4F2ED"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def icon_svg(icon_id, theme):
    if icon_id == "keras":
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
            f'<rect width="256" height="256" rx="60" fill="{TILE[theme]}"/>'
            '<g transform="translate(56 56) scale(6)"><clipPath id="k"><rect width="24" height="24" rx="3"/></clipPath>'
            '<rect width="24" height="24" rx="3" fill="#FFFFFF"/>'
            f'<path clip-path="url(#k)" fill="#D00000" fill-rule="evenodd" d="{KERAS_GLYPH}"/></g></svg>'
        )
    url = f"https://skillicons.dev/icons?i={icon_id}&theme={theme}"
    req = urllib.request.Request(url, headers={"User-Agent": "anhdenday-profile-build"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def data_uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def build_header(theme):
    t = THEMES[theme]
    W, H = 1200, 280

    # Decorative neural net on the right: 4 layers, edges between consecutive layers.
    layers = [3, 4, 4, 2]
    xs = [850, 950, 1050, 1130]
    nodes = [[(x, 140 + (i - (n - 1) / 2) * 50) for i in range(n)] for x, n in zip(xs, layers)]
    edges = [(a, b) for l in range(len(nodes) - 1) for a in nodes[l] for b in nodes[l + 1]]

    edge_svg = "".join(
        f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{t["edge"]}" stroke-width="1.2"/>'
        for a, b in edges
    )
    # Signal pulses travelling along a subset of edges.
    pulses = []
    for k, (a, b) in enumerate(edges[::3]):
        pulses.append(
            f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="url(#pulse)" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-dasharray="16 400" stroke-dashoffset="16">'
            f'<animate attributeName="stroke-dashoffset" values="16;-150" dur="2.8s" begin="{k * 0.37:.2f}s" '
            f'repeatCount="indefinite"/></line>'
        )
    node_svg = []
    for l, layer in enumerate(nodes):
        for i, (x, y) in enumerate(layer):
            color = t["a1"] if (l + i) % 2 == 0 else t["a2"]
            node_svg.append(
                f'<circle cx="{x}" cy="{y}" r="7" fill="{t["bg"]}" stroke="{color}" stroke-width="2"/>'
                f'<circle cx="{x}" cy="{y}" r="2.5" fill="{color}">'
                f'<animate attributeName="r" values="2.5;4;2.5" dur="2.4s" begin="{(l + i) * 0.3:.1f}s" repeatCount="indefinite"/>'
                f"</circle>"
            )

    pin = (
        f'<path transform="translate(64 222) scale(0.75)" fill="{t["muted"]}" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 '
        '7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title">
  <title id="title">{esc(NAME)} — {esc(" · ".join(ROLES))} · {esc(LOCATION)}</title>
  <defs>
    <clipPath id="card"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16"/></clipPath>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="{t["dot"]}" fill-opacity="{t["dot_op"]}"/>
    </pattern>
    <radialGradient id="orb1"><stop offset="0" stop-color="{t["a1"]}" stop-opacity="{t["orb_op"]}"/><stop offset="1" stop-color="{t["a1"]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orb2"><stop offset="0" stop-color="{t["a2"]}" stop-opacity="{t["orb_op"]}"/><stop offset="1" stop-color="{t["a2"]}" stop-opacity="0"/></radialGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
      <stop offset="0" stop-color="{t["a1"]}"/><stop offset="1" stop-color="{t["a2"]}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1 0;0 0" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="pulse" gradientUnits="userSpaceOnUse" x1="800" y1="0" x2="1150" y2="0">
      <stop offset="0" stop-color="{t["a1"]}"/><stop offset="1" stop-color="{t["a2"]}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t["a1"]}"/><stop offset="1" stop-color="{t["a2"]}"/>
    </linearGradient>
  </defs>

  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    <circle cx="960" cy="40" r="300" fill="url(#orb1)">
      <animate attributeName="cx" values="960;1060;960" dur="16s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1120" cy="280" r="260" fill="url(#orb2)">
      <animate attributeName="cy" values="280;200;280" dur="12s" repeatCount="indefinite"/>
    </circle>
    <rect y="0" width="{W}" height="3" fill="url(#accent)"/>
  </g>

  <g font-family="{MONO}" font-size="16">
    <text x="64" y="74"><tspan fill="{t["a1"]}">{esc(PROMPT)}</tspan><tspan fill="{t["muted"]}"> $ whoami</tspan></text>
    <rect x="262" y="61" width="9" height="17" fill="{t["a1"]}">
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>
    </rect>
  </g>
  <text x="60" y="150" font-family="{SANS}" font-size="74" font-weight="800" letter-spacing="-1.5" fill="url(#name)">{esc(NAME)}</text>
  <text x="64" y="194" font-family="{SANS}" font-size="25" font-weight="600" fill="{t["text"]}">{esc(ROLES[0])}<tspan fill="{t["muted"]}" font-weight="400">  ·  </tspan>{esc(ROLES[1])}</text>
  {pin}
  <text x="86" y="236" font-family="{SANS}" font-size="16" fill="{t["muted"]}">{esc(LOCATION)}<tspan dx="14">|</tspan><tspan dx="14" font-family="{MONO}" font-size="15">{esc(HANDLE)}</tspan></text>

  <g>{edge_svg}</g>
  <g>{"".join(pulses)}</g>
  <g>{"".join(node_svg)}</g>
</svg>
"""


def build_stack(theme):
    t = THEMES[theme]
    group_w, gap, pad, icon, head, label_h = 292, 16, 20, 52, 50, 30
    H = head + icon + label_h + 14
    W = len(STACK) * group_w + (len(STACK) - 1) * gap
    slot = (group_w - 2 * pad) / 4

    # No entrance animation on purpose: static renderers (GitHub mobile, previews) only draw frame 0.
    parts = []
    for g, (title, items) in enumerate(STACK):
        gx = g * (group_w + gap)
        parts.append(
            f'<rect x="{gx + 0.5}" y="0.5" width="{group_w - 1}" height="{H - 1}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>'
            f'<rect x="{gx + pad}" y="22" width="3" height="14" rx="1.5" fill="url(#accent)"/>'
            f'<text x="{gx + pad + 11}" y="34" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="1.4" fill="{t["text"]}">{esc(title.upper())}</text>'
        )
        for i, (icon_id, label) in enumerate(items):
            cx = gx + pad + slot * i + slot / 2
            parts.append(
                f'<image x="{cx - icon / 2:.1f}" y="{head}" width="{icon}" height="{icon}" href="{data_uri(icon_svg(icon_id, theme))}"/>'
                f'<text x="{cx:.1f}" y="{head + icon + 21}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{t["muted"]}">{esc(label)}</text>'
            )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title">
  <title id="title">Tech stack: {esc("; ".join(f"{t_}: {', '.join(l for _, l in it)}" for t_, it in STACK))}</title>
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["a1"]}"/><stop offset="1" stop-color="{t["a2"]}"/>
    </linearGradient>
  </defs>
  {"".join(parts)}
</svg>
"""


def main():
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        (OUT / f"header-{theme}.svg").write_text(build_header(theme))
        (OUT / f"stack-{theme}.svg").write_text(build_stack(theme))
        print(f"built assets/header-{theme}.svg, assets/stack-{theme}.svg")


if __name__ == "__main__":
    main()
