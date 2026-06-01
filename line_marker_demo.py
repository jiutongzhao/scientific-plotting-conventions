"""
line_marker_demo.py
===================
A visual reference: what different line widths, line styles and marker sizes
actually look like. These are rarely mandated by journals, so the point is to
let you SEE the choices rather than prescribe them. Colours are the SciencePlots
"high-vis" cycle (github.com/garrettj403/SciencePlots).

Output: line_marker_demo.png / .pdf
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

HIGHVIS = ["#0d49fb", "#e6091c", "#26eb47", "#8936df", "#fec32d", "#25d7fd"]
mpl.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "font.size": 11,
})
INK, SUB = "#1f2a37", "#6b7280"

fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.9))
for a in axes:
    a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis("off")

# ---- panel 1: line width ----------------------------------------------------
ax = axes[0]
ax.set_title("Line width  ·  lines.linewidth", fontsize=12, fontweight="bold",
             color=INK, pad=10)
lws = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
for y, lw in zip(np.linspace(0.84, 0.12, len(lws)), lws):
    ax.plot([0.34, 0.97], [y, y], lw=lw, color=HIGHVIS[0], solid_capstyle="round")
    ax.text(0.0, y, f"{lw:g} pt", va="center", ha="left", fontsize=10.5, color=INK)

# ---- panel 2: line style ----------------------------------------------------
ax = axes[1]
ax.set_title("Line style  ·  linestyle (ls)", fontsize=12, fontweight="bold",
             color=INK, pad=10)
styles = [("solid", "-"), ("dashed", "--"), ("dotted", ":"), ("dash-dot", "-.")]
for y, (nm, ls) in zip(np.linspace(0.80, 0.16, len(styles)), styles):
    ax.plot([0.46, 0.97], [y, y], lw=1.9, ls=ls, color=HIGHVIS[1], solid_capstyle="round")
    ax.text(0.0, y, f"{nm}  '{ls}'", va="center", ha="left", fontsize=10.5, color=INK)

# ---- panel 3: marker size ---------------------------------------------------
ax = axes[2]
ax.set_title("Marker size  ·  lines.markersize", fontsize=12, fontweight="bold",
             color=INK, pad=10)
mss = [3, 5, 7, 9, 12]
for y, ms in zip(np.linspace(0.80, 0.16, len(mss)), mss):
    ax.plot([0.62], [y], marker="o", ms=ms, color=HIGHVIS[3],
            markeredgecolor="white", markeredgewidth=0.8)
    ax.text(0.0, y, f"ms = {ms}", va="center", ha="left", fontsize=10.5, color=INK)

fig.text(0.5, 0.015,
         "Rarely journal-mandated — choose for legibility at final size; go thicker / larger "
         "for slides and posters. Vary line style and marker shape too, so a figure still reads "
         "in grayscale.", ha="center", va="bottom", fontsize=8.8, color=SUB)

fig.subplots_adjust(left=0.02, right=0.99, top=0.86, bottom=0.12, wspace=0.12)
fig.savefig("line_marker_demo.pdf", bbox_inches="tight", pad_inches=0.06)
fig.savefig("line_marker_demo.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
print("wrote line_marker_demo.png and .pdf")
