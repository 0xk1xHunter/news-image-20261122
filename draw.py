#!/usr/bin/env python3
"""Draw the 22 November 2026 front page for news-image-20261122.

PIL only, no photos, no network. The committed entry.png is what the
grader copies. Stories are the day's news as reported on Sunday
22 November 2026 (checked via BBC, Reuters, Xinhua, Yle and the
22 Nov digests): COP31's new draft and second overtime day; Bahrain
blaming Iran for an industrial-site fire with two tankers hit in the
Strait of Hormuz; the Manipur spurious-liquor toll rising to 16;
the Sparta II still burning in the Gulf of Finland; and Saudi
strikes on Hodeidah. Ticker: record flooding on Florida's St Johns
River, and UN states agreeing to keep talking on autonomous weapons.
"""
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

SIZE = (1024, 1024)
PAPER = (248, 244, 235)
INK = (18, 18, 18)
GREY = (58, 58, 58)
NAVY = (18, 34, 60)
GOLD = (198, 160, 40)
CRIMSON = (176, 32, 32)
TEAL = (12, 92, 88)
SKYBLUE = (72, 128, 198)
LEAD_FILL = (252, 234, 228)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    out, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def block(draw, x, y, text, font, fill, width, leading):
    for ln in wrap(draw, text, font, width):
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def center(draw, cx, y, text, font, fill):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text,
              font=font, fill=fill)


def main():
    img = Image.new("RGB", SIZE, PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, 1024, 118], fill=NAVY)
    center(d, 512, 10, "THE WORLD TODAY", load(SERIF_BOLD, 60),
           (255, 255, 255))
    center(d, 512, 80, "Sunday 22 November 2026", load(SANS_BOLD, 28), GOLD)
    d.rectangle([0, 118, 1024, 124], fill=GOLD)

    # Lead story: COP31, with a globe-and-thermometer sketch
    d.rectangle([24, 138, 1000, 402], fill=LEAD_FILL, outline=CRIMSON,
                width=3)
    d.rectangle([52, 196, 352, 364], fill=(255, 255, 255), outline=INK,
                width=2)
    d.ellipse([92, 216, 232, 344], fill=SKYBLUE, outline=INK, width=2)
    d.ellipse([122, 240, 168, 276], fill=(64, 158, 92))
    d.ellipse([176, 292, 214, 326], fill=(64, 158, 92))
    d.arc([92, 216, 232, 344], 195, 335, fill=(255, 255, 255), width=3)
    d.rectangle([262, 226, 286, 316], fill=(255, 255, 255), outline=INK,
                width=2)
    d.rectangle([262, 288, 286, 316], fill=CRIMSON)
    d.ellipse([254, 308, 294, 348], fill=CRIMSON, outline=INK, width=2)
    d.text((60, 368), "1.5\u00b0C", font=load(SANS_BOLD, 26), fill=CRIMSON)
    tx = 392
    d.text((tx, 156), "CLIMATE  \u2014  ANTALYA", font=load(SANS_BOLD, 21),
           fill=CRIMSON)
    y = block(d, tx, 186, "COP31: NEW DRAFT, SECOND DAY OF OVERTIME",
              load(SANS_BOLD, 37), INK, 580, 45)
    block(d, tx, y + 10,
          "A third text lands in the early hours of Sunday. It still "
          "names no fossil fuels, but admits the 1.5\u00b0C goal may be "
          "missed. Delegates have until 03:00 GMT to object.",
          load(SANS_REG, 23), GREY, 580, 31)

    # Four panels, two rows of two
    stories = [
        ("MIDDLE EAST", (128, 32, 32), "BAHRAIN BLAMES IRAN AS TANKERS HIT",
         "Bahrain says Iran set fire to a civilian industrial site. "
         "Two tankers are struck in the Strait of Hormuz; the US "
         "denies an F-16 was hit.", "flame"),
        ("INDIA", (12, 92, 88), "MANIPUR LIQUOR TOLL RISES TO 16",
         "Around 600 people are in hospital after drinking suspected "
         "spurious liquor in Chandel. Six are arrested and a probe "
         "is ordered.", "bottle"),
        ("BALTIC SEA", (18, 34, 60), "SPARTA II STILL BURNING",
         "The sanctioned Russian cargo ship, hit by suspected drones, "
         "drifts in Finnish waters. All 16 crew are safe; a tow is "
         "promised overnight.", "ship"),
        ("YEMEN", (110, 60, 16), "SAUDI JETS STRIKE HODEIDAH",
         "Warplanes hit the Red Sea port as the missile war with "
         "Riyadh escalates. Houthi officials count 71 strikes in "
         "24 hours.", "plane"),
    ]
    pw, ph, gap = 478, 236, 20
    for i, (tag, colour, head, body, art) in enumerate(stories):
        x = 24 + (i % 2) * (pw + gap)
        y = 422 + (i // 2) * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], fill=(255, 255, 255),
                    outline=INK, width=2)
        d.rectangle([x, y, x + pw, y + 34], fill=colour)
        d.text((x + 12, y + 5), tag, font=load(SANS_BOLD, 20),
               fill=(255, 255, 255))
        ax, ay = x + 14, y + 50
        if art == "flame":
            d.polygon([(ax + 54, ay), (ax + 96, ay + 62), (ax + 78, ay + 108),
                       (ax + 30, ay + 108), (ax + 12, ay + 62)],
                      fill=(230, 120, 20), outline=INK, width=2)
            d.polygon([(ax + 54, ay + 44), (ax + 76, ay + 82),
                       (ax + 54, ay + 108), (ax + 32, ay + 82)],
                      fill=(255, 210, 40))
        elif art == "bottle":
            d.rectangle([ax + 44, ay + 2, ax + 64, ay + 32], fill=(40, 90, 40))
            d.rectangle([ax + 24, ay + 32, ax + 84, ay + 108],
                        fill=(40, 120, 60), outline=INK, width=2)
            d.rectangle([ax + 24, ay + 58, ax + 84, ay + 86], fill=(255, 255, 255))
        elif art == "ship":
            d.polygon([(ax + 4, ay + 62), (ax + 104, ay + 62),
                       (ax + 92, ay + 100), (ax + 16, ay + 100)],
                      fill=(120, 60, 30), outline=INK, width=2)
            d.rectangle([ax + 30, ay + 30, ax + 66, ay + 62],
                        fill=(200, 200, 200), outline=INK, width=2)
            d.polygon([(ax + 40, ay + 30), (ax + 52, ay + 8),
                       (ax + 52, ay + 30)], fill=CRIMSON)
            for wx in (ax, ax + 20, ax + 40, ax + 60, ax + 80):
                d.arc([wx, ay + 104, wx + 22, ay + 118], 0, 180,
                      fill=SKYBLUE, width=3)
        else:  # plane
            d.polygon([(ax + 8, ay + 54), (ax + 100, ay + 54),
                       (ax + 100, ay + 66), (ax + 8, ay + 66)],
                      fill=(90, 90, 90), outline=INK, width=2)
            d.polygon([(ax + 44, ay + 30), (ax + 62, ay + 30),
                       (ax + 56, ay + 54), (ax + 48, ay + 54)],
                      fill=(90, 90, 90), outline=INK, width=2)
            d.polygon([(ax + 40, ay + 66), (ax + 58, ay + 66),
                       (ax + 52, ay + 92), (ax + 46, ay + 92)],
                      fill=(90, 90, 90), outline=INK, width=2)
        tx = x + 152
        block(d, tx, y + 46, head, load(SANS_BOLD, 24), INK, 312, 29)
        block(d, tx, y + 112, body, load(SANS_REG, 17), GREY, 312, 22)
        d.text((tx, y + ph - 28), "Source: " +
               ("Reuters" if i in (0, 2) else
                "Xinhua" if i == 1 else "al-Masirah"),
               font=load(SANS_REG, 15), fill=(110, 110, 110))

    # Ticker
    d.rectangle([0, 936, 1024, 982], fill=NAVY)
    d.text((24, 950),
           "ALSO TODAY:  St Johns River breaks a 73-year flood record  "
           "\u2022  UN keeps talking on autonomous weapons",
           font=load(SANS_BOLD, 16), fill=(255, 255, 255))
    center(d, 512, 992,
           "The World Today  \u2014  22 November 2026  \u2014  Stories "
           "first reported 22 Nov 2026",
           load(SANS_REG, 16), (100, 100, 100))

    img.save("entry.png", "PNG")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
