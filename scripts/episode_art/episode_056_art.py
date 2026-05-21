from PIL import Image, ImageDraw, ImageFilter
import math
import random


def draw_art(img, W, H):
    """EP056 bespoke center art: agent runtime control deck and private-tool lanes."""
    random.seed(56056)

    ink = (5, 10, 18)
    cyan = (45, 218, 235)
    blue = (70, 132, 255)
    green = (70, 224, 145)
    amber = (255, 184, 66)
    violet = (184, 105, 255)
    red = (255, 88, 94)
    white = (235, 248, 255)

    def composite(draw_fn, blur=0):
        nonlocal img
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        draw_fn(d)
        if blur:
            layer = layer.filter(ImageFilter.GaussianBlur(blur))
        img = Image.alpha_composite(img, layer)
        return img

    composite(lambda d: d.rounded_rectangle((120, 145, W - 120, 985), radius=58,
                                            fill=blue + (26,)), 42)
    composite(lambda d: d.ellipse((280, 210, W - 280, 870), fill=cyan + (20,)), 76)
    composite(lambda d: d.ellipse((455, 260, W - 455, 760), fill=violet + (16,)), 58)

    def grid(d):
        for x in range(100, W - 90, 58):
            d.line((x, 145, x, 1000), fill=(110, 150, 190, 24), width=1)
        for y in range(155, 1010, 58):
            d.line((90, y, W - 90, y), fill=(110, 150, 190, 20), width=1)
        for _ in range(58):
            x = random.randint(140, W - 140)
            y = random.randint(165, 970)
            col = random.choice([cyan, blue, green, amber, violet])
            d.rectangle((x - 2, y - 2, x + 2, y + 2), fill=col + (90,))

    composite(grid)

    cx, cy = W // 2, 535

    def main_console(d):
        d.rounded_rectangle((cx - 300, cy - 205, cx + 300, cy + 205), radius=34,
                            fill=ink + (242,), outline=white + (120,), width=3)
        d.rounded_rectangle((cx - 270, cy - 172, cx + 270, cy - 124), radius=14,
                            fill=cyan + (42,), outline=cyan + (170,), width=2)
        for i in range(5):
            x = cx - 232 + i * 112
            col = [cyan, green, amber, violet, blue][i]
            d.rounded_rectangle((x, cy - 80, x + 78, cy + 76), radius=15,
                                fill=col + (34,), outline=col + (165,), width=2)
            d.ellipse((x + 23, cy - 48, x + 55, cy - 16), fill=col + (215,))
            d.line((x + 24, cy + 1, x + 54, cy + 1), fill=white + (135,), width=4)
            d.line((x + 19, cy + 22, x + 59, cy + 22), fill=white + (90,), width=3)
            d.line((x + 29, cy + 43, x + 49, cy + 43), fill=white + (85,), width=3)
        for i in range(3):
            y = cy + 112 + i * 25
            d.rounded_rectangle((cx - 235, y, cx + 235, y + 10), radius=5,
                                fill=white + (40,))
            d.rounded_rectangle((cx - 235, y, cx - 80 + i * 52, y + 10), radius=5,
                                fill=[green, amber, cyan][i] + (170,))
        d.polygon([(cx - 32, cy - 148), (cx + 2, cy - 160), (cx + 32, cy - 148),
                   (cx + 24, cy - 130), (cx - 24, cy - 130)], fill=white + (150,))

    composite(lambda d: d.rounded_rectangle((cx - 350, cy - 255, cx + 350, cy + 255),
                                            radius=52, fill=cyan + (23,)), 30)
    composite(main_console)

    nodes = [
        (230, 315, cyan, "plugin"),
        (238, 735, green, "tunnel"),
        (1160, 315, amber, "event"),
        (1160, 735, violet, "sandbox"),
        (700, 895, blue, "route"),
    ]

    def node_glow(d):
        for x, y, col, _ in nodes:
            d.ellipse((x - 122, y - 78, x + 122, y + 78), fill=col + (25,))

    def draw_nodes(d):
        for x, y, col, _ in nodes:
            d.line((cx, cy, x, y), fill=col + (92,), width=4)
        for x, y, col, kind in nodes:
            d.rounded_rectangle((x - 112, y - 64, x + 112, y + 64), radius=23,
                                fill=ink + (238,), outline=col + (210,), width=3)
            if kind == "plugin":
                for i in range(3):
                    bx = x - 58 + i * 44
                    d.rounded_rectangle((bx, y - 28, bx + 32, y + 28), radius=8,
                                        fill=col + (58,), outline=col + (175,), width=2)
                    if i:
                        d.line((bx - 12, y, bx, y), fill=white + (120,), width=3)
            elif kind == "tunnel":
                d.arc((x - 62, y - 38, x + 62, y + 38), 190, 350, fill=col + (220,), width=6)
                d.arc((x - 42, y - 22, x + 42, y + 22), 190, 350, fill=white + (145,), width=4)
                d.polygon([(x + 55, y - 13), (x + 82, y), (x + 55, y + 13)], fill=col + (230,))
            elif kind == "event":
                for i in range(4):
                    yy = y - 34 + i * 22
                    d.ellipse((x - 66, yy - 5, x - 56, yy + 5), fill=col + (210,))
                    d.line((x - 42, yy, x + 62 - i * 12, yy), fill=white + (125,), width=4)
            elif kind == "sandbox":
                for row in range(2):
                    for col_i in range(3):
                        bx = x - 64 + col_i * 48
                        by = y - 32 + row * 42
                        d.rounded_rectangle((bx, by, bx + 34, by + 26), radius=7,
                                            fill=col + (54,), outline=col + (165,), width=2)
            else:
                d.arc((x - 52, y - 52, x + 52, y + 52), 210, 25, fill=col + (220,), width=8)
                d.line((x, y, x + 35, y - 26), fill=white + (175,), width=5)
                for a in [230, 270, 310, 350]:
                    px = x + math.cos(math.radians(a)) * 42
                    py = y + math.sin(math.radians(a)) * 42
                    d.ellipse((px - 4, py - 4, px + 4, py + 4), fill=white + (115,))

    composite(node_glow, 18)
    composite(draw_nodes)

    def bottom_data_lanes(d):
        y0 = 1000
        colors = [cyan, green, amber, violet, blue]
        for lane in range(5):
            y = y0 + lane * 18
            last = None
            for i in range(20):
                x = 175 + i * 55
                yy = y + math.sin(i * 0.66 + lane) * 8
                col = colors[(i + lane) % len(colors)]
                if last:
                    d.line((last[0], last[1], x, yy), fill=col + (56,), width=3)
                if i % 4 == lane % 4:
                    d.ellipse((x - 5, yy - 5, x + 5, yy + 5), fill=col + (135,))
                last = (x, yy)

    composite(bottom_data_lanes)

    def alert_chip(d):
        d.rounded_rectangle((510, 178, 890, 236), radius=18,
                            fill=(8, 20, 32, 220), outline=red + (160,), width=2)
        for i, col in enumerate([red, amber, green]):
            x = 548 + i * 36
            d.ellipse((x - 9, 207 - 9, x + 9, 207 + 9), fill=col + (210,))
        d.line((660, 207, 840, 207), fill=white + (95,), width=5)

    composite(alert_chip)
    return img
