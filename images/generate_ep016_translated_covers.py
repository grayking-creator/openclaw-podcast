#!/usr/bin/env python3
"""Generate EP016 translated covers — same style as EP015, no colored borders."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random

BG        = (4,   7,  18)
GRID_COLOR= (30,  50,  90)
BLUE      = (40, 100, 230)
CYAN      = (61, 212, 247)
TEAL      = (0,  200, 180)
STEEL     = (170,190, 220)
WHITE     = (245,248, 255)
ORANGE    = (255,143,  64)

SIZE = 1400
OUTPUT_DIR = os.path.dirname(__file__)

LATIN_FONT      = "/System/Library/Fonts/HelveticaNeue.ttc"
DEVANAGARI_FONT = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"

# EP016: "OpenClaw Sheds Its Skin" — properly translated titles
TRANSLATIONS = {
    "en": ("EP. 016", "SHEDS ITS SKIN",          "The v2026.3.22 and v2026.3.23 double release deep dive"),
    "de": ("EP. 016", "HÄUTET SICH",             "Die Doppelveröffentlichung v2026.3.22 und v2026.3.23 im Detail"),
    "es": ("EP. 016", "MUDA DE PIEL",            "Análisis profundo de las versiones v2026.3.22 y v2026.3.23"),
    "pt": ("EP. 016", "TROCA DE PELE",           "Análise detalhada das versões v2026.3.22 e v2026.3.23"),
    "hi": ("EP. 016", "खाल उतारता है",            "v2026.3.22 और v2026.3.23 डबल रिलीज़ का गहन विश्लेषण"),
}

def get_font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def fit_font(draw, text, path, max_size, min_size, max_width):
    for size in range(max_size, min_size - 1, -2):
        f = get_font(path, size)
        box = draw.textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= max_width:
            return f
    return get_font(path, min_size)

def gradient_background(size):
    img = Image.new("RGBA", (size, size), (*BG, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    for x in range(0, size, 28):
        draw.line([(x,0),(x,size)], fill=(*GRID_COLOR, random.randint(12, 28)), width=1)
    for y in range(0, size, 28):
        draw.line([(0,y),(size,y)], fill=(*GRID_COLOR, random.randint(12, 28)), width=1)
    for _ in range(18):
        x = random.randint(0, size); y = random.randint(0, size)
        w = random.randint(60, 260); h = random.randint(40, 120)
        draw.line([(x,y),(x+w,y)], fill=(*CYAN, 22), width=1)
        draw.line([(x,y),(x,y+h)], fill=(*CYAN, 22), width=1)
    return img

def draw_concentric_rings(draw, center, size):
    cx, cy = center
    for i, r in enumerate(range(80, size//2, 55)):
        alpha = max(8, 55 - i*4)
        c = CYAN if i % 3 == 0 else (BLUE if i % 3 == 1 else TEAL)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(*c, alpha), width=2)

def add_dots(img, center, count=340):
    draw = ImageDraw.Draw(img, "RGBA")
    cx, cy = center
    size = img.width
    random.seed(42)
    for _ in range(count):
        angle = random.uniform(0, 2*math.pi)
        dist = random.uniform(0, size*0.48)
        x = int(cx + dist*math.cos(angle))
        y = int(cy + dist*math.sin(angle))
        r = random.choice([1,1,1,2,2,3])
        col = random.choice([(*CYAN,180),(*BLUE,160),(*TEAL,140),(*WHITE,120)])
        draw.ellipse([x-r,y-r,x+r,y+r], fill=col)

def draw_snake_icon(draw, center):
    """Snake shedding skin — fits EP016 theme."""
    cx, cy = center
    # Coiled snake body using arcs
    for i, r in enumerate([70, 55, 40]):
        offset = i * 12
        draw.arc([cx-r-offset, cy-r, cx+r-offset, cy+r], 180, 360, fill=(*TEAL, 200-i*40), width=6)
        draw.arc([cx-r+offset, cy-r+20, cx+r+offset, cy+r+20], 0, 180, fill=(*CYAN, 200-i*40), width=6)
    # Shed skin pieces (dashed fragments)
    for angle in range(0, 360, 40):
        rad = math.radians(angle)
        x1 = cx + int(100*math.cos(rad))
        y1 = cy + int(100*math.sin(rad))
        x2 = cx + int(130*math.cos(rad))
        y2 = cy + int(130*math.sin(rad))
        draw.line([x1,y1,x2,y2], fill=(*STEEL, 60), width=2)
    # Central eye
    draw.ellipse([cx-15, cy-15, cx+15, cy+15], fill=(*BLUE, 220))
    draw.ellipse([cx-6, cy-6, cx+6, cy+6], fill=ORANGE)

def draw_text(img, size, ep_label, main_title, subtitle_text, is_hi=False):
    draw = ImageDraw.Draw(img)
    fp = DEVANAGARI_FONT if is_hi else LATIN_FONT

    top_font     = get_font(LATIN_FONT, 42)
    heading_font = fit_font(draw, main_title, fp, 148 if not is_hi else 120, 72, 1080)
    subtitle_font= fit_font(draw, subtitle_text, fp, 52 if not is_hi else 38, 22, 1180)
    episode_font = get_font(LATIN_FONT, 72)

    top = "OPENCLAW DAILY"
    tb = draw.textbbox((0,0), top, font=top_font)
    draw.text(((size-(tb[2]-tb[0]))//2, 52), top, font=top_font, fill=(*STEEL, 255))

    mb = draw.textbbox((0,0), main_title, font=heading_font)
    mx = (size-(mb[2]-mb[0]))//2
    my = size//2 + 120
    draw.text((mx, my), main_title, font=heading_font, fill=WHITE)

    sb = draw.textbbox((0,0), subtitle_text, font=subtitle_font)
    sx = (size-(sb[2]-sb[0]))//2
    sy = my + 185
    draw.text((sx, sy), subtitle_text, font=subtitle_font, fill=(*CYAN, 255))

    eb = draw.textbbox((0,0), ep_label, font=episode_font)
    draw.text((size-(eb[2]-eb[0])-52, size-86), ep_label, font=episode_font, fill=(*ORANGE, 255))

def make_cover(locale, ep_label, main_title, subtitle_text):
    random.seed(hash(locale) % 9999)
    img = gradient_background(SIZE)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_concentric_rings(draw, (SIZE//2, SIZE//2+20), SIZE)
    add_dots(img, (SIZE//2, SIZE//2+20), count=340)
    draw_snake_icon(draw, (SIZE//2, SIZE//2+20))

    vignette = Image.new("RGBA", (SIZE,SIZE),(0,0,0,0))
    vd = ImageDraw.Draw(vignette)
    for r in range(SIZE, 0, -6):
        alpha = int(190*(1-r/SIZE)**1.7)
        vd.ellipse([SIZE//2-r//2,SIZE//2-r//2,SIZE//2+r//2,SIZE//2+r//2],
                   outline=(0,0,0,alpha), width=6)
    vignette = vignette.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img, vignette)

    draw_text(img, SIZE, ep_label, main_title, subtitle_text, is_hi=(locale=="hi"))
    img = img.convert("RGB")
    out = f"{OUTPUT_DIR}/episode_016_cover_{locale}.png"
    img.save(out)
    print(f"✅ {locale}: {out}")
    return out

if __name__ == "__main__":
    for locale, (ep, title, subtitle) in TRANSLATIONS.items():
        make_cover(locale, ep, title, subtitle)
