#!/usr/bin/env python3
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images/episode_011_cover.png"
OUT_DIR = "/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images"

TRANSLATIONS = {
    "de": ("OpenClaw Goes Hardware", "Die Agentenschicht wird real"),
    "es": ("OpenClaw Goes Hardware", "La capa de agentes se vuelve real"),
    "pt": ("OpenClaw Goes Hardware", "A camada de agentes se torna real"),
    "hi": ("OpenClaw Goes Hardware", "एजेंट लेयर वास्तविक हो गई"),
}

WHITE = (245, 245, 245)
ORANGE = (232, 145, 45)
GRAY = (174, 174, 174)
BG = (10, 7, 3, 255)
BG_SOFT = (22, 14, 6, 235)
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


def make_cover(locale: str, title: str, subtitle: str):
    img = Image.open(BASE).convert("RGBA")

    # Replace the bottom-left text block while preserving the central hardware illustration.
    panel = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel, "RGBA")
    pd.rounded_rectangle((55, 1030, 1210, 1390), radius=26, fill=BG)
    pd.rounded_rectangle((78, 1050, 1185, 1368), radius=18, fill=BG_SOFT)
    panel = panel.filter(ImageFilter.GaussianBlur(5))
    img = Image.alpha_composite(img, panel)

    draw = ImageDraw.Draw(img)

    title_font = fit_font(draw, title, LATIN_FONT, 70, 42, 860)
    subtitle_font = fit_font(draw, subtitle, DEVANAGARI_FONT if locale == 'hi' else LATIN_FONT, 52 if locale != 'hi' else 46, 24, 920)
    credit_font = font(LATIN_FONT, 28)

    title_x, title_y = 120, 1090
    subtitle_x, subtitle_y = 120, 1196 if locale != 'hi' else 1204
    credit_y = 1315

    for dx, dy, fill in [(-2, 2, (0, 0, 0, 150)), (0, 0, WHITE)]:
        draw.text((title_x + dx, title_y + dy), title, font=title_font, fill=fill)
    for dx, dy, fill in [(-1, 2, (0, 0, 0, 140)), (0, 0, ORANGE)]:
        draw.text((subtitle_x + dx, subtitle_y + dy), subtitle, font=subtitle_font, fill=fill)

    credit = "Nova & Alloy · OpenClaw Daily"
    draw.text((120, credit_y), credit, font=credit_font, fill=GRAY)

    out = f"{OUT_DIR}/episode_011_cover_{locale}.png"
    img.convert("RGB").save(out)
    return out


def main():
    paths = [make_cover(locale, title, subtitle) for locale, (title, subtitle) in TRANSLATIONS.items()]
    print("\n".join(paths))


if __name__ == "__main__":
    main()
