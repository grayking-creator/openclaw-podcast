#!/usr/bin/env python3
"""Generate Episode 13 podcast cover for OpenClaw Daily.
Theme: NVIDIA picks OpenClaw — massive glowing claw ripping open a dark void,
NVIDIA green + OpenClaw cyan energy explosion. Bold, iconic, specific.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

WIDTH, HEIGHT = 1400, 1400
OUTPUT_PATH = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_013_cover.png"

NVIDIA_GREEN  = (118, 185, 0)
BRIGHT_GREEN  = (180, 255, 60)
NEON_GREEN    = (80, 255, 20)
CYAN          = (0, 220, 255)
CYAN_DARK     = (0, 80, 120)
WHITE         = (255, 255, 255)
GRAY          = (130, 145, 155)
BG_DARK       = (3, 6, 10)
BG_MID        = (6, 14, 6)
ORANGE        = (255, 130, 0)

FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def centered_text(draw, text, y, font, color, glow=None, gr=4):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w) // 2
    if glow:
        for ox in range(-gr, gr+1):
            for oy in range(-gr, gr+1):
                if ox*ox+oy*oy <= gr*gr:
                    draw.text((x+ox, y+oy), text, font=font, fill=glow)
    draw.text((x, y), text, font=font, fill=color)

random.seed(13)

# ── 1. Deep black background ─────────────────────────────────────────────────
img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
draw = ImageDraw.Draw(img)

# Faint star field
for _ in range(300):
    sx, sy = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    sr = random.randint(0, 2)
    col = random.choice([(255,255,255), (80,255,20), (0,200,255)])
    alpha = random.randint(30, 120)
    draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr],
                 fill=tuple(int(c*alpha/255) for c in col))

# Subtle hex grid overlay
hex_col = (8, 20, 8)
for row in range(-2, 24):
    for col_i in range(-2, 24):
        hx = col_i * 80 + (40 if row % 2 else 0)
        hy = row * 69
        pts = [(hx + 40*math.cos(math.radians(a+30)),
                hy + 40*math.sin(math.radians(a+30))) for a in range(0,360,60)]
        draw.polygon(pts, outline=hex_col)

# ── 2. Central energy explosion / radial burst ───────────────────────────────
cx, cy = WIDTH // 2, HEIGHT // 2 + 40

# Deep green nebula glow in center
glow_img = Image.new("RGB", (WIDTH, HEIGHT), (0,0,0))
gd = ImageDraw.Draw(glow_img)
for r in range(600, 0, -15):
    t = 1 - r/600
    g_val = int(NVIDIA_GREEN[1] * t * 0.6)
    b_val = int(CYAN[2] * t * 0.3)
    gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(0, g_val, b_val//2))
glow_img = glow_img.filter(ImageFilter.GaussianBlur(80))
img = Image.blend(img, glow_img, 0.85)
draw = ImageDraw.Draw(img)

# ── 3. Three massive claw slash marks ────────────────────────────────────────
# Near-vertical slashes sweeping from top to bottom, spaced like a real claw
# Slash coordinates: top point, bottom point, base width
claw_slashes = [
    (cx - 220, cy - 480,  cx - 80,  cy + 480),   # left claw
    (cx - 40,  cy - 500,  cx + 100, cy + 460),   # center claw
    (cx + 140, cy - 460,  cx + 280, cy + 440),   # right claw
]

# Wide outer glow (NVIDIA green)
for (x1,y1,x2,y2) in claw_slashes:
    for bw in range(60, 0, -8):
        t = bw/60
        col = (int(NVIDIA_GREEN[0]*t*0.4),
               int(NVIDIA_GREEN[1]*t*0.7),
               int(t*40))
        draw.line([(x1,y1),(x2,y2)], fill=col, width=bw*2)

# Mid cyan glow
for (x1,y1,x2,y2) in claw_slashes:
    for bw in range(30, 0, -5):
        t = bw/30
        col = (0, int(200*t), int(255*t))
        draw.line([(x1,y1),(x2,y2)], fill=col, width=bw)

# Bright white/green core
for (x1,y1,x2,y2) in claw_slashes:
    draw.line([(x1,y1),(x2,y2)], fill=BRIGHT_GREEN, width=8)
    draw.line([(x1,y1),(x2,y2)], fill=WHITE, width=3)

# ── 4. Explosive impact sparks at claw tips ──────────────────────────────────
impact_pts = [(x1,y1) for x1,y1,x2,y2 in claw_slashes] + \
             [(x2,y2) for x1,y1,x2,y2 in claw_slashes]

for px, py in impact_pts:
    # Large starburst
    burst_count = 50
    for i in range(burst_count):
        angle = random.uniform(0, 2*math.pi)
        length = random.randint(20, 180)
        ex = px + int(math.cos(angle)*length)
        ey = py + int(math.sin(angle)*length)
        col = random.choice([BRIGHT_GREEN, CYAN, WHITE, NEON_GREEN, ORANGE, NVIDIA_GREEN])
        lw = random.randint(1,4)
        draw.line([(px,py),(ex,ey)], fill=col, width=lw)
    # Bright core
    draw.ellipse([px-18, py-18, px+18, py+18], fill=WHITE)
    draw.ellipse([px-9, py-9, px+9, py+9], fill=BRIGHT_GREEN)

# ── 5. Circuit traces radiating from impact ───────────────────────────────────
for _ in range(24):
    sx = cx + random.randint(-250, 250)
    sy = cy + random.randint(-250, 250)
    angle = random.uniform(0, 2*math.pi)
    seg_len = random.randint(60, 220)
    ex = sx + int(math.cos(angle)*seg_len)
    ey = sy + int(math.sin(angle)*seg_len)
    col = random.choice([NVIDIA_GREEN, CYAN_DARK, (20,60,10)])
    draw.line([(sx,sy),(ex,ey)], fill=col, width=2)
    # elbow
    angle2 = angle + math.pi/2
    ex2 = ex + int(math.cos(angle2)*random.randint(30,100))
    ey2 = ey + int(math.sin(angle2)*random.randint(30,100))
    draw.line([(ex,ey),(ex2,ey2)], fill=col, width=2)

# ── 6. NVIDIA "chip" badge in corner ─────────────────────────────────────────
badge_x, badge_y = WIDTH - 200, HEIGHT - 200
badge_r = 55
draw.ellipse([badge_x-badge_r, badge_y-badge_r,
              badge_x+badge_r, badge_y+badge_r],
             fill=(10, 30, 5), outline=NVIDIA_GREEN, width=3)
font_badge = get_font(28)
bbox = draw.textbbox((0,0),"GPU",font=font_badge)
bw = bbox[2]-bbox[0]
draw.text((badge_x - bw//2, badge_y - 18), "GPU",
          font=font_badge, fill=NVIDIA_GREEN)
font_badge2 = get_font(20)
bbox2 = draw.textbbox((0,0),"NVIDIA",font=font_badge2)
bw2 = bbox2[2]-bbox2[0]
draw.text((badge_x - bw2//2, badge_y + 12), "NVIDIA",
          font=font_badge2, fill=GRAY)

# ── 7. Typography ─────────────────────────────────────────────────────────────
font_show  = get_font(86)
font_ep    = get_font(58)
font_title1 = get_font(90)
font_title2 = get_font(90)
font_sub   = get_font(36)

# Show name
centered_text(draw, "OPENCLAW DAILY", 55, font_show, CYAN,
              glow=(0,60,100), gr=8)

# Separator
draw.line([(WIDTH//2-320, 158), (WIDTH//2+320, 158)],
          fill=(0,80,100), width=2)

# Episode
centered_text(draw, "EPISODE 13", 172, font_ep, NVIDIA_GREEN,
              glow=(20,50,0), gr=5)

# Title — overlaid over claw area, bottom
centered_text(draw, "NVIDIA PICKED", 1060, font_title1, WHITE,
              glow=(20,60,20), gr=4)
centered_text(draw, "OPENCLAW", 1162, font_title2, NVIDIA_GREEN,
              glow=(30,80,0), gr=8)

# Subtitle
centered_text(draw, "NemoClaw  •  Nemotron 3 Super  •  DGX Spark",
              1282, font_sub, GRAY)

# ── 8. Vignette edges ─────────────────────────────────────────────────────────
vig = Image.new("RGB", (WIDTH, HEIGHT), (0,0,0))
vd = ImageDraw.Draw(vig)
for r in range(900, 0, -30):
    alpha = int(140 * (1 - r/900))
    c = (alpha//8, alpha//8, alpha//8)
    vd.ellipse([WIDTH//2-r, HEIGHT//2-r, WIDTH//2+r, HEIGHT//2+r],
               outline=c, width=30)
vig = vig.filter(ImageFilter.GaussianBlur(50))
img = Image.blend(img, vig, 0.3)

img.save(OUTPUT_PATH)
print(f"✅ Cover saved: {OUTPUT_PATH}")
