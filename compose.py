"""Build the news-image-20261121 front page (1024x1024 JPEG).

Authored fresh in this session for Saturday 21 November 2026.
Flat vector illustration only (PIL drawing); every word is typeset by
this script, never baked into artwork. No faces, no hands in detail.
Layout follows the winning front-page grammar measured on this date's
field (see ~/workspace/makefun/news21-analysis/field-analysis.md):
masthead + huge serif date + subhead + 6-figure numbers strip +
coloured segmented region bar + 3 large illustrated leads + 10
illustrated cards with banner kickers + data chips + CONFIRMED/CLAIM/
REPORTED tag chips + pale map with numbered pins + 22 briefs +
boxed DATE CHECK + sources footer.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (20, 33, 61)
SEA_PALE = (208, 222, 230)  # pale sea, top-3 consensus (v2)
RED = (179, 39, 30)
RED_DARK = (150, 28, 22)
CREAM_PANEL = (250, 246, 236)
TAN = (217, 201, 163)
TAN_LIGHT = (228, 214, 182)
GREY = (90, 90, 90)
GOLD = (184, 134, 11)
BLUE = (31, 78, 121)
GREEN = (46, 125, 50)
PURPLE = (106, 61, 154)
TEAL = (14, 124, 123)

REGION_COLORS = [
    ("EUROPE", 6, BLUE),
    ("ASIA", 9, RED),
    ("MIDDLE EAST", 5, GOLD),
    ("AFRICA", 1, GREEN),
    ("AMERICAS", 10, PURPLE),
    ("OCEANIA", 2, TEAL),
    ("GLOBAL", 2, GREY),
]


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def pf_black(s):
    return F("PlayfairDisplay-Black.ttf", s)


def pf_bold(s):
    return F("PlayfairDisplay-Bold.ttf", s)


def nr(s):
    return F("Newsreader-Regular.ttf", s)


def nr_sb(s):
    return F("Newsreader-SemiBold.ttf", s)


def bc_b(s):
    return F("BarlowSC-Bold.ttf", s)


def bc_sb(s):
    return F("BarlowSC-SemiBold.ttf", s)


def bc_m(s):
    return F("BarlowSC-Medium.ttf", s)


def wrap(text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, font, max_w, max_lines, x, y, fill, leading):
    """Draw text wrapped to at most max_lines; warns loudly if truncated."""
    lines = wrap(text, font, max_w)
    if len(lines) > max_lines:
        print(f"TRUNCATED ({max_lines} lines max): {text[:80]!r} "
              f"-> {len(lines)} lines")
    lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        draw.text((x, y + i * leading), ln, font=font, fill=fill)
    return lines


def chip(draw, x, y, text, font, fg, bg, pad=5, outline=None):
    """Small rounded label; returns its right edge."""
    w = int(font.getlength(text)) + 2 * pad
    h = font.size + 2 * pad - 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg,
                           outline=outline, width=1 if outline else 0)
    draw.text((x + pad, y + pad - 1), text, font=font, fill=fg)
    return x + w


def banner(draw, x, y, text, font, w=None):
    """Red banner kicker inside a panel; returns its right edge."""
    tw = int(font.getlength(text)) + 12
    bw = w if w else tw
    h = font.size + 8
    draw.rectangle([x, y, x + bw, y + h], fill=RED)
    draw.text((x + 6, y + 4), text, font=font, fill=(255, 255, 255))
    return x + bw


# ---------------------------------------------------------------- data
SUBHEAD = ("Climate summit runs past its deadline \u00b7 Three missiles "
           "shot down over Riyadh \u00b7 Strong quake shakes Peru")

NUMBERS = [
    ("13", "DAY OF COP31, MEANT TO", "CLOSE ON DAY 12"),
    ("3", "MISSILES SHOT DOWN", "OVER RIYADH"),
    ("6.7", "MAGNITUDE OF THE QUAKE", "IN JUN\u00cdN, PERU"),
    ("146", "PEOPLE SAFE AFTER A JET'S", "EMERGENCY LANDING"),
    ("$58,983", "BITCOIN EARLY SATURDAY,", "DOWN 3.9% IN A DAY"),
    ("124*", "K L RAHUL'S SCORE AT TEA", "IN WELLINGTON"),
]

LEADS = [
    dict(num=1, place="ANTALYA, T\u00dcRKIYE", beat="CLIMATE",
         kicker="COP31: OVERTIME", data="NO DEAL \u00b7 DAY 13",
         source="Ongoing \u00b7 AFP, Al Jazeera",
         head="Climate summit runs into Saturday with no deal",
         deck=("COP31 missed its Friday close. A draft with no fossil fuels "
               "split nearly 200 countries. (AFP)")),
    dict(num=2, place="RIYADH", beat="WAR",
         kicker="SAUDI: MISSILES", data="3 SHOT DOWN",
         source="Coalition's count \u00b7 AFP",
         head="Three Houthi missiles shot down over Riyadh",
         deck=("Air defences downed three missiles over Riyadh before dawn. "
               "No damage or casualties. (Reuters, AFP)")),
    dict(num=3, place="JUN\u00cdN, PERU", beat="EARTHQUAKE",
         kicker="PERU: QUAKE 6.7", data="00:09 UTC \u00b7 108 KM DEEP",
         source="USGS \u00b7 IGP",
         head="Magnitude 6.7 earthquake shakes central Peru",
         deck=("The deep quake near Carhuamayo was felt in Lima and along "
               "the coast. No deaths or tsunami risk. (USGS, IGP)")),
]

CARDS = [
    dict(num=4, place="KYIV", beat="WAR", kicker="KYIV: WARNING",
         data="NBC INTERVIEW", tag="REPORTED",
         head="Zelensky: Crimea bridge \u201cwill not stay\u201d",
         deck="He warns of double-tap strikes in an NBC interview. (NBC)"),
    dict(num=5, place="STRAIT OF HORMUZ", beat="WAR", kicker="HORMUZ: DRONE",
         data="IRAN'S CLAIM", tag="CLAIM",
         head="Iran says it shot down a US drone",
         deck="No confirmation from Washington. (IRIB)"),
    dict(num=6, place="TEHRAN", beat="DIPLOMACY", kicker="IRAN: URANIUM",
         data="FAIR SOLUTION", tag="REPORTED",
         head="Iran: uranium stock stays in the country",
         deck="Minister still seeks a \u201cfair solution\u201d. (Reuters)"),
    dict(num=7, place="WASHINGTON", beat="TECHNOLOGY", kicker="TRUMP: AI TAX",
         data="NO DETAILS YET", tag="REPORTED",
         head="Trump vows tax on data centres abroad",
         deck="\u201cTremendous\u201d penalty; no details yet. (AP)"),
    dict(num=8, place="MERCURY", beat="SPACE", kicker="MERCURY: ORBIT",
         data="19:24 CET", tag="CONFIRMED",
         head="BepiColombo reaches Mercury after eight years",
         deck=("37-minute burn puts it in orbit; third mission to Mercury. "
               "(ESA, AP)")),
    dict(num=9, place="DAVAO", beat="AVIATION", kicker="DAVAO: 146 SAFE",
         data="146 SAFE", tag="CONFIRMED",
         head="Jet lands safely after engine fire alert",
         deck="Air Niugini 767 diverts after midnight. (Airline, AP)"),
    dict(num=10, place="BAHRAIN", beat="WAR", kicker="BAHRAIN: STRIKE",
         data="IRGC ATTACK", tag="REPORTED",
         head="Iran strikes US bases in Bahrain",
         deck=("IRGC claims two Patriot radars hit; Bahrain: fire, no "
               "injuries. (Reuters)")),
    dict(num=11, place="WORLD", beat="MARKETS", kicker="BITCOIN: $58,983",
         data="$58,983", tag="CONFIRMED",
         head="Bitcoin trades below $59,000 on Saturday",
         deck="Down 3.9% in 24 hours; ether $1,619. (CoinGecko)"),
    dict(num=12, place="LAS VEGAS", beat="FORMULA ONE", kicker="VERSTAPPEN: POLE",
         data="1:34.151", tag="CONFIRMED",
         head="Verstappen inherits Vegas pole after penalty",
         deck=("Antonelli fastest (1:33.893) but drops five places. "
               "(Formula 1)")),
    dict(num=13, place="WELLINGTON", beat="CRICKET", kicker="RAHUL: 124*",
         data="124*", tag="CONFIRMED",
         head="Rahul hits a century against New Zealand",
         deck="India 344 for 2 at tea, replying to 368. (AFP)"),
]

BRIEFS = [
    (14, "Kryvyi Rih", "Double strike kills 2 and injures 58 (Kyiv Indep.)"),
    (15, "Copenhagen", "Russian attack expelled over a plot (Al Jazeera)"),
    (16, "Antalya", "EU warns COP31 risks a \u201cfossil summit\u201d (AFP)"),
    (17, "Antalya", "Panama threatens to block the climate deal (Al Jazeera)"),
    (18, "Antalya", "Indonesia's PLN signs clean-power deals (Antara)"),
    (19, "Yemen", "Houthis threaten Jeddah and Red Sea ports (Al Jazeera)"),
    (20, "Washington", "Vance: Iran strikes were Trump's decision (Reuters)"),
    (21, "Washington", "Lawmaker threatens SpaceX's funding (CNN)"),
    (22, "Texas", "Execution of a man of 70 takes 63 minutes (ABC)"),
    (23, "Los Angeles", "Jury convicts man of starting Palisades fire (ABC)"),
    (24, "Missouri", "Judge approves $7.25bn Roundup settlement (AFP)"),
    (25, "Vancouver", "Canada rests defence in youth climate trial (AFP)"),
    (26, "Pyongyang", "Kim tours factories after no Trump meeting (AFP)"),
    (27, "Sejong", "Freight train derails; no one hurt (Korea Herald)"),
    (28, "Gulf of Finland", "Drones hit Russian cargo ship Sparta II; crew evacuated (Reuters)"),
    (29, "Bangkok", "Six-point plan on arsenic in two rivers (The Nation)"),
    (30, "New Delhi", "Pakistani minister joins SCO forum in India (Dawn)"),
    (31, "Eastern India", "Rain alerts as Akvan's remnants move inland (ETV)"),
    (32, "Myanmar", "Rights groups urge sanctions after court ruling (AP)"),
    (33, "Guasave", "Mexico captures FBI most-wanted 'Chapo Isidro'; 11 dead (Reuters)"),
    (34, "Melbourne", "Cummins keeps the Australian captaincy (ABC)"),
    (35, "Turin", "Zverev beats Medvedev 7-6(0), 6-4 in semi; final vs Alcaraz (ATP Tour)"),
]

DATE_CHECK_L1 = ("DATE CHECK \u2014 Left out as Friday 20 November's news: Wall Street's "
                 "correction, the Kyiv bridges barrage, the Poland missile, "
                 "the UK\u2013EU deal, Cyclone Akvan's landfall, the China\u2013Japan "
                 "Taiwan row, the Canberra AI talks.")
DATE_CHECK_L2 = ("Older: ICJ Myanmar ruling + Shenzhen declaration (Thu 19), Anthropic "
                 "IPO (Wed 18). Not yet: a final COP31 text, the Las Vegas GP "
                 "race, the ATP Finals final.")

TIMELINE = ("SATURDAY, HOUR BY HOUR \u2014 00:08 Davao lands \u00b7 00:09 Peru quake "
            "\u00b7 01:53 Riyadh alert \u00b7 02:47 India 344/2 \u00b7 05:37 Korea derail "
            "\u00b7 19:24 Mercury orbit")

FOOTER_L = ("Every story here happened, or was first reported, on Saturday 21 "
            "November 2026. Officials' counts and claims are attributed.")
FOOTER_R = ("HOW WE CHECKED \u2014 CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on the record "
            "\u00b7 REPORTED = one outlet \u00b7 CLAIM = one side's account")

# map pins: (story num, lon, lat, dx, dy) for stories 1-13 (11 = Bitcoin, everywhere)
PINS = [
    (1, 30.7, 36.9, 0, -6),
    (2, 46.7, 24.7, 6, 8),
    (3, -75.9, -11.2, 0, 0),
    (4, 30.5, 50.5, -2, -10),
    (5, 56.3, 26.5, 10, -2),
    (6, 51.4, 35.7, 8, -8),
    (7, -77.0, 38.9, 0, 0),
    (9, 125.6, 7.1, 0, 6),
    (10, 50.5, 26.2, -20, 18),  # Bahrain, clear of pin 5 (Hormuz) and pin 2 (Riyadh)
    (12, -115.1, 36.2, -8, 0),
    (13, 174.8, -41.3, 0, 0),
]

# rough continent polygons in (lon, lat); drawn as tan land on a navy sea
LAND = {
    "north_america": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                      (-85, 80), (-75, 72), (-65, 60), (-55, 52), (-60, 46),
                      (-70, 42), (-75, 35), (-80, 32), (-85, 30), (-90, 29),
                      (-97, 26), (-105, 22), (-110, 23), (-115, 30), (-120, 34),
                      (-125, 40), (-125, 48), (-135, 58), (-150, 60), (-160, 58)],
    "greenland": [(-58, 64), (-45, 60), (-40, 65), (-30, 68), (-22, 70),
                  (-25, 76), (-40, 78), (-55, 76), (-58, 70)],
    "south_america": [(-80, 10), (-75, 11), (-70, 12), (-62, 10), (-55, 6),
                      (-52, 4), (-50, 0), (-45, -3), (-38, -5), (-35, -8),
                      (-40, -15), (-42, -22), (-48, -28), (-55, -35), (-60, -38),
                      (-65, -40), (-68, -45), (-70, -50), (-73, -54), (-75, -50),
                      (-73, -40), (-72, -30), (-70, -20), (-78, -12), (-80, -5)],
    "europe": [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53),
               (8, 55), (10, 57), (18, 56), (21, 55), (24, 59), (28, 60),
               (30, 62), (25, 65), (20, 70), (15, 70), (12, 65), (5, 60),
               (0, 58), (-5, 55), (-8, 52), (-10, 48), (-10, 43)],
    "africa": [(-17, 15), (-16, 20), (-10, 30), (0, 35), (10, 37), (20, 32),
               (30, 31), (32, 31), (35, 28), (38, 22), (40, 18), (43, 12),
               (48, 11), (51, 10), (46, 5), (42, 0), (40, -5), (38, -12),
               (35, -18), (32, -25), (28, -32), (20, -35), (16, -30),
               (13, -20), (12, -12), (9, -2), (9, 4), (-8, 4), (-13, 8),
               (-17, 12)],
    "asia": [(30, 36), (36, 36), (42, 38), (44, 41), (48, 40), (50, 37),
             (54, 26), (57, 26), (60, 25), (62, 25), (66, 25), (70, 23),
             (75, 20), (80, 15), (85, 18), (90, 22), (92, 21), (95, 16),
             (98, 10), (100, 8), (103, 2), (105, 0), (108, -5), (110, -7),
             (115, -8), (118, -10), (120, -12), (125, -10), (130, -5),
             (135, 0), (140, 5), (142, 10), (140, 15), (138, 20), (135, 25),
             (132, 30), (130, 35), (128, 38), (126, 40), (122, 40),
             (120, 38), (118, 35), (122, 32), (120, 28), (118, 25),
             (115, 22), (112, 20), (108, 18), (105, 10), (102, 8),
             (100, 12), (98, 15), (95, 16), (92, 18), (90, 22), (88, 22),
             (86, 20), (84, 19), (82, 17), (80, 14), (78, 10), (76, 8),
             (74, 12), (72, 20), (70, 22), (68, 23), (66, 25), (62, 25),
             (58, 26), (56, 27), (54, 27), (52, 28), (50, 30), (48, 30),
             (46, 30), (44, 29), (42, 30), (40, 32), (38, 35), (36, 36),
             (33, 36)],
    "australia": [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
                  (129, -32), (132, -32), (136, -35), (138, -35), (140, -38),
                  (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
                  (146, -19), (142, -15), (142, -11), (136, -12), (132, -12),
                  (130, -13), (126, -14), (122, -17), (118, -20), (114, -22)],
}


# ------------------------------------------------------- illustrations
def draw_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 236, 222))
    # draft document (third text)
    d.rectangle([x + 118, y + 58, x + 164, y + h - 8], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([x + 118, y + 58, x + 164, y + 68], fill=RED)
    for ly in (76, 84, 92):
        d.line([x + 124, y + ly, x + 158, y + ly], fill=(150, 150, 150), width=2)
    # globe
    cx, cy, r = x + 210, y + 58, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 130, 190))
    d.ellipse([cx - 18, cy - 24, cx + 2, cy - 6], fill=(86, 170, 96))
    d.ellipse([cx - 6, cy + 4, cx + 20, cy + 22], fill=(86, 170, 96))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 90, 60), width=2)
    # thermometer
    tx = x + w - 82
    d.rounded_rectangle([tx, y + 14, tx + 14, y + h - 26], radius=7,
                        fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx + 4, y + 26, tx + 10, y + h - 34], fill=RED)
    d.ellipse([tx - 5, y + h - 36, tx + 19, y + h - 12], fill=RED,
              outline=INK, width=2)
    d.text((tx + 18, y + 20), "1.5\u00b0C", font=bc_b(13), fill=RED_DARK)


def draw_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    # moon
    d.ellipse([x + w - 44, y + 10, x + w - 18, y + 36], fill=(240, 230, 190))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 46, 34), (52, 34, 52), (92, 40, 28), (138, 30, 44),
                       (174, 44, 60), (224, 36, 38), (266, 34, 48), (306, 20, 30)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(10, 16, 34))
        for wy in range(base - bh + 6, base - 4, 10):
            for wx in range(x + bx + 5, x + bx + bw - 5, 11):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 210, 90))
    # missile trails: dotted arcs + bursts
    def trail(x0, y0, x1, y1):
        for t in range(0, 11):
            px = int(x0 + (x1 - x0) * t / 10)
            py = int(y0 + (y1 - y0) * t / 10 - 18 * (t / 10) * (1 - t / 10) * 4)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(250, 200, 80))
    trail(x + 40, y + 18, x + 90, y + 58)
    trail(x + 150, y + 10, x + 190, y + 52)
    trail(x + 250, y + 16, x + 290, y + 56)
    for bx, by in [(90, 58), (190, 52), (290, 56)]:
        for dx, dy in [(0, 0), (8, -6), (-7, -5), (6, 6), (-6, 7)]:
            d.line([x + bx, y + by, x + bx + dx, y + by + dy],
                   fill=(255, 170, 40), width=2)


def draw_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 180))
    # sun
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(240, 170, 60))
    # seismograph paper band
    d.rectangle([x + 8, y + 40, x + w - 8, y + 68], fill=(255, 255, 255),
                outline=(180, 160, 130), width=1)
    pts = []
    for i, v in enumerate([0, -9, 6, -12, 9, -5, 11, -9, 4, -3, 0]):
        pts.append((x + 16 + i * 20, y + 54 + v))
    d.line(pts, fill=RED, width=2)
    d.text((x + w - 66, y + 46), "M 6.7", font=bc_b(13), fill=RED_DARK)
    # mountains
    d.polygon([(x, y + h), (x + 90, y + 70), (x + 180, y + h)],
              fill=(150, 110, 70))
    d.polygon([(x + 140, y + h), (x + 240, y + 62), (x + w, y + h)],
              fill=(120, 84, 52))
    d.polygon([(x + 222, y + 74), (x + 240, y + 62), (x + 258, y + 74)],
              fill=(250, 246, 236))
    # houses
    for hx, hy in [(120, 88), (154, 92), (188, 88)]:
        d.rectangle([x + hx, y + hy, x + hx + 26, y + hy + 18],
                    fill=(250, 246, 236), outline=INK, width=1)
        d.polygon([(x + hx - 3, y + hy), (x + hx + 13, y + hy - 10),
                   (x + hx + 29, y + hy)], fill=RED)


LEAD_ART = [draw_cop31, draw_riyadh, draw_peru]


def card_art(d, idx, x, y, w, h):
    """Small flat motif for card idx (0-based)."""
    if idx == 0:  # Kyiv bridge, blue/yellow
        d.rectangle([x, y, x + w, y + h], fill=(198, 214, 232))
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(60, 90, 130))
        d.arc([x + 30, y + 2, x + w - 30, y + h + 6], 180, 360,
              fill=(240, 200, 40), width=5)
        d.line([x + 8, y + h - 16, x + w - 8, y + h - 16], fill=INK, width=2)
        for px in (52, 96, 140):
            d.line([x + px, y + h - 16, x + px, y + 12], fill=INK, width=2)
    elif idx == 1:  # Hormuz drone over sea
        d.rectangle([x, y, x + w, y + h], fill=(70, 120, 170))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(30, 70, 110))
        d.rectangle([x + 60, y + h - 24, x + 130, y + h - 12], fill=(20, 30, 50))
        d.rectangle([x + 88, y + h - 34, x + 104, y + h - 24], fill=(20, 30, 50))
        cx, cy = x + 150, y + 16
        d.ellipse([cx - 8, cy - 4, cx + 8, cy + 4], fill=(20, 20, 20))
        for sx in (-14, 14):
            d.line([cx + sx - 8, cy - 6, cx + sx + 8, cy - 6], fill=(20, 20, 20),
                   width=2)
        d.line([cx, cy + 4, cx, cy + 10], fill=(20, 20, 20), width=2)
    elif idx == 2:  # Tehran dome + flag bars
        d.rectangle([x, y, x + w, y + h], fill=(238, 230, 210))
        d.rectangle([x + 20, y + 8, x + 96, y + 16], fill=(0, 120, 60))
        d.rectangle([x + 20, y + 16, x + 96, y + 24], fill=(255, 255, 255))
        d.rectangle([x + 20, y + 24, x + 96, y + 32], fill=(200, 40, 30))
        d.pieslice([x + 120, y + 6, x + 168, y + 44], 180, 360, fill=(0, 120, 60))
        d.rectangle([x + 120, y + 40, x + 168, y + h - 4], fill=(0, 100, 52))
    elif idx == 3:  # AI data centres
        d.rectangle([x, y, x + w, y + h], fill=(20, 33, 61))
        for rx in (18, 62, 106):
            d.rectangle([x + rx, y + 8, x + rx + 34, y + h - 8], fill=(40, 55, 90),
                        outline=(120, 140, 180), width=1)
            for ry in (14, 24, 34):
                d.rectangle([x + rx + 5, y + ry, x + rx + 12, y + ry + 4],
                            fill=(90, 200, 120))
        d.ellipse([x + 148, y + 8, x + 182, y + 42], fill=RED)
        d.text((x + 156, y + 12), "%", font=bc_b(20), fill=(255, 255, 255))
    elif idx == 4:  # BepiColombo at Mercury: cratered planet + probe
        d.rectangle([x, y, x + w, y + h], fill=(12, 14, 28))
        for sx, sy in [(20, 10), (60, 22), (110, 8), (160, 16), (40, 34),
                       (140, 30)]:
            d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                      fill=(255, 255, 255))
        # Mercury, cratered grey disc
        d.ellipse([x + 18, y + 8, x + 82, y + h - 6], fill=(168, 158, 142),
                  outline=(120, 110, 96), width=1)
        for cx, cy, cr in [(34, 20, 6), (58, 16, 4), (44, 34, 5), (64, 30, 3),
                           (30, 34, 3)]:
            d.ellipse([x + cx - cr, y + cy - cr, x + cx + cr, y + cy + cr],
                      fill=(140, 130, 116))
        # probe body + solar panels, approaching from the right
        d.rectangle([x + 120, y + 20, x + 140, y + 34], fill=(200, 200, 200),
                    outline=INK, width=1)
        d.rectangle([x + 96, y + 24, x + 120, y + 30], fill=(40, 80, 160))
        d.rectangle([x + 140, y + 24, x + 164, y + 30], fill=(40, 80, 160))
        d.line([x + 140, y + 27, x + 168, y + 27], fill=(250, 200, 60), width=2)
    elif idx == 5:  # Davao plane
        d.rectangle([x, y, x + w, y + h], fill=(150, 195, 225))
        d.ellipse([x + 16, y + 10, x + 44, y + 20], fill=(255, 255, 255))
        d.ellipse([x + 150, y + 6, x + 178, y + 16], fill=(255, 255, 255))
        d.ellipse([x + 60, y + 22, x + 130, y + 34], fill=(255, 255, 255))
        d.polygon([(x + 52, y + 30), (x + 96, y + 30), (x + 108, y + 34),
                   (x + 60, y + 34)], fill=(255, 255, 255))
        d.rectangle([x + 40, y + h - 8, x + w - 20, y + h - 4], fill=(90, 90, 90))
    elif idx == 6:  # Bahrain strike: night sky, base buildings, fire glow
        d.rectangle([x, y, x + w, y + h], fill=(16, 22, 44))
        d.ellipse([x + w - 40, y + 6, x + w - 20, y + 26],
                  fill=(240, 230, 190))
        # low base buildings
        for bx, bw, bh in [(0, 52, 22), (58, 44, 30), (108, 50, 20),
                           (164, 28, 26)]:
            d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                        fill=(10, 14, 30))
            for wy in range(y + h - bh + 5, y + h - 4, 8):
                for wx in range(x + bx + 5, x + bx + bw - 5, 11):
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=(250, 210, 90))
        # two fire bursts above the base
        for bx, by in [(70, 14), (140, 10)]:
            for dx, dy in [(0, 0), (9, -6), (-8, -5), (7, 6), (-7, 7)]:
                d.line([x + bx, y + by, x + bx + dx, y + by + dy],
                       fill=(255, 170, 40), width=2)
            d.ellipse([x + bx - 3, y + by - 3, x + bx + 3, y + by + 3],
                      fill=(255, 200, 80))
    elif idx == 7:  # Bitcoin chart
        d.rectangle([x, y, x + w, y + h], fill=(18, 18, 22))
        d.ellipse([x + 14, y + 8, x + 48, y + 42], fill=(245, 150, 30))
        d.text((x + 24, y + 12), "B", font=bc_b(20), fill=(255, 255, 255))
        pts = [(x + 56, y + 12), (x + 80, y + 18), (x + 104, y + 16),
               (x + 128, y + 28), (x + 152, y + 26), (x + 176, y + 40)]
        d.line(pts, fill=(220, 60, 40), width=3)
    elif idx == 8:  # Las Vegas GP track + flag
        d.rectangle([x, y, x + w, y + h], fill=(30, 32, 40))
        d.arc([x + 20, y + 6, x + w - 60, y + h + 10], 90, 270,
              fill=(150, 150, 150), width=7)
        d.rectangle([x + w - 52, y + 8, x + w - 12, y + 40], fill=(255, 255, 255),
                    outline=INK, width=1)
        for r in range(2):
            for c in range(2):
                if (r + c) % 2 == 0:
                    d.rectangle([x + w - 52 + c * 10, y + 8 + r * 8,
                                 x + w - 42 + c * 10, y + 16 + r * 8],
                                fill=INK)
        d.rectangle([x + 30, y + h - 18, x + 78, y + h - 8], fill=RED)
        d.ellipse([x + 36, y + h - 6, x + 44, y + h - 2], fill=INK)
        d.ellipse([x + 64, y + h - 6, x + 72, y + h - 2], fill=INK)
    else:  # Rahul cricket
        d.rectangle([x, y, x + w, y + h], fill=(120, 170, 90))
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(90, 130, 60))
        d.polygon([(x + 60, y + 8), (x + 76, y + 8), (x + 66, y + 40),
                   (x + 52, y + 40)], fill=(210, 180, 130))
        d.ellipse([x + 108, y + 30, x + 120, y + 42], fill=(180, 30, 20))
        for sx in (140, 146, 152):
            d.line([x + sx, y + 24, x + sx, y + 40], fill=(255, 255, 255), width=2)
        d.line([x + 138, y + 24, x + 154, y + 24], fill=(255, 255, 255), width=2)


# ------------------------------------------------------------ layout
def fit_font_size(text, name, start, max_w):
    size = start
    while size > 40:
        f = F(name, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return F(name, size)


def draw_masthead(d):
    d.text((14, 12), "THE WORLD IN ONE DAY", font=bc_b(16), fill=RED)
    count = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    f = bc_sb(13)
    d.text((1010 - f.getlength(count), 14), count, font=f, fill=INK)
    d.line([14, 36, 1010, 36], fill=INK, width=2)
    date_f = fit_font_size("Saturday 21 November 2026",
                           "PlayfairDisplay-Black.ttf", 88, 980)
    dw = date_f.getlength("Saturday 21 November 2026")
    d.text(((1024 - dw) / 2, 42), "Saturday 21 November 2026",
           font=date_f, fill=INK)
    sf = nr(19)
    sw = sf.getlength(SUBHEAD)
    d.text(((1024 - sw) / 2, 134), SUBHEAD, font=sf, fill=INK)
    d.line([14, 156, 1010, 156], fill=INK, width=1)


def draw_numbers(d):
    cell_w = 996 / 6
    for i, (num, cap1, cap2) in enumerate(NUMBERS):
        cx = 14 + cell_w * i + cell_w / 2
        nf = pf_black(30)
        nw = nf.getlength(num)
        d.text((cx - nw / 2, 162), num, font=nf, fill=RED)
        cf = bc_m(10)
        for j, cap in enumerate((cap1, cap2)):
            cw = cf.getlength(cap)
            d.text((cx - cw / 2, 196 + j * 12), cap, font=cf, fill=INK)
        if i:
            d.line([14 + cell_w * i, 164, 14 + cell_w * i, 216],
                   fill=(200, 195, 180), width=1)


def draw_region_bar(d):
    seg_w = 996 / 7
    x = 14
    for name, count, color in REGION_COLORS:
        d.rectangle([x, 220, x + seg_w, 240], fill=color)
        label = f"{name} {count}"
        f = bc_b(12)
        tw = f.getlength(label)
        d.text((x + (seg_w - tw) / 2, 224), label, font=f,
               fill=(255, 255, 255))
        x += seg_w


def draw_lead(d, lead, x, y, w, h, art):
    art(d, x, y, w, h)
    banner(d, x + 6, y + 6, lead["kicker"], bc_b(12))
    chip(d, x + 6, y + 36, lead["data"], bc_sb(11), INK, (255, 255, 255))
    chip(d, x + 6, y + h - 26, lead["source"], bc_sb(10),
         (255, 255, 255), INK)
    ky = y + h + 6
    d.text((x, ky), f"{lead['num']} \u00b7 {lead['place']} \u00b7 {lead['beat']}",
           font=bc_b(11), fill=RED)
    fit_lines(d, lead["head"], pf_bold(23), w, 2, x, ky + 16, INK, 24)
    fit_lines(d, lead["deck"], nr(12), w, 2, x, ky + 66, INK, 14)


def draw_card(d, card, x, y, w, h, idx):
    card_art(d, idx, x, y, w, h)
    banner(d, x + 4, y + 4, card["kicker"], bc_b(11))
    data_w = int(bc_sb(9).getlength(card["data"])) + 10
    chip(d, x + w - data_w - 4, y + h - 20, card["data"], bc_sb(9), INK,
         (255, 255, 255))
    ky = y + h + 4
    d.text((x, ky), f"{card['num']} \u00b7 {card['place']} \u00b7 {card['beat']}",
           font=bc_b(10), fill=RED)
    fit_lines(d, card["head"], pf_bold(15), w, 2, x, ky + 14, INK, 16)
    fit_lines(d, card["deck"], nr(10.5), w, 2, x, ky + 48, INK, 12)
    tag = card["tag"]
    tf = bc_b(8)
    tw = int(tf.getlength(tag)) + 8
    chip(d, x + w - tw, ky + 70, tag, tf, RED, None, pad=4, outline=RED)


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    return (mx + (lon + 180) / 360 * mw, my + (90 - lat) / 180 * mh)


def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA_PALE)
    for pts in LAND.values():
        xy = [lonlat_to_xy(lon, lat, mx, my, mw, mh) for lon, lat in pts]
        d.polygon(xy, fill=TAN)
    for num, lon, lat, dx, dy in PINS:
        px, py = lonlat_to_xy(lon, lat, mx, my, mw, mh)
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        tf = bc_b(10)
        t = str(num)
        d.text((px - tf.getlength(t) / 2, py - 7), t, font=tf,
               fill=(255, 255, 255))
    d.text((mx + 6, my + mh - 14),
           "Pins 1\u201313 mark the pictured stories. 8 is in space: Mercury. "
           "11 Bitcoin is everywhere.",
           font=nr(8.5), fill=INK)


def draw_briefs(d, x, y, w):
    d.text((x, y), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
           font=bc_b(12), fill=RED)
    by = y + 18
    for num, place, text in BRIEFS:
        nf = bc_b(9)
        d.text((x, by), str(num), font=nf, fill=RED)
        nx = x + nf.getlength(str(num)) + 4
        pf = nr_sb(9)
        d.text((nx, by), place, font=pf, fill=INK)
        tx = nx + pf.getlength(place) + 4
        d.text((tx, by), "\u2014 " + text, font=nr(9), fill=INK)
        by += 9


def draw_date_check(d, y):
    d.rectangle([14, y, 1010, y + 32], outline=RED, width=2)
    l1 = ("DATE CHECK \u2014 Left out as Friday 20 November's news: Wall Street's "
          "correction, the Kyiv bridges barrage, the Poland missile, the "
          "UK\u2013EU deal, Cyclone Akvan's landfall, the China\u2013Japan Taiwan "
          "row, the Canberra AI talks.")
    l2 = ("Older: ICJ Myanmar ruling + Shenzhen declaration (Thu 19), Anthropic "
          "IPO (Wed 18). Not yet: a final COP31 text, the Las Vegas GP race, "
          "the ATP Finals final.")
    f = nr(10.5)
    d.text((22, y + 4), l1, font=f, fill=INK)
    d.text((22, y + 18), l2, font=f, fill=INK)


def build(quality=82):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, 1018, 1018], outline=INK, width=2)
    draw_masthead(d)
    draw_numbers(d)
    draw_region_bar(d)
    lead_y, lead_h = 244, 112
    lead_w = 326
    for i, lead in enumerate(LEADS):
        draw_lead(d, lead, 14 + i * (lead_w + 8), lead_y, lead_w, lead_h,
                  LEAD_ART[i])
    card_w, card_h = 192, 50
    for r in range(2):
        for c in range(5):
            idx = r * 5 + c
            draw_card(d, CARDS[idx], 14 + c * (card_w + 8),
                      462 + r * 140, card_w, card_h, idx)
    d.text((14, 744), "WHERE IT HAPPENED", font=bc_b(12), fill=INK)
    draw_map(d, 14, 758, 472, 200)
    draw_briefs(d, 496, 744, 514)
    draw_date_check(d, 964)
    ff = nr(8.5)
    d.text((14, 1002), FOOTER_L, font=ff, fill=INK)
    rw = ff.getlength(FOOTER_R)
    d.text((1010 - rw, 1002), FOOTER_R, font=ff, fill=INK)
    out = os.path.join(HERE, "image.jpg")
    img.save(out, "JPEG", quality=quality, optimize=True)
    return out


if __name__ == "__main__":
    import hashlib
    import sys

    q = int(sys.argv[1]) if len(sys.argv) > 1 else 82
    path = build(q)
    data = open(path, "rb").read()
    print(f"{path}: {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
