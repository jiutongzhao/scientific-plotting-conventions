"""
rcparams_text_map.py
====================
A combined matplotlib styling reference:

  TOP  — which rcParam sets the SIZE of each text element. Every text element in
         the sample plot is coloured by the rcParam that controls it (x- and
         y-axis labels share a colour because both are `axes.labelsize`), with a
         colour-matched key of the parameter names.
  BOTTOM — what the line-width, line-style and marker-size choices look like
         (lines.linewidth / linestyle / lines.markersize). These are rarely
         mandated by journals, so the point is to SEE the options.

Colours are the SciencePlots "high-vis" cycle (github.com/garrettj403/SciencePlots).

Output: rcparams_text_map.png / .pdf
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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
INK, SUB = "#1f2a37", "#6b7280"

fig = plt.figure(figsize=(11.8, 9.4))
gs = fig.add_gridspec(2, 1, height_ratios=[5.0, 3.1], hspace=0.34,
                      left=0.085, right=0.965, top=0.85, bottom=0.085)
gtop = gs[0].subgridspec(1, 2, width_ratios=[1.08, 1.0], wspace=0.10)
ax = fig.add_subplot(gtop[0])
key = fig.add_subplot(gtop[1]); key.axis("off")
gbot = gs[1].subgridspec(1, 3, wspace=0.12)
bw, bs, bm = [fig.add_subplot(gbot[i]) for i in range(3)]
for a in (bw, bs, bm):
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis("off")

# ===================== TOP: text element -> rcParam map =====================
x = np.linspace(0, 10, 200)
ax.plot(x, np.sin(x), color="#3a3a3a", label="signal A")
ax.plot(x, 0.7 * np.cos(x), color="#9a9a9a", ls="--", label="signal B")

ax.set_title("Axes title  ·  ax.set_title()", color=C["axes.titlesize"], fontweight="bold")
ax.set_xlabel("x-axis label (unit)", color=C["axes.labelsize"])
ax.set_ylabel("y-axis label (unit)", color=C["axes.labelsize"])
ax.tick_params(axis="both", color="#888888")
ax.tick_params(axis="x", labelcolor=C["xtick.labelsize"])
ax.tick_params(axis="y", labelcolor=C["ytick.labelsize"])
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#888888")

leg = ax.legend(title="Legend title", loc="upper right")
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

# ===================== BOTTOM: line / style / marker choices =================
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

fig.text(0.52, 0.0,
         "Line width / style / marker size are rarely journal-mandated — choose for legibility at "
         "final size (thicker / larger for talks); vary style and shape so it reads in grayscale.",
         ha="center", va="bottom", fontsize=8.8, color=SUB)

# faint divider between the two halves
fig.add_artist(Line2D([0.085, 0.965], [0.405, 0.405], color="#dde1e6", lw=1.0))

# ---- annotate the figure's OWN size (set by figsize) with dimension lines ----
ov = fig.add_axes([0, 0, 1, 1]); ov.set_xlim(0, 1); ov.set_ylim(0, 1)
ov.axis("off"); ov.set_zorder(12); ov.patch.set_alpha(0)
DIM = "#3b4a5c"
_ap = dict(arrowstyle="<|-|>", color=DIM, lw=1.1, shrinkA=0, shrinkB=0, mutation_scale=11)
ov.annotate("", (0.02, 0.955), (0.98, 0.955), arrowprops=_ap)                  # width (top)
for _x in (0.02, 0.98):
    ov.plot([_x, _x], [0.955, 0.942], color=DIM, lw=0.8)
ov.text(0.5, 0.967, f"figure width  ·  figsize[0] = {fig.get_figwidth():g} in",
        ha="center", va="bottom", color=DIM, fontsize=10.5, fontweight="bold")
ov.annotate("", (0.026, 0.03), (0.026, 0.95), arrowprops=_ap)                  # height (left)
for _y in (0.03, 0.95):
    ov.plot([0.026, 0.039], [_y, _y], color=DIM, lw=0.8)
ov.text(0.011, 0.49, f"figure height  ·  figsize[1] = {fig.get_figheight():g} in",
        ha="center", va="center", color=DIM, fontsize=10.5, fontweight="bold", rotation=90)

fig.savefig("rcparams_text_map.pdf", bbox_inches="tight", pad_inches=0.06)
fig.savefig("rcparams_text_map.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
print("wrote rcparams_text_map.png and .pdf (combined text-map + line/marker demo)")
