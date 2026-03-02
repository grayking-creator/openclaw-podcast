#!/usr/bin/env python3
"""Episode 9 Cover Art Generator

Theme: OpenClaw v2026.3.1 — infrastructure maturity.
Visual: dark synthwave grid + central "gateway" node, surrounding nodes (Discord thread, Telegram topics, Android),
plus subtle heartbeat/health probe motif.

Outputs: images/ep009_cover.png (1400x1400)
"""

from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math
import random
from pathlib import Path

W, H = 1400, 1400
random.seed(9031)

out_path = Path(__file__).parent / "images" / "ep009_cover.png"
out_path.parent.mkdir(parents=True, exist_ok=True)

# Base background
img = Image.new("RGB", (W, H), (0, 0, 0))
draw = ImageDraw.Draw(img)

# Vertical gradient (deep navy -> near black)
for y in range(H):
    t = y / H
    r = int(0 + t * 4)
    g = int(0 + t * 3)
    b = int(18 + t * 20)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Subtle grid layer
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)

for x in range(0, W, 44):
    a = random.randint(8, 18)
    gd.line([(x, 0), (x, H)], fill=(0, 110, 170, a), width=1)
for y in range(0, H, 44):
    a = random.randint(8, 18)
    gd.line([(0, y), (W, y)], fill=(0, 110, 170, a), width=1)

img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")

# Glow layer
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
lg = ImageDraw.Draw(glow)

# Node layout
cx, cy = 700, 560

nodes = [
    # central gateway
    {"x": cx, "y": cy, "r": 60, "c": (0, 220, 255)},
    # Discord thread (purple)
    {"x": cx - 250, "y": cy - 120, "r": 30, "c": (190, 70, 255)},
    # Telegram topics (blue)
    {"x": cx + 260, "y": cy - 90, "r": 32, "c": (0, 160, 255)},
    # Android node (orange)
    {"x": cx + 200, "y": cy + 180, "r": 34, "c": (255, 140, 0)},
    # Container probes (green-cyan)
    {"x": cx - 220, "y": cy + 210, "r": 28, "c": (0, 255, 200)},
]

# Connections
connections = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 3)]
for i, j in connections:
    n1, n2 = nodes[i], nodes[j]
    r, g, b = n1["c"]
    lg.line([(n1["x"], n1["y"]), (n2["x"], n2["y"])], fill=(r, g, b, 40), width=10)
    lg.line([(n1["x"], n1["y"]), (n2["x"], n2["y"])], fill=(r, g, b, 90), width=3)
    lg.line([(n1["x"], n1["y"]), (n2["x"], n2["y"])], fill=(255, 255, 255, 40), width=1)

# Draw nodes with multi-glow
for n in nodes:
    x, y, rad = n["x"], n["y"], n["r"]
    r, g, b = n["c"]
    # outer glow
    lg.ellipse([(x - rad - 18, y - rad - 18), (x + rad + 18, y + rad + 18)], fill=(r, g, b, 12))
    lg.ellipse([(x - rad - 10, y - rad - 10), (x + rad + 10, y + rad + 10)], fill=(r, g, b, 28))
    lg.ellipse([(x - rad - 4, y - rad - 4), (x + rad + 4, y + rad + 4)], fill=(r, g, b, 60))
    # core
    lg.ellipse([(x - rad, y - rad), (x + rad, y + rad)], fill=(r, g, b, 120))
    lg.ellipse([(x - rad // 2, y - rad // 2), (x + rad // 2, y + rad // 2)], fill=(255, 255, 255, 110))

# Heartbeat line motif (health probes)
base_y = 980
x0, x1 = 180, 1220
pts = [
    (x0, base_y),
    (420, base_y),
    (480, base_y - 60),
    (540, base_y + 90),
    (600, base_y - 40),
    (680, base_y),
    (x1, base_y),
]
lg.line(pts, fill=(0, 220, 255, 70), width=10, joint="curve")
lg.line(pts, fill=(0, 220, 255, 160), width=3, joint="curve")

# Speckles
for _ in range(120):
    px = random.randint(80, W - 80)
    py = random.randint(80, H - 80)
    a = random.randint(40, 160)
    c = random.choice([
        (0, 220, 255, a),
        (190, 70, 255, a),
        (255, 140, 0, a),
        (0, 255, 200, a),
        (255, 255, 255, a),
    ])
    s = random.randint(1, 3)
    lg.ellipse([(px - s, py - s), (px + s, py + s)], fill=c)

# Composite glow with blur
base = img.convert("RGBA")
blur = glow.filter(ImageFilter.GaussianBlur(radius=6))
combo = ImageChops.screen(base, blur)
combo = ImageChops.screen(combo, glow)

# Bottom fade for text area
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for i in range(520):
    a = int(220 * (i / 520))
    od.rectangle([0, H - 520 + i, W, H - 520 + i + 1], fill=(0, 0, 0, a))
combo = Image.alpha_composite(combo, overlay)

final = combo.convert("RGB")
final.save(out_path)
print(f"Wrote {out_path}")
