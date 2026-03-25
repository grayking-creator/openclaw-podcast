#!/usr/bin/env python3
"""Generate EP000 translated covers (same pipeline as EP015)."""
from __future__ import annotations
import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG         = (4,   7,  18)
GRID_COLOR = (30,  50,  90)
BLUE       = (40, 100, 230)
CYAN       = (61, 212, 247)
TEAL       = (0,  200, 180)
STEEL      = (170,190, 220)
WHITE      = (245,248, 255)
ORANGE     = (255,143,  64)

SIZE       = 1400
OUTPUT_DIR = os.path.dirname(__file__)

LATIN_FONT      = "/System/Library/Fonts/HelveticaNeue.ttc"
DEVANAGARI_FONT = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"

TRANSLATIONS = {
    "de": ("EP. 000", "HARDWARE-ANALYSE",      "Wie wir lokale KI-Modellfehler behoben haben"),
    "es": ("EP. 000", "ANÁLISIS DE HARDWARE",  "Cómo solucionamos los fallos del modelo de IA local"),
    "pt": ("EP. 000", "ANÁLISE DE HARDWARE",   "Como corrigimos falhas no modelo de IA local"),
    "hi": ("EP. 000", "हार्डवेयर विश्लेषण",    "हमने लोकल AI मॉडल की विफलताएं कैसे ठीक कीं"),
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
        draw.line([(x,0),(x,size)], fill=(*GRID_COLOR, random.randint(12,28)), width=1)
    for y in range(0, size, 28):
        draw.line([(0,y),(size,y)], fill=(*GRID_COLOR, random.randint(12,28)), width=1)
    for _ in range(18):
        x=random.randint(0,size); y=random.randint(0,size)
        w=random.randint(60,260); h=random.randint(40,120)
        draw.line([(x,y),(x+w,y)], fill=(*CYAN, 22), width=1)
        draw.line([(x,y),(x,y+h)], fill=(*CYAN, 22), width=1)
    return img

def draw_concentric_rings(draw, center, size):
    cx, cy = center
    for i, r in enumerate(range(80, size//2, 55)):
        alpha = max(8, 55 - i*4)
        c = CYAN if i%3==0 else (BLUE if i%3==1 else TEAL)
        draw.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(*c, alpha), width=2)

def add_dots(img, center, count=340):
    draw = ImageDraw.Draw(img, "RGBA")
    cx, cy = center
    size = img.width
    random.seed(42)
    for _ in range(count):
        angle = random.uniform(0, 2*math.pi)
        dist  = random.uniform(0, size*0.48)
        x = int(cx + dist*math.cos(angle))
        y = int(cy + dist*math.sin(angle))
        r = random.choice([1,1,1,2,2,3])
        col = random.choice([(*CYAN,180),(*BLUE,160),(*TEAL,140),(*WHITE,120)])
        draw.ellipse([x-r,y-r,x+r,y+r], fill=col)

def draw_chip_icon(draw, center):
    """CPU/chip icon — fits EP000 hardware theme."""
    cx, cy = center
    draw.rectangle([cx-80,cy-80,cx+80,cy+80], fill=(*BLUE,200), outline=(*CYAN,180), width=3)
    for off in [-40, 0, 40]:
        draw.rectangle([cx+off-10, cy-80-20, cx+off+10, cy-80], fill=(*CYAN,200))
        draw.rectangle([cx+off-10, cy+80,    cx+off+10, cy+80+20], fill=(*CYAN,200))
        draw.rectangle([cx-80-20, cy+off-10, cx-80, cy+off+10], fill=(*CYAN,200))
        draw.rectangle([cx+80,    cy+off-10, cx+80+20, cy+off+10], fill=(*CYAN,200))
    draw.rectangle([cx-50,cy-50,cx+50,cy+50], outline=(*TEAL,160), width=2)
    for r in [10, 20, 30]:
        draw.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(*WHITE,40), width=1)
    draw.ellipse([cx-12,cy-12,cx+12,cy+12], fill=ORANGE)

def draw_text(img, size, ep_label, main_title, subtitle_text, is_hi=False):
    draw = ImageDraw.Draw(img)
    fp = DEVANAGARI_FONT if is_hi else LATIN_FONT

    top_font     = get_font(LATIN_FONT, 42)
    heading_font = fit_font(draw, main_title, fp, 110 if not is_hi else 90, 60, 1080)
    subtitle_font= fit_font(draw, subtitle_text, fp, 48 if not is_hi else 36, 20, 1180)
    episode_font = get_font(LATIN_FONT, 72)

    top = "OPENCLAW DAILY"
    tb  = draw.textbbox((0,0), top, font=top_font)
    draw.text(((size-(tb[2]-tb[0]))//2, 52), top, font=top_font, fill=(*STEEL,255))

    mb = draw.textbbox((0,0), main_title, font=heading_font)
    mx = (size-(mb[2]-mb[0]))//2
    my = size//2 + 120
    draw.text((mx, my), main_title, font=heading_font, fill=WHITE)

    sb = draw.textbbox((0,0), subtitle_text, font=subtitle_font)
    sx = (size-(sb[2]-sb[0]))//2
    sy = my + 175
    draw.text((sx, sy), subtitle_text, font=subtitle_font, fill=(*CYAN,255))

    eb = draw.textbbox((0,0), ep_label, font=episode_font)
    draw.text((size-(eb[2]-eb[0])-52, size-86), ep_label, font=episode_font, fill=(*ORANGE,255))

def make_cover(locale, ep_label, main_title, subtitle_text):
    random.seed(hash(locale) % 9999)
    img = gradient_background(SIZE)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_concentric_rings(draw, (SIZE//2, SIZE//2+20), SIZE)
    add_dots(img, (SIZE//2, SIZE//2+20), count=340)
    draw_chip_icon(draw, (SIZE//2, SIZE//2+20))

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
    out = f"{OUTPUT_DIR}/episode_000_cover_{locale}.png"
    img.save(out)
    print(f"✅ {locale}: {out}")
    return out

def main():
    for locale, (ep, title, subtitle) in TRANSLATIONS.items():
        make_cover(locale, ep, title, subtitle)

if __name__ == "__main__":
    main()
