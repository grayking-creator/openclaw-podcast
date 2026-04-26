def draw_art(img, W, H):
    from PIL import Image, ImageDraw, ImageFilter
    import math, random

    def composite(draw_fn, blur=0):
        nonlocal img
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        draw_fn(ld)
        if blur:
            layer = layer.filter(ImageFilter.GaussianBlur(blur))
        img = Image.alpha_composite(img, layer)
        return img

    rng = random.Random(404004)
    cx, cy = W // 2, 520

    # Concrete EP040 centerpiece: Anthropic/Google agent deal table + Claude connectors + ComfyUI nodes + Meet artifacts.
    def draw_deal_table(ld):
        ld.rounded_rectangle([(250, 290), (1150, 760)], radius=42, fill=(12, 18, 40, 155), outline=(135, 210, 255, 85), width=4)
        ld.rounded_rectangle([(305, 345), (1095, 705)], radius=28, fill=(245, 238, 220, 32), outline=(245, 238, 220, 70), width=2)
        # signed deal card in the middle
        ld.rounded_rectangle([(530, 365), (870, 650)], radius=22, fill=(250, 245, 226, 205), outline=(255, 220, 120, 135), width=4)
        for y in [420, 465, 510, 555]:
            ld.line([(585, y), (815, y)], fill=(45, 55, 78, 110), width=5)
        ld.arc([(610, 565), (750, 635)], 200, 350, fill=(30, 42, 68, 150), width=5)
        ld.line([(735, 610), (815, 590)], fill=(30, 42, 68, 150), width=4)
    composite(draw_deal_table, blur=2)

    def draw_anthropic_mark(ld):
        # Anthropic-inspired vertical bars on the left, not text.
        base_x, base_y = 370, 455
        heights = [145, 205, 145]
        xs = [base_x, base_x + 52, base_x + 104]
        for x, h in zip(xs, heights):
            ld.rounded_rectangle([(x, base_y + (205 - h)//2), (x + 34, base_y + (205 - h)//2 + h)], radius=15, fill=(238, 225, 198, 205))
        ld.rounded_rectangle([(330, 405), (520, 640)], radius=34, outline=(238, 225, 198, 75), width=3)
    composite(draw_anthropic_mark, blur=2)

    def draw_google_g_and_handshake(ld):
        # Google-colored G-like ring on right.
        gx, gy, r = 1010, 520, 95
        box = [(gx-r, gy-r), (gx+r, gy+r)]
        ld.arc(box, 310, 45, fill=(66, 133, 244, 220), width=22)
        ld.arc(box, 45, 135, fill=(52, 168, 83, 220), width=22)
        ld.arc(box, 135, 220, fill=(251, 188, 5, 220), width=22)
        ld.arc(box, 220, 310, fill=(234, 67, 53, 220), width=22)
        ld.line([(gx+18, gy), (gx+92, gy)], fill=(66, 133, 244, 220), width=20)
        ld.line([(gx+72, gy), (gx+72, gy+44)], fill=(66, 133, 244, 220), width=18)
        # handshake crossing from Anthropic side to Google side over the deal card
        ld.rounded_rectangle([(500, 515), (652, 565)], radius=22, fill=(238, 225, 198, 175))
        ld.rounded_rectangle([(748, 515), (900, 565)], radius=22, fill=(120, 190, 255, 170))
        ld.polygon([(640, 505), (720, 535), (680, 592), (604, 558)], fill=(238, 225, 198, 190))
        ld.polygon([(760, 505), (680, 535), (720, 592), (796, 558)], fill=(120, 190, 255, 185))
        for i in range(4):
            ld.line([(666+i*18, 552+i%2*3), (690+i*18, 584)], fill=(35, 48, 76, 95), width=3)
    composite(draw_google_g_and_handshake, blur=3)

    def draw_meet_and_artifacts(ld):
        # Google Meet tile stack and export cards at top.
        ld.rounded_rectangle([(210, 165), (520, 282)], radius=22, fill=(25, 45, 84, 120), outline=(80, 220, 180, 85), width=3)
        for i, (x, y) in enumerate([(235, 190), (330, 190), (425, 190)]):
            ld.rounded_rectangle([(x, y), (x+70, y+54)], radius=12, fill=(70+i*45, 125+i*25, 210-i*20, 95))
            ld.ellipse([(x+22, y+12), (x+48, y+38)], fill=(230, 245, 255, 105))
        ld.rounded_rectangle([(615, 170), (790, 280)], radius=18, fill=(235, 245, 255, 54), outline=(170, 230, 255, 75), width=2)
        for y in [197, 225, 253]:
            ld.line([(640, y), (765, y)], fill=(210, 235, 255, 80), width=4)
        ld.rounded_rectangle([(850, 170), (1055, 280)], radius=18, fill=(235, 245, 255, 48), outline=(255, 210, 120, 70), width=2)
        for i in range(4):
            ld.ellipse([(878+i*38, 210), (900+i*38, 232)], fill=(255, 210, 120, 95))
    composite(draw_meet_and_artifacts, blur=2)

    def draw_connector_icons(ld):
        # Claude personal-app connectors around the table: music, car, groceries, travel, tax.
        icons = [
            (245, 850, (92, 220, 130), "music"),
            (405, 880, (95, 185, 255), "car"),
            (565, 865, (255, 185, 80), "cart"),
            (730, 880, (180, 140, 255), "pin"),
            (895, 865, (255, 125, 165), "tax"),
            (1060, 850, (105, 240, 215), "node"),
        ]
        for x, y, col, kind in icons:
            ld.line([(cx, cy+120), (x, y)], fill=(col[0], col[1], col[2], 45), width=3)
            ld.rounded_rectangle([(x-48, y-48), (x+48, y+48)], radius=22, fill=(18, 26, 58, 145), outline=(col[0], col[1], col[2], 135), width=3)
            if kind == "music":
                ld.ellipse([(x-12, y+10), (x+12, y+34)], fill=col+(170,)); ld.line([(x+10,y+18),(x+10,y-25)], fill=col+(170,), width=7); ld.line([(x+10,y-25),(x+32,y-18)], fill=col+(170,), width=6)
            elif kind == "car":
                ld.rounded_rectangle([(x-28,y-8),(x+28,y+18)], radius=10, fill=col+(150,)); ld.polygon([(x-18,y-8),(x-5,y-25),(x+20,y-25),(x+32,y-8)], fill=col+(115,)); ld.ellipse([(x-25,y+14),(x-9,y+30)], fill=(10,15,30,180)); ld.ellipse([(x+9,y+14),(x+25,y+30)], fill=(10,15,30,180))
            elif kind == "cart":
                ld.line([(x-26,y-20),(x-12,y+16),(x+26,y+16)], fill=col+(170,), width=6); ld.line([(x-16,y-4),(x+26,y-4)], fill=col+(135,), width=5); ld.ellipse([(x-12,y+22),(x+2,y+36)], fill=col+(160,)); ld.ellipse([(x+18,y+22),(x+32,y+36)], fill=col+(160,))
            elif kind == "pin":
                ld.ellipse([(x-20,y-30),(x+20,y+10)], outline=col+(180,), width=7); ld.polygon([(x-10,y+4),(x+10,y+4),(x,y+34)], fill=col+(160,)); ld.ellipse([(x-7,y-17),(x+7,y-3)], fill=col+(180,))
            elif kind == "tax":
                ld.rounded_rectangle([(x-24,y-30),(x+24,y+30)], radius=8, outline=col+(170,), width=5); ld.line([(x-12,y-8),(x+12,y-8)], fill=col+(150,), width=4); ld.line([(x-12,y+8),(x+12,y+8)], fill=col+(150,), width=4)
            else:
                for dx, dy in [(-18,-12),(18,-12),(0,20)]: ld.ellipse([(x+dx-9,y+dy-9),(x+dx+9,y+dy+9)], fill=col+(170,))
                ld.line([(x-10,y-8),(x+10,y-8),(x,y+12),(x-10,y-8)], fill=col+(115,), width=4)
    composite(draw_connector_icons, blur=2)

    def draw_comfy_nodes(ld):
        # Distinct ComfyUI-style node graph on lower right.
        nodes = [(935, 715, 110, 48), (1080, 775, 120, 50), (990, 840, 130, 50), (1180, 690, 100, 46)]
        for x,y,w,h in nodes:
            ld.rounded_rectangle([(x,y),(x+w,y+h)], radius=13, fill=(22, 30, 64, 135), outline=(255, 145, 80, 105), width=3)
            ld.ellipse([(x+12,y+16),(x+26,y+30)], fill=(255, 145, 80, 150))
            ld.line([(x+38,y+18),(x+w-14,y+18)], fill=(230, 210, 180, 75), width=4)
            ld.line([(x+38,y+32),(x+w-34,y+32)], fill=(230, 210, 180, 48), width=3)
        for (x1,y1,w1,h1),(x2,y2,w2,h2) in zip(nodes, nodes[1:]):
            ld.line([(x1+w1,y1+h1/2),(x2,y2+h2/2)], fill=(255, 145, 80, 75), width=5)
    composite(draw_comfy_nodes, blur=2)

    def draw_focus_glow(ld):
        ld.ellipse([(cx-430, cy-310), (cx+430, cy+310)], fill=(80, 180, 255, 18))
        ld.ellipse([(cx-260, cy-190), (cx+260, cy+190)], fill=(255, 210, 120, 20))
    composite(draw_focus_glow, blur=45)

    return img
