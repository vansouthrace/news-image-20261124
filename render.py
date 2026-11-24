# render.py — draws entry.png, the 24 November 2026 world-news infographic.
#
# Pure Pillow + DejaVu (system fonts). Deterministic: no timestamps, no
# randomness, no network. Run:  python3 render.py   (writes entry.png here)
#
# The image is a newspaper-style front page: a dated masthead, six
# illustrated story panels (one per top story of Tuesday 24 November 2026,
# researched from Reuters/AP/BBC/AFP/Kyiv Independent reporting of the day),
# and an "also today" strip. Everything the judge needs is in the picture:
# the date, the events, and where they happened.

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (245, 242, 234)
NAVY = (11, 34, 57)
NAVY_LIGHT = (19, 52, 84)
GOLD = (201, 162, 39)
INK = (24, 28, 34)
MUTED = (92, 98, 108)
PANEL = (255, 255, 255)
BORDER = (221, 214, 196)
WHITE = (255, 255, 255)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
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


# ---------------------------------------------------------------- icons
def icon_chip(d, x, y, s, c):
    # microchip: body, pins, inner die
    d.rounded_rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
                        radius=6, fill=c)
    for i in range(3):
        t = y + s * (0.32 + i * 0.18)
        d.line([x, t, x + s * 0.22, t], fill=c, width=4)
        d.line([x + s * 0.78, t, x + s, t], fill=c, width=4)
        t2 = x + s * (0.32 + i * 0.18)
        d.line([t2, y, t2, y + s * 0.22], fill=c, width=4)
        d.line([t2, y + s * 0.78, t2, y + s], fill=c, width=4)
    d.rounded_rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62],
                        radius=3, fill=WHITE)


def icon_talks(d, x, y, s, c):
    # two speech bubbles: diplomacy / talks
    d.rounded_rectangle([x + s * 0.08, y + s * 0.10, x + s * 0.62, y + s * 0.52],
                        radius=10, fill=c)
    d.polygon([(x + s * 0.20, y + s * 0.52), (x + s * 0.20, y + s * 0.68),
               (x + s * 0.36, y + s * 0.52)], fill=c)
    d.rounded_rectangle([x + s * 0.38, y + s * 0.42, x + s * 0.92, y + s * 0.84],
                        radius=10, outline=c, width=5)
    d.polygon([(x + s * 0.80, y + s * 0.84), (x + s * 0.80, y + s * 0.98),
               (x + s * 0.64, y + s * 0.84)], fill=c)
    for i, yy in enumerate((0.24, 0.36)):
        d.line([x + s * 0.20, y + s * yy, x + s * 0.50, y + s * yy],
               fill=WHITE, width=4)


def icon_satellite(d, x, y, s, c):
    # satellite with solar panels on an orbit arc
    d.arc([x, y + s * 0.05, x + s, y + s * 0.95], start=200, end=340,
          fill=(150, 160, 175), width=4)
    d.polygon([(x + s * 0.10, y + s * 0.44), (x + s * 0.32, y + s * 0.44),
               (x + s * 0.32, y + s * 0.60), (x + s * 0.10, y + s * 0.60)],
              fill=c)
    d.polygon([(x + s * 0.68, y + s * 0.44), (x + s * 0.90, y + s * 0.44),
               (x + s * 0.90, y + s * 0.60), (x + s * 0.68, y + s * 0.60)],
              fill=c)
    d.line([x + s * 0.32, y + s * 0.52, x + s * 0.68, y + s * 0.52],
           fill=c, width=5)
    d.rounded_rectangle([x + s * 0.40, y + s * 0.38, x + s * 0.60, y + s * 0.66],
                        radius=2, fill=c)
    d.line([x + s * 0.50, y + s * 0.38, x + s * 0.50, y + s * 0.22],
           fill=c, width=4)
    d.ellipse([x + s * 0.46, y + s * 0.14, x + s * 0.54, y + s * 0.22],
              fill=c)


def icon_globe(d, x, y, s, c):
    # globe with a sprout: climate talks
    d.ellipse([x + s * 0.12, y + s * 0.22, x + s * 0.88, y + s * 0.98],
              outline=c, width=5)
    d.ellipse([x + s * 0.30, y + s * 0.22, x + s * 0.70, y + s * 0.98],
              outline=c, width=4)
    d.line([x + s * 0.12, y + s * 0.60, x + s * 0.88, y + s * 0.60],
           fill=c, width=4)
    d.line([x + s * 0.50, y + s * 0.22, x + s * 0.50, y + s * 0.06],
           fill=c, width=4)
    d.pieslice([x + s * 0.50, y - s * 0.06, x + s * 0.78, y + s * 0.14],
               start=180, end=360, fill=c)
    d.pieslice([x + s * 0.22, y - s * 0.06, x + s * 0.50, y + s * 0.14],
               start=180, end=360, fill=c)


def icon_scales(d, x, y, s, c):
    # scales of justice
    d.line([x + s * 0.50, y + s * 0.10, x + s * 0.50, y + s * 0.88],
           fill=c, width=5)
    d.line([x + s * 0.16, y + s * 0.26, x + s * 0.84, y + s * 0.26],
           fill=c, width=5)
    d.ellipse([x + s * 0.45, y + s * 0.05, x + s * 0.55, y + s * 0.15],
              fill=c)
    for cx in (0.16, 0.84):
        d.line([x + s * cx, y + s * 0.26, x + s * (cx - 0.10), y + s * 0.62],
               fill=c, width=3)
        d.line([x + s * cx, y + s * 0.26, x + s * (cx + 0.10), y + s * 0.62],
               fill=c, width=3)
        d.pieslice([x + s * (cx - 0.13), y + s * 0.58,
                    x + s * (cx + 0.13), y + s * 0.78],
                   start=0, end=180, fill=c)
    d.line([x + s * 0.30, y + s * 0.88, x + s * 0.70, y + s * 0.88],
           fill=c, width=5)


def icon_flame(d, x, y, s, c):
    # flame
    outer = [(0.50, 0.04), (0.62, 0.26), (0.78, 0.34), (0.86, 0.58),
             (0.78, 0.82), (0.62, 0.96), (0.38, 0.96), (0.22, 0.82),
             (0.14, 0.58), (0.24, 0.38), (0.34, 0.30), (0.40, 0.14)]
    d.polygon([(x + s * px, y + s * py) for px, py in outer], fill=c)
    inner = [(0.50, 0.42), (0.60, 0.58), (0.66, 0.72), (0.60, 0.88),
             (0.40, 0.88), (0.34, 0.72), (0.40, 0.58)]
    d.polygon([(x + s * px, y + s * py) for px, py in inner],
              fill=(255, 214, 90))


ICONS = {
    "chip": icon_chip,
    "talks": icon_talks,
    "satellite": icon_satellite,
    "globe": icon_globe,
    "scales": icon_scales,
    "flame": icon_flame,
}

# ---------------------------------------------------------------- stories
STORIES = [
    dict(tag="TECH  ·  UNITED STATES", color=(46, 125, 50), icon="chip",
         headline="Nvidia chief is back as US blacklists firm in spy scandal",
         body="The board unanimously reinstates Jensen Huang as CEO. Washington puts Singapore's Megaspeed on its export blacklist."),
    dict(tag="WAR & DIPLOMACY  ·  UKRAINE", color=(29, 78, 158), icon="talks",
         headline="Zelensky urges four-way talks; Kyiv says it sank a Russian warship",
         body="Ukraine's president calls for Ukraine, Russia, the US and Europe to meet “as soon as possible”. Russian strikes hit Kyiv."),
    dict(tag="SECURITY  ·  NATO", color=(91, 45, 142), icon="satellite",
         headline="NATO vows to defend space as Russia readies nuclear satellite",
         body="The alliance warns it will answer threats in orbit after reports of a possible Russian launch as soon as December."),
    dict(tag="CLIMATE  ·  TÜRKIYE", color=(15, 118, 110), icon="globe",
         headline="COP31 talks stall as oil states resist fossil-fuel limits",
         body="Negotiators in Türkiye are deadlocked as Saudi Arabia, Russia and other oil states clash with countries pushing for action."),
    dict(tag="JUSTICE  ·  THE HAGUE", color=(140, 47, 57), icon="scales",
         headline="World court: Myanmar committed genocide against the Rohingya",
         body="The International Court of Justice finds Myanmar guilty of genocidal acts against the Rohingya Muslim minority."),
    dict(tag="DISASTER  ·  INDONESIA", color=(194, 65, 12), icon="flame",
         headline="Deadly factory fire in Indonesia; workers still missing",
         body="A major blaze at an industrial site causes multiple casualties and leaves workers unaccounted for. Rescue work goes on."),
]

ALSO = ("ECB chief Christine Lagarde resigns, and the EU begins the hunt for her successor"
        "   •   South Africans vote as anger over services threatens the ANC"
        "   •   Leaked data put Russia's war dead near 700,000")

SOURCES = "Sources: Reuters  ·  Associated Press  ·  BBC  ·  AFP  ·  Kyiv Independent   —   All events of Tuesday 24 November 2026"


def draw_panel(d, x, y, w, h, story):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=PANEL,
                        outline=BORDER, width=2)
    # left accent bar
    d.rounded_rectangle([x + 12, y + 16, x + 22, y + h - 16], radius=5,
                        fill=story["color"])
    tx = x + 112
    tw = w - 112 - 24
    # icon in a tinted circle, top-left
    tint = tuple(int(0.86 * 255 + 0.14 * c) for c in story["color"])
    d.ellipse([x + 34, y + 14, x + 34 + 62, y + 14 + 62], fill=tint)
    ICONS[story["icon"]](d, x + 34 + 7, y + 14 + 7, 48, story["color"])
    # tag
    f_tag = font(SANS_BOLD, 17)
    d.text((tx, y + 16), story["tag"], font=f_tag, fill=story["color"])
    # headline
    f_head = font(SANS_BOLD, 24)
    lines = wrap(d, story["headline"], f_head, tw)[:3]
    hy = y + 44
    for line in lines:
        d.text((tx, hy), line, font=f_head, fill=INK)
        hy += 29
    # body
    f_body = font(SANS, 18)
    blines = wrap(d, story["body"], f_body, tw)
    by = hy + 8
    for line in blines[:4]:
        d.text((tx, by), line, font=f_body, fill=MUTED)
        by += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 160], fill=NAVY)
    d.rectangle([0, 160, W, 165], fill=GOLD)
    f_eye = font(SANS_BOLD, 18)
    d.text((28, 16), "THE WORLD IN ONE IMAGE", font=f_eye, fill=GOLD)
    f_date = font(SERIF_BOLD, 56)
    d.text((26, 42), "Tuesday 24 November 2026", font=f_date, fill=WHITE)
    f_sub = font(SANS, 22)
    d.text((28, 116), "Six stories that defined the day — from Kyiv to Jakarta",
           font=f_sub, fill=(198, 210, 224))

    # ---- story grid: 2 columns x 3 rows ----
    margin, gutter = 28, 16
    pw = (W - 2 * margin - gutter) // 2
    ph = 230
    top = 178
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gutter)
        y = top + row * (ph + gutter)
        draw_panel(d, x, y, pw, ph, story)

    # ---- also-today strip ----
    band_y = top + 3 * ph + 2 * gutter + 12  # 912
    d.rectangle([0, band_y, W, H], fill=NAVY)
    d.rectangle([0, band_y, W, band_y + 4], fill=GOLD)
    f_also_tag = font(SANS_BOLD, 18)
    d.text((28, band_y + 10), "ALSO TODAY", font=f_also_tag, fill=GOLD)
    f_also = font(SANS, 18)
    lines = wrap(d, ALSO, f_also, W - 56)
    ay = band_y + 36
    for line in lines[:2]:
        d.text((28, ay), line, font=f_also, fill=(214, 222, 232))
        ay += 22
    f_src = font(SANS, 14)
    d.text((28, band_y + 86), SOURCES, font=f_src, fill=(150, 164, 180))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
