from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random

W, H = 1400, 1400
OUT = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_020_cover.png"

BLACK       = (2, 2, 4)
TOP_BG      = (4, 6, 10)
BOT_BG      = (8, 4, 2)
AMBER       = (200, 110, 20)
AMBER_BRIGHT= (255, 165, 50)
AMBER_GLOW  = (255, 200, 100)
ORANGE_HOT  = (255, 130, 30)
STEEL       = (50, 55, 60)
STEEL_LIGHT = (90, 100, 115)
WHITE       = (248, 246, 240)
DIM_WHITE   = (180, 175, 165)

img = Image.new("RGBA", (W, H), BLACK + (255,))
d = ImageDraw.Draw(img)

# Background gradient — near-black with warm hint at bottom
for y in range(H):
    t = y / (H - 1)
    r = int(TOP_BG[0] * (1 - t) + BOT_BG[0] * t)
    g = int(TOP_BG[1] * (1 - t) + BOT_BG[1] * t)
    b = int(TOP_BG[2] * (1 - t) + BOT_BG[2] * t)
    d.line([(0, y), (W, y)], fill=(r, g, b, 255))

def blur_overlay(draw_fn, blur=18):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld)
    return layer.filter(ImageFilter.GaussianBlur(blur))

# Central amber core glow
core = blur_overlay(
    lambda ld: ld.ellipse([(350, 350), (1050, 1050)], fill=AMBER + (40,)),
    blur=160
)
img = Image.alpha_composite(img, core)

# --- CIRCUIT / INFRASTRUCTURE GRID ---
random.seed(7)

# Horizontal circuit traces
trace_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(trace_layer)

# Main horizontal traces
traces_h = [220, 380, 540, 700, 860, 1020]
for ty in traces_h:
    td.line([(80, ty), (1320, ty)], fill=STEEL + (45,), width=1)

# Main vertical traces
traces_v = [240, 460, 700, 940, 1160]
for tx in traces_v:
    td.line([(tx, 80), (tx, 1320)], fill=STEEL + (35,), width=1)

trace_layer = trace_layer.filter(ImageFilter.GaussianBlur(0.4))
img = Image.alpha_composite(img, trace_layer)

# Circuit nodes at intersections (small squares)
node_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(node_layer)
for ty in traces_h:
    for tx in traces_v:
        if random.random() > 0.35:
            sz = random.choice([4, 5, 6])
            nd.rectangle([(tx - sz, ty - sz), (tx + sz, ty + sz)],
                          fill=AMBER + (random.randint(60, 130),),
                          outline=AMBER_BRIGHT + (80,), width=1)
node_layer = node_layer.filter(ImageFilter.GaussianBlur(0.6))
img = Image.alpha_composite(img, node_layer)

# --- CENTRAL PLATFORM SYMBOL: stacked layers / shield ---
# Three stacked hexagon-ish rings representing "layers" of infrastructure
cx, cy = 700, 600

def draw_hex_ring(img, cx, cy, r, color, alpha, width, blur_amt):
    pts = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.polygon(pts, outline=color + (alpha,), width=width)
    layer = layer.filter(ImageFilter.GaussianBlur(blur_amt))
    return layer

# Outer glow rings
for ring_r, ring_alpha, ring_blur in [(320, 30, 30), (260, 50, 20), (210, 65, 12)]:
    ring = draw_hex_ring(img, cx, cy, ring_r, AMBER, ring_alpha, 4, ring_blur)
    img = Image.alpha_composite(img, ring)

# Solid hex rings
for ring_r, ring_alpha, ring_blur, ring_w in [(320, 160, 3, 3), (260, 200, 2, 3), (210, 220, 1.5, 4)]:
    ring = draw_hex_ring(img, cx, cy, ring_r, AMBER_BRIGHT, ring_alpha, ring_w, ring_blur)
    img = Image.alpha_composite(img, ring)

# Center filled hex
pts_center = []
for i in range(6):
    angle = math.radians(60 * i - 30)
    pts_center.append((cx + 160 * math.cos(angle), cy + 160 * math.sin(angle)))

center_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cld = ImageDraw.Draw(center_layer)
cld.polygon(pts_center, fill=(30, 20, 8, 200), outline=AMBER_GLOW + (220,), width=3)
center_layer = center_layer.filter(ImageFilter.GaussianBlur(1.5))
img = Image.alpha_composite(img, center_layer)

# Inner center glow
inner_glow = blur_overlay(
    lambda ld: ld.ellipse([(cx - 100, cy - 100), (cx + 100, cy + 100)],
                           fill=ORANGE_HOT + (80,)),
    blur=40
)
img = Image.alpha_composite(img, inner_glow)

# Claw mark inside center hex — 3 slash lines
slash_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sld = ImageDraw.Draw(slash_layer)
offsets = [-36, 0, 36]
for ox in offsets:
    x1 = cx + ox - 30
    y1 = cy - 90
    x2 = cx + ox + 30
    y2 = cy + 90
    sld.line([(x1, y1), (x2, y2)], fill=AMBER_GLOW + (230,), width=7)
slash_layer = slash_layer.filter(ImageFilter.GaussianBlur(2))
img = Image.alpha_composite(img, slash_layer)

# Floating particles — amber data bits orbiting the hex
random.seed(42)
part_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(part_layer)
for orbit_r in [330, 275, 220]:
    n = 12
    for i in range(n):
        angle = random.uniform(0, 2 * math.pi)
        px = int(cx + orbit_r * math.cos(angle))
        py = int(cy + orbit_r * math.sin(angle))
        pr = random.randint(2, 5)
        alpha = random.randint(100, 200)
        pd.ellipse([(px - pr, py - pr), (px + pr, py + pr)],
                   fill=AMBER_BRIGHT + (alpha,))
part_layer = part_layer.filter(ImageFilter.GaussianBlur(1.2))
img = Image.alpha_composite(img, part_layer)

# --- TYPOGRAPHY ---
try:
    font_show  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
    font_ep    = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 68)
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 108)
    font_sub   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
except Exception:
    font_show = font_ep = font_title = font_sub = ImageFont.load_default()

md = ImageDraw.Draw(img)

SHOW_TEXT = "OPENCLAW DAILY"
EP_TEXT   = "EP020"
LINE1     = "THE INFRASTRUCTURE"
LINE2     = "RELEASE"

sw  = md.textlength(SHOW_TEXT, font=font_show)
ew  = md.textlength(EP_TEXT, font=font_ep)
l1w = md.textlength(LINE1, font=font_title)
l2w = md.textlength(LINE2, font=font_title)

# Show name
md.text(((W - sw) / 2, 62), SHOW_TEXT, font=font_show, fill=(210, 205, 195, 235))

# EP number — amber glow
for blur_amt, alpha in ((16, 110), (30, 55)):
    eg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    egd = ImageDraw.Draw(eg)
    egd.text(((W - ew) / 2, 120), EP_TEXT, font=font_ep, fill=AMBER + (alpha,))
    eg = eg.filter(ImageFilter.GaussianBlur(blur_amt))
    img = Image.alpha_composite(img, eg)
md = ImageDraw.Draw(img)
md.text(((W - ew) / 2, 120), EP_TEXT, font=font_ep, fill=AMBER_GLOW + (255,))

# Dark plate behind title
plate = blur_overlay(
    lambda ld: ld.polygon(
        [(80, 1010), (1320, 1010), (1380, 1400), (20, 1400)],
        fill=(0, 0, 0, 170)
    ),
    blur=28
)
img = Image.alpha_composite(img, plate)
md = ImageDraw.Draw(img)

# Title lines
for text, y, tw in ((LINE1, 1050, l1w), (LINE2, 1176, l2w)):
    # Shadow
    md.text(((W - tw) / 2 + 4, y + 4), text, font=font_title, fill=(0, 0, 0, 200))
    # Amber glow
    tg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tgd = ImageDraw.Draw(tg)
    tgd.text(((W - tw) / 2, y), text, font=font_title, fill=ORANGE_HOT + (70,))
    tg = tg.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img, tg)
    md = ImageDraw.Draw(img)
    md.text(((W - tw) / 2, y), text, font=font_title, fill=WHITE + (255,))

# Tagline
tag = "WHEN A TOOL BECOMES INFRASTRUCTURE"
tw2 = md.textlength(tag, font=font_sub)
md.text(((W - tw2) / 2, 1162), tag, font=font_sub, fill=AMBER_BRIGHT + (190,))

# Vignette
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.rectangle((60, 30, W - 60, H - 30), fill=210)
inv = Image.eval(vig, lambda p: 255 - p)
black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
black.putalpha(inv.filter(ImageFilter.GaussianBlur(90)))
img = Image.alpha_composite(img, black)

# Final sharpen
img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=145, threshold=2))
img.convert("RGB").save(OUT, "PNG")
print(OUT)
