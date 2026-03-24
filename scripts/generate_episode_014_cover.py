from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

W, H = 1400, 1400
OUT = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_014_cover.png"

# Colors
TOP_BG = (0x0A, 0x0A, 0x1A)
BOT_BG = (0x00, 0x00, 0x05)
STEEL = (0x88, 0x88, 0x99)
STEEL_DARK = (0x55, 0x55, 0x66)
ELEC_BLUE = (0x00, 0xAA, 0xFF)
CYAN = (0x00, 0xCC, 0xFF)
ORANGE = (0xFF, 0x66, 0x00)
TOOL_ORANGE = (0xFF, 0x88, 0x00)
WHITE = (245, 248, 255)

img = Image.new("RGB", (W, H), BOT_BG)
d = ImageDraw.Draw(img)

# 1) Vertical gradient background
for y in range(H):
    t = y / (H - 1)
    r = int(TOP_BG[0] * (1 - t) + BOT_BG[0] * t)
    g = int(TOP_BG[1] * (1 - t) + BOT_BG[1] * t)
    b = int(TOP_BG[2] * (1 - t) + BOT_BG[2] * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# 2) subtle grid/circuit overlay (~10% opacity)
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
grid_col = (25, 45, 90, 26)
for x in range(0, W, 70):
    od.line([(x, 0), (x, H)], fill=grid_col, width=1)
for y in range(0, H, 70):
    od.line([(0, y), (W, y)], fill=grid_col, width=1)

# Circuit traces
for y in range(140, H - 220, 180):
    od.line([(80, y), (300, y), (300, y + 40), (520, y + 40)], fill=(30, 70, 130, 32), width=2)
    od.ellipse((515, y + 35, 525, y + 45), outline=(40, 90, 170, 38), width=2)
for y in range(220, H - 180, 210):
    od.line([(W - 80, y), (W - 330, y), (W - 330, y + 50), (W - 560, y + 50)], fill=(30, 70, 130, 32), width=2)
    od.ellipse((W - 565, y + 45, W - 555, y + 55), outline=(40, 90, 170, 38), width=2)

img = Image.alpha_composite(img.convert("RGBA"), overlay)

# Utility glow painter
def glow_polygon(base, points, color, glow_radius=24, glow_alpha=120, width=0):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    if width == 0:
        gd.polygon(points, fill=color + (glow_alpha,))
    else:
        gd.line(points + [points[0]], fill=color + (glow_alpha,), width=width)
    g = g.filter(ImageFilter.GaussianBlur(glow_radius))
    return Image.alpha_composite(base, g)

# 3) Mechanical claw arm
# Main shaft
shaft = [(620, 0), (780, 0), (740, 520), (660, 520)]
img = glow_polygon(img, shaft, ELEC_BLUE, glow_radius=22, glow_alpha=75)
md = ImageDraw.Draw(img)
md.polygon(shaft, fill=STEEL)

# segment details
md.polygon([(645, 40), (755, 40), (740, 230), (660, 230)], fill=STEEL_DARK)
md.polygon([(650, 235), (750, 235), (736, 415), (664, 415)], fill=(120, 120, 136))

# blue specular strip
md.polygon([(740, 0), (780, 0), (750, 520), (720, 520)], fill=(40, 90, 150))
md.line([(735, 20), (710, 500)], fill=(90, 190, 255), width=3)

# side braces
left_brace = [(560, 170), (640, 200), (610, 500), (530, 470)]
right_brace = [(840, 170), (760, 200), (790, 500), (870, 470)]
for poly in (left_brace, right_brace):
    img = glow_polygon(img, poly, ORANGE, glow_radius=14, glow_alpha=55)
    md = ImageDraw.Draw(img)
    md.polygon(poly, fill=(95, 95, 112))

# claw hub
hub_center = (700, 600)
hub_r = 88
img = glow_polygon(img, [(hub_center[0]-hub_r, hub_center[1]-hub_r), (hub_center[0]+hub_r, hub_center[1]-hub_r), (hub_center[0]+hub_r, hub_center[1]+hub_r), (hub_center[0]-hub_r, hub_center[1]+hub_r)], ELEC_BLUE, glow_radius=30, glow_alpha=65)
md = ImageDraw.Draw(img)
md.ellipse((hub_center[0]-hub_r, hub_center[1]-hub_r, hub_center[0]+hub_r, hub_center[1]+hub_r), fill=(110, 110, 128), outline=(180, 185, 205), width=4)
md.ellipse((hub_center[0]-22, hub_center[1]-22, hub_center[0]+22, hub_center[1]+22), fill=(60, 60, 78))

# 4) Claw fingers/tines reaching toolbox
fingers = [
    [(640, 640), (585, 760), (560, 980), (605, 1000), (665, 790), (690, 670)],
    [(760, 640), (815, 760), (840, 980), (795, 1000), (735, 790), (710, 670)],
    [(700, 670), (670, 790), (675, 1030), (725, 1030), (730, 790)],
]
for i, f in enumerate(fingers):
    glow_c = ELEC_BLUE if i != 1 else ORANGE
    img = glow_polygon(img, f, glow_c, glow_radius=18, glow_alpha=70)
    md = ImageDraw.Draw(img)
    md.polygon(f, fill=(128, 128, 146), outline=(210, 215, 230))
    # claw tips
    tip = f[2]
    md.polygon([tip, (tip[0]-16, tip[1]+40), (tip[0]+16, tip[1]+40)], fill=(230, 235, 245))

# 5) Open toolbox center-lower with glow bloom
tool_top_y = 960
tool_bottom_y = 1170
tool = [(470, tool_top_y), (930, tool_top_y), (1010, tool_bottom_y), (390, tool_bottom_y)]
lid = [(500, 900), (900, 900), (940, 960), (460, 960)]

img = glow_polygon(img, tool, ORANGE, glow_radius=45, glow_alpha=95)
img = glow_polygon(img, tool, CYAN, glow_radius=38, glow_alpha=80)

md = ImageDraw.Draw(img)
md.polygon(tool, fill=(35, 37, 52), outline=(110, 115, 140), width=3)
md.polygon(lid, fill=(45, 47, 62), outline=(140, 145, 170), width=3)

# interior glow spill
spill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(spill)
sd.ellipse((500, 900, 900, 1180), fill=(255, 130, 20, 110))
sd.ellipse((520, 920, 880, 1160), fill=(10, 190, 255, 90))
spill = spill.filter(ImageFilter.GaussianBlur(28))
img = Image.alpha_composite(img, spill)

# 6) Glowing tool shapes inside
md = ImageDraw.Draw(img)

def glow_line(points, color, width=5, blur=12, alpha=180):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.line(points, fill=color + (alpha,), width=width, joint="curve")
    g = g.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(img, g)

# Curly-ish braces { }
brace_l = [(575, 1020), (560, 1035), (560, 1060), (575, 1075), (560, 1090), (560, 1115), (575, 1130)]
brace_r = [(825, 1020), (840, 1035), (840, 1060), (825, 1075), (840, 1090), (840, 1115), (825, 1130)]
for pts, col in ((brace_l, CYAN), (brace_r, TOOL_ORANGE)):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.line(pts, fill=col + (220,), width=6)
    g = g.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, g)
    md = ImageDraw.Draw(img)
    md.line(pts, fill=col, width=3)

# chip/square icon
chip_box = (655, 1038, 745, 1128)
for col, a, b in ((CYAN, 140, 12), (TOOL_ORANGE, 100, 18)):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.rectangle(chip_box, outline=col + (a,), width=4)
    g = g.filter(ImageFilter.GaussianBlur(b))
    img = Image.alpha_composite(img, g)
md = ImageDraw.Draw(img)
md.rectangle(chip_box, outline=(230, 245, 255), width=3)
for i in range(6):
    x = 662 + i * 14
    md.line([(x, 1028), (x, 1038)], fill=CYAN, width=2)
    md.line([(x, 1128), (x, 1138)], fill=TOOL_ORANGE, width=2)

# package/box outline
pkg = [(760, 1050), (800, 1030), (840, 1050), (800, 1070)]
md.polygon(pkg, outline=CYAN, fill=None, width=3)
md.line([(800, 1030), (800, 1070)], fill=TOOL_ORANGE, width=2)

# additional halo on claw-toolbox interaction
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
hd.ellipse((520, 780, 900, 1140), fill=(0, 170, 255, 65))
hd.ellipse((540, 800, 880, 1120), fill=(255, 110, 10, 55))
halo = halo.filter(ImageFilter.GaussianBlur(36))
img = Image.alpha_composite(img, halo)

# vignette for cinematic depth
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse((-220, -160, W + 220, H + 220), fill=200)
inv = Image.eval(vig, lambda p: 255 - p)
black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
black.putalpha(inv)
img = Image.alpha_composite(img, black)

# 7/8/9 Text
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
t1 = "OPENCLAW DAILY"
t2 = "Episode 14"
t3 = "THE ACQUISITION OF EVERYTHING"

w1 = md.textlength(t1, font=font_small)
w2 = md.textlength(t2, font=font_ep)

md.text(((W - w1) / 2, 72), t1, font=font_small, fill=WHITE)
# glow for Episode 14
for blur, a in ((10, 120), (22, 70)):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.text(((W - w2) / 2, 128), t2, font=font_ep, fill=ELEC_BLUE + (a,))
    g = g.filter(ImageFilter.GaussianBlur(blur))
    img = Image.alpha_composite(img, g)
md = ImageDraw.Draw(img)
md.text(((W - w2) / 2, 128), t2, font=font_ep, fill=ELEC_BLUE)

# lower-third title in wrapped two lines
line1 = "THE ACQUISITION"
line2 = "OF EVERYTHING"
w31 = md.textlength(line1, font=font_title)
w32 = md.textlength(line2, font=font_title)

for text, y, w in ((line1, 1185, w31), (line2, 1270, w32)):
    # subtle dark stroke
    md.text(((W - w)/2 + 2, y + 2), text, font=font_title, fill=(0, 0, 0))
    # white text
    md.text(((W - w)/2, y), text, font=font_title, fill=WHITE)

# Final sharpen for premium/edgy look
img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=135, threshold=3))

img.convert("RGB").save(OUT, "PNG")
print(OUT)
