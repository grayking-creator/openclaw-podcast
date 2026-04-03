"""
EP023 — The Infrastructure Week
Visual concept: data center / power grid aesthetic. Dark background, electric
blue/green server rack glow, power line silhouettes, circuit board patterns.
Feel: industrial, massive, essential. The physical skeleton of AI.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random, math

W, H = 1400, 1400
OUT = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_023_cover.png"

BLACK       = (2, 4, 10)
DARK_BG     = (3, 7, 18)
RACK_DARK   = (8, 14, 28)
CYAN        = (0, 210, 255)
CYAN_BRIGHT = (60, 235, 255)
CYAN_GLOW   = (110, 245, 255)
GREEN       = (30, 230, 120)
GREEN_BRIGHT= (80, 255, 160)
STEEL       = (28, 40, 65)
STEEL_LIGHT = (48, 68, 105)
DIM_WHITE   = (140, 165, 200)
WHITE       = (242, 248, 255)
AMBER       = (215, 145, 25)
AMBER_BRIGHT= (248, 175, 50)
ORANGE      = (240, 110, 30)

img = Image.new("RGBA", (W, H), BLACK + (255,))
d = ImageDraw.Draw(img)

# Background gradient — deep space black top to dark navy bottom
for y in range(H):
    t = y / (H - 1)
    r = int(2 + 6 * t)
    g = int(4 + 10 * t)
    b = int(10 + 22 * t)
    d.line([(0, y), (W, y)], fill=(r, g, b, 255))

def blur_overlay(draw_fn, blur=18):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld)
    return layer.filter(ImageFilter.GaussianBlur(blur))

# === CIRCUIT BOARD TRACE PATTERN (background, subtle) ===
random.seed(7)
circuit_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cl = ImageDraw.Draw(circuit_layer)

def draw_circuit_trace(draw, x, y, length, direction, color, alpha, width=1):
    """Draw an L-shaped circuit trace"""
    dx, dy = [(1,0),(-1,0),(0,1),(0,-1)][direction % 4]
    seg1 = random.randint(length // 3, length)
    ex, ey = x + dx * seg1, y + dy * seg1
    draw.line([(x, y), (ex, ey)], fill=color + (alpha,), width=width)
    # dot at junction
    draw.ellipse([(ex-2, ey-2), (ex+2, ey+2)], fill=color + (alpha,))
    # perpendicular branch
    px, py = [0,1,0,-1][(direction+1) % 4], [1,0,-1,0][(direction+1) % 4]
    seg2 = random.randint(20, length // 2)
    draw.line([(ex, ey), (ex + px*seg2, ey + py*seg2)], fill=color + (alpha,), width=width)

for _ in range(80):
    x = random.randint(0, W)
    y = random.randint(0, H)
    col = random.choice([CYAN, GREEN, STEEL_LIGHT])
    draw_circuit_trace(cl, x, y, random.randint(60, 200), random.randint(0, 3),
                       col, random.randint(12, 35), width=1)

circuit_layer = circuit_layer.filter(ImageFilter.GaussianBlur(0.8))
img = Image.alpha_composite(img, circuit_layer)
d = ImageDraw.Draw(img)

# === SERVER RACK SILHOUETTES ===
rack_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(rack_layer)

def draw_server_rack(draw, cx, top_y, rack_w, rack_h, glow_color, intensity=1.0):
    """Draw a server rack with glowing LEDs"""
    # Rack body
    draw.rectangle([(cx - rack_w//2, top_y), (cx + rack_w//2, top_y + rack_h)],
                   fill=(6, 10, 22, int(220 * intensity)),
                   outline=STEEL_LIGHT + (int(80 * intensity),), width=1)
    # Server unit slots
    unit_h = 14
    unit_gap = 4
    y_offset = top_y + 8
    slot = 0
    while y_offset + unit_h < top_y + rack_h - 8:
        # Server tray
        draw.rectangle([(cx - rack_w//2 + 4, y_offset),
                         (cx + rack_w//2 - 4, y_offset + unit_h)],
                        fill=(10, 16, 32, 200), outline=STEEL + (60,), width=1)
        # Status LEDs
        for i, led_col in enumerate([glow_color, GREEN if slot % 3 != 0 else AMBER]):
            lx = cx - rack_w//2 + 12 + i * 10
            ly = y_offset + unit_h//2 - 2
            draw.ellipse([(lx, ly), (lx+4, ly+4)], fill=led_col + (int(200 * intensity),))
        y_offset += unit_h + unit_gap
        slot += 1

# Define racks — positions across the frame
racks = [
    (110,  240, 80, 700, CYAN,       0.6),
    (220,  180, 80, 760, GREEN,      0.55),
    (330,  220, 80, 720, CYAN,       0.65),
    (450,  160, 80, 780, GREEN,      0.5),
    (570,  200, 90, 740, CYAN_BRIGHT,0.7),
    (700,  140, 90, 800, CYAN,       0.75),  # centre-ish, tallest
    (830,  160, 90, 780, GREEN,      0.7),
    (950,  200, 80, 740, CYAN,       0.65),
    (1070, 180, 80, 760, GREEN,      0.55),
    (1180, 220, 80, 720, CYAN,       0.6),
    (1290, 240, 80, 700, GREEN,      0.5),
]

for cx, ty, rw, rh, col, intensity in racks:
    draw_server_rack(rd, cx, ty, rw, rh, col, intensity)

rack_layer = rack_layer.filter(ImageFilter.GaussianBlur(0.5))
img = Image.alpha_composite(img, rack_layer)

# Glow emanating from rack tops
for cx, ty, rw, rh, col, intensity in racks:
    glow = blur_overlay(
        lambda ld, cx=cx, ty=ty, rw=rw, col=col, intensity=intensity:
            ld.ellipse([(cx - rw, ty - 40), (cx + rw, ty + 60)],
                       fill=col + (int(25 * intensity),)),
        blur=50
    )
    img = Image.alpha_composite(img, glow)

d = ImageDraw.Draw(img)

# === POWER LINE SILHOUETTES (top third of image) ===
power_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pl = ImageDraw.Draw(power_layer)

def draw_power_tower(draw, x, base_y, height, col, alpha):
    """Draw a simplified power transmission tower"""
    top_y = base_y - height
    mid_y = base_y - height // 2
    # Main verticals
    draw.line([(x - 8, base_y), (x, top_y)], fill=col + (alpha,), width=2)
    draw.line([(x + 8, base_y), (x, top_y)], fill=col + (alpha,), width=2)
    # Cross arms
    draw.line([(x - 40, mid_y + 20), (x + 40, mid_y + 20)], fill=col + (alpha,), width=2)
    draw.line([(x - 30, top_y + 20), (x + 30, top_y + 20)], fill=col + (alpha,), width=2)
    draw.line([(x - 18, top_y + 5), (x + 18, top_y + 5)], fill=col + (alpha,), width=2)
    # Diagonal supports
    draw.line([(x - 8, base_y), (x - 40, mid_y + 20)], fill=col + (alpha,), width=1)
    draw.line([(x + 8, base_y), (x + 40, mid_y + 20)], fill=col + (alpha,), width=1)

# Power towers across top area
tower_positions = [100, 260, 440, 620, 800, 980, 1150, 1310]
tower_base_y = 360
tower_heights = [160, 185, 155, 190, 180, 158, 182, 162]

for i, (tx, th) in enumerate(zip(tower_positions, tower_heights)):
    draw_power_tower(pl, tx, tower_base_y, th, STEEL_LIGHT, 55)

# Catenary wires between towers
def catenary(x1, y1, x2, y2, sag, num_points=40):
    pts = []
    for i in range(num_points + 1):
        t = i / num_points
        x = x1 + (x2 - x1) * t
        # Parabolic sag approximation
        y = y1 + (y2 - y1) * t + sag * 4 * t * (1 - t)
        pts.append((x, y))
    return pts

for i in range(len(tower_positions) - 1):
    tx1, tx2 = tower_positions[i], tower_positions[i+1]
    th1, th2 = tower_heights[i], tower_heights[i+1]
    for wire_offset in [-40, -28, -16, -5]:
        pts = catenary(tx1, tower_base_y - th1 + wire_offset,
                       tx2, tower_base_y - th2 + wire_offset, 18)
        for j in range(len(pts)-1):
            pl.line([pts[j], pts[j+1]], fill=STEEL_LIGHT + (40,), width=1)

power_layer = power_layer.filter(ImageFilter.GaussianBlur(0.6))
img = Image.alpha_composite(img, power_layer)
d = ImageDraw.Draw(img)

# === AMBIENT GLOW — central server heat haze ===
centre_glow = blur_overlay(
    lambda ld: ld.ellipse([(350, 300), (1050, 900)], fill=CYAN + (8,)),
    blur=120
)
img = Image.alpha_composite(img, centre_glow)
centre_glow2 = blur_overlay(
    lambda ld: ld.ellipse([(500, 400), (900, 800)], fill=GREEN + (6,)),
    blur=90
)
img = Image.alpha_composite(img, centre_glow2)

# Floor reflection / light bleed at bottom of racks
for cx, ty, rw, rh, col, intensity in racks:
    floor_y = ty + rh
    refl = blur_overlay(
        lambda ld, cx=cx, floor_y=floor_y, rw=rw, col=col, intensity=intensity:
            ld.ellipse([(cx - rw*2, floor_y - 10), (cx + rw*2, floor_y + 60)],
                       fill=col + (int(18 * intensity),)),
        blur=35
    )
    img = Image.alpha_composite(img, refl)

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
EP_TEXT   = "EP023"
LINE1     = "THE"
LINE2     = "INFRASTRUCTURE"
LINE3     = "WEEK"
TAG_LINE  = "$690B. THE SKELETON OF AI."

# Measure text
sw  = md.textlength(SHOW_TEXT, font=font_show)
ew  = md.textlength(EP_TEXT,   font=font_ep)
l1w = md.textlength(LINE1,     font=font_title)
l2w = md.textlength(LINE2,     font=font_title)
l3w = md.textlength(LINE3,     font=font_title)
tw2 = md.textlength(TAG_LINE,  font=font_sub)

# "OPENCLAW DAILY" top centre
md.text(((W - sw) / 2, 55), SHOW_TEXT, font=font_show, fill=(185, 205, 230, 210))

# "EP023" — electric blue glow
for blur_amt, alpha in ((18, 95), (34, 45)):
    eg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    egd = ImageDraw.Draw(eg)
    egd.text(((W - ew) / 2, 112), EP_TEXT, font=font_ep, fill=CYAN + (alpha,))
    eg = eg.filter(ImageFilter.GaussianBlur(blur_amt))
    img = Image.alpha_composite(img, eg)
md = ImageDraw.Draw(img)
md.text(((W - ew) / 2, 112), EP_TEXT, font=font_ep, fill=CYAN_GLOW + (255,))

# Dark title plate behind bottom text block
plate = blur_overlay(
    lambda ld: ld.polygon(
        [(0, 960), (1400, 960), (1400, 1400), (0, 1400)],
        fill=(0, 0, 0, 195)
    ),
    blur=28
)
img = Image.alpha_composite(img, plate)
md = ImageDraw.Draw(img)

# "THE" — white, first title line
md.text(((W - l1w) / 2 + 3, 978), LINE1, font=font_title, fill=(0, 0, 0, 160))
tg1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tg1d = ImageDraw.Draw(tg1)
tg1d.text(((W - l1w) / 2, 975), LINE1, font=font_title, fill=CYAN + (50,))
tg1 = tg1.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img, tg1)
md = ImageDraw.Draw(img)
md.text(((W - l1w) / 2, 975), LINE1, font=font_title, fill=WHITE + (255,))

# "INFRASTRUCTURE" — electric blue/green glow — dominant line
md.text(((W - l2w) / 2 + 4, 1103), LINE2, font=font_title, fill=(0, 0, 0, 170))
tg2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tg2d = ImageDraw.Draw(tg2)
tg2d.text(((W - l2w) / 2, 1100), LINE2, font=font_title, fill=CYAN + (80,))
tg2 = tg2.filter(ImageFilter.GaussianBlur(16))
img = Image.alpha_composite(img, tg2)
md = ImageDraw.Draw(img)
md.text(((W - l2w) / 2, 1100), LINE2, font=font_title, fill=CYAN_BRIGHT + (255,))

# "WEEK" — green accent
md.text(((W - l3w) / 2 + 4, 1233), LINE3, font=font_title, fill=(0, 0, 0, 160))
tg3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tg3d = ImageDraw.Draw(tg3)
tg3d.text(((W - l3w) / 2, 1230), LINE3, font=font_title, fill=GREEN + (70,))
tg3 = tg3.filter(ImageFilter.GaussianBlur(14))
img = Image.alpha_composite(img, tg3)
md = ImageDraw.Draw(img)
md.text(((W - l3w) / 2, 1230), LINE3, font=font_title, fill=GREEN_BRIGHT + (255,))

# Tagline
md.text(((W - tw2) / 2, 1365), TAG_LINE, font=font_sub, fill=CYAN_BRIGHT + (100,))

# Vignette
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.rectangle((50, 25, W-50, H-25), fill=205)
inv = Image.eval(vig, lambda p: 255 - p)
black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
black.putalpha(inv.filter(ImageFilter.GaussianBlur(90)))
img = Image.alpha_composite(img, black)

img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=145, threshold=2))
img.convert("RGB").save(OUT, "PNG")
print(f"Saved: {OUT}")
