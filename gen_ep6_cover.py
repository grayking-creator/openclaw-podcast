#!/usr/bin/env python3
"""
Episode 6 Cover Art Generator
Programmatic cyberpunk/synthwave style matching the OpenClaw Daily series.
Episode 6 theme: "The v2026.2.24 Update & Bot Social Networks" - interconnected nodes representing bots talking to each other.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math
import random

W, H = 1400, 1400
random.seed(126)  # Different seed for variety

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

# === NETWORK GRAPH - Bot social network nodes ===
# Central hub (largest, brightest cyan) surrounded by smaller nodes in orange/magenta/purple
# This represents bots talking to each other

cx, cy = 700, 600  # Center of network

# Create glow layer
glow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd2 = ImageDraw.Draw(glow_layer)

# Define node positions - central hub + surrounding nodes
nodes = [
    # Central hub - largest, brightest cyan
    {'x': cx, 'y': cy, 'radius': 55, 'color': (0, 220, 255), 'glow': 60},
    # First ring - 6 nodes around center
    {'x': cx + 180, 'y': cy - 100, 'radius': 28, 'color': (255, 140, 0), 'glow': 40},   # orange
    {'x': cx + 160, 'y': cy + 140, 'radius': 30, 'color': (220, 0, 255), 'glow': 40},   # magenta
    {'x': cx - 50, 'y': cy + 200, 'radius': 25, 'color': (255, 100, 50), 'glow': 35},   # orange-red
    {'x': cx - 190, 'y': cy + 50, 'radius': 32, 'color': (180, 0, 220), 'glow': 42},   # purple
    {'x': cx - 170, 'y': cy - 140, 'radius': 26, 'color': (255, 120, 0), 'glow': 38},   # orange
    {'x': cx + 30, 'y': cy - 200, 'radius': 24, 'color': (200, 0, 255), 'glow': 35},    # magenta
    # Second ring - 5 more distant nodes
    {'x': cx + 280, 'y': cy + 30, 'radius': 18, 'color': (100, 180, 255), 'glow': 25},
    {'x': cx + 200, 'y': cy - 220, 'radius': 20, 'color': (255, 80, 150), 'glow': 28},
    {'x': cx - 100, 'y': cy - 240, 'radius': 17, 'color': (180, 100, 255), 'glow': 24},
    {'x': cx - 280, 'y': cy - 80, 'radius': 19, 'color': (255, 150, 0), 'glow': 26},
    {'x': cx - 250, 'y': cy + 180, 'radius': 16, 'color': (220, 50, 200), 'glow': 22},
]

# Draw connection lines between nodes (representing bot-to-bot communication)
connections = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),  # Center to first ring
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1),  # Ring connections
    (1, 7), (2, 7), (2, 8), (6, 8), (6, 9), (5, 9),
    (4, 10), (4, 11), (3, 11),  # Outer connections
]

# Draw connections first (behind nodes)
for i, j in connections:
    n1, n2 = nodes[i], nodes[j]
    r, g, b = n1['color']
    # Glow line
    gd2.line([(n1['x'], n1['y']), (n2['x'], n2['y'])], fill=(r, g, b, 30), width=8)
    gd2.line([(n1['x'], n1['y']), (n2['x'], n2['y'])], fill=(r, g, b, 60), width=3)
    # Core bright line
    gd2.line([(n1['x'], n1['y']), (n2['x'], n2['y'])], fill=(r, g, b, 150), width=1)

# Draw nodes - glow effect layers
for node in nodes:
    x, y = node['x'], node['y']
    r, g, b = node['color']
    radius = node['radius']
    glow_intensity = node['glow']
    
    # Outer glow (wide, dim)
    gd2.ellipse([(x-radius-15, y-radius-15), (x+radius+15, y+radius+15)], 
                fill=(r, g, b, 15))
    # Mid glow
    gd2.ellipse([(x-radius-8, y-radius-8), (x+radius+8, y+radius+8)], 
                fill=(r, g, b, 35))
    # Inner glow
    gd2.ellipse([(x-radius-3, y-radius-3), (x+radius+3, y+radius+3)], 
                fill=(r, g, b, 80))
    # Core bright center
    gd2.ellipse([(x-radius//2, y-radius//2), (x+radius//2, y+radius//2)], 
                fill=(r, g, b, 200))
    # Brightest center dot
    gd2.ellipse([(x-3, y-3), (x+3, y+3)], fill=(255, 255, 255, 230))

# === DATA STREAMS - vertical flowing lines (data flowing between bots) ===
for _ in range(25):
    x = random.randint(50, W-50)
    y_start = random.randint(-50, H//2)
    length = random.randint(30, 150)
    color_choice = random.choice([(0, 180, 255), (255, 120, 0), (180, 0, 255)])
    r, g, b = color_choice
    alpha = random.randint(30, 100)
    gd2.line([(x, y_start), (x, y_start + length)], fill=(r, g, b, alpha), width=1)

# === CIRCUIT TRACES radiating from network center ===
trace_colors = [(0, 180, 255, 60), (255, 100, 0, 50), (180, 0, 255, 40)]
for _ in range(15):
    start_angle = random.uniform(0, 2*math.pi)
    start_r = random.randint(200, 280)
    sx = cx + start_r * math.cos(start_angle)
    sy = cy + start_r * math.sin(start_angle)
    
    # L-shaped trace
    seg1_len = random.randint(60, 150)
    turn_angle = start_angle + random.choice([math.pi/2, -math.pi/2])
    seg2_len = random.randint(40, 100)
    
    mx = sx + seg1_len * math.cos(start_angle)
    my = sy + seg1_len * math.sin(start_angle)
    ex = mx + seg2_len * math.cos(turn_angle)
    ey = my + seg2_len * math.sin(turn_angle)
    
    color = random.choice(trace_colors)
    gd2.line([(int(sx), int(sy)), (int(mx), int(my))], fill=color, width=1)
    gd2.line([(int(mx), int(my)), (int(ex), int(ey))], fill=color, width=1)
    # Node dot at corner
    gd2.ellipse([(int(mx)-3, int(my)-3), (int(mx)+3, int(my)+3)], fill=color)

# === HEXAGON RING around network ===
hex_radius = 320
for i in range(6):
    angle1 = math.radians(i * 60 - 30)
    angle2 = math.radians((i+1) * 60 - 30)
    x1 = cx + hex_radius * math.cos(angle1)
    y1 = cy + hex_radius * math.sin(angle1)
    x2 = cx + hex_radius * math.cos(angle2)
    y2 = cy + hex_radius * math.sin(angle2)
    gd2.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=(0, 180, 255, 100), width=2)
    gd2.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=(0, 100, 200, 30), width=8)

# Outer hex ring
hex_radius2 = 400
for i in range(6):
    angle1 = math.radians(i * 60)
    angle2 = math.radians((i+1) * 60)
    x1 = cx + hex_radius2 * math.cos(angle1)
    y1 = cy + hex_radius2 * math.sin(angle1)
    x2 = cx + hex_radius2 * math.cos(angle2)
    y2 = cy + hex_radius2 * math.sin(angle2)
    gd2.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=(0, 100, 160, 40), width=1)

# === SPARK PARTICLES ===
for _ in range(80):
    px = random.randint(200, 1200)
    py = random.randint(200, 1000)
    size = random.randint(1, 4)
    dist = math.sqrt((px-cx)**2 + (py-cy)**2)
    if dist > 250:  # Outside network area
        color_choice = random.choice([
            (0, 200, 255, random.randint(80, 200)),
            (255, 140, 0, random.randint(60, 160)),
            (200, 0, 255, random.randint(40, 120)),
            (255, 255, 255, random.randint(100, 220))
        ])
        gd2.ellipse([(px-size, py-size), (px+size, py+size)], fill=color_choice)

# === ENERGY RINGS (expanding from center) ===
for ring_r in [380, 450, 520]:
    alpha = max(0, 50 - ring_r//15)
    gd2.arc([(cx-ring_r, cy-ring_r), (cx+ring_r, cy+ring_r)], 
            0, 360, fill=(0, 150, 255, alpha), width=1)

# Apply the glow layer
img = Image.alpha_composite(img.convert('RGBA'), glow_layer)

# === BLUR PASS for glow softness ===
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
    font_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 68)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 32)
except:
    try:
        font_ep = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 52)
        font_show = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 38)
        font_title = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 68)
        font_sub = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 32)
    except:
        font_ep = ImageFont.load_default()
        font_show = font_ep
        font_title = font_ep
        font_sub = font_ep

# Episode badge - top left
draw.text((70, 65), "EP. 6", fill=(80, 160, 255), font=font_ep)
draw.text((70, 130), "OpenClaw Daily", fill=(190, 195, 210), font=font_show)

# Thin accent line under header
draw.line([(70, 178), (400, 178)], fill=(0, 120, 220, 180), width=1)

# Episode title - bottom (may need to split to 2 lines)
episode_title = "The v2026.2.24 Update"
episode_title2 = "& Bot Social Networks"
draw.text((70, 1200), episode_title, fill=(255, 255, 255), font=font_title)
draw.text((70, 1280), episode_title2, fill=(255, 255, 255), font=font_title)

# Subtitle
draw.text((70, 1360), "Nova & Alloy  •  OpenClaw Daily", fill=(120, 130, 160), font=font_sub)

# === SAVE ===
out_path = '/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_006_cover.png'
img.save(out_path, quality=95)
print(f"Saved: {out_path}")
print(f"Size: {img.size}")
