from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

W, H = 1400, 1400
OUT = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_017_cover.png"

# Colors
TOP_BG = (0x0A, 0x0A, 0x1A)
BOT_BG = (0x00, 0x00, 0x05)
ELEC_BLUE = (0x00, 0xAA, 0xFF)
CYAN = (0x00, 0xCC, 0xFF)
PURPLE = (0x66, 0x00, 0xCC)
WHITE = (245, 248, 255)
GRID1 = (22, 42, 88, 26)
GRID2 = (32, 74, 130, 32)

img = Image.new("RGB", (W, H), BOT_BG)
d = ImageDraw.Draw(img)

# 1) Vertical gradient background
for y in range(H):
    t = y / (H - 1)
    r = int(TOP_BG[0] * (1 - t) + BOT_BG[0] * t)
    g = int(TOP_BG[1] * (1 - t) + BOT_BG[1] * t)
    b = int(TOP_BG[2] * (1 - t) + BOT_BG[2] * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# 2) circuit/grid overlay
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for x in range(0, W, 66):
    od.line([(x, 0), (x, H)], fill=GRID1, width=1)
for y in range(0, H, 66):
    od.line([(0, y), (W, y)], fill=GRID1, width=1)

for y in range(120, H - 320, 165):
    od.line([(70, y), (290, y), (290, y + 34), (530, y + 34)], fill=GRID2, width=2)
    od.ellipse((525, y + 28, 535, y + 38), outline=(45, 95, 185, 36), width=2)
for y in range(190, H - 250, 165):
    od.line([(W - 70, y), (W - 290, y), (W - 290, y + 42), (W - 530, y + 42)], fill=GRID2, width=2)
    od.ellipse((W - 535, y + 37, W - 525, y + 47), outline=(45, 95, 185, 36), width=2)
img = Image.alpha_composite(img.convert("RGBA"), overlay)


# Utility glow painter

def glow_polygon(base, points, color, glow_radius=26, glow_alpha=120, width=0):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    if width == 0:
        gd.polygon(points, fill=color + (glow_alpha,))
    else:
        gd.line(points + [points[0]], fill=color + (glow_alpha,), width=width)
    g = g.filter(ImageFilter.GaussianBlur(glow_radius))
    return Image.alpha_composite(base, g)


def glow_circle(base, x, y, radius, color, glow_radius=26, glow_alpha=130, fill_alpha=255):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color + (glow_alpha,))
    g = g.filter(ImageFilter.GaussianBlur(glow_radius))
    base = Image.alpha_composite(base, g)

    d2 = ImageDraw.Draw(base)
    d2.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color + (fill_alpha,))
    return base

# 3) Centered hierarchical node tree
root = (W // 2, 380)
children = [
    (W // 2 - 280, 620),
    (W // 2, 620),
    (W // 2 + 280, 620),
]
grandchildren = []
for cx, cy in children:
    grandchildren.append((cx - 95, 860))
    grandchildren.append((cx + 95, 860))

node_colors = [ELEC_BLUE, CYAN, PURPLE]

def glow_line(base, p1, p2, color, width=6, blur=12, alpha=160):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.line([p1, p2], fill=color + (alpha,), width=width)
    g = g.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base, g)

# root->children
for i, c in enumerate(children):
    color = node_colors[i % len(node_colors)]
    img = glow_line(img, root, c, color, width=8, blur=18, alpha=170)

# children->grandchildren
for i, child in enumerate(children):
    col = node_colors[i % len(node_colors)]
    for j in range(2):
        gnode = grandchildren[i * 2 + j]
        img = glow_line(img, child, gnode, col, width=5, blur=14, alpha=145)

# draw nodes large-to-small
img = glow_circle(img, root[0], root[1], 130, ELEC_BLUE, glow_radius=36, glow_alpha=165)
for i, (x, y) in enumerate(children):
    img = glow_circle(img, x, y, 90, node_colors[i % len(node_colors)], glow_radius=28, glow_alpha=135)
for i, (x, y) in enumerate(grandchildren):
    img = glow_circle(img, x, y, 52, node_colors[i % len(node_colors)], glow_radius=18, glow_alpha=110,)

# Add faint concentric rings around root for hierarchy emphasis
for r, a in ((205, 28), (250, 20), (300, 12)):
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse((root[0]-r, root[1]-r, root[0]+r, root[1]+r), outline=ELEC_BLUE + (a,), width=2)
    ring = ring.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img, ring)

# soft network drift points
n = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(n)
for i in range(50):
    x = 120 + (i * 79) % (W - 240)
    y = 250 + (i * 53) % 700
    nd.point((x, y), fill=(CYAN[0], CYAN[1], CYAN[2], 24))
    nd.point((x + 10, y + 24), fill=(ELEC_BLUE[0], ELEC_BLUE[1], ELEC_BLUE[2], 18))
    nd.point((x + 20, y + 48), fill=(PURPLE[0], PURPLE[1], PURPLE[2], 16))
n = n.filter(ImageFilter.GaussianBlur(2))
img = Image.alpha_composite(img, n)

# 4) vignette for depth
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse((-240, -180, W + 240, H + 180), fill=220)
inv = Image.eval(vig, lambda p: 255 - p)
black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
black.putalpha(inv)
img = Image.alpha_composite(img, black)

# 5) Text (matching EP014 style with glow)
md = ImageDraw.Draw(img)
try:
    font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 44)
    font_ep = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 56)
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 84)
except Exception:
    font_small = ImageFont.load_default()
    font_ep = ImageFont.load_default()
    font_title = ImageFont.load_default()

# top texts
md.text(((W - md.textlength("OPENCLAW DAILY", font=font_small)) / 2, 72), "OPENCLAW DAILY", font=font_small, fill=WHITE)

w2 = md.textlength("Episode 17", font=font_ep)
# glow glow for episode line
for blur, a in ((10, 130), (24, 80)):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.text(((W - w2) / 2, 128), "Episode 17", font=font_ep, fill=ELEC_BLUE + (a,))
    g = g.filter(ImageFilter.GaussianBlur(blur))
    img = Image.alpha_composite(img, g)
md = ImageDraw.Draw(img)
md.text(((W - w2) / 2, 128), "Episode 17", font=font_ep, fill=ELEC_BLUE)

# bottom title split
line1 = "AGENTS ALL THE WAY"
line2 = "DOWN"
w31 = md.textlength(line1, font=font_title)
w32 = md.textlength(line2, font=font_title)
for text, y, w, fill in ((line1, 1200, w31, WHITE), (line2, 1290, w32, WHITE)):
    md.text(((W - w) / 2 + 2, y + 2), text, font=font_title, fill=(0, 0, 0))
    md.text(((W - w) / 2, y), text, font=font_title, fill=fill)

# final sharpen
img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=140, threshold=2))

img.convert("RGB").save(OUT, "PNG")
print(OUT)
