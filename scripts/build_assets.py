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

# (group title, [(icon id, label), ...]) — laid out 2 panels per row, 4 icons per line.
# ids: https://skillicons.dev/api/icons, or a key of CUSTOM_GLYPHS / "qdrant" below.
STACK = [
    ("Languages", [("python", "Python"), ("c", "C"), ("java", "Java"), ("php", "PHP")]),
    ("Frontend", [("react", "React"), ("redux", "Redux"), ("typescript", "TypeScript"), ("tailwindcss", "Tailwind CSS")]),
    ("AI / ML", [
        ("tensorflow", "TensorFlow"), ("keras", "Keras"), ("pytorch", "PyTorch"), ("opencv", "OpenCV"),
        ("langchain", "LangChain"), ("qdrant", "Qdrant"), ("neo4j", "Neo4j"),
    ]),
    ("Backend & Data", [
        ("flask", "Flask"), ("fastapi", "FastAPI"), ("celery", "Celery"), ("redis", "Redis"),
        ("mysql", "MySQL"), ("mongodb", "MongoDB"), ("docker", "Docker"), ("git", "Git"),
    ]),
]

TILE = {"dark": "#242938", "light": "#F4F2ED"}

# Icons skillicons lacks, drawn in the same tile style. 24x24 glyphs from simple-icons (CC0).
# id: (path, {theme: color}, square) — square logos are cut-out glyphs laid on a white plate.
CUSTOM_GLYPHS = {
    "keras": (
        "M24 0H0v24h24V0zM8.45 5.16l.2.17v6.24l6.46-6.45h1.96l.2.4-5.14 5.1 5.47 7.94-.2.3h-1.94"
        "l-4.65-6.88-2.16 2.08v4.6l-.19.2H7l-.2-.2V5.33l.17-.17h1.48z",
        {"dark": "#D00000", "light": "#D00000"}, True,
    ),
    "celery": (
        "M2.303 0A2.298 2.298 0 0 0 0 2.303v19.394A2.298 2.298 0 0 0 2.303 24h19.394A2.298 2.298 0 0 0 24 21.697"
        "V2.303A2.298 2.298 0 0 0 21.697 0zm8.177 3.072c4.098 0 7.028 1.438 7.68 1.764l-1.194 2.55c-2.442-1.057"
        "-4.993-1.41-5.672-1.41-1.574 0-2.17.922-2.17 1.763v8.494c0 .869.596 1.791 2.17 1.791.679 0 3.23-.38 "
        "5.672-1.41l1.194 2.496c-.435.271-3.637 1.818-7.68 1.818-1.112 0-4.64-.244-4.64-4.64V7.713c0-4.397 "
        "3.528-4.64 4.64-4.64z",
        {"dark": "#37814A", "light": "#37814A"}, True,
    ),
    # Brand #7FC8FF is unreadable on the light tile; the logo's dark teal is used there.
    "langchain": (
        "M13.796 0a6.93 6.93 0 0 0-4.91 2.019L5.451 5.455l3.273 3.27 3.432-3.432a2.284 2.284 0 0 1 3.277 0 "
        "2.28 2.28 0 0 1 0 3.275L12 12.001l3.273 3.273 3.433-3.435c2.692-2.692 2.692-7.127 0-9.82A6.92 6.92 0 0 0 "
        "13.796 0m-5.07 8.728-3.433 3.434c-2.692 2.693-2.692 7.126 0 9.819A6.92 6.92 0 0 0 10.203 24a6.93 6.93 0 0 0 "
        "4.911-2.02l3.432-3.432-3.271-3.272-3.433 3.433a2.284 2.284 0 0 1-3.277 0 2.28 2.28 0 0 1 0-3.276L12 12z",
        {"dark": "#7FC8FF", "light": "#1C3C3C"}, False,
    ),
    "neo4j": (
        "M9.629 13.227c-.593 0-1.139.2-1.58.533l-2.892-1.976a2.61 2.61 0 0 0 .101-.711 2.633 2.633 0 0 0-2.629-2.629"
        "A2.632 2.632 0 0 0 0 11.073a2.632 2.632 0 0 0 2.629 2.629c.593 0 1.139-.2 1.579-.533L7.1 15.145c-.063.226"
        "-.1.465-.1.711 0 .247.037.484.1.711l-2.892 1.976a2.608 2.608 0 0 0-1.579-.533A2.632 2.632 0 0 0 0 20.639"
        "a2.632 2.632 0 0 0 2.629 2.629 2.632 2.632 0 0 0 2.629-2.629c0-.247-.037-.485-.101-.711l2.892-1.976c.441"
        ".333.987.533 1.58.533a2.633 2.633 0 0 0 2.629-2.629c0-1.45-1.18-2.629-2.629-2.629ZM16.112.732c-4.72 0-7.888 "
        "2.748-7.888 8.082v3.802a3.525 3.525 0 0 1 3.071.008v-3.81c0-3.459 1.907-5.237 4.817-5.237s4.817 1.778 4.817 "
        "5.237v8.309H24V8.814C24 3.448 20.832.732 16.112.732Z",
        {"dark": "#4581C3", "light": "#4581C3"}, False,
    ),
}

# Official Qdrant logomark (qdrant.tech brand resources), viewBox 0 0 346.42 400: (fill, points).
QDRANT_MARK = [
    ("#dc244c", "173.21 0 0 100 0 300 173.21 400 238.16 362.5 238.16 287.5 173.21 325 64.96 262.5 64.96 137.5 "
                "173.21 75 281.46 137.5 281.46 387.5 346.42 350 346.42 100 173.21 0"),
    ("#dc244c", "108.26 162.5 108.26 237.5 173.21 275 238.16 237.5 238.16 162.5 173.21 125 108.26 162.5"),
    ("#9e0d38", "238.16 287.5 238.16 362.5 173.21 400 173.21 325 238.16 287.5"),
    ("#9e0d38", "346.42 100 346.42 350 281.46 387.5 281.46 137.5 346.42 100"),
    ("#ff516b", "346.42 100 281.46 137.5 173.21 75 64.96 137.5 0 100 173.21 0 346.42 100"),
    ("#dc244c", "173.21 325 173.21 400 0 300 0 100 64.96 137.5 64.96 262.5 173.21 325"),
    ("#ff516b", "238.16 162.5 173.21 200 108.26 162.5 173.21 125 238.16 162.5"),
    ("#dc244c", "173.21 200 173.21 275 108.26 237.5 108.26 162.5 173.21 200"),
    ("#9e0d38", "238.16 162.5 238.16 237.5 173.21 275 173.21 200 238.16 162.5"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def icon_svg(icon_id, theme):
    tile = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">'
        f'<rect width="256" height="256" rx="60" fill="{TILE[theme]}"/>'
    )
    if icon_id == "qdrant":
        mark = "".join(f'<polygon fill="{fill}" points="{pts}"/>' for fill, pts in QDRANT_MARK)
        return f'{tile}<svg x="63" y="54" width="130" height="148" viewBox="0 0 346.42 400">{mark}</svg></svg>'
    if icon_id in CUSTOM_GLYPHS:
        path, colors, square = CUSTOM_GLYPHS[icon_id]
        glyph = f'<path fill="{colors[theme]}" d="{path}"/>'
        if square:
            glyph = (
                '<clipPath id="c"><rect width="24" height="24" rx="3"/></clipPath>'
                '<rect width="24" height="24" rx="3" fill="#FFFFFF"/>'
                f'<path clip-path="url(#c)" fill="{colors[theme]}" fill-rule="evenodd" d="{path}"/>'
            )
        return f'{tile}<g transform="translate(56 56) scale(6)">{glyph}</g></svg>'
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
    cols, per_row = 2, 4
    group_w, gap, pad, icon, head, cell_h, row_gap, bottom = 446, 16, 20, 52, 50, 82, 10, 14
    W = cols * group_w + (cols - 1) * gap
    slot = (group_w - 2 * pad) / per_row

    # No entrance animation on purpose: static renderers (GitHub mobile, previews) only draw frame 0.
    parts = []
    y = 0
    for grid_row in (STACK[i:i + cols] for i in range(0, len(STACK), cols)):
        # Panels on the same grid row share the height of the tallest one.
        lines = max(-(-len(items) // per_row) for _, items in grid_row)
        h = head + lines * cell_h + (lines - 1) * row_gap + bottom
        for g, (title, items) in enumerate(grid_row):
            gx = g * (group_w + gap)
            parts.append(
                f'<rect x="{gx + 0.5}" y="{y + 0.5}" width="{group_w - 1}" height="{h - 1}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>'
                f'<rect x="{gx + pad}" y="{y + 22}" width="3" height="14" rx="1.5" fill="url(#accent)"/>'
                f'<text x="{gx + pad + 11}" y="{y + 34}" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="1.4" fill="{t["text"]}">{esc(title.upper())}</text>'
            )
            for k, (icon_id, label) in enumerate(items):
                line, col = divmod(k, per_row)
                cx = gx + pad + slot * col + slot / 2
                iy = y + head + line * (cell_h + row_gap)
                parts.append(
                    f'<image x="{cx - icon / 2:.1f}" y="{iy}" width="{icon}" height="{icon}" href="{data_uri(icon_svg(icon_id, theme))}"/>'
                    f'<text x="{cx:.1f}" y="{iy + icon + 21}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{t["muted"]}">{esc(label)}</text>'
                )
        y += h + gap
    H = y - gap

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
