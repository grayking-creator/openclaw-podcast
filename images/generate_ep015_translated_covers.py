#!/usr/bin/env python3
"""Generate EP015 translated covers by running the full EN generator with swapped text."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random

# ── palette (same as EN cover) ──────────────────────────────────────────────
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

TRANSLATIONS = {
    "de": ("EP. 015", "ERINNER DICH",    "Wie wir ein echtes KI-Gedächtnissystem gebaut haben"),
    "es": ("EP. 015", "RECUÉRDAME",      "Cómo construimos un sistema de memoria real para IA"),
    "pt": ("EP. 015", "LEMBRA DE MIM",   "Como construímos um sistema de memória real para IA"),
    "hi": ("EP. 015", "मुझे याद करो",    "हमने AI के लिए एक असली मेमोरी सिस्टम कैसे बनाया"),
}

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def fit_font(draw, text, path, max_size, min_size, max_width):
    for size in range(max_size, min_size - 1, -2):
        f = get_font(path, size)
        box = draw.textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= max_width:
            return f
    return get_font(path, min_size)

# ── background (identical to EN) ─────────────────────────────────────────────
def gradient_background(size):
    img = Image.new("RGBA", (size, size), (*BG, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    for x in range(0, size, 28):
        alpha = random.randint(12, 28)
        draw.line([(x,0),(x,size)], fill=(*GRID_COLOR, alpha), width=1)
    for y in range(0, size, 28):
        alpha = random.randint(12, 28)
        draw.line([(0,y),(size,y)], fill=(*GRID_COLOR, alpha), width=1)
    for _ in range(18):
        x = random.randint(0, size); y = random.randint(0, size)
        w = random.randint(60, 260); h = random.randint(40, 120)
        draw.line([(x,y),(x+w,y)], fill=(*CYAN, 22), width=1)
        draw.line([(x,y),(x,y+h)], fill=(*CYAN, 22), width=1)
    return img

def draw_grid(draw, size):
    pass  # already in gradient_background

def draw_concentric_memory_rings(draw, center, size):
    cx, cy = center
    for i, r in enumerate(range(80, size//2, 55)):
        alpha = max(8, 55 - i*4)
        c = CYAN if i % 3 == 0 else (BLUE if i % 3 == 1 else TEAL)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(*c, alpha), width=2)

def add_vector_dots(img, center, count=340):
    draw = ImageDraw.Draw(img, "RGBA")
    cx, cy = center
    size = img.width
    random.seed(42)
    for _ in range(count):
        angle = random.uniform(0, 2*math.pi)
        dist  = random.uniform(0, size*0.48)
        x = int(cx + dist * math.cos(angle))
        y = int(cy + dist * math.sin(angle))
        r = random.choice([1,1,1,2,2,3])
        col = random.choice([(*CYAN,180),(*BLUE,160),(*TEAL,140),(*WHITE,120)])
        draw.ellipse([x-r,y-r,x+r,y+r], fill=col)

def draw_brain_icon(draw, center):
    cx, cy = center
    draw.ellipse([cx-90,cy-90,cx+90,cy+90], fill=(*BLUE,220))
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1,y1 = cx+int(95*math.cos(rad)), cy+int(95*math.sin(rad))
        x2,y2 = cx+int(135*math.cos(rad)),cy+int(135*math.sin(rad))
        alpha = 70+int(50*abs(math.sin(rad)))
        draw.line([x1,y1,x2,y2], fill=(*CYAN,alpha), width=2)
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        x,y = cx+int(140*math.cos(rad)),cy+int(140*math.sin(rad))
        draw.ellipse([x-9,y-9,x+9,y+9], fill=(*CYAN,38), outline=(0,0,0,0))
        draw.ellipse([x-6,y-6,x+6,y+6], fill=ORANGE)
    pr_x, pr_y = cx-10, cy+5
    draw.arc([pr_x-34,pr_y-28,pr_x+26,pr_y+42],180,0,fill=(*TEAL,190),width=4)
    draw.line([(pr_x-24,pr_y+8),(pr_x+10,pr_y+8)],fill=(*TEAL,190),width=4)
    draw.ellipse([pr_x-6,pr_y-6,pr_x+6,pr_y+6],fill=CYAN)

def draw_text(img, size, ep_label, main_title, subtitle_text, is_hi=False):
    draw = ImageDraw.Draw(img)
    fp_latin = LATIN_FONT
    fp = DEVANAGARI_FONT if is_hi else fp_latin

    top_font    = get_font(fp_latin, 42)
    heading_font= fit_font(draw, main_title, fp, 148 if not is_hi else 120, 72, 1080)
    subtitle_font= fit_font(draw, subtitle_text, fp, 52 if not is_hi else 38, 22, 1180)
    episode_font= get_font(fp_latin, 72)

    top = "OPENCLAW DAILY"
    tb  = draw.textbbox((0,0), top, font=top_font)
    tx  = (size-(tb[2]-tb[0]))//2
    ty  = 52
    draw.text((tx,ty), top, font=top_font, fill=(*STEEL,255))

    mb = draw.textbbox((0,0), main_title, font=heading_font)
    mx = (size-(mb[2]-mb[0]))//2 + (18 if not is_hi else 0)
    my = size//2 + 120
    draw.text((mx,my), main_title, font=heading_font, fill=WHITE)

    sb = draw.textbbox((0,0), subtitle_text, font=subtitle_font)
    sx = (size-(sb[2]-sb[0]))//2 + (10 if not is_hi else 0)
    sy = my + 185
    draw.text((sx,sy), subtitle_text, font=subtitle_font, fill=(*CYAN,255))

    eb = draw.textbbox((0,0), ep_label, font=episode_font)
    ew = eb[2]-eb[0]
    ex = size-ew-52
    ey = size-86
    draw.text((ex,ey), ep_label, font=episode_font, fill=(*ORANGE,255))

def make_cover(locale, ep_label, main_title, subtitle_text):
    random.seed(locale.__hash__() % 9999)
    img = gradient_background(SIZE)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_concentric_memory_rings(draw, (SIZE//2, SIZE//2+20), SIZE)
    add_vector_dots(img, (SIZE//2, SIZE//2+20), count=340)
    draw_brain_icon(draw, (SIZE//2, SIZE//2+20))

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
    out = f"{OUTPUT_DIR}/episode_015_cover_{locale}.png"
    img.save(out)
    print(f"✅ {locale}: {out}")
    return out

def main():
    for locale, (ep, title, subtitle) in TRANSLATIONS.items():
        make_cover(locale, ep, title, subtitle)

if __name__ == "__main__":
    main()
