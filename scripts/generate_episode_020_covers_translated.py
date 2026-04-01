from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, random, os

W, H = 1400, 1400
BASE = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images"

BLACK        = (2, 2, 4)
TOP_BG       = (4, 6, 10)
BOT_BG       = (8, 4, 2)
AMBER        = (200, 110, 20)
AMBER_BRIGHT = (255, 165, 50)
AMBER_GLOW   = (255, 200, 100)
ORANGE_HOT   = (255, 130, 30)
STEEL        = (50, 55, 60)
WHITE        = (248, 246, 240)

TRANSLATIONS = [
    {
        "lang": "de",
        "LINE1": "DIE INFRASTRUCTURE",
        "LINE2": "RELEASE",
        "tag": "WENN EIN TOOL ZUR INFRASTRUKTUR WIRD",
    },
    {
        "lang": "es",
        "LINE1": "EL LANZAMIENTO DE",
        "LINE2": "LA INFRAESTRUCTURA",
        "tag": "CUANDO UNA HERRAMIENTA SE CONVIERTE EN INFRAESTRUCTURA",
    },
    {
        "lang": "pt",
        "LINE1": "O LANÇAMENTO DA",
        "LINE2": "INFRAESTRUTURA",
        "tag": "QUANDO UMA FERRAMENTA VIRA INFRAESTRUTURA",
    },
    {
        "lang": "hi",
        "LINE1": "इन्फ्रास्ट्रक्चर",
        "LINE2": "रिलीज़",
        "tag": "जब एक टूल इन्फ्रास्ट्रक्चर बन जाता है",
        "hindi": True,
    },
]

def build_cover(LINE1, LINE2, tag, out_path, hindi=False):
    img = Image.new("RGBA", (W, H), BLACK + (255,))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        r = int(TOP_BG[0] * (1 - t) + BOT_BG[0] * t)
        g = int(TOP_BG[1] * (1 - t) + BOT_BG[1] * t)
        b = int(TOP_BG[2] * (1 - t) + BOT_BG[2] * t)
        d.line([(0, y), (W, y)], fill=(r, g, b, 255))

    def blur_overlay(draw_fn, blur=18):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        draw_fn(ld)
        return layer.filter(ImageFilter.GaussianBlur(blur))

    core = blur_overlay(
        lambda ld: ld.ellipse([(350, 350), (1050, 1050)], fill=AMBER + (40,)), blur=160)
    img = Image.alpha_composite(img, core)

    # Grid
    trace_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(trace_layer)
    for ty in [220, 380, 540, 700, 860, 1020]:
        td.line([(80, ty), (1320, ty)], fill=STEEL + (45,), width=1)
    for tx in [240, 460, 700, 940, 1160]:
        td.line([(tx, 80), (tx, 1320)], fill=STEEL + (35,), width=1)
    trace_layer = trace_layer.filter(ImageFilter.GaussianBlur(0.4))
    img = Image.alpha_composite(img, trace_layer)

    # Nodes
    node_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(node_layer)
    random.seed(7)
    for ty in [220, 380, 540, 700, 860, 1020]:
        for tx in [240, 460, 700, 940, 1160]:
            if random.random() > 0.35:
                sz = random.choice([4, 5, 6])
                nd.rectangle([(tx - sz, ty - sz), (tx + sz, ty + sz)],
                              fill=AMBER + (random.randint(60, 130),),
                              outline=AMBER_BRIGHT + (80,), width=1)
    node_layer = node_layer.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img, node_layer)

    # Hex rings
    cx, cy = 700, 600
    def draw_hex_ring(cx, cy, r, color, alpha, width, blur_amt):
        pts = [(cx + r * math.cos(math.radians(60 * i - 30)),
                cy + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.polygon(pts, outline=color + (alpha,), width=width)
        return layer.filter(ImageFilter.GaussianBlur(blur_amt))

    for ring_r, ring_alpha, ring_blur in [(320, 30, 30), (260, 50, 20), (210, 65, 12)]:
        img = Image.alpha_composite(img, draw_hex_ring(cx, cy, ring_r, AMBER, ring_alpha, 4, ring_blur))
    for ring_r, ring_alpha, ring_blur, ring_w in [(320, 160, 3, 3), (260, 200, 2, 3), (210, 220, 1.5, 4)]:
        img = Image.alpha_composite(img, draw_hex_ring(cx, cy, ring_r, AMBER_BRIGHT, ring_alpha, ring_w, ring_blur))

    pts_center = [(cx + 160 * math.cos(math.radians(60 * i - 30)),
                   cy + 160 * math.sin(math.radians(60 * i - 30))) for i in range(6)]
    cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cld = ImageDraw.Draw(cl)
    cld.polygon(pts_center, fill=(30, 20, 8, 200), outline=AMBER_GLOW + (220,), width=3)
    img = Image.alpha_composite(img, cl.filter(ImageFilter.GaussianBlur(1.5)))

    inner_glow = blur_overlay(lambda ld: ld.ellipse([(cx-100,cy-100),(cx+100,cy+100)], fill=ORANGE_HOT+(80,)), blur=40)
    img = Image.alpha_composite(img, inner_glow)

    slash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sld = ImageDraw.Draw(slash)
    for ox in [-36, 0, 36]:
        sld.line([(cx+ox-30, cy-90), (cx+ox+30, cy+90)], fill=AMBER_GLOW+(230,), width=7)
    img = Image.alpha_composite(img, slash.filter(ImageFilter.GaussianBlur(2)))

    # Fonts
    try:
        font_show  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
        font_ep    = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 68)
        font_sub   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
        if hindi:
            for fname in ["/System/Library/Fonts/Supplemental/ITFDevanagari.ttc",
                          "/System/Library/Fonts/Supplemental/DevanagariMT.ttc"]:
                if os.path.exists(fname):
                    font_title = ImageFont.truetype(fname, 108)
                    break
            else:
                font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 108)
        else:
            font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 108)
    except Exception:
        font_show = font_ep = font_title = font_sub = ImageFont.load_default()

    md = ImageDraw.Draw(img)
    SHOW_TEXT = "OPENCLAW DAILY"
    EP_TEXT   = "EP020"

    sw  = md.textlength(SHOW_TEXT, font=font_show)
    ew  = md.textlength(EP_TEXT, font=font_ep)

    md.text(((W - sw) / 2, 62), SHOW_TEXT, font=font_show, fill=(210, 205, 195, 235))

    for blur_amt, alpha in ((16, 110), (30, 55)):
        eg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        egd = ImageDraw.Draw(eg)
        egd.text(((W - ew) / 2, 120), EP_TEXT, font=font_ep, fill=AMBER + (alpha,))
        img = Image.alpha_composite(img, eg.filter(ImageFilter.GaussianBlur(blur_amt)))
    md = ImageDraw.Draw(img)
    md.text(((W - ew) / 2, 120), EP_TEXT, font=font_ep, fill=AMBER_GLOW + (255,))

    plate = blur_overlay(lambda ld: ld.polygon(
        [(80, 1010), (1320, 1010), (1380, 1400), (20, 1400)], fill=(0, 0, 0, 170)), blur=28)
    img = Image.alpha_composite(img, plate)
    md = ImageDraw.Draw(img)

    l1w = md.textlength(LINE1, font=font_title)
    l2w = md.textlength(LINE2, font=font_title)

    for text, y, tw in ((LINE1, 1050, l1w), (LINE2, 1176, l2w)):
        md.text(((W - tw) / 2 + 4, y + 4), text, font=font_title, fill=(0, 0, 0, 200))
        tg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tgd = ImageDraw.Draw(tg)
        tgd.text(((W - tw) / 2, y), text, font=font_title, fill=ORANGE_HOT + (70,))
        img = Image.alpha_composite(img, tg.filter(ImageFilter.GaussianBlur(14)))
        md = ImageDraw.Draw(img)
        md.text(((W - tw) / 2, y), text, font=font_title, fill=WHITE + (255,))

    tw2 = md.textlength(tag, font=font_sub)
    if tw2 > W - 80:
        font_sub2 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
        tw2 = md.textlength(tag, font=font_sub2)
        md.text(((W - tw2) / 2, 1162), tag, font=font_sub2, fill=AMBER_BRIGHT + (190,))
    else:
        md.text(((W - tw2) / 2, 1162), tag, font=font_sub, fill=AMBER_BRIGHT + (190,))

    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.rectangle((60, 30, W - 60, H - 30), fill=210)
    inv = Image.eval(vig, lambda p: 255 - p)
    black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    black.putalpha(inv.filter(ImageFilter.GaussianBlur(90)))
    img = Image.alpha_composite(img, black)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=145, threshold=2))
    img.convert("RGB").save(out_path, "PNG")
    print(f"✅ {out_path}")

for t in TRANSLATIONS:
    out = f"{BASE}/episode_020_cover_{t['lang']}.png"
    build_cover(t["LINE1"], t["LINE2"], t["tag"], out, hindi=t.get("hindi", False))

print("All translated covers done.")
