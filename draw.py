#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Run: python3 draw.py  -> writes entry.png beside this file.
Pure PIL drawing, no network, no downloaded images, deterministic.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (24, 22, 18)
RED = (178, 34, 28)
GREY = (92, 88, 80)
RULE = (24, 22, 18)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap, returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(d, text, fnt, max_w)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def flame(d, cx, base_y, h, w, colors):
    """Layered teardrop flame centred at cx, base at base_y."""
    for i, col in enumerate(colors):
        f = 1.0 - i * 0.28
        hh, ww = h * f, w * f
        pts = []
        for a in range(0, 361, 12):
            r = math.radians(a)
            px = cx + math.sin(r) * ww * 0.5 * (1 - 0.35 * math.cos(r))
            py = base_y - hh * (0.5 + 0.5 * math.cos(r)) * (1 if math.cos(r) >= 0 else 0.55)
            pts.append((px, py))
        d.polygon(pts, fill=col)
        d.ellipse([cx - ww * 0.28, base_y - hh * 0.55, cx + ww * 0.28, base_y - hh * 0.05],
                  fill=colors[-1])


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)
    x0, x1 = 34, W - 34

    # ---- masthead ----
    y = 34
    d.text((W // 2, y), "THE WORLD IN ONE PAGE", font=SERIF_B(50),
           fill=INK, anchor="ma")
    y = 100
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 9
    d.text((W // 2, y), "THURSDAY, 26 NOVEMBER 2026", font=SANS_B(20),
           fill=RED, anchor="ma")
    y += 28
    d.text((W // 2, y), "THE DAY'S WORLD NEWS  •  ONE PAGE  •  ALL THE STORIES THAT MATTERED",
           font=SANS(13), fill=GREY, anchor="ma")
    y += 22
    d.line([(x0, y), (x1, y)], fill=RULE, width=4)

    # ---- lead story ----
    y += 14
    d.text((x0, y), "TRADE", font=SANS_B(16), fill=RED)
    y += 24
    y = draw_wrapped(d, x0, y, "US proposes new tariffs of up to 35% on 14 trading partners",
                     SERIF_B(36), INK, x1 - x0, 42)
    y += 5
    y = draw_wrapped(d, x0, y,
                     "China, the European Union, Japan and India are among those named, as "
                     "Washington cites excess manufacturing capacity. Markets rattled.",
                     SERIF(17), (60, 56, 48), x1 - x0, 23)
    y += 10

    # ---- lead illustration: Cairo tanker fire ----
    px0, py0, px1, py1 = x0, y, x1, y + 220
    # night sky bands
    for i in range(py1 - py0):
        t = i / (py1 - py0)
        r = int(38 + 30 * t)
        g = int(44 + 30 * t)
        b = int(66 + 40 * t)
        d.line([(px0, py0 + i), (px1, py0 + i)], fill=(r, g, b))
    # stars
    for sx, sy in [(90, 22), (210, 48), (330, 18), (470, 40), (620, 24),
                   (760, 46), (900, 20), (150, 66), (540, 64), (830, 66)]:
        d.ellipse([px0 + sx - 2, py0 + sy - 2, px0 + sx + 2, py0 + sy + 2],
                  fill=(240, 235, 210))
    # city silhouette
    for bx, bw, bh in [(0, 90, 40), (95, 60, 60), (160, 110, 35), (275, 70, 68),
                       (350, 90, 45), (700, 80, 62), (785, 110, 40), (900, 60, 55)]:
        d.rectangle([px0 + bx, py1 - 70 - bh, px0 + bx + bw, py1 - 70],
                    fill=(30, 34, 52))
    # road
    d.rectangle([px0, py1 - 70, px1, py1 - 40], fill=(52, 50, 48))
    d.line([(px0, py1 - 55), (px1, py1 - 55)], fill=(220, 200, 90), width=3)
    for lx in range(0, 964, 64):
        d.line([(px0 + lx, py1 - 55), (px0 + lx + 32, py1 - 55)],
               fill=(248, 244, 232), width=3)
    # tanker truck
    tx, ty = px0 + 330, py1 - 70  # ground line under wheels
    d.rounded_rectangle([tx, ty - 78, tx + 300, ty - 8], radius=18,
                        fill=(200, 196, 188), outline=(40, 38, 34), width=3)
    d.rounded_rectangle([tx + 305, ty - 66, tx + 392, ty - 8], radius=8,
                        fill=(178, 34, 28), outline=(40, 38, 34), width=3)
    d.rectangle([tx + 318, ty - 56, tx + 352, ty - 30], fill=(180, 220, 235),
                outline=(40, 38, 34), width=2)
    for wx in (tx + 40, tx + 250, tx + 335):
        d.ellipse([wx, ty - 16, wx + 34, ty + 18], fill=(24, 22, 18))
        d.ellipse([wx + 10, ty - 6, wx + 24, ty + 8], fill=(120, 116, 110))
    # flames over the tank (kept inside the panel: base ty-76, max height 74)
    flame(d, tx + 120, ty - 76, 52, 62, [(255, 120, 20), (255, 170, 30), (255, 220, 80)])
    flame(d, tx + 210, ty - 76, 74, 78, [(255, 100, 10), (255, 150, 25), (255, 210, 70)])
    flame(d, tx + 60, ty - 76, 40, 48, [(255, 130, 25), (255, 180, 40), (255, 225, 90)])
    # smoke puffs drifting above the flames, inside the panel
    for sx, sy, sr in [(tx + 130, py0 + 26, 22), (tx + 180, py0 + 14, 26),
                       (tx + 235, py0 + 28, 20), (tx + 95, py0 + 38, 16),
                       (tx + 275, py0 + 40, 15)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 118, 116))
    # caption bar
    d.rectangle([px0, py1 - 40, px1, py1], fill=(24, 22, 18))
    d.text((px0 + 12, py1 - 35),
           "A fuel tanker burns on Cairo's ring road after a crash. At least 31 people",
           font=SANS_B(15), fill=(248, 244, 232))
    d.text((px0 + 12, py1 - 20),
           "were killed and about 21 hurt, Egypt's health ministry said.",
           font=SANS(15), fill=(220, 214, 200))
    y = py1 + 14
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)

    # ---- middle grid: 6 stories ----
    y += 12
    d.text((x0, y), "MORE FROM THE DAY", font=SANS_B(16), fill=RED)
    y += 26
    stories = [
        ("HOUTHI STRIKES",
         "Houthis attack Saudi ports and the Ras Tanura refinery.",
         "rocket"),
        ("US WARNS ON IRAN",
         "Washington tells its citizens to leave Iran as war fears grow.",
         "plane"),
        ("GAZA STRIKE",
         "Israeli strike kills Hamas security chief Mohammed Abu al-Ouf.",
         "burst"),
        ("ONE MILLION SATELLITES",
         "FCC approves SpaceX plan for up to one million satellites.",
         "satellite"),
        ("FIRST ABOARD TIANGONG",
         "Pakistan's Muhammad Zeeshan Ali is the first foreign astronaut aboard "
         "China's Tiangong station.",
         "helmet"),
        ("HOSTAGES FREED",
         "Police free 76 supermarket hostages in Cartagena after a 17-hour siege.",
         "store"),
    ]
    col_w = (x1 - x0 - 2 * 24) // 3
    row_h = 112
    for i, (head, body, icon) in enumerate(stories):
        cx = x0 + (i % 3) * (col_w + 24)
        cy = y + (i // 3) * (row_h + 14)
        draw_icon(d, cx, cy, icon)
        tx = cx + 76
        tw = col_w - 76
        yy = draw_wrapped(d, tx, cy + 2, head, SANS_B(17), INK, tw, 21)
        draw_wrapped(d, tx, yy + 2, body, SANS(14), (60, 56, 48), tw, 18)
    y += 2 * row_h + 14 + 6
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)

    # ---- in brief strip ----
    y += 12
    d.text((x0, y), "IN BRIEF", font=SANS_B(16), fill=RED)
    y += 26
    briefs = [
        ("MARKETS",
         "Nasdaq falls about 4% as an AI sell-off and tariff worries hit Wall Street; "
         "the Bank of Korea raises its rate to 3.25%."),
        ("PARADE",
         "Macy's postpones its 100th Thanksgiving Day Parade to Saturday over severe "
         "weather."),
        ("INDONESIA",
         "A coal mine flood in Indonesia leaves 13 people dead and 13 missing."),
    ]
    for i, (head, body) in enumerate(briefs):
        cx = x0 + i * (col_w + 24)
        yy = draw_wrapped(d, cx, y, head, SANS_B(15), INK, col_w, 18)
        draw_wrapped(d, cx, yy + 2, body, SANS(14), (60, 56, 48), col_w, 17)
    y += 80
    d.line([(x0, y), (x1, y)], fill=RULE, width=1)
    y += 8
    d.text((W // 2, y), "Compiled from wire reports  •  Thursday, 26 November 2026",
           font=SANS(13), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


def draw_icon(d, x, y, kind):
    """Small 64x64 drawn icon in a bordered box."""
    d.rectangle([x, y, x + 64, y + 64], outline=INK, width=2, fill=(238, 232, 214))
    cx, cy = x + 32, y + 32
    if kind == "rocket":
        d.polygon([(cx, cy - 24), (cx + 12, cy + 8), (cx + 6, cy + 16),
                   (cx - 6, cy + 16), (cx - 12, cy + 8)], fill=RED)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(248, 244, 232))
        d.polygon([(cx - 4, cy + 16), (cx, cy + 26), (cx + 4, cy + 16)],
                  fill=(255, 170, 30))
    elif kind == "plane":
        d.polygon([(cx - 26, cy + 2), (cx + 26, cy + 2), (cx + 30, cy + 8),
                   (cx - 26, cy + 8)], fill=(40, 70, 120))
        d.polygon([(cx + 2, cy - 20), (cx + 10, cy - 20), (cx + 8, cy + 2),
                   (cx - 2, cy + 2)], fill=(40, 70, 120))
        d.polygon([(cx - 14, cy + 8), (cx - 8, cy + 8), (cx - 20, cy + 20),
                   (cx - 24, cy + 20)], fill=(40, 70, 120))
    elif kind == "burst":
        for a in range(0, 360, 30):
            r = math.radians(a)
            d.line([(cx, cy), (cx + 26 * math.cos(r), cy + 26 * math.sin(r))],
                   fill=(255, 170, 30), width=5)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)
    elif kind == "satellite":
        d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=(60, 60, 66),
                    outline=INK, width=2)
        d.rectangle([cx - 28, cy - 5, cx - 10, cy + 5], fill=(40, 70, 120),
                    outline=INK, width=1)
        d.rectangle([cx + 10, cy - 5, cx + 28, cy + 5], fill=(40, 70, 120),
                    outline=INK, width=1)
        d.line([(cx - 8, cy - 8), (cx - 20, cy - 20)], fill=INK, width=2)
        d.ellipse([cx - 23, cy - 23, cx - 17, cy - 17], fill=RED)
    elif kind == "helmet":
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(248, 244, 232),
                  outline=INK, width=3)
        d.ellipse([cx - 13, cy - 10, cx + 13, cy + 12], fill=(140, 190, 220),
                  outline=INK, width=2)
        d.arc([cx - 22, cy - 22, cx + 22, cy + 22], 200, 340, fill=RED, width=4)
    elif kind == "store":
        d.rectangle([cx - 24, cy - 14, cx + 24, cy + 22], fill=(120, 90, 60),
                    outline=INK, width=2)
        d.polygon([(cx - 28, cy - 14), (cx + 28, cy - 14), (cx + 22, cy - 24),
                   (cx - 22, cy - 24)], fill=RED)
        d.rectangle([cx - 6, cy + 4, cx + 6, cy + 22], fill=(248, 244, 232),
                    outline=INK, width=1)
        d.rectangle([cx - 18, cy - 6, cx - 10, cy + 2], fill=(180, 220, 235))
        d.rectangle([cx + 10, cy - 6, cx + 18, cy + 2], fill=(180, 220, 235))


if __name__ == "__main__":
    main()
