#!/usr/bin/env python3
"""News Image 25 Nov 2026 — REVISI VISUAL (v2).

Fresh rewrite for the visual revision Ale asked for after seeing v1:
bigger, more dramatic lead scenes, richer colours, bolder headlines,
a TOP STORY flare, more detailed secondary scenes, gold masthead accent.

CONTENT IS UNCHANGED from v1: same 45 stories, same text, same sources,
same numbers (stats, tally 8/10/6/9/6/2/4 = 45, 13 map pins + index,
12 DATE CHECK items), same numbering 1-45, same order. Only the drawing
is richer. All facts come from the research dossier; every illustration
is drawn by this code.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "news.png"

# ---------- palette ----------
PAPER = (253, 252, 247)
INK = (17, 17, 17)
GREY = (90, 90, 86)
RED = (200, 16, 46)
DARKRED = (158, 10, 34)
GOLD = (201, 162, 39)
GOLD_D = (170, 132, 18)
NAVY = (18, 38, 74)
SKY1 = (176, 210, 236)
SKY2 = (233, 243, 251)
SEA1 = (52, 116, 182)
SEA2 = (28, 76, 134)
SAND = (233, 218, 176)
GROUND = (214, 196, 150)
GRASS = (178, 206, 128)
LAND = (166, 200, 116)
LAND_D = (140, 182, 96)
OCEAN = (180, 215, 236)
GRID = (146, 184, 208)
ORANGE = (238, 120, 30)
YELLOW = (250, 196, 60)
BROWN = (139, 94, 52)
STEEL = (120, 124, 130)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(size, bold=False, serif=False):
    path = (SERIF_B if serif else SANS_B) if bold else (SERIF if serif else SANS)
    if not os.path.exists(path):
        path = ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if serif
                else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") if bold else (
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf" if serif
                else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(path, int(size))


def wrap(d, text, font, max_w):
    """Greedy word wrap using real font metrics."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(d, box, c1, c2):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / h
        c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def para(d, x, y, max_w, text, font, fill, lh):
    lines = wrap(d, text, font, max_w)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------- content: UNCHANGED from v1 ----------
DATE_LINE = ("DATE CHECK: Wednesday 25 November 2026 — today's news, as reported "
             "today; earlier events are dated in the text.")

STATS = [
    ("KOSPI", "-6.16%", "4,697.51 \u2022 SEOUL"),
    ("NIKKEI", "-2.78%", "57,011.62 \u2022 TOKYO"),
    ("TAIEX", "-4.80%", "38,195.43 \u2022 TAIPEI"),
    ("BRENT", "~$90.97", "-0.5% \u2022 WED 25 NOV"),
    ("GOLD", "~$3,548", "-0.4% \u2022 WED 25 NOV"),
    ("BITCOIN", "~$59,145", "-1.18% \u2022 WED 25 NOV"),
]
TALLY = "N. AMERICA 8 \u2022 EUROPE 10 \u2022 MIDDLE EAST 6 \u2022 ASIA 9 \u2022 AFRICA 6 \u2022 S. AMERICA 2 \u2022 OCEANIA 4"

LEADS = [
    dict(kicker="1 \u2022 GULF \u2022 STRAIT OF HORMUZ",
         head="IRAN CLAIMS TWO TANKERS HIT MINES IN HORMUZ",
         body=("Iran's Revolutionary Guard said on Wednesday that two oil tankers struck "
               "sea mines, exploded and caught fire in the Strait of Hormuz on what it "
               "called an unofficial route. The mine claim could not be independently "
               "verified. Oil prices moved on the news."),
         src="Reuters \u2022 Just Security", scene="hormuz"),
    dict(kicker="2 \u2022 TRADE \u2022 WASHINGTON",
         head="US ANNOUNCES NEW TARIFFS, CHINA AMONG TARGETS",
         body=("The Trump administration announced new tariffs on Wednesday against a host "
               "of trading partners including China, after a Section 301 probe into alleged "
               "subsidies and overcapacity in 16 economies. Specific rates had not been "
               "announced when the first reports landed."),
         src="BBC \u2022 AP", scene="tariffs"),
    dict(kicker="3 \u2022 MARKETS \u2022 SEOUL",
         head="ASIAN MARKETS TUMBLE: KOSPI -6.16% IN AI ROUT",
         body=("Asian stocks fell sharply on Wednesday as the AI sell-off deepened. Seoul's "
               "KOSPI plunged 6.16% to 4,697.51, wiping out the previous day's 6.32% gain; "
               "Samsung fell 9.9% and SK Hynix 11.1%. Taiwan's Taiex fell 4.80% and "
               "Tokyo's Nikkei 2.78%."),
         src="AP \u2022 Reuters", scene="markets"),
]

SECONDARIES = [
    dict(kicker="4 \u2022 RUSSIA \u2022 WAR",
         head="UKRAINIAN DRONES SET TWO REFINERIES ABLAZE",
         body=("Kyiv said overnight drones hit two Rosneft refineries in Samara, starting "
               "big fires. One person was killed; Reuters could not verify which plants "
               "burned."),
         src="Reuters", scene="refinery"),
    dict(kicker="5 \u2022 GAZA \u2022 WAR",
         head="ISRAEL KILLS SENIOR HAMAS SECURITY CHIEF IN GAZA",
         body=("An Israeli strike killed Hamas colonel Mohammad Abuelouf, who ran the "
               "group's internal security, with his wife and two children at Beach camp "
               "in Gaza."),
         src="Reuters", scene="gaza"),
    dict(kicker="6 \u2022 COLOMBIA \u2022 HOSTAGES",
         head="ALL HOSTAGES FREED IN CARTAGENA SUPERMARKET RAID",
         body=("Colombian forces stormed an \u00c9xito supermarket early on Wednesday, "
               "freeing the last 20 hostages and killing one kidnapper after a 17-hour "
               "siege."),
         src="Reuters \u2022 AFP \u2022 BBC", scene="cartagena"),
    dict(kicker="7 \u2022 SPACE \u2022 CHINA",
         head="SHENZHOU-24 CARRIES FIRST PAKISTANI TO TIANGONG",
         body=("China launched Shenzhou-24 from Jiuquan carrying two Chinese astronauts "
               "and Pakistan's Muhammad Zeeshan Ali, the first foreign visitor to "
               "Tiangong station."),
         src="AP \u2022 BBC", scene="rocket"),
    dict(kicker="8 \u2022 PACIFIC \u2022 TREATY",
         head="SOLOMON ISLANDS SIGNS AUSTRALIA TREATY",
         body=("Solomon Islands and Australia signed a treaty in Canberra making Australia "
               "the islands' 'principal security partner' and barring foreign military "
               "bases."),
         src="AP \u2022 NYT \u2022 BBC", scene="treaty"),
    dict(kicker="9 \u2022 BANGLADESH \u2022 WAGES",
         head="BANGLADESH RAISES GARMENT WAGE 36% AFTER PROTESTS",
         body=("Bangladesh raised the garment minimum wage 36% to 17,000 taka (~US$136) "
               "after a 12-hour wage-board session. Workers wanting more blocked roads "
               "in Gazipur."),
         src="AP \u2022 Reuters", scene="factory"),
    dict(kicker="10 \u2022 INDONESIA \u2022 MINE",
         head="THREE BODIES FOUND IN FLOODED BOGOR GOLD MINE",
         body=("Rescuers found three bodies on Wednesday in the search for miners trapped "
               "since Monday when rain flooded an unlicensed gold mine in Bogor. "
               "Twenty-three are still missing."),
         src="AP \u2022 Reuters", scene="mine"),
    dict(kicker="11 \u2022 SUDAN \u2022 WAR",
         head="RSF DRONE STRIKES KILL 19 CIVILIANS IN SUDAN",
         body=("RSF drones killed 19 civilians, including six women, and wounded 20 in "
               "Damazin and Roseires, Sudanese rights lawyers said on Wednesday."),
         src="Reuters", scene="sudan"),
    dict(kicker="12 \u2022 EUROPE \u2022 RAIL",
         head="EUROSTAR STRIKE CANCELS PARIS-LONDON TRAINS",
         body=("Paris-based Eurostar staff walked out without notice in a pay dispute, "
               "cancelling morning trains both ways. About four in five services still "
               "ran."),
         src="AP", scene="train"),
    dict(kicker="13 \u2022 S. AFRICA \u2022 COURTS",
         head="RAMAPHOSA WINS COURT FIGHT OVER IMPEACHMENT",
         body=("President Cyril Ramaphosa won a court battle over the Phala Phala "
               "impeachment threat when a court set aside the impeachment report \u2014 "
               "for now."),
         src="BBC", scene="court"),
]

DATECHECK = [
    "Huawei convicted of trade-secret conspiracy (Tue 24)",
    "Unclassified CIA & ODNI systems breached (Tue 24)",
    "Houthi drone hits Riyadh tower; 11 hurt (Tue 24)",
    "Two Libyan officers die of Benghazi wounds (Tue 24)",
    "Cessna crash off Mississippi kills 6, incl. children (Tue 24)",
    "CAS restores AFCON 2025 title to Senegal (Tue 24)",
    "Dell posts record Q3: revenue $54.9bn (Tue 24)",
    "Democrats win House majority, 259 seats (Tue 24)",
    "Thomas Markle charged in US federal court (Tue 24)",
    "Zelensky: Ukraine needs \u20ac115bn foreign aid for 2027",
    "Russian strikes on Odesa/Kyiv overnight: 2 killed (24\u201325 Nov)",
    "BBC analysis: Russia has lost 490,334+ troops since 2022",
]

PINS = [
    (1, "Hormuz", 26.5, 56.3), (2, "Washington", 38.9, -77.0),
    (3, "Seoul", 37.6, 127.0), (4, "Samara", 53.2, 50.1),
    (5, "Gaza", 31.5, 34.47), (6, "Cartagena", 10.4, -75.5),
    (7, "Jiuquan", 39.7, 98.5), (8, "Canberra", -35.3, 149.1),
    (9, "Dhaka", 23.8, 90.4), (10, "Bogor", -6.6, 106.8),
    (11, "Damazin", 11.8, 34.35), (12, "Paris", 48.85, 2.35),
    (13, "Pretoria", -25.7, 28.2),
]

# (num, city, headline, subline, glyph)
BRIEFS = [
    (14, "MADRID", "\u00c1brego Garc\u00eda reaches Spain",
     "Ending the Trump deportation battle. BBC \u2022 AP", "plane"),
    (15, "IOWA", "Army to blast unstable explosives",
     "Unstable lead azide, day before Thanksgiving. AP", "warn"),
    (16, "USA", "81.5m travel for Thanksgiving",
     "Busiest Thanksgiving flying in 16 years. AP", "plane"),
    (17, "WASHINGTON", "Melania reunites 7th group",
     "Ukrainian, Russian children; total now 43. AP", "people"),
    (18, "USA", "Pentagon to audit military schools",
     "Conservative contractors; 'classical' PE pilot. AP", "building"),
    (19, "USA", "GoFundMe warns donors of breach",
     "Scale of data exposed not yet confirmed. AP", "coin"),
    (20, "SEATTLE", "Amazon buys Decart for AI chips",
     "Software bet to catch Nvidia. Principia", "chip"),
    (21, "EUROZONE", "Inflation rises to 4.0%",
     "Growth and jobs data also released. Principia", "chart"),
    (22, "BERLIN", "Merz: Russia 'escalating' threat",
     "Defends defence spending and Ukraine aid. Reuters", "flag"),
    (23, "BERLIN", "Germany weighs US troop drawdown",
     "Officials meet on offsetting a US pullback. POLITICO", "scales"),
    (24, "PARIS", "Sarkozy, Carla Bruni to face trial",
     "Charges and trial date not yet confirmed. BBC", "gavel"),
    (25, "LONDON", "UK energy bills to rise 26%",
     "Typical bill \u00a31,723 to \u00a32,166 from January. BBC", "bolt"),
    (26, "LUTON", "EasyJet profit falls 89%",
     "\u00a3244m fuel hit; older jets retired faster. Principia", "plane"),
    (27, "NORFOLK", "Two charged over William break-in",
     "Charged over Monday's raid at Anmer Hall. AP \u2022 BBC", "scales"),
    (28, "VATICAN", "Pope dismayed at COP31 failure",
     "Pope: extreme weather 'growing more frequent'. AP", "globe"),
    (29, "RAS TANURA", "Houthis claim refinery strike",
     "Riyadh: 4 drones downed; hit unconfirmed. Reuters", "building"),
    (30, "BENGHAZI", "Libya vows revenge on Ukraine",
     "Two officers died of Sunday's wounds. AP \u2022 Reuters", "flag"),
    (31, "TEHRAN", "Iran 'not worried' over blockade",
     "Aref cites rising cargo via other borders. Reuters", "ship"),
    (32, "ISLAMABAD", "Pakistan warns of energy crisis",
     "Warning reported by SRI; single source. SRI", "bolt"),
    (33, "SHANGHAI", "China probes party chief Chen",
     "Politburo member probed. Daily Summary", "building"),
    (34, "SEOUL", "Russian jets entered air zone",
     "Jets and date not confirmed; single source. SRI", "plane"),
    (35, "INDIA", "The rising cost of food",
     "Household food-price pressure mounts. BBC", "chart"),
    (36, "TOKYO", "Services inflation at 36-year high",
     "Services prices +4.2% in Oct; BOJ rise seen. Reuters", "chart"),
    (37, "N. KOREA", "Jailed for being Christian",
     "Witnesses: spied on, beaten, jailed. BBC", "people"),
    (38, "ITURI", "Fighting traps Ebola responders",
     "WHO concern as violence deepens. PANA \u2022 WHO", "cross"),
    (39, "HARARE", "Mugabe's son faces arrest warrant",
     "Warrant over a missed court date. BBC", "scales"),
    (40, "DAKAR", "CAF: Senegal are AFCON champions",
     "CAS restored Senegal's 1\u20130 final win. BBC", "trophy"),
    (41, "NIGERIA", "Nollywood's Pete Edochie dies, 79",
     "Veteran Nollywood actor dies at 79. BBC", "film"),
    (42, "QUITO", "US pauses Ecuador joint operations",
     "Pause dates to mid-October, sources say. Atlantic", "scales"),
    (43, "CANBERRA", "Australian inflation hits 4.9%",
     "Fuel drove the rise; RBA expected to hold. Principia", "chart"),
    (44, "CANBERRA", "Online safety law passes",
     "Big Tech faces multibillion-dollar fines. AP", "chip"),
    (45, "WELLINGTON", "NZ netball league collapses",
     "Players left in limbo as league folds. BBC", "globe"),
]

FOOT_SRC = ("Sources: Reuters \u2022 AP \u2022 BBC \u2022 NYT \u2022 Just Security \u2022 "
            "POLITICO \u2022 Principia \u2022 Sharecast \u2022 PANA \u2022 The Atlantic")
FOOT_TAG = ("All the day's news, in one image \u2014 Wednesday 25 November 2026 \u2022 "
            "Rounds: blind \u2014 final heat: 3 Swiss rounds + playoff (top 52)")


# ---------- fixed stickman character (same figure in every scene) ----------
def stick(d, x, y, h, pose="stand", shirt=RED, tie=False, helmet=False,
          cap=False):
    """Stickman standing on ground point (x, y), total height h.
    Red torso, black limbs, 2px outline. Poses: stand, wave, panic,
    point, row, shake, cheer, walk."""
    hr = max(3, int(h * 0.11))
    cx, cy = x, y - h + hr
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], outline=INK, width=2,
              fill=(255, 255, 255))
    if helmet:  # orange rescuer helmet
        d.pieslice([cx - hr - 1, cy - hr - 2, cx + hr + 1, cy + 1], 180, 360,
                   fill=ORANGE, outline=INK)
    if cap:  # navy sailor cap
        d.pieslice([cx - hr - 1, cy - hr - 1, cx + hr + 1, cy + 1], 180, 360,
                   fill=NAVY, outline=INK)
        d.line([cx + hr - 1, cy - 1, cx + hr + 4, cy - 1], fill=INK, width=2)
    top = cy + hr
    bot = y - int(h * 0.36)
    d.line([x, top, x, bot], fill=shirt, width=4)
    if tie:
        d.line([x, top + 2, x, bot - 2], fill=INK, width=2)
    lw = 2
    if pose == "stand":
        d.line([x, top + 3, x - int(h * 0.14), top + int(h * 0.22)], fill=INK, width=lw)
        d.line([x, top + 3, x + int(h * 0.14), top + int(h * 0.22)], fill=INK, width=lw)
        d.line([x, bot, x - int(h * 0.15), y], fill=INK, width=lw)
        d.line([x, bot, x + int(h * 0.15), y], fill=INK, width=lw)
    elif pose == "wave":
        d.line([x, top + 3, x - int(h * 0.14), top + int(h * 0.22)], fill=INK, width=lw)
        d.line([x, top + 3, x + int(h * 0.16), top - int(h * 0.10)], fill=INK, width=lw)
        d.line([x, bot, x - int(h * 0.15), y], fill=INK, width=lw)
        d.line([x, bot, x + int(h * 0.15), y], fill=INK, width=lw)
    elif pose == "panic":
        d.line([x, top + 3, x - int(h * 0.18), top - int(h * 0.14)], fill=INK, width=lw)
        d.line([x, top + 3, x + int(h * 0.18), top - int(h * 0.14)], fill=INK, width=lw)
        d.line([x, bot, x - int(h * 0.13), y], fill=INK, width=lw)
        d.line([x, bot, x + int(h * 0.17), y - int(h * 0.06)], fill=INK, width=lw)
    elif pose == "point":
        d.line([x, top + 3, x - int(h * 0.14), top + int(h * 0.22)], fill=INK, width=lw)
        d.line([x, top + 3, x + int(h * 0.20), top + int(h * 0.05)], fill=INK, width=lw)
        d.line([x, bot, x - int(h * 0.15), y], fill=INK, width=lw)
        d.line([x, bot, x + int(h * 0.15), y], fill=INK, width=lw)
    elif pose == "row":
        d.line([x, top + 3, x + int(h * 0.20), top + int(h * 0.18)], fill=INK, width=lw)
        d.line([x, top + 3, x + int(h * 0.16), top + int(h * 0.24)], fill=INK, width=lw)
        d.line([x, bot, x - int(h * 0.12), y], fill=INK, width=lw)
        d.line([x, bot, x + int(h * 0.12), y], fill=INK, width=lw)
    elif pose == "shake":
        d.line([x, top + 3, x - int(h * 0.14), top + int(h * 0.22)], fill=INK, width=lw)
        d.line([x, top + 3, x + int(h * 0.20), top + int(h * 0.10)], fill=INK, width=lw)
        d.line([x, bot, x - int(h * 0.15), y], fill=INK, width=lw)
        d.line([x, bot, x + int(h * 0.15), y], fill=INK, width=lw)
    elif pose == "cheer":
        d.line([x, top + 3, x - int(h * 0.20), top - int(h * 0.16)], fill=INK, width=lw)
        d.line([x, top + 3, x + int(h * 0.20), top - int(h * 0.16)], fill=INK, width=lw)
        d.line([x, bot, x - int(h * 0.16), y], fill=INK, width=lw)
        d.line([x, bot, x + int(h * 0.16), y], fill=INK, width=lw)
    elif pose == "walk":
        d.line([x, top + 3, x - int(h * 0.16), top + int(h * 0.18)], fill=INK, width=lw)
        d.line([x, top + 3, x + int(h * 0.16), top + int(h * 0.18)], fill=INK, width=lw)
        d.line([x, bot, x - int(h * 0.18), y - int(h * 0.04)], fill=INK, width=lw)
        d.line([x, bot, x + int(h * 0.14), y], fill=INK, width=lw)


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1, fill=(255, 255, 255))
    for i in range(7):
        yy = y + i * h / 7
        if i % 2 == 0:
            d.rectangle([x, yy, x + w, yy + h / 7], fill=RED)
    cw, ch = w * 0.42, h * 0.54
    d.rectangle([x, y, x + cw, y + ch], fill=NAVY)
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 3 + c * (cw - 6) / 3, y + 3 + r * (ch - 6) / 2,
                       x + 6 + c * (cw - 6) / 3, y + 6 + r * (ch - 6) / 2],
                      fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1, fill=RED)
    star(d, x + w * 0.22, y + h * 0.28, max(3, int(h * 0.16)), YELLOW)
    for sx, sy in [(0.55, 0.15), (0.68, 0.30), (0.68, 0.48), (0.55, 0.62)]:
        star(d, x + w * sx, y + h * sy, max(2, int(h * 0.09)), YELLOW)


def cloud(d, x, y, s):
    d.ellipse([x, y, x + s, y + s * 0.55], fill=(255, 255, 255), outline=(200, 215, 230))
    d.ellipse([x + s * 0.3, y - s * 0.25, x + s * 1.1, y + s * 0.4],
              fill=(255, 255, 255), outline=(200, 215, 230))


def explosion(d, cx, cy, r):
    star(d, cx, cy, r, ORANGE)
    star(d, cx, cy, int(r * 0.62), YELLOW)
    star(d, cx, cy, int(r * 0.34), (255, 240, 180))
    for dx, dy, rr in [(-r, -r * 0.7, 7), (r * 0.8, -r * 0.9, 8), (r * 0.3, -r * 1.2, 6),
                       (-r * 0.5, r * 0.8, 6)]:
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                  fill=(120, 120, 120), outline=(90, 90, 90))


def mine(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    for k in range(8):
        a = k * math.pi / 4
        d.line([cx + (r - 1) * math.cos(a), cy + (r - 1) * math.sin(a),
                cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a)],
               fill=INK, width=2)


# ---------- LEAD SCENES (bigger, more dramatic than v1) ----------
def scene_hormuz(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    sea_y = y0 + int((y1 - y0) * 0.52)
    vgrad(d, (x0, y0, x1, sea_y), SKY1, SKY2)
    vgrad(d, (x0, sea_y, x1, y1), SEA1, SEA2)
    d.line([x0, sea_y, x1, sea_y], fill=(255, 255, 255), width=1)
    # sun with rays
    sx, sy = x1 - 34, y0 + 20
    d.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=YELLOW, outline=ORANGE, width=2)
    for k in range(8):
        a = k * math.pi / 4
        d.line([sx + 15 * math.cos(a), sy + 15 * math.sin(a),
                sx + 21 * math.cos(a), sy + 21 * math.sin(a)], fill=ORANGE, width=2)
    cloud(d, x0 + 18, y0 + 12, 34)
    cloud(d, x0 + 150, y0 + 6, 26)
    # waves
    for wy in (sea_y + 14, sea_y + 30, sea_y + 46):
        for wx in range(x0 + 8, x1 - 8, 34):
            d.arc([wx, wy, wx + 22, wy + 12], 180, 360, fill=(200, 225, 245), width=2)
    # tanker 1 (left, sailor aboard)
    tx, ty, tw = x0 + 16, sea_y + 6, 128
    d.polygon([(tx, ty), (tx + tw, ty), (tx + tw - 14, ty + 22), (tx + 10, ty + 22)],
              fill=(178, 30, 44), outline=INK)
    d.rectangle([tx + 18, ty - 16, tx + 58, ty], fill=(245, 245, 240), outline=INK)
    d.rectangle([tx + 66, ty - 10, tx + 78, ty], fill=INK)
    stick(d, tx + 96, ty - 2, 30, pose="panic", cap=True)
    # tanker 2 (right) with big explosion
    tx2, ty2, tw2 = x0 + 176, sea_y + 10, 118
    d.polygon([(tx2, ty2), (tx2 + tw2, ty2), (tx2 + tw2 - 12, ty2 + 20),
               (tx2 + 8, ty2 + 20)], fill=(178, 30, 44), outline=INK)
    d.rectangle([tx2 + 16, ty2 - 14, tx2 + 52, ty2], fill=(245, 245, 240), outline=INK)
    explosion(d, tx2 + 78, ty2 - 22, 26)
    # mine in the water
    mine(d, x0 + 158, sea_y + 40, 8)
    # lifeboat with rower, bottom-left
    bx, by = x0 + 22, y1 - 8
    d.polygon([(bx, by), (bx + 44, by), (bx + 38, by - 10), (bx + 6, by - 10)],
              fill=ORANGE, outline=INK)
    stick(d, bx + 22, by - 8, 22, pose="row", shirt=NAVY)
    d.line([bx + 34, by - 16, bx + 52, by - 2], fill=INK, width=2)


def scene_tariffs(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    floor_y = y0 + int((y1 - y0) * 0.62)
    vgrad(d, (x0, y0, x1, floor_y), (238, 236, 228), (226, 222, 210))
    d.rectangle([x0, floor_y, x1, y1], fill=(206, 186, 150))
    d.line([x0, floor_y, x1, floor_y], fill=BROWN, width=2)
    # flags on poles
    d.line([x0 + 22, y0 + 10, x0 + 22, floor_y], fill=INK, width=3)
    flag_us(d, x0 + 24, y0 + 12, 44, 28)
    d.line([x1 - 24, y0 + 10, x1 - 24, floor_y], fill=INK, width=3)
    flag_cn(d, x1 - 68, y0 + 12, 44, 28)
    # two negotiators facing each other, standing BEHIND the table
    stick(d, x0 + 78, floor_y, 52, pose="shake", tie=True)
    stick(d, x1 - 118, floor_y, 52, pose="shake", cap=True)
    # table (drawn over their legs so they read as standing behind it)
    tx0, tx1, ty = x0 + 40, x1 - 40, floor_y - 26
    d.rectangle([tx0, ty, tx1, floor_y], fill=BROWN, outline=INK)
    d.rectangle([tx0 + 6, ty + 4, tx1 - 6, ty + 8], fill=(160, 112, 66))
    # document with big % on the table
    d.rectangle([x0 + 128, ty - 22, x0 + 178, ty], fill=(255, 255, 255), outline=INK)
    d.text((x0 + 136, ty - 21), "%", font=F(20, bold=True, serif=True), fill=RED)
    # briefcase
    d.rectangle([x1 - 96, ty - 16, x1 - 62, ty], fill=(110, 70, 35), outline=INK)
    d.arc([x1 - 88, ty - 22, x1 - 70, ty - 12], 180, 360, fill=INK, width=2)


def scene_markets(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    d.rectangle([x0, y0, x1, y1], fill=(250, 248, 242))
    for gx in range(x0 + 20, x1, 40):
        d.line([gx, y0, gx, y1], fill=(232, 228, 218), width=1)
    for gy in range(y0 + 18, y1, 26):
        d.line([x0, gy, x1, gy], fill=(232, 228, 218), width=1)
    # falling red line with arrow
    pts = [(x0 + 12, y0 + 26), (x0 + 70, y0 + 18), (x0 + 128, y0 + 34),
           (x0 + 186, y0 + 30), (x0 + 232, y0 + 58), (x0 + 276, y0 + 78),
           (x0 + 312, y0 + 100)]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.polygon([(x0 + 312, y0 + 100), (x0 + 298, y0 + 92), (x0 + 300, y0 + 106)],
              fill=RED)
    # red candles + blue squares along the fall
    for cx, cy, ch in [(x0 + 96, y0 + 40, 16), (x0 + 208, y0 + 62, 20), (x0 + 262, y0 + 86, 16)]:
        d.rectangle([cx, cy, cx + 14, cy + ch], fill=RED, outline=DARKRED)
        d.line([cx + 7, cy - 6, cx + 7, cy + ch + 6], fill=DARKRED, width=2)
    for cx, cy in [(x0 + 150, y0 + 52), (x0 + 240, y0 + 44)]:
        d.rectangle([cx, cy, cx + 13, cy + 13], fill=NAVY, outline=INK)
    # panicking trader
    stick(d, x0 + 46, y1 - 8, 46, pose="panic")
    # big red number
    d.text((x0 + 196, y0 + 4), "-6.16%", font=F(30, bold=True, serif=True), fill=RED)


# ---------- SECONDARY SCENES (sky + ground + landmark) ----------
def sec_base(d, x0, y0, x1, y1, ground=GROUND, night=False):
    sky2 = (18, 30, 64) if night else SKY2
    sky1 = (10, 18, 48) if night else SKY1
    gy = y0 + int((y1 - y0) * 0.58)
    vgrad(d, (x0, y0, x1, gy), sky1, sky2)
    d.rectangle([x0, gy, x1, y1], fill=ground)
    d.line([x0, gy, x1, gy], fill=(120, 100, 70), width=1)
    return gy


def drone(d, cx, cy, s=10):
    d.ellipse([cx - s, cy - 3, cx + s, cy + 3], fill=INK)
    d.line([cx - s - 4, cy - 5, cx + s + 4, cy - 5], fill=INK, width=2)
    d.line([cx - s - 4, cy + 5, cx + s + 4, cy + 5], fill=INK, width=2)


def flame(d, cx, cy, r):
    d.polygon([(cx, cy - r), (cx + r * 0.6, cy), (cx + r * 0.3, cy + r * 0.4),
               (cx - r * 0.3, cy + r * 0.4), (cx - r * 0.6, cy)], fill=ORANGE)
    d.polygon([(cx, cy - r * 0.55), (cx + r * 0.35, cy), (cx, cy + r * 0.3),
               (cx - r * 0.35, cy)], fill=YELLOW)


def smoke(d, cx, cy, r):
    for dx, dy, rr in [(0, 0, r), (-r, r * 0.5, r * 0.8), (r, r * 0.6, r * 0.7)]:
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                  fill=(150, 150, 150), outline=(110, 110, 110))


def sec_scene(d, x0, y0, x1, y1, kind):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    w, h = x1 - x0, y1 - y0
    if kind == "refinery":
        gy = sec_base(d, x0, y0, x1, y1)
        for tx in (x0 + 26, x0 + 62, x0 + 100):
            d.rectangle([tx, gy - 26, tx + 22, gy], fill=STEEL, outline=INK)
            d.rectangle([tx + 4, gy - 32, tx + 18, gy - 26], fill=STEEL, outline=INK)
            flame(d, tx + 11, gy - 36, 7)
        smoke(d, x0 + 150, gy - 30, 7)
        drone(d, x0 + 160, y0 + 12)
    elif kind == "gaza":
        gy = sec_base(d, x0, y0, x1, y1)
        d.rectangle([x0 + 22, gy - 24, x0 + 66, gy], fill=(196, 176, 140), outline=INK)
        d.rectangle([x0 + 74, gy - 16, x0 + 108, gy], fill=(178, 156, 120), outline=INK)
        for wx in (x0 + 30, x0 + 46):
            d.rectangle([wx, gy - 18, wx + 8, gy - 10], fill=NAVY)
        smoke(d, x0 + 140, gy - 26, 9)
        stick(d, x0 + 150, gy, 26, pose="walk", helmet=True)
    elif kind == "cartagena":
        gy = sec_base(d, x0, y0, x1, y1)
        d.rectangle([x0 + 30, gy - 26, x0 + 130, gy], fill=(70, 110, 180), outline=INK)
        d.rectangle([x0 + 30, gy - 26, x0 + 130, gy - 18], fill=(250, 250, 250), outline=INK)
        d.rectangle([x0 + 72, gy - 14, x0 + 88, gy], fill=(255, 255, 255), outline=INK)
        stick(d, x0 + 152, gy, 28, pose="shake", helmet=True)
        stick(d, x0 + 172, gy, 26, pose="wave")
    elif kind == "rocket":
        gy = sec_base(d, x0, y0, x1, y1, ground=(60, 60, 70), night=True)
        for sx, sy in [(x0 + 20, y0 + 10), (x0 + 60, y0 + 6), (x0 + 170, y0 + 12),
                       (x0 + 140, y0 + 20), (x0 + 30, y0 + 26)]:
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        d.ellipse([x0 + 12, y0 + 8, x0 + 30, y0 + 26], fill=(235, 235, 220), outline=INK)
        rx = x0 + 108
        d.polygon([(rx, y0 + 8), (rx + 8, y0 + 18), (rx + 8, gy - 12), (rx, gy - 12)],
                  fill=(245, 245, 245), outline=INK)
        d.polygon([(rx - 8, gy - 12), (rx, gy - 22), (rx + 8, gy - 12)],
                  fill=RED, outline=INK)
        flame(d, rx + 4, gy - 8, 9)
        stick(d, x0 + 152, gy, 24, pose="cheer")
    elif kind == "treaty":
        gy = sec_base(d, x0, y0, x1, y1, ground=GRASS)
        d.line([x0 + 24, y0 + 6, x0 + 24, gy], fill=INK, width=2)
        d.polygon([(x0 + 26, y0 + 8), (x0 + 52, y0 + 14), (x0 + 26, y0 + 22)],
                  fill=(40, 90, 170), outline=INK)
        d.rectangle([x0 + 78, gy - 12, x0 + 128, gy], fill=BROWN, outline=INK)
        d.rectangle([x0 + 92, gy - 22, x0 + 114, gy - 12], fill=(255, 255, 255), outline=INK)
        stick(d, x0 + 88, gy - 10, 26, pose="shake")
        stick(d, x0 + 120, gy - 10, 26, pose="shake", cap=True)
        d.line([x0 + 158, gy, x0 + 158, gy - 26], fill=BROWN, width=3)
        for a in (-50, -20, 10, 40):
            r = math.radians(a)
            d.line([x0 + 158, gy - 26, x0 + 158 + 16 * math.cos(r),
                    gy - 26 + 10 * math.sin(r)], fill=(40, 130, 60), width=2)
    elif kind == "factory":
        gy = sec_base(d, x0, y0, x1, y1)
        d.rectangle([x0 + 20, gy - 24, x0 + 100, gy], fill=STEEL, outline=INK)
        d.rectangle([x0 + 106, gy - 34, x0 + 116, gy], fill=STEEL, outline=INK)
        smoke(d, x0 + 111, gy - 40, 6)
        d.rectangle([x0 + 30, gy - 18, x0 + 42, gy - 8], fill=NAVY)
        d.rectangle([x0 + 50, gy - 18, x0 + 62, gy - 8], fill=NAVY)
        stick(d, x0 + 140, gy, 28, pose="wave")
        d.rectangle([x0 + 148, gy - 34, x0 + 178, gy - 20], fill=(255, 255, 255),
                    outline=RED)
        d.text((x0 + 152, gy - 33), "36%", font=F(10, bold=True), fill=RED)
    elif kind == "mine":
        gy = sec_base(d, x0, y0, x1, y1, ground=(150, 110, 70))
        d.polygon([(x0 + 30, gy), (x0 + 70, gy - 26), (x0 + 120, gy - 26),
                   (x0 + 160, gy)], fill=(120, 86, 52))
        d.ellipse([x0 + 78, gy - 22, x0 + 112, gy - 2], fill=(40, 110, 180),
                  outline=INK)
        d.line([x0 + 95, gy - 22, x0 + 95, gy - 34], fill=INK, width=2)
        stick(d, x0 + 150, gy, 28, pose="row", helmet=True)
    elif kind == "sudan":
        gy = sec_base(d, x0, y0, x1, y1)
        for hx in (x0 + 26, x0 + 78):
            d.rectangle([hx, gy - 16, hx + 40, gy], fill=(176, 132, 84), outline=INK)
            d.polygon([(hx - 3, gy - 16), (hx + 20, gy - 28), (hx + 43, gy - 16)],
                      fill=(140, 90, 50), outline=INK)
        smoke(d, x0 + 140, gy - 26, 8)
        drone(d, x0 + 128, y0 + 10)
        stick(d, x0 + 148, gy, 24, pose="panic")
    elif kind == "train":
        gy = sec_base(d, x0, y0, x1, y1)
        d.rectangle([x0 + 14, gy - 22, x0 + 150, gy - 4], fill=YELLOW, outline=INK)
        d.rectangle([x0 + 14, gy - 22, x0 + 150, gy - 14], fill=NAVY)
        for wx in range(x0 + 22, x0 + 144, 20):
            d.rectangle([wx, gy - 12, wx + 12, gy - 5], fill=(200, 225, 245),
                        outline=INK)
        d.ellipse([x0 + 30, gy - 3, x0 + 44, gy + 9], fill=INK)
        d.ellipse([x0 + 120, gy - 3, x0 + 134, gy + 9], fill=INK)
        stick(d, x0 + 168, gy, 26, pose="wave")
        d.rectangle([x0 + 176, gy - 34, x0 + 190, gy - 20], fill=(255, 255, 255),
                    outline=RED)
        d.text((x0 + 181, gy - 34), "!", font=F(12, bold=True), fill=RED)
    elif kind == "court":
        gy = sec_base(d, x0, y0, x1, y1)
        d.polygon([(x0 + 30, gy - 30), (x0 + 90, gy - 44), (x0 + 150, gy - 30)],
                  fill=(200, 200, 200), outline=INK)
        for cx in (x0 + 44, x0 + 74, x0 + 104, x0 + 134):
            d.rectangle([cx, gy - 28, cx + 8, gy], fill=(220, 220, 220), outline=INK)
        d.rectangle([x0 + 30, gy - 4, x0 + 150, gy], fill=(200, 200, 200), outline=INK)
        stick(d, x0 + 168, gy, 28, pose="stand", tie=True)
        d.line([x0 + 176, gy - 30, x0 + 190, gy - 18], fill=BROWN, width=3)
        d.rectangle([x0 + 172, gy - 18, x0 + 192, gy - 12], fill=BROWN, outline=INK)


# ---------- brief glyphs (16px line icons) ----------
def glyph(d, cx, cy, kind):
    s = 7
    if kind == "plane":
        d.line([cx - s, cy, cx + s, cy], fill=INK, width=2)
        d.line([cx, cy - s, cx, cy + s], fill=INK, width=2)
        d.polygon([(cx + s, cy), (cx + s - 4, cy - 3), (cx + s - 4, cy + 3)], fill=INK)
    elif kind == "warn":
        d.polygon([(cx, cy - s), (cx + s, cy + s), (cx - s, cy + s)], outline=INK, width=2)
        d.text((cx - 1, cy - 2), "!", font=F(9, bold=True), fill=INK)
    elif kind == "people":
        for dx in (-4, 4):
            d.ellipse([cx + dx - 3, cy - s, cx + dx + 3, cy - s + 6], outline=INK, width=2)
            d.arc([cx + dx - 4, cy - 2, cx + dx + 4, cy + s], 180, 360, fill=INK, width=2)
    elif kind == "building":
        d.rectangle([cx - s, cy - s, cx + s, cy + s], outline=INK, width=2)
        for bx in (-3, 3):
            d.rectangle([cx + bx - 2, cy - 4, cx + bx + 2, cy], fill=INK)
    elif kind == "coin":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=INK, width=2)
        d.text((cx - 3, cy - 5), "$", font=F(9, bold=True), fill=INK)
    elif kind == "chip":
        d.rectangle([cx - 5, cy - 5, cx + 5, cy + 5], outline=INK, width=2)
        for k in (-3, 0, 3):
            d.line([cx + k, cy - s, cx + k, cy - 5], fill=INK, width=1)
            d.line([cx + k, cy + 5, cx + k, cy + s], fill=INK, width=1)
    elif kind == "chart":
        d.line([cx - s, cy + s, cx - s, cy - s], fill=INK, width=2)
        d.line([cx - s, cy + s, cx + s, cy + s], fill=INK, width=2)
        d.line([(cx - s + 1, cy + 2), (cx - 1, cy - 2), (cx + 2, cy + 1),
                (cx + s - 1, cy - s + 2)], fill=RED, width=2)
    elif kind == "flag":
        d.line([cx - 5, cy - s, cx - 5, cy + s], fill=INK, width=2)
        d.polygon([(cx - 5, cy - s), (cx + s, cy - s + 4), (cx - 5, cy - s + 8)],
                  fill=RED, outline=INK)
    elif kind == "scales":
        d.line([cx, cy - s, cx, cy + s], fill=INK, width=2)
        d.line([cx - s, cy - s + 3, cx + s, cy - s + 3], fill=INK, width=2)
        d.arc([cx - s - 1, cy - 2, cx - s + 7, cy + 6], 0, 180, fill=INK, width=2)
        d.arc([cx + s - 7, cy - 2, cx + s + 1, cy + 6], 0, 180, fill=INK, width=2)
    elif kind == "gavel":
        d.line([cx - s, cy + s, cx + s, cy - s], fill=INK, width=2)
        d.rectangle([cx - 1, cy - s - 2, cx + s + 2, cy - s + 2], fill=BROWN, outline=INK)
    elif kind == "bolt":
        d.polygon([(cx + 2, cy - s), (cx - 4, cy + 1), (cx, cy + 1), (cx - 2, cy + s),
                   (cx + 4, cy - 1), (cx, cy - 1)], fill=YELLOW, outline=INK)
    elif kind == "globe":
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=INK, width=2)
        d.line([cx, cy - s, cx, cy + s], fill=INK, width=1)
        d.ellipse([cx - 3, cy - s, cx + 3, cy + s], outline=INK, width=1)
    elif kind == "ship":
        d.polygon([(cx - s, cy + 2), (cx + s, cy + 2), (cx + s - 3, cy + s),
                   (cx - s + 3, cy + s)], fill=INK)
        d.line([cx, cy + 2, cx, cy - s], fill=INK, width=2)
        d.polygon([(cx, cy - s), (cx + 6, cy - s + 5), (cx, cy - s + 5)], fill=RED)
    elif kind == "cross":
        d.line([cx, cy - s, cx, cy + s], fill=RED, width=3)
        d.line([cx - s, cy, cx + s, cy], fill=RED, width=3)
    elif kind == "trophy":
        d.arc([cx - s, cy - s, cx + s, cy + 2], 0, 180, fill=INK, width=2)
        d.line([cx, cy + 1, cx, cy + s], fill=INK, width=2)
        d.line([cx - 4, cy + s, cx + 4, cy + s], fill=INK, width=2)
    elif kind == "film":
        d.rectangle([cx - s, cy - 5, cx + s, cy + 5], outline=INK, width=2)
        for fx in (-4, 0, 4):
            d.rectangle([cx + fx - 1, cy - 3, cx + fx + 1, cy + 3], fill=INK)


# ---------- world map (own simplified shapes, equirectangular) ----------
NA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
      (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
      (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9),
      (-79, 9), (-81, 13), (-84, 16), (-87, 21), (-90, 21), (-91, 19),
      (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 25), (-80, 32),
      (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47),
      (-55, 52), (-60, 55), (-65, 60), (-68, 58), (-78, 62), (-85, 66),
      (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71),
      (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-22, 70),
             (-25, 76), (-35, 80), (-50, 80), (-58, 76), (-60, 70)]
SA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
      (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
      (-66, -55), (-68, -50), (-65, -45), (-62, -41), (-58, -35), (-52, -32),
      (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3),
      (-44, -2), (-50, 0), (-53, 4), (-55, 6), (-60, 8), (-65, 10), (-70, 12),
      (-75, 11)]
AFRICA = [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
          (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28),
          (34, 27), (37, 22), (39, 21), (43, 12), (48, 11), (51, 12),
          (46, 5), (41, 0), (40, -5), (40, -10), (38, -15), (36, -20),
          (33, -26), (28, -33), (20, -35), (17, -32), (15, -27), (13, -20),
          (12, -15), (13, -10), (12, -5), (9, -1), (9, 4), (-8, 5),
          (-13, 8), (-17, 12)]
EURASIA = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50),
           (0, 51), (3, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62),
           (10, 64), (18, 69), (25, 71), (30, 70), (35, 68), (40, 66),
           (45, 66), (50, 68), (55, 68), (60, 69), (68, 68), (75, 72),
           (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72),
           (140, 72), (150, 70), (160, 69), (170, 67), (178, 65), (178, 62),
           (170, 60), (162, 56), (158, 52), (152, 58), (142, 55), (140, 50),
           (135, 45), (130, 42), (127, 40), (126, 38), (122, 38), (120, 35),
           (122, 31), (120, 28), (118, 25), (110, 21), (108, 18), (105, 10),
           (104, 9), (100, 8), (98, 10), (97, 15), (94, 17), (92, 21),
           (90, 22), (88, 22), (86, 20), (82, 17), (80, 15), (77, 8),
           (75, 12), (72, 20), (70, 23), (66, 25), (62, 25), (58, 26),
           (56, 27), (54, 26), (52, 25), (50, 29), (48, 30), (44, 29),
           (43, 17), (40, 15), (39, 21), (37, 24), (35, 29), (34, 31),
           (36, 36), (30, 36), (27, 37), (23, 36), (19, 40), (16, 40),
           (12, 44), (8, 44), (3, 42), (0, 40), (-2, 37), (-6, 36), (-9, 37)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51)]
JAPAN = [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
         (142, 44), (140, 43), (138, 39), (135, 35), (132, 33)]
MADAG = [(44, -16), (47, -15), (50, -17), (49, -20), (46, -24), (44, -22),
         (43, -18)]
NZ = [(167, -45), (170, -42), (174, -39), (176, -38), (174, -41), (170, -44)]
ICELAND = [(-18, 65), (-15, 64), (-14, 66), (-18, 66)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -11), (137, -12), (135, -15), (132, -12),
             (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)]
ISLANDS = [(95, 0), (100, -2), (105, -3), (110, -4), (115, -5), (120, -6),
           (125, -8), (130, -3), (135, -4), (140, -6), (121, 14), (80, 7)]


def draw_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1, fill=OCEAN)

    def px(lon, lat):
        return (x0 + (lon + 180) / 360 * (x1 - x0),
                y0 + (85 - lat) / 145 * (y1 - y0))

    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = px(lon, 0)
        d.line([gx, y0, gx, y1], fill=GRID, width=1)
    for lat in (60, 30, 0, -30):
        _, gy = px(0, lat)
        d.line([x0, gy, x1, gy], fill=GRID, width=1)
    # continents
    for poly in (NA, GREENLAND, SA, AFRICA, EURASIA, UK, JAPAN, MADAG, NZ,
                 ICELAND, AUSTRALIA):
        d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_D)
    for lon, lat in ISLANDS:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 3, cy - 2, cx + 3, cy + 2], fill=LAND, outline=LAND_D)
    # ocean labels
    lf = F(9, bold=True)
    for txt, lon, lat in [("ARCTIC", -100, 78), ("PACIFIC", -150, 10),
                          ("PACIFIC", 165, -10), ("ATLANTIC", -30, 5),
                          ("INDIAN", 85, -28), ("SOUTHERN", -60, -52)]:
        cx, cy = px(lon, lat)
        w = d.textlength(txt, font=lf)
        d.text((cx - w / 2, cy - 5), txt, font=lf, fill=(70, 110, 150))
    # pins
    nf = F(8, bold=True)
    for n, name, lat, lon in PINS:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255),
                  width=1)
        t = str(n)
        w = d.textlength(t, font=nf)
        d.text((cx - w / 2, cy - 5), t, font=nf, fill=(255, 255, 255))
    return px


# ---------- page assembly ----------
def build():
    import os
    global SERIF_B
    noto = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
    if os.path.exists(noto):
        SERIF_B = noto
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0

    # masthead: black bar, white serif title, gold subtitle + gold badge
    d.rectangle([0, 0, W, 46], fill=(13, 13, 13))
    title = "THE WORLD IN ONE PAGE"
    tf = F(28, bold=True, serif=True)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 2), title, font=tf, fill=(255, 255, 255))
    sf = F(12, bold=True)
    seg1 = "WEDNESDAY 25 NOVEMBER 2026  \u2022  "
    seg3 = "  \u2022  7 REGIONS  \u2022  ONE PAGE"
    badge = "  45 STORIES  "
    total = (d.textlength(seg1, font=sf) + d.textlength(badge, font=sf)
             + d.textlength(seg3, font=sf))
    sx = (W - total) / 2
    d.text((sx, 31), seg1, font=sf, fill=GOLD)
    bx = sx + d.textlength(seg1, font=sf)
    bw = d.textlength(badge, font=sf)
    d.rounded_rectangle([bx, 30, bx + bw, 43], radius=4, fill=GOLD)
    d.text((bx, 31), badge, font=sf, fill=(13, 13, 13))
    d.text((bx + bw, 31), seg3, font=sf, fill=GOLD)
    d.rectangle([0, 46, W, 49], fill=RED)
    y = 49

    # date-check line
    d.text((12, y + 3), DATE_LINE, font=F(10), fill=GREY)
    y += 14

    # stat strip
    sw = int((W - 24 - 5 * 6) / 6)
    for i, (label, val, sub) in enumerate(STATS):
        x0 = 12 + i * (sw + 6)
        d.rectangle([x0, y, x0 + sw, y + 40], outline=(150, 150, 145), width=1,
                    fill=(255, 255, 255))
        d.text((x0 + 7, y + 2), label, font=F(9, bold=True), fill=GREY)
        d.text((x0 + 7, y + 12), val, font=F(18, bold=True), fill=RED)
        d.text((x0 + 7, y + 30), sub, font=F(8), fill=GREY)
    y += 40

    # region tally
    d.line([12, y + 2, W - 12, y + 2], fill=(180, 180, 175), width=1)
    tf2 = F(11.5, bold=True)
    parts = TALLY.split(" \u2022 ")
    tw = sum(d.textlength(p, font=tf2) for p in parts) + (len(parts) - 1) * 18
    cx = (W - tw) / 2
    d.text((cx, y + 5), "REGION TALLY \u2014 ", font=tf2, fill=GREY)
    cx += d.textlength("REGION TALLY \u2014 ", font=tf2)
    for i, p in enumerate(parts):
        region, num = p.rsplit(" ", 1)
        d.text((cx, y + 5), region + " ", font=tf2, fill=INK)
        cx += d.textlength(region + " ", font=tf2)
        d.text((cx, y + 5), num, font=tf2, fill=RED)
        cx += d.textlength(num, font=tf2)
        if i < len(parts) - 1:
            d.text((cx, y + 5), " \u2022 ", font=tf2, fill=GREY)
            cx += 18
    y += 16

    # ---- leads ----
    lw = int((W - 24 - 2 * 8) / 3)
    lead_top = y
    for i, L in enumerate(LEADS):
        x0 = 12 + i * (lw + 8)
        x1 = x0 + lw
        kf = F(11, bold=True)
        d.text((x0, y + 2), L["kicker"], font=kf, fill=RED)
        if i == 0:  # TOP STORY flare on lead 1
            tag = "TOP STORY"
            tagf = F(9, bold=True)
            twd = d.textlength(tag, font=tagf)
            tx1 = x1
            d.rounded_rectangle([tx1 - twd - 18, y + 1, tx1, y + 15], radius=3,
                                fill=RED)
            star(d, tx1 - twd - 12, y + 8, 4, (255, 255, 255))
            d.text((tx1 - twd - 6, y + 3), tag, font=tagf, fill=(255, 255, 255))
        hf = ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 21)
        hl = wrap(d, L["head"], hf, lw)
        assert len(hl) <= 2, f"lead headline wraps to {len(hl)} lines: {hl}"
        hy = y + 17
        for ln in hl:
            d.text((x0, hy), ln, font=hf, fill=INK)
            hy += 24
        sy0 = hy + 2
        sy1 = sy0 + 97
        # draw the scene on its own layer so nothing can spill over the box
        layer = Image.new("RGB", (int(lw), 97), PAPER)
        ld = ImageDraw.Draw(layer)
        if L["scene"] == "hormuz":
            scene_hormuz(ld, 0, 0, int(lw), 97)
        elif L["scene"] == "tariffs":
            scene_tariffs(ld, 0, 0, int(lw), 97)
        else:
            scene_markets(ld, 0, 0, int(lw), 97)
        img.paste(layer, (int(x0), sy0))
        by = sy1 + 5
        by = para(d, x0, by, lw, L["body"], F(11), INK, 13)
        d.text((x0, by + 2), "Sources: " + L["src"], font=F(9), fill=GREY)
        if i == 0:
            lead_bottom = by + 14
    y = lead_bottom + 7

    # ---- secondaries: 2 rows x 5 ----
    sw2 = int((W - 24 - 4 * 8) / 5)
    for row in range(2):
        for col in range(5):
            s = SECONDARIES[row * 5 + col]
            x0 = 12 + col * (sw2 + 8)
            x1 = x0 + sw2
            layer = Image.new("RGB", (int(sw2), 48), PAPER)
            ld = ImageDraw.Draw(layer)
            sec_scene(ld, 0, 0, int(sw2), 48, s["scene"])
            img.paste(layer, (int(x0), y))
            yy = y + 52
            d.text((x0, yy), s["kicker"], font=F(10, bold=True), fill=RED)
            yy += 12
            hf = ImageFont.truetype(
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 11)
            hl = wrap(d, s["head"], hf, sw2)
            assert len(hl) <= 2, f"secondary headline wraps to {len(hl)}: {hl}"
            for ln in hl:
                d.text((x0, yy), ln, font=hf, fill=INK)
                yy += 14
            yy = para(d, x0, yy + 1, sw2, s["body"], F(9.5), INK, 11.5)
            d.text((x0, yy + 1), s["src"], font=F(8.5), fill=GREY)
        y += 150

    # ---- map + date check ----
    map_y = y
    d.text((12, y + 2), "WHERE IT HAPPENED \u2014 13 STORY SITES, NUMBERED",
           font=F(12, bold=True), fill=NAVY)
    d.text((664, y + 2), "DATE CHECK \u2014 NOT TODAY'S NEWS",
           font=F(12, bold=True), fill=RED)
    y += 17
    draw_map(d, 12, y, 652, y + 132)
    # date check box
    d.rectangle([664, y, W - 12, y + 132], outline=(180, 140, 90), width=1,
                fill=(255, 248, 230))
    yy = y + 6
    for item in DATECHECK:
        d.rectangle([672, yy + 3, 679, yy + 10], fill=RED)
        yy = para(d, 684, yy, W - 12 - 684 - 6, item, F(9.5), INK, 10.5)
        yy += 0.5
    y += 132
    # pin index
    idx1 = "1 Hormuz  \u2022  2 Washington  \u2022  3 Seoul  \u2022  4 Samara  \u2022  5 Gaza  \u2022  6 Cartagena  \u2022  7 Jiuquan"
    idx2 = "8 Canberra  \u2022  9 Dhaka  \u2022  10 Bogor  \u2022  11 Damazin  \u2022  12 Paris  \u2022  13 Pretoria"
    d.text((12, y + 2), idx1, font=F(10, bold=True), fill=INK)
    d.text((12, y + 13), idx2, font=F(10, bold=True), fill=INK)
    y += 24

    # ---- briefs: 4 cols x 8 rows ----
    d.text((12, y + 2), "ALSO ON WEDNESDAY \u2014 THE REST OF THE WORLD IN ONE LINE EACH",
           font=F(12, bold=True), fill=NAVY)
    y += 14
    bw2 = int((W - 24 - 3 * 10) / 4)
    for r in range(8):
        for c in range(4):
            n, city, head, sub, gl = BRIEFS[r * 4 + c]
            x0 = 12 + c * (bw2 + 10)
            glyph(d, x0 + 7, y + 7, gl)
            tx = x0 + 18
            d.text((tx, y), f"{n}. {city} \u2014 {head}", font=F(9, bold=True),
                   fill=INK)
            d.text((tx, y + 10), sub, font=F(8.5), fill=GREY)
        y += 19

    # ---- footer ----
    d.line([12, y + 2, W - 12, y + 2], fill=(180, 180, 175), width=1)
    d.text((12, y + 4), FOOT_SRC, font=F(9), fill=GREY)
    d.text((12, y + 14), FOOT_TAG, font=F(9), fill=GREY)
    y += 20
    print("final y:", y, "(canvas 1024)")
    assert y <= 1024, f"OVERFLOW: final y {y} > 1024"
    img.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    build()
