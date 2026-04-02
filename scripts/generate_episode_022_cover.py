"""
EP022 — The Release Train
Visual concept: a fast-moving train of glowing release tags on dark rails,
with the AI stack as infrastructure. Deep black bg, neon cyan/amber speed lines,
stacked version labels streaking through the frame.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random, math

W, H = 1400, 1400
OUT = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_022_cover.png"

BLACK      = (2, 3, 8)
DARK_BG    = (4, 6, 16)
RAIL_GRAY  = (25, 32, 48)
CYAN       = (0, 195, 225)
CYAN_BRIGHT= (60, 235, 255)
CYAN_GLOW  = (110, 245, 255)
AMBER      = (210, 140, 20)
AMBER_BRIGHT=(245, 170, 45)
GREEN      = (40, 220, 110)
MAGENTA    = (200, 60, 180)
WHITE      = (242, 246, 252)
DIM_WHITE  = (150, 168, 192)
STEEL      = (28, 38, 58)

img = Image.new("RGBA", (W, H), BLACK + (255,))
d = ImageDraw.Draw(img)

# Background gradient — deep space black to dark navy
for y in range(H):
    t = y / (H - 1)
    r = int(DARK_BG[0] * (1-t) + 2 * t)
    g = int(DARK_BG[1] * (1-t) + 3 * t)
    b = int(DARK_BG[2] * (1-t) + 8 * t)
    d.line([(0, y), (W, y)], fill=(r, g, b, 255))

def blur_overlay(draw_fn, blur=18):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld)
    return layer.filter(ImageFilter.GaussianBlur(blur))

# Central warm glow (horizon point — vanishing point of the rails)
vx, vy = 700, 560
core_glow = blur_overlay(
    lambda ld: ld.ellipse([(vx-180, vy-120), (vx+180, vy+120)], fill=AMBER + (30,)),
    blur=160
)
img = Image.alpha_composite(img, core_glow)
core_glow2 = blur_overlay(
    lambda ld: ld.ellipse([(vx-80, vy-60), (vx+80, vy+60)], fill=CYAN + (20,)),
    blur=80
)
img = Image.alpha_composite(img, core_glow2)

d = ImageDraw.Draw(img)

# === PERSPECTIVE RAILS ===
# Two rails converging to vanishing point
rail_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(rail_layer)

# Left rail: from bottom-left to vanishing point
rd.line([(80, H-40), (vx, vy)], fill=RAIL_GRAY + (180,), width=6)
rd.line([(80, H-40), (vx, vy)], fill=CYAN + (60,), width=2)
# Right rail
rd.line([(W-80, H-40), (vx, vy)], fill=RAIL_GRAY + (180,), width=6)
rd.line([(W-80, H-40), (vx, vy)], fill=CYAN + (60,), width=2)

# Cross ties — perspective-scaled
num_ties = 14
for i in range(num_ties):
    t = (i + 1) / (num_ties + 1)
    # perspective: closer to bottom = bigger gap
    pt = t ** 1.6
    y_pos = int(vy + (H - 40 - vy) * pt)
    # x positions on each rail at this y
    left_frac = (y_pos - vy) / (H - 40 - vy)
    lx = int(vx + (80 - vx) * left_frac)
    rx = int(vx + (W - 80 - vx) * left_frac)
    alpha = int(40 + 80 * left_frac)
    rd.line([(lx, y_pos), (rx, y_pos)], fill=RAIL_GRAY + (alpha,), width=max(1, int(1 + 3*left_frac)))

rail_layer = rail_layer.filter(ImageFilter.GaussianBlur(0.8))
img = Image.alpha_composite(img, rail_layer)

# === SPEED LINES — streaking from vanishing point ===
random.seed(42)
speed_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(speed_layer)
colors_speed = [CYAN, AMBER, GREEN, MAGENTA, CYAN_BRIGHT, AMBER_BRIGHT]
for _ in range(55):
    angle = random.uniform(-math.pi, math.pi)
    length = random.uniform(80, 380)
    ex = vx + math.cos(angle) * length
    ey = vy + math.sin(angle) * length
    col = random.choice(colors_speed)
    alpha = random.randint(20, 70)
    width_val = random.choice([1, 1, 2, 2, 3])
    sd.line([(vx, vy), (ex, ey)], fill=col + (alpha,), width=width_val)
speed_layer = speed_layer.filter(ImageFilter.GaussianBlur(1.2))
img = Image.alpha_composite(img, speed_layer)

# === RELEASE TAG CARDS — floating on the track ===
try:
    font_tag   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
    font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
except:
    font_tag = font_small = ImageFont.load_default()

release_tags = [
    ("v2026.4.1",        CYAN_BRIGHT,   (420, 390), 1.0),
    ("v2026.3.31",       AMBER_BRIGHT,  (680, 460), 0.82),
    ("v2026.3.28",       GREEN,         (860, 510), 0.67),
    ("v2026.3.24",       MAGENTA,       (560, 525), 0.60),
    ("v2026.3.23",       DIM_WHITE,     (730, 548), 0.52),
]

for tag_text, color, pos, scale in release_tags:
    tx, ty = pos
    w_box = int(180 * scale)
    h_box = int(46 * scale)
    # card bg
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cld = ImageDraw.Draw(card_layer)
    cld.rounded_rectangle(
        [(tx - w_box//2, ty - h_box//2), (tx + w_box//2, ty + h_box//2)],
        radius=int(8*scale),
        fill=(8, 12, 28, int(200*scale)),
        outline=color + (int(180*scale),),
        width=max(1, int(2*scale))
    )
    card_layer = card_layer.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img, card_layer)
    # glow behind card
    glow_card = blur_overlay(
        lambda ld, tx=tx, ty=ty, w_box=w_box, h_box=h_box, color=color, scale=scale:
            ld.rounded_rectangle(
                [(tx - w_box//2 - 4, ty - h_box//2 - 4), (tx + w_box//2 + 4, ty + h_box//2 + 4)],
                radius=int(10*scale), fill=color + (int(30*scale),)
            ),
        blur=12
    )
    img = Image.alpha_composite(img, glow_card)
    # text
    cd = ImageDraw.Draw(img)
    try:
        fs = max(14, int(28 * scale))
        f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", fs)
    except:
        f = font_tag
    tw = cd.textlength(tag_text, font=f)
    cd.text((tx - tw/2, ty - fs/2), tag_text, font=f, fill=color + (int(230*scale),))

# === GLOWING LOCOMOTIVE FRONT — implied shape at vanishing point ===
loco_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ll = ImageDraw.Draw(loco_layer)
# headlight burst
ll.ellipse([(vx-18, vy-14), (vx+18, vy+14)], fill=WHITE + (230,))
loco_layer = loco_layer.filter(ImageFilter.GaussianBlur(0.5))
img = Image.alpha_composite(img, loco_layer)

headlight_glow = blur_overlay(
    lambda ld: ld.ellipse([(vx-40, vy-30), (vx+40, vy+30)], fill=WHITE + (160,)),
    blur=22
)
img = Image.alpha_composite(img, headlight_glow)
headlight_glow2 = blur_overlay(
    lambda ld: ld.ellipse([(vx-80, vy-60), (vx+80, vy+60)], fill=CYAN + (50,)),
    blur=50
)
img = Image.alpha_composite(img, headlight_glow2)

# === TYPOGRAPHY ===
try:
    font_show  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
    font_ep    = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 68)
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 118)
    font_sub   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
except:
    font_show = font_ep = font_title = font_sub = ImageFont.load_default()

md = ImageDraw.Draw(img)

SHOW_TEXT = "OPENCLAW DAILY"
EP_TEXT   = "EP022"
LINE1     = "THE"
LINE2     = "RELEASE TRAIN"
TAG_LINE  = "FIVE STORIES. ONE TRACK."

sw  = md.textlength(SHOW_TEXT, font=font_show)
ew  = md.textlength(EP_TEXT,   font=font_ep)
l1w = md.textlength(LINE1,     font=font_title)
l2w = md.textlength(LINE2,     font=font_title)
tw2 = md.textlength(TAG_LINE,  font=font_sub)

# Show name — top centre
md.text(((W - sw) / 2, 60), SHOW_TEXT, font=font_show, fill=(185, 200, 222, 220))

# EP number — cyan glow
for blur_amt, alpha in ((18, 90), (32, 45)):
    eg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    egd = ImageDraw.Draw(eg)
    egd.text(((W - ew) / 2, 118), EP_TEXT, font=font_ep, fill=CYAN + (alpha,))
    eg = eg.filter(ImageFilter.GaussianBlur(blur_amt))
    img = Image.alpha_composite(img, eg)
md = ImageDraw.Draw(img)
md.text(((W - ew) / 2, 118), EP_TEXT, font=font_ep, fill=CYAN_GLOW + (255,))

# Dark plate behind title block
plate = blur_overlay(
    lambda ld: ld.polygon(
        [(30, 1000), (1370, 1000), (1400, 1400), (0, 1400)],
        fill=(0, 0, 0, 185)
    ),
    blur=30
)
img = Image.alpha_composite(img, plate)
md = ImageDraw.Draw(img)

# Title line 1 — "THE"
md.text(((W - l1w) / 2 + 3, 1013), LINE1, font=font_title, fill=(0, 0, 0, 180))
tg1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tg1d = ImageDraw.Draw(tg1)
tg1d.text(((W - l1w) / 2, 1010), LINE1, font=font_title, fill=AMBER + (55,))
tg1 = tg1.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img, tg1)
md = ImageDraw.Draw(img)
md.text(((W - l1w) / 2, 1010), LINE1, font=font_title, fill=WHITE + (255,))

# Title line 2 — "RELEASE TRAIN" — amber/gold
md.text(((W - l2w) / 2 + 4, 1143), LINE2, font=font_title, fill=(0, 0, 0, 180))
tg2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tg2d = ImageDraw.Draw(tg2)
tg2d.text(((W - l2w) / 2, 1140), LINE2, font=font_title, fill=AMBER + (70,))
tg2 = tg2.filter(ImageFilter.GaussianBlur(16))
img = Image.alpha_composite(img, tg2)
md = ImageDraw.Draw(img)
md.text(((W - l2w) / 2, 1140), LINE2, font=font_title, fill=AMBER_BRIGHT + (255,))

# Tagline between EP and title
md.text(((W - tw2) / 2, 1136), TAG_LINE, font=font_sub, fill=CYAN_BRIGHT + (170,))

# Vignette
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.rectangle((55, 28, W-55, H-28), fill=205)
inv = Image.eval(vig, lambda p: 255 - p)
black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
black.putalpha(inv.filter(ImageFilter.GaussianBlur(95)))
img = Image.alpha_composite(img, black)

img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=148, threshold=2))
img.convert("RGB").save(OUT, "PNG")
print(f"Saved: {OUT}")
