# build_page22_r2.py — The World Today, Sunday 22 November 2026 (round 2).
#
# Fresh round-2 generator: new lead hierarchy (Sparta II promoted to lead 3),
# COP31 de-padded, all-Sunday briefs, richer lead art with NO label chips on
# the art panels. Deterministic: no clock, no randomness, no network.
# Run: python3 build_page22_r2.py  ->  writes entry.png (1024x1024) here.
# Then: python3 build_page22_r2.py again and compare sha256 (must match).

import hashlib
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 20
CW = W - 2 * MARGIN  # 984

FDIR = "/usr/share/fonts/truetype"
SERIF = os.path.join(FDIR, "liberation/LiberationSerif-Regular.ttf")
SERIF_B = os.path.join(FDIR, "liberation/LiberationSerif-Bold.ttf")
SERIF_I = os.path.join(FDIR, "liberation/LiberationSerif-Italic.ttf")
SANS = os.path.join(FDIR, "liberation/LiberationSans-Regular.ttf")
SANS_B = os.path.join(FDIR, "liberation/LiberationSans-Bold.ttf")
COND_B = os.path.join(FDIR, "noto/NotoSerif-CondensedBold.ttf")
COND = os.path.join(FDIR, "noto/NotoSerif-Condensed.ttf")

INK = (18, 18, 18)
PAPER = (255, 255, 255)
RED = (178, 34, 34)
RULE = (120, 120, 120)
LIGHT = (242, 242, 240)
MIDGREY = (110, 110, 110)
DARK = (38, 38, 38)


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# (dateline, source, headline, body, art_key)
LEADS = [
    ("ANTALYA", "REUTERS",
     "COP31 closes in on a deal at dawn",
     "Objections to the draft are due at 03:00 GMT; the approval session is "
     "set for 06:00 GMT. President Kurum says he has put forward a text "
     "\u201call the parties can agree upon\u201d \u2014 but fossil fuels still "
     "divide the room.",
     "cop31"),
    ("MANAMA", "ANI / EURONEWS",
     "Iran hits US bases in Bahrain",
     "Two overnight waves struck US facilities, the IRGC says, claiming two "
     "Patriot radars destroyed at al-Riffa and Awali. Bahrain says a "
     "civilian site burned; Washington has yet to confirm the damage.",
     "bahrain"),
    ("GULF OF FINLAND", "RFE/RL",
     "Sparta II still ablaze off Finland",
     "The fire aboard the 121-metre Russian freighter is still out of "
     "control after Saturday\u2019s drone hits, and Helsinki warns it could "
     "rage for days. All 16 crew are safe. PM Orpo: \u201cThe war is "
     "spilling over into our neighbouring areas.\u201d",
     "sparta"),
]

# (dateline, source, headline, body, art_key)
FEATURES = [
    ("NEW DELHI", "IANS",
     "Nepal PM flies to Delhi on first state visit",
     "Balendra Shah arrives with a 34-member delegation for talks with Modi "
     "on Monday \u2014 and a Rs 200bn aid ask.",
     "nepal"),
    ("TEHRAN", "STATE TV",
     "Iran rations power from today",
     "Rolling cuts of up to two hours a day begin today. Pezeshkian said "
     "Saturday\u2019s strikes worsened the shortage.",
     "power"),
    ("HONG KONG", "STRAITS TIMES",
     "Hong Kong votes for 723 seats",
     "Polls are open 9am\u20136pm: 856 candidates, 723 seats, 5,700 voters. "
     "Turnout hit 44.74% by 10am.",
     "vote"),
    ("MECCA", "ANADOLU",
     "Saudi coalition downs missile near Mecca",
     "An air alert sounded in Riyadh at 23:43 on Saturday; the missile was "
     "downed in the early hours of Sunday.",
     "mecca"),
    ("TURIN", "ATP",
     "Zverev v Alcaraz for the title",
     "The ATP Finals end at 18:00 CET. Alcaraz beat Shelton 3-6, 6-3, "
     "7-6(1); Zverev beat Medvedev 7-6(0), 6-4. FORECAST",
     "atp"),
    ("LAS VEGAS", "F1",
     "Verstappen on pole in Las Vegas",
     "50 laps from 8pm local, round 21 of 23. Antonelli was fastest but "
     "starts sixth after a five-place penalty. FORECAST",
     "f1"),
    ("NEW YORK", "MARKETS",
     "Bitcoin holds above $60,000",
     "$60,164 at 00:58 UTC, steady after Saturday\u2019s plunge to $55,130 "
     "\u2014 the lowest since September 2024.",
     "bitcoin"),
    ("MOGADISHU", "REUTERS",
     "Somalia deadline ends today",
     "The 72-hour order expelling the UAE envoy, issued on 19 November, "
     "runs out today with no sign of a climbdown from either side.",
     "somalia"),
    ("PARIS", "AFP",
     "France takes Myanmar to the UN",
     "France is taking Myanmar to the United Nations over the Rohingya "
     "case, after rejecting the ICJ verdict and seeking a new hearing.",
     "un"),
    ("LIVERPOOL", "PREMIER LEAGUE",
     "Pochettino debut at Anfield",
     "The new United boss takes his side to Liverpool at 16:30 GMT, with "
     "United 19th in the table. FORECAST",
     "stadium"),
]

# (city, text) — briefs 14-28
BRIEFS = [
    ("WELLINGTON", "India 629/6 at lunch on day four; Pant 128."),
    ("NFL", "Week 12 Sunday slate kicks off across the US. FORECAST"),
    ("VATICAN", "Pope Leo XIV leads the Sunday Angelus in St Peter\u2019s Square."),
    ("COPENHAGEN", "Denmark urges the EU to curb travel by Russians."),
    ("BRUSSELS", "EU agrees a provisional \u20ac45bn loan for Ukraine."),
    ("KATHMANDU", "Shah seeks Rs 200bn in aid from Delhi."),
    ("ANTALYA", "Draft sets a 35%-by-2035 goal for clean electricity."),
    ("ANTALYA", "Bowen: a deal is \u201cstill possible\u201d before dawn."),
    ("NEW DELHI", "Jaishankar to call on Shah at 6pm."),
    ("ADDIS ABABA", "COP32 goes to Ethiopia in November 2027."),
    ("WASHINGTON", "CENTCOM denies Iran\u2019s claim it damaged F-16s."),
    ("KHARTOUM", "Relief group says RSF killed civilians, among them three children, in West Kordofan."),
    ("JERUSALEM", "Eisenkot invites Likud to resume coalition talks from today."),
    ("ANTALYA", "Draft drops the $120bn adaptation-finance target."),
    ("PRETORIA", "Flags at half-mast; a prayer service honours Phumzile Mlambo-Ngcuka, who died on Friday."),
]

STATS = [
    ("03:00", "GMT \u2014 COP31 objections due"),
    ("2 HRS", "Iran power cuts from today"),
    ("5,700", "Hong Kong voters"),
    ("$60,164", "Bitcoin holds"),
    ("16", "Sparta II crew safe"),
    ("629/6", "India at lunch, Wellington"),
]

REGIONS = [
    ("EUROPE", 7), ("MIDDLE EAST", 5), ("ASIA-PACIFIC", 4),
    ("AFRICA", 4), ("GLOBAL", 4), ("AMERICAS", 3), ("OCEANIA", 1),
]

DATECHECK = [
    "Ukraine barrage \u2014 Fri", "Peru quake \u2014 Fri",
    "El Chapo capture \u2014 Fri", "Kuwait strike \u2014 Wed",
    "EU\u2013Indonesia pact \u2014 Sat", "Gaza aid-van strike \u2014 Sat",
    "Cyclone Akvan \u2014 Sat", "Nvidia probe \u2014 Fri",
    "Sudan landmine \u2014 Fri", "Japan poll \u2014 Fri",
    "Melbourne T20 \u2014 Sat", "Venezuela report \u2014 12 Nov",
    "USDA/FBI hacks \u2014 Fri", "Baltiysk blasts \u2014 Sat",
    "Doha talks \u2014 Fri", "Riemann proof verified \u2014 Sat",
]

# map pins for stories 01-13: (lon, lat)
PINS = [
    (30.7, 36.9), (50.6, 26.2), (24.0, 59.9), (77.2, 28.6),
    (51.4, 35.7), (114.2, 22.3), (39.8, 21.4), (7.7, 45.1),
    (-115.1, 36.1), (-74.0, 40.7), (45.3, 2.0), (2.35, 48.85),
    (-2.99, 53.4),
]

assert len(LEADS) + len(FEATURES) + len(BRIEFS) == 28
assert sum(n for _, n in REGIONS) == 28
assert len(PINS) == 13


# ---------------------------------------------------------------- helpers
def wrap(font, text, width, max_lines=None):
    """Greedy word wrap; returns list of lines. Asserts fit if max given."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None:
        assert len(lines) <= max_lines, (
            "wrap overflow: %r -> %d lines (max %d): %s"
            % (text[:40], len(lines), max_lines, lines))
    return lines


def vgrad(d, x, y, w, h, top, bottom):
    """Vertical gradient (deterministic)."""
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        d.line([(x, y + i), (x + w - 1, y + i)], fill=c)


def starburst(d, cx, cy, r1, r2, n, fill):
    """n-point starburst polygon."""
    import math
    pts = []
    for i in range(2 * n):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def flames(d, x, y, w, h, seed=0):
    """Layered flame tongues across a box (deterministic)."""
    import math
    n = max(3, int(w // 16))
    for k in range(n):
        fx = x + (k + 0.5) * (w / n)
        fw = w / n * 0.9
        fh = h * (0.55 + 0.35 * abs(math.sin(seed + k * 1.7)))
        col = [(255, 120, 0), (255, 170, 20), (230, 60, 10)][k % 3]
        d.polygon([(fx - fw / 2, y + h), (fx, y + h - fh),
                   (fx + fw / 2, y + h)], fill=col)
        d.ellipse([fx - fw / 4, y + h - fh * 0.45, fx + fw / 4,
                   y + h - fh * 0.15], fill=(255, 220, 90))

# ---------------------------------------------------------------- art
# Every art panel is a drawn illustration; no text or label chips on the art.

def art_cop31(d, x, y, w, h):
    vgrad(d, x, y, w, h, (28, 34, 78), (232, 130, 55))
    d.ellipse([x + w * 0.42, y + h * 0.30, x + w * 0.62, y + h * 0.62],
              fill=(255, 214, 130))
    # conference hall silhouette with lit windows
    d.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.94, y + h], fill=(22, 22, 30))
    d.rectangle([x + w * 0.30, y + h * 0.48, x + w * 0.70, y + h * 0.62],
                fill=(22, 22, 30))
    d.polygon([(x + w * 0.28, y + h * 0.48), (x + w * 0.50, y + h * 0.34),
               (x + w * 0.72, y + h * 0.48)], fill=(22, 22, 30))
    for r in range(2):
        for c in range(9):
            wx = x + w * (0.10 + c * 0.09)
            wy = y + h * (0.70 + r * 0.12)
            d.rectangle([wx, wy, wx + w * 0.045, wy + h * 0.05],
                        fill=(255, 196, 90))
    for c in range(5):
        fx = x + w * (0.36 + c * 0.07)
        d.line([(fx, y + h * 0.34), (fx, y + h * 0.48)], fill=(200, 200, 200))
        d.polygon([(fx, y + h * 0.34), (fx + w * 0.05, y + h * 0.37),
                   (fx, y + h * 0.40)], fill=[(200, 60, 60), (60, 120, 200),
                                               (240, 200, 60), (60, 160, 90),
                                               (220, 120, 40)][c])
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(16, 16, 22))


def art_bahrain(d, x, y, w, h):
    vgrad(d, x, y, w, h, (8, 12, 34), (34, 28, 62))
    for sx, sy in [(0.08, 0.12), (0.22, 0.07), (0.35, 0.16), (0.55, 0.08),
                   (0.70, 0.14), (0.86, 0.06), (0.93, 0.18), (0.45, 0.05)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2],
                  fill=(230, 230, 240))
    # base silhouettes
    d.rectangle([x + w * 0.04, y + h * 0.68, x + w * 0.30, y + h], fill=(14, 14, 20))
    d.rectangle([x + w * 0.62, y + h * 0.60, x + w * 0.96, y + h], fill=(14, 14, 20))
    d.rectangle([x + w * 0.36, y + h * 0.78, x + w * 0.56, y + h], fill=(18, 18, 26))
    for c in range(4):
        d.rectangle([x + w * (0.08 + c * 0.055), y + h * 0.74,
                     x + w * (0.105 + c * 0.055), y + h * 0.79], fill=(255, 200, 100))
    # missile arcs + bursts
    d.arc([x + w * 0.05, y + h * 0.05, x + w * 0.55, y + h * 0.75],
          start=200, end=330, fill=(255, 190, 80), width=2)
    d.arc([x + w * 0.45, y - h * 0.10, x + w * 1.0, y + h * 0.70],
          start=180, end=300, fill=(255, 210, 120), width=2)
    starburst(d, x + w * 0.30, y + h * 0.42, 13, 5, 8, (255, 150, 30))
    starburst(d, x + w * 0.30, y + h * 0.42, 7, 3, 8, (255, 220, 120))
    starburst(d, x + w * 0.78, y + h * 0.34, 11, 4, 8, (255, 140, 20))
    starburst(d, x + w * 0.78, y + h * 0.34, 6, 2, 8, (255, 215, 110))
    for cx, cy, r in [(0.30, 0.30, 9), (0.78, 0.24, 8), (0.55, 0.45, 6)]:
        d.ellipse([x + w * cx - r, y + h * cy - r * 0.7,
                   x + w * cx + r, y + h * cy + r * 0.7], fill=(90, 90, 100))
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(10, 10, 16))


def art_sparta(d, x, y, w, h):
    vgrad(d, x, y, w, h, (52, 62, 78), (120, 125, 135))
    # smoke column
    for i, (cx, cy, r) in enumerate([(0.58, 0.16, 10), (0.56, 0.24, 13),
                                     (0.60, 0.33, 16), (0.55, 0.42, 18)]):
        d.ellipse([x + w * cx - r, y + h * cy - r * 0.7,
                   x + w * cx + r, y + h * cy + r * 0.7],
                  fill=(48 + i * 6, 48 + i * 6, 52 + i * 6))
    # distant coast
    d.polygon([(x, y + h * 0.52), (x + w * 0.25, y + h * 0.46),
               (x + w * 0.45, y + h * 0.52), (x + w * 0.7, y + h * 0.47),
               (x + w, y + h * 0.52), (x + w, y + h * 0.58),
               (x, y + h * 0.58)], fill=(70, 78, 70))
    # sea
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=(24, 52, 84))
    for i in range(5):
        wy = y + h * (0.64 + i * 0.08)
        d.line([(x + w * 0.04, wy), (x + w * (0.30 + i * 0.06), wy)],
               fill=(120, 160, 200), width=1)
        d.line([(x + w * 0.68, wy + 3), (x + w * 0.96, wy + 3)],
               fill=(120, 160, 200), width=1)
    # ship hull + containers
    d.polygon([(x + w * 0.06, y + h * 0.66), (x + w * 0.94, y + h * 0.66),
               (x + w * 0.88, y + h * 0.80), (x + w * 0.12, y + h * 0.80)],
              fill=(20, 20, 26))
    d.rectangle([x + w * 0.72, y + h * 0.52, x + w * 0.82, y + h * 0.66],
                fill=(26, 26, 34))
    for c, col in enumerate([(150, 60, 50), (60, 110, 150), (180, 140, 60)]):
        d.rectangle([x + w * (0.14 + c * 0.13), y + h * 0.56,
                     x + w * (0.25 + c * 0.13), y + h * 0.66], fill=col)
    flames(d, x + w * 0.44, y + h * 0.30, w * 0.26, h * 0.36, seed=2)
    # rescue boat
    d.polygon([(x + w * 0.80, y + h * 0.86), (x + w * 0.94, y + h * 0.86),
               (x + w * 0.90, y + h * 0.92), (x + w * 0.84, y + h * 0.92)],
              fill=(230, 110, 30))
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(16, 30, 52))


def art_nepal(d, x, y, w, h):
    vgrad(d, x, y, w, h, (168, 200, 228), (238, 222, 190))
    # India Gate: piers + arch + dome
    d.rectangle([x + w * 0.34, y + h * 0.38, x + w * 0.42, y + h * 0.92],
                fill=(150, 120, 95))
    d.rectangle([x + w * 0.58, y + h * 0.38, x + w * 0.66, y + h * 0.92],
                fill=(150, 120, 95))
    d.rectangle([x + w * 0.30, y + h * 0.30, x + w * 0.70, y + h * 0.40],
                fill=(150, 120, 95))
    d.pieslice([x + w * 0.42, y + h * 0.30, x + w * 0.58, y + h * 0.62],
               start=180, end=360, fill=(168, 200, 228))
    d.ellipse([x + w * 0.45, y + h * 0.18, x + w * 0.55, y + h * 0.32],
              fill=(150, 120, 95))
    d.rectangle([x + w * 0.48, y + h * 0.12, x + w * 0.52, y + h * 0.20],
                fill=(150, 120, 95))
    # plane + contrail
    d.line([(x + w * 0.06, y + h * 0.16), (x + w * 0.30, y + h * 0.10)],
           fill=(255, 255, 255), width=2)
    d.polygon([(x + w * 0.30, y + h * 0.10), (x + w * 0.40, y + h * 0.08),
               (x + w * 0.36, y + h * 0.13)], fill=(240, 240, 240))
    # flags
    for fx, cols in [(0.10, [(255, 153, 51), (255, 255, 255), (19, 136, 8)]),
                     (0.86, [(220, 20, 60), (0, 56, 147)])]:
        px = x + w * fx
        d.line([(px, y + h * 0.55), (px, y + h * 0.92)], fill=(60, 60, 60))
        for i, col in enumerate(cols):
            d.rectangle([px, y + h * (0.55 + i * 0.05),
                         px + w * 0.09, y + h * (0.60 + i * 0.05)], fill=col)
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(120, 100, 80))


def art_power(d, x, y, w, h):
    vgrad(d, x, y, w, h, (10, 12, 28), (26, 28, 52))
    d.ellipse([x + w * 0.80, y + h * 0.10, x + w * 0.90, y + h * 0.24],
              fill=(235, 235, 220))
    d.pieslice([x + w * 0.78, y + h * 0.08, x + w * 0.90, y + h * 0.26],
               start=90, end=270, fill=(10, 12, 28))
    # skyline: left block dark (blackout), right block a few lit windows
    for bx, bw, bh in [(0.03, 0.16, 0.55), (0.21, 0.13, 0.72), (0.36, 0.18, 0.48)]:
        d.rectangle([x + w * bx, y + h * (1 - bh), x + w * (bx + bw), y + h],
                    fill=(8, 8, 12))
    for bx, bw, bh in [(0.56, 0.14, 0.66), (0.72, 0.17, 0.80), (0.91, 0.07, 0.55)]:
        d.rectangle([x + w * bx, y + h * (1 - bh), x + w * (bx + bw), y + h],
                    fill=(16, 16, 24))
        for r in range(3):
            for c in range(2):
                if (r + c) % 2 == 0:
                    wx = x + w * (bx + 0.03 + c * 0.06)
                    wy = y + h * (1 - bh + 0.08 + r * 0.16)
                    d.rectangle([wx, wy, wx + w * 0.03, wy + h * 0.05],
                                fill=(255, 196, 90))
    # transmission tower
    tx = x + w * 0.47
    d.polygon([(tx - w * 0.03, y + h), (tx, y + h * 0.30),
               (tx + w * 0.03, y + h)], fill=(40, 40, 50))
    d.line([(tx - w * 0.06, y + h * 0.38), (tx + w * 0.06, y + h * 0.38)],
           fill=(40, 40, 50), width=2)
    d.line([(tx - w * 0.08, y + h * 0.55), (tx + w * 0.08, y + h * 0.55)],
           fill=(40, 40, 50), width=2)
    d.line([(tx - w * 0.06, y + h * 0.38), (x + w * 0.02, y + h * 0.30)],
           fill=(70, 70, 85))
    d.line([(tx + w * 0.06, y + h * 0.38), (x + w * 0.98, y + h * 0.30)],
           fill=(70, 70, 85))
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(8, 8, 12))


def art_vote(d, x, y, w, h):
    vgrad(d, x, y, w, h, (214, 228, 240), (240, 238, 228))
    # skyline behind
    for bx, bw, bh in [(0.02, 0.12, 0.45), (0.16, 0.09, 0.60), (0.27, 0.13, 0.52),
                       (0.62, 0.11, 0.58), (0.76, 0.10, 0.42), (0.88, 0.10, 0.50)]:
        d.rectangle([x + w * bx, y + h * (0.95 - bh), x + w * (bx + bw), y + h * 0.95],
                    fill=(140, 155, 175))
    # ballot box
    d.rectangle([x + w * 0.38, y + h * 0.55, x + w * 0.66, y + h * 0.95],
                fill=(28, 58, 110))
    d.rectangle([x + w * 0.35, y + h * 0.50, x + w * 0.69, y + h * 0.57],
                fill=(20, 44, 86))
    d.rectangle([x + w * 0.46, y + h * 0.52, x + w * 0.58, y + h * 0.55],
                fill=(10, 10, 14))
    # ballot paper going in
    d.polygon([(x + w * 0.47, y + h * 0.52), (x + w * 0.57, y + h * 0.52),
               (x + w * 0.60, y + h * 0.28), (x + w * 0.50, y + h * 0.28)],
              fill=(255, 255, 255))
    d.line([(x + w * 0.51, y + h * 0.34), (x + w * 0.57, y + h * 0.34)],
           fill=(150, 150, 150))
    d.line([(x + w * 0.51, y + h * 0.40), (x + w * 0.56, y + h * 0.40)],
           fill=(150, 150, 150))
    # voter silhouettes queuing
    for vx, s in [(0.10, 1.0), (0.20, 0.92), (0.78, 0.95)]:
        cx = x + w * vx
        d.ellipse([cx - w * 0.035 * s, y + h * 0.62,
                   cx + w * 0.035 * s, y + h * 0.62 + h * 0.10 * s],
                  fill=(40, 40, 48))
        d.polygon([(cx - w * 0.05 * s, y + h * 0.95),
                   (cx - w * 0.045 * s, y + h * 0.72),
                   (cx + w * 0.045 * s, y + h * 0.72),
                   (cx + w * 0.05 * s, y + h * 0.95)], fill=(40, 40, 48))
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(120, 125, 135))


def art_mecca(d, x, y, w, h):
    vgrad(d, x, y, w, h, (8, 10, 30), (46, 32, 66))
    for sx, sy in [(0.06, 0.10), (0.18, 0.05), (0.30, 0.14), (0.44, 0.07),
                   (0.66, 0.12), (0.80, 0.06), (0.92, 0.15)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2],
                  fill=(230, 230, 240))
    # intercept burst + smoke trail arc
    d.arc([x + w * 0.30, y - h * 0.20, x + w * 0.90, y + h * 0.55],
          start=190, end=320, fill=(200, 200, 210), width=2)
    starburst(d, x + w * 0.62, y + h * 0.26, 14, 5, 10, (255, 170, 60))
    starburst(d, x + w * 0.62, y + h * 0.26, 8, 3, 10, (255, 235, 170))
    d.ellipse([x + w * 0.55, y + h * 0.10, x + w * 0.70, y + h * 0.20],
              fill=(70, 70, 85))
    # minaret skyline
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(16, 14, 24))
    for mx, mh in [(0.08, 0.55), (0.22, 0.42), (0.82, 0.50), (0.92, 0.38)]:
        px = x + w * mx
        d.rectangle([px - w * 0.018, y + h * (0.95 - mh), px + w * 0.018, y + h * 0.95],
                    fill=(16, 14, 24))
        d.rectangle([px - w * 0.035, y + h * (0.95 - mh + 0.10),
                     px + w * 0.035, y + h * (0.95 - mh + 0.13)], fill=(16, 14, 24))
        d.polygon([(px - w * 0.022, y + h * (0.95 - mh)),
                   (px, y + h * (0.95 - mh - 0.09)),
                   (px + w * 0.022, y + h * (0.95 - mh))], fill=(16, 14, 24))
    # dome
    d.pieslice([x + w * 0.42, y + h * 0.55, x + w * 0.58, y + h * 0.80],
               start=180, end=360, fill=(16, 14, 24))
    d.rectangle([x + w * 0.40, y + h * 0.78, x + w * 0.60, y + h * 0.95],
                fill=(16, 14, 24))
    for i in range(9):
        wx = x + w * (0.05 + i * 0.11)
        d.rectangle([wx, y + h * 0.80, wx + w * 0.03, y + h * 0.85],
                    fill=(255, 196, 90))
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(10, 10, 16))


def art_atp(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(36, 64, 110))
    d.rectangle([x + w * 0.08, y + h * 0.18, x + w * 0.92, y + h * 0.88],
                fill=(28, 96, 140))
    d.rectangle([x + w * 0.08, y + h * 0.18, x + w * 0.92, y + h * 0.88],
                outline=(255, 255, 255), width=2)
    d.line([(x + w * 0.50, y + h * 0.18), (x + w * 0.50, y + h * 0.88)],
           fill=(255, 255, 255), width=2)
    d.line([(x + w * 0.08, y + h * 0.53), (x + w * 0.92, y + h * 0.53)],
           fill=(255, 255, 255), width=2)
    # net
    d.rectangle([x + w * 0.08, y + h * 0.46, x + w * 0.92, y + h * 0.52],
                fill=(20, 20, 26))
    d.line([(x + w * 0.08, y + h * 0.46), (x + w * 0.92, y + h * 0.46)],
           fill=(255, 255, 255), width=2)
    # ball in flight
    d.ellipse([x + w * 0.68, y + h * 0.22, x + w * 0.78, y + h * 0.36],
              fill=(204, 255, 0))
    d.arc([x + w * 0.68, y + h * 0.22, x + w * 0.78, y + h * 0.36],
          start=200, end=340, fill=(255, 255, 255), width=1)
    # floodlight glare
    for gx in (0.06, 0.94):
        d.ellipse([x + w * gx - 5, y + 2, x + w * gx + 5, y + 12],
                  fill=(255, 255, 220))
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(20, 40, 70))


def art_f1(d, x, y, w, h):
    vgrad(d, x, y, w, h, (12, 12, 26), (52, 30, 74))
    # strip lights
    for i, col in enumerate([(255, 60, 120), (60, 200, 255), (255, 200, 60),
                             (120, 255, 140), (255, 120, 60)]):
        lx = x + w * (0.06 + i * 0.19)
        d.rectangle([lx, y + h * 0.06, lx + w * 0.13, y + h * 0.16], fill=col)
    # track curve
    d.arc([x - w * 0.30, y + h * 0.30, x + w * 0.90, y + h * 1.30],
          start=270, end=30, fill=(90, 90, 100), width=10)
    d.arc([x - w * 0.30, y + h * 0.30, x + w * 0.90, y + h * 1.30],
          start=270, end=30, fill=(200, 200, 60), width=1)
    # F1 car silhouette
    cx, cy = x + w * 0.42, y + h * 0.66
    d.polygon([(cx - w * 0.22, cy), (cx + w * 0.20, cy - h * 0.06),
               (cx + w * 0.30, cy + h * 0.02), (cx - w * 0.18, cy + h * 0.06)],
              fill=(200, 30, 40))
    d.rectangle([cx + w * 0.26, cy - h * 0.14, cx + w * 0.30, cy + h * 0.02],
                fill=(200, 30, 40))
    for wx in (-0.14, 0.12):
        d.ellipse([cx + w * wx - 7, cy - 2, cx + w * wx + 7, cy + 12],
                  fill=(12, 12, 14))
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(14, 14, 22))


def art_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 26, 34))
    # candlesticks
    bars = [(0.10, 0.55, 0.70, 1), (0.22, 0.40, 0.62, 1), (0.34, 0.62, 0.80, 0),
            (0.46, 0.30, 0.55, 1), (0.58, 0.48, 0.66, 0), (0.70, 0.26, 0.44, 1),
            (0.82, 0.42, 0.58, 0)]
    for bx, top, bot, up in bars:
        col = (60, 190, 110) if up else (220, 70, 60)
        d.rectangle([x + w * bx, y + h * top, x + w * (bx + 0.06), y + h * bot],
                    fill=col)
        d.line([(x + w * (bx + 0.03), y + h * (top - 0.08)),
                (x + w * (bx + 0.03), y + h * (bot + 0.08))], fill=col, width=1)
    # gold coin
    cx, cy, r = x + w * 0.50, y + h * 0.52, min(w, h) * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(212, 160, 40))
    d.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82],
              fill=(242, 190, 60))
    bf = F(SERIF_B, int(r * 1.05))
    d.text((cx, cy), "B", font=bf, fill=(146, 96, 10), anchor="mm")
    d.line([(cx - r * 0.28, cy - r * 0.75), (cx - r * 0.28, cy + r * 0.75)],
           fill=(146, 96, 10), width=2)
    d.line([(cx + r * 0.28, cy - r * 0.75), (cx + r * 0.28, cy + r * 0.75)],
           fill=(146, 96, 10), width=2)
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(16, 18, 24))


def art_somalia(d, x, y, w, h):
    vgrad(d, x, y, w, h, (150, 190, 220), (232, 222, 196))
    # sea band + coast
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(40, 110, 160))
    d.polygon([(x, y + h * 0.72), (x + w * 0.35, y + h * 0.66),
               (x + w * 0.7, y + h * 0.72), (x + w, y + h * 0.68),
               (x + w, y + h * 0.74), (x, y + h * 0.74)], fill=(222, 206, 170))
    # buildings
    for bx, bw, bh in [(0.05, 0.14, 0.30), (0.22, 0.11, 0.42), (0.36, 0.16, 0.26),
                       (0.68, 0.13, 0.36), (0.84, 0.12, 0.28)]:
        d.rectangle([x + w * bx, y + h * (0.72 - bh), x + w * (bx + bw), y + h * 0.72],
                    fill=(120, 105, 90))
    # flag: light blue + white star
    fx = x + w * 0.55
    d.line([(fx, y + h * 0.22), (fx, y + h * 0.72)], fill=(60, 60, 60))
    d.rectangle([fx, y + h * 0.22, fx + w * 0.16, y + h * 0.40],
                fill=(65, 137, 221))
    starburst(d, fx + w * 0.08, y + h * 0.31, 7, 3, 5, (255, 255, 255))
    # clock (deadline)
    cx, cy, r = x + w * 0.55, y + h * 0.52, min(w, h) * 0.16
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=(30, 30, 30), width=2)
    d.line([(cx, cy), (cx, cy - r * 0.62)], fill=(30, 30, 30), width=2)
    d.line([(cx, cy), (cx + r * 0.55, cy + r * 0.25)], fill=(30, 30, 30), width=2)
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(30, 80, 120))


def art_un(d, x, y, w, h):
    vgrad(d, x, y, w, h, (140, 180, 215), (225, 225, 220))
    # UN HQ slab
    d.rectangle([x + w * 0.36, y + h * 0.12, x + w * 0.64, y + h * 0.92],
                fill=(70, 95, 130))
    for r in range(8):
        for c in range(4):
            wx = x + w * (0.39 + c * 0.06)
            wy = y + h * (0.16 + r * 0.09)
            d.rectangle([wx, wy, wx + w * 0.04, wy + h * 0.05],
                        fill=(190, 210, 230))
    # low wing
    d.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.36, y + h * 0.92],
                fill=(110, 125, 140))
    d.rectangle([x + w * 0.64, y + h * 0.62, x + w * 0.94, y + h * 0.92],
                fill=(110, 125, 140))
    # flag row (French tricolore first)
    for i, cols in enumerate([[(0, 85, 164), (255, 255, 255), (239, 65, 53)],
                             [(65, 137, 221), (255, 255, 255)],
                             [(200, 60, 60), (255, 255, 255)],
                             [(60, 160, 90), (255, 255, 255)]]):
        fx = x + w * (0.10 + i * 0.20)
        d.line([(fx, y + h * 0.55), (fx, y + h * 0.92)], fill=(60, 60, 60))
        fw = w * 0.11
        for j, col in enumerate(cols):
            d.rectangle([fx, y + h * (0.55 + j * 0.05),
                         fx + fw, y + h * (0.60 + j * 0.05)], fill=col)
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(90, 100, 110))


def art_stadium(d, x, y, w, h):
    vgrad(d, x, y, w, h, (14, 16, 34), (40, 44, 66))
    # stands with crowd dots
    d.rectangle([x, y + h * 0.28, x + w, y + h * 0.62], fill=(28, 30, 48))
    for r in range(3):
        for c in range(14):
            px = x + w * (0.04 + c * 0.068)
            py = y + h * (0.33 + r * 0.09)
            col = [(220, 220, 220), (200, 60, 60), (240, 200, 60)][(r + c) % 3]
            d.ellipse([px, py, px + 2, py + 2], fill=col)
    # floodlights
    for gx in (0.08, 0.92):
        d.ellipse([x + w * gx - 6, y + h * 0.06, x + w * gx + 6, y + h * 0.06 + 12],
                  fill=(255, 255, 220))
        d.line([(x + w * gx, y + h * 0.06 + 12), (x + w * gx, y + h * 0.28)],
               fill=(150, 150, 160), width=1)
    # pitch
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(34, 128, 60))
    for i in range(6):
        sx = x + w * (i * 0.17)
        d.rectangle([sx, y + h * 0.62, sx + w * 0.085, y + h], fill=(40, 140, 68))
    d.ellipse([x + w * 0.38, y + h * 0.70, x + w * 0.62, y + h * 0.98],
              outline=(255, 255, 255), width=2)
    d.line([(x + w * 0.50, y + h * 0.62), (x + w * 0.50, y + h * 0.98)],
           fill=(255, 255, 255), width=2)
    d.ellipse([x + w * 0.46, y + h * 0.80, x + w * 0.53, y + h * 0.90],
              fill=(255, 255, 255), outline=(20, 20, 20))
    d.rectangle([x, y + h - 2, x + w, y + h], fill=(20, 80, 40))


ART = {
    "cop31": art_cop31, "bahrain": art_bahrain, "sparta": art_sparta,
    "nepal": art_nepal, "power": art_power, "vote": art_vote,
    "mecca": art_mecca, "atp": art_atp, "f1": art_f1,
    "bitcoin": art_bitcoin, "somalia": art_somalia, "un": art_un,
    "stadium": art_stadium,
}

# ---------------------------------------------------------------- world map
# Rough continent polygons (lon, lat). Deliberately coarse: the map is drawn
# as dots on a ~7-degree grid, so fine coastlines would not survive anyway.
POLYS = [
    # North America
    [(-168, 65), (-150, 70), (-130, 71), (-115, 69), (-100, 69), (-90, 68),
     (-85, 66), (-78, 71), (-75, 62), (-65, 60), (-55, 52), (-60, 47),
     (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26),
     (-84, 30), (-90, 29), (-97, 26), (-97, 21), (-94, 17), (-90, 14),
     (-86, 12), (-83, 9), (-79, 9), (-81, 13), (-87, 15), (-92, 15),
     (-97, 16), (-105, 20), (-110, 23), (-114, 28), (-120, 34), (-124, 40),
     (-124, 48), (-130, 54), (-135, 58), (-145, 60), (-155, 58), (-165, 60)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-65, -45), (-62, -41), (-58, -35), (-52, -32), (-48, -28),
     (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
     (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12),
     (-75, 10)],
    # Africa
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-6, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (30, 31), (32, 31), (34, 28), (35, 23), (37, 18),
     (39, 15), (43, 12), (48, 11), (51, 12), (46, 5), (42, 0), (40, -5),
     (40, -10), (36, -18), (33, -26), (28, -33), (20, -35), (17, -32),
     (15, -27), (13, -18), (12, -10), (9, -1), (9, 4), (-8, 5), (-13, 8),
     (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64),
     (12, 66), (18, 69), (25, 71), (30, 70), (35, 68), (40, 68), (45, 68),
     (50, 69), (55, 68), (60, 69), (65, 69), (70, 72), (75, 73), (80, 73),
     (90, 75), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 69), (170, 66), (178, 65), (178, 62), (170, 60),
     (162, 60), (158, 53), (156, 51), (150, 59), (142, 59), (142, 55),
     (140, 50), (135, 45), (130, 42), (127, 40), (122, 38), (120, 32),
     (122, 28), (120, 24), (114, 22), (110, 20), (108, 18), (106, 10),
     (104, 9), (101, 7), (98, 8), (97, 12), (94, 16), (92, 21), (89, 22),
     (86, 20), (83, 17), (80, 14), (77, 8), (76, 10), (73, 16), (70, 20),
     (66, 25), (62, 25), (58, 25), (57, 27), (54, 27), (52, 26), (50, 29),
     (48, 30), (44, 29), (42, 25), (39, 21), (36, 18), (35, 16), (33, 15),
     (36, 36), (33, 36), (30, 36), (27, 37), (23, 36), (19, 40), (15, 44),
     (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    # Arabia (separate blob so the Gulf reads)
    [(43, 12), (45, 13), (48, 14), (52, 15), (55, 17), (58, 20), (59, 22),
     (57, 25), (54, 26), (51, 28), (50, 29), (48, 30), (44, 29), (42, 25),
     (39, 21), (36, 18), (35, 16), (33, 15), (36, 17), (39, 14), (41, 13)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (140, -17), (136, -15), (135, -12), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (140, 38),
     (141, 41), (142, 44), (144, 44), (141, 40), (138, 37), (134, 34),
     (131, 32)],
    # New Zealand
    [(167, -45), (170, -42), (173, -40), (175, -38), (178, -37), (176, -40),
     (173, -42), (170, -44)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (50, -20), (47, -25), (44, -25),
     (43, -20)],
    # Indonesia (thin chain)
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -3), (135, -4), (140, -8), (138, -9), (130, -6),
     (120, -11), (110, -8), (100, -2), (95, 3)],
]


def _inside(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)):
            xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xint:
                inside = not inside
        j = i
    return inside


def on_land(lon, lat):
    return any(_inside(lon, lat, p) for p in POLYS)


def draw_map(d, x, y, w, h):
    """Dotted world map, equirectangular, lat 78..-58, plus numbered pins."""
    lat_top, lat_bot = 78.0, -58.0
    step = 5.0  # degrees per dot
    lon = -180.0
    while lon <= 180.0:
        lat = lat_top
        while lat >= lat_bot:
            if on_land(lon, lat):
                px = x + (lon + 180.0) / 360.0 * w
                py = y + (lat_top - lat) / (lat_top - lat_bot) * h
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                          fill=(96, 96, 96))
            lat -= step
        lon += step
    # pins for stories 01-13
    pf = F(SANS_B, 8)
    for i, (plon, plat) in enumerate(PINS, start=1):
        px = x + (plon + 180.0) / 360.0 * w
        py = y + (lat_top - plat) / (lat_top - lat_bot) * h
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py - 0.5), str(i), font=pf, fill=(255, 255, 255),
               anchor="mm")

# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top rules + kicker
    d.rectangle([MARGIN, 10, W - MARGIN, 11], fill=INK)
    d.rectangle([MARGIN, 13, W - MARGIN, 13], fill=INK)
    fk = F(SANS_B, 11)
    d.text((MARGIN, 18), "SUNDAY 22 NOVEMBER 2026", font=fk, fill=INK)
    rk = "28 STORIES  \u00b7  SEVEN REGIONS"
    d.text((W - MARGIN, 18), rk, font=fk, fill=RED, anchor="ra")

    # --- masthead
    fm = F(COND_B, 56)
    d.text((W // 2, 32), "THE WORLD TODAY", font=fm, fill=INK, anchor="ma")
    d.rectangle([MARGIN, 88, W - MARGIN, 89], fill=INK)

    # --- deck line
    fd = F(SERIF_I, 15)
    deck = ("COP31 nears a dawn deal  \u00b7  Iran strikes US bases in Bahrain  "
            "\u00b7  Sparta II still ablaze off Finland")
    assert fd.getlength(deck) <= CW, "deck too wide"
    d.text((W // 2, 94), deck, font=fd, fill=INK, anchor="ma")

    # --- stat strip: 6 cells
    sy, sh = 112, 36
    d.rectangle([MARGIN, sy, W - MARGIN, sy], fill=RULE)
    d.rectangle([MARGIN, sy + sh, W - MARGIN, sy + sh], fill=RULE)
    cellw = CW / 6.0
    fn = F(COND_B, 20)
    fl = F(SANS, 9)
    for i, (num, lab) in enumerate(STATS):
        cx = MARGIN + cellw * (i + 0.5)
        d.text((cx, sy + 3), num, font=fn, fill=INK, anchor="ma")
        assert fl.getlength(lab) <= cellw - 8, "stat label too wide: %s" % lab
        d.text((cx, sy + 24), lab, font=fl, fill=MIDGREY, anchor="ma")
        if i:
            x0 = MARGIN + cellw * i
            d.line([(x0, sy + 4), (x0, sy + sh - 4)], fill=RULE)

    # --- region chips (bordered, centred)
    fr = F(SANS_B, 10)
    chips = ["%s %d" % (name, n) for name, n in REGIONS]
    widths = [fr.getlength(c) + 14 for c in chips]
    total = sum(widths) + 6 * (len(chips) - 1)
    assert total <= CW
    cx = (W - total) / 2
    cy = 154
    for c, wdt in zip(chips, widths):
        d.rectangle([cx, cy, cx + wdt, cy + 16], outline=RULE)
        d.text((cx + wdt / 2, cy + 3), c, font=fr, fill=INK, anchor="ma")
        cx += wdt + 6

    # --- leads: 3 cards, h=200
    ly, lh = 176, 200
    lw, lgap = 322, 9
    fdl = F(SANS_B, 9)
    fhl = F(COND_B, 21)
    fbl = F(SERIF, 12)
    for i, (city, src, head, body, art) in enumerate(LEADS):
        x = MARGIN + i * (lw + lgap)
        d.rectangle([x, ly, x + lw, ly + lh], outline=RULE)
        ART[art](d, x + 1, ly + 1, lw - 2, 70)
        d.text((x + 8, ly + 76), city, font=fdl, fill=RED)
        sw = fdl.getlength(city + "  ")
        d.text((x + 8 + sw, ly + 76), src, font=fdl, fill=MIDGREY)
        hl = wrap(fhl, head, lw - 16, max_lines=2)
        hy = ly + 90
        for ln in hl:
            d.text((x + 8, hy), ln, font=fhl, fill=INK)
            hy += 22
        bl = wrap(fbl, body, lw - 16, max_lines=4)
        by = hy + 4
        for ln in bl:
            d.text((x + 8, by), ln, font=fbl, fill=INK)
            by += 14.5
        assert by <= ly + lh - 3, "lead %d overflows: end %.1f" % (i + 1, by)

    # --- features: 2 rows of 5, h=154
    fw, fgap = 192, 6
    fdf = F(SANS_B, 8)
    fhf = F(COND_B, 14)
    fbf = F(SERIF, 11)
    for row in range(2):
        fy = 380 + row * 158
        for col in range(5):
            j = row * 5 + col
            city, src, head, body, art = FEATURES[j]
            x = MARGIN + col * (fw + fgap)
            d.rectangle([x, fy, x + fw, fy + 154], outline=RULE)
            ART[art](d, x + 1, fy + 1, fw - 2, 46)
            d.text((x + 6, fy + 51), city, font=fdf, fill=RED)
            sw = fdf.getlength(city + "  ")
            assert x + 6 + sw + fdf.getlength(src) <= x + fw - 6, \
                "feature %d dateline too wide" % (j + 1)
            d.text((x + 6 + sw, fy + 51), src, font=fdf, fill=MIDGREY)
            hl = wrap(fhf, head, fw - 12, max_lines=2)
            hy = fy + 63
            for ln in hl:
                d.text((x + 6, hy), ln, font=fhf, fill=INK)
                hy += 16
            bl = wrap(fbf, body, fw - 12, max_lines=4)
            by = hy + 4
            for ln in bl:
                d.text((x + 6, by), ln, font=fbf, fill=INK)
                by += 13
            assert by <= fy + 154 - 2, "feature %d overflows: end %.1f" % (j + 1, by)

    # --- bottom split: map left, briefs right
    by0 = 696
    fbt = F(SANS_B, 11)
    d.text((MARGIN, by0), "WHERE THE NEWS IS", font=fbt, fill=INK)
    d.text((362, by0), "BRIEFS 14\u201328", font=fbt, fill=INK)
    d.rectangle([MARGIN, by0 + 15, 350, by0 + 15], fill=INK)
    d.rectangle([362, by0 + 15, W - MARGIN, by0 + 15], fill=INK)
    draw_map(d, MARGIN, by0 + 22, 330, 236)
    d.text((MARGIN, by0 + 256), "Numbered pins mark stories 01\u201313.",
           font=F(SERIF_I, 10), fill=MIDGREY)

    # briefs: 2 columns, 8 + 7
    fbn = F(SANS_B, 11.5)
    fbb = F(SERIF, 11.5)
    cols = [(362, 312, BRIEFS[:8]), (686, 318, BRIEFS[8:])]
    for colx, colw, items in cols:
        yy = by0 + 22
        for k, (city, text) in enumerate(items):
            num = 14 + (BRIEFS.index((city, text)))
            prefix = "%d \u00b7 %s \u2014 " % (num, city)
            pw = fbn.getlength(prefix)
            first_w = colw - pw
            # wrap text: first line fits first_w, rest colw
            words = text.split(" ")
            lines, cur, first = [], "", True
            for wrd in words:
                trial = (cur + " " + wrd).strip()
                lim = first_w if first else colw
                if fbb.getlength(trial) <= lim:
                    cur = trial
                else:
                    lines.append(cur)
                    cur, first = wrd, False
            if cur:
                lines.append(cur)
            assert len(lines) <= 2, "brief %d wraps to %d lines: %s" % (
                num, len(lines), lines)
            d.text((colx, yy), prefix, font=fbn, fill=RED)
            d.text((colx + pw, yy), lines[0], font=fbb, fill=INK)
            if len(lines) > 1:
                d.text((colx, yy + 13.5), lines[1], font=fbb, fill=INK)
            yy += 30
        assert yy <= by0 + 270, "brief column overflows: end %.1f" % yy

    # --- DATE CHECK box
    dy = 964
    d.rectangle([MARGIN, dy, W - MARGIN, dy + 40], outline=RULE)
    fdt = F(SANS_B, 9)
    d.text((MARGIN + 8, dy + 3), "DATE CHECK \u2014 EARLIER STORIES DELIBERATELY LEFT OUT",
           font=fdt, fill=RED)
    fdi = F(SERIF, 10)
    joined = "  \u00b7  ".join(DATECHECK)
    dl = wrap(fdi, joined, CW - 16, max_lines=2)
    assert len(dl) <= 2, "datecheck wraps to %d lines" % len(dl)
    yy = dy + 15
    for ln in dl:
        d.text((MARGIN + 8, yy), ln, font=fdi, fill=MIDGREY)
        yy += 12
    assert yy <= dy + 40, "datecheck box overflow"

    # --- footer
    ff = F(SANS, 8)
    foot = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 ANI \u00b7 euronews \u00b7 IANS "
            "\u00b7 RFE/RL \u00b7 Straits Times \u00b7 Anadolu "
            "\u00b7 Iran International \u00b7 Times of India  \u2014  "
            "All stories verified against Sunday 22 November 2026 reporting; "
            "forecasts flagged FORECAST.")
    assert ff.getlength(foot) <= CW, "footer too wide"
    d.text((W // 2, 1006), foot, font=ff, fill=MIDGREY, anchor="ma")

    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    data = open(out, "rb").read()
    print("wrote %s (%d bytes)" % (out, len(data)))
    print("sha256 %s" % hashlib.sha256(data).hexdigest())
    assert len(data) <= 1048576, "entry.png over 1 MiB"
    assert img.size == (1024, 1024)


if __name__ == "__main__":
    main()
