"""Generate neofetch-style profile cards (dark + light) as SVG."""
import math
import sys
from xml.sax.saxutils import escape

OUT_DIR = sys.argv[1]

# ---------- ASCII torus (static frame) ----------
W, H = 42, 23
CHARS = ".,-~:;=!*#$@"


def torus(A=1.15, B=0.45):
    out = [[" "] * W for _ in range(H)]
    lum = [[-1] * W for _ in range(H)]
    zbuf = [[0.0] * W for _ in range(H)]
    cA, sA, cB, sB = math.cos(A), math.sin(A), math.cos(B), math.sin(B)
    R1, R2, K2 = 1.0, 2.0, 5.0
    K1 = W * K2 * 3 / (8 * (R1 + R2)) * 0.95
    theta = 0.0
    while theta < 2 * math.pi:
        ct, st = math.cos(theta), math.sin(theta)
        phi = 0.0
        while phi < 2 * math.pi:
            cp, sp = math.cos(phi), math.sin(phi)
            cx, cy = R2 + R1 * ct, R1 * st
            x = cx * (cB * cp + sA * sB * sp) - cy * cA * sB
            y = cx * (sB * cp - sA * cB * sp) + cy * cA * cB
            z = K2 + cA * cx * sp + cy * sA
            ooz = 1 / z
            xp = int(W / 2 + K1 * ooz * x)
            yp = int(H / 2 - K1 * ooz * y * 0.5)
            L = cp * ct * sB - cA * ct * sp - sA * st + cB * (cA * st - ct * sA * sp)
            if 0 <= xp < W and 0 <= yp < H and L > 0 and ooz > zbuf[yp][xp]:
                zbuf[yp][xp] = ooz
                idx = min(int(L * 8), len(CHARS) - 1)
                out[yp][xp] = CHARS[idx]
                lum[yp][xp] = idx
            phi += 0.012
        theta += 0.04
    return out, lum


# ---------- Info panel ----------
TOTAL = 58  # characters per info line
INFO = [
    ("title", "ansh@cmu"),
    ("kv", "OS", "MS Information Systems & AI"),
    ("kv", "Host", "Carnegie Mellon University"),
    ("kv", "Uptime", "graduating Dec 2026"),
    ("kv", "Kernel", "B.E. Electronics, BITS Pilani"),
    ("kv", "Shell", "TA, ML in Production (17-645)"),
    ("kv", "Status", "open to full-time ML/AI roles '27"),
    ("blank",),
    ("section", "Experience"),
    ("kv", "Transient AI", "Applied AI Engineer Intern '26"),
    ("kv", "Tata AIG", "Lead SWE, ML & Cloud '23-'25"),
    ("kv", "Tata AIG", "Software Engineer, Backend '21-'23"),
    ("kv", "Petasense", "SWE Intern '21"),
    ("blank",),
    ("section", "Stack"),
    ("kv", "Languages", "Python, Java, JavaScript, C++"),
    ("kv", "ML", "PyTorch, scikit-learn, CUDA, FAISS"),
    ("kv", "Agents", "RAG, LangChain, agentic workflows"),
    ("kv", "Infra", "Kafka, K8s, Docker, AWS, GCP"),
    ("blank",),
    ("section", "Contact"),
    ("kv", "Email", "heyansh314@gmail.com"),
    ("kv", "LinkedIn", "in/ansh3491"),
    ("kv", "X", "@anshm3491"),
    ("kv", "Web", "anshbuilds.com"),
    ("blank",),
    ("section", "Shipped"),
    ("pair", "Docs automated", "30K+/mo", "Saved", "$1.3M/yr"),
    ("pair", "Securities/day", "80K", "Trading desks", "400+"),
]

THEMES = {
    "dark": dict(bg="#1a1b27", border="#2f334d", fg="#c0caf5", key="#bb9af7",
                 val="#7dcfff", dots="#414868", hl="#e0af68", title="#9ece6a",
                 ramp=["#3b4261", "#565f89", "#7aa2f7", "#7dcfff", "#bb9af7"]),
    "light": dict(bg="#f6f8fa", border="#d0d7de", fg="#24292f", key="#8250df",
                  val="#0550ae", dots="#afb8c1", hl="#bc4c00", title="#1a7f37",
                  ramp=["#d0d7de", "#8c959f", "#0969da", "#0550ae", "#8250df"]),
}

FONT = 15
LH = 20
PAD_Y = 34
ASCII_X = 24
INFO_X = 452
WIDTH = 1000
HEIGHT = PAD_Y + LH * (len(INFO) - 1) + 30


def kv_line(t, key, val):
    dots = TOTAL - len(key) - len(val) - 5
    return (f'<tspan class="cc">. </tspan><tspan class="k">{escape(key)}</tspan>:'
            f'<tspan class="cc"> {"." * dots} </tspan><tspan class="v">{escape(val)}</tspan>')


def pair_line(k1, v1, k2, v2):
    half = 29
    d1 = half - len(k1) - len(v1) - 5
    left = (f'<tspan class="cc">. </tspan><tspan class="k">{escape(k1)}</tspan>:'
            f'<tspan class="cc"> {"." * d1} </tspan><tspan class="h">{escape(v1)}</tspan>')
    d2 = TOTAL - half - len(k2) - len(v2) - 6
    right = (f'<tspan class="cc"> | </tspan><tspan class="k">{escape(k2)}</tspan>:'
             f'<tspan class="cc"> {"." * d2} </tspan><tspan class="h">{escape(v2)}</tspan>')
    return left + right


def build(theme):
    c = THEMES[theme]
    art, lum = torus()
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="\'JetBrains Mono\',\'Fira Code\',Consolas,\'DejaVu Sans Mono\',monospace" font-size="{FONT}px">',
        "<style>",
        f"text,tspan{{white-space:pre;fill:{c['fg']};font-variant-ligatures:none;font-feature-settings:\"liga\" 0,\"calt\" 0;}}",
        f".k{{fill:{c['key']};}} .v{{fill:{c['val']};}} .cc{{fill:{c['dots']};}}",
        f".h{{fill:{c['hl']};font-weight:bold;}} .t{{fill:{c['title']};font-weight:bold;}}",
        "".join(f".a{i}{{fill:{col};}}" for i, col in enumerate(c["ramp"])),
        "</style>",
        f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="14" fill="{c["bg"]}" stroke="{c["border"]}"/>',
    ]
    # ascii art, vertically centred against the info panel
    top = PAD_Y + ((len(INFO) - 1) * LH - (H - 1) * LH) / 2
    parts.append("<text>")
    for r in range(H):
        y = top + r * LH
        row = []
        for col in range(W):
            ch = art[r][col]
            if ch == " ":
                row.append(" ")
            else:
                band = min(lum[r][col] * len(c["ramp"]) // len(CHARS), len(c["ramp"]) - 1)
                row.append(f'<tspan class="a{band}">{escape(ch)}</tspan>')
        parts.append(f'<tspan x="{ASCII_X}" y="{y:.0f}">{"".join(row)}</tspan>')
    parts.append("</text>")
    # info panel
    parts.append("<text>")
    for i, item in enumerate(INFO):
        y = PAD_Y + i * LH
        kind = item[0]
        if kind == "blank":
            continue
        if kind == "title":
            body = (f'<tspan class="t">{escape(item[1])}</tspan>'
                    f'<tspan class="cc"> {"-" * (TOTAL - len(item[1]) - 1)}</tspan>')
        elif kind == "section":
            body = (f'<tspan class="cc">- </tspan><tspan class="t">{escape(item[1])}</tspan>'
                    f'<tspan class="cc"> {"-" * (TOTAL - len(item[1]) - 3)}</tspan>')
        elif kind == "kv":
            body = kv_line(theme, item[1], item[2])
        else:
            body = pair_line(*item[1:])
        parts.append(f'<tspan x="{INFO_X}" y="{y}">{body}</tspan>')
    parts.append("</text>")
    parts.append("</svg>")
    return "\n".join(parts)


for theme in THEMES:
    path = f"{OUT_DIR}/card-{theme}.svg"
    with open(path, "w") as f:
        f.write(build(theme))
    print("wrote", path)
