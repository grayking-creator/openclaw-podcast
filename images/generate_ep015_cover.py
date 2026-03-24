#!/usr/bin/env python3
"""Generate Episode 015 cover art for OpenClaw Daily.
Theme: AI memory systems, layered memory tiers, vector embeddings, local-first privacy.
"""

from __future__ import annotations

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SIZE = 1400
OUTPUT_PATH = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_015_cover.png"

# Palette
BG_TOP = (8, 11, 24)
BG_BOTTOM = (2, 6, 15)
GRID_COLOR = (22, 40, 72)
CYAN = (61, 212, 247)
TEAL = (38, 220, 214)
BLUE = (88, 155, 255)
ORANGE = (255, 143, 64)
STEEL = (168, 184, 204)
WHITE = (245, 248, 255)

FONT_PATHS = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

def get_font(size: int, bold: bool = False):
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()

def gradient_background(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), BG_BOTTOM)
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        for x in range(size):
            px[x, y] = (r, g, b, 255)
    return img

def draw_grid(draw: ImageDraw.ImageDraw, size: int):
    spacing = 62
    for x in range(0, size + 1, spacing):
        alpha = 35 if x % (spacing * 2) == 0 else 16
        draw.line([(x, 0), (x, size)], fill=(*GRID_COLOR, alpha), width=1)
    for y in range(0, size + 1, spacing):
        alpha = 35 if y % (spacing * 2) == 0 else 16
        draw.line([(0, y), (size, y)], fill=(*GRID_COLOR, alpha), width=1)

    # Random circuit-like breaks
    random.seed(15)
    for _ in range(150):
        x = random.randint(0, size)
        y = random.randint(0, size)
        w = random.randint(16, 58)
        h = random.randint(8, 34)
        if random.random() > 0.5:
            draw.line([(x, y), (x + w, y)], fill=(*CYAN, 22), width=1)
        else:
            draw.line([(x, y), (x, y + h)], fill=(*CYAN, 22), width=1)


def draw_concentric_memory_rings(draw: ImageDraw.ImageDraw, center, max_radius: int):
    cx, cy = center
    rings = [110, 185, 260, 340, 425, 510]
    for idx, r in enumerate(rings):
        alpha = int(140 * (1 - idx / len(rings)))
        width = 4 + int((len(rings) - idx) * 0.5)
        if idx % 2 == 0:
            base = TEAL
        else:
            base = BLUE
        color = (*base, alpha)
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            outline=color,
            width=width,
        )


def add_vector_dots(img: Image.Image, center, count: int = 270):
    random.seed(15)
    draw = ImageDraw.Draw(img)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(layer)
    cx, cy = center
    for _ in range(count):
        # bias dots toward center field while keeping outer space busy
        ang = random.random() * 2 * math.pi
        dist = random.random() ** 1.25 * (SIZE * 0.45)
        x = int(cx + math.cos(ang) * dist + random.randint(-18, 18))
        y = int(cy + math.sin(ang) * dist + random.randint(-18, 18))
        r = random.randint(1, 3)
        col = (*CYAN, random.randint(70, 190))
        ldraw.ellipse([x - r, y - r, x + r, y + r], fill=col)
    ldraw = layer.filter(ImageFilter.GaussianBlur(0.8))
    img.paste(ldraw, (0, 0), ldraw)

    # Electric blue special nodes
    for _ in range(45):
        ang = random.random() * 2 * math.pi
        dist = random.random() ** 1.1 * (SIZE * 0.43)
        x = int(cx + math.cos(ang) * dist + random.randint(-10, 10))
        y = int(cy + math.sin(ang) * dist + random.randint(-10, 10))
        rr = random.randint(2, 4)
        draw.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(*BLUE, 220))


def draw_brain_icon(draw: ImageDraw.ImageDraw, center):
    cx, cy = center
    base_layer = [
        (cx - 210, cy - 20), (cx - 130, cy - 175), (cx - 30, cy - 155),
        (cx + 35, cy - 210), (cx + 150, cy - 145), (cx + 210, cy - 90),
        (cx + 130, cy + 5), (cx + 165, cy + 120), (cx + 75, cy + 180),
        (cx - 30, cy + 200), (cx - 150, cy + 140), (cx - 170, cy + 20)
    ]

    # Smooth polyline strokes
    for i in range(len(base_layer)):
        x1, y1 = base_layer[i]
        x2, y2 = base_layer[(i + 1) % len(base_layer)]
        for w, alpha in [(8, 18), (5, 80), (2, 200)]:
            draw.line([x1, y1, x2, y2], fill=(*BLUE, alpha), width=w)

    # Internal synapses
    inner = []
    for x, y in base_layer:
        inner.append((x + random.randint(-24, 24), y + random.randint(-24, 24)))

    for i in range(len(inner) - 3):
        p1 = inner[i]
        p2 = inner[(i + 4) % len(inner)]
        draw.line([p1, p2], fill=(*CYAN, 95), width=2)

    # Key nodes (orange accents)
    for i, (x, y) in enumerate(inner):
        if i % 3 != 0:
            continue
        draw.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(*CYAN, 38), outline=(0, 0, 0, 0))
        if i % 2 == 0:
            draw.ellipse([x - 6, y - 6, x + 6, y + 6], fill=ORANGE)

    # Privacy motif: tiny secure ring around lower-right node
    pr_x, pr_y = cx + 125, cy + 110
    draw.arc([pr_x - 34, pr_y - 28, pr_x + 26, pr_y + 42], 180, 0, fill=(*TEAL, 190), width=4)
    draw.line([(pr_x - 24, pr_y + 8), (pr_x + 10, pr_y + 8)], fill=(*TEAL, 190), width=4)
    draw.ellipse([pr_x - 6, pr_y - 6, pr_x + 6, pr_y + 6], fill=CYAN)


def draw_text(img: Image.Image, size: int):
    draw = ImageDraw.Draw(img)
    title_font = get_font(58)
    heading_font = get_font(170)
    subtitle_font = get_font(54)
    episode_font = get_font(72)

    # Top: OpenClaw Daily
    top = "OPENCLAW DAILY"
    tb = draw.textbbox((0, 0), top, font=title_font)
    tw = tb[2] - tb[0]
    tx = (size - tw) // 2
    ty = 48
    draw.text((tx, ty), top, font=title_font, fill=(*STEEL, 255))

    # center title
    main = "REMEMBER ME"
    mb = draw.textbbox((0, 0), main, font=heading_font)
    mw = mb[2] - mb[0]
    mx = (size - mw) // 2
    my = 560
    draw.text((mx, my), main, font=heading_font, fill=WHITE)

    # subtitle
    sub = "How We Built a Real Memory System for an AI Assistant"
    sb = draw.textbbox((0, 0), sub, font=subtitle_font)
    sw = sb[2] - sb[0]
    sx = (size - sw) // 2
    sy = my + 190
    draw.text((sx, sy), sub, font=subtitle_font, fill=(*CYAN, 255))

    # Episode number
    ep = "EP 015"
    eb = draw.textbbox((0, 0), ep, font=episode_font)
    ew = eb[2] - eb[0]
    ex = size - ew - 52
    ey = size - 86
    draw.text((ex, ey), ep, font=episode_font, fill=(*ORANGE, 255))


def main():
    img = gradient_background(SIZE)
    draw = ImageDraw.Draw(img, "RGBA")

    draw_grid(draw, SIZE)
    draw_concentric_memory_rings(draw, (SIZE // 2, SIZE // 2 + 20), SIZE)
    add_vector_dots(img, (SIZE // 2, SIZE // 2 + 20), count=340)
    draw_brain_icon(draw, (SIZE // 2, SIZE // 2 + 20))

    # Subtle vignette to keep focus center
    vignette = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for r in range(SIZE, 0, -6):
        alpha = int(190 * (1 - r / SIZE) ** 1.7)
        vdraw.ellipse(
            [SIZE // 2 - r // 2, SIZE // 2 - r // 2,
             SIZE // 2 + r // 2, SIZE // 2 + r // 2],
            outline=(0, 0, 0, alpha),
            width=6,
        )
    vignette = vignette.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img, vignette)

    draw_text(img, SIZE)
    img = img.convert("RGB")
    img.save(OUTPUT_PATH)
    print(f"Saved: { __import__('os').path.getsize(OUTPUT_PATH)} bytes")

if __name__ == "__main__":
    main()
