#!/usr/bin/env python3
"""Generate Episode 11 podcast cover for OpenClaw Daily - CPU/Hardware theme."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import os

# Constants
WIDTH, HEIGHT = 1400, 1400
OUTPUT_PATH = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_011_cover.png"

# Colors
BG_COLOR = (8, 10, 20)  # Near-black #080A14
AMBER = (240, 160, 48)  # #F0A030
ORANGE = (224, 96, 16)  # #E06010
GOLD = (212, 160, 23)   # #D4A017
ORANGE_RED = (224, 80, 32)  # #E05020
WHITE = (255, 255, 255)
MUTED_GRAY = (160, 168, 176)  # #A0A8B0
DARK_GRAY = (122, 128, 144)   # #7A8090
PALE_YELLOW = (255, 250, 200)

# Font paths
FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
FONT_FALLBACK = "/System/Library/Fonts/SFNSDisplay.ttf"

def get_font(size, bold=True):
    """Load font, fallback if needed."""
    try:
        font = ImageFont.truetype(FONT_PATH, size)
    except:
        try:
            font = ImageFont.truetype(FONT_FALLBACK, size)
        except:
            font = ImageFont.load_default()
    return font

def draw_text_with_glow(draw, text, x, y, font, color, glow_color=None, glow_offset=2):
    """Draw text with a glow effect."""
    if glow_color:
        # Draw blurred glow layer
        for ox in range(-glow_offset, glow_offset + 1):
            for oy in range(-glow_offset, glow_offset + 1):
                if ox != 0 or oy != 0:
                    draw.text((x + ox, y + oy), text, font=font, fill=glow_color)
    draw.text((x, y), text, font=font, fill=color)

def create_background():
    """Create background with circuit board pattern."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Subtle circuit grid (PCB-like)
    grid_spacing = 50
    grid_color = (20, 40, 30)  # Very dark green
    
    for x in range(0, WIDTH, grid_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
    for y in range(0, HEIGHT, grid_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)
    
    # Scattered solder point dots
    random.seed(42)
    solder_colors = [AMBER, WHITE, ORANGE, GOLD]
    for _ in range(80):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice(solder_colors)
        radius = random.randint(1, 3)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    # Digital rain streaks in upper right
    for i in range(15):
        x = WIDTH - 200 + random.randint(0, 150)
        y_start = random.randint(-100, HEIGHT // 2)
        length = random.randint(50, 150)
        color = random.choice([AMBER, ORANGE])
        alpha = random.randint(20, 50)
        draw.line([(x, y_start), (x, y_start + length)], fill=(*color[:3], alpha) if len(color) == 4 else color, width=2)
    
    return img, draw

def draw_cpu_chip(draw, center_x, center_y):
    """Draw detailed CPU chip in center."""
    chip_size = 300
    half = chip_size // 2
    
    # Chip body - dark metallic
    chip_body = [
        center_x - half, center_y - half,
        center_x + half, center_y + half
    ]
    draw.rectangle(chip_body, fill=(20, 22, 30), outline=AMBER, width=3)
    
    # Subtle hex/grid texture inside chip
    grid_size = 20
    for gx in range(center_x - half + 10, center_x + half - 10, grid_size):
        for gy in range(center_y - half + 10, center_y + half - 10, grid_size):
            draw.ellipse([gx-2, gy-2, gx+2, gy+2], fill=(30, 32, 40))
    
    # Concentric inner squares (3 nested)
    layers = [180, 130, 80]
    layer_colors = [(40, 42, 55), (50, 52, 65), (60, 62, 75)]
    for size, color in zip(layers, layer_colors):
        offset = (chip_size - size) // 2
        draw.rectangle(
            [center_x - size//2, center_y - size//2,
             center_x + size//2, center_y + size//2],
            outline=color, width=2
        )
    
    # Pin grid array - pins on all 4 sides
    pins_per_side = 10
    pin_length = 25
    pin_color = AMBER
    
    for i in range(pins_per_side):
        # Top side
        px = center_x - half + 30 + i * ((chip_size - 60) // (pins_per_side - 1))
        py_top = center_y - half
        draw.line([(px, py_top), (px, py_top - pin_length)], fill=pin_color, width=2)
        draw.ellipse([px-3, py_top - pin_length - 3, px+3, py_top - pin_length + 3], fill=ORANGE)
        
        # Bottom side
        py_bottom = center_y + half
        draw.line([(px, py_bottom), (px, py_bottom + pin_length)], fill=pin_color, width=2)
        draw.ellipse([px-3, py_bottom + pin_length - 3, px+3, py_bottom + pin_length + 3], fill=ORANGE)
        
        # Left side
        py = center_y - half + 30 + i * ((chip_size - 60) // (pins_per_side - 1))
        px_left = center_x - half
        draw.line([(px_left, py), (px_left - pin_length, py)], fill=pin_color, width=2)
        draw.ellipse([px_left - pin_length - 3, py - 3, px_left - pin_length + 3, py + 3], fill=ORANGE)
        
        # Right side
        px_right = center_x + half
        draw.line([(px_right, py), (px_right + pin_length, py)], fill=pin_color, width=2)
        draw.ellipse([px_right + pin_length - 3, py - 3, px_right + pin_length + 3, py + 3], fill=ORANGE)
    
    # Core glow - bright amber inner glow
    glow_radius = 50
    for r in range(glow_radius, 0, -5):
        alpha = int(255 * (1 - r / glow_radius) * 0.3)
        draw.ellipse(
            [center_x - r, center_y - r, center_x + r, center_y + r],
            fill=(AMBER[0], AMBER[1], AMBER[2], alpha)
        )
    
    # Inner core bright spot
    draw.ellipse([center_x - 20, center_y - 20, center_x + 20, center_y + 20], fill=GOLD)

def draw_circuit_traces(draw, center_x, center_y):
    """Draw glowing circuit traces radiating outward."""
    trace_colors = [AMBER, ORANGE, GOLD, WHITE, PALE_YELLOW]
    random.seed(123)
    
    # 12 radial traces
    num_traces = 12
    for i in range(num_traces):
        angle = (2 * math.pi / num_traces) * i + random.uniform(-0.2, 0.2)
        length = random.randint(200, 350)
        
        end_x = center_x + int(length * math.cos(angle))
        end_y = center_y + int(length * math.sin(angle))
        
        color = random.choice(trace_colors)
        draw.line([(center_x, center_y), (end_x, end_y)], fill=color, width=2)
        
        # Endpoint dot
        dot_radius = random.randint(3, 6)
        draw.ellipse([end_x - dot_radius, end_y - dot_radius, end_x + dot_radius, end_y + dot_radius], fill=ORANGE_RED)

def draw_component_nodes(draw, center_x, center_y):
    """Draw floating component nodes around the chip."""
    components = []
    node_colors = [AMBER, ORANGE_RED, GOLD, WHITE, PALE_YELLOW]
    
    # 6 component nodes positioned around the chip
    positions = [
        (center_x - 280, center_y - 180),
        (center_x + 320, center_y - 150),
        (center_x - 250, center_y + 250),
        (center_x + 280, center_y + 220),
        (center_x - 350, center_y + 50),
        (center_x + 350, center_y - 50),
    ]
    
    random.seed(456)
    for i, (cx, cy) in enumerate(positions):
        color = node_colors[i % len(node_colors)]
        comp_type = i % 3
        
        if comp_type == 0:
            # Resistor (zigzag)
            draw.line([cx-20, cy, cx+20, cy], fill=color, width=3)
            for z in range(-15, 16, 10):
                draw.line([cx+z, cy-8, cx+z+5, cy+8], fill=color, width=2)
        elif comp_type == 1:
            # Capacitor (two lines)
            draw.line([cx-15, cy-20, cx-15, cy+20], fill=color, width=3)
            draw.line([cx+15, cy-20, cx+15, cy+20], fill=color, width=3)
            draw.line([cx-25, cy, cx+25, cy], fill=color, width=2)
        else:
            # Logic gate (triangle)
            draw.polygon([(cx, cy-15), (cx-15, cy+10), (cx+15, cy+10)], outline=color, width=2)
        
        # Connection trace to chip
        draw.line([center_x, center_y, cx, cy], fill=color, width=1)

def add_ambient_glow(img, center_x, center_y):
    """Add soft amber ambient glow radiating from chip center."""
    glow_layer = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(glow_layer)
    
    # Large soft gradient circles
    for radius in [400, 300, 200, 150]:
        alpha = int(255 * (1 - radius / 400) * 0.15)
        draw.ellipse(
            [center_x - radius, center_y - radius,
             center_x + radius, center_y + radius],
            fill=(AMBER[0], AMBER[1], AMBER[2], alpha)
        )
    
    # Apply blur for bloom effect
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=80))
    
    # Composite
    result = Image.alpha_composite(img.convert("RGBA"), glow_layer.convert("RGBA"))
    return result.convert("RGB")

def draw_text_layers(draw):
    """Draw all text elements."""
    # TOP-LEFT block
    # "EP. 11" - bold, large, amber
    font_ep = get_font(90, bold=True)
    draw.text((80, 60), "EP. 11", font=font_ep, fill=AMBER)
    
    # Horizontal rule below EP. 11
    draw.line([(80, 165), (680, 165)], fill=AMBER, width=2)
    
    # "OpenClaw Daily" - smaller, muted gray
    font_ocd = get_font(32, bold=True)
    draw.text((80, 180), "OpenClaw Daily", font=font_ocd, fill=MUTED_GRAY)
    
    # BOTTOM-LEFT block (lower 25%, left-aligned, 80px margin)
    # "OpenClaw Goes Hardware" - large bold white
    font_title1 = get_font(72, bold=True)
    draw.text((80, HEIGHT - 280), "OpenClaw Goes Hardware", font=font_title1, fill=WHITE)
    
    # "The Agent Layer Gets Real" - large bold amber
    font_title2 = get_font(72, bold=True)
    draw.text((80, HEIGHT - 190), "The Agent Layer Gets Real", font=font_title2, fill=AMBER)
    
    # Byline - small muted gray
    font_byline = get_font(28, bold=True)
    draw.text((80, HEIGHT - 110), "Nova & Alloy · OpenClaw Daily", font=font_byline, fill=DARK_GRAY)

def main():
    """Generate the podcast cover."""
    print("Generating Episode 11 cover...")
    
    # Create background
    img, draw = create_background()
    
    # Center of canvas
    center_x, center_y = WIDTH // 2, HEIGHT // 2 - 50
    
    # Draw CPU chip
    draw_cpu_chip(draw, center_x, center_y)
    
    # Draw circuit traces
    draw_circuit_traces(draw, center_x, center_y)
    
    # Draw component nodes
    draw_component_nodes(draw, center_x, center_y)
    
    # Add ambient glow
    img = add_ambient_glow(img, center_x, center_y)
    
    # Redraw on top after glow
    draw = ImageDraw.Draw(img)
    draw_cpu_chip(draw, center_x, center_y)
    draw_circuit_traces(draw, center_x, center_y)
    draw_component_nodes(draw, center_x, center_y)
    
    # Draw text
    draw_text_layers(draw)
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, "PNG", quality=95)
    
    # Verify
    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"File size: {file_size} bytes ({file_size/1024:.1f} KB)")
    
    # Load and check dimensions
    verify_img = Image.open(OUTPUT_PATH)
    print(f"Dimensions: {verify_img.size}")
    print(f"Mode: {verify_img.mode}")
    
    return file_size, verify_img.size

if __name__ == "__main__":
    file_size, dims = main()
