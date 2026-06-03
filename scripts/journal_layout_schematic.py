"""
journal_layout_schematic.py
===========================
A clean schematic of a two-column journal article page, showing how single- and
double-column figures are inserted into the text grid.

Dimensions follow the *Nature branded research journals — Guide to preparing
final artwork*:
    research figures :  1-column = 88 mm | 2-column = 180 mm | gutter 4 mm
    text             :  sans-serif (Helvetica/Arial), 5-7 pt
    line art         :  vector (AI/EPS/PDF), editable text
    photos           :  bitmap >= 300 dpi
    max fig height   :  caption-length dependent (see spec card)

Output: journal_layout_schematic.pdf (vector) and .png (preview).
"""

from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- style ----
mpl.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
})

# ---------------------------------------------------------------- palette --
INK     = "#1f2a37"   # primary ink (titles, dark bars)
SUB     = "#6b7280"   # secondary text
ACCENT  = "#2563b8"   # dimensions, badges, UI accent
WARN    = "#b3261e"   # "avoid"
BODY    = "#d8dde3"   # greeked body-text lines
GUIDE   = "#e7ebef"   # margin / gutter guides
FIGEDGE = "#d7dde4"   # figure frame
CANVAS  = "#eef1f4"   # page background
CARD    = "#ffffff"
CARDED  = "#e2e7ec"
W_BLUE  = "#0072B2"   # Wong palette for figure content
W_ORNG  = "#E69F00"

# ---------------------------------------------------- page geometry (mm) ---
W, H   = 210.0, 276.0
ML, MR = 15.0, 15.0
MT, MB = 17.0, 18.0
GUT    = 4.0
COL    = (W - ML - MR - GUT) / 2            # 88 mm
C1 = (ML, ML + COL)                         # 15 .. 103
C2 = (ML + COL + GUT, W - MR)               # 107 .. 195
FULL = (ML, W - MR)                         # 15 .. 195  (180 mm)

def Yp(t):                                   # mm-from-page-top -> data y
    return H - t

# ---------------------------------------------------------------- canvas ---
fig, ax = plt.subplots(figsize=(11.6, 9.6))
ax.set_xlim(-12, 356)
ax.set_ylim(-10, 312)
ax.set_aspect("equal")
ax.axis("off")
ax.add_patch(Rectangle((-12, -10), 368, 322, facecolor=CANVAS,
                       edgecolor="none", zorder=-5))

# ---------------------------------------------------------------- helpers --
def pbox(x0, x1, t0, t1, **kw):
    ax.add_patch(Rectangle((x0, Yp(t1)), x1 - x0, t1 - t0, **kw))

def greek(x0, x1, t0, t1, lh=3.0, lw=1.1, color=BODY):
    width, i, t = x1 - x0, 0, t0
    while t <= t1:
        end = (i % 7 == 6)
        frac = (0.42 + 0.40 * ((i * 37) % 5) / 4) if end else 1.0
        ax.hlines(Yp(t), x0, x0 + width * frac, lw=lw, color=color,
                  zorder=2, capstyle="round")
        t += lh + (1.7 if end else 0.0)
        i += 1

def caption(x0, x1, t0, num, n=4, lh=2.5):
    ax.text(x0, Yp(t0), f"Figure {num}", fontsize=6.6, fontweight="bold",
            color=INK, va="top", ha="left")
    ax.hlines(Yp(t0 + 0.4), x0 + 13.5, x1, lw=1.1, color="#aeb5bd",
              capstyle="round")
    for k in range(1, n):
        frac = 0.5 if k == n - 1 else 1.0
        ax.hlines(Yp(t0 + k * lh), x0, x0 + (x1 - x0) * frac, lw=1.0,
                  color=BODY, capstyle="round")

def dim_h(x0, x1, y, label, ext=2.4, above=True):
    for xx in (x0, x1):
        ax.plot([xx, xx], [y - ext, y + ext], color=ACCENT, lw=0.7, zorder=5)
    ax.annotate("", (x0, y), (x1, y), zorder=5,
                arrowprops=dict(arrowstyle="<|-|>", color=ACCENT, lw=0.9,
                                mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y + (2.6 if above else -2.6), label, color=ACCENT,
            fontsize=7.2, ha="center", va=("bottom" if above else "top"),
            fontweight="bold", zorder=6)

def dim_v(x, y0, y1, label, ext=2.4):
    for yy in (y0, y1):
        ax.plot([x - ext, x + ext], [yy, yy], color=ACCENT, lw=0.7, zorder=5)
    ax.annotate("", (x, y0), (x, y1), zorder=5,
                arrowprops=dict(arrowstyle="<|-|>", color=ACCENT, lw=0.9,
                                mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(x - 3.0, (y0 + y1) / 2, label, color=ACCENT, fontsize=6.8,
            ha="center", va="center", rotation=90, fontweight="bold", zorder=6)

def inset(x0, x1, t0, t1):
    a = ax.inset_axes([x0, Yp(t1), x1 - x0, t1 - t0], transform=ax.transData)
    a.set_zorder(4)
    return a

def badge(x, y, n, r=3.4):
    ax.add_patch(Circle((x, y), r, facecolor=ACCENT, edgecolor="white",
                        lw=1.0, zorder=8))
    ax.text(x, y - 0.1, str(n), ha="center", va="center", color="white",
            fontsize=6.6, fontweight="bold", zorder=9)

# ============================================================== the page ===
# soft drop shadow + page sheet
ax.add_patch(Rectangle((3, -3), W, H, facecolor="#0b1320", alpha=0.07,
                       edgecolor="none", zorder=0))
pbox(0, W, 0, H, facecolor="white", edgecolor="#c9cfd6", lw=1.0, zorder=1)

# margin / column guides
for gx in (ML, ML + COL, ML + COL + GUT, W - MR):
    ax.plot([gx, gx], [Yp(MT), Yp(H - MB)], color=GUIDE, lw=0.7,
            ls=(0, (5, 4)), zorder=1)

# masthead: title / authors / affiliation
pbox(ML, ML + 150, 20.0, 24.4, facecolor=INK, ec="none")
pbox(ML, ML + 112, 26.6, 30.4, facecolor=INK, ec="none")
ax.hlines(Yp(35.4), ML, ML + 128, lw=1.6, color=ACCENT, capstyle="round")
ax.hlines(Yp(38.8), ML, ML + 96,  lw=1.0, color="#9aa1a9", capstyle="round")

# abstract / standfirst block
pbox(*FULL, 43, 58, facecolor="#f3f6f9", edgecolor="#e6ebf0", lw=0.8)
ax.text(ML + 2.0, Yp(45.2), "Abstract", fontsize=6.6, fontweight="bold",
        color=INK, va="top")
for k in range(4):
    fr = 0.62 if k == 3 else 1.0
    ax.hlines(Yp(49.4 + k * 2.5), ML + 2.0, ML + (180 - 4) * fr, lw=1.0,
              color="#c2c9d1", capstyle="round")

# ---- Figure 1 : single column (right column, top) ----
F1 = dict(x0=C2[0], x1=C2[1], t0=64, t1=104)
pbox(F1["x0"], F1["x1"], F1["t0"], F1["t1"], facecolor="#fcfdfe",
     edgecolor=FIGEDGE, lw=0.9, zorder=3)
a1 = inset(F1["x0"] + 5, F1["x1"] - 4, F1["t0"] + 6, F1["t1"] - 5)
rng = np.random.default_rng(3)
a1.bar(range(5), rng.uniform(0.45, 1.0, 5), color=W_BLUE, width=0.66)
a1.set_ylim(0, 1.12); a1.set_xticks([]); a1.set_yticks([])
for s in ("top", "right"):
    a1.spines[s].set_visible(False)
for s in ("left", "bottom"):
    a1.spines[s].set_linewidth(0.8); a1.spines[s].set_color("#9aa1a9")
caption(F1["x0"], F1["x1"], 107, num=1, n=4)
dim_h(F1["x0"], F1["x1"], Yp(123), "1-column · 88 mm")

# ---- Figure 2 : double column (full width, lower) ----
F2 = dict(x0=FULL[0], x1=FULL[1], t0=150, t1=205)
pbox(F2["x0"], F2["x1"], F2["t0"], F2["t1"], facecolor="#fcfdfe",
     edgecolor=FIGEDGE, lw=0.9, zorder=3)
# panel a — vector line plot
aa = inset(24, 100, 161, 200)
xx = np.linspace(0, 2 * np.pi, 200)
aa.plot(xx, np.sin(xx), color=W_BLUE, lw=1.6)
aa.plot(xx, np.cos(xx), color=W_ORNG, lw=1.6, ls=(0, (4, 2)))
aa.set_xticks([]); aa.set_yticks([])
for s in ("top", "right"):
    aa.spines[s].set_visible(False)
for s in ("left", "bottom"):
    aa.spines[s].set_linewidth(0.8); aa.spines[s].set_color("#9aa1a9")
# panel b — bitmap "photo"
ab = inset(112, 188, 161, 200)
zz = np.add.outer(np.sin(np.linspace(0, 3, 90)), np.cos(np.linspace(0, 3.4, 90)))
ab.imshow(zz, cmap="viridis", aspect="auto", rasterized=True)
ab.set_xticks([]); ab.set_yticks([])
ab.text(0.965, 0.07, "300 dpi", transform=ab.transAxes, fontsize=5.6,
        ha="right", va="bottom", color="white")
ax.text(26, Yp(157), "a", fontsize=8.5, fontweight="bold", color=INK,
        va="center", ha="center", zorder=6)
ax.text(114, Yp(157), "b", fontsize=8.5, fontweight="bold", color=INK,
        va="center", ha="center", zorder=6)
caption(F2["x0"], F2["x1"], 208, num=2, n=4)
dim_h(F2["x0"], F2["x1"], Yp(146), "2-column (full width) · 180 mm")
dim_v(10.5, Yp(F2["t1"]), Yp(F2["t0"]), "max height")

# ---- simulated body text ----
greek(*C1, 64, 142)
greek(*C2, 132, 142)
greek(*C1, 222, 258)
greek(*C2, 222, 258)

# ---- minor grid dimensions (in the clear gap below the 1-column dim, so the
#      label doesn't fall behind a figure panel) ----
dim_h(C1[1], C2[0], Yp(128), "", ext=1.2)
ax.text((C1[1] + C2[0]) / 2 + 4.5, Yp(128), "4 mm gutter", color=ACCENT,
        fontsize=6.0, ha="left", va="center", fontweight="bold")
dim_h(0, W, Yp(269), "210 mm trim", above=False)

# ---- numbered badges on the page (always top-right of their target) ----
badge(191.5, Yp(67.5),  1)   # Fig 1  — single-column figure
badge(191.5, Yp(152.5), 2)   # Fig 2  — double-column figure
badge(96.0,  Yp(157.0), 3)   # panel a — vector line art
badge(182.0, Yp(157.0), 4)   # panel b — bitmap photo
badge(191.5, Yp(108.5), 5)   # Fig 1 caption

# ============================================== header (top-left, clean) ===
ax.text(-10, 305, "Anatomy of a journal page",
        fontsize=15, fontweight="bold", color=INK, va="bottom")
ax.text(-10, 296.5, "How single- and double-column figures are inserted into the "
        "two-column research-article grid", fontsize=8.6, color=SUB, va="bottom")
ax.plot([-10, 150], [292, 292], color=ACCENT, lw=2.0, solid_capstyle="round")

# ============================================ right column: legend + spec ===
LX0, LX1 = 232, 352

# --- card 1: numbered legend ---
ax.add_patch(FancyBboxPatch((LX0, 184), LX1 - LX0, 104,
             boxstyle="round,pad=0,rounding_size=4", facecolor=CARD,
             edgecolor=CARDED, lw=1.0, zorder=3))
ax.text(LX0 + 6, 281, "Reading the page", fontsize=9.5, fontweight="bold",
        color=INK, va="center", zorder=4)
ax.plot([LX0 + 6, LX1 - 6], [274.5, 274.5], color="#eef1f4", lw=1.0, zorder=4)

legend = [
    (1, "Single-column figure", "88 mm wide, set at a column top"),
    (2, "Double-column figure", "180 mm, multi-panel (label a, b)"),
    (3, "Vector line art", "AI / EPS / PDF — text stays editable"),
    (4, "Photo / bitmap panel", "raster image, ≥ 300 dpi at final size"),
    (5, "Figure caption", 'bold "Figure n" lead, below panel'),
]
ly = 270
for n, title, desc in legend:
    badge(LX0 + 11, ly, n)
    ax.text(LX0 + 19, ly + 1.4, title, fontsize=8.0, fontweight="bold",
            color=INK, va="center", zorder=4)
    ax.text(LX0 + 19, ly - 3.4, desc, fontsize=6.6, color=SUB, va="center",
            zorder=4)
    ly -= 20.0

# --- card 2: spec sheet ---
ax.add_patch(FancyBboxPatch((LX0, 42), LX1 - LX0, 132,
             boxstyle="round,pad=0,rounding_size=4", facecolor=CARD,
             edgecolor=CARDED, lw=1.0, zorder=3))
sx = LX0 + 6
ax.text(sx, 166, "Nature final-artwork specs", fontsize=9.5, fontweight="bold",
        color=INK, va="center", zorder=4)
ax.plot([sx, LX1 - 6], [159.5, 159.5], color="#eef1f4", lw=1.0, zorder=4)

cur = {"y": 152}
def line(txt, dy=5.2, color=INK, size=7.2, weight="normal", fam="sans-serif",
         x=None):
    ax.text(sx if x is None else x, cur["y"], txt, fontsize=size, color=color,
            fontweight=weight, family=fam, va="center", zorder=4)
    cur["y"] -= dy

def head(txt):
    cur["y"] -= 1.2
    line(txt, dy=5.6, color=ACCENT, size=7.6, weight="bold")

head("Figure widths")
line("research:  88 / 180 mm")
line("review:    58 / 121 / 185 mm")
head("Max height (by caption length)")
line("caption     1-col   2-col", size=6.8, fam="monospace", color=SUB)
line("< 300 w      130     185 mm", size=6.8, fam="monospace")
line("< 150 w      180     210 mm", size=6.8, fam="monospace")
line("<  50 w      220     225 mm", size=6.8, fam="monospace")
head("Text")
line("sans-serif (Helvetica / Arial)")
line("5–7 pt  (max 7, min 5)")
head("Formats")
line("line art → vector AI/EPS/PDF")
line("photos → bitmap ≥ 300 dpi")
head("Colour")
line("RGB research  /  CMYK other")
cur["y"] -= 1.6
line("Avoid JPG/PNG/TIFF line art,", color=WARN, size=6.8)
line("drop-shadow & 3-D effects", color=WARN, size=6.8)

# source note
ax.text(-10, -7, "Grid and dimensions per Nature branded research journals’ "
        "guide to preparing final artwork.", fontsize=7, color=SUB, va="center")

fig.savefig(OUT / "journal_layout_schematic.pdf", bbox_inches="tight", pad_inches=0.15)
fig.savefig(OUT / "journal_layout_schematic.png", dpi=200, bbox_inches="tight",
            pad_inches=0.15)
print("wrote journal_layout_schematic.pdf and .png")
