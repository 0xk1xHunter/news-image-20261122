#!/usr/bin/env python3
"""Draw "The World Today" — Sunday 22 November 2026.

A newspaper front page summarising the day's world news, rendered with PIL.
Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
Run:  python3 draw.py   (writes entry.png next to this file)
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (250, 248, 240)
INK = (18, 18, 18)
RULE = (18, 18, 18)
ACCENT = (158, 24, 24)
MUTED = (90, 86, 78)
TICKER_BG = (18, 18, 18)
TICKER_FG = (250, 248, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 66)
F_DATE = font("DejaVuSans.ttf", 21)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 40)
F_LEAD_BODY = font("DejaVuSerif.ttf", 21)
F_KICKER = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSerif-Bold.ttf", 24)
F_BODY = font("DejaVuSerif.ttf", 18)
F_SOURCE = font("DejaVuSans.ttf", 15)
F_TICKER = font("DejaVuSans-Bold.ttf", 17)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using the real rendered width of each word."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text; return the y coordinate just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin
    right = W - mx

    # ---- Masthead ----
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_MASTHEAD)
    d.text(((W - tw) / 2, 26), title, font=F_MASTHEAD, fill=INK)
    date = "SUNDAY 22 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 108), date, font=F_DATE, fill=MUTED)
    rule(d, mx, 142, right, 4)
    rule(d, mx, 150, right, 1)

    # ---- Lead story: COP31 ----
    y = 168
    d.text((mx, y), "CLIMATE  •  ANTALYA", font=F_KICKER, fill=ACCENT)
    y += 26
    y = draw_para(d, mx, y,
                  "COP31 talks run into a second day of overtime as a new draft lands",
                  F_LEAD_HEAD, right - mx, 48)
    y += 6
    y = draw_para(d, mx, y,
                  "Negotiators in Antalya receive a third draft text early on Sunday. "
                  "It still names no fossil-fuel phase-out, but concedes the 1.5°C goal "
                  "may be missed. Delegates have until 03:00 GMT to object, with an "
                  "approval session set for 06:00 GMT.",
                  F_LEAD_BODY, right - mx, 28)
    y += 4
    d.text((mx, y), "Sources: BBC, Reuters", font=F_SOURCE, fill=MUTED)
    y += 30
    rule(d, mx, y, right, 2)

    # ---- Four panels, 2 x 2 ----
    gap = 24
    col_w = (right - mx - gap) // 2
    row_h = 208
    top = y + 18
    panels = [
        ("MIDDLE EAST", "Bahrain blames Iran as tankers are hit",
         "Bahrain says Iran set fire to a civilian industrial site and two "
         "tankers were struck in the Strait of Hormuz. Washington denies an "
         "F-16 was hit.", "Reuters"),
        ("INDIA", "Manipur liquor toll rises to 16",
         "About 600 people are in hospital in Chandel after suspected "
         "spurious liquor. Six people have been arrested and a probe ordered.",
         "Xinhua"),
        ("BALTIC SEA", "Sanctioned ship Sparta II still burning",
         "The Russian cargo ship, hit by a suspected drone strike, drifts in "
         "Finnish waters. All 16 crew are safe and a tow is promised overnight.",
         "Reuters, Yle"),
        ("YEMEN", "Saudi jets strike Hodeidah port",
         "Warplanes hit the Red Sea port as the missile war with Riyadh "
         "escalates. The Houthis count 71 strikes in 24 hours.",
         "al-Masirah"),
    ]
    for i, (kicker, head, body, src) in enumerate(panels):
        px = mx + (i % 2) * (col_w + gap)
        py = top + (i // 2) * (row_h + 14)
        d.text((px, py), kicker, font=F_KICKER, fill=ACCENT)
        hy = py + 26
        hy = draw_para(d, px, hy, head, F_HEAD, col_w, 29)
        hy += 4
        hy = draw_para(d, px, hy, body, F_BODY, col_w, 23)
        d.text((px, py + row_h - 20), "Source: " + src,
               font=F_SOURCE, fill=MUTED)
        if i % 2 == 0:
            d.line([(px + col_w + gap // 2, py),
                    (px + col_w + gap // 2, py + row_h - 8)],
                   fill=(200, 196, 186), width=1)

    # ---- Ticker ----
    ty = top + 2 * row_h + 14 + 16
    d.rectangle([mx, ty, right, ty + 56], fill=TICKER_BG)
    ticker = ("ST JOHNS RIVER BREAKS A 73-YEAR FLOOD RECORD"
              "   •   UN TALKS ON AUTONOMOUS WEAPONS")
    d.text((mx + 16, ty + 17), ticker, font=F_TICKER, fill=TICKER_FG)
    d.text((mx, ty + 66), "One image. One day. The world, 22 November 2026.",
           font=F_SOURCE, fill=MUTED)

    img.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
