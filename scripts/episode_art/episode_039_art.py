def draw_art(img, W, H):
    from PIL import Image, ImageDraw, ImageFilter
    import math, random

    def composite(draw_fn, blur=0):
        nonlocal img
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        draw_fn(ld)
        if blur > 0:
            layer = layer.filter(ImageFilter.GaussianBlur(blur))
        img = Image.alpha_composite(img, layer)
        return img

    rng = random.Random(40)
    cx = W // 2
    cy = 565

    def draw_grid(ld):
        for x in range(40, W, 56):
            ld.line([(x, 160), (x, 950)], fill=(90, 125, 210, 18), width=1)
        for y in range(160, 950, 56):
            ld.line([(40, y), (W - 40, y)], fill=(90, 125, 210, 14), width=1)
    composite(draw_grid, blur=0)

    def draw_gateway(ld):
        for i in range(5):
            margin = 160 + i * 26
            alpha = 50 - i * 6
            ld.rounded_rectangle([(cx - margin, 245 - margin * 0.22), (cx + margin, 245 + margin * 0.22)],
                                 radius=24, outline=(110, 200, 255, max(alpha, 12)), width=3)
    composite(draw_gateway, blur=3)

    lane_colors = [
        (90, 210, 255, 42),
        (140, 120, 255, 38),
        (255, 110, 180, 32),
        (120, 240, 190, 30),
    ]
    lane_y = [430, 520, 610, 700]

    def make_lane(y, color):
        def draw_lane(ld):
            pts = [(120, y), (320, y - 14), (cx - 60, y + 10), (cx + 120, y - 12), (W - 120, y + 4)]
            ld.line(pts, fill=color, width=18)
        return draw_lane

    for y, c in zip(lane_y, lane_colors):
        composite(make_lane(y, c), blur=10)

    def draw_nodes(ld):
        for y in lane_y:
            for x in [180, 300, 430, 560, 700, 840, 980, 1120]:
                jx = x + rng.randint(-12, 12)
                jy = y + rng.randint(-10, 10)
                r = rng.randint(6, 16)
                alpha = rng.randint(90, 180)
                color = rng.choice([
                    (150, 230, 255, alpha),
                    (220, 170, 255, alpha),
                    (255, 170, 210, alpha),
                ])
                ld.ellipse([(jx - r, jy - r), (jx + r, jy + r)], fill=color)
    composite(draw_nodes, blur=4)

    def draw_core(ld):
        for r, a in [(165, 20), (120, 36), (78, 70), (42, 120), (18, 220)]:
            ld.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(225, 235, 255, a))
    composite(draw_core, blur=12)

    def draw_orbits(ld):
        for i, r in enumerate([120, 165, 215]):
            ld.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=(180, 210, 255, 55 - i * 10), width=2)
        for a in range(0, 360, 24):
            ang = math.radians(a)
            x1 = cx + 55 * math.cos(ang)
            y1 = cy + 55 * math.sin(ang)
            x2 = cx + 205 * math.cos(ang)
            y2 = cy + 205 * math.sin(ang)
            ld.line([(x1, y1), (x2, y2)], fill=(160, 205, 255, 26), width=1)
    composite(draw_orbits, blur=3)

    def draw_story_satellites(ld):
        satellites = [
            (cx - 250, cy - 150, (120, 230, 255, 150)),
            (cx + 255, cy - 135, (210, 150, 255, 150)),
            (cx - 270, cy + 150, (255, 135, 190, 145)),
            (cx + 270, cy + 165, (120, 245, 190, 140)),
        ]
        for sx, sy, color in satellites:
            ld.line([(cx, cy), (sx, sy)], fill=(150, 200, 255, 34), width=2)
            for r, a in [(34, 28), (22, 60), (10, 180)]:
                rgba = (color[0], color[1], color[2], min(220, a))
                ld.ellipse([(sx - r, sy - r), (sx + r, sy + r)], fill=rgba)
    composite(draw_story_satellites, blur=6)

    def draw_shards(ld):
        for _ in range(28):
            x = rng.randint(120, W - 120)
            y = rng.randint(180, 920)
            w = rng.randint(20, 64)
            h = rng.randint(5, 16)
            angle = math.radians(rng.randint(-55, 55))
            dx = math.cos(angle) * w
            dy = math.sin(angle) * w * 0.35
            color = rng.choice([
                (120, 210, 255, 34),
                (210, 140, 255, 30),
                (255, 140, 190, 26),
            ])
            ld.polygon([(x, y), (x + dx, y + dy), (x + dx + h, y + dy + h), (x + h, y + h)], fill=color)
    composite(draw_shards, blur=2)

    def draw_breach_wave(ld):
        for i in range(5):
            y = 840 + i * 16
            alpha = 50 - i * 8
            pts = [(160, y), (360, y - 18), (620, y + 10), (860, y - 16), (1140, y + 8), (W - 160, y - 12)]
            ld.line(pts, fill=(255, 120, 160, max(alpha, 10)), width=3)
    composite(draw_breach_wave, blur=5)

    def draw_vignette(ld):
        for step in range(16):
            m = step * 30
            alpha = 12
            ld.rectangle([(m, 150 + m // 2), (W - m, 960 - m // 2)], outline=(8, 10, 26, alpha), width=3)
    composite(draw_vignette, blur=0)

    return img
