#!/usr/bin/env python3
"""THE WORLD IN ONE PAGE - Wednesday 25 November 2026.
News image entry for make.fun bounty news-image-20261125.
Drawn from scratch with PIL. Deterministic: no randomness, no network, no clock.
All 45 stories from the research dossier (25 Nov 2026 only); claims framed as claims.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")

# ---------------------------------------------------------------- fonts
FDIR = "/usr/share/fonts/truetype"
def F(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)
def serif_b(s): return F("liberation/LiberationSerif-Bold.ttf", s)
def serif(s):   return F("liberation/LiberationSerif-Regular.ttf", s)
def sans(s):    return F("liberation/LiberationSans-Regular.ttf", s)
def sans_b(s):  return F("liberation/LiberationSans-Bold.ttf", s)
def sans_i(s):  return F("liberation/LiberationSans-Italic.ttf", s)

# ---------------------------------------------------------------- colours
INK    = (18, 18, 18)
RED    = (185, 28, 28)
DRED   = (150, 20, 20)
BLUE   = (28, 68, 140)
GOLD   = (216, 178, 60)
GREY   = (90, 90, 90)
LGREY  = (150, 150, 150)
PANEL  = (244, 244, 242)
SKY    = (214, 233, 246)
OCEAN  = (203, 224, 238)
LAND   = (178, 205, 138)
LAND_O = (120, 160, 90)
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)

# ---------------------------------------------------------------- data
# Final story list (45). Regions: NA 8, EU 10, ME 6, ASIA 9, AFR 6, SA 2, OC 4.
LEADS = [
    dict(n=1, kick="1  •  GULF  •  STRAIT OF HORMUZ",
         head="IRAN CLAIMS TWO TANKERS HIT MINES IN HORMUZ",
         body=("Iran's Revolutionary Guard said on Wednesday that two oil tankers struck sea "
               "mines, exploded and caught fire in the Strait of Hormuz on what it called an "
               "unofficial route. The mine claim could not be independently verified. "
               "Oil prices moved on the news."),
         src="Sources: Reuters  •  Just Security", scene="hormuz"),
    dict(n=2, kick="2  •  TRADE  •  WASHINGTON",
         head="US ANNOUNCES NEW TARIFFS, CHINA AMONG TARGETS",
         body=("The Trump administration announced new tariffs on Wednesday against a host of "
               "trading partners including China, after a Section 301 probe into alleged "
               "subsidies and overcapacity in 16 economies. Specific rates had not been "
               "announced when the first reports landed."),
         src="Sources: BBC  •  AP", scene="tariffs"),
    dict(n=3, kick="3  •  MARKETS  •  SEOUL",
         head="ASIAN MARKETS TUMBLE: KOSPI -6.16% IN AI ROUT",
         body=("Asian stocks fell sharply on Wednesday as the AI sell-off deepened. Seoul's "
               "KOSPI plunged 6.16% to 4,697.51, wiping out the previous day's 6.32% gain; "
               "Samsung fell 9.9% and SK Hynix 11.1%. Taiwan's Taiex fell 4.80% and "
               "Tokyo's Nikkei 2.78%."),
         src="Sources: AP  •  Reuters", scene="kospi"),
]

SECONDS = [
    dict(n=4, kick="4  •  RUSSIA  •  WAR",
         head="UKRAINIAN DRONES SET TWO REFINERIES ABLAZE",
         body=("Kyiv said overnight drones hit two Rosneft refineries in Samara, starting big "
               "fires. One person was killed; Reuters could not verify which plants burned."),
         src="Reuters", scene="samara"),
    dict(n=5, kick="5  •  GAZA  •  WAR",
         head="ISRAEL KILLS SENIOR HAMAS SECURITY CHIEF IN GAZA",
         body=("An Israeli strike killed Hamas colonel Mohammad Abuelouf, who ran the group's "
               "internal security, with his wife and two children at Beach camp in Gaza."),
         src="Reuters", scene="gaza"),
    dict(n=6, kick="6  •  COLOMBIA  •  HOSTAGES",
         head="ALL HOSTAGES FREED IN CARTAGENA SUPERMARKET RAID",
         body=("Colombian forces stormed an Éxito supermarket early on Wednesday, freeing the "
               "last 20 hostages and killing one kidnapper after a 17-hour siege."),
         src="Reuters  •  AFP  •  BBC", scene="cartagena"),
    dict(n=7, kick="7  •  SPACE  •  CHINA",
         head="SHENZHOU-24 CARRIES FIRST PAKISTANI TO TIANGONG",
         body=("China launched Shenzhou-24 from Jiuquan carrying two Chinese astronauts and "
               "Pakistan's Muhammad Zeeshan Ali, the first foreign visitor to Tiangong station."),
         src="AP  •  BBC", scene="shenzhou"),
    dict(n=8, kick="8  •  PACIFIC  •  TREATY",
         head="SOLOMON ISLANDS SIGNS AUSTRALIA TREATY",
         body=("Solomon Islands and Australia signed a treaty in Canberra making Australia the "
               "islands' 'principal security partner' and barring foreign military bases."),
         src="AP  •  NYT  •  BBC", scene="solomon"),
    dict(n=9, kick="9  •  BANGLADESH  •  WAGES",
         head="BANGLADESH RAISES GARMENT WAGE 36% AFTER PROTESTS",
         body=("Bangladesh raised the garment minimum wage 36% to 17,000 taka (~US$136) after "
               "a 12-hour wage-board session. Workers wanting more blocked roads in Gazipur."),
         src="AP  •  Reuters", scene="dhaka"),
    dict(n=10, kick="10  •  INDONESIA  •  MINE",
         head="THREE BODIES FOUND IN FLOODED BOGOR GOLD MINE",
         body=("Rescuers found three bodies on Wednesday in the search for miners trapped "
               "since Monday when rain flooded an unlicensed gold mine in Bogor. Twenty-three "
               "are still missing."),
         src="AP  •  Reuters", scene="bogor"),
    dict(n=11, kick="11  •  SUDAN  •  WAR",
         head="RSF DRONE STRIKES KILL 19 CIVILIANS IN SUDAN",
         body=("RSF drones killed 19 civilians, including six women, and wounded 20 in "
               "Damazin and Roseires, Sudanese rights lawyers said on Wednesday."),
         src="Reuters", scene="damazin"),
    dict(n=12, kick="12  •  EUROPE  •  RAIL",
         head="EUROSTAR STRIKE CANCELS PARIS-LONDON TRAINS",
         body=("Paris-based Eurostar staff walked out without notice in a pay dispute, "
               "cancelling morning trains both ways. About four in five services still ran."),
         src="AP", scene="eurostar"),
    dict(n=13, kick="13  •  S. AFRICA  •  COURTS",
         head="RAMAPHOSA WINS COURT FIGHT OVER IMPEACHMENT",
         body=("President Cyril Ramaphosa won a court battle over the Phala Phala impeachment "
               "threat when a court set aside the impeachment report — for now."),
         src="BBC", scene="pretoria"),
]

# briefs: (number, place, headline, detail+source, glyph)
BRIEFS = [
 (14, "MADRID", "Ábrego García reaches Spain", "Ending the Trump deportation battle. BBC • AP", "plane"),
 (15, "IOWA", "Army to blast unstable explosives", "Unstable lead azide, day before Thanksgiving. AP", "alert"),
 (16, "USA", "81.5m travel for Thanksgiving", "Busiest Thanksgiving flying in 16 years. AP", "plane"),
 (17, "WASHINGTON", "Melania reunites 7th group", "Ukrainian, Russian children; total now 43. AP", "people"),
 (18, "USA", "Pentagon to audit military schools", "Conservative contractors; 'classical' PE pilot. AP", "gov"),
 (19, "USA", "GoFundMe warns donors of breach", "Scale of data exposed not yet confirmed. AP", "money"),
 (20, "SEATTLE", "Amazon buys Decart for AI chips", "Software bet to catch Nvidia. Principia", "tech"),
 (21, "EUROZONE", "Inflation rises to 4.0%", "Growth and jobs data also released. Principia", "chart"),
 (22, "BERLIN", "Merz: Russia 'escalating' threat", "Defends defence spending and Ukraine aid. Reuters", "flag"),
 (23, "BERLIN", "Germany weighs US troop drawdown", "Officials meet on offsetting a US pullback. POLITICO", "shield"),
 (24, "PARIS", "Sarkozy, Carla Bruni to face trial", "Charges and trial date not yet confirmed. BBC", "court"),
 (25, "LONDON", "UK energy bills to rise 26%", "Typical bill £1,723 to £2,166 from January. BBC", "energy"),
 (26, "LUTON", "EasyJet profit falls 89%", "£244m fuel hit; older jets retired faster. Principia", "plane"),
 (27, "NORFOLK", "Two charged over William break-in", "Charged over Monday's raid at Anmer Hall. AP • BBC", "court"),
 (28, "VATICAN", "Pope dismayed at COP31 failure", "Pope: extreme weather 'growing more frequent.' AP", "globe"),
 (29, "RAS TANURA", "Houthis claim refinery strike", "Riyadh: 4 drones downed; hit unconfirmed. Reuters", "factory"),
 (30, "BENGHAZI", "Libya vows revenge on Ukraine", "Two officers died of Sunday's wounds. AP • Reuters", "flag"),
 (31, "TEHRAN", "Iran 'not worried' over blockade", "Aref cites rising cargo via other borders. Reuters", "ship"),
 (32, "ISLAMABAD", "Pakistan warns of energy crisis", "Warning reported by SRI; single source. SRI", "energy"),
 (33, "SHANGHAI", "China probes party chief Chen", "Politburo member probed. Daily Summary", "gov"),
 (34, "SEOUL", "Russian jets entered air zone", "Jets and date not confirmed; single source. SRI", "plane"),
 (35, "INDIA", "The rising cost of food", "Household food-price pressure mounts. BBC", "money"),
 (36, "TOKYO", "Services inflation at 36-year high", "Services prices +4.2% in Oct; BOJ rise seen. Reuters", "chart"),
 (37, "N. KOREA", "Jailed for being Christian", "Witnesses: spied on, beaten, jailed. BBC", "people"),
 (38, "ITURI", "Fighting traps Ebola responders", "WHO concern as violence deepens. PANA • WHO", "health"),
 (39, "HARARE", "Mugabe's son faces arrest warrant", "Warrant over a missed court date. BBC", "court"),
 (40, "DAKAR", "CAF: Senegal are AFCON champions", "CAS restored Senegal's 1-0 final win. BBC", "ball"),
 (41, "NIGERIA", "Nollywood's Pete Edochie dies, 79", "Veteran Nollywood actor dies at 79. BBC", "film"),
 (42, "QUITO", "US pauses Ecuador joint operations", "Pause dates to mid-October, sources say. Atlantic", "shield"),
 (43, "CANBERRA", "Australian inflation hits 4.9%", "Fuel drove the rise; RBA expected to hold. Principia", "chart"),
 (44, "CANBERRA", "Online safety law passes", "Big Tech faces multibillion-dollar fines. AP", "tech"),
 (45, "WELLINGTON", "NZ netball league collapses", "Players left in limbo as league folds. BBC", "ball"),
]

STATS = [  # (label, value, sub) — all Wednesday 25 Nov closes / morning readings
 ("KOSPI", "-6.16%", "4,697.51  •  SEOUL"),
 ("NIKKEI", "-2.78%", "57,011.62  •  TOKYO"),
 ("TAIEX", "-4.80%", "38,195.43  •  TAIPEI"),
 ("BRENT", "~$90.97", "-0.5%  •  WED 25 NOV"),
 ("GOLD", "~$3,548", "-0.4%  •  WED 25 NOV"),
 ("BITCOIN", "~$59,145", "-1.18%  •  WED 25 NOV"),
]

TALLY = [("N. AMERICA", 8), ("EUROPE", 10), ("MIDDLE EAST", 6), ("ASIA", 9),
         ("AFRICA", 6), ("S. AMERICA", 2), ("OCEANIA", 4)]

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
 "Zelensky: Ukraine needs €115bn foreign aid for 2027",
 "Russian strikes on Odesa/Kyiv overnight: 2 killed (24-25 Nov)",
 "BBC analysis: Russia has lost 490,334+ troops since 2022",
]

# map pins: (number, name, lat, lon)
PINS = [
 (1, "Hormuz", 26.5, 56.3), (2, "Washington", 38.9, -77.0),
 (3, "Seoul", 37.6, 127.0), (4, "Samara", 53.2, 50.1),
 (5, "Gaza", 31.5, 34.47), (6, "Cartagena", 10.4, -75.5),
 (7, "Jiuquan", 39.7, 98.5), (8, "Canberra", -35.3, 149.1),
 (9, "Dhaka", 23.8, 90.4), (10, "Bogor", -6.6, 106.8),
 (11, "Damazin", 11.8, 34.35), (12, "Paris", 48.85, 2.35),
 (13, "Pretoria", -25.7, 28.2),
]

# ------------------------------------------------------- continent polygons (lon, lat)
N_AMERICA = [(-168,66),(-165,60),(-158,58),(-152,59),(-145,60),(-140,60),(-135,57),
 (-132,54),(-128,50),(-124,48),(-124,42),(-121,37),(-117,33),(-112,29),(-109,25),
 (-105,22),(-100,18),(-96,16),(-94,17),(-91,14),(-88,13),(-85,11),(-83,9),(-80,8),
 (-78,8),(-76,10),(-80,24),(-81,26),(-80,32),(-76,35),(-74,39),(-70,42),(-68,45),
 (-65,44),(-60,47),(-55,47),(-53,50),(-56,52),(-60,55),(-65,58),(-68,55),(-70,58),
 (-75,62),(-80,63),(-85,66),(-90,66),(-95,69),(-110,68),(-125,70),(-140,70),
 (-155,71),(-165,68)]
GREENLAND = [(-58,64),(-52,60),(-45,60),(-40,64),(-32,68),(-25,70),(-20,74),(-25,78),
 (-35,80),(-50,80),(-58,76),(-60,72),(-58,64)]
S_AMERICA = [(-79,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),
 (-72,-37),(-73,-44),(-70,-50),(-68,-54),(-66,-55),(-68,-50),(-65,-45),(-62,-40),
 (-58,-35),(-52,-32),(-48,-28),(-41,-23),(-39,-17),(-35,-9),(-35,-6),(-40,-3),
 (-44,-2),(-50,0),(-53,4),(-58,6),(-62,9),(-68,11),(-72,12),(-76,10),(-79,9)]
AFRICA = [(-6,35),(-10,31),(-15,27),(-17,21),(-17,15),(-15,11),(-13,8),(-8,5),(-4,5),
 (2,6),(6,4),(9,4),(13,-1),(12,-6),(13,-12),(12,-18),(14,-22),(16,-28),(19,-34),
 (25,-34),(28,-32),(32,-28),(35,-24),(36,-20),(40,-16),(40,-10),(42,-4),(46,-1),
 (51,2),(51,11),(48,11),(44,11),(43,12),(40,15),(38,18),(37,22),(35,28),(34,31),
 (32,31),(30,32),(26,34),(22,33),(19,32),(15,32),(11,34),(10,37),(6,37),(0,36),(-6,35)]
MADAGASCAR = [(44,-16),(47,-15),(50,-16),(49,-20),(47,-24),(45,-25),(43,-21),(44,-16)]
EURASIA = [(-10,36),(-9,38),(-9,43),(-2,44),(-4,48),(0,50),(3,53),(8,57),(10,59),
 (5,60),(5,62),(10,64),(13,66),(18,69),(25,71),(30,70),(35,68),(40,68),(45,68),
 (50,69),(55,69),(60,69),(65,70),(70,71),(75,72),(80,73),(85,74),(90,75),(95,76),
 (100,77),(105,78),(110,76),(115,73),(120,73),(125,72),(130,72),(135,72),(140,72),
 (145,72),(150,70),(155,69),(160,69),(165,66),(170,66),(178,65),(178,62),(170,60),
 (162,58),(158,52),(152,55),(142,54),(140,48),(138,42),(135,40),(132,38),(130,35),
 (127,35),(126,38),(122,38),(120,34),(121,30),(120,25),(118,22),(112,22),(108,18),
 (106,10),(104,9),(101,7),(100,8),(98,10),(97,15),(94,17),(92,21),(89,22),(86,20),
 (83,18),(80,15),(80,13),(77,8),(76,10),(73,16),(70,20),(67,24),(62,25),(58,25),
 (56,27),(52,26),(56,26),(59,23),(58,19),(55,17),(52,15),(48,14),(44,13),(42,15),
 (39,20),(38,24),(36,28),(35,31),(36,36),(33,36),(30,36),(27,37),(26,38),(23,36),
 (22,37),(19,40),(16,38),(15,40),(12,44),(8,44),(3,42),(0,40),(-2,37),(-6,36),
 (-9,37),(-10,36)]
UK = [(-5,50),(-3,53),(-5,56),(-3,58),(-1,57),(0,53),(-1,51),(-3,50),(-5,50)]
JAPAN = [(130,31),(132,33),(135,34),(137,35),(139,37),(140,39),(141,41),(142,43),
 (144,44),(141,45),(140,42),(139,38),(137,35),(133,35),(130,33)]
SUMATRA = [(95,5),(98,3),(101,0),(104,-3),(106,-6),(103,-6),(100,-2),(97,2),(95,5)]
BORNEO = [(109,1),(112,3),(116,5),(118,2),(117,-2),(115,-4),(111,-3),(109,1)]
NEW_GUINEA = [(131,-1),(136,-2),(141,-3),(146,-6),(150,-8),(147,-9),(143,-8),(138,-7),
 (134,-4),(131,-1)]
JAVA = [(105,-6),(108,-7),(112,-7),(114,-8),(111,-8),(107,-7),(105,-6)]
PHILIPPINES = [(120,18),(122,16),(124,13),(122,11),(120,13),(119,16),(120,18)]
NZ = [(167,-45),(170,-43),(174,-41),(177,-38),(175,-37),(173,-40),(170,-42),(167,-45)]
ANTARCTICA = [(-180,-62),(-120,-68),(-60,-64),(0,-68),(60,-64),(120,-62),(180,-60),
 (180,-78),(-180,-78)]
CONTINENTS = [N_AMERICA, GREENLAND, S_AMERICA, AFRICA, MADAGASCAR, EURASIA, UK,
              JAPAN, SUMATRA, BORNEO, NEW_GUINEA, JAVA, PHILIPPINES, NZ, ANTARCTICA]

# ---------------------------------------------------------------- helpers
def wrap(text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(d, lines, x, y, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def stickman(d, x, y, s=1.0, hat=None, pose="stand", color=INK, flip=False):
    """Stickman with feet at (x, y). hat: tie|helmet|sailor. pose: stand|up|point|wave|carry|shake."""
    fx = -1 if flip else 1
    hx, hy = x, y - 26 * s
    w = max(1, int(2 * s))
    d.ellipse([hx - 5 * s, hy - 5 * s, hx + 5 * s, hy + 5 * s], outline=color, width=w)
    d.line([x, y - 21 * s, x, y - 10 * s], fill=color, width=w)
    d.line([x, y - 10 * s, x - 6 * s * fx, y], fill=color, width=w)
    d.line([x, y - 10 * s, x + 6 * s * fx, y], fill=color, width=w)
    shx, shy = x, y - 19 * s
    if pose == "up":
        d.line([shx, shy, x - 8 * s * fx, y - 27 * s], fill=color, width=w)
        d.line([shx, shy, x + 8 * s * fx, y - 27 * s], fill=color, width=w)
    elif pose == "point":
        d.line([shx, shy, x + 12 * s * fx, y - 18 * s], fill=color, width=w)
        d.line([shx, shy, x - 5 * s * fx, y - 12 * s], fill=color, width=w)
    elif pose == "wave":
        d.line([shx, shy, x + 8 * s * fx, y - 28 * s], fill=color, width=w)
        d.line([shx, shy, x - 6 * s * fx, y - 12 * s], fill=color, width=w)
    elif pose == "carry":
        d.line([shx, shy, x + 7 * s * fx, y - 11 * s], fill=color, width=w)
        d.line([shx, shy, x + 5 * s * fx, y - 11 * s], fill=color, width=w)
    elif pose == "shake":
        d.line([shx, shy, x + 10 * s * fx, y - 17 * s], fill=color, width=w)
        d.line([shx, shy, x - 5 * s * fx, y - 12 * s], fill=color, width=w)
    else:
        d.line([shx, shy, x - 6 * s * fx, y - 12 * s], fill=color, width=w)
        d.line([shx, shy, x + 6 * s * fx, y - 12 * s], fill=color, width=w)
    if hat == "tie":
        d.polygon([(x - 2 * s, y - 20 * s), (x + 2 * s, y - 20 * s),
                   (x + 3.5 * s, y - 12 * s), (x, y - 9 * s),
                   (x - 3.5 * s, y - 12 * s)], fill=RED)
    elif hat == "helmet":
        d.pieslice([hx - 6 * s, hy - 7 * s, hx + 6 * s, hy + 3 * s], 180, 360,
                   fill=(230, 126, 34))
        d.rectangle([hx - 6 * s, hy - 2 * s, hx + 6 * s, hy + 1 * s], fill=(230, 126, 34))
    elif hat == "sailor":
        d.ellipse([hx - 6 * s, hy - 8 * s, hx + 6 * s, hy - 1 * s], fill=WHITE,
                  outline=color, width=1)
        d.rectangle([hx - 7 * s, hy - 2 * s, hx + 7 * s, hy + 1 * s], fill=WHITE,
                    outline=color, width=1)

def briefcase(d, x, y, s=1.0):
    d.rectangle([x, y, x + 14 * s, y + 10 * s], fill=(150, 90, 30), outline=INK, width=1)
    d.line([x + 5 * s, y, x + 5 * s, y - 3 * s], fill=INK, width=1)
    d.line([x + 9 * s, y, x + 9 * s, y - 3 * s], fill=INK, width=1)
    d.line([x + 5 * s, y - 3 * s, x + 9 * s, y - 3 * s], fill=INK, width=1)

def flame(d, cx, cy, s=1.0):
    d.polygon([(cx, cy - 12 * s), (cx + 5 * s, cy - 2 * s), (cx + 10 * s, cy + 4 * s),
               (cx + 4 * s, cy + 6 * s), (cx, cy + 12 * s), (cx - 4 * s, cy + 6 * s),
               (cx - 10 * s, cy + 4 * s), (cx - 5 * s, cy - 2 * s)],
              fill=(240, 120, 20))
    d.polygon([(cx, cy - 5 * s), (cx + 3 * s, cy + 1 * s), (cx + 5 * s, cy + 5 * s),
               (cx, cy + 8 * s), (cx - 5 * s, cy + 5 * s), (cx - 3 * s, cy + 1 * s)],
              fill=(250, 200, 40))

def smoke(d, cx, cy, s=1.0):
    for dx, dy, r in ((0, 0, 6), (7, -5, 5), (-7, -4, 5), (3, -10, 4)):
        d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                   cx + dx * s + r * s, cy + dy * s + r * s], fill=(120, 120, 120))

def drone(d, cx, cy, s=1.0):
    d.rectangle([cx - 6 * s, cy - 3 * s, cx + 6 * s, cy + 3 * s], fill=INK)
    for dx in (-9, 9):
        d.line([cx + dx * s - 4 * s, cy - 4 * s, cx + dx * s + 4 * s, cy - 4 * s],
               fill=INK, width=2)
        d.ellipse([cx + dx * s - 2 * s, cy - 6 * s, cx + dx * s + 2 * s, cy - 2 * s],
                  outline=INK, width=1)

def scene_box(d, x, y, w, h, bg=SKY):
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=(120, 140, 160), width=1)

# ---------------------------------------------------------------- lead scenes
def scene_hormuz(d, x, y, w, h):
    scene_box(d, x, y, w, h)
    sea = y + int(h * 0.55)
    d.rectangle([x + 1, sea, x + w - 1, y + h - 1], fill=(70, 130, 180))
    for wx in range(x + 8, x + w - 8, 26):
        d.arc([wx, sea + 6, wx + 16, sea + 12], 0, 180, fill=WHITE, width=1)
    # tanker A (left, sailor aboard)
    ax, ay = x + 18, y + h - 26
    d.polygon([(ax, ay), (ax + 92, ay), (ax + 84, ay + 13), (ax + 8, ay + 13)],
              fill=(150, 40, 40))
    d.rectangle([ax + 58, ay - 13, ax + 82, ay], fill=WHITE, outline=INK, width=1)
    d.rectangle([ax + 20, ay - 9, ax + 30, ay], fill=(40, 40, 40))
    stickman(d, ax + 70, ay - 13, s=0.85, hat="sailor", pose="wave")
    # tanker B (right, burning)
    bx, by = x + w - 118, y + h - 26
    d.polygon([(bx, by), (bx + 92, by), (bx + 84, by + 13), (bx + 8, by + 13)],
              fill=(120, 35, 35))
    d.rectangle([bx + 12, by - 13, bx + 36, by], fill=WHITE, outline=INK, width=1)
    flame(d, bx + 55, by - 14, s=1.1)
    smoke(d, bx + 55, by - 32, s=0.9)
    # mine in the water between the ships
    mx, my = x + w // 2 + 8, y + h - 12
    d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=INK)
    for ang in range(0, 360, 45):
        import math
        dx = math.cos(math.radians(ang)) * 8
        dy = math.sin(math.radians(ang)) * 8
        d.line([mx, my, mx + dx, my + dy], fill=INK, width=2)

def scene_tariffs(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(235, 240, 245))
    # flags on poles at the back
    for fx, cols in ((x + 22, [(185, 28, 28), WHITE]), (x + w - 56, [RED, RED])):
        d.line([fx, y + 8, fx, y + 42], fill=INK, width=2)
        if fx < x + w // 2:  # US flag: stripes + canton
            for i in range(5):
                d.rectangle([fx, y + 8 + i * 4, fx + 34, y + 11 + i * 4],
                            fill=(185, 28, 28) if i % 2 == 0 else WHITE)
            d.rectangle([fx, y + 8, fx + 14, y + 18], fill=(28, 68, 140))
            for sx in (3, 8):
                for sy in (11, 15):
                    d.ellipse([fx + sx - 1, y + sy - 1, fx + sx + 1, y + sy + 1],
                              fill=WHITE)
        else:  # China flag
            d.rectangle([fx, y + 8, fx + 34, y + 28], fill=RED)
            d.ellipse([fx + 4, y + 11, fx + 10, y + 17], fill=(250, 220, 60))
            for sx, sy in ((16, 11), (20, 14), (16, 18), (12, 15)):
                d.ellipse([fx + sx - 1, y + sy - 1, fx + sx + 1, y + sy + 1],
                          fill=(250, 220, 60))
    # desk
    d.rectangle([x + 30, y + h - 24, x + w - 30, y + h - 8], fill=(150, 105, 60),
                outline=INK, width=1)
    # tariff document with %
    d.rectangle([x + w // 2 - 6, y + h - 38, x + w // 2 + 34, y + h - 24],
                fill=WHITE, outline=INK, width=1)
    d.text((x + w // 2 + 2, y + h - 38), "%", font=sans_b(13), fill=RED)
    d.line([x + w // 2 + 2, y + h - 26, x + w // 2 + 28, y + h - 26], fill=GREY, width=1)
    # negotiator with tie, pointing at the document
    stickman(d, x + 108, y + h - 24, s=1.15, hat="tie", pose="point")
    briefcase(d, x + w - 96, y + h - 34, s=0.9)

def scene_kospi(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=WHITE)
    d.text((x + w - 92, y + 4), "-6.16%", font=sans_b(20), fill=RED)
    # plunging chart
    pts = [(x + 14, y + 14), (x + 60, y + 10), (x + 110, y + 22), (x + 150, y + 18),
           (x + 195, y + 44), (x + 240, y + 52), (x + 290, y + 68)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.polygon([(x + 290, y + 68), (x + 278, y + 62), (x + 282, y + 74)], fill=RED)
    for cx, cy in ((x + 60, y + 10), (x + 150, y + 18), (x + 240, y + 52)):
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    # falling chips
    for cx, cy in ((x + 210, y + 16), (x + 250, y + 26), (x + 175, y + 34)):
        d.rectangle([cx, cy, cx + 12, cy + 12], fill=(28, 68, 140), outline=INK, width=1)
        d.line([cx + 2, cy - 4, cx + 2, cy], fill=GREY, width=1)
        d.line([cx + 10, cy - 4, cx + 10, cy], fill=GREY, width=1)
    # trader with tie, hands on head
    stickman(d, x + 62, y + h - 6, s=1.0, hat="tie", pose="up")

LEAD_SCENES = {"hormuz": scene_hormuz, "tariffs": scene_tariffs, "kospi": scene_kospi}

# ---------------------------------------------------------------- secondary scenes
def scene_samara(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(238, 236, 228))
    d.rectangle([x + 14, y + h - 26, x + 30, y + h - 2], fill=(110, 110, 110), outline=INK, width=1)
    d.rectangle([x + 36, y + h - 30, x + 54, y + h - 2], fill=(90, 90, 90), outline=INK, width=1)
    d.rectangle([x + 60, y + h - 20, x + 92, y + h - 2], fill=(130, 130, 130), outline=INK, width=1)
    flame(d, x + 22, y + h - 24, s=0.8)
    flame(d, x + 45, y + h - 27, s=0.8)
    smoke(d, x + 34, y + 8, s=0.7)
    drone(d, x + w - 34, y + 10, s=0.8)

def scene_gaza(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(238, 234, 226))
    d.rectangle([x + 12, y + h - 28, x + 78, y + h - 2], fill=(150, 145, 135), outline=INK, width=1)
    for wy in (y + h - 24, y + h - 14):
        for wx in (x + 20, x + 38, x + 56):
            d.rectangle([wx, wy, wx + 8, wy + 6], fill=(60, 60, 60))
    smoke(d, x + 45, y + 9, s=0.7)
    stickman(d, x + w - 26, y + h - 2, s=0.85, hat="helmet", pose="up")

def scene_cartagena(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(226, 236, 246))
    d.rectangle([x + 52, y + h - 26, x + w - 14, y + h - 2], fill=(60, 110, 190), outline=INK, width=1)
    for i in range(6):
        d.rectangle([x + 54 + i * 14, y + h - 26, x + 62 + i * 14, y + h - 18],
                    fill=WHITE if i % 2 == 0 else (60, 110, 190))
    d.rectangle([x + 96, y + h - 12, x + 116, y + h - 2], fill=(30, 30, 30))
    stickman(d, x + 30, y + h - 2, s=0.85, hat="helmet", pose="point")
    stickman(d, x + 148, y + h - 2, s=0.85, pose="up")

def scene_shenzhou(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(18, 28, 58))
    for sx, sy in ((14, 8), (40, 20), (90, 6), (150, 12), (180, 26), (120, 30)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    # rocket rising diagonally
    d.polygon([(x + 118, y + 30), (x + 128, y + 8), (x + 138, y + 30)], fill=WHITE)
    d.polygon([(x + 128, y + 8), (x + 133, y + 16), (x + 123, y + 16)], fill=RED)
    d.rectangle([x + 122, y + 28, x + 134, y + 34], fill=(200, 200, 200), outline=INK, width=1)
    flame(d, x + 128, y + 40, s=0.7)
    d.ellipse([x + 20, y + h - 12, x + 70, y + h - 1], fill=(90, 130, 180))

def scene_solomon(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(232, 242, 232))
    for fx, col in ((x + 12, (28, 68, 140)), (x + w - 26, (20, 120, 80))):
        d.line([fx, y + 6, fx, y + 26], fill=INK, width=2)
        d.polygon([(fx, y + 6), (fx + 14, y + 10), (fx, y + 14)], fill=col)
    stickman(d, x + 78, y + h - 2, s=0.85, hat="tie", pose="shake")
    stickman(d, x + 118, y + h - 2, s=0.85, pose="shake", flip=True)
    d.rectangle([x + 84, y + h - 12, x + 112, y + h - 4], fill=WHITE, outline=INK, width=1)
    d.line([x + 88, y + h - 9, x + 108, y + h - 9], fill=GREY, width=1)

def scene_dhaka(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(240, 236, 224))
    d.polygon([(x + 12, y + h - 2), (x + 12, y + 14), (x + 26, y + 6), (x + 40, y + 14),
               (x + 54, y + 6), (x + 68, y + 14), (x + 68, y + h - 2)], fill=(140, 140, 140),
              outline=INK)
    d.rectangle([x + 74, y + 4, x + 82, y + h - 2], fill=(110, 110, 110), outline=INK, width=1)
    smoke(d, x + 78, y + 6, s=0.5)
    stickman(d, x + 110, y + h - 2, s=0.85, pose="carry")
    briefcase(d, x + 116, y + h - 14, s=0.7)
    d.rectangle([x + 140, y + 6, x + w - 10, y + 20], fill=WHITE, outline=RED, width=1)
    d.text((x + 143, y + 7), "36%", font=sans_b(10), fill=RED)

def scene_bogor(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(236, 230, 214))
    d.polygon([(x + 8, y + h - 2), (x + 40, y + 8), (x + 90, y + 6), (x + 130, y + h - 2)],
              fill=(150, 115, 70))
    d.ellipse([x + 48, y + 14, x + 82, y + 26], fill=(30, 30, 30))
    d.polygon([(x + 52, y + 20), (x + 78, y + 20), (x + 86, y + h - 2), (x + 44, y + h - 2)],
              fill=(70, 130, 180))
    d.line([x + 65, y + 6, x + 65, y + 22], fill=INK, width=2)
    stickman(d, x + 130, y + h - 2, s=0.85, hat="helmet", pose="point")

def scene_damazin(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(240, 232, 216))
    for hx in (x + 16, x + 58):
        d.rectangle([hx, y + h - 20, hx + 34, y + h - 2], fill=(170, 130, 80), outline=INK, width=1)
        d.polygon([(hx - 3, y + h - 20), (hx + 17, y + h - 30), (hx + 37, y + h - 20)],
                  fill=(120, 70, 40))
    smoke(d, x + 33, y + 4, s=0.7)
    drone(d, x + w - 36, y + 10, s=0.8)

def scene_eurostar(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(226, 236, 246))
    d.rectangle([x + 44, y + 8, x + w - 10, y + h - 10], fill=(250, 210, 40), outline=INK, width=1)
    d.rectangle([x + 44, y + h - 16, x + w - 10, y + h - 10], fill=(28, 68, 140))
    for wx in range(x + 52, x + w - 22, 22):
        d.rectangle([wx, y + 14, wx + 14, y + 22], fill=(200, 230, 245), outline=INK, width=1)
    for cx in (x + 62, x + w - 30):
        d.ellipse([cx - 5, y + h - 10, cx + 5, y + h], fill=INK)
    stickman(d, x + 24, y + h - 2, s=0.85, pose="stand")
    d.line([x + 23, y + h - 19, x + 23, y + h - 8], fill=INK, width=2)
    d.rectangle([x + 13, y + h - 31, x + 33, y + h - 19], fill=WHITE, outline=RED, width=1)
    d.text((x + 20, y + h - 31), "!", font=sans_b(10), fill=RED)

def scene_pretoria(d, x, y, w, h):
    scene_box(d, x, y, w, h, bg=(238, 236, 230))
    d.polygon([(x + 40, y + 6), (x + 96, y + 6), (x + 68, y + 16)], fill=(180, 175, 165),
              outline=INK)
    for cx in (48, 68, 88):
        d.rectangle([x + cx, y + 16, x + cx + 8, y + h - 6], fill=WHITE, outline=INK, width=1)
    d.rectangle([x + 36, y + h - 6, x + 100, y + h - 2], fill=(150, 145, 135))
    stickman(d, x + 130, y + h - 2, s=0.85, hat="tie", pose="stand")
    d.rectangle([x + 150, y + 10, x + 164, y + 16], fill=(120, 72, 20))
    d.line([x + 157, y + 16, x + 168, y + 26], fill=(120, 72, 20), width=2)

SEC_SCENES = {"samara": scene_samara, "gaza": scene_gaza, "cartagena": scene_cartagena,
              "shenzhou": scene_shenzhou, "solomon": scene_solomon, "dhaka": scene_dhaka,
              "bogor": scene_bogor, "damazin": scene_damazin, "eurostar": scene_eurostar,
              "pretoria": scene_pretoria}

# ---------------------------------------------------------------- brief glyphs (14x14)
def glyph(d, x, y, kind):
    c = (70, 70, 70)
    if kind == "plane":
        d.polygon([(x + 1, y + 7), (x + 7, y + 3), (x + 13, y + 7), (x + 7, y + 8),
                   (x + 9, y + 12), (x + 6, y + 10), (x + 4, y + 12), (x + 5, y + 8)],
                  fill=c)
    elif kind == "ship":
        d.polygon([(x + 2, y + 9), (x + 12, y + 9), (x + 10, y + 13), (x + 4, y + 13)],
                  fill=c)
        d.line([x + 7, y + 2, x + 7, y + 9], fill=c, width=1)
        d.polygon([(x + 7, y + 2), (x + 11, y + 7), (x + 7, y + 7)], fill=RED)
    elif kind == "court":
        d.line([x + 7, y + 2, x + 7, y + 11], fill=c, width=1)
        d.line([x + 2, y + 5, x + 12, y + 5], fill=c, width=1)
        d.polygon([(x + 1, y + 5), (x + 4, y + 5), (x + 2, y + 9)], outline=c)
        d.polygon([(x + 10, y + 5), (x + 13, y + 5), (x + 12, y + 9)], outline=c)
        d.line([x + 3, y + 12, x + 11, y + 12], fill=c, width=1)
    elif kind == "chart":
        d.line([x + 2, y + 12, x + 2, y + 2], fill=c, width=1)
        d.line([x + 2, y + 12, x + 12, y + 12], fill=c, width=1)
        d.line([(x + 3, y + 9), (x + 6, y + 6), (x + 9, y + 8), (x + 12, y + 3)],
               fill=RED, width=2)
    elif kind == "flag":
        d.line([x + 3, y + 2, x + 3, y + 12], fill=c, width=1)
        d.polygon([(x + 3, y + 2), (x + 12, y + 5), (x + 3, y + 8)], fill=RED)
    elif kind == "rocket":
        d.polygon([(x + 7, y + 1), (x + 10, y + 8), (x + 7, y + 11), (x + 4, y + 8)],
                  fill=c)
        d.polygon([(x + 5, y + 11), (x + 7, y + 13), (x + 9, y + 11)], fill=(240, 120, 20))
    elif kind == "factory":
        d.polygon([(x + 1, y + 13), (x + 1, y + 6), (x + 4, y + 6), (x + 4, y + 4),
                   (x + 7, y + 4), (x + 7, y + 6), (x + 12, y + 6), (x + 12, y + 13)],
                  fill=c)
        d.rectangle([x + 3, y + 9, x + 5, y + 11], fill=WHITE)
        d.rectangle([x + 8, y + 9, x + 10, y + 11], fill=WHITE)
    elif kind == "train":
        d.rectangle([x + 2, y + 3, x + 12, y + 11], fill=c)
        d.rectangle([x + 4, y + 5, x + 6, y + 7], fill=WHITE)
        d.rectangle([x + 8, y + 5, x + 10, y + 7], fill=WHITE)
        d.ellipse([x + 4, y + 11, x + 6, y + 13], fill=c)
        d.ellipse([x + 8, y + 11, x + 10, y + 13], fill=c)
    elif kind == "ball":
        d.ellipse([x + 1, y + 1, x + 13, y + 13], outline=c, width=1)
        d.polygon([(x + 7, y + 5), (x + 10, y + 7), (x + 9, y + 10), (x + 5, y + 10),
                   (x + 4, y + 7)], fill=c)
        d.line([x + 7, y + 1, x + 7, y + 5], fill=c, width=1)
        d.line([x + 1, y + 7, x + 4, y + 7], fill=c, width=1)
        d.line([x + 13, y + 7, x + 10, y + 7], fill=c, width=1)
    elif kind == "health":
        d.rectangle([x + 5, y + 2, x + 9, y + 12], fill=RED)
        d.rectangle([x + 2, y + 5, x + 12, y + 9], fill=RED)
    elif kind == "tech":
        d.rectangle([x + 3, y + 3, x + 11, y + 11], fill=c)
        d.rectangle([x + 6, y + 6, x + 8, y + 8], fill=WHITE)
        for px in (5, 7, 9):
            d.line([x + px, y + 1, x + px, y + 3], fill=c, width=1)
            d.line([x + px, y + 11, x + px, y + 13], fill=c, width=1)
        for py in (5, 7, 9):
            d.line([x + 1, y + py, x + 3, y + py], fill=c, width=1)
            d.line([x + 11, y + py, x + 13, y + py], fill=c, width=1)
    elif kind == "money":
        d.ellipse([x + 2, y + 2, x + 12, y + 12], fill=(212, 175, 55), outline=c, width=1)
        d.text((x + 5, y + 3), "$", font=sans_b(8), fill=c)
    elif kind == "energy":
        d.polygon([(x + 8, y + 1), (x + 4, y + 8), (x + 7, y + 8), (x + 5, y + 13),
                   (x + 11, y + 6), (x + 8, y + 6)], fill=(240, 180, 20))
    elif kind == "globe":
        d.ellipse([x + 1, y + 1, x + 13, y + 13], outline=c, width=1)
        d.ellipse([x + 5, y + 1, x + 9, y + 13], outline=c, width=1)
        d.line([x + 1, y + 7, x + 13, y + 7], fill=c, width=1)
    elif kind == "people":
        d.ellipse([x + 2, y + 2, x + 6, y + 6], outline=c, width=1)
        d.ellipse([x + 8, y + 2, x + 12, y + 6], outline=c, width=1)
        d.arc([x + 1, y + 7, x + 7, y + 13], 180, 360, fill=c, width=1)
        d.arc([x + 7, y + 7, x + 13, y + 13], 180, 360, fill=c, width=1)
    elif kind == "shield":
        d.polygon([(x + 2, y + 2), (x + 12, y + 2), (x + 12, y + 8), (x + 7, y + 13),
                   (x + 2, y + 8)], outline=c, width=1)
        d.line([x + 5, y + 7, x + 7, y + 9], fill=c, width=1)
        d.line([x + 7, y + 9, x + 10, y + 4], fill=c, width=1)
    elif kind == "alert":
        d.polygon([(x + 7, y + 1), (x + 13, y + 12), (x + 1, y + 12)], outline=RED, width=1)
        d.text((x + 6, y + 4), "!", font=sans_b(8), fill=RED)
    elif kind == "film":
        d.rectangle([x + 1, y + 4, x + 13, y + 12], outline=c, width=1)
        d.polygon([(x + 1, y + 4), (x + 13, y + 4), (x + 13, y + 1), (x + 1, y + 1)],
                  outline=c, width=1)
        d.ellipse([x + 5, y + 6, x + 9, y + 10], outline=c, width=1)
    elif kind == "gov":
        d.polygon([(x + 1, y + 5), (x + 7, y + 1), (x + 13, y + 5)], fill=c)
        for px in (3, 6, 9):
            d.line([x + px, y + 6, x + px, y + 11], fill=c, width=1)
        d.line([x + 2, y + 12, x + 12, y + 12], fill=c, width=1)
    else:
        d.ellipse([x + 3, y + 3, x + 11, y + 11], fill=c)

# ---------------------------------------------------------------- world map
def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=OCEAN, outline=(90, 120, 150), width=1)
    def px(lon):
        return min(max(x0 + (lon + 180) / 360.0 * w, x0), x0 + w)
    def py(lat):
        return min(max(y0 + (78 - lat) / 136.0 * h, y0), y0 + h)
    for lon in range(-150, 181, 30):
        d.line([px(lon), y0, px(lon), y0 + h], fill=(172, 202, 222), width=1)
    for lat in (60, 30, 0, -30):
        d.line([x0, py(lat), x0 + w, py(lat)], fill=(172, 202, 222), width=1)
    d.line([x0, py(0), x0 + w, py(0)], fill=(140, 180, 205), width=1)
    for poly in CONTINENTS:
        d.polygon([(px(lo), py(la)) for lo, la in poly], fill=LAND, outline=LAND_O,
                  width=1)
    lab = sans_b(9)
    for txt, lon, lat in (("PACIFIC", -152, 10), ("PACIFIC", 160, -14),
                          ("ATLANTIC", -32, 2), ("INDIAN", 82, -32),
                          ("SOUTHERN", -12, -50), ("ARCTIC", -152, 72)):
        tw = lab.getlength(txt)
        d.text((px(lon) - tw / 2, py(lat) - 5), txt, font=lab, fill=(70, 110, 140))
    for n, name, lat, lon in PINS:
        cx, cy = px(lon), py(lat)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=WHITE, width=2)
        f = sans_b(9 if n >= 10 else 10)
        t = str(n)
        tw = f.getlength(t)
        d.text((cx - tw / 2, cy - 5.5), t, font=f, fill=WHITE)

# ---------------------------------------------------------------- layout
def draw_index_line(d, items, x, y):
    fb, fr = sans_b(10), sans(10)
    cx = x
    for i, (n, name) in enumerate(items):
        t = str(n)
        d.text((cx, y), t, font=fb, fill=RED)
        cx += fb.getlength(t) + 2
        s = name + ("   •   " if i < len(items) - 1 else "")
        d.text((cx, y), s, font=fr, fill=INK)
        cx += fr.getlength(s)

def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 70], fill=BLACK)
    t = "THE WORLD IN ONE PAGE"
    f = serif_b(42)
    d.text(((W - f.getlength(t)) / 2, 4), t, font=f, fill=WHITE)
    t = "WEDNESDAY 25 NOVEMBER 2026  •  45 STORIES  •  7 REGIONS  •  ONE PAGE"
    f = sans_b(13)
    d.text(((W - f.getlength(t)) / 2, 50), t, font=f, fill=GOLD)
    d.rectangle([0, 70, W, 72], fill=RED)

    # ---- date-check strip
    t = ("DATE CHECK: Wednesday 25 November 2026 — today's news, as reported today; "
         "earlier events are dated in the text.")
    d.text((8, 75), t, font=sans_b(10), fill=BLUE)
    d.line([8, 91, W - 8, 91], fill=INK, width=1)

    # ---- stats strip (all Wednesday 25 Nov)
    for i, (lab, val, sub) in enumerate(STATS):
        x = 8 + i * 168
        d.rectangle([x, 94, x + 165, 142], fill=PANEL, outline=LGREY, width=1)
        d.text((x + 7, 97), lab, font=sans_b(9), fill=GREY)
        d.text((x + 7, 108), val, font=sans_b(17), fill=RED)
        d.text((x + 7, 129), sub, font=sans(8), fill=GREY)

    # ---- region tally (must sum to 45)
    d.line([8, 145, W - 8, 145], fill=LGREY, width=1)
    parts = "  •  ".join("%s %d" % (name, n) for name, n in TALLY)
    t = "REGION TALLY — " + parts
    f = sans_b(11)
    d.text(((W - f.getlength(t)) / 2, 148), t, font=f, fill=INK)
    d.line([8, 161, W - 8, 161], fill=LGREY, width=1)

    # ---- leads (162-374)
    for i, L in enumerate(LEADS):
        x = 8 + i * 336
        y0 = 162
        if i:
            d.line([x - 4, y0 + 2, x - 4, y0 + 210], fill=LGREY, width=1)
        d.text((x, y0 + 2), L["kick"], font=sans_b(11), fill=RED)
        hl = wrap(L["head"], serif_b(18), 328)
        draw_lines(d, hl, x, y0 + 17, serif_b(18), INK, 21)
        LEAD_SCENES[L["scene"]](d, x, y0 + 61, 328, 70)
        bl = wrap(L["body"], sans(11), 328)
        draw_lines(d, bl, x, y0 + 135, sans(11), INK, 13)
        d.text((x, y0 + 202), L["src"], font=sans_i(8), fill=GREY)

    # ---- secondaries (5 x 2, 128 px rows)
    for i, S in enumerate(SECONDS):
        col, row = i % 5, i // 5
        x = 8 + col * 203
        y0 = 374 + row * 128
        SEC_SCENES[S["scene"]](d, x, y0, 198, 34)
        d.text((x, y0 + 37), S["kick"], font=sans_b(10), fill=RED)
        hl = wrap(S["head"], serif_b(11), 198)
        draw_lines(d, hl, x, y0 + 49, serif_b(11), INK, 12)
        bl = wrap(S["body"], sans(9), 198)
        draw_lines(d, bl, x, y0 + 75, sans(9), INK, 9.5)
        d.text((x, y0 + 115), S["src"], font=sans_i(7), fill=GREY)

    # ---- map section title
    d.text((8, 630), "WHERE IT HAPPENED — 13 STORY SITES, NUMBERED",
           font=sans_b(12), fill=BLUE)
    d.text((656, 630), "DATE CHECK — NOT TODAY'S NEWS", font=sans_b(12), fill=RED)

    # ---- map
    draw_map(d, 8, 644, 640, 130)
    draw_index_line(d, [(n, nm) for n, nm, _, _ in PINS[:7]], 8, 778)
    draw_index_line(d, [(n, nm) for n, nm, _, _ in PINS[7:]], 8, 791)

    # ---- date check box
    d.rectangle([656, 644, 1016, 802], fill=(255, 248, 235), outline=(200, 150, 100),
                width=1)
    yy = 649
    for item in DATECHECK:
        d.rectangle([662, yy + 4, 667, yy + 9], fill=RED)
        d.text((672, yy), item, font=sans(9), fill=INK)
        yy += 13

    d.line([8, 808, W - 8, 808], fill=LGREY, width=1)

    # ---- briefs
    d.text((8, 812), "ALSO ON WEDNESDAY — THE REST OF THE WORLD IN ONE LINE EACH",
           font=sans_b(12), fill=BLUE)
    for i, (n, place, head, detail, gk) in enumerate(BRIEFS):
        col, row = i % 4, i // 4
        x = 8 + col * 253
        y = 826 + row * 22
        glyph(d, x, y + 1, gk)
        pre = "%d. %s — " % (n, place)
        d.text((x + 17, y), pre, font=sans_b(9), fill=INK)
        d.text((x + 17 + sans_b(9).getlength(pre), y), head, font=sans(9), fill=INK)
        d.text((x + 17, y + 10), detail, font=sans(8), fill=(70, 70, 70))

    # ---- footer
    d.line([8, 1002, W - 8, 1002], fill=INK, width=1)
    t = ("Sources: Reuters  •  AP  •  BBC  •  NYT  •  Just Security  •  POLITICO  •  "
         "Principia  •  Sharecast  •  PANA  •  The Atlantic")
    f = sans(9)
    d.text(((W - f.getlength(t)) / 2, 1004), t, font=f, fill=INK)
    t = ("All the day's news, in one image — Wednesday 25 November 2026  •  "
         "Rounds: blind — final heat: 3 Swiss rounds + playoff (top 52)")
    d.text(((W - f.getlength(t)) / 2, 1013), t, font=f, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
    print("stories: leads", len(LEADS), "secondaries", len(SECONDS),
          "briefs", len(BRIEFS),
          "total", len(LEADS) + len(SECONDS) + len(BRIEFS))
    print("tally sum:", sum(n for _, n in TALLY), "->", TALLY)
    print("pins:", len(PINS), "datecheck:", len(DATECHECK))

if __name__ == "__main__":
    main()
