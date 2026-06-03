"""
rcparams_text_map.py
====================
A combined matplotlib typography & styling reference, in three bands:

  TOP    — which rcParam sets the SIZE of each text element. Every text element
           in the sample plot is coloured by the rcParam that controls it (x- and
           y-axis labels share a colour because both are `axes.labelsize`), with a
           colour-matched key of the parameter names.
  MIDDLE — what the line-width, line-style and marker-size choices look like
           (lines.linewidth / linestyle / lines.markersize). Rarely mandated by
           journals, so the point is just to SEE the options.
  BOTTOM — three typefaces (Arial, Times New Roman, Computer Modern) at a few
           sizes, plus italic, bold and a math formula — sans vs serif vs the
           LaTeX face, the same text and equation rendered in each.

Colours are the SciencePlots "high-vis" cycle (github.com/garrettj403/SciencePlots).

Output: ../figures/rcparams_text_map.png / .pdf
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties, findfont

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

HIGHVIS = ["#0d49fb", "#e6091c", "#26eb47", "#8936df", "#fec32d", "#25d7fd"]

# one distinct colour per controlling rcParam (high-vis hues, darkened where
# needed so small text stays legible; two extras round out the eight)
C = {
    "figure.titlesize":      "#0d49fb",   # high-vis blue
    "axes.titlesize":        "#e6091c",   # high-vis red
    "axes.labelsize":        "#8936df",   # high-vis purple  (x AND y axis labels)
    "xtick.labelsize":       "#1a9e30",   # high-vis green (darkened)
    "ytick.labelsize":       "#0e9ec4",   # high-vis cyan (darkened)
    "legend.fontsize":       "#b8860b",   # high-vis yellow (darkened to gold)
    "legend.title_fontsize": "#c2185b",   # crimson (extra)
    "font.size":             "#555555",   # grey  (extra; generic text / fallback base)
}

# exaggerated, clearly-different sizes so the text hierarchy is obvious
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "figure.titlesize": 19, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 10.5, "ytick.labelsize": 10.5,
    "legend.fontsize": 12, "legend.title_fontsize": 12, "font.size": 11,
    "axes.linewidth": 1.0, "lines.linewidth": 2.0,
})
INK, SUB, ACCENT = "#1f2a37", "#6b7280", "#2563b8"

# typeface specimen fonts (fall back to a bundled face if Arial/Times absent)
FP_TIMES = FontProperties(fname=findfont("Times New Roman"))
FP_TIMES_I = FontProperties(family="Times New Roman", style="italic")
FP_TIMES_B = FontProperties(family="Times New Roman", weight="bold")
FP_ARIAL = FontProperties(fname=findfont("Arial"))
FP_ARIAL_I = FontProperties(family="Arial", style="italic")
FP_ARIAL_B = FontProperties(family="Arial", weight="bold")
FP_CM = FontProperties(fname=findfont("cmr10"))
FP_CMB = FontProperties(fname=findfont("cmb10"))

fig = plt.figure(figsize=(11.8, 12.7))
gs = fig.add_gridspec(3, 1, height_ratios=[5.0, 3.1, 3.0], hspace=0.40,
                      left=0.085, right=0.965, top=0.85, bottom=0.05)
gtop = gs[0].subgridspec(1, 2, width_ratios=[1.08, 1.0], wspace=0.10)
ax = fig.add_subplot(gtop[0])
key = fig.add_subplot(gtop[1]); key.axis("off")
gmid = gs[1].subgridspec(1, 3, wspace=0.12)
bw, bs, bm = [fig.add_subplot(gmid[i]) for i in range(3)]
for a in (bw, bs, bm):
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis("off")
spec = fig.add_subplot(gs[2]); spec.axis("off")

# ===================== TOP: text element -> rcParam map =====================
x = np.linspace(0, 10, 200)
ax.plot(x, np.sin(x), color="#3a3a3a", label="signal A")
ax.plot(x, 0.7 * np.cos(x), color="#9a9a9a", ls="--", label="signal B")

ax.set_title("Axes title  ·  ax.set_title()", color=C["axes.titlesize"], fontweight="bold")
ax.set_xlabel("x-axis label (unit)", color=C["axes.labelsize"])
ax.set_ylabel("y-axis label (unit)", color=C["axes.labelsize"])
# boxed look matching convention.mplstyle: inward ticks on all four sides + minor ticks
ax.tick_params(axis="both", which="both", color="#888888", direction="in", top=True, right=True)
ax.tick_params(axis="x", labelcolor=C["xtick.labelsize"])
ax.tick_params(axis="y", labelcolor=C["ytick.labelsize"])
ax.minorticks_on()
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_color("#888888")

# frameless legend (convention.mplstyle). NB: entries are coloured by rcParam role
# (legend.fontsize / legend.title_fontsize) for the map, not line-coloured.
leg = ax.legend(title="Legend title", loc="upper right", frameon=False)
for t in leg.get_texts():
    t.set_color(C["legend.fontsize"])
leg.get_title().set_color(C["legend.title_fontsize"])

ax.text(0.035, 0.07, "Text annotation  ·  ax.text()", transform=ax.transAxes,
        color=C["font.size"], style="italic")

fig.suptitle("Figure title  ·  fig.suptitle()", x=0.31, y=0.905,
             color=C["figure.titlesize"], fontweight="bold")

# key (parameter names in matching colours)
key.set_xlim(0, 1); key.set_ylim(0, 1)
key.text(0.0, 1.0, "Which rcParam sets each text size", fontsize=14,
         fontweight="bold", color=INK, va="top")
rows = [
    ("figure.titlesize",       "figure title — fig.suptitle()"),
    ("axes.titlesize",         "axes title — ax.set_title()"),
    ("axes.labelsize",         "x- and y-axis labels (both)"),
    ("xtick.labelsize",        "x tick labels"),
    ("ytick.labelsize",        "y tick labels"),
    ("legend.fontsize",        "legend entries"),
    ("legend.title_fontsize",  "legend title"),
    ("font.size",              "other text; base others fall back to"),
]
y = 0.885
for param, desc in rows:
    col = C[param]
    key.plot([0.0, 0.035], [y - 0.012, y - 0.012], color=col, lw=4,
             solid_capstyle="round", clip_on=False)
    key.text(0.055, y, param, color=col, fontweight="bold", fontsize=12.5,
             family="monospace", va="top")
    key.text(0.055, y - 0.045, f"{mpl.rcParams[param]:g} pt  →  {desc}",
             color=col, fontsize=10, va="top")
    y -= 0.112
key.text(0.0, -0.02,
         "Typeface of every element: font.family / font.sans-serif.\n"
         "Weights: axes.titleweight · axes.labelweight · figure.titleweight.\n"
         "Also: figure.labelsize → fig.supxlabel()/supylabel().",
         fontsize=8.6, color=SUB, va="top")

# ===================== MIDDLE: line / style / marker choices =================
bw.set_title("Line width  ·  lines.linewidth", fontsize=12, fontweight="bold", color=INK, pad=8)
for yy, lw in zip(np.linspace(0.80, 0.10, 6), [0.5, 0.75, 1.0, 1.5, 2.0, 3.0]):
    bw.plot([0.36, 0.97], [yy, yy], lw=lw, color=HIGHVIS[0], solid_capstyle="round")
    bw.text(0.0, yy, f"{lw:g} pt", va="center", ha="left", fontsize=10.5, color=INK)

bs.set_title("Line style  ·  linestyle (ls)", fontsize=12, fontweight="bold", color=INK, pad=8)
for yy, (nm, ls) in zip(np.linspace(0.76, 0.14, 4),
                        [("solid", "-"), ("dashed", "--"), ("dotted", ":"), ("dash-dot", "-.")]):
    bs.plot([0.48, 0.97], [yy, yy], lw=1.9, ls=ls, color=HIGHVIS[1], solid_capstyle="round")
    bs.text(0.0, yy, f"{nm}  '{ls}'", va="center", ha="left", fontsize=10.5, color=INK)

bm.set_title("Marker size  ·  lines.markersize", fontsize=12, fontweight="bold", color=INK, pad=8)
for yy, ms in zip(np.linspace(0.76, 0.14, 5), [3, 5, 7, 9, 12]):
    bm.plot([0.64], [yy], marker="o", ms=ms, color=HIGHVIS[3],
            markeredgecolor="white", markeredgewidth=0.8)
    bm.text(0.0, yy, f"ms = {ms}", va="center", ha="left", fontsize=10.5, color=INK)

fig.text(0.52, bm.get_position().y0 - 0.018,
         "Line width / style / marker size are rarely journal-mandated — choose for legibility at "
         "final size (thicker / larger for talks); vary style and shape so it reads in grayscale.",
         ha="center", va="top", fontsize=8.8, color=SUB)

# ===================== BOTTOM: three-typeface specimen =======================
cw, ch = 250, 72
spec.set_xlim(0, cw); spec.set_ylim(0, ch)
spec.text(0, ch, "Typeface  ·  font.family / font.sans-serif  —  sans vs serif vs the LaTeX face",
          fontsize=12, fontweight="bold", color=INK, va="top")
speccols = [("Arial  (sans-serif)",       FP_ARIAL, FP_ARIAL_I, FP_ARIAL_B, "stixsans"),
            ("Times New Roman  (serif)",   FP_TIMES, FP_TIMES_I, FP_TIMES_B, "stix"),
            ("Computer Modern  (LaTeX)",   FP_CM,    None,       FP_CMB,     "cm")]
srows = [("Large · 12 pt", 12, "reg"), ("Regular · 9 pt", 9, "reg"),
         ("Small · 7 pt", 7, "reg"), ("italic", 9, "ital"),
         ("bold", 9, "bold"), ("math formula", 11, "math")]
TXT, FORMULA = "Sample 0123", r"$E=mc^2$"
colx = [44, 122, 196]
yhdr = ch - 14
for cj, (nm, reg, ital, bold, mset) in enumerate(speccols):
    cx = colx[cj]
    spec.text(cx, yhdr, nm, fontproperties=bold, fontsize=10.5, color=ACCENT, va="center", ha="left")
    for ri, (lab, fs, kind) in enumerate(srows):
        ry = yhdr - 11 - ri * 8.4
        if cj == 0:
            spec.text(0, ry, lab, fontsize=8.5, color=SUB, va="center", ha="left", style="italic")
        if kind == "reg":
            spec.text(cx, ry, TXT, fontproperties=reg, fontsize=fs, color=INK, va="center", ha="left")
        elif kind == "bold":
            spec.text(cx, ry, TXT, fontproperties=bold, fontsize=fs, color=INK, va="center", ha="left")
        elif kind == "ital":
            if ital is not None:
                spec.text(cx, ry, TXT, fontproperties=ital, fontsize=fs, color=INK, va="center", ha="left")
            else:   # Computer Modern italic via mathtext
                spec.text(cx, ry, r"$Sample\ 0123$", math_fontfamily="cm", fontsize=fs,
                          color=INK, va="center", ha="left")
        else:
            spec.text(cx, ry, FORMULA, math_fontfamily=mset, fontsize=fs, color=INK, va="center", ha="left")

# faint dividers between the three bands (placed from the actual axes positions)
div1 = (ax.get_position().y0 + bw.get_position().y1) / 2
div2 = (bw.get_position().y0 + spec.get_position().y1) / 2
for dy in (div1, div2):
    fig.add_artist(Line2D([0.085, 0.965], [dy, dy], color="#dde1e6", lw=1.0))

# ---- annotate the figure's OWN size (set by figsize) with dimension lines ----
ov = fig.add_axes([0, 0, 1, 1]); ov.set_xlim(0, 1); ov.set_ylim(0, 1)
ov.axis("off"); ov.set_zorder(12); ov.patch.set_alpha(0)
DIM = "#3b4a5c"
_ap = dict(arrowstyle="<|-|>", color=DIM, lw=1.1, shrinkA=0, shrinkB=0, mutation_scale=11)
ov.annotate("", (0.02, 0.965), (0.98, 0.965), arrowprops=_ap)                  # width (top)
for _x in (0.02, 0.98):
    ov.plot([_x, _x], [0.965, 0.955], color=DIM, lw=0.8)
ov.text(0.5, 0.974, f"figure width  ·  figsize[0] = {fig.get_figwidth():g} in",
        ha="center", va="bottom", color=DIM, fontsize=10.5, fontweight="bold")
ov.annotate("", (0.026, 0.022), (0.026, 0.96), arrowprops=_ap)                 # height (left)
for _y in (0.022, 0.96):
    ov.plot([0.026, 0.039], [_y, _y], color=DIM, lw=0.8)
ov.text(0.011, 0.49, f"figure height  ·  figsize[1] = {fig.get_figheight():g} in",
        ha="center", va="center", color=DIM, fontsize=10.5, fontweight="bold", rotation=90)

fig.savefig(OUT / "rcparams_text_map.pdf", bbox_inches="tight", pad_inches=0.06)
fig.savefig(OUT / "rcparams_text_map.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
print("wrote rcparams_text_map.png and .pdf (text-map + line/marker demo + typeface specimen)")
