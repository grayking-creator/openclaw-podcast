#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import shutil

BASE = Path('/Users/tobyglennpeters/.openclaw/workspace/openclaw-podcast/images')
LATIN_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
LATIN_REG = '/System/Library/Fonts/Helvetica.ttc'
HINDI_FONT = '/System/Library/Fonts/Supplemental/Devanagari Sangam MN.ttc'
BYLINE_COLOR = (120, 130, 160)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 255)

LANGS = ['es', 'de', 'pt', 'hi']

TRANSLATIONS = {
    '004': {
        'type': 'left_1', 'rect': (0, 1220, 1400, 1400), 'title_y': 1235, 'byline_y': 1325,
        'titles': {
            'es': ['El Despertar de los Agentes'],
            'de': ['Das Erwachen der Agenten'],
            'pt': ['O Despertar dos Agentes'],
            'hi': ['एजेंट्स का जागरण'],
        }
    },
    '005': {
        'type': 'left_1', 'rect': (0, 1220, 1400, 1400), 'title_y': 1235, 'byline_y': 1325,
        'titles': {
            'es': ['La Revolución de la IA Local'],
            'de': ['Die Lokale KI-Revolution'],
            'pt': ['A Revolução da IA Local'],
            'hi': ['स्थानीय AI क्रांति'],
        }
    },
    '006': {
        'type': 'left_2', 'rect': (0, 1180, 1400, 1400), 'line_ys': [1200, 1280], 'byline_y': 1360,
        'titles': {
            'es': ['Actualización v2026.2.24', 'y Redes Sociales de Bots'],
            'de': ['Das v2026.2.24 Update', '& Bot-Soziale Netzwerke'],
            'pt': ['Atualização v2026.2.24', 'e Redes Sociais de Bots'],
            'hi': ['v2026.2.24 अपडेट', 'और बॉट सोशल नेटवर्क'],
        }
    },
    '007': {
        'type': 'left_2', 'rect': (0, 1145, 1400, 1400), 'line_ys': [1168, 1245], 'byline_y': 1325,
        'titles': {
            'es': ['La Semana que OpenClaw', 'Creció'],
            'de': ['Die Woche, in der OpenClaw', 'erwachsen wurde'],
            'pt': ['A Semana em que o OpenClaw', 'Cresceu'],
            'hi': ['जिस हफ्ते OpenClaw', 'बड़ा हुआ'],
        }
    },
    '008': {
        'type': 'left_2', 'rect': (0, 1145, 1400, 1400), 'line_ys': [1168, 1247], 'byline_y': 1325,
        'titles': {
            'es': ['La Revolución de la IA', 'de Código Abierto'],
            'de': ['Die Open-Source', 'KI-Revolution'],
            'pt': ['A Revolução da IA', 'de Código Aberto'],
            'hi': ['ओपन सोर्स', 'AI क्रांति'],
        }
    },
    '012': {
        'type': 'center_subtitle', 'rect': (0, 1290, 1400, 1400), 'subtitle_y': 1315,
        'subtitles': {
            'es': 'Modelos Frontier Gratuitos • Memoria Multimodal • Automatizaciones Comunitarias',
            'de': 'Kostenlose Frontier-Modelle • Multimodale Erinnerung • Community-Automatisierungen',
            'pt': 'Modelos Frontier Gratuitos • Memória Multimodal • Automações da Comunidade',
            'hi': 'मुफ्त फ्रंटियर मॉडल • मल्टीमोडल मेमोरी • सामुदायिक स्वचालन',
        }
    },
    '013': {
        'type': 'center_headline', 'rect': (0, 1040, 1400, 1155), 'headline_y': 1060,
        'headlines': {
            'es': 'NVIDIA ELIGIÓ',
            'de': 'NVIDIA WÄHLTE',
            'pt': 'NVIDIA ESCOLHEU',
            'hi': 'NVIDIA ने चुना',
        }
    }
}

BYLINE = 'Nova & Alloy • OpenClaw Daily'

def load_font(path, size):
    return ImageFont.truetype(path, size)

def font_for_lang(lang, size, bold=True):
    if lang == 'hi':
        return load_font(HINDI_FONT, size)
    return load_font(LATIN_BOLD if bold else LATIN_REG, size)

def fit_font(draw, text, lang, max_width, start_size, min_size=24, bold=True):
    for size in range(start_size, min_size - 1, -2):
        font = font_for_lang(lang, size, bold=bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
    return font_for_lang(lang, min_size, bold=bold)

def centered_x(draw, text, font, width=1400):
    bbox = draw.textbbox((0, 0), text, font=font)
    return (width - (bbox[2] - bbox[0])) // 2

def add_opaque_rect(img, rect):
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle(rect, fill=BLACK)
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def render_left_block(ep, lang):
    cfg = TRANSLATIONS[ep]
    src = BASE / f'episode_{ep}_cover.png'
    out = BASE / f'episode_{ep}_cover_{lang}.png'
    img = Image.open(src).convert('RGBA')
    img = add_opaque_rect(img, cfg['rect'])
    draw = ImageDraw.Draw(img)

    max_width = 1260
    x = 70
    if cfg['type'] == 'left_1':
        title = cfg['titles'][lang][0]
        font = fit_font(draw, title, lang, max_width, 70 if lang != 'hi' else 66, min_size=42, bold=True)
        draw.text((x, cfg['title_y']), title, fill=WHITE, font=font)
    else:
        for i, line in enumerate(cfg['titles'][lang]):
            font = fit_font(draw, line, lang, max_width, 70 if lang != 'hi' else 66, min_size=40, bold=True)
            draw.text((x, cfg['line_ys'][i]), line, fill=WHITE, font=font)
    by_font = fit_font(draw, BYLINE, 'es', 1260, 36, min_size=30, bold=False)
    draw.text((x, cfg['byline_y']), BYLINE, fill=BYLINE_COLOR, font=by_font)
    img.convert('RGB').save(out)

def render_ep12(lang):
    cfg = TRANSLATIONS['012']
    src = BASE / 'episode_012_cover.png'
    out = BASE / f'episode_012_cover_{lang}.png'
    img = Image.open(src).convert('RGBA')
    img = add_opaque_rect(img, cfg['rect'])
    draw = ImageDraw.Draw(img)
    text = cfg['subtitles'][lang]
    font = fit_font(draw, text, lang, 1280, 36 if lang != 'hi' else 34, min_size=20, bold=False)
    draw.text((centered_x(draw, text, font), cfg['subtitle_y']), text, fill=(180, 100, 255), font=font)
    img.convert('RGB').save(out)

def render_ep13(lang):
    cfg = TRANSLATIONS['013']
    src = BASE / 'episode_013_cover.png'
    out = BASE / f'episode_013_cover_{lang}.png'
    img = Image.open(src).convert('RGBA')
    img = add_opaque_rect(img, cfg['rect'])
    draw = ImageDraw.Draw(img)
    text = cfg['headlines'][lang]
    font = fit_font(draw, text, lang, 1000, 90 if lang != 'hi' else 82, min_size=46, bold=True)
    draw.text((centered_x(draw, text, font), cfg['headline_y']), text, fill=WHITE, font=font)
    img.convert('RGB').save(out)

def copy_ep10():
    src = BASE / 'episode_010_cover.png'
    for lang in LANGS:
        shutil.copy2(src, BASE / f'episode_010_cover_{lang}.png')

def main():
    for ep in ['004', '005', '006', '007', '008']:
        for lang in LANGS:
            render_left_block(ep, lang)
    copy_ep10()
    for lang in LANGS:
        render_ep12(lang)
        render_ep13(lang)
    print('generated 32 files')

if __name__ == '__main__':
    main()
