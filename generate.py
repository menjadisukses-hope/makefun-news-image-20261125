#!/usr/bin/env python3
"""
News Image — Wednesday 25 November 2026.
Flat newspaper-infographic front page in the style Ale approved on 2026-11-26:
giant serif date masthead, coloured region tally bar, THE DAY IN UTC strip,
IN NUMBERS strip, wide flat-vector lead banners with overlay labels and
numbered circle badges, status tags, secondary cards with flat illustration
headers, briefs with source-strength badges, region-coloured map pins and a
DATE CHECK strip. All illustrations are original flat shapes drawn here.
No stick figures anywhere. Deterministic: no randomness, no clock.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16                      # page margin
CW = W - 2 * M              # content width = 992

BG      = (250, 246, 238)
INK     = (22, 22, 22)
GRAY    = (92, 92, 92)
RULE    = (40, 40, 40)
RED     = (198, 16, 44)
DARKRED = (160, 10, 34)
WHITE   = (255, 255, 255)
CREAM2  = (243, 236, 222)

# region colours (tally bar, chips, map pins, legend)
REG = {
    "NA": (125, 60, 152),    # N. America  purple
    "EU": (43, 94, 167),     # Europe      blue
    "ME": (181, 101, 29),    # Middle East ochre
    "AS": (198, 16, 44),     # Asia        red
    "AF": (46, 139, 87),     # Africa      green
    "SA": (169, 122, 196),   # S. America  light purple
    "OC": (23, 145, 135),    # Oceania     teal
}
REGNAME = {"NA": "N. AMERICA", "EU": "EUROPE", "ME": "MIDDLE EAST",
           "AS": "ASIA", "AF": "AFRICA", "SA": "S. AMERICA", "OC": "OCEANIA"}

TAGCOL = {"CONFIRMED": (30, 132, 73), "OFFICIAL": (202, 111, 30),
          "REPORTED": (36, 113, 163), "CLAIM": (198, 16, 44)}
BADGE = {"C": (46, 139, 87), "O": (202, 111, 30),
         "R": (96, 106, 116), "CL": (198, 16, 44)}

FD = "/usr/share/fonts/truetype/liberation/"
def f(name, size):
    return ImageFont.truetype(FD + name, size)
SERIF   = "LiberationSerif-Bold.ttf"
SERIF_I = "LiberationSerif-Italic.ttf"
SERIF_R = "LiberationSerif-Regular.ttf"
SANS    = "LiberationSans-Regular.ttf"
SANS_B  = "LiberationSans-Bold.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def tw(text, font):
    return d.textlength(text, font=font)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def rect(x, y, w, h, fill=None, outline=None, width=1):
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=width)

def chip_num(x, y, n, colour, size=15, font_sz=9):
    """Square number chip, model style."""
    rect(x, y, size, size, fill=colour)
    d.text((x + size / 2, y + size / 2), str(n), font=f(SANS_B, font_sz),
           fill=WHITE, anchor="mm")

def circle_badge(x, y, n, r=13):
    """Red numbered circle badge overlapping a lead banner corner."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=WHITE, width=2)
    d.text((x, y), str(n), font=f(SANS_B, 13), fill=WHITE, anchor="mm")

def status_tag(x_right, y, label):
    font = f(SANS_B, 9)
    w = tw(label, font) + 10
    col = TAGCOL[label]
    d.rounded_rectangle([x_right - w, y, x_right, y + 13], radius=2,
                        outline=col, width=1)
    d.text((x_right - w / 2, y + 7), label, font=font, fill=col, anchor="mm")
    return w

def source_badge(x, y, code):
    r = 7
    d.ellipse([x - r, y - r, x + r, y + r], fill=BADGE[code])
    d.text((x, y), code, font=f(SANS_B, 8 if len(code) == 1 else 7),
           fill=WHITE, anchor="mm")

def overlay_label(x, y, s, bg, fg=WHITE, font_sz=12, pad=6):
    font = f(SANS_B, font_sz)
    w = tw(s, font) + 2 * pad
    rect(x, y, w, font_sz + 8, fill=bg)
    d.text((x + pad, y + (font_sz + 8) / 2), s, font=font, fill=fg, anchor="lm")
    return w

# ---------------------------------------------------------------- masthead
y = 9
text(M, y, "ONE DAY OF WORLD NEWS", f(SANS_B, 11), fill=INK)
r = "45 STORIES · 7 REGIONS · EVERY ONE FROM WEDNESDAY 25 NOVEMBER 2026"
text(W - M, y, r, f(SANS_B, 11), fill=INK, anchor="ra")
d.line([M, y + 17, W - M, y + 17], fill=RULE, width=1)

# giant serif date
title = "Wednesday 25 November 2026"
tf = f(SERIF, 55)
while tw(title, tf) > CW - 8:
    tf = f(SERIF, tf.size - 1)
text(W / 2, 30, title, tf, fill=INK, anchor="ma")

iy = 92
itext = ("Iran claims two tankers hit mines in Hormuz · US announces new "
         "tariffs, China among targets · Asian markets tumble, Kospi −6.16%")
text(W / 2, iy, itext, f(SERIF_I, 15), fill=(60, 55, 50), anchor="ma")

# ---------------------------------------------------------------- tally bar
ty = 116
tally = [("NA", 8), ("EU", 10), ("ME", 6), ("AS", 9), ("AF", 6),
         ("SA", 2), ("OC", 4)]
assert sum(c for _, c in tally) == 45
bar_w = CW - 92
mins = {"SA": 86, "OC": 88}
fixed = sum(mins.values())
rest = bar_w - fixed
tot_rest = sum(c for k, c in tally if k not in mins)
x = M
tf2 = f(SANS_B, 11)
for k, c in tally:
    wseg = mins[k] if k in mins else rest * c / tot_rest
    rect(x, ty, wseg - 2, 21, fill=REG[k])
    label = f"{REGNAME[k]} {c}"
    d.text((x + wseg / 2 - 1, ty + 10.5), label, font=tf2, fill=WHITE,
           anchor="mm")
    x += wseg
text(W - M, ty + 2, "= 45 stories", f(SANS_B, 13), fill=INK, anchor="ra")

# ---------------------------------------------------------------- UTC strip
uy = 146
rect(M, uy, 62, 34, fill=INK)
d.text((M + 31, uy + 8), "THE DAY", font=f(SANS_B, 10), fill=WHITE, anchor="ma")
d.text((M + 31, uy + 20), "IN UTC", font=f(SANS_B, 10), fill=WHITE, anchor="ma")
utc = [("01:26", "Zimbabwe: warrant for Mugabe's son"),
       ("02:12", "Samara refineries ablaze"),
       ("03:06", "Ramaphosa wins court fight"),
       ("06:34", "Ituri: Ebola teams trapped"),
       ("06:35", "Shenzhou-24 crew reach Tiangong"),
       ("14:19", "US announces new tariffs")]
ux = M + 74
uw = (CW - 74) / 6
for i, (t, cap) in enumerate(utc):
    cx = ux + i * uw
    if i:
        d.line([cx - 6, uy + 2, cx - 6, uy + 32], fill=(200, 192, 175), width=1)
    text(cx, uy, t, f(SANS_B, 15), fill=INK)
    for j, ln in enumerate(wrap(cap, f(SANS, 9), uw - 12)):
        text(cx, uy + 19 + j * 10, ln, f(SANS, 9), fill=GRAY)

# ---------------------------------------------------------------- IN NUMBERS
ny = 188
rect(M, ny, 62, 34, fill=INK)
d.text((M + 31, ny + 8), "IN", font=f(SANS_B, 10), fill=WHITE, anchor="ma")
d.text((M + 31, ny + 20), "NUMBERS", font=f(SANS_B, 10), fill=WHITE, anchor="ma")
nums = [("−6.16%", "Kospi close, Seoul"),
        ("−2.78%", "Nikkei 225, Tokyo"),
        ("−4.80%", "Taiex close, Taipei"),
        ("~$90.97", "Brent crude, a barrel"),
        ("~$3,548", "gold, an ounce"),
        ("~$59,145", "Bitcoin, Wednesday")]
nx = M + 74
nw = (CW - 74) / 6
for i, (v, cap) in enumerate(nums):
    cx = nx + i * nw
    if i:
        d.line([cx - 6, ny + 2, cx - 6, ny + 32], fill=(200, 192, 175), width=1)
    text(cx, ny, v, f(SERIF, 20), fill=INK)
    for j, ln in enumerate(wrap(cap, f(SANS, 9), nw - 12)):
        text(cx, ny + 24 + j * 10, ln, f(SANS, 9), fill=GRAY)

# ---------------------------------------------------------------- lead scenes
def scene_canvas(w, h, bg):
    s = Image.new("RGB", (w, h), bg)
    return s, ImageDraw.Draw(s)

def tanker(sd, x, y, w, hull=(38, 48, 64), scale=1.0):
    """Flat oil tanker silhouette: hull, red waterline, deck tanks, bridge."""
    h = int(26 * scale)
    sd.polygon([(x, y), (x + w, y), (x + w - int(14 * scale), y + h),
                (x + int(8 * scale), y + h)], fill=hull)
    sd.rectangle([x + int(2 * scale), y + h - int(6 * scale),
                  x + w - int(10 * scale), y + h], fill=(178, 40, 44))
    deck = y - int(7 * scale)
    for i in range(3):  # deck tank cylinders
        tx = x + int((14 + i * (w / 3.4)) * scale)
        sd.rounded_rectangle([tx, deck, tx + int(w / 4.4), y],
                             radius=int(3 * scale), fill=(96, 108, 124))
    bx = x + w - int(30 * scale)  # bridge block at stern
    sd.rectangle([bx, y - int(22 * scale), bx + int(20 * scale), y],
                 fill=(226, 228, 230))
    sd.rectangle([bx + int(3 * scale), y - int(19 * scale),
                  bx + int(17 * scale), y - int(15 * scale)], fill=(70, 90, 115))
    sd.line([x + int(10 * scale), y, x + int(10 * scale), y - int(16 * scale)],
            fill=hull, width=2)

def starburst(sd, cx, cy, r1, r2, fill):
    import math
    pts = []
    for i in range(16):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    sd.polygon(pts, fill=fill)

def sea_mine(sd, cx, cy, r=7):
    import math
    for i in range(8):
        a = math.pi * i / 4
        sd.line([cx, cy, cx + (r + 4) * math.cos(a), cy + (r + 4) * math.sin(a)],
                fill=(30, 34, 40), width=2)
    sd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 34, 40))
    sd.ellipse([cx - 2, cy - 3, cx + 1, cy], fill=(120, 128, 138))

def lead_hormuz(w, h):
    s, sd = scene_canvas(w, h, (206, 226, 238))
    sd.rectangle([0, int(h * 0.58), w, h], fill=(56, 106, 148))       # sea
    sd.ellipse([w - 58, 8, w - 26, 40], fill=(246, 214, 110))          # sun
    starburst(sd, 96, 52, 34, 15, (240, 128, 28))                      # blast
    starburst(sd, 96, 52, 20, 9, (250, 196, 60))
    for (gx, gy, gr) in [(70, 18, 10), (88, 10, 13), (108, 16, 9)]:    # smoke
        sd.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(150, 152, 156))
    tanker(sd, 26, 66, 168, scale=1.0)
    tanker(sd, 218, 74, 96, scale=0.62)
    sea_mine(sd, 196, 88, 7)
    sea_mine(sd, 52, 96, 6)
    for wx in (18, 120, 250, 292):                                     # wave caps
        sd.arc([wx, 92, wx + 26, 104], 180, 330, fill=(225, 240, 248), width=2)
    overlay_label_on(sd, w - 128, 6, "STRAIT OF HORMUZ", INK, 11)
    overlay_label_on(sd, 8, h - 26, "TWO TANKERS HIT", RED, 13)
    return s

def lead_tariffs(w, h):
    s, sd = scene_canvas(w, h, (198, 208, 220))
    sd.rectangle([0, h - 16, w, h], fill=(150, 160, 174))              # plaza
    bx, bw = 26, 168                                                   # Capitol
    sd.rectangle([bx, h - 26, bx + bw, h - 16], fill=(206, 212, 220),
                 outline=(110, 120, 136))
    sd.rectangle([bx + 8, h - 30, bx + bw - 8, h - 26], fill=(196, 204, 214),
                 outline=(110, 120, 136))
    for i in range(6):                                                 # columns
        cx = bx + 18 + i * 23
        sd.rectangle([cx, h - 62, cx + 8, h - 30], fill=(232, 236, 242),
                     outline=(110, 120, 136))
    sd.rectangle([bx + 6, h - 68, bx + bw - 6, h - 62], fill=(206, 212, 220),
                 outline=(110, 120, 136))
    sd.pieslice([bx + bw / 2 - 34, h - 102, bx + bw / 2 + 34, h - 62],
                180, 360, fill=(58, 78, 106))                          # dome
    sd.rectangle([bx + bw / 2 - 3, h - 112, bx + bw / 2 + 3, h - 98],
                 fill=(58, 78, 106))
    sd.rectangle([bx + bw / 2 - 7, h - 116, bx + bw / 2 + 7, h - 111],
                 fill=(178, 40, 44))                                   # flag
    dx, dy, dw, dh = w - 108, 22, 84, 76                               # document
    sd.rectangle([dx, dy, dx + dw, dy + dh], fill=(252, 252, 250),
                 outline=(150, 152, 158), width=1)
    sd.polygon([(dx + dw - 14, dy), (dx + dw, dy + 14), (dx + dw - 14, dy + 14)],
               fill=(205, 208, 212))
    sd.text((dx + dw / 2, dy + 30), "%", font=f(SERIF, 40), fill=RED,
            anchor="mm")
    sd.line([dx + 12, dy + 56, dx + dw - 12, dy + 56], fill=(170, 172, 178), width=2)
    sd.line([dx + 12, dy + 64, dx + dw - 26, dy + 64], fill=(170, 172, 178), width=2)
    overlay_label_on(sd, 8, h - 25, "WASHINGTON", INK, 11)
    overlay_label_on(sd, w - 118, h - 26, "NEW TARIFFS", RED, 13)
    return s

def lead_markets(w, h):
    s, sd = scene_canvas(w, h, (22, 32, 52))
    for i, (bw2, bh) in enumerate([(36, 34), (26, 48), (44, 28), (30, 56),
                                  (38, 40), (28, 62), (46, 32), (34, 44)]):
        bx = 4 + i * 41
        sd.rectangle([bx, h - bh, bx + bw2, h], fill=(43, 58, 84))
        for wy in range(h - bh + 6, h - 6, 9):                         # windows
            for wx in range(bx + 5, bx + bw2 - 5, 9):
                if (wx * 7 + wy * 13) % 5 == 0:
                    sd.rectangle([wx, wy, wx + 3, wy + 4], fill=(240, 205, 110))
    pts = [(14, 16), (62, 26), (104, 24), (140, 44), (178, 42), (214, 64),
           (258, 82)]
    sd.line(pts, fill=RED, width=4)
    sd.polygon([(258, 82), (240, 78), (248, 64)], fill=RED)            # arrowhead
    for (cx, cy, ch) in [(268, 40, 16), (284, 54, 20), (300, 70, 14)]:  # candles
        sd.rectangle([cx, cy, cx + 9, cy + ch], fill=(214, 48, 49))
        sd.line([cx + 4, cy - 4, cx + 4, cy + ch + 4], fill=(214, 48, 49), width=1)
    overlay_label_on(sd, 24, 6, "SEOUL", INK, 11, outline=WHITE)
    overlay_label_on(sd, 8, h - 26, "KOSPI −6.16%", RED, 13)
    return s

def overlay_label_on(sd, x, y, s, bg, font_sz=12, fg=WHITE, pad=6, outline=None):
    font = f(SANS_B, font_sz)
    w = sd.textlength(s, font=font) + 2 * pad
    sd.rectangle([x, y, x + w, y + font_sz + 8], fill=bg, outline=outline,
                 width=1 if outline else 0)
    sd.text((x + pad, y + (font_sz + 8) / 2), s, font=font, fill=fg, anchor="lm")
    return w

LEADS = [
    dict(n=1, scene=lead_hormuz, kicker="GULF · STRAIT OF HORMUZ", tag="CLAIM",
         head="Iran claims two tankers hit mines in Hormuz",
         body=("Iran's Revolutionary Guard said two oil tankers struck sea "
               "mines, exploded and caught fire in the Strait of Hormuz on "
               "what it called an unofficial route. The mine claim could not "
               "be independently verified. Oil prices moved on the news."),
         src="Reuters · Just Security"),
    dict(n=2, scene=lead_tariffs, kicker="TRADE · WASHINGTON", tag="CONFIRMED",
         head="US announces new tariffs, China among targets",
         body=("The Trump administration announced new tariffs against a host "
               "of trading partners including China, after a Section 301 "
               "probe into alleged subsidies and overcapacity in 16 "
               "economies. Specific rates had not been announced."),
         src="BBC · AP"),
    dict(n=3, scene=lead_markets, kicker="MARKETS · SEOUL", tag="CONFIRMED",
         head="Asian markets tumble: Kospi −6.16% in AI rout",
         body=("Asian stocks fell sharply as the AI sell-off deepened. "
               "Seoul's Kospi plunged 6.16% to 4,697.51, wiping out the "
               "previous day's 6.32% gain; Samsung fell 9.9% and SK Hynix "
               "11.1%. Taiwan's Taiex fell 4.80%, Tokyo's Nikkei 2.78%."),
         src="AP · Reuters"),
]

LY = 232
LCW = (CW - 26) // 3          # lead column width = 322
LBH = 112                     # lead banner height
for i, L in enumerate(LEADS):
    x = M + i * (LCW + 13)
    img.paste(L["scene"](LCW, LBH), (x, LY))
    rect(x, LY, LCW - 1, LBH - 1, outline=(120, 115, 105))
    circle_badge(x + 4, LY + 4, L["n"])
    ky = LY + LBH + 6
    text(x, ky, L["kicker"], f(SANS_B, 10), fill=RED)
    status_tag(x + LCW, ky - 2, L["tag"])
    hy = ky + 16
    for ln in wrap(L["head"], f(SERIF, 19), LCW):
        text(x, hy, ln, f(SERIF, 19), fill=INK)
        hy += 23
    by = hy + 3
    for ln in wrap(L["body"], f(SANS, 10), LCW):
        text(x, by, ln, f(SANS, 10), fill=(45, 45, 45))
        by += 12.5
    text(x, by + 1, "Sources: " + L["src"], f(SANS, 9), fill=GRAY)

# ---------------------------------------------------------------- secondaries
def sec_label(sd, x, y, s, bg):
    overlay_label_on(sd, x, y, s, bg, 9, pad=4)

def sec_badge(drw, x, y, n):
    r = 9
    drw.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=WHITE, width=2)
    drw.text((x, y), str(n), font=f(SANS_B, 10), fill=WHITE, anchor="mm")

def sec_samara(w, h):
    s, sd = scene_canvas(w, h, (198, 214, 230))
    sd.rectangle([18, 12, 30, h], fill=(110, 116, 124))                # towers
    sd.rectangle([44, 8, 54, h], fill=(96, 102, 112))
    sd.polygon([(46, 8), (52, -4), (58, 8)], fill=(240, 128, 28))      # flame
    sd.ellipse([70, 22, 108, h], fill=(130, 136, 144))                 # tanks
    sd.ellipse([112, 25, 142, h], fill=(118, 124, 134))
    sd.line([150, 8, 162, 14], fill=(30, 34, 40), width=2)             # drone
    sd.line([162, 8, 150, 14], fill=(30, 34, 40), width=2)
    sd.rectangle([154, 9, 160, 13], fill=(30, 34, 40))
    sec_label(sd, 4, h - 19, "REFINERIES ABLAZE", RED)
    return s

def sec_gaza(w, h):
    s, sd = scene_canvas(w, h, (216, 208, 192))
    for (bx, bw, bh) in [(14, 30, 30), (52, 24, 22), (120, 34, 32), (160, 24, 24)]:
        sd.rectangle([bx, h - bh, bx + bw, h], fill=(150, 144, 132))
        for wy in range(h - bh + 5, h - 5, 7):
            for wx in range(bx + 4, bx + bw - 4, 8):
                sd.rectangle([wx, wy, wx + 3, wy + 3], fill=(96, 92, 84))
    starburst(sd, 96, 12, 13, 6, (240, 128, 28))
    sd.ellipse([86, 0, 106, 10], fill=(150, 150, 150))
    sec_label(sd, 4, h - 19, "GAZA CITY", INK)
    return s

def sec_cartagena(w, h):
    s, sd = scene_canvas(w, h, (208, 226, 236))
    sd.rectangle([24, 10, w - 24, h], fill=(238, 240, 242))            # store
    for i in range(9):                                                 # awning
        sd.rectangle([24 + i * 16, 10, 24 + (i + 1) * 16, 17],
                     fill=(198, 16, 44) if i % 2 == 0 else (245, 245, 245))
    sd.rectangle([78, 22, 112, h], fill=(90, 110, 130))                # doors
    sd.rectangle([34, 22, 66, 30], fill=(170, 200, 220))
    sd.rectangle([124, 22, 156, 30], fill=(170, 200, 220))
    sec_label(sd, 4, h - 19, "HOSTAGES FREED", RED)
    return s

def sec_shenzhou(w, h):
    s, sd = scene_canvas(w, h, (22, 32, 52))
    for (sx, sy) in [(12, 6), (40, 14), (80, 5), (150, 10), (176, 20), (105, 16)]:
        sd.rectangle([sx, sy, sx + 2, sy + 2], fill=(240, 240, 220))
    sd.polygon([(88, 34), (96, 20), (104, 34)], fill=(250, 196, 60))   # flame
    sd.rectangle([90, 8, 102, 34], fill=(238, 238, 238))               # rocket
    sd.polygon([(90, 8), (96, 0), (102, 8)], fill=(198, 16, 44))
    sd.rectangle([90, 16, 102, 20], fill=(198, 16, 44))
    sd.rectangle([140, 12, 158, 18], fill=(200, 204, 210))             # station
    sd.rectangle([126, 10, 139, 20], fill=(70, 110, 170))
    sd.rectangle([159, 10, 172, 20], fill=(70, 110, 170))
    sec_label(sd, 4, h - 19, "SHENZHOU-24", INK)
    return s

def sec_solomon(w, h):
    s, sd = scene_canvas(w, h, (206, 228, 238))
    sd.line([30, 4, 30, h], fill=(90, 80, 70), width=2)                # poles
    sd.line([72, 4, 72, h], fill=(90, 80, 70), width=2)
    sd.polygon([(30, 5), (64, 10), (30, 18)], fill=(40, 150, 80))      # Solomon
    sd.polygon([(30, 5), (64, 10), (30, 11)], fill=(250, 200, 40))
    sd.rectangle([72, 5, 106, 19], fill=(40, 70, 150))                 # Australia
    for (sx, sy) in [(79, 8), (90, 13), (97, 8), (86, 16)]:
        sd.rectangle([sx, sy, sx + 2, sy + 2], fill=WHITE)
    sd.rectangle([126, 12, 168, 32], fill=(252, 252, 250),
                 outline=(150, 152, 158))                              # document
    sd.line([132, 19, 162, 19], fill=(170, 172, 178), width=2)
    sd.line([132, 25, 156, 25], fill=(170, 172, 178), width=2)
    sec_label(sd, 4, h - 19, "AUSTRALIA TREATY", INK)
    return s

def sec_bangladesh(w, h):
    s, sd = scene_canvas(w, h, (210, 220, 208))
    sd.rectangle([14, 18, 120, h], fill=(176, 168, 152))               # factory
    sd.rectangle([24, 4, 34, 18], fill=(140, 132, 118))
    sd.rectangle([96, 2, 106, 18], fill=(140, 132, 118))
    sd.ellipse([92, -2, 112, 6], fill=(170, 170, 170))
    for wx in range(22, 114, 12):
        sd.rectangle([wx, 24, wx + 6, 30], fill=(96, 100, 96))
    sd.rectangle([132, 8, 178, 30], fill=(252, 252, 250),
                 outline=(150, 152, 158))                              # placard
    sd.text((155, 19), "36%", font=f(SANS_B, 15), fill=RED, anchor="mm")
    sec_label(sd, 4, h - 19, "WAGE RISE 36%", RED)
    return s

def sec_bogor(w, h):
    s, sd = scene_canvas(w, h, (198, 222, 200))
    sd.polygon([(0, h), (52, 6), (104, h)], fill=(96, 140, 92))        # hills
    sd.polygon([(66, h), (118, 12), (170, h)], fill=(80, 124, 78))
    sd.pieslice([76, 18, 106, 44], 180, 360, fill=(40, 34, 26))        # mine mouth
    sd.rectangle([76, 30, 106, h], fill=(40, 34, 26))
    sd.rectangle([0, h - 8, w, h], fill=(70, 130, 180))                # flood water
    for (gx, gy) in [(30, 26), (150, 24), (164, 30)]:
        sd.ellipse([gx, gy, gx + 4, gy + 4], fill=(240, 200, 60))      # gold
    sec_label(sd, 4, h - 19, "BOGOR MINE", INK)
    return s

def sec_sudan(w, h):
    s, sd = scene_canvas(w, h, (226, 210, 178))
    for (hx, hw) in [(16, 34), (66, 30), (140, 36)]:
        sd.rectangle([hx, 18, hx + hw, h], fill=(196, 172, 138))
        sd.polygon([(hx - 3, 18), (hx + hw / 2, 8), (hx + hw + 3, 18)],
                   fill=(150, 104, 66))
    sd.line([100, 6, 114, 12], fill=(30, 34, 40), width=2)             # drone
    sd.line([114, 6, 100, 12], fill=(30, 34, 40), width=2)
    sd.rectangle([103, 7, 111, 11], fill=(30, 34, 40))
    sec_label(sd, 4, h - 19, "19 DEAD", RED)
    return s

def sec_eurostar(w, h):
    s, sd = scene_canvas(w, h, (206, 216, 226))
    sd.rectangle([10, 12, w - 14, 30], fill=(216, 219, 224))           # body
    sd.polygon([(w - 14, 12), (w - 2, 20), (w - 2, 30), (w - 14, 30)],
               fill=(250, 200, 40))                                    # yellow nose
    sd.rectangle([16, 17, w - 40, 23], fill=(90, 110, 140))            # windows
    sd.line([10, 32, w - 2, 32], fill=(90, 90, 96), width=2)           # rail
    sec_label(sd, 4, h - 19, "EUROSTAR STRIKE", INK)
    return s

def sec_ramaphosa(w, h):
    s, sd = scene_canvas(w, h, (216, 212, 198))
    sd.polygon([(30, 4), (66, 16), (102, 16)], fill=(120, 110, 96))    # pediment
    for i in range(4):
        sd.rectangle([38 + i * 16, 18, 44 + i * 16, 32], fill=(238, 236, 228))
    sd.rectangle([30, 32, 102, h], fill=(120, 110, 96))
    sd.line([128, 26, 148, 12], fill=(120, 84, 40), width=4)           # gavel
    sd.rectangle([142, 6, 158, 14], fill=(150, 104, 52))
    sec_label(sd, 4, h - 19, "COURT WIN", INK)
    return s

SECS = [
    dict(n=4, scene=sec_samara, kicker="RUSSIA · WAR", tag="REPORTED",
         head="Ukrainian drones set two refineries ablaze",
         body="Kyiv said its drones hit two Rosneft refineries in Samara, killing one.",
         src="Reuters"),
    dict(n=5, scene=sec_gaza, kicker="GAZA · WAR", tag="CONFIRMED",
         head="Israel kills senior Hamas security chief",
         body="Strike killed Hamas colonel Mohammad Abuelouf, his wife and two children.",
         src="Reuters"),
    dict(n=6, scene=sec_cartagena, kicker="COLOMBIA · HOSTAGES", tag="CONFIRMED",
         head="All hostages freed in Cartagena raid",
         body="Forces stormed an Éxito supermarket and freed the last 20 hostages.",
         src="Reuters · AFP · BBC"),
    dict(n=7, scene=sec_shenzhou, kicker="SPACE · CHINA", tag="CONFIRMED",
         head="Shenzhou-24 carries first Pakistani to Tiangong",
         body="China launched Shenzhou-24 from Jiuquan with Pakistan's Muhammad Zeeshan Ali aboard.",
         src="AP · BBC"),
    dict(n=8, scene=sec_solomon, kicker="PACIFIC · TREATY", tag="OFFICIAL",
         head="Solomon Islands signs Australia treaty",
         body="Treaty signed in Canberra makes Australia the islands' principal security partner.",
         src="AP · NYT"),
    dict(n=9, scene=sec_bangladesh, kicker="BANGLADESH · WAGES", tag="OFFICIAL",
         head="Bangladesh raises garment wage 36%",
         body="Minimum wage rises 36% to 17,000 taka (~$136) after a 12-hour wage-board session.",
         src="AP · Reuters"),
    dict(n=10, scene=sec_bogor, kicker="INDONESIA · MINE", tag="CONFIRMED",
         head="Three bodies found in flooded Bogor mine",
         body="Three bodies found; 23 miners still missing in the flooded, unlicensed mine.",
         src="Reuters · AP"),
    dict(n=11, scene=sec_sudan, kicker="SUDAN · WAR", tag="REPORTED",
         head="RSF drone strikes kill 19 civilians",
         body="Drones killed 19 civilians, six of them women, in Damazin and Roseires, lawyers said.",
         src="Reuters"),
    dict(n=12, scene=sec_eurostar, kicker="EUROPE · RAIL", tag="CONFIRMED",
         head="Eurostar strike cancels Paris–London trains",
         body="Paris-based staff walked out in a pay dispute, cancelling morning trains.",
         src="AP"),
    dict(n=13, scene=sec_ramaphosa, kicker="S. AFRICA · COURTS", tag="CONFIRMED",
         head="Ramaphosa wins court fight over impeachment",
         body="A court set aside the Phala Phala impeachment report — for now.",
         src="BBC"),
]

SY = 472
SCW = 190
SHH = 38                       # secondary header height
for r in range(2):
    row_y = SY + r * 118
    for c in range(5):
        S = SECS[r * 5 + c]
        x = M + c * 200
        img.paste(S["scene"](SCW, SHH), (x, row_y))
        rect(x, row_y, SCW - 1, SHH - 1, outline=(120, 115, 105))
        sec_badge(d, x + 3, row_y + 3, S["n"])
        ky = row_y + SHH + 4
        text(x, ky, S["kicker"], f(SANS_B, 8), fill=RED)
        status_tag(x + SCW, ky - 3, S["tag"])
        hy = ky + 12
        for ln in wrap(S["head"], f(SERIF, 12), SCW):
            text(x, hy, ln, f(SERIF, 12), fill=INK)
            hy += 14
        by = hy + 1
        for ln in wrap(S["body"], f(SANS, 8), SCW)[:3]:
            text(x, by, ln, f(SANS, 8), fill=(45, 45, 45))
            by += 10.5
        text(x, by + 1, S["src"], f(SANS, 8), fill=GRAY)

# ---------------------------------------------------------------- briefs
BRIEFS = [
    (14, "NA", "MADRID — Ábrego García in Spain, saga ends · BBC·AP", "C"),
    (15, "NA", "IOWA — Army to blast unstable explosives · AP", "R"),
    (16, "NA", "USA — 81.5m travel for Thanksgiving · AP·Reuters", "C"),
    (17, "NA", "WASHINGTON — Melania reunites 7th group; 43 children · AP", "R"),
    (18, "NA", "USA — Pentagon to audit military base schools · AP", "R"),
    (19, "NA", "USA — GoFundMe warns donors of data breach · AP", "R"),
    (20, "NA", "SEATTLE — Amazon buys Decart for AI chips · Principia", "R"),
    (21, "EU", "EUROZONE — Inflation rises to 4.0% · Principia", "O"),
    (22, "EU", "BERLIN — Merz: Russia 'escalating' threat · Reuters", "R"),
    (23, "EU", "BERLIN — Germany weighs US troop pullback · POLITICO", "R"),
    (24, "EU", "PARIS — Sarkozy, Carla Bruni to face trial · BBC", "R"),
    (25, "EU", "LONDON — UK energy bills to rise 26% · BBC", "R"),
    (26, "EU", "LUTON — EasyJet profit falls 89% · Principia", "R"),
    (27, "EU", "NORFOLK — Two charged over William break-in · AP·BBC", "C"),
    (28, "EU", "VATICAN — Pope dismayed at COP31 failure · AP", "R"),
    (29, "ME", "RAS TANURA — Houthis claim refinery hit · Reuters", "CL"),
    (30, "ME", "BENGHAZI — Libya vows revenge on Ukraine · AP·Reuters", "C"),
    (31, "ME", "TEHRAN — Iran 'not worried' over blockade · Reuters", "R"),
    (32, "ME", "ISLAMABAD — Pakistan warns of energy crisis · SRI", "R"),
    (33, "AS", "SHANGHAI — China probes party chief Chen · Daily Summary", "R"),
    (34, "AS", "SEOUL — Russian jets entered air zone · SRI", "R"),
    (35, "AS", "INDIA — Rising cost of food on the table · BBC", "R"),
    (36, "AS", "TOKYO — Services inflation at 36-year high · Reuters", "R"),
    (37, "AS", "N. KOREA — Jailed for being Christian · BBC", "R"),
    (38, "AF", "ITURI — Fighting traps Ebola responders · PANA·WHO", "C"),
    (39, "AF", "HARARE — Arrest warrant for Mugabe's son · BBC", "R"),
    (40, "AF", "DAKAR — CAF: Senegal keep AFCON title · BBC", "C"),
    (41, "AF", "NIGERIA — Nollywood's Pete Edochie dies, 79 · BBC", "R"),
    (42, "SA", "QUITO — US pauses joint ops with Ecuador · Atlantic", "R"),
    (43, "OC", "CANBERRA — Australian inflation hits 4.9% · Principia", "R"),
    (44, "OC", "CANBERRA — Safety law: Big Tech faces huge fines · AP", "R"),
    (45, "OC", "WELLINGTON — NZ netball league collapses · BBC", "R"),
]
assert [b[0] for b in BRIEFS] == list(range(14, 46))

BY = 714
text(M, BY, "ALSO ON WEDNESDAY · 32 MORE, BY REGION", f(SANS_B, 12), fill=INK)
leg = "C 2+ outlets · O official · R one outlet · CL one side's claim"
text(664, BY + 2, leg, f(SANS, 9), fill=GRAY, anchor="ra")
d.line([M, BY + 16, W - M, BY + 16], fill=RULE, width=1)

BRY = BY + 22
BCW = 316
for i, (n, reg, s, badge) in enumerate(BRIEFS):
    col = 0 if i < 16 else 1
    row = i if i < 16 else i - 16
    x = M + col * (BCW + 16)
    y = BRY + row * 13.5
    chip_num(x, y, n, REG[reg], size=13, font_sz=8)
    city, rest = s.split(" — ", 1)
    tx = x + 17
    text(tx, y + 1, city, f(SANS_B, 9), fill=INK)
    tx += tw(city, f(SANS_B, 9))
    text(tx, y + 1, " — " + rest, f(SANS, 9), fill=(45, 45, 45))
    source_badge(x + BCW - 7, y + 6.5, badge)

# ---------------------------------------------------------------- world map
from PIL import ImageFilter

LAND = [
    # North & Central America
    [(-168, 65), (-155, 71), (-141, 70), (-132, 70), (-122, 71), (-110, 72),
     (-98, 79), (-90, 80), (-84, 76), (-88, 72), (-93, 66), (-95, 60),
     (-90, 56), (-84, 54), (-79, 50), (-76, 46), (-70, 44), (-66, 45),
     (-61, 46), (-65, 42), (-69, 40), (-72, 38), (-75, 36), (-79, 33),
     (-81, 31), (-80, 27), (-82, 24), (-85, 20), (-88, 16), (-92, 15),
     (-97, 16), (-102, 18), (-105, 21), (-108, 24), (-111, 28), (-114, 31),
     (-118, 33), (-121, 35), (-124, 41), (-124, 47), (-121, 51), (-127, 55),
     (-133, 58), (-141, 60), (-152, 59), (-158, 56), (-164, 59)],
    # Greenland
    [(-46, 60), (-32, 68), (-22, 70), (-19, 76), (-28, 81), (-50, 80),
     (-56, 74), (-54, 66), (-51, 61)],
    # South America
    [(-79, 9), (-72, 12), (-64, 11), (-56, 6), (-51, 1), (-45, -2),
     (-36, -7), (-38, -14), (-39, -21), (-47, -26), (-52, -33), (-57, -39),
     (-62, -42), (-65, -46), (-67, -51), (-68, -55), (-71, -54), (-73, -50),
     (-74, -45), (-73, -38), (-72, -31), (-70, -22), (-70, -18), (-75, -15),
     (-78, -9), (-80, -5), (-80, 1)],
    # Europe
    [(-10, 37), (-9, 43), (-2, 44), (-5, 48), (-1, 50), (3, 52), (6, 54),
     (8, 56), (9, 58), (6, 59), (5, 61), (11, 60), (18, 59), (21, 61),
     (24, 66), (30, 70), (40, 67), (48, 65), (45, 58), (38, 52), (30, 50),
     (24, 48), (28, 46), (30, 42), (26, 39), (23, 36), (19, 40), (15, 39),
     (12, 39), (10, 37), (4, 37), (-1, 37), (-6, 36)],
    # Asia incl. Arabia, India, SE Asia
    [(40, 67), (55, 66), (68, 68), (85, 70), (105, 72), (125, 72), (145, 71),
     (162, 68), (176, 65), (178, 62), (168, 61), (160, 57), (155, 52),
     (148, 49), (143, 47), (141, 41), (137, 36), (131, 33), (127, 38),
     (122, 31), (121, 26), (116, 21), (110, 18), (108, 13), (106, 7),
     (104, 2), (101, 5), (99, 9), (97, 14), (94, 17), (91, 22), (88, 22),
     (86, 20), (83, 17), (80, 14), (77, 8), (75, 12), (73, 17), (72, 20),
     (68, 23), (65, 25), (60, 25), (56, 26), (52, 27), (50, 30), (48, 30),
     (50, 25), (55, 25), (58, 23), (59, 22), (55, 18), (52, 16), (48, 14),
     (44, 12), (43, 13), (40, 17), (38, 22), (35, 29), (34, 31), (36, 36),
     (33, 30), (30, 36), (27, 37), (30, 42), (28, 46), (24, 48), (30, 50),
     (38, 52), (45, 58)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (35, 28), (38, 24), (40, 20), (43, 12), (48, 11), (51, 12), (45, 5),
     (42, -2), (40, -8), (40, -15), (38, -22), (35, -28), (32, -29),
     (26, -33), (20, -35), (17, -32), (15, -27), (13, -20), (12, -15),
     (13, -8), (9, -2), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8),
     (-17, 12), (-17, 16), (-16, 21), (-15, 25), (-13, 28), (-9, 31)],
    [(44, -16), (47, -15), (50, -18), (48, -22), (46, -25), (45, -22),
     (44, -18)],                                                    # Madagascar
    [(-5, 50), (-2, 51), (-1, 53), (-3, 55), (-6, 56), (-8, 58), (-6, 59),
     (-3, 57), (-2, 54), (-4, 51)],                                 # Britain
    [(-22, 64), (-15, 64), (-14, 66), (-20, 66), (-22, 65)],        # Iceland
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 36), (141, 39),
     (142, 43), (141, 45), (139, 40), (137, 36), (133, 34), (130, 32)],  # Japan
    [(126, 35), (128, 35), (129, 37), (128, 40), (126, 39)],        # Korea
    [(120, 13), (122, 13), (121, 16), (120, 18), (119, 15)],        # Philippines
    [(95, 5), (99, 2), (103, -2), (106, -6), (103, -5), (99, 0), (96, 4)],  # Sumatra
    [(109, 1), (110, 3), (114, 4), (117, 6), (119, 3), (118, -1),
     (114, -3), (110, -2)],                                         # Borneo
    [(105, -6), (109, -7), (113, -8), (114, -9), (108, -8), (105, -7)],  # Java
    [(119, 0), (121, 1), (120, -3), (119, -5), (118, -2)],          # Sulawesi
    [(131, -1), (135, -2), (140, -3), (145, -5), (149, -9), (146, -8),
     (141, -6), (136, -4), (132, -3)],                              # New Guinea
    # Australia
    [(113, -22), (114, -29), (115, -34), (119, -35), (126, -32), (131, -32),
     (134, -33), (136, -35), (138, -36), (140, -38), (144, -38), (147, -39),
     (150, -37), (153, -31), (153, -26), (151, -21), (149, -17), (146, -15),
     (143, -13), (142, -11), (141, -15), (140, -19), (137, -16), (136, -15),
     (135, -12), (132, -11), (129, -13), (125, -15), (121, -18), (117, -20)],
    [(173, -35), (176, -37), (178, -38), (176, -40), (174, -41), (173, -39)],
    [(167, -45), (169, -44), (171, -42), (173, -42), (171, -44), (168, -47)],
    [(-85, 23), (-80, 23), (-75, 21), (-74, 20), (-79, 22), (-84, 22)],  # Cuba
]

MX, MW2 = 680, W - M - 680
text(MX, BY, "WHERE IT HAPPENED · PINS 1–13", f(SANS_B, 12), fill=INK)
MY, MH2 = BY + 22, 152
LAT_T, LAT_B = 78, -58

def proj(lon, lat):
    return (MX + (lon + 180) / 360 * MW2, MY + (LAT_T - lat) / (LAT_T - LAT_B) * MH2)

mimg = Image.new("RGB", (MW2, MH2), (196, 218, 231))
md2 = ImageDraw.Draw(mimg)
for lon in range(-160, 180, 20):                                     # graticule
    gx = (lon + 180) / 360 * MW2
    md2.line([gx, 0, gx, MH2], fill=(172, 199, 216), width=1)
for lat in range(-40, 80, 20):
    gy = (LAT_T - lat) / (LAT_T - LAT_B) * MH2
    md2.line([0, gy, MW2, gy], fill=(172, 199, 216), width=1)
mask = Image.new("L", (MW2, MH2), 0)
mk = ImageDraw.Draw(mask)
for poly in LAND:
    mk.polygon([(x - MX, y - MY) for x, y in (proj(lon, lat) for lon, lat in poly)],
               fill=255)
land_img = Image.new("RGB", (MW2, MH2), (233, 221, 192))
mimg.paste(land_img, (0, 0), mask)
edge = mask.filter(ImageFilter.MaxFilter(3))
diff = Image.new("L", (MW2, MH2), 0)
diff.paste(edge, (0, 0))
import PIL.ImageChops as _chops
diff = _chops.subtract(edge, mask)
mimg.paste(Image.new("RGB", (MW2, MH2), (176, 160, 124)), (0, 0), diff)
img.paste(mimg, (MX, MY))
rect(MX, MY, MW2 - 1, MH2 - 1, outline=(120, 115, 105))
for (lx, ly, lab) in [(0.30, 0.06, "ARCTIC"), (0.03, 0.42, "PACIFIC"),
                      (0.33, 0.40, "ATLANTIC"), (0.60, 0.74, "INDIAN"),
                      (0.88, 0.68, "PACIFIC"), (0.44, 0.93, "SOUTHERN")]:
    d.text((MX + lx * MW2, MY + ly * MH2), lab, font=f(SERIF_I, 9),
           fill=(110, 140, 160))

PINS = [(1, 56.3, 26.5, "ME", "Hormuz"), (2, -77.0, 38.9, "NA", "Washington"),
        (3, 127.0, 37.6, "AS", "Seoul"), (4, 50.1, 53.2, "EU", "Samara"),
        (5, 34.47, 31.5, "ME", "Gaza"), (6, -75.5, 10.4, "SA", "Cartagena"),
        (7, 98.5, 39.7, "AS", "Jiuquan"), (8, 149.1, -35.3, "OC", "Canberra"),
        (9, 90.4, 23.8, "AS", "Dhaka"), (10, 106.8, -6.6, "AS", "Bogor"),
        (11, 34.35, 11.8, "AF", "Damazin"), (12, 2.35, 48.85, "EU", "Paris"),
        (13, 28.2, -25.7, "AF", "Pretoria")]
for n, lon, lat, reg, _name in PINS:
    px, py = proj(lon, lat)
    r = 8
    d.ellipse([px - r, py - r, px + r, py + r], fill=REG[reg], outline=WHITE,
              width=1)
    d.text((px, py), str(n), font=f(SANS_B, 8), fill=WHITE, anchor="mm")

IY = MY + MH2 + 6
idx = ("1 Hormuz · 2 Washington · 3 Seoul · 4 Samara · 5 Gaza · 6 Cartagena · "
       "7 Jiuquan · 8 Canberra · 9 Dhaka · 10 Bogor · 11 Damazin · 12 Paris · "
       "13 Pretoria")
for ln in wrap(idx, f(SANS, 8), MW2):
    text(MX, IY, ln, f(SANS, 8), fill=GRAY)
    IY += 10.5
IY += 2
lx = MX
for k, c in tally:
    d.ellipse([lx, IY + 1, lx + 7, IY + 8], fill=REG[k])
    s = f"{REGNAME[k].title()} {c}"
    text(lx + 10, IY, s, f(SANS, 8), fill=(45, 45, 45))
    lx += 10 + tw(s, f(SANS, 8)) + 8
    if lx > MX + MW2 - 60:
        lx = MX
        IY += 11

# ---------------------------------------------------------------- DATE CHECK
DY = 956
rect(M, DY, 88, 15, fill=RED)
d.text((M + 44, DY + 7.5), "DATE CHECK", font=f(SANS_B, 9), fill=WHITE,
       anchor="mm")
dc = ("Left off as earlier news — Tue 24 Nov: Huawei guilty of trade-secret "
      "conspiracy · CIA & ODNI unclassified systems breached · Houthi drone "
      "hits Riyadh tower, 11 hurt · Two Libyan officers die of Benghazi "
      "wounds · Cessna crash off Mississippi kills 6, incl. 2 children · CAS "
      "restores Senegal's AFCON title · Dell posts record Q3: $54.9bn "
      "revenue · Democrats win House majority, 259 seats · Thomas Markle "
      "charged in US federal court · Zelenskyy: Ukraine needs €115bn for "
      "2027 · Russian strikes on Odesa & Kyiv overnight, 2 killed (24–25 "
      "Nov) · BBC analysis: Russia has lost 490,334+ troops since 2022")
dyy = DY - 1
for ln in wrap(dc, f(SANS, 9), CW - 98):
    text(M + 98, dyy, ln, f(SANS, 9), fill=(45, 45, 45))
    dyy += 11

# ---------------------------------------------------------------- footer
FY = 1006
d.line([M, FY - 4, W - M, FY - 4], fill=RULE, width=1)
text(W / 2, FY, "Every story happened or was first reported on Wednesday "
     "25 Nov 2026 (UTC) · sources named on each item · original drawings, "
     "no photos", f(SANS, 9), fill=GRAY, anchor="ma")

img.save("news.png")
print("saved news.png", img.size)
