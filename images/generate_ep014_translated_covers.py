#!/usr/bin/env python3
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_014_cover.png"
OUT_DIR = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images"

TRANSLATIONS = {
    "de": ("DIE ÜBERNAHME", "VON ALLEM"),
    "es": ("LA ADQUISICIÓN", "DE TODO"),
    "pt": ("A AQUISIÇÃO", "DE TUDO"),
    "hi": ("सब कुछ का", "अधिग्रहण"),
}

WHITE = (255, 255, 255)
CYAN = (39, 199, 255)
BG = (4, 5, 14, 255)
BG_SOFT = (8, 12, 22, 235)
LATIN_FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
DEVANAGARI_FONT = "/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc"


def font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def fit_font(draw: ImageDraw.ImageDraw, text: str, path: str, max_size: int, min_size: int, max_width: int):
    for size in range(max_size, min_size - 1, -2):
        f = font(path, size)
        box = draw.textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= max_width:
            return f
    return font(path, min_size)


def centered(draw: ImageDraw.ImageDraw, text: str, fnt, width: int = 1400):
    box = draw.textbbox((0, 0), text, font=fnt)
    return (width - (box[2] - box[0])) // 2


def make_cover(locale: str, line1: str, line2: str):
    img = Image.open(BASE).convert("RGBA")

    # Replace the original English title block with a dark footer panel.
    panel = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel, "RGBA")
    pd.rounded_rectangle((210, 1095, 1190, 1395), radius=28, fill=BG)
    pd.rounded_rectangle((240, 1120, 1160, 1370), radius=18, fill=BG_SOFT)
    panel = panel.filter(ImageFilter.GaussianBlur(4))
    img = Image.alpha_composite(img, panel)

    draw = ImageDraw.Draw(img)
    is_hi = locale == "hi"
    title_font = fit_font(draw, line1, DEVANAGARI_FONT if is_hi else LATIN_FONT, 92 if not is_hi else 88, 54, 980)
    sub_font = fit_font(draw, line2, DEVANAGARI_FONT if is_hi else LATIN_FONT, 92 if not is_hi else 88, 54, 980)
    episode_font = font(LATIN_FONT, 66)
    brand_font = font(LATIN_FONT, 60)

    # Refresh the top header text so the style remains consistent after edits.
    top_panel = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(top_panel, "RGBA")
    td.rounded_rectangle((410, 18, 990, 176), radius=20, fill=(8, 11, 20, 180))
    top_panel = top_panel.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img, top_panel)
    draw = ImageDraw.Draw(img)

    brand = "OPENCLAW DAILY"
    bx = centered(draw, brand, brand_font)
    draw.text((bx, 40), brand, font=brand_font, fill=WHITE)

    ep = "Episode 14"
    ex = centered(draw, ep, episode_font)
    draw.text((ex, 105), ep, font=episode_font, fill=CYAN)

    x1 = centered(draw, line1, title_font)
    x2 = centered(draw, line2, sub_font)
    y1 = 1145 if not is_hi else 1162
    y2 = 1260 if not is_hi else 1278

    for dx, dy, fill in [(-2, 2, (0, 0, 0, 150)), (0, 0, WHITE)]:
        draw.text((x1 + dx, y1 + dy), line1, font=title_font, fill=fill)
        draw.text((x2 + dx, y2 + dy), line2, font=sub_font, fill=fill)

    out = f"{OUT_DIR}/episode_014_cover_{locale}.png"
    img.convert("RGB").save(out)
    return out


def main():
    paths = [make_cover(locale, line1, line2) for locale, (line1, line2) in TRANSLATIONS.items()]
    print("\n".join(paths))


if __name__ == "__main__":
    main()
