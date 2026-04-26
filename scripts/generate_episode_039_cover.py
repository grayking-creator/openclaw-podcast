from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random

W, H = 1400, 1400
OUT = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_039_cover.png"
WEB_OUT = "/Users/tobyglennpeters/.openclaw/workspace/websiteBuilder/frontend/public/images/podcast/episode_039_cover.png"
CDN_OUT = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast-audio/episode_039_cover.png"

NAVY_TOP = (10, 20, 52)
NAVY_BOT = (3, 8, 22)
CYAN = (87, 216, 255)
CYAN_SOFT = (120, 236, 255)
AMBER = (255, 184, 54)
AMBER_SOFT = (255, 214, 124)
MAGENTA = (242, 104, 217)
WHITE = (244, 247, 255)
SILVER = (176, 190, 215)
INK = (4, 8, 16)

img = Image.new("RGBA", (W, H), NAVY_TOP + (255,))
d = ImageDraw.Draw(img)

for y in range(H):
    t = y / (H - 1)
    r = int(NAVY_TOP[0] * (1 - t) + NAVY_BOT[0] * t)
    g = int(NAVY_TOP[1] * (1 - t) + NAVY_BOT[1] * t)
    b = int(NAVY_TOP[2] * (1 - t) + NAVY_BOT[2] * t)
    d.line([(0, y), (W, y)], fill=(r, g, b, 255))


def composite(draw_fn, blur=0):
    global img, d
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld)
    if blur > 0:
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img = Image.alpha_composite(img, layer)
    d = ImageDraw.Draw(img)


rng = random.Random(40)

# Atmosphere
composite(lambda ld: ld.ellipse([(160, 130), (1240, 960)], fill=(20, 80, 150, 34)), blur=100)
composite(lambda ld: ld.ellipse([(330, 260), (1070, 850)], fill=(120, 170, 255, 26)), blur=80)

cx, cy = 700, 560

# Release-oriented central panel
panel_outer = [(430, 280), (970, 280), (1090, 560), (970, 840), (430, 840), (310, 560)]
panel_inner = [(500, 350), (900, 350), (995, 560), (900, 770), (500, 770), (405, 560)]
composite(lambda ld: ld.polygon(panel_outer, fill=(18, 36, 82, 138), outline=CYAN + (130,)), blur=10)
composite(lambda ld: ld.polygon(panel_inner, fill=(10, 18, 42, 182), outline=WHITE + (65,)), blur=2)

# Nested release/build frames
for i, alpha in enumerate([95, 70, 48]):
    inset = 34 + i * 42
    composite(
        lambda ld, inset=inset, alpha=alpha: ld.rounded_rectangle(
            [(430 + inset, 320 + inset * 0.7), (970 - inset, 800 - inset * 0.7)],
            radius=28,
            outline=(110, 190, 255, alpha),
            width=3,
        ),
        blur=3,
    )

# Central release chip / command surface
composite(lambda ld: ld.rounded_rectangle([(555, 455), (845, 665)], radius=34, fill=(20, 28, 56, 210), outline=CYAN_SOFT + (120,)), blur=2)
composite(lambda ld: ld.rounded_rectangle([(585, 490), (815, 630)], radius=24, fill=(14, 20, 40, 230), outline=WHITE + (70,)), blur=1)
composite(lambda ld: ld.ellipse([(615, 440), (785, 610)], fill=(170, 215, 255, 30)), blur=28)

# Subtle internal UI rails instead of stars
for y in [395, 430, 700, 735]:
    composite(lambda ld, y=y: ld.line([(470, y), (930, y)], fill=(70, 125, 220, 40), width=2), blur=1)
for x in [495, 560, 840, 905]:
    composite(lambda ld, x=x: ld.line([(x, 360), (x, 760)], fill=(70, 125, 220, 24), width=2), blur=1)

# Story connectors routed into the release core
nodes = [
    ((385, 430), CYAN, "release"),
    ((1015, 415), AMBER, "google"),
    ((420, 710), MAGENTA, "deepseek"),
    ((1005, 705), CYAN_SOFT, "vercel"),
]
for (nx, ny), col, _ in nodes:
    bend_x = 520 if nx < cx else 880
    composite(lambda ld, nx=nx, ny=ny, col=col, bend_x=bend_x: ld.line([(nx, ny), (bend_x, ny), (cx, cy)], fill=col + (48,), width=6), blur=16)
    composite(lambda ld, nx=nx, ny=ny, col=col, bend_x=bend_x: ld.line([(nx, ny), (bend_x, ny), (cx, cy)], fill=col + (170,), width=2), blur=1)
    composite(lambda ld, nx=nx, ny=ny, col=col: ld.rounded_rectangle([(nx - 22, ny - 22), (nx + 22, ny + 22)], radius=10, fill=col + (200,), outline=WHITE + (65,)), blur=0)
    composite(lambda ld, nx=nx, ny=ny: ld.ellipse([(nx - 6, ny - 6), (nx + 6, ny + 6)], fill=WHITE + (255,)), blur=0)

# Center accents suggest release/build artifact rather than sky
for x in [615, 700, 785]:
    composite(lambda ld, x=x: ld.rounded_rectangle([(x - 22, 540), (x + 22, 580)], radius=8, fill=AMBER + (180,), outline=AMBER_SOFT + (80,)), blur=1)
for y in [510, 620]:
    composite(lambda ld, y=y: ld.line([(590, y), (810, y)], fill=CYAN_SOFT + (95,), width=3), blur=2)

# Replace stars/shards with release-interface widgets
widget_rows = [250, 300, 790, 840]
for y in widget_rows:
    for x in [250, 360, 1040, 1150]:
        w = 42
        h = 14
        col = rng.choice([CYAN, CYAN_SOFT, AMBER, MAGENTA])
        composite(lambda ld, x=x, y=y, w=w, h=h, col=col: ld.rounded_rectangle([(x - w, y - h), (x + w, y + h)], radius=7, outline=col + (42,), width=2), blur=2)
        composite(lambda ld, x=x, y=y, w=w, col=col: ld.line([(x - w + 8, y), (x + w - 8, y)], fill=col + (70,), width=2), blur=1)

for x in [210, 1190]:
    composite(lambda ld, x=x: ld.rounded_rectangle([(x - 32, 390), (x + 32, 730)], radius=18, outline=(80, 130, 220, 28), width=3), blur=3)
    for y in [445, 515, 585, 655]:
        composite(lambda ld, x=x, y=y: ld.rounded_rectangle([(x - 18, y - 10), (x + 18, y + 10)], radius=5, fill=(30, 60, 120, 120), outline=CYAN_SOFT + (50,)), blur=1)

for y in [370, 748]:
    composite(lambda ld, y=y: ld.line([(300, y), (1100, y)], fill=(70, 120, 210, 26), width=3), blur=2)
    for x in [430, 560, 700, 840, 970]:
        composite(lambda ld, x=x, y=y: ld.ellipse([(x - 5, y - 5), (x + 5, y + 5)], fill=CYAN_SOFT + (85,)), blur=1)

# Lower blackout panel for title legibility
composite(lambda ld: ld.rectangle([(0, 930), (W, H)], fill=INK + (235,)), blur=0)
composite(lambda ld: ld.rectangle([(0, 860), (W, 1030)], fill=(8, 18, 38, 120)), blur=45)

# Fonts
try:
    font_brand = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 64)
    font_ep = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 86)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 38)
    font_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
except Exception:
    font_brand = font_ep = font_title = font_sub = font_tag = ImageFont.load_default()


def centered_text(text, y, font, fill, glow=None, blur=14, tracking=0):
    bbox = d.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    x = (W - width) // 2
    if glow:
        composite(lambda ld, x=x, y=y, text=text, font=font, glow=glow: ld.text((x, y), text, font=font, fill=glow + (130,)), blur=blur)
    d.text((x, y), text, font=font, fill=fill)

centered_text("OPENCLAW DAILY", 56, font_brand, SILVER, glow=(20, 20, 30), blur=8)
centered_text("EP039", 128, font_ep, AMBER, glow=AMBER_SOFT, blur=12)

centered_text("OPENCLAW", 980, font_title, WHITE, glow=(160, 190, 255), blur=18)
centered_text("GOOGLE DEAL", 1080, font_title, AMBER, glow=AMBER_SOFT, blur=16)
centered_text("DEEPSEEK V4  •  VERCEL SPILLOVER", 1188, font_sub, CYAN_SOFT, glow=(80, 170, 255), blur=12)
centered_text("v2026.4.23 leads the release block", 1280, font_tag, SILVER, glow=(20, 30, 45), blur=8)

# Vignette + sharpen
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vig)
for i in range(22):
    m = i * 22
    alpha = 8
    vd.rectangle([(m, m), (W - m, H - m)], outline=(0, 0, 0, alpha), width=10)
vig = vig.filter(ImageFilter.GaussianBlur(16))
img = Image.alpha_composite(img, vig)
img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=145, threshold=3))

img = img.convert("RGB")
img.save(OUT, quality=95)
img.save(WEB_OUT, quality=95)
img.save(CDN_OUT, quality=95)
print(f"Saved: {OUT}")
print(f"Copied: {WEB_OUT}")
print(f"Copied: {CDN_OUT}")
