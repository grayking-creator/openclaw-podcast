"""
EP022 translated covers — DE/ES/PT/HI
Same visual as EN (perspective rails + release tags) with translated title text.
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random, math, shutil

W, H = 1400, 1400
BASE_IMG = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_022_cover.png"

BLACK       = (2, 3, 8)
DARK_BG     = (4, 6, 16)
CYAN        = (0, 195, 225)
CYAN_BRIGHT = (60, 235, 255)
CYAN_GLOW   = (110, 245, 255)
AMBER       = (210, 140, 20)
AMBER_BRIGHT= (245, 170, 45)
WHITE       = (242, 246, 252)
DIM_WHITE   = (150, 168, 192)

def blur_overlay(img, draw_fn, blur=18):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld)
    return layer.filter(ImageFilter.GaussianBlur(blur))

def make_cover(lang, line1, line2, tagline, out_path, use_devanagari=False):
    img = Image.open(BASE_IMG).convert("RGBA")

    try:
        font_show  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
        font_ep    = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 68)
        font_sub   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
        if use_devanagari:
            try:
                font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/ITFDevanagari.ttc", 98)
                font_title2 = font_title
            except:
                try:
                    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/DevanagariMT.ttc", 98)
                    font_title2 = font_title
                except:
                    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 98)
                    font_title2 = font_title
        else:
            font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 108)
            font_title2 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 108)
    except:
        font_show = font_ep = font_title = font_title2 = font_sub = ImageFont.load_default()

    # Paint over the existing title area with a dark plate
    plate = blur_overlay(img,
        lambda ld: ld.polygon(
            [(30, 990), (1370, 990), (1400, 1400), (0, 1400)],
            fill=(0, 0, 0, 210)
        ),
        blur=25
    )
    img = Image.alpha_composite(img, plate)

    md = ImageDraw.Draw(img)

    SHOW_TEXT = "OPENCLAW DAILY"
    EP_TEXT   = "EP022"

    sw = md.textlength(SHOW_TEXT, font=font_show)
    ew = md.textlength(EP_TEXT,   font=font_ep)

    # Show name
    md.text(((W - sw) / 2, 60), SHOW_TEXT, font=font_show, fill=(185, 200, 222, 220))

    # EP number cyan glow
    for blur_amt, alpha in ((18, 90), (32, 45)):
        eg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        egd = ImageDraw.Draw(eg)
        egd.text(((W - ew) / 2, 118), EP_TEXT, font=font_ep, fill=CYAN + (alpha,))
        eg = eg.filter(ImageFilter.GaussianBlur(blur_amt))
        img = Image.alpha_composite(img, eg)
    md = ImageDraw.Draw(img)
    md.text(((W - ew) / 2, 118), EP_TEXT, font=font_ep, fill=CYAN_GLOW + (255,))

    # Title line 1
    l1w = md.textlength(line1, font=font_title)
    # shadow
    md.text(((W - l1w) / 2 + 3, 1013), line1, font=font_title, fill=(0, 0, 0, 180))
    tg1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tg1d = ImageDraw.Draw(tg1)
    tg1d.text(((W - l1w) / 2, 1010), line1, font=font_title, fill=AMBER + (55,))
    tg1 = tg1.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img, tg1)
    md = ImageDraw.Draw(img)
    md.text(((W - l1w) / 2, 1010), line1, font=font_title, fill=WHITE + (255,))

    # Title line 2 — amber
    l2w = md.textlength(line2, font=font_title2)
    # auto-shrink if too wide
    f2 = font_title2
    sz = 108
    while l2w > W - 80 and sz > 60:
        sz -= 6
        try:
            f2 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", sz) if not use_devanagari else f2
        except:
            pass
        l2w = md.textlength(line2, font=f2)

    md.text(((W - l2w) / 2 + 4, 1143), line2, font=f2, fill=(0, 0, 0, 180))
    tg2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tg2d = ImageDraw.Draw(tg2)
    tg2d.text(((W - l2w) / 2, 1140), line2, font=f2, fill=AMBER + (70,))
    tg2 = tg2.filter(ImageFilter.GaussianBlur(16))
    img = Image.alpha_composite(img, tg2)
    md = ImageDraw.Draw(img)
    md.text(((W - l2w) / 2, 1140), line2, font=f2, fill=AMBER_BRIGHT + (255,))

    # Tagline below title block — avoid collision with the main title
    tw2 = md.textlength(tagline, font=font_sub)
    md.text(((W - tw2) / 2, 1288), tagline, font=font_sub, fill=CYAN_BRIGHT + (120,))

    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=145, threshold=2))
    img.convert("RGB").save(out_path, "PNG")
    print(f"Saved: {out_path}")

BASE = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images"
WEB  = "/Users/tobyglennpeters/.openclaw/workspace/websiteBuilder/frontend/public/images/podcast"

# DE — Die Release-Lokomotive
make_cover("de",
    line1="DIE",
    line2="RELEASE-LOKOMOTIVE",
    tagline="FÜNF GESCHICHTEN. EIN GLEIS.",
    out_path=f"{BASE}/episode_022_cover_de.png"
)

# ES — El Tren de Lanzamientos
make_cover("es",
    line1="EL TREN DE",
    line2="LANZAMIENTOS",
    tagline="CINCO HISTORIAS. UNA VÍA.",
    out_path=f"{BASE}/episode_022_cover_es.png"
)

# PT — O Trem dos Lançamentos
make_cover("pt",
    line1="O TREM DOS",
    line2="LANÇAMENTOS",
    tagline="CINCO HISTÓRIAS. UM TRILHO.",
    out_path=f"{BASE}/episode_022_cover_pt.png"
)

# HI — रिलीज़ ट्रेन
make_cover("hi",
    line1="रिलीज़",
    line2="ट्रेन",
    tagline="FIVE STORIES. ONE TRACK.",
    out_path=f"{BASE}/episode_022_cover_hi.png",
    use_devanagari=True
)

# Copy all to website
import shutil
for lang in ["de", "es", "pt", "hi"]:
    src = f"{BASE}/episode_022_cover_{lang}.png"
    dst = f"{WEB}/episode_022_cover_{lang}.png"
    shutil.copy(src, dst)
    print(f"Copied to website: {dst}")
