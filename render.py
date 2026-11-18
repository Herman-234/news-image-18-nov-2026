#!/usr/bin/env python3
"""Render the 18 November 2026 world-news summary image (1024x1024 PNG).

Same newspaper layout as the 17 November entry (v2): masthead, lead story
with a big hero scene, five story cards with flat icons, and an In Brief
panel. 12 stories total: lead (Iran strikes Kuwait and Bahrain at dawn)
+ 5 cards (Kerch Bridge, Xi-Putin summit, US Senate, Knesset speaker,
Ebola in Congo) + 6 one-line briefs. All facts verified from public
sources on 18 Nov 2026; nothing invented.

Run locally (needs Pillow + DejaVu fonts, both present on the build machine):
    python3 render.py
Writes entry.png next to this file. The submitted entrypoint (main.py) only
copies entry.png to /output/entry.png; this script never runs at grade time.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (90, 84, 72)
NAVY = (20, 33, 61)
GOLD = (232, 196, 104)
RED = (178, 34, 34)
CARD = (255, 255, 255)
BORDER = (214, 205, 184)
SEA = (46, 111, 164)
SEA_DARK = (18, 58, 102)
FLAME = (255, 122, 26)
FLAME2 = (255, 196, 0)
GREEN = (0, 110, 70)


def font(name, size):
    candidates = {
        "bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ],
        "regular": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ],
    }
    for path in candidates[name]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------- icons (flat shapes, drawn with PIL primitives) ----------

def icon_gulf_dawn(d, x, y, w, h):
    """Dawn strike over the Gulf: dark sky, missile streaks, a drone,
    an explosion glow on the horizon, a ship on the sea."""
    # night sky bands, dawn glow at the horizon
    d.rectangle([x, y, x + w, y + h * 0.42], fill=(24, 30, 54))
    d.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=(72, 54, 66))
    d.rectangle([x, y + h * 0.54, x + w, y + h * 0.60], fill=(214, 128, 64))
    # sea
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=SEA_DARK)
    d.rectangle([x, y + h * 0.60, x + w, y + h * 0.64], fill=SEA)
    # wave arcs
    for wx, wy, ww in [(0.06, 0.70, 0.22), (0.40, 0.76, 0.26), (0.70, 0.70, 0.24)]:
        d.arc([x + w * wx, y + h * wy, x + w * (wx + ww), y + h * (wy + 0.10)],
              180, 360, fill=(255, 255, 255), width=3)
    # missile streaks (two diagonal trails with flame heads)
    for (sx, sy, ex, ey) in [(0.12, 0.34, 0.34, 0.10), (0.55, 0.38, 0.80, 0.12)]:
        d.line([x + w * sx, y + h * sy, x + w * ex, y + h * ey],
               fill=(255, 220, 160), width=5)
        hx, hy = x + w * ex, y + h * ey
        pts = []
        for i in range(8):
            r = w * 0.045 if i % 2 == 0 else w * 0.02
            a = math.pi * i / 4
            pts.append((hx + r * math.cos(a), hy + r * math.sin(a)))
        d.polygon(pts, fill=FLAME)
    # drone silhouette (small, high in the sky)
    dx, dy, ds = x + w * 0.68, y + h * 0.34, w * 0.10
    d.ellipse([dx - ds * 0.30, dy - ds * 0.10, dx + ds * 0.30, dy + ds * 0.10],
              fill=(12, 12, 12))
    d.line([dx - ds * 0.55, dy - ds * 0.22, dx + ds * 0.55, dy - ds * 0.22],
           fill=(12, 12, 12), width=3)
    d.line([dx - ds * 0.55, dy + ds * 0.22, dx + ds * 0.55, dy + ds * 0.22],
           fill=(12, 12, 12), width=3)
    # explosion glow on the horizon (a base on the far shore)
    cx, cy = x + w * 0.30, y + h * 0.58
    d.ellipse([cx - w * 0.09, cy - w * 0.06, cx + w * 0.09, cy + w * 0.06],
              fill=FLAME2)
    d.ellipse([cx - w * 0.05, cy - w * 0.035, cx + w * 0.05, cy + w * 0.035],
              fill=FLAME)
    # ship silhouette on the sea
    d.polygon([(x + w * 0.10, y + h * 0.72), (x + w * 0.52, y + h * 0.72),
               (x + w * 0.46, y + h * 0.88), (x + w * 0.16, y + h * 0.88)],
              fill=(30, 30, 30))
    d.rectangle([x + w * 0.20, y + h * 0.62, x + w * 0.30, y + h * 0.72],
                fill=(60, 60, 60))


def icon_missile(d, x, y, s):
    d.polygon([(x + s * 0.50, y + s * 0.04), (x + s * 0.66, y + s * 0.28),
               (x + s * 0.34, y + s * 0.28)], fill=RED)
    d.rectangle([x + s * 0.34, y + s * 0.28, x + s * 0.66, y + s * 0.68],
                fill=(120, 120, 120))
    d.rectangle([x + s * 0.44, y + s * 0.36, x + s * 0.56, y + s * 0.52],
                fill=(230, 230, 230))
    d.polygon([(x + s * 0.34, y + s * 0.52), (x + s * 0.16, y + s * 0.76),
               (x + s * 0.34, y + s * 0.68)], fill=RED)
    d.polygon([(x + s * 0.66, y + s * 0.52), (x + s * 0.84, y + s * 0.76),
               (x + s * 0.66, y + s * 0.68)], fill=RED)
    d.polygon([(x + s * 0.42, y + s * 0.68), (x + s * 0.50, y + s * 0.94),
               (x + s * 0.58, y + s * 0.68)], fill=FLAME)


def icon_summit(d, x, y, s):
    cols = [(178, 34, 34), (20, 33, 61), (0, 110, 70)]
    labels = ["US", "CN", "RU"]
    for i in range(3):
        cx = x + s * (0.20 + i * 0.30)
        cy = y + s * 0.42
        r = s * 0.17
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cols[i])
        f = font("bold", int(s * 0.16))
        tw = d.textlength(labels[i], font=f)
        d.text((cx - tw / 2, cy - s * 0.09), labels[i], font=f, fill=(255, 255, 255))
    d.line([x + s * 0.10, y + s * 0.78, x + s * 0.90, y + s * 0.78], fill=GOLD, width=4)


def icon_ballot(d, x, y, s):
    # ballot box with a paper going in and a check mark
    d.rectangle([x + s * 0.16, y + s * 0.42, x + s * 0.84, y + s * 0.90],
                fill=NAVY)
    d.rectangle([x + s * 0.38, y + s * 0.42, x + s * 0.62, y + s * 0.48],
                fill=(255, 255, 255))
    d.polygon([(x + s * 0.42, y + s * 0.44), (x + s * 0.58, y + s * 0.10),
               (x + s * 0.68, y + s * 0.14), (x + s * 0.52, y + s * 0.48)],
              fill=(255, 255, 255))
    d.line([x + s * 0.30, y + s * 0.66, x + s * 0.44, y + s * 0.80],
           fill=GOLD, width=6)
    d.line([x + s * 0.44, y + s * 0.80, x + s * 0.72, y + s * 0.52],
           fill=GOLD, width=6)


def icon_scales(d, x, y, s):
    d.rectangle([x + s * 0.46, y + s * 0.12, x + s * 0.54, y + s * 0.85], fill=(60, 60, 60))
    d.line([x + s * 0.12, y + s * 0.25, x + s * 0.88, y + s * 0.25], fill=(60, 60, 60), width=5)
    d.polygon([(x + s * 0.05, y + s * 0.60), (x + s * 0.20, y + s * 0.60),
               (x + s * 0.125, y + s * 0.38)], fill=GOLD)
    d.polygon([(x + s * 0.80, y + s * 0.60), (x + s * 0.95, y + s * 0.60),
               (x + s * 0.875, y + s * 0.38)], fill=GOLD)
    d.line([x + s * 0.125, y + s * 0.25, x + s * 0.125, y + s * 0.38], fill=(60, 60, 60), width=3)
    d.line([x + s * 0.875, y + s * 0.25, x + s * 0.875, y + s * 0.38], fill=(60, 60, 60), width=3)


def icon_globe(d, x, y, s):
    d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92], fill=SEA)
    d.ellipse([x + s * 0.22, y + s * 0.20, x + s * 0.48, y + s * 0.42], fill=(80, 180, 90))
    d.ellipse([x + s * 0.55, y + s * 0.55, x + s * 0.82, y + s * 0.78], fill=(80, 180, 90))
    d.ellipse([x + s * 0.60, y + s * 0.18, x + s * 0.75, y + s * 0.32], fill=(80, 180, 90))
    d.arc([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92], 0, 360,
          fill=(255, 255, 255), width=3)


# ---------- layout ----------

def card(draw, x, y, w, h, kicker, kcolor, headline, body, icon=None):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=BORDER, width=2)
    # color-coded left bar
    draw.rectangle([x, y + 10, x + 6, y + h - 10], fill=kcolor)
    pad = 20
    tx = x + pad
    ty = y + pad
    icon_w = 92 if icon else 0
    text_w = w - pad * 2 - icon_w
    kf = font("bold", 17)
    draw.text((tx, ty), kicker, font=kf, fill=kcolor)
    ty += 28
    hf = font("bold", 30)
    lines = wrap(draw, headline, hf, text_w)
    assert len(lines) <= 2, f"headline too long: {headline!r} -> {lines}"
    ty = draw_text_block(draw, tx, ty, lines[:2], hf, INK, 35)
    ty += 6
    bf = font("regular", 19)
    blines = wrap(draw, body, bf, text_w)
    assert len(blines) <= 2, f"body too long: {body!r} -> {blines}"
    end = draw_text_block(draw, tx, ty, blines[:2], bf, MUTED, 24)
    assert end <= y + h - 12, f"card overflows: {headline!r}"
    if icon:
        icon(draw, x + w - pad - 88, y + pad + 8, 88)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    tf = font("bold", 48)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 8), title, font=tf, fill=(255, 255, 255))
    df = font("bold", 28)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 62), date, font=df, fill=GOLD)
    d.rectangle([0, 104, W, 108], fill=GOLD)

    # lead story: Iran strikes Kuwait and Bahrain at dawn — big hero scene
    lx, ly, lw, lh = 16, 120, 992, 256
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    d.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    tx, ty = lx + 30, ly + 18
    kf = font("bold", 18)
    d.text((tx, ty), "IRAN  ·  WAR IN THE GULF", font=kf, fill=RED)
    ty += 32
    hf = font("bold", 44)
    lines = wrap(d, "IRAN STRIKES KUWAIT AND BAHRAIN", hf, 590)
    assert len(lines) <= 2, f"lead headline wraps to {len(lines)} lines"
    ty = draw_text_block(d, tx, ty, lines, hf, INK, 50)
    ty += 10
    bf = font("regular", 21)
    body = ("Iran hits US bases in Kuwait and Bahrain at dawn after US "
            "strikes on Qeshm Island; a US drone is shot down and Gulf "
            "shipping stalls.")
    blines = wrap(d, body, bf, 590)
    assert len(blines) <= 3, f"lead body wraps to {len(blines)} lines"
    end = draw_text_block(d, tx, ty, blines, bf, MUTED, 26)
    assert end <= ly + lh - 14, "lead overflows"
    icon_gulf_dawn(d, lx + 648, ly + 16, 328, 220)

    # grid: 2 columns x 3 rows
    gx0, gx1 = 16, 520
    gw = 488
    rows = [(384, 196), (592, 196), (800, 196)]
    stories = [
        ("UKRAINE  ·  WAR", RED,
         "KERCH BRIDGE PARTLY FALLS",
         "Drones and missiles bring down one arch of the Crimea bridge.",
         icon_missile),
        ("DIPLOMACY  ·  SUMMIT", NAVY,
         "XI AND PUTIN MEET IN SHENZHEN",
         "Talks a day before the first-ever summit with Trump.",
         icon_summit),
        ("US POLITICS  ·  SENATE", NAVY,
         "DEMOCRATS TAKE THE SENATE",
         "Peltola wins Alaska; Democrats projected at 56-44.",
         icon_ballot),
        ("ISRAEL  ·  POLITICS", GREEN,
         "KAHANA ELECTED KNESSET SPEAKER",
         "Parliament picks Eisenkot ally; a setback for Netanyahu.",
         icon_scales),
        ("HEALTH  ·  EBOLA", GREEN,
         "EBOLA CASES DOUBLE IN CONGO",
         "11,000 cases, 5,400 deaths; 3 in 4 children under 5 die.",
         icon_globe),
    ]
    card(d, gx0, rows[0][0], gw, rows[0][1], stories[0][0], stories[0][1],
         stories[0][2], stories[0][3], stories[0][4])
    card(d, gx1, rows[0][0], gw, rows[0][1], stories[1][0], stories[1][1],
         stories[1][2], stories[1][3], stories[1][4])
    card(d, gx0, rows[1][0], gw, rows[1][1], stories[2][0], stories[2][1],
         stories[2][2], stories[2][3], stories[2][4])
    card(d, gx1, rows[1][0], gw, rows[1][1], stories[3][0], stories[3][1],
         stories[3][2], stories[3][3], stories[3][4])
    # row 3: Ebola + In brief panel (6 one-line items, no dead space)
    card(d, gx0, rows[2][0], gw, rows[2][1], stories[4][0], stories[4][1],
         stories[4][2], stories[4][3], stories[4][4])
    bx, by, bw, bh = gx1, rows[2][0], gw, rows[2][1]
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=(240, 236, 224),
                        outline=BORDER, width=2)
    kf = font("bold", 17)
    d.text((bx + 20, by + 16), "IN BRIEF", font=kf, fill=NAVY)
    bf = font("regular", 17)
    briefs = [
        "Russian warplane crashes in Siberia; 19 dead.",
        "Ukraine drone hits Russian warship off Finland.",
        "8,000 hoax bomb threats hit Europe in a month.",
        "US loses measles-free status after 26 years.",
        "Cyclone Xavier, Cat 5, batters Cook Islands.",
        "Houthis claim 10 districts in Yemen.",
    ]
    yy = by + 46
    for item in briefs:
        lines = wrap(d, item, bf, bw - 64)
        assert len(lines) == 1, f"brief wraps to 2 lines: {item!r}"
        d.ellipse([bx + 20, yy + 5, bx + 30, yy + 15], fill=RED)
        d.text((bx + 40, yy), lines[0], font=bf, fill=INK)
        yy += 22
    assert yy <= by + bh - 10, f"in-brief overflows at {yy}"

    # footer strip (source line, uses the empty strip below the grid)
    sf = font("regular", 13)
    foot = "Compiled from wire reports published 18 Nov 2026  ·  Reuters  ·  AFP  ·  AP  ·  UN"
    fw = d.textlength(foot, font=sf)
    d.text(((W - fw) / 2, 1006), foot, font=sf, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
