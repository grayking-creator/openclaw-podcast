#!/usr/bin/env python3
"""Generate episode 11 cover art for OpenClaw Daily podcast."""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Configuration
SIZE = 1400
BACKGROUND_COLOR = (10, 14, 26)  # #0A0E1A

# Node colors
NODE_COLORS = [
    (245, 168, 112),   # peach/coral #F5A870
    (213, 128, 240),   # lavender #D580F0
    (64, 216, 240),    # cyan #40D8F0
    (112, 240, 192),   # mint #70F0C0
    (240, 224, 96),    # yellow #F0E060
    (0, 224, 240),     # bright cyan center #00E0F0
]

# Node positions (relative to image size)
NODE_POSITIONS = [
    (0.5, 0.45),      # center
    (0.65, 0.30),     # top right
    (0.35, 0.32),     # top left  
    (0.28, 0.55),     # lower left
    (0.72, 0.55),     # lower right
    (0.82, 0.40),     # right
]

# Connections between nodes (indices)
CONNECTIONS = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),  # center to all
    (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),  # outer ring
]

def create_background(size):
    """Create background with grid and stars."""
    img = Image.new('RGB', (size, size), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Grid pattern - lines every ~70px
    grid_spacing = 70
    grid_color = (40, 50, 80, 25)  # Very low opacity
    
    for i in range(0, size + 1, grid_spacing):
        draw.line([(i, 0), (i, size)], fill=grid_color, width=1)
        draw.line([(0, i), (size, i)], fill=grid_color, width=1)
    
    # Scattered star dots
    random.seed(42)
    star_colors = [
        (255, 255, 255),
        (64, 216, 240),
        (213, 128, 240),
        (240, 224, 96),
        (245, 168, 112),
        (180, 100, 255),
    ]
    
    for _ in range(300):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        color = random.choice(star_colors)
        radius = random.randint(1, 3)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
    
    return img

def create_glow_layer(size, color, intensity=30):
    """Create a blurred glow layer for an orb."""
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse([size//2 - intensity, size//2 - intensity, 
                  size//2 + intensity, size//2 + intensity], 
                 fill=(*color, 150))
    return glow.filter(ImageFilter.GaussianBlur(intensity // 2))

def draw_node(draw, x, y, radius, color):
    """Draw a glowing node orb."""
    # Outer glow
    glow_radius = int(radius * 2.5)
    glow_img = Image.new('RGBA', (glow_radius * 2, glow_radius * 2), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.ellipse([0, 0, glow_radius * 2, glow_radius * 2], fill=(*color, 60))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(glow_radius // 2))
    
    # Main orb with gradient effect (simulated)
    # Draw outer darker ring
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], 
                 fill=(*color, 180))
    
    # Inner bright core
    inner_radius = int(radius * 0.7)
    draw.ellipse([x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius], 
                 fill=color)
    
    # Specular highlight
    highlight_offset = int(radius * 0.3)
    highlight_radius = int(radius * 0.25)
    draw.ellipse([x - highlight_offset - highlight_radius, 
                  y - highlight_offset - highlight_radius,
                  x - highlight_offset + highlight_radius, 
                  y - highlight_offset + highlight_radius], 
                 fill=(255, 255, 255, 200))
    
    return glow_img

def draw_connection(draw, x1, y1, x2, y2, color1, color2):
    """Draw a glowing line between two nodes."""
    # Calculate midpoint for gradient
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    
    # Draw glow layer (wider, blurred line)
    # Main line
    draw.line([(x1, y1), (x2, y2)], fill=color1, width=4)

def draw_wavy_lines(img, size):
    """Draw wavy cyan lines in lower third."""
    draw = ImageDraw.Draw(img)
    
    base_y = int(size * 0.65)
    amplitudes = [25, 20, 30, 18]
    frequencies = [0.008, 0.012, 0.006, 0.015]
    offsets = [0, 40, 80, 120]
    
    for amp, freq, offset in zip(amplitudes, frequencies, offsets):
        points = []
        for x in range(0, size + 10, 10):
            y = base_y + offset + amp * math.sin(freq * x)
            points.append((x, y))
        
        # Draw glow
        for i in range(3):
            glow_draw = ImageDraw.Draw(Image.new('RGBA', (size, size), (0,0,0,0)))
            glow_points = [(p[0], p[1] + i*2) for p in points]
            # Simple approach: draw multiple lines with offset
            draw.line(points, fill=(64, 216, 240, 30), width=6)
        
        # Main line
        draw.line(points, fill=(64, 216, 240, 180), width=2)

def draw_text(img, size):
    """Draw text elements."""
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay-Bold.ttf", 120)
        font_subtitle = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay-Regular.ttf", 45)
        font_small = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay-Regular.ttf", 28)
    except:
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
            font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        except:
            font_large = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # EP. 11 - upper area
    ep_text = "EP. 11"
    # Get text bbox
    bbox = draw.textbbox((0, 0), ep_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = 80
    
    # Draw glow effect for EP text
    for offset in range(3, 8):
        glow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        glow_draw.text((x, y), ep_text, font=font_large, fill=(255, 255, 255, 40))
        glow_img = glow_img.filter(ImageFilter.GaussianBlur(offset))
        img.paste(glow_img, (0, 0), glow_img)
    
    # Main EP text
    draw.text((x, y), ep_text, font=font_large, fill=(255, 255, 255))
    
    # Subtitle - The Agent Layer Gets Real
    subtitle = "The Agent Layer Gets Real"
    bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    sub_width = bbox[2] - bbox[0]
    sub_x = (size - sub_width) // 2
    sub_y = y + text_height + 15
    
    draw.text((sub_x, sub_y), subtitle, font=font_subtitle, fill=(64, 216, 240))
    
    # Show name - OpenClaw Daily at bottom
    show_name = "OpenClaw Daily"
    bbox = draw.textbbox((0, 0), show_name, font=font_small)
    name_width = bbox[2] - bbox[0]
    name_x = (size - name_width) // 2
    name_y = size - 60
    
    draw.text((name_x, name_y), show_name, font=font_small, fill=(160, 180, 200))

def main():
    print("Creating episode 11 cover art...")
    
    # Create background
    img = create_background(SIZE)
    draw = ImageDraw.Draw(img)
    
    # Convert node positions to pixels
    node_pixels = [(int(x * SIZE), int(y * SIZE)) for x, y in NODE_POSITIONS]
    
    # Draw connections first (behind nodes)
    for i, j in CONNECTIONS:
        x1, y1 = node_pixels[i]
        x2, y2 = node_pixels[j]
        color1 = NODE_COLORS[i]
        color2 = NODE_COLORS[j]
        
        # Glow line
        for width in [12, 8, 4]:
            alpha = 20 if width > 4 else 80
            draw.line([(x1, y1), (x2, y2)], fill=(*color1, alpha), width=width)
        
        # Main line
        draw.line([(x1, y1), (x2, y2)], fill=color1, width=3)
    
    # Draw nodes with glow
    # Create a separate layer for node glows
    glow_layer = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    
    for (x, y), color in zip(node_pixels, NODE_COLORS):
        radius = 45
        
        # Draw outer glow on glow layer
        glow_radius = radius * 3
        glow_img = Image.new('RGBA', (glow_radius * 2, glow_radius * 2), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        glow_draw.ellipse([0, 0, glow_radius * 2, glow_radius * 2], fill=(*color, 40))
        glow_img = glow_img.filter(ImageFilter.GaussianBlur(glow_radius // 2))
        
        # Paste glow at position
        paste_x = x - glow_radius
        paste_y = y - glow_radius
        glow_layer.paste(glow_img, (paste_x, paste_y), glow_img)
    
    # Composite glow layer
    img.paste(glow_layer, (0, 0), glow_layer)
    
    # Draw actual nodes on top
    for (x, y), color in zip(node_pixels, NODE_COLORS):
        radius = 45
        
        # Outer ring (darker)
        draw.ellipse([x - radius - 3, y - radius - 3, x + radius + 3, y + radius + 3], 
                     fill=(*color, 150))
        
        # Main orb
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
        
        # Inner highlight
        inner_radius = int(radius * 0.6)
        highlight_color = tuple(min(255, c + 40) for c in color)
        draw.ellipse([x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius], 
                     fill=highlight_color)
        
        # Specular highlight
        highlight_x = x - int(radius * 0.25)
        highlight_y = y - int(radius * 0.25)
        highlight_r = int(radius * 0.2)
        draw.ellipse([highlight_x - highlight_r, highlight_y - highlight_r,
                      highlight_x + highlight_r, highlight_y + highlight_r], 
                     fill=(255, 255, 255, 220))
    
    # Draw wavy lines
    draw_wavy_lines(img, SIZE)
    
    # Draw text
    draw_text(img, SIZE)
    
    # Save
    output_path = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_011_cover.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Saved to {output_path}")
    
    # Verify
    import os
    file_size = os.path.getsize(output_path)
    print(f"File size: {file_size} bytes ({file_size / 1024:.1f} KB)")
    print(f"Dimensions: {img.size}")

if __name__ == "__main__":
    main()
