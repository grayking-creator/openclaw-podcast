#!/usr/bin/env python3
"""Episode 12 Cover Art Generator

Theme: Free Frontier Models, Multimodal Memory & Community Automations
Visual: Dark synthwave/cyberpunk aesthetic with glowing network of interconnected nodes
representing community automations (morning briefing, email triage, calendar, server monitoring, knowledge base).
Add visual elements: alpha symbol for free models, eye/brain for multimodal memory, Ollama llama.
Color palette: deep purples, electric blues, neon cyan accents.

Outputs: images/episode_012_cover.png (1400x1400)
"""

from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math
import random
from pathlib import Path

W, H = 1400, 1400
random.seed(12012)

out_path = Path(__file__).parent / "images" / "episode_012_cover.png"
out_path.parent.mkdir(parents=True, exist_ok=True)

# Base background
img = Image.new("RGB", (W, H), (0, 0, 0))
draw = ImageDraw.Draw(img)

# Vertical gradient (deep purple -> near black)
for y in range(H):
    t = y / H
    r = int(8 + t * 6)
    g = int(0 + t * 4)
    b = int(24 + t * 25)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Subtle grid layer (synthwave cyan/purple)
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)

for x in range(0, W, 50):
    a = random.randint(6, 16)
    gd.line([(x, 0), (x, H)], fill=(0, 200, 255, a), width=1)
for y in range(0, H, 50):
    a = random.randint(6, 16)
    gd.line([(0, y), (W, y)], fill=(150, 50, 255, a), width=1)

img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")

# Glow layer
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
lg = ImageDraw.Draw(glow)

# Node layout - central hub with community automation nodes
cx, cy = 700, 520

# Central hub node
central_node = {"x": cx, "y": cy, "r": 65, "c": (0, 255, 255)}  # neon cyan

# Community automation nodes (outer ring)
automation_nodes = [
    {"x": cx - 280, "y": cy - 80, "r": 28, "c": (180, 60, 255), "label": "Morning Briefing"},    # purple
    {"x": cx + 290, "y": cy - 60, "r": 26, "c": (0, 180, 255), "label": "Email Triage"},        # blue
    {"x": cx + 200, "y": cy + 220, "r": 30, "c": (255, 100, 200), "label": "Calendar"},         # pink
    {"x": cx - 210, "y": cy + 230, "r": 26, "c": (0, 255, 180), "label": "Server Monitor"},     # green-cyan
    {"x": cx, "y": cy - 280, "r": 32, "c": (255, 200, 0), "label": "Knowledge Base"},         # gold
]

# Special feature nodes
# Alpha/Free models (top-left)
alpha_node = {"x": cx - 180, "y": cy + 80, "r": 35, "c": (255, 140, 0)}  # orange

# Multimodal memory (eye/brain) - top-right
memory_node = {"x": cx + 180, "y": cy + 60, "r": 38, "c": (200, 50, 255)}  # magenta/purple

# Ollama llama - bottom center
ollama_node = {"x": cx, "y": cy + 180, "r": 32, "c": (100, 200, 255)}  # light blue

nodes = [central_node] + automation_nodes + [alpha_node, memory_node, ollama_node]

# Connections from central hub to all nodes
connections = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),  # central to automation
    (0, 6), (0, 7), (0, 8),  # central to special features
    # Cross connections between automation nodes
    (1, 4), (1, 6),
    (2, 7), (2, 8),
    (3, 8),
    (4, 6),
    # Connect special features
    (6, 7), (7, 8),
]

for i, j in connections:
    n1, n2 = nodes[i], nodes[j]
    r, g, b = n1["c"]
    # Glow lines
    lg.line([(n1["x"], n1["y"]), (n2["x"], n2["y"])], fill=(r, g, b, 30), width=12)
    lg.line([(n1["x"], n1["y"]), (n2["x"], n2["y"])], fill=(r, g, b, 80), width=4)
    lg.line([(n1["x"], n1["y"]), (n2["x"], n2["y"])], fill=(255, 255, 255, 30), width=1)

# Draw nodes with multi-glow
for idx, n in enumerate(nodes):
    x, y, rad = n["x"], n["y"], n["r"]
    r, g, b = n["c"]
    
    # Special drawing for central node
    if idx == 0:
        # Outer glow rings
        lg.ellipse([(x - rad - 30, y - rad - 30), (x + rad + 30, y + rad + 30)], fill=(r, g, b, 8))
        lg.ellipse([(x - rad - 18, y - rad - 18), (x + rad + 18, y + rad + 18)], fill=(r, g, b, 20))
        lg.ellipse([(x - rad - 10, y - rad - 10), (x + rad + 10, y + rad + 10)], fill=(r, g, b, 50))
    
    # Regular node outer glow
    lg.ellipse([(x - rad - 16, y - rad - 16), (x + rad + 16, y + rad + 16)], fill=(r, g, b, 10))
    lg.ellipse([(x - rad - 8, y - rad - 8), (x + rad + 8, y + rad + 8)], fill=(r, g, b, 30))
    lg.ellipse([(x - rad - 3, y - rad - 3), (x + rad + 3, y + rad + 3)], fill=(r, g, b, 70))
    
    # Core
    lg.ellipse([(x - rad, y - rad), (x + rad, y + rad)], fill=(r, g, b, 130))
    lg.ellipse([(x - rad // 2, y - rad // 2), (x + rad // 2, y + rad // 2)], fill=(255, 255, 255, 120))

# Alpha symbol (stylized "A" with crown) on alpha node
alpha_x, alpha_y = alpha_node["x"], alpha_node["y"]
alpha_color = alpha_node["c"]
# Draw a stylized alpha symbol
for offset in range(-2, 3):
    lg.line([(alpha_x - 12, alpha_y + 10 + offset), (alpha_x, alpha_y - 15 + offset)], fill=(*alpha_color, 150), width=2)
    lg.line([(alpha_x, alpha_y - 15 + offset), (alpha_x + 12, alpha_y + 10 + offset)], fill=(*alpha_color, 150), width=2)
    lg.line([(alpha_x - 6, alpha_y - 2 + offset), (alpha_x + 6, alpha_y - 2 + offset)], fill=(*alpha_color, 150), width=2)

# Eye/brain symbol for multimodal memory
mem_x, mem_y = memory_node["x"], memory_node["y"]
mem_color = memory_node["c"]
# Eye outline
lg.ellipse([(mem_x - 15, mem_y - 10), (mem_x + 15, mem_y + 10)], outline=(*mem_color, 180), width=2)
# Iris
lg.ellipse([(mem_x - 8, mem_y - 6), (mem_x + 8, mem_y + 6)], fill=(*mem_color, 160))
# Pupil
lg.ellipse([(mem_x - 4, mem_y - 3), (mem_x + 4, mem_y + 3)], fill=(0, 0, 0, 200))
# Brain waves above
lg.arc([(mem_x - 20, mem_y - 30), (mem_x + 20, mem_y - 10)], 180, 360, fill=(*mem_color, 140), width=2)

# Llama silhouette for Ollama
ollama_x, ollama_y = ollama_node["x"], ollama_node["y"]
ollama_color = ollama_node["c"]
# Simple llama head shape
lg.ellipse([(ollama_x - 10, ollama_y - 18), (ollama_x + 10, ollama_y - 2)], fill=(*ollama_color, 160))  # head
lg.ellipse([(ollama_x - 6, ollama_y - 25), (ollama_x + 6, ollama_y - 18)], fill=(*ollama_color, 140))  # ears
lg.ellipse([(ollama_x - 12, ollama_y - 2), (ollama_x + 12, ollama_y + 12)], fill=(*ollama_color, 140))  # body

# Speckles for atmosphere
for _ in range(150):
    px = random.randint(60, W - 60)
    py = random.randint(60, H - 60)
    a = random.randint(30, 180)
    c = random.choice([
        (0, 255, 255, a),       # cyan
        (180, 60, 255, a),      # purple
        (255, 100, 200, a),    # pink
        (0, 255, 180, a),       # green-cyan
        (255, 200, 0, a),       # gold
        (255, 255, 255, a),     # white
    ])
    s = random.randint(1, 3)
    lg.ellipse([(px - s, py - s), (px + s, py + s)], fill=c)

# Composite glow with blur
base = img.convert("RGBA")
blur = glow.filter(ImageFilter.GaussianBlur(radius=8))
combo = ImageChops.screen(base, blur)
combo = ImageChops.screen(combo, glow)

# Add bottom fade for text area
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for i in range(480):
    a = int(200 * (i / 480))
    od.rectangle([0, H - 480 + i, W, H - 480 + i + 1], fill=(0, 0, 0, a))
combo = Image.alpha_composite(combo, overlay)

final = combo.convert("RGB")

# Draw text using ImageDraw
final_draw = ImageDraw.Draw(final)

# "OPENCLAW DAILY" at top
import subprocess
try:
    # Use a bold system font if available
    from PIL import ImageFont
    font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 72)
    font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    font_episode = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 90)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_episode = ImageFont.load_default()

# Title at top
title = "OPENCLAW DAILY"
# Get text bounds for centering
bbox = final_draw.textbbox((0, 0), title, font=font_large)
title_w = bbox[2] - bbox[0]
final_draw.text(((W - title_w) // 2, 45), title, fill=(0, 255, 255), font=font_large)

# Episode number - prominent
ep_text = "EPISODE 12"
bbox = final_draw.textbbox((0, 0), ep_text, font=font_episode)
ep_w = bbox[2] - bbox[0]
final_draw.text(((W - ep_w) // 2, H - 180), ep_text, fill=(255, 255, 255), font=font_episode)

# Subtitle
subtitle = "Free Frontier Models • Multimodal Memory • Community Automations"
bbox = final_draw.textbbox((0, 0), subtitle, font=font_small)
sub_w = bbox[2] - bbox[0]
final_draw.text(((W - sub_w) // 2, H - 85), subtitle, fill=(180, 100, 255), font=font_small)

final.save(out_path)
print(f"Wrote {out_path}")
