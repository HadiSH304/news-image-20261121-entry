"""Build the news-image-20261121 front page (1024x1024 JPEG) — v3.

Authored fresh in this session for Saturday 21 November 2026.
Flat vector illustration only (PIL drawing); every word is typeset by
this script, never baked into artwork. No faces, no hands in detail.
Layout follows the winning front-page grammar measured on this date's
field (see ~/workspace/makefun/news21-analysis/v3-plan.md):
masthead + huge serif date + subhead + 6-figure numbers strip +
9-segment region bar + UTC timeline strip + 3 large illustrated leads
+ 10 illustrated cards with banner kickers + data chips + CONFIRMED/
CLAIM/REPORTED tag chips + pale map with region-coloured pins +
22 briefs + boxed DATE CHECK + sources footer.

v3 = the CURRENT top-cluster consensus story set (Bahrain lead, Sparta II
lead, EU-Indonesia / Geneva-128 / France-marches / England-rugby card
core, new numbers strip, 9 regions) on v2's fixed layout, plus the UTC
timeline strip v2 defined but never drew.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (20, 33, 61)
SEA_PALE = (208, 222, 230)  # pale sea, top-3 consensus
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
ORANGE = (210, 110, 30)
BROWN = (140, 90, 40)

REGION_COLORS = [
    ("EUROPE", 9, BLUE),
    ("MID EAST", 6, GOLD),
    ("AFRICA", 2, GREEN),
    ("S. ASIA", 3, PURPLE),
    ("E. ASIA", 3, RED),
    ("SE ASIA", 3, TEAL),
    ("AMERICAS", 4, ORANGE),
    ("OCEANIA", 2, BROWN),
    ("GLOBAL", 3, GREY),
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
SUBHEAD = ("Iran strikes Bahrain \u00b7 Sparta II ablaze off Finland \u00b7 "
           "COP31 runs into overtime")

NUMBERS = [
    ("6.7", "PERU QUAKE MAGNITUDE", "(USGS)"),
    ("2", "TANKERS HIT OFF KHASAB", "(UKMTO)"),
    ("128", "NATIONS BACKING GENEVA", "ROBOT-ARMS TALKS"),
    ("90.4%", "TARIFF LINES DUTY-FREE", "(IEU-CEPA)"),
    ("82,500", "MARCHERS IN FRANCE", "(MINISTRY)"),
    ("37\u201312", "ENGLAND OVER NEW", "ZEALAND"),
]

TIMELINE = ("00:09 Peru quake \u00b7 03:00 Basra fire \u00b7 c.04:00 Geneva talks "
            "end \u00b7 06:50 Sparta II alarm \u00b7 09:42 Banda Sea quake \u00b7 "
            "18:24 BepiColombo orbit \u00b7 c.22:00 COP31 talks pause")

LEADS = [
    dict(num=1, place="BAHRAIN \u00b7 HORMUZ", beat="WAR",
         kicker="GULF: IRAN STRIKES", data="2 BASES \u00b7 2 TANKERS",
         source="Al Jazeera \u00b7 Reuters \u00b7 UKMTO",
         head="Iran strikes Bahrain bases; tankers hit off Oman",
         deck=("IRGC says it hit US radar at two bases; Bahrain says a "
               "civilian plant burned. (Reuters, UKMTO)")),
    dict(num=2, place="GULF OF FINLAND", beat="SECURITY",
         kicker="SHIP ABLAZE", data="06:50 UTC \u00b7 16 SAFE",
         source="Reuters \u00b7 Finnish MoD",
         head="Drones set Russian cargo ship ablaze off Finland",
         deck=("Hit by two drones, Sparta II drifted into Finnish waters; "
               "16 crew evacuated. (Reuters)")),
    dict(num=3, place="ANTALYA, T\u00dcRKIYE", beat="CLIMATE",
         kicker="COP31: OVERTIME", data="NO DEAL \u00b7 DAY 13",
         source="Ongoing \u00b7 AFP, Al Jazeera",
         head="Climate summit runs into Saturday with no deal",
         deck=("COP31 missed its Friday close. A draft with no fossil fuels "
               "split nearly 200 countries. (AFP)")),
]

CARDS = [
    dict(num=4, place="JUN\u00cdN, PERU", beat="EARTHQUAKE",
         kicker="PERU: QUAKE 6.7", data="00:09 UTC", tag="OFFICIAL",
         head="Deep 6.7 earthquake shakes central Peru",
         deck="Near Carhuamayo, felt in Lima; no deaths or tsunami risk. (USGS, IGP)"),
    dict(num=5, place="BRUSSELS", beat="TRADE", kicker="EU\u2013INDONESIA",
         data="90.4% DUTY-FREE", tag="OFFICIAL",
         head="EU and Indonesia sign trade pact",
         deck="90.4% of tariff lines duty-free; in force from 2027. (EC, Antara)"),
    dict(num=6, place="GENEVA", beat="ARMS CONTROL", kicker="GENEVA: ROBOT ARMS",
         data="128 NATIONS", tag="CONFIRMED",
         head="128 nations back Geneva robot-arms talks",
         deck="Deal to draft killer-robot rules by 2028; no binding treaty yet. (AP, AFP)"),
    dict(num=7, place="SINALOA, MEXICO", beat="CRIME", kicker="CHAPO ISIDRO",
         data="11 DEAD", tag="CONFIRMED",
         head="Mexico captures cartel boss \u2018Chapo Isidro\u2019",
         deck="FBI most-wanted seized in Guasave; 4 soldiers, 7 gunmen killed. (AP, Reuters)"),
    dict(num=8, place="MERCURY", beat="SPACE", kicker="MERCURY: ORBIT",
         data="19:24 CET", tag="CONFIRMED",
         head="BepiColombo reaches Mercury after eight years",
         deck=("37-minute burn puts it in orbit; third mission to Mercury. "
               "(ESA, AP)")),
    dict(num=9, place="PARIS", beat="PROTEST", kicker="FRANCE: MARCHES",
         data="82,500", tag="OFFICIAL",
         head="Sixth Saturday of cost-of-living marches",
         deck="Ministry counts 82,500; organisers say 150,000. (Reuters)"),
    dict(num=10, place="LONDON", beat="RUGBY", kicker="ENGLAND: 37\u201312",
         data="RECORD MARGIN", tag="CONFIRMED",
         head="England beat All Blacks by record margin",
         deck="Five tries in a 37\u201312 rout at Twickenham. (RFU, AP)"),
    dict(num=11, place="ABUJA", beat="FOOTBALL", kicker="CAF: 54/54",
         data="54/54", tag="OFFICIAL",
         head="All 54 CAF nations back Infantino",
         deck="Vote for FIFA president set for March 2027 in Rabat. (AP, CAF)"),
    dict(num=12, place="BASRA, IRAQ", beat="DISASTER", kicker="BASRA: FIRE",
         data="4 DEAD", tag="CONFIRMED",
         head="Basra power-station fire kills 4",
         deck="Gas pipeline burst at the Hartha plant; 35 injured. (Reuters, INA)"),
    dict(num=13, place="TAIWAN", beat="SECURITY", kicker="TAIWAN: 21 JETS",
         data="15 CROSSED", tag="OFFICIAL",
         head="Chinese jets cross the median line",
         deck="21 PLA aircraft detected; 15 cross the line. (Taiwan MND)"),
]

BRIEFS = [
    (14, "Riyadh", "Coalition says it downed 3 Houthi missiles (AFP)"),
    (15, "Hormuz", "Iran claims it downed a US drone; no US comment (IRIB)"),
    (16, "Davao", "Jet lands safely after engine fire; 146 safe (AP)"),
    (17, "Kyiv", "Zelensky: Crimea bridge \u201cwill not stay\u201d (NBC)"),
    (18, "Tehran", "Iran: uranium stock stays in the country (Reuters)"),
    (19, "Washington", "Trump vows tax on data centres abroad (AP)"),
    (20, "Tokyo", "China tells Japan to \u201ccorrect\u201d Taiwan words (AFP)"),
    (21, "Canberra", "Australia and China agree to AI talks (ABC)"),
    (22, "Markets", "Bitcoin hits $55,100 low, then back over $60,000 (CoinDesk)"),
    (23, "Osaka", "BTS take five MAMA awards, two grand prizes (Yonhap)"),
    (24, "Banda Sea", "M6.8 quake, 105 km NE of Lospalos; felt in Darwin (USGS)"),
    (25, "Bayelsa", "Funeral boat toll reaches 24; capsized Friday (NEMA)"),
    (26, "Las Vegas", "Verstappen takes pole; Antonelli docked 5 places (F1)"),
    (27, "Turin", "Zverev beats Medvedev 7-6(0), 6-4; final vs Alcaraz (ATP Tour)"),
    (28, "Turin", "Alcaraz beats Shelton; faces Zverev in final (ATP Tour)"),
    (29, "Wellington", "Rahul 136 as India reach 486/4 at stumps (AFP)"),
    (30, "Kryvyi Rih", "Double strike kills 2 and injures 58 (Kyiv Indep.)"),
    (31, "Yemen", "Houthis threaten Jeddah and Red Sea ports (Al Jazeera)"),
    (32, "Bangkok", "Six-point plan on arsenic in two rivers (The Nation)"),
    (33, "Melbourne", "Cummins keeps the Australian captaincy (ABC)"),
    (34, "New Delhi", "Pakistani minister joins SCO forum in India (Dawn)"),
    (35, "Eastern India", "Rain alerts as Akvan's remnants move inland (ETV)"),
]

DATE_CHECK_L1 = ("DATE CHECK \u2014 Left out as Friday 20 November's news: Wall Street's "
                 "correction, the Kyiv bridges barrage, the Poland missile, "
                 "the UK\u2013EU deal, Cyclone Akvan's landfall.")
DATE_CHECK_L2 = ("Older: ICJ Myanmar ruling + Shenzhen declaration (Thu 19), Anthropic "
                 "IPO (Wed 18). Sun 22 Nov: Verstappen wins the Las Vegas GP \u00b7 "
                 "COP31's final text put to the vote \u00b7 the ATP Finals final "
                 "still to play.")

FOOTER_L = ("Every story here happened, or was first reported, on Saturday 21 "
            "November 2026. Officials' counts and claims are attributed.")
FOOTER_R = ("HOW WE CHECKED \u2014 CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on the record "
            "\u00b7 REPORTED = one outlet \u00b7 CLAIM = one side's account")

# map pins: (story num, lon, lat, dx, dy, region colour) for stories 1-13
# (8 = BepiColombo, in space: no pin; 11 Bitcoin was a card in v2, a brief now)
PINS = [
    (1, 50.5, 26.2, -16, 14, GOLD),    # Bahrain
    (2, 23.0, 59.5, 0, -12, BLUE),     # Sparta II, Gulf of Finland
    (3, 30.7, 36.9, 0, -6, GREY),      # COP31, Antalya
    (4, -75.9, -11.2, 0, 0, ORANGE),   # Peru
    (5, 4.4, 50.8, -16, -10, BLUE),    # Brussels
    (6, 6.1, 46.2, 16, 8, BLUE),       # Geneva
    (7, -108.5, 25.6, -8, 0, ORANGE),  # Guasave
    (9, 2.35, 48.85, -14, 12, BLUE),   # Paris
    (10, -0.1, 51.5, 14, -10, BLUE),   # London
    (11, 7.5, 9.1, 0, 0, GREEN),       # Abuja
    (12, 47.8, 30.5, 14, -12, GOLD),   # Basra
    (13, 121.0, 25.0, 0, 0, RED),      # Taipei
]

# rough continent polygons in (lon, lat); drawn as tan land on a pale sea
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
def draw_bahrain(d, x, y, w, h):
    """Lead 1: stylised Gulf map — Iran top, Arabia bottom-left, Bahrain
    island with a fire burst, two tankers struck near the Strait of Hormuz."""
    d.rectangle([x, y, x + w, y + h], fill=(170, 205, 220))
    # Iran land, top edge
    d.polygon([(x + 190, y), (x + w, y), (x + w, y + 30), (x + 272, y + 42),
               (x + 218, y + 30)], fill=TAN)
    # Arabian peninsula, bottom-left
    d.polygon([(x, y + 62), (x + 58, y + 46), (x + 118, y + 52),
               (x + 148, y + 78), (x + 118, y + h), (x, y + h)], fill=TAN)
    # Qatar peninsula
    d.polygon([(x + 148, y + 62), (x + 166, y + 58), (x + 172, y + 74),
               (x + 158, y + 80)], fill=TAN)
    # Oman, bottom-right
    d.polygon([(x + 282, y + 78), (x + w, y + 68), (x + w, y + h),
               (x + 292, y + h)], fill=TAN)
    # dashed red arc: Iran coast -> Bahrain
    for t in range(0, 11, 2):
        px = int(x + 252 - (252 - 152) * t / 10)
        py = int(y + 30 + (66 - 30) * t / 10 - 16 * (t / 10) * (1 - t / 10))
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    # Bahrain island + fire burst
    bx, by = x + 152, y + 66
    d.ellipse([bx - 5, by - 3, bx + 5, by + 3], fill=(120, 90, 60))
    for dx, dy in [(0, 0), (9, -7), (-9, -6), (8, 7), (-8, 8), (0, -10)]:
        d.line([bx, by, bx + dx, by + dy], fill=(255, 170, 40), width=2)
    d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 200, 80))
    # two tankers near Hormuz (right side)
    for tx, ty in [(238, 58), (264, 76)]:
        d.rectangle([x + tx, y + ty, x + tx + 34, y + ty + 7],
                    fill=(20, 30, 50))
        d.rectangle([x + tx + 6, y + ty - 5, x + tx + 14, y + ty],
                    fill=(20, 30, 50))
        d.ellipse([x + tx + 14, y + ty - 3, x + tx + 20, y + ty + 3],
                  fill=(255, 170, 40))
    lf = bc_b(9)
    d.text((x + 236, y + 6), "IRAN", font=lf, fill=INK)
    d.text((x + 8, y + 88), "SAUDI", font=lf, fill=INK)
    d.text((x + 232, y + 92), "HORMUZ", font=lf, fill=INK)


def draw_sparta(d, x, y, w, h):
    """Lead 2: cargo ship ablaze on a dark sea, two drones above, a pale
    Finnish coast at the top-right corner."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 45, 75))
    # Finnish coast, top-right
    d.polygon([(x + 240, y), (x + w, y), (x + w, y + 26), (x + 268, y + 34),
               (x + 246, y + 22)], fill=TAN)
    d.text((x + 262, y + 4), "FINLAND", font=bc_b(9), fill=INK)
    # sea
    d.rectangle([x, y + 44, x + w, y + h], fill=(16, 34, 64))
    # moon
    d.ellipse([x + 18, y + 8, x + 40, y + 30], fill=(240, 230, 190))
    # ship hull + containers + bridge
    base = y + h - 12
    d.polygon([(x + 30, base - 22), (x + 296, base - 22), (x + 286, base),
               (x + 40, base)], fill=(12, 14, 22))
    d.rectangle([x + 30, base - 26, x + 296, base - 22], fill=(150, 30, 25))
    for cx in (60, 104, 148, 192, 236):
        d.rectangle([x + cx, base - 46, x + cx + 38, base - 26],
                    fill=(90, 110, 130))
        d.rectangle([x + cx, base - 38, x + cx + 38, base - 34],
                    fill=(60, 75, 90))
    d.rectangle([x + 262, base - 58, x + 292, base - 26],
                fill=(220, 220, 210))
    for wy in range(base - 54, base - 28, 8):
        d.rectangle([x + 266, wy, x + 272, wy + 4], fill=(250, 210, 90))
    # flames above mid-ship
    fx, fy = x + 160, base - 48
    for dx, dy in [(0, 0), (12, -10), (-12, -9), (10, 10), (-10, 11),
                   (0, -14), (18, -4), (-18, -3)]:
        d.line([fx, fy, fx + dx, fy + dy], fill=(255, 170, 40), width=3)
    d.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=(255, 200, 80))
    # smoke
    for sx, sy, sr in [(150, 30, 7), (168, 22, 9), (186, 28, 6)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(120, 120, 120))
    # two drones with dashed paths
    for dx0, dy0 in [(70, 6), (250, 4)]:
        for t in range(0, 8):
            px = x + dx0 + t * 4
            py = y + dy0 + t * 3
            d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255))
        cx, cy = x + dx0 + 30, y + dy0 + 24
        d.ellipse([cx - 6, cy - 3, cx + 6, cy + 3], fill=(20, 20, 20))
        d.line([cx - 12, cy - 4, cx + 12, cy - 4], fill=(20, 20, 20), width=2)
    d.text((x + 44, base - 12), "SPARTA II", font=bc_b(10),
           fill=(255, 255, 255))


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


LEAD_ART = [draw_bahrain, draw_sparta, draw_cop31]


def card_art(d, idx, x, y, w, h):
    """Small flat motif for card idx (0-based, cards 4-13)."""
    if idx == 0:  # Peru: seismograph band + mountains + houses
        d.rectangle([x, y, x + w, y + h], fill=(232, 214, 180))
        d.ellipse([x + w - 30, y + 4, x + w - 12, y + 22], fill=(240, 170, 60))
        d.rectangle([x + 6, y + 12, x + w - 6, y + 28], fill=(255, 255, 255),
                    outline=(180, 160, 130), width=1)
        pts = []
        for i, v in enumerate([0, -5, 4, -6, 5, -3, 6, -5, 3, -2, 0]):
            pts.append((x + 12 + i * 15, y + 20 + v))
        d.line(pts, fill=RED, width=2)
        d.text((x + w - 46, y + 14), "M 6.7", font=bc_b(11), fill=RED_DARK)
        d.polygon([(x, y + h), (x + 70, y + 30), (x + 140, y + h)],
                  fill=(150, 110, 70))
        d.polygon([(x + 110, y + h), (x + 170, y + 32), (x + w, y + h)],
                  fill=(120, 84, 52))
        for hx in (96, 122, 148):
            d.rectangle([x + hx, y + 38, x + hx + 18, y + 48],
                        fill=(250, 246, 236), outline=INK, width=1)
            d.polygon([(x + hx - 2, y + 38), (x + hx + 9, y + 31),
                       (x + hx + 20, y + 38)], fill=RED)
    elif idx == 1:  # EU-Indonesia: two flags + SIGNED stamp
        d.rectangle([x, y, x + w, y + h], fill=(238, 230, 210))
        # EU flag, left
        d.rectangle([x + 14, y + 8, x + 82, y + h - 8], fill=(0, 45, 120))
        for k in range(12):
            import math
            ang = 2 * math.pi * k / 12
            sx = x + 48 + int(20 * math.cos(ang))
            sy = y + 25 + int(13 * math.sin(ang))
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(250, 210, 60))
        # Indonesia flag, right
        d.rectangle([x + 110, y + 8, x + 178, y + h - 8], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.rectangle([x + 110, y + 8, x + 178, y + 25], fill=(210, 30, 25))
    elif idx == 2:  # Geneva robot + draft doc
        d.rectangle([x, y, x + w, y + h], fill=(214, 224, 232))
        # robot: head, body, arms, wheels
        d.rectangle([x + 22, y + 6, x + 62, y + 22], fill=(120, 130, 140),
                    outline=INK, width=1)
        d.ellipse([x + 32, y + 11, x + 38, y + 17], fill=(255, 255, 255))
        d.ellipse([x + 46, y + 11, x + 52, y + 17], fill=(255, 255, 255))
        d.line([x + 42, y + 6, x + 42, y + 1], fill=INK, width=2)
        d.rectangle([x + 16, y + 24, x + 68, y + 42], fill=(150, 160, 170),
                    outline=INK, width=1)
        d.rectangle([x + 30, y + 28, x + 54, y + 34], fill=(40, 80, 160))
        d.ellipse([x + 24, y + 42, x + 34, y + 48], fill=INK)
        d.ellipse([x + 50, y + 42, x + 60, y + 48], fill=INK)
        # draft doc
        d.rectangle([x + 110, y + 6, x + 158, y + h - 6], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.rectangle([x + 110, y + 6, x + 158, y + 14], fill=NAVY)
        for ly in (20, 26, 32):
            d.line([x + 116, y + ly, x + 152, y + ly], fill=(150, 150, 150),
                   width=2)
    elif idx == 3:  # Chapo: Mexico map + CAPTURED stamp + badge
        d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
        d.polygon([(x + 20, y + 8), (x + 90, y + 6), (x + 150, y + 12),
                   (x + 168, y + 26), (x + 150, y + 40), (x + 90, y + 44),
                   (x + 40, y + 38), (x + 18, y + 24)], fill=(200, 170, 120))
        d.ellipse([x + 66, y + 18, x + 74, y + 26], fill=RED,
                  outline=(255, 255, 255), width=1)
        # badge star
        bx, by = x + 178, y + 12
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=GOLD, outline=INK,
                  width=1)
        d.text((bx - 3, by - 6), "*", font=bc_b(12), fill=INK)
    elif idx == 4:  # BepiColombo at Mercury: cratered planet + probe
        d.rectangle([x, y, x + w, y + h], fill=(12, 14, 28))
        for sx, sy in [(20, 10), (60, 22), (110, 8), (160, 16), (40, 34),
                       (140, 30)]:
            d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                      fill=(255, 255, 255))
        d.ellipse([x + 18, y + 8, x + 82, y + h - 6], fill=(168, 158, 142),
                  outline=(120, 110, 96), width=1)
        for cx, cy, cr in [(34, 20, 6), (58, 16, 4), (44, 34, 5), (64, 30, 3),
                           (30, 34, 3)]:
            d.ellipse([x + cx - cr, y + cy - cr, x + cx + cr, y + cy + cr],
                      fill=(140, 130, 116))
        d.rectangle([x + 120, y + 20, x + 140, y + 34], fill=(200, 200, 200),
                    outline=INK, width=1)
        d.rectangle([x + 96, y + 24, x + 120, y + 30], fill=(40, 80, 160))
        d.rectangle([x + 140, y + 24, x + 164, y + 30], fill=(40, 80, 160))
        d.line([x + 140, y + 27, x + 168, y + 27], fill=(250, 200, 60), width=2)
    elif idx == 5:  # France marches: crowd silhouettes + placards
        d.rectangle([x, y, x + w, y + h], fill=(222, 226, 232))
        # Eiffel-tower silhouette, left
        d.polygon([(x + 14, y + h), (x + 28, y + 6), (x + 42, y + h)],
                  fill=(60, 60, 70))
        d.rectangle([x + 18, y + 30, x + 38, y + 34], fill=(222, 226, 232))
        # placards
        for px, col in [(70, RED), (120, NAVY), (160, RED)]:
            d.line([x + px + 8, y + 14, x + px + 8, y + 34], fill=INK, width=2)
            d.rectangle([x + px, y + 6, x + px + 18, y + 16], fill=(255, 255, 255),
                        outline=col, width=1)
        # crowd: heads + shoulders along the bottom
        for hx in range(60, 190, 16):
            d.ellipse([x + hx - 4, y + 30, x + hx + 4, y + 38], fill=(40, 40, 50))
            d.rectangle([x + hx - 7, y + 38, x + hx + 7, y + h],
                        fill=(40, 40, 50))
    elif idx == 6:  # Rugby: goal posts + ball + scoreboard
        d.rectangle([x, y, x + w, y + h], fill=(120, 170, 90))
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 130, 60))
        for ly in (8, 20, 32):
            d.line([x, y + ly, x + w, y + ly], fill=(255, 255, 255), width=1)
        # goal posts
        d.line([x + 84, y + 8, x + 84, y + 40], fill=(255, 255, 255), width=3)
        d.line([x + 108, y + 8, x + 108, y + 40], fill=(255, 255, 255), width=3)
        d.line([x + 84, y + 24, x + 108, y + 24], fill=(255, 255, 255), width=3)
        # ball
        d.ellipse([x + 140, y + 28, x + 168, y + 42], fill=(180, 30, 20))
        d.line([x + 144, y + 32, x + 164, y + 38], fill=(255, 255, 255), width=1)
        # scoreboard
        d.rectangle([x + 8, y + 6, x + 62, y + 20], fill=NAVY)
        d.text((x + 12, y + 8), "37\u201312", font=bc_b(11),
               fill=(255, 255, 255))
    elif idx == 7:  # CAF: football + pitch
        d.rectangle([x, y, x + w, y + h], fill=(30, 60, 40))
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(46, 125, 50))
        d.line([x, y + h - 10, x + w, y + h - 10], fill=(255, 255, 255),
               width=1)
        d.ellipse([x + 18, y + 8, x + 58, y + 48], fill=(255, 255, 255),
                  outline=INK, width=1)
        for px, py in [(38, 18), (28, 30), (48, 30), (38, 40)]:
            d.ellipse([x + px - 3, y + py - 3, x + px + 3, y + py + 3],
                      fill=INK)
        d.rectangle([x + 120, y + 10, x + 182, y + 30], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.text((x + 126, y + 13), "54 / 54", font=bc_b(12), fill=RED_DARK)
    elif idx == 8:  # Basra: power station + flames
        d.rectangle([x, y, x + w, y + h], fill=(40, 36, 34))
        # cooling towers
        for tx in (20, 62, 104):
            d.polygon([(x + tx, y + h), (x + tx + 6, y + 14),
                       (x + tx + 28, y + 14), (x + tx + 34, y + h)],
                      fill=(120, 120, 120))
        # chimney
        d.rectangle([x + 150, y + 8, x + 160, y + h], fill=(90, 90, 90))
        # flames
        for fx in (36, 78, 120):
            for dx, dy in [(0, 0), (6, -6), (-6, -5), (5, 5), (-5, 6)]:
                d.line([x + fx, y + 12, x + fx + dx, y + 12 + dy],
                       fill=(255, 170, 40), width=2)
        # smoke
        for sx, sy, sr in [(40, 4, 4), (80, 2, 5), (120, 4, 4)]:
            d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                      fill=(150, 150, 150))
    else:  # Taiwan: island + jets crossing a dashed median line
        d.rectangle([x, y, x + w, y + h], fill=(170, 205, 220))
        # dashed median line
        for ly in range(4, h - 2, 8):
            d.line([x + 96, y + ly, x + 96, y + ly + 4], fill=RED, width=2)
        # Taiwan island
        d.polygon([(x + 108, y + 6), (x + 122, y + 4), (x + 130, y + 16),
                   (x + 126, y + 34), (x + 116, y + 46), (x + 106, y + 30)],
                  fill=TAN)
        # jets (small triangles) + trails
        for jx, jy in [(30, 14), (52, 26), (74, 12)]:
            d.polygon([(x + jx, y + jy), (x + jx + 12, y + jy + 4),
                       (x + jx, y + jy + 8)], fill=(30, 30, 40))
            d.line([x + jx - 14, y + jy + 4, x + jx, y + jy + 4],
                   fill=(255, 255, 255), width=1)
        d.text((x + 140, y + 8), "15", font=bc_b(14), fill=RED_DARK)


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
    count = "35 STORIES \u00b7 9 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    f = bc_sb(13)
    d.text((1010 - f.getlength(count), 14), count, font=f, fill=INK)
    d.line([14, 36, 1010, 36], fill=INK, width=2)
    date_f = fit_font_size("Saturday 21 November 2026",
                           "PlayfairDisplay-Black.ttf", 84, 980)
    dw = date_f.getlength("Saturday 21 November 2026")
    d.text(((1024 - dw) / 2, 42), "Saturday 21 November 2026",
           font=date_f, fill=INK)
    sf = nr(19)
    sw = sf.getlength(SUBHEAD)
    d.text(((1024 - sw) / 2, 130), SUBHEAD, font=sf, fill=INK)
    d.line([14, 150, 1010, 150], fill=INK, width=1)


def draw_numbers(d):
    cell_w = 996 / 6
    for i, (num, cap1, cap2) in enumerate(NUMBERS):
        cx = 14 + cell_w * i + cell_w / 2
        nf = pf_black(30)
        nw = nf.getlength(num)
        d.text((cx - nw / 2, 154), num, font=nf, fill=RED)
        cf = bc_m(10)
        for j, cap in enumerate((cap1, cap2)):
            cw = cf.getlength(cap)
            d.text((cx - cw / 2, 186 + j * 12), cap, font=cf, fill=INK)
        if i:
            d.line([14 + cell_w * i, 158, 14 + cell_w * i, 208],
                   fill=(200, 195, 180), width=1)


def draw_region_bar(d):
    seg_w = 996 / 9
    x = 14
    for name, count, color in REGION_COLORS:
        d.rectangle([x, 212, x + seg_w, 230], fill=color)
        label = f"{name} {count}"
        f = bc_b(11)
        tw = f.getlength(label)
        d.text((x + (seg_w - tw) / 2, 216), label, font=f,
               fill=(255, 255, 255))
        x += seg_w


def draw_timeline(d):
    d.rectangle([14, 232, 1010, 245], fill=NAVY)
    lf = bc_b(9)
    label = "THE DAY IN UTC"
    d.text((20, 234), label, font=lf, fill=(255, 255, 255))
    tf = nr(9)
    d.text((20 + lf.getlength(label) + 10, 234), TIMELINE, font=tf,
           fill=(255, 255, 255))


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
    for num, lon, lat, dx, dy, color in PINS:
        px, py = lonlat_to_xy(lon, lat, mx, my, mw, mh)
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=color,
                  outline=(255, 255, 255), width=1)
        tf = bc_b(10)
        t = str(num)
        d.text((px - tf.getlength(t) / 2, py - 7), t, font=tf,
               fill=(255, 255, 255))
    d.text((mx + 6, my + mh - 14),
           "Pins 1\u201313 mark the pictured stories; pin colour is the region. "
           "8 is in space: Mercury.",
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
    f = nr(10.5)
    d.text((22, y + 4), DATE_CHECK_L1, font=f, fill=INK)
    d.text((22, y + 18), DATE_CHECK_L2, font=f, fill=INK)


def build(quality=82):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, 1018, 1018], outline=INK, width=2)
    draw_masthead(d)
    draw_numbers(d)
    draw_region_bar(d)
    draw_timeline(d)
    lead_y, lead_h = 246, 110
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
