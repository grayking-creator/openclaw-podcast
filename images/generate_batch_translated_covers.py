#!/usr/bin/env python3
from __future__ import annotations

import shutil
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = Path('/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images')
LATIN_FONT = '/System/Library/Fonts/HelveticaNeue.ttc'
DEVANAGARI_FONT = '/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc'

WHITE = (245, 245, 245)
ORANGE = (255, 183, 80)
PURPLE = (198, 126, 255)
GREEN = (88, 234, 126)
BLUE = (124, 188, 255)
GRAY = (170, 170, 180)
DARK = (6, 6, 14, 245)
DARK_SOFT = (10, 10, 22, 225)

TRANSLATABLE = {
    '003': {
        'source': 'episode_003_cover.png',
        'rects': [(70, 900, 1130, 1185, 40), (98, 935, 1100, 1165, 30)],
        'lines': lambda locale, t: [
            {'text': 'OPENCLAW DAILY', 'size': 46, 'color': BLUE, 'font': 'latin', 'y': 1010, 'align': 'center'},
            {'text': t, 'size': 92, 'color': WHITE, 'font': 'dev' if locale == 'hi' else 'latin', 'y': 1070, 'align': 'center'},
        ],
        'translations': {
            'es': 'LA CONTROVERSIA',
            'de': 'DIE KONTROVERSE',
            'pt': 'A CONTROVÉRSIA',
            'hi': 'विवाद',
        },
    },
    '004': {
        'source': 'episode_004_cover.png',
        'rects': [(22, 960, 860, 1188, 30), (38, 980, 836, 1172, 22)],
        'lines': lambda locale, t: [
            {'text': t, 'size': 78 if locale != 'hi' else 68, 'color': WHITE, 'font': 'dev' if locale == 'hi' else 'latin', 'y': 1030, 'align': 'left', 'x': 56, 'max_width': 720},
            {'text': 'Nova & Alloy  •  OpenClaw Daily', 'size': 28, 'color': GRAY, 'font': 'latin', 'y': 1135, 'align': 'left', 'x': 58},
        ],
        'translations': {
            'es': 'El Despertar de los Agentes',
            'de': 'Das Erwachen der Agenten',
            'pt': 'O Despertar dos Agentes',
            'hi': 'एजेंट्स का जागरण',
        },
    },
    '005': {
        'source': 'episode_005_cover.png',
        'rects': [(20, 930, 790, 1188, 30), (36, 952, 768, 1172, 22)],
        'lines': lambda locale, t: wrap_lines(locale, t, x=55, y=998, max_width=680, size=78, line_gap=6, accent=GREEN),
        'translations': {
            'es': 'La Revolución de la IA Local',
            'de': 'Die Lokale KI-Revolution',
            'pt': 'A Revolução da IA Local',
            'hi': 'स्थानीय AI क्रांति',
        },
    },
    '006': {
        'source': 'episode_006_cover.png',
        'rects': [(20, 920, 950, 1188, 30), (36, 944, 928, 1172, 22)],
        'lines': lambda locale, t: wrap_lines(locale, t, x=56, y=988, max_width=830, size=74 if locale != 'hi' else 62, line_gap=2, accent=WHITE),
        'translations': {
            'es': 'La Actualización v2026.2.24 y Redes Sociales de Bots',
            'de': 'Das v2026.2.24 Update & Bot-Soziale Netzwerke',
            'pt': 'A Atualização v2026.2.24 e Redes Sociais de Bots',
            'hi': 'v2026.2.24 अपडेट और बॉट सोशल नेटवर्क',
        },
    },
    '007': {
        'source': 'episode_007_cover.png',
        'rects': [(20, 920, 900, 1188, 30), (36, 944, 876, 1172, 22)],
        'lines': lambda locale, t: wrap_lines(locale, t, x=58, y=980, max_width=760, size=76 if locale != 'hi' else 64, line_gap=4, accent=ORANGE),
        'translations': {
            'es': 'La Semana que OpenClaw Creció',
            'de': 'Die Woche, in der OpenClaw erwachsen wurde',
            'pt': 'A Semana em que o OpenClaw Cresceu',
            'hi': 'जिस हफ्ते OpenClaw बड़ा हुआ',
        },
    },
    '008': {
        'source': 'episode_008_cover.png',
        'rects': [(20, 920, 800, 1188, 30), (36, 944, 776, 1172, 22)],
        'lines': lambda locale, t: wrap_lines(locale, t, x=56, y=980, max_width=670, size=76 if locale != 'hi' else 64, line_gap=4, accent=ORANGE),
        'translations': {
            'es': 'La Revolución de la IA de Código Abierto',
            'de': 'Die Open-Source-KI-Revolution',
            'pt': 'A Revolução da IA de Código Aberto',
            'hi': 'ओपन सोर्स AI क्रांति',
        },
    },
    '012': {
        'source': 'episode_012_cover.png',
        'rects': [(30, 940, 1170, 1188, 28), (54, 968, 1146, 1170, 22)],
        'lines': lambda locale, t: [
            {'text': 'EPISODE 12', 'size': 78, 'color': WHITE, 'font': 'latin', 'y': 1020, 'align': 'center'},
            {'text': t, 'size': 34 if locale != 'hi' else 31, 'color': PURPLE, 'font': 'dev' if locale == 'hi' else 'latin', 'y': 1110, 'align': 'center', 'max_width': 1040},
        ],
        'translations': {
            'es': 'Modelos Frontier Gratuitos • Memoria Multimodal • Automatizaciones Comunitarias',
            'de': 'Kostenlose Frontier-Modelle • Multimodale Erinnerung • Community-Automatisierungen',
            'pt': 'Modelos Frontier Gratuitos • Memória Multimodal • Automações da Comunidade',
            'hi': 'मुफ्त फ्रंटियर मॉडल • मल्टीमोडल मेमोरी • सामुदायिक स्वचालन',
        },
    },
    '013': {
        'source': 'episode_013_cover.png',
        'rects': [(170, 690, 1080, 1158, 36), (200, 720, 1050, 1135, 26)],
        'lines': lambda locale, t: ep13_lines(locale, t),
        'translations': {
            'es': ('NVIDIA ELIGIÓ OPENCLAW', 'NemoClaw • Nemotron 3 Super • DGX Spark'),
            'de': ('NVIDIA WÄHLTE OPENCLAW', 'NemoClaw • Nemotron 3 Super • DGX Spark'),
            'pt': ('NVIDIA ESCOLHEU OPENCLAW', 'NemoClaw • Nemotron 3 Super • DGX Spark'),
            'hi': ('NVIDIA ने OPENCLAW चुना', 'NemoClaw • Nemotron 3 Super • DGX Spark'),
        },
    },
}

COPY_ONLY = {
    '001': 'episode_001_cover.png',
    '002': 'episode_002_cover.png',
    '009': 'ep009_cover.png',
    '010': 'episode_010_cover.png',
}


def font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def fit_font(draw, text, path, max_size, min_size, max_width):
    for size in range(max_size, min_size - 1, -2):
        f = font(path, size)
        box = draw.textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= max_width:
            return f
    return font(path, min_size)


def script_segments(text: str):
    segments = []
    if not text:
        return segments
    current = text[0]
    current_type = char_type(text[0])
    for ch in text[1:]:
        t = char_type(ch)
        if t == current_type:
            current += ch
        else:
            segments.append((current_type, current))
            current = ch
            current_type = t
    segments.append((current_type, current))
    return segments


def char_type(ch: str):
    code = ord(ch)
    if 0x0900 <= code <= 0x097F:
        return 'dev'
    return 'latin'


def line_width(draw, text, latin_font, dev_font):
    width = 0
    for seg_type, seg in script_segments(text):
        f = dev_font if seg_type == 'dev' else latin_font
        box = draw.textbbox((0, 0), seg, font=f)
        width += box[2] - box[0]
    return width


def draw_mixed_text(draw, x, y, text, latin_font, dev_font, fill, shadow=(0,0,0,140), align='left', max_width=None, center_x=None):
    width = line_width(draw, text, latin_font, dev_font)
    if align == 'center' and center_x is not None:
        x = center_x - width / 2
    cursor = x
    for dx, dy, color in [(-2, 2, shadow), (0, 0, fill)]:
        cursor = x
        for seg_type, seg in script_segments(text):
            f = dev_font if seg_type == 'dev' else latin_font
            draw.text((cursor + dx, y + dy), seg, font=f, fill=color)
            box = draw.textbbox((0, 0), seg, font=f)
            cursor += box[2] - box[0]


def wrap_text(draw, text, font_path, max_size, min_size, max_width, max_lines):
    words = text.split()
    for size in range(max_size, min_size - 1, -2):
        f = font(font_path, size)
        lines = []
        cur = ''
        for word in words:
            trial = word if not cur else cur + ' ' + word
            w = draw.textbbox((0, 0), trial, font=f)[2]
            if w <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                    cur = word
                else:
                    lines.append(trial)
                    cur = ''
        if cur:
            lines.append(cur)
        if len(lines) <= max_lines and all(draw.textbbox((0,0), line, font=f)[2] <= max_width for line in lines):
            return f, lines
    return font(font_path, min_size), textwrap.wrap(text, width=max(8, int(max_width / 22)))[:max_lines]


def wrap_lines(locale, text, x, y, max_width, size, line_gap, accent):
    # Placeholder marker object interpreted later.
    return {'kind': 'wrapped', 'locale': locale, 'text': text, 'x': x, 'y': y, 'max_width': max_width, 'size': size, 'line_gap': line_gap, 'accent': accent}


def ep13_lines(locale, pair):
    title, subtitle = pair
    return [
        {'text': title, 'size': 76 if locale != 'hi' else 62, 'color': WHITE, 'font': 'mixed' if locale == 'hi' else 'latin', 'y': 790, 'align': 'center', 'max_width': 760},
        {'text': subtitle, 'size': 42, 'color': GRAY, 'font': 'latin', 'y': 1045, 'align': 'center', 'max_width': 730},
    ]


def add_panel(img, rects):
    panel = Image.new('RGBA', img.size, (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel, 'RGBA')
    for x1, y1, x2, y2, r in rects:
        fill = DARK if (x2 - x1) > 900 else DARK_SOFT
        pd.rounded_rectangle((x1, y1, x2, y2), radius=r, fill=fill)
    panel = panel.filter(ImageFilter.GaussianBlur(5))
    return Image.alpha_composite(img, panel)


def render_lines(img, episode, locale, translation):
    draw = ImageDraw.Draw(img)
    spec = TRANSLATABLE[episode]
    items = spec['lines'](locale, translation)
    if isinstance(items, dict) and items.get('kind') == 'wrapped':
        items = render_wrapped_spec(draw, items)
    elif any(isinstance(item, dict) and item.get('kind') == 'wrapped' for item in items):
        expanded = []
        for item in items:
            if item.get('kind') == 'wrapped':
                expanded.extend(render_wrapped_spec(draw, item))
            else:
                expanded.append(item)
        items = expanded

    for item in items:
        text = item['text']
        y = item['y']
        size = item['size']
        color = item['color']
        align = item.get('align', 'left')
        max_width = item.get('max_width', 1000)
        if item['font'] == 'mixed':
            latin = fit_font(draw, text, LATIN_FONT, size, max(18, size - 26), max_width)
            dev = fit_font(draw, text, DEVANAGARI_FONT, size, max(18, size - 26), max_width)
            draw_mixed_text(draw, item.get('x', 0), y, text, latin, dev, color, align=align, center_x=600)
        else:
            path = DEVANAGARI_FONT if item['font'] == 'dev' else LATIN_FONT
            f = fit_font(draw, text, path, size, max(18, size - 28), max_width)
            if align == 'center':
                box = draw.textbbox((0, 0), text, font=f)
                x = 600 - (box[2] - box[0]) / 2
            else:
                x = item.get('x', 55)
            for dx, dy, fill in [(-2, 2, (0, 0, 0, 145)), (0, 0, color)]:
                draw.text((x + dx, y + dy), text, font=f, fill=fill)


def render_wrapped_spec(draw, item):
    text = item['text']
    locale = item['locale']
    path = DEVANAGARI_FONT if locale == 'hi' else LATIN_FONT
    f, lines = wrap_text(draw, text, path, item['size'], max(22, item['size'] - 28), item['max_width'], 3)
    out = []
    y = item['y']
    for i, line in enumerate(lines):
        color = WHITE if i < len(lines) - 1 else item['accent']
        out.append({'text': line, 'size': getattr(f, 'size', item['size']), 'color': color, 'font': 'dev' if locale == 'hi' else 'latin', 'y': y, 'align': 'left', 'x': item['x'], 'max_width': item['max_width']})
        box = draw.textbbox((0, 0), line, font=f)
        y += (box[3] - box[1]) + item['line_gap']
    out.append({'text': 'Nova & Alloy  •  OpenClaw Daily', 'size': 28, 'color': GRAY, 'font': 'latin', 'y': min(1140, y + 12), 'align': 'left', 'x': item['x'] + 2, 'max_width': 700})
    return out


def make_cover(episode: str, locale: str, translation):
    spec = TRANSLATABLE[episode]
    img = Image.open(OUT_DIR / spec['source']).convert('RGBA')
    img = add_panel(img, spec['rects'])
    render_lines(img, episode, locale, translation)
    out = OUT_DIR / f'episode_{episode}_cover_{locale}.png'
    img.convert('RGB').save(out)
    return out


def copy_cover(episode: str, source_name: str, locale: str):
    src = OUT_DIR / source_name
    out = OUT_DIR / f'episode_{episode}_cover_{locale}.png'
    shutil.copy2(src, out)
    return out


def main():
    paths = []
    for episode, source_name in COPY_ONLY.items():
        for locale in ('es', 'de', 'pt', 'hi'):
            paths.append(copy_cover(episode, source_name, locale))

    for episode, spec in TRANSLATABLE.items():
        for locale, translation in spec['translations'].items():
            paths.append(make_cover(episode, locale, translation))

    print('\n'.join(str(p) for p in paths))


if __name__ == '__main__':
    main()
