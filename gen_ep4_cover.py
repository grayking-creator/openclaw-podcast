#!/usr/bin/env python3
"""
Episode 4 Cover Art Generator
Programmatic cyberpunk/synthwave style matching the OpenClaw Daily series.
Episode 4 theme: "The Agents Awakening" - AI agents going autonomous, taking action
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math
import random

W, H = 1400, 1400
random.seed(42)

# === BASE: Deep black background with subtle blue-purple gradient ===
img = Image.new('RGB', (W, H), (0, 0, 0))
draw = ImageDraw.Draw(img)

# Background gradient - deep void
for y in range(H):
    t = y / H
    r = int(0 + t * 5)
    g = int(0 + t * 2)
    b = int(15 + t * 25)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# === CIRCUIT BOARD GRID (subtle) ===
grid_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid_layer)

# Horizontal and vertical grid lines - very faint
for x in range(0, W, 40):
    alpha = random.randint(8, 20)
    gd.line([(x, 0), (x, H)], fill=(0, 80, 120, alpha), width=1)
for y in range(0, H, 40):
    alpha = random.randint(8, 20)
    gd.line([(0, y), (W, y)], fill=(0, 80, 120, alpha), width=1)

img = Image.alpha_composite(img.convert('RGBA'), grid_layer).convert('RGB')

# === CENTRAL CLAW ICON - geometric mechanical claw ===
# The OpenClaw claw: three prongs emerging from a central hub, glowing cyan

def draw_glow_line(draw, p1, p2, color, width, glow_passes=3):
    """Draw a line with glow effect by layering with decreasing alpha."""
    r, g, b = color
    for i in range(glow_passes, 0, -1):
        alpha_factor = i / glow_passes
        w = width + (glow_passes - i) * 3
        # We can't do alpha in RGB mode directly, so just vary brightness
        cr = int(r * alpha_factor)
        cg = int(g * alpha_factor)
        cb = int(b * alpha_factor)
        draw.line([p1, p2], fill=(cr, cg, cb), width=w)

# Create a separate RGBA layer for glow effects
glow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd2 = ImageDraw.Draw(glow_layer)

cx, cy = 700, 620  # Center of claw

# Three claw prongs - pointing outward-downward
prong_angles = [-120, 0, 120]  # degrees from top
prong_length = 220
prong_curve_offset = 40

cyan = (0, 220, 255)
orange = (255, 140, 0)
magenta = (220, 0, 255)

prong_colors = [cyan, orange, magenta]

for i, angle_deg in enumerate(prong_angles):
    angle = math.radians(angle_deg + 90)  # +90 so 0 = downward
    
    # Prong tip
    tip_x = cx + prong_length * math.cos(angle)
    tip_y = cy + prong_length * math.sin(angle)
    
    # Curved prong - draw with intermediate points
    mid_x = cx + (prong_length * 0.6) * math.cos(angle)
    mid_y = cy + (prong_length * 0.6) * math.sin(angle)
    
    # Hook curve at the end
    hook_angle = angle + math.radians(30)
    hook_x = tip_x + 50 * math.cos(hook_angle)
    hook_y = tip_y + 50 * math.sin(hook_angle)
    
    color = prong_colors[i]
    r, g, b = color
    
    # Outer glow (wide, dim)
    gd2.line([(cx, cy), (int(tip_x), int(tip_y))], fill=(r, g, b, 40), width=20)
    # Mid glow
    gd2.line([(cx, cy), (int(tip_x), int(tip_y))], fill=(r, g, b, 80), width=10)
    # Core bright line
    gd2.line([(cx, cy), (int(tip_x), int(tip_y))], fill=(r, g, b, 220), width=3)
    
    # Hook
    gd2.line([(int(tip_x), int(tip_y)), (int(hook_x), int(hook_y))], fill=(r, g, b, 180), width=3)
    gd2.line([(int(tip_x), int(tip_y)), (int(hook_x), int(hook_y))], fill=(r, g, b, 60), width=10)

# Central hub - glowing circle
for radius in [60, 45, 30, 15, 8]:
    alpha = int(255 * (1 - radius/70))
    gd2.ellipse([(cx-radius, cy-radius), (cx+radius, cy+radius)], 
                outline=(0, 200, 255, min(255, alpha + 50)), width=2)

# Filled center
gd2.ellipse([(cx-8, cy-8), (cx+8, cy+8)], fill=(0, 255, 255, 200))

# === DATA STREAMS - vertical flowing lines ===
for _ in range(25):
    x = random.randint(50, W-50)
    y_start = random.randint(-50, H//2)
    length = random.randint(30, 150)
    color_choice = random.choice([(0, 180, 255), (255, 120, 0), (180, 0, 255)])
    r, g, b = color_choice
    alpha = random.randint(30, 100)
    gd2.line([(x, y_start), (x, y_start + length)], fill=(r, g, b, alpha), width=1)

# === CIRCUIT TRACES radiating from center ===
trace_colors = [(0, 180, 255, 60), (255, 100, 0, 50), (180, 0, 255, 40)]
for _ in range(20):
    start_angle = random.uniform(0, 2*math.pi)
    start_r = random.randint(80, 120)
    sx = cx + start_r * math.cos(start_angle)
    sy = cy + start_r * math.sin(start_angle)
    
    # L-shaped trace
    seg1_len = random.randint(60, 180)
    turn_angle = start_angle + random.choice([math.pi/2, -math.pi/2])
    seg2_len = random.randint(40, 120)
    
    mx = sx + seg1_len * math.cos(start_angle)
    my = sy + seg1_len * math.sin(start_angle)
    ex = mx + seg2_len * math.cos(turn_angle)
    ey = my + seg2_len * math.sin(turn_angle)
    
    color = random.choice(trace_colors)
    gd2.line([(int(sx), int(sy)), (int(mx), int(my))], fill=color, width=1)
    gd2.line([(int(mx), int(my)), (int(ex), int(ey))], fill=color, width=1)
    # Node dot at corner
    gd2.ellipse([(int(mx)-3, int(my)-3), (int(mx)+3, int(my)+3)], fill=color)

# === HEXAGON RING around claw ===
hex_radius = 180
for i in range(6):
    angle1 = math.radians(i * 60 - 30)
    angle2 = math.radians((i+1) * 60 - 30)
    x1 = cx + hex_radius * math.cos(angle1)
    y1 = cy + hex_radius * math.sin(angle1)
    x2 = cx + hex_radius * math.cos(angle2)
    y2 = cy + hex_radius * math.sin(angle2)
    gd2.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=(0, 180, 255, 120), width=2)
    gd2.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=(0, 100, 200, 40), width=8)

# Outer hex ring (slightly larger, dimmer)
hex_radius2 = 270
for i in range(6):
    angle1 = math.radians(i * 60)
    angle2 = math.radians((i+1) * 60)
    x1 = cx + hex_radius2 * math.cos(angle1)
    y1 = cy + hex_radius2 * math.sin(angle1)
    x2 = cx + hex_radius2 * math.cos(angle2)
    y2 = cy + hex_radius2 * math.sin(angle2)
    gd2.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=(0, 100, 160, 50), width=1)

# === SPARK PARTICLES ===
for _ in range(80):
    px = random.randint(200, 1200)
    py = random.randint(200, 1000)
    size = random.randint(1, 4)
    dist = math.sqrt((px-cx)**2 + (py-cy)**2)
    if dist > 150:  # Outside claw hub
        color_choice = random.choice([
            (0, 200, 255, random.randint(80, 200)),
            (255, 140, 0, random.randint(60, 160)),
            (200, 0, 255, random.randint(40, 120)),
            (255, 255, 255, random.randint(100, 220))
        ])
        gd2.ellipse([(px-size, py-size), (px+size, py+size)], fill=color_choice)

# === ENERGY RINGS (expanding from center) ===
for ring_r in [300, 400, 500]:
    alpha = max(0, 60 - ring_r//10)
    gd2.arc([(cx-ring_r, cy-ring_r), (cx+ring_r, cy+ring_r)], 
            0, 360, fill=(0, 150, 255, alpha), width=1)

# Apply the glow layer
img = Image.alpha_composite(img.convert('RGBA'), glow_layer)

# === BLUR PASS for glow softness ===
# Blur then composite back for bloom effect
blurred = img.filter(ImageFilter.GaussianBlur(radius=4))
img = ImageChops.screen(img, blurred.point(lambda x: x * 0.4))

img = img.convert('RGB')

# === BOTTOM GRADIENT OVERLAY for text legibility ===
overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for i in range(500):
    alpha = int(210 * (i / 500) ** 1.5)
    od.rectangle([(0, 900 + i), (W, 901 + i)], fill=(0, 0, 0, alpha))

# Also top gradient for header text
for i in range(200):
    alpha = int(160 * (1 - i/200) ** 1.2)
    od.rectangle([(0, i), (W, i+1)], fill=(0, 0, 10, alpha))

img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

draw = ImageDraw.Draw(img)

# === TEXT OVERLAY ===
try:
    font_ep = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 52)
    font_show = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 38)
    font_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 76)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 32)
except:
    try:
        font_ep = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 52)
        font_show = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 38)
        font_title = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 76)
        font_sub = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 32)
    except:
        font_ep = ImageFont.load_default()
        font_show = font_ep
        font_title = font_ep
        font_sub = font_ep

# Episode badge - top left
draw.text((70, 65), "EP. 4", fill=(80, 160, 255), font=font_ep)
draw.text((70, 130), "OpenClaw Daily", fill=(190, 195, 210), font=font_show)

# Thin accent line under header
draw.line([(70, 178), (400, 178)], fill=(0, 120, 220, 180), width=1)

# Episode title - bottom
episode_title = "The Agents Awakening"
draw.text((70, 1235), episode_title, fill=(255, 255, 255), font=font_title)

# Subtitle
draw.text((70, 1325), "Nova & Alloy  •  OpenClaw Daily", fill=(120, 130, 160), font=font_sub)

# === SAVE ===
out_path = '/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/episode_004_cover.jpg'
img.save(out_path, quality=95)
print(f"Saved: {out_path}")
print(f"Size: {img.size}")
